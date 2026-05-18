---
layout: default
title: "Doc Map"
nav_order: 3
---

# FullSense ™ — Document Map

> One-page map of every doc spread across the FullSense umbrella + product
> repos + maintainer memory. Use this when the work is split across more
> than one repo (which is almost always).

## Portal (this repo, furuse-kazufumi/fullsense)

| File | What's in it |
|---|---|
| [`docs/index.md`]({{ '/' | relative_url }}) | landing page, Family Tree, Product Sites, Reference hubs (2026-05-18 追加) |
| [`docs/roadmap.md`]({{ '/roadmap' | relative_url }}) | live + planned + parked products + ステータス遷移モデル / 依存グラフ / タイムライン (2026-05-18 拡張) |
| [`docs/comparison.md`]({{ '/comparison' | relative_url }}) | honest vs Claude Code / Perplexity / Codex / Gemini + Honest disclosure (2026-05-18) |
| [`docs/PROGRESS.md`]({{ '/PROGRESS' | relative_url }}) | portal-side changelog (Phase 0.4 まで) |
| [`docs/NOTES.md`]({{ '/NOTES' | relative_url }}) | design notes, link-rot watch (hub 含む) |
| [`docs/NEXT_SESSION.md`]({{ '/NEXT_SESSION' | relative_url }}) | handoff to the next agent run |
| [`docs/doc_map.md`]({{ '/doc_map' | relative_url }}) | this page |

### Reference hubs (2026-05-18 追加 — drift 防止用)

| File | What's in it |
|---|---|
| [`docs/spec/index.md`]({{ '/spec/' | relative_url }}) | FullSense Eternal Spec v1.1 章直リンク + 要件定義 8 本一覧 |
| [`docs/benchmarks/policy.md`]({{ '/benchmarks/policy/' | relative_url }}) | ベンチ三本柱 (purity / progressive curve / honest disclosure) + 運用チェックリスト |
| [`docs/recommended-models.md`]({{ '/recommended-models/' | relative_url }}) | 用途別推奨 on-prem モデル + llama3.2:3b 非推奨根拠 + install スニペット |

### Benchmarks (under `docs/benchmarks/`)

| File | What's in it |
|---|---|
| [`PLAN_progressive_model_brief.md`]({{ '/benchmarks/PLAN_progressive_model_brief' | relative_url }}) | model × brief size matrix test plan |
| [`2026-05-16_mermaid_brief.md`]({{ '/benchmarks/2026-05-16_mermaid_brief' | relative_url }}) | Brief A/B: Mermaid generation (llive + ollama + Perplexity + 3 cloud fail) |
| [`2026-05-16_quickstart_seqdiag.md`]({{ '/benchmarks/2026-05-16_quickstart_seqdiag' | relative_url }}) | Brief A/B: Quick Start + Sequence diagram |
| [`2026-05-16_lltrade_yaml.md`]({{ '/benchmarks/2026-05-16_lltrade_yaml' | relative_url }}) | Brief A/B: lltrade paper-trading YAML |
| [`2026-05-16_vlm.md`]({{ '/benchmarks/2026-05-16_vlm' | relative_url }}) | VLM A/B: og-card description |
| [`2026-05-16_progressive_llive.md`]({{ '/benchmarks/2026-05-16_progressive_llive' | relative_url }}) | llive 5-size progressive (rule-based) |
| `2026-05-16-matrix/matrix_summary.md` | llive × ollama models × brief sizes matrix |
| `2026-05-16-quiz-{debug,release}/quiz_summary.md` | 10-quiz reasoning probe through llive |

### Scripts (under `scripts/`)

| File | Purpose |
|---|---|
| `verify_publication.sh` | one-shot Pages / portal links / branch protection / About verify |
| `bench_run.py` | replay 4 Briefs × 6 cloud/on-prem models (llive single-product mode) |
| `bench_vlm.py` | same shape for vision models |
| `bench_model_brief_matrix.py` | llive × ollama-models × brief-sizes matrix |
| `bench_quiz.py` | 10-quiz reasoning probe through llive (5 categories × 2 difficulties) |

## llive (furuse-kazufumi/llive)

### Specs + requirements

