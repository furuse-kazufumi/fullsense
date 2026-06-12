---
title: '【📗かみくだき版】「良すぎる数値」は勝ちじゃなくて警報 — 計算機を1個入れ替えたら自慢の結果が崩れた話 (llcore #35-02)'
tags:
  - FullSense
  - llcore
  - honest disclosure
  - 解説
private: true
id: 146d5e2b27dabc59e799
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 【かみくだき版】「良すぎる数値」は勝ちじゃなくて警報 — 計算機を1個入れ替えたら自慢の結果が崩れた話

![かみくだき獅子 — 噛まれた読者に「理解」のご利益](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi.svg)

📗 これは [完全版](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615) のかみくだき版です。専門用語は出てきたらすぐ日常のたとえに言い換えます。技術版の前の地ならし、または「だいたい何やったの?」を10分で掴みたい人向けです。

![計算機を入れ替えると偽の数値が崩れる図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap.svg)

## 三行あらすじ

- 進化させた AI が「暴走しないか」を調べる**検査器**を作っていた。性能を測ったら、やたら「豊かで都合のいい」数字が出た。
- 数字が良すぎたので疑った。原因は、計算に使っていた**電卓 (ソルバ)** が境界付近でズルをしていたこと。**正確な電卓に入れ替えた**ら、自慢の結果は幻だったと判明。
- でも幻の壊れ方が面白い。ある所では「**盛りすぎ**」、別の所では逆に「**控えめすぎ**」。本命の検査器は、実は思っていたより**もっと強かった**。教訓は一行 ──「**数字が良すぎたら、信じる前にまず電卓を疑え**」。

---

## 第1幕: そもそも何を検査してるの?

私たちは **llcore (エルコア)** という研究基盤で、小さな AI の「頭の部品」を生き物の進化みたいに少しずつ作り変えています。やり方は遺伝的アルゴリズムと呼ばれる定番の方法で、ざっくり言えば「候補をたくさん作る → 成績の良いものを残す → 少しだけ変えてまた試す」の繰り返し。甘いトマトを目指す品種改良と同じ理屈です。しかも CPU だけ・自分の PC の中だけ・お金ゼロで動く、という縛りつき。

進化で作った部品には当たり外れがあります。困るのが「**暴走する部品**」。ここで言う部品とは「状態 (内部の数字の組) を一歩ずつ更新していく小さな計算装置」のことで、出力が次の入力に戻ってくる、ぐるぐる回る仕組みです。こういう繰り返しの仕組みでは、一周ごとにほんの少しでも「増幅」が勝つと、数字は雪だるま式に膨らみます。マイクとスピーカーが近すぎると「キーン」とハウリングするのと同じ構図 ── マイクが拾った音が増幅されてスピーカーから出て、それをまたマイクが拾って…の繰り返しで、小さな音が一瞬で爆音になる。あれの計算版で、いわば「アクセル踏みっぱなしで止まらない車」みたいな部品です。

そこで必要なのが**検査器 (verifier)**。進化で生まれた部品を一つずつ調べて、

> 「この部品は、繰り返しても暴走しない (むしろ落ち着いていく) か?」

を判定し、ダメなやつを門前払いします。研究の問いはシンプルで「**じゃあ、正しい検査器ってどう作るの?**」です。

「実際に動かして様子を見ればいいのでは?」と思うかもしれません。でも観察で言えるのは「**ここまでは**大人しかった」だけ。実はこのあと出てきますが、ふだんの動かし方では大人しいのに、最悪の条件 (動かす順番) を引いたときだけ暴れ出す部品が本当に存在します。試運転に合格した、では足りない。欲しいのは「この先どう転んでも暴走しない」という**未来までカバーする保証**で、それは観察ではなく数学でしか出せません。

その「落ち着いていく」性質を、研究では **収縮 (しゅうしゅく)** と呼びます。一歩進むたびにゴールまでの距離が必ず縮む、お椀の中のビー玉が最後は底で止まる、みたいなイメージ。「毎回必ず縮む」なら膨らみようがないので、収縮さえ言えれば暴走の心配は消えます。そして「この部品はちゃんと収縮します」という**数学的な証明書**を発行できれば、安心して通せます。建物でいう構造計算書と同じで、「揺らしてみたけど倒れなかった」ではなく「この範囲の揺れなら絶対に倒れない、と計算で示した書類」です。

その証明書の正体は、P という**行列** ── かみくだくと「**歪んだものさし**」です。まっすぐな普通のものさしで測ると縮んで見えない動きも、その部品に合わせて歪めた特注のものさしで測り直すと「一歩ごとにちゃんと縮んでいる」と分かることがある。「この歪んだものさし P で測れば、どの一歩でも必ず距離が縮む」と言えれば、その一文がそのまま収縮の証明書になります。

そして、この都合のいいものさし P を探してくる計算方法の本命が **SDP** という**凸最適化**の手法。凸最適化とは「お椀型の地形で一番低い点を探す」タイプの問題のことで、お椀型なら途中の小さなくぼみ (偽物の谷) に騙される心配がありません。だから「見つかった答え」をそのまま「保証」として使える ── 証明書探しに使えるのは、この性質のおかげです。

ちなみに、当初は「論理パズルを解く高級ソルバ (SMT/Z3)」も検査の柱になるかと期待していました。でも調べると、この基盤での Z3 は**飾り**でした。というのも、ここで Z3 に聞いていた判定は、実は紙と鉛筆で書き下せる**閉じた式** (足し算掛け算で直接計算できる式) に帰着するものだったから。実測でも、2 万件・3270 件と照合して、Z3 の判定は閉じた式の計算と**完全に一致** (食い違いゼロ)。電卓一発で答えが出る問題に、論理パズルの達人を呼んでいたわけです。達人は間違えてはいないけれど、何も足してもいない。収縮の本質をつかんでいたのは**やはり SDP の証明書**の方だった、というのが下地の理解です。

---

## 第2幕: 自慢の成績表が出た ── でも、良すぎた

