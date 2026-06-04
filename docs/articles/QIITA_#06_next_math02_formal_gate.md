---
layout: default
title: "LLM 数式幻覚をどう止めるか — 形式検証ゲート (MATH-02 設計予告)"
date: 2026-05-17
tags: [llm, math, formal-verification, z3, sympy, hallucination]
draft: true
id: acb5f5e0dabe2020c166
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# LLM 数式幻覚をどう止めるか — 形式検証ゲート (MATH-02 設計予告)

> **Status**: 設計予告。実装は MATH-02 として v0.7-vertical で着手予定。
> 本記事は llive の vertical specialisation「数学・単位特化 AI」における
> 形式検証層の設計を、SafeCalculator (MATH-08, 実装済) と組み合わせる文脈で
> 解説する。

## TL;DR

- LLM が出力した数式は文字列としては妥当でも、**等式として偽**であることが多い
- 例: `x² + x = 2x³` のような誤等式を、それっぽい文章で生成してしまう
- 解: LLM 出力を AST 化 → **Sympy で simplify → 差分を flag** → **Z3 で satisfiability check**
- これにより「LLM が言ったから正しい」ではなく「llive が検算して通った」を保証
- 既存 EVO-04 (Z3 静的検証) を数式版に拡張し、MATH-08 SafeCalculator (実装済) と連携

## なぜ単なる SafeCalculator では足りないか

[MATH-08 SafeCalculator](./03_math_vertical.md) は「式が来たら決定論的に評価する」 → これは **算術** の幻覚を止める強力な道具。

しかし、LLM がよくやる別の幻覚があります:

| 幻覚タイプ | SafeCalculator で防げるか |
|---|---|
| `(2.5 * 7.8) / 0.3 = 12.4` (実際は 65.0) | ✅ 防げる |
| `5 m/s + 3 s = 8` | ✅ 単位次元 (MATH-01) で防げる |
| `∫ x² dx = x³/3 + C` (これは正しい) | — (検算不要) |
| `(x+1)² = x² + 2x` (2x ではなく 2x+1) | ❌ 防げない — **これが MATH-02 の対象** |
| `lim x→0 sin(x)/x = 0` (実際は 1) | ❌ 防げない — Sympy 必要 |
| `det([[1,2],[3,4]]) = 0` (実際は -2) | ❌ 防げない — Sympy 必要 |
| `e^(iπ) + 1 = 2` (実際は 0) | ❌ 防げない — Sympy 必要 |

つまり、**記号操作・極限・行列・複素数** の幻覚は SafeCalculator では捕まらない。MATH-02 Sympy 検算層が必要。

## 設計

![MATH-02 形式検証ゲートのフロー: LLM 出力テキストを式抽出器で AST 化し、Sympy simplify と Z3 satisfiability check で等式の真偽を検算する](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q06/formal_gate_flow.svg)

```python
# 設計案 (実装予定)
from llive.math.formal import FormalChecker

checker = FormalChecker()
verdict = checker.check_equation("(x+1)**2", "x**2 + 2*x")
# verdict.satisfied: False
# verdict.counterexample: {"x": 0}  # 0+1=1 ≠ 0+0=0
# verdict.rationale: "differs at x=0: 1 vs 0"
```

## EVO-04 (既存) の延長線

llive は既に Phase 3 で **EVO-04 Z3 静的検証** を実装しています (構造的不変量検査用)。MATH-02 は同じ Z3 layer を **数式版** に拡張する形:

- EVO-04: 「mutation 後の sub-block が ABI 制約を満たすか」を Z3 で検証
- MATH-02: 「LLM が出した等式が満たすべき推論ステップを Z3 で検証」

つまり「形式検証 gate」のリソースを新規購入せず、既存 Phase 3 資産で拡張する経済設計。

## llive 思考層との接続

MATH-02 は COG-FX の **整合因子** を強化:

- LLM 出力 → BriefGrounder → SafeCalculator (算術) → MATH-02 (記号) → outcome
- 各段階で ledger に citation を固定記録 → COG-03 Trace Graph の evidence_chain に蓄積
- 不一致が見つかったら COG-01 missing_evidence に「Sympy: LHS ≠ RHS at x=0」と記録

## 評価ベンチマーク

- **MATH dataset** (Hendrycks 2021): 12,500 件の competition math
- **GSM8K**: 8,500 件の小学校レベル文章題
- **MMLU math subset**
- **llive 独自 EquaSafe**: LLM 幻覚 1,000 件を Sympy 検算で recall ≥99% 目標

