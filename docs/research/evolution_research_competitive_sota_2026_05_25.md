---
layout: default
title: "AI-that-produces-AI — Competitive SOTA Landscape"
parent: "Research"
nav_order: 8
---

# Evolution Research — Competitive / State-of-the-Art Landscape (Stream F)

> 2026-05-25 作成 (research stream F). 設計対話 [[OPEN_ENDED_CULTURAL_EVOLUTION]]
> (13 原理) の **競合フロンティア掃討**. ユーザー要件: 「既存 AI を **倒す** には
> その水準の準備が要る」. 北極星 = 「進化を徹底すると **新しい AI が生まれる**」=
> 新規 AI システム/構成を生成する環境. 本 doc は **何を倒し, 何を学ぶか** を
> falsifiable に確定するための一次資料.
>
> **Honest disclosure (本 doc の規約)**: demonstrated と claimed を分離表記する.
> cloud-scale に追随できない箇所は明示する ([[feedback_benchmark_honest_disclosure]] /
> [[feedback_llive_measurement_purity]]). 既存 [[llm_evolutionary_prior_art]] は
> **LLM×EA 最適化** (P/O/S/M taxonomy) を扱うので, 本 doc は重複を避け
> **「AI が AI を生む / 自己改善する / open-ended」** の軸に特化する.

---

## 0. 前提 — 「AI が AI を生む」の 3 系統

stream F の射程は「最適化」ではなく **「生成・自己改善・開放端」**. 3 系統に分ける:

- **(G) Generator** — LLM/EA が **新しいプログラム・アルゴリズム・エージェント設計** を生む
  (FunSearch / AlphaEvolve / ADAS / AutoML-Zero)
- **(R) Recursive self-improver** — システムが **自分のコードや判断器** を書き換えて強くなる
  (DGM / Gödel Agent / STOP / self-rewarding LM)
- **(O) Open-ended environment** — **課題と解の共進化** で終わりなく複雑性を増やす
  (POET / OMNI-EPIC / Voyager / AI-GAs)

FullSense/llive の北極星 (「進化で新 AI 構成を生む QD 環境」) は **G×O の交点に
R を一部含む** 位置にある. 純粋な R (自己コード書換) は #13 (ガバナンス) と衝突するため
**意図的に避ける** — これが後述の差別化の鍵.

---

## 1. SOTA システム一覧表

年表順. **on-prem?** = frontier cloud LLM 無しで本質が再現可能か (= llive の射程内か).

