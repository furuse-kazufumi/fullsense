---
layout: default
title: "Qwen と相互補完する llive — Local 環境で『隙間』を埋める設計"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags: [llm, complementary, on-prem, local, qwen, llive, niche]
id: f400cf06e86b350b055c
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# Qwen と相互補完する llive — Local 環境で『隙間』を埋める設計

著者: 古瀬 和文（ぷるやん）

## TL;DR

- 前記事 [10](./QIITA_%2310_qwen_divergence_strategy.md) で「Qwen から離脱する 5 段階」を提示したが、**完全離脱だけが path ではない**
- ユーザー観察 (2026-05-17): 「相互補完の関係を目指すのもあり。もともと llive は Local 環境で動かす想定のもの。隙間をうまく補間できるといい」
- llive の差別化軸を **「Qwen を置換」から「Qwen と相互補完」** に再フレーム
- Local 環境特有の隙間 5 領域 (計算 / 記憶 / 監査 / 認知構造 / オフライン) で llive が Qwen を補う設計

## 「離脱」vs「相互補完」の二択は両立する

実は前記事 10 の Stage A (短期、〜3 ヶ月) は **相互補完戦略** そのもの:

- LLM コアは凍結 (Qwen をそのまま使う)
- 周辺差別化を最大化 (CABT / MATH / CREAT)
- 「Qwen が苦手 → llive が決定論的に補完」

ただし Stage B〜E (中長期) は「独自化路線」。両者は **同時並走** が可能で:

![補完路線と独自化路線の二層構造図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q11/two_routes.svg)

「Local 環境で隙間補完」を **常設のポジション** とし、その上に「研究路線として
独自化」を積む二層構造。

## llive が Qwen を補完する 5 つの「隙間」

### 隙間 1: 数値計算・記号操作・形式検証

| Qwen の弱点 | llive の補完 |
|---|---|
| `(2.5 * 7.8) / 0.3` を間違える | **MATH-08 SafeCalculator** (AST + 決定論) |
| `5 m/s + 3 s = 8` (次元誤り) | **MATH-01 SI 次元解析** |
| `(x+1)² = x² + 2x` (記号幻覚) | **MATH-02 Sympy 検算 + EVO-04 Z3** |
| CODATA 値の捏造 | **MATH-05 物理定数辞書** (grounded) |

LLM は「言語的に妥当な式」を出すのは得意だが「数学的に正しい式」は苦手。
llive が決定論的サイドカーとして補完する。

### 隙間 2: 長期記憶・経験再生

| Qwen の弱点 | llive の補完 |
|---|---|
| context window (32K-128K) の限界 | **4 層メモリ** (semantic / episodic / structural / parameter) |
| session を跨ぐ記憶不能 | **persistent memory** + provenance |
| 同じ間違いを繰り返す | **Failed Reservoir** (EVO-06) + Reverse-Evo Monitor (EVO-07) |
| 「自分が以前何を言ったか」忘れる | **append-only ledger** (BriefLedger / SqliteLedger) |

LLM は stateless。llive が memory layer として補完する。

### 隙間 3: 行動監査・責任所在

| Qwen の弱点 | llive の補完 |
|---|---|
| 危険な動作の architectural gate なし | **Approval Bus** + Policy + SQLite Ledger (C-1) |
| 出力責任の追跡困難 | **Provenance chain** + SHA-256 audit chain (SEC-03) |
| dangerous tokens (rm -rf 等) のフィルタなし | **GovernanceScorer** (COG-02, 4 軸 scoring) |
| 監査ログがエフェメラル | **persistent JSONL + replay** 可 |

LLM 単体ではコンプライアンス対応が困難。llive が監査基盤を提供。

### 隙間 4: 認知構造・多視点・矛盾解決

| Qwen の弱点 | llive の補完 |
|---|---|
| 視野狭窄 (最初の候補に引きずられる) | **CREAT-01 KJ法ノード** (拡散 ≥20 件強制) |
| 思考の浅さ (1 階層展開) | **CREAT-02 MindMap** (DFS depth=3) |
| 偏った楽観 | **CREAT-04 Six Hats** (cautious 観点強制) |
| 既存パターン依存 | **CREAT-05 Synectics** (異分野類比) |
| 矛盾を扱えない | **TRIZ 40 原理** (FR-23〜27) |

LLM の "思考の浅さ" を、llive の認知構造で補完する。

### 隙間 5: Local 環境特有の制約

これは llive の **設計コンセプトと完全一致**:

| Local 環境の特性 | llive の対応 |
|---|---|
| ネットワーク不在 | **完全 on-prem 動作** (Ollama / LM Studio / vLLM) |
| 個人データを外に出せない | **provenance + Quarantined Zone** (SEC-01) |
| 計測機器との直接接続 | **llmesh sensor bridge** (FR-19, MQTT/OPC-UA) |
| エッジ推論 (低スペック) | **MATH-08 等の決定論的層** (LLM を呼ばない) |
| プライバシー (家族の会話、医療情報) | **Local-only ledger** + クラウド送信ゼロ |
| 起動時間・通信遅延の制約 | **Brief API の overhead < 1 %** (実測済) |

