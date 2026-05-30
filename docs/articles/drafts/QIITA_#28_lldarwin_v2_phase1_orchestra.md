---
title: '進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28（lldarwin 実装編）'
tags:
  - FullSense
  - llive
  - 進化計算
  - MoA
  - honest_disclosure
private: true
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

> ⚠️ **DRAFT** — 連載番号は portal 整理で確定（lldarwin アーク #25→#26→#27→**本記事=実装編**）。

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28

> 📚 **連載ナビ（lldarwin アーク）**: #24-05 集団進化 → #25 monoculture の失敗 → #26 設計編 → #27 徹夜の意思決定（climax）→ **#28 本記事（実装編）**。※ 各記事は単独でも読めます。

> **コンセプト hook**:
> 1 体の賢い AI に何度も聞くのではなく、**少しずつ違う大勢の AI を「進化」させ続け、答えが要るその瞬間に、指揮者が適材を選んで合奏（オーケストラ）させて 1 つの答えにする**。
> ——これが llive がいま目指している姿です。`llive` は「LLM そのもの」ではなく「LLM の周りに被せる認知 OS」。その中で、**集団を絶やさず・偏らせず・成長させ続ける**のが、今回作り込んだ進化エンジン `lldarwin` です。
>
> 前作 #27 で私たちは「評価（ものさし）が満点に張り付くと、進化は止まってただのふるい付きランダムサーチになる」という病を、実 LLM の 12 時間ランで確認しました。そして「淘汰器をいくら磨いても無駄。**評価そのものを開放端にせよ**」と方策を決めた。
>
> 今回はその方策を **実装** しました。そして proxy（合成のものさし）の上で、**best スコアが満点に張り付かず、最後まで伸び続けた**のです。

---

## 0. 三行であらすじ（落語の「枕」）

- **売りが決まった** — llive の北極星は「**連続進化 × ライブ・オーケストラ**」。進化し続ける集団を止めずに、任意の瞬間に competence-aware routing（指揮者）で合奏させて 1 答する。これは先行研究の **white-space（空白地帯）**。
- **飽和を治す 3 つを実装した** — ①意味次元を個別保護する factor-subspace QD ②成果を「単一 best」でなく多様性アーカイブに貯める MAP-Elites ③ものさしを集団に追従させる適応難易度。これで「奏者（多様な個体）が絶えない」基盤ができた。
- **proxy で飽和回避を実証** — lldarwin-v2 を 10 世代回したら best 0.80 → **0.92 と張り付かずに上昇**。多様性アーカイブは 21 セルが埋まった。**ただし proxy であり、実 LLM の能力を測ったわけではない**（honest）。

要するに **「賢い 1 体」ではなく「多様な大勢 × 指揮者」**。そのための「奏者を絶やさない仕掛け」が今回の実装です。

---

## 1. llive とは何か（はじめての方へ）

`llive`（エル・ライブ。L は 2 つ）は **自己進化型・モジュラー記憶の LLM フレームワーク**です。FullSense という傘ブランドの一員で、兄弟に `llmesh`（オンプレ LLM ハブ）と `llove`（端末ダッシュボード）がいます。3 つは独立 OSS ですが、組み合わせると 1 つの世界観になります。

llive の思想を 1 行で言うと「**LLM 本体ではなく、LLM の"周り"に被せる認知 OS**」。4 層メモリ・6 ステージのループ・承認バス（Approval Bus）・TRIZ・10 個の思考因子……といった「考え方の足場」を LLM の外側に組み、**同じ LLM でも振る舞いを進化させられる**ようにします。

その「進化」を担うのが、今回の主役 **`lldarwin`**（ダーウィン）です。役割分担はこうです。

- **lleval（眼鏡）** = 個体を *測る*（評価）
- **lldarwin（淘汰器）** = 測った差を「誰が生き残り・子を残すか」に *変換する*（選択圧）

そして両者の上に乗る北極星が、次の「オーケストラ」です。

---

## 2. 売り = 連続進化 × ライブ・オーケストラ（独自性の核）

普通の Mixture-of-Agents（MoA）は、**固定された**複数モデルに同じ問いを投げ、答えを集約します。llive が狙うのはその一歩先です。

> **集団を止めずに進化させ続け（online evolution）、答えが要るその瞬間に（online answering）、指揮者が「この問いにはこの奏者たち」と選んで合奏させて 1 答する。**

この「online 進化 + online 回答の統合」は、調べた限り**明確な先行研究がない white-space** でした（#27 で Perplexity に文献を漁らせて確認）。近いものに MoA / Self-MoA / sequential aggregation / routing はありますが、「進化し続ける集団そのものをライブで合奏させる」型は見当たりません。

ここで効くのが #27 で得た 2 つの正直な発見です。

1. **集約は「投票」ではなく「指揮者（competence-aware routing / gating）」でなければならない。** 自己 PoC と実 LLM 検証が三重に一致しました：headroom（伸びしろ）のあるタスクでは `best_of`／`routing` が `single`（単一モデル反復）を上回るが、**`majority`（多数決）はむしろ逆効果**。これは 2025 年の "Self-MoA"（多様性は自動的に優位ではない）への、私たちなりの回答でもあります。
2. **指揮者の判断キーには、多様性アーカイブの「behavior descriptor」を流用できる。** つまり後述の QD（Quality-Diversity）と指揮者が、**同じ記述子の土台**を共有できる。

——ただし、オーケストラ本体（指揮者＝router の実装）はこれからです。**今回はその手前、「合奏させるに足る、多様で絶えない奏者の集団」を作る基盤**を実装しました。

---

## 3. なぜ「奏者が絶える」のか — 飽和という病（#25〜#27 のおさらい）

オーケストラに必要なのは「**個性の違う奏者が大勢、絶えずいること**」です。ところが素朴に進化させると、これが崩壊します。

- #25：500 世代回したら、世界に「私とフリストンだけ」が残った（**monoculture**）。
- #27：実 LLM(llama3.2) で 12 時間回したら、gen5 で best=1.0 に張り付き、65 世代無進歩。**全滅しないが累積もしない**＝ふるい付きランダムサーチ。

真因はどちらも同じ。**人手で固定したものさし（評価関数）が満点に張り付くと、全員が同点になって選択圧が消え、あとは遺伝的浮動で勝手に偏る**。眼鏡（lleval）が飽和すると、淘汰器（lldarwin）をどれだけ磨いても無力——これが #27 の結論でした。

だから磨く対象を変える。「ものさしを動かす」「多様性を構造的に守る」方へ。具体的には次の 3 つです。

---

## 4. 実装した 3 つの仕掛け（lldarwin v2 / Phase 1）

