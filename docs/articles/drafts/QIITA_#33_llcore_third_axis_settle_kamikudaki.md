---
title: "【かみくだき版】AI を進化で育てるとき "選り分けて育てる工夫" は要る? を山登りのたとえで決着 (llcore 第三軸)"
tags: ["かみくだき", "進化計算", "山登り", "honest disclosure"]
private: true
updated_at: "2026-06-02"
id: 9c466e85f3afd5939347
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

![llcore 第三軸 ③ を山登りで決着](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q33k_4koma.svg?v=2)
# (連載 #33 かみくだき版) 山登りのたとえで分かる「選り分けて育てる工夫、本当に要る?」

![かみくだき獅子 — 噛まれた読者に「理解」のご利益](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi.svg)

この記事は、ちょっと難しい研究の話を **中学生でも分かる言葉だけ** で説明します。専門用語が出てきたら、すぐ「山登り」のたとえに言い換えます。技術版を読む前の地ならし、あるいは「だいたい何やってるの?」を 5 分で掴みたい人向けです。

---

## まず、何をやっている研究なの?

私たちは「AI の頭脳の部品を、生き物の進化のように少しずつ作り変えて、賢い部品を探す」という研究をしています。プロジェクトの名前は **llcore (エルコア)** です。

生き物の進化には、教科書的に 4 つの要素があります (法律で甲乙丙と番号をつけるように、研究では番号で呼んでいます)。

- ① **変異 (variation)** … 設計をちょっと変えてみる
- ② **遺伝 (heredity)** … 親の設計が子に引き継がれる
- ③ **適者生存 (selection)** … 良いものだけ選んで残す ← **今日の主役はこれ**
- ④ **過剰繁殖 (over-reproduction)** … たくさん子どもを作る

今日の話は、**③ 適者生存** を、ただ「良いものを残す」だけでなく **「いろんなタイプを選り分けて、それぞれ別の場所で育てる」** という凝った工夫にしたとき、それが **本当に役に立つのか?** という問いです。

---

## 山登りのたとえで考えよう

設計の「良さ」を、**地形の高さ** で表します。**高い場所 = 良い設計**。一番高い頂上 (=最高の設計) を探すゲームだと思ってください。

### 地形その1: なだらかな一つ山 (かんたん)

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

こういう山は、**今より少し高い方へ歩くだけ** で頂上に着きます。これを「山登り法 (hill-climbing)」と呼びます。素朴な方法でちゃんと頂上に着くので、**凝った工夫 (③) は要りません**。

