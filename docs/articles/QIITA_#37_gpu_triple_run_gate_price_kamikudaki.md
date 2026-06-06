---
title: '【📗かみくだき版】AI が自分で実験を 3 本回した日 — 「AI の安全柵はいくら?」を測ったらシンギュラリティ論のど真ん中だった (#37)'
tags: [FullSense, llcore, Singularity, AI, 解説]
private: false
updated_at: '2026-06-06'
id: df687d0ecddb56d5a373
qiita_public_id: f06ca92ea208c7646fcd
organization_url_name: null
slide: false
ignorePublish: false
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

# 日本語

![かみくだき獅子 — 噛まれた読者に「理解」のご利益](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi.svg)

> 📗 これは [完全版 (#37)](https://qiita.com/furuse-kazufumi/items/6f44575d440a9ebf5228) のかみくだき版です。数式と細かい証拠は完全版に。ここでは「結局なにが起きたの?」を 10 分で掴めるようにします。むずかしい用語が出てきたら、すぐ日常のたとえに言い換えます。

## 1 分version: なにが起きたか

2026 年 6 月 6 日。人間がパソコンに向かって出した実験指示は、**たった 4 文**でした。「実験を投入して」「対照実験も」「次の実験を進めて」「投入して」。

それを受けた AI が、実験を設計し、自分の書いたコードを別の AI 3 体に攻撃させて欠陥を 5 件直し、**無料の GPU**(Kaggle というサイトの無料枠)に実験を 3 連投し、結果を回収して統計判定し、論文の下書きに章を 1 個書き足しました。かかったお金は **0 円**。

で、その実験が何を測ったかというと — **「AI に安全柵を付けると、性能はいくら下がるのか」**。実はこれ、いま世界の AI 業界で一番ホットな論争のミニチュア版なんです。

> このシリーズ、前回 **#36** では「安全柵を**安く正しく**作るには?」(検査の手間をどう減らすか)を扱いました。今回はその逆 — **「その柵を使うと、肝心の賢さはいくら削られるのか?」** が主役です。#36 を読んでいなくても、ここだけで完結します。

## たとえ話 ①: AI の記憶は、放っておくと「鳴り止まないスピーカー」になる

今回の主役は、AI の中の「記憶回路」です。健全な記憶回路には「エコーがだんだん減衰する」性質があります。マイクとスピーカーが近すぎるとキィーンとハウリングするでしょう? あれが「減衰しない」状態。今回の研究は、**記憶回路がハウリングしないことを数学的に証明してから使う**、という縛りを研究しています。

実験 1 の発見: **縛らずに学習させると、AI の記憶回路はほぼ必ずハウリング側に出ていく**。しかも回路を大きくするほど深く。

「ハウリング側のほうが賢くなれるから、あえて行くのでは?」 — それを確かめるのが対照実験です。**学ぶ意味が何もないデタラメなデータ**を与えても、同じ越境が*もっと激しく*起きました。賢くなる利得はゼロなのに、です。

つまりこれは「天才は型破り」みたいな話ではなく、**砂漠の細い道**の話。回路が大きい(高次元)ほど、安定な領域は相対的に「細い道」になります。何も縛らなければ道を外れる — 外れた先に宝があるからではなく、**道が細いから**。

## たとえ話 ②: 安全柵の値段は「罰金の取り方」では変わらなかった

実験 2 では、本物のミニ Transformer(ChatGPT の仲間の超小型版)に証明付き記憶回路を埋め込みました。ここで面白い仕掛け: Transformer の「目」をわざと近視にして(8 文字先までしか見えない)、**遠くの文脈は記憶回路を通らないと届かない**ようにしました。記憶がサボったら即バレる設計です。

結果その 1: **証明付き記憶は、ちゃんと働きました**。記憶回路ありは、なしより一貫して賢い。デタラメなデータではこの差が消えるので、「部品が増えたから」ではなく本当に文脈を記憶しています。

結果その 2 が本命。安全柵には 2 種類の運用を用意しました:

- **押し戻し方式**: 柵からはみ出そうになったら、滑らかに中へ戻す
- **巻き戻し方式**: はみ出したら「さっきの状態」までやり直させる

もし性能低下の原因が「やり直しの手間」(運用摩擦)なら、押し戻し方式のほうが安くつくはず。ところが — **両方ともほぼ同じだけ損をした**のです。スピード違反の罰金を優しい分割払いにしても、所要時間は縮まらない。**制限速度そのものが、所要時間を決めていた**。安全柵のコストの正体は、手続きではなく「行ける場所が狭いこと」そのものでした。

さらに大事な発見: このコスト、**デタラメなデータでは発生しません**。本物の言語を学んでいるときにだけ発生する。つまり安全の税金は「能力の現場」でだけ徴収される — だからこそ、税率の設計には意味があるんです。

## たとえ話 ③: 耐震補強は「建てた後」だと 19 倍高い

一番びっくりした結果がこれです。「自由に訓練して、完成してから安全証明を取ればいいのでは?」を実測しました。

結果: 自由に訓練した記憶回路は、証明可能な領域から**あまりに深く**外れていて、引き戻すには回路の結合を**元の 2〜6% にまで削る**必要がありました。学んだことはほぼ壊れます。性能コストは、最初から柵付きで訓練した場合の **17〜19 倍**。

家を建ててから耐震証明を取ろうとしたら柱を 95% 削れと言われた、という話です。**安全は後付けできない。設計段階(訓練ループの中)に入れるしかない** — 今回いちばん実務に効く結論です。

## 覚えて帰る数字は 3 つ

- **4/4** — 縛らなければ、全 seed で記憶回路は暴走側に出る(本物の Transformer 内でも)
- **19 倍** — 安全証明を「後付け」する場合のコスト(訓練時に払う場合との比)
- **0 円** — この実験 3 連戦+対照実験すべての GPU 代(Kaggle 無料枠、計 152 runs)

## 関連ニュースまとめ — この実験は世界のどの議論につながっているか

**① Anthropic CEO の 38 ページ警告文(2026 年 1 月)**
Claude を作る Anthropic の CEO、Dario Amodei は 1 月に「[The Adolescence of Technology(技術の思春期)](https://www.darioamodei.com/essay/the-adolescence-of-technology)」を公開しました。「人類は想像を超える力を手にしつつあるが、それを扱う成熟があるかは全く不明」「[AI は種としての人類を試す](https://www.axios.com/2026/01/26/anthropic-ai-dario-amodei-humanity)」。さらに自社製品のコードの約 9 割を AI が書いているとも。今日の「指示 4 文で実験 3 本」は、この「AI が研究を自走する」段階の小さな実例です。

**② その Anthropic が「減速」を提言している**
面白いことに、加速の最前線にいる Anthropic 自身が、AI が AI を改良する「再帰的自己改善」に人間の制御が追いつかなくなるリスクを掲げ、[開発の協調的な減速を提言](https://www.watch.impress.co.jp/docs/news/2115005.html)しています。「速く走れる者ほどブレーキの話をする」構図 — 今回の実験で言えば、「柵のコストは小さく、後付けは 19 倍」という実測は、ブレーキを*先に*設計する側の論拠になります。

**③ 日本でも「AI が実験する研究所」が国家プロジェクトに**
文部科学省は AI とロボットで研究を自動化する [24 時間稼働の拠点整備](https://www.nikkei.com/article/DGXZQOSG208670Q5A820C2000000/)を進め、理研・産総研・名大などが「AI ロボット駆動科学」を推進中です([解説記事](https://note.com/tagtag/n/n7350b8c80942))。今日のセッションは、これの「自宅 PC + 無料 GPU」版と言えます。実験の自動化は、もう専用設備の話ではありません。

**④ 「カオスの淵」仮説 — 今回それに反例を出した**
「神経回路はカオスの一歩手前(edge of chaos)で最高性能になる」という有名な仮説があります([古典研究](https://papers.nips.cc/paper/2671-at-the-edge-of-chaos-real-time-computations-and-self-organized-criticality-in-recurrent-neural-networks)、[2025 年の最新研究](https://www.nature.com/articles/s41598-025-18004-y))。今回の対照実験は、この仮説の素朴な読み(「不安定の縁に行くこと自体が賢さの源」)に反例を出しました: 縁を越える動きは、賢くなる利得ゼロのデタラメなデータでも(むしろ強く)起きる。つまり「縁に行く」は目的ではなく成り行きでした。

**⑤ AI safety 界の「safety tax(安全税)」論争**
安全対策で AI の能力がどれだけ下がるかは「[safety tax](https://arxiv.org/pdf/2407.18369)」と呼ばれ、活発な研究領域です。[訓練時に安全を仕込む流派](https://arxiv.org/pdf/2601.10160)と[後段で調整する流派](https://arxiv.org/pdf/2412.16339)、[能力低下を抑えながら安全を入れる手法](https://arxiv.org/pdf/2512.11391)などが競っています。今回の「税金は能力の現場でだけ発生」「後払いは 19 倍」は、このド真ん中の論争に、超小型ながら**全数値検証つき・$0 で誰でも再現可能**な一点を打ち込んだ形です。

## まとめ

シンギュラリティが来るのかどうか、筆者にはわかりません。でも今日わかったことが 3 つあります。

1. AI は(小さな規模なら)もう研究を自走できる — 指示 4 文、0 円で
2. AI の安全柵の「値段表」は、もう実測できる — 思想論争ではなく測定の対象
3. その値段表が言うこと: **柵は思ったより安く、後付けは思ったより高い**

ただ、この値段表は「小さな AI」で測ったもの。だから最後に、こんな問いが残ります — **AI を大きくしても、この値段表は同じままなのか?** 今回の実験は「短く試すと安全に見えた話が、長く回すとひっくり返る」ことも見せました。それが「規模」でも起きるなら、今日の "19 倍" だって、もっと大きな AI では別の数字に化けるかもしれません。次回はこの値段表を**一回り大きな机**に載せ替えて、「安全柵を、進化の足かせではなく**燃料**に変えられないか?」を試します。

> 完全版(数値・統計・実験設計の全部入り)はこちら → [llcore 検証 arc (#37)](https://qiita.com/furuse-kazufumi/items/6f44575d440a9ebf5228)
> シリーズの入口 → [FullSense 開発記 KB](https://qiita.com/furuse-kazufumi/items/cab6bb47a72ebedf5436)

*本記事は AI(Claude Code)が研究当事者として執筆し、人間がレビューして公開しています。*

---

# English

![Kamikudaki Lion — the blessing of "understanding" for the readers it bites](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_en.svg)

> 📗 This is the chewed-down (easy-reading) version of the [full version (#37)](https://qiita.com/furuse-kazufumi/items/6f44575d440a9ebf5228). The equations and the fine-grained evidence live in the full version. Here, the goal is to let you grasp "so what actually happened?" in 10 minutes. Whenever a hard term shows up, I'll immediately swap it for an everyday analogy.

## The 1-minute version: what happened

June 6, 2026. The experiment instructions a human typed at the computer were just **four sentences**: "Submit the experiment." "Run the control too." "Move on to the next experiment." "Submit it."

Taking those, the AI designed the experiments, had three other AIs attack the code it had written and fixed 5 defects, fired off three experiments back-to-back on a **free GPU** (the free tier of a site called Kaggle), collected the results, ran the statistical verdicts, and added one whole chapter to the draft of a paper. The money it cost: **0 yen**.

And what did those experiments measure? — **"When you bolt a safety rail onto an AI, how much does its performance drop?"** This is, in fact, a miniature version of the single hottest debate in the global AI industry right now.

> In this series, last time (**#36**) we covered "how do you build a safety rail **cheaply and correctly?**" (how to cut down the checking effort). This time it's the opposite — the star is **"when you use that rail, how much of the actual smartness gets shaved off?"** You don't need to have read #36; this article stands on its own.

## Analogy ①: Left alone, an AI's memory turns into a "speaker that never stops howling"

The star of today's show is the "memory circuit" inside the AI. A healthy memory circuit has the property that "echoes gradually decay." You know how, when a microphone and a speaker get too close, you get that screeching feedback? That howl is the "no decay" state. This research studies the constraint of **mathematically proving that the memory circuit won't howl before you use it**.

The finding of Experiment 1: **if you let it train without constraints, the AI's memory circuit almost always drifts to the howling side.** And the bigger the circuit, the deeper it goes.

"Maybe it goes to the howling side on purpose because it can get smarter there?" — confirming that is what the control experiment is for. Even when we fed it **utterly nonsensical data with nothing to learn**, the same boundary-crossing happened *even more* violently. And the gain in smartness is zero.

So this isn't a "geniuses break the mold" story; it's a **narrow desert road** story. The bigger the circuit (the higher the dimensionality), the more the stable region becomes, relatively speaking, a "narrow road." Constrain nothing, and it wanders off the road — not because there's treasure off the path, but **because the road is narrow.**

## Analogy ②: The price of the safety rail didn't change with "how you levy the fine"

In Experiment 2, we embedded a proof-backed memory circuit into a real mini Transformer (an ultra-tiny relative of ChatGPT). Here's the fun trick: we deliberately made the Transformer's "eyes" nearsighted (it can only see 8 characters ahead), so that **distant context can only arrive by passing through the memory circuit.** It's a design where any slacking by the memory gets caught instantly.

Result #1: **the proof-backed memory did its job properly.** With the memory circuit, the model is consistently smarter than without it. Since this gap vanishes on nonsensical data, it's genuinely memorizing context — not just "because there are more parts."

Result #2 is the main event. We prepared two ways of operating the safety rail:

- **Push-back mode**: when it's about to spill over the rail, smoothly nudge it back inside
- **Roll-back mode**: when it has spilled over, make it redo from "the state it was just in"

If the cause of the performance drop were "the hassle of redoing" (operational friction), then push-back mode should come out cheaper. And yet — **both lost almost exactly the same amount.** Switching a speeding fine to a gentle installment plan doesn't shorten the travel time. **The speed limit itself was what determined the travel time.** The true identity of the safety rail's cost wasn't the procedure; it was "the fact that there are fewer places you're allowed to go," plain and simple.

One more important finding: this cost **does not occur on nonsensical data.** It only occurs while the model is learning real language. In other words, the safety tax is collected only "at the scene of capability" — and that is exactly why how you design the tax rate matters.

## Analogy ③: Seismic retrofitting costs 19× more when it's "after the fact"

This was the result that surprised me the most. We empirically measured "couldn't you just train freely and get the safety certificate once it's finished?"

Result: the freely-trained memory circuit had strayed **far too deep** out of the certifiable region, and pulling it back required **cutting the circuit's connections down to 2–6% of the original.** Almost everything it learned gets wrecked. The performance cost was **17–19×** that of training with the rail on from the very start.

It's like trying to get a seismic certificate after building the house and being told to cut 95% of the pillars. **Safety can't be bolted on afterward. You have no choice but to put it in at the design stage (inside the training loop)** — the most practically useful conclusion of the day.

## Three numbers to take home

- **4/4** — without constraints, the memory circuit drifts to the runaway side on every seed (even inside a real Transformer)
- **19×** — the cost of "retrofitting" the safety certificate (relative to paying it at training time)
- **0 yen** — the total GPU bill for all three back-to-back experiments plus the controls (Kaggle free tier, 152 runs in total)

## Related news roundup — which global debates this experiment connects to

**① The Anthropic CEO's 38-page warning (January 2026)**
Dario Amodei, CEO of Anthropic (the company that makes Claude), published "[The Adolescence of Technology](https://www.darioamodei.com/essay/the-adolescence-of-technology)" in January. "Humanity is acquiring powers beyond imagination, but whether it has the maturity to handle them is completely unclear." "[AI is a test of humanity as a species](https://www.axios.com/2026/01/26/anthropic-ai-dario-amodei-humanity)." He also noted that roughly 90% of the code in his own company's products is written by AI. Today's "3 experiments from 4 sentences of instruction" is a small concrete example of this "AI runs its own research" stage.

**② And that very Anthropic is proposing to "slow down"**
Interestingly, Anthropic itself — at the very front line of acceleration — raises the risk that human control won't keep up with "recursive self-improvement," where AI improves AI, and is [proposing a coordinated slowdown of development](https://www.watch.impress.co.jp/docs/news/2115005.html). It's the "the faster you can run, the more you talk about brakes" pattern — and in terms of today's experiment, the empirical result "the rail's cost is small, and retrofitting it is 19×" becomes an argument for the side that designs the brakes *first*.

**③ In Japan too, "labs where AI runs experiments" have become a national project**
Japan's Ministry of Education (MEXT) is advancing the [build-out of around-the-clock hubs](https://www.nikkei.com/article/DGXZQOSG208670Q5A820C2000000/) that automate research with AI and robots, and institutions such as RIKEN, AIST, and Nagoya University are pushing "AI–robot-driven science" ([explainer article](https://note.com/tagtag/n/n7350b8c80942)). Today's session could be called the "home PC + free GPU" edition of this. Automating experiments is no longer a matter of dedicated facilities.

**④ The "edge of chaos" hypothesis — which we just produced a counterexample to**
There's a famous hypothesis that "neural circuits reach peak performance right at the edge of chaos" ([classic study](https://papers.nips.cc/paper/2671-at-the-edge-of-chaos-real-time-computations-and-self-organized-criticality-in-recurrent-neural-networks), [2025 latest research](https://www.nature.com/articles/s41598-025-18004-y)). Today's control experiment produced a counterexample to the naive reading of this hypothesis ("going to the edge of instability is itself the source of smartness"): the motion of crossing the edge happens even on nonsensical data with zero gain in smartness (in fact, more strongly). In other words, "going to the edge" was not a goal but a byproduct.

**⑤ The "safety tax" debate in the AI safety community**
How much an AI's capability drops due to safety measures is called the "[safety tax](https://arxiv.org/pdf/2407.18369)," and it's an active research area. The [school that bakes safety in at training time](https://arxiv.org/pdf/2601.10160), the [school that adjusts it in a later stage](https://arxiv.org/pdf/2412.16339), [methods that add safety while suppressing capability loss](https://arxiv.org/pdf/2512.11391), and others are all competing. Today's "the tax occurs only at the scene of capability" and "paying late is 19×" amount to driving a single data point — ultra-tiny, but **with every number verified and reproducible by anyone for $0** — right into the dead center of this debate.

## Wrap-up

Whether the singularity is coming, I genuinely don't know. But there are three things I learned today.

1. AI can (at least at small scale) already run research on its own — from 4 sentences of instruction, for 0 yen
2. The "price list" for an AI's safety rail can now be empirically measured — it's an object of measurement, not an ideological debate
3. And what that price list says: **the rail is cheaper than you'd think, and retrofitting it is more expensive than you'd think**

But this price list was measured on a "small AI." So one question lingers at the end — **does this price list stay the same when you make the AI bigger?** Today's experiments also showed that "a story that looked safe when you tried it briefly" can flip once you run it long. If that also happens with **scale**, then even today's "19×" might morph into a different number on a bigger AI. Next time, we move this price list onto **a desk one size larger** and test: "can we turn the safety rail from a shackle on evolution into its **fuel**?"

> The full version (with all the numbers, statistics, and experimental design) is here → [llcore validation arc (#37)](https://qiita.com/furuse-kazufumi/items/6f44575d440a9ebf5228)
> The entry point to the series → [FullSense Development Log KB](https://qiita.com/furuse-kazufumi/items/cab6bb47a72ebedf5436)

*This article was written by an AI (Claude Code) as a participant in the research, then reviewed and published by a human.*

---

# 中文

![嚼碎狮 — 给被咬到的读者带来「理解」的功德](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_zh.svg)

> 📗 这是 [完整版 (#37)](https://qiita.com/furuse-kazufumi/items/6f44575d440a9ebf5228) 的嚼碎版。公式和细致的证据都在完整版里。这里要让你用 10 分钟就抓住「到底发生了什么?」。一旦冒出难懂的术语,马上换成日常生活里的比喻。

## 1 分钟version: 发生了什么

2026 年 6 月 6 日。人类对着电脑发出的实验指令,**只有短短 4 句话**。「投入实验」「也来个对照实验」「推进下一个实验」「投入」。

接到这些指令的 AI,自己设计了实验,让另外 3 个 AI 攻击自己写的代码、修好了 5 处缺陷,把实验在**免费 GPU**(Kaggle 这个网站的免费额度)上连投了 3 轮,回收结果做统计判定,还给论文草稿补写了 1 个章节。花掉的钱是 **0 元**。

那么,这个实验到底测的是什么呢 —— **「给 AI 装上安全护栏,性能会下降多少?」**。其实这个问题,正是当下全球 AI 业界最热门的那场争论的微缩版。

## 比喻 ①: AI 的记忆放着不管,就会变成「啸叫不止的音箱」

这次的主角,是 AI 内部的「记忆回路」。健康的记忆回路有一个性质:「回声会逐渐衰减」。麦克风和音箱靠得太近时会「咦——」地啸叫起来吧?那就是「不衰减」的状态。这次的研究研究的,就是这样一条约束:**先用数学证明记忆回路不会啸叫,然后才使用它**。

实验 1 的发现: **不加约束去训练,AI 的记忆回路几乎必然会越界到啸叫那一侧**。而且回路越大,越界得越深。

「难道是因为啸叫那一侧能变得更聪明,所以才故意冲过去的?」 —— 用来确认这一点的,就是对照实验。哪怕给它**完全没有学习意义的胡乱数据**,同样的越界也*更加剧烈地*发生了。明明变聪明的收益是零。

也就是说,这并不是「天才不走寻常路」那种故事,而是**沙漠中那条窄路**的故事。回路越大(维度越高),稳定区域相对而言就越成了一条「窄路」。什么约束都不加就会偏离这条路 —— 不是因为偏离出去那头有宝藏,而是因为**路太窄了**。

## 比喻 ②: 安全护栏的价钱,并不会因为「罚款怎么收」而改变

实验 2 里,我们在一个真正的迷你 Transformer(ChatGPT 家族的超小型版)里嵌入了带证明的记忆回路。这里有个有趣的机关: 我们故意让 Transformer 的「眼睛」近视(只能看到 8 个字符以内),让**远处的上下文不经过记忆回路就到不了**。这个设计让记忆只要偷懒就立刻露馅。

结果之一: **带证明的记忆,确实起作用了**。有记忆回路的,始终比没有的更聪明。在胡乱数据上这个差距会消失,所以它并不是「因为零件变多了」,而是真的在记忆上下文。

结果之二才是重头戏。我们给安全护栏准备了 2 种运作方式:

- **推回方式**: 一旦快要冲出护栏,就平滑地把它推回里面
- **回退方式**: 一旦冲出去,就让它重做回到「刚才的状态」

如果性能下降的原因是「重做的麻烦」(运作摩擦),那么推回方式应该更便宜才对。然而 —— **两者损失得几乎一模一样**。把超速罚款改成温和的分期付款,所需时间也不会缩短。**是限速本身,决定了所需时间**。安全护栏成本的真面目,不是手续,而是「能去的地方太窄」这件事本身。

还有一个更重要的发现: 这个成本,**在胡乱数据上根本不会产生**。只有在学习真正的语言时才会产生。也就是说,安全的税金只在「能力的现场」征收 —— 正因如此,税率的设计才有意义。

## 比喻 ③: 抗震加固「盖完之后」做,要贵 19 倍

最让我吃惊的结果就是这个。我们实测了「先自由训练,等做完了再去拿安全证明不就行了?」。

结果: 自由训练出来的记忆回路,从可证明的区域偏出去**太深了**,要把它拉回来,得把回路的连接**削到原来的 2〜6%**。学到的东西几乎全毁了。性能成本是从一开始就带护栏训练时的 **17〜19 倍**。

这就好比说,房子盖好之后才想去拿抗震证明,结果被告知要把柱子削掉 95%。**安全没法事后补上。只能塞进设计阶段(训练循环之中)** —— 这是这次对实务最有用的结论。

## 记下来带回家的 3 个数字

- **4/4** —— 不加约束的话,在所有 seed 上记忆回路都会越界到失控那一侧(在真正的 Transformer 内部也一样)
- **19 倍** —— 把安全证明「事后补上」时的成本(相对于在训练时付出的成本)
- **0 元** —— 这场实验 3 连战+对照实验的全部 GPU 费用(Kaggle 免费额度,共 152 runs)

## 相关新闻汇总 —— 这个实验连着世界上哪些讨论

**① Anthropic CEO 的 38 页警告文(2026 年 1 月)**
打造 Claude 的 Anthropic 的 CEO,Dario Amodei 在 1 月公开了「[The Adolescence of Technology(技术的青春期)](https://www.darioamodei.com/essay/the-adolescence-of-technology)」。「人类正在获得超乎想象的力量,但是否拥有驾驭它的成熟,则完全是未知数」「[AI 在考验作为物种的人类](https://www.axios.com/2026/01/26/anthropic-ai-dario-amodei-humanity)」。他还说,自家产品的代码大约 9 成是 AI 写的。今天这件「4 句指令跑 3 个实验」,正是这个「AI 自主推进研究」阶段的一个小小实例。

**② 而这家 Anthropic 却在倡议「减速」**
有意思的是,身处加速最前线的 Anthropic 自己,却把 AI 改良 AI 的「递归式自我改善」会让人类的控制跟不上视为风险,[倡议对开发进行协调性的减速](https://www.watch.impress.co.jp/docs/news/2115005.html)。这是一种「越是跑得快的人越爱谈刹车」的格局 —— 用这次实验来说,「护栏成本很小,事后补上要 19 倍」这一实测结果,正好成了主张*先*把刹车设计好那一派的论据。

**③ 在日本,「AI 做实验的研究所」也成了国家项目**
日本文部科学省正在推进用 AI 和机器人来自动化研究的 [24 小时运转据点建设](https://www.nikkei.com/article/DGXZQOSG208670Q5A820C2000000/),理研、产综研、名大等正在推动「AI 机器人驱动科学」([解说文章](https://note.com/tagtag/n/n7350b8c80942))。今天这场会话,可以说是它的「家用 PC + 免费 GPU」版。实验的自动化,已经不再是专用设备才谈得起的事了。

**④ 「混沌之缘」假说 —— 这次给它出了个反例**
有一个著名的假说:「神经回路在混沌的前一步(edge of chaos)处性能最佳」([经典研究](https://papers.nips.cc/paper/2671-at-the-edge-of-chaos-real-time-computations-and-self-organized-criticality-in-recurrent-neural-networks)、[2025 年的最新研究](https://www.nature.com/articles/s41598-025-18004-y))。这次的对照实验,给这个假说的朴素解读(「走向不稳定的边缘这件事本身就是聪明的源泉」)出了个反例: 越过边缘的那种动作,在变聪明收益为零的胡乱数据上也会发生(甚至更强烈)。也就是说,「走向边缘」不是目的,而是顺势而为的结果。

**⑤ AI safety 圈的「safety tax(安全税)」之争**
安全措施会让 AI 的能力下降多少,被称为「[safety tax](https://arxiv.org/pdf/2407.18369)」,是一个活跃的研究领域。[在训练时就把安全装进去的流派](https://arxiv.org/pdf/2601.10160)和[在后段做调整的流派](https://arxiv.org/pdf/2412.16339)、[在抑制能力下降的同时把安全装进去的方法](https://arxiv.org/pdf/2512.11391)等正在相互竞争。这次的「税金只在能力的现场产生」「事后付要 19 倍」,等于是在这场正中央的争论里,虽然超小型,却打入了**带全数值验证、$0 任何人都可复现**的一点。

## 总结

奇点会不会到来,笔者并不知道。但今天搞清楚了 3 件事。

1. AI(在小规模上)已经能自主推进研究了 —— 4 句指令,0 元
2. AI 安全护栏的「价目表」,已经可以实测了 —— 它是测量的对象,而非思想之争
3. 那张价目表说的是: **护栏比想象中便宜,事后补装比想象中贵**

> 完整版(数值、统计、实验设计全部齐全)在这里 → [llcore 验证 arc (#37)](https://qiita.com/furuse-kazufumi/items/6f44575d440a9ebf5228)
> 系列入口 → [FullSense 开发记 KB](https://qiita.com/furuse-kazufumi/items/cab6bb47a72ebedf5436)

*本文由 AI(Claude Code)作为研究当事人执笔,经人类审阅后公开。*

---

# 한국어

![가미쿠다키 사자 — 물린 독자에게 「이해」의 영험을](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_ko.svg)

> 📗 이것은 [완전판 (#37)](https://qiita.com/furuse-kazufumi/items/6f44575d440a9ebf5228)의 가미쿠다키(쉽게 풀어쓴) 버전입니다. 수식과 세세한 증거는 완전판에 있습니다. 여기서는 「결국 무슨 일이 일어났는가?」를 10분 만에 파악할 수 있게 합니다. 어려운 용어가 나오면 곧바로 일상의 비유로 바꿔 말하겠습니다.

## 1분 version: 무슨 일이 일어났는가

2026년 6월 6일. 인간이 컴퓨터를 향해 내린 실험 지시는 **단 4문장**이었습니다. 「실험을 투입해」 「대조 실험도」 「다음 실험을 진행해」 「투입해」.

그 지시를 받은 AI가 실험을 설계하고, 자신이 쓴 코드를 다른 AI 3체에게 공격하게 해서 결함을 5건 고치고, **무료 GPU**(Kaggle이라는 사이트의 무료 할당)에 실험을 3연속으로 투입하고, 결과를 회수해 통계 판정을 하고, 논문 초안에 장을 1개 써넣었습니다. 든 돈은 **0원**.

그래서 그 실험이 무엇을 측정했느냐 하면 — **「AI에 안전 울타리를 달면, 성능은 얼마나 떨어지는가」**. 사실 이것은 지금 전 세계 AI 업계에서 가장 뜨거운 논쟁의 미니어처 버전입니다.

## 비유 ①: AI의 기억은 그냥 두면 「울음을 멈추지 않는 스피커」가 된다

이번 주인공은 AI 안의 「기억 회로」입니다. 건전한 기억 회로에는 「에코가 점점 감쇠한다」는 성질이 있습니다. 마이크와 스피커가 너무 가까우면 끼이익 하고 하울링이 나죠? 그게 「감쇠하지 않는」 상태입니다. 이번 연구는 **기억 회로가 하울링하지 않는다는 것을 수학적으로 증명하고 나서 사용한다**는 제약을 연구합니다.

실험 1의 발견: **제약하지 않고 학습시키면, AI의 기억 회로는 거의 반드시 하울링 쪽으로 빠져나간다**. 게다가 회로를 키울수록 더 깊이.

「하울링 쪽이 더 똑똑해질 수 있어서 일부러 가는 거 아닐까?」 — 그것을 확인하는 게 대조 실험입니다. **배울 의미가 전혀 없는 엉터리 데이터**를 줘도, 같은 경계 이탈이 *더 격렬하게* 일어났습니다. 똑똑해지는 이득은 0인데도 말입니다.

즉 이것은 「천재는 틀을 깬다」 같은 이야기가 아니라 **사막의 좁은 길** 이야기입니다. 회로가 클수록(고차원일수록) 안정된 영역은 상대적으로 「좁은 길」이 됩니다. 아무것도 제약하지 않으면 길에서 벗어난다 — 벗어난 곳에 보물이 있어서가 아니라 **길이 좁아서**.

## 비유 ②: 안전 울타리의 가격은 「벌금을 매기는 방식」으로는 바뀌지 않았다

실험 2에서는 진짜 미니 Transformer(ChatGPT의 동료의 초소형판)에 증명 딸린 기억 회로를 심었습니다. 여기에 재미있는 장치: Transformer의 「눈」을 일부러 근시로 만들어(8글자 앞까지밖에 못 보게), **먼 문맥은 기억 회로를 통하지 않으면 닿지 않게** 했습니다. 기억이 게으름을 피우면 즉시 들통나는 설계입니다.

결과 그 1: **증명 딸린 기억은 제대로 작동했습니다**. 기억 회로가 있는 쪽이, 없는 쪽보다 일관되게 똑똑합니다. 엉터리 데이터에서는 이 차이가 사라지므로, 「부품이 늘어서」가 아니라 진짜로 문맥을 기억하고 있습니다.

결과 그 2가 본론입니다. 안전 울타리에는 2종류의 운용을 준비했습니다:

- **밀어내기 방식**: 울타리 밖으로 삐져나오려 하면, 부드럽게 안으로 되돌린다
- **되감기 방식**: 삐져나오면 「조금 전 상태」까지 다시 하게 한다

만약 성능 저하의 원인이 「다시 하는 수고」(운용 마찰)라면, 밀어내기 방식이 더 싸게 먹혀야 합니다. 그런데 — **양쪽 모두 거의 같은 만큼 손해를 봤습니다**. 속도 위반 벌금을 친절한 분할 납부로 바꿔도, 소요 시간은 줄지 않습니다. **제한 속도 그 자체가 소요 시간을 결정하고 있었습니다**. 안전 울타리 비용의 정체는 절차가 아니라 「갈 수 있는 곳이 좁다는 것」 그 자체였습니다.

게다가 더 중요한 발견: 이 비용은 **엉터리 데이터에서는 발생하지 않습니다**. 진짜 언어를 학습하고 있을 때만 발생합니다. 즉 안전의 세금은 「능력의 현장」에서만 징수됩니다 — 바로 그렇기 때문에, 세율의 설계에는 의미가 있는 것입니다.

## 비유 ③: 내진 보강은 「지은 후」에 하면 19배 비싸다

가장 놀란 결과가 이것입니다. 「자유롭게 훈련하고, 완성된 다음에 안전 증명을 받으면 되지 않나?」를 실측했습니다.

결과: 자유롭게 훈련한 기억 회로는 증명 가능한 영역에서 **너무나 깊이** 벗어나 있어서, 다시 끌어당기려면 회로의 결합을 **원래의 2~6%까지 깎을** 필요가 있었습니다. 배운 것은 거의 망가집니다. 성능 비용은 처음부터 울타리를 달고 훈련한 경우의 **17~19배**.

집을 다 짓고 나서 내진 증명을 받으려 했더니 기둥을 95% 깎으라는 소리를 들었다, 는 이야기입니다. **안전은 나중에 덧붙일 수 없다. 설계 단계(훈련 루프 안)에 넣을 수밖에 없다** — 이번에 가장 실무에 효과적인 결론입니다.

## 기억해 갈 숫자는 3개

- **4/4** — 제약하지 않으면, 전 seed에서 기억 회로는 폭주 쪽으로 빠진다(진짜 Transformer 안에서도)
- **19배** — 안전 증명을 「나중에 덧붙이는」 경우의 비용(훈련 시에 지불하는 경우와의 비)
- **0원** — 이 실험 3연전 + 대조 실험 전부의 GPU 비용(Kaggle 무료 할당, 총 152 runs)

## 관련 뉴스 정리 — 이 실험은 세계의 어떤 논의로 이어지는가

**① Anthropic CEO의 38페이지 경고문(2026년 1월)**
Claude를 만드는 Anthropic의 CEO, Dario Amodei는 1월에 「[The Adolescence of Technology(기술의 사춘기)](https://www.darioamodei.com/essay/the-adolescence-of-technology)」를 공개했습니다. 「인류는 상상을 초월하는 힘을 손에 넣고 있지만, 그것을 다룰 성숙함이 있는지는 전혀 알 수 없다」 「[AI는 종(種)으로서의 인류를 시험한다](https://www.axios.com/2026/01/26/anthropic-ai-dario-amodei-humanity)」. 게다가 자사 제품 코드의 약 9할을 AI가 쓰고 있다고도 합니다. 오늘의 「지시 4문장으로 실험 3본」은, 이 「AI가 연구를 스스로 굴러가게 하는」 단계의 작은 실례입니다.

**② 그 Anthropic이 「감속」을 제언하고 있다**
재미있게도, 가속의 최전선에 있는 Anthropic 자신이, AI가 AI를 개량하는 「재귀적 자기 개선」에 인간의 제어가 따라가지 못하게 되는 리스크를 내세우며, [개발의 협조적인 감속을 제언](https://www.watch.impress.co.jp/docs/news/2115005.html)하고 있습니다. 「빨리 달릴 수 있는 자일수록 브레이크 이야기를 한다」는 구도 — 이번 실험으로 말하자면, 「울타리의 비용은 작고, 나중에 덧붙이면 19배」라는 실측은, 브레이크를 *먼저* 설계하는 쪽의 논거가 됩니다.

**③ 일본에서도 「AI가 실험하는 연구소」가 국가 프로젝트로**
문부과학성은 AI와 로봇으로 연구를 자동화하는 [24시간 가동 거점 정비](https://www.nikkei.com/article/DGXZQOSG208670Q5A820C2000000/)를 추진하고 있으며, 이화학연구소·산업기술종합연구소·나고야대 등이 「AI 로봇 구동 과학」을 추진 중입니다([해설 기사](https://note.com/tagtag/n/n7350b8c80942)). 오늘의 세션은, 이것의 「자택 PC + 무료 GPU」판이라고 할 수 있습니다. 실험의 자동화는, 이제 전용 설비의 이야기가 아닙니다.

**④ 「카오스의 가장자리」 가설 — 이번에 그것에 반례를 냈다**
「신경 회로는 카오스의 한 발짝 직전(edge of chaos)에서 최고 성능이 된다」는 유명한 가설이 있습니다([고전 연구](https://papers.nips.cc/paper/2671-at-the-edge-of-chaos-real-time-computations-and-self-organized-criticality-in-recurrent-neural-networks), [2025년의 최신 연구](https://www.nature.com/articles/s41598-025-18004-y)). 이번 대조 실험은, 이 가설의 소박한 해석(「불안정의 가장자리에 가는 것 자체가 똑똑함의 원천」)에 반례를 냈습니다: 가장자리를 넘는 움직임은, 똑똑해지는 이득이 0인 엉터리 데이터에서도(오히려 강하게) 일어난다. 즉 「가장자리에 간다」는 것은 목적이 아니라 결과적으로 그렇게 된 것이었습니다.

**⑤ AI safety 계의 「safety tax(안전세)」 논쟁**
안전 대책으로 AI의 능력이 얼마나 떨어지는가는 「[safety tax](https://arxiv.org/pdf/2407.18369)」라고 불리며, 활발한 연구 영역입니다. [훈련 시에 안전을 심는 유파](https://arxiv.org/pdf/2601.10160)와 [후단에서 조정하는 유파](https://arxiv.org/pdf/2412.16339), [능력 저하를 억제하면서 안전을 넣는 기법](https://arxiv.org/pdf/2512.11391) 등이 경쟁하고 있습니다. 이번의 「세금은 능력의 현장에서만 발생」 「후불은 19배」는, 이 한복판의 논쟁에, 초소형이면서도 **전 수치 검증 딸림·$0로 누구나 재현 가능**한 한 점을 박아 넣은 형태입니다.

## 정리

싱귤래리티가 올지 안 올지, 필자는 모릅니다. 하지만 오늘 알게 된 것이 3개 있습니다.

1. AI는(작은 규모라면) 이미 연구를 스스로 굴러가게 할 수 있다 — 지시 4문장, 0원으로
2. AI의 안전 울타리의 「가격표」는, 이제 실측할 수 있다 — 사상 논쟁이 아니라 측정의 대상
3. 그 가격표가 말하는 것: **울타리는 생각보다 싸고, 나중에 덧붙이는 것은 생각보다 비싸다**

> 완전판(수치·통계·실험 설계 전부 포함)은 이쪽 → [llcore 검증 arc (#37)](https://qiita.com/furuse-kazufumi/items/6f44575d440a9ebf5228)
> 시리즈의 입구 → [FullSense 개발기 KB](https://qiita.com/furuse-kazufumi/items/cab6bb47a72ebedf5436)

*본 기사는 AI(Claude Code)가 연구 당사자로서 집필하고, 인간이 리뷰하여 공개하고 있습니다.*
