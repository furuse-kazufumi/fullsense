#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""manga_q25_build.py — QIITA #25 (monoculture) 4-koma strip, 4 language variants.

Builds declarative panel JSON (mangamd L0 DSL) for ja/en/zh/ko and renders them
via manga-md-poc's generator into docs/articles/assets/manga/.

Layout is defined ONCE; only the text dictionary varies per language, so the
four variants stay geometrically identical (feedback_multilingual_article_structure:
every language section gets its own translated SVG variant).

Usage:  py -3.11 tools/manga_q25_build.py
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

# --------------------------------------------------------------------------- #
# Per-language text (everything that differs between variants lives here)
# --------------------------------------------------------------------------- #
TEXT = {
    "ja": {
        "title": "4コマでわかる #25 — AI 500 世代進化の「大失敗」",
        "header": "4コマでわかる #25\nAI 500 世代進化の「大失敗」",
        "p1_cap": "世界を代表する 8 つの知性を、種として AI に蒔いた",
        "names": ["古瀬", "フリストン", "ミリッジ", "磯村",
                  "岡潔", "グロタン\nディーク", "ノイマン", "ファインマン"],
        "p1_foot": "最強知性の進化バトル、開始！",
        "p2_big": "500 世代",
        "p2_badge": "best_score\n1.0",
        "p2_bubble": "全員満点!? なんて強さだ…!",
        "p3_cap": "500 世代後——生き残ったのは 2 人だけ",
        "p3_a": "古瀬\n52%",
        "p3_b": "フリストン\n48%",
        "p3_bubble": "これが進化の力…！",
        "p4_bubble": "違います。\n選択圧ゼロの『くじ引き』でした",
        "p4_cap": "全員 100 点のテストでは、席次は決まらない。\n「測る」(lleval) の次に必要なのは\n「淘汰する」(lldarwin) だった",
        "p4_foot": "→ 詳しくは本編で（この下から）",
    },
    "en": {
        "title": "4-panel digest #25 — the 'great failure' of evolving an AI for 500 generations",
        "header": "4-panel digest #25\nEvolving an AI 500 generations: a \"great failure\"",
        "p1_cap": "We seeded 8 of the world's great minds into the AI",
        "names": ["Furuse", "Friston", "Millidge", "Isomura",
                  "Kiyoshi\nOka", "Grothen-\ndieck", "von\nNeumann", "Feynman"],
        "p1_foot": "Battle of the smartest minds — begin!",
        "p2_big": "500 gens",
        "p2_badge": "best_score\n1.0",
        "p2_bubble": "Everyone scores perfect!? What power...!",
        "p3_cap": "After 500 generations — only two survived",
        "p3_a": "Furuse\n52%",
        "p3_b": "Friston\n48%",
        "p3_bubble": "Behold, the power of evolution...!",
        "p4_bubble": "Nope. With zero selection pressure,\nit was just a lottery.",
        "p4_cap": "A test everyone aces ranks no one.\nAfter \"measuring\" (lleval), what we needed\nwas \"culling\" (lldarwin)",
        "p4_foot": "→ Full story below",
    },
    "zh": {
        "title": "4格速读 #25 — 把 AI 进化 500 代的“大失败”",
        "header": "4格速读 #25\n把 AI 进化 500 代的“大失败”",
        "p1_cap": "把世界级的 8 位智者作为种子播进 AI",
        "names": ["古濑", "弗里斯顿", "米利奇", "矶村",
                  "冈洁", "格罗滕\n迪克", "冯·诺依曼", "费曼"],
        "p1_foot": "最强智者的进化之战，开始！",
        "p2_big": "500 代",
        "p2_badge": "best_score\n1.0",
        "p2_bubble": "全员满分!? 太强了…!",
        "p3_cap": "500 代之后——只剩 2 人幸存",
        "p3_a": "古濑\n52%",
        "p3_b": "弗里斯顿\n48%",
        "p3_bubble": "这就是进化的力量…！",
        "p4_bubble": "不对。选择压为零，\n这只是一场抽签。",
        "p4_cap": "人人 100 分的考试排不出名次。\n会“测量”(lleval) 之后，\n还需要会“淘汰”(lldarwin)",
        "p4_foot": "→ 详见下方正文",
    },
    "ko": {
        "title": "4컷 다이제스트 #25 — AI를 500세대 진화시킨 '대실패'",
        "header": "4컷 다이제스트 #25\nAI를 500세대 진화시킨 '대실패'",
        "p1_cap": "세계적인 지성 8인을 씨앗으로 AI에 심었다",
        "names": ["후루세", "프리스턴", "밀리지", "이소무라",
                  "오카", "그로텐디크", "폰 노이만", "파인만"],
        "p1_foot": "최강 지성들의 진화 배틀, 시작!",
        "p2_big": "500 세대",
        "p2_badge": "best_score\n1.0",
        "p2_bubble": "전원 만점!? 이런 강함이…!",
        "p3_cap": "500세대 후—— 살아남은 건 단 2명",
        "p3_a": "후루세\n52%",
        "p3_b": "프리스턴\n48%",
        "p3_bubble": "이것이 진화의 힘…!",
        "p4_bubble": "아닙니다. 선택압이 0이라\n그저 '제비뽑기'였습니다.",
        "p4_cap": "전원 100점인 시험으론 순위가 안 나온다.\n'측정'(lleval) 다음에 필요한 것은\n'도태'(lldarwin)였다",
        "p4_foot": "→ 자세한 이야기는 아래 본문에서",
    },
}

