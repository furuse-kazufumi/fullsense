# 線形化(蒸留変換)レシピ比較と llcore 採用方針 — 2026-06-28

> **目的**: softmax attention を線形 attention / 線形再帰 / SSM へ「線形化(蒸留変換)」する各レシピを精査し、llcore(Qwen2.5 0.5B/1.5B を線形化、現状蒸留 = per-layer attention 出力 MSE = LoLCATs Step1 相当、RTX 5090 32GB 着荷予定)への **採用判断材料**を 1 枚に統合する。
> **担当**: 5 本の deep-read(LoLCATs / SUPRA / MOHAWK / Mamba-in-Llama / 横断アンカー+失敗モード)を統合。`docs/research/preregistration/prereg_linearization_distill.md` と接続。
> **規律**(`feedback_benchmark_honest_disclosure` / `feedback_implementation_status_record` / `feedback_verify_existence_before_claiming`): RAD/コーパスの記述は一次情報(arXiv 原論文)で検証してから採用。未確認は「未確認」と明記。誇張禁止・確信度明記・出典必須。
> **検証ステータス**: 本 md の中核主張のうち、(a) LoLCATs 2 段手順・損失・RoPE・Hedgehog feature map、(b) SUPRA の LM-CE/GroupNorm/減衰、(c) MOHAWK 3 段損失、(d) Mamba-in-Llama の重み移植式・KL 損失・hybrid 残層、(e) 失敗モードの中核 = 「What Matters in Linearizing」2504.14366 の **gated-delta 必須 / additive は不可逆 state saturation / state 解像度 > 蒸留 budget**(本統合担当が WebFetch で原文確認)、(f) STILL 2602.02180 の実在・正式名(本担当が WebSearch で確認)— は一次情報で検証済み。残りの確信度は §5 に明記。

---

## 1. 目的と llcore の現在地

### 1.1 北極星と射程
- **北極星 = メモリ効率(constant state)**。線形 attention は KV を O(d²) state に畳み込むので会話長が無限でも固定メモリ。代償は **長文脈品質**(`prereg §1`)。
- **射程 = Qwen2.5 0.5B(24層)/ 1.5B(28層)の線形化**。GQA + QKV bias + RoPE を持つ Qwen 系が対象。
- **GPU = RTX 5090 32GB 着荷予定**。LoLCATs が 8B を 40GB A100 1 枚・数時間で回す事実(`2410.10254`、本担当 RECIPE1 で本文確認)から、0.5–1.5B は 32GB で余裕。block-by-block 蒸留は不要。

### 1.2 実装済み資産(prereg の実装状態 4 段から、honest)
llcore は「per-layer 出力 MSE 蒸留だけ」ではなく、LoLCATs の **核心部品をすでに実装済み**である点が重要(`prereg §1 実装状態`、コード = `src/llcore/runtime/linearize.py` / `distill.py`):

| llcore 実装物 | 対応するレシピ概念 | 状態 |
|---|---|---|
| `linearize_qwen2`(softmax→linear, **weight 再利用**, **RoPE 厳密**)| LoLCATs/MIL の「射影流用」+ LoLCATs の「RoPE を q,k に適用後に feature map」 | 実装+単体検証済 |
| `LinearAttention(feature_map="diag"\|"full")`、full = per-head 全結合 W∈[H,d,d] 恒等初期化 | Hedgehog 系の学習可能 feature map(容量 = full が Hedgehog 寄り)| 実装+単体検証済 |
| `WindowLinearAttention`(直近 window=softmax + 古い key=線形、**単一分母融合**)| **LoLCATs の intra-layer hybrid(線形 + SWA)そのもの** / Liger Attention | 実装+単体検証済(10 tests)|
| `SlidingWindowAttention` | hybrid の SWA 経路 | 実装済 |
| `distill_layer` / `distill_all_layers`(出力 MSE、base 凍結、feature map のみ学習、pristine teacher から per-layer 独立)| **LoLCATs Step1 = attention transfer** | 実装+単体検証済 |
| 層別 hybrid NAS(`evolve_linearization.py` / `nas_pareto.py --proxy-v2`、memetic 多目的)| **どのレシピにも無い llcore 固有**(層ごとに mixer を選ぶ Pareto 探索)| 実装済 |

