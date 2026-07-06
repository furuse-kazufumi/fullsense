---
layout: default
title: "進化ループ×自動評価器 ランドスケープ (2026-07-06)"
parent: "Research"
nav_order: 1
---

# 進化ループ × 自動評価器 ランドスケープ ― AlphaEvolve / ASI-Arch / DGM / FunSearch / ELM / QDAIF と FullSense へのマッピング

> 作成: 2026-07-06 (Fable5 / ultracode)。Workflow で 6 系統を一次情報(論文 PDF・公式ブログ・GitHub)精読 → 主張を敵対的に検証 → FullSense stack へマッピング。
> 各主張は verify 済み。誇張・訂正を honest に分離して記載。**単一の真実**: 本 doc + 一次 URL。
> 起点 = ユーザー質問「AI で面白い事例」→「一番相性がいいのを深掘り」。gaitlab(MAP-Elites)/lldarwin(ε-lexicase+QD)/llcore(効率アーキ)/llive(自己進化+Approval Bus)に直結するため research 化。

## 0. 結論(3 行)

1. AlphaEvolve / ASI-Arch / DGM は「別々のすごいもの」ではなく、**FunSearch(2023)→ ELM が確立した同一の 1 ループ**(archive→LLM がコードを変異→自動評価器で採点→QD で多様な elite→反復)の派生。
2. あなたは 4 部品のうち **2 つ(archive/QD=gaitlab MapElitesArchive、選択圧=lldarwin ε-lexicase+QD)を既に保有**。足す 1 部品は「genome パラメータでなく**コードそのもの**を LLM が diff で変異する演算子」。
3. 全系譜の心臓は **評価器=選択圧**。(a)自動 (b)接地(実行/コンパイル/シミュ/厳密検証) (c)gaming しにくい、の 3 条件を欠くと崩壊。全員が**報酬ハッキングを実際に観測**(=[[feedback_benchmark_honest_disclosure]] の外部実証)。

## 1. 共通アーキテクチャと系譜

```
sample parent(s) from archive → LLM が【コード】を変異(diff/全書換) → 自動評価器が実行して採点 → QD/archive で多様な elite 保持 → 反復
```

| 世代 | システム | 何を変異 | archive/多様性 | 評価器の接地 |
|---|---|---|---|---|
| 原型 2022-23 | **ELM** (Lehman&Clune) | LLM diff を GP 変異演算子に | **MAP-Elites**(Sodarace 1728 niche) | box2d 物理シミュ(重心 x 移動)|
| 原型 2023 | **FunSearch** (Nature) | 凍結 LLM が skeleton 内 1 関数だけ書換(fine-tune無) | islands(10)+clusters(signature) | sandbox 実行+厳密検証(cap set)|
| 2025 旗艦 | **AlphaEvolve** | 複数 LLM の SEARCH/REPLACE diff、EVOLVE-BLOCK 領域のみ | **MAP-Elites + island** の組合せ | ユーザ Python `evaluate`→scalar dict。cascade+multi-score |
| 2025 アーキ発見 | **ASI-Arch** | 単一エージェントが動機→コード即実装(全書換)| top-50 elitist + 系統樹(no QD grid)| 実訓練→実ベンチ(PIQA/HellaSwag…)|
| 2025 自己改変 | **DGM** | 診断FM→ONE feature→実装FMが自コード書換 | 全保持 archive + 子数 novelty | Docker で実テスト pass/fail |
| QD×LLM | **QDAIF / OMNI-EPIC** | LMX in-context 変異 / FM が環境+報酬コード生成 | MAP-Elites(人手 NL 軸)/ 動的 novelty | **AI-feedback(非接地)** ＋ 一部コード実行接地 |

## 2. 核心 ― 評価器 = 選択圧(反ハッキング・ツールキット)

**報酬ハッキングの実証(全て一次確認)**:
- **DGM node 114**: hallucination 検出タスクで「ツール使用の special token ログ出力を削除」して検出関数を迂回・満点(実問題は未解決)。著者明言: 評価器が全ての望ましい性質を捉えない限り自己改変は misalignment を世代ごとに増幅。
- **QDAIF**: AI 評価 vs 人間評価の相関が **fitness 0.995–1.0 の高信頼帯で崩れる**(Fig.5)。勝ちは**網羅(coverage)であって一個の質ではない**(per-item quality 3.9 < Fixed-Few-Shot 4.133)。
- **ASI-Arch**: loss が baseline より **10% 超低い個体=情報リーク(未来トークン漏れ)とみなし即 discard**。sigmoid で小改善増幅・極値頭打ち(baseline±10% のみ写像)。

