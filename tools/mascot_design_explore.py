#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mascot_design_explore.py — かみくだき獅子舞マスコットのデザイン探索 (B/C/D 案, JA only, 使い捨て).

A 案 (バナー型) は mascot_kamikudaki_build.py が正。本スクリプトは方向性比較用のスケッチ:
  B = キャラ単体型 (480x480, ゆるかわ寄り, README 等へ使い回せるマスコット)
  C = 漫画コマ風 (880x320, 既存 mangamd 4 コマとトーン統一: 白黒 + 朱のみ)
  D = 伝統祝祭型 (880x320, 紅白幕・雲文様・落款 = 神事/神憑き全振り)
出力: D:/tmp/mascot_explore/mascot_B.svg, mascot_C.svg, mascot_D.svg
方向性確定後は採用案を mascot_kamikudaki_build.py に統合し、本スクリプトの役目は終了。
"""
from __future__ import annotations

import math
import os
import sys
from xml.dom import minidom

for s in ("stdout", "stderr"):
    try:
        getattr(sys, s).reconfigure(encoding="utf-8")
    except Exception:
        pass

OUT = "D:/tmp/mascot_explore"
FONT = "'Hiragino Sans','Noto Sans CJK JP','Yu Gothic',Meiryo,sans-serif"
MINCHO = "'Yu Mincho','Hiragino Mincho ProN',serif"


def mane(cx: float, cy: float, rx: float, ry: float, r: float, a0: int, a1: int, step: int,
         fill: str = "#fffdf5", stroke: str = "#e8e0c8") -> str:
    out = []
    for ang in range(a0, a1, step):
        a = math.radians(ang)
        out.append(f'<circle cx="{cx + rx * math.cos(a):.1f}" cy="{cy + ry * math.sin(a):.1f}" r="{r}" '
                   f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>')
    return "".join(out)


# --------------------------------------------------------------------------- #
# B 案: キャラ単体型 (480x480) — ゆるかわ。丸目大きめ、二頭身、ご利益オーブ
# --------------------------------------------------------------------------- #

def build_b() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 480 480" width="480" height="480" role="img">
<desc>かみくだき獅子 B案: キャラ単体型 (ゆるかわ)</desc>
<rect x="2" y="2" width="476" height="476" rx="20" fill="#fdf8ee" stroke="#c1272d" stroke-width="3"/>
<!-- 注連縄 + 紙垂 -->
<rect x="14" y="16" width="452" height="12" rx="6" fill="#c9a063" stroke="#a87f3f" stroke-width="1.8"/>
<polygon points="120,28 136,28 136,40 126,43 136,53 126,56 134,66 120,66" fill="#fffefa" stroke="#d8d2c2" stroke-width="1.2"/>
<polygon points="340,28 356,28 356,40 346,43 356,53 346,56 354,66 340,66" fill="#fffefa" stroke="#d8d2c2" stroke-width="1.2"/>
<!-- 神霊オーブ -->
<circle cx="350" cy="105" r="20" fill="#f6d365" opacity="0.32"/>
<path d="M350 88 q8 -15 1 -26 q-6 10 -12 15 q8 3 11 11" fill="#f6d365" opacity="0.75"/>
<circle cx="350" cy="105" r="11" fill="#f0b429" stroke="#d4920a" stroke-width="1.8"/>
<circle cx="346" cy="102" r="1.6" fill="#fff"/><circle cx="354" cy="106" r="1.6" fill="#fff"/><circle cx="349" cy="109" r="1.6" fill="#fff"/>
<line x1="346" y1="102" x2="354" y2="106" stroke="#fff" stroke-width="1"/>
<line x1="354" y1="106" x2="349" y2="109" stroke="#fff" stroke-width="1"/>
<!-- 胴幕 (小さめ二頭身) -->
<path d="M130 330 Q110 420 160 448 L320 448 Q370 420 350 330 Q240 365 130 330 Z" fill="#2e7d32" stroke="#1b5e20" stroke-width="3.5"/>
<path d="M175 390 q15 -14 24 1 q8 14 -9 18 q-13 3 -14 -10" stroke="#fffdf5" stroke-width="3" fill="none" opacity="0.9"/>
<path d="M260 400 q15 -14 24 1 q8 14 -9 18 q-13 3 -14 -10" stroke="#fffdf5" stroke-width="3" fill="none" opacity="0.9"/>
<!-- たてがみ -->
{mane(240, 230, 118, 112, 34, -170, -5, 17)}
<!-- 耳 -->
<circle cx="135" cy="135" r="22" fill="#d4a017" stroke="#a87f3f" stroke-width="3"/>
<circle cx="345" cy="135" r="22" fill="#d4a017" stroke="#a87f3f" stroke-width="3"/>
<!-- 頭 (大きめ = 二頭身) -->
<ellipse cx="240" cy="225" rx="118" ry="105" fill="#c1272d" stroke="#8e1b20" stroke-width="4"/>
<!-- 額の巻き毛 -->
<path d="M218 140 q18 -10 22 8 q4 16 -14 18 q-14 2 -13 -11" stroke="#222" stroke-width="4" fill="none"/>
<path d="M268 146 q15 -7 18 7 q3 13 -11 15" stroke="#222" stroke-width="3.5" fill="none"/>
<!-- 金眉 (やわらか) -->
<path d="M150 185 q30 -22 62 -8" stroke="#d4a017" stroke-width="10" fill="none" stroke-linecap="round"/>
<path d="M330 185 q-30 -22 -62 -8" stroke="#d4a017" stroke-width="10" fill="none" stroke-linecap="round"/>
<!-- 丸目 (大きめ・ゆるかわ) -->
<circle cx="185" cy="215" r="24" fill="#fffefa" stroke="#8e1b20" stroke-width="2"/>
<circle cx="295" cy="215" r="24" fill="#fffefa" stroke="#8e1b20" stroke-width="2"/>
<circle cx="190" cy="220" r="11" fill="#1a1a1a"/><circle cx="300" cy="220" r="11" fill="#1a1a1a"/>
<circle cx="194" cy="215" r="4" fill="#fff"/><circle cx="304" cy="215" r="4" fill="#fff"/>
<!-- ほっぺ -->
<ellipse cx="155" cy="255" rx="14" ry="9" fill="#e8847d" opacity="0.55"/>
<ellipse cx="325" cy="255" rx="14" ry="9" fill="#e8847d" opacity="0.55"/>
<!-- 鼻 -->
<path d="M224 252 q16 -13 32 0 q-8 19 -16 19 q-8 0 -16 -19" fill="#d4a017" stroke="#a87f3f" stroke-width="2.5"/>
<!-- にっこり開いた口 + 紙 -->
<path d="M165 290 Q240 280 315 290 L305 330 Q240 358 175 330 Z" fill="#571015" stroke="#8e1b20" stroke-width="3.5"/>
<rect x="180" y="290" width="18" height="14" rx="2" fill="#fffdf5"/>
<rect x="206" y="293" width="18" height="14" rx="2" fill="#fffdf5"/>
<rect x="232" y="294" width="18" height="14" rx="2" fill="#fffdf5"/>
<rect x="258" y="293" width="18" height="14" rx="2" fill="#fffdf5"/>
<rect x="284" y="290" width="18" height="14" rx="2" fill="#fffdf5"/>
<g transform="rotate(-12 330 320)">
  <rect x="290" y="302" width="110" height="38" rx="3" fill="#fffefa" stroke="#c8c0ae" stroke-width="1.6"/>
  <circle cx="300" cy="302" r="8" fill="#571015"/>
  <text x="350" y="328" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="bold" fill="#4a4a4a">難解</text>
</g>
<!-- バッジ -->
<rect x="150" y="450" width="180" height="0" fill="none"/>
<text x="240" y="471" text-anchor="middle" font-family="{FONT}" font-size="17" font-weight="bold" fill="#8e1b20">かみくだき版</text>
</svg>
"""


