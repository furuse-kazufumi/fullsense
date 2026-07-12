---
layout: default
title: "10 思考因子で整理する llive 思考層"
date: 2026-05-17
tags: [llm, agent, cognitive-architecture, design]
project_group: llive
id: 4de8dcff1cf4c2ab9bdc
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 「心理の深層」10 因子で整理する llive 思考層 — 既に 9/10 実装済

## TL;DR

- 「心理の深層」YouTube から抽出された **10 思考因子** (構造化・再構成・閉ループ・自己拡張・不確実性・探索・整合・来歴・多視点・現実接続) を llive 既存 FR にマッピング
- v1.0 リリース必須の **土台 5 因子 (構造化 / 閉ループ / 不確実性 / 整合 / 来歴) は全て実装済**
- 不足分を COG-01〜04 として要件化し、2026-05-17 同セッション内で COG-01/02/03 を実装完了
- 残るは「現実接続」(Phase 4 IoT) と「多視点」の強化 (CREAT-04 と統合する COG-04)

## なぜ 10 因子フレームワークか

汎用 LLM の能力評価は「知識量」「言語流暢性」「推論精度」で語られがちですが、エージェント設計では **「どの認知フレームで状況を切るか」** の方が決定的に効きます。

ユーザー観察:

> 探索 / 再構成を強化する前に、構造化 / 不確実性 / 閉ループ / 整合 / 来歴の土台が必要

これがない状態で探索因子や再構成因子を強くすると、面白い案は増えるが、誤差・暴走・非再現性も増える。

この時点で **10 因子のうち 9/10 には既存 FR か同日実装による初期マッピングがある**。ただし **初期マッピング済み = 十分に成熟済み** ではない。とくに「多視点」は強化余地が残り、**未マッピングのまま残っている 1 因子** は「現実接続」で、これは Phase 4 IoT と実環境 integration 側の宿題として切り分ける。

## 10 因子 × llive マッピング

| # | 因子 | LLM 役割 | llive 既存 (実装済) | 追加 (2026-05-17 実装) |
|---|---|---|---|---|
| 1 | 構造化 | 課題を分解 | Brief constraints, Salience+Curiosity gate | — |
| 2 | 再構成 | 代替案生成 | TRIZ 40 原理 + ARIZ + 9 画法 (FR-23〜27) | (CREAT-01 計画) |
| 3 | 閉ループ | 検証計画を伴う | BriefRunner (submit→plan→approval→tool→outcome) | — |
| 4 | 自己拡張 | 外部資源を使う | 4 層メモリ + RAD 49 分野 + tools whitelist | MATH-08 計算エンジン |
| 5 | 不確実性 | 仮説と事実を分離 | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | 探索 | 未踏案を試す | EVO-* (Z3 + Failed Reservoir + Reverse-Evo) | — |
| 7 | 整合 | 全体制約で再評価 | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | 来歴 | 判断履歴を残す | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | 多視点 | 評価関数を分離 | Multi-track Filter A-1.5 (5 EpistemicType) | (COG-04 + CREAT-04 計画) |
| 10 | 現実接続 | 実環境制約を扱う | (Phase 4 INT-01〜04 計画中) | — |

## v1.0 必須 5 因子は全て実装済

| 因子 | 実装場所 | 役割 |
|---|---|---|
| 構造化 | `src/llive/brief/types.py::Brief` + loop._salience_gate / _curiosity_drive | 課題を decompose |
| 閉ループ | `src/llive/brief/runner.py::BriefRunner.submit` | plan-act-check loop |
| 不確実性 | `src/llive/learning/bayesian_surprise.py` (FR-21) + COG-01 | 仮説と事実の三層分離 |
| 整合 | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py` (EVO-04) + COG-02 | 全体制約 + governance |
| 来歴 | `src/llive/memory/provenance.py` + `src/llive/approval/ledger.py` + `src/llive/brief/ledger.py` + COG-03 | evidence/tool/decision chain |

これは llive が「v1.0 リリース水準で誤差・暴走・非再現性を防ぐ土台を備えている」という強い根拠です。

## 新規 COG-01〜03 の実装

### COG-01 Triple Output (不確実性因子の強化)

`BriefResult` に 3 列追加:

```python
@dataclass
class BriefResult:
    # ... 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` が決定論的に算出:

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`: grounding 不在 / success_criteria 不在を明文化
- `missing_evidence`: TRIZ 原理が surface しなかった / tool 失敗 を保存

すべて ledger の `outcome` event に固定記録 → auditor が後から検証可能。

### COG-02 Governance Scoring Layer (整合因子の強化)

Approval Bus の **前段** に 4 軸スコアラを挿入:

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block を返す
```

