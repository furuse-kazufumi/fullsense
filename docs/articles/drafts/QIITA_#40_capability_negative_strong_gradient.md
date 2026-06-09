---
title: 'llcore 検証 arc (#40) — 進化が「20戦20勝」した日、でも"強い対戦相手"を出したら幻だった: capability を測ったら NEGATIVE、価値は guarantee に確定'
tags: [FullSense, llcore, Singularity, AI, 解説]
private: true
updated_at: '2026-06-10'
slide: false
ignorePublish: false
---

> **本記事は日本語ドラフト**(private-first)。English / 中文 / 한국어 版は publish 前に展開予定。

# 日本語

## この記事は何か — 「勝ったと思った瞬間に、自分のフレームワークが自分を止めた」報告

前回(#39)で私たちはこう締めくくりました。「証明つきで進化する記憶コアは作れた。ただし n≤6 の小さな部品まで。スケーラビリティの壁はびくともしなかった」。

そして今回(2026 年 6 月 10 日)は、ずっと後回しにしてきた **本丸の問い** に答えました。

> **「で、その『進化する記憶』は、ちゃんと賢くなるの? 勾配法(普通の学習)より強いの?」**

結論を 1 行で言います。**「実在の小型 LLM が作る本物の地形で、進化は普通の勾配法に 20戦20勝した。一瞬、勝ったと思った。でも自分のフレームワークの規律に従って『強い勾配』を出したら、その勝利は幻だった」**。

この記事は、研究で一番こわい瞬間 — **「異常に良い結果が出てしまった瞬間」** — に、勝った気になる前にどう自分を疑ったか、の記録です。いつもの ①用語 → ②かみくだき → ③詳細 で、盛らずに書きます。最後に、自分の数値主張を **検証 AI に並列で反証させた** 結果(MAJOR な不一致ゼロ)も開示します。

正本データ: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)(全実験コード/データ + verdict)。

---

## ① 用語ミニ辞典(本文で詰まらないために)

| 用語 | ひとことで |
|---|---|
| **capability(性能)** | 「賢くなるか」。ここでは次に来るものを当てる予測の良さ(交差エントロピー=CE が小さい)。 |
| **guarantee(保証)** | 「暴走しないか」。証明つきで安定(収縮 ρ<1)を保てること。本研究の主軸。**この 2 つを混同しないのが honest-disclosure の生命線。** |
| **MAP-Elites(進化)** | 多様な解を碁盤の目に貯めながら探す進化的探索。今回の「進化」側。 |
| **finite-diff 勾配(弱い勾配)** | 関数値を少しずらして傾きを **推定** する素朴な勾配法。1 ステップに次元数+1 回の評価が要る=**遅くて弱い**。 |
| **解析(exact)勾配(強い勾配)** | 自動微分(backprop)で **正確な** 傾きを 1 回で得る勾配法。実際の LLM 学習が使うのはこちら。今回の決め手。 |
| **meta-gate** | 「進化が勝った」ように見えたとき、**もっと強い対戦相手**を出して利得が消えないか確かめる関門。消えれば幻(ARTIFACT)。 |
| **ARTIFACT(まやかし)** | 本物の性能差ではなく、**対戦相手が弱かったせい**で生まれた見かけの勝利。 |
| **ラングトンの蟻** | 単純な規則なのに、しばらく無秩序に見え、突然秩序が現れる有名な系。「見かけ」と「本質」がズレる比喩として使う。 |

---

## ② かみくだき — 「弱い相手に20連勝しても、何も言えない」

野球で例えます。あなたのチーム(進化)が、ある相手(finite-diff 勾配)に **20戦20勝** しました。強い。文句なし。

…でも、その相手が **草野球チーム** だったら? 20連勝は「あなたが強い」証拠になりません。「相手が弱かった」だけかもしれない。

研究でこれをやると大事故になります。「進化が勾配に勝った!」と論文に書いて、後で「いや、あなたが比べた勾配法が弱すぎただけです」と言われる。これが **capability の罠** です。

そこで私たちのフレームワークには、最初から **掟(meta-gate)** が入れてあります。

> **進化が勝ったら、勝った気になる前に "プロ" を呼んで再戦せよ。**

今回その "プロ"(解析勾配=実際の LLM 学習が使う正確な勾配)を呼びました。結果:

- 草野球(finite-diff)相手: 進化 **20勝0敗**(平均 CE で +0.029 リード)
- プロ(解析勾配)相手: 進化 **1勝19敗**(プロが逆に勝ち越し)

