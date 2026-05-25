# Evolution Research — Stream B: Open-Endedness & Quality-Diversity

> **作成**: 2026-05-25 / **対象**: llive persona・認知進化アルゴリズムの再設計
> **問題**: proxy 進化が自明収束（founder 全絶滅 gen23 / best 頭打ち / 多様性崩壊 gen25）。
> 原因 = 目的が単峰「全因子を均等に高く」。本ストリームは **open-endedness（収束/停滞しない）**
> と **quality-diversity（単一最適でなく多様アーカイブ）** の文献を掃討し、falsifiable 要件へ昇格させる。
> **honest disclosure**: 全て proxy（決定論・LLM 非呼出）。実 LLM 評価は最終段（ollama, GO 待ち）。
> 投機的記述には【SPECULATION】を明示する。
> 関連: [[OPEN_ENDED_CULTURAL_EVOLUTION]] §1 の 12 設計原理。

---

## 1. 技術テーブル

| 技術 | 1 行説明 | 引用 / URL | 成熟度 |
|---|---|---|---|
| **Novelty Search (NS)** | 目的を捨て、行動の新規性のみで選択。欺瞞的地形で目的探索を上回る | Lehman & Stanley 2011, Evol. Comp. 19(2):189-223 / https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/lehman_ecj11.pdf | 確立（基礎・引用多数） |
| **NS with Local Competition (NSLC)** | NS + k-NN 近傍内のみの局所適応度競争を NSGA-II Pareto で両立。1 run で多様な高品質形態を発見 | Lehman & Stanley 2011 (GECCO) / https://stars.library.ucf.edu/scopus2010/2703/ | 確立（QD の祖） |
| **MAP-Elites** | 行動記述子で区切った grid の各 cell に elite を保存し探索空間を「照らす」 | Mouret & Clune 2015 / https://arxiv.org/abs/1504.04909 | 確立（QD 旗艦・実装多数） |
| **CVT-MAP-Elites** | 重心 Voronoi 分割で cell 数を次元非依存に固定。高次元記述子に scale | Vassiliades+ 2016/2018 / https://arxiv.org/abs/1610.05729 | 確立 |
| **CMA-ME** | CMA-ES emitter 群を共有 archive に同期。flat fitness で MAP-Elites より高速照射 | Fontaine+ 2020 (GECCO) / https://arxiv.org/abs/1912.02400 | 確立 |
| **CMA-MAE** | discount 関数を annealing し CMA-ES↔CMA-ME を滑らかに blend。CMA-ME の早期目的放棄/flat 弱点を解消 | Fontaine & Nikolaidis 2022/2024 / https://arxiv.org/abs/2205.10752 | 確立（QD の現 SOTA 系） |
| **AURORA** | VAE で軌跡から行動記述子を**教師なし学習**。記述子を手設計しない QD | Cully 2019; Grillotti & Cully 2021 / https://arxiv.org/abs/2106.05648 | 成熟途上（強力だが配線重い） |
| **Dominated Novelty Search** | NSLC の局所競争を「自分を支配する近傍密度」で再定式化。記述子境界に鈍感 | Templier+ 2025 / https://arxiv.org/html/2502.00593v1 | 新興（2025・要検証） |
| **POET / Enhanced POET** | 環境（課題）と解の対進化。stepping-stone を転移し無限カリキュラム生成 | Wang+ 2019/2020 / https://arxiv.org/abs/1901.01753 ; https://arxiv.org/abs/2003.08536 | 確立（OEE 代表・重量級） |
| **Minimal Criterion Coevolution (MCC)** | 「最小基準（=繁殖可否）を満たせ」だけで 2 集団が開放端的に拡張。novelty 明示計算不要 | Brant & Stanley 2017 (GECCO) / https://stars.library.ucf.edu/scopus2015/7496/ | 確立（OEE 軽量代替） |
| **Minimal Criterion (MC) / viability 選択** | スカラー最大化でなく「生存可能性の閾値」を満たせば繁殖。Soros&Stanley 4 条件の核 | Soros & Stanley 2014; Brant&Stanley 2017 | 確立 |
| **AI-GAs（3 pillars）** | (1) アーキ meta-learn (2) 学習則 meta-learn (3) **学習環境の自動生成**。open-ended に「永遠に学ぶ」 | Clune 2019 / https://arxiv.org/abs/1905.10985 | パラダイム提唱（実装は研究中） |
| **Fitness Uniform Selection (FUSS)** | 高 fitness でなく**疎な fitness 帯**へ選択圧。多様性完全崩壊が原理的に不可能 | Hutter & Legg 2002/2006 / https://arxiv.org/abs/cs/0610126 | 確立（軽量・実装容易） |
| **Fitness Uniform Deletion (FUDS)** | 削除時に「fitness 帯が混んでいる個体」を消す。単峰へ集約しない | Legg & Hutter 2005 / https://arxiv.org/pdf/cs/0504035 | 確立 |
| **OEE 形式要件（5 条件）** | robustly-reproductive / 無限多様性媒体 / より複雑な子 / 変異経路 / 進化駆動。bounded↔unbounded を区別 | Taylor 2015/2016 / https://arxiv.org/pdf/1507.07403 | 理論（設計チェックリスト） |
| **OEE 4 必要条件（Soros&Stanley）** | (1) 非自明な MC を課す (2) 新個体が新たな MC 充足機会を生む (3) 相互作用は個体が決める (4) phenotype は原理上無限 | Soros & Stanley 2014; 2019 / https://direct.mit.edu/artl/article/25/2/198/2923 | 理論（最有用な実装指針） |
| **Evolved Open-Endedness（OEE≠EOE）** | 開放端性は「与える」ものでなく**進化で獲得される性質**。系は開放端性そのものを進化させねば持続しない | Pattee & Sayama 2019 / Banzhaf+ 2016 | 理論（深い・設計思想） |
| **QD-score / coverage / 多様性指標** | archive 充填率(coverage) と Σelite-fitness(QD-score) で「照らし具合」を測る | Pugh, Soros & Stanley 2016, Front. Robot. AI / https://www.frontiersin.org/articles/10.3389/frobt.2016.00040/full | 確立（評価デファクト） |
| **multi-BC QD** | 複数の行動特徴づけ（BC）を同時に走らせ、diversity が quality と非整合な欺瞞地形を打開 | Pugh+ 2016 "Searching for QD…" | 確立 |
| **Free-Market Algorithm（FMA）** | 供給需要動学で fitness が**創発**、探索空間が open-ended。固定 fitness/空間を持たない metaheuristic | Jaraiz 2026 arXiv:2603.24559（corpus 内） | 新規（2026・未検証だが思想近接） |
| **Diversity Collapse（反面教師）** | MAS の密結合相互作用が探索を収縮させ多様性崩壊。独立性と不一致の保持が鍵 | Chen+ 2026 arXiv:2604.18005（corpus 内） | 新規（llive に直接示唆） |

