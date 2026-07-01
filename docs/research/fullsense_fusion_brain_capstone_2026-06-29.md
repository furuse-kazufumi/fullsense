# FullSense 統合アーキ capstone — 脳構造 × モデル融合 × 最初の PoC (2026-06-29)

> **これは何**: 同日の 2 ワークフロー — `model-fusion-deepdive`(wylzjj2vv, 8 agents, frontier 全文検証 + 具体レシピ + TRIZ/異分野)と `brain-structured-fullsense`(w2li8t45p, 7 agents, 脳 6 原理マッピング) — を実行可能な 1 枚に統合。
> **詳細正本**: `model_fusion_landscape_2026-06-29.md`(融合手法地図)/ `brain_structured_fullsense_2026-06-29.md`(脳マッピング)/ `option_b_verification_poc1_novelty_2026-06-29.md`(P7 天井)/ memory `project_fullsense_unified_model_vision`(北極星)。
> **規律**: `feedback_benchmark_honest_disclosure`(脳インスパイアの衣装を殺す)/ `feedback_llm_value_is_solution`(実用解)。

**一行**: 「全く別のモデルを融合して 1 つに」+「脳構造を目指す」の honest な答えは収束する ── **退屈だが正しい backbone(FuseChat-3.0 流 implicit 多教師蒸留)+ CLS 3-store アーキ(hot/cold split)+ 1 つの defensible 工夫(interference-staging rule)+ 安く falsify できる net-new 2 本(T1 operator-union / X1 CDMA)**。それ以外は narrative。

---

## 1. 2 ワークフローの収束(と見かけの緊張の解消)

| 論点 | fusion deep-dive | brain workflow | 統合判定 |
|---|---|---|---|
| breadth の system アーキ | #3 hot/cold split(in-state dense core + 外部 recall) | CLS 3-store(新皮質=重み / 海馬=llive / WM=定数状態) | **同一物**。Schlag fast-weight 容量限界=P7 が外部 store を必然化 |
| sleep/consolidation | KILL list:「→ continual-KD / DER++」(機構として非新規) | #1「唯一の新機構」だが closest prior art=DER++/生成 replay・novelty=medium は**三つ組**ゆえ | **収束**: sleep=**採用すべき既知ツール(DER++ interleaved replay)**で逐次多教師蒸留の忘却対策。機構新規性は無い |
| 真に net-new | #1 T1 operator-union write-rule / #2 X1 CDMA 割当 | (脳枠は機構を生まないと自認) | **T1/X1 が唯一の medium novelty**。固定 state に「より多く詰める」かを問う |
| 退屈な正解 | FuseChat-3.0 IMF + WRPO(backbone) | 「暗黙多教師蒸留は既に動く、脳枠は置換せず 2 つ足すだけ」 | **一致**: backbone は forced・low-novelty、compute はここへ |

**緊張の解消**: 「sleep が新機構」(脳)と「sleep は DER++」(fusion)は矛盾しない ── sleep/DER++ は**逐次蒸留の忘却対策として採用**する既知ツールであり、**機構新規性は T1/X1 にしか無い**。両者は別レイヤーの話。

---

## 2. ★FullSense 統合アーキ(脳構造を北極星に据える)

```
  WAKE(online)          海馬 / episodic = llive 外部 4 層メモリ(疎・1-shot・retrieval, HippoRAG 写像)
  入力・教師I/O ───────► rare / teacher-specific / long-tail はここに残す(governed store)
                              │ surprise ‖v−Sk‖ が promote-gate(Approval Bus = fail-closed)
                              ▼
  SLEEP(offline)        consolidation stage = DER++ interleaved logit-replay
                        頻出 episode + 記録済み teacher logit(Qwen/GLM-MIT/JP)を INTERLEAVE 蒸留
                        ★interference-staging rule: 「旧 softmax 模倣(O2)」と「教師へ寄せる融合」は
                          同一 optimizer step を共有させない(別 warm-start)= 収束の鍵
                              ▼
  constant state        新皮質 / 遅い意味重み = llcore(有界 state, Schlag 容量上限=P7)
  (working memory)      delta-rule 書込 + 疎/準直交キー(既に Gated DeltaNet ベース内)
                        ここには cross-teacher COMMON な dense 構造だけを詰める(long-context recall は詰めない)
```