> 設計の合言葉は「**新しいアルゴリズムを発明しない**」。すでに llive 内に積み上げた部品（ε-lexicase / NoveltyScorer / MAP-Elites / 中立貯蔵庫）を、確定方策 S1 の形に**合成・配線**するのが Phase 1 です。`--selection lldarwin-v2` で一括 on になります。

### ③ 適応難易度 — ものさしを集団に追従させる

`AdaptivePercentileGate`。各評価軸の「最低ライン（minimal-criterion）」を、毎世代**集団のスコア分布の指定パーセンタイル（例：下位 40% 点）**に置き直します。集団が伸びれば最低ラインも自動で上がる。`ratchet`（単調非減少）にしておけば、一時的に下振れしても基準は緩まない。

これで「固定ものさしが満点で飽和する」病に蓋ができます（PoC では固定難易度が能力 0.627 で停滞 → 適応難易度で 0.952 まで上昇）。全員が最低ラインを割る荒れた世代でも、淘汰器は gate を無視して全滅を避けます（fail-open ガード）。

落語でいえば、**生徒が伸びたら合格点も上げる先生**です。満点を取らせて終わりにしない。

### ① factor-subspace QD — 意味次元の個性を個別に守る

`FactorSubspaceNovelty`。novelty 探索は「集団全体としての多様性」は保ちますが、巨大な潜在次元の下では「**意味のある次元（思考因子）の多様性**」が、いつのまにか痩せていきます（factor drift）。

そこで、思考因子の**部分空間だけ**で別途 novelty を測り、全体 novelty とブレンドします。PoC では、これで意味次元の多様性の目減りがほぼ半減しました（retention 49.5% → 68.1%）。

> 正直な改良点：元の PoC は「生の距離を 0.5 ずつ足す」でしたが、部分空間ごとに距離のスケールが違うため、実装では**それぞれを z-score（標準化）してからブレンド**するように直しました。「全体の合唱」と「各パートの個性」を公平に混ぜるためです。

奏者でいえば、**第二バイオリンが第一バイオリンに飲まれて消えない**ようにする仕掛けです。

### ② MAP-Elites — 成果を「1 人の優勝者」でなく「多様性の地図」に貯める

`run_persona_evolution(map_elites=True)`。毎世代、全個体を MAP-Elites アーカイブに投入します。これは「最高スコアの 1 体」ではなく、**振る舞いの座標ごとに、そのマスでの最良個体を残す**地図（QD アーカイブ）です。新しいマスを埋めても既存のマスは消さない＝**多様性が構造的に崩壊しない・アーカイブは単調に育つ**。

これがそのまま、オーケストラの**奏者カタログ**になります。指揮者は将来、この地図から「この問いに合う座標の奏者」を選んで合奏させる——QD と routing が同じ記述子を共有する、という #27 の設計がここで効いてきます。

実装は **個体のフォーマットを拡張せず**、既存ゲノムの思考因子から座標（descriptor）を導出する additive 配線にしました（基盤の後方互換 900+ テストを壊さないため）。記述子の本格設計（高次元の縮約など）は将来 Phase の課題として余地を残しています。

---

## 5. 結果 — proxy で「飽和しない進化」を確認

