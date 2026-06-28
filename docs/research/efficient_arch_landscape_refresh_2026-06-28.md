# 効率アーキ・ランドスケープ refresh — 2026-06-28(6/26 landscape からの差分更新)

> **目的**: `project_llcore_efficient_arch_landscape_2026_06_26`(memory)と T2 結論(`linearization_recipes_2026-06-28.md`)以降に出た一次情報を統合し、(a) T2 核心主張(additive→不可逆 saturation / gated-delta 必須)の独立検証 verdict、(b) 6/26 以降の新着リード採否、(c) plateau を動かす機構の現ベスト、(d) 競合地図更新と llcore 差別化軸、を 1 枚に refresh する。
> **担当**: 4 本の deep-read survey(①T2 核心の敵対的検証 ②新着リード ③plateau/TTT 軸 ④競合地図)を統合。
> **規律**(`feedback_benchmark_honest_disclosure` / `feedback_verify_existence_before_claiming`): 各主張に確信度と出典を付す。本統合担当が本セッションで**独立再確認**したのは 2 件(下記 §0 検証台帳)。他は各 survey が原文/abstract で検証した範囲を継承し、検証レベルを明記する。誇張禁止・未確認は「未確認」と書く。

---

## 0. 検証台帳(この refresh で誰がどこまで一次確認したか)

| 主張の核 | 論文 | 検証レベル | 確認者 |
|---|---|---|---|
| gated-delta のみ long-context recall を維持 / additive は不可逆 state saturation / state 解像度 > 蒸留 budget | 2504.14366 | **本文 full-text(53KB)+ Table 3 実数値**で照合、abstract 引用 verbatim 一致 | survey① |
| TTT-E2E が 3B/164B で full-attention 同様に context scaling、GatedDeltaNet/Mamba2 は plateau、128K で 2.7× | 2512.23675 | **abstract 本セッション独立再確認**(下記) | 本統合担当 + survey③ |
| Gated DeltaNet-2 が erase/write を channel-wise 別ゲートに分離、1.3B/100B で RULER NIAH 最強 | 2605.22791 | **abstract 本セッション独立再確認**(下記) | 本統合担当 + survey③ |
| TPTT / Lizard / LAWCAT / LoLA の本文 | 2506.17671 / 2507.09025 / 2509.18467 / 2505.23666 | **本文(HTML)確認** | survey② |
| Qwen3.5 gated-delta 3:1 / xLSTM-distill / HALO / Kimi Linear | qwen.ai / 2603.15590 / 2601.22156 / 2510.26692 | qwen.ai 一次 + arXiv abstract、小型ラインナップは二次 | survey④ |

**本セッション独立再確認(arXiv MCP abstract)**:
- **2512.23675**「End-to-End Test-Time Training for Long Context」(Tandon, Dalal, Li, …, Yu Sun ら; cs.LG; 2025-12-29): *"for 3B models trained with 164B tokens, our method (TTT-E2E) scales with context length in the same way as Transformer with full attention, while others, such as Mamba 2 and Gated DeltaNet, do not. However, similar to RNNs, TTT-E2E has constant inference latency …, making it 2.7 times faster than full attention for 128K context."* アーキ = **SWA Transformer + test 時 next-token 学習 + 訓練時 meta-learning**。★重要: abstract は full attention と「**同様にスケール**(parity)」までで、「full 超え ppl」は主張していない(= survey③ の honest 留保が正しい)。
- **2605.22791**「Gated DeltaNet-2: Decoupling Erase and Write in Linear Attention」(Hatamizadeh, Choi, Kautz; **NVlabs**; cs.AI; 2026-05-21): channel-wise **erase gate b_t + write gate w_t** で「単一スカラが erase と write を tie」する制約を解消、KDA(両ゲート=同一スカラ)と Gated DeltaNet(decay も collapse)を一般化。**1.3B / 100B FineWeb-Edu tokens** で Mamba-2 / Gated DeltaNet / KDA / Mamba-3 中**最強**、*"advantage is most pronounced on long-context RULER needle-in-a-haystack"*。chunkwise WY 並列訓練を保持。code = `github.com/NVlabs/GatedDeltaNet-2`。

---

## 1. 更新サマリ — 6/26 landscape memory からの差分

6/26 landscape の 3 戦略発見(①core=LoLCATs Step1 ②新規軸=層別 NAS ③plateau 本命=TTT)は **方向として維持**。ただし 4 survey の一次情報で次の差分が出た:

