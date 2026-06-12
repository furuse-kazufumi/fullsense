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

証明書 (歪んだものさし P) を探す計算は、定型化された数学の問題なので、裏で**ソルバ**という「専門電卓」に丸投げしています。料理人がだしを取る工程を専用機械に任せるようなもので、それ自体は普通のことです。問題は、その電卓の**性格**でした。

使っていたデフォルトの電卓は **SCS** という名前。「ざっくり速く」が信条のタイプで、軽い反復計算で答えに近づいていき、「だいたい合ってる」ところで切り上げます。普段はそれで十分。ところが弱点がありました。

> **答えがギリギリ存在するかどうかの「境界」付近で、SCS はズルをして「見つかりませんでした」と言ってしまう。**

部品には「証明書が余裕で見つかるもの」と「ギリギリ見つかるもの」がいます。余裕案件なら、どんな電卓でも正解できる。でもギリギリ案件 ── 駐車場の枠に数センチの余裕でなんとか入る車みたいなケース ── では、「だいたい」で切り上げる電卓は「入りません (見つかりません)」と答えてしまう。本当はちゃんと証明書が存在するのに、「いや〜、見つからなかったっす」と**嘘の報告 (偽陰性)** をしていたのです。

たちが悪いことに、電卓自身も薄々気づいていて「Solution may be inaccurate (この答え、不正確かも)」という警告を小さく出していました。体重計の隅に「参考値」と表示されているのに、数字だけ読んで記録していたようなものです。

そこで、正確だけど少し遅い**内点法**という別の電卓 **CLARABEL** に入れ替えてみました。内点法は、答えの存在範囲の「内側」を慎重に歩いて高精度の答えにたどり着くタイプで、境界ギリギリの案件にも強い。暗算の達人 (SCS) に対する、筆算で丁寧に検算する人 (CLARABEL) です。

ここで大事なのは実験の組み方。**同じ部品プール、同じ問題、電卓だけスイッチ**。理科の対照実験と同じで、変えたものが1つだけなら、結果が変わったとき「変わった原因はそれ」と言い切れます。すると ──

| 集計項目 | SCS (ズルする電卓・偽) | CLARABEL (正確な電卓・真) |
|---|---|---|
| 次数4だけ / 次数6だけ / 両方 | 23 / 13 / 18 | 0 / 1 / 54 |
| 構造の解釈 | バラバラ (豊かな階層に見える) | きれいな入れ子 (実はシンプル) |
| 「未証明で残った数」 | 53個 | 10個 |
| 本命 SDP のカバー率 | 64% (300個中193個) | **95% (300個中286個)** |
| 「次数を上げて増えた獲物」 | +54個 (豪華!) | +4個 (地味…) |

自慢の「豊かな階層」は、**まるごと幻**でした。

表を一行ずつ読みほどくと:

- **「次数4だけ」が 23 → 0**: 正確に計算したら、「次数4の網でしか捕れない魚」は1匹もいなかった。次数4で捕まる子は次数6でも全部捕まる。マトリョーシカ人形みたいに、大きい網の捕獲リストが小さい網のリストを丸ごと含む、きれいな**入れ子**だったのです。
- **「未証明で残った数」が 53 → 10**: 「証明できませんでした」の山の大半は、部品が悪いのではなく**電卓の取りこぼし**だった。
- **カバー率 64% → 95%**: 本命 SDP は実は、収縮する部品のほとんどを一人で証明できていた。
- **「次数を上げて増えた獲物」+54 → +4**: 高い次数の固有の手柄は、豪華な54ではなくささやかな4。

「次数で証明能力が階層的に増える」という映える絵は、ズルする電卓が作った砂上の楼閣だったのです。

![電卓を入れ替えると幻が崩れる図 (再掲)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap.svg)

— ここで一息。「やられた、自慢が崩れた」で終わると思いきや、話はもう一ひねりあります。 —

---

## 第4幕: 幻の壊れ方が面白い ── 盛りすぎと、控えめすぎ

普通、「都合のいい数字が崩れる」と言えば、全部しょぼくなって終わりです。でも今回の電卓のズルは**両方向**にかかっていました。同じ「見つかりませんでした」という一種類のミスでも、**何を測っているか**によって、見かけを盛ることも削ることもあるのです。

- **ある所では「盛りすぎ」**: 取りこぼしが次数4と次数6にバラバラに散ったせいで、「それぞれの網に固有の獲物がいる」ように見えた。さっきの「豊かな階層」がこれで、実態より豪華に見せていた。
- **別の所では「控えめすぎ」**: もっと大きな検証 (3270個の部品) では、本命 SDP が本来取れるはずだった手柄を取りこぼして、SDP の強さを**過小評価**していた。

この「控えめすぎ」が効きます。本命 SDP は、素朴な検査法 (2-norm という単純な物差し) に対して「+254個ぶん強い」と見えていました。ところが正確な電卓で測り直すと、本当は「**+692個ぶん強い**」。SDP は思っていたより**ずっと優秀**だったのです。

なぜ差がこれほど開いたのか。素朴な 2-norm の判定は電卓いらずで直接計算できる (= ズルの影響を受けない) 一方、SDP の判定だけがズルする電卓を経由していたからです。徒競走にたとえると、本命選手だけ足に砂袋をつけて走らされていた。砂袋を外したら、もともとの実力差がそのまま出た、という話です。

念のため数字の出どころを補足すると、ズルする電卓 SCS は「本当は証明できる」案件を53件も取りこぼしていました。正確な電卓 CLARABEL はそのうち42〜43件を**回収**。残ったわずかな取りこぼしも、よく見ると **6件はわざと正しく弾いた「危ない部品」** で、これはミスではなく**正しい拒否**です。この6件は、ふだんの動かし方では大人しいのに、最悪の順番で動かすと距離が伸びてしまうタイプの部品 ── 第1幕で「観察だけでは足りない」と言った、まさにその実例でした。どのラング (検査の段) でも「ダメな部品を通した不健全な証明書」はゼロでした。

つまりこの一件、自慢が崩れた**負け**の話ではありません。

> **幻の階層は消えたが、本命の検査器 (SDP) はむしろ前より強いと判明した。**

統一された一つの真実は「**本命の SDP 検査器が、収縮する部品の約95%を証明できる**」。シンプルで、強い。

ちなみに「じゃあ暴走する部品をうっかり通しちゃう危険は?」という心配は無用でした。検査のミスには2種類あります。空港の手荷物検査でいえば、「安全な荷物を『怪しい』と止めてしまう」(不便だが事故にはならない) と、「危険物を素通りさせてしまう」(大惨事)。今回の電卓のズルは前者だけ ── 「**ある証明書を見つけられない (偽陰性)**」方向のミスで、「**ダメな部品を OK と通す (偽許可)**」方向ではありません。さらに、発行された証明書が本物かを別の計算方法でもう一度確かめる再チェックと、実際に部品を動かす組合せを試して暴走の反例を探す再チェック ── 独立した二系統の答え合わせで「観測された偽許可ゼロ」を確認済み。**安全側に倒れるズル**だったので、検査器としての信頼は崩れていません。

---

## 第5幕: なぜ自力で気づけた? ── 多視点の敵対レビュー

ここがメタな見どころです。この罠、**普通の検査では構造的に見つかりません**。

よくある自己チェックに「margin-sweep (余白をちょっとずつ揺らして堅牢性を確かめる赤チーム)」があります。判定の境目を少し厳しくしたり緩めたりして、結論がコロッと変わらないか試す手法で、ふだんは頼れるチェックです。でも今回は無力でした。なぜなら、揺らした条件での計算も**全部同じズルする電卓がやる**から。狂った体重計の上で、立ち位置を変えたり荷物を持ったりして何十回測り直しても、体重計そのものが狂っている事実は1ミリも見えてきません ── 比べている相手が全員、同じ嘘を共有しているからです。嘘を見破るには、**外**が要ります。

効いた決定打は2つ。どちらも「外」を持ち込む手です。

1. **電卓を入れ替える (SOLVER-SWAP)**: SCS と CLARABEL という素性の違う2台に同じ問題を解かせて答えを突き合わせる。2台目の体重計に乗って初めて「あれ、数字が違う」と分かる。
2. **複数の視点で敵対的にレビューする (pair-review)**: 別の AI (Codex) と6体の懐疑エージェントに「この結論を壊してみろ」という宿題を出す。大事なのは、彼らが感想を述べるのではなく、**実コードを読み、数字を独立に再計算して**反証を試みること。「お前の自慢、嘘だろ?」と本気で攻めさせるのです。

このレビューで5件の指摘 (F1〜F5) が出ました。代表的なものだけ:

- **F1**: 電卓の指定が空っぽ ("") のとき、安全装置をすり抜けてこっそりズルする電卓 (SCS) に戻ってしまう穴があった。プログラムの世界では空文字は「未記入」と同じ扱いになりがちで、「正確な電卓がなければ拒否しろ」という安全装置 (fail-closed) が「指定なし → デフォルトの SCS でいいか」と解釈してしまう抜け道です。問診票のアレルギー欄が空欄だと「なし」扱いになってしまう、あの怖さ → **塞いで回帰テスト (再発防止の自動テスト) を追加**。
- **F2**: 「絶対安全」という言い回しが強すぎた → 「**観測された範囲で偽許可ゼロ**」に正直に弱めた。調べた範囲では全部正しかった、と言えるところまでしか言わない。
- **F3**: ある主張の論理が**そもそも逆向き**だった。あるチェックを「ゆるくなる方向」と説明していたのに、実際は「より厳しい方向」だった、という向きの取り違え → 訂正 (詳しくは完全版)。

結果、**中心の結論を覆す指摘はゼロ**。レビューがやったのは「言い過ぎを3つ削り、危ない穴を1つ塞いだ」こと。主張の線を「どこから攻められても守り切れる位置」まで正直に下げる ── 城壁を守れる範囲まで縮めて固めるのと同じで、論旨は崩れるどころか**かえって頑丈**になりました。

![自分の結論を疑い続ける honest-disclosure ループ図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_honest_loop.svg)

### おまけ: 強い検査器は、進化そのものを良くする

「で、その正確な検査器を進化ループに組み込むと何が嬉しいの?」という当然の疑問にも、数字で答えが出ています。

まず安全面。検査器なしで進化させると、生まれた子のうち **17〜20%** がこっそり暴走側へドリフトしていきます。世代を重ねるうちに、危ない子が静かに混ざり続けるわけです。本命 SDP の検査器を門番に置くと、**暴走する子は0匹も通りません**。

しかも面白いのは、ただ安全になるだけでなく**進化の上限まで上がる**こと。素朴な検査器 (inf-norm) では到達できた賢さ (fitness) が **約0.41** で頭打ちなのに対し、本命 SDP の検査器では **約0.86** まで伸びました。偶然でこの差が出る確率は約10万分の3 (p = 3.1e-5) ── まぐれではありません。

なぜ門番を強くすると上限が上がるのか。弱い門番は、危ない部品を弾くだけでなく、**本当は安全な部品まで「証明できない」と大量に弾いてしまう**からです (実際、第2幕の成績ラダーでは、素朴なものさしが証明できたのは300個中88個、SDP は286個)。冤罪の多い門番の下では、進化は無難な設計しか試せない。安全なものを安全と見抜ける門番の下でなら、進化はより大胆な設計まで安心して試せる。**強い門番ほど、安全に到達できる賢さの天井を高く開放してくれる** ── 検査の精度は、安全のためだけでなく、進化の成果そのものを底上げするのです。

---

## 正直に言っておく限界 (honest disclosure)

良い話だけ書くのは FullSense の流儀に反するので、限界もそのまま開示します。

- **証明書を手の込ませても、必ず強くなるわけではない**。直感的には「ものさしの曲げ方の自由度を増やせば強くなる一方」のはずですが、実際には次数を上げると逆に**ゆるい (=弱い) 境界**を返すことがある。一番きつい見積もりが欲しければ、各次数の結果を並べて一番良いものを採るしかなく、きれいな一本の階段にはなっていません。「次数を上げれば一直線に最強へ」は**嘘**です。
- 厳密な答えを出す計算は **NP困難** (問題が大きくなると、知られているどの方法でも計算時間が爆発すると考えられている難問クラス)。残った未証明のうち、さらに手の込んだ証明 (次数8) で4個、厳密計算の挟み撃ちでそのうち2個まで閉じましたが、境界ギリギリの最後の約2個は、CPU の範囲では証明しきれず**開いたまま**。きれいに閉じない、正直な限界です。
- 全部の結果は「小さい部品 (n=2、状態の数字が2個)・CPU・このプール」の話。安全性は「**観測された範囲で偽許可ゼロ**」であって「数学的に絶対」ではない (機械チェック済みの厳密な証明は別途あり、ただし追加オプション扱い)。
- これは「**正しい検査器の作り方**」の話であって、「進化させた AI が広く役に立つ」という主張ではありません。

---

## で、結局何がわかったの?

一言でまとめます。

> **自慢の「豊かな成績表」は、ズルする電卓が作った幻だった。正確な電卓に替えたら幻は崩れ、本命の検査器はむしろ前より強いと判明した。**

そして今日いちばん伝えたいこと:

> **「うまく行きすぎた結果」は、勝ちではなく警報。**
> 数字が良すぎたら、信じる前にまず電卓 (ソルバ) を疑え。そして、同じ道具の中で揺らすだけの自己チェックは罠に盲目。**道具を入れ替える** ことと **別の視点から敵対的に叩く** ことが、幻を見破る決定打になる。

数値そのものより、**順番**を覚えて帰ってください。「良い結果が出る → 喜ぶ → 念のため確認」では、確認はどうしても甘くなります。「疑う仕組みを先に置く → 良い結果が出る → 仕組みが勝手に疑ってくれる」。正直に自分を疑う仕組みを先に置いておいたから、ぬか喜びで止まらず、正しい土台にたどり着けた ── そういう一日でした。

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

In a research base called **llcore**, we evolve the "brain parts" of small AIs, bit by bit, like living organisms. The recipe is a classic genetic algorithm; roughly, "make lots of candidates → keep the good ones → tweak them a little and try again," over and over — the same logic as breeding sweeter tomatoes. All under strict constraints: CPU-only, inside your own PC, zero cost.

Evolved parts vary in quality. The troublesome ones "run away." A "part" here is a small computing device that updates a state (a bundle of internal numbers) one step at a time, with its output fed back as the next input — a loop. In a loop like that, if "amplify" wins by even a sliver on each pass, the numbers snowball. It's the same shape as audio feedback when a microphone sits too close to a speaker: the mic picks up the speaker's sound, the amp boosts it, the speaker plays it louder, the mic picks that up again… and a whisper becomes a shriek in an instant. This is the computational version — a car stuck with the accelerator pinned.

So we need a **verifier** that inspects each evolved part and decides:

> "Does this part stay calm (settle down) under repetition, instead of running away?"

It turns away the bad ones. The research question is simple: **"So how do you build a *correct* verifier?"**

"Why not just run it and watch?" you might ask. But observation can only ever say "it has been calm **so far**." In fact — this comes up later in the story — there really are parts that behave on an ordinary run yet break loose only when they hit the worst-case conditions (the worst order of operations). Passing a test drive isn't enough. What we want is a guarantee that **covers the future**: "no matter how things unfold, this will not run away" — and that comes from mathematics, not observation.

We call the "settling down" property **contraction**: with every step, the distance to the resting point must shrink — like a marble in a bowl that always ends up at the bottom. If every single step shrinks the distance, blow-up is simply impossible; prove contraction, and the worry about runaway disappears. And if we can issue a **mathematical certificate** that "this part really contracts," we can safely admit it. Think of a building's structural-engineering report: not "we shook it and it didn't fall," but "we computed that it cannot fall under any shaking within this range."

The certificate itself is a matrix called P — in plain terms, a **skewed ruler**. A motion that doesn't look shrinking under an ordinary straight ruler can turn out to shrink at every step once you re-measure it with a custom-bent ruler fitted to that part. If you can say "measured with this skewed ruler P, every possible step shrinks the distance," that one sentence *is* the certificate of contraction.

The front-runner method for finding such a convenient ruler P is **SDP**, a kind of **convex optimization**. Convex optimization means problems shaped like a single bowl — searching for the lowest point in a bowl-shaped landscape, where no small fake dip can fool you. That is why an answer found there can be used directly as a guarantee — and why it works for certificate hunting.

By the way, we initially hoped that a fancy logic-puzzle solver (SMT/Z3) would also become a pillar of the verification. But on inspection, Z3 was **decorative** on this base. The questions we were asking Z3 actually reduce to **closed-form expressions** — formulas you can compute directly with ordinary arithmetic. Empirically too: checked against 20,000 cases and 3,270 cases, Z3's verdicts **matched the closed-form computation perfectly** (zero disagreements). We had hired a logic-puzzle master for problems a pocket calculator answers in one stroke. The master was never wrong — but never added anything either. What truly captured the essence of contraction was, after all, **the SDP certificate**. That's the groundwork.

---

## Act 2: A proud report card appeared — but it was too good

We measured the verifier's strength. The key concept is the **degree**. We just called the certificate a "skewed ruler"; the degree is that ruler's **freedom to bend**. Raising the degree allows ever more intricate ruler shapes = fancier certificates = in principle, more parts you can catch.

So we built a **stepwise ladder**: "as we raise the degree, how does the number of catchable parts grow?" — like a fishing log where you keep weaving the net finer and counting what each net catches.

The first tally looked like this:

- Caught only by the fancier certificate (degree 4): 23 parts
- Caught only by the even fancier certificate (degree 6): 13 parts
- Caught by both: 18 parts

Read it like this: 23 fish only the degree-4 net can catch, 13 fish only the degree-6 net can catch, and 18 caught by both. In other words, each net seems to have **fish that only it can catch**.

For a researcher this is "tasty." It looks like **each higher degree unlocks fresh prey** — a "rich hierarchy of proving power." "Every higher degree has its own unique reason to exist, so it's worth keeping every net" — a story where every new tool yields new results is the best-looking picture a paper can have.

