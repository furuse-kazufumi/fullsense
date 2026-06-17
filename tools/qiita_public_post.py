#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qiita_public_post.py — post FullSense articles to PUBLIC qiita.com (stdlib only).

qiita_team_post.py の公開 (qiita.com) 版。Team poster とは独立に動き、互いの id を壊さない。

設計差分 (qiita_team_post.py との違い):
  - API = https://qiita.com/api/v2 (公開), token = qiita-cli credentials か env QIITA_PUBLIC_TOKEN。
  - 冪等キーは frontmatter **`public_id:`** (Team の `id:` は触らない)。
    → 初回 POST 成功時に `public_id:` を書き戻し、以後は PATCH (重複作成防止)。
  - 本ツールは PUBLIC poster なので `private` 既定 = **false (一般公開)**。`--private` で限定共有。
  - 公開 = 不可逆な外部公開アクション。既定 dry-run、実 POST/PATCH は `--yes` 必須 (ユーザー GO)。
  - fail-closed: NO TITLE / NO TAGS / OVER CHAR / 非公開画像 / ローカルパス があれば BLOCK。

使い方:
  py -3.11 qiita_public_post.py verify                       # 公開トークン疎通
  py -3.11 qiita_public_post.py dry-run <file.md>            # payload + 警告 (network なし)
  py -3.11 qiita_public_post.py post <file.md> --yes         # 実 POST/PATCH (private=false)
  py -3.11 qiita_public_post.py post <file.md> --yes --private   # 限定共有で投稿
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
CHAR_LIMIT = 2_000_000


# --------------------------------------------------------------------------- #
# token (public; never hardcoded / never printed)
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


# --------------------------------------------------------------------------- #
# frontmatter + body (mirrors qiita_team_post.py)
# --------------------------------------------------------------------------- #


def _block_scalar_lines(lines: list[str], start_idx: int) -> tuple[list[str], int]:
    cont: list[str] = []
    j = start_idx + 1
    while j < len(lines):
        ln = lines[j]
        if not ln.strip():
            if cont:
                break
            j += 1
            continue
        if re.match(r"^[ \t]+\S", ln):
            cont.append(ln.strip())
            j += 1
            continue
        break
    return cont, j


def _unquote_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        inner = value[1:-1]
        if value[0] == "'":
            return inner.replace("''", "'")
        return inner.replace('\\"', '"')
    return value


def split_frontmatter(text: str) -> tuple[dict, str]:
    meta: dict = {}
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            fm = text[3:end].strip("\n")
            body = text[end + 4:].lstrip("\n")
            cur_list_key = None
            lines = fm.splitlines()
            i = 0
            while i < len(lines):
                line = lines[i]
                if cur_list_key and re.match(r"\s*-\s+", line):
                    meta.setdefault(cur_list_key, []).append(line.split("-", 1)[1].strip().strip("'\""))
                    i += 1
                    continue
                cur_list_key = None
                m = re.match(r"([A-Za-z_]+):\s*(.*)$", line)
                if not m:
                    i += 1
                    continue
                k, v = m.group(1), m.group(2).strip()
                if v == "":
                    cur_list_key = k
                    meta[k] = []
                elif v in (">", ">-", ">+", "|", "|-", "|+"):
                    cont, i = _block_scalar_lines(lines, i)
                    meta[k] = " ".join(cont).strip()
                    continue
                elif v.startswith("[") and v.endswith("]"):
                    meta[k] = [_unquote_scalar(x.strip()) for x in v[1:-1].split(",") if x.strip()]
                else:
                    meta[k] = _unquote_scalar(v)
                i += 1
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
    out, seen = [], set()
    for t in tags:
        for part in str(t).split(","):
            name = re.sub(r"\s+", "_", part.strip())
            if name and name != "TODO_TAG" and name not in seen:
                seen.add(name)
                out.append({"name": name, "versions": []})
    return out[:5]


def real_public_id(meta: dict) -> str | None:
    """Frontmatter public_id (PUBLIC qiita.com item id). 'null'/'none'/'' -> ABSENT (POST-create)."""
    v = meta.get("public_id")
    if isinstance(v, list):
        v = v[0] if v else None
    if v is None:
        return None
    v = str(v).strip()
    return v if v and v.lower() not in ("null", "none") else None


def as_bool(v, default=False) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        return v.strip().lower() in ("true", "yes", "1")
    return default


# --------------------------------------------------------------------------- #
# registration safety (mirrors qiita_team_post.py)
# --------------------------------------------------------------------------- #

_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']")
_LOCALPATH_RE = re.compile(r"[A-Za-z]:\\|[A-Za-z]:/(?!/)|\]\(\.{1,2}/")


