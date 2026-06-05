# SPDX-License-Identifier: Apache-2.0
"""zenn_convert.py の unit tests。

frontmatter 変換 / slug 制約 / book config 生成 / ローカルパス混入検査を中心に検証する。
スクリプトはパッケージ外なので importlib で直接ロードする (既存 test 流儀に従う)。
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "publish" / "zenn_convert.py"

spec = importlib.util.spec_from_file_location("zenn_convert", SCRIPT)
assert spec is not None and spec.loader is not None
zc = importlib.util.module_from_spec(spec)
sys.modules["zenn_convert"] = zc
spec.loader.exec_module(zc)


# ===========================================================================
# Fixtures: 代表的な Qiita 記事テキスト
# ===========================================================================

MULTILANG_ARTICLE = """\
---
title: 'llive 完全解説 (1) — 「忘れない LLM」: 4 層メモリ'
tags:
  - FullSense
  - llive
  - 解説
private: false
updated_at: '2026-05-23'
id: 2732122ed0a4c9ace0af
slide: false
ignorePublish: false
---
言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

これは日本語の本文です。

![hero](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/x.svg)

# English

This is the English body. SHOULD NOT appear in Zenn output.

# 中文

中文正文。

# 한국어

한국어 본문.
"""

INLINE_TAGS_ARTICLE = """\
---
title: 'llcore 検証 arc — SMT より SDP が正解だった話'
tags: [FullSense, llcore, 解説, 形式手法, 進化計算]
private: true
id: 6fc86b4732eeec77adb6
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english)

# 日本語

検証の本文。

# English

verification body.
"""

SINGLE_LANG_ARTICLE = """\
---
title: 単一言語記事
tags:
  - llive
  - 進化計算