1. **「plateau 本命=TTT」に直接の一次証拠が付いた**(6/26 時点は TTT 原典 2407.04620 の "Mamba 16k plateau" のみ)。**TTT-E2E 2512.23675**(2025-12、TTT 原典著者ら、3B/164B)が「**Gated DeltaNet・Mamba2 は context scaling せず、TTT-E2E は full attention 同様にスケール**」を実証。→ memory の予測が裏付けられた。**精緻化**: gated-delta は plateau を「動かす(16k→~32k)」が「破らない」。破るのは TTT-E2E(=訓練時 meta-learning による end-to-end credit assignment + test 時学習)。
2. **T2 核心(additive vs gated-delta)は full-text で検証済=妥当、ただし過度に clean**(§2)。正しくは「**gating ∧ delta の連言が必須**」で、gate 付き additive(GLA/xLSTM)も delta 単独(ungated DeltaNet)も崩壊。"only gated delta-rule" は **Kimi/KDA 反例**で要限定(勝者は Gated DeltaNet 特定構成)。
3. **llcore の現時点 linear-native ベストが更新**: 6/26 は「忠実 Gated DeltaNet セル(head-wise scalar)」。今回 **Gated DeltaNet-2(2605.22791, erase/write 分離)が RULER NIAH 最強**として登場 → 定数 state を保ったまま recall を最大化する linear-native の到達点を更新。
4. **競合がアーキ層で収斂**: 「**gated-delta 線形 + 3:1 ハイブリッド**」が業界デフォルト化(Qwen3.5 / Kimi Linear / xLSTM-distill / HALO が独立着地)。6/26 の `reference_low_memory_llm_wave`(小型 dense+量子化が主役)は**アーキ層で時代遅れ**。llcore の「Qwen 線形化」value prop は新規デプロイ用途で**コモディティ化**。
5. **RoPE の前提が揺らぐ**: T2 は「RoPE 厳密 = LoLCATs path の強み」と置いたが、**Lizard・LAWCAT が独立に RoPE を除去**し、ゲート/再帰累積積が位置を担う方が**長文脈で優る**(LAWCAT は RoPE 有で 3K 崩壊を本文実測)。→ 長文脈路線では RoPE 保持は資産でなく**負債になり得る**。
6. **TPTT は触れ込みと裏腹に不採用**: T2 が「Qwen2.5-1.5B 最近接」と期待したが、本文では当該ケースが**劣化**かつ**長文脈ベンチ皆無**(§3)。

---

## 2. ★additive-vs-gated 検証 verdict(T2 核心主張は妥当か)

**verdict: 妥当(refinement 付き)。確信度: 高(2504.14366 本文 full-text 照合)。**

### (a) 引用正確性 — 完全一致
T2 の「直接引用」2 文は 2504.14366 abstract と **verbatim 一致**(本文照合済)。誤引用・捏造なし。論文メタ(Haller/Golde/Akbik, HU Berlin, 140M–1.7B, 7 アーキ, 10B tokens)も T2 記載通り。

### (b) 機構主張 — 妥当だが過度に clean、正しくは「連言必須」
Table 3(S-NIAH-1 pass-key @10B tokens)の実数値が示す load-bearing な精緻化:

| Model | 分類 | 512 | 1k | 2k | 4k |
|---|---|---|---|---|---|
| **Gated DeltaNet** | gated+delta(head-wise scalar α) | 99.4 | 97.8 | **81.8** | 29.8 |
| xLSTM | **additive**+gated | 95.8 | 78.0 | 25.2 | 8.4 |
| DeltaNet | delta, **ungated** | 98.8 | 96.2 | **0.0** | 0.0 |
| Kimi/KDA | gated+delta(channel-wise diag α) | 33.4 | 7.4 | 2.0 | 0.8 |
| GLA | **additive**+gated | 10.6 | 1.0 | 0.0 | 0.0 |
| Linear Attn | **pure additive** | **0.0** | 0.0 | 0.0 | 0.0 |

1. **「additive」= outer-product additive *update family*** であって「gate 無し」ではない。**GLA・xLSTM は gate 付きでも additive ゆえ崩壊**(gating は saturation を遅らせるが防がない)。
2. **delta 単独(ungated DeltaNet)も 2k で 0.0%**。→ **長文脈 recall には gating ∧ delta の連言が必須**。Gated DeltaNet のみ 2k/4k で生存。
3. **"only gated delta-rule" はやや寛大**: 同じ gated-delta でも **Kimi/KDA(channel-wise diag gate)は 2.0%@2k と惨敗**。実勝者は **Gated DeltaNet(head-wise scalar α)に限定**。
4. **scope**: SmolLM2 teacher・FineWeb・3 段蒸留・NIAH/S-NIAH のみ。hybrid/SWA は**未検証**(著者明記)。Gated DeltaNet ですら 4k(29.8)や S-NIAH-3(UUID, 1.2%@2k)で崩れ、teacher KV-cache には遠く及ばない=「maintain precision」は**相対的**。