---

## 2. Falsifiable な要件文（MUST / SHOULD）

> 全て **proxy run（決定論）上で測定可能** な形にした。各要件に検証コマンド観点を付す。
> 旧診断（founder 絶滅 gen23 / best 頭打ち gen281 / 多様性崩壊 gen25）を「絶対に再発させない」反証条件群。

### A. Open-endedness（収束/停滞しない）

- **OE-1（MUST）**: 選択はスカラー最大化を**禁止**する。fitness はスカラー単峰目的で定義してはならない。
  *反証*: `_proxy_fitness` 系が単一スカラーの argmax 選択を行っていれば FAIL。
- **OE-2（MUST）**: archive サイズ（占有 cell 数 / 既知行動の数）は run を通じて**単調非減少**で、
  末尾 20% 世代でも `Δarchive > 0` の世代が ≥ 1 回出ること（成長が完全停止しない）。
  *反証*: 末尾 20% で archive growth が恒常的に 0 なら停滞＝FAIL。
- **OE-3（MUST）**: いかなる単一系統（founder lineage）も集団の **> 80% を占有してはならない**（monoculture 禁止）。
  *反証*: 任意世代で 1 lineage 占有率 > 0.8 → 旧 founder 絶滅→単系統化の再発＝FAIL。
- **OE-4（MUST）**: founder lineage の**早期全絶滅を禁止**。多様性保存機構（FUSS/FUDS or QD archive 不削除）により、
  少なくとも archive 内では初期系統の代表が gen23 相当時点で残存すること。
  *反証*: 旧来どおり gen23 で founder 全絶滅なら FAIL。
