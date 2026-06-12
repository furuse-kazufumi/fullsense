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

生き物は、要らないものをどんどん捨てて単純になることがある。真っ暗な洞窟に棲む魚は眼を捨て、他の生き物に寄りかかって暮らす寄生虫は自前の遺伝子を捨て、深海の細菌はゲノムを削って身軽になる。なぜ捨てるほうが得なのか——眼も遺伝子も、持っているだけで維持にコスト (エネルギーや複製の手間) がかかる。光のない洞窟で眼は何の役にも立たないのに維持費だけ取られるなら、捨てた個体のほうが生き残りやすい。**「維持費 > 役立ち度」なら、単純なほうが生き残る**——これが生き物の世界の冷徹なルールだ。

これを AI の進化にも持ち込みたい。今は「性能が良い」かどうかだけで個体を選んでいる。そこに「**安く検証できる単純な体**」という観点を点数に足してやれば、AI は誰に言われずとも、門番が一望で楽に通せる身軽な構造へ自分から向かっていくはずだ。コストの低さ自体を「進化の選択圧」にする、という発想である。

ただし、ここには落とし穴がある。「単純」には見分けるべき種類があるからだ。

- **良い単純** = 体の作りそのものがシンプル (本当に軽い)。検証も安く、しかも進化が動きやすい。これは大歓迎。
- **悪い単純①** = 門番が厳しすぎるせいで、何も学ばない「優等生もどき」が生き残ってしまう (= 一番安い ∞門番の罠)。安全に見えるが、ただ縮こまっているだけ。
- **悪い単純②** = 「何も言わない」に退化した個体 (= とにかく無難な答えだけ返す状態)。安全で安いが無能。削りすぎて自力で生きられなくなった寄生虫と同じだ。

つまり「安ければ何でも良い」と素朴に報酬を与えると、AI は楽をして退化するほうへ逃げてしまう。だから性能とコストは単純に足し算 (スカラー化) するのではなく、両者のつり合い (パレート) として扱う必要がある。

幸い llcore には「本当に安定しているか」を見抜く目 (健全性 oracle) がある。だから **良い単純と退化した単純を見分けられる**——同じ「単純で安い」でも、ちゃんと中身のある個体なのか、ただ縮こまっただけの個体なのかを判別できる。これは普通の進化システムにはできない芸当だ。これこそが FullSense の世界観 ——「賢いだけでなく、安く・安全だと証明できる方向へ進化する」。

## 正直な内訳: 「検査器が賢くする」は言い過ぎだった

最後に、今日いちばん削った話をする。実験では「強い門番ほど AI が賢くなる (言語予測がうまくなる)」という結果が出ていた。10 回試して全部同じ傾向、偶然では起きにくい差で、数字そのものは本物だ。だが——勝った気になる前に、内訳を疑った。

そこでやったのが対照実験だ。学習に使う文章をぐちゃぐちゃにシャッフルして、意味の通る並びを壊し、「学ぶべき中身をゼロ」にした。もし門番ごとの差が「言葉をうまく学んだから」生まれているなら、学ぶ中身を消したこの条件では差も消えるはずだ——そう事前に予想していた。

ところが、**門番ごとの差は消えなかった**。意味のない文字列でも、強い門番のほうが良いスコアを出し続けたのだ。これは「言葉を学んだから賢くなった」のではないことを意味する。差を生んでいた正体は、中身とは関係のない「**進化のしやすさ (動きやすさ)**」だった。良い遺伝子がどこかに在るかどうか (天井の高さ) ではなく、変異をくり返しながらそこへ「歩いて登れるか」の差、というわけだ。

駄目押しの確認もある。進化 (ランダムな変異と選択) ではなく、勾配でガッツリ最適化して学習させると、**どの門番でも結果は同じ**になった。つまり強い門番のご利益は「進化のとき限定」で、学習そのものを底上げしていたわけではない。

これは負けではない。**勝った気になる前に内訳を疑う**——これこそが FullSense の研究の核だ ([feedback_benchmark_honest_disclosure])。華やかな見出し (「検査器が AI を賢くする」) を捨てる代わりに、「検査器の効きめは learning ではなく evolvability だ」という、より正確で地味な発見が手元に残った。地味でも、正しいほうを残す。

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

