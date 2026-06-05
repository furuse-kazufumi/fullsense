#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""zenn_convert.py — FullSense の Qiita 形式記事を Zenn.dev (zenn-cli) 形式へ変換する。

設計方針 (project_zenn_publication_strategy.md / Phase 1):
  - GitHub repo (fullsense) を single source of truth とし、`docs/articles/` の
    既存記事を **読み取り専用** で変換する (実記事は一切編集しない)。
  - 依存ゼロ (stdlib のみ)。frontmatter は軽量パーサで処理する (PyYAML 不要)。
  - 出力は `zenn/` 配下に隔離 (`zenn/articles/<slug>.md` / `zenn/books/<book>/`).
  - 多言語記事 (# 日本語 / # English / # 中文 / # 한국어) のうち **ja セクションのみ**
    を抽出する (Zenn は日本語プラットフォームのため)。
  - 画像は raw.githubusercontent 絶対 URL をそのまま維持 (相対パス禁止)。
  - `published: false` 固定 (実投稿はユーザー判断)。
  - Zenn は canonical_url 非対応 → 本文冒頭に元記事 (GitHub) へのリンク注記を挿入。
  - 公開出力に D ドライブ等のローカルパスを一切含めない (scrub_local_paths で検査)。

使い方:
  py -3.11 zenn_convert.py article <md...>     # 単発記事を articles/ へ変換
  py -3.11 zenn_convert.py book                # 連載 #24 を Book へ変換
  py -3.11 zenn_convert.py all                 # book + 主要単発記事を一括変換
  py -3.11 zenn_convert.py article <md> --dry-run   # 出力を書かず内容を表示

ネットワーク投稿 (zenn-cli deploy 等) は一切行わない。変換のみ。
"""
from __future__ import annotations

import argparse
import io
import re
import sys
from pathlib import Path
from typing import Iterable, Optional


# ──────────────────────────────────────────────────────────────────────────
# UTF-8 stdout (Windows cp932 対策) — feedback_cli_utf8_stdout_pattern
# ──────────────────────────────────────────────────────────────────────────

def _ensure_utf8_stdout() -> None:
    """Windows cp932 console で日本語/em-dash/絵文字が化けないよう UTF-8 へ再設定。"""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is None:
            continue
        try:
            stream.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except (AttributeError, ValueError):
            try:
                setattr(
                    sys,
                    stream_name,
                    io.TextIOWrapper(stream.buffer, encoding="utf-8", newline=""),
                )
            except (AttributeError, ValueError):
                pass


# ──────────────────────────────────────────────────────────────────────────
# Paths & constants
# ──────────────────────────────────────────────────────────────────────────

# repo root = scripts/publish/zenn_convert.py から 2 つ上
REPO_ROOT = Path(__file__).resolve().parents[2]
ARTICLES_DIR = REPO_ROOT / "docs" / "articles"
ZENN_DIR = REPO_ROOT / "zenn"
ZENN_ARTICLES_DIR = ZENN_DIR / "articles"
ZENN_BOOKS_DIR = ZENN_DIR / "books"

# 連載 #24 を載せる Book。
BOOK_SLUG = "llive-complete-guide"
BOOK_TITLE = "llive 完全解説 — 認知 OS を構成する技術を名称ごとに解く 9 章"

# GitHub raw / blob ベース URL (記事の出自リンク + 画像 URL に使用)
GITHUB_BLOB_BASE = (
    "https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles"
)

# Zenn slug 制約: a-z0-9 と '-' '_'、12〜50 文字。
ZENN_SLUG_RE = re.compile(r"^[a-z0-9_-]{12,50}$")

# Zenn topics 制約: 英字は小文字、記号は基本不可 (日本語は可)。
# 既存 Qiita タグ → Zenn topic の対応表。表に無いものは sanitize_topic で処理。
TOPIC_MAP = {
    "FullSense": "fullsense",
    "llive": "llive",
    "llmesh": "llmesh",
    "llove": "llove",
    "llcore": "llcore",
    "lldarwin": "lldarwin",
    "解説": "解説",
    "進化計算": "進化計算",
    "形式手法": "形式手法",
    "honest_disclosure": "honestdisclosure",
    "HonestDisclosure": "honestdisclosure",
    "Mamba": "mamba",
    "RWKV": "rwkv",
    "Rust": "rust",
    "pyo3": "pyo3",
    "evolutionary": "evolutionary",
    "AI": "ai",
    "機械学習": "機械学習",
    "Python": "python",
    "LLM": "llm",
}

# Book の章ごとの emoji (project_zenn_publication_strategy: 🧬 進化 / 🧠 記憶 /
# ⚖ governance / 🔬 eval で統一感)。
BOOK_CHAPTER_EMOJI = {
    "00": "📖",  # index
    "01": "🧠",  # memory layer
    "02": "🧠",  # 思考因子 + COG-MESH
    "03": "🧬",  # 構造進化 TRIZ
    "04": "🧬",  # 収束型最適化
    "05": "🧬",  # 進化型最適化
    "06": "🔬",  # LLM backend
    "07": "⚖",  # observability + governance
    "08": "🔬",  # lleval
}
BOOK_COVER_EMOJI = "🧬"

# 単発記事 emoji の既定 (タイトル / topic から推定できない場合)。
DEFAULT_ARTICLE_EMOJI = "🧬"


# ──────────────────────────────────────────────────────────────────────────
# Frontmatter parsing (軽量・PyYAML 不要)
# ──────────────────────────────────────────────────────────────────────────

def split_frontmatter(text: str) -> tuple[list[str], str]:
    """先頭の `---\\n ... \\n---` を (frontmatter_lines, body) に分割する。

    frontmatter が無ければ ([], text) を返す。先頭 BOM を許容。
    """
    if text.startswith("﻿"):
        text = text.lstrip("﻿")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return [], text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            fm = lines[1:i]
            # body は元改行を保つため splitlines ではなく原文から切り出す
            # (画像 URL や SVG が改行 sensitive なケースに備える)
            joined_head = "\n".join(lines[: i + 1])
            body = text[len(joined_head):]
            return fm, body.lstrip("\n")
    return [], text


def parse_frontmatter(fm_lines: list[str]) -> dict:
    """軽量 YAML パーサ。スカラー値・block-sequence (- item)・inline list ([a, b]) に対応。

    Qiita / FullSense 記事で使われる範囲のみを対象とし、ネストは扱わない。
    """
    meta: dict = {}
    i = 0
    n = len(fm_lines)
    while i < n:
        raw = fm_lines[i]
        line = raw.rstrip()
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^([A-Za-z_][\w]*):\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, val = m.group(1), m.group(2).strip()

        # inline list:  tags: [a, b, c]
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            items = [
                _strip_quotes(s.strip())
                for s in _split_inline_list(inner)
                if s.strip()
            ]
            meta[key] = items
            i += 1
            continue

        # block sequence:  tags:\n  - a\n  - b
        if val == "":
            seq: list[str] = []
            j = i + 1
            while j < n:
                item = re.match(r"^\s+-\s+(.*)$", fm_lines[j])
                if not item:
                    break
                seq.append(_strip_quotes(item.group(1).strip()))
                j += 1
            if seq:
                meta[key] = seq
                i = j
                continue
            # 空値スカラー
            meta[key] = ""
            i += 1
            continue

        # scalar
        meta[key] = _strip_quotes(val)
        i += 1
    return meta


def _split_inline_list(inner: str) -> list[str]:
    """inline list の中身をカンマで分割 (簡易; quote 内カンマは想定しない)。"""
    return inner.split(",")


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1]
    return s


# ──────────────────────────────────────────────────────────────────────────
# 言語セクション抽出 (ja のみ)
# ──────────────────────────────────────────────────────────────────────────

_LANG_MARKERS = {
    "ja": re.compile(r"^#{1,3}\s+日本語\s*$", re.MULTILINE),
    "en": re.compile(r"^#{1,3}\s+English\b", re.MULTILINE | re.IGNORECASE),
    "zh": re.compile(r"^#{1,3}\s+中文\s*$", re.MULTILINE),
    "ko": re.compile(r"^#{1,3}\s+한국어\s*$", re.MULTILINE),
}


def extract_ja_section(body: str) -> str:
    """body から `# 日本語` セクションのみを抽出する。

    多言語マーカーが無い (単一言語記事) 場合は body 全体を返す。
    ja マーカーの直後から、次に現れる他言語マーカー (en/zh/ko) の手前までを返す。
    先頭の言語ナビ行 (言語 / Language / ...) は除去する。
    """
    ja_m = _LANG_MARKERS["ja"].search(body)
    if not ja_m:
        # 単一言語記事: 言語ナビ行だけ落として返す
        return _strip_lang_nav(body).strip()

    content_start = body.index("\n", ja_m.start()) + 1
    end_pos = len(body)
    for lang in ("en", "zh", "ko"):
        om = _LANG_MARKERS[lang].search(body, content_start)
        if om and om.start() < end_pos:
            end_pos = om.start()

    section = body[content_start:end_pos].strip()
    # ja セクション内に残る先頭の区切り '---' を整える
    return section


def _strip_lang_nav(body: str) -> str:
    """先頭付近の「言語 / Language / 语言 / 언어: ...」ナビ行を除去する。"""
    lines = body.splitlines()
    out = []
    for ln in lines:
        if re.match(r"^\s*言語\s*/\s*Language\s*/", ln):
            continue
        out.append(ln)
    return "\n".join(out)


# ──────────────────────────────────────────────────────────────────────────
# slug 生成 (Zenn 制約: 12-50 文字, a-z0-9_-)
# ──────────────────────────────────────────────────────────────────────────

def make_slug(source_filename: str, *, hint: Optional[str] = None) -> str:
    """ファイル名 (QIITA_#NN_*.md) から Zenn slug を生成する。

    例: 'QIITA_#22_transformer_escape_status.md' -> 'fs-22-transformer-escape-status'

    制約: a-z0-9_-、12〜50 文字。短ければ padding、長ければ truncate する。
    """
    stem = Path(source_filename).stem
    # 'QIITA_#22_transformer_escape_status' -> 番号と残りを抽出
    base = hint if hint else stem
    base = base.lower()
    # 'qiita_#24_05_evolutionary' のような形を 'fs-24-05-evolutionary' に
    base = base.replace("qiita_#", "fs-").replace("qiita_", "fs-")
    base = base.replace("#", "")
    # 非許可文字 -> ハイフン
    base = re.sub(r"[^a-z0-9_-]+", "-", base)
    base = re.sub(r"[-_]{2,}", "-", base)
    base = base.strip("-_")

    if not base.startswith("fs"):
        base = "fs-" + base

    # 50 文字に truncate (末尾ハイフン除去)
    if len(base) > 50:
        base = base[:50].rstrip("-_")
    # 12 文字未満なら padding
    if len(base) < 12:
        base = (base + "-fullsense")[:50]
        base = base.rstrip("-_")
        if len(base) < 12:
            base = (base + "-000000000000")[:12]

    return base


def book_chapter_slug(num: str) -> str:
    """Book 章ファイルの slug (ファイル名先頭の番号)。zenn-cli は 'NN-name' を推奨。"""
    return num  # config.yaml の chapters で章ファイル stem を列挙する


# ──────────────────────────────────────────────────────────────────────────
# topics (≤5) 変換
# ──────────────────────────────────────────────────────────────────────────

def sanitize_topic(tag: str) -> str:
    """Qiita タグ 1 つを Zenn topic へ正規化する (表優先、無ければ機械処理)。"""
    if tag in TOPIC_MAP:
        return TOPIC_MAP[tag]
    t = tag.strip()
    # 日本語 (非 ASCII) を含むなら原則そのまま (Zenn は日本語 topic 可)。
    if any(ord(c) > 0x7F for c in t):
        # ただし空白・記号は除去
        return re.sub(r"[\s/]+", "", t)
    # ASCII: 小文字化し、英数字のみ残す
    t = t.lower()
    t = re.sub(r"[^a-z0-9]+", "", t)
    return t


def build_topics(tags: Iterable[str], *, max_topics: int = 5) -> list[str]:
    """Qiita tags -> Zenn topics (≤5, 重複除去, 空除去)。"""
    out: list[str] = []
    seen: set[str] = set()
    for tag in tags:
        topic = sanitize_topic(tag)
        if not topic or topic in seen:
            continue
        seen.add(topic)
        out.append(topic)
        if len(out) >= max_topics:
            break
    return out


# ──────────────────────────────────────────────────────────────────────────
# emoji 推定
# ──────────────────────────────────────────────────────────────────────────

def infer_article_emoji(title: str, topics: list[str]) -> str:
    """タイトル / topics から記事 emoji を 1 文字推定する。"""
    text = title.lower() + " " + " ".join(topics)
    if any(k in text for k in ("eval", "lleval", "検証", "verifier", "honest")):
        return "🔬"
    if any(k in text for k in ("governance", "approval", "audit", "統治", "審査")):
        return "⚖"
    if any(k in text for k in ("memory", "記憶", "忘れない")):
        return "🧠"
    if any(k in text for k in ("evolution", "進化", "darwin", "genome", "ga", "集団")):
        return "🧬"
    return DEFAULT_ARTICLE_EMOJI


# ──────────────────────────────────────────────────────────────────────────
# 出自リンク注記 (Zenn は canonical_url 非対応 → 本文冒頭で代替)
# ──────────────────────────────────────────────────────────────────────────

def origin_note(source_filename: str) -> str:
    """元記事 (GitHub source of truth) への注記行を生成する。

    Zenn は canonical_url frontmatter を持たないため、cross-post の出自を
    本文冒頭にリンク注記で示す (README にもこの代替策を明記する)。
    """
    # ファイル名の '#' は URL fragment 区切りと衝突するため %23 にエンコードする。
    url = f"{GITHUB_BLOB_BASE}/{source_filename.replace('#', '%23')}"
    return (
        "> この記事は [FullSense リポジトリ]"
        f"({url}) の記事を Zenn 向けに変換したものです "
        "(原本 = GitHub / single source of truth)。\n"
    )


# ──────────────────────────────────────────────────────────────────────────
# Zenn frontmatter 生成
# ──────────────────────────────────────────────────────────────────────────

def build_article_frontmatter(
    *, title: str, emoji: str, topics: list[str], article_type: str = "tech"
) -> str:
    """Zenn article 用 frontmatter を生成する。"""
    topics_yaml = "[" + ", ".join(f'"{t}"' for t in topics) + "]"
    return (
        "---\n"
        f'title: "{_yaml_escape(title)}"\n'
        f'emoji: "{emoji}"\n'
        f'type: "{article_type}"\n'
        f"topics: {topics_yaml}\n"
        "published: false\n"
        "---\n"
    )


def _yaml_escape(s: str) -> str:
    """double-quote YAML スカラー用の最小エスケープ。"""
    return s.replace("\\", "\\\\").replace('"', '\\"')


# ──────────────────────────────────────────────────────────────────────────
# ローカルパス混入検査 (公開資料に D ドライブ等を出さない)
# ──────────────────────────────────────────────────────────────────────────

_LOCAL_PATH_PATTERNS = [
    # C:\ / D:/ など。URL scheme (https:) と誤検出しないよう、ドライブ文字の
    # 直前が英数字でないこと (= 単独のドライブ文字) を要求する。
    re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]"),
    re.compile(r"/Users/[^/\s]+/"),         # macOS home
    re.compile(r"/home/[^/\s]+/"),          # linux home
    re.compile(r"\\\\[^\\]+\\"),            # UNC \\host\
]


def find_local_paths(text: str) -> list[str]:
    """text 中のローカルパスらしき断片を列挙する (空なら混入なし)。"""
    hits: list[str] = []
    for pat in _LOCAL_PATH_PATTERNS:
        for m in pat.finditer(text):
            # 行ごと拾って文脈を残す
            line_start = text.rfind("\n", 0, m.start()) + 1
            line_end = text.find("\n", m.end())
            if line_end == -1:
                line_end = len(text)
            hits.append(text[line_start:line_end].strip())
    return hits


def scrub_check(text: str, label: str) -> None:
    """ローカルパス混入を検査し、見つかれば stderr に警告する (出力は止めない)。"""
    hits = find_local_paths(text)
    if hits:
        print(
            f"[warn] {label}: ローカルパスらしき断片を {len(hits)} 件検出 "
            "(公開前に確認してください):",
            file=sys.stderr,
        )
        for h in hits[:5]:
            print(f"        {h}", file=sys.stderr)


# ──────────────────────────────────────────────────────────────────────────
# 記事変換 (single article)
# ──────────────────────────────────────────────────────────────────────────

def convert_article_text(
    raw_text: str, source_filename: str, *, article_type: str = "tech"
) -> tuple[str, dict]:
    """Qiita 記事テキスト -> Zenn article テキスト (frontmatter + body) を返す。

    戻り値: (zenn_markdown, info)  info = {slug, title, emoji, topics}
    """
    fm_lines, body = split_frontmatter(raw_text)
    meta = parse_frontmatter(fm_lines)

    title = meta.get("title", Path(source_filename).stem)
    if isinstance(title, list):
        title = title[0] if title else Path(source_filename).stem

    raw_tags = meta.get("tags", [])
    if isinstance(raw_tags, str):
        raw_tags = [raw_tags] if raw_tags else []
    topics = build_topics(raw_tags)
    if not topics:
        topics = ["fullsense"]

    emoji = infer_article_emoji(str(title), topics)
    slug = make_slug(source_filename)

    ja_body = extract_ja_section(body)

    note = origin_note(source_filename)
    front = build_article_frontmatter(
        title=str(title), emoji=emoji, topics=topics, article_type=article_type
    )

    zenn_md = front + "\n" + note + "\n" + ja_body.rstrip() + "\n"

    info = {
        "slug": slug,
        "title": str(title),
        "emoji": emoji,
        "topics": topics,
        "source": source_filename,
    }
    return zenn_md, info


# ──────────────────────────────────────────────────────────────────────────
# Book 変換 (連載 #24 → llive-complete-guide)
# ──────────────────────────────────────────────────────────────────────────

# 連載 #24 章ファイル (実在を find_book_chapters で確認する)。
_BOOK_CHAPTER_SPEC = [
    ("00", "QIITA_#24_00_llive_tech_series_index.md"),
    ("01", "QIITA_#24_01_memory_layer.md"),
    ("02", "QIITA_#24_02_thought_factors_cog_mesh.md"),
    ("03", "QIITA_#24_03_structural_evolution_triz.md"),
    ("04", "QIITA_#24_04_convergent_optimization_b_series.md"),
    ("05", "QIITA_#24_05_evolutionary_v0BCDE.md"),
    ("06", "QIITA_#24_06_llm_backend_non_transformer.md"),
    ("07", "QIITA_#24_07_observability_governance.md"),
    ("08", "QIITA_#24_08_lleval_eval_framework.md"),
]


def find_book_chapters(articles_dir: Path) -> list[tuple[str, Path]]:
    """連載 #24 の章ファイルを解決する。実在するもののみ (num, path) で返す。"""
    found: list[tuple[str, Path]] = []
    for num, fname in _BOOK_CHAPTER_SPEC:
        p = articles_dir / fname
        if p.exists():
            found.append((num, p))
    return found


def build_book_config(chapters: list[tuple[str, str]]) -> str:
    """Book config.yaml を生成する。

    chapters: [(章ファイル stem, 表示タイトル), ...] (順序が章順)。
    手書き YAML (PyYAML 不要)。
    """
    lines = [
        f'title: "{_yaml_escape(BOOK_TITLE)}"',
        f'summary: "FullSense の認知 OS llive を 9 章 (index + 8 大分類) で解説する Book。'
        f' 認知 / 最適化 / 実行 / 横断の 4 層を、具体的な class / function 名まで降りて解く。"',
        "topics: [\"llive\", \"fullsense\", \"進化計算\", \"llm\", \"解説\"]",
        f'published: false',
        f'price: 0',
        "chapters:",
    ]
    for stem, _title in chapters:
        lines.append(f"  - {stem}")
    return "\n".join(lines) + "\n"


def build_book_chapter(
    raw_text: str, num: str, source_filename: str
) -> tuple[str, str, str]:
    """Book 章ファイル 1 つを生成する。

    戻り値: (chapter_stem, chapter_markdown, title)
    Zenn Book 章 frontmatter は title のみ必須 (emoji/type/topics は book 側)。
    """
    fm_lines, body = split_frontmatter(raw_text)
    meta = parse_frontmatter(fm_lines)
    title = meta.get("title", f"第 {num} 章")
    if isinstance(title, list):
        title = title[0] if title else f"第 {num} 章"

    ja_body = extract_ja_section(body)
    note = origin_note(source_filename)

    # 章ファイル stem: '00-index' のように番号 + 短い英語名。
    short = _chapter_short_name(source_filename)
    stem = f"{num}-{short}"

    front = (
        "---\n"
        f'title: "{_yaml_escape(str(title))}"\n'
        "---\n"
    )
    chapter_md = front + "\n" + note + "\n" + ja_body.rstrip() + "\n"
    return stem, chapter_md, str(title)


def _chapter_short_name(source_filename: str) -> str:
    """'QIITA_#24_01_memory_layer.md' -> 'memory-layer' (英語短縮名)。"""
    stem = Path(source_filename).stem
    # '#24_NN_' を除去
    m = re.match(r"^QIITA_#\d+_\d+_(.*)$", stem)
    rest = m.group(1) if m else stem
    rest = rest.lower().replace("_", "-")
    rest = re.sub(r"[^a-z0-9-]+", "-", rest).strip("-")
    return rest or "chapter"


# ──────────────────────────────────────────────────────────────────────────
# I/O: 出力書き込み
# ──────────────────────────────────────────────────────────────────────────

def write_output(path: Path, content: str, *, dry_run: bool) -> None:
    scrub_check(content, str(path.name))
    if dry_run:
        print(f"[dry-run] would write {path} ({len(content)} chars)")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[ok] wrote {path} ({len(content)} chars)")


# ──────────────────────────────────────────────────────────────────────────
# Sub-commands
# ──────────────────────────────────────────────────────────────────────────

def cmd_article(md_paths: list[Path], *, dry_run: bool) -> int:
    rc = 0
    for md in md_paths:
        if md.suffix == ".lnk":
            print(f"[skip] {md.name}: Windows shortcut (.lnk)", file=sys.stderr)
            continue
        if not md.exists():
            print(f"[error] not found: {md}", file=sys.stderr)
            rc = 1
            continue
        raw = md.read_text(encoding="utf-8")
        zenn_md, info = convert_article_text(raw, md.name)
        out = ZENN_ARTICLES_DIR / f"{info['slug']}.md"
        if not ZENN_SLUG_RE.match(info["slug"]):
            print(
                f"[error] slug 制約違反: {info['slug']} (12-50, a-z0-9_-)",
                file=sys.stderr,
            )
            rc = 1
            continue
        write_output(out, zenn_md, dry_run=dry_run)
        print(
            f"       title='{info['title'][:50]}' emoji={info['emoji']} "
            f"topics={info['topics']}"
        )
    return rc


def cmd_book(*, dry_run: bool) -> int:
    chapters = find_book_chapters(ARTICLES_DIR)
    if not chapters:
        print("[error] 連載 #24 章ファイルが見つかりません。", file=sys.stderr)
        return 1
    if len(chapters) != len(_BOOK_CHAPTER_SPEC):
        print(
            f"[warn] 期待 {len(_BOOK_CHAPTER_SPEC)} 章中 {len(chapters)} 章のみ検出。",
            file=sys.stderr,
        )

    book_dir = ZENN_BOOKS_DIR / BOOK_SLUG
    chapter_meta: list[tuple[str, str]] = []  # (stem, title)
    for num, path in chapters:
        raw = path.read_text(encoding="utf-8")
        stem, chapter_md, title = build_book_chapter(raw, num, path.name)
        write_output(book_dir / f"{stem}.md", chapter_md, dry_run=dry_run)
        chapter_meta.append((stem, title))

    config_yaml = build_book_config(chapter_meta)
    write_output(book_dir / "config.yaml", config_yaml, dry_run=dry_run)
    print(f"[ok] Book '{BOOK_SLUG}': {len(chapter_meta)} 章")
    return 0


# all で変換する代表的な単発記事 (連載 #24 以外)。
_SINGLE_ARTICLES = [
    "QIITA_#22_transformer_escape_status.md",
    "QIITA_#23_15h_marathon_mid_report.md",
    "QIITA_#25_monoculture_evolution_lldarwin.md",
]


def cmd_all(*, dry_run: bool) -> int:
    rc = cmd_book(dry_run=dry_run)
    md_paths = [ARTICLES_DIR / f for f in _SINGLE_ARTICLES]
    rc2 = cmd_article(md_paths, dry_run=dry_run)
    return rc or rc2


# ──────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────

def main(argv: Optional[list[str]] = None) -> int:
    _ensure_utf8_stdout()
    parser = argparse.ArgumentParser(
        description="FullSense Qiita 記事 -> Zenn (zenn-cli) 形式に変換する (変換のみ・投稿しない)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_article = sub.add_parser("article", help="単発記事を articles/ へ変換")
    p_article.add_argument("files", nargs="+", help="変換する Markdown ファイル")
    p_article.add_argument("--dry-run", action="store_true", help="書き込まず内容を表示")

    p_book = sub.add_parser("book", help="連載 #24 を Book へ変換")
    p_book.add_argument("--dry-run", action="store_true", help="書き込まず内容を表示")

    p_all = sub.add_parser("all", help="Book + 主要単発記事を一括変換")
    p_all.add_argument("--dry-run", action="store_true", help="書き込まず内容を表示")

    args = parser.parse_args(argv)

    if args.cmd == "article":
        return cmd_article([Path(f) for f in args.files], dry_run=args.dry_run)
    if args.cmd == "book":
        return cmd_book(dry_run=args.dry_run)
    if args.cmd == "all":
        return cmd_all(dry_run=args.dry_run)
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    sys.exit(main())
