#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""NO-FM の QIITA_#NN_*.md に frontmatter skeleton を一括挿入する.

既存 #24_00 のテンプレを reference:

    ---
    title: <H1>
    tags:
      - FullSense
      - llive
      - 解説
      - <個別 1>
      - <個別 2>
    private: false
    updated_at: 'YYYY-MM-DD'
    id: null
    organization_url_name: null
    slide: false
    ignorePublish: true
    ---

`ignorePublish: true` で **draft 状態** から開始. 投稿時にユーザーが false に切替.

タグは「FullSense / llive / 解説」を default に, 残り 2 個は記事末尾の
`## 投稿時の推奨タグ` セクションがあれば抽出, なければ TODO プレースホルダ.

Usage:
    py -3.11 scripts/qiita_frontmatter_skeleton.py

dry-run (default はファイル書換): --dry-run flag は実装簡略化のため省略.
git で diff 確認 + revert 可能.
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "docs" / "articles"

DEFAULT_TAGS = ["FullSense", "llive", "解説"]


def parse_recommended_tags(text: str) -> list[str]:
    """記事末尾の `## 投稿時の推奨タグ` セクションから 1 番候補 5 個を抽出."""
    m = re.search(
        r"##\s*投稿時の推奨タグ.*?(?=\n##|\Z)", text, re.DOTALL
    )
    if not m:
        return []
    section = m.group(0)
    # コードブロック内の最初のタグ群を取得
    cb = re.search(r"```\s*\n(.*?)\n```", section, re.DOTALL)
    if not cb:
        # コードブロックがなければ箇条書きを試す
        tags = re.findall(r"^\s*[-*]\s+([^\s]+)", section, re.MULTILINE)
        return [t.strip("`") for t in tags[:5]]
    block = cb.group(1).strip()
    tags = [line.strip() for line in block.split("\n") if line.strip()]
    return tags[:5]


def extract_h1_title(text: str) -> str:
    m = re.search(r"^# (.+)$", text, re.MULTILINE)
    if not m:
        return "TITLE_TODO"
    return m.group(1).strip()


def guess_updated_at(file: Path) -> str:
    """ファイルの mtime 起源で日付推測. ファイル名に YYYY-MM-DD があれば優先."""
    # path に YYYY-MM-DD があれば
    m = re.search(r"(20\d{2}-\d{2}-\d{2})", str(file))
    if m:
        return m.group(1)
    return date.today().isoformat()


def build_frontmatter(title: str, tags: list[str], updated: str) -> str:
    yaml_tags = "\n".join(f"  - {t}" for t in tags)
    return (
        "---\n"
        f"title: {title}\n"
        f"tags:\n{yaml_tags}\n"
        "private: false\n"
        f"updated_at: '{updated}'\n"
        "id: null\n"
        "organization_url_name: null\n"
        "slide: false\n"
        "ignorePublish: true\n"
        "---\n\n"
    )


def has_frontmatter(text: str) -> bool:
    return re.match(r"^---\n.*?\n---\n", text, re.DOTALL) is not None


def process_file(file: Path) -> str:
    text = file.read_text(encoding="utf-8")
    if has_frontmatter(text):
        return "SKIP (has frontmatter)"

    title = extract_h1_title(text)
    recommended = parse_recommended_tags(text)
    # default 3 個 + 推奨先頭 2 個 (重複除く)
    tags = list(DEFAULT_TAGS)
    for t in recommended:
        if t not in tags and len(tags) < 5:
            tags.append(t)
    while len(tags) < 5:
        tags.append("TODO_TAG")

    updated = guess_updated_at(file)
    fm = build_frontmatter(title, tags, updated)
    new_text = fm + text

    file.write_text(new_text, encoding="utf-8", newline="\n")
    return f"OK  title=「{title[:30]}...」 tags={tags}"


def main() -> int:
    files = sorted(ROOT.glob("QIITA_#*.md"))
    for f in files:
        result = process_file(f)
        print(f"{f.name:<55} {result}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