- **OE-5（SHOULD）**: best 個体記述子は世代を追って**新しい cell へ移動し続ける**（goal-switching 許容）。
  best の記述子が長期固定（例 100 世代変化なし）＝停滞兆候。
- **OE-6（MUST）**: 選択は**最小基準（MC）型を含む**（Soros&Stanley #1）。「ある閾値を満たせば繁殖可」を採用し、
  繁殖可否を連続スカラー順位だけで決めない。MC は非自明（全個体が常に満たすほど緩くない）。
  *反証*: 全個体が MC を常時満たす（=実質無効）なら非自明性 FAIL。
- **OE-7（SHOULD, Soros&Stanley #2）**: 新個体の出現が**新たな MC 充足機会を生む**経路を 1 つ以上持つ
  （例: 獲得 persona が次世代の MC 対象を拡張、belief space 更新が新ニッチを開く）。

### B. Quality-Diversity（多様アーカイブを成果物に）

- **QD-1（MUST）**: 成果物は**単一 best でなく QD アーカイブ**（cell→elite map）。run 終了時に
  archive を JSON で出力し、各 cell に記述子＋elite を保持する。
- **QD-2（MUST）**: 記述子は**絶対値でなく相対構造**（z-score 標準化）。全因子満点→フラット→無特徴を
  検証で確認（標準化後に全個体同一なら記述子無効）。
- **QD-3（MUST）**: archive は**新規性に基づく不削除原則**を持つ。新 cell の個体は既存 cell elite を消さない
  （MAP-Elites/CVT-MAP-Elites のセル別保存）。⇒ 多様性は構造的に崩壊不能（FUSS と同精神）。
- **QD-4（SHOULD）**: 記述子は `z(c_factors) ⊕ z(c_cultural) ⊕ z(c_latent)`。意味因子（人間らしさ）と
  中立貯蔵庫（予期せぬ特異）の**併存**を記述子が読む（§OPEN_ENDED #3-#6,#10 の「消費目的とセット」）。
- **QD-5（SHOULD）**: cell 数は **CVT-MAP-Elites** で次元非依存に固定（記述子 17+次元の grid 爆発回避）。
- **QD-6（SHOULD）**: **複数 BC（multi-BC）** を許容（c_factors 軸 / cultural 軸 / latent 軸）。
  単一 BC が quality と非整合な欺瞞を打開（Pugh+ 2016）。
- **QD-7（MUST, 反・収束）**: 局所競争を採用する場合は**グローバル競争でなく局所**（NSLC: k-NN 近傍内のみ fitness 比較）。
  グローバル順位選択は monoculture を招くため禁止。

### C. 「特異が生き残る」選択圧（保守を淘汰）

- **SEL-1（MUST）**: 中央一致（平均への近さ）を**報酬から除外**（#2）。中心に居ることが有利になってはならない。
- **SEL-2（SHOULD）**: PERSONA-FX の **pull 型獲得＝報酬**を選択圧に組込む。平均から逸脱した個体が
  相関 argmax で persona を獲得し、獲得が適応度に寄与（「平均を外れること」自体が多様性エンジン）。
