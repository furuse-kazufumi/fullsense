#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Qiita 投稿 preflight checker.

docs/articles/QIITA_#NN_*.md の frontmatter / タイトル / タグ / 本文長 /
内部参照を一覧化し、投稿準備状態を可視化する。
`--include-drafts` を付けると docs/articles/drafts/QIITA*.md も対象に含める。
公開対象記事 (`docs/articles/QIITA_#*.md`) では project_group 必須を確認し、
`*_LINK_MAP.md` のような補助文書は除外する。
draft では publish-ready 候補
(`ignorePublish` / `private` / `public_private` / `id` / `qiita_public_id` /
`public_id` のいずれかを持つもの) すべてに group lint を適用する。

Usage:
    py -3.11 scripts/qiita_preflight.py
    py -3.11 scripts/qiita_preflight.py --include-drafts
    py -3.11 scripts/qiita_preflight.py --json

Output (UTF-8):
    file ... pub priv tags title_chars body_chars unresolved_refs
    Warning breakdown: KEY=COUNT, ...
    Warning breakdown JSON: {"KEY": COUNT, ...}
    Warning files JSON: {"KEY": ["file.md", ...], ...}
    --json: {"total_files": ..., "warnings": ..., "counts": {...}, "files": {...}}

判定:
    pub:   ignorePublish の値 (TRUE = まだ非公開, false = 公開準備, NO-FM = frontmatter なし)
    priv:  private (Qiita 限定公開)
    tags:  タグ数 (5 個まで推奨)
    title_chars:  実投稿タイトル文字数。既定では frontmatter title を正本にし、
                  title が無い場合だけ本文側 H1 を使う
    body_chars:   本文文字数 (frontmatter 除く)
    unresolved_refs: `QIITA_#NN_*` (内部参照) として残っている数
    group warnings:
        - 公開対象記事では project_group 必須
        - draft では publish-ready 候補すべてに project_group 必須
        - canonical 名 typo、related_groups 内の自己重複、
          project_group の related_groups 混入を警告

Exit code:
    0: 全 OK
    1: 警告あり
       (NO-FM / タグ 0 / タイトル 80 字超 / unresolved_refs > 0 /
        GROUP-MISSING / GROUP=* / RELATED=* / RELATED-DUP /
        GROUP-IN-RELATED / TITLE-MISMATCH / TITLE-HITL)
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import lru_cache
import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ROOT = Path(__file__).resolve().parent.parent / "docs" / "articles"
DRAFTS = ROOT / "drafts"
TOOLS_DIR = REPO_ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

from _frontmatter import (
    find_quoted_scalar_end,
    parse_frontmatter_lines,
    parse_inline_list_value,
    parse_scalar_value,
    resolve_body_title,
    strip_unquoted_inline_comment,
    split_frontmatter_lines as shared_split_frontmatter_lines,
)
from _qiita_title_guard import (
    EMPTY_TREE_HASH,
    git_ref_exists as shared_git_ref_exists,
    has_title_mismatch as shared_has_title_mismatch,
    load_git_text_at_rev as shared_load_git_text_at_rev,
    meta_has_identity as shared_meta_has_identity,
    resolve_upstream_ref as shared_resolve_upstream_ref,
    should_report_title_mismatch as shared_should_report_title_mismatch,
    title_change_requires_human_gate as shared_title_change_requires_human_gate,
)

# Qiita article taxonomy is narrower than the product family tree.
# `llove` remains intentionally excluded until there is a stable article lane
# that cannot be expressed under the existing groups without drift.
CANONICAL_GROUPS = {"gaitlab", "spikelab", "onocollo", "llcore", "llive", "llmesh"}
BLOCK_SCALAR_VALUES = {">", ">-", ">+", "|", "|-", "|+"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-drafts",
        action="store_true",
        help="also scan docs/articles/drafts/QIITA*.md; apply project-group lint to public files and all publish-ready drafts",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit a single machine-readable JSON object instead of the table/summary text",
    )
    return parser.parse_args()


def iter_targets(include_drafts: bool) -> list[Path]:
    files = sorted(ROOT.glob("QIITA_#*.md"))
    if include_drafts:
        files += sorted(DRAFTS.glob("QIITA*.md"))
    return files


def split_frontmatter(text: str) -> tuple[str | None, str]:
    fm_lines, body = shared_split_frontmatter_lines(text)
    if not fm_lines:
        return None, text
    newline = "\r\n" if "\r\n" in text else "\n"
    return newline.join(fm_lines), body


def parse_frontmatter_meta(fm: str | None) -> dict:
    if not fm:
        return {}
    return parse_frontmatter_lines(fm.splitlines())


