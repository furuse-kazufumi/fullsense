---
layout: default
title: "数学・単位に強い AI を作る最初の一歩"
date: 2026-05-17
tags: [llm, math, units, dimensional-analysis, hallucination]
id: 2c4a993937c373c464f6
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 数学・単位に強い AI を作る最初の一歩 — MATH-01/08 内蔵計算エンジン

> 📚 **連載ナビ**: ← #01 [Brief API 設計と progressive matrix](./QIITA_#01_brief_api_progressive.md) / #02 [10 思考因子で整理する思考層](./QIITA_#02_cognitive_factors.md) ｜ **#03 本記事**（最初の vertical = 数学・単位）｜ #06 [LLM 数式幻覚をどう止めるか](./QIITA_#06_next_math02_formal_gate.md) →。※ 各記事は単独でも読めます。
>
> #01 で Brief という入口を、#02 でその上を流れる思考因子を見た。本記事では、その入口に **最初の専門分野** を載せる——数学と単位だ。なぜ汎用 LLM が `5 m/s + 3 s = 8` を平然と書いてしまうのか、そこから始める。

## TL;DR

- llive 最初の specialised vertical として「**数学・単位特化 AI**」を選定 (ユーザー戦略指示)
- 汎用 LLM が苦手な (a) 記号操作の幻覚 (b) 単位次元の取り違え (c) 数値計算の error propagation を **「LLM に計算させない」決定論的サイドカー** で克服
- 2026-05-17 同セッションで **MATH-01 (SI 単位次元解析)** + **MATH-08 (内蔵計算エンジン = 差別化軸)** の minimal skeleton を実装、47 件テスト追加
- `5 m/s + 3 s = 8` のような **次元不一致を検知したら、確実に拒否する** API (検知できる範囲では決定論的に止まる)

## 動機 — 汎用 LLM の数学的弱点

LLM は言語的に妥当な数式を生成しますが、以下が苦手:

| 観点 | 汎用 LLM の弱点 | llive 既存資産との合致 |
|---|---|---|
| 記号操作の幻覚 | `x² + x = 2x³` のような誤等式 | EVO-04 Z3 静的検証で gate |
| 単位次元 | `5 m/s + 3 s = 8` | SI 次元解析エンジン (MATH-01) |
| 数値精度 | float 演算誤差を無視 | error propagation tracking (MATH-04) |
| 公理体系 | 暗黙の前提を混入 | EpistemicType=MATHEMATICAL の strict track |
| 引用の信頼性 | "CODATA value is X" と適当に答える | RAD math/metrology + provenance |

## MATH-01 — SI 7 基本単位 + 派生単位の次元代数

最小依存版を自前実装 (Pint 等の外部ライブラリ不要)。

```python
from llive.math import Quantity, parse_unit, UnitMismatchError

# 速度 + 時間 = 不可能 (典型的 LLM 幻覚)
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t
assert d.dimensions.matches(parse_unit("m"))

# 力 × 距離 = エネルギー (J)
F = Quantity(10.0, parse_unit("N"))
d = Quantity(5.0, parse_unit("m"))
E = F * d
assert E.dimensions.matches(parse_unit("J"))  # ✓ Joule
```

実装の核は `Dimensions(m, kg, s, A, K, mol, cd)` の 7 次元ベクトル。演算は次元の加減算 (積/除)。`Quantity.__add__` で次元検算 → 不一致は **必ず raise**。

### 派生単位

`N` (kg·m/s²) / `J` (kg·m²/s²) / `W` (kg·m²/s³) / `Pa` (kg/m/s²) / `Hz` (1/s) / `C` (s·A) / `V` (kg·m²/s³/A) / `ohm` を頻出範囲のみ実装。

## MATH-08 — 内蔵計算エンジン (差別化の中核)

**設計の核**: LLM に **数値計算をさせない**。

```python
from llive.math import SafeCalculator, extract_expressions

calc = SafeCalculator()
brief_text = "Compute (2.5 * 7.8) / 0.3 then verify sqrt(16) is exact."

for expr in extract_expressions(brief_text):
    r = calc.evaluate(expr)
    print(f"{r.expression} = {r.value}  (ops={r.operation_count}, fns={r.used_functions})")
# (2.5 * 7.8) / 0.3 = 65.0   (ops=2, fns=())
# sqrt(16)          = 4.0    (ops=1, fns=('sqrt',))
```

### Safety の意味

`Safe` の制約:

