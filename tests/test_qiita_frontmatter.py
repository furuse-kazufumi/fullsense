# SPDX-License-Identifier: Apache-2.0
"""Frontmatter regression tests for Qiita/Zenn helper scripts."""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest


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


def _public_root() -> Path:
    return TOOLS_DIR / "qiita-cli-poc" / "public"


@pytest.fixture(autouse=True)
def _allow_marker_paths_in_cmd_post_tests(request, monkeypatch):
    if "cmd_post" in request.node.name:
        monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)


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


def test_shared_split_frontmatter_preserves_crlf_body():
    text = "---\r\ntitle: hello\r\ntags: [a]\r\n---\r\n# body\r\nline2\r\n"
    meta, body = fm.split_frontmatter(text)
    assert meta["title"] == "hello"
    assert meta["tags"] == ["a"]
    assert body == "# body\r\nline2\r\n"


def test_shared_split_frontmatter_allows_whitespace_around_delimiters():
    text = "  ---  \n" "title: hello\n" "tags: [a]\n" " --- \n" "# body\n"
    meta, body = fm.split_frontmatter(text)
    assert meta["title"] == "hello"
    assert meta["tags"] == ["a"]
    assert body == "# body\n"


def test_shared_split_frontmatter_keeps_empty_frontmatter_and_body_newline():
    text = "---\n---\n\n# body\n"
    meta, body = fm.split_frontmatter(text)
    assert meta == {}
    assert body == "\n# body\n"


def test_shared_inline_list_preserves_double_quote_escape_and_following_item():
    # Regression: a backslash-escaped quote inside a double-quoted inline-list
    # item must not toggle quote tracking off early. Before the fix,
    # `["a\"b", x]` mis-tracked the closing quote and dropped the `x` element.
    assert fm.parse_inline_list_value(r'["a\"b", x]') == ['a"b', "x"]
    # Plain / single-quote-escaped / unescaped-double forms stay intact.
    assert fm.parse_inline_list_value("[a, b, c]") == ["a", "b", "c"]
    assert fm.parse_inline_list_value("['a''b', x]") == ["a'b", "x"]
    assert fm.parse_inline_list_value('["ab", "cd"]') == ["ab", "cd"]


def test_shared_parser_keeps_unquoted_title_hash_literal():
    text = "---\n" "title: QIITA #24 observability governance\n" "---\n" "# body\n"
    meta, body = fm.split_frontmatter(text)
    assert meta["title"] == "QIITA #24 observability governance"
    assert body == "# body\n"


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


def test_qiita_public_post_infer_title_prefers_frontmatter_title_over_body_h1():
    meta = {"title": "Old frontmatter title"}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    assert qpp.infer_title(meta, body) == "Old frontmatter title"


def test_qiita_public_post_infer_title_falls_back_to_frontmatter_without_publish_h1():
    meta = {"title": "Frontmatter title"}
    body = "body only\n"
    assert qpp.infer_title(meta, body) == "Frontmatter title"


def test_qiita_public_post_safety_findings_do_not_block_title_mismatch_without_path_context():
    meta = {"title": "Old frontmatter title", "tags": ["AI"], "public_private": False}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    assert qpp.TITLE_MISMATCH_BLOCK not in qpp.safety_findings(meta, body)


def test_qiita_public_post_build_payload_uses_frontmatter_title_when_present():
    meta = {"title": "Old frontmatter title", "tags": ["AI"], "public_private": False}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    payload = qpp.build_payload(meta, body, force_private=None)
    assert payload["title"] == "Old frontmatter title"


def test_qiita_public_post_infer_title_ignores_fenced_code_headings():
    meta = {"title": "Fallback frontmatter title"}
    body = (
        "```md\n"
        "# Fake title in code\n"
        "```\n\n"
        "# 日本語\n\n"
        "```python\n"
        "# Another fake title\n"
        "```\n\n"
        "# Visible publish title\n"
    )
    assert qpp.infer_title(meta, body) == "Fallback frontmatter title"


def test_qiita_public_post_infer_title_respects_longer_backtick_fence_length():
    meta = {"title": "Fallback frontmatter title"}
    body = (
        "````md\n"
        "```inside\n"
        "# Fake title in code\n"
        "```\n"
        "````\n\n"
        "# 日本語\n\n"
        "# Visible publish title\n"
    )
    assert qpp.infer_title(meta, body) == "Fallback frontmatter title"


def test_qiita_public_post_infer_title_skips_multiple_language_headings():
    meta = {"title": "Fallback frontmatter title"}
    body = "# English\n\n# 日本語\n\n# Visible publish title\n"
    assert qpp.infer_title(meta, body) == "Fallback frontmatter title"


