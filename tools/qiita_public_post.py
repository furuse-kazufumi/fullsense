#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qiita_public_post.py — post FullSense articles to PUBLIC qiita.com (stdlib only).

qiita_team_post.py の公開 (qiita.com) 版。Team poster とは独立に動き、互いの id を壊さない。

設計差分 (qiita_team_post.py との違い):
  - API = https://qiita.com/api/v2 (公開), token = qiita-cli credentials か env QIITA_PUBLIC_TOKEN。
  - 冪等キーは frontmatter **`public_id:`** (Team の `id:` は触らない)。
    → 初回 POST 成功時に `public_id:` を書き戻し、以後は PATCH (重複作成防止)。
  - 本ツールは PUBLIC poster なので `private` 既定 = **false (一般公開)**。`--private` で限定共有。
  - `public_id` 無しで `id:` だけがある source は accidental create の危険があるため、実 POST には `--allow-create` を追加要求する。
  - 公開 = 不可逆な外部公開アクション。既定 dry-run、実 POST/PATCH は `--yes` 必須 (ユーザー GO)。
  - fail-closed: NO TITLE / NO TAGS / OVER CHAR / 非公開画像 / ローカルパス があれば BLOCK。

使い方:
  py -3.11 qiita_public_post.py verify                       # 公開トークン疎通
  py -3.11 qiita_public_post.py dry-run <file.md>            # payload + 警告 (network なし)
  py -3.11 qiita_public_post.py post <file.md> --yes         # 実 POST/PATCH (private=false)
  py -3.11 qiita_public_post.py post <file.md> --yes --private   # 限定共有で投稿
  py -3.11 qiita_public_post.py post <file.md> --yes --allow-create  # `public_id` 無し create を明示許可
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request

from _frontmatter import split_frontmatter


def _utf8() -> None:
    for s in ("stdout", "stderr"):
        st = getattr(sys, s, None)
        try:
            st.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
        except Exception:
            pass


API_BASE = "https://qiita.com/api/v2"
CHAR_LIMIT = 2_000_000
LEGACY_ID_WARNING_TEMPLATE = (
    "WARNING: frontmatter has id={legacy_id} but no public_id. "
    "This path will POST-create, not PATCH-update."
)
LEGACY_ID_BLOCK = (
    "BLOCKED: legacy/team-style id without public_id requires --allow-create "
    "before creating a new public item."
)
AMBIGUOUS_PRIVATE_BLOCK = (
    "BLOCKED: frontmatter private: is ignored by qiita_public_post.py. "
    "Set public_private: true/false explicitly."
)
CONFLICTING_PRIVATE_BLOCK = (
    "BLOCKED: frontmatter private: and public_private: disagree. "
    "Resolve visibility before posting."
)
UNRECOGNIZED_VISIBILITY_BLOCK = (
    "BLOCKED: frontmatter {field}: has unrecognized visibility value {value!r}. "
    "Use true/false (or yes/no/1/0)."
)


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


def legacy_id_without_public_id(meta: dict) -> str | None:
    """Return legacy/team-style id when public_id is absent, so callers can warn before accidental POST-create."""
    if real_public_id(meta):
        return None
    v = meta.get("id")
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


def parse_visibility(v) -> tuple[bool | None, str | None]:
    if isinstance(v, bool):
        return v, None
    if v is None:
        return None, None
    if isinstance(v, str):
        s = v.strip().lower()
        if s in ("true", "yes", "1"):
            return True, None
        if s in ("false", "no", "0"):
            return False, None
        if not s:
            return None, None
        return None, repr(v)
    return None, repr(v)


def privacy_field_findings(meta: dict) -> list[str]:
    out: list[str] = []
    has_private = "private" in meta
    has_public_private = "public_private" in meta
    private_val, private_bad = parse_visibility(meta.get("private"))
    public_private_val, public_private_bad = parse_visibility(meta.get("public_private"))
    if has_private and private_bad is not None:
        out.append(UNRECOGNIZED_VISIBILITY_BLOCK.format(field="private", value=meta.get("private")))
    if has_public_private and public_private_bad is not None:
        out.append(UNRECOGNIZED_VISIBILITY_BLOCK.format(field="public_private", value=meta.get("public_private")))
    if out:
        return out
    if has_private and not has_public_private:
        out.append(AMBIGUOUS_PRIVATE_BLOCK)
        return out
    if has_private and has_public_private:
        if private_val != public_private_val:
            out.append(CONFLICTING_PRIVATE_BLOCK)
    return out


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
    public_private, _bad = parse_visibility(meta.get("public_private"))
    private = force_private if force_private is not None else (public_private if public_private is not None else False)
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
    force_private = True if "--private" in args else None
    text = open(files[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    p = build_payload(meta, body, force_private)
    finds = safety_findings(meta, body)
    privacy_finds = privacy_field_findings(meta)
    pid = real_public_id(meta)
    legacy_id = legacy_id_without_public_id(meta)
    print(f"target: PUBLIC qiita.com ({API_BASE})")
    print(f"action: {'PATCH update public_id=' + str(pid) if pid else 'POST create (new public article)'}")
    print(f"title : {p['title']}")
    print(f"tags  : {[t['name'] for t in p['tags']]}")
    print(f"private: {p['private']}   body chars: {len(body)}")
    if legacy_id:
        print(LEGACY_ID_WARNING_TEMPLATE.format(legacy_id=legacy_id))
    for x in privacy_finds:
        print(x)
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
        print("usage: post <file.md> --yes [--private] [--allow-create]")
        return 2
    if "--yes" not in args:
        print("refusing: --yes required (公開は外部公開アクション。ユーザーが GO を出す)")
        return cmd_dry_run(files[:1] + (["--private"] if "--private" in args else []))
    token = get_token()
    if not token:
        print("NO TOKEN")
        return 2
    force_private = True if "--private" in args else None
    text = open(files[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    # safety_findings currently returns only hard blockers. Keep the prefix filter explicit
    # so future soft warnings do not silently become publish-blocking.
    hard = [x for x in safety_findings(meta, body)
            if x.startswith(("NO TITLE", "NO TAGS", "OVER CHAR", "NON-PUBLIC IMAGE", "LOCAL PATH"))]
    hard.extend(privacy_field_findings(meta))
    if hard:
        print("BLOCKED (fix first): " + "; ".join(hard))
        return 1
    p = build_payload(meta, body, force_private)
    pid = real_public_id(meta)
    legacy_id = legacy_id_without_public_id(meta)
    if legacy_id:
        print(LEGACY_ID_WARNING_TEMPLATE.format(legacy_id=legacy_id))
        if "--allow-create" not in args:
            print(LEGACY_ID_BLOCK)
            return 1
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
