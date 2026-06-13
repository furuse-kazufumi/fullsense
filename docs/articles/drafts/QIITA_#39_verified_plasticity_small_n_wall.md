---
title: 'llcore 検証 arc (#39) — 「証明つきで進化する記憶」を本当に作れた日、ただし n≤6 まで: verified-plasticity を測ったら "navigable かつ scalable な証明器は今も居なかった"'
tags: [FullSense, llcore, Singularity, AI, 解説]
private: true
updated_at: '2026-06-09'
slide: false
ignorePublish: false
id: 9bf5a8c9120b21a0f16e
public_id: bfb20aca3cf1df510c26
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

# 日本語

## この記事は何か — 「窓は実装で閉じた、でも壁はびくともしなかった」報告

前回(#38)の最後で、私たちはこう予告しました。「次回は四点交差点の本丸 — verified memory evolution の小 PoC を report する。SSGM が理論で看板を取った窓が、実装で閉じる前に」。

2026 年 6 月 9 日、その PoC が走り切りました。結論を 1 行で言うと、**「窓は実装で閉じた。でも壁(スケーラビリティの壁)はびくともしなかった」**。

具体的には:

- **証明つきで進化する記憶コア**(実際に構造を太らせる手術 `width_grow` を含む)を、**0 観測 false-admit のまま** 動かせた(= 偽の合格を 1 件も出さずに進化できた)。
- 同時に、前回まで「未測定」と正直に残していた **cert_sdp(SDP 証明器)を初めて測り**、それが **最も "通りやすい"(navigable)健全証明器**(真に収縮する個体の 90〜99% を合格にする)と判明した。
- **にもかかわらず、その cert_sdp も含めて、計算コストは `2^n`(次元 n の指数)のまま** だった。つまり **「通りやすくて、かつ大規模でも安い」証明器は、今回も見つからなかった**。verified に構造進化させられるのは、当面 **小さな部品(n≤6)に限る**。

この記事は、その 1 日の「やれたこと」と「やれなかったこと」を、いつもの順番 ①用語 → ②かみくだき → ③詳細 で、盛らずに書きます。最後に、自分の数値主張を **6 体の検証 AI に並列で反証させた**結果(MAJOR な不一致ゼロ)も開示します。

正本データ: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)(論文ドラフト + 全実験コード/データ)。

---

## ① 用語ミニ辞典(本文で詰まらないために)

