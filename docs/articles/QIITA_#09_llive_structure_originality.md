---
layout: default
title: "llive の構造は LLM として独自になっているか — 8 つの差別化要素の点検"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags: [llm, architecture, originality, cognitive-os, llive]
id: 0c1d5ebd6b0656ba74e1
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# llive の構造は LLM として独自になっているか — 8 つの差別化要素の点検

著者: 古瀬 和文（ぷるやん）

> 📚 **連載ナビ**: ← #08 [Quiz bench Debug vs Release 比較](./QIITA_%2308_quiz_bench_debug_vs_release.md) ｜ **#09 本記事**（構造の独自性を点検する）｜ #10 [Qwen 依存から離脱する 5 段階ロードマップ](./QIITA_%2310_qwen_divergence_strategy.md) →。※ 各記事は単独でも読めます。
>
> #07/#08 では「llive を速度でベンチして良いのか」を測定の側から見た。本記事では問いを構造の側へ移す——llive は LLM として、何か独自の形になりつつあるのか。ユーザーから来た 1 つの問いを起点に、8 つの差別化要素を 1 つずつ点検していく。

## TL;DR

ユーザーからの問い：「llive の構造って、LLM として独自の構造になっていってますか？」

答え: **llive は LLM そのものではなく、LLM の周りに被せる「認知 OS」として独自**。Decoder-only LLM (Qwen / Llama / Mistral / 等) を frozen な計算コアとして使い、その上に 8 つの構造要素を積層することで、既存類似研究 (MemGPT / LongMem / AutoML-Zero / Self-Refine / Reflexion / MERA / AutoGPT 系) のいずれとも一致しない設計に到達している。

## 8 つの差別化要素

### 1. Decoder-only LLM コアは凍結 + 周辺で能力拡張

| 既存 | llive |
|---|---|
| 全量 fine-tune / LoRA / adapter | LLM 重みは **現状 (Phase 1〜v0.6) では更新しない** |
| 学習 = モデル更新 | 学習 = **外部記憶への書き込み** + **構造変更** |

これは LoRA / adapter の延長線にあるが、「重みを更新しないことで replay 可能 / monitorable な学習軌跡」を最優先にしている点が独自。CABT (S2 で計画中) では forward hook で attention に bias を加えるが、これも重み凍結のまま。

### 2. 4 層メモリの責務分離 (特に parameter memory が独自)

| 層 | 役割 | 既存研究の対応 |
|---|---|---|
| semantic | 知識 (事実) | RAG、ベクトル DB、kNN-LM |
| episodic | 経験 (時系列) | MemGPT / Memorizing Transformers |
| **structural** | **関係 (graph / dependency)** | **少例 (Knowledge Graph 系)** |
| **parameter** | **重みの差分** | **llive 独自寄り** |

特に **parameter memory** は「LoRA adapter / sub-block の集合を memory として扱い、surprise gate で write 制御する」発想。Adapter Store + Bayesian Surprise + 進化レポジトリ という組合せは類似がない。

### 3. 6 stage FullSense Loop の擬人化された認知段階

```
Salience Gate ──→ Curiosity Drive ──→ Inner Monologue ──→
Ego/Altruism Scorer ──→ Action Plan ──→ Output Bus (Sandbox / Production)
```

各段階に **数式 + 心理学的根拠** を持たせている設計:

- Salience: 入力の surprise score でフィルタ
- Curiosity: 既知 corpus との novelty で点数化
- Inner Monologue: 鏡映認知 (mirror-thought)、TRIZ 原理検出を内蔵
- Ego/Altruism: 動機の二軸でアクションを再採点
- Action Plan: PROPOSE / INTERVENE / NOTE / SILENT の 4 択
- Output Bus: Sandbox (副作用なし) と Production (Approval 経由) を物理分離

これは既存の "agent loop" (ReAct / ToT / Reflexion) より **心理的妥当性を重視した 6 段モデル**。

### 4. Multi-track Filter Architecture A-1.5 (EpistemicType による track 切替)

`EpistemicType` 列挙 (FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC / RESERVED_1〜5) に応じて filter chain を切り替える。

例:
- 数学質問 → MATHEMATICAL track (FACTUAL strict)
- 倫理的判断 → NORMATIVE track (§F5 ethical 優先)
- 歴史認識 → INTERPRETIVE track (perspective-dependent)

「結論不変な FACTUAL と perspective-dependent な INTERPRETIVE を crude に混ぜない」設計。これは LLM 単体には存在しない。

### 5. Approval Bus を Loop 内に組み込み (HITL を architecture level に)

PROPOSE / INTERVENE 決定は必ず Approval Bus を経由。policy で auto-approve/deny、残りは llove TUI で人手 review。すべて SQLite ledger に永続化。

既存類似:
- Codex CLI の `suggest / auto-edit / full-auto` モード
- Gemini CLI の approval prompt

しかし、**Bus 経由で全 PROPOSE/INTERVENE が SQLite に永続化 + replay 可** な実装は llive 独自。これは COG-FX 整合因子 (COG-02) の核心。

### 6. TRIZ 40 原理を mutation policy として内蔵

FR-23〜27 で実装:
- Contradiction Detector (メトリクスから矛盾自動検出)
- Principle Mapper (39×39 マトリクス内蔵)
- RAD-Backed Idea Generator (TRIZ × RAD コーパス → CandidateDiff 生成)
- 9-Window System Operator (時間軸 × 階層軸)
- ARIZ Pipeline (9 ステップを mutation 自動化)

