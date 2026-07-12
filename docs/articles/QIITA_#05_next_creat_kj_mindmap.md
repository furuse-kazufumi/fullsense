---
layout: default
title: "LLM × KJ法 × MindMap で要件定義を自動化する — CREAT 設計予告"
date: 2026-05-17
tags: [llm, agent, creative-thinking, kj-method, mindmap, triz]
project_group: llive
draft: true
id: 0c6deb6f462843a71094
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# LLM × KJ法 × MindMap で要件定義を自動化する — CREAT 設計予告

> **Status**: 設計予告。実装は v0.9 Phase 9 (CREAT-01〜05) で順次着手予定。
> 本記事はユーザー観察「人間の思考の流れは KJ法 / MindMap / TRIZ 等を経て
> 要件定義に入る」を技術設計に落としたもの。

## TL;DR

- 現在の LLM (GPT / Claude / Gemini) は **収束的**思考が得意 (input → answer) だが、**拡散的**思考は弱い
- 人間の創造プロセス: 拡散 (KJ法) → 構造化 (MindMap) → 矛盾解決 (TRIZ) → 多視点検証 (Six Hats) → 構造化変換 (要件 spec)
- llive にこのフルパスを **明示的な拡散層** として組み込み、Brief から要件 spec を自動生成する経路を作る
- 5 件の FR (CREAT-01〜05) として要件化、Phase 9 で段階実装

## 人間の思考フロー vs llive 思考層

```
[人間の思考]                          [llive の対応]
  Brief (問題定義)            ←→     Brief API (LLIVE-002, 実装済 2026-05-17)
       ↓
  KJ法 (拡散 + 親和)          ←→     CREAT-01 KJ法ノード (計画)
       ↓
  MindMap (構造化)            ←→     CREAT-02 MindMap ノード (計画)
       ↓
  TRIZ (矛盾解決)             ←→     既存 FR-23〜27 + CREAT-05 類比 (計画)
       ↓
  Six Hats (多視点検証)       ←→     CREAT-04 + EpistemicType (計画)
       ↓
  要件定義 (構造化変換)        ←→     CREAT-03 構造化変換 (計画)
       ↓
  実装                          ←→    BriefRunner.submit → FullSenseLoop (実装済)
```

## 5 つの FR

### CREAT-01: KJ法ノード

Brief を起点に拡散的にアイデア集合 (≥20 件) を **LLM mixture sampling** で生成。各アイデアを embedding clustering で親和グループ化し、グループ命名と関係線を ledger に記録。

```python
# 設計案
from llive.creat import KjNode

node = KjNode(backend=ollama_backend, target_count=20)
result = node.diverge(brief)
# result.ideas: tuple[str, ...]
# result.clusters: dict[str, list[int]]  # group_name -> idea_indices
# result.relations: list[tuple[int, int, str]]  # (idx_a, idx_b, kind)
```

### CREAT-02: MindMap ノード

中心テーマ → 階層的 sub-topic 展開 (DFS, 深さ 3)。各枝は LLM の 1 呼び出しで分岐。tree 構造を ledger に保存。

### CREAT-03: 構造化変換

KJ + MindMap + TRIZ + Six Hats の 4 出力を統合し、**要件 spec (REQUIREMENTS.md 形式の Markdown 表)** を自動生成。

最終的には: Brief 1 件 → 自動生成された REQUIREMENTS.md フラグメント を出力できる状態。

### CREAT-04: Six Hats Multi-track

Brief を 6 観点 (factual / emotional / cautious / optimistic / creative / process) で多視点評価。各観点が独立した sub-Brief を発行 → 並列実行 → 結論を統合。

既存 `EpistemicType` の拡張 + Multi-track Filter Architecture A-1.5 と統合。

### CREAT-05: Synectics 類比エンジン

RAD コーパス (49 分野) から「Brief と意味的に遠いが構造的に類似」な doc を取得 → TRIZ 原理に紐付けて発想資源化。raptor の `cross_domain_ideation` skill と連携。

## なぜ「明示的な拡散層」か