`lldarwin-v2`（上記 3 つ＋ novelty ＋中立貯蔵庫を全部 on）を proxy のものさしで 16 個体 × 10 世代回した実測です。

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21（多様性の地図に 21 マスが埋まった）
```

- **best が満点に張り付かず、0.80 → 0.92 と最後まで上昇し続けた。** #27 で見た「gen5 で 1.0 飽和→固定」の病理を、proxy 段では脱却できました。適応難易度が「ものさし」を集団に追従させた兆候です。
- **多様性アーカイブに 21 セルが埋まった** = 合奏させるべき「個性の違う奏者」のカタログができ始めた。
- 進化系の自動テスト **879 件＋新規テストが全部グリーン**、回帰なし。

---

## 6. honest disclosure（ここを飛ばさないでください）

良い結果ほど内訳を疑う、が FullSense の流儀です。

- **これは proxy です。** 個体は実 LLM ではなく llive のゲノム（思考因子の代理）。今回測ったのは「複数の独立した苦手軸に同時に選択圧をかけ、軸ごとの専門家を維持できるか」という **仕組みの実現可能性（mechanism feasibility）** であって、**production の LLM 能力ではありません**。実 LLM 評価は次の Phase です。
- **factor-subspace は完全保護ではない**（retention 68%、残りはドリフト）。中立貯蔵庫の併用や factor 重みの強化が要ります。
- **舞台裏の正直**：今回の実装中、自動コミットフックが編集のたびに「編集前」スナップショットを 49 件も積んでしまい、履歴が散らかりました。最後に意味のある 1 コミットへ squash して整理しています（公開 OSS 側）。逆に、内部戦略を含む fork は意図通りローカル保持のままで、露出していないことも確認しました。

---

## 7. これからどうするか

進化エンジン（奏者を絶やさない基盤）は Phase 1 で形になりました。次はオーケストラ本体と、proxy から実物への橋渡しです。

1. **Phase 2 = 実 LLM 配線。** オンプレ（localhost ollama）の実 LLM を相手に、適応難易度・factor-subspace QD・MAP-Elites を実評価で検証する。proxy で見えた「飽和回避」が、本物の能力でも起きるか。
2. **指揮者（router）の実装。** QD アーカイブの descriptor を流用した competence-aware routing で、「進化する集団をライブで合奏させて 1 答」を実際に動かす。`best_of` の oracle にどこまで迫れるか。
3. **規模を上げる。** 集団 256 → 4096、潜在次元のスケールアップ。容量仮説（大きいほどニッチが増える）の確認。
4. **対話的な連続運転。** 長時間ランを step / pause / resume で覗ける運転席（CKPT-1）。

---

## 8. ここで一息（休憩ポイント）

ここまでで「**llive は何を売りにするのか**」は伝わったでしょうか。

- 賢い 1 体ではなく、**進化し続ける多様な集団 × 指揮者の合奏**。
- そのために、**奏者を絶やさず・個性を守り・成長させ続ける**進化エンジンを作った。
- proxy では飽和を治せた。**次は実 LLM とオーケストラ本体**。

続きの「実 LLM 編」と「オーケストラ編」で、proxy の約束が本物になるかをお見せします。——ここまでお付き合いありがとうございました。

---

## Series Navigation

- 連載ナビ（lldarwin アーク）: #24-05 集団進化 → #25 monoculture の失敗 → #26 設計編 → #27 徹夜の意思決定 → **#28 本記事（実装編）**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

# English

# An Ensemble Where a "Conductor" Makes an Ever-Evolving AI Population Play Together — llive's Orchestra-Style Evolution and the 3 Devices That Cured Saturation #28

> 📚 **Series guide (lldarwin arc)**: #24-05 population evolution → #25 the failure of monoculture → #26 design article → #27 the all-nighter decision (climax) → **#28 this article (implementation)**. ※ Each article can also be read on its own.

> **Concept hook**:
> Instead of asking one clever AI over and over, you **keep "evolving" a large crowd of slightly different AIs, and at the very moment an answer is needed, a conductor picks the right ones and makes them play together (an orchestra) to produce a single answer**.
> ——This is what llive is now aiming to become. `llive` is not "the LLM itself" but "a cognitive OS you wrap around an LLM". Within it, the evolution engine `lldarwin` we built this time is what **keeps the population alive, unbiased, and continuously growing**.
>
> In the previous article #27, we confirmed, over a 12-hour run with a real LLM, the disease that "once the evaluation (the yardstick) pins to a perfect score, evolution stops and degenerates into a mere sieve-fitted random search". And we decided on a policy: "No matter how much you polish the selector, it is futile. **Make the evaluation itself an open end**."
>
> This time we **implemented** that policy. And on top of a proxy (a synthetic yardstick), **the best score did not pin to a perfect mark — it kept rising all the way to the end**.

---

## 0. The gist in three lines (the rakugo "opening")

- **The selling point is set** — llive's North Star is "**continuous evolution × live orchestra**". Without stopping the ever-evolving population, at any given moment it plays them together via competence-aware routing (the conductor) to produce one answer. This is a **white-space** in prior research.
- **We implemented the 3 things that cure saturation** — ① factor-subspace QD, which protects semantic dimensions individually; ② MAP-Elites, which stores outcomes not as a "single best" but in a diversity archive; ③ adaptive difficulty, which makes the yardstick follow the population. With these, we now have a foundation where "the players (diverse individuals) never run out".
- **Demonstrated saturation avoidance on a proxy** — running lldarwin-v2 for 10 generations, the best rose from 0.80 → **0.92 without pinning**. The diversity archive filled 21 cells. **However, this is a proxy and does not measure the capability of a real LLM** (honest).

In short, **not "one clever individual" but "a diverse crowd × a conductor"**. The implementation this time is the "device that keeps the players from running out" needed for that.

---

## 1. What is llive (for first-time readers)

`llive` (el-live; with two L's) is a **self-evolving, modular-memory LLM framework**. It is a member of the umbrella brand FullSense, with siblings `llmesh` (on-prem LLM hub) and `llove` (terminal dashboard). The three are independent OSS, but combined they form a single worldview.

llive's philosophy in one line: "**not the LLM itself, but a cognitive OS you wrap *around* an LLM**". You build a "scaffold for thinking" outside the LLM — 4-layer memory, a 6-stage loop, the Approval Bus, TRIZ, 10 thought factors, and so on — so that **even with the same LLM you can evolve its behavior**.

The protagonist this time, **`lldarwin`** (Darwin), is what carries that "evolution". The division of roles is as follows.

- **lleval (the eyeglasses)** = *measures* an individual (evaluation)
- **lldarwin (the selector)** = *converts* the measured difference into "who survives and who leaves offspring" (selection pressure)

And the North Star riding on top of both is the next "orchestra".

---

## 2. The selling point = continuous evolution × live orchestra (the core of originality)

An ordinary Mixture-of-Agents (MoA) throws the same question at a **fixed** set of multiple models and aggregates the answers. What llive aims at is one step beyond that.

> **Keep the population evolving without stopping it (online evolution), and at the very moment an answer is needed (online answering), the conductor selects "for this question, these players" and makes them play together to produce one answer.**

As far as we investigated, this "integration of online evolution + online answering" was a **white-space with no clear prior research** (confirmed in #27 by having Perplexity dig through the literature). Close to it are MoA / Self-MoA / sequential aggregation / routing, but a form that "makes the ever-evolving population itself play together live" is nowhere to be found.

Here, the two honest findings obtained in #27 come into play.

1. **Aggregation must not be "voting" but a "conductor (competence-aware routing / gating)".** A self-PoC and real-LLM verification agreed in triplicate: on tasks with headroom, `best_of` / `routing` beat `single` (single-model iteration), but **`majority` (majority vote) is actually counterproductive**. This is also our own answer to 2025's "Self-MoA" (diversity is not automatically advantageous).
2. **The "behavior descriptor" of the diversity archive can be reused as the conductor's decision key.** That is, the QD (Quality-Diversity) described later and the conductor can **share the same descriptor foundation**.

——That said, the orchestra body itself (the conductor = the router implementation) is still ahead. **This time we implemented the step before that: the foundation that builds a "diverse, never-exhausting population of players good enough to play together".**

---

## 3. Why do "the players run out" — the disease called saturation (a recap of #25–#27)

What an orchestra needs is "**a large crowd of players with distinct individuality, never running out**". Yet if you evolve naively, this collapses.

- #25: After running 500 generations, only "me and Friston" were left in the world (**monoculture**).
- #27: After running 12 hours with a real LLM (llama3.2), the best pinned to 1.0 at gen5 and made no progress for 65 generations. **It does not go extinct, but it does not accumulate either** = a sieve-fitted random search.

The root cause is the same in both. **Once the manually fixed yardstick (fitness function) pins to a perfect score, everyone ties, selection pressure vanishes, and after that the population drifts on its own via genetic drift.** Once the eyeglasses (lleval) saturate, no amount of polishing the selector (lldarwin) helps — that was the conclusion of #27.

So we change what we polish. Toward "moving the yardstick" and "structurally protecting diversity". Concretely, the following 3 things.

---

## 4. The 3 devices we implemented (lldarwin v2 / Phase 1)

> The watchword of the design is "**do not invent a new algorithm**". Phase 1 is to **compose and wire** the parts already accumulated within llive (ε-lexicase / NoveltyScorer / MAP-Elites / the neutral reservoir) into the shape of the decided policy S1. They all turn on at once with `--selection lldarwin-v2`.

### ③ Adaptive difficulty — make the yardstick follow the population

`AdaptivePercentileGate`. Each evaluation axis's "minimum line (minimal-criterion)" is re-placed every generation at a **specified percentile of the population's score distribution (e.g., the bottom-40% point)**. If the population improves, the minimum line automatically rises too. If you keep it on a `ratchet` (monotonically non-decreasing), the criterion does not loosen even on a temporary dip.

This puts a lid on the disease of "the fixed yardstick saturating at a perfect score" (in the PoC, fixed difficulty stagnated at capability 0.627 → with adaptive difficulty it rose to 0.952). Even in a turbulent generation where everyone falls below the minimum line, the selector ignores the gate to avoid total extinction (a fail-open guard).

In rakugo terms, it is **a teacher who raises the passing mark as the students improve**. It does not let them get a perfect score and call it a day.

### ① factor-subspace QD — protect the individuality of semantic dimensions one by one

`FactorSubspaceNovelty`. Novelty search preserves "diversity as a whole population", but under a huge latent dimension, "**the diversity of meaningful dimensions (thought factors)**" quietly withers (factor drift).

So we measure novelty separately on **only the subspace** of thought factors and blend it with the overall novelty. In the PoC, this roughly halved the loss of semantic-dimension diversity (retention 49.5% → 68.1%).

> An honest improvement point: the original PoC "added the raw distances 0.5 each", but since the distance scale differs per subspace, in the implementation we fixed it to **z-score (standardize) each one before blending**. This is to mix "the whole chorus" and "the individuality of each part" fairly.

In player terms, it is a device that keeps **the second violin from being swallowed and disappearing into the first violin**.

### ② MAP-Elites — store outcomes not as "a single champion" but as a "map of diversity"

`run_persona_evolution(map_elites=True)`. Every generation, all individuals are fed into the MAP-Elites archive. This is not "the single highest-scoring individual" but a map (QD archive) that **keeps the best individual in each cell, per coordinate of behavior**. Filling a new cell does not erase existing cells = **diversity does not structurally collapse, and the archive grows monotonically**.

This directly becomes the orchestra's **player catalog**. In the future the conductor will select "a player at the coordinate that fits this question" from this map and make them play together — the #27 design where QD and routing share the same descriptor takes effect here.

The implementation is **without extending the individual's format**: an additive wiring that derives the coordinate (descriptor) from the thought factors of the existing genome (so as not to break the 900+ backward-compatible tests of the foundation). The full-fledged design of the descriptor (e.g., reduction of high dimensions) is left as a task for a future Phase.

---

## 5. Results — confirming "evolution that does not saturate" on a proxy

These are measurements from running `lldarwin-v2` (all 3 above + novelty + the neutral reservoir on) for 16 individuals × 10 generations on a proxy yardstick.

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21 (21 cells filled in the map of diversity)
```

