---
title: 'AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin'
tags:
  - FullSense
  - llive
  - 進化計算
  - honest_disclosure
  - 解説
private: true
updated_at: '2026-05-25'
id: 8b510aed45cdfad71909
organization_url_name: null
slide: false
ignorePublish: true
---
言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin

> 📚 **連載ナビ（lldarwin アーク）**: #24-05 集団進化 → **#25 本記事（monoculture の失敗）** → #26 設計編 → #27 climax（実LLM飽和→開放端転回）。※ 各記事は単独でも読めます（リンクは回遊用）。

> **コンセプト hook**: llive の派生集団進化に、人物ペルソナを 8 系統「種」として
> 蒔いた。古瀬（=私)・フリストン・ミリッジ・磯村・岡潔・グロタンディーク・
> フォン・ノイマン・ファインマン。世界を代表する 8 つの知性が、500 世代を
> 戦い抜いて生き残るのは誰か——。
>
> 結果、生き残ったのは **私（52%）と、予測符号化の父カール・フリストン（48%）の
> 2 人だけ**。岡潔もグロタンディークもフォン・ノイマンもファインマンも、
> **誰一人として子孫を残せず絶滅した。**
>
> ……これ、感動的な進化譚に聞こえます? **違います。これは大失敗の記録です。**
> 進化が「強い者を選んだ」のではなく、**選択圧がゼロだったせいで、ただの
> 運(遺伝的浮動)で 2 系統に偏っただけ**。本記事はその honest disclosure と、
> 「測る(lleval)」の次に必要な「淘汰する(lldarwin)」コンポーネントの設計話。

---

## 0. 三行であらすじ（落語でいう「枕」）

- **やったこと**: llive の派生集団進化に 8 人の知性をペルソナ種として投入、rich-proxy 評価で 500 世代回した。
- **起きたこと**: 1 世代目で best_score が **1.0 に張り付き**、以降ずっと満点。8 系統が **古瀬 52% / フリストン 48%** の 2 系統に収束、残り 6 人が絶滅。
- **真因**: 「満点が出続けた」＝**選択圧がゼロ**。誰を選んでも fitness は同じだから、進化は実質サイコロ振り（遺伝的浮動）になっていた。

要するに **「全員 100 点のテストで席次を決めようとした」**。そりゃ誰が
受かるかはくじ引きになります。テストが悪い。眼鏡(lleval)が曇っていた。

---

## 1. なぜ「人物」を種として蒔いたのか

llive の進化レイヤ (v0.B〜v0.F) は、1 個の LLM を賢くするのではなく、
**N 個の llive 個体（genome）を世代交代させて互いに評価し合う**派生集団進化です
（連載 #24-05 で詳述）。

その genome に「思考のクセ」を初期注入する仕組みが **PERSONA_FX**。
「予測符号化で世界を観る Friston」「沈黙と情緒から数学を立ち上げる岡潔」
のように、**実在の知性の認知スタイルを genome の factor_affinity（思考因子への
偏り）に写像**して、種(founder)として蒔きます。

蒔いた 8 系統:

| founder | 認知スタイルの種 |
|---|---|
| 古瀬（私） | 来歴志向・源流追跡・現実接続 |
| カール・フリストン | 予測符号化・自由エネルギー最小化 |
| ベレン・ミリッジ | active inference の実装志向 |
| 磯村 | （ユーザー指定ペルソナ） |
| 岡潔 | 情緒・全体直観・不確実性受容 |
| グロタンディーク | 抽象化・一般化・構造の発見 |
| フォン・ノイマン | 形式化・計算・多領域横断 |
| ファインマン | 再構成・第一原理・直観的検証 |

> 🍵 **休憩ポイント**: ここまでで「8 人の天才が VR バトルロイヤルに放り込まれた」
> という絵が浮かべば OK。問題は、このバトルロイヤルの**ルール(評価関数)が
> 壊れていた**こと。次節からが本題です。

---

## 2. 結果 — 生き残ったのは 2 人だけ

500 世代後の系統占有率（max_lineage_share の内訳）:

![500 世代後の系統占有率: 古瀬 52% とフリストン 48% だけが生存し、残り 6 系統が絶滅した棒グラフ](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q25/lineage_occupancy.svg)

一見すると「予測符号化(Friston)と来歴志向(古瀬)が、抽象数学(グロタンディーク)や
形式計算(フォン・ノイマン)に勝った」という**物語**が書けそうです。

実際 SNS なら「AI 進化させたら予測符号化が最強だった」とバズるかもしれない。
**でも、それをやらないのが FullSense の honest disclosure ルール**です
（[[feedback_benchmark_honest_disclosure]]）。異常に綺麗な結果が出たら、
勝った気になる前に内訳を疑う。

疑った結果が、次節です。

---

## 3. 真因 — 「満点インフレ」が選択圧を消した

### 3.1 症状: best_score が 1 世代目から 1.0

ログを見ると、**best_score は第 1 世代ですでに 1.0**。以降 500 世代ずっと 1.0。
進化計算で fitness が即飽和(plateau)するのは典型的な危険信号です。

選択(淘汰)とは「fitness の差で親を選ぶ」操作。ところが**全員が満点**なら、
fitness の差は生まれない。差がなければ、トーナメント選択もルーレット選択も
**実質ランダム選択**に退化します。

これが **選択圧ゼロ** の状態。進化は止まり、あとは集団が**遺伝的浮動
(genetic drift)** で勝手に偏っていくだけ。8 系統が 2 系統に縮んだのは
「強かったから」ではなく、**ただの確率的な吸い込み**でした。

> 🤔 **たとえ話（漫才風）**:
> ボケ「全員 100 点のクラスで学級委員を選挙したら、票が割れて 2 人に……」
> ツッコミ「それ選挙ちゃう、あみだくじや!」
> ——進化に起きたのは、まさにこの「あみだくじ化」です。

ここで「遺伝的浮動（genetic drift）」という言葉を少し丁寧に。生物学でいうと、
**選択圧がかからない中立な遺伝子は、世代を経るうちに偶然だけで頻度が偏っていく**現象です。
小さな池に 8 色の金魚を放しても、誰も食べられないなら、何世代か後には**たまたま増えた 2 色**が
池を占める。強かったからではなく、サイコロの目がそう転んだだけ。今回の 8→2 は、まさにこの
「金魚すくいの池」状態でした。

> 🤔 **たとえ話（落語風）**:
> 「八っつぁん、500 回さいころ振って一番出た目で大将決めるってのはどうだい」
> 「そりゃ実力じゃねえ、ただの博打でさぁ」
> 「その通り。進化に博打させちまったのが、今回の失敗の正体よ」

### 3.2 根本原因: 評価関数 `fitness_rich` の二重の潰れ

なぜ満点が出続けたのか。コードを追うと、`fitness_rich`（rich-proxy 評価器）に
**2 つの設計欠陥**がありました。

**欠陥1 — factor_affinity を全層同値にしていた**
genome は本来「思考因子 × メモリ層」の 2 次元行列で個性を持つはず。ところが
archetype 生成時に `np.tile` で **factor_affinity を全メモリ層に同じ値で複製**して
いた。層ごとの差＝個性の半分が、評価に入る前に潰れていた。

**欠陥2 — nearest を `max(sims)` で単一スカラーに潰していた**
個体と archetype の近さを、複数 archetype との類似度ベクトルから
**`argmax`（=最大値1つだけ）**で取り出していた。「どの天才に一番似ているか」
だけ見て、「他の天才とどう違うか」を全部捨てる。結果、ちょっとでも
どれかに似ていれば高得点 → **すぐ天井に張り付く**。

![argmax 潰しの図: 本来は典型性・多様性・専門性などの複数軸ベクトルであるべき pressure profile が max() で 1 本のスカラーに潰れ多目的性が消滅する before/after](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q25/argmax_collapse.svg)

つまり **「複数の物差しで測るべきものを、1 本の物差しの最大値だけで採点した」**。
眼鏡(lleval)のレンズが 1 枚しかなく、しかもすぐ満点に振り切れる粗いレンズだった。