これは Self-Refine / Reflexion の「自己批評」と異なり、**創造の代替案生成エンジン**として TRIZ を内蔵。Synectics (CREAT-05 計画) と組合せて cross-domain analogical reasoning も。

### 7. Cognitive Factor Framework (CFF) ― 認知設計を明示的に分解

「心理の深層」由来の 10 因子 (構造化・再構成・閉ループ・自己拡張・不確実性・探索・整合・来歴・多視点・現実接続) を **役割別 policy に分解**:

- planner policy / memory policy / critic policy / evolution policy / trace policy

これにより個別 A/B 比較・改善・evolve が可能。COG-01/02/03 (本日実装) で確認: BriefResult に (confidence, assumptions, missing_evidence) の Triple Output + Governance Scoring (4 軸) + Trace Graph (3 chain)。

既存 LLM ライブラリ (LangChain / LlamaIndex / AutoGen / CrewAI) には policy 分解の発想はあるが、**認知因子を明示的にマップした architecture** は llive のみ。

### 8. Brief API ― 構造化 work unit という primitives

外部クライアント (lldesign / lltrade / 計画中の llcad / lleda / llchip) が work unit を渡せる API:

```python
Brief(
    brief_id="webpage-portal-refresh",
    goal="...",
    constraints=("no inline HTML inside fenced ```mermaid``` blocks",),
    success_criteria=("rendered HTML contains SVG",),
    tools=("read_file", "write_file"),
    approval_required=True,
    epistemic_type=EpistemicType.PRAGMATIC,
)
```

これは LangChain の `Chain` や CrewAI の `Task` と類似だが:

- **frozen dataclass** (immutable, replay-friendly)
- **append-only JSONL ledger** に全段階を固定記録
- **Approval Bus + Governance Scorer** を built-in
- **Grounder (TRIZ × RAD × SafeCalculator)** を前段に持つ

これらの組合せは類似がない。

## 構造として「独自」と言える理由

8 要素の各々は既存研究のどこかに対応物がある。しかし **8 要素の組合せ + 役割分離 + 心理因子マッピング** は llive 固有。

```
LLM (Qwen/Llama/...) を凍結コアとして使い
  + 4 層メモリで知識/経験/関係/重みを分離保持
  + 6 stage Loop で擬人化された認知段階
  + Multi-track Filter で epistemic_type 別 chain
  + Approval Bus で HITL を architecture level に
  + TRIZ 40 原理 + RAD 49 分野で代替案生成
  + 10 思考因子で policy を分解
  + Brief API で外部入力を構造化
```

この **積層構造** は、LangChain (chain) / AutoGen (multi-agent) / MemGPT (memory) / Self-Refine (critique) / AutoML-Zero (search) のいずれかに偏ることなく、**認知 OS** として横断する。

## 「LLM 自体は何か変えているか」への答え

**Phase 1〜v0.6 では LLM 重みは触らない** (frozen)。これは設計判断:
- replay 可能性を最優先
- 学習軌跡を monitorable に保つ
- LLM 提供元 (Qwen, Meta, Mistral) の更新を直接取り込める

ただし **Phase 8 (CABT) で forward hook による attention bias 注入** を計画。これも **重み更新ではない** が、推論時に metadata bias を加えるという「LLM の挙動を変える」レイヤー。完全な独自 LLM 構築 (LoRA training / distillation) は Phase 10+ の話で、現状の "独自性" は **LLM の周りに被せる cognitive OS** にある。

## 既存類似研究との位置づけ (再掲)

| 既存系 | 重なる範囲 | llive の差別化 |
|---|---|---|
| MemGPT / LongMem | 階層メモリ | 4 層分離 + phase transition + 署名 zone |
| AutoML-Zero / NAS-LLM | 構造探索 | 形式検証 gate + multi-precision shadow + 失敗データ化 |
| Self-Refine / Reflexion | 自己批評 | online/offline 分離 + llove TUI HITL staging |
| MERA / ModularLLM | モジュラー化 | 可変長 BlockContainer YAML + plugin registry |
| AutoGPT 系 | エージェント | llmesh 産業 IoT 直結 + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | 10 因子明示分解 + 認知 OS positioning |

## まとめ

「llive は LLM か」 → No、**llive は LLM を内蔵する認知 OS**。

「llive の構造は独自か」 → Yes、**8 要素の組合せ × 役割分離 × 心理因子マッピング** が独自。

「ベンチで速度比較すべきか」 → No、**速度ではなく構造を比較**すべき。llive の付加価値は ledger / approval / governance / grounding / 6 stage trace にあり、これは ollama 直叩きや LangChain chain では再現できない。

## 残った問い — 「周辺だけ」で独自と言い切れるのか

ここまでの結論は「独自性は **LLM の周りに被せる cognitive OS** にある」だった。だが、これには痛いところを突く反論がありうる——コアが Qwen / Llama / Mistral のままなら、それは「他人の脳に自前の前頭葉を継ぎ足しただけ」ではないのか? 周辺をどれだけ精緻にしても、思考の根っこを借り物に依存している限り、研究としての独自性は本当に主張できるのか。

これは筆者自身がユーザーから受けた問いでもある。次回 **#10「[Qwen 依存から離脱する 5 段階ロードマップ](./QIITA_%2310_qwen_divergence_strategy.md)」** では、その借り物のコアを段階的に自前へ移していく道筋を扱う——周辺で証明した独自性を、どうやってコアそのものへ降ろしていくのか。本記事で「現状 (Phase 1〜v0.6) は重みを更新しない」と書いた一線を、いつ、どこまで踏み越えるのかを確かめにいく。

