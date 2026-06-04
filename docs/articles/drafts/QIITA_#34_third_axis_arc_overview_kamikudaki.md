---
title: "【かみくだき版】"選り分けて育てる工夫" はいつ役立つ? を山登り 6 連戦 + 蛾と大腸菌のたとえで (llcore 第三軸 arc 全体)"
tags: ["かみくだき", "進化計算", "山登り", "進化生物学"]
private: true
updated_at: "2026-06-02"
id: 5a1124083298fdbcb9e6
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# (連載 #34 かみくだき版) 山登り 6 連戦と、暗くなった蛾・新しい力を得た大腸菌の話

この記事は、ちょっと難しい研究の話を **中学生でも分かる言葉だけ** で説明します。専門用語が出てきたら、すぐ「山登り」や「生き物」のたとえに言い換えます。

連載 #33 のかみくだき版では「最後の決着」を説明しました。この #34 では、そこに **たどり着くまでの 6 つの実験ぜんぶ**を 1 つの物語として並べます。さらに今回は、**100 年近く前の生き物の研究が、私たちと同じ答えを出していた**という話をします。

---

## まず、何をやっている研究なの?

私たちは「AI の頭脳の部品を、生き物の進化のように少しずつ作り変えて、賢い部品を探す」研究をしています。プロジェクトの名前は **llcore (エルコア)** です。

生き物の進化には、教科書的に 4 つの要素があります (研究では番号で呼びます)。

- ① **変異** … 設計をちょっと変えてみる
- ② **遺伝** … 親の設計が子に引き継がれる
- ③ **適者生存・分離** … 良いものを選んで残す ← **今日の主役**
- ④ **過剰繁殖** … たくさん子どもを作る

今日の話は、③ を **「いろんなタイプを選り分けて、それぞれ別の場所で育てる」**という凝った工夫にしたとき、それが **本当に役に立つのか?** という問いです。

---

## 山登りのたとえ (おさらい)

設計の「良さ」を **地形の高さ**で表します。**高い場所 = 良い設計**。一番高い頂上を探すゲームです。

**なだらかな一つ山 (かんたん)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

これは **今より少し高い方へ歩くだけ** (山登り法) で頂上に着きます。**凝った工夫 (③) は要りません**。

**だまし地形 (むずかしい)**

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

手前に「ニセ頂上」があって、谷を渡った先に「本物の頂上」がある。素朴な山登りは **ニセ頂上で止まります** (谷を下れないから)。

ここで効くのが ③ です。**いろんなタイプの登山者を谷のあちこちに残しておく**と、誰かが谷を「飛び石」で渡って本物の頂上に着ける。これを研究では「記憶の宮殿 (MAP-Elites)」と呼びます。

> **一番大事なポイント**: ③ が役立つのは **「だまし地形」のときだけ**。なだらかな一つ山なら素朴な山登りで十分。

だから問いはこうです。

> **AI の設計を探すとき、出てくる地形は「だまし地形」なの? それとも「なだらかな一つ山」なの?**

— ここで一息。たとえはこれで全部。あとは 6 連戦の実録です。 —

---

## 6 連戦を一望する地図

先に地図を出します。これが背骨です。

| 戦 | どんな地形を測ったか | ③ は効いた? | 一言 |
|---|---|---|---|
| **1** | わざと作った「だまし地形」 | **Yes (圧勝)** | ③ は本物だと証明 |
| **2** | 記憶テスト / 部品を複数つなぐ | **測れず** | 地形が簡単すぎ/難しすぎで測定不能 |
| **3** | いろんなタスクへの応用力 | **No** | ③ は「選択なし」には勝つが、それ以上ではない |
| **4** | 実物そっくりの地形 (道具のブレをゼロに) | **No** | 地形が**本当になだらか**と確定 |
| **5** | 部品を 4 種類混ぜる抜け道 | **No** | サイコロで全部ひけるので**ふさがっていた** |

物語はこうです。**まず「だまし地形なら③は圧勝する」と証明し (1)、では実物ではどうかと 4 回測りに行ったら (2〜5)、実物に近い地形はぜんぶ "③が要らない地形" だった**。しかも最後 (4, 5) で「要らない理由」が **測り方が雑だからではなく、地形が本当に簡単だったから**と確定した。これが今日の弧 (アーク) です。

---

## 第1戦: わざと「だまし地形」を作ったら、③ が圧勝

