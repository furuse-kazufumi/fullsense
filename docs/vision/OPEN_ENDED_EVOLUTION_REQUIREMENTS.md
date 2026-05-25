# 開放端進化 AI 環境 — 要件定義 (Requirements Definition)

> **Goal (2026-05-25 ユーザー)**: 「AI を徹底的に進化ランさせると**新しい AI が生み出される**環境を
> 構築し、様々な条件で PoC を実施、**導入可能な段階**へ進める」。「既存 AI に勝つ」水準の準備を要する。
> **本書の位置づけ**: 13 原理（[[OPEN_ENDED_CULTURAL_EVOLUTION]]）+ 研究 6 系統（A–F）を
> **falsifiable な MUST/SHOULD 要件**へ統合。**実装はこの要件確定後**に着手する。
> **honest disclosure**: 全要件は proxy 段で検証可能な形にした。実 LLM 評価は最終段（ollama, GO 待ち）。

## 0. 「新しい AI が生み出される」の操作的定義（成功基準の核）

進化ランが「新しい AI を生む」とは、次を**同時に満たす個体**が**継続的に**出現すること:
1. **新規性**: 既存アーカイブの全 elite と記述子空間で有意に離れている（新 cell を占有 or 既存 cell の novelty 距離超）。
2. **可生存性 (minimal criterion)**: 連続スカラー順位ではなく、満たすべき最低基準を満たす。
3. **非自明性**: 退化（全因子フラット/単峰総取り）や gaming（偽の個性）でない（非自明性ガード通過）。
4. **(最終段) 実証**: 実 LLM タスクで proxy を上書きした評価で意味を持つ（Stage6）。
- **継続的** = 末尾 20% 世代でも新 cell 増加 ≥1（停滞しない）。これが open-endedness の operational 判定。

## 1. 要件（falsifiable, MUST/SHOULD）

### 1.1 選択・標準化（中央でなく特異を選ぶ / 正規化）— Stream B,C
- **STD-1 (MUST)**: 記述子は**集団内 per-dim z-score**で標準化。「全因子満点」は分散ほぼ0＝**無特徴**となり優位を得ない（反例: 旧 proxy の均等高値単峰）。
- **SEL-1 (MUST)**: **中央一致（集団平均への近さ）を報酬から除外**。逸脱（中心からの距離=novelty）を選択圧に。
- **SEL-2 (MUST)**: **スカラー単峰目的の argmax 選択を禁止**（OE-1）。
- **SEL-3 (MUST)**: 主選択は **ε-lexicase**（多軸ケースを集約せず個別評価。many-objective の呪い回避・専門家＝特異個体が生存）。NSGA-II は ≤3 目的レーンのみ。
- **SEL-4 (MUST)**: **minimal-criterion 型の繁殖可否**を含む（連続順位だけで決めない, OE-6）。退化/境界の偽 novelty は criterion floor で排除（R-PEC-3）。

