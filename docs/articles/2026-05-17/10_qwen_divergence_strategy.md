---
layout: default
title: "Qwen 依存から離脱する 5 段階ロードマップ — llive の独自性をコアに移植する"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags: [llm, architecture, originality, qwen, distillation, mamba, research]
---

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

- 要件: `D:/projects/llive/.planning/REQUIREMENTS.md` v2.0-core ORG-FX セクション
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