- `eval()` は使わない (任意コード実行回避)
- AST visitor で許可ノード (`BinOp` / `UnaryOp` / `Constant` / `Call` to whitelist) のみ通す
- 関数 whitelist: `sqrt` / `sin` / `cos` / `log` / `abs` / `mean` / ... (math + statistics モジュールから 28 関数)
- 定数 whitelist: `pi` / `e` / `tau` / `inf` / `nan`
- 0 除算は `CalculationError` で安全に reject
- `__import__('os').system('rm')` などの攻撃チェーンを attribute access 段階で reject

### Brief への grounding

Brief の goal に算術式が含まれていれば、`extract_expressions()` が抽出 → `SafeCalculator` が決定論的に評価 → 結果を **grounded Stimulus** として注入する設計:

```
Brief.goal にある式 → SafeCalculator が評価 → 結果が augmented goal に追加 → ledger に固定記録 → LLM はそれを「事実」として参照するだけ
```

LLM が計算する → 浮動小数点幻覚、桁落ち
llive が計算する → IEEE 754 精度、再現可能、引用可能

## なぜこれを最初の差別化軸に選んだか

- 汎用 LLM (GPT / Claude / Gemini) は「LLM が計算する」設計。llive は「LLM の出力を **検証**し、必要なら **再計算** する」設計を取った——どちらが優れているかは用途次第で、ここでは設計思想の違いとして示す
- Wolfram Alpha は強力な計算エンジンだが closed cloud。llive は完全 on-prem。この差が効くかは、データを外に出せるかどうかという制約次第
- 数学・物理・工学・金融・薬学 すべてが「単位次元」と「精密計算」を必要とする → 最初の vertical として適用範囲が広く、検証する価値があると判断した

## v0.7-vertical MATH の 8 件全要件

| FR | 名前 | 優先 |
|---|---|---|
| MATH-01 | SI 単位次元解析エンジン | ✅ 1st 実装済 |
| MATH-02 | Z3 / Sympy 統合検証層 | 2nd |
| MATH-05 | 物理定数辞書 (CODATA 2022 + NIST) | 3rd |
| **MATH-08** | **内蔵計算エンジン (差別化軸)** | ✅ 4th 実装済 |
| MATH-03 | 数式構文解析 (LaTeX/MathML/Sympy AST) | MED |
| MATH-04 | 数値計算精度トラッキング (IEEE 754) | MED |
| MATH-06 | 単位変換 + Buckingham π 無次元化 | MED |
| MATH-07 | MATHEMATICAL EpistemicType | MED |

## 評価ベンチマーク (vertical 専用)

- **MMLU math** subset
- **GSM8K / MATH** dataset
- **PhysicsBench** (物理単位問題)
- **DimSafe**: llive 独自テストセット — 単位次元誤りを含む 1000 件で recall ≥99 %, precision ≥95 %

## ソース

- 実装: `llive/src/llive/math/units.py` + `calculator.py`
- 公開 API: `from llive.math import Quantity, parse_unit, SafeCalculator, extract_expressions`
- テスト: `tests/unit/test_math_units.py` (22 件) + `tests/unit/test_math_calculator.py` (24 件)
- 全 1014 PASS / 回帰ゼロ

## 残った問い — 「計算させない」で十分か

ここまでは「LLM に **計算させない**」設計だった。算術式を奪い取って決定論エンジンに渡せば、`5 m/s + 3 s` は止まる。だが LLM が吐くのは数値だけではない。`x² + x = 2x³` のような **誤った数式そのもの** を、もっともらしい言葉で書いてきたら? 式を奪う前に、その式が正しいかどうかを機械的に反証できなければ、検証は片肺だ。

次回 **#06「[LLM 数式幻覚をどう止めるか — 形式検証ゲート](./QIITA_#06_next_math02_formal_gate.md)」** では、MATH-02 を解剖する。LLM が出した数式を Sympy で AST 化し、矛盾を機械的に flag する仕組み——今回の「計算をさせない」から、「出力を反証する」へ一歩進む。式を信じる前に、式を疑う側のエンジンを作りにいく。

（手元の作業としては、BriefGrounder への `SafeCalculator` 統合で Brief 投入時に式を自動 ground し、MATH-05 CODATA 辞書を RAD `metrology` 分野へ append する整備も並走している。）

---

> FullSense ™ の最初の vertical specialisation。「数学に強い AI」を最初のキラー応用として育てる戦略。

---

# English

# The First Step Toward an AI That Is Strong at Math and Units — The MATH-01/08 Built-in Calculation Engine

