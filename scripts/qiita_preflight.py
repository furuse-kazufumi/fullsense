#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Qiita 投稿 preflight checker.

docs/articles/QIITA_#NN_*.md の frontmatter / タイトル / タグ / 本文長 / 内部参照を
一覧化し、投稿準備状態を可視化する。

Usage:
    py -3.11 scripts/qiita_preflight.py

Output (UTF-8):
    file ... pub priv tags title_chars body_chars unresolved_refs

判定:
    pub:   ignorePublish の値 (TRUE = まだ非公開, false = 公開準備, NO-FM = frontmatter なし)
    priv:  private (Qiita 限定公開)
    tags:  タグ数 (5 個まで推奨)
    title_chars:  タイトル文字数 (Qiita 推奨 50 字以内)
    body_chars:   本文文字数 (frontmatter 除く)
    unresolved_refs: `QIITA_#NN_*` (内部参照) として残っている数

Exit code:
    0: 全 OK
    1: 警告あり (NO-FM / タグ 0 / タイトル 80 字超 / unresolved_refs > 0)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs" / "articles"


def main() -> int:
    files = sorted(ROOT.glob("QIITA_#*.md"))
    print(
        f"{'file':<55} {'pub':>6} {'priv':>5} {'tag':>4} "
        f"{'title':>5} {'body':>6} {'refs':>5}"
    )
    print("-" * 95)
    warnings = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        body_chars = len(text)
        unresolved_refs = len(re.findall(r"QIITA_#\d{2}_[\w-]*\` ?\(内部参照\)", text))
        if not m:
            title_match = re.search(r"^# (.+)$", text, re.MULTILINE)
            title = title_match.group(1) if title_match else "(no title)"
            print(
                f"{f.name:<55} {'NO-FM':>6} {'-':>5} {'-':>4} "
                f"{len(title):>5} {body_chars:>6} {unresolved_refs:>5}"
            )
            warnings += 1
            continue

        fm = m.group(1)
        body_chars = len(text) - len(m.group(0))

        if re.search(r"ignorePublish:\s*true", fm):
            ip = "TRUE"
        elif re.search(r"ignorePublish:\s*false", fm):
            ip = "false"
        else:
            ip = "-"

        if re.search(r"private:\s*true", fm):
            pv = "true"
        elif re.search(r"private:\s*false", fm):
            pv = "false"
        else:
            pv = "-"

        tags_match = re.search(r"tags:\s*\n((?:  - .+\n)+)", fm)
        tag_count = (
            len(tags_match.group(1).strip().split("\n")) if tags_match else 0
        )

        title_match = re.search(r"title:\s*(.+)", fm)
        title = title_match.group(1).strip() if title_match else "-"
        title_chars = len(title)

        flag = ""
        if tag_count == 0:
            flag += " [TAGS=0]"
            warnings += 1
        if title_chars > 80:
            flag += " [TITLE-LONG]"
            warnings += 1
        if unresolved_refs > 0:
            flag += f" [REFS={unresolved_refs}]"
            warnings += 1

        print(
            f"{f.name:<55} {ip:>6} {pv:>5} {tag_count:>4} "
            f"{title_chars:>5} {body_chars:>6} {unresolved_refs:>5}{flag}"
        )

    print()
    print(f"Total files: {len(files)}, warnings: {warnings}")
    return 0 if warnings == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
