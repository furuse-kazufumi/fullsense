# SPDX-License-Identifier: Apache-2.0
"""Frontmatter regression tests for Qiita/Zenn helper scripts."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TOOLS_DIR = ROOT / "tools"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


fm = _load("frontmatter_shared", TOOLS_DIR / "_frontmatter.py")
qpp = _load("qiita_public_post", TOOLS_DIR / "qiita_public_post.py")
qtp = _load("qiita_team_post", TOOLS_DIR / "qiita_team_post.py")
qconv = _load("convert_to_qiita_cli", TOOLS_DIR / "qiita-cli-poc" / "convert_to_qiita_cli.py")
zc = _load("zenn_convert", ROOT / "scripts" / "publish" / "zenn_convert.py")


FOLDED_TEXT = """\
---
title: >-
  AI's first line
  second line

  third paragraph
tags:
  - AI
  - 'AI''s'
---
body
"""

LITERAL_TEXT = """\
---
title: 'AI''s title'
notes: |
  line 1

  line 2
tags:
  - AI
  - 'AI''s'
---
body
"""


def test_shared_split_frontmatter_parses_folded_title():
    meta, body = fm.split_frontmatter(FOLDED_TEXT)
    assert meta["title"] == "AI's first line second line\nthird paragraph"
    assert meta["tags"] == ["AI", "AI's"]
    assert body == "body\n"


def test_shared_parser_restores_single_quote_and_literal_block():
    meta = fm.parse_frontmatter_lines(fm.split_frontmatter_lines(LITERAL_TEXT)[0])
    assert meta["title"] == "AI's title"
    assert meta["notes"] == "line 1\n\nline 2"
    assert meta["tags"] == ["AI", "AI's"]


def test_qiita_posters_parse_folded_title_and_tags():
    for mod in (qpp, qtp):
        meta, body = mod.split_frontmatter(FOLDED_TEXT)
        assert meta["title"] == "AI's first line second line\nthird paragraph"
        assert meta["tags"] == ["AI", "AI's"]
        assert body == "body\n"


def test_qiita_public_post_real_public_id_uses_public_id_only():
    assert qpp.real_public_id({"id": "f06ca92ea208c7646fcd"}) is None
    assert qpp.real_public_id({"public_id": "f06ca92ea208c7646fcd"}) == "f06ca92ea208c7646fcd"
    assert qpp.real_public_id({"public_id": " none "}) is None


def test_qiita_public_post_warns_on_legacy_id_without_public_id():
    assert qpp.legacy_id_without_public_id({"id": "team-or-legacy-id"}) == "team-or-legacy-id"
    assert qpp.legacy_id_without_public_id({"id": "legacy", "public_id": "public"}) is None
    assert qpp.legacy_id_without_public_id({"id": " none "}) is None


def test_qiita_public_post_build_payload_uses_public_private_only():
    body = "body\n"
    meta = {"title": "hello", "tags": ["AI"], "private": True}
    payload = qpp.build_payload(meta, body, force_private=None)
    assert payload["private"] is False

    meta_with_public_private = {"title": "hello", "tags": ["AI"], "public_private": True}
    payload = qpp.build_payload(meta_with_public_private, body, force_private=None)
    assert payload["private"] is True

    forced_payload = qpp.build_payload(meta_with_public_private, body, force_private=True)
    assert forced_payload["private"] is True


def test_qiita_public_post_parse_visibility_is_strict():
    assert qpp.parse_visibility("true") == (True, None)
    assert qpp.parse_visibility("false") == (False, None)
    assert qpp.parse_visibility(" yes ") == (True, None)
    assert qpp.parse_visibility("0") == (False, None)
    assert qpp.parse_visibility("ture") == (None, "'ture'")
    assert qpp.parse_visibility("限定共有")[0] is None


def test_qiita_public_post_scan_asset_urls_deduplicates_http_images():
    body = (
        "![a](https://example.test/a.svg \"title\")\n"
        "<img src=\"https://example.test/b.jpg\">\n"
        "![dup](https://example.test/a.svg \"title\")\n"
        "![local](./local.png)\n"
    )
    assert qpp.scan_asset_urls(body) == [
        "https://example.test/a.svg",
        "https://example.test/b.jpg",
    ]


def test_qiita_public_post_scan_asset_urls_handles_single_quote_and_angle_brackets():
    body = (
        "![a](<https://example.test/a path.svg> \"title\")\n"
        "![b](https://example.test/b.jpg 'caption')\n"
    )
    assert qpp.scan_asset_urls(body) == [
        "https://example.test/a path.svg",
        "https://example.test/b.jpg",
    ]


def test_qiita_public_post_privacy_field_findings_require_public_private():
    assert qpp.privacy_field_findings({"private": True}) == [qpp.AMBIGUOUS_PRIVATE_BLOCK]
    assert qpp.privacy_field_findings({"private": True, "public_private": False}) == [qpp.CONFLICTING_PRIVATE_BLOCK]
    assert qpp.privacy_field_findings({"private": False, "public_private": False}) == []
    assert qpp.privacy_field_findings({"private": "ture", "public_private": False}) == [
        qpp.UNRECOGNIZED_VISIBILITY_BLOCK.format(field="private", value="ture")
    ]
    assert qpp.privacy_field_findings({"private": False, "public_private": "限定共有"}) == [
        qpp.UNRECOGNIZED_VISIBILITY_BLOCK.format(field="public_private", value="限定共有")
    ]


def test_qiita_team_post_real_id_treats_nullish_as_absent():
    assert qtp.real_id({"id": "team-item-id"}) == "team-item-id"
    assert qtp.real_id({"id": " none "}) is None
    assert qtp.real_id({"id": " none ", "qiita_item_id": "fallback-id"}) == "fallback-id"
    assert qtp.real_id({"id": "null"}) is None
    assert qtp.real_id({"qiita_item_id": "fallback-id"}) == "fallback-id"


def test_qiita_team_post_build_payload_uses_private_flag_directly():
    body = "body\n"
    private_payload = qtp.build_payload({"title": "hello", "tags": ["AI"], "private": True}, body)
    public_payload = qtp.build_payload({"title": "hello", "tags": ["AI"], "private": False}, body)
    default_payload = qtp.build_payload({"title": "hello", "tags": ["AI"]}, body)

    assert private_payload["private"] is True
    assert public_payload["private"] is False
    assert default_payload["private"] is True


def test_qiita_team_post_build_payload_treats_blank_private_as_default_true():
    body = "body\n"
    payload = qtp.build_payload({"title": "hello", "tags": ["AI"], "private": ""}, body)
    assert payload["private"] is True


def test_qiita_team_post_frontmatter_string_false_maps_to_public():
    text = (
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "---\n"
        "body\n"
    )
    meta, body = qtp.split_frontmatter(text)
    payload = qtp.build_payload(meta, body)
    assert payload["private"] is False


def test_qiita_public_post_dry_run_surfaces_legacy_id_warning(tmp_path, capsys):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "id: legacy-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qpp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "POST create (new public article)" in out
    assert qpp.LEGACY_ID_WARNING_TEMPLATE.format(legacy_id="legacy-id") in out


def test_qiita_public_post_cmd_post_blocks_legacy_id_without_allow_create(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "id: legacy-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    called = {"req": False}

    def _boom(*_args, **_kwargs):
        called["req"] = True
        raise AssertionError("_req should not run without --allow-create")

    monkeypatch.setattr(qpp, "_req", _boom)
    rc = qpp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.LEGACY_ID_WARNING_TEMPLATE.format(legacy_id="legacy-id") in out
    assert qpp.LEGACY_ID_BLOCK in out
    assert called["req"] is False


def test_qiita_public_post_cmd_post_blocks_ambiguous_private_without_public_private(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    called = {"req": False}

    def _boom(*_args, **_kwargs):
        called["req"] = True
        raise AssertionError("_req should not run when visibility is ambiguous")

    monkeypatch.setattr(qpp, "_req", _boom)
    rc = qpp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.AMBIGUOUS_PRIVATE_BLOCK in out
    assert called["req"] is False


def test_qiita_public_post_cmd_post_blocks_unrecognized_public_private(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: ture\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    called = {"req": False}

    def _boom(*_args, **_kwargs):
        called["req"] = True
        raise AssertionError("_req should not run when visibility is invalid")

    monkeypatch.setattr(qpp, "_req", _boom)
    rc = qpp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.UNRECOGNIZED_VISIBILITY_BLOCK.format(field="public_private", value="ture") in out
    assert called["req"] is False


def test_qiita_public_post_cmd_post_allows_legacy_id_with_allow_create(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "id: legacy-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")

    def _fake_req(method, path, token, payload=None):
        assert token == "fake-token"
        if method == "GET":
            assert path == "/authenticated_user"
            return 200, {"id": "furuse-kazufumi"}
        assert method == "POST"
        assert path == "/items"
        assert payload is not None
        assert payload["private"] is False
        return 201, {"id": "new-public-id", "url": "https://example.test/items/new-public-id"}

    monkeypatch.setattr(qpp, "_req", _fake_req)
    rc = qpp.cmd_post([str(path), "--yes", "--allow-create"])
    out = capsys.readouterr().out
    assert rc == 0
    assert qpp.LEGACY_ID_WARNING_TEMPLATE.format(legacy_id="legacy-id") in out
    assert "OK (201) [PUBLIC(一般公開)]" in out


def test_qiita_public_post_preflight_checks_live_and_assets(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_marker: canonical-marker\n"
        "---\n"
        "![img](https://example.test/a.svg)\n",
        encoding="utf-8",
    )

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title> canonical-marker"
        raise AssertionError(f"unexpected URL: {url}")

    def _fake_probe_asset(url):
        if url == "https://example.test/a.svg":
            return 200, {"Content-Type": "image/svg+xml"}
        raise AssertionError(f"unexpected asset URL: {url}")

    def _fake_req(method, path, token, payload=None):
        assert method == "GET"
        assert path == "/authenticated_user"
        assert token == "fake-token"
        return 200, {"id": "furuse-kazufumi"}

    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "_http_probe_asset", _fake_probe_asset)
    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "auth_status: 200" in out
    assert "api_status: 200" in out
    assert "html_status: 200" in out
    assert "marker_present: True" in out
    assert "asset_count: 1" in out
    assert "preflight: OK" in out


def test_qiita_public_post_preflight_requires_marker_when_requested(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_marker: canonical-marker\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path), "--require-marker"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "marker_present: False" in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_blocks_when_marker_required_but_missing_from_frontmatter(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path), "--require-marker"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.PREFLIGHT_MARKER_REQUIRED_BLOCK in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_blocks_without_write_auth(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: None)
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "auth_status: missing-token" in out
    assert qpp.WRITE_AUTH_WARNING in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_blocks_on_api_decode_error(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, "{broken json"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "BLOCKED: API 200 but JSON decode failed" in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_blocks_on_html_404(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 404, {}, "not found"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "html_status: 404" in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_blocks_on_live_title_mismatch(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"different","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>different - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.LIVE_TITLE_BLOCK in out


def test_qiita_public_post_preflight_blocks_on_live_visibility_mismatch(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":true,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.LIVE_VISIBILITY_BLOCK in out


def test_qiita_public_post_preflight_blocks_on_asset_404(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "![img](https://example.test/a.svg)\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    def _fake_probe_asset(url):
        return 404, {"Content-Type": "text/plain"}

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "_http_probe_asset", _fake_probe_asset)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "asset_status: 404" in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_surfaces_ignore_publish_warning(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "ignorePublish: true\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert qpp.IGNORE_PUBLISH_WARNING in out


def test_qiita_public_post_preflight_blocks_unrecognized_ignore_publish(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "ignorePublish: ture\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.UNRECOGNIZED_IGNORE_PUBLISH_BLOCK.format(value="ture") in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_cmd_post_blocks_ignore_publish_without_override(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "ignorePublish: true\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.IGNORE_PUBLISH_WARNING in out
    assert qpp.IGNORE_PUBLISH_BLOCK in out


def test_qiita_public_post_cmd_post_blocks_unrecognized_ignore_publish(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "ignorePublish: ture\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.UNRECOGNIZED_IGNORE_PUBLISH_BLOCK.format(value="ture") in out


def test_qiita_public_post_cmd_post_allows_ignore_publish_with_override(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "ignorePublish: true\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    calls = []

    def _fake_req(method, path, token, payload=None):
        calls.append((method, path))
        if method == "GET":
            return 200, {"id": "furuse-kazufumi"}
        assert method == "PATCH"
        return 200, {"id": "existing-public-id", "url": "https://example.test/items/existing-public-id"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    rc = qpp.cmd_post([str(path), "--yes", "--force-ignore-publish"])
    out = capsys.readouterr().out
    assert rc == 0
    assert ("PATCH", "/items/existing-public-id") in calls
    assert "OK (200) [PUBLIC(一般公開)]" in out


def test_qiita_public_post_post_requires_passing_preflight(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    called = {"req": 0}

    def _fake_req(method, path, token, payload=None):
        called["req"] += 1
        if method == "GET" and path == "/authenticated_user":
            return 200, {"id": "furuse-kazufumi"}
        raise AssertionError("PATCH/POST should not run when preflight blocks")

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"different","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>different - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    rc = qpp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "BLOCKED: post requires a passing preflight before PATCH/POST." in out
    assert called["req"] == 1


def test_qiita_public_post_http_probe_asset_falls_back_after_head_403(monkeypatch):
    calls = []

    class _Resp:
        def __init__(self, status, headers=None):
            self.status = status
            self.headers = headers or {"Content-Type": "image/svg+xml"}

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

    def _fake_urlopen(req, timeout=30):
        calls.append((req.get_method(), req.full_url, req.headers.get("Range")))
        if req.get_method() == "HEAD":
            raise qpp.urllib.error.HTTPError(req.full_url, 403, "forbidden", hdrs={}, fp=None)
        return _Resp(206)

    monkeypatch.setattr(qpp.urllib.request, "urlopen", _fake_urlopen)
    status, _headers = qpp._http_probe_asset("https://example.test/a.svg")
    assert status == 206
    assert calls == [
        ("HEAD", "https://example.test/a.svg", None),
        ("GET", "https://example.test/a.svg", "bytes=0-0"),
    ]


def test_qiita_public_post_preflight_blocks_on_non_image_content_type(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "![img](https://example.test/a.svg)\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    def _fake_probe_asset(url):
        return 200, {"Content-Type": "text/html"}

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "_http_probe_asset", _fake_probe_asset)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.ASSET_CONTENT_TYPE_BLOCK.format(content_type="text/html", url="https://example.test/a.svg") in out


def test_qiita_public_post_safety_findings_uses_normalized_asset_url():
    body = "![a](<https://example.test/a path.svg> \"title\")\n"
    assert qpp.safety_findings({"title": "hello", "tags": ["AI"]}, body) == []


def test_convert_to_qiita_cli_parses_folded_title():
    fm_lines, _body = qconv.split_frontmatter(FOLDED_TEXT)
    meta = qconv.parse_frontmatter(fm_lines)
    assert meta["title"] == "AI's first line second line\nthird paragraph"
    assert meta["tags"] == ["AI", "AI's"]


def test_zenn_convert_parses_folded_title():
    fm_lines, _body = zc.split_frontmatter(FOLDED_TEXT)
    meta = zc.parse_frontmatter(fm_lines)
    assert meta["title"] == "AI's first line second line\nthird paragraph"
    assert meta["tags"] == ["AI", "AI's"]


def test_public_patch_sources_define_public_private_and_match_private():
    public_dir = ROOT / "tools" / "qiita-cli-poc" / "public"
    checked = 0
    for path in sorted(public_dir.glob("*.md")):
        meta, _body = qpp.split_frontmatter(path.read_text(encoding="utf-8-sig"))
        if "public_id" not in meta:
            continue
        checked += 1
        assert "public_private" in meta, f"{path.name} missing public_private"
        private_val, private_bad = qpp.parse_visibility(meta.get("private"))
        public_private_val, public_private_bad = qpp.parse_visibility(meta.get("public_private"))
        assert private_bad is None, f"{path.name} has invalid private: {meta.get('private')!r}"
        assert public_private_bad is None, f"{path.name} has invalid public_private: {meta.get('public_private')!r}"
        assert private_val == public_private_val, f"{path.name} private/public_private mismatch"
    assert checked > 0


def test_qiita37_full_source_has_public_id():
    path = ROOT / "tools" / "qiita-cli-poc" / "public" / "qiita37_gpu_triple_run_gate_price.md"
    meta, _body = qpp.split_frontmatter(path.read_text(encoding="utf-8-sig"))
    assert meta["public_id"] == "6f44575d440a9ebf5228"


def test_qiita37_companion_source_has_public_id_and_remote_baseline():
    path = ROOT / "tools" / "qiita-cli-poc" / "public" / "qiita37_gpu_triple_run_gate_price_kamikudaki.md"
    meta, _body = qpp.split_frontmatter(path.read_text(encoding="utf-8-sig"))
    assert meta["public_id"] == "f06ca92ea208c7646fcd"
    assert meta["preflight_remote_baseline"] == ".remote/f06ca92ea208c7646fcd.md"


def test_qiita_public_post_preflight_blocks_when_remote_baseline_body_is_not_preserved(tmp_path, capsys, monkeypatch):
    remote_dir = tmp_path / ".remote"
    remote_dir.mkdir()
    (remote_dir / "existing-public-id.md").write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "---\n"
        "baseline line 1\n"
        "baseline line 2\n",
        encoding="utf-8",
    )
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_remote_baseline: .remote/existing-public-id.md\n"
        "---\n"
        "baseline line 1\n"
        "extra local line\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "baseline_body_preserved: False" in out
    assert qpp.PREFLIGHT_BASELINE_BODY_BLOCK.format(path=remote_dir / "existing-public-id.md") in out


def test_qiita_public_post_preflight_blocks_remote_baseline_path_escape(tmp_path, capsys, monkeypatch):
    outside = tmp_path / "outside.md"
    outside.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "---\n"
        "outside\n",
        encoding="utf-8",
    )
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_remote_baseline: ../outside.md\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.PREFLIGHT_BASELINE_PATH_BLOCK.format(path="../outside.md") in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_refreshes_remote_baseline_from_live_api(tmp_path, capsys, monkeypatch):
    remote_dir = tmp_path / ".remote"
    remote_dir.mkdir()
    baseline = remote_dir / "existing-public-id.md"
    baseline.write_text(
        "---\n"
        "title: stale\n"
        "tags:\n"
        "  - AI\n"
        "---\n"
        "stale body\n",
        encoding="utf-8",
    )
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_remote_baseline: .remote/existing-public-id.md\n"
        "---\n"
        "live body line 1\n"
        "live body line 2\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        if method == "GET" and path == "/authenticated_user":
            return 200, {"id": "furuse-kazufumi"}
        if method == "GET" and path == "/items/existing-public-id":
            return 200, {
                "id": "existing-public-id",
                "title": "hello",
                "private": False,
                "url": "https://qiita.com/example/items/existing-public-id",
                "updated_at": "2026-06-19T00:00:00+09:00",
                "tags": [{"name": "AI"}],
                "body": "live body line 1\nlive body line 2\n",
            }
        raise AssertionError(f"unexpected _req: {method} {path}")

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path), "--refresh-baseline"])
    out = capsys.readouterr().out
    assert rc == 0
    assert f"baseline_refreshed: {baseline}" in out
    assert "baseline_body_preserved: True" in out
    refreshed = baseline.read_text(encoding="utf-8")
    assert "live body line 1" in refreshed
    assert "public_id: existing-public-id" in refreshed


def test_qiita_public_post_preflight_refresh_does_not_overwrite_baseline_on_live_title_mismatch(tmp_path, capsys, monkeypatch):
    remote_dir = tmp_path / ".remote"
    remote_dir.mkdir()
    baseline = remote_dir / "existing-public-id.md"
    original = (
        "---\n"
        "title: stale\n"
        "tags:\n"
        "  - AI\n"
        "---\n"
        "stale body\n"
    )
    baseline.write_text(original, encoding="utf-8")
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_remote_baseline: .remote/existing-public-id.md\n"
        "---\n"
        "live body line 1\n"
        "live body line 2\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        if method == "GET" and path == "/authenticated_user":
            return 200, {"id": "furuse-kazufumi"}
        if method == "GET" and path == "/items/existing-public-id":
            return 200, {
                "id": "existing-public-id",
                "title": "different live title",
                "private": False,
                "url": "https://qiita.com/example/items/existing-public-id",
                "updated_at": "2026-06-19T00:00:00+09:00",
                "tags": [{"name": "AI"}],
                "body": "live body line 1\nlive body line 2\n",
            }
        raise AssertionError(f"unexpected _req: {method} {path}")

    def _fake_http_get(url, token=None):
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path), "--refresh-baseline"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.LIVE_TITLE_BLOCK in out
    assert "baseline_refreshed:" not in out
    assert baseline.read_text(encoding="utf-8") == original


def test_qiita_public_post_preflight_preserves_blank_lines_in_baseline_check(tmp_path, capsys, monkeypatch):
    remote_dir = tmp_path / ".remote"
    remote_dir.mkdir()
    (remote_dir / "existing-public-id.md").write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "---\n"
        "line 1\n"
        "\n"
        "line 2\n",
        encoding="utf-8",
    )
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_remote_baseline: .remote/existing-public-id.md\n"
        "---\n"
        "line 1\n"
        "line 2\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "baseline_body_preserved: False" in out
    assert qpp.PREFLIGHT_BASELINE_BODY_BLOCK.format(path=remote_dir / "existing-public-id.md") in out


def test_qiita_public_post_preflight_blocks_when_asset_content_type_is_missing(tmp_path, capsys, monkeypatch):
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "---\n"
        "![a](https://example.test/a.svg)\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id"}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    def _fake_probe_asset(url):
        assert url == "https://example.test/a.svg"
        return 200, {}

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "_http_probe_asset", _fake_probe_asset)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.ASSET_CONTENT_TYPE_BLOCK.format(content_type="", url="https://example.test/a.svg") in out