最初に「③ が **理屈どおり効く場面が本当にあるか**」を証明しました。地形を **わざと意地悪に作って**、③ を素朴な方法 (とくに「ふりだしに戻ってやり直すランダムリスタート山登り」) と勝負させたのです。

結果は **③ の圧勝**。③ だけが本物の頂上に約 95% で到達し、ほかの方法は全部ニセ頂上で止まりました (勝率 100%、効果は理論上の最大)。

→ **③ は、ちゃんと役に立つ本物の仕組み**だと分かりました。

ただし正直に言うと、**わざと意地悪に作った地形**での話です。「③ は可能」と証明しただけで、「実物の地形もこんなに意地悪」とは言っていません。だから次の 4 戦は、実物に近い地形で確かめる旅でした。

— 一服。第1戦は気持ちのいい圧勝。ここから雲行きが…。 —

---

## 第2戦: 地形が簡単すぎ/難しすぎて、測れなかった

実物の記憶テストで測ろうとしたら、**地形が両極端**でした。

- あるテストは **難しすぎて誰も登れない** (全員ふもとで足踏み)。
- 別のテストは **簡単すぎて全員が頂上**(差がつかない)。

どちらも「③ が効くか」を比べられない = **測定不能**。部品を複数つないでも、この壁 (5 ビットのパリティという計算が原理的にこの方式では解けない) は越えられませんでした。

ここで 1 つ大事な気づき。**地形が遺伝子のレベルでデコボコでも、それは "③ で渡るべきだまし地形" とは違う**。後でこの区別が効いてきます。

— 小休止。「測れなかった」は地味ですが、地図の空白地帯として大事です。 —

---

## 第3戦: いろんなタスクへの応用力 — ③ は要らなかった

次は「習っていない長さの問題にも応用できるか」(応用力) で測りました。

結果: ③ は **「選択をまったくしない方法」には勝った**けれど、**ふつうに選択する方法 (ただし選り分けはしない) には勝てず**、サイコロ任せ (random) にも勝てませんでした。

つまり「③ ならではの工夫 (選り分け)」の効果は無かった。この地形は **なだらかで、ふつうの方法でも同じところに着いた**のです。

正直な話: 別の AI (Codex) が最初「この結果は信用できない」と言って、3 つの直しを要求しました。でも **直しても結論は変わりませんでした**。「直したら変わる脆い結果」ではなかった、というのが収穫です。

— 一服。負けは負けですが、「正しく負けた」と確かめる方が時間がかかりました。 —

---

## 第4戦: 道具のブレをゼロにしたら、地形は「本当になだらか」だった

ここが物語の転回点です。第3戦まで「③ は要らない」が続いたけれど、**しこり**が残っていました。

- (A) 地形が本当に **なだらか**だから ③ が要らないのか?
- (B) それとも **測り方が雑**で、谷があっても見えなかっただけ?

これを取り違えると「③ は無力」と言い過ぎてしまう。

そこで **測る道具のブレを物理的にゼロにする**工夫をしました。揺れる船を止めてから身長を測るイメージです。結果はこう。

| 測った地形 | 谷の割合 | 判定 |
|---|---|---|
| 実物に近い地形 (小) | **0% (谷なし)** | なだらか → ③ 要らない |
| 実物に近い地形 (大) | 約 10% (ごく浅い) | ほぼなだらか → ③ 要らない |
| わざと作った「でこぼこ」(テスト用) | 70〜80% | ちゃんと「でこぼこ」と検出 ✓ |
| わざと作った「なだらか」(テスト用) | 0% | ちゃんと「なだらか」と検出 ✓ |

大事なのは **測る道具そのものは正しく働いている**こと。だから「実物がなだらか」は道具のバグではなく、**地形が本当になだらか**だった。

→ **「③ が要らなく見えたのは、地形が本当になだらかだったから」**がハッキリしました。

(正直な注意: 「完璧にツルツル」ではなく「ごく浅い谷 (2〜4%) がぎりぎりある」くらいです。そこは丸めずに書いておきます。)

— 深呼吸。実物もどきは「なだらか」と確定。残るは「最後の抜け道」。 —

---

## 第5戦: 部品を 4 つ混ぜる抜け道 — サイコロで全部ひけてしまった

大きな計算機 (GPU) はお金がかかるので、すぐ手を出したくない。そこで **部品 (kernel) を 4 種類混ぜる**という別の手を試しました。