def parse_csv_list_value(value: str) -> list[str]:
    items: list[str] = []
    buf: list[str] = []
    quote: str | None = None
    for ch in value:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in ("'", '"'):
            quote = ch
            buf.append(ch)
            continue
        if ch == ",":
            item = parse_scalar_value(
                "".join(buf).strip(), allow_unquoted_comment=True
            )
            if item:
                items.append(item)
            buf = []
            continue
        buf.append(ch)
    if buf:
        item = parse_scalar_value("".join(buf).strip(), allow_unquoted_comment=True)
        if item:
            items.append(item)
    return items


def parse_yaml_list_field(fm: str, field_name: str) -> list[str]:
    lines = fm.splitlines()
    values: list[str] = []
    collecting = False
    for line in lines:
        if not collecting:
            if re.match(rf"^{re.escape(field_name)}:\s*(?:#.*)?$", line):
                collecting = True
                continue
            inline_match = re.match(
                rf"^{re.escape(field_name)}:\s*(\[.*\])(?:\s+#.*)?\s*$", line
            )
            if inline_match:
                return parse_inline_list_value(inline_match.group(1))
            scalar_match = re.match(rf"^{re.escape(field_name)}:\s*(.+?)\s*$", line)
            if scalar_match:
                return parse_csv_list_value(scalar_match.group(1))
            if re.match(rf"^{re.escape(field_name)}:\s*$", line):
                collecting = True
            continue
        if re.match(r"^\S", line):
            break
        m = re.match(r"^\s*-\s*(.+?)\s*$", line)
        if m:
            values.append(parse_scalar_value(m.group(1), allow_unquoted_comment=True))
    return values


def parse_group_fields(fm: str) -> tuple[str | None, list[str]]:
    meta = parse_frontmatter_meta(fm)
    project_group = meta.get("project_group")
    related_groups = parse_yaml_list_field(fm, "related_groups")
    if not related_groups:
        raw_related = meta.get("related_groups") or []
        if isinstance(raw_related, str):
            raw_related = [raw_related]
        related_groups = [
            parse_scalar_value(str(group), allow_unquoted_comment=True)
            for group in raw_related
            if parse_scalar_value(str(group), allow_unquoted_comment=True)
        ]
    return (
        (
            parse_scalar_value(str(project_group), allow_unquoted_comment=True)
            if project_group not in (None, "")
            else None
        ),
        related_groups,
    )


def group_field_findings(fm: str, require_project_group: bool = False) -> list[str]:
    project_group, related_groups = parse_group_fields(fm)
    findings: list[str] = []
    if require_project_group and not project_group:
        findings.append("[GROUP-MISSING]")
    if project_group and project_group not in CANONICAL_GROUPS:
        findings.append(f"[GROUP={project_group}]")
    for group in related_groups:
        if group not in CANONICAL_GROUPS:
            findings.append(f"[RELATED={group}]")
    if len(related_groups) != len(set(related_groups)):
        findings.append("[RELATED-DUP]")
    if project_group and project_group in related_groups:
        findings.append("[GROUP-IN-RELATED]")
    return findings


def resolve_frontmatter_title(fm: str) -> str | None:
    title_match = re.search(r"^title:\s*(.+)$", fm, re.MULTILINE)
    if title_match:
        raw_value = title_match.group(1).strip()
        if raw_value in BLOCK_SCALAR_VALUES:
            title = parse_frontmatter_meta(fm).get("title")
            if title not in (None, ""):
                return str(title).strip()
        elif raw_value[:1] in {"'", '"'}:
            quote_end = find_quoted_scalar_end(raw_value)
            uncommented = raw_value
            if quote_end is not None:
                uncommented = raw_value[: quote_end + 1]
            title = parse_frontmatter_lines([f"title: {uncommented}"]).get("title")
            if title not in (None, ""):
                return str(title).strip()
        else:
            return strip_unquoted_inline_comment(raw_value)
    title = parse_frontmatter_meta(fm).get("title")
    if title in (None, ""):
        return None
    return str(title).strip()


def resolve_title(fm: str, body: str) -> str:
    fm_title = resolve_frontmatter_title(fm)
    if fm_title:
        return fm_title
    body_title = resolve_body_title(body)
    if body_title:
        return body_title
    return "-"


def resolve_publish_title(fm: str, body: str) -> str:
    return resolve_title(fm, body)


def title_findings(fm: str, body: str) -> list[str]:
    return ["[TITLE-MISMATCH]"] if shared_has_title_mismatch(parse_frontmatter_meta(fm), body) else []


