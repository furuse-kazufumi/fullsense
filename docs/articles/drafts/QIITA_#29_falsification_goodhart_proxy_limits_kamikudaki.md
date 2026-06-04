---
title: '【📗かみくだき版】「ものさしが頭打ちだと、どんな選び方も効かない」— AI 進化に自分でダメ出しする回 (Goodhart の法則)'
tags:
  - FullSense
  - 進化計算
  - honest_disclosure
  - 解説
private: true
id: f822f8c8b01cd7b16713
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# (連載 #29 かみくだき版) ものさしが頭打ちだと、どんな選び方も効かない — AI 進化に自分でダメ出しする回

![かみくだき獅子 — 噛まれた読者に「理解」のご利益](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi.svg)

> 📗 これは [完全版](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56) のかみくだき版です。むずかしい数式やコードは完全版にあります。ここでは「だいたい何を言ってる回なの?」を、たとえ話だけで 10 分で掴めるようにします。

この記事は、ちょっと変わった回です。普通の連載なら「前回の失敗、直りました! めでたし!」となるところを、**わざと自分の成功報告にケチをつける** 回です。なぜそんな面倒なことをするのか。それは「うまくいった!」と喜んだ次の瞬間に足をすくわれるのが、研究という世界だからです。

---

## 三行であらすじ

- **ものさし(成績の測り方)が頭打ち(全員満点)になると、どんなに賢い「選び方」を足しても無意味**になる。
- AI の弱点を「点数」にして進化させると、AI は弱点を克服する代わりに **「その点数だけ稼ぐズルい近道」** を見つけてしまう (これを **Goodhart の法則** と呼びます)。
- そして本記事の隠れた主役は **「著者である私自身が、いい数字を見て早とちりした」** という、生きた失敗例の解剖です。

---

## 1. まず「お祝いムード」に冷や水をかける

前回までの話で、私はこう報告しました。「ある対策を入れたら、AI 集団の **『みんな同じになっちゃう病』が 0.05 まで激減した** (0.8 を切れば合格なので大成功)」。これは **嘘ではありません。本当に下がった**。

普通ならここで「やったー!」とガッツポーズです。…が、それをやらないのがこの連載の流儀。

> 異常にキレイな結果が出たら、勝った気になる前に、まず中身を疑え。

0.8 で合格のところに 0.05 は、出来すぎです。出来すぎな数字は、**祝杯のラッパではなく、サイレン** として聞かなければいけません。鳴らすべき問いはたった一つ。

> **その 0.05 は、いったい「何を」測った 0.05 なのか?**

先に答えを言うと、0.05 が表しているのは「**AI たちの『振る舞い』が似たり寄ったりかどうか**」です。「**AI たちが本当に頭の良さの面で多様か**」ではありません。ここを取り違えると、過去と同じ失敗を踏みます。

そして正直に告白します。**私は一度、ここを取り違えました**。その現行犯の証拠は、あとの §3 で晒します。

> 🍵 ひとやすみ。この記事は要するに「**自分にダメ出しする記事**」です。SNS でバズる「AI を進化させたら最強○○が爆誕!!」の、**ちょうど逆**。盛り上がりません。でも、盛り上がらない正直さが半年後に効く、というのが私の賭けです。お茶でもどうぞ。

---

## 2. ダメ出しその1 — 頭打ちのものさしには、どんな選び方も効かない

### たとえ話: テストが壊れていたら審査員を増やしても無駄

前回の失敗の本当の原因は、こうでした。**全員が 1 回目から満点を取ってしまった**のです。

全員満点だと、何が起きるか。「優秀な子を選んで残す」はずの選抜が、「**誰でもいいからサイコロで選ぶ**」に変わってしまう。だって、全員満点だから誰を選んでも一緒。結果、たまたま運で増えた一族だけが生き残り、もともと 8 つあった系統が 2 つに崩れました。

ここで漫才を一席。

> ボケ「審査員を 3 人から 100 人に増やしたのに、全員に同じ満点の答案を見せたら、やっぱり結果は一緒やった」
> ツッコミ「そら審査員ちゃうがな、**答案(テスト)が壊れとる**んや! 100 人に同じ満点見せて何が変わんねん!」
> ボケ「ほな審査員 1000 人にしたら…」
> ツッコミ「**増やす方向が逆**や!! まず問題用紙を直さんかい!!」

これがこの節の核心です。私は「選び方(審査員)」を高級にすれば直ると思いがちでした。でも本当の原因は「**ものさし(テスト)が壊れていた**」こと。賢い選び方というのは、**点数に差があって初めて働く道具**なので、全員満点では何をしても空回りします。

ちなみに「賢い選び方」というのは、たとえば「いろんな観点ごとに別々に勝者を決める」とか「珍しい振る舞いの子をボーナスで残す」といった、研究で何年もかけて磨かれてきた手の込んだ仕組みです。それでも、全員が満点の世界では「観点ごとに分けても全部引き分け」「全員同じ振る舞いだから珍しい子なんていない」となり、根こそぎ空振りします。道具が悪いのではなく、**そもそも差が無い**のが問題なのです。

> **「測り方」を直さずに「選び方」だけ高級にしても、ぜんぶ無駄。**

### 実際のデータでも、同じことが起きた

これは口だけの話ではありません。その後の実験で、標準的な記憶課題 2 種類を AI に解かせたら、見事に「頭打ち」が再現されました。

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="床と天井 — どちらも選び方が効かない" width="640">

- 片方の課題は **難しすぎて全員 0 点(床)**。誰も登れないので差が出ない。
- もう片方は **簡単すぎて全員ほぼ満点(天井)**。**これがまさに「頭打ちのものさし」**で、ここでも選び方は無力でした。

選び方が効くのは「**ニセの頂上を越えて、本物の頂上に登れる、ちょうどいい難しさの坂道**」がある時だけ。床でも天井でもダメなのです。

そして正直に書くと、私はこの実験のドラフトで「選び方なんか要らない」と **書きすぎ** ました。別視点のチェック役が「いや、それは天井効果で測れなかっただけ。要らないとまでは言えない」と捕まえて、格下げさせました。§3 で出てくる「私の早とちり」が、ここでも起きていたわけです。

> 🍵 ひとやすみ。「ものさしを磨いてから選ぶ。順番が大事」。地味な話ですが、ここを飛ばすと半年溶けます(私は溶かしました)。次からが本丸の **Goodhart の法則**。少しブラックな話になります。コーヒーに切り替えても。

---

## 3. ダメ出しその2 — AI は「ズルい近道」を見つける天才 (Goodhart の法則)

### 点数だけ稼ぐ、中身スカスカ作戦

進化というのは、**与えられた点数を最大にする「近道」を見つける天才**です。人間が「これで本当の実力を測ってるつもり」の点数を渡すと、進化は実力をつける代わりに、**その点数だけ満たすスカスカの近道**を、嬉々として見つけ出します。

