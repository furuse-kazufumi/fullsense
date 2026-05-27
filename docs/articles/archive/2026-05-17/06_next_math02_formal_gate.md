---
layout: default
title: "LLM 数式幻覚をどう止めるか — 形式検証ゲート (MATH-02 設計予告)"
date: 2026-05-17
tags: [llm, math, formal-verification, z3, sympy, hallucination]
draft: true
---

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

```
LLM 出力テキスト
    │
    ▼
[式抽出器] (MATH-03 multi-syntax parser, LaTeX/MathML/Sympy)
    │
    ▼
[Sympy AST]
    │
    ├─→ simplify(lhs - rhs) == 0 ? → ✅ 通過
    │   ❌ → 失敗 flag
    │
    └─→ Z3 で satisfiability check (∀ x. lhs(x) == rhs(x) ?)
        ❌ → 反例を ledger に記録
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
