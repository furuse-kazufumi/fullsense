---
layout: default
title: "Qwen 依存から離脱する 5 段階ロードマップ — llive の独自性をコアに移植する"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags: [llm, architecture, originality, qwen, distillation, mamba, research]
id: ba3a0f41e42ec533a3a1
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# Qwen 依存から離脱する 5 段階ロードマップ — llive の独自性をコアに移植する

著者: 古瀬 和文（ぷるやん）

## TL;DR

- 現状の llive (v0.6) は **周辺認知 OS としては独自**だが、**LLM コアは Qwen / Llama / Mistral に依存** している
- ユーザー観察: 「差別化されていないと研究の価値がない。普及している AI を使った方がマシってなりそう」
- 中長期的な研究価値のため、**コア LLM 自体の独自化** を 5 段階ロードマップで要件化 (ORG-FX, Phase 11)
- 短期は周辺強化を維持、中期 LoRA → 蒸留、長期 Transformer block 置換 → Mamba/RWKV 系 native

## 現状の差別化の "層別" 分析

| 層 | llive 独自性 | Qwen 依存度 |
|---|---|---|
| 入力 (Brief API) | ★★★★★ | 0% |
| Grounder (TRIZ × RAD) | ★★★★★ | 0% |
| 6 stage Loop | ★★★★☆ | 10% (思考の数式化は独自) |
| 4 層メモリ | ★★★★☆ | 0% |
| Multi-track Filter | ★★★★☆ | 0% |
| Approval Bus | ★★★★★ | 0% |
| Governance Scoring | ★★★★★ | 0% |
| Trace Graph (Ledger) | ★★★★☆ | 0% |
| **LLM コア (Decoder-only Transformer)** | ☆ | **100%** ← 問題 |

→ 周辺は十分独自。**コアの独自性が未着手**。これが研究としての弱点。

## なぜコアを独自化する必要があるか

### 理由 1: 研究としての価値

Qwen / Llama / Mistral / GPT を frozen で使うだけだと、研究の中核が
「他人の重み + 自分のラッパー」になる。論文化や長期視点で見ると、コア
自体に手を入れていない設計は引用価値が下がる。

### 理由 2: 普及との差別化

「普及している AI を使った方がマシ」になる懸念。Qwen を使うなら直接 Qwen を
使えば良いという論理に対抗するには、**llive にしかできない計算** を増やす
必要がある。これは MATH-08 (SafeCalculator) や CREAT-01 (KJ法ノード) のような
**「LLM を使わない決定論的層」** を増やすか、**「LLM 自体が llive 専用」** に
する 2 路線。

### 理由 3: 産業 IoT との接続

llmesh sensor bridge (FR-19) で 産業 IoT に直接 LLM を接続する場合、
Qwen の汎用性は必ずしも有利ではない。専用特化した小型 LLM の方が:
- レイテンシが低い
- メモリ消費が少ない
- ドメイン特化精度が高い
- セキュリティ監査が容易

## 5 段階ロードマップ

![Qwen 依存離脱の 5 段階ロードマップ（Stage A 周辺強化から Stage E 非 Transformer コアまでのフロー）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q10/roadmap_5stage.svg)

## 各 Stage で導入する ORG-* 要件

| FR | 名前 | Stage | 動機 |
|---|---|---|---|
| **ORG-06** | Provenance-aware tokens | B+D | 各 token に metadata 列を追加、attention で参照 |
| **ORG-02** | Memory-coupled inference | C/D | LLM 推論時に 4 層メモリを直接参照 |
| **ORG-03** | Multi-track sub-network | C | EpistemicType ごとの sub-network (MoE 認知版) |
| **ORG-08** | llive-specialized small model | C | qwen2.5:14b → llive-7b 蒸留 |
| **ORG-07** | Approval-native decoding | C/D | Approval を decoder 内に持ち込む |
| **ORG-01** | Cognitive Block Replacement | D | Transformer block を llive 思考層と同期 |
| **ORG-04** | TRIZ-guided architecture search | D | LLM コアを自己改良 |
| **ORG-05** | Surprise-native pretraining | E | Bayesian Surprise を loss に内在化 |

## 各 Stage のリスクと評価

| Stage | リスク | GPU 必要量 | 評価指標 |
|---|---|---|---|
| A | 低 | なし | 既存 progressive matrix で overhead < 5% を維持 |
| B | 中 | RTX 3090+ | LoRA 後の品質: 元 Qwen と同等 ± 5% |
| C | 中 | A100 1 台 ~1 週 | 蒸留後 llive-7b が qwen2.5:7b より MATH/RAD-grounded で +10% |
| D | 高 | A100 4-8 台 | 完全 train-from-scratch、Mamba / Hyena 並走比較 |
| E | 最高 | クラスタ | 学術論文化、Surprise loss が標準 training と差別化 |

## 「Qwen からの距離」を測る metric

新規評価指標として 3 つを導入 (REQUIREMENTS.md ORG-FX セクション):

### 1. Architectural Originality Score (AOS)

```
AOS = Σ (差別化 FR 実装数) / 全 FR 数
```