LLM の単一回答に頼ると、いくつかの典型的な失敗が起きる:

| 典型的失敗 | 原因 | 拡散層での対策 |
|---|---|---|
| 視野狭窄 | 最初の候補に引きずられる | KJ法 ≥20 候補を**強制** |
| 思考の浅さ | 1 階層しか展開しない | MindMap で深さ 3 を**強制** |
| 偏った楽観 | "良い案ばかり" 出す | Six Hats で cautious 観点を**強制** |
| 既存パターン依存 | 知っている解の組合せに終始 | Synectics で異分野類比を**強制** |

## スパイラル開発 (C1-C6)

| Iter | スコープ | 評価 | リスク |
|---|---|---|---|
| C1 | CREAT-01 KJ法ノード — 拡散 sampling + clustering | 1 Brief で ≥20 件 + group ≥3 | 中 (LLM 呼出回数増) |
| C2 | CREAT-02 MindMap ノード — DFS depth=3 | tree 構造の妥当性、leaf の具体性 | 中 (token コスト) |
| C3 | CREAT-04 Six Hats — 6 sub-Brief 並列発行 | 観点間独立性、結論多様性 | 中 |
| C4 | CREAT-05 類比エンジン — cross-domain RAD bridge | 類比の有用性 (人間評価) | 高 (semantic distance metric 設計) |
| C5 | CREAT-03 構造化変換 — 4 種出力を要件 spec に合成 | spec の網羅性 + 矛盾検出 | 高 (出力品質測定が困難) |
| C6 | 統合 — KJ → MindMap → TRIZ → Six Hats → 構造化変換 のフルパス | end-to-end Brief → REQUIREMENTS.md 自動生成 | 高 (アーキ統合) |

## llove TUI との統合

C6 完成時には llove TUI に **Creative Workbench** モードを追加:

- KJ 付箋ボード (drag & drop で再グルーピング可)
- MindMap 樹形図 (折り畳み可)
- Six Hats 6 タブ (観点切替で同じ Brief を異なる視点で表示)
- 構造化変換結果のリアルタイムプレビュー

HITL (Human-in-the-loop) の力を最大化するインタフェース設計。

## 既存研究との位置づけ

- **Tree of Thoughts** (Yao 2023): DFS 推論
- **Self-Refine** (Madaan 2023): 自己批評ループ
- **Reflexion** (Shinn 2023): エピソード記憶からの改善
- **CoT / Auto-CoT** (Wei 2022 / Zhang 2023): 推論パス露出

llive の差別化: **拡散プロセスを明示的に構造化 + ledger に固定記録** → 後から replay / audit / 学習データ抽出可能。

## ソース (実装前)

- 要件: REQUIREMENTS.md v0.9 CREAT セクション
- ロードマップ: ROADMAP.md Phase 9
- 既存 TRIZ 連携: `src/llive/triz/`

## 完成版記事の予告

C1 (CREAT-01 KJ法ノード) 実装後に draft 解除し:
- 実 Brief × CREAT-01 拡散結果の可視化 (clusters)
- LLM 呼出コストの実測
- 比較: 単一回答 vs KJ法経由の意思決定品質
を追加してリリースします。

---

> 設計記事段階。実装が進んだ時点で内容を更新します。

---

# English

# Automating Requirements Definition with LLM × KJ Method × MindMap — CREAT Design Preview

> **Status**: Design preview. Implementation will proceed incrementally in v0.9 Phase 9 (CREAT-01 through 05).
> This article translates the user observation "human thought flows through the KJ method / MindMap / TRIZ and so on before entering requirements definition" into a technical design.

## TL;DR

- Today's LLMs (GPT / Claude / Gemini) are good at **convergent** thinking (input → answer) but weak at **divergent** thinking
- The human creative process: divergence (KJ method) → structuring (MindMap) → contradiction resolution (TRIZ) → multi-perspective verification (Six Hats) → structured conversion (requirements spec)
- We embed this full path into llive as an **explicit divergence layer**, building a route that auto-generates a requirements spec from a Brief
- Formalized as 5 FRs (CREAT-01 through 05), implemented in stages in Phase 9