### 1.2 表現・ゲノム（余計な因子 / 疎差別化）— Stream C
- **NEUT-1 (MUST)**: 中立貯蔵庫を実 `Genome3D.c_latent` にし、**記述子が読む**（現状 `genome_flat_vector` は c_factors のみ＝貯蔵庫が bloat。これを是正）。
- **NEUT-2 (MUST)**: 貯蔵庫は **novelty 記述子に入るが品質目的には入らない**（縮退: fitness 中立・振る舞いで発現）。
- **SPARSE-1 (MUST)**: **全染色体で疎な per-locus 変異**（c_factors は現状全座位変異＝生物比率原理に反する。要是正）。
- **GENOME-1 (MUST, 容量で多様性を支える)**: ゲノム容量は **~10,000 世代の長期ランでも行動多様性が崩壊しない**規模を持つ（OEE「実質無限の多様性を許す媒体」要件の具体化; ユーザー実測知見 2026-05-25 = 小容量・単峰だと 1h 未満で全滅）。**遺伝子数を LLM の token 数（語彙 ~3万〜数十万）に匹敵させる**ことを上限 sweep 点とする（ユーザー予想 2026-05-25: 表現容量が結果を質的に変える）。中立貯蔵庫サイズ・疎度・記述子次元・QD cell 数を**多様性持続の制御変数**として sweep（256 → 1024 → 4096 → 32768+）。生物比: 大ゲノム + 疎差別化（高次元遺伝子の多くは fitness 中立＝真の構造は低次元, という EA 知見と整合）。
- **ELEM-1 (SHOULD, もっと色んな要素)**: 意味ある因子の**families を増やす**（現 思考因子10 + 文化~12 に加え、感情・時間/発達・社会関係・モダリティ/感覚・ドメインスキル・言語スタイル等の候補を段階導入）。ただし**追加因子は必ず記述子/選択が消費**（消費されないと c_latent と区別不能, #10）。「要素を増やす」= 容量(GENOME-1) と 種類(ELEM-1) の両面。
- **RUN-1 (MUST, 長期ランで評価)**: PoC は**≥10,000 世代**で評価する（世代交代は秒オーダーで安価: 実測 proxy 500gen≈7s[71 gen/s] / rich≈25s[20 gen/s] → 10K gen は proxy≈2.3min / rich≈8min）。多様性持続・archive 成長・monoculture<0.8 を**末尾世代（gen≈10K 近傍）で**判定する（短期の見かけの多様性でなく持続性が open-endedness の本質）。全 sweep 総計算 <10h を目安（並列ラン可）。
- **POP-1 (MUST, 競争母数を大きく)**: 集団サイズ（competing 母数）も大規模化（現 32 → 256/1024/4096 を sweep, ユーザー 2026-05-25）。大母数は **QD アーカイブの cell 被覆・並列ニッチ・ドリフト耐性**を上げ多様性持続に寄与。低次元記述子(DESC-1)で novelty k-NN が pop×(pop+archive) でも tractable なため大母数でも実行可。**スケール 4 軸（ゲノム容量 × 母数 × 世代数 × 要素種類）を一括して上げ「結果が質的に変わるか」を検証**するのが本プロジェクトの核仮説（ユーザー）。

### 1.3 多様性・open-endedness（QD アーカイブ）— Stream B
- **QD-1 (MUST)**: 成果物は**単一 best でなく QD アーカイブ**（MAP-Elites/CVT-MAP-Elites; cell 別 elite で多様性崩壊が構造的に不可能）。
- **QD-2 (MUST)**: 新 cell 個体は既存 elite を**消さない**（アーカイブ単調成長）。
- **OE-3 (MUST)**: 単一系統が集団の **>80% を占有しない**（monoculture 禁止; 旧 founder 絶滅→単系統化の反証）。
- **DESC-1 (MUST, 記述子は低次元縮約)**: token 級の巨大ゲノム（GENOME-1）に対し、novelty/QD の **行動記述子は低次元へ縮約**（JL ランダム射影 or 学習記述子 AURORA/VQ）してから距離計算する。**生の高次元ユークリッド k-NN は次元の呪いで無意味**（距離が均質化）になるため。ゲノム=token 級・記述子=低次元（例 8–50）。JL 補題で距離は保存され**全遺伝子が統計的に記述子へ寄与**（= bloat でなく読まれる, NEUT-1 と両立）。

### 1.4 メタ進化（アルゴリズム自体の進化）— Stream A
- **META-1 (MUST)**: `algorithm_id` 等の c_meta が**実選択/変異を切替**（同 seed で軌道が分岐することで検証）。現状デッドの dispatch 層を配線。
- **META-2 (MUST)**: メタ params は heritable + 適応（self-adaptive ES or UCB1 AOS）。**適応 run ≥ 固定 baseline**。
- **META-3 (MUST)**: **変異率/σ に下限クランプ**（or GESMR）で rate→0 崩壊を防止（500gen で min>floor をログ検証）。
- **META-4 (MUST)**: neighborhood 拡張は**予算上限**（runaway 防止）。
- **META-5 (MUST)**: **後方互換**（`MetaChromosome.default()` が旧 run を再現）。
- AVOID: AutoML-Zero/Gödel machine の完全実装（on-prem 非現実的・証明探索 uncomputable）。

