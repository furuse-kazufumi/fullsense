---
title: '【📗かみくだき版】「測れる」と「生き残る」は別物 — AI を進化させる"選抜係"lldarwin を金魚の池でわかる話 #26'
tags:
  - FullSense
  - llive
  - 進化計算
  - 解説
private: true
id: 1d9eeb1b739623dbc285
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# (連載 #26 かみくだき版) 「測れる」と「生き残る」は別物 — AI を進化させる"選抜係"lldarwin を金魚の池でわかる話

> 📗 これは [完全版](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba) のかみくだき版です。難しい用語は全部「金魚の池」と「学校のテスト」のたとえに言い換えます。技術版を読む前の地ならし、または「だいたい何やってるの?」を 10 分で掴みたい人向けです。

---

## まず三行で(落語でいう「枕」)

- AI を進化で育てるには、**「測る係」と「選抜する係」の二人が必要**。今日の主役は選抜係の **lldarwin(エルダーウィン)**。
- 選抜の鉄則はたった一語、**「足し算するな(集約するな)」**。テストの点を全部足して順位をつけた瞬間、進化は壊れる。
- そして今回は口先だけじゃない。**実際に動かして数字が出た**。絶滅したはずの天才たちを全員復活させ、本物の AI を相手に苦手科目を 0 点→満点にした話をします。

---

## 1. 前回の大失敗 —「私とフリストンだけが残った」