**両 north star を同時に満たす規則**(P7 が予算ルール):
- **memory-efficiency**: 有界 state に詰めるのは FFN-resident な instruction/reasoning/knowledge/JP(MMLU の data-parity penalty は ~2–4pt のみ)。**long-context recall(8–16k の cliff)は詰めない=効かない** → llive へ offload。
- **multi-teacher fusion**: 異 arch/tokenizer は weight で混ぜられない(AC/DC 同 base 制約・HeteroFusion の崩壊・FusionRoute の同 tokenizer 要求が三方向から再確認)→ **black-box text-level IMF が唯一路**で student の mixer(softmax/linear)に非依存。

---

## 3. 実行レシピ(本命 = linearize-first, fuse-last)

詳細は fusion deep-dive 出力に。骨子:
- **C1 データ**: 各教師(Qwen=math/code/anchor, GLM-MIT=reasoning, JP specialist=和知識/style、**全て MIT/Apache** で商用クリーン)が K 応答生成 → RM scoring → `sft.jsonl`/`dpo.jsonl`(vocab 整列・logit 不要=tokenizer/arch 非依存)。
- **S0/S1 warm-start**: O1(出力 MSE, **既に distill.py 実装済**)→ O2(attention 分布 CE, Hedgehog)+O3(block hidden)を**凍結 Qwen base 相手に**。
- **S2 joint(net-new composition)**: 単一 CE で linearization 回復(O5)+ IMF 融合 SFT を同時(両方 next-token CE=融合データが回復コーパス)。**★interference-staging rule**: O2(旧 attention 模倣)と融合(教師へ寄せる)は逆向き → **同 step に混ぜない**(別 warm-start に分離)= 「fusion×constant-state を 1 段で」収束させる defensible contribution。
- **S3 WRPO DPO**: best/worst pair で源-標的マージン重み付け(1 教師に collapse させない)。
- **C4(OFF 既定)**: GLM/JP の cross-tokenizer white-box は BLD(byte head, 蒸留後除去=O(1) 維持)で attempt 可だが **linear student 未検証・byte-to-byte で −21 MMLU 警告** → ablation のみ。
- **llcore 接点**: `distill.py` 拡張(O2/O3/logit-KD/joint)+ 新 `runtime/fusion.py`(imf_dataset/wrpo_loss/teacher_router)+ **4 軸 eval gate**(A 短中 Δnll / B long-context recall / **C 定数状態 purity=peak KV bytes が文脈長で flat=北極星 gate** / D 融合 capability が no-fusion baseline を超え C を退行させない)。

---

## 4. ★net-new spike(安く falsify、勝てば S2 に採用)

固定 state は **bounded additive outer-product (Σvkᵀ) fast-weight 連想記憶 + delta-rule**(Schlag 2102.11174)= sketching/VSA/CDMA は比喩でなく文字通りの「詰め方」。**複数 pretrained を 1 つの constant recurrent state に融合した公刊は無い**(MoE-SSM 系は from-scratch state)。

- **#1 T1 — Operator-Matched Write-Rule Fusion**: 教師アンサンブルの実効 attention 演算子(key→value)を student の write rule(`S+=β(v−Sᵀk)kᵀ`)に蒸留。「融合 = どう書くか」で state は固定 d×d。**multi-teacher operator の UNION を 1 つの線形 write rule に**が未公刊スライス。closest=LoLCATs/MOHAWK(単一教師)。
- **#2 X1 — CDMA 直交コード多重化**: 各教師に準直交 spreading code を与え bind→write、read で query と相関分離。**P7 を明示・割当可能に**。closest=Cheung 2019「Superposition of many models into one」(feedforward, recurrent state でない)。
- **CPU PoC(1 日)**: 合成 **multi-source MQAR**(dim-64 Gated-DeltaNet student, 2 つの凍結 disjoint-table softmax 教師)で **operator-matching(T1)+CDMA(X1)vs logit-KD** を recall@capacity 比較。**勝てば S2 の fusion loss に採用、負ければ kill して FuseChat-3.0 IMF 単独**。どちらでも勝ち、コストは CPU 1 日。

