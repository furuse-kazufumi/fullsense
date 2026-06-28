# 蒸留プロトコル + llcore 差別化テーゼ統合 — 2026-06-28

> **目的**: 4 本の deep investigation(①HALO novelty 侵食検証 ②蒸留プロトコル T3 ③差別化テーゼ T5 ④純定数状態ニッチ実在性)を 1 枚に統合し、llcore(Qwen2.5 0.5B/1.5B 線形化、採用 = LoLCATs path、北極星 = メモリ効率の定数状態)の **(1)層別 NAS novelty の生死 (2)実装可能粒度の蒸留プロトコル (3)defensible 差別化テーゼ 1-2 本 (4)純定数状態ニッチの実在性 (5)未確認事項** を確定する。
> **接続先**: T2 `linearization_recipes_2026-06-28.md` / T4 `efficient_arch_landscape_refresh_2026-06-28.md` / memory `project_llcore_efficient_arch_landscape_2026_06_26` / `project_fullsense_unified_model_vision` / prereg `preregistration/prereg_linearization_distill.md` / 実装 `D:/projects/llcore/src/llcore/runtime/distill.py` ・ `lm/ttt.py`。
> **規律**(`feedback_benchmark_honest_disclosure` / `feedback_verify_existence_before_claiming`): 主張に確信度と出典を付す。誇張禁止、未確認は「未確認」と明記。

---

## 0. 本統合セッションで一次確認した範囲(検証台帳)

| 主張 | 出典 | 検証レベル | 確信度 |
|---|---|---|---|
| HALO 論文 title = "Hybrid Linear Attention Done Right: Efficient Distillation and Effective Architectures for Extremely Long Contexts" / **HALO = "Hybrid Attention via Layer Optimization" は pipeline の acronym 正式展開**(両立)/ Qwen3→HypeNet、**2.3B tokens(<0.01%)**、hybrid(softmax+RNN)=非定数 | 2601.22156 abstract | **本統合が arXiv MCP abstract 独立確認** | 高 |
| HALO 層選択機構 = recall/CSR 比の単層 ablation importance + Top-k(k=⌊L/4⌋=25% softmax 固定)= 単一パス貪欲・非定数 | 2601.22156 §4.3 | **INVESTIGATE 1/3 が本文 HTML 確認(本統合は abstract まで)** | 中-高(機構は investigations 由来) |
| Hedgehog 蒸留損失 = per-query soft-CE / MOHAWK 3 段損失 + 予算 80M/160M/2.76B(92% e2e) | 2402.04347 / 2408.10189 | INVESTIGATE 2 本文確認 | 高 |
| additive→不可逆 state saturation / gated∧delta 連言必須 / state 解像度 > 蒸留 budget | 2504.14366 | T2/T4 本文照合(継承) | 高 |
| Falcon Mamba pure: MMLU 62.11 / avg 64.09(data-parity の MMLU 罰則 ~2-4pt)/ 長文脈 recall は 8-16k で cliff | 2410.05355 / 2406.07887 / 2410.07145 | INVESTIGATE 4(HF blog + arXiv) | 高 |

**他の機構詳細**(Jet-Nemotron PostNAS / STAR / Gated DeltaNet-2 / RWKV-7 cliff 等)は各 investigation の検証レベルを継承し、本文中に確信度を明記する。

---

## 1. ★HALO novelty verdict — llcore 層別 NAS の生死

### 1.1 結論一文
llcore 現行 novelty 文言「**memetic NAS による層別 線形化-vs-温存 を探索(固定ヒューリスティックでなく)**」は、**現行のまま研究 novelty として死亡。確信度: 高**。理由は HALO 単体でなく「**層別 線形化の選択**」が 2025 年半ばに成立した**混雑サブ分野**全体に包括的に先取りされているため。生存は「**温存 softmax ゼロ = KV 完全定数の制約下**で、長文脈 recall を明示 Pareto 目的に置いた多目的・異質層別探索」へ **狭めた場合のみ**。

### 1.2 HALO は「固定」か「探索」か — 正確には「データ駆動の単一パス貪欲選択」
INVESTIGATE 1 と 3 の用語の食い違い(1=「探索」/3=「探索でない」)を機構レベルで一致させると:

- HALO の層配置 = 各 attention 層を RNN 化した `M^(i)` の **recall 低下 ÷ CSR 低下** で importance `s_i` を**一度だけ**算定 → `Top-k(s_i), k=⌊L/4⌋`(25% softmax 固定)。
- これは **(a) 固定位置ヒューリスティックでは「ない」**(データ駆動で「どの層か」を選ぶ)が、**(b) NAS でも進化探索でも多目的 Pareto でも「ない」**(単一スカラ・単一パス・貪欲・比率固定・機構は softmax/RNN の二択)。
- → 結論: 「**層別線形化を固定でなく選ぶ**」という素の主張は HALO が既に実装済 = **死亡**。しかし「**多目的・進化的に探索する**」「**定数制約下で**」までは HALO 単体は占めていない。

