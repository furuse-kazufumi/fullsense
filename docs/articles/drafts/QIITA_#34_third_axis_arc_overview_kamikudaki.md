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

![山登り6連戦 — 選り分けて育てる工夫はいつ効く?](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q34k_4koma.svg)
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

![Six Hill-Climbing Bouts — When Does Sort-and-Raise Work?](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q34k_4koma_en.svg)
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

---

# 中文

![爬山六连战 — 选别培养的工夫何时有效?](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q34k_4koma_zh.svg)
# (连载 #34 通俗版) 爬山六连战，以及变黑的蛾子、获得新能力的大肠杆菌的故事

这篇文章用**只有中学生也能懂的词语**来讲一个有点难的研究故事。每当出现专业术语，我们立刻把它换成"爬山"或"生物"的比喻。

连载 #33 的通俗版讲了"最后的决战"。这篇 #34 把**到达那里之前的全部六个实验**串成一个故事。而且这次我们再加一点：**将近 100 年前的生物研究，早就得出了和我们一样的答案**。

---

## 首先，这到底是在研究什么?

我们在做的研究是"像生物进化那样，把 AI 大脑的零件一点一点改造，去寻找聪明的零件"。这个项目的名字叫 **llcore**。

教科书里讲的生物进化有四个要素 (在研究里我们用编号来称呼)。

- ① **变异** … 把设计稍微改一改
- ② **遗传** … 父代的设计传给子代
- ③ **适者生存・分离** … 挑出好的并留下 ← **今天的主角**
- ④ **过度繁殖** … 生很多后代

今天的故事就是这个问题：当我们把 ③ 变成**"把各种类型选别出来，分别在不同地方培养"**这种精巧的工夫时，它**真的有用吗?**

---

## 爬山的比喻 (复习)

我们用**地形的高度**来表示设计的"好坏"。**高处 = 好设计**。这是一个寻找唯一最高山顶的游戏。

**平缓的单峰 (简单)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

这种地形，**只要朝比现在稍高一点的方向走** (爬山法)，就能到达山顶。**不需要任何精巧的工夫 (③)。**

**骗人地形 (困难)**

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

前面有一个"假山顶"，越过一道山谷之后才是"真山顶"。朴素的爬山**停在假山顶上**(因为它没法往谷里走下去)。

这时候 ③ 就发挥作用了。如果你**把各种类型的登山者撒在山谷各处**，就会有人靠"踏脚石"渡过山谷、到达真山顶。在研究里我们把这叫"记忆宫殿 (MAP-Elites)"。

> **最重要的一点**：③ 只有在地形是"骗人地形"时才有用。如果是平缓的单峰，朴素爬山就够了。

所以问题是这样的。

> **当我们去寻找 AI 的设计时，出现的地形是"骗人地形"? 还是"平缓的单峰"?**

— 这里喘口气。比喻就到这儿。剩下的是六连战的实录。 —

---

## 一览六连战的地图

先把地图放出来。这是骨架。

| 战 | 测的是什么样的地形 | ③ 有效吗? | 一句话 |
|---|---|---|---|
| **1** | 故意造的"骗人地形" | **Yes (大胜)** | 证明 ③ 是真本事 |
| **2** | 记忆测试 / 把多个零件串起来 | **测不了** | 地形太简单/太难，无法测量 |
| **3** | 对各种任务的应用能力 | **No** | ③ 能赢"不做选择"，但仅此而已 |
| **4** | 跟实物一模一样的地形 (把工具的抖动归零) | **No** | 确定地形**真的平缓** |
| **5** | 把零件混 4 种的捷径 | **No** | 用骰子全都能抽到，所以**那条路本来就堵死了** |

故事是这样的。**先证明"如果是骗人地形，③ 会大胜"(1)，然后想知道"那实物呢"，就去测了四次 (2~5)，结果接近实物的地形全都是"不需要 ③ 的地形"。**而且在最后两战 (4、5)，我们确定了"不需要的理由"**不是因为测量粗糙，而是因为地形真的简单**。这就是今天的弧 (arc)。

---

## 第 1 战：故意造"骗人地形"，③ 大胜

最初我们证明了"③ **是否真有按理论生效的场景**"。我们**故意把地形造得刁钻**，让 ③ 跟朴素方法 (尤其是"回到起点重来的随机重启爬山") 较量。

结果是 **③ 大胜**。只有 ③ 以约 95% 到达真山顶，其他方法全都停在假山顶上 (胜率 100%，效果达到理论上的最大值)。

→ 我们弄清了 **③ 是个确实有用的真本事机制**。

不过老实说，这是在我们**故意造得刁钻的地形**上的故事。我们只证明了"③ 可行"，并没有说"实物地形也这么刁钻"。所以接下来四战，是去接近实物的地形上验证的旅程。

— 歇一下。第 1 战是痛快的大胜。从这里开始，天色开始变了…… —

---

## 第 2 战：地形太简单/太难，测不了

想用实物的记忆测试来测，结果**地形走了两个极端**。

