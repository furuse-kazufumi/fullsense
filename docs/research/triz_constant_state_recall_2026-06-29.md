# TRIZ ideation 統合 — llcore 物理的矛盾「定数 state ∧ 任意過去 recall」(2026-06-29)

> **目的**: 4 本の TRIZ ideation(①時間/スケール分離 ②空間/条件分離 ③40 原理 sweep ④異分野アナロジー)を統合・重複排除し、(1)矛盾の定式化 (2)既存技術↔TRIZ 原理対応 (3)候補ランキング (4)最初の PoC (5)honest 留保 を 1 枚に確定する。
> **接続先(整合済)**: `efficient_arch_landscape_refresh_2026-06-28.md`(plateau 3 軸 / §4.2 prereg / §5.3 白地)/ `distill_protocol_and_differentiation_2026-06-28.md`(軸 A=CSC-NAS 生存路 / 軸 B=llive 外部化 / §4.3 serving wall)。実装接地 = `D:/projects/llcore/src/llcore/lm/ttt.py`(忠実 Gated DeltaNet セル)/ `runtime/distill.py`(蒸留・hook 拡張点)/ `scripts/evolve_linearization.py`・`nas_pareto.py`(NAS allele 追加点)— **4 ファイルすべて本セッションで実在確認済**。
> **規律**(`feedback_benchmark_honest_disclosure` / `feedback_verify_existence_before_claiming`): 各候補に確信度・出典・検証レベルを付す。本統合担当の検証レベル = **4 ideation の abstract 一次確認を継承**(本統合は arXiv 本文を独立再精読していない)。「未踏」は全員 absence-of-evidence(arXiv keyword/abstract 検索の recall 限界)に基づき確信度=中が上限。誇張禁止・未確認は明記。

---

## 1. 矛盾の定式化

### 1.1 物理的矛盾(physical contradiction)
llcore の定数 state は次を同時要求される:
- **小さく保つ**: KV 非増加・softmax ゼロ(完全定数 = 北極星・serving wall 解消の前提)。
- **大きく持つ**: 任意過去トークンの高精度 recall(associative recall / NIAH / passkey に十分な情報)。

固定サイズ連想記憶 `S = Σ kᵢvᵢᵀ`(d_k×d_v)は容量 ~d で頭打ち、新規書込が旧連想と**破壊的干渉**(state saturation, 2504.14366)を起こすため、長文脈で recall が崩壊する。

### 1.2 先行の回避策(= llcore が捨てたい逃げ道)
全先行は**矛盾を矛盾のまま回避**する:
- **softmax 層温存**(Qwen3.5/Kimi の 3:1 hybrid、SR-TTT/Tensor Cache/CoMeT の L1 softmax 窓)= KV 線形増 = 定数性を犠牲。
- **外部退避**(IndexMem/RetentiveKV/LoLA の sparse cache)= primary が softmax KV か O(λ·d) で定数でない。

→ **llcore の賭け = softmax を使わず pure-constant primitive 内部で recall を出す別解**。

### 1.3 理想最終結果(IFR)
**O(1) state のまま、必要なときに任意過去トークンの情報を高精度に取り出せる。**

### 1.4 TRIZ 分離原理による再フレーム(4 ideation の核心的収束)
定数 state の「バイト数」は時刻で変えられない。変えられるのは**アクセスの解像度(=計算)**と**書込先の構造**。よって矛盾は次の分離軸で攻める:
- **時間分離**(ideation ①③): ほとんどの時刻は安く、recall/consolidation 時だけ計算を burst して同じ定数 state から高解像度を引き出す。
- **空間分離**(ideation ②④): state を異質な副系(別 decay / 別 dynamics / 厳密スロット)に分け、干渉を構造で限定。
- **条件分離**(ideation ②③): 「将来どの query に読まれるか」で書込/忘却を変調。
- **動作内分離**(ideation ④): ダムな線形書込 + スマートな反復読み(エンコード/デコードの役割分離)。

---

## 2. 既存技術が暗黙に踏んだ TRIZ 原理(地図 — 「踏まれた原理」を避けて未踏を探す)