### 1.5 文化・学習（人間要素 / belief space / Baldwin）— Stream D
- **CG-1 (MUST)**: `CulturalChromosome` は**構造的に対立する因子対を ≥2**（openness↔conservation, self-enh↔self-trans）含む。これで「全因子満点」が**幾何的に不可能**＝原理#1 を因子構造で解く。v1 ≈12 次元（Schwartz 高次2軸 + WVS 2軸 + Big Five + Nisbett analytic-holistic）。
- **CG-2 (MUST)**: 文化因子は**必ず novelty 記述子が消費**（消費されない文化因子は c_latent と区別不能＝原理#10 違反）。
- **BS-1 (MUST)**: belief space は**≥3 知識源**（normative=価値域 / situational=最良 exemplar / temporal=軌跡）。
- **BS-2 (MUST)**: belief の影響は**変異 params のバイアスのみ。genome を書き換えない**（Baldwinian, not Lamarckian; 測定純度）。
- **BS-3 (MUST, Rogers ガード)**: **critical social learning** — belief 誘導の子が改善しなければ個体変異へ fallback。belief-blind 個体が 100% にならない。
- **BL-1 (SHOULD)**: 遺伝的同化を狙うなら**学習コストを fitness に課す**（コスト0だと同化が止まる, Turney/Mayley）。
- **PA-1 (MUST, 学習→実現の検証)**: 「学習が persona 獲得の実現確率を上げる」を**falsifiable に測定**（belief 参照群の獲得率が非参照群を同逸脱度で有意に上回る）。

### 1.6 ペルソナ獲得（pull 型 / 上から与えない）— PERSONA-FX
- **PERS-1 (MUST)**: persona は**遺伝しない**。プール常駐、逸脱個体が相関 argmax で**獲得**（上位者が一方的に付与しない）。
- **PERS-2 (MUST)**: persona 側 uniqueness（1 persona ≤1 個体）、個体側 0..N（多才 hub/generic 創発）、相関個体不在→休眠→隔世復活。
- **PERS-3 (MUST)**: 相関は**拡張空間（思考因子 ⊕ 文化因子）**で計算。獲得＝報酬で「平均を外れること」が選択圧＝多様性エンジン内蔵。

### 1.7 安全（contained open-endedness / 競合排除を生まない）— Stream E, 原理#13
- **SR-1 (MUST, 実行 containment)**: 個体・演算子は**データのみ**。評価は**純粋・I/O なし関数**で実権限ゼロ。harness は個体由来データを **eval/exec しない**。
- **SR-2 (MUST, 検出・監査・隔離)**: 毎世代の transgression スコア → append-only AuditTrail → 隔離。**deploy 昇格は不可**だが **red-team 信号として保持**（探索の開放性は維持）。
- **SR-3 (MUST, 迂回不能メタガバナンス)**: ガバナンスは**進化集合の外**（演算子が知覚・到達できない＝「到達できない制約は最適化で消せない」）。**fail-closed**。#12 メタ進化が自らのガバナンスを進化で迂回しないことを不変条件に。
- **SR-4 (MUST, インセンティブ衛生)**: transgression は**いかなる fitness 経路でも正の報酬ゼロ**。協調進化は**隔離・資源上限プロセス**で（crash=0 点＝crash-to-win exploit を無効化）。
- **アーキ**: **二空間分離（探索≠効果）**。探索空間=最大開放・実効果ゼロ（データのみ個体・純粋評価 sandbox）。**Approval Bus 上の片方向 fail-closed 昇格ゲート**（transgression<θ ∧ trust≥τ ∧ audit-clean）のみが effect 空間（実 LLM 評価/persona deploy/belief 更新）への経路。raptor `@govern`/IntentClassifier/TrustScore/AuditTrail を再利用、新規は4部品（transgression scorer / 昇格ゲート / semgrep eval-exec 到達性ルール / 進化用 intent signals）。