## なぜこれが Wolfram Alpha より良いか

- Wolfram Alpha: 強力だが closed cloud, 商用、有料
- MATH-02: 完全 on-prem (Z3 + Sympy はオープンソース), 監査ログ付き, BriefLedger に固定記録
- 数学・物理・工学・金融・薬学 のすべてが「数式の正しさ」を要求する → llive の vertical 戦略の中核

## ソース (実装前)

- 既存 Z3 ベース: `src/llive/evolution/z3_checker.py` (EVO-04, Phase 3 実装済)
- 既存 SafeCalculator: `src/llive/math/calculator.py` (MATH-08, 実装済 2026-05-17)
- 要件: REQUIREMENTS.md v0.7-vertical MATH-02
- ロードマップ: Phase 10

## 完成版記事の予告

MATH-02 実装後に draft 解除し:
- LLM 数式幻覚 1000 件を Sympy 検算した recall / precision
- 反例 (counterexample) のサンプル可視化
- LLM 単独 vs llive (MATH-02 ゲート付き) の比較ベンチ結果
を追加してリリースします。

---

> 設計記事段階。実装が進んだ時点で内容を更新します。

---

# English

# How Do We Stop LLM Math Hallucinations — A Formal Verification Gate (MATH-02 Design Preview)

> **Status**: Design preview. Implementation is planned as MATH-02, to land in the v0.7-vertical track.
> This article explains the design of the formal verification layer in llive's vertical
> specialisation — the "math/unit-aware AI" — in the context of combining it with the
> already-shipped SafeCalculator (MATH-08).

## TL;DR

- A formula emitted by an LLM may be syntactically valid as a string yet **false as an equation** — and that happens a lot
- Example: it will happily generate a wrong identity like `x² + x = 2x³`, wrapped in plausible-sounding prose
- Solution: turn the LLM output into an AST → **simplify with Sympy → flag the difference** → **run a satisfiability check with Z3**
- This guarantees "llive checked the arithmetic and it passed" instead of "it's correct because the LLM said so"
- We extend the existing EVO-04 (Z3 static verification) into a formula-aware version and link it with the shipped MATH-08 SafeCalculator

## Why a Plain SafeCalculator Is Not Enough

[MATH-08 SafeCalculator](./03_math_vertical.md) evaluates "any incoming expression deterministically" → that is a powerful tool for stopping **arithmetic** hallucinations.

But there is another class of hallucination that LLMs commit all the time:

| Hallucination type | Caught by SafeCalculator? |
|---|---|
| `(2.5 * 7.8) / 0.3 = 12.4` (actually 65.0) | ✅ Caught |
| `5 m/s + 3 s = 8` | ✅ Caught by dimensional units (MATH-01) |
| `∫ x² dx = x³/3 + C` (this one is correct) | — (no check needed) |
| `(x+1)² = x² + 2x` (it's 2x+1, not 2x) | ❌ Not caught — **this is the target of MATH-02** |
| `lim x→0 sin(x)/x = 0` (actually 1) | ❌ Not caught — needs Sympy |
| `det([[1,2],[3,4]]) = 0` (actually -2) | ❌ Not caught — needs Sympy |
| `e^(iπ) + 1 = 2` (actually 0) | ❌ Not caught — needs Sympy |

In other words, hallucinations involving **symbolic manipulation, limits, matrices, or complex numbers** are not caught by SafeCalculator. We need the MATH-02 Sympy verification layer.

## Design

![Flow of the MATH-02 formal verification gate: the formula extractor turns the LLM output text into an AST, then Sympy simplify and a Z3 satisfiability check verify whether the equation is true](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q06/formal_gate_flow_en.svg)

```python
# 設計案 (実装予定)
from llive.math.formal import FormalChecker

checker = FormalChecker()
verdict = checker.check_equation("(x+1)**2", "x**2 + 2*x")
# verdict.satisfied: False
# verdict.counterexample: {"x": 0}  # 0+1=1 ≠ 0+0=0
# verdict.rationale: "differs at x=0: 1 vs 0"
```

## An Extension of the Existing EVO-04

llive already implemented **EVO-04 Z3 static verification** in Phase 3 (for structural-invariant checking). MATH-02 extends the same Z3 layer into a **formula-aware version**:

- EVO-04: verifies with Z3 whether "a post-mutation sub-block satisfies the ABI constraints"
- MATH-02: verifies with Z3 whether "an equation emitted by the LLM satisfies the inference step it should"

So we extend the "formal verification gate" using existing Phase 3 assets rather than buying new resources — an economical design.

## Connection to llive's Thinking Layers

MATH-02 reinforces the **coherence factor** of COG-FX:

- LLM output → BriefGrounder → SafeCalculator (arithmetic) → MATH-02 (symbolic) → outcome
- At each stage a citation is pinned into the ledger → accumulated in the evidence_chain of the COG-03 Trace Graph
- When a mismatch is found, it is recorded in COG-01 missing_evidence as "Sympy: LHS ≠ RHS at x=0"

## Evaluation Benchmarks

- **MATH dataset** (Hendrycks 2021): 12,500 competition-math problems
- **GSM8K**: 8,500 grade-school word problems
- **MMLU math subset**
- **llive's own EquaSafe**: 1,000 LLM hallucinations, targeting recall ≥99% via Sympy verification

## Why This Is Better Than Wolfram Alpha

- Wolfram Alpha: powerful, but a closed cloud — commercial and paid
- MATH-02: fully on-prem (Z3 + Sympy are open source), with an audit log, pinned into the BriefLedger
- Mathematics, physics, engineering, finance, and pharmacology all demand "correctness of formulas" → this is the core of llive's vertical strategy

## Sources (Pre-Implementation)

- Existing Z3 base: `src/llive/evolution/z3_checker.py` (EVO-04, shipped in Phase 3)
- Existing SafeCalculator: `src/llive/math/calculator.py` (MATH-08, shipped 2026-05-17)
- Requirements: REQUIREMENTS.md v0.7-vertical MATH-02
- Roadmap: Phase 10

## Preview of the Finished Article

After MATH-02 is implemented we will lift the draft flag and add:
- recall / precision from running Sympy verification over 1,000 LLM math hallucinations
- a visualization of sample counterexamples
- comparative benchmark results of LLM alone vs llive (with the MATH-02 gate)
and then release it.

---

> This is at the design-article stage. We will update the content as implementation progresses.

---

# 中文

# 如何阻止 LLM 的数式幻觉 —— 形式化验证门 (MATH-02 设计预告)

> **Status**: 设计预告。实现将作为 MATH-02 在 v0.7-vertical 中着手。
> 本文在与已实现的 SafeCalculator (MATH-08) 相结合的语境下，
> 讲解 llive 垂直专精化「数学・单位特化 AI」中形式化验证层的设计。

## TL;DR

- LLM 输出的数式作为字符串也许合法，但**作为等式却往往是假的**
- 例如：会用看似像模像样的文字生成 `x² + x = 2x³` 这类错误等式
- 解法：将 LLM 输出转为 AST → **用 Sympy simplify → 标记差异** → **用 Z3 做可满足性检查**
- 由此保证的不是「因为 LLM 说了所以正确」，而是「llive 核算通过了」
- 将既有的 EVO-04 (Z3 静态验证) 扩展为数式版，并与已实现的 MATH-08 SafeCalculator 联动

## 为什么单靠 SafeCalculator 还不够

[MATH-08 SafeCalculator](./03_math_vertical.md) 是「来了表达式就确定性地求值」→ 这是阻止**算术**幻觉的强力工具。

然而，LLM 常犯另一类幻觉：

| 幻觉类型 | SafeCalculator 能否防住 |
|---|---|
| `(2.5 * 7.8) / 0.3 = 12.4` (实际是 65.0) | ✅ 能防 |
| `5 m/s + 3 s = 8` | ✅ 用单位量纲 (MATH-01) 能防 |
| `∫ x² dx = x³/3 + C` (这是正确的) | — (无需核算) |
| `(x+1)² = x² + 2x` (应是 2x+1 而非 2x) | ❌ 防不住 —— **这正是 MATH-02 的对象** |
| `lim x→0 sin(x)/x = 0` (实际是 1) | ❌ 防不住 —— 需要 Sympy |
| `det([[1,2],[3,4]]) = 0` (实际是 -2) | ❌ 防不住 —— 需要 Sympy |
| `e^(iπ) + 1 = 2` (实际是 0) | ❌ 防不住 —— 需要 Sympy |

也就是说，**符号运算・极限・矩阵・复数** 的幻觉无法被 SafeCalculator 抓住。需要 MATH-02 Sympy 核算层。

## 设计

![MATH-02 形式化验证门的流程: 用式抽取器将 LLM 输出文本转为 AST, 再用 Sympy simplify 与 Z3 可满足性检查核算等式真伪](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q06/formal_gate_flow_zh.svg)

```python
# 設計案 (実装予定)
from llive.math.formal import FormalChecker

checker = FormalChecker()
verdict = checker.check_equation("(x+1)**2", "x**2 + 2*x")
# verdict.satisfied: False
# verdict.counterexample: {"x": 0}  # 0+1=1 ≠ 0+0=0
# verdict.rationale: "differs at x=0: 1 vs 0"
```

## EVO-04 (既有) 的延长线

llive 已经在 Phase 3 实现了 **EVO-04 Z3 静态验证** (用于结构性不变量检查)。MATH-02 是将同一个 Z3 layer 扩展为**数式版**的形态：

- EVO-04：用 Z3 验证「mutation 之后的 sub-block 是否满足 ABI 约束」
- MATH-02：用 Z3 验证「LLM 给出的等式是否满足它应当满足的推理步骤」

也就是说，不必新购「形式化验证 gate」的资源，而是用既有 Phase 3 资产来扩展的经济型设计。

## 与 llive 思考层的衔接

MATH-02 强化 COG-FX 的**整合因子**：

- LLM 输出 → BriefGrounder → SafeCalculator (算术) → MATH-02 (符号) → outcome
- 在每个阶段将 citation 固定记录到 ledger → 累积进 COG-03 Trace Graph 的 evidence_chain
- 一旦发现不一致，就在 COG-01 missing_evidence 中记下「Sympy: LHS ≠ RHS at x=0」

## 评测基准

- **MATH dataset** (Hendrycks 2021)：12,500 道竞赛数学题
- **GSM8K**：8,500 道小学水平应用题
- **MMLU math subset**
- **llive 自有 EquaSafe**：将 1,000 个 LLM 幻觉用 Sympy 核算，目标 recall ≥99%

## 为什么这比 Wolfram Alpha 更好

- Wolfram Alpha：很强大，但是封闭云端、商业、收费
- MATH-02：完全 on-prem (Z3 + Sympy 是开源)，带审计日志，固定记录到 BriefLedger
- 数学・物理・工程・金融・药学 全都要求「数式的正确性」→ 这是 llive 垂直战略的核心

## 来源 (实现前)

- 既有 Z3 基础：`src/llive/evolution/z3_checker.py` (EVO-04, Phase 3 已实现)
- 既有 SafeCalculator：`src/llive/math/calculator.py` (MATH-08, 已于 2026-05-17 实现)
- 需求：REQUIREMENTS.md v0.7-vertical MATH-02
- 路线图：Phase 10

## 完成版文章的预告

MATH-02 实现后将解除 draft，并追加：
- 将 1,000 个 LLM 数式幻觉用 Sympy 核算后的 recall / precision
- 反例 (counterexample) 的样例可视化
- LLM 单独 vs llive (带 MATH-02 门) 的对比基准结果
之后再发布。

---

> 处于设计文章阶段。实现推进到一定程度后将更新内容。

---

# 한국어

# LLM 수식 환각을 어떻게 멈출 것인가 — 형식 검증 게이트 (MATH-02 설계 예고)

> **Status**: 설계 예고. 구현은 MATH-02 로서 v0.7-vertical 에서 착수 예정.
> 본 글은 llive 의 vertical 특화「수학・단위 특화 AI」에서의
> 형식 검증 층 설계를, 이미 구현된 SafeCalculator (MATH-08) 와 결합하는
> 맥락에서 해설한다.

## TL;DR

- LLM 이 출력한 수식은 문자열로서는 타당해도 **등식으로서는 거짓**인 경우가 많다
- 예: `x² + x = 2x³` 같은 잘못된 등식을, 그럴듯한 문장으로 생성해 버린다
- 해법: LLM 출력을 AST 화 → **Sympy 로 simplify → 차이를 flag** → **Z3 로 satisfiability check**
- 이로써 「LLM 이 말했으니 옳다」가 아니라 「llive 가 검산해서 통과했다」를 보장
- 기존 EVO-04 (Z3 정적 검증) 를 수식 버전으로 확장하고, MATH-08 SafeCalculator (구현 완료) 와 연계

## 왜 단순한 SafeCalculator 로는 부족한가

[MATH-08 SafeCalculator](./03_math_vertical.md) 는 「식이 오면 결정론적으로 평가한다」 → 이것은 **산술** 환각을 멈추는 강력한 도구.

그러나 LLM 이 자주 저지르는 또 다른 환각이 있습니다:

| 환각 유형 | SafeCalculator 로 막을 수 있는가 |
|---|---|
| `(2.5 * 7.8) / 0.3 = 12.4` (실제는 65.0) | ✅ 막을 수 있음 |
| `5 m/s + 3 s = 8` | ✅ 단위 차원 (MATH-01) 으로 막을 수 있음 |
| `∫ x² dx = x³/3 + C` (이것은 옳음) | — (검산 불필요) |
| `(x+1)² = x² + 2x` (2x 가 아니라 2x+1) | ❌ 막을 수 없음 — **이것이 MATH-02 의 대상** |
| `lim x→0 sin(x)/x = 0` (실제는 1) | ❌ 막을 수 없음 — Sympy 필요 |
| `det([[1,2],[3,4]]) = 0` (실제는 -2) | ❌ 막을 수 없음 — Sympy 필요 |
| `e^(iπ) + 1 = 2` (실제는 0) | ❌ 막을 수 없음 — Sympy 필요 |

즉, **기호 조작・극한・행렬・복소수** 의 환각은 SafeCalculator 로는 잡히지 않는다. MATH-02 Sympy 검산 층이 필요.

## 설계

```
LLM 출력 텍스트
    │
    ▼
[식 추출기] (MATH-03 multi-syntax parser, LaTeX/MathML/Sympy)
    │
    ▼
[Sympy AST]
    │
    ├─→ simplify(lhs - rhs) == 0 ? → ✅ 통과
    │   ❌ → 실패 flag
    │
    └─→ Z3 로 satisfiability check (∀ x. lhs(x) == rhs(x) ?)
        ❌ → 반례를 ledger 에 기록
```

```python
# 設計案 (実装予定)
from llive.math.formal import FormalChecker

checker = FormalChecker()
verdict = checker.check_equation("(x+1)**2", "x**2 + 2*x")
# verdict.satisfied: False
# verdict.counterexample: {"x": 0}  # 0+1=1 ≠ 0+0=0
# verdict.rationale: "differs at x=0: 1 vs 0"
```

## EVO-04 (기존) 의 연장선

llive 는 이미 Phase 3 에서 **EVO-04 Z3 정적 검증** 을 구현했습니다 (구조적 불변량 검사용). MATH-02 는 같은 Z3 layer 를 **수식 버전**으로 확장하는 형태:

- EVO-04: 「mutation 후의 sub-block 이 ABI 제약을 충족하는가」를 Z3 로 검증
- MATH-02: 「LLM 이 내놓은 등식이 충족해야 할 추론 스텝을 Z3 로 검증」

즉, 「형식 검증 gate」의 리소스를 신규 구매하지 않고, 기존 Phase 3 자산으로 확장하는 경제적 설계.

## llive 사고 층과의 접속

MATH-02 는 COG-FX 의 **정합 인자** 를 강화:

- LLM 출력 → BriefGrounder → SafeCalculator (산술) → MATH-02 (기호) → outcome
- 각 단계에서 ledger 에 citation 을 고정 기록 → COG-03 Trace Graph 의 evidence_chain 에 축적
- 불일치가 발견되면 COG-01 missing_evidence 에「Sympy: LHS ≠ RHS at x=0」라고 기록

## 평가 벤치마크

- **MATH dataset** (Hendrycks 2021): 12,500 건의 competition math
- **GSM8K**: 8,500 건의 초등학교 수준 문장제
- **MMLU math subset**
- **llive 자체 EquaSafe**: LLM 환각 1,000 건을 Sympy 검산으로 recall ≥99% 목표

## 왜 이것이 Wolfram Alpha 보다 좋은가

- Wolfram Alpha: 강력하지만 closed cloud, 상용, 유료
- MATH-02: 완전 on-prem (Z3 + Sympy 는 오픈소스), 감사 로그 포함, BriefLedger 에 고정 기록
- 수학・물리・공학・금융・약학 의 모든 것이 「수식의 정확성」을 요구한다 → llive 의 vertical 전략의 핵심

## 소스 (구현 전)

- 기존 Z3 기반: `src/llive/evolution/z3_checker.py` (EVO-04, Phase 3 구현 완료)
- 기존 SafeCalculator: `src/llive/math/calculator.py` (MATH-08, 2026-05-17 구현 완료)
- 요건: REQUIREMENTS.md v0.7-vertical MATH-02
- 로드맵: Phase 10

## 완성판 글의 예고

MATH-02 구현 후 draft 를 해제하고:
- LLM 수식 환각 1000 건을 Sympy 검산한 recall / precision
- 반례 (counterexample) 의 샘플 시각화
- LLM 단독 vs llive (MATH-02 게이트 포함) 의 비교 벤치 결과
를 추가하여 릴리스합니다.

---

> 설계 글 단계. 구현이 진행된 시점에 내용을 갱신합니다.
