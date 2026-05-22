# SPDX-License-Identifier: Apache-2.0
"""qiita_url_sync.py の unit tests."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "qiita_url_sync.py"

# Load qiita_url_sync.py as a module (not a package member)
spec = importlib.util.spec_from_file_location("qiita_url_sync", SCRIPT)
assert spec is not None and spec.loader is not None
qus = importlib.util.module_from_spec(spec)
sys.modules["qiita_url_sync"] = qus
spec.loader.exec_module(qus)


# ===========================================================================
# parse_link_map
# ===========================================================================


def test_parse_link_map_finds_posted_articles(monkeypatch, tmp_path):
    fake_map = tmp_path / "LINK_MAP.md"
    fake_map.write_text(
        "# header\n\n"
        "## URL mapping table\n\n"
        "| ID | ファイル | Qiita URL | 投稿日 |\n"
        "|---|---|---|---|\n"
        "| #14 | QIITA_#14_foo.md | <https://qiita.com/x/items/aaa> | 2026-05-22 |\n"
        "| #15 | QIITA_#15_bar.md | _未投稿_ | — |\n"
        "| #24-05 | QIITA_#24_05_baz.md | <https://qiita.com/x/items/bbb> | 2026-05-22 |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qus, "LINK_MAP", fake_map)

    posted = qus.parse_link_map()

    assert "14" in posted
    assert "24-05" in posted
    assert "15" not in posted  # _未投稿_ は skip
    assert posted["14"]["url"] == "https://qiita.com/x/items/aaa"
    assert posted["24-05"]["fname"] == "QIITA_#24_05_baz.md"


def test_parse_link_map_empty_when_no_posted(monkeypatch, tmp_path):
    fake_map = tmp_path / "LINK_MAP.md"
    fake_map.write_text(
        "| ID | ファイル | URL | 日 |\n"
        "|---|---|---|---|\n"
        "| #14 | QIITA_#14_foo.md | _未投稿_ | — |\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qus, "LINK_MAP", fake_map)
    assert qus.parse_link_map() == {}


# ===========================================================================
# replace_in_text — Rule 1: ``QIITA_#NN_*` (内部参照)``
# ===========================================================================


def test_replace_rule1_basic_internal_reference():
    posted = {
        "14": {
            "fname": "QIITA_#14_foo.md",
            "url": "https://qiita.com/x/items/aaa",
            "date": "2026-05-22",
        }
    }
    text = "詳細は `QIITA_#14_foo.md` (内部参照) を参照."
    new_text, changes = qus.replace_in_text(text, posted)

    assert len(changes) == 1
    assert "https://qiita.com/x/items/aaa" in new_text
    assert "QIITA_#14_foo.md](https://qiita.com" in new_text


def test_replace_rule1_unposted_article_kept_as_is():
    posted = {"14": {"fname": "QIITA_#14_foo.md", "url": "https://x/a", "date": "x"}}
    text = "未投稿: `QIITA_#99_unposted.md` (内部参照)"
    new_text, changes = qus.replace_in_text(text, posted)

    # 未投稿は据置, changes ゼロ
    assert changes == []
    assert "QIITA_#99_unposted.md" in new_text


def test_replace_rule1_with_24_sub_number():
    """#24-05 形式 (`QIITA_#24_05_*.md` (内部参照)) も置換される."""
    posted = {
        "24-05": {
            "fname": "QIITA_#24_05_evo.md",
            "url": "https://qiita.com/x/items/zzz",
            "date": "2026-05-22",
        }
    }
    text = "次に `QIITA_#24_05_evo.md` (内部参照) で詳述する."
    new_text, changes = qus.replace_in_text(text, posted)

    assert len(changes) == 1
    assert "https://qiita.com/x/items/zzz" in new_text


def test_replace_rule1_multiple_references_in_one_text():
    posted = {
        "14": {"fname": "QIITA_#14_a.md", "url": "https://x/a", "date": "d"},
        "15": {"fname": "QIITA_#15_b.md", "url": "https://x/b", "date": "d"},
    }
    text = (
        "両方参照: `QIITA_#14_a.md` (内部参照) と `QIITA_#15_b.md` (内部参照)."
    )
    new_text, changes = qus.replace_in_text(text, posted)
    assert len(changes) == 2
    assert "https://x/a" in new_text
    assert "https://x/b" in new_text


# ===========================================================================
# replace_in_text — Rule 2 (aggressive): `#NN-XX` 単独表記
# ===========================================================================


def test_replace_rule2_aggressive_off_by_default():
    """aggressive=False では #NN-XX 単独表記は置換されない."""
    posted = {
        "24-05": {"fname": "f.md", "url": "https://x/a", "date": "d"},
    }
    text = "詳細は #24-05 で."
    new_text, changes = qus.replace_in_text(text, posted, aggressive=False)
    assert changes == []
    assert new_text == text


def test_replace_rule2_aggressive_on_converts_bare_reference():
    """aggressive=True なら #24-05 単独表記も link 化."""
    posted = {
        "24-05": {"fname": "f.md", "url": "https://x/a", "date": "d"},
    }
    text = "詳細は #24-05 で."
    new_text, changes = qus.replace_in_text(text, posted, aggressive=True)
    assert len(changes) == 1
    assert "[#24-05](https://x/a)" in new_text


def test_replace_rule2_aggressive_skips_unposted():
    posted: dict[str, dict[str, str]] = {}
    text = "未投稿: #24-99 の話."
    new_text, changes = qus.replace_in_text(text, posted, aggressive=True)
    assert changes == []
    assert new_text == text


# ===========================================================================
# integration: empty posted
# ===========================================================================


def test_replace_empty_posted_returns_unchanged():
    text = "test `QIITA_#14_foo.md` (内部参照) text"
    new_text, changes = qus.replace_in_text(text, {})
    assert changes == []
    assert new_text == text