"An evolving AI" may not mean much at first. The "evolution" here is close to selective breeding of livestock. We create many tiny AI individuals, breed offspring whose settings are nudged a little each time, keep only the "well-made" ones for the next generation — and repeat this for hundreds of generations. Nobody designs a clever one by hand, yet smarter individuals gradually emerge.

But along the road to cleverness, dangerous individuals slip in. These are individuals whose "state" (the bundle of numbers the computation carries midway) keeps swelling generation after generation and never stops. We call this **running away (out of control)**. Conversely, an individual whose small deviations naturally shrink over time is stable (technically, it "contracts"). Leave a runaway child in the herd and later generations break along with it.

So we place a **checkpoint** before entering the castle town, with a gatekeeper who checks each individual one by one: "won't this one run away out of control?" This is the protagonist of the article, the **inspector**. He is a very diligent gatekeeper who never overlooks even a single runaway.

But this gatekeeper has an absurdly meticulous way of checking. Picture the castle (= the AI's state) as having n "rooms." The gatekeeper wants to examine the "corner" — the most extreme wobble — of each room. The trouble is that each room has two corners (one extreme and the other), and he tries every combination across all n rooms. This is the same as trying every ON/OFF pattern of n switches, which comes to **2ⁿ combinations**.

The numbers are chilling. With 8 rooms it is 2⁸ = 256 combinations — fine. But every time you add one room, the work **doubles**. So 16 rooms is 65,536 (over sixty thousand), and 32 rooms is **4.3 billion**. Going from 8 to 16 rooms is not "twice" but "256 times" the work. The moment you try to grow it to the scale of an insect's brain — still small for an AI — the gatekeeper collapses from overwork first.

So the true identity of the wall "we can't grow the AI any bigger" was not a limit of cleverness nor the number of genes, but the fact that **the gatekeeper's (inspector's) labor grows exponentially with the number of rooms**. This is the "ceiling on evolution."

## What we did: don't walk every corner — take in the rooms "at a glance"

So we hit on this: stop walking the corners one by one, and estimate the whole room at a glance. As an analogy, instead of going around measuring every nook with a tape measure, you stand in the doorway and size up the ceiling at a glance: "even at its messiest, this room is about this big." The number of corners to walk drops from 2ⁿ to a single estimate, so it is incomparably cheaper.

But there was a knack to building the estimate.

- **The first naive estimate (B1)**: erring on the safe side, it was **too cautious**. It estimated the room's "average shape" and its "wobble width" separately, each at its worst, and added them up — so the worst case got counted twice, making everything look far more dangerous than it really is. As a result it turned away even harmless individuals, letting only 30% of the contracting (stable) individuals into the castle. That is stricter than the cheapest gatekeeper — putting the cart before the horse — and for a moment we got discouraged: "the cheap glance really is no good after all."
- **The version that changed how the estimate is built (B2 = pressing down from above with absolute values)**: instead of treating the wobble separately, it presses everything down from above using absolute values. This hit the mark. **It let through nearly 80% (77.6%) of the people the diligent gatekeeper passes, with a single glance.** And with the cheap gatekeeper (∞-norm) as a second pair of eyes, it reaches 87%. The speed at 16 rooms was **12,000×**. Work that took the diligent gatekeeper seconds finishes almost instantly.

What matters most here is that **oversights (false positives) were zero**. When the glance gatekeeper says "pass," he passes only genuinely safe individuals, and not once did he carelessly let a dangerous one through. In exchange, there are some safe ones he rejects just in case. But that direction of error is forgivable — a checkpoint exists to keep things safe, and while "too strict" is bearable, "too lax, letting a runaway through" is not. The glance kept this safe-side property (technically called soundness) — "if it says pass, it is always right" — while gaining only speed.

The lesson is clear. The "cheap glance" itself was not the problem — **the way the first estimate was built was simply clumsy**. And we figured this out in seconds precisely because we tried it cheaply with a small experiment before building the heavy full-scale apparatus (SDP) from scratch. Confirm the skeleton cheaply before inflating the spec — that order saved us time.

## Another idea: model it on "creatures that declutter"

Living things sometimes keep discarding what they don't need and become simpler. Fish living in pitch-dark caves discard their eyes; parasites that live leaning on other organisms discard their own genes; deep-sea bacteria trim their genomes to travel light. Why is discarding the better deal? Eyes and genes cost something to maintain (energy, the labor of copying) just by being held. If eyes are useless in a lightless cave yet still charge a maintenance fee, the individual that discards them survives more easily. **If "maintenance cost > usefulness," the simpler one survives** — that is the cold rule of the living world.