ねらい: 1 種類だと地形がなだらかでも、**4 種類を切り替える瞬間に段差 (谷) ができて「だまし地形」になるかも**。そうなれば ③ の出番ができるかも。

結果: **この抜け道はふさがっていました**。しかも「たまたま」ではなく **「もともと通れない作り」**でした。

なぜか。たとえで言うと、

> **部品を 4 つから選ぶのは、登山者がふりだしに戻る (リスタート) たびに、サイコロを振って 4 つから 1 つ試すようなもの。**

素朴な山登りの登山者は、行き止まったらリスタートします。部品は **4 つしかない**ので、何回かリスタートすれば **4 つ全部を直接ためせてしまう**。谷を渡らなくても、サイコロで本物の頂上を **直接ひける (ワープ)**。

そうなると ③ (谷を渡る工夫) の出番がありません。**渡るべき谷がそもそも無い**から。

別の角度 (敵対チェック) からも何度も叩きましたが、ふさがり方は崩れず、むしろ「サイコロで全部ひけるから③の出番がない」が確かになりました。

> **③ が活きるのは、選択肢が "直接ためせないほど膨大" なときだけ**。部品 4 つでは少なすぎた。

(正直な注意: 部品の 1 つ「hopfield」は簡易版で本調子じゃなかった、という弱点は残っています。それでも結論は変わりません。)

---

## 6 戦をまとめる「たった 1 つの条件」

6 つの結果は、たった 1 つの条件でぜんぶつながります。

> **③ が役立つのは、「難所」が "直接ためせないほど膨大 (高次元)" なときだけ。**

- 第1戦が圧勝したのは、本物の頂上が **サイコロでは一生かかっても引けないほど膨大な組合せ**の先にあったから。
- 実物の地形 (4 戦・5 戦) は逆に **難所が小さい** (なだらか、または 4 択)。だからサイコロ (リスタート) で直接ワープできて、③ の出番が無かった。

だから「遺伝子レベルでデコボコ」(第2戦) でも十分ではない。大事なのは **"探索がたどり着くべきゴールの広さ"** なのです。

---

## ここからが今日の目玉: 100 年前の生き物の研究と同じだった

実は、**「多様性を保つ工夫は、狭い条件でだけ役立つ」**という私たちの結論は、100 年近く前の生き物の研究にそっくりの先例があります。

> ⚠ 大事な注意: 生き物の話は **「たとえ話」であって、私たちのコンピュータ実験を証明するものではありません**。たとえがぴったり合わない所は正直に書きます。

### ライトの「みんなで散らばって谷を渡る」作戦

生物学者の **ライト (1931・1932 年)** はこう考えました。大きな「一つの群れ」のままだと、目の前の小さな丘で止まってしまう。もっと高い山に行くには一度「谷」を下らないといけないのに、ふつうの自然淘汰は「下る」を許さないから。

ライトのアイデアは **群れを小さなグループにバラバラに分ける**こと。

1. 小さなグループが偶然フラフラ動いて、たまたま谷を渡る。
2. そこからふつうの淘汰で別の山を登る。
3. 高い山に登れたグループの良い遺伝子が、群れ全体に広がる。

これが **シフティング・バランス (移り変わるバランス)**。「散らばっておくと誰かが谷を渡れる」── まさに私たちの ③ (MAP-Elites) とそっくりです。

> 正直な注意: これは「似ている」という *たとえ話*。MAP-Elites を作った人がライトを真似たわけではありません (論文も引用していない)。

### でも「いつも必要」ではなかった

ライトと同時代の **フィッシャー (1930 年)** は逆を言いました。「大きな群れのまま、ふつうの淘汰だけで十分。わざわざ散らばらなくていい」。

二人の一番深い対立は **「地形がデコボコ (山がたくさん) か、なだらか (山が一つ) か」**でした。ライトは「デコボコだから谷を渡る作戦がいる」、フィッシャーは「だいたいなだらかだから、ふつうの淘汰でいい」。

そして後の生物学者 **コイン・バートン・トゥレリ (1997 年)** が、ライトの作戦を本気で検証してこう結論しました。

- **ふつうの自然淘汰だけでたいてい説明できる**。ライトの作戦でしか説明できない実例はほとんど無い。
- **ライトの作戦が効くのは、深い谷があるすごく特別なときだけ**。現実の谷はたいてい浅くて、そもそも谷を渡らなくても進化できることが多い。

