# 開放端・文化的進化 — 統合マスター設計 (Open-Ended Cultural Evolution)

> **由来**: 2026-05-25 ユーザーとの設計対話（「進化として成立しているか」から始まり 11 原理に到達）。
> **位置づけ**: llive persona 進化を「本物の進化／差別化を生む系」にするための統合設計。
> [[PERSONA_FX]] を**核**に据え、文化因子・中立貯蔵庫・novelty 選択・学習層で拡張する。
> **honest disclosure**: 全て proxy（決定論, LLM 非呼出）。実 LLM 評価は最終段（ollama, GO 待ち）。
> **前段記録**: 診断と Stage1 実測は [[evolution_fitness_redesign_2026_05_25]]。

## 0. 出発点 — proxy 進化はなぜ「成立しない」か（実測）

旧 `_proxy_fitness` = `0.7*balance + 0.3*provenance`、c_factors(10×4) を層平均10次元に圧縮。
⇒ 目的は **単峰（全因子を均等に高く）**。実測（seed2/500gen）: founder 全絶滅 gen23 /
best 頭打ち gen281 / 多様性崩壊 gen25。Stage1（多峰 rich-proxy）で絶滅は解消したが、
founder を峰に置いたため best=1.0 が gen0 から＝**勾配ゼロ**。⇒ ユーザーの 11 原理で再設計。

## 1. 設計原理（ユーザー）→ 機構（先行研究）→ 実装

| # | 原理（ユーザー 2026-05-25） | 機構（研究） | 実装 |
|---|---|---|---|
| 1 | 全因子満点はダメ／正規化・標準化を | 絶対値除去で相対構造のみ残す | **z-score 標準化**した記述子（全満点→フラット→無特徴） |
| 2 | 保守／中央が勝つ系では新規も差別化も無理 | 中央を報酬にしない | 中心一致を報酬から外す |
| 3 | 進化は突然変異から。**特異**が生き残れ | **novelty search**（Lehman & Stanley: 目的は欺瞞、新規性が勝つ） | fitness = 記述子の新規性（集団+archive 距離） |
| 4 | 標準化で特異が出るには**余計な因子**が要る | **中立ネットワーク／縮退／中立ドリフト**（Kimura, Whitacre&Bender） | **`LatentReservoirChromosome`**（意味なし自由遺伝子＝exaptation 材料）✅着地 |
| 5 | 個体差は遺伝子の**限られた部分**から（生物の比率） | ヒト個体差 ~0.1%・コード ~1-2%。小調節変化が大効果（evo-devo） | **大規模ゲノム + 疎変異**（毎世代ごく一部だけ変異）✅着地 |
| 6 | 人間の**文化・文明・多様性**から因子が生まれる | Hofstede / Schwartz / WVS(Inglehart-Welzel) / Big Five / dual-inheritance | **`CulturalChromosome`**（下記§3 の人間要素因子セット）※新規 |
| 7 | 各個体が**人間の要素を取り込む** | 文化的形質を個体が保持 | 各 Individual が CulturalChromosome を持つ |
| 8 | 上位者が一方的に与えず、**希望する個体が獲得** | 水平的文化伝達／ミーム（Dawkins, Boyd&Richerson） | **PERSONA-FX**: pull 型獲得（逸脱個体が相関 argmax で獲得、persona 側 uniqueness、0..N、隔世） |
| 9 | **経験・学習**を与えると実現確率が上がる | **Baldwin 効果**（Hinton&Nowlan: 学習が進化を導く）＋ **Cultural Algorithm belief space**（Reynolds） | per-個体 経験／記憶層 + 共有 belief space（best が更新） |
| 10 | 染色体／次元を増やす | 進化性の原材料（ただし**消費目的とセット**で） | 文化染色体＋貯蔵庫を**記述子/選択が読む**形で追加（中立ドリフト化を回避） |
| 11 | 最適解が賢いとは限らない | open-ended evolution（変異+遺伝+選択だけでは不十分） | 成果物＝**単一最適でなく QD アーカイブ**（多様な認知・文化スタイルの地図） |
| 12 | **アルゴリズム部分でも進化の仕組みを追求** | **メタ進化／自己適応 EA**（AutoML-Zero, hyper-heuristics, self-adaptive σ, Gödel machine） | `c_meta` を実際に消費（現状デッド）し、**進化演算子・選択・変異率そのものを進化**させる。belief space と接続 |