We want to bring this into AI evolution too. Right now we select individuals only by whether their "performance is good." If we also add the viewpoint of "**a simple body that is cheap to verify**" to the score, the AI should, without being told, steer on its own toward a light structure that the gatekeeper can wave through at a glance. The idea is to make the cheapness of cost itself an "evolutionary selection pressure."

But there is a pitfall here, because "simple" comes in kinds we must tell apart.

- **Good simplicity** = the body's build itself is simple (truly light). Cheap to verify, and easy for evolution to move through. Very welcome.
- **Bad simplicity ①** = because the gatekeeper is so strict, a "pseudo-honor-student" who learns nothing survives (= the trap of the cheapest ∞ gatekeeper). It looks safe but is merely cowering.
- **Bad simplicity ②** = an individual that has degenerated into "saying nothing" (= a state that just returns the safest non-answer, sticking to a unigram). Safe and cheap, but incompetent. The same as a parasite that trimmed so much it can no longer fend for itself.

In other words, if you naively reward "anything cheap is fine," the AI takes the easy way out and escapes toward degeneration. So performance and cost must not be simply added up (scalarized); they must be handled as a balance between the two (a Pareto trade-off).

Fortunately, llcore has an eye (a soundness oracle) that sees through "whether it is truly stable." So it can **tell good simplicity apart from degenerate simplicity** — for the same "simple and cheap," it can tell whether it is an individual with real substance or one that merely cowered. This is a feat ordinary evolutionary systems cannot pull off. This is the FullSense worldview —— "evolve not merely to be clever, but in a direction where one can prove it is cheap and safe."

## The honest breakdown: "the inspector makes it smart" was an overstatement

Finally, the story I cut the most today. In the experiment we had a result that "the stronger the gatekeeper, the smarter the AI gets (the better it predicts language)." We tried it 10 times and the trend held every time — a difference unlikely to arise by chance — and the numbers themselves are real. But before feeling like we'd won, we doubted the breakdown.

So we ran a control experiment. We shuffled the training text into a mess, destroying any meaningful order, so that there was "zero substance to learn." If the difference between gatekeepers arose "because it learned the language well," then in this condition with the substance removed, the difference should also vanish — that is what we predicted in advance.

Yet **the difference between gatekeepers did not vanish**. Even on meaningless strings, the stronger gatekeeper kept producing better scores. This means it was not "got smarter because it learned the language." The true cause of the difference was something unrelated to substance: "**ease of evolving (ease of moving)**." It is not about whether a good gene exists somewhere (the height of the ceiling), but about whether you can "walk up" to it through repeated mutation.

There is a clinching check too. When we optimized hard with gradients — instead of evolution (random mutation and selection) — **the result was the same for every gatekeeper**. So the benefit of a strong gatekeeper is "limited to evolution," not a lift to learning itself.

It is not a defeat. **Doubt the breakdown before you feel like you've won** —— this is the very core of FullSense research ([feedback_benchmark_honest_disclosure]). In exchange for throwing away the flashy headline ("the inspector makes the AI smart"), we kept a more accurate, plainer finding: "the inspector's payoff is not learning but evolvability." Plain, but we keep the one that is correct.

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

「进化中的 AI」乍一听可能没什么概念。这里说的「进化」，接近家畜的选育。我们造出许多个微小的 AI 个体，让它们繁殖出设置略有改动的后代，只把「做得好的」留给下一代 —— 如此重复几百代。没有人手把手去设计聪明个体，但越来越聪明的个体会渐渐冒出来。

可是在变聪明的路上，也混进了危险的孩子：它的「状态」（计算过程中携带的一堆数值）会随着世代不断膨胀、停不下来。本文把这叫做 **失控**。反过来，那些微小偏差会随时间自然缩小的个体则是稳定的（专业上叫「收缩」）。把失控的孩子留在群里，后面的世代会跟着一起坏掉。

于是，在进城之前设一道 **关卡**，让守门人一个一个确认「这个个体会不会失控？」这就是本文的主角 —— **检查器**。它是个一个失控个体都不放过的、非常认真的守门人。

