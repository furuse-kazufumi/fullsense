---
layout: default
title: "Transformer ブロックを高度化する 7 つのアプローチ — CABT 設計予告"
date: 2026-05-17
tags: [llm, transformer, attention, architecture, design]
draft: true
id: a6804f6b8c47605177a8
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

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

![現状の attention と CABT 置換案の設計動機比較図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q04/design_motivation.svg)

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

- 設計 doc: `llive/docs/proposals/cabt-01_reference_attention.md`
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

---

# English

# Seven Approaches to Making the Transformer Block Smarter — A CABT Design Preview

> **Status**: Design preview. Implementation is scheduled to begin in stages from S2 (CABT-01).
> This article turns the following user directions into a technical design: "The Transformer
> structure is simple, but each block could do something far more sophisticated," "Replace the
> matrix with a reference-based reordering that carries side information," and "Pick the ideas
> that mesh best with llive's own layers of thought."

## TL;DR

- Transformer's `softmax(QK^T)·V` mixes the values themselves → there is nowhere to attach side information (provenance / trust / epistemic_type)
- It can instead be replaced with a design that "selects a reference pointer → aggregates the metadata at the referenced location"
- In llive we adopt a path that, **with the weights frozen**, adds a metadata bias to the attention output via HF transformers' `forward_hook`
- Captured as the seven requirements CABT-01 through 07, prototyped in turn across spiral-development iterations S2-S6

## Design Motivation

![Design motivation: current attention vs CABT replacement proposal](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q04/design_motivation_en.svg)

## Seven Approaches (CABT-01 through 07)

### CABT-01: Reference-based Attention with Metadata (the user's direct proposal)

Insert a hook that adds a bias of 6-column metadata to the attention output. Achievable with the weights kept frozen.

```python
# src/llive/cabt/hooks.py (to be implemented in S2)
class ReferenceAttentionHook:
    def _on_attention(self, module, inputs, outputs):
        attn_output = outputs[0]  # [batch, seq, hidden]
        bias = self._metadata_provider(attn_output)  # provenance/trust/...
        return (attn_output + self._strength * bias, *outputs[1:])
```

The 6 metadata columns:
- `provenance_id`: the record ID from memory/provenance.py
- `trust_score`: the Quarantined Memory trust value [0,1]
- `epistemic_type`: FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC + RESERVED
- `timestamp_norm`: time-series normalization [0,1]
- `source_domain_id`: an ID from the 49 RAD domains
- `surprise_score`: the output of BayesianSurpriseGate (FR-21)

### CABT-02: Stage-aware Block Routing

According to the FullSense 6 stages (salience → curiosity → thought → ego/altruism → plan → output), switch the active block configuration. A lightweight, Soft-MoE-style routing.

Different stages call for thinking about different things:
- in the salience stage, sparse attention (fast filtering)
- in the thought stage, dense attention (deep reasoning)
- in the output stage, narrow heads (deterministic generation)

### CABT-03: Epistemic-typed Token Pool

Attach an `EpistemicType` to each token → bias attention toward the same type. The tokenization of the Multi-track Filter Architecture A-1.5 (llive Spec §F*).

Example: tokens on the `MATHEMATICAL` track weaken attention coming from other types → preserving mathematical rigor.

### CABT-04: Salience-gated Attention

Use a token-level surprise score (FR-21) to make attention strength dynamic per token:
- low-surprise tokens → pass through the MLP only (cheap)
- high-surprise tokens → full attention (expensive)

Similar to Mixture-of-Depths, but the decision criterion derives from an external memory layer (the novelty of semantic memory).

### CABT-05: TRIZ-conditioned Head Selection

Depending on the TRIZ principle that BriefGrounder surfaces in a Brief, mask / bias a subset of the attention heads.

Example: in a Brief where TRIZ principle 24 (Mediator) is surfaced, emphasize media-related heads.

### CABT-06: Approval-gated Decoding