- 有的测试**太难，谁都爬不上去** (所有人都在山脚原地踏步)。
- 另一个测试**太简单，所有人都到了山顶** (拉不开差距)。

两种情况都**无法比较**"③ 有没有用" = **无法测量**。即使把多个零件串起来，也越不过这堵墙 (一种叫 5 比特奇偶校验的计算，原理上这种方式无法解)。

这里有一个重要的领悟。**即使地形在基因层面凹凸不平，那也不同于"③ 该去渡的骗人地形"。**这个区分后面会发挥作用。

— 小憩。"测不了"听起来很平淡，但它作为地图上的空白地带很重要。 —

---

## 第 3 战：对各种任务的应用能力 —— 不需要 ③

接下来我们用"对没学过的长度的问题也能应用吗"(应用能力) 来测。

结果：③ **赢了"完全不做选择的方法"**，但**赢不了普通的做选择的方法 (只是不做选别)**，也赢不了听天由命 (random)。

也就是说，"③ 独有的工夫 (选别)"没有效果。这个地形是**平缓的，普通方法也到了同一个地方**。

老实说：另一个 AI (Codex) 一开始说"这个结果不可信"，提出了三处修改要求。但**改了之后结论也没变**。收获是它并不是"一改就变的脆弱结果"。

— 歇一下。输就是输，但确认"输得正确"花的时间更多。 —

---

## 第 4 战：把工具的抖动归零后，地形是"真的平缓"

这里是故事的转折点。到第 3 战为止"不需要 ③"一直成立，但心里留着一个**疙瘩**。

- (A) 是因为地形真的**平缓**所以不需要 ③?
- (B) 还是因为**测量粗糙**，就算有山谷也没看见而已?

如果搞混了，就会过头地说成"③ 无能"。

于是我们想了个办法，**把测量工具的抖动从物理上归零**。想象先把摇晃的船停稳，再量身高。结果是这样。

| 测的地形 | 山谷比例 | 判定 |
|---|---|---|
| 接近实物的地形 (小) | **0% (无谷)** | 平缓 → 不需要 ③ |
| 接近实物的地形 (大) | 约 10% (极浅) | 几乎平缓 → 不需要 ③ |
| 故意造的"凹凸"(测试用) | 70~80% | 正确地检测为"凹凸"✓ |
| 故意造的"平缓"(测试用) | 0% | 正确地检测为"平缓"✓ |

重要的是，**测量工具本身在正确工作**。所以"实物是平缓的"不是工具的 bug，而是**地形真的平缓**。

→ "**③ 看起来不需要，是因为地形真的平缓**"清楚地确定了。

(老实的提醒：不是"完美光滑"，而更像是"勉强存在极浅的山谷 (2~4%)"。这一点我们不四舍五入地写下来。)

— 深呼吸。仿实物确定是"平缓"。剩下的是"最后的捷径"。 —

---

## 第 5 战：把零件混 4 个的捷径 —— 用骰子全抽到了

大计算机 (GPU) 很花钱，不想立刻动手。于是我们试了另一招：**把零件 (kernel) 混 4 种**。

意图：单一种类时地形即使平缓，**在 4 种之间切换的瞬间也许会产生台阶 (山谷)，变成"骗人地形"。**那样的话 ③ 就有出场机会了。

结果：**这条捷径本来就堵死了**。而且不是"碰巧"，是**"本来就走不通的构造"**。

为什么? 用比喻来说，

> **从 4 个里选一个零件，就像登山者每次回到起点 (重启) 都掷一次骰子，从 4 个里试 1 个。**

朴素爬山的登山者，碰到死路就重启。零件**只有 4 个**，所以重启几次就会**把 4 个全都直接试过一遍**。不用渡谷，靠骰子就能**直接抽到真山顶 (瞬移)**。

这样一来，③ (渡谷的工夫) 就没有出场机会了。因为**根本就没有该渡的谷**。

我们也从另一个角度 (对抗性检查) 反复敲打过它，但"堵死"的状态并没有崩，反而"因为骰子能全抽到，所以 ③ 没有出场机会"变得更确定了。

> **③ 能发挥作用，只有在选项"多到无法直接逐个试"的时候**。零件 4 个太少了。

(老实的提醒：零件之一"hopfield"是简化版、没发挥全力，这个弱点还留着。即便如此结论也不变。)

---

## 把六战串起来的"唯一一个条件"

六个结果，靠唯一一个条件全都连起来。

> **③ 有用，只有在"难关"是"多到无法直接逐个试 (高维)"的时候。**

- 第 1 战大胜，是因为真山顶在**一个组合的尽头，那个组合大到骰子一辈子也抽不到**。
- 实物地形 (第 4、5 战) 反过来**难关很小** (平缓，或者 4 选 1)。所以骰子 (重启) 就能直接瞬移过去，③ 没有出场机会。

所以"基因层面凹凸不平"(第 2 战) 也不够。重要的是**"搜索该到达的目标有多大"**。

---

## 从这里开始才是今天的重头戏：和 100 年前的生物研究一模一样

其实，我们"保持多样性的工夫只有在狭窄条件下才有用"这个结论，在将近 100 年前的生物研究里有一个惊人相似的先例。