現状 (v0.6, 2026-05-17 時点): AOS ≈ 60% (周辺差別化のみ)
目標 (Phase 11 完了時): AOS ≥ 85%

### 2. LLM Core Independence Ratio (LCIR)

```
LCIR = (llive 専用 inference path のセル数) / (全 inference path のセル数)
```

現状: LCIR ≈ 0% (Qwen 完全依存)
目標 (Stage C 完了時): LCIR ≥ 50%

### 3. Replaceability Test

Qwen を抜いて llive-only で動作するか:
- Stage A: ❌ (Qwen 不在では動かない)
- Stage C: 🟡 (llive-7b で動作するが品質低下)
- Stage E: ✅ (Transformer 不要、Mamba 系で動作)

## 短期で何をすべきか

**Stage A (〜3 ヶ月)** で集中的に **「LLM を使わない層」を厚くする**:

1. **MATH-01/08 を Brief Grounder に統合** (今日着手済) — 計算は LLM ではなく SafeCalculator
2. **MATH-02 形式検証ゲート** — LLM 数式幻覚を Sympy/Z3 で検証して止める
3. **MATH-05 CODATA 辞書** — 物理定数を RAD metrology で grounded
4. **CREAT-01 KJ法ノード** — 拡散はテンプレート + clustering、LLM は最後の名前付けのみ
5. **CABT-01 forward hook** — Transformer 出力に memory bias を加える hook (重み凍結のまま)

これだけで「llive にしかできない計算」が大幅に増え、Qwen 直叩きとの差別化が
visible になります。

## 中期 (Stage B/C, 3〜12 ヶ月) の戦略判断

- **LoRA**: RTX 3090+ で訓練可、リスク中。元 Qwen に戻せる
- **蒸留**: A100 が必要、リスク中、llive 専用化が決定的になる
- **完全 train**: GPU クラスタ必要、研究予算が必須

GPU 投資の判断は中期計画で別途決定 (Stage B から始める想定)。

## 長期 (Stage D/E, 1〜3 年) の研究テーマ化

Stage D 以降は学術論文化候補:

- "**Cognitive Block Replacement**: Memory-coupled Transformer for Verifiable Agent Loops"
- "**Provenance-aware Attention**: Trust Score as Inductive Bias"
- "**Surprise-native Pretraining**: Bayesian Surprise as Loss Function"
- "**TRIZ-guided Neural Architecture Search**: 40 Principles for Network Mutation"

これらは ICML / NeurIPS / ICLR / AAAI で通る研究品質。Stage D が完成すれば
博士論文や著書のテーマにもなります。

## まとめ

llive の周辺独自性は十分。コア独自性を **5 段階で計画的に積む** ことで、
研究としての価値を持続させる:

- 短期: 周辺の厚みを最大化 (Stage A、今日進めた MATH/COG/CABT 計画)
- 中期: LoRA → 蒸留で「llive 専用 LLM」を作る (Stage B/C)
- 長期: Transformer 自体の置換 / Surprise-native pretraining (Stage D/E)

「普及している AI を使った方がマシ」と言われない設計に持ち込むには、
**「llive にしかできない計算」を増やし続けるだけでなく、コア自体が llive と
ともに進化する architecture** が必要です。

## ソース

- 要件: `llive/.planning/REQUIREMENTS.md` v2.0-core ORG-FX セクション
- ロードマップ: ROADMAP.md Phase 11 (ORG-FX) + Phase 12 (full independence)
- 関連: 同日記事 [09 — llive 構造の独自性点検](./09_llive_structure_originality.md)

## 同日の他公開資料

- [01 — Brief API + progressive matrix](./01_brief_api_progressive.md)
- [02 — 心理の深層 10 因子 × llive](./02_cognitive_factors.md)
- [03 — 数学・単位特化 AI (MATH-01/08)](./03_math_vertical.md)
- [04-06 — 設計予告 3 本 (CABT / CREAT / MATH-02)](./README.md)
- [07 — fair bench (honest disclosure)](./07_bench_results.md)
- [08 — quiz bench Debug vs Release](./08_quiz_bench_debug_vs_release.md)
- [09 — llive 構造独自性 8 要素](./09_llive_structure_originality.md)

---

> llive を「Qwen の上にラップ」から「Qwen を内蔵から外す」へ。5 段階で計画的に
> 独自路線に進む。

---

# English

# A 5-Stage Roadmap to Break Free From Qwen Dependence — Migrating llive's Originality Into the Core

Author: Kazufumi Furuse (Puruyan)

## TL;DR

- The current llive (v0.6) is **original as a peripheral cognitive OS**, but its **LLM core still depends on Qwen / Llama / Mistral**.
- A user observation: "Research has no value if it isn't differentiated. We'd be tempted to just say it's better to use a mainstream AI instead."
- For the sake of mid- to long-term research value, we are turning **making the core LLM itself original** into requirements as a 5-stage roadmap (ORG-FX, Phase 11).
- Short term: keep strengthening the periphery; mid term: LoRA → distillation; long term: Transformer block replacement → native Mamba/RWKV-class architectures.

