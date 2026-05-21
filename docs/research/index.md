---
layout: default
title: "Research"
nav_order: 92
has_children: true
---

# Research Notes

> AI agent (Claude Opus 4.7) が自律的に作成した先行研究 / SOTA 比較 / 競合
> 分析の集約場所. 「設計判断の前提資料」として参照する.

## 一覧

| File | 内容 |
|---|---|
| [lleval — SOTA Survey]({{ '/research/lleval_sota' | relative_url }}) | LLM eval framework (OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse / TruLens / Ragas) の SOTA matrix + LM-as-judge bias + 推奨 fork base |
| [llgrow — Prior Art Survey]({{ '/research/llgrow_prior_art' | relative_url }}) | HITL content automation (Jasper / Mautic / Langfuse 等) と academic 2025 研究を比較し、個人開発者 OSS 配信 vertical の gap を整理 |
| [Cognitive Mesh vs SOTA]({{ '/research/cognitive_mesh_vs_sota' | relative_url }}) | llive v0.8 Cognitive Mesh (M8.1〜M8.9) を MemGPT / Generative Agents / A-MEM / Reflexion / Constitutional AI 等と sub-system 毎に対応づけた比較 |
| [llcraft — Creative Material SOTA]({{ '/research/llcraft_sota' | relative_url }}) | on-prem creative material (TTS / 画像 / 動画 / 音楽) の OSS Stack matrix + license tier 管理. C2PA + IPTC 2025.1 への llcraft 拡張案 |
| [llrisk — Continuous Risk Tracking Prior Art]({{ '/research/llrisk_prior_art' | relative_url }}) | AI-driven GRC / DevOps risk monitoring / LLM × risk register / reputation / developer burnout を 6 軸縦割りで整理. 個人開発者向け on-prem 空白 |
| [llgov — AI Governance / Compliance SOTA]({{ '/research/llgov_sota' | relative_url }}) | NeMo Guardrails / OPA / Cedar / MS Agent Governance Toolkit / Credo AI / Holistic AI の matrix + EU AI Act Art.9-15 自動検証 OSS の空白 |
| [LLM × Evolutionary — Prior Art]({{ '/research/llm_evolutionary_prior_art' | relative_url }}) | llive v0.B/v0.C (集団 GA × 19 dim genome × subprocess transport) と類似する LMX / EvoPrompt / Promptbreeder / EUREKA / FunSearch / R2SAEA / MappingEvolve / MASPO の SOTA matrix + 差別化 4 軸 (on-prem / 19 dim 数値 / subprocess / honest disclosure) |

## 方針

- 1 ファイル = 1 トピック (spinoff 候補 or 主要設計判断).
- 800 字内外の要約 + Sources 5〜10 件. これ以上深い分析は **個別 spike** に派生.
- 内容は **AI 自律調査**. 人間が裏取りしてから設計に降ろす扱い.
- 引用元の link-rot は portal の Lychee CI で監視.

## いつ更新するか

- `spinoff_ideas_2026_05.md` の Planned / Pattern が新しい段階に進む直前.
- 主要設計判断 (差別化軸) を変更する前.
- 競合 / SOTA が大きく動いたと感じたとき.