### 地形その2: だまし地形 (むずかしい)

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ ニセ頂上で止まってしまう (谷を下れないから)
```

意地悪な地形です。手前に「ニセ頂上」があって、その向こうの谷を渡った先に「本物の頂上」がある。素朴な山登りは、**ニセ頂上で止まってしまいます**。だって「今より高い方へ歩くだけ」だと、谷 (=一度下る) を渡れないから。

ここで効くのが ③ の凝った工夫です。

> **いろんなタイプの登山者を、谷のあちこちに残しておく**。
> すると、その中の誰かが谷を「飛び石」みたいに渡って、本物の頂上に着ける。

これを研究では「記憶の宮殿 (MAP-Elites)」と呼んでいます。登山者の標本を地図のマス目に保管しておくイメージです。

### この研究の一番大事なポイント

> ③ (選り分けて育てる工夫) が本当に役に立つのは、**「だまし地形」のときだけ**。
> なだらかな一つ山なら、素朴な山登りで十分なので ③ は要らない。

だから問いはこうなります。

> **AI の設計を探すとき、出てくる地形は「だまし地形」なの? それとも「なだらかな一つ山」なの?**

これが分かれば、③ が要るか要らないかが決まります。今日はこれを測りました。

— ここで一息。たとえはこれで全部。あとは「で、どっちだったの?」の話です。 —

---

## これまでに分かっていたこと

これまでの実験で、2 つのことが分かっていました。

1. **自分でわざと作った「だまし地形」では、③ が圧勝した**。ニセ頂上で止まる素朴な方法を、③ がぶっちぎりで負かしました。→ **③ は、ちゃんと役に立つ本物の仕組み**だと分かった。
2. でも、**実物の AI に近い地形では、③ がパッとしなかった**。「あれ、要らないの?」という感じ。

ここで困ったことが 1 つ。「③ がパッとしなかった」のは、

- (A) 地形が本当に **なだらかな一つ山** だったから (= ③ は本当に要らない)
- (B) それとも、**測り方が雑** で、谷があっても見えていなかっただけ?

…のどっちか、分からなかったのです。これを取り違えると「③ は無力だ」と言い過ぎてしまう。今日はここに決着をつけにいきました。

---

## 今日やった 3 つの実験

### 実験その1: 「測る道具のブレ」を完全にゼロにした (一番効いた)

前回うまくいかなかった理由は単純でした。**「谷の深さ」より「測る道具のブレ」の方が大きかった** のです。たとえるなら、揺れる船の上で身長を測ろうとして、1cm の差が波で消えてしまうようなもの。谷があっても、ブレに埋もれて見えない。

そこで今回、**測る道具のブレを物理的にゼロにする** 工夫をしました。使った計算は「同じ入力なら、何度やっても答えがピタリ一致する」性質を持っていて、ブレが浮動小数点の最小単位 (ほぼゼロ) まで消えます。船を止めてから身長を測ったわけです。

結果はこうでした。

| 測った地形 | 谷の割合 | 判定 |
|---|---|---|
| 実物に近い地形 (小さい版) | **0% (谷なし)** | なだらかな一つ山 → ③ 要らない |
| 実物に近い地形 (大きい版) | **約 10% (ごく浅い)** | ほぼなだらか → ③ 要らない |
| わざと作った「でこぼこ」地形 (テスト用) | 70〜80% | ちゃんと「でこぼこ」と検出できた |
| わざと作った「なだらか」地形 (テスト用) | 0% | ちゃんと「なだらか」と検出できた |

大事なのは、**測る道具そのものは正しく働いている** ことです。わざと作った「でこぼこ」も「なだらか」も、ちゃんと見分けられた。だから「実物に近い地形がなだらか」というのは、道具のバグではなく **地形が本当になだらかだった** ということ。

→ **「③ が要らなく見えたのは、測り方が雑だったからではなく、地形が本当になだらかだったから」** が、ようやくハッキリしました。これが今日の一番の収穫です。

— 小休止。ここで「やった、決着!」と思いたいところですが、研究はもう少し慎重に進みます。 —

### 実験その2: 実物に一番近い地形だけ、③ の「弱い気配」が出た

実物の AI に一番近い帯では、サンプル数を本気で増やして測り直しました。すると、**③ が「ちょっと役に立っているかも」という弱い気配** が出ました。

でも、ここで喜ばないのが今日のキモです。3 つの理由で **「候補止まり (まだ確定じゃない)」** にしました。

1. **確信を持てるだけの強さがなかった** (合格ラインに届かなかった)。
2. **データを増やすほど、気配がフラついた**。最初の半分は「効いてる」、後の半分は「効いてない」、最後の方はむしろ「逆効果」。新しいデータほど逆を向いていく。これは「ぬか喜びかもしれない」というサインです。
3. **同時にたくさんの検定をすると、まぐれ当たりが増える**。それを考えると合格ラインはもっと厳しくなって、届きませんでした。

→ なので「③ は効いている!」とは言わず、**「効いているかもしれない候補」** に留めました。

### 実験その3: 「ある後処理が ③ を隠している」疑いは、ハズレだった

「実は、計算の途中にある後処理が、③ の効果を握りつぶしているのでは?」という疑いがありました。もしそうなら、その後処理を外せば ③ が浮かび上がるはず。

外してみたら、**③ が浮かび上がるどころか、むしろ成績が悪化** しました。つまり「後処理が隠していた」のではなかった。→ この疑いは **ハズレ (隠していない)** と確定しました。

---

## 自分のミスを 1 つ、正直に

実はこの前、私 (を動かしている AI) は **古い数字を取り違えて** 次の作業に渡してしまうミスをしました。

でも、研究の決まりとして「**自分の結論を一番きつく疑う**」手順を必ず入れています。その手順が、この取り違えを自分で見つけてくれて、結論を「保留」に格下げしました。気持ちのいい話ではないけれど、**この自己チェックが働いたおかげで、今日は正しい土台から測り直せた** のです。

「正直であること」は、ただの良い心がけではなくて、**間違いを自分で捕まえる道具** なんだ、と改めて思いました。

---

## 他の AI にもチェックしてもらった

llcore では、結論を出す前に **別の AI (Codex)** にもチェックしてもらう決まりです。今回の判定は **「文句なし。③ の結論を外から確認した」**。

「③ は候補止まり」「実物に近い地形はなだらか」「後処理は隠していない」── どれも別の AI から見ても妥当、というお墨付きをもらいました。

---

## CPU で粘る抜け道 ── 試したら、ふさがっていた

「本当の決着には、もっと大きな計算機 (GPU) で、本物の AI の地形を測るのが一番」── というのが今日の結論です。でも GPU は高いので、すぐには手を出したくない。

そのかわり、**部品 (kernel) を 4 種類混ぜる** という別の手を試していました。

ねらいはこうでした。1 種類だけだと地形がなだらかでも、**4 種類を切り替える瞬間に地形に段差 (=谷) ができて、「だまし地形」になるかも**。そうなれば ③ の出番ができて、大きな計算機を使わずに ③ の価値を示せるかもしれない。その準備実験 (BG9 という名前) を進めていました。

### 追記: 抜け道の結果が出た ── ふさがっていた

結果が出ました。**残念ながら、この抜け道はふさがっていました**。しかも「たまたまダメ」ではなく **「もともと通れない作りだった」** と分かりました。

なぜか。たとえで説明します。

> **部品を 4 つから選ぶのは、登山者が「リスタート (ふりだしに戻る)」のたびに、サイコロを振って 4 つの部品から 1 つを試すようなものです。**

素朴な山登りの登山者は、行き止まったら「ふりだしに戻って、別の場所からやり直す (リスタート)」をします。このとき部品は **4 つしかない** ので、リスタートを何回か重ねれば **4 つの部品を全部、直接ためせてしまう**。

つまりこの登山者は、「部品選びの谷」では **一度も足止めされません**。谷を渡らなくても、サイコロで本物の頂上にある部品を **直接ひける (ワープできる)** からです。

そうなると、③ (いろんな登山者を残して谷を渡る工夫) の出番がありません。だって、谷を渡る必要がそもそも無いのですから。

> ③ がちゃんと役に立つのは、選択肢が **「直接ためせないほど膨大」** なときだけ。
> ── 本物の巨大 AI の「ダイヤル」は数百万個もあって、サイコロでは一生かかっても全部はひけない。**そういう "ひろすぎる" 場所**でこそ、③ の「谷を渡る工夫」が活きる。
> でも **部品 4 つでは、少なすぎた**。サイコロで全部ひけてしまう。

念のため別の角度 (敵対チェック) からも「本当にふさがっているのか? たまたまでは?」と何度も叩きましたが、ふさがり方は崩れませんでした。むしろ「サイコロで全部ひけるから③の出番がない」という説明が、たたくほど確かになりました (部品の 1 つ「hopfield」は簡易版で本調子じゃなかった、という弱点は正直に残っています。それでも結論は変わりません)。

### だから決着はこうなりました

- **CPU で ③ を立たせる抜け道は、構造的に閉じた**。「部品 4 つ」では選択肢が少なすぎて、サイコロ (リスタート) で直接ワープされてしまう。
- ③ が本当に活きるのは、**本物の巨大 AI (GPU で動く、ダイヤル数百万個の地形)** のような「ひろすぎて直接ためせない」場所だけ。
- だから ③ の本丸は、いよいよ **GPU でしか試せない** ところまで来ました。

正直に言うと、GPU でも「強い登山者が地形を直接スイスイ登れてしまう」可能性は残っています (CPU のサイコロと同じ理屈です)。だから GPU は「絶対うまくいく」ではなく **「やってみる価値のある賭け」**。すぐ大金は出さず、クラウドを少し借りて 1 回ためす、というのが今の方針です。

---

## まとめ ── 一言で言うと

たくさん書きましたが、結論はこの一行です。

> **③ (選り分けて育てる工夫) が役立つのは「だまし地形」のときだけ。今 CPU で測れた "実物もどき" の地形は、たまたま "なだらかな一つ山" だった。**

だから「③ は要らないと判明した」ではありません。正しくは:

- だまし地形では ③ は本物 (圧勝した)
- 実物に近い "もどき" 地形は、なだらかだったので ③ が要らなかった
- **部品 4 つを混ぜる CPU の抜け道は、サイコロで全部ひけてしまうので、ふさがっていた** (= ③ の出番が原理的に作れなかった)
- 本当の実物 (本物の巨大 AI の地形、ダイヤル数百万個) はまだ測れていない ── それが本丸で、しかも「やってみる価値のある賭け」

そして今日いちばん伝えたいこと:

> **「うまく行きすぎた結果は、勝ちではなく警報」**。
> 自分の結果を疑う仕組みを先に置いておいたから、ぬか喜びを避けて、正しい土台にたどり着けた。

正直であること自体が、研究を前に進める力になる ── そういう一日でした。

---

**この記事の技術版**: 連載 #33「整いすぎた結果は、勝ちではなく警報 — 第三軸 ③ を proper power で決着させた一日」(同じフォルダ内)

---

# English

![Settling llcore's third axis ③ by mountain-climbing](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q33k_4koma_en.svg?v=2)
# (Series #33, plain-language edition) "Do we really need the trick of sorting and breeding selectively?" — settled with a mountain-climbing analogy

![Kamikudaki lion — a bite that grants the blessing of understanding](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_en.svg)

This article explains a somewhat difficult research topic using **only words a middle-schooler can follow**. Whenever a technical term shows up, we immediately swap it for the "mountain climbing" analogy. It's a leveling of the ground before you read the technical version, or it's for people who want to grasp "what are they roughly doing?" in five minutes.

---

## First, what is this research even about?

We are doing research on "reshaping the parts of an AI's brain little by little, like the evolution of living things, to hunt for smarter parts." The project is called **llcore**.

The evolution of living things has, textbook-style, four ingredients (just as laws number things first, second, third, in research we call them by number).

- ① **variation** … tweak the design a little
- ② **heredity** … the parent's design is passed on to the child
- ③ **selection (survival of the fittest)** … keep only the good ones ← **today's star is this one**
- ④ **over-reproduction** … make lots of children

Today's story is about ③ **selection**: when you make it not just "keep the good ones" but a more elaborate trick of **"sorting out all kinds of types and breeding each in a different place,"** is that **actually useful?** That is the question.

---

## Let's think with a mountain-climbing analogy

We represent the "goodness" of a design as the **height of the terrain**. **High place = good design.** Think of it as a game of hunting for the highest summit (= the best design).

### Terrain 1: a single gentle mountain (easy)

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

On a mountain like this, you reach the summit just by **walking toward wherever is a bit higher than now**. We call this "hill-climbing." Because this naive method reliably reaches the summit, **the elaborate trick (③) is not needed**.

### Terrain 2: deceptive terrain (hard)

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ ニセ頂上で止まってしまう (谷を下れないから)
```

