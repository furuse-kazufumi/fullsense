#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal frontmatter/body-title parser shared by Qiita/Zenn helper scripts.

Supports the subset used in this repo:
- top-level scalars
- block sequences (`tags:\n  - a`)
- inline lists (`tags: [a, b]`)
- YAML block scalars for title/body metadata (`>-`, `|`)
"""
from __future__ import annotations

import re


_BLOCK_SCALAR_VALUES = {">", ">-", ">+", "|", "|-", "|+"}
_LANGUAGE_H1S = {"日本語", "English", "中文", "한국어"}


def split_frontmatter_lines(text: str) -> tuple[list[str], str]:
    """Split leading `--- ... ---` frontmatter into lines + remaining body."""
    if text.startswith("\ufeff"):
        text = text[1:]
    lines = text.splitlines(keepends=True)
    if not lines or not re.match(r"^[ \t]*---[ \t]*(?:\r?\n|$)", lines[0]):
        return [], text
    fm_raw: list[str] = []
    for idx in range(1, len(lines)):
        if re.match(r"^[ \t]*---[ \t]*(?:\r?\n|$)", lines[idx]):
            fm_text = "".join(fm_raw)
            fm_lines = fm_text.splitlines()
            if not fm_lines:
                fm_lines = [""]
            body = "".join(lines[idx + 1 :])
            return fm_lines, body
        fm_raw.append(lines[idx])
    return [], text


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return parsed frontmatter metadata and remaining body."""
    fm_lines, body = split_frontmatter_lines(text)
    return parse_frontmatter_lines(fm_lines), body


def resolve_body_title(body: str) -> str | None:
    """Return the publish-title H1 from body text.

    Rules:
    - ignore headings inside fenced code blocks
    - if the first H1 is a language marker (`# 日本語` etc), keep scanning
    - tolerate language nav / prose / anchors before the publish-title H1
    """
    in_fence = False
    fence_marker: str | None = None
    for line in body.splitlines():
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            marker = fence_match.group(1)
            if not in_fence:
                in_fence = True
                fence_marker = marker
            elif fence_marker and marker[:1] == fence_marker[:1] and len(marker) >= len(fence_marker):
                in_fence = False
                fence_marker = None
            continue
        if in_fence:
            continue
        stripped = line.strip()
        if not stripped or stripped.startswith("<!--"):
            continue
        if stripped.startswith("<a ") or stripped.startswith("</a>"):
            continue
        match = re.match(r"^# (.+)$", line)
        if not match:
            continue
        title = match.group(1).strip()
        if title in _LANGUAGE_H1S:
            continue
        return title
    return None


def parse_frontmatter_lines(fm_lines: list[str]) -> dict:
    """Parse the repo's limited frontmatter subset."""
    meta: dict = {}
    i = 0
    n = len(fm_lines)
    while i < n:
        line = fm_lines[i].rstrip()
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][\w]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()

        if val == "":
            seq, j = _consume_block_sequence(fm_lines, i + 1)
            if seq:
                meta[key] = seq
                i = j
                continue
            meta[key] = ""
            i += 1
            continue

        if val in _BLOCK_SCALAR_VALUES:
            meta[key], i = _consume_block_scalar(fm_lines, i, val[0])
            continue

        if val.startswith("[") and val.endswith("]"):
            meta[key] = parse_inline_list_value(val)
            i += 1
            continue

        meta[key] = parse_scalar_value(val)
        i += 1
    return meta


def _consume_block_sequence(lines: list[str], start: int) -> tuple[list[str], int]:
    seq: list[str] = []
    j = start
    while j < len(lines):
        stripped = lines[j].strip()
        if not stripped:
            j += 1
            continue
        m = re.match(r"^\s+-\s+(.*)$", lines[j])
        if not m:
            break
        seq.append(_unquote_scalar(m.group(1).strip()))
        j += 1
    return seq, j