責務分離:
- **Governance** = scoring (なぜ良い/悪いか)
- **Approval Bus** = gating (実行可否の判断)

dangerous_token 検出 (`rm -rf` / `DROP TABLE` / `format c:` 等)、INTERVENE-without-approval ペナルティ、`block_threshold` / `safety_floor` をサポート。

### COG-03 Trace Graph (来歴因子の強化)

`BriefLedger.trace_graph()` メソッドが 3 層 view を返す:

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

これにより、デバッグ・自己改善・失敗分析・evolution への学習データ抽出が機械的に可能になります。

## 横断 metadata schema

各メモリ・各 ledger entry に統一 attribute を付与する設計:

```python
{
    "factor": "uncertainty",       # 10 因子のどれか
    "uncertainty": 0.23,
    "dependency": ["evidence:doc#42", "tool:sympy.simplify"],
    "evidence_source": "doc#42",
    "applicable_scope": "math:dimensional",
    "promotion_status": "candidate",
}
```

LLM の自然言語ルールに依存せず、llove TUI / audit agent / evolution scheduler が機械的に消費できる形式。

## 結論

「面白い AI を作る」前に「壊れない AI を作る」ためのフレームワークとして、10 因子は強い指針になります。llive はその土台 5 因子をすべて実装済で、これからは **再構成・探索** (CREAT / EVO / TRIZ) を安心して積める段階に入りました。

## ソース

- 要件: `llive/.planning/REQUIREMENTS.md` v1.0-frame COG-FX セクション
- 実装: `src/llive/brief/governance.py` (新規) + `src/llive/brief/ledger.py::trace_graph()` (拡張) + `src/llive/brief/types.py::BriefResult` (拡張)
- テスト: `tests/unit/test_brief_cog.py` (16 件) — 1014 PASS / 回帰ゼロ
- memory: `project_llive_cog_fx_factors.md`

---

> 出典: 「心理の深層」 YouTube チャンネルから抽出された人間の思考因子セットを、ユーザーが「LLM に組み込める形」に変換した結果を要件化したものです。

---

# English

# Organizing the llive Thinking Layer with the 10 Cognitive Factors of "The Depths of the Mind" — 9/10 Already Implemented

## TL;DR

- We map the **10 cognitive factors** extracted from the "The Depths of the Mind" YouTube channel (structuring, reframing, closed loop, self-expansion, uncertainty, exploration, coherence, provenance, multi-perspective, reality grounding) onto llive's existing FRs.
- The **5 foundational factors required for the v1.0 release (structuring / closed loop / uncertainty / coherence / provenance) are all already implemented**.
- The missing pieces were specified as COG-01 through COG-04, and COG-01/02/03 were implemented within the same 2026-05-17 session.
- What remains is "reality grounding" (Phase 4 IoT) and the reinforcement of "multi-perspective" (COG-04, which integrates with CREAT-04).

## Why the 10-Factor Framework

The capabilities of general-purpose LLMs tend to be discussed in terms of "knowledge volume," "linguistic fluency," and "reasoning accuracy," but in agent design, **"which cognitive frame you use to slice the situation"** has a far more decisive effect.

User observation:

> Before strengthening exploration / reframing, you need the foundation of structuring / uncertainty / closed loop / coherence / provenance.

Without this foundation, strengthening the exploration or reframing factors increases the number of interesting ideas, but it also increases error, runaway behavior, and non-reproducibility.

At this point, **9 out of the 10 factors have at least an initial mapping through existing FRs or implementations added on the same day**. However, **having an initial mapping is not the same as being fully mature**. "Multi-perspective" still needs further strengthening, while the **one factor that remains unmapped** is "reality grounding," intentionally split out as homework for the Phase 4 IoT / real-environment integration side.

## The 10 Factors × llive Mapping