cloud LLM (GPT / Claude / Gemini / Perplexity) では **絶対に再現できない領域**。
これが llive の **不変の差別化軸**。

## 「隙間補完」のメンタルモデル

```
        ┌─────────────────────────────────┐
        │  Qwen (汎用言語能力)              │
        │  ├ 言語流暢性 ★★★★★              │
        │  ├ 文章生成 ★★★★★               │
        │  ├ 多言語 ★★★★★                 │
        │  ├ 一般知識 ★★★★☆               │
        │  ├ 推論 ★★★★☆                  │
        │  └─ 数値計算 ★★☆☆☆ ← 隙間 ─┐  │
        └────────────────────────────┼───┘
                                     ↓
        ┌─────────────────────────────────┐
        │  llive (認知 OS + 補完層)         │
        │  ├ 数値計算 ★★★★★ (MATH-08)      │
        │  ├ 単位次元 ★★★★★ (MATH-01)      │
        │  ├ 形式検証 ★★★★★ (MATH-02)      │
        │  ├ 長期記憶 ★★★★★ (4 層メモリ)   │
        │  ├ 監査 ★★★★★ (Approval Bus)    │
        │  ├ 認知構造 ★★★★★ (CREAT/TRIZ)  │
        │  └ Local on-prem ★★★★★          │
        └─────────────────────────────────┘
```

Qwen は **言語能力** で強く、llive は **その隙間 (計算・記憶・監査・認知構造・Local)** で強い。両者を組み合わせると、cloud LLM 単独でも、ollama 単独でも到達できない領域に届く。

## 評価ベンチへの示唆

「llive vs Qwen」の **対立構図** で測ると、Qwen の言語能力 × llive の決定論的層が **同じ axis で競合** することになり不公平。

代わりに以下の **協調 axis** で測るべき:

- **Hybrid task score**: Qwen のみ vs llive (= Qwen + 決定論的補完層) の **総合スコア**
- **Niche task score**: Qwen が苦手なタスク (数値計算 / 単位 / 形式検証) で llive がどれだけ補えるか
- **Local capability**: ネットワークなしで完結する task の網羅率
- **Audit completeness**: 出力に対する trace coverage

これらは記事 08 で示した quiz bench のさらに上位の評価軸として、次回 (Phase 4
Production 後) に導入予定。

## 結論

llive の戦略は **二層構造**:

1. **常設の補完路線** (Local 環境特化 + 5 隙間補完): これは Qwen / Llama / Mistral / 等の OSS LLM が進化しても **不変の価値**
2. **研究としての独自化路線** (ORG-FX 5 段階): 中長期的に研究価値を持続

「普及している AI を使った方がマシ」と言われる懸念に対しては、**「llive を使う = Qwen を使う上で Local + 計算 + 監査 + 認知構造 を全部得られる」** という **複合価値** で答える。

「単独で使うなら Qwen で十分」かもしれない。しかし **「Qwen を Local 環境で安全に責任を持って使う」なら llive が最短経路**、というポジションを取る。

## 関連 ORG-FX 要件 (補完視点の再解釈)

| ORG-FX FR | 補完戦略での解釈 |
|---|---|
| ORG-06 Provenance-aware tokens | Qwen の token に llive の trust score を付与 |
| ORG-02 Memory-coupled inference | Qwen 推論時に llive memory を直接参照 |
| ORG-07 Approval-native decoding | Qwen 出力を llive Approval policy で filter |
| ORG-08 llive-specialized distillation | Qwen-shaped, llive-aware な小型 model |

つまり **ORG-* 要件は「Qwen との分離」だけでなく「Qwen との癒着」にも使える**。
どちらの方向に進むかは、各 Stage で再評価する。

## ソース

- 要件: `llive/.planning/REQUIREMENTS.md` v2.0-core ORG-FX (補完視点での再解釈)
- 関連記事: [10 — Qwen 依存から離脱する 5 段階](./10_qwen_divergence_strategy.md)
- 関連 memory:
  - `feedback_llive_measurement_purity` — Local + on-prem 純度ルール
  - `project_llive` — llive 全体 (Local 環境で動かす想定が明記)

## 同日の他公開資料

- [01](./QIITA_%2301_brief_api_progressive.md) Brief API
- [02](./QIITA_%2302_cognitive_factors.md) 10 思考因子
- [03](./QIITA_%2303_math_vertical.md) 数学・単位
- [04-06]({{ '/articles/2026-05-17/README' | relative_url }}) 設計予告 3 本
- [07](./QIITA_%2307_bench_results.md) fair bench
- [08](./QIITA_%2308_quiz_bench_debug_vs_release.md) quiz bench
- [09](./QIITA_%2309_llive_structure_originality.md) llive 独自性 8 要素
- [10](./QIITA_%2310_qwen_divergence_strategy.md) Qwen 離脱 5 段階

---

> 完全置換だけが path ではない。Local 環境で 5 隙間を補完する llive は、Qwen が進化しても価値が落ちない。

---

# English

# llive Complementing Qwen — Designing to Fill the "Gaps" in the Local Environment

Author: Kazufumi Furuse (Puruyan)

## TL;DR

