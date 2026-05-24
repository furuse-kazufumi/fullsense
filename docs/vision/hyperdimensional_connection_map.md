# Hyperdimensional Thinking — FullSense 接続マップ & 採用方針

> 2026-05-24 作成。`HYPERDIMENSIONAL_THINKING.md`(B) / `SINGULARITY_REQUIREMENTS.md`(A) を
> FullSense にどう位置づけ、既存資産とどう接続し、どこまでを今やる(=未来計画レベル)かを記す
> 統合ノート。**本書は FullSense 側の整理であって、B/A 原文は改変しない**。

## 0. 位置づけ (ユーザー判断 2026-05-24)

- Hyperdimensional Thinking は **シンギュラリティを起こすために必要な因子の「一つ」** である
  (唯一の要件ではない)。A の §1 ビジョン肉付け時は「複数の必要因子のうちの一因子」として
  組み込む。他因子の例 (FullSense 文脈): 自己進化 (llive)、来歴/責任 (Approval Bus)、
  on-prem 純度、人間-AI 融合ビジョン ([[user_vision_ai_human_fusion]])。
- **採用レベル = 未来計画**: 現状を破綻させない。既存プロジェクトに即時リファクタを強制しない。
  B はあくまで **opt-in の指針**で、新規設計で自然に適用できる箇所に機会的に使う。A は
  **スケルトンのまま保留**し、§0 の立項判断基準が揃ったら立項する。
- 本接続マップ自体は production コードを一切変更しない (doc のみ)。

## 1. B の原則は FullSense で既に部分的に実現されている

「拡張された表現空間で考える」発想は、実は FullSense の既存設計に断片的に現れている。
B を新規に押し付けるのではなく、**既にある実践を B の言葉で再記述**できる:

| B の原則 / §2 空間 | 既存 FullSense 実装 | 接続 |
|---|---|---|
| (d) 複数表現の同時保持 | **llive Genome3D 多層ゲノム** (c_impl/c_prompt/c_meta/c_factors) | 同一 llive variant を 4 つの異なる「層=表現」で同時に持ち、層内/層間 crossover で操作。2026-05-24 実装着地 (commit 84d41a8…5dfca68) |
| (a) 表現を第一級に / (c) 思考空間と提示空間の分離 | **RepIR / llrepr** (LLVM-for-expression, 型付き表現 over MCP) | コア閉集合 + extensions、capability negotiation + degrade。思考側 typed IR と提示側 Markdown degrade の二層 = (c) |
| §2 球面調和の既約表現空間 (名指し実践例) | **精密計測 × 3DGS SH** ([[project_precision_metrology_llm]]) | 3DGS の SH 係数回転 = SO(3) の既約表現上の Wigner-D 作用。B が「3DGSのSH回転がこの実践例」と明記 |
| (b) 変換と不変量のペア / 等変 | (未実装、Phase 0 候補) | SH band energy の SO(3) 不変、曲率の剛体変換不変など。テストで不変性を固定する規律 (B §4) |
| 多視点 (10 思考因子の一つ) | **llive 10 思考因子** ([[project_llive_cog_fx_factors]]) | 「多視点」因子 = 認知版の多重表現。Genome3D c_factors は因子×メモリ層の 2D matrix |
| (c) 予測(内部)→誤差(提示) | **予測符号化アーキテクチャ** ([[project_fullsense_expression_realtime_marathon]]) | 内部で予測生成し、確定時に typed diff(予測誤差)だけ push = 思考空間と提示空間の分離の動的版 |

→ **B の評価軸 (多重表現/転移/還元/非自明性テスト) は FullSense の honest disclosure /
measurement purity 文化と地続き**。特に「非自明性テスト」(人間が日常次元で考えただけでは
得られない結論か) は [[feedback_benchmark_honest_disclosure]] の「異常に良い結果は内訳を疑う」
の裏返し — 本物の非自明 vs 偽物の不可解 を切り分ける要請。

## 2. 知識入力パイプライン: 3Blue1Brown / Ufolium tracker

数学・科学教育チャンネル追跡ルール (raptor, `3b1b-tracker`) が追う領域 —
`group_theory / conformal_map / complex_analysis / topology / geometry / signal_processing` —
は **まさに B §2 の表現空間の数学そのもの**。例の新着「絵の対数を取る」(Escher × 複素対数 ×
等角写像) は B の「複素平面・等角写像群」の直接の教材。

→ tracker は **表現空間ライブラリ (B §3 `spaces/transforms/invariants/`) の継続的な知識入力源**
として位置づけられる。新しい数学概念 → 表現空間候補の発見 → ライブラリ拡張、の供給線。
(tracker 自体の仕様・実装は raptor 側の別件)

## 3. 未来の適用候補 (Phase 0、計画のみ・今は実装しない)

A のロードマップ Phase 0「HYPERDIMENSIONAL_THINKING を個別プロジェクトに適用」「表現空間
ライブラリ初版」の具体候補。**現状非破壊のため、着手は別途ユーザー判断**:

1. **SH × SO(3) reference 実装** (B 名指し例): 隔離した experiment として
   `spaces/sphere_harmonic` + `transforms/so3` (Wigner-D) + `invariants/sh_power_spectrum`
   + 不変性テスト。最小の「動く B」。精密計測 / mcp-3d / 3DGS と接続可能。
2. **llive: 表現空間を genome の選択軸に**: 「どの空間で考えるか」を進化の選択対象にする
   (B §5 AIへの空間選択権の委譲の自律化)。Genome3D に「表現空間」chromosome を足す将来案
   (※ 走行中の進化を壊さない凍結点ルールに従うこと — [[project_llive_evolution_next_session]])。
3. **多重表現テストの暫定運用**: 同じ対象を 2 空間で処理して結論一致を確認する小さなテスト
   群を 1 プロジェクトで試す (A 評価要件 §3.3 の最小実践)。

## 4. 採用ガードレール (現状を破綻させないために)

- **opt-in / 機会的適用**: 既存コードの一括リファクタは禁止。新規設計・新規モジュールで
  自然に使える箇所にのみ B を適用する。
- **隔離**: PoC は `experiments/` 等の隔離領域で。production パスに未成熟な抽象を入れない。
- **FullSense 構成プロジェクト間インターフェース変更はユーザー確認** (CLAUDE.md 規約)。
- **A は保留**: 立項判断基準 (A §0) が揃うまでスケルトン維持。個別プロジェクトでの発見を
  A の検討事項に追記していく運用 (A §7)。

## 関連
- `docs/vision/HYPERDIMENSIONAL_THINKING.md` (B, 実務指針)
- `docs/vision/SINGULARITY_REQUIREMENTS.md` (A, 要件定義スケルトン・保留)
- memory: [[project_precision_metrology_llm]] / [[project_llive_thought_factor_per_layer]] /
  [[project_llmesh_representation_layer]] / [[project_fullsense_expression_realtime_marathon]] /
  [[user_vision_ai_human_fusion]]
