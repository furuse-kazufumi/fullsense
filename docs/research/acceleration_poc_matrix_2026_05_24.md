---
layout: default
title: "高速化候補 全 PoC 判定マトリクス (2026-05-24)"
parent: "Research"
nav_order: 97
---

# 高速化候補 全 PoC 判定マトリクス (2026-05-24)

> ユーザー指示「ちゃんと定量的に比較する PoC が必要。効果がありそうなら要件定義に
> まとめて本格導入」+「組み合わせごとの PoC も」+ Goal「全 PoC を済ませる」に対応。
> 5 単体 + 3 組み合わせ = **8 PoC を実装・実測**し、優先付けの定量根拠をここに集約する。
> 規約: 要件→PoC→フィジビリティ ([[feedback_poc_feasibility_first]]) /
> 採用は選別 ([[feedback_originality_over_imitation]]) / 数字を疑う
> ([[feedback_benchmark_honest_disclosure]])。

すべて **simulation / toy 環境** であり実測ハードウェアではない (honest disclosure)。
損益の**構造**を見るためのもので、絶対値は実配線後に上書きする。

## 単体 PoC (5)

| # | 候補 | repo / module | 効果 (定量) | 条件・コスト | tests |
|---|---|---|---|---|---|
| 1 | **Speculative Mesh** | llmesh `speculative/bench.py` | LAN fast-fallback 1.39–7.77x、swap-bound 最大 **9.18x** | **LAN 限定** (WAN 全敗 0.43–0.70x) / **fast-fallback 必須** / 低 hit_rate は wasted_compute 大 | 11+23 |
| 2 | **Antifragile Mutation** | llive `evolution/antifragile_bench.py` | 局所最適脱出 **0%→100%** (mean best 0.85→1.0) | toy 1-D / panic **47.7/60 世代** (コスト高) / 実 fitness 未測 | 5 |
| 3 | **適応推論予算 (IBPO/early-exit)** | llive `perf/adaptive_budget_bench.py` | 完全推定器で **44% 計算削減・品質同等** | 推定器ノイズで品質低下 (0.2 で精度65.8%) / frozen core 非干渉 | 5 |
| 4 | **予測検証メタゲート (#1)** | llive `evolution/predictive_gate_bench.py` | invalid 30/60/90% で **29/55/80% コスト削減** | 有効候補 ~3-4% 誤却下 / cheap≪verify 前提 | 5 |
| 5 | **KV-cache mesh 差分 (#2)** | llmesh `speculative/kv_diff_bench.py` | LAN 全 locality で win (5%差分 **29.85x**) | **LAN 限定** (WAN 全敗) / locality 高ほど得 | 8 |

## 組み合わせ PoC (3)

| Combo | ペア | synergy (定量) | tests |
|---|---|---|---|
| **A** | Antifragile × Speculative Mesh | 脱出率 100% 維持 + 並行投機で wall-clock **W=8→6.82x** (W=1 は overhead で 0.91x) | 4 |
| **B** | Speculative Mesh × KV-cache 差分 | 暖機で exec 40→13.4ms、hit_rate **0.60→0.80**、speedup **2.40x→4.52x**、miss 無駄 34% (高 locality) | 5 |
| **C** | Antifragile × 予測検証ゲート | panic burst (高 invalid) で run 全体の verifier コスト **69% 削減** (通常区間のみなら 25%) | 4 |

## 共通発見 (honest disclosure)

- **LAN 前提が mesh 系 (Speculative / KV-cache) の必須条件**。WAN は帯域・往復で**全敗**。
  → 産業 on-prem (LAN) が FullSense の主戦場であることと整合。
- すべて**予測符号化 spine** と整合 (予測を先に立て、誤差/差分だけ流す/計算する)。
- **コストの正直な計上**: Antifragile の panic は探索評価を増やす (電力)、Speculative は
  低 hit_rate で wasted_compute 大。latency が得でも環境負荷は残る。

## 優先付け提案 (定量根拠ベース)

- **Tier 1 — 要件済・高 ROI・基盤性**: **Speculative Mesh**。要件定義
  (`llmesh/docs/requirements_speculative_mesh.md`, SPEC-MESH-01..10) 済。Combo-A/B が
  この上に乗る (並行投機 + KV 暖機)。次の本格導入の最有力。
- **Tier 2 — 汎用・低リスク・frozen core 非干渉**: **適応推論予算 (IBPO)** +
  **予測検証ゲート (#1)**。ゲートは Antifragile panic と強い synergy (Combo-C 69%)。
- **Tier 3 — 効果実証済だが汎化/コスト要検証**: **Antifragile** (toy で決定的だが panic
  コスト高、実 fitness/高次元 genome の ROI 要測定)、**KV-cache 差分 (#2)** (LAN 前提、
  実装重め、Speculative と署名スキーム共通化が前提)。

## 眼鏡 — PoC メタ評価 (単に高速 ≠ 採用)

> ユーザー指示「単に高速というだけでは、少し疑わないといけない」「lleval のような眼鏡で
> PoC する」に対応。自作 PoC の speedup をそのまま信じず、独立ルーブリックで
> **速さの裏 (品質犠牲 / 隠れコスト / 汎化リスク / self-preference)** を採点する。
> 実装: `fullsense/tools/poc_lens.py` (`py -3.11 tools/poc_lens.py`, 自己検証 assert 込)。

| PoC | 主張 | 品質犠牲 | 隠れコスト | 汎化リスク | self-pref | trust | verdict |
|---|---|---|---|---|---|---|---|
| Speculative Mesh | LAN 9.18x | 0 | 2 | 2 | 1 | 0.47 | 実測で再検証 |
| Antifragile | 脱出 0%→100% | 0 | 2 | 2 | 2 | 0.35 | 実測で再検証 |
| 適応推論予算 (IBPO) | 44% 削減 | 2 | 0 | 2 | 1 | 0.47 | 実測で再検証 |
| 予測検証ゲート (#1) | 29-80% 削減 | 1 | 0 | 1 | 1 | **0.72** | 有望 (低疑い) |
| KV-cache 差分 (#2) | LAN 29.85x | 0 | 1 | 2 | 1 | 0.60 | 実測で再検証 |
| Combo-A | wall-clock 6.82x | 0 | 2 | 2 | 2 | 0.35 | 実測で再検証 |
| Combo-B | 2.40x→4.52x | 0 | 1 | 2 | 1 | 0.60 | 実測で再検証 |
| Combo-C | run 69% 削減 | 1 | 0 | 2 | 2 | 0.47 | 実測で再検証 |

**眼鏡の結論**:

- どの PoC も **trust=1.0 (無条件採用) にならない** — 全て simulation/toy。「速い」は仮説。
- **self-preference が重い (Antifragile / Combo-A,C) は採用保留** — landscape を panic 有利に
  設計した自覚があり、独立な実測が要る。
- **適応推論予算は「速いが間違える」罠** — 推定器ノイズで精度 65.8% まで落ちる。速度だけ見て
  採用すると品質が崩れる典型。推定器精度の floor が前提。
- 最も疑い低は **予測検証ゲート (#1, trust 0.72)** — simulation 距離が近く rigging も薄い。
- → **速い結果ほど内訳を疑い、実 transport/executor/fitness 配線後の実測で上書きする**
  ([[feedback_benchmark_honest_disclosure]] / [[feedback_rust_usage_matters]])。

## 本格導入への道筋 (次)

1. Tier 1: Speculative Mesh SPEC-MESH-01 (予測器の hit_rate 単体測定) から着手。
2. 各 PoC の simulation 値を、実 transport / 実 executor / 実 fitness 配線後に**実測で上書き**。
3. 結合 (要素統合) 判断は**ユーザー** (FullSense 規約: 勝手に結合しない)。

## Sources / 関連

- 単体: llmesh `speculative/` (`2a05f64`/`b1d95e6`/`e7ced23`) / llive
  `antifragile_bench`(`aff62ab`) `adaptive_budget_bench`(`81212a8`) `predictive_gate_bench`(`d9113ae`)
- 組み合わせ: llive `combo_bench`(`5d51f3b`) / llmesh `combo_bench`(`65672d5`)
- 要件: `llmesh/docs/requirements_speculative_mesh.md`
- 上流: [Gemini ブレスト #3/#4 実装着地]({{ '/research/gemini_brainstorm_impl_2026_05_24' | relative_url }}) /
  `llive/docs/algorithms_for_ai_development.md` (高速化レンズ)
