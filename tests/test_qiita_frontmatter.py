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


def test_qiita_public_post_privacy_field_findings_require_public_private():
    assert qpp.privacy_field_findings({"private": True}) == [qpp.AMBIGUOUS_PRIVATE_BLOCK]
    assert qpp.privacy_field_findings({"private": True, "public_private": False}) == [qpp.CONFLICTING_PRIVATE_BLOCK]
    assert qpp.privacy_field_findings({"private": False, "public_private": False}) == []


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

    def _fake_req(method, path, token, payload):
        assert method == "POST"
        assert path == "/items"
        assert token == "fake-token"
        assert payload["private"] is False
        return 201, {"id": "new-public-id", "url": "https://example.test/items/new-public-id"}

    monkeypatch.setattr(qpp, "_req", _fake_req)
    rc = qpp.cmd_post([str(path), "--yes", "--allow-create"])
    out = capsys.readouterr().out
    assert rc == 0
    assert qpp.LEGACY_ID_WARNING_TEMPLATE.format(legacy_id="legacy-id") in out
    assert "OK (201) [PUBLIC(一般公開)]" in out


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