## Human Thought Flow vs. llive Thinking Layers

```
[人間の思考]                          [llive の対応]
  Brief (問題定義)            ←→     Brief API (LLIVE-002, 実装済 2026-05-17)
       ↓
  KJ法 (拡散 + 親和)          ←→     CREAT-01 KJ法ノード (計画)
       ↓
  MindMap (構造化)            ←→     CREAT-02 MindMap ノード (計画)
       ↓
  TRIZ (矛盾解決)             ←→     既存 FR-23〜27 + CREAT-05 類比 (計画)
       ↓
  Six Hats (多視点検証)       ←→     CREAT-04 + EpistemicType (計画)
       ↓
  要件定義 (構造化変換)        ←→     CREAT-03 構造化変換 (計画)
       ↓
  実装                          ←→    BriefRunner.submit → FullSenseLoop (実装済)
```

## The Five FRs

### CREAT-01: KJ Method Node

Starting from a Brief, divergently generate a set of ideas (≥20) via **LLM mixture sampling**. Group each idea into affinity clusters with embedding clustering, and record cluster naming and relationship lines in the ledger.

```python
# 設計案
from llive.creat import KjNode

node = KjNode(backend=ollama_backend, target_count=20)
result = node.diverge(brief)
# result.ideas: tuple[str, ...]
# result.clusters: dict[str, list[int]]  # group_name -> idea_indices
# result.relations: list[tuple[int, int, str]]  # (idx_a, idx_b, kind)
```

### CREAT-02: MindMap Node

Central theme → hierarchical sub-topic expansion (DFS, depth 3). Each branch is split by a single LLM call. Save the tree structure to the ledger.

### CREAT-03: Structured Conversion

Integrate the four outputs of KJ + MindMap + TRIZ + Six Hats and auto-generate a **requirements spec (a Markdown table in REQUIREMENTS.md format)**.

The ultimate goal: a state where one Brief → an auto-generated REQUIREMENTS.md fragment can be output.

### CREAT-04: Six Hats Multi-track

Evaluate a Brief from six perspectives (factual / emotional / cautious / optimistic / creative / process), each from a different viewpoint. Each perspective issues an independent sub-Brief → runs in parallel → conclusions are integrated.

An extension of the existing `EpistemicType`, integrated with the Multi-track Filter Architecture A-1.5.

### CREAT-05: Synectics Analogy Engine

Retrieve docs from the RAD corpus (49 domains) that are "semantically distant from the Brief but structurally similar," then tie them to TRIZ principles to turn them into ideation resources. Linked with raptor's `cross_domain_ideation` skill.

## Why an "Explicit Divergence Layer"?

Relying on a single LLM answer leads to several typical failure modes:

| Typical failure | Cause | Countermeasure in the divergence layer |
|---|---|---|
| Tunnel vision | Anchored to the first candidate | **Force** ≥20 candidates with the KJ method |
| Shallow thinking | Only expands one level | **Force** depth 3 with MindMap |
| Biased optimism | Outputs "only good ideas" | **Force** the cautious perspective with Six Hats |
| Dependence on existing patterns | Stuck recombining known solutions | **Force** cross-domain analogies with Synectics |

## Spiral Development (C1–C6)

| Iter | Scope | Evaluation | Risk |
|---|---|---|---|
| C1 | CREAT-01 KJ method node — divergence sampling + clustering | ≥20 items + ≥3 groups for one Brief | Medium (more LLM calls) |
| C2 | CREAT-02 MindMap node — DFS depth=3 | Validity of tree structure, concreteness of leaves | Medium (token cost) |
| C3 | CREAT-04 Six Hats — 6 sub-Briefs issued in parallel | Independence across perspectives, diversity of conclusions | Medium |
| C4 | CREAT-05 analogy engine — cross-domain RAD bridge | Usefulness of analogies (human evaluation) | High (designing the semantic distance metric) |
| C5 | CREAT-03 structured conversion — synthesize 4 output types into a requirements spec | Spec comprehensiveness + contradiction detection | High (output quality is hard to measure) |
| C6 | Integration — full path of KJ → MindMap → TRIZ → Six Hats → structured conversion | End-to-end Brief → auto-generation of REQUIREMENTS.md | High (architectural integration) |