> 📚 **Series nav**: ← #01 [Brief API design and the progressive matrix](./QIITA_#01_brief_api_progressive.md) / #02 [Organizing the thinking layer with 10 cognitive factors](./QIITA_#02_cognitive_factors.md) ｜ **#03 This article** (the first vertical = math & units) ｜ #06 [How do we stop LLM math hallucinations](./QIITA_#06_next_math02_formal_gate.md) →. ※ Each article stands on its own.
>
> In #01 we looked at the Brief as an entry point, and in #02 at the cognitive factors that flow over it. In this article we put the **first specialised field** onto that entry point — math and units. We start from the question of why a general-purpose LLM will calmly write `5 m/s + 3 s = 8`.

## TL;DR

- As llive's first specialised vertical, we chose a "**math- and unit-focused AI**" (per the user's strategic direction)
- We overcome the three things general-purpose LLMs are bad at — (a) hallucinated symbolic manipulation, (b) confusing unit dimensions, (c) error propagation in numerical computation — with a **deterministic sidecar that does not let the LLM do the calculation**
- In the same 2026-05-17 session we implemented the minimal skeletons of **MATH-01 (SI unit dimensional analysis)** + **MATH-08 (built-in calculation engine = the differentiation axis)**, adding 47 tests
- An API that, **once it detects a dimensional mismatch like `5 m/s + 3 s = 8`, reliably refuses it** (deterministically, within the range it can detect)

## Motivation — The Mathematical Weaknesses of General-Purpose LLMs

LLMs generate linguistically plausible formulas, but they are bad at the following:

| Aspect | Weakness of general-purpose LLM | Match with llive's existing assets |
|---|---|---|
| Hallucinated symbolic manipulation | False equalities like `x² + x = 2x³` | Gated by EVO-04 Z3 static verification |
| Unit dimensions | `5 m/s + 3 s = 8` | SI dimensional analysis engine (MATH-01) |
| Numerical precision | Ignoring float arithmetic errors | error propagation tracking (MATH-04) |
| Axiomatic systems | Mixing in implicit premises | strict track of EpistemicType=MATHEMATICAL |
| Reliability of citations | Answering "CODATA value is X" off the cuff | RAD math/metrology + provenance |

## MATH-01 — Dimensional Algebra of the 7 SI Base Units + Derived Units

Implemented in-house as a minimal-dependency version (no external libraries such as Pint required).

```python
from llive.math import Quantity, parse_unit, UnitMismatchError

# 速度 + 時間 = 不可能 (典型的 LLM 幻覚)
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t
assert d.dimensions.matches(parse_unit("m"))

# 力 × 距離 = エネルギー (J)
F = Quantity(10.0, parse_unit("N"))
d = Quantity(5.0, parse_unit("m"))
E = F * d
assert E.dimensions.matches(parse_unit("J"))  # ✓ Joule
```

The core of the implementation is the 7-dimensional vector `Dimensions(m, kg, s, A, K, mol, cd)`. Operations are addition/subtraction of dimensions (for product/division). In `Quantity.__add__`, the dimensions are checked → on mismatch it **always raises**.

### Derived Units

`N` (kg·m/s²) / `J` (kg·m²/s²) / `W` (kg·m²/s³) / `Pa` (kg/m/s²) / `Hz` (1/s) / `C` (s·A) / `V` (kg·m²/s³/A) / `ohm` — only the frequently-used range is implemented.

## MATH-08 — Built-in Calculation Engine (Core of the Differentiation)

**Core of the design**: do **not** let the LLM do the numerical computation.

```python
from llive.math import SafeCalculator, extract_expressions

calc = SafeCalculator()
brief_text = "Compute (2.5 * 7.8) / 0.3 then verify sqrt(16) is exact."

for expr in extract_expressions(brief_text):
    r = calc.evaluate(expr)
    print(f"{r.expression} = {r.value}  (ops={r.operation_count}, fns={r.used_functions})")
# (2.5 * 7.8) / 0.3 = 65.0   (ops=2, fns=())
# sqrt(16)          = 4.0    (ops=1, fns=('sqrt',))
```

### What "Safe" Means

Constraints of `Safe`:

- Does not use `eval()` (avoids arbitrary code execution)
- An AST visitor allows only permitted nodes (`BinOp` / `UnaryOp` / `Constant` / `Call` to whitelist)
- Function whitelist: `sqrt` / `sin` / `cos` / `log` / `abs` / `mean` / ... (28 functions from the math + statistics modules)
- Constant whitelist: `pi` / `e` / `tau` / `inf` / `nan`
- Division by zero is safely rejected with `CalculationError`
- Attack chains like `__import__('os').system('rm')` are rejected at the attribute-access stage