独立 corroboration(abstract レベル): DeltaNet 2406.06484(additive→delta で AR 改善)/ Gated DeltaNet 2412.06464(gating=高速消去 ∧ delta=的確更新の補完)/ TTT 2407.04620(更新則が長文脈律速)/ Hedgehog 2402.04347(feature map 改善は additive 天井を破らない=境界づけ、refute でない)。

### (c) llcore 含意 — 妥当・要強化 + T2 §4.2 S5 の要修正
- **T2 §3.2 の honest 警告は完全に validate、むしろ強めるべき**: llcore 現 student `LinearAttention(diag/full)` = 論文の **Linear Attn = 全長 0% NIAH**。additive gap は **scale で広がる**(14%@140M→20%@1.7B)。**T2 §5 caveat #3「0.5–1.5B は範囲外」は部分的に誤り** — 本論文は 140M–1.7B を実測しており **llcore scale は範囲内**(de-risk されると同時に結論は additive に不利)。
- **★最大の指摘 = T2 §4.2 S5 の修正**: S5 は「Liger key→gate / gated-delta 更新則」を**並置**し「加法 saturation 回避の唯一の本質策」とするが、論文上 **Liger 流 gate-without-delta(GLA family)は不十分**(GLA は 1k で崩壊)。**支持されるのは gated-*delta* アームのみ**。→ llcore の長文脈アームは既実装の **忠実 Gated DeltaNet セル(data-dep α_t/β_t・head-wise = 論文の勝者構成に一致)へ routing すべき**で、**Liger gate-only は長文脈 recall の解にしない**(Liger は downstream 品質・効率には有効、needle retrieval には不可)。
- **plateau null との整合**: 6/26 memory の past_block_gain≈0 は**静的ゲート・chunk=block=128(勾配 truncate)**の gated-deltanet で測ったもの。論文の Gated DeltaNet は **data-dependent gate + 全長訓練**で別物 → **矛盾しない**。むしろ 2504.14366 は llcore の保留実験「忠実データ依存 gated-delta + chunk>128」を動機づけ、recall が ~2k へ伸びると予測。

---

## 3. 新着リード採否(6/26 以降、本文確認ベース)

5 本を arXiv 本文で精査(survey②)。**corpus 2026 追加(Patched-DeltaNet 2605.27992 / Exact Linear Attention 2605.18848 / CART 2606.01495)は off-target**(時系列・from-scratch アーキで pretrained-LLM 線形化でない)。

### ★llcore が今すぐ取り込む価値がある TOP-2

**TOP-1: LAWCAT(2509.18467, 本文確認)** — 北極星(constant state で長文脈)に最も直撃。
- 手法: **causal depthwise Conv1D(kernel r+1=4)を q,k → normalized GLA**(正規化分母の保持が安定性に critical)。既定で**完全線形(softmax 残置なし)**。
- 実績: Mistral-7B を **1K 長で蒸留 → passkey >90% を 22K まで汎化**、token 予算 passkey 93M/<0.1% pretrain。**Llama3.2-1B teacher 込み**(S-NIAH-1 100%@1-4K/80%@8K)。LoLCATs は 2K 超で ~0 崩壊と明示比較。状態 = dk×dv 定数。
- **★最重要発見: RoPE は長文脈に有害** — RoPE 無し版は 1K→8K で精度維持、RoPE 付きは 3K 超で崩壊。「recurrence が位置を内在化、明示位置符号は不要」。**prereg §5-4「RoPE 処理未確定」を一次情報で埋める**。
- LoLCATs path との関係: **強力な補完**(2 段骨格を保ちつつ SWA を Conv1D+正規化 GLA に差し替え、constant memory のまま recall 回復)。1K 蒸留=5090/CPU 予算に最適。

