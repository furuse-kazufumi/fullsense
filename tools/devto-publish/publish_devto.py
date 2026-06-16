#!/usr/bin/env python3
"""
publish_devto.py — dev.to (DEV Community) 自動投稿スクリプト
===================================================================
Usage:
    py -3.11 publish_devto.py <markdown_file> [options]

Options:
    --published          公開状態で投稿 (デフォルト: draft)
    --dry-run            実際に POST せず payload を表示
    --tags TAG,...       タグ上書き (最大4個)
    --title-override     タイトル上書き
    --lang LANG          抽出言語セクション (english/japanese/chinese/korean, デフォルト: english)
    --series SERIES      連載名 (dev.to series)

API key の設定:
    D:\\api-keys.json の "devto_api_key" に設定 or 環境変数 DEVTO_API_KEY

冪等性:
    初回投稿後、同ディレクトリに <markdown_stem>.devto.json が生成されます。
    次回実行時にこのファイルが存在すれば PUT (更新) になります。
"""

import sys
import os
import json
import re
import argparse
import urllib.request
import urllib.error
import textwrap
from pathlib import Path
from typing import Optional


# ────────────────────────────────────────────────
# UTF-8 stdout (Windows cp932 対策)
# ────────────────────────────────────────────────

def _ensure_utf8_stdout() -> None:
    """Windows の cp932 コンソールで日本語・絵文字が文字化けしないよう UTF-8 に統一する。"""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


# ────────────────────────────────────────────────
# Constants
# ────────────────────────────────────────────────

DEVTO_API_BASE = "https://dev.to/api"
API_KEYS_PATH = Path(r"D:\api-keys.json")

# セクション見出しのパターン (# English / ## English / # 英語 等)
_SECTION_PATTERNS = {
    "english": re.compile(r"^#{1,3}\s+English\b", re.IGNORECASE | re.MULTILINE),
    "japanese": re.compile(r"^#{1,3}\s+日本語\b", re.MULTILINE),
    "chinese": re.compile(r"^#{1,3}\s+中文\b", re.MULTILINE),
    "korean": re.compile(r"^#{1,3}\s+한국어\b", re.MULTILINE),
}

# dev.to タグに使えない文字 (英数字・ハイフンのみ許可)
_TAG_SANITIZE = re.compile(r"[^a-zA-Z0-9\-]")


# ────────────────────────────────────────────────
# API key resolution
# ────────────────────────────────────────────────

def load_api_key() -> Optional[str]:
    """
    優先順位:
      1. 環境変数 DEVTO_API_KEY
      2. D:\\api-keys.json の "devto_api_key"
    キーが存在しない場合は None を返す (値は絶対にログ出力しない)。
    """
    env_key = os.environ.get("DEVTO_API_KEY", "").strip()
    if env_key:
        return env_key

    if API_KEYS_PATH.exists():
        try:
            data = json.loads(API_KEYS_PATH.read_text(encoding="utf-8"))
            key = data.get("devto_api_key", "").strip()
            if key:
                return key
        except (json.JSONDecodeError, OSError) as e:
            print(f"[warn] {API_KEYS_PATH} の読み込みに失敗: {e}", file=sys.stderr)

    return None