The Approval Bus inspects the output token sequence. Policy-violating candidates are rejected at the generation stage. Similar to Constitutional AI, but the policy is persisted in SQLite so an auditor can verify it.

### CABT-07: Memory-augmented Residual

On each layer's residual path, add the embedding of the 4 memory layers (semantic / episodic / structural / parameter). It opens, for attention as well, a write path that is dual to the Hippocampal Consolidation Scheduler (FR-12).

## Spiral Development Plan

| Iter | Scope | Risk | Evaluation metric |
|---|---|---|---|
| S2 | CABT-01: HFAdapter forward hook prototype | Medium (HF internal dependency) | Brief × {grounded, ungrounded} comparison |
| S3 | CABT-03 + CABT-04 | Medium (LoRA under consideration) | token-level surprise log |
| S4 | CABT-02: Soft-MoE routing | High (large architectural change) | per-stage benchmark |
| S5 | CABT-05 + CABT-06 | High (Approval Bus performance impact) | safety bench (RPAR) |
| S6 | CABT-07 integration | High (quality is hard to measure) | full progressive matrix |

## Positioning Relative to Prior Work

- **Pointer Networks** (Vinyals 2015): the ancestor of reference-based attention
- **Memorizing Transformers** (Wu 2022): kNN over external memory
- **RETRO** (Borgeaud 2022): retrieval-augmented decoder
- **kNN-LM** (Khandelwal 2020): non-parametric memory lookup
- **Mixture-of-Depths** (Raposo 2024): per-token compute budget
- **Hyena Operator** (Poli 2023): a long-convolution alternative

llive's differentiation: **adding behavior via a forward hook while keeping the existing OSS LLM weights frozen**. No LoRA or full fine-tuning is needed. On-prem inference is possible.

## Sources (pre-implementation)

- Design doc: `llive/docs/proposals/cabt-01_reference_attention.md`
- Requirements: REQUIREMENTS.md v0.8 CABT section
- Roadmap: ROADMAP.md Phase 8

## Preview of the Completed Article

Once S2 (the CABT-01 prototype) is working, this article will leave draft status and add:
- the effect of the measured attention bias (the output difference for Brief × {hook on, hook off})
- changes in thought_chars / decision rationale
- an HF transformers version-compatibility report
and be released.

---

> This is the design-article stage. The content will be updated once implementation advances.

---

# 中文

# 让 Transformer 块更高级的 7 种方法 — CABT 设计预告

> **Status**: 设计预告。实现计划从 S2 (CABT-01) 开始分阶段着手。本文将用户的以下
> 指示落实为技术设计：「Transformer 结构虽然简单，但每个块可以做更高级的事情」
> +「把矩阵替换为基于引用的重排序并赋予附加信息」+「选取与 llive 独有的思考层
> 亲和性最高的方案」这一方向。

## TL;DR

- Transformer 的 `softmax(QK^T)·V` 混合的是值本身 → 没有地方承载附加信息 (provenance / trust / epistemic_type)
- 可以替换为「选择引用指针 → 聚合被引用位置的 metadata」的设计
- 在 llive 中，我们采用**在权重冻结的前提下**通过 HF transformers 的 `forward_hook` 向 attention 输出加上 metadata bias 的路径
- 将其需求化为 CABT-01〜07 这 7 项，在螺旋式开发 S2-S6 中依次试制

## 设计动机

```
[现状的 attention]                  [CABT 的置换方案]
attn_output = softmax(QK^T) · V     ref_id = softmax(QK^T)
                                    attn_output = lookup(ref_id) + metadata_bias

  ┌ V (float[B, S, H])              ┌ token table
  │ 值本身                          │ (id, embedding, metadata)
  │ 无法保留元信息                  │ 可引用、可承载附加信息
  └                                  └
```

## 7 种方法 (CABT-01〜07)

### CABT-01: Reference-based Attention with Metadata (用户的直接提案)

在 attention 输出上插入一个加上 6 列 metadata bias 的 hook。在权重冻结的前提下即可实现。