**TOP-2: Lizard(2507.09025, 本文確認)** — 現 LoLCATs Step1 の**回復レシピ上位互換**を同 ~40M token で提供。
- 手法: **GLA(ゲート Γ=σ(Wx))+ Anchor Window Attention(w=128 SWA + m=4 学習可能 meta-memory token)**、feature map=Hedgehog、**RoPE を線形経路から除去しゲート累積積 ∏Γ が相対位置を代替**。2 段(注意出力 MSE 20M + LM-CE+LoRA 20M)。**Llama-3.2-1B/3B ablation 込み**。
- 実績: 5-shot MMLU は Mistral-7B 60.8(teacher 62.4, −1.6)/ **50% hybrid 65.1(−1.5)**。RULER(hybrid)4K 92.5/8K 91.2/16K 85.2/32K 81.3 ≈ teacher。
- **★honest 内訳注意**: 「+9.4/+24.5pt」は **teacher 比でなく他線形化手法比**(vs LoLCATs 51.4 / Liger-GLA 36.3)。**最良長文脈数値は 50% softmax hybrid(= constant memory でない、KV 増大)**。純線形版は passkey 完全想起だが訓練 2048・評価 8192 止まり。
- LoLCATs path との関係: **補完**(同 2 段+SWA hybrid 骨格に gating と meta-token を足す上位版)。

### 補欠・不採用(理由つき)

- **LoLA(2505.23666, 本文確認)= 採用見送り、ただし必読の診断証拠**: 訓練不要で LoLCATs に被せる 3 メモリ系(SWA + sparse global + 線形状態)、**self-recall error SRE** で想起不能 KV だけ sparse cache に退避。**LoLCATs base 0.6% → LoLA 97.4%**(S-NIAH-1@4K)。**★LoLCATs path の recall 壊滅(0.6%)を定量化する一次証拠**。honest: sparse cache が O(λ·d) 追加(λ→768)= **厳密 constant memory でなく bounded に緩和**(論文も自認)。→ **コア採用でなく recall 診断軸 + 安価な推論時オプション**。
- **TPTT(2506.17671, 本文確認)= 結果レシピ不採用**: softmax を**置換せず** linear(DeltaProduct=Householder 積 gated-delta)を**並列注入** `o=α·o_lin+(1−α)·o_base`。★T2 が「Qwen2.5-1.5B 最近接」と期待した点を本文が裏切る: (1) 既定 α=0.5 では **softmax を捨てず O(L²)・KV 残=constant memory にならない**、(2) **Titans-Qwen2.5-1.5B は base より劣化**(PEM 0.500/0.583 vs base 0.598/0.690)、abstract の "+20% rel" は Llama-3.2-1B の EM 0.246 vs 0.007=退化指標、(3) **長文脈ベンチ皆無**。著者自身「preliminary」連呼。→ **DeltaProduct を feature map に据える発想と OSS パイプラインの工学参照のみ**(`tptt` PyPI 公開)。
- **Component-Aware Self-Speculative Decoding(2605.01106, abstract のみ)= 直交**: hybrid LM の SSM/線形部分を内部ドラフトに self-speculative。**parallel hybrid α=0.68 / sequential hybrid α=0.038(18× 差)**。北極星(メモリ効率)に非直結=推論加速。将来 llcore が hybrid を作るなら「**parallel 合成を選べ**」の設計示唆のみ。確信度低(無名著者群、前提モデル要実在確認)。

---

## 4. plateau を動かす機構の現ベスト + prereg `plateau_full` で確かめる点

### 4.1 plateau を支配する 3 軸(効き目順、一次総合)
**更新則の表現力 ≳ 訓練時 end-to-end credit assignment ≫ state 容量**。

1. **更新則の表現力(第一軸・linear-native で実装可)**:
   additive(最弱・不可逆 saturation, 2504.14366)< **gated-delta(誤り訂正、16k→32k に押すが破らない)** < **TTT-Linear(内側 1-SGD step)** < **TTT-MLP / MesaNet / Atlas(内側最適化を厚く)= plateau を破る**。
   → **linear-native の現ベスト = Gated DeltaNet-2(2605.22791, erase/write 分離、RULER NIAH 最強)** を線形 student の既定 mixer に。これが「**北極星=定数 state を保ったまま recall を最大化**」する到達点。**ただし gated-delta は plateau を破らない**(TTT-E2E が示す天井)。