## Integration with the llove TUI

When C6 is complete, a **Creative Workbench** mode will be added to the llove TUI:

- KJ sticky-note board (re-groupable by drag & drop)
- MindMap tree diagram (collapsible)
- Six Hats 6 tabs (switch perspectives to view the same Brief from different viewpoints)
- Real-time preview of structured-conversion results

An interface design that maximizes the power of HITL (Human-in-the-loop).

## Positioning Relative to Prior Research

- **Tree of Thoughts** (Yao 2023): DFS reasoning
- **Self-Refine** (Madaan 2023): self-critique loop
- **Reflexion** (Shinn 2023): improvement from episodic memory
- **CoT / Auto-CoT** (Wei 2022 / Zhang 2023): exposing the reasoning path

llive's differentiation: **explicitly structuring the divergence process + pinning it into the ledger** → enabling later replay / audit / extraction of training data.

## Sources (Pre-implementation)

- Requirements: REQUIREMENTS.md v0.9 CREAT section
- Roadmap: ROADMAP.md Phase 9
- Existing TRIZ integration: `src/llive/triz/`

## Preview of the Finished Article

After C1 (CREAT-01 KJ method node) is implemented, the draft will be lifted and we will add:
- Visualization of real Brief × CREAT-01 divergence results (clusters)
- Actual measurement of LLM call cost
- Comparison: single answer vs. decision quality via the KJ method
and then release it.

---

> Design-article stage. Content will be updated as implementation progresses.

---

# 中文

# 用 LLM × KJ 法 × 思维导图自动化需求定义 — CREAT 设计预告

> **Status**: 设计预告。实现将在 v0.9 Phase 9（CREAT-01〜05）中逐步推进。
> 本文将用户的观察「人类的思考流程会经过 KJ 法 / 思维导图 / TRIZ 等，然后才进入需求定义」落实为技术设计。

## TL;DR

- 当前的 LLM（GPT / Claude / Gemini）擅长**收敛性**思考（input → answer），但**发散性**思考较弱
- 人类的创造过程：发散（KJ 法）→ 结构化（思维导图）→ 矛盾解决（TRIZ）→ 多视角验证（Six Hats）→ 结构化转换（需求 spec）
- 将这条完整路径作为**显式的发散层**嵌入 llive，构建从 Brief 自动生成需求 spec 的通路
- 形式化为 5 个 FR（CREAT-01〜05），在 Phase 9 中分阶段实现

## 人类思考流程 vs llive 思考层

```
[人間の思考]                          [llive の対応]
  Brief (問題定義)            ←→     Brief API (LLIVE-002, 実装済 2026-05-17)
       ↓
  KJ法 (拡散 + 親和)          ←→     CREAT-01 KJ法ノード (計画)
       ↓
  MindMap (構造化)            ←→     CREAT-02 MindMap ノード (計画)
       ↓
  TRIZ (矛盾解決)             ←→     既存 FR-23〜27 + CREAT-05 類比 (計画)
       ↓
  Six Hats (多視点検証)       ←→     CREAT-04 + EpistemicType (計画)
       ↓
  要件定義 (構造化変換)        ←→     CREAT-03 構造化変換 (計画)
       ↓
  実装                          ←→    BriefRunner.submit → FullSenseLoop (実装済)
```

## 五个 FR

### CREAT-01：KJ 法节点

以 Brief 为起点，通过 **LLM mixture sampling** 发散式生成一组创意（≥20 件）。用 embedding clustering 将每个创意进行亲和分组，并将分组命名与关系连线记录到 ledger。

```python
# 設計案
from llive.creat import KjNode

node = KjNode(backend=ollama_backend, target_count=20)
result = node.diverge(brief)
# result.ideas: tuple[str, ...]
# result.clusters: dict[str, list[int]]  # group_name -> idea_indices
# result.relations: list[tuple[int, int, str]]  # (idx_a, idx_b, kind)
```