### 1.8 競合差別化・スコープ（既存 AI に勝つ）— Stream F
- **DIFF-1 (MUST)**: 差別化白地＝**検証可能性のない領域（認知・文化スタイルの多様性）を、明示的人間文化記述子（Hofstede/Schwartz/WVS を外在化, FM 暗黙でなく）+ novelty/QD で「多様性の地図」として生む**。pull 型 persona 獲得 + 中立貯蔵庫（先行実装が見つからない白地）+ 迂回不能ガバナンスを進化不変条件に。これが「勝てる軸」。
- **SCOPE-1 (MUST NOT)**: **検証可能なアルゴリズム/コード発見（AlphaEvolve/FunSearch の土俵）で competition しない**。on-prem では frontier cloud LLM + 大規模計算に discovery 品質で勝てない（honest）。別軸で勝つ。
- **SCOPE-2 (MUST NOT, #13 整合)**: **R 型 自己コード書換を主経路に置かない**（Darwin Gödel Machine / AI-Scientist が objective-hacking を実演; #13 ガバナンスと衝突）。
- **ADOPT-1 (SHOULD)**: **island モデル**で QD アーカイブを島化（`founder_lineage.jsonl` を親エッジに流用）＝早期収束防止（FunSearch/AlphaEvolve/DGM 共通手法）。
- **ADOPT-2 (SHOULD)**: **explicit-culture interestingness** — OMNI-EPIC の「学習可能 + 次に新規」を frontier FM でなく**文化因子 + novelty 距離**で再構成（= 差別化の核心の賭け）。
- **ADOPT-3 (Stage6)**: 二層 on-prem LLM（小=変異 / 中=洗練、AlphaEvolve の Flash/Pro 相当）。
- **最近接既存**: **CycleQD（Sakana, Llama3-8B 上の QD model-merge）** が on-prem QD の実在証明＝#11 の最近接アナログ（手法を学ぶ）。**OpenEvolve** が AlphaEvolve ループを Ollama で再現＝ループ自体は on-prem 可。

### 1.9 運用規模・連続運転・チェックポイント（5h+ 連続 / 一時停止・再開）— ユーザー 2026-05-25
- **RUN-2 (MUST, 5h+ 連続運転前提で規模決定)**: 平日・夜間に **≥5 時間連続運転**する前提で規模を決める。
  **決定スケール（初期）**: population=**1024**（POP-1, sweep で上下）、genome=**token 級（c_latent≈32,768 +
  思考因子 40 + 文化 ~12 ≈ 32,820 遺伝子）**、generations は **wallclock 予算（5–10h）で上限**
  （既存 `max_wallclock_seconds` を流用）+ 高 gen cap（例 200,000）。**校正ラン（calibration）で per-gen
  実測 → 5h window を埋めるパラメータ確定**（token 級 +novelty+QD の per-gen は未実測 [SPEC]）。**規模はさらに大きく可**（夜間 8–10h+）。
- **CADENCE-1 (SHOULD, 研究要素)**: **進化ラン時間 : 改良時間 ≈ 50/50 を初期 cadence** とし**少しずつ調整**（ユーザー 2026-05-25）。**AI 実装は人間より根本的に高速で最適比率が異なる** → cadence 自体を **meta 研究要素**として run/improve 実時間を計測し適応（改良サイクルが速いほど run を長く・大きく取れる）。
- **PDCA-1 (SHOULD, 速い PDCA + 品質向上維持)**: 研究改良ループを **自動化された高速 PDCA** にする —
  **Plan**(次 config/仮説) → **Do**(run, 5h+ 可, CKPT-1 で連続) → **Check**(Bedau/MODES + 安全 audit +
  受入メトリクスを**自動集計**) → **Act**(config/コード改良 + belief/要件更新) → 反復。**品質維持の担保**:
  (1) 各サイクルで**メトリクス回帰をゲート**（多様性/open-endedness/安全不変条件が悪化したら昇格不可＝速度
  のために品質を犠牲にしない）、(2) **SPC で品質指標を継続監視**（FullSense 中核, 管理限界外れを異常検知）、
  (3) honest disclosure（見かけの改善を neutral shadow 対照で疑う）。cadence(CADENCE-1) を高速化しても
  ゲート + SPC で品質向上が単調に積み上がる状態を作る。
- **CKPT-1 (MUST, 一時停止・再開で連続性維持)**: **全状態チェックポイント/再開**。`checkpoint_every`
  （例 500–1000 世代）で **population + generation + RNG 状態 + QD アーカイブ + novelty アーカイブ +
  belief space + metrics + founder_lineage** を永続化。`--resume` が**全状態を復元し決定論的に継続**。
  一時停止＝チェックポイント後に停止、再開＝最新から。既存 snapshot/resume（population/generation のみ）を
  **全状態へ拡張**する。ccr 連続運転と整合（[[project_ccr_auto_resume]] / [[feedback_session_marathon]]）。

### 1.10 推奨アルゴリズムスタック — Stream G
- **記述子縮約**: **JL ランダム射影**（学習不要・決定論・O(nd), 32k→8–50 次元; DESC-1, 全遺伝子が寄与=NEUT-1 両立）。
- **選択**: **ε-lexicase + minimal-criterion**（SEL-3/4）。
- **アーカイブ/QD**: **CVT-MAP-Elites を CMA-MAE で照らす**（QD SOTA, pyribs 移植可）; 高次元/教師なしは **Dominated Novelty Search (2025)** を A/B。
- **変異 σ 適応（2 層, 差別化白地）**: 小さい意味因子(factors/cultural)=**full-CMA** / 大きい c_latent(32k+)=**sep-CMA 対角 + 疎変異**（full-CMA は O(n²) で 32k 破綻）。この 2 層構成は既存 QD 文献がほぼ扱わない白地。
- **メタ**: UCB1 / self-adaptive + **σ 下限クランプ**（META-3）。
- **Stage6 実 LLM**: **surrogate-assisted EA** で評価予算を間引く（proxy 段では不要）。
- **AVOID**: QDAIF（多様性判定を LLM に委ねる＝DIFF-1 と衝突）/ MOEA-D・SMS-EMOA（argmax/hypervolume が SEL-2 と不整合）/ PSO・CEM（中央収束で OE-3 違反）。
- honest: DNS / CMA-MAE / BR-NS は最新ゆえ我々規模・on-prem 未実証 → **MAP-Elites baseline と A/B 必須**。

## 2. 受入メトリクス（「成立したか」の定量判定）

| メトリクス | 合格条件 | 反証する旧症状 |
|---|---|---|
| **Archive growth curve** | 末尾20%世代でも占有 cell 増加 ≥1 | best 頭打ち gen281 |
| **Monoculture ratio** | 全世代 max_lineage_share < 0.8 | founder 絶滅→(random)100% |
| **Behavioral diversity（記述子分散）** | 非ゼロで高止まり | 多様性 gen25 崩壊 |
| **Novelty 時系列** | 平均 novelty が枯渇しない | — |
| **Mutation rate/σ min** | > floor を 500gen 維持 | rate→0 崩壊（META） |
| **Adaptive ≥ baseline** | メタ適応 run が固定を下回らない | — |
| **PA 実現率** | belief 参照群 > 非参照群（同逸脱度, 有意） | — |
| **Safety 不変条件** | transgression 個体の実効果 = 構造的ゼロ / 全件 audit 記録 | — |

## 3. 段階 PoC 計画（「色々な条件で」= sweep）

PoC は**隔離・決定論・proxy**（実 LLM 無し）。**SR-1 により本質的に sandbox**（個体=データ・純粋評価）。
スイープ条件（直交軸）:
- 選択: scalar(baseline) / novelty / ε-lexicase / FUSS / +minimal-criterion
- 標準化: on/off（per-dim z-score）
- 中立貯蔵庫: off / size∈{64,256,1024} / 疎度∈{0.02,0.05,0.1}
- 文化染色体: off / v1(12次元, 対立対あり)
- メタ進化: off / UCB1 AOS / self-adaptive σ（+floor）
- アーカイブ: なし / MAP-Elites(記述子2軸 or CVT)
各条件で §2 メトリクスを記録 → 「どの構成が継続的に新しい AI を生むか」を比較表に。

## 4. 実装着手ゲート（implementation readiness — 全 ✓ で実装へ）

- [ ] A–F 全 findings 統合済（F=競合 SOTA / コーパス増設の知見反映）
- [ ] 操作的定義（§0）と受入メトリクス（§2）が測定コードに落ちている
- [ ] SR-1..4 の containment アーキが設計図化（二空間 + 昇格ゲート）
- [ ] 既存資産の再利用範囲確定（NoveltyScorer/MAPElitesGrid/nsga2/speciation/MetaEvolutionLoop/raptor governance）と新規4部品の境界
- [ ] 後方互換（META-5）と測定純度（proxy/real 分離）の担保方針
- [ ] honest: 残存リスク（§5）を明記し受容

## 5. honest disclosure / 残存リスク

- **最大の残存リスク（E）**: 欺瞞的整合/監視回避は**原理的に検出困難**（観測時のみ良振る舞い）。containment で**実効果は構造ゼロ**にできるが「検出」は保証できない＝「contain+audit+disclose」ループであって保証ではない。
- **人間文化因子の妥当性（D）**: Hofstede/Schwartz/WVS は**人間集団統計**。proxy エージェントが同じ幾何を持つ保証はゼロ＝**メタファー/着想であって測定的接地ではない**。circular-consistency テストは粗い破綻検出のみ。Hofstede は個体遺伝子から除外（生態学的誤謬）。
- **Baldwin は条件付き（D）**: 高学習コスト + genotype-phenotype 近傍相関が要る（Mayley）。実際に効くか要測定。
- **RAD コーパス（C）**: 既存 RAD は evo-comp 固有材料が薄い → 本書の evo-comp 知見は web 出典主体。コーパス増設を実行中（補強）。
- 全 proxy 段は mechanism feasibility の検証であり production 値ではない（実 LLM=Stage6）。

## 6. 出典（findings docs, docs/research/）
- A `evolution_research_meta_2026_05_25.md` / B `evolution_research_openendedness_2026_05_25.md` /
  C `evolution_research_representation_selection_2026_05_25.md` / D `evolution_research_culture_learning_2026_05_25.md` /
  E `evolution_research_safety_2026_05_25.md` / F `evolution_research_competitive_sota_2026_05_25.md`（6 系統完了）
- 実験設計: [[evolution_poc_experiment_design_2026_05_25]]（sandbox / 記述子 CVT・AURORA / 選択 / sweep / 測定）
- 測定方法論: Bedau 進化的活動統計（neutral shadow 対照）+ MODES toolbox（change/novelty/diversity/complexity）
- 設計: [[OPEN_ENDED_CULTURAL_EVOLUTION]] / [[PERSONA_FX]] / [[evolution_fitness_redesign_2026_05_25]]
- RAD コーパス: `evolutionary_computation` 分野を増設中（arXiv fetch 背景実行、Stream C の evo-comp 弱点補強）