# pastel fills for the 8 seed-persona circles
SEED_FILLS = ["#ffe2a8", "#cfe6ff", "#e8d5ff", "#d5ffd9",
              "#ffd5d5", "#fff3c4", "#d9f2ff", "#ffe0f0"]


def rect(x0: float, y0: float, x1: float, y1: float) -> list[list[float]]:
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def text_bubble(shape: dict, text: str, origin: list[float], size: int, font: str,
                fill: str = "#ffffff", border: bool = True, border_width: int = 3,
                text_color: str = "#1a1a1a", line_gap: float | None = None,
                tail: list[list[float]] | None = None,
                border_color: str = "#1a1a1a") -> dict:
    b: dict = {
        "shape": shape, "text": text, "writing": "horizontal", "font": font,
        "font_size": size, "text_origin": origin, "fill": fill,
        "border": border, "border_color": border_color, "border_width": border_width,
        "text_color": text_color,
    }
    if line_gap:
        b["line_gap"] = line_gap
    if tail:
        b["tail"] = tail
    return {"bubble": b}


def build(lang: str) -> dict:
    t = TEXT[lang]
    f = FONTS[lang]
    els: list[dict] = []

    # header band
    els.append(text_bubble({"polygon": rect(24, 18, 736, 118)}, t["header"],
                           [380, 58], 28, f, fill="#2b2317", border=False,
                           text_color="#f7efdd", line_gap=40))

    # 4 panel frames (white, manga border)
    for y0, y1 in [(140, 640), (660, 1160), (1180, 1680), (1700, 2200)]:
        els.append(text_bubble({"polygon": rect(20, y0, 740, y1)}, "",
                               [0, 0], 1, f, fill="#ffffff", border=True,
                               border_width=5))

    # ---- Panel 1 (起): seed the 8 minds -----------------------------------
    els.append(text_bubble({"polygon": rect(40, 160, 720, 232)}, t["p1_cap"],
                           [380, 203], 23, f, fill="#fffbe8", border_width=3))
    name_size = {"ja": 19, "en": 16, "zh": 19, "ko": 16}[lang]
    for i, name in enumerate(t["names"]):
        cx = [110, 290, 470, 650][i % 4]
        cy = 330 if i < 4 else 490
        two_line = "\n" in name
        oy = cy - 4 if two_line else cy + 7
        size = name_size - (3 if len(name.replace("\n", "")) > 6 else 0)
        els.append(text_bubble({"circle": [cx, cy, 62]}, name, [cx, oy], size, f,
                               fill=SEED_FILLS[i], border_width=3, line_gap=size * 1.2))
    els.append(text_bubble({"polygon": rect(376, 596, 384, 600)}, t["p1_foot"],
                           [380, 622], 23, f, fill="#ffffff", border=False))

    # ---- Panel 2 (承): 500 generations, everyone perfect -------------------
    els.append({"effect": {"concentration_lines": {
        "center": [380, 880], "n": 44, "r_inner": 105, "r_outer": 240,
        "color": "#2a2417", "width": 5}}})
    els.append(text_bubble({"polygon": rect(250, 825, 510, 930)}, t["p2_big"],
                           [380, 893], 50, f, fill="#ffffff", border=False))
    els.append({"region": {"op": "union",
                           "shapes": [{"circle": [310, 1000, 62]},
                                      {"circle": [395, 1000, 50]}],
                           "fill": "#ffd84d", "stroke": "#1a1a1a",
                           "stroke_width": 4, "border": True}})
    els.append(text_bubble({"polygon": rect(348, 975, 352, 978)}, t["p2_badge"],
                           [352, 995], 19, f, fill="#ffd84d", border=False,
                           line_gap=24))
    els.append(text_bubble({"polygon": rect(120, 1062, 660, 1130)}, t["p2_bubble"],
                           [390, 1103], 25, f, border_width=3,
                           tail=[[200, 1064], [230, 1025], [262, 1064]]))

    # ---- Panel 3 (転): only two survive ------------------------------------
    els.append(text_bubble({"polygon": rect(40, 1200, 720, 1268)}, t["p3_cap"],
                           [380, 1241], 23, f, fill="#fffbe8", border_width=3))
    els.append(text_bubble({"circle": [250, 1420, 95]}, t["p3_a"], [250, 1408],
                           26, f, fill="#ffe2a8", border_width=4, line_gap=34))
    els.append(text_bubble({"circle": [510, 1420, 92]}, t["p3_b"], [510, 1410],
                           21, f, fill="#cfe6ff", border_width=4, line_gap=30))
    for k in range(6):
        cx = 120 + k * 104
        els.append(text_bubble({"circle": [cx, 1565, 32]}, "×", [cx, 1576], 28, f,
                               fill="#d9d4c8", border_width=2,
                               border_color="#8a8474", text_color="#6a645a"))
    els.append(text_bubble({"polygon": rect(140, 1612, 700, 1670)}, t["p3_bubble"],
                           [420, 1648], 25, f, border_width=3))

    # ---- Panel 4 (結): the honest-disclosure punchline ----------------------
    els.append(text_bubble({"polygon": rect(60, 1730, 700, 1872)}, t["p4_bubble"],
                           [380, 1788], 27, f, border_width=4, line_gap=42))
    els.append(text_bubble({"polygon": rect(60, 1900, 700, 2034)}, t["p4_cap"],
                           [380, 1944], 21, f, fill="#efe7d2", border_width=2,
                           line_gap=33))
    els.append(text_bubble({"polygon": rect(376, 2086, 384, 2090)}, t["p4_foot"],
                           [380, 2120], 21, f, fill="#f5efe2", border=False,
                           text_color="#6a645a"))
    els.append(text_bubble({"polygon": rect(376, 2156, 384, 2160)},
                           "mangamd L0 / FullSense", [380, 2180], 13, f,
                           fill="#f5efe2", border=False, text_color="#8a8474"))

    return {"title": t["title"],
            "canvas": {"w": 760, "h": 2300, "bg": "#f5efe2"},
            "elements": els}


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    SRC_DIR.mkdir(parents=True, exist_ok=True)
    for lang in ("ja", "en", "zh", "ko"):
        panel = build(lang)
        suffix = "" if lang == "ja" else f"_{lang}"
        src = SRC_DIR / f"q25_4koma{suffix}.json"
        out = OUT_DIR / f"q25_4koma{suffix}.svg"
        src.write_text(json.dumps(panel, ensure_ascii=False, indent=1),
                       encoding="utf-8")
        svg = mangamd_poc.render(panel)
        from xml.dom import minidom
        minidom.parseString(svg.encode("utf-8"))  # fail-closed
        out.write_bytes(svg.encode("utf-8"))
        print(f"wrote {out} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
