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
  py -3.11 qiita_team_post.py preflight <item_id> [item_id...]
                                                # auth / membership / readable item の共通 gate
  py -3.11 qiita_team_post.py dry-run <file.md> [--patch-group-url-name]
                                                # payload + 警告を表示 (network なし)
  py -3.11 qiita_team_post.py show <item_id>    # read-only Team API GET (visibility readback)
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
DEFAULT_SCAN_STEMS = (
    "QIITA_#28",
    "QIITA_#29",
    "QIITA_#30",
    "QIITA_#31",
    "QIITA_#32",
    "QIITA_#33",
    "QIITA_#34",
    "QIITA_#38",
    "QIITA_#39",
    "QIITA_#40",
    "QIITA_#41",
    "QIITA_#42",
)
DEFAULT_SCAN_STEM_SET = set(DEFAULT_SCAN_STEMS)


# --------------------------------------------------------------------------- #
# token (never hardcoded; env or api-keys.json)
# --------------------------------------------------------------------------- #


def resolve_token() -> tuple[str | None, str | None]:
    t = os.environ.get("QIITA_TEAM_TOKEN")
    if t:
        return t.strip(), "env:QIITA_TEAM_TOKEN"
    for p in (r"D:/api-keys.json", os.path.expanduser("~/api-keys.json")):
        try:
            with open(p, "r", encoding="utf-8-sig") as f:
                d = json.load(f)
            for k in ("qiita_team_token", "QIITA_TEAM_TOKEN", "qiita_token"):
                if d.get(k):
                    return str(d[k]).strip(), f"{p}:{k}"
        except (OSError, ValueError):
            continue
    return None, None


def get_token() -> str | None:
    token, _source = resolve_token()
    return token


def _print_token_source(context: str, source: str | None) -> None:
    if not source:
        return
    print(f"{context}: token_source={source}")
    if source.endswith(":qiita_token"):
        print(f"{context}: WARNING qiita.com personal token fallback is in use; Team auth / membership results may be misleading.")


def _is_personal_token_source(source: str | None) -> bool:
    return bool(source and source.endswith(":qiita_token"))


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


def format_team_visibility(res: dict) -> str:
    group = res.get("group")
    group_url_name = None
    group_private = None
    if isinstance(group, dict):
        group_url_name = group.get("url_name")
        group_private = group.get("private")
    organization_url_name = res.get("organization_url_name")
    return (
        f"private={res.get('private')} "
        f"group.url_name={group_url_name} "
        f"group.private={group_private} "
        f"organization_url_name={organization_url_name}"
    )


IGNORE_PUBLISH_WARNING = "WARNING: frontmatter ignorePublish: true is a qiita-cli gate; Team post requires explicit override."
IGNORE_PUBLISH_BLOCK = "IGNORE_PUBLISH_BLOCK: add --force-ignore-publish only after human approval for this Team POST."
UNRECOGNIZED_IGNORE_PUBLISH_BLOCK = "UNRECOGNIZED_IGNORE_PUBLISH_BLOCK: ignorePublish value '{value}' is not recognized"
UNRECOGNIZED_PRIVATE_BLOCK = "UNRECOGNIZED_PRIVATE_BLOCK: private value '{value}' is not recognized"
PATCH_GROUP_URL_NAME_BLOCK = (
    "PATCH_GROUP_URL_NAME_BLOCK: --patch-group-url-name requires explicit non-empty group_url_name in frontmatter"
)
PATCH_GROUP_URL_NAME_CREATE_NOTE = (
    "note: --patch-group-url-name is a no-op on CREATE (group_url_name is already sent from frontmatter; the flag only adds resend on PATCH/update)"
)
UNKNOWN_FLAG_BLOCK = "UNKNOWN_FLAG_BLOCK: unsupported flag '{flag}'"


def parse_gate_bool(v) -> tuple[bool | None, str | None]:
    # Operator gate values must never silently degrade to an allowed state.
    # Unrecognized values stay blocked until the caller spells them correctly.
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


def parse_private_bool(v, default=True) -> tuple[bool, str | None]:
    if v is None:
        return default, None
    if isinstance(v, bool):
        return v, None
    if isinstance(v, str):
        s = v.strip().lower()
        if not s:
            return default, None
        if s in ("true", "yes", "1"):
            return True, None
        if s in ("false", "no", "0"):
            return False, None
        return False, UNRECOGNIZED_PRIVATE_BLOCK.format(value=v)
    return False, UNRECOGNIZED_PRIVATE_BLOCK.format(value=v)


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


_SCAN_STEM_RE = re.compile(r"(QIITA_#\d+)")


def _all_qiita_stems() -> set[str]:
    stems: set[str] = set()
    for suffix in ("*.md", "*.md.bak"):
        pattern = os.path.join(ARTICLES_DIR, "**", f"QIITA_#*{suffix}")
        for f in _glob.glob(pattern, recursive=True):
            if "archive" in f or ".worktrees" in f:
                continue
            m = _SCAN_STEM_RE.search(os.path.basename(f))
            if m:
                stems.add(m.group(1))
    return stems


