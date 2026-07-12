---
title: '【📗かみくだき版】一晩で AI 進化を作り直した夜 — 「本物の AI 先生」でテストしてもまた満点で詰んだ話（実 LLM 飽和→開放端への転回）'
tags:
  - FullSense
  - 進化計算
  - honest_disclosure
  - 解説
project_group: llive
private: true
id: 6b134e5a4f87963681c2
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 【📗かみくだき版】一晩で AI 進化を作り直した夜 — 「本物の AI 先生」でテストしてもまた満点で詰んだ話（実 LLM 飽和→開放端への転回）

![かみくだき獅子 — 噛まれた読者に「理解」のご利益](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi.svg)

> 📗 これは [完全版](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0) のかみくだき版です。数式・表・細かい数値は完全版に全部あります。ここでは「結局、何が起きて、何がわかったの?」を、たとえ話多めで 5〜10 分で掴める形にします。技術的な結論と「正直な失敗の告白」は、薄めずにそのまま残します。

---

## まず三行で（落語でいう「枕」）

落語には本題の前に軽い「枕」があります。まずは三行で。

- **また満点で詰んだ** — AI を「進化」で賢くしようとして、今度こそ本物の AI 先生（llama3.2 という、自宅 PC で動く LLM）に採点させた。12 時間ぶっ通しで回したら、**5 世代目で全員が満点を取り、そこから 65 世代、一ミリも伸びなかった**。
- **一晩で作戦を立て直した** — 自分で小さい実験を 6 本、別の AI 助手を 4 体並列で、さらに調べもの担当 AI（Perplexity）を 1 体。**全員が別々のやり方で、朝には同じ結論にたどり着いた**。
- **意外な「誰もやってない隙間」が見えた** — 進化を止めずに、進化し続けている集団をその場でまとめて 1 つの答えにする「**生バンド（ライブ・オーケストラ）方式**」が、世界中の先行研究にまだ無いと判明した。

ひとことで言うと——**「採点表（ものさし）が壊れたら、選抜のやり方をどれだけ磨いても無駄」**。だから磨く相手を変える。**採点表そのものを“終わらない作り”に変える**、が今回の結論です。

---

## 1. そもそも何をやってる研究なの?

私たちは「AI の頭脳の設計図を、生き物の進化みたいに少しずつ作り変えて、賢いやつを探す」という研究をしています。1 個の AI を必死に鍛えるのではなく、**たくさんの AI を“群れ”にして、世代交代させながら互いに競わせる**やり方です。

進化には 3 つの部品が要ります。

- **変異** … 設計をちょっと変えてみる
- **遺伝** … 良かった設計を子に引き継ぐ
- **選抜（適者生存）** … 良いやつを残し、ダメなやつを落とす ← ここが今回の主役

この「選抜」がちゃんと働くには、**良し悪しを測る“ものさし”（採点表）**が要ります。研究では、これを `lleval`（評価器）と呼んでいます。

そして連載の前回（#25）、私は大失敗をすでに告白しています。500 世代も進化させたら、**世界に「私」と「フリストン（種にした賢人の 1 人）」しか残らなかった**。原因は採点表が壊れていたこと。採点表が全員に満点をつけ続けたせいで、「誰を残しても同じ」状態になり、選抜が機能しなくなったのです。

> 🤔 **たとえ話**: クラス全員がいつも 100 点を取るテストでは、誰が優秀か分かりません。差がつかないので「優秀な子だけ残す」ができない。これが「採点表の飽和（満点張り付き）」です。

前回までは、ぜんぶ**“ニセ採点表”（proxy = コンピュータが機械的に出す合成のものさし）**で実験していました。ニセ採点表は「仕組みが回るか」は確かめられても、「本物の AI で意味ある進化が起きたか」までは言えません。だから当然の次の一手——**本物の AI 先生で確かめる**。これが今回の出発点です。

---

## 2. 出発点 —「本物の AI 先生」でも、正直に不合格だった

自宅 PC で動く本物の LLM（llama3.2）を採点者にして、12 時間ぶっ通しで進化させました。結果がこれです。

| 事実 | 値 | どういうこと? |
|---|---|---|
| 回った世代数 | 71 世代 / 12 時間 | 本物の AI は遅いので、これで精一杯 |
| 最高点 | **5 世代目で満点（1.0）→ 70 世代までずっと満点** | **早々に天井。65 世代が無進歩** |
| 平均点 | 0.85 で頭打ち | **上達が積み上がらない** |
| 全滅したか | していない（群れは生き残った） | 仕組み自体は壊れていない |

![本物の AI 先生（llama3.2）で進化させた 12 時間の記録。最高点が早々に天井に張り付き、その後ずっと平らなまま](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status.svg)

ここで「全滅しなかった! 満点に届いた!」と書けば、いかにも成功っぽい。でも FullSense には「**良い結果が出たら、勝った気になる前に必ず内訳を疑う**」という正直ルールがあります。内訳を見ると、出していたテストは 10 問。そのうち**8 問は数世代で全員が満点**。差がついていたのは難しい 2 問だけ。つまり「誰を選んでも同じ」が 8 割。

これは進化ではなく、**ただの「ふるい付きのランダム探し」**です。落ちこぼれは弾くけど、上達は積み上がらない。

**判定: 全滅はしてないが、進化にはなっていなかった。**

しかも衝撃だったのは、これが**ニセ採点表だけの問題ではなかった**こと。前回の失敗は「proxy だからでしょ?」で片付けられましたが、今回は本物の AI 先生でも同じ壁に当たった。

> 🤔 **たとえ話**: 採点者を「本物のベテラン先生」に格上げしても、**毎回まったく同じ問題用紙を配っていたら**、数回で全員が満点を取り、以降は何回テストしても差がつきません。悪いのは先生じゃない。**問題用紙が固定で簡単すぎる**のです。

つまり真犯人は「採点者（AI か proxy か）」ではなく、**「問題用紙が固定だったこと」**。ここが今回いちばん大事な気づきです。

> 🍵 **ひと休み**: ここで多くの人は「本物の AI でも詰みなら、もうお手上げでは?」と思います。私もそう思いました。でも「固定にしたのが間違い」なら、直すべきは選抜の仕組みでも AI でもなく、**問題用紙の作り方そのもの**。それを一晩かけて確かめにいきました。

---

## 3. 一晩の作戦 —「正解を 1 つの頭で決めない」

ユーザー（私自身が方向性を決める側）からの指示はこうでした。「大きな本番ランを 1 本回すより、**小さい実験を朝まで回しまくって“作戦を決める”**」。

そこで、こんな“6 人がかり”の体制を組みました。

| 担当 | 中身 |
|---|---|
| 私（本人） | 小さい実験（PoC）を 6 本、自分の手で回す |
| AI 助手 A | 「終わらない進化」を 1 万世代の大規模実験で検証 |
| AI 助手 B | 観測の道具づくり（誰がどう進化したか後から辿れるように） |
| AI 助手 C | 本物の AI で「群れの合奏」を検証 |
| 調べもの AI（Perplexity） | 世界の先行研究を漁って「これ既出?」を確認 |

なぜ 1 人（1 つの頭）で全部やらないのか? ここが今回の隠れた主役です。

> **同じ頭で考えた結論は、同じ思い込みに引きずられる。** だから、まったく別のやり方（自作の合成実験 / 本物の AI / 文献調べ）で**バラバラに**確かめて、それが偶然じゃなく**全部一致したときだけ**結論を信じる。これを「**独立クロス検証**」と呼びます。後半で、この威力が出ます。

正直な不発も 1 つ書いておきます。**部下として使うはずの Codex（別の AI）は、今回まったく使えませんでした。** アカウント設定の不一致で API がモデルを軒並み拒否。「使えるはずの道具が使えなかった」も、隠さず記録します。

---

## 4. 最初の決定打 — 問題を“だんだん難しく”したら、飽和は直った

最初に検証したい仮説は、いちばん根っこの問い。**「問題用紙を固定じゃなく、群れの実力に合わせてだんだん難しくしたら、飽和は直るのか?」**

合成のニセ採点表で（ただし条件を公平に揃えて）比べました。

- **固定の問題（baseline）**: 実力 0.627 で低空飛行のまま停滞。12 時間の病気をちゃんと再現。
- **適応難易度（みんなが解けるようになったら問題を難しくする）**: 実力が 0.952 まで上昇。**飽和が解けた!**