> 🍵 **休憩ポイント**: ここが本記事の山場。「結果が偏った」のが問題なのではなく、
> **「結果を偏らせた原因が評価関数の潰れ」**だった、という二段構えに気づけば
> この記事は読了したも同然です。残りは「ではどう直すか」。

---

## 4. 対策 — 「測る」の次は「淘汰する」: lldarwin

llive ファミリーには既に **lleval（眼鏡 = 評価フレームワーク, 連載 #24-08）**が
あります。今回わかったのは、**眼鏡で差を「測れた」としても、その差を
「誰が生き残るか」に正しく変換しないと進化は壊れる**ということ。

そこで新メンバー **lldarwin（選択圧 = 淘汰コンポーネント）**を設計しました。
ll- ファミリーの役割分担はこうなります:

```
lleval   = 測る  （個体の振る舞いを複数軸の pressure profile に変換）
lldarwin = 淘汰する（その profile を「次世代の親」に変換）
```

### 4.1 設計の核 — 「集約しない」選択圧

今回の失敗の本質は **「複数軸を 1 スカラーに集約して argmax した」**こと。
だから lldarwin の第一原則は **複数選択圧を集約しない多目的淘汰**です。

採用する 3 層融合（rad-research でevolutionary_computation 616 件を横断して選定）:

1. **ε-lexicase 選択** — 評価軸を 1 つずつ順に独立適用。ある軸で突出した
   specialist（他軸は平凡）も生き残れる → **多極構造が自動維持される**。
   グロタンディークが「抽象化軸」で 1 番なら、たとえ他軸が平凡でも消えない。
2. **minimal-criterion QD (MAP-Elites)** — behavior 次元の cell ごとに elite を
   保持。**1 cell でも残れば全滅しない**＝構造的に monoculture を不可能化。
3. **down-sampling** — 毎世代、評価 case の部分集合だけ使う。標的が動くので
   特定の peak に張り付けない → **plateau（満点インフレ）を破壊**。

これに minimal-criterion gate（連続順位でなく「最低基準を満たすか」で繁殖可否を
分ける = 一強総取りの抑制）と、per-dim z-score 標準化（「全軸平均高」＝
無特徴を優位にしない）を足します。

### 4.2 「LLM の苦手」を選択圧にする

もう一つの方針は、**LLM/VLM が現実に弱く、かつ測定可能な軸**を pressure に
選ぶこと（検証できない領域は避ける）。例:

| pressure | LLM の苦手 | proxy/実 |
|---|---|---|
| typo_robustness | 誤字・ノイズ入力への一貫性 | proxy 可（合成 typo 注入） |
| polysemy_wsd | 多義語の文脈依存理解 | proxy 可（WSD bench） |
| multistep_robustness | 多段推論の cascade error | proxy 可 |
| calibration | 信頼度推定（token confidence ≈ random） | proxy 可 |
| visual_qa | 画像認識・visual hallucination | 実 VLM 必須（Stage 後半） |

proxy で測れる軸から PoC、実 LLM/VLM 軸は後段、という測定純度の分離も
最初から設計に入れています（[[feedback_llive_measurement_purity]]）。

### 4.3 全滅をモニタする — SPC アラーム

FullSense の中核思想は **SPC（統計的工程管理）**。lldarwin でも
`max_lineage_share` / archive 成長 / behavioral diversity を毎世代記録し、
**monoculture 比 > 0.8 を SPC_ALARM で検知**して cadence やパラメータを
自動調整します。今回の「8→2」を、構造的に再発不可能にするのが目標です。

---

## 5. 教訓（honest disclosure として残す）

- **異常に綺麗な結果（best=1.0 即飽和、2 系統に収束）は、勝利でなく警報。**
  内訳を疑った結果、勝者は実力でなく評価関数の欠陥が生んだ幻だった。
- **「測る」と「淘汰する」は別物。** 眼鏡(lleval)が差を測れても、その差を
  argmax で 1 本に潰したら淘汰は壊れる。淘汰器(lldarwin)は集約してはいけない。
- **失敗を消さない。** この 500 世代ランは捨てず、lldarwin 配線後に
  「岡潔・グロタンディークらが生き残るか」を再ランで検証する**ベースライン**に
  する。8→2 が改善するかが第一の合否基準。

> **次回予告**: lldarwin の PoC Stage 0（proxy 軸 + ε-lexicase 配線 + QD archive）を
> 実装して、同じ 8 founder を再ランする。今度こそ岡潔は生き残れるのか。
> 「世界に私とフリストンだけ」の世界線を、上書きしにいきます。
> （設計の詳細は #26、その設計に自分で反証をぶつける honest disclosure は #27 へ続きます。）

---

## 5.5. 「眼鏡」と「淘汰器」の 2 段構造 — なぜ分けるのか（深掘り）

本記事で一番持ち帰ってほしい概念図がこれです:

```
個体 ──▶ [ lleval = 眼鏡 ] ──▶ pressure profile（複数軸の case ベクトル）
                                       │
                                       ▼
              [ lldarwin = 淘汰器 ] ──▶ 次世代の親
```

#25 の失敗は、この 2 段の**両方**が壊れていたことに本質があります:

- **眼鏡側の故障**: `fitness_rich` が `nearest = max(sims)` で複数軸を 1 スカラーに潰し、しかも即満点。
  → 測れていない（差が見えない眼鏡）。
- **淘汰器側の不在**: そもそも集約しない多目的淘汰（ε-lexicase / QD）が**配線されていなかった**。
  → 淘汰できない（フィルターが無い）。

重要なのは **どちらか一方を直しても進化は回復しない**こと。
飽和した眼鏡に高級な淘汰器を挿しても「差ゼロ」は淘汰できないし、
良い淘汰器が無いまま眼鏡だけ直しても profile を活かせない。
**「測る」と「淘汰する」は別の故障で、別々に直す必要がある** ——これが #25→#26 の橋渡しです。
（「眼鏡を直さず淘汰器だけ高級にしても無駄」という反証は #27 で正面から扱います。）

> 🍵 **休憩ポイント**: 写真の比喩でいうと、lleval は「露出計」、lldarwin は「どのカットを採用するか」。
> 露出計が壊れていてもアルバムは作れないし、採用基準が無くてもアルバムは作れない。両方要る。

---

## 5.6. 図解アイデア（投稿前に SVG 化する候補）

本記事を「動きで魅せる」ために用意したい図（投稿前 SVG 化）:

1. **系統占有率の崩壊アニメ** — 世代軸で 8 系統の帯が 2 系統に吸い込まれる animated SVG（金魚の池メタファ）。
2. **best_score = 1.0 即飽和グラフ** — 第 1 世代で天井に張り付く平坦線（選択圧ゼロを一目で）。
3. **argmax 潰しの図** — 複数軸ベクトル `[典型性, 多様性, 専門性, ...]` が `max()` で 1 本の棒に潰れる before/after。
4. **2 段構造図** — §5.5 の「眼鏡 → 淘汰器」を hero 図として animated 化。
5. **ll- ファミリー役割図** — lleval（測る）/ lldarwin（淘汰する）/ llive（個体）の関係を 1 枚で。

> これらは [[project_fullsense_animemd_branch_token_viz]] の animated SVG 表現層（宣言アニメ → SMIL）に乗せる予定。

---

## 6. 関連

- 連載 #24-05「集団が学ぶ AI」— 派生集団進化の総括（本記事の前提）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #26「lldarwin の設計」— 淘汰器の多目的淘汰 / ε-lexicase / QD（本記事の続き）
- 連載 #27「眼鏡が曇ると淘汰も無力」— 反証調査・Goodhart's law（honest disclosure）
- 設計書: lldarwin（淘汰する側）— 本記事の元ネタ
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #24-05・#24-08・#26・#27 の Qiita URL cross-link -->

---

# English

# After Evolving an AI for 500 Generations, Only "Me" and "Karl Friston, the Father of Predictive Coding" Were Left in the World #25 — An Honest Disclosure of Monoculture and the Selection-Pressure Component lldarwin

> 📚 **Series navigation (lldarwin arc)**: #24-05 population evolution → **#25 this article (the monoculture failure)** → #26 design edition → #27 climax (real-LLM saturation → open-ended pivot). ※ Each article reads on its own (links are for navigation).