### CREAT-02：思维导图节点

中心主题 → 层级化 sub-topic 展开（DFS，深度 3）。每个分支由 1 次 LLM 调用进行分叉。将 tree 结构保存到 ledger。

### CREAT-03：结构化转换

整合 KJ + 思维导图 + TRIZ + Six Hats 的四种输出，自动生成**需求 spec（REQUIREMENTS.md 格式的 Markdown 表格）**。

最终目标是：达到可以从 1 件 Brief → 自动生成的 REQUIREMENTS.md 片段 的输出状态。

### CREAT-04：Six Hats Multi-track

从 6 个视角（factual / emotional / cautious / optimistic / creative / process）对 Brief 进行多视角评估。每个视角发出独立的 sub-Brief → 并行执行 → 整合结论。

对现有 `EpistemicType` 的扩展 + 与 Multi-track Filter Architecture A-1.5 集成。

### CREAT-05：Synectics 类比引擎

从 RAD 语料库（49 个领域）中检索「与 Brief 在语义上较远但在结构上相似」的 doc → 关联到 TRIZ 原理，将其转化为发想资源。与 raptor 的 `cross_domain_ideation` skill 联动。

## 为什么需要「显式的发散层」

仅依赖 LLM 的单一回答时，会出现几种典型的失败：

| 典型失败 | 原因 | 发散层的对策 |
|---|---|---|
| 视野狭窄 | 被最初的候选牵着走 | 用 KJ 法**强制** ≥20 个候选 |
| 思考浅薄 | 只展开一个层级 | 用思维导图**强制**深度 3 |
| 偏向乐观 | 只产出「好点子」 | 用 Six Hats**强制** cautious 视角 |
| 依赖既有模式 | 始终在已知解的组合中打转 | 用 Synectics**强制**跨领域类比 |

## 螺旋式开发（C1-C6）

| Iter | 范围 | 评估 | 风险 |
|---|---|---|---|
| C1 | CREAT-01 KJ 法节点 — 发散 sampling + clustering | 1 件 Brief 产出 ≥20 件 + group ≥3 | 中（LLM 调用次数增加） |
| C2 | CREAT-02 思维导图节点 — DFS depth=3 | tree 结构的合理性、leaf 的具体性 | 中（token 成本） |
| C3 | CREAT-04 Six Hats — 6 个 sub-Brief 并行发出 | 视角间独立性、结论多样性 | 中 |
| C4 | CREAT-05 类比引擎 — cross-domain RAD bridge | 类比的有用性（人工评估） | 高（semantic distance metric 设计） |
| C5 | CREAT-03 结构化转换 — 将 4 种输出合成为需求 spec | spec 的完备性 + 矛盾检测 | 高（输出质量难以测量） |
| C6 | 集成 — KJ → 思维导图 → TRIZ → Six Hats → 结构化转换 的完整路径 | end-to-end Brief → REQUIREMENTS.md 自动生成 | 高（架构集成） |

## 与 llove TUI 的集成

C6 完成时，将在 llove TUI 中添加 **Creative Workbench** 模式：

- KJ 便签板（可通过 drag & drop 重新分组）
- 思维导图树形图（可折叠）
- Six Hats 6 个标签页（切换视角，以不同视点查看同一个 Brief）
- 结构化转换结果的实时预览

最大化 HITL（Human-in-the-loop）能力的接口设计。

## 与既有研究的定位

- **Tree of Thoughts**（Yao 2023）：DFS 推理
- **Self-Refine**（Madaan 2023）：自我批评循环
- **Reflexion**（Shinn 2023）：从情景记忆中改进
- **CoT / Auto-CoT**（Wei 2022 / Zhang 2023）：暴露推理路径

llive 的差异化：**将发散过程显式结构化 + 固定记录到 ledger** → 之后可 replay / audit / 抽取训练数据。

## 来源（实现前）