- **The best did not pin to a perfect score; it kept rising all the way, 0.80 → 0.92.** We escaped, at the proxy stage, the pathology of "1.0 saturation at gen5 → frozen" seen in #27. This is a sign that adaptive difficulty made the "yardstick" follow the population.
- **21 cells filled in the diversity archive** = a catalog of "players with distinct individuality" to be played together began to form.
- The evolutionary automated tests, **879 + new tests, are all green**, with no regressions.

---

## 6. Honest disclosure (please do not skip this)

The better the result, the more you doubt its breakdown — that is the FullSense way.

- **This is a proxy.** The individuals are not real LLMs but llive's genome (a proxy for thought factors). What we measured this time is the **mechanism feasibility** of "whether we can apply selection pressure to multiple independent weak axes simultaneously and maintain a specialist per axis", and is **not the LLM capability of production**. Real-LLM evaluation is the next Phase.
- **factor-subspace is not complete protection** (retention 68%, the rest drifts). It needs the joint use of the neutral reservoir and reinforcement of factor weights.
- **Honesty about backstage**: during this implementation, the auto-commit hook piled up 49 "pre-edit" snapshots on every edit, and the history got cluttered. In the end we squashed it into a single meaningful commit to tidy it up (on the public OSS side). Conversely, we also confirmed that the fork containing internal strategy stayed locally held as intended and was not exposed.

---

## 7. What we will do from here

The evolution engine (the foundation that keeps the players from running out) took shape in Phase 1. Next is the orchestra body itself and the bridge from proxy to the real thing.

1. **Phase 2 = real-LLM wiring.** Against a real LLM on-prem (localhost ollama), verify adaptive difficulty, factor-subspace QD, and MAP-Elites with real evaluation. Does the "saturation avoidance" seen on the proxy also happen with real capability?
2. **Implementing the conductor (router).** With competence-aware routing reusing the QD archive's descriptor, actually run "make the evolving population play together live to produce one answer". How close can we get to the `best_of` oracle?
3. **Scaling up.** Population 256 → 4096, scaling up the latent dimension. Verifying the capacity hypothesis (the bigger, the more niches).
4. **Interactive continuous operation.** A driver's seat (CKPT-1) from which you can peek into a long run with step / pause / resume.

---

## 8. A breather here (a rest point)

Up to here, has it come across "**what llive sells**"?

- Not one clever individual, but **an ever-evolving diverse population × the ensemble of a conductor**.
- For that, we built an evolution engine that **keeps the players from running out, protects individuality, and continuously grows them**.
- On the proxy, we could cure saturation. **Next is the real LLM and the orchestra body itself.**

In the upcoming "real-LLM article" and "orchestra article", we will show you whether the proxy's promise becomes real. ——Thank you for staying with us this far.

---

## Series Navigation

- Series guide (lldarwin arc): #24-05 population evolution → #25 the failure of monoculture → #26 design article → #27 the all-nighter decision → **#28 this article (implementation)**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

# 中文

# 让"指挥者"指挥不断进化的 AI 群体合奏来作答 — llive 的乐团式进化, 以及治好饱和的 3 个装置 #28

> 📚 **连载导航（lldarwin 弧线）**: #24-05 群体进化 → #25 monoculture 的失败 → #26 设计篇 → #27 通宵的决断（climax）→ **#28 本文（实现篇）**。※ 各篇文章也可单独阅读。

> **概念 hook**:
> 不是对 1 个聪明的 AI 反复发问, 而是 **让一大群略有不同的 AI 持续"进化", 在需要答案的那一刻, 由指挥者挑选合适的成员合奏（乐团）汇成 1 个答案**。
> ——这就是 llive 现在所追求的形态。`llive` 不是"LLM 本身", 而是"套在 LLM 周围的认知 OS"。在其中, 让 **群体不绝、不偏、持续成长** 的, 就是这次打磨出的进化引擎 `lldarwin`。
>
> 在前作 #27 中, 我们通过真实 LLM 的 12 小时运行确认了这样一个病症:"评价（尺子）一旦贴死在满分上, 进化就会停止, 退化为仅仅带筛子的随机搜索"。于是定下方策:"无论怎么打磨淘汰器都是徒劳。**要让评价本身成为开放端**"。
>
> 这次我们 **实现** 了该方策。而在 proxy（合成尺子）之上, **best 分数没有贴死在满分上, 一直上升到最后**。

---

## 0. 三行剧情梗概（落语的"开场白"）