### Grounding to the Brief

If the goal of a Brief contains an arithmetic expression, `extract_expressions()` extracts it → `SafeCalculator` evaluates it deterministically → the result is injected as a **grounded Stimulus**:

```
Brief.goal にある式 → SafeCalculator が評価 → 結果が augmented goal に追加 → ledger に固定記録 → LLM はそれを「事実」として参照するだけ
```

LLM computes → floating-point hallucinations, loss of significance
llive computes → IEEE 754 precision, reproducible, citable

## Why We Chose This as the First Differentiation Axis

- General-purpose LLMs (GPT / Claude / Gemini) are designed so that "the LLM computes." llive took the design where it "**verifies** the LLM's output and, if necessary, **recomputes** it" — which is better depends on the use case, so we present it here as a difference in design philosophy
- Wolfram Alpha is a powerful calculation engine but a closed cloud. llive is fully on-prem. Whether that difference matters depends on the constraint of whether you can send your data outside
- Math, physics, engineering, finance, and pharmacy all need "unit dimensions" and "precise computation" → as the first vertical it has a broad range of applicability, which is why we judged it worth validating first

## All 8 Requirements of v0.7-vertical MATH

| FR | Name | Priority |
|---|---|---|
| MATH-01 | SI unit dimensional analysis engine | ✅ implemented 1st |
| MATH-02 | Z3 / Sympy integrated verification layer | 2nd |
| MATH-05 | Physical constants dictionary (CODATA 2022 + NIST) | 3rd |
| **MATH-08** | **Built-in calculation engine (differentiation axis)** | ✅ implemented 4th |
| MATH-03 | Formula parsing (LaTeX/MathML/Sympy AST) | MED |
| MATH-04 | Numerical precision tracking (IEEE 754) | MED |
| MATH-06 | Unit conversion + Buckingham π non-dimensionalization | MED |
| MATH-07 | MATHEMATICAL EpistemicType | MED |

## Evaluation Benchmarks (Vertical-Specific)

- **MMLU math** subset
- **GSM8K / MATH** dataset
- **PhysicsBench** (physics unit problems)
- **DimSafe**: llive's own test set — 1000 items containing unit-dimension errors, targeting recall ≥99 %, precision ≥95 %

## Sources

- Implementation: `llive/src/llive/math/units.py` + `calculator.py`
- Public API: `from llive.math import Quantity, parse_unit, SafeCalculator, extract_expressions`
- Tests: `tests/unit/test_math_units.py` (22 items) + `tests/unit/test_math_calculator.py` (24 items)
- All 1014 PASS / zero regressions

## The Question That Remains — Is "Don't Let It Compute" Enough?

So far the design has been to **not let the LLM compute**. Snatch the arithmetic expression away, hand it to a deterministic engine, and `5 m/s + 3 s` is stopped. But numbers are not the only thing an LLM emits. What if it writes out a **wrong formula itself**, like `x² + x = 2x³`, dressed up in plausible words? If we cannot mechanically disprove whether a formula is correct before we take it away, the verification is running on one lung.

In the next article, **#06 "[How Do We Stop LLM Math Hallucinations — A Formal Verification Gate](./QIITA_#06_next_math02_formal_gate.md)"**, we dissect MATH-02: the machinery that turns the LLM's emitted formula into an AST with Sympy and mechanically flags contradictions — a step forward from this article's "don't let it compute" toward "disprove the output." Before trusting a formula, we go build the engine that doubts it.

(As ongoing hands-on work, integrating `SafeCalculator` into BriefGrounder so expressions are auto-grounded the moment a Brief is submitted, and appending the MATH-05 CODATA dictionary to the RAD `metrology` field, are also running in parallel.)

---

> FullSense ™'s first vertical specialisation. The strategy is to grow an "AI that is strong at math" as the first killer application.

---

# 中文

# 打造在数学与单位上很强的 AI 的第一步 — MATH-01/08 内置计算引擎

> 📚 **连载导航**: ← #01 [Brief API 设计与 progressive matrix](./QIITA_#01_brief_api_progressive.md) / #02 [用 10 思考因子梳理思考层](./QIITA_#02_cognitive_factors.md) ｜ **#03 本文**（第一个 vertical = 数学与单位）｜ #06 [如何阻止 LLM 的数式幻觉](./QIITA_#06_next_math02_formal_gate.md) →。※ 每篇文章均可单独阅读。
>
> 在 #01 我们看了 Brief 这个入口，在 #02 看了流经其上的思考因子。本文则在这个入口上装载 **第一个专门领域**——数学与单位。我们从一个问题开始：为何通用 LLM 会若无其事地写出 `5 m/s + 3 s = 8`。