- The previous article [10](./QIITA_%2310_qwen_divergence_strategy.md) presented "5 stages of breaking away from Qwen," but **full divergence is not the only path**.
- User observation (2026-05-17): "Aiming for a complementary relationship is also valid. llive was originally designed to run in the Local environment. It would be great if it could nicely fill the gaps."
- We re-frame llive's axis of differentiation **from 'replacing Qwen' to 'complementing Qwen'**.
- A design where llive complements Qwen across 5 gap areas specific to the Local environment (compute / memory / audit / cognitive structure / offline).

## The dichotomy of "divergence" vs "complementarity" is reconcilable

In fact, Stage A (short-term, up to ~3 months) of the previous article 10 is itself the **complementary strategy**:

- The LLM core is frozen (Qwen is used as-is)
- Peripheral differentiation is maximized (CABT / MATH / CREAT)
- "Where Qwen is weak → llive complements deterministically"

However, Stages B through E (mid-to-long term) follow the "independence route." The two can **run in parallel at the same time**:

![Two-layer structure: complementary route and independence route](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q11/two_routes_en.svg)

A two-layer structure that treats "filling gaps in the Local environment" as a **permanent position**, on top of which "independence as a research route" is stacked.

## The 5 "gaps" where llive complements Qwen

### Gap 1: Numerical computation, symbolic manipulation, formal verification

| Qwen's weakness | llive's complement |
|---|---|
| Gets `(2.5 * 7.8) / 0.3` wrong | **MATH-08 SafeCalculator** (AST + deterministic) |
| `5 m/s + 3 s = 8` (dimension error) | **MATH-01 SI dimensional analysis** |
| `(x+1)² = x² + 2x` (symbolic hallucination) | **MATH-02 Sympy verification + EVO-04 Z3** |
| Fabricating CODATA values | **MATH-05 physical constants dictionary** (grounded) |

LLMs are good at producing "linguistically plausible expressions" but poor at "mathematically correct expressions."
llive complements this as a deterministic sidecar.

### Gap 2: Long-term memory, experience replay

| Qwen's weakness | llive's complement |
|---|---|
| The limits of the context window (32K-128K) | **4-layer memory** (semantic / episodic / structural / parameter) |
| Inability to remember across sessions | **persistent memory** + provenance |
| Repeating the same mistakes | **Failed Reservoir** (EVO-06) + Reverse-Evo Monitor (EVO-07) |
| Forgetting "what I said before" | **append-only ledger** (BriefLedger / SqliteLedger) |

LLMs are stateless. llive complements this as a memory layer.

### Gap 3: Action audit, locus of responsibility

| Qwen's weakness | llive's complement |
|---|---|
| No architectural gate for dangerous operations | **Approval Bus** + Policy + SQLite Ledger (C-1) |
| Difficulty tracing output responsibility | **Provenance chain** + SHA-256 audit chain (SEC-03) |
| No filter for dangerous tokens (rm -rf etc.) | **GovernanceScorer** (COG-02, 4-axis scoring) |
| Ephemeral audit logs | **persistent JSONL + replay** possible |

Compliance is difficult for an LLM alone. llive provides the audit infrastructure.

### Gap 4: Cognitive structure, multiple perspectives, contradiction resolution

| Qwen's weakness | llive's complement |
|---|---|
| Tunnel vision (anchored to the first candidate) | **CREAT-01 KJ-method nodes** (forces divergence of ≥20 items) |
| Shallow thinking (single-level expansion) | **CREAT-02 MindMap** (DFS depth=3) |
| Biased optimism | **CREAT-04 Six Hats** (forces the cautious perspective) |
| Dependence on existing patterns | **CREAT-05 Synectics** (cross-domain analogy) |
| Cannot handle contradictions | **TRIZ 40 principles** (FR-23 through 27) |

We complement the LLM's "shallow thinking" with llive's cognitive structure.

### Gap 5: Constraints specific to the Local environment

This is a **perfect match with llive's design concept**:

| Characteristic of the Local environment | llive's response |
|---|---|
| Absence of network | **Fully on-prem operation** (Ollama / LM Studio / vLLM) |
| Personal data cannot be sent outside | **provenance + Quarantined Zone** (SEC-01) |
| Direct connection to measurement instruments | **llmesh sensor bridge** (FR-19, MQTT/OPC-UA) |
| Edge inference (low-spec) | **Deterministic layers such as MATH-08** (no LLM calls) |
| Privacy (family conversations, medical information) | **Local-only ledger** + zero cloud transmission |
| Constraints of boot time and communication latency | **Brief API overhead < 1%** (measured) |

A domain that **can absolutely never be reproduced** by cloud LLMs (GPT / Claude / Gemini / Perplexity).
This is llive's **invariant axis of differentiation**.

## The mental model of "gap complementation"

