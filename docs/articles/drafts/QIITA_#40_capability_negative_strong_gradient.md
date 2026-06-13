---
title: 'llcore 検証 arc (#40) — 進化が「20戦20勝」した日、でも"強い対戦相手"を出したら幻だった: capability を測ったら NEGATIVE、価値は guarantee に確定'
tags: [FullSense, llcore, Singularity, AI, 解説]
private: true
updated_at: '2026-06-10'
slide: false
ignorePublish: false
id: 56e7b79acd010a6a24e2
public_id: 525cd01eda5c1ad707ef
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

<a id="日本語"></a>
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
# 中文

## 这是什么 — "我以为赢了的那一刻，自己的框架把自己拦住了"

上一篇(#39)我们这样收尾："带证明地进化的记忆核心做出来了。但只到 n≤6 的小部件。可扩展性的墙纹丝不动。"

这次(2026 年 6 月 10 日)我们终于回答了一直被搁置的**核心问题**：

> **"那么，这个'会进化的记忆'真的会变聪明吗？比梯度法(普通的学习)更强吗？"**

一句话结论：**"在真实小型 LLM 生成的真实地形上，进化以 20 比 0 战胜了普通梯度法。一瞬间我以为赢了。但遵循自己框架的纪律换上'强对手'之后，那场胜利只是幻觉。"**

这是研究中最可怕的瞬间 —— **"出现了异常好的结果的瞬间"** —— 在得意之前如何怀疑自己的记录。仍按 ①术语 → ②通俗解释 → ③细节 的顺序，不夸张地写。最后公开让**验证 AI 并行反驳**我的数值主张的结果(零个 MAJOR 不一致)。

正本数据：[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)(全部实验代码/数据 + verdict)。

---

## ① 术语小词典

| 术语 | 一句话 |
|---|---|
| **capability(性能)** | "会变聪明吗"。这里指预测下一个的好坏(交叉熵 CE 越小越好)。 |
| **guarantee(保证)** | "会不会失控"。带证明地保持稳定(收缩 ρ<1)。本研究的主轴。**不混淆这两者是 honest-disclosure 的生命线。** |
| **MAP-Elites(进化)** | 在格子里囤积多样解同时搜索的进化式探索。这里的"进化"方。 |
| **finite-diff 梯度(弱)** | 通过微调函数值来**估计**斜率的朴素梯度法。每步要维数+1 次评估＝**慢而弱**。 |
| **解析(exact)梯度(强)** | 用自动微分(backprop)一次得到**精确**斜率。真实 LLM 训练用的就是它。本次的决定因素。 |
| **meta-gate** | 当进化"赢了"，换上**更强的对手**确认增益是否消失。消失则是幻觉(ARTIFACT)。 |
| **ARTIFACT(假象)** | 不是真实性能差，而是因**对手太弱**产生的表面胜利。 |
| **兰顿蚂蚁** | 规则简单却先显混乱后突现秩序的著名系统。比喻"表象 ≠ 本质"。 |

---

## ② 通俗解释 — "对弱对手 20 连胜，什么也说明不了"

用棒球打比方。你的队(进化)对某对手(finite-diff 梯度)**20 比 0**。强，没话说。

…但如果那对手是**业余球队**呢？20 连胜不能证明*你*强 —— 也许只是*对手弱*。

在研究里这么干会出大事故。你在论文里写"进化赢了梯度！"，后来有人说"不，你比的那个梯度法太弱了"。这就是 **capability 的陷阱**。

所以我们的框架从一开始就内置了**规矩(meta-gate)**：

> **进化赢了，得意之前先请"职业选手"再战。**

我们请来了职业选手(解析梯度＝真实 LLM 训练用的精确梯度)。结果：

- 对业余(finite-diff)：进化 **20–0**(平均 CE 领先 +0.029)
- 对职业(解析梯度)：进化 **1–19**(职业反超)

也就是说**进化能赢只是因为对手弱**。换上强梯度，梯度更好。**"进化会变聪明(capability)"无法主张。**

关键在于：**输本身不是失败。** 我们框架的价值从一开始就不在"聪明"一侧(capability)，而在**"不失控"一侧(guarantee)**。这次的结果意味着那个方针**在数据上是对的** —— 没拿聪明来卖是对的。

---

## ③ 细节 — 在真实 LLM 地形上，测了什么、怎么测

### 3-1. 地形从"合成"到"真实"

此前的 capability 实验在**人工多峰地形**(造出来的有多个山的地貌)上测。我们诚实地留了保留："这不是真实 LLM 的损失地形。"

这次用**真实的 SmolLM2-135M**(Apache-2.0 小型 LLM)补上：

1. 让文本通过 SmolLM2，取出中间层(layer 15)的**真实内部表示(hidden state)**。
2. 投影到小维度(n=6)，构造**预测"下一个内部表示的簇"的 CE 地形** —— 不是合成高斯，而是**源自模型自身内部动态的真实预测任务**。
3. 在该地形上，用同样的预算(评估次数)跑进化(MAP-Elites)/随机/弱梯度/**强解析梯度**，在**未见过的句子(held-out)**上以 20 个种子比较。

### 3-2. 结果(held-out 平均 fitness = −CE，越高越好)

| 方法 | held-out 平均 | 备注 |
|---|---|---|
| **强解析梯度(torch Adam)** | **−1.446** | **全部最佳** |
| 进化(MAP-Elites) | −1.454 | 第 2 |
| 随机 | −1.473 | |
| 弱梯度(多重启) | −1.481 | |
| 弱梯度(finite-diff) | −1.483 | **最末** |
| 进化+ρ<1 gate | −1.483 | 加 gate 后探索被约束到 finite-diff 水平 |

- 进化 vs **弱梯度**：+0.029 平均，**20–0**，p<1e-6 → 4 条件 AND **成立**(看似 EXISTS)。
- 进化 vs **强解析梯度**：−0.008 平均，**1–19**，梯度以 p=3.5e-4 反超 → 4 条件 AND **不成立**。

**→ 判定 = ARTIFACT+NEGATIVE。** 进化的胜利源于对手弱。换强梯度，梯度 ≥ 进化 = **即便在真实 LLM 地形上 capability 也是 NEGATIVE**。

### 3-3. 还确认了两种地形上一致(cross-check)

"那之前合成地形的'平局(NULL_TIE)'是不是也被弱梯度低估了？" —— 这个疑问也**用数据确认了**。给合成地形加上强解析梯度重跑，**解析梯度平均最高**(0.575 > 进化 0.535)。只是合成地形运气波动(方差)大，配对检验止于平局。真实地形波动小，梯度的优势达到了**显著**(19/20)。

**结论：capability NEGATIVE 在两种地形上一致**(强梯度在两边都最佳)。区别只在方差。

### 3-4. "框架看穿真相"的一侧 PASS

capability 卖不了。那么立得住的是 —— **guarantee(安全性的判别力)**。同一节里确认了三点：

- **判别力**：基于经验的 gate **漏掉 84%** 的"危险结构"(会失控却当作"安全"放行)。**健全证明器漏 0%**。尤其 cert_sdp 零误许且过度拒绝仅 4.6%＝**健全且最易通过**。
- **base 级判别**：Mamba(结构上稳定的 SSM)全 24 层固有稳定 → 自明通过。标准 Transformer 的 SmolLM2 没有状态递归 → **安全性必须靠后加的 gate 才被赋予**。框架能在 base 级分开"安全底座"和"需要 gate 的底座"。
- **可扩展性(framework 性)**：基质·目的·证明器三个插口，可用**单对象替换**载入(单元测试 17 项 green)。但"多样性帮助泛化"的假说为 **NULL**(不成立) —— 也诚实公开。

### 3-5. 用"动"来看 —— 范数不会暴走，只有敏感度暴走

附带发现。这个基质用 tanh 让状态始终有界，所以**即使不稳定，输出范数也不发散**。更甚，ρ≈2.9 的失控个体在某一条轨道上扰动**看起来在衰减**(正是兰顿蚂蚁＝表象背叛本质)。看状态范数、做有限视野的"遗忘测试"，**都看不穿 ρ≥1**。能看穿的只有**证明器的最坏情况评估(box-sup)**。demo 把这"经验被骗、唯证明器能看穿"做成了一张图(`phase2_demo_gate_discrimination.svg`)。

---

## honest disclosure — 最可怕的瞬间，我怀疑了什么

最危险的是**看到"进化 20–0"的瞬间**。一个适合社交媒体的标题闪过("发现进化战胜梯度的真实 LLM 地形！")。

拦住我的不是新灵感，而是**从一开始就内置的规矩(meta-gate)**："赢了就请强对手。"请了，输了。所以不能写。

这不是输的报告，而是**框架奏效的报告**。没有 meta-gate，我就会发布一个谎言。"异常好的结果，得意之前先怀疑内幕" —— 这条纪律，在数据上实实在在地拦下了一个假阳性。

剩余的诚实保留：
- 是隐藏簇 CE 的 proxy，不是全词表 softmax CE(小 n 下全词表会退化)。
- 加 gate 在真实地形上掉 −0.028 性能(可测量地削减可塑性)。但因进化没有 capability 优势，不影响结论。
- "强梯度最佳"的前提是 backprop 免费给出精确梯度 —— 这正是真实 LLM 训练所做的，所以是现实的比较。

## 验证 — 让 AI 反驳我自己的主张(MAJOR 0)

最后，让**独立的验证 AI 并行反驳**三个实验的数值主张。尤其主结果(capability)，验证 AI **自己加载 SmolLM2 独立重跑 3 个种子**，确定性地重现"强梯度胜过进化"。**零个 MAJOR 不一致。** 所有指摘都是改善可复现性/措辞/保留精度，无一推翻结论(一处发现验证用随机数不可复现的缺陷，当场改为确定性并重跑)。

---

## 总结 — "可进化的 LLM"的真面目

三篇(#38→#39→#40)的弧，我们落到这里：

- **#38**：防御性公开 —— "带证明的记忆"的窗在理论上打开。
- **#39**：窗在实现上关闭。但**可扩展性的墙**纹丝不动(带证明地进化只到 n≤6)。
- **#40(本篇)**：那会变聪明吗？→ **不会。** 即便在真实 LLM 地形上，强梯度也胜过进化。**capability 卖不了。**

所以"可进化的 LLM"的真面目是：**不是"进化在性能上取胜的 AI"，而是"对在线改变结构也不失控·不灾难性遗忘这一点，带证明地保证并测量的框架"。** 朴素。但既然决定**不夸大聪明、以安全取胜**，这就是诚实的样子。

下次计划用"看穿兰顿蚂蚁幻象之眼"这一比喻来总结这个框架。经验被表象欺骗；唯证明器看见本质 —— 在这一点上，三篇的 honest disclosure 全部汇聚。

---

<a id="한국어"></a>
# 한국어

## 이 글은 무엇인가 — "이겼다고 생각한 순간, 내 프레임워크가 나를 멈춰 세웠다"는 보고

지난 회(#39)에서 우리는 이렇게 마무리했습니다. "증명을 동반해 진화하는 기억 코어는 만들었다. 다만 n≤6의 작은 부품까지. 확장성의 벽은 꿈쩍도 하지 않았다."

그리고 이번(2026년 6월 10일)에는 계속 미뤄온 **본질적 질문**에 답했습니다.

> **"그래서 그 '진화하는 기억'은 정말 똑똑해지나? 경사법(보통의 학습)보다 강한가?"**

한 줄 결론: **"실재 소형 LLM이 만드는 진짜 지형에서, 진화는 보통 경사법에 20전 20승했다. 한순간 이겼다고 생각했다. 하지만 내 프레임워크의 규율에 따라 '강한 상대'를 내보내자 그 승리는 환상이었다."**

이것은 연구에서 가장 무서운 순간 — **"비정상적으로 좋은 결과가 나온 순간"** — 에, 이겼다고 들뜨기 전에 어떻게 자신을 의심했는지의 기록입니다. 늘 그렇듯 ①용어 → ②쉬운 풀이 → ③상세 순으로, 부풀리지 않고 씁니다. 마지막에 제 수치 주장을 **검증 AI에게 병렬로 반증**시킨 결과(MAJOR 불일치 0)도 공개합니다.

원본 데이터: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)(전체 실험 코드/데이터 + verdict).

---

## ① 용어 미니 사전

| 용어 | 한마디로 |
|---|---|
| **capability(성능)** | "똑똑해지나". 여기서는 다음에 올 것을 맞히는 예측의 좋음(교차 엔트로피 CE가 작음). |
| **guarantee(보증)** | "폭주하지 않나". 증명을 동반해 안정(수축 ρ<1)을 유지함. 본 연구의 주축. **이 둘을 혼동하지 않는 것이 honest-disclosure의 생명선.** |
| **MAP-Elites(진화)** | 다양한 해를 바둑판에 쌓으며 탐색하는 진화적 탐색. 이번의 "진화" 쪽. |
| **finite-diff 경사(약)** | 함숫값을 조금 흔들어 기울기를 **추정**하는 소박한 경사법. 한 스텝에 차원수+1회 평가＝**느리고 약함**. |
| **해석(exact) 경사(강)** | 자동미분(backprop)으로 **정확한** 기울기를 한 번에 얻는 경사법. 실제 LLM 학습이 쓰는 것. 이번의 결정타. |
| **meta-gate** | 진화가 "이겼을" 때 **더 강한 상대**를 내보내 이득이 사라지지 않는지 확인하는 관문. 사라지면 환상(ARTIFACT). |
| **ARTIFACT(눈속임)** | 진짜 성능차가 아니라 **상대가 약했던 탓**에 생긴 겉보기 승리. |
| **랭턴의 개미** | 규칙은 단순한데 한동안 무질서해 보이다 갑자기 질서가 나타나는 유명한 계. "겉보기 ≠ 본질"의 비유. |

---

## ② 쉬운 풀이 — "약한 상대에 20연승해도 아무것도 말할 수 없다"

야구로 비유합니다. 당신 팀(진화)이 어떤 상대(finite-diff 경사)에 **20대 0**. 강합니다. 할 말 없죠.

…그런데 그 상대가 **동네 야구팀**이었다면? 20연승은 *당신이* 강하다는 증거가 못 됩니다 — 그냥 *상대가 약했을* 뿐일지도.

연구에서 이러면 큰 사고입니다. "진화가 경사를 이겼다!"고 논문에 쓰고, 나중에 "아니, 당신이 비교한 경사법이 너무 약했을 뿐"이라는 말을 듣습니다. 이것이 **capability의 함정**입니다.

그래서 우리 프레임워크에는 처음부터 **규율(meta-gate)**이 들어 있습니다.

> **진화가 이기면, 들뜨기 전에 "프로"를 불러 재대결하라.**

그 프로(해석 경사 = 실제 LLM 학습이 쓰는 정확한 경사)를 불렀습니다. 결과:

- 동네야구(finite-diff) 상대: 진화 **20–0**(평균 CE +0.029 리드)
- 프로(해석 경사) 상대: 진화 **1–19**(프로가 역전)

즉 **진화가 이긴 건 상대가 약했기 때문**. 강한 경사를 내자 경사가 더 좋았습니다. **"진화가 똑똑해진다(capability)"는 말할 수 없습니다.**

중요한 건 **지는 것 자체는 실패가 아니라**는 점입니다. 우리 프레임워크의 가치는 처음부터 "똑똑함"(capability)이 아니라 **"폭주하지 않음"(guarantee)** 쪽에 둡니다. 이번 결과는 그 방침이 **데이터로 옳았음**을 뜻합니다 — 똑똑함으로 팔지 않은 게 정답이었다고.

---

## ③ 상세 — 실재 LLM 지형에서 무엇을 어떻게 측정했나

### 3-1. 지형을 "합성"에서 "실재"로

지금까지의 capability 실험은 **인공 다봉 지형**(만들어낸, 산이 여럿인 지형)에서 측정했습니다. 정직한 유보로 "이것은 실재 LLM의 손실 지형이 아니다"라고 남겼습니다.

이번에는 **실재 SmolLM2-135M**(Apache-2.0 소형 LLM)로 메웠습니다.

1. SmolLM2에 문장을 통과시켜 중간층(layer 15)의 **진짜 내부 표현(hidden state)**을 꺼낸다.
2. 작은 차원(n=6)으로 사영해 **"다음 내부 표현의 클러스터"를 맞히는 CE 지형**을 만든다 — 합성 가우스가 아니라 **모델 자신의 내부 동역학에서 유래한 진짜 예측 과제**.
3. 그 지형 위에서 같은 예산(평가 횟수)으로 진화(MAP-Elites)/랜덤/약한 경사/**강한 해석 경사**를 돌려 **미관측 문장(held-out)**에서 20 시드로 비교.

### 3-2. 결과(held-out 평균 fitness = −CE, 높을수록 좋음)

| 방법 | held-out 평균 | 비고 |
|---|---|---|
| **강한 해석 경사(torch Adam)** | **−1.446** | **전체 최고** |
| 진화(MAP-Elites) | −1.454 | 2위 |
| 랜덤 | −1.473 | |
| 약한 경사(재시작 다수) | −1.481 | |
| 약한 경사(finite-diff) | −1.483 | **최하위** |
| 진화+ρ<1 gate | −1.483 | gate를 걸면 탐색이 finite-diff 수준으로 제약 |

- 진화 vs **약한 경사**: 평균 +0.029, **20–0**, p<1e-6 → 4조건 AND **성립**(언뜻 EXISTS).
- 진화 vs **강한 해석 경사**: 평균 −0.008, **1–19**, 경사가 p=3.5e-4로 역전 → 4조건 AND **불성립**.

**→ 판정 = ARTIFACT+NEGATIVE.** 진화의 승리는 상대가 약한 탓. 강한 경사로는 경사 ≥ 진화 = **실재 LLM 지형에서도 capability는 NEGATIVE**.

### 3-3. 두 지형에서 일관됨도 확인(cross-check)

"그럼 이전 합성 지형의 '무승부(NULL_TIE)'도 약한 경사 탓에 과소평가된 것 아닌가?" — 그 의심도 **데이터로 확인**했습니다. 합성 지형에 강한 해석 경사를 더해 다시 돌리니 **해석 경사가 평균 최고**(0.575 > 진화 0.535). 다만 합성 지형은 운의 흔들림(분산)이 커 짝지은 검정에서는 무승부에 그쳤습니다. 실재 지형은 흔들림이 작아 경사의 우위가 **유의**(19/20)에 도달했습니다.

**결론: capability NEGATIVE는 두 지형에서 일관**(강한 경사가 양쪽 모두 최고). 차이는 분산뿐.

### 3-4. "프레임워크가 진짜를 꿰뚫어 본다" 쪽은 PASS

capability는 못 팝니다. 그럼 서는 것은 — **guarantee(안전성의 판별력)**. 같은 세션에서 셋을 확인했습니다.

- **판별력**: 경험 기반 gate는 "위험한 구조"의 **84%를 놓침**(폭주하는데 '안전'으로 통과). **건전한 인증서는 0% 놓침**. 특히 cert_sdp는 오허용 0이고 과잉 기각도 4.6%뿐＝**건전하고 가장 통과하기 쉬움**.
- **base 수준 판별**: Mamba(구조적으로 안정한 SSM)는 24개 층 전부 고유 안정 → 자명히 통과. 표준 Transformer인 SmolLM2는 상태 재귀가 없음 → **안전성은 덧붙인 gate로 비로소 부과**. 프레임워크는 "안전한 토대"와 "gate가 필요한 토대"를 base 수준에서 나눌 수 있습니다.
- **확장성(framework성)**: 기질·목적·인증기 세 꽂이를 **단일 객체 교체**로 실을 수 있음(단위 테스트 17건 green). 단 "다양성이 일반화를 돕는다"는 가설은 **NULL**(성립 안 함) — 이것도 정직하게 공개.

### 3-5. "움직임"으로 보면 — 노름은 날뛰지 않고, 민감도만 날뛴다

부수적 발견. 이 기질은 tanh로 상태를 늘 유계로 하므로 **불안정해도 출력 노름은 발산하지 않습니다**. 게다가 ρ≈2.9의 폭주 개체조차 어떤 한 궤도에서는 섭동이 **감쇠하는 것처럼 보입니다**(바로 랭턴의 개미＝겉보기가 본질을 배신). 상태 노름을 봐도, 유한 지평의 "망각 테스트"를 해도 **ρ≥1을 꿰뚫어 보지 못합니다**. 꿰뚫어 보는 것은 **인증기의 최악 경우 평가(box-sup)뿐**. demo는 이 "경험은 속고, 인증기만 본다"를 한 장의 그림으로 만들었습니다(`phase2_demo_gate_discrimination.svg`).

---

## honest disclosure — 가장 무서운 순간에 무엇을 의심했나

가장 위험했던 건 **"진화 20–0"을 본 순간**입니다. SNS에 어울리는 제목이 스쳤습니다("진화가 경사를 이기는 실재 LLM 지형을 발견!").

멈춰 세운 건 새 영감이 아니라 **처음부터 넣어둔 규율(meta-gate)**입니다. "이기면 강한 상대를 불러라." 불렀더니 졌습니다. 그래서 쓸 수 없습니다.

이것은 패배의 보고가 아니라 **프레임워크가 작동한 보고**입니다. meta-gate가 없었다면 저는 거짓을 publish했을 겁니다. "비정상적으로 좋은 결과는, 들뜨기 전에 내막을 의심하라" — 이 규율이 데이터 위에서 실제로 거짓 양성 하나를 멈춰 세웠습니다.

남은 정직한 유보:
- 전체 어휘 softmax CE가 아니라 은닉 클러스터 CE의 proxy(작은 n에서 전체 어휘는 퇴화).
- gate를 걸면 실재 지형에서 −0.028 성능이 떨어짐(가소성을 측정 가능하게 깎음). 단 진화에 capability 우위가 없으므로 결론에는 무영향.
- "강한 경사가 최고"는 backprop이 정확한 경사를 공짜로 준다는 전제 — 이는 실제 LLM 학습이 하는 일이므로 현실적 비교.

## 검증 — AI에게 내 주장을 반증시켰다(MAJOR 0)

마지막으로 세 실험의 수치 주장을 **독립 검증 AI에게 병렬로 반증**시켰습니다. 특히 주결과(capability)는 검증 AI가 **직접 SmolLM2를 로드해 3 시드를 독립 재실행**해 "강한 경사가 진화를 능가"를 결정론적으로 재현했습니다. **MAJOR 불일치 0.** 모든 지적은 재현성/표현/유보 정밀도 개선이며 결론을 뒤집는 것은 없었습니다(검증용 난수가 재현되지 않는 결함 하나를 발견해 즉시 결정론화하고 재실행).

---

## 정리 — "진화 가능한 LLM"의 정체

세 편(#38→#39→#40)의 호를 거쳐 우리는 여기에 닿았습니다.

- **#38**: 방어적 공개 — "증명을 동반한 기억"의 창이 이론에서 열렸다.
- **#39**: 창은 구현에서 닫혔다. 하지만 **확장성의 벽**은 꿈쩍도 안 했다(증명을 동반한 진화는 n≤6까지).
- **#40(이번)**: 그럼 똑똑해지나? → **아니오.** 실재 LLM 지형에서도 강한 경사가 진화를 이긴다. **capability는 못 판다.**

그래서 "진화 가능한 LLM"의 정체는 **"진화가 성능으로 이기는 AI"가 아니라 "온라인으로 구조를 바꿔도 폭주·파국적 망각하지 않음을 증명을 동반해 보증·측정하는 프레임워크"**입니다. 수수합니다. 하지만 **부풀린 똑똑함이 아니라 안전성으로 승부한다**고 정한 이상, 이것이 정직한 모습입니다.

다음 회에는 이 프레임워크를 "랭턴의 개미 환상을 꿰뚫어 보는 눈"이라는 비유로 총괄할 예정입니다. 경험은 겉보기에 속고, 인증기만 본질을 본다 — 그 한 점에 세 편의 honest disclosure가 모두 수렴합니다.

<!-- NAV -->
---
**FullSense KB ナビ**: [← #39 llcore 検証 arc (#39) — 「証](https://fullsense.qiita.com/furuse-kazufumi/items/9bf5a8c9120b21a0f16e) ・ [📑 目次](https://fullsense.qiita.com/furuse-kazufumi/items/1ad8db4b854194e2d215) ・ [#41 llcore 検証 arc (#41) — ve →](https://fullsense.qiita.com/furuse-kazufumi/items/f8ff0a278c190afde1cd)
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
