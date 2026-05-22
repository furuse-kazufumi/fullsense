#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Qiita URL sync — LINK_MAP の確定 URL を本文の cross-link に一括置換.

QIITA_#24_LINK_MAP.md の表から確定 URL を読み取り、各 QIITA_#NN_*.md 内の
内部参照 (例: `QIITA_#14_*` (内部参照) や `[#14]`) を Qiita 確定 URL に置換する.

LINK_MAP の表形式 (例):

    | #14 | QIITA_#14_invisible_annotation_channel.md | <https://qiita.com/.../items/XXX> | 2026-05-22 |
    | #15 | QIITA_#15_second_brain_spiral_dev.md       | <https://qiita.com/.../items/YYY> | 2026-05-22 |
    | #16 | QIITA_#16_three_self_spirit_ai_management.md | _未投稿_                       | — |

URL が `_未投稿_` の行は skip (まだ確定していない).

置換ルール (本文中で対象):

1. ``QIITA_#NN_*` (内部参照)`` → `[<title>](<qiita_url>)`
2. ``QIITA_#NN_XX_*` (内部参照)`` → `[<title>](<qiita_url>)`  (#24 サブ番号付き)
3. `#NN-XX` 単独表記 (例: 「詳細は #24-05 で」) → 当該 URL 入り link に変換 (option, default OFF)

Usage:
    py -3.11 scripts/qiita_url_sync.py            # 全置換実行 (1, 2 ルール)
    py -3.11 scripts/qiita_url_sync.py --dry-run  # diff 表示のみ (書換しない)
    py -3.11 scripts/qiita_url_sync.py --aggressive  # ルール 3 も適用 (#NN-XX 単独)

dry-run なしで実行する場合は git で diff 確認 + revert 可能.

Exit code:
    0: success
    1: parse error (LINK_MAP のフォーマット崩れ等)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs" / "articles"
LINK_MAP = ROOT / "QIITA_#24_LINK_MAP.md"

# ---------------------------------------------------------------------------
# Parse LINK_MAP
# ---------------------------------------------------------------------------

#: LINK_MAP table row regex.
#:   | #14 | QIITA_#14_*.md | <https://qiita.com/.../items/XXX> | 2026-05-22 |
#: または `_未投稿_` の場合 URL がない.
TABLE_ROW = re.compile(
    r"^\|\s*(#\d+(?:-\d+)?)\s*\|\s*([\w#.\-]+\.md)\s*\|\s*"
    r"(?:<(https?://[^>]+)>|_未投稿_|—)\s*\|\s*([^|]*?)\s*\|$",
    re.MULTILINE,
)


def parse_link_map() -> dict[str, dict[str, str]]:
    """LINK_MAP から確定済 URL を抽出.

    Returns:
        dict[id, dict[fname / url / date]]
    """
    text = LINK_MAP.read_text(encoding="utf-8")
    out: dict[str, dict[str, str]] = {}
    for m in TABLE_ROW.finditer(text):
        article_id = m.group(1).lstrip("#")  # "14" / "24-00" 等
        fname = m.group(2)
        url = m.group(3) or ""
        date = m.group(4) or ""
        if url:
            out[article_id] = {"fname": fname, "url": url, "date": date}
    return out


# ---------------------------------------------------------------------------
# Extract title from article file
# ---------------------------------------------------------------------------


def extract_title(file: Path) -> str:
    text = file.read_text(encoding="utf-8")
    # frontmatter title:
    m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip().strip("\"'")
    # body H1
    m = re.search(r"^# (.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return file.stem


# ---------------------------------------------------------------------------
# Replace
# ---------------------------------------------------------------------------


def replace_in_text(
    text: str,
    posted: dict[str, dict[str, str]],
    aggressive: bool = False,
) -> tuple[str, list[str]]:
    """本文中の cross-link を Qiita URL に置換.

    Returns:
        (new_text, list_of_changes_description)
    """
    changes: list[str] = []
    new_text = text

    # Rule 1: ``QIITA_#NN_*` (内部参照)`` → markdown link
    pattern1 = re.compile(r"`?QIITA_#(\d+(?:_\d+)?)_[\w\-]+\.md`?\s*\(内部参照\)")

    def repl1(match: re.Match) -> str:
        raw_id = match.group(1)
        # "24_05" → "24-05" にも変換 (LINK_MAP は "24-05" 形式の場合もある)
        norm_id = raw_id.replace("_", "-") if "_" in raw_id else raw_id
        for try_id in (raw_id, norm_id):
            if try_id in posted:
                url = posted[try_id]["url"]
                fname = posted[try_id]["fname"]
                changes.append(f"  rule1: {match.group(0)} → {url}")
                return f"[{fname}]({url})"
        return match.group(0)  # 未投稿なら据置

    new_text = pattern1.sub(repl1, new_text)

    # Rule 2: ``[#NN-XX]`` 風の単独参照 (aggressive only)
    if aggressive:
        pattern2 = re.compile(r"#(\d+-\d+)\b")

        def repl2(match: re.Match) -> str:
            article_id = match.group(1)
            if article_id in posted:
                url = posted[article_id]["url"]
                changes.append(f"  rule2: #{article_id} → {url}")
                return f"[#{article_id}]({url})"
            return match.group(0)

        new_text = pattern2.sub(repl2, new_text)

    return new_text, changes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="diff 表示のみ")
    parser.add_argument(
        "--aggressive",
        action="store_true",
        help="単独 #NN-XX 表記も link 化 (誤爆リスクあり)",
    )
    args = parser.parse_args()

    posted = parse_link_map()
    if not posted:
        print("WARN: no posted articles found in LINK_MAP", file=sys.stderr)
        return 0

    print(f"Posted articles: {len(posted)}")
    for aid, info in sorted(posted.items()):
        print(f"  #{aid}: {info['fname']} → {info['url']}")
    print()

    files = sorted(ROOT.glob("QIITA_#*.md"))
    total_changes = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        new_text, changes = replace_in_text(text, posted, aggressive=args.aggressive)
        if not changes:
            continue
        print(f"[{f.name}] {len(changes)} changes")
        for c in changes[:5]:
            print(c)
        if len(changes) > 5:
            print(f"  ... ({len(changes) - 5} more)")
        total_changes += len(changes)
        if not args.dry_run:
            f.write_text(new_text, encoding="utf-8", newline="\n")

    print()
    if args.dry_run:
        print(f"DRY RUN: {total_changes} changes would be applied")
    else:
        print(f"APPLIED: {total_changes} changes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