---
言語 / Language / 语言 / 언어: [日本語](#日本語)

普通の本文。多言語マーカーは無い。
"""


# ===========================================================================
# frontmatter parsing
# ===========================================================================

def test_parse_block_sequence_tags():
    fm, body = zc.split_frontmatter(MULTILANG_ARTICLE)
    meta = zc.parse_frontmatter(fm)
    assert meta["title"] == "llive 完全解説 (1) — 「忘れない LLM」: 4 層メモリ"
    assert meta["tags"] == ["FullSense", "llive", "解説"]
    assert meta["private"] == "false"


def test_parse_inline_list_tags():
    fm, _body = zc.split_frontmatter(INLINE_TAGS_ARTICLE)
    meta = zc.parse_frontmatter(fm)
    assert meta["tags"] == ["FullSense", "llcore", "解説", "形式手法", "進化計算"]


def test_split_frontmatter_no_frontmatter():
    fm, body = zc.split_frontmatter("no frontmatter here\njust text")
    assert fm == []
    assert body == "no frontmatter here\njust text"


# ===========================================================================
# ja section extraction (多言語 -> ja のみ)
# ===========================================================================

def test_extract_ja_section_drops_other_languages():
    _fm, body = zc.split_frontmatter(MULTILANG_ARTICLE)
    ja = zc.extract_ja_section(body)
    assert "これは日本語の本文です" in ja
    assert "English body" not in ja
    assert "中文正文" not in ja
    assert "한국어 본문" not in ja
    # 画像 raw URL は維持される
    assert "raw.githubusercontent.com" in ja


def test_extract_ja_single_language_returns_body():
    _fm, body = zc.split_frontmatter(SINGLE_LANG_ARTICLE)
    ja = zc.extract_ja_section(body)
    assert "普通の本文" in ja
    # 言語ナビ行は除去
    assert "言語 / Language" not in ja


# ===========================================================================
# slug 制約 (12-50 文字, a-z0-9_-)
# ===========================================================================

@pytest.mark.parametrize(
    "filename",
    [
        "QIITA_#22_transformer_escape_status.md",
        "QIITA_#24_05_evolutionary_v0BCDE.md",
        "QIITA_#35_00_verifier_sdp_not_smt_index.md",
        "QIITA_#9_x.md",  # 短い → padding される
    ],
)
def test_make_slug_satisfies_zenn_constraints(filename):
    slug = zc.make_slug(filename)
    assert zc.ZENN_SLUG_RE.match(slug), f"slug 制約違反: {slug!r}"
    assert 12 <= len(slug) <= 50


def test_make_slug_lowercases_and_strips_hash():
    slug = zc.make_slug("QIITA_#22_Transformer_Escape.md")
    assert "#" not in slug
    assert slug == slug.lower()
    assert slug.startswith("fs-")


# ===========================================================================
# topics 変換 (≤5, 正規化)
# ===========================================================================

def test_build_topics_maps_and_caps_at_five():
    tags = ["FullSense", "llcore", "解説", "形式手法", "進化計算", "extra"]
    topics = zc.build_topics(tags)
    assert len(topics) <= 5
    assert "fullsense" in topics
    assert "解説" in topics  # 日本語 topic は維持


def test_sanitize_topic_lowercases_ascii_and_strips_symbols():
    assert zc.sanitize_topic("RWKV") == "rwkv"
    assert zc.sanitize_topic("honest_disclosure") == "honestdisclosure"


# ===========================================================================
# article frontmatter 生成
# ===========================================================================

def test_convert_article_produces_zenn_frontmatter():
    zenn_md, info = zc.convert_article_text(
        MULTILANG_ARTICLE, "QIITA_#24_01_memory_layer.md"
    )
    assert zenn_md.startswith("---\n")
    assert 'type: "tech"' in zenn_md
    assert "published: false" in zenn_md
    assert info["emoji"] in ("🧠", "🧬", "⚖", "🔬")
    # topics は ≤5 行で 1 行に列挙
    assert "topics:" in zenn_md
    # canonical 非対応の代替 = 出自リンク注記
    assert "single source of truth" in zenn_md
    assert "github.com/furuse-kazufumi/fullsense" in zenn_md


def test_convert_article_published_is_false_always():
    zenn_md, _ = zc.convert_article_text(INLINE_TAGS_ARTICLE, "QIITA_#35_00_x.md")
    assert "published: false" in zenn_md
    assert "published: true" not in zenn_md


# ===========================================================================
# book config 生成
# ===========================================================================

def test_build_book_config_lists_chapters_and_unpublished():
    chapters = [("00-index", "索引"), ("01-memory", "メモリ層")]
    cfg = zc.build_book_config(chapters)
    assert "published: false" in cfg
    assert "chapters:" in cfg
    assert "- 00-index" in cfg
    assert "- 01-memory" in cfg
    assert "price: 0" in cfg


def test_build_book_chapter_frontmatter_has_title_only():
    stem, chapter_md, title = zc.build_book_chapter(
        MULTILANG_ARTICLE, "01", "QIITA_#24_01_memory_layer.md"
    )
    assert stem == "01-memory-layer"
    assert chapter_md.startswith("---\n")
    assert "title:" in chapter_md
    # 章 frontmatter には emoji/type/topics を入れない (book 側が持つ)
    assert "emoji:" not in chapter_md.split("---\n")[1]
    assert "これは日本語の本文です" in chapter_md


# ===========================================================================
# ローカルパス混入検査
# ===========================================================================

def test_find_local_paths_detects_windows_drive():
    text = "see D:\\projects\\fullsense\\foo.md for details"
    hits = zc.find_local_paths(text)
    assert hits, "D:\\ パスを検出できていない"


def test_find_local_paths_detects_unix_home():
    assert zc.find_local_paths("/home/puruy/secret")
    assert zc.find_local_paths("/Users/puruy/secret")


def test_converted_article_has_no_local_paths():
    """変換出力 (raw URL のみの記事) にローカルパスが混入しないこと。"""
    zenn_md, _ = zc.convert_article_text(
        MULTILANG_ARTICLE, "QIITA_#24_01_memory_layer.md"
    )
    assert zc.find_local_paths(zenn_md) == []