これが **私たちの結果とそっくり**。私たちも「地形が本当になだらかなら ③ は要らない、単純なやり方で十分」と分かりました。コインたちの「現実の地形はたいてい単純」は、私たちの **負の結果 (③ は要らなかった) の生物学版**です。

> 正直な注意 (3 つ):
> - コインたちは「ライトは絶対あり得ない」とは言っていない。「一般的・重要とは言えない」と言っただけ。論争はまだ決着していません。
> - だから「ライトは間違い」と書いてはいけません。
> - しかも生き物では「散らばる作戦」がときに **逆効果**になる (良い遺伝子が小さなグループに閉じ込められて広がらない)。私たちのコンピュータにはこれに当たるものが無い ── ここはたとえがずれる所で、生き物の方が一段強い主張をしています。

### たとえ①: 暗くなった蛾 (ひくい次元 = ふつうの淘汰で十分)

イギリスの **オオシモフリエダシャク** という蛾の話。工場の煙で木が黒くなった時代、白い蛾は鳥に食べられやすく、黒い蛾が増えた。空気がきれいになると、また白い蛾が増えた。

この「黒/白」は **たった一つの遺伝子のスイッチ**で決まり、選べる色は実質 2〜3 種類だけ = **とても単純 (低次元)**。鳥に食べられにくい色がそのまま生き残るだけ (ふつうの強い淘汰)。**散らばる作戦 (③) は要らないし、誰も使っていない**。

これは私たちの **第5戦「部品 4 種を混ぜる」とまったく同じ**。部品は 4 択 = 低次元だから、サイコロで全部直接ためせてしまう。③ の出番がない。**暗くなった蛾 = 部品 4 択の話の生き物版**です。

> 正直な注意: 色がしばらく混ざる時期もあるが、それは「場所で環境が違う + 移動」のせいで、③ のような多様性保存のおかげではありません。たとえが少しずれる所。

### たとえ②: 新しい力を得た大腸菌 (高い次元 = 歴史と多様性が効く)

レンスキーという研究者の **大腸菌の超長期実験**。同じ大腸菌を 12 グループに分けて 1988 年からずっと育てた。あるとき **12 グループのうち 1 つだけ**が、それまで使えなかった「クエン酸」を酸素のある環境で食べる新しい力を手に入れました (3 万 1500 世代目)。

大事なのは、それが **「いきなり」ではなく「前もって別の変化が積み重なっていた特定のグループでだけ」起きた**こと。順番に変化が積み重ならないとたどり着けなかった = **高次元で歴史に依存する複雑な地形**の本物の例。**③ が効きうる側のたとえ**です。

> 正直な注意: これは「③ というアルゴリズムが勝った」証明ではありません。ただの自然の実験で、③ の仕組みは使っていない。しかも 12 グループに分けたこと自体が「ふりだしに戻ってやり直す」のに似ている。だから「散らばる作戦が一番だった」とまでは言えません。あくまで「複雑な地形では多様性が効きうる」というイメージ。

— 一服。100 年前の論争が同じ形だと気づいたときはゾクッとしました。でも「ゾクッ」を「証明」と取り違えないのが今日の規律です。 —

---

## で、GPU を借りるべき?

ここまでをまとめると、

- **私たちが試した CPU の地形は、ぜんぶ「なだらか」か「低次元の単純な選択」だった**。だから ③ は要らなかった (= 暗くなった蛾、フィッシャー、コインたちの側)。
- **③ が本当に効くのは「デコボコで高次元の地形」だけ** (= ライトのシフティング・バランス、レンスキーの大腸菌の側)。
- では「デコボコで高次元の地形」はどこにある? → **GPU で動かす本物の大規模 AI の地形** (ダイヤル数百万個 = まさに高次元) くらいしか残っていません。

だから「GPU を借りて本物の AI で ③ を試す」のは **ヤマ勘ではなく、ちゃんとした理由 (高次元でだけ ③ は意味を持つ) に沿った賭け**です。

ただし **やっぱり賭け**。本物の AI の地形も、勾配を使う強いやり方 (backprop) でスイスイ進めてしまうなら、結局 ③ は要らないかもしれない (部品 4 択でサイコロに勝てなかったのと同じリスク)。だからすぐ大金は出さず、クラウドを少し借りて 1 回ためす、という方針です。

---

## まとめ ── 一言で

たくさん書きましたが、結論はこの一行です。

