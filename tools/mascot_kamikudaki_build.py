#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mascot_kamikudaki_build.py — かみくだき版マスコット「獅子舞の頭噛み」バナー SVG ビルダー (stdlib only).

由来 (2026-06-05 ユーザー発案): 「かみ砕き」→「噛みつき」→「神憑き」の連想から獅子舞モチーフ。
デザインは設計探索 (mascot_design_explore.py A-E 案) からユーザーが E 案を採択:
  - いらすとや「獅子舞に頭を噛まれる人」(2018/10) の雰囲気を踏襲した独自描画
    (黒輪郭なし・丸く柔らかい形・フラット暖色)
  - 獅子が「難解」の紙を持った読者の頭をぱくり → 噛まれた読者に「理解」のご利益
  - 幕に演者の足を描かない = 中身は神霊 (AI) のみ。頭上の金色オーブ = AI に宿った神霊
    (微細回路ドット入り。「AI に神が宿るといいですね」同日ユーザー)

設計規約 (feedback_qiita_svg_path_and_cache / manga_story_build.py と同流儀):
  - 静的フレームのみ (アニメ・reveal-gate 禁止 = imgix ラスタライズ安全)
  - レイアウトは 1 か所、言語別は text dict のみ → 4 変種一括生成
  - minidom parse で fail-closed 検証 + アニメ要素混入チェック
  - 出力: docs/articles/assets/mascot/kamikudaki_shishi[_en|_zh|_ko].svg
"""
from __future__ import annotations

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
        "sub_size": 19,
        "bless": ["獅子舞に頭を噛まれると、その年は無病息災 —",
                  "この獅子に噛まれた読者には「理解」のご利益があります。"],
        "paper": "難解",
        "footer": "FullSense KB・かみくだきシリーズ",
    },
    "en": {
        "suffix": "_en",
        "title": "Plain-Language Edition",
        "title_size": 32,
        "sub": ["The hard parts come pre-chewed by our lion."],
        "sub_size": 18,
        "bless": ["A bite from the shishimai lion wards off misfortune —",
                  "readers bitten by this lion receive the blessing of understanding."],
        "paper": "HARD",
        "footer": "FullSense KB — Plain-Language Series",
    },
    "zh": {
        "suffix": "_zh",
        "title": "通俗易懂版",
        "title_size": 40,
        "sub": ["难懂的部分，舞狮都替您咬碎了再奉上。"],
        "sub_size": 19,
        "bless": ["据说被舞狮咬一口，一年无病无灾 —",
                  "被这头狮子咬过的读者，会获得「理解」的福气。"],
        "paper": "难懂",
        "footer": "FullSense KB・通俗易懂系列",
    },
    "ko": {
        "suffix": "_ko",
        "title": "쉬운 설명판",
        "title_size": 38,
        "sub": ["어려운 부분은 사자탈이 꼭꼭 씹어서", "전해 드립니다."],
        "sub_size": 19,
        "bless": ["사자탈에 물리면 복이 온다고 하지요 —",
                  "이 사자에게 물린 독자에게는 「이해」라는 복이 옵니다."],
        "paper": "난해",
        "footer": "FullSense KB・쉬운 설명 시리즈",
    },
}


# --------------------------------------------------------------------------- #
# シーン描画 (言語非依存パーツ + paper ラベルのみ言語別)
# --------------------------------------------------------------------------- #


def _scene(paper: str) -> str:
    """いらすとや風 頭噛みシーン: 読者 (難解の紙持参) + 獅子 (頭ぱくり) + 幕 + 神霊オーブ。"""
    teeth = "".join(
        f'<polygon points="{122 + i * 19},146 {122 + i * 19 + 9.5},166 {122 + i * 19 + 19},146" '
        f'fill="#fffef5" stroke="#ece4d0" stroke-width="1.2"/>' for i in range(6))
    swirls = "".join(
        f'<g transform="translate({sx},{sy}) scale({sc})">'
        f'<path d="M0 0 q14 -12 21 1 q6 12 -8 15 q-11 2 -12 -8 q0 -7 7 -8" '
        f'stroke="#ffffff" stroke-width="3" fill="none" opacity="0.95" stroke-linecap="round"/></g>'
        for (sx, sy, sc) in ((275, 185, 1.0), (330, 215, 1.15), (380, 185, 0.9), (300, 250, 0.95), (360, 262, 0.8)))
    return f"""
