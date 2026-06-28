# Pre-registration — PoC-1: 凍結 constant-state からの test-time 反復 READ で long-context recall が出るか

- **日付**: 2026-06-29
- **status**: `pre-registered`(CPU 実行可・GPU 不要。実装は TDD)
- **由来**: TRIZ ideation TOP-1(`triz_constant_state_recall_2026-06-29.md`)+ 1-step 最適リスクの一次検証(verdict (c)→(b) 条件付き有望)
- **位置づけ**: 北極星の核心 feasibility 問題「**softmax を使わず constant-state primitive のみで実用 long-context recall が出るか**」(= TRIZ 物理的矛盾 定数状態 vs recall)への**最初の実証的一手**。literature では決まらない(= novelty の負担が『新規性』→『実現可能性実証』に移った=landscape memory)。
- **honest 規律**: `feedback_benchmark_honest_disclosure`。**「突破」と書かない**(plateau 突破は from-scratch 164B=TTT-E2E=射程外、本 PoC は cliff 地図化/緩和の検証)。

> **凍結宣言**: 仮説・主要指標・成功基準・baseline・ablation・失敗モード監視を実装前に固定。走らせてから指標・閾値・arm を選び直さない。null も削除せず記録。

---

## 1. 背景と理論 gate(一次検証で確定)

- 凍結した線形/gated-delta state `S = Σ kᵢ vᵢᵀ`(連想記憶行列、O(1) memory)から query `q` の単発 read は `q·S`(線形・閉形式)。
- **「1-step 最適」定理は線形 state に存在しない**(2502.05164 Thm3.1 は softmax/DAM・球面台・L→∞ 限定)。CCQ(2606.01294)は read 側を単発 contraction `(I−λΣ)q` で開いた(反復・学習なし)= read 側は未回収 lever。FDM(2604.07716, 単著・経験値)/2502.05164 とも「反復は無益」を線形 state については証明していない。
- **★真の gate = 「decode 時に key 辞書が既知/構造化か」**(検証の核心、CS/連想記憶の原理):
  - `n ≤ d_state` かつ直交 key → 単発線形 read で厳密(反復無益)。
  - **`n > d_state`(線形が softmax に負ける長系列域)+ sparse target + 低 coherence key + 辞書既知** → underdetermined、**非線形反復(ISTA/OMP/Count-Min)が単発線形 read を原理的に上回りうる**。
  - 辞書未知(任意連続 key)→ ill-posed、**素朴反復は bulk 平均へ収束**(2502.05164 Fig.5 の罠)。
- ∴ PoC-1 は **key 辞書が既知/有限な設定(MQAR 語彙 key / 学習 codebook)** で、`n > d_state` の sparse 域に絞って検証する。

---

## 2. 仮説(falsifiable)

- **H1(主仮説)**: 既知 key 辞書の下で、凍結 constant-state からの **非線形・反復 read**(R-ISTA / R-Hopfield-cleanup / R-CountMin)は、**単発線形 read(`q·S`)および CCQ 一発 contraction を、`n > d_state` の sparse recall(MQAR)で CI 上有意に上回る**。
  - 成功: recall@{n>d_state 域}で反復 read の 3-seed 平均が baseline 群を bootstrap 95% CI 下限 > 0 で上回る。
- **H2(非線形が gain 源・ablation)**: gain は反復そのものでなく**非線形**(soft-threshold / cleanup の非線形性)に由来する。**線形のみの反復は null**(線形合成=線形・二次形式は閉形式 → 改善なし)。
  - 成功: 非線形反復 > 線形反復 ≈ 単発、が CI で分離。
- **H3(辞書 gate)**: 辞書既知条件で出た gain は、辞書未知(任意連続 key)条件では消える/bulk 崩壊する。
  - これは gate の正しさの確認(既知→well-posed / 未知→ill-posed)。

> 事前予想(honest): verdict (b) 条件付きより、**辞書既知 × n>d_state × sparse で小〜中 gain は出る公算、辞書未知では null〜崩壊**と予想。gain が出ても「long-context recall を解決」とは言わず「**この well-posed 域で単発線形 read を超える**」に限定。

---

## 3. 実験デザイン

### 3.1 タスク(key 辞書が既知)
- **MQAR(Multi-Query Associative Recall, 合成)**: key-value ペアを既知有限語彙から生成、後段で複数 query。**key 集合=辞書として decode 時に既知**(gate を満たす)。系列長で `n`(格納ペア数)を制御し `n vs d_state` を掃引。
- **S-NIAH(single needle, 補助)**: 文脈中の needle 1 本。辞書は「候補トークン集合」。MQAR が主、S-NIAH は汎化確認の副。
- **★SWA 窓は使わない**(窓由来 recall を線形 state の手柄にしない=検証の指摘)。

### 3.2 モデルと state
- 忠実 **Gated DeltaNet**(`src/llcore/lm/ttt.py` の data-dependent α/β cell)、tiny(2–4 層 / d=128 / state 次元 d_state を {64,128,256} で振り `n vs d_state` を作る)。
- TBPTT は **state detach 解除 × seq_len{512,1024,2048} 掃引**(truncation 交絡を避ける=landscape refresh の指摘)。学習後に **state を凍結**して read 法のみ比較。