**未実装(prereg「要追加」)**: ① LoRA Step2 回復、② logit-level KD(最終 logit / 層別 hidden)、③ end-to-end 本訓練。
→ **honest**: 現コードの「蒸留」は LoLCATs Step1 に等しい(車輪の再発明)。新規性は **層別 hybrid NAS** にある(`prereg §5-3`)。本 md は「現 Step1 から何を足すか」を 5 レシピの一次知見で具体化する。

---

## 2. ★レシピ比較表

固定 9 観点のうち load-bearing な 8 列を表に、ニュアンスと出典は各行下に。すべて arXiv 一次情報で検証した範囲のみ(未確認は明記)。**回復率は単一数字に丸めず内訳必須**(`feedback_benchmark_honest_disclosure`)。

### 2.1 主要 4 レシピ + アンカー 3(Hedgehog / DiJiang / Liger)

| レシピ (arXiv) | 手順段数 | 蒸留損失 | 対象層 (全/hybrid) | RoPE 処理 | 報告回復率(内訳)| 長文脈挙動 | コスト | llcore 実装容易性 |
|---|---|---|---|---|---|---|---|---|
| **LoLCATs** `2410.10254` (ICLR25) | **2 段**: ①attention transfer ②LoRA 回復 | ①**出力 MSE** ②**next-token CE**(logit KD でなく CE)| **全層線形** だが各層内 **線形+SWA(w=64)hybrid** | **q,k に RoPE 適用後**に feature map(検証済)| 5-shot MMLU 先行比 **+20pt 超**、zero-shot LM avg 73.1 vs 元 74.2(L3-8B)| **弱**(SWA 窓外を想起不可。本文は長文脈評価を報告せず=正直に弱点)| ~40M tokens、8B で 40GB A100・数時間、param 0.2%/token 0.4% | **最高**(Step1=実装済、RoPE 厳密済、hybrid=WindowLinearAttention 済。Qwen GQA/bias 対応の薄い adapter のみ要)|
| **SUPRA** `2405.06640` | **1 段**(uptraining、joint)| **LM-CE のみ**(MSE/KD 不使用)| **全層線形**(hybrid 無)| feature map **後**に RoPE、**減衰 γ(RetNet)併存** | 常識系は competitive 回復、**MMLU 5-shot は ~28–30 へ崩壊**(base ~62)※数値概数 | **見かけ維持だが減衰 γ の副作用**(effective context 短縮)= 真の長文脈でない | **~5%(=20B–100B tokens)** = LoLCATs の 500× | 低(全層線形+大トークン。32GB 1 枚では非現実的)|
| **MOHAWK** `2408.10189` | **3 段**: ①matrix orientation ②hidden alignment ③weight transfer+KD | ①**混合行列 Frobenius** ②**hidden L2** ③**logit KD(CE)** | Mamba-2 へ全置換 / **Hybrid 版は 4 層 softmax 残置** | **未確認**(原論文・blog・README とも RoPE 明示記述なし。Mamba 化で RoPE 喪失=外挿弱の含意)| Phi-Mamba-1.5B 6bench 平均 ≈62.6%、Hybrid 1.5B 66.0% ≈ teacher 67.2%(回復 ~98%)| Mamba 固定 state ゆえ recall 弱、**hybrid 残層で回復** | 3B(full)/5B(hybrid) tokens、スクラッチ <1% data | 中(student=Mamba-2 前提で Q/K/V/O を捨てる。llcore の線形 student と別系。**Stage1 行列マッチング思想だけ移植可**)|
| **Mamba-in-Llama (MIL)** `2408.15237` (NeurIPS24) | **1+任意段**: 重み移植→**end-to-end KL**(+任意 SFT/DPO)| **系列 KL(α=1,β=0.1)+CE**。per-layer 整合は optional | **hybrid 必須**: attention **25–50% 残置**(0%=明確に劣化)| **未確認**(論文 silent。残置層=RoPE 保持/Mamba 層=SSM が位置担当 と推論)| AlpacaEval2 LC **29.61**(50%残置/Mamba1-L3)、25%版=25.85、MT-Bench 7.35 | **強い(needle 蒸留長の 20×)** ただし **attention 残置が前提** | 20B tokens、8×80GB A100・3–5 日 | 中(target=Mamba。**hybrid 残置 25–50% の教訓**と weight 移植思想は直輸入可)|
| **Hedgehog** `2402.04347` (ICLR24) | 2 段(feature map distill→微調整)| **注意分布 CE**(softmax 重みを soft-label、線形の正規化重みを予測)= 出力 MSE より一段強い目的 | 全層線形 | **未確認**(標準位置符号互換前提、明示処理なし)| 標準 Transformer 品質 **99%超回復**、GPT-2 変換 WikiText-103 16.7ppl(SOTA)| state 容量律速(全層線形)| 軽量(feature map=単層 MLP+出力 softmax)| **高**(損失アップグレード候補。出力 MSE → 注意分布 CE で Step1 品質↑。full feature map と相性)|
| **DiJiang** `2403.19928` (ICML24) | 1 段(置換→fine-tune)| **未確認**(明示損失式を本文で特定できず)| 全層置換(hybrid 無)| **未確認**(DCT×位置符号の相互作用未記述)| DiJiang-7B ≈ LLaMA2-7B(11bench 0.557 vs 0.565)、学習 1/16–1/50 | **弱**(gating 無し加法+固定 DCT 特徴、長文脈評価薄い)| 非常に軽量(Pythia 70M 1.3 日)| 低-中(加法線形=state saturation 直撃。DCT 基底は参考のみ)|
| **Liger** `2503.01496` | **1 段**(LoLCATs の 2 段を省く)| **next-token CE のみ** | **層内 hybrid**: gated recurrent + **SWA(w=64)** | **未確認**(線形/再帰経路への RoPE 移植 明示なし)| **93% 回復を 0.02% tokens(≈0.02B)** で(1B–8B 検証)| 中(gate+窓 64 で recall 補強、上限は state+窓律速)| **最軽量**(追加パラメータ **0**、key 重み再利用 gate、LoRA r=8/2ep/Alpaca 10万)| **最高クラス**(追加パラメータ0+key→gate+単段 LoRA で Qwen 系に直移植しやすい)|