## A "Layer-by-Layer" Analysis of the Current Differentiation

| Layer | llive Originality | Qwen Dependence |
|---|---|---|
| Input (Brief API) | ★★★★★ | 0% |
| Grounder (TRIZ × RAD) | ★★★★★ | 0% |
| 6-stage Loop | ★★★★☆ | 10% (formalizing thought as equations is original) |
| 4-layer memory | ★★★★☆ | 0% |
| Multi-track Filter | ★★★★☆ | 0% |
| Approval Bus | ★★★★★ | 0% |
| Governance Scoring | ★★★★★ | 0% |
| Trace Graph (Ledger) | ★★★★☆ | 0% |
| **LLM core (Decoder-only Transformer)** | ☆ | **100%** ← the problem |

→ The periphery is sufficiently original. **The originality of the core is untouched.** This is the weak point as research.

## Why the Core Needs to Be Made Original

### Reason 1: Value as research

If you merely use Qwen / Llama / Mistral / GPT frozen, the heart of the research becomes "someone else's weights + your own wrapper." From the standpoint of writing papers or taking a long-term view, a design that doesn't touch the core itself loses citation value.

### Reason 2: Differentiation from the mainstream

There is the worry of becoming "you'd be better off using a mainstream AI." To counter the logic of "if you're going to use Qwen, just use Qwen directly," you need to increase the amount of **computation only llive can do**. This means either increasing the **"deterministic layers that don't use an LLM"** — like MATH-08 (SafeCalculator) or CREAT-01 (KJ-method nodes) — or making **the LLM itself llive-exclusive**: two routes.

### Reason 3: Connection to industrial IoT

When connecting an LLM directly to industrial IoT via the llmesh sensor bridge (FR-19), Qwen's generality is not necessarily an advantage. A small, purpose-specialized LLM is:
- lower latency
- lower memory consumption
- higher domain-specific accuracy
- easier to audit for security

## The 5-Stage Roadmap

![The 5-stage roadmap to break free from Qwen dependence (flow from Stage A peripheral strengthening to Stage E non-Transformer core)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q10/roadmap_5stage_en.svg)

## The ORG-* Requirements Introduced at Each Stage

| FR | Name | Stage | Motivation |
|---|---|---|---|
| **ORG-06** | Provenance-aware tokens | B+D | Add a metadata column to each token, referenced in attention |
| **ORG-02** | Memory-coupled inference | C/D | Reference the 4-layer memory directly during LLM inference |
| **ORG-03** | Multi-track sub-network | C | A sub-network per EpistemicType (a cognitive version of MoE) |
| **ORG-08** | llive-specialized small model | C | qwen2.5:14b → llive-7b distillation |
| **ORG-07** | Approval-native decoding | C/D | Bring Approval inside the decoder |
| **ORG-01** | Cognitive Block Replacement | D | Synchronize Transformer blocks with llive's thinking layers |
| **ORG-04** | TRIZ-guided architecture search | D | Self-improve the LLM core |
| **ORG-05** | Surprise-native pretraining | E | Internalize Bayesian Surprise as the loss |

## Risks and Evaluation per Stage

| Stage | Risk | GPU Requirement | Evaluation Metric |
|---|---|---|---|
| A | Low | None | Keep overhead < 5% on the existing progressive matrix |
| B | Medium | RTX 3090+ | Post-LoRA quality: on par with original Qwen ± 5% |
| C | Medium | 1× A100, ~1 week | Distilled llive-7b beats qwen2.5:7b by +10% on MATH/RAD-grounded tasks |
| D | High | 4–8× A100 | Full train-from-scratch; parallel comparison against Mamba / Hyena |
| E | Highest | Cluster | Academic publication; Surprise loss differentiates from standard training |

## Metrics to Measure "Distance From Qwen"

We introduce three new evaluation metrics (REQUIREMENTS.md ORG-FX section):

### 1. Architectural Originality Score (AOS)

```
AOS = Σ (差別化 FR 実装数) / 全 FR 数
```

Current (v0.6, as of 2026-05-17): AOS ≈ 60% (peripheral differentiation only)
Target (at completion of Phase 11): AOS ≥ 85%

### 2. LLM Core Independence Ratio (LCIR)

```
LCIR = (llive 専用 inference path のセル数) / (全 inference path のセル数)
```

Current: LCIR ≈ 0% (fully dependent on Qwen)
Target (at completion of Stage C): LCIR ≥ 50%

### 3. Replaceability Test

Does it run llive-only with Qwen removed:
- Stage A: ❌ (does not run without Qwen)
- Stage C: 🟡 (runs on llive-7b, but with degraded quality)
- Stage E: ✅ (no Transformer needed; runs on Mamba-class architectures)

## What Should Be Done in the Short Term

In **Stage A (~3 months)**, intensively **thicken the "layers that don't use an LLM"**:

