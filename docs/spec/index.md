---
layout: default
title: "Spec"
nav_order: 40
has_children: false
permalink: /spec/
---

# FullSense ™ — Spec hub

> 仕様の **真実ソースは [llive リポ](https://github.com/furuse-kazufumi/llive)**。
> 本ページは portal 側のナビゲーション・ハブ。drift を防ぐためにフル文書を
> ミラーせず、章タイトル + 直接リンクで構成する。

## 公式 Spec: `fullsense.eternal v1.1.0`

| meta | value |
|---|---|
| spec id | `fullsense.eternal` |
| version | `1.1.0` (2026-05-15) |
| status | normative draft |
| 真実ソース | [`llive/docs/fullsense_spec_eternal.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md) |
| ライセンス | Apache-2.0 (code 部) + Commercial dual-license |
| 著者 | Furuse Kazufumi (古瀬 和文) |

> *A specification of autonomous-resident cognition meant to hold across
> substrates, civilizations, and millennia — independent of the
> implementation language, physical substrate, cultural value framework,
> and time scale of the underlying agent.*

## なぜ「FullSense」か

著者の苗字 **Furuse (古瀬)** に由来。さらに author given name *Kazufumi*
(和文) は二重読解で spec の中核に load-bearing で組み込まれている:

1. **和 (kazu, 数) + 文 (fumi, 一歩 / 行)** — 「多くの経験を踏み歩く」
   → §A6 (evolution requires inner + outer signal) / §E1–E4 / §OP-SING に
   反映
2. **和 (wa, 調和) × 文 (written line)** — Session × Context × Prompt の
   調和的融合 → §I1 (provenance) / §R2 (multi-timescale loops) /
   §22.3 step 4 に反映

両読解とも保存され、後の amendments で失われない。

## 章立て (TOC + 直接リンク)

`llive/docs/fullsense_spec_eternal.md` の各章へ直接アンカー:

| § | 章タイトル | 用途 |
|---|---|---|
| 0 | [Reading guide](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#0-reading-guide) | 読み方の前置き |
| 1 | [Axioms](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#1-axioms) | 公理群 |
| 2 | [Structural invariants](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#2-structural-invariants) | 不変条件 |
| 3 | [Trigger genesis](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#3-trigger-genesis) | trigger 発生 |
| 4 | [Resident cognition](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#4-resident-cognition) | 常駐認知 |
| 5 | [The thought filter (`F*`)](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#5-the-thought-filter-f) | 思考フィルタ |
| 6 | [Action system](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#6-action-system) | 行動系 |
| 7 | [Self-evolution](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#7-self-evolution) | 自己進化 |
| 8 | [Ethical boundaries](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#8-ethical-boundaries) | 倫理境界 |
| 9 | [Mortality protocol](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#9-mortality-protocol) | 寿命プロトコル |
| 10 | [Millennial invariants](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#10-millennial-invariants) | 千年スケール不変条件 |
| 11 | [Verification](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#11-verification) | 検証 |
| 12 | [Threat model (abridged)](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#12-threat-model-abridged) | 脅威モデル |
| 13 | [Amendment procedure](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#13-amendment-procedure) | 改訂手順 |
| 14 | [Relationship to existing thought](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#14-relationship-to-existing-thought) | 既存思想との関係 |
| 15 | [Conformance levels](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#15-conformance-levels) | 適合度レベル |
| 16 | [Glossary](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#16-glossary) | 用語集 |
| 17 | [Open questions](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#17-open-questions) | 未解決問 |
| 18 | [Appendix A — Conformance checklist](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#18-appendix-a--conformance-checklist-machine-friendly) | 適合度チェックリスト |
| 19 | [Appendix B — Lineage](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#19-appendix-b--lineage-of-this-document) | 系譜 |
| 20 | [Superhuman scope (`SHS*`)](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#20-superhuman-scope-shs--what-makes-fullsense-not-a-human-emulator) | 人間エミュレータ脱却 |
| 21 | [Differentiation — vs current AI agent paradigms](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#21-differentiation--vs-current-ai-agent-paradigms) | 既存 AI agent との差別化 |
| 22 | [Autonomy × Self-sufficiency — the FullSense Singularity (`SING*`)](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md#22-autonomy--self-sufficiency--the-fullsense-singularity-sing) | 自律 × 自己充足 |

## 要件定義 (実装側)

Spec を実装に落とした **要件定義**は llive 配下に複数の version 文書として存在:

| 文書 | スコープ |
|---|---|
| [`requirements_v0.1.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.1.md) | Core MVR (v1 Phase 1) |
| [`requirements_v0.2_addendum.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.2_addendum.md) | Phase 2 追補 |
| [`requirements_v0.3_triz_self_evolution.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.3_triz_self_evolution.md) | TRIZ × 自己進化 |
| [`requirements_v0.4_llm_wiki.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.4_llm_wiki.md) | LLM Wiki パターン (Karpathy 2026-04) |
| [`requirements_v0.5_spatial_memory.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.5_spatial_memory.md) | Spatial Memory |
| [`requirements_v0.6_concurrency.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.6_concurrency.md) | 並行プロンプト処理 |
| [`requirements_v0.7_rust_acceleration.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.7_rust_acceleration.md) | Rust ホットパス置換 |
| [`requirements_v0.8_cognitive_mesh.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.8_cognitive_mesh.md) | **COG-MESH (能動性 / 並列 Brief / Quiet Hours)** (2026-05-18 追加、全 10 件 skeleton 完了 2026-05-19) — portal 概要は [Cognitive Mesh hub]({{ '/cognitive-mesh/' | relative_url }}) |

加えて、`.planning/REQUIREMENTS.md` に GSD workflow 用の REQ-ID 化版が
あり、CABT (v0.8) / COG-MESH (v0.8b) / CREAT (v0.9) / VLM-FX / ORG-FX 等を
横断的に管理 ([live link](https://github.com/furuse-kazufumi/llive/blob/main/.planning/REQUIREMENTS.md))。

## アーキテクチャ

実装上の 8 層アーキテクチャ + v0.8 拡張ポイントは
[`llive/docs/architecture.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/architecture.md)
を参照。

## なぜ portal 側にミラーしないか

NOTES.md `Link-rot watch list` の方針通り、spec を **portal にコピーすると
drift する**。本ページは GitHub アンカーへの直接リンクのみで、変更は
真実ソース (llive リポ) で起き、自動的に portal 側からも見える。

ただし将来 v1.0 PyPI rename / 商標確定後など **stable な周期点** で、
portal に snapshot を取り込むことを検討する (現状は v0.x 期間で頻繁に
更新されるためミラー非推奨)。

## 関連ページ

- [Roadmap]({{ '/roadmap' | relative_url }}) — 何が live / planned / parked か
- [Comparison]({{ '/comparison' | relative_url }}) — vs Claude Code /
  Perplexity / Codex / Gemini
- [Benchmark Policy]({{ '/benchmarks/policy/' | relative_url }}) — ベンチ運用ルール

## Last updated

2026-05-18 — Spec hub 初版。drift 防止のため章直リンク方式を採用。
COG-MESH (v0.8b) 要件追加と同期。