## TL;DR

- 作为 llive 的第一个专门化纵向 (specialised vertical)，我们选择了「**数学与单位特化 AI**」(依据用户的战略指示)
- 通用 LLM 不擅长的 (a) 符号操作的幻觉 (b) 单位量纲的混淆 (c) 数值计算中的误差传播，我们用一个**不让 LLM 进行计算的确定性旁车 (sidecar)** 来克服
- 在 2026-05-17 的同一会话中，我们实现了 **MATH-01 (SI 单位量纲分析)** + **MATH-08 (内置计算引擎 = 差异化轴)** 的最小骨架，并新增了 47 个测试
- 一个**一旦检测到 `5 m/s + 3 s = 8` 这类量纲不一致，就会确定性地拒绝** 的 API（在可检测的范围内确定性地阻止）

## 动机 — 通用 LLM 的数学弱点

LLM 能生成在语言上合理的数学式，但不擅长以下几点:

| 观点 | 通用 LLM 的弱点 | 与 llive 既有资产的契合 |
|---|---|---|
| 符号操作的幻觉 | 像 `x² + x = 2x³` 这样的错误等式 | 由 EVO-04 Z3 静态验证把关 |
| 单位量纲 | `5 m/s + 3 s = 8` | SI 量纲分析引擎 (MATH-01) |
| 数值精度 | 忽视 float 运算误差 | error propagation tracking (MATH-04) |
| 公理体系 | 混入隐含的前提 | EpistemicType=MATHEMATICAL 的 strict track |
| 引用的可信度 | 随口回答「CODATA value is X」 | RAD math/metrology + provenance |

## MATH-01 — SI 7 个基本单位 + 导出单位的量纲代数

自行实现了最小依赖版 (无需 Pint 等外部库)。

```python
from llive.math import Quantity, parse_unit, UnitMismatchError

# 速度 + 時間 = 不可能 (典型的 LLM 幻覚)
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t
assert d.dimensions.matches(parse_unit("m"))

# 力 × 距離 = エネルギー (J)
F = Quantity(10.0, parse_unit("N"))
d = Quantity(5.0, parse_unit("m"))
E = F * d
assert E.dimensions.matches(parse_unit("J"))  # ✓ Joule
```

实现的核心是 `Dimensions(m, kg, s, A, K, mol, cd)` 这个 7 维向量。运算就是量纲的加减 (对应乘/除)。在 `Quantity.__add__` 中进行量纲校验 → 不一致时**必定 raise**。

### 导出单位

`N` (kg·m/s²) / `J` (kg·m²/s²) / `W` (kg·m²/s³) / `Pa` (kg/m/s²) / `Hz` (1/s) / `C` (s·A) / `V` (kg·m²/s³/A) / `ohm` — 只实现了高频范围。

## MATH-08 — 内置计算引擎 (差异化的核心)

**设计的核心**: **不让** LLM 做数值计算。

```python
from llive.math import SafeCalculator, extract_expressions

calc = SafeCalculator()
brief_text = "Compute (2.5 * 7.8) / 0.3 then verify sqrt(16) is exact."

for expr in extract_expressions(brief_text):
    r = calc.evaluate(expr)
    print(f"{r.expression} = {r.value}  (ops={r.operation_count}, fns={r.used_functions})")
# (2.5 * 7.8) / 0.3 = 65.0   (ops=2, fns=())
# sqrt(16)          = 4.0    (ops=1, fns=('sqrt',))
```

### Safety 的含义

`Safe` 的约束:

- 不使用 `eval()` (避免任意代码执行)
- AST visitor 只放行被许可的节点 (`BinOp` / `UnaryOp` / `Constant` / `Call` to whitelist)
- 函数 whitelist: `sqrt` / `sin` / `cos` / `log` / `abs` / `mean` / ... (来自 math + statistics 模块的 28 个函数)
- 常量 whitelist: `pi` / `e` / `tau` / `inf` / `nan`
- 除以零会以 `CalculationError` 被安全地 reject
- 像 `__import__('os').system('rm')` 这样的攻击链会在 attribute access 阶段被 reject

### 对 Brief 的 grounding

如果 Brief 的 goal 中包含算术式，`extract_expressions()` 会抽取出来 → `SafeCalculator` 进行确定性求值 → 将结果作为 **grounded Stimulus** 注入的设计:

