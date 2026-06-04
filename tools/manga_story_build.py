#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""manga_story_build.py — generic story JSON -> 4-koma strip (4 language variants).

Generalizes manga_q25_build.py: the panel geometry proven by the #25 pilot is the
fixed template; a story JSON (written by an LLM agent per article) supplies the
text + per-panel visual motif. Output is static-only SVG (no SMIL) = imgix-safe.

Story schema (per language in story["langs"][lang]):
    {"title": str, "header": "line1\\nline2",
     "panels": [
       {"caption": str|null, "motif": MOTIF|null, "bubble": str},          # x3
       {"caption": null, "motif": null, "bubble": "punch\\nline",
        "caption_box": "lesson1\\nlesson2", "foot": str}                   # panel 4
     ]}
MOTIF is one of:
    {"circles": [{"label": "name", "fill": "#hex"?}, ...]}        # 2-8
    {"flow": ["box1", "box2", ...]}                               # 2-4
    {"burst": {"big": str, "badge": "two\\nlines"?}}
    {"duo": [{"label": "a\\n52%", "fill": "#hex"}, {...}], "extinct": int?}

Usage:  py -3.11 tools/manga_story_build.py <story.json> [more.json ...]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

FULLSENSE = Path(__file__).resolve().parents[1]
MANGAMD = Path("D:/projects/manga-md-poc")
sys.path.insert(0, str(MANGAMD))

import mangamd_poc  # noqa: E402

OUT_DIR = FULLSENSE / "docs" / "articles" / "assets" / "manga"
SRC_DIR = OUT_DIR / "src"

FONTS = {
    "ja": "'Yu Gothic','Noto Sans CJK JP',sans-serif",
    "en": "'Segoe UI','Noto Sans',sans-serif",
    "zh": "'Microsoft YaHei','Noto Sans CJK SC',sans-serif",
    "ko": "'Malgun Gothic','Noto Sans CJK KR',sans-serif",
}
PASTELS = ["#ffe2a8", "#cfe6ff", "#e8d5ff", "#d5ffd9",
           "#ffd5d5", "#fff3c4", "#d9f2ff", "#ffe0f0"]
PANELS = [(140, 640), (660, 1160), (1180, 1680), (1700, 2200)]