def safety_findings(meta: dict, body: str) -> list[str]:
    out: list[str] = []
    title = infer_title(meta, body)
    if not title:
        out.append("NO TITLE (frontmatter title: か 先頭 # 見出しが必要)")
    if not norm_tags(meta):
        out.append("NO TAGS (Qiita は tag 0 個で publish 拒否)")
    n = len(body)
    if n > CHAR_LIMIT:
        out.append(f"OVER CHAR LIMIT ({n} > {CHAR_LIMIT})")
    for m in _IMG_RE.finditer(body):
        url = m.group(1) or m.group(2) or ""
        if not url.startswith("http"):
            out.append(f"NON-PUBLIC IMAGE: {url[:80]} (public URL か Qiita 直アップが必要)")
    if _LOCALPATH_RE.search(body):
        out.append("LOCAL PATH in body (D:\\ や ./ — feedback_no_local_path_in_public)")
    return out


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
        print("NO TOKEN: set env QIITA_PUBLIC_TOKEN or qiita-cli credentials.json")
        return 2
    code, body = _req("GET", "/authenticated_user", token)
    if code == 200 and isinstance(body, dict):
        print(f"OK: authenticated as @{body.get('id')} on PUBLIC qiita.com ({API_BASE})")
        return 0
    print(f"FAIL ({code}): {body}")
    return 1


def build_payload(meta: dict, body: str, force_private: bool | None) -> dict:
    private = force_private if force_private is not None else as_bool(meta.get("public_private"), default=False)
    return {
        "title": infer_title(meta, body),
        "body": body,
        "tags": norm_tags(meta),
        "private": private,
        "tweet": False,
    }


def cmd_dry_run(args: list[str]) -> int:
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("usage: dry-run <file.md>")
        return 2
    force_private = True if "--private" in args else False
    text = open(files[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    p = build_payload(meta, body, force_private)
    finds = safety_findings(meta, body)
    pid = real_public_id(meta)
    print(f"target: PUBLIC qiita.com ({API_BASE})")
    print(f"action: {'PATCH update public_id=' + str(pid) if pid else 'POST create (new public article)'}")
    print(f"title : {p['title']}")
    print(f"tags  : {[t['name'] for t in p['tags']]}")
    print(f"private: {p['private']}   body chars: {len(body)}")
    if finds:
        print("WARNINGS:")
        for x in finds:
            print(f"  - {x}")
    else:
        print("registration-safe: no findings")
    print("\n(dry-run: nothing sent. `post <file> --yes` to publish.)")
    return 0


def _writeback_public_id(path: str, item_id: str) -> None:
    if not item_id:
        return
    text = open(path, "r", encoding="utf-8-sig").read()
    if not text.startswith("---"):
        return
    end = text.find("\n---", 3)
    if end == -1:
        return
    head, fm, tail = text[:3], text[3:end], text[end:]
    m = re.search(r"^(\s*public_id:\s*)(.*)$", fm, re.M)
    if m:
        cur = m.group(2).strip().strip("'\"")
        if cur and cur.lower() not in ("null", "none"):
            return
        fm = fm[:m.start()] + m.group(1) + item_id + fm[m.end():]
    else:
        fm = fm + f"\npublic_id: {item_id}"
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + fm + tail)


def cmd_post(args: list[str]) -> int:
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("usage: post <file.md> --yes [--private]")
        return 2
    if "--yes" not in args:
        print("refusing: --yes required (公開は外部公開アクション。ユーザーが GO を出す)")
        return cmd_dry_run(files[:1] + (["--private"] if "--private" in args else []))
    token = get_token()
    if not token:
        print("NO TOKEN")
        return 2
    force_private = True if "--private" in args else False
    text = open(files[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    hard = [x for x in safety_findings(meta, body)
            if x.startswith(("NO TITLE", "NO TAGS", "OVER CHAR", "NON-PUBLIC IMAGE", "LOCAL PATH"))]
    if hard:
        print("BLOCKED (fix first): " + "; ".join(hard))
        return 1
    p = build_payload(meta, body, force_private)
    pid = real_public_id(meta)
    if pid:
        code, res = _req("PATCH", f"/items/{pid}", token, p)
    else:
        code, res = _req("POST", "/items", token, p)
    if code in (200, 201) and isinstance(res, dict):
        if not pid and res.get("id"):
            _writeback_public_id(files[0], res.get("id"))
        vis = "private(限定共有)" if p["private"] else "PUBLIC(一般公開)"
        print(f"OK ({code}) [{vis}]: {res.get('url')}  public_id={res.get('id')}")
        return 0
    print(f"FAIL ({code}): {res}")
    return 1


def main() -> int:
    _utf8()
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd, rest = sys.argv[1], sys.argv[2:]
    return {"verify": cmd_verify, "dry-run": cmd_dry_run, "post": cmd_post}.get(
        cmd, lambda a: (print(f"unknown cmd {cmd}"), 2)[1])(rest)


if __name__ == "__main__":
    raise SystemExit(main())