- **SEL-3（SHOULD）**: **FUSS 的選択**（疎な fitness/記述子帯への選択圧）を novelty scheduler に併用。
  完全な多様性崩壊を原理的に不可能にする。
- **SEL-4（SHOULD）**: **疎変異 + 大規模ゲノム**（毎世代ごく一部だけ変異, c_latent 大）を維持（#4,#5）。
  小調節変異が大効果（evo-devo）＝特異の供給源。

### D. メタ（要件運用）

- **META-1（MUST）**: 各 run は proxy/real ラベルを記録（[[feedback_benchmark_honest_disclosure]]）。
- **META-2（MUST）**: 学習信号（Baldwin/belief）と遺伝 fitness は**分離記録**（measurement purity）。
- **META-3（SHOULD）**: 上記指標（archive growth, monoculture率, QD-score, coverage）を毎 run で
  baseline と並べて可視化（Stage ごとに改善を反証可能に）。

---

## 3. 設計原理（§OPEN_ENDED 12 原理）へのマッピング

| 原理# | 本ストリームが裏付ける機構 | 対応要件 |
|---|---|---|
| #1 正規化/標準化 | z-score 記述子（QD の BC 設計, AURORA も latent 標準化） | QD-2, QD-4 |
| #2 中央が勝つ系は無理 | NS は中心を報酬にしない / FUSS は疎帯へ | SEL-1, OE-1 |
| #3 突然変異から特異が生き残れ | Novelty Search（目的は欺瞞, 新規性が勝つ） | OE-1, SEL-2, SEL-4 |
| #4 余計な因子（中立） | 中立ネットワーク + AURORA latent + c_latent を記述子へ | QD-4, SEL-4 |
| #5 個体差は遺伝子の一部から | 疎変異 + 大規模ゲノム（evo-devo） | SEL-4 |
| #6/#7 文化・人間要素 | multi-BC（cultural 軸を BC に） | QD-4, QD-6 |
| #8 希望個体が pull 獲得 | NSLC 局所競争 + 獲得＝報酬。Soros&Stanley #3「相互作用は個体が決める」 | SEL-2, OE-7, QD-7 |
| #9 経験・学習が確率を上げる | Baldwin（学習が地形を均す）＋ Cultural Algorithm belief（AI-GAs pillar 適応） | OE-7, META-2 |
| #10 染色体/次元を増やす（消費とセット） | CVT-MAP-Elites（高次元 BC を scale）＋ multi-BC が次元を**消費** | QD-4, QD-5, QD-6 |
| #11 最適解が賢いとは限らない | QD アーカイブ＝多様性の地図（単一最適を捨てる） | QD-1, QD-3 |
| #12 アルゴ部分も進化 | AI-GAs 3 pillars（特に学習則/環境の meta 生成）, CMA-MAE annealing | （Stream A メタ進化と接続） |

---

## 4. ADOPT vs AVOID（正直な理由）

### ADOPT

- **MAP-Elites / CVT-MAP-Elites（archive 本体）** — 既存 `MAPElitesGrid` を流用可、cell 別保存で
  多様性崩壊が**構造的に不可能**。17+次元記述子には CVT 版（grid 爆発回避）。確立・実装容易。
- **Novelty Search を選択の核に** — 旧単峰収束の直接対策。llive `SchedulerFn` が集団全体を受け取るので
  集団相対 novelty を注入でき、per-individual fitness 制約を回避できる（設計的に好相性）。
- **NSLC の局所競争** — グローバル競争 = monoculture を避ける。pull 型 persona 獲得（#8）と同じ
  「近い者同士で競う」精神。Pareto(NSGA-II) は既存 `nsga2.py` 流用可。
- **Minimal Criterion（MC）型選択** — Soros&Stanley 4 条件の核。スカラー argmax を捨てる最小変更で
  「保守が勝つ」を断つ。MCC 全体は重いが **MC の発想だけ**採れば軽量。