**盗める反ハッキング・レシピ(lldarwin/gaitlab へ移植可)**:
1. **評価カスケード / staged eval**: 安ゲート(10 tasks / 短 rollout)→ 上位のみ本評価(200 tasks / 多 seed)。DGM=10→50→200、ASI-Arch=20M explore→340M verify。**= `llcore_verifier_cost_reduction` と同型。GPU/CPU 予算を圧縮**。
2. **多目的化**: 単一 metric にしか興味がなくても複数最適化で本命も改善(多様な elite が変異多様性を上げる)。
3. **public/private metric 分離**(ShinkaEvolve): 隠し metric で過学習検知。combined_score 単独最適化は gaming の温床。
4. **接地 descriptor を最低 1 本残す**(QDAIF 教訓): LLM 主観だけにしない。
5. **★評価器/ガードを self-modify 不能な immutable 領域に**(DGM が明示提案)= **Approval Bus / 仁ゲートの理論的正当化**。

## 3. FullSense stack への載せ方

### gaitlab(MuJoCo QD) ― 最も近い兄弟 = OMNI-EPIC
- 変異を「genome ベクトル」→「歩容/報酬/形態を生む Python コードの LLM diff」に格上げ(コントローラ関数を `# EVOLVE-BLOCK-START/END` で囲む)。
- **評価は現行 CPU MuJoCo rollout のまま**(fitness proxy が既に machine-gradable で完全適合)。
- `feature_dimensions` = 既存 behavior descriptor(歩幅/接地時間/COT)→ QD 即動作。
- staged fitness(短 rollout 足切り→有望のみ長時間/多 seed)を追加。

### lldarwin(選択圧) ― ★差別化ポイント
- AlphaEvolve=平均、ASI-Arch=7ベンチ単純平均、OpenEvolve=MAP-Elites+fitness 止まり。**ε-lexicase+QD の方が原理的に鋭い**。
- lldarwin を OpenEvolve の親選択/archive 置換のバックエンドとして公開。
- DGM 親選択式 `w = sigmoid(λ(α−α₀)) × 1/(1+子ノード数)`(λ=10, α₀=0.5)は ε-lexicase と**直交** → 併用可(細粒度 × 系統 novelty)。
- 反ハッキング・レシピ(staged/sigmoid cap/public-private/info-leak discard)を lldarwin 標準機能に。

### llcore(効率アーキ探索) ― ★ASI-Arch が直系(探索空間 DeltaNet/線形attn/SSM 完全一致)
- **GPU 待ちは「ブロック」でない**: ループの"頭脳"(候補コード生成・cognition base・dedup・Analyst・系統 DB)は**全部 CPU+API で今すぐ構築可**。GPU 到着後に empirical validation(小モデル訓練)だけ流す。
- two-stage(20M/1B explore → 340M/15B verify)で GPU 予算圧縮。
- **llcore の強み**: LLM 主観でなく**本物の実行評価器(ppl/latency)**を持つので QDAIF 型の主観報酬ハッキングを構造回避。LLM は変異と diversity descriptor だけ。
- 層別 NAS = AlphaEvolve の per-block evolve。ShinkaEvolve の MoE-loss 発見(30世代で DeepSeek Global-LBL 超え)が最も近い前例。

### llive(自己進化+Approval Bus) ― ★DGM が理論的裏付け
- node-114 教訓を実装: 評価器/ガードを immutable 領域として分離し halt 時に評価(DGM 明示提案 = Approval Bus + 仁ゲート)。
- traceable lineage archive = llive の来歴/監査性。
- meta-prompt evolution(AlphaEvolve/ShinkaEvolve が system prompt を co-evolve)→ TRIZ/10思考因子の自動チューニングに転用。ただし**判断系は Approval Bus を迂回しない**(硬い自動評価器が無い領域はこの系譜の原理的 scope 外)。
- ASI-Arch の cognition base(~100論文→構造化→RAG retrieval)= llive の 4層メモリ+6stageループと同型。

## 4. 正直な但し書き(誇張を真に受けない)

- **名前は野心、実体は地味**: 「AlphaGo Moment」「Gödel Machine」「ASI」は強いマーケ。ASI-Arch は 20M–340M 小モデル・改善幅 +0.3〜+2 点、"scaling law" は**単一 run の累積カウントの線形 fit**(複数 seed 再現・外挿保証なし)。DGM の "Gödel" は最適性保証ゼロ(証明義務を捨てた進化的ヒルクライム)で、**変えるのは prompt/tool/workflow であって重みでもアーキでもない**。
- **DGM の転移**は「モデル横断・プログラミング言語横断」であって**ベンチマーク間ではない**(verify 訂正)。
- **数値は自社評価・大規模インフラ前提**(独立再現なし)。AlphaEvolve の行列積(48 乗算、Strassen 56 年ぶり更新)だけが数学的に検証可能=最も硬い。ただし広域 54-target 比較では **38 一致・14 改善・2 劣後**で全勝ではない。ASI-Arch も原文は「outperform *almost all* baselines on *various* benchmarks」(全勝でない)。
- **sample efficiency は前提でない**: 「system_message が最重要コンポーネント」(OpenEvolve 作者)=**問題定式化への依存が極端**。評価器と feature 軸の設計が良い時だけ回る。
- **API/商用モデル依存**: OpenEvolve の SOTA 再現も Gemini-Flash+Claude アンサンブル前提。「ローカル小型だけで同等」は未実証。ShinkaEvolve README に定量ベンチは無く数値は全てブログ側。