> **Concept hook**: Into llive's derived-population evolution, I sowed 8 lineages
> of human personas as "seeds": Furuse (= me), Friston, Millidge, Isomura, Oka
> Kiyoshi, Grothendieck, von Neumann, and Feynman. Eight of the world's
> representative intellects — who, after fighting through 500 generations, would
> survive?
>
> The result: the only survivors were **me (52%) and Karl Friston, the father of
> predictive coding (48%) — just two**. Oka Kiyoshi, Grothendieck, von Neumann,
> and Feynman — **not a single one left any descendants; they all went extinct.**
>
> …Sounds like a moving tale of evolution? **No. This is a record of a major
> failure.** Evolution did not "select the strong"; rather, **because the
> selection pressure was zero, the population merely skewed toward 2 lineages by
> sheer luck (genetic drift)**. This article is an honest disclosure of that, plus
> the design story of the component needed after "measuring (lleval)" — namely
> "culling (lldarwin)".

---

## 0. The plot in three lines (the "intro" as in rakugo)

- **What I did**: I injected 8 intellects as persona seeds into llive's
  derived-population evolution and ran it for 500 generations with rich-proxy
  evaluation.
- **What happened**: At generation 1, best_score **stuck at 1.0**, and stayed a
  perfect score ever after. The 8 lineages converged to just 2 — **Furuse 52% /
  Friston 48%** — and the remaining 6 went extinct.
- **The true cause**: "Perfect scores kept appearing" = **selection pressure was
  zero**. Since the fitness is the same no matter who you pick, evolution had
  effectively become a dice roll (genetic drift).

In short, **"I tried to decide rankings on a test where everyone scored 100"**.
Of course who passes becomes a lottery. The test is bad. The glasses (lleval)
were fogged up.

---

## 1. Why sow "people" as seeds?