### 1.3 ★本丸 — 「層選択」は確立サブ分野(HALO 単体より広く先取り)

| 手法 | 時期 | 層選択機構 | 定数性 |
|---|---|---|---|
| Mamba-in-Llama 2408.15237 | 2024-08 | simple selection scheme | 非定数(attn 残置) |
| SMART (Yang 2026) | 2025-05 | output distribution shift importance | 非定数 |
| RAD (Hoshino 2025) | 2025-05 | redundancy metric | 非定数 |
| **Jet-Nemotron / PostNAS 2508.15884 (NVIDIA, Song Han/Han Cai)** | 2025-08 | **明示的 NAS**: full-attn 層配置の学習 + linear block selection | 非定数 |
| KL-LS (Li 2025) | 2025-12 | KL-divergence + 全層 re-distill 探索 | 非定数 |
| HALO 2601.22156 (THUNLP) | 2026-01 | recall/CSR ratio Top-k(貪欲) | 非定数(25% softmax) |
| **STAR (Liquid AI)** | — | **進化探索**(attn/linear/conv/SSM operator の striped hybrid genome、KV を cost proxy) | 非定数 |

- **Jet-Nemotron PostNAS(確信度: 高=abstract 独立確認は未、INVESTIGATE 1 の abstract 確認継承=中-高)** が決定打: *"learning optimal full-attention layer placement and elimination" + "linear attention block selection"* を**そのまま NAS**で実施、*"Strategic attention layer placement outperforms uniform distribution."* → 「**NAS で層配置 + ブロック選択**」キーワードを占有済。
- **STAR(確信度: 中=web 要約)** が「**memetic/進化**」部分を占有: hybrid genome の進化的探索。
- → load-bearing な 3 キーワード(**層別 / 探索 / NAS・進化**)それぞれに直接先行があり、**素の組み合わせに空白がない**。T4 の「HALO が名称衝突」警告は過小評価で、実態は「**サブ分野が成立済み**」。

### 1.4 侵食しないもの(scope 限定)
- **MoH 2410.11842** は per-head × per-token のソフトルーティング(head を expert 化)= 「per-layer 線形化-vs-温存」とは別問題(確信度: 高、abstract 確認)。侵食しない。
- 上記サブ分野は**全員が非定数(softmax/SWA 残置 → KV 線形増)**。これが §3 の生存路の鍵。

### 1.5 残る差別化の余地(narrow・honest)
死んだのは**裸の「層別探索」**。先行が全員占めていない次元のみ生存:

- **★A(最有力)= 完全定数状態(KV 非増加・温存 softmax ゼロ)制約下の異質層別探索**。先行は全員 ~25% softmax 温存 = 定数でない。「温存層ゼロ / KV 完全定数」を hard 制約に課した heterogeneous 層別 mixer 探索は無人(T4 白地 #1 と一致、確信度: 中-高、absence-of-evidence 留保)。
- **B = 多目的 Pareto(5-shot MMLU × 長文脈 recall × 機械検証したメモリ定数性)**。HALO は単一スカラ Top-k、STAR は quality+KV proxy。「**メモリ定数性を明示目的**に入れた 3 軸 Pareto」は弱差別化(incremental)。
- **C(弱)= 機構 allele を検証済みラダーに接地**(additive < gated-delta < Gated DeltaNet-2 < TTT-Linear, 2504.14366 準拠)。STAR/Jet-Nemotron も block 型を探索済 → 探索空間の質改善で novel な探索問題ではない。
- **D(弱)= 比率も同時探索**。HALO は 25% 固定だが Jet-Nemotron の placement/elimination が実質 count も探索 → 部分被り。

### 1.6 ★binding な honest 警告(novelty 文言の書き換え必須)
1. 生存路 = **A(定数制約)∩ B(多目的)の交点のみ**。文言を「memetic NAS で層別線形化を探索」**ではなく**「**完全定数状態(温存 softmax ゼロ・KV 非増加)制約下で、長文脈 recall を明示 Pareto 目的に置いた heterogeneous 層別 mixer 探索**」へ書き換える。
2. **貪欲 baseline を上回る実証が必須**: HALO の教訓 = 貪欲 importance ランキングは安価で competitive。memetic 探索機構を正当化するには「貪欲 LOO/Top-k(=HALO 流)を実測で上回る(=層間相互作用の捕捉が効く)」ことが必須。示せなければ探索機構自体が冗長。
3. **自明解再発見のリスク**: 完全定数を強制すると additive の state 解像度天井(2504.14366)に当たり、探索が「全層 gated-delta + 一部 SWA」に収束しうる。それは既存 gated-delta+SWA 文献の含意 → A の生存は「**定数制約下でも層別異質性が均一配置を有意に上回る**」ことの実証に懸かる。**支配できなければ honest null**(=「定数制約下では層探索は均一 gated-delta に勝てない」)も公表価値ある負の結果。

---

## 2. llcore 蒸留プロトコル(LoLCATs path に積む・実装可能粒度)

### 2.1 5 蒸留目的の粒度ラダー(一次情報ベース)
下に行くほど (a)結合度↑(per-layer→joint)(b)コスト↑(c)層間誤差累積の補正力↑。

| # | 目的 | ターゲット | 損失 | 結合 | コスト | 何を直す/直さない | 出典 | 確信度 |
|---|---|---|---|---|---|---|---|---|
| **O1** | feature-map 出力 MSE(現 llcore Step1) | attention sub-layer 出力 | `MSE(attn_S, attn_T)` | per-layer 独立 | 最安(CPU 可) | 出力値は合うが注意機構(spiky/単調)は無保証 → 後段 finetune と勾配衝突しうる(Hedgehog 核心指摘)。長文脈/分布シフトに脆弱 | LoLCATs Step1 / 現 distill.py | 高 |
| **O2** | 注意分布 CE(Hedgehog) | softmax 注意重み `A_T`(soft target) | per-query soft-CE `−Σⱼ softmax(qᵢ·kⱼ)·log[φ(qᵢ)·φ(kⱼ)/Σₘφ(qᵢ)·φ(kₘ)]` | per-layer 独立 | 中(O(T²) 注意行列 materialize、因果マスク要) | 出力値でなく注意機構を移植(spiky+単調を強制)→ joint 段の収束改善。finetuned-conversion で 99% 回復 | 2402.04347 | 高(式)/ llcore 効果=未測 |
| **O3** | hidden-state alignment(MOHAWK St2) | block 出力 hidden(attn+MLP+residual 後) | `‖block_S − block_T‖₂`、入力=teacher 前段出力 | per-block 独立 | 中(全 block forward) | 次層が消費する表現を合わせる(O1 より richer)。block 内累積は補正、層間累積は未補正 | 2408.10189 | 高 |
| **O4** | logit-KD | teacher 最終 logit(温度 τ) | `KL(softmax(z_T/τ)‖softmax(z_S/τ))` | joint/e2e | 高(全 forward+backprop, GPU) | 最終出力分布を直接最適化、層間誤差累積を補正。per-layer 分解不能 | MOHAWK St3 / MIL KL | 高 |
| **O5** | end-to-end CE(+LoRA) | 正解 next-token(hard) | `CE(z_S, y)`、projection に LoRA | joint/e2e | 高(GPU) | 最終回復。LoLCATs の MMLU +20pt の主因。O4 併用可 `λ·KD+(1−λ)·CE` | LoLCATs St2 / Liger | 高 |

**★最重要の一次事実(採否を縛る)**: MOHAWK の段別予算 = **80M / 160M / 2.76B**(3B 中 **92% が e2e**)。per-component+per-block(O1/O2/O3)は全予算の **8%**、残り 92 % が e2e(O4/O5)。→ **per-layer 蒸留は warm-start であって回復本体ではない**。T2/T4 の「per-layer 独立 ≠ joint(誤差累積)」を予算面から裏づける一次証拠。

### 2.2 段階プロトコル D0→D5(現 distill.py に何を足すか)
llcore 現状 = O1 実装済(`distill_layer`/`distill_all_layers`、出力 MSE、projection 凍結、各層を pristine softmax から独立蒸留)。

| 段 | 内容 | 損失 | 対象層 | データ量(0.5-1.5B 想定) | llcore 実装点 | 確信度 |
|---|---|---|---|---|---|---|
| **D0(済)** | NAS 探索用の安価 warm-start | O1 出力 MSE | 全候補層を独立蒸留 | ~512 tok×数百 step/層 | `distill_all_layers`(現状) | 高 |
| **D1** | 選定 genome の per-layer warm-start を O2 へ昇格 | 注意分布 CE(Hedgehog) | NAS が線形化を選んだ層のみ(温存層は触らない) | calib 512–1024、~数十 step/層 | `distill.py` に `attn_ce_loss` 追加。`_capture_layer_io` を拡張し teacher の**注意重み行列**も hook(現状は出力のみ)。`feature_map="full"` と組む | 高(式)/ llcore 効果=中 |
| **D2(任意)** | block-hidden 整合(richer warm-start) | O3 `‖block_S−block_T‖₂` | 同上 | ~160M 級(MOHAWK 比) | `distill_block` 新関数(full block forward hook) | 高 |
| **D3** | joint 化①: logit-KD | O4 `KL(z_T‖z_S)/τ` | 全線形化層を同時 install、全モデル forward | ~数十M–百M tok, GPU | `distill_joint` 新関数(`feature_parameters()` 全層同時最適化) | 高 |
| **D4** | joint 化②: LoRA Step2 + next-token CE | O5 `λ·KD+(1−λ)·CE`、LoRA r=8 | 同 joint | LoLCATs 基準 ~40M tok(Liger は 20M で 93%) | projection に LoRA を載せ学習対象に追加(現 `feature_parameters()` のみ) | 高 |
| **D5(長文脈アーム)** | mixer を gated-delta へ routing(蒸留でなく機構変更) | 同 D1–D4 ラダーを gated-delta セルに適用 | 長文脈 recall 要件層 | 同上 | `ttt.py` 忠実 Gated DeltaNet セル(実装済)/ **Gated DeltaNet-2 型(erase/write 分離, 2605.22791)**を NAS allele に。RoPE は別アーム(保持 vs 除去) | 機構=高 / llcore 実装=未着手 |

**順序の根拠**: ① MOHAWK の粗→密 単調昇格(行列→hidden→logit)。② **安価段で探索・高価段で本回復** = NAS は数百 genome を回すので **O(T²) の O2 を NAS fitness に wire しない**(prereg §5-6 整合)。O2 は **選定済み 1 genome の per-layer warm-start にのみ**使う。
**どの層に**: `linearize_tolerance.py` の zero-shot Δnll プロファイルで層をランク → NAS が線形化を選んだ層だけ蒸留、温存層は対象外。長文脈要件層は D5 へ routing。

### 2.3 ★per-layer → joint 昇格条件(定量トリガ、既存ハーネスで測定可)
`distill_all_layers` は各層を pristine softmax 前提で蒸留 → 全 student 同時 install すると入力分布シフトで誤差が深さ方向に累積(exposure-bias 構造)。

- `ε_indep` = Σ_i(層 i だけ install した held-out Δnll)= 独立予測の和
- `ε_joint` = 選定層を全同時 install した held-out Δnll(`reeval_frontier` で算出)
- **累積ギャップ `G = ε_joint − ε_indep`**
- **判定**: `G` が選択 CI を超える(または `G > ε_indep`)なら **D3/D4 の joint 段が必須**。CI 内なら per-layer warm-start のみで可。
- **事前予測(honest)**: MOHAWK は 4 層置換でも予算 92% を e2e に投じる → llcore の射程(多数層線形化)では **G は大きく出る公算が高く joint は事実上必須**。per-layer-only frontier は「warm-start 品質の下界」として報告し、回復済みモデルと読み替えない(確信度: 機構=高、llcore 実測=未測)。

### 2.4 held-out eval プロトコル(3 軸分離・短文脈 ppl で判断しない)
- **軸A 短中文脈品質(主軸+winner's curse 管理)**: disjoint holdout の next-token Δnll、`--context-sweep 256,512,1024,2048`。headline は選択窓でなく `delta_nll_heldout` + `optimism_gap`(2000 bootstrap paired)。短窓改善を「回復」と呼ばない。
- **軸B 長文脈 recall(独立 honest gate)**: S-NIAH / passkey / MQAR を 1k/2k/4k/8k。**2504.14366 の binding constraint**: additive `LinearAttention(diag/full)` は全長 NIAH≈0%、gap は scale で広がる(14%@140M→20%@1.7B、**0.5-1.5B は実測範囲内**)。軸A PASS でも軸B は別 verdict。長文脈クレームは **D5(gated-delta)アーム + 軸B 実測でのみ**。
- **軸C 定数性の純度(llcore 差別化軸、副次)**: 3:1 hybrid は full 層残で KV 線形増 = 定数でない。llcore は state が増えないことを context-sweep × needle と並べて計測軸化(温存 SWA 残層を入れた場合も「定数だが天井あり」を正直開示)。

---

## 3. ★差別化テーゼ(defensible・検証実験つき)

### 3.1 軸 A(主)— 定数状態純度を hard 制約にした層別多目的 Pareto 探索(CSC-NAS)
**TRIZ 矛盾(発見)**: 「長文脈 recall を上げる」と「メモリ定数性=footprint」が両立しない。業界の解(Qwen3.5/Kimi/HALO)は全員 full-softmax 層を残置して**定数性を犠牲**(KV 線形増)。彼らの最適点は**定数状態多様体の外**にある。

**主張**: llcore は探索空間を「**全層が定数状態 mixer**」に閉じる(pure-linear / full feature-map / 忠実 Gated DeltaNet / **Gated DeltaNet-2 型 erase-write 分離 2605.22791** / WindowLinearAttention=有界窓 SWA / Conv1D+正規化 GLA=LAWCAT)。**unbounded-KV な softmax 層を allele から禁止**し、目的 = {5-shot MMLU, S-NIAH/RULER@{1k,2k,4k,8k}, **機械検証した厳密メモリ定数性(peak KV bytes が文脈長で平坦)**} の memetic 多目的 Pareto(既実装 `evolve_linearization.py`/`nas_pareto.py` 基盤)。**成果物は単一モデルでなく「定数状態多様体内の最良 Pareto 前線 = 正直な cliff 地図」**。

**なぜ先行に潰されないか**(§1 一次根拠つき): HALO=単一パス貪欲・固定 k=L/4・非定数 / Qwen3.5・Kimi=固定均等 3:1・KV 増 / Jet-Nemotron・STAR=「attn を残す hybrid」を出力(非定数)/ RWKV-7=真定数だが Qwen 由来でも層別探索でもない別系譜。→ **「Qwen 由来 × 厳密定数 × 多目的層別探索」の交点は無人**(確信度: 白地存在=中-高)。インフラだから陳腐化しにくい(新 cell が出ても allele として吸収)。

**検証実験**(compute-matched・held-out・honest):
1. **非定数性の暴露**: HALO importance s_i と Qwen3.5 流均等 3:1 を再実装し、(a)原版(softmax 残置)と (b)残置を有界窓 SWA に強制置換した定数版を同 compute 比較 → 「3:1 は定数でない/定数化するといくら落ちるか」を一次数値化。
2. **本探索**: 上記 allele で memetic 多目的 NAS、hard 制約 = unbounded-KV 層ゼロ。
3. **固定ヒューリスティック ablation**: 探索前線 vs {全層 gated-delta 均等 / HALO-importance を定数版に / Liger 均等 SWA}。**反証可能な主張**: 探索前線が (MMLU × recall) で固定ヒューリスティックを Pareto 支配するか。支配しなければ **honest null = 「定数制約下では層探索は均一 gated-delta に勝てない」**(公表価値ある負の結果)。
4. **cliff 開示を headline 化**: context-sweep × needle の cliff 位置を主成果に(単一回復率を headline にしない)。2504.14366 通り cliff は必ず出る → 各定数 mixer 族で 0.5-1.5B の cliff が**どこか**を地図化すること自体が貢献。
5. **winner's curse**: 前線選択は max-of-N → held-out 再評価 + `optimism_gap`(`reeval_frontier` 既存基盤)。

**確信度**: 白地存在=中-高(§1)。探索が均等 gated-delta に勝つか=中-低(未実測、2504.14366 定数天井ゆえ絶対 gain 小の可能性)。→ **耐久 deliverable は「絶対勝利」でなく「定数多様体内の honest Pareto/cliff 地図」**。

### 3.2 軸 B(副・統合ビジョン接続)— 定数モデル × 外部化された統治 recall(llive)の共同設計
**TRIZ 矛盾(より深い層)**: 「モデルが全部知っている(recall)」と「モデルが小さく定数のまま」が両立しない。業界は**モデル内部**で解く(3:1 hybrid)。別解 = **空間的分離**(TRIZ 原理 1/2): recall 機能を定数状態モデルから取り出し、llive の統治された 4 層メモリ+検索に外部化する。

**主張(薄い刃を正確に)**: 新規性は「線形モデル」でも「RAG」でもなく(両者既存)、**(i) 軸 A の cliff 地図で「モデルが内部保持すべき範囲 vs llive に外部化する範囲」の境界を共同設計し、(ii) その境界経路を Approval Bus/SPC/HITL で統治・監査可能にし、(iii) honest gate(capability-gate/cliff 実測/provenance)で計測する**こと。`project_fullsense_unified_model_vision` の「llcore 縦統合 + governance vs Hermes 横 wrap」をそのまま実装。

**なぜ潰されないか**: Qwen3.5/Kimi/HALO は model 層プレイヤで recall をモデル内に押し込む。Hermes(Nous, model-agnostic 横 wrap)は縦統合も governance も定数モデル共同設計も無い。→ 食われない核 = **境界共同設計 + 統治/監査 + honest gate**(model でなく infra/governance 貢献=llcore テーゼと一致)。

**検証実験**: ①境界学習プローブ(cliff を境に内部/外部化、長文書 QA を llive 外部化 有/無 で held-out 測定。**反証可能**: cliff 超 recall を llive 外部化すると定数状態を保ったまま task 精度回復するか)②governance 非迂回テスト(recall 経路が Approval Bus/audit を通過 = Hermes 差別化の load-bearing)③honest 比較 vs (a)3:1 hybrid(無統治)(b)線形モデル素 RAG(無共同設計)。**「ただの RAG ではない」を示せなければ novelty 不成立**と正直判定。

**確信度**: 概念整合・vision 接続=強だが研究 novelty=中-低(RAG 文献と重複)。「**製品/システム差別化が主、研究 novelty は細い刃**」と位置づける。

### 3.3 A と B の連結(1 本の物語)
軸 A は「定数状態モデルの recall 天井がどこか」を honest に測る(cliff 地図)。その天井が軸 B の「内部保持 vs llive 外部化の境界」を定義する。**A が B に cliff を供給し、B が A の天井を統治された外部層へ逃がす**。TRIZ 的にも一貫(A=mixer 空間内分離、B=モデルと外部メモリの空間的分離)。**2504.14366 の「定数状態は state 解像度天井あり」を否認(3:1 で隠す)でなく設計で受け止める**のが両軸共通の honest 姿勢。**推奨 = 軸 A を主 novelty(falsifiable・実装基盤あり)、軸 B を vision 接続の system 差別化(研究核は細い刃と正直に)として併走**。

---

## 4. 純定数状態(KV 非増加)ニッチの実在性 verdict

### 4.1 結論一文
純定数状態ニッチは **実在するが narrow かつ honest に bounded**。品質コストの本体は MMLU/一般知識ではなく **長文脈 associative recall の構造的天井**(蒸留 budget では破れない)。「長文脈 recall で勝つ」路線なら **No**。「**graceful な無限ストリーム圧縮 + native GGUF serveability + 正直な天井開示**」に再定義し、かつ **gated-delta 系セルで**やるなら **条件付き Yes**。確信度=中〜高。

### 4.2 品質コストの局在(一次情報)
- **MMLU/一般知識コストは data-parity では小さい**(確信度=高): **Falcon Mamba 7B(完全 pure Mamba, 2410.05355)= MMLU 62.11** vs Llama3.1-8B 66.43 / Mistral-7B 64.16、6bench 平均 **64.09**。→ 十分なデータ規模なら pure の MMLU 罰則 ~2-4pt = 限定的。「全層線形=MMLU 崩壊」(SUPRA 28 vs 62)は **uptraining token 不足 artifact** であって pure の本質ではない。
- **本体コスト = 長文脈 recall の hard cliff**(確信度=高): Mamba-2 pure=8K まで near-perfect、**16K 超で poor〜zero、規模に依らず**(larger ほど length-gen 悪化, 2406.07887 / Stuffed Mamba 2410.07145)。RWKV-7 "Goose"(2503.14456)=4k 訓練で 8k-16k まで perfect → その後 drastically forget(著者自認)。from-scratch 下限(2504.14366 Table 3)= pure additive 全長 0% NIAH、最良 linear-native(Gated DeltaNet head-wise α)でも 2k=81.8/4k=29.8%。
- **cliff は蒸留で埋まらない**(確信度=高): 2504.14366「state resolution > distillation budget」。

### 4.3 ★3 メモリ階層で見る純度ニッチの正体
1. **3:1 full-attn hybrid**(Qwen3.5/Kimi 業界デフォルト)= 1/4 層 full attention → **KV 線形増 = 厳密に定数でない**。
2. **linear+SWA hybrid**(LoLCATs/Liger=llcore 現状)= KV は window で bounded → **実質定数だが exact recall は窓内のみ、かつ非標準で GGUF 不可**。
3. **pure recurrent/SSM**(RWKV-7/Mamba/pure Gated DeltaNet)= 何も育たない = **真の定数 + native GGUF**。

→ 純度ニッチの優位は **Tier1 に対して真の定数メモリ(無限ストリーム/エッジ)**、**Tier2 に対しては serving(native GGUF)+ window 簿記不要 + 理論的純度**(メモリ差は marginal)。**★llcore 文脈での純度の最大価値 = 「serving wall の解消」**: `project_fullsense_unified_model_vision §2` の「llcore 非標準 linear attn は llama.cpp 非対応→Ollama 直は非自明」を、標準 pure-recurrent セル(`llama_memory_recurrent` + `llm_build_rwkv7_base`/`llm_build_mamba_base`)に揃えれば直接解ける(確信度=中〜高)。現 `WindowLinearAttention`(非標準 intra-layer linear+SWA 融合)は native kernel 無し=配れない。

### 4.4 llcore 北極星との噛み合い + 採用条件
- **本質的 tension**(確信度=高): llcore 北極星「定数 state で長文脈」。pure 定数はその最大表現だが**長文脈 exact recall を上限で殺す**。切り分け = llcore の「長文脈」が **(A) 無限会話の graceful な lossy 圧縮(recency 偏重)** なら pure 定数は最良適合 / **(B) 32k+ exact needle retrieval** なら pure は失格で window/hybrid 必須(純度を捨てる)。
- **長文脈 recall で品質勝負 = No**(確信度=高)。
- **以下に再定義なら条件付き Yes**(確信度=中): ①旗印を「純度=真の定数(KV 非増加)」に反転、Qwen3.5 ベースラインに context-sweep×needle で「3:1 は定数でない」を一次提示 / ②標準 pure-recurrent セル(Gated DeltaNet-2 / RWKV-7 型 vector-gated delta / Mamba-2)で **native GGUF/Ollama 経路**を開く(純度が deployability を買う = 統合モデル北極星の第 1 の壁を崩す)/ ③空白の交点「Qwen 由来 × 完全定数 × CPU オンプレ × honest gate」は無人。
- **★絶対条件(honest)**: 現 student の **additive `LinearAttention(diag/full)` で純度をやってはいけない**(=2504.14366 の 0% NIAH)。pure でいくなら **gated-delta セル(`ttt.py` / Gated DeltaNet-2 型)必須**。cliff を隠さず context-sweep+needle で開示してこそ honest differentiation。**RWKV-7 自身が gated-delta-rule の一種に収斂** = 「純定数を正しくやる = 結局 gated-delta」、pure-additive 純度は dead end。

---

## 5. 未確認・要一次検証(honest)

**本統合が abstract 一次確認**: HALO title/acronym/Qwen3/2.3B/hybrid(2601.22156)。
**investigations 由来で本統合は未再検証**(各確信度は本文記載):
1. **HALO §4.3 の層選択式 s_i = recall低下/CSR低下 と k=⌊L/4⌋**: INVESTIGATE 1/3 が本文 HTML 確認と主張。本統合は abstract まで(機構詳細は body 依存=PDF/repo `thunlp/hybrid-linear-attention` で式の厳密形を再確認推奨)。
2. **Jet-Nemotron PostNAS 2508.15884 / STAR(Liquid AI)**: abstract/web 要約レベル(INVESTIGATE 1 継承)。「NAS で層配置」「進化探索」の核主張は本文で最終確定推奨。
3. **llcore で O1 vs O2(出力 MSE → 注意分布 CE)が held-out/長文脈で実際に勝つか = 未測**(損失式は確証、llcore 効果は要 A/B、CPU 可)。
4. **Qwen GQA/QKV-bias への feature map / 注意行列 hook 割当**(KV-head 単位 or Q-head 単位、bias 処理)= llcore 自前 PoC 必須・未検証(最大の移植コスト)。
5. **0.5B 域の絶対 gap**(範囲内だが量は未実測、0.5B は特に厳しい予想)。
6. **D3/D4/D5 は未実装**(`logit_kd_loss`/`distill_joint`/LoRA/gated-delta routing)。「やった」と書かない。
7. **Gated DeltaNet-2(2605.22791)は abstract のみ**(本文未精読、RULER 改善の絶対値・hybrid vs recurrent 内訳未確認)。
8. **Falcon Mamba 長文脈 recall 弱点は HF blog 非開示**(出版バイアス)、NIAH/RULER 絶対値は本文/第三者 bench 要確認。RWKV-7/Mamba cliff 数値(8k/16k)は一部二次 web 経由 → OpenReview/原論文 table 直読で最終確定推奨。
9. **GGUF 純度 serving の優位**: llcore 固有セルの GGUF kernel 化コストは未見積(pure recurrent セルにすれば native 化見込みだが工数未確定)。
10. **軸 A の探索が固定ヒューリスティックを実際に Pareto 支配するか = 全未測**(2504.14366 定数天井ゆえ gain 小の可能性)。
11. **Qwen3.5 小型の正確な比率と <35B=Apache-2.0**(軸 B/新ベース判断の前提、二次=HF LICENSE 要確認)。

---

## ★memory 更新案(main が適用)

### → `project_llcore_efficient_arch_landscape_2026_06_26` へ追記

```
## 2026-06-28 統合(蒸留プロトコル T3 + 差別化テーゼ T5 + 純定数ニッチ。詳細正本 = fullsense docs/research/distill_protocol_and_differentiation_2026-06-28.md)
- **★層別 NAS novelty verdict = 現行文言のまま死亡(確信度高)**: HALO(2601.22156, title=「Hybrid Linear Attention Done Right」/ HALO=pipeline acronym「Hybrid Attention via Layer Optimization」両立, Qwen3→HypeNet 2.3B<0.01%, hybrid=非定数, abstract 本統合確認)単体でなく、層別線形化選択が混雑サブ分野(SMART/RAD/KL-LS=importance 選択, Jet-Nemotron PostNAS 2508.15884=真 NAS で層配置+block 選択, STAR=進化探索)に先取り済。HALO 選択=単一パス貪欲・固定 k=L/4・非定数。MoH は別軸(per-head 不侵食)。
- **生存路 = A(温存 softmax ゼロ=KV 完全定数 hard 制約)∩ B(長文脈 recall 明示 Pareto 目的)の交点のみ**。文言を「memetic NAS で層別線形化探索」→「**完全定数制約下で長文脈 recall を Pareto 目的に置いた heterogeneous 層別 mixer 探索**」へ書換必須。binding: ①貪欲 LOO/Top-k(HALO 流)baseline を実測超え必須 ②定数制約下で層別異質性が均一 gated-delta を支配しないと honest null。
- **蒸留プロトコル(LoLCATs path)**: 5 目的ラダー O1 出力MSE(済)→O2 Hedgehog 注意分布 CE→O3 MOHAWK hidden→O4 logit-KD→O5 LoRA+CE。★MOHAWK 予算 80M/160M/2.76B=92% e2e → per-layer は warm-start・joint が回復本体。昇格トリガ `G=ε_joint−ε_indep`(reeval_frontier で測定可)が CI 超で D3/D4 joint 必須。O(T²) の O2 を NAS fitness に wire しない(選定 1 genome の warm-start のみ)。実装点 = distill.py に attn_ce_loss/distill_joint/LoRA、ttt.py に Gated DeltaNet-2 型。
- **純定数ニッチ verdict = 実在 narrow・honest bounded**: コストは MMLU でなく長文脈 recall に局在(Falcon Mamba 2410.05355=data-parity MMLU 罰則 ~2-4pt / 但し 8-16k で recall hard cliff、蒸留で埋まらず=2504.14366)。★最大価値 = serving wall 解消(標準 pure-recurrent セルで native GGUF/Ollama 経路)。絶対条件: additive で純度禁止、gated-delta 必須。「長文脈 recall で勝つ」=No、「無限ストリーム圧縮+GGUF serveability+正直な天井開示」=条件付き Yes。
```

### → `project_fullsense_unified_model_vision` へ追記

```
## 2026-06-28 差別化テーゼ補強(distill_protocol_and_differentiation_2026-06-28.md)
- **serving の壁(§2)に一次の解決路**: llcore 非標準 linear attn が llama.cpp 非対応の問題は、**標準 pure-recurrent セル(Gated DeltaNet-2 / RWKV-7 型 / Mamba-2)に揃えれば native GGUF(llama_memory_recurrent + llm_build_rwkv7/mamba_base)で直接解ける**。現 WindowLinearAttention(非標準融合)は配れない。「純度=真の定数」が deployability を買う = 北極星第1の壁を崩す(確信度 中〜高、kernel 化工数は未見積)。
- **対 Hermes 差別化を研究テーゼ化(軸 B)**: 定数モデル × llive 外部化 recall の共同設計。novelty は「線形モデル」でも「RAG」でもなく (i)軸 A の cliff 地図で内部保持 vs 外部化の境界を共同設計 (ii)境界経路を Approval Bus/SPC/HITL で統治・監査 (iii)honest gate で計測。研究核は細い刃(RAG と重複)=製品/システム差別化が主と正直に。Hermes(横 wrap, model-agnostic)は縦統合も governance も持たない=食われない核。
- **A↔B 連結**: 軸 A(定数モデルの recall cliff 地図)が軸 B(内部保持 vs llive 外部化の境界)を定義。A が cliff を供給、B が天井を統治された外部層へ逃がす。2504.14366 の定数天井を「3:1 で隠す」でなく「設計で受け止める」のが両軸共通の honest 姿勢。
```

---

## Sources(一次/準一次)
- HALO — https://arxiv.org/abs/2601.22156(title/acronym/Qwen3/2.3B/hybrid=本統合 abstract 確認 / §4.3 層選択=investigations 本文)
- Jet-Nemotron PostNAS — https://arxiv.org/abs/2508.15884(NVIDIA, abstract レベル)/ STAR — https://www.liquid.ai/research/automated-architecture-synthesis-via-targeted-evolution(web 要約)/ MoH — https://arxiv.org/abs/2410.11842
- Hedgehog — https://arxiv.org/abs/2402.04347 / MOHAWK — https://arxiv.org/abs/2408.10189 / LoLCATs — https://arxiv.org/abs/2410.10254 / Liger — https://arxiv.org/abs/2503.01496
- What Matters in Linearizing(additive 0% NIAH / state>budget) — https://arxiv.org/abs/2504.14366
- Gated DeltaNet-2 — https://arxiv.org/abs/2605.22791(abstract)
- RWKV-7 "Goose" — https://arxiv.org/abs/2503.14456(OpenReview ayB1PACN5j)/ Falcon Mamba — https://arxiv.org/abs/2410.05355 + https://huggingface.co/blog/falconmamba / Mamba LM 実証 — https://arxiv.org/abs/2406.07887 / Stuffed Mamba — https://arxiv.org/abs/2410.07145
- llama.cpp 対応 — https://deepwiki.com/ggml-org/llama.cpp/3.11-supported-model-architectures
- 接続: T2 `linearization_recipes_2026-06-28.md` / T4 `efficient_arch_landscape_refresh_2026-06-28.md` / prereg `preregistration/prereg_linearization_distill.md` / 実装 `D:/projects/llcore/src/llcore/runtime/distill.py` ・ `lm/ttt.py`