## ソース

- 設計: `llive/.planning/REQUIREMENTS.md` (要件 92 件、内 v1.0-frame COG-FX 4 件で因子マッピング)
- 実装: `llive/src/llive/` (brief / fullsense / approval / triz / memory / evolution / cabt 計画)
- 比較ベンチ: 同日記事 [01](./QIITA_%2301_brief_api_progressive.md) / [07](./QIITA_%2307_bench_results.md) / [08](./QIITA_%2308_quiz_bench_debug_vs_release.md)

---

> llive は LLM ではなく、LLM の周りに被せる認知 OS。8 要素の組合せが独自性を構成する。

---

# English

# Is llive's Structure Becoming Original as an LLM? — A Review of 8 Differentiating Elements

Author: Kazufumi Furuse (Puruyan)

> 📚 **Series nav**: ← #08 [Quiz bench Debug vs Release comparison](./QIITA_%2308_quiz_bench_debug_vs_release.md) ｜ **#09 This article** (reviewing the originality of the structure) ｜ #10 [A 5-stage roadmap to break free from Qwen dependence](./QIITA_%2310_qwen_divergence_strategy.md) →. ※ Each article stands on its own.
>
> In #07/#08 we looked, from the measurement side, at whether it even makes sense to benchmark llive on speed. In this article we move the question to the structural side — is llive becoming something original *as an LLM*? Starting from a single question raised by the user, we review the 8 differentiating elements one by one.

## TL;DR

A question from the user: "Is llive's structure becoming an original structure as an LLM?"

Answer: **llive is not an LLM itself, but is original as a "cognitive OS" layered around an LLM**. It uses a decoder-only LLM (Qwen / Llama / Mistral / etc.) as a frozen computational core, and by stacking 8 structural elements on top of it, it reaches a design that matches none of the existing related works (MemGPT / LongMem / AutoML-Zero / Self-Refine / Reflexion / MERA / the AutoGPT family).

## The 8 Differentiating Elements

### 1. The Decoder-only LLM Core is Frozen + Capability is Extended in the Periphery

| Existing | llive |
|---|---|
| Full fine-tune / LoRA / adapter | LLM weights are **not updated for now (Phase 1 through v0.6)** |
| Learning = model update | Learning = **writing to external memory** + **structural change** |

This is an extension of the LoRA / adapter line, but what is original is that it prioritizes "a replayable / monitorable learning trajectory through not updating weights." In CABT (planned in S2), a forward hook adds a bias to attention, but this too keeps the weights frozen.

### 2. Responsibility Separation Across 4 Memory Layers (parameter memory in particular is original)

| Layer | Role | Corresponding existing research |
|---|---|---|
| semantic | Knowledge (facts) | RAG, vector DB, kNN-LM |
| episodic | Experience (time series) | MemGPT / Memorizing Transformers |
| **structural** | **Relations (graph / dependency)** | **Few examples (Knowledge Graph family)** |
| **parameter** | **Weight deltas** | **Largely original to llive** |

In particular, **parameter memory** is the idea of "treating a collection of LoRA adapters / sub-blocks as memory, and controlling writes via a surprise gate." The combination of Adapter Store + Bayesian Surprise + evolutionary repository has no analog.

### 3. The 6-stage FullSense Loop with Anthropomorphized Cognitive Stages

```
Salience Gate ──→ Curiosity Drive ──→ Inner Monologue ──→
Ego/Altruism Scorer ──→ Action Plan ──→ Output Bus (Sandbox / Production)
```

A design that gives each stage **a formula + a psychological basis**:

- Salience: filters by the surprise score of the input
- Curiosity: scores by novelty against a known corpus
- Inner Monologue: built-in mirror-thought (reflective cognition) and TRIZ principle detection
- Ego/Altruism: re-scores actions along two axes of motivation
- Action Plan: a 4-way choice of PROPOSE / INTERVENE / NOTE / SILENT
- Output Bus: physically separates Sandbox (no side effects) and Production (via Approval)

This is **a 6-stage model that emphasizes psychological plausibility** more than existing "agent loops" (ReAct / ToT / Reflexion).

### 4. Multi-track Filter Architecture A-1.5 (track switching by EpistemicType)

The filter chain is switched according to the `EpistemicType` enumeration (FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC / RESERVED_1–5).

Examples:
- Mathematical question → MATHEMATICAL track (FACTUAL strict)
- Ethical judgment → NORMATIVE track (§F5 ethical priority)
- Historical understanding → INTERPRETIVE track (perspective-dependent)

A design that "does not crudely mix conclusion-invariant FACTUAL with perspective-dependent INTERPRETIVE." This does not exist in an LLM on its own.

### 5. The Approval Bus Built into the Loop (HITL at the architecture level)

PROPOSE / INTERVENE decisions always pass through the Approval Bus. Policy handles auto-approve/deny, and the rest is reviewed by humans in the llove TUI. Everything is persisted to a SQLite ledger.

Existing analogs:
- Codex CLI's `suggest / auto-edit / full-auto` modes
- Gemini CLI's approval prompt

However, **an implementation where all PROPOSE/INTERVENE is persisted to SQLite via a Bus + is replayable** is original to llive. This is the core of the COG-FX consistency factor (COG-02).

