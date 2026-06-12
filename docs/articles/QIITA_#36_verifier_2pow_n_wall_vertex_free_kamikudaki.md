---
title: 'llcore 検証 arc (#36 かみくだき) — 「関所が重すぎる」問題を、角を全部見ずに解く'
tags: [FullSense, llcore, 解説, 形式手法, 進化計算]
private: true
updated_at: '2026-06-06'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

> 📘 これは [#36 本編](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/QIITA_%2336_verifier_2pow_n_wall_vertex_free.md) のかみくだき版です (比喩多め・数式少なめ・短時間で要点だけ)。正確な数値と手順は本編へ。

> ⚠️ **追記 / Addendum (2026-06-06)**: 本文の「8 割(87%)通せた」は **部屋が 8 個(n=8)のとき**の話。部屋が増えると一望の精度は落ちる(部屋 16 個=n=16 で 6 割まで、安い門番と同水準に)。**速さと見逃しゼロは全 n で維持**されるが、高次元では一望が慎重になりすぎる。 / "Passed ~80% (87%)" is for **8 rooms (n=8)**; the glance gets less accurate as rooms grow (down to ~60% at n=16, level with the cheap gatekeeper). Speed and zero-oversight hold at all n. / 「通过约 8 成(87%)」是 **8 个房间(n=8)** 时；房间增多则一望精度下降(n=16 时约 6 成)。速度与零漏检在所有 n 下保持。 / 「약 80%(87%) 통과」는 **방 8 개(n=8)** 기준이며, 방이 늘면 정확도가 떨어진다(n=16 에서 약 60%). 속도와 무누락은 모든 n 에서 유지.

---

# 日本語

# 「進化する AI の関所が、重すぎて潰れる」問題

## たとえ話: 関所と、角を全部見て回る門番

進化する AI、と言われてもピンと来ないかもしれない。ここでの「進化」は、家畜の品種改良に近い。AI の小さな個体をたくさん作って、少しずつ設定を変えた子孫をどんどん生み、その中から「出来のいい子」だけを選んで次の世代に残す——これを何百世代もくり返す。誰も手で設計していないのに、だんだん賢い個体が育っていく。

ただし、賢くなる道のりには危ない子も混じる。AI の「状態」(計算の途中で持っている数値のかたまり) が、世代を追うごとにじわじわ膨らんで止まらなくなる個体だ。これを本稿では **暴走**と呼ぶ。逆に、ちょっとしたズレが時間とともに自然に小さくしぼんでいく個体は安定している (専門的には「収縮する」と言う)。暴走する子を群れに残すと、後の世代ごと壊れてしまう。

そこで、城下に入る前の **関所**で「この個体は暴走しないか?」を一人ずつ確かめる門番を置く。これが本稿の主役、**検査器**だ。暴走する個体を一匹も見逃さない、とてもまじめな門番である。

ところが、この門番の確認のしかたがやたらと律儀で困る。城 (= AI の状態) には「部屋」が n 個ある、と思ってほしい。門番は、各部屋の状態が一番ぶれたときの「角」を調べたい。やっかいなのは、部屋ごとに「角」は端と端の 2 通りあって、n 個の部屋ぜんぶの組み合わせを試すことだ。これは n 個のスイッチの ON/OFF の全パターンを試すのと同じで、組み合わせは **2ⁿ 通り**になる。

数で見るとぞっとする。部屋が 8 個なら 2⁸ = 256 通りで済む。ところが部屋を 1 個増やすたびに、調べる手間がそのつど **倍**になる。だから 16 個では 65,536 (6 万超) 通り、32 個では **43 億通り**。8 個から 16 個は「2 倍」ではなく「256 倍」だ。虫の脳みそ程度——AI として見ればまだ小さい——の規模に育てようとした途端、門番のほうが先に過労で倒れてしまう。

つまり「これ以上 AI を大きく育てられない」という壁の正体は、賢さの限界でも遺伝子の数でもなく、**門番 (検査器) の手間が部屋の数に対して指数的に重くなる**ことだった。これが「進化の天井」だ。

## やったこと: 角を全部歩かず、部屋を「一望」する

そこで思いついたのが、「角を一つずつ歩くのをやめて、部屋全体をひと目で見積もる」やり方だ。たとえるなら、部屋の隅々を巻尺で測って回る代わりに、入り口に立って「この部屋なら、一番散らかってもこのくらいだろう」と一望で天井を見積もる感覚に近い。歩く角の数が 2ⁿ 通りから 1 回の見積もりに減るので、けた違いに安い。

ただし、見積もりには作り方のコツがあった。

- **最初の素朴な見積もり (B1)**: 安全側に倒した結果、**慎重すぎた**。部屋の「平均的な形」と「ぶれ幅」を別々に最悪値で見積もって足し合わせたので、最悪が二重に乗ってしまい、実際よりずっと危険そうに見えてしまう。結果、本当は無害な個体まで門前払いし、城に入れたのは収縮 (安定) 個体のわずか 3 割。これはいちばん安い門番より厳しいという本末転倒で、いったん「安い一望はやっぱりダメだ」と落ち込んだ。
- **見積もりの作り方を変えた版 (B2 = 絶対値で上から押さえる)**: ぶれ幅を別建てにせず、「絶対値で上からまとめて押さえる」やり方に変えた。これが当たりだった。**律儀な門番が通す人の 8 割近く (77.6%) を、たった 1 回の一望で通せた**。さらに安い門番 (∞ノルム) と二人がかりで見ると 87% まで届く。速さは部屋 16 個のとき **1 万 2 千倍**。律儀な門番が数秒かけていた仕事が、ほぼ一瞬で終わる。

ここで大事なのが、**見逃し (偽陽性) はゼロ**だったこと。一望の門番は「通す」と言ったら本当に安全な個体だけを通し、危ない個体をうっかり通すことは一度もなかった。代わりに、安全なのに念のため弾いてしまう取りこぼしはある。だがこの方向の間違いなら許せる——関所の役目は安全の確保で、「厳しすぎる」のは我慢できても「甘くて暴走を通す」のは許されないからだ。一望は「通すと言ったら必ず正しい」という安全側の性質 (専門的には健全性と呼ぶ) を保ったまま、速さだけを稼いだ。

教訓は明快だ。「安い一望」そのものが悪かったのではなく、**最初の見積もりの作り方が下手だっただけ**。しかもこれは、重い本格装置 (SDP) を一から作り始める前に、小さな実験で安く試したからこそ数秒で分かった。仕様を大きくふくらませる前に骨組みだけ安く確かめる——この順番が時間を救った。

## もうひとつの発想: 「断捨離する生き物」に倣う

生き物は、要らないものをどんどん捨てて単純になることがある。洞窟の魚は眼を捨て、寄生虫は遺伝子を捨て、深海の細菌はゲノムを削って身軽になる。**「維持費 > 役立ち度」なら、単純なほうが生き残る**。

これを AI の進化にも入れたい。「性能が良い」だけでなく「**安く検証できる単純な体**」を点数に足せば、AI は自分から身軽な構造へ向かう。

ただし落とし穴がある。「単純」には 2 種類:

- **良い単純** = 体の作りがシンプル (本当に軽い)。これは歓迎。
- **悪い単純①** = 門番が厳しすぎて、何も学ばない優等生もどき (= 一番安い ∞門番の罠)。
- **悪い単純②** = 「何も言わない」に退化した個体 (= unigram 張り付き)。安全で安いが無能。削りすぎて自活できなくなった寄生虫だ。

llcore には「本当に安定しているか」を見抜く目 (健全性 oracle) があるので、**良い単純と退化した単純を見分けられる**。これが FullSense の世界観 ——「賢いだけでなく、安く・安全だと証明できる方向へ進化する」。

## 正直な内訳: 「検査器が賢くする」は言い過ぎだった

最後に、今日いちばん削った話。「強い門番ほど AI が賢くなる」という結果が出ていた。数字は本物だ。でも内訳を疑うと——

文章をぐちゃぐちゃにシャッフルして「学ぶ中身ゼロ」にしても、**門番ごとの差が消えなかった**。つまりこの差は「言葉を学んだ」からではなく、「**進化のしやすさ (動きやすさ)**」という、中身と関係ない現象だった。さらに、進化ではなく勾配でガッツリ学習させると、どの門番でも結果は同じ — 強い門番のご利益は「進化 (ランダム変異) のとき限定」だったのだ。

負けたわけではない。**勝った気になる前に内訳を疑う**——これが FullSense の研究の核 ([feedback_benchmark_honest_disclosure])。本物の発見は「検査器の payoff は learning でなく evolvability」という、より正確な記述のほうだった。

---

要点 3 行:
- 進化 AI の関所 (検査器) は部屋が増えると **2ⁿ で爆発**して潰れる。
- 角を全部見ず**一望する健全な見積もり (B2)** で、8 割近くを 1 万倍速・見逃しゼロで通せた。
- 「コストを進化の選択圧に」+「内訳を疑う正直開示」——身軽で、賢いふりをしない AI へ。

(本編に正確な数値・表・図があります。前段 = #35 検査器の梯子。)

---

# English

# The "evolving AI's checkpoint is too heavy and breaks down" problem

> 📘 This is the plain-language (かみくだき) version of [the #36 main article](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/QIITA_%2336_verifier_2pow_n_wall_vertex_free.md) (more metaphors, fewer formulas, just the gist in a short time). For exact numbers and procedures, go to the main article.

## A parable: a checkpoint, and a gatekeeper who walks around every corner

An evolving AI has a **checkpoint** before entering the castle town. It is a gatekeeper who verifies "won't this individual run away out of control?" (we call this the inspector). It is a diligent gatekeeper who never overlooks a runaway individual.

But this gatekeeper has an absurdly meticulous way of checking. If the castle (= the AI's state) has n "rooms," he walks **all 2ⁿ ways through the corners of the rooms** to check. If there are 8 rooms it takes 256 ways, but with 16 rooms it is 60,000-some ways, and with 32 rooms it is **4.3 billion ways**. The moment you try to grow it to the scale of an insect's brain, the gatekeeper collapses from overwork first. This was the true identity of the "ceiling on evolution."

## What we did: don't walk every corner — take in the rooms "at a glance"

So we tried an approximation that "stops walking every corner and estimates the whole room at a glance."

- The first naive estimate (B1): safe, but **too cautious** — it turned away even individuals that were actually harmless. It let only 30% of the contracting individuals into the castle. That is putting the cart before the horse — stricter than the cheapest gatekeeper — and for a moment we got discouraged, thinking "the cheap glance is no good."
- The version that changed how the estimate is built (B2 = pressing down from above with absolute values): this hit the mark. **It let through nearly 80% (77.6%) of the people the diligent gatekeeper passes, with a single glance.** Paired with the cheap gatekeeper, 87%. The speed at 16 rooms was **12,000×**. Oversights (false positives) were zero.

Lesson: the "cheap glance" itself was not the problem — **the way the first estimate was built was just clumsy**. Before starting to build the heavy full-scale apparatus (SDP), we checked cheaply with a small experiment, and figured it out in seconds.

## Another idea: model it on "creatures that declutter"

Living things sometimes keep discarding what they don't need and become simpler. Cave fish discard their eyes, parasites discard their genes, deep-sea bacteria trim their genomes to travel light. **If "maintenance cost > usefulness," the simpler one survives.**

We want to bring this into AI evolution too. If we add not just "good performance" but "**a simple body that is cheap to verify**" to the score, the AI will steer on its own toward a lighter structure.

But there is a pitfall. "Simple" comes in two kinds:

- **Good simplicity** = the body's build is simple (truly light). This is welcome.
- **Bad simplicity ①** = the gatekeeper is so strict that you get a pseudo-honor-student who learns nothing (= the trap of the cheapest ∞ gatekeeper).
- **Bad simplicity ②** = an individual that has degenerated into "saying nothing" (= sticking to a unigram). Safe and cheap, but incompetent. A parasite that trimmed so much it can no longer fend for itself.

llcore has an eye (a soundness oracle) that sees through "whether it is truly stable," so it can **tell good simplicity apart from degenerate simplicity**. This is the FullSense worldview —— "evolve not merely to be clever, but in a direction where one can prove it is cheap and safe."

## The honest breakdown: "the inspector makes it smart" was an overstatement

Finally, the story I cut the most today. We had a result that "the stronger the gatekeeper, the smarter the AI gets." The numbers are real. But when you doubt the breakdown ——

Even when we shuffled the text into a mess so that there was "zero substance to learn," **the difference between gatekeepers did not vanish**. In other words, this difference was not because it "learned the language," but a phenomenon unrelated to substance: "**ease of evolving (ease of moving)**." Furthermore, when we trained hard with gradients instead of evolution, the result was the same for every gatekeeper — the benefit of a strong gatekeeper was "limited to evolution (random mutation)."

It is not a defeat. **Doubt the breakdown before you feel like you've won** —— this is the core of FullSense research ([feedback_benchmark_honest_disclosure]). The real finding was the more accurate description: "the inspector's payoff is not learning but evolvability."

---

The point in 3 lines:
- An evolving AI's checkpoint (the inspector) **explodes as 2ⁿ** and breaks down as the rooms increase.
- With a **sound estimate that takes the whole thing in at a glance (B2)** instead of looking at every corner, we passed nearly 80% at 10,000× speed with zero oversights.
- "Turning cost into evolutionary selection pressure" + "honest disclosure that doubts the breakdown" —— toward an AI that travels light and does not pretend to be clever.

(The main article has the exact numbers, tables, and figures. The preceding installment = #35: the ladder of inspectors.)

---

# 中文

# 「进化中的 AI 的关卡，重得自己先垮了」这个问题

> 📘 这是 [#36 正篇](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/QIITA_%2336_verifier_2pow_n_wall_vertex_free.md) 的通俗（かみくだき）版（比喻多、公式少、短时间只讲要点）。准确的数值与步骤请看正篇。

## 打个比方：关卡，以及一个把所有角都走遍的守门人

进化中的 AI，在进城之前有一道 **关卡**。守门人会确认「这个个体会不会失控？」（这就是检查器）。这是一个不会放过任何失控个体的、认真的守门人。

可这位守门人的确认方式过分一板一眼。当城（= AI 的状态）里有 n 个「房间」时，他会 **把房间的角 2ⁿ 种全部走遍** 来检查。房间有 8 个的话 256 种就够了，但 16 个就是 6 万种，32 个就是 **43 亿种**。一旦想把它养到昆虫脑子那点规模，守门人自己反而先累垮了。这就是「进化天花板」的真面目。

## 做了什么：不走遍所有角，而是把房间「一眼望尽」

于是我们尝试了「不再走遍所有角，而是一眼把整个房间估算出来」的近似。

- 最初的朴素估算（B1）：安全，但 **太过谨慎**，连本来无害的个体也吃了闭门羹。能进城的只有收缩个体的三成。比最便宜的守门人还严，本末倒置，一度沮丧地认为「便宜的一眼望尽不行」。
- 改了估算做法的版本（B2 = 用绝对值从上面压住）：这一招中了。**律己的守门人会放行的人里，近八成（77.6%）只用一眼望尽 1 次就能放行**。和便宜的守门人搭档则达 87%。速度在房间 16 个时为 **1 万 2 千倍**。漏放（假阳性）为零。

教训：并不是「便宜的一眼望尽」本身不好，而是 **最初的估算做法太笨拙** 罢了。在开始做沉重的正规装置（SDP）之前，用小实验廉价地确认一下，几秒钟就明白了。

## 另一个发想：仿照「会断舍离的生物」

生物会把不需要的东西一个个舍弃、变得简单。穴居的鱼舍弃眼睛，寄生虫舍弃基因，深海的细菌削减基因组让自己变轻。**若「维持费 > 有用度」，那么简单的一方存活**。

我们想把这个也放进 AI 的进化里。不只看「性能好」，而是在打分里加上「**能廉价验证的简单身体**」，AI 就会自己朝轻装的结构前进。

不过有个坑。「简单」分两种：

- **好的简单** = 身体构造简单（真的轻）。这是欢迎的。
- **坏的简单①** = 守门人太严，结果出了个什么都不学的「伪优等生」（= 最便宜的 ∞ 守门人的陷阱）。
- **坏的简单②** = 退化成「什么都不说」的个体（= 黏在 unigram 上）。安全又便宜，但无能。是削减过头、再也无法自食其力的寄生虫。

llcore 有一双能看穿「是否真的稳定」的眼睛（健全性 oracle），所以 **能分辨好的简单与退化的简单**。这正是 FullSense 的世界观 —— 「不只是聪明，而是朝着能证明自己廉价、安全的方向进化」。

## 诚实的内幕：「检查器让 AI 变聪明」说过头了

最后，讲今天削减得最多的那段。曾经出现过「守门人越强，AI 越聪明」的结果。数字是真的。但一旦怀疑其内幕——

把文章打乱成一团、让「要学的内容为零」，**各守门人之间的差异也没有消失**。也就是说，这个差异并不是因为「学会了语言」，而是「**易进化性（容易动起来）**」这种与内容无关的现象。再进一步，不用进化、而用梯度狠狠地学习时，无论哪个守门人结果都一样 —— 强守门人的好处，原来「仅限于进化（随机变异）的时候」。

这不算输。**在自以为赢之前先怀疑内幕** —— 这才是 FullSense 研究的核心（[feedback_benchmark_honest_disclosure]）。真正的发现，是「检查器的 payoff 不是 learning 而是 evolvability」这个更准确的描述。

---

要点 3 行：
- 进化 AI 的关卡（检查器）随着房间增多会 **以 2ⁿ 爆炸** 而垮掉。
- 用不看遍所有角、**一眼望尽的健全估算（B2）**，把近八成以 1 万倍速、零漏放放行。
- 「把成本变成进化的选择压」+「怀疑内幕的诚实披露」—— 朝着轻装、不装聪明的 AI 前进。

（准确的数值、表、图在正篇。前篇 = #35 检查器的梯子。）

---

# 한국어

# "진화하는 AI의 관문이, 너무 무거워서 무너진다" 문제

> 📘 이것은 [#36 본편](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/QIITA_%2336_verifier_2pow_n_wall_vertex_free.md)의 쉽게 풀어쓴 버전입니다 (비유 많음·수식 적음·짧은 시간에 요점만). 정확한 수치와 절차는 본편으로.

## 비유 이야기: 관문과, 모서리를 전부 돌아보는 문지기

진화하는 AI에는, 성 안으로 들어가기 전의 **관문(關所)**이 있다. "이 개체가 폭주하지 않는가?"를 확인하는 문지기다(이것을 검사기라고 부른다). 폭주하는 개체를 놓치지 않는, 성실한 문지기다.

그런데 이 문지기, 확인하는 방식이 지나치게 깐깐하다. 성(= AI의 상태)의 "방"이 n개 있으면, **방의 모서리를 2ⁿ 가지 전부 걸어 다니며** 체크한다. 방이 8개라면 256가지로 끝나지만, 16개면 6만 가지, 32개면 **43억 가지**. 곤충의 뇌 정도의 규모로 키우려는 순간, 문지기 쪽이 먼저 과로로 쓰러진다. 이것이 "진화의 천장"의 정체였다.

## 한 일: 모서리를 전부 걷지 않고, 방을 "한눈에" 본다

그래서 "모서리를 전부 걷는 것을 그만두고, 방 전체를 한눈에 어림한다"는 근사를 시도했다.

- 처음의 소박한 어림 (B1): 안전하지만 **너무 신중해서**, 사실은 무해한 개체까지 문전박대. 성에 들인 것은 수축 개체의 3할뿐. 가장 싼 문지기보다 엄격하다는 본말 전도로, 일단 "싼 한눈에 보기는 안 된다"고 낙담했다.
- 어림을 만드는 방식을 바꾼 버전 (B2 = 절댓값으로 위에서 누른다): 이것이 정답. **깐깐한 문지기가 통과시키는 사람의 8할 가까이(77.6%)를, 한눈에 보기 1회로 통과시켰다**. 싼 문지기와 짝지으면 87%. 속도는 방 16개에서 **1만 2천 배**. 놓침(위양성)은 제로.

교훈: "싼 한눈에 보기" 자체가 나쁜 것이 아니라, **처음의 어림을 만드는 방식이 서툴렀을 뿐**. 무거운 본격 장치(SDP)를 만들기 시작하기 전에, 작은 실험으로 싸게 확인했더니 수 초 만에 알 수 있었다.

## 또 하나의 발상: "단샤리(斷捨離)하는 생물"을 본뜨다

생물은, 필요 없는 것을 자꾸자꾸 버리고 단순해지는 경우가 있다. 동굴의 물고기는 눈을 버리고, 기생충은 유전자를 버리고, 심해의 세균은 게놈을 깎아서 가벼워진다. **"유지비 > 유용도"라면, 단순한 쪽이 살아남는다**.

이것을 AI의 진화에도 넣고 싶다. "성능이 좋다"뿐만 아니라 "**싸게 검증할 수 있는 단순한 몸**"을 점수에 더하면, AI는 스스로 가벼운 구조로 향한다.

다만 함정이 있다. "단순"에는 2종류:

- **좋은 단순** = 몸의 구조가 심플(정말로 가볍다). 이것은 환영.
- **나쁜 단순①** = 문지기가 너무 엄격해서, 아무것도 학습하지 않는 우등생 흉내(= 가장 싼 ∞문지기의 함정).
- **나쁜 단순②** = "아무 말도 하지 않는다"로 퇴화한 개체(= unigram 달라붙음). 안전하고 싸지만 무능. 너무 깎아서 자립할 수 없게 된 기생충이다.

llcore에는 "정말로 안정되어 있는가"를 꿰뚫어 보는 눈(건전성 oracle)이 있으므로, **좋은 단순과 퇴화한 단순을 구분할 수 있다**. 이것이 FullSense의 세계관 —— "똑똑하기만 한 것이 아니라, 싸고·안전하다고 증명할 수 있는 방향으로 진화한다."

## 정직한 내역: "검사기가 똑똑하게 만든다"는 과장이었다

마지막으로, 오늘 가장 많이 깎은 이야기. "강한 문지기일수록 AI가 똑똑해진다"는 결과가 나와 있었다. 숫자는 진짜다. 하지만 내역을 의심해 보면——

문장을 뒤죽박죽 셔플해서 "배울 내용 제로"로 만들어도, **문지기별 차이가 사라지지 않았다**. 즉 이 차이는 "말을 배웠기" 때문이 아니라, "**진화의 용이성(움직이기 쉬움)**"이라는, 내용과 관계없는 현상이었다. 게다가, 진화가 아니라 경사(gradient)로 진하게 학습시키면, 어느 문지기에서도 결과는 같다 — 강한 문지기의 이득은 "진화(랜덤 변이)일 때 한정"이었던 것이다.

진 것이 아니다. **이긴 기분이 되기 전에 내역을 의심한다** —— 이것이 FullSense 연구의 핵심([feedback_benchmark_honest_disclosure]). 진짜 발견은 "검사기의 payoff는 learning이 아니라 evolvability"라는, 더 정확한 기술 쪽이었다.

---

요점 3줄:
- 진화 AI의 관문(검사기)은 방이 늘어나면 **2ⁿ으로 폭발**해서 무너진다.
- 모서리를 전부 보지 않고 **한눈에 보는 건전한 어림(B2)**으로, 8할 가까이를 1만 배 빠르게·놓침 제로로 통과시켰다.
- "비용을 진화의 선택압으로" + "내역을 의심하는 정직한 개시" —— 가볍고, 똑똑한 척하지 않는 AI로.

(본편에 정확한 수치·표·그림이 있습니다. 전편 = #35 검사기의 사다리.)