ところが、ここに落とし穴。難しくする過程で、**群れが 1 つの正解パターンに凝り固まってしまった**（多様性が崩壊）。金太郎飴です。

そこで「だんだん難しく」に、もう 1 つ足しました。**「変わった解き方にもご褒美をやる」**（研究では novelty = 新規性ボーナスと呼びます）。

| やり方 | 最終実力 | 多様性 |
|---|---|---|
| 固定の問題 | 0.627 | あり（でも低実力） |
| だんだん難しく | 0.952 | **崩壊（金太郎飴）** |
| **だんだん難しく + 変わり者にご褒美** | **0.881** | **維持** |

**「だんだん難しく + 変わり者にご褒美」の二刀流が、実力（固定比 +40%）と多様性を両立**しました。実力を少し（7%）譲るかわりに、多様性を完全に守った。

> 🤔 **たとえ話**: 全員が満点を取ったら問題を難しくする（=点が割れる）。でも今度は全員が同じ解き方に収束する。そこで「ヘンな解き方の子も褒める」を足すと、賢さと個性が両立する。**「難しくする」と「変わり者を褒める」の二刀流**が要点です。

---

## 5. 本丸 —「終わらない進化」を 1 万世代で徹底検証した

小さい実験で「方向」は見えました。次は大規模に厳密に。AI 助手 A に、**1 万世代 × 19 通りの設定**で「終わらない進化（open-ended）」かどうかを徹底検証させました。判定は「飽和せず、1 色に染まらず、多様性の貯蔵庫が増え続けるか」。

結果は驚くほどスッキリでした。

- **昔ながらの「点数を 1 本にまとめる選抜（scalar）」は、全部ダメ（飽和 + 1 色化）**。
- **「変わり者ボーナス（novelty）」や「問題ごとに別々に評価する選抜（lexicase）」は、全部うまくいった（終わらない進化が成立）**。

![昔ながらの選抜（崩壊）と、変わり者ボーナスありの選抜（維持）を 1 枚で対比。点線が崩れていくのが旧方式、平らに保たれるのが新方式](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay.svg)

ここで一番大事な発見はこれ。**「多様性の貯蔵庫（archive）を足すだけ」では救えなかった**こと。旧方式は、貯蔵庫を足してもやっぱり 1 色に染まって全滅した。救ったのは貯蔵庫ではなく、**選抜の仕方そのものを“終わらない作り”にすること**でした。

> 🍵 **ひと休み**: この記事でいちばん硬い節です。持ち帰ってほしいのは 1 行——**「貯蔵庫を足すだけじゃ救えない。選抜のやり方そのものを終わらない作りにしないと駄目」**。1 万世代の実データが、これを言い切ってくれました。

そして AI 助手 A は、良い結果が出たときこそ**自分から限界も指摘**してきました。「全体としては多様でも、特定の側面（思考のクセ）だけはこっそり 1 色になることがある」。これは正直な限界として記録し、別の対策（後述）を立てました。

---

## 6. 独自性の核 —「進化を止めずに、群れを生バンドで合奏させる」

飽和を避ける選抜の核が固まったので、次は「で、何が新しいの?（独自性）」です。

私が温めていたアイデアは——**進化し続けている群れを、止めずに、その場でまとめて 1 つの答えにする**。普通は「進化を止めて、できあがった最強の 1 体で答える」。でも私がやりたいのは、進化を**止めずに**、進化中の集団をそのままバンドのように合奏させて答えること。名付けて「**ライブ・オーケストラ**」。

調べもの AI（Perplexity）が、これを裏付けてくれました。

> 「進化しながら同時に答え続けるシステム」は、明確な先行研究が無い = **世界の研究の空白地帯（white-space）**。似たものはあるが、同一物はない。

つまり、まだ誰もやっていない隙間だった。ただし Perplexity は、舞い上がる私に**冷や水**もかけてきました。

> 2025 年の研究では、**「多様な群れで合奏すれば単体より強い」は自明ではない**。むしろ単一トップモデルの反復が、寄せ集めより強かった例がある。

> 🍵 **ひと休み**: ここ、研究の誠実さが試される分岐点です。「空白地帯だ! 独自性だ!」で舞い上がりたいところに、「でも多様性は自動的に良いわけじゃないよ」という反証が来る。**舞い上がる材料と冷や水を、同じ調査の中で両方受け取る。** これができると結論がぐっと強くなります。

---

## 7. 冷や水の正体 —「投票」じゃなく「振り分け」だった

「多様な群れの合奏は自動的に強くはない」——この反証の正体を、仕組みのレベルで解明したのが山場です。自分の合成実験（PoC #3）と、AI 助手 C の本物の AI 実験が、**別々に同じ答え**を出しました。

カギは「**まとめ方**」でした。

- **多数決（投票）でまとめると、多様性は逆効果**。各問題で本当に詳しい専門家 1 人が、無知な多数派に打ち消されてしまう。
- **詳しい人に振り分けてまとめると（routing）、多様性が活きる**。数学の問題は数学者に振る。

つまり——**「指揮者がいるオーケストラ」と「全員が好き勝手に音を出す雑踏」の違い**。投票は専門家を打ち消し、振り分け（指揮者）は専門家を活かす。

さらに上手い話があって、**この“指揮者の楽譜”（誰がどの問題に強いかの目印）は、多様性を管理するためにすでに計算してあるもの**を、そのまま使い回せました。一石二鳥です。

> 🔑 **これが本記事の核**: 合成実験（自作）と、本物の AI 実験（AI 助手 C）が、**まったく別のやり方で同じ結論**にたどり着いた。「合奏は“振り分け”でだけ単体を超える / 投票では超えない」。2 つが偶然じゃなく一致したからこそ、信じてよい。これが独立クロス検証の威力です。

> 🤔 **たとえ話**: 専門家 10 人に多数決させると、無知な多数派が正しい専門家を押し切ってしまう。だから「数学は数学者へ」と**振り分ける係（指揮者）**が要る。しかもその指揮者の楽譜は、別の目的でとっくに用意済みのものが使える。投票は専門家を打ち消し、指揮者が活かす。

---

## 8. おまけ —「自分で調べに行く AI」と「数を増やすほど多様になる」

独自性のアイデアはもう 2 つあって、それぞれ小さい実験で裏を取りました。

- **自分で調べに行く個体**: 個体が必要なときだけ自分で調べに行けるようにする。実験では、**「調べるのにコストをかけると、進化が“調べるべきときだけ調べる”という賢い使い分けを自分で身につけた」**。タダなら調べ放題、有料なら選んで調べる、を進化が勝手に学んだのです。
- **数を増やすほど多様になる**: 群れの数を 256 → 4096 まで増やすと、多様性が素直に増え続けた。しかも今回は群れを増やすぶん世代数を削った（**多様性に不利な条件**）のに、それでも増えた。だから「これは下限。本当はもっと効くはず」と正直に書けます。良い結果を「上限」と誇張せず「下限」と書くのも、正直ルールの一部です。

---

## で、結局何がわかったの?

一晩で、自作の実験 6 本も、4 体の AI 助手も、調べもの AI も、**バラバラのやり方で、朝には同じ結論**に着いていました。

1. **本物の AI 先生でも飽和した。** 「本物の LLM を使えば進化する」は嘘だった。真犯人は採点者ではなく、**問題用紙が固定だったこと**。
2. **貯蔵庫を足すだけでは救えない。** 救うのは「選抜のやり方そのものを“終わらない作り”にすること」。具体的には「変わり者ボーナス」「問題ごとに別評価」「だんだん難しく」「変わった解き方を保管」の合わせ技。
3. **多様性は自動的には良くない。** 合奏は「投票」だと逆効果、「指揮者による振り分け」でだけ価値になる。
4. **独立クロス検証が結論を強くする。** 同じ頭の結論は同じ思い込みを共有する。別々の手法が一致したときだけ信じる。
5. **正直さを核に。** 「本物の AI でも飽和した」「貯蔵庫だけでは救えなかった」「使えなかった道具（Codex）があった」——失敗も不発も、消さずに残す。