def test_qiita_public_post_title_mismatch_compat_blocks_when_frontmatter_publish_title_changed(monkeypatch):
    meta = {"title": "Old frontmatter title", "public_id": "abc123", "tags": ["AI"], "public_private": False}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    baseline = (
        "---\n"
        "title: Legacy frontmatter title\n"
        "public_id: abc123\n"
        "tags: [AI]\n"
        "---\n"
        "# 日本語\n\n# New publish title\n"
    )
    monkeypatch.setattr(qpp, "_load_baseline_text", lambda path: baseline)
    assert qpp._should_block_title_mismatch(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md", meta, body) is True


def _write_title_mismatch_source(tmp_path: Path) -> Path:
    # frontmatter title differs from the body publish H1, with a live public_id.
    path = tmp_path / "mismatch.md"
    path.write_text(
        "---\n"
        "title: Old frontmatter title\n"
        "public_id: abc123\n"
        "tags: [AI]\n"
        "public_private: false\n"
        "---\n"
        "# 日本語\n\n# New publish title\n\nbody\n",
        encoding="utf-8",
    )
    return path


def test_qiita_public_post_dry_run_surfaces_title_mismatch_block(tmp_path, capsys, monkeypatch):
    # Regression: dry-run must surface the same title-mismatch block as post so
    # a clean dry-run/preflight actually predicts a clean post.
    monkeypatch.setattr(qpp, "_load_baseline_text", lambda path: None)
    path = _write_title_mismatch_source(tmp_path)
    rc = qpp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 0  # dry-run is a preview; it warns rather than exits non-zero
    assert qpp.TITLE_MISMATCH_BLOCK in out


def test_qiita_public_post_preflight_blocks_title_mismatch(tmp_path, capsys, monkeypatch):
    # Regression: preflight OK must guarantee the post-time title guard passes.
    # Previously only cmd_post ran the title check, so a title mismatch could
    # pass preflight and then fail post.
    monkeypatch.setattr(qpp, "_load_baseline_text", lambda path: None)
    monkeypatch.setattr(qpp, "_preflight_report", lambda *a, **k: ([], False))
    path = _write_title_mismatch_source(tmp_path)
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.TITLE_MISMATCH_BLOCK in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_refresh_baseline_not_run_on_title_mismatch(tmp_path, capsys, monkeypatch):
    # Fail-closed regression: a title-mismatch source that will ultimately BLOCK
    # must NOT trigger the `.remote` baseline write, even with --refresh-baseline.
    calls = []
    monkeypatch.setattr(qpp, "_load_baseline_text", lambda path: None)
    monkeypatch.setattr(
        qpp, "_refresh_remote_baseline",
        lambda *a, **k: (calls.append(a) or (["REFRESHED"], False)),
    )
    monkeypatch.setattr(qpp, "_preflight_report", lambda *a, **k: ([], False))
    monkeypatch.setattr(qpp, "get_token", lambda: "tok")
    path = _write_title_mismatch_source(tmp_path)
    rc = qpp.cmd_preflight([str(path), "--refresh-baseline"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.TITLE_MISMATCH_BLOCK in out
    assert "preflight: BLOCKED" in out
    assert calls == []  # baseline refresh side effect never fired


def test_qiita_public_post_preflight_ok_when_titles_align(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qpp, "_load_baseline_text", lambda path: None)
    monkeypatch.setattr(qpp, "_preflight_report", lambda *a, **k: ([], False))
    path = tmp_path / "aligned.md"
    path.write_text(
        "---\n"
        "public_id: abc123\n"
        "tags: [AI]\n"
        "public_private: false\n"
        "---\n"
        "# Publish title\n\nbody\n",
        encoding="utf-8",
    )
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "preflight: OK" in out


def test_qiita_public_post_live_identity_uses_public_id_only():
    assert qpp._has_live_identity({"public_id": "abc123"}) is True
    assert qpp._has_live_identity({"id": "team-only-id"}) is False
    assert qpp._has_live_identity({"public_id": " null "}) is False


def test_qiita_public_post_title_mismatch_compat_blocks_new_publish_title_change_on_live_item(monkeypatch):
    meta = {"title": "Old frontmatter title", "public_id": "abc123", "tags": ["AI"], "public_private": False}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    baseline = (
        "---\n"
        "title: Legacy frontmatter title\n"
        "public_id: abc123\n"
        "tags: [AI]\n"
        "---\n"
        "# 日本語\n\n# Old publish title\n"
    )
    monkeypatch.setattr(qpp, "_load_baseline_text", lambda path: baseline)
    assert qpp._should_block_title_mismatch(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md", meta, body) is True


def test_qiita_public_post_tag_signatures_normalize_case_and_commas():
    meta = {"tags": ["AI, FullSense", "llcore", "AI"]}
    payload = {"tags": [{"name": "ai"}, {"name": "FULLSENSE"}, {"name": "llcore"}]}
    api_tags = [{"name": "AI"}, {"name": "fullsense"}, {"name": "LLCORE"}]

    expected = ("ai", "fullsense", "llcore")
    assert qpp._tag_name_signature_from_meta(meta) == expected
    assert qpp._tag_name_signature_from_payload(payload) == expected
    assert qpp._tag_name_signature_from_api(api_tags) == expected


def test_qiita_public_post_norm_tags_preserves_case_and_dedups_case_insensitively():
    meta = {"tags": ["AI, FullSense", "fullsense", "llcore", "AI"]}
    assert qpp.norm_tags(meta) == [
        {"name": "AI", "versions": []},
        {"name": "FullSense", "versions": []},
        {"name": "llcore", "versions": []},
    ]


def test_qiita_public_post_norm_tags_excludes_todo_tag_placeholder():
    meta = {"tags": ["TODO_TAG", "AI", "TODO_TAG"]}
    assert qpp.norm_tags(meta) == [
        {"name": "AI", "versions": []},
    ]


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


def test_qiita_team_post_infer_title_prefers_frontmatter_title_over_body_h1():
    meta = {"title": "Old frontmatter title"}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    assert qtp.infer_title(meta, body) == "Old frontmatter title"


def test_qiita_team_post_safety_findings_do_not_block_title_mismatch_without_path_context():
    meta = {"title": "Old frontmatter title", "tags": ["AI"], "private": False}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    assert qtp.TITLE_MISMATCH_BLOCK not in qtp.safety_findings(meta, body)


def test_qiita_team_post_build_payload_uses_frontmatter_title_when_present():
    meta = {"title": "Old frontmatter title", "tags": ["AI"], "private": False}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    payload = qtp.build_payload(meta, body)
    assert payload["title"] == "Old frontmatter title"


def test_qiita_team_post_build_payload_preserves_group_url_name():
    body = "body\n"
    payload = qtp.build_payload(
        {"title": "hello", "tags": ["AI"], "private": False, "group_url_name": "general"},
        body,
        include_group_url_name=True,
    )
    assert payload["group_url_name"] == "general"


def test_qiita_team_post_title_mismatch_compat_blocks_when_frontmatter_publish_title_changed(monkeypatch):
    meta = {"title": "Old frontmatter title", "id": "team-id-123", "tags": ["AI"], "private": False}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    baseline = (
        "---\n"
        "title: Legacy frontmatter title\n"
        "id: team-id-123\n"
        "tags: [AI]\n"
        "---\n"
        "# 日本語\n\n# New publish title\n"
    )
    monkeypatch.setattr(qtp, "_load_baseline_text", lambda path: baseline)
    assert qtp._should_block_title_mismatch(r"D:\projects\fullsense\docs\articles\QIITA_#02_cognitive_factors.md", meta, body) is True


def test_qiita_team_post_live_identity_uses_team_id_only():
    assert qtp._has_live_identity({"id": "team-id-123"}) is True
    assert qtp._has_live_identity({"public_id": "public-only-id"}) is False
    assert qtp._has_live_identity({"id": " none "}) is False


def test_qiita_team_post_title_mismatch_compat_blocks_new_publish_title_change_on_live_item(monkeypatch):
    meta = {"title": "Old frontmatter title", "id": "team-id-123", "tags": ["AI"], "private": False}
    body = "# 日本語\n\n# New publish title\n\nbody\n"
    baseline = (
        "---\n"
        "title: Legacy frontmatter title\n"
        "id: team-id-123\n"
        "tags: [AI]\n"
        "---\n"
        "# 日本語\n\n# Old publish title\n"
    )
    monkeypatch.setattr(qtp, "_load_baseline_text", lambda path: baseline)
    assert qtp._should_block_title_mismatch(r"D:\projects\fullsense\docs\articles\QIITA_#02_cognitive_factors.md", meta, body) is True


def test_qiita_team_post_build_payload_skips_group_url_name_without_create_intent():
    body = "body\n"
    payload = qtp.build_payload(
        {"title": "hello", "tags": ["AI"], "private": False, "group_url_name": "general"},
        body,
    )
    assert "group_url_name" not in payload


def test_qiita_team_post_build_payload_treats_blank_private_as_default_true():
    body = "body\n"
    payload = qtp.build_payload({"title": "hello", "tags": ["AI"], "private": ""}, body)
    assert payload["private"] is True


def test_qiita_team_post_build_payload_blocks_unrecognized_private_value():
    body = "body\n"
    try:
        qtp.build_payload({"title": "hello", "tags": ["AI"], "private": "ture"}, body)
    except ValueError as e:
        assert "UNRECOGNIZED_PRIVATE_BLOCK" in str(e)
    else:
        raise AssertionError("expected ValueError for malformed private")


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


def test_qiita_team_post_dry_run_blocks_unrecognized_private_value(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: ture\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out

    assert rc == 1
    assert "UNRECOGNIZED_PRIVATE_BLOCK" in out


def test_qiita_team_post_invalidate_marker_writes_false_and_exits_zero(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_invalidate_marker([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert f"marker invalidated: {path}" in out
    assert "qiita_team_verified: false" in path.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_blocks_without_frontmatter_marker(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "plain.md"
    path.write_text("body\n", encoding="utf-8")
    rc = qtp.cmd_invalidate_marker([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert f"BLOCKED: no frontmatter marker written for {path}" in out


def test_qiita_team_post_invalidate_marker_usage_without_files(capsys):
    rc = qtp.cmd_invalidate_marker([])
    out = capsys.readouterr().out
    assert rc == 2
    assert "usage: invalidate-marker <file.md> [file2.md ...]" in out
    assert "does not touch remote/Team API state" in out


def test_qiita_team_post_invalidate_marker_blocks_flag_errors(capsys):
    rc = qtp.cmd_invalidate_marker(["--bogus"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "BLOCKED:" in out
    assert "usage: invalidate-marker <file.md> [file2.md ...]" in out


def test_qiita_team_post_invalidate_marker_multiple_files_fail_if_any_write_is_blocked(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    ok = tmp_path / "ok.md"
    ok.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    bad = tmp_path / "bad.md"
    bad.write_text("body\n", encoding="utf-8")
    rc = qtp.cmd_invalidate_marker([str(ok), str(bad)])
    out = capsys.readouterr().out
    assert rc == 1
    assert f"BLOCKED: no frontmatter marker written for {bad}" in out
    assert f"marker invalidated: {ok}" not in out
    assert "qiita_team_verified: true" in ok.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_blocks_when_frontmatter_lacks_marker_key(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_invalidate_marker([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert f"BLOCKED: no frontmatter marker written for {path}" in out
    assert "qiita_team_verified:" not in path.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_blocks_paths_outside_allowed_roots(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_invalidate_marker([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert f"BLOCKED: invalidate-marker path outside allowed roots: {path}" in out
    assert "qiita_team_verified: true" in path.read_text(encoding="utf-8")


def test_qiita_team_post_allowed_marker_path_normalizes_case(monkeypatch):
    root = str(_public_root())
    target = str(_public_root() / "team_stock_example.md")
    monkeypatch.setattr(qtp.os.path, "realpath", lambda path: root if str(path).endswith("public") else target)
    monkeypatch.setattr(qtp.os.path, "normcase", lambda path: path.lower())
    assert qtp._is_allowed_marker_path(str(_public_root() / "team_stock_example.md").upper()) is True


def test_qiita_team_post_allowed_marker_path_rejects_non_team_stock_public_articles(monkeypatch):
    root = str(_public_root())
    target = str(_public_root() / "22d5460384c2cb54a9e6.md")
    monkeypatch.setattr(qtp.os.path, "realpath", lambda path: root if str(path).endswith("public") else target)
    monkeypatch.setattr(qtp.os.path, "normcase", lambda path: path.lower())
    assert qtp._is_allowed_marker_path(str(_public_root() / "22d5460384c2cb54a9e6.md").upper()) is False


def test_qiita_team_post_allowed_marker_path_rejects_team_stock_backups(monkeypatch):
    root = str(_public_root())
    target = str(_public_root() / "team_stock_example.md.bak")
    monkeypatch.setattr(qtp.os.path, "realpath", lambda path: root if str(path).endswith("public") else target)
    monkeypatch.setattr(qtp.os.path, "normcase", lambda path: path.lower())
    assert qtp._is_allowed_marker_path(str(_public_root() / "team_stock_example.md.bak").upper()) is False


def test_qiita_team_post_invalidate_marker_reports_partial_apply_on_late_oserror(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    first = tmp_path / "first.md"
    second = tmp_path / "second.md"
    for path in (first, second):
        path.write_text(
            "---\n"
            "title: hello\n"
            "qiita_team_verified: true\n"
            "---\n"
            "body\n",
            encoding="utf-8",
        )
    real_writeback = qtp._writeback_team_verified
    calls = {"count": 0}

    def flaky_writeback(path, verified):
        calls["count"] += 1
        if calls["count"] == 2:
            raise OSError("disk full")
        return real_writeback(path, verified)

    monkeypatch.setattr(qtp, "_writeback_team_verified", flaky_writeback)
    rc = qtp.cmd_invalidate_marker([str(first), str(second)])
    out = capsys.readouterr().out
    assert rc == 1
    assert f"marker invalidated: {first}" in out
    assert f"FAIL: marker invalidate writeback failed for {second}: disk full" in out
    assert f"FAIL: invalidate-marker partially applied; invalidated: {first}" in out
    assert f"FAIL: invalidate-marker not invalidated: {second}" in out
    assert "qiita_team_verified: false" in first.read_text(encoding="utf-8")
    assert "qiita_team_verified: true" in second.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_reports_phase1_read_failure(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    real_has_key = qtp._frontmatter_has_key

    def flaky_has_key(candidate, key):
        if str(candidate) == str(path):
            raise OSError("access denied")
        return real_has_key(candidate, key)

    monkeypatch.setattr(qtp, "_frontmatter_has_key", flaky_has_key)
    rc = qtp.cmd_invalidate_marker([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert f"FAIL: marker invalidate read failed for {path}: access denied" in out
    assert "FAIL: no markers were invalidated (fail-closed)." in out
    assert "qiita_team_verified: true" in path.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_continues_after_midstream_oserror(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    first = tmp_path / "first.md"
    second = tmp_path / "second.md"
    third = tmp_path / "third.md"
    for path in (first, second, third):
        path.write_text(
            "---\n"
            "title: hello\n"
            "qiita_team_verified: true\n"
            "---\n"
            "body\n",
            encoding="utf-8",
        )
    real_writeback = qtp._writeback_team_verified
    calls = {"count": 0}

    def flaky_writeback(path, verified):
        calls["count"] += 1
        if calls["count"] == 2:
            raise OSError("disk full")
        return real_writeback(path, verified)

    monkeypatch.setattr(qtp, "_writeback_team_verified", flaky_writeback)
    rc = qtp.cmd_invalidate_marker([str(first), str(second), str(third)])
    out = capsys.readouterr().out

    assert rc == 1
    assert f"marker invalidated: {first}" in out
    assert f"FAIL: marker invalidate writeback failed for {second}: disk full" in out
    assert f"marker invalidated: {third}" in out
    assert f"FAIL: invalidate-marker partially applied; invalidated: {first}, {third}" in out
    assert f"FAIL: invalidate-marker not invalidated: {second}" in out
    assert "qiita_team_verified: false" in first.read_text(encoding="utf-8")
    assert "qiita_team_verified: true" in second.read_text(encoding="utf-8")
    assert "qiita_team_verified: false" in third.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_reports_validation_writeback_drift(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "_writeback_team_verified", lambda candidate, verified: False)

    rc = qtp.cmd_invalidate_marker([str(path)])
    out = capsys.readouterr().out

    assert rc == 1
    assert f"FAIL: marker invalidate validation/writeback drift for {path}" in out
    assert f"FAIL: invalidate-marker not invalidated: {path}" in out
    assert "qiita_team_verified: true" in path.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_deduplicates_same_file(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    rc = qtp.cmd_invalidate_marker([str(path), str(path)])
    out = capsys.readouterr().out

    assert rc == 0
    assert out.count(f"marker invalidated: {path}") == 1
    assert "qiita_team_verified: false" in path.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_deduplicates_same_realpath_alias(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "team.md"
    alias = tmp_path / "." / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    rc = qtp.cmd_invalidate_marker([str(path), str(alias)])
    out = capsys.readouterr().out

    assert rc == 0
    assert out.count("marker invalidated:") == 1
    assert "qiita_team_verified: false" in path.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_warns_on_malformed_marker_value(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: maybe\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    rc = qtp.cmd_invalidate_marker([str(path)])
    out = capsys.readouterr().out

    assert rc == 0
    assert "WARNING: existing qiita_team_verified value was malformed ('maybe') - resetting to false" in out
    assert f"marker invalidated: {path}" in out
    assert "qiita_team_verified: false" in path.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_reports_noop_when_already_false(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: false\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    rc = qtp.cmd_invalidate_marker([str(path)])
    out = capsys.readouterr().out

    assert rc == 0
    assert f"marker already invalidated (no-op): {path}" in out
    assert f"marker invalidated: {path}" not in out
    assert "qiita_team_verified: false" in path.read_text(encoding="utf-8")


def test_qiita_team_post_invalidate_marker_defers_malformed_warning_until_write_phase(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda path: True)
    malformed = tmp_path / "malformed.md"
    malformed.write_text(
        "---\n"
        "title: hello\n"
        "qiita_team_verified: maybe\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    blocked = tmp_path / "blocked.md"
    blocked.write_text("body\n", encoding="utf-8")

    rc = qtp.cmd_invalidate_marker([str(malformed), str(blocked)])
    out = capsys.readouterr().out

    assert rc == 1
    assert "WARNING: existing qiita_team_verified value was malformed" not in out
    assert f"BLOCKED: no frontmatter marker written for {blocked}" in out
    assert "FAIL: no markers were invalidated (fail-closed)." in out
    assert "qiita_team_verified: maybe" in malformed.read_text(encoding="utf-8")


def test_qiita_team_post_writeback_team_verified_blocks_yaml_regex_drift(tmp_path):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "notes: hello\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    original_split_frontmatter = qtp.split_frontmatter
    qtp.split_frontmatter = lambda text: ({"qiita_team_verified": "maybe"}, "body\n")
    try:
        wrote = qtp._writeback_team_verified(str(path), False)
    finally:
        qtp.split_frontmatter = original_split_frontmatter

    assert wrote is False
    text = path.read_text(encoding="utf-8")
    assert text.count("qiita_team_verified:") == 0
    assert "notes: hello" in text


def test_qiita_team_post_main_dispatches_invalidate_marker(monkeypatch):
    calls = {}

    def fake_invalidate(args):
        calls["args"] = args
        return 7

    monkeypatch.setattr(qtp, "cmd_invalidate_marker", fake_invalidate)
    monkeypatch.setattr(qtp.sys, "argv", ["qiita_team_post.py", "invalidate-marker", "team_stock_example.md"])

    rc = qtp.main()

    assert rc == 7
    assert calls["args"] == ["team_stock_example.md"]


def test_qiita_team_post_cmd_post_blocks_marker_writeback_outside_allowlist(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "_is_allowed_marker_path", lambda candidate: False)

    def unexpected_resolve_token():
        raise AssertionError("resolve_token should not run when the source path is outside the marker allowlist")

    monkeypatch.setattr(qtp, "resolve_token", unexpected_resolve_token)

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert (
        "BLOCKED: Team poster post is only supported for "
        "tools/qiita-cli-poc/public/team_stock_*.md sources."
    ) in out


def test_qiita_team_post_cmd_post_blocks_unrecognized_private_value(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: on\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "UNRECOGNIZED_PRIVATE_BLOCK" in out


def test_qiita_team_post_dry_run_warns_on_ignore_publish(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "ignorePublish: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert qtp.IGNORE_PUBLISH_WARNING in out


def test_qiita_team_post_dry_run_blocks_create_without_group_url_name(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "GROUP_URL_NAME_BLOCK" in out


def test_qiita_team_post_dry_run_blocks_local_path_warning(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "See [local](./note.md)\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "LOCAL PATH in body" in out


def test_qiita_team_post_dry_run_blocks_create_with_null_group_url_name(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: null\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "GROUP_URL_NAME_BLOCK" in out


def test_qiita_team_post_dry_run_without_ignore_publish_stays_ok(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "BLOCKED:" not in out


def test_qiita_team_post_dry_run_patch_surfaces_non_resent_group_target(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "PATCH update id=team-item-id" in out
    assert "group_url_name(frontmatter): general" in out
    assert "PATCH does not resend this field" in out


def test_qiita_team_post_dry_run_patch_can_resend_group_target_with_opt_in(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path), "--patch-group-url-name"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "group_url_name(patch): general" in out
    assert "PATCH will resend this field" in out
    assert "private is still resent from frontmatter (False)" in out


def test_qiita_team_post_dry_run_patch_surfaces_missing_group_target_note(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "PATCH update id=team-item-id" in out
    assert "group_url_name(frontmatter): (none)" in out
    assert "PATCH does not resend this field" in out


def test_qiita_team_post_dry_run_patch_blocks_opt_in_without_group_target(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path), "--patch-group-url-name"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.PATCH_GROUP_URL_NAME_BLOCK in out
    assert "PATCH does not resend this field" not in out


def test_qiita_team_post_dry_run_flag_only_returns_usage(capsys):
    rc = qtp.cmd_dry_run(["--patch-group-url-name"])
    out = capsys.readouterr().out
    assert rc == 2
    assert "usage: dry-run <file.md> [--patch-group-url-name]" in out


def test_qiita_team_post_dry_run_blocks_multiple_files(tmp_path, capsys):
    path1 = tmp_path / "team1.md"
    path2 = tmp_path / "team2.md"
    for path in (path1, path2):
        path.write_text(
            "---\n"
            "title: hello\n"
            "tags:\n"
            "  - AI\n"
            "private: false\n"
            "id: team-item-id\n"
            "---\n"
            "body\n",
            encoding="utf-8",
        )
    rc = qtp.cmd_dry_run([str(path1), str(path2)])
    out = capsys.readouterr().out
    assert rc == 2
    assert "BLOCKED: exactly one file expected, got 2" in out


def test_qiita_team_post_dry_run_blocks_unknown_flag(capsys):
    rc = qtp.cmd_dry_run(["sample.md", "--patch-group-url-nme"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.UNKNOWN_FLAG_BLOCK.format(flag="--patch-group-url-nme") in out


def test_qiita_team_post_dry_run_blocks_single_dash_flag_typo(capsys):
    rc = qtp.cmd_dry_run(["sample.md", "-patch-group-url-name"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.UNKNOWN_FLAG_BLOCK.format(flag="-patch-group-url-name") in out


def test_qiita_team_post_dry_run_blocks_value_form_flag(capsys):
    rc = qtp.cmd_dry_run(["sample.md", "--patch-group-url-name=general"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.UNKNOWN_FLAG_BLOCK.format(flag="--patch-group-url-name=general") in out


def test_qiita_team_post_dry_run_patch_normalizes_null_group_target_note(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "group_url_name: null\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 0
    assert "PATCH update id=team-item-id" in out
    assert "group_url_name(frontmatter): (none)" in out
    assert "PATCH does not resend this field" in out


def test_qiita_team_post_dry_run_blocks_unrecognized_ignore_publish(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "ignorePublish: ture\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.UNRECOGNIZED_IGNORE_PUBLISH_BLOCK.format(value="ture") in out


def test_qiita_team_post_dry_run_blocks_ignore_publish_key_typo(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "ignorepublish: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert "IGNORE_PUBLISH_KEY_BLOCK" in out


def test_qiita_team_post_cmd_post_blocks_ignore_publish_without_override(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "ignorePublish: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.IGNORE_PUBLISH_WARNING in out
    assert qtp.IGNORE_PUBLISH_BLOCK in out


def test_qiita_team_post_cmd_post_allows_ignore_publish_with_override(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "ignorePublish: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    calls = []

    def _fake_req(method, path, token, payload=None):
        calls.append((method, path, payload))
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", _fake_req)
    rc = qtp.cmd_post([str(path), "--yes", "--force-ignore-publish"])
    out = capsys.readouterr().out
    assert rc == 0
    assert any(call[0] == "POST" and call[1] == "/items" for call in calls)
    assert qtp.IGNORE_PUBLISH_WARNING in out


def test_qiita_team_post_cmd_post_blocks_unrecognized_ignore_publish(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "ignorePublish: ture\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.UNRECOGNIZED_IGNORE_PUBLISH_BLOCK.format(value="ture") in out


def test_qiita_team_post_cmd_post_blocks_ignore_publish_key_typo(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "IgnorePublish: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "IGNORE_PUBLISH_KEY_BLOCK" in out


def test_qiita_team_post_cmd_post_blocks_create_without_group_url_name(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "GROUP_URL_NAME_BLOCK" in out


def test_qiita_team_post_cmd_post_blocks_create_with_null_group_url_name(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: null\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out
    assert rc == 1
    assert "GROUP_URL_NAME_BLOCK" in out


def test_qiita_team_post_cmd_post_patch_does_not_resend_group_url_name(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    calls = []

    def _fake_req(method, req_path, token, payload=None):
        calls.append((method, req_path, token, payload))
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", _fake_req)
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (200)" in out
    assert len(calls) == 3
    assert calls[0] == ("GET", "/items/team-item-id", "fake-token", None)
    method, req_path, token, payload = calls[1]
    assert method == "PATCH"
    assert req_path == "/items/team-item-id"
    assert token == "fake-token"
    assert payload["title"] == "hello"
    assert payload["body"] == "body\n"
    assert payload["tags"] == [{"name": "AI", "versions": []}]
    assert payload["private"] is False
    assert payload["tweet"] is False
    assert "group_url_name" not in payload
    assert calls[2] == ("GET", "/items/team-item-id", "fake-token", None)


def test_qiita_team_post_cmd_post_patch_can_resend_group_url_name_with_opt_in(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    calls = []

    def _fake_req(method, req_path, token, payload=None):
        calls.append((method, req_path, token, payload))
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", _fake_req)
    rc = qtp.cmd_post([str(path), "--yes", "--patch-group-url-name"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (200)" in out
    assert calls[1][3]["group_url_name"] == "general"


def test_qiita_team_post_cmd_post_patch_blocks_opt_in_without_group_target(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    rc = qtp.cmd_post([str(path), "--yes", "--patch-group-url-name"])
    out = capsys.readouterr().out

    assert rc == 1
    assert qtp.PATCH_GROUP_URL_NAME_BLOCK in out


def test_qiita_team_post_cmd_post_without_yes_preserves_patch_group_url_name_preview(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_post([str(path), "--patch-group-url-name"])
    out = capsys.readouterr().out

    assert rc == 3
    assert "refusing: --yes required" in out
    assert "group_url_name(patch): general" in out
    assert "PATCH will resend this field" in out


def test_qiita_team_post_cmd_post_without_yes_ignores_force_ignore_publish_in_preview(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_post([str(path), "--force-ignore-publish"])
    out = capsys.readouterr().out
    assert rc == 3
    assert "refusing: --yes required" in out
    assert "UNKNOWN_FLAG_BLOCK" not in out
    assert "PATCH update id=team-item-id" in out


def test_qiita_team_post_cmd_post_blocks_multiple_files(tmp_path, capsys):
    path1 = tmp_path / "team1.md"
    path2 = tmp_path / "team2.md"
    for path in (path1, path2):
        path.write_text(
            "---\n"
            "title: hello\n"
            "tags:\n"
            "  - AI\n"
            "private: false\n"
            "id: team-item-id\n"
            "---\n"
            "body\n",
            encoding="utf-8",
        )
    rc = qtp.cmd_post([str(path1), str(path2), "--yes"])
    out = capsys.readouterr().out
    assert rc == 2
    assert "BLOCKED: exactly one file expected, got 2" in out


def test_qiita_team_post_cmd_post_blocks_unknown_flag(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_post([str(path), "--yes", "--patch-group-url-nme"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.UNKNOWN_FLAG_BLOCK.format(flag="--patch-group-url-nme") in out


def test_qiita_team_post_cmd_post_blocks_single_dash_flag_typo(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_post([str(path), "--yes", "-patch-group-url-name"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.UNKNOWN_FLAG_BLOCK.format(flag="-patch-group-url-name") in out


def test_qiita_team_post_cmd_post_blocks_value_form_flag(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_post([str(path), "--yes", "--patch-group-url-name=general"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qtp.UNKNOWN_FLAG_BLOCK.format(flag="--patch-group-url-name=general") in out


def test_qiita_team_post_dry_run_create_notes_patch_group_url_name_is_ignored(tmp_path, capsys):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    rc = qtp.cmd_dry_run([str(path), "--patch-group-url-name"])
    out = capsys.readouterr().out
    assert rc == 0
    assert qtp.PATCH_GROUP_URL_NAME_CREATE_NOTE in out
    assert "group_url_name is already sent from frontmatter" in out


def test_qiita_team_post_cmd_post_create_notes_patch_group_url_name_is_ignored(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    calls = []

    def _fake_req(method, req_path, token, payload=None):
        calls.append((method, req_path, token, payload))
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", _fake_req)
    rc = qtp.cmd_post([str(path), "--yes", "--patch-group-url-name"])
    out = capsys.readouterr().out

    assert rc == 0
    assert qtp.PATCH_GROUP_URL_NAME_CREATE_NOTE in out
    assert calls[0][0] == "POST"
    assert "group_url_name" in calls[0][3]


def test_qiita_team_post_cmd_post_patch_preserves_private_true(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    calls = []

    def _fake_req(method, req_path, token, payload=None):
        calls.append((method, req_path, token, payload))
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "private": True,
            "group": {"url_name": None, "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", _fake_req)
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (200)" in out
    assert calls[1][3]["private"] is True


def test_qiita_team_post_cmd_post_surfaces_visibility_readback(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "private=False" in out
    assert "group.url_name=general" in out
    assert "group.private=False" in out
    assert "organization_url_name=None" in out


def test_qiita_team_post_cmd_post_create_surfaces_visibility_readback(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (201)" in out
    assert "private=False" in out
    assert "group.url_name=general" in out
    assert "group.private=False" in out
    assert "organization_url_name=None" in out


def test_qiita_team_post_cmd_show_surfaces_visibility_readback(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        assert method == "GET"
        assert path == "/items/team-item-id"
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_show(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "READABLE (200)" in out
    assert "title=hello" in out
    assert "private=False" in out
    assert "group.url_name=general" in out
    assert "group.private=False" in out
    assert "organization_url_name=None" in out


def test_qiita_team_post_cmd_show_distinguishes_auth_failures(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 403, {"message": "forbidden"}

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_show(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "AUTH FAIL (403)" in out


def test_qiita_team_post_cmd_show_blocks_unknown_flag(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    rc = qtp.cmd_show(["team-item-id", "--foo"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "UNKNOWN_FLAG_BLOCK" in out
    assert "usage: show <item_id>" in out


def test_qiita_team_post_cmd_preflight_checks_auth_and_item_readback(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    calls = []

    def fake_req(method, path, token, payload=None):
        calls.append((method, path, token, payload))
        if path == "/authenticated_user":
            return 200, {"id": "furuse-kazufumi"}
        if path == "/items/team-item-id":
            return 200, {
                "id": "team-item-id",
                "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
                "title": "hello",
                "private": False,
                "group": {"url_name": "general", "private": False},
                "organization_url_name": None,
            }
        raise AssertionError(path)

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_preflight(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "preflight: token_source=env:QIITA_TEAM_TOKEN" in out
    assert "preflight auth: OK user=@furuse-kazufumi team='fullsense'" in out
    assert "preflight item: OK" in out
    assert "organization_url_name=None" in out
    assert calls[0][1] == "/authenticated_user"
    assert calls[1][1] == "/items/team-item-id"


def test_qiita_team_post_cmd_preflight_blocks_unknown_flag(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    rc = qtp.cmd_preflight(["team-item-id", "--foo"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "UNKNOWN_FLAG_BLOCK" in out
    assert "usage: preflight <item_id> [item_id...]" in out


def test_qiita_team_post_cmd_preflight_blocks_on_item_auth_failure(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        if path == "/authenticated_user":
            return 200, {"id": "furuse-kazufumi"}
        if path == "/items/team-item-id":
            return 403, {"message": "forbidden"}
        raise AssertionError(path)

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_preflight(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "preflight item: BLOCKED  AUTH FAIL (403)" in out
    assert "preflight: BLOCKED" in out


def test_qiita_team_post_cmd_scan_explicit_glob_keeps_qiita_cli_poc_files(tmp_path, capsys):
    article = tmp_path / "qiita-cli-poc" / "public" / "team_stock_example.md"
    article.parent.mkdir(parents=True)
    article.write_text(
        "---\n"
        "title: example\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    old_file = qtp.__file__
    qtp.__file__ = str(tmp_path / "shadow_qtp.py")
    try:
        rc = qtp.cmd_scan([str(tmp_path / "**" / "team_stock_*.md")])
    finally:
        qtp.__file__ = old_file
    out = capsys.readouterr().out

    assert rc == 0
    assert "scan: 1 files" in out
    assert "summary: 1/1 registration-safe" in out


def test_qiita_team_post_cmd_scan_default_targets_curated_qiita_range(tmp_path, capsys, monkeypatch):
    article_28 = tmp_path / "QIITA_#28_sample.md"
    article_42 = tmp_path / "QIITA_#42_sample.md"
    article_35 = tmp_path / "QIITA_#35_sample.md"
    for path in (article_28, article_42, article_35):
        path.write_text(
            "---\n"
            "title: example\n"
            "tags:\n"
            "  - AI\n"
            "private: true\n"
            "group_url_name: general\n"
            "---\n"
            "body\n",
            encoding="utf-8",
        )

    monkeypatch.setattr(qtp, "ARTICLES_DIR", str(tmp_path))
    old_file = qtp.__file__
    qtp.__file__ = str(tmp_path / "shadow_qtp.py")
    try:
        rc = qtp.cmd_scan([])
    finally:
        qtp.__file__ = old_file
    out = capsys.readouterr().out

    assert rc == 0
    assert "scan: 2 files" in out
    assert "scan coverage: queued 12 / existing 3 stem(s); excluded 1 (#35); queued-but-missing 10 (#29–34,#38–41)" in out
    assert "QIITA_#28" in out
    assert "QIITA_#42" in out
    assert "summary: 2/2 registration-safe" in out


def test_qiita_team_post_cmd_preflight_blocks_on_qiita_token_fallback(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "D:/api-keys.json:qiita_token"))
    rc = qtp.cmd_preflight(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "preflight: token_source=D:/api-keys.json:qiita_token" in out
    assert "WARNING qiita.com personal token fallback is in use" in out
    assert "preflight: BLOCKED personal-token fallback cannot prove Team auth / membership / visibility." in out


def test_qiita_team_post_resolve_token_skips_whitespace_only_env_and_uses_file_fallback(tmp_path, monkeypatch):
    api_keys = tmp_path / "api-keys.json"
    api_keys.write_text('{"qiita_team_token":"team-token"}\n', encoding="utf-8")
    monkeypatch.setenv("QIITA_TEAM_TOKEN", "   ")
    monkeypatch.setattr(qtp.os.path, "expanduser", lambda _: str(api_keys))
    real_open = open

    def fake_open(path, *args, **kwargs):
        if path == "D:/api-keys.json":
            raise OSError("blocked for test isolation")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    token, source = qtp.resolve_token()

    assert token == "team-token"
    assert source == f"{api_keys}:qiita_team_token"


def test_qiita_team_post_resolve_token_skips_whitespace_only_file_token_and_falls_back(tmp_path, monkeypatch):
    api_keys = tmp_path / "api-keys.json"
    api_keys.write_text(
        '{\n'
        '  "qiita_team_token": "   ",\n'
        '  "qiita_token": "personal-token"\n'
        '}\n',
        encoding="utf-8",
    )
    monkeypatch.delenv("QIITA_TEAM_TOKEN", raising=False)
    monkeypatch.setattr(qtp.os.path, "expanduser", lambda _: str(api_keys))
    real_open = open

    def fake_open(path, *args, **kwargs):
        if path == "D:/api-keys.json":
            raise OSError("blocked for test isolation")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    token, source = qtp.resolve_token()

    assert token == "personal-token"
    assert source == f"{api_keys}:qiita_token"


def test_qiita_team_post_resolve_token_prefers_team_key_over_personal(tmp_path, monkeypatch):
    api_keys = tmp_path / "api-keys.json"
    api_keys.write_text(
        '{\n'
        '  "qiita_token": "personal-token",\n'
        '  "QIITA_TEAM_TOKEN": "team-token"\n'
        '}\n',
        encoding="utf-8",
    )
    monkeypatch.delenv("QIITA_TEAM_TOKEN", raising=False)
    monkeypatch.setattr(qtp.os.path, "expanduser", lambda _: str(api_keys))
    real_open = open

    def fake_open(path, *args, **kwargs):
        if path == "D:/api-keys.json":
            raise OSError("blocked for test isolation")
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    token, source = qtp.resolve_token()

    assert token == "team-token"
    assert source == f"{api_keys}:QIITA_TEAM_TOKEN"


def test_qiita_team_post_resolve_token_prefers_team_key_in_later_file_over_personal(tmp_path, monkeypatch):
    first = tmp_path / "api-keys.json"
    second_dir = tmp_path / "home"
    second_dir.mkdir()
    second = second_dir / "api-keys.json"
    first.write_text('{"qiita_token":"personal-token"}\n', encoding="utf-8")
    second.write_text('{"qiita_team_token":"team-token"}\n', encoding="utf-8")
    monkeypatch.delenv("QIITA_TEAM_TOKEN", raising=False)
    monkeypatch.setattr(qtp.os.path, "expanduser", lambda _: str(second))
    real_open = open

    def fake_open(path, *args, **kwargs):
        if path == "D:/api-keys.json":
            return real_open(first, *args, **kwargs)
        return real_open(path, *args, **kwargs)

    monkeypatch.setattr("builtins.open", fake_open)

    token, source = qtp.resolve_token()

    assert token == "team-token"
    assert source == f"{second}:qiita_team_token"


def test_qiita_team_post_cmd_verify_blocks_on_qiita_token_fallback(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "D:/api-keys.json:qiita_token"))

    rc = qtp.cmd_verify([])
    out = capsys.readouterr().out

    assert rc == 1
    assert "verify: token_source=D:/api-keys.json:qiita_token" in out
    assert "WARNING qiita.com personal token fallback is in use" in out
    assert "verify: BLOCKED personal-token fallback cannot prove Team auth / membership / visibility." in out


def test_qiita_team_post_cmd_show_blocks_on_qiita_token_fallback(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "D:/api-keys.json:qiita_token"))

    rc = qtp.cmd_show(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "show: token_source=D:/api-keys.json:qiita_token" in out
    assert "WARNING qiita.com personal token fallback is in use" in out
    assert "show: BLOCKED personal-token fallback cannot prove Team visibility on this workspace." in out


def test_qiita_team_post_cmd_show_labels_readable_private(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_show(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "READABLE PRIVATE (200)" in out


def test_qiita_team_post_cmd_show_surfaces_not_found_hint(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 404, {"message": "not found"}

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_show(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "NOT FOUND (404): item id=team-item-id is not readable on team 'fullsense'" in out


def test_qiita_team_post_cmd_show_blocks_empty_url_readback(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 200, {
            "id": "team-item-id",
            "url": "",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_show(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "returned without url; cannot confirm team host identity" in out


def test_qiita_team_post_cmd_show_blocks_missing_private_readback(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_show(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "private field missing" in out


def test_qiita_team_post_cmd_show_blocks_non_bool_private_readback(capsys, monkeypatch):
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": "maybe",
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    rc = qtp.cmd_show(["team-item-id"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "private field is non-bool" in out


def test_qiita_team_post_cmd_scan_default_accepts_md_bak_and_normalizes_name(tmp_path, capsys, monkeypatch):
    article = tmp_path / "nested" / "QIITA_#32_llcore_cpu_poc_battery.md.bak"
    article.parent.mkdir(parents=True)
    article.write_text(
        "---\n"
        "title: example\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "See [local](./note.md)\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(qtp, "ARTICLES_DIR", str(tmp_path))
    old_file = qtp.__file__
    qtp.__file__ = str(tmp_path / "shadow_qtp.py")
    try:
        rc = qtp.cmd_scan([])
    finally:
        qtp.__file__ = old_file
    out = capsys.readouterr().out

    assert rc == 0
    assert "QIITA_#32_llcore_cpu_poc_battery.md" in out
    assert "LOCAL PATH in body" in out


def test_qiita_team_post_cmd_scan_default_prefers_md_over_md_bak(tmp_path, capsys, monkeypatch):
    current = tmp_path / "nested" / "QIITA_#32_llcore_cpu_poc_battery.md"
    backup = tmp_path / "nested" / "QIITA_#32_llcore_cpu_poc_battery.md.bak"
    current.parent.mkdir(parents=True)
    current.write_text(
        "---\n"
        "title: current\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "current body\n",
        encoding="utf-8",
    )
    backup.write_text(
        "---\n"
        "title: stale\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "stale body with [local](./note.md)\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(qtp, "ARTICLES_DIR", str(tmp_path))
    old_file = qtp.__file__
    qtp.__file__ = str(tmp_path / "shadow_qtp.py")
    try:
        rc = qtp.cmd_scan([])
    finally:
        qtp.__file__ = old_file
    out = capsys.readouterr().out
    report = qtp.json.loads((tmp_path / "qiita_registration_safety_report.json").read_text(encoding="utf-8"))

    assert rc == 0
    assert "LOCAL PATH in body" not in out
    assert "summary: 1/1 registration-safe" in out
    assert len(report["files"]) == 1
    assert report["files"][0]["file"] == "QIITA_#32_llcore_cpu_poc_battery.md"


def test_qiita_team_post_cmd_post_blocks_local_path_warning(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "See [local](./note.md)\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, path, token, payload=None):
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "BLOCKED (fix first):" in out
    assert "LOCAL PATH in body" in out


def test_qiita_team_post_cmd_post_blocks_on_qiita_token_fallback(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "id: team-item-id\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "D:/api-keys.json:qiita_token"))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "post: token_source=D:/api-keys.json:qiita_token" in out
    assert "WARNING qiita.com personal token fallback is in use" in out
    assert "post: BLOCKED personal-token fallback cannot prove Team auth / membership / visibility." in out


def test_qiita_team_post_cmd_post_persists_create_id_even_if_authoritative_get_readback_fails(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    writeback_calls = []

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", lambda item_id, token: (200, {
        "id": item_id,
        "url": "",
        "title": "hello",
        "private": True,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (writeback_calls.append(args) or True))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "authoritative read-after-write check failed" in out
    assert "returned without url; cannot confirm team host identity" in out
    assert "create already persisted frontmatter id=team-item-id" in out
    assert writeback_calls == [(str(path), "team-item-id")]


def test_qiita_team_post_cmd_post_blocks_on_private_get_readback_mismatch_after_persisting_id(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    writeback_calls = []

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", lambda item_id, token: (200, {
        "id": item_id,
        "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
        "title": "hello",
        "private": False,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (writeback_calls.append(args) or True))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "authoritative read-after-write check failed" in out
    assert "did not match intended private=True" in out
    assert "create already persisted frontmatter id=team-item-id" in out
    assert writeback_calls == [(str(path), "team-item-id")]


def test_qiita_team_post_cmd_post_blocks_on_group_get_readback_mismatch_after_persisting_id(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: target-group\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    writeback_calls = []

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "target-group", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", lambda item_id, token: (200, {
        "id": item_id,
        "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
        "title": "hello",
        "private": True,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (writeback_calls.append(args) or True))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "authoritative read-after-write check failed" in out
    assert "did not match intended group_url_name='target-group'" in out
    assert "create already persisted frontmatter id=team-item-id" in out
    assert writeback_calls == [(str(path), "team-item-id")]


def test_qiita_team_post_cmd_post_persists_create_id_after_authoritative_get_readback(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    writeback_calls = []

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", lambda item_id, token: (200, {
        "id": item_id,
        "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
        "title": "hello",
        "private": True,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (writeback_calls.append(args) or True))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (201)" in out
    assert writeback_calls == [(str(path), "team-item-id")]


def test_qiita_team_post_cmd_post_marks_verified_true_after_authoritative_get_readback(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", lambda item_id, token: (200, {
        "id": item_id,
        "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
        "title": "hello",
        "private": True,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (201)" in out
    text = path.read_text(encoding="utf-8")
    assert "id: team-item-id" in text
    assert "qiita_team_verified: true" in text


def test_qiita_team_post_cmd_post_uses_authoritative_get_over_response_private_mismatch(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    writeback_calls = []

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", lambda item_id, token: (200, {
        "id": item_id,
        "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
        "title": "hello",
        "private": True,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (writeback_calls.append(args) or True))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (201)" in out
    assert writeback_calls == [(str(path), "team-item-id")]


def test_qiita_team_post_cmd_post_blocks_patch_response_id_mismatch(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "id: expected-item-id\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        if method == "GET":
            return 200, {
                "id": "expected-item-id",
                "url": "https://fullsense.qiita.com/furuse-kazufumi/items/expected-item-id",
                "title": "hello",
                "private": True,
                "group": {"url_name": "general", "private": False},
                "organization_url_name": None,
            }
        assert method == "PATCH"
        return 200, {
            "id": "wrong-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/wrong-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "write response id mismatch; requested id=expected-item-id but API returned id=wrong-item-id" in out


def test_qiita_team_post_cmd_post_retries_create_readback_not_found(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    monkeypatch.setattr(qtp.time, "sleep", lambda _: None)
    writeback_calls = []
    read_calls = []

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    def fake_read(item_id, token):
        read_calls.append(item_id)
        if len(read_calls) < 3:
            return 404, "not yet visible"
        return 200, {
            "id": item_id,
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", fake_read)
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (writeback_calls.append(args) or True))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (201)" in out
    assert read_calls == ["team-item-id", "team-item-id", "team-item-id"]
    assert writeback_calls == [(str(path), "team-item-id")]


def test_qiita_team_post_cmd_post_ignores_empty_response_url_when_authoritative_get_passes(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    writeback_calls = []

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", lambda item_id, token: (200, {
        "id": item_id,
        "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
        "title": "hello",
        "private": True,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (writeback_calls.append(args) or True))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (201)" in out
    assert writeback_calls == [(str(path), "team-item-id")]


def test_qiita_team_post_cmd_post_blocks_create_when_response_id_missing(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    writeback_calls = []

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (writeback_calls.append(args) or True))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "write response missing item id; cannot perform authoritative readback" in out
    assert writeback_calls == []


def test_qiita_team_post_cmd_post_blocks_unverified_patch_until_readback_recovers(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "qiita_team_verified: false\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    monkeypatch.setattr(qtp, "_read_item_with_retry", lambda item_id, token: (404, "not found"))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "qiita_team_verified=false" in out
    assert "authoritative pre-PATCH readback failed" in out


def test_qiita_team_post_cmd_post_blocks_marker_missing_patch_until_readback_recovers(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    monkeypatch.setattr(qtp, "_read_item_with_retry", lambda item_id, token: (404, "not found"))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "qiita_team_verified=missing" in out
    assert "authoritative pre-PATCH readback failed" in out


def test_qiita_team_post_cmd_post_reports_true_marker_on_failed_pre_patch_readback(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    monkeypatch.setattr(qtp, "_read_item_with_retry", lambda item_id, token: (404, "not found"))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "qiita_team_verified=true" in out
    assert "authoritative pre-PATCH readback failed" in out


def test_qiita_team_post_cmd_post_allows_corrective_patch_drift_when_readable(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    req_calls = []

    def fake_req(method, req_path, token, payload=None):
        req_calls.append((method, req_path, payload))
        assert method == "PATCH"
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    read_results = [
        (200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }),
        (200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }),
    ]

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item_with_retry", lambda item_id, token: read_results.pop(0))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert req_calls[0][0] == "PATCH"
    assert "pre-PATCH drift detected: private False -> intended True." in out
    assert "OK (200)" in out


def test_qiita_team_post_cmd_post_patch_without_group_assert_keeps_verified_false(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        assert method == "PATCH"
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item_with_retry", lambda item_id, token: (200, {
        "id": item_id,
        "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
        "title": "hello",
        "private": False,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "group.url_name is observed as general on this PATCH path" in out
    assert "cannot promote qiita_team_verified=true" in out
    assert "leaving qiita_team_verified=false" in out
    text = path.read_text(encoding="utf-8")
    assert "qiita_team_verified: false" in text


def test_qiita_team_post_cmd_post_patch_without_group_blocks_on_group_drift_and_resets_verified(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: false\n"
        "id: team-item-id\n"
        "qiita_team_verified: true\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        assert method == "PATCH"
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    read_results = [
        (200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }),
        (200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": False,
            "group": {"url_name": "drifted-group", "private": False},
            "organization_url_name": None,
        }),
    ]

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item_with_retry", lambda item_id, token: read_results.pop(0))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "authoritative read-after-write check failed" in out
    assert "did not match intended group_url_name='general'" in out
    text = path.read_text(encoding="utf-8")
    assert "qiita_team_verified: false" in text


def test_qiita_team_post_cmd_post_reports_writeback_io_failure_after_create(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: (_ for _ in ()).throw(OSError("disk full")))

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "local id writeback failed after create id=team-item-id" in out
    assert "item is already live on team with id=team-item-id" in out
    assert "id was not persisted locally" in out


def test_qiita_team_post_cmd_post_reports_verified_writeback_failure_after_create(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    real_writeback_id = qtp._writeback_id

    def fake_writeback_verified(*args):
        raise OSError("disk full")

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_writeback_id", real_writeback_id)
    monkeypatch.setattr(qtp, "_writeback_team_verified", fake_writeback_verified)

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "local verification-marker writeback failed after create id=team-item-id" in out
    assert "item id=team-item-id is already persisted locally; do not re-POST" in out
    text = path.read_text(encoding="utf-8")
    assert "id: team-item-id" in text


def test_qiita_team_post_cmd_post_blocks_when_create_id_writeback_makes_no_change(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_writeback_id", lambda *args: False)

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "local id writeback made no change after create id=team-item-id" in out
    assert "frontmatter id not persisted locally" in out
    assert "local writeback drift" in out


def test_qiita_team_post_cmd_post_blocks_when_create_marker_writeback_makes_no_change(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_writeback_team_verified", lambda *args: False)

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "local verification-marker writeback skipped after create id=team-item-id" in out
    assert "frontmatter missing/invalid" in out
    assert "Investigate and repair the qiita_team_verified writeback path before retrying." in out


def test_qiita_team_post_cmd_post_blocks_when_patch_failure_marker_writeback_makes_no_change(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        if method == "GET":
            return 200, {
                "id": "team-item-id",
                "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
                "title": "hello",
                "private": True,
                "group": {"url_name": "general", "private": False},
                "organization_url_name": None,
            }
        assert method == "PATCH"
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    read_calls = []

    def fake_read_with_retry(item_id, token):
        read_calls.append(item_id)
        if len(read_calls) == 1:
            return 200, {
                "id": item_id,
                "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
                "title": "hello",
                "private": True,
                "group": {"url_name": "general", "private": False},
                "organization_url_name": None,
            }
        return 200, {
            "id": item_id,
            "url": "",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item_with_retry", fake_read_with_retry)
    monkeypatch.setattr(qtp, "_writeback_team_verified", lambda *args: False)

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "authoritative read-after-write check failed" in out
    assert "qiita_team_verified=false writeback was skipped" in out
    assert "frontmatter missing/invalid" in out


def test_qiita_team_post_cmd_post_blocks_when_success_marker_writeback_makes_no_change(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private: true\n"
        "group_url_name: general\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))

    def fake_req(method, req_path, token, payload=None):
        assert method == "POST"
        return 201, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "title": "hello",
            "private": True,
            "group": {"url_name": "general", "private": False},
            "organization_url_name": None,
        }

    real_writeback_verified = qtp._writeback_team_verified
    write_calls = []

    def fake_writeback_verified(*args):
        write_calls.append(args)
        if len(write_calls) == 1:
            return real_writeback_verified(*args)
        return False

    monkeypatch.setattr(qtp, "_req", fake_req)
    monkeypatch.setattr(qtp, "_read_item", lambda item_id, token: (200, {
        "id": item_id,
        "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
        "title": "hello",
        "private": True,
        "group": {"url_name": "general", "private": False},
        "organization_url_name": None,
    }))
    monkeypatch.setattr(qtp, "_writeback_team_verified", fake_writeback_verified)

    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 1
    assert "authoritative readback passed but local verification marker writeback was skipped for id=team-item-id" in out
    assert "frontmatter missing/invalid" in out


def test_qiita_team_post_cmd_post_patch_defaults_blank_private_to_true(tmp_path, capsys, monkeypatch):
    path = tmp_path / "team.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "private:\n"
        "id: team-item-id\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(qtp, "resolve_token", lambda: ("fake-token", "env:QIITA_TEAM_TOKEN"))
    calls = []

    def _fake_req(method, req_path, token, payload=None):
        calls.append((method, req_path, token, payload))
        return 200, {
            "id": "team-item-id",
            "url": "https://fullsense.qiita.com/furuse-kazufumi/items/team-item-id",
            "private": True,
            "group": {"url_name": None, "private": False},
            "organization_url_name": None,
        }

    monkeypatch.setattr(qtp, "_req", _fake_req)
    rc = qtp.cmd_post([str(path), "--yes"])
    out = capsys.readouterr().out

    assert rc == 0
    assert "OK (200)" in out
    assert calls[1][3]["private"] is True


def test_qiita_team_post_parse_private_bool_returns_private_on_error():
    value, error = qtp.parse_private_bool("ture", default=True)

    assert value is True
    assert "UNRECOGNIZED_PRIVATE_BLOCK" in error


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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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


def test_qiita_public_post_preflight_blocks_when_baseline_path_is_nested_under_remote(tmp_path, capsys, monkeypatch):
    remote_dir = tmp_path / ".remote" / "nested"
    remote_dir.mkdir(parents=True)
    (remote_dir / "existing-public-id.md").write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "---\n"
        "body\n",
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
        "preflight_remote_baseline: .remote/nested/existing-public-id.md\n"
        "---\n"
        "body\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.PREFLIGHT_BASELINE_PATH_BLOCK.format(path=".remote/nested/existing-public-id.md") in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_refresh_blocks_without_baseline_metadata(tmp_path, capsys, monkeypatch):
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
    rc = qpp.cmd_preflight([str(path), "--refresh-baseline"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.PREFLIGHT_BASELINE_REFRESH_REQUIRED_BLOCK in out
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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


def test_qiita_public_post_preflight_refresh_blocks_when_live_tags_drift(tmp_path, capsys, monkeypatch):
    remote_dir = tmp_path / ".remote"
    remote_dir.mkdir()
    baseline = remote_dir / "existing-public-id.md"
    baseline.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "---\n"
        "live body line 1\n",
        encoding="utf-8",
    )
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "  - Agent\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_remote_baseline: .remote/existing-public-id.md\n"
        "---\n"
        "live body line 1\n",
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
                "body": "live body line 1\n",
            }
        raise AssertionError(f"unexpected _req: {method} {path}")

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path), "--refresh-baseline"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.LIVE_TAGS_BLOCK in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_blocks_when_baseline_tags_drift(tmp_path, capsys, monkeypatch):
    remote_dir = tmp_path / ".remote"
    remote_dir.mkdir()
    baseline = remote_dir / "existing-public-id.md"
    baseline.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "---\n"
        "live body line 1\n",
        encoding="utf-8",
    )
    path = tmp_path / "sample.md"
    path.write_text(
        "---\n"
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
        "  - Agent\n"
        "private: false\n"
        "public_private: false\n"
        "public_id: existing-public-id\n"
        "preflight_remote_baseline: .remote/existing-public-id.md\n"
        "---\n"
        "live body line 1\n",
        encoding="utf-8",
    )

    def _fake_req(method, path, token, payload=None):
        return 200, {"id": "furuse-kazufumi"}

    def _fake_http_get(url, token=None):
        if url == f"{qpp.API_BASE}/items/existing-public-id":
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"},{"name":"Agent"}]}'
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    rc = qpp.cmd_preflight([str(path)])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.PREFLIGHT_BASELINE_TAGS_BLOCK.format(path=baseline) in out
    assert "baseline_tags_match: False" in out
    assert "preflight: BLOCKED" in out


def test_qiita_public_post_preflight_refresh_blocks_when_baseline_write_fails(tmp_path, capsys, monkeypatch):
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
        if url == "https://qiita.com/example/items/existing-public-id":
            return 200, {}, "<title>hello - Qiita</title>"
        raise AssertionError(f"unexpected URL: {url}")

    real_write_text = Path.write_text

    def _boom_write_text(self, *args, **kwargs):
        if self.name.endswith(".tmp"):
            raise OSError("disk full")
        return real_write_text(self, *args, **kwargs)

    monkeypatch.setattr(qpp, "_req", _fake_req)
    monkeypatch.setattr(qpp, "_http_get", _fake_http_get)
    monkeypatch.setattr(qpp, "get_token", lambda: "fake-token")
    monkeypatch.setattr(Path, "write_text", _boom_write_text)
    rc = qpp.cmd_preflight([str(path), "--refresh-baseline"])
    out = capsys.readouterr().out
    assert rc == 1
    assert qpp.PREFLIGHT_BASELINE_REFRESH_WRITE_BLOCK.format(path=baseline) in out
    assert "preflight: BLOCKED" in out


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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
            return 200, {}, '{"id":"existing-public-id","title":"hello","private":false,"url":"https://qiita.com/example/items/existing-public-id","tags":[{"name":"AI"}]}'
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