| # | Factor | LLM Role | Existing in llive (implemented) | Added (implemented 2026-05-17) |
|---|---|---|---|---|
| 1 | Structuring | Decompose the problem | Brief constraints, Salience+Curiosity gate | — |
| 2 | Reframing | Generate alternatives | TRIZ 40 principles + ARIZ + 9-windows (FR-23–27) | (CREAT-01 planned) |
| 3 | Closed loop | Accompanied by a verification plan | BriefRunner (submit→plan→approval→tool→outcome) | — |
| 4 | Self-expansion | Use external resources | 4-layer memory + RAD 49 fields + tools whitelist | MATH-08 calculation engine |
| 5 | Uncertainty | Separate hypotheses from facts | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | Exploration | Try uncharted ideas | EVO-* (Z3 + Failed Reservoir + Reverse-Evo) | — |
| 7 | Coherence | Re-evaluate under global constraints | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | Provenance | Keep a record of decisions | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | Multi-perspective | Separate evaluation functions | Multi-track Filter A-1.5 (5 EpistemicType) | (COG-04 + CREAT-04 planned) |
| 10 | Reality grounding | Handle real-environment constraints | (Phase 4 INT-01–04 in planning) | — |

## The 5 Mandatory v1.0 Factors Are All Implemented

| Factor | Implementation Location | Role |
|---|---|---|
| Structuring | `src/llive/brief/types.py::Brief` + loop._salience_gate / _curiosity_drive | Decompose the problem |
| Closed loop | `src/llive/brief/runner.py::BriefRunner.submit` | plan-act-check loop |
| Uncertainty | `src/llive/learning/bayesian_surprise.py` (FR-21) + COG-01 | Three-layer separation of hypothesis and fact |
| Coherence | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py` (EVO-04) + COG-02 | Global constraints + governance |
| Provenance | `src/llive/memory/provenance.py` + `src/llive/approval/ledger.py` + `src/llive/brief/ledger.py` + COG-03 | evidence/tool/decision chain |

This is strong evidence that llive "is equipped with a foundation that prevents error, runaway behavior, and non-reproducibility at the v1.0 release level."

## Implementing the New COG-01–03

### COG-01 Triple Output (Strengthening the Uncertainty Factor)

Three columns added to `BriefResult`:

```python
@dataclass
class BriefResult:
    # ... 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` computes them deterministically:

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`: makes explicit the absence of grounding / absence of success_criteria
- `missing_evidence`: stores cases where a TRIZ principle did not surface / a tool failed

All of it is fixed-recorded into the ledger's `outcome` event → an auditor can verify it later.

### COG-02 Governance Scoring Layer (Strengthening the Coherence Factor)

A 4-axis scorer is inserted in the **stage before** the Approval Bus:

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block を返す
```

Separation of responsibilities:
- **Governance** = scoring (why it is good/bad)
- **Approval Bus** = gating (the judgment of whether to execute)

It supports dangerous_token detection (`rm -rf` / `DROP TABLE` / `format c:` etc.), an INTERVENE-without-approval penalty, and `block_threshold` / `safety_floor`.

### COG-03 Trace Graph (Strengthening the Provenance Factor)

The `BriefLedger.trace_graph()` method returns a 3-layer view:

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

This makes debugging, self-improvement, failure analysis, and extraction of learning data for evolution mechanically possible.

## Cross-Cutting Metadata Schema

A design that attaches a unified attribute to each memory and each ledger entry:

```python
{
    "factor": "uncertainty",       # 10 因子のどれか
    "uncertainty": 0.23,
    "dependency": ["evidence:doc#42", "tool:sympy.simplify"],
    "evidence_source": "doc#42",
    "applicable_scope": "math:dimensional",
    "promotion_status": "candidate",
}
```

A format that does not depend on the LLM's natural-language rules and that the llove TUI / audit agent / evolution scheduler can consume mechanically.

## Conclusion

As a framework for "building an AI that doesn't break" before "building an interesting AI," the 10 factors serve as a strong guiding principle. llive has already implemented all 5 of those foundational factors, and it has now entered a stage where it can safely stack up **reframing and exploration** (CREAT / EVO / TRIZ).

## Sources

- Requirements: `llive/.planning/REQUIREMENTS.md` v1.0-frame COG-FX section
- Implementation: `src/llive/brief/governance.py` (new) + `src/llive/brief/ledger.py::trace_graph()` (extended) + `src/llive/brief/types.py::BriefResult` (extended)
- Tests: `tests/unit/test_brief_cog.py` (16 cases) — 1014 PASS / zero regressions
- memory: `project_llive_cog_fx_factors.md`

---

> Source: This is the result of taking a set of human thinking factors extracted from the "The Depths of the Mind" YouTube channel, having the user convert them into "a form that can be embedded in an LLM," and turning that into requirements.

---

# 中文

# 用《心理的深层》10 因子梳理 llive 思考层 — 已实现 9/10

## TL;DR