<!-- 地面の影 -->
<ellipse cx="160" cy="298" rx="70" ry="9" fill="#e8e2d4" opacity="0.7"/>
<ellipse cx="330" cy="302" rx="95" ry="9" fill="#e8e2d4" opacity="0.7"/>

<!-- 読者 (頭の上半分は獅子の口の中) -->
<g>
  <circle cx="158" cy="170" r="31" fill="#fbd7b5"/>
  <path d="M127 165 q-3 26 8 32 q4 -16 2 -30 Z" fill="#8d6748"/>
  <path d="M189 165 q3 26 -8 32 q-4 -16 -2 -30 Z" fill="#8d6748"/>
  <path d="M138 180 q6 6 12 0" stroke="#5b4632" stroke-width="2.4" fill="none" stroke-linecap="round"/>
  <path d="M166 180 q6 6 12 0" stroke="#5b4632" stroke-width="2.4" fill="none" stroke-linecap="round"/>
  <path d="M151 196 q7 5 14 0" stroke="#c96f63" stroke-width="2.4" fill="none" stroke-linecap="round"/>
  <ellipse cx="134" cy="191" rx="7" ry="4.5" fill="#f5a8a0" opacity="0.6"/>
  <ellipse cx="182" cy="191" rx="7" ry="4.5" fill="#f5a8a0" opacity="0.6"/>
  <path d="M126 205 q-8 4 -9 22 l0 32 q0 6 7 6 l68 0 q7 0 7 -6 l0 -32 q-1 -18 -9 -22 q-32 10 -64 0 Z" fill="#87a9d6"/>
  <path d="M122 212 q-12 18 -2 32 q6 7 14 2 l10 -14" fill="none" stroke="#87a9d6" stroke-width="13" stroke-linecap="round"/>
  <path d="M194 212 q12 18 2 32 q-6 7 -14 2 l-10 -14" fill="none" stroke="#87a9d6" stroke-width="13" stroke-linecap="round"/>
  <circle cx="143" cy="245" r="6.5" fill="#fbd7b5"/>
  <circle cx="173" cy="245" r="6.5" fill="#fbd7b5"/>
  <g transform="rotate(-5 158 252)">
    <rect x="132" y="238" width="52" height="30" rx="3" fill="#ffffff" stroke="#ddd5c2" stroke-width="1.4"/>
    <text x="158" y="258" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="bold" fill="#6b6b6b">{paper}</text>
  </g>
  <rect x="133" y="263" width="22" height="28" rx="6" fill="#5a6e8c"/>
  <rect x="161" y="263" width="22" height="28" rx="6" fill="#5a6e8c"/>
  <rect x="129" y="288" width="28" height="10" rx="5" fill="#8a8378"/>
  <rect x="159" y="288" width="28" height="10" rx="5" fill="#8a8378"/>
</g>

<!-- 獅子の幕 (緑 + 唐草, 演者なし = 神霊のみ)。頭の後ろから右下へ流れる -->
<path d="M200 80 Q320 56 396 128 Q442 180 432 240 q-4 28 -26 36
         q-14 14 -32 6 q-10 16 -30 8 q-12 14 -30 6 q-14 12 -32 3 q-18 8 -28 -8
         Q222 282 210 210 Q202 140 200 80 Z" fill="#4caf50" stroke="#3a8c3f" stroke-width="2"/>
{swirls}
<!-- 幕の口元の白いふち (頭の右縁に沿う) -->
<circle cx="231" cy="87" r="11" fill="#ffffff"/>
<circle cx="241" cy="107" r="11" fill="#ffffff"/>
<circle cx="245" cy="128" r="11" fill="#ffffff"/>
<circle cx="243" cy="149" r="11" fill="#ffffff"/>