### 3.3 read arm(FLOP-matched で比較)
| arm | 内容 | 種別 |
|---|---|---|
| **R0**(baseline) | 単発線形 read `q·S` | baseline |
| **R-CCQ**(baseline) | CCQ 単発 contraction `(I−λΣ)q`(λ=学習ゲート) | baseline |
| **R-ISTA** | 既知辞書 Φ に対し unrolled ISTA(soft-threshold)K step | 提案(非線形反復) |
| **R-Hopfield** | energy descent + 非線形 cleanup K step | 提案(非線形反復) |
| **R-CountMin** | 既知候補集合を query する sketch 風復元 | 提案 |
| **R-linear-iter**(ablation) | 非線形を除いた線形のみ K step | ablation(H2、null 予測) |

- **FLOP-matched**: 反復 K step の総 FLOP を R0/R-CCQ と概ね揃える(または FLOP を横軸に Pareto)。

### 3.4 baseline / 対照(必須)
- 単発線形 read(R0)・CCQ 一発(R-CCQ)を**必ず並置**。
- 辞書未知条件(任意連続 key)を **H3 用の対照**として走らせ、gain が消える/崩壊することを確認(gate の検証)。

---

## 4. 測定指標と監視

- **主要指標(事前指定・1 つ)**: **recall accuracy@(n>d_state 域)**(MQAR の query 正答率)。`n ≤ d_state` 域は well-posed すぎて差が出ない予測なので、主張は `n>d_state` sparse 域で。
- **副次**: recall vs n/d_state 比の曲線、FLOP-recall Pareto、S-NIAH recall。
- **★失敗モード監視(必須)**: **bulk 平均崩壊**(2502.05164 Fig.5)— 反復 read 出力が query 非依存の遠方極小(state の平均)へ収束していないかを、query 入替時の出力分散・query-output 相関で監視。崩壊していれば「反復が効いた」と言わない。

---

## 5. 成功基準(事前固定)と honest 内訳

### 成功基準
- **PASS(H1 支持)**: `n>d_state` sparse 域で非線形反復 read の 3-seed recall が R0 と R-CCQ を bootstrap 95% CI 下限 > 0 で上回り、**かつ H2 ablation(非線形>線形反復≈単発)が CI 分離**、**かつ bulk 崩壊なし**。→ 「read 側 test-time 最適化に未回収 gain あり(well-posed 域)」を初実証 → 学習 read adapter / codebook 設計へ前進。
- **NULL(H1 棄却・価値ある結論)**: 反復が baseline と CI 区別不能、または非線形 ablation が分離しない、または bulk 崩壊。→ 「凍結 constant-state からの read 最適化では gain 出ず」を確定 → **TOP-2(anticipatory/future-queriability write gate, `distill.py` 補助損失で前向き保持を学習)へ pivot**。

### honest 内訳プラン
1. **辞書 gate を明示**: gain は「辞書既知」前提でのみ。任意連続 key への一般化は H3 対照で消えることを併記(過度一般化禁止)。
2. **bulk 崩壊の罠**: 反復出力が query 非依存になっていないか必ず監視。
3. **非線形が源泉**: 線形反復 ablation を必ず置き、「反復が効いた」でなく「非線形 cleanup が効いた」と正確に。
4. **規模の限定**: tiny char/合成 MQAR・~数M params の結論を LLM 一般へ外挿しない。
5. **「突破」禁止**: plateau 突破でなく「well-posed 域で単発線形を超える/超えない」。共通天井(蒸留予算 < state 解像度 2504.14366)を併記。
6. **未踏は absence-of-evidence**: TTT/LISTA/DEQ-read は未一次確認 → 「3 本+既知文献に対して未踏」に限定。priority 主張前に Semantic Scholar/Connected Papers で再検索。

---

## 6. 実装(TDD・CPU)— 着手時の最小増分

1. **MQAR/S-NIAH 合成データ生成**(既知辞書つき)+ 単体テスト。
2. **read arm モジュール**(`R0/R-CCQ/R-ISTA/R-Hopfield/R-CountMin/R-linear-iter`)を凍結 state に対する純関数として実装 + 各単体テスト(既知の小例で正答・FLOP 計測)。
3. **bulk 崩壊メトリクス**(query 入替分散・query-output 相関)+ テスト。
4. tiny Gated DeltaNet 学習(detach 解除 × seq_len 掃引)→ state 凍結 → arm 比較ハーネス。
5. 単一 CPU で `n vs d_state` × seed の最小 grid → recall@域 + ablation + 崩壊監視。null/pass を JSON+本 md に記録。

> 実装は新規 `src/llcore/lm/` モジュール(read 法)+ `scripts/poc1_testtime_read.py`。既存非破壊・mypy strict/ruff・テスト green を維持(`feedback_dev_rules`)。

---

## 7. 未確認(着手前/主張前に潰す)
- key 辞書を「既知」にする具体設計(MQAR 語彙そのまま vs 学習 codebook)— MQAR は語彙が辞書なので初手は語彙利用で gate を満たす。
- TTT(write 側 test-time)/ LISTA / DEQ-read の一次未確認 → 未踏断定は限定。
- CCQ/FDM/2502.05164 の式細部は二次(WebFetch 要約経由)→ R-CCQ 実装時に原文 Eq を確認。
- 共通の移植コスト(Qwen GQA/QKV-bias の attention hook)は本 PoC(合成 tiny)では回避できるが、実モデル適用時に再浮上。