そして大事な但し書き。今回の実験の多くは**「仕組みが回るか」の確認**であって、「本物の AI が一般的に賢くなった」という主張ではありません。**この線引きを越えた瞬間、研究は嘘になる**。だから派手な「進化で AI が賢くなった!」は、まだ一度も書いていません。書けるだけの根拠が揃ったとき、初めて書きます。

ひとことで——**「採点表が壊れたら、選抜をどれだけ磨いても無力」**。だから磨く相手を、選抜でも AI でもなく、**採点表そのものの“終わらない作り”**に移す。これが一晩の結論です。

---

## もっと知りたい人へ

- 数式・全 19 構成の比較表・6 本の PoC の詳細・正直な限界の全リストは、**[完全版](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)** にあります。
- 前回 #25「私とフリストンだけが残った」が、この記事の動機（採点表が壊れた失敗の告白）です。
- このあと #28 で、ここで決めた作戦を実際のコードに落とす「オーケストラ型 AI」の実装編に進みます。

---

# English

# [Plain-Language Edition] The Night I Rebuilt AI Evolution — When a "Real AI Teacher" Still Pinned Everyone at a Perfect Score

![Kamikudaki lion — a bite that grants the blessing of understanding](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_en.svg)

> 📗 This is the plain-language edition of the [full version](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0). All the equations, tables, and fine-grained numbers live in the full version. Here, I aim to give you "so what actually happened, and what did we learn?" in 5–10 minutes, heavy on analogies. The technical conclusions and the "honest confession of failure" are kept intact, not watered down.

---

## First, the story in three lines (the "preamble," in rakugo terms)

Rakugo (Japanese comic storytelling) opens with a light "preamble" before the main story. So, three lines first.

- **It saturated at a perfect score again** — Trying to make AI smarter through "evolution," this time I had a real AI teacher grade it: llama3.2, an LLM that runs on a home PC. Running it for 12 hours straight, **everyone hit a perfect score by generation 5, and for the next 65 generations not a single inch of progress.**
- **I rebuilt the strategy overnight** — Six small experiments by my own hand, four AI assistants running in parallel, plus one research-assistant AI (Perplexity). **By morning, everyone, by different methods, had converged on the same conclusion.**
- **An unexpected "nobody-has-done-this gap" appeared** — Letting a continuously-evolving population perform an ensemble — without ever stopping — to produce one answer, a "**live orchestra**" approach, turned out to be missing from prior research worldwide.

In one line: **"Once the grading sheet (the ruler) breaks, no amount of polishing the selection method helps."** So I change what I polish. **I make the grading sheet itself "open-ended" (never-finishing).** That's the conclusion.

---

## 1. What is this research about, anyway?

We are researching how to "remake the blueprint of an AI's brain little by little, like biological evolution, to find the smart ones." Rather than training one AI hard, we form a "flock" of many AIs and let them compete with each other across generations.

Evolution needs three parts:

- **Variation** … tweak the design a little
- **Heredity** … pass good designs to the children
- **Selection (survival of the fittest)** … keep the good ones, drop the bad ones ← today's star

For "selection" to work, you need a "ruler" (grading sheet) that measures good vs. bad. In our research, we call this `lleval` (the evaluator).