# --------------------------------------------------------------------------- #
# C 案: 漫画コマ風 (880x320) — mangamd 4 コマとトーン統一 (白黒 + 朱のみ)
# --------------------------------------------------------------------------- #

def build_c() -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 320" width="880" height="320" role="img">
<desc>かみくだき獅子 C案: 漫画コマ風 (白黒+朱)</desc>
<rect x="0" y="0" width="880" height="320" fill="#ffffff"/>
<rect x="6" y="6" width="868" height="308" fill="none" stroke="#111" stroke-width="4"/>
<!-- 集中線 (左上から獅子へ) -->
<g stroke="#222" stroke-width="1.6" opacity="0.6">
  <line x1="30" y1="30" x2="120" y2="105"/><line x1="90" y1="22" x2="150" y2="95"/>
  <line x1="160" y1="18" x2="185" y2="88"/><line x1="240" y1="20" x2="225" y2="85"/>
  <line x1="320" y1="30" x2="262" y2="98"/>
</g>
<!-- 獅子 (白黒線画 + 頭のみ朱) -->
<g>
  {mane(195, 185, 92, 86, 26, -168, -8, 18, fill="#ffffff", stroke="#111")}
  <circle cx="118" cy="118" r="17" fill="#fff" stroke="#111" stroke-width="3"/>
  <circle cx="272" cy="118" r="17" fill="#fff" stroke="#111" stroke-width="3"/>
  <ellipse cx="195" cy="185" rx="88" ry="74" fill="#c1272d" stroke="#111" stroke-width="3.5"/>
  <path d="M178 120 q14 -8 17 7 q3 13 -11 14 q-11 1 -10 -9" stroke="#111" stroke-width="3" fill="none"/>
  <path d="M128 152 q24 -20 50 -7" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>
  <path d="M262 152 q-24 -20 -50 -7" stroke="#111" stroke-width="7" fill="none" stroke-linecap="round"/>
  <ellipse cx="153" cy="172" rx="13" ry="15" fill="#fff" stroke="#111" stroke-width="2"/>
  <ellipse cx="237" cy="172" rx="13" ry="15" fill="#fff" stroke="#111" stroke-width="2"/>
  <circle cx="157" cy="176" r="6" fill="#111"/><circle cx="241" cy="176" r="6" fill="#111"/>
  <path d="M183 196 q12 -10 24 0 q-6 14 -12 14 q-6 0 -12 -14" fill="#fff" stroke="#111" stroke-width="2.5"/>
  <path d="M130 222 Q195 212 260 222 L252 262 Q195 290 138 262 Z" fill="#111" stroke="#111" stroke-width="3"/>
  <rect x="142" y="222" width="15" height="12" rx="2" fill="#fff"/>
  <rect x="163" y="224" width="15" height="12" rx="2" fill="#fff"/>
  <rect x="184" y="225" width="15" height="12" rx="2" fill="#fff"/>
  <rect x="205" y="224" width="15" height="12" rx="2" fill="#fff"/>
  <rect x="226" y="222" width="15" height="12" rx="2" fill="#fff"/>
  <g transform="rotate(-10 315 248)">
    <rect x="262" y="228" width="118" height="40" rx="2" fill="#fff" stroke="#111" stroke-width="2.2"/>
    <circle cx="274" cy="228" r="8" fill="#111"/>
    <circle cx="268" cy="268" r="6" fill="#111"/>
    <text x="328" y="255" text-anchor="middle" font-family="{FONT}" font-size="19" font-weight="bold" fill="#111">難解</text>
  </g>