def _consume_block_scalar(lines: list[str], start: int, style: str) -> tuple[str, int]:
    block: list[str] = []
    j = start + 1
    while j < len(lines):
        ln = lines[j]
        if not ln.strip():
            block.append("")
            j += 1
            continue
        if re.match(r"^[ \t]+\S", ln):
            block.append(ln)
            j += 1
            continue
        break

    normalized = _normalize_indented_block(block)
    if style == "|":
        return "\n".join(normalized).strip(), j
    return _fold_block_scalar(normalized).strip(), j


def _normalize_indented_block(lines: list[str]) -> list[str]:
    nonblank = [ln for ln in lines if ln.strip()]
    if not nonblank:
        return []
    min_indent = min(len(ln) - len(ln.lstrip(" \t")) for ln in nonblank)
    out: list[str] = []
    for ln in lines:
        if not ln.strip():
            out.append("")
        else:
            out.append(ln[min_indent:])
    return out


def _fold_block_scalar(lines: list[str]) -> str:
    paras: list[str] = []
    cur: list[str] = []
    for ln in lines:
        if ln == "":
            if cur:
                paras.append(" ".join(cur))
                cur = []
            elif paras:
                paras.append("")
            continue
        cur.append(ln)
    if cur:
        paras.append(" ".join(cur))

    out: list[str] = []
    pending_blank = False
    for para in paras:
        if para == "":
            pending_blank = True
            continue
        if out:
            out.append("\n\n" if pending_blank else "\n")
        out.append(para)
        pending_blank = False
    return "".join(out)


def _split_inline_list(inner: str) -> list[str]:
    return inner.split(",")


def find_quoted_scalar_end(value: str) -> int | None:
    if not value or value[0] not in ("'", '"'):
        return None
    quote = value[0]
    i = 1
    while i < len(value):
        ch = value[i]
        if quote == "'" and ch == "'" and i + 1 < len(value) and value[i + 1] == "'":
            i += 2
            continue
        if quote == '"' and ch == "\\" and i + 1 < len(value):
            i += 2
            continue
        if ch == quote:
            return i
        i += 1
    return None


def strip_unquoted_inline_comment(value: str) -> str:
    comment = re.search(r"\s+#", value)
    if not comment:
        return value.strip()
    return value[: comment.start()].rstrip()


def parse_scalar_value(value: str, *, allow_unquoted_comment: bool = False) -> str:
    value = value.strip()
    if not value:
        return ""
    if value[0] in ("'", '"'):
        end = find_quoted_scalar_end(value)
        if end is not None:
            value = value[: end + 1]
    elif allow_unquoted_comment:
        return strip_unquoted_inline_comment(value)
    return _unquote_scalar(value)


def parse_inline_list_value(value: str) -> list[str]:
    cleaned = strip_unquoted_inline_comment(value).strip()
    if cleaned.startswith("[") and cleaned.endswith("]"):
        cleaned = cleaned[1:-1].strip()
    if not cleaned:
        return []
    items: list[str] = []
    buf: list[str] = []
    in_single = False
    in_double = False
    i = 0
    n = len(cleaned)
    while i < n:
        ch = cleaned[i]
        # Inside a double-quoted item, keep a backslash escape (`\"`, `\\`, ...)
        # verbatim so it does not prematurely toggle in_double. _unquote_scalar
        # decodes the escape later. Without this, `["a\"b", x]` mis-tracks the
        # closing quote and drops the following element.
        if in_double and ch == "\\" and i + 1 < n:
            buf.append(ch)
            buf.append(cleaned[i + 1])
            i += 2
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            buf.append(ch)
            i += 1
            continue
        if ch == '"' and not in_single:
            in_double = not in_double
            buf.append(ch)
            i += 1
            continue
        if ch == "," and not in_single and not in_double:
            item = parse_scalar_value("".join(buf), allow_unquoted_comment=True)
            if item:
                items.append(item)
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    if buf:
        item = parse_scalar_value("".join(buf), allow_unquoted_comment=True)
        if item:
            items.append(item)
    return items


def _unquote_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        inner = value[1:-1]
        if value[0] == "'":
            return inner.replace("''", "'")
        return (
            inner.replace("\\\\", "\\")
            .replace('\\"', '"')
            .replace("\\n", "\n")
            .replace("\\r", "\r")
            .replace("\\t", "\t")
        )
    return value
