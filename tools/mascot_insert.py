#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mascot_insert.py — かみくだき記事へ獅子舞マスコットバナーを挿入する (stdlib only).

対象: かみくだき 9 本 (8 本 = `# 日本語/# English/# 中文/# 한국어` 区切りの標準 4 言語縦積み、
llive_mega = 言語別タイトル H1 直書きの別スタイル [memory: reference_qiita_team_fullsense 注意書き])。

挿入位置: 各言語セクションのタイトル H1 直後 (hero 画像の位置)。
冪等: 本文に 'kamikudaki_shishi' があれば skip。
fail-closed: アンカー数が期待 (4 言語) と合わないファイルは変更せず報告。
既定 dry-run / 書き込みは --yes。code fence 内の見出しは無視。
"""
from __future__ import annotations

import os
import re
import sys


def _utf8() -> None:
    for s in ("stdout", "stderr"):
        try:
            getattr(sys, s).reconfigure(encoding="utf-8")
        except Exception:
            pass


ART = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "articles"))
RAW = "https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot"

LANG_ORDER = ["ja", "en", "zh", "ko"]
LANG_HEADINGS = {"# 日本語": "ja", "# English": "en", "# 中文": "zh", "# 한국어": "ko"}
IMG = {
    "ja": f"![かみくだき獅子 — 噛まれた読者に「理解」のご利益]({RAW}/kamikudaki_shishi.svg)",
    "en": f"![Kamikudaki lion — a bite that grants the blessing of understanding]({RAW}/kamikudaki_shishi_en.svg)",
    "zh": f"![通俗易懂版舞狮 — 被咬的读者获得「理解」的福气]({RAW}/kamikudaki_shishi_zh.svg)",
    "ko": f"![쉬운 설명판 사자탈 — 물린 독자에게 「이해」의 복]({RAW}/kamikudaki_shishi_ko.svg)",
}

TARGETS = [
    ("std", os.path.join(ART, "QIITA_#26_lldarwin_multi_pressure_selection_kamikudaki.md")),
    ("std", os.path.join(ART, "QIITA_#27_lldarwin_v2_overnight_marathon_kamikudaki.md")),
    ("std", os.path.join(ART, "QIITA_#35_00_verifier_sdp_not_smt_index_kamikudaki.md")),
    ("std", os.path.join(ART, "QIITA_#35_01_verifier_frontier_sdp_kamikudaki.md")),
    ("std", os.path.join(ART, "QIITA_#35_02_honest_disclosure_solver_swap_kamikudaki.md")),
    ("std", os.path.join(ART, "drafts", "QIITA_#29_falsification_goodhart_proxy_limits_kamikudaki.md")),
    ("std", os.path.join(ART, "drafts", "QIITA_#33_llcore_third_axis_settle_kamikudaki.md")),
    ("std", os.path.join(ART, "drafts", "QIITA_#34_third_axis_arc_overview_kamikudaki.md")),
    ("mega", os.path.join(ART, "QIITA_llive_mega_evolution.md")),
]


def _h1_lines(lines: list[str]) -> list[int]:
    """code fence 外の `# ` 行 index を返す。frontmatter (--- 区切り) はスキップ。"""
    out, in_fence, i = [], False, 0
    # frontmatter を飛ばす
    if lines and lines[0].strip() == "---":
        for j in range(1, len(lines)):
            if lines[j].strip() == "---":
                i = j + 1
                break
    for k in range(i, len(lines)):
        s = lines[k]
        if s.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and s.startswith("# "):
            out.append(k)
    return out


def plan_insertions(mode: str, lines: list[str]) -> list[tuple[int, str]] | None:
    """挿入計画 [(line_index_after, lang)] を返す。アンカー不整合は None (fail-closed)。"""
    h1s = _h1_lines(lines)
    plan: list[tuple[int, str]] = []
    if mode == "std":
        for idx in h1s:
            lang = LANG_HEADINGS.get(lines[idx].strip())
            if not lang:
                continue
            # この言語見出しの次の H1 = タイトル行
            nxt = [j for j in h1s if j > idx]
            if not nxt:
                return None
            plan.append((nxt[0], lang))
        if [lg for _, lg in plan] != LANG_ORDER:
            return None
    else:  # mega: 言語タイトル H1 直書き ×4 (出現順 = ja,en,zh,ko)
        titles = [idx for idx in h1s if lines[idx].strip() not in LANG_HEADINGS]
        if len(titles) != 4:
            return None
        plan = list(zip(titles, LANG_ORDER))
    return plan


def process(mode: str, path: str, write: bool) -> str:
    if not os.path.exists(path):
        return f"[MISSING] {os.path.basename(path)}"
    text = open(path, "r", encoding="utf-8-sig").read()
    if "kamikudaki_shishi" in text:
        return f"[SKIP already] {os.path.basename(path)}"
    lines = text.split("\n")
    plan = plan_insertions(mode, lines)
    if plan is None:
        return f"[FAIL-CLOSED anchors] {os.path.basename(path)} (期待 4 言語アンカーと不一致 — 未変更)"
    # 後ろから挿入して index を保つ
    for idx, lang in sorted(plan, reverse=True):
        lines[idx + 1:idx + 1] = ["", IMG[lang]]
    if write:
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    pos = ",".join(f"{lg}@{ix + 1}" for ix, lg in plan)
    return f"[{'OK' if write else 'PLAN'}] {os.path.basename(path)}  mode={mode}  {pos}"


def main() -> int:
    _utf8()
    write = "--yes" in sys.argv
    ok = True
    for mode, path in TARGETS:
        msg = process(mode, path, write)
        ok = ok and not msg.startswith(("[FAIL", "[MISSING"))
        print(msg)
    print(f"\n{'written' if write else 'dry-run (add --yes to write)'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