2. **訓練時 end-to-end credit assignment(第二軸・llcore の confound そのもの)**:
   TTT-E2E の "E2E" = **訓練時 meta-learning で内ループ更新を通し長文脈を end-to-end 逆伝播**。llcore の **TBPTT-128-detach はこの軸を殺している** → past_block_gain≈0 が機構天井か訓練切断かが**未分離**。
   - 一次根拠: DeltaNet 並列化(2406.06484)— **chunkwise の chunk_size はタイリングのパラメータで勾配は訓練系列全長を流れる(recurrence と数学的に等価)**。→ 標準 chunkwise の credit assignment は **chunk size でなく訓練系列長**で決まる。llcore の「chunk=block=128 + state detach」は **credit を 128 で切る非標準の弱い訓練レジーム**= confound。
3. **state 容量(第三軸・副次)**: StateX/SSE/head-merge は recall(NIAH +16pt)を上げるが、Atlas が容量を「online 更新性・管理表現力」と分離する通り**容量単独では plateau を破らない**。6/26 memory の「StateX は容量を足すだけで未解決」を一次支持。

> **★honest 警告(採否の binding constraint)**: plateau を破った証拠(TTT-E2E)は **from-scratch・164B tokens**。llcore は **Qwen 蒸留(~40M〜数 B tokens, 単一 32GB)**。2504.14366 の "state resolution > distillation budget" と合わせると、**蒸留予算を増やしても additive 天井は破れない=機構を変えるしかない**が、**「蒸留で gated-delta/TTT セルの plateau がどこまで動くか」は完全未測**。164B(=LoLCATs の約 4000×)が要るなら llcore 射程外。**ここが採否を分ける**。

### 4.2 prereg `plateau_full` で確かめる点(優先順、全て compute-matched・held-out)
指標 = 「per-position loss vs context length(monotonic 減少=活用 / plateau=未活用、LaCT 2505.23884 / TTT-E2E 定義)」+ S-NIAH/RULER/passkey。

1. **【最優先】credit-assignment と容量の分離(confound を潰す唯一の実験)**: state detach を外し**訓練系列全長を full backprop**(chunk_size は単なるタイリング=64 等)、**train_seq_len ∈ {256,512,1024,2048} ≫ 128** で再測。動けば既往 null は**訓練アーティファクト**、動かなければ **gated-delta 静的機構の架構天井確定**。**正しい操作は「chunk_size>128 単独」でなく「detach 解除 × seq_len 掃引」**(6/26 memory の「chunk_size>128」記述を修正)。
2. **更新則ラダー(機構天井の定量)**: 容量・credit を固定し mixer のみ替える。additive < 忠実 Gated DeltaNet(既実装 `ttt.py`)< **Gated DeltaNet-2 型(erase/write 分離)** < TTT-Linear セル(内側 1-step)。
3. **容量制御(StateX 流、副次)**: 機構・seq_len 固定で state size のみ掃引(credit を正した上で二次レバーか確認)。
4. **hybrid SWA の寄与切り分け**: `WindowLinearAttention` on/off で窓由来の局所 recall を線形 state の手柄に読み替えない対照。
5. **蒸留 vs from-scratch の予算ギャップ(採否の決め手)**: 同じ gated-delta セルを (a) Qwen 蒸留 と (b) 小規模 from-scratch で plateau 指標比較。**動かなければ「llcore は定数 state での会話品質回復は狙えるが長文脈 recall plateau 突破は射程外」と honest 確定**。

**落とし込み**: 採用機構の現ベスト = **Gated DeltaNet-2 型セルを NAS allele 既定**、**長文脈アームに TTT-Linear セルを第三 rung 追加**。ただし plateau 突破証拠は from-scratch・大トークン限定ゆえ、実験 #1(detach 解除×seq_len)で **null が機構天井か訓練切断かを最初に分離**し、#5 で蒸留予算の壁を実測してから「plateau 突破」を語る。それまで honest に主張できる上限は「gated-delta で plateau を**緩和**(16k→32k 級)」まで。

---

## 5. 競合地図更新 + llcore 差別化軸

### 5.1 ★この 6ヶ月の構造変化
**「gated-delta 線形 + 3:1 ハイブリッド(4 層に 1 層だけ full attention)」が業界デフォルトに収斂**。Qwen3.5・Kimi Linear・蒸留系(HALO / xLSTM-distill)が独立に同じ箱に着地。`reference_low_memory_llm_wave_2026_06`(Gemma4/Hermes 等=小型 dense+量子化)は**アーキ層で時代遅れ化**。

llcore にとって**追い風かつ最大の脅威**:
- 追い風 = T2 結論の S5(gated 機構)が「将来アーム」でなく**主流が選んだ正解**に。LoLCATs→gated-delta 方針は正しい。
- 脅威 = **Qwen 自身が Apache-2.0 の gated-delta 小モデル(0.8B/2B/4B)をオンデバイス最適化済で配布** → 「Qwen2.5 を自分で線形化する」value の大半が新規デプロイ用途で**コモディティ化**。

