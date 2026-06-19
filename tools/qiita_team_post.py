#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""qiita_team_post.py — minimal Qiita Team poster / registration-safety checker (stdlib only).

公開の "qiita-team-cli" は npm に存在せず、公式 @qiita/qiita-cli は qiita.com 専用 (Team 非対応)。
本ツールは Qiita Team API v2 (https://<team>.qiita.com/api/v2/) を直接叩く最小クライアント。

SECURITY (CLAUDE.md / reference_qiita_cli 運用ルール厳守):
  - 生トークンをコードに書かない。env `QIITA_TEAM_TOKEN` か D:/api-keys.json の `qiita_team_token` から読む。
  - publish は外部公開 = ユーザーが GO。本ツールは既定で **dry-run / scan のみ**。実 POST は明示 `--yes` 必須。
  - 新規は private:true を既定送信するが、Qiita Team での実効可視範囲は別途一次確認が必要。
  - 既存更新 (frontmatter に id) も payload には `private` を含むが、Qiita Team 側で visibility flip に効くかは未検証。rollback は runbook の確認手順を前提にする。

Qiita API v2 (一次確認 2026-06-04, https://qiita.com/api/v2/docs):
  POST  /api/v2/items            新規作成   body={title, body, tags:[{name,versions}], private, tweet,
                                            coediting(Team), group_url_name(Team)}
  PATCH /api/v2/items/:id         更新
  GET   /api/v2/authenticated_user  トークン疎通確認

使い方:
  py -3.11 qiita_team_post.py scan  [glob]      # 登録安全性スキャン (read-only, network なし)
  py -3.11 qiita_team_post.py verify            # トークン疎通 (GET authenticated_user)
  py -3.11 qiita_team_post.py dry-run <file.md> [--patch-group-url-name]
                                                # payload + 警告を表示 (network なし)
  py -3.11 qiita_team_post.py post <file.md> --yes [--force-ignore-publish]
                                                [--patch-group-url-name]
                                                # 実 POST/PATCH (ユーザーが GO したときのみ)

team 既定 = fullsense。env `QIITA_TEAM` で上書き。

NOTE:
  - create (`id` なし) は explicit `group_url_name` を payload へ送る
  - PATCH (`id` あり) は `group_url_name` を既定送信しない。share target を寄せ直す
    ときだけ `--patch-group-url-name` を明示し、frontmatter の concrete target を再送する
"""
from __future__ import annotations

import glob as _glob
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
        for part in str(t).split(","):  # handle inline comma-separated `tags: a,b,c`
            name = re.sub(r"\s+", "_", part.strip())  # Qiita tags cannot contain spaces -> 403
            if name and name != "TODO_TAG" and name not in seen:
                seen.add(name)
                out.append({"name": name, "versions": []})
    return out[:5]  # Qiita allows at most 5 tags


def _clean_nullish_scalar(v) -> str | None:
    if v is None:
        return None
    v = str(v).strip()
    return v if v and v.lower() not in ("null", "none") else None


def explicit_group_target(meta: dict) -> str | None:
    if "group_url_name" not in meta:
        return None
    return _clean_nullish_scalar(meta.get("group_url_name"))


def real_id(meta: dict) -> str | None:
    """Frontmatter id, treating 'null'/'none'/'' as ABSENT (so we POST-create, not PATCH /items/null)."""
    return _clean_nullish_scalar(meta.get("id")) or _clean_nullish_scalar(meta.get("qiita_item_id"))


def as_bool(v, default=True) -> bool:
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        s = v.strip().lower()
        if not s:
            return default
        return s in ("true", "yes", "1")
    return default


IGNORE_PUBLISH_WARNING = "WARNING: frontmatter ignorePublish: true is a qiita-cli gate; Team post requires explicit override."
IGNORE_PUBLISH_BLOCK = "IGNORE_PUBLISH_BLOCK: add --force-ignore-publish only after human approval for this Team POST."
UNRECOGNIZED_IGNORE_PUBLISH_BLOCK = "UNRECOGNIZED_IGNORE_PUBLISH_BLOCK: ignorePublish value '{value}' is not recognized"
PATCH_GROUP_URL_NAME_BLOCK = (
    "PATCH_GROUP_URL_NAME_BLOCK: --patch-group-url-name requires explicit non-empty group_url_name in frontmatter"
)
PATCH_GROUP_URL_NAME_CREATE_NOTE = (
    "note: --patch-group-url-name is a no-op on CREATE (group_url_name is already sent from frontmatter; the flag only adds resend on PATCH/update)"
)
UNKNOWN_FLAG_BLOCK = "UNKNOWN_FLAG_BLOCK: unsupported flag '{flag}'"


def parse_gate_bool(v) -> tuple[bool | None, str | None]:
    # Intentional split: `private` uses as_bool(default=True) so malformed values
    # collapse to the safer private side, while `ignorePublish` is an operator
    # gate and must surface malformed values as explicit errors.
    if v is None:
        return None, None
    if isinstance(v, bool):
        return v, None
    if isinstance(v, str):
        s = v.strip().lower()
        if not s:
            return None, None
        if s in ("true", "yes", "1"):
            return True, None
        if s in ("false", "no", "0"):
            return False, None
        return None, UNRECOGNIZED_IGNORE_PUBLISH_BLOCK.format(value=v)
    return None, UNRECOGNIZED_IGNORE_PUBLISH_BLOCK.format(value=v)


def find_ignore_publish_key_issue(meta: dict) -> str | None:
    for key in meta.keys():
        stripped = str(key).strip()
        if stripped.casefold() == "ignorepublish" and stripped != "ignorePublish":
            return f"IGNORE_PUBLISH_KEY_BLOCK: use exact frontmatter key 'ignorePublish', not '{key}'"
    return None


def wants_patch_group_url_name(args: list[str]) -> bool:
    return "--patch-group-url-name" in args


def validate_flags(args: list[str], *, allowed_flags: set[str]) -> str | None:
    for arg in args:
        if not arg.startswith("-"):
            continue
        if arg in allowed_flags:
            continue
        return UNKNOWN_FLAG_BLOCK.format(flag=arg)
    return None


# --------------------------------------------------------------------------- #
# registration safety
# --------------------------------------------------------------------------- #

_IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)|<img[^>]+src=[\"']([^\"']+)[\"']")
# Drive-letter path (D:\ or D:/foo) or relative markdown link (](./ ](../).
# `:/(?!/)` excludes URL schemes like https:// (s:// → ':/' followed by '/'),
# which the old `[A-Za-z]:[\\/]` falsely flagged once articles include links.
_LOCALPATH_RE = re.compile(r"[A-Za-z]:\\|[A-Za-z]:/(?!/)|\]\(\.{1,2}/")


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
    if not real_id(meta) and "group_url_name" not in meta:
        out.append("MISSING GROUP TARGET: Team create requires explicit group_url_name")
    elif not real_id(meta) and "group_url_name" in meta and explicit_group_target(meta) is None:
        out.append("INVALID GROUP TARGET: group_url_name must be a non-empty concrete share target")
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


def build_payload(meta: dict, body: str, *, include_group_url_name: bool = False) -> dict:
    payload = {
        "title": infer_title(meta, body),
        "body": body,
        "tags": norm_tags(meta),
        "private": as_bool(meta.get("private"), default=True),
        "tweet": False,
    }
    # Team visibility can depend on an explicit share target. Require callers
    # to spell out group_url_name on create instead of relying on implicit
    # Team defaults such as "General".
    if include_group_url_name:
        group_url_name = explicit_group_target(meta)
        if group_url_name is not None:
            payload["group_url_name"] = group_url_name
    return payload


def cmd_dry_run(args: list[str]) -> int:
    flag_error = validate_flags(args, allowed_flags={"--patch-group-url-name"})
    if flag_error:
        print(f"BLOCKED: {flag_error}")
        print("usage: dry-run <file.md> [--patch-group-url-name]")
        return 1
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("usage: dry-run <file.md> [--patch-group-url-name]")
        return 2
    if len(files) != 1:
        print(f"BLOCKED: exactly one file expected, got {len(files)}")
        print("usage: dry-run <file.md> [--patch-group-url-name]")
        return 2
    text = open(files[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    item_id = real_id(meta)
    create_group_target = explicit_group_target(meta) if not item_id else None
    patch_group_target = explicit_group_target(meta) if item_id else None
    patch_group_flag = wants_patch_group_url_name(args)
    resend_patch_group = bool(item_id and patch_group_flag)
    p = build_payload(meta, body, include_group_url_name=(not item_id) or resend_patch_group)
    finds = safety_findings(meta, body)
    gate_value, gate_error = parse_gate_bool(meta.get("ignorePublish"))
    gate_key_error = find_ignore_publish_key_issue(meta)
    print(f"action: {'PATCH update id=' + str(item_id) if item_id else 'POST create'} on team '{TEAM}'")
    print(f"title : {p['title']}")
    print(f"tags  : {[t['name'] for t in p['tags']]}")
    print(f"private: {p['private']}   body chars: {len(body)}")
    if create_group_target is not None:
        print(f"group_url_name: {p['group_url_name']}")
    elif resend_patch_group and patch_group_target is not None:
        print(
            "group_url_name(patch): "
            f"{p['group_url_name']}   note: PATCH will resend this field (--patch-group-url-name); "
            f"private is still resent from frontmatter ({p['private']})"
        )
    elif item_id and not resend_patch_group:
        shown_target = patch_group_target if patch_group_target is not None else "(none)"
        print(f"group_url_name(frontmatter): {shown_target}   note: PATCH does not resend this field")
    if patch_group_flag and not item_id:
        print(PATCH_GROUP_URL_NAME_CREATE_NOTE)
    if gate_key_error:
        print(f"BLOCKED: {gate_key_error}")
    elif gate_error:
        print(f"BLOCKED: {gate_error}")
    elif gate_value is True:
        print(IGNORE_PUBLISH_WARNING)
    if not item_id and "group_url_name" not in meta:
        print("BLOCKED: GROUP_URL_NAME_BLOCK: Team create requires explicit non-empty group_url_name to avoid implicit sharing defaults.")
    elif not item_id and create_group_target is None:
        print("BLOCKED: GROUP_URL_NAME_BLOCK: Team create requires explicit non-empty group_url_name to avoid implicit sharing defaults.")
    elif resend_patch_group and patch_group_target is None:
        print(f"BLOCKED: {PATCH_GROUP_URL_NAME_BLOCK}")
    if finds:
        print("WARNINGS:")
        for x in finds:
            print(f"  - {x}")
    else:
        print("registration-safe: no findings")
    print("\n(dry-run: nothing sent. add `post <file> --yes` to actually publish.)")
    return 1 if gate_key_error or gate_error or (not item_id and create_group_target is None) or (resend_patch_group and patch_group_target is None) else 0


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
    flag_error = validate_flags(args, allowed_flags={"--yes", "--force-ignore-publish", "--patch-group-url-name"})
    if flag_error:
        print(f"BLOCKED: {flag_error}")
        print("usage: post <file.md> --yes [--force-ignore-publish] [--patch-group-url-name]")
        return 1
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("usage: post <file.md> --yes [--force-ignore-publish] [--patch-group-url-name]")
        return 2
    if len(files) != 1:
        print(f"BLOCKED: exactly one file expected, got {len(files)}")
        print("usage: post <file.md> --yes [--force-ignore-publish] [--patch-group-url-name]")
        return 2
    if "--yes" not in args:
        print("refusing: --yes required (publish is an external action; you give the GO).")
        return cmd_dry_run(files[:1] + (["--patch-group-url-name"] if "--patch-group-url-name" in args else []))
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
    gate_key_error = find_ignore_publish_key_issue(meta)
    if gate_key_error:
        print(f"BLOCKED: {gate_key_error}")
        return 1
    gate_value, gate_error = parse_gate_bool(meta.get("ignorePublish"))
    if gate_error:
        print(f"BLOCKED: {gate_error}")
        return 1
    if gate_value is True:
        print(IGNORE_PUBLISH_WARNING)
        if "--force-ignore-publish" not in args:
            print(IGNORE_PUBLISH_BLOCK)
            return 1
    item_id = real_id(meta)
    create_group_target = explicit_group_target(meta) if not item_id else None
    patch_group_target = explicit_group_target(meta) if item_id else None
    patch_group_flag = wants_patch_group_url_name(args)
    resend_patch_group = bool(item_id and patch_group_flag)
    p = build_payload(meta, body, include_group_url_name=(not item_id) or resend_patch_group)
    if patch_group_flag and not item_id:
        print(PATCH_GROUP_URL_NAME_CREATE_NOTE)
    if not item_id and "group_url_name" not in meta:
        print("BLOCKED: GROUP_URL_NAME_BLOCK: Team create requires explicit non-empty group_url_name to avoid implicit sharing defaults.")
        return 1
    if not item_id and create_group_target is None:
        print("BLOCKED: GROUP_URL_NAME_BLOCK: Team create requires explicit non-empty group_url_name to avoid implicit sharing defaults.")
        return 1
    if resend_patch_group and patch_group_target is None:
        print(f"BLOCKED: {PATCH_GROUP_URL_NAME_BLOCK}")
        return 1
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