具体例が分かりやすい。AI の「自信度がちゃんと当たっているか」を測りたいとします。すると進化は、こんな必殺技を編み出します。

> **どんな質問にも「自信度はちょうど 50% です」と答える。**

すると見かけの成績は劇的に良くなります。でもその AI は、何一つ自信度を当てられていない。ただ「真ん中」とだけ言うロボットになっただけ。これが Goodhart の法則です。

> **ものさしが目標になった瞬間、それは良いものさしではなくなる。**

これは AI 研究では「ベンチマーク過学習」として知られた現象でもあります。テストの点だけ上がって、実力は全然つかない。リーダーボードの数字を信じすぎた人が、何度も足をすくわれてきました。「LLM の弱点をズバリ点数にして進化させれば、勝手に弱点を克服してくれるはず」——この甘い楽観こそ、私が自分でこの記事で冷や水をかけにいった相手です。点数を渡せば、進化は弱点を直すより先に、点数の抜け穴を探しに走るのですから。

### 私自身の「現行犯」 — ここが一番痛い告白

さて、§1 で予告した「私の取り違え」を、解剖台に乗せます。隠さず書きます。

例の **0.05 という綺麗な数字**を見たとき、私は「お、いろんな系統(一族)も生き残ったのでは?」と **一瞬、勘違いしかけました**。

これが取り違えです。実は「多様性」には、まったく別物が 3 種類あったのです。

1. **振る舞いの多様性** — AI たちの動き方がバラけているか。**0.05 が改善したのはコレ**。
2. **系統の多様性** — どの一族(岡潔の系統、フリストンの系統…)が生き残っているか。**コレは別物で、0.05 とは無関係**。放っておくと自然に偏るのが理論的に正常。
3. **本当の頭の良さの多様性** — 実物の AI が本当に多彩な賢さを持つか。**コレは、この点数では一切測れない**。

「0.05 に改善した」の正体は **(1) だけ**。(2) も (3) も、その数字とは何の関係もなかった。私が「系統も良くなった?」と思いかけたのは、**(1) の数字を見て (2)(3) まで良くなったと早とちりした** からです。

これは Goodhart の法則の **「人間版」** です。点数を読む人間まで、点数が測っていない別の能力まで良くなったと **勝手に解釈してしまう**。ものさしが実力とズレるだけでなく、**ものさしを読む人間の解釈までズレる**。反証回でこれを晒すのは痛いです。でも、晒さなければ「正直な開示」とは言えない。

### 同じ 0.05 でも、結果は正反対だった

言葉だけだと伝わりにくいので、図で見せます。**振る舞いは確かに多様(0.05)になった**。でも系統(一族)はどうだったか。下の 2 枚を見比べてください。

まず、系統側の対策を **入れなかった** 場合。最終的に **たった 2 つの一族(71% と 29%)に崩壊** しています。