| 用語 | ひとことで |
|---|---|
| **可塑性 (plasticity)** | 学習・進化で「形を変えられる」性質。ここでは記憶コアの構造そのもの(行列の大きさ=次元)を後から太らせること。 |
| **verified-plasticity(検証つき可塑性)** | 「形を変える」たびに、その変更が安全(暴走しない)かを **証明してから採用** すること。本研究の主軸。 |
| **width_grow(幅成長)** | ニューラルネットの層を `n → n+1` に **太らせる構造手術**(Net2Net 系)。机上ではなく実際に実行した。 |
| **収縮性 (contraction, ρ<1)** | 過去の揺れが時間とともに **減衰** する性質。スペクトル半径 ρ が 1 未満。記憶が暴走せず「忘れる」性質。 |
| **false-admit(偽の合格)** | 本当は危険(ρ≥1=暴走しうる)なのに、証明器が「安全」と通してしまう取りこぼし。これがゼロなのが健全性の生命線。 |
| **健全 (sound)** | 「合格」と言ったら **本当に安全**(偽の合格を出さない)性質。統計的に「たぶん安全」とは別物。 |
| **navigability(通りやすさ/探索可能性)** | 「本当に安全な個体を、どれだけ合格にできるか」。厳しすぎる証明器は安全な個体まで弾く=進化が動けない。これが高いほど進化は地形を動きやすい。 |
| **証明器格子 (cert ladder)** | 安い順に `cert_inf`(∞-ノルム上界・ソルバ不要)→ `cert_two`(全 `2^n` 頂点 SVD)→ `cert_sdp`(凸 LMI/SDP)の 3 段。 |
| **prove-then-reject ゲート** | 変異(更新)を **証明してから採用**、ダメなら **棄却** する関所。fail-closed(証明できなければ通さない)。 |
| **SSGM** | 「進化する記憶を統べる」write ゲートを **理論だけ** で提案した先行研究([arXiv:2603.11768](https://arxiv.org/abs/2603.11768))。実装 + 健全証明の窓が空いていた相手。 |
| **empirical_rho(経験的 ρ)** | 真のスペクトル半径を、多数サンプルで **下から** 近似するオラクル。「0 観測 false-admit」はこの下からの監査での結果(=強い consistency 証拠だが、絶対証明ではない)。 |
| **2^n 壁** | 証明コストが次元 n に対して指数 `2^n` で増える限界。`cert_two`/`cert_sdp` は頂点を全部見るのでこの壁に当たる。 |

![四点交差点と 2^n 壁 — 通りやすさ(navigability)を縦軸、次元 n を横軸にとると、cert_sdp は天井を上げたが壁(2^n)は破れていない](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_39/qiita_39_fig_wall.svg)

---

## ② かみくだき — 3 分でわかる全体像

前回(#38)で立てた旗は「**証明つきで進化する記憶コア**」でした。記憶コアは更新のたびに変異(進化)しますが、その変異を採用する前に必ず関所(ゲート)を通し、「この変異を入れても記憶が暴走しない」と **数学的に証明できたものだけ** を通す。証明できなければ門前払い(fail-closed)。これが prove-then-reject ゲートです。

今回やったのは、その旗を **「文書」から「動く実物」へ** 進めることでした。3 つの「やれた」があります。

**やれた①: 形を太らせながら、偽の合格ゼロ。** これまでは「変異(中身の微調整)を証明する」までしか試していませんでした。今回は **構造そのものを太らせる手術(`width_grow`、n→n+1)** を実際に走らせ、太らせた後でも証明器が「安全(ρ<1)」を **0 観測 false-admit** で保つことを確認しました。発散域(ρ が 1.85〜2.21 に達する危険な個体)は、全部正しく棄却されました。

**やれた②: 一番"通りやすい"証明器を、初めて測れた。** 前回まで「SDP 証明器(cert_sdp)は未測定」と正直に残していた穴を埋めました。SDP ソルバ(CLARABEL)が使える環境で初めて測ったところ、**cert_sdp が 3 段の証明器のうち最も "通りやすい"** — 真に収縮する個体のうち 90〜99% を合格にする(安い `cert_inf` は 20〜40%、中位の `cert_two` は 40〜50% しか通せない)。つまり「厳しすぎて進化が動けない」問題を、SDP がかなり緩めてくれた。

**やれた③: 小さな部品なら、計算は自明に間に合う。** n≤6 の小さなコアなら、verified に進化させるループ全体が **30 時間の予算の 0.04%(0.013 時間)** しか食わない。「証明つき進化なんて重くて回らないのでは?」という心配は、小規模では杞憂でした。

…ここまで聞くと「全部勝った」ように見えます。でも honest disclosure(正直な開示)が私たちの規律です。**勝てなかったこと** を 3 つ、はっきり書きます。

**やれなかった①: 2^n の壁は破れていない。** cert_sdp は確かに "通りやすさの天井" を上げました。が、その代償としてコストは依然 `2^n`(頂点を全部見る)。`cert_two` は n=12 で 1 証明 1.3 秒、n=14 で予算外。**「通りやすくて、かつ大規模でも安い」証明器は、今回も存在しなかった**。だから verified に構造進化できるのは当面 **小さな部品(n≤6)に限る** — この結論は前回(Phase −1)から **変わっていません**。SDP は壁を **越えた** のではなく、壁の手前で天井を **上げた** だけです。

**やれなかった②: 「偽の合格ゼロ」は経験的観測であって、機械が証明したわけではない。** 0 観測 false-admit は、真の ρ を **下から** 近似するオラクル(多数サンプル)で反証を探した結果です。証明器の *条件* は数学的に健全ですが、それを担う *実装* が端から端まで形式検証されたわけではありません。「0 観測」は強い consistency 証拠ですが、「全ての入力で安全」の絶対証明ではない — ここは誇張しません。

**やれなかった③: 学習が賢くなったわけではない。** 証明器の効き目は **navigability(進化の動きやすさ)** であって、モデルが賢くなる(=学習性能が上がる)ことではありません。しかも効果は進化的アルゴリズム(EA)固有で、勾配法では消えます。さらに今回の適合度(fitness)は **合成 proxy** で、実 GPU 訓練での確認は次フェーズ(Phase 2)送りです。

要するに今回は **「機構は実装で証明できた、規模の壁は正直に残った」** という、半分勝って半分宿題、の日でした。

---

## ③ 詳細 — 5 つの実験と、潰せなかった留保

主軸は **Verified-Plasticity Evaluation Framework**(検証つき可塑性の測定ハーネス)です。「うちの手法が強い」と主張する前に、まず **測る物差し** を作る。その物差しで 5 つの実験を回しました(全て `$0` / CPU、torch 2.12+cpu、seed 固定で再現可能)。

### 3.1 固定構造での証明器の健全性と格子

収縮〜発散を跨ぐ個体を n={4,6,8} で各数百サンプルし、3 証明器の合格と真の ρ(empirical_rho 6000 サンプル)を突合しました。

| n | 収縮(ρ<1) | false-admit (inf/two/sdp) | 真に収縮する個体の合格率 (inf/two/**sdp**) |
|---|---|---|---|
| 4 | 453/600 | **0 / 0 / 0** | 0.41 / 0.51 / **0.95** |
| 6 | 426/600 | **0 / 0 / 0** | 0.29 / 0.43 / **0.94** |
| 8 | 280/400 | **0 / 0 / 0** | 0.23 / 0.40 / **0.91** |

確定知見:
1. **3 証明器すべてが 0 観測 false-admit**(cert_sdp の健全性も初確認)。証明器の数学的健全性と一致。
2. **cert_sdp が圧倒的に navigable** — 真に収縮する個体のうち、安い cert_inf は 23〜41%・cert_two は 40〜51% しか通さないのに、**cert_sdp は 91〜95% 通す**。なお `two⊆sdp`(cert_two が通すなら cert_sdp も通す)は実装上の fast-path による **構造的保証(トートロジー)** であって経験的発見ではない、と明記しておきます(盛らないため)。

### 3.2 実構造手術(width_grow)下での健全性 × 非自明性

実際に `width_grow`(Net2Net/fresh)で base を n→n+1 に太らせ、各ゲートが **成長下でも 0 false-admit を保つ ∧ 非自明な合格を 1 件以上開く** かを判定しました(1 セル = 1536 個の成長後個体)。

- **成長下の健全性: 全 16(セル×ゲート)で 0 観測 false-admit。** 成長 ρ 最大 1.85〜2.21(発散域)は正しく全棄却。これが **North Star #1(成長操作下で偽の合格ゼロ)** の実構造手術での確認です。
- **安い cheap gate(cert_inf)は健全だが、小 n で脆い** — n=6 の最も保守的なエッジ(headroom 0)では非自明な合格が **0 件** → gate FAIL。headroom があっても非自明合格はわずか 3 件で τ ギリギリ。= 「cheap gate の navigability は脆弱」。
- **navigable gate(cert_two/cert_sdp)は全セル PASS** — cert_two は 114〜168、cert_sdp は 673〜733 の非自明な健全合格を開く。→ **「per-component ゲートは cert_two/sdp に格上げ・small-n 限定」がデータで正当化**。

### 3.3 ブロック間結合(coupling)の盲点

2 ブロックを残差結合し、**「各ブロック単体では合格でも、合成すると暴走する」盲点** を真の ρ で測りました。

- **per-block AND(各ブロック単体の合格を AND する)は結合下で本当に不健全** — 結合強度 γ≥1.0 で、単体合格済の **24〜34%(γ=1.0)〜 80〜96%(γ=2.0)が合成真 ρ≥1**(暴走)。→ **per-block AND は禁止確定**。
- **full-system cert(系全体を一括で証明)は全 γ で 0 false-admit = 健全。**
- ここでも **cert_sdp が最 navigable** だが、次元(ブロック数 2→3)と結合強度を上げると coverage は低下(full=6・γ=1.0 で cert_inf/cert_two は 0%、cert_sdp のみ 75.8%)。= SDP は過保守を解消するが、**次元の壁は SDP でも効く**。
- ⚠ 正直な留保: ブロック数 3 で SDP ソルバが「解が不正確かも」警告を数件出しました。**独立な固有値再検査で健全性(false-admit=0)は保証** されますが、coverage の数値は近似解由来の僅かな揺れを含みえます。

### 3.4 feasibility(本当に予算内に回るか)

per-op の実測 wall-time から 30 時間予算へ外挿しました。

| n | 1 eval あたり | 総時間 | 30h に収まる |
|---|---|---|---|
| 4 | 769μs | **0.011h** | はい |
| 6 | 912μs | **0.013h** | はい |
| 8 | 9.2ms | 0.131h | はい |
| 10 | 38.6ms | 0.550h | はい |
| 12 | 1.31s | **18.6h** | 辛うじて |
| 14 | — | (cert_two 2^14 外挿 = 不能) | いいえ |

確定知見:
1. **small-n(n≤6)は計算上自明に feasible** — 予算の 0.04%。
2. **2^n 壁は n≥10〜12 で binding** — cert_two が n=12 で 1.3 秒/証明(=18.6h、マージン薄)、n=14 で予算外。
3. ⚠ 留保: ここの fitness は `RotationNDObjective` の **合成 adapter proxy** で、実 GPU 訓練では base forward(CE)が dominant になります。この外挿は「per-eval ごとに証明を 1 回課金する保守的上限」見積りで、実 GPU 実測は Phase 2 で要確認。

### 3.5 第 2 base(Mamba)への移植性

framework が SmolLM2 以外の base にも載るかを確認しました。**Mamba-130M を CPU で load 成功**(coherent な生成も確認)、その hidden 上で cert_two ゲートが load-bearing(gate あり/なしで合格率が +0.287 動く、SmolLM2 の +0.320 と整合)。= 「新しい base に載せ替えられる」plug-point の実証。
- ⚠ 留保: ここの健全性オラクルは §3.1-3.4 の empirical_rho ではなく **弱いオラクル(単一摂動)** で、合格 n=7 の小集団。Mamba 自体の固有安定性(base-level の Lyapunov)は未測定で Phase 2 送り。本フェーズの deliverable は「framework portability + Mamba CPU 動作確認」に限定します(固有安定性の正対照ではない)。

### 3.6 統合判定 — Decision gate 1 = PASS(small-n)

| gate | 条件 | 判定 |
|---|---|---|
| 成長下 soundness ∧ 非自明 admit≥1 | width_grow N 回で false-admit=0 ∧ 非自明合格≥1 | **PASS**(cheap gate は n=6 で trivial → cert_two/sdp 必須) |
| coupling-aware 合成 soundness | per-block AND 禁止 + full cert 健全 | **PASS** |
| feasibility | small-n ループが 30h 予算内 | **PASS**(small-n) |

→ **Decision gate 1 = PASS → Phase 2 へ(small-n per-component 域、Phase −1 確定の制約内)**。Phase 1 の deliverable は **「健全・feasible な small-n verified 構造適応の測定ハーネス + 証明器格子(inf/two/sdp)の完全な特性評価」** です。

### 3.7 honest 限界(潰せていないもの)

防衛的開示でも honest disclosure は曲げません。前回(#38)の留保に、今回の測定で潰せたもの/残ったものを重ねます。

- **2^n scalability 壁は不変(最大の宿題)**: cert_sdp で navigability 天井は ~0.9 に上がった(前回 cert_two ~0.45 から大幅改善)が、**2^n 頂点コストは不変**。「navigable かつ scalable な健全証明器は依然不在」= verified 構造進化の高次元での不成立は **堅持**。SDP は天井を上げただけで壁は破っていない。
- **empirical_rho は from-below 推定**: 0 観測 false-admit は強い consistency だが「全 (s,x) で ρ<1」の絶対証明ではない。near-boundary を取りこぼしうる。
- **net2net は incoming-copy 近似**(exact function-preserving ではない)→ 関数変化 Δfunc は近似評価。
- **fitness は合成 proxy**: 実 SmolLM2 CE での capability 副線(EXISTS/NULL/ARTIFACT)は Phase 2 必須。
- **Mamba 固有安定性は未測定**: gate は adapter に掛かり、Mamba base 自体の Lyapunov は未検証 → Phase 2 defer。

---

## 敵対的検証 — 自分の数値を 6 体の AI に並列で反証させた

honest disclosure の核は「異常に良い結果が出たら、勝った気になる前に内訳を疑う」です([feedback_benchmark_honest_disclosure])。そこで本 verdict の数値主張を、6 実験それぞれの `results.json` + 実装 `.py` に対し、**独立な検証 AI 6 体を並列**で突合させました。

**結果 = MAJOR issue ゼロ(結論を覆す不一致なし)、全て MINOR。** 検出された指摘は本文に反映済です:
- 転記丸め誤差 4 件(maxΔfunc 0.108→0.107 等)を修正。
- §3.1 の `two⊆sdp` は経験的発見ではなく実装上のトートロジーと明記。
- 「cheap gate は n=6 で trivial」を「n=6 最保守エッジのみ trivial、headroom ありでも脆弱」へ精緻化。
- 「cert_sdp 98% 救済」はブロック数 2 限定、3 では 75.8% / inf・two は 0% と明記。
- fitness が合成 proxy であること、外挿の保守性、CPU→GPU 外挿の前提を透明化。

→ **検証後も Decision gate 1 = PASS、SDP navigability 知見、small-n 限定結論は不変**。指摘は全て honest-disclosure の精度向上であり、機構的結論を揺るがすものは無し。

---

## まとめ — 「窓は閉じた、壁は残った」

#38 で立てた旗は、今回 **文書から動く実物へ** 進みました。証明つきで進化する記憶コアを、実際に構造を太らせながら **0 観測 false-admit** で動かし、未測定だった SDP 証明器を埋め、small-n の feasibility を確認しました。SSGM が理論で取った看板の「実装 + 健全証明」の窓は、こうして実装側で閉じました。

一方で、最大の宿題 **2^n 壁** は今回もびくともしませんでした。「通りやすくて、かつ大規模でも安い」証明器は依然として存在しません。だから私たちは **盛りません**: verified に構造進化できるのは **当面 n≤6 の小さな部品まで**、という前回の結論を堅持します。

次回(#40 以降)は Phase 2 — 校正済みの「多峰性 instrument」を実損失地形に当て、進化が地形をどう動くか(capability 副線)を proper power で 1 つ確定する予定です。物差しはできた。次は、その物差しで実地形を測る番です。

正本: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) — 論文ドラフト + 全実験コード/データ(5 実験 + 敵対的検証 workflow)。

---

# English

## What this article is — "the window closed in implementation, but the wall did not budge"

At the end of #38, we promised: "Next time we will report the heart of the four-point intersection — a small PoC of verified memory evolution. Before the window where SSGM took the banner in theory closes in implementation."

On June 9, 2026, that PoC ran to completion. In one sentence: **"The window closed in implementation. But the wall (the scalability wall) did not budge an inch."**

Concretely:

- We ran a **memory core that evolves with proofs** (including real structural surgery `width_grow`) with **zero observed false-admits** (i.e., it evolved without issuing a single false pass).
- At the same time, we measured for the first time the **cert_sdp (SDP verifier)** that we had honestly left "unmeasured" until now, and found it to be the **most "navigable" sound verifier** (it passes 90–99% of genuinely contracting individuals).
- **Nevertheless, even cert_sdp's cost remains `2^n` (exponential in dimension n).** That is, **a verifier that is "both navigable and cheap at scale" was, once again, not found.** For now, verified structural evolution is limited to **small components (n≤6).**

This article writes, without inflating, both what we "could" and "could not" do that day, in the usual order ① terms → ② breakdown → ③ details. At the end we also disclose the result of having **6 verifier AIs adversarially refute our own numbers in parallel** (zero MAJOR discrepancies).

Source of truth: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) (paper draft + all experiment code/data).

---

## ① Mini-glossary (so you don't get stuck in the body)

| Term | In a word |
|---|---|
| **Plasticity** | The property of being able to "change shape" through learning/evolution. Here, growing the memory core's own structure (matrix size = dimension) after the fact. |
| **Verified-plasticity** | Each time you "change shape," **proving the change is safe (won't run away) before adopting it.** The main axis of this research. |
| **width_grow** | **Structural surgery** that grows a network layer from `n → n+1` (Net2Net family). Actually executed, not on paper. |
| **Contraction (ρ<1)** | The property that past perturbations **decay** over time. Spectral radius ρ below 1. The property by which memory "forgets" rather than running away. |
| **false-admit** | A miss where a verifier passes something actually dangerous (ρ≥1 = can run away) as "safe." Zero of these is the lifeline of soundness. |
| **Sound** | The property that when it says "pass," it is **actually safe** (never a false pass). Different from a statistical "probably safe." |
| **navigability** | "How many genuinely safe individuals it can pass." An overly strict verifier rejects even safe individuals = evolution can't move. The higher, the more freely evolution moves over the terrain. |
| **cert ladder** | Three rungs, cheapest first: `cert_inf` (∞-norm bound, solver-free) → `cert_two` (SVD at all `2^n` vertices) → `cert_sdp` (convex LMI/SDP). |
| **prove-then-reject gate** | A checkpoint that **adopts a mutation only after proving it**, and **rejects** it if it fails. fail-closed (no proof, no pass). |
| **SSGM** | Prior work proposing a write gate "to govern evolving memory" **in theory only** ([arXiv:2603.11768](https://arxiv.org/abs/2603.11768)). The party for whom the window of implementation + sound proof was open. |
| **empirical_rho** | An oracle that approximates the true spectral radius **from below** with many samples. "Zero observed false-admits" is the result of this from-below audit (= strong consistency evidence, but not an absolute proof). |
| **2^n wall** | The limit where proof cost grows exponentially `2^n` in dimension n. `cert_two`/`cert_sdp` look at all vertices, so they hit this wall. |

![Four-point intersection and the 2^n wall — with navigability on the vertical axis and dimension n on the horizontal, cert_sdp raised the ceiling but did not break the wall (2^n)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_39/qiita_39_fig_wall.svg)

---

## ② Breakdown — the whole picture in 3 minutes

The flag planted in #38 was a **"memory core that evolves with proofs."** The memory core mutates (evolves) each update, but before any mutation is adopted it must pass a checkpoint (gate) that admits **only what can be mathematically proven** not to run away; otherwise it is turned away (fail-closed). This is the prove-then-reject gate.

This time we moved that flag **from "a document" to "a working thing."** Three things we "could" do.

**Could ①: Zero false passes, even while growing the shape.** Until now we had only tried "proving mutations (small internal tweaks)." This time we actually ran **structural surgery that grows the shape (`width_grow`, n→n+1)** and confirmed the verifier keeps "safe (ρ<1)" with **zero observed false-admits** even after growing. The divergent region (dangerous individuals reaching ρ 1.85–2.21) was all correctly rejected.

**Could ②: We measured the most "navigable" verifier for the first time.** We filled the hole we had honestly left as "cert_sdp unmeasured." In an environment with an SDP solver (CLARABEL), we measured it for the first time and found **cert_sdp the most "navigable" of the three** — it passes 90–99% of genuinely contracting individuals (the cheap `cert_inf` passes only 20–40%, the middle `cert_two` 40–50%). The "too strict, evolution can't move" problem was substantially relaxed by SDP.

**Could ③: For small components, the computation trivially fits.** For a small core of n≤6, the entire verified-evolution loop eats only **0.04% of a 30-hour budget (0.013 hours).** The worry "isn't proof-gated evolution too heavy to run?" was, at small scale, unfounded.

…So far it sounds like "we won everything." But honest disclosure is our discipline. Here are three things we **could not** win, stated plainly.

**Could not ①: The 2^n wall is not broken.** cert_sdp did raise the "navigability ceiling." But at the cost of a still-`2^n` price (looking at all vertices). `cert_two` is 1.3 s per proof at n=12, out of budget at n=14. **A verifier that is "both navigable and cheap at scale" did not exist this time either.** So verified structural evolution is, for now, limited to **small components (n≤6)** — this conclusion is **unchanged** from last time (Phase −1). SDP did not **cross** the wall; it merely **raised** the ceiling in front of it.

**Could not ②: "Zero false passes" is an empirical observation, not a machine proof.** Zero observed false-admits is the result of searching for refutations with an oracle that approximates the true ρ **from below** (many samples). The verifier's *conditions* are mathematically sound, but the *implementation* carrying them is not end-to-end formally verified. "Zero observed" is strong consistency evidence, not an absolute proof of "safe for all inputs" — we don't exaggerate here.

**Could not ③: The model did not get smarter.** The verifier's payoff is **navigability (how freely evolution moves)**, not the model getting smarter (learning performance going up). And the effect is specific to evolutionary algorithms (EA); it vanishes with gradient methods. Furthermore, this round's fitness is a **synthetic proxy**, and confirmation under real GPU training is deferred to the next phase (Phase 2).

In short, this was a half-won, half-homework day: **"the mechanism was proven in implementation; the scale wall remains, honestly."**

---

## ③ Details — five experiments and the caveats we couldn't kill

The main axis is the **Verified-Plasticity Evaluation Framework.** Before claiming "our method is strong," first build **the ruler to measure with.** With that ruler we ran five experiments (all `$0` / CPU, torch 2.12+cpu, fixed seed, reproducible).

### 3.1 Verifier soundness and ladder under fixed structure

Sampling hundreds of individuals each at n={4,6,8} spanning contraction–divergence, we cross-checked the three verifiers' passes against true ρ (empirical_rho, 6000 samples).

| n | contracting (ρ<1) | false-admit (inf/two/sdp) | pass rate of genuinely contracting (inf/two/**sdp**) |
|---|---|---|---|
| 4 | 453/600 | **0 / 0 / 0** | 0.41 / 0.51 / **0.95** |
| 6 | 426/600 | **0 / 0 / 0** | 0.29 / 0.43 / **0.94** |
| 8 | 280/400 | **0 / 0 / 0** | 0.23 / 0.40 / **0.91** |

Findings:
1. **All three verifiers have zero observed false-admits** (cert_sdp's soundness confirmed for the first time). Consistent with the verifiers' mathematical soundness.
2. **cert_sdp is overwhelmingly navigable** — of genuinely contracting individuals, the cheap cert_inf passes only 23–41%, cert_two 40–51%, but **cert_sdp passes 91–95%**. Note that `two⊆sdp` (if cert_two passes, cert_sdp passes) is a **structural guarantee (tautology)** from an implementation fast-path, not an empirical finding — we state this so as not to inflate.

### 3.2 Soundness × non-triviality under real structural surgery (width_grow)

We actually grew the base n→n+1 with `width_grow` (Net2Net/fresh) and judged whether each gate **keeps zero false-admits under growth ∧ opens ≥1 non-trivial pass** (1 cell = 1536 grown individuals).

- **Soundness under growth: zero observed false-admits across all 16 (cell × gate).** Growth ρ up to 1.85–2.21 (divergent region) all correctly rejected. This is the confirmation of **North Star #1 (zero false passes under growth operations)** under real structural surgery.
- **The cheap gate (cert_inf) is sound but fragile at small n** — at the most conservative edge of n=6 (headroom 0), non-trivial passes are **0** → gate FAIL. Even with headroom, non-trivial passes are merely 3, right at the τ margin. = "the cheap gate's navigability is fragile."
- **The navigable gates (cert_two/cert_sdp) PASS all cells** — cert_two opens 114–168, cert_sdp 673–733 non-trivial sound passes. → **"Promote per-component gates to cert_two/sdp, limited to small-n" is justified by data.**

### 3.3 The blind spot of inter-block coupling

Coupling two blocks residually, we measured with true ρ the **blind spot where "each block passes alone but the composite runs away."**

- **per-block AND (AND-ing each block's individual pass) is genuinely unsound under coupling** — at coupling strength γ≥1.0, **24–34% (γ=1.0) to 80–96% (γ=2.0) of individually-passed cases have composite true ρ≥1** (run away). → **per-block AND is forbidden.**
- **full-system cert (proving the whole system at once) has zero false-admits across all γ = sound.**
- Here too **cert_sdp is the most navigable**, but raising the dimension (block count 2→3) and coupling strength lowers coverage (at full=6, γ=1.0, cert_inf/cert_two are 0%, only cert_sdp 75.8%). = SDP resolves over-conservatism, but **the dimension wall still bites even with SDP.**
- ⚠ Honest caveat: at block count 3 the SDP solver issued a few "solution may be inaccurate" warnings. **Soundness (false-admit=0) is guaranteed by an independent eigenvalue recheck**, but the coverage numbers may include slight wobble from the approximate solution.

### 3.4 feasibility (does it really run within budget)

We extrapolated measured per-op wall-time to a 30-hour budget.

| n | per eval | total | fits in 30h |
|---|---|---|---|
| 4 | 769μs | **0.011h** | yes |
| 6 | 912μs | **0.013h** | yes |
| 8 | 9.2ms | 0.131h | yes |
| 10 | 38.6ms | 0.550h | yes |
| 12 | 1.31s | **18.6h** | barely |
| 14 | — | (cert_two 2^14 extrapolation = infeasible) | no |

Findings:
1. **small-n (n≤6) is trivially feasible** — 0.04% of the budget.
2. **The 2^n wall binds at n≥10–12** — cert_two is 1.3 s/proof at n=12 (=18.6h, thin margin), out of budget at n=14.
3. ⚠ Caveat: this fitness is a **synthetic adapter proxy** of `RotationNDObjective`; under real GPU training the base forward (CE) becomes dominant. This extrapolation is a "conservative upper bound charging one proof per eval"; real GPU measurement is to be confirmed in Phase 2.

### 3.5 Portability to a second base (Mamba)

We checked whether the framework rides on bases other than SmolLM2. **Mamba-130M loaded successfully on CPU** (coherent generation confirmed), and on its hidden state the cert_two gate is load-bearing (pass rate moves +0.287 with/without the gate, consistent with SmolLM2's +0.320). = Demonstration of the "swap in a new base" plug-point.
- ⚠ Caveat: the soundness oracle here is not the empirical_rho of §3.1-3.4 but a **weak oracle (single perturbation)**, with a small group of n=7 passes. Mamba's own intrinsic stability (base-level Lyapunov) is unmeasured, deferred to Phase 2. This phase's deliverable is limited to "framework portability + Mamba CPU operation check" (not an intrinsic-stability positive control).

### 3.6 Integrated verdict — Decision gate 1 = PASS (small-n)

| gate | condition | verdict |
|---|---|---|
| Soundness under growth ∧ non-trivial admit≥1 | false-admit=0 over N width_grow ∧ non-trivial pass≥1 | **PASS** (cheap gate trivial at n=6 → cert_two/sdp required) |
| coupling-aware composite soundness | per-block AND forbidden + full cert sound | **PASS** |
| feasibility | small-n loop within 30h budget | **PASS** (small-n) |

→ **Decision gate 1 = PASS → on to Phase 2 (small-n per-component regime, within the constraint fixed in Phase −1).** Phase 1's deliverable is **"a measurement harness for sound, feasible small-n verified structural adaptation + a full characterization of the verifier ladder (inf/two/sdp)."**

### 3.7 Honest limits (not yet killed)

Even with defensive disclosure we do not bend honest disclosure. Onto #38's caveats, we overlay what this round's measurement killed / left.

- **The 2^n scalability wall is unchanged (the biggest homework)**: cert_sdp raised the navigability ceiling to ~0.9 (a big improvement from Phase −1's cert_two ~0.45), but the **2^n vertex cost is unchanged.** "A navigable-and-scalable sound verifier remains absent" = the non-viability of high-dimensional verified structural evolution is **upheld.** SDP only raised the ceiling; it did not break the wall.
- **empirical_rho is a from-below estimate**: zero observed false-admits is strong consistency, not an absolute proof of "ρ<1 for all (s,x)." It can miss near-boundary cases.
- **net2net is an incoming-copy approximation** (not exact function-preserving) → the function change Δfunc is an approximate measure.
- **fitness is a synthetic proxy**: a capability side-line (EXISTS/NULL/ARTIFACT) on real SmolLM2 CE is required in Phase 2.
- **Mamba's intrinsic stability is unmeasured**: the gate applies to the adapter; the Mamba base's own Lyapunov is unverified → deferred to Phase 2.

---

## Adversarial verification — having 6 AIs refute our own numbers in parallel

The core of honest disclosure is "when an abnormally good result appears, doubt the breakdown before feeling like you've won" ([feedback_benchmark_honest_disclosure]). So we had **6 independent verifier AIs in parallel** cross-check this verdict's numerical claims against each experiment's `results.json` + implementation `.py`.

**Result = zero MAJOR issues (no discrepancy that overturns the conclusion); all MINOR.** The findings are reflected in the body:
- Fixed 4 transcription rounding errors (maxΔfunc 0.108→0.107, etc.).
- §3.1's `two⊆sdp` stated as an implementation tautology, not an empirical finding.
- Refined "the cheap gate is trivial at n=6" to "trivial only at n=6's most conservative edge, fragile even with headroom."
- "cert_sdp 98% rescue" stated as limited to block count 2; at 3 it is 75.8% / inf·two 0%.
- Made transparent that fitness is a synthetic proxy, the conservatism of the extrapolation, and the CPU→GPU extrapolation premise.

→ **After verification, Decision gate 1 = PASS, the SDP navigability finding, and the small-n-limited conclusion are unchanged.** The findings all improve honest-disclosure precision; none shake the mechanistic conclusion.

---

## Summary — "the window closed, the wall remained"

The flag planted in #38 advanced this time **from a document to a working thing.** We ran a memory core that evolves with proofs, while actually growing its structure, with **zero observed false-admits**, filled in the previously-unmeasured SDP verifier, and confirmed small-n feasibility. The window of "implementation + sound proof" for the banner SSGM took in theory thus closed on the implementation side.

On the other hand, the biggest homework, the **2^n wall**, did not budge this time either. A verifier "both navigable and cheap at scale" still does not exist. So we do not inflate: we uphold last time's conclusion that verified structural evolution is, **for now, limited to small components of n≤6.**

Next time (from #40 on) is Phase 2 — applying the calibrated "multimodality instrument" to a real loss terrain and confirming, with proper power, one thing about how evolution moves over the terrain (the capability side-line). The ruler is built. Next, it's time to measure real terrain with that ruler.

Source of truth: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) — paper draft + all experiment code/data (5 experiments + adversarial-verification workflow).

---

# 中文

## 这篇文章是什么 —— 「窗在实现里关上了，但墙纹丝不动」的报告

上一回（#38）结尾，我们这样预告：「下一回将 report 四点交叉点的本丸 —— verified memory evolution 的小 PoC。趁 SSGM 以理论拿下招牌的那扇窗，还没被实现合上之前。」

2026 年 6 月 9 日，那个 PoC 跑完了。用一句话说结论：**「窗在实现里关上了。但墙（可扩展性的墙）纹丝不动。」**

具体来说：

- 我们让**带证明地进化的记忆核**（包含真正把结构变大的手术 `width_grow`）在 **零观测 false-admit** 下跑了起来（= 一件假合格都没发，就完成了进化）。
- 同时，把此前一直诚实地留作「未测定」的 **cert_sdp（SDP 证明器）首次测量**，发现它是**最「易通过」（navigable）的健全证明器**（把真正收缩的个体的 90～99% 判为合格）。
- **尽管如此，包括 cert_sdp 在内，计算成本仍是 `2^n`（维度 n 的指数）。** 也就是说，**「既易通过、在大规模下又便宜」的证明器，这次也没找到。** 目前能 verified 地做结构进化的，仅限于**小部件（n≤6）。**

这篇文章，按惯例的顺序 ①术语 → ②拆解 → ③详细，不注水地写下那一天「能做到的」与「做不到的」。最后还公开把自己的数值主张**让 6 个验证 AI 并行反证**的结果（零 MAJOR 不一致）。

正本数据：[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)（论文草稿 + 全部实验代码/数据）。

---

## ① 术语小辞典（免得在正文里卡住）

| 术语 | 一句话 |
|---|---|
| **可塑性 (plasticity)** | 通过学习/进化能「改变形状」的性质。这里指事后把记忆核自身的结构（矩阵大小=维度）变大。 |
| **verified-plasticity（带验证的可塑性）** | 每次「改变形状」时，都**先证明该变更安全（不暴走）再采用**。本研究的主轴。 |
| **width_grow（宽度成长）** | 把网络层从 `n → n+1` 变大的**结构手术**（Net2Net 系）。是实际执行的，不是纸上。 |
| **收缩性 (contraction, ρ<1)** | 过去的扰动随时间**衰减**的性质。谱半径 ρ 小于 1。记忆不暴走、会「遗忘」的性质。 |
| **false-admit（假合格）** | 明明危险（ρ≥1=可能暴走），证明器却放行为「安全」的漏检。这一项为零是健全性的命门。 |
| **健全 (sound)** | 一旦说「合格」就**真的安全**（绝不发假合格）的性质。与统计上「大概安全」是两回事。 |
| **navigability（易通过/可探索性）** | 「能把多少真正安全的个体判为合格」。过严的证明器连安全个体也弹掉=进化动不了。越高，进化越能在地形上自由移动。 |
| **证明器格子 (cert ladder)** | 按便宜优先三级：`cert_inf`（∞-范数上界、无需求解器）→ `cert_two`（全 `2^n` 顶点 SVD）→ `cert_sdp`（凸 LMI/SDP）。 |
| **prove-then-reject 门** | **证明之后才采用**变异，不行则**棄却**的关卡。fail-closed（无法证明就不放行）。 |
| **SSGM** | **仅以理论**提出「统御进化记忆」write 门的先行研究（[arXiv:2603.11768](https://arxiv.org/abs/2603.11768)）。实现 + 健全证明的窗口对它而言是空着的。 |
| **empirical_rho（经验 ρ）** | 用大量采样**从下方**逼近真谱半径的预言机。「零观测 false-admit」是这种从下方审计的结果（=强一致性证据，但非绝对证明）。 |
| **2^n 墙** | 证明成本对维度 n 呈指数 `2^n` 增长的极限。`cert_two`/`cert_sdp` 要看全部顶点，所以撞上这堵墙。 |

![四点交叉点与 2^n 墙 —— 纵轴取易通过性(navigability)、横轴取维度 n，cert_sdp 抬高了天花板，但没破墙(2^n)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_39/qiita_39_fig_wall.svg)

---

## ② 拆解 —— 3 分钟看懂全貌

#38 立的旗是**「带证明地进化的记忆核」**。记忆核每次更新都会变异（进化），但在采用任何变异前，都必须先过关卡（门），只放行**能在数学上证明不暴走**的变异，证明不出来就拒之门外（fail-closed）。这就是 prove-then-reject 门。

这次做的，是把那面旗**从「文件」推进到「能跑的实物」**。有三件「能做到」。

**能做到①：一边把形状变大，一边零假合格。** 此前只试到「证明变异（内部微调）」。这次实际跑了**把结构本身变大的手术（`width_grow`，n→n+1）**，确认变大之后证明器仍以**零观测 false-admit**保持「安全（ρ<1）」。发散域（ρ 达 1.85～2.21 的危险个体）全部被正确棄却。

**能做到②：第一次测到了最「易通过」的证明器。** 把此前诚实留下的「cert_sdp 未测定」这个洞补上了。在能用 SDP 求解器（CLARABEL）的环境里首次测量，发现 **cert_sdp 是三级证明器中最「易通过」的** —— 把真正收缩的个体的 90～99% 判合格（便宜的 `cert_inf` 只通 20～40%，中位的 `cert_two` 40～50%）。「太严、进化动不了」的问题，被 SDP 大幅缓解。

**能做到③：小部件的话，计算轻松够用。** n≤6 的小核，verified 进化的整个循环只吃 **30 小时预算的 0.04%（0.013 小时）**。「带证明的进化是不是太重跑不动？」的担心，在小规模下是杞人忧天。

…听到这里像是「全赢了」。但 honest disclosure（诚实开示）是我们的纪律。把**没赢的三件事**明明白白写下来。

**没做到①：2^n 墙没破。** cert_sdp 确实抬高了「易通过性的天花板」。但代价是成本仍为 `2^n`（看全部顶点）。`cert_two` 在 n=12 是 1 次证明 1.3 秒，n=14 超预算。**「既易通过、大规模下又便宜」的证明器，这次也不存在。** 所以目前能 verified 地做结构进化的仅限**小部件（n≤6）** —— 这个结论与上一回（Phase −1）**没有变**。SDP 不是**翻过**了墙，而只是在墙前**抬高**了天花板。

**没做到②：「零假合格」是经验观测，并非机器证明出来的。** 零观测 false-admit，是用**从下方**逼近真 ρ 的预言机（大量采样）去找反证的结果。证明器的*条件*在数学上健全，但承载它的*实现*并未做端到端的形式验证。「零观测」是强一致性证据，不是「对所有输入都安全」的绝对证明 —— 这里不夸张。

**没做到③：模型并没变聪明。** 证明器的功效是 **navigability（进化的可移动性）**，不是模型变聪明（学习性能提升）。而且效果是进化算法（EA）固有的，在梯度法里会消失。再者这次的适应度（fitness）是**合成 proxy**，实 GPU 训练下的确认留到下一阶段（Phase 2）。

总之这一天是「机构在实现里证明了，规模的墙诚实地留着」—— 赢一半、作业留一半的一天。

---

## ③ 详细 —— 五个实验，以及没能潰掉的留白

主轴是 **Verified-Plasticity Evaluation Framework**（带验证的可塑性测量框架）。在主张「我们的方法强」之前，先造**度量的尺子**。用那把尺子跑了五个实验（全部 `$0` / CPU、torch 2.12+cpu、固定 seed、可复现）。

### 3.1 固定结构下证明器的健全性与格子

在 n={4,6,8} 各采样数百个跨越收缩～发散的个体，把 3 证明器的合格与真 ρ（empirical_rho 6000 采样）做突合。

| n | 收缩(ρ<1) | false-admit (inf/two/sdp) | 真正收缩个体的合格率 (inf/two/**sdp**) |
|---|---|---|---|
| 4 | 453/600 | **0 / 0 / 0** | 0.41 / 0.51 / **0.95** |
| 6 | 426/600 | **0 / 0 / 0** | 0.29 / 0.43 / **0.94** |
| 8 | 280/400 | **0 / 0 / 0** | 0.23 / 0.40 / **0.91** |

确定知见：
1. **三个证明器全部零观测 false-admit**（首次确认 cert_sdp 的健全性）。与证明器的数学健全性一致。
2. **cert_sdp 压倒性 navigable** —— 真正收缩的个体中，便宜的 cert_inf 只通 23～41%、cert_two 40～51%，而 **cert_sdp 通 91～95%**。注：`two⊆sdp`（cert_two 通则 cert_sdp 通）是实现 fast-path 带来的**结构性保证（同义反复）**，不是经验发现 —— 为不注水而写明。

### 3.2 实结构手术（width_grow）下的健全性 × 非平凡性

实际用 `width_grow`（Net2Net/fresh）把 base 从 n→n+1 变大，判定各门是否**在成长下仍保持零 false-admit ∧ 开出≥1 个非平凡合格**（1 格 = 1536 个成长后个体）。

- **成长下健全性：全 16（格×门）零观测 false-admit。** 成长 ρ 最大 1.85～2.21（发散域）全部正确棄却。这是 **North Star #1（成长操作下零假合格）** 在实结构手术下的确认。
- **便宜门（cert_inf）健全但在小 n 脆弱** —— n=6 最保守边缘（headroom 0）非平凡合格 **0 个** → 门 FAIL。即便有 headroom，非平凡合格也仅 3 个，卡在 τ 边缘。= 「便宜门的 navigability 脆弱」。
- **navigable 门（cert_two/cert_sdp）全格 PASS** —— cert_two 开 114～168、cert_sdp 开 673～733 个非平凡健全合格。→ **「把 per-component 门升级到 cert_two/sdp、限定 small-n」由数据正当化。**

### 3.3 块间结合（coupling）的盲点

把 2 个块残差结合，用真 ρ 测**「各块单独合格、合成却暴走」的盲点**。

- **per-block AND（把各块单独合格做 AND）在结合下确实不健全** —— 结合强度 γ≥1.0 时，单独合格里的 **24～34%（γ=1.0）～ 80～96%（γ=2.0）合成真 ρ≥1**（暴走）。→ **per-block AND 禁止确定。**
- **full-system cert（把整个系统一次性证明）全 γ 零 false-admit = 健全。**
- 这里同样 **cert_sdp 最 navigable**，但抬高维度（块数 2→3）与结合强度，coverage 会下降（full=6、γ=1.0 时 cert_inf/cert_two 为 0%，仅 cert_sdp 75.8%）。= SDP 解决过保守，但**维度墙对 SDP 也起作用。**
- ⚠ 诚实留白：块数 3 时 SDP 求解器发了几条「解可能不准确」警告。**用独立特征值复检保证健全性（false-admit=0）**，但 coverage 数值可能含近似解带来的微小抖动。

### 3.4 feasibility（是否真能在预算内跑）

由实测 per-op wall-time 外推到 30 小时预算。

| n | 每次 eval | 总时间 | 30h 内 |
|---|---|---|---|
| 4 | 769μs | **0.011h** | 是 |
| 6 | 912μs | **0.013h** | 是 |
| 8 | 9.2ms | 0.131h | 是 |
| 10 | 38.6ms | 0.550h | 是 |
| 12 | 1.31s | **18.6h** | 勉强 |
| 14 | — | (cert_two 2^14 外推 = 不能) | 否 |

确定知见：
1. **small-n（n≤6）计算上自明 feasible** —— 预算的 0.04%。
2. **2^n 墙在 n≥10～12 binding** —— cert_two 在 n=12 是 1.3 秒/证明（=18.6h，余量薄），n=14 超预算。
3. ⚠ 留白：此处 fitness 是 `RotationNDObjective` 的**合成 adapter proxy**，实 GPU 训练里 base forward（CE）会成为 dominant。该外推是「每次 eval 课金一次证明的保守上限」，实 GPU 实测留待 Phase 2 确认。

### 3.5 向第 2 个 base（Mamba）的可移植性

确认框架是否能载到 SmolLM2 以外的 base。**Mamba-130M 在 CPU 上 load 成功**（确认了 coherent 生成），在其 hidden 上 cert_two 门 load-bearing（有/无门合格率移动 +0.287，与 SmolLM2 的 +0.320 相洽）。= 「换上新 base」plug-point 的实证。
- ⚠ 留白：此处健全性预言机不是 §3.1-3.4 的 empirical_rho，而是**弱预言机（单一摄动）**，合格 n=7 的小集团。Mamba 自身的固有稳定性（base-level Lyapunov）未测定，留待 Phase 2。本阶段 deliverable 仅限「框架可移植性 + Mamba CPU 动作确认」（不是固有稳定性的正对照）。

### 3.6 综合判定 —— Decision gate 1 = PASS（small-n）

| gate | 条件 | 判定 |
|---|---|---|
| 成长下 soundness ∧ 非平凡 admit≥1 | width_grow N 次 false-admit=0 ∧ 非平凡合格≥1 | **PASS**（便宜门在 n=6 trivial → 必须 cert_two/sdp） |
| coupling-aware 合成 soundness | per-block AND 禁止 + full cert 健全 | **PASS** |
| feasibility | small-n 循环在 30h 预算内 | **PASS**（small-n） |

→ **Decision gate 1 = PASS → 进入 Phase 2（small-n per-component 域，在 Phase −1 确定的约束内）。** Phase 1 的 deliverable 是**「健全·feasible 的 small-n verified 结构适应测量框架 + 证明器格子（inf/two/sdp）的完整特性评价」**。

### 3.7 honest 局限（没能潰掉的）

即便是防御性开示，honest disclosure 也不弯折。把这次测量潰掉/留下的，叠在 #38 的留白之上。

- **2^n scalability 墙不变（最大作业）**：cert_sdp 把 navigability 天花板抬到 ~0.9（从 Phase −1 的 cert_two ~0.45 大幅改善），但 **2^n 顶点成本不变**。「navigable 且 scalable 的健全证明器依然不在」= 高维 verified 结构进化不成立 **堅持**。SDP 只抬了天花板，没破墙。
- **empirical_rho 是从下方估计**：零观测 false-admit 是强一致性，不是「对全部 (s,x) ρ<1」的绝对证明。可能漏掉 near-boundary。
- **net2net 是 incoming-copy 近似**（非 exact function-preserving）→ 函数变化 Δfunc 是近似评估。
- **fitness 是合成 proxy**：实 SmolLM2 CE 上的 capability 副线（EXISTS/NULL/ARTIFACT）是 Phase 2 必须。
- **Mamba 固有稳定性未测定**：门挂在 adapter 上，Mamba base 自身的 Lyapunov 未验证 → 留待 Phase 2。

---

## 敌对验证 —— 让 6 个 AI 并行反证自己的数值

honest disclosure 的核心是「出现异常好的结果时，在自觉赢之前先怀疑内訳」（[feedback_benchmark_honest_disclosure]）。于是把本 verdict 的数值主张，对各实验的 `results.json` + 实现 `.py`，让**6 个独立验证 AI 并行**突合。

**结果 = 零 MAJOR issue（无能覆盖结论的不一致），全是 MINOR。** 检出的指摘已反映进正文：
- 修正 4 件转记舍入误差（maxΔfunc 0.108→0.107 等）。
- §3.1 的 `two⊆sdp` 写明是实现上的同义反复，而非经验发现。
- 把「便宜门在 n=6 trivial」精炼为「仅 n=6 最保守边缘 trivial、有 headroom 也脆弱」。
- 「cert_sdp 98% 救济」写明限块数 2，块数 3 是 75.8% / inf·two 0%。
- 透明化 fitness 是合成 proxy、外推的保守性、CPU→GPU 外推前提。

→ **验证后 Decision gate 1 = PASS、SDP navigability 知见、small-n 限定结论不变。** 指摘全是 honest-disclosure 的精度提升，无一动摇机构性结论。

---

## 总结 —— 「窗关上了，墙留下了」

#38 立的旗，这次**从文件推进到了能跑的实物**。我们让带证明地进化的记忆核，一边真把结构变大，一边以**零观测 false-admit**跑起来，补上了此前未测定的 SDP 证明器，确认了 small-n 的 feasibility。SSGM 以理论拿下招牌的「实现 + 健全证明」的窗，就这样在实现侧关上了。

另一方面，最大作业 **2^n 墙** 这次也纹丝不动。「既易通过、大规模下又便宜」的证明器依然不存在。所以我们不注水：堅持上一回的结论 —— 能 verified 地做结构进化的，**目前仅限 n≤6 的小部件**。

下一回（#40 以后）是 Phase 2 —— 把校准好的「多峰性 instrument」当到实损失地形上，以 proper power 确定一件关于进化如何在地形上移动的事（capability 副线）。尺子造好了。下一步，是用那把尺子去量实地形。

正本：[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) —— 论文草稿 + 全部实验代码/数据（5 实验 + 敌对验证 workflow）。

---

# 한국어

## 이 글은 무엇인가 — 「창은 구현으로 닫혔다, 그러나 벽은 꿈쩍도 안 했다」보고

지난 회(#38) 마지막에 우리는 이렇게 예고했습니다. 「다음 회는 네 점 교차점의 본진 — verified memory evolution의 작은 PoC를 report한다. SSGM이 이론으로 간판을 차지한 창문이, 구현으로 닫히기 전에.」

2026년 6월 9일, 그 PoC가 완주했습니다. 한 줄로 결론을 말하면, **「창은 구현으로 닫혔다. 그러나 벽(확장성의 벽)은 한 치도 꿈쩍하지 않았다.」**

구체적으로:

- **증명을 붙여 진화하는 기억 코어**(실제로 구조를 키우는 수술 `width_grow` 포함)를 **0 관측 false-admit으로** 돌릴 수 있었다(= 거짓 합격을 1건도 내지 않고 진화).
- 동시에, 지금껏 정직하게 「미측정」으로 남겨 두었던 **cert_sdp(SDP 증명기)를 처음 측정**했고, 그것이 **가장 "통과하기 쉬운"(navigable) 건전 증명기**(진짜로 축소하는 개체의 90~99%를 합격시킴)임을 확인했다.
- **그럼에도 cert_sdp를 포함해 계산 비용은 여전히 `2^n`(차원 n의 지수)이었다.** 즉 **「통과하기 쉽고, 대규모에서도 싼」 증명기는 이번에도 찾지 못했다.** 당분간 verified로 구조 진화를 시킬 수 있는 것은 **작은 부품(n≤6)에 한한다.**

이 글은 그 하루의 「해낸 것」과 「못 해낸 것」을, 늘 그렇듯 ①용어 → ②쉽게 풀기 → ③상세 순으로, 부풀리지 않고 씁니다. 마지막에 자신의 수치 주장을 **6개의 검증 AI에게 병렬로 반증시킨** 결과(MAJOR 불일치 제로)도 공개합니다.

정본 데이터: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)(논문 드래프트 + 전체 실험 코드/데이터).

---

## ① 용어 미니 사전(본문에서 막히지 않도록)

| 용어 | 한마디로 |
|---|---|
| **가소성 (plasticity)** | 학습·진화로 「형태를 바꿀 수 있는」 성질. 여기서는 기억 코어 자체의 구조(행렬 크기=차원)를 나중에 키우는 것. |
| **verified-plasticity(검증 붙은 가소성)** | 「형태를 바꿀」 때마다 그 변경이 안전(폭주하지 않음)한지 **증명하고 나서 채용**하는 것. 본 연구의 주축. |
| **width_grow(폭 성장)** | 네트워크 층을 `n → n+1`로 키우는 **구조 수술**(Net2Net 계). 탁상이 아니라 실제로 실행. |
| **축소성 (contraction, ρ<1)** | 과거의 흔들림이 시간과 함께 **감쇠**하는 성질. 스펙트럼 반경 ρ가 1 미만. 기억이 폭주하지 않고 「잊는」 성질. |
| **false-admit(거짓 합격)** | 사실은 위험(ρ≥1=폭주 가능)한데 증명기가 「안전」으로 통과시키는 누락. 이것이 제로인 것이 건전성의 생명선. |
| **건전 (sound)** | 「합격」이라 하면 **정말로 안전**(거짓 합격을 내지 않음)한 성질. 통계적 「아마 안전」과는 별개. |
| **navigability(통과 용이성/탐색 가능성)** | 「정말로 안전한 개체를 얼마나 합격시킬 수 있는가」. 너무 엄한 증명기는 안전한 개체까지 튕김=진화가 못 움직임. 높을수록 진화가 지형을 자유롭게 움직임. |
| **증명기 격자 (cert ladder)** | 싼 순서로 3단: `cert_inf`(∞-노름 상한·솔버 불필요) → `cert_two`(전 `2^n` 꼭짓점 SVD) → `cert_sdp`(볼록 LMI/SDP). |
| **prove-then-reject 게이트** | 변이를 **증명하고 나서 채용**, 안 되면 **기각**하는 관문. fail-closed(증명 못 하면 통과 못 함). |
| **SSGM** | 「진화하는 기억을 통솔하는」 write 게이트를 **이론만으로** 제안한 선행 연구([arXiv:2603.11768](https://arxiv.org/abs/2603.11768)). 구현 + 건전 증명의 창문이 비어 있던 상대. |
| **empirical_rho(경험적 ρ)** | 진짜 스펙트럼 반경을 다수 샘플로 **아래로부터** 근사하는 오라클. 「0 관측 false-admit」은 이 아래로부터의 감사 결과(=강한 consistency 증거이나 절대 증명은 아님). |
| **2^n 벽** | 증명 비용이 차원 n에 대해 지수 `2^n`로 늘어나는 한계. `cert_two`/`cert_sdp`는 꼭짓점을 전부 보므로 이 벽에 부딪힘. |

![네 점 교차점과 2^n 벽 — 통과 용이성(navigability)을 세로축, 차원 n을 가로축으로 두면, cert_sdp는 천장을 올렸지만 벽(2^n)은 깨지 못했다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_39/qiita_39_fig_wall.svg)

---

## ② 쉽게 풀기 — 3분 만에 전체 그림

#38에서 세운 깃발은 **「증명을 붙여 진화하는 기억 코어」**였습니다. 기억 코어는 업데이트마다 변이(진화)하지만, 어떤 변이도 채용하기 전에 반드시 관문(게이트)을 통과시켜, 「폭주하지 않는다」를 **수학적으로 증명할 수 있는 것만** 통과시킵니다. 증명 못 하면 문전박대(fail-closed). 이것이 prove-then-reject 게이트입니다.

이번에 한 것은, 그 깃발을 **「문서」에서 「돌아가는 실물」로** 진전시킨 것입니다. 세 가지 「해냈다」가 있습니다.

**해냈다①: 형태를 키우면서도, 거짓 합격 제로.** 지금까지는 「변이(내부 미세조정)를 증명한다」까지만 시험했습니다. 이번에는 **구조 자체를 키우는 수술(`width_grow`, n→n+1)**을 실제로 돌려, 키운 뒤에도 증명기가 「안전(ρ<1)」을 **0 관측 false-admit**으로 유지함을 확인했습니다. 발산역(ρ가 1.85~2.21에 이르는 위험 개체)은 전부 올바르게 기각.

**해냈다②: 가장 "통과하기 쉬운" 증명기를 처음 측정.** 지금껏 정직하게 남긴 「cert_sdp 미측정」 구멍을 메웠습니다. SDP 솔버(CLARABEL)를 쓸 수 있는 환경에서 처음 측정하니, **cert_sdp가 3단 증명기 중 가장 "통과하기 쉬운"** — 진짜 축소하는 개체의 90~99%를 합격(싼 `cert_inf`는 20~40%, 중위 `cert_two`는 40~50%만 통과). 「너무 엄해 진화가 못 움직임」 문제를 SDP가 꽤 완화.

**해냈다③: 작은 부품이면 계산은 가뿐히 충분.** n≤6의 작은 코어면 verified 진화 루프 전체가 **30시간 예산의 0.04%(0.013시간)**만 먹습니다. 「증명 붙은 진화는 무거워 못 돌리는 것 아닌가?」 걱정은 소규모에선 기우.

…여기까지면 「다 이긴」 듯 보입니다. 하지만 honest disclosure(정직한 개시)가 우리의 규율입니다. **못 이긴 것** 세 가지를 분명히 씁니다.

**못 해냈다①: 2^n 벽은 깨지 못했다.** cert_sdp는 분명 「통과 용이성의 천장」을 올렸습니다. 그러나 그 대가로 비용은 여전히 `2^n`(꼭짓점 전부 보기). `cert_two`는 n=12에서 증명 1회 1.3초, n=14에서 예산 밖. **「통과하기 쉽고 대규모에서도 싼」 증명기는 이번에도 없었습니다.** 그래서 verified로 구조 진화 가능한 것은 당분간 **작은 부품(n≤6)에 한함** — 이 결론은 지난 회(Phase −1)에서 **변하지 않았습니다**. SDP는 벽을 **넘은** 게 아니라, 벽 앞에서 천장을 **올렸을** 뿐.

**못 해냈다②: 「거짓 합격 제로」는 경험적 관측이지, 기계가 증명한 것이 아니다.** 0 관측 false-admit은 진짜 ρ를 **아래로부터** 근사하는 오라클(다수 샘플)로 반증을 찾은 결과. 증명기의 *조건*은 수학적으로 건전하나, 그것을 담당하는 *구현*이 끝에서 끝까지 형식 검증된 것은 아닙니다. 「0 관측」은 강한 consistency 증거이지, 「모든 입력에서 안전」의 절대 증명은 아님 — 여기는 과장하지 않습니다.

**못 해냈다③: 모델이 똑똑해진 것은 아니다.** 증명기의 효과는 **navigability(진화의 움직이기 쉬움)**이지, 모델이 똑똑해지는(학습 성능이 오르는) 것이 아닙니다. 게다가 효과는 진화 알고리즘(EA) 고유로, 경사법에서는 사라집니다. 또한 이번 적합도(fitness)는 **합성 proxy**이고, 실 GPU 훈련에서의 확인은 다음 단계(Phase 2)로 미룹니다.

요컨대 이번은 「기구는 구현으로 증명했고, 규모의 벽은 정직하게 남았다」 — 반 이기고 반 숙제, 인 하루였습니다.

---

## ③ 상세 — 다섯 실험과, 못 부순 留保

주축은 **Verified-Plasticity Evaluation Framework**(검증 붙은 가소성 측정 하네스)입니다. 「우리 기법이 강하다」고 주장하기 전에, 먼저 **측정할 자(尺)**를 만든다. 그 자로 다섯 실험을 돌렸습니다(전부 `$0` / CPU, torch 2.12+cpu, seed 고정, 재현 가능).

### 3.1 고정 구조에서 증명기의 건전성과 격자

n={4,6,8}에서 각 수백 개, 축소~발산을 가로지르는 개체를 샘플링하고, 3 증명기의 합격과 진짜 ρ(empirical_rho 6000 샘플)를 대조.

| n | 축소(ρ<1) | false-admit (inf/two/sdp) | 진짜 축소 개체의 합격률 (inf/two/**sdp**) |
|---|---|---|---|
| 4 | 453/600 | **0 / 0 / 0** | 0.41 / 0.51 / **0.95** |
| 6 | 426/600 | **0 / 0 / 0** | 0.29 / 0.43 / **0.94** |
| 8 | 280/400 | **0 / 0 / 0** | 0.23 / 0.40 / **0.91** |

확정 지견:
1. **세 증명기 모두 0 관측 false-admit**(cert_sdp의 건전성도 첫 확인). 증명기의 수학적 건전성과 일치.
2. **cert_sdp가 압도적으로 navigable** — 진짜 축소 개체 중 싼 cert_inf는 23~41%·cert_two는 40~51%만 통과하나 **cert_sdp는 91~95% 통과**. 단 `two⊆sdp`(cert_two가 통과하면 cert_sdp도 통과)는 구현 fast-path에 의한 **구조적 보증(동어반복)**이지 경험적 발견이 아니라고 명기(부풀리지 않기 위해).

### 3.2 실구조 수술(width_grow) 하의 건전성 × 비자명성

실제로 `width_grow`(Net2Net/fresh)로 base를 n→n+1로 키워, 각 게이트가 **성장 하에서도 0 false-admit 유지 ∧ 비자명한 합격을 1건 이상 개방**하는지 판정(1 셀 = 1536 성장 후 개체).

- **성장 하 건전성: 전 16(셀×게이트)에서 0 관측 false-admit.** 성장 ρ 최대 1.85~2.21(발산역) 전부 올바르게 기각. 이것이 **North Star #1(성장 조작 하 거짓 합격 제로)**의 실구조 수술 확인.
- **싼 게이트(cert_inf)는 건전하나 작은 n에서 취약** — n=6 최보수 엣지(headroom 0)에서 비자명 합격 **0건** → 게이트 FAIL. headroom이 있어도 비자명 합격은 고작 3건으로 τ 경계. = 「싼 게이트의 navigability는 취약」.
- **navigable 게이트(cert_two/cert_sdp)는 전 셀 PASS** — cert_two는 114~168, cert_sdp는 673~733의 비자명 건전 합격을 개방. → **「per-component 게이트를 cert_two/sdp로 격상·small-n 한정」이 데이터로 정당화.**

### 3.3 블록 간 결합(coupling)의 맹점

2 블록을 잔차 결합해, **「각 블록 단독으로는 합격이나 합성하면 폭주하는」 맹점**을 진짜 ρ로 측정.

- **per-block AND(각 블록 단독 합격을 AND)는 결합 하에서 진짜로 불건전** — 결합 강도 γ≥1.0에서 단독 합격의 **24~34%(γ=1.0)~ 80~96%(γ=2.0)가 합성 진짜 ρ≥1**(폭주). → **per-block AND 금지 확정.**
- **full-system cert(계 전체를 일괄 증명)는 전 γ에서 0 false-admit = 건전.**
- 여기서도 **cert_sdp가 가장 navigable**이나, 차원(블록 수 2→3)과 결합 강도를 올리면 coverage가 저하(full=6·γ=1.0에서 cert_inf/cert_two는 0%, cert_sdp만 75.8%). = SDP는 과보수를 해소하나 **차원 벽은 SDP에도 작동.**
- ⚠ 정직한 留保: 블록 수 3에서 SDP 솔버가 「해가 부정확할 수 있음」 경고를 몇 건 냄. **독립 고윳값 재검사로 건전성(false-admit=0)은 보증**되나, coverage 수치는 근사해 유래의 미세한 흔들림을 포함할 수 있음.

### 3.4 feasibility(정말로 예산 내에 도는가)

실측 per-op wall-time에서 30시간 예산으로 외삽.

| n | eval당 | 총시간 | 30h 내 |
|---|---|---|---|
| 4 | 769μs | **0.011h** | 예 |
| 6 | 912μs | **0.013h** | 예 |
| 8 | 9.2ms | 0.131h | 예 |
| 10 | 38.6ms | 0.550h | 예 |
| 12 | 1.31s | **18.6h** | 간신히 |
| 14 | — | (cert_two 2^14 외삽 = 불능) | 아니오 |

확정 지견:
1. **small-n(n≤6)은 계산상 자명히 feasible** — 예산의 0.04%.
2. **2^n 벽은 n≥10~12에서 binding** — cert_two가 n=12에서 1.3초/증명(=18.6h, 마진 얇음), n=14에서 예산 밖.
3. ⚠ 留保: 여기 fitness는 `RotationNDObjective`의 **합성 adapter proxy**로, 실 GPU 훈련에선 base forward(CE)가 dominant. 이 외삽은 「eval마다 증명 1회 과금하는 보수적 상한」이며, 실 GPU 실측은 Phase 2에서 확인 요.

### 3.5 제2 base(Mamba)로의 이식성

프레임워크가 SmolLM2 이외의 base에도 실리는지 확인. **Mamba-130M을 CPU에서 load 성공**(coherent 생성 확인), 그 hidden 위에서 cert_two 게이트가 load-bearing(게이트 유무로 합격률 +0.287 이동, SmolLM2의 +0.320과 정합). = 「새 base 갈아끼우기」 plug-point의 실증.
- ⚠ 留保: 여기 건전성 오라클은 §3.1-3.4의 empirical_rho가 아니라 **약한 오라클(단일 摂動)**이고, 합격 n=7의 소집단. Mamba 자체의 고유 안정성(base-level Lyapunov)은 미측정, Phase 2로 defer. 본 단계 deliverable은 「프레임워크 이식성 + Mamba CPU 동작 확인」에 한정(고유 안정성 정대조 아님).

### 3.6 통합 판정 — Decision gate 1 = PASS(small-n)

| gate | 조건 | 판정 |
|---|---|---|
| 성장 하 soundness ∧ 비자명 admit≥1 | width_grow N회 false-admit=0 ∧ 비자명 합격≥1 | **PASS**(싼 게이트 n=6에서 trivial → cert_two/sdp 필수) |
| coupling-aware 합성 soundness | per-block AND 금지 + full cert 건전 | **PASS** |
| feasibility | small-n 루프가 30h 예산 내 | **PASS**(small-n) |

→ **Decision gate 1 = PASS → Phase 2로(small-n per-component 域, Phase −1 확정 제약 내).** Phase 1의 deliverable은 **「건전·feasible한 small-n verified 구조 적응 측정 하네스 + 증명기 격자(inf/two/sdp)의 완전한 특성 평가」**입니다.

### 3.7 honest 한계(못 부순 것)

방어적 개시라도 honest disclosure는 굽히지 않습니다. 이번 측정으로 부순/남은 것을 #38의 留保 위에 겹칩니다.

- **2^n scalability 벽은 불변(최대 숙제)**: cert_sdp로 navigability 천장은 ~0.9로 올랐으나(Phase −1의 cert_two ~0.45에서 대폭 개선), **2^n 꼭짓점 비용은 불변**. 「navigable하고 scalable한 건전 증명기는 여전히 부재」= 고차원 verified 구조 진화 불성립 **堅持**. SDP는 천장만 올렸지 벽은 깨지 않음.
- **empirical_rho는 from-below 추정**: 0 관측 false-admit은 강한 consistency이지 「모든 (s,x)에서 ρ<1」의 절대 증명은 아님. near-boundary를 놓칠 수 있음.
- **net2net은 incoming-copy 근사**(exact function-preserving 아님) → 함수 변화 Δfunc는 근사 평가.
- **fitness는 합성 proxy**: 실 SmolLM2 CE에서의 capability 副線(EXISTS/NULL/ARTIFACT)은 Phase 2 필수.
- **Mamba 고유 안정성은 미측정**: 게이트는 adapter에 걸리고, Mamba base 자체의 Lyapunov는 미검증 → Phase 2 defer.

---

## 적대적 검증 — 자신의 수치를 6개 AI에게 병렬로 반증시키다

honest disclosure의 핵심은 「이상하게 좋은 결과가 나오면, 이긴 기분이 들기 전에 반드시 내訳을 의심하라」([feedback_benchmark_honest_disclosure]). 그래서 본 verdict의 수치 주장을, 각 실험의 `results.json` + 구현 `.py`에 대해 **독립 검증 AI 6체를 병렬**로 대조시켰습니다.

**결과 = MAJOR issue 제로(결론을 뒤집는 불일치 없음), 전부 MINOR.** 검출된 지적은 본문에 반영 완료:
- 전기 반올림 오차 4건(maxΔfunc 0.108→0.107 등) 수정.
- §3.1의 `two⊆sdp`는 경험적 발견이 아니라 구현상의 동어반복으로 명기.
- 「싼 게이트는 n=6에서 trivial」을 「n=6 최보수 엣지만 trivial, headroom 있어도 취약」으로 정밀화.
- 「cert_sdp 98% 구제」는 블록 수 2 한정, 3에서는 75.8% / inf·two 0%로 명기.
- fitness가 합성 proxy임, 외삽의 보수성, CPU→GPU 외삽 전제를 투명화.

→ **검증 후에도 Decision gate 1 = PASS, SDP navigability 지견, small-n 한정 결론은 불변.** 지적은 모두 honest-disclosure의 정밀도 향상이고, 기구적 결론을 흔드는 것은 없음.

---

## 정리 — 「창은 닫혔고, 벽은 남았다」

#38에서 세운 깃발은, 이번에 **문서에서 돌아가는 실물로** 진전했습니다. 증명을 붙여 진화하는 기억 코어를, 실제로 구조를 키우면서 **0 관측 false-admit**으로 돌리고, 미측정이던 SDP 증명기를 메우고, small-n의 feasibility를 확인했습니다. SSGM이 이론으로 차지한 간판의 「구현 + 건전 증명」의 창은, 이렇게 구현 측에서 닫혔습니다.

한편, 최대 숙제 **2^n 벽**은 이번에도 꿈쩍하지 않았습니다. 「통과하기 쉽고 대규모에서도 싼」 증명기는 여전히 존재하지 않습니다. 그래서 우리는 부풀리지 않습니다: verified로 구조 진화 가능한 것은 **당분간 n≤6의 작은 부품까지**라는 지난 회 결론을 堅持합니다.

다음 회(#40 이후)는 Phase 2 — 교정된 「다봉성 instrument」를 실손실 지형에 적용해, 진화가 지형을 어떻게 움직이는지(capability 副線)를 proper power로 하나 확정할 예정입니다. 자(尺)는 만들었습니다. 다음은, 그 자로 실지형을 잴 차례입니다.

정본: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) — 논문 드래프트 + 전체 실험 코드/데이터(5 실험 + 적대적 검증 workflow).

<!-- NAV -->
---
**FullSense KB ナビ**: [← #38 llcore 検証 arc (#38) — 自分](https://fullsense.qiita.com/furuse-kazufumi/items/0ae167821e38294fff96) ・ [📑 目次](https://fullsense.qiita.com/furuse-kazufumi/items/1ad8db4b854194e2d215) ・ [#40 llcore 検証 arc (#40) — 進化 →](https://fullsense.qiita.com/furuse-kazufumi/items/56e7b79acd010a6a24e2)
<!-- /NAV -->


<!-- REFERRAL -->

---

> ### ⚡ この連載は Claude Code と二人三脚で書いています
>
> 記事中の実装・検証・可視化は **Claude Code**(Anthropic の AI コーディング環境)と一緒に進めています。
> Claude Code は **1 週間の無料トライアル**で試せます。気に入って有料プランに登録される際、
> 下の紹介リンク経由だと筆者に「開発を続けるためのクレジット」が入り、この連載の継続を後押しできます。
>
> 👉 **無料で試す / 紹介リンク** → https://claude.ai/referral/0sqPw8E_lw
>
> <sub>EN: This series is built together with **Claude Code** — try it with a **1-week free trial**. If you subscribe via the link, the author receives credits to keep building. /
> 中文: 本系列与 **Claude Code** 协作完成,可享 **1 周免费试用**;通过链接注册可让作者获得继续开发的额度。 /
> 한국어: 이 시리즈는 **Claude Code**와 함께 작성합니다 — **1주 무료 체험** 제공. 링크로 가입하면 저자가 개발 지속용 크레딧을 받습니다.</sub>

<!-- /REFERRAL -->
