---
layout: default
title: "Meta-Evolution Research — Evolving the Evolutionary Algorithm Itself"
parent: "Research"
nav_order: 8
---

# Meta-Evolution — 進化アルゴリズム自体を進化させる (Research Stream A)

> **由来**: 2026-05-25 ユーザー指示「アルゴリズム部分でも進化の仕組みを追求する／
> あらゆる外部リソースを調べ上げて完璧な要件定義を見つける」。
> [[OPEN_ENDED_CULTURAL_EVOLUTION]] 原理 **#12** の falsifiable 要件定義化を担う系統 A。
> **対象**: `MetaChromosome` (algorithm_id / mutation_rate_per_layer / selection_pressure /
> novelty_weight 等) を **DEAD（誰も消費しない）状態から、ループを実際に駆動する遺伝的形質**へ昇格する。
> **honest disclosure**: 本系統の文献は古典 EC（Eiben/Hansen/Schmidhuber）が主。LLM×EA 側
> （Promptbreeder/EUREKA 等）は既存 [[llm_evolutionary_prior_art]] が担当済 → 本 doc は重複を避け、
> **古典メタ進化・パラメータ制御・自己適応・hyper-heuristic・自己参照** に集中する。
> 投機的な主張・未検証の前提はすべて §6 で明示フラグ。

---

## 0. 現状コードの診断（要件定義の出発点）

| 構成要素 | 場所 | 状態 |
|---|---|---|
| `MetaChromosome` (frozen dataclass) | `llive/src/llive/perf/evolutionary/meta_chromosome.py` | ✅ 存在。validation/serialization/`sample_neighborhood`/`kolmogorov_proxy`(gzip) まで実装 |
| `MetaEvolutionLoop` (UCB1 algorithm selection) | `meta_loop.py` | ✅ 存在。register / `select_next`(UCB1) / `record_delta` / `expand_neighborhood`。**ただし apply は mock dispatch のみ** |
| meta-evolution PoC | `experiments/meta_evolution_poc/poc.py` | ✅ 50gen×3alg×8seed で UCB1 が high arm を支配的に選ぶことを実証済 |
| **実 `EvolutionLoop` への配線** | — | ❌ **未配線（DEAD）**。`algorithm_id` で実際に選択方式を切り替える dispatch、`mutation_rate_per_layer` を実 mutation に流す経路、`selection_pressure` を実 selection に流す経路、いずれも存在しない |

**結論**: 機構は skeleton として揃っている。欠けているのは **MetaChromosome の各フィールドを実ループの
挙動に結線する dispatch 層** と、**メタ層を「進化」させた時に必ず起きる病理（mutation rate→0 collapse /
選択圧消失 / runaway）への対策**。この 2 点を falsifiable 要件として確定するのが本 doc の目的。

---

## 1. 技術一覧表（name / 1-line / citation / maturity）

maturity 凡例: **Established**（数十年の実績）/ **Mature**（査読・再現多数）/ **Emerging**（2020 以降・有望だが少数）/ **Speculative**（理論先行・実装難）。