検査器の実力を測りました。鍵になるのが**次数**という概念です。さっき証明書を「歪んだものさし」と言いましたが、次数とはそのものさしの「曲げ方の自由度」のこと。次数を上げるほど、より複雑な形のものさしまで許される = より手の込んだ証明書が書ける = 理屈の上では、捕まえられる部品が増えるはずです。

そこで「次数を上げると、捕まえられる部品がどう増えるか」という**段階的な成績ラダー** (はしご) を作りました。網の目を細かくしながら、それぞれ何匹捕れるか数えていく漁の記録みたいなものです。

最初の集計はこんな雰囲気でした。

- 手の込んだ証明書 (次数4) だけで捕まえられた部品: 23個
- もっと手の込んだ証明書 (次数6) だけで捕まえられた部品: 13個
- 両方で捕まえられた部品: 18個

読み方はこうです。次数4の網でしか捕れない魚が23匹、次数6の網でしか捕れない魚が13匹、両方の網で捕れるのが18匹。つまり、それぞれの網に**その網でしか捕れない魚がいる**、という解釈になります。

これ、研究者にとっては「**おいしい**」結果なんです。なぜなら、**次数を上げるたびに新しい獲物が増える** = 「証明能力に豊かな階層がある」ように見えるから。「高い次数にはそれぞれ固有の存在価値がある。だから全部の網を持っておく意味がある」── 新しい道具を足すたびに新しい成果が出る物語は、論文として最高に映える絵です。

…が。ここで [[honest disclosure 規律]] が発動します。FullSense の研究には鉄の掟があって、

> **異常に良い結果が出たら、勝った気になる前に必ず内訳を疑え。**

人間は、期待どおりの結果は見直さず、期待外れの結果だけ必死に原因を探す生き物です。つまり、放っておくと「自分に都合のいい間違い」だけが検査をすり抜けて生き残ってしまう。それが分かっているから、わざわざ逆向きのルール ── 結果が良い**ほど**疑う ── を先に決めてあるのです。成績表が「豊かすぎ・都合よすぎ」だったので、素直に喜ばず疑いにかかりました。

---

## 第3幕: 犯人は電卓だった (ここが本題)

証明書を探す計算は、裏で**ソルバ**という「専門電卓」に丸投げしています。使っていたデフォルトの電卓は **SCS** という名前。速いのが取り柄ですが、弱点がありました。

> **答えがギリギリ存在するかどうかの「境界」付近で、SCS はズルをして「見つかりませんでした」と言ってしまう。**

本当はちゃんと証明書が存在するのに、「いや〜、見つからなかったっす」と**嘘の報告 (偽陰性)** をしていたのです。電卓自身も薄々気づいていて「Solution may be inaccurate (この答え、不正確かも)」という警告を小さく出していました。

そこで、正確だけど少し遅い**内点法**という別の電卓 **CLARABEL** に入れ替えてみました。同じ部品プール、同じ問題、電卓だけスイッチ。すると ──

| 集計項目 | SCS (ズルする電卓・偽) | CLARABEL (正確な電卓・真) |
|---|---|---|
| 次数4だけ / 次数6だけ / 両方 | 23 / 13 / 18 | 0 / 1 / 54 |
| 構造の解釈 | バラバラ (豊かな階層に見える) | きれいな入れ子 (実はシンプル) |
| 「未証明で残った数」 | 53個 | 10個 |
| 本命 SDP のカバー率 | 64% | **95%** |
| 「次数を上げて増えた獲物」 | +54個 (豪華!) | +4個 (地味…) |

自慢の「豊かな階層」は、**まるごと幻**でした。

正しく計算したら、次数4で捕まる子は次数6でも全部捕まる。きれいに**入れ子**になっていて、次数を上げて新しく増える獲物はたった4個。「次数で証明能力が階層的に増える」という映える絵は、ズルする電卓が作った砂上の楼閣だったのです。

![電卓を入れ替えると幻が崩れる図 (再掲)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap.svg)

— ここで一息。「やられた、自慢が崩れた」で終わると思いきや、話はもう一ひねりあります。 —

---

## 第4幕: 幻の壊れ方が面白い ── 盛りすぎと、控えめすぎ

普通、「都合のいい数字が崩れる」と言えば、全部しょぼくなって終わりです。でも今回の電卓のズルは**両方向**にかかっていました。

- **ある所では「盛りすぎ」**: さっきの「豊かな階層」みたいに、実態より豪華に見せていた。
- **別の所では「控えめすぎ」**: もっと大きな検証 (3270個の部品) では、本命 SDP の強さを**過小評価**していた。

この「控えめすぎ」が効きます。本命 SDP は、素朴な検査法 (2-norm という単純な物差し) に対して「+254個ぶん強い」と見えていました。ところが正確な電卓で測り直すと、本当は「**+692個ぶん強い**」。SDP は思っていたより**ずっと優秀**だったのです。

念のため数字の出どころを補足すると、ズルする電卓 SCS は「本当は証明できる」案件を53件も取りこぼしていました。正確な電卓 CLARABEL はそのうち42〜43件を**回収**。残ったわずかな取りこぼしも、よく見ると **6件はわざと正しく弾いた「危ない部品」** で、これはミスではなく**正しい拒否**です。どのラング (検査の段) でも「ダメな部品を通した不健全な証明書」はゼロでした。

つまりこの一件、自慢が崩れた**負け**の話ではありません。

> **幻の階層は消えたが、本命の検査器 (SDP) はむしろ前より強いと判明した。**

統一された一つの真実は「**本命の SDP 検査器が、収縮する部品の約95%を証明できる**」。シンプルで、強い。

ちなみに「じゃあ暴走する部品をうっかり通しちゃう危険は?」という心配は無用でした。電卓のズルは「**ある証明書を見つけられない (偽陰性)**」方向のミスで、「**ダメな部品を OK と通す (偽許可)**」方向ではありません。別の独立した再チェックで「観測された偽許可ゼロ」を確認済み。**安全側に倒れるズル**だったので、検査器としての信頼は崩れていません。