### 6. TRIZ's 40 Principles Built in as a Mutation Policy

Implemented in FR-23–27:
- Contradiction Detector (automatically detects contradictions from metrics)
- Principle Mapper (built-in 39×39 matrix)
- RAD-Backed Idea Generator (TRIZ × RAD corpus → CandidateDiff generation)
- 9-Window System Operator (time axis × hierarchy axis)
- ARIZ Pipeline (automates the 9 steps as mutations)

Unlike the "self-critique" of Self-Refine / Reflexion, this builds in TRIZ as **an engine for generating creative alternatives**. Combined with Synectics (planned in CREAT-05) it also does cross-domain analogical reasoning.

### 7. Cognitive Factor Framework (CFF) — Decomposing Cognitive Design Explicitly

The 10 factors derived from "The Depths of Psychology" (structuring / restructuring / closed-loop / self-expansion / uncertainty / exploration / consistency / provenance / multiple perspectives / reality grounding) are **decomposed into role-based policies**:

- planner policy / memory policy / critic policy / evolution policy / trace policy

This makes individual A/B comparison, improvement, and evolution possible. Confirmed in COG-01/02/03 (implemented today): BriefResult has Triple Output of (confidence, assumptions, missing_evidence) + Governance Scoring (4 axes) + Trace Graph (3 chains).

Existing LLM libraries (LangChain / LlamaIndex / AutoGen / CrewAI) do have the idea of policy decomposition, but **an architecture that explicitly maps cognitive factors** exists only in llive.

### 8. Brief API — Structured Work Units as Primitives

An API by which external clients (lldesign / lltrade / the planned llcad / lleda / llchip) can hand over work units:

```python
Brief(
    brief_id="webpage-portal-refresh",
    goal="...",
    constraints=("no inline HTML inside fenced ```mermaid``` blocks",),
    success_criteria=("rendered HTML contains SVG",),
    tools=("read_file", "write_file"),
    approval_required=True,
    epistemic_type=EpistemicType.PRAGMATIC,
)
```

This resembles LangChain's `Chain` or CrewAI's `Task`, but:

- **frozen dataclass** (immutable, replay-friendly)
- All stages are fixed-recorded in an **append-only JSONL ledger**
- **Approval Bus + Governance Scorer** are built-in
- It has a **Grounder (TRIZ × RAD × SafeCalculator)** at the front

There is no analog to these combinations.

## Why It Can Be Called "Original" as a Structure

Each of the 8 elements has a counterpart somewhere in existing research. But the **combination of the 8 elements + role separation + psychological factor mapping** is unique to llive.

```
Use an LLM (Qwen/Llama/...) as a frozen core
  + Separately retain knowledge/experience/relations/weights in 4 memory layers
  + Anthropomorphized cognitive stages in a 6-stage Loop
  + Per-epistemic_type chains via a Multi-track Filter
  + HITL at the architecture level via the Approval Bus
  + Alternative generation via TRIZ's 40 principles + RAD's 49 domains
  + Decompose policies via the 10 thinking factors
  + Structure external input via the Brief API
```

This **layered structure** crosses over as a **cognitive OS** without leaning toward any one of LangChain (chain) / AutoGen (multi-agent) / MemGPT (memory) / Self-Refine (critique) / AutoML-Zero (search).

## The Answer to "Is the LLM Itself Being Changed in Any Way?"

**In Phase 1 through v0.6, the LLM weights are not touched** (frozen). This is a design decision:
- Prioritize replayability
- Keep the learning trajectory monitorable
- Be able to directly incorporate updates from the LLM providers (Qwen, Meta, Mistral)

However, **Phase 8 (CABT) plans to inject attention bias via a forward hook**. This too is **not a weight update**, but a layer that "changes the LLM's behavior" by adding a metadata bias at inference time. Building a fully original LLM (LoRA training / distillation) is a matter for Phase 10+; the current "originality" lies in the **cognitive OS layered around the LLM**.

## Positioning Against Existing Related Research (recap)

| Existing family | Overlapping scope | llive's differentiation |
|---|---|---|
| MemGPT / LongMem | Hierarchical memory | 4-layer separation + phase transition + signature zone |
| AutoML-Zero / NAS-LLM | Structure search | Formal verification gate + multi-precision shadow + failure-as-data |
| Self-Refine / Reflexion | Self-critique | online/offline separation + llove TUI HITL staging |
| MERA / ModularLLM | Modularization | Variable-length BlockContainer YAML + plugin registry |
| AutoGPT family | Agent | Direct connection to llmesh industrial IoT + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | Explicit decomposition of the 10 factors + cognitive OS positioning |

## Summary

"Is llive an LLM?" → No, **llive is a cognitive OS that embeds an LLM**.

"Is llive's structure original?" → Yes, **the combination of 8 elements × role separation × psychological factor mapping** is original.

"Should we benchmark its speed?" → No, **we should compare structure, not speed**. llive's added value lies in the ledger / approval / governance / grounding / 6-stage trace, and this cannot be reproduced by hitting ollama directly or by a LangChain chain.

## Sources

- Design: `llive/.planning/REQUIREMENTS.md` (92 requirements, of which 4 v1.0-frame COG-FX map the factors)
- Implementation: `llive/src/llive/` (brief / fullsense / approval / triz / memory / evolution / cabt planned)
- Comparison benchmarks: same-day articles [01](./QIITA_%2301_brief_api_progressive.md) / [07](./QIITA_%2307_bench_results.md) / [08](./QIITA_%2308_quiz_bench_debug_vs_release.md)