- **FUSS/FUDS** — 軽量で「多様性完全崩壊が原理的に不可能」を保証。novelty scheduler の保険として併用推奨。
- **QD-score / coverage 指標** — 評価デファクト。Stage 比較に必須（§5）。
- **multi-BC（c_factors / cultural / latent の複数軸）** — 欺瞞地形打開。記述子設計の自然な拡張。

### AVOID（または保留）

- **POET / Enhanced POET 全体** — 重量級（環境共進化 + ES 群 + 転移）。llive の persona 進化は
  「環境を生成する」問題設定でないため過剰。**stepping-stone 転移と goal-switching の発想だけ**借用（OE-5）。
- **AURORA（教師なし記述子）全配線** — VAE をオンライン学習する配線が重く、proxy 段では手設計記述子
  （z-score c_factors⊕cultural⊕latent）で十分。**実 LLM 段（Stage6）で軌跡が出てから再検討**【SPECULATION】。
- **AI-GAs フル実装** — パラダイム提唱で実装指針が薄い。pillar 3（環境生成）は llive に直結しない。
  pillar 1/2（meta 学習）は **Stream A（メタ進化）に委譲**。
- **Free-Market Algorithm** — 2026 新規・未検証で fitness 創発の魅力はあるが、既存 llive 資産との
  接続コストが高い。**思想（fitness を固定しない）だけ参照**、採用は見送り。
- **CMA-ME/CMA-MAE の CMA-ES emitter** — 連続パラメータ最適化に強いが llive ゲノムは
  混在型（factor + impl 選択 + prompt）。**annealing 思想（discount で探索↔最適化を blend）は将来候補**、
  emitter 機構そのものは過剰【SPECULATION】。
- **Dominated Novelty Search** — 2025 新興で魅力的（記述子境界に鈍感）だが**未検証**。
  NSLC で実績を作ってから差し替え候補として保持。

> **honest disclosure**: 基盤（NS/QD/中立NW/MC/文化次元）は全て既存。FullSense 独自性は
> **(意味文化因子 + 中立貯蔵庫) × 標準化 novelty × pull 型 persona 獲得 × Baldwin 学習 × on-prem 監査**
> の**統合**であり、個別アルゴリズムの新規性ではない（§OPEN_ENDED §5 と一致）。

---

## 5. 「本当に進化しているか / open-ended か」の測定（具体メトリクス）

> 各 run 終了時に算出し、baseline（旧単峰 proxy）と並置。proxy 段で全て計算可能。

### 一次メトリクス（open-endedness の核）

1. **Archive growth curve（最重要）** — 占有 cell 数（または既知行動数）の世代推移。
   - 判定: 末尾 20% 世代でも増加世代が ≥1 → open-ended の兆候。完全 plateau → 停滞。
   - 旧来: best 頭打ち gen281 = plateau。これを**消す**ことが Stage2 の合否。
2. **Monoculture ratio** — 任意世代の `max_lineage_share = max_i(count_i)/N`。
   - 判定: 全世代で **< 0.8** を維持（OE-3）。旧来は単系統化していた。
3. **Lineage survival @ gen23** — 初期 founder 系統の archive 内残存数。
   - 判定: **> 0**（OE-4）。旧来 0（全絶滅）。

### 二次メトリクス（quality-diversity の質）

4. **QD-score** = Σ(各 cell elite の fitness)。多様性×品質の総和。世代で**増加**を確認（Pugh+ 2016）。
5. **Coverage** = 占有 cell 数 / 全 cell 数。空間をどれだけ「照らした」か。
6. **Behavioral diversity** = 集団記述子の平均ペアワイズ距離（or 記述子分散）。
   - 判定: 旧来 gen25 で崩壊（→0）。**高止まり**（非ゼロで安定）すれば成功。
7. **Novelty trajectory of best** — best 個体記述子の世代間移動距離の累積。
   - 判定: 単調増加（goal-switch し続ける）→ open-ended。早期飽和 → 収束（OE-5）。

### 三次メトリクス（OEE 形式チェック・Taylor/Soros-Stanley）