- 需求：REQUIREMENTS.md v0.9 CREAT 章节
- 路线图：ROADMAP.md Phase 9
- 既有 TRIZ 联动：`src/llive/triz/`

## 完成版文章预告

在 C1（CREAT-01 KJ 法节点）实现后解除 draft，并追加：
- 真实 Brief × CREAT-01 发散结果的可视化（clusters）
- LLM 调用成本的实测
- 比较：单一回答 vs 经 KJ 法的决策质量
然后发布。

---

> 设计文章阶段。实现推进后将更新内容。

---

# 한국어

# LLM × KJ법 × 마인드맵으로 요구사항 정의를 자동화한다 — CREAT 설계 예고

> **Status**: 설계 예고. 구현은 v0.9 Phase 9(CREAT-01〜05)에서 순차적으로 착수할 예정.
> 본 글은 사용자의 관찰「인간의 사고 흐름은 KJ법 / 마인드맵 / TRIZ 등을 거쳐 요구사항 정의로 들어간다」를 기술 설계로 옮긴 것이다.

## TL;DR

- 현재의 LLM(GPT / Claude / Gemini)은 **수렴적** 사고(input → answer)에는 능하지만 **발산적** 사고는 약하다
- 인간의 창조 과정: 발산(KJ법) → 구조화(마인드맵) → 모순 해결(TRIZ) → 다관점 검증(Six Hats) → 구조화 변환(요구사항 spec)
- 이 전체 경로를 **명시적인 발산 계층**으로서 llive에 내장하고, Brief에서 요구사항 spec을 자동 생성하는 경로를 만든다
- 5건의 FR(CREAT-01〜05)로 요구사항화하여 Phase 9에서 단계적으로 구현

## 인간의 사고 흐름 vs llive 사고 계층

```
[人間の思考]                          [llive の対応]
  Brief (問題定義)            ←→     Brief API (LLIVE-002, 実装済 2026-05-17)
       ↓
  KJ法 (拡散 + 親和)          ←→     CREAT-01 KJ法ノード (計画)
       ↓
  MindMap (構造化)            ←→     CREAT-02 MindMap ノード (計画)
       ↓
  TRIZ (矛盾解決)             ←→     既存 FR-23〜27 + CREAT-05 類比 (計画)
       ↓
  Six Hats (多視点検証)       ←→     CREAT-04 + EpistemicType (計画)
       ↓
  要件定義 (構造化変換)        ←→     CREAT-03 構造化変換 (計画)
       ↓
  実装                          ←→    BriefRunner.submit → FullSenseLoop (実装済)
```

## 5개의 FR

### CREAT-01: KJ법 노드

Brief를 기점으로 발산적으로 아이디어 집합(≥20건)을 **LLM mixture sampling**으로 생성. 각 아이디어를 embedding clustering으로 친화 그룹화하고, 그룹 명명과 관계선을 ledger에 기록.

```python
# 設計案
from llive.creat import KjNode

node = KjNode(backend=ollama_backend, target_count=20)
result = node.diverge(brief)
# result.ideas: tuple[str, ...]
# result.clusters: dict[str, list[int]]  # group_name -> idea_indices
# result.relations: list[tuple[int, int, str]]  # (idx_a, idx_b, kind)
```

### CREAT-02: 마인드맵 노드

중심 테마 → 계층적 sub-topic 전개(DFS, 깊이 3). 각 가지는 LLM의 1회 호출로 분기. tree 구조를 ledger에 저장.

### CREAT-03: 구조화 변환

KJ + 마인드맵 + TRIZ + Six Hats의 4개 출력을 통합하여 **요구사항 spec(REQUIREMENTS.md 형식의 Markdown 표)**을 자동 생성.

최종적으로는: Brief 1건 → 자동 생성된 REQUIREMENTS.md 프래그먼트를 출력할 수 있는 상태.

### CREAT-04: Six Hats Multi-track

Brief를 6개 관점(factual / emotional / cautious / optimistic / creative / process)으로 다관점 평가. 각 관점이 독립된 sub-Brief를 발행 → 병렬 실행 → 결론을 통합.