- **卖点确定了** — llive 的北极星是"**连续进化 × 现场乐团**"。在不停止持续进化的群体的同时, 在任意时刻用 competence-aware routing（指挥者）合奏汇成 1 答。这是先行研究中的 **white-space（空白地带）**。
- **实现了治好饱和的 3 个装置** — ①对语义维度逐个保护的 factor-subspace QD ②把成果不存为"单一 best"而存入多样性 archive 的 MAP-Elites ③让尺子跟随群体的适应难度。由此搭好了"奏者（多样的个体）不绝"的基盘。
- **在 proxy 上验证了规避饱和** — 把 lldarwin-v2 跑 10 代后, best 从 0.80 → **0.92 不贴死地上升**。多样性 archive 填满了 21 个 cell。**不过这是 proxy, 并未测量真实 LLM 的能力**（honest）。

总之就是 **不是"聪明的 1 体"而是"多样的一大群 × 指挥者"**。为此的"让奏者不绝的装置"就是这次的实现。

---

## 1. llive 是什么（致初次接触的读者）

`llive`（el-live。L 有 2 个）是 **自我进化型、模块化记忆的 LLM 框架**。它是名为 FullSense 的伞形品牌的一员, 兄弟有 `llmesh`（本地 LLM hub）和 `llove`（终端 dashboard）。这 3 者是独立 OSS, 但组合起来就成为 1 个世界观。

用 1 行概括 llive 的思想就是"**不是 LLM 本体, 而是套在 LLM '周围' 的认知 OS**"。把 4 层记忆、6 阶段的 loop、承认 bus（Approval Bus）、TRIZ、10 个思考因子……这些"思考的脚手架"搭在 LLM 的外侧, 使得 **即便是同一个 LLM 也能进化其行为**。

承担这个"进化"的, 就是这次的主角 **`lldarwin`**（达尔文）。角色分工如下。

- **lleval（眼镜）** = *测量* 个体（评价）
- **lldarwin（淘汰器）** = 把测出的差异 *转换* 为"谁存活、谁留下后代"（选择压）

而骑在两者之上的北极星, 就是接下来的"乐团"。

---

## 2. 卖点 = 连续进化 × 现场乐团（独特性的核心）

普通的 Mixture-of-Agents（MoA）是向 **固定的** 多个模型抛出同一个问题, 再聚合答案。llive 瞄准的是那再往前的一步。

> **不停止地让群体持续进化（online evolution）, 在需要答案的那一刻（online answering）, 由指挥者挑选"针对这个问题用这些奏者"合奏汇成 1 答。**

这种"online 进化 + online 回答的整合", 据我们调查是 **没有明确先行研究的 white-space**（在 #27 中让 Perplexity 翻阅文献确认过）。与之相近的有 MoA / Self-MoA / sequential aggregation / routing, 但"让持续进化的群体本身现场合奏"的形式则遍寻不见。

在这里发挥作用的是在 #27 得到的 2 个诚实发现。

1. **聚合不能是"投票", 而必须是"指挥者（competence-aware routing / gating）"。** 自我 PoC 和真实 LLM 验证三重一致: 在有 headroom（提升空间）的任务上 `best_of`／`routing` 胜过 `single`（单模型迭代）, 但 **`majority`（多数决）反而适得其反**。这也是我们对 2025 年 "Self-MoA"（多样性并非自动占优）的回答。
2. **指挥者的判断键可以挪用多样性 archive 的 "behavior descriptor"。** 也就是说后述的 QD（Quality-Diversity）和指挥者可以 **共享同一套记述子的根基**。

——不过, 乐团本体（指挥者＝router 的实现）还在后头。**这次实现的是其前一步:"搭建足以合奏的、多样且不绝的奏者群体"的基盘。**

---

## 3. 为什么"奏者会断绝" — 名为饱和的病（#25〜#27 的复习）

乐团需要的是"**个性各异的奏者一大群, 持续不绝地存在**"。然而若朴素地进化, 这会崩溃。

- #25: 跑 500 代后, 世界上只剩下"我和弗里斯顿"（**monoculture**）。
- #27: 用真实 LLM(llama3.2) 跑 12 小时后, gen5 时 best 贴死在 1.0, 65 代毫无进展。**不会全灭但也不会累积** ＝带筛子的随机搜索。

真因两者相同。**人为固定的尺子（评价函数）一旦贴死在满分上, 全体就同分, 选择压消失, 之后就靠遗传漂变随意偏移**。眼镜（lleval）一旦饱和, 无论怎么打磨淘汰器（lldarwin）都无力——这就是 #27 的结论。

所以要改变打磨的对象。转向"让尺子动起来""结构性地守护多样性"。具体就是接下来的 3 个。

---

## 4. 实现的 3 个装置（lldarwin v2 / Phase 1）

> 设计的口号是"**不发明新算法**"。Phase 1 就是把 llive 内已经积累的部件（ε-lexicase / NoveltyScorer / MAP-Elites / 中立贮藏库）**合成、配线** 成已确定方策 S1 的形态。用 `--selection lldarwin-v2` 即可一并开启。

### ③ 适应难度 — 让尺子跟随群体

`AdaptivePercentileGate`。把各评价轴的"最低线（minimal-criterion）"每一代 **重置为群体分数分布的指定百分位（例: 后 40% 点）**。群体提升, 最低线也自动上抬。设为 `ratchet`（单调非减）的话, 即便一时下探基准也不会松动。

由此就给"固定尺子在满分处饱和"的病盖上了盖（PoC 中固定难度停滞在能力 0.627 → 适应难度上升到 0.952）。即便在全体都跌破最低线的乱世代, 淘汰器也会无视 gate 以避免全灭（fail-open 防护）。

用落语来说, 就是 **学生进步了就把及格分也上调的老师**。不会让其拿了满分就到此为止。

### ① factor-subspace QD — 逐个守护语义维度的个性

`FactorSubspaceNovelty`。novelty 探索能保持"群体整体的多样性", 但在巨大的潜在维度之下,"**有意义的维度（思考因子）的多样性**"会不知不觉地萎缩（factor drift）。

于是, **仅在** 思考因子的 **子空间** 上另行测量 novelty, 并与整体 novelty 混合。在 PoC 中, 这使语义维度多样性的目减几乎减半（retention 49.5% → 68.1%）。

> 诚实的改良点: 原本的 PoC 是"把生距离各加 0.5", 但由于各子空间的距离尺度不同, 在实现中改为 **先把各自 z-score（标准化）再混合**。这是为了公平地混合"整体的合唱"和"各声部的个性"。

用奏者来说, 这是让 **第二小提琴不会被第一小提琴吞没消失** 的装置。

### ② MAP-Elites — 把成果存为"多样性的地图"而非"1 个冠军"