# ────────────────────────────────────────────────
# Frontmatter parsing
# ────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    YAML frontmatter (---...---) を解析して (meta_dict, body_text) を返す。
    pyyaml 不要 — 必要最低限のキーのみ正規表現で抽出する。
    """
    meta: dict = {}
    body = text

    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if not fm_match:
        return meta, body

    fm_text = fm_match.group(1)
    body = text[fm_match.end():]

    # title — plain / quoted / YAML block scalar (`title: >-`, `|`) 対応。
    # 折返しスカラは後続のインデント行を結合し、空なら本文の最初の H1 へフォールバックする。
    m = re.search(r"^title:[ \t]*(.*)$", fm_text, re.MULTILINE)
    title = ""
    if m:
        val = m.group(1).strip()
        if val in (">", ">-", ">+", "|", "|-", "|+", ""):
            cont: list[str] = []
            for ln in fm_text[m.end():].splitlines():
                if not ln.strip():
                    if cont:
                        break
                    continue
                if re.match(r"^[ \t]+\S", ln):
                    cont.append(ln.strip())
                else:
                    break
            title = " ".join(cont).strip()
        else:
            title = val.strip("'\"")
    if not title:
        h1 = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = h1.group(1).strip() if h1 else ""
    if title:
        meta["title"] = title

    # tags (list形式 or inline)
    tags_block = re.search(r"^tags:\s*\n((?:\s+-\s+.+\n?)+)", fm_text, re.MULTILINE)
    if tags_block:
        meta["tags"] = re.findall(r"^\s+-\s+(.+)", tags_block.group(1), re.MULTILINE)
    else:
        inline = re.search(r"^tags:\s*\[(.+)\]", fm_text, re.MULTILINE)
        if inline:
            meta["tags"] = [t.strip().strip("'\"") for t in inline.group(1).split(",")]

    # private / ignorePublish
    for key in ("private", "ignorePublish", "slide"):
        m = re.search(rf"^{key}:\s*(true|false)", fm_text, re.MULTILINE | re.IGNORECASE)
        if m:
            meta[key] = m.group(1).lower() == "true"

    # id (Qiita article id — 流用しない、参考情報として保持)
    m = re.search(r"^id:\s*(.+)", fm_text, re.MULTILINE)
    if m:
        raw_id = m.group(1).strip()
        meta["qiita_id"] = None if raw_id == "null" else raw_id

    return meta, body


# ────────────────────────────────────────────────
# Section extraction
# ────────────────────────────────────────────────

def extract_section(body: str, lang: str) -> str:
    """
    body から指定言語セクション (# English etc.) を抽出する。
    見つからない場合は body 全体を返す。

    戦略:
      1. セクションマーカー行 (# English / # 日本語 等) を探す。
      2. マーカー行の直後から始まる本文を取得する。
      3. 終端 = 他の言語セクションマーカー (# 中文 / # 한국어 等) のうち
         最も近いもの。
         → これにより「# English」の直後に「# Rebuilding...」という
           本文タイトルが来るような構造でも正しく全体を取得できる。
    """
    pattern = _SECTION_PATTERNS.get(lang.lower())
    if not pattern:
        print(f"[warn] 未知の言語 '{lang}', 全体を使用します。", file=sys.stderr)
        return body

    m = pattern.search(body)
    if not m:
        print(f"[info] '{lang}' セクションが見つかりません。全体を使用します。", file=sys.stderr)
        return body

    # マーカー行の終端 (改行の次から本文開始)
    marker_end = body.index("\n", m.start()) + 1
    content_start = marker_end

    # 他の言語セクションマーカーを終端として使う
    other_patterns = [p for k, p in _SECTION_PATTERNS.items() if k != lang.lower()]
    end_pos = len(body)
    for other_pat in other_patterns:
        om = other_pat.search(body, content_start)
        if om and om.start() < end_pos:
            end_pos = om.start()

    section_content = body[content_start:end_pos].strip()

    if not section_content:
        print(
            f"[warn] '{lang}' セクション本文が空です。全体を使用します。",
            file=sys.stderr,
        )
        return body

    return section_content


# ────────────────────────────────────────────────
# Tag sanitization for dev.to
# ────────────────────────────────────────────────

def sanitize_tags(raw_tags: list[str], max_tags: int = 4) -> list[str]:
    """
    dev.to のタグ制約:
      - 最大 4 タグ
      - 英数字とハイフンのみ (それ以外は削除 or ハイフン化)
      - 小文字推奨
    日本語タグはローマ字化せず除去 (英語タグを優先)。
    """
    sanitized = []
    for tag in raw_tags:
        # 全角記号・スペースをハイフンに
        t = tag.replace(" ", "-").replace("_", "-")
        t = _TAG_SANITIZE.sub("", t)
        t = t.strip("-").lower()
        if t:
            sanitized.append(t)
    # 重複除去・上限
    seen: set[str] = set()
    result = []
    for t in sanitized:
        if t not in seen:
            seen.add(t)
            result.append(t)
        if len(result) >= max_tags:
            break
    return result


# ────────────────────────────────────────────────
# Sidecar (.devto.json) — 冪等性のための id 保存
# ────────────────────────────────────────────────

def sidecar_path(md_path: Path) -> Path:
    return md_path.with_suffix(".devto.json")


def load_sidecar(md_path: Path) -> Optional[dict]:
    sp = sidecar_path(md_path)
    if sp.exists():
        try:
            return json.loads(sp.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return None
    return None


def save_sidecar(md_path: Path, data: dict) -> None:
    sp = sidecar_path(md_path)
    sp.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[info] サイドカー保存: {sp}")


# ────────────────────────────────────────────────
# dev.to API calls
# ────────────────────────────────────────────────

def _api_request(
    method: str,
    endpoint: str,
    api_key: str,
    payload: dict,
) -> dict:
    """
    urllib で dev.to API を呼び出す。
    エラー時は例外を raise せず、エラー情報を含む dict を返す。
    """
    url = f"{DEVTO_API_BASE}{endpoint}"
    body_bytes = json.dumps({"article": payload}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body_bytes,
        method=method,
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
            "Accept": "application/vnd.forem.api-v1+json",
            # dev.to の WAF は無 UA / urllib デフォルト UA を 403 で弾くため browser 風 UA を付ける。
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode("utf-8")
            err_json = json.loads(err_body)
        except Exception:
            err_json = {"raw": e.reason}
        return {
            "_error": True,
            "status": e.code,
            "detail": err_json,
        }
    except urllib.error.URLError as e:
        return {
            "_error": True,
            "status": 0,
            "detail": f"ネットワークエラー: {e.reason}",
        }


def post_article(api_key: str, payload: dict) -> dict:
    return _api_request("POST", "/articles", api_key, payload)


def update_article(api_key: str, article_id: int, payload: dict) -> dict:
    return _api_request("PUT", f"/articles/{article_id}", api_key, payload)


# ────────────────────────────────────────────────
# Payload builder
# ────────────────────────────────────────────────

def build_payload(
    meta: dict,
    body_markdown: str,
    *,
    published: bool = False,
    tags_override: Optional[list[str]] = None,
    title_override: Optional[str] = None,
    series: Optional[str] = None,
    canonical_url: Optional[str] = None,
) -> dict:
    """dev.to POST /api/articles の payload を構築する。"""
    title = title_override or meta.get("title", "Untitled")

    raw_tags = tags_override if tags_override else meta.get("tags", [])
    tags = sanitize_tags(raw_tags)

    payload: dict = {
        "title": title,
        "body_markdown": body_markdown,
        "published": published,
        "tags": tags,
    }
    if series:
        payload["series"] = series
    if canonical_url:
        payload["canonical_url"] = canonical_url

    return payload


# ────────────────────────────────────────────────
# Dry-run display
# ────────────────────────────────────────────────

def display_dry_run(payload: dict, sidecar: Optional[dict] = None) -> None:
    """dry-run 時に送信予定の payload サマリを表示する。"""
    print("=" * 60)
    print("[DRY-RUN] 送信予定の payload:")
    print("=" * 60)
    print(f"  title      : {payload['title']}")
    print(f"  published  : {payload['published']}")
    print(f"  tags       : {payload['tags']}")

    if sidecar and sidecar.get("id"):
        print(f"  操作       : PUT (更新) id={sidecar['id']}")
    else:
        print(f"  操作       : POST (新規)")

    body_preview = payload["body_markdown"][:500].replace("\n", " ")
    print(f"  body_markdown (先頭500文字):")
    for chunk in textwrap.wrap(body_preview, width=70, subsequent_indent="    "):
        print(f"    {chunk}")
    print(f"  body_markdown 全長: {len(payload['body_markdown'])} 文字")
    print("=" * 60)
    print("[DRY-RUN] 実際には POST/PUT しません。--published / 引数から --dry-run を外すと送信します。")


# ────────────────────────────────────────────────
# Main
# ────────────────────────────────────────────────

def main() -> int:
    _ensure_utf8_stdout()

    parser = argparse.ArgumentParser(
        description="dev.to (DEV Community) へ Markdown 記事を自動投稿する",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("markdown_file", help="投稿する Markdown ファイルのパス")
    parser.add_argument(
        "--published",
        action="store_true",
        default=False,
        help="公開状態で投稿 (デフォルト: draft)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=False,
        help="実際に POST せず payload を表示",
    )
    parser.add_argument(
        "--tags",
        default="",
        help="タグをカンマ区切りで指定 (例: python,ai,llm) — 最大4個",
    )
    parser.add_argument("--title-override", default="", help="タイトルを上書き")
    parser.add_argument(
        "--lang",
        default="english",
        choices=["english", "japanese", "chinese", "korean"],
        help="抽出する言語セクション (デフォルト: english)",
    )
    parser.add_argument("--series", default="", help="dev.to の連載 (Series) 名")
    parser.add_argument("--canonical-url", default="", help="canonical URL (元記事 URL)")

    args = parser.parse_args()

    # ── ファイル読み込み ──────────────────────────
    md_path = Path(args.markdown_file)
    if not md_path.exists():
        print(f"[error] ファイルが見つかりません: {md_path}", file=sys.stderr)
        return 1

    text = md_path.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)

    # ── 言語セクション抽出 ────────────────────────
    body_markdown = extract_section(body, args.lang)

    # ── payload 構築 ──────────────────────────────
    tags_override = [t.strip() for t in args.tags.split(",") if t.strip()] or None
    payload = build_payload(
        meta,
        body_markdown,
        published=args.published,
        tags_override=tags_override,
        title_override=args.title_override or None,
        series=args.series or None,
        canonical_url=args.canonical_url or None,
    )

    # ── サイドカー (既存記事 id) ──────────────────
    sidecar = load_sidecar(md_path)

    # ── API key 解決 ──────────────────────────────
    api_key = load_api_key()

    if not api_key:
        print(
            "\n[warn] dev.to API token が設定されていません。dry-run モードに自動フォールバックします。",
            file=sys.stderr,
        )
        print(
            "       token を設定するには:\n"
            "         1. https://dev.to/settings/extensions を開く\n"
            "         2. 'DEV Community API Keys' > 'Generate API Key'\n"
            "         3. 発行したキーを D:\\api-keys.json に追記:\n"
            '            { "devto_api_key": "<YOUR_KEY>" }\n'
            "         4. または環境変数 DEVTO_API_KEY に設定\n",
            file=sys.stderr,
        )
        display_dry_run(payload, sidecar)
        return 0  # dry-run は正常終了

    if args.dry_run:
        display_dry_run(payload, sidecar)
        return 0

    # ── 実際に POST / PUT ─────────────────────────
    if sidecar and sidecar.get("id"):
        article_id = sidecar["id"]
        print(f"[info] 既存記事を更新します (id={article_id}) ...")
        result = update_article(api_key, article_id, payload)
        operation = "PUT"
    else:
        print("[info] 新規記事を投稿します ...")
        result = post_article(api_key, payload)
        operation = "POST"

    # ── レスポンス処理 ────────────────────────────
    if result.get("_error"):
        status = result.get("status", "?")
        detail = result.get("detail", "")
        print(f"[error] {operation} 失敗 (HTTP {status}): {detail}", file=sys.stderr)

        if status == 401:
            print(
                "[hint] 401 Unauthorized: API token が無効です。\n"
                "       dev.to の Settings > Extensions で再発行し、\n"
                "       D:\\api-keys.json の devto_api_key を更新してください。",
                file=sys.stderr,
            )
        elif status == 422:
            print(
                "[hint] 422 Unprocessable Entity: タイトルの重複・タグ制約違反等。\n"
                "       --title-override や --tags を調整してください。",
                file=sys.stderr,
            )
        elif status == 429:
            print(
                "[hint] 429 Too Many Requests: レート制限。しばらく待ってから再実行してください。",
                file=sys.stderr,
            )
        elif status == 0:
            print(
                "[hint] ネットワーク接続エラー。インターネット接続と dev.to のステータスを確認してください。",
                file=sys.stderr,
            )
        return 1

    # ── 成功 ──────────────────────────────────────
    new_id = result.get("id")
    url = result.get("url", result.get("path", ""))
    print(f"[ok] {operation} 成功!")
    print(f"     id  : {new_id}")
    print(f"     url : {url}")
    print(f"     状態: {'公開' if result.get('published') else 'draft'}")

    # サイドカー保存 (id / url を永続化)
    sidecar_data = {
        "id": new_id,
        "url": url,
        "published": result.get("published", False),
        "title": result.get("title", ""),
        "created_at": result.get("created_at", ""),
        "updated_at": result.get("updated_at", ""),
        "source_file": str(md_path.resolve()),
    }
    save_sidecar(md_path, sidecar_data)

    return 0


if __name__ == "__main__":
    sys.exit(main())