- 将从《心理的深层》YouTube 频道中提取的 **10 个思考因子**（结构化・重构・闭环・自我扩展・不确定性・探索・一致性・来历・多视角・现实连接）映射到 llive 既有的 FR。
- v1.0 发布所必需的 **5 个基础因子（结构化 / 闭环 / 不确定性 / 一致性 / 来历）已全部实现**。
- 将欠缺的部分作为 COG-01～04 进行需求化，并在 2026-05-17 同一会话内完成了 COG-01/02/03 的实现。
- 剩下的是「现实连接」（Phase 4 IoT）与「多视角」的强化（与 CREAT-04 整合的 COG-04）。

## 为什么采用 10 因子框架

通用 LLM 的能力评估往往以「知识量」「语言流畅度」「推理精度」来谈论，但在智能体设计中，**「用哪种认知框架来切分情境」** 才更具决定性的作用。

用户观察：

> 在强化探索 / 重构之前，需要结构化 / 不确定性 / 闭环 / 一致性 / 来历这一基础。

在没有这一基础的状态下增强探索因子或重构因子，有趣的方案会增多，但误差、失控、不可复现性也会随之增多。

在这一时点，**10 个因子中的 9 个已经有既有 FR 或同日实现形成的初始映射**。但 **已有初始映射并不等于已经成熟完成**。其中「多视角」仍有强化空间，而 **尚未映射的那 1 个因子** 是「现实连接」，这部分被有意切分到 Phase 4 IoT / 实环境 integration 一侧，作为后续课题处理。

## 10 因子 × llive 映射

| # | 因子 | LLM 角色 | llive 既有（已实现） | 新增（2026-05-17 实现） |
|---|---|---|---|---|
| 1 | 结构化 | 分解课题 | Brief constraints, Salience+Curiosity gate | — |
| 2 | 重构 | 生成替代方案 | TRIZ 40 原理 + ARIZ + 9 画法（FR-23～27） | （CREAT-01 计划） |
| 3 | 闭环 | 伴随验证计划 | BriefRunner（submit→plan→approval→tool→outcome） | — |
| 4 | 自我扩展 | 使用外部资源 | 4 层记忆 + RAD 49 领域 + tools whitelist | MATH-08 计算引擎 |
| 5 | 不确定性 | 分离假设与事实 | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | 探索 | 尝试未涉足的方案 | EVO-*（Z3 + Failed Reservoir + Reverse-Evo） | — |
| 7 | 一致性 | 在整体约束下重新评估 | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | 来历 | 保留判断历史 | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | 多视角 | 分离评估函数 | Multi-track Filter A-1.5（5 EpistemicType） | （COG-04 + CREAT-04 计划） |
| 10 | 现实连接 | 处理真实环境约束 | （Phase 4 INT-01～04 计划中） | — |

## v1.0 必需的 5 个因子已全部实现

| 因子 | 实现位置 | 角色 |
|---|---|---|
| 结构化 | `src/llive/brief/types.py::Brief` + loop._salience_gate / _curiosity_drive | 分解课题 |
| 闭环 | `src/llive/brief/runner.py::BriefRunner.submit` | plan-act-check loop |
| 不确定性 | `src/llive/learning/bayesian_surprise.py`（FR-21）+ COG-01 | 假设与事实的三层分离 |
| 一致性 | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py`（EVO-04）+ COG-02 | 整体约束 + governance |
| 来历 | `src/llive/memory/provenance.py` + `src/llive/approval/ledger.py` + `src/llive/brief/ledger.py` + COG-03 | evidence/tool/decision chain |

这是 llive「具备了能在 v1.0 发布水准上防止误差、失控、不可复现性的基础」的有力证据。

## 新增 COG-01～03 的实现

### COG-01 Triple Output（强化不确定性因子）

在 `BriefResult` 中追加 3 列：

```python
@dataclass
class BriefResult:
    # ... 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` 以确定性方式计算：

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`：明示 grounding 缺失 / success_criteria 缺失
- `missing_evidence`：保存 TRIZ 原理未浮现 / tool 失败的情况

全部固定记录到 ledger 的 `outcome` event → 审计者可在事后验证。

### COG-02 Governance Scoring Layer（强化一致性因子）

在 Approval Bus 的 **前段** 插入一个 4 轴评分器：

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block を返す
```

职责分离：
- **Governance** = scoring（为什么好/坏）
- **Approval Bus** = gating（能否执行的判断）

支持 dangerous_token 检测（`rm -rf` / `DROP TABLE` / `format c:` 等）、INTERVENE-without-approval 惩罚、`block_threshold` / `safety_floor`。

