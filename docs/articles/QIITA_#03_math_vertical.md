---
layout: default
title: "数学・単位に強い AI を作る最初の一歩"
date: 2026-05-17
tags: [llm, math, units, dimensional-analysis, hallucination]
id: 2c4a993937c373c464f6
---

# 数学・単位に強い AI を作る最初の一歩 — MATH-01/08 内蔵計算エンジン

## TL;DR

- llive 最初の specialised vertical として「**数学・単位特化 AI**」を選定 (ユーザー戦略指示)
- 汎用 LLM が苦手な (a) 記号操作の幻覚 (b) 単位次元の取り違え (c) 数値計算の error propagation を **「LLM に計算させない」決定論的サイドカー** で克服
- 2026-05-17 同セッションで **MATH-01 (SI 単位次元解析)** + **MATH-08 (内蔵計算エンジン = 差別化軸)** の minimal skeleton を実装、47 件テスト追加
- `5 m/s + 3 s = 8` のような典型的幻覚を **必ず止める** API

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

## MATH-08 — 内蔵計算エンジン (差別化軸最大)

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

## なぜこれが差別化軸として最強か

- 汎用 LLM (GPT / Claude / Gemini) は「LLM が計算する」設計
- llive は「LLM の出力を **検証**し、必要なら **再計算** する」設計
- Wolfram Alpha は強力だが closed cloud。llive は完全 on-prem
- 数学・物理・工学・金融・薬学 すべてが「単位次元」と「精密計算」を必要とする → 最初の vertical として広い適用範囲

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

## 次の一歩

- BriefGrounder に `SafeCalculator` を統合 → Brief 投入時点で式が自動 ground される
- MATH-05 CODATA 辞書を RAD `metrology` 分野に append
- MATH-02 Sympy 検算層で LLM の数式出力を AST 化 → 不整合 flag

---

> FullSense ™ の最初の vertical specialisation。「数学に強い AI」を最初のキラー応用として育てる戦略。
