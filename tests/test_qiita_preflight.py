# SPDX-License-Identifier: Apache-2.0
"""Regression tests for scripts/qiita_preflight.py."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "qiita_preflight.py"

spec = importlib.util.spec_from_file_location("qiita_preflight", SCRIPT)
assert spec is not None and spec.loader is not None
qp = importlib.util.module_from_spec(spec)
sys.modules["qiita_preflight"] = qp
spec.loader.exec_module(qp)


def test_parse_group_fields_extracts_project_and_related_groups():
    fm = (
        "title: hello\n"
        "project_group: onocollo\n"
        "related_groups:\n"
        "  - gaitlab\n"
        "  - llcore\n"
    )
    assert qp.parse_group_fields(fm) == ("onocollo", ["gaitlab", "llcore"])


def test_parse_yaml_list_field_supports_inline_list():
    fm = (
        "title: hello\n"
        "tags: [llm, agent]\n"
        "related_groups: [gaitlab, llcore]\n"
    )
    assert qp.parse_yaml_list_field(fm, "tags") == ["llm", "agent"]
    assert qp.parse_yaml_list_field(fm, "related_groups") == ["gaitlab", "llcore"]


def test_parse_yaml_list_field_supports_inline_list_with_comment():
    fm = (
        "title: hello\n"
        "tags: [llm, agent]  # note\n"
        "related_groups: [gaitlab, llcore] # note\n"
    )
    assert qp.parse_yaml_list_field(fm, "tags") == ["llm", "agent"]
    assert qp.parse_yaml_list_field(fm, "related_groups") == ["gaitlab", "llcore"]


def test_parse_yaml_list_field_supports_single_quote_escape_in_inline_list():
    fm = "tags: ['AI''s note', c] # note\n"
    assert qp.parse_yaml_list_field(fm, "tags") == ["AI's note", "c"]


def test_parse_yaml_list_field_supports_scalar_csv_list():
    fm = "tags: FullSense, llcore, Singularity, AI, 解説\n"
    assert qp.parse_yaml_list_field(fm, "tags") == [
        "FullSense",
        "llcore",
        "Singularity",
        "AI",
        "解説",
    ]


def test_parse_yaml_list_field_supports_scalar_csv_list_with_comment():
    fm = "tags: FullSense, llcore, Singularity  # note\n"
    assert qp.parse_yaml_list_field(fm, "tags") == [
        "FullSense",
        "llcore",
        "Singularity",
    ]


def test_parse_yaml_list_field_supports_block_list_after_inline_comment_header():
    fm = "tags:  # note\n  - AI\n  - LLM\n"
    assert qp.parse_yaml_list_field(fm, "tags") == ["AI", "LLM"]


def test_parse_group_fields_allows_quotes_and_inline_comments():
    fm = (
        'title: hello\n'
        'project_group: "onocollo"  # note\n'
        "related_groups:\n"
        "  - gaitlab  # related\n"
        "  - 'llcore'\n"
    )
    assert qp.parse_group_fields(fm) == ("onocollo", ["gaitlab", "llcore"])


def test_resolve_frontmatter_title_strips_quotes_and_inline_comment():
    fm = 'title: "Visible title"  # note\n'
    assert qp.resolve_frontmatter_title(fm) == "Visible title"


def test_resolve_frontmatter_title_supports_single_quote_escape():
    fm = "title: 'AI''s title'\n"
    assert qp.resolve_frontmatter_title(fm) == "AI's title"


def test_resolve_frontmatter_title_supports_folded_block_scalar():
    fm = "title: >-\n  AI's first line\n  second line\n\n  third paragraph\n"
    assert qp.resolve_frontmatter_title(fm) == "AI's first line second line\nthird paragraph"


def test_resolve_frontmatter_title_strips_unquoted_inline_comment():
    fm = "title: Example title  # note\n"
    assert qp.resolve_frontmatter_title(fm) == "Example title"


def test_resolve_frontmatter_title_keeps_hash_when_part_of_title():
    fm = "title: 'Example article #25 — honest disclosure'\n"
    assert qp.resolve_frontmatter_title(fm) == "Example article #25 — honest disclosure"


def test_resolve_title_prefers_frontmatter_title_when_present():
    fm = 'title: "Visible title"  # note\n'
    body = "# 日本語\n\n# Fallback title\n"
    assert qp.resolve_title(fm, body) == "Visible title"


def test_parse_group_fields_keeps_last_related_group_without_trailing_newline():
    text = (
        "---\n"
        "title: hello\n"
        "project_group: onocollo\n"
        "related_groups:\n"
        "  - gaitlab\n"
        "  - onocollo\n"
        "---\n"
        "# body\n"
    )
    fm, body = qp.split_frontmatter(text)
    assert fm is not None
    assert body == "# body\n"
    assert qp.parse_group_fields(fm) == ("onocollo", ["gaitlab", "onocollo"])


def test_split_frontmatter_supports_crlf():
    text = "---\r\ntitle: hello\r\ntags: [a]\r\n---\r\n# body\r\n"
    fm, body = qp.split_frontmatter(text)
    assert fm == "title: hello\r\ntags: [a]"
    assert body == "# body\r\n"


def test_split_frontmatter_supports_bom_prefixed_text():
    text = "\ufeff---\n" "title: hello\n" "tags: [a]\n" "---\n" "# body\n"
    fm, body = qp.split_frontmatter(text)
    assert fm == "title: hello\ntags: [a]"
    assert body == "# body\n"


def test_split_frontmatter_allows_whitespace_around_delimiters():
    text = " --- \n" "title: hello\n" "tags: [a]\n" "\t---\t\n" "# body\n"
    fm, body = qp.split_frontmatter(text)
    assert fm == "title: hello\ntags: [a]"
    assert body == "# body\n"


def test_split_frontmatter_keeps_empty_frontmatter_and_leading_body_newline():
    text = "---\n---\n\n# body\n"
    fm, body = qp.split_frontmatter(text)
    assert fm == ""
    assert body == "\n# body\n"


def test_group_field_findings_accepts_canonical_groups():
    fm = (
        "title: hello\n"
        "project_group: gaitlab\n"
        "related_groups:\n"
        "  - spikelab\n"
        "  - onocollo\n"
    )
    assert qp.group_field_findings(fm, require_project_group=True) == []


def test_group_field_findings_accepts_llmesh_canonical_group():
    fm = "title: hello\nproject_group: llmesh\n"
    assert qp.group_field_findings(fm, require_project_group=True) == []


def test_group_field_findings_flags_unknown_and_group_in_related():
    fm = (
        "title: hello\n"
        "project_group: typo_group\n"
        "related_groups:\n"
        "  - typo_related\n"
        "  - typo_group\n"
    )
    assert qp.group_field_findings(fm, require_project_group=True) == [
        "[GROUP=typo_group]",
        "[RELATED=typo_related]",
        "[RELATED=typo_group]",
        "[GROUP-IN-RELATED]",
    ]


def test_group_field_findings_flags_missing_project_group_and_true_related_duplicates():
    fm = (
        "title: hello\n"
        "related_groups:\n"
        "  - gaitlab\n"
        "  - gaitlab\n"
    )
    assert qp.group_field_findings(fm, require_project_group=True) == [
        "[GROUP-MISSING]",
        "[RELATED-DUP]",
    ]


def test_is_publish_ready_draft_is_true_for_publish_control_frontmatter():
    fm = (
        "title: hello\n"
        "ignorePublish: true\n"
        "public_private: false\n"
    )
    assert qp.is_publish_ready_draft(fm) is True


def test_is_publish_ready_draft_is_false_for_plain_legacy_draft():
    fm = (
        "title: hello\n"
        "tags:\n"
        "  - AI\n"
    )
    assert qp.is_publish_ready_draft(fm) is False


def test_requires_project_group_skips_link_map_support_doc():
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#24_LINK_MAP.md")
    assert qp.requires_project_group(path, "title: hello\n", include_drafts=False) is False


def test_requires_project_group_for_public_article_path_is_true():
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#22_transformer_escape_status.md")
    assert qp.requires_project_group(path, "title: hello\n", include_drafts=False) is True


def test_requires_project_group_for_draft_path_is_false_without_include_drafts():
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_#48_gpu_wait_cpu_roundup_ja.md")
    assert qp.requires_project_group(path, "title: hello\n", include_drafts=False) is False


def test_requires_project_group_for_publish_ready_draft_with_group_metadata_is_true():
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_#48_gpu_wait_cpu_roundup_ja.md")
    fm = (
        "related_groups:\n"
        "  - onocollo\n"
        "public_id: abc123\n"
    )
    assert qp.requires_project_group(path, fm, include_drafts=True) is True


def test_requires_project_group_for_public_id_draft_without_group_metadata_is_true():
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_#45_honest_disclosure_anthology_ja.md")
    fm = (
        "title: hello\n"
        "public_id: abc123\n"
        "ignorePublish: true\n"
    )
    assert qp.requires_project_group(path, fm, include_drafts=True) is True


def test_requires_project_group_for_private_only_draft_without_group_metadata_is_true():
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_token_economy_ja.md")
    fm = (
        "title: hello\n"
        "private: true\n"
    )
    assert qp.requires_project_group(path, fm, include_drafts=True) is True


def test_requires_project_group_for_id_only_draft_without_group_metadata_is_true():
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_token_economy_en.md")
    fm = (
        "title: hello\n"
        "id: draft-id-123\n"
    )
    assert qp.requires_project_group(path, fm, include_drafts=True) is True


def test_requires_project_group_for_non_publish_ready_draft_is_false_even_with_group_metadata():
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_legacy_note.md")
    fm = (
        "related_groups:\n"
        "  - onocollo\n"
        "tags:\n"
        "  - AI\n"
    )
    assert qp.requires_project_group(path, fm, include_drafts=True) is False


def test_iter_targets_includes_drafts_only_when_requested(tmp_path, monkeypatch):
    articles = tmp_path / "docs" / "articles"
    drafts = articles / "drafts"
    drafts.mkdir(parents=True)
    root_file = articles / "QIITA_#01_root.md"
    draft_file = drafts / "QIITA_onocollo_draft.md"
    root_file.write_text("", encoding="utf-8")
    draft_file.write_text("", encoding="utf-8")

    monkeypatch.setattr(qp, "ROOT", articles)
    monkeypatch.setattr(qp, "DRAFTS", drafts)

    assert qp.iter_targets(include_drafts=False) == [root_file]
    assert qp.iter_targets(include_drafts=True) == [root_file, draft_file]


def test_resolve_title_falls_back_to_h1_when_frontmatter_title_is_missing():
    fm = "tags:\n  - AI\n"
    body = "# Visible title\n\nbody\n"
    assert qp.resolve_title(fm, body) == "Visible title"


def test_resolve_body_title_skips_language_heading_and_uses_real_h1():
    body = "# 日本語\n\n# Visible title\n\nbody\n"
    assert qp.resolve_body_title(body) == "Visible title"


def test_resolve_body_title_finds_real_h1_after_non_title_content():
    # Non-title content (a subheading + prose) before the real H1 does not stop
    # the scan: resolve_body_title skips it and still returns the later H1.
    body = "# 日本語\n\n## 導入\n\ntext\n\n# Visible title\n"
    assert qp.resolve_body_title(body) == "Visible title"


def test_resolve_body_title_ignores_fenced_code_headings():
    body = (
        "```md\n"
        "# Fake title in code\n"
        "```\n\n"
        "# 日本語\n\n"
        "```python\n"
        "# Another fake title\n"
        "```\n\n"
        "# Visible title\n"
    )
    assert qp.resolve_body_title(body) == "Visible title"


def test_resolve_body_title_respects_longer_backtick_fence_length():
    body = (
        "````md\n"
        "```inside\n"
        "# Fake title in 4-backtick fence\n"
        "```\n"
        "````\n\n"
        "# 日本語\n\n"
        "# Visible title\n"
    )
    assert qp.resolve_body_title(body) == "Visible title"


def test_resolve_body_title_skips_multiple_language_headings_until_real_h1():
    body = "# English\n\n# 日本語\n\n# Visible title\n"
    assert qp.resolve_body_title(body) == "Visible title"


def test_resolve_body_title_regression_from_real_multilingual_file():
    path = ROOT / "tools" / "qiita-cli-poc" / "public" / "qiita2401memorylayer.md"
    text = path.read_text(encoding="utf-8-sig")
    fm, body = qp.split_frontmatter(text)
    assert fm is not None
    assert qp.resolve_body_title(body) == "llive 完全解説 (1) — 「忘れない LLM」: 4 層メモリ + Bayesian surprise gating"


def test_title_findings_flags_mismatch_between_frontmatter_and_body_h1():
    fm = 'title: "Frontmatter title"\n'
    body = "# 日本語\n\n# Body title\n"
    assert qp.title_findings(fm, body) == ["[TITLE-MISMATCH]"]


def test_should_report_title_mismatch_is_false_for_legacy_live_mismatch_without_new_title_change(monkeypatch):
    fm = 'title: "Frontmatter title"\nid: public-item-id\n'
    body = "# 日本語\n\n# Body title\n"
    baseline = (
        "---\n"
        'title: "Frontmatter title"\n'
        "id: public-item-id\n"
        "---\n"
        "# 日本語\n\n# Body title\n"
    )
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md")
    assert qp.should_report_title_mismatch(path, fm, body) is False


def test_should_report_title_mismatch_is_true_for_unconnected_local_mismatch(monkeypatch):
    fm = 'title: "Frontmatter title"\n'
    body = "# 日本語\n\n# Body title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: None)
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_local_only.md")
    assert qp.should_report_title_mismatch(path, fm, body) is True


def test_should_report_title_mismatch_is_false_for_team_draft_id_mismatch_without_publish_title_change(monkeypatch):
    fm = 'title: "Frontmatter title"\nid: team-item-id\n'
    body = "# 日本語\n\n# Body title\n"
    baseline = (
        "---\n"
        'title: "Frontmatter title"\n'
        "id: team-item-id\n"
        "---\n"
        "# 日本語\n\n# Older body title\n"
    )
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_team_only.md")
    assert qp.should_report_title_mismatch(path, fm, body) is False


def test_has_publish_identity_treats_nullish_public_id_as_absent():
    assert qp.has_publish_identity("public_id: abc123\n") is True
    assert qp.has_publish_identity("public_id: null\n") is False
    assert qp.has_publish_identity("public_id: ''\n") is False


def test_has_live_identity_normalizes_nullish_ids():
    draft_path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_team_draft.md")
    public_path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#01_article.md")
    assert qp.has_live_identity(draft_path, "id: team-id-123\n") is True
    assert qp.has_live_identity(draft_path, "public_id: abc123\n") is True
    assert qp.has_live_identity(draft_path, "id: none\n") is False
    assert qp.has_live_identity(draft_path, "public_id: \"\"\n") is False
    assert qp.has_live_identity(draft_path, "qiita_public_id: legacy-only\n") is False
    assert qp.has_live_identity(public_path, "id: team-id-123\n") is False


def test_parse_scalar_value_keeps_unquoted_hash_when_comment_stripping_disabled():
    assert qp.parse_scalar_value("Title #37") == "Title #37"


def test_requires_title_sync_skips_link_map_support_doc():
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#24_LINK_MAP.md")
    assert qp.requires_title_sync(path) is False


def test_requires_title_sync_for_public_article_path_is_true():
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#22_transformer_escape_status.md")
    assert qp.requires_title_sync(path) is True


def test_title_change_requires_human_gate_is_false_for_body_only_diff_when_frontmatter_title_is_stable(monkeypatch):
    fm = "title: hello\npublic_id: abc123\n"
    body = "# 日本語\n\n# New title\n"
    baseline = "---\ntitle: hello\npublic_id: abc123\n---\n# 日本語\n\n# Old title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_#48_gpu_wait_cpu_roundup_ja.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_is_false_for_team_draft_body_only_diff_when_frontmatter_title_is_stable(monkeypatch):
    fm = "title: hello\nid: team-or-mirror-id\n"
    body = "# 日本語\n\n# New title\n"
    baseline = "---\ntitle: hello\nid: team-or-mirror-id\n---\n# 日本語\n\n# Old title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_team_only.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_is_false_for_public_article_id_only_legacy_path(monkeypatch):
    fm = "title: hello\nid: team-or-mirror-id\n"
    body = "# 日本語\n\n# New title\n"
    baseline = "---\ntitle: hello\nid: team-or-mirror-id\n---\n# 日本語\n\n# Old title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#22_transformer_escape_status.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_is_false_for_qiita_public_id_only(monkeypatch):
    fm = "title: hello\nqiita_public_id: legacy-team-id\n"
    body = "# 日本語\n\n# New title\n"
    baseline = "---\ntitle: hello\nqiita_public_id: legacy-team-id\n---\n# 日本語\n\n# Old title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#23_15h_marathon_mid_report.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_is_false_without_publish_identity(monkeypatch):
    fm = "title: hello\n"
    body = "# 日本語\n\n# New title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(
        qp,
        "load_git_text_at_rev",
        lambda rev, path: "---\ntitle: hello\n---\n# 日本語\n\n# Old title\n" if rev == "BASE" else None,
    )
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_onocollo_worldmodel_alife_ja.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_is_false_for_non_title_h1_addition(monkeypatch):
    fm = "title: hello\npublic_id: abc123\n"
    body = "# 日本語\n\n# Stable title\n\n## Added section\n"
    baseline = "---\ntitle: hello\npublic_id: abc123\n---\n# 日本語\n\n# Stable title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#22_transformer_escape_status.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_uses_branch_baseline_but_stays_false_for_body_only_diff(monkeypatch):
    fm = "title: hello\npublic_id: abc123\n"
    body = "# 日本語\n\n# New title\n"
    baseline = "---\ntitle: hello\npublic_id: abc123\n---\n# 日本語\n\n# Old title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#25_monoculture_evolution_lldarwin.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_is_true_for_frontmatter_only_diff_when_publish_title_changes(monkeypatch):
    fm = "title: New frontmatter title\npublic_id: abc123\n"
    body = "# 日本語\n\n# Stable body title\n"
    baseline = (
        "---\n"
        "title: Old frontmatter title\n"
        "public_id: abc123\n"
        "---\n"
        "# 日本語\n\n# Stable body title\n"
    )
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is True


def test_title_change_requires_human_gate_is_true_if_identity_removed_but_publish_title_changed_from_baseline(monkeypatch):
    fm = "title: New frontmatter title\n"
    body = "# 日本語\n\n# Stable body title\n"
    baseline = (
        "---\n"
        "title: Old frontmatter title\n"
        "public_id: abc123\n"
        "---\n"
        "# 日本語\n\n# Stable body title\n"
    )
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#26_lldarwin_multi_pressure_selection.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is True


def test_title_change_requires_human_gate_is_false_when_worktree_matches_baseline(monkeypatch):
    fm = "title: New frontmatter title\npublic_id: abc123\n"
    body = "# 日本語\n\n# Stable body title\n"
    baseline = (
        "---\n"
        "title: New frontmatter title\n"
        "public_id: abc123\n"
        "---\n"
        "# 日本語\n\n# Stable body title\n"
    )
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_is_true_when_branch_baseline_diff_changes_frontmatter_publish_title(monkeypatch):
    fm = "title: New frontmatter title\npublic_id: abc123\n"
    body = "# 日本語\n\n# Stable body title\n"
    baseline = (
        "---\n"
        "title: Old frontmatter title\n"
        "public_id: abc123\n"
        "---\n"
        "# 日本語\n\n# Stable body title\n"
    )
    head = (
        "---\n"
        "title: New frontmatter title\n"
        "public_id: abc123\n"
        "---\n"
        "# 日本語\n\n# Stable body title\n"
    )

    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")

    def fake_load(rev, path):
        if rev == "BASE":
            return baseline
        if rev == "HEAD":
            return head
        return None

    monkeypatch.setattr(qp, "load_git_text_at_rev", fake_load)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is True


def test_title_change_requires_human_gate_persists_after_commit_relative_to_branch_baseline_when_publish_title_changed(monkeypatch):
    fm = "title: New frontmatter title\npublic_id: abc123\n"
    body = "# 日本語\n\n# New publish title\n"
    baseline = (
        "---\n"
        "title: Old frontmatter title\n"
        "public_id: abc123\n"
        "---\n"
        "# 日本語\n\n# Old publish title\n"
    )

    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is True


def test_title_change_requires_human_gate_for_publish_connected_promotion_from_baseline_without_identity(monkeypatch):
    fm = "title: New draft title\npublic_id: abc123\n"
    body = "# 日本語\n\n# New draft title\n"
    baseline = (
        "---\n"
        "title: Old draft title\n"
        "---\n"
        "# 日本語\n\n# Old draft title\n"
    )
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_#48_gpu_wait_cpu_roundup_ja.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is True


def test_title_change_requires_human_gate_when_frontmatter_is_newly_added_to_legacy_baseline(monkeypatch):
    fm = "title: New frontmatter title\npublic_id: abc123\n"
    body = "# 日本語\n\n# New frontmatter title\n"
    baseline = "# 日本語\n\n# Old legacy title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is True


def test_title_change_requires_human_gate_is_false_when_frontmatter_added_but_publish_title_same(monkeypatch):
    fm = "title: Same publish title\npublic_id: abc123\n"
    body = "# 日本語\n\n# Same publish title\n"
    baseline = "# 日本語\n\n# Same publish title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: baseline if rev == "BASE" else None)
    path = Path(r"D:\projects\fullsense\docs\articles\QIITA_#01_brief_api_progressive.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is False


def test_title_change_requires_human_gate_is_true_for_new_publish_connected_file_without_baseline(monkeypatch):
    fm = "title: New publish title\npublic_id: abc123\n"
    body = "# 日本語\n\n# New publish title\n"
    qp.load_hitl_baseline_text.cache_clear()
    monkeypatch.setattr(qp, "resolve_hitl_baseline_commit", lambda: "BASE")
    monkeypatch.setattr(qp, "load_git_text_at_rev", lambda rev, path: None)
    path = Path(r"D:\projects\fullsense\docs\articles\drafts\QIITA_#48_gpu_wait_cpu_roundup_ja.md")
    assert qp.title_change_requires_human_gate(path, fm, body) is True


def test_resolve_hitl_baseline_commit_falls_back_when_upstream_missing(monkeypatch):
    qp.resolve_upstream_ref.cache_clear()
    qp.resolve_hitl_baseline_commit.cache_clear()

    def fake_exists(ref: str) -> bool:
        return ref == "main"

    class Result:
        def __init__(self, stdout: str):
            self.stdout = stdout

    def fake_run(args, **kwargs):
        if args[:2] == ["git", "merge-base"]:
            return Result("abc123\n")
        raise AssertionError(f"unexpected command: {args}")

    monkeypatch.setattr(qp, "git_ref_exists", fake_exists)
    monkeypatch.setattr(qp, "resolve_upstream_ref", lambda: None)
    monkeypatch.setattr(qp.subprocess, "run", fake_run)
    assert qp.resolve_hitl_baseline_commit() == "abc123"


def test_resolve_hitl_baseline_commit_falls_back_to_empty_tree_without_parent(monkeypatch):
    qp.resolve_upstream_ref.cache_clear()
    qp.resolve_hitl_baseline_commit.cache_clear()

    monkeypatch.setattr(qp, "resolve_upstream_ref", lambda: None)
    monkeypatch.setattr(qp, "git_ref_exists", lambda ref: ref == "HEAD")
    assert qp.resolve_hitl_baseline_commit() == qp.EMPTY_TREE_HASH


def test_load_git_text_at_rev_uses_repo_root_as_cwd(monkeypatch, tmp_path):
    qp.load_git_text_at_rev.cache_clear()
    target = Path("docs/articles/QIITA_#01_test.md")
    seen = {}

    class Result:
        def __init__(self):
            self.returncode = 0
            self.stdout = "hello"

    def fake_run(args, **kwargs):
        seen["cwd"] = kwargs.get("cwd")
        return Result()

    monkeypatch.setattr(qp.subprocess, "run", fake_run)
    assert qp.load_git_text_at_rev("HEAD", str(target)) == "hello"
    assert seen["cwd"] == qp.REPO_ROOT


def test_main_prints_warning_breakdown_for_hitl(monkeypatch, tmp_path, capsys):
    article = tmp_path / "QIITA_#01_test.md"
    article.write_text(
        "---\n"
        "title: Title\n"
        "tags: [FullSense]\n"
        "project_group: llive\n"
        "public_id: abc123\n"
        "---\n"
        "# 日本語\n\n# Title\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(qp, "ROOT", tmp_path)
    monkeypatch.setattr(qp, "DRAFTS", tmp_path / "drafts")
    monkeypatch.setattr(
        qp,
        "parse_args",
        lambda: type("Args", (), {"include_drafts": False, "json": False})(),
    )
    monkeypatch.setattr(
        qp,
        "resolve_hitl_baseline_commit",
        lambda: "BASE",
    )
    monkeypatch.setattr(
        qp,
        "load_git_text_at_rev",
        lambda rev, path: (
            "---\n"
            "title: Old title\n"
            "tags: [FullSense]\n"
            "project_group: llive\n"
            "public_id: abc123\n"
            "---\n"
            "# 日本語\n\n# Old title\n"
        )
        if rev == "BASE"
        else None,
    )

    rc = qp.main()
    out = capsys.readouterr().out
    assert rc == 1
    assert "Warning breakdown: TITLE_HITL=1" in out
    assert 'Warning breakdown JSON: {"TITLE_HITL": 1}' in out
    assert 'Warning files JSON: {"TITLE_HITL": ["QIITA_#01_test.md"]}' in out


def test_main_prints_empty_json_when_no_warnings(monkeypatch, tmp_path, capsys):
    article = tmp_path / "QIITA_#01_test.md"
    article.write_text(
        "---\n"
        "title: Title\n"
        "tags: [FullSense]\n"
        "project_group: llive\n"
        "---\n"
        "# 日本語\n\n# Title\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(qp, "ROOT", tmp_path)
    monkeypatch.setattr(qp, "DRAFTS", tmp_path / "drafts")
    monkeypatch.setattr(
        qp,
        "parse_args",
        lambda: type("Args", (), {"include_drafts": False, "json": False})(),
    )

    rc = qp.main()
    out = capsys.readouterr().out
    assert rc == 0
    assert "Warning breakdown: (none)" in out
    assert "Warning breakdown JSON: {}" in out
    assert "Warning files JSON: {}" in out


def test_main_json_mode_emits_single_machine_readable_object(monkeypatch, tmp_path, capsys):
    article = tmp_path / "QIITA_#01_test.md"
    article.write_text(
        "---\n"
        "title: Title\n"
        "tags: [FullSense]\n"
        "project_group: llive\n"
        "public_id: abc123\n"
        "---\n"
        "# 日本語\n\n# Title\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(qp, "ROOT", tmp_path)
    monkeypatch.setattr(qp, "DRAFTS", tmp_path / "drafts")
    monkeypatch.setattr(
        qp,
        "parse_args",
        lambda: type("Args", (), {"include_drafts": False, "json": True})(),
    )
    monkeypatch.setattr(
        qp,
        "resolve_hitl_baseline_commit",
        lambda: "BASE",
    )
    monkeypatch.setattr(
        qp,
        "load_git_text_at_rev",
        lambda rev, path: (
            "---\n"
            "title: Old title\n"
            "tags: [FullSense]\n"
            "project_group: llive\n"
            "public_id: abc123\n"
            "---\n"
            "# 日本語\n\n# Old title\n"
        )
        if rev == "BASE"
        else None,
    )

    rc = qp.main()
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert rc == 1
    assert payload == {
        "total_files": 1,
        "warnings": 1,
        "counts": {"TITLE_HITL": 1},
        "files": {"TITLE_HITL": ["QIITA_#01_test.md"]},
    }


def test_main_json_mode_emits_empty_maps_when_clean(monkeypatch, tmp_path, capsys):
    article = tmp_path / "QIITA_#01_test.md"
    article.write_text(
        "---\n"
        "title: Title\n"
        "tags: [FullSense]\n"
        "project_group: llive\n"
        "---\n"
        "# 日本語\n\n# Title\n",
        encoding="utf-8",
    )

    monkeypatch.setattr(qp, "ROOT", tmp_path)
    monkeypatch.setattr(qp, "DRAFTS", tmp_path / "drafts")
    monkeypatch.setattr(
        qp,
        "parse_args",
        lambda: type("Args", (), {"include_drafts": False, "json": True})(),
    )

    rc = qp.main()
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert rc == 0
    assert payload == {
        "total_files": 1,
        "warnings": 0,
        "counts": {},
        "files": {},
    }


def test_main_handles_utf8_bom_frontmatter(monkeypatch, tmp_path, capsys):
    article = tmp_path / "QIITA_#01_test.md"
    article.write_text(
        "---\n"
        "title: Title\n"
        "tags: [FullSense]\n"
        "project_group: llive\n"
        "---\n"
        "# 日本語\n\n# Title\n",
        encoding="utf-8-sig",
    )

    monkeypatch.setattr(qp, "ROOT", tmp_path)
    monkeypatch.setattr(qp, "DRAFTS", tmp_path / "drafts")
    monkeypatch.setattr(
        qp,
        "parse_args",
        lambda: type("Args", (), {"include_drafts": False, "json": True})(),
    )

    rc = qp.main()
    out = capsys.readouterr().out.strip()
    payload = json.loads(out)
    assert rc == 0
    assert payload["warnings"] == 0