つまり **進化が勝てたのは相手が弱かったから**。強い勾配を出したら、勾配の方が良かった。**「進化が賢くなる(capability)」は言えない。**

ここで大事なのは、**負けたこと自体は失敗ではない** という点です。私たちのフレームワークの価値は最初から「賢くなる」側(capability)ではなく、**「暴走しない」側(guarantee)** に置いています。今回の結果は、その方針が **データで正しかった** ことを意味します — 賢さで売らなくて正解だった、と。

---

## ③ 詳細 — 実在 LLM の地形で、何を、どう測ったか

### 3-1. 地形を「合成」から「本物」へ

前回までの capability 実験は、**人工の多峰地形**(山がいくつもある作り物)で測っていました。正直な留保として「これは実在 LLM の損失地形ではない」と残していました。

今回はそこを **実在の SmolLM2-135M**(Apache-2.0 の小型 LLM)で詰めました。手順:

1. SmolLM2 に文章を通し、中間層(layer 15)の **本物の内部表現(hidden state)** を取り出す。
2. それを小さな次元(n=6)に射影し、**「次に来る内部表現のクラスタ」を当てる CE 地形**を作る。これは合成ガウスではなく、**モデル自身の内部ダイナミクス由来の本物の予測タスク**。
3. その地形の上で、進化(MAP-Elites)・ランダム・弱い勾配・**強い解析勾配**を **同じ予算**(評価回数)で走らせ、**未観測の文(held-out)** での予測精度を 20 シードで比べる。

### 3-2. 結果(held-out 平均 fitness = −CE、高いほど良い)

| 手法 | held-out 平均 | ひとこと |
|---|---|---|
| **強い解析勾配(torch Adam)** | **−1.446** | **全手法で最良** |
| 進化(MAP-Elites) | −1.454 | 2 位 |
| ランダム | −1.473 | |
| 弱い勾配(restart 多め) | −1.481 | |
| 弱い勾配(finite-diff) | −1.483 | **最下位** |
| 進化+ρ<1 gate | −1.483 | gate を掛けると探索が制約され finite-diff 並みに |

- 進化 vs **弱い勾配**: 平均差 +0.029、**20勝0敗**、p<1e-6 → 4条件 AND **成立**(一見 EXISTS)。
- 進化 vs **強い解析勾配**: 平均差 −0.008、**1勝19敗**、p=3.5e-4 で **勾配が逆転** → 4条件 AND **不成立**。

**→ 判定 = ARTIFACT+NEGATIVE。** 進化の勝ちは弱い対戦相手のせい。強い勾配では勾配 ≥ 進化 = **実在 LLM 地形でも capability は NEGATIVE**。

### 3-3. 両地形で一貫することも確認した(cross-check)

「じゃあ前回までの合成地形の『引き分け(NULL_TIE)』も、弱い勾配のせいで過小評価だったのでは?」 — その疑いも **データで確かめました**。合成地形にも強い解析勾配を足して再走させると、**解析勾配が最高平均**(0.575 > 進化 0.535)。ただし合成地形は運の振れ(分散)が大きく、ペア検定では引き分け止まり。実在地形は振れが小さいぶん、勾配の優位が **統計的に有意**(19/20)まで届いた。

**結論: capability NEGATIVE は両地形で一貫**(強い勾配が両方で最高)。違いは分散だけ。

### 3-4. 「枠組みが本物を見抜く」側は PASS

capability は売れない。では何が立つのか — **guarantee(安全性の判別力)** です。同じセッションで 3 つ確認しました。

- **判別力**: 「危険な構造」を経験ベースの gate は **84% 見逃す**(暴走するのに『安全』と通す)。**証明器(sound certificate)は 0% 見逃し**。とくに cert_sdp は誤許可ゼロかつ過剰な棄却も 4.6% だけ=**健全かつ最も通りやすい**。
- **base レベルの判別**: Mamba(構造的に安定な SSM)は全 24 層で固有安定 → 自明に合格。標準 Transformer の SmolLM2 は状態再帰を持たない → **安全性は後付けの gate で初めて課される**。枠組みは「安全な土台」と「gate が要る土台」を base レベルで分けられる。
- **拡張性(framework 性)**: 基質・目的・証明器の 3 つの差し込み口を、**1 オブジェクト差し替え**で載せ替えられる(単体テスト 17 件 green)。ただし「多様性が汎化を助ける」仮説は **NULL**(立たず)— これも正直に開示。

### 3-5. 「動き」で見せると — ノルムは暴れない、感度だけが暴れる