### 5.2 競合 1 行地図(≤6ヶ月優先)

| # | 主体 / 名称(時期) | 何を | 状態 | llcore との関係 |
|---|---|---|---|---|
| 1 | **Qwen3.5 Small 0.8/2/4/9B**(Alibaba, 2026-03) | gated-delta + full の 3:1、<2GB VRAM、Apache-2.0(<35B) | qwen.ai 一次 / 小型は二次(HF 要確認) | **正面衝突**: llcore 射程をほぼ包含。ただし 3:1=full 層残=**KV 線形増(定数でない)** |
| 2 | **Kimi Linear / KDA**(Moonshot, 2025-10, 2510.26692) | Gated DeltaNet を細粒度ゲート拡張、MLA と 3:1、NoPE | HF paper 一次 | gated-delta 最前線。**NoPE 位置処理**が RoPE 移植問題の回答例。窓外(8ヶ月)だが基盤 |
| 3 | **xLSTM 蒸留(HALO 系)**(JKU/NXAI, 2026-03, 2603.15590) | Llama/Qwen/Olmo を xLSTM ハイブリッドへ蒸留、expert merging stage | arXiv abstract 一次 | **最直接の技術競合**(Hochreiter 本家が同一タスク)。token 数・小モデル成績は本文要精査 |
| 4 | **HALO + HyPE**(清華 THUNLP, 2026-01, 2601.22156) | Transformer→RNN-attn hybrid 蒸留、**Qwen3 を 2.3B tokens(<0.01%)で変換**、新位置符号 HyPE | arXiv abstract 一次 | 直接競合。題名「Hybrid Attention via **Layer Optimization**」= **llcore 唯一の新規軸(層別 NAS)と名称衝突** → 本文で「探索 or 固定」を一次確認必須(novelty 侵食リスク) |
| 5 | **SubQ**(Miami startup, 2026-05, $29M seed) | 独自 SSA、12M context、NIAH 92.1%@12M 主張 | **未検証**(論文/重み/査読なし、ソース自ら懐疑) | frontier 規模・クローズド=別セグメント。**誇張の反面教師、数値引用しない** |
| 6 | **RWKV-7 "Goose" 2.9B**(2025, ICLR25) | **真の定数メモリ/定数 per-token**、vector-gating | OpenReview 一次(窓外) | 「完全定数状態」の正典。北極星に最も近い既存実装(ただし Qwen 線形化でも CPU 特化でもない別系譜) |
| 7 | **Falcon-H1R 7B**(TII, 2026) | Transformer–Mamba 並列 hybrid、48K | 二次 | 7B=サイズ帯上だが「hybrid でオンプレ効率」で被る |
| 8 | **Hermes Agent**(Nous, 2026-06, MIT) | オンプレ自己改善エージェント | 二次(効果自称) | **llive の正面競合**(llcore でなくエージェント層)。オンプレ波の象徴 |

### 5.3 llcore の被り / 空白 / 差別化軸

**被り(コモディティ化)**: 「Qwen 小型を線形化して定数寄り state に」「gated-delta+SWA で recall 補強」「蒸留でほぼ無損失変換」は全て Qwen3.5/Kimi/HALO/xLSTM-distill が実装済 → **T2 の S1–S5 はもはや差別化でなく追従**。HALO は **2.3B tokens で Qwen3 変換**=llcore 想定より洗練。

**空白(まだ無人)**:
1. **真の定数状態(KV 非増加)× 競争力品質**: 主流 3:1 は full 層残で **KV 線形増**(Qwen3.5「40% 減」/Kimi「最大 75% 減」=定数でない)。完全定数で品質を保つのは RWKV-7 のみ(Qwen 由来でも CPU 特化でもない)。**「Qwen 由来 × 完全定数 × CPU オンプレ」の交点は無人**。honest 警告: 2504.14366 通り完全定数は state 解像度天井=長文脈 recall とトレードオフ。
2. **定数状態制約下の層別 NAS**: 先行は固定ヒューリスティック(全員 3:1 均等)。**ただし HALO "Layer Optimization" が侵食リスク** → 本文で「探索 or 固定」一次確認が必須。
3. **CPU ネイティブ完全オンプレ + honest 計測/gate**: SubQ(クローズド・誇張)、Hermes(自称)等ベンチ不透明が業界の癖 → llcore の capability-gate / cliff 実測 / verified-plasticity / honest disclosure は**構造的差別化として依然有効**。
4. **TTT / credit-assignment(plateau 本命)**: 競合 8 件の誰も「block_size 付近 plateau の BPTT 越え credit assignment」を扱っていない。gated-delta 波と直交する**研究差別化の余地**(リスク高だが無人)。