---

## 5. ★honest 評価(これが核)

- **退屈な答え(§3 IMF レシピ)が正解で、compute はここへ**。mostly FuseChat-3.0 verbatim、実際の gap(世界知識・JP)を突く。唯一の arch 固有の工夫=interference-staging rule は defensible で安く検証可。
- **「fusion × constant-state」を novel 研究 thread にするのは distraction**。だが **time-boxed CPU spike(T1/X1)としては安く・gap は本当に開いている**ので 1 回回す価値あり(勝てば S2 の自由 param を埋める)。**P7 は out-engineer できない、allocate するだけ**。
- **脳構造を目指す**は「新機構の源」としては inspirational、「選別・組立・統治の発見的手法」としては生産的。硬い実利は ①「resident MoE を作るな」(負の知見)② CLS 3-store が llcore+llive+offline を 1 枚に束ねた ③ surprise/consolidation-gate/ignition が Approval Bus に写る(framing)。
- **frontier 4 本は実在だが推奨を覆さない**: AC/DC=oracle Coverage 頼み・param 数(constant-state でない)/ HeteroFusion=hypernet transfer(weight-merge でなく蒸留=再確認)/ FusionRoute=ensemble(反 O(1))/ **BLD だけが cross-tokenizer bridge として OFF 既定 ablation 価値**。

---

## 6. ★推奨 first step(CPU・並行可)

1. **Recipe backbone proof**: `runtime/fusion.py` に `imf_dataset`+`teacher_router`、local Qwen2.5-0.5B/1.5B で K=4 応答(remote GLM/JP は stub)→ heuristic score → `sft.jsonl`/`dpo.jsonl`(schema valid + best≠worst を assert)。+ **axis-D held-out scorer** で現 O1-linearized 0.5B の **no-fusion baseline(融合が超えるべき数値)を記録**。
2. **Novel-angle falsification(別ファイル・state 非共有)**: multi-source MQAR で T1 operator-matching + X1 CDMA vs logit-KD → recall@capacity。1 日で S2 採否決定。
3. **(brain leg)** sleep/DER++ の interleaved-replay 忘却対策は (1) の逐次教師アームに同梱(baseline=素朴逐次が教師A を忘れることをまず実測、honest gate=勝因が RAG か consolidation か)。

**next_plan(1 行)**: `llcore fusion: runtime/fusion.py の IMF plumbing(C1)+teacher_router(C2)+axis-D baseline を CPU で確立し、並行して multi-source MQAR で operator-matching(T1)+CDMA(X1) vs logit-KD を falsify。勝てば S2 fusion loss に採用、負ければ FuseChat-3.0 IMF 単独で GPU 段(e2e fusion SFT+WRPO DPO ~20–40M tok, rented)へ。breadth は CLS 3-store hot/cold(llive 外部 recall + Approval Bus 統治)で別途設計。C4(BLD byte-bridge)は OFF 既定 ablation。`

---

## 7. 未検証・留保(ruthless)