**行ごとの load-bearing 注記と確信度**:

- **LoLCATs**: 窓サイズは本文 **w=64** を採用(repo config 名 `wtk64_fd64_w01`)。二次要約の「1024」は **不採用**(repo config 直読で最終確定推奨=未確認)。LoRA rank r=8 は本文 HTML 抽出由来で repo 再確認推奨。Hedgehog feature map(`[SM(xW̃)⊕SM(−xW̃)]`, fd=64)が既定。**Qwen 非対応**(公式 repo は Llama/Mistral のみ)= 最大の移植コスト。
- **SUPRA**: GroupNorm 置換(分母 Σsim 除算をやめ RetNet 流 GroupNorm)+ γ^{i−j} 固定指数減衰。**γ が長文脈崩壊の主因**(effective context 短縮)。abstract が「persistent ICL and long-context shortfalls」と自認。数値(28–30 / 62)は二次抽出=概数、定性傾向は検証済。
- **MOHAWK**: 3 種損失の段別使い分けが本質。Stage1 は全 student 層を並列最適化可、conv=identity / gate=1 初期化、teacher 前段出力を入力に使う(検証済)。Hybrid ablation(残置 1/2/4 層 = 61.8/62.3/64.0%)と最終 66.0% はトークン予算差込みで断定回避。Llamba(`2502.14458`)が Llama-3.x→Mamba-2 へ MOHAWK 適用、MLP も解凍学習。
- **MIL**: 初期化式 `B=W_K·o, C=W_Q·o, x=W_V·o, 出力=W_O 再利用, softmax 除去`(本文式、検証済)。**主損失は end-to-end logit KL**で per-layer MSE は中核でない(LoLCATs/MOHAWK と対照)。逐次 hybrid は self-speculative 受容率が壊滅的の別報告あり(`2605.01106` abstract のみ=未確認)。
- **Hedgehog**: 損失 = `−Σ_j softmax(q·k)·log[φ(q)φ(k)/Σφ(q)φ(k)]`(注意確率の KL/CE)。診断 = softmax の (a)低エントロピー spiky 性 (b)dot-product 単調性 の 2 性質欠落が劣化原因。式番号は HTML 読解由来(損失の「形」は確証、番号は参考)。
- **Liger**: gate を **pretrained key からパラメータフリー Pooling** で生成(`G_t=Pooling(k_t)`)、feature map=Softmax。α/β 具体値は本文未指定(未確認)。**llcore 最重要参照**(Qwen 親和・追加パラメータ0)。