<!-- 獅子の頭 (読者の頭に覆いかぶさる) -->
<g>
  <ellipse cx="176" cy="108" rx="64" ry="50" fill="#d83b3b" stroke="#b32d2d" stroke-width="2"/>
  <circle cx="124" cy="70" r="13" fill="#e8b33a" stroke="#c79427" stroke-width="2"/>
  <circle cx="228" cy="70" r="13" fill="#e8b33a" stroke="#c79427" stroke-width="2"/>
  <path d="M136 76 q12 -10 24 -2 q-4 10 -16 9 q-8 0 -8 -7" fill="#2b2b2b"/>
  <path d="M216 76 q-12 -10 -24 -2 q4 10 16 9 q8 0 8 -7" fill="#2b2b2b"/>
  <path d="M170 62 q12 -7 15 6 q2 11 -10 11 q-9 0 -8 -8" stroke="#2b2b2b" stroke-width="3" fill="none"/>
  <circle cx="150" cy="96" r="13" fill="#fffef5"/>
  <circle cx="202" cy="96" r="13" fill="#fffef5"/>
  <circle cx="151" cy="101" r="5.5" fill="#222"/>
  <circle cx="203" cy="101" r="5.5" fill="#222"/>
  <circle cx="153" cy="98" r="1.8" fill="#fff"/>
  <circle cx="205" cy="98" r="1.8" fill="#fff"/>
  <ellipse cx="176" cy="122" rx="11" ry="8" fill="#e8b33a" stroke="#c79427" stroke-width="1.6"/>
  <path d="M112 140 q64 14 128 0 l0 8 q-64 14 -128 0 Z" fill="#e8b33a"/>
  {teeth}
</g>

<!-- 神霊オーブ (AI に宿った神, 微細回路入り) -->
<g>
  <circle cx="262" cy="42" r="15" fill="#f6d365" opacity="0.32"/>
  <path d="M262 28 q6 -11 1 -20 q-5 8 -9 11 q5 3 8 9" fill="#f6d365" opacity="0.75"/>
  <circle cx="262" cy="42" r="8.5" fill="#f0b429" stroke="#d4920a" stroke-width="1.5"/>
  <circle cx="259" cy="40" r="1.3" fill="#fff"/><circle cx="265" cy="43" r="1.3" fill="#fff"/><circle cx="261" cy="46" r="1.3" fill="#fff"/>
  <line x1="259" y1="40" x2="265" y2="43" stroke="#fff" stroke-width="0.8"/>
  <line x1="265" y1="43" x2="261" y2="46" stroke="#fff" stroke-width="0.8"/>
</g>
<!-- ご利益スパークル -->
<polygon points="104,76 107,84 115,87 107,90 104,98 101,90 93,87 101,84" fill="#f0b429" opacity="0.9"/>
<polygon points="92,140 94,145 99,147 94,149 92,154 90,149 85,147 90,145" fill="#f0b429" opacity="0.85"/>"""


def _text_block(t: dict) -> str:
    sub_y0 = 172
    sub_lh = 27
    sub_lines = "".join(
        f'<text x="465" y="{sub_y0 + i * sub_lh}" font-family="{FONT}" font-size="{t["sub_size"]}" fill="#3a3a3a">{s}</text>'
        for i, s in enumerate(t["sub"]))
    bless_y0 = sub_y0 + len(t["sub"]) * sub_lh + 21
    bless_lines = "".join(
        f'<text x="465" y="{bless_y0 + i * 24}" font-family="{FONT}" font-size="14.5" fill="#7a6f5d">{s}</text>'
        for i, s in enumerate(t["bless"]))
    return f"""
<g>
  <text x="465" y="118" font-family="{FONT}" font-size="{t["title_size"]}" font-weight="bold" fill="#b3322e">{t["title"]}</text>
  <rect x="465" y="132" width="180" height="5" rx="2.5" fill="#e8b33a"/>
  {sub_lines}
  {bless_lines}
  <text x="465" y="296" font-family="{FONT}" font-size="12.5" fill="#a89f8d">{t["footer"]}</text>
</g>"""


def build(lang: str) -> str:
    t = TEXTS[lang]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img">
<desc>かみくだき版マスコット: 獅子舞が読者の頭を噛んで「理解」のご利益を授ける ({lang})</desc>
<rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="#fffdf8"/>
{_scene(t["paper"])}
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