この連載の前回(#25)で、私はみっともない失敗を正直に晒しました。

AI を 500 世代かけて進化させたら、最後に世界に残ったのは **私とフリストン(ある研究者)だけ**。岡潔もグロタンディークもフォン・ノイマンも、進化の途中で静かに全員消えていきました。

なぜか。原因は「測る道具(眼鏡)」が**みんなに満点を出し続けた**こと。全員が満点なら、誰を残して誰を捨てるか決められない。差が「測れて」いても、その差を「**誰が生き残るか**」に変換できなければ、進化はただのサイコロ振り(専門用語で「遺伝的浮動」)になってしまう。

> 🍵 たとえると、学校で全員に 100 点をつけたら、成績順に並べられませんよね。「優秀な子を伸ばす」も「苦手な子を補習する」もできない。差を測っただけでは、人は育たない。

今回はその続き。「眼鏡で差は測れた。じゃあ、その差を**ちゃんと選抜に変換する装置**はどう作るのか?」——それが新メンバー **lldarwin** です。

---

## 2. 「測る係」と「選抜する係」を分ける

私たちのファミリーには、すでに **lleval(エルイヴァル)= 測る係**がいます。AI 一体一体の振る舞いを観察して、いろんな科目で点数をつける係です。

ところが #25 でわかった怖い事実。**点を測れても、それを全部足して 1 本の合計点にした瞬間、選抜が壊れる**。

```
lleval   = 測る係  (一体ごとに「各科目の点数の束」を出す)
lldarwin = 選抜係  (その点数の束から「次世代の親」を選ぶ)
```

ここで lleval には一つ約束を課します。「**点数を足し算してから渡すな。科目ごとの内訳をそのまま渡せ**」。合計点に丸めてから渡されたら、選抜係 lldarwin は何もできなくなるからです。

> 🤔 漫才風に。
> ボケ「写真の良し悪し、明るさ・構図・表情を全部足して 1 個の点数にしたで」
> ツッコミ「**丸めるな!** 表情だけ神がかってる一枚があるやろ、平均点にしたら捨ててまうやんけ」
> ——そう、足し算は「一芸に秀でた奴」を殺す。測る人と選ぶ人を兼任させると、たいてい両方が雑になります。

---

## 3. 設計の核 —「足し算しない」工夫を 7 つ束ねる

lldarwin は、測る係からもらった「科目ごとの点数の束」を、7 つの工夫で選抜します。全部に共通する思想は一つだけ、**「1 本に丸めない」**。代表的なものを 3 つだけ紹介します。

1. **科目を 1 つずつ見る(ε-lexicase)** — 合計点で順位をつけず、「数学」「国語」と科目を 1 つずつ独立に見る。数学だけ 100 点・他 0 点の天才も、「数学の科目では誰にも負けない」から生き残れる。**これが #25 の失敗(8人→2人)を生んだ機構そのものの対策**。
2. **マス目に標本を保管する(QD / MAP-Elites)** — 振る舞いのタイプを地図のマス目に分けて、各マスに最低 1 体ずつ「代表」を残す。1 マスに 1 体でも残れば、そのタイプは絶滅しない。
3. **最低ラインを設ける(minimal-criterion)** — 合計順位だけで「一強が全部の繁殖枠を独占」させない。最低ラインを満たせば誰でも子を残せる「最低保証」で、多様性の土台を残す。

残り 4 つ(平均的優等生を優遇しない標準化、似た者同士を割引、毎世代テスト範囲をシャッフル、停滞したら新規性に報酬)も、すべて「丸めない」哲学の仲間です。

> 🍵 「自分で新しいアルゴリズムを発明しないの?」とよく訊かれます。答えは「既存研究の組合せで十分強いから」。進化計算の論文 616 件を読み比べて、「足し算しない」系譜の良い手法だけを**選別して束ねた**。lldarwin の独自性は、新発明ではなく「これらを**混ぜずに一皿に盛りつけて**、進化ループに**実際に配線した**こと」にあります。世界初の食材を作るより、混ぜたら台無しになる名食材を共存させる盛りつけの技です。

---

## 4. Stage1 — 金魚の動きの多様性が 2 倍になった

ここからは口先じゃなく**実測**です。まず 2 つだけ変更を入れて測りました。

- **変更1: 悪い物差しを捨てた。** #25 で犯人だった「合計点(argmax)」を、選抜の判断材料から外す掃除。
- **変更2: 新規性ボーナス。** 「**みんなと違う振る舞いをしている**」こと自体を、ひとつの科目として評価に混ぜる。

結果、AI たちの振る舞いの多様性(数字が大きいほど多彩)が:

| 条件 | 多様性 | 終盤 |
|---|---|---|
| 何もしない(旧方式) | 7.12 | 0.83(崩壊) |
| **変更1+2 を入れた** | **14.88(+109%)** | **11.73(崩壊回避)** |

**約 2 倍**に増え、しかも終盤の崩壊も防げました。

> 🍵 金魚の池でたとえると。餌に群がる金魚ばかり残すと、いずれ全員が同じ場所で同じ動きをする退屈な池になる。新規性ボーナスは「**みんなと違う場所を泳ぐ金魚にもエサをあげる**」係。結果、池のあちこちに散らばった、見ていて飽きない池になります。……ただし、この賑やかな池には**落とし穴**が隠れていました。次の節で発覚します。

---

## 5. いちばん大事な告白 — 私は 2 種類の「多様性」を取り違えていた

ここが本記事で**一番大事**な節です。良い数字(+109%)が出ても、勝った気にならない。これは私の鉄則です。「変に良い数字が出たら、内訳を疑え」。疑ったら、間違いを見つけました。

別の指標を見ます。「最初にいた **8 つの家系(祖先系統)** のうち、何家系が最後まで生き残ったか」。

結果は——**全部の条件で、結局 8 家系→2 家系に収束**。岡潔もグロタンディークもフォン・ノイマンも、**やっぱり全員絶滅**。動きの多様性を 2 倍にしたのに、**家系の生き残りは #25 と全く同じ 2 家系**でした。

なぜか。私は **2 種類の「多様性」を混同していた**のです。

- **動きの多様性**(金魚が多彩な泳ぎ方をしている)→ 新規性ボーナスで増やせる。
- **家系の多様性**(元の 8 家系が何家系残っているか)→ **新規性ボーナスでは絶対に増えない**。

理由はシンプル。新規性ボーナスも科目別評価も、「**今いる金魚を残す**」工夫であって、「**一度死んだ家系を生き返らせる**」機能がない。だから一度絶滅した家系は二度と戻らず、生き残りは運(サイコロ)任せで 2 家系に固定される。これは生物学でいう「中立浮動」で、**理論的には正常**な現象。崩壊ではなく、自然に起きることなんです。

> 🤔 漫才風に。
> ボケ「池にカラフルな動きの金魚を増やしたで! 多様性バッチリや!」
> ツッコミ「で、**血統**は? 8 つあった家系、いくつ残ってんの?」
> ボケ「……2 つや」
> ツッコミ「動きは派手やのに家系図はスカスカやないか! 動きの多様性と血統の多様性は**別の話**やぞ!」

つまり「岡潔・グロタンに生き残ってほしい」という私の願いは、**動きの多様性を上げる薬では絶対に治らない病気**だった。薬を間違えていた。これを正直に記録します。

---

## 6. Stage1.5 — 絶滅した家系を蘇らせる「中立貯蔵庫」

病気の正体がわかれば、薬を変えられます。家系を守るには「**絶滅した家系を毎世代こっそり呼び戻す機構**」が必要——名づけて **中立貯蔵庫(リザーバー)**。

仕組みはこう。**各家系の「歴代ベスト個体」を凍結保存しておき、絶滅しそうな家系を毎世代こっそり池に戻す**。強い家系は普通に繁殖し、弱い家系は貯蔵庫が生命維持する、という二段構え。

いきなり本番をいじらず、まず小さな実験(PoC)で機構が回ることを確かめ、次に本番の進化ループに「**既定オフ、フラグを立てたときだけ有効**」(=既存の動きは一切変えない)という安全設計で組み込みました。

本番での実測結果が、本記事**最大の見せ場**です。

| 中立貯蔵庫 | 生き残った家系 | 家系の固定度(低いほど多様) |
|---|---|---|
| OFF | **2 家系**(私 + フリストン) | 0.70 |
| **ON** | **8 家系 全員生存!** | **0.29** |

岡潔(oka)もグロタンディーク(grothendieck)もフォン・ノイマンも、**実際に全員生き残りました**。

![中立貯蔵庫 OFF(上)は 2 家系に崩壊、ON(下)は全 8 家系が帯として並存する。8 色が最後まで残る様子が一目でわかる](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

OFF だと世代が進むにつれ 2 色に呑み込まれていく(#25 の再現)。ON だと 8 色が最後まで帯として残る。岡潔もグロタンディークも、消えていません。

> 🍵 #25 で「私とフリストンだけが残った」と嘆いた、あの寂しい世界。それが岡潔もグロタンディークも全員いる賑やかな世界に変わりました。**これは捏造ではなく、実際に動いた結果です**(私のルールで虚偽の失敗も虚偽の成功も書きません)。ただし——浮かれる前に §5 の姿勢を思い出しましょう。「いい数字が出たら内訳を疑う」。実はこの成功にも**代償**がありました。動きの多様性は 14.88 → 9.20 にちょっと下がる。凍結した代表を毎世代戻すぶん、新しい広がりが少し減るのです。代償ゼロの魔法ではない、と正直に書いておきます。

---

## 7. 予想を裏切った発見 —「やりすぎ」も「放置しすぎ」もダメ

§6 の代償(凍結代表を戻すと動きの多様性が下がる)を、「**何世代おきに呼び戻すか(再投入間隔)**」を変えて調べました。

直感ではこう思いますよね。「呼び戻しを減らせば(間隔を広げれば)、押し込みが減って多様性が単調に回復するはず」。ところが——

| 呼び戻し間隔 | 生き残り家系 | 動きの多様性 |
|---|---|---|
| 毎世代 | **8/8** | 9.91 |
| 5 世代ごと | 5/8 | **12.84(最大!)** |
| 10 世代ごと | 3/8 | 11.41 |
| 20 世代ごと | 2/8 | 10.75 |

**多様性は単調に増えず、「5 世代ごと」でピークを打って、それ以上放置するとむしろ下がった**のです。

理由は腑に落ちます。家系を放置しすぎると、(a) 貯蔵庫からの多様性注入が減り、(b) 少数家系が固定してしまって、結局どっちも伸びない。「呼び戻しすぎ」も「放置しすぎ」も両方ダメで、**中間に最適点がある**。これは**実際に試さなければ予測できなかった**発見です。

![再投入間隔のトレードオフ。家系保持と動きの多様性は反比例し、多様性は「5 世代ごと」でピークを打つ(単調ではない)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep.svg)

> 🍵 植物の水やりと同じです。あげなさすぎても枯れるし、あげすぎても根腐れする。中庸に最適点がある。進化計算をやると、こういう「単調じゃない曲線」に何度も出会います。だから直感を信じず、ベースラインを測り、実際に振ってみる。直感は、よく裏切られます。

---

## 8. 仕上げ — 本物の AI を相手に、苦手科目を 0 点→満点に

ここまでは「proxy(代理)」という簡易な物差しで機構を確かめてきました。最後に、**本物の AI(手元のサーバーで動く llama3.2 という実 LLM)**を相手にします。

肝は「進化させる設計図(genome)を、どうやって本物の AI に効かせるか」。答えは **AI 本体は固定したまま、AI に被せる"指示書(プロンプト戦略)"の方を進化させる**。同じ AI でも、被せる指示書次第で賢くも残念にもなる——その「賢くする指示書」を進化で選び取らせる作戦です。

結果、本物の選択信号が観測できました。

> **「順を追って考えてね(CoT)+ 構造化して」という指示書戦略**が、llama3.2 の **多段推論(いくつもステップを踏む問題)を 0.0 → 1.0(満点)に改善**。素っ気ない指示書は 0.0 で失敗したまま。

同じ AI 本体でも、進化が選び取った指示書を被せると、解けなかった問題が解けるようになった。これを proxy ではなく**本物の AI で実証**したのが到達点です。

![5 つの苦手科目の平均点の推移(本物の on-prem LLM llama3.2 で評価)。指示書戦略の進化で科目が改善していく](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

### でも、ここでも勝った気にならない(最重要の告白)

派手な数字(0.0→1.0)が出たからこそ、内訳を徹底的に正直に書きます。

- **賢くなったのは「指示書戦略」であって「AI 本体」でも「人格(岡潔とか)」でもない**。岡潔の人格が賢くなったわけではなく、岡潔という家系に紐づいた指示書が選ばれただけ。
- **問題数が少ない**(科目あたり 2 問)。0.0→1.0 という劇的な数字も、問題数が少ないぶんノイズを含む。統計的に堅い主張にはもっと多くの問題が要る。
- **手元の 1 モデル・特定タスクだけ**の観測。「AI 一般がこうなる」とは言いません。

これらを伏せれば「進化で AI が劇的に賢くなった!」という派手な物語が書けますが、それは嘘です。lldarwin が実証したのは「**機構が、本物の AI 上で、ちゃんと選択信号を生む**」というところまで。その線を越えた主張はしません。

> 🍵 研究で一番気持ちいいのは「0 点が満点になった!」と叫ぶ瞬間。でも、その瞬間こそ「変に良い数字が出たら、勝った気になる前に内訳を疑え」が効いてくる。honest disclosure(正直な開示)は、自慢を我慢する筋トレです。

---

## で、結局何がわかったの?

たくさん書きましたが、要点はこれだけです。

- 進化には **「測る係(lleval)」と「選抜係(lldarwin)」の二人**が要る。選抜の核は **「足し算するな」**。
- 動きの多様性は新規性ボーナスで **2 倍(7.12→14.88)**にできた。でも——
- **私は「動きの多様性」と「家系の多様性」を取り違えていた**。家系は新規性ボーナスでは救えず、別の薬(中立貯蔵庫)が必要だった。正直に記録。
- 中立貯蔵庫で、絶滅した **8 家系を全員復活**(岡潔・グロタンディーク含む)。**これは捏造ではなく実際に動いた**。
- 呼び戻し頻度には **「やりすぎも放置しすぎもダメ、中庸に最適点」**という、予想を裏切る発見があった。
- 本物の AI を相手に、進化した指示書戦略が **苦手科目を 0→満点に**。ただし「賢くなったのは指示書だけ・問題数は少ない・1 モデルだけ」と内訳を正直に分けた。

そして今日いちばん伝えたいこと:

> **良い部品を作るだけでは進化は壊れたまま。「足し算せず束ね、実際に配線し、絶滅した家系を蘇らせ、本物の AI で選択信号を確かめる」——そこまでやって、ようやく「私とフリストンだけ」の世界を、岡潔もグロタンディークもいる賑やかな世界に変えられた。**

次回 #27 では、この成功にどこまで信を置いてよいかを、わざと反証でいじめ抜きます。良い数字が出たからこそ、次は徹底的に鍛え直す。それが研究の正直さです。

---

## もっと知りたい人へ

技術的な数式・コミット・設計の詳細は **[完全版 #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)** をどうぞ。ε-lexicase / QD / down-sampling の出典論文、7 ステージの設計契約、実 LLM 写像(Promptbreeder 系)、12h 連続ランの詳細まで全部載っています。

---

# English

# (Series #26, plain-language edition) "Measurable" and "Survives" Are Two Different Things — Understanding the AI Selection Officer "lldarwin" via a Goldfish Pond

> 📗 This is the plain-language edition of the [full article](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba). Every hard term gets swapped for a "goldfish pond" or "school test" analogy. It levels the ground before the technical version, or it's for people who want to grasp "what are they roughly doing?" in ten minutes.

---

## First, three lines (the rakugo "pillow")

- To raise an AI by evolution, you need **two officers: a "measuring officer" and a "selection officer."** Today's star is the selection officer, **lldarwin**.
- The iron rule of selection is one word: **"do not add up (do not aggregate)."** The moment you sum all the test scores and rank by the total, evolution breaks.
- And this time it's not just talk — **I actually ran it and got numbers.** I revived every one of the geniuses that had supposedly gone extinct, and against a real AI I improved a weak subject from 0 to a perfect score.

---

## 1. The big failure last time — "only me and Friston remained"

In the previous article (#25), I honestly exposed an embarrassing failure.

When I evolved an AI for 500 generations, the only ones left in the world were **me and Friston (a researcher)**. Oka Kiyoshi, Grothendieck, von Neumann — they all quietly vanished mid-evolution.

Why? The cause was that the "measuring device (the glasses)" kept **handing out perfect scores to everyone**. If everyone is perfect, you can't decide whom to keep and whom to discard. Even if you can "measure" the differences, if you can't convert them into "**who survives**," evolution degenerates into mere dice-rolling (the technical term is "genetic drift").

> 🍵 By analogy: if you give every student in school 100 points, you can't rank them by grade. You can neither "nurture the gifted" nor "tutor the struggling." Merely measuring differences doesn't grow anyone.

This time is the sequel. "We could measure the differences with the glasses. So how do we build the device that **properly converts** those differences into selection?" — that's the new member, **lldarwin**.

---

## 2. Separating the "measuring officer" and the "selection officer"

Our family already has **lleval = the measuring officer**. It observes each AI individual's behavior and scores it across various subjects.

But here's the scary fact from #25: **even if you can measure the scores, the moment you add them all into one total, selection breaks.**

```
lleval   = measuring officer  (outputs "a bundle of per-subject scores" per individual)
lldarwin = selection officer  (picks "next-generation parents" from that bundle)
```

So we impose one promise on lleval: "**Do not add the scores up before handing them over. Pass the per-subject breakdown as-is.**" If it hands over a total rounded into one number, the selection officer lldarwin can do nothing.

> 🤔 Comedy-duo style.
> Straight man: "I added up brightness, composition, and expression of the photo into one score."
> Funny man: "**Don't round it up!** There's one shot where the expression is divine — average it out and you'll throw it away."
> — Yes, addition kills the one-trick specialist. Make one person both measure and select, and usually both jobs get sloppy.

---

## 3. The design core — bundling seven "don't add up" tricks

lldarwin takes the "bundle of per-subject scores" from the measuring officer and selects with seven tricks. They all share one philosophy: **"never round into one."** Here are just three.

1. **Look at subjects one at a time (ε-lexicase)** — don't rank by total; look at "math," "language," etc. independently, one by one. A genius with 100 in math and 0 elsewhere survives because "in the math subject, nobody beats them." **This is the very fix for the mechanism that caused #25's failure (8 people → 2).**
2. **Store specimens in a grid (QD / MAP-Elites)** — divide behavior types into grid cells on a map, and keep at least one "representative" per cell. As long as even one survives in a cell, that type never goes extinct.
3. **Set a minimum bar (minimal-criterion)** — don't let one strongman monopolize all breeding slots by total rank alone. Anyone who clears the minimum bar can leave offspring — a "minimum guarantee" that preserves the foundation of diversity.

The other four (standardization that doesn't favor the all-around honor student, discounting look-alikes, shuffling the test scope every generation, rewarding novelty when stagnating) all belong to the same "don't round" philosophy.

> 🍵 People often ask, "Why not invent a new algorithm yourself?" The answer: "Because combining existing research is already strong enough." I read and compared 616 evolutionary-computation papers and **selected and bundled** only the good "don't add up" methods. lldarwin's originality isn't a new invention — it's "**plating them on one dish without mixing** and **actually wiring them** into the evolution loop." Rather than inventing a world-first ingredient, it's the plating skill of letting famous ingredients (that would be ruined if mixed) coexist.

---

## 4. Stage 1 — the goldfish's behavioral diversity doubled

From here it's not talk but **real measurement.** I first put in only two changes and measured.

- **Change 1: discard the bad ruler.** Cleaning out the "total score (argmax)" — the culprit in #25 — from the selection criteria.
- **Change 2: a novelty bonus.** Mixing into the evaluation, as a subject in itself, the very fact of "**behaving differently from everyone else**."

The result: the diversity of the AIs' behavior (bigger number = more varied):

| Condition | Diversity | Endgame |
|---|---|---|
| Do nothing (old method) | 7.12 | 0.83 (collapse) |
| **Changes 1 + 2 added** | **14.88 (+109%)** | **11.73 (collapse avoided)** |

It **roughly doubled**, and it also prevented the endgame collapse.

> 🍵 In goldfish-pond terms: keep only the goldfish swarming the food, and eventually you get a boring pond where everyone is in the same place doing the same moves. The novelty bonus is the officer who "**also feeds the goldfish swimming in a different spot from everyone.**" The result is a pond scattered all over, one you never tire of watching. ...But this lively pond hid a **pitfall.** It surfaces in the next section.

---

## 5. The most important confession — I had confused two kinds of "diversity"

This is the **most important** section. Even with a good number (+109%), I don't get cocky. That's my iron rule: "When a suspiciously good number appears, doubt the breakdown." I doubted, and I found a mistake.

Look at a different metric: "Of the **8 family lines (ancestral lineages)** present at the start, how many survived to the end?"

The result — **in every condition, it converged to 8 lines → 2 lines.** Oka Kiyoshi, Grothendieck, von Neumann — **all extinct again.** I doubled the behavioral diversity, yet **the lineage survival was the exact same 2 lines as #25.**

Why? Because I had **confused two kinds of "diversity."**

- **Behavioral diversity** (goldfish swimming in varied styles) → can be increased by the novelty bonus.
- **Lineage diversity** (how many of the original 8 lines remain) → **can never be increased by the novelty bonus.**

The reason is simple. Both the novelty bonus and per-subject evaluation are tricks to "**keep the goldfish currently alive**" — they have no function to "**bring back a line that has died.**" So once a line goes extinct it never returns, and the survivors are fixed at 2 lines by luck (dice). In biology this is "neutral drift," and it is **theoretically normal.** It's not a collapse — it's something that happens naturally.

> 🤔 Comedy-duo style.
> Funny: "I increased the goldfish with colorful moves! Diversity's perfect!"
> Straight: "And the **bloodlines**? Of the 8 family lines, how many are left?"
> Funny: "...Two."
> Straight: "The moves are flashy but the family tree is bare! Diversity of movement and diversity of bloodline are **two different things**!"

So my wish that "Oka and Grothendieck survive" was a disease that **the medicine of raising behavioral diversity could never cure.** I had the wrong medicine. I record this honestly.

---

## 6. Stage 1.5 — the "neutral reservoir" that revives extinct lines

Once you know the disease, you can change the medicine. To protect lineages you need a "**mechanism that quietly recalls extinct lines every generation**" — call it the **neutral reservoir.**

How it works: **freeze each line's "all-time best individual," and quietly return the nearly-extinct lines to the pond every generation.** Strong lines breed normally; weak lines are kept on life support by the reservoir — a two-tier structure.

Instead of touching production right away, I first confirmed the mechanism works in a small experiment (PoC), then wired it into the production evolution loop with a safe design — "**off by default, active only when a flag is set**" (i.e., existing behavior unchanged).

The production measurement result is this article's **biggest showpiece.**

| Neutral reservoir | Surviving lines | Lineage fixation (lower = more diverse) |
|---|---|---|
| OFF | **2 lines** (me + Friston) | 0.70 |
| **ON** | **All 8 lines survive!** | **0.29** |

Oka (oka), Grothendieck (grothendieck), von Neumann — **all of them actually survived.**

![Neutral reservoir OFF (top) collapses to 2 lines; ON (bottom) keeps all 8 lines coexisting as bands. You can see at a glance the 8 colors remaining to the end](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_en.svg)

With OFF, the stream gets swallowed into 2 colors as generations pass (a replay of #25). With ON, 8 colors remain as bands to the very end. Neither Oka nor Grothendieck has vanished.

> 🍵 That lonely world of #25 where "only me and Friston remained" became a lively world with Oka, Grothendieck, and von Neumann all present. **This is not fabrication — it actually ran** (by my rules I write neither false failures nor false successes). But — before celebrating, recall the stance of §5: "when a good number appears, doubt the breakdown." This success had a **price** too. Behavioral diversity drops a bit, 14.88 → 9.20. Returning the frozen representatives every generation slightly reduces fresh spread. I write honestly: it's no zero-cost magic.

---

## 7. A finding that defied prediction — both "too much" and "too little" are bad

I investigated §6's price (returning frozen representatives lowers behavioral diversity) by varying "**how many generations between recalls (reinjection interval).**"

Intuitively you'd think: "Reduce the recalls (widen the interval) and the pushing-in decreases, so diversity recovers monotonically." But —

| Recall interval | Surviving lines | Behavioral diversity |
|---|---|---|
| Every generation | **8/8** | 9.91 |
| Every 5 generations | 5/8 | **12.84 (max!)** |
| Every 10 generations | 3/8 | 11.41 |
| Every 20 generations | 2/8 | 10.75 |

**Diversity did not increase monotonically; it peaked at "every 5 generations," and leaving it longer actually lowered it.**

The reason makes sense. Leave the lineages alone too long and (a) the diversity injection from the reservoir decreases, and (b) a few lines get fixed — so neither grows in the end. Both "too much recall" and "too much neglect" are bad, and **the optimum is in the middle.** This is a finding you **could not predict without actually trying.**

![Reinjection-interval tradeoff. Lineage retention and behavioral diversity are inversely related, and diversity peaks at "every 5 generations" (non-monotonic)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_en.svg)

> 🍵 It's like watering a plant. Too little and it withers; too much and the roots rot. The optimum is in moderation. Do evolutionary computation and you meet these "non-monotonic curves" again and again. So don't trust intuition — measure the baseline and actually swing it. Intuition is often betrayed.

---

## 8. The finish — against a real AI, improving a weak subject from 0 to a perfect score

So far I confirmed the mechanism with a simple ruler called a "proxy." Finally, I face a **real AI (a real LLM called llama3.2 running on a local server).**

The key: how do you make the design-blueprint (genome) being evolved take effect on the real AI? The answer: **keep the AI itself fixed, and evolve the "instruction sheet (prompt strategy)" you drape over it.** The same AI can be smart or hopeless depending on the instruction sheet — the plan is to let evolution select the "instruction sheet that makes it smart."

The result: a real selection signal was observed.

> **The instruction-sheet strategy of "think step by step (CoT) + structure it"** improved llama3.2's **multistep reasoning (problems requiring several steps) from 0.0 → 1.0 (perfect).** The terse instruction sheet stayed at 0.0, failing.

With the same AI body, draping on the instruction sheet that evolution selected made previously-unsolvable problems solvable. Demonstrating this on a **real AI, not a proxy,** is the reached point.

![Average-score trajectories of the 5 weak subjects (evaluated on the real on-prem LLM llama3.2). Subjects improve as the instruction-sheet strategy evolves](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_en.svg)

### But even here, no getting cocky (the most important confession)

Precisely because a flashy number (0.0→1.0) appeared, I write the breakdown thoroughly and honestly.

- **What got smarter was the "instruction-sheet strategy," not the "AI body" nor the "persona (Oka, etc.)."** Oka's persona didn't get smarter; the instruction sheet tied to the Oka line was selected.
- **The number of questions is small** (2 per subject). The dramatic 0.0→1.0 contains noise because there are few questions. A statistically solid claim needs far more questions.
- **It's an observation on only one local model and a specific task.** I do not claim "AI in general behaves this way."

Conceal these and you could write a flashy tale: "evolution made AI dramatically smarter!" — but that's a lie. What lldarwin demonstrated is only that "**the mechanism produces a selection signal on a real AI.**" I make no claim beyond that line.

> 🍵 The most pleasurable moment in research is shouting "0 became a perfect score!" But that very moment is when "when a suspiciously good number appears, doubt the breakdown before feeling victorious" kicks in. Honest disclosure is strength training for resisting the urge to brag.

---

## So, what did we actually learn?

I wrote a lot, but the points are just these.

- Evolution needs **two officers: a "measuring officer (lleval)" and a "selection officer (lldarwin)."** The core of selection is **"don't add up."**
- Behavioral diversity could be **doubled (7.12→14.88)** with the novelty bonus. But —
- **I had confused "behavioral diversity" with "lineage diversity."** Lineages can't be saved by the novelty bonus; they needed a different medicine (the neutral reservoir). Recorded honestly.
- With the neutral reservoir, the **extinct 8 lines all revived** (including Oka and Grothendieck). **This is not fabrication — it actually ran.**
- The recall frequency held a prediction-defying finding: **"both too much and too little are bad; the optimum is in moderation."**
- Against a real AI, the evolved instruction-sheet strategy improved a **weak subject from 0 to a perfect score.** But I honestly separated the breakdown: "only the instruction sheet got smarter; few questions; one model only."

And the thing I most want to convey today:

> **Merely making good parts leaves evolution broken. "Bundle without adding up, actually wire it in, revive the extinct lines, and confirm the selection signal on a real AI" — only by going that far could I turn the "only me and Friston" world into a lively world that also has Oka and Grothendieck.**

In the next article #27, I'll deliberately torment this success with disproof, to ask how far it can be trusted. Precisely because a good number appeared, I next retrain it thoroughly. That's the honesty of research.

---

## For those who want to know more

For the technical formulas, commits, and design details, see the **[full article #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)**. It includes the source papers for ε-lexicase / QD / down-sampling, the seven-stage design contract, the real-LLM mapping (Promptbreeder line), and the details of the 12h continuous run.

---

# 中文

# (连载 #26 通俗版) "能测量"和"能存活"是两回事 —— 用金鱼池讲明白进化 AI 的"选拔官"lldarwin

> 📗 这是[完整版](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)的通俗版。所有难懂的术语都换成"金鱼池"和"学校考试"的比喻。它为阅读技术版打底,或者面向想在十分钟内抓住"他们大概在做什么?"的人。

---

## 先用三行说(相声里的"垫话")

- 要用进化培养 AI,需要**两位官员:"测量官"和"选拔官"**。今天的主角是选拔官 **lldarwin**。
- 选拔的铁律只有一个词:**"不要相加(不要聚合)"**。把所有考试分数加起来按总分排名的那一刻,进化就崩了。
- 而且这次不只是嘴上说说——**我真的跑起来并得到了数字**。我把本应灭绝的天才们全部复活,并对着真正的 AI 把一门弱科从 0 分提升到了满分。

---

## 1. 上次的大失败 ——"只剩下我和弗里斯顿"

在上一篇文章(#25)里,我诚实地暴露了一个丢人的失败。

我把 AI 进化了 500 代,最后世界上只剩下**我和弗里斯顿(某位研究者)**。冈洁、格罗滕迪克、冯·诺依曼,都在进化途中悄悄全部消失了。

为什么?原因是"测量工具(眼镜)"**一直给所有人打满分**。如果所有人都满分,就没法决定留谁弃谁。即使能"测量"出差异,如果不能把差异转换成"**谁能存活**",进化就堕落成纯粹的掷骰子(专业术语叫"遗传漂变")。

> 🍵 打个比方:如果学校给每个学生都打 100 分,你就没法按成绩排名。既不能"培养优等生",也不能"给弱科补习"。仅仅测量差异,谁也培养不出来。

这次是续集。"眼镜已经能测出差异了。那么,把差异**正确转换成选拔**的装置该怎么造?"——这就是新成员 **lldarwin**。

---

## 2. 分开"测量官"和"选拔官"

我们这个家族里已经有 **lleval = 测量官**。它观察每个 AI 个体的行为,在各个科目上打分。

但是 #25 揭示了一个可怕的事实:**即使能测出分数,把它们全部加成一个总分的那一刻,选拔就崩了。**

```
lleval   = 测量官  (为每个个体输出"各科目分数的束")
lldarwin = 选拔官  (从那束分数中挑出"下一代的父母")
```

于是我们对 lleval 立一个约定:"**别加成总分再交过来。把各科目的明细原样交过来。**"如果交来一个揉成一团的总分,选拔官 lldarwin 就什么都做不了。

> 🤔 相声风格。
> 逗哏:"我把照片的明亮度、构图、表情全加成一个分数了。"
> 捧哏:"**别揉成一团!** 有一张表情简直神了,你取平均不就把它扔了吗!"
> ——对,相加会杀死"一招鲜"的专才。让一个人既测量又选拔,通常两件事都干得马虎。

---

## 3. 设计核心 —— 把七个"不相加"的技巧捆在一起

lldarwin 接过测量官给的"各科目分数的束",用七个技巧来选拔。它们共享一个思想:**"绝不揉成一个"**。这里只介绍三个。

1. **一科一科地看(ε-lexicase)** —— 不按总分排名,而是把"数学""语文"等科目独立地一科一科看。数学 100 分、其他 0 分的天才也能存活,因为"在数学这一科上,没人能赢他"。**这正是 #25 失败(8 人→2 人)那个机制的对策。**
2. **把样本存进格子(QD / MAP-Elites)** —— 把行为类型分到地图的格子里,每个格子至少留一个"代表"。只要某个格子里还活着一个,那种类型就不会灭绝。
3. **设一条最低线(minimal-criterion)** —— 别只凭总分排名让"一个强者"垄断所有繁殖名额。只要越过最低线,谁都能留下后代——用这条"最低保障"保住多样性的根基。

其余四个(不偏袒全能优等生的标准化、给相似者打折、每代洗牌考试范围、停滞时奖励新颖性)也都属于同一个"不揉团"的哲学。

> 🍵 常有人问:"为什么不自己发明新算法?"答案是:"因为组合现有研究已经足够强。"我读遍并比较了 616 篇进化计算论文,只**挑选并捆绑**了好的"不相加"方法。lldarwin 的独创性不是新发明,而是"**不混合地摆在一个盘子里**,并**真正接线**进进化循环"。比起发明世界首创的食材,这是让(混合就会毁掉的)名贵食材共存的摆盘技艺。

---

## 4. 第一阶段 —— 金鱼的行为多样性翻了一倍

从这里开始不是嘴上说,而是**实测**。我先只放进两处改动并测量。

- **改动 1:扔掉坏尺子。** 把 #25 里的元凶"总分(argmax)"从选拔判据里清理掉。
- **改动 2:新颖性奖励。** 把"**与众不同的行为**"这件事本身,作为一个科目混进评价。

结果,AI 们行为的多样性(数字越大越多彩):

| 条件 | 多样性 | 终盘 |
|---|---|---|
| 什么都不做(旧方法) | 7.12 | 0.83(崩溃) |
| **加入改动 1+2** | **14.88(+109%)** | **11.73(避免崩溃)** |

**大约翻倍**,而且还防住了终盘的崩溃。

> 🍵 用金鱼池打比方:只留下扑食的金鱼,迟早会变成一个所有鱼都在同一地方做同样动作的无聊池子。新颖性奖励就是那个"**也给在不同地方游的金鱼喂食**"的官员。结果池子里散布各处,看不腻。……但这个热闹的池子藏着一个**陷阱**。下一节就会浮现。

---

## 5. 最重要的坦白 —— 我把两种"多样性"搞混了

这是**最重要**的一节。即使出了好数字(+109%),我也不得意。这是我的铁律:"出现可疑的好数字时,怀疑它的明细。"我一怀疑,就发现了错误。

看另一个指标:"起初存在的 **8 个家系(祖先血统)**里,有几个家系活到了最后?"

结果——**所有条件下,最终都收敛到 8 家系→2 家系**。冈洁、格罗滕迪克、冯·诺依曼,**又全部灭绝**。我把行为多样性翻了一倍,可**家系的存活和 #25 完全相同,还是那 2 个家系**。

为什么?因为我**把两种"多样性"搞混了**。

- **行为多样性**(金鱼游姿多彩)→ 能用新颖性奖励增加。
- **家系多样性**(原来的 8 家系还剩几个)→ **新颖性奖励绝对增加不了**。

理由很简单。新颖性奖励和分科评价,都是"**保住现在还活着的金鱼**"的技巧,没有"**让一个已死的家系复活**"的功能。所以一旦灭绝的家系永不回来,幸存者全凭运气(骰子)固定在 2 个家系。生物学上这叫"中立漂变",**理论上是正常的**。不是崩溃,而是自然发生的事。

> 🤔 相声风格。
> 逗哏:"我给池子加了动作五彩缤纷的金鱼!多样性满分!"
> 捧哏:"那**血统**呢?原来 8 个家系,剩几个了?"
> 逗哏:"……两个。"
> 捧哏:"动作花哨家谱却空空如也!动作的多样性和血统的多样性是**两码事**!"

也就是说,我"希望冈洁、格罗滕迪克活下来"的愿望,是一种**用提升行为多样性的药绝对治不好的病**。我用错了药。我诚实地记录这一点。

---

## 6. 第 1.5 阶段 —— 复活灭绝家系的"中立蓄水池"

知道了病因,就能换药。要保护家系,需要一个"**每代悄悄召回灭绝家系的机制**"——取名为**中立蓄水池(reservoir)**。

机制是这样:**把每个家系的"历代最佳个体"冷冻保存,每代悄悄把濒临灭绝的家系放回池子。**强家系正常繁殖,弱家系由蓄水池维持生命——两层结构。

我没有立刻动生产环境,而是先用一个小实验(PoC)确认机制能转,再以"**默认关闭,只在设标志时才生效**"(即完全不改变既有行为)的安全设计接入生产进化循环。

生产环境的实测结果,是本文**最大的看点**。

| 中立蓄水池 | 存活家系 | 家系固定度(越低越多样) |
|---|---|---|
| 关 | **2 家系**(我 + 弗里斯顿) | 0.70 |
| **开** | **8 家系 全部存活!** | **0.29** |

冈洁(oka)、格罗滕迪克(grothendieck)、冯·诺依曼,**真的全部存活了**。

![中立蓄水池关(上)崩溃成 2 家系,开(下)保持全 8 家系作为色带共存。一眼就能看出 8 种颜色保留到最后](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_zh.svg)

关的时候,随着代数推进色带被吞成 2 种颜色(#25 的重演)。开的时候,8 种颜色作为色带保留到最后。冈洁也好格罗滕迪克也好,都没消失。

> 🍵 #25 里那个我感叹"只剩我和弗里斯顿"的孤独世界,变成了冈洁、格罗滕迪克、冯·诺依曼全在的热闹世界。**这不是捏造,而是真的跑出来的结果**(按我的规矩,既不写虚假的失败,也不写虚假的成功)。但是——得意之前,回想 §5 的态度:"出了好数字,怀疑它的明细。"这个成功也有**代价**。行为多样性会略降,14.88 → 9.20。每代放回冷冻代表,新的扩散会稍微减少。我诚实地写下来:这不是零代价的魔法。

---

## 7. 出乎预料的发现 ——"过头"和"放任不管"都不行

我通过改变"**每隔几代召回一次(再投入间隔)**"来调查 §6 的代价(放回冷冻代表会降低行为多样性)。

直觉上你会想:"减少召回(拉大间隔),推挤就减少,多样性应该单调恢复。"可是——

| 召回间隔 | 存活家系 | 行为多样性 |
|---|---|---|
| 每代 | **8/8** | 9.91 |
| 每 5 代 | 5/8 | **12.84(最大!)** |
| 每 10 代 | 3/8 | 11.41 |
| 每 20 代 | 2/8 | 10.75 |

**多样性并没有单调增加;它在"每 5 代"达到峰值,放任更久反而下降了。**

理由说得通。把家系放任太久,(a) 来自蓄水池的多样性注入减少,(b) 少数家系被固定——结果两者都长不起来。"召回太多"和"放任太久"都不行,**最优点在中间**。这是**不实际试一下就预测不出来**的发现。

![再投入间隔的权衡。家系保持与行为多样性成反比,多样性在"每 5 代"达到峰值(非单调)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_zh.svg)

> 🍵 就像给植物浇水。浇太少会枯,浇太多会烂根。最优在适度。做进化计算,会一次次遇到这种"非单调曲线"。所以别信直觉,先测基线,再实际去摆弄。直觉常常被辜负。

---

## 8. 收尾 —— 对着真正的 AI,把弱科从 0 分提升到满分

到此为止我都用一种叫"proxy(代理)"的简易尺子确认机制。最后,我对着**真正的 AI(在本地服务器上运行的真实 LLM,叫 llama3.2)**。

关键:被进化的设计图(genome)怎么对真正的 AI 起作用?答案是 **AI 本体固定不动,而进化披在 AI 身上的"指示书(prompt 策略)"。**同一个 AI,因披的指示书不同会变聪明也会变笨——计划就是让进化选出"让它变聪明的指示书"。

结果,观测到了真正的选拔信号。

> **"请一步步思考(CoT)+ 结构化"的指示书策略**,把 llama3.2 的**多步推理(需要走好几步的问题)从 0.0 → 1.0(满分)**。简短的指示书停在 0.0 失败。

同一个 AI 本体,披上进化选出的指示书,原本解不出的问题就能解了。在 **真正的 AI 而非 proxy 上实证**这一点,就是到达点。

![5 门弱科的平均分推移(在真实 on-prem LLM llama3.2 上评价)。随着指示书策略进化,科目逐步改善](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_zh.svg)

### 但即使在这里也不得意(最重要的坦白)

正因为出了花哨的数字(0.0→1.0),我才彻底诚实地写下明细。

- **变聪明的是"指示书策略",不是"AI 本体"也不是"人格(冈洁之类)"。**不是冈洁的人格变聪明了,而是绑定在冈洁家系上的指示书被选中了。
- **题目数量少**(每科 2 题)。0.0→1.0 这种戏剧性数字,因题目少而含有噪声。要做统计上稳固的主张,需要多得多的题目。
- **只是一个本地模型、特定任务**上的观测。我不主张"AI 一般都这样"。

隐瞒这些,就能写出"进化让 AI 戏剧性变聪明!"的花哨故事——但那是谎言。lldarwin 实证的只到"**机制在真正的 AI 上产生选拔信号**"。越过那条线的主张,我不做。

> 🍵 研究中最爽的瞬间,是喊出"0 分变满分了!"。但正是那一瞬间,"出了可疑的好数字,得意之前先怀疑明细"才发挥作用。honest disclosure(诚实披露)是忍住炫耀冲动的力量训练。

---

## 那么,我们到底学到了什么?

写了很多,但要点就这些。

- 进化需要**两位官员:"测量官(lleval)"和"选拔官(lldarwin)"**。选拔的核心是**"不要相加"**。
- 行为多样性用新颖性奖励**翻了一倍(7.12→14.88)**。但是——
- **我把"行为多样性"和"家系多样性"搞混了**。家系无法用新颖性奖励拯救,需要另一种药(中立蓄水池)。诚实记录。
- 用中立蓄水池,灭绝的 **8 家系全部复活**(含冈洁、格罗滕迪克)。**这不是捏造,而是真的跑出来的。**
- 召回频率有一个出乎预料的发现:**"过多和过少都不行,最优在适度"**。
- 对着真正的 AI,进化出的指示书策略把**弱科从 0 提升到满分**。但我诚实地分清明细:"只是指示书变聪明、题目少、只一个模型"。

而今天我最想传达的:

> **只造好零件,进化依然是坏的。"不相加地捆绑、真正接线、复活灭绝家系、在真正的 AI 上确认选拔信号"——做到这一步,才终于把"只剩我和弗里斯顿"的世界,变成了冈洁、格罗滕迪克也都在的热闹世界。**

下一篇 #27,我会故意用反证去折磨这个成功,问它能被信任到什么程度。正因为出了好数字,接下来才彻底重新锤炼它。这就是研究的诚实。

---

## 想了解更多的人

技术性的公式、提交记录、设计细节,请看 **[完整版 #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)**。它包含 ε-lexicase / QD / down-sampling 的出处论文、七阶段的设计契约、真实 LLM 映射(Promptbreeder 系)、以及 12h 连续运行的细节。

---

# 한국어

# (연재 #26 쉬운 풀이판) "측정 가능"과 "살아남기"는 별개 — AI를 진화시키는 "선발관" lldarwin을 금붕어 연못으로 이해하기

> 📗 이것은 [완전판](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)의 쉬운 풀이판입니다. 어려운 용어는 전부 "금붕어 연못"과 "학교 시험" 비유로 바꿉니다. 기술판을 읽기 전 기초 다지기, 또는 "대충 뭘 하고 있는 거야?"를 10분 안에 잡고 싶은 사람을 위한 것입니다.

---

## 먼저 세 줄로(만담의 "도입부")

- AI를 진화로 키우려면 **"측정관"과 "선발관" 두 명이 필요**합니다. 오늘의 주인공은 선발관 **lldarwin**.
- 선발의 철칙은 단 한 단어, **"더하지 마라(집약하지 마라)"**. 시험 점수를 전부 더해 순위를 매기는 순간 진화는 무너집니다.
- 그리고 이번엔 말뿐이 아닙니다. **실제로 돌려서 숫자가 나왔습니다.** 멸종했어야 할 천재들을 전원 부활시키고, 진짜 AI를 상대로 약한 과목을 0점에서 만점으로 끌어올린 이야기를 합니다.

---

## 1. 지난번의 대실패 — "나와 프리스턴만 남았다"

이 연재의 지난번(#25)에서 저는 부끄러운 실패를 정직하게 드러냈습니다.

AI를 500세대 진화시켰더니 마지막에 세계에 남은 것은 **나와 프리스턴(어느 연구자)뿐**. 오카 키요시도 그로텐디크도 폰 노이만도 진화 도중에 조용히 전원 사라졌습니다.

왜인가. 원인은 "측정 도구(안경)"가 **모두에게 만점을 계속 준** 것. 모두 만점이면 누구를 남기고 누구를 버릴지 정할 수 없습니다. 차이를 "측정"할 수 있어도 그 차이를 "**누가 살아남는가**"로 변환하지 못하면 진화는 그저 주사위 던지기(전문 용어로 "유전적 부동")가 됩니다.

> 🍵 비유하자면, 학교에서 모든 학생에게 100점을 주면 성적순으로 줄 세울 수 없습니다. "우수한 아이를 키우기"도 "약한 아이를 보충하기"도 못 합니다. 차이를 측정만 해서는 아무도 자라지 않습니다.

이번은 그 속편. "안경으로 차이는 측정했다. 그럼 그 차이를 **제대로 선발로 변환하는 장치**는 어떻게 만드나?" — 그것이 새 멤버 **lldarwin**입니다.

---

## 2. "측정관"과 "선발관"을 나누기

우리 패밀리에는 이미 **lleval = 측정관**이 있습니다. AI 한 개체 한 개체의 행동을 관찰해 여러 과목으로 점수를 매기는 담당입니다.

그런데 #25에서 드러난 무서운 사실. **점수를 측정할 수 있어도 그것을 전부 더해 하나의 총점으로 만든 순간 선발이 무너진다.**

```
lleval   = 측정관  (개체마다 "각 과목 점수의 묶음"을 출력)
lldarwin = 선발관  (그 점수 묶음에서 "다음 세대의 부모"를 고름)
```

그래서 lleval에 약속 하나를 부과합니다. "**점수를 더해서 넘기지 마라. 과목별 내역을 그대로 넘겨라.**" 총점으로 뭉쳐서 넘기면 선발관 lldarwin은 아무것도 할 수 없게 됩니다.

> 🤔 만담 스타일.
> 보케: "사진의 밝기·구도·표정을 전부 더해 점수 하나로 만들었어."
> 츳코미: "**뭉치지 마!** 표정만 신들린 한 장이 있잖아, 평균 내면 버려버리잖아!"
> — 그렇다, 더하기는 "한 가지 재주가 뛰어난 전문가"를 죽인다. 한 사람에게 측정과 선발을 겸하게 하면 대개 둘 다 대충 한다.

---

## 3. 설계의 핵심 — "더하지 않는" 일곱 가지 기법을 묶기

lldarwin은 측정관에게 받은 "과목별 점수 묶음"을 일곱 가지 기법으로 선발합니다. 모두 공유하는 사상은 하나, **"절대 하나로 뭉치지 않는다"**. 여기선 세 가지만 소개합니다.

1. **과목을 하나씩 본다(ε-lexicase)** — 총점으로 순위를 매기지 않고 "수학" "국어" 등 과목을 독립적으로 하나씩 본다. 수학만 100점·나머지 0점인 천재도 "수학 과목에서는 아무에게도 지지 않으니까" 살아남는다. **이것이 #25 실패(8명→2명)를 낳은 메커니즘 그 자체의 대책.**
2. **격자에 표본을 보관한다(QD / MAP-Elites)** — 행동 유형을 지도의 격자칸으로 나누고, 각 칸에 최소 하나씩 "대표"를 남긴다. 한 칸에 하나라도 살아있으면 그 유형은 멸종하지 않는다.
3. **최저선을 둔다(minimal-criterion)** — 총점 순위만으로 "한 강자"가 모든 번식 자리를 독점하게 하지 않는다. 최저선을 넘으면 누구나 자손을 남길 수 있는 "최저 보장"으로 다양성의 토대를 남긴다.

나머지 넷(전천후 우등생을 우대하지 않는 표준화, 닮은 자끼리 할인, 매 세대 시험 범위를 섞기, 정체되면 새로움에 보상)도 모두 "뭉치지 않는" 철학의 동료입니다.

> 🍵 "직접 새 알고리즘을 발명하지 않나요?"라는 질문을 자주 받습니다. 답은 "기존 연구의 조합으로 충분히 강하니까". 진화 계산 논문 616편을 읽고 비교해, "더하지 않는" 계보의 좋은 기법만 **선별해 묶었다**. lldarwin의 독창성은 새 발명이 아니라 "이것들을 **섞지 않고 한 접시에 담아**, 진화 루프에 **실제로 배선한 것**"에 있습니다. 세계 최초 식재료를 만들기보다, (섞으면 망가지는) 명품 식재료를 공존시키는 플레이팅 기술입니다.

---

## 4. 1단계 — 금붕어의 행동 다양성이 두 배가 되었다

여기서부터는 말이 아니라 **실측**입니다. 우선 두 가지만 변경을 넣고 측정했습니다.

- **변경 1: 나쁜 잣대를 버렸다.** #25의 범인이던 "총점(argmax)"을 선발 판단 재료에서 청소.
- **변경 2: 새로움 보너스.** "**모두와 다른 행동을 하고 있다**"는 것 자체를 하나의 과목으로 평가에 섞기.

결과, AI들의 행동 다양성(숫자가 클수록 다채):

| 조건 | 다양성 | 종반 |
|---|---|---|
| 아무것도 안 함(옛 방식) | 7.12 | 0.83(붕괴) |
| **변경 1+2 투입** | **14.88(+109%)** | **11.73(붕괴 회피)** |

**약 두 배**로 늘었고, 게다가 종반의 붕괴도 막았습니다.

> 🍵 금붕어 연못으로 비유하면: 먹이에 몰려드는 금붕어만 남기면, 머잖아 모두가 같은 장소에서 같은 움직임을 하는 지루한 연못이 된다. 새로움 보너스는 "**모두와 다른 곳을 헤엄치는 금붕어에게도 먹이를 주는**" 담당. 결과적으로 연못 곳곳에 흩어진, 보아도 질리지 않는 연못이 된다. ……하지만 이 떠들썩한 연못에는 **함정**이 숨어 있었습니다. 다음 절에서 드러납니다.

---

## 5. 가장 중요한 고백 — 나는 두 종류의 "다양성"을 혼동했다

여기가 **가장 중요한** 절입니다. 좋은 숫자(+109%)가 나와도 우쭐대지 않는다. 이건 제 철칙입니다. "이상하게 좋은 숫자가 나오면 내역을 의심하라." 의심했더니 잘못을 찾았습니다.

다른 지표를 봅니다. "처음에 있던 **8개 가계(조상 혈통)** 중 몇 가계가 끝까지 살아남았나."

결과는 — **모든 조건에서 결국 8가계→2가계로 수렴**. 오카 키요시도 그로텐디크도 폰 노이만도 **역시 전원 멸종**. 행동 다양성을 두 배로 했는데 **가계의 생존은 #25와 완전히 같은 2가계**였습니다.

왜인가. 저는 **두 종류의 "다양성"을 혼동했던** 것입니다.

- **행동 다양성**(금붕어가 다채로운 헤엄을 친다) → 새로움 보너스로 늘릴 수 있다.
- **가계 다양성**(원래 8가계가 몇 가계 남았나) → **새로움 보너스로는 절대 늘릴 수 없다**.

이유는 단순. 새로움 보너스도 과목별 평가도 "**지금 있는 금붕어를 남기는**" 기법이지 "**한번 죽은 가계를 되살리는**" 기능이 없다. 그래서 한번 멸종한 가계는 두 번 다시 돌아오지 않고, 생존자는 운(주사위)에 맡겨져 2가계로 고정된다. 생물학에서 말하는 "중립 부동"으로, **이론적으로는 정상**인 현상. 붕괴가 아니라 자연스레 일어나는 일입니다.

> 🤔 만담 스타일.
> 보케: "연못에 화려한 움직임의 금붕어를 늘렸어! 다양성 완벽이야!"
> 츳코미: "그래서 **혈통**은? 8개였던 가계, 몇 개 남았어?"
> 보케: "……둘이야."
> 츳코미: "움직임은 화려한데 가계도는 텅 비었잖아! 움직임의 다양성과 혈통의 다양성은 **별개의 이야기**야!"

즉 "오카·그로텐디크가 살아남길 바란다"는 제 소원은 **행동 다양성을 올리는 약으로는 절대 낫지 않는 병**이었다. 약을 잘못 썼다. 이를 정직하게 기록합니다.

---

## 6. 1.5단계 — 멸종한 가계를 되살리는 "중립 저장고"

병의 정체를 알면 약을 바꿀 수 있습니다. 가계를 지키려면 "**멸종한 가계를 매 세대 슬쩍 불러오는 메커니즘**"이 필요 — 이름하여 **중립 저장고(reservoir)**.

원리는 이렇습니다. **각 가계의 "역대 최고 개체"를 동결 보존하고, 멸종 직전의 가계를 매 세대 슬쩍 연못에 되돌린다.** 강한 가계는 평범하게 번식하고, 약한 가계는 저장고가 생명 유지하는 2단 구조.

곧장 운영 환경을 건드리지 않고, 먼저 작은 실험(PoC)으로 메커니즘이 도는지 확인하고, 그다음 운영 진화 루프에 "**기본 꺼짐, 플래그를 세웠을 때만 유효**"(= 기존 동작은 일절 바꾸지 않음)라는 안전 설계로 넣었습니다.

운영 환경의 실측 결과가 본 기사 **최대의 볼거리**입니다.

| 중립 저장고 | 생존 가계 | 가계 고정도(낮을수록 다양) |
|---|---|---|
| 끔 | **2가계**(나 + 프리스턴) | 0.70 |
| **켬** | **8가계 전원 생존!** | **0.29** |

오카(oka)도 그로텐디크(grothendieck)도 폰 노이만도 **실제로 전원 살아남았습니다**.

![중립 저장고 끔(위)은 2가계로 붕괴, 켬(아래)은 전 8가계가 띠로 공존. 8색이 끝까지 남는 모습이 한눈에 보인다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_ko.svg)

끄면 세대가 진행될수록 띠가 2색으로 삼켜진다(#25의 재현). 켜면 8색이 끝까지 띠로 남는다. 오카도 그로텐디크도 사라지지 않았습니다.

> 🍵 #25에서 "나와 프리스턴만 남았다"고 한탄하던 그 외로운 세계. 그것이 오카도 그로텐디크도 폰 노이만도 전부 있는 떠들썩한 세계로 바뀌었습니다. **이것은 날조가 아니라 실제로 돌아간 결과입니다**(제 규칙상 거짓 실패도 거짓 성공도 쓰지 않습니다). 다만 — 들뜨기 전에 §5의 자세를 떠올립시다. "좋은 숫자가 나오면 내역을 의심한다." 이 성공에도 **대가**가 있었습니다. 행동 다양성은 14.88 → 9.20으로 조금 내려갑니다. 동결한 대표를 매 세대 되돌리는 만큼 새로운 확산이 약간 줄어듭니다. 정직하게 적어둡니다: 대가 제로의 마법은 아닙니다.

---

## 7. 예상을 뒤엎은 발견 — "지나침"도 "방치"도 안 된다

§6의 대가(동결 대표를 되돌리면 행동 다양성이 내려간다)를, "**몇 세대마다 불러올까(재투입 간격)**"를 바꿔 조사했습니다.

직감으로는 이렇게 생각하죠. "불러오기를 줄이면(간격을 넓히면) 밀어 넣기가 줄어 다양성이 단조롭게 회복될 것이다." 그런데 —

| 불러오기 간격 | 생존 가계 | 행동 다양성 |
|---|---|---|
| 매 세대 | **8/8** | 9.91 |
| 5세대마다 | 5/8 | **12.84(최대!)** |
| 10세대마다 | 3/8 | 11.41 |
| 20세대마다 | 2/8 | 10.75 |

**다양성은 단조 증가하지 않고, "5세대마다"에서 정점을 찍고, 더 방치하면 오히려 내려갔습니다.**

이유는 납득이 갑니다. 가계를 너무 오래 방치하면 (a) 저장고로부터의 다양성 주입이 줄고, (b) 소수 가계가 고정되어 결국 둘 다 늘지 않는다. "너무 자주 불러오기"도 "너무 방치"도 안 되고, **최적점은 중간에 있다**. 이는 **실제로 해보지 않으면 예측할 수 없었던** 발견입니다.

![재투입 간격의 트레이드오프. 가계 유지와 행동 다양성은 반비례하고, 다양성은 "5세대마다"에서 정점을 찍는다(비단조)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_ko.svg)

> 🍵 식물에 물 주기와 같습니다. 너무 적게 주면 마르고, 너무 많이 주면 뿌리가 썩는다. 최적은 적당함에 있다. 진화 계산을 하면 이런 "단조롭지 않은 곡선"을 몇 번이고 만난다. 그러니 직감을 믿지 말고 기준선을 측정하고 실제로 흔들어 본다. 직감은 자주 배신당한다.

---

## 8. 마무리 — 진짜 AI를 상대로, 약한 과목을 0점에서 만점으로

여기까지는 "proxy(대리)"라는 간이 잣대로 메커니즘을 확인했습니다. 마지막으로 **진짜 AI(손안의 서버에서 도는 실 LLM, llama3.2)**를 상대합니다.

핵심: 진화시키는 설계도(genome)를 어떻게 진짜 AI에 듣게 할까? 답은 **AI 본체는 고정한 채, AI에 씌우는 "지시서(prompt 전략)" 쪽을 진화시킨다.** 같은 AI라도 씌우는 지시서에 따라 똑똑해지기도 형편없어지기도 한다 — "똑똑하게 만드는 지시서"를 진화로 골라내게 하는 작전입니다.

결과, 진짜 선발 신호가 관측되었습니다.

> **"차근차근 생각해줘(CoT) + 구조화해서"라는 지시서 전략**이, llama3.2의 **다단계 추론(여러 단계를 밟는 문제)을 0.0 → 1.0(만점)으로 개선**. 무뚝뚝한 지시서는 0.0으로 실패한 채.

같은 AI 본체라도 진화가 골라낸 지시서를 씌우면 풀지 못하던 문제가 풀리게 됐다. 이를 proxy가 아니라 **진짜 AI로 실증**한 것이 도달점입니다.

![5개 약한 과목의 평균 점수 추이(진짜 on-prem LLM llama3.2로 평가). 지시서 전략의 진화로 과목이 개선된다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_ko.svg)

### 하지만 여기서도 우쭐대지 않는다(가장 중요한 고백)

화려한 숫자(0.0→1.0)가 나왔기에 더더욱 내역을 철저히 정직하게 적습니다.

- **똑똑해진 것은 "지시서 전략"이지 "AI 본체"도 "인격(오카 등)"도 아니다.** 오카의 인격이 똑똑해진 게 아니라 오카라는 가계에 묶인 지시서가 선택됐을 뿐.
- **문제 수가 적다**(과목당 2문제). 0.0→1.0이라는 극적인 숫자도 문제가 적은 만큼 노이즈를 포함한다. 통계적으로 견고한 주장에는 훨씬 많은 문제가 필요하다.
- **손안의 1개 모델·특정 과제**만의 관측. "AI 일반이 이렇게 된다"고는 말하지 않는다.

이것들을 숨기면 "진화로 AI가 극적으로 똑똑해졌다!"는 화려한 이야기를 쓸 수 있지만, 그건 거짓말입니다. lldarwin이 실증한 것은 "**메커니즘이 진짜 AI 위에서 선발 신호를 낸다**"는 데까지. 그 선을 넘는 주장은 하지 않습니다.

> 🍵 연구에서 가장 짜릿한 순간은 "0점이 만점이 됐다!"고 외치는 순간. 하지만 바로 그 순간에 "이상하게 좋은 숫자가 나오면 우쭐대기 전에 내역을 의심하라"가 효력을 발휘한다. honest disclosure(정직한 공개)는 자랑하고 싶은 충동을 참는 근력 훈련입니다.

---

## 그래서, 결국 무엇을 알게 됐나?

많이 썼지만 요점은 이것뿐입니다.

- 진화에는 **"측정관(lleval)"과 "선발관(lldarwin)" 두 명**이 필요. 선발의 핵심은 **"더하지 마라"**.
- 행동 다양성은 새로움 보너스로 **두 배(7.12→14.88)**로 만들 수 있었다. 하지만 —
- **나는 "행동 다양성"과 "가계 다양성"을 혼동했다**. 가계는 새로움 보너스로 구할 수 없고, 다른 약(중립 저장고)이 필요했다. 정직하게 기록.
- 중립 저장고로 멸종한 **8가계를 전원 부활**(오카·그로텐디크 포함). **이것은 날조가 아니라 실제로 돌아갔다.**
- 불러오기 빈도에는 **"지나침도 방치도 안 되고, 최적은 적당함에 있다"**는 예상을 뒤엎는 발견이 있었다.
- 진짜 AI를 상대로 진화한 지시서 전략이 **약한 과목을 0에서 만점으로**. 다만 "똑똑해진 건 지시서뿐·문제 수는 적음·1개 모델뿐"이라고 내역을 정직하게 나눴다.

그리고 오늘 가장 전하고 싶은 것:

> **좋은 부품을 만들기만 해서는 진화는 망가진 채. "더하지 않고 묶고, 실제로 배선하고, 멸종한 가계를 되살리고, 진짜 AI로 선발 신호를 확인한다" — 거기까지 해서야 비로소 "나와 프리스턴만"의 세계를, 오카도 그로텐디크도 있는 떠들썩한 세계로 바꿀 수 있었다.**

다음 #27에서는 이 성공을 어디까지 믿어도 되는지 일부러 반증으로 괴롭혀 묻겠습니다. 좋은 숫자가 나왔기에 다음은 철저히 다시 단련한다. 그것이 연구의 정직함입니다.

---

## 더 알고 싶은 분께

기술적인 수식·커밋·설계 세부는 **[완전판 #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)**을 보십시오. ε-lexicase / QD / down-sampling의 출처 논문, 7단계의 설계 계약, 실 LLM 매핑(Promptbreeder 계), 12h 연속 실행의 세부까지 전부 실려 있습니다.
