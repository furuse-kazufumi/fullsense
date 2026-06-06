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
| [`docs/NEXT_SESSION.md`]({{ '/NEXT_SESSION' | relative_url }}) | handoff to the next agent run (人手, 方向性メモ) |
| [`docs/NEXT_SESSION.auto.md`]({{ '/NEXT_SESSION.auto' | relative_url }}) | Stop hook 自動上書き (git/test/operator status snapshot) |
| [`docs/doc_map.md`]({{ '/doc_map' | relative_url }}) | this page |

### Reference hubs (2026-05-18 追加 — drift 防止用)

| File | What's in it |
|---|---|
| [`docs/spec/index.md`]({{ '/spec/' | relative_url }}) | FullSense Eternal Spec v1.1 章直リンク + 要件定義 8 本一覧 |
| [`docs/benchmarks/policy.md`]({{ '/benchmarks/policy/' | relative_url }}) | ベンチ三本柱 (purity / progressive curve / honest disclosure) + 運用チェックリスト |
| [`docs/recommended-models.md`]({{ '/recommended-models/' | relative_url }}) | 用途別推奨 on-prem モデル + llama3.2:3b 非推奨根拠 + install スニペット |
| [`docs/cognitive-mesh.md`]({{ '/cognitive-mesh/' | relative_url }}) | llive v0.8 cognitive mesh (COG-MESH-01〜10) の portal 視点 overview、統合 demo の触り方、10/10 skeleton 完了 |

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
| `gen_next_session_auto.py` | `docs/NEXT_SESSION.auto.md` を毎ターン上書き (raptor Stop hook 連動, 2026-05-20 追加) |

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

### Research docs (under `docs/research/`) — 2026-05-25〜27 追加分

| File | What's in it |
|---|---|
| `repir_mcp_compat_2026_05_23` | llrepr MCP structuredContent 配線 + RepIR→llrepr 改名経緯 |
| `spec_mesh_wiring_2026_05_25` | SPEC-MESH-02/03/04 配線完了 + security 修正報告 |
| `evolution_research_openendedness_2026_05_25` | proxy 進化の自明収束分析 + open-endedness 手法 (novelty/QD/MAP-Elites) 整理 |
| `evolution_research_algorithm_survey_2026_05_25` | ε-lexicase / NSGA / island / UCB1 AOS 等を llive 文脈で評価した横断調査 |
| `evolution_research_representation_selection_2026_05_25` | genome 表現 + 選択圧手法の組み合わせ評価 |
| `evolution_research_culture_learning_2026_05_25` | 文化染色体 / belief space / persona pull 要件化 (Stream D) |
| `evolution_research_meta_2026_05_25` | meta-EA (CMA-ES / GESMR / ANAS) の SOTA と llive 適用可否 |
| `evolution_research_safety_2026_05_25` | 開放端エージェントの安全設計 + Approval Bus 迂回防止 |
| `evolution_fitness_redesign_2026_05_25` | 多峰・多目的 fitness 再設計。"is it really evolving?" |
| `evolution_design_tensions_open_decisions_2026_05_25` | 開放端進化の未解決設計対立 (open decisions) 一覧 |
| `evolution_poc_experiment_design_2026_05_25` | PoC 実験設計プロトコル (sandbox / metrics / stop criterion) |
| `evolution_poc_deployment_results_2026_05_25` | deployment sweep 結果 + honest disclosure (飽和パターン) |
| `evolution_visualization_plan_2026_05_25` | evolution.svg 現状評価 + 3DGS 方向への可視化ロードマップ |
| `evolution_visualization_advanced_2026_05_25` | ALife / Karl Sims 先例から llive 独自表現空間の位置づけ |
| `evolution_viz_viewing_guide_2026_05_25` | 進化ラン出力ファイルの閲覧手順 (ツール・コマンド) |
| `llove_qt_gui_architecture_2026_05_25` | llove Textual → Qt 移行設計。ll 系統合フロント構想 |
| `openended_evo_sota_perplexity_2026_05_26` | Perplexity による QD/novelty/ORCH white-space 確認 |
| `lldarwin_v2_poc_marathon_2026_05_26` | overnight PoC マラソン全記録 + 確定方策 (ORCH/QD 等) の**正本** |
| `lldarwin_stage1_results_2026_05_26` | MultiPressureSelector + ORCH 基盤 Stage1 実装結果 |
| `lldarwin_v2_ops_readiness_2026_05_27` | 連続稼働向け動作テスト結果 + ready/blocked 一覧 |
| `mythos_competitor_spec_2026_05_27` | **Goal「進化型で Claude Mythos 超え」競合スペック台帳**。Mythos 公開数値(Cybench 100%/ExploitBench ACE 18/41)を proxy バー固定 + 確定 harness(InterCode-CTF→Cybench) + on-prem 在庫 |
| `mythos_surpass_design_2026_05_27` | **同 Goal 設計正本**。生成(llive 進化)×検証(RAPTOR 決定論オラクル)×無制限 test-time compute。RAD 先行研究 + PoC-CTF-0 進捗(coverage@k harness) |