`run_persona_evolution(map_elites=True)`。每一代把全部个体投入 MAP-Elites archive。这不是"最高分的 1 体", 而是 **按行为的坐标、在那个格子里保留最优个体** 的地图（QD archive）。填了新格子也不会消除既有格子 ＝ **多样性不会结构性崩溃、archive 单调地成长**。

这直接就成为乐团的 **奏者目录**。指挥者将来会从这张地图中挑选"契合这个问题的坐标的奏者"合奏——QD 和 routing 共享同一记述子的、那个 #27 的设计在这里发挥作用。

实现上 **不扩展个体的格式**, 而是从既有 genome 的思考因子导出坐标（descriptor）的 additive 配线（为的是不破坏基盘的后向兼容 900+ 测试）。记述子的正式设计（高维的缩约等）作为将来 Phase 的课题留有余地。

---

## 5. 结果 — 在 proxy 上确认"不饱和的进化"

这是把 `lldarwin-v2`（上述 3 个＋ novelty ＋中立贮藏库全部开启）用 proxy 尺子跑 16 个体 × 10 代的实测。

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21（多样性的地图填满了 21 个格子）
```

- **best 没有贴死在满分上, 0.80 → 0.92 一路上升到最后。** 在 proxy 阶段摆脱了 #27 中看到的"gen5 时 1.0 饱和→固定"的病理。这是适应难度让"尺子"跟随群体的征兆。
- **多样性 archive 填满了 21 个 cell** ＝应当合奏的"个性各异的奏者"的目录开始成形。
- 进化系的自动测试 **879 件＋新增测试全部 green**, 无回归。

---

## 6. honest disclosure（请不要跳过这里）

结果越好越要怀疑其内幕, 这是 FullSense 的做派。

- **这是 proxy。** 个体不是真实 LLM, 而是 llive 的 genome（思考因子的代理）。这次测量的是"能否同时对多个独立的弱轴施加选择压、并按轴维持专家"这一 **机制的可行性（mechanism feasibility）**, 而 **不是 production 的 LLM 能力**。真实 LLM 评价是下一个 Phase。
- **factor-subspace 并非完全保护**（retention 68%, 其余漂移）。需要并用中立贮藏库以及强化 factor 权重。
- **幕后的诚实**: 这次实现过程中, 自动 commit 钩子在每次编辑时堆积了多达 49 个"编辑前"快照, 历史变得杂乱。最后 squash 成 1 个有意义的 commit 加以整理（公开 OSS 一侧）。反过来, 也确认了含有内部战略的 fork 如预期那样仍保持在本地、未被暴露。

---

## 7. 接下来要做什么

进化引擎（让奏者不绝的基盘）在 Phase 1 中成形了。接下来是乐团本体, 以及从 proxy 到实物的过渡。

1. **Phase 2 = 真实 LLM 配线。** 以本地（localhost ollama）的真实 LLM 为对象, 用真实评价验证适应难度、factor-subspace QD、MAP-Elites。在 proxy 上看到的"规避饱和"是否在真实能力上也会发生。
2. **指挥者（router）的实现。** 用挪用 QD archive 的 descriptor 的 competence-aware routing, 实际运行"让进化中的群体现场合奏汇成 1 答"。能逼近 `best_of` 的 oracle 到何种程度。
3. **提升规模。** 群体 256 → 4096, 潜在维度的扩容。验证容量假说（越大 niche 越多）。
4. **交互式连续运行。** 能以 step / pause / resume 窥探长时间运行的驾驶席（CKPT-1）。

---

## 8. 在此稍歇（休息点）

到此为止,"**llive 以什么为卖点**"传达到了吗。

- 不是聪明的 1 体, 而是 **不断进化的多样群体 × 指挥者的合奏**。
- 为此, 做出了一个 **让奏者不绝、守护个性、持续成长** 的进化引擎。
- 在 proxy 上治好了饱和。**接下来是真实 LLM 和乐团本体。**

在后续的"真实 LLM 篇"和"乐团篇"中, 我们会让大家看到 proxy 的承诺是否成真。——感谢您一路相伴至此。

---

## Series Navigation

- 连载导航（lldarwin 弧线）: #24-05 群体进化 → #25 monoculture 的失败 → #26 设计篇 → #27 通宵的决断 → **#28 本文（实现篇）**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

# 한국어

# "지휘자"가 끊임없이 진화하는 AI 집단을 합주시켜 답한다 — llive의 오케스트라형 진화, 그리고 포화를 고친 3가지 장치 #28

> 📚 **연재 내비（lldarwin 아크）**: #24-05 집단 진화 → #25 monoculture의 실패 → #26 설계편 → #27 밤샘의 의사결정（climax）→ **#28 본 글（구현편）**。※ 각 글은 단독으로도 읽을 수 있습니다.

> **콘셉트 hook**:
> 1체의 똑똑한 AI에게 몇 번이고 묻는 것이 아니라, **조금씩 다른 대규모의 AI를 계속 "진화"시키고, 답이 필요한 바로 그 순간에 지휘자가 적임자를 골라 합주（오케스트라）시켜 1개의 답으로 만든다**.
> ——이것이 llive가 지금 지향하는 모습입니다. `llive`는 "LLM 그 자체"가 아니라 "LLM 주위에 씌우는 인지 OS". 그 안에서 **집단을 끊기지 않게・편향되지 않게・계속 성장시키는** 것이, 이번에 만들어 넣은 진화 엔진 `lldarwin`입니다.
>
> 전작 #27에서 우리는 "평가（잣대）가 만점에 들러붙으면 진화는 멈추고 그저 체가 달린 랜덤 서치가 된다"는 병을 실 LLM의 12시간 런에서 확인했습니다. 그리고 "도태기를 아무리 갈아도 무의미하다. **평가 그 자체를 개방단으로 하라**"고 방책을 정했습니다.
>
> 이번에는 그 방책을 **구현**했습니다. 그리고 proxy（합성 잣대） 위에서, **best 점수가 만점에 들러붙지 않고 끝까지 계속 올랐습니다**.

---

## 0. 세 줄로 줄거리（라쿠고의 "도입부"）

- **셀링 포인트가 정해졌다** — llive의 북극성은 "**연속 진화 × 라이브 오케스트라**". 계속 진화하는 집단을 멈추지 않고, 임의의 순간에 competence-aware routing（지휘자）으로 합주시켜 1답한다. 이것은 선행 연구의 **white-space（공백 지대）**.
- **포화를 고치는 3가지를 구현했다** — ①의미 차원을 개별 보호하는 factor-subspace QD ②성과를 "단일 best"가 아니라 다양성 archive에 쌓는 MAP-Elites ③잣대를 집단에 따라가게 하는 적응 난이도. 이로써 "주자（다양한 개체）가 끊기지 않는" 기반이 만들어졌다.
- **proxy에서 포화 회피를 실증** — lldarwin-v2를 10세대 돌렸더니 best 0.80 → **0.92로 들러붙지 않고 상승**. 다양성 archive는 21 셀이 채워졌다. **단, proxy이며 실 LLM의 능력을 측정한 것은 아니다**（honest）.

요컨대 **"똑똑한 1체"가 아니라 "다양한 대규모 × 지휘자"**. 그것을 위한 "주자를 끊기지 않게 하는 장치"가 이번 구현입니다.

---

## 1. llive란 무엇인가（처음 접하는 분께）

`llive`（엘 라이브. L은 2개）는 **자기 진화형・모듈러 기억의 LLM 프레임워크**입니다. FullSense라는 우산 브랜드의 일원으로, 형제로 `llmesh`（온프렘 LLM 허브）와 `llove`（단말 대시보드）가 있습니다. 3개는 독립 OSS이지만, 조합하면 1개의 세계관이 됩니다.

llive의 사상을 1줄로 말하면 "**LLM 본체가 아니라 LLM의 '주위'에 씌우는 인지 OS**". 4층 메모리・6스테이지의 루프・승인 버스（Approval Bus）・TRIZ・10개의 사고 인자…… 같은 "사고의 발판"을 LLM의 바깥쪽에 짜서, **같은 LLM이라도 행동을 진화시킬 수 있게** 합니다.

그 "진화"를 담당하는 것이, 이번의 주역 **`lldarwin`**（다윈）입니다. 역할 분담은 이렇습니다.

- **lleval（안경）** = 개체를 *측정한다*（평가）
- **lldarwin（도태기）** = 측정한 차이를 "누가 살아남고・자식을 남기는가"로 *변환한다*（선택압）

그리고 둘 위에 올라타는 북극성이, 다음의 "오케스트라"입니다.

---

## 2. 셀링 포인트 = 연속 진화 × 라이브 오케스트라（독창성의 핵심）

보통의 Mixture-of-Agents（MoA）는, **고정된** 복수의 모델에 같은 질문을 던지고 답을 집약합니다. llive가 노리는 것은 그 한 걸음 앞입니다.

> **집단을 멈추지 않고 계속 진화시키고（online evolution）, 답이 필요한 바로 그 순간에（online answering）, 지휘자가 "이 질문에는 이 주자들"이라고 골라 합주시켜 1답한다.**

이 "online 진화 + online 회답의 통합"은, 조사한 한 **명확한 선행 연구가 없는 white-space**였습니다（#27에서 Perplexity에게 문헌을 뒤지게 해 확인）. 가까운 것으로 MoA / Self-MoA / sequential aggregation / routing이 있지만, "계속 진화하는 집단 그 자체를 라이브로 합주시키는" 형태는 찾을 수 없습니다.

여기서 효과를 내는 것이 #27에서 얻은 2개의 정직한 발견입니다.

1. **집약은 "투표"가 아니라 "지휘자（competence-aware routing / gating）"여야 한다.** 자체 PoC와 실 LLM 검증이 삼중으로 일치했습니다: headroom（성장 여지）이 있는 태스크에서는 `best_of`／`routing`이 `single`（단일 모델 반복）을 웃돌지만, **`majority`（다수결）는 오히려 역효과**. 이것은 2025년의 "Self-MoA"（다양성은 자동으로 우위가 아니다）에 대한 우리 나름의 답이기도 합니다.
2. **지휘자의 판단 키에는, 다양성 archive의 "behavior descriptor"를 전용할 수 있다.** 즉 후술하는 QD（Quality-Diversity）와 지휘자가 **같은 기술자（descriptor）의 토대**를 공유할 수 있다.

——단, 오케스트라 본체（지휘자＝router의 구현）는 이제부터입니다. **이번에는 그 직전, "합주시키기에 충분한, 다양하고 끊기지 않는 주자의 집단"을 만드는 기반**을 구현했습니다.

---

## 3. 왜 "주자가 끊기는가" — 포화라는 병（#25〜#27의 복습）

오케스트라에 필요한 것은 "**개성이 다른 주자가 대규모로, 끊임없이 있는 것**"입니다. 그런데 소박하게 진화시키면 이것이 붕괴합니다.

- #25: 500세대를 돌렸더니, 세계에 "나와 프리스턴만"이 남았다（**monoculture**）.
- #27: 실 LLM(llama3.2)으로 12시간 돌렸더니, gen5에서 best=1.0에 들러붙어 65세대 무진보. **전멸하지는 않지만 누적도 하지 않는다** ＝체가 달린 랜덤 서치.

진짜 원인은 둘 다 같습니다. **사람 손으로 고정한 잣대（평가 함수）가 만점에 들러붙으면, 전원이 동점이 되어 선택압이 사라지고, 그 다음은 유전적 부동으로 멋대로 편향됩니다**. 안경（lleval）이 포화하면, 도태기（lldarwin）를 아무리 갈아도 무력하다——이것이 #27의 결론이었습니다.

그래서 가는 대상을 바꿉니다. "잣대를 움직인다", "다양성을 구조적으로 지킨다" 쪽으로. 구체적으로는 다음 3가지입니다.

---

## 4. 구현한 3가지 장치（lldarwin v2 / Phase 1）

> 설계의 표어는 "**새로운 알고리즘을 발명하지 않는다**". 이미 llive 안에 쌓아 온 부품（ε-lexicase / NoveltyScorer / MAP-Elites / 중립 저장고）을, 확정 방책 S1의 형태로 **합성・배선**하는 것이 Phase 1입니다. `--selection lldarwin-v2`로 일괄 on이 됩니다.

### ③ 적응 난이도 — 잣대를 집단에 따라가게 한다

`AdaptivePercentileGate`. 각 평가 축의 "최저선（minimal-criterion）"을, 매 세대 **집단의 점수 분포의 지정 퍼센타일（예: 하위 40% 점）**에 다시 놓습니다. 집단이 자라면 최저선도 자동으로 올라갑니다. `ratchet`（단조 비감소）로 해두면, 일시적으로 하락해도 기준은 느슨해지지 않습니다.

이로써 "고정 잣대가 만점에서 포화하는" 병에 뚜껑을 덮을 수 있습니다（PoC에서는 고정 난이도가 능력 0.627에서 정체 → 적응 난이도로 0.952까지 상승）. 전원이 최저선을 밑도는 거친 세대라도, 도태기는 gate를 무시하고 전멸을 피합니다（fail-open 가드）.

라쿠고로 말하면, **학생이 자라면 합격점도 올리는 선생님**입니다. 만점을 받게 하고 끝내지 않습니다.

### ① factor-subspace QD — 의미 차원의 개성을 개별로 지킨다

`FactorSubspaceNovelty`. novelty 탐색은 "집단 전체로서의 다양성"은 유지하지만, 거대한 잠재 차원 아래에서는 "**의미 있는 차원（사고 인자）의 다양성**"이 어느새 야위어 갑니다（factor drift）.

그래서 사고 인자의 **부분 공간만**으로 별도로 novelty를 측정하고, 전체 novelty와 블렌드합니다. PoC에서는 이로써 의미 차원 다양성의 감소가 거의 반감했습니다（retention 49.5% → 68.1%）.

> 정직한 개량점: 원래 PoC는 "생거리를 0.5씩 더한다"였지만, 부분 공간마다 거리의 스케일이 다르므로, 구현에서는 **각각을 z-score（표준화）한 다음 블렌드**하도록 고쳤습니다. "전체의 합창"과 "각 파트의 개성"을 공평하게 섞기 위해서입니다.

주자로 말하면, **제2바이올린이 제1바이올린에 잡아먹혀 사라지지 않게** 하는 장치입니다.

### ② MAP-Elites — 성과를 "1명의 우승자"가 아니라 "다양성의 지도"에 쌓는다

`run_persona_evolution(map_elites=True)`. 매 세대, 전 개체를 MAP-Elites archive에 투입합니다. 이것은 "최고 점수의 1체"가 아니라, **행동의 좌표마다, 그 칸에서의 최량 개체를 남기는** 지도（QD archive）입니다. 새 칸을 채워도 기존 칸은 사라지지 않는다 ＝ **다양성이 구조적으로 붕괴하지 않는다・archive는 단조롭게 자란다**.

이것이 그대로 오케스트라의 **주자 카탈로그**가 됩니다. 지휘자는 장래에 이 지도에서 "이 질문에 맞는 좌표의 주자"를 골라 합주시킨다——QD와 routing이 같은 기술자를 공유한다는 #27의 설계가 여기서 효과를 냅니다.

구현은 **개체의 포맷을 확장하지 않고**, 기존 genome의 사고 인자에서 좌표（descriptor）를 도출하는 additive 배선으로 했습니다（기반의 후방 호환 900+ 테스트를 깨뜨리지 않기 위해서）. 기술자의 본격 설계（고차원의 축약 등）는 장래 Phase의 과제로 여지를 남겨두었습니다.

---

## 5. 결과 — proxy에서 "포화하지 않는 진화"를 확인

`lldarwin-v2`（위의 3가지＋ novelty ＋중립 저장고를 전부 on）를 proxy의 잣대로 16개체 × 10세대 돌린 실측입니다.

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21（다양성의 지도에 21칸이 채워졌다）
```