### COG-03 Trace Graph（强化来历因子）

`BriefLedger.trace_graph()` 方法返回 3 层 view：

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

由此，调试、自我改进、失败分析、向 evolution 提取学习数据都可以机械化地实现。

## 横向 metadata schema

为每个记忆、每个 ledger entry 赋予统一 attribute 的设计：

```python
{
    "factor": "uncertainty",       # 10 因子のどれか
    "uncertainty": 0.23,
    "dependency": ["evidence:doc#42", "tool:sympy.simplify"],
    "evidence_source": "doc#42",
    "applicable_scope": "math:dimensional",
    "promotion_status": "candidate",
}
```

一种不依赖 LLM 自然语言规则、可被 llove TUI / audit agent / evolution scheduler 机械化消费的格式。

## 结论

作为在「制作有趣的 AI」之前「制作不会坏的 AI」的框架，10 因子是有力的指针。llive 已经实现了这 5 个基础因子的全部，从此进入了可以安心地堆叠 **重构・探索**（CREAT / EVO / TRIZ）的阶段。

## 来源

- 需求：`llive/.planning/REQUIREMENTS.md` v1.0-frame COG-FX 部分
- 实现：`src/llive/brief/governance.py`（新增）+ `src/llive/brief/ledger.py::trace_graph()`（扩展）+ `src/llive/brief/types.py::BriefResult`（扩展）
- 测试：`tests/unit/test_brief_cog.py`（16 件）— 1014 PASS / 零回归
- memory：`project_llive_cog_fx_factors.md`

---

> 出处：这是将从《心理的深层》YouTube 频道中提取的人类思考因子集合，由用户转换为「可嵌入 LLM 的形式」后进行需求化的结果。

---

# 한국어

# 「심리의 심층」10 인자로 정리하는 llive 사고층 — 이미 9/10 구현 완료

## TL;DR

- 「심리의 심층」YouTube 채널에서 추출한 **10 가지 사고 인자**(구조화・재구성・폐루프・자기확장・불확실성・탐색・정합・내력・다관점・현실접속)를 llive 의 기존 FR 에 매핑.
- v1.0 릴리스에 필수인 **토대 5 인자(구조화 / 폐루프 / 불확실성 / 정합 / 내력)는 모두 구현 완료**.
- 부족분을 COG-01～04 로 요건화하고, 2026-05-17 같은 세션 내에서 COG-01/02/03 을 구현 완료.
- 남은 것은 「현실접속」(Phase 4 IoT) 과 「다관점」의 강화(CREAT-04 와 통합하는 COG-04).

## 왜 10 인자 프레임워크인가

범용 LLM 의 능력 평가는 「지식량」「언어 유창성」「추론 정밀도」로 이야기되기 쉽지만, 에이전트 설계에서는 **「어떤 인지 프레임으로 상황을 자르는가」** 가 훨씬 결정적으로 작용합니다.

사용자 관찰:

> 탐색 / 재구성을 강화하기 전에, 구조화 / 불확실성 / 폐루프 / 정합 / 내력의 토대가 필요하다.

이것이 없는 상태에서 탐색 인자나 재구성 인자를 강하게 하면, 흥미로운 안은 늘어나지만 오차・폭주・비재현성도 늘어난다.

이 시점에서 **10 인자 중 9/10 에는 기존 FR 이나 같은 날 구현된 항목을 통한 초기 매핑이 들어가 있다**. 다만 **초기 매핑이 곧 성숙 완료를 뜻하지는 않는다**. 특히 「다관점」은 아직 강화 여지가 남아 있고, **아직 매핑되지 않은 1 인자**는 「현실접속」이며, 이것은 의도적으로 Phase 4 IoT / 실환경 integration 측의 과제로 분리해 둔다.

## 10 인자 × llive 매핑

| # | 인자 | LLM 역할 | llive 기존(구현 완료) | 추가(2026-05-17 구현) |
|---|---|---|---|---|
| 1 | 구조화 | 과제를 분해 | Brief constraints, Salience+Curiosity gate | — |
| 2 | 재구성 | 대안 생성 | TRIZ 40 원리 + ARIZ + 9 화법(FR-23～27) | (CREAT-01 계획) |
| 3 | 폐루프 | 검증 계획을 동반 | BriefRunner(submit→plan→approval→tool→outcome) | — |
| 4 | 자기확장 | 외부 자원을 사용 | 4 층 메모리 + RAD 49 분야 + tools whitelist | MATH-08 계산 엔진 |
| 5 | 불확실성 | 가설과 사실을 분리 | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | 탐색 | 미답의 안을 시도 | EVO-*(Z3 + Failed Reservoir + Reverse-Evo) | — |
| 7 | 정합 | 전체 제약으로 재평가 | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | 내력 | 판단 이력을 남김 | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | 다관점 | 평가 함수를 분리 | Multi-track Filter A-1.5(5 EpistemicType) | (COG-04 + CREAT-04 계획) |
| 10 | 현실접속 | 실환경 제약을 다룸 | (Phase 4 INT-01～04 계획 중) | — |