可这位守门人的确认方式过分一板一眼。请把城（= AI 的状态）想象成有 n 个「房间」。守门人想检查每个房间状态摆得最厉害时的「角」。麻烦在于，每个房间的「角」有两端两种，而他要把全部 n 个房间的组合都试一遍。这跟试遍 n 个开关的 ON/OFF 全部模式一样，组合数是 **2ⁿ 种**。

数字看着就发憷。房间 8 个的话是 2⁸ = 256 种 —— 还行。可每多加 1 个房间，要检查的工作量就 **翻一倍**。于是 16 个是 65,536（六万多）种，32 个是 **43 亿** 种。从 8 个到 16 个不是「2 倍」，而是「256 倍」。一旦想把它养到昆虫脑子那点规模 —— 对 AI 来说还很小 —— 守门人自己反而先累垮了。

所以「没法把 AI 养得更大」这堵墙的真面目，既不是聪明程度的极限，也不是基因的数量，而是 **守门人（检查器）的工作量相对房间数呈指数级沉重**。这就是「进化天花板」。

## 做了什么：不走遍所有角，而是把房间「一眼望尽」

于是我们想到：不再一个一个走遍角，而是把整个房间一眼估算出来。打个比方，与其拿着卷尺把每个角落量一遍，不如站在门口一眼把天花板估出来：「这房间再乱，顶多也就这么大。」要走的角从 2ⁿ 种降到一次估算，便宜得不是一个量级。

不过，估算的做法是有讲究的。

- **最初的朴素估算（B1）**：往安全一侧倒，结果 **太过谨慎**。它把房间的「平均形状」和「摆动幅度」分别按最坏估算再加起来，于是最坏被算了两遍，看上去比实际危险得多。结果连本来无害的个体也吃了闭门羹，能进城的只有收缩（稳定）个体的三成。这比最便宜的守门人还严，本末倒置，一度沮丧地认为「便宜的一眼望尽果然不行」。
- **改了估算做法的版本（B2 = 用绝对值从上面压住）**：不再把摆动幅度单独算，而是「用绝对值从上面整体压住」。这一招中了。**律己的守门人会放行的人里，近八成（77.6%）只用一眼望尽 1 次就放行了**。再加上便宜的守门人（∞ 范数）当第二双眼睛，可达 87%。速度在房间 16 个时为 **1 万 2 千倍**。律己守门人花上几秒的活，几乎一瞬间就完成。

这里最要紧的是：**漏放（假阳性）为零**。一眼望尽的守门人说「放行」时，只放真正安全的个体，一次也没有粗心放过危险个体。代价是，有些安全的个体被他保险起见挡下了。但这个方向的错误是可以接受的 —— 关卡的职责是保障安全，「太严」尚可忍受，「太松、放走失控」却绝不允许。一眼望尽保住了「说放行就一定对」这个安全侧性质（专业上称健全性），只赚了速度。

教训很清楚：并不是「便宜的一眼望尽」本身不好，而是 **最初的估算做法太笨拙** 罢了。而且我们能在几秒内弄明白，正是因为在从头做沉重的正规装置（SDP）之前，先用小实验廉价地试了一下。在把规格做大之前先廉价地确认骨架 —— 正是这个顺序救了时间。

## 另一个发想：仿照「会断舍离的生物」

生物会把不需要的东西一个个舍弃、变得简单。住在漆黑洞穴里的鱼舍弃眼睛，靠依附别的生物过活的寄生虫舍弃自己的基因，深海的细菌削减基因组让自己变轻。为什么舍弃反而更划算？眼睛也好、基因也好，光是持有就要付维持成本（能量、复制的工夫）。在没有光的洞穴里眼睛毫无用处，却照样收维持费，那么舍弃它的个体更容易存活。**若「维持费 > 有用度」，那么简单的一方存活** —— 这是生物世界冷酷的规则。

我们想把这个也放进 AI 的进化里。现在我们只凭「性能好不好」来挑个体。如果在打分里再加上「**能廉价验证的简单身体**」这一视角，AI 应该不用人教，就会自己朝着守门人一眼就能放行的轻装结构前进。这就是把成本之低本身变成「进化的选择压」的发想。

不过这里有个坑，因为「简单」分成我们必须分辨的几种。

