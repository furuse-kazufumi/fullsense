# 内部状態安定性解析の防御地図 — T4 4-3 (2026-06-07)

> master_plan T4 4-3 (D4' の最脆部 = 「Hopfield/SSM はとっくに安定性解析している」という査読反論の
> 先回り) の実行記録。方法 = Workflow 38 agents: 4 系統 (modern Hopfield / SSM・Mamba /
> linear attention・DeltaNet / RWKV・hybrid) 並列 sweep → 候補ごとに一次情報確認 + threat 判定 +
> **引用価値 (must_cite / nice_to_have / skip)** 評価。

## 結論

**breaks 0 / must_cite 27 (ユニーク ~25) / nice_to_have 7。**

corner (ii) の隣接 (記憶コア内部 dynamics の安定性「解析」) は**成熟した活発な分野**だが、
全候補が同じ形で交差点を外す: 安定性は **(a) 解析・診断** (Lyapunov/Jacobian/ISS — post-hoc) か
**(b) by-construction** (reparameterization / clamp / 正規化 — reject 対象が表現空間に存在しない) か
**(c) 監視** (criticality monitoring) であり、**候補更新を証明して棄却する prove-then-reject ゲート
(corner iii) はどの系統にも存在しない**。→ D4' は「解析は存在する (譲歩) が、ゲートは無い (差別化)」
の二段構えで防御可能。

## 論文編入の系統地図 (代表のみ引用、過剰引用は padding リスク)

| 系統 | 代表 (must_cite) | 防御壁での役割 |
|---|---|---|
| Hopfield/energy | Ramsauer+ 2008.02217 (正準: 収束保証 = attention) / Krotov+Bullo survey 2604.05042 (成熟分野の譲歩アンカー) / Masumura+ NeurIPS25 2511.20698 (最新 (ii) 隣接) / DenseAM Epanechnikov 2506.10801 / capacity 2410.23126 | 「energy descent 収束は想起 dynamics の受動特性 — 更新採否ゲートでない」 |
| Attention spectral | Emadi 2602.18849 (**exact softmax Jacobian norm — 結論 θ(p)≈1 = 非収縮の診断**) / Recurrent Self-Attention Dynamics NeurIPS25 2505.19458 (Jacobian/Lyapunov **監視**) | 「最強の解析ですら診断/監視であり、強制ゲートでないことを自証」 |
| SSM by-construction | StableSSM 2311.14495 / LRU 2303.06349 / LinOSS 2410.03943 (+D-LinOSS 2505.12171) / S4-PTD 2310.01698 / Mamba-Lyapunov 2406.00209 (post-hoc 解析) / Selective-SSM ISS/LMI 2505.11602 (解析の最直接) / contracting implicit RNN 1912.10402 (convex 制約系譜) | 「reparameterization = 設計時保証 vs prove-then-reject = 候補毎検証」の archetype 群 |
| Delta-rule/linear RNN | **Gated DeltaNet 2412.06464 (「gate」語彙衝突: decay/forget gate ≠ admission gate — 明示対比必須)** / DeltaProduct 2502.10297 / 負固有値 2411.12537 (**非縮小を志向 = 我々と逆方向**) / xLSTM 2405.04517 (数値安定化) / ReGLA 2502.01578 / GatedFWA 2512.07782 | 「学習された忘却ゲート ≠ 証明された採否ゲート」 |
| Test-time memory | Titans 2501.00663 (heuristic 安定化: decay/momentum/gating, 無条件更新) / RWKV-7 2503.14456 (clamp/parameterization) | 「最近接の test-time 記憶更新も certificate なし・棄却なし」 |

nice_to_have 7 件 (Spectral Bias 2508.20441 / RWKV v1 2305.13048 / M^2RNN 2603.14360 等) は
doc 保持のみ — 論文には足さない (padding 回避、Workflow verifier 自身の指摘)。

## D4' 文言への含意

- 旧 D4 「検証派は制御系 dynamics 限定」は**そのまま維持可能** — 内部状態の安定性「解析」は
  ML 側に豊富だが、「sound 証明でゲートする」は依然 control 系のみ → 四点交差点は無傷。
- ただし related work で**譲歩を先に置く**こと: 「内部 dynamics の安定性解析は成熟分野である
  (survey 引用)。我々の新規性はその解析の存在ではなく、解析を fail-closed 採否ゲートに変えて
  進化ループに入れた点にある」。
- 「gate」語彙の衝突 (Gated DeltaNet 等の forget gate) は**明示的に注記**しないと誤読される。

## 監査の質 (honest)

- RWKV-7 / DeltaProduct は 2 系統から独立検出 (検出網の冗長性確認)。
- skip 判定 0 件 = sweep の選別が甘い可能性 (must_cite 27 は多すぎる)。論文編入時に系統代表へ
  圧縮することで補正した。
- 検索は英語のみ。中国語圏 (Qwen/RWKV コミュニティ) の非 arXiv 文献は未踏。

## 論文への反映 (同日実施)

PAPER_DRAFT four-point intersection 節に新グループ「Stability analyses of memory-core internal
dynamics」を追加 (系統 5 群、代表 ~14 件)。