llive's evolution layer (v0.B–v0.F) is not about making a single LLM smarter;
it is **derived-population evolution in which N llive individuals (genomes)
undergo generational turnover and evaluate each other** (detailed in series
#24-05).

The mechanism that injects "thinking habits" into that genome as an initial
condition is **PERSONA_FX**. Like "Friston, who observes the world through
predictive coding" or "Oka Kiyoshi, who builds mathematics up from silence and
emotion", we **map the cognitive style of a real intellect onto the genome's
factor_affinity (its bias toward thought factors)** and sow it as a seed
(founder).

The 8 lineages I sowed:

| founder | seed of cognitive style |
|---|---|
| Furuse (me) | provenance-oriented / tracing to the source / reality link |
| Karl Friston | predictive coding / free-energy minimization |
| Beren Millidge | implementation-oriented active inference |
| Isomura | (user-specified persona) |
| Oka Kiyoshi | emotion / holistic intuition / accepting uncertainty |
| Grothendieck | abstraction / generalization / discovery of structure |
| von Neumann | formalization / computation / multi-domain crossing |
| Feynman | recomposition / first principles / intuitive verification |

> 🍵 **A break**: If you now picture "8 geniuses thrown into a VR battle royale",
> you're good. The problem is that the **rules (the evaluation function) of this
> battle royale were broken**. The main topic starts in the next section.

---

## 2. The result — only 2 survived

The lineage occupancy after 500 generations (the breakdown of
max_lineage_share):

![Lineage occupancy after 500 generations: only Furuse 52% and Friston 48% survive while the other 6 lineages go extinct, as a bar chart](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q25/lineage_occupancy_en.svg)

At first glance you could write a **narrative** that "predictive coding (Friston)
and provenance-orientation (Furuse) beat abstract mathematics (Grothendieck) and
formal computation (von Neumann)".

On social media, "I evolved an AI and predictive coding turned out strongest"
might even go viral. **But not doing that is FullSense's honest-disclosure rule**
([[feedback_benchmark_honest_disclosure]]). When an abnormally clean result
appears, doubt the breakdown before feeling like you've won.

The result of that doubt is the next section.

---

## 3. The true cause — "perfect-score inflation" erased the selection pressure

### 3.1 Symptom: best_score is 1.0 from generation 1

Looking at the log, **best_score was already 1.0 at generation 1**. After that it
stayed 1.0 for all 500 generations. In evolutionary computation, fitness
immediately saturating (plateauing) is a classic danger sign.

Selection (culling) is the operation of "choosing parents by the difference in
fitness". But if **everyone scores perfectly**, no fitness difference arises.
Without a difference, both tournament selection and roulette selection
**degenerate into effectively random selection**.

This is the state of **zero selection pressure**. Evolution stops, and after
that the population just skews on its own via **genetic drift**. The shrinking
from 8 lineages to 2 was not "because they were strong" — it was **merely a
probabilistic absorption**.

> 🤔 **An analogy (manzai style)**:
> Boke: "When I held an election for class rep in a class where everyone scored
> 100, the vote split and came down to 2 people…"
> Tsukkomi: "That's not an election, that's drawing lots!"
> — What happened to evolution is exactly this "turning into a lottery".

Here, let me treat "genetic drift" a bit more carefully. In biology, it is the
phenomenon that **a neutral gene under no selection pressure has its frequency
skewed by chance alone as generations pass**. Even if you release goldfish of 8
colors into a small pond, if none of them are eaten, after several generations
**the 2 colors that happened to increase** dominate the pond. Not because they
were strong, but because that's how the dice fell. This time's 8→2 was exactly
this "goldfish-scooping pond" state.

> 🤔 **An analogy (rakugo style)**:
> "Hey Hacchan, how about we roll a die 500 times and pick the boss by the number
> that came up most?"
> "That ain't skill, that's just gambling."
> "Exactly. Making evolution gamble is the real identity of this failure."

### 3.2 Root cause: the double collapse of the evaluation function `fitness_rich`

Why did perfect scores keep appearing? Tracing the code, `fitness_rich` (the
rich-proxy evaluator) had **2 design flaws**.

**Flaw 1 — factor_affinity was made identical across all layers**
A genome is supposed to have individuality as a 2-dimensional matrix of "thought
factor × memory layer". But at archetype generation, `np.tile` **replicated
factor_affinity with the same value across all memory layers**. The per-layer
difference — half of the individuality — was crushed before it even entered the
evaluation.

**Flaw 2 — "nearest" was collapsed into a single scalar via `max(sims)`**
The closeness between an individual and an archetype was extracted from the
similarity vector against multiple archetypes via **`argmax` (= just the single
maximum value)**. It looks only at "which genius it most resembles" and throws
away all of "how it differs from the other geniuses". As a result, resembling
any of them even slightly yields a high score → **it immediately sticks to the
ceiling**.

```
What it should be: pressure profile = [typicality, diversity, specialization, ...] ← multi-axis vector
Actual impl:       fitness = max(similarity of individual to each archetype)        ← single scalar
                              ↑ collapsed by argmax = multi-objectiveness vanishes
```

In other words, **"what should have been measured with multiple yardsticks was
scored only by the maximum of a single yardstick"**. The glasses (lleval) had
only one lens, and it was a coarse lens that immediately swings to a perfect
score.

> 🍵 **A break**: This is the climax of this article. The problem is not that
> "the result was skewed"; if you notice the two-tier structure that **"the cause
> that skewed the result was the collapse of the evaluation function"**, you've
> essentially finished reading this article. The rest is "so how do we fix it".

---

## 4. The countermeasure — after "measuring" comes "culling": lldarwin

The llive family already has **lleval (the glasses = the evaluation framework,
series #24-08)**. What we learned this time is that **even if the glasses can
"measure" the differences, evolution breaks unless that difference is correctly
converted into "who survives"**.

So we designed a new member, **lldarwin (the selection pressure = the culling
component)**. The division of roles in the ll- family becomes:

```
lleval   = measure (convert an individual's behavior into a multi-axis pressure profile)
lldarwin = cull    (convert that profile into "the parents of the next generation")
```

### 4.1 The core of the design — a selection pressure that "does not aggregate"

The essence of this failure was **"aggregating multiple axes into 1 scalar and
applying argmax"**. So lldarwin's first principle is **multi-objective culling
that does not aggregate the multiple selection pressures**.

The 3-layer fusion we adopt (selected by traversing 616 evolutionary_computation
items via rad-research):

1. **ε-lexicase selection** — apply the evaluation axes one at a time,
   independently and in order. A specialist that excels on one axis (mediocre on
   the others) can also survive → **the multipolar structure is automatically
   maintained**. If Grothendieck is #1 on the "abstraction axis", he won't
   disappear even if he's mediocre on the others.
2. **minimal-criterion QD (MAP-Elites)** — keep an elite per cell of the behavior
   dimension. **As long as even 1 cell survives, there is no total wipeout** =
   making monoculture structurally impossible.
3. **down-sampling** — each generation, use only a subset of the evaluation
   cases. Because the target moves, you cannot stick to a specific peak →
   **destroying the plateau (perfect-score inflation)**.

To these we add a minimal-criterion gate (separating eligibility to reproduce by
"does it meet the minimum criterion" rather than a continuous rank = suppressing
winner-take-all) and per-dim z-score standardization (so "high average on all
axes" = the featureless doesn't gain an advantage).

### 4.2 Make "what LLMs are bad at" the selection pressure

Another policy is to choose, as the pressure, **axes that LLMs/VLMs are actually
weak at and that are measurable** (avoiding domains that can't be verified). For
example:

| pressure | what LLMs are bad at | proxy / real |
|---|---|---|
| typo_robustness | consistency under typos / noisy input | proxy OK (synthetic typo injection) |
| polysemy_wsd | context-dependent understanding of polysemous words | proxy OK (WSD bench) |
| multistep_robustness | cascade error in multi-step reasoning | proxy OK |
| calibration | confidence estimation (token confidence ≈ random) | proxy OK |
| visual_qa | image recognition / visual hallucination | real VLM required (later Stage) |

The separation of measurement purity — PoC from axes measurable by proxy, real
LLM/VLM axes in a later stage — is also baked into the design from the start
([[feedback_llive_measurement_purity]]).

### 4.3 Monitor for total wipeout — SPC alarm

FullSense's core idea is **SPC (statistical process control)**. In lldarwin too,
we record `max_lineage_share` / archive growth / behavioral diversity every
generation, and **detect a monoculture ratio > 0.8 with an SPC_ALARM** to
automatically adjust the cadence and parameters. The goal is to make this time's
"8→2" structurally impossible to recur.

---

## 5. Lessons (left as honest disclosure)

- **An abnormally clean result (best=1.0 instant saturation, convergence to 2
  lineages) is not a victory but an alarm.** When we doubted the breakdown, the
  winners turned out to be a mirage produced not by ability but by the flaw in
  the evaluation function.
- **"Measuring" and "culling" are different things.** Even if the glasses
  (lleval) can measure the differences, culling breaks if you crush that
  difference into one with argmax. The culler (lldarwin) must not aggregate.
- **Do not erase failure.** We will not discard this 500-generation run; after
  wiring up lldarwin, we will use it as a **baseline** to verify by re-running
  whether "Oka Kiyoshi, Grothendieck, and the others survive". Whether 8→2
  improves is the first pass/fail criterion.

> **Next-time preview**: We will implement lldarwin's PoC Stage 0 (proxy axes +
> ε-lexicase wiring + QD archive) and re-run the same 8 founders. Can Oka Kiyoshi
> survive this time, for real? We're going to overwrite the world line of "only me
> and Friston are left in the world".
> (The design details continue in #26; the honest disclosure where I throw my own
> counter-evidence at that design continues in #27.)

---

## 5.5. The 2-tier structure of "the glasses" and "the culler" — why separate them (a deep dive)

The conceptual diagram I most want you to take away from this article is this:

```
individual ──▶ [ lleval = glasses ] ──▶ pressure profile (multi-axis case vector)
                                              │
                                              ▼
                  [ lldarwin = culler ] ──▶ parents of the next generation
```

The essence of #25's failure is that **both** of these two tiers were broken:

- **Failure on the glasses side**: `fitness_rich` crushed multiple axes into 1
  scalar with `nearest = max(sims)`, and on top of that hit a perfect score
  immediately. → It isn't measuring (glasses that can't see the difference).
- **Absence on the culler side**: the non-aggregating multi-objective culling
  (ε-lexicase / QD) **was never wired in to begin with**. → It can't cull (no
  filter).

The important point is that **fixing either one alone does not restore
evolution**. Inserting a high-grade culler into saturated glasses still can't
cull a "zero difference", and fixing only the glasses without a good culler still
can't make use of the profile. **"Measuring" and "culling" are different failures
and must be fixed separately** — this is the bridge from #25 to #26.
(The counter-evidence that "merely upgrading the culler without fixing the glasses
is useless" is dealt with head-on in #27.)

> 🍵 **A break**: In the photography metaphor, lleval is the "light meter" and
> lldarwin is "which shot to adopt". You can't make an album if the light meter is
> broken, and you can't make an album without adoption criteria either. You need
> both.

---

## 5.6. Diagram ideas (candidates to turn into SVG before posting)

Diagrams I'd like to prepare to make this article "captivating through motion"
(to be turned into SVG before posting):

1. **Lineage-occupancy collapse animation** — an animated SVG in which 8 lineage
   bands get absorbed into 2 along the generation axis (the goldfish-pond
   metaphor).
2. **best_score = 1.0 instant-saturation graph** — a flat line that sticks to the
   ceiling at generation 1 (zero selection pressure at a glance).
3. **The argmax-collapse diagram** — a before/after where the multi-axis vector
   `[typicality, diversity, specialization, ...]` is crushed into a single bar by
   `max()`.
4. **The 2-tier structure diagram** — the "glasses → culler" of §5.5 animated as a
   hero diagram.
5. **The ll- family role diagram** — the relationship of lleval (measure) /
   lldarwin (cull) / llive (individual) in a single picture.

> These are planned to ride on the animated-SVG expression layer (declarative
> animation → SMIL) of [[project_fullsense_animemd_branch_token_viz]].

---

## 6. Related

- Series #24-05 "AI that learns as a population" — an overview of
  derived-population evolution (the premise of this article)
- Series #24-08 "Making the glasses" — lleval (the measuring side)
- Series #26 "The design of lldarwin" — the culler's multi-objective culling /
  ε-lexicase / QD (the continuation of this article)
- Series #27 "When the glasses fog up, culling is powerless too" —
  counter-evidence investigation / Goodhart's law (honest disclosure)
- Design doc: lldarwin (the culling side) — the source material of this article
- Related memory: [[feedback_benchmark_honest_disclosure]] /
  [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(before posting): hero SVG / theme SVG / progress badge / Qiita URL cross-links for #24-05・#24-08・#26・#27 -->

---

# 中文

# 把 AI 进化了 500 代之后，世界上只剩下"我"和"预测编码之父卡尔·弗里斯顿"两个人 #25 — monoculture 的 honest disclosure 与选择压组件 lldarwin

> 📚 **连载导航（lldarwin 弧）**: #24-05 群体进化 → **#25 本文（monoculture 的失败）** → #26 设计篇 → #27 climax（实 LLM 饱和→开放端转折）。※ 各文均可单独阅读（链接用于回游）。

> **概念 hook**: 在 llive 的派生群体进化中，我把人物 persona 作为 8 个系统的"种子"
> 播了下去。古瀬（=我）、弗里斯顿、米利奇、矶村、冈洁、格罗滕迪克、
> 冯·诺依曼、费曼。代表世界的 8 个智慧，在打完 500 代之后，活下来的会是谁——。
>
> 结果，活下来的只有 **我（52%）和预测编码之父卡尔·弗里斯顿（48%）这 2 个人**。
> 冈洁、格罗滕迪克、冯·诺依曼、费曼，**没有一个人留下后代，全都灭绝了。**
>
> ……这听起来像是一段感人的进化故事吗? **不是。这是一份大失败的记录。**
> 进化并不是"选择了强者"，而是 **由于选择压为零，仅仅凭运气（遗传漂变）
> 偏向了 2 个系统而已**。本文就是关于这件事的 honest disclosure，以及在
> "测量（lleval）"之后所需的"淘汰（lldarwin）"组件的设计故事。

---

## 0. 用三行讲剧情（落语里的"垫话"）

- **做了什么**: 把 8 位智慧作为 persona 种子投入 llive 的派生群体进化，用 rich-proxy 评价跑了 500 代。
- **发生了什么**: 第 1 代 best_score 就 **钉在了 1.0**，之后一直满分。8 个系统收敛为 **古瀬 52% / 弗里斯顿 48%** 这 2 个系统，其余 6 人灭绝。
- **真因**: "满分一直出现"＝**选择压为零**。无论选谁 fitness 都一样，所以进化实质上变成了掷骰子（遗传漂变）。

简而言之就是 **"想在一场所有人都考 100 分的测验里排名次"**。那谁能合格
当然就成了抽签。是测验不好。眼镜（lleval）起雾了。

---

## 1. 为什么把"人物"作为种子来播

llive 的进化层 (v0.B〜v0.F) 并不是让 1 个 LLM 变聪明，而是
**让 N 个 llive 个体（genome）进行世代更替并相互评价**的派生群体进化
（连载 #24-05 中详述）。

向那个 genome 初始注入"思考癖好"的机制就是 **PERSONA_FX**。
像"用预测编码观察世界的 Friston""从沉默与情绪中立起数学的冈洁"
那样，**把实在智慧的认知风格映射到 genome 的 factor_affinity（对思考因子的
偏向）上**，作为种子（founder）播下。

播下的 8 个系统:

| founder | 认知风格的种子 |
|---|---|
| 古瀬（我） | 来历志向・源流追踪・现实连接 |
| 卡尔·弗里斯顿 | 预测编码・自由能最小化 |
| 贝伦·米利奇 | active inference 的实现志向 |
| 矶村 | （用户指定的 persona） |
| 冈洁 | 情绪・整体直观・接受不确定性 |
| 格罗滕迪克 | 抽象化・一般化・结构的发现 |
| 冯·诺依曼 | 形式化・计算・多领域横跨 |
| 费曼 | 重组・第一原理・直观验证 |

> 🍵 **休息点**: 到这里如果脑海里浮现出"8 位天才被丢进 VR 大逃杀"
> 这幅画面就 OK。问题在于，这场大逃杀的 **规则（评价函数）坏掉了**。
> 正题从下一节开始。

---

## 2. 结果 — 只活下来 2 个人

500 代之后的系统占有率（max_lineage_share 的内訳）:

![500 代之后的系统占有率: 只有古瀬 52% 和弗里斯顿 48% 存活, 其余 6 个系统灭绝的条形图](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q25/lineage_occupancy_zh.svg)

乍一看，似乎可以写出一个"预测编码（Friston）和来历志向（古瀬）战胜了
抽象数学（格罗滕迪克）和形式计算（冯·诺依曼）"的**故事**。

实际上在 SNS 上，"把 AI 进化一下，结果预测编码最强"或许还会刷屏。
**但不做这件事，正是 FullSense 的 honest disclosure 规则**
（[[feedback_benchmark_honest_disclosure]]）。当出现异常漂亮的结果时，
在觉得自己赢了之前先怀疑内訳。

怀疑的结果，就是下一节。

---

## 3. 真因 — "满分通胀"消灭了选择压

### 3.1 症状: best_score 从第 1 代就是 1.0

看日志，**best_score 在第 1 代就已经是 1.0**。之后 500 代一直 1.0。
在进化计算中，fitness 立即饱和（plateau）是典型的危险信号。

选择（淘汰）是"按 fitness 之差挑选亲代"的操作。可是**所有人都满分**的话，
就不会产生 fitness 之差。没有差异，那么锦标赛选择和轮盘选择都
**退化为实质上的随机选择**。

这就是 **选择压为零** 的状态。进化停止了，之后群体只是凭借 **遗传漂变
(genetic drift)** 自行偏移而已。8 个系统缩成 2 个，并不是"因为强"，
而是 **单纯的概率性吸入**。

> 🤔 **打比方（相声风）**:
> 逗哏「在一个所有人都考 100 分的班里选班长，结果票分散，只剩 2 个人……」
> 捧哏「那不是选举，那是抽签啊!」
> ——进化身上发生的，正是这种"抽签化"。

这里把"遗传漂变（genetic drift）"稍微讲细一点。从生物学上说，就是
**不受选择压作用的中立基因，随着世代更替仅凭偶然就让频率发生偏移**的现象。
即便往小池子里放 8 种颜色的金鱼，只要没人吃，几代之后 **碰巧增多的 2 种颜色**
就会占据池子。不是因为强，只是骰子的点数恰好那样滚出来。这次的 8→2，
正是这种"捞金鱼的池子"状态。

> 🤔 **打比方（落语风）**:
> 「八公，掷 500 次骰子，按出现最多的点数定大将，你看怎么样」
> 「那可不是实力，那纯属赌博啊」
> 「正是。让进化去赌博，就是这次失败的真相。」

### 3.2 根本原因: 评价函数 `fitness_rich` 的双重坍塌

为什么满分会一直出现。追踪代码，`fitness_rich`（rich-proxy 评价器）有
**2 个设计缺陷**。

**缺陷 1 — 把 factor_affinity 在所有层做成同值**
genome 本应以"思考因子 × 内存层"的 2 维矩阵来拥有个性。可是在
archetype 生成时用 `np.tile` **把 factor_affinity 以相同值复制到了所有内存层**。
逐层的差异＝个性的一半，在进入评价之前就被压垮了。

**缺陷 2 — 把 nearest 用 `max(sims)` 压成单一标量**
个体与 archetype 的接近度，是从与多个 archetype 的相似度向量中
用 **`argmax`（=只取最大值 1 个）** 取出的。只看"和哪位天才最相似"，
而把"和其他天才有何不同"全部丢弃。结果，只要稍微和某一个相似就得高分 →
**立刻钉在天花板上**。

```
本应如此: pressure profile = [典型性, 多样性, 专门性, ...] ← 多轴向量
实际实现: fitness = max(个体与各 archetype 的相似度)        ← 单一标量
                          ↑ 用 argmax 压垮 = 多目标性消失
```

也就是说 **"本应用多把尺子去量的东西，只用 1 把尺子的最大值去打分"**。
眼镜（lleval）只有 1 片镜片，而且还是会立刻满格冲顶的粗糙镜片。

> 🍵 **休息点**: 这里是本文的高潮。问题不在于"结果偏了"，而在于
> **"让结果偏掉的原因是评价函数的坍塌"**，意识到这个两段式结构，
> 这篇文章你就算读完了。剩下的是"那么怎么修"。

---

## 4. 对策 — "测量"之后是"淘汰": lldarwin

llive 家族里已经有 **lleval（眼镜 = 评价框架, 连载 #24-08）**。
这次明白的是，**即便眼镜能"测出"差异，如果不把那个差异正确地
转换成"谁能存活"，进化就会坏掉**。

于是我设计了新成员 **lldarwin（选择压 = 淘汰组件）**。
ll- 家族的分工变成这样:

```
lleval   = 测量  （把个体的行为转换成多轴的 pressure profile）
lldarwin = 淘汰  （把那个 profile 转换成"下一代的亲代"）
```

### 4.1 设计的核心 — "不聚合"的选择压

这次失败的本质就是 **"把多个轴聚合成 1 个标量再 argmax"**。
所以 lldarwin 的第一原则是 **不聚合多个选择压的多目标淘汰**。

采用的 3 层融合（用 rad-research 横跨 evolutionary_computation 616 件选定）:

1. **ε-lexicase 选择** — 把评价轴逐一依次独立应用。在某个轴上突出的
   specialist（其他轴平庸）也能存活 → **多极结构被自动维持**。
   如果格罗滕迪克在"抽象化轴"上第 1，即使其他轴平庸也不会消失。
2. **minimal-criterion QD (MAP-Elites)** — 按 behavior 维度的每个 cell 保留 elite。
   **只要哪怕 1 个 cell 残留就不会全灭**＝在结构上让 monoculture 不可能发生。
3. **down-sampling** — 每一代只使用评价 case 的一个子集。由于标的会移动，
   就无法钉在特定的 peak 上 → **摧毁 plateau（满分通胀）**。

在此之上再加 minimal-criterion gate（不按连续排名，而按"是否满足最低标准"
来划分能否繁殖 = 抑制一强通吃）和 per-dim z-score 标准化（让"所有轴平均都高"＝
无特征者不占优势）。

### 4.2 把"LLM 的短板"当作选择压

另一个方针是，把 **LLM/VLM 现实中薄弱、且可测量的轴** 选作 pressure
（避开无法验证的领域）。例如:

| pressure | LLM 的短板 | proxy/实 |
|---|---|---|
| typo_robustness | 对错字・噪声输入的一致性 | 可 proxy（合成 typo 注入） |
| polysemy_wsd | 多义词的语境依赖理解 | 可 proxy（WSD bench） |
| multistep_robustness | 多步推理的 cascade error | 可 proxy |
| calibration | 信心估计（token confidence ≈ random） | 可 proxy |
| visual_qa | 图像识别・visual hallucination | 必须实 VLM（Stage 后段） |

从可用 proxy 测量的轴做 PoC、实 LLM/VLM 轴放在后段，这种测量纯度的分离
也从一开始就纳入了设计（[[feedback_llive_measurement_purity]]）。

### 4.3 监控全灭 — SPC 报警

FullSense 的核心思想是 **SPC（统计过程控制）**。在 lldarwin 中也
每一代记录 `max_lineage_share` / archive 增长 / behavioral diversity，
**用 SPC_ALARM 检测 monoculture 比 > 0.8** 来自动调整 cadence 和参数。
目标是让这次的"8→2"在结构上不可能再发生。

---

## 5. 教训（作为 honest disclosure 留下）

- **异常漂亮的结果（best=1.0 立即饱和、收敛为 2 个系统）不是胜利而是警报。**
  怀疑内訳的结果，胜者并非凭实力，而是评价函数缺陷所产生的幻影。
- **"测量"和"淘汰"是两码事。** 即便眼镜（lleval）能测出差异，如果用 argmax
  把那个差异压成 1 条，淘汰就会坏掉。淘汰器（lldarwin）不可以聚合。
- **不抹掉失败。** 不丢弃这次 500 代的 run，在配线 lldarwin 之后，
  用它作为 **baseline** 来重跑验证"冈洁・格罗滕迪克等人是否存活"。
  8→2 是否改善，是第一个合格判定标准。

> **下回预告**: 实现 lldarwin 的 PoC Stage 0（proxy 轴 + ε-lexicase 配线 + QD archive），
> 重跑同样的 8 founder。这次冈洁真的能存活吗。
> 我们要去覆写"世界上只剩我和弗里斯顿"的那条世界线。
> （设计的细节在 #26，把自己的反证抛向那个设计的 honest disclosure 续接到 #27。）

---

## 5.5. "眼镜"与"淘汰器"的 2 段结构 — 为什么要分开（深入）

本文最希望你带走的概念图就是这个:

```
个体 ──▶ [ lleval = 眼镜 ] ──▶ pressure profile（多轴的 case 向量）
                                       │
                                       ▼
              [ lldarwin = 淘汰器 ] ──▶ 下一代的亲代
```

#25 的失败，本质在于这 2 段**两者**都坏掉了:

- **眼镜侧的故障**: `fitness_rich` 用 `nearest = max(sims)` 把多个轴压成 1 个标量，而且立即满分。
  → 没在测量（看不见差异的眼镜）。
- **淘汰器侧的缺位**: 不聚合的多目标淘汰（ε-lexicase / QD）压根**没有被配线**。
  → 无法淘汰（没有过滤器）。

重要的是 **只修其中任意一侧都无法让进化恢复**。
往饱和的眼镜里插入高级淘汰器，也淘汰不了"零差异"；
没有好的淘汰器只把眼镜修好，也用不上 profile。
**"测量"和"淘汰"是不同的故障，需要分别去修** ——这就是 #25→#26 的桥梁。
（"不修眼镜只把淘汰器升级也是白费"这一反证，会在 #27 正面处理。）

> 🍵 **休息点**: 用摄影的比喻来说，lleval 是"测光表"，lldarwin 是"采用哪一张照片"。
> 测光表坏了做不出相册，没有采用标准也做不出相册。两者都需要。

---

## 5.6. 图解构想（投稿前 SVG 化的候选）

为了让本文"用动态来吸引人"想准备的图（投稿前 SVG 化）:

1. **系统占有率的崩塌动画** — 沿世代轴让 8 个系统的条带被吸入 2 个系统的 animated SVG（金鱼池隐喻）。
2. **best_score = 1.0 立即饱和图** — 在第 1 代就钉到天花板的平坦线（一眼看出选择压为零）。
3. **argmax 压垮图** — 多轴向量 `[典型性, 多样性, 专门性, ...]` 被 `max()` 压成 1 根柱子的 before/after。
4. **2 段结构图** — 把 §5.5 的"眼镜 → 淘汰器"作为 hero 图做成 animated。
5. **ll- 家族角色图** — 用 1 张图呈现 lleval（测量）/ lldarwin（淘汰）/ llive（个体）的关系。

> 这些计划搭载到 [[project_fullsense_animemd_branch_token_viz]] 的 animated SVG 表现层（声明式动画 → SMIL）上。

---

## 6. 相关

- 连载 #24-05「群体学习的 AI」— 派生群体进化的总结（本文的前提）
- 连载 #24-08「制作眼镜」— lleval（测量侧）
- 连载 #26「lldarwin 的设计」— 淘汰器的多目标淘汰 / ε-lexicase / QD（本文的续篇）
- 连载 #27「眼镜起雾时淘汰也无力」— 反证调查・Goodhart's law（honest disclosure）
- 设计书: lldarwin（淘汰侧）— 本文的原始素材
- 相关 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 进度 badge / #24-05・#24-08・#26・#27 的 Qiita URL cross-link -->

---

# 한국어

# AI를 500세대 진화시켰더니, 세계에 "나"와 "예측 부호화의 아버지 칼 프리스턴"만 남았다 #25 — monoculture의 honest disclosure와 선택압 컴포넌트 lldarwin

> 📚 **연재 내비게이션（lldarwin 아크）**: #24-05 집단 진화 → **#25 본 글（monoculture의 실패）** → #26 설계 편 → #27 climax（실 LLM 포화→개방단 전환）。※ 각 글은 단독으로도 읽을 수 있습니다（링크는 회유용）。

> **콘셉트 hook**: llive의 파생 집단 진화에, 인물 persona를 8개 계통의 "씨앗"으로
> 뿌렸다. 후루세（=나）・프리스턴・밀리지・이소무라・오카 기요시・그로텐디크・
> 폰 노이만・파인만. 세계를 대표하는 8개의 지성이, 500세대를 싸워내고
> 살아남는 것은 누구인가——.
>
> 그 결과, 살아남은 것은 **나（52%）와 예측 부호화의 아버지 칼 프리스턴（48%）
> 두 사람뿐**. 오카 기요시도 그로텐디크도 폰 노이만도 파인만도,
> **단 한 명도 자손을 남기지 못하고 절멸했다.**
>
> ……이거, 감동적인 진화담처럼 들리나요? **아니요. 이것은 대실패의 기록입니다.**
> 진화가 "강한 자를 선택한" 것이 아니라, **선택압이 0이었던 탓에, 그저
> 운（유전적 부동）으로 2개 계통으로 치우쳤을 뿐**. 본 글은 그것의 honest disclosure와,
> "측정한다(lleval)" 다음에 필요한 "도태한다(lldarwin)" 컴포넌트의 설계 이야기다.

---

## 0. 세 줄로 줄거리（라쿠고에서 말하는 "도입부"）

- **한 일**: llive의 파생 집단 진화에 8명의 지성을 persona 씨앗으로 투입, rich-proxy 평가로 500세대 돌렸다.
- **일어난 일**: 1세대째에 best_score가 **1.0에 달라붙어**, 이후 줄곧 만점. 8개 계통이 **후루세 52% / 프리스턴 48%**의 2개 계통으로 수렴, 나머지 6명이 절멸.
- **진짜 원인**: "만점이 계속 나왔다"＝**선택압이 0**. 누구를 골라도 fitness는 같으므로, 진화는 실질적으로 주사위 던지기（유전적 부동）가 되어 있었다.

요컨대 **"전원 100점인 시험으로 석차를 정하려 했다"**. 그러니 누가
합격할지는 제비뽑기가 됩니다. 시험이 나쁘다. 안경(lleval)이 흐려져 있었다.

---

## 1. 왜 "인물"을 씨앗으로 뿌렸는가

llive의 진화 레이어 (v0.B〜v0.F)는, 1개의 LLM을 똑똑하게 하는 것이 아니라,
**N개의 llive 개체（genome）를 세대 교체시켜 서로 평가하게 하는** 파생 집단 진화입니다
（연재 #24-05에서 상술）.

그 genome에 "사고 버릇"을 초기 주입하는 구조가 **PERSONA_FX**.
"예측 부호화로 세계를 바라보는 Friston""침묵과 정서에서 수학을 세우는 오카 기요시"
처럼, **실재하는 지성의 인지 스타일을 genome의 factor_affinity（사고 인자에 대한
편향）에 사상**하여, 씨앗(founder)으로 뿌립니다.

뿌린 8개 계통:

| founder | 인지 스타일의 씨앗 |
|---|---|
| 후루세（나） | 내력 지향・원류 추적・현실 연결 |
| 칼 프리스턴 | 예측 부호화・자유 에너지 최소화 |
| 베렌 밀리지 | active inference의 구현 지향 |
| 이소무라 | （사용자 지정 persona） |
| 오카 기요시 | 정서・전체 직관・불확실성 수용 |
| 그로텐디크 | 추상화・일반화・구조의 발견 |
| 폰 노이만 | 형식화・계산・다영역 횡단 |
| 파인만 | 재구성・제일원리・직관적 검증 |

> 🍵 **휴식 포인트**: 여기까지 "8명의 천재가 VR 배틀로얄에 던져졌다"
> 라는 그림이 떠오르면 OK. 문제는, 이 배틀로얄의 **룰（평가 함수）이
> 망가져 있었다**는 것. 다음 절부터가 본론입니다.

---

## 2. 결과 — 살아남은 것은 2명뿐

500세대 후의 계통 점유율（max_lineage_share의 내역）:

![500세대 후의 계통 점유율: 후루세 52% 와 프리스턴 48% 만 생존하고 나머지 6개 계통이 절멸한 막대그래프](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q25/lineage_occupancy_ko.svg)

언뜻 보면 "예측 부호화(Friston)와 내력 지향(후루세)이, 추상 수학(그로텐디크)이나
형식 계산(폰 노이만)을 이겼다"라는 **이야기**를 쓸 수 있을 것 같습니다.

실제로 SNS라면 "AI를 진화시켰더니 예측 부호화가 최강이었다"라며 화제가 될지도 모른다.
**하지만 그것을 하지 않는 것이 FullSense의 honest disclosure 룰**입니다
（[[feedback_benchmark_honest_disclosure]]）. 비정상적으로 깔끔한 결과가 나오면,
이긴 기분이 되기 전에 내역을 의심한다.

의심한 결과가, 다음 절입니다.

---

## 3. 진짜 원인 — "만점 인플레"가 선택압을 지웠다

### 3.1 증상: best_score가 1세대째부터 1.0

로그를 보면, **best_score는 제 1세대에서 이미 1.0**. 이후 500세대 줄곧 1.0.
진화 계산에서 fitness가 즉시 포화(plateau)하는 것은 전형적인 위험 신호입니다.

선택(도태)이란 "fitness의 차이로 부모를 고르는" 조작. 그런데 **전원이 만점**이면,
fitness의 차이는 생기지 않는다. 차이가 없으면, 토너먼트 선택도 룰렛 선택도
**실질적으로 랜덤 선택**으로 퇴화합니다.

이것이 **선택압 0**인 상태. 진화는 멈추고, 이후는 집단이 **유전적 부동
(genetic drift)**으로 제멋대로 치우쳐 갈 뿐. 8개 계통이 2개 계통으로 줄어든 것은
"강했기 때문"이 아니라, **단순한 확률적 빨려듦**이었습니다.

> 🤔 **비유（만담풍）**:
> 보케 "전원 100점인 반에서 반장을 선거했더니, 표가 갈려서 2명으로……"
> 츳코미 "그건 선거가 아니라 제비뽑기야!"
> ——진화에 일어난 것은, 바로 이 "제비뽑기화"입니다.

여기서 "유전적 부동（genetic drift）"이라는 말을 조금 정성껏. 생물학으로 말하면,
**선택압이 걸리지 않는 중립적인 유전자는, 세대를 거치는 사이 우연만으로 빈도가 치우쳐 간다**는 현상입니다.
작은 연못에 8색 금붕어를 풀어도, 아무도 먹히지 않으면, 몇 세대 후에는 **우연히 늘어난 2색**이
연못을 차지한다. 강했기 때문이 아니라, 주사위의 눈이 그렇게 굴렀을 뿐. 이번의 8→2는, 바로 이
"금붕어 뜨기 연못" 상태였습니다.

> 🤔 **비유（라쿠고풍）**:
> "핫쨩, 주사위 500번 던져서 제일 많이 나온 눈으로 대장 정하는 건 어떤가"
> "그건 실력이 아니지, 그냥 노름이올시다"
> "그렇지. 진화에 노름을 시킨 게, 이번 실패의 정체라네."

### 3.2 근본 원인: 평가 함수 `fitness_rich`의 이중 붕괴

왜 만점이 계속 나왔는가. 코드를 따라가 보니, `fitness_rich`（rich-proxy 평가기）에
**2개의 설계 결함**이 있었습니다.

**결함 1 — factor_affinity를 전 층 동일 값으로 했다**
genome은 본래 "사고 인자 × 메모리 층"의 2차원 행렬로 개성을 가져야 한다. 그런데
archetype 생성 시 `np.tile`로 **factor_affinity를 전 메모리 층에 같은 값으로 복제**하고
있었다. 층별 차이＝개성의 절반이, 평가에 들어가기 전에 붕괴되어 있었다.

**결함 2 — nearest를 `max(sims)`로 단일 스칼라로 붕괴시켰다**
개체와 archetype의 가까움을, 복수 archetype와의 유사도 벡터에서
**`argmax`（=최대값 1개만）**으로 꺼내고 있었다. "어느 천재와 가장 닮았는가"만
보고, "다른 천재와 어떻게 다른가"를 전부 버린다. 결과, 조금이라도
어느 하나에 닮으면 고득점 → **즉시 천장에 달라붙는다**.

```
본래 그래야 할: pressure profile = [전형성, 다양성, 전문성, ...] ← 복수 축 벡터
실제 구현:      fitness = max(개체와 각 archetype의 유사도)        ← 단일 스칼라
                          ↑ argmax로 붕괴 = 다목적성이 소멸
```

즉 **"복수의 잣대로 측정해야 할 것을, 1개의 잣대의 최대값만으로 채점했다"**.
안경(lleval)의 렌즈가 1장뿐이고, 게다가 즉시 만점으로 치솟는 거친 렌즈였다.

> 🍵 **휴식 포인트**: 여기가 본 글의 클라이맥스. "결과가 치우친" 것이 문제가 아니라,
> **"결과를 치우치게 한 원인이 평가 함수의 붕괴"**였다는, 이 2단 구조를 깨달으면
> 이 글은 다 읽은 것이나 마찬가지입니다. 나머지는 "그럼 어떻게 고치는가".

---

## 4. 대책 — "측정한다" 다음은 "도태한다": lldarwin

llive 패밀리에는 이미 **lleval（안경 = 평가 프레임워크, 연재 #24-08）**가
있습니다. 이번에 알게 된 것은, **안경으로 차이를 "측정할 수 있었다"고 해도, 그 차이를
"누가 살아남는가"로 올바르게 변환하지 않으면 진화는 망가진다**는 것.

그래서 새 멤버 **lldarwin（선택압 = 도태 컴포넌트）**를 설계했습니다.
ll- 패밀리의 역할 분담은 이렇게 됩니다:

```
lleval   = 측정한다  （개체의 행동을 복수 축의 pressure profile로 변환）
lldarwin = 도태한다  （그 profile을 "다음 세대의 부모"로 변환）
```

### 4.1 설계의 핵심 — "집약하지 않는" 선택압

이번 실패의 본질은 **"복수 축을 1 스칼라로 집약해서 argmax 했다"**는 것.
그래서 lldarwin의 제 1원칙은 **복수 선택압을 집약하지 않는 다목적 도태**입니다.

채용하는 3층 융합（rad-research로 evolutionary_computation 616건을 횡단하여 선정）:

1. **ε-lexicase 선택** — 평가 축을 하나씩 순서대로 독립 적용. 어떤 축에서 돌출한
   specialist（다른 축은 평범）도 살아남을 수 있다 → **다극 구조가 자동 유지된다**.
   그로텐디크가 "추상화 축"에서 1등이면, 설령 다른 축이 평범해도 사라지지 않는다.
2. **minimal-criterion QD (MAP-Elites)** — behavior 차원의 cell마다 elite를
   보유. **1 cell이라도 남으면 전멸하지 않는다**＝구조적으로 monoculture를 불가능화.
3. **down-sampling** — 매 세대, 평가 case의 부분 집합만 사용. 표적이 움직이므로
   특정 peak에 달라붙을 수 없다 → **plateau（만점 인플레）를 파괴**.

여기에 minimal-criterion gate（연속 순위가 아니라 "최저 기준을 충족하는가"로 번식 가부를
나눈다 = 일강 독식의 억제）와, per-dim z-score 표준화（"전 축 평균 높음"＝
무특징을 우위에 두지 않는다）를 더합니다.

### 4.2 "LLM의 약점"을 선택압으로 한다

또 하나의 방침은, **LLM/VLM이 현실에서 약하고, 또한 측정 가능한 축**을 pressure로
고르는 것（검증할 수 없는 영역은 피한다）. 예:

| pressure | LLM의 약점 | proxy/실 |
|---|---|---|
| typo_robustness | 오타・노이즈 입력에 대한 일관성 | proxy 가（합성 typo 주입） |
| polysemy_wsd | 다의어의 문맥 의존 이해 | proxy 가（WSD bench） |
| multistep_robustness | 다단 추론의 cascade error | proxy 가 |
| calibration | 신뢰도 추정（token confidence ≈ random） | proxy 가 |
| visual_qa | 이미지 인식・visual hallucination | 실 VLM 필수（Stage 후반） |

proxy로 측정 가능한 축부터 PoC, 실 LLM/VLM 축은 후단, 이라는 측정 순도의 분리도
처음부터 설계에 넣고 있습니다（[[feedback_llive_measurement_purity]]）.

### 4.3 전멸을 모니터한다 — SPC 알람

FullSense의 핵심 사상은 **SPC（통계적 공정 관리）**. lldarwin에서도
`max_lineage_share` / archive 성장 / behavioral diversity를 매 세대 기록하고,
**monoculture 비 > 0.8을 SPC_ALARM으로 검지**하여 cadence나 파라미터를
자동 조정합니다. 이번의 "8→2"를, 구조적으로 재발 불가능하게 하는 것이 목표입니다.

---

## 5. 교훈（honest disclosure로 남긴다）

- **비정상적으로 깔끔한 결과（best=1.0 즉시 포화, 2개 계통으로 수렴）는, 승리가 아니라 경보.**
  내역을 의심한 결과, 승자는 실력이 아니라 평가 함수의 결함이 낳은 환영이었다.
- **"측정한다"와 "도태한다"는 별개.** 안경(lleval)이 차이를 측정할 수 있어도, 그 차이를
  argmax로 1개로 붕괴시키면 도태는 망가진다. 도태기(lldarwin)는 집약해서는 안 된다.
- **실패를 지우지 않는다.** 이 500세대 run을 버리지 않고, lldarwin 배선 후에
  "오카 기요시・그로텐디크 등이 살아남는가"를 재실행으로 검증하는 **baseline**으로
  삼는다. 8→2가 개선되는지가 제 1의 합격 기준.

> **다음 예고**: lldarwin의 PoC Stage 0（proxy 축 + ε-lexicase 배선 + QD archive）을
> 구현해서, 같은 8 founder를 재실행한다. 이번에야말로 오카 기요시는 살아남을 수 있는가.
> "세계에 나와 프리스턴뿐"인 세계선을, 덮어쓰러 갑니다.
> （설계의 상세는 #26, 그 설계에 스스로 반증을 던지는 honest disclosure는 #27로 이어집니다.）

---

## 5.5. "안경"과 "도태기"의 2단 구조 — 왜 나누는가（심화）

본 글에서 가장 가져가 주었으면 하는 개념도가 이것입니다:

```
개체 ──▶ [ lleval = 안경 ] ──▶ pressure profile（복수 축의 case 벡터）
                                       │
                                       ▼
              [ lldarwin = 도태기 ] ──▶ 다음 세대의 부모
```

#25의 실패는, 이 2단의 **양쪽**이 망가져 있었던 데에 본질이 있습니다:

- **안경 측의 고장**: `fitness_rich`가 `nearest = max(sims)`로 복수 축을 1 스칼라로 붕괴시키고, 게다가 즉시 만점.
  → 측정하지 못하고 있다（차이가 보이지 않는 안경）.
- **도태기 측의 부재**: 애초에 집약하지 않는 다목적 도태（ε-lexicase / QD）가 **배선되어 있지 않았다**.
  → 도태할 수 없다（필터가 없다）.

중요한 것은 **어느 한쪽만 고쳐도 진화는 회복되지 않는다**는 것.
포화된 안경에 고급 도태기를 꽂아도 "차이 0"은 도태할 수 없고,
좋은 도태기가 없는 채 안경만 고쳐도 profile을 살릴 수 없다.
**"측정한다"와 "도태한다"는 다른 고장이고, 따로따로 고칠 필요가 있다** ——이것이 #25→#26의 다리 놓기입니다.
（"안경을 고치지 않고 도태기만 고급으로 해도 무익"하다는 반증은 #27에서 정면으로 다룹니다.）

> 🍵 **휴식 포인트**: 사진의 비유로 말하면, lleval은 "노출계", lldarwin은 "어느 컷을 채용할까".
> 노출계가 고장 나도 앨범은 못 만들고, 채용 기준이 없어도 앨범은 못 만든다. 양쪽 다 필요하다.

---

## 5.6. 도해 아이디어（투고 전 SVG화할 후보）

본 글을 "움직임으로 매료시키기" 위해 준비하고 싶은 그림（투고 전 SVG화）:

1. **계통 점유율의 붕괴 애니메** — 세대 축으로 8개 계통의 띠가 2개 계통으로 빨려드는 animated SVG（금붕어 연못 메타포）.
2. **best_score = 1.0 즉시 포화 그래프** — 제 1세대에 천장에 달라붙는 평탄선（선택압 0을 한눈에）.
3. **argmax 붕괴 도** — 복수 축 벡터 `[전형성, 다양성, 전문성, ...]`이 `max()`로 1개의 막대로 붕괴되는 before/after.
4. **2단 구조도** — §5.5의 "안경 → 도태기"를 hero 도로 animated화.
5. **ll- 패밀리 역할도** — lleval（측정）/ lldarwin（도태）/ llive（개체）의 관계를 1장으로.

> 이것들은 [[project_fullsense_animemd_branch_token_viz]]의 animated SVG 표현층（선언 애니메 → SMIL）에 실을 예정.

---

## 6. 관련

- 연재 #24-05「집단이 학습하는 AI」— 파생 집단 진화의 총괄（본 글의 전제）
- 연재 #24-08「안경을 만든다」— lleval（측정 측）
- 연재 #26「lldarwin의 설계」— 도태기의 다목적 도태 / ε-lexicase / QD（본 글의 속편）
- 연재 #27「안경이 흐려지면 도태도 무력」— 반증 조사・Goodhart's law（honest disclosure）
- 설계서: lldarwin（도태 측）— 본 글의 원천 소재
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(투고 전): hero SVG / theme SVG / 진행 badge / #24-05・#24-08・#26・#27의 Qiita URL cross-link -->
