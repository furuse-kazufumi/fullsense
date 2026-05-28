---
layout: default
title: "llcore CPU PoC Battery 完成 (2026-05-29)"
parent: Research
nav_order: 1054
---

# llcore CPU PoC Battery 完成 — Stage 0-2 全 PoC 完走

**日付**: 2026-05-29  
**Source**: `D:/projects/llcore/docs/poc/COMPLETION_VERDICT.md`  
**Project**: `llmesh-llcore` 0.1.0a0 (llive 独立路線)

## 何が完成したか

Transformer のコアアルゴリズム (state update / 学習則 / 認知駆動 Δ) に進化形態を与え、**Z3 verifier で破綻させずに** 異アルゴリズムへ進化させる研究フレームワーク `llcore` の CPU PoC battery が Stage 0-2 完走。

| PoC | Stage | Gates | pytest | Codex |
|---|---|---|---|---|
| 0a v2 | state update gene RWKV-style | 10/10 | 20 | Green |
| 0b v2 | synthetic fitness (copy/add) | 7/7 | 17 | Green |
| 0c v2 | 自前 minimal GA (llive 非依存) | 7/7 | 10 | Green |
| 1a v2 | Z3 verifier state_norm invariant | 8/8 | 10 | Green (5.8ms) |
| 2a | factor_hook × state update mock | 7/7 | 10 | Green |
| **計** | **5 PoC** | **39** | **76** | **5/5 Green** |

## 確定独自軸 (事前調査 Agent A-D + RAD 14 分野で negation work なし)

mechanism 実証済 (4 軸):
1. **ChangeOp → Z3 事前 gate (online)** — Stage 1a で 5.8ms 動作実証
2. **state update 規則を遺伝子化 (RWKV-style)** — Stage 0a v2 採択 (Codex 推奨)
3. **factor_hook (認知状態 → SSM Δ)** — Stage 2a mock 接続
4. **自前進化器 + verifier 基盤** — Stage 0c (minimal GA) + 1a

post-llcore phase (3 軸):
5. persona-indexed specialist 集団 × verifier
6. Marabou Incremental の "異なる構造" refinement relation sound 拡張
7. VNN-COMP "online architecture evolution verification" 新カテゴリ提案

## 投稿先候補

- **TMLR** (本命, no hard deadline)
- **GECCO 2027 short paper** (1月/2月 abstract deadline)
- **NeurIPS 2026 workshop** (verification × ML)

## Codex × Claude 相互レビュー実績

**5 PoC 中 4 件で Claude 単独では見落とした設計問題を Codex (gpt-5.4) が検出**:
- 0a: zero attractor (Fix A 不採用 → RWKV-style 採用)
- 0b: MSE 不整合 blocker (raw_error Protocol 統一)
- 1a: verify_gene_safe gene-non-specific bug (tighter tanh bound)
- 2a: wording 盛りすぎ ("RWKV mock" → "state update kernel mock")

→ [[feedback_codex_pair_review_for_llcore]] が **構造破綻防止に機能した実例**。

## 次選択肢 (実装拡張トラック)

a. Stage 3 kernel 多様化 gene (rwkv / mamba / hopfield / linear-attn)  
b. Stage 4 学習則 (FF/EP/PCN/Hebb) を impl_chromosome gene 化  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. PrediPrune + Quokka で Z3 gate 高速化 (51% reduction 実証)  
e. FlashEvolve で lldarwin/minimal GA 非同期化 (3.5-5x wall-clock)  
f. 論文化トラック (TMLR draft + GECCO 2027 short)

## 関連

- llcore 統合 verdict: `D:/projects/llcore/docs/poc/COMPLETION_VERDICT.md`
- 事前調査 master survey: `docs/papers/2026-05-29_core_evolution_master_survey.md`
- 研究計画書 v1: `docs/papers/2026-05-29_research_plan_core_evolution.md`
- memory: `project_llcore_init_2026_05_29` / `feedback_codex_pair_review_for_llcore` / `project_core_evolution_survey_2026_05_28`