```
Brief.goal にある式 → SafeCalculator が評価 → 結果が augmented goal に追加 → ledger に固定記録 → LLM はそれを「事実」として参照するだけ
```

LLM 计算 → 浮点幻觉、有效位丢失
llive 计算 → IEEE 754 精度、可复现、可引用

## 为何我们把它选为第一个差异化轴

- 通用 LLM (GPT / Claude / Gemini) 是「LLM 来计算」的设计；llive 则采用「**验证** LLM 的输出，必要时**重新计算**」的设计——孰优孰劣取决于用途，这里仅作为设计思路的差异来呈现
- Wolfram Alpha 是强大的计算引擎，但是封闭的云端；llive 则完全 on-prem。这一差异是否起作用，取决于你能否把数据送到外部这一约束
- 数学、物理、工程、金融、药学全都需要「单位量纲」和「精密计算」→ 作为第一个 vertical，适用范围很广，我们据此判断它值得优先验证

## v0.7-vertical MATH 的全部 8 项要求

| FR | 名称 | 优先级 |
|---|---|---|
| MATH-01 | SI 单位量纲分析引擎 | ✅ 1st 已实现 |
| MATH-02 | Z3 / Sympy 集成验证层 | 2nd |
| MATH-05 | 物理常数辞典 (CODATA 2022 + NIST) | 3rd |
| **MATH-08** | **内置计算引擎 (差异化轴)** | ✅ 4th 已实现 |
| MATH-03 | 数学式语法解析 (LaTeX/MathML/Sympy AST) | MED |
| MATH-04 | 数值计算精度跟踪 (IEEE 754) | MED |
| MATH-06 | 单位换算 + Buckingham π 无量纲化 | MED |
| MATH-07 | MATHEMATICAL EpistemicType | MED |

## 评估基准 (vertical 专用)

- **MMLU math** subset
- **GSM8K / MATH** dataset
- **PhysicsBench** (物理单位问题)
- **DimSafe**: llive 自有测试集 — 包含单位量纲错误的 1000 个样本，目标 recall ≥99 %, precision ≥95 %

## 来源

- 实现: `llive/src/llive/math/units.py` + `calculator.py`
- 公开 API: `from llive.math import Quantity, parse_unit, SafeCalculator, extract_expressions`
- 测试: `tests/unit/test_math_units.py` (22 个) + `tests/unit/test_math_calculator.py` (24 个)
- 全部 1014 PASS / 零回归

## 留下的问题 — 「不让它计算」就够了吗

到目前为止的设计都是「**不让** LLM 计算」。把算术式夺过来交给确定性引擎，`5 m/s + 3 s` 就会被拦下。但 LLM 吐出的不只是数值。如果它用一套像模像样的措辞，写出 `x² + x = 2x³` 这样**本身就错的数式**，又该怎么办？如果在夺走式子之前，无法机械地反证这个式子是否正确，那这套验证就只用了一半的肺。

下一篇 **#06「[如何阻止 LLM 的数式幻觉 —— 形式化验证门](./QIITA_#06_next_math02_formal_gate.md)」** 将解剖 MATH-02：把 LLM 吐出的数式用 Sympy 转成 AST、并机械地标记 (flag) 矛盾的机制——从本文的「不让它计算」向「反证它的输出」迈进一步。在相信一个式子之前，我们先去打造那台怀疑式子的引擎。

（作为手头并行推进的工作，还包括把 `SafeCalculator` 集成进 BriefGrounder，使式子在投入 Brief 的那一刻被自动 ground，以及把 MATH-05 CODATA 辞典 append 到 RAD `metrology` 分野。）

---

> FullSense ™ 的第一个 vertical specialisation。把「数学很强的 AI」当作第一个杀手级应用来培育的战略。

---

# 한국어

# 수학·단위에 강한 AI를 만드는 첫걸음 — MATH-01/08 내장 계산 엔진

> 📚 **연재 내비**: ← #01 [Brief API 설계와 progressive matrix](./QIITA_#01_brief_api_progressive.md) / #02 [10 사고 인자로 정리하는 사고층](./QIITA_#02_cognitive_factors.md) ｜ **#03 본 기사**（첫 vertical = 수학·단위）｜ #06 [LLM 수식 환각을 어떻게 멈출 것인가](./QIITA_#06_next_math02_formal_gate.md) →. ※ 각 기사는 단독으로도 읽을 수 있습니다.
>
> #01 에서 Brief 라는 입구를, #02 에서 그 위를 흐르는 사고 인자를 보았다. 본 기사에서는 그 입구에 **첫 전문 분야** 를 얹는다——수학과 단위다. 왜 범용 LLM 이 `5 m/s + 3 s = 8` 을 태연히 써 버리는가, 그 물음에서 시작한다.

