# Evolution Research — Stream D: Culture & Learning (Cultural Algorithms / Baldwin / Human-Factor Genome)

> **由来**: 2026-05-25 要件定義モード（[[OPEN_ENDED_CULTURAL_EVOLUTION]] #6/#7/#8/#9, [[PERSONA_FX]]）。
> **担当系統**: D = CULTURAL EVOLUTION + LIFETIME LEARNING + HUMAN-FACTOR FRAMEWORKS。
> **目的**: 文化染色体 (`CulturalChromosome`) / belief space 学習層 / persona pull 獲得を **falsifiable な要件**へ昇格。
> **honest disclosure**: 本 doc は文献掃討 + 設計勧告。実装/proxy 値は未測定。人間サーベイ→agent genome 写像の妥当性 caveat は §6 に集約。

---

## 0. エグゼクティブサマリ

- **学習層の背骨 = Reynolds Cultural Algorithm (1994) の belief space**。5 知識源 (normative / situational / domain / temporal / spatial) + acceptance 関数 (上位個体が belief を更新) + influence 関数 (belief が変異を誘導)。これが #9 「best 個体が共有知を更新し後続を導く」を直接実装する。
- **個体生涯学習 = Baldwin 効果 (Hinton & Nowlan 1987)**。学習が fitness 地形を平滑化し針穴探索を可能にする。**Lamarckian (獲得形質を遺伝へ書戻し) は使わない** — 測定純度 ([[feedback_llive_measurement_purity]]) を壊し、Turney 曰く一般に Baldwinian より優位とは限らない。**学習コストを fitness に入れないと genetic assimilation は起きない**（重要な falsifiable 条件）。
- **文化染色体 = 人間サーベイ次元の operationalize**。核に **Schwartz 10 値（円環構造で TRADE OFF）** を据える。理由: 値は構造的に対立する（benevolence↔power, openness↔conservation）ので「全部最大化」が**数学的に不可能** = #1「全因子満点はダメ」「余計な構造が要る」を**因子セット自体が内蔵**する。Hofstede/WVS/Big Five は補助・honest caveat 付き。
- **social learning strategy (Henrich)**: conformist / payoff-biased / prestige-biased の 3 伝達バイアスを persona 獲得 & belief 更新の **acceptance/influence の選び方**に対応づける。**Rogers' paradox**（安い社会学習だけでは集団平均適応度は上がらない）→ **critical social learning**（まず社会学習、不満なら個体学習）を採用すると保証付きで優れる = #2「保守/中央が勝つ系はダメ」の解。

---

## 1. 技術テーブル (techniques)