```
        ┌─────────────────────────────────┐
        │  Qwen (汎用言語能力)              │
        │  ├ 言語流暢性 ★★★★★              │
        │  ├ 文章生成 ★★★★★               │
        │  ├ 多言語 ★★★★★                 │
        │  ├ 一般知識 ★★★★☆               │
        │  ├ 推論 ★★★★☆                  │
        │  └─ 数値計算 ★★☆☆☆ ← 隙間 ─┐  │
        └────────────────────────────┼───┘
                                     ↓
        ┌─────────────────────────────────┐
        │  llive (認知 OS + 補完層)         │
        │  ├ 数値計算 ★★★★★ (MATH-08)      │
        │  ├ 単位次元 ★★★★★ (MATH-01)      │
        │  ├ 形式検証 ★★★★★ (MATH-02)      │
        │  ├ 長期記憶 ★★★★★ (4 層メモリ)   │
        │  ├ 監査 ★★★★★ (Approval Bus)    │
        │  ├ 認知構造 ★★★★★ (CREAT/TRIZ)  │
        │  └ Local on-prem ★★★★★          │
        └─────────────────────────────────┘
```

Qwen is strong in **language ability**, while llive is strong in **its gaps (computation, memory, audit, cognitive structure, Local)**. Combining the two reaches domains unattainable by either a cloud LLM alone or ollama alone.

## Implications for evaluation benchmarks

Measuring with the **opposition framing** of "llive vs Qwen" makes Qwen's language ability and llive's deterministic layer **compete on the same axis**, which is unfair.

Instead, we should measure on the following **collaborative axes**:

- **Hybrid task score**: the **overall score** of Qwen alone vs llive (= Qwen + deterministic complement layer)
- **Niche task score**: how much llive can supplement on tasks where Qwen is weak (numerical computation / units / formal verification)
- **Local capability**: the coverage rate of tasks that can be completed without a network
- **Audit completeness**: trace coverage for outputs

These are planned for introduction next time (after Phase 4 Production), as evaluation axes even higher than the quiz bench shown in article 08.

## Conclusion

llive's strategy is a **two-layer structure**:

1. **The permanent complementary route** (Local-environment specialization + 5-gap complementation): this is **invariant value** even as OSS LLMs like Qwen / Llama / Mistral / etc. evolve
2. **The independence route as research** (the 5 stages of ORG-FX): sustaining research value over the mid-to-long term

To the concern that "you'd be better off using a widely adopted AI," we answer with the **compound value**: **"using llive = while using Qwen, you get Local + computation + audit + cognitive structure all at once."**

"If you use it standalone, Qwen alone might be enough." But **if you want to use Qwen safely and responsibly in the Local environment, llive is the shortest path** — that is the position we take.

## Related ORG-FX requirements (reinterpreted from the complementary viewpoint)

| ORG-FX FR | Interpretation in the complementary strategy |
|---|---|
| ORG-06 Provenance-aware tokens | Attach llive's trust score to Qwen's tokens |
| ORG-02 Memory-coupled inference | Directly reference llive memory during Qwen inference |
| ORG-07 Approval-native decoding | Filter Qwen output with llive's Approval policy |
| ORG-08 llive-specialized distillation | A Qwen-shaped, llive-aware compact model |

In other words, **the ORG-* requirements can be used not only for "separation from Qwen" but also for "fusion with Qwen."** Which direction to proceed in is re-evaluated at each Stage.

## Sources

- Requirements: `llive/.planning/REQUIREMENTS.md` v2.0-core ORG-FX (reinterpreted from the complementary viewpoint)
- Related article: [10 — 5 stages of breaking away from Qwen dependence](./10_qwen_divergence_strategy.md)
- Related memory:
  - `feedback_llive_measurement_purity` — Local + on-prem purity rule
  - `project_llive` — llive overall (explicitly states the assumption of running in the Local environment)

## Other materials published the same day

- [01](./QIITA_%2301_brief_api_progressive.md) Brief API
- [02](./QIITA_%2302_cognitive_factors.md) 10 cognitive factors
- [03](./QIITA_%2303_math_vertical.md) Math & units
- [04-06]({{ '/articles/2026-05-17/README' | relative_url }}) 3 design previews
- [07](./QIITA_%2307_bench_results.md) fair bench
- [08](./QIITA_%2308_quiz_bench_debug_vs_release.md) quiz bench
- [09](./QIITA_%2309_llive_structure_originality.md) 8 elements of llive originality
- [10](./QIITA_%2310_qwen_divergence_strategy.md) 5 stages of breaking away from Qwen

---

> Full replacement is not the only path. llive, which fills 5 gaps in the Local environment, does not lose its value even as Qwen evolves.

---

# 中文

# 与 Qwen 相互补充的 llive — 在 Local 环境中填补"缝隙"的设计

作者：古濑 和文（Puruyan）

## TL;DR

- 上一篇文章 [10](./QIITA_%2310_qwen_divergence_strategy.md) 提出了"脱离 Qwen 的 5 个阶段"，但**完全脱离并非唯一的 path**。
- 用户观察（2026-05-17）："以相互补充的关系为目标也可以。llive 本来就是设想在 Local 环境中运行的东西。如果能很好地填补缝隙就好了。"
- 将 llive 的差异化轴**从「替换 Qwen」重新定位为「与 Qwen 相互补充」**。
- 一种让 llive 在 Local 环境特有的 5 个缝隙领域（计算 / 记忆 / 审计 / 认知结构 / 离线）中补充 Qwen 的设计。

