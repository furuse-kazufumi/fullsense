# 進化研究 — 広域アルゴリズムサーベイ & 適合評価 (Stream G)

> **由来**: 2026-05-25 ユーザー指示「様々なアルゴリズムを調べて検討せよ」.
> **位置づけ**: Stream A–F が深掘りした手法群（novelty search / MAP-Elites / NSLC / ε-lexicase /
> NSGA / FUSS / island / self-adaptive ES / UCB1 AOS / GESMR / Cultural Algorithms / Baldwin /
> AlphaEvolve・FunSearch・DGM・CycleQD・OMNI・ELM・ADAS）の**外側**を広域に掃討し、本系の要件
> （[[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] / [[OPEN_ENDED_CULTURAL_EVOLUTION]]）への適合を
> ADOPT / CONSIDER / AVOID で評価する。
> **honest disclosure**: 我々の規模（token 級ゲノム ~32k+ 遺伝子・低次元記述子・10K 世代・on-prem proxy）で
> **未検証**な箇所は明示。hype（特に LLM-as-operator 系）は割り引く。
> **出典**: WebSearch（2026-05-25, ユーザー許可）+ raptor corpus `evolutionary_computation_corpus`（616 papers）.

## 0. 評価軸（我々の要件への射影）

我々の系の制約は他の進化系と質的に異なる。評価はこの 5 軸で行う:

1. **large genome (GENOME-1)**: ~32k 遺伝子（LLM 語彙級）まで上限 sweep。多くは fitness 中立。
2. **low-dim descriptor (DESC-1)**: 行動記述子は低次元（8–50）へ縮約。生の高次元 k-NN は次元の呪いで無意味。
3. **sustained diversity / open-endedness (QD-1, OE-3, RUN-1)**: 10K 世代末尾でも新 cell 増加・monoculture<0.8。
4. **on-prem (SCOPE-1, ADOPT-3)**: cloud frontier LLM・大規模計算に依存しない。proxy 段は LLM 非呼出。
5. **governance (SR-1..4)**: 個体=データのみ・純粋評価・迂回不能メタガバナンス・fail-closed。

---

## 1. 大評価表（アルゴリズム × 適合）

凡例: **H2D?** = scales-to-high-dim genome / **OP?** = on-prem 純 CPU で現実的か / 判定 = ADOPT / CONSIDER / AVOID

### 1.1 連続 EA（continuous black-box optimizers）

| アルゴリズム | family | 1-line mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **CMA-ES** (Hansen 2003) | covariance ES | 共分散行列を適応し探索分布を回転・伸縮 | ✗ O(n²) mem/O(n³) update | △ | **CONSIDER（小ブロックのみ）** | 既に `cma_es.py` 着地。**だが 32k 次元では full-CMA は破綻**（共分散 32k² ≈ 10⁹ 要素）。意味因子ブロック（40-dim c_factors）に限定使用。large genome 全体には不可。 |
| **sep-CMA-ES** (Ros & Hansen 2008) | diagonal CMA | 共分散を対角に制限し O(n) に | ✓ | ✓ | **ADOPT（高次元 σ 適応の第一候補）** | 対角化で 32k 次元でも線形コスト。**large genome の σ 適応**にそのまま使える。full-CMA の回転は捨てるが、我々は座標独立な疎変異前提なので損失小。 |
| **LM-CMA / LM-MA-ES** (Loshchilov 2014/17) | low-rank CMA | 共分散を低ランク近似（過去ステップ m 本）で表現 | ✓ O(n·m) | ✓ | **CONSIDER** | 対角より表現力↑（相関を一部保持）。sep-CMA で不足なら昇格。実装コスト中。 |
| **Differential Evolution (DE)** (Storn 1997) | vector-diff | 3 個体差ベクトルで変異、座標非依存・無微分 | ✓ | ✓ | **CONSIDER（QD 内変異演算子として）** | スケール自由・パラメータ少・高次元頑健。MAP-Elites の variation operator に DE/rand/1 を挿すと cell 間情報移送が効く。単独 selector では使わない（単峰収束）。 |
| **PSO** (Kennedy 1995) | swarm | 個体が自/群 best へ速度更新 | △ | ✓ | **AVOID** | global-best 引力＝**中央収束**で SEL-1（中央一致除外）と原理的に衝突。多様性持続に逆行。lbest 変種でも QD の方が直截。 |
| **NES** (Wierstra 2008) / **CR-FM-NES** (2022) | natural ES | 探索分布の自然勾配で更新。CR-FM-NES は高次元特化 | ✓ (FM 系) | ✓ | **CONSIDER** | CR-FM-NES は高次元 black-box 特化＝GENOME-1 と整合。OpenAI-ES の理論基盤。proxy fitness が滑らかなら有効。 |
| **OpenAI-ES** (Salimans 2017) | scalable ES | 多数の摂動を並列評価、勾配を平均推定。RL 代替 | ✓ | ✓（並列前提） | **CONSIDER（Stage6 の実 LLM fine-tune 用）** | full-param LLM fine-tune で PPO/GRPO を sample 効率で上回る報告（2509.24372）。**proxy 段では不要**、実 LLM 重みを進化させる将来路線で再評価。 |

### 1.2 分布推定（EDA / CEM）

| アルゴリズム | family | mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **EDA / PMBGA** (Mühlenbein 1996) | model-building | crossover/mutation を「有望解の確率モデルからのサンプリング」で置換 | △（依存モデル次第） | ✓ | **AVOID（主路線）/ CONSIDER（belief space 接続）** | univariate EDA は多峰で全滅、依存モデル EDA は高次元で学習コスト爆発＝GENOME-1 と相性悪。**ただし Cultural Algorithm の belief space（normative 確率モデル）は実質 EDA**＝BS-1 と概念接続できる（DOWN: 進化集団本体には適用しない）。 |
| **CEM** (Rubinstein 1997) | elite refit | top-k elite にガウスを再フィット、反復 | ✓（対角） | ✓ | **AVOID（単峰）** | 単一ガウス＝単峰収束で OE-3 違反。CMA-ES の劣化版。QD なら CMA-MAE が上位互換。 |

### 1.3 遺伝的プログラミング（program/tree representations）

| アルゴリズム | family | mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **Tree-GP / Linear-GP** | program evo | 式木/命令列を交叉・変異で進化 | n/a（可変長） | ✓ | **AVOID（コア表現）** | プログラム発見＝SCOPE-1（検証可能コード discovery）で competition しない方針と衝突。bloat 制御も別問題系。我々のゲノムは**固定スキーマ実数ベクトル**であり GP 表現は不要。 |
| **PushGP** (Spector) | stack-GP | スタック型言語で型安全に program 進化。lexicase の母体 | n/a | ✓ | **AVOID** | 同上。ただし **lexicase selection の出自**＝SEL-3（ε-lexicase）の根として参照価値あり（手法は既採用）。 |
| **TPG (Tangled Program Graphs)** | graph-GP | プログラム群をグラフ的に絡め emergent モジュール性 | n/a | ✓ | **AVOID** | モジュール性は魅力だが表現がプログラム前提。我々の実数ゲノムに移植する旨味が薄い。 |
| **Grammatical Evolution** (Ryan 1998) | grammar map | 整数列を BNF 文法で表現型へ写像（genotype-phenotype 分離） | ✓（整数列は伸縮自在） | ✓ | **CONSIDER（間接エンコードの着想源）** | **genotype（整数列, 大）→ phenotype（文法生成物, 構造的）の分離**は GENOME-1+DESC-1 の「大ゲノム→低次元発現」と同型。c_latent の発現写像設計の参照に。直接採用はしない。 |

### 1.4 ニューロ進化（large genome → low-dim phenotype の鍵分野）

| アルゴリズム | family | mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **NEAT** (Stanley 2002) | direct topology evo | NN 構造＋重みを進化、historical marking で交叉、speciation で保護 | △（構造膨張） | ✓ | **CONSIDER（speciation の母体, 既採用）** | speciation は既に `speciation.py`。直接エンコードは大ゲノムで膨張。topology 進化自体は我々の固定スキーマと不一致。 |
| **HyperNEAT / ES-HyperNEAT** (Stanley 2009) | **indirect/generative** | CPPN（小ゲノム）が幾何座標→重みを生成。30k 遺伝子が 兆 接続を規定する DNA 比喩 | ✓✓ | ✓ | **ADOPT（思想）/ CONSIDER（実装）** | **本系の中核思想と最も整合**: 小 CPPN ＝ low-dim、生成される大表現 ＝ large phenotype。我々は逆向き（大ゲノム→低次元記述子）だが「**圧縮された生成規則が規則性・対称性を持つ大構造を生む**」原理は c_latent 発現写像の設計指針。完全実装は重い → 思想を借りる。 |
| **CPPN** (Stanley 2007) | generative encoding | 関数合成ネットで対称・反復パターンを compact に符号化 | ✓✓ | ✓ | **CONSIDER** | c_latent → 行動記述子の**発現写像**を CPPN 風（座標→値の合成関数）にすると、疎変異が大域的・規則的な表現変化を生む＝SPARSE-1 の「小変化→大効果」を構造的に実現。 |
| **WANN (Weight-Agnostic NN)** (Gaier 2019) | architecture-only | 重みを共有単一値にして**構造だけ**で性能を出す | n/a | ✓ | **AVOID** | 面白いが我々の固定スキーマに非適合。参照のみ。 |
| **PGA-MAP-Elites** (Nilsson 2021) | QD + policy gradient | MAP-Elites の variation に TD3 policy gradient を併用 | ✓（deep NE 向け） | △（GPU/勾配前提） | **AVOID（proxy 段）/ CONSIDER（Stage6）** | 勾配が要る＝proxy の純粋評価関数（SR-1, I/O なし）とは別世界。実 LLM・微分可能タスクが入る Stage6 以降でのみ意味。 |

### 1.5 多目的（many-objective, NSGA を超える）

| アルゴリズム | family | mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **NSGA-III** (Deb 2014) | reference-point | 参照点で多様性維持、NSGA-II の many-obj 弱点を補正 | ✓（obj 数に強い） | ✓ | **CONSIDER（≤3 レーン超で必要なら）** | SEL-3 で「NSGA-II は ≤3 目的レーンのみ」と既決。4+ 目的を扱うなら NSGA-III が正解。**だが我々は many-objective を ε-lexicase で回避する方針**＝NSGA 系自体の優先度低。 |
| **MOEA/D** (Zhang 2007) | decomposition | 多目的を多数のスカラー部分問題に分解、近傍で情報共有 | ✓ | ✓ | **AVOID** | スカラー集約＝SEL-2（argmax 禁止）の精神に反する方向。ε-lexicase が「集約しない多軸評価」で上位互換。 |
| **SMS-EMOA** (Beume 2007) | hypervolume | hypervolume 寄与最小の個体を淘汰 | ✗（HV 計算が obj 数で指数爆発） | ✗ | **AVOID** | many-obj で hypervolume 計算がボトルネック。我々の多軸（思考10+文化17+...）では計算不能。 |

### 1.6 QD フロンティア拡張（既採用 MAP-Elites の正統進化）

| アルゴリズム | family | mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **CMA-ME** (Fontaine 2019) | QD + CMA | CMA-ES の自己適応を MAP-Elites の archive 充填に投入。ME の 2倍超性能 | △（CMA 由来） | ✓ | **CONSIDER** | 連続記述子空間の**充填速度**が ME より大幅↑（corpus 1912.02400）。意味因子ブロックの QD 探索に有効。ただし full-CMA 由来で大ゲノム全体には不可。 |
| **CMA-MAE** (Fontaine 2023) | QD + CMA annealing | CMA-ES↔CMA-ME を割引関数 α で連続補間。低解像度 archive・平坦目的・早期 objective 放棄の 3 弱点を解消。SOTA | △ | ✓ | **ADOPT（意味因子 QD の主 illuminator）** | CMA-ME の既知 3 弱点（うち「平坦目的の探索難」「低解像度 archive 不調」は我々の懸念点）を直接解消。**proxy 段の意味因子 QD で最有力**。pyribs 参照実装あり＝on-prem 移植容易。 |
| **CMA-MEGA / CMA-MAEGA (DQD)** | differentiable QD | 目的・記述子の勾配が available なとき gradient arborescence で加速 | ✓（勾配前提） | △ | **AVOID（proxy 段）** | 勾配前提＝proxy の純粋評価と不一致。Stage6 で微分可能 proxy を作るなら再評価。 |
| **PGA-MAP-Elites** | QD + PG | （上述 1.4） | ✓ | △ | **AVOID（proxy）/ CONSIDER（Stage6）** | 同上。 |
| **MAP-Elites with sliding boundaries (SBX-ME)** | adaptive bins | archive 境界をデータ分布で動的調整、事前 bound 不要 | ✓ | ✓ | **CONSIDER** | 記述子の値域が事前不明（z-score 後でも分布が動く）我々の系で、**手動 bound 設定を不要化**。CVT-MAP-Elites の代替/補完。 |
| **Dominated Novelty Search (DNS)** (Bahlous-Boldi 2025) | archive-less QD | local competition を「明示 archive/grid」でなく**動的 fitness 変換**で実現。事前 bound・パラメータ不要。高次元・教師なし空間で既存 QD を有意に上回る | ✓✓ | ✓ | **ADOPT（高次元記述子の最有力 QD）** | corpus 2502.00593。**まさに我々の課題**（高次元・bound 未知・記述子が学習的）に直撃。grid を消して fitness 変換に畳むので DESC-1（低次元縮約後）でも grid 解像度問題が消える。最新ゆえ我々規模での実証は無し（honest）→ MAP-Elites baseline と A/B 必須。 |

### 1.7 LLM-as-operator（最も hype が乗る領域 — 割り引いて評価）

| アルゴリズム | family | mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **ELM (Evolution through LLM)** (Lehman 2022) | LLM mutation | LLM（diff モデル/few-shot）が「賢い変異」を生成 | n/a | △（LLM 呼出） | **CONSIDER（Stage6 のみ）** | proxy 段は LLM 非呼出（測定純度）＝適用外。Stage6 で on-prem 小 LLM を変異演算子に（ADOPT-3 の二層 LLM と整合）。 |
| **LMX (Language Model Crossover)** (Meyerson 2023) | LLM crossover | 親個体を prompt に並べ in-context で子テキスト生成。専用学習不要 | n/a | △ | **CONSIDER（Stage6, テキスト遺伝子のみ）** | 我々のゲノムは**実数ベクトル**でありテキスト交叉の出番が薄い。c_prompt（プロンプト遺伝子）が大きくなった場合のみ。proxy 段は不可。 |
| **QDAIF** (Bradley 2024, CarperAI) | LLM-judged QD | MAP-Elites の変異(LMX)・記述子・品質を全て LLM が評価。創作テキストで多様性 | n/a | ✗（LLM 多用） | **AVOID（我々の差別化と衝突）** | **DIFF-1 の核心と正面衝突**: 我々は「FM 暗黙の多様性判定でなく**明示的人間文化記述子**（Hofstede/Schwartz/WVS）+ 幾何 novelty」で勝負する方針。QDAIF は判定を LLM に委ねる＝検証不能・on-prem 高コスト・差別化を捨てる。**手法として学ぶが採用しない**。 |

### 1.8 高次元記述子の縮約・archive-less novelty（DESC-1 直撃）

| アルゴリズム | family | mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **Random projection / JL 補題** (Johnson-Lindenstrauss 1984) | dim reduction | ランダム行列で高次元→低次元へ射影、距離をε精度で保存 | ✓✓ | ✓✓ | **ADOPT（記述子縮約の既定）** | 要件 DESC-1 が明示指定。**学習不要・決定論（seed 固定で再現）・O(nd) と激軽**。32k ゲノム→8–50 次元記述子へ。全遺伝子が統計的に記述子へ寄与＝NEUT-1（bloat でなく読まれる）と両立。**第一採用**。 |
| **AURORA / 学習記述子 (VQ/AE)** | learned descriptor | autoencoder で行動を低次元潜在へ圧縮、進化と共更新 | ✓ | △（学習コスト） | **CONSIDER（JL の上位として）** | Stream B 既出。表現力は JL を超えるが学習・非定常性が課題。**まず JL で baseline → 不足なら AURORA**。決定論性は JL が勝る。 |
| **BR-NS (archive-less novelty)** (Salehi 2021) | learned recognizer | archive/k-NN を使わず「既見行動の認識器」で novelty 推定。高次元で k-NN が壊れる問題を回避 | ✓✓ | ✓ | **CONSIDER（高次元 novelty の代替路線）** | DESC-1 が警告する「高次元 k-NN は距離均質化で無意味」を**記述子側でなく novelty 推定側**で解く別アプローチ。JL+k-NN と BR-NS を A/B できる。cycling 抑制も利点。最新ゆえ我々規模で未実証。 |

### 1.9 共進化・カリキュラム・surrogate・diffusion

| アルゴリズム | family | mechanism | H2D? | OP? | 判定 | why-for-us |
|---|---|---|---|---|---|---|
| **Competitive coevolution** | adversarial co-evo | 2 集団が互いを問題として進化（軍拡競走） | ✓ | ✓ | **CONSIDER（隔離・資源上限下で）** | SR-4 が「協調進化は隔離・資源上限プロセスで」と既定。crash=0点で crash-to-win 無効化が前提。open-ended の駆動力にはなるが governance 設計が重い。 |
| **Minimal Criterion Coevolution (MCC)** | co-evo + MC | 問題と解が「最低基準」で互いを選別、報酬勾配なしで複雑性増 | ✓ | ✓ | **ADOPT（思想, Stream B 既出）** | SEL-4（minimal-criterion 繁殖可否）の母体。連続順位でなく floor で選別＝退化/偽novelty 排除（R-PEC-3）と整合。既に要件に取込済。 |
| **Hindsight / Curriculum** | task ordering | 易→難でタスクを並べ学習を導く | n/a | ✓ | **CONSIDER（OMNI 系の interestingness）** | ADOPT-2（OMNI-EPIC「学習可能+次に新規」を文化因子+novelty 距離で再構成）に接続。タスク生成側の自動カリキュラムは将来。 |
| **Surrogate-assisted EA (SAEA)** | cheap proxy model | 高コスト評価を代理モデル（GP/RF/NN）で近似し評価回数を削減 | ✓ | ✓ | **ADOPT（Stage6 の実 LLM 評価で必須）** | 実 LLM fitness は高コスト（Stage6）。代理モデルで「どの個体だけ実評価するか」を絞る＝on-prem 計算予算の鍵。**proxy 段は評価が既に安価（7s/500gen）なので不要**だが、Stage6 移行時に最重要。corpus に SAEA 多数（1804.05364 等）。 |
| **Diffusion Evolution** (Zhang/Levin 2024, 2410.02543) | diffusion-as-EA | 進化を denoising、逆進化を diffusion とみなす数学的等価。反復 denoising で多解同時発見 | ✓（潜在空間版） | △（学習/勾配寄り） | **CONSIDER（着想・将来）** | 「多最適解の同時発見」は QD と目的が重なる。Latent Space Diffusion Evolution は DESC-1（低次元潜在）と同型の発想。**だが diffusion model の学習が要る＝proxy 段の純粋関数評価と乖離**。理論的橋渡しとして価値、実装は将来。 |

---

## 2. 推奨アルゴリズムスタック（本系への組み付け）

役割ごとに「proxy 段（今すぐ）」と「Stage6（実 LLM）」を分離して提示する。

| 役割 | proxy 段（決定論・LLM 非呼出） | Stage6（実 LLM・GO 待ち） |
|---|---|---|
| **変異 (variation)** | **疎 per-locus 変異（SPARSE-1）+ sep-CMA-ES の σ 適応**を意味因子ブロックに。c_latent は疎ガウス。DE/rand/1 を QD 内演算子で併用 CONSIDER | **ELM/LMX**（on-prem 小 LLM, ADOPT-3 二層）を c_prompt 系に限定 |
| **選択 (selection)** | **ε-lexicase（主, SEL-3）+ minimal-criterion 繁殖ゲート（SEL-4/MCC）**。中央一致除外（SEL-1）、argmax 禁止（SEL-2） | 同左（測定純度のため選択ロジックは不変） |
| **記述子縮約 (descriptor reduction)** | **JL ランダム射影（ADOPT, 既定）** 32k→8–50 次元。決定論 seed 固定。不足なら AURORA へ | 同左 + AURORA CONSIDER |
| **アーカイブ / QD (archive)** | **CVT-MAP-Elites（基盤, QD-1/QD-2 単調成長）** + **CMA-MAE（意味因子の illuminator, ADOPT）**。高次元記述子では **Dominated Novelty Search を A/B（ADOPT 候補）**。sliding boundaries で bound 自動化 CONSIDER | 同左（surrogate で実評価を間引き） |
| **メタ制御 (meta-control)** | **UCB1 AOS or self-adaptive σ + 下限クランプ/GESMR（META-2/3, 既決）**。algorithm_id dispatch を配線（META-1） | 同左 |
| **高次元スケーリング (high-dim scaling)** | **sep-CMA-ES（対角, ADOPT）** を σ 適応に。full-CMA は意味因子ブロック（≤数百次元）に限定。LM-CMA は予備 CONSIDER | OpenAI-ES CONSIDER（実 LLM 重み進化路線） |
| **発現写像 (genome→behavior, 任意)** | **CPPN 風合成関数 CONSIDER**: c_latent の疎変異が規則的・大域的な記述子変化を生む（HyperNEAT 思想の借用） | — |
| **島構造 (island, ADOPT-1)** | island model で QD archive を島化、founder_lineage を親エッジに | 同左 |
| **実 LLM 評価予算 (Stage6)** | （不要） | **surrogate-assisted EA（ADOPT）** で実評価個体を選別 |

**スタックの一言要約**: *記述子は JL で低次元化 → 選択は ε-lexicase + minimal-criterion → アーカイブは CVT-MAP-Elites を CMA-MAE で照らし、高次元では Dominated Novelty Search を当てる → σ は sep-CMA-ES の対角適応で 32k 次元へ → メタは UCB1/self-adaptive + 下限クランプ。実 LLM は Stage6 で surrogate で間引く。*

---

## 3. ギャップと驚き（honest disclosure）

1. **「大ゲノム」と「連続 ES」は本質的に緊張関係**。CMA-ES/CMA-ME/CMA-MAE は全て **full covariance（O(n²)）が前提**で、32k 次元では破綻する。我々のスタックは「**意味因子（小・full-CMA 可）**」と「**c_latent（大・対角/疎のみ）**」を**別アルゴリズムで扱う 2 層構成**を強制される。これは既存 QD 文献がほぼ扱っていない領域＝**ギャップ＝差別化白地**でもある。
2. **Dominated Novelty Search（2025）が我々の課題に予想以上に直撃**。「事前 bound 不要・高次元・教師なし空間で既存 QD を上回る」は DESC-1 の悩み（記述子値域が動く・grid 解像度設定が難しい）をそのまま解く。**最新ゆえ我々の規模・on-prem での実証ゼロ**＝必ず MAP-Elites baseline と A/B（[[feedback_benchmark_honest_disclosure]]）。
3. **LLM-as-operator 系（QDAIF/ELM/LMX）は我々の差別化と正面衝突**。QDAIF は「多様性判定を LLM に委ねる」が、DIFF-1 は「**FM 暗黙でなく明示的人間文化記述子で多様性を地図化**」が勝ち筋。**hype に流されて LLM judge を入れると差別化軸を自ら捨てる**。手法は学ぶが proxy 段では採用しない（測定純度 + on-prem コスト）。
4. **多目的（NSGA/MOEA-D/SMS-EMOA）は我々ではほぼ不要**。ε-lexicase が「集約しない多軸評価」で many-objective の呪いを回避する方針が既に正しい。NSGA 系は ≤3 レーンの補助に留め、MOEA/D・SMS-EMOA は AVOID。
5. **GP 系（PushGP/TPG/Tree-GP）は SCOPE-1 と衝突**。プログラム/コード discovery は AlphaEvolve の土俵で competition しない方針＝採用しない。ただし **lexicase の出自が PushGP**、**Grammatical Evolution の genotype-phenotype 分離が c_latent 発現写像の参照**という形で「思想だけ」借りる。
6. **驚き: HyperNEAT/CPPN の「30k 遺伝子が兆接続を規定する DNA 比喩」が我々の GENOME-1 哲学と同根**。我々は方向が逆（大ゲノム→低次元記述子）だが、「**圧縮された生成規則が規則性を持つ大表現を生む**」原理は SPARSE-1（小変化→大効果）の構造的実装手段になりうる。**実装は重いので思想を借りる**。
7. **surrogate-assisted EA は proxy 段では完全に不要だが Stage6 で最重要**。今の proxy は 7s/500gen と激安なので評価間引きの意味がない。**実 LLM fitness に移った瞬間に最優先**になる役割の入れ替わりを設計に織り込むべき。
8. **Diffusion-as-Evolution（2410.02543）は理論的に美しいが我々には時期尚早**。diffusion model の学習が要り proxy の純粋関数評価から外れる。「多解同時発見」が QD と目的を共有する点だけ記憶に留める。

---

## 4. 既存タクソノミ（[[algorithms_for_ai_development]]）との突合

llive `docs/algorithms_for_ai_development.md` §6（進化計算）が**既に持つもの** vs **本サーベイで新規に評価したもの**:

| 観点 | 既存 taxonomy にある | 本サーベイで新規追加・深掘り |
|---|---|---|
| 連続 EA | CMA-ES（着地✅）, DE（検討余地） | **sep-CMA-ES / LM-CMA / NES / CR-FM-NES / OpenAI-ES / PSO** を高次元 on-prem 軸で評価。CMA-ES の **32k 次元破綻**を明示し 2 層構成を提案（taxonomy は単に「相性良い」止まり） |
| QD | MAP-Elites✅ / PGA-MAP-Elites（検討余地） / ME-NSS | **CMA-ME / CMA-MAE / CMA-MEGA(DQD) / sliding boundaries / Dominated Novelty Search(2025)** を追加。CMA-MAE と DNS を ADOPT 候補に |
| ニューロ進化 | NEAT（検討余地） / CoDeepNEAT | **HyperNEAT / ES-HyperNEAT / CPPN / WANN / 間接エンコード**を「大ゲノム→低次元」軸で評価。taxonomy は topology evo 視点のみ |
| 多目的 | NSGA-II✅ | **NSGA-III / MOEA/D / SMS-EMOA** を many-objective の呪い軸で評価し AVOID 判定 |
| LLM-operator | EvoFlow / Promptbreeder | **ELM / LMX / QDAIF** を差別化衝突軸で評価（QDAIF=AVOID）。taxonomy は名前列挙のみ |
| 記述子・novelty | （無し） | **JL ランダム射影 / AURORA / BR-NS** を新カテゴリとして追加（taxonomy に欠落していた DESC-1 領域） |
| 分布推定 | （無し） | **EDA / CEM** を追加し belief space=EDA の概念接続を指摘 |
| surrogate / diffusion | （無し） | **SAEA / Diffusion-Evolution(2410.02543)** を Stage6 軸で追加 |

**結論**: 既存 taxonomy は「llive 全般の AI 開発アルゴリズム台帳」であり進化計算は 1/9 軸の俯瞰に留まる。本サーベイは**開放端進化系の要件 5 軸（大ゲノム/低次元記述子/持続多様性/on-prem/governance）に射影した深掘り**で、特に **記述子縮約（JL/AURORA/BR-NS）・QD フロンティア（CMA-MAE/DNS）・高次元 ES（sep-CMA）・大ゲノム→低次元の間接エンコード思想（HyperNEAT/CPPN）** が新規貢献。taxonomy 側 §6 へ「QD フロンティア」「記述子縮約」「高次元 ES」の 3 行を追記すると cumulative。

---

## 5. 出典（WebSearch 2026-05-25 + corpus）

### CMA / QD フロンティア
- [Covariance Matrix Adaptation MAP-Annealing (CMA-MAE, arXiv:2205.10752)](https://arxiv.org/abs/2205.10752)
- [Scaling CMA-MAE (OpenReview)](https://openreview.net/pdf?id=dYOan-IoLxd) / [pyribs cma_mae 実装](https://github.com/icaros-usc/cma_mae)
- corpus: `1912_02400` CMA-ME / `2502_00593` Dominated Novelty Search / `2210_13156` PGA-MAP-Elites empirical
- [Dominated Novelty Search (arXiv:2502.00593)](https://arxiv.org/abs/2502.00593)

### 高次元 ES / scalable ES
- [Evolution Strategies as Scalable Alternative to RL (OpenAI, arXiv:1703.03864)](https://arxiv.org/pdf/1703.03864)
- [Fast Moving NES for High-Dimensional / CR-FM-NES (arXiv:2201.11422)](https://arxiv.org/pdf/2201.11422)
- [ES for LLM Fine-Tuning (arXiv:2509.24372)](https://www.emergentmind.com/papers/2509.24372)
- [CyberAgent cmaes (sep-CMA/LM-MA-ES 実装)](https://github.com/CyberAgentAILab/cmaes)

### LLM-as-operator
- [Language Model Crossover / LMX (arXiv:2302.12170)](https://arxiv.org/html/2302.12170v3)
- [Quality-Diversity through AI Feedback / QDAIF (arXiv:2310.13032)](https://arxiv.org/pdf/2310.13032) / [CarperAI blog](https://carper.ai/quality-diversity-through-ai-feedback/)
- [LLM_EA awesome list](https://github.com/xiaofangxd/LLM_EA)

### ニューロ進化 / 間接エンコード
- [HyperNEAT 解説 (Heidenreich)](https://hunterheidenreich.com/posts/next-gen-neuroevolution-hyperneat/)
- [Hypercube-Based Encoding (HyperNEAT 原典)](https://www.researchgate.net/publication/23986881_A_Hypercube-Based_Encoding_for_Evolving_Large-Scale_Neural_Networks)
- [Generative NeuroEvolution for Deep Learning (arXiv:1312.5355)](https://arxiv.org/pdf/1312.5355)

### 多目的
- [Runtime Analysis of SMS-EMOA for Many-Objective (arXiv:2312.10290)](https://arxiv.org/pdf/2312.10290)
- [Normalization in MOEA/D (Springer)](https://link.springer.com/article/10.1007/s40747-017-0061-9)
- [pymoo (NSGA-III/MOEA-D 実装)](https://pymoo.org/)

### 記述子縮約 / archive-less novelty
- [BR-NS: Archive-less Novelty Search (arXiv:2104.03936)](https://arxiv.org/abs/2104.03936)

### EDA / CEM / GP
- [Estimation of Distribution Algorithm (Wikipedia)](https://en.wikipedia.org/wiki/Estimation_of_distribution_algorithm)
- [EDA through Algorithmic Lens (arXiv:1905.10474)](https://arxiv.org/pdf/1905.10474)
- [EDA for Grammar-Guided GP (MIT Press EVCO)](https://direct.mit.edu/evco/article/32/4/339/119215/)

### diffusion / surrogate
- [Diffusion Models are Evolutionary Algorithms (arXiv:2410.02543)](https://arxiv.org/abs/2410.02543)
- corpus: `1804_05364` Kernel-Based Surrogate Neuroevolution / `1806_05865` Surrogate-Assisted Design Exploration

### 既存 taxonomy
- [[algorithms_for_ai_development]] (llive `docs/algorithms_for_ai_development.md`, 2026-05-23)