> **要件定義モード（2026-05-25 ユーザー指示）**: 「徹底的に要件定義を精査し完璧な要件定義を見つける／
> あらゆる外部リソースを調べ上げる」。本設計を **falsifiable な要件定義**へ昇格させるため、4 系統
> （メタ進化 / open-endedness / 表現・選択 / 文化・学習）の網羅文献掃討を並列実施中（findings docs を
> 本 research/ 配下に蓄積 → 要件定義へ統合）。実装着手は要件確定後。

## 2. アーキテクチャ（層）

```
個体 (Individual)
├─ ゲノム (進化・遺伝)
│   ├─ c_factors        10×4 思考因子   … 意味あり・標準化して記述子へ (#1)
│   ├─ c_cultural        人間要素因子    … §3、意味あり・記述子へ (#6,#7)  ※新規
│   ├─ c_latent          中立貯蔵庫(大)  … 余計な因子・疎変異・記述子へ (#3,#4,#5) ✅
│   └─ c_impl/c_prompt/c_meta            … 既存 (構造選択)
├─ 経験・学習 (lifetime, 非遺伝 or Baldwin 同化)        … #9 ※新規
│   └─ 個体記憶 / belief 参照
└─ 獲得ペルソナ集合 (毎世代 pull 再選定, 遺伝しない)     … #8 PERSONA-FX

集団レベル
├─ belief space (Cultural Algorithm): best 個体が共有知識を更新 → 適応誘導   #9
├─ persona プール (文化ライブラリ): 1 エントリ追加で拡張                    #8
└─ QD アーカイブ (MAP-Elites): 多様な cell ごとの elite を保存 = 成果物     #11
```

**選択（中核）**: スカラー最大化を捨て、**標準化記述子（c_factors⊕c_cultural⊕c_latent）の novelty**
で選択（#1,#2,#3）。novelty は集団文脈が要るが llive の `SchedulerFn` は集団全体を受け取るので
そこに注入（per-individual fitness の制約を回避）。QD アーカイブで「単一最適でなく多様性の地図」（#11）。

**ペルソナ（PERSONA-FX 核, 既存設計）**: 遺伝しない。プール常駐 persona を、平均から逸脱した
（＝特異な, #3 と同じ novelty 軸）個体が相関 argmax で獲得。persona 側 uniqueness（1 persona≤1 個体）、
個体側 0..N（多才 hub/generic 創発）、相関個体不在→休眠→隔世復活。**獲得＝報酬**にすると
「平均を外れること」自体が選択圧＝多様性エンジン内蔵（#8, #2 の解）。

**学習（#9, Baldwin+Cultural Algorithm）**: 個体は生涯で経験／記憶を蓄積し、それが persona 獲得や
proxy 適応度の実現確率を上げる（学習が地形を均し進化を導く＝Baldwin）。best 個体が集団の
belief space を更新し後続を導く（Reynolds）。honest: 学習信号と遺伝 fitness は分離記録
([[feedback_llive_measurement_purity]] / PERSONA_FX §4)。

## 3. 人間要素 因子セット（#6 の調査結果 → 候補因子）

`CulturalChromosome` に載せる候補（各 [0,1] or [-1,1]、組合せが差別化を生む）:

- **Schwartz 10 基本価値**: self-direction / stimulation / hedonism / achievement / power /
  security / conformity / tradition / benevolence / universalism。
- **Hofstede 6 文化次元**: power-distance / individualism–collectivism / masculinity–femininity /
  uncertainty-avoidance / long-term-orientation / indulgence–restraint。
- **WVS / Inglehart-Welzel 2 軸**: traditional↔secular-rational / survival↔self-expression。
- **Big Five (OCEAN)**: openness / conscientiousness / extraversion / agreeableness / neuroticism。
- **認知スタイル**: analytic↔holistic (Nisbett) / 文化的 tightness↔looseness (Gelfand)。
- **社会的学習バイアス (dual-inheritance)**: conformist / payoff-biased / prestige-biased 伝達。