## TL;DR

- llive의 첫 specialised vertical로서 「**수학·단위 특화 AI**」를 선정 (사용자 전략 지시)
- 범용 LLM이 약한 (a) 기호 조작의 환각 (b) 단위 차원의 혼동 (c) 수치 계산의 error propagation 을 **「LLM에게 계산시키지 않는」 결정론적 사이드카**로 극복
- 2026-05-17 같은 세션에서 **MATH-01 (SI 단위 차원 해석)** + **MATH-08 (내장 계산 엔진 = 차별화 축)** 의 minimal skeleton을 구현, 테스트 47건 추가
- `5 m/s + 3 s = 8` 같은 **차원 불일치를 감지하면 확실히 거부하는** API (감지 가능한 범위에서는 결정론적으로 멈춘다)

## 동기 — 범용 LLM의 수학적 약점

LLM은 언어적으로 그럴듯한 수식을 생성하지만, 다음에 약합니다:

| 관점 | 범용 LLM의 약점 | llive 기존 자산과의 부합 |
|---|---|---|
| 기호 조작의 환각 | `x² + x = 2x³` 같은 잘못된 등식 | EVO-04 Z3 정적 검증으로 gate |
| 단위 차원 | `5 m/s + 3 s = 8` | SI 차원 해석 엔진 (MATH-01) |
| 수치 정밀도 | float 연산 오차를 무시 | error propagation tracking (MATH-04) |
| 공리 체계 | 암묵적 전제를 혼입 | EpistemicType=MATHEMATICAL 의 strict track |
| 인용의 신뢰성 | "CODATA value is X" 라고 대충 답함 | RAD math/metrology + provenance |

## MATH-01 — SI 7개 기본 단위 + 유도 단위의 차원 대수

최소 의존성 버전을 자체 구현 (Pint 등 외부 라이브러리 불필요).

```python
from llive.math import Quantity, parse_unit, UnitMismatchError

# 速度 + 時間 = 不可能 (典型的 LLM 幻覚)
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t
assert d.dimensions.matches(parse_unit("m"))

# 力 × 距離 = エネルギー (J)
F = Quantity(10.0, parse_unit("N"))
d = Quantity(5.0, parse_unit("m"))
E = F * d
assert E.dimensions.matches(parse_unit("J"))  # ✓ Joule
```

구현의 핵심은 `Dimensions(m, kg, s, A, K, mol, cd)` 라는 7차원 벡터. 연산은 차원의 가감산 (곱/나눗셈에 대응). `Quantity.__add__` 에서 차원 검산 → 불일치는 **반드시 raise**.

### 유도 단위

`N` (kg·m/s²) / `J` (kg·m²/s²) / `W` (kg·m²/s³) / `Pa` (kg/m/s²) / `Hz` (1/s) / `C` (s·A) / `V` (kg·m²/s³/A) / `ohm` — 자주 쓰이는 범위만 구현.

## MATH-08 — 내장 계산 엔진 (차별화의 핵심)

**설계의 핵심**: LLM에게 **수치 계산을 시키지 않는다**.

```python
from llive.math import SafeCalculator, extract_expressions

calc = SafeCalculator()
brief_text = "Compute (2.5 * 7.8) / 0.3 then verify sqrt(16) is exact."

for expr in extract_expressions(brief_text):
    r = calc.evaluate(expr)
    print(f"{r.expression} = {r.value}  (ops={r.operation_count}, fns={r.used_functions})")
# (2.5 * 7.8) / 0.3 = 65.0   (ops=2, fns=())
# sqrt(16)          = 4.0    (ops=1, fns=('sqrt',))
```

### Safety의 의미

`Safe`의 제약:

- `eval()` 은 사용하지 않는다 (임의 코드 실행 회피)
- AST visitor로 허용 노드 (`BinOp` / `UnaryOp` / `Constant` / `Call` to whitelist) 만 통과시킨다
- 함수 whitelist: `sqrt` / `sin` / `cos` / `log` / `abs` / `mean` / ... (math + statistics 모듈에서 28개 함수)
- 상수 whitelist: `pi` / `e` / `tau` / `inf` / `nan`
- 0으로 나누기는 `CalculationError` 로 안전하게 reject
- `__import__('os').system('rm')` 같은 공격 체인을 attribute access 단계에서 reject

### Brief로의 grounding