…But here the [[honest-disclosure discipline]] kicks in. FullSense research has an iron rule:

> **If a result looks abnormally good, suspect the breakdown before you feel like you've won.**

Humans don't re-examine results that match their hopes; we only hunt for causes when results disappoint. Which means, left alone, it is exactly the *convenient* mistakes that slip through inspection and survive. Knowing that, we pre-committed to the opposite rule — the better the result, the harder we doubt it. The report card looked "too rich, too convenient," so instead of celebrating, we got suspicious.

---

## Act 3: The culprit was the calculator (this is the heart of it)

The search for the certificate (the skewed ruler P) is a standardized math problem, so it's outsourced to a specialist **solver** ("calculator") behind the scenes — like a kitchen delegating stock-making to a dedicated machine. Nothing wrong with that in itself. The problem was the calculator's **personality**.

The default calculator was named **SCS** — a "roughly but fast" type that creeps toward the answer with lightweight iterations and calls it a day at "approximately right." Usually that's plenty. But it had a weakness:

> **Near the "boundary" of whether an answer barely exists, SCS cheats and reports "couldn't find one."**

Some parts have certificates that exist with room to spare; others, only barely. Any calculator gets the comfortable cases right. But on the borderline cases — like a car that fits the parking space with just a few centimeters to spare — a calculator that stops at "approximately" answers "doesn't fit (couldn't find it)." Even though a certificate really did exist, it filed a **false report (false negative)**: "Nope, couldn't find it."

Worse, the calculator half-knew: it quietly flashed a warning, "Solution may be inaccurate." Like a bathroom scale showing "approximate reading" in the corner while we recorded only the number.

So we swapped in **CLARABEL**, an accurate-but-slower **interior-point** calculator. Interior-point methods walk carefully through the *inside* of the region where answers live, arriving at a high-precision result, so they hold up even on borderline cases. The mental-math whiz (SCS) versus the careful long-hand checker (CLARABEL).

The crucial part is the experimental design: **same pool of parts, same problems, only the calculator switched**. Just like a controlled experiment in science class — change exactly one thing, and when the outcome changes, you can pin the cause on that one thing. The result:

| Tally item | SCS (cheating calculator, false) | CLARABEL (accurate calculator, true) |
|---|---|---|
| degree-4-only / degree-6-only / both | 23 / 13 / 18 | 0 / 1 / 54 |
| Structural reading | scattered (looks like a rich hierarchy) | clean nesting (actually simple) |
| "Left unproven" | 53 parts | 10 parts |
| Main SDP coverage | 64% (193 of 300) | **95% (286 of 300)** |
| "Prey gained by raising degree" | +54 (lavish!) | +4 (modest…) |

The proud "rich hierarchy" was **entirely an illusion**.

Reading the table line by line:

- **"degree-4-only" went 23 → 0**: computed correctly, there wasn't a single fish only the degree-4 net could catch. Every part caught at degree 4 is also caught at degree 6 — like matryoshka dolls, the bigger net's catch list wholly contains the smaller net's. Clean **nesting**.
- **"Left unproven" went 53 → 10**: most of the "couldn't prove it" pile wasn't bad parts — it was the **calculator's dropped balls**.
- **Coverage 64% → 95%**: the main SDP could in fact prove almost all of the contracting parts single-handedly.
- **"Prey gained by raising degree" +54 → +4**: the higher degrees' unique contribution wasn't a lavish 54 but a modest 4.

The flashy "proving power grows hierarchically with degree" picture was a castle on sand, built by a cheating calculator.

![Diagram of the illusion collapsing on calculator swap (reprise)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_en.svg)

— A pause here. You'd think it ends at "ouch, the boast collapsed," but there's one more twist. —

---

## Act 4: The way the illusion broke is interesting — over-inflated, and under-stated

Usually "convenient numbers collapse" just means everything shrinks and that's it. But this calculator's cheating ran **both ways**. The very same single kind of error — "couldn't find it" — can inflate or deflate appearances, depending on **what you are measuring**.

- **In one place, "over-inflated":** the dropped balls were scattered across degree 4 and degree 6, creating the impression that "each net has its own unique prey." That was the "rich hierarchy" — fancier than reality.
- **In another, "under-stated":** in a larger check (3270 parts), the calculator dropped wins the main SDP was rightfully owed, and **under-estimated** its strength.

The under-statement is the punch line. The main SDP looked "+254 parts stronger" than a naive method (a simple yardstick called 2-norm). Re-measured with the accurate calculator, it was really "**+692 parts stronger**." SDP was **far better** than we thought.

Why did the gap widen so much? Because the naive 2-norm verdict is computable directly, no calculator needed (= immune to the cheating), while only the SDP verdict passed through the cheating calculator. Picture a footrace where only the favorite runs with sandbags on his ankles. Take the sandbags off, and the true gap in ability shows itself.

To be careful about where the numbers come from: the cheating calculator SCS had dropped 53 cases that were "actually provable." The accurate calculator CLARABEL **recovered 42–43** of them. And of the few that remained, **6 were "dangerous parts" deliberately and correctly rejected** — not misses but **correct refusals**. These 6 are exactly the type that behaves on an ordinary run yet breaks loose under the worst-case ordering — the living example of why, back in Act 1, we said observation alone isn't enough. At every rung of the inspection ladder, "unsound certificates that passed a bad part" were zero.

So this episode is not a story of a **loss** where a boast collapses.

> **The illusory hierarchy vanished, but the main verifier (SDP) turned out to be even stronger than before.**

The single unified truth: **"the main SDP verifier can prove about 95% of the contracting parts."** Simple, and strong.

By the way, "doesn't this risk waving through a runaway part?" — no need to worry. Inspection errors come in two kinds. At airport security: stopping a safe bag as "suspicious" (inconvenient, but no accident), versus letting a dangerous item through (catastrophe). This calculator's cheating was strictly the former — the "**can't find a certificate (false negative)**" kind, never the "**OK a bad part (false admit)**" kind. On top of that, two independent lines of cross-checking — re-verifying each issued certificate with a different computation, and actually exercising combinations of the parts while hunting for runaway counterexamples — confirmed "zero false admits observed." It was cheating that **fails to the safe side**, so trust in the verifier itself didn't collapse.

---

## Act 5: How did we catch it ourselves? — multi-perspective adversarial review

Here's the meta highlight. This trap is **structurally invisible to ordinary checks**.

A common self-check is "margin-sweep" (a red team that nudges thresholds and margins to test robustness): tighten the cutoff a little, loosen it a little, and see whether the conclusion flips. Normally a dependable check. Here it was powerless — because every computation under every nudged condition was **still done by the same cheating calculator**. Stand on a broken bathroom scale, shift your stance, hold a bag, re-measure thirty times: nothing will ever reveal that the scale itself is broken, because everything you compare shares the same lie. To expose a lie, you need an **outside**.

Two things were decisive — both ways of bringing in an outside:

1. **Swap the calculator (SOLVER-SWAP):** have two calculators of different pedigree, SCS and CLARABEL, solve the same problems and compare answers. Only when you step onto a second scale do you notice "huh, the numbers differ."
2. **Review adversarially from multiple perspectives (pair-review):** hand another AI (Codex) plus six skeptic agents the assignment "break this conclusion." The point is that they don't offer impressions — they **read the real code and independently recompute the numbers**, genuinely attacking: "your boast — that's a lie, right?"

The review raised five findings (F1–F5). The representative ones:

- **F1:** when the solver field was empty (""), there was a hole that slipped past the safety guard and quietly fell back to the cheating calculator (SCS). In programming, an empty string tends to be treated the same as "not filled in," so the fail-closed guard — "if the accurate calculator isn't available, refuse" — read it as "no preference → default SCS is fine." The same quiet horror as a medical questionnaire treating a blank allergy field as "no allergies." → **Plugged, with a regression test (an automated don't-let-this-happen-again test) added.**
- **F2:** the "absolutely safe" phrasing was too strong → honestly weakened to "**zero false admits observed**." Say only as much as the checks actually support: everything was correct *within the range we examined*.
- **F3:** the logic of one claim was **backwards to begin with** — a check had been described as the "more lenient" direction when it is actually the "stricter" one → corrected (see the full version).

The result: **zero findings overturned the central conclusion.** What the review did was "trim three overclaims and plug one dangerous hole." Honestly pulling your claims back to the line you can defend from any direction — like shrinking a castle wall to the perimeter you can actually hold — far from collapsing, the thesis became **sturdier**.

![Diagram of the honest-disclosure loop that keeps doubting its own conclusion](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_honest_loop_en.svg)

### Bonus: a strong verifier improves evolution itself

"So what do we gain by wiring this accurate verifier into the evolution loop?" — the natural question, and the numbers answer it.

Safety first. Evolving without the verifier, **17–20%** of the admitted offspring quietly drift toward the runaway side — generation after generation, risky children keep slipping in. Put the main SDP verifier at the gate, and **zero divergent offspring get through**.

The fun part: it doesn't just get safer — **the ceiling of evolution rises too**. With a naive verifier (inf-norm) as the gatekeeper, the reachable fitness plateaued at **about 0.41**; with the main SDP verifier it reached **about 0.86**. The probability of that gap arising by sheer luck is about 3 in 100,000 (p = 3.1e-5) — not a fluke.

Why does a stronger gatekeeper raise the ceiling? Because a weak gatekeeper doesn't just reject dangerous parts — it also **wrongly rejects masses of genuinely safe parts as "unprovable"** (indeed, on the Act 2 ladder the naive ruler could certify only 88 of 300, versus 286 for SDP). Under a gatekeeper prone to false accusations, evolution can only try timid designs. Under one that recognizes safe as safe, evolution can confidently explore bolder designs. **The stronger the gatekeeper, the higher the ceiling of safely reachable intelligence** — verification accuracy doesn't just buy safety; it lifts the very payoff of evolution.

---

## Limits, stated honestly (honest disclosure)

Writing only the good parts goes against the FullSense way, so here are the limits as-is.

- **Making the certificate fancier doesn't always make it stronger.** Intuition says "more freedom to bend the ruler can only help," but in reality raising the degree can return a **looser (weaker) bound**. If you want the tightest estimate, you must lay the results out across degrees and take the best one — there is no clean single staircase. "Raise the degree and march straight to the strongest" is **false**.
- The computation that gives exact answers is **NP-hard** (a problem class believed to blow up in computing time, for every known method, as the size grows). Of the remaining unproven parts, an even fancier certificate (degree 8) closed 4 more, and an exact bracketing computation closed 2 of those — but the last ~2 parts right at the boundary stay **open** within CPU range. A limit that doesn't close cleanly — and we say so honestly.
- All results are for "small parts (n=2 — two numbers of state), CPU, this pool." Safety is "**zero false admits observed**," not "mathematically absolute" (there is a separate machine-checked rigorous proof, but it's treated as an add-on option).
- This is about "**how to build a correct verifier**," not a claim that "evolved AIs are broadly useful."

---

## So, what did we actually learn?

In one line:

> **The proud "rich report card" was an illusion built by a cheating calculator. Swap in an accurate calculator and the illusion collapses — and the main verifier turns out to be even stronger than before.**

And the thing I most want to convey today:

> **A result that "goes too well" is not a win; it's an alarm.**
> If the numbers are too good, suspect the calculator (solver) before you believe them. And a self-check that merely nudges inside the same tool is blind to the trap. **Swapping the tool** and **attacking adversarially from another perspective** are what break the illusion.

More than any single number, please take home the **order of operations**. "Get a good result → celebrate → check just in case" makes the check soft, every time. "Install the doubting machinery first → get a good result → the machinery doubts it for you." Because we set up the machinery to honestly doubt ourselves first, we didn't stop at premature joy and reached solid ground — that was the kind of day it was.

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

在名为 **llcore** 的研究基座里，我们像培育生物一样，一点点改造小型 AI 的"大脑部件"。做法是经典的遗传算法，粗略说就是"造一大批候选 → 留下成绩好的 → 稍微改一改再试"，反复循环——和培育更甜的番茄是同一个道理。而且带着严格约束：仅用 CPU、只在自己的电脑里、零成本。

进化出的部件质量参差不齐。麻烦的是会"失控"的部件。这里说的部件，是"把状态(一组内部数字)一步一步更新下去的小计算装置"，输出会变成下一步的输入，是个不断转圈的回路。在这种回路里，只要每转一圈"放大"哪怕赢过一丝丝，数字就会滚雪球。和麦克风离音箱太近时"嗡——"的啸叫是同一个结构：麦克风拾取音箱的声音，放大后再从音箱播出，又被麦克风拾取……如此往复，一点细响瞬间变成轰鸣。这就是它的计算版——像油门被卡死的汽车。

所以需要一个**检查器 (verifier)**，逐个检查进化出的部件并判断：

> "这个部件在重复时会保持平静(逐渐稳定)，而不是失控吗？"

把坏的挡在门外。研究问题很简单：**"那么，正确的检查器该怎么造？"**

你可能会想："实际跑一跑、看一看不就行了？"但观察只能说"**到目前为止**很乖"。实际上(后文会出现)真的存在这样的部件：平常的跑法下很安分，可一旦碰上最坏的条件(最坏的执行顺序)才开始撒野。通过试车是不够的。我们要的是**覆盖未来的保证**——"不管之后怎么发展都不会失控"——这只能靠数学给出，观察给不了。

我们把"逐渐稳定"的性质称为**收缩 (contraction)**：每走一步，到终点的距离都必须缩小，像碗里的玻璃球最终一定停在碗底。既然"每一步都必缩"，那就根本胀不起来——只要证明了收缩，失控的担心就消失了。如果能开出一张"这个部件确实收缩"的**数学证书**，就能放心通过。就像建筑的结构计算书：不是"摇了摇没倒"，而是"经计算，在这个范围内的任何摇晃下都绝不会倒"的文件。

证书的真身是一个叫 P 的**矩阵**——掰开揉碎说，是一把**歪尺子**。用普通的直尺量，看不出在缩的运动，换一把按这个部件定制的、特意弯过的尺子重新量，可能就会发现"其实每一步都在乖乖缩短"。只要能说"用这把歪尺子 P 来量，任何一步都必然缩短距离"，这一句话本身就是收缩的证书。

而寻找这把趁手的尺子 P 的主力方法，就是 **SDP**——一种**凸优化**。凸优化指"在碗形地形里找最低点"那一类问题：因为是碗形，不会被半路的小坑(假谷底)骗住，所以找到的答案可以直接当成保证来用——证书搜索之所以成立，靠的正是这个性质。

顺带一提，当初我们也期待"解逻辑谜题的高级求解器(SMT/Z3)"能成为检查的另一根支柱。但一查，Z3 在这个基座上是**装饰品**。因为我们问 Z3 的那些判定，其实都能归结为**闭式**——用加减乘除直接算出来的式子。实测也是：分别对 2 万件和 3270 件进行比对，Z3 的判定与闭式计算**完全一致**(零分歧)。等于给"计算器一按就出答案"的问题请了位逻辑谜题大师——大师没出错，但也什么都没加上。真正抓住收缩本质的，终究是 **SDP 的证书**。这就是底层认知。

---

## 第二幕：自豪的成绩单出现了——可它太好了

我们测了检查器的实力。关键概念是**次数 (degree)**。刚才把证书比作"歪尺子"，次数就是这把尺子的"可弯曲程度"。次数越高，允许的尺子形状越复杂 = 能写出越花哨的证书 = 按道理，能抓到的部件应该越多。

于是我们做了一个**逐级阶梯**："提高次数后，能抓到的部件怎么增加？"——像一本捕鱼日志：网眼越织越细，数一数各张网能捞到几条。

最初的统计是这样的：

- 只被更花哨证书(次数4)抓到的部件：23个
- 只被更花哨证书(次数6)抓到的部件：13个
- 两者都抓到的部件：18个

读法是：只有次数4的网才捞得到的鱼有23条，只有次数6的网才捞得到的鱼有13条，两张网都能捞到的有18条。也就是说，每张网似乎都有**只属于自己的鱼**。

对研究者来说这很"香"。它看起来意味着**每提高一档次数就解锁新猎物**——"证明能力有丰富的层级"。"每个更高的次数都有自己独有的存在价值，所以每张网都值得留着"——每加一件新工具就出一批新成果的故事，是论文里最好看的一张图。

……但这里 [[honest disclosure 纪律]] 启动了。FullSense 研究有铁律：

> **若结果异常地好，在觉得自己赢了之前，务必怀疑其内部构成。**

人这种生物，对合乎期待的结果不会回头细看，只对令人失望的结果拼命找原因。也就是说，放着不管的话，恰恰是"合自己心意的错误"最容易溜过检查、活下来。正因为明白这一点，才提前定下反向的规则——结果**越好越要怀疑**。成绩单"太丰富、太方便"，于是没有庆祝，而是去怀疑。

---

## 第三幕：元凶是计算器(这是核心)

寻找证书(歪尺子 P)的计算是一类标准化的数学问题，所以幕后甩给一个专用 **solver**("计算器")处理——就像后厨把熬高汤交给专用机器，这本身很正常。问题出在这台计算器的**性格**上。

默认那台名叫 **SCS**，信条是"粗略但快"：用轻量的反复迭代逐步逼近答案，到"差不多对"就收工。平时这足够了。但它有弱点：

> **在"答案是否勉强存在"的边界附近，SCS 会作弊并报告"没找到"。**

部件分两种：证书"绰绰有余地存在"的，和"勉勉强强才存在"的。宽裕的案子哪台计算器都能答对。可在边界案子上——好比一辆只比车位窄几厘米、勉强停得进去的车——到"差不多"就收工的计算器会回答"停不进去(没找到)"。明明证书确实存在，它却交了**假报告(假阴性)**："没找到。"

更糟的是，计算器自己也半知半觉，悄悄闪出警告："Solution may be inaccurate(此解可能不准确)。"就像体重秤角落里标着"参考值"，我们却只抄数字。

于是我们换上 **CLARABEL**，一台准确但稍慢的**内点法**计算器。内点法在答案存在区域的"内部"小心行走、走向高精度的答案，所以边界案子也扛得住。心算高手(SCS)对上认真列竖式验算的人(CLARABEL)。

最关键的是实验的设计：**同一批部件、同样的问题，只换计算器**。和理科课的对照实验一样——只改一个变量，结果一变，就能咬定"原因就是它"。结果：

| 统计项 | SCS(作弊计算器·假) | CLARABEL(准确计算器·真) |
|---|---|---|
| 仅次数4 / 仅次数6 / 两者 | 23 / 13 / 18 | 0 / 1 / 54 |
| 结构解读 | 零散(看似丰富的层级) | 干净的嵌套(其实简单) |
| "未证明剩余数" | 53个 | 10个 |
| 主力 SDP 覆盖率 | 64%(300个中193个) | **95%(300个中286个)** |
| "提高次数新增猎物" | +54(豪华！) | +4(朴素…) |

自豪的"丰富层级"，**整个是幻象**。

把表逐行读开：

- **"仅次数4"从 23 → 0**：正确计算后，"只有次数4的网才捞得到的鱼"一条也不存在。次数4抓到的，次数6全都抓得到——像俄罗斯套娃，大网的捕获名单把小网的名单整个包住，干净的**嵌套**。
- **"未证明剩余数"从 53 → 10**："证明不了"那一大堆，多半不是部件的问题，而是**计算器掉的球**。
- **覆盖率 64% → 95%**：主力 SDP 其实凭一己之力就能证明绝大多数收缩部件。
- **"提高次数新增猎物"+54 → +4**：高次数的独有功劳不是豪华的54，而是朴素的4。

"证明能力随次数分层增长"那张好看的图，是作弊计算器搭起的沙上楼阁。

![换掉计算器后幻象崩塌的示意图(重出)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_zh.svg)

— 在此小憩。你以为故事到"哎呀，吹的牛崩了"就结束，其实还有一个转折。 —

---

## 第四幕：幻象崩塌的方式很有意思——夸大，和低估

通常"方便的数字崩塌"就是全部缩水、到此为止。但这台计算器的作弊是**双向**的。同样一种错误——"没找到"——取决于**你在测什么**，既可能把表象吹大，也可能把表象削小。

- **一处"夸大"：** 掉的球零散地落在次数4和次数6两边，造成"每张网都有自己独有猎物"的假象。那就是"丰富层级"——比现实更花哨。
- **另一处"低估"：** 在更大规模的检查(3270个部件)里，计算器掉了主力 SDP 本该到手的战果，**低估**了它的强度。

这个低估是包袱所在。主力 SDP 相对朴素方法(一个叫 2-norm 的简单标尺)看起来"强 +254 个部件"。用准确计算器重测，实际是"**强 +692 个部件**"。SDP 比我们想的**强得多**。

差距为什么拉开这么多？因为朴素的 2-norm 判定不需要计算器、可以直接算出来(= 不受作弊影响)，而只有 SDP 的判定要经过那台作弊计算器。打个比方：一场赛跑里，只有夺冠热门被绑着沙袋跑。解开沙袋，真实的实力差就原样显现。

为稳妥起见交代数字的来历：作弊计算器 SCS 把53件"其实能证明"的案子掉在了地上。准确计算器 CLARABEL **回收**了其中42〜43件。剩下的少数里，仔细一看，**有6件是故意且正确弹掉的"危险部件"**——不是失误，而是**正确的拒绝**。这6件正是那种部件：平常的跑法下安分，最坏顺序下才开始撒野——第一幕里说"只靠观察不够"，活生生的例子就是它们。在检查的每一级上，"放走坏部件的不健全证书"都为零。

所以这桩事并不是吹牛崩塌的**失败**故事。

> **虚幻的层级消失了，但主力检查器(SDP)反而比之前更强了。**

统一的一个真相：**"主力 SDP 检查器能证明约95%的收缩部件。"** 简单，而强。

顺便说，"那会不会不小心放过一个失控部件？"——不必担心。检查的失误有两种。拿机场安检打比方：把安全的行李拦下来当"可疑"(不方便，但不出事故)，和把危险品放过去(大祸)。这台计算器的作弊只属于前者——"**找不到证书(假阴性)**"那一类，绝不是"**把坏部件判为 OK(假放行)**"那一类。此外还有两条独立的对账线：用另一种算法把每张签发的证书重新核验一遍，以及实际组合运行部件、搜寻失控的反例——都确认了"观测到的假放行为零"。这是**偏向安全侧**的作弊，所以对检查器本身的信任并未崩塌。

---

## 第五幕：我们怎么自己抓到的？——多视角对抗式评审

这是元层面的看点。这个陷阱**对普通检查在结构上是不可见的**。

常见的自检是"margin-sweep"(微调阈值与余量、测试稳健性的红队)：把判定的门槛收紧一点、放松一点，看结论会不会翻转。平时这是可靠的检查。这次却无能为力——因为每个微调条件下的计算，**仍然全部由同一台作弊计算器来做**。站在一台坏掉的体重秤上，换站姿、拎包、重测三十次，也永远看不出秤本身坏了——因为你比较的一切都共享同一个谎言。要戳穿谎言，需要**外部**。

起决定作用的有两点——都是引入"外部"的手法：

1. **换计算器(SOLVER-SWAP)：** 让出身不同的两台计算器 SCS 和 CLARABEL 解同样的问题并对照答案。踏上第二台秤，才第一次发现"咦，数字不一样"。
2. **从多个视角对抗式评审(pair-review)：** 给另一个 AI(Codex)加上六个怀疑者智能体布置作业："把这个结论搞垮。"重点在于他们不是发表感想，而是**读真实代码、独立重算数字**，认真进攻："你吹的牛，是假的吧？"

这次评审提出五条(F1–F5)。代表性的几条：

- **F1：** 当 solver 字段为空("")时，存在一个绕过安全护栏、悄悄退回作弊计算器(SCS)的漏洞。在编程世界里，空字符串往往被当成"没填写"，于是"没有准确计算器就拒绝"的安全设计(fail-closed)把它解读成"没有偏好 → 用默认的 SCS 吧"。和问诊单上过敏栏空白就被当成"无过敏"是同一种后怕 → **已堵上，并加了回归测试(防复发的自动测试)**。
- **F2：** "绝对安全"的措辞太强 → 诚实地弱化为"**观测到的假放行为零**"。只说检查真正撑得住的话：在我们查过的范围内全部正确。
- **F3：** 某条主张的逻辑**本就方向相反**——一项检查被描述成"更宽松"的方向，实际却是"更严格"的方向，是个方向搞反 → 已更正(详见完整版)。

结果：**没有任何一条推翻中心结论。** 评审做的是"削去三处过度主张、堵上一个危险漏洞"。把主张诚实地退到"从任何方向进攻都守得住"的那条线——就像把城墙收缩到真正守得住的范围再加固——论点非但没崩，反而**更加结实**。

![不断怀疑自身结论的 honest-disclosure 循环图](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_honest_loop_zh.svg)

### 彩蛋：强的检查器，会让进化本身变好

"那么，把这台准确的检查器装进进化循环里，到底有什么好处？"——这个理所当然的疑问，也有数字作答。

先看安全。不装检查器就进化，被放行的后代里有 **17〜20%** 会悄悄向失控一侧漂移——一代一代地，危险的孩子持续混进来。把主力 SDP 检查器放在门口当门卫，**失控的孩子一个也过不去**。

更有意思的是，不止变安全，**进化的上限也抬高了**。用朴素检查器(inf-norm)当门卫，能达到的聪明程度(fitness)在**约0.41**就封顶；换主力 SDP 检查器后伸到了**约0.86**。这个差距纯靠运气出现的概率约为十万分之三(p = 3.1e-5)——不是侥幸。

为什么门卫越强、上限越高？因为弱的门卫不只弹掉危险部件，还会**把大量其实安全的部件误判为"无法证明"而弹掉**(事实上，在第二幕的成绩阶梯上，朴素的尺子只能证明300个中的88个，SDP 能证明286个)。在冤案频出的门卫手下，进化只敢尝试平庸的设计；在能把"安全"认作安全的门卫手下，进化才能放心探索更大胆的设计。**门卫越强，安全可达的聪明天花板就开得越高**——检查的精度不只买来安全，还托起了进化的成果本身。

---

## 诚实交代的局限 (honest disclosure)

只写好的部分有违 FullSense 的风格，所以局限也原样公开。

- **把证书弄得更花哨，未必更强。** 直觉上"尺子可弯的自由度越大只会更强"，可现实是提高次数可能返回**更松(更弱)的界**。想要最紧的估计，只能把各个次数的结果摆在一起、挑最好的那个——并不存在一条干净的单向阶梯。"提高次数就一路走到最强"是**假的**。
- 给出精确答案的计算是 **NP 困难**(被认为随着问题变大、已知任何方法的计算时间都会爆炸的难题类别)。剩下的未证明部件里，更花哨的证明(次数8)又关上了4个，精确计算的两面夹逼又关上了其中2个；但恰在边界上的最后约2个部件，在 CPU 范围内**仍未闭合**。一个无法干净闭合的局限——我们如实说出。
- 全部结果都是"小部件(n=2，状态只有两个数字)、CPU、这一批"的情形。安全性是"**观测到的假放行为零**"，并非"数学上绝对"(另有一份机器校验的严格证明，但作为附加选项处理)。
- 这讲的是"**如何造一个正确的检查器**"，不是声称"进化出的 AI 普遍有用"。

---

## 那么，到底学到了什么？

一句话：

> **自豪的"丰富成绩单"是作弊计算器造的幻象。换上准确的计算器，幻象崩塌——而主力检查器反而比之前更强。**

以及今天最想传达的：

> **"太顺的结果"不是胜利，而是警报。**
> 数字太好时，先怀疑计算器(solver)，再选择相信。而只在同一工具内微调的自检，对陷阱是盲的。**换工具**与**从另一视角对抗式攻击**，才是戳破幻象的决定手。

比起任何数字，请把**顺序**带回家。"出好结果 → 高兴 → 顺便确认一下"——这样的确认注定是松的。"先装好怀疑的机制 → 出好结果 → 机制替你怀疑"。正因为我们先架好了诚实怀疑自己的机制，才没有止步于过早的喜悦、抵达了坚实的地面——就是这样的一天。

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

**llcore** 라는 연구 기반에서 우리는 작은 AI의 "두뇌 부품"을 생물의 진화처럼 조금씩 고쳐 만듭니다. 방법은 고전적인 유전 알고리즘으로, 대략 "후보를 잔뜩 만든다 → 성적 좋은 것을 남긴다 → 조금 바꿔서 또 시험한다"의 반복 —— 더 달콤한 토마토를 노리는 품종 개량과 같은 이치입니다. 게다가 엄격한 제약과 함께: CPU만, 내 PC 안에서만, 비용 제로.

진화시킨 부품은 품질이 들쭉날쭉합니다. 골치 아픈 건 "폭주하는" 부품. 여기서 부품이란 "상태(내부 숫자 묶음)를 한 걸음씩 갱신해 가는 작은 계산 장치"로, 출력이 다음 입력으로 되돌아오는, 빙글빙글 도는 구조입니다. 이런 반복 구조에서는 한 바퀴마다 "증폭"이 아주 조금이라도 이기면 숫자가 눈덩이처럼 불어납니다. 마이크와 스피커가 너무 가까우면 "삐——" 하고 하울링이 나는 것과 같은 구도 —— 마이크가 스피커 소리를 줍고, 증폭돼 다시 스피커로 나오고, 그걸 또 마이크가 줍고…의 반복으로 작은 소리가 순식간에 굉음이 되는, 그것의 계산 버전입니다. 말하자면 액셀이 고착돼 멈추지 않는 자동차 같은 부품이죠.

그래서 **검사기 (verifier)** 가 필요합니다. 진화한 부품을 하나씩 조사해 판정합니다:

> "이 부품은 반복해도 차분히 (오히려 안정되게) 가라앉는가, 폭주하지 않는가?"

나쁜 놈은 문전박대합니다. 연구 질문은 단순합니다: **"그럼 올바른 검사기는 어떻게 만드나?"**

"실제로 돌려 보고 지켜보면 되지 않나?"라고 생각할 수 있습니다. 하지만 관찰로 말할 수 있는 건 "**지금까지는** 얌전했다"뿐. 실제로 (뒤에 나옵니다만) 평소 돌리는 방식에서는 얌전한데, 최악의 조건(돌아가는 순서)을 만났을 때만 날뛰기 시작하는 부품이 정말로 존재합니다. 시운전 합격으로는 부족합니다. 원하는 것은 "앞으로 어떻게 굴러가도 폭주하지 않는다"는 **미래까지 커버하는 보증**이고, 그것은 관찰이 아니라 수학에서만 나옵니다.

그 "가라앉는" 성질을 연구에서는 **수축 (contraction)** 이라 부릅니다: 한 걸음마다 목적지까지의 거리가 반드시 줄어드는, 그릇 속 구슬이 결국 바닥에서 멈추는 이미지. "매번 반드시 줄어든다"면 불어날 도리가 없으니, 수축만 증명되면 폭주 걱정은 사라집니다. 그리고 "이 부품은 확실히 수축한다"는 **수학적 증명서**를 발행할 수 있으면 안심하고 통과시킵니다. 건물로 치면 구조계산서와 같습니다 —— "흔들어 봤는데 안 무너졌다"가 아니라 "이 범위의 흔들림이라면 절대 무너지지 않는다고 계산으로 보인 서류"죠.

증명서의 정체는 P라는 **행렬** —— 쉽게 말해 "**비뚤어진 자**"입니다. 곧은 보통 자로 재면 줄어드는 걸로 보이지 않는 움직임도, 그 부품에 맞춰 일부러 휘게 만든 특제 자로 다시 재면 "한 걸음마다 제대로 줄고 있다"고 드러나는 경우가 있습니다. "이 비뚤어진 자 P로 재면 어떤 한 걸음도 반드시 거리가 줄어든다"고 말할 수 있으면, 그 한 문장이 그대로 수축의 증명서가 됩니다.

그리고 이 편리한 자 P를 찾아오는 계산 방법의 본명이 **SDP** 라는 **볼록 최적화** 기법. 볼록 최적화란 "사발 모양 지형에서 가장 낮은 점을 찾는" 유형의 문제로, 사발 모양이니 도중의 작은 웅덩이(가짜 골짜기)에 속을 일이 없습니다. 그래서 "찾아낸 답"을 그대로 "보증"으로 쓸 수 있고 —— 증명서 탐색에 쓸 수 있는 것도 이 성질 덕분입니다.

참고로, 당초에는 "논리 퍼즐을 푸는 고급 솔버 (SMT/Z3)"도 검사의 기둥이 될까 기대했습니다. 그런데 조사해 보니 이 기반에서의 Z3는 **장식**이었습니다. Z3에 묻던 판정이 사실은 **닫힌 식** —— 사칙연산으로 직접 계산해 쓸 수 있는 식 —— 으로 귀착되는 것이었기 때문입니다. 실측으로도 2만 건·3270건을 대조해 Z3의 판정은 닫힌 식 계산과 **완전히 일치** (어긋남 제로). 계산기 한 번이면 답이 나오는 문제에 논리 퍼즐의 달인을 모셔 온 셈입니다. 달인은 틀리지 않았지만, 아무것도 보태지도 않았다. 수축의 본질을 잡고 있던 건 **역시 SDP의 증명서** 쪽이었다 —— 이것이 바탕이 되는 이해입니다.

---

## 제2막: 자랑스러운 성적표가 나왔다 —— 그런데 너무 좋았다

검사기의 실력을 쟀습니다. 열쇠가 되는 개념이 **차수**입니다. 방금 증명서를 "비뚤어진 자"라고 했는데, 차수란 그 자의 "휘게 할 수 있는 자유도"입니다. 차수를 올릴수록 더 복잡한 모양의 자까지 허용된다 = 더 공들인 증명서를 쓸 수 있다 = 이론상으로는, 잡을 수 있는 부품이 늘어날 것입니다.

그래서 "차수를 올리면 잡히는 부품이 어떻게 늘어나나"를 재는 **단계별 사다리**를 만들었습니다. 그물코를 점점 촘촘히 짜면서, 그물마다 몇 마리 잡히는지 세어 가는 조업 일지 같은 것이죠.

처음 집계는 이런 느낌이었습니다:

- 더 공들인 증명서(차수4)로만 잡힌 부품: 23개
- 더더욱 공들인 증명서(차수6)로만 잡힌 부품: 13개
- 둘 다로 잡힌 부품: 18개

읽는 법은 이렇습니다: 차수4 그물로만 잡히는 물고기 23마리, 차수6 그물로만 잡히는 물고기 13마리, 둘 다에 잡히는 게 18마리. 즉 그물마다 **그 그물로만 잡히는 물고기**가 있다는 해석이 됩니다.

연구자에게 이건 "맛있는" 결과입니다. **차수를 올릴 때마다 새 사냥감이 늘어난다** = "증명 능력에 풍부한 계층이 있다"처럼 보이니까요. "높은 차수마다 고유한 존재 가치가 있다, 그러니 모든 그물을 갖춰 둘 의미가 있다" —— 새 도구를 더할 때마다 새 성과가 나오는 이야기는, 논문으로서 최고로 돋보이는 그림입니다.

…그런데 여기서 [[honest disclosure 규율]]이 발동합니다. FullSense 연구에는 철칙이 있습니다:

> **비정상적으로 좋은 결과가 나오면, 이겼다고 느끼기 전에 반드시 내역을 의심하라.**

인간은 기대에 맞는 결과는 다시 들여다보지 않고, 기대를 벗어난 결과에만 필사적으로 원인을 찾는 생물입니다. 즉 내버려 두면, 하필 "내 입맛에 맞는 오류"만 검사를 빠져나가 살아남는다는 것. 그걸 알기에 일부러 반대 방향의 규칙 —— 결과가 **좋을수록** 의심한다 —— 을 먼저 정해 둔 것입니다. 성적표가 "너무 풍부, 너무 편리"했기에 순순히 기뻐하지 않고 의심에 나섰습니다.

---

## 제3막: 범인은 계산기였다 (여기가 핵심)

증명서(비뚤어진 자 P)를 찾는 계산은 정형화된 수학 문제라서, 뒤에서 전용 **solver** ("계산기")에 통째로 맡깁니다. 주방이 육수 내기를 전용 기계에 맡기는 것과 같아, 그 자체는 평범한 일입니다. 문제는 그 계산기의 **성격**이었습니다.

기본 계산기 이름은 **SCS**. "대충 빠르게"가 신조인 타입으로, 가벼운 반복 계산으로 답에 다가가다 "대충 맞다" 싶으면 거기서 끊습니다. 평소엔 그걸로 충분. 그런데 약점이 있었습니다:

> **답이 가까스로 존재하는지 마는지의 "경계" 부근에서, SCS는 속임수를 써서 "못 찾았습니다"라고 말해버린다.**

부품에는 "증명서가 여유 있게 존재하는 것"과 "간신히 존재하는 것"이 있습니다. 여유 있는 안건이면 어떤 계산기든 정답을 냅니다. 하지만 아슬아슬한 안건 —— 주차 칸에 몇 센티미터 여유로 간신히 들어가는 차 같은 케이스 —— 에서는 "대충"에서 끊는 계산기가 "안 들어갑니다(못 찾았습니다)"라고 답해 버립니다. 사실은 증명서가 분명히 존재하는데도 **거짓 보고(거짓 음성)** 를 한 겁니다: "아니요, 못 찾았어요."

더 고약하게도, 계산기 자신도 어렴풋이 알아서 "Solution may be inaccurate(이 답, 부정확할 수 있음)"라는 경고를 작게 띄우고 있었습니다. 체중계 구석에 "참고치"라고 떠 있는데 숫자만 읽어 적던 셈입니다.

그래서 정확하지만 조금 느린 **내점법** 계산기 **CLARABEL** 로 바꿔봤습니다. 내점법은 답이 존재하는 영역의 "안쪽"을 신중히 걸어 고정밀 답에 도달하는 타입이라, 경계 아슬아슬한 안건에도 강합니다. 암산의 달인(SCS) 대(對) 세로셈으로 꼼꼼히 검산하는 사람(CLARABEL)이죠.

여기서 중요한 건 실험의 짜임새입니다. **같은 부품 풀, 같은 문제, 계산기만 스위치**. 과학 시간의 대조 실험과 같아서, 바꾼 것이 하나뿐이면 결과가 달라졌을 때 "달라진 원인은 그것"이라고 단언할 수 있습니다. 그러자 ——

| 집계 항목 | SCS (속이는 계산기·거짓) | CLARABEL (정확한 계산기·참) |
|---|---|---|
| 차수4만 / 차수6만 / 둘 다 | 23 / 13 / 18 | 0 / 1 / 54 |
| 구조 해석 | 제각각 (풍부한 계층처럼 보임) | 깔끔한 중첩 (실은 단순) |
| "미증명으로 남은 수" | 53개 | 10개 |
| 주력 SDP 커버율 | 64% (300개 중 193개) | **95% (300개 중 286개)** |
| "차수를 올려 늘어난 사냥감" | +54 (호화!) | +4 (수수…) |

자랑하던 "풍부한 계층"은 **통째로 환상**이었습니다.

표를 한 줄씩 풀어 읽으면:

- **"차수4만"이 23 → 0**: 정확히 계산하니 "차수4 그물로만 잡히는 물고기"는 한 마리도 없었다. 차수4에서 잡히는 것은 차수6에서도 전부 잡힌다 —— 마트료시카 인형처럼, 큰 그물의 포획 명단이 작은 그물의 명단을 통째로 품는 깔끔한 **중첩**.
- **"미증명으로 남은 수"가 53 → 10**: "증명 못 했습니다" 더미의 태반은 부품 탓이 아니라 **계산기가 흘린 공**이었다.
- **커버율 64% → 95%**: 주력 SDP는 사실 수축하는 부품 대부분을 혼자 힘으로 증명하고 있었다.
- **"차수를 올려 늘어난 사냥감" +54 → +4**: 높은 차수의 고유한 공로는 호화로운 54가 아니라 소박한 4.

"증명 능력이 차수에 따라 계층적으로 늘어난다"는 멋진 그림은, 속이는 계산기가 쌓아 올린 모래 위 누각이었습니다.

![계산기를 바꾸면 환상이 무너지는 그림 (재게재)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_solver_swap_ko.svg)

— 여기서 한숨 돌립시다. "당했다, 자랑이 무너졌다"로 끝날 줄 알았겠지만, 이야기엔 한 번의 반전이 더 있습니다. —

---

## 제4막: 환상이 무너지는 방식이 흥미롭다 —— 과장, 그리고 과소평가

보통 "편리한 숫자가 무너진다"면 전부 초라해지고 끝입니다. 하지만 이번 계산기의 속임수는 **양방향**으로 걸려 있었습니다. 같은 한 종류의 실수 —— "못 찾았습니다" —— 라도 **무엇을 재고 있느냐**에 따라, 겉모습을 부풀릴 수도 깎을 수도 있는 겁니다.

- **한쪽은 "과장":** 흘린 공이 차수4와 차수6에 제각각 흩어진 탓에 "그물마다 고유한 사냥감이 있다"는 착시가 생겼다. 그것이 아까의 "풍부한 계층" —— 실태보다 호화롭게 보였다.
- **다른 쪽은 "과소평가":** 더 큰 검증(3270개 부품)에서는 주력 SDP가 마땅히 가져갈 전과를 흘려, 그 강함을 **과소평가**했다.

이 과소평가가 한 방입니다. 주력 SDP는 소박한 검사법(2-norm이라는 단순한 잣대)에 대해 "+254개만큼 강하다"로 보였습니다. 그런데 정확한 계산기로 다시 재니, 사실은 "**+692개만큼 강하다**". SDP는 생각보다 **훨씬 우수**했던 거죠.

왜 차이가 이렇게나 벌어졌을까. 소박한 2-norm 판정은 계산기 없이 직접 계산할 수 있어(= 속임수의 영향을 안 받음), 속이는 계산기를 거치는 건 SDP의 판정뿐이었기 때문입니다. 달리기 시합에 비유하면, 우승 후보만 발목에 모래주머니를 차고 뛰게 한 것. 모래주머니를 풀자 원래 실력 차가 그대로 드러난 이야기입니다.

혹시 몰라 숫자의 출처를 보충하면, 속이는 계산기 SCS는 "사실은 증명 가능"한 안건을 53건이나 흘리고 있었습니다. 정확한 계산기 CLARABEL은 그중 42〜43건을 **회수**. 남은 소수도 자세히 보면 **6건은 일부러 올바르게 튕겨낸 "위험한 부품"** 으로, 이건 실수가 아니라 **올바른 거부**입니다. 이 6건이 바로, 평소 돌리는 방식에서는 얌전한데 최악의 순서로 돌리면 날뛰는 타입의 부품 —— 제1막에서 "관찰만으로는 부족하다"고 한, 바로 그 실례였습니다. 어느 검사 단에서도 "나쁜 부품을 통과시킨 불건전한 증명서"는 제로였습니다.

그러니 이 사건은 자랑이 무너진 **패배**의 이야기가 아닙니다.

> **환상의 계층은 사라졌지만, 주력 검사기(SDP)는 오히려 전보다 강하다고 드러났다.**

통일된 하나의 진실: **"주력 SDP 검사기가 수축하는 부품의 약 95%를 증명할 수 있다."** 단순하고, 강합니다.

참고로 "그럼 폭주하는 부품을 실수로 통과시킬 위험은?" —— 걱정 없습니다. 검사의 실수에는 두 종류가 있습니다. 공항 수하물 검사로 치면, 안전한 짐을 "수상하다"며 세우는 것(불편하지만 사고는 안 남)과, 위험물을 그냥 통과시키는 것(대참사). 이번 계산기의 속임수는 전자뿐 —— "**증명서를 못 찾는(거짓 음성)**" 종류의 실수이지, "**나쁜 부품을 OK로 통과(거짓 허가)**" 하는 종류가 아닙니다. 게다가 발행된 증명서가 진짜인지 다른 계산 방식으로 한 번 더 확인하는 재검사와, 실제로 부품을 조합해 돌려 보며 폭주의 반례를 찾는 재검사 —— 독립된 두 계통의 답 맞추기로 "관측된 거짓 허가 0"을 확인했습니다. **안전한 쪽으로 넘어지는** 속임수였기에, 검사기에 대한 신뢰는 무너지지 않았습니다.

---

## 제5막: 어떻게 스스로 잡아냈나? —— 다시점 적대적 리뷰

여기가 메타적인 볼거리입니다. 이 함정은 **보통 검사에는 구조적으로 보이지 않습니다.**

흔한 자체 점검에 "margin-sweep"(판정 문턱과 여백을 조금씩 흔들어 강건성을 확인하는 레드팀)이 있습니다. 기준을 살짝 조이고 살짝 풀어 보며 결론이 휙 뒤집히지 않는지 확인하는, 평소라면 믿음직한 점검법이죠. 그런데 이번엔 무력했습니다. 흔든 조건에서의 계산도 **전부 같은 속이는 계산기가 하기** 때문입니다. 고장 난 체중계 위에서 자세를 바꾸고 짐을 들고 서른 번을 다시 재 봐야, 체중계 자체가 고장 났다는 사실은 1밀리미터도 보이지 않습니다 —— 비교하는 모든 것이 같은 거짓말을 공유하고 있으니까요. 거짓을 간파하려면 **바깥**이 필요합니다.

결정타는 두 가지. 둘 다 "바깥"을 끌어들이는 수입니다:

1. **계산기를 바꾼다 (SOLVER-SWAP):** 출신이 다른 두 대, SCS와 CLARABEL에게 같은 문제를 풀게 하고 답을 맞대어 본다. 두 번째 체중계에 올라서야 비로소 "어, 숫자가 다르네"를 알게 된다.
2. **여러 시점에서 적대적으로 리뷰한다 (pair-review):** 다른 AI(Codex)와 6체의 회의주의 에이전트에게 "이 결론을 부숴 봐라"는 숙제를 낸다. 중요한 건 그들이 감상을 말하는 게 아니라, **실제 코드를 읽고 숫자를 독립적으로 다시 계산해서** 반증을 시도한다는 점. "네 자랑, 거짓말이지?"라고 진심으로 공격하게 하는 겁니다.

이 리뷰에서 5건(F1–F5)이 나왔습니다. 대표적인 것만:

- **F1:** solver 항목이 비었을 때("") 안전장치를 빠져나가 슬그머니 속이는 계산기(SCS)로 되돌아가는 구멍이 있었다. 프로그래밍 세계에서 빈 문자열은 "미기입"과 같은 취급을 받기 쉬워서, "정확한 계산기가 없으면 거부하라"는 안전 설계(fail-closed)가 "지정 없음 → 기본값 SCS면 되겠지"로 해석해 버리는 샛길입니다. 문진표의 알레르기 칸이 공란이면 "없음"으로 처리되는, 그 서늘함 → **막고 회귀 테스트(재발 방지 자동 테스트) 추가**.
- **F2:** "절대 안전"이라는 표현이 너무 강했다 → "**관측된 거짓 허가 0**"으로 정직하게 약화. 점검이 실제로 받쳐 주는 데까지만 말한다: 조사한 범위에서는 전부 옳았다, 까지가 사실.
- **F3:** 어떤 주장의 논리가 **애초에 방향이 반대**였다 —— 한 점검을 "더 느슨한" 방향이라고 설명했는데 실제로는 "더 엄격한" 방향이었다는, 방향의 착오 → 정정(자세한 건 완전판).

결과: **중심 결론을 뒤집은 지적은 0건.** 리뷰가 한 일은 "과한 주장 셋을 깎고, 위험한 구멍 하나를 막은" 것. 주장의 선을 "어느 방향에서 공격당해도 지켜낼 수 있는 위치"까지 정직하게 물리는 것 —— 성벽을 지킬 수 있는 범위까지 줄여서 단단히 굳히는 것과 같아서, 논지는 무너지기는커녕 **오히려 더 단단해졌습니다**.

![자신의 결론을 계속 의심하는 honest-disclosure 루프 그림](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_35/qiita_35_honest_loop_ko.svg)

### 덤: 강한 검사기는 진화 자체를 좋게 만든다

"그래서 그 정확한 검사기를 진화 루프에 끼우면 뭐가 좋은데?"라는 당연한 의문에도 숫자로 답이 나와 있습니다.

먼저 안전. 검사기 없이 진화시키면 허가된 자식 중 **17〜20%** 가 슬금슬금 폭주 쪽으로 표류해 갑니다 —— 세대를 거듭할수록 위험한 자식이 조용히 섞여 들어오는 거죠. 주력 SDP 검사기를 문지기로 세우면 **폭주하는 자식은 한 마리도 통과하지 못합니다**.

게다가 재미있는 건, 그저 안전해질 뿐 아니라 **진화의 상한까지 올라간다**는 점. 소박한 검사기(inf-norm)를 문지기로 두면 도달 가능한 영리함(fitness)이 **약 0.41**에서 머리를 치는데, 주력 SDP 검사기에서는 **약 0.86**까지 뻗었습니다. 이 차이가 순전히 운으로 나올 확률은 약 10만분의 3 (p = 3.1e-5) —— 요행이 아닙니다.

왜 문지기를 강하게 하면 상한이 올라갈까. 약한 문지기는 위험한 부품을 튕겨낼 뿐 아니라, **사실은 안전한 부품까지 "증명 못 함"이라며 대량으로 튕겨내기** 때문입니다 (실제로 제2막의 성적 사다리에서 소박한 자가 증명할 수 있던 건 300개 중 88개, SDP는 286개). 억울한 판정이 잦은 문지기 밑에서 진화는 무난한 설계밖에 시도하지 못합니다. 안전한 것을 안전하다고 알아보는 문지기 밑에서라야, 진화는 더 대담한 설계까지 안심하고 시도할 수 있습니다. **강한 문지기일수록, 안전하게 도달할 수 있는 영리함의 천장을 높이 열어 준다** —— 검사의 정밀도는 안전만이 아니라 진화의 성과 자체를 끌어올리는 것입니다.

---

## 정직하게 밝히는 한계 (honest disclosure)

좋은 이야기만 쓰는 건 FullSense의 방식에 어긋나므로, 한계도 그대로 공개합니다.

- **증명서를 더 공들인다고 반드시 강해지는 건 아니다.** 직관적으로는 "자를 휘게 할 자유도가 늘면 강해질 일밖에 없다"일 것 같지만, 실제로는 차수를 올리면 오히려 **더 느슨한(약한) 경계**를 돌려줄 수 있다. 가장 빡빡한 추정치를 원하면 각 차수의 결과를 늘어놓고 가장 좋은 것을 고르는 수밖에 없고, 깔끔한 한 줄짜리 계단은 존재하지 않는다. "차수를 올리면 일직선으로 최강에 도달"은 **거짓**이다.
- 정확한 답을 내는 계산은 **NP-난해**(문제가 커지면 알려진 어떤 방법으로도 계산 시간이 폭발한다고 여겨지는 난문 클래스). 남은 미증명 부품 중 더 공들인 증명(차수8)이 4개를 더 닫고, 엄밀 계산의 양면 협공이 그중 2개를 닫았지만, 경계에 딱 걸린 마지막 약 2개 부품은 CPU 범위에서 **여전히 열린 채**. 깔끔하게 닫히지 않는, 정직한 한계입니다.
- 모든 결과는 "작은 부품(n=2, 상태 숫자가 2개)·CPU·이 풀"의 이야기. 안전성은 "**관측된 거짓 허가 0**"이지 "수학적으로 절대"가 아니다(별도의 기계 검증된 엄밀한 증명이 있으나 추가 옵션으로 다룸).
- 이는 "**올바른 검사기를 만드는 법**"의 이야기이지, "진화시킨 AI가 널리 쓸모 있다"는 주장이 아닙니다.

---

## 그래서, 결국 무엇을 알았나?

한 줄로:

> **자랑하던 "풍부한 성적표"는 속이는 계산기가 만든 환상이었다. 정확한 계산기로 바꾸니 환상은 무너지고 —— 주력 검사기는 오히려 전보다 강하다고 드러났다.**

그리고 오늘 가장 전하고 싶은 것:

> **"너무 잘 풀린 결과"는 승리가 아니라 경보.**
> 숫자가 너무 좋으면 믿기 전에 먼저 계산기(solver)를 의심하라. 그리고 같은 도구 안에서 흔들기만 하는 자체 점검은 함정에 눈먼다. **도구를 바꾸는 것**과 **다른 시점에서 적대적으로 두드리는 것**이 환상을 깨는 결정타가 된다.

어떤 숫자보다 **순서**를 기억해 가시길. "좋은 결과가 나온다 → 기뻐한다 → 혹시 몰라 확인한다"에서는 확인이 아무래도 느슨해집니다. "의심하는 장치를 먼저 깐다 → 좋은 결과가 나온다 → 장치가 알아서 의심해 준다". 정직하게 자신을 의심하는 장치를 먼저 깔아 두었기에, 섣부른 기쁨에서 멈추지 않고 단단한 토대에 다다랐다 —— 그런 하루였습니다.

---

**이 글의 기술(완전)판:** [연재 #35-02 "'너무 좋은 숫자'를 의심하라: 다시점 pair-review로 SCS 솔버의 함정을 잡아 정정한 이야기"](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)