> ⚠ 重要提醒：生物的故事是**"比喻"，并不能证明我们的计算机实验**。比喻不完全吻合的地方，我们会老实写出来。

### 赖特的"大家散开去渡谷"战略

生物学家 **赖特 (Wright，1931、1932 年)** 是这么想的。如果一直是一个大"群体"，就会停在眼前的小丘上。要去更高的山，就得先下到一道"谷"，可普通的自然选择不允许"往下走"。

赖特的想法是**把群体拆成一个个小群**。

1. 小群偶然到处晃动，碰巧渡过了山谷。
2. 从那里用普通的选择去爬另一座山。
3. 爬上高山的那个群的好基因，扩散到整个群体。

这就是**渐变平衡 (shifting balance)**。"只要保持散开，就会有人能渡谷"—— 简直和我们的 ③ (MAP-Elites) 一模一样。

> 老实的提醒：这是"看起来像"的*比喻*。做出 MAP-Elites 的人并没有模仿赖特 (论文里也没引用他)。

### 但并非"总是需要"

赖特的同代人 **费希尔 (Fisher，1930 年)** 说的正相反。"保持一个大群、只靠普通选择就够了。不必特意散开。"

两人最深的对立是**"地形是凹凸 (山很多) 还是平缓 (只有一座山)?"** 赖特说"因为凹凸，所以需要渡谷战略"；费希尔说"大体平缓，所以普通选择就行"。

后来的生物学家 **科因・巴顿・图雷利 (Coyne, Barton, Turelli，1997 年)** 认真检验了赖特的战略，得出这样的结论。

- **只靠普通自然选择，大多数都能解释。**几乎没有只有赖特战略才能解释的真实例子。
- **赖特战略起作用，只有在有深谷的非常特殊的时候。**现实的谷大多很浅，而且很多时候根本不用渡谷也能进化。

这**和我们自己的结果惊人地像**。我们也发现了"如果地形真的平缓，③ 不需要，简单的做法就够"。科因等人的"现实地形大多简单"，正是我们的**负面结果 (③ 不需要) 的生物学版本**。

> 老实的提醒 (三点)：
> - 科因等人并没有说"赖特绝无可能"。他们只是说"不能说它普遍、重要"。争论尚未定论。
> - 所以不能写"赖特是错的"。
> - 而且在生物里"散开战略"有时会**起反效果** (好基因被困在小群里散不开)。我们的计算机里没有与之对应的东西 —— 这里比喻会偏，生物那边的主张要更强一档。

### 比喻①：变黑的蛾子 (低维 = 普通选择就够)

英国一种叫**桦尺蛾**的蛾子的故事。在工厂烟把树熏黑的年代，白蛾容易被鸟吃掉，黑蛾增多了。空气变干净后，白蛾又增多了。

这"黑/白"由**仅仅一个基因的开关**决定，能选的颜色实质上只有 2~3 种 = **非常简单 (低维)**。不容易被鸟吃掉的颜色就那样存活下来 (普通的强选择)。**散开战略 (③) 既不需要，也没人在用。**

这和我们的**第 5 战"把零件混 4 种"完全一样**。零件是 4 选 1 = 低维，所以骰子能把它们全都直接试一遍。③ 没有出场机会。**变黑的蛾子 = 零件 4 选 1 那个故事的生物版本。**

> 老实的提醒：也有一段时期颜色会混在一起，但那是因为"不同地方环境不同 + 迁移"，并不是靠像 ③ 那样的多样性保持。这是比喻稍微偏的地方。

### 比喻②：获得新能力的大肠杆菌 (高维 = 历史与多样性起作用)

研究者伦斯基 (Lenski) 的**大肠杆菌超长期实验**。他把同样的大肠杆菌分成 12 组，从 1988 年起一直培养。某个时候，**12 组里只有 1 组**获得了在有氧环境下吃"柠檬酸"这个以前用不了的新能力 (第 3 万 1500 代)。

重要的是，它**不是"突然"发生，而是"只在事先积累了别的变化的那个特定组里"发生**。不按顺序积累变化就到不了 = **高维、依赖历史的复杂地形**的真实例子。这是属于**③ 有可能起作用那一侧的比喻**。

> 老实的提醒：这不是"③ 这个算法赢了"的证明。它只是一个自然的实验，没有用到 ③ 的机制。而且分成 12 组这件事本身，就像"回到起点重来"。所以不能说到"散开战略是最好的"。充其量是"在复杂地形里，多样性有可能起作用"这个印象。

— 歇一下。当我意识到 100 年前的争论是同一个形状时，背上一阵发凉。但不把"发凉"误当成"证明"，正是今天的纪律。 —

---

## 那么，该租 GPU 吗?

把前面总结一下，

- **我们在 CPU 上测过的地形，全都是"平缓"或"低维的简单选择"。**所以不需要 ③ (= 变黑的蛾子、费希尔、科因等人那一侧)。
- **③ 真正起作用，只在"凹凸的高维地形"** (= 赖特的渐变平衡、伦斯基的大肠杆菌那一侧)。
- 那么"凹凸的高维地形"在哪里? → 大概只剩下**在 GPU 上运行的真正大规模 AI 的地形** (几百万个旋钮 = 正是高维) 了。