- **三つ組(sleep + 有界 constant-state + multi-teacher)+ T1/X1 は「公刊が見つからない」であって「存在しない」ではない** → 外部 novelty 主張前に focused prior-art sweep。
- **constant-state student の merge/operator-union が機能する保証なし**(§4 spike がまさにこれを試す、仮定しない)。
- **P7 容量上限は廃止不可**: 2 大教師を小 state に無損失では詰められない。超過は llive へ offload=その "fusion" は実質 RAG → honest gate で内訳分解必須。
- **on-prem purity の緊張(開示)**: deployed student は CPU/on-prem だが**教師生成 pass は rented GPU/cloud teacher 呼び出しが要る** → purity は student に適用、生成 step には適用しない(or FuseChat-3.0 公開データ再利用)。
- **frontier 数値**: AC/DC Table は WebFetch summarizer 経由の二次情報(PDF で要再確認)/ HeteroFusion は未再現(~0 citation)/ BLD は linear student 未検証。
- **post-cutoff papers(title/abstract のみ)**: Gated DeltaNet-2 2605.22791 / Routing Mamba 2506.18145 / Distilling-to-Byte 2602.01007 等は内部主張未確認。"Retrieval-Aware Distillation 2602.11374" は**未検証=引用禁止**。
- **JP specialist のライセンス/入手性**(Sarashina/Qwen3-4B-JP class)は依存前に要再確認。
- **llcore 接地(本セッション確認)**: `distill.py`(6.2KB)は O1 のみ(fusion/dpo/logit_kd 無し)=greenfield。`nas_pareto/eval/longctx_eval/linearize/ttt` + `Qwen2.5-0.5B/1.5B-Instruct` 在存。

---

## 8. ★Firming update(敵対 prior-art + 理論導出, WF wudmz9dmh 6 agents, 2026-06-29)

§4 の net-new 2 本と §3 の境界・§3 の staging を一次・敵対検証して**精緻化**(調査のみ)。

### 8.1 net-new の確定
- **T1(operator-union write-rule)= FIRMED(medium, killer 無し)**。3 leg は pairwise 占有も **triple(多教師 UNION × attention-operator × DeltaNet write rule)の交差は genuine gap**。firmed-by-structure(両親分野が 2026 も活発ゆえ交差の持続的空白が意味を持つ negative)。差別化 cite: **Attention-to-Mamba 2604.14191 + Taylor-Calibrate 2606.16429**(単一教師 operator→linear、これを ensemble に一般化)/ **FuseChat 2408.07990**(多教師だが output-level、これを operator 階層へ降ろす)。
- **X1(CDMA)= DOWNGRADED → application-only novelty**。機構は occupied folklore(Frady/Kleyko VSA-in-RNN 1803.00412 / CDMA↔VSA MAC framing 2111.06077 / Schlag 2102.11174 / Cheung 2019 1902.05522 / Task-Projected HDC 2004.14252)。**「発明」と呼ばない**。残る slice=「per-teacher コードで蒸留中に bounded linear-attn student state を teacher 別 allocate」のみ=実装技法。**naive shared-write 比較 ablation で勝てなければ CDMA framing を捨てる**。
- **staging-rule = ADOPT(既知)+ 小 empirical**。要訂正: 絶対形「同 optimizer step を共有してはならない」は**誤り**(PCGrad/CAGrad は gradient surgery で対立勾配を co-train 可)→「default。cos≥0 なら merge 可、attention-MSE 回復 vs 融合は cos<0 で stage、recovery-CE vs 融合は cos≥0 で merge 可」の cosine-gated recipe + ablation に軟化。

### 8.2 ★in-state↔external 境界の計算ルール(physics=high confidence)
bounded state W=Σvkᵀ(d×d 連想記憶)。容量則は VSA / 統計物理 / linear-attn で収束:
- **SNR = d/M**(M=格納連想数, Frady 2018)。
- **信頼容量 N_assoc ≈ d/(2·ln d)**(McEliece/Clarkson)、error-tolerant ~0.138d(Hopfield)、hard ceiling ≤ d。
- **使える数値**: d=64 → ~8 / d=128 → ~13 / d=256 → ~23(信頼)。512→~41, 1024→~74, 2048→~134。
- **hot/cold 閾値**: top **r\* ≈ d/(2 ln d)** を HOT(in-state)、rank>r\* を llive へ。**頻度形**: probability-mass share < **(2 ln d)/d** を cold(d=128 なら ~7.7% 未満)。**recency 形**: Gated DeltaNet 忘却 λ ≈ 1−(2 ln d)/d。
- **regime**: HOT=bounded state(線形容量 O(d/log d), dense 高頻度共通知識)/ COLD=llive softmax/kNN store(指数容量 ~2^{d/2}, long-tail/factual/polysemous)。
- confidence: 法則と「線形 vs 指数の cut」=high、定数は band d/(2–7 ln d)、数値頻度 cutoff=medium、「rare/polysemous→cold」=high。