---

## 第5幕: なぜ自力で気づけた? ── 多視点の敵対レビュー

ここがメタな見どころです。この罠、**普通の検査では構造的に見つかりません**。

よくある自己チェックに「margin-sweep (余白をちょっとずつ揺らして堅牢性を確かめる赤チーム)」があります。でもこれ、**同じズルする電卓の中で余白を揺らすだけ**。電卓自体が嘘をついているので、いくら揺らしても嘘は嘘のまま。気づけません。

効いた決定打は2つ。

1. **電卓を入れ替える (SOLVER-SWAP)**: SCS と CLARABEL で同じ問題を解かせて答えを突き合わせる。ここで初めて「あれ、電卓で答えが違う」と分かる。
2. **複数の視点で敵対的にレビューする (pair-review)**: 別の AI (Codex) と6体の懐疑エージェントが、それぞれ実コードと独立再計算で「お前の自慢、嘘だろ?」と反証を試みる。

このレビューで5件の指摘 (F1〜F5) が出ました。代表的なものだけ:

- **F1**: 電卓の指定が空っぽ ("") のとき、安全装置をすり抜けてこっそりズルする電卓 (SCS) に戻ってしまう穴があった → **塞いで回帰テスト追加**。
- **F2**: 「絶対安全」という言い回しが強すぎた → 「**観測された範囲で偽許可ゼロ**」に正直に弱めた。
- **F3**: ある主張の論理が**そもそも逆向き**だった → 訂正 (詳しくは完全版)。

結果、**中心の結論を覆す指摘はゼロ**。レビューがやったのは「言い過ぎを3つ削り、危ない穴を1つ塞いだ」こと。論旨は崩れるどころか、正直に弱められて**かえって頑丈**になりました。

![自分の結論を疑い続ける honest-disclosure ループ図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_honest_loop.svg)

### おまけ: 強い検査器は、進化そのものを良くする

「で、その正確な検査器を進化ループに組み込むと何が嬉しいの?」という当然の疑問にも、数字で答えが出ています。検査器なしで進化させると、生まれた子のうち **17〜20%** がこっそり暴走側へドリフトしていきます。本命 SDP の検査器を門番に置くと、**暴走する子は0匹も通りません**。

しかも面白いのは、ただ安全になるだけでなく**進化の上限まで上がる**こと。素朴な検査器 (inf-norm) では到達できた賢さが **約0.41** で頭打ちなのに対し、本命 SDP の検査器では **約0.86** まで伸びました (まぐれではない統計的な差つき)。**強い門番ほど、安全に到達できる賢さの天井を高く開放してくれる** ── 検査の精度は、安全のためだけでなく、進化の成果そのものを底上げするのです。

---

## 正直に言っておく限界 (honest disclosure)

良い話だけ書くのは FullSense の流儀に反するので、限界もそのまま開示します。

- **証明書を手の込ませても、必ず強くなるわけではない**。次数を上げると逆に**ゆるい (=弱い) 境界**を返すことがある。「次数を上げれば一直線に最強へ」は**嘘**です。
- 厳密な答えを出す計算は **NP困難** (現実的な時間では解けない難問)。境界ギリギリの約2個の部品は、CPU の範囲では証明しきれず**開いたまま**。きれいに閉じない、正直な限界です。
- 全部の結果は「小さい部品 (n=2)・CPU・このプール」の話。安全性は「**観測された範囲で偽許可ゼロ**」であって「数学的に絶対」ではない (機械チェック済みの厳密な証明は別途あり、ただし追加オプション扱い)。
- これは「**正しい検査器の作り方**」の話であって、「進化させた AI が広く役に立つ」という主張ではありません。

---

## で、結局何がわかったの?

一言でまとめます。

> **自慢の「豊かな成績表」は、ズルする電卓が作った幻だった。正確な電卓に替えたら幻は崩れ、本命の検査器はむしろ前より強いと判明した。**

そして今日いちばん伝えたいこと:

> **「うまく行きすぎた結果」は、勝ちではなく警報。**
> 数字が良すぎたら、信じる前にまず電卓 (ソルバ) を疑え。そして、同じ道具の中で揺らすだけの自己チェックは罠に盲目。**道具を入れ替える** ことと **別の視点から敵対的に叩く** ことが、幻を見破る決定打になる。

正直に自分を疑う仕組みを先に置いておいたから、ぬか喜びで止まらず、正しい土台にたどり着けた ── そういう一日でした。

---