所以"租 GPU、在真正的 AI 上试 ③"**不是凭直觉，而是顺着扎实理由 (只有在高维 ③ 才有意义) 的赌注**。

不过，**终究是赌注**。即使在真正 AI 的地形上，如果用梯度的强方法 (backprop) 一路顺滑前进，③ 说不定到头来还是不需要 (和零件 4 选 1 赢不了骰子是同样的风险)。所以不立刻砸大钱，方针是租一点云，先试一次。

---

## 总结 —— 一句话

写了很多，但结论就这一行。

> **③ (选别出来分别培养的工夫) 有用，只有在"高维的骗人地形"时。我们现在能在 CPU 上测到的"仿实物"地形，全都不满足那个条件。**

所以这不是"查明 ③ 不需要"。正确的说法是：

- 在骗人地形上，③ 是真本事 (大胜)
- 记忆测试、应用能力、仿实物、零件 4 种，全都不满足条件，③ 不需要
- 真正的实物 (真正巨大 AI 的地形，几百万个旋钮) 还没测过 —— 那才是主城，而且是"值得一试的赌注"
- 而且这个结论的骨架，**100 年前的生物研究 (赖特和科因等人) 早就画出来了** —— 只不过生物的故事**不是证明，而是比喻 (接地)**

还有今天最想传达的一点。

> **"好得过头的结果，不是胜利而是警报。"**
> 因为事先放好了怀疑自己结果的机制，才避免了空欢喜，到达了正确的地基。

诚实本身就是推动研究前进的力量 —— 就是这样一场六连战。

---

**这篇文章的技术版**：连载 #34"爬山六连战弄清了'进化的 ③ 何时有效'—— 而且 100 年前的进化生物学早已给出同样的答案"(在同一个文件夹内)

---

# 한국어

![등산 6연전 — 선별 육성 기법은 언제 효과가 있나?](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q34k_4koma_ko.svg)
# (연재 #34 쉬운 버전) 등산 6연전과, 검게 변한 나방・새로운 힘을 얻은 대장균 이야기

이 글은 조금 어려운 연구 이야기를 **중학생도 알 수 있는 말만으로** 설명합니다. 전문 용어가 나오면 곧바로 "등산"이나 "생물"의 비유로 바꿔 말합니다.

연재 #33의 쉬운 버전에서는 "마지막 결판"을 설명했습니다. 이 #34에서는 거기에 **도달하기까지의 여섯 가지 실험 전부**를 하나의 이야기로 늘어놓습니다. 게다가 이번에는 **거의 100년 전의 생물 연구가, 우리와 같은 답을 내놓았다**는 이야기를 합니다.

---

## 먼저, 무엇을 하는 연구인가?

우리는 "AI 두뇌의 부품을, 생물의 진화처럼 조금씩 바꿔 만들어, 똑똑한 부품을 찾는" 연구를 하고 있습니다. 프로젝트 이름은 **llcore**입니다.

생물의 진화에는, 교과서적으로 네 가지 요소가 있습니다 (연구에서는 번호로 부릅니다).

- ① **변이** … 설계를 조금 바꿔 본다
- ② **유전** … 부모의 설계가 자식에게 이어진다
- ③ **적자생존・분리** … 좋은 것을 골라 남긴다 ← **오늘의 주인공**
- ④ **과잉번식** … 자식을 많이 만든다

오늘의 이야기는, ③을 **"여러 타입을 선별해서, 각각 다른 장소에서 키운다"**는 정교한 궁리로 만들었을 때, 그것이 **정말로 도움이 되는가?**라는 물음입니다.

---

## 등산의 비유 (복습)

설계의 "좋음"을 **지형의 높이**로 나타냅니다. **높은 곳 = 좋은 설계**. 가장 높은 정상을 찾는 게임입니다.

**완만한 외봉우리 (쉬움)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

이건 **지금보다 조금 더 높은 쪽으로 걷기만 하면** (등산법) 정상에 도착합니다. **정교한 궁리 (③)는 필요 없습니다.**

**속임수 지형 (어려움)**

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

앞쪽에 "가짜 정상"이 있고, 골짜기를 건넌 그 너머에 "진짜 정상"이 있습니다. 소박한 등산은 **가짜 정상에서 멈춥니다** (골짜기를 내려갈 수 없으니까).

여기서 효과를 내는 것이 ③입니다. **여러 타입의 등산자를 골짜기 여기저기에 남겨 두면**, 누군가가 골짜기를 "디딤돌"로 건너 진짜 정상에 도달할 수 있습니다. 이것을 연구에서는 "기억의 궁전 (MAP-Elites)"이라고 부릅니다.

> **가장 중요한 포인트**: ③이 도움이 되는 것은 **"속임수 지형"일 때뿐**. 완만한 외봉우리라면 소박한 등산으로 충분합니다.

그래서 물음은 이렇습니다.