## 「脱离」vs「相互补充」的二选一可以兼得

事实上，上一篇文章 10 的 Stage A（短期，约 3 个月内）本身就是**相互补充策略**：

- LLM 核心被冻结（直接使用 Qwen）
- 最大化外围差异化（CABT / MATH / CREAT）
- 「Qwen 不擅长 → llive 以确定性方式补充」

不过 Stage B 至 E（中长期）走的是"独立化路线"。两者**可以同时并行**：

![补充路线与独立化路线的双层结构图](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q11/two_routes_zh.svg)

将"在 Local 环境中填补缝隙"作为**常设定位**，并在其之上叠加"作为研究路线的独立化"的双层结构。

## llive 补充 Qwen 的 5 个「缝隙」

### 缝隙 1：数值计算、符号操作、形式验证

| Qwen 的弱点 | llive 的补充 |
|---|---|
| 把 `(2.5 * 7.8) / 0.3` 算错 | **MATH-08 SafeCalculator**（AST + 确定性） |
| `5 m/s + 3 s = 8`（量纲错误） | **MATH-01 SI 量纲分析** |
| `(x+1)² = x² + 2x`（符号幻觉） | **MATH-02 Sympy 验算 + EVO-04 Z3** |
| 捏造 CODATA 值 | **MATH-05 物理常数词典**（grounded） |

LLM 擅长输出"语言上合理的式子"，但不擅长"数学上正确的式子"。
llive 作为确定性的 sidecar 进行补充。

### 缝隙 2：长期记忆、经验回放

| Qwen 的弱点 | llive 的补充 |
|---|---|
| context window（32K-128K）的限制 | **4 层记忆**（semantic / episodic / structural / parameter） |
| 无法跨 session 记忆 | **persistent memory** + provenance |
| 重复同样的错误 | **Failed Reservoir**（EVO-06）+ Reverse-Evo Monitor（EVO-07） |
| 忘记"自己之前说过什么" | **append-only ledger**（BriefLedger / SqliteLedger） |

LLM 是 stateless 的。llive 作为 memory layer 进行补充。

### 缝隙 3：行为审计、责任归属

| Qwen 的弱点 | llive 的补充 |
|---|---|
| 没有针对危险操作的 architectural gate | **Approval Bus** + Policy + SQLite Ledger（C-1） |
| 难以追踪输出责任 | **Provenance chain** + SHA-256 audit chain（SEC-03） |
| 没有对 dangerous tokens（rm -rf 等）的过滤 | **GovernanceScorer**（COG-02，4 轴 scoring） |
| 审计日志是临时性的 | **persistent JSONL + replay** 可行 |

仅凭 LLM 单体难以应对合规。llive 提供审计基础设施。

### 缝隙 4：认知结构、多视角、矛盾消解

| Qwen 的弱点 | llive 的补充 |
|---|---|
| 视野狭窄（被最初的候选项牵着走） | **CREAT-01 KJ 法节点**（强制发散 ≥20 项） |
| 思考肤浅（单层展开） | **CREAT-02 MindMap**（DFS depth=3） |
| 偏颇的乐观 | **CREAT-04 Six Hats**（强制 cautious 视角） |
| 依赖既有模式 | **CREAT-05 Synectics**（异领域类比） |
| 无法处理矛盾 | **TRIZ 40 原理**（FR-23～27） |

用 llive 的认知结构来补充 LLM 的"思考肤浅"。

### 缝隙 5：Local 环境特有的约束

这与 llive 的**设计理念完全一致**：

| Local 环境的特性 | llive 的对应 |
|---|---|
| 没有网络 | **完全 on-prem 运行**（Ollama / LM Studio / vLLM） |
| 个人数据不能外传 | **provenance + Quarantined Zone**（SEC-01） |
| 与计测仪器直接连接 | **llmesh sensor bridge**（FR-19，MQTT/OPC-UA） |
| 边缘推理（低规格） | **MATH-08 等确定性层**（不调用 LLM） |
| 隐私（家庭对话、医疗信息） | **Local-only ledger** + 云端传输为零 |
| 启动时间、通信延迟的约束 | **Brief API 的 overhead < 1 %**（已实测） |

这是 cloud LLM（GPT / Claude / Gemini / Perplexity）**绝对无法再现的领域**。
这是 llive **不变的差异化轴**。

## 「缝隙补充」的心智模型

```
        ┌─────────────────────────────────┐
        │  Qwen (汎用言語能力)              │
        │  ├ 言語流暢性 ★★★★★              │
        │  ├ 文章生成 ★★★★★               │
        │  ├ 多言語 ★★★★★                 │
        │  ├ 一般知識 ★★★★☆               │
        │  ├ 推論 ★★★★☆                  │
        │  └─ 数値計算 ★★☆☆☆ ← 隙間 ─┐  │
        └────────────────────────────┼───┘
                                     ↓
        ┌─────────────────────────────────┐
        │  llive (認知 OS + 補完層)         │
        │  ├ 数値計算 ★★★★★ (MATH-08)      │
        │  ├ 単位次元 ★★★★★ (MATH-01)      │
        │  ├ 形式検証 ★★★★★ (MATH-02)      │
        │  ├ 長期記憶 ★★★★★ (4 層メモリ)   │
        │  ├ 監査 ★★★★★ (Approval Bus)    │
        │  ├ 認知構造 ★★★★★ (CREAT/TRIZ)  │
        │  └ Local on-prem ★★★★★          │
        └─────────────────────────────────┘
```

