# CAV/TACAS/FM 逆引き 2 巡目 — llcore 四点交差点の脅威監査 (2026-06-07)

> master_plan T4 4-2 (監査 critic 指摘の最優先盲点 = 形式手法会議側の逆引きが 1 巡のみ) の実行記録。
> 方法 = Workflow 36 agents: 4 角度並列 sweep (CAV/TACAS tool papers / FM×RNN・Transformer 検証 /
> runtime assurance×更新ゲート / 2026 最新自己進化×検証) → 候補ごとに一次情報 (arXiv abstract /
> 会議ページ / GitHub) を WebFetch 確認して敵対判定。1 巡目 (differentiation_audit_dna_roadmap_2026_06_06.md)
> の既知 narrows 19 件は除外済み。

## 結論

**breaks 0 / narrows 17 (ユニーク ~14) / background 15。四点交差点は 2 巡目でも生存。**

- **SSGM (2603.11768) の後続実装は見つからず** — verified memory evolution の実装先取り窓は
  本日時点でまだ開いている (Phase 2a の防衛的公開を急ぐ根拠は維持)。
- ただし新規 narrows に**従来より交差点に近い**ものが複数出現 (下記 Tier 1)。論文 related work に
  追記済み (PAPER_DRAFT four-point intersection 節)。

## Tier 1: 論文防御壁に追加 (必須)

| 先行 | 何をやっている | なぜ交差点を埋めないか |
|---|---|---|
| **Scrivens 2026 ペア**: Information-Theoretic Limits (arXiv 2603.28650) + Classification-Verification Dichotomy (2604.00072) | 自己改善ループ内の**重みパラメータ更新**に sound fail-closed prove-then-reject ゲートを実装 (accept θ iff ‖θ−θ₀‖<r=m/L の Lipschitz-ball verifier)。理論編は classifier gate の不可能性定理 + Lipschitz-ball escape (Thm 2) | certified property は**安全オラクル境界からの parameter-ball 距離**であって contraction (ρ(J)<1) でない (corner i)。記憶コアの内部 dynamics でもない (corner ii)。**corner iii を weights で占有する現時点の最近接** — D3' の文言更新が必要 |
| **CART (arXiv 2606.01495)** | Recurrent Transformer 記憶コアの内部 dynamics の spectral radius を分析、訓練中 ρ∈[0.79,0.83]<1 に整定 | **stability は learned** (データから創発、sigmoid gate で「学習」) — 証明ゼロ・ゲートゼロ。corner (ii) の対象が一致する初の例だが (i)(iii) を欠く。「learned vs proven stability」の対比軸として引用必須 |
| **RNN-SDP (arXiv 2509.17898)** | RNN の Lipschitz 定数の certified 上界を SDP 凸緩和で計算 (proof machinery が llcore の cert_sdp と同族) | global Lipschitz bound ≠ contraction 証明、訓練/進化ループ外の post-hoc 証明、ゲートなし |

## Tier 2: 論文に 1-2 文で言及 (推奨)

| 先行 | 位置づけ |
|---|---|
| **alpha-beta-CROWN Jacobian operators (2025-08 release + VNN-COMP 2025 Lyapunov benchmark, arXiv 2512.19007)** | SOTA NN verifier が Jacobian バウンディング → continuous-time Lyapunov 検証を可能に。corner (i) のツール面の接近。**llcore の将来 certifier ladder 候補としても有用** (R-LLM-1 の vertex-free 化に使える可能性) |
| **SpectralGuard (arXiv 2603.12414)** | SSM 内部の spectral radius を**監視** (memory collapse 攻撃検出)。post-hoc モニタで証明ゲートでない。内部状態解釈の防御 (監査 4-3, D4') に有用 — 「内部 spectral dynamics が攻撃面」という動機づけを共有 |
| **Adaptive provably-correct Simplex (STTT 2025)** + **Safe Parameter Update (RA-L 2026, RaCLF+CBF QP)** | RTA/adaptive-control 側で「適応・パラメータ更新そのもの」のゲートに最接近。前者は proof-on-demand reachability、後者は QP modulation = **projection** (rejection でない)。対象は制御系 |

## Tier 3: background (参考のみ、編入不要)

Set-Based Training (2401.14961) / CAV 2025 deductive RL synthesis / logRASM policy verification
(2406.00826) / SEDM (2509.09498) / ASG-SI (2512.23760) / VASO (2606.05395, NuSMV ゲートだが対象は
robot plan) / NNV 3.0 / StarV / Neural Simplex / VeRecycle / Incremental NN verification ほか。
いずれも by-construction・合成・replay 検証・出力ゲート系で 4 corner の 2 つ以上を欠く。

## 監査の質に関する注記 (honest)

- finder の 1 候補 (2603.28650) を「pure negative result」と誤特徴付けしていたのを verifier が
  一次情報で訂正 (実際は impossibility + constructive escape の mixed) — 敵対検証層が機能した証跡。
- Scrivens 2 本は単一著者 (Arsenios Scrivens) の theory+empirical ペアで、複数角度から独立に
  検出された (検出網の冗長性確認)。
- 特許 DB 照会 (T4 4-1) は依然未実施 — 残る既知の穴。

## 論文への反映 (同日実施)

PAPER_DRAFT.md four-point intersection 節に Tier 1 (3 件) + Tier 2 (3 件) を追記、
audit provenance の「single-round」記述を 2 巡目完了に更新。