1. **Integrate MATH-01/08 into the Brief Grounder** (started today) — calculation goes through SafeCalculator, not the LLM.
2. **MATH-02 formal verification gate** — verify and halt LLM equation hallucinations with Sympy/Z3.
3. **MATH-05 CODATA dictionary** — ground physical constants in RAD metrology.
4. **CREAT-01 KJ-method nodes** — divergence is template + clustering; the LLM only does the final naming.
5. **CABT-01 forward hook** — a hook that adds memory bias to the Transformer output (weights stay frozen).

This alone greatly increases the "computation only llive can do" and makes the differentiation from hitting Qwen directly *visible*.

## Strategic Judgment for the Mid Term (Stage B/C, 3–12 months)

- **LoRA**: trainable on RTX 3090+, medium risk. Can be reverted to the original Qwen.
- **Distillation**: requires an A100, medium risk; llive-specialization becomes decisive.
- **Full train**: requires a GPU cluster; a research budget is essential.

The GPU investment decision will be made separately in the mid-term plan (the assumption is to start from Stage B).

## Turning the Long Term (Stage D/E, 1–3 years) Into Research Themes

From Stage D onward, these become candidates for academic publication:

- "**Cognitive Block Replacement**: Memory-coupled Transformer for Verifiable Agent Loops"
- "**Provenance-aware Attention**: Trust Score as Inductive Bias"
- "**Surprise-native Pretraining**: Bayesian Surprise as Loss Function"
- "**TRIZ-guided Neural Architecture Search**: 40 Principles for Network Mutation"

These are of research quality that would pass at ICML / NeurIPS / ICLR / AAAI. Once Stage D is complete, they could even become the theme of a doctoral dissertation or a book.

## Summary

llive's peripheral originality is sufficient. By **building core originality methodically across 5 stages**, we sustain its value as research:

- Short term: maximize the thickness of the periphery (Stage A; the MATH/COG/CABT plans advanced today).
- Mid term: build a "llive-exclusive LLM" via LoRA → distillation (Stage B/C).
- Long term: replace the Transformer itself / Surprise-native pretraining (Stage D/E).

To reach a design that won't be told "you'd be better off using a mainstream AI," you need not only to **keep increasing the "computation only llive can do," but also an architecture in which the core itself evolves together with llive**.

## Sources