기존 `EpistemicType`의 확장 + Multi-track Filter Architecture A-1.5와 통합.

### CREAT-05: Synectics 유추 엔진

RAD 코퍼스(49개 분야)에서 「Brief와 의미적으로는 멀지만 구조적으로 유사한」 doc을 가져와 → TRIZ 원리에 연결하여 발상 자원화. raptor의 `cross_domain_ideation` skill과 연계.

## 왜 「명시적인 발산 계층」인가

LLM의 단일 답변에 의존하면 몇 가지 전형적인 실패가 발생한다:

| 전형적 실패 | 원인 | 발산 계층에서의 대책 |
|---|---|---|
| 시야 협착 | 최초의 후보에 끌려간다 | KJ법으로 ≥20 후보를 **강제** |
| 사고의 얕음 | 한 계층만 전개한다 | 마인드맵으로 깊이 3을 **강제** |
| 치우친 낙관 | "좋은 안만" 내놓는다 | Six Hats로 cautious 관점을 **강제** |
| 기존 패턴 의존 | 알고 있는 해의 조합에 머문다 | Synectics로 이분야 유추를 **강제** |

## 스파이럴 개발(C1-C6)

| Iter | 범위 | 평가 | 리스크 |
|---|---|---|---|
| C1 | CREAT-01 KJ법 노드 — 발산 sampling + clustering | 1 Brief에서 ≥20건 + group ≥3 | 중(LLM 호출 횟수 증가) |
| C2 | CREAT-02 마인드맵 노드 — DFS depth=3 | tree 구조의 타당성, leaf의 구체성 | 중(token 비용) |
| C3 | CREAT-04 Six Hats — 6 sub-Brief 병렬 발행 | 관점 간 독립성, 결론 다양성 | 중 |
| C4 | CREAT-05 유추 엔진 — cross-domain RAD bridge | 유추의 유용성(인간 평가) | 고(semantic distance metric 설계) |
| C5 | CREAT-03 구조화 변환 — 4종 출력을 요구사항 spec으로 합성 | spec의 망라성 + 모순 검출 | 고(출력 품질 측정이 곤란) |
| C6 | 통합 — KJ → 마인드맵 → TRIZ → Six Hats → 구조화 변환의 풀 패스 | end-to-end Brief → REQUIREMENTS.md 자동 생성 | 고(아키텍처 통합) |

## llove TUI와의 통합

C6 완성 시에는 llove TUI에 **Creative Workbench** 모드를 추가:

- KJ 포스트잇 보드(drag & drop으로 재그룹화 가능)
- 마인드맵 수형도(접기 가능)
- Six Hats 6개 탭(관점 전환으로 같은 Brief를 다른 시점으로 표시)
- 구조화 변환 결과의 실시간 미리보기

HITL(Human-in-the-loop)의 힘을 극대화하는 인터페이스 설계.

## 기존 연구와의 위치 설정

- **Tree of Thoughts**(Yao 2023): DFS 추론
- **Self-Refine**(Madaan 2023): 자기 비평 루프
- **Reflexion**(Shinn 2023): 에피소드 기억으로부터의 개선
- **CoT / Auto-CoT**(Wei 2022 / Zhang 2023): 추론 경로 노출

llive의 차별화: **발산 프로세스를 명시적으로 구조화 + ledger에 고정 기록** → 나중에 replay / audit / 학습 데이터 추출 가능.

## 소스(구현 전)

- 요구사항: REQUIREMENTS.md v0.9 CREAT 섹션
- 로드맵: ROADMAP.md Phase 9
- 기존 TRIZ 연계: `src/llive/triz/`

## 완성판 글 예고

C1(CREAT-01 KJ법 노드) 구현 후에 draft를 해제하고:
- 실제 Brief × CREAT-01 발산 결과의 시각화(clusters)
- LLM 호출 비용의 실측
- 비교: 단일 답변 vs KJ법을 거친 의사결정 품질
을 추가하여 릴리스합니다.

---

> 설계 글 단계. 구현이 진행되는 시점에 내용을 업데이트합니다.
