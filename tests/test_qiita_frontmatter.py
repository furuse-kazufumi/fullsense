# SPDX-License-Identifier: Apache-2.0
"""Frontmatter regression tests for Qiita/Zenn helper scripts."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


fm = _load("frontmatter_shared", TOOLS_DIR / "_frontmatter.py")
qpp = _load("qiita_public_post", TOOLS_DIR / "qiita_public_post.py")
qtp = _load("qiita_team_post", TOOLS_DIR / "qiita_team_post.py")
qconv = _load("convert_to_qiita_cli", TOOLS_DIR / "qiita-cli-poc" / "convert_to_qiita_cli.py")
zc = _load("zenn_convert", ROOT / "scripts" / "publish" / "zenn_convert.py")


FOLDED_TEXT = """\
---
title: >-
  AI's first line
  second line

  third paragraph
tags:
  - AI
  - 'AI''s'
---
body
"""

LITERAL_TEXT = """\
---
title: 'AI''s title'
notes: |
  line 1

  line 2
tags:
  - AI
  - 'AI''s'
---
body
"""


def test_shared_split_frontmatter_parses_folded_title():
    meta, body = fm.split_frontmatter(FOLDED_TEXT)
    assert meta["title"] == "AI's first line second line\nthird paragraph"
    assert meta["tags"] == ["AI", "AI's"]
    assert body == "body\n"


def test_shared_parser_restores_single_quote_and_literal_block():
    meta = fm.parse_frontmatter_lines(fm.split_frontmatter_lines(LITERAL_TEXT)[0])
    assert meta["title"] == "AI's title"
    assert meta["notes"] == "line 1\n\nline 2"
    assert meta["tags"] == ["AI", "AI's"]


def test_qiita_posters_parse_folded_title_and_tags():
    for mod in (qpp, qtp):
        meta, body = mod.split_frontmatter(FOLDED_TEXT)
        assert meta["title"] == "AI's first line second line\nthird paragraph"
        assert meta["tags"] == ["AI", "AI's"]
        assert body == "body\n"


def test_convert_to_qiita_cli_parses_folded_title():
    fm_lines, _body = qconv.split_frontmatter(FOLDED_TEXT)
    meta = qconv.parse_frontmatter(fm_lines)
    assert meta["title"] == "AI's first line second line\nthird paragraph"
    assert meta["tags"] == ["AI", "AI's"]


def test_zenn_convert_parses_folded_title():
    fm_lines, _body = zc.split_frontmatter(FOLDED_TEXT)
    meta = zc.parse_frontmatter(fm_lines)
    assert meta["title"] == "AI's first line second line\nthird paragraph"
    assert meta["tags"] == ["AI", "AI's"]
