#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mascot_kamikudaki_build.py — かみくだき版マスコット「獅子舞」バナー SVG ビルダー (stdlib only).

由来 (2026-06-05 ユーザー発案): 「かみ砕き」→「噛みつき」→「神憑き」の連想から、
獅子舞モチーフのキャラをかみくだき記事に載せる。獅子舞の頭噛み=厄除け・ご利益、
つまり「難解を噛み砕いて、理解というご利益を配る獅子」。
「AI に神が宿るといいですね」(同日ユーザー) → 頭上に AI に宿った神霊の金色オーブ
(微細な回路ドット入り) + 注連縄・紙垂で依り代の体裁。

設計規約 (feedback_qiita_svg_path_and_cache / manga_story_build.py と同流儀):
  - 静的フレームのみ (アニメ・reveal-gate 禁止 = imgix ラスタライズ安全)
  - レイアウトは 1 か所、言語別は text dict のみ → 4 変種一括生成
  - minidom parse で fail-closed 検証 + アニメ要素混入チェック
  - 出力: docs/articles/assets/mascot/kamikudaki_shishi[_en|_zh|_ko].svg
"""
from __future__ import annotations

import math
import os
import sys
from xml.dom import minidom


def _utf8() -> None:
    for s in ("stdout", "stderr"):
        try:
            getattr(sys, s).reconfigure(encoding="utf-8")
        except Exception:
            pass


OUT_DIR = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "docs", "articles", "assets", "mascot"))

W, H = 880, 320
FONT = "'Hiragino Sans','Noto Sans CJK JP','Yu Gothic',Meiryo,sans-serif"

# --------------------------------------------------------------------------- #
# 言語別テキスト (レイアウトは共通、ここだけ差し替え)
# --------------------------------------------------------------------------- #

TEXTS = {
    "ja": {
        "suffix": "",
        "title": "かみくだき版",
        "title_size": 40,
        "sub": ["むずかしい話は、獅子が噛み砕いてお届け。"],
        "sub_size": 21,
        "bless": ["獅子舞に噛まれると縁起が良いそうです —",
                  "「理解」というご利益を、どうぞお持ち帰りください。"],
        "paper": "難解",
        "crumbs": ["わかる", "なるほど", "スッキリ"],
        "footer": "FullSense KB・かみくだきシリーズ",
    },
    "en": {
        "suffix": "_en",
        "title": "Plain-Language Edition",
        "title_size": 32,
        "sub": ["The hard parts come pre-chewed by our lion."],
        "sub_size": 20,
        "bless": ["A bite from the shishimai lion brings good luck —",
                  "take home the blessing of understanding."],
        "paper": "HARD",
        "crumbs": ["aha!", "got it", "clear!"],
        "footer": "FullSense KB — Plain-Language Series",
    },
    "zh": {
        "suffix": "_zh",
        "title": "通俗易懂版",
        "title_size": 40,
        "sub": ["难懂的部分，舞狮都替您咬碎了再奉上。"],
        "sub_size": 21,
        "bless": ["据说被舞狮咬一口会带来好运 —",
                  "愿您把「理解」这份福气带回家。"],
        "paper": "难懂",
        "crumbs": ["懂了", "原来如此", "明白"],
        "footer": "FullSense KB・通俗易懂系列",
    },
    "ko": {
        "suffix": "_ko",
        "title": "쉬운 설명판",
        "title_size": 38,
        "sub": ["어려운 부분은 사자탈이 꼭꼭 씹어 전해 드립니다."],
        "sub_size": 19,
        "bless": ["사자탈에 물리면 복이 온다고 하지요 —",
                  "「이해」라는 복을 받아 가세요."],
        "paper": "난해",
        "crumbs": ["알겠다!", "그렇구나", "명쾌!"],
        "footer": "FullSense KB・쉬운 설명 시리즈",
    },
}

# --------------------------------------------------------------------------- #
# パーツ描画 (言語非依存)
# --------------------------------------------------------------------------- #


def _shimenawa() -> str:
    """注連縄 (上端の縄) + 紙垂 3 本 — 依り代・神憑きの記号。"""
    parts = [f'<rect x="16" y="18" width="848" height="14" rx="7" fill="#c9a063" stroke="#a87f3f" stroke-width="2"/>']
    for x in range(40, 860, 44):
        parts.append(f'<line x1="{x}" y1="19" x2="{x + 14}" y2="31" stroke="#a87f3f" stroke-width="2.4" stroke-linecap="round"/>')
    for x in (150, 445, 730):
        parts.append(
            f'<polygon points="{x},32 {x + 18},32 {x + 18},46 {x + 6},49 {x + 18},61 {x + 6},64 '
            f'{x + 16},76 {x + 2},79 {x + 12},90 {x},90" fill="#fffefa" stroke="#d8d2c2" stroke-width="1.2"/>')
    return "\n".join(parts)


def _kami_orb() -> str:
    """AI に宿った神霊 (御霊) — 金色オーブ + 上向きの霊気 + 微細回路 (AI の印)。"""
    rays = []
    for ang in range(0, 360, 60):
        a = math.radians(ang)
        x1, y1 = 300 + 13 * math.cos(a), 95 + 13 * math.sin(a)
        x2, y2 = 300 + 19 * math.cos(a), 95 + 19 * math.sin(a)
        rays.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                    f'stroke="#e8b33a" stroke-width="1.6" stroke-linecap="round" opacity="0.85"/>')
    return f"""