**この記事の技術版 (完全版)**: [連載 #35-02「『良すぎる数値』を疑え: SCS ソルバの罠を多視点 pair-review で捕まえて訂正した話」](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)

---

# English

# (Plain-language edition) "Too-good numbers" aren't a win — they're an alarm: the story of how swapping one calculator made our proud result collapse

![Kamikudaki lion — a bite that grants the blessing of understanding](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_en.svg)

📗 This is the plain-language edition of the [full version](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615). Whenever a technical term shows up, we immediately swap it for an everyday analogy. Think of it as leveling the ground before the technical version, or a 10-minute "what did they roughly do?" for the curious.

![Diagram of fake numbers collapsing when the calculator is swapped](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_en.svg)

## Three-line summary

- We built a **verifier** that checks whether an evolved AI part will "run away" (diverge). When we measured its power, we got suspiciously "rich and convenient" numbers.
- The numbers were too good, so we got suspicious. The culprit: the **calculator (solver)** we used was cheating near the feasibility boundary. When we **swapped in an accurate calculator**, the proud result turned out to be an illusion.
- But the way the illusion broke is interesting. In one place it was **over-inflated**, in another **under-stated**. Our main verifier was actually **stronger** than we thought. The lesson, in one line: **"If the numbers are too good, suspect the calculator before you believe them."**

---

## Act 1: What are we even verifying?

In a research base called **llcore**, we evolve the "brain parts" of small AIs, bit by bit, like living organisms — under strict constraints: CPU-only, inside your own PC, zero cost.

Evolved parts vary in quality. The troublesome ones "run away": repeating the same computation, their numbers balloon and diverge — like a car stuck with the accelerator pinned. So we need a **verifier** that inspects each evolved part and decides:

> "Does this part stay calm (settle down) under repetition, instead of running away?"

It turns away the bad ones. The research question is simple: **"So how do you build a *correct* verifier?"**

We call the "settling down" property **contraction**: distance shrinks with each step, like a marble rolling down a slope and finally resting at the bottom. If we can issue a **mathematical certificate** that "this part really contracts," we can safely admit it.

There are several schools of computation for finding that certificate; the front-runner is **SDP**, a convex-optimization method — "search, within fixed rules, for a convenient certificate (a matrix P)."

---

## Act 2: A proud report card appeared — but it was too good

We measured the verifier's strength. We built a **stepwise ladder**: as we raise the "degree" (allow fancier certificates), the number of parts we can catch grows.

The first tally looked like this:

- Caught only by the fancier certificate (degree 4): 23 parts
- Caught only by the even fancier certificate (degree 6): 13 parts
- Caught by both: 18 parts

For a researcher this is "tasty," because some parts are caught only at degree 4 and others only at degree 6 — meaning **each higher degree unlocks fresh prey**, suggesting a "rich hierarchy of proving power." A picture that looks great in a paper.

…But here the [[honest-disclosure discipline]] kicks in. FullSense research has an iron rule:

> **If a result looks abnormally good, suspect the breakdown before you feel like you've won.**

The report card looked "too rich, too convenient," so instead of celebrating, we got suspicious.

---

## Act 3: The culprit was the calculator (this is the heart of it)

The certificate search is outsourced to a specialist **solver** ("calculator") behind the scenes. The default one was named **SCS**. Fast, but with a weakness:

> **Near the "boundary" of whether an answer barely exists, SCS cheats and reports "couldn't find one."**

Even though a certificate really did exist, it gave a **false report (false negative)**: "Nope, couldn't find it." The calculator half-knew, quietly flashing a warning: "Solution may be inaccurate."

So we swapped in **CLARABEL**, an accurate-but-slower **interior-point** calculator. Same pool of parts, same problems, calculator only switched. The result:

| Tally item | SCS (cheating calculator, false) | CLARABEL (accurate calculator, true) |
|---|---|---|
| degree-4-only / degree-6-only / both | 23 / 13 / 18 | 0 / 1 / 54 |
| Structural reading | scattered (looks like a rich hierarchy) | clean nesting (actually simple) |
| "Left unproven" | 53 parts | 10 parts |
| Main SDP coverage | 64% | **95%** |
| "Prey gained by raising degree" | +54 (lavish!) | +4 (modest…) |

The proud "rich hierarchy" was **entirely an illusion**.

Computed correctly, every part caught at degree 4 is also caught at degree 6. It nests cleanly, and raising the degree gains only 4 new parts. The flashy "proving power grows hierarchically with degree" picture was a castle on sand, built by a cheating calculator.

![Diagram of the illusion collapsing on calculator swap (reprise)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_en.svg)

— A pause here. You'd think it ends at "ouch, the boast collapsed," but there's one more twist. —

---

## Act 4: The way the illusion broke is interesting — over-inflated, and under-stated

Usually "convenient numbers collapse" just means everything shrinks and that's it. But this calculator's cheating ran **both ways**.

- **In one place, "over-inflated":** like the "rich hierarchy," it made things look fancier than reality.
- **In another, "under-stated":** in a larger check (3270 parts), it **under-estimated** the main SDP's strength.

The under-statement is the punch line. The main SDP looked "+254 parts stronger" than a naive method (a simple yardstick called 2-norm). Re-measured with the accurate calculator, it was really "**+692 parts stronger**." SDP was **far better** than we thought.

So this episode is not a story of a **loss** where a boast collapses.

> **The illusory hierarchy vanished, but the main verifier (SDP) turned out to be even stronger than before.**

The single unified truth: **"the main SDP verifier can prove about 95% of the contracting parts."** Simple, and strong.

By the way, "doesn't this risk waving through a runaway part?" — no need to worry. The calculator's cheating was the "**can't find a certificate (false negative)**" kind of error, not the "**OK a bad part (false admit)**" kind. A separate independent re-check confirmed "zero false admits observed." It was cheating that **fails to the safe side**, so trust in the verifier itself didn't collapse.

---

## Act 5: How did we catch it ourselves? — multi-perspective adversarial review

Here's the meta highlight. This trap is **structurally invisible to ordinary checks**.

A common self-check is "margin-sweep" (a red team that nudges the margins to test robustness). But it only **nudges margins inside the same cheating calculator**. The calculator itself is lying, so no matter how much you nudge, a lie stays a lie. You can't catch it.

Two things were decisive:

1. **Swap the calculator (SOLVER-SWAP):** have SCS and CLARABEL solve the same problems and compare answers. Only here do you notice "huh, the answers differ by calculator."
2. **Review adversarially from multiple perspectives (pair-review):** another AI (Codex) plus six skeptic agents each tried, with real code and independent recomputation, to **refute** the headline claims: "your boast — that's a lie, right?"

The review raised five findings (F1–F5). The representative ones:

- **F1:** when the solver field was empty (""), there was a hole that slipped past the safety guard and quietly fell back to the cheating calculator (SCS) → **plugged, with a regression test added**.
- **F2:** the "absolutely safe" phrasing was too strong → honestly weakened to "**zero false admits observed**."
- **F3:** the logic of one claim was **backwards to begin with** → corrected (see the full version).

The result: **zero findings overturned the central conclusion.** What the review did was "trim three overclaims and plug one dangerous hole." Far from collapsing, the thesis was honestly weakened and thereby made **sturdier**.

![Diagram of the honest-disclosure loop that keeps doubting its own conclusion](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_honest_loop_en.svg)

---

## Limits, stated honestly (honest disclosure)

Writing only the good parts goes against the FullSense way, so here are the limits as-is.

- **Making the certificate fancier doesn't always make it stronger.** Raising the degree can return a **looser (weaker) bound**. "Raise the degree and march straight to the strongest" is **false**.
- The computation that gives exact answers is **NP-hard** (a problem not solvable in realistic time). About 2 parts right at the boundary stay **open** within CPU range. A limit that doesn't close cleanly — and we say so honestly.
- All results are for "small parts (n=2), CPU, this pool." Safety is "**zero false admits observed**," not "mathematically absolute" (there is a separate machine-checked rigorous proof, but it's treated as an add-on option).
- This is about "**how to build a correct verifier**," not a claim that "evolved AIs are broadly useful."

---

## So, what did we actually learn?

In one line:

> **The proud "rich report card" was an illusion built by a cheating calculator. Swap in an accurate calculator and the illusion collapses — and the main verifier turns out to be even stronger than before.**

And the thing I most want to convey today:

> **A result that "goes too well" is not a win; it's an alarm.**
> If the numbers are too good, suspect the calculator (solver) before you believe them. And a self-check that merely nudges inside the same tool is blind to the trap. **Swapping the tool** and **attacking adversarially from another perspective** are what break the illusion.

Because we set up the machinery to honestly doubt ourselves first, we didn't stop at premature joy and reached solid ground — that was the kind of day it was.

---

**Technical (full) version of this article:** [Series #35-02 "Suspect 'too-good numbers': how a multi-perspective pair-review caught and corrected the SCS solver trap"](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)

---

# 中文

# (通俗版) "太好的数字"不是胜利，而是警报 —— 换掉一台计算器，自豪的结果就崩塌了

![通俗易懂版舞狮 — 被咬的读者获得「理解」的福气](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_zh.svg)

📗 这是[完整版](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)的通俗版。一旦出现专业术语，我们立刻换成日常比喻。可以把它当作技术版之前的铺垫，或者给想用10分钟掌握"他们大概在做什么"的人看。

![换掉计算器后假数字崩塌的示意图](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_zh.svg)

## 三行摘要

- 我们做了一个**检查器 (verifier)**，用来判断进化出的 AI 部件会不会"失控"(发散)。测它的能力时，得到了可疑地"丰富又方便"的数字。
- 数字太好了，于是起了疑心。元凶是：计算用的**计算器 (solver)** 在可行性边界附近作弊。**换上准确的计算器**后，自豪的结果原来是幻象。
- 但幻象崩塌的方式很有意思。一处是**夸大**，另一处反而是**低估**。主力检查器其实比我们想的**更强**。教训一句话——**"数字太好时，先怀疑计算器，再选择相信。"**

---

## 第一幕：到底在检查什么？

在名为 **llcore** 的研究基座里，我们像培育生物一样，一点点改造小型 AI 的"大脑部件"——并带着严格约束：仅用 CPU、只在自己的电脑里、零成本。

进化出的部件质量参差不齐。麻烦的是会"失控"的部件：重复同一计算时数字越滚越大、最终发散——就像油门被卡死的汽车。所以需要一个**检查器**，逐个检查进化出的部件并判断：

> "这个部件在重复时会保持平静(逐渐稳定)，而不是失控吗？"

把坏的挡在门外。研究问题很简单：**"那么，正确的检查器该怎么造？"**

我们把"逐渐稳定"的性质称为**收缩 (contraction)**：每走一步距离都缩小，像滚下斜坡的玻璃球最终停在谷底。如果能开出一张"这个部件确实收缩"的**数学证书**，就能放心通过。

寻找该证书的计算有几个流派，主力是 **SDP**(一种凸优化方法)——"在固定规则内，搜索一张方便的证书(矩阵 P)"。

---

## 第二幕：自豪的成绩单出现了——可它太好了

我们测了检查器的实力，做了一个**逐级阶梯**：随着"次数"提高(允许更花哨的证书)，能抓到的部件越来越多。

最初的统计是这样的：

- 只被更花哨证书(次数4)抓到的部件：23个
- 只被更花哨证书(次数6)抓到的部件：13个
- 两者都抓到的部件：18个

对研究者来说这很"香"，因为有些部件只在次数4被抓、有些只在次数6被抓——意味着**每提高一档次数就解锁新猎物**，看起来有"丰富的证明能力层级"。论文里很好看的一张图。

……但这里 [[honest disclosure 纪律]] 启动了。FullSense 研究有铁律：

> **若结果异常地好，在觉得自己赢了之前，务必怀疑其内部构成。**

成绩单"太丰富、太方便"，于是没有庆祝，而是去怀疑。

---

## 第三幕：元凶是计算器(这是核心)

寻找证书的计算，幕后是甩给一个专用 **solver**("计算器")。默认那台名叫 **SCS**。优点是快，但有弱点：

> **在"答案是否勉强存在"的边界附近，SCS 会作弊并报告"没找到"。**

明明证书确实存在，它却给出**假报告(假阴性)**："没找到。"计算器自己也半知半觉，悄悄闪出警告："Solution may be inaccurate(此解可能不准确)。"

于是我们换上 **CLARABEL**，一台准确但稍慢的**内点法**计算器。同一批部件、同样的问题，只换计算器。结果：

| 统计项 | SCS(作弊计算器·假) | CLARABEL(准确计算器·真) |
|---|---|---|
| 仅次数4 / 仅次数6 / 两者 | 23 / 13 / 18 | 0 / 1 / 54 |
| 结构解读 | 零散(看似丰富的层级) | 干净的嵌套(其实简单) |
| "未证明剩余数" | 53个 | 10个 |
| 主力 SDP 覆盖率 | 64% | **95%** |
| "提高次数新增猎物" | +54(豪华！) | +4(朴素…) |

自豪的"丰富层级"，**整个是幻象**。

正确计算后，次数4抓到的部件，次数6全都抓得到。干净地**嵌套**，提高次数只新增4个。"证明能力随次数分层增长"那张好看的图，是作弊计算器搭起的沙上楼阁。

![换掉计算器后幻象崩塌的示意图(重出)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_zh.svg)

— 在此小憩。你以为故事到"哎呀，吹的牛崩了"就结束，其实还有一个转折。 —

---

## 第四幕：幻象崩塌的方式很有意思——夸大，和低估

通常"方便的数字崩塌"就是全部缩水、到此为止。但这台计算器的作弊是**双向**的。

- **一处"夸大"：** 像那个"丰富层级"，把东西显得比现实更花哨。
- **另一处"低估"：** 在更大规模的检查(3270个部件)里，**低估**了主力 SDP 的强度。

这个低估是包袱所在。主力 SDP 相对朴素方法(一个叫 2-norm 的简单标尺)看起来"强 +254 个部件"。用准确计算器重测，实际是"**强 +692 个部件**"。SDP 比我们想的**强得多**。

所以这桩事并不是吹牛崩塌的**失败**故事。

> **虚幻的层级消失了，但主力检查器(SDP)反而比之前更强了。**

统一的一个真相：**"主力 SDP 检查器能证明约95%的收缩部件。"** 简单，而强。

顺便说，"那会不会不小心放过一个失控部件？"——不必担心。计算器的作弊是"**找不到证书(假阴性)**"那一类错误，不是"**把坏部件判为 OK(假放行)**"那一类。另一项独立复查确认"观测到的假放行为零"。这是**偏向安全侧**的作弊，所以对检查器本身的信任并未崩塌。

---

## 第五幕：我们怎么自己抓到的？——多视角对抗式评审

这是元层面的看点。这个陷阱**对普通检查在结构上是不可见的**。

常见的自检是"margin-sweep"(一支微调余量、测试稳健性的红队)。但它只在**同一台作弊计算器内部微调余量**。计算器本身在说谎，无论怎么微调，谎言还是谎言。抓不到。

起决定作用的有两点：

1. **换计算器(SOLVER-SWAP)：** 让 SCS 和 CLARABEL 解同样的问题并对照答案。只有在这里才会发现"咦，按计算器答案不一样"。
2. **从多个视角对抗式评审(pair-review)：** 另一个 AI(Codex)加上六个怀疑者智能体，各自用真实代码与独立重算，试图**反驳**头条主张："你吹的牛，是假的吧？"

这次评审提出五条(F1–F5)。代表性的几条：

- **F1：** 当 solver 字段为空("")时，存在一个绕过安全护栏、悄悄退回作弊计算器(SCS)的漏洞 → **已堵上，并加了回归测试**。
- **F2：** "绝对安全"的措辞太强 → 诚实地弱化为"**观测到的假放行为零**"。
- **F3：** 某条主张的逻辑**本就方向相反** → 已更正(详见完整版)。

结果：**没有任何一条推翻中心结论。** 评审做的是"削去三处过度主张、堵上一个危险漏洞"。论点非但没崩，反而被诚实地弱化而**更加结实**。

![不断怀疑自身结论的 honest-disclosure 循环图](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_honest_loop_zh.svg)

---

## 诚实交代的局限 (honest disclosure)

只写好的部分有违 FullSense 的风格，所以局限也原样公开。

- **把证书弄得更花哨，未必更强。** 提高次数可能返回**更松(更弱)的界**。"提高次数就一路走到最强"是**假的**。
- 给出精确答案的计算是 **NP 困难**(现实时间内无法求解的难题)。恰在边界上的约2个部件，在 CPU 范围内**仍未闭合**。一个无法干净闭合的局限——我们如实说出。
- 全部结果都是"小部件(n=2)、CPU、这一批"的情形。安全性是"**观测到的假放行为零**"，并非"数学上绝对"(另有一份机器校验的严格证明，但作为附加选项处理)。
- 这讲的是"**如何造一个正确的检查器**"，不是声称"进化出的 AI 普遍有用"。

---

## 那么，到底学到了什么？

一句话：

> **自豪的"丰富成绩单"是作弊计算器造的幻象。换上准确的计算器，幻象崩塌——而主力检查器反而比之前更强。**

以及今天最想传达的：

> **"太顺的结果"不是胜利，而是警报。**
> 数字太好时，先怀疑计算器(solver)，再选择相信。而只在同一工具内微调的自检，对陷阱是盲的。**换工具**与**从另一视角对抗式攻击**，才是戳破幻象的决定手。

正因为我们先架好了诚实怀疑自己的机制，才没有止步于过早的喜悦、抵达了坚实的地面——就是这样的一天。

---

**本文的技术(完整)版：** [连载 #35-02"怀疑'太好的数字'：多视角 pair-review 如何抓住并更正 SCS 求解器陷阱"](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)

---

# 한국어

# (쉬운 풀이판) "너무 좋은 숫자"는 승리가 아니라 경보 —— 계산기 하나를 바꿨더니 자랑하던 결과가 무너진 이야기

![쉬운 설명판 사자탈 — 물린 독자에게 「이해」의 복](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/mascot/kamikudaki_shishi_ko.svg)

📗 이 글은 [완전판](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)의 쉬운 풀이판입니다. 전문 용어가 나오면 바로 일상적인 비유로 바꿉니다. 기술판을 읽기 전의 사전 정지 작업, 또는 "대충 뭘 한 거야?"를 10분 만에 잡고 싶은 분을 위한 글입니다.

![계산기를 바꾸면 가짜 숫자가 무너지는 그림](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_ko.svg)

## 세 줄 요약

- 진화시킨 AI 부품이 "폭주하지 않는지"를 검사하는 **검사기 (verifier)** 를 만들었다. 성능을 재 봤더니 의심스러울 만큼 "풍부하고 편리한" 숫자가 나왔다.
- 숫자가 너무 좋아서 의심했다. 원인은 계산에 쓰던 **계산기 (solver)** 가 가능성 경계 부근에서 속임수를 쓰고 있었던 것. **정확한 계산기로 바꾸니** 자랑하던 결과는 환상이었음이 드러났다.
- 그런데 환상이 무너지는 방식이 흥미롭다. 한쪽은 **과장**, 다른 쪽은 오히려 **과소평가**. 주력 검사기는 사실 생각보다 **더 강했다**. 교훈은 한 줄 —— **"숫자가 너무 좋으면 믿기 전에 먼저 계산기를 의심하라."**

---

## 제1막: 애초에 무엇을 검사하나?

**llcore** 라는 연구 기반에서 우리는 작은 AI의 "두뇌 부품"을 생물의 진화처럼 조금씩 고쳐 만듭니다 —— 엄격한 제약과 함께: CPU만, 내 PC 안에서만, 비용 제로.

진화시킨 부품은 품질이 들쭉날쭉합니다. 골치 아픈 건 "폭주하는" 부품: 같은 계산을 반복하는 사이 숫자가 점점 불어나 발산합니다 —— 액셀이 고착된 자동차 같은 거죠. 그래서 **검사기**가 필요합니다. 진화한 부품을 하나씩 조사해 판정합니다:

> "이 부품은 반복해도 차분히 (오히려 안정되게) 가라앉는가, 폭주하지 않는가?"

나쁜 놈은 문전박대합니다. 연구 질문은 단순합니다: **"그럼 올바른 검사기는 어떻게 만드나?"**

"가라앉는" 성질을 연구에서는 **수축 (contraction)** 이라 부릅니다: 한 걸음마다 거리가 줄어, 비탈을 굴러 내려가는 구슬이 결국 골짜기 바닥에서 멈추는 이미지. 그리고 "이 부품은 확실히 수축한다"는 **수학적 증명서**를 발행할 수 있으면 안심하고 통과시킵니다.

이 증명서를 찾는 계산에는 몇 가지 유파가 있는데, 본명은 **SDP** 라는 볼록 최적화 기법 —— "정해진 규칙 안에서 편리한 증명서(행렬 P)를 찾아온다"는 이미지입니다.

---

## 제2막: 자랑스러운 성적표가 나왔다 —— 그런데 너무 좋았다

검사기의 실력을 쟀습니다. "차수를 올리면(더 공들인 증명서를 허용하면) 잡을 수 있는 부품이 점점 늘어난다"는 **단계별 사다리**를 만들었죠.

처음 집계는 이런 느낌이었습니다:

- 더 공들인 증명서(차수4)로만 잡힌 부품: 23개
- 더더욱 공들인 증명서(차수6)로만 잡힌 부품: 13개
- 둘 다로 잡힌 부품: 18개

연구자에게 이건 "맛있는" 결과입니다. 어떤 부품은 차수4에서만, 어떤 부품은 차수6에서만 잡힌다 —— 즉 **차수를 올릴 때마다 새 사냥감이 늘어난다** = "증명 능력에 풍부한 계층이 있다"처럼 보이니까요. 논문에 잘 어울리는 그림입니다.

…그런데 여기서 [[honest disclosure 규율]]이 발동합니다. FullSense 연구에는 철칙이 있습니다:

> **비정상적으로 좋은 결과가 나오면, 이겼다고 느끼기 전에 반드시 내역을 의심하라.**

성적표가 "너무 풍부, 너무 편리"했기에 순순히 기뻐하지 않고 의심에 나섰습니다.

---

## 제3막: 범인은 계산기였다 (여기가 핵심)

증명서를 찾는 계산은 뒤에서 전용 **solver** ("계산기") 에 통째로 맡깁니다. 기본 계산기 이름은 **SCS**. 빠른 게 장점이지만 약점이 있었습니다:

> **답이 가까스로 존재하는지 마는지의 "경계" 부근에서, SCS는 속임수를 써서 "못 찾았습니다"라고 말해버린다.**

사실은 증명서가 분명히 존재하는데도 **거짓 보고(거짓 음성)** 를 한 겁니다: "아니요, 못 찾았어요." 계산기 자신도 어렴풋이 알아서 "Solution may be inaccurate(이 답, 부정확할 수 있음)"라는 경고를 작게 띄우고 있었죠.

그래서 정확하지만 조금 느린 **내점법** 계산기 **CLARABEL** 로 바꿔봤습니다. 같은 부품 풀, 같은 문제, 계산기만 스위치. 그러자 ——

| 집계 항목 | SCS (속이는 계산기·거짓) | CLARABEL (정확한 계산기·참) |
|---|---|---|
| 차수4만 / 차수6만 / 둘 다 | 23 / 13 / 18 | 0 / 1 / 54 |
| 구조 해석 | 제각각 (풍부한 계층처럼 보임) | 깔끔한 중첩 (실은 단순) |
| "미증명으로 남은 수" | 53개 | 10개 |
| 주력 SDP 커버율 | 64% | **95%** |
| "차수를 올려 늘어난 사냥감" | +54 (호화!) | +4 (수수…) |

자랑하던 "풍부한 계층"은 **통째로 환상**이었습니다.

올바르게 계산하니, 차수4에서 잡히는 부품은 차수6에서도 전부 잡힙니다. 깔끔하게 **중첩**되어 있고, 차수를 올려 새로 느는 사냥감은 고작 4개. "증명 능력이 차수에 따라 계층적으로 늘어난다"는 멋진 그림은, 속이는 계산기가 쌓아 올린 모래 위 누각이었습니다.

![계산기를 바꾸면 환상이 무너지는 그림 (재게재)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_ko.svg)

— 여기서 한숨 돌립시다. "당했다, 자랑이 무너졌다"로 끝날 줄 알았겠지만, 이야기엔 한 번의 반전이 더 있습니다. —

---

## 제4막: 환상이 무너지는 방식이 흥미롭다 —— 과장, 그리고 과소평가

보통 "편리한 숫자가 무너진다"면 전부 초라해지고 끝입니다. 하지만 이번 계산기의 속임수는 **양방향**으로 걸려 있었습니다.

- **한쪽은 "과장":** 아까의 "풍부한 계층"처럼, 실태보다 호화롭게 보이게 했다.
- **다른 쪽은 "과소평가":** 더 큰 검증(3270개 부품)에서는 주력 SDP의 강함을 **과소평가**했다.

이 과소평가가 한 방입니다. 주력 SDP는 소박한 검사법(2-norm이라는 단순한 잣대)에 대해 "+254개만큼 강하다"로 보였습니다. 그런데 정확한 계산기로 다시 재니, 사실은 "**+692개만큼 강하다**". SDP는 생각보다 **훨씬 우수**했던 거죠.

그러니 이 사건은 자랑이 무너진 **패배**의 이야기가 아닙니다.

> **환상의 계층은 사라졌지만, 주력 검사기(SDP)는 오히려 전보다 강하다고 드러났다.**

통일된 하나의 진실: **"주력 SDP 검사기가 수축하는 부품의 약 95%를 증명할 수 있다."** 단순하고, 강합니다.

참고로 "그럼 폭주하는 부품을 실수로 통과시킬 위험은?" —— 걱정 없습니다. 계산기의 속임수는 "**증명서를 못 찾는(거짓 음성)**" 종류의 실수이지, "**나쁜 부품을 OK로 통과(거짓 허가)**" 하는 종류가 아닙니다. 별개의 독립 재검사로 "관측된 거짓 허가 0"을 확인했습니다. **안전한 쪽으로 넘어지는** 속임수였기에, 검사기에 대한 신뢰는 무너지지 않았습니다.

---

## 제5막: 어떻게 스스로 잡아냈나? —— 다시점 적대적 리뷰

여기가 메타적인 볼거리입니다. 이 함정은 **보통 검사에는 구조적으로 보이지 않습니다.**

흔한 자체 점검에 "margin-sweep"(여백을 조금씩 흔들어 강건성을 확인하는 레드팀)이 있습니다. 하지만 이건 **같은 속이는 계산기 안에서 여백을 흔들 뿐**. 계산기 자체가 거짓말을 하니, 아무리 흔들어도 거짓은 거짓 그대로. 잡지 못합니다.

결정타는 두 가지:

1. **계산기를 바꾼다 (SOLVER-SWAP):** SCS와 CLARABEL에게 같은 문제를 풀게 하고 답을 맞대어 본다. 여기서 비로소 "어, 계산기마다 답이 다르네"를 알게 된다.
2. **여러 시점에서 적대적으로 리뷰한다 (pair-review):** 다른 AI(Codex)와 6체의 회의주의 에이전트가 각자 실제 코드와 독립 재계산으로 헤드라인 주장을 **반증**하려 시도한다: "네 자랑, 거짓말이지?"

이 리뷰에서 5건(F1–F5)이 나왔습니다. 대표적인 것만:

- **F1:** solver 항목이 비었을 때("") 안전장치를 빠져나가 슬그머니 속이는 계산기(SCS)로 되돌아가는 구멍이 있었다 → **막고 회귀 테스트 추가**.
- **F2:** "절대 안전"이라는 표현이 너무 강했다 → "**관측된 거짓 허가 0**"으로 정직하게 약화.
- **F3:** 어떤 주장의 논리가 **애초에 방향이 반대**였다 → 정정(자세한 건 완전판).

결과: **중심 결론을 뒤집은 지적은 0건.** 리뷰가 한 일은 "과한 주장 셋을 깎고, 위험한 구멍 하나를 막은" 것. 논지는 무너지기는커녕 정직하게 약화되어 **오히려 더 단단해졌습니다**.

![자신의 결론을 계속 의심하는 honest-disclosure 루프 그림](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_honest_loop_ko.svg)

---

## 정직하게 밝히는 한계 (honest disclosure)

좋은 이야기만 쓰는 건 FullSense의 방식에 어긋나므로, 한계도 그대로 공개합니다.

- **증명서를 더 공들인다고 반드시 강해지는 건 아니다.** 차수를 올리면 오히려 **더 느슨한(약한) 경계**를 돌려줄 수 있다. "차수를 올리면 일직선으로 최강에 도달"은 **거짓**이다.
- 정확한 답을 내는 계산은 **NP-난해**(현실적 시간 안에 풀 수 없는 난문). 경계에 딱 걸린 약 2개 부품은 CPU 범위에서 **여전히 열린 채**. 깔끔하게 닫히지 않는, 정직한 한계입니다.
- 모든 결과는 "작은 부품(n=2)·CPU·이 풀"의 이야기. 안전성은 "**관측된 거짓 허가 0**"이지 "수학적으로 절대"가 아니다(별도의 기계 검증된 엄밀한 증명이 있으나 추가 옵션으로 다룸).
- 이는 "**올바른 검사기를 만드는 법**"의 이야기이지, "진화시킨 AI가 널리 쓸모 있다"는 주장이 아닙니다.

---

## 그래서, 결국 무엇을 알았나?

한 줄로:

> **자랑하던 "풍부한 성적표"는 속이는 계산기가 만든 환상이었다. 정확한 계산기로 바꾸니 환상은 무너지고 —— 주력 검사기는 오히려 전보다 강하다고 드러났다.**

그리고 오늘 가장 전하고 싶은 것:

> **"너무 잘 풀린 결과"는 승리가 아니라 경보.**
> 숫자가 너무 좋으면 믿기 전에 먼저 계산기(solver)를 의심하라. 그리고 같은 도구 안에서 흔들기만 하는 자체 점검은 함정에 눈먼다. **도구를 바꾸는 것**과 **다른 시점에서 적대적으로 두드리는 것**이 환상을 깨는 결정타가 된다.

정직하게 자신을 의심하는 장치를 먼저 깔아 두었기에, 섣부른 기쁨에서 멈추지 않고 단단한 토대에 다다랐다 —— 그런 하루였습니다.

---

**이 글의 기술(완전)판:** [연재 #35-02 "'너무 좋은 숫자'를 의심하라: 다시점 pair-review로 SCS 솔버의 함정을 잡아 정정한 이야기"](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)