- **best가 만점에 들러붙지 않고, 0.80 → 0.92로 끝까지 계속 상승했다.** #27에서 본 "gen5에서 1.0 포화→고정"의 병리를, proxy 단계에서는 벗어날 수 있었습니다. 적응 난이도가 "잣대"를 집단에 따라가게 한 징후입니다.
- **다양성 archive에 21 셀이 채워졌다** ＝합주시켜야 할 "개성이 다른 주자"의 카탈로그가 만들어지기 시작했다.
- 진화계의 자동 테스트 **879건＋신규 테스트가 전부 green**, 회귀 없음.

---

## 6. honest disclosure（여기를 건너뛰지 말아 주세요）

좋은 결과일수록 내막을 의심한다, 가 FullSense의 방식입니다.

- **이것은 proxy입니다.** 개체는 실 LLM이 아니라 llive의 genome（사고 인자의 대리）. 이번에 측정한 것은 "복수의 독립된 약점 축에 동시에 선택압을 가하고, 축마다의 전문가를 유지할 수 있는가"라는 **메커니즘의 실현 가능성（mechanism feasibility）**이며, **production의 LLM 능력이 아닙니다**. 실 LLM 평가는 다음 Phase입니다.
- **factor-subspace는 완전 보호가 아닙니다**（retention 68%, 나머지는 드리프트）. 중립 저장고의 병용이나 factor 가중치의 강화가 필요합니다.
- **무대 뒤의 정직**: 이번 구현 중, 자동 commit 훅이 편집할 때마다 "편집 전" 스냅샷을 49건이나 쌓아 버려, 이력이 어지러워졌습니다. 마지막에 의미 있는 1 commit으로 squash해 정리하고 있습니다（공개 OSS 측）. 반대로, 내부 전략을 포함하는 fork는 의도대로 로컬 보유 그대로이며, 노출되지 않은 것도 확인했습니다.

