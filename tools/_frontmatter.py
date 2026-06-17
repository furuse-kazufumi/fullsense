#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal frontmatter parser shared by Qiita/Zenn helper scripts.

Supports the subset used in this repo:
- top-level scalars
- block sequences (`tags:\n  - a`)
- inline lists (`tags: [a, b]`)
- YAML block scalars for title/body metadata (`>-`, `|`)
"""
from __future__ import annotations

import re


_BLOCK_SCALAR_VALUES = {">", ">-", ">+", "|", "|-", "|+"}


def split_frontmatter_lines(text: str) -> tuple[list[str], str]:
    """Split leading `--- ... ---` frontmatter into lines + remaining body."""
    if text.startswith("\ufeff"):
        text = text.lstrip("\ufeff")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = lines[1:i]
            head = "\n".join(lines[: i + 1])
            body = text[len(head):].lstrip("\n")
            return fm, body
    return [], text


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return parsed frontmatter metadata and remaining body."""
    fm_lines, body = split_frontmatter_lines(text)
    return parse_frontmatter_lines(fm_lines), body


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
            meta[key] = [
                _unquote_scalar(part.strip())
                for part in _split_inline_list(val[1:-1].strip())
                if part.strip()
            ]
            i += 1
            continue

        meta[key] = _unquote_scalar(val)
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