> **③ (選り分けて育てる工夫) が役立つのは「高次元のだまし地形」のときだけ。今 CPU で測れた "実物もどき" の地形は、ぜんぶその条件を満たさなかった。**

だから「③ は要らないと判明した」ではありません。正しくは:

- だまし地形では ③ は本物 (圧勝した)
- 記憶テスト・応用力・実物もどき・部品 4 種、ぜんぶ条件を満たさず ③ は要らなかった
- 本当の実物 (本物の巨大 AI の地形、ダイヤル数百万個) はまだ測れていない ── それが本丸で、しかも「やってみる価値のある賭け」
- そしてこの結論の骨組みは、**100 年前の生き物の研究 (ライトとコインたち) が既に描いていた** ── ただし生き物の話は **証明ではなく、たとえ (接地)**

そして今日いちばん伝えたいこと。

> **「うまく行きすぎた結果は、勝ちではなく警報」**。
> 自分の結果を疑う仕組みを先に置いておいたから、ぬか喜びを避けて、正しい土台にたどり着けた。

正直であること自体が、研究を前に進める力になる ── そういう 6 連戦でした。

---

**この記事の技術版**: 連載 #34「山登り 6 連戦で分かった "いつ進化の③は効くのか" — そして 100 年前の進化生物学が同じ答えを出していた」(同じフォルダ内)

---

# English

# (Series #34, Plain-Language Edition) Six Hill-Climbing Bouts, the Moth That Turned Dark, and the E. coli That Gained a New Power

This article explains a slightly difficult research story using **only words a middle-schooler can understand**. Whenever a technical term shows up, we immediately rephrase it as a "hill-climbing" or "living-creature" analogy.

The plain-language edition of Series #33 explained "the final showdown." This #34 lines up **all six experiments that led there** as a single story. And this time we add another point: **research on living creatures from nearly 100 years ago had already reached the same answer we did**.

---

## First, what is this research even about?

We are doing research on "remaking the parts of an AI's brain little by little, like the evolution of living things, to search for smart parts." The project is named **llcore**.

The evolution of living things, as taught in textbooks, has four ingredients (in our research we call them by number).

- (1) **Mutation** … try changing the design a little
- (2) **Heredity** … the parent's design is passed on to the child
- (3) **Survival of the fittest / separation** … pick the good ones and keep them ← **today's main character**
- (4) **Overproduction** … make lots of offspring

Today's story is about this question: when we turn (3) into the elaborate trick of **"sorting out various types and raising each one in a separate place,"** is it **actually useful?**

---

## The hill-climbing analogy (recap)

We represent the "goodness" of a design by the **height of the terrain**. **High place = good design**. It's a game of searching for the single highest summit.

**A single gentle hill (easy)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

For this one, you reach the summit just by **walking toward whatever is a little higher than where you are now** (the hill-climbing method). **No elaborate trick (3) is needed.**

**Deceptive terrain (hard)**

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

There's a "fake summit" up front, and beyond a valley lies the "real summit." Naive hill-climbing **stops at the fake summit** (because it can't walk down into a valley).

This is where (3) shines. If you **keep various types of climbers scattered all over the valley**, someone can cross the valley by "stepping stones" and reach the real summit. In research we call this the "memory palace (MAP-Elites)."

> **The single most important point**: (3) is useful **only when the terrain is "deceptive."** For a single gentle hill, naive hill-climbing is enough.

So the question is this.

> **When we search for an AI design, is the terrain that shows up "deceptive terrain"? Or is it "a single gentle hill"?**

— A breather here. That's all the analogies. The rest is the actual record of the six bouts. —

---

## A map that surveys all six bouts at once

Let's put up the map first. This is the backbone.

| Bout | What kind of terrain we measured | Did (3) work? | In a word |
|---|---|---|---|
| **1** | Deliberately built "deceptive terrain" | **Yes (landslide win)** | (3) is proven to be the real deal |
| **2** | Memory test / chaining multiple parts | **Couldn't measure** | Terrain too easy/too hard, measurement impossible |
| **3** | Generalization power to various tasks | **No** | (3) beats "no selection," but is no better beyond that |
| **4** | Terrain just like the real thing (instrument jitter zeroed out) | **No** | Confirmed the terrain is **genuinely gentle** |
| **5** | A loophole of mixing 4 kinds of parts | **No** | A die can draw all of them, so **the hole was already closed** |