---

## 7. 앞으로 어떻게 할 것인가

진화 엔진（주자를 끊기지 않게 하는 기반）은 Phase 1에서 형태가 잡혔습니다. 다음은 오케스트라 본체와, proxy에서 실물로의 가교입니다.

1. **Phase 2 = 실 LLM 배선.** 온프렘（localhost ollama）의 실 LLM을 상대로, 적응 난이도・factor-subspace QD・MAP-Elites를 실평가로 검증한다. proxy에서 보인 "포화 회피"가, 진짜 능력에서도 일어나는가.
2. **지휘자（router）의 구현.** QD archive의 descriptor를 전용한 competence-aware routing으로, "진화하는 집단을 라이브로 합주시켜 1답"을 실제로 동작시킨다. `best_of`의 oracle에 어디까지 다가갈 수 있는가.
3. **규모를 올린다.** 집단 256 → 4096, 잠재 차원의 스케일업. 용량 가설（클수록 niche가 늘어난다）의 확인.
4. **대화적인 연속 운전.** 장시간 런을 step / pause / resume로 들여다볼 수 있는 운전석（CKPT-1）.

---

## 8. 여기서 한숨 돌리기（휴식 포인트）

여기까지로 "**llive는 무엇을 셀링 포인트로 하는가**"는 전해졌을까요.

- 똑똑한 1체가 아니라, **계속 진화하는 다양한 집단 × 지휘자의 합주**.
- 그것을 위해, **주자를 끊기지 않게・개성을 지키고・계속 성장시키는** 진화 엔진을 만들었다.
- proxy에서는 포화를 고칠 수 있었다. **다음은 실 LLM과 오케스트라 본체**.

이어지는 "실 LLM 편"과 "오케스트라 편"에서, proxy의 약속이 진짜가 되는지를 보여드리겠습니다. ——여기까지 함께해 주셔서 감사합니다.

---

## Series Navigation

- 연재 내비（lldarwin 아크）: #24-05 집단 진화 → #25 monoculture의 실패 → #26 설계편 → #27 밤샘의 의사결정 → **#28 본 글（구현편）**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
