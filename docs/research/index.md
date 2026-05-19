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

## 方針

- 1 ファイル = 1 トピック (spinoff 候補 or 主要設計判断).
- 800 字内外の要約 + Sources 5〜10 件. これ以上深い分析は **個別 spike** に派生.
- 内容は **AI 自律調査**. 人間が裏取りしてから設計に降ろす扱い.
- 引用元の link-rot は portal の Lychee CI で監視.

## いつ更新するか

- `spinoff_ideas_2026_05.md` の Planned / Pattern が新しい段階に進む直前.
- 主要設計判断 (差別化軸) を変更する前.
- 競合 / SOTA が大きく動いたと感じたとき.