The story goes like this. **First we proved "if the terrain is deceptive, (3) wins by a landslide" (1); then we went to measure the real thing four times to ask "so what about reality?" (2-5), and every terrain close to the real thing turned out to be a "terrain that doesn't need (3)."** Moreover, in the last two (4, 5), we confirmed that the reason it isn't needed is **not that our measurement was sloppy, but that the terrain really was simple**. This is today's arc.

---

## Bout 1: When we deliberately built "deceptive terrain," (3) won by a landslide

First we proved whether there is **really a scene where (3) works as the theory says**. We **deliberately built nasty terrain** and pitted (3) against naive methods (especially "random-restart hill-climbing, which goes back to the start and tries again").

The result was a **landslide win for (3)**. Only (3) reached the real summit about 95% of the time, while all the other methods got stuck at fake summits (win rate 100%, the effect was the theoretical maximum).

→ We learned that **(3) is a genuine mechanism that really does work**.

To be honest, though, this is a story on terrain we **deliberately built to be nasty**. We only proved "(3) is possible"; we did not claim "the real terrain is this nasty too." So the next four bouts were a journey to verify on terrain close to the real thing.

— Take a break. Bout 1 was a satisfying landslide. From here, the weather starts to turn... —

---

## Bout 2: The terrain was too easy/too hard, so we couldn't measure

When we tried to measure on a real memory test, **the terrain was at both extremes**.

- One test was **too hard for anyone to climb** (everyone marking time at the foot).
- Another test was **too easy, so everyone reached the summit** (no difference shows up).

In both cases we **could not compare** "does (3) work" = **measurement impossible**. Even chaining multiple parts couldn't get over this wall (a computation called 5-bit parity that, in principle, this method cannot solve).

Here's one important realization. **Even if the terrain is bumpy at the gene level, that is different from a "deceptive terrain that (3) should cross."** This distinction pays off later.

— A short rest. "Couldn't measure" is plain, but it matters as a blank zone on the map. —

---

## Bout 3: Generalization power to various tasks — (3) wasn't needed

Next we measured by "can it apply even to problem lengths it wasn't taught?" (generalization power).

Result: (3) **beat "the method that does no selection at all,"** but **couldn't beat the ordinary method that does selection (just no sorting),** and couldn't beat leave-it-to-the-die (random) either.

In other words, there was no effect from "the trick unique to (3) (sorting)." This terrain was **gentle, and ordinary methods arrived at the same place**.

An honest aside: another AI (Codex) at first said "this result can't be trusted" and demanded three fixes. But **even after fixing, the conclusion didn't change.** What we gained was that it wasn't "a fragile result that changes once you fix it."

— Take a break. A loss is a loss, but it took more time to confirm "we lost correctly." —

---

## Bout 4: When we zeroed out the instrument's jitter, the terrain was "genuinely gentle"

This is the turning point of the story. "(3) isn't needed" kept holding through Bout 3, but a **lump of doubt** remained.

- (A) Is (3) unneeded because the terrain really is **gentle**?
- (B) Or was our **measurement just sloppy**, so that even if there were valleys, we couldn't see them?

If you mix these up, you overstate things into "(3) is powerless."

So we devised a way to **physically zero out the jitter of the measuring instrument**. Picture stopping a rocking ship before measuring someone's height. The result was this.

| Terrain measured | Fraction of valleys | Verdict |
|---|---|---|
| Terrain close to the real thing (small) | **0% (no valleys)** | Gentle → (3) not needed |
| Terrain close to the real thing (large) | About 10% (very shallow) | Almost gentle → (3) not needed |
| Deliberately built "bumpy" (for testing) | 70-80% | Correctly detected as "bumpy" ✓ |
| Deliberately built "gentle" (for testing) | 0% | Correctly detected as "gentle" ✓ |

The important thing is that **the measuring instrument itself is working correctly.** So "the real thing is gentle" is not a bug in the instrument — **the terrain really was gentle.**

→ It became clear that **"(3) looked unneeded because the terrain really was gentle."**