```python
# src/llive/cabt/hooks.py (计划在 S2 实现)
class ReferenceAttentionHook:
    def _on_attention(self, module, inputs, outputs):
        attn_output = outputs[0]  # [batch, seq, hidden]
        bias = self._metadata_provider(attn_output)  # provenance/trust/...
        return (attn_output + self._strength * bias, *outputs[1:])
```

metadata 6 列：
- `provenance_id`: memory/provenance.py 的记录 ID
- `trust_score`: Quarantined Memory 的 trust 值 [0,1]
- `epistemic_type`: FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC + RESERVED
- `timestamp_norm`: 时间序列归一化 [0,1]
- `source_domain_id`: RAD 49 个领域的 ID
- `surprise_score`: BayesianSurpriseGate (FR-21) 的输出

### CABT-02: Stage-aware Block Routing

根据 FullSense 6 阶段 (salience → curiosity → thought → ego/altruism → plan → output)，切换处于 active 的块配置。一种 Soft-MoE 风格的轻量 routing。

阶段不同，「应该思考的事情」也不同：
- 在 salience 阶段使用 sparse attention (快速 filtering)
- 在 thought 阶段使用 dense attention (深度推理)
- 在 output 阶段使用 narrow head (确定性生成)

### CABT-03: Epistemic-typed Token Pool

为每个 token 赋予 `EpistemicType` → 偏向同 type 的 attention bias。Multi-track Filter Architecture A-1.5 (llive Spec §F*) 的 token 化。

例：`MATHEMATICAL` track 的 token 会削弱来自其他 type 的 attention → 保持数学上的严谨性。

### CABT-04: Salience-gated Attention

用 token 级的 surprise score (FR-21) 让 attention 强度按 token 动态化：
- surprise 低的 token → 仅通过 MLP (cheap)
- surprise 高的 token → full attention (expensive)

与 Mixture-of-Depths 类似，但判定基准来源于外部记忆层 (semantic memory 的 novelty)。

### CABT-05: TRIZ-conditioned Head Selection

根据 BriefGrounder 在 Brief 中 surface 出的 TRIZ 原理，对部分 attention head 进行 mask / bias。

例：在 surface 出 TRIZ 原理 24 (Mediator) 的 Brief 中，强调与 media 相关的 head。

### CABT-06: Approval-gated Decoding

由 Approval Bus 检查输出的 token sequence。违反 policy 的候选会在 generation 阶段被 reject。与 Constitutional AI 类似，但 policy 被持久化到 SQLite，使 auditor 可以验证。

### CABT-07: Memory-augmented Residual

在每一层的 residual path 上，加上 4 层记忆 (semantic / episodic / structural / parameter) 的 embedding。它也为 attention 打开了一条与 Hippocampal Consolidation Scheduler (FR-12) 对偶的写入路径。

## 螺旋式开发计划

| Iter | 范围 | 风险 | 评价指标 |
|---|---|---|---|
| S2 | CABT-01: HFAdapter forward hook prototype | 中 (依赖 HF 内部) | Brief × {grounded, ungrounded} 比较 |
| S3 | CABT-03 + CABT-04 | 中 (考虑 LoRA) | token 级 surprise log |
| S4 | CABT-02: Soft-MoE routing | 高 (架构改动幅度大) | per-stage benchmark |
| S5 | CABT-05 + CABT-06 | 高 (对 Approval Bus 性能有影响) | safety bench (RPAR) |
| S6 | CABT-07 集成 | 高 (质量难以测量) | full progressive matrix |

## 与既有研究的定位

- **Pointer Networks** (Vinyals 2015): 基于引用的 attention 之鼻祖
- **Memorizing Transformers** (Wu 2022): kNN over external memory
- **RETRO** (Borgeaud 2022): retrieval-augmented decoder
- **kNN-LM** (Khandelwal 2020): non-parametric memory lookup
- **Mixture-of-Depths** (Raposo 2024): per-token compute budget
- **Hyena Operator** (Poli 2023): long-convolution 的替代方案