Qwen 在**语言能力**上强，而 llive 在**其缝隙（计算、记忆、审计、认知结构、Local）**上强。将两者结合，便能触及单凭 cloud LLM 或单凭 ollama 都无法到达的领域。

## 对评估基准的启示

以"llive vs Qwen"的**对立构图**来衡量，会让 Qwen 的语言能力与 llive 的确定性层**在同一 axis 上竞争**，这并不公平。

取而代之，应在以下**协作 axis** 上衡量：

- **Hybrid task score**：仅 Qwen vs llive（= Qwen + 确定性补充层）的**综合得分**
- **Niche task score**：在 Qwen 不擅长的任务（数值计算 / 单位 / 形式验证）上 llive 能补充多少
- **Local capability**：无网络即可完成的 task 的覆盖率
- **Audit completeness**：对输出的 trace coverage

这些计划在下次（Phase 4 Production 之后）引入，作为比文章 08 中所示 quiz bench 更上位的评估轴。

## 结论

llive 的战略是**双层结构**：

1. **常设的补充路线**（Local 环境特化 + 5 缝隙补充）：即使 Qwen / Llama / Mistral / 等 OSS LLM 进化，这也是**不变的价值**
2. **作为研究的独立化路线**（ORG-FX 5 个阶段）：在中长期持续保有研究价值

对于"用普及的 AI 更划算"的担忧，我们以**复合价值**来回答：**「使用 llive = 在使用 Qwen 的同时，能一并获得 Local + 计算 + 审计 + 认知结构」**。

"如果单独使用，或许 Qwen 就足够了。"但**「若要在 Local 环境中安全且负责任地使用 Qwen，llive 就是最短路径」**——我们采取这一定位。

## 相关 ORG-FX 要求（补充视角的再解释）

| ORG-FX FR | 在补充策略中的解释 |
|---|---|
| ORG-06 Provenance-aware tokens | 为 Qwen 的 token 附加 llive 的 trust score |
| ORG-02 Memory-coupled inference | 在 Qwen 推理时直接参照 llive memory |
| ORG-07 Approval-native decoding | 用 llive Approval policy 过滤 Qwen 输出 |
| ORG-08 llive-specialized distillation | Qwen-shaped、llive-aware 的小型 model |

也就是说，**ORG-* 要求不仅可用于「与 Qwen 分离」，也可用于「与 Qwen 融合」**。朝哪个方向前进，在各 Stage 重新评估。

## 来源

- 要求：`llive/.planning/REQUIREMENTS.md` v2.0-core ORG-FX（补充视角的再解释）
- 相关文章：[10 — 脱离 Qwen 依赖的 5 个阶段](./10_qwen_divergence_strategy.md)
- 相关 memory：
  - `feedback_llive_measurement_purity` — Local + on-prem 纯度规则
  - `project_llive` — llive 整体（明确记载了设想在 Local 环境中运行）

## 同日发布的其他资料

- [01](./QIITA_%2301_brief_api_progressive.md) Brief API
- [02](./QIITA_%2302_cognitive_factors.md) 10 思考因子
- [03](./QIITA_%2303_math_vertical.md) 数学・单位
- [04-06]({{ '/articles/2026-05-17/README' | relative_url }}) 设计预告 3 篇
- [07](./QIITA_%2307_bench_results.md) fair bench
- [08](./QIITA_%2308_quiz_bench_debug_vs_release.md) quiz bench
- [09](./QIITA_%2309_llive_structure_originality.md) llive 独自性 8 要素
- [10](./QIITA_%2310_qwen_divergence_strategy.md) 脱离 Qwen 的 5 个阶段

---

> 完全替换并非唯一的 path。在 Local 环境中补充 5 个缝隙的 llive，即使 Qwen 进化也不会贬值。

---

# 한국어

# Qwen 과 상호 보완하는 llive — Local 환경에서 '틈새'를 메우는 설계

저자: 후루세 가즈후미（Puruyan）

## TL;DR

- 이전 글 [10](./QIITA_%2310_qwen_divergence_strategy.md) 에서 "Qwen 으로부터 이탈하는 5 단계"를 제시했지만, **완전 이탈만이 path 는 아니다**.
- 사용자 관찰 (2026-05-17): "상호 보완 관계를 목표로 하는 것도 괜찮다. 원래 llive 는 Local 환경에서 동작시킬 것을 상정한 것. 틈새를 잘 보간할 수 있으면 좋겠다."
- llive 의 차별화 축을 **「Qwen 을 대체」에서 「Qwen 과 상호 보완」으로** 재구성한다.
- Local 환경 특유의 틈새 5 영역 (계산 / 기억 / 감사 / 인지 구조 / 오프라인) 에서 llive 가 Qwen 을 보완하는 설계.

## 「이탈」vs「상호 보완」의 양자택일은 양립한다