**差別化軸(優先順)**:
- **A. 「定数状態の純度」を旗印に(被りを反転)**: 主流 hybrid は KV が増える。llcore は「**増えない**」を honest に計測軸化(context-sweep × needle で「定数だが天井あり」を正直開示)。Qwen3.5 を**ベースライン兼比較対象**に「3:1 は定数でない」を一次で示すのが最も説得力。
- **B. インフラ/計測/gate 層で勝つ**: モデルでは勝てない(Qwen が Apache 配布)が、honest gate + cliff 実測 + verified-plasticity は構造的余地。
- **C. 層別 NAS は HALO 一次確認後に再評価**: 衝突なら novelty を「**定数状態制約下**の Pareto 探索(5-shot MMLU + 長文脈 + メモリ定数性)」へ絞る。
- **D. 商用ライセンス純度 / 新ベース検討**: Qwen3.5 小型が Apache-2.0(<35B、二次=HF LICENSE 要確認)なら `feedback_qwen_commercial_barrier` 懸念が **Qwen3.5 系では解消** → llcore は **Qwen3.5-0.8B/2B を新ベース**に乗り換える選択肢を検討(現 0.5B/1.5B 固執の見直し)。

---

## 6. 未確認・要一次検証(honest 留保)

1. **TTT-E2E「full attn 超え ppl」はブログのみ=未確認**。abstract は「**同様にスケール(parity)**」止まり(本セッション再確認済)。
2. **Gated DeltaNet-2 は abstract のみ**(本文未精読)。RULER NIAH 改善の絶対値・hybrid vs recurrent 内訳は本文要確認。
3. **蒸留予算下での plateau 可動性は全手法とも未測**(from-scratch 証拠のみ)。llcore 実験 #5(§4.2)で初めて埋まる。
4. **Kimi/KDA の低スコア原因**(2504.14366 Table 3 で 2.0%@2k)が実装・ハイパラ依存か本質か不明(論文が mechanistic 分析を欠く=著者明記の limitation)。
5. **競合の二次情報どまり**: Qwen3.5 小型 4 機種の正確なラインナップと **<35B=Apache-2.0**(乗り換え判断の前提)、Falcon-H1R 数値、Hermes 学習ループ効果(自称)。
6. **SubQ 数値は明示的に未検証**(論文・重み・査読なし、ソース自ら懐疑)→ 数値引用しない、誇張の反面教師。
7. **HALO 2601.22156 が層別配置を「探索」するか「固定」か = 本文一次確認必須**(llcore 層別 NAS の novelty 侵食リスクの核心)。
8. **RoPE 除去の llcore 適用**: Lizard/LAWCAT は RoPE 除去+ゲート位置が長文脈で優ると本文実測。llcore は「RoPE 保持(LoLCATs path・短中文向き)」と「RoPE 除去+ゲート位置(LAWCAT/Lizard・長文脈向き)」を**別アームで分離測定**すべき(未着手)。
9. **corpus 2026 追加 3 本(Patched-DeltaNet/Exact Linear Attn/CART)は off-target**(時系列/from-scratch)=本件に不採用。

---

