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