設計判断: 全部を一度に載せず、まず **Schwartz10 + Big Five + WVS2軸**（計 ~17 次元、確立・直交性が
比較的高い）を初版に。意味のある文化因子（標準化して novelty 記述子へ）＋ c_latent（中立）の
**併存**が #3-#6 の核（意味因子で「人間らしさ」、中立貯蔵庫で「予期せぬ特異」）。

## 4. 段階実装計画（測定優先・各段で baseline と可視化比較）

- **Stage 1** ✅ 着地: 多峰 rich-proxy（全40次元+persona archetype）+ founder_lineage 来歴 + P2 可視化。
- **Stage 2 (次)**: **標準化 + novelty scheduler**（#1,#2,#3,#11）。`SchedulerFn` に集団相対 novelty を注入、
  記述子 = z-score(c_factors⊕c_latent)。QD アーカイブ（既存 `MAPElitesGrid` 流用）。
  → 実測: best 単調収束が消え、多様性が高止まり・特異個体が持続するか。
- **Stage 3**: **`CulturalChromosome`**（§3 初版 17 次元）を Genome3D に追加（記述子へ混ぜる＝#10 の消費目的とセット）。
- **Stage 4**: **PERSONA-FX 配線**（pull 獲得 pass を本ループに、`demo_persona_fx.py` の核を実装層へ）。獲得＝報酬で多様性エンジン化。
- **Stage 5**: **学習層**（#9, Baldwin + Cultural Algorithm belief space）。個体記憶 + 集団 belief。
- **Stage 6**: 実 LLM fitness（ollama, GO 待ち）で proxy を上書き。

各段は既存安全弁（collapse guard / eval_timeout）の上、extensibility 契約遵守（既存 run 後方互換）。
全 viz に proxy/real ラベル（[[feedback_benchmark_honest_disclosure]]）。

## 5. 差別化（正直に）

基盤（novelty search / QD / 中立ネットワーク / Cultural Algorithm / 文化次元）はいずれも既存。
FullSense 独自性は **(意味ある文化因子 + 中立貯蔵庫) × 標準化 novelty × pull 型 persona 獲得（PERSONA-FX）
× Baldwin 学習 × on-prem 監査** の**統合**と、「保守を淘汰し変異由来の特異が生き残る」「最適解でなく
多様性の地図を成果物にする」という設計思想の一貫性。

## 6. 既存コード接続

- ✅ `llive/.../fitness_rich.py`（Stage1 多峰）/ `latent_reservoir.py`（#3,#4,#5 中立貯蔵庫）
- ✅ `persona_evolution.py`（founder_lineage 来歴 + is_proxy）/ `evolution_lineage_viz.py`（P2 可視化）
- 流用: `diversity.py NoveltyScorer`（逸脱/novelty）/ `quality_diversity.py MAPElitesGrid + PersonaOverlapPenalty` /
  `nsga2.py` / `speciation.py` / `persona.py factor_affinity`（相関）/ `demo_persona_fx.py`（PERSONA-FX 核 PoC）
- 新規: `CulturalChromosome`（§3）/ novelty `SchedulerFn`（Stage2）/ persona 獲得 pass（Stage4）/ belief space（Stage5）

## 参考文献
- Lehman & Stanley (2011) Abandoning Objectives; Stanley & Lehman (2015) Why Greatness Cannot Be Planned
- Kimura (1968) 中立説; Whitacre & Bender (2010) Degeneracy; 中立ネットワーク (Schuster, Wagner)
- Hinton & Nowlan (1987) How Learning Can Guide Evolution（Baldwin）; Reynolds (1994) Cultural Algorithms
- Hofstede 文化次元; Schwartz 基本価値; Inglehart & Welzel (WVS); Boyd & Richerson 二重継承; Nisbett; Gelfand
- 関連: [[PERSONA_FX]] / [[evolution_fitness_redesign_2026_05_25]] / [[goal_evolution_run_and_viz]] /
  [[project_llive_evolution_next_session]] / [[project_persona_fx]]