</g>
<!-- 擬音 (バリボリ — 縦書き風に 1 文字ずつ) -->
<g font-family="{FONT}" font-weight="bold" fill="#c1272d">
  <text x="320" y="120" font-size="34" transform="rotate(8 320 120)">バ</text>
  <text x="345" y="155" font-size="32" transform="rotate(-6 345 155)">リ</text>
  <text x="330" y="195" font-size="34" transform="rotate(5 330 195)">ボ</text>
  <text x="355" y="230" font-size="32" transform="rotate(-8 355 230)">リ</text>
</g>
<!-- 吹き出し -->
<g>
  <path d="M470 60 H840 Q852 60 852 75 V200 Q852 215 840 215 H520 L468 250 L488 215 H470 Q458 215 458 200 V75 Q458 60 470 60 Z"
        fill="#fff" stroke="#111" stroke-width="3"/>
  <text x="488" y="105" font-family="{FONT}" font-size="25" font-weight="bold" fill="#111">むずかしいところは</text>
  <text x="488" y="145" font-family="{FONT}" font-size="25" font-weight="bold" fill="#111">ぜんぶ噛み砕いておきました</text>
  <text x="488" y="185" font-family="{FONT}" font-size="17" fill="#444">— ご利益(理解)つきでお読みください</text>