def is_publish_ready_draft(fm: str) -> bool:
    meta = parse_frontmatter_meta(fm)
    if any(key in meta for key in ("ignorePublish", "private", "public_private")):
        return True
    # Identity keys count only when non-nullish, matching qiita_public_post.py and
    # qiita_team_post.py. A bare `id: null` / `public_id: null` / `qiita_public_id: null`
    # is NOT publish-ready and must not trip the project_group requirement (that was a
    # false GROUP-MISSING source).
    return shared_meta_has_identity(meta, "id", "qiita_public_id", "public_id")


def requires_project_group(path: Path, fm: str, include_drafts: bool) -> bool:
    if path.name.endswith("_LINK_MAP.md"):
        return False
    if path.parent == DRAFTS:
        return include_drafts and is_publish_ready_draft(fm)
    return True


def requires_title_sync(path: Path) -> bool:
    return not path.name.endswith("_LINK_MAP.md")


def has_publish_identity(fm: str) -> bool:
    return shared_meta_has_identity(parse_frontmatter_meta(fm), "public_id")


def has_team_identity(path: Path, fm: str) -> bool:
    meta = parse_frontmatter_meta(fm)
    if path.parent != DRAFTS:
        return False
    return shared_meta_has_identity(meta, "id", "qiita_item_id")


def has_live_identity(path: Path, fm: str) -> bool:
    return has_publish_identity(fm) or has_team_identity(path, fm)


@lru_cache(maxsize=1)
def resolve_upstream_ref() -> str | None:
    return shared_resolve_upstream_ref(str(REPO_ROOT))


def git_ref_exists(ref: str) -> bool:
    return shared_git_ref_exists(REPO_ROOT, ref)


@lru_cache(maxsize=1)
def resolve_hitl_baseline_commit() -> str | None:
    refs: list[str] = []
    upstream = resolve_upstream_ref()
    if upstream:
        refs.append(upstream)
    for fallback in ("origin/main", "origin/master", "main", "master"):
        if fallback not in refs and git_ref_exists(fallback):
            refs.append(fallback)
    for ref in refs:
        try:
            result = subprocess.run(
                ["git", "merge-base", "HEAD", ref],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=REPO_ROOT,
            )
        except OSError:
            return None
        commit = result.stdout.strip()
        if commit:
            return commit
    if git_ref_exists("HEAD^"):
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD^"],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                cwd=REPO_ROOT,
            )
        except OSError:
            return None
        commit = result.stdout.strip()
        if commit:
            return commit
    if git_ref_exists("HEAD"):
        return EMPTY_TREE_HASH
    return None


@lru_cache(maxsize=None)
def load_git_text_at_rev(rev: str, path_str: str) -> str | None:
    return shared_load_git_text_at_rev(str(REPO_ROOT), rev, path_str)


@lru_cache(maxsize=None)
def load_hitl_baseline_text(path_str: str) -> str | None:
    baseline = resolve_hitl_baseline_commit()
    if not baseline:
        return None
    return load_git_text_at_rev(baseline, path_str)


# TITLE_HITL is public_id-only by contract (docs/articles/QIITA_POST_GUIDE.md): a
# `[TITLE-HITL]` human gate is raised for public_id articles with an unreflected
# publish-title change, while `id` / `qiita_public_id` mirror / Team-系 items are
# handled by a separate gate and must NOT be mixed into the TITLE_HITL count. The
# guide already asserts the impl excludes `id`; this keeps the impl matching that.
_TITLE_HITL_IDENTITY_KEYS = ("public_id",)


def title_change_requires_human_gate(path: Path, fm: str, body: str) -> bool:
    return shared_title_change_requires_human_gate(
        parse_frontmatter_meta(fm),
        body,
        baseline_text=load_hitl_baseline_text(str(path)),
        live_identity_keys=_TITLE_HITL_IDENTITY_KEYS,
    )


def should_report_title_mismatch(path: Path, fm: str, body: str) -> bool:
    return shared_should_report_title_mismatch(
        parse_frontmatter_meta(fm),
        body,
        baseline_text=load_hitl_baseline_text(str(path)),
        live_identity_keys=_TITLE_HITL_IDENTITY_KEYS,
    )


def summary_key(finding: str) -> str:
    if finding == "[TAGS=0]":
        return "TAGS_EMPTY"
    if finding == "[TITLE-LONG]":
        return "TITLE_LONG"
    if finding.startswith("[REFS="):
        return "REFS"
    if finding == "[TITLE-HITL]":
        return "TITLE_HITL"
    if finding == "[TITLE-MISMATCH]":
        return "TITLE_MISMATCH"
    if finding == "[GROUP-MISSING]":
        return "GROUP_MISSING"
    if finding == "[RELATED-DUP]":
        return "RELATED_DUP"
    if finding == "[GROUP-IN-RELATED]":
        return "GROUP_IN_RELATED"
    if finding.startswith("[GROUP="):
        return "GROUP_INVALID"
    if finding.startswith("[RELATED="):
        return "RELATED_INVALID"
    if finding == "NO-FM":
        return "NO_FM"
    return finding.strip("[]").replace("-", "_").replace("=", "_")