8. **MC 非自明性チェック** — 各世代で MC を満たす個体比率。
   - 判定: 0 < ratio < 1（全員でも全滅でもない）＝ MC が選択圧として機能（OE-6）。
9. **新規 MC 機会の生成率** — 新 cell 出現が新しい繁殖機会（新 persona 獲得 / belief 更新）を
   開いた回数 / 世代。> 0 が持続 → Soros&Stanley #2 充足（OE-7）。【一部 SPECULATION: 計測定義は実装時に確定】
10. **Bounded vs unbounded 判定（Taylor）** — archive growth と complexity（記述子有効次元数 = PCA で
    分散の 95% を説明する成分数）の長期トレンド。両方が頭打ち → bounded（=失敗）。

### 反証テスト（regression guard）

- **旧単峰 proxy を baseline として常に並走測定**。新設計が baseline 比で
  「archive growth が立つ / monoculture < 0.8 / behavioral diversity 非崩壊 / founder gen23 残存」
  の**4 点全て**で勝てなければ Stage は不合格（FAIL を消さず記録）。

---

## 参考文献（主要）

- Lehman & Stanley 2011, *Abandoning Objectives*, Evol. Comp. 19(2). https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/lehman_ecj11.pdf
- Lehman & Stanley 2011, *Evolving a Diversity of Creatures through NSLC* (GECCO). https://stars.library.ucf.edu/scopus2010/2703/
- Mouret & Clune 2015, *Illuminating search spaces by mapping elites*. https://arxiv.org/abs/1504.04909
- Vassiliades, Chatzilygeroudis, Mouret 2016, *CVT-MAP-Elites*. https://arxiv.org/abs/1610.05729
- Fontaine+ 2020, *CMA-ME (Rapid Illumination of Behavior Space)*. https://arxiv.org/abs/1912.02400
- Fontaine & Nikolaidis 2022, *CMA-MAE*. https://arxiv.org/abs/2205.10752
- Grillotti & Cully 2021, *AURORA (Unsupervised Behaviour Discovery with QD)*. https://arxiv.org/abs/2106.05648
- Templier+ 2025, *Dominated Novelty Search*. https://arxiv.org/html/2502.00593v1
- Wang+ 2019, *POET*. https://arxiv.org/abs/1901.01753 ; Wang+ 2020, *Enhanced POET*. https://arxiv.org/abs/2003.08536
- Brant & Stanley 2017, *Minimal Criterion Coevolution* (GECCO). https://stars.library.ucf.edu/scopus2015/7496/
- Soros & Stanley 2014/2019, *Open-Endedness for the Sake of Open-Endedness*, Artificial Life 25(2). https://direct.mit.edu/artl/article/25/2/198/2923
- Stanley, Lehman, Soros 2019, *Why Open-Endedness Matters*, Artificial Life 25(3). https://direct.mit.edu/artl/article/25/3/232/2917
- Clune 2019, *AI-GAs*. https://arxiv.org/abs/1905.10985
- Hutter & Legg 2002/2006, *Fitness Uniform Optimization (FUSS)*. https://arxiv.org/abs/cs/0610126 ; Legg&Hutter 2005, *FUDS*. https://arxiv.org/pdf/cs/0504035
- Taylor 2015/2016, *Requirements for Open-Ended Evolution*. https://arxiv.org/pdf/1507.07403
- Pugh, Soros & Stanley 2016, *Quality Diversity: A New Frontier*, Front. Robot. AI. https://www.frontiersin.org/articles/10.3389/frobt.2016.00040/full
- Pattee & Sayama 2019, *Evolved Open-Endedness, Not Open-Ended Evolution*, Artificial Life. (OEE≠EOE 区別)
- corpus: Chen+ 2026 *Diversity Collapse in Multi-Agent LLM Systems* arXiv:2604.18005 ; Jaraiz 2026 *Free-Market Algorithm* arXiv:2603.24559
