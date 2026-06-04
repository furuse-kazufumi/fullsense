#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qiita_public_team_link.py — 公開 qiita.com 記事へ FullSense Team KB 誘導ブロックを外科的に挿入する (stdlib only).

背景 (memory: reference_qiita_team_fullsense):
  Qiita Team (https://fullsense.qiita.com/) に全史 KB (63+ 記事) を集約済。残タスク (c) =
  公開 qiita.com 記事から Team KB への誘導リンク。ローカル md は Team 正本になっているため、
  **公開側の live body を GET → 誘導ブロックだけ挿入 → PATCH** する (公開記事の他内容を壊さない)。

SECURITY / 運用 (qiita_team_post.py と同方針):
  - 生トークンをコードに書かない。env `QIITA_PUBLIC_TOKEN` か qiita-cli credentials
    (~/.config/qiita-cli/credentials.json) から読む。token 値は決して print しない。
  - 既定は read-only (list / dry-run / verify)。実 PATCH は `apply --yes` のみ (外部公開=ユーザー GO)。
  - idempotent: 挿入ブロックに MARKER を埋め、既に在れば skip。
  - fail-closed: GET 失敗・構造不明はその記事を skip して報告 (黙って変形しない)。

使い方:
  py -3.11 qiita_public_team_link.py list                  # 公開記事一覧 (read-only)
  py -3.11 qiita_public_team_link.py dry-run <id>...       # 挿入プレビュー (D:/tmp/qiita_team_link_preview/)
  py -3.11 qiita_public_team_link.py apply <id>... --yes   # 実 PATCH (ユーザー GO 必須)
  py -3.11 qiita_public_team_link.py verify <id>...        # 再 GET で MARKER 存在確認
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request


def _utf8() -> None:
    for s in ("stdout", "stderr"):
        st = getattr(sys, s, None)
        try:
            st.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except Exception:
            pass


API_BASE = "https://qiita.com/api/v2"
PREVIEW_DIR = "D:/tmp/qiita_team_link_preview"
MARKER = "<!-- fullsense-team-kb -->"

# 誘導先: Qiita Team の読む順 index (QIITA_INDEX_reading_order.md, team id=90ea260703fb49065346)
TEAM_TOP = "https://fullsense.qiita.com/"
TEAM_INDEX = "https://fullsense.qiita.com/furuse-kazufumi/items/90ea260703fb49065346"

# 言語セクション見出し (feedback_multilingual_article_structure の縦積み形式)
LANG_HEADINGS = {
    "ja": re.compile(r"^# 日本語\s*$", re.M),
    "en": re.compile(r"^# English\s*$", re.M),
    "zh": re.compile(r"^# 中文\s*$", re.M),
    "ko": re.compile(r"^# 한국어\s*$", re.M),
}

# 誘導ブロック (言語別)。アクセス招待 CTA は入れない (Team は有償メンバー制のため
# 「コメントで招待希望」のような約束はユーザー判断なしに公開しない)。
BLURBS = {
    "ja": (
        f":::note info\n"
        f"**📚 FullSense ナレッジベースのご案内** {MARKER}\n"
        f"この記事の最新版 (4 言語・図版更新済) と、FullSense 開発全史 60+ 記事"
        f" (物語ベースの[読む順ガイド]({TEAM_INDEX})・かみくだき版・4 コマ漫画つき) は"
        f" Qiita Team **[FullSense KB]({TEAM_TOP})** に集約しています (チームメンバー向け)。\n"
        f":::\n"
    ),
    "en": (
        f":::note info\n"
        f"**📚 FullSense Knowledge Base** {MARKER}\n"
        f"The latest version of this article (4 languages, updated figures) — together with the full"
        f" FullSense development history of 60+ articles (a story-based [reading guide]({TEAM_INDEX}),"
        f" plain-language editions, and 4-panel manga) — is consolidated in our Qiita Team"
        f" **[FullSense KB]({TEAM_TOP})** (team members only).\n"
        f":::\n"
    ),
    "zh": (
        f":::note info\n"
        f"**📚 FullSense 知识库指南** {MARKER}\n"
        f"本文的最新版本（4 种语言・图表已更新），以及 FullSense 开发全史 60+ 篇文章"
        f"（故事化的[阅读顺序指南]({TEAM_INDEX})・通俗易懂版・四格漫画）均已汇总至 Qiita Team"
        f" **[FullSense KB]({TEAM_TOP})**（仅限团队成员）。\n"
        f":::\n"
    ),
    "ko": (
        f":::note info\n"
        f"**📚 FullSense 지식 베이스 안내** {MARKER}\n"
        f"이 글의 최신판 (4개 언어・도판 갱신됨) 과 FullSense 개발 전사 60+ 편"
        f" (스토리 기반 [읽기 순서 가이드]({TEAM_INDEX})・쉬운 설명판・4컷 만화 포함) 은 Qiita Team"
        f" **[FullSense KB]({TEAM_TOP})** 에 모여 있습니다 (팀 멤버 전용).\n"
        f":::\n"
    ),
}


# --------------------------------------------------------------------------- #
# token (never hardcoded / never printed; env or qiita-cli credentials)
# --------------------------------------------------------------------------- #


def get_token() -> str | None:
    t = os.environ.get("QIITA_PUBLIC_TOKEN")
    if t:
        return t.strip()
    p = os.path.expanduser("~/.config/qiita-cli/credentials.json")
    try:
        with open(p, "r", encoding="utf-8-sig") as f:
            d = json.load(f)
        for c in d.get("credentials", []):
            if c.get("accessToken"):
                return str(c["accessToken"]).strip()
    except (OSError, ValueError):
        pass
    return None


def _req(method: str, path: str, token: str, payload: dict | None = None) -> tuple[int, dict | list | str]:
    url = f"{API_BASE}{path}"
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", f"Bearer {token}")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode("utf-8"))
        except Exception:
            return e.code, str(e)
    except urllib.error.URLError as e:
        return 0, f"URLError: {e}"


# --------------------------------------------------------------------------- #
# insertion
# --------------------------------------------------------------------------- #


def insert_blurbs(body: str) -> tuple[str | None, dict]:
    """誘導ブロックを挿入した body と report を返す。挿入不能/既挿入は (None, report)。

    多言語縦積み (>=2 言語見出し) → 各言語見出し行の直後に言語別ブロック。
    それ以外 (JA 単独等) → 先頭 (先頭行が H1 ならその直後) に JA ブロック。
    """
    report: dict = {"langs": [], "mode": None, "skipped": None}
    if MARKER in body:
        report["skipped"] = "already-inserted"
        return None, report

    hits = []  # (pos_end_of_heading_line, lang)
    for lang, pat in LANG_HEADINGS.items():
        m = pat.search(body)
        if m:
            hits.append((m.end(), lang))
    hits.sort()
    report["langs"] = [lang for _, lang in hits]

    if len(hits) >= 2:
        report["mode"] = "multilang"
        new = body
        for end, lang in reversed(hits):  # 後ろから挿入して index を保つ
            new = new[:end] + "\n\n" + BLURBS[lang].rstrip("\n") + "\n" + new[end:]
        return new, report

    # 単言語 fallback: 先頭 H1 の直後 (なければ最先頭)
    report["mode"] = "top"
    lines = body.split("\n")
    idx = 0
    if lines and lines[0].startswith("# "):
        idx = 1
    new = "\n".join(lines[:idx]) + ("\n\n" if idx else "") + BLURBS["ja"].rstrip("\n") + "\n\n" + "\n".join(lines[idx:])
    return new, report


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #


def cmd_list(_args: list[str]) -> int:
    token = get_token()
    if not token:
        print("NO TOKEN: env QIITA_PUBLIC_TOKEN か qiita-cli credentials が必要")
        return 2
    items, page = [], 1
    while True:
        code, batch = _req("GET", f"/authenticated_user/items?page={page}&per_page=100", token)
        if code != 200 or not isinstance(batch, list):
            print(f"FAIL ({code}): {batch}")
            return 1
        if not batch:
            break
        items.extend(batch)
        page += 1
    rows = []
    for i in items:
        rows.append({
            "id": i["id"], "title": i["title"], "created_at": i["created_at"][:10],
            "updated_at": i["updated_at"][:10], "private": i["private"],
            "tags": [t["name"] for t in i["tags"]], "likes": i["likes_count"],
            "body_chars": len(i["body"]), "url": i["url"],
            "has_marker": MARKER in i["body"],
        })
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    outp = os.path.join(PREVIEW_DIR, "public_items.json")
    json.dump(rows, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"total={len(rows)}  (saved {outp})\n")
    for r in rows:
        flag = "M" if r["has_marker"] else ("p" if r["private"] else "-")
        print(f"{r['id']}  {r['created_at']} {flag} {r['body_chars']:>7}c likes={r['likes']:>3}  {r['title'][:78]}")
    print("\nflag: M=誘導挿入済 p=限定共有 -=公開")
    return 0


def cmd_dry_run(args: list[str]) -> int:
    ids = [a for a in args if not a.startswith("--")]
    if not ids:
        print("usage: dry-run <id>...")
        return 2
    token = get_token()
    if not token:
        print("NO TOKEN")
        return 2
    os.makedirs(PREVIEW_DIR, exist_ok=True)
    ok = 0
    for item_id in ids:
        code, item = _req("GET", f"/items/{item_id}", token)
        if code != 200 or not isinstance(item, dict):
            print(f"[FAIL-GET] {item_id} ({code}): {str(item)[:120]}")
            continue
        new, rep = insert_blurbs(item["body"])
        if new is None:
            print(f"[SKIP] {item_id}  {rep['skipped']}  {item['title'][:60]}")
            continue
        prev = os.path.join(PREVIEW_DIR, f"{item_id}.md")
        with open(prev, "w", encoding="utf-8") as f:
            f.write(new)
        print(f"[PREVIEW] {item_id}  mode={rep['mode']} langs={','.join(rep['langs']) or '-'}  "
              f"+{len(new) - len(item['body'])}c  {item['title'][:60]}")
        ok += 1
    print(f"\n{ok}/{len(ids)} previews written to {PREVIEW_DIR} (nothing sent)")
    return 0


def cmd_apply(args: list[str]) -> int:
    ids = [a for a in args if not a.startswith("--")]
    if not ids:
        print("usage: apply <id>... --yes")
        return 2
    if "--yes" not in args:
        print("refusing: --yes required (公開記事の変更=外部公開アクション。ユーザーが GO を出す)")
        return 2
    token = get_token()
    if not token:
        print("NO TOKEN")
        return 2
    ok = fail = skip = 0
    for item_id in ids:
        code, item = _req("GET", f"/items/{item_id}", token)  # 直前 re-GET (鮮度)
        if code != 200 or not isinstance(item, dict):
            print(f"[FAIL-GET] {item_id} ({code})")
            fail += 1
            continue
        new, rep = insert_blurbs(item["body"])
        if new is None:
            print(f"[SKIP] {item_id}  {rep['skipped']}")
            skip += 1
            continue
        payload = {
            "title": item["title"],
            "body": new,
            "tags": item["tags"],
            "private": item["private"],  # 可視性は変えない
        }
        code, res = _req("PATCH", f"/items/{item_id}", token, payload)
        if code == 200 and isinstance(res, dict):
            print(f"[OK] {item_id}  mode={rep['mode']} langs={','.join(rep['langs']) or '-'}  {res.get('url')}")
            ok += 1
        else:
            print(f"[FAIL-PATCH] {item_id} ({code}): {str(res)[:200]}")
            fail += 1
    print(f"\napplied={ok} skipped={skip} failed={fail}")
    return 0 if fail == 0 else 1


def cmd_verify(args: list[str]) -> int:
    ids = [a for a in args if not a.startswith("--")]
    if not ids:
        print("usage: verify <id>...")
        return 2
    token = get_token()
    if not token:
        print("NO TOKEN")
        return 2
    bad = 0
    for item_id in ids:
        code, item = _req("GET", f"/items/{item_id}", token)
        if code != 200 or not isinstance(item, dict):
            print(f"[FAIL-GET] {item_id} ({code})")
            bad += 1
            continue
        n = item["body"].count(MARKER)
        status = "OK" if n >= 1 else "MISSING"
        if n < 1:
            bad += 1
        print(f"[{status}] {item_id}  markers={n}  {item['title'][:60]}")
    print(f"\nverify: {len(ids) - bad}/{len(ids)} OK")
    return 0 if bad == 0 else 1


def main() -> int:
    _utf8()
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd, rest = sys.argv[1], sys.argv[2:]
    return {"list": cmd_list, "dry-run": cmd_dry_run, "apply": cmd_apply,
            "verify": cmd_verify}.get(cmd, lambda a: (print(f"unknown cmd {cmd}"), 2)[1])(rest)


if __name__ == "__main__":
    raise SystemExit(main())
