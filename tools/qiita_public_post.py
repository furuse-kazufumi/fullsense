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
  py -3.11 qiita_public_post.py preflight <file.md>          # dry-run + live/API/assets 事前確認
  py -3.11 qiita_public_post.py preflight <file.md> --refresh-baseline  # live API 本文で .remote baseline を更新
  py -3.11 qiita_public_post.py preflight <file.md> --require-marker  # live HTML に marker 反映まで要求
  py -3.11 qiita_public_post.py post <file.md> --yes         # 実 POST/PATCH (private=false)
  py -3.11 qiita_public_post.py post <file.md> --yes --private   # 限定共有で投稿
  py -3.11 qiita_public_post.py post <file.md> --yes --allow-create  # `public_id` 無し create を明示許可
  py -3.11 qiita_public_post.py post <file.md> --yes --force-ignore-publish  # ignorePublish:true を override
"""
from __future__ import annotations

import json
import os
from pathlib import Path
import re
import sys
import urllib.error
import urllib.parse
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
UNRECOGNIZED_IGNORE_PUBLISH_BLOCK = (
    "BLOCKED: frontmatter ignorePublish: has unrecognized gate value {value!r}. "
    "Use true/false (or yes/no/1/0)."
)
WRITE_AUTH_WARNING = (
    "WARNING: preflight does not prove PATCH auth unless /authenticated_user succeeds. "
    "Run `verify` or use preflight with a valid token before posting."
)
IGNORE_PUBLISH_WARNING = (
    "WARNING: frontmatter ignorePublish: true is a qiita-cli gate, not a qiita_public_post.py gate."
)
IGNORE_PUBLISH_BLOCK = (
    "BLOCKED: frontmatter ignorePublish: true requires --force-ignore-publish before qiita_public_post.py can send."
)
LIVE_TITLE_BLOCK = (
    "BLOCKED: live title differs from payload title. Resolve live-only edits or align source before PATCH."
)
LIVE_VISIBILITY_BLOCK = (
    "BLOCKED: live private visibility differs from payload visibility. Resolve before PATCH."
)
PREFLIGHT_MARKER_REQUIRED_BLOCK = (
    "BLOCKED: --require-marker was requested but frontmatter preflight_marker: is missing."
)
PREFLIGHT_BASELINE_REQUIRED_BLOCK = (
    "BLOCKED: frontmatter preflight_remote_baseline: is set but baseline file is missing or unreadable: {path}"
)
PREFLIGHT_BASELINE_PATH_BLOCK = (
    "BLOCKED: frontmatter preflight_remote_baseline: must be a direct child of .remote/ and may not escape: {path}"
)
PREFLIGHT_BASELINE_BODY_BLOCK = (
    "BLOCKED: local body no longer preserves the required remote baseline body sequence: {path}"
)
ASSET_CONTENT_TYPE_BLOCK = (
    "BLOCKED: asset does not look like an image content-type: {content_type!r} ({url})"
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


def parse_gate_bool(v) -> tuple[bool | None, str | None]:
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
    for raw in scan_image_targets(body):
        url = _strip_markdown_title(raw)
        if not url.startswith("http"):
            out.append(f"NON-PUBLIC IMAGE: {raw[:80]} (public URL か Qiita 直アップが必要)")
    if _LOCALPATH_RE.search(body):
        out.append("LOCAL PATH in body (D:\\ や ./ — feedback_no_local_path_in_public)")
    return out


def _strip_markdown_title(raw: str) -> str:
    raw = raw.strip()
    if raw.startswith("<"):
        end = raw.find(">")
        if end != -1:
            head = raw[1:end].strip()
            if head.startswith(("http://", "https://")):
                return head
    m = re.match(r"^(https?://\S+?)(?:\s+['\"].*)?$", raw)
    if m:
        return m.group(1).strip()
    return raw.strip()


def scan_image_targets(body: str) -> list[str]:
    targets: list[str] = []
    seen: set[str] = set()
    for m in _IMG_RE.finditer(body):
        raw = (m.group(1) or m.group(2) or "").strip()
        if not raw or raw in seen:
            continue
        seen.add(raw)
        targets.append(raw)
    return targets


def scan_asset_urls(body: str) -> list[str]:
    urls: list[str] = []
    seen: set[str] = set()
    for raw in scan_image_targets(body):
        url = _strip_markdown_title(raw)
        if not url.startswith("http"):
            continue
        if url in seen:
            continue
        seen.add(url)
        urls.append(url)
    return urls


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


def _http_get(url: str, token: str | None = None) -> tuple[int, dict[str, str], str]:
    req = urllib.request.Request(url, method="GET")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read().decode("utf-8", errors="replace")
            return r.status, dict(r.headers.items()), data
    except urllib.error.HTTPError as e:
        data = e.read().decode("utf-8", errors="replace")
        return e.code, dict(e.headers.items()) if e.headers else {}, data
    except urllib.error.URLError as e:
        return 0, {}, f"URLError: {e}"


def _http_probe_asset(url: str) -> tuple[int, dict[str, str]]:
    req = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, dict(r.headers.items())
    except urllib.error.HTTPError as e:
        if e.code not in (400, 403, 405, 501):
            return e.code, dict(e.headers.items()) if e.headers else {}
    except urllib.error.URLError:
        pass

    req = urllib.request.Request(url, method="GET")
    req.add_header("Range", "bytes=0-0")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, dict(r.headers.items())
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers.items()) if e.headers else {}
    except urllib.error.URLError:
        return 0, {}


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


def _normalize_body_lines(body: str) -> list[str]:
    return body.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def _is_line_subsequence(needles: list[str], haystack: list[str]) -> bool:
    if not needles:
        return True
    i = 0
    for line in haystack:
        if line == needles[i]:
            i += 1
            if i == len(needles):
                return True
    return False


def _yaml_quote_single(v: str) -> str:
    return "'" + v.replace("'", "''") + "'"


def _resolve_baseline_path(meta: dict, source_path: str) -> tuple[Path | None, str | None]:
    rel = str(meta.get("preflight_remote_baseline") or "").strip()
    if not rel:
        return None, None
    source_dir = Path(source_path).resolve().parent
    allowed_dir = (source_dir / ".remote").resolve()
    rel_path = Path(rel)
    base_path = (source_dir / rel_path).resolve()
    rel_norm = rel.replace("\\", "/")
    if rel_path.is_absolute() or ".." in rel_path.parts or not rel_norm.startswith(".remote/") or base_path.parent != allowed_dir:
        return None, PREFLIGHT_BASELINE_PATH_BLOCK.format(path=rel)
    return base_path, None


def _refresh_remote_baseline(meta: dict, source_path: str, payload: dict, token: str | None) -> tuple[list[str], bool]:
    path, err = _resolve_baseline_path(meta, source_path)
    if not path:
        return ([err] if err else []), bool(err)
    pid = real_public_id(meta)
    if not pid:
        return ["baseline_refresh: skipped (no public_id)"], False
    if not token:
        return ["baseline_refresh: skipped (missing token)"], True
    code, res = _req("GET", f"/items/{pid}", token)
    if code != 200 or not isinstance(res, dict):
        return [f"baseline_refresh_status: {code}", "BLOCKED: failed to refresh live baseline via API"], True
    body = str(res.get("body") or "")
    title = str(res.get("title") or "")
    tags = res.get("tags") or []
    private = bool(res.get("private"))
    live_url = str(res.get("url") or "")
    live_id = str(res.get("id") or "")
    updated_at = str(res.get("updated_at") or "")
    report_lines = [f"baseline_refresh_status: {code}"]
    report_lines.append(f"baseline_refresh_api_id: {live_id}")
    report_lines.append(f"baseline_refresh_title: {title}")
    report_lines.append(f"baseline_refresh_private: {private}")
    report_lines.append(f"baseline_refresh_url: {live_url}")
    blocked = False
    if live_id and live_id != pid:
        blocked = True
        report_lines.append("BLOCKED: live baseline refresh returned a different item id")
    if title != str(payload["title"]):
        blocked = True
        report_lines.append(LIVE_TITLE_BLOCK)
    if private != bool(payload["private"]):
        blocked = True
        report_lines.append(LIVE_VISIBILITY_BLOCK)
    if not live_url:
        blocked = True
        report_lines.append("BLOCKED: live baseline refresh returned no live URL")
    else:
        html_status, _html_headers, html_text = _http_get(live_url)
        report_lines.append(f"baseline_refresh_html_status: {html_status}")
        if html_status != 200:
            blocked = True
        preflight_marker = str(meta.get("preflight_marker") or "").strip()
        if preflight_marker:
            report_lines.append(f"baseline_refresh_marker_present: {preflight_marker in html_text}")
    if blocked:
        return report_lines, True

    baseline_lines = ["---", f"title: {_yaml_quote_single(title)}", "tags:"]
    for tag in tags:
        name = str((tag or {}).get("name") or "").strip()
        if name:
            baseline_lines.append(f"  - {name}")
    baseline_lines.extend([
        f"private: {'true' if private else 'false'}",
        f"public_private: {'true' if private else 'false'}",
    ])
    if updated_at:
        baseline_lines.append(f"updated_at: {_yaml_quote_single(updated_at)}")
    baseline_lines.extend([
        f"id: {pid}",
        f"public_id: {pid}",
        "---",
        body,
    ])
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text("\n".join(baseline_lines).rstrip("\n") + "\n", encoding="utf-8")
    tmp_path.replace(path)
    report_lines.append(f"baseline_refreshed: {path}")
    return report_lines, False


def _baseline_body_report(meta: dict, body: str, source_path: str) -> tuple[list[str], bool]:
    path, err = _resolve_baseline_path(meta, source_path)
    if not path:
        return ([err] if err else []), bool(err)
    try:
        text = path.read_text(encoding="utf-8-sig")
        _base_meta, base_body = split_frontmatter(text)
    except (OSError, ValueError):
        lines = [f"baseline_path: {path}", PREFLIGHT_BASELINE_REQUIRED_BLOCK.format(path=path)]
        return lines, True
    lines = [f"baseline_path: {path}"]
    ok = _is_line_subsequence(_normalize_body_lines(base_body), _normalize_body_lines(body))
    lines.append(f"baseline_body_preserved: {ok}")
    if not ok:
        lines.append(PREFLIGHT_BASELINE_BODY_BLOCK.format(path=path))
    return lines, not ok


def _preflight_report(meta: dict, body: str, payload: dict, require_marker: bool, source_path: str) -> tuple[list[str], bool]:
    lines: list[str] = []
    finds = safety_findings(meta, body)
    privacy_finds = privacy_field_findings(meta)
    pid = real_public_id(meta)
    legacy_id = legacy_id_without_public_id(meta)
    asset_urls = scan_asset_urls(body)
    preflight_marker = str(meta.get("preflight_marker") or "").strip()
    blocked = bool(finds or privacy_finds)

    lines.append(f"target: PUBLIC qiita.com ({API_BASE})")
    lines.append(f"action: {'PATCH update public_id=' + str(pid) if pid else 'POST create (new public article)'}")
    lines.append(f"title : {payload['title']}")
    lines.append(f"tags  : {[t['name'] for t in payload['tags']]}")
    lines.append(f"private: {payload['private']}   body chars: {len(body)}")
    baseline_lines, baseline_blocked = _baseline_body_report(meta, body, source_path)
    lines.extend(baseline_lines)
    blocked = blocked or baseline_blocked
    if legacy_id:
        lines.append(LEGACY_ID_WARNING_TEMPLATE.format(legacy_id=legacy_id))
    ignore_publish, ignore_publish_bad = parse_gate_bool(meta.get("ignorePublish"))
    if ignore_publish_bad is not None:
        blocked = True
        lines.append(UNRECOGNIZED_IGNORE_PUBLISH_BLOCK.format(value=meta.get("ignorePublish")))
    elif ignore_publish:
        lines.append(IGNORE_PUBLISH_WARNING)
    lines.extend(privacy_finds)
    if finds:
        lines.append("WARNINGS:")
        lines.extend([f"  - {x}" for x in finds])
    else:
        lines.append("registration-safe: no findings")

    auth_ok = False
    auth_token = get_token()
    if auth_token:
        auth_code, _auth_body = _req("GET", "/authenticated_user", auth_token)
        lines.append(f"auth_status: {auth_code}")
        auth_ok = auth_code == 200
        if not auth_ok:
            blocked = True
            lines.append(WRITE_AUTH_WARNING)
    else:
        lines.append("auth_status: missing-token")
        blocked = True
        lines.append(WRITE_AUTH_WARNING)
    if not pid:
        lines.append("live-check: skipped (no public_id; create path has no existing live item)")
    else:
        api_status, _api_headers, api_text = _http_get(f"{API_BASE}/items/{pid}", token=auth_token)
        lines.append(f"api_status: {api_status}")
        live_url = ""
        if api_status == 200:
            try:
                api_obj = json.loads(api_text)
                live_url = str(api_obj.get("url") or "")
                api_title = str(api_obj.get("title") or "")
                live_private = bool(api_obj.get("private"))
                lines.append(f"api_title: {api_title}")
                lines.append(f"api_url  : {live_url}")
                lines.append(f"api_private: {live_private}")
                if api_title != str(payload["title"]):
                    blocked = True
                    lines.append(LIVE_TITLE_BLOCK)
                if live_private != bool(payload["private"]):
                    blocked = True
                    lines.append(LIVE_VISIBILITY_BLOCK)
            except json.JSONDecodeError:
                blocked = True
                lines.append("BLOCKED: API 200 but JSON decode failed")
        else:
            blocked = True
        if live_url:
            html_status, _html_headers, html_text = _http_get(live_url)
            lines.append(f"html_status: {html_status}")
            if html_status == 200:
                start = html_text.find("<title>")
                end = html_text.find("</title>", start)
                if start != -1 and end != -1:
                    html_title = html_text[start + 7:end]
                    lines.append(f"html_title: {html_title}")
                if preflight_marker:
                    marker_ok = preflight_marker in html_text
                    lines.append(f"marker_present: {marker_ok}")
                    if require_marker and not marker_ok:
                        blocked = True
                elif require_marker:
                    blocked = True
                    lines.append(PREFLIGHT_MARKER_REQUIRED_BLOCK)
            else:
                blocked = True
        else:
            blocked = True

    lines.append(f"asset_count: {len(asset_urls)}")
    for url in asset_urls:
        code, headers = _http_probe_asset(url)
        content_type = headers.get("Content-Type", "")
        lines.append(f"asset_status: {code}  content-type={content_type}  url={url}")
        if code not in (200, 206):
            blocked = True
            continue
        if not content_type or not content_type.lower().startswith("image/"):
            blocked = True
            lines.append(ASSET_CONTENT_TYPE_BLOCK.format(content_type=content_type, url=url))
    return lines, blocked


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


def cmd_preflight(args: list[str]) -> int:
    files = [a for a in args if not a.startswith("--")]
    if not files:
        print("usage: preflight <file.md>")
        return 2
    force_private = True if "--private" in args else None
    require_marker = "--require-marker" in args
    text = open(files[0], "r", encoding="utf-8-sig").read()
    meta, body = split_frontmatter(text)
    p = build_payload(meta, body, force_private)
    if "--refresh-baseline" in args:
        refresh_lines, refresh_blocked = _refresh_remote_baseline(meta, files[0], p, get_token())
        for line in refresh_lines:
            print(line)
        if refresh_blocked:
            print("preflight: BLOCKED")
            return 1
    lines, blocked = _preflight_report(meta, body, p, require_marker=require_marker, source_path=files[0])
    for line in lines:
        print(line)
    if blocked:
        print("preflight: BLOCKED")
        return 1
    print("preflight: OK")
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
        print("usage: post <file.md> --yes [--private] [--allow-create] [--force-ignore-publish]")
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
    ignore_publish, ignore_publish_bad = parse_gate_bool(meta.get("ignorePublish"))
    if ignore_publish_bad is not None:
        print(UNRECOGNIZED_IGNORE_PUBLISH_BLOCK.format(value=meta.get("ignorePublish")))
        return 1
    if ignore_publish and "--force-ignore-publish" not in args:
        print(IGNORE_PUBLISH_WARNING)
        print(IGNORE_PUBLISH_BLOCK)
        return 1
    preflight_lines, preflight_blocked = _preflight_report(meta, body, p, require_marker=False, source_path=files[0])
    for line in preflight_lines:
        print(line)
    if preflight_blocked:
        print("BLOCKED: post requires a passing preflight before PATCH/POST.")
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
    return {"verify": cmd_verify, "dry-run": cmd_dry_run, "preflight": cmd_preflight, "post": cmd_post}.get(
        cmd, lambda a: (print(f"unknown cmd {cmd}"), 2)[1])(rest)


if __name__ == "__main__":
    raise SystemExit(main())