- Requirements: `llive/.planning/REQUIREMENTS.md` v2.0-core, ORG-FX section
- Roadmap: ROADMAP.md Phase 11 (ORG-FX) + Phase 12 (full independence)
- Related: same-day article [09 — Inspecting the Originality of llive's Structure](./09_llive_structure_originality.md)

## Other Materials Published the Same Day

- [01 — Brief API + progressive matrix](./01_brief_api_progressive.md)
- [02 — The 10 deep-psychology factors × llive](./02_cognitive_factors.md)
- [03 — A math/units-specialized AI (MATH-01/08)](./03_math_vertical.md)
- [04-06 — Three design previews (CABT / CREAT / MATH-02)](./README.md)
- [07 — fair bench (honest disclosure)](./07_bench_results.md)
- [08 — quiz bench Debug vs Release](./08_quiz_bench_debug_vs_release.md)
- [09 — The 8 elements of llive structural originality](./09_llive_structure_originality.md)

---

> Move llive from "wrapping over Qwen" to "removing Qwen from the inside." Advance methodically down the path of originality in 5 stages.

---

# 中文

# 摆脱 Qwen 依赖的 5 阶段路线图 —— 把 llive 的独创性移植进内核

作者：古濑 和文（Puruyan）

## TL;DR

- 目前的 llive (v0.6) **作为外围认知 OS 是独创的**，但 **LLM 内核仍依赖 Qwen / Llama / Mistral**。
- 用户的观察：「不做差异化，研究就没有价值。很容易让人觉得，还不如直接用普及的 AI 算了。」
- 为了中长期的研究价值，我们把 **让内核 LLM 本身独创化** 拆成 5 阶段路线图并需求化（ORG-FX, Phase 11）。
- 短期保持强化外围，中期 LoRA → 蒸馏，长期替换 Transformer block → 转向 Mamba/RWKV 系原生架构。

## 对当前差异化的「分层」分析

| 层 | llive 独创性 | Qwen 依赖度 |
|---|---|---|
| 输入 (Brief API) | ★★★★★ | 0% |
| Grounder (TRIZ × RAD) | ★★★★★ | 0% |
| 6 阶段 Loop | ★★★★☆ | 10%（把思考公式化是独创的） |
| 4 层记忆 | ★★★★☆ | 0% |
| Multi-track Filter | ★★★★☆ | 0% |
| Approval Bus | ★★★★★ | 0% |
| Governance Scoring | ★★★★★ | 0% |
| Trace Graph (Ledger) | ★★★★☆ | 0% |
| **LLM 内核（Decoder-only Transformer）** | ☆ | **100%** ← 问题所在 |

→ 外围已经足够独创。**内核的独创性尚未着手。** 这是作为研究的薄弱点。

## 为什么需要让内核独创化

### 理由 1：作为研究的价值

如果只是把 Qwen / Llama / Mistral / GPT 冻结后使用，研究的核心就变成了「别人的权重 + 自己的封装」。从论文化或长期视角来看，不动内核本身的设计，引用价值会下降。

### 理由 2：与普及方案的差异化

存在「还不如用普及的 AI」这一隐忧。要对抗「既然要用 Qwen，直接用 Qwen 就好」的逻辑，就必须增加 **只有 llive 才能做的计算**。这意味着要么增加 **「不使用 LLM 的确定性层」**——如 MATH-08 (SafeCalculator) 或 CREAT-01 (KJ 法节点)，要么让 **LLM 本身成为 llive 专用**：两条路线。

### 理由 3：与工业 IoT 的连接

通过 llmesh sensor bridge (FR-19) 将 LLM 直接接入工业 IoT 时，Qwen 的通用性未必是优势。专门特化的小型 LLM 反而：
- 延迟更低
- 内存占用更少
- 领域特化精度更高
- 安全审计更容易

## 5 阶段路线图

```
Stage A (短期, 〜3 ヶ月)
  ├ LLM コアは凍結
  ├ 周辺差別化を最大化
  └ CABT forward hook / MATH-08 / CREAT-01 で「LLM を使わない層」を厚く
       ↓
Stage B (中期 1, 3〜6 ヶ月)
  ├ LoRA で llive 用 specialised adapter
  ├ RTX 3090 級で訓練可
  └ Attention に memory bias を注入 (CABT-07 本実装の前段)
       ↓
Stage C (中期 2, 6〜12 ヶ月)
  ├ Distillation: qwen2.5:14b → llive-7b
  ├ 学習データ: RAD 49 分野 + ledger 成功例 + TRIZ 出力
  └ Multi-track sub-network (EpistemicType 別)
       ↓
Stage D (長期 1, 1〜2 年)
  ├ Transformer block を memory-coupled に置換
  ├ Cognitive Block Replacement (CABT-01〜07 の本実装)
  └ Approval-native decoding (constitutional AI の architectural 版)
       ↓
Stage E (長期 2, 2〜3 年)
  ├ Transformer 以外の LLM コア (Mamba / RWKV / Hyena / RetNet)
  ├ Surprise-native pretraining (Bayesian Surprise を loss に組込)
  └ TRIZ-guided architecture search (AutoML-Zero + TRIZ ハイブリッド)
```

## 每个 Stage 引入的 ORG-* 需求

| FR | 名称 | Stage | 动机 |
|---|---|---|---|
| **ORG-06** | Provenance-aware tokens | B+D | 为每个 token 增加一个 metadata 列，并在 attention 中引用 |
| **ORG-02** | Memory-coupled inference | C/D | LLM 推理时直接引用 4 层记忆 |
| **ORG-03** | Multi-track sub-network | C | 按 EpistemicType 划分的 sub-network（认知版的 MoE） |
| **ORG-08** | llive-specialized small model | C | qwen2.5:14b → llive-7b 蒸馏 |
| **ORG-07** | Approval-native decoding | C/D | 把 Approval 带入 decoder 内部 |
| **ORG-01** | Cognitive Block Replacement | D | 让 Transformer block 与 llive 的思考层同步 |
| **ORG-04** | TRIZ-guided architecture search | D | 自我改良 LLM 内核 |
| **ORG-05** | Surprise-native pretraining | E | 把 Bayesian Surprise 内化为 loss |

## 各 Stage 的风险与评估

| Stage | 风险 | GPU 需求 | 评估指标 |
|---|---|---|---|
| A | 低 | 无 | 在现有 progressive matrix 上维持 overhead < 5% |
| B | 中 | RTX 3090+ | LoRA 后的质量：与原 Qwen 同等 ± 5% |
| C | 中 | 1 台 A100，约 1 周 | 蒸馏后的 llive-7b 在 MATH/RAD-grounded 上比 qwen2.5:7b 高 +10% |
| D | 高 | 4-8 台 A100 | 完全 train-from-scratch，与 Mamba / Hyena 并行比较 |
| E | 最高 | 集群 | 学术论文化，Surprise loss 与标准 training 形成差异化 |

## 衡量「与 Qwen 的距离」的 metric

引入三个新的评估指标（REQUIREMENTS.md ORG-FX 部分）：

### 1. Architectural Originality Score (AOS)

```
AOS = Σ (差別化 FR 実装数) / 全 FR 数
```

当前 (v0.6, 截至 2026-05-17)：AOS ≈ 60%（仅外围差异化）
目标（Phase 11 完成时）：AOS ≥ 85%

### 2. LLM Core Independence Ratio (LCIR)

```
LCIR = (llive 専用 inference path のセル数) / (全 inference path のセル数)
```

当前：LCIR ≈ 0%（完全依赖 Qwen）
目标（Stage C 完成时）：LCIR ≥ 50%

### 3. Replaceability Test

抽掉 Qwen 后能否以 llive-only 运行：
- Stage A: ❌（没有 Qwen 就无法运行）
- Stage C: 🟡（能在 llive-7b 上运行，但质量下降）
- Stage E: ✅（不需要 Transformer，可在 Mamba 系上运行）

## 短期内应该做什么

在 **Stage A（〜3 个月）** 集中地 **加厚「不使用 LLM 的层」**：

1. **将 MATH-01/08 集成进 Brief Grounder**（今天已着手）—— 计算交给 SafeCalculator，而不是 LLM。
2. **MATH-02 形式验证门**—— 用 Sympy/Z3 验证并拦截 LLM 的公式幻觉。
3. **MATH-05 CODATA 词典**—— 用 RAD metrology 为物理常数提供 grounding。
4. **CREAT-01 KJ 法节点**—— 发散用模板 + clustering，LLM 只负责最后的命名。
5. **CABT-01 forward hook**—— 给 Transformer 输出加上 memory bias 的 hook（权重保持冻结）。

仅此一项就能大幅增加「只有 llive 才能做的计算」，让与直接调用 Qwen 的差异化变得 *可见*。

## 中期（Stage B/C, 3〜12 个月）的战略判断

- **LoRA**：可在 RTX 3090+ 上训练，风险中等。可回退到原始 Qwen。
- **蒸馏**：需要 A100，风险中等，llive 专用化将变得决定性。
- **完全训练**：需要 GPU 集群，研究预算必不可少。

GPU 投资的决策将在中期计划中另行确定（设想从 Stage B 开始）。

## 把长期（Stage D/E, 1〜3 年）研究主题化

从 Stage D 起，以下成为学术论文化的候选：

- "**Cognitive Block Replacement**: Memory-coupled Transformer for Verifiable Agent Loops"
- "**Provenance-aware Attention**: Trust Score as Inductive Bias"
- "**Surprise-native Pretraining**: Bayesian Surprise as Loss Function"
- "**TRIZ-guided Neural Architecture Search**: 40 Principles for Network Mutation"

这些都达到了能在 ICML / NeurIPS / ICLR / AAAI 上通过的研究质量。一旦 Stage D 完成，它们甚至可以成为博士论文或著作的主题。

## 总结

llive 的外围独创性已经足够。通过 **用 5 个阶段有计划地积累内核独创性**，使其作为研究的价值得以持续：

- 短期：最大化外围的厚度（Stage A，今天推进的 MATH/COG/CABT 计划）。
- 中期：用 LoRA → 蒸馏打造「llive 专用 LLM」（Stage B/C）。
- 长期：替换 Transformer 本身 / Surprise-native pretraining（Stage D/E）。

要做到一个不会被说「还不如用普及的 AI」的设计，不仅要 **持续增加「只有 llive 才能做的计算」，还需要一种内核本身与 llive 一同进化的 architecture**。

## 来源

- 需求：`llive/.planning/REQUIREMENTS.md` v2.0-core，ORG-FX 部分
- 路线图：ROADMAP.md Phase 11 (ORG-FX) + Phase 12 (full independence)
- 相关：同日文章 [09 — 点检 llive 结构的独创性](./09_llive_structure_originality.md)

## 同日发布的其他材料

- [01 — Brief API + progressive matrix](./01_brief_api_progressive.md)
- [02 — 心理深层的 10 因子 × llive](./02_cognitive_factors.md)
- [03 — 数学・单位特化 AI (MATH-01/08)](./03_math_vertical.md)
- [04-06 — 三篇设计预告 (CABT / CREAT / MATH-02)](./README.md)
- [07 — fair bench (honest disclosure)](./07_bench_results.md)
- [08 — quiz bench Debug vs Release](./08_quiz_bench_debug_vs_release.md)
- [09 — llive 结构独创性 8 要素](./09_llive_structure_originality.md)

---

> 把 llive 从「在 Qwen 之上封装」转向「从内部移除 Qwen」。用 5 个阶段有计划地走向独创路线。

---

# 한국어

# Qwen 의존에서 벗어나는 5 단계 로드맵 — llive 의 독자성을 코어로 이식하다

저자: 후루세 가즈후미 (Puruyan)

## TL;DR

- 현재의 llive (v0.6) 는 **주변 인지 OS 로서는 독자적**이지만, **LLM 코어는 Qwen / Llama / Mistral 에 의존**하고 있다.
- 사용자 관찰: "차별화되어 있지 않으면 연구의 가치가 없다. 보급된 AI 를 쓰는 편이 낫다는 식이 되어 버릴 것 같다."
- 중장기적 연구 가치를 위해 **코어 LLM 자체의 독자화**를 5 단계 로드맵으로 요건화한다 (ORG-FX, Phase 11).
- 단기는 주변 강화를 유지, 중기는 LoRA → 증류, 장기는 Transformer block 치환 → Mamba/RWKV 계열 native.

## 현재 차별화의 "계층별" 분석

| 계층 | llive 독자성 | Qwen 의존도 |
|---|---|---|
| 입력 (Brief API) | ★★★★★ | 0% |
| Grounder (TRIZ × RAD) | ★★★★★ | 0% |
| 6 단계 Loop | ★★★★☆ | 10% (사고의 수식화는 독자적) |
| 4 계층 메모리 | ★★★★☆ | 0% |
| Multi-track Filter | ★★★★☆ | 0% |
| Approval Bus | ★★★★★ | 0% |
| Governance Scoring | ★★★★★ | 0% |
| Trace Graph (Ledger) | ★★★★☆ | 0% |
| **LLM 코어 (Decoder-only Transformer)** | ☆ | **100%** ← 문제 |

→ 주변은 충분히 독자적. **코어의 독자성은 손대지 않았다.** 이것이 연구로서의 약점.

## 왜 코어를 독자화할 필요가 있는가

### 이유 1: 연구로서의 가치

Qwen / Llama / Mistral / GPT 를 frozen 으로 쓰기만 하면 연구의 핵심이 "남의 가중치 + 자신의 래퍼"가 된다. 논문화나 장기적 관점에서 보면, 코어 자체에 손대지 않은 설계는 인용 가치가 떨어진다.

### 이유 2: 보급된 것과의 차별화

"보급된 AI 를 쓰는 편이 낫다"가 될 우려. Qwen 을 쓸 거면 직접 Qwen 을 쓰면 된다는 논리에 맞서려면, **llive 만이 할 수 있는 계산**을 늘릴 필요가 있다. 이것은 MATH-08 (SafeCalculator) 나 CREAT-01 (KJ법 노드) 같은 **"LLM 을 쓰지 않는 결정론적 계층"** 을 늘리거나, **"LLM 자체를 llive 전용"** 으로 만드는 두 가지 노선이다.

### 이유 3: 산업 IoT 와의 연결

llmesh sensor bridge (FR-19) 로 산업 IoT 에 LLM 을 직접 연결할 경우, Qwen 의 범용성이 반드시 유리한 것은 아니다. 전용으로 특화된 소형 LLM 쪽이:
- 지연시간이 낮다
- 메모리 소비가 적다
- 도메인 특화 정확도가 높다
- 보안 감사가 쉽다

## 5 단계 로드맵

```
Stage A (短期, 〜3 ヶ月)
  ├ LLM コアは凍結
  ├ 周辺差別化を最大化
  └ CABT forward hook / MATH-08 / CREAT-01 で「LLM を使わない層」を厚く
       ↓
Stage B (中期 1, 3〜6 ヶ月)
  ├ LoRA で llive 用 specialised adapter
  ├ RTX 3090 級で訓練可
  └ Attention に memory bias を注入 (CABT-07 本実装の前段)
       ↓
Stage C (中期 2, 6〜12 ヶ月)
  ├ Distillation: qwen2.5:14b → llive-7b
  ├ 学習データ: RAD 49 分野 + ledger 成功例 + TRIZ 出力
  └ Multi-track sub-network (EpistemicType 別)
       ↓
Stage D (長期 1, 1〜2 年)
  ├ Transformer block を memory-coupled に置換
  ├ Cognitive Block Replacement (CABT-01〜07 の本実装)
  └ Approval-native decoding (constitutional AI の architectural 版)
       ↓
Stage E (長期 2, 2〜3 年)
  ├ Transformer 以外の LLM コア (Mamba / RWKV / Hyena / RetNet)
  ├ Surprise-native pretraining (Bayesian Surprise を loss に組込)
  └ TRIZ-guided architecture search (AutoML-Zero + TRIZ ハイブリッド)
```

## 각 Stage 에서 도입하는 ORG-* 요건

| FR | 이름 | Stage | 동기 |
|---|---|---|---|
| **ORG-06** | Provenance-aware tokens | B+D | 각 token 에 metadata 열을 추가하고 attention 에서 참조 |
| **ORG-02** | Memory-coupled inference | C/D | LLM 추론 시 4 계층 메모리를 직접 참조 |
| **ORG-03** | Multi-track sub-network | C | EpistemicType 별 sub-network (MoE 의 인지 버전) |
| **ORG-08** | llive-specialized small model | C | qwen2.5:14b → llive-7b 증류 |
| **ORG-07** | Approval-native decoding | C/D | Approval 을 decoder 내부로 가져오기 |
| **ORG-01** | Cognitive Block Replacement | D | Transformer block 을 llive 의 사고 계층과 동기화 |
| **ORG-04** | TRIZ-guided architecture search | D | LLM 코어를 자기 개량 |
| **ORG-05** | Surprise-native pretraining | E | Bayesian Surprise 를 loss 에 내재화 |

## 각 Stage 의 리스크와 평가

| Stage | 리스크 | GPU 필요량 | 평가 지표 |
|---|---|---|---|
| A | 낮음 | 없음 | 기존 progressive matrix 에서 overhead < 5% 유지 |
| B | 중간 | RTX 3090+ | LoRA 후 품질: 원래 Qwen 과 동등 ± 5% |
| C | 중간 | A100 1 대 ~1 주 | 증류 후 llive-7b 가 qwen2.5:7b 보다 MATH/RAD-grounded 에서 +10% |
| D | 높음 | A100 4-8 대 | 완전 train-from-scratch, Mamba / Hyena 병행 비교 |
| E | 최고 | 클러스터 | 학술 논문화, Surprise loss 가 표준 training 과 차별화 |

## "Qwen 으로부터의 거리"를 재는 metric

새로운 평가 지표로 세 가지를 도입한다 (REQUIREMENTS.md ORG-FX 섹션):

### 1. Architectural Originality Score (AOS)

```
AOS = Σ (差別化 FR 実装数) / 全 FR 数
```

현재 (v0.6, 2026-05-17 시점): AOS ≈ 60% (주변 차별화만)
목표 (Phase 11 완료 시): AOS ≥ 85%

### 2. LLM Core Independence Ratio (LCIR)

```
LCIR = (llive 専用 inference path のセル数) / (全 inference path のセル数)
```

현재: LCIR ≈ 0% (Qwen 완전 의존)
목표 (Stage C 완료 시): LCIR ≥ 50%

### 3. Replaceability Test

Qwen 을 빼고 llive-only 로 동작하는가:
- Stage A: ❌ (Qwen 없이는 동작하지 않음)
- Stage C: 🟡 (llive-7b 로 동작하지만 품질 저하)
- Stage E: ✅ (Transformer 불필요, Mamba 계열로 동작)

## 단기에 무엇을 해야 하는가

**Stage A (〜3 개월)** 에서 집중적으로 **"LLM 을 쓰지 않는 계층"을 두껍게 한다**:

1. **MATH-01/08 을 Brief Grounder 에 통합** (오늘 착수함) — 계산은 LLM 이 아니라 SafeCalculator.
2. **MATH-02 형식 검증 게이트** — LLM 의 수식 환각을 Sympy/Z3 로 검증하여 멈춘다.
3. **MATH-05 CODATA 사전** — 물리 상수를 RAD metrology 로 grounding.
4. **CREAT-01 KJ법 노드** — 발산은 템플릿 + clustering, LLM 은 마지막 이름 붙이기만.
5. **CABT-01 forward hook** — Transformer 출력에 memory bias 를 더하는 hook (가중치는 frozen 유지).

이것만으로도 "llive 만이 할 수 있는 계산"이 크게 늘어, Qwen 직접 호출과의 차별화가 *가시화*된다.

## 중기 (Stage B/C, 3〜12 개월) 의 전략 판단

- **LoRA**: RTX 3090+ 에서 훈련 가능, 리스크 중간. 원래 Qwen 으로 되돌릴 수 있다.
- **증류**: A100 이 필요, 리스크 중간, llive 전용화가 결정적이 된다.
- **완전 train**: GPU 클러스터 필요, 연구 예산이 필수.

GPU 투자 판단은 중기 계획에서 별도로 결정 (Stage B 부터 시작하는 것을 상정).

## 장기 (Stage D/E, 1〜3 년) 의 연구 테마화

Stage D 이후는 학술 논문화 후보:

- "**Cognitive Block Replacement**: Memory-coupled Transformer for Verifiable Agent Loops"
- "**Provenance-aware Attention**: Trust Score as Inductive Bias"
- "**Surprise-native Pretraining**: Bayesian Surprise as Loss Function"
- "**TRIZ-guided Neural Architecture Search**: 40 Principles for Network Mutation"

이들은 ICML / NeurIPS / ICLR / AAAI 에서 통과할 연구 품질이다. Stage D 가 완성되면 박사 논문이나 저서의 테마도 될 수 있다.

## 정리

llive 의 주변 독자성은 충분하다. 코어 독자성을 **5 단계로 계획적으로 쌓아 올림**으로써, 연구로서의 가치를 지속시킨다:

- 단기: 주변의 두께를 최대화 (Stage A, 오늘 진행한 MATH/COG/CABT 계획).
- 중기: LoRA → 증류로 "llive 전용 LLM"을 만든다 (Stage B/C).
- 장기: Transformer 자체의 치환 / Surprise-native pretraining (Stage D/E).

"보급된 AI 를 쓰는 편이 낫다"는 말을 듣지 않을 설계로 가져가려면, **"llive 만이 할 수 있는 계산"을 계속 늘리는 것뿐 아니라, 코어 자체가 llive 와 함께 진화하는 architecture** 가 필요하다.

## 소스

- 요건: `llive/.planning/REQUIREMENTS.md` v2.0-core, ORG-FX 섹션
- 로드맵: ROADMAP.md Phase 11 (ORG-FX) + Phase 12 (full independence)
- 관련: 같은 날 기사 [09 — llive 구조의 독자성 점검](./09_llive_structure_originality.md)

## 같은 날 공개한 다른 자료

- [01 — Brief API + progressive matrix](./01_brief_api_progressive.md)
- [02 — 심리의 심층 10 인자 × llive](./02_cognitive_factors.md)
- [03 — 수학・단위 특화 AI (MATH-01/08)](./03_math_vertical.md)
- [04-06 — 설계 예고 3 편 (CABT / CREAT / MATH-02)](./README.md)
- [07 — fair bench (honest disclosure)](./07_bench_results.md)
- [08 — quiz bench Debug vs Release](./08_quiz_bench_debug_vs_release.md)
- [09 — llive 구조 독자성 8 요소](./09_llive_structure_originality.md)

---

> llive 를 "Qwen 위에 래핑"에서 "Qwen 을 내장에서 빼낸다"로. 5 단계로 계획적으로 독자 노선으로 나아간다.