| 既存技術(出典) | 暗黙の TRIZ 原理 | 何を解決済 |
|---|---|---|
| TTT / Titans(2407.04620 / 2501.00663) | #25 セルフサービス(モデルが自分の state を学習) | **write 側** test-time 学習で更新則を強化 |
| Gated DeltaNet-2(2605.22791) | #34 排除と再生(erase/write channel 分離) | 単一スカラの erase-write tie を解消、RULER NIAH 最強 |
| Mamba / data-dependent gate | #15 動性化 + #3 局所的性質 | 入力依存ゲートで保持を可変化 |
| chunkwise 並列(2406.06484) | #1 分割 | recurrence を等価タイリング |
| MoM(2502.13685) | #1 分割 + #24 仲介(router) | token を複数 **homogeneous** memory に振り分け干渉低減 |
| Titans surprise | #22 災い転じて福(後向き予測誤差=記憶信号) | 驚いた過去を優先記憶 |
| Q-Delta(2606.08804) | #23 フィードバック(query 条件付き write) | 読みを意識した書込 |
| CCQ(2606.01294) | #2 引き出し(read step を分離) | **read 側を初めて開いた**が単発・解析的・非学習 |
| Do LMs Need Sleep / SleepGate(2605.26099 ほか) | #19 周期的作用 + #25 | offline consolidation(ただし wake 中 KV 保持=非定数) |

**★この sweep で判明した地形(load-bearing)**:
1. **write 側はほぼ飽和**(gate∧delta / erase-write 分離 / query-aware write / 容量拡張)。残る隙間は narrow。
2. **read 側が新前線**: CCQ(2606.01294)が「read step は手付かず=全 key が加法的に薄まる」を初指摘。だが**単発の解析操作**で、学習も反復もしない → **read 側の「反復/学習/test-time」は無人**。
3. **二層メモリ(window+archive)は softmax 窓に収斂**: SR-TTT/Tensor Cache/CoMeT が全員 L1 に softmax 窓を残し、退避を位置基準で行う → **「両層とも定数・softmax ゼロ・退避は忘却量/surprise 基準」は無人**。
4. **gate は全部「現 token 条件付き(後向き)」**: 「将来 query 条件付き(前向き)」の write gate は無人。

---

## 3. ★候補ランキング(統合 = 4 ideation を重複排除しクラスタ化)

4 ideation の 17 案を 7 クラスタに統合した。**3 つの独立 ideation 手法(異分野 CS / 40 原理逆転 / 時間分離)が同一案に収束したものを最優先**とする。各候補の評価軸 = (a)適用原理 (b)本当に未踏か(一次確認・収束元) (c)llcore 実装難度★ (d)CPU 先試 (e)CSC-NAS 生存路/serving wall 適合。