### 2.2 最近(≤1y)の派生(比較軸用・確信度は abstract 検証レベル)

| 手法 (arXiv) | 中核 | hybrid? | 報告(内訳)| llcore 含意 |
|---|---|---|---|---|
| **Lizard** `2507.09025`(abstract 検証)| 学習可能 adaptive memory 制御 + gated attention 数値安定化 | adaptive | 5-shot MMLU 先行比 **+9.4–24.5pt**、recall 優位、near-lossless | recall/length を狙い撃ち改善 |
| **STILL** `2602.02180`(**本担当が実在+正式名確認**)| Self-Saliency で重要 token を sparse softmax、残りを線形要約 + **NP-Map(norm 温存)** | **層内 hybrid(token 選択型)** | 長文脈 bench で先行線形化比 **最大 +86.2% 相対**、常識/推論で原モデル同等以上 | 「学習 feature map が pretrained 特徴の magnitude を歪める」失敗を NP-Map で直接対処 |
| **LAWCAT** `2509.18467`(abstract 検証)| Causal Conv1D + normalized gated linear attention、1K 長で蒸留 | 全層線形+局所 conv | 1K 蒸留で **passkey 90%超を 22K まで**、<0.1% tokens | 局所 conv で recall 補強。短窓蒸留→長窓汎化の前例 |
| **TPTT** `2506.17671`(abstract 検証)| LiZA + Memory-as-Gate、LoRA、DeltaProduct で純線形化 | 可変 | **Qwen2.5-1.5B 含む 1B 級で検証** | **llcore 対象 Qwen に最も近い実例**(要本文精査)|
| **LoLA** `2505.23666`(LoLCATs recall 失敗の定量)| sparse cache 追加 | hybrid+cache | LoLCATs 系 passkey/S-NIAH **≈0.6%** → LoLA **97.4%** | LoLCATs の recall 欠陥の定量裏付け+緩和策 |

---

## 3. 失敗モード横断 と llcore 北極星(constant state)との噛み合い

### 3.1 線形化が劣化する条件(一次情報の中核知見)
1. **Associative recall が劣化主因**: Zoology(`2312.04927`)— AR の取りこぼしが attention との perplexity ギャップの **平均 82%** を説明。**規模でなく機構の問題**(70M Transformer が 1.4B Hyena より AR を解く)。
2. **recall–throughput トレードオフ(state 容量律速)**: Based(`2402.18668`)— recurrent state サイズと recall 精度が原理的トレードオフ。固定 state は長文脈で needle/passkey/MQAR が頭打ち。
3. **★加法線形の不可逆 state saturation**: 「What Matters in Linearizing」(`2504.14366`、**本担当が WebFetch で原文確認**)— *"only gated delta-rule formulations maintain the precision necessary for long-context retrieval, whereas additive models suffer from irreversible state saturation"*、*"state resolution is a more fundamental bottleneck than the distillation budget"*。**アーキの帰納バイアスが第一制約で、蒸留 token を増やしても克服できない**(140M–1.7B、7 アーキ比較)。
4. **学習 feature map の分布シフト**: STILL(`2602.02180`)— 学習可能 feature map が pretrained 特徴の magnitude を歪める → norm 温存(NP-Map)で対処。
5. **spiky/単調性欠落**: Hedgehog(`2402.04347`)— kernel が低エントロピー性・単調性を欠くと注意が平坦化。
6. **長文脈 ICL/extrapolation 不足**: SUPRA(`2405.06640`)が最大規模でも自認。