おまけの発見。この基質は tanh で状態が常に有界なので、**不安定でも出力ノルムは発散しません**。さらに、ρ≈2.9 の暴走する個体ですら、ある 1 本の軌道では摂動が **減衰して見える**(まさにラングトンの蟻=見かけが本質を裏切る)。状態ノルムを見ても、有限ホライズンの「忘却テスト」をしても、**ρ≥1 は見抜けない**。見抜けるのは **証明器の最悪ケース評価(box-sup)だけ**。デモはこの「経験は騙され、証明器だけが見抜く」を 1 枚の図にしました(`phase2_demo_gate_discrimination.svg`)。

---

## honest disclosure — 一番こわい瞬間に、何を疑ったか

この研究で一番危なかったのは、**「進化 20戦20勝」を見た瞬間**です。SNS 映えする見出しが一瞬よぎりました(「進化が勾配に勝つ実在 LLM 地形を発見!」)。

そこで止めたのは、新しいひらめきではなく、**最初から入れてあった掟(meta-gate)** です。「勝ったら強い相手を呼べ」。呼んだら負けた。だから書けない。

これは負けの報告ではなく、**フレームワークが機能した報告** です。もし meta-gate が無ければ、私は嘘を publish していました。「異常に良い結果は、勝った気になる前に内訳を疑う」— この規律が、データの上で実際に false-positive を 1 件、止めました。

残る正直な留保:
- 実 vocab の full-softmax CE ではなく hidden クラスタ CE の proxy(小さい n では full-vocab が退化するため)。
- gate を掛けると実在地形では性能が −0.028 落ちる(可塑性を測定可能に削る)。ただし進化に capability 優位が無いので結論には影響しない。
- 「強い勾配が最良」は backprop が無料で正確な勾配を得られる前提。実際の LLM 学習はまさにそれなので、現実的な比較。

## 検証 — 自分の主張を AI に反証させた(MAJOR 0)

最後に、3 つの実験の数値主張を **独立した検証 AI に並列で反証** させました。とくに本丸(capability)は、**検証 AI が実際に SmolLM2 を読み込んで 3 シード独立再走** し、「強い勾配が進化を上回る」を決定論的に再現。**重大な不一致(MAJOR)ゼロ**。指摘はすべて再現性・言い回し・留保の精度向上で、結論を覆すものはありませんでした(1 件、検証用乱数が再現しない欠陥を見つけたので、その場で決定論化して再走しました)。

---

## まとめ — 「進化可能な LLM」の正体