### Scripts (追加分 2026-05-25〜27)

| File | Purpose |
|---|---|
| `scripts/research_pocs/poc_agentic_2026_05_26.py` | agentic 個体 PoC (コスト選択的調査創発) |
| `scripts/research_pocs/poc_factor_subspace_qd_2026_05_26.py` | factor-subspace QD PoC |
| `scripts/research_pocs/poc_orchestra_headroom_2026_05_26.py` | オーケストラ headroom 計測 PoC |
| `scripts/research_pocs/poc_router_2026_05_26.py` | competence-aware router PoC |
| `scripts/research_pocs/poc_saturation_fixes_2026_05_26.py` | 飽和修正手法 PoC |
| `docs/research/llcore_cpu_poc_battery_completion_2026_05_29.md` | llcore Stage 0-2 完成 (39 gates / 76 tests / Codex 5/5 Green) |
| `docs/research/gate_taxonomy_audit_2026_06_06.md` | A-Evolve 三重検問の棚卸し + 検問体系化監査 (llcore/llive/raptor/lleval/llmesh の gate 対応表・gap 分析・TOP-3) |
| `docs/research/classics_dna_mapping_2026_06_06.md` | 孫子13篇+論語から差別化 trait を 20 原理抽出 → (a)研究戦略/(b)設計遺伝子/(c)検問統治 に写像。新設遺伝子座 G14-G18 提案。llive ontology に sun-tzu-strategist/confucius ペルソナ追加 |
| `docs/research/differentiation_audit_dna_roadmap_2026_06_06.md` | 敵対的差別化監査の確定結果 (56 agents, breaks 0/narrows 36) + 特別 DNA ロードマップ。四点交差点の生存確認、D1'-D4' クレーム再定義、防御壁 15 件、Phase 0-4 優先度計画 (計画→小PoC→大PoC→組込み) |
| `docs/research/master_plan_2026_06_06.md` | 包括計画: 5 トラック (llcore 本線/llive+Sakana/発信/防御調査/台帳掃除) に全やり残しを統合、次 3 セッションの推奨実行順 + user-gate 一覧 |
| `docs/research/patent_search_2026_06_06.md` | 特許 DB 照会 (T4 4-1): 結論 clear — 四点交差点の特許ゼロ、narrows 弱 2 件は related work で対比推奨。D2' は出願でも先取り可能 (user 判断) |
| `docs/papers/2026-05-29_core_evolution_master_survey.md` | Core Evolution master survey (Agent A-D + RAD 14 分野) |
| `docs/papers/2026-05-29_research_plan_core_evolution.md` | 研究計画書 v1 (TMLR 本命) |

## Maintenance rule

- When a new doc lands under any `docs/`, add a row above and link it.
- When a script under `scripts/` is added or changes purpose, update the
  Scripts row.
- When a new maintainer memory is created, add it under the Memory section.
- One-line entries. Long-form lives in the doc itself.