- **好的简单** = 身体构造本身就简单（真的轻）。验证便宜，进化也容易动。非常欢迎。
- **坏的简单①** = 因为守门人太严，结果留下个什么都不学的「伪优等生」（= 最便宜的 ∞ 守门人的陷阱）。看上去安全，其实只是缩着不动。
- **坏的简单②** = 退化成「什么都不说」的个体（= 只回最无难的非答案、黏在 unigram 上的状态）。安全又便宜，但无能。跟削减过头、再也无法自食其力的寄生虫一样。

也就是说，如果天真地奖励「只要便宜就好」，AI 就会偷懒往退化那头逃。所以性能与成本不能简单相加（标量化），而必须当作两者的权衡（帕累托）来处理。

幸好 llcore 有一双能看穿「是否真的稳定」的眼睛（健全性 oracle）。所以它 **能分辨好的简单与退化的简单** —— 同样是「简单又便宜」，它能分清是真有内容的个体，还是只缩着不动的个体。这是普通进化系统办不到的本事。这正是 FullSense 的世界观 —— 「不只是聪明，而是朝着能证明自己廉价、安全的方向进化」。

## 诚实的内幕：「检查器让 AI 变聪明」说过头了

最后，讲今天削减得最多的那段。实验里曾出现「守门人越强，AI 越聪明（语言预测越好）」的结果。试了 10 次，每次趋势都一样 —— 这种差异很难是偶然 —— 数字本身是真的。但在自以为赢之前，我们怀疑了它的内幕。

于是做了对照实验。我们把训练用的文章打乱成一团，破坏掉有意义的顺序，让「要学的内容为零」。如果守门人之间的差异是「因为把语言学好了」才产生的，那么在这个抽掉内容的条件下，差异也应该消失 —— 这是我们事先的预测。

然而 **守门人之间的差异并没有消失**。即便是毫无意义的字符串，强守门人依旧持续给出更好的分数。这说明并不是「学会了语言才变聪明」。制造差异的真身，是与内容无关的「**易进化性（容易动起来）**」。问题不在于好基因是否存在于某处（天花板的高度），而在于能否通过反复变异「一步步爬上去」。

还有一记定音的确认。当我们不用进化（随机变异与选择），而用梯度狠狠优化、学习时，**无论哪个守门人结果都一样**。可见强守门人的好处「仅限于进化时」，并没有把学习本身整体抬高。

这不算输。**在自以为赢之前先怀疑内幕** —— 这才是 FullSense 研究的核心（[feedback_benchmark_honest_disclosure]）。我们舍弃了华丽的标题（「检查器让 AI 变聪明」），换来的是一个更准确、更朴素的发现：「检查器的效用不是 learning 而是 evolvability」。朴素，但我们留下正确的那个。

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

"진화하는 AI"라고 해도 선뜻 와닿지 않을 수 있다. 여기서 말하는 "진화"는 가축의 품종 개량에 가깝다. 작은 AI 개체를 잔뜩 만들어, 설정을 조금씩 바꾼 자손을 자꾸자꾸 낳고, 그중 "잘 만들어진 녀석"만 다음 세대에 남긴다 —— 이것을 수백 세대 반복한다. 아무도 손으로 똑똑한 개체를 설계하지 않는데도, 점점 똑똑한 개체가 자라난다.

다만 똑똑해지는 길에는 위험한 녀석도 섞인다. AI의 "상태"(계산 도중에 들고 있는 수치 덩어리)가 세대를 거듭할수록 점점 부풀어 멈추지 않는 개체다. 본문에서는 이것을 **폭주**라고 부른다. 반대로, 사소한 어긋남이 시간이 지나면서 자연히 작게 줄어드는 개체는 안정되어 있다(전문적으로는 "수축한다"고 한다). 폭주하는 녀석을 무리에 남기면 뒷세대째 망가진다.

그래서 성 안으로 들어가기 전 **관문(關所)**을 두고, "이 개체는 폭주하지 않는가?"를 하나하나 확인하는 문지기를 세운다. 이것이 본문의 주역, **검사기**다. 폭주하는 개체를 한 마리도 놓치지 않는, 아주 성실한 문지기다.

그런데 이 문지기, 확인하는 방식이 지나치게 깐깐해서 곤란하다. 성(= AI의 상태)에는 "방"이 n개 있다고 생각해 보자. 문지기는 각 방의 상태가 가장 크게 흔들렸을 때의 "모서리"를 조사하고 싶어 한다. 골치 아픈 건, 방마다 "모서리"가 끝과 끝 두 가지씩 있고, n개 방 전부의 조합을 다 시험한다는 점이다. 이는 n개의 스위치 ON/OFF 모든 패턴을 시험하는 것과 같아서, 조합은 **2ⁿ 가지**가 된다.