3 回(#38→#39→#40)の弧で、私たちはこう着地しました。

- **#38**: 防御的開示 — 「証明つき記憶」の窓は理論で開いた。
- **#39**: 窓は実装で閉じた。でも **スケーラビリティの壁** はびくともしなかった(verified に進化できるのは n≤6 まで)。
- **#40(今回)**: では賢くなるのか? → **NO**。実在 LLM 地形でも、強い勾配が進化に勝つ。**capability は売れない。**

だから「進化可能な LLM」の正体は、**「進化が性能で勝つ AI」ではなく、「online で構造を変えても暴走・破滅的忘却しないことを、証明つきで保証・測定する枠組み」** です。地味です。でも、**賢さを盛らずに安全性で勝負する** と決めた以上、これが正直な姿です。

次回は、この枠組みを「ラングトンの蟻の幻を見抜く眼」という比喩で総括する予定です。経験は見かけに騙される。証明器だけが本質を見る — その 1 点に、3 回分の honest disclosure が全部つながります。

---

<a id="english"></a>
# English

## What this is — "the moment I thought I'd won, my own framework stopped me"

In the last installment (#39) we concluded: "We built a memory core that evolves *with a proof* — but only for small parts, n≤6. The scalability wall didn't budge."

This time (2026-06-10) we finally answered the question we'd been putting off:

> **"So does this 'evolving memory' actually get *smart*? Is it better than gradient descent (ordinary learning)?"**

One-line answer: **"On a real terrain made by an actual small LLM, evolution beat ordinary gradient descent 20 games to 0. For a moment I thought I'd won. Then, following my own framework's discipline, I called in a *strong* gradient — and the victory turned out to be an illusion."**

This is a record of the scariest moment in research — **the moment an abnormally good result appears** — and how I doubted myself before celebrating. Same order as always: ① terms → ② plain words → ③ details. No embellishment. At the end I disclose the result of having **verifier AIs adversarially refute** my numerical claims in parallel (zero MAJOR discrepancies).

Source data: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) (all experiment code/data + verdicts).

---

## ① Mini-glossary

| Term | In one line |
|---|---|
| **capability** | "Does it get smart?" Here, how well it predicts what comes next (low cross-entropy / CE). |
| **guarantee** | "Does it avoid blowing up?" Provably stable (contraction ρ<1). **The lifeline of honest-disclosure is never confusing these two.** |
| **MAP-Elites (evolution)** | Evolutionary search that keeps a grid of diverse solutions. The "evolution" side. |
| **finite-diff gradient (weak)** | Naively *estimates* the slope by nudging values. Costs dim+1 evals per step = **slow and weak**. |
| **analytic (exact) gradient (strong)** | Gets the *exact* slope in one pass via autodiff (backprop). What real LLM training actually uses. The decider here. |
| **meta-gate** | When evolution "wins," bring in a **stronger opponent** and check whether the gain survives. If it vanishes, it was an illusion (ARTIFACT). |
| **ARTIFACT** | A fake win caused by the **opponent being weak**, not a real performance gap. |
| **Langton's ant** | A famous system, simple rules, that looks chaotic then suddenly orders. A metaphor for "appearance ≠ essence." |

---

## ② Plain words — "winning 20 straight against a weak opponent says nothing"

A baseball analogy. Your team (evolution) beats an opponent (finite-diff gradient) **20 games to 0**. Strong, no complaints.

…but what if that opponent was a *sandlot* team? 20 straight wins is no proof *you* are strong — maybe the *opponent was weak*.

Do this in research and you get a disaster. You write "evolution beat gradient!" in a paper, and later someone says "no, the gradient method you compared against was just too weak." This is the **capability trap**.

So our framework had a **rule (meta-gate)** baked in from the start:

> **If evolution wins, call in the "pro" for a rematch before you celebrate.**

We called the pro (analytic gradient = the exact gradient real LLM training uses). Result:

- vs sandlot (finite-diff): evolution **20–0** (+0.029 mean CE lead)
- vs pro (analytic gradient): evolution **1–19** (the pro wins)

So **evolution won only because the opponent was weak**. With a strong gradient, gradient was better. **"Evolution gets smarter (capability)" cannot be claimed.**

The key point: **losing here is not a failure.** Our framework's value was never on the "smart" side (capability) — it's on the **"doesn't blow up" side (guarantee)**. This result means that choice was **right, in data** — good thing we didn't sell on smarts.

---

## ③ Details — what we measured on a real LLM terrain, and how

### 3-1. From "synthetic" to "real" terrain

Earlier capability experiments measured on a **synthetic multi-peaked terrain** (an artificial landscape). We honestly flagged: "this is not a real LLM loss terrain."

This time we closed that gap with the **real SmolLM2-135M** (an Apache-2.0 small LLM):

1. Run text through SmolLM2, extract the **real internal representations (hidden states)** at layer 15.
2. Project to small dimension (n=6) and build a **CE terrain that predicts "the cluster of the next internal representation"** — not synthetic Gaussians, but a **real prediction task derived from the model's own internal dynamics**.
3. On that terrain, run evolution (MAP-Elites) / random / weak gradient / **strong analytic gradient** at the **same budget** (eval count), comparing prediction on **held-out (unseen) sentences** across 20 seeds.

### 3-2. Results (held-out mean fitness = −CE, higher is better)

| Method | held-out mean | Note |
|---|---|---|
| **strong analytic gradient (torch Adam)** | **−1.446** | **best of all** |
| evolution (MAP-Elites) | −1.454 | 2nd |
| random | −1.473 | |
| weak gradient (more restarts) | −1.481 | |
| weak gradient (finite-diff) | −1.483 | **last** |
| evolution + ρ<1 gate | −1.483 | gating constrains search to finite-diff level |

- evolution vs **weak gradient**: +0.029 mean, **20–0**, p<1e-6 → 4-condition AND **passes** (looks like EXISTS).
- evolution vs **strong analytic gradient**: −0.008 mean, **1–19**, gradient wins at p=3.5e-4 → 4-condition AND **fails**.

**→ Verdict = ARTIFACT+NEGATIVE.** Evolution's win was due to a weak opponent. With a strong gradient, gradient ≥ evolution = **capability is NEGATIVE even on a real LLM terrain**.

### 3-3. We also checked it holds on both terrains (cross-check)

"Then wasn't the earlier synthetic 'tie (NULL_TIE)' also understated by the weak gradient?" — we checked that **in data** too. Adding the strong analytic gradient to the synthetic terrain, **the analytic gradient had the best mean** (0.575 > evolution 0.535). But the synthetic terrain has high run-to-run variance, so the paired test stayed a tie. The real terrain, with lower variance, let the gradient advantage reach **significance** (19/20).

**Conclusion: capability NEGATIVE is consistent across both terrains** (strong gradient best on both). The only difference is variance.

### 3-4. The "does the framework see the real thing" side PASSES

Capability can't be sold. So what stands up — the **guarantee (discriminative power)**. Three confirmations in the same session:

- **Discrimination**: an experience-based gate **misses 84%** of "dangerous structures" (passes diverging ones as "safe"). A **sound certificate misses 0%**. In particular cert_sdp has zero false-admits and only 4.6% over-rejection = **sound and most navigable**.
- **Base-level discrimination**: Mamba (a structurally stable SSM) is intrinsically stable across all 24 layers → trivially passes. The standard Transformer SmolLM2 has no state recurrence → **safety must be imposed by a bolted-on gate**. The framework cleanly separates "safe base" from "needs-a-gate base."
- **Extensibility (framework-ness)**: the three plug-points (substrate / objective / certifier) swap with a **single object** (17 unit tests green). But the hypothesis "diversity helps generalization" is **NULL** (doesn't hold) — also disclosed honestly.

### 3-5. Shown "in motion" — the norm doesn't explode, only the sensitivity does

A side finding. This substrate keeps the state bounded via tanh, so **even when unstable, the output norm does not diverge**. Worse, even a diverging individual (ρ≈2.9) has its perturbation **appear to decay** on one trajectory (exactly Langton's ant — appearance betrays essence). Watching the state norm, or a finite-horizon "forgetting test," **cannot catch ρ≥1**. Only the **certificate's worst-case (box-sup) evaluation** can. The demo captures this "experience is fooled, only the certificate sees" in one figure (`phase2_demo_gate_discrimination.svg`).

---

## Honest disclosure — what I doubted at the scariest moment

The most dangerous moment was **seeing "evolution 20–0."** An SNS-friendly headline flashed by ("Found a real LLM terrain where evolution beats gradient!").

What stopped me wasn't a new insight — it was the **rule baked in from the start (meta-gate)**: "if you win, call the strong opponent." I called, and lost. So I can't write it.

This is not a report of losing — it's a report of **the framework working**. Without the meta-gate, I would have published a falsehood. "Abnormally good results: doubt the breakdown before celebrating" — that discipline actually stopped one false positive, in data.

Remaining honest caveats:
- A hidden-cluster CE proxy, not a full-vocab softmax CE (full-vocab degenerates at small n).
- Gating costs −0.028 performance on the real terrain (it measurably trims plasticity). But since evolution has no capability edge, this doesn't change the conclusion.
- "Strong gradient is best" assumes backprop gives exact gradients for free — which is exactly what real LLM training does, so it's a realistic comparison.

## Verification — I had AIs refute my own claims (MAJOR 0)

Finally, I had **independent verifier AIs adversarially refute** the numerical claims of all three experiments in parallel. For the main result (capability), a verifier AI **loaded SmolLM2 itself and re-ran 3 seeds independently**, deterministically reproducing "strong gradient beats evolution." **Zero MAJOR discrepancies.** All findings improved reproducibility / wording / caveat precision, none overturned a conclusion (one verifier found a non-reproducible RNG defect, which I made deterministic and re-ran on the spot).

---

## Wrap-up — what "evolvable LLM" really is

Across three installments (#38→#39→#40) we landed here:

- **#38**: Defensive disclosure — the window for "proof-carrying memory" opened in theory.
- **#39**: The window closed in implementation. But the **scalability wall** didn't budge (verified evolution only up to n≤6).
- **#40 (this one)**: Does it get smart? → **NO.** Even on a real LLM terrain, a strong gradient beats evolution. **Capability can't be sold.**

So "evolvable LLM" really means: **not "an AI where evolution wins on performance," but "a framework that provably guarantees and measures that online structural adaptation doesn't blow up or catastrophically forget."** It's unglamorous. But having decided to **compete on safety, not inflated smarts**, this is the honest picture.

Next time we plan to summarize this framework under the metaphor "an eye that sees through Langton's-ant illusions." Experience is fooled by appearances; only the certificate sees the essence — and on that single point, three installments of honest disclosure all converge.

---

<a id="中文"></a>
# 中文 / <a id="한국어"></a>한국어

(翻訳 follow-up: 中文・한국어 版は publish 前に上記日本語/English と同じ構成で自己完結展開する。)