### 8.3 post-cutoff 確定(5/5 実在)
**★capstone の「2602.11374 引用禁止」は overturned = 実在で引用可**。Retrieval-Aware Distillation for Transformer-SSM Hybrids(2026-02-11): retrieval-critical Gather-and-Aggregate head ~2% を model 内に残し他を recur → state 8× 縮小・net 5-6× memory。**境界アーキの partial prior art に再分類**。差別化: 私は cut を **d/log d 容量則から導出**し cold を **llive 外部**へ routing(2602.11374 は dedicated head で in-model 保持)。**2603.22056 Dual-Space KD**(cross-tokenizer)= T1 の多教師 cross-tokenizer mechanics の partial prior art=tokenizer-alignment baseline として cite。Routing Mamba 2506.18145 / Distilling-to-Byte 2602.01007 / MossNet 2510.26182 も real。

### 8.4 ★first-PoC を変更(X1 でなく T1 主導)
1. **2-3 教師の attention operator の ensemble を 1 つの DeltaNet/Gated-DeltaNet student に蒸留**(Taylor-Calibrate/Attention-to-Mamba の init を multi-teacher に一般化)。
2. bounded state を**容量則でサイズ決定**(d/(2 ln d) ≥ 目標 hot-association budget となる d)、long-tail は (2 ln d)/d cutoff で llive へ。
3. 単一教師 operator→linear baseline + **2602.11374**(retrieval-offload hybrid)に対し明示差別化。
4. **X1 の per-teacher CDMA は ablated variant**(coded vs naive shared write)として、headline でなく付帯。staging も同様に ablation-backed の design choice。

**更新 next_plan(1 行)**: `llcore fusion PoC は T1 主導に変更: 2-3教師の attention operator を 1つの (Gated)DeltaNet student に ensemble 蒸留(Taylor-Calibrate/Attention-to-Mamba を多教師一般化)、state 幅は容量則 d/(2 ln d)≥hot予算で決定、long-tail は (2 ln d)/d 頻度 cutoff で llive 外部へ。baseline=単一教師 operator→linear + 2602.11374(retrieval-offload)。X1 CDMA と cosine-gated staging は ablation 付帯(naive 共有 write/joint+surgery に勝てねば捨てる)。FuseChat-3.0 IMF backbone は不変、GPU 段は rented。`

> **⚠ §9 が §8.4 の「T1 主導」を SUPERSEDE する（下記 redirect）。**

---

## 9. ★T1 REDIRECT — 「正しい層か」の理論判定（WF wbgmo37m4 5 agents, high confidence, 2026-06-29）

§8 は T1（多教師 operator-union）を novel と firm したが、**novelty ≠ value**。「T1 は正しい層を狙っているか」を局在化文献で詰めた結果 **= REDIRECT(B)・high confidence**。理論で PoC 前に headline を補正。

### 9.1 判定（high）: 融合価値は FFN/output に住む
7+ の独立系列が収束: ① 知識局在=mid-layer FFN（ROME 2202.05262 / MEMIT 2210.07229 / Geva FFN=KV 2012.14913 / Knowledge Neurons 2104.08696）、attention=recall/copy/routing（induction 2209.11895 / retrieval heads 2404.15574=ablate で検索/CoT 崩壊も「intrinsic 知識は無傷」）。② **線形化レシピが答えを実装**: LoLCATs/MOHAWK/Mamba-in-Llama は例外なく **FFN を freeze** し attention を **single-teacher** MSE 蒸留、capability は別の FFN/logit 回復段で戻る = **operator は mixing/recall を運ぶが capability を運ばない**。③ 実在 fusion は全て FFN/output（FuseChat logit+DPO+param merge / BTX FFN→MoE・attention は平均 / Expert-Merging は深層 MLP）= **attention operator を teacher 間 union する前例ゼロ**。

