#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Build reusable animated SVG article assets.

Design rules:
- static-safe: the authored frame must already communicate the idea
- imgix-safe: avoid animateMotion / mpath, use animate + animateTransform only
- deterministic: no randomness
- stdlib only

Output:
  docs/articles/assets/motion_pack/*.svg
"""
from __future__ import annotations

from html import escape
from pathlib import Path
from xml.dom import minidom


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "articles" / "assets" / "motion_pack"

W = 960
H = 320
FONT = "'Segoe UI','Hiragino Sans','Noto Sans JP',sans-serif"
BG0 = "#09111f"
BG1 = "#0f1c33"
FG = "#e5eefc"
MUTED = "#93a6c6"
CYAN = "#5dd1ff"
GREEN = "#7ee787"
YELLOW = "#ffd166"
RED = "#ef476f"
PURPLE = "#8b7dff"


def esc(value: str) -> str:
    return escape(value, quote=True)


def text_node(
    x: float,
    y: float,
    content: str,
    *,
    fill: str,
    size: int,
    weight: str | None = None,
    anchor: str = "middle",
    extra: str = "",
) -> str:
    weight_attr = f' font-weight="{weight}"' if weight else ""
    extra_attr = f" {extra}" if extra else ""
    return (
        f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anchor}" fill="{fill}" '
        f'font-family="{FONT}" font-size="{size}"{weight_attr}{extra_attr}>'
        f"{esc(content)}</text>"
    )


def wrap(title: str, desc: str, body: str, defs: str = "") -> str:
    safe_title = esc(title)
    safe_desc = esc(desc)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{safe_title}" style="width:100%;height:auto;max-width:1200px">
  <title>{safe_title}</title>
  <desc>{safe_desc}</desc>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{BG1}"/>
      <stop offset="100%" stop-color="{BG0}"/>
    </linearGradient>
    {defs}
  </defs>
  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  {body}
</svg>
"""


def frame_title(main: str, sub: str) -> str:
    return "\n  " + text_node(W / 2, 32, main, fill=FG, size=22, weight="700") + "\n  " + text_node(
        W / 2, 54, sub, fill=MUTED, size=11
    ) + "\n"


def loop_observe_gate_repair() -> str:
    boxes = """
  <g font-family="{font}" font-size="13" text-anchor="middle">
    <g transform="translate(90 118)">
      <rect width="150" height="72" rx="12" fill="#12233d" stroke="{cyan}" stroke-opacity="0.35"/>
      <text x="75" y="31" fill="{fg}" font-weight="700">Observe</text>
      <text x="75" y="50" fill="{muted}" font-size="11">desired vs actual drift</text>
    </g>
    <g transform="translate(290 118)">
      <rect width="150" height="72" rx="12" fill="#142942" stroke="{yellow}" stroke-opacity="0.35"/>
      <text x="75" y="31" fill="{fg}" font-weight="700">Gate</text>
      <text x="75" y="50" fill="{muted}" font-size="11">block bad writes first</text>
    </g>
    <g transform="translate(490 118)">
      <rect width="150" height="72" rx="12" fill="#112b26" stroke="{green}" stroke-opacity="0.35"/>
      <text x="75" y="31" fill="{fg}" font-weight="700">Repair</text>
      <text x="75" y="50" fill="{muted}" font-size="11">patch smallest safe delta</text>
    </g>
    <g transform="translate(690 118)">
      <rect width="150" height="72" rx="12" fill="#261432" stroke="{purple}" stroke-opacity="0.35"/>
      <text x="75" y="31" fill="{fg}" font-weight="700">Meaning</text>
      <text x="75" y="50" fill="{muted}" font-size="11">human stays outside loop</text>
    </g>
  </g>
""".format(font=FONT, fg=FG, muted=MUTED, cyan=CYAN, yellow=YELLOW, green=GREEN, purple=PURPLE)
    flow = f"""
  <g fill="none" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" opacity="0.7">
    <path d="M240 154 H290"/>
    <path d="M440 154 H490"/>
    <path d="M640 154 H690"/>
    <path d="M765 204 C765 250 195 250 165 190"/>
  </g>
  <g stroke="{CYAN}" stroke-width="3" fill="{CYAN}">
    <circle cx="165" cy="190" r="5">
      <animateTransform attributeName="transform" type="translate"
        values="0 0;75 -36;275 -36;475 -36;675 -36;600 18;0 0"
        dur="7s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.95;0.95;0.55;0.95" dur="7s" repeatCount="indefinite"/>
    </circle>
  </g>
  <g fill="{RED}" opacity="0.22">
    <rect x="342" y="102" width="46" height="8" rx="4" opacity="0.22">
      <animate attributeName="opacity" values="0.22;0.95;0.22" dur="3.2s" repeatCount="indefinite"/>
    </rect>
    <rect x="344" y="96" width="42" height="20" rx="8" fill="none" stroke="{RED}" stroke-width="1.5" opacity="0.22">
      <animate attributeName="opacity" values="0.22;0.95;0.22" dur="3.2s" repeatCount="indefinite"/>
    </rect>
  </g>
"""
    body = frame_title("Observe -> Gate -> Repair -> Human Meaning", "A reusable motion asset for approval-loop articles")
    body += boxes + flow
    body += "\n  " + text_node(
        480,
        292,
        "The loop moves on its own, but the final interpretation stays with the operator.",
        fill=MUTED,
        size=11,
    ) + "\n"
    return wrap(
        "Observe gate repair loop",
        "Static-safe four-stage loop with a circulating token and visible gate pulse.",
        body,
    )


def worldmodel_rollout() -> str:
    body = frame_title("World Model Rollout", "Plan in latent space, then only commit safe steps")
    body += f"""
  <g font-family="{FONT}">
    <rect x="72" y="104" width="180" height="110" rx="14" fill="#13253f" stroke="{CYAN}" stroke-opacity="0.35"/>
    <text x="162" y="132" text-anchor="middle" fill="{FG}" font-size="18" font-weight="700">Current State</text>
    <text x="162" y="154" text-anchor="middle" fill="{MUTED}" font-size="11">observation + memory + controls</text>

    <rect x="314" y="86" width="258" height="146" rx="16" fill="#101f35" stroke="{PURPLE}" stroke-opacity="0.45"/>
    <text x="443" y="118" text-anchor="middle" fill="{FG}" font-size="18" font-weight="700">Dream Rollout</text>
    <text x="443" y="138" text-anchor="middle" fill="{MUTED}" font-size="11">multiple imagined futures, one safe branch selected</text>

    <rect x="650" y="104" width="238" height="110" rx="14" fill="#112a24" stroke="{GREEN}" stroke-opacity="0.35"/>
    <text x="769" y="132" text-anchor="middle" fill="{FG}" font-size="18" font-weight="700">Commit Action</text>
    <text x="769" y="154" text-anchor="middle" fill="{MUTED}" font-size="11">real actuator command after filtering</text>

    <path d="M252 159 H314" stroke="{CYAN}" stroke-width="2" fill="none" opacity="0.75"/>
    <path d="M572 159 H650" stroke="{GREEN}" stroke-width="2" fill="none" opacity="0.75"/>

    <g fill="none" stroke-width="2">
      <path d="M348 179 C404 209 462 207 522 174" stroke="{PURPLE}" opacity="0.48"/>
      <path d="M348 162 C406 122 462 120 528 151" stroke="{YELLOW}" opacity="0.62"/>
      <path d="M350 144 C408 90 468 92 532 134" stroke="{RED}" opacity="0.42"/>
    </g>

    <circle cx="350" cy="162" r="5" fill="{YELLOW}">
      <animate attributeName="cx" values="350;528;350" dur="4.5s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="162;151;162" dur="4.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="352" cy="179" r="4" fill="{PURPLE}" opacity="0.55">
      <animate attributeName="cx" values="352;520;352" dur="5.5s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="179;174;179" dur="5.5s" repeatCount="indefinite"/>
    </circle>
    <circle cx="350" cy="144" r="4" fill="{RED}" opacity="0.38">
      <animate attributeName="cx" values="350;532;350" dur="6s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="144;134;144" dur="6s" repeatCount="indefinite"/>
    </circle>
  </g>
"""
    return wrap(
        "World model rollout",
        "Current state flows into an imagined rollout box; multiple futures flicker while one branch is selected for real action.",
        body,
    )


def qd_archive_pulse() -> str:
    cells = []
    colors = [CYAN, GREEN, YELLOW, PURPLE]
    for r in range(3):
        for c in range(6):
            x = 180 + c * 82
            y = 96 + r * 58
            color = colors[(r + c) % len(colors)]
            begin = (r * 0.25) + (c * 0.18)
            cells.append(
                f'<rect x="{x}" y="{y}" width="64" height="40" rx="8" fill="{color}" opacity="0.22" stroke="{color}" stroke-opacity="0.35">'
                f'<animate attributeName="opacity" values="0.22;0.58;0.22" dur="4.6s" begin="{begin:.2f}s" repeatCount="indefinite"/></rect>'
            )
    body = frame_title("QD Archive Pulse", "Coverage grows by filling many niches, not by chasing one winner")
    body += f"""
  {text_node(96, 157, "behavior descriptor B", fill=MUTED, size=12, extra='transform="rotate(-90 96 157)"')}
  {text_node(480, 270, "behavior descriptor A", fill=MUTED, size=12)}
  <g fill="none" stroke="{MUTED}" stroke-opacity="0.35">
    <path d="M152 74 V238 H694"/>
  </g>
  <g>{''.join(cells)}</g>
  <g>
    <circle cx="220" cy="114" r="6" fill="{FG}">
      <animate attributeName="cx" values="220;380;542;622;220" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="114;172;114;172;114" dur="8s" repeatCount="indefinite"/>
    </circle>
  </g>
  <rect x="736" y="92" width="146" height="120" rx="12" fill="#102036" stroke="{CYAN}" stroke-opacity="0.25"/>
  {text_node(809, 120, "Archive view", fill=FG, size=16, weight="700")}
  {text_node(809, 145, "coverage, novelty, elites", fill=MUTED, size=11)}
  <rect x="762" y="166" width="94" height="12" rx="6" fill="{CYAN}" opacity="0.25"/>
  <rect x="762" y="166" width="42" height="12" rx="6" fill="{CYAN}">
    <animate attributeName="width" values="42;76;58;88;42" dur="6s" repeatCount="indefinite"/>
  </rect>
  {text_node(809, 199, "coverage pulse", fill=MUTED, size=10)}
"""
    return wrap(
        "QD archive pulse",
        "Animated grid of archive cells with a moving elite token and a side coverage bar.",
        body,
    )


def human_gate_funnel() -> str:
    body = frame_title("Human Gate Funnel", "Fast model proposals narrow into a small set of operator-approved writes")
    body += f"""
  <g font-family="{FONT}">
    <text x="178" y="102" text-anchor="middle" fill="{FG}" font-size="17" font-weight="700">Many proposals</text>
    <text x="480" y="102" text-anchor="middle" fill="{FG}" font-size="17" font-weight="700">Policy / verifier</text>
    <text x="784" y="102" text-anchor="middle" fill="{FG}" font-size="17" font-weight="700">Approved action</text>

    <g fill="{CYAN}" opacity="0.75">
      <circle cx="118" cy="132" r="10"><animateTransform attributeName="transform" type="translate" values="0 0;18 0;0 0" dur="3s" repeatCount="indefinite"/></circle>
      <circle cx="172" cy="158" r="9"><animateTransform attributeName="transform" type="translate" values="0 0;18 0;0 0" dur="3.4s" repeatCount="indefinite"/></circle>
      <circle cx="226" cy="132" r="10"><animateTransform attributeName="transform" type="translate" values="0 0;18 0;0 0" dur="3.1s" repeatCount="indefinite"/></circle>
      <circle cx="150" cy="192" r="9"><animateTransform attributeName="transform" type="translate" values="0 0;18 0;0 0" dur="3.6s" repeatCount="indefinite"/></circle>
      <circle cx="214" cy="192" r="9"><animateTransform attributeName="transform" type="translate" values="0 0;18 0;0 0" dur="3.8s" repeatCount="indefinite"/></circle>
    </g>

    <path d="M300 116 L610 116 L680 160 L610 204 L300 204 L370 160 Z" fill="#142942" stroke="{YELLOW}" stroke-opacity="0.45"/>
    <text x="470" y="152" text-anchor="middle" fill="{FG}" font-size="16" font-weight="700">fail closed</text>
    <text x="470" y="173" text-anchor="middle" fill="{MUTED}" font-size="11">unsafe or ambiguous paths do not pass</text>

    <rect x="736" y="128" width="96" height="64" rx="14" fill="#112a24" stroke="{GREEN}" stroke-opacity="0.5"/>
    <text x="784" y="155" text-anchor="middle" fill="{FG}" font-size="16" font-weight="700">WRITE</text>
    <text x="784" y="174" text-anchor="middle" fill="{MUTED}" font-size="10">one bounded delta</text>

    <circle cx="226" cy="132" r="8" fill="{YELLOW}">
      <animate attributeName="cx" values="226;352;784;784;226" dur="5.8s" repeatCount="indefinite"/>
      <animate attributeName="cy" values="132;160;160;160;132" dur="5.8s" repeatCount="indefinite"/>
    </circle>
    <circle cx="150" cy="192" r="7" fill="{RED}" opacity="0.32">
      <animate attributeName="opacity" values="0.32;0.32;0.1;0.32" dur="4.2s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0 0;120 -30;0 0" dur="4.2s" repeatCount="indefinite"/>
    </circle>
  </g>
"""
    return wrap(
        "Human gate funnel",
        "Multiple proposals converge into a fail-closed policy gate, then one safe write passes through.",
        body,
    )


def backend_swap_compare() -> str:
    body = frame_title("Backend Swap Compare", "Same interface, different engines, stable outer harness")
    body += f"""
  <g font-family="{FONT}">
    <rect x="74" y="112" width="178" height="96" rx="14" fill="#13253f" stroke="{CYAN}" stroke-opacity="0.35"/>
    <text x="163" y="144" text-anchor="middle" fill="{FG}" font-size="18" font-weight="700">Harness</text>
    <text x="163" y="168" text-anchor="middle" fill="{MUTED}" font-size="11">prompt, memory, gate, verifier</text>

    <rect x="708" y="88" width="162" height="144" rx="14" fill="#101f35" stroke="{PURPLE}" stroke-opacity="0.35"/>
    <text x="789" y="118" text-anchor="middle" fill="{FG}" font-size="17" font-weight="700">Backend lane</text>
    <g fill="{FG}" font-size="12" text-anchor="middle">
      <text x="789" y="146">Transformer</text>
      <text x="789" y="168">SSM</text>
      <text x="789" y="190">RWKV</text>
      <text x="789" y="212">Mamba</text>
    </g>

    <g>
      <rect x="372" y="132" width="184" height="56" rx="12" fill="#112a24" stroke="{GREEN}" stroke-opacity="0.35"/>
      <text x="464" y="154" text-anchor="middle" fill="{FG}" font-size="16" font-weight="700">Stable API</text>
      <text x="464" y="174" text-anchor="middle" fill="{MUTED}" font-size="11">same contract, swap engine beneath</text>
    </g>

    <path d="M252 160 H372" stroke="{CYAN}" stroke-width="2.2" opacity="0.75"/>
    <path d="M556 160 H708" stroke="{GREEN}" stroke-width="2.2" opacity="0.75"/>

    <rect x="732" y="132" width="114" height="20" rx="10" fill="{PURPLE}" opacity="0.82">
      <animate attributeName="y" values="132;154;176;198;132" dur="7s" repeatCount="indefinite"/>
    </rect>
    {text_node(789, 244, "engine cursor moves, outer contract stays", fill=MUTED, size=10)}
  </g>
"""
    return wrap(
        "Backend swap compare",
        "Static-safe comparison asset showing a stable harness and a moving backend selector.",
        body,
    )


def rocket_launch_land_cycle() -> str:
    body = frame_title("Rocket Launch -> Flip -> Landing", "One static-safe strip for ascent, boostback, descent, and soft touchdown")
    body += f"""
  <g font-family="{FONT}">
    <rect x="72" y="92" width="816" height="176" rx="18" fill="#0b1629" stroke="{CYAN}" stroke-opacity="0.16"/>
    <path d="M104 240 H856" stroke="{MUTED}" stroke-opacity="0.28" stroke-width="2"/>

    <text x="152" y="118" text-anchor="middle" fill="{FG}" font-size="14" font-weight="700">launch</text>
    <text x="364" y="118" text-anchor="middle" fill="{FG}" font-size="14" font-weight="700">coast / flip</text>
    <text x="584" y="118" text-anchor="middle" fill="{FG}" font-size="14" font-weight="700">descent burn</text>
    <text x="804" y="118" text-anchor="middle" fill="{FG}" font-size="14" font-weight="700">landing</text>

    <path d="M140 224
             C196 180 256 126 320 120
             S434 150 508 178
             S636 226 744 232
             S810 236 836 226"
          fill="none" stroke="{CYAN}" stroke-width="3" stroke-opacity="0.72" stroke-linecap="round"/>

    <g fill="none" stroke="{MUTED}" stroke-opacity="0.22" stroke-dasharray="4 6">
      <path d="M284 126 L284 240"/>
      <path d="M496 126 L496 240"/>
      <path d="M708 126 L708 240"/>
    </g>

    <g id="rocket-phase-launch" transform="translate(136 208)">
      <rect x="-8" y="-44" width="16" height="44" rx="7" fill="{FG}" opacity="0.96"/>
      <rect x="-10" y="-48" width="20" height="8" rx="4" fill="{CYAN}" opacity="0.95"/>
      <path d="M-8 0 L-13 11 H-6 L0 3 L6 11 H13 L8 0 Z" fill="{RED}" opacity="0.72"/>
    </g>
    <g id="rocket-phase-coast" transform="translate(342 126) rotate(-22)">
      <rect x="-8" y="-44" width="16" height="44" rx="7" fill="{FG}" opacity="0.92"/>
      <rect x="-10" y="-48" width="20" height="8" rx="4" fill="{CYAN}" opacity="0.86"/>
    </g>
    <g id="rocket-phase-flip" transform="translate(470 166) rotate(18)">
      <rect x="-8" y="-44" width="16" height="44" rx="7" fill="{FG}" opacity="0.9"/>
      <rect x="-10" y="-48" width="20" height="8" rx="4" fill="{PURPLE}" opacity="0.82"/>
    </g>
    <g id="rocket-phase-descent" transform="translate(584 206) rotate(8)">
      <rect x="-8" y="-44" width="16" height="44" rx="7" fill="{FG}" opacity="0.94"/>
      <rect x="-10" y="-48" width="20" height="8" rx="4" fill="{YELLOW}" opacity="0.92"/>
      <path d="M-8 0 L-13 10 H-6 L0 3 L6 10 H13 L8 0 Z" fill="{YELLOW}" opacity="0.54"/>
    </g>
    <g id="rocket-phase-landing" transform="translate(804 220)">
      <rect x="-8" y="-44" width="16" height="44" rx="7" fill="{FG}" opacity="0.98"/>
      <rect x="-10" y="-48" width="20" height="8" rx="4" fill="{GREEN}" opacity="0.96"/>
      <path d="M-8 0 L-12 8 H-6 L0 2 L6 8 H12 L8 0 Z" fill="{GREEN}" opacity="0.42"/>
    </g>

    <g transform="translate(0 0)">
      <g id="rocket-animated-token" transform="translate(130 208)">
        <rect x="-8" y="-44" width="16" height="44" rx="7" fill="{FG}" opacity="0.48"/>
        <rect x="-10" y="-48" width="20" height="8" rx="4" fill="{CYAN}" opacity="0.46"/>
        <path d="M-8 0 L-13 11 H-6 L0 3 L6 11 H13 L8 0 Z" fill="{RED}" opacity="0.56">
          <animate attributeName="opacity" values="0.18;0.72;0.18" dur="0.55s" repeatCount="indefinite"/>
        </path>
        <animateTransform attributeName="transform" type="translate"
          values="130 208;230 138;340 120;450 164;572 205;700 224;814 220"
          keyTimes="0;0.18;0.35;0.55;0.74;0.88;1"
          dur="8.5s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" additive="sum" type="rotate"
          values="0 0 -22;0 0 -22;0 0 18;0 0 12;0 0 0;0 0 0;0 0 0"
          keyTimes="0;0.22;0.4;0.58;0.76;0.9;1"
          dur="8.5s" repeatCount="indefinite"/>
      </g>
    </g>

    <g>
      <circle cx="230" cy="138" r="5" fill="{YELLOW}" opacity="0.9"/>
      <circle cx="340" cy="120" r="5" fill="{PURPLE}" opacity="0.9"/>
      <circle cx="572" cy="205" r="5" fill="{GREEN}" opacity="0.82"/>
      <circle cx="814" cy="220" r="5" fill="{GREEN}" opacity="0.95"/>
    </g>

    <path d="M122 214 C128 198 134 186 142 174" stroke="{RED}" stroke-width="2.2" stroke-opacity="0.38" fill="none"/>
    <path d="M562 206 C572 212 582 216 592 220" stroke="{YELLOW}" stroke-width="2.2" stroke-opacity="0.34" fill="none"/>
    <path d="M804 220 C804 206 804 194 804 180" stroke="{GREEN}" stroke-width="2.4" stroke-opacity="0.42" fill="none"/>

    <text x="480" y="289" text-anchor="middle" fill="{MUTED}" font-size="11">Use with the real GIF when motion matters; use this strip when Qiita must stay static-safe.</text>
  </g>
"""
    return wrap(
        "Rocket launch and landing cycle",
        "A booster ascends, flips, descends, and lands in one static-safe strip suitable for Qiita.",
        body,
    )


ARTS = {
    "loop_observe_gate_repair.svg": loop_observe_gate_repair,
    "worldmodel_rollout_strip.svg": worldmodel_rollout,
    "qd_archive_pulse.svg": qd_archive_pulse,
    "human_gate_funnel.svg": human_gate_funnel,
    "backend_swap_compare.svg": backend_swap_compare,
    "rocket_launch_land_cycle.svg": rocket_launch_land_cycle,
}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, builder in ARTS.items():
        svg = builder()
        minidom.parseString(svg.encode("utf-8"))
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"wrote {(OUT / name)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