| 手法 | 出典 | 何を与えるか | llive での役割 | ADOPT/AVOID |
|---|---|---|---|---|
| Cultural Algorithm + belief space | Reynolds 1994 | 集団とは別の共有知識空間。5 知識源を acceptance/influence で双方向接続 | #9 学習層の背骨。belief space = 集団 best が更新する共有適応知 | **ADOPT (核)** |
| 5 知識源 (normative/situational/domain/temporal/spatial) | Reynolds, Chung & Reynolds | normative=値域, situational=最良 exemplar, domain=領域知, temporal=探索履歴, spatial=地形 | 各知識源を別ストアに。novelty 記述子 (spatial/temporal) と直結 | **ADOPT** |
| Baldwin 効果 (学習が進化を導く) | Hinton & Nowlan 1987 | 学習で地形平滑化→針穴探索可能。$2^{20}$ 探索を回避 | per-個体 lifetime 学習で「実現確率を上げる」(#9) | **ADOPT** |
| genetic assimilation (canalization) | Waddington / Mayley | 学習で見つけた形質が後世に instinct 化。**学習コスト必須** | belief 由来の良形質が c_factors へ「定着」する経路 (任意拡張) | **ADOPT (条件付)** |
| Lamarckian local search (獲得形質を genome へ書戻し) | Whitley et al. 1994 | 速い局所最適化だが測定純度を壊す | **使わない** (測定純度 + Turney「常に優位ではない」) | **AVOID** |
| dual inheritance (gene-culture coevolution) | Boyd & Richerson 1985, Cavalli-Sforza & Feldman 1981 | 遺伝と文化を**2 つの並行継承系**として形式化 | genome 進化 (遺伝) ⊥ persona/belief (文化) の分離を理論的に正当化 | **ADOPT (枠組)** |
| memetic algorithm (GA + local search) | Moscato; FitText 2026 (corpus) | 個体が生涯局所探索を併用。Baldwinian/Lamarckian の選択 | Baldwinian variant のみ採用 (上記) | ADOPT (Baldwinian) |
| social learning biases: conformist | Henrich & Boyd | 多数派形質を頻度依存でコピー | belief「normative」更新を多数決寄りに（だが #2 で抑制） | ADOPT (限定) |
| social learning biases: payoff-biased (success bias) | Henrich | 最高成績の demonstrator をコピー | acceptance 関数 = payoff 上位個体が belief 更新 | **ADOPT** |
| social learning biases: prestige-biased | Henrich; Chudek et al. | 「尊敬される個体」を近道でコピー | persona bearer (hub) が prestige モデルに。獲得 cue として | ADOPT (実験的) |
| Rogers' paradox + critical social learning | Rogers 1988; Enquist 2007; Rendell 2010 | 安い社会学習のみは平均適応度を上げない。critical = 社会学習→不満なら個体学習 | belief を盲信せず個体学習でフォールバック (#2 の解) | **ADOPT** |
| Schwartz 10 基本値 (円環) | Schwartz 1992/2012 | 動機の円環連続体。**隣接=両立, 対極=対立** | `CulturalChromosome` 核。TRADE OFF を因子に内蔵 | **ADOPT (核)** |
| Schwartz 高次 2 軸 | Schwartz | openness↔conservation / self-enh↔self-trans | 2 軸を導出記述子に。直交性が比較的高い | ADOPT |
| Hofstede 6 次元 | Hofstede/Bond/Minkov | 国レベル文化次元 | 補助。**ecological fallacy 注意** (国≠個人) | ADOPT (caveat) |
| Inglehart-Welzel WVS 2 軸 | Inglehart & Welzel | trad↔secular / survival↔self-expr。**2 軸はほぼ直交** | 低次元の直交軸。Schwartz と相関あり | ADOPT |
| Big Five (OCEAN) | Costa & McCrae | 5 性格因子。**理想は直交だが実証では弱相関残** | 性格層。Schwartz と既知相関 (下記) | ADOPT (caveat) |
| Gelfand tight-loose | Gelfand 2011 | 規範の強さ・逸脱許容度 (6-item CTLS) | **集団/環境パラメータ**（個体因子でなく場の制約）に転用 | ADOPT (集団変数として) |
| Nisbett analytic-holistic | Nisbett & Peng 2001 | 分析的↔包括的認知スタイル | 認知スタイル軸。10 思考因子と意味が近く重複注意 | ADOPT (重複監査) |

---

## 2. Falsifiable 要件 (REQUIREMENTS)

### A. Belief Space (Cultural Algorithm 層) — #9

- **R-BS-1 (構成)**: belief space は **最低 3 知識源を別構造で保持しなければならない (MUST)**: `normative`（各文化因子の望ましい値域 = `[low_d, high_d]` 区間）、`situational`（世代横断 best exemplar の記述子ベクトル ≤K 件）、`temporal`（探索履歴: 各因子の最良値の移動軌跡）。`domain` / `spatial` は任意拡張。
- **R-BS-2 (acceptance)**: belief space は **acceptance 関数で選ばれた上位個体のみから更新されなければならない (MUST)**。デフォルト = **payoff-biased**（fitness/novelty 上位 p% = success bias, Henrich）。acceptance の選択方式は belief とは別ログに記録（測定純度）。
- **R-BS-3 (influence)**: belief space は **influence 関数を通じてのみ変異/初期化に作用しなければならない (MUST)**。normative は変異の値域を狭める（区間内サンプリング）、situational は exemplar 方向へのバイアス。**influence は genome を直接書き換えてはならない (MUST NOT)** — 変異オペレータのパラメータのみ変える（Baldwinian; Lamarckian 禁止）。
- **R-BS-4 (Rogers ガード)**: belief 由来の誘導は **critical social learning でなければならない (MUST)**: belief に従って生成した子が proxy fitness で改善しない場合、その個体は belief を無視した独立変異（個体学習）にフォールバックする。**belief 盲従個体が集団の 100% を占めてはならない (MUST NOT)**（Rogers' paradox 回避）。
- **R-BS-5 (測定純度)**: belief 更新信号・influence 適用回数・critical フォールバック率は **遺伝 fitness とは別チャネルで記録されなければならない (MUST)** ([[feedback_llive_measurement_purity]] / PERSONA_FX §4)。

### B. Cultural Genome (`CulturalChromosome`) — #6, #7

- **R-CG-1 (TRADE OFF 内蔵)**: 文化ゲノムは **構造的に対立する因子対を最低 2 組エンコードしなければならない (MUST)**: (a) Schwartz `openness_to_change ↔ conservation`、(b) `self_enhancement ↔ self_transcendence`。これにより **「全文化因子を同時に最大化した個体」は円環構造上 存在し得ない**（#1 の解を因子セットが内蔵）。
- **R-CG-2 (円環一貫性, falsifiable)**: 10 Schwartz 値を個別因子で持つ場合、ランダム集団で **隣接値間の相関 > 対極値間の相関** が成立しなければならない（Schwartz 円環の経験的署名）。成立しなければ因子マッピングが破綻している（検証テスト）。
- **R-CG-3 (記述子へ消費)**: 文化因子は **novelty 記述子に z-score 標準化して必ず混ぜられなければならない (MUST)**（#10「増やすなら消費目的とセット」）。記述子に入らない文化因子は **追加してはならない (MUST NOT)** — でないと中立ドリフト化し `c_latent` と区別がつかなくなる。
- **R-CG-4 (直交/相関の明示)**: 採用する各次元は **直交群か相関群かを宣言しなければならない (MUST)**。冗長な高相関次元（例: Schwartz `universalism` と Big Five `openness`）は **片方を導出値にするか重み 0.5 で減衰** させる（二重計上の回避）。
- **R-CG-5 (集団変数の分離)**: tight-loose (Gelfand) は **個体因子ではなく集団/環境パラメータとして実装されなければならない (MUST)** — 規範の強さ = 「平均からの逸脱に対する選択圧の強度」を制御する場の変数（個体の遺伝子ではない）。

### C. Persona 獲得 (PERSONA-FX 連携) — #8

- **R-PA-1 (pull のみ)**: persona は **上位から付与されてはならない (MUST NOT)**。各 persona が独立に「相関最大の逸脱個体」を argmax で選ぶ pull のみ（PERSONA_FX §1）。
- **R-PA-2 (相関空間の拡張)**: persona prototype と個体の相関は、従来の 10 思考因子に加え **文化因子 (Schwartz 等) を含む拡張空間で計算されてよい (MAY)**。これにより「ドストエフスキー persona」が思考因子だけでなく価値構造 (conservation 高 / self-transcendence 高) でも共鳴できる。
- **R-PA-3 (prestige cue, 任意)**: prestige-biased 学習を入れる場合、複数 persona を帯びた hub 個体は **prestige モデルとして後続世代の belief 更新に追加の重みを持ってよい (MAY)** — ただし退化 hub 総取り (PERSONA_FX §2 H) を悪化させないか監査必須。
- **R-PA-4 (学習が実現確率を上げる証拠)**: 「経験/belief を与えると persona 獲得率/専門性スコアが上がる」は **falsifiable に測定されなければならない (MUST)**: belief 参照あり群 vs なし群で、同等逸脱度における persona 獲得成功率を比較し、あり群が有意に高いこと（無ければ Baldwin 経路が機能していない）。

### D. Baldwin 学習層 — #9

- **R-BL-1 (Baldwinian, 非 Lamarckian)**: 生涯学習は **genome を書き換えてはならない (MUST NOT)**。学習は phenotype（評価時の振る舞い/記述子）のみを変える。
- **R-BL-2 (学習コスト)**: genetic assimilation（任意拡張）を狙う場合、**学習コストを fitness に必ず計上しなければならない (MUST)** — Turney/Mayley: コスト 0 では assimilation が停止する。コスト = 学習ステップ数 × 係数。
- **R-BL-3 (地形平滑化の検証)**: 学習導入で **proxy fitness 地形の探索効率が baseline (学習なし) より改善することを実測しなければならない (MUST)**（Hinton-Nowlan 針穴: 学習群が解に到達、非学習群が到達しない、を toy で再現）。改善しなければ学習層は飾り。

---

## 3. 提案 `CulturalChromosome` 因子セット (CONCRETE)

> 設計原則: **TRADE OFF を持つ因子を核に**。全部を一度に積まず、初版は **直交性/確立度が高く、かつ構造的対立を内蔵する**ものに絞る。各 [0,1]（円環は内部で対立に変換）。

### 初版 (v1) — 計 ~12 次元

**核: Schwartz 高次 2 軸 (連続, [-1,1]) — TRADE OFF を直接エンコード (4 次元 → 実質 2 自由度)**

| 因子 | 範囲 | 意味 | なぜ (TRADE OFF) |
|---|---|---|---|
| `openness_vs_conservation` | [-1,1] | -1=保守/秩序, +1=変化/自律 | **両立不可**（一方を上げると他方が下がる）。#1 の核 |
| `selfenh_vs_selftrans` | [-1,1] | -1=他者厚生/普遍, +1=個人成功/支配 | benevolence↔power の対立を 1 軸に圧縮 |

> この 2 軸だけで「全因子最大化」が**幾何学的に不可能**になる（円の対極は同時に取れない）。これが本因子セットの最重要ポイント。

**WVS / Inglehart-Welzel 2 軸 (連続, [-1,1]) — Schwartz とほぼ直交な社会軸 (2 次元)**

| `trad_vs_secular` | [-1,1] | 伝統・権威 ↔ 世俗・合理 | Schwartz と弱相関、別軸を足す |
| `survival_vs_selfexpr` | [-1,1] | 経済/安全志向 ↔ 自己表現/寛容 | 2 軸はほぼ直交（IW map の経験則） |

**Big Five (連続, [0,1]) — 性格層 (5 次元, 一部 Schwartz と相関し減衰)**

| `openness` | [0,1] | 好奇心・新規性 | Schwartz openness と相関 → 重み 0.5 |
| `conscientiousness` | [0,1] | 自己規律・計画性 | achievement/conformity と相関 |
| `extraversion` | [0,1] | 社交・活動性 | stimulation/achievement と相関 |
| `agreeableness` | [0,1] | 協調・利他 | benevolence/tradition と相関 → 重み 0.5 |
| `neuroticism` | [0,1] | 情動不安定性 | 他軸とほぼ直交（独立価値高） |

**認知スタイル (連続, [-1,1]) — Nisbett (1 次元, 思考因子との重複監査必須)**

| `analytic_vs_holistic` | [-1,1] | 対象分離・論理 ↔ 文脈・弁証法 | 10 思考因子の「構造化」と意味近接 → 重複なら片方 derived |

**集団/環境変数（個体ゲノムではない, R-CG-5）**

| `tightness` (集団 scalar) | [0,1] | 規範の強さ = 逸脱への選択圧 | Gelfand。**個体因子に入れない**。novelty 報酬の係数を変調 |

### 設計判断・根拠

1. **Schwartz は「10 個別値」でなく「高次 2 軸」を v1 核に**。理由: 10 値を個別に持つと冗長 (隣接値は高相関) で TRADE OFF が薄まる。2 軸なら**対立がゼロサムで明示**され #1 を最も強く満たす。10 値展開は v2 (R-CG-2 円環テストで検証してから)。
2. **WVS 2 軸を足すのは直交性のため**。Schwartz 2 軸 ⊥ WVS 2 軸で 4 自由度の文化空間 → novelty に多様な記述子を供給。
3. **Big Five は性格層**として補助。ただし `openness`/`agreeableness` は Schwartz と既知相関 (Roccas et al. 2002: O↔self-direction/universalism, A↔benevolence/tradition) → R-CG-4 で重み減衰。
4. **neuroticism は独立価値が高い** (どの文化軸とも弱相関) → フル重み。
5. **tightness は場の変数**: 「規範が強い集団では逸脱が罰せられる」を novelty 報酬の係数 (#8 獲得報酬の強度) に写像。これで「文化が違えば多様性エンジンの効き方も違う」を表現でき、QD アーカイブ (#11) のセル次元候補にもなる。

---

## 4. 学習 (Baldwin / belief space) → persona 獲得 → 実現確率 の接続 (#9 ↔ #8)

```
[個体生涯学習: Baldwin]                    [集団共有知: Cultural Algorithm belief space]
 個体が評価中に局所探索で記述子を改善      best 個体 (acceptance=payoff上位) が belief を更新
 (genome 不変, phenotype のみ)              ├─ normative: 文化因子の望ましい値域
   └→ 地形平滑化 (Hinton-Nowlan)           ├─ situational: 成功 exemplar 記述子
   └→ 学習コストを fitness 計上             └─ temporal: 探索軌跡
        (assimilation 条件, Turney)                    │
            │                                          │ influence (変異パラメータのみ)
            ▼                                          ▼
  ┌────────────────── persona 獲得 pull pass (PERSONA-FX) ──────────────────┐
  │ 逸脱個体 × persona prototype の相関 argmax (思考因子 ⊕ 文化因子, R-PA-2)    │
  │ belief 参照で persona の専門 rubric を満たしやすくなる → 獲得率↑ (R-PA-4)   │
  │ = 「経験/学習を与えると実現(獲得)確率が上がる」(#9 の主張の操作的定義)        │
  └────────────────────────────────────────────────────────────────────────┘
            │ critical social learning (R-BS-4): belief 従い改善せねば個体学習へ
            ▼
       Rogers' paradox 回避 (belief 盲従 100% を禁止) = #2「中央が勝つ系」の解
```

**核心**: 「実現確率が上がる」を **belief 参照あり群の persona 獲得率 / 専門性スコアが、なし群より有意に高い** という falsifiable な形で定義 (R-PA-4 + R-BL-3)。belief space は「集団が学んだ文化的成功パターン」、Baldwin は「個体が生涯で地形を均す」、両者が persona rubric を満たしやすくする = 学習が進化（獲得=報酬で多様性駆動）を導く。Lamarckian 書戻しを使わないので測定純度を保ったまま「学習が進化を導く」を実現する。

---

## 5. ADOPT vs AVOID + Honest Disclosure

### ADOPT (採用)

- **Cultural Algorithm belief space (5 知識源, acceptance/influence)** — 学習層の確立済み背骨。#9 を直訳できる。
- **Baldwinian 学習 (genome 書戻しなし) + 学習コスト計上** — 測定純度を保ち assimilation 条件を満たす。
- **Schwartz 高次 2 軸を核とした文化ゲノム** — TRADE OFF を因子構造に内蔵 = #1 を因子側で解く（fitness 設計に頼らない）。
- **payoff-biased acceptance + critical social learning (Rogers ガード)** — belief 盲従を防ぎ #2 を解く。
- **dual inheritance の枠組** — 遺伝(genome) ⊥ 文化(persona/belief) の分離を理論的に正当化（PERSONA_FX の核と整合）。

### AVOID (回避)

- **Lamarckian local search (獲得形質を genome に書戻し)** — 測定純度破壊 + Turney「常に Baldwinian より優位ではない」。速度目当てでも採らない。
- **Schwartz 10 値の全個別搭載 (v1)** — 冗長・高相関で TRADE OFF が薄まる。v2 で円環テスト (R-CG-2) 通過後に展開。
- **Hofstede 全 6 次元の個体因子化** — ecological fallacy（国レベル↔個人レベル混同）。個体ゲノムには不適。使うなら集団変数 or 既存軸の補強のみ。
- **記述子に消費されない文化因子の追加** — #10 違反。中立ドリフト化し `c_latent` と区別不能になる。
- **prestige-biased を無条件強化** — 退化 hub 総取り (PERSONA_FX §2 H) を悪化させうる。監査付き実験のみ。

### Honest Disclosure / 妥当性 caveat（必読）

1. **【最重要 caveat】人間サーベイ → agent genome 写像の妥当性は未検証の speculation**。Hofstede/Schwartz/WVS は**人間集団**の統計構造であって、proxy agent の「価値」がそれと同じ幾何（円環・直交）を持つ保証はゼロ。R-CG-2 (円環一貫性テスト) は**この写像が壊れていないかを検出するための最低限の falsifiable ガード**であり、通っても「意味的に妥当」を保証しない。**「人間らしい因子」はメタファー/着想源であって、measurement の根拠ではない**。
2. **Hofstede 批判**: データが古い (1970s IBM)、国を均質と仮定、ステレオタイプ強化、ecological fallacy。学術的にも個人レベル適用は誤用とされる。→ 個体因子に使わない方針は妥当。
3. **Big Five の「直交」は理想で、実証では弱相関が残る**。R-CG-4 の宣言・減衰はこの現実への対処。
4. **Schwartz 円環は cross-culturally 頑健**だが、それでも「45 項目の人間自己申告」由来。agent には項目自体が無い → 因子値の意味は**操作的に再定義**するしかなく、人間の値とは別物 (PERSONA_FX §4 の「眼鏡の信頼性が土台」と同じ警告)。
5. **Baldwin 効果が EC で効くのは特定条件下のみ** (Mayley: 学習コスト高 + genotype-phenotype 近傍相関高)。条件外では学習層は単なるオーバーヘッド。R-BL-3 で「効いているか」を必ず実測する設計にした。
6. **Rogers' paradox の含意**: 安い社会学習 (belief 盲従) を足すだけでは集団平均適応度は上がらない。これは「belief space を足せば良くなる」という素朴な期待への反証。critical social learning でしか保証付き改善は出ない。
7. **全て proxy・決定論・LLM 非呼出**（OPEN_ENDED §0）。実 LLM 評価 (ollama, GO 待ち) で上書きするまで、本 doc の因子・要件は**機構 feasibility の仮説**である。

---

## 参考文献 (本 stream 掃討分)

- Reynolds, R.G. (1994) *An Introduction to Cultural Algorithms*. — belief space / 5 知識源 / acceptance & influence
- Chung & Reynolds; Saleem & Reynolds — knowledge source 拡張 (situational/normative/topographic/historical/domain)
- Hinton, G. & Nowlan, S. (1987) *How Learning Can Guide Evolution*, Complex Systems 1:495-502. — 針穴, 20 allele (1/0/?), 地形平滑化
- Turney, P. (2002) *Myths and Legends of the Baldwin Effect*, arXiv cs/0212036. — Lamarckian ≠ 常に優位, 学習コスト必須, 2 phase, 非 Lamarckian
- Whitley, Gordon, Mathias (1994) — Lamarckian vs Baldwinian in GA
- Mayley, G. (1996) — genetic assimilation 2 条件 (学習コスト高 + 近傍相関)
- Waddington — canalization / genetic assimilation
- Boyd, R. & Richerson, P. (1985) *Culture and the Evolutionary Process*; Cavalli-Sforza & Feldman (1981) — dual inheritance, 伝達バイアス形式化
- Henrich, J. & Boyd — conformist / payoff / prestige biased transmission; Chudek et al. — prestige bias 形式
- Rogers (1988); Enquist et al. (2007) *Critical Social Learning*; Rendell et al. (2010) Rogers' paradox recast — 社会学習が平均適応度を上げない / critical SL の優位
- Schwartz, S.H. (1992, 2012) Theory of Basic Values — 10 値円環, 高次 2 軸, SVS(45 項目)/PVQ(40 項目), refined 19 値
- Roccas, Sagiv, Schwartz, Knafo (2002) — Big Five × Schwartz 相関
- Hofstede, Hofstede & Minkov — 6 次元; Minkov LTO; ecological fallacy 批判
- Inglehart & Welzel — WVS 2 軸 (trad↔secular / survival↔self-expr), cultural map
- Gelfand et al. (2011) *Differences between tight and loose cultures: a 33-nation study*; CTLS 6-item
- Nisbett & Peng (2001) *Culture and systems of thought: holistic vs analytic cognition*; *Geography of Thought*
- FitText (arXiv 2605.02411, corpus) — memetic retrieval (弱モデルで進化探索が反転する観察 = 能力依存)
- 関連: [[OPEN_ENDED_CULTURAL_EVOLUTION]] / [[PERSONA_FX]] / [[feedback_llive_measurement_purity]] / [[feedback_benchmark_honest_disclosure]]