### 9.2 T1 = REDIRECT(B)（(A) でも (C) でもない）
- **(A) でない**: operator-union は output/FFN fusion が運べないものを足さない（capability は operator に無い）。
- **(C)（両方）でもない**: multi-teacher operator-union は **recall に対しても misdirected** — ① teacher は各自 basis で attend → 正準 union 不在で fused-operator MSE target が**内部不整合** ② 有界状態の信頼連想数 ~**23(d=256)** に multi-teacher routing を詰めるのは容量と戦う ③ recall は計画上すでに llive へ外部化する次元。recall に要るのは **single-teacher operator 蒸留**（fusion でない）。
- narrow residual: teacher 間で in-context retrieval が違えば operator の**選択**は効きうるが、union でなく「最強 teacher の operator 選択 or HALO 流 selective full-attention 層保持」で扱う。

### 9.3 ★真の headline 貢献（機構でなく配置理論 + 統合契約）
operator-union は前例ゼロかつ理論的 misdirected ゆえ headline にできない。新規性は **placement rule + 統合契約**に置く:
> **容量導出 hot/cold 境界に基づく layer-targeted fusion contract** — どの teacher 価値をどの層に置くかを `d/(2 ln d)` 容量則で形式的に正当化し、CPU 完結・constant-state・JP-capable な linearized student として統合。
1. **operator = single-teacher**（LoLCATs/HALO 流 attention-transfer to Gated DeltaNet、FFN freeze。役割=efficiency + recall 保存のみ）。
2. **fusion = FFN/output**（FuseChat-3.0 logit-KD + DPO、任意で BTX/BAR/task-vector の FFN merge）= capability が住み非冗長な唯一の層。
3. **rare/world recall = llive 外部**（23-slot 容量則が形式的根拠）。

差別化の核 = **capacity-derived placement + llive co-design 外部化**であって operator-union ではない（過剰主張せず honest disclosure 整合）。

### 9.4 ★first-PoC を再変更（§8.4 を置換）: RIGHT question を測る
- **Step 0（ほぼゼロコスト well-posedness 診断・まずこれ）**: union target がそもそも存在するか。小 teacher 2 体の同一入力 attention 出力を取り「両者 mean を single linear-attention で MSE 一致させる irreducible floor」を測る。basis 非整合なら floor 大 → **学習前に operator-union は ill-posed と判明**。
- **Step 1（gain 分解 ablation）**: 小 base + teacher 2-3 体。(A) single-teacher operator linearization のみ=baseline / (B) A + output 多教師 KD / (C) A + operator-union(T1) / (D) A + 両方。recall-light reasoning/JP + recall-heavy で評価。**予測: capability で B≫A, C≈A(recall-heavy では C<A もあり), D≈B = gain は output fusion 由来・operator-union delta≈0**。これを commit 前の必須 gate に。

### 9.5 honest 留保
- A/B 直接実験は文献に**不在** → redirect は収束的 mechanistic 証拠 + operator-fusion 前例の不在に依拠（単一決定 study でない)→ §9.4 ablation を commit gate に（必須）。
- 分割は statistical（Geva 2023: 一部 head が subject→attribute / Hase 2023: 局在は編集位置を予測せず）。operator は capability-void でない（mixer 除去 >35,000x ppl）= single-teacher operator 蒸留は essential、軽視しない。redirect の主張は「operator が無価値」でなく「**teacher 間 capability 差は operator に無い**」。
- verdict-bearing 論文（2408.10189/2408.15237/2410.10254/2412.06464/2012.14913/2403.07816/2401.10491/2408.07990）は pre-cutoff・確認済で redirect は成立。RAD corpus は interpretability 未収録 → 上記 + 局在化 8 本を `raptor-rad-ingest` で取込推奨（`feedback_research_to_rad_autoingest`）。