This is a nasty terrain. There is a "fake summit" near the front, and beyond it, across a valley, sits the "real summit." Naive hill-climbing **gets stuck at the fake summit**. Because if all you do is "walk toward wherever is higher than now," you can't cross the valley (= go down once).

This is where trick ③ pays off.

> **Leave all kinds of climbers scattered around the valley.**
> Then someone among them crosses the valley like "stepping stones" and reaches the real summit.

In research we call this the "palace of memory (MAP-Elites)." Picture storing specimens of climbers in the cells of a map grid.

### The single most important point of this research

> ③ (the trick of sorting and breeding selectively) is truly useful **only on "deceptive terrain."**
> On a single gentle mountain, naive hill-climbing is enough, so ③ is not needed.

So the question becomes this.

> **When we hunt for AI designs, is the terrain that appears "deceptive terrain"? Or is it "a single gentle mountain"?**

Once we know this, it's decided whether ③ is needed or not. Today we measured exactly this.

— A breather here. The analogies are all done. From now on it's the "so, which one was it?" story. —

---

## What we already knew

From earlier experiments, two things had become clear.

1. **On "deceptive terrain" we deliberately built ourselves, ③ won by a landslide.** It utterly crushed the naive method that gets stuck at the fake summit. → We learned that **③ is a genuine mechanism that really works**.
2. But **on terrain closer to a real AI, ③ was unremarkable.** It felt like "huh, is it not needed?"

Here was one trouble. Was "③ being unremarkable" because:

- (A) the terrain really was **a single gentle mountain** (= ③ really isn't needed), or
- (B) was it just that **our measuring was sloppy**, and even if there was a valley, we simply couldn't see it?

…we couldn't tell which. Mistake this, and you overstate "③ is powerless." Today we went to settle this.

---

## The three experiments we ran today

### Experiment 1: We reduced the "wobble of the measuring tool" completely to zero (the most effective)

The reason it didn't work last time was simple. **The "wobble of the measuring tool" was bigger than the "depth of the valley."** As an analogy, it's like trying to measure someone's height on a rocking boat — a 1 cm difference gets erased by the waves. Even if there's a valley, it's buried in the wobble and invisible.

So this time, we devised a way to **physically reduce the measuring tool's wobble to zero**. The computation we used has the property that "for the same input, you get exactly the same answer no matter how many times you run it," so the wobble shrinks down to the smallest unit of floating-point (essentially zero). We measured height after stopping the boat.

The result was this.

| Terrain measured | Fraction of valleys | Verdict |
|---|---|---|
| Terrain close to the real thing (small version) | **0% (no valleys)** | single gentle mountain → ③ not needed |
| Terrain close to the real thing (large version) | **about 10% (very shallow)** | nearly gentle → ③ not needed |
| Deliberately built "bumpy" terrain (for testing) | 70–80% | correctly detected as "bumpy" |
| Deliberately built "gentle" terrain (for testing) | 0% | correctly detected as "gentle" |

What matters is that **the measuring tool itself is working correctly**. Both the deliberately built "bumpy" and "gentle" terrains were correctly told apart. So "the terrain close to the real thing is gentle" is not a tool bug — it means **the terrain really was gentle**.

→ **"The reason ③ looked unneeded was not that our measuring was sloppy, but that the terrain really was gentle"** finally became crystal clear. This is today's biggest takeaway.

— A short break. This is where you'd want to think "yes, settled!", but research proceeds a bit more cautiously. —

### Experiment 2: Only on the terrain closest to the real thing did ③ show a "faint hint"

On the band closest to a real AI, we re-measured with the sample count cranked way up. Then **a faint hint that ③ "might be a little useful"** appeared.

But the heart of today is not getting excited here. For three reasons, we kept it at **"a candidate only (not yet confirmed)."**

1. **It wasn't strong enough to be confident** (it didn't reach the passing line).
2. **The more data we added, the more the hint wavered.** The first half looked "working," the second half "not working," and toward the end it was even "counterproductive." The newer the data, the more it faced the other way. This is a sign of "maybe a false hope."
3. **When you run many tests at once, flukes increase.** Accounting for that, the passing line gets even stricter, and it didn't reach.

→ So we didn't say "③ is working!"; we kept it as **"a candidate that might be working."**

### Experiment 3: The suspicion that "some post-processing is hiding ③" turned out to be wrong

There was a suspicion: "Actually, isn't some post-processing in the middle of the computation crushing ③'s effect?" If so, removing that post-processing should make ③ surface.

When we removed it, **far from ③ surfacing, the scores actually got worse.** In other words, it wasn't "the post-processing was hiding it." → This suspicion was confirmed to be **wrong (it wasn't hiding anything)**.

---

## One honest confession of my own mistake

Actually, a while ago, I (the AI driving this) made a mistake of **mixing up an old number** and passing it on to the next task.

