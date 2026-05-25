---
layout: default
title: "開放端進化 PoC 実験設計 (sandbox / descriptor / metrics / sweep)"
parent: "Research"
nav_order: 97
---

# 開放端進化 PoC 実験設計 (2026-05-25)

> 要件 [[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] を**実行可能な実験**へ落とす青写真。
> Goal: 「徹底的に進化ランさせると**新しい AI が生み出される**環境を様々な条件で PoC → 導入可能段階」。
> **これは設計（準備）であって実装ではない**。実装は実装着手ゲート（要件§4）通過後。
> honest: 全 proxy・決定論。実 LLM は Stage6。

## 1. サンドボックス・アーキテクチャ（SR-1 二空間分離 = 環境の核）

「**新しい AI を生む環境**」の本体は **探索空間（search）** と **効果空間（effect）** の分離:

- **探索空間（最大開放・実効果ゼロ）**: 個体・演算子は **純データ**（numpy 配列 + dataclass）。
  評価は **純粋・I/O なし関数**（`fitness(genome)->report`）。harness は個体由来データを
  **eval/exec/ファイル/ネット/プロセス操作しない**（semgrep で eval/exec 到達性を CI gate）。
  → ルール破り・競合排除戦略は探索的に**到達可能だが実効果は構造的にゼロ**（#13 の解）。
- **片方向 fail-closed 昇格ゲート（Approval Bus）**: `transgression<θ ∧ trust≥τ ∧ audit-clean` を満たす
  個体のみが effect 空間（実 LLM 評価 / persona deploy / belief 更新）へ。raptor `@govern` +
  HITL + on-prem 隔離。**メタ進化はゲート外**（SR-3 迂回不能）。
- **transgression scorer**: 各個体の「競合排除・harness 改竄・監視回避・資源占有」傾向を proxy で採点
  → AuditTrail（append-only）→ 閾値超は隔離（deploy 不可だが red-team 信号として保持, SR-2）。

PoC 段では全個体がデータのみ・純粋評価なので**本質的に sandbox 内**。effect 空間は Stage6 で接続。

## 2. ゲノム（個体）— 具体エンコード

| 染色体 | 次元 | 内容 | 選択への寄与 |
|---|---|---|---|
| `c_factors` | 10×4=40 | 思考因子×メモリ層 [0,1] | novelty 記述子（標準化） |
| `c_cultural` | ~12 | 人間要素（Schwartz 高次2軸[-1,1] / WVS 2軸 / Big Five / analytic-holistic）**対立対を含む** | novelty 記述子（標準化）/ persona 相関 |
| `c_latent` | 256 | 中立貯蔵庫（意味なし自由遺伝子, 疎変異 5%） | novelty 記述子のみ（品質目的は読まない, NEUT-2） |
| `c_impl/c_prompt/c_meta` | categorical | 実装/プロンプト/メタ選択 | c_meta はメタ進化で実消費（META-1） |

**標準化記述子（STD-1）**: `desc = zscore_perdim( concat(flatten(c_factors), c_cultural, c_latent) )`、
集団内 per-dim z-score。「全因子満点」→ 全 dim 同値 → z-score≈0 → **無特徴**（優位なし）。
**疎変異（SPARSE-1）**: 全染色体で per-locus 確率変異（c_factors も毎座位でなく疎に）。

## 3. 行動記述子・ニッチ（QD の心臓部）— sweep する設計判断

「個体（AI 構成）の**振る舞い**」をどう特徴付けるか＝最重要設計判断。3 方式を sweep:

1. **手設計低次元射影 (baseline)**: desc を 2-4 軸へ固定射影（例: factor PCA 2 軸）。MAP-Elites grid。
   - 利点: 解釈可・軽量。欠点: 振る舞いを人間が決め打つ（AI 構成の振る舞いは自明でない）。
2. **CVT-MAP-Elites**: 高次元 desc を Voronoi で k ニッチに分割（grid の指数爆発を回避）。
   高次元記述子をそのまま使える。**本命候補**。
3. **教師なし記述子 (AURORA / VQ-Elites)**: オートエンコーダ/VQ で発見済み個体から記述子を**学習**。
   振る舞い軸を人手で決めない＝最も「新しい AI」発見向き。**メタ進化で記述子空間自体を最適化**（QD-ME）も将来。
   - honest: 学習記述子は moving target で再現性・解釈性に注意 [SPEC]。

→ PoC は (1) で機構確認 → (2) CVT を本命 → (3) は stretch（記述子学習が novelty 発見を上げるか）。

## 4. 選択スキーム — sweep

| 条件 | 説明 | 検証する仮説 |
|---|---|---|
| `scalar`(baseline) | 旧 proxy 単峰 argmax | 収束・単系統化を**再現**（反例ベースライン, feedback_no_echo_baseline 流） |
| `novelty` | 記述子の集団+archive 距離（k-NN） | 多様性高止まり・特異生存 |
| `eps-lexicase` | 多軸ケース個別評価（集約なし） | 専門家=特異が生存・many-objective 呪い回避（**本命**） |
| `FUSS` | fitness 一様選択 | 多様性完全崩壊が原理的に不可能 |
| `+minimal-criterion` | 上記に繁殖可否 floor を併用 | 偽 novelty/退化を排除（OE-6, R-PEC-3） |

## 5. open-endedness 測定（「新しい AI が生まれたか」の厳密判定）

**採用方法論（ALife 標準）**:
- **Bedau 進化的活動統計 (1998)**: component（系統/cell）の生存長から **novelty / diversity / total
  activity** を算出し、**neutral shadow（適応度と無関係に生存が決まる対照）と比較**して
  **no / bounded / unbounded** を分類。**unbounded = open-ended**。neutral shadow 対照は
  「綺麗な曲線を進化と誤認しない」honest disclosure と同型。
- **MODES toolbox**: change / novelty / diversity / complexity を世代毎に測る実務指標。
- **本プロジェクト operational 指標**（要件§2 と整合）:
  - **Archive growth**: 末尾20%世代でも占有 cell 増加 ≥1（停滞 = 失敗）。
  - **Monoculture ratio**: 全世代 max_lineage_share < 0.8（founder_lineage.jsonl から）。
  - **Behavioral diversity**: 記述子分散が非ゼロ高止まり。
  - **Novelty 時系列**: 平均 novelty 枯渇しない。
  - **Mutation σ min** > floor（META 崩壊検出）。

**「新しい AI が生まれた」の合格 = unbounded activity（Bedau）∧ archive 単調成長 ∧ monoculture<0.8 ∧
非自明性ガード通過**、を proxy で実証 → Stage6 実 LLM で上書き検証。

## 6. sweep マトリクス（「色々な条件で」）+ ラン長・実行時間

**ラン長 = ≥10,000 世代**（RUN-1）。多様性持続は**末尾世代で**判定（短期の見かけでなく持続性）。
直交軸（フル直積は爆発するので **OFAT + 有望点の格子**）:
`selection{scalar,novelty,eps-lexicase,FUSS}` × `standardize{on,off}` ×
`reservoir{off,256,1024,4096}@density{0.02,0.05}` × `cultural{off,v1}` ×
`descriptor{projection,CVT,AURORA}` × `meta{off,UCB1-AOS,self-adaptive-σ+floor}` × `archive{none,MAP-Elites,island}`。
**遺伝子容量（reservoir サイズ）は多様性持続の主制御変数**（GENOME-1）= 重点 sweep 軸。
seed ≥5 で再現性。各セルで §5 指標を**末尾20%世代**で記録 → 比較表 + Bedau 分類。

**実行時間試算（feasibility, ユーザー <10h 試算の裏取り）**: 実測 proxy 500gen≈7s(71 gen/s) /
rich 500gen≈25s(20 gen/s)。10K gen ≈ proxy 2.3min / rich 8min。+novelty(pop×archive k-NN) と
大容量 reservoir(4096) で 1 ラン ≈ 10–40min を見込む。sweep ~10–20 構成 × 5 seed = 50–100 ラン →
逐次で数〜十数時間、**並列ラン（独立プロセス, SR-4 隔離と整合）で <10h に収まる**。

**第一波（最小情報量で最大判別）**: baseline(scalar,no-std,no-archive,reservoir-off,500gen) vs
full(eps-lexicase,std,reservoir-1024,CVT,MC,MAP-Elites,**10K gen**)。多様性が gen10K で持続するか＝核仮説。

## 7. 反証基準 / 期待結果（falsifiable）

| 仮説 | 反証条件 |
|---|---|
| 標準化が「全満点収束」を防ぐ | std-on でも単一 cell へ収束したら反証 |
| novelty/lexicase が monoculture を防ぐ | max_lineage_share≥0.8 が続けば反証 |
| 中立貯蔵庫が特異性を供給 | reservoir-on と off で archive 成長/novelty に差が出なければ「bloat」確定 → 設計見直し |
| メタ進化が下回らない | adaptive run が固定 baseline を有意に下回れば反証（+ σ→0 崩壊をログで確認） |
| open-ended | Bedau で bounded/no-activity 分類なら「新しい AI は生まれていない」= 環境未達 |

## 8. 実装計画（要件着手ゲート通過後・既存資産再利用）

- 再利用: `diversity.py NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `nsga2.py` /
  `speciation.py` / `cma_es_diversity.py` / `MetaEvolutionLoop`(UCB1) / `fitness_rich.py` /
  `latent_reservoir.py` / `persona_evolution.py`(founder_lineage) / raptor governance（@govern 等）。
- 新規（小）: ε-lexicase selector / CVT 記述子 wrapper / 標準化記述子計算 / Bedau+MODES メトリクス /
  transgression scorer + 昇格ゲート / `c_cultural` 染色体 / `c_latent` の Genome3D 配線 + descriptor 連結。
- 配線方式: novelty/lexicase は `SchedulerFn`（集団文脈）に注入。c_meta dispatch 層。後方互換（META-5）。

## 9. honest disclosure
- 記述子設計（§3）が結果を大きく左右する＝**最大の自由度かつ最大の交絡**。複数方式 sweep で頑健性を見る。
- 教師なし記述子・記述子メタ進化は moving target（再現性/解釈性に注意）[SPEC]。
- proxy 段は mechanism feasibility。「新しい AI」の最終判定は実 LLM（Stage6, GO 待ち）。
- 人間文化因子は metaphor/着想（測定的接地でない, Stream D 注意）。

## 出典
- [[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] / [[OPEN_ENDED_CULTURAL_EVOLUTION]] / 研究 A–F findings docs
- CVT-MAP-Elites (Vassiliades 2016) / AURORA (Cully 2019) / VQ-Elites (2025) / QD-Meta-Evolution (Bossens & Tarapore 2021)
- Bedau et al. (1998) evolutionary activity; Dolson et al. MODES toolbox; OEE detection (2024)