llive 的差异化：**在保持既有 OSS LLM 权重冻结的同时，通过 forward hook 加入行为**。无需 LoRA / 全量 fine-tune。可进行 on-prem 推理。

## 来源 (实现前)

- 设计 doc: `llive/docs/proposals/cabt-01_reference_attention.md`
- 需求: REQUIREMENTS.md v0.8 CABT 章节
- 路线图: ROADMAP.md Phase 8

## 完成版文章的预告

待 S2 (CABT-01 prototype) 跑通后，本文将解除 draft 状态并补充：
- 实测 attention bias 的效果 (Brief × {hook on, hook off} 的输出差异)
- thought_chars / decision rationale 的变化
- HF transformers version 兼容性报告
然后发布。

---

> 设计文章阶段。实现推进后将更新内容。

---

# 한국어

# Transformer 블록을 고도화하는 7 가지 접근법 — CABT 설계 예고

> **Status**: 설계 예고. 구현은 S2 (CABT-01) 부터 단계적으로 착수 예정. 본 글은 사용자
> 지시「Transformer 구조는 단순하지만 각 블록에서 더 고도의 일을 할 수 있다」
> +「행렬을 참조 기반 재배열로 치환하고 부가 정보를 갖게 한다」+「llive
> 고유의 사고 층과 친화성이 높은 것으로」라는 방향성을 기술 설계로 옮긴 것이다.

## TL;DR

- Transformer 의 `softmax(QK^T)·V` 는 값 그 자체를 혼합한다 → 부가 정보 (provenance / trust / epistemic_type) 를 담을 곳이 없다
- 대신「참조 포인터를 선택 → 참조처의 metadata 를 집약」하는 설계로 치환 가능
- llive 에서는 HF transformers 의 `forward_hook` 으로 **가중치를 동결한 채** attention 출력에 metadata bias 를 가산하는 경로를 채택
- 7 개의 CABT-01〜07 로 요건화하여, 나선형 개발 S2-S6 에서 순차적으로 시작(試作)

## 설계 동기

```
[현재의 attention]                  [CABT 의 치환안]
attn_output = softmax(QK^T) · V     ref_id = softmax(QK^T)
                                    attn_output = lookup(ref_id) + metadata_bias

  ┌ V (float[B, S, H])              ┌ token table
  │ 값 그 자체                      │ (id, embedding, metadata)
  │ 메타 정보를 보유 불가           │ 참조 가능, 부가 정보 가능
  └                                  └
```

## 7 가지 접근법 (CABT-01〜07)

### CABT-01: Reference-based Attention with Metadata (사용자 직접안)

attention 출력에 6 열 metadata 의 bias 를 가산하는 hook 을 넣는다. 가중치를 동결한 채 실현 가능.

```python
# src/llive/cabt/hooks.py (S2 에서 구현 예정)
class ReferenceAttentionHook:
    def _on_attention(self, module, inputs, outputs):
        attn_output = outputs[0]  # [batch, seq, hidden]
        bias = self._metadata_provider(attn_output)  # provenance/trust/...
        return (attn_output + self._strength * bias, *outputs[1:])
```

metadata 6 열:
- `provenance_id`: memory/provenance.py 의 레코드 ID
- `trust_score`: Quarantined Memory 의 trust 값 [0,1]
- `epistemic_type`: FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC + RESERVED
- `timestamp_norm`: 시계열 정규화 [0,1]
- `source_domain_id`: RAD 49 분야의 ID
- `surprise_score`: BayesianSurpriseGate (FR-21) 의 출력

### CABT-02: Stage-aware Block Routing

FullSense 6 stage (salience → curiosity → thought → ego/altruism → plan → output) 에 따라 active 한 블록 구성을 전환한다. Soft-MoE 풍의 경량 routing.