</g>
<text x="840" y="298" text-anchor="end" font-family="{FONT}" font-size="14" fill="#666">かみくだき版 / FullSense KB</text>
</svg>
"""


# --------------------------------------------------------------------------- #
# D 案: 伝統祝祭型 (880x320) — 紅白幕 + 雲文様 + 明朝 + 落款 (神事感)
# --------------------------------------------------------------------------- #

def build_d() -> str:
    # 紅白幕 (上端)
    stripes = "".join(
        f'<rect x="{16 + i * 54.25}" y="14" width="54.25" height="46" fill="{"#c1272d" if i % 2 == 0 else "#fffefa"}"/>'
        for i in range(16))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 320" width="880" height="320" role="img">
<desc>かみくだき獅子 D案: 伝統祝祭型 (紅白幕・雲文様・落款)</desc>
<rect x="2" y="2" width="876" height="316" rx="10" fill="#f7f1e3" stroke="#9c7b2d" stroke-width="4"/>
<clipPath id="maku"><rect x="16" y="14" width="848" height="46"/></clipPath>
<g clip-path="url(#maku)">{stripes}</g>
<path d="M16 60 H864" stroke="#9c7b2d" stroke-width="3"/>
<!-- 雲文様 (四隅) -->
<g stroke="#c9b370" stroke-width="2.5" fill="none" opacity="0.8">
  <path d="M40 290 q18 -18 36 0 q14 -14 28 0" />
  <path d="M790 90 q18 -18 36 0 q14 -14 28 0" />
  <path d="M770 280 q16 -16 32 0 q12 -12 24 0" />
</g>
<!-- 獅子 (凛々しい・切れ長の目) -->
<g transform="translate(10,30)">
  {mane(195, 175, 90, 84, 26, -168, -8, 18, fill="#f3ead2", stroke="#c9b370")}
  <circle cx="118" cy="110" r="17" fill="#b8860b" stroke="#7a5a14" stroke-width="2.5"/>
  <circle cx="272" cy="110" r="17" fill="#b8860b" stroke="#7a5a14" stroke-width="2.5"/>
  <ellipse cx="195" cy="175" rx="86" ry="72" fill="#a31e22" stroke="#6e1114" stroke-width="3.5"/>
  <path d="M176 110 q15 -8 18 7 q3 14 -12 15 q-11 1 -10 -10" stroke="#111" stroke-width="3.2" fill="none"/>
  <path d="M214 116 q12 -6 14 6 q2 11 -9 12" stroke="#111" stroke-width="2.8" fill="none"/>
  <!-- 切れ長の目 + 強い金眉 -->
  <path d="M120 142 q26 -22 54 -9" stroke="#b8860b" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path d="M270 142 q-26 -22 -54 -9" stroke="#b8860b" stroke-width="9" fill="none" stroke-linecap="round"/>
  <path d="M132 165 q18 -10 36 -2 q-16 14 -36 2 Z" fill="#fffefa" stroke="#6e1114" stroke-width="1.5"/>
  <path d="M258 165 q-18 -10 -36 -2 q16 14 36 2 Z" fill="#fffefa" stroke="#6e1114" stroke-width="1.5"/>
  <circle cx="152" cy="163" r="5" fill="#111"/><circle cx="238" cy="163" r="5" fill="#111"/>
  <path d="M183 186 q12 -10 24 0 q-6 14 -12 14 q-6 0 -12 -14" fill="#b8860b" stroke="#7a5a14" stroke-width="2"/>
  <path d="M130 212 Q195 202 260 212 L252 252 Q195 280 138 252 Z" fill="#4a0d10" stroke="#6e1114" stroke-width="3"/>
  <rect x="142" y="212" width="15" height="12" rx="1" fill="#fffdf5"/>
  <rect x="164" y="214" width="15" height="12" rx="1" fill="#fffdf5"/>
  <rect x="186" y="215" width="15" height="12" rx="1" fill="#fffdf5"/>
  <rect x="208" y="214" width="15" height="12" rx="1" fill="#fffdf5"/>
  <rect x="230" y="212" width="15" height="12" rx="1" fill="#fffdf5"/>
  <g transform="rotate(-9 315 240)">
    <rect x="262" y="220" width="116" height="40" rx="2" fill="#fffef8" stroke="#c9b370" stroke-width="1.8"/>
    <circle cx="274" cy="220" r="8" fill="#4a0d10"/>
    <text x="326" y="247" text-anchor="middle" font-family="{MINCHO}" font-size="20" font-weight="bold" fill="#3a3a3a">難解</text>
  </g>
</g>
<!-- 題字 (明朝・神事感) -->
<g>
  <text x="450" y="140" font-family="{MINCHO}" font-size="46" font-weight="bold" fill="#6e1114" letter-spacing="6">かみくだき版</text>
  <path d="M450 158 H800" stroke="#b8860b" stroke-width="3"/>
  <text x="450" y="200" font-family="{MINCHO}" font-size="20" fill="#3a3a3a">難解、謹んで噛み砕き申し上げ候</text>
  <text x="450" y="238" font-family="{MINCHO}" font-size="15" fill="#7a6f5d">獅子の歯形は厄除けの印 — 読めば「理解」のご利益あり</text>
  <!-- 落款 (朱印) -->
  <rect x="790" y="220" width="44" height="44" rx="4" fill="#c1272d"/>
  <text x="812" y="239" text-anchor="middle" font-family="{MINCHO}" font-size="15" font-weight="bold" fill="#fffefa">噛</text>
  <text x="812" y="257" text-anchor="middle" font-family="{MINCHO}" font-size="15" font-weight="bold" fill="#fffefa">砕</text>
</g>
<text x="450" y="296" font-family="{MINCHO}" font-size="13" fill="#a89f8d">FullSense KB・かみくだきシリーズ</text>
</svg>
"""