---

> llive is not an LLM, but a cognitive OS layered around an LLM. The combination of the 8 elements constitutes its originality.

---

# 中文

# llive 的结构作为 LLM 是否已变得独特 — 8 个差异化要素的审视

作者：古濑 和文（Puruyan）

## TL;DR

来自用户的提问：「llive 的结构，作为 LLM 是否正变得具有独特结构？」

答案：**llive 并非 LLM 本身，而是作为覆盖在 LLM 周围的「认知 OS」而独特**。它将 decoder-only LLM（Qwen / Llama / Mistral / 等）当作冻结的计算核心使用，并在其之上叠加 8 个结构要素，从而达到了一种与任何现有相似研究（MemGPT / LongMem / AutoML-Zero / Self-Refine / Reflexion / MERA / AutoGPT 系列）都不一致的设计。

## 8 个差异化要素

### 1. Decoder-only LLM 核心被冻结 + 在外围扩展能力

| 现有 | llive |
|---|---|
| 全量 fine-tune / LoRA / adapter | LLM 权重**绝对不触碰** |
| 学习 = 模型更新 | 学习 = **写入外部记忆** + **结构变更** |

这处于 LoRA / adapter 的延长线上，但其独特之处在于：通过不更新权重，把「可 replay / 可 monitorable 的学习轨迹」置于最优先。在 CABT（计划于 S2）中，通过 forward hook 给 attention 加上 bias，但这同样保持权重冻结。

### 2. 4 层记忆的职责分离（尤其 parameter memory 独特）

| 层 | 角色 | 对应的现有研究 |
|---|---|---|
| semantic | 知识（事实） | RAG、向量 DB、kNN-LM |
| episodic | 经验（时间序列） | MemGPT / Memorizing Transformers |
| **structural** | **关系（graph / dependency）** | **少量示例（Knowledge Graph 系）** |
| **parameter** | **权重的差分** | **偏向 llive 独有** |

尤其是 **parameter memory**，其构想是「把 LoRA adapter / sub-block 的集合当作 memory，并通过 surprise gate 控制写入」。Adapter Store + Bayesian Surprise + 进化仓库 这一组合没有相似先例。

### 3. 6 阶段 FullSense Loop 的拟人化认知阶段

```
Salience Gate ──→ Curiosity Drive ──→ Inner Monologue ──→
Ego/Altruism Scorer ──→ Action Plan ──→ Output Bus (Sandbox / Production)
```

为每个阶段赋予 **公式 + 心理学依据** 的设计：

- Salience：以输入的 surprise score 进行过滤
- Curiosity：以与已知 corpus 的 novelty 评分
- Inner Monologue：内置镜映认知（mirror-thought）、TRIZ 原理检测
- Ego/Altruism：以动机的二轴对动作重新评分
- Action Plan：PROPOSE / INTERVENE / NOTE / SILENT 的 4 选 1
- Output Bus：将 Sandbox（无副作用）与 Production（经 Approval）物理分离

这相比现有的 "agent loop"（ReAct / ToT / Reflexion），是 **更重视心理合理性的 6 段模型**。

### 4. Multi-track Filter Architecture A-1.5（按 EpistemicType 切换 track）

根据 `EpistemicType` 枚举（FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC / RESERVED_1〜5）切换 filter chain。

例：
- 数学问题 → MATHEMATICAL track（FACTUAL strict）
- 伦理判断 → NORMATIVE track（§F5 ethical 优先）
- 历史认识 → INTERPRETIVE track（perspective-dependent）

这是「不把结论不变的 FACTUAL 与 perspective-dependent 的 INTERPRETIVE 粗糙地混在一起」的设计。这在 LLM 单体中并不存在。

### 5. 将 Approval Bus 嵌入 Loop 之内（把 HITL 提升到 architecture level）

PROPOSE / INTERVENE 的决定必然经由 Approval Bus。由 policy 进行 auto-approve/deny，其余则在 llove TUI 中由人工 review。全部持久化到 SQLite ledger。

现有相似：
- Codex CLI 的 `suggest / auto-edit / full-auto` 模式
- Gemini CLI 的 approval prompt

然而，**经 Bus 让全部 PROPOSE/INTERVENE 持久化到 SQLite + 可 replay** 的实现是 llive 独有的。这是 COG-FX 整合因子（COG-02）的核心。

### 6. 把 TRIZ 40 原理作为 mutation policy 内置

在 FR-23〜27 中实现：
- Contradiction Detector（从指标自动检测矛盾）
- Principle Mapper（内置 39×39 矩阵）
- RAD-Backed Idea Generator（TRIZ × RAD 语料 → 生成 CandidateDiff）
- 9-Window System Operator（时间轴 × 层级轴）
- ARIZ Pipeline（把 9 个步骤自动化为 mutation）

这与 Self-Refine / Reflexion 的「自我批评」不同，而是把 TRIZ 作为 **创造的替代方案生成引擎** 内置。与 Synectics（CREAT-05 计划）结合，还能进行 cross-domain analogical reasoning。

### 7. Cognitive Factor Framework (CFF) — 把认知设计显式分解

将源自「心理的深层」的 10 个因子（结构化・再构成・闭环・自我扩展・不确定性・探索・整合・来历・多视角・现实连接）**分解为按角色划分的 policy**：

- planner policy / memory policy / critic policy / evolution policy / trace policy