def _format_stem_ranges(stems: set[str]) -> str:
    nums = sorted({int(s.split("#", 1)[1]) for s in stems})
    if not nums:
        return "(none)"
    ranges = []
    start = prev = nums[0]
    for n in nums[1:]:
        if n == prev + 1:
            prev = n
            continue
        ranges.append((start, prev))
        start = prev = n
    ranges.append((start, prev))
    parts = []
    for start, end in ranges:
        if start == end:
            parts.append(f"#{start:02d}")
        else:
            parts.append(f"#{start:02d}–{end:02d}")
    return ",".join(parts)


def _format_missing_stems(stems: set[str]) -> str:
    return _format_stem_ranges(stems)


def cmd_scan(args: list[str]) -> int:
    if args:
        patterns = args
        files = []
        seen = set()
        for pattern in patterns:
            for f in sorted(_glob.glob(pattern, recursive=True)):
                if "archive" in f or ".worktrees" in f:
                    continue
                if f in seen:
                    continue
                seen.add(f)
                files.append(f)
        pattern_label = ", ".join(patterns)
    else:
        files = []
        seen = set()
        for stem in DEFAULT_SCAN_STEMS:
            for suffix in (".md", ".md.bak"):
                pattern = os.path.join(ARTICLES_DIR, "**", f"{stem}*{suffix}")
                for f in sorted(_glob.glob(pattern, recursive=True)):
                    if "archive" in f or ".worktrees" in f:
                        continue
                    if f in seen:
                        continue
                    seen.add(f)
                    files.append(f)
        pattern_label = ", ".join(DEFAULT_SCAN_STEMS)
        existing_stems = _all_qiita_stems()
        excluded_stems = existing_stems - DEFAULT_SCAN_STEM_SET
        missing_stems = DEFAULT_SCAN_STEM_SET - existing_stems
    safe = 0
    print(f"scan: {len(files)} files (pattern={pattern_label})\n")
    if not args:
        print(
            "scan coverage: queued "
            f"{len(DEFAULT_SCAN_STEM_SET)} / existing {len(existing_stems)} stem(s); "
            f"excluded {len(excluded_stems)} ({_format_stem_ranges(excluded_stems)}); "
            f"queued-but-missing {len(missing_stems)} ({_format_missing_stems(missing_stems)})\n"
        )
    report = []
    for f in files:
        try:
            text = open(f, "r", encoding="utf-8-sig").read()
        except OSError:
            continue
        meta, body = split_frontmatter(text)
        finds = safety_findings(meta, body)
        base = os.path.basename(f)
        if base.endswith(".md.bak"):
            base = base[:-4]
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
    token, token_source = resolve_token()
    if not token:
        print("NO TOKEN: set env QIITA_TEAM_TOKEN or add qiita_team_token to D:/api-keys.json")
        return 2
    _print_token_source("verify", token_source)
    if _is_personal_token_source(token_source):
        print("verify: BLOCKED personal-token fallback cannot prove Team auth / membership / visibility.")
        print("verify: configure QIITA_TEAM_TOKEN or qiita_team_token before using Team diagnosis output.")
        return 1
    code, body = _req("GET", "/authenticated_user", token)
    if code == 200 and isinstance(body, dict):
        print(f"OK: authenticated as @{body.get('id')} on team '{TEAM}' ({API_BASE})")
        return 0
    print(f"FAIL ({code}): {body}")
    return 1


def _read_item(item_id: str, token: str) -> tuple[int, dict | str]:
    return _req("GET", f"/items/{item_id}", token)


def _format_item_readback(item_id: str, code: int, res: dict | str) -> tuple[bool, str]:
    if code == 401:
        return False, f"AUTH FAIL ({code}): token invalid or expired for team '{TEAM}'"
    if code == 403:
        return False, f"AUTH FAIL ({code}): token lacks scope or membership for team '{TEAM}'"
    if code == 404:
        return False, (
            f"NOT FOUND ({code}): item id={item_id} is not readable on team '{TEAM}' "
            f"(possible delete / wrong team context / private-or-membership mismatch): {res}"
        )
    if code == 200 and isinstance(res, dict):
        res_id = str(res.get("id") or "").strip()
        if res_id != item_id:
            return False, f"FAIL (200): requested id={item_id} but API returned id={res_id or '(missing)'}"
        url = str(res.get("url") or "")
        expected_host = f"https://{TEAM}.qiita.com/"
        if url and not url.startswith(expected_host):
            return False, f"FAIL (200): item url host drifted outside team '{TEAM}': {url}"
        private_value = res.get("private")
        state_hint = "READABLE PRIVATE" if private_value is True else "READABLE"
        return True, (
            f"{state_hint} ({code}): {url}  id={res_id}  "
            f"title={res.get('title')}  {format_team_visibility(res)}"
        )
    return False, f"FAIL ({code}): {res}"