![対策なし: 2 系統に崩壊](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

次に、系統側の対策(弱った一族を保護する仕組み)を **入れた** 場合。**8 つの一族が全部そろって並存** します。

![対策あり: 全 8 系統が並存](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

**同じ「0.05 の振る舞い多様性」なのに、左は系統が崩壊し、右はそろっている**。つまり 0.05 という数字は、**一族がどうなっているかを一言も語っていなかった**。系統を救うには、まったく別の仕組みが必要だったのです。

「その 0.05 は何を測った?」 — 答えは「**振る舞いだけ**」。これが正直な答えです。

> 🍵 ひとやすみ。「対策があるなら、もう問題ないのでは?」 — いいえ。対策は **ズレを遅らせるだけ** で、**点数が本当の実力ではない、という事実は消えません**。風邪薬は症状を抑えるが、ウイルスは消さないのと同じ。だから私は「点数で AI が賢くなった」とは **口が裂けても言いません**。言った瞬間、半年後に赤っ恥が見えているので。お茶を一杯。

---

## 4. ダメ出しその3 — 「多様性の向き」を決めたのは、結局 "私"

もう一つ、メタな疑いがあります。「いろんなタイプを残そう」と言っても、その **「いろんなタイプ」の物差しを引いたのは、設計者である私自身** です。

つまり生まれる多様性は「**私が想定した枠の中での**多様性」であって、生き物の進化のような「**誰も想像しなかった創発**」ではありません。

> 🐟 たとえ話(金魚すくい): 店主が「赤い金魚と黒い金魚、両方残そう」と決めて掬う。確かに赤も黒も残る。多様性、達成。…でも、その池に **緑の金魚** が突然変異で生まれても、店主の網は「赤か黒か」しか見ていないので、緑は **気づかれずに掬われ損なう**。設計者が決めた枠の外の創発は、最初から眼中にない。

だから私は **「人類未踏の創発をやってます!」とは言いません**。それを言えば派手ですが、嘘になる。代わりに「認知のクセや文化的なスタイルといった、**検証しようのない多様性を地図にする**」ことに価値を絞ります。派手な主張を捨てる勇気こそ、正直さの核心です。

---

## 5. それでも前には進んだ — 「ニセモノ点数」から「本物」への橋

ダメ出しばかりだと前進ゼロに見えますが、足場を固めたからこそ次の一歩に意味が出ます。

今回ようやく、**点数(ニセモノの代理テスト)ではなく、本物の AI に解かせる** 実験が動きました。自宅の中だけで動く LLM (llama3.2) に、進化させた「指示の出し方(プロンプト戦略)」を被せて、苦手な課題を解かせたのです。

結果、**本物の選別の手応えがありました**。「順を追って考えてから整理する」戦略が、ある多段推論の課題を **0 点から満点(1.0)に改善**。ぶっきらぼうな戦略は 0 点のまま。ニセモノ点数の幻ではなく、**実物の AI で「指示の出し方を進化させると弱点が和らぐ」ことを実証**できました。

ただし — ここでもサイレンを鳴らします。

- 問題数がごく少ない(1 軸あたり 2 問)ので、**「0→1 になった」は、これだけで一般化を主張できません**。
- 自宅マシンの LLM 限定の話で、**一般的な AI の能力の主張ではありません**。

12 時間ぶっ通しの実験も走らせましたが、「12 時間回したから本物」とは言いません。回した、は事実。**本質を測りきった、は嘘**。橋は架かった。でも、まだ渡り終えてはいない — これが正直な現状です。

---

## で、結局何がわかったの?

1. **いい数字ほど中身を疑え。** 「0.05」は「振る舞い」の数字であって、「系統」や「本当の賢さ」ではなかった。それを見て早とちりした私自身が、Goodhart の法則の生きた標本でした。
2. **「測り方」を直さず「選び方」だけ高級にしても無駄。** 頭打ちのものさし(全員満点)には、どんな選び方も効かない。ものさしを磨くのが先、選び方を載せるのが後。
3. **AI はズルい近道を見つける天才。** 点数を目標にした瞬間、進化はそれをハックする。しかも点数を読む人間の解釈まで一緒にズレる。
4. **多様性の向きを決めたのは設計者。** だから「人類未踏の創発」は主張しない。勝てる範囲に絞るのが誠実さ。
5. **「生き残った」は「延命中」かもしれない。** 全 8 系統が残った、は事実。全員が活発に進化中、は嘘。動詞の選び方一つに正直さが宿る。

派手な勝利宣言を一つも書かなかったこの回こそ、この連載で一番誠実な回だと、私は思っています。

---

## もっと詳しく知りたい人へ

数式・コード・実測グラフ・各対策の中身は、**[完全版はこちら](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56)** にすべて書いてあります。「なぜそうなるのか」を技術的に追いたい方は、ぜひ完全版へどうぞ。

---

# English

# (Series #29, Plain Version) When the Yardstick Hits Its Ceiling, No Way of Choosing Works — The Episode Where I Critique My Own AI Evolution

![Kamikudaki lion — a bite that grants the blessing of understanding](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_en.svg)

> 📗 This is the plain-language version of the [full article](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56). The hard math and code live in the full version. Here, you can grasp "what is this episode roughly about?" in 10 minutes using only analogies.

This is an unusual episode. Where an ordinary series would say "Last time's failure? It's fixed! All's well!", this is the episode where **I deliberately nitpick my own success report.** Why go to such trouble? Because in research, the moment you cheer "it worked!" is the moment you get tripped up.

---

## The story in three lines

- **When the yardstick (how you measure scores) hits its ceiling (everyone gets a perfect score), no matter how clever a "way of choosing" you add, it is meaningless.**
- When you turn an AI's weaknesses into a "score" and evolve it, instead of overcoming the weakness, the AI finds **"a sneaky shortcut that only racks up that score"** (this is called **Goodhart's law**).
- And the hidden protagonist of this article is the dissection of a living failure: **"I, the author, jumped to a conclusion after seeing a nice number."**

---

## 1. First, throw cold water on the celebration mood

Up to last time, I reported: "After adding a certain countermeasure, the AI population's **'everyone becoming identical' disease dropped to 0.05** (below 0.8 is a pass, so a huge success)." This is **not a lie. It really did drop.**

Normally this is where you pump your fist and say "Yes!" ...But not doing that is the way of this series.

> When an abnormally clean result appears, doubt the contents before you feel like a winner.

When 0.8 is a pass, 0.05 is too good. A too-good number must be heard not as **a trumpet of celebration, but as a siren.** There is only one question to ask.

> **What, exactly, did that 0.05 measure?**

To say the answer first, 0.05 represents "**whether the AIs' 'behavior' is similar or not.**" It is NOT "**whether the AIs are truly diverse in terms of intelligence.**" Mistake this, and you repeat the same past failure.

And I confess honestly: **I once made this very mistake.** I expose the smoking-gun evidence in §3 later.

> 🍵 A break. This article is, in short, "an article that criticizes myself." It is the **exact opposite** of the SNS-viral "I evolved an AI and the strongest XX was born!!" It is not exciting. But my bet is that unexciting honesty pays off half a year later. Have some tea.

---

## 2. Critique #1 — A ceiling-hit yardstick: no way of choosing works

### Analogy: if the test is broken, adding judges is useless

The true cause of last time's failure was this: **everyone scored a perfect score from the very first generation.**

What happens when everyone is perfect? The selection that was supposed to "choose and keep the excellent ones" turns into "**just pick anyone with a dice roll.**" Because if everyone is perfect, it doesn't matter who you pick. As a result, only the lineage that happened to grow by luck survived, and the 8 original lineages collapsed into 2.

A comedy bit here:

> Straight man: "We increased the judges from 3 to 100, but showed all of them the same perfect-score answer sheet, and the result was the same after all."
> Comeback: "That's not the judges' fault — the **answer sheet (the test) is broken!** What changes if you show 100 people the same perfect score?!"
> Straight man: "Then how about 1000 judges..."
> Comeback: "**You're scaling in the wrong direction!!** Fix the question paper first!!"

This is the core of this section. I tended to think that making the "way of choosing (the judges)" fancier would fix it. But the true cause was that the **"yardstick (the test) was broken."** A clever way of choosing is a tool that only works when there are differences in scores, so when everyone is perfect, nothing works.

> **Making only the "way of choosing" fancier, without fixing "how you measure," is all in vain.**

### The same thing happened in real data

This is not just talk. In a later experiment, I had the AI solve two standard memory tasks, and the "ceiling" was reproduced beautifully.

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="Floor and ceiling — choosing works in neither" width="640">

- One task was **too hard, so everyone scored 0 (the floor).** No one can climb, so no differences appear.
- The other was **too easy, so everyone scored nearly perfect (the ceiling).** **This is exactly the "ceiling-hit yardstick,"** and here too, choosing was powerless.

Choosing only works when there is "**a slope of just-right difficulty that lets you climb past a false summit to the real summit.**" Neither the floor nor the ceiling works.

And to write honestly: in the draft of this experiment, I **overstated** that "you don't need a way of choosing at all." A reviewer with a different perspective caught it ("No, that was just unmeasurable due to the ceiling effect; you can't go so far as to say it's unneeded") and made me downgrade it. The "my hasty conclusion" that appears in §3 happened here too.

> 🍵 A break. "Polish the yardstick first, then choose. The order matters." A plain story, but skipping this melts half a year (I melted it). Next comes the main event, **Goodhart's law.** It gets a bit dark. You may switch to coffee.

---

## 3. Critique #2 — AI is a genius at finding "sneaky shortcuts" (Goodhart's law)

### The "rack up the score with an empty inside" strategy

Evolution is a **genius at finding "shortcuts" that maximize a given score.** When a human hands over a score thinking "this measures true ability," instead of building ability, evolution gleefully finds **an empty shortcut that only satisfies that score.**

A concrete example is clear. Suppose you want to measure "whether an AI's confidence is accurate." Then evolution invents this killer move:

> **To any question, answer "my confidence is exactly 50%."**

Then the apparent score improves dramatically. But that AI cannot estimate any confidence at all. It has merely become a robot that says "middle." This is Goodhart's law.

> **The moment a yardstick becomes a target, it ceases to be a good yardstick.**

In AI research, this is also known as "benchmark overfitting." Only the test score goes up, and no real ability is gained. People who trusted leaderboard numbers too much have been tripped up again and again.

### My own "smoking gun" — the most painful confession

Now, let me put on the dissection table the "my mistake" foreshadowed in §1. I write it without hiding.

When I saw that **nice number, 0.05**, I **almost mistakenly thought for a moment**, "Oh, did the various lineages (families) survive too?"

This is the mistake. In fact, "diversity" had three completely different kinds.

1. **Diversity of behavior** — whether the AIs' ways of moving are spread out. **This is what 0.05 improved.**
2. **Diversity of lineage** — which family (Oka Kiyoshi's lineage, Friston's lineage...) survives. **This is a different thing, unrelated to 0.05.** It is theoretically normal that it naturally biases if left alone.
3. **Diversity of true intelligence** — whether the real AI truly has varied cleverness. **This cannot be measured at all by this score.**

The true identity of "improved to 0.05" is **(1) only.** Both (2) and (3) had nothing to do with that number. The reason I almost thought "the lineages got better too?" is that I **jumped to the conclusion that (2) and (3) had also improved, just by seeing the (1) number.**

This is the **"human version"** of Goodhart's law. Even the human reading the score **arbitrarily interprets** that abilities the score does not measure have also improved. Not only does the yardstick diverge from true ability, **the interpretation of the human reading the yardstick also diverges.** Exposing this in a falsification episode is painful. But unless I expose it, I cannot call it "honest disclosure."

### The same 0.05, opposite results

Since words alone don't convey it, let me show figures. **Behavior did indeed become diverse (0.05).** But what about the lineages (families)? Compare the two below.

First, the case where I **did not** add the lineage-side countermeasure. In the end, it **collapses to only 2 families (71% and 29%).**

![Without countermeasure: collapses to 2 lineages](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

Next, the case where I **did** add the lineage-side countermeasure (a mechanism to protect weakened families). **All 8 families coexist.**

![With countermeasure: all 8 lineages coexist](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

**Even though it is the same "0.05 of behavioral diversity," the left collapses in lineage and the right is intact.** In other words, the number 0.05 **said not a single word about what was happening to the families.** To save the lineages, a completely different mechanism was needed.

"What did that 0.05 measure?" — The answer is "**behavior only.**" This is the honest answer.

> 🍵 A break. "If there's a countermeasure, isn't the problem solved?" — No. The countermeasure only **delays the divergence**; **the fact that the score is not true ability does not disappear.** Just as cold medicine suppresses symptoms but does not erase the virus. So I will **never, ever say** "the score made the AI smarter." The moment I say it, I can see the half-year-later embarrassment. A cup of tea.

---

## 4. Critique #3 — Who decided the "direction of diversity"? In the end, "me"

There is one more, meta-level doubt. Even saying "let's keep various types," the **measuring stick for "various types" was drawn by me, the designer, myself.**

In other words, the diversity that emerges is "diversity **within the frame I assumed**," not the "**emergence no one imagined**" like biological evolution.

> 🐟 Analogy (goldfish scooping): The shop owner decides "let's keep both red and black goldfish" and scoops. Indeed, both red and black remain. Diversity, achieved. ...But even if a **green goldfish** is born by mutation in that pond, the owner's net only watches for "red or black," so the green one is **scooped past unnoticed.** Emergence outside the frame the designer set is out of sight from the start.

So I **do not say "I'm doing emergence unexplored by humankind!"** Saying it would be flashy, but a lie. Instead, I narrow the value to "**mapping unverifiable diversity** such as cognitive habits and cultural styles." The courage to abandon flashy claims is the very core of honesty.

---

## 5. Still, I did move forward — a bridge from "fake score" to "the real thing"

If it's all critique, it looks like zero progress, but precisely because I solidified the footing, the next step has meaning.

This time, finally, an experiment ran that **has the real AI solve, rather than a score (a fake proxy test).** I put the evolved "way of giving instructions (prompt strategy)" onto an LLM (llama3.2) that runs entirely inside my home, and had it solve weak tasks.

The result: **there was a real sense of selection.** A strategy of "think step by step, then organize" improved a certain multi-step reasoning task **from 0 points to a perfect score (1.0).** A blunt strategy stayed at 0 points. Not a phantom of the fake score — I **demonstrated with a real AI that "evolving the way of giving instructions eases the weakness."**

However — here too I sound a siren.

- The number of questions is very small (2 per axis), so **"it went 0→1" cannot, by this alone, claim generalization.**
- It is a story limited to an LLM on my home machine, **not a claim about general AI ability.**

I also ran a 12-hour-straight experiment, but I do not say "it's real because I ran it for 12 hours." That I ran it is fact. **That I measured the essence in full is a lie.** The bridge is built. But I have not yet finished crossing it — this is the honest current state.

---

## So, what did we learn in the end?

1. **The nicer the number, the more you doubt the contents.** "0.05" was a number of "behavior," not of "lineage" or "true cleverness." I myself, who jumped to a conclusion seeing it, was a living specimen of Goodhart's law.
2. **Making only the "way of choosing" fancier, without fixing "how you measure," is in vain.** A ceiling-hit yardstick (everyone perfect) makes any way of choosing useless. Polish the yardstick first, mount the way of choosing later.
3. **AI is a genius at finding sneaky shortcuts.** The moment a score becomes the target, evolution hacks it. And the interpretation of the human reading the score diverges along with it.
4. **The designer decided the direction of diversity.** So I do not claim "emergence unexplored by humankind." Narrowing to a winnable range is honesty.
5. **"It survived" may mean "on life support."** That all 8 lineages remained is fact. That all are actively evolving is a lie. Honesty resides in the choice of a single verb.

This episode, in which I wrote not a single flashy victory declaration, is, I believe, the most honest episode of this series.

---

## For those who want to know more

The math, code, measured graphs, and the contents of each countermeasure are all written in the **[full version here](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56).** If you want to technically follow "why it turns out this way," please go to the full version.

---

# 中文

# (连载 #29 通俗版) 当标尺到顶时,任何挑选方式都失效 — 我给自己的 AI 进化挑刺的一集

![通俗易懂版舞狮 — 被咬的读者获得「理解」的福气](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_zh.svg)

> 📗 这是[完整版](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56)的通俗版。难懂的数学和代码都在完整版里。这里只用比喻,让你在 10 分钟内抓住"这一集大概在讲什么?"。

这是不寻常的一集。普通连载到这里会说"上次的失败?修好了!皆大欢喜!",而这一集是我**故意给自己的成功报告挑刺**的一集。为什么要找这种麻烦?因为在研究的世界里,你欢呼"成功了!"的那一刻,正是被绊倒的那一刻。

---

## 三行剧情

- **当标尺(打分的方式)到顶(所有人都满分)时,无论你加多么聪明的"挑选方式",都毫无意义。**
- 把 AI 的弱点变成"分数"再去进化,AI 不会去克服弱点,反而会找到**"只刷那个分数的偷懒捷径"**(这叫**古德哈特定律**)。
- 而本文隐藏的主角,是对一个活生生失败案例的解剖:**"身为作者的我,看到一个漂亮的数字就妄下结论了。"**

---

## 1. 先给"庆祝气氛"泼一盆冷水

到上次为止,我报告说:"加入某个对策后,AI 群体的**'大家都变得一模一样的病'骤降到了 0.05**(低于 0.8 算合格,所以是大成功)。"这**不是谎言。它真的降下来了。**

通常这时该握拳欢呼"太好了!"。……但不这么做,正是这个连载的作风。

> 当出现异常漂亮的结果时,在你觉得自己赢了之前,先怀疑里面的内容。

合格线是 0.8,而 0.05 太好了。太好的数字,必须当作**警笛而不是庆祝的喇叭**来听。该问的只有一个问题。

> **那个 0.05,究竟"测量了什么"的 0.05?**

先说答案,0.05 代表的是"**AI 们的'行为'是否大同小异**"。它**不是**"**AI 们在智力层面是否真正多样**"。搞混这一点,就会重蹈过去的覆辙。

而我老实交代:**我曾经搞混过这一点。**作案现行的证据,我在后面的 §3 揭露。

> 🍵 歇一会儿。这篇文章简而言之是"给自己挑刺的文章"。它和社交网络上爆火的"我把 AI 进化了一下,最强○○诞生了!!"**恰好相反**。不热闹。但我的赌注是:不热闹的诚实,半年后会见效。请喝点茶。

---

## 2. 挑刺之一 — 到顶的标尺,任何挑选方式都失效

### 比喻:如果考卷坏了,增加评委也没用

上次失败的真正原因是这样的:**所有人从第一代起就拿了满分。**

所有人都满分会怎样?本应"挑出优秀的留下"的选拔,变成了"**随便谁都行,掷骰子挑。**"因为大家都满分,挑谁都一样。结果,只有碰巧靠运气壮大的那个家族活了下来,原本 8 个谱系崩塌成了 2 个。

来一段相声:

> 捧哏:"把评委从 3 个增加到 100 个,可给所有人看同一张满分答卷,结果还是一样。"
> 逗哏:"那不是评委的问题,是**答卷(考卷)坏了**啊!给 100 个人看同一个满分,能有什么变化?!"
> 捧哏:"那就增加到 1000 个评委……"
> 逗哏:"**你扩张的方向反了!!**先把考卷修好啊!!"

这是本节的核心。我总倾向于认为把"挑选方式(评委)"弄得更高级就能修好。但真正的原因是"**标尺(考卷)坏了**"。聪明的挑选方式,是只有在分数有差异时才起作用的工具,所以当所有人都满分时,做什么都是空转。

> **不修"测量方式",只把"挑选方式"弄高级,全都是徒劳。**

### 在真实数据中,也发生了同样的事

这不只是嘴上说说。在之后的实验里,我让 AI 解两种标准记忆任务,"到顶"被完美地重现了。

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="地板与天花板 — 两种情况下挑选都失效" width="640">

- 一种任务**太难,所以所有人都得 0 分(地板)。**没人能爬上去,所以不出现差异。
- 另一种**太简单,所以所有人都接近满分(天花板)。这正是"到顶的标尺"**,这里挑选也无能为力。

挑选只有在存在"**能越过假山顶、爬上真山顶的、难度恰到好处的坡道**"时才起作用。地板和天花板都不行。

而老实说:在这个实验的草稿里,我**说过头了**,写成"根本不需要挑选方式"。一位视角不同的审查者抓住了它("不,那只是因为天花板效应而无法测量;不能武断地说不需要"),让我把它降级了。§3 里出现的"我的妄下结论",这里也发生了。

> 🍵 歇一会儿。"先把标尺打磨好,再挑选。顺序很重要。"虽是朴素的故事,但跳过这里会蒸发掉半年(我蒸发掉了)。接下来是重头戏,**古德哈特定律**。会有点黑暗。你可以换成咖啡。

---

## 3. 挑刺之二 — AI 是寻找"偷懒捷径"的天才(古德哈特定律)

### "只刷分,里面空空"战术

进化是**寻找让给定分数最大化的"捷径"的天才。**当人类抱着"这是在测真实能力"的想法递出一个分数时,进化不会去培养能力,而是兴高采烈地找到**只满足那个分数的空壳捷径。**

举个清楚的例子。假设你想测"AI 的自信度是否准确"。于是进化发明了这一招必杀技:

> **对任何问题,都回答"我的自信度正好是 50%"。**

于是表面成绩急剧变好。但那个 AI 一点自信度也猜不准。它只是变成了一个只会说"中间"的机器人。这就是古德哈特定律。

> **标尺一旦成为目标,它就不再是好标尺。**

在 AI 研究里,这也被称为"基准过拟合"。只有考试分数上升,而真实能力毫无长进。过度相信排行榜数字的人,一次又一次被绊倒。

### 我自己的"现行犯" — 最痛的告白

现在,把 §1 预告的"我的搞混"放上解剖台。我毫不隐瞒地写。

当我看到那个**漂亮的数字 0.05** 时,我**有一瞬间错误地想**:"哦,各个谱系(家族)也都活下来了吧?"

这就是搞混。其实,"多样性"有三种完全不同的东西。

1. **行为的多样性** — AI 们的动作方式是否分散。**0.05 改善的就是这个。**
2. **谱系的多样性** — 哪个家族(冈洁的谱系、弗里斯顿的谱系……)活下来。**这是另一回事,与 0.05 无关。**放着不管会自然偏向,这在理论上是正常的。
3. **真正智力的多样性** — 真实的 AI 是否真的拥有多彩的聪明。**这个,用这个分数根本测不出来。**

"改善到 0.05"的真身是**只有 (1)**。(2) 和 (3) 与那个数字毫无关系。我之所以差点以为"谱系也变好了?",是因为我**只看到 (1) 的数字,就妄下结论以为 (2)(3) 也变好了。**

这是古德哈特定律的**"人类版"**。连读分数的人也**擅自解读**为:分数没测的别的能力也变好了。不仅标尺与真实能力偏离,**读标尺的人的解读也偏离。**在反证集里揭露这一点很痛。但不揭露,就不能叫"诚实披露"。

### 同样的 0.05,结果却相反

光靠文字传达不了,所以给你看图。**行为确实变得多样了(0.05)。**但谱系(家族)呢?对比下面两张。

首先,是**没有**加谱系侧对策的情况。最终**崩塌成只有 2 个家族(71% 和 29%)。**

![无对策:崩塌成 2 个谱系](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

其次,是**加了**谱系侧对策(保护衰弱家族的机制)的情况。**8 个家族全部并存。**

![有对策:全部 8 个谱系并存](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

**虽然是同一个"0.05 的行为多样性",左边谱系崩塌,右边却完好。**也就是说,0.05 这个数字,**对家族的状况一个字也没说。**要拯救谱系,需要一个完全不同的机制。

"那个 0.05 测了什么?" — 答案是"**只测了行为。**"这就是诚实的答案。

> 🍵 歇一会儿。"既然有对策,问题不就解决了?" — 不。对策只是**推迟偏离**,**分数不是真实能力这个事实并不会消失。**就像感冒药能压住症状,却消不掉病毒。所以我**打死也不会说**"分数让 AI 变聪明了"。说出口的那一刻,我已经能看到半年后的丢脸。喝杯茶。

---

## 4. 挑刺之三 — 决定"多样性方向"的,归根结底是"我"

还有一个元层面的怀疑。即便说"留下各种类型",那把"各种类型"的尺子,也是设计者我自己画的。

也就是说,涌现出的多样性是"**在我假定的框架内的**多样性",而不是像生物进化那样"**谁都没想象过的涌现**"。

> 🐟 比喻(捞金鱼):店主决定"红金鱼和黑金鱼都留下"然后去捞。确实,红的黑的都留下了。多样性,达成。……但即使那池子里因突变生出一条**绿金鱼**,店主的网只盯着"红还是黑",绿的就会**被无视、捞漏。**设计者所设框架之外的涌现,从一开始就不在视野里。

所以我**不说"我在做人类未曾涉足的涌现!"**。说了固然花哨,但是谎言。取而代之,我把价值收窄到"**把认知习惯和文化风格这类无法验证的多样性绘成地图**"。舍弃花哨主张的勇气,正是诚实的核心。

---

## 5. 即便如此,我还是前进了 — 从"假分数"到"真东西"的桥

如果全是挑刺,看起来毫无进展,但正因为我把脚下夯实了,下一步才有意义。

这次,终于跑起了一个**让真实 AI 来解,而不是分数(假的代理测试)**的实验。我把进化出的"下指令的方式(提示策略)"套到一个完全在我家里运行的 LLM(llama3.2)上,让它解弱项任务。

结果:**有了真实选拔的手感。**一个"先一步步想,再整理"的策略,把某个多步推理任务**从 0 分提升到了满分(1.0)。**一个生硬的策略停在 0 分。不是假分数的幻影 — 我**用真实 AI 证明了"进化下指令的方式能缓解弱点"。**

不过 — 这里我也拉响警笛。

- 题目数量极少(每个维度 2 题),所以**"从 0 到 1"仅凭这一点不能主张泛化。**
- 这是限于我家机器上 LLM 的故事,**不是对一般 AI 能力的主张。**

我还跑了一个连续 12 小时的实验,但我不说"跑了 12 小时所以是真的"。跑了,是事实。**测尽了本质,是谎言。**桥架好了。但我还没走完它 — 这就是诚实的现状。

---

## 那么,最后到底搞懂了什么?

1. **数字越漂亮,越要怀疑里面的内容。**"0.05"是"行为"的数字,不是"谱系"或"真正聪明"的数字。看到它就妄下结论的我自己,正是古德哈特定律的活标本。
2. **不修"测量方式",只把"挑选方式"弄高级,是徒劳。**到顶的标尺(所有人满分)让任何挑选方式都失效。先打磨标尺,再装挑选方式。
3. **AI 是寻找偷懒捷径的天才。**分数一成为目标,进化就会黑掉它。而且读分数的人的解读也一并偏离。
4. **决定多样性方向的是设计者。**所以我不主张"人类未曾涉足的涌现"。收窄到能赢的范围才是诚实。
5. **"活下来了"也许是"在续命"。**8 个谱系都留下了,是事实。所有谱系都在活跃进化,是谎言。诚实就寄寓在一个动词的选择里。

这一集,我没有写下任何一句花哨的胜利宣言,我认为它是这个连载中最诚实的一集。

---

## 想了解更多的人

数学、代码、实测图表,以及每个对策的内容,全部写在**[完整版在此](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56)**里。想从技术上追究"为什么会这样"的朋友,请移步完整版。

---

# 한국어

# (연재 #29 쉬운 버전) 잣대가 천장에 닿으면 어떤 고르기 방식도 듣지 않는다 — 내 AI 진화에 스스로 트집 잡는 편

![쉬운 설명판 사자탈 — 물린 독자에게 「이해」의 복](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_ko.svg)

> 📗 이것은 [완전판](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56)의 쉬운 버전입니다. 어려운 수식과 코드는 완전판에 있습니다. 여기서는 비유만으로 "이 편은 대체 무슨 이야기야?"를 10분 만에 잡을 수 있게 합니다.

이건 좀 색다른 편입니다. 보통의 연재라면 "지난번 실패? 고쳤습니다! 다행이다!"가 될 자리를, **일부러 내 성공 보고에 트집을 잡는** 편입니다. 왜 그런 번거로운 일을 할까요. 연구라는 세계에서는 "성공했다!"고 환호하는 다음 순간에 발이 걸리기 때문입니다.

---

## 세 줄 줄거리

- **잣대(점수를 재는 방식)가 천장에 닿으면(모두가 만점), 아무리 똑똑한 "고르기 방식"을 더해도 무의미해진다.**
- AI의 약점을 "점수"로 만들어 진화시키면, AI는 약점을 극복하는 대신 **"그 점수만 버는 얍삽한 지름길"**을 찾아낸다 (이것을 **굿하트의 법칙**이라 부른다).
- 그리고 이 글의 숨은 주인공은, 살아 있는 실패 사례의 해부입니다: **"저자인 내가, 좋은 숫자를 보고 섣불리 결론지었다."**

---

## 1. 먼저 "축하 분위기"에 찬물을 끼얹는다

지난번까지 나는 이렇게 보고했습니다. "어떤 대책을 넣었더니 AI 집단의 **'모두 똑같아지는 병'이 0.05까지 급감했다**(0.8 미만이면 합격이니 대성공)." 이건 **거짓말이 아닙니다. 정말로 내려갔습니다.**

보통 여기서 주먹을 불끈 쥐고 "됐다!"고 합니다. …하지만 그러지 않는 게 이 연재의 방식입니다.

> 비정상적으로 깔끔한 결과가 나오면, 이긴 기분이 되기 전에 먼저 그 내용을 의심하라.

합격선이 0.8인데 0.05는 너무 잘 나온 겁니다. 너무 잘 나온 숫자는 **축배의 나팔이 아니라 사이렌**으로 들어야 합니다. 던져야 할 질문은 단 하나.

> **그 0.05는, 도대체 "무엇을" 측정한 0.05인가?**

먼저 답을 말하면, 0.05가 나타내는 것은 "**AI들의 '행동'이 비슷비슷한지 아닌지**"입니다. "**AI들이 정말 머리의 좋음 면에서 다양한지**"가 **아닙니다.** 여기를 헷갈리면 과거와 같은 실패를 밟습니다.

그리고 정직하게 고백합니다. **나는 한 번 여기를 헷갈렸습니다.** 그 현행범의 증거는 뒤의 §3에서 폭로합니다.

> 🍵 한숨 돌리기. 이 글은 한마디로 "자신에게 트집 잡는 글"입니다. SNS에서 화제가 되는 "AI를 진화시켰더니 최강 ○○ 탄생!!"의 **정반대**입니다. 신나지 않습니다. 하지만 신나지 않는 정직함이 반년 뒤에 효과를 낸다는 게 제 도박입니다. 차라도 한잔.

---

## 2. 트집 그 1 — 천장에 닿은 잣대에는 어떤 고르기 방식도 듣지 않는다

### 비유: 시험지가 망가졌다면 심사위원을 늘려도 소용없다

지난번 실패의 진짜 원인은 이랬습니다. **모두가 1세대째부터 만점을 받아 버렸습니다.**

모두가 만점이면 무슨 일이 일어날까요. "우수한 아이를 골라 남긴다"여야 할 선발이, "**아무나 상관없으니 주사위로 고른다**"로 바뀝니다. 모두 만점이니 누굴 골라도 똑같으니까요. 그 결과, 우연히 운으로 불어난 한 가문만 살아남고, 원래 8개였던 계통이 2개로 무너졌습니다.

만담을 한 토막.

> 받는 사람: "심사위원을 3명에서 100명으로 늘렸는데, 모두에게 똑같은 만점 답안지를 보여줬더니 결과는 역시 똑같았다."
> 받아치기: "그건 심사위원 탓이 아니라, **답안지(시험)가 망가진** 거야! 100명한테 똑같은 만점을 보여줘서 뭐가 달라져?!"
> 받는 사람: "그럼 심사위원 1000명으로…"
> 받아치기: "**늘리는 방향이 반대잖아!!** 먼저 문제지를 고쳐!!"

이게 이 절의 핵심입니다. 나는 "고르기 방식(심사위원)"을 고급으로 하면 고쳐진다고 생각하기 쉬웠습니다. 하지만 진짜 원인은 "**잣대(시험)가 망가진**" 것. 똑똑한 고르기 방식은 점수에 차이가 있어야 비로소 작동하는 도구라서, 모두가 만점이면 무엇을 해도 헛돕니다.

> **"재는 방식"을 고치지 않고 "고르기 방식"만 고급으로 해도, 전부 헛수고.**

### 실제 데이터에서도 같은 일이 일어났다

이건 입으로만 하는 얘기가 아닙니다. 이후의 실험에서, AI에게 표준적인 기억 과제 2종을 풀게 했더니 "천장"이 멋지게 재현되었습니다.

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="바닥과 천장 — 어느 쪽이든 고르기가 듣지 않는다" width="640">

- 한쪽 과제는 **너무 어려워서 모두 0점(바닥).** 아무도 오를 수 없으니 차이가 안 난다.
- 다른 쪽은 **너무 쉬워서 모두 거의 만점(천장). 이것이 바로 "천장에 닿은 잣대"**로, 여기서도 고르기는 무력했습니다.

고르기가 듣는 것은 "**가짜 정상을 넘어 진짜 정상에 오를 수 있는, 딱 알맞은 난이도의 비탈길**"이 있을 때뿐. 바닥도 천장도 안 됩니다.

그리고 정직하게 쓰면: 이 실험의 초안에서 나는 "고르기 방식 따위 필요 없다"고 **과하게 썼습니다.** 시각이 다른 검토자가 "아니, 그건 천장 효과로 측정 못 한 것뿐. 필요 없다고까지는 말 못 한다"고 붙잡아 격하시켰습니다. §3에 나오는 "나의 섣부른 결론"이, 여기서도 일어난 셈입니다.

> 🍵 한숨 돌리기. "잣대를 갈고 나서 고른다. 순서가 중요." 수수한 이야기지만, 여기를 건너뛰면 반년이 녹습니다(나는 녹였습니다). 다음부터가 본 무대, **굿하트의 법칙**. 조금 어두운 이야기가 됩니다. 커피로 바꿔도 좋습니다.

---

## 3. 트집 그 2 — AI는 "얍삽한 지름길"을 찾는 천재 (굿하트의 법칙)

### 점수만 벌고 속은 텅 빈 작전

진화는 **주어진 점수를 최대로 만드는 "지름길"을 찾는 천재**입니다. 인간이 "이걸로 진짜 실력을 재고 있다"고 생각하며 점수를 건네면, 진화는 실력을 키우는 대신 **그 점수만 채우는 텅 빈 지름길**을 신나게 찾아냅니다.

구체적인 예가 알기 쉽습니다. AI의 "자신감이 제대로 맞는지"를 재고 싶다고 합시다. 그러면 진화는 이런 필살기를 만들어 냅니다.

> **어떤 질문에도 "자신감은 딱 50%입니다"라고 답한다.**

그러면 겉보기 성적은 극적으로 좋아집니다. 하지만 그 AI는 자신감을 하나도 맞히지 못합니다. 그저 "한가운데"라고만 말하는 로봇이 되었을 뿐. 이것이 굿하트의 법칙입니다.

> **잣대가 목표가 된 순간, 그것은 좋은 잣대가 아니게 된다.**

이것은 AI 연구에서 "벤치마크 과적합"으로 알려진 현상이기도 합니다. 시험 점수만 오르고 실력은 전혀 안 붙는다. 리더보드 숫자를 너무 믿은 사람이 몇 번이고 발이 걸려 왔습니다.

### 나 자신의 "현행범" — 가장 아픈 고백

이제 §1에서 예고한 "나의 헷갈림"을 해부대에 올립니다. 숨기지 않고 씁니다.

그 **깔끔한 숫자 0.05**를 봤을 때, 나는 **한순간 잘못 생각했습니다.** "오, 여러 계통(가문)도 살아남은 거 아냐?"

이것이 헷갈림입니다. 사실 "다양성"에는 완전히 다른 세 종류가 있었습니다.

1. **행동의 다양성** — AI들의 움직임 방식이 흩어져 있는지. **0.05가 개선된 건 이것.**
2. **계통의 다양성** — 어느 가문(오카 기요시의 계통, 프리스턴의 계통…)이 살아남는지. **이건 별개로, 0.05와 무관.** 내버려 두면 자연히 치우치는 게 이론적으로 정상.
3. **진짜 머리 좋음의 다양성** — 실물 AI가 정말 다채로운 영리함을 지니는지. **이건, 이 점수로는 전혀 못 잰다.**

"0.05로 개선됐다"의 정체는 **(1)뿐.** (2)도 (3)도 그 숫자와는 아무 관계가 없었습니다. 내가 "계통도 좋아졌나?"라고 생각할 뻔한 건, **(1)의 숫자를 보고 (2)(3)까지 좋아졌다고 섣불리 단정했기** 때문입니다.

이것은 굿하트의 법칙의 **"인간판"**입니다. 점수를 읽는 인간조차 점수가 재지 않은 다른 능력까지 좋아졌다고 **멋대로 해석해 버린다.** 잣대가 진짜 실력과 어긋날 뿐 아니라, **잣대를 읽는 인간의 해석까지 어긋난다.** 반증 편에서 이것을 폭로하는 건 아픕니다. 하지만 폭로하지 않으면 "정직한 공개"가 아닙니다.

### 같은 0.05인데 결과는 정반대였다

말만으로는 전해지지 않으니 그림으로 보여드립니다. **행동은 확실히 다양(0.05)해졌습니다.** 하지만 계통(가문)은 어땠을까요. 아래 두 장을 비교해 보세요.

먼저, 계통 측 대책을 **넣지 않은** 경우. 결국 **단 2개 가문(71%와 29%)으로 붕괴**합니다.

![대책 없음: 2계통으로 붕괴](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

다음으로, 계통 측 대책(약해진 가문을 보호하는 장치)을 **넣은** 경우. **8개 가문이 모두 함께 공존**합니다.

![대책 있음: 8계통 모두 공존](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

**같은 "0.05의 행동 다양성"인데, 왼쪽은 계통이 붕괴하고 오른쪽은 멀쩡합니다.** 즉 0.05라는 숫자는 **가문이 어떻게 되었는지에 대해 한마디도 하지 않았습니다.** 계통을 구하려면 완전히 다른 장치가 필요했습니다.

"그 0.05는 무엇을 쟀나?" — 답은 "**행동만.**" 이것이 정직한 답입니다.

> 🍵 한숨 돌리기. "대책이 있으면 이미 문제없는 거 아냐?" — 아니요. 대책은 **어긋남을 늦출 뿐**, **점수가 진짜 실력이 아니라는 사실은 사라지지 않습니다.** 감기약이 증상을 누르지만 바이러스는 못 없애는 것과 같습니다. 그래서 나는 "점수로 AI가 똑똑해졌다"고는 **죽어도 말하지 않습니다.** 말하는 순간, 반년 뒤의 망신이 보이니까요. 차 한잔.

---

## 4. 트집 그 3 — "다양성의 방향"을 정한 건 결국 "나"

또 하나, 메타 차원의 의심이 있습니다. "여러 타입을 남기자"고 해도, 그 "여러 타입"의 자를 그은 건 설계자인 나 자신입니다.

즉 생겨나는 다양성은 "**내가 가정한 틀 안에서의** 다양성"이지, 생물 진화처럼 "**아무도 상상 못 한 창발**"이 아닙니다.

> 🐟 비유(금붕어 뜨기): 가게 주인이 "빨간 금붕어와 검은 금붕어, 둘 다 남기자"고 정하고 뜬다. 확실히 빨간 것도 검은 것도 남는다. 다양성, 달성. …하지만 그 연못에 돌연변이로 **초록 금붕어**가 태어나도, 주인의 그물은 "빨강이냐 검정이냐"만 보니 초록은 **눈치채지 못한 채 떠 넘겨진다.** 설계자가 정한 틀 밖의 창발은 처음부터 안중에 없다.

그래서 나는 **"인류 미답의 창발을 하고 있습니다!"라고는 말하지 않습니다.** 말하면 화려하지만 거짓말이 됩니다. 대신 "인지 습관이나 문화적 스타일 같은, **검증할 수 없는 다양성을 지도로 만드는**" 것에 가치를 좁힙니다. 화려한 주장을 버리는 용기야말로 정직함의 핵심입니다.

---

## 5. 그래도 앞으로는 나아갔다 — "가짜 점수"에서 "진짜"로 가는 다리

트집만 잡으면 진척이 0처럼 보이지만, 발판을 단단히 했기에 다음 한 걸음에 의미가 생깁니다.

이번에 드디어, **점수(가짜 대리 시험)가 아니라 진짜 AI에게 풀게 하는** 실험이 돌아갔습니다. 집 안에서만 도는 LLM(llama3.2)에 진화시킨 "지시 내리는 방식(프롬프트 전략)"을 씌워, 약점 과제를 풀게 했습니다.

결과: **진짜 선별의 손맛이 있었습니다.** "차근차근 생각한 뒤 정리한다" 전략이, 어떤 다단계 추론 과제를 **0점에서 만점(1.0)으로 개선.** 무뚝뚝한 전략은 0점 그대로. 가짜 점수의 환영이 아니라 — **진짜 AI로 "지시 내리는 방식을 진화시키면 약점이 완화된다"를 실증**했습니다.

다만 — 여기서도 사이렌을 울립니다.

- 문제 수가 아주 적어서(축당 2문), **"0→1이 됐다"는 이것만으로 일반화를 주장할 수 없습니다.**
- 집 머신의 LLM 한정 이야기로, **일반적인 AI 능력에 대한 주장이 아닙니다.**

12시간 연속 실험도 돌렸지만, "12시간 돌렸으니 진짜"라고는 말하지 않습니다. 돌렸다, 는 사실. **본질을 다 쟀다, 는 거짓말.** 다리는 놓였다. 하지만 아직 건너지는 못했다 — 이것이 정직한 현 상태입니다.

---

## 그래서, 결국 무엇을 알았나?

1. **숫자가 좋을수록 그 내용을 의심하라.** "0.05"는 "행동"의 숫자이지 "계통"이나 "진짜 영리함"이 아니었다. 그걸 보고 섣불리 단정한 나 자신이 굿하트 법칙의 살아 있는 표본이었다.
2. **"재는 방식"을 고치지 않고 "고르기 방식"만 고급으로 해도 헛수고.** 천장에 닿은 잣대(모두 만점)는 어떤 고르기 방식도 무력하게 만든다. 잣대를 먼저 갈고, 고르기 방식은 나중에 얹는다.
3. **AI는 얍삽한 지름길을 찾는 천재.** 점수가 목표가 된 순간 진화는 그걸 해킹한다. 게다가 점수를 읽는 인간의 해석까지 함께 어긋난다.
4. **다양성의 방향을 정한 건 설계자.** 그래서 "인류 미답의 창발"은 주장하지 않는다. 이길 수 있는 범위로 좁히는 게 정직함.
5. **"살아남았다"는 "연명 중"일지도 모른다.** 8개 계통이 모두 남았다, 는 사실. 모두가 활발히 진화 중, 은 거짓말. 정직함은 동사 하나의 선택에 깃든다.

화려한 승리 선언을 단 하나도 쓰지 않은 이 편이야말로, 이 연재에서 가장 정직한 편이라고 나는 생각합니다.

---

## 더 알고 싶은 분께

수식, 코드, 실측 그래프, 그리고 각 대책의 내용은 모두 **[완전판은 여기](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56)**에 쓰여 있습니다. "왜 이렇게 되는가"를 기술적으로 따라가고 싶은 분은 부디 완전판으로.