| # | 技術 | 1-line | citation / URL | maturity |
|---|---|---|---|---|
| T1 | **パラメータ制御 4 分類** | tuning（事前）/ deterministic（時間関数）/ adaptive（フィードバック）/ self-adaptive（パラメータを genome に埋め共進化） | Eiben, Hinterding & Michalewicz (1999), IEEE TEC 3(2):124–141. [PDF](https://www.cs.vu.nl/~gusz/papers/2007-eib-mich-schoen-smit-chap.pdf) | Established |
| T2 | **Rechenberg 1/5 成功則** | 突然変異成功率 > 1/5 なら step を拡大、< 1/5 なら縮小（最も古い adaptive step-size 制御） | Rechenberg (1973) *Evolutionsstrategie*; Beyer & Schwefel (2002) ES tutorial | Established |
| T3 | **自己適応 σ (ES)** | mutation step σ を個体の genome に符号化し、σ 自身も変異・選択を受ける（log-normal 摂動） | Schwefel (1981); Beyer & Schwefel (2002). [Survey](https://link.springer.com/article/10.1007/s12065-010-0035-y) | Established |
| T4 | **CMA-ES + CSA** | 共分散行列を進化パスから適応、step-size は累積ステップ長制御（CSA）で derandomized 調整 | Hansen & Ostermeier (2001); [tutorial arXiv:1604.00772](https://arxiv.org/pdf/1604.00772) | Mature |
| T5 | **Adaptive Operator Selection (AOS) + 多腕バンディット** | 各 variation operator を bandit の arm とし、credit assignment（過去子孫の fitness 改善）→ UCB/DMAB で選択確率を適応 | DaCosta, Fialho, Schoenauer & Sebag (2008) GECCO; Fialho et al. (2010). [HAL](https://inria.hal.science/inria-00278542v2) | Mature |
| T6 | **Hyper-heuristics（selection / generation）** | 「ヒューリスティクスを選ぶヒューリスティクス」。selection HH＝既存 low-level heuristic を選択、generation HH＝GP 等で新 heuristic を合成 | Burke et al. (2013) JORS survey; Cowling et al. (2000) Choice Function. [survey PDF](https://www.cs.stir.ac.uk/~goc/papers/hhsurvey.pdf) | Mature |
| T7 | **Meta-GA / meta-EA** | 外側 EA が内側 EA のパラメータ（pop size / pc / pm / selection）を進化させる入れ子最適化 | Grefenstette (1986); Eiben et al. (1999) §「meta-GA」 | Established |
| T8 | **AutoML-Zero** | 基本数学演算（命令列）から ML アルゴリズム全体を進化探索。SGD/BP/2層 NN を「再発見」 | Real, Liang, So & Le (2020). [arXiv:2003.03384](https://arxiv.org/abs/2003.03384) | Emerging |
| T9 | **Gödel machine（自己参照最適自己改善）** | 効用が向上する証明が得られた時のみ自分自身のコードを書き換える、証明探索ベースの自己改善 | Schmidhuber (2003/2009). [IDSIA](https://people.idsia.ch/~juergen/goedelmachine.html) | Speculative |
| T10 | **Meta-Learning by the Baldwin Effect** | 学習が進化を導く（Baldwin）を deep net の初期値/hyperparam に適用、MAML 同等性能を**勾配 BP 無し**で達成 | Fernando et al. (2018). [arXiv:1806.07917](https://arxiv.org/abs/1806.07917) | Emerging |
| T11 | **Promptbreeder（自己参照変異）** | mutation prompt 自体を進化させる self-referential 層（LLM 文脈での meta-mutation） | Fernando et al. (2023). [arXiv:2309.16797](https://arxiv.org/abs/2309.16797)（既存 [[llm_evolutionary_prior_art]] でも言及） | Emerging |
| T12 | **GESMR（Group Elite Selection of Mutation Rates）** | 解集団と mutation-rate 集団を共進化。group の**最良**変異で MR を評価し vanishing-MR を回避 | Kim, Yang & Lehman (2022) GECCO. [arXiv:2204.04817](https://arxiv.org/pdf/2204.04817) | Emerging |
| T13 | **POET / Minimal Criterion Coevolution** | 解と環境（タスク）を共進化させ open-ended に複雑化。minimal criterion で「簡単すぎ/難しすぎ」を排除 | Wang et al. (2019) POET; Brant & Stanley (2017) MCC | Emerging |

---

## 2. 病理と既知の失敗モード（要件の制約条件になる）

> メタ進化を「動かす」前に、**動かすと必ず起きる病理**を要件で先に潰す。これが honest disclosure の核。

- **P1: mutation rate → 0 collapse**。mutation_rate を自己適応させると、ほとんどの変異は fitness を下げるため
  「変異しない個体」が短期最適となり MR が 0 へ崩壊 → 進化停止・早期収束。実証された脆弱性
  （[Effective Mutation Rate Adaptation, arXiv:2204.04817](https://arxiv.org/pdf/2204.04817);
  [Wikipedia: Premature convergence](https://en.wikipedia.org/wiki/Premature_convergence)）。
  **対策**: GESMR（group の最良変異で MR を評価）/ MR 下限クランプ / σ floor。
- **P2: 選択圧の消失（loss of selection pressure）**。`selection_pressure` や `novelty_weight` を進化対象に
  すると、「淘汰されない（= selection_pressure を下げる）」方向が短期的に有利になり、メタ層が自分への
  選択圧を弱める方向へドリフトしうる。novelty_weight=1.0 へ振り切ると目的勾配が消える。
- **P3: runaway / 自己強化ループ**。メタ層が「メタ層自身を守る」方向に固着（meta_mutation_decay→1.0 で
  メタ変異が止まる、あるいは逆に発散）。Schmidhuber 風の能動拡張（`expand_neighborhood`）は探索空間を
  単調膨張させるため、予算なしでは制御不能。
- **P4: 信用割当のタイムスケール不整合**。AOS の credit assignment は「直近の改善」を見るが、進化的に
  有益な変異は**遅延報酬**（Baldwin 効果 #9 と同じ構造）。短期 credit で評価すると探索的 operator が
  不当に淘汰される。
- **P5: 計測純度の汚染**。メタ層の delta（algorithm 改善量）を proxy fitness で測ると、proxy の歪みが
  メタ選択にそのまま乗る。実 LLM 評価とは分離記録必須（[[feedback_llive_measurement_purity]]）。
- **P6: 非定常性**。集団状態が世代で変わるため「どの algorithm が良いか」は非定常。固定 UCB1 は定常前提。
  DMAB（Page-Hinkley change detection 付き）が対策（T5）。

---

## 3. Falsifiable 要件文（the system MUST / SHOULD …）

> 各要件に **反証可能な acceptance 条件**（測れる・落とせる）を付す。ID は `META-Rxx`。

### A. MetaChromosome を実ループに結線する（DEAD → LIVE）

- **META-R01 (MUST)**: `algorithm_id` は実 `EvolutionLoop` の selection/variation スキームを切り替える
  dispatch を駆動しなければならない。
  *Acceptance*: 同一 seed・同一初期集団で `algorithm_id ∈ {tournament_gauss, nsga2_novelty,
  map_elites_niche}` を入れ替えたとき、世代0以降の集団軌跡が **観測可能に異なる**（軌跡ハッシュ差 > 0）。
  入れ替えても挙動が同一なら配線されていない証拠 → FAIL。
- **META-R02 (MUST)**: `mutation_rate_per_layer = (c_impl, c_prompt, c_meta)` は対応する各染色体層の
  実 mutation 確率/強度を制御しなければならない。
  *Acceptance*: c_prompt の rate を 0.0 に固定した run では c_prompt 層の遺伝子が全世代で不変、
  0.5 にした run では平均変化量が単調増。
- **META-R03 (MUST)**: `selection_pressure`（truncation top-N 比）は実 selection の生存数を決めなければ
  ならない。*Acceptance*: pressure=0.1 と 0.9 で、生存個体の親集団内 fitness 分位が統計的に分離（KS 検定 p<0.05）。
- **META-R04 (SHOULD)**: `novelty_weight` は Stage2 novelty scheduler の M/(N+M) 比を駆動し、
  原理 #2/#3（中央を報酬にしない・novelty 選択）と整合しなければならない。
  *Acceptance*: weight を上げると archive 内多様性指標（mean pairwise descriptor distance）が単調増。

### B. メタ層を「進化」させる（heritable evolvable traits）

- **META-R05 (MUST)**: メタ層パラメータ（mutation rate / selection / operator choice）は **遺伝・変異・選択を
  受ける heritable trait** として扱い、自己適応 ES（T3）または AOS バンディット（T5）の少なくとも一方で
  オンライン適応しなければならない。*Acceptance*: メタ層を固定した baseline run と適応 run を比較し、
  適応 run が **同等以上**の best/diversity を達成（劣化なら採用しない）。
- **META-R06 (MUST)**: operator 選択は credit assignment + 多腕バンディット（UCB1 既存 / DMAB 望ましい）で
  行い、各 operator の使用回数・平均報酬をログに残さなければならない（監査可能性 [[feedback_implementation_status_record]]）。
  *Acceptance*: snapshot JSON に operator 別 `use_count` / `mean_delta` が出力され、明らかに有益な
  operator が劣 operator より高使用率になる（PoC で実証済の性質を実ループで再現）。
- **META-R07 (SHOULD)**: メタ層は **deterministic（時間関数）/ adaptive（フィードバック）/ self-adaptive
  （共進化）** の 3 モードを設定で選べ、既定は self-adaptive とする（Eiben 分類 T1 に明示準拠）。

### C. 病理対策（§2 の制約を要件化）

- **META-R08 (MUST)**: mutation rate / σ には **下限クランプ**（floor）を設け、`mutation_rate → 0` collapse
  （P1）を構造的に防がなければならない。あるいは GESMR（T12）方式で group 最良変異により MR を評価する。
  *Acceptance*: 任意の 500 世代 run で全層の実効 mutation rate が floor 以上を維持（log で検証、min > floor）。
- **META-R09 (MUST)**: `selection_pressure` と `novelty_weight` の進化可能レンジは **下限 > 0 / 上限 < 1** に
  bound し、選択圧消失（P2）と目的勾配消失を防がなければならない。
  *Acceptance*: validation（既存 `__post_init__` は既に `0 < selection_pressure ≤ 1`）に加え、
  実効レンジを `[ε, 1-ε]` にクランプ。pressure が境界に張り付く頻度をログ化し閾値超なら警告。
- **META-R10 (MUST)**: メタ層の探索空間能動拡張（`expand_neighborhood`, Schmidhuber 風 T9）は **予算上限**
  （max candidates / 世代あたり追加数）を持ち、runaway（P3）を防がなければならない。
  *Acceptance*: candidate 数が設定上限で頭打ちになる（単調膨張しない）。
- **META-R11 (SHOULD)**: credit assignment は **遅延報酬**（直近 N 世代窓の最良 delta、平均でなく extreme value）を
  使い、探索的 operator の早期淘汰（P4）を緩和すべき（Fialho extreme-value reward T5、`recent_mean_delta` を
  extreme 版に拡張）。

### D. 計測純度・監査・再現性

- **META-R12 (MUST)**: メタ層の delta は proxy/real ラベル付きで分離記録し、proxy の歪みがメタ選択へ
  混入しても後から切り分け可能でなければならない（P5、[[feedback_llive_measurement_purity]]）。
  *Acceptance*: snapshot に `is_proxy` フラグ。real LLM run（ollama, GO 待ち）と proxy run のメタ統計を別管理。
- **META-R13 (MUST)**: メタ進化を**有効化しても既存 run は後方互換**でなければならない（meta を固定値に
  すれば従来挙動に一致）。*Acceptance*: `MetaChromosome.default()` 固定で従来 v0.B/v0.C run の結果が再現。
- **META-R14 (SHOULD)**: メタ層が「自己改善した」と主張する前に、必ず **固定メタ baseline との対照実験**を
  添付すべき（[[feedback_benchmark_honest_disclosure]]）。異常に良い結果は内訳を疑う。

---

## 4. 設計原理（#1–#12）へのマッピング

| 原理 | 本系統の寄与 | 関連要件 |
|---|---|---|
| **#12 アルゴリズム部分でも進化** | 本 doc の主目的そのもの。MetaChromosome を LIVE 化し、選択方式・変異率・operator を heritable trait に | META-R01〜R07 |
| #2 中央を報酬にしない | `novelty_weight` を実 scheduler に結線（中央一致を報酬から外す機構をメタ層で調整） | META-R04, R09 |
| #3 novelty / 特異が生き残る | algorithm_id=`nsga2_novelty` / `map_elites_niche` を実ディスパッチ。novelty 選択をメタ層が選べる | META-R01, R04 |
| #9 学習が進化を導く（Baldwin） | メタ層自体が「遅延報酬での学習」構造（T10 Baldwin meta-learning と同型）。credit assignment は学習信号 | META-R11；belief space 連携は系統 D |
| #10 染色体を増やす（消費目的とセット） | MetaChromosome は「増やした次元」。**消費目的（実ループ駆動）とセット**でなければ中立ドリフト化 → DEAD のまま | META-R01〜R03（消費の担保） |
| #11 単一最適でなく多様性の地図 | `map_elites_niche` algorithm を実装し QD アーカイブをメタ層が選べる | META-R01, R04 |

> **重要な整合**: 原理 #10 は「次元を増やすなら**消費目的とセット**で（さもなくば中立ドリフト）」と明記。
> 現状 MetaChromosome はまさに「増やしたが消費されていない＝DEAD」状態。本系統 A の存在理由は
> **#10 の警告を MetaChromosome について解消すること**に集約される。

---

## 5. ADOPT vs AVOID（正直な理由つき）

### ADOPT（採用推奨）

| 技術 | 理由 | 注意 |
|---|---|---|
| **T1 Eiben 分類** | 要件の語彙基盤。deterministic/adaptive/self-adaptive を設定軸にすれば設計が明快（META-R07） | 分類は枠組みであり手法ではない |
| **T5 AOS + バンディット** | 既に UCB1（`ucb1_score` / `MetaEvolutionLoop`）が実装済。operator 選択へ**そのまま転用可能**。配線コスト最小 | 非定常性（P6）→ 将来 DMAB へ |
| **T3 自己適応 σ + T2 1/5 則** | 古典・堅牢。`self_adaptive_sigma` algorithm_id が既にレジストリにある。floor クランプ（META-R08）と併用 | 単独だと P1 collapse |
| **T12 GESMR** | P1（MR→0）の**直接的処方**。集団を group 化し最良変異で MR 評価。派生集団進化（v0.C/D/E）と親和的 | 実装やや重い → SHOULD 扱い |
| **T11 Promptbreeder 型 self-referential** | LLM 文脈での meta-mutation。Stage6（実 LLM）以降の拡張先。既存 prior_art と接続 | credential 待ち。今は scope 外 |

### AVOID / 慎重（今は採らない）

| 技術 | 理由（honest） |
|---|---|
| **T9 Gödel machine（完全版）** | 証明探索が計算不能・実装不能（Schmidhuber 自身が認める brittleness/safety 問題）。**gzip K-proxy + UCB1 近似**（既存実装）に留め、「証明ベース自己改善」は思想的 anchor としてのみ参照。完全実装は **Speculative**、要件には入れない |
| **T8 AutoML-Zero（フル）** | 命令列から algorithm 全体を進化＝探索空間が天文学的。Google 規模の計算が前提。on-prem 単機では非現実的。**algorithm_id レジストリ（離散選択）に留める**のが現実解。「AST encoded bytes へ拡張」は将来の野心であり今期要件外 |
| **無制約な meta_mutation 進化** | P1/P2/P3 を全て誘発。**必ず floor/bound/budget（META-R08〜R10）とセットでのみ**有効化 |
| **expand_neighborhood の無予算運用** | runaway（P3）。予算上限なしでは禁止（META-R10） |
| **proxy だけでメタ自己改善を主張** | P5。[[feedback_benchmark_honest_disclosure]] 違反。必ず固定メタ baseline 対照（META-R14） |

---

## 6. Open Questions（投機・未検証フラグ）

1. **[未検証]** UCB1（定常前提）で集団状態の非定常性（P6）にどれだけ耐えるか。DMAB（Page-Hinkley）への
   移行が必要になる世代規模の閾値は未測定。要 PoC（500gen で UCB1 vs DMAB の regret 比較）。
2. **[投機]** メタ層 delta の「遅延報酬」構造（P4）は Baldwin 効果（#9）と**同型**と本 doc は主張するが、
   これは概念的アナロジーであり形式的同値性は未証明。要 honest disclosure。
3. **[未確定]** self-adaptive（共進化）と AOS（バンディット）を**併用**したときの干渉（二重適応の不安定性）。
   どちらか一方を既定にすべきか、層で分けるべきか（例: 連続パラメータ=self-adaptive σ、離散 operator=AOS）未決。
4. **[未検証]** mutation rate floor（META-R08）の適正値。floor が高すぎると収束阻害、低すぎると P1。
   層別（c_impl/c_prompt/c_meta）に異なる floor が要るか未測定。
5. **[scope 境界]** algorithm_id の離散レジストリ（現状）と「AST encoded bytes へ拡張」（AutoML-Zero 路線）の
   境界をどこに引くか。本 doc は**離散レジストリで十分**と判断するが、open-ended 性（#11）の観点では
   将来 generation hyper-heuristic（T6 後半）で「新 algorithm を合成」する余地がある。今期は AVOID。
6. **[要他系統連携]** メタ層の credit を **belief space**（Cultural Algorithm, #9 / 系統 D）へ流し込めば
   「集団が学んだメタ戦略」を共有知識化できる。系統 D（文化・学習）との結線は本 doc の射程外だが有望。

---

## 7. References

### パラメータ制御・自己適応（古典）
- Eiben, A.E., Hinterding, R., Michalewicz, Z. (1999). *Parameter Control in Evolutionary Algorithms.* IEEE TEC 3(2):124–141. [PDF](https://www.cs.vu.nl/~gusz/papers/2007-eib-mich-schoen-smit-chap.pdf)
- Rechenberg, I. (1973). *Evolutionsstrategie.* （1/5 成功則）
- Beyer, H.-G., Schwefel, H.-P. (2002). *Evolution Strategies: A Comprehensive Introduction.* Natural Computing 1.
- Kramer, O. (2010). *Evolutionary self-adaptation: a survey.* Evolutionary Intelligence. [link](https://link.springer.com/article/10.1007/s12065-010-0035-y)
- Hansen, N., Ostermeier, A. (2001). *Completely Derandomized Self-Adaptation in Evolution Strategies (CMA-ES).* Evol. Comput. 9(2). [tutorial arXiv:1604.00772](https://arxiv.org/pdf/1604.00772)

### Adaptive Operator Selection / Hyper-heuristics
- DaCosta, L., Fialho, Á., Schoenauer, M., Sebag, M. (2008). *Adaptive Operator Selection with Dynamic Multi-Armed Bandits.* GECCO. [HAL](https://inria.hal.science/inria-00278542v2)
- Fialho, Á. et al. (2010). *Extreme value based reward / DMAB for AOS.*
- Auer, P., Cesa-Bianchi, N., Fischer, P. (2002). *Finite-time Analysis of the Multiarmed Bandit Problem.* （UCB1）
- Burke, E.K. et al. (2013). *Hyper-heuristics: A Survey of the State of the Art.* JORS. [PDF](https://www.cs.stir.ac.uk/~goc/papers/hhsurvey.pdf)
- Cowling, P., Kendall, G., Soubeiga, E. (2000). *A Hyperheuristic Approach to Scheduling (Choice Function).*

### Meta-EA / 自己参照 / Baldwin
- Grefenstette, J.J. (1986). *Optimization of Control Parameters for Genetic Algorithms.* IEEE SMC.（meta-GA）
- Real, E., Liang, C., So, D.R., Le, Q.V. (2020). *AutoML-Zero.* [arXiv:2003.03384](https://arxiv.org/abs/2003.03384)
- Schmidhuber, J. (2003/2009). *Gödel Machines.* [IDSIA](https://people.idsia.ch/~juergen/goedelmachine.html)
- Fernando, C. et al. (2018). *Meta-Learning by the Baldwin Effect.* [arXiv:1806.07917](https://arxiv.org/abs/1806.07917)
- Fernando, C. et al. (2023). *Promptbreeder.* [arXiv:2309.16797](https://arxiv.org/abs/2309.16797)

### 病理・open-ended
- Kim, A., Yang, J., Lehman, J. (2022). *Effective Mutation Rate Adaptation through Group Elite Selection (GESMR).* GECCO. [arXiv:2204.04817](https://arxiv.org/pdf/2204.04817)
- *Premature convergence.* [Wikipedia](https://en.wikipedia.org/wiki/Premature_convergence)
- Wang, R. et al. (2019). *POET: Open-Ended Coevolution of Environments and their Optimized Solutions.* GECCO.
- Brant, J.C., Stanley, K.O. (2017). *Minimal Criterion Coevolution.* GECCO.

### llive 内部 cross-reference
- `llive/src/llive/perf/evolutionary/meta_chromosome.py` / `meta_loop.py`（本系統の改修対象）
- `llive/experiments/meta_evolution_poc/poc.py`（UCB1 選択の PoC、実証済）
- `llive/docs/requirements_v0.I_meta_evolution_and_cross_substrate.md` §3（形式化の出典）
- [[OPEN_ENDED_CULTURAL_EVOLUTION]] 原理 #10/#12 / [[llm_evolutionary_prior_art]]（LLM×EA 側、重複回避）
- [[feedback_llive_measurement_purity]] / [[feedback_benchmark_honest_disclosure]] / [[feedback_implementation_status_record]]