Stage 가 다르면「생각해야 할 일」이 다르다:
- salience 단계에서는 sparse attention (고속 filtering)
- thought 단계에서는 dense attention (깊은 추론)
- output 단계에서는 narrow head (확정적 생성)

### CABT-03: Epistemic-typed Token Pool

각 token 에 `EpistemicType` 을 부여 → 같은 type 우선 attention bias. Multi-track Filter Architecture A-1.5 (llive Spec §F*) 의 token 화.

예: `MATHEMATICAL` track 의 token 은 다른 type 으로부터의 attention 을 약화시킨다 → 수학적 엄밀성을 유지.

### CABT-04: Salience-gated Attention

Token 단위 surprise score (FR-21) 로 attention 강도를 per-token 으로 동적화:
- surprise 가 낮은 token → MLP 만 통과 (cheap)
- surprise 가 높은 token → full attention (expensive)

Mixture-of-Depths 와 유사하지만, 판정 기준이 외부 기억 층 (semantic memory 의 novelty) 에서 유래한다.

### CABT-05: TRIZ-conditioned Head Selection

Brief 에서 BriefGrounder 가 surface 한 TRIZ 원리에 따라 attention head 의 일부를 mask / bias.

예: TRIZ 원리 24 (Mediator) 가 surface 한 Brief 에서는 media 관련 head 를 강조.

### CABT-06: Approval-gated Decoding

출력 token sequence 를 Approval Bus 가 검사. policy 위반 후보는 generation 단계에서 reject. Constitutional AI 와 유사하지만, policy 가 SQLite 에 영속화되어 auditor 가 검증 가능.

### CABT-07: Memory-augmented Residual

각 층의 residual path 에 4 층 메모리 (semantic / episodic / structural / parameter) 의 embedding 을 가산. Hippocampal Consolidation Scheduler (FR-12) 와 쌍대(雙對)인 쓰기 경로를 attention 에도 연다.

## 나선형 개발 계획

| Iter | 스코프 | 리스크 | 평가 지표 |
|---|---|---|---|
| S2 | CABT-01: HFAdapter forward hook prototype | 중 (HF 내부 의존) | Brief × {grounded, ungrounded} 비교 |
| S3 | CABT-03 + CABT-04 | 중 (LoRA 검토) | token 단위 surprise log |
| S4 | CABT-02: Soft-MoE routing | 고 (아키텍처 변경 폭 큼) | per-stage benchmark |
| S5 | CABT-05 + CABT-06 | 고 (Approval Bus 성능 영향) | safety bench (RPAR) |
| S6 | CABT-07 통합 | 고 (품질 측정이 곤란) | full progressive matrix |

## 기존 연구와의 위치 설정

- **Pointer Networks** (Vinyals 2015): 참조 기반 attention 의 시조
- **Memorizing Transformers** (Wu 2022): kNN over external memory
- **RETRO** (Borgeaud 2022): retrieval-augmented decoder
- **kNN-LM** (Khandelwal 2020): non-parametric memory lookup
- **Mixture-of-Depths** (Raposo 2024): per-token compute budget
- **Hyena Operator** (Poli 2023): long-convolution 의 대안

llive 의 차별화: **기존 OSS LLM 가중치를 동결한 채 forward hook 으로 거동을 더한다**. LoRA / 전체 fine-tune 은 불필요. on-prem 추론 가능.

## 소스 (구현 전)

- 설계 doc: `llive/docs/proposals/cabt-01_reference_attention.md`
- 요건: REQUIREMENTS.md v0.8 CABT 섹션
- 로드맵: ROADMAP.md Phase 8

## 완성판 글의 예고

S2 (CABT-01 prototype) 가 동작한 시점에 본 글은 draft 를 해제하고:
- 실측 attention bias 의 효과 (Brief × {hook on, hook off} 의 출력 차이)
- thought_chars / decision rationale 의 변화
- HF transformers version 호환성 보고
를 추가하여 릴리스한다.

---

> 설계 글 단계. 구현이 진행된 시점에 내용을 업데이트한다.