실은 이전 글 10 의 Stage A (단기, ~3 개월) 는 **상호 보완 전략** 그 자체다:

- LLM 코어는 동결 (Qwen 을 그대로 사용)
- 주변 차별화를 최대화 (CABT / MATH / CREAT)
- 「Qwen 이 약함 → llive 가 결정론적으로 보완」

다만 Stage B~E (중장기) 는 "독자화 노선". 양자는 **동시 병행** 이 가능하며:

![보완 노선과 독자화 노선의 이층 구조도](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q11/two_routes_ko.svg)

「Local 환경에서 틈새 보완」을 **상설 포지션** 으로 삼고, 그 위에 "연구 노선으로서의 독자화"를 쌓는 이층 구조.

## llive 가 Qwen 을 보완하는 5 가지 「틈새」

### 틈새 1: 수치 계산・기호 조작・형식 검증

| Qwen 의 약점 | llive 의 보완 |
|---|---|
| `(2.5 * 7.8) / 0.3` 을 틀린다 | **MATH-08 SafeCalculator** (AST + 결정론) |
| `5 m/s + 3 s = 8` (차원 오류) | **MATH-01 SI 차원 해석** |
| `(x+1)² = x² + 2x` (기호 환각) | **MATH-02 Sympy 검산 + EVO-04 Z3** |
| CODATA 값의 날조 | **MATH-05 물리 상수 사전** (grounded) |

LLM 은 "언어적으로 타당한 식"을 내는 것은 잘하지만 "수학적으로 올바른 식"은 못한다.
llive 가 결정론적 사이드카로서 보완한다.

### 틈새 2: 장기 기억・경험 재생

| Qwen 의 약점 | llive 의 보완 |
|---|---|
| context window (32K-128K) 의 한계 | **4 층 메모리** (semantic / episodic / structural / parameter) |
| session 을 넘는 기억 불가 | **persistent memory** + provenance |
| 같은 실수를 반복 | **Failed Reservoir** (EVO-06) + Reverse-Evo Monitor (EVO-07) |
| 「자신이 이전에 무엇을 말했는지」 잊는다 | **append-only ledger** (BriefLedger / SqliteLedger) |

LLM 은 stateless. llive 가 memory layer 로서 보완한다.

### 틈새 3: 행동 감사・책임 소재

| Qwen 의 약점 | llive 의 보완 |
|---|---|
| 위험한 동작의 architectural gate 없음 | **Approval Bus** + Policy + SQLite Ledger (C-1) |
| 출력 책임의 추적 곤란 | **Provenance chain** + SHA-256 audit chain (SEC-03) |
| dangerous tokens (rm -rf 등) 의 필터 없음 | **GovernanceScorer** (COG-02, 4 축 scoring) |
| 감사 로그가 휘발성 | **persistent JSONL + replay** 가능 |

LLM 단체로는 컴플라이언스 대응이 곤란. llive 가 감사 기반을 제공한다.

### 틈새 4: 인지 구조・다시점・모순 해결

| Qwen 의 약점 | llive 의 보완 |
|---|---|
| 시야 협착 (최초 후보에 끌려간다) | **CREAT-01 KJ 법 노드** (확산 ≥20 건 강제) |
| 사고의 얕음 (1 계층 전개) | **CREAT-02 MindMap** (DFS depth=3) |
| 편향된 낙관 | **CREAT-04 Six Hats** (cautious 관점 강제) |
| 기존 패턴 의존 | **CREAT-05 Synectics** (이분야 유추) |
| 모순을 다룰 수 없음 | **TRIZ 40 원리** (FR-23~27) |

LLM 의 "사고의 얕음"을 llive 의 인지 구조로 보완한다.

### 틈새 5: Local 환경 특유의 제약

이것은 llive 의 **설계 콘셉트와 완전히 일치**:

| Local 환경의 특성 | llive 의 대응 |
|---|---|
| 네트워크 부재 | **완전 on-prem 동작** (Ollama / LM Studio / vLLM) |
| 개인 데이터를 밖으로 내보낼 수 없음 | **provenance + Quarantined Zone** (SEC-01) |
| 계측 기기와의 직접 접속 | **llmesh sensor bridge** (FR-19, MQTT/OPC-UA) |
| 엣지 추론 (저사양) | **MATH-08 등의 결정론적 층** (LLM 을 호출하지 않음) |
| 프라이버시 (가족의 대화, 의료 정보) | **Local-only ledger** + 클라우드 전송 제로 |
| 기동 시간・통신 지연의 제약 | **Brief API 의 overhead < 1 %** (실측 완료) |

cloud LLM (GPT / Claude / Gemini / Perplexity) 에서는 **절대로 재현할 수 없는 영역**.
이것이 llive 의 **불변의 차별화 축**.

## 「틈새 보완」의 멘탈 모델