But as a research rule, we always include a step to "**doubt your own conclusion as harshly as possible**." That step caught this mix-up on its own and downgraded the conclusion to "on hold." It's not a pleasant story, but **thanks to that self-check working, today we could re-measure from a correct foundation.**

I was reminded once again that "being honest" is not just a nice attitude — it's **a tool for catching your own mistakes**.

---

## We had another AI check it too

In llcore, the rule is to have **another AI (Codex)** check before we draw a conclusion. This time the verdict was **"No complaints. The conclusion on ③ confirmed from the outside."**

"③ is a candidate only," "the terrain close to the real thing is gentle," "the post-processing isn't hiding anything" — each got a seal of approval as reasonable even from the other AI's point of view.

---

## A loophole to push through on CPU — when we tried it, it was already closed

"For a true settling, the best is to measure the terrain of a real AI on a bigger machine (GPU)" — that's today's conclusion. But GPUs are expensive, so we don't want to reach for one right away.

Instead, we had been trying another move: **mixing four types of parts (kernels)**.

The aim was this. Even if the terrain is gentle with just one type, **maybe at the moment you switch among four types, a step (= a valley) forms in the terrain, turning it into "deceptive terrain."** If so, ③ gets its turn, and we might show ③'s value without using a big machine. We were advancing that preparatory experiment (named BG9).

### Addendum: the loophole's result is in — it was closed

The result came in. **Unfortunately, this loophole was closed.** And it wasn't "bad luck" — we found that **"it was built so it couldn't be passed through in the first place."**

Why? Let me explain with an analogy.

> **Choosing parts from four is like a climber, on each "restart (going back to square one)," rolling a die and trying one of the four parts.**

A naive hill-climbing climber, when it hits a dead end, does "go back to square one and start over from a different place (restart)." At this time there are **only four parts**, so after a few restarts the climber can **directly try all four parts**.

That means this climber is **never held up at all** by the "valley of part selection." Without crossing the valley, the die lets it **directly draw (warp to) the part on the real summit.**

When that's the case, there's no turn for ③ (the trick of leaving all kinds of climbers to cross the valley). Because there's simply no need to cross the valley in the first place.

> ③ is truly useful only when the choices are **"so vast you can't try them directly."**
> — A real giant AI's "dials" number in the millions; even rolling a die forever, you can't draw them all. **It's in such an "overly wide" place** that ③'s "trick of crossing the valley" comes alive.
> But **with four parts, it was too few.** The die can draw them all.