由此，单独的 A/B 比较・改进・evolve 成为可能。在 COG-01/02/03（今日实现）中确认：BriefResult 具有 (confidence, assumptions, missing_evidence) 的 Triple Output + Governance Scoring（4 轴）+ Trace Graph（3 chain）。

现有 LLM 库（LangChain / LlamaIndex / AutoGen / CrewAI）虽有 policy 分解的构想，但 **显式映射认知因子的 architecture** 唯独 llive 才有。

### 8. Brief API — 作为 primitives 的结构化 work unit

一个供外部客户端（lldesign / lltrade / 计划中的 llcad / lleda / llchip）传递 work unit 的 API：

```python
Brief(
    brief_id="webpage-portal-refresh",
    goal="...",
    constraints=("no inline HTML inside fenced ```mermaid``` blocks",),
    success_criteria=("rendered HTML contains SVG",),
    tools=("read_file", "write_file"),
    approval_required=True,
    epistemic_type=EpistemicType.PRAGMATIC,
)
```

这与 LangChain 的 `Chain` 或 CrewAI 的 `Task` 相似，但：

- **frozen dataclass**（immutable, replay-friendly）
- 在 **append-only JSONL ledger** 中固定记录全部阶段
- 内置 **Approval Bus + Governance Scorer**
- 在前段持有 **Grounder (TRIZ × RAD × SafeCalculator)**

这些组合没有相似先例。

## 作为结构可称「独特」的理由

8 个要素的每一个，在现有研究的某处都有对应物。但 **8 个要素的组合 + 角色分离 + 心理因子映射** 是 llive 固有的。

```
把 LLM (Qwen/Llama/...) 当作冻结核心使用
  + 用 4 层记忆分离保持 知识/经验/关系/权重
  + 用 6 stage Loop 实现拟人化的认知阶段
  + 用 Multi-track Filter 按 epistemic_type 切换 chain
  + 用 Approval Bus 把 HITL 提升到 architecture level
  + 用 TRIZ 40 原理 + RAD 49 分野 生成替代方案
  + 用 10 思考因子分解 policy
  + 用 Brief API 把外部输入结构化
```

这种 **叠层结构**，作为 **认知 OS** 横向贯通，而不偏向 LangChain (chain) / AutoGen (multi-agent) / MemGPT (memory) / Self-Refine (critique) / AutoML-Zero (search) 中的任何一者。

## 对「LLM 本身是否改变了什么」的回答

**在 Phase 1〜v0.6 中不触碰 LLM 权重**（frozen）。这是一项设计判断：
- 把 replay 可能性置于最优先
- 把学习轨迹保持为 monitorable
- 能够直接吸纳 LLM 提供方（Qwen、Meta、Mistral）的更新

不过，**计划在 Phase 8 (CABT) 通过 forward hook 注入 attention bias**。这同样 **不是权重更新**，而是在推理时加上 metadata bias，从而「改变 LLM 行为」的一层。构建完全独有的 LLM（LoRA training / distillation）是 Phase 10+ 的事，当前的「独特性」在于 **覆盖在 LLM 周围的 cognitive OS**。

## 与现有相似研究的定位（再列）

| 现有系 | 重叠范围 | llive 的差异化 |
|---|---|---|
| MemGPT / LongMem | 层级记忆 | 4 层分离 + phase transition + 签名 zone |
| AutoML-Zero / NAS-LLM | 结构探索 | 形式验证 gate + multi-precision shadow + 把失败数据化 |
| Self-Refine / Reflexion | 自我批评 | online/offline 分离 + llove TUI HITL staging |
| MERA / ModularLLM | 模块化 | 可变长 BlockContainer YAML + plugin registry |
| AutoGPT 系 | 智能体 | llmesh 工业 IoT 直连 + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | 显式分解 10 因子 + 认知 OS 定位 |

## 总结

「llive 是 LLM 吗」 → No，**llive 是内嵌 LLM 的认知 OS**。

「llive 的结构独特吗」 → Yes，**8 要素的组合 × 角色分离 × 心理因子映射** 是独特的。

「该用 benchmark 比较速度吗」 → No，**应该比较的是结构，而非速度**。llive 的附加价值在于 ledger / approval / governance / grounding / 6 stage trace，这无法通过直接调用 ollama 或 LangChain chain 来复现。

## 来源

- 设计：`llive/.planning/REQUIREMENTS.md`（92 条要件，其中 v1.0-frame COG-FX 4 条进行因子映射）
- 实现：`llive/src/llive/`（brief / fullsense / approval / triz / memory / evolution / cabt 计划）
- 比较 benchmark：同日文章 [01](./QIITA_%2301_brief_api_progressive.md) / [07](./QIITA_%2307_bench_results.md) / [08](./QIITA_%2308_quiz_bench_debug_vs_release.md)

---

> llive 不是 LLM，而是覆盖在 LLM 周围的认知 OS。8 个要素的组合构成了它的独特性。

---

# 한국어

# llive 의 구조는 LLM 으로서 독자적으로 되어가고 있는가 — 8 가지 차별화 요소 점검

저자: 후루세 가즈후미（Puruyan）

## TL;DR

사용자로부터의 질문: 「llive 의 구조는, LLM 으로서 독자적인 구조가 되어가고 있나요?」