## Sources(一次情報、検証レベル付記)
- **本セッション独立再確認(abstract)**: TTT-E2E https://arxiv.org/abs/2512.23675 / Gated DeltaNet-2 https://arxiv.org/abs/2605.22791
- **本文 full-text 照合**(survey①): What Matters in Linearizing https://arxiv.org/abs/2504.14366
- **本文 HTML 確認**(survey②): TPTT https://arxiv.org/abs/2506.17671 / Lizard https://arxiv.org/abs/2507.09025 / LAWCAT https://arxiv.org/abs/2509.18467 / LoLA https://arxiv.org/abs/2505.23666
- **abstract 確認**(survey③): TTT 原典 https://arxiv.org/abs/2407.04620 / LaCT https://arxiv.org/abs/2505.23884 / Gated DeltaNet https://arxiv.org/abs/2412.06464 / Atlas https://arxiv.org/abs/2505.23735 / Titans https://arxiv.org/abs/2501.00663 / MesaNet https://arxiv.org/abs/2506.05233 / TTT≈linear-attn https://arxiv.org/abs/2602.21204 / StateX https://arxiv.org/abs/2509.22630 / DeltaNet 並列化 https://arxiv.org/abs/2406.06484
- **competitive(qwen.ai 一次 + arXiv abstract)**(survey④): Qwen3.5 https://qwen.ai/blog?id=qwen3.5 / Kimi Linear https://huggingface.co/papers/2510.26692 / xLSTM 蒸留 https://arxiv.org/abs/2603.15590 / HALO https://arxiv.org/abs/2601.22156 / RWKV-7 https://openreview.net/forum?id=ayB1PACN5j
- **未検証(反面教師、数値引用しない)**: SubQ https://www.technologyreview.com/2026/06/19/1139313/
- 接続: T2 = `D:/projects/fullsense/docs/research/linearization_recipes_2026-06-28.md`(§3.2 / §4.2 S5 / §5 caveat #3 を本 refresh が更新)、prereg = `prereg_linearization_distill.md`(§5-4 RoPE / plateau_full)、6/26 landscape memory = `project_llcore_efficient_arch_landscape_2026_06_26`

---

## ★memory 更新案(`project_llcore_efficient_arch_landscape_2026_06_26` への追記、main が適用)

```
## 2026-06-28 refresh(4-survey 統合、一次再確認 2 件)
- **plateau 本命=TTT に一次証拠付与**: TTT-E2E(2512.23675, 3B/164B, 本セッション abstract 再確認)が「Gated DeltaNet/Mamba2 は context scaling せず TTT-E2E は full-attn 同様にスケール、128K で 2.7×」を実証。精緻化: **gated-delta は plateau を緩和(16k→~32k)するが破らない**。破るのは TTT-E2E の訓練時 meta-learning(end-to-end credit assignment)。「full 超え ppl」はブログのみ=未確認。
- **T2 additive-vs-gated 検証 verdict=妥当(refinement)**: 2504.14366 本文照合で「gating∧delta の連言必須/gate 付き additive(GLA/xLSTM)も delta 単独も崩壊/"only gated delta-rule" は Kimi-KDA 反例で要限定=勝者は Gated DeltaNet 特定構成」。**llcore scale(0.5-1.5B)は論文の 140M-1.7B 実測範囲内**(T2「範囲外」は誤り)。**T2 §4.2 S5 修正: Liger gate-only は長文脈 recall の解にならない→忠実 Gated DeltaNet セルへ routing**。
- **linear-native 現ベスト更新**: 忠実 Gated DeltaNet → **Gated DeltaNet-2(2605.22791, NVlabs, erase/write を channel-wise 別ゲート分離, 1.3B/100B で RULER NIAH 最強, abstract 再確認)** を NAS allele 既定に。長文脈アームに TTT-Linear セルを第三 rung 追加。
- **plateau confound の正しい操作を訂正**: 「chunk_size>128 単独」でなく **「state detach 解除 × train_seq_len {256..2048} 掃引」**(chunkwise の chunk_size はタイリング、勾配は系列全長を流れる=2406.06484)。これが機構天井か訓練切断かを分離する最優先実験。蒸留予算で plateau が動くかは全手法未測(TTT-E2E 証拠は from-scratch 164B=llcore 射程外の懸念)。
- **新着 TOP-2 採用**: LAWCAT(2509.18467, 1K 蒸留→22K 汎化, 完全線形, Conv1D+正規化 GLA, **RoPE は長文脈に有害=3K 崩壊を一次実測**→prereg §5-4 を埋める)/ Lizard(2507.09025, GLA+meta-token, 回復レシピ上位互換, 1B/3B ablation 込)。**RoPE 保持 vs 除去を別アームで分離測定**。不採用: TPTT(Qwen2.5-1.5B が base 劣化・長文脈未実証)、LoLA(recall 診断軸のみ、sparse cache が定数性緩和)。
- **競合地図**: 「gated-delta 線形+3:1 hybrid」が業界デフォルト化(Qwen3.5/Kimi/HALO/xLSTM-distill)→ Qwen 線形化 value はコモディティ化。reference_low_memory_llm_wave は時代遅れ化。残る白地=(1)完全定数状態(KV 非増加)の純度、(2)定数制約下の層別 NAS(★HALO 2601.22156 "Layer Optimization" が名称衝突=本文で探索/固定を一次確認必須)、(3)honest gate/計測、(4)Qwen3.5-0.8B/2B 新ベース乗り換え検討。
```