Brief의 goal에 산술식이 포함되어 있으면, `extract_expressions()` 가 추출 → `SafeCalculator` 가 결정론적으로 평가 → 결과를 **grounded Stimulus** 로 주입하는 설계:

```
Brief.goal にある式 → SafeCalculator が評価 → 結果が augmented goal に追加 → ledger に固定記録 → LLM はそれを「事実」として参照するだけ
```

LLM이 계산한다 → 부동소수점 환각, 자릿수 손실
llive가 계산한다 → IEEE 754 정밀도, 재현 가능, 인용 가능

## 왜 이것을 첫 차별화 축으로 선택했는가

- 범용 LLM (GPT / Claude / Gemini) 는 「LLM이 계산한다」 설계. llive는 「LLM의 출력을 **검증**하고, 필요하면 **재계산**한다」 설계를 택했다——어느 쪽이 우월한지는 용도에 달려 있으므로, 여기서는 설계 사상의 차이로 제시한다
- Wolfram Alpha는 강력한 계산 엔진이지만 closed cloud. llive는 완전 on-prem. 이 차이가 효력을 발휘하는지는 데이터를 외부로 내보낼 수 있는가라는 제약에 달려 있다
- 수학·물리·공학·금융·약학 모두가 「단위 차원」과 「정밀 계산」을 필요로 한다 → 첫 vertical로서 적용 범위가 넓어, 먼저 검증할 가치가 있다고 판단했다

## v0.7-vertical MATH의 8건 전체 요건

| FR | 이름 | 우선 |
|---|---|---|
| MATH-01 | SI 단위 차원 해석 엔진 | ✅ 1st 구현 완료 |
| MATH-02 | Z3 / Sympy 통합 검증층 | 2nd |
| MATH-05 | 물리 상수 사전 (CODATA 2022 + NIST) | 3rd |
| **MATH-08** | **내장 계산 엔진 (차별화 축)** | ✅ 4th 구현 완료 |
| MATH-03 | 수식 구문 해석 (LaTeX/MathML/Sympy AST) | MED |
| MATH-04 | 수치 계산 정밀도 트래킹 (IEEE 754) | MED |
| MATH-06 | 단위 변환 + Buckingham π 무차원화 | MED |
| MATH-07 | MATHEMATICAL EpistemicType | MED |

## 평가 벤치마크 (vertical 전용)

- **MMLU math** subset
- **GSM8K / MATH** dataset
- **PhysicsBench** (물리 단위 문제)
- **DimSafe**: llive 독자 테스트셋 — 단위 차원 오류를 포함한 1000건으로 recall ≥99 %, precision ≥95 %

## 소스

- 구현: `llive/src/llive/math/units.py` + `calculator.py`
- 공개 API: `from llive.math import Quantity, parse_unit, SafeCalculator, extract_expressions`
- 테스트: `tests/unit/test_math_units.py` (22건) + `tests/unit/test_math_calculator.py` (24건)
- 전체 1014 PASS / 회귀 제로

## 남은 물음 — 「계산시키지 않는다」로 충분한가

여기까지의 설계는 「LLM에게 **계산시키지 않는다**」였다. 산술식을 빼앗아 결정론 엔진에 넘기면 `5 m/s + 3 s` 는 멈춘다. 하지만 LLM이 토해내는 것은 수치만이 아니다. `x² + x = 2x³` 같은 **틀린 수식 그 자체** 를 그럴듯한 말로 써 온다면? 식을 빼앗기 전에 그 식이 옳은지를 기계적으로 반증할 수 없다면, 그 검증은 한쪽 폐로만 숨 쉬는 셈이다.

다음 회 **#06「[LLM 수식 환각을 어떻게 멈출 것인가 — 형식 검증 게이트](./QIITA_#06_next_math02_formal_gate.md)」** 에서는 MATH-02 를 해부한다. LLM이 내놓은 수식을 Sympy로 AST화하고 모순을 기계적으로 flag 하는 구조——이번의 「계산시키지 않는다」에서 「출력을 반증한다」로 한 걸음 나아간다. 식을 믿기 전에, 식을 의심하는 쪽의 엔진을 만들러 간다.

（손에 잡히는 병행 작업으로는, BriefGrounder에 `SafeCalculator` 를 통합해 Brief 투입 시점에 식을 자동 ground 하고, MATH-05 CODATA 사전을 RAD `metrology` 분야에 append 하는 정비도 함께 진행 중이다.）

---

> FullSense ™ 의 첫 vertical specialisation. 「수학에 강한 AI」를 첫 킬러 애플리케이션으로 키우는 전략.