> **AI의 설계를 찾을 때, 나오는 지형은 "속임수 지형"인가? 아니면 "완만한 외봉우리"인가?**

— 여기서 한숨 돌립니다. 비유는 이것으로 전부. 이제부터는 6연전의 실록입니다. —

---

## 6연전을 한눈에 보는 지도

먼저 지도를 내놓습니다. 이것이 등뼈입니다.

| 전 | 어떤 지형을 쟀는가 | ③은 통했나? | 한마디 |
|---|---|---|---|
| **1** | 일부러 만든 "속임수 지형" | **Yes (압승)** | ③은 진짜라고 증명 |
| **2** | 기억 테스트 / 부품을 여러 개 잇기 | **잴 수 없음** | 지형이 너무 쉽거나 너무 어려워 측정 불가 |
| **3** | 여러 과제에 대한 응용력 | **No** | ③은 "선택 없음"에는 이기지만, 그 이상은 아님 |
| **4** | 실물 그대로의 지형 (도구의 흔들림을 0으로) | **No** | 지형이 **정말로 완만**하다고 확정 |
| **5** | 부품을 4종류 섞는 샛길 | **No** | 주사위로 전부 뽑을 수 있어 **이미 막혀 있었다** |

이야기는 이렇습니다. **먼저 "속임수 지형이라면 ③은 압승한다"를 증명하고 (1), 그럼 실물에서는 어떤지 네 번 재러 갔더니 (2~5), 실물에 가까운 지형은 전부 "③이 필요 없는 지형"이었다.** 게다가 마지막 (4, 5)에서 "필요 없는 이유"가 **측정이 거칠어서가 아니라, 지형이 정말로 단순했기 때문**이라고 확정되었습니다. 이것이 오늘의 호(arc)입니다.

---

## 제1전: 일부러 "속임수 지형"을 만들었더니, ③이 압승

처음에 "③이 **이론대로 통하는 장면이 정말로 있는가**"를 증명했습니다. 지형을 **일부러 심술궂게 만들어서**, ③을 소박한 방법 (특히 "처음으로 돌아가 다시 하는 랜덤 리스타트 등산")과 겨루게 했습니다.

결과는 **③의 압승**. ③만이 진짜 정상에 약 95%로 도달하고, 다른 방법은 전부 가짜 정상에서 멈췄습니다 (승률 100%, 효과는 이론상 최대).

→ **③은, 제대로 도움이 되는 진짜 구조**임을 알았습니다.

다만 솔직히 말하면, **일부러 심술궂게 만든 지형**에서의 이야기입니다. "③은 가능하다"를 증명했을 뿐, "실물 지형도 이렇게 심술궂다"고는 말하지 않았습니다. 그래서 다음 4전은, 실물에 가까운 지형에서 확인하는 여정이었습니다.

— 잠깐 쉽니다. 제1전은 기분 좋은 압승. 여기서부터 구름이 끼기 시작합니다…. —

---

## 제2전: 지형이 너무 쉽거나/너무 어려워, 잴 수 없었다

실물 기억 테스트로 재려고 했더니, **지형이 양극단**이었습니다.

- 어떤 테스트는 **너무 어려워 아무도 오르지 못함** (모두 산기슭에서 제자리걸음).
- 다른 테스트는 **너무 쉬워 전원이 정상**(차이가 안 남).

둘 다 "③이 통하는가"를 비교할 수 없음 = **측정 불가**. 부품을 여러 개 이어도, 이 벽 (5비트 패리티라는 계산이 원리적으로 이 방식으로는 풀리지 않음)은 넘을 수 없었습니다.

여기서 한 가지 중요한 깨달음. **지형이 유전자 수준에서 울퉁불퉁해도, 그것은 "③으로 건너야 할 속임수 지형"과는 다르다.** 나중에 이 구분이 효과를 냅니다.

— 잠시 휴식. "잴 수 없었다"는 수수하지만, 지도의 공백 지대로서 중요합니다. —

---

## 제3전: 여러 과제에 대한 응용력 — ③은 필요 없었다

다음은 "배우지 않은 길이의 문제에도 응용할 수 있는가"(응용력)로 쟀습니다.

결과: ③은 **"선택을 전혀 하지 않는 방법"에는 이겼지만**, **보통으로 선택하는 방법 (단 선별은 안 함)에는 이기지 못했고**, 주사위 맡김 (random)에도 이기지 못했습니다.

즉 "③만의 궁리 (선별)"의 효과는 없었습니다. 이 지형은 **완만하고, 보통 방법으로도 같은 곳에 도착**했습니다.

솔직한 이야기: 다른 AI (Codex)가 처음 "이 결과는 믿을 수 없다"고 말하며, 세 가지 수정을 요구했습니다. 하지만 **고쳐도 결론은 바뀌지 않았습니다.** "고치면 바뀌는 취약한 결과"는 아니었다는 것이 수확입니다.

— 잠깐 쉽니다. 진 것은 진 것이지만, "올바르게 졌다"고 확인하는 데 더 시간이 걸렸습니다. —

---

