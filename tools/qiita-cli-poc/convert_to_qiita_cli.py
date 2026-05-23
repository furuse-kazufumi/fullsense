#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""convert_to_qiita_cli.py — 既存 FullSense 記事を @qiita/qiita-cli schema へ正規化する PoC。

入力: D:/projects/fullsense/docs/articles/ の記事を **コピー** したもの
      (このスクリプトは実記事を一切編集しない。input_copies/ のコピーに対してのみ動く)。
出力: public/<basename>.md (qiita-cli が publish 対象とするディレクトリ)。

設計方針:
  - 依存ゼロ (stdlib のみ)。frontmatter は軽量パーサで処理する。
  - private: true をデフォルト化 (Qiita の 24h 投稿数制限は限定共有=private には掛からない、
    という制限回避戦略のため)。
  - Jekyll 専用フィールド (layout / permalink / hero_svg 等) を除去。
  - qiita-cli が解釈しない補助フィールド (updated_at) は許容されるが、PoC では除去して最小 schema にする。
  - TODO_TAG プレースホルダタグを検出して警告 (Qiita タグ規則違反の温床)。

使い方:
  py -3.11 convert_to_qiita_cli.py [入力ファイル...]
  引数なしの場合は input_copies/*.md を全て変換する。
"""
from __future__ import annotations

import sys
import io
import glob
import os
import difflib
from pathlib import Path


def _ensure_utf8_stdout() -> None:
    """Windows cp932 console で日本語/em-dash/絵文字が化けないよう UTF-8 へ再設定。"""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        try:
            stream.reconfigure(encoding="utf-8")
        except (AttributeError, ValueError):
            try:
                setattr(sys, stream_name,
                        io.TextIOWrapper(stream.buffer, encoding="utf-8", newline=""))
            except (AttributeError, ValueError):
                pass


# qiita-cli が認識する frontmatter キー (公式 schema)
QIITA_CLI_KEYS = {
    "title", "tags", "private", "id",
    "organization_url_name", "slide", "ignorePublish",
}

# Jekyll / その他のプラットフォーム由来で qiita-cli では不要なキー
DROP_KEYS = {
    "layout", "permalink", "categories", "date", "author",  # Jekyll
    "hero_svg",                                              # FullSense 独自
    "updated_at",                                            # qiita-cli は許容するが PoC では最小化
}

PLACEHOLDER_TAGS = {"TODO_TAG", "TODO", "TBD", ""}

SCRIPT_DIR = Path(__file__).resolve().parent


def split_frontmatter(text: str):
    """先頭の `---\\n ... \\n---` を (frontmatter_lines, body) に分割。

    frontmatter が無ければ ([], text) を返す。
    """
    # 先頭 BOM を許容
    if text.startswith("﻿"):
        text = text.lstrip("﻿")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text
    # 2 番目の '---' を探す
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = lines[1:i]
            body = "\n".join(lines[i + 1:])
            return fm, body
    # 閉じ '---' が無い = frontmatter ではない
    return [], text


def parse_frontmatter(fm_lines):
    """軽量 YAML パーサ。スカラー値と block-sequence (- item) の list のみ対応。

    戻り値: dict[str, str|list[str]]、出現順を保つため Python 3.7+ の dict 順序に依存。
    """
    data = {}
    i = 0
    n = len(fm_lines)
    while i < n:
        raw = fm_lines[i]
        line = raw.rstrip()
        if not line.strip():
            i += 1
            continue
        # "key:" または "key: value"
        if ":" not in line:
            i += 1
            continue
        # インデント無しのトップレベルキーのみ扱う
        if line[:1] in (" ", "\t"):
            i += 1
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val == "":
            # 次行以降が block sequence なら list として収集
            seq = []
            j = i + 1
            while j < n:
                nxt = fm_lines[j]
                stripped = nxt.strip()
                if stripped.startswith("- "):
                    seq.append(_unquote(stripped[2:].strip()))
                    j += 1
                elif stripped == "":
                    j += 1
                elif nxt[:1] in (" ", "\t"):
                    # ネストした map 等は PoC では未対応 → スキップ
                    j += 1
                else:
                    break
            if seq:
                data[key] = seq
                i = j
                continue
            data[key] = ""
            i += 1
            continue
        # flow list ["a","b"] も最低限対応
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1]
            items = [_unquote(x.strip()) for x in inner.split(",") if x.strip()]
            data[key] = items
        else:
            data[key] = _unquote(val)
        i += 1
    return data


def _unquote(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    return s


def _to_bool(v, default: bool) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "yes", "1")
    return default


def normalize(data: dict, default_private: bool = True):
    """既存 frontmatter dict を qiita-cli schema へ正規化。

    戻り値: (out_dict, warnings)
    """
    warnings = []

    # title
    title = data.get("title", "")
    if isinstance(title, list):
        title = " ".join(title)
    if not title:
        warnings.append("title が空 — Qiita publish で拒否される")

    # tags: list 化 + プレースホルダ除去
    tags = data.get("tags", [])
    if isinstance(tags, str):
        tags = [tags] if tags else []
    clean_tags = []
    dropped_placeholders = 0
    for t in tags:
        t = str(t).strip()
        if t in PLACEHOLDER_TAGS:
            dropped_placeholders += 1
            continue
        if t not in clean_tags:
            clean_tags.append(t)
    if dropped_placeholders:
        warnings.append(f"TODO_TAG プレースホルダを {dropped_placeholders} 件除去 — 実タグへの差し替えが必要")
    if not clean_tags:
        warnings.append("有効なタグが 0 件 — Qiita は最低 1 個のタグを要求する")
    # Qiita はタグ最大 5 個
    if len(clean_tags) > 5:
        warnings.append(f"タグが {len(clean_tags)} 個 — Qiita 上限 5 個に切り詰め")
        clean_tags = clean_tags[:5]

    # private: 既存値があっても制限回避戦略のため default_private を優先する
    out = {
        "title": title,
        "tags": clean_tags,
        "private": default_private,
        "id": None,
        "organization_url_name": data.get("organization_url_name") or None,
        "slide": _to_bool(data.get("slide", False), False),
        # ignorePublish は元が true でも、移行後は publish したいので false にする
        "ignorePublish": False,
    }

    # Jekyll / 独自フィールドの除去を記録
    dropped = [k for k in data if k in DROP_KEYS]
    if dropped:
        warnings.append(f"非 qiita-cli フィールドを除去: {', '.join(dropped)}")
    unknown = [k for k in data if k not in QIITA_CLI_KEYS and k not in DROP_KEYS]
    if unknown:
        warnings.append(f"未知フィールドを除去: {', '.join(unknown)}")

    return out, warnings


def dump_frontmatter(out: dict) -> str:
    """qiita-cli schema dict を frontmatter テキストへ。tags は block sequence で出力。"""
    lines = ["---"]
    lines.append(f"title: {out['title']}")
    if out["tags"]:
        lines.append("tags:")
        for t in out["tags"]:
            lines.append(f"  - {t}")
    else:
        lines.append("tags: []")
    lines.append(f"private: {'true' if out['private'] else 'false'}")
    lines.append(f"id: {out['id'] if out['id'] is not None else 'null'}")
    org = out["organization_url_name"]
    lines.append(f"organization_url_name: {org if org is not None else 'null'}")
    lines.append(f"slide: {'true' if out['slide'] else 'false'}")
    lines.append(f"ignorePublish: {'true' if out['ignorePublish'] else 'false'}")
    lines.append("---")
    return "\n".join(lines)


def convert_file(in_path: Path, out_dir: Path, default_private: bool = True):
    text = in_path.read_text(encoding="utf-8")
    fm_lines, body = split_frontmatter(text)
    data = parse_frontmatter(fm_lines)
    out_fm, warnings = normalize(data, default_private=default_private)

    new_fm = dump_frontmatter(out_fm)
    # 本文は先頭の空行を 1 つに正規化
    new_text = new_fm + "\n\n" + body.lstrip("\n")
    # BOM 無し UTF-8 で出力
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / in_path.name
    out_path.write_text(new_text, encoding="utf-8", newline="\n")

    return out_path, fm_lines, new_fm.splitlines(), warnings


def print_diff(orig_fm_lines, new_fm_lines, name: str):
    print(f"\n--- frontmatter diff: {name} ---")
    diff = difflib.unified_diff(
        ["---"] + orig_fm_lines + ["---"],
        new_fm_lines,
        fromfile="before",
        tofile="after",
        lineterm="",
    )
    any_line = False
    for line in diff:
        any_line = True
        print(line)
    if not any_line:
        print("(変更なし)")


def main(argv):
    _ensure_utf8_stdout()
    args = argv[1:]
    if args:
        inputs = [Path(a) for a in args]
    else:
        inputs = sorted(SCRIPT_DIR.glob("input_copies/*.md"))
    if not inputs:
        print("入力ファイルが無い。input_copies/ に記事のコピーを置くか引数で指定する。")
        return 1

    out_dir = SCRIPT_DIR / "public"
    print(f"出力先: {out_dir}")
    print(f"既定 private: true (24h 投稿数制限の回避戦略)")

    for in_path in inputs:
        if not in_path.exists():
            print(f"[skip] 見つからない: {in_path}")
            continue
        out_path, orig_fm, new_fm, warnings = convert_file(in_path, out_dir)
        print(f"\n========== {in_path.name} ==========")
        print(f"-> {out_path}")
        print_diff(orig_fm, new_fm, in_path.name)
        if warnings:
            print("  warnings:")
            for w in warnings:
                print(f"    - {w}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