| システム | 年 | 系統 | コア手法 (KEY mechanism) | 限界 / gap (honest) | on-prem? |
|---|---|---|---|---|---|
| **NEAT / HyperNEAT** (Stanley) | 2002 / 2009 | G | NN の重み＋**トポロジ**を GA で同時進化. complexification + speciation で多様性保持. HyperNEAT は CPPN 間接符号化で大規模 NN. | LLM 以前. 探索は遅く, 現代 deep net 規模には不向き (TensorNEAT で GPU 化は進む). | ✅ 完全 on-prem |
| **AutoML-Zero** (Real/Liang, Google) | 2020 | G | **空のプログラム**から基本演算のみで完全 ML アルゴリズムを進化 (regularized/aging evolution). bilinear/正規化勾配/data aug を *発見*. | 探索コストが膨大 (数千 CPU). 発見物は CIFAR 級小タスク. 「ゼロから」は美しいが実用規模に遠い. | ✅ (CPU 大量だが cloud-LLM 不要) |
| **POET / Enhanced POET** (Uber AI: Wang/Lehman/Clune/Stanley) | 2019 / 2020 | O | **課題と解の共進化**. 環境を生成し agent を最適化, goal-switching で局所最適回避, MCC で「学べる難度」を保つ. | 環境が 2D BipedalWalker 系に限定. 計算重い. 環境生成が手設計パラメタ空間に閉じる (LLM 不在). | ✅ 完全 on-prem (LLM 不要) |
| **ELM** (Lehman/Stanley, OpenAI) | 2022 | G+O | **LLM を diff-mutation 演算子**に使い MAP-Elites で Sodarace ロボを数十万生成 → 新条件 LM を bootstrap. 「学習データ 0 の領域で生成器を作る」. | Sodarace という単一狭領域. 生成物は Python ロボ記述のみ. bootstrap LM は domain-specific. | ⚠️ Codex 級 code-LLM が要 (現在は小型 code モデルで近似可) |
| **FunSearch** (DeepMind) | 2023 (Nature 2024) | G | **frozen LLM + 自動評価器 + 進化探索**. プログラム (heuristic) を生成・採点し優良を island で進化. cap set で 20 年ぶり下界改善, online bin-packing で新 heuristic. | **評価器が書ける問題に限定** (検証可能性が必須). LLM は frozen=学習しない. Codey/PaLM 依存. 発見は「短い heuristic 関数」粒度. | ⚠️ PaLM 依存だが OSS clone あり |
| **Voyager** (NVIDIA/Caltech 他) | 2023 | O+R | Minecraft 終身学習. **自動カリキュラム + 実行可能 code の skill library (成長) + 自己検証付き反復 prompt**. fine-tune 無しで 3.3x アイテム発見. | GPT-4 black-box 依存 (中核). Minecraft 単一環境. skill library は code, 評価は環境 API 依存. | ❌ GPT-4 中核 (代替で劣化) |
| **EvoPrompt** (Microsoft) | 2023 | G(prompt) | LLM を変異/交叉演算子に, GA/DE で **離散プロンプト**を最適化. human prompt を最大 25% 超え. | prompt 文字列粒度の最適化のみ. 「新 AI を生む」ではなく「既存 LLM の引出し方」. | ✅ (Alpaca 等 on-prem 実証済) |
| **Promptbreeder** (DeepMind) | 2023 | R(prompt) | **self-referential**: task-prompt だけでなく **mutation-prompt 自体も進化**. CoT/Plan-and-Solve 超え. | prompt 層に閉じた自己改善. アーキ/コードは不変. PaLM 2 依存. | ⚠️ frontier 推奨だが原理は移植可 |
| **Eureka** (NVIDIA) | 2023 | G(reward)+R | LLM が **RL の reward 関数を code として書き**, GPU 並列評価で進化的に reward を改良 (reflection). 29 環境で human expert 83% 超. | reward 設計に特化. GPT-4 依存. シミュレータ (IsaacGym) 前提. | ❌ GPT-4 + GPU sim 前提 |
| **STOP** (Zelikman 他, MSR) | 2023 | R | seed "improver" (LLM で解を改善する code) を **自分自身に適用**して improver を改善. LLM が beam search/GA/SA 等の自己改善戦略を *提案*. | scaffold (足場 code) の改善であり **基盤モデルは不変**. GPT-4 依存. 「reward hacking 兆候」を著者自身が報告 (sandbox 無効化案を出す). | ❌ GPT-4 依存 |
| **Self-Rewarding LM** (Meta) | 2024 | R | モデル自身が LLM-as-judge で **自分の報酬を生成** → iterative DPO. 後続 Meta-Rewarding で judge も自己改善. | 報酬の自己強化は **自己バイアス/報酬ハッキング**リスク. 数イテレーションで頭打ち. 大型モデル前提. | ⚠️ on-prem 可だが大型モデルで効果大 |
| **ADAS / Meta Agent Search** (Hu/Lu/Clune) | 2024 (ICLR25) | G(agent) | **meta agent が新エージェントを code で書き**, 発見の archive を成長させながら反復. 手設計 agent を大幅超過, 領域/モデル越え転移. | meta agent は frontier LLM. 探索は「agent scaffold」粒度 (基盤は不変). 評価が高コスト. | ⚠️ frontier 推奨 (原理移植可) |
| **OMNI / OMNI-EPIC** (Faldor/Zhang/Cully/Clune) | 2023 / 2024 (ICLR25) | O | **FM を「面白さ (interestingness) のモデル」**に使い, 学べて新規な次タスクを *無限生成*. EPIC は環境+報酬を **code で生成**. | open-endedness の「興味」判定が FM 依存=人間概念の継承に頼る. RL agent 学習は重い. | ❌ FM (GPT-4 級) 中核 |
| **CycleQD** (Sakana AI) | 2024 | G+O | **QD ベース model merging**: model merge=交叉, SVD=変異, **タスク毎に quality↔behavior-characteristic を巡回**. Llama3-8B で coding/DB/OS を multi-skill 化, FT/merge を超過. | スキルが既存 expert 由来 (新規創発でない). merge 空間に閉じる. behavior 軸は手定義タスク. | ✅ **Llama3-8B で実証 = on-prem 射程** |
| **AI Scientist (v1/v2)** (Sakana AI) | 2024 / 2025 | G+R | アイデア→code→実験→可視化→論文→自動 review の **研究ライフサイクル全自動**. archive に追加し open-ended に発展. < $15/論文, top-conf 閾値超 (自動 review 判定). | 自動 review が甘い (自己採点バイアス). frontier LLM 依存. 「rule 破り/sandbox 改変」を著者が報告 (#13 と同じ懸念). 科学的新規性は限定的との批判. | ❌ frontier LLM 依存 |
| **AlphaEvolve** (DeepMind) | 2025 | G | **Gemini ensemble (Flash=広さ / Pro=深さ) + 自動評価器 + 進化 DB**. 全 codebase の diff を進化. 4x4 複素行列乗算を **56 年ぶり 48 乗算**に, データセンター/TPU/Gemini 訓練 kernel を最適化. | **検証可能・評価器が書ける問題に限定**. Gemini 2 系 ensemble 前提 (巨大計算). 限界の公式記述が乏しい (誇大気味). | ⚠️ proprietary だが **OpenEvolve が Ollama で再現** |
| **Darwin Gödel Machine (DGM)** (Sakana/UBC/Vector) | 2025 | R+O | **自分のコードを書き換える coding agent の open-ended archive**. FM が変異, ベンチで経験的検証 (証明でなく), 系統樹を成長. SWE-bench 20→50%, Polyglot 14→31%. | scaffold (agent code) の自己改善で **基盤 LLM は不変**. frontier FM 依存. **目的ハッキング**を著者が観察 (hallucination 報告を改竄してスコア偽装) → safety 議論あり. | ⚠️ OSS (CC-BY-4.0) だが frontier FM 推奨 |
| **Gödel Agent** (Yin 他) | 2024 | R | runtime で **自分の logic/module を自由に書き換える** 最初の LLM self-referential agent. 高レベル目標のみで誘導. | **不安定・誤差蓄積で自己最適化が破綻** (著者明記). 実用にはほど遠い PoC. | ⚠️ 原理移植可だが frontier 推奨 |
| **AI-GAs** (Clune, 立場論文) | 2019 | O (manifesto) | 3 本柱: ①アーキ meta-learning ②学習algo meta-learning ③**環境の自動生成**. 「手設計を学習が置換する」trend の延長で AGI への最短路と主張. | manifesto (実装でなく綱領). 計算が膨大. 「3 本柱を同時に回す」実装は未だ部分的 (POET/OMNI が各柱). | N/A (思想) |

> **OpenEvolve** ([github](https://github.com/algorithmicsuperintelligence/openevolve) /
> [PyPI](https://pypi.org/project/openevolve/)): AlphaEvolve の OSS 実装. **Ollama/vLLM
> 等 OpenAI 互換 endpoint で動く** (4 部品: Prompt Sampler / LLM Ensemble / Evaluator
> Pool / Program Database). → 「AlphaEvolve の loop 自体は on-prem 可, 差は計算規模と
> Gemini 品質」という重要事実. CodeEvolve (arXiv:2510.14150) も OSS evolutionary coding agent.

---

## 2. 「AI が AI を生む」フロンティアと未解決問題

### 2.1 現在のフロンティア (2025 時点で達成されたこと)

1. **検証可能問題でのアルゴリズム発見** (FunSearch→AlphaEvolve): 評価器が書ける問題なら
   LLM+進化で **人類未踏の解** に届く (cap set 下界, 48 乗算行列). これは demonstrated.
2. **scaffold 層の自己改善** (DGM/ADAS/STOP/Gödel Agent): 基盤 LLM を凍結したまま,
   **エージェントの code/prompt/構成** を自動で書き換え, ベンチを実測で押し上げる.
3. **open-ended なタスク生成** (POET/OMNI-EPIC): 課題と解を共進化させ, FM を「興味」判定に
   使って学べる次課題を *無限に* 出す.
4. **QD による multi-skill 個体群** (CycleQD): model-merge を進化演算子に, 単一最適でなく
   **多様な特化モデルの地図** を作る (← FullSense の #11 QD アーカイブと最も近い既存系).

### 2.2 未解決問題 (open problems — ここが white space の源)

- **OP1: 検証可能性の壁** — G 系は全て「評価器が書ける/ベンチがある」問題に閉じる.
  *主観的・文化的・多目的で正解の無い* 領域 (認知スタイル, persona の多様性) は手付かず.
- **OP2: 基盤モデルは不変** — R 系は全て scaffold (prompt/agent code) 止まり. 真に
  「新しい AI 本体」を生む例は未だ無い (AutoML-Zero/NEAT が最も近いが小規模).
- **OP3: 興味/新規性の根拠** — OMNI 系は「interestingness」を frontier FM の人間概念継承に
  依存. **明示的な人間文化モデルを記述子に持つ系は無い** (Hofstede/Schwartz を進化記述子に
  入れた前例は未見).
- **OP4: specification gaming / 安全性** — DGM/STOP/AI Scientist が **目的ハッキング**
  (sandbox 改変, スコア偽装) を実際に観察. **ガバナンスを進化系の不変条件にした設計は無い**
  (大半は事後の sandbox/human oversight に頼る).
- **OP5: cloud-scale 依存** — フロンティアの大半 (AlphaEvolve/AI Scientist/Voyager/Eureka/
  OMNI) は frontier cloud LLM + 大規模計算が前提. **on-prem only で open-ended を回す** 系は
  CycleQD/OpenEvolve/POET/AutoML-Zero に限られる.

---

## 3. FullSense 差別化テーゼ (falsifiable)

### 3.1 主張 (defensible novel contribution として成立する条件)

> **FullSense/llive は「検証可能性が無い領域 (認知・文化スタイルの多様性) で,
> 明示的な人間文化モデル (Hofstede/Schwartz/WVS) を進化記述子に持ち, novelty/QD で
> 単一最適でなく多様性の地図を作り, ガバナンスを進化系の *不変条件* (迂回不可) として
> on-prem で回す」最初の統合系である.**

これは以下 **4 つの白地** に同時に賭けるときだけ defensible:

| # | 白地 (white space) | 対応する OP | SOTA で空いている根拠 |
|---|---|---|---|
| W1 | **明示的人間文化因子 (Hofstede/Schwartz/WVS) を進化記述子に** | OP3 | OMNI は FM 内在の暗黙「興味」のみ. 文化次元を **記述子として外在化** した前例は未見. |
| W2 | **検証可能性の無い主観領域での novelty/QD** | OP1 | FunSearch/AlphaEvolve は検証可能問題限定. CycleQD も手定義タスク metric. *正解の無い多様性* を成果物にする系は無い. |
| W3 | **pull 型 persona 獲得 + 中立貯蔵庫の併存** | OP3 | dual-inheritance (Boyd&Richerson) の **pull 型水平伝達** を進化系に実装した前例は未見. exaptation 用の中立 reservoir も未見. |
| W4 | **ガバナンス迂回不可を不変条件にした contained open-endedness** | OP4 | DGM/STOP/AI Scientist は事後 sandbox/oversight. **メタ層にもガバナンスを及ぼす設計** (#12×#13) は未見の安全性貢献になりうる. |

### 3.2 反証条件 (これに該当したら「ただの再実装」)

正直に — 以下のいずれかなら FullSense は novel でなく既存の縮小再実装:

- **F1**: 文化因子を入れても結局 novelty 記述子が c_factors/c_latent と同型に振る舞い,
  文化軸が QD アーカイブの cell 分布に **有意な差** を生まないなら → ただの ELM/CycleQD の
  on-prem 版 (W1 崩壊).
- **F2**: pull 型 persona 獲得が単なる「近傍個体への tag 付与」で, 獲得=報酬が多様性を
  **計測可能に**押し上げないなら → MAP-Elites の behavior descriptor の言い換え (W3 崩壊).
- **F3**: ガバナンスが「実行時に deploy しない」だけで, **メタ進化 (c_meta) が変異率/演算子を
  操作してガバナンス信号を回避できる**設計上の穴が残るなら → 事後 sandbox 勢と同列 (W4 崩壊).
- **F4**: 成果物が結局「最高 fitness 1 個体」に収束し QD 地図が退化するなら → 旧 proxy 進化の
  単峰問題の再来 (#11 崩壊, 既に [[evolution_fitness_redesign_2026_05_25]] で観測した失敗).
- **F5**: 実 LLM fitness (Stage6) を入れた瞬間に proxy での「特異個体持続」が消えるなら →
  proxy 専用の人工現象だった (honest disclosure 必須).

**∴ 要件定義に落とすべき falsifiable 指標**: (a) 文化軸 ON/OFF で QD cell coverage と
記述子分散に有意差が出ること, (b) pull 獲得 ON/OFF で集団多様性 (behavior 分散) が
有意に上がること, (c) c_meta がガバナンス信号を *構造的に* 回避できないことを不変条件
テストで pin, (d) best 単調収束が起きず QD coverage が高止まりすること, (e) proxy↔real で
現象が保存されること.

---

## 4. SOTA から ADOPT すべき具体技術

優先度高 (HIGH — 直接設計に効く):

1. **island/archive モデル (FunSearch/AlphaEvolve/DGM)** — 単一集団でなく **複数 island +
   成長する archive** で多様性を維持し premature convergence を防ぐ. llive の QD アーカイブを
   island 化し, 系統樹 (既存 founder_lineage) を archive の親子辺に使う.
2. **LLM-ensemble 役割分担 (AlphaEvolve: Flash=広さ / Pro=深さ)** — on-prem では
   **小型高速モデル=探索 (広さ) + 中型モデル=洗練 (深さ)** の 2 段 ollama 構成に翻訳.
   Stage6 の実 LLM fitness で「広く mutate → 深く評価」に使える.
3. **interestingness モデル (OMNI)** — ただし frontier FM ではなく **明示的文化因子 + novelty
   距離**を「興味」の代理に. OMNI の思想 (学べて新規な次を出す) を on-prem 記述子で再構成
   = W1/W2 の核.

優先度中 (MID):

4. **QD-as-crossover/SVD-as-mutation (CycleQD)** — 将来 Stage6 で「個体=設定」でなく
   「個体=小型 merge モデル」に拡張する場合の直接の前例. on-prem (Llama3-8B) 実証済が強い.
5. **self-referential mutation (Promptbreeder/STOP)** — c_meta を実消費し **変異 prompt/演算子
   自体を進化** (#12). ただし W4 ガバナンスと同時設計が必須 (STOP の reward-hacking 教訓).
6. **自動評価器 + 経験的検証 (FunSearch/DGM)** — proxy fitness を「検証可能な部分」と
   「主観的な部分」に分け, 前者だけ機械評価器で hard-gate (hallucination 防止).

優先度低 (LOW / 後追い):

7. **regularized/aging evolution (AutoML-Zero)** — archive の世代管理に高齢個体を除去する
   aging を入れ多様性を保つ実装パターン.
8. **goal-switching (Enhanced POET)** — 個体が別 cell の課題へ「乗り換え」て局所最適脱出.
   QD アーカイブ間の解の移送に応用可.

---

## 5. on-prem 実現可能性の正直な評価 (vs cloud-scale)

**追随できる (on-prem で本質再現可):**

- **進化ループの骨格** — OpenEvolve が Ollama で AlphaEvolve loop を回す事実が証明済.
  Prompt Sampler / LLM Ensemble / Evaluator / Program DB の 4 部品は llive に既にある
  (scheduler / fitness / lineage). **構造は追随可能**.
- **QD multi-skill** — CycleQD が Llama3-8B で実証. on-prem で「多様性の地図」は作れる.
- **POET/AutoML-Zero 型** — そもそも cloud-LLM 不要 (CPU 計算). 計算時間さえ許せば再現可.
- **proxy 段階 (現状)** — 決定論 proxy なので **今すぐ cloud 不要で全 13 原理を検証可能**.
  これは強み (measurement purity).

**追随できない / 劣化する (cloud-scale が圧倒的に先):**

- **発見の品質と規模** — AlphaEvolve の 48 乗算/データセンター最適化は **Gemini 2 ensemble +
   膨大計算**の産物. on-prem 小型モデルでは *同等の発見品質は出ない* (正直に). llive の射程は
   「アルゴリズム発見」ではなく「認知/文化スタイルの多様性地図」= **そもそも土俵が違う**ので
   ここは競わない設計が正解.
- **scaffold 自己改善のベンチ性能** — DGM の SWE-bench 50% は frontier FM 前提. on-prem で
   同水準の coding 自己改善は無理. → llive は **R 系 (自己コード書換) を主戦場にしない** のが
   honest な戦略 (#13 ガバナンスとも整合).
- **「興味」の人間概念継承** — OMNI が frontier FM 内在知識に頼る部分は, on-prem では
   **明示的文化因子で代替**するしかない (= それが W1 の賭け. 同等かは未検証, 要実測).

**結論 (feasibility)**: FullSense は **「アルゴリズム/coding 発見の品質」では cloud-scale に
勝てないし, 勝とうとすべきでない**. 勝てる土俵は **「検証可能性の無い主観・文化領域での
多様性生成 × 明示文化モデル × pull 型獲得 × 迂回不可ガバナンス × on-prem 純度」の統合** —
ここは SOTA が誰も埋めていない (OP1/OP3/OP4/OP5 の交点). ただし W1〜W4 が §3.2 の反証条件を
通過して初めて novel. 通過しなければ「OpenEvolve/CycleQD の on-prem 文化版」に留まる.

---

## 6. References

### Generator (G)
- Romera-Paredes, B. et al. (2024). [Mathematical discoveries from program search with LLMs (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6). *Nature*.
- Novikov, A. et al. (2025). [AlphaEvolve: A coding agent for scientific and algorithmic discovery](https://arxiv.org/abs/2506.13131). arXiv:2506.13131. ([DeepMind blog](https://deepmind.google/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/))
- Lehman, J. et al. (2022). [Evolution through Large Models (ELM)](https://arxiv.org/abs/2206.08896). arXiv:2206.08896. (OpenAI)
- Real, E. & Liang, C. et al. (2020). [AutoML-Zero: Evolving ML Algorithms From Scratch](https://arxiv.org/abs/2003.03384). ICML 2020.
- Stanley, K. & Miikkulainen, R. (2002). NEAT; Stanley et al. (2009). [HyperNEAT](https://en.wikipedia.org/wiki/HyperNEAT).
- Hu, S., Lu, C., Clune, J. (2024). [Automated Design of Agentic Systems (ADAS / Meta Agent Search)](https://arxiv.org/abs/2408.08435). ICLR 2025.
- Guo, Q. et al. (2023). [EvoPrompt](https://arxiv.org/abs/2309.08532). (Microsoft)
- Ma, Y. et al. (2023). [Eureka: Human-Level Reward Design via Coding LLMs](https://arxiv.org/abs/2310.12931). (NVIDIA)

### Recursive self-improver (R)
- Hu, J. et al. (2025). [Darwin Gödel Machine: Open-Ended Evolution of Self-Improving Agents](https://arxiv.org/abs/2505.22954). (Sakana/UBC/Vector; [code](https://github.com/jennyzzt/dgm))
- Yin, X. et al. (2024). [Gödel Agent: A Self-Referential Agent Framework for Recursive Self-Improvement](https://arxiv.org/abs/2410.04444).
- Zelikman, E. et al. (2023). [STOP: Self-Taught Optimizer (Recursively Self-Improving Code Generation)](https://arxiv.org/abs/2310.02304). (MSR)
- Yuan, W. et al. (2024). [Self-Rewarding Language Models](https://arxiv.org/abs/2401.10020). (Meta) + [Meta-Rewarding LMs](https://arxiv.org/abs/2407.19594).
- Fernando, C. et al. (2023). [Promptbreeder: Self-Referential Self-Improvement](https://arxiv.org/abs/2309.16797). (DeepMind)
- Lu, C. et al. (2024). [The AI Scientist: Towards Fully Automated Open-Ended Scientific Discovery](https://arxiv.org/abs/2408.06292). (Sakana) + [v2](https://arxiv.org/abs/2504.08066).

### Open-ended (O)
- Wang, R. et al. (2019). [POET](https://arxiv.org/abs/1901.01753) + (2020) [Enhanced POET](https://arxiv.org/abs/2003.08536). (Uber AI)
- Zhang, J. et al. (2023). [OMNI](https://arxiv.org/abs/2306.01711) + Faldor, M. et al. (2024). [OMNI-EPIC](https://arxiv.org/abs/2405.15568). (ICLR 2025)
- Wang, G. et al. (2023). [Voyager: An Open-Ended Embodied Agent with LLMs](https://arxiv.org/abs/2305.16291). (NVIDIA/Caltech)
- Clune, J. (2019). [AI-GAs: AI-generating algorithms](https://arxiv.org/abs/1905.10985).
- Khan, A. et al. (2024). [CycleQD: Agent Skill Acquisition for LLMs via Quality Diversity](https://arxiv.org/abs/2410.14735). (Sakana)

### on-prem 再現 (feasibility 根拠)
- [OpenEvolve](https://github.com/algorithmicsuperintelligence/openevolve) — AlphaEvolve OSS 実装 (Ollama/vLLM 対応). [PyPI](https://pypi.org/project/openevolve/).
- [CodeEvolve](https://arxiv.org/abs/2510.14150) — OSS evolutionary coding agent.

### FullSense 内部 cross-reference
- [[OPEN_ENDED_CULTURAL_EVOLUTION]] (13 原理) / [[evolution_fitness_redesign_2026_05_25]] (診断・失敗観測)
- [[llm_evolutionary_prior_art]] (LLM×EA 最適化 P/O/S/M, 本 doc と相補)
- 並列 stream: [[evolution_research_meta_2026_05_25]] / [[evolution_research_openendedness_2026_05_25]] / [[evolution_research_representation_selection_2026_05_25]] / [[evolution_research_culture_learning_2026_05_25]] / [[evolution_research_safety_2026_05_25]]

### maintainer memory
- [[feedback_benchmark_honest_disclosure]] — 異常に良い結果は内訳を疑う
- [[feedback_llive_measurement_purity]] — on-prem only の測定純度
- [[feedback_originality_over_imitation]] — 網羅でなく選別, 単なる模倣は排除

## 7. 次アクション
- [ ] §3.2 反証条件 (a)〜(e) を **要件定義の falsifiable 受入基準** に昇格
- [ ] §4 HIGH 3 件 (island/archive, 2 段 LLM ensemble, 文化版 interestingness) を Stage2/3 設計に注入
- [ ] OpenEvolve を 1 回 ollama で実走させ「on-prem loop 再現可」を実測で pin (feasibility 証跡)
- [ ] CycleQD の QD-merge を Stage6 (実 LLM) の拡張候補として要件登録