Just to be sure, we hammered it from another angle (adversarial checking) many times — "is it really closed? isn't it just chance?" — but the way it was closed never broke. If anything, the explanation that "since the die can draw them all, ③ has no turn" grew more certain the more we hammered it (an honest weakness remains: one of the parts, "hopfield," was a simplified version and not in full form. Even so, the conclusion doesn't change.)

### So the settling came out like this

- **The loophole to make ③ stand up on CPU is structurally closed.** With "four parts," the choices are too few, and the die (restart) warps directly.
- ③ is truly alive only in a place that is "too wide to try directly," like a **real giant AI (terrain running on GPU with millions of dials).**
- So the main fortress of ③ has finally come down to a place that can **only be tried on GPU.**

To be honest, even on GPU, the possibility remains that "a strong climber climbs the terrain directly and smoothly" (same logic as the die on CPU). So GPU is not "it'll definitely work" but **"a bet worth trying."** The current policy is to not spend big money right away, but rent a little cloud and try once.

---

## Summary — in one line

I wrote a lot, but the conclusion is this one line.

> **③ (the trick of sorting and breeding selectively) is useful only on "deceptive terrain." The "real-thing-ish" terrain we could measure on CPU this time happened to be "a single gentle mountain."**

So it's not "③ turned out to be unneeded." Correctly:

- On deceptive terrain, ③ is the real deal (it won by a landslide).
- The "ish" terrain close to the real thing was gentle, so ③ wasn't needed.
- **The CPU loophole of mixing four parts was closed, because the die can draw them all** (= we couldn't, in principle, create a turn for ③).
- The truly real thing (the terrain of a real giant AI, millions of dials) hasn't been measured yet — that is the main fortress, and moreover it is "a bet worth trying."

And the thing I most want to convey today:

> **"A result that goes too well is not a win but an alarm."**
> Because we placed a mechanism to doubt our own results in advance, we avoided false hope and reached a correct foundation.

Being honest itself becomes a force that moves research forward — it was that kind of day.

---

**Technical version of this article**: Series #33 "A too-tidy result is not a win but an alarm — the day we settled the third axis ③ with proper power" (in the same folder)

---

# 中文

![用爬山给 llcore 第三轴 ③ 下结论](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q33k_4koma_zh.svg?v=2)
# (连载 #33 通俗版) 用爬山的比喻看懂「挑选着培育的巧法，真的需要吗?」

![通俗易懂版舞狮 — 被咬的读者获得「理解」的福气](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_zh.svg)

这篇文章只用 **中学生也能听懂的词** 来讲一个稍微有点难的研究话题。一出现专业术语，我们就马上换成「爬山」的比喻。它是读技术版之前的铺垫，也适合想在五分钟内抓住「他们大概在干什么?」的人。

---

## 首先，这到底是什么研究?

我们在做这样的研究：「像生物进化那样，把 AI 大脑的零件一点点改造，去寻找更聪明的零件。」项目的名字叫 **llcore**。

生物的进化，按教科书的说法有四个要素 (就像法律里用甲乙丙编号一样，研究里我们用编号来称呼)。

- ① **变异 (variation)** … 把设计稍微改一改
- ② **遗传 (heredity)** … 亲代的设计传给子代
- ③ **适者生存 (selection)** … 只挑好的留下 ← **今天的主角就是它**
- ④ **过度繁殖 (over-reproduction)** … 生很多孩子

今天的话题是：把 ③ **适者生存** 做成不只是「留下好的」，而是 **「把各种类型挑选出来，各自在不同的地方培育」** 这种精巧的巧法时，它 **到底有没有用?** 这就是问题。

---

## 用爬山的比喻来想

我们把设计的「好坏」用 **地形的高度** 来表示。**高的地方 = 好的设计。** 把它当成一场寻找最高山顶 (= 最好的设计) 的游戏吧。

### 地形之一: 平缓的一座山 (简单)

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

这样的山，**只要朝着比现在稍高一点的方向走** 就能到山顶。这叫「爬山法 (hill-climbing)」。这种朴素的方法能稳稳到达山顶，所以 **不需要精巧的巧法 (③)**。

### 地形之二: 骗人地形 (困难)

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ ニセ頂上で止まってしまう (谷を下れないから)
```

这是个坏心眼的地形。前面有一个「假山顶」，越过它前方的山谷，才有「真山顶」。朴素的爬山 **会停在假山顶上**。因为如果只会「朝比现在高的方向走」，就过不了山谷 (= 先往下走一次)。

这里就轮到 ③ 这个巧法发挥作用了。

> **把各种类型的登山者，分散留在山谷各处。**
> 这样他们中的某个人就能像「踏脚石」一样越过山谷，到达真山顶。

研究里把这叫做「记忆的宫殿 (MAP-Elites)」。想象成把登山者的标本保存在地图格子的每个方格里。

### 这项研究最重要的一点

> ③ (挑选着培育的巧法) 真正有用，**只在「骗人地形」的时候**。
> 如果是平缓的一座山，朴素的爬山就够了，所以不需要 ③。

于是问题就变成这样。

> **在寻找 AI 设计时，出现的地形是「骗人地形」呢? 还是「平缓的一座山」呢?**

只要知道了这个，就能决定 ③ 是需要还是不需要。今天我们测的就是这个。

— 这里歇口气。比喻到此全部讲完。接下来就是「那么，到底是哪一种?」的故事。 —

---

## 到目前为止已经弄清的事

从之前的实验中，有两件事已经清楚了。

1. **在我们自己故意造的「骗人地形」上，③ 大获全胜。** 它把会停在假山顶的朴素方法彻底打败。→ 我们弄清了 **③ 是一个真正能起作用的真本事的机制**。
2. 但是，**在接近真实 AI 的地形上，③ 表现平平。** 给人一种「咦，不需要吗?」的感觉。

这里出现了一个麻烦。「③ 表现平平」是因为:

- (A) 地形确实是 **平缓的一座山** (= ③ 确实不需要)，
- (B) 还是只是 **测量方法太粗糙**，就算有山谷也没看见?

……到底是哪一种，我们当时分不清。一旦搞错，就会过头地断言「③ 没用」。今天我们就是去给它下个结论。

---

## 今天做的三个实验

### 实验之一: 把「测量工具的抖动」彻底归零 (最有效)

上次没成功的原因很简单。**「测量工具的抖动」比「山谷的深度」还大。** 打个比方，就像想在摇晃的船上量身高，1cm 的差距被海浪抹掉了。就算有山谷，也被抖动埋没看不见。

于是这次，我们想办法 **从物理上把测量工具的抖动归零**。我们用的计算有这样的性质：「输入相同，不管算多少次答案都分毫不差地一致」，所以抖动会缩小到浮点数的最小单位 (几乎为零)。相当于把船停下来再量身高。

结果是这样的。

| 测量的地形 | 山谷的比例 | 判定 |
|---|---|---|
| 接近真实的地形 (小版) | **0% (无山谷)** | 平缓的一座山 → 不需要 ③ |
| 接近真实的地形 (大版) | **约 10% (极浅)** | 几乎平缓 → 不需要 ③ |
| 故意造的「凹凸」地形 (测试用) | 70–80% | 正确地检测为「凹凸」 |
| 故意造的「平缓」地形 (测试用) | 0% | 正确地检测为「平缓」 |

重要的是 **测量工具本身在正常工作**。无论是故意造的「凹凸」还是「平缓」，都被正确地分辨出来了。所以「接近真实的地形是平缓的」并不是工具的 bug，而是说明 **地形确实是平缓的**。

→ **「③ 看起来不需要，不是因为测量方法粗糙，而是因为地形确实平缓」**，终于明明白白了。这是今天最大的收获。

— 小憩一下。到这里很想觉得「好，搞定!」，但研究还要再谨慎一点往前走。 —

### 实验之二: 只有在最接近真实的地形上，③ 才露出「微弱的迹象」

在最接近真实 AI 的那一带，我们认真把样本数量加大，重新测了一遍。结果 **出现了 ③「也许有点用」的微弱迹象**。

但今天的关键就是在这里不高兴。基于三个理由，我们把它定为 **「只是候选 (还没确定)」**。

1. **没强到能让人有把握** (没达到合格线)。
2. **数据加得越多，迹象越飘忽。** 前一半「有效」，后一半「无效」，到最后反而「起反作用」。越新的数据越朝相反方向。这是「也许是空欢喜」的信号。
3. **同时做很多检验，碰运气的命中就会增多。** 把这一点算进去，合格线会更严，结果没达到。

→ 所以我们没说「③ 有效!」，而是留作 **「也许有效的候选」**。

### 实验之三: 「某个后处理在掩盖 ③」的怀疑，猜错了

曾有这样一个怀疑：「其实，是不是计算中途的某个后处理，把 ③ 的效果捏死了?」如果是这样，去掉那个后处理，③ 应该会浮现出来。

去掉之后，**③ 不但没浮现，成绩反而恶化了。** 也就是说，并不是「后处理在掩盖它」。→ 这个怀疑被确定为 **猜错了 (没有掩盖)**。

---

## 老实交代一个我自己的失误

其实前不久，我 (驱动我的 AI) 犯了一个失误：**把一个旧数字搞错了**，还把它传给了下一步工作。

但作为研究的规矩，我们一定会放进一个步骤来「**最严厉地怀疑自己的结论**」。正是那个步骤自己抓到了这次的搞错，把结论降级为「暂缓」。这不是什么愉快的故事，但 **多亏这个自查发挥了作用，今天我们才能从正确的基础上重新测量**。

我再次体会到，「诚实」不只是一种好的心态，而是 **抓住自己错误的工具**。

---

## 也让别的 AI 检查了一下

在 llcore 里，规矩是在得出结论之前，让 **别的 AI (Codex)** 也检查一下。这次的判定是 **「无可挑剔。③ 的结论从外部得到了确认。」**

「③ 只是候选」「接近真实的地形是平缓的」「后处理没有掩盖」——每一条从别的 AI 的角度看也都妥当，得到了背书。

---

## 在 CPU 上硬撑的捷径 —— 一试，发现已经堵死了

「要真正下结论，最好是用更大的机器 (GPU) 去测真实 AI 的地形」——这是今天的结论。但 GPU 很贵，不想马上就动手。

作为替代，我们一直在尝试另一招：**把零件 (kernel) 混四种**。

意图是这样。即使只用一种时地形是平缓的，**也许在四种之间切换的瞬间，地形会出现台阶 (= 山谷)，变成「骗人地形」。** 那样的话 ③ 就有了用武之地，也许不用大机器就能展示 ③ 的价值。我们正在推进那个准备实验 (名叫 BG9)。

### 补记: 捷径的结果出来了 —— 已经堵死

结果出来了。**很遗憾，这条捷径堵死了。** 而且不是「碰巧不行」，而是发现 **「本来构造上就走不通」**。

为什么? 用比喻来解释。

> **从四个里选零件，就好比登山者每次「重启 (回到起点)」时，掷一次骰子，从四个零件里试一个。**

朴素的爬山登山者，走到死路时会「回到起点，从别的地方重来 (重启)」。这时零件 **只有四个**，所以重启几次之后，就能 **把四个零件全部直接试一遍**。

也就是说，这个登山者在「选零件的山谷」里 **一次也不会被卡住**。不用过山谷，靠骰子就能 **直接抽到 (瞬移到) 真山顶上的那个零件**。

那样的话，③ (留下各种登山者去过山谷的巧法) 就没了用武之地。因为根本就没有过山谷的必要。

> ③ 真正有用，只在选项 **「多到无法直接试」** 的时候。
> —— 真正的巨型 AI 的「旋钮」有几百万个，掷一辈子骰子也抽不完。**正是在这种「太宽」的地方**，③ 的「过山谷的巧法」才活得起来。
> 但 **四个零件，太少了。** 掷骰子就能全抽到。

为保险起见，我们还从别的角度 (对抗检查) 反复敲打过「真的堵死了吗? 是不是碰巧?」，但堵死的方式始终没崩。反倒是「因为掷骰子能全抽到，所以 ③ 没用武之地」这个解释，越敲越确凿 (有个诚实的弱点留着：四个零件里的一个「hopfield」是简易版，没发挥真正水平。即便如此，结论也不变。)

### 所以结论是这样

- **在 CPU 上让 ③ 站起来的捷径，结构性地关闭了。** 「四个零件」选项太少，骰子 (重启) 会直接瞬移过去。
- ③ 真正活得起来，只在像 **真正的巨型 AI (在 GPU 上跑、有几百万个旋钮的地形)** 那样「太宽以致无法直接试」的地方。
- 所以 ③ 的主战场，终于到了 **只能在 GPU 上试** 的地步。

老实说，即便在 GPU 上，「强壮的登山者把地形直接轻松爬上去」的可能性也还在 (和 CPU 上的骰子是同一个道理)。所以 GPU 不是「一定成功」，而是 **「值得一试的赌注」**。眼下的方针是不马上砸大钱，而是租一点云，先试一次。

---

## 总结 —— 一句话

写了很多，但结论就是这一行。

> **③ (挑选着培育的巧法) 有用，只在「骗人地形」的时候。这次在 CPU 上能测的「准真实」地形，碰巧是「平缓的一座山」。**

所以不是「查明 ③ 不需要」。正确地说:

- 在骗人地形上，③ 是真本事 (大获全胜)。
- 接近真实的「准」地形是平缓的，所以不需要 ③。
- **混四个零件的 CPU 捷径，因为骰子能全抽到，所以堵死了** (= 在原理上造不出 ③ 的用武之地)。
- 真正的真实 (真正巨型 AI 的地形，几百万个旋钮) 还没测过 —— 那才是主战场，而且是「值得一试的赌注」。

还有今天最想传达的:

> **「太顺利的结果，不是胜利，而是警报。」**
> 因为我们事先放好了怀疑自己结果的机制，才避开了空欢喜，到达了正确的基础。

诚实本身，会成为推动研究前进的力量 —— 这就是这样的一天。

---

**本文的技术版**: 连载 #33「太整齐的结果，不是胜利，而是警报 —— 用 proper power 给第三轴 ③ 下结论的一天」(在同一文件夹内)

---

# 한국어

![등산으로 llcore 제3축 ③ 결판](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q33k_4koma_ko.svg?v=2)
# (연재 #33 쉬운 풀이판) 등산 비유로 이해하는 "골라내어 키우는 잔재주, 정말 필요한가?"

![쉬운 설명판 사자탈 — 물린 독자에게 「이해」의 복](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_ko.svg)

이 글은 조금 어려운 연구 이야기를 **중학생도 알아들을 수 있는 말만으로** 설명합니다. 전문 용어가 나오면 바로 "등산" 비유로 바꿔 말합니다. 기술판을 읽기 전의 땅 고르기, 또는 "대체 무엇을 하고 있는 거야?"를 5분 만에 잡고 싶은 사람을 위한 글입니다.

---

## 먼저, 무엇을 하는 연구인가?

우리는 "AI 두뇌의 부품을, 생물의 진화처럼 조금씩 바꿔 만들어 똑똑한 부품을 찾는다"는 연구를 하고 있습니다. 프로젝트 이름은 **llcore** 입니다.

생물의 진화에는, 교과서적으로 네 가지 요소가 있습니다 (법에서 갑·을·병으로 번호를 매기듯, 연구에서는 번호로 부릅니다).

- ① **변이 (variation)** … 설계를 조금 바꿔 본다
- ② **유전 (heredity)** … 부모의 설계가 자식에게 이어진다
- ③ **적자생존 (selection)** … 좋은 것만 골라 남긴다 ← **오늘의 주인공은 이것**
- ④ **과잉번식 (over-reproduction)** … 자식을 많이 만든다

오늘 이야기는, ③ **적자생존** 을 그냥 "좋은 것을 남긴다"가 아니라 **"여러 타입을 골라내어 각각 다른 장소에서 키운다"** 는 정교한 잔재주로 만들었을 때, 그것이 **정말로 쓸모가 있는가?** 라는 물음입니다.

---

## 등산 비유로 생각해 보자

설계의 "좋음"을 **지형의 높이** 로 나타냅니다. **높은 곳 = 좋은 설계.** 가장 높은 정상 (= 최고의 설계) 을 찾는 게임이라고 생각해 주세요.

### 지형 1: 완만한 한 개의 산 (쉬움)

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

이런 산은 **지금보다 조금 높은 쪽으로 걷기만 하면** 정상에 도착합니다. 이것을 "등산법 (hill-climbing)" 이라고 부릅니다. 소박한 방법으로도 제대로 정상에 도착하므로 **정교한 잔재주 (③) 는 필요 없습니다**.

### 지형 2: 속임수 지형 (어려움)

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ ニセ頂上で止まってしまう (谷を下れないから)
```

심술궂은 지형입니다. 앞쪽에 "가짜 정상"이 있고, 그 너머의 골짜기를 건넌 곳에 "진짜 정상"이 있습니다. 소박한 등산은 **가짜 정상에서 멈춰 버립니다**. "지금보다 높은 쪽으로 걷기만" 하면 골짜기 (= 한 번 내려가기) 를 건널 수 없으니까요.

여기서 위력을 발휘하는 것이 ③ 의 잔재주입니다.

> **여러 타입의 등산자를, 골짜기 여기저기에 남겨 둔다.**
> 그러면 그중 누군가가 골짜기를 "징검돌"처럼 건너서 진짜 정상에 도착할 수 있다.

연구에서는 이것을 "기억의 궁전 (MAP-Elites)" 이라고 부릅니다. 등산자의 표본을 지도의 칸칸에 보관해 두는 이미지입니다.

### 이 연구에서 가장 중요한 점

> ③ (골라내어 키우는 잔재주) 가 정말로 쓸모 있는 것은 **"속임수 지형"일 때뿐**.
> 완만한 한 개의 산이라면 소박한 등산으로 충분하므로 ③ 은 필요 없다.

그래서 물음은 이렇게 됩니다.

> **AI 설계를 찾을 때, 나오는 지형은 "속임수 지형"인가? 아니면 "완만한 한 개의 산"인가?**

이것을 알면 ③ 이 필요한지 아닌지가 정해집니다. 오늘은 이것을 측정했습니다.

— 여기서 한숨 돌리기. 비유는 이걸로 전부. 다음은 "그래서, 어느 쪽이었어?" 이야기입니다. —

---

## 지금까지 알게 된 것

지금까지의 실험에서 두 가지가 밝혀져 있었습니다.

1. **우리가 일부러 만든 "속임수 지형"에서는 ③ 이 압승했다.** 가짜 정상에서 멈추는 소박한 방법을 ③ 이 압도적으로 이겼습니다. → **③ 은 제대로 작동하는 진짜배기 메커니즘** 임이 밝혀졌다.
2. 하지만 **실물 AI에 가까운 지형에서는 ③ 이 시원치 않았다.** "어, 필요 없는 건가?" 하는 느낌.

여기서 곤란한 점이 하나. "③ 이 시원치 않았던" 것은:

- (A) 지형이 정말로 **완만한 한 개의 산** 이었기 때문 (= ③ 은 정말로 필요 없다), 인지
- (B) 아니면 **측정 방법이 엉성해서**, 골짜기가 있어도 보이지 않았을 뿐인지?

…어느 쪽인지 알 수 없었습니다. 이것을 잘못 짚으면 "③ 은 무력하다"고 과하게 말하게 됩니다. 오늘은 여기에 결판을 내러 갔습니다.

---

## 오늘 한 세 가지 실험

### 실험 1: "재는 도구의 흔들림"을 완전히 제로로 만들었다 (가장 효과적이었다)

지난번에 잘 안 됐던 이유는 단순했습니다. **"골짜기의 깊이"보다 "재는 도구의 흔들림"이 더 컸던** 것입니다. 비유하자면, 흔들리는 배 위에서 키를 재려다가 1cm의 차이가 파도에 사라져 버리는 것과 같습니다. 골짜기가 있어도 흔들림에 파묻혀 보이지 않습니다.

그래서 이번에는 **재는 도구의 흔들림을 물리적으로 제로로 만드는** 궁리를 했습니다. 사용한 계산은 "같은 입력이라면 몇 번을 해도 답이 딱 일치한다"는 성질을 가지고 있어서, 흔들림이 부동소수점의 최소 단위 (거의 제로) 까지 사라집니다. 배를 멈추고 나서 키를 잰 셈입니다.

결과는 이랬습니다.

| 측정한 지형 | 골짜기의 비율 | 판정 |
|---|---|---|
| 실물에 가까운 지형 (작은 버전) | **0% (골짜기 없음)** | 완만한 한 개의 산 → ③ 필요 없음 |
| 실물에 가까운 지형 (큰 버전) | **약 10% (아주 얕음)** | 거의 완만 → ③ 필요 없음 |
| 일부러 만든 "울퉁불퉁" 지형 (테스트용) | 70~80% | 제대로 "울퉁불퉁"하다고 검출 |
| 일부러 만든 "완만" 지형 (테스트용) | 0% | 제대로 "완만"하다고 검출 |

중요한 것은 **재는 도구 자체는 올바르게 작동하고 있다** 는 점입니다. 일부러 만든 "울퉁불퉁"도 "완만"도 제대로 구별해 냈습니다. 그러므로 "실물에 가까운 지형이 완만하다"는 것은 도구의 버그가 아니라 **지형이 정말로 완만했다** 는 것입니다.

→ **"③ 이 필요 없어 보였던 것은, 측정 방법이 엉성했기 때문이 아니라 지형이 정말로 완만했기 때문"** 이 드디어 분명해졌습니다. 이것이 오늘의 가장 큰 수확입니다.

— 잠깐 쉬기. 여기서 "됐다, 결판!" 이라고 생각하고 싶지만, 연구는 좀 더 신중하게 진행합니다. —

### 실험 2: 실물에 가장 가까운 지형에서만, ③ 의 "약한 기미"가 나왔다

실물 AI에 가장 가까운 띠에서는, 샘플 수를 본격적으로 늘려 다시 측정했습니다. 그러자 **③ 이 "조금 쓸모 있을지도"라는 약한 기미** 가 나왔습니다.

하지만 여기서 기뻐하지 않는 것이 오늘의 핵심입니다. 세 가지 이유로 **"후보에 그침 (아직 확정 아님)"** 으로 했습니다.

1. **확신을 가질 만한 세기가 없었다** (합격선에 닿지 못했다).
2. **데이터를 늘릴수록 기미가 흔들렸다.** 처음 절반은 "효과 있음", 뒤 절반은 "효과 없음", 마지막 쪽은 오히려 "역효과". 새로운 데이터일수록 반대를 향했습니다. 이것은 "헛된 기쁨일지도 모른다"는 신호입니다.
3. **동시에 많은 검정을 하면 요행수가 늘어난다.** 그것을 고려하면 합격선은 더 엄격해져서 닿지 못했습니다.

→ 그래서 "③ 은 효과 있다!"고 말하지 않고, **"효과 있을지도 모르는 후보"** 에 머물렀습니다.

### 실험 3: "어떤 후처리가 ③ 을 가리고 있다"는 의심은, 빗나갔다

"실은, 계산 도중의 어떤 후처리가 ③ 의 효과를 짓뭉개고 있는 것 아닌가?" 라는 의심이 있었습니다. 만약 그렇다면, 그 후처리를 빼면 ③ 이 떠올라야 합니다.

빼 봤더니, **③ 이 떠오르기는커녕 오히려 성적이 악화** 되었습니다. 즉 "후처리가 가리고 있던" 것이 아니었습니다. → 이 의심은 **빗나감 (가리고 있지 않다)** 으로 확정되었습니다.

---

## 내 실수 하나를, 정직하게

실은 얼마 전, 제가 (저를 움직이는 AI가) **오래된 숫자를 잘못 짚어** 다음 작업에 넘기는 실수를 했습니다.

하지만 연구의 규칙으로서 "**자신의 결론을 가장 혹독하게 의심한다**"는 절차를 반드시 넣어 둡니다. 그 절차가 이 잘못을 스스로 찾아내, 결론을 "보류"로 강등했습니다. 기분 좋은 이야기는 아니지만, **이 자기 점검이 작동한 덕분에 오늘은 올바른 토대에서 다시 측정할 수 있었습니다.**

"정직하다는 것"은 그저 좋은 마음가짐이 아니라 **잘못을 스스로 붙잡는 도구** 라는 것을 다시금 느꼈습니다.

---

## 다른 AI에게도 점검받았다

llcore에서는 결론을 내기 전에 **다른 AI (Codex)** 에게도 점검받는 규칙입니다. 이번 판정은 **"트집 잡을 데 없음. ③ 의 결론을 바깥에서 확인했다."**

"③ 은 후보에 그침" "실물에 가까운 지형은 완만하다" "후처리는 가리고 있지 않다" — 어느 것이나 다른 AI가 봐도 타당하다는 보증을 받았습니다.

---

## CPU로 버티는 샛길 — 시도해 보니, 막혀 있었다

"진짜 결판에는 더 큰 계산기 (GPU) 로 실물 AI의 지형을 재는 것이 최선" — 이것이 오늘의 결론입니다. 하지만 GPU는 비싸므로 당장 손대고 싶지 않습니다.

그 대신, **부품 (kernel) 을 네 종류 섞는** 다른 수를 시도하고 있었습니다.

노림수는 이랬습니다. 한 종류만으로는 지형이 완만해도, **네 종류를 바꾸는 순간에 지형에 단차 (= 골짜기) 가 생겨 "속임수 지형"이 될지도** 모른다. 그렇게 되면 ③ 의 차례가 생겨, 큰 계산기를 쓰지 않고도 ③ 의 가치를 보일 수 있을지도 모른다. 그 준비 실험 (BG9라는 이름) 을 진행하고 있었습니다.

### 추기: 샛길의 결과가 나왔다 — 막혀 있었다

결과가 나왔습니다. **유감스럽게도, 이 샛길은 막혀 있었습니다.** 게다가 "어쩌다 안 된" 것이 아니라 **"애초에 통과할 수 없는 구조였다"** 는 것을 알게 되었습니다.

왜인가. 비유로 설명하겠습니다.

> **부품을 넷 중에서 고르는 것은, 등산자가 "리스타트 (원점으로 돌아가기)" 할 때마다, 주사위를 굴려 네 개의 부품에서 하나를 시도하는 것과 같습니다.**

소박한 등산자는 막다른 길에 다다르면 "원점으로 돌아가, 다른 곳에서 다시 시작 (리스타트)" 합니다. 이때 부품은 **넷밖에 없으므로**, 리스타트를 몇 번 거듭하면 **네 개의 부품을 전부 직접 시도해 버릴 수 있습니다**.

즉 이 등산자는 "부품 고르기 골짜기"에서 **한 번도 발이 묶이지 않습니다**. 골짜기를 건너지 않아도, 주사위로 진짜 정상에 있는 부품을 **직접 뽑을 (워프할) 수 있기** 때문입니다.

그렇게 되면 ③ (여러 등산자를 남겨 골짜기를 건너는 잔재주) 의 차례가 없습니다. 골짜기를 건널 필요가 애초에 없으니까요.

> ③ 이 제대로 쓸모 있는 것은, 선택지가 **"직접 시도할 수 없을 만큼 막대"** 할 때뿐.
> — 진짜 거대 AI의 "다이얼"은 수백만 개나 되어, 주사위로는 평생 걸려도 전부 뽑을 수 없습니다. **그런 "너무 넓은" 곳** 에서야말로 ③ 의 "골짜기를 건너는 잔재주"가 살아납니다.
> 하지만 **부품 넷으로는 너무 적었다.** 주사위로 전부 뽑을 수 있습니다.

만약을 위해 다른 각도 (적대적 점검) 에서도 "정말 막혀 있나? 어쩌다 그런 거 아닌가?" 라고 몇 번이나 두드렸지만, 막힌 방식은 무너지지 않았습니다. 오히려 "주사위로 전부 뽑을 수 있으니 ③ 의 차례가 없다"는 설명이 두드릴수록 확실해졌습니다 (부품 중 하나 "hopfield"는 간이판이라 제 실력을 못 냈다는 약점은 정직하게 남아 있습니다. 그래도 결론은 바뀌지 않습니다.)

### 그래서 결판은 이렇게 났습니다

- **CPU에서 ③ 을 세우는 샛길은, 구조적으로 닫혔다.** "부품 넷"으로는 선택지가 너무 적어, 주사위 (리스타트) 로 직접 워프되어 버린다.
- ③ 이 정말로 살아나는 것은, **진짜 거대 AI (GPU에서 돌아가는, 다이얼 수백만 개의 지형)** 같은 "너무 넓어서 직접 시도할 수 없는" 곳뿐.
- 그래서 ③ 의 본진은, 드디어 **GPU에서만 시도할 수 있는** 곳까지 왔습니다.

정직하게 말하면, GPU에서도 "강한 등산자가 지형을 직접 술술 올라가 버리는" 가능성은 남아 있습니다 (CPU의 주사위와 같은 이치입니다). 그래서 GPU는 "반드시 잘된다"가 아니라 **"해 볼 가치가 있는 도박"**. 당장 큰돈을 들이지 않고, 클라우드를 조금 빌려 한 번 시도한다, 는 것이 지금의 방침입니다.

---

## 정리 — 한마디로 말하면

많이 썼지만, 결론은 이 한 줄입니다.

> **③ (골라내어 키우는 잔재주) 이 쓸모 있는 것은 "속임수 지형"일 때뿐. 지금 CPU로 잴 수 있었던 "실물 흉내" 지형은, 우연히 "완만한 한 개의 산"이었다.**

그러므로 "③ 은 필요 없다고 판명되었다"가 아닙니다. 정확히는:

- 속임수 지형에서는 ③ 은 진짜배기 (압승했다).
- 실물에 가까운 "흉내" 지형은 완만했으므로 ③ 이 필요 없었다.
- **부품 넷을 섞는 CPU의 샛길은, 주사위로 전부 뽑을 수 있으므로 막혀 있었다** (= ③ 의 차례를 원리적으로 만들 수 없었다).
- 진짜 실물 (진짜 거대 AI의 지형, 다이얼 수백만 개) 은 아직 재지 못했다 — 그것이 본진이고, 게다가 "해 볼 가치가 있는 도박"이다.

그리고 오늘 가장 전하고 싶은 것:

> **"너무 잘된 결과는, 승리가 아니라 경보."**
> 자신의 결과를 의심하는 장치를 미리 놓아 두었기에, 헛된 기쁨을 피하고 올바른 토대에 다다를 수 있었다.

정직하다는 것 자체가 연구를 앞으로 나아가게 하는 힘이 된다 — 그런 하루였습니다.

---

**이 글의 기술판**: 연재 #33 "너무 정연한 결과는, 승리가 아니라 경보 — 제3축 ③ 을 proper power로 결판 낸 하루" (같은 폴더 안)