| File | What's in it |
|---|---|
| `docs/fullsense_spec_eternal.md` | normative FullSense Spec v1.1 (§§1-22). §21 = "Differentiation vs current AI agent paradigms" |
| `docs/requirements_v0.1.md` | initial 6-layer + sub-block requirements |
| `docs/requirements_v0.2_addendum.md` | TRIZ-derived FR-12..FR-22 + §5 "差別化軸" (4-axis intersection) |
| `docs/requirements_v0.3_triz_self_evolution.md` | self-evolving TRIZ engine (FR-23..FR-27) |
| `docs/requirements_v0.4_llm_wiki.md` | Karpathy-style LLM Wiki integration (LLW-01..LLW-08) |
| `docs/requirements_v0.5_spatial_memory.md` | 3D Gaussian / CAD spatial memory (FR-29..) |
| `docs/requirements_v0.6_concurrency.md` | concurrency requirements |
| `docs/requirements_v0.7_rust_acceleration.md` | Rust acceleration plan (RUST-01..RUST-14) |

### Architecture + ops

| File | What's in it |
|---|---|
| `docs/architecture.md` | top-level architecture |
| `docs/data_model.md` | memory tier schemas |
| `docs/family_integration.md` | llmesh + llove + lldesign + lltrade integration |
| `docs/mcp_integration.md` | MCP server tool definitions |
| `docs/security_model.md` | threat model + zone trust |
| `docs/PROGRESS.md` | maintainer's session-by-session changelog (続 1..続 14+ format) |

### LLM benchmark + bug docs (2026-05-16 session)

| File | What's in it |
|---|---|
| `docs/BUGS_2026-05-16_brief_ab.md` | 8 gaps from Brief A/B run, **LLIVE-001 corrected to "Wired" 2026-05-16** |
| `docs/proposals/brief_api_design.md` | v0.7 Brief API + LLMBackend wiring design draft |
| `scripts/run_brief.py` | single-Brief probe (supports `--json`, `--debug`) |

### Source (key modules)

| Module | What it is |
|---|---|
| `src/llive/fullsense/loop.py` | the 6-stage FullSenseLoop. As of 2026-05-16 wires `LLMBackend` opt-in + `debug=True` trace |
| `src/llive/fullsense/runner.py` | ResidentRunner (fast/medium/slow timescales) |
| `src/llive/fullsense/sandbox.py` | SandboxOutputBus + SandboxRecord |
| `src/llive/llm/backend.py` | LLMBackend + Ollama/Anthropic/OpenAI/Mock implementations (shipped Phase C-1.0) |
| `src/llive/approval/bus.py` | C-1 Approval Bus + Policy |
| `src/llive/approval/ledger.py` | SQLite Ledger (C-1) |
| `src/llive/mcp/server.py` | MCP server (Phase C-1, 7 tools) |

## llmesh / llove / lldesign / lltrade

| Repo | Key docs |
|---|---|
| [llmesh](https://github.com/furuse-kazufumi/llmesh) | `docs/SPECIFICATION.md`, `docs/ARCHITECTURE.md`, `docs/demos/clustering_demo.md` |
| [llove](https://github.com/furuse-kazufumi/llove) | `docs/scenarios/`, `docs/scenarios/anim/shogi/` |
| [lldesign](https://github.com/furuse-kazufumi/lldesign) | `docs/index.md`, `docs/SPEC.md`, `docs/PROGRESS.md`, `docs/NOTES.md` |
| [lltrade](https://github.com/furuse-kazufumi/lltrade) | same shape as lldesign, plus 3-layer paper-only safety pin |

## Maintainer memory (raptor repo + ~/.claude/.../memory/)

| File | What's in it |
|---|---|
| `project_fullsense_brand.md` | brand & product family ledger |
| `project_llive*` (multiple) | llive 9-axis skeleton progress, RAD integration, v0.6 legal, ... |
| `project_llive_bug_2026_05_16.md` | 8 bugs from the A/B run (LLIVE-001 corrected) |
| `project_llive_ci_observation_2026_05_16.md` | llive CI failure observation |
| `project_benchmark_2026_05_16.md` | 3 Brief × 6 model A/B results |
| `feedback_competitor_benchmark.md` | Claude Code / Perplexity / Codex / Gemini benchmark methodology |
| `feedback_benchmark_progressive_tokens.md` | xs/s/m/l/xl brief-size methodology |
| `feedback_llive_measurement_purity.md` | llive single-product vs cloud-API direct (purity guard) |
| `feedback_implementation_status_record.md` | 4-tier status (実装済/未配線/部分実装/未実装) |
| `feedback_webpage_research_first.md` | Pages / kramdown / Mermaid pitfalls |

## Maintenance rule

- When a new doc lands under any `docs/`, add a row above and link it.
- When a script under `scripts/` is added or changes purpose, update the
  Scripts row.
- When a new maintainer memory is created, add it under the Memory section.
- One-line entries. Long-form lives in the doc itself.