**失敗が露出する評価**: MQAR / S-NIAH / passkey / RULER / BABILong / 5-shot MMLU。**短中文 PPL・常識 bench だけだと失敗モードが隠れる**(DiJiang・初期手法はここが薄い)。

### 3.2 llcore 北極星との噛み合い(最重要の honest 警告)
llcore の北極星は「**constant state(固定メモリ)**」かつ用途は「会話 + **長文脈 recall**」。ここに **構造的緊張**がある:

- llcore の現 student = `LinearAttention(feature_map=diag/full)` は **加法型(additive)**。`2504.14366` の verdict 上、これは **long-context retrieval で不可逆 state saturation を起こす最も弱い機構**。
- 重大な含意: **prereg の H1(出力 MSE 蒸留が frontier を右シフト)/ H4(logit-KD+LoRA 追加)が PASS しても、それは「加法型 student の回復」であり、長文脈 recall の天井(state 解像度)は蒸留 budget では破れない**。つまり「蒸留で右シフト」と「長文脈 recall が解決」は **別問題**。`2504.14366` は明確に **state 解像度 > 蒸留 budget**。
- 一方 **constant state とは両立可能**: hybrid(SWA 残層 = llcore は WindowLinearAttention 実装済)と **gated-delta(誤り訂正更新)** は、いずれも O(d²) 固定 state を保ちつつ recall を改善できる(`2504.14366` が gated-delta を、MIL が attention 25–50% 残置を、Liger が key→gate+窓を提示)。**北極星を捨てずに recall を救う道は「機構の選択」**であって「蒸留の強化」ではない。

→ **結論的緊張**: llcore は LoLCATs path(加法 + SWA hybrid + 蒸留回復)を最短で実装できるが、**長文脈 recall を本気で狙うなら加法 feature map のままでは天井がある**。採用方針(§4)はこの 2 面を分けて設計する。

---

## 4. ★llcore 採用方針(1 本に絞る + 理由 + 段階)

### 4.1 採用 1 本: **LoLCATs path(2 段蒸留 + 層内 SWA hybrid)を主軸に確定**
**理由**(prereg のレシピ基準と一致):
1. **llcore の core と最短距離**: Step1(出力 MSE)・RoPE 厳密・WindowLinearAttention(線形+SWA)・full feature map が **すでに実装済**。残りは LoRA Step2 と logit-KD の追加のみ。
2. **32GB・小トークンで現実的**: ~40M–数 B tokens 級で足り、SUPRA(20–100B)/MIL(20B・8×A100)は単一 32GB に不適。MOHAWK(Mamba student)は Q/K/V/O を捨てる別系で移植コスト大。
3. **Liger を補助採用**: 「追加パラメータ0 + key→gate Pooling + 層内 SWA」は Qwen 系に直移植しやすく、LoLCATs path に **gating を足す最小手**。長文脈アームで第一候補。

**1 本に絞る = LoLCATs を蒸留/回復の足場に固定**。SUPRA は **全層線形 = lower-bound 比較対象**(採用しない)、MOHAWK は **段階蒸留の設計参照(logit-KD 手順の雛形)**、MIL は **hybrid 残置率と weight 移植思想の裏付け**(直輸入しない)。これは prereg §「レシピ基準」表と整合。

### 4.2 現 Step1 から足すもの(prereg と接続した段階計画)