## 제4전: 도구의 흔들림을 0으로 했더니, 지형은 "정말로 완만"했다

여기가 이야기의 전환점입니다. 제3전까지 "③은 필요 없다"가 이어졌지만, **응어리**가 남아 있었습니다.

- (A) 지형이 정말로 **완만**하니까 ③이 필요 없는 것인가?
- (B) 아니면 **측정이 거칠어서**, 골짜기가 있어도 안 보였을 뿐인가?

이것을 헷갈리면 "③은 무력하다"고 지나치게 말하게 됩니다.

그래서 **재는 도구의 흔들림을 물리적으로 0으로 하는** 궁리를 했습니다. 흔들리는 배를 멈춘 뒤 키를 재는 이미지입니다. 결과는 이랬습니다.

| 잰 지형 | 골짜기 비율 | 판정 |
|---|---|---|
| 실물에 가까운 지형 (소) | **0% (골짜기 없음)** | 완만 → ③ 필요 없음 |
| 실물에 가까운 지형 (대) | 약 10% (아주 얕음) | 거의 완만 → ③ 필요 없음 |
| 일부러 만든 "울퉁불퉁"(테스트용) | 70~80% | 제대로 "울퉁불퉁"으로 검출 ✓ |
| 일부러 만든 "완만"(테스트용) | 0% | 제대로 "완만"으로 검출 ✓ |

중요한 것은 **재는 도구 자체는 올바르게 작동하고 있다**는 것. 그러니 "실물이 완만하다"는 도구의 버그가 아니라, **지형이 정말로 완만**했던 것입니다.

→ **"③이 필요 없어 보인 것은, 지형이 정말로 완만했기 때문"**이 확실해졌습니다.

(솔직한 주의: "완벽하게 매끈"이 아니라 "아주 얕은 골짜기 (2~4%)가 아슬아슬하게 있다" 정도입니다. 그 점은 반올림하지 않고 적어 둡니다.)

— 심호흡. 실물 흉내는 "완만"으로 확정. 남은 것은 "마지막 샛길". —

---

## 제5전: 부품을 4개 섞는 샛길 — 주사위로 전부 뽑혀 버렸다

큰 계산기 (GPU)는 돈이 들어, 곧바로 손대고 싶지 않습니다. 그래서 **부품 (kernel)을 4종류 섞는**다는 다른 수를 시도했습니다.

노림수: 한 종류면 지형이 완만해도, **4종류를 전환하는 순간에 단차 (골짜기)가 생겨 "속임수 지형"이 될지도.** 그렇게 되면 ③의 차례가 생길지도.

결과: **이 샛길은 막혀 있었습니다.** 게다가 "우연히"가 아니라 **"원래부터 지날 수 없는 구조"**였습니다.

왜인가. 비유로 말하면,

> **부품을 4개에서 고르는 것은, 등산자가 처음으로 돌아갈 (리스타트) 때마다, 주사위를 굴려 4개에서 1개를 시험하는 것과 같다.**

소박한 등산의 등산자는, 막다른 곳에 다다르면 리스타트합니다. 부품은 **4개밖에 없으**니까, 몇 번 리스타트하면 **4개 전부를 직접 시험해 버립니다.** 골짜기를 건너지 않아도, 주사위로 진짜 정상을 **직접 뽑을 수 있습니다 (워프).**

그렇게 되면 ③ (골짜기를 건너는 궁리)의 차례가 없습니다. **건너야 할 골짜기가 애초에 없으**니까.

다른 각도 (적대적 체크)에서도 몇 번이나 두들겼지만, 막힌 방식은 무너지지 않았고, 오히려 "주사위로 전부 뽑을 수 있으니 ③의 차례가 없다"가 확실해졌습니다.

> **③이 살아나는 것은, 선택지가 "직접 시험할 수 없을 만큼 방대"할 때뿐.** 부품 4개로는 너무 적었습니다.

(솔직한 주의: 부품 중 하나 "hopfield"는 간이판이라 제 실력이 아니었다는 약점은 남아 있습니다. 그래도 결론은 바뀌지 않습니다.)

---

## 6전을 정리하는 "단 하나의 조건"

여섯 결과는, 단 하나의 조건으로 전부 이어집니다.

> **③이 도움이 되는 것은, "난관"이 "직접 시험할 수 없을 만큼 방대 (고차원)"할 때뿐.**

- 제1전이 압승한 것은, 진짜 정상이 **주사위로는 평생 걸려도 뽑을 수 없을 만큼 방대한 조합**의 그 너머에 있었기 때문.
- 실물 지형 (4전・5전)은 거꾸로 **난관이 작다** (완만, 또는 4지선다). 그러니 주사위 (리스타트)로 직접 워프할 수 있어, ③의 차례가 없었다.

그러니 "유전자 수준에서 울퉁불퉁"(제2전)으로도 충분하지 않습니다. 중요한 것은 **"탐색이 도달해야 할 목표의 넓이"**인 것입니다.

---

## 여기서부터가 오늘의 하이라이트: 100년 전의 생물 연구와 같았다

