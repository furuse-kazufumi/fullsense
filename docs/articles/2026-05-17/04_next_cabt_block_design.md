---
layout: default
title: "Transformer ブロックを高度化する 7 つのアプローチ — CABT 設計予告"
date: 2026-05-17
tags: [llm, transformer, attention, architecture, design]
draft: true
---

# Transformer ブロックを高度化する 7 つのアプローチ — CABT 設計予告

> **Status**: 設計予告。実装は S2 (CABT-01) から段階着手予定。本記事はユーザー
> 指示「Transformer 構造はシンプルだが各ブロックでもっと高度なことができる」
> +「マトリクスを参照ベース並べ替えに置換し付加情報を持たせる」+「llive
> 独自の思考の層と親和性が高いものに」という方向性を技術設計に落としたもの。

## TL;DR

- Transformer の `softmax(QK^T)·V` は値そのものを混合する → 付加情報 (provenance / trust / epistemic_type) を持たせる場所がない
- 代わりに「参照ポインタを選択 → 参照先 metadata を集約」する設計に置換可能
- llive では HF transformers の `forward_hook` で **重み凍結のまま** attention 出力に metadata bias を加算する経路を採用
- 7 つの CABT-01〜07 として要件化、スパイラル開発 S2-S6 で順次試作

## 設計動機

```
[現状の attention]                  [CABT の置換案]
attn_output = softmax(QK^T) · V     ref_id = softmax(QK^T)
                                    attn_output = lookup(ref_id) + metadata_bias

  ┌ V (float[B, S, H])              ┌ token table
  │ 値そのもの                      │ (id, embedding, metadata)
  │ メタ情報を保持不能              │ 参照可能、付加情報可能
  └                                  └
```

## 7 つのアプローチ (CABT-01〜07)

### CABT-01: Reference-based Attention with Metadata (ユーザー直接案)

attention 出力に 6 列 metadata の bias を加算する hook を入れる。重み凍結のまま実現可能。

```python
# src/llive/cabt/hooks.py (S2 で実装予定)
class ReferenceAttentionHook:
    def _on_attention(self, module, inputs, outputs):
        attn_output = outputs[0]  # [batch, seq, hidden]
        bias = self._metadata_provider(attn_output)  # provenance/trust/...
        return (attn_output + self._strength * bias, *outputs[1:])
```

metadata 6 列:
- `provenance_id`: memory/provenance.py のレコード ID
- `trust_score`: Quarantined Memory の trust 値 [0,1]
- `epistemic_type`: FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC + RESERVED
- `timestamp_norm`: 時系列正規化 [0,1]
- `source_domain_id`: RAD 49 分野の ID
- `surprise_score`: BayesianSurpriseGate (FR-21) の出力

### CABT-02: Stage-aware Block Routing

FullSense 6 stage (salience → curiosity → thought → ego/altruism → plan → output) に応じて、active なブロック構成を切り替える。Soft-MoE 風の軽量 routing。

Stage が違えば「考えるべき事」が違う:
- salience 段階では sparse attention (高速 filtering)
- thought 段階では dense attention (深い推論)
- output 段階では narrow head (確定的生成)

### CABT-03: Epistemic-typed Token Pool

各 token に `EpistemicType` を付与 → 同 type 優先 attention bias。Multi-track Filter Architecture A-1.5 (llive Spec §F*) の token 化。

例: `MATHEMATICAL` track の token は他 type からの attention を弱める → 数学的厳密性を保つ。

### CABT-04: Salience-gated Attention

Token-level surprise score (FR-21) で attention 強度を per-token に動的化:
- surprise 低い token → MLP のみ通過 (cheap)
- surprise 高い token → full attention (expensive)

Mixture-of-Depths と類似だが、判定基準が外部記憶層 (semantic memory の novelty) 由来。

### CABT-05: TRIZ-conditioned Head Selection

Brief で BriefGrounder が surface した TRIZ 原理に応じて attention head の一部を mask / bias。

例: TRIZ 原理 24 (Mediator) が surface した Brief では、media 関連 head を強調。

### CABT-06: Approval-gated Decoding

出力 token sequence を Approval Bus が検査。policy 違反候補は generation 段階で reject。Constitutional AI と類似だが、policy が SQLite に永続化されて auditor が検証可能。

### CABT-07: Memory-augmented Residual

各層 residual path に 4 層メモリ (semantic / episodic / structural / parameter) の embedding を加算。Hippocampal Consolidation Scheduler (FR-12) と双対な書き込み経路を attention にも開く。

## スパイラル開発計画

| Iter | スコープ | リスク | 評価指標 |
|---|---|---|---|
| S2 | CABT-01: HFAdapter forward hook prototype | 中 (HF 内部依存) | Brief × {grounded, ungrounded} 比較 |
| S3 | CABT-03 + CABT-04 | 中 (LoRA 検討) | token-level surprise log |
| S4 | CABT-02: Soft-MoE routing | 高 (アーキ変更幅大) | per-stage benchmark |
| S5 | CABT-05 + CABT-06 | 高 (Approval Bus 性能影響) | safety bench (RPAR) |
| S6 | CABT-07 統合 | 高 (品質測定が困難) | full progressive matrix |

## 既存研究との位置づけ

- **Pointer Networks** (Vinyals 2015): 参照ベース attention の祖
- **Memorizing Transformers** (Wu 2022): kNN over external memory
- **RETRO** (Borgeaud 2022): retrieval-augmented decoder
- **kNN-LM** (Khandelwal 2020): non-parametric memory lookup
- **Mixture-of-Depths** (Raposo 2024): per-token compute budget
- **Hyena Operator** (Poli 2023): long-convolution alternative

llive の差別化: **既存 OSS LLM 重みを凍結したまま forward hook で挙動を加える**。LoRA / 全 fine-tune は不要。on-prem 推論可。

## ソース (実装前)

- 設計 doc: `D:/projects/llive/docs/proposals/cabt-01_reference_attention.md`
- 要件: REQUIREMENTS.md v0.8 CABT セクション
- ロードマップ: ROADMAP.md Phase 8

## 完成版記事の予告

S2 (CABT-01 prototype) が動いた時点で、本記事は draft 解除し:
- 実測 attention bias の効果 (Brief × {hook on, hook off} の出力差)
- thought_chars / decision rationale の変化
- HF transformers version 互換性報告
を追加してリリースします。

---

> 設計記事段階。実装が進んだ時点で内容を更新します。