| 段階 | 内容 | レシピ出典 | prereg 接続 | 確信度 |
|---|---|---|---|---|
| **S0(済)** | per-layer 出力 MSE 蒸留(feature map 学習、base 凍結)| LoLCATs Step1 | `distill_layer` 実装済、H1/H2/H3 の主対象 | 実装+単体検証済 |
| **S1** | **層内 hybrid を既定化**: WindowLinearAttention(線形+SWA w≈64)を NAS allele の第一候補に。**純線形は MSE が悪化**(LoLCATs/Liger の核心)| LoLCATs / Liger | `prereg §3.1` の変換タイプ allele。aggressive genome は SWA 併設 | 実装済(配線/既定化のみ)|
| **S2** | **損失を注意分布 CE へアップグレード**(出力 MSE → Hedgehog 型 `KL(softmax‖φφ正規化)`)。full feature map と組む | Hedgehog | **prereg 範囲外の新アーム**(現 prereg は出力 MSE のみ登録)→ 実装後に prereg 版上げ | 損失形は検証済、llcore 効果は未測 |
| **S3** | **LoRA Step2 回復**(projection に LoRA r=8、end-to-end next-token CE)。MMLU +20pt の主因 | LoLCATs Step2 / Liger | prereg H4(条件付き・要実装)| 未実装 |
| **S4** | **logit-KD(+任意 層別 hidden KD)**: 最終 logit KL(τ)/ block hidden MSE | MOHAWK Stage2-3 / MIL | prereg H4 / `§3.2 要追加` | 未実装 |
| **S5(長文脈アーム)** | **gated 機構を NAS allele に追加**(Liger key→gate / gated-delta 更新則)。**加法 state saturation を回避する唯一の本質策** | Liger / `2504.14366` / LAWCAT 局所 conv | prereg 範囲外の将来アーム。長文脈が要件なら必須 | 機構選択は検証済、llcore 実装は未着手 |

**RoPE の扱い(llcore の強み)**: LoLCATs path を採れば **RoPE は q,k に適用後 feature map**(`2410.10254` 検証済)で、llcore は既に RoPE 厳密実装済 = この path は **唯一 RoPE が一次情報で確定している路線**。Mamba 化(MOHAWK/MIL)に進むと RoPE 喪失で外挿が落ちる(両論文とも RoPE 未記述=未確認)ため、**線形 attention student を維持して RoPE を保つ**のが honest かつ低リスク。残置 softmax 層は RoPE 保持。

### 4.3 honest 内訳の注意(prereg §5 と一致、必ず守る)
1. **compute-matched**: 蒸留あり/なしを同 compute で比較。S3/S4 追加時は token 予算を揃える(LoLCATs ~40M を基準スケール、`prereg §6`)。
2. **held-out / winner's curse**: frontier は max-of-N の楽観。`delta_nll_heldout` と `optimism_gap`(`reeval_frontier`)で語り、選択窓 Δnll を headline にしない。
3. **短窓の盲点**: 線形劣化は長文脈で出る。`--context-sweep 256,512,1024,2048` + `--needle` で測り、**短窓改善を「回復」と呼ばない**。
4. **車輪の再発明の開示**: 「蒸留が効いた」= LoLCATs Step1 の追試。**新規性は層別 hybrid NAS**(`evolve_multiobjective`)と正確に位置づける。
5. **加法 student の天井の開示(本 md の追加 honest)**: §3.2 の通り、蒸留右シフトが PASS しても長文脈 recall の解決は別問題(`2504.14366`: state 解像度 > 蒸留 budget)。**「frontier 右シフト」を「会話品質/長文脈回復」と読み替えない**。長文脈クレームは S5(gated)アーム + needle/RULER 実測でのみ行う。
6. **実装状態の正直開示**: S3/S4/S5 は未実装。「やった」と書かない。H4 系は実装完了をもって prereg を版上げして別 run。

---

## 5. 未確認・要一次検証の残事項(honest)