def cmd_preflight(args: list[str]) -> int:
    if not args:
        print("usage: preflight <item_id> [item_id...]")
        return 2
    token, token_source = resolve_token()
    if not token:
        print("NO TOKEN: set env QIITA_TEAM_TOKEN or add qiita_team_token to D:/api-keys.json")
        return 2
    _print_token_source("preflight", token_source)
    if _is_personal_token_source(token_source):
        print("preflight: BLOCKED personal-token fallback cannot prove Team auth / membership / visibility.")
        print("preflight: diagnosis cannot start until QIITA_TEAM_TOKEN or qiita_team_token is configured.")
        return 1
    code, body = _req("GET", "/authenticated_user", token)
    if code != 200 or not isinstance(body, dict):
        print(f"preflight: BLOCKED auth ({code}): {body}")
        print("preflight: diagnosis cannot start until auth / membership / scope are confirmed.")
        return 1
    print(f"preflight auth: OK user=@{body.get('id')} team='{TEAM}'")
    blocked = False
    for raw_item_id in args:
        item_id = raw_item_id.strip()
        code, res = _read_item(item_id, token)
        ok, line = _format_item_readback(item_id, code, res)
        print(f"preflight item: {'OK' if ok else 'BLOCKED'}  {line}")
        blocked = blocked or (not ok)
    if blocked:
        print("preflight: BLOCKED (diagnosis preflight failed; retry after fixing auth / membership / item target)")
        return 1
    print("preflight: OK")
    return 0


def cmd_show(args: list[str]) -> int:
    if len(args) != 1:
        print("usage: show <item_id>")
        return 2
    token, token_source = resolve_token()
    if not token:
        print("NO TOKEN: set env QIITA_TEAM_TOKEN or add qiita_team_token to D:/api-keys.json")
        return 2
    _print_token_source("show", token_source)
    if _is_personal_token_source(token_source):
        print("show: BLOCKED personal-token fallback cannot prove Team visibility on this workspace.")
        print("show: configure QIITA_TEAM_TOKEN or qiita_team_token before trusting readback output.")
        return 1
    item_id = args[0].strip()
    code, res = _read_item(item_id, token)
    ok, line = _format_item_readback(item_id, code, res)
    print(line)
    return 0 if ok else 1


def build_payload(meta: dict, body: str, *, include_group_url_name: bool = False) -> dict:
    private_value, private_error = parse_private_bool(meta.get("private"), default=True)
    if private_error:
        raise ValueError(private_error)
    payload = {
        "title": infer_title(meta, body),
        "body": body,
        "tags": norm_tags(meta),
        "private": private_value,
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
    private_value, private_error = parse_private_bool(meta.get("private"), default=True)
    item_id = real_id(meta)
    create_group_target = explicit_group_target(meta) if not item_id else None
    patch_group_target = explicit_group_target(meta) if item_id else None
    patch_group_flag = wants_patch_group_url_name(args)
    resend_patch_group = bool(item_id and patch_group_flag)
    if private_error:
        print(f"BLOCKED: {private_error}")
        return 1
    p = build_payload(meta, body, include_group_url_name=(not item_id) or resend_patch_group)
    finds = safety_findings(meta, body)
    gate_value, gate_error = parse_gate_bool(meta.get("ignorePublish"))
    gate_key_error = find_ignore_publish_key_issue(meta)
    print(f"action: {'PATCH update id=' + str(item_id) if item_id else 'POST create'} on team '{TEAM}'")
    print(f"title : {p['title']}")
    print(f"tags  : {[t['name'] for t in p['tags']]}")
    print(f"private: {private_value}   body chars: {len(body)}")
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
        preview_rc = cmd_dry_run(files[:1] + (["--patch-group-url-name"] if "--patch-group-url-name" in args else []))
        return 3 if preview_rc == 0 else preview_rc
    token, token_source = resolve_token()
    if not token:
        print("NO TOKEN: set env QIITA_TEAM_TOKEN or add qiita_team_token to D:/api-keys.json")
        return 2
    _print_token_source("post", token_source)
    text = open(files[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    private_value, private_error = parse_private_bool(meta.get("private"), default=True)
    if private_error:
        print(f"BLOCKED: {private_error}")
        return 1
    all_finds = safety_findings(meta, body)
    blocking_finds = [x for x in all_finds if x.startswith(("NO TITLE", "NO TAGS", "OVER CHAR"))]
    if blocking_finds:
        print("BLOCKED (fix first): " + "; ".join(blocking_finds))
        return 1
    warn_finds = [x for x in all_finds if x not in blocking_finds]
    if warn_finds:
        print("WARNINGS:")
        for x in warn_finds:
            print(f"  - {x}")
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
        print(f"OK ({code}): {res.get('url')}  id={res.get('id')}  {format_team_visibility(res)}")
        return 0
    print(f"FAIL ({code}): {res}")
    return 1


def main() -> int:
    _utf8()
    if len(sys.argv) < 2:
        print(__doc__)
        return 0
    cmd, rest = sys.argv[1], sys.argv[2:]
    return {
        "scan": cmd_scan,
        "verify": cmd_verify,
        "preflight": cmd_preflight,
        "dry-run": cmd_dry_run,
        "show": cmd_show,
        "get": cmd_show,
        "post": cmd_post,
    }.get(cmd, lambda a: (print(f"unknown cmd {cmd}"), 2)[1])(rest)


if __name__ == "__main__":
    raise SystemExit(main())