숫자로 보면 아찔하다. 방이 8개라면 2⁸ = 256가지로 끝난다. 그런데 방을 1개 늘릴 때마다 조사하는 수고가 그때마다 **두 배**가 된다. 그래서 16개면 65,536(6만 초과)가지, 32개면 **43억 가지**. 8개에서 16개는 "2배"가 아니라 "256배"다. 곤충의 뇌 정도 —— AI로 보면 아직 작은 —— 규모로 키우려는 순간, 문지기 쪽이 먼저 과로로 쓰러진다.

즉 "더 이상 AI를 크게 키울 수 없다"는 벽의 정체는, 똑똑함의 한계도 유전자의 수도 아니라, **문지기(검사기)의 수고가 방의 수에 대해 지수적으로 무거워지는** 것이었다. 이것이 "진화의 천장"이다.

## 한 일: 모서리를 전부 걷지 않고, 방을 "한눈에" 본다

그래서 떠올린 것이, "모서리를 하나하나 걷는 것을 그만두고, 방 전체를 한눈에 어림한다"는 방법이다. 비유하자면, 방 구석구석을 줄자로 재며 도는 대신, 입구에 서서 "이 방이라면 아무리 어질러져도 이 정도겠지" 하고 한눈에 천장을 어림하는 감각에 가깝다. 걸어야 할 모서리가 2ⁿ 가지에서 1회 어림으로 줄어드니, 비교가 안 될 만큼 싸다.

다만 어림에는 만드는 요령이 있었다.

- **처음의 소박한 어림 (B1)**: 안전 쪽으로 기운 결과, **너무 신중했다**. 방의 "평균적인 형태"와 "흔들림 폭"을 따로따로 최악값으로 어림해 더했기 때문에, 최악이 두 번 얹혀 실제보다 훨씬 위험해 보였다. 그 결과 무해한 개체까지 문전박대해, 성에 들인 것은 수축(안정) 개체의 고작 3할. 이는 가장 싼 문지기보다 엄격하다는 본말 전도라, 일단 "싼 한눈에 보기는 역시 안 된다"고 낙담했다.
- **어림을 만드는 방식을 바꾼 버전 (B2 = 절댓값으로 위에서 누른다)**: 흔들림 폭을 따로 잡지 않고, "절댓값으로 위에서 통째로 누른다"는 방식으로 바꿨다. 이것이 정답이었다. **깐깐한 문지기가 통과시키는 사람의 8할 가까이(77.6%)를, 단 1회의 한눈에 보기로 통과시켰다**. 게다가 싼 문지기(∞노름)와 두 번째 눈으로 함께 보면 87%까지 닿는다. 속도는 방 16개일 때 **1만 2천 배**. 깐깐한 문지기가 수 초 걸리던 일이 거의 한순간에 끝난다.

여기서 가장 중요한 건, **놓침(위양성)이 제로**였다는 점이다. 한눈에 보는 문지기는 "통과"라고 하면 정말 안전한 개체만 통과시키고, 위험한 개체를 깜빡 통과시키는 일은 한 번도 없었다. 대신, 안전한데도 혹시 몰라 막아 버리는 취사가 있다. 하지만 이 방향의 실수라면 용서가 된다 —— 관문의 역할은 안전 확보이고, "너무 엄격한" 것은 참을 수 있어도 "물러서 폭주를 통과시키는" 것은 용납되지 않기 때문이다. 한눈에 보기는 "통과라고 하면 반드시 옳다"는 안전 쪽 성질(전문적으로는 건전성)을 지킨 채, 속도만 벌었다.

교훈은 명쾌하다. "싼 한눈에 보기" 자체가 나빴던 게 아니라, **처음의 어림을 만드는 방식이 서툴렀을 뿐**. 게다가 이를 수 초 만에 알 수 있었던 건, 무거운 본격 장치(SDP)를 처음부터 만들기 전에 작은 실험으로 싸게 시험해 봤기 때문이다. 사양을 크게 부풀리기 전에 뼈대만 싸게 확인한다 —— 이 순서가 시간을 구했다.

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