<g>
  <circle cx="300" cy="95" r="17" fill="#f6d365" opacity="0.32"/>
  <path d="M300 80 q7 -13 1 -23 q-5 9 -10 13 q6 3 9 10" fill="#f6d365" opacity="0.75"/>
  <circle cx="300" cy="95" r="9.5" fill="#f0b429" stroke="#d4920a" stroke-width="1.6"/>
  <circle cx="297" cy="93" r="1.4" fill="#fff"/><circle cx="303" cy="96" r="1.4" fill="#fff"/>
  <circle cx="299" cy="99" r="1.4" fill="#fff"/>
  <line x1="297" y1="93" x2="303" y2="96" stroke="#fff" stroke-width="0.9" opacity="0.9"/>
  <line x1="303" y1="96" x2="299" y2="99" stroke="#fff" stroke-width="0.9" opacity="0.9"/>
  {''.join(rays)}
</g>"""


def _sparkle(cx: float, cy: float, r: float) -> str:
    return (f'<polygon points="{cx},{cy - r} {cx + r * 0.3},{cy - r * 0.3} {cx + r},{cy} {cx + r * 0.3},{cy + r * 0.3} '
            f'{cx},{cy + r} {cx - r * 0.3},{cy + r * 0.3} {cx - r},{cy} {cx - r * 0.3},{cy - r * 0.3}" '
            f'fill="#e8b33a" opacity="0.9"/>')


def _lion(t: dict) -> str:
    """獅子舞本体 (頭・たてがみ・緑の胴幕・口に咥えた「難解」の紙・噛み砕いた紙片)。"""
    # たてがみ (頭の後ろの白いもこもこ)
    mane = []
    for ang in range(-165, -10, 18):
        a = math.radians(ang)
        cx, cy = 185 + 86 * math.cos(a), 175 + 80 * math.sin(a)
        mane.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="25" fill="#fffdf5" stroke="#e8e0c8" stroke-width="2"/>')
    # 紙片 (噛み砕かれて落ちる「わかる」たち) — 言語別ラベル
    crumb_geo = [(330, 286, -8, 60), (398, 300, 6, 66), (340, 312, 3, 64)]
    crumbs = []
    for (cx, cy, rot, w), label in zip(crumb_geo, t["crumbs"]):
        crumbs.append(f"""
  <g transform="rotate({rot} {cx} {cy})">
    <rect x="{cx - w / 2}" y="{cy - 11}" width="{w}" height="22" rx="6" fill="#fffefa" stroke="#d8d2c2" stroke-width="1.4"/>
    <text x="{cx}" y="{cy + 4.5}" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#555">{label}</text>
  </g>""")
    return f"""