def build_report(
    files: list[Path],
    counts: Counter[str],
    detail_files: dict[str, list[str]],
    warnings: int,
) -> dict[str, object]:
    return {
        "total_files": len(files),
        "warnings": warnings,
        "counts": dict(sorted(counts.items())),
        "files": {
            key: sorted(set(values))
            for key, values in sorted(detail_files.items())
        },
    }


def main() -> int:
    args = parse_args()
    files = iter_targets(args.include_drafts)
    counts: Counter[str] = Counter()
    detail_files: dict[str, list[str]] = {}
    if not args.json:
        print(
            f"{'file':<55} {'pub':>6} {'priv':>5} {'tag':>4} "
            f"{'title':>5} {'body':>6} {'refs':>5}"
        )
        print("-" * 95)
    warnings = 0
    for f in files:
        text = f.read_text(encoding="utf-8-sig")
        fm_text, body = split_frontmatter(text)
        body_chars = len(text)
        unresolved_refs = len(re.findall(r"QIITA_#\d{2}_[\w-]*\` ?\(内部参照\)", text))
        if fm_text is None:
            title_match = re.search(r"^# (.+)$", text, re.MULTILINE)
            title = title_match.group(1) if title_match else "(no title)"
            if not args.json:
                print(
                    f"{f.name:<55} {'NO-FM':>6} {'-':>5} {'-':>4} "
                    f"{len(title):>5} {body_chars:>6} {unresolved_refs:>5}"
                )
            warnings += 1
            key = summary_key("NO-FM")
            counts[key] += 1
            detail_files.setdefault(key, []).append(f.name)
            continue

        fm = fm_text
        body_chars = len(body)

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

        tag_count = len(parse_yaml_list_field(fm, "tags"))

        title = resolve_title(fm, body)
        title_chars = len(title)

        flag = ""
        if tag_count == 0:
            flag += " [TAGS=0]"
            warnings += 1
            key = summary_key("[TAGS=0]")
            counts[key] += 1
            detail_files.setdefault(key, []).append(f.name)
        if title_chars > 80:
            flag += " [TITLE-LONG]"
            warnings += 1
            key = summary_key("[TITLE-LONG]")
            counts[key] += 1
            detail_files.setdefault(key, []).append(f.name)
        if unresolved_refs > 0:
            flag += f" [REFS={unresolved_refs}]"
            warnings += 1
            key = summary_key(f"[REFS={unresolved_refs}]")
            counts[key] += 1
            detail_files.setdefault(key, []).append(f.name)
        if requires_title_sync(f):
            mismatch_findings = title_findings(fm, body) if should_report_title_mismatch(f, fm, body) else []
            for finding in mismatch_findings:
                flag += f" {finding}"
                warnings += 1
                key = summary_key(finding)
                counts[key] += 1
                detail_files.setdefault(key, []).append(f.name)
            if title_change_requires_human_gate(f, fm, body):
                flag += " [TITLE-HITL]"
                warnings += 1
                key = summary_key("[TITLE-HITL]")
                counts[key] += 1
                detail_files.setdefault(key, []).append(f.name)
        require_project_group = requires_project_group(f, fm, args.include_drafts)
        for finding in group_field_findings(fm, require_project_group=require_project_group):
            flag += f" {finding}"
            warnings += 1
            key = summary_key(finding)
            counts[key] += 1
            detail_files.setdefault(key, []).append(f.name)

        if not args.json:
            print(
                f"{f.name:<55} {ip:>6} {pv:>5} {tag_count:>4} "
                f"{title_chars:>5} {body_chars:>6} {unresolved_refs:>5}{flag}"
            )

    report = build_report(files, counts, detail_files, warnings)
    if args.json:
        print(json.dumps(report, ensure_ascii=False))
        return 0 if warnings == 0 else 1

    print()
    print(f"Total files: {report['total_files']}, warnings: {report['warnings']}")
    ordered = ", ".join(f"{name}={counts[name]}" for name in sorted(counts))
    if ordered:
        print(f"Warning breakdown: {ordered}")
    else:
        print("Warning breakdown: (none)")
    print(
        "Warning breakdown JSON: "
        + json.dumps(report["counts"], ensure_ascii=False)
    )
    print(
        "Warning files JSON: "
        + json.dumps(report["files"], ensure_ascii=False)
    )
    return 0 if warnings == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