In the previous installment (#25), I already confessed a major failure. After 500 generations of evolution, **the only survivors left in the world were "me" and "Friston" (one of the wise minds I used as a seed).** The cause: the grading sheet was broken. It kept handing everyone a perfect score, so "it doesn't matter who you keep" set in, and selection stopped working.

> 🤔 **Analogy**: On a test where the whole class always scores 100, you can't tell who is talented. No gap forms, so you can't "keep only the bright ones." This is "saturation of the grading sheet (pinned at a perfect score)."

Up to last time, all my experiments used a **"fake grading sheet" (a proxy = a synthetic ruler the computer produces mechanically).** A fake sheet can confirm "does the mechanism run?" but it can't show "did meaningful evolution happen with a real AI?" So the obvious next move — **verify it with a real AI teacher.** That's the starting point this time.

---

## 2. The starting point — even with a "real AI teacher," it honestly failed

I made a real LLM running on a home PC (llama3.2) the grader, and evolved for 12 hours straight. Here is the result.

| Fact | Value | What it means |
|---|---|---|
| Generations run | 71 / 12 hours | Real AI is slow, so this is the most we could do |
| Top score | **Perfect (1.0) by gen 5 → stayed perfect through gen 70** | **Ceiling hit early. 65 generations of no progress** |
| Mean score | Plateaued at 0.85 | **Improvement doesn't accumulate** |
| Extinction? | No (the flock survived) | The mechanism itself isn't broken |

![A 12-hour record of evolving with a real AI teacher (llama3.2). The top score pins to the ceiling early and stays flat afterward](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_en.svg)

Writing "it didn't go extinct! it reached a perfect score!" sounds like a success. But FullSense has an honest rule: **"when a good result appears, always doubt the breakdown before you feel like you've won."** Look inside: the test had 10 questions. **Eight of them were aced by everyone within a few generations.** Only the 2 hard questions still showed a gap. So 80% of the test was "doesn't matter who you pick."

This isn't evolution — it's **just "filtered random search."** It rejects the dropouts, but improvement never piles up.

**Verdict: not extinct, but not evolution either.**

The shocking part: this was **not just a fake-grading-sheet problem.** Last time's failure could be dismissed as "well, it's a proxy." But this time we hit the same wall with a real AI teacher.

> 🤔 **Analogy**: Even if you upgrade the grader to a "real veteran teacher," **if you hand out the exact same test paper every time**, everyone aces it within a few rounds and no gap forms no matter how many times you test. The teacher isn't the problem. **The test paper is fixed and too easy.**

So the real culprit isn't "the grader (AI vs. proxy)" but **"the test paper being fixed."** This is the most important realization this time.

> 🍵 **Break**: Many people think "if even a real AI is stuck, isn't it game over?" I thought so too. But if "fixing it was the mistake," then what to fix is neither the selection mechanism nor the AI, but **the way the test paper itself is made.** I spent the all-nighter verifying that.

---

## 3. The overnight strategy — "don't decide the answer with one head"

The instruction (I'm the one deciding direction) was: rather than running one big production run, **run small experiments until morning and "decide a strategy."**

So I assembled a "six-handed" setup.

| Worker | What it did |
|---|---|
| Me (in person) | Ran six small experiments (PoCs) by my own hand |
| AI assistant A | Verified "never-ending evolution" with a large 10,000-generation experiment |
| AI assistant B | Built observation tools (so we can trace who evolved how, after the fact) |
| AI assistant C | Verified "flock ensemble" with a real AI |
| Research AI (Perplexity) | Combed world prior research to check "has this been done?" |

Why not do it all with one person (one head)? This is the hidden star.

> **A conclusion reached by one head gets dragged by the same biases.** So I verify with entirely different methods (my own synthetic experiments / real AI / literature search) **separately**, and I only believe the conclusion **when they all agree, not by coincidence.** I call this "**independent cross-validation**." Its power shows in the second half.

One honest dud, too: **Codex (another AI), which was supposed to be a subordinate, was totally unusable this time.** An account-config mismatch made the API reject the models across the board. "A tool that should have worked, didn't" — I record that too, without hiding it.

---

## 4. The first decisive move — making the problems "gradually harder" fixed the saturation

The first hypothesis to test was the most fundamental one: **"If, instead of fixing the test paper, we gradually make it harder in step with the flock's ability, does the saturation get fixed?"**

I compared on a synthetic fake grading sheet (but with conditions fairly aligned).

- **Fixed problems (baseline)**: ability stuck at 0.627, flying low. Faithfully reproduced the 12-hour illness.
- **Adaptive difficulty (make problems harder once everyone can solve them)**: ability rose to 0.952. **The saturation broke!**

But there's a trap. In the process of making things harder, **the flock hardened into one single correct pattern** (diversity collapsed). A cookie-cutter result.

So I added one more thing to "gradually harder": **"give a reward to unusual solving styles too"** (in research, this is called novelty bonus).

| Method | Final ability | Diversity |
|---|---|---|
| Fixed problems | 0.627 | present (but low ability) |
| Gradually harder | 0.952 | **collapsed (cookie-cutter)** |
| **Gradually harder + reward the odd ones** | **0.881** | **maintained** |

**The two-sword combo of "gradually harder + reward the odd ones" achieved both ability (+40% vs. fixed) and diversity.** It gave up a little (7%) ability in exchange for fully preserving diversity.

> 🤔 **Analogy**: When everyone aces it, make the problems harder (so scores split). But then everyone converges on the same solving style. So you add "praise the kids with weird solving styles too," and smartness and individuality coexist. **The two-sword combo of "make it harder" and "praise the odd ones"** is the point.

---

## 5. The main event — rigorously testing "never-ending evolution" over 10,000 generations

The small experiments showed the "direction." Next, do it at large scale, rigorously. I had AI assistant A rigorously test **10,000 generations × 19 settings** to see whether it's "never-ending evolution (open-ended)." The criterion: does it avoid saturation, avoid being dyed one color, and keep growing a reservoir of diversity?

The result was strikingly clean.

- **The old-fashioned "selection that mashes scores into one number (scalar)" all failed (saturation + one-color).**
- **"Odd-one bonus (novelty)" and "selection that evaluates each problem separately (lexicase)" all worked (never-ending evolution held).**

![One figure contrasting the old-fashioned selection (collapse) with the odd-one-bonus selection (maintenance). The line that crumbles is the old method; the one held flat is the new method](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_en.svg)

The most important finding here: **"just adding a reservoir of diversity (archive)" could not save it.** Even with a reservoir added, the old method still got dyed one color and died out. What saved it was not the reservoir, but **making the way of selecting itself "never-ending."**

> 🍵 **Break**: This is the hardest section in the article. The one line to take home: **"Just adding a reservoir won't save you. You have to make the selection method itself never-ending."** 10,000 generations of real data said this outright.

And AI assistant A, precisely when a good result appeared, **pointed out the limits on its own**: "Even if it's diverse overall, one specific aspect (a thinking habit) can quietly turn one-color." I recorded that as an honest limitation and set up a separate countermeasure (below).

---

## 6. The core of originality — "without stopping evolution, let the flock perform as a live band"

With the selection core for avoiding saturation settled, next: "so, what's new about it? (originality)"

The idea I'd been nursing: **without stopping the still-evolving flock, ensemble it on the spot into one answer.** Normally you "stop evolution, then answer with the single strongest individual you ended up with." But what I want is to answer **without stopping** evolution — letting the mid-evolution population perform together like a band. I call it the "**live orchestra**."

The research AI (Perplexity) backed this up.

> A "system that answers continuously while evolving at the same time" has no clear prior research = **a white-space in world research.** Similar things exist, but not the same thing.

So it was a gap nobody has filled. But Perplexity also threw **cold water** on my excitement.

> In 2025 research, **"ensembling a diverse flock beats a single one" is not self-evident.** In fact, there are cases where iterating a single top model beat the mixed bag.

> 🍵 **Break**: This is the fork where research honesty is tested. Just as you want to soar with "it's a white-space! it's original!", the counter-evidence arrives: "but diversity isn't automatically good." **Receive the soaring material and the cold water both, within the same investigation.** Do this, and the conclusion gets much stronger.

---

## 7. The true nature of the cold water — it was "routing," not "voting"

"A diverse flock's ensemble isn't automatically stronger" — clarifying the true nature of this counter-evidence at the mechanism level was the climax. My own synthetic experiment (PoC #3) and AI assistant C's real-AI experiment, **separately, gave the same answer.**

The key was the "**way of combining**."

- **Combine by majority vote, and diversity backfires.** On each problem, the one expert who truly knows gets negated by the ignorant majority.
- **Combine by routing to the knowledgeable person, and diversity comes alive.** Send the math problem to the mathematician.

In other words — **the difference between "an orchestra with a conductor" and "a crowd where everyone makes sound as they please."** Voting cancels out the expert; routing (the conductor) brings the expert alive.

There's an even nicer twist: **the "conductor's score" (the markers of who is strong on which problem) could be reused as-is** from what we already compute to manage diversity. Two birds, one stone.

> 🔑 **This is the article's core**: My synthetic experiment (homemade) and the real-AI experiment (AI assistant C) reached the **same conclusion by entirely different methods**: "the ensemble beats the single one only via 'routing' / it doesn't via voting." Because the two agreed not by coincidence, you may believe it. This is the power of independent cross-validation.

> 🤔 **Analogy**: Have 10 experts vote, and the ignorant majority overrides the right expert. So you need a **dispatcher (conductor)** to "send math to the mathematician." And that conductor's score can reuse something already prepared for another purpose. Voting cancels out the expert; the conductor brings them alive.

---

## 8. Bonus — "AI that goes and investigates on its own" and "more numbers, more diversity"

There were two more originality ideas, each backed by a small experiment.

- **An individual that goes and investigates on its own**: let an individual go look things up by itself only when needed. In the experiment, **"when investigation costs something, evolution learned on its own to 'investigate only when it should.'"** Free? investigate freely. Costly? investigate selectively — evolution learned this by itself.
- **More numbers, more diversity**: scaling the flock from 256 → 4096, diversity kept rising smoothly. And this time, to grow the flock we cut the number of generations (**a condition unfavorable to diversity**), yet it still rose. So I can honestly write "this is a lower bound; it should actually be more effective." Not exaggerating a good result as an "upper bound" but writing it as a "lower bound" is also part of the honest rule.

---

## So, what did we actually learn?

Overnight, six homemade experiments, four AI assistants, and the research AI had all, **by different methods, landed on the same conclusion by morning.**

1. **Even a real AI teacher saturated.** "Use a real LLM and it'll evolve" was a lie. The real culprit was not the grader, but **the fixed test paper.**
2. **Just adding a reservoir won't save it.** What saves it is "making the selection method itself never-ending": the combined trick of "odd-one bonus," "per-problem evaluation," "gradually harder," and "stockpile odd solving styles."
3. **Diversity isn't automatically good.** Ensembling backfires with "voting"; it becomes valuable only with "routing by a conductor."
4. **Independent cross-validation strengthens the conclusion.** A conclusion from one head shares one head's biases. Believe it only when different methods agree.
5. **Honesty at the core.** "Even a real AI saturated," "a reservoir alone couldn't save it," "there was a tool that didn't work (Codex)" — failures and duds alike, kept rather than erased.

And an important caveat. Most of these experiments are **confirmation of "does the mechanism run?"**, not a claim that "a real AI got generally smarter." **The moment you cross that line, the research becomes a lie.** So I have not once written the flashy "AI got smarter through evolution!" I'll write it only when I have enough grounds to.

In one line — **"Once the grading sheet breaks, no amount of polishing the selection helps."** So I move what I polish — neither the selection nor the AI, but **the grading sheet itself, into a "never-ending" form.** That's the overnight conclusion.

---

## For those who want more

- The equations, the comparison table of all 19 settings, the details of the six PoCs, and the full list of honest limits are all in the **[full version](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)**.
- The previous installment #25, "Only Friston and I remained," is the motivation for this article (the confession of the broken grading sheet).
- After this, #28 moves to the implementation chapter — "orchestra-style AI" — that turns the strategy decided here into actual code.

---

# 中文

# 【通俗版】一夜之间重建 AI 进化 —— 用"真正的 AI 老师"测验，全员还是钉在满分的故事

![通俗易懂版舞狮 — 被咬的读者获得「理解」的福气](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_zh.svg)

> 📗 这是[完整版](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)的通俗版。公式、表格、细致数值都在完整版里。这里用大量比喻，5～10 分钟讲清"到底发生了什么、学到了什么"。技术结论与"诚实的失败坦白"原样保留，不稀释。

---

## 先用三行讲（相声里的"垫话"）

落语（日本单口相声）开场前有段轻松的"垫话"。先来三行。

- **又钉在满分上了** —— 想用"进化"让 AI 变聪明，这次让真正的 AI 老师来打分：llama3.2，一个能在家用电脑上跑的 LLM。连跑 12 小时，**第 5 代全员就拿了满分，之后 65 代一寸都没长。**
- **一夜之间重新定策略** —— 自己亲手跑 6 个小实验，4 个 AI 助手并行，再加 1 个负责查资料的 AI（Perplexity）。**到了早上，所有人用不同的方法，竟收敛到同一个结论。**
- **看见了一个意外的"没人做过的空白"** —— 不停止进化，让正在进化的群体当场合奏出 1 个答案的"**现场乐队（live orchestra）方式**"，被发现是全世界先行研究里还没有的空白地带。

一句话：**"评分表（尺子）一旦坏了，选拔方法磨得再亮也没用。"** 所以换打磨的对象。**把评分表本身改成"永不结束"的构造。** 这就是结论。

---

## 1. 这究竟是什么研究?

我们在研究"像生物进化那样，一点点改造 AI 大脑的设计图，找出聪明的那些"。不是死磕一个 AI，而是把许多 AI 组成"群"，让它们隔代更替、互相竞争。

进化需要三个部件：

- **变异** … 把设计稍微改一改
- **遗传** … 把好设计传给子代
- **选拔（适者生存）** … 留下好的、淘汰差的 ← 今天的主角

要让"选拔"奏效，需要一把衡量好坏的"尺子"（评分表）。在研究中我们称之为 `lleval`（评价器）。

在上一集（#25）里，我已经坦白过一次大失败。进化了 500 代后，**世界上只剩下"我"和"Friston（我用作种子的贤者之一）"。** 原因是评分表坏了。它一直给所有人打满分，于是变成"留谁都一样"，选拔停摆。

> 🤔 **比喻**：在一场全班永远考 100 分的考试里，你分不出谁优秀。拉不开差距，就没法"只留聪明的"。这就是"评分表的饱和（钉在满分）"。

到上一集为止，所有实验都用**"假评分表"（proxy = 计算机机械产出的合成尺子）**。假评分表能确认"机制能不能转"，却说不出"用真正的 AI 是否发生了有意义的进化"。所以下一步理所当然 —— **用真正的 AI 老师来验证。** 这就是这次的起点。

---

## 2. 起点 —— 即便是"真正的 AI 老师"，也诚实地不及格

我让一个能在家用电脑上跑的真 LLM（llama3.2）当打分者，连续进化 12 小时。结果如下。

| 事实 | 值 | 含义 |
|---|---|---|
| 跑了几代 | 71 代 / 12 小时 | 真 AI 慢，这已是极限 |
| 最高分 | **第 5 代满分（1.0）→ 一直到第 70 代都满分** | **很早撞天花板。65 代无进步** |
| 平均分 | 卡在 0.85 | **提升不累积** |
| 是否全灭 | 没有（群体存活） | 机制本身没坏 |

![用真正的 AI 老师（llama3.2）进化 12 小时的记录。最高分很早就钉在天花板，之后一直平坦](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_zh.svg)

写成"没全灭！到了满分！"显得像成功。但 FullSense 有条诚实规则：**"出现好结果时，在自以为赢之前，务必怀疑其内幕。"** 看内幕：考题有 10 道。**其中 8 道几代之内就被全员拿满分。** 还有差距的只有那 2 道难题。也就是说 80% 是"选谁都一样"。

这不是进化，**只是"带筛子的随机搜索"**。它淘汰掉落后者，但提升从不累积。

**判定：没全灭，但也不是进化。**

最震撼的是，这**不只是假评分表的问题**。上一集的失败可以用"因为是 proxy 嘛"打发，但这次用真正的 AI 老师也撞了同一面墙。

> 🤔 **比喻**：哪怕把打分者升级成"真正的资深老师"，**只要每次都发一模一样的考卷**，几轮内全员满分，之后考多少次都拉不开差距。问题不在老师。**是考卷固定且太简单。**

所以真凶不是"打分者（AI 还是 proxy）"，而是**"考卷被固定了"**。这是这次最重要的领悟。

> 🍵 **小憩**：很多人会想"连真 AI 都卡住，岂不是没救了?"我也这么想过。但若"固定才是错误"，那要修的既不是选拔机制也不是 AI，而是**考卷本身的出法**。我用一整夜去验证它。

---

## 3. 一夜的作战 —— "不要用一个脑袋定答案"

指示是（由我来定方向）：与其跑一个大型正式运行，不如**把小实验跑到天亮来"定策略"**。

于是我搭了一个"六手齐上"的阵容。

| 担当 | 内容 |
|---|---|
| 我（本人） | 亲手跑 6 个小实验（PoC） |
| AI 助手 A | 用 1 万代的大规模实验验证"永不结束的进化" |
| AI 助手 B | 做观测工具（事后能追溯谁怎么进化的） |
| AI 助手 C | 用真正的 AI 验证"群体合奏" |
| 查资料 AI（Perplexity） | 翻遍世界先行研究，确认"这个做过没?" |

为什么不用一个人（一个脑袋）全包? 这是隐藏的主角。

> **同一个脑袋想出的结论，会被同样的成见拖着走。** 所以用截然不同的方法（自制合成实验 / 真 AI / 文献检索）**各自分头**验证，只有当它们**并非偶然地全部一致**时才相信结论。我称之为"**独立交叉验证**"。它的威力在后半段显现。

也诚实记一笔哑炮：**本该当下属用的 Codex（另一个 AI），这次完全用不了。** 账号配置不一致，API 把模型全数拒绝。"本该能用的工具却不能用"——我也照记不误，不藏着掖着。

---

## 4. 第一记决定性出招 —— 把题目"逐渐变难"，饱和就修好了

第一个要验证的假设是最根本的问题：**"如果不固定考卷，而是随群体实力逐渐加难，饱和会不会修好?"**

我在合成假评分表上比较（但把条件公平对齐）。

- **固定题目（baseline）**：实力卡在 0.627 低空飞行。忠实重现了 12 小时的病症。
- **自适应难度（大家都会解了就加难）**：实力升到 0.952。**饱和破了!**

但这里有个陷阱。在加难的过程中，**群体硬化成一种正确套路**（多样性崩塌）。千篇一律。

于是我在"逐渐变难"上又加了一条：**"对不寻常的解法也给奖励"**（研究里称为 novelty = 新颖性奖励）。

| 方法 | 最终实力 | 多样性 |
|---|---|---|
| 固定题目 | 0.627 | 有（但实力低） |
| 逐渐变难 | 0.952 | **崩塌（千篇一律）** |
| **逐渐变难 + 奖励另类** | **0.881** | **维持** |

**"逐渐变难 + 奖励另类"的双刀流，让实力（比固定 +40%）与多样性兼得。** 让出一点（7%）实力，换来完全保住多样性。

> 🤔 **比喻**：全员满分就加难（分数拉开）。但接着全员又收敛到同一套解法。于是加上"也表扬解法古怪的孩子"，聪明与个性就能并存。**"加难"和"表扬另类"的双刀流**是要点。

---

## 5. 主战场 —— 用 1 万代严格检验"永不结束的进化"

小实验看清了"方向"。接下来要大规模、严格地做。我让 AI 助手 A 用 **1 万代 × 19 种设置**严格检验，看是不是"永不结束的进化（open-ended）"。判据：是否避免饱和、不被染成单色、多样性的库存是否持续增长。

结果惊人地干净。

- **老式的"把分数揉成一个数的选拔（scalar）"，全部失败（饱和 + 单色化）。**
- **"另类奖励（novelty）"和"逐题分别评价的选拔（lexicase）"，全部成功（永不结束的进化成立）。**

![一图对比老式选拔（崩塌）与带另类奖励的选拔（维持）。崩裂的那条是旧法，被压平维持的是新法](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_zh.svg)

这里最重要的发现：**"只加一个多样性库存（archive）"救不了。** 即便加了库存，旧法照样被染成单色、全灭。救它的不是库存，而是**把选拔的方式本身改成"永不结束"**。

> 🍵 **小憩**：这是全文最硬的一节。要带走的一行：**"只加库存救不了。必须把选拔方式本身改成永不结束。"** 1 万代的真实数据把这句话说死了。

而且 AI 助手 A 恰恰在出好结果时，**主动指出了局限**："即便整体多样，某个特定侧面（思维习惯）也可能悄悄变单色。"我把它记为诚实的局限，并另设对策（见下）。

---

## 6. 独创性的核心 —— "不停止进化，让群体作为现场乐队合奏"

避免饱和的选拔核心定下来后，接着是"那它新在哪? (独创性)"

我一直酝酿的点子：**不停止仍在进化的群体，当场把它合奏成 1 个答案。** 通常是"停止进化，再用最终最强的那 1 个体来回答"。但我想要的是**不停止**进化，让进化中的群体像乐队一样合奏作答。取名"**现场乐队（live orchestra）**"。

查资料 AI（Perplexity）佐证了这点。

> "一边进化、同时持续作答的系统"没有明确的先行研究 = **世界研究的空白地带（white-space）**。相似的有，但没有相同的。

也就是说，是个没人填过的空白。但 Perplexity 也给我泼了**冷水**。

> 2025 年的研究表明，**"用多样群体合奏就胜过单体"并非不言自明**。反而有单一顶尖模型迭代胜过大杂烩的例子。

> 🍵 **小憩**：这是考验研究诚实度的岔口。正想用"是空白! 是独创!"飘起来时，反证来了："可多样性并非自动就好。" **把让你飘的素材和泼来的冷水，在同一次调查里同时接住。** 做到这点，结论会强很多。

---

## 7. 冷水的真面目 —— 不是"投票"，而是"分派"

"多样群体的合奏并不自动更强"——在机制层面厘清这条反证的真面目，是高潮。我自己的合成实验（PoC #3）和 AI 助手 C 的真 AI 实验，**各自分头给出了同一个答案。**

关键在于"**合并方式**"。

- **按多数投票合并，多样性会反作用。** 每道题上，那个真正懂的专家会被无知的多数派抵消掉。
- **按"分派给懂的人"合并（routing），多样性就活了。** 数学题交给数学家。

换句话说——**"有指挥的乐队"和"各吹各的喧闹人群"的区别。** 投票抵消专家；分派（指挥）让专家活起来。

还有更妙的一手：**这张"指挥的乐谱"（谁在哪类题上强的标记），可以原样复用**我们为管理多样性而早已算好的东西。一石二鸟。

> 🔑 **这是本文的核心**：我的合成实验（自制）和真 AI 实验（AI 助手 C），用**截然不同的方法得出同一结论**："合奏只有通过'分派'才胜过单体 / 通过投票则不及。"正因二者并非偶然地一致，才可相信。这就是独立交叉验证的威力。

> 🤔 **比喻**：让 10 位专家投票，无知的多数派会压过对的专家。所以需要一个**分派员（指挥）**"把数学交给数学家"。而这位指挥的乐谱，可以复用为别的目的早已备好的东西。投票抵消专家，指挥让其活起来。

---

## 8. 附带 —— "会自己去查的 AI"与"数量越多越多样"

独创性的点子还有两个，各用一个小实验取证。

- **会自己去查的个体**：让个体只在需要时自己去查资料。实验里，**"一旦查资料要付出代价，进化就自己学会了'只在该查时才查'。"** 免费就随便查，收费就挑着查——进化自己学会了这点。
- **数量越多越多样**：把群体从 256 → 4096 扩大，多样性顺势持续上升。而且这次为了扩群体而削减了代数（**对多样性不利的条件**），它依然上升。所以我可以诚实地写"这是下限，实际应该更有效"。不把好结果夸大为"上限"而写成"下限"，也是诚实规则的一部分。

---

## 那么，到底学到了什么?

一夜之间，6 个自制实验、4 个 AI 助手、查资料 AI，全都**用各不相同的方法，到早上落到了同一个结论。**

1. **连真正的 AI 老师也饱和了。** "用真 LLM 就能进化"是谎言。真凶不是打分者，而是**固定的考卷**。
2. **只加库存救不了。** 救它的是"把选拔方式本身改成永不结束"：即"另类奖励""逐题评价""逐渐变难""收藏古怪解法"的组合拳。
3. **多样性并非自动就好。** 合奏用"投票"会反作用，只有用"指挥来分派"才成价值。
4. **独立交叉验证让结论更强。** 同一个脑袋的结论共享同一种成见。只有不同方法一致时才相信。
5. **以诚实为核心。** "连真 AI 也饱和""光有库存救不了""有个用不了的工具（Codex）"——失败与哑炮一律保留，不抹去。

还有一条重要的但书。这些实验大多是**确认"机制能不能转"**，并非主张"真 AI 普遍变聪明了"。**一旦越过这条线，研究就成了谎言。** 所以那句花哨的"靠进化让 AI 变聪明了!"我一次都没写过。等有足够根据时，我才会写。

一句话——**"评分表一旦坏了，选拔磨得再亮也没用。"** 所以把要打磨的对象，从选拔、从 AI，移到**评分表本身的"永不结束"构造**上。这就是这一夜的结论。

---

## 想了解更多

- 公式、全部 19 种设置的对比表、6 个 PoC 的细节、诚实局限的完整清单，都在 **[完整版](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)** 里。
- 上一集 #25"只剩 Friston 和我"是本文的动机（评分表坏掉的失败坦白）。
- 在此之后，#28 进入实现篇——把这里定下的策略落成实际代码的"乐队式 AI"。

---

# 한국어

# [쉽게 풀어쓴 판] 하룻밤 사이에 AI 진화를 다시 만든 밤 — "진짜 AI 선생님"으로 시험을 봐도 또 만점에 박혀버린 이야기

![쉬운 설명판 사자탈 — 물린 독자에게 「이해」의 복](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_ko.svg)

> 📗 이 글은 [완전판](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)의 쉽게 풀어쓴 판입니다. 수식·표·세밀한 수치는 모두 완전판에 있습니다. 여기서는 비유를 많이 써서 "결국 무슨 일이 일어났고, 무엇을 알게 됐나?"를 5~10분 안에 잡을 수 있게 합니다. 기술적 결론과 "정직한 실패의 고백"은 희석하지 않고 그대로 남깁니다.

---

## 먼저 세 줄로 (라쿠고로 치면 "도입부")

라쿠고(일본 만담)는 본론 전에 가벼운 "도입부"가 있습니다. 우선 세 줄.

- **또 만점에 박혔다** — "진화"로 AI를 똑똑하게 만들려고, 이번에는 진짜 AI 선생님에게 채점시켰다: llama3.2, 가정용 PC에서 도는 LLM. 12시간 내리 돌렸더니 **5세대째에 전원이 만점을 받고, 이후 65세대 동안 한 치도 늘지 않았다.**
- **하룻밤 사이에 작전을 다시 세웠다** — 내 손으로 작은 실험 6개, 다른 AI 조수 4명을 병렬로, 거기에 자료 조사 담당 AI(Perplexity) 1명. **아침에는 모두가 서로 다른 방법으로 같은 결론에 다다랐다.**
- **뜻밖의 "아무도 안 한 빈틈"이 보였다** — 진화를 멈추지 않고, 진화 중인 집단을 그 자리에서 합주시켜 1개의 답을 내는 "**라이브 오케스트라 방식**"이, 전 세계 선행 연구에 아직 없는 빈 영역으로 판명됐다.

한마디로 — **"채점표(잣대)가 망가지면, 선발 방식을 아무리 갈고닦아도 소용없다."** 그래서 갈고닦을 대상을 바꾼다. **채점표 자체를 "끝나지 않는" 구조로 바꾼다.** 이것이 결론입니다.

---

## 1. 애초에 무슨 연구인가?

우리는 "AI 두뇌의 설계도를, 생물의 진화처럼 조금씩 고쳐가며 똑똑한 녀석을 찾는" 연구를 하고 있습니다. AI 하나를 죽어라 단련하는 게 아니라, **많은 AI를 "무리"로 만들어 세대교체시키며 서로 경쟁**시키는 방식입니다.

진화에는 세 부품이 필요합니다.

- **변이** … 설계를 조금 바꿔본다
- **유전** … 좋은 설계를 자식에게 물려준다
- **선발(적자생존)** … 좋은 것을 남기고 나쁜 것을 떨군다 ← 오늘의 주역

이 "선발"이 작동하려면, 좋고 나쁨을 재는 "잣대"(채점표)가 필요합니다. 연구에서는 이것을 `lleval`(평가기)이라 부릅니다.

지난 회(#25)에서 저는 이미 큰 실패를 고백했습니다. 500세대나 진화시켰더니 **세상에 "나"와 "Friston(씨앗으로 쓴 현자 중 하나)"만 남았습니다.** 원인은 채점표가 망가진 것. 모두에게 만점을 계속 줘서 "누구를 남겨도 똑같다"가 되어 선발이 멈춘 겁니다.

> 🤔 **비유**: 반 전체가 늘 100점을 받는 시험에서는 누가 우수한지 알 수 없습니다. 차이가 안 나니 "잘하는 애만 남기기"가 불가능합니다. 이것이 "채점표의 포화(만점에 박힘)"입니다.

지난 회까지는 전부 **"가짜 채점표"(proxy = 컴퓨터가 기계적으로 내는 합성 잣대)**로 실험했습니다. 가짜 채점표는 "구조가 도는지"는 확인할 수 있어도 "진짜 AI로 의미 있는 진화가 일어났는지"까지는 말할 수 없습니다. 그래서 당연한 다음 수 — **진짜 AI 선생님으로 확인하기.** 이것이 이번 출발점입니다.

---

## 2. 출발점 — "진짜 AI 선생님"이어도 정직하게 불합격이었다

가정용 PC에서 도는 진짜 LLM(llama3.2)을 채점자로 삼아 12시간 내리 진화시켰습니다. 결과가 이것입니다.

| 사실 | 값 | 무슨 뜻 |
|---|---|---|
| 돈 세대 수 | 71세대 / 12시간 | 진짜 AI는 느려서 이게 한계 |
| 최고점 | **5세대째 만점(1.0) → 70세대까지 계속 만점** | **일찌감치 천장. 65세대가 무진보** |
| 평균점 | 0.85에서 정체 | **향상이 쌓이지 않음** |
| 전멸했나 | 안 함(무리는 생존) | 구조 자체는 안 망가짐 |

![진짜 AI 선생님(llama3.2)으로 진화시킨 12시간의 기록. 최고점이 일찌감치 천장에 달라붙고 이후 줄곧 평탄](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_ko.svg)

"전멸 안 했다! 만점에 닿았다!"라고 쓰면 성공처럼 보입니다. 하지만 FullSense에는 정직 규칙이 있습니다: **"좋은 결과가 나오면, 이긴 기분이 들기 전에 반드시 내막을 의심하라."** 내막을 보면 시험 문제는 10문항. **그중 8문항은 몇 세대 안에 전원이 만점.** 차이가 난 건 어려운 2문항뿐. 즉 80%가 "누구를 골라도 똑같다".

이건 진화가 아니라 **그저 "체 달린 무작위 탐색"**입니다. 낙오자는 떨궈도, 향상은 쌓이지 않습니다.

**판정: 전멸은 안 했지만, 진화도 아니다.**

충격적인 건, 이것이 **가짜 채점표만의 문제가 아니었다**는 점. 지난 회 실패는 "proxy라서 그렇지"로 넘길 수 있었지만, 이번엔 진짜 AI 선생님으로도 같은 벽에 부딪혔습니다.

> 🤔 **비유**: 채점자를 "진짜 베테랑 선생님"으로 승격해도, **매번 똑같은 시험지를 나눠주면** 몇 번 만에 전원이 만점을 받고, 이후로는 아무리 시험을 봐도 차이가 안 납니다. 문제는 선생님이 아닙니다. **시험지가 고정이고 너무 쉬운 겁니다.**

그러니 진범은 "채점자(AI냐 proxy냐)"가 아니라 **"시험지가 고정됐다는 것"**. 이것이 이번의 가장 중요한 깨달음입니다.

> 🍵 **한숨 돌리기**: 많은 분이 "진짜 AI로도 막히면 이제 끝 아닌가?"라고 생각합니다. 저도 그랬습니다. 하지만 "고정한 게 잘못"이라면, 고칠 것은 선발 구조도 AI도 아니라 **시험지를 내는 방식 자체**. 그것을 하룻밤 들여 확인하러 갔습니다.

---

## 3. 하룻밤의 작전 — "정답을 한 머리로 정하지 않는다"

지시는 (방향은 제가 정합니다): 큰 본방 런을 하나 돌리기보다, **작은 실험을 아침까지 마구 돌려 "작전을 정하라".**

그래서 "여섯 손 동시" 체제를 짰습니다.

| 담당 | 내용 |
|---|---|
| 나(본인) | 작은 실험(PoC) 6개를 직접 돌린다 |
| AI 조수 A | 1만 세대 대규모 실험으로 "끝나지 않는 진화"를 검증 |
| AI 조수 B | 관측 도구 제작(나중에 누가 어떻게 진화했는지 추적 가능하게) |
| AI 조수 C | 진짜 AI로 "무리 합주"를 검증 |
| 자료 조사 AI(Perplexity) | 세계 선행 연구를 뒤져 "이거 한 적 있나?" 확인 |

왜 한 사람(한 머리)으로 다 안 하나? 이것이 숨은 주역입니다.

> **같은 머리로 생각한 결론은 같은 선입견에 끌려간다.** 그래서 완전히 다른 방법(자작 합성 실험 / 진짜 AI / 문헌 조사)으로 **따로따로** 확인하고, 우연이 아니라 **전부 일치했을 때만** 결론을 믿는다. 이것을 "**독립 교차 검증**"이라 부릅니다. 그 위력은 후반에 드러납니다.

정직하게 불발도 하나 적습니다. **부하로 쓸 예정이던 Codex(다른 AI)는 이번에 전혀 못 썼습니다.** 계정 설정 불일치로 API가 모델을 죄다 거부. "쓸 수 있어야 할 도구가 안 됐다"도 숨기지 않고 기록합니다.

---

## 4. 첫 결정타 — 문제를 "점점 어렵게" 했더니 포화가 고쳐졌다

먼저 검증할 가설은 가장 근본적인 물음: **"시험지를 고정하지 말고 무리의 실력에 맞춰 점점 어렵게 하면, 포화는 고쳐지는가?"**

합성 가짜 채점표에서 (단, 조건을 공평히 맞춰) 비교했습니다.

- **고정 문제(baseline)**: 실력 0.627에서 저공비행 정체. 12시간의 병증을 충실히 재현.
- **적응 난이도(다들 풀 수 있게 되면 문제를 어렵게)**: 실력이 0.952로 상승. **포화가 풀렸다!**

그런데 함정이 있습니다. 어렵게 하는 과정에서 **무리가 하나의 정답 패턴으로 굳어버렸습니다**(다양성 붕괴). 붕어빵.

그래서 "점점 어렵게"에 하나를 더 붙였습니다. **"별난 푸는 방식에도 보상을 준다"**(연구에서는 novelty = 신규성 보너스라 부름).

| 방식 | 최종 실력 | 다양성 |
|---|---|---|
| 고정 문제 | 0.627 | 있음(그러나 실력 낮음) |
| 점점 어렵게 | 0.952 | **붕괴(붕어빵)** |
| **점점 어렵게 + 별난 녀석에 보상** | **0.881** | **유지** |

**"점점 어렵게 + 별난 녀석에 보상"의 이도류가, 실력(고정 대비 +40%)과 다양성을 둘 다 잡았습니다.** 실력을 조금(7%) 양보하는 대신 다양성을 완전히 지켰습니다.

> 🤔 **비유**: 전원이 만점이면 문제를 어렵게(점수가 갈린다). 하지만 이번엔 전원이 같은 푸는 방식으로 수렴한다. 거기에 "푸는 방식이 별난 아이도 칭찬"을 더하면 똑똑함과 개성이 공존한다. **"어렵게 하기"와 "별난 녀석 칭찬"의 이도류**가 핵심입니다.

---

## 5. 본진 — "끝나지 않는 진화"를 1만 세대로 철저히 검증했다

작은 실험으로 "방향"은 보였습니다. 다음은 대규모로 엄밀하게. AI 조수 A에게 **1만 세대 × 19가지 설정**으로 "끝나지 않는 진화(open-ended)"인지 철저히 검증하게 했습니다. 판정 기준: 포화를 피하고, 한 색으로 물들지 않고, 다양성 저장고가 계속 자라는가.

결과는 놀랄 만큼 깔끔했습니다.

- **옛날식 "점수를 하나로 뭉치는 선발(scalar)"은 전부 실패(포화 + 단색화).**
- **"별난 녀석 보너스(novelty)"와 "문제마다 따로 평가하는 선발(lexicase)"은 전부 성공(끝나지 않는 진화 성립).**

![옛날식 선발(붕괴)과 별난 녀석 보너스가 있는 선발(유지)을 한 장으로 대비. 무너지는 선이 구방식, 평탄하게 유지되는 것이 신방식](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_ko.svg)

여기서 가장 중요한 발견: **"다양성 저장고(archive)를 더하기만" 해서는 못 구한다**는 것. 저장고를 더해도 구방식은 역시 한 색으로 물들어 전멸했습니다. 구한 것은 저장고가 아니라 **선발 방식 자체를 "끝나지 않는" 구조로 만드는 것**이었습니다.

> 🍵 **한숨 돌리기**: 이 글에서 가장 딱딱한 절입니다. 가져갈 한 줄 — **"저장고만 더해선 못 구한다. 선발 방식 자체를 끝나지 않는 구조로 해야 한다."** 1만 세대의 실데이터가 이를 못 박았습니다.

그리고 AI 조수 A는, 좋은 결과가 나왔을 때야말로 **스스로 한계도 지적**해 왔습니다. "전체적으로는 다양해도, 특정 측면(사고 버릇)만은 슬쩍 한 색이 될 수 있다." 이를 정직한 한계로 기록하고 별도 대책(아래)을 세웠습니다.

---

## 6. 독창성의 핵 — "진화를 멈추지 않고, 무리를 라이브 밴드로 합주시킨다"

포화를 피하는 선발의 핵이 정해졌으니, 다음은 "그래서 뭐가 새로운가? (독창성)"입니다.

제가 품어온 아이디어 — **진화 중인 무리를 멈추지 않고, 그 자리에서 합주시켜 1개의 답으로 만든다.** 보통은 "진화를 멈추고, 완성된 최강의 1개체로 답한다". 하지만 제가 하고 싶은 건 진화를 **멈추지 않고**, 진화 중인 집단을 그대로 밴드처럼 합주시켜 답하는 것. 이름하여 "**라이브 오케스트라**".

자료 조사 AI(Perplexity)가 이를 뒷받침했습니다.

> "진화하면서 동시에 계속 답하는 시스템"은 명확한 선행 연구가 없다 = **세계 연구의 빈 영역(white-space).** 비슷한 건 있어도 같은 건 없다.

즉 아무도 못 채운 빈틈이었습니다. 다만 Perplexity는 들뜬 제게 **찬물**도 끼얹었습니다.

> 2025년 연구에서는 **"다양한 무리로 합주하면 단일보다 강하다"는 자명하지 않다**. 오히려 단일 톱 모델의 반복이 잡탕보다 강했던 예가 있다.

> 🍵 **한숨 돌리기**: 여기는 연구의 정직함이 시험받는 갈림길입니다. "빈 영역이다! 독창성이다!"로 들뜨고 싶을 때, "하지만 다양성이 자동으로 좋은 건 아니다"라는 반증이 옵니다. **들뜨게 하는 재료와 끼얹는 찬물을, 같은 조사 안에서 둘 다 받는다.** 이걸 해내면 결론이 훨씬 강해집니다.

---

## 7. 찬물의 정체 — "투표"가 아니라 "배분"이었다

"다양한 무리의 합주가 자동으로 더 강하진 않다" — 이 반증의 정체를 메커니즘 수준에서 풀어낸 것이 절정입니다. 제 합성 실험(PoC #3)과 AI 조수 C의 진짜 AI 실험이 **따로따로 같은 답**을 냈습니다.

열쇠는 "**합치는 방식**"이었습니다.

- **다수결(투표)로 합치면, 다양성은 역효과.** 각 문제에서 정말 잘 아는 전문가 1명이, 무지한 다수파에게 상쇄됩니다.
- **잘 아는 사람에게 배분해 합치면(routing), 다양성이 살아납니다.** 수학 문제는 수학자에게 보냅니다.

다시 말해 — **"지휘자가 있는 오케스트라"와 "다들 제멋대로 소리 내는 군중"의 차이.** 투표는 전문가를 상쇄하고, 배분(지휘자)은 전문가를 살립니다.

게다가 더 영리한 점: **이 "지휘자의 악보"(누가 어느 문제에 강한지의 표식)는, 다양성 관리를 위해 이미 계산해 둔 것**을 그대로 재사용할 수 있었습니다. 일석이조.

> 🔑 **이것이 본문의 핵**: 제 합성 실험(자작)과 진짜 AI 실험(AI 조수 C)이, **완전히 다른 방법으로 같은 결론**에 다다랐습니다. "합주는 '배분'으로만 단일을 넘어선다 / 투표로는 못 넘는다." 둘이 우연이 아니라 일치했기에 믿어도 됩니다. 이것이 독립 교차 검증의 위력입니다.

> 🤔 **비유**: 전문가 10명에게 다수결을 시키면 무지한 다수파가 옳은 전문가를 눌러버립니다. 그래서 "수학은 수학자에게" 배분하는 **배분원(지휘자)**이 필요합니다. 게다가 그 지휘자의 악보는, 다른 목적으로 이미 준비된 것을 재사용할 수 있습니다. 투표는 전문가를 상쇄하고, 지휘자는 살립니다.

---

## 8. 덤 — "스스로 조사하러 가는 AI"와 "수가 많을수록 다양해진다"

독창성 아이디어가 둘 더 있고, 각각 작은 실험으로 근거를 잡았습니다.

- **스스로 조사하러 가는 개체**: 개체가 필요할 때만 스스로 조사하게 한다. 실험에서 **"조사에 비용이 들면, 진화가 '조사해야 할 때만 조사한다'를 스스로 익혔습니다."** 공짜면 마음껏, 유료면 가려서 — 진화가 스스로 배운 겁니다.
- **수가 많을수록 다양해진다**: 무리를 256 → 4096으로 늘리면 다양성이 순순히 계속 올랐습니다. 게다가 이번엔 무리를 늘린 만큼 세대 수를 깎았는데(**다양성에 불리한 조건**), 그래도 올랐습니다. 그래서 "이건 하한, 실제론 더 효과적일 것"이라고 정직하게 쓸 수 있습니다. 좋은 결과를 "상한"으로 과장하지 않고 "하한"으로 쓰는 것도 정직 규칙의 일부입니다.

---

## 그래서, 결국 무엇을 알게 됐나?

하룻밤 사이에, 자작 실험 6개도, AI 조수 4명도, 자료 조사 AI도, **제각각 다른 방법으로, 아침에는 같은 결론**에 다다라 있었습니다.

1. **진짜 AI 선생님도 포화했다.** "진짜 LLM을 쓰면 진화한다"는 거짓말이었다. 진범은 채점자가 아니라 **고정된 시험지**.
2. **저장고만 더해선 못 구한다.** 구하는 것은 "선발 방식 자체를 끝나지 않는 구조로 하기": 곧 "별난 녀석 보너스" "문제별 평가" "점점 어렵게" "별난 푸는 방식 보관"의 합동 기술.
3. **다양성이 자동으로 좋진 않다.** 합주는 "투표"면 역효과, "지휘자에 의한 배분"으로만 가치가 된다.
4. **독립 교차 검증이 결론을 강하게 한다.** 같은 머리의 결론은 같은 선입견을 공유한다. 다른 방법이 일치할 때만 믿는다.
5. **정직함을 핵으로.** "진짜 AI도 포화했다" "저장고만으론 못 구했다" "못 쓴 도구(Codex)가 있었다" — 실패도 불발도 지우지 않고 남긴다.

그리고 중요한 단서. 이 실험들 대부분은 **"메커니즘이 도는지"의 확인**이지, "진짜 AI가 일반적으로 똑똑해졌다"는 주장이 아닙니다. **이 선을 넘는 순간, 연구는 거짓이 됩니다.** 그래서 화려한 "진화로 AI가 똑똑해졌다!"는 아직 한 번도 쓰지 않았습니다. 쓸 만한 근거가 갖춰졌을 때 비로소 씁니다.

한마디로 — **"채점표가 망가지면, 선발을 아무리 갈고닦아도 소용없다."** 그래서 갈고닦을 대상을, 선발도 AI도 아니라 **채점표 자체의 "끝나지 않는" 구조**로 옮긴다. 이것이 하룻밤의 결론입니다.

---

## 더 알고 싶은 분께

- 수식, 전체 19가지 설정 비교표, 6개 PoC의 세부, 정직한 한계의 전체 목록은 모두 **[완전판](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)**에 있습니다.
- 지난 회 #25 "Friston과 나만 남았다"가 이 글의 동기(채점표가 망가진 실패의 고백)입니다.
- 이후 #28에서, 여기서 정한 작전을 실제 코드로 떨어뜨리는 "오케스트라형 AI" 구현 편으로 나아갑니다.