## v1.0 필수 5 인자는 모두 구현 완료

| 인자 | 구현 위치 | 역할 |
|---|---|---|
| 구조화 | `src/llive/brief/types.py::Brief` + loop._salience_gate / _curiosity_drive | 과제를 decompose |
| 폐루프 | `src/llive/brief/runner.py::BriefRunner.submit` | plan-act-check loop |
| 불확실성 | `src/llive/learning/bayesian_surprise.py`(FR-21) + COG-01 | 가설과 사실의 삼층 분리 |
| 정합 | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py`(EVO-04) + COG-02 | 전체 제약 + governance |
| 내력 | `src/llive/memory/provenance.py` + `src/llive/approval/ledger.py` + `src/llive/brief/ledger.py` + COG-03 | evidence/tool/decision chain |

이는 llive 가 「v1.0 릴리스 수준에서 오차・폭주・비재현성을 막는 토대를 갖추고 있다」는 강력한 근거입니다.

## 신규 COG-01～03 의 구현

### COG-01 Triple Output (불확실성 인자의 강화)

`BriefResult` 에 3 열 추가:

```python
@dataclass
class BriefResult:
    # ... 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` 가 결정론적으로 산출:

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`: grounding 부재 / success_criteria 부재를 명문화
- `missing_evidence`: TRIZ 원리가 surface 하지 않은 / tool 실패를 저장

모두 ledger 의 `outcome` event 에 고정 기록 → auditor 가 나중에 검증 가능.

### COG-02 Governance Scoring Layer (정합 인자의 강화)

Approval Bus 의 **전단** 에 4 축 스코어러를 삽입:

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block を返す
```

책무 분리:
- **Governance** = scoring (왜 좋은가/나쁜가)
- **Approval Bus** = gating (실행 가부의 판단)

dangerous_token 검출(`rm -rf` / `DROP TABLE` / `format c:` 등), INTERVENE-without-approval 페널티, `block_threshold` / `safety_floor` 를 지원.

### COG-03 Trace Graph (내력 인자의 강화)

`BriefLedger.trace_graph()` 메서드가 3 층 view 를 반환:

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

이로써 디버그・자기개선・실패분석・evolution 으로의 학습 데이터 추출이 기계적으로 가능해집니다.

## 횡단 metadata schema

각 메모리・각 ledger entry 에 통일된 attribute 를 부여하는 설계:

```python
{
    "factor": "uncertainty",       # 10 因子のどれか
    "uncertainty": 0.23,
    "dependency": ["evidence:doc#42", "tool:sympy.simplify"],
    "evidence_source": "doc#42",
    "applicable_scope": "math:dimensional",
    "promotion_status": "candidate",
}
```

LLM 의 자연어 규칙에 의존하지 않고, llove TUI / audit agent / evolution scheduler 가 기계적으로 소비할 수 있는 형식.

## 결론

「흥미로운 AI 를 만들기」 전에 「부서지지 않는 AI 를 만들기」 위한 프레임워크로서, 10 인자는 강력한 지침이 됩니다. llive 는 그 토대 5 인자를 모두 구현 완료했으며, 이제부터는 **재구성・탐색**(CREAT / EVO / TRIZ)을 안심하고 쌓을 수 있는 단계에 들어섰습니다.

## 소스

- 요건: `llive/.planning/REQUIREMENTS.md` v1.0-frame COG-FX 섹션
- 구현: `src/llive/brief/governance.py`(신규) + `src/llive/brief/ledger.py::trace_graph()`(확장) + `src/llive/brief/types.py::BriefResult`(확장)
- 테스트: `tests/unit/test_brief_cog.py`(16 건) — 1014 PASS / 회귀 제로
- memory: `project_llive_cog_fx_factors.md`

---

> 출처: 「심리의 심층」 YouTube 채널에서 추출된 인간의 사고 인자 세트를, 사용자가 「LLM 에 조립해 넣을 수 있는 형태」로 변환한 결과를 요건화한 것입니다.