(An honest caveat: it's not "perfectly smooth" but more like "there are barely-there, very shallow valleys (2-4%)." We write that down without rounding it off.)

— Take a deep breath. The real-thing-imitation is confirmed "gentle." What's left is "the last loophole." —

---

## Bout 5: The loophole of mixing 4 parts — a die could draw them all

Big computers (GPUs) cost money, so we didn't want to reach for them right away. So we tried another hand: **mixing 4 kinds of parts (kernels)**.

The aim: even if the terrain is gentle with one kind, **maybe a step (valley) forms at the moment you switch among 4 kinds, turning it into "deceptive terrain."** If so, (3) might get its turn.

Result: **this loophole was already closed.** And not "by chance" — it was **"a structure that was impassable from the start."**

Why? In analogy terms,

> **Choosing a part out of 4 is like a climber rolling a die and trying 1 of 4 every time they go back to the start (restart).**

A naive hill-climbing climber restarts whenever they hit a dead end. Since there are **only 4 parts**, after a few restarts they end up **trying all 4 directly.** Without crossing any valley, they can **draw the real summit directly with a die (a warp).**

In that case, (3) (the trick of crossing valleys) has no turn. Because **there is no valley to cross in the first place.**

We also hammered at it many times from another angle (adversarial checks), but the "closed-ness" did not crack; if anything, "because a die can draw all of them, (3) has no turn" became more certain.

> **(3) comes alive only when the choices are "so vast you cannot try them directly."** Four parts were too few.

(An honest caveat: one of the parts, "hopfield," was a simplified version and not at full strength — that weakness remains. Even so, the conclusion does not change.)

---

## The "single condition" that ties all six bouts together

The six results all connect through a single condition.

> **(3) is useful only when the "hard spot" is "so vast you cannot try it directly (high-dimensional)."**

- Bout 1 was a landslide win because the real summit lay beyond **a combination so vast that a die could never draw it in a lifetime.**
- The real terrains (Bouts 4 and 5) conversely had a **small hard spot** (gentle, or 4 choices). So a die (restart) could warp directly there, and (3) had no turn.

That's why "bumpy at the gene level" (Bout 2) isn't enough either. What matters is **"how vast the goal that the search must reach is."**

---

## And now today's main event: it was the same as research on living creatures 100 years ago

Actually, our conclusion that **"the trick of preserving diversity is useful only under narrow conditions"** has a precedent in research on living creatures from nearly 100 years ago that looks remarkably similar.

> ⚠ An important caveat: the living-creature story is **"an analogy," and it does not prove our computer experiments.** Wherever the analogy doesn't fit perfectly, we'll write that honestly.

### Wright's "scatter out as a group and cross the valley" strategy

The biologist **Wright (1931, 1932)** thought this way. If you stay as one big "single herd," you stop at the little hill in front of you. To go to a higher mountain you must once go down into a "valley," but ordinary natural selection won't allow "going down."

Wright's idea was to **break the herd into small scattered groups.**

1. A small group drifts around by chance and happens to cross a valley.
2. From there, ordinary selection climbs a different mountain.
3. The good genes of the group that managed to climb the high mountain spread to the whole herd.

This is the **shifting balance.** "If you stay scattered, someone can cross the valley" — exactly like our (3) (MAP-Elites).

> An honest caveat: this is an *analogy* of "looking similar." The people who built MAP-Elites did not imitate Wright (their paper doesn't even cite him).

### But it wasn't "always necessary"

Wright's contemporary **Fisher (1930)** said the opposite. "Stay as one big herd; ordinary selection alone is enough. There's no need to go to the trouble of scattering."

The deepest disagreement between the two was **"is the terrain bumpy (many mountains) or gentle (a single mountain)?"** Wright said "it's bumpy, so we need the valley-crossing strategy"; Fisher said "it's mostly gentle, so ordinary selection is fine."

Then a later biologist, **Coyne, Barton, and Turelli (1997)**, seriously tested Wright's strategy and concluded as follows.

- **Ordinary natural selection alone explains most things.** There are almost no real cases that only Wright's strategy can explain.
- **Wright's strategy works only in the very special case of a deep valley.** Real valleys are mostly shallow, and often evolution can proceed without crossing any valley at all.

This is **strikingly like our own result.** We too found that "if the terrain really is gentle, (3) is unneeded; a simple method is enough." Coyne and colleagues' "real terrain is mostly simple" is the **biology version of our negative result ((3) wasn't needed).**

> An honest caveat (three of them):
> - Coyne and colleagues did not say "Wright is utterly impossible." They only said "it can't be called general or important." The debate is not yet settled.
> - So you must not write "Wright is wrong."
> - Moreover, in living creatures the "scattering strategy" can sometimes be **counterproductive** (good genes get trapped in a small group and don't spread). Our computer has no counterpart to this — here the analogy breaks down, and the living-creature side makes a one-step-stronger claim.

### Analogy 1: The moth that turned dark (low dimension = ordinary selection is enough)

The story of an English moth called the **peppered moth.** In an era when factory smoke blackened the trees, white moths were easily eaten by birds, and dark moths increased. When the air became clean, white moths increased again.

This "dark/white" is decided by **just a single gene's switch,** and the choosable colors are really only about 2-3 kinds = **very simple (low-dimensional).** The color that's harder for birds to eat simply survives (ordinary strong selection). **The scattering strategy (3) isn't needed, and nobody uses it.**

This is **exactly the same as our Bout 5, "mixing 4 kinds of parts."** With 4 choices for the part = low-dimensional, a die can try all of them directly. (3) has no turn. **The moth that turned dark = the living-creature version of the 4-choice-part story.**

> An honest caveat: there are periods when the colors mix for a while, but that's due to "different environments in different places + migration," not thanks to diversity preservation like (3). A spot where the analogy slips a little.

### Analogy 2: The E. coli that gained a new power (high dimension = history and diversity matter)

The researcher Lenski's **super-long-term experiment with E. coli.** He divided the same E. coli into 12 groups and raised them continuously from 1988. At one point, **only 1 of the 12 groups** acquired the new power to eat "citrate" in an oxygen-rich environment, which it previously couldn't (at the 31,500th generation).

The important thing is that it happened **not "suddenly" but "only in a specific group where other changes had piled up beforehand."** It couldn't be reached unless changes accumulated in order = a genuine example of **a complex, high-dimensional, history-dependent terrain.** It's an analogy on the side where **(3) could work.**

> An honest caveat: this is not proof that "the algorithm (3) won." It's just a natural experiment, and it doesn't use the mechanism of (3). Moreover, dividing into 12 groups itself resembles "going back to the start and trying again." So we can't go as far as "the scattering strategy was the best." It's only the image that "in complex terrain, diversity could work."

— Take a break. When I realized the 100-year-old debate had the same shape, it gave me chills. But not mistaking the "chill" for "proof" is today's discipline. —

---

## So, should we rent a GPU?

To sum up so far,

- **Every terrain we tested on CPU was either "gentle" or "a low-dimensional simple choice."** So (3) wasn't needed (= the side of the moth that turned dark, Fisher, and Coyne's group).
- **(3) really works only on "bumpy, high-dimensional terrain"** (= the side of Wright's shifting balance and Lenski's E. coli).
- So where is "bumpy, high-dimensional terrain"? → Pretty much only **the terrain of a genuine large-scale AI running on a GPU** (millions of dials = truly high-dimensional) remains.

So "renting a GPU and trying (3) on a real AI" is **not a hunch but a bet that follows a solid reason (only in high dimensions does (3) carry meaning).**

That said, it's **still a bet.** Even on a real AI's terrain, if a strong gradient-using method (backprop) glides smoothly along, (3) might end up unneeded after all (the same risk as failing to beat the die with 4-choice parts). So we don't spend big money right away; the plan is to rent a little cloud and try it once.

---

## Summary — in one line

We wrote a lot, but the conclusion is this one line.

> **(3) (the trick of sorting and raising separately) is useful only on "high-dimensional deceptive terrain." Every "real-thing-imitation" terrain we could measure on CPU failed to meet that condition.**

So it is not "we found out (3) is unneeded." Correctly:

- On deceptive terrain, (3) is the real deal (it won by a landslide)
- Memory test, generalization power, real-thing-imitation, 4 kinds of parts — none met the condition, and (3) wasn't needed
- The true real thing (a genuine huge AI's terrain, millions of dials) hasn't been measured yet — that's the main keep, and it's also "a bet worth making"
- And the skeleton of this conclusion was **already drawn by research on living creatures 100 years ago (Wright and Coyne's group)** — though the living-creature story is **not proof but an analogy (grounding)**

And the thing I most want to convey today.

> **"A result that goes too well is not a victory but an alarm."**
> Because we placed a mechanism to doubt our own results in advance, we avoided premature celebration and reached a correct foundation.

Being honest is itself a force that moves research forward — that's the kind of six bouts it was.

---

**The technical edition of this article**: Series #34 "Six Hill-Climbing Bouts Reveal 'When Does Evolution's (3) Work' — And 100-Year-Old Evolutionary Biology Had Already Given the Same Answer" (in the same folder)