실은, **"다양성을 유지하는 궁리는, 좁은 조건에서만 도움이 된다"**는 우리의 결론은, 거의 100년 전의 생물 연구에 똑 닮은 선례가 있습니다.

> ⚠ 중요한 주의: 생물 이야기는 **"비유 이야기"이며, 우리의 컴퓨터 실험을 증명하는 것은 아닙니다.** 비유가 딱 맞지 않는 곳은 솔직하게 적습니다.

### 라이트의 "다 함께 흩어져 골짜기를 건넌다" 작전

생물학자 **라이트 (Wright, 1931・1932년)**는 이렇게 생각했습니다. 큰 "하나의 무리"인 채로는, 눈앞의 작은 언덕에서 멈춰 버린다. 더 높은 산에 가려면 한 번 "골짜기"를 내려가야 하는데, 보통의 자연도태는 "내려가는 것"을 허락하지 않으니까.

라이트의 아이디어는 **무리를 작은 그룹으로 뿔뿔이 나누는** 것.

1. 작은 그룹이 우연히 어슬렁어슬렁 움직여, 마침 골짜기를 건넌다.
2. 거기서 보통의 도태로 다른 산을 오른다.
3. 높은 산에 오른 그룹의 좋은 유전자가, 무리 전체에 퍼진다.

이것이 **시프팅 밸런스 (옮겨가는 균형)**. "흩어져 두면 누군가가 골짜기를 건널 수 있다" ── 바로 우리의 ③ (MAP-Elites)과 똑 닮았습니다.

> 솔직한 주의: 이것은 "비슷하다"는 *비유 이야기*. MAP-Elites를 만든 사람이 라이트를 흉내 낸 것은 아닙니다 (논문도 인용하지 않았습니다).

### 하지만 "항상 필요"는 아니었다

라이트와 동시대의 **피셔 (Fisher, 1930년)**는 반대를 말했습니다. "큰 무리인 채로, 보통의 도태만으로 충분. 일부러 흩어지지 않아도 된다."

두 사람의 가장 깊은 대립은 **"지형이 울퉁불퉁 (산이 많음)한가, 완만 (산이 하나)한가"**였습니다. 라이트는 "울퉁불퉁하니까 골짜기를 건너는 작전이 필요", 피셔는 "대체로 완만하니까, 보통의 도태로 된다".

그리고 후대의 생물학자 **코인・바턴・투렐리 (Coyne, Barton, Turelli, 1997년)**가, 라이트의 작전을 본격적으로 검증하고 이렇게 결론지었습니다.

- **보통의 자연도태만으로 대개 설명할 수 있다.** 라이트의 작전으로밖에 설명할 수 없는 실례는 거의 없다.
- **라이트의 작전이 통하는 것은, 깊은 골짜기가 있는 굉장히 특별할 때뿐.** 현실의 골짜기는 대개 얕고, 애초에 골짜기를 건너지 않아도 진화할 수 있는 경우가 많다.

이것이 **우리의 결과와 똑 닮았습니다**. 우리도 "지형이 정말로 완만하면 ③은 필요 없다, 단순한 방식으로 충분"하다고 알았습니다. 코인 등의 "현실의 지형은 대개 단순"은, 우리의 **부정적 결과 (③은 필요 없었다)의 생물학판**입니다.

> 솔직한 주의 (세 가지):
> - 코인 등은 "라이트는 절대 있을 수 없다"고는 말하지 않았다. "일반적・중요하다고는 말할 수 없다"고 말했을 뿐. 논쟁은 아직 결판나지 않았습니다.
> - 그러니 "라이트는 틀렸다"고 써서는 안 됩니다.
> - 게다가 생물에서는 "흩어지는 작전"이 때때로 **역효과**가 됩니다 (좋은 유전자가 작은 그룹에 갇혀 퍼지지 않음). 우리의 컴퓨터에는 이에 해당하는 것이 없습니다 ── 여기는 비유가 어긋나는 곳으로, 생물 쪽이 한 단계 강한 주장을 하고 있습니다.

### 비유①: 검게 변한 나방 (낮은 차원 = 보통의 도태로 충분)

영국의 **얼룩나방**이라는 나방 이야기. 공장 매연으로 나무가 검어진 시대, 흰 나방은 새에게 잡아먹히기 쉬웠고, 검은 나방이 늘었다. 공기가 깨끗해지자, 다시 흰 나방이 늘었다.

이 "검정/흰색"은 **단 하나의 유전자의 스위치**로 정해지고, 고를 수 있는 색은 실질 2~3종류뿐 = **아주 단순 (저차원)**. 새에게 잡아먹히기 어려운 색이 그대로 살아남을 뿐 (보통의 강한 도태). **흩어지는 작전 (③)은 필요 없고, 아무도 쓰지 않습니다.**

이것은 우리의 **제5전 "부품 4종을 섞는다"와 완전히 같습니다**. 부품은 4지선다 = 저차원이니까, 주사위로 전부 직접 시험할 수 있습니다. ③의 차례가 없습니다. **검게 변한 나방 = 부품 4지선다 이야기의 생물판**입니다.