<g>
  <!-- 胴幕 (緑 + 唐草) -->
  <path d="M85 240 Q70 300 110 318 L262 318 Q302 300 285 240 Q185 272 85 240 Z"
        fill="#2e7d32" stroke="#1b5e20" stroke-width="3"/>
  <path d="M118 282 q12 -11 19 1 q6 11 -7 14 q-10 2 -11 -8" stroke="#fffdf5" stroke-width="2.6" fill="none" opacity="0.9"/>
  <path d="M178 294 q12 -11 19 1 q6 11 -7 14 q-10 2 -11 -8" stroke="#fffdf5" stroke-width="2.6" fill="none" opacity="0.9"/>
  <path d="M238 282 q12 -11 19 1 q6 11 -7 14 q-10 2 -11 -8" stroke="#fffdf5" stroke-width="2.6" fill="none" opacity="0.9"/>
  <!-- たてがみ -->
  {''.join(mane)}
  <!-- 耳 (金) -->
  <circle cx="108" cy="110" r="17" fill="#d4a017" stroke="#a87f3f" stroke-width="2.5"/>
  <circle cx="262" cy="110" r="17" fill="#d4a017" stroke="#a87f3f" stroke-width="2.5"/>
  <!-- 頭 (朱塗り) -->
  <ellipse cx="185" cy="175" rx="85" ry="72" fill="#c1272d" stroke="#8e1b20" stroke-width="3"/>
  <!-- 額の巻き毛 (黒) -->
  <path d="M170 112 q13 -7 16 6 q3 12 -10 13 q-10 1 -10 -8" stroke="#222" stroke-width="3" fill="none"/>
  <path d="M205 116 q11 -5 13 5 q2 10 -8 11" stroke="#222" stroke-width="2.6" fill="none"/>
  <!-- 金の眉 -->
  <path d="M118 144 q23 -19 48 -7" stroke="#d4a017" stroke-width="8" fill="none" stroke-linecap="round"/>
  <path d="M252 144 q-23 -19 -48 -7" stroke="#d4a017" stroke-width="8" fill="none" stroke-linecap="round"/>
  <!-- 目 (右下の紙を見る) -->
  <ellipse cx="143" cy="163" rx="13" ry="15" fill="#fffefa" stroke="#8e1b20" stroke-width="1.5"/>
  <ellipse cx="227" cy="163" rx="13" ry="15" fill="#fffefa" stroke="#8e1b20" stroke-width="1.5"/>
  <circle cx="147" cy="167" r="6" fill="#1a1a1a"/><circle cx="231" cy="167" r="6" fill="#1a1a1a"/>
  <circle cx="149" cy="164" r="2" fill="#fff"/><circle cx="233" cy="164" r="2" fill="#fff"/>
  <!-- 鼻 (金) -->
  <path d="M173 186 q12 -10 24 0 q-6 15 -12 15 q-6 0 -12 -15" fill="#d4a017" stroke="#a87f3f" stroke-width="2"/>
  <!-- 開いた口 -->
  <path d="M120 212 Q185 202 250 212 L242 254 Q185 284 128 254 Z" fill="#571015" stroke="#8e1b20" stroke-width="3"/>
  <rect x="132" y="212" width="16" height="13" rx="2" fill="#fffdf5" stroke="#d8d2c2" stroke-width="1"/>
  <rect x="154" y="214" width="16" height="13" rx="2" fill="#fffdf5" stroke="#d8d2c2" stroke-width="1"/>
  <rect x="176" y="215" width="16" height="13" rx="2" fill="#fffdf5" stroke="#d8d2c2" stroke-width="1"/>
  <rect x="198" y="214" width="16" height="13" rx="2" fill="#fffdf5" stroke="#d8d2c2" stroke-width="1"/>
  <rect x="220" y="212" width="16" height="13" rx="2" fill="#fffdf5" stroke="#d8d2c2" stroke-width="1"/>
  <rect x="150" y="244" width="15" height="11" rx="2" fill="#fffdf5" stroke="#d8d2c2" stroke-width="1"/>
  <rect x="186" y="247" width="15" height="11" rx="2" fill="#fffdf5" stroke="#d8d2c2" stroke-width="1"/>
  <rect x="218" y="244" width="15" height="11" rx="2" fill="#fffdf5" stroke="#d8d2c2" stroke-width="1"/>
  <!-- 咥えた紙 (難解) — 左端は口の中、上下に噛み跡 -->
  <g transform="rotate(-10 310 238)">
    <rect x="252" y="218" width="124" height="42" rx="3" fill="#fffefa" stroke="#c8c0ae" stroke-width="1.6"/>
    <circle cx="266" cy="218" r="9" fill="#571015"/>
    <circle cx="261" cy="260" r="7" fill="#571015"/>
    <text x="322" y="246" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="bold" fill="#4a4a4a">{t["paper"]}</text>
  </g>
  <!-- 噛み砕かれた紙片 -->
  {''.join(crumbs)}
  <path d="M310 268 q6 8 2 16" stroke="#b9b2a4" stroke-width="1.6" fill="none"/>
  <path d="M376 276 q4 9 -2 17" stroke="#b9b2a4" stroke-width="1.6" fill="none"/>