```
        ┌─────────────────────────────────┐
        │  Qwen (汎用言語能力)              │
        │  ├ 言語流暢性 ★★★★★              │
        │  ├ 文章生成 ★★★★★               │
        │  ├ 多言語 ★★★★★                 │
        │  ├ 一般知識 ★★★★☆               │
        │  ├ 推論 ★★★★☆                  │
        │  └─ 数値計算 ★★☆☆☆ ← 隙間 ─┐  │
        └────────────────────────────┼───┘
                                     ↓
        ┌─────────────────────────────────┐
        │  llive (認知 OS + 補完層)         │
        │  ├ 数値計算 ★★★★★ (MATH-08)      │
        │  ├ 単位次元 ★★★★★ (MATH-01)      │
        │  ├ 形式検証 ★★★★★ (MATH-02)      │
        │  ├ 長期記憶 ★★★★★ (4 層メモリ)   │
        │  ├ 監査 ★★★★★ (Approval Bus)    │
        │  ├ 認知構造 ★★★★★ (CREAT/TRIZ)  │
        │  └ Local on-prem ★★★★★          │
        └─────────────────────────────────┘
```

Qwen 은 **언어 능력** 에서 강하고, llive 는 **그 틈새 (계산・기억・감사・인지 구조・Local)** 에서 강하다. 양자를 조합하면, cloud LLM 단독으로도, ollama 단독으로도 도달할 수 없는 영역에 닿는다.

## 평가 벤치에 대한 시사

「llive vs Qwen」의 **대립 구도** 로 측정하면, Qwen 의 언어 능력 × llive 의 결정론적 층이 **같은 axis 에서 경합** 하게 되어 불공평하다.

대신 다음의 **협조 axis** 로 측정해야 한다:

- **Hybrid task score**: Qwen 만 vs llive (= Qwen + 결정론적 보완층) 의 **종합 스코어**
- **Niche task score**: Qwen 이 약한 태스크 (수치 계산 / 단위 / 형식 검증) 에서 llive 가 얼마나 보완할 수 있는가
- **Local capability**: 네트워크 없이 완결되는 task 의 망라율
- **Audit completeness**: 출력에 대한 trace coverage

이것들은 글 08 에서 보인 quiz bench 의 더 상위 평가 축으로서, 다음번 (Phase 4 Production 이후) 에 도입 예정.

## 결론

llive 의 전략은 **이층 구조**:

1. **상설 보완 노선** (Local 환경 특화 + 5 틈새 보완): 이것은 Qwen / Llama / Mistral / 등의 OSS LLM 이 진화해도 **불변의 가치**
2. **연구로서의 독자화 노선** (ORG-FX 5 단계): 중장기적으로 연구 가치를 지속

"보급되어 있는 AI 를 쓰는 편이 낫다"는 우려에 대해서는, **「llive 를 쓴다 = Qwen 을 쓰는 데 있어서 Local + 계산 + 감사 + 인지 구조 를 전부 얻을 수 있다」** 라는 **복합 가치** 로 답한다.

"단독으로 쓴다면 Qwen 으로 충분"할지도 모른다. 그러나 **「Qwen 을 Local 환경에서 안전하게 책임을 가지고 쓴다면 llive 가 최단 경로」**, 라는 포지션을 취한다.

## 관련 ORG-FX 요구사항 (보완 시점의 재해석)

| ORG-FX FR | 보완 전략에서의 해석 |
|---|---|
| ORG-06 Provenance-aware tokens | Qwen 의 token 에 llive 의 trust score 를 부여 |
| ORG-02 Memory-coupled inference | Qwen 추론 시 llive memory 를 직접 참조 |
| ORG-07 Approval-native decoding | Qwen 출력을 llive Approval policy 로 filter |
| ORG-08 llive-specialized distillation | Qwen-shaped, llive-aware 한 소형 model |

즉 **ORG-* 요구사항은 「Qwen 과의 분리」뿐만 아니라 「Qwen 과의 유착」에도 쓸 수 있다**. 어느 방향으로 나아갈지는 각 Stage 에서 재평가한다.

## 소스

- 요구사항: `llive/.planning/REQUIREMENTS.md` v2.0-core ORG-FX (보완 시점의 재해석)
- 관련 글: [10 — Qwen 의존으로부터 이탈하는 5 단계](./10_qwen_divergence_strategy.md)
- 관련 memory:
  - `feedback_llive_measurement_purity` — Local + on-prem 순도 규칙
  - `project_llive` — llive 전체 (Local 환경에서 동작시킬 것을 상정함이 명기됨)

## 같은 날의 다른 공개 자료

- [01](./QIITA_%2301_brief_api_progressive.md) Brief API
- [02](./QIITA_%2302_cognitive_factors.md) 10 사고 인자
- [03](./QIITA_%2303_math_vertical.md) 수학・단위
- [04-06]({{ '/articles/2026-05-17/README' | relative_url }}) 설계 예고 3 편
- [07](./QIITA_%2307_bench_results.md) fair bench
- [08](./QIITA_%2308_quiz_bench_debug_vs_release.md) quiz bench
- [09](./QIITA_%2309_llive_structure_originality.md) llive 독자성 8 요소
- [10](./QIITA_%2310_qwen_divergence_strategy.md) Qwen 이탈 5 단계

---

> 완전 대체만이 path 는 아니다. Local 환경에서 5 틈새를 보완하는 llive 는, Qwen 이 진화해도 가치가 떨어지지 않는다.
