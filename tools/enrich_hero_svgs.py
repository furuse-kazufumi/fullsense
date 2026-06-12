#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""hero アニメ SVG に「強化レイヤ」を冪等に注入する (FullSense house style)。

設計方針 (家訓 feedback_qiita_svg_path_and_cache / feedback_animated_svg_static_fallback 準拠):
- **言語中立**: テキストを一切足さない → ja/en/zh/ko 変種に同一注入でき翻訳ドリフトが起きない。
- **静止完成形**: 全要素は authored 値で可視。reveal-gate (width=0/opacity=0 始点) を作らない。
  → imgix がラスタライズした静止1枚 (Qiita 表示) でも意味を持つ。
- **imgix 安全**: animateMotion / <mpath> を使わない (imgix が解決できず空画像になる)。
  動きは animateTransform translate と animate (opacity/x) のみ = 静止安全 + imgix 安全。
- **冪等**: 既に強化レイヤ (id=llt-enrich) があれば一度剥がしてから入れ直す。
- **viewBox 相対**: hero は 1200x360 と 800x240 の 2 種。viewBox を読んで座標を算出。

使い方: python tools/enrich_hero_svgs.py <svg ...>   (対象ファイルを列挙)
"""
from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

MARKER = "llt-enrich"
_VB = re.compile(r'viewBox="\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*"')
# 冪等化: 既存の強化レイヤ <g id="llt-enrich" ...> ... </g> を丸ごと除去する
_EXISTING = re.compile(r'\n?\s*<g id="llt-enrich".*?</g>\s*(?=</svg>)', re.DOTALL)

ACCENT = "#38bdf8"  # cyan (FullSense アクセント。既存パレットと調和)


def _corner_ticks(w: float, h: float) -> str:
    """四隅の L 字ティック (静止可視 + ゆっくり呼吸する opacity)。奥行きを足す。"""
    m, ln = 12.0, 20.0  # margin, tick length
    specs = [  # (x, y, sx, sy)  sx/sy = 内側方向
        (m, m, 1, 1), (w - m, m, -1, 1), (m, h - m, 1, -1), (w - m, h - m, -1, -1),
    ]
    out = []
    for i, (x, y, sx, sy) in enumerate(specs):
        d = f"M {x + sx * ln:.1f} {y:.1f} L {x:.1f} {y:.1f} L {x:.1f} {y + sy * ln:.1f}"
        out.append(
            f'<path d="{d}" stroke="{ACCENT}" stroke-width="1.4" fill="none" '
            f'stroke-linecap="round" opacity="0.55">'
            f'<animate attributeName="opacity" values="0.55;0.9;0.55" dur="3.6s" '
            f'begin="{i * 0.4:.1f}s" repeatCount="indefinite"/></path>')
    return "".join(out)


def _particles(w: float, h: float) -> str:
    """漂う微粒子 (静止可視の authored 位置 + translate ドリフト)。imgix 安全。"""
    # viewBox 相対の散布位置と微小ドリフト (deterministic、乱数不使用)
    pts = [(0.12, 0.30), (0.30, 0.68), (0.50, 0.22), (0.68, 0.74), (0.82, 0.40), (0.92, 0.60)]
    out = []
    for i, (fx, fy) in enumerate(pts):
        cx, cy = fx * w, fy * h
        dx = (8 if i % 2 == 0 else -8)
        dy = (-6 if i % 3 == 0 else 6)
        dur = 8 + (i % 4) * 1.5
        out.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{2 + i % 2}" fill="{ACCENT}" opacity="0.38">'
            f'<animateTransform attributeName="transform" type="translate" '
            f'values="0 0; {dx} {dy}; 0 0" dur="{dur:.1f}s" begin="{i * 0.7:.1f}s" '
            f'repeatCount="indefinite" additive="sum"/>'
            f'<animate attributeName="opacity" values="0.38;0.6;0.38" dur="{dur:.1f}s" '
            f'begin="{i * 0.7:.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)


def _baseline_shimmer(w: float, h: float) -> str:
    """最下部の細いアクセント線 (静止可視の実線 + 左→右へ流れるハイライト)。"""
    y = h - 3.0
    seg = w * 0.18
    return (
        f'<rect x="0" y="{y:.1f}" width="{w:.1f}" height="1.5" fill="{ACCENT}" opacity="0.18"/>'
        f'<rect x="0" y="{y:.1f}" width="{seg:.1f}" height="1.5" fill="{ACCENT}" opacity="0.75">'
        f'<animate attributeName="x" values="{-seg:.1f};{w:.1f}" dur="5s" '
        f'repeatCount="indefinite"/></rect>')


def enrich(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    m = _VB.search(text)
    if not m:
        print(f"  SKIP (viewBox なし): {path.name}")
        return False
    _, _, w, h = (float(x) for x in m.groups())
    text = _EXISTING.sub("", text)  # 冪等: 既存強化レイヤを除去
    block = (
        f'\n  <g id="{MARKER}" font-family="inherit" aria-hidden="true">'
        f"<!-- llt-enrich: 言語中立・静止完成形・imgix安全な強化レイヤ -->"
        f"{_corner_ticks(w, h)}{_particles(w, h)}{_baseline_shimmer(w, h)}"
        f"</g>\n")
    if "</svg>" not in text:
        print(f"  SKIP (</svg> なし): {path.name}")
        return False
    text = text.replace("</svg>", block + "</svg>", 1)
    try:  # XML well-formed 検証 (壊れた SVG を書き出さない)
        ET.fromstring(text)
    except ET.ParseError as e:
        print(f"  FAIL (XML 不正、書き込まず): {path.name}: {e}")
        return False
    path.write_text(text, encoding="utf-8")
    return True


def main(argv: list[str]) -> int:
    files = [Path(a) for a in argv]
    if not files:
        print("usage: enrich_hero_svgs.py <svg ...>", file=sys.stderr)
        return 2
    ok = 0
    for p in files:
        if not p.is_file():
            print(f"  SKIP (なし): {p}")
            continue
        if enrich(p):
            ok += 1
            print(f"  OK: {p}")
    print(f"\n強化レイヤ注入: {ok}/{len(files)} 成功")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