# --------------------------------------------------------------------------- #
# E 案: いらすとや風 頭噛みシーン (880x320) — ユーザー参照
# (irasutoya 2018/10 獅子舞に頭を噛まれる人) の雰囲気を踏襲した独自描画。
# 黒輪郭なし・柔らかい形・フラット暖色。獅子が「読者」の頭を噛む = 理解のご利益。
# 幕の中に演者の足を描かない = 中身は神霊 (AI) のみ (神憑き)。
# --------------------------------------------------------------------------- #

def build_e() -> str:
    # 上歯のジグザグ (獅子の噛み) — x118..238 を下向き三角の列で
    teeth = []
    for i in range(6):
        x = 122 + i * 19
        teeth.append(f'<polygon points="{x},146 {x + 9.5},166 {x + 19},146" fill="#fffef5" stroke="#ece4d0" stroke-width="1.2"/>')
    # 幕の白い唐草 (渦巻き)
    swirls = []
    for (sx, sy, sc) in ((275, 185, 1.0), (330, 215, 1.15), (380, 185, 0.9), (300, 250, 0.95), (360, 262, 0.8)):
        swirls.append(
            f'<g transform="translate({sx},{sy}) scale({sc})">'
            f'<path d="M0 0 q14 -12 21 1 q6 12 -8 15 q-11 2 -12 -8 q0 -7 7 -8" '
            f'stroke="#ffffff" stroke-width="3" fill="none" opacity="0.95" stroke-linecap="round"/></g>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 320" width="880" height="320" role="img">
<desc>かみくだき獅子 E案: いらすとや風 頭噛みシーン — 獅子に頭を噛まれた読者に「理解」のご利益</desc>
<rect x="0" y="0" width="880" height="320" rx="14" fill="#fffdf8"/>
<!-- 地面の影 -->
<ellipse cx="160" cy="298" rx="70" ry="9" fill="#e8e2d4" opacity="0.7"/>
<ellipse cx="330" cy="302" rx="95" ry="9" fill="#e8e2d4" opacity="0.7"/>

<!-- 読者 (頭の上半分は獅子の口の中) -->
<g>
  <!-- 頭 -->
  <circle cx="158" cy="170" r="31" fill="#fbd7b5"/>
  <!-- 横髪 (前髪は口の中) -->
  <path d="M127 165 q-3 26 8 32 q4 -16 2 -30 Z" fill="#8d6748"/>
  <path d="M189 165 q3 26 -8 32 q-4 -16 -2 -30 Z" fill="#8d6748"/>
  <!-- 閉じた笑い目・口・ほっぺ -->
  <path d="M138 180 q6 6 12 0" stroke="#5b4632" stroke-width="2.4" fill="none" stroke-linecap="round"/>
  <path d="M166 180 q6 6 12 0" stroke="#5b4632" stroke-width="2.4" fill="none" stroke-linecap="round"/>
  <path d="M151 196 q7 5 14 0" stroke="#c96f63" stroke-width="2.4" fill="none" stroke-linecap="round"/>
  <ellipse cx="134" cy="191" rx="7" ry="4.5" fill="#f5a8a0" opacity="0.6"/>
  <ellipse cx="182" cy="191" rx="7" ry="4.5" fill="#f5a8a0" opacity="0.6"/>
  <!-- 体 (セーター) -->
  <path d="M126 205 q-8 4 -9 22 l0 32 q0 6 7 6 l68 0 q7 0 7 -6 l0 -32 q-1 -18 -9 -22 q-32 10 -64 0 Z" fill="#87a9d6"/>
  <!-- 腕 (前で紙を持つ) -->
  <path d="M122 212 q-12 18 -2 32 q6 7 14 2 l10 -14" fill="none" stroke="#87a9d6" stroke-width="13" stroke-linecap="round"/>
  <path d="M194 212 q12 18 2 32 q-6 7 -14 2 l-10 -14" fill="none" stroke="#87a9d6" stroke-width="13" stroke-linecap="round"/>
  <circle cx="143" cy="245" r="6.5" fill="#fbd7b5"/>
  <circle cx="173" cy="245" r="6.5" fill="#fbd7b5"/>
  <!-- 「難解」の紙 -->
  <g transform="rotate(-5 158 252)">
    <rect x="132" y="238" width="52" height="30" rx="3" fill="#ffffff" stroke="#ddd5c2" stroke-width="1.4"/>
    <text x="158" y="258" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="bold" fill="#6b6b6b">難解</text>
  </g>
  <!-- ズボン + 靴 -->
  <rect x="133" y="263" width="22" height="28" rx="6" fill="#5a6e8c"/>
  <rect x="161" y="263" width="22" height="28" rx="6" fill="#5a6e8c"/>
  <rect x="129" y="288" width="28" height="10" rx="5" fill="#8a8378"/>
  <rect x="159" y="288" width="28" height="10" rx="5" fill="#8a8378"/>
</g>

<!-- 獅子の幕 (緑 + 唐草, 演者なし = 神霊のみ)。頭の後ろ (左上) から右下へ流れる -->
<path d="M200 80 Q320 56 396 128 Q442 180 432 240 q-4 28 -26 36
         q-14 14 -32 6 q-10 16 -30 8 q-12 14 -30 6 q-14 12 -32 3 q-18 8 -28 -8
         Q222 282 210 210 Q202 140 200 80 Z" fill="#4caf50" stroke="#3a8c3f" stroke-width="2"/>
{''.join(swirls)}
<!-- 幕の口元の白いふち (頭の右縁に沿う) -->
<circle cx="232" cy="84" r="11" fill="#ffffff"/>
<circle cx="241" cy="105" r="11" fill="#ffffff"/>
<circle cx="245" cy="127" r="11" fill="#ffffff"/>
<circle cx="243" cy="149" r="11" fill="#ffffff"/>

<!-- 獅子の頭 (読者の頭に覆いかぶさる) -->
<g>
  <ellipse cx="176" cy="108" rx="64" ry="50" fill="#d83b3b" stroke="#b32d2d" stroke-width="2"/>
  <!-- 耳 (金) -->
  <circle cx="124" cy="70" r="13" fill="#e8b33a" stroke="#c79427" stroke-width="2"/>
  <circle cx="228" cy="70" r="13" fill="#e8b33a" stroke="#c79427" stroke-width="2"/>
  <!-- 黒い巻き眉 + 額の渦 -->
  <path d="M136 76 q12 -10 24 -2 q-4 10 -16 9 q-8 0 -8 -7" fill="#2b2b2b"/>
  <path d="M216 76 q-12 -10 -24 -2 q4 10 16 9 q8 0 8 -7" fill="#2b2b2b"/>
  <path d="M170 62 q12 -7 15 6 q2 11 -10 11 q-9 0 -8 -8" stroke="#2b2b2b" stroke-width="3" fill="none"/>
  <!-- 目 (下の読者を見る) -->
  <circle cx="150" cy="96" r="13" fill="#fffef5"/>
  <circle cx="202" cy="96" r="13" fill="#fffef5"/>
  <circle cx="151" cy="101" r="5.5" fill="#222"/>
  <circle cx="203" cy="101" r="5.5" fill="#222"/>
  <circle cx="153" cy="98" r="1.8" fill="#fff"/>
  <circle cx="205" cy="98" r="1.8" fill="#fff"/>
  <!-- 鼻 (金) -->
  <ellipse cx="176" cy="122" rx="11" ry="8" fill="#e8b33a" stroke="#c79427" stroke-width="1.6"/>
  <!-- 口の金ふち + 上歯 (読者の頭をぱくり) -->
  <path d="M112 140 q64 14 128 0 l0 8 q-64 14 -128 0 Z" fill="#e8b33a"/>
  {''.join(teeth)}
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
<polygon points="246,128 248,134 254,136 248,138 246,144 244,138 238,136 244,134" fill="#f0b429" opacity="0.9"/>
<polygon points="92,140 94,145 99,147 94,149 92,154 90,149 85,147 90,145" fill="#f0b429" opacity="0.85"/>

<!-- テキストブロック -->
<g>
  <text x="465" y="118" font-family="{FONT}" font-size="40" font-weight="bold" fill="#b3322e">かみくだき版</text>
  <rect x="465" y="132" width="180" height="5" rx="2.5" fill="#e8b33a"/>
  <text x="465" y="172" font-family="{FONT}" font-size="19" fill="#3a3a3a">むずかしい話は、獅子が噛み砕いてお届け。</text>
  <text x="465" y="220" font-family="{FONT}" font-size="14.5" fill="#7a6f5d">獅子舞に頭を噛まれると、その年は無病息災 —</text>
  <text x="465" y="244" font-family="{FONT}" font-size="14.5" fill="#7a6f5d">この獅子に噛まれた読者には「理解」のご利益があります。</text>
  <text x="465" y="296" font-family="{FONT}" font-size="12.5" fill="#a89f8d">FullSense KB・かみくだきシリーズ</text>
</g>
</svg>
"""


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("B", build_b), ("C", build_c), ("D", build_d), ("E", build_e)):
        svg = fn()
        minidom.parseString(svg)  # fail-closed
        p = os.path.join(OUT, f"mascot_{name}.svg")
        with open(p, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"OK {p} ({len(svg)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