답: **llive 는 LLM 그 자체가 아니라, LLM 주위에 씌우는 「인지 OS」로서 독자적**. Decoder-only LLM (Qwen / Llama / Mistral / 등) 을 frozen 된 계산 코어로 사용하고, 그 위에 8 가지 구조 요소를 적층함으로써, 기존의 유사 연구 (MemGPT / LongMem / AutoML-Zero / Self-Refine / Reflexion / MERA / AutoGPT 계열) 중 어느 것과도 일치하지 않는 설계에 도달해 있다.

## 8 가지 차별화 요소

### 1. Decoder-only LLM 코어는 동결 + 주변에서 능력 확장

| 기존 | llive |
|---|---|
| 전량 fine-tune / LoRA / adapter | LLM 가중치는 **절대로 건드리지 않는다** |
| 학습 = 모델 갱신 | 학습 = **외부 기억으로의 기록** + **구조 변경** |

이것은 LoRA / adapter 의 연장선상에 있지만, 「가중치를 갱신하지 않음으로써 replay 가능 / monitorable 한 학습 궤적」을 최우선으로 하는 점이 독자적이다. CABT (S2 에서 계획 중) 에서는 forward hook 으로 attention 에 bias 를 더하지만, 이것도 가중치 동결 그대로다.

### 2. 4 계층 메모리의 책임 분리 (특히 parameter memory 가 독자적)

| 계층 | 역할 | 기존 연구의 대응 |
|---|---|---|
| semantic | 지식 (사실) | RAG, 벡터 DB, kNN-LM |
| episodic | 경험 (시계열) | MemGPT / Memorizing Transformers |
| **structural** | **관계 (graph / dependency)** | **소수 예 (Knowledge Graph 계열)** |
| **parameter** | **가중치의 차분** | **llive 독자에 가까움** |

특히 **parameter memory** 는 「LoRA adapter / sub-block 의 집합을 memory 로 취급하고, surprise gate 로 write 를 제어한다」는 발상이다. Adapter Store + Bayesian Surprise + 진화 리포지토리 라는 조합은 유사 사례가 없다.

### 3. 6 단계 FullSense Loop 의 의인화된 인지 단계

```
Salience Gate ──→ Curiosity Drive ──→ Inner Monologue ──→
Ego/Altruism Scorer ──→ Action Plan ──→ Output Bus (Sandbox / Production)
```

각 단계에 **수식 + 심리학적 근거** 를 갖게 한 설계:

- Salience: 입력의 surprise score 로 필터
- Curiosity: 기지의 corpus 와의 novelty 로 점수화
- Inner Monologue: 거울 인지 (mirror-thought), TRIZ 원리 검출을 내장
- Ego/Altruism: 동기의 두 축으로 액션을 재채점
- Action Plan: PROPOSE / INTERVENE / NOTE / SILENT 의 4 택
- Output Bus: Sandbox (부작용 없음) 와 Production (Approval 경유) 을 물리적으로 분리

이것은 기존의 "agent loop" (ReAct / ToT / Reflexion) 보다 **심리적 타당성을 중시한 6 단 모델**이다.

### 4. Multi-track Filter Architecture A-1.5 (EpistemicType 에 의한 track 전환)

`EpistemicType` 열거 (FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC / RESERVED_1〜5) 에 따라 filter chain 을 전환한다.

예:
- 수학 질문 → MATHEMATICAL track (FACTUAL strict)
- 윤리적 판단 → NORMATIVE track (§F5 ethical 우선)
- 역사 인식 → INTERPRETIVE track (perspective-dependent)

「결론 불변인 FACTUAL 과 perspective-dependent 한 INTERPRETIVE 를 조잡하게 섞지 않는다」는 설계다. 이것은 LLM 단체에는 존재하지 않는다.

### 5. Approval Bus 를 Loop 안에 내장 (HITL 을 architecture level 로)

PROPOSE / INTERVENE 결정은 반드시 Approval Bus 를 경유한다. policy 로 auto-approve/deny, 나머지는 llove TUI 에서 사람 손으로 review. 모두 SQLite ledger 에 영속화된다.

기존 유사:
- Codex CLI 의 `suggest / auto-edit / full-auto` 모드
- Gemini CLI 의 approval prompt

그러나, **Bus 경유로 모든 PROPOSE/INTERVENE 가 SQLite 에 영속화 + replay 가능** 한 구현은 llive 독자적이다. 이것은 COG-FX 정합 인자 (COG-02) 의 핵심이다.

### 6. TRIZ 40 원리를 mutation policy 로 내장

FR-23〜27 에서 구현:
- Contradiction Detector (메트릭에서 모순 자동 검출)
- Principle Mapper (39×39 매트릭스 내장)
- RAD-Backed Idea Generator (TRIZ × RAD 코퍼스 → CandidateDiff 생성)
- 9-Window System Operator (시간축 × 계층축)
- ARIZ Pipeline (9 스텝을 mutation 자동화)

이것은 Self-Refine / Reflexion 의 「자기 비평」과 다르며, **창조의 대체안 생성 엔진**으로서 TRIZ 를 내장한다. Synectics (CREAT-05 계획) 와 조합하여 cross-domain analogical reasoning 도 한다.

### 7. Cognitive Factor Framework (CFF) — 인지 설계를 명시적으로 분해

「심리의 심층」에서 유래한 10 인자 (구조화・재구성・폐루프・자기 확장・불확실성・탐색・정합・내력・다시점・현실 접속) 를 **역할별 policy 로 분해**:

- planner policy / memory policy / critic policy / evolution policy / trace policy