def rect(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def tb(shape, text, origin, size, font, fill="#ffffff", border=True,
       border_width=3, text_color="#1a1a1a", line_gap=None, tail=None,
       border_color="#1a1a1a"):
    b = {"shape": shape, "text": text, "writing": "horizontal", "font": font,
         "font_size": size, "text_origin": origin, "fill": fill,
         "border": border, "border_color": border_color,
         "border_width": border_width, "text_color": text_color}
    if line_gap:
        b["line_gap"] = line_gap
    if tail:
        b["tail"] = tail
    return {"bubble": b}


def nlines(s: str) -> int:
    return s.count("\n") + 1


def _bust(els: list, cx: float, cy: float, k: float, sx: int,
          hair: str = "#4a3826", skin: str = "#fbd7b5", cloth: str = "#5a6e8c") -> tuple[float, float]:
    """説明役の半身 (バスト)。sx=-1 で左向き (右側に置く)、+1 で右向き (左側に置く)。

    manga_grammar.md: フキダシには必ず話者を立て、尻尾を口元へ。戻り値 = 口元座標。
    k = 頭半径スケール (基準 r=68 のサンプル比)。
    """
    r = 68 * k
    shapes = [
        {"shape": {"circle": [cx - 10 * sx, cy - 28 * k, 86 * k]}, "fill": hair},   # 後ろ髪
        {"shape": {"circle": [cx, cy, r]}, "fill": skin},                            # 顔
        {"shape": {"circle": [cx + 37 * sx * k, cy - 50 * k, 30 * k]}, "fill": hair},  # 前髪
        {"shape": {"circle": [cx - 5 * sx * k, cy - 60 * k, 33 * k]}, "fill": hair},
        {"shape": {"circle": [cx - 47 * sx * k, cy - 46 * k, 29 * k]}, "fill": hair},
        {"path": f"M {cx + 52 * sx * k} {cy - 20 * k} q {-12 * sx * k} -8 {-24 * sx * k} -2",
         "fill": "none", "stroke": "#3a2c20", "stroke_width": max(2.5, 4 * k)},      # 眉
        {"shape": {"circle": [cx + 38 * sx * k, cy - 4 * k, 6 * k]}, "fill": "#3a2c20"},  # 目
        {"shape": {"ellipse": [cx + 55 * sx * k, cy + 28 * k, 13 * k, 16 * k]},
         "fill": "#8e3b35"},                                                          # 開いた口
        {"path": f"M {cx - 85 * k} {cy + 225 * k} Q {cx - 85 * k} {cy + 100 * k} {cx} {cy + 95 * k} "
                 f"Q {cx + 85 * k} {cy + 100 * k} {cx + 85 * k} {cy + 225 * k} Z", "fill": cloth},  # 体
        {"path": f"M {cx - 15 * k} {cy + 110 * k} L {cx} {cy + 134 * k} L {cx + 15 * k} {cy + 110 * k}",
         "fill": "#ffffff"},                                                          # 襟
    ]
    els.append({"draw": {"shapes": shapes}})
    return (cx + 55 * sx * k, cy + 28 * k)  # 口元 (尻尾アンカー)


def speech(text: str, cx: float, cy: float, rx: float, ry: float, size: int, font: str,
           tail_to: tuple[float, float] | None = None, kind: str = "speech",
           seed: float = 1.0, bw: int = 3) -> dict:
    """speech/shout フキダシ (一体型尻尾)。テキストは中央揃え。"""
    lines = nlines(text)
    oy = cy + size * 0.35 - (lines - 1) * (size * 1.25) / 2
    b = {"kind": kind, "shape": {"ellipse": [cx, cy, rx, ry]}, "text": text,
         "writing": "horizontal", "font": font, "font_size": size,
         "text_origin": [cx, oy], "fill": "#ffffff", "border": True,
         "border_color": "#1a1a1a", "border_width": bw, "text_color": "#1a1a1a",
         "line_gap": size * 1.25, "seed": seed}
    if tail_to:
        b["tail_to"] = list(tail_to)
    return {"bubble": b}


def auto_text_color(fill: str) -> str:
    """White text on dark fills, near-black on light fills (WCAG-ish luminance)."""
    try:
        h = fill.lstrip("#")
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        return "#ffffff" if (0.299 * r + 0.587 * g + 0.114 * b) < 150 else "#1a1a1a"
    except Exception:
        return "#1a1a1a"


def render_motif(els, motif, y0, y1, font, lang):
    """Render one motif into the zone between caption (y0+110) and 話者/フキダシ帯 (y1-170)."""
    if not motif:
        return
    zone_top, zone_bot = y0 + 112, y1 - 170
    mid_y = (zone_top + zone_bot) // 2
    if "circles" in motif:
        items = motif["circles"][:8]
        n = len(items)
        rows = [items] if n <= 4 else [items[: (n + 1) // 2], items[(n + 1) // 2:]]
        row_ys = [mid_y] if len(rows) == 1 else [zone_top + 75, zone_top + 235]
        for row, cy in zip(rows, row_ys):
            k = len(row)
            span = 760 / (k + 1)
            for j, it in enumerate(row):
                cx = span * (j + 1)
                label = it.get("label", "")
                two = "\n" in label
                size = 19 - (3 if max(len(x) for x in label.split("\n")) > 6 else 0)
                if lang in ("en", "ko"):
                    size = max(12, size - 3)
                oy = cy - 4 if two else cy + 7
                fill = it.get("fill") or PASTELS[(j + (0 if cy == row_ys[0] else 4)) % 8]
                els.append(tb({"circle": [cx, cy, 62]}, label, [cx, oy], size, font,
                              fill=fill, border_width=3, line_gap=size * 1.2,
                              text_color=auto_text_color(fill)))
    elif "flow" in motif:
        boxes = motif["flow"][:4]
        bh, gap = 58, 34
        total = len(boxes) * bh + (len(boxes) - 1) * gap
        y = mid_y - total // 2
        for j, label in enumerate(boxes):
            els.append(tb({"polygon": rect(150, y, 610, y + bh)}, label,
                          [380, y + bh / 2 + 7], 21, font, fill="#fffbe8",
                          border_width=3))
            if j < len(boxes) - 1:
                ay = y + bh + 4
                els.append(tb({"polygon": [[368, ay], [392, ay], [380, ay + gap - 8]]},
                              "", [0, 0], 1, font, fill="#1a1a1a", border=False))
            y += bh + gap
    elif "burst" in motif:
        # 集中線はコマの枠から生やす (r_outer をコマ外 + clip)。揺らぎ・間引き・白フチは
        # mangamd v2 既定。大文字は叫びフキダシ (尻尾なし=インパクトワード)。
        # 旧 union 黄バッジは廃止 (意味不明な部品 — feedback_manga_craft_integration)。
        b = motif["burst"]
        els.append({"effect": {"concentration_lines": {
            "center": [380, mid_y - 10], "n": 52, "r_inner": 150, "r_outer": 720,
            "color": "#2a2417", "width": 4.2, "jitter": 0.7, "skip": 0.13,
            "fringe": "#ffffff", "clip": [25, y0 + 8, 710, (y1 - y0) - 16]}}})
        big = b.get("big", "")
        size = 46 if len(big) <= 8 else 34
        els.append(speech(big, 380, mid_y - 10, 195, 92, size, font, kind="shout",
                          seed=11, bw=4))
        if b.get("badge"):
            bl = nlines(b["badge"])
            els.append(tb({"polygon": rect(540, zone_bot - 60 - bl * 24, 716, zone_bot - 36)},
                          b["badge"], [628, zone_bot - 44 - bl * 24 + 20], 17, font,
                          fill="#fffbe8", border_width=2, line_gap=22))
    elif "duo" in motif:
        a, c = motif["duo"][0], motif["duo"][1]
        cy = zone_top + 130
        for (it, cx, r, size) in ((a, 250, 95, 24), (c, 510, 92, 20)):
            if lang in ("en", "ko"):
                size = max(14, size - 4)
            els.append(tb({"circle": [cx, cy, r]}, it.get("label", ""),
                          [cx, cy - 10], size, font,
                          fill=it.get("fill", "#ffe2a8"), border_width=4,
                          line_gap=size * 1.3,
                          text_color=auto_text_color(it.get("fill", "#ffe2a8"))))
        ext = int(motif.get("extinct") or 0)
        if ext > 0:
            ey = cy + 145
            for k in range(min(ext, 6)):
                cx = 120 + k * 104
                els.append(tb({"circle": [cx, ey, 32]}, "×", [cx, ey + 11], 28, font,
                              fill="#d9d4c8", border_width=2,
                              border_color="#8a8474", text_color="#6a645a"))


def build(slug: str, lang: str, spec: dict) -> dict:
    f = FONTS[lang]
    els: list[dict] = []
    els.append(tb({"polygon": rect(24, 18, 736, 118)}, spec["header"], [380, 58],
                  26 if lang != "en" else 24, f, fill="#2b2317", border=False,
                  text_color="#f7efdd", line_gap=40))
    for y0, y1 in PANELS:
        els.append(tb({"polygon": rect(20, y0, 740, y1)}, "", [0, 0], 1, f,
                      fill="#ffffff", border=True, border_width=5))

    panels = spec["panels"]
    # panels 1-3: caption (ナレーション箱) / motif (説明内容) / 話者バスト + speech フキダシ
    # 話者を左右交互に置いて単調さを避ける (p1 右, p2 左, p3 右)
    for i in range(3):
        p = panels[i]
        y0, y1 = PANELS[i]
        if p.get("caption"):
            cap_size = 22 if lang != "en" else 19
            els.append(tb({"polygon": rect(40, y0 + 20, 720, y0 + 92)}, p["caption"],
                          [380, y0 + 63], cap_size, f, fill="#fffbe8",
                          border_width=3, line_gap=28))
        render_motif(els, p.get("motif"), y0, y1, f, lang)
        if p.get("bubble"):
            right = i != 1  # p2 のみ左
            sx = -1 if right else 1
            bx = 640 if right else 120
            mouth = _bust(els, bx, y1 - 148, 0.62, sx)
            if i == 2:  # 転 (フリ) のコマ: こめかみに汗 (1 コマ 1 漫符)
                els.append({"manpu": {"kind": "sweat",
                                      "at": [bx - 60 * sx, y1 - 188], "s": 22,
                                      "seed": 3.0 + i}})
            two = nlines(p["bubble"]) > 1
            bsize = 24 if lang != "en" else 20
            bcx = 290 if right else 470
            els.append(speech(p["bubble"], bcx, y1 - 92, 205, 60 if two else 48,
                              bsize, f, tail_to=mouth, seed=5.0 + i))

    # panel 4 (結): 叫びフキダシ (オチ) + 集中線は話者に収束 + 教訓ナレーション箱
    p4 = panels[3]
    y0, y1 = PANELS[3]
    els.append({"effect": {"concentration_lines": {
        "center": [628, y0 + 330], "n": 56, "r_inner": 230, "r_outer": 820,
        "color": "#2a2417", "width": 4.0, "jitter": 0.7, "skip": 0.13,
        "fringe": "#ffffff", "clip": [25, y0 + 8, 710, (y1 - y0) - 16]}}})
    mouth4 = _bust(els, 628, y0 + 330, 0.66, -1)
    psize = 26 if lang != "en" else 22
    els.append(speech(p4.get("bubble", ""), 300, y0 + 120, 240, 78, psize, f,
                      kind="shout", tail_to=mouth4, seed=9, bw=4))
    if p4.get("caption_box"):
        c_lines = nlines(p4["caption_box"])
        c_oy = (y0 + 415) - (c_lines - 1) * 16
        els.append(tb({"polygon": rect(48, y0 + 360, 470, y0 + 478)}, p4["caption_box"],
                      [259, c_oy], 19 if lang != "en" else 16, f, fill="#efe7d2",
                      border_width=2, line_gap=30))
    if p4.get("foot"):
        els.append(tb({"polygon": rect(376, 2086, 384, 2090)}, p4["foot"],
                      [259, y0 + 498 - 6], 17, f, fill="#f5efe2", border=False,
                      text_color="#6a645a"))
    els.append(tb({"polygon": rect(376, 2156, 384, 2160)},
                  "mangamd L0 / FullSense", [380, 2180], 13, f,
                  fill="#f5efe2", border=False, text_color="#8a8474"))
    return {"title": spec.get("title", f"{slug} 4-koma"),
            "canvas": {"w": 760, "h": 2300, "bg": "#f5efe2"},
            "elements": els}


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    from xml.dom import minidom
    for story_path in argv[1:]:
        story = json.loads(Path(story_path).read_text(encoding="utf-8"))
        slug = story["slug"]
        (SRC_DIR / f"{slug}_story.json").write_text(
            json.dumps(story, ensure_ascii=False, indent=1), encoding="utf-8")
        for lang in ("ja", "en", "zh", "ko"):
            spec = story["langs"][lang]
            panel = build(slug, lang, spec)
            suffix = "" if lang == "ja" else f"_{lang}"
            out = OUT_DIR / f"{slug}_4koma{suffix}.svg"
            svg = mangamd_poc.render(panel)
            minidom.parseString(svg.encode("utf-8"))  # fail-closed
            out.write_bytes(svg.encode("utf-8"))
            print(f"wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