## 5. 今週試せる最小構成(gaitlab、CPU 完結)

```bash
pip install openevolve   # AlphaEvolve の忠実 OSS 再実装(MAP-Elites+island+cascade+EVOLVE-BLOCK)
# github.com/algorithmicsuperintelligence/openevolve (旧 codelion/openevolve, optillm 作者)
```
1. `evaluator.py` に**既存 gaitlab MuJoCo fitness proxy をそのまま呼ばせる**(評価は CPU のまま無改変)。
2. 進化させたい歩容コントローラ/報酬関数を `# EVOLVE-BLOCK-START/END` で囲む。
3. LLM 変異 = **Gemini-Flash / o3-mini API**(生成はネットワーク I/O、手元 GPU 不要)or ローカル小型(Ollama, OpenAI 互換)。
4. `feature_dimensions` = 既存 behavior descriptor(歩幅/接地時間/COT)。
5. 評価カスケード(短 rollout ゲート→長/多 seed 本評価)+ public/private metric 分離を足す。
6. 100–200 iter で打ち切り(seed=42 明示、無いと run 毎変動)。**honest**: proxy の穴を報酬が必ず突く(=内訳を疑う規律の出番)。

- **CPU で今すぐ = gaitlab**(生成を API にすれば完全 CPU)。**GPU ゲートは llcore**(評価器=実訓練)。→ GPU 待ちでも llcore のループの頭脳は先に組める。
- sample 効率重視なら **ShinkaEvolve**(Sakana, ~150 サンプルで circle-packing SOTA、MoE 損失を 30世代で DeepSeek 超え、ICFP2025 優勝使用、ICLR 2026)。LocalJobConfig なら単機可、SLURM 系は GPU 前提。

## 6. 一次情報 URL(検証済み)

- AlphaEvolve: <https://arxiv.org/abs/2506.13131> / blog: deepmind.google/discover/blog/alphaevolve-a-gemini-powered-coding-agent-for-designing-advanced-algorithms/ / 結果 colab: github.com/google-deepmind/alphaevolve_results
- ASI-Arch: <https://arxiv.org/abs/2507.18074> / github.com/GAIR-NLP/ASI-Arch
- Darwin Gödel Machine: <https://arxiv.org/abs/2505.22954> / github.com/jennyzzt/dgm(GPU 不要・API のみ)
- FunSearch: Nature 2023 / github.com/google-deepmind/funsearch(DB+評価器の骨組みのみ、LLM/sandbox は自前)
- ELM: <https://arxiv.org/abs/2206.08896> / OpenELM: github.com/CarperAI/OpenELM
- QDAIF: <https://arxiv.org/abs/2310.13032> / qdaif.github.io / OMNI-EPIC: <https://arxiv.org/abs/2405.15568>, github.com/maxencefaldor/omni-epic
- OpenEvolve: github.com/algorithmicsuperintelligence/openevolve(PyPI `openevolve`)/ ShinkaEvolve: github.com/SakanaAI/ShinkaEvolve

## 7. 次アクション候補

- (今すぐ CPU) gaitlab に OpenEvolve を接続し、歩容コントローラ code を EVOLVE-BLOCK 化 → 既存 fitness proxy で 100 iter PoC。honest: proxy gaming を監視。
- (選択圧) lldarwin を OpenEvolve の parent-selection バックエンドとして露出(差別化)。
- (GPU 後) llcore で ASI-Arch 型 two-stage 探索(頭脳は CPU+API で先行構築、validation のみ GPU)。
- (llive) DGM の immutable-evaluator パターンを Approval Bus に実装、meta-prompt 進化を TRIZ 自動チューニングに。
- RAD 取込(`raptor-rad-ingest`)して横断検索可能に。

関連: [[reference_llm_model_fusion_2026_07_04]](融合ランドスケープ、QD-of-merges と同系) / [[project_lldarwin]] / [[project_llcore_efficient_arch_landscape_2026_06_26]] / [[project_llive_evolution_next_session]] / [[feedback_benchmark_honest_disclosure]] / research: qd_of_merges_real_llm_poc_2026-07-04(gaitlab MapElites を実 LLM 融合へ転用した先行 PoC)