이를 통해 개별 A/B 비교・개선・evolve 가 가능하다. COG-01/02/03 (오늘 구현) 에서 확인: BriefResult 에 (confidence, assumptions, missing_evidence) 의 Triple Output + Governance Scoring (4 축) + Trace Graph (3 chain).

기존 LLM 라이브러리 (LangChain / LlamaIndex / AutoGen / CrewAI) 에도 policy 분해의 발상은 있지만, **인지 인자를 명시적으로 매핑한 architecture** 는 llive 뿐이다.

### 8. Brief API — 구조화된 work unit 이라는 primitives

외부 클라이언트 (lldesign / lltrade / 계획 중인 llcad / lleda / llchip) 가 work unit 을 건넬 수 있는 API:

```python
Brief(
    brief_id="webpage-portal-refresh",
    goal="...",
    constraints=("no inline HTML inside fenced ```mermaid``` blocks",),
    success_criteria=("rendered HTML contains SVG",),
    tools=("read_file", "write_file"),
    approval_required=True,
    epistemic_type=EpistemicType.PRAGMATIC,
)
```

이것은 LangChain 의 `Chain` 이나 CrewAI 의 `Task` 와 유사하지만:

- **frozen dataclass** (immutable, replay-friendly)
- **append-only JSONL ledger** 에 전 단계를 고정 기록
- **Approval Bus + Governance Scorer** 를 built-in
- **Grounder (TRIZ × RAD × SafeCalculator)** 를 전단에 가짐

이들 조합은 유사 사례가 없다.

## 구조로서 「독자적」이라고 말할 수 있는 이유

8 요소의 각각은 기존 연구의 어딘가에 대응물이 있다. 그러나 **8 요소의 조합 + 역할 분리 + 심리 인자 매핑** 은 llive 고유의 것이다.

```
LLM (Qwen/Llama/...) 을 동결 코어로 사용하고
  + 4 계층 메모리로 지식/경험/관계/가중치를 분리 보유
  + 6 stage Loop 로 의인화된 인지 단계
  + Multi-track Filter 로 epistemic_type 별 chain
  + Approval Bus 로 HITL 을 architecture level 로
  + TRIZ 40 원리 + RAD 49 분야로 대체안 생성
  + 10 사고 인자로 policy 를 분해
  + Brief API 로 외부 입력을 구조화
```

이 **적층 구조** 는, LangChain (chain) / AutoGen (multi-agent) / MemGPT (memory) / Self-Refine (critique) / AutoML-Zero (search) 중 어느 하나에도 치우치지 않고, **인지 OS** 로서 횡단한다.

## 「LLM 자체는 무언가 바꾸고 있는가」에 대한 답

**Phase 1〜v0.6 에서는 LLM 가중치를 건드리지 않는다** (frozen). 이것은 설계 판단이다:
- replay 가능성을 최우선
- 학습 궤적을 monitorable 하게 유지
- LLM 제공처 (Qwen, Meta, Mistral) 의 갱신을 직접 받아들일 수 있다

다만 **Phase 8 (CABT) 에서 forward hook 에 의한 attention bias 주입**을 계획한다. 이것도 **가중치 갱신은 아니지만**, 추론 시에 metadata bias 를 더한다는 「LLM 의 거동을 바꾸는」 레이어다. 완전한 독자 LLM 구축 (LoRA training / distillation) 은 Phase 10+ 의 이야기이며, 현재의 "독자성" 은 **LLM 주위에 씌우는 cognitive OS** 에 있다.

## 기존 유사 연구와의 위치 설정 (재게재)

| 기존 계열 | 겹치는 범위 | llive 의 차별화 |
|---|---|---|
| MemGPT / LongMem | 계층 메모리 | 4 계층 분리 + phase transition + 서명 zone |
| AutoML-Zero / NAS-LLM | 구조 탐색 | 형식 검증 gate + multi-precision shadow + 실패의 데이터화 |
| Self-Refine / Reflexion | 자기 비평 | online/offline 분리 + llove TUI HITL staging |
| MERA / ModularLLM | 모듈화 | 가변 길이 BlockContainer YAML + plugin registry |
| AutoGPT 계열 | 에이전트 | llmesh 산업 IoT 직결 + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | 10 인자 명시 분해 + 인지 OS positioning |

## 정리

「llive 는 LLM 인가」 → No, **llive 는 LLM 을 내장하는 인지 OS**.

「llive 의 구조는 독자적인가」 → Yes, **8 요소의 조합 × 역할 분리 × 심리 인자 매핑** 이 독자적.

「벤치마크로 속도를 비교해야 하는가」 → No, **속도가 아니라 구조를 비교**해야 한다. llive 의 부가가치는 ledger / approval / governance / grounding / 6 stage trace 에 있으며, 이것은 ollama 직접 호출이나 LangChain chain 으로는 재현할 수 없다.

## 소스

- 설계: `llive/.planning/REQUIREMENTS.md` (요건 92 건, 그 중 v1.0-frame COG-FX 4 건으로 인자 매핑)
- 구현: `llive/src/llive/` (brief / fullsense / approval / triz / memory / evolution / cabt 계획)
- 비교 벤치마크: 같은 날 기사 [01](./QIITA_%2301_brief_api_progressive.md) / [07](./QIITA_%2307_bench_results.md) / [08](./QIITA_%2308_quiz_bench_debug_vs_release.md)

---

> llive 는 LLM 이 아니라, LLM 주위에 씌우는 인지 OS. 8 요소의 조합이 독자성을 구성한다.