> 솔직한 주의: 색이 한동안 섞이는 시기도 있지만, 그것은 "장소마다 환경이 다름 + 이동" 탓이지, ③ 같은 다양성 보존 덕분이 아닙니다. 비유가 조금 어긋나는 곳.

### 비유②: 새로운 힘을 얻은 대장균 (높은 차원 = 역사와 다양성이 효과를 냄)

렌스키라는 연구자의 **대장균 초장기 실험**. 같은 대장균을 12그룹으로 나눠 1988년부터 계속 키웠다. 어느 때 **12그룹 중 단 하나만**이, 그때까지 못 쓰던 "구연산"을 산소가 있는 환경에서 먹는 새로운 힘을 손에 넣었습니다 (3만 1500세대째).

중요한 것은, 그것이 **"갑자기"가 아니라 "미리 다른 변화가 쌓여 있던 특정 그룹에서만" 일어난** 것. 순서대로 변화가 쌓이지 않으면 도달할 수 없었다 = **고차원이고 역사에 의존하는 복잡한 지형**의 진짜 예. **③이 효과를 낼 수 있는 쪽의 비유**입니다.

> 솔직한 주의: 이것은 "③이라는 알고리즘이 이겼다"는 증명이 아닙니다. 그저 자연의 실험이고, ③의 구조는 쓰지 않았습니다. 게다가 12그룹으로 나눈 것 자체가 "처음으로 돌아가 다시 한다"와 닮았습니다. 그러니 "흩어지는 작전이 최고였다"고까지는 말할 수 없습니다. 어디까지나 "복잡한 지형에서는 다양성이 효과를 낼 수 있다"는 이미지.

— 잠깐 쉽니다. 100년 전의 논쟁이 같은 형태라고 깨달았을 때는 오싹했습니다. 하지만 "오싹"을 "증명"으로 헷갈리지 않는 것이 오늘의 규율입니다. —

---

## 그래서, GPU를 빌려야 하나?

여기까지를 정리하면,

- **우리가 시험한 CPU의 지형은, 전부 "완만"하거나 "저차원의 단순한 선택"이었다.** 그러니 ③은 필요 없었다 (= 검게 변한 나방, 피셔, 코인 등의 쪽).
- **③이 정말로 효과를 내는 것은 "울퉁불퉁하고 고차원인 지형"뿐** (= 라이트의 시프팅 밸런스, 렌스키의 대장균 쪽).
- 그럼 "울퉁불퉁하고 고차원인 지형"은 어디에 있나? → **GPU로 돌리는 진짜 대규모 AI의 지형** (다이얼 수백만 개 = 바로 고차원) 정도밖에 남아 있지 않습니다.

그러니 "GPU를 빌려 진짜 AI로 ③을 시험한다"는 것은 **눈대중이 아니라, 제대로 된 이유 (고차원에서만 ③은 의미를 가진다)에 따른 베팅**입니다.

다만 **역시 베팅**. 진짜 AI의 지형도, 기울기를 쓰는 강한 방식 (backprop)으로 술술 나아가 버린다면, 결국 ③은 필요 없을지도 모릅니다 (부품 4지선다로 주사위에 이기지 못한 것과 같은 리스크). 그러니 곧바로 큰돈을 들이지 않고, 클라우드를 조금 빌려 한 번 시험한다, 는 방침입니다.

---

## 정리 ── 한마디로

많이 적었지만, 결론은 이 한 줄입니다.

> **③ (선별해서 키우는 궁리)이 도움이 되는 것은 "고차원의 속임수 지형"일 때뿐. 지금 CPU로 잴 수 있었던 "실물 흉내" 지형은, 전부 그 조건을 만족하지 않았다.**

그러니 "③은 필요 없다고 판명됐다"가 아닙니다. 올바르게는:

- 속임수 지형에서 ③은 진짜 (압승했다)
- 기억 테스트・응용력・실물 흉내・부품 4종, 전부 조건을 만족하지 않아 ③은 필요 없었다
- 진짜 실물 (진짜 거대 AI의 지형, 다이얼 수백만 개)은 아직 재지 못했다 ── 그것이 본진이고, 게다가 "해 볼 가치가 있는 베팅"
- 그리고 이 결론의 골격은, **100년 전의 생물 연구 (라이트와 코인 등)가 이미 그려 두었다** ── 단 생물 이야기는 **증명이 아니라, 비유 (접지)**

그리고 오늘 가장 전하고 싶은 것.

> **"너무 잘 풀린 결과는, 승리가 아니라 경보."**
> 자기 결과를 의심하는 구조를 미리 놓아 두었기에, 헛김칫국 마시기를 피하고, 올바른 토대에 도달할 수 있었다.

솔직함 그 자체가, 연구를 앞으로 나아가게 하는 힘이 된다 ── 그런 6연전이었습니다.

---

**이 글의 기술 버전**: 연재 #34 "등산 6연전으로 알게 된 '진화의 ③은 언제 효과를 내는가' — 그리고 100년 전의 진화생물학이 같은 답을 내놓고 있었다" (같은 폴더 안)