### 【TOP-1・flagship】Test-time 反復 READ 最適化(凍結定数 state への賢い復号)
**収束**: ideation ① 案4(read-time deliberate recall)+ ③ 案A(test-time READ=#13 逆転, 各 flagship)+ ④ ①(圧縮センシング→unrolled ISTA read, flagship)+ ④ ②(count-min robust read)。**3 手法独立収束 = 最強シグナル**。

- **(a) 適用原理**: #13 逆転(write 側 TTT の逆 = read 側学習)× #24 仲介(反復 retriever)× #25 セルフサービス(read 側)× #1 分割(エンコード/デコード役割分離 = 動作内分離)。**IFR 直撃**: O(1) state を「ダムな線形 CS 測定」と見なし、query 時のみ反復で疎復元/連想 cleanup して特定 value を高精度抽出。
- **(b) 未踏か**: **CCQ(2606.01294)が read 側を開いたが単発・解析的・非学習・非反復**。TTT/Titans/Atlas は全て **write 側** test-time 学習。「pure-linear 定数 state への decode-time 反復/学習 read 最適化」「圧縮再帰 state を CS 測定行列と見なし unrolled ISTA/Hopfield cleanup で疎復元」は **abstract 検索で直接先行未検出(確信度=中、検索 recall 限界あり)**。**最近接競合 = FDM(2604.07716, 単著未査読)の Holographic Reference Beam Decoding**(read-time 変調だが単発+particle cache 272 slot 併用)。
- **(c) 実装難度=中(推論側中心)**: read path に小反復 module(K=3–5 step、low-rank read adapter or query 摂動 + soft-threshold)を足すのみ。**write は一切変えない = 既存 student/state にそのまま被せられる**。難所 = ground-truth key 無しで成立する自己教師 read 目的の設計(snap-to-codebook / readout 低エントロピー化 / forward-inverse consistency が候補)。
- **(d) CPU 先試=◎(最適・最安)**: **state 追加ゼロ・訓練不要**。凍結 gated-delta state に対し query を 1–5 step 反復し recall@{2k,4k,8k} を A/B。単一 CPU 数時間。
- **(e) 生存路適合=◎(最良)**: **state を一切増やさない = 純度(軸 A)を完全無損**。新 cell を足さない = **GGUF/serving wall を構造的に悪化させない**(推論ループのみ)。CSC-NAS の cliff 地図に「read 最適化で cliff がどれだけ動くか」の新次元を追加。
- **★honest risk**: 2502.05164(read=DAM 上 1 勾配ステップ=softmax Hopfield)が「**1 step が最適**」を示唆 → 多 step 不要で**理論的に null に潰れうる**。非 softmax エネルギーで underdetermined な読みに事前制約(疎性/codebook)を足して初めて gain。**この潰れやすさ自体が最良の falsifiability**(安価に棄却可能)。

### 【TOP-2】Anticipatory 書込ゲート(future-queriability で write/forget を変調)
**収束**: ideation ② 案1(anticipatory-retention gate, flagship)+ ① 案1(recall-prioritized consolidation, 教師後向き attention oracle)+ ③ 案C(前向き future-queriability 補助目的)。**3 手法独立収束**。

- **(a) 適用原理**: #10 先取り作用(query 前に書く)× #11 事前保護 × #3 局所的性質(解像度を非一様配分)× #23 フィードバック(future-query 予測誤差で駆動)× #25。
- **(b) 未踏か**: 既存ゲート(Mamba/GLA/Gated DeltaNet/RWKV-7/FoX/**Titans-surprise**)は**全て「現 token の key/value/surprise」条件付き = 後向き**。本案の条件軸「この情報は将来どの query に読まれるか」は**前向きで直交**。教師 Transformer は oracle を持つ(後続トークンが過去のどこに attention したか = 実際に recall された位置)→ 蒸留ターゲット化。RAG の query-rewriting/store-routing は**外部メモリ**で定数 recurrent state に適用例なし。**「定数 state セルで future-query を書込ゲートに入れた先行は未検出(確信度=中)」**。最近接 = **Titans(後向き surprise)/ Birdie(2411.01030, RL 目的混合・双方向)** → 差別化軸(前向きラベル監督 vs RL 目的混合)の load-bearing 性は本文要確認。
- **(c) 実装難度=低〜中**: 既存 gated-delta セルに小 head `Q̂_t=g(h_t)`(次 w query 方向を予測)を追加、書込ゲート β_t / 忘却ゲート α_t を `align(write_key, Q̂_t)` で変調。**自己教師補助損失**(teacher forcing で未来 query は既知 = 追加データ不要)。`distill.py` の `_capture_layer_io` を拡張し teacher 後向き attention 行列も hook。最大コスト = **Qwen GQA/QKV-bias での attention hook 割当**(両研究 docs 共通の未確認事項 = distill §5 #4)。
- **(d) CPU 先試=◎(最安)**: tiny 2–4 層 d=128 で MQAR / selective-copy に「近 needle vs 遠 needle 混在」を課し、補助損失 on/off で遠 needle recall 比較。
- **(e) 生存路適合=◎**: **標準 gated-delta セル上の加算 = GGUF 経路を壊しにくい**。`distill.py` 直挿し = 蒸留パイプライン(D1 段)に最小摩擦で統合。教師 oracle = 蒸留と思想一致。

### 【TOP-3】Purity-preserving twin 定数 state(忘却量 routed archive、softmax ゼロ)
**収束**: ideation ③ 案B(purity-preserving twin state, surprise-routed)+ ② 案4(twin-state online CLS consolidation)+ ① 案2(結合カスケード leaky-bucket)+ ④ ⑤(LSM-tree tiers, 隣接)。**4 ideation 全員が触れた最広収束**。

- **(a) 適用原理**: #22 害→信号(忘却が捨てる残差を retrieval index 化)× #34 排除と再生 × #7 入れ子(fast ⊃ slow)× #3 局所的性質(段ごと別 decay)× #4 非対称性(可塑性非対称)。
- **(b) 未踏か**: fast state(GDN-2, recency)+ slow state(固定サイズ VQ/連想 codebook, archive)。fast の**忘却ゲートが上書きする残差の大きさ**を surprise 信号とし閾値超だけ slow に sparse write、線形 consolidation op で結合。**両層とも定数・softmax/KV ゼロ**。**SR-TTT(2603.06642)/ Tensor Cache(2605.22884)/ CoMeT(2602.01766)/ Do LMs Need Sleep(2605.26099)は全員 L1 に softmax 窓を残し退避は位置基準**。Titans は単一 memory に圧縮(第二定数 store に分離せず)。mGRADE(2507.01829)は fast+slow 並列だが**無結合**(消去質量の下方移送なし)。**「忘却量 routing × 両層定数 × softmax 完全ゼロ × 明示 consolidation op で結合」の交点は未踏(確信度=中)**。**軸 A(純度)を機構として体現する唯一の案**。
- **(c) 実装難度=中〜高**: 二 state 相互作用・VQ 訓練安定性・routing 閾値学習。`ttt.py` の gated-delta セルを K=2 本 + 安価線形 consolidation op(chunk 境界適用、chunkwise 並列保持)。NAS allele(`evolve_linearization.py`/`nas_pareto.py`)に「cascade depth K・decay 比・結合ゲート」を追加。**hard routing は非標準 = serving 注意、soft 版なら標準セルの和で GGUF 経路維持**。
- **(d) CPU 先試=○(クリーン ablation)**: 意図的 state collision を起こす MQAR(同一 slot に多 key)で routing 有無の recall 差、結合カスケード vs (i)同 total-state 単一 gated-delta (ii)無結合 multi-decay heads を NIAH 2k/4k/8k 比較。**支配しなければ honest null も公表価値**。
- **(e) 生存路適合=○(soft 版)〜△(hard 版)**: 軸 A の旗印「定数のまま階層化」を直接実装。soft 版で GGUF 維持。HiPPO(単一 state 最適圧縮)を正直 baseline に併置すべき。

---

### 下位ティア(統合後・正直に降格)

| クラスタ | 収束元 | 一行評価 | 確信度 | 降格理由 |
|---|---|---|---|---|
| **D. 異質時間スケール routing** | ② 案2(predicted-temporal-scope routing)/ ① 案2 一部 | token を**内容でなく予測時間射程**で heterogeneous-decay バンクへ動的 routing。MoM(homogeneous)・固定 multi-timescale SSM の交点で未踏寄り(確信度=中) | 中 | **自明収束リスク**(全 token を遅バンクへ退化)→ load/timescale バランス正則化必須。soft 版を NAS allele 化可 |
| **F. 可変深度 consolidation tick** | ① 案3(adaptive-depth tick)/ ② 一部 | chunk 境界で再構成誤差 ∝ K_t 回の内ループ更新。**最も混雑**(Do LMs Need Sleep / SleepGate / Elastic-TTT が近接、全員 KV 保持 or 固定 N)。novelty narrow | 中-低 | **価値は novelty でなく「plateau 起源分離を CPU 予算で測る装置」** = 両研究 docs §4.2 #1(detach 解除×seq_len)の operationalize。**研究 instrument として高戦略価値・novelty bet ではない** |
| **E. 厳密ピンスロット / 冗長 sketch** | ② 案3(bounded exact-recall register)/ ④ ②(count-min)③(SDM Kanerva) | 固定 m 厳密スロット + 損失 working state、or 冗長複製+min/median robust read。厳密 O(1) で exact needle | 中 | **混雑**(GSA 2409.07146 / MoM / Product-Key / LoLA が区画占有)。離散 admission 非微分(Gumbel/STE 不安定)。**非標準セル = serving wall 悪化**。GSA/MoM 本文確認まで降格 |
| **G. Kalman 自己不確実性→外部 escalate** | ④ ④ | 定数 state の共分散で「内部解像不能」を検出し llive 外部 4 層メモリへ escalate | 中(write 側既知 MesaNet 2506.05233 / read-time routing は細い刃) | **研究 novelty 細(RAG 重複)、システム/製品差別化が主**。distill §3.2 軸 B(llive 外部化)を read-time signal で実装する位置づけ |

**棄却(不採用)**: スペクトル帯共振読出し(② 案5、安定性・検証コスト過大・未踏一次確認未完)/ LSM-tree 厳密 tier(④ ⑤、階層 memory 飽和 = MKA/MELODI/Compressive Transformer 占有、定数性厳密化のみが差)/ Reservoir Computing(反面教師 = ランダム固定 state は fading memory で精密 recall 構造的に不可、①〜③の「学習アドレス/構造化読み必須」を支持する負の根拠)。

---

## 4. ★最初の PoC(CPU 可・最小・反証可能)

**選定 = TOP-1(Test-time 反復 READ)を最初に回す。** 理由: state 追加ゼロ・訓練不要・推論のみ = **CPU 最安かつ最速で falsifiable**、純度無損で生存路に最適、3 手法独立収束、そして「1-step 最適で潰れる」理論リスクゆえ**安価に棄却もできる**(投機を最小コストで決着)。

### PoC-1: 凍結 gated-delta state への単発 vs 反復 read(state 追加ゼロ)
**問い**: softmax を温存せず、定数 state の **read 側 test-time 最適化だけで** associative recall が出るか。

**手順(最小)**:
1. **state を作る**: `ttt.py` の忠実 Gated DeltaNet セルで tiny model(2–4 層, d=128)を合成 MQAR + S-NIAH-1 passkey で学習。**訓練系列長 512–2048、state detach を解除して full backprop**(両研究 docs §4.2 #1 の confound をこの段で混入させない)。学習後 state を**凍結**。
2. **read を比較(FLOP-matched)**:
   - **R0**: 単発線形 read(= 現状ベースライン)
   - **R-ISTA**: state S を CS 測定行列と見なし K∈{3,5} step の unrolled soft-threshold 疎復元(NOODL 流 linear+soft-threshold のみ、微分可能)
   - **R-Hopfield**: K step の連想 cleanup(snap-to-stored-value energy descent)
   - **R-CCQ**: 単発曲率収縮(2606.01294 再現)= 「**反復は本当に要るか**」の対照
   - **R-CountMin**: R∈{2,4} 本の独立射影副 state に冗長書込 + soft-min 集約(④ ② の最小版、state は R 倍だが系列長 O(1))
3. **指標**: recall@{2k,4k,8k} を K(read 反復数)の関数として。**ベースライン必須 = FDM / MoM / 単発 CCQ**(④ の honest 警告 = cross-domain は FDM が先行、実装ベースラインに置かねば「新規」と言えない)。
4. **対照(confound 潰し)**: **SWA 窓を一切使わない**(両研究 docs §4.2 #4 = 窓由来の局所 recall を線形 state の手柄に読み替えない)。

**判定ルール(事前登録)**:
- 反復 read(K=3–5)が **単発 R0 かつ 単発 R-CCQ を CI 超で上回る** → read 側 test-time にシグナルあり → 学習 read adapter + スケールアップへ。
- gain 無し(= 1-step が最適、2502.05164/FDM リスク顕在) → **honest null「線形定数 state では read 反復は無効、read 側 test-time は dead」を公表**し即棄却 → TOP-2(anticipatory write gate)へ pivot。

**コスト**: 単一 CPU 数時間。state 追加ゼロ・訓練(tiny)1 回のみ。

### PoC-2(fast follow): Anticipatory write gate(TOP-2)
PoC-1 が null でも独立に価値。同 tiny harness + `distill.py` に補助損失 `L_aux = Σ‖Q̂_t − sg(q_{t+1..t+w})‖`(teacher forcing で追加データ不要)、近/遠 needle 混在 MQAR で補助損失 on/off の遠 needle recall を比較。**PoC-1 と直交**(A=賢く読む / B=賢く書く)ため、両方 gain なら合成可能。

---

## 5. honest 留保(どれが投機的か / 無人 = 機会か既知不可能か)

1. **「未踏」は全て absence-of-evidence**: 4 ideation の判定は arXiv keyword/abstract 検索(total_results 1–4 と薄い)依存。priority 主張前に **Semantic Scholar / Connected Papers / OpenReview で TOP-1/2/3 を再検索必須**。確信度は全候補**中が上限**。
2. **TOP-1 の自己教師 read 目的が機能するか未検証**: snap-to-codebook が有望だが PoC 未実施。**1-step 最適(2502.05164)で潰れる理論リスクを明記** = 最大の投機点だが最安で決着可。
3. **TOP-2 は Birdie/Titans に思想近接**: 差別化(前向きラベル監督 vs 後向き surprise / RL 目的混合)の load-bearing 性は本文要確認(③ 確信度=中〜低)。
4. **TOP-3 が単一 GDN-2 を有意に超えるか未検証**: 2504.14366 の state 解像度天井ゆえ絶対 gain 小の可能性 → honest null も成果。
5. **全候補に binding な天井**: いずれも「定数 state の recall **天井を緩和/地図化**」であって **plateau 突破ではない**。突破証拠(TTT-E2E 2512.23675)は **from-scratch 164B = llcore 蒸留予算(~40M〜数 B)射程外**。2504.14366「state resolution > distillation budget」が binding。**「破った」と書かない**。
6. **測定の前提(両研究 docs と整合)**: どの案も効果測定前に **state detach 解除 × train_seq_len 掃引**(refresh §4.2 #1)で「機構天井か訓練切断か」を分離しないと null/偽陽性が confound する。**異常に良い NIAH が出たら window 由来の局所 recall を線形 state の手柄に読み替えていないか(§4.2 #4)を先に疑う**。
7. **serving wall(distill §4.3)との整合**: 非標準セルは llama.cpp/GGUF native kernel 無し = 配れない。**TOP-1(state 追加ゼロ)> TOP-2(標準セル加算)> TOP-3 soft 版 > TOP-3 hard/E(非標準)** の順に生存路適合。研究核は falsifiable な TOP-1/2、軸 A 体現は TOP-3、軸 B(llive 外部化)接続は G。
8. **abstract のみ(本文未精読)**: CCQ 2606.01294 / FDM 2604.07716 / Gated DeltaNet-2 2605.22791 / OVQ 2602.03922 / SR-TTT 2603.06642 / Tensor Cache 2605.22884 / MoM 2502.13685 ほか。機構詳細・数値は本文 + GitHub(FDM `YasongFan/FDM`, MoM `OpenSparseLLMs/MoM`)で着手前最終確認。FDM は単著・未査読・主張過大 = **数値鵜呑み禁止**だが cross-domain 最近接競合として必引用。

---

## next_plan 候補(claude-projects.json `next_plan` / memory 反映用、1–3 行)

> **llcore 研究方針(CSC-NAS 生存路維持 + 新規軸)**: write 側が飽和した今、未踏前線 = **READ 側 test-time 最適化**(CCQ が単発で開いたのみ)。最初の PoC = 凍結 gated-delta state(`ttt.py`)に対し単発 read vs K-step 反復 read(ISTA/Hopfield cleanup/CountMin)で MQAR・S-NIAH recall@{2k,4k,8k} を CPU 比較、**state 追加ゼロ = 純度(軸 A)無損・GGUF 経路無傷**。FDM/MoM/単発 CCQ をベースライン必須、SWA 窓由来 recall を線形 state の手柄にしない対照を入れる。gain 無(1-step 最適 = 2502.05164 リスク)なら honest null で即棄却し TOP-2(anticipatory future-queriability write gate, `distill.py` 直挿し・標準セル・教師 oracle)へ pivot。いずれも plateau 緩和/cliff 地図化であって突破ではない(蒸留予算 < state 解像度天井, 2504.14366)。

---

## Sources(4 ideation の一次確認を継承、arXiv ID)
- **read 側前線**: CCQ 2606.01294 / FDM 2604.07716(単著未査読・数値要再検)
- **write 側飽和**: Gated DeltaNet 2412.06464 / Gated DeltaNet-2 2605.22791 / DeltaNet 並列 2406.06484 / Q-Delta 2606.08804 / Kaczmarz 2605.08587 / MesaNet 2506.05233
- **二層/consolidation(softmax 窓温存)**: SR-TTT 2603.06642 / Tensor Cache 2605.22884 / CoMeT 2602.01766 / Do LMs Need Sleep 2605.26099 / SleepGate・Elastic-TTT・mGRADE 2507.01829
- **routing/容量/VQ**: MoM 2502.13685 / OVQ 2602.03922 / SSE 2507.16577 / GSA 2409.07146 / PICASO 2502.17605 / Titans 2501.00663 / Atlas 2505.23735
- **異分野**: SDM↔attention 2111.05498 / Universal Hopfield 2202.04557 / Neural Bloom Filter 1906.04304 / LoLA 2505.23666 / 1-step read 2502.05164
- **天井制約**: 2504.14366(additive 0% NIAH / state 解像度 > 蒸留予算)/ TTT-E2E 2512.23675(plateau 突破は from-scratch 164B)
- **接続**: `efficient_arch_landscape_refresh_2026-06-28.md`(§4.2 prereg / §5.3 白地)/ `distill_protocol_and_differentiation_2026-06-28.md`(軸 A CSC-NAS / 軸 B llive / §4.3 serving wall)
- **実装接地(実在確認済)**: `D:/projects/llcore/src/llcore/lm/ttt.py` / `runtime/distill.py` / `scripts/evolve_linearization.py` / `nas_pareto.py`