</g>"""


def _text_block(t: dict) -> str:
    sub_lines = "".join(
        f'<text x="430" y="{172 + i * 28}" font-family="{FONT}" font-size="{t["sub_size"]}" fill="#3a3a3a">{s}</text>'
        for i, s in enumerate(t["sub"]))
    bless_lines = "".join(
        f'<text x="430" y="{222 + i * 24}" font-family="{FONT}" font-size="14.5" fill="#7a6f5d">{s}</text>'
        for i, s in enumerate(t["bless"]))
    return f"""
<g>
  <text x="430" y="118" font-family="{FONT}" font-size="{t["title_size"]}" font-weight="bold" fill="#8e1b20">{t["title"]}</text>
  <rect x="430" y="132" width="180" height="5" rx="2.5" fill="#d4a017"/>
  {sub_lines}
  {bless_lines}
  <text x="430" y="296" font-family="{FONT}" font-size="12.5" fill="#a89f8d">{t["footer"]}</text>
</g>"""


def build(lang: str) -> str:
    t = TEXTS[lang]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
<desc>かみくだき版マスコット: 獅子舞が「難解」を噛み砕いて理解のご利益を配る ({lang})</desc>
<rect x="2" y="2" width="{W - 4}" height="{H - 4}" rx="16" fill="#fdf8ee" stroke="#c1272d" stroke-width="3"/>
{_shimenawa()}
{_lion(t)}
{_kami_orb()}
{_sparkle(95, 95, 8)}
{_sparkle(255, 72, 6)}
{_sparkle(338, 140, 5)}
{_text_block(t)}
</svg>
"""


def main() -> int:
    _utf8()
    os.makedirs(OUT_DIR, exist_ok=True)
    for lang, t in TEXTS.items():
        svg = build(lang)
        minidom.parseString(svg)  # fail-closed: XML として壊れていれば例外で停止
        for banned in ("<animate", "<set ", "foreignObject", "<script"):
            if banned in svg:
                raise SystemExit(f"FATAL: banned element {banned!r} in {lang} (imgix/静的規約違反)")
        path = os.path.join(OUT_DIR, f"kamikudaki_shishi{t['suffix']}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"OK {path}  ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