**本担当(統合)が原文確認した**: LoLCATs 2 段/損失/RoPE/Hedgehog(RECIPE1, 一次)・SUPRA LM-CE/GroupNorm/γ(RECIPE2)・MOHAWK 3 段損失(RECIPE3)・MIL 移植式/KL/hybrid(RECIPE4)・Hedgehog/DiJiang/Liger(RECIPE5)・**`2504.14366` の gated-delta/additive saturation/state>budget(本担当 WebFetch)**・**STILL `2602.02180` 実在と正式名(本担当 WebSearch)**。

**未確認 / 要一次検証(採用前に潰すべき)**:
1. **LoLCATs 窓サイズ w**: 本文 **w=64** を採用したが repo config `wtk64_fd64_w01` と二次要約「1024」が不一致 → **repo config 直読で最終確定**。LoRA rank r=8・block b=9 も repo 再確認推奨。
2. **Qwen GQA/QKV-bias への feature map 割当**: LoLCATs/Liger 公式は Llama/Mistral 前提。**feature map を KV head 単位 / Q head 単位どちらに割るか、bias の扱いは llcore 自前実装で PoC 必須**(最大の移植コスト、未検証)。
3. **0.5B/1.5B 域の線形化 gap**: LoLCATs は 7B–405B 検証。超小モデルでは絶対 gap が大きく出る可能性(`2504.14366` は階層が規模で覆らないと示すが gap 量は未実測)。**0.5B は特に厳しい予想=要実測**。
4. **RoPE 処理が未確認のレシピ**: SUPRA 以外(MOHAWK/MIL/Hedgehog/DiJiang/Liger)は線形/再帰経路の RoPE 処理が原論文に明示なし。**llcore が LoLCATs path 以外を試す場合は自前で決める設計判断**。
5. **DiJiang の蒸留損失式 / Liger の α,β 具体値**: 原文で特定できず(未確認)。
6. **abstract 検証どまりの最近手法**: Lizard `2507.09025` / LAWCAT `2509.18467` / TPTT `2506.17671` / LoLA `2505.23666` / Component-Aware Self-Spec `2605.01106` は abstract のみ。**特に TPTT(Qwen2.5-1.5B 実例)は本文精査の価値が高い**(llcore に最も近い)。
7. **per-layer 独立蒸留 vs joint/e2e**: llcore の `distill_all_layers` は pristine teacher から各層独立。**誤差累積する e2e とは別物**。frontier の良さを e2e 品質と読み替えない(prereg §5-5)。

---

## Sources(一次情報)
- LoLCATs — https://arxiv.org/abs/2410.10254 (ICLR2025) / repo https://github.com/HazyResearch/lolcats
- SUPRA / Linearizing LLMs — https://arxiv.org/abs/2405.06640
- MOHAWK / Transformers-to-SSMs — https://arxiv.org/abs/2408.10189 / Llamba https://arxiv.org/abs/2502.14458
- Mamba-in-Llama — https://arxiv.org/abs/2408.15237 (NeurIPS2024) / repo https://github.com/jxiw/MambaInLlama
- Hedgehog — https://arxiv.org/abs/2402.04347 (ICLR2024)
- DiJiang — https://arxiv.org/abs/2403.19928 (ICML2024)
- Liger — https://arxiv.org/abs/2503.01496
- **What Matters in Linearizing**(gated-delta 必須 / additive saturation / state>budget、本担当確認)— https://arxiv.org/abs/2504.14366
- **STILL**(本担当実在確認)— https://arxiv.org/abs/2602.02180
- LoLA(LoLCATs recall 失敗の定量)— https://arxiv.org/abs/2505.23666
- Lizard https://arxiv.org/abs/2507.09025 / LAWCAT https://arxiv.org/abs/2509.18467 / TPTT https://arxiv.org/abs/2506.17671(abstract 検証)
- Zoology https://arxiv.org/abs/2312.04927 / Based https://arxiv.org/abs/2402.18668
- corpus: `D:/tools/raptor/.claude/skills/corpus/efficient_seqmodels_corpus_v2/`(750 papers、abstract のみ。本文詳細は上記 arXiv で補完)
- 接続先 prereg: `D:/projects/fullsense/docs/research/preregistration/prereg_linearization_distill.md`
