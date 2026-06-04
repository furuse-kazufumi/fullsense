#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qiita_team_post.py — minimal Qiita Team poster / registration-safety checker (stdlib only).

公開の "qiita-team-cli" は npm に存在せず、公式 @qiita/qiita-cli は qiita.com 専用 (Team 非対応)。
本ツールは Qiita Team API v2 (https://<team>.qiita.com/api/v2/) を直接叩く最小クライアント。

SECURITY (CLAUDE.md / reference_qiita_cli 運用ルール厳守):
  - 生トークンをコードに書かない。env `QIITA_TEAM_TOKEN` か D:/api-keys.json の `qiita_team_token` から読む。
  - publish は外部公開 = ユーザーが GO。本ツールは既定で **dry-run / scan のみ**。実 POST は明示 `--yes` 必須。
  - 新規は private:true 既定 (限定共有)。既存更新 (frontmatter に id) は可視性を変えない。

Qiita API v2 (一次確認 2026-06-04, https://qiita.com/api/v2/docs):
  POST  /api/v2/items            新規作成   body={title, body, tags:[{name,versions}], private, tweet,
                                            coediting(Team), group_url_name(Team)}
  PATCH /api/v2/items/:id         更新
  GET   /api/v2/authenticated_user  トークン疎通確認

使い方:
  py -3.11 qiita_team_post.py scan  [glob]      # 登録安全性スキャン (read-only, network なし)
  py -3.11 qiita_team_post.py verify            # トークン疎通 (GET authenticated_user)
  py -3.11 qiita_team_post.py dry-run <file.md> # payload + 警告を表示 (network なし)
  py -3.11 qiita_team_post.py post <file.md> --yes   # 実 POST/PATCH (ユーザーが GO したときのみ)

team 既定 = fullsense。env `QIITA_TEAM` で上書き。
"""
from __future__ import annotations

import glob as _glob
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


TEAM = os.environ.get("QIITA_TEAM", "fullsense")
API_BASE = f"https://{TEAM}.qiita.com/api/v2"
ARTICLES_DIR = os.environ.get(
    "QIITA_ARTICLES_DIR",
    os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "docs", "articles")),
)
CHAR_LIMIT = 2_000_000  # Qiita 1 記事上限 (feedback_qiita_char_limit)


# --------------------------------------------------------------------------- #
# token (never hardcoded; env or api-keys.json)
# --------------------------------------------------------------------------- #


def get_token() -> str | None:
    t = os.environ.get("QIITA_TEAM_TOKEN")
    if t:
        return t.strip()
    for p in (r"D:/api-keys.json", os.path.expanduser("~/api-keys.json")):
        try:
            with open(p, "r", encoding="utf-8-sig") as f:
                d = json.load(f)
            for k in ("qiita_team_token", "qiita_token", "QIITA_TEAM_TOKEN"):
                if d.get(k):
                    return str(d[k]).strip()
        except (OSError, ValueError):
            continue
    return None


# --------------------------------------------------------------------------- #
# frontmatter (minimal, qiita-cli-compatible subset) + body
# --------------------------------------------------------------------------- #


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Return (meta, body). Supports `title:`, `tags:` (block list or inline), `private:`, `id:`."""
    meta: dict = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = text[3:end].strip("\n")
            body = text[end + 4:].lstrip("\n")
            cur_list_key = None
            for line in fm.splitlines():
                if cur_list_key and re.match(r"\s*-\s+", line):
                    meta.setdefault(cur_list_key, []).append(line.split("-", 1)[1].strip().strip("'\""))
                    continue
                cur_list_key = None
                m = re.match(r"([A-Za-z_]+):\s*(.*)$", line)
                if not m:
                    continue
                k, v = m.group(1), m.group(2).strip()
                if v == "":
                    cur_list_key = k  # block list follows
                    meta[k] = []
                elif v.startswith("[") and v.endswith("]"):
                    meta[k] = [x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
                else:
                    meta[k] = v.strip("'\"")
    return meta, body


def infer_title(meta: dict, body: str) -> str:
    if meta.get("title"):
        return str(meta["title"])
    for line in body.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def norm_tags(meta: dict) -> list[dict]:
    tags = meta.get("tags") or []
    if isinstance(tags, str):
        tags = [tags]
    out = []
    for t in tags:
        if not t or t == "TODO_TAG":
            continue
        name = re.sub(r"\s+", "_", str(t).strip())  # Qiita tags cannot contain spaces -> 403; normalise to '_'
        if name:
            out.append({"name": name, "versions": []})
    return out


def real_id(meta: dict) -> str | None:
    """Frontmatter id, treating 'null'/'none'/'' as ABSENT (so we POST-create, not PATCH /items/null)."""
    v = meta.get("id") or meta.get("qiita_item_id")
    if v is None:
        return None
    v = str(v).strip()
    return v if v and v.lower() not in ("null", "none") else None


def as_bool(v, default=True) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "yes", "1")
    return default


# --------------------------------------------------------------------------- #
# registration safety
# --------------------------------------------------------------------------- #

_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']")
_LOCALPATH_RE = re.compile(r"[A-Za-z]:[\\/]|\]\(\.{1,2}/")


def safety_findings(meta: dict, body: str) -> list[str]:
    out: list[str] = []
    title = infer_title(meta, body)
    if not title:
        out.append("NO TITLE (frontmatter title: or leading # 見出しが必要)")
    if not norm_tags(meta):
        out.append("NO TAGS (Qiita は tag 0 個で publish 拒否; TODO_TAG は実タグ化要)")
    n = len(body)
    if n > CHAR_LIMIT:
        out.append(f"OVER CHAR LIMIT ({n} > {CHAR_LIMIT})")
    for m in _IMG_RE.finditer(body):
        url = m.group(1) or m.group(2) or ""
        if not url.startswith("http"):
            out.append(f"NON-PUBLIC IMAGE: {url[:80]} (Qiita は local/相対パスを読めない → public URL か Qiita 直アップ)")
    if _LOCALPATH_RE.search(body):
        out.append("LOCAL PATH in body (D:\\ や ./ — feedback_no_local_path_in_public)")
    return out


def cmd_scan(args: list[str]) -> int:
    pattern = args[0] if args else os.path.join(ARTICLES_DIR, "QIITA_*.md")
    files = sorted(f for f in _glob.glob(pattern, recursive=True)
                   if "archive" not in f and ".worktrees" not in f and "qiita-cli-poc" not in f)
    safe = 0
    print(f"scan: {len(files)} files (pattern={pattern})\n")
    report = []
    for f in files:
        try:
            text = open(f, "r", encoding="utf-8-sig").read()
        except OSError:
            continue
        meta, body = split_frontmatter(text)
        finds = safety_findings(meta, body)
        base = os.path.basename(f)
        if finds:
            print(f"[NEEDS-FIX] {base}  ({len(body)} chars)")
            for x in finds:
                print(f"    - {x}")
        else:
            safe += 1
        report.append({"file": base, "chars": len(body), "title": bool(infer_title(meta, body)),
                       "tags": len(norm_tags(meta)), "findings": finds})
    print(f"\nsummary: {safe}/{len(files)} registration-safe (no findings)")
    outp = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qiita_registration_safety_report.json")
    json.dump({"team": TEAM, "files": report}, open(outp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"saved {outp}")
    return 0


# --------------------------------------------------------------------------- #
# API
# --------------------------------------------------------------------------- #


def _req(method: str, path: str, token: str, payload: dict | None = None) -> tuple[int, dict | str]:
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


def cmd_verify(_args: list[str]) -> int:
    token = get_token()
    if not token:
        print("NO TOKEN: set env QIITA_TEAM_TOKEN or add qiita_team_token to D:/api-keys.json")
        return 2
    code, body = _req("GET", "/authenticated_user", token)
    if code == 200 and isinstance(body, dict):
        print(f"OK: authenticated as @{body.get('id')} on team '{TEAM}' ({API_BASE})")
        return 0
    print(f"FAIL ({code}): {body}")
    return 1


def build_payload(meta: dict, body: str) -> dict:
    return {
        "title": infer_title(meta, body),
        "body": body,
        "tags": norm_tags(meta),
        "private": as_bool(meta.get("private"), default=True),
        "tweet": False,
    }


def cmd_dry_run(args: list[str]) -> int:
    if not args:
        print("usage: dry-run <file.md>")
        return 2
    text = open(args[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    p = build_payload(meta, body)
    finds = safety_findings(meta, body)
    item_id = real_id(meta)
    print(f"action: {'PATCH update id=' + str(item_id) if item_id else 'POST create'} on team '{TEAM}'")
    print(f"title : {p['title']}")
    print(f"tags  : {[t['name'] for t in p['tags']]}")
    print(f"private: {p['private']}   body chars: {len(body)}")
    if finds:
        print("WARNINGS:")
        for x in finds:
            print(f"  - {x}")
    else:
        print("registration-safe: no findings")
    print("\n(dry-run: nothing sent. add `post <file> --yes` to actually publish.)")
    return 0


def _writeback_id(path: str, item_id: str) -> None:
    """Store the new id in frontmatter so re-posts PATCH (idempotent). Replaces `id: null`/empty,
    inserts if absent, leaves a pre-existing real id untouched."""
    if not item_id:
        return
    text = open(path, "r", encoding="utf-8-sig").read()
    if not text.startswith("---"):
        return
    end = text.find("\n---", 3)
    if end == -1:
        return
    head, fm, tail = text[:3], text[3:end], text[end:]
    m = re.search(r"^(\s*id:\s*)(.*)$", fm, re.M)
    if m:
        cur = m.group(2).strip().strip("'\"")
        if cur and cur.lower() not in ("null", "none"):
            return  # a real id is already present
        fm = fm[:m.start()] + m.group(1) + item_id + fm[m.end():]  # replace id: null
    else:
        fm = fm + f"\nid: {item_id}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + fm + tail)


def cmd_post(args: list[str]) -> int:
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("usage: post <file.md> --yes")
        return 2
    if "--yes" not in args:
        print("refusing: --yes required (publish is an external action; you give the GO).")
        return cmd_dry_run(files[:1])
    token = get_token()
    if not token:
        print("NO TOKEN: set env QIITA_TEAM_TOKEN or add qiita_team_token to D:/api-keys.json")
        return 2
    text = open(files[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    finds = [x for x in safety_findings(meta, body) if x.startswith(("NO TITLE", "NO TAGS", "OVER CHAR"))]
    if finds:
        print("BLOCKED (fix first): " + "; ".join(finds))
        return 1
    p = build_payload(meta, body)
    item_id = real_id(meta)
    if item_id:
        code, res = _req("PATCH", f"/items/{item_id}", token, p)
    else:
        code, res = _req("POST", "/items", token, p)
    if code in (200, 201) and isinstance(res, dict):
        if not item_id and res.get("id"):
            _writeback_id(files[0], res.get("id"))  # idempotent re-posts (create -> store id -> future PATCH)
        print(f"OK ({code}): {res.get('url')}  id={res.get('id')}")
        return 0
    print(f"FAIL ({code}): {res}")
    return 1


def main() -> int:
    _utf8()
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd, rest = sys.argv[1], sys.argv[2:]
    return {"scan": cmd_scan, "verify": cmd_verify, "dry-run": cmd_dry_run,
            "post": cmd_post}.get(cmd, lambda a: (print(f"unknown cmd {cmd}"), 2)[1])(rest)


if __name__ == "__main__":
    raise SystemExit(main())
