---
title: lldarwin / 進化 arc 総集編 (#25–#34) — monoculture進化 / 選択圧lldarwin / 一晩で作り直し / 指揮者合奏 / 反証とGoodhart / 進化可視化 / Codex二本柱 / llcore CPU進化 × 第3の軸
tags: 解説, 進化計算, llive, FullSense, honest_disclosure
private: false
public_id: 6e107c7dfa0c261ee4d7
---

# lldarwin / 進化 arc 総集編 (#25–#34) — monoculture進化 / 選択圧lldarwin / 一晩で作り直し / 指揮者合奏 / 反証とGoodhart / 進化可視化 / Codex二本柱 / llcore CPU進化 × 第3の軸

> この記事は連載の **10 本を 1 記事に結合**したものです(**言語別構成**: 各言語で全章を連続して読めます)。

<!-- SERIESNAV -->
> **📚 FullSense 総集編シリーズ**(各記事は独立して読めます。横断で読む入口です)
> - [llcore 検証 arc 総集編 (#38–#42)](https://qiita.com/furuse-kazufumi/items/cc0713ab78a5b390df76)
> - [かみくだき総集編](https://qiita.com/furuse-kazufumi/items/bfb20aca3cf1df510c26)
> - [llive 完全解説 総集編 (0–8)](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
> - [llmesh 総集編](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762)
> - [lldarwin / 進化 arc 総集編 (#25–)](https://qiita.com/furuse-kazufumi/items/6e107c7dfa0c261ee4d7)
<!-- /SERIESNAV -->

**言語 / Language:** [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)


---

# 日本語


## 1. AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin

:::note info
**📚 FullSense ナレッジベースのご案内** <!-- fullsense-team-kb -->
FullSense 開発全史 60+ 記事 (4 言語版・物語ベースの読む順ガイド・かみくだき版・4 コマ漫画つき) は Qiita Team **FullSense KB** に集約しています (チームメンバー向け)。
:::

### AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin

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

#### 0. 三行であらすじ（落語でいう「枕」）

- **やったこと**: llive の派生集団進化に 8 人の知性をペルソナ種として投入、rich-proxy 評価で 500 世代回した。
- **起きたこと**: 1 世代目で best_score が **1.0 に張り付き**、以降ずっと満点。8 系統が **古瀬 52% / フリストン 48%** の 2 系統に収束、残り 6 人が絶滅。
- **真因**: 「満点が出続けた」＝**選択圧がゼロ**。誰を選んでも fitness は同じだから、進化は実質サイコロ振り（遺伝的浮動）になっていた。

要するに **「全員 100 点のテストで席次を決めようとした」**。そりゃ誰が
受かるかはくじ引きになります。テストが悪い。眼鏡(lleval)が曇っていた。

---

#### 1. なぜ「人物」を種として蒔いたのか

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

#### 2. 結果 — 生き残ったのは 2 人だけ

500 世代後の系統占有率（max_lineage_share の内訳）:

```
古瀬           ████████████████████████████  52%
フリストン     ██████████████████████████    48%
ミリッジ       (絶滅)
磯村           (絶滅)
岡潔           (絶滅)
グロタンディーク (絶滅)
フォン・ノイマン (絶滅)
ファインマン   (絶滅)
```

一見すると「予測符号化(Friston)と来歴志向(古瀬)が、抽象数学(グロタンディーク)や
形式計算(フォン・ノイマン)に勝った」という**物語**が書けそうです。

実際 SNS なら「AI 進化させたら予測符号化が最強だった」とバズるかもしれない。
**でも、それをやらないのが FullSense の honest disclosure ルール**です
（[[feedback_benchmark_honest_disclosure]]）。異常に綺麗な結果が出たら、
勝った気になる前に内訳を疑う。

疑った結果が、次節です。

---

#### 3. 真因 — 「満点インフレ」が選択圧を消した

##### 3.1 症状: best_score が 1 世代目から 1.0

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

##### 3.2 根本原因: 評価関数 `fitness_rich` の二重の潰れ

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

```
本来あるべき: pressure profile = [典型性, 多様性, 専門性, ...] ← 複数軸ベクトル
実際の実装:   fitness = max(個体と各archetypeの類似度)        ← 単一スカラー
                          ↑ argmax で潰す = 多目的性が消滅
```

つまり **「複数の物差しで測るべきものを、1 本の物差しの最大値だけで採点した」**。
眼鏡(lleval)のレンズが 1 枚しかなく、しかもすぐ満点に振り切れる粗いレンズだった。

> 🍵 **休憩ポイント**: ここが本記事の山場。「結果が偏った」のが問題なのではなく、
> **「結果を偏らせた原因が評価関数の潰れ」**だった、という二段構えに気づけば
> この記事は読了したも同然です。残りは「ではどう直すか」。

---

#### 4. 対策 — 「測る」の次は「淘汰する」: lldarwin

llive ファミリーには既に **lleval（眼鏡 = 評価フレームワーク, 連載 #24-08）**が
あります。今回わかったのは、**眼鏡で差を「測れた」としても、その差を
「誰が生き残るか」に正しく変換しないと進化は壊れる**ということ。

そこで新メンバー **lldarwin（選択圧 = 淘汰コンポーネント）**を設計しました。
ll- ファミリーの役割分担はこうなります:

```
lleval   = 測る  （個体の振る舞いを複数軸の pressure profile に変換）
lldarwin = 淘汰する（その profile を「次世代の親」に変換）
```

##### 4.1 設計の核 — 「集約しない」選択圧

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

##### 4.2 「LLM の苦手」を選択圧にする

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

##### 4.3 全滅をモニタする — SPC アラーム

FullSense の中核思想は **SPC（統計的工程管理）**。lldarwin でも
`max_lineage_share` / archive 成長 / behavioral diversity を毎世代記録し、
**monoculture 比 > 0.8 を SPC_ALARM で検知**して cadence やパラメータを
自動調整します。今回の「8→2」を、構造的に再発不可能にするのが目標です。

---

#### 5. 教訓（honest disclosure として残す）

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

#### 5.5. 「眼鏡」と「淘汰器」の 2 段構造 — なぜ分けるのか（深掘り）

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

#### 5.6. 図解アイデア（投稿前に SVG 化する候補）

本記事を「動きで魅せる」ために用意したい図（投稿前 SVG 化）:

1. **系統占有率の崩壊アニメ** — 世代軸で 8 系統の帯が 2 系統に吸い込まれる animated SVG（金魚の池メタファ）。
2. **best_score = 1.0 即飽和グラフ** — 第 1 世代で天井に張り付く平坦線（選択圧ゼロを一目で）。
3. **argmax 潰しの図** — 複数軸ベクトル `[典型性, 多様性, 専門性, ...]` が `max()` で 1 本の棒に潰れる before/after。
4. **2 段構造図** — §5.5 の「眼鏡 → 淘汰器」を hero 図として animated 化。
5. **ll- ファミリー役割図** — lleval（測る）/ lldarwin（淘汰する）/ llive（個体）の関係を 1 枚で。

> これらは [[project_fullsense_animemd_branch_token_viz]] の animated SVG 表現層（宣言アニメ → SMIL）に乗せる予定。

---

#### 6. 関連

- 連載 #24-05「集団が学ぶ AI」— 派生集団進化の総括（本記事の前提）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #26「lldarwin の設計」— 淘汰器の多目的淘汰 / ε-lexicase / QD（本記事の続き）
- 連載 #27「眼鏡が曇ると淘汰も無力」— 反証調査・Goodhart's law（honest disclosure）
- 設計書: lldarwin（淘汰する側）— 本記事の元ネタ
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #24-05・#24-08・#26・#27 の Qiita URL cross-link -->

---

## 2. 「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26（多目的淘汰 / ε-lexicase / 中立貯蔵庫 / 実 LLM 評価）

:::note info
**📚 FullSense ナレッジベースのご案内** <!-- fullsense-team-kb -->
FullSense 開発全史 60+ 記事 (4 言語版・物語ベースの読む順ガイド・かみくだき版・4 コマ漫画つき) は Qiita Team **FullSense KB** に集約しています (チームメンバー向け)。
:::

### 「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26

> **コンセプト hook**: 前作 #25 で、私は「AI を 500 世代進化させたら、世界に**私とフリストンだけ**が残った」という大失敗を晒しました。
> 岡潔もグロタンディークもフォン・ノイマンも、全員、進化の途中で静かに消えていった。原因は、評価関数（眼鏡 = lleval）が満点を出し続けて、**選択圧がゼロになった**こと。誰が優れているか「測れて」いても、その差を「誰が生き残るか」に変換できなければ、進化はただの遺伝的浮動に堕ちる。
>
> では——眼鏡で差を「測れた」として、その差を「淘汰」に**正しく変換する装置**はどう作るのか。
> それが今回の主役、**lldarwin**。ll- ファミリーの新メンバーで、**淘汰（選択圧）専門**のコンポーネントです。
>
> この記事で覚えてほしいキーワードは、たった一語。**「集約しない」**。複数の物差しを 1 本に足し算した瞬間、進化は壊れます。なぜそうなるのか、そしてどう実測でそれを乗り越えたのか——失敗の続きから、今度は**実際に動いた**話をします。

---

#### 0. 三行であらすじ（落語の「枕」）

落語には本題の前に「枕」があります。まずは三行で全体像を。

- **lleval が測り、lldarwin が淘汰する** — 進化は「測る」と「淘汰する」の 2 段構えで、初めて意味を持つ。
- 淘汰の第一原則は、**複数の選択圧を集約しない多目的淘汰**。#25 の失敗（単一スカラーの argmax で潰した）の真因を、ここで構造的に断つ。
- 採用三本柱 = **ε-lexicase + minimal-criterion QD + down-sampling**（evolutionary_computation コーパス 616 件を横断して選定）。

そして今回は骨子だけでなく、**実測がある**のが #25 との違いです。novelty pressure で行動多様性を 7.12 → 14.88（+109%）に倍増させ、**中立貯蔵庫**で「絶滅した岡潔・グロタンディーク系統」を実際に**全員復活**させ、最後は **on-prem の本物の LLM（llama3.2）**を相手に、prompt 戦略を進化させて苦手タスクを 0.0 → 1.0 に改善させた。順を追って見ていきます。

---

#### 1. なぜ「測る」と「淘汰する」を分けるのか

llive ファミリーには、すでに **lleval（眼鏡 = 評価フレームワーク、連載 #24-08）** があります。個体の振る舞いを観測し、複数の軸でスコア化する装置です。

ところが #25 でわかったのは、致命的な真実でした。**眼鏡で差を測れても、その差を argmax で 1 本に潰したら、淘汰が壊れる。** 具体的には、`fitness_rich` が複数の archetype 類似度を `nearest = max(sims)` という単一スカラーに畳んでいた。これが SEL-2 違反——「best=1.0 が飽和し、全員が満点になり、選択勾配が消える」真因です。

役割を明確に分けると、こうなります。

```
lleval   = 測る  （個体の振る舞いを「複数軸の pressure profile」に変換）
lldarwin = 淘汰する（その profile を「次世代の親」に変換）
```

`lleval` の出力は **case ベクトル**（各軸のスコアが並んだ配列）です。`lldarwin` はそれを入力契約として受け取り、**集約せずに**淘汰する。両者の責務境界はここにあります。lleval が「軸を 1 本に足し算してから」渡してきたら、lldarwin は何もできません。だから lleval 側には「breakdown（軸ごとの内訳）を必ず保持して渡す」ことを契約として課す。

lldarwin の `Pressure` インターフェースは、次の最小契約で表現されます。

- `name` — 軸の名前（`typo_robustness` 等）
- `evaluate(individual_output) -> case_scores: list[float]` — 個体の振る舞いを「軸ごとのスコア配列」に変換
- `is_proxy: bool` — proxy 測定か、実 LLM/VLM 測定か（測定純度の区別）
- `minimal_criterion: float | None` — その軸の最低繁殖基準（None なら gate なし）

ポイントは、`evaluate` の戻り値が**スカラーではなくリスト**であること。1 軸の中にも複数の case（テストケース）があり、それを潰さずに lldarwin へ流す。この「潰さない」設計が、後で specialist を救う伏線になります。

> 🍵 **休憩ポイント**: 眼鏡（lleval）とフィルター（lldarwin）を分ける意味は、写真でいう「露出を測る」と「どのカットを採用するか決める」の違いです。測光が完璧でも、ベストショットの選び方を間違えればアルバムは台無し。露出計（lleval）が「この一枚は明るさ 80 点、構図 30 点、表情 95 点」と教えてくれても、それを「平均 68 点」に丸めて捨てるか、「表情 95 点の一枚は別枠で残す」かで、アルバムの豊かさは天と地ほど変わる。lldarwin は「採用判断」の専門家です。測る人と選ぶ人を兼任させると、たいてい両方が雑になる。

---

#### 2. 設計の核 — 「集約しない」7 ステージ

lldarwin は、lleval から受け取った pressure profile（複数軸の case ベクトル）を、次の 7 ステージで淘汰します。それぞれに「なぜ必要か = どの失敗を防ぐか」を添えます。

1. **Standardizer** — per-dim z-score。「全軸が平均的に高い」だけの無特徴な優等生を優位にせず、各軸での**逸脱**を選択圧に変える。中央一致（みんなと同じ）は除外。
   - *防ぐ失敗*: 「平均点が高いだけ」の凡庸が勝ち、尖った個体が消える monoculture の入口。
2. **MinimalCriterionGate** — 各軸の最低基準で繁殖の可否を分ける。連続順位だけで「総取り」させない。
   - *防ぐ失敗*: 一強がすべての繁殖枠を独占する全滅シナリオ。基準を満たせば誰でも繁殖できる「最低保証」で多様性の土台を残す。
3. **EpsilonLexicaseSelection** — 軸を case として 1 つずつ独立に評価する。ある軸で突出した specialist（他軸は平凡）が生き残れる。
   - *防ぐ失敗*: 集約 argmax による specialist の絶滅。これが #25 の 8→2 を生んだ機構そのもの。
4. **QD / MAP-Elites archive** — pressure profile を behavior 記述子に変換し、cell ごとに elite を保持。archive は単調成長。
   - *防ぐ失敗*: 構造的な全滅。1 つの cell に 1 個体でも残れば、その振る舞いは消えない。
5. **Niching / FitnessSharing** — 同じ niche の個体を down-weight し、多峰を並存させる。
   - *防ぐ失敗*: 単峰への凝集（monoculture）。
6. **Down-sampling** — 毎世代、case の部分集合だけで評価して環境をかく乱する。
   - *防ぐ失敗*: 特定 peak への過適応と plateau（停滞高原）。moving target にすることで「同じ勝ち方」を許さない。
7. **NoveltyScorer** — 停滞時に「過去と違う振る舞い」へ探索圧をかける。
   - *防ぐ失敗*: 探索枯渇。改善が止まったとき、新規性そのものを報酬にして外へ押し出す。

#25 の 8→2 monoculture と対比すると、核は **(3) ε-lexicase・(4) QD archive・(2) minimal-criterion** の三つです。#25 では、これらがすべて欠けて単一スカラー argmax だけが回っていた。だから「平均的に最強な 1 系統」が連続順位を総取りし、残りが浮動で消えた。lldarwin はこの 3 つを「集約せずに束ねる」ことで、世代を重ねても破綻しない構造を作ります。

> 🤔 **たとえ話（漫才風）**:
> ボケ「テストの点を全部足して順位つけたら、平均点が高いだけの優等生ばっかり残ったわ」
> ツッコミ「それ多様性ゼロや! 数学だけ 100 点・他 0 点の天才が消えてるやんか!」
> ボケ「いや、トータルで見たら優等生のほうが上やし……」
> ツッコミ「**トータルで見るな!** 科目を 1 つずつ見たら、その天才は『数学』の case では誰にも負けへんのや。ε-lexicase はそれを救う仕組みやねん。足し算した瞬間に天才は死ぬ」
> ——足し算（集約）が specialist を殺す。ε-lexicase は「科目を 1 つずつ見る」から、尖った奴が残る。これが lldarwin の一丁目一番地です。

---

#### 3. なぜこの 3 本柱なのか（rad-research の裏付け）

「世代を重ねても破綻しない」最有力の融合案として、evolutionary_computation コーパス 616 件を横断して選定しました。自前で発明したのではなく、既存研究の「集約しない」系譜を選別して束ねた——という来歴が大事です。

| 手法 | 効能 | 出典 |
|---|---|---|
| **ε-lexicase** | specialist 保存・high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | cell 別 elite で全滅不可 | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | 環境かく乱・コスト削減 | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | 早期収束防止（将来オプション） | Lyu 2020 (2005.07376) |

三本柱はバラバラの手法に見えて、実は **「集約しない」という 1 つの思想**で串刺しにできます。ε-lexicase は「軸を集約しない」。QD は「振る舞い空間を集約しない（cell ごとに保持）」。down-sampling は「評価環境を固定しない（毎世代かく乱）」。どれも「1 本に丸めない」点で同じ哲学です。だから組み合わせても思想が衝突せず、相乗する。

> 🍵 **休憩ポイント**: 「なぜ自前で発明しないのか?」と訊かれます。答えは単純で、**既存研究の組合せで十分強いから**。私の開発ルール（[[feedback_originality_over_imitation]]）には「外部アルゴリズムの採用は網羅でなく**選別**。破綻リスクや単なる模倣は排除し、独自設計に価値を足すものだけ採る」とあります。lldarwin の独自性は「新しい選択アルゴリズムを発明したこと」ではなく、「これらを**集約せず束ねる束ね方**と、それを llive の進化ループに**実際に配線**したこと」にある。料理でいえば、世界初の食材を作るのではなく、既存の名食材を「混ぜずに一皿に盛りつける」技です。混ぜたら台無しになる素材を、混ぜずに共存させる。

---

#### 4. Stage1 — criteria 除外 + novelty pressure で行動多様性を倍にする

ここから実測です。Stage1 では、設計をいきなり全部実装するのではなく、最も効きそうな 2 つの変更だけを入れて測りました（llive, branch `optimize/core-2026-05-20`、commit `8060204`）。

**変更 1: criteria 除外。** ε-lexicase の case から、`factor_score`（= max-archetype の単一スカラー = argmax、まさに #25 の best=1.0 飽和の真因）と `nearest_persona_idx`（= 順序に意味のないカテゴリ index）を外しました。これは「悪い物差しを淘汰の判断材料から除く」掃除です。

**変更 2: novelty pressure。** `MultiPressureSelector(use_novelty=True)` を有効化。毎世代、過去世代の archive との k-NN 平均距離（Lehman-Stanley 流の novelty）を計算し、それを集団内で z-score 化（STD-1）して、追加の lexicase case として淘汰に混ぜます。「みんなと違う振る舞いをしている」こと自体を、軸の 1 つとして評価する。

テストは `tests/unit/test_evolutionary_lldarwin.py` を 8 → 10 件に拡張（除外・novelty 保存を追加）。進化系 847 件 green、回帰なし。

実測条件は rich-proxy、8 founders + pop24、150 世代、seed 0。結果が以下です。

##### 4.1 行動多様性 (diversity_l2) — novelty が効く指標

| 条件 | mean | tail30 min | final |
|---|---|---|---|
| BASELINE（除外前・Tournament 相当の旧 lldarwin） | 7.12 | 0.68 | 0.83（崩壊） |
| A: criteria 除外のみ | 9.16 | 1.57 | 1.57 |
| **B: 除外 + novelty** | **14.88（+109%）** | **6.56（9.6×）** | **11.73（崩壊回避）** |

novelty pressure は、行動（genome 空間）の多様性を約 2 倍に維持し、終盤の多様性崩壊を防ぎました。criteria 除外だけでも単独で効いている（spurious な argmax 圧を取り除いたぶん）。BASELINE は final 0.83 で**崩壊**しているのに対し、B 条件は final 11.73 で**踏みとどまっている**。これが「集約しない」設計の第一の手応えです。

![Stage1 baseline（novelty なし）の適応度と多様性。終盤に多様性が崩壊する](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg)

![Stage1 novelty あり。多様性が終盤まで維持される](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status.svg)

2 枚を並べると、終盤の挙動の違いが一目でわかります。baseline は多様性の曲線が床に張り付くのに対し、novelty ありは高い水準を保ったまま走り切る。

> 🍵 **休憩ポイント**: novelty pressure を金魚の池でたとえると——餌（高 fitness）に群がる金魚ばかり残すと、いずれ全員が同じ場所で同じ動きをする池になります。novelty pressure は「**みんなと違う場所を泳いでる金魚にもボーナス**」を出す係です。結果、池のあちこちに散らばった、見ていて飽きない池になる。ただしここで油断してはいけません。次の節で、この「賑やかな池」に潜んでいた**落とし穴**が見つかります。

---

#### 5. honest disclosure（最重要）— 行動多様性と系統生存を私は混同していた

ここが本記事で一番大事な節です。良い数字（+109%）が出たからといって、勝った気にならない——これは私の鉄則（[[feedback_benchmark_honest_disclosure]]）です。内訳を疑いました。そして、間違いを見つけました。

##### 5.1 系統固定 (founder_counts) — novelty では改善しない指標

同じ実測で、別の指標を見ます。「8 人の founder（祖先系統）のうち、何系統が最後まで生き残ったか」。

結果は——**全条件で最終的に 8 → 2 系統**（furuse-kazufumi + friston）に収束。oka-kiyoshi（岡潔）/ grothendieck（グロタンディーク）/ von-neumann / feynman / millidge / isomura は、**全部絶滅**。

novelty を入れて行動多様性を倍にしたのに、**系統の生き残りは #25 とまったく同じ 2 系統**だったのです。

##### 5.2 なぜか — 私は 2 つの「多様性」を混同していた

設計書（#25 時点）の TODO には「再ランで岡潔・グロタンディーク系統が生き残るか検証」とありました。これは、**行動多様性と系統生存を混同していた**のです。

`poc_evolution_env.py` の著者コメント（L129-132）が、この混同を正確に言い当てています。

> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs QD niching on lineage / PERSONA-FX, not pure novelty**"

噛み砕くと、こうです。

- 実証済の monoculture 0.05 は、**行動的**（archive-cell の占有率）であって、**系統的ではない**。novelty/lexicase が改善するのは「振る舞いの広がり」であって「祖先の生き残り」ではない。
- 系統固定が中立浮動（木村資生の中立進化説）によって monoculture に向かうのは、**理論的に正常**です。崩壊ではない。novelty も lexicase も、**既存個体を保存する**機構しか持たず、**いったん絶滅した系統を復活させる機構を持たない**。だから系統固定は構造的に止められない。
- さらに、archetype 間距離も 0.068〜0.29 と圧縮されていて（類似度が 0.71〜1.0 に密集）、選択勾配が弱く drift（浮動）が支配的。friston は最も非中心的（centroid 距離 0.162）なのに生き残った = 中心性（強さ）ではなく、**運（drift）**で 2 系統が固定したのです。

つまり——「岡潔・グロタンが生き残ってほしい」という私の願いは、**行動多様性を上げる薬では絶対に治らない病気**だった。薬を間違えていた。これは正直に記録する価値のある教訓です。

> 🍵 **休憩ポイント**: 漫才で言うなら。
> ボケ「池に色とりどりの動きをする金魚を増やしたで! 多様性バッチリや!」
> ツッコミ「で、**血統**は? 8 つあった金魚の家系、いくつ残ってんの?」
> ボケ「……2 つや」
> ツッコミ「動きは派手やのに家系図はスカスカやないか! 動きの多様性と血統の多様性は**別の話**やぞ!」
> ——「行動が多様」と「系統が多様」は、見た目が似ているだけのまったく別の指標。私はこれを混同していました。正直に晒します。

---

#### 6. Stage1.5 — 中立貯蔵庫で絶滅した系統を蘇らせる

病気の正体がわかれば、薬を変えられます。系統生存に必要なのは「絶滅した系統を毎世代 re-inject する機構」——**lineage-niched 中立貯蔵庫（reservoir）**です。

##### 6.1 まず PoC で機構を確かめる

いきなり本番ループを改造せず、まず standalone PoC で機構が回ることを確かめました（[[feedback_poc_feasibility_first]] = 要件 → PoC → フィジビリティ → 詳細設計、llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`）。

selection は Stage1 の `MultiPressureSelector`（criteria 除外 + novelty）を流用。fitness は rich-proxy。系統は parent_a から継承。**reservoir = 系統別の best-ever genome を保持し、絶滅した系統を毎世代 re-inject する**（低 score の子を置き換える。best は壊さない）。8 founders + pop24 + 150 gens + seed 0 で測りました。

| reservoir | 最終 named 系統 | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1**（oka-kiyoshi 24/24 = 完全 monoculture） | 1.00 | 1.58 |
| **ON** | **8（全 founder 生存）** | **0.31（≪ 0.8 OE-3）** | 1.69 |

reservoir ON で、岡潔（oka）・グロタンディーク（grothendieck）を含む**全 8 系統が生存**。最終 shares は friston 7 / furuse 6 / grothendieck 4 / oka 3 / 他 4 系統各 1。**強い系統は子孫を持って繁殖し、弱い系統は貯蔵庫が生命維持する**という、理想的な挙動です。行動多様性も低下なし（1.69 vs OFF 1.58）。

**Honest 留保（PoC 段階）**: 貯蔵庫は frozen elite（凍結された代表）を再投入するので、弱系統（各 1 体）の「生存」は再投入由来であって、能動的進化ではありません。これは中立貯蔵庫の定義どおり（代表を保持し、再結合可能にする）で正当ですが、「弱系統が活発に進化し続ける」とは主張しません。

##### 6.2 本番 EvolutionLoop へ組込（additive + default-off）

PoC で機構が確かめられたので、本番の `EvolutionLoop` に組み込みました（commit `b03cbda`）。設計の肝は **additive かつ default-off**——既存の挙動を一切変えず、フラグを立てたときだけ有効になる。後方互換を死守しました。

- `EvolutionLoop.on_population_bred` hook を追加（breed 直後・評価前に bred リストを変換できる。既定 None = 後方互換）。
- `LineageReservoir`（`lineage_reservoir.py`）: 祖先追跡（parent_ids[0] を継承）+ 系統別 best-ever 保持 + 絶滅保護系統の re-inject。`founder_map` を共有し系統ログとも整合。
- `run_persona_evolution(lineage_reservoir=True)` / run スクリプト `--lineage-reservoir` を追加。
- tests: `test_evolutionary_lineage_reservoir.py` 6 件 + 進化系 **937 green**（回帰なし）。

実 EvolutionLoop での実測（rich-proxy + lldarwin + novelty, 8 founders / pop24 / 150gens / seed0）。

| 条件 | named 系統生存 | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8（furuse 17 + friston 7） | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8（全系統）** | **0.33** | **0.29（≪ 0.8 OE-3）** | 9.20 |

岡潔（oka 3）・グロタンディーク（grothendieck 1）を含む**全 8 系統が、実ループで生存**しました。PoC の予測（fixation 0.31）を、本番実装が 0.29 で再現した——機構が設計どおり動いた証拠です。

これが、本記事最大の見せ場です。下の 2 枚を見比べてください。

![中立貯蔵庫 OFF。系統支配ストリームが最終的に furuse 71% / friston 29% の 2 系統に崩壊する](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

![中立貯蔵庫 ON。全 8 系統（millidge / von-neumann / oka / grothendieck 等）が並存する](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

OFF（上）は、世代が進むにつれてストリームが 2 色に呑み込まれていく——「私と friston だけが残った」#25 の再現です。ON（下）は、8 色が最後まで帯として残る。岡潔もグロタンディークも、消えていない。

![中立貯蔵庫 ON の適応度と多様性](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_status.svg)

> 🍵 **休憩ポイント**: #25 で「私とフリストンだけが残った」と嘆いた、あの寂しい世界。それが今度は岡潔もグロタンディークもフォン・ノイマンも全員いる、賑やかな世界に変わりました。**これは捏造ではなく、実際に動いた結果です**（[[feedback_benchmark_honest_disclosure]] に従い、虚偽の失敗も虚偽の成功も書きません）。ただし——浮かれる前に、§5 で学んだ姿勢を思い出しましょう。「いい数字が出たら内訳を疑う」。次の §6.3 で、この成功にも**代償**があったことを正直に書きます。

##### 6.3 Honest 留保 — 系統保持と行動多様性は弱いトレードオフ

reservoir ON で系統は全員生き残りました。が、よく見ると **diversity_l2 は 14.88 → 9.20 に低下**しています。frozen elite（凍結代表）を毎世代再投入するぶん、genome 空間の広がりがやや減るのです。

ただし、OFF 時の崩壊（final 0.83）は回避しています。つまり「系統保持を取ると、行動多様性のピークは少し下がるが、崩壊は防げる」という**弱いトレードオフ**の関係です。代償ゼロの魔法ではない。これを正直に書いておきます。そして、この代償をどこまで小さくできるかが、次の sweep の主題になります。

---

#### 7. 再投入頻度 sweep — 非単調な最適点という非自明な発見

§6.3 の honest 留保（frozen elite 再投入で diversity が下がる）を、`reinject_interval`（再投入を行う世代間隔。既定 1 = 毎世代）の sweep で特性化しました（commit `da93dd3`）。`LineageReservoir.reinject_interval` + `--reinject-interval` フラグを追加（test 7 件）。8 founders / pop24 / 150gens / seed0。

| interval | named 生存 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**（毎世代） | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84（最大）** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**ここで非自明な発見がありました。** 直感的には「再投入を減らす（interval を上げる）ほど、frozen elite の押し込みが減って diversity が単調に回復する」と予想しますよね。ところが——**diversity は単調増加せず、interval=5 でピーク**を打ち、10/20 ではむしろ低下したのです。

理由を考えると腑に落ちます。系統を放置しすぎる（interval が大きすぎる）と、(a) 貯蔵庫由来の多様性注入が減り、(b) 少数系統が固定してしまって、結局 diversity も伸びない。「再投入しすぎ」も「放置しすぎ」も両方ダメで、中間に最適点がある。これは**実際に sweep を回さなければ予測できなかった**知見です。

運用指針はこうなりました。

- **系統保持を最優先**するなら → interval=1（8/8 全系統生存）。
- **行動多様性も両立**させたいなら → interval=5（5/8 を保持しつつ diversity 最大）。

両立の最適点は fitness の設計や集団規模に依存するので、本番では sweep で再較正します。

![再投入頻度のトレードオフ。系統保持と行動多様性は反比例し、diversity は interval=5 でピークを打つ（非単調）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep.svg)

> 🍵 **休憩ポイント**: 落語のサゲ（オチ）のように、ここには「予想を裏切る転」があります。「やればやるほど良い」と思っていたら、「やりすぎると逆効果」だった。植物の水やりと同じで、あげなさすぎても枯れるし、あげすぎても根腐れする。中庸に最適点がある。進化計算をやっていると、こういう「単調じゃない曲線」に何度も出会います。だからベースラインを測り、sweep を回す。直感は、よく裏切られる。

---

#### 8. Stage2 前半 — 「LLM の苦手」を proxy で選択圧にする

ここまでは rich-proxy（persona 類似度ベースの heuristic）で機構を確かめてきました。次は設計のもう 1 つの柱、**「LLM/VLM が現実に弱く、かつ測定可能な軸」を pressure にする**を実装します（commit の系列、`pressures.py`）。

設計 §3 で挙げた proxy 可能な 5 軸を plugin 化しました。

| pressure（LLM 弱点） | 関連思考因子（case） |
|---|---|
| typo_robustness（ノイズ耐性） | consistency / reality_link / uncertainty |
| polysemy_wsd（多義語） | multiview / consistency / reality_link |
| multistep_robustness（多段推論） | structurize / closed_loop / self_extend |
| calibration（信頼度推定） | uncertainty / provenance |
| context_management（無関係文脈耐性） | consistency / provenance / recompose |

`make_pressure_fitness()` が各 pressure の case（計 14）を breakdown に出力し、lldarwin の ε-lexicase が**集約せず軸ごとに specialist を淘汰**します。`--fitness pressure-proxy` を追加。tests `test_evolutionary_pressures.py` 4 件 + 進化系 **942 green**。

end-to-end の実測（pressure-proxy + lldarwin + novelty + reservoir, 8 founders / 120gens）: named 系統 **8/8 生存** / lineage_fixation (tail) 0.67 / diversity_l2 (tail) **17.91**。14 個の苦手軸 case が独立に淘汰され、行動多様性は高い。系統は reservoir が維持しています（pressure-proxy は persona の同一性を直接報酬化しないため、優占系統の share は rich-proxy の 0.29 より高い 0.67 になります）。

![5 苦手軸（typo / polysemy / multistep / calibration / context）の母集団平均推移（proxy 測定）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes.svg)

**Honest 留保（設計 §7 / §7.1 に明記済の受容済み限界）**: 個体は実 LLM ではなく genome（llive 構成）です。本 pressure が測るのは「genome がその弱点に**関連する思考因子**をどれだけ備えるか」という**振る舞いの代理**であって、**production の LLM 能力ではありません**。これは **mechanism feasibility（機構が回ること）の検証**に限定されます。Goodhart リスク（proxy をハックする表面戦略が進化する）も受容済みの限界です。実 LLM/VLM の苦手軸の実測は、Stage2 後半（OLLAMA_HOST 設定 + 個体→実 LLM 写像が前提）に持ち越します。

> 🍵 **休憩ポイント**: ここは誤解されやすいので、念押しします。「LLM の苦手を進化で克服した!」とは**まだ言っていません**。proxy が測っているのは「機構が回るか」だけ。本物の LLM がタイポに強くなったかどうかは、この段階では一切わからない。proxy で派手な数字（17.91）が出ても、それは「装置が動く」証明であって「中身が賢くなった」証明ではない。この線引きを曖昧にした瞬間、研究は嘘になります。だから次に、**本物の LLM**を相手にします。

---

#### 9. Stage2 後半 — 本物の on-prem LLM を相手に prompt 戦略を進化させる

localhost の ollama（llama3.2:latest 等）が到達可能とわかったので、ついに**実 LLM 評価**が可能になりました（commit `2fb2912`）。localhost = on-prem なので、measurement purity（測定純度。cloud LLM と混在させない）の規律も満たします（[[feedback_llive_measurement_purity]]）。

##### 9.1 個体 → 実 LLM への写像（Promptbreeder 系）

肝は「genome を、どうやって実 LLM に効かせるか」です。`real_pressures.py` で **個体 → 実 LLM 写像**を実装しました。

- **個体の `c_prompt`（PromptChromosome）を system prompt に変換**: skill_set → 指示文 / prompt_template_id → 推論スタイル / language_style → 語調。固定の LLM（llama3.2）にこの system prompt を被せ、5 苦手軸の**実タスク**を解かせて採点します。
- **LLM 本体は固定し、prompt 戦略（genome）を進化させる** = 「どの prompt 戦略が LLM の弱点を緩和するか」を実測で淘汰する。これは Promptbreeder（prompt を進化的に最適化する研究系列）の流儀です。
- temp=0（greedy）で決定論的に。`(system_prompt, task)` をキャッシュ（同一戦略は再評価しない）。
- robust: per-call try/except（ollama の hiccup は task の失点として扱い、走行は継続）。
- `--fitness real-pressure` / `--ollama-model` / `--max-wallclock-seconds` を追加。tests 5 件 + 進化系 947 green。

##### 9.2 実選択信号の実証 — CoT+structure 戦略が multistep を 0.0 → 1.0 に

そして、本物の選択信号が観測できました。

**CoT+structure 戦略**（`chain_of_thought` + structurize + loop）が、llama3.2 の **multistep（多段推論）を 0.0 → 1.0 に改善**しました（terse な戦略は 0.0 で失敗。score は 0.80 → 1.00 に上昇）。

これは、lldarwin の主張「prompt 戦略の進化で LLM の弱点を緩和できる」を、**proxy ではなく実 LLM で実証**したことを意味します。同じ llama3.2 本体でも、被せる system prompt（= 進化した genome）次第で、多段推論タスクが解けたり解けなかったりする。進化は「解ける prompt 戦略」を実際に選び取ったのです。

![5 苦手軸の母集団平均推移（実 on-prem LLM llama3.2 評価）。prompt 戦略の進化で軸が改善する](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

##### 9.3 12h 連続ラン

実 LLM 評価は重いので、長時間の連続ランを起動しました（`out/lldarwin_12h_realpressure_2026_05_26/`）。

```
--fitness real-pressure --selection lldarwin --novelty --lineage-reservoir
--genome3d --population 24 --max-wallclock-seconds 43200 --checkpoint-every 5
```

wallclock 12h で safely 停止（snapshot 済 → `--resume` で継続可能）。連続ランの中で best_score=1.0 に到達しています。

![実 LLM 進化ランの適応度と多様性（12h 連続ラン）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status.svg)

##### 9.4 Honest 留保（実 LLM 評価の限界）

ここが #25 から学んだ姿勢の総決算です。派手な結果（0.0 → 1.0、best 1.0）が出たからこそ、内訳を徹底的に正直に書きます。

- **(a) fitness に関与するのは `c_prompt` だけ。** persona / c_factors は中立（系統は reservoir で維持、初期選択は novelty が担う）。つまりこれは「**prompt 戦略の進化**」であって「persona の進化」ではありません。岡潔の人格が賢くなったのではなく、岡潔という系統に紐づいた prompt 戦略が選ばれた、という話。
- **(b) 全 founder の初期 c_prompt は同一（default）。** だから探索は mutation 駆動です（founder ごとに prompt を多様化させるのは今後の改善）。スタート地点が同じなので、初期の系統差は prompt 戦略には効いていない。
- **(c) 小バッテリ（軸あたり 2 問）= ノイジーな推定。** 0.0 → 1.0 という劇的な数字も、問題数が少ないぶんノイズを含みます。統計的に堅牢な主張をするには、もっと大きなバッテリが要る。
- **(d) on-prem only（measurement purity）。一般能力の主張ではない。** llama3.2 という特定モデル・特定タスクでの観測であって、「LLM 一般がこうなる」とは言いません。

これらを伏せれば「進化で LLM が劇的に賢くなった!」という派手な物語が書けますが、それは嘘です。lldarwin が実証したのは「**機構が、実 LLM 上で、選択信号を生む**」というところまで。その線を越えた主張はしません。

> 🍵 **休憩ポイント**: 研究で一番気持ちいいのは「0.0 が 1.0 になった!」と叫ぶ瞬間です。でも、その瞬間こそ [[feedback_benchmark_honest_disclosure]] が効いてくる。「変に良い数字が出たら、勝った気になる前に内訳を疑え」。今回でいえば——勝ったのは「prompt 戦略」であって「LLM 本体」でも「persona」でもない。問題数も少ない。on-prem の 1 モデルだけ。これを全部書いてから、初めて「実証した」と言える。honest disclosure は、自慢を我慢する筋トレです。

---

#### 10. 既存資産の再利用（codex コード調査ベース）

設計を絵に描いた餅にしないため、配下の Codex に既存コードを調査させたところ、**多くは実装済・未配線**でした。

- `mating.py:139 LexicaseSelection`（ε 付き、実装済だが未配線 → 配線するだけ）
- `nsga2.py:197 NSGA2Selection`（≤3 目的レーン用）
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**新規実装**: `Standardizer` / `MinimalCriterionGate` / `Pressure` 群 / `MultiPressureSelector`（中核）/ `LineageReservoir`（Stage1.5）/ `SelectionAudit`。
**配線点**: `loop.py:122` の `selection` に `MultiPressureSelector` を注入、`persona_evolution.py:606` に注入口を追加、`EvolutionLoop.on_population_bred` hook に `LineageReservoir` を接続。

> 🍵 **休憩ポイント**: 「実装済だが未配線」が一番多かったのが、最大の教訓でした。良い部品を作っても、**配線（オーケストレーション）しなければ進化は壊れたまま**。#25 で 8→2 になったのは、ε-lexicase も NoveltyScorer も QD も「箱の中にあったのに、配線されていなかった」から。lldarwin の本質は、新規アルゴリズムの発明よりも、「既存の良い部品を**集約せず**束ねて、進化ループに**実際に配線する**こと」にあります。電子部品を全部揃えても、半田付けしなければラジオは鳴らない。

---

#### 11. 破綻回避の保証 — 全滅しない多層構造（実測で裏付け済）

#25 の monoculture（8→2）を反証する多層構造は、設計どおりに揃い、しかも今回は**実測で裏付けられました**。

1. **MinimalCriterionGate** — 最低基準で繁殖可否 → 一強総取りを抑制。
2. **QD cell 別 elite** — 1 cell でも残れば系統全滅不可（archive 単調成長）。
3. **Niching / FitnessSharing** — 同 niche を down-weight → 多峰並存。
4. **Down-sampling** — moving target で plateau 破壊。
5. **per-dim z-score + 中央一致除外** — 無特徴を優位にしない。
6. **LineageReservoir（Stage1.5 で追加）** — 絶滅系統の中立貯蔵庫 → 系統全滅を構造的に阻止（実測で 8/8 生存）。
7. **monoculture モニタ + SPC** — max_lineage_share を毎世代記録、>0.8 を SPC_ALARM で検知 → 自動調整。

特に (6) は、§5 の honest disclosure（novelty では系統固定を止められない）を受けて**後から追加した層**です。設計の穴を実測で見つけ、塞いだ。実測の lineage_fixation は OFF 0.70 → ON 0.29 と、OE-3 基準（<0.8）を大きく下回ります。「集約しない」+「絶滅系統を蘇らせる」の二段構えで、#25 を構造的に潰せたのが本記事の到達点です。

---

#### 12. honest disclosure / リスク（前振り）

設計を盲信しません。受容済みの限界（次作 #27 で深掘り）を、もう一度まとめておきます。

- **Goodhart's law / proxy 乖離** — LLM 弱点を proxy fitness にすると、「指標をハックする表面戦略」が進化する（typo → 特定置換の暗記、WSD → テストのヒューリスティクス利用、等）。proxy は mechanism feasibility に限定し、production 能力を主張しない。
- **設計者依存性** — lexicase=case / QD=記述子 / novelty=距離尺度、いずれも「多様性の方向」を設計者が決める。生物進化級の未想定創発は限定的。
- **minimal-criterion の停滞⇄崩壊トレードオフ** / **QD の次元の呪い + アーカイブ飽和**。
- **実 LLM 評価の限界（§9.4 再掲）** — c_prompt のみ fitness 関与・founder 初期 prompt 同一・小バッテリ・on-prem only。

> **次回予告（#27）**: 「眼鏡が飽和すると選択圧は無力」という最も痛い反証を、Goodhart's law と proxy fitness の限界とともに正直に晒します。lldarwin は万能ではない。**どこまで主張してよいか**の線引きが #27 の主題です。今回「8/8 生存」「0.0→1.0」という良い数字が出たからこそ、次は徹底的に反証で鍛えます。

---

#### 13. 結論

- 進化は「**測る（lleval）**」と「**淘汰する（lldarwin）**」の 2 段構え。淘汰の核は **「集約しない」**。
- Stage1: criteria 除外 + novelty pressure で、行動多様性を 7.12 → 14.88（+109%）に倍増し、終盤の崩壊を回避した。
- honest disclosure: novelty/lexicase は**行動多様性**は保つが、**系統固定**は中立浮動（Kimura）で monoculture に向かう。私は 2 つの多様性を混同していた——正直に記録。
- Stage1.5: lineage-niched **中立貯蔵庫**で、実 EvolutionLoop において **OFF=2 系統 / ON=全 8 系統生存**（岡潔・グロタンディーク含む）、lineage_fixation 0.29（≪0.8）を実現。**これは捏造ではなく実際に動いた**。
- 再投入頻度 sweep: 系統保持↔行動多様性のトレードオフ。diversity は interval=5 でピーク（**非単調**）という非自明な知見。
- Stage2 前半（proxy）: 5 苦手軸を Pressure plugin 化（mechanism feasibility のみ）。
- Stage2 後半（実 LLM）: 個体 c_prompt → system prompt 写像で固定 on-prem LLM（llama3.2）を実タスク採点。**CoT+structure 戦略が multistep を 0.0 → 1.0 に改善**。12h 連続ランで best=1.0 到達。
- 楽観せず、勝った気にならず、内訳を分けて報告した（[[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]]）。

良い部品を作るだけでは進化は壊れたまま。**集約せずに束ね、実際に配線し、絶滅した系統を蘇らせ、本物の LLM で選択信号を確かめる**——そこまでやって、ようやく #25 の「私とフリストンだけ」の世界を、岡潔もグロタンディークもいる賑やかな世界に変えられました。次の #27 では、この成功にどこまで信を置いてよいかを、反証で問い直します。

---

#### 14. 関連

- 連載 #25「私とフリストンだけが残った」— 本記事の動機（失敗の記録）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #27「眼鏡が曇ると淘汰も無力」— 反証調査（honest disclosure）
- 設計書: lldarwin（淘汰する側）`docs/vision/LLDARWIN_DESIGN.md`
- 実測正本: `docs/research/lldarwin_stage1_results_2026_05_26.md`
- llive commits: Stage1=`8060204` / 中立貯蔵庫 PoC=`0d0537d` / Stage1.5=`b03cbda` / reinject sweep=`da93dd3` / Stage2 実 LLM=`2fb2912`
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]] / [[feedback_poc_feasibility_first]]

---

## 3. 一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27（開放端進化 / ライブ・オーケストラ / honest cross-validation）

:::note info
**📚 FullSense ナレッジベースのご案内** <!-- fullsense-team-kb -->
FullSense 開発全史 60+ 記事 (4 言語版・物語ベースの読む順ガイド・かみくだき版・4 コマ漫画つき) は Qiita Team **FullSense KB** に集約しています (チームメンバー向け)。
:::

### 一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27

> 📚 **連載ナビ（lldarwin アーク）**: #24-05 集団進化 → #25 monoculture の失敗 → #26 設計編 → **#27 本記事（climax）** → [#28 実装編（オーケストラ型 AI）](drafts/QIITA_#28_lldarwin_v2_phase1_orchestra.md)。※ 各記事は単独でも読めます（リンクは回遊用）。

> **コンセプト hook**: 前作 #25 で、私は「AI を 500 世代進化させたら、世界に**私とフリストンだけ**が
> 残った」という大失敗を晒しました。原因は、評価関数（眼鏡 = lleval）が満点を出し続けて、
> **選択圧がゼロになった**こと。
>
> 「では今度こそ、本物の LLM で確かめよう」——そう思って、on-prem の llama3.2 を相手に
> **12 時間ぶっ通しで進化**させました。proxy（合成のものさし）ではなく、実 LLM です。
>
> 結果。**gen5 で満点に張り付き、そこから 65 世代、ピクリとも進歩しませんでした。**
> 全滅はしない。でも累積もしない。これは進化ではなく、**ただの「ふるい付きランダムサーチ」**
> だった——proxy だけでなく、**実 LLM でも、まだ進化になっていなかった**のです。
>
> そこから一晩。私は「方策を決める」ために、自分で 6 本の PoC を回し、4 体の Claude Agent を
> 並列で走らせ、Perplexity に文献を漁らせました。そして朝、**全員が独立に、同じ結論へ収束**
> していた。これは、その「徹夜の意思決定ログ」の honest disclosure です。

---

#### 0. 三行であらすじ（落語でいう「枕」）

落語には本題の前に「枕」があります。まずは三行で。

- **また飽和した** — 実 LLM(llama3.2) で 12h 回したら、gen5 で best=1.0 に張り付き、65 世代無進歩。全滅はしないが累積もしない＝**filtered random search**。真因は #25 と同じ「固定の人手ものさしの飽和」。
- **一晩で方策を決めた** — 自己 PoC 6 本 + 並列 Agent 4 体 + Perplexity が、**独立に同じ結論**へ収束。「ものさしを固定したまま淘汰器を磨いても無駄。**評価そのものを開放端化せよ**」。
- **独自性が見えた** — 連続進化する集団を、止めずに任意の瞬間に合奏（MoA）させて 1 答する「**ライブ・オーケストラ**」が、先行研究の white-space（空白地帯）だと判明した。

要するに **「眼鏡（評価）が飽和したら、淘汰器（lldarwin）をどれだけ磨いても無力」**。
だから磨く対象を変える——**評価そのものを開放端にする**、が今回の結論です。

---

#### 1. なぜ「また」やったのか — #25 / #26(設計) の続き

ここまでの連載を 3 行で振り返ります。

- **#24-05**「集団が学ぶ AI」— 1 個の LLM を賢くするのではなく、**N 個の llive 個体（genome）を世代交代させて互いに評価し合う**派生集団進化、という枠組みを立てた。
- **#25**「私とフリストンだけが残った」— その集団に 8 人の知性をペルソナ種として蒔き、proxy 500 世代で回したら、**満点飽和 → 選択圧ゼロ → 運（遺伝的浮動）だけで 2 系統に偏る**大失敗。眼鏡が曇っていた。
- **#26(設計編)**「眼鏡で測るだけでは進化しない」— 淘汰器 **lldarwin** を設計し、「集約しない多目的淘汰（ε-lexicase / QD / 中立貯蔵庫）」を実装。proxy では系統絶滅を防げた。

ここまでは全部 **proxy（決定論 heuristic、LLM 非依存）**での話でした。proxy は「機構が回ること」は示せても、「進化が**意味あるもの**を見つけた」ことは示せません（[[feedback_benchmark_honest_disclosure]]）。

だから、当然の次の一手。**本物の LLM で確かめる。**

localhost の ollama（llama3.2:latest）が到達可能だったので、個体の `c_prompt`（prompt 戦略の遺伝子）を system prompt に変換し、固定の llama3.2 に被せて実タスクを解かせる——**Promptbreeder 系の写像**で、12 時間の連続進化ランを起動しました。これが本記事の出発点です。

> 🍵 **休憩ポイント**: ここまでで「proxy では機構が回った。じゃあ本物の LLM では?」という
> 問いが立てば OK。研究のいいところは、この「じゃあ本物では?」を実際に回せること。
> そして今回、本物は——容赦なかった。

---

#### 2. 出発点 — 実 LLM 12h ランの「正直な不合格」

12 時間の実 LLM 進化ラン（on-prem llama3.2、measurement purity 厳守＝cloud LLM と混在させない、[[feedback_llive_measurement_purity]]）の結果が、これです。

| 事実 | 値 | 含意 |
|---|---|---|
| 完走 | 71 世代 / 12h（≒10.3 分/世代、実 LLM 逐次） | スループットが律速 |
| best_score | **gen5 で 1.0 → gen70 まで固定** | **目的飽和。65 世代が無進歩** |
| mean | 0.85 で頭打ち、1.0 戦略が席巻しない | **適応が蓄積しない** |
| 軸別 | 10 問中 6-7 問が飽和、勾配は multistep（2 問）のみ | 実効解像度が小さすぎ |
| fitness 依存 | **c_prompt のみ**。c_factors(40 次元)/c_impl/c_meta は中立浮動 | **43 次元が選択圧ゼロ** |
| 集団健全性 | pop=24 維持・min ≥ 0.70・**全滅せず** | 機構（GA）は壊れていない |

ここで踏みとどまるのが、FullSense の honest disclosure ルールです（[[feedback_benchmark_honest_disclosure]]）。「全滅しなかった！ best=1.0 に到達した！」と書けば、いかにも成功っぽい。でも内訳を見れば一目瞭然です。

**判定: 全滅はしていないが、累積進化になっていない（≒ filtered random search）。**

10 問のテストのうち、勾配（差）が残っているのは multistep の 2 問だけ。残り 8 問は早々に全員満点。つまり 10 問中 8 問は、もはや誰を選んでも同じ。選択圧の実効解像度が、ほぼ 2 問分しか残っていない。しかも fitness に関与するのは 4 つの染色体のうち `c_prompt` ただ 1 つで、残り 43 次元（思考因子 40 次元 + 実装 + メタ）は**選択圧ゼロの中立浮動**。

![実 on-prem LLM（llama3.2）進化ランの適応度と多様性（12h 連続ラン）。best は早々に天井に張り付き、以降は平坦](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status.svg)

![5 苦手軸（typo / polysemy / multistep / calibration / context）の母集団平均推移（実 on-prem LLM 評価）。multistep 以外は早期に飽和し、勾配が残らない](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

**真因 = 人手の固定ものさしの飽和。** #25 でユーザーが言語化した洞察「**眼鏡が飽和すると、選択圧は無力**」を、今度は proxy ではなく**実 LLM で実証**してしまった、という構図です。眼鏡を proxy から実 LLM に替えても、**ものさしが「固定の 10 問」である限り、すぐ満点で飽和する**。レンズのメーカーを替えても、目盛りが粗ければ同じ。

> 🤔 **たとえ話**: 採点者を「本物の先生（実 LLM）」に替えても、出す問題が毎回同じなら、
> 数回で全員が満点を取り、以降は何回テストしても差がつきません。問題が悪いのではなく、
> **問題用紙が固定で簡単すぎる**のです。採点者（眼鏡）を proxy から実 LLM に交換しても、
> ものさし（問題）が固定なら飽和する。これが「正直な不合格」の正体です。

> 🍵 **休憩ポイント**: ここで多くの人は「実 LLM でも飽和なら、もう詰みでは?」と思います。
> 私もそう思いました。でも、ここからが本題。**「ものさしを固定したのが間違い」**だとしたら、
> 直すべきは淘汰器でも LLM でもなく、**ものさしの作り方そのもの**です。それを一晩かけて、
> 6 本の PoC と 4 体の Agent と Perplexity で確かめました。

---

#### 3. 一晩の作戦 — 「方策を決める」ための分散調査

ユーザーから来た指示は、こうでした。

> 「徹底的に要件を整理して、もっと進化型として独自性を出す。PoC も何度も繰り返す。
> 明日の朝までずっと小さい単位で PoC をしまくって**方策を決める**。」

ここで重要なのは、**「実装を完成させる」ではなく「方策を決める」**が目的だったこと。だから、大きな本番ランを 1 本回すのではなく、**小さい PoC を大量に**回して、設計判断を 1 つずつ実データで潰していく、という作戦を取りました（[[feedback_poc_feasibility_first]] = 要件 → PoC → フィジビリティ → 詳細設計）。

並列で動かしたワーカーは、これです（[[feedback_parallel_first_execution]] = 独立タスクは並列 Agent 起動が default）。

| # | ワーカー | タスク |
|---|---|---|
| A | Claude Agent | 開放端 sweep PoC（baseline は飽和・全滅 / 開放端は回避 を実証、≥1 万世代） |
| B | Claude Agent | 観測基盤（応答ログ / 個体別スコア時系列ビューワー / lineage 復元） |
| C | Claude Agent | オーケストラ PoC（MoA が単一 best を上回るか、多様性選抜 vs 冗長選抜） |
| P | Perplexity | QD/novelty/MoA/agentic 進化の SOTA サーベイ（文献ギャップ補完） |
| X | Codex | 設計の独立批評 + 最小 PoC 3 案 + 見落とし指摘 |
| 自己 | 私（main） | 自己 PoC #1〜#6 を直接実装・実行（orchestrator 兼最重要タスク担当） |

> 🍵 **休憩ポイント**: この「6 人がかり」の体制、実は本記事の隠れた主役です。
> なぜ 1 人（1 つの context）で全部やらないのか? 答えは honest disclosure の核心にあります。
> **同じ頭で考えた結論は、同じバイアスに引きずられる。** 別々の手法（合成 PoC / 実 LLM /
> 文献調査）で**独立に**確かめて、それが一致したときだけ、結論を信用する。これを
> **honest cross-validation** と呼びます。後半でその威力が出てきます。

ここで 1 つ、正直な不発も書いておきます。**Codex（X）は使えませんでした。** ChatGPT アカウントの許可モデル不一致（API 側が codex 系モデルを軒並み拒否）でブロック。10x promo 期間中のはずが、API が "not supported when using Codex with a ChatGPT account" を返す。これは環境問題なので、当面は自己 PoC + 並列 Agent + Perplexity を主軸に切り替えました。**「使えるはずの道具が使えなかった」も、隠さず記録する。**

---

#### 4. 最初の決定打 — 「固定ものさし」を捨てるか（自己 PoC #1 / #2）

最初に潰すべき仮説は、いちばん根っこの問いでした。**「ものさしを固定難易度から適応難易度に変えれば、飽和は直るのか?」**

##### 4.1 自己 PoC #1 — 適応難易度は飽和を直す。が、多様性を殺す

合成の competence ベクトルを使った proxy で、交絡を除去して（elite を score 基準で選ぶ）比較しました。

- **baseline（固定難易度）**: 能力 **0.627 で低位停滞**（best 0.757）。12h の病理を proxy で再現。
- **adaptive（難易度 = 集団 60 分位に追従）**: 能力 **0.952 へ上昇**（best 1.0）。

難易度を集団に追従させる（できる問題が増えたら問題を難しくする）と、飽和が解けて能力が伸びた。**だが**——adaptive は**多様性を犠牲**にしました（diversity 0.310 → 0.134 に崩壊）。難しい問題に最適化する過程で、集団が 1 つの正解戦略に凝集してしまう。

##### 4.2 自己 PoC #2 — 適応難易度 × novelty は両立する

そこで「適応難易度（勾配を維持）」に「novelty 選抜（多様性を維持）」を足したらどうなるか。

| 構成 | 最終能力 | best | 多様性 | plateau |
|---|---|---|---|---|
| baseline（固定難易度） | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive（難易度追従） | 0.952 | 1.000 | 0.134（崩壊） | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316（維持）** | gen99（最長探索） |

**adaptive + novelty が、能力（baseline 比 +40%）と多様性（adaptive 比 2.4 倍、baseline 同等）を両立**しました。能力を 7% 譲るかわりに、多様性を完全維持。

ここで**方策の核が、自前データで確定**しました。

> **「適応難易度＝勾配維持」と「QD/novelty＝多様性維持」は相補で、両方必須。**
> 固定ものさし単独（baseline）も、適応難易度単独（adaptive）も、どちらも不十分。

honest 留保: これは抽象 proxy（competence ベクトル）であって、実 LLM 写像ではありません。**mechanism feasibility（機構が回るか）の検証**に限定されます。plateau@gen の数字は「停滞した世代」を指しますが、本質は停滞の**水準**——baseline は低位（0.627）で停滞、adaptive 系は天井近傍で停滞、という違いです。

> 🤔 **たとえ話**: 全員が満点を取ったら問題を難しくする（適応難易度）。すると点は割れますが、
> 今度は全員が同じ解き方に収束してしまう（金太郎飴）。そこで「変わった解き方にもご褒美をやる」
> （novelty）を足すと、能力と多様性が両立する。**「難しくする」と「変わり者を褒める」の二刀流**——
> これが PoC #2 の要点です。

---

#### 5. 本丸の証拠 — 開放端進化の 1 万世代 sweep（Agent A）

自己 PoC で「方向」は見えました。次は、それを**大規模に・厳密に**叩く番です。並列 Agent A に、**各 1 万世代 × pop256 × 19 構成 × 2 巡**の開放端 sweep を回させました。

判定基準は「open-ended（開放端）かどうか」——**飽和せず、monoculture（単一文化への収束）を避け、archive（多様性の貯蔵）が成長し続けるか**。

##### 5.1 決定的な判定表

**verdict（gen9999 時点）: 全 scalar 構成 = False / 全 novelty・lexicase 構成 = True**

| label | 選択 | std | MC | reservoir | archive | open-ended | occupied | monoculture | uniq_lineages |
|---|---|---|---|---|---|---|---|---|---|
| baseline_scalar | scalar | - | - | 0 | none | **False** | 9 | 0.74 | 1.0 |
| baseline_scalar_mc | scalar | - | ✓ | 0 | none | **False** | 9 | 0.90 | 1.0 |
| **scalar_qd** | scalar | - | - | 0 | map-elites | **False** | — | — | — |
| novelty_std | novelty | ✓ | - | 0 | none | True | 100 | 0.13 | 1.0 |
| novelty_std_qd | novelty | ✓ | - | 0 | map-elites | True | — | — | — |
| **novelty_std_res256** | novelty | ✓ | - | 256 | map-elites | True | 95 | 0.05 | **31.9** |
| novelty_std_res1024 | novelty | ✓ | - | 1024 | map-elites | True | 98 | 0.04 | 15.2 |
| **full_oe** | novelty | ✓ | ✓ | 1024 | map-elites | True | 90 | 0.05 | 15.3 |
| lexicase_std(_mc) | lexicase | ✓ | -/✓ | 0 | none | True | 111–122 | 0.03 | 1.0 |

ここから、4 つの決定的な発見が出ました。

1. **選択圧が決定打。** scalar（単一スカラー fitness）は、MAP-Elites の archive を足しても（`scalar_qd`）**全滅（False）**。つまり「貯蔵庫を足せば多様性が守れる」というのは**誤り**で、**novelty / lexicase という開放端な選択でないと、そもそも開放端は成立しない**。archive 単独では救えない。**選択圧そのものを開放端化する**のが本質だった。
2. **標準化（z-score）が QD 被覆を桁で広げる。** novelty に per-dim z-score 標準化を足すと、occupied cells が 9 → 100+ に。各軸の「逸脱」を選択圧に変えると、行動空間の被覆が一桁広がる。
3. **中立貯蔵庫が系統多様性を回復。** novelty_std だけだと uniq_lineages は 1.0（系統は 1 つに固定）。reservoir256 を足すと **31.9** に。**行動多様性と系統多様性は別の軸**で、後者には貯蔵庫が要る（これは #26 設計編で実装済の知見の再確認）。
4. **スケールが効く。** latent 次元を 256 → 1024 にすると niche が 101 → 166、archive が 1021（飽和）→ 2234（成長継続）。多様性は「容量」で買える。

![Stage1 baseline（novelty なし）の適応度と多様性。終盤に多様性が崩壊する（scalar の典型的な失敗）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg)

![Stage1 novelty pressure あり。行動多様性が終盤まで維持される](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status.svg)

![baseline vs +novelty の diversity を重ね描き。崩壊（scalar）と維持（novelty）を 1 枚で対比](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay.svg)

##### 5.2 Agent A が出してくれた「正直な限界」

良い結果（open-ended 成立）が出たときこそ、限界を書く。Agent A 自身が、こう指摘してきました。

> novelty/lexicase は記述子**全体**の多様性は保つが、**特定の意味次元（factor）の多様性は保証しない**。
> 大きな latent では factor drift が起き、fspread（factor の広がり）が要監視。

つまり「全体としては多様」でも「思考因子という特定の意味次元では収束している」ことがありうる。これは新しい要件 **factor-subspace QD（意味次元を個別に保護する QD）** を生みました（後述の PoC #6 で対処）。

> 🍵 **休憩ポイント**: ここが本記事のいちばん硬い節です。持ち帰ってほしいのは 1 行——
> **「archive（貯蔵庫）を足すだけでは救えない。選択圧そのものを開放端にしないと駄目」**。
> #25/#26 設計編で「集約しない」と言ってきましたが、その本丸が「**選択の仕方を開放端化する**」
> ことだった、と 1 万世代の実データが言い切ってくれた。ここを越えたら、あとは独自性の話です。

---

#### 6. 独自性の核 — 「連続進化する集団を、止めずに合奏させる」

ここまでで「飽和を構造的に避ける選択核（S1）」が固まりました。次は、ユーザーが対話で示した**独自性 3 軸**を、PoC と文献で裏付ける番です。

ユーザーが言語化した 3 軸は、これでした。

1. **連続進化集団 = ライブ・オーケストラ（ORCH）** — 進化し続ける集団が、その場で MoA（Mixture-of-Agents）集約して 1 答する。進化を止めない。**最大の差別化候補。**
2. **調査機能を持つ個体（AGENT）** — 個体が自分で調べに行く。Voyager 系。
3. **観測・対話制御（OBS）** — 個体別の応答 + 選択スコアの時系列を見て、止めて、再開できる。

##### 6.1 Perplexity が裏付けた white-space

並列で走らせた Perplexity の SOTA サーベイ（1143 行）が、最重要の裏付けを返してきました。

> 「**online evolution + online answering を統合した連続稼働システム**」は、明確な先行研究なし
> ＝ **research white-space（空白地帯）**。近接は MoA / Self-MoA / sequential aggregation / routing
> だが、同一物はない。

つまり「進化を止めて、できあがった最強個体で答える」のは普通。「進化を**止めずに**、進化中の集団をそのまま合奏させて答える」のは、誰もまだやっていない。**ORCH §1.11 の差別化が確定**しました。

##### 6.2 ただし Perplexity は反証警告もくれた

honest disclosure として、Perplexity がくれた**反証警告**も同じ重みで書きます。

> 2025 年の **Self-MoA 研究**では、**多様性は自動的に優位ではない**。単一トップモデルの反復が、
> 異種混合 MoA を AlpacaEval で 6.6% 上回った（quality-diversity トレードオフ）。

「集団を合奏させれば単一個体より強い」は、**自明ではない**。むしろ多様性が逆効果になる場合がある、と先行研究が警告している。だから ORCH は「実測で証明せよ、pass-bar を正直に」。これを Agent C と自己 PoC #3/#4 で検証しました。

> 🍵 **休憩ポイント**: ここ、研究の誠実さが試される分岐点です。「online 進化 + online 回答は
> white-space！独自性！」で舞い上がりたいところに、Perplexity が「でも多様性は自動的に良くない
> という反証があるよ」と冷や水をかけてくる。**舞い上がる材料と冷や水を、同じ調査の中で両方
> 受け取る。** これができると、結論がぐっと強くなります。次節で、その冷や水の正体を解明します。

---

#### 7. Self-MoA 反証の「正体」を解明する（自己 PoC #3 → Agent C 実 LLM）

「多様性は自動的に優位でない」——この反証を、proxy ではなく**メカニズムのレベル**で解明したのが、ここの山場です。

##### 7.1 自己 PoC #3 — 投票か、ルーティングか

まず、proxy では検証不能でした（飽和した fitness では single best が既に満点 = headroom ゼロで差が出ない）。そこで**「単一個体が満点を取れない難タスク」**（専門家が分散し、single_best=0.5）を合成して測りました。

| 構成 | best_of（routing） | majority（vote） | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant（top-k） | 0.750 | 0.500 | 3/4 |
| MoA diverse（max-cover） | **1.000** | **0.000** | 4/4 |

ここで**決定的な発見**が出ました。

- 多様 MoA は **best-of / routing なら 1.000**（単一 best の倍）。**ORCH は成立する。**
- **ところが naive majority（多数決）では、多様性が逆効果**（diverse = 0.000）。各 sub-task で competent な専門家 1 人が、無知な多数派に negate（打ち消し）される。冗長 MoA の majority（0.500）のほうが上。

つまり **Self-MoA 反証（多様性 ≠ 自動優位）の正体は、「集約器が投票か、ルーティングか」だった**。投票・平均は多様性を殺し、competence-aware な routing/gating は多様性を活かす。「指揮者がいるオーケストラ」と「全員が好き勝手に音を出す雑踏」の違いです。

##### 7.2 Agent C の実 LLM が、独立に同じ結論を出した

そして——並列 Agent C が、**実 LLM（llama3.2、105 回の LLM 呼び出し、15 タスク）**で、自己 PoC #3 と**独立に同じ結論**を出してきました。

- 単一 best = **0.933**。MoA `best_of` + k≥5 で **1.000**（+0.067）。**majority / weighted は一度も 0.933 を超えず。**
- diverse > redundant（多様選抜が異 QD cell の補完 specialist を少ない k で先に拾う）。
- 改善は**丸ごと multistep の 1 問**（「5 を 2 倍して 3 引く」）由来。CoT 個体群が揃って落とす 1 問を、多様選抜の異種個体が解いた。

> 🔑 **独立クロス検証（本記事の核）**: 自己 PoC #3（合成・専門家分散）と Agent C（実 LLM・llama3.2）が、
> **別の手法で同一の結論**——「MoA は competence-aware routing（best_of）でのみ単一 best を上回る /
> 投票では届かない / 多様性は routing 下でのみ価値を持つ」——に達しました。
> 2 手法が一致することは、honest disclosure 上きわめて強い証拠です。

##### 7.3 最大の穴 — 「実ルーター」は oracle に届くのか（自己 PoC #4）

ここで Agent C が、最大の穴を指摘してきました。「best_of は **oracle routing**（どの個体が正解かを神様が知っている上限）であって、実際は『どの個体が competent か』を**予測する gate** の精度が律速。実投票（majority）は oracle に届かない」。

これを自己 PoC #4（実ルーター vs oracle、20 seed 平均）で埋めました。

| κ（較正） | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **descriptor / specialty-router は較正不要で robust に 0.90**（単一 best 0.675 を安定超え、oracle 近傍）。しかも **routing キーは QD 用に既に計算する behavior descriptor を流用できる**——**QD と ORCH が同じ記述子基盤を共有**する相乗効果。
- **confidence-router は較正 κ≥0.6 で oracle 到達**。ただし小型 LLM は較正が弱い恐れ → **descriptor-router を第一選択**（較正非依存）。
- **majority = 0.338 は確定的に不適**（PoC #3、Agent C と**三たび一致**）。

**結論**: Agent C が指摘した「oracle に実投票が届かない」穴は、**descriptor-routing（QD 記述子を流用）で実用的に埋まる**。ORCH が proxy + （部分）実 LLM で end-to-end に成立しました。

> 🤔 **たとえ話**: 専門家を 10 人集めて多数決させると、無知な多数派が正しい専門家を打ち消してしまう。
> 数学の問題は数学者に振る——**振り分ける係（指揮者 = routing）**が要るのです。しかもその指揮者の楽譜
> （behavior descriptor）は、多様性を管理するために**すでに計算してある**ものを流用できる。投票
> （majority）は専門家を殺し、指揮者（routing）が活かす。これが PoC #4 の要点です。

---

#### 8. 個体に「調べる力」を持たせる（自己 PoC #5）

独自性 3 軸の 2 つ目、**調査機能を持つ個体（AGENT）**。個体が探索空間でサンドボックス読取専用の調査をできるようにする構想です。ただし「調査はタダではない」——コストを計上したとき、進化は調査を使いこなすのか?

自己 PoC #5（コスト λ を変えて、調査閾値 θ がどう進化するか、20 seed 平均）。

| λ | θ*（=λc, 最適閾値） | θ_evolved（進化が獲得した閾値） | evolved | always | never |
|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.049 | 21.46 | 21.47 | **11.70** |
| 0.3 | 0.30 | 0.476 | 21.34 | 21.26 | 21.20 |
| 0.6 | 0.60 | 0.659 | **21.24** | 21.06 | 21.21 |
| 0.9 | 0.90 | 0.888 | 21.21 | 20.85 | 21.21 |

- **進化が、選択閾値 θ → λc を自力で獲得**した（= 状況に応じて「調べるべきときだけ調べる」選択的調査が**創発**）。
- **調査機能の価値は明白**: λ=0（調査無料）のとき、never（一切調べない）は 11.70 = **45% の損**。
- **コスト λ が「always 調査」を劣化させ、選択を強制**する。AGENT-3（コスト原理）成立。

honest 留保: 中間 λ での margin は小さく（浅い報酬地形）、これも抽象 proxy（実 LLM × 知識ベースは別段）。それでも「コストがあると、選択的調査が創発する」というメカニズムは proxy で確かめられました。

---

#### 9. スケールが「多様性を質的に増やす」（Round 3）

最後に、Agent A が指摘した「容量で多様性を買える」を、母数（集団サイズ）でも確かめました。`full_oe` 構成（novelty + std + MC + reservoir1024 + map-elites）で、pop を 256 → 4096 まで振りました。

| pop | gens | occupied niches | monoculture | uniq_lineages | distinct_genomes | bspread_tail |
|---|---|---|---|---|---|---|
| 256 | 5000 | 171 | 0.047 | 14 | 256 | 0.939 |
| 1024 | 3500 | 467 | 0.019 | 74 | 1022 | 1.003 |
| 2048 | 2500 | 754 | 0.009 | 188 | 2041 | 1.071 |
| 4096 | 1200 | **1219** | **0.006** | **372** | 4054 | 1.253 |

母数スケールで、open-endedness が**単調に向上**しました（niches 171 → 1219 / monoculture 0.047 → 0.006 / uniq_lineages 14 → 372 / 行動の広がり bspread も単調増）。POP-1 仮説（母数が多様性を増やす）が proxy で支持されました。

**honest（交絡を明示）**: ここに正直な落とし穴があります。pop を上げるぶん、gens を短縮しました（5000 → 1200）。これは **niche 蓄積には不利な方向の交絡**です。それでも単調増だった——つまり **POP 効果は robust な下限**（本来はもっと効くはず）。逆に言えば「もっと効く可能性」は、この実験では証明できていない。proxy mechanism feasibility に限定された主張です。

![勝者個体の思考因子 × メモリ層ヒートマップ（Genome3D）。real-pressure では c_factors が中立浮動のため、これは認知プロファイルの可視化として参考扱い](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_genome_heatmap.svg)

> 🍵 **休憩ポイント**: 「スケールすれば多様性が増える」は直感的ですが、ここで大事なのは
> **「不利な交絡を入れてもなお単調増だった」**という正直さです。gens を削るのは普通なら
> 多様性に不利。それでも増えた。だから「下限」と言える。良い結果を「上限」と誇張せず
> 「下限」と書く——これも honest disclosure の作法です。

---

#### 10. 朝、全員が同じ結論に着いていた — 確定した方策

一晩で、**自己 PoC 6 本 + Agent A/B/C + Perplexity が、独立に同じ結論へ収束**しました。これが honest cross-validation の威力です。固定ものさし路線を捨て、以下を lldarwin v2 の核に確定採用しました。

##### S1. 選択核（飽和を構造的に回避）

- **固定スカラー quiz fitness を廃止**（baseline は 1 万世代で飽和 + monoculture 0.9 + 多様性崩壊 = 12h 病理を大規模再現、open-ended 0/6）。
- **選択 = novelty / ε-lexicase（z-score 標準化必須）+ minimal-criterion**。**MAP-Elites archive 単独では不可**（scalar_qd も全滅）= 選択圧そのものを開放端化する。
- **品質も要るので QD（品質 × 多様性 per cell）**: 純 novelty は scalar 品質を犠牲（0.77-0.83）→ 適応難易度（条件カリキュラム）と組んで品質勾配を供給（PoC #2）。
- **系統多様性は中立貯蔵庫で別途確保**（行動多様性 ≠ 系統多様性、res256 で uniq_lineages 1 → 32）。
- **factor-subspace QD を追加**（意味次元の多様性を個別保護、Agent A の factor-drift 限界への対処、PoC #6）。

##### S2. 成果の出し方 = 連続進化 × ライブ・オーケストラ（独自性の核）

- 成果物は単一 best でなく、**QD archive を連続進化させ、任意時点で MoA オーケストラして 1 答**（ORCH; online 進化 + online 回答の統合は white-space = 独自性、Perplexity 確認）。
- **集約は投票でなく competence-aware routing/gating（指揮者）必須**（自己 PoC #3/#4 + 実 LLM Agent C が三重一致）。
- **routing キーは QD の behavior descriptor を流用**（descriptor-router が較正非依存で oracle 近傍 0.90）= QD と ORCH が同一記述子基盤を共有（設計の節約）。

##### S3. 個体 = 調査機能を持つ agentic 個体（段階導入、proxy 検証済）

- 探索空間ではサンドボックス読取専用調査のみ（実 I/O は Approval Bus 片方向昇格後）。調査はコスト計上。
- **proxy 検証済（PoC #5）**: コスト λ が「選択的調査」を創発。AGENT-3（コスト原理）成立。実 LLM × 知識ベースは次段。

##### S4. 観測・対話制御（実装済 = 全ランで標準装備、Agent B 完了）

- 応答ログ / 個体別スコア時系列ビューワー / lineage 復元（進化系 886 テスト緑）。step/pause/resume は次段で配線予定。
- Agent B の lineage 復元は、12h データで「**全部 ?**」だった系統表示を解消し、champion 系統を gen70 → gen59 まで 12 hops 解決。欠落は捏造せず `lost@genN` と明示する（根因 = 親 ID が snapshot と winners のどちらか単独では辿れなかったこと）。観測基盤こそが honest disclosure の土台です。

##### 自己 PoC #6 — factor-subspace QD で Agent A の限界に対処

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

意味次元（factor）用の novelty を別途課すと、意味次元の多様性損失をほぼ半減（50% 損 → 32% 損）。Agent A の factor-drift 限界への有効策を proxy で実証。honest: 完全固定ではなく 68% 残存 = 残 drift は中立貯蔵庫併用 or factor 重み強化が要。

---

#### 11. 教訓（honest disclosure として残す）

- **実 LLM でも飽和した。** 眼鏡を proxy から実 LLM に替えても、ものさしが固定なら gen5 で満点。
  「本物の LLM を使えば進化する」は**嘘**でした。問題はものさしの作り方だった。
- **archive を足すだけでは救えない。** 「多様性の貯蔵庫を持てば多様性が守れる」は誤り。
  scalar 選択は QD archive を足しても全滅した。**救うのは選択圧の開放端化そのもの。**
- **多様性は自動的には良くない。** Self-MoA 反証の正体は「投票か routing か」。
  指揮者（competence-aware routing）がいて初めて、多様性は価値になる。投票は専門家を殺す。
- **独立クロス検証が、結論を強くする。** 自己 PoC（合成）と Agent C（実 LLM）と Perplexity（文献）が
  別々に同じ結論へ収束したからこそ、信用してよい。同じ頭の結論は、同じバイアスを共有する。
- **proxy は mechanism feasibility のみ。** 本記事の PoC 群は「機構が回るか」の検証であって、
  「実 LLM 一般の能力向上」の主張ではありません。この線引きを越えた瞬間、研究は嘘になります。
- **使えなかった道具（Codex）も記録する。** 成功だけでなく不発も honest に。

要するに——**「眼鏡（評価）が飽和したら、淘汰器をどれだけ磨いても無力」**。
だから磨く対象を、淘汰器でも LLM でもなく、**評価そのものの開放端化**に移す。これが一晩の結論です。

> 🍵 **休憩ポイント**: #25 で「失敗を晒す」と決めた。#26 設計編で「集約しない淘汰器」を作った。
> そして今回、本物の LLM が「それでもまだ足りない、ものさしが固定だから」と教えてくれた。
> **失敗が次の設計を生み、その設計の限界がまた次を生む。** これが連載の背骨です。
> 派手な「進化で AI が賢くなった！」は、まだ一度も書いていません。書けるだけの根拠が
> 揃っていないからです。揃ったときに、初めて書きます。

---

#### 12. 結論

- 実 LLM 12h ランは「正直な不合格」だった——全滅しないが累積しない filtered random search。真因は固定ものさしの飽和（#25 の洞察を実 LLM で実証）。
- 一晩の分散調査（自己 PoC 6 本 + Agent A/B/C + Perplexity）が、独立に同じ結論へ収束 = **honest cross-validation**。
- 確定方策: **S1 開放端な選択核**（novelty/lexicase + std + MC + QD + 適応難易度 + 中立貯蔵庫 + factor-subspace QD）/ **S2 連続進化 × routing-MoA**（white-space 独自性、投票でなく指揮者）/ **S3 agentic 個体 + コスト**（選択的調査の創発）/ **S4 観測**（実装済）。
- すべての要素を proxy / （部分）実 LLM で裏付け済。残課題は「実 LLM 段への配線」「factor-subspace QD 実装」「scale-up」。コア戦略は確定した。

良い部品を作り、集約せずに束ね、実 LLM で飽和を確かめ、開放端な選択へ作り直す。そして 6 通りの独立検証が同じ結論に着いたとき、ようやく「方策が決まった」と言える。本記事こそ、#25 で予告した「**眼鏡が曇ると淘汰も無力**」の回です——実 LLM で眼鏡が曇った瞬間（飽和）を正直に晒し、Goodhart's law と proxy の限界を引き受けたうえで、開放端へ作り直しました。次は、この確定方策をコードへ落とす [**#28 実装編（オーケストラ型 AI）**](drafts/QIITA_#28_lldarwin_v2_phase1_orchestra.md) へ。

---

#### 13. 関連

- 連載 #24-05「集団が学ぶ AI」— 派生集団進化の枠組み（本記事の前提）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #25「私とフリストンだけが残った」— monoculture の honest disclosure（本記事の動機）
- 連載 #26（設計編）「眼鏡で測るだけでは進化しない」— 淘汰器 lldarwin の設計と Stage1/1.5/2 実測（本記事の姉妹編）
- 先駆者論文（2026-05-27, date of record）「Continuously-Evolving Populations as Live Orchestrated Ensembles」— 本記事の方策を学術形式で定式化した防御的公開（FullSense 公開リポジトリ `docs/papers/`）
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

## 4. 進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28（lldarwin 実装編）

### 進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28

> 📚 **連載ナビ（lldarwin アーク）**: #24-05 集団進化 → #25 monoculture の失敗 → #26 設計編 → #27 徹夜の意思決定（climax）→ **#28 本記事（実装編）**。※ 各記事は単独でも読めます。

> **コンセプト hook**:
> 1 体の賢い AI に何度も聞くのではなく、**少しずつ違う大勢の AI を「進化」させ続け、答えが要るその瞬間に、指揮者が適材を選んで合奏（オーケストラ）させて 1 つの答えにする**。
> ——これが llive がいま目指している姿です。`llive` は「LLM そのもの」ではなく「LLM の周りに被せる認知 OS」。その中で、**集団を絶やさず・偏らせず・成長させ続ける**のが、今回作り込んだ進化エンジン `lldarwin` です。
>
> 前作 #27 で私たちは「評価（ものさし）が満点に張り付くと、進化は止まってただのふるい付きランダムサーチになる」という病を、実 LLM の 12 時間ランで確認しました。そして「淘汰器をいくら磨いても無駄。**評価そのものを開放端にせよ**」と方策を決めた。
>
> 今回はその方策を **実装** しました。そして proxy（合成のものさし）の上で、**best スコアが満点に張り付かず、最後まで伸び続けた**のです。

---

#### 0. 三行であらすじ（落語の「枕」）

- **売りが決まった** — llive の北極星は「**連続進化 × ライブ・オーケストラ**」。進化し続ける集団を止めずに、任意の瞬間に competence-aware routing（指揮者）で合奏させて 1 答する。これは先行研究の **white-space（空白地帯）**。
- **飽和を治す 3 つを実装した** — ①意味次元を個別保護する factor-subspace QD ②成果を「単一 best」でなく多様性アーカイブに貯める MAP-Elites ③ものさしを集団に追従させる適応難易度。これで「奏者（多様な個体）が絶えない」基盤ができた。
- **proxy で飽和回避を実証** — lldarwin-v2 を 10 世代回したら best 0.80 → **0.92 と張り付かずに上昇**。多様性アーカイブは 21 セルが埋まった。**ただし proxy であり、実 LLM の能力を測ったわけではない**（honest）。

要するに **「賢い 1 体」ではなく「多様な大勢 × 指揮者」**。そのための「奏者を絶やさない仕掛け」が今回の実装です。

---

#### 1. llive とは何か（はじめての方へ）

`llive`（リブ。L は 2 つ）は **自己進化型・モジュラー記憶の LLM フレームワーク**です。FullSense という傘ブランドの一員で、兄弟に `llmesh`（オンプレ LLM ハブ）と `llove`（端末ダッシュボード）がいます。3 つは独立 OSS ですが、組み合わせると 1 つの世界観になります。

llive の思想を 1 行で言うと「**LLM 本体ではなく、LLM の"周り"に被せる認知 OS**」。4 層メモリ・6 ステージのループ・承認バス（Approval Bus）・TRIZ・10 個の思考因子……といった「考え方の足場」を LLM の外側に組み、**同じ LLM でも振る舞いを進化させられる**ようにします。

その「進化」を担うのが、今回の主役 **`lldarwin`**（ダーウィン）です。役割分担はこうです。

- **lleval（眼鏡）** = 個体を *測る*（評価）
- **lldarwin（淘汰器）** = 測った差を「誰が生き残り・子を残すか」に *変換する*（選択圧）

そして両者の上に乗る北極星が、次の「オーケストラ」です。

---

#### 2. 売り = 連続進化 × ライブ・オーケストラ（独自性の核）

普通の Mixture-of-Agents（MoA）は、**固定された**複数モデルに同じ問いを投げ、答えを集約します。llive が狙うのはその一歩先です。

> **集団を止めずに進化させ続け（online evolution）、答えが要るその瞬間に（online answering）、指揮者が「この問いにはこの奏者たち」と選んで合奏させて 1 答する。**

この「online 進化 + online 回答の統合」は、調べた限り**明確な先行研究がない white-space** でした（#27 で Perplexity に文献を漁らせて確認）。近いものに MoA / Self-MoA / sequential aggregation / routing はありますが、「進化し続ける集団そのものをライブで合奏させる」型は見当たりません。

ここで効くのが #27 で得た 2 つの正直な発見です。

1. **集約は「投票」ではなく「指揮者（competence-aware routing / gating）」でなければならない。** 自己 PoC と実 LLM 検証が三重に一致しました：headroom（伸びしろ）のあるタスクでは `best_of`／`routing` が `single`（単一モデル反復）を上回るが、**`majority`（多数決）はむしろ逆効果**。これは 2025 年の "Self-MoA"（多様性は自動的に優位ではない）への、私たちなりの回答でもあります。
2. **指揮者の判断キーには、多様性アーカイブの「behavior descriptor」を流用できる。** つまり後述の QD（Quality-Diversity）と指揮者が、**同じ記述子の土台**を共有できる。

——ただし、オーケストラ本体（指揮者＝router の実装）はこれからです。**今回はその手前、「合奏させるに足る、多様で絶えない奏者の集団」を作る基盤**を実装しました。

---

#### 3. なぜ「奏者が絶える」のか — 飽和という病（#25〜#27 のおさらい）

オーケストラに必要なのは「**個性の違う奏者が大勢、絶えずいること**」です。ところが素朴に進化させると、これが崩壊します。

- #25：500 世代回したら、世界に「私とフリストンだけ」が残った（**monoculture**）。
- #27：実 LLM(llama3.2) で 12 時間回したら、gen5 で best=1.0 に張り付き、65 世代無進歩。**全滅しないが累積もしない**＝ふるい付きランダムサーチ。

真因はどちらも同じ。**人手で固定したものさし（評価関数）が満点に張り付くと、全員が同点になって選択圧が消え、あとは遺伝的浮動で勝手に偏る**。眼鏡（lleval）が飽和すると、淘汰器（lldarwin）をどれだけ磨いても無力——これが #27 の結論でした。

だから磨く対象を変える。「ものさしを動かす」「多様性を構造的に守る」方へ。具体的には次の 3 つです。

---

#### 4. 実装した 3 つの仕掛け（lldarwin v2 / Phase 1）

> 設計の合言葉は「**新しいアルゴリズムを発明しない**」。すでに llive 内に積み上げた部品（ε-lexicase / NoveltyScorer / MAP-Elites / 中立貯蔵庫）を、確定方策 S1 の形に**合成・配線**するのが Phase 1 です。`--selection lldarwin-v2` で一括 on になります。

##### ③ 適応難易度 — ものさしを集団に追従させる

`AdaptivePercentileGate`。各評価軸の「最低ライン（minimal-criterion）」を、毎世代**集団のスコア分布の指定パーセンタイル（例：下位 40% 点）**に置き直します。集団が伸びれば最低ラインも自動で上がる。`ratchet`（単調非減少）にしておけば、一時的に下振れしても基準は緩まない。

これで「固定ものさしが満点で飽和する」病に蓋ができます（PoC では固定難易度が能力 0.627 で停滞 → 適応難易度で 0.952 まで上昇）。全員が最低ラインを割る荒れた世代でも、淘汰器は gate を無視して全滅を避けます（fail-open ガード）。

落語でいえば、**生徒が伸びたら合格点も上げる先生**です。満点を取らせて終わりにしない。

##### ① factor-subspace QD — 意味次元の個性を個別に守る

`FactorSubspaceNovelty`。novelty 探索は「集団全体としての多様性」は保ちますが、巨大な潜在次元の下では「**意味のある次元（思考因子）の多様性**」が、いつのまにか痩せていきます（factor drift）。

そこで、思考因子の**部分空間だけ**で別途 novelty を測り、全体 novelty とブレンドします。PoC では、これで意味次元の多様性の目減りがほぼ半減しました（retention 49.5% → 68.1%）。

> 正直な改良点：元の PoC は「生の距離を 0.5 ずつ足す」でしたが、部分空間ごとに距離のスケールが違うため、実装では**それぞれを z-score（標準化）してからブレンド**するように直しました。「全体の合唱」と「各パートの個性」を公平に混ぜるためです。

奏者でいえば、**第二バイオリンが第一バイオリンに飲まれて消えない**ようにする仕掛けです。

##### ② MAP-Elites — 成果を「1 人の優勝者」でなく「多様性の地図」に貯める

`run_persona_evolution(map_elites=True)`。毎世代、全個体を MAP-Elites アーカイブに投入します。これは「最高スコアの 1 体」ではなく、**振る舞いの座標ごとに、そのマスでの最良個体を残す**地図（QD アーカイブ）です。新しいマスを埋めても既存のマスは消さない＝**多様性が構造的に崩壊しない・アーカイブは単調に育つ**。

これがそのまま、オーケストラの**奏者カタログ**になります。指揮者は将来、この地図から「この問いに合う座標の奏者」を選んで合奏させる——QD と routing が同じ記述子を共有する、という #27 の設計がここで効いてきます。

実装は **個体のフォーマットを拡張せず**、既存ゲノムの思考因子から座標（descriptor）を導出する additive 配線にしました（基盤の後方互換 900+ テストを壊さないため）。記述子の本格設計（高次元の縮約など）は将来 Phase の課題として余地を残しています。

---

#### 5. 結果 — proxy で「飽和しない進化」を確認

`lldarwin-v2`（上記 3 つ＋ novelty ＋中立貯蔵庫を全部 on）を proxy のものさしで 16 個体 × 10 世代回した実測です。

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21（多様性の地図に 21 マスが埋まった）
```

- **best が満点に張り付かず、0.80 → 0.92 と最後まで上昇し続けた。** #27 で見た「gen5 で 1.0 飽和→固定」の病理を、proxy 段では脱却できました。適応難易度が「ものさし」を集団に追従させた兆候です。
- **多様性アーカイブに 21 セルが埋まった** = 合奏させるべき「個性の違う奏者」のカタログができ始めた。
- 進化系の自動テスト **879 件＋新規テストが全部グリーン**、回帰なし。

---

#### 6. honest disclosure（ここを飛ばさないでください）

良い結果ほど内訳を疑う、が FullSense の流儀です。

- **これは proxy です。** 個体は実 LLM ではなく llive のゲノム（思考因子の代理）。今回測ったのは「複数の独立した苦手軸に同時に選択圧をかけ、軸ごとの専門家を維持できるか」という **仕組みの実現可能性（mechanism feasibility）** であって、**production の LLM 能力ではありません**。実 LLM 評価は次の Phase です。
- **factor-subspace は完全保護ではない**（retention 68%、残りはドリフト）。中立貯蔵庫の併用や factor 重みの強化が要ります。
- **舞台裏の正直**：今回の実装中、自動コミットフックが編集のたびに「編集前」スナップショットを 49 件も積んでしまい、履歴が散らかりました。最後に意味のある 1 コミットへ squash して整理しています（公開 OSS 側）。逆に、内部戦略を含む fork は意図通りローカル保持のままで、露出していないことも確認しました。

---

#### 7. これからどうするか

進化エンジン（奏者を絶やさない基盤）は Phase 1 で形になりました。次はオーケストラ本体と、proxy から実物への橋渡しです。

1. **Phase 2 = 実 LLM 配線。** オンプレ（localhost ollama）の実 LLM を相手に、適応難易度・factor-subspace QD・MAP-Elites を実評価で検証する。proxy で見えた「飽和回避」が、本物の能力でも起きるか。
2. **指揮者（router）の実装。** QD アーカイブの descriptor を流用した competence-aware routing で、「進化する集団をライブで合奏させて 1 答」を実際に動かす。`best_of` の oracle にどこまで迫れるか。
3. **規模を上げる。** 集団 256 → 4096、潜在次元のスケールアップ。容量仮説（大きいほどニッチが増える）の確認。
4. **対話的な連続運転。** 長時間ランを step / pause / resume で覗ける運転席（CKPT-1）。

---

#### 8. ここで一息（休憩ポイント）

ここまでで「**llive は何を売りにするのか**」は伝わったでしょうか。

- 賢い 1 体ではなく、**進化し続ける多様な集団 × 指揮者の合奏**。
- そのために、**奏者を絶やさず・個性を守り・成長させ続ける**進化エンジンを作った。
- proxy では飽和を治せた。**次は実 LLM とオーケストラ本体**。

続きの「実 LLM 編」と「オーケストラ編」で、proxy の約束が本物になるかをお見せします。——ここまでお付き合いありがとうございました。

---

#### Series Navigation

- 連載ナビ（lldarwin アーク）: #24-05 集団進化 → #25 monoculture の失敗 → #26 設計編 → #27 徹夜の意思決定 → **#28 本記事（実装編）**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

## 5. 「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #29（Goodhart の法則と proxy fitness の限界）

> 📗 **お急ぎの方へ**: この記事には かみくだき版 があります（比喩多め・短時間で要点だけ）。
![眼鏡が飽和すると選択圧は無力 — 反証4コマ #29](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q29_4koma.svg?v=2)
### 「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #29

> **コンセプト hook**: #25 で失敗を晒し、#26 で「淘汰器 lldarwin」を設計しました。普通の連載なら
> 次は「直りました! めでたし、完!」です。**でも、それをやらないのが FullSense の honest disclosure**。
> この記事はあえて**自分の設計に反証をぶつける回**。テーマは進化計算と機械学習の両方に効く一語——
> **Goodhart's law（指標が目標になると、それは良い指標でなくなる）**。
>
> 「LLM の弱点を fitness にすれば、進化で勝手に克服してくれる」——この甘い楽観に、私は自分で冷や水を
> かけにいきます。しかも今回は、**自分が一度やらかした「事実誤認」を、生きた標本として解剖台に乗せます**。

---

#### 0. 三行であらすじ

- **眼鏡（fitness）が飽和すると、どんな高級な選択圧（lldarwin）を足しても淘汰は無力**になる（#25 の真の教訓）。
- **proxy fitness で LLM 弱点を測ると、真能力でなく「指標をハックする表面戦略」が進化する**（Goodhart's law）。
- 結論: lldarwin の価値主張は **(a) proxy は mechanism feasibility のみ (b) 実 LLM/VLM 評価が本質 (c) 多様性の地図化** に**限定**する。これが正直な線引き。

そして本記事の隠れた主役は、もう一行あります。

- **私自身が「行動多様性」と「系統多様性」と「実 LLM 知能多様性」を一度混同した**。その自己反証を、
  反証回の核に据えます。「うまくいった」を疑うとは、こういうことだ、という実演です。

---

#### 1. honest disclosure の念押し — 良い結果ほど疑う

#26 で「PoC デプロイで行動 monoculture は全条件 **0.05（≪0.8）に改善した**」と書きました。
これは**事実**です。誇張ではありません。

…が、ここで「やったぞ、monoculture 撲滅!」と胸を張って終わると、**#25 で自分が立てた誓いを破る**ことになる。

> 異常に綺麗な結果が出たら、勝った気になる前に内訳を疑う（[[feedback_benchmark_honest_disclosure]]）。

連載 #25 の通奏低音はこうでした——「**異常に綺麗な結果は勝利でなく警報**」。
0.8 を切れば OE-3 達成、という基準に対して **0.05** はあまりにも綺麗すぎる。0.05 という数字は、
祝杯のラッパではなく、**サイレン**として聞かねばなりません。

ではサイレンを鳴らしてみましょう。鳴らすべき問いはただ一つ。

> **何を測った 0.05 なのか?**

答えを先に言うと、0.05 は「**proxy 評価における行動 monoculture**」です。
これは「genome の振る舞い代理（behavioral surrogate）」の集中度であって、
**実 LLM の知能の多様性ではありません**。ここを混同すると、#25 とまったく同じ轍を踏む。

そして正直に告白します。**私は一度、ここを混同しました**。後ほど §3 で、その「現行犯」の証拠を出します。

> 🍵 **休憩ポイント（90 秒）**: この記事は要するに「**自分にダメ出しする記事**」です。
> 読者の皆さんには、ぜひ「成功報告の裏で、著者が何をどこまで疑っているか」を観察してもらう回にしたい。
> SNS でバズる「AI を進化させたら最強○○が誕生!!」の**ちょうど逆**をいきます。盛り上がりません。
> でも、盛り上がらない正直さこそが、半年後に効いてくる——というのが私の賭けです。お茶でもどうぞ。

---

#### 2. 反証 1 — 飽和した眼鏡には、どんな選択圧も効かない

##### 2.1 #25 の真因をもう一度

#25 の真因は「**best_score が 1 世代目から 1.0 に飽和 → 選択圧ゼロ → 遺伝的浮動（genetic drift）**」でした。
全員が満点なら、誰を選んでも一緒。選択は「優れた者を残す」ではなく「サイコロを振る」になる。
結果、運よく増えた系統が運だけで固定し、8 系統が 2 系統（furuse-kazufumi + friston）に崩れた。

ここで、進化アークの中核となる反証を置きます。

> **lldarwin（ε-lexicase でも QD でも novelty でも）を、飽和した eval にそのまま挿しても直らない。**

なぜか。淘汰器の各部品は、いずれも「**差があること**」を大前提にしているからです。

- **ε-lexicase** は「軸ごとに差があること」が前提。**全軸が満点なら、軸を何個に分けても差はゼロ**。
  100 個の軸に分割しても、全部 1.0 なら 100 個の「引き分け」が並ぶだけ。
- **QD（MAP-Elites）** は「behavior 記述子に分散があること」が前提。**全個体が同じ振る舞いなら、cell は 1 つ**。
  地図を作っても、全員が同じマス目に立っていたら、地図は真っ白の一マスになる。
- **novelty** は「過去 archive との距離」が前提。**全員が同じ点に収束していたら、距離は全員ゼロ**。
  新規性で報いようにも、誰も新規でない。

つまり、図式にするとこうです。

```
壊れた眼鏡（fitness 飽和） + 高級な淘汰器 = やっぱり壊れたまま
```

##### 2.1.5 実証 — 記憶タスクで「床」と「天井」が選択圧を殺した（Step C, 2026-05-30）

この反証は、その後 llcore の Step C 実験（CPU 完結）で**実データとして再現**されました。標準的な記憶タスク 2 種を、進化（MAP-Elites）と素朴な探索で解かせた結果がこれです:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="Step C の2つの結果（床と天井）" width="640">

- **delayed_parity（XOR）= 床**: 全 method が R²≈0（基質が原理的に解けない）。誰も登れない＝差が出ない。
- **flip_flop（覚えるだけ）= 天井**: 全 method が R²≈0.95（簡単すぎて全員到達）。**まさに「飽和した眼鏡」で、ここでも選択圧は無力**。

参考までに、③（選択）が効くのは「ニセ頂上を越える、だましだが渡れる坂道（欺瞞 corridor）」がある時だけです:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/deceptive_corridor.svg" alt="だまし地形と進化（③が効く状態）" width="640">

Step C の結論は、潔く **N/A（この基質では③の有無を測れなかった）**。しかも draft 段階で私は「③は不要」と**書きすぎ**、多視点の adversarial 検証が「天井効果で非診断・検出力不足（δ=+0.33 は medium だが p=0.15 で inconclusive）」と捕まえて格下げさせました——§3.2 の「自己反証」が、ここでもそのまま起きたわけです。

##### 2.2 「#25 が直った」は、半分しか正しくない

ここが #25→#26 で見落とされがちな反証です。**#25 が直ったのは lldarwin のおかげ「だけ」ではない**。

実際には、**眼鏡側の修正が先**にありました。

- **per-dim z-score 標準化（STD-1）** — 軸ごとに分散を揃え、「全軸そこそこ高い無特徴な個体」を優位にしない。
- **中央一致除外（SEL-1）** — 全員が同じ値を出す軸は選択に寄与しないので case から外す。
- **記述子の低次元縮約（DESC-1, JL 射影）** — QD の次元の呪いを避け、cell が空っぽにならないようにする。
- **真因 criteria の除外** — `factor_score`（max-archetype の単一スカラー = argmax, SEL-2 違反 = best=1.0 飽和の真因）と
  `nearest_persona_idx`（順序に意味のないカテゴリ index）を ε-lexicase の case から外す。

この「眼鏡を磨く」作業が**先**にあって、初めて淘汰器が効いた。
順番が逆だったら、どんなに高級な lldarwin を載せても、飽和した眼鏡の前では無力だったのです。

> **「測る」を直さず「淘汰する」だけ高級にしても無駄。**

これは進化計算に限らず、機械学習の評価設計全般に効く教訓です。
リーダーボードのスコアが飽和したら、モデルを高級にする前に、まず**ベンチマークが壊れていないか**を疑え。

> 🤔 **たとえ話（漫才風）**:
> ボケ「審査員を 3 人から 100 人に増やしたのに、全員に同じ満点の答案を見せたら、やっぱり結果は一緒やった」
> ツッコミ「そら審査員ちゃうがな、**答案（テスト）が壊れとる**んや! 100 人に同じ満点見せて何が変わんねん!」
> ボケ「ほな審査員 1000 人にしたら…」
> ツッコミ「**増やす方向が逆**や!! まず問題用紙を直さんかい!!」

##### 2.3 責務分離 — どちらが欠けても進化は壊れる

眼鏡（測る）と淘汰器（淘汰する）の責務を分けると、こうなります。

| | 眼鏡が正常 | 眼鏡が飽和 |
|---|---|---|
| **淘汰器が高級（lldarwin）** | ◎ 進化が回る（#26 で達成） | ✗ 無力（#25 の罠） |
| **淘汰器が素朴（Tournament）** | △ 回るが多極性は弱い | ✗ 崩壊（#25 の出発点） |

注目すべきは右下と右上です。**眼鏡が飽和している限り、淘汰器の高級さは右の列を救えない**。
進化の成否は「淘汰器の賢さ」より先に「**眼鏡が差を映せているか**」で決まる。
これが反証 1 の結論であり、#25 の「真の教訓」を一段精密にした言い方です。

実測でこの「眼鏡が曇ると淘汰も崩れる」帰結を見てみましょう。下は baseline（novelty なし・素朴な選択圧）の
適応度と多様性の推移です。終盤、多様性が崩壊していくのが見えます。

![baseline: 終盤の多様性崩壊](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg)

> 🍵 **休憩ポイント（90 秒）**: 「眼鏡を磨いてから淘汰する」——順番が大事、という地味な話でした。
> 地味だけど、ここを飛ばすと半年溶けます（私は溶かしました）。次節からが本記事の本丸、
> **Goodhart's law**。ここからちょっとブラックな話になります。コーヒーに切り替えてもいいかも。

---

#### 3. 反証 2 — Goodhart's law: proxy fitness をハックする進化

##### 3.1 最重大リスク

設計書（LLDARWIN_DESIGN.md §7.1）が「**最重大リスク**」と明記した一点です。

> **LLM の弱点を proxy fitness にすると、真能力でなく「指標をハックする表面戦略」が進化する。**

進化計算は、**与えられた指標を最大化する「近道」を見つける天才**です。
人間が「これで真の能力を測っているつもり」の proxy を渡すと、進化は真の能力を獲得する代わりに、
**proxy だけを満たす表面的な戦略**を必ず発見する。しかも嬉々として、効率的に。

具体的にどんな gaming（指標ハック）が起きうるか。設計書の受容済み限界をそのまま展開します。

| pressure（LLM の弱点） | 起こりうる gaming（指標ハック） | なぜ真能力でないか |
|---|---|---|
| typo_robustness | 特定の typo パターンを暗記して置換するだけ | 未知の typo には無力。ノイズ耐性を獲得していない |
| polysemy_wsd | テスト分布のヒューリスティクスを利用 | 「最頻 sense を返す」等の統計的近道。意味理解ではない |
| multistep_robustness | persuasive な推論「痕跡」だけ生成 | それらしい中間ステップを並べるが、実際には推論していない |
| calibration | 自信度を中庸に操作して ECE を下げる | 全部「自信度 50%」と言えば較正誤差は下がる。較正能力ではない |

最後の calibration の例が一番わかりやすい。
「自信度をちゃんと推定できる」ことを ECE（期待較正誤差）で測ると、進化は
「**全部の質問に『自信度ちょうど真ん中』と答える**」という戦略を見つける。
ECE は劇的に下がる。でもそのモデルは、何一つ較正できていない。ただ中庸を吐くロボットになっただけ。

> **指標が目標になると、それは良い指標でなくなる（Goodhart's law）。**

これは LLM 研究の実例でもあります。GSM8K 型のベンチマークでスコアだけ上がり、汎化しない
**benchmark overfitting** は、まさにこの構造。リーダーボードの数字を信じすぎた者が、何度も足を掬われてきた。

##### 3.2 私自身の「現行犯」— 自己反証

ここで、§1 で予告した「混同の現行犯」を解剖台に乗せます。隠さずに書きます。

私は当初、TODO にこう書いていました——「**再ランで岡潔・グロタンディーク系統が生き残るか**を検証する」。
そして PoC で monoculture **0.05** という綺麗な数字を見て、「お、系統多様性も改善したのでは?」と
**一瞬、勘違いしかけた**。

これが混同です。正本（lldarwin_stage1_results §3）に書いた通り、`poc_evolution_env.py` の著者コメント
（私が書いたコメント）自身が、その混同を明確に否定しています。

> "monoculture = **BEHAVIORAL** concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is **behavioral spread**. lineage_fixation … to keep it <1 needs
> **QD niching on lineage / PERSONA-FX, not pure novelty**"

整理すると、私が混同しかけた 3 つの「多様性」は、まったく別物でした。

1. **行動多様性（behavioral diversity）** — genome 空間での振る舞いの広がり。`diversity_l2` で測る。
   **novelty が効く指標**。0.05 が改善したのはこれ。
2. **系統多様性（lineage diversity）** — どの founder（岡潔・グロタンら）が生き残っているか。`founder_counts`。
   **novelty では構造的に改善しない**。novelty も lexicase も「既存個体の保存」しかできず、
   一度絶滅した系統を復活させる機構を持たない。だから中立浮動（Kimura）で monoculture に向かうのは
   **理論的に正常**。崩壊ではなく、想定内。
3. **実 LLM 知能多様性（real intelligence diversity）** — 実モデルが本当に多様な賢さを持つか。
   **proxy では一切測れない**。Stage2 の実 LLM 評価が担う領域。

つまり「0.05 に改善した」の正体は **(1) 行動多様性のみ**。(2) も (3) も、その数字とは無関係だったのです。
私が一瞬「系統も改善した?」と思いかけたのは、**(1) を見て (2)/(3) も良くなったと早合点した**から。

これこそ Goodhart の法則の、設計者側バージョンです。
指標（行動多様性 0.05）を見て、それが測っていない別の能力（系統生存・実知能）まで良くなったと
**人間が勝手に解釈してしまう**。proxy が真能力と乖離するだけでなく、**proxy を読む人間の解釈も乖離する**。
反証回でこれを晒すのは、痛い。でも、晒さなければ honest disclosure ではない。

##### 3.3 「何を測った 0.05 か」を、対比で見る

言葉だけでは伝わりにくいので、**「何を測ったか」を 2 枚の SVG で対比**します。

まず、**行動多様性は本当に改善した**（これは事実・誇張なし）。下は中立貯蔵庫 OFF の系統支配ストリーム。
最終的に **furuse 71% / friston 29% の 2 系統に崩壊**しています。行動が多様でも、系統はこの通り。

![reservoir OFF: 2 系統に崩壊](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

そして下が、**系統側の対策（中立貯蔵庫 ON）を入れた後**。**全 8 系統が並存**します
（millidge / von-neumann / oka-kiyoshi / grothendieck … が生き残る）。

![reservoir ON: 全 8 系統が並存](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

この 2 枚の対比が、本記事の心臓です。
**同じ「0.05 の行動多様性」でも、左（OFF）は系統が崩壊し、右（ON）は系統が並存する**。
つまり 0.05 という行動多様性の数字は、**系統がどうなっているかを一切語っていなかった**。
別の機構（lineage-niched QD / 中立貯蔵庫）を足して、初めて系統が救われた。

「何を測った 0.05 か」——答えは「**行動だけ**」。系統は別の眼鏡で見なければ見えなかった。これが正直な答えです。

##### 3.4 対策はあるが、問題は消えない

設計には Goodhart 対策を織り込んであります。

- proxy は **mechanism feasibility 検証に限定**し、production 能力を主張しない。
- **実 LLM/VLM 評価（Stage 2）を本質**とする。
- **neutral shadow 対照（Bedau）** で見かけの改善を疑う（中立変異だけのシャドウ集団と比べ、
  本当に選択が効いているか確認する）。
- **down-sampling** で毎世代 case をかく乱 + **OOD 軸**で過学習を相殺。

> 🍵 **休憩ポイント（90 秒）**: 「対策があるなら、もう問題ないのでは?」——いいえ、ここが肝心。
> 対策は**乖離を遅らせる**だけで、**proxy が真能力でないという事実は消えません**。
> 風邪薬は症状を抑えるが、ウイルスそのものは消さないのと同じ。だから私は「proxy で LLM が賢くなった」とは
> **口が裂けても言いません**。言った瞬間、半年後に赤っ恥をかくのが見えているので。お茶を一杯。

---

#### 4. 反証 3 — 設計者依存性: 「多様性の方向」は誰が決めた?

##### 4.1 メタな疑い

ε-lexicase の case、QD の behavior 記述子、novelty の距離尺度、minimal-criterion の基準値——
これらは全部、**「多様性の方向」を設計者（私）が決めています**。

つまり lldarwin が生む多様性は「**設計者が想定した軸の中での**多様性」であって、
生物進化級の**未想定創発（unanticipated emergence）**ではない。
Taylor et al. (2016) が open-endedness の限界として指摘する通り、
「人間が定義した尺度の中で多様」なのと「定義の外に飛び出す」のは、まったく別の話です。

たとえば私が「行動多様性」を `diversity_l2`（genome 空間の L2 距離）で定義した瞬間、
進化は「**L2 距離が大きくなる方向**」に多様化します。でもそれは私が引いた座標軸の上での多様性であって、
私が想像もしなかった軸（たとえば「ユーモアのセンス」とか「沈黙の使い方」とか）での多様性は、
**そもそも測定対象に入っていない**ので、生まれても気づけない。

> 🤔 **たとえ話（金魚の池）**:
> 金魚すくいの店主が「赤い金魚と黒い金魚、両方残るように選ぼう」と決めて掬う。
> 確かに赤も黒も池に残る。多様性、達成。…でも、その池に**緑の金魚**が突然変異で生まれても、
> 店主の網は「赤か黒か」しか見ていないので、緑は**評価されずに掬われ損なう**。
> 設計者が決めた軸の外側の創発は、最初から眼中にない。これが設計者依存性です。

##### 4.2 受容 — 勝てる軸を限定する

ではどうするか。**未想定創発を主張しない**、というのが正直な答えです。

lldarwin は「**検証可能性のない多様性の地図**」を狙うのであって（差別化軸 DIFF-1）、
strong / unbounded open-endedness は主張しない（SCOPE と整合）。
「人類未踏の創発をやってます!」と言えば派手ですが、それは嘘になる。
**勝てる軸を限定する**——認知スタイル・文化的スタイルといった「検証可能性のない多様性」を地図化することに
価値を絞る。これが lldarwin が誠実に主張できる範囲です。

派手な主張を捨てる勇気が、honest disclosure の核心でもあります。

---

#### 5. 反証 4 — minimal-criterion と QD 自身のトレードオフ

淘汰器の各部品にも、固有の弱点があります。設計書 §7.1 の受容済み限界を一つずつ解説します。

##### 5.1 minimal-criterion の停滞⇄崩壊

minimal-criterion（最低基準 gate）は「基準を満たさない個体は繁殖させない」仕組みですが、
**基準の高さがそのままトレードオフ**になります。

- **基準が低い** → ほぼ全員が通る → 選択圧ゼロ → **停滞**（#25 の飽和と同じ構造）。
- **基準が高い** → ほとんど誰も通らない → **全滅**（実証あり。全員 gate で落ちると次世代が作れない）。

ぬるま湯か地獄か。**対策**: criterion を固定値でなく**集団分位点で適応**させる（例: 下位 30% を落とす）。
さらに全員 fail なら gate を無視する安全弁を入れる（`MultiPressureSelector` 実装済）。

##### 5.2 QD の次元の呪い + アーカイブ飽和

QD（MAP-Elites）は behavior 記述子で cell を切りますが、**記述子が高次元だと cell の大半が空**になる
（次元の呪い）。また長期間回すと全 cell が埋まり、新規性が頭打ちになる（**アーカイブ飽和**）。
これは人工生命の古典 Avida / Tierra でも観測された現象です。

**対策**: 記述子を**低次元に縮約**（DESC-1, JL 射影）+ 飽和を **Bedau 統計で監視**し、
「**飽和＝失敗**」として正直に記録する（飽和を「もう探索しきった証拠」と都合よく解釈しない）。

##### 5.3 lexicase のスケール限界

ε-lexicase は case 数が増えると**計算コストが増大**し、しかも**ノイズで実質ランダム選択化**する。
case が多すぎると、たまたま順序の先頭に来た case で勝者が決まり、選択がサイコロに近づく。

**対策**: **down-sampled lexicase**（毎世代 case の部分集合だけ使う）でコスト削減 + 環境かく乱。

##### 5.4 トレードオフは実測で「見える」

これらのトレードオフは机上の空論ではなく、**実測で現れます**。
中立貯蔵庫の「再投入頻度（reinject_interval）」を変えた sweep がその好例。

| interval | named 系統生存 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**（毎世代） | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84（最大）** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**非自明な発見**: 行動多様性（diversity_l2）は interval を上げるほど単調増加せず、**interval=5 でピーク**を打つ。
10/20 はむしろ低下する。理由は——系統を放置しすぎる（interval を上げる）と、
貯蔵庫由来の多様性注入が減り、かつ少数系統が固定して diversity も伸びなくなる。
ちょうどいい「放置加減」が真ん中にある、という非線形な世界です。

![再投入頻度 sweep: diversity は interval=5 でピーク（非単調）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep.svg)

運用指針はこうなります——**系統保持を最優先するなら interval=1（8/8 全系統生存）**、
**系統保持と行動多様性を両立させたいなら interval=5（5/8 保持しつつ diversity 最大）**。
最適点は fitness / 集団規模に依存するので、本番では再較正が要る。
「どれか一つの正解」ではなく「目的次第で動く最適点」だ、というのが正直な結論です。

##### 5.5 honest 留保 — 「生存」は「生命維持」かもしれない

ここで、もう一つ正直に書いておくべき留保があります。
中立貯蔵庫が全 8 系統を生かしたのは事実ですが、**その「生存」の質を疑う**必要があります。

正本（§4.1 / §4.2）に書いた通り、貯蔵庫は「系統別 best-ever genome（frozen elite）を再投入する」機構です。
強い系統は実際に子孫を増やして繁殖している。一方、弱い系統（各 1 体）の「生存」は、
**再投入由来であって、能動的な進化ではない**。言うなれば、**繁殖ではなく生命維持装置**。

これは中立貯蔵庫の定義通りの正当な挙動（代表を保持し、再結合可能にする）です。
でも「全 8 系統が**活発に進化し続けている**」とは主張しません。
「全滅は防いだ。だが弱系統は ICU で延命中」——これが正確な表現です。

> 🤔 **たとえ話（落語風）**:
> 大家「長屋の住人が一人も欠けず 8 人全員そろっておりますな、めでたいめでたい」
> 八っつぁん「へえ。ただ、半分は息してるだけで店賃も払わず寝込んでまして…」
> 大家「**それは『住んでる』ちゅうより『置いてある』だろ!**」
> 八っつぁん「まあ、追い出すよりはマシかと…」
> ——全員いる、は事実。全員が活躍してる、は嘘。この線引きが honest disclosure です。

---

#### 6. Stage2 — proxy から「実」への橋

反証ばかりでは、設計が前に進まないように見えるかもしれません。
でも反証で足場を固めたからこそ、次の一歩に意味が出ます。それが **Stage2: 実 LLM 評価**です。

##### 6.1 proxy 軸（mechanism feasibility）

まず Stage2 の前半として、LLM の苦手 5 軸を **proxy（決定論 heuristic, LLM 非依存）**で plugin 化しました。

| pressure（LLM 弱点） | 関連思考因子（case） |
|---|---|
| typo_robustness（ノイズ耐性） | consistency / reality_link / uncertainty |
| polysemy_wsd（多義語） | multiview / consistency / reality_link |
| multistep_robustness（多段推論） | structurize / closed_loop / self_extend |
| calibration（信頼度推定） | uncertainty / provenance |
| context_management（無関係文脈耐性） | consistency / provenance / recompose |

計 14 case を breakdown に出力し、lldarwin の ε-lexicase が**集約せず軸ごとに specialist を淘汰**します。
下が、その proxy 軸の母集団平均推移です。

![Stage2 proxy 軸の推移（mechanism feasibility）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes.svg)

ただし——ここまで散々言ってきた通り——**これは proxy**。
個体は実 LLM ではなく genome なので、この pressure は「genome がその弱点に関連する思考因子を
どれだけ備えるか」の**振る舞い代理**にすぎません。**production の LLM 能力は測っていない**（mechanism feasibility のみ）。
SVG にも "PROXY" と焼き込んであります。Goodhart リスクは、ここでは受容済みの限界として明示します。

##### 6.2 実 on-prem LLM 評価（proxy→real の橋）

そして本記事で初めて報告できる前進——**実 LLM 評価が動きました**。

localhost の ollama（llama3.2:latest）が到達可能と判明したため、`real_pressures.py` で
**個体 → 実 LLM 写像**を実装（Promptbreeder 系）。仕組みはこうです。

- 個体の `c_prompt`（PromptChromosome）を **system prompt** に変換する
  （skill_set → 指示文 / prompt_template_id → 推論スタイル / language_style → 語調）。
- 固定 LLM（llama3.2）にその system prompt を被せ、5 苦手軸の**実タスク**を解かせて採点。
- つまり **LLM 本体は固定し、prompt 戦略（genome）を進化**させる。
  「どの prompt 戦略が LLM の弱点を緩和するか」を**実測で淘汰**する。

結果、**実選択信号が確認できました**。
CoT + structure 戦略（`chain_of_thought` + structurize + loop）が、
llama3.2 の **multistep を 0.0 → 1.0 に改善**（terse な戦略は 0.0 で失敗、score 0.80→1.00）。
proxy の幻ではなく、**実 LLM で「prompt 戦略の進化が弱点を緩和する」ことを実証**できた。

![Stage2 実 on-prem LLM 軸の推移（prompt 戦略進化）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

proxy 軸（前掲）と実 LLM 軸（上）を**並べて見る**と、「proxy で測った形」と「実測の形」が
どう違うかが目で分かります。proxy は機構が回ることを示すだけ。実 LLM は、実際にモデルの弱点に対して
prompt 戦略がどう効くかを示す。**この 2 枚の違いこそが、本記事の主張の実物**です。

##### 6.3 だが、ここでも正直に

実 LLM で動いた——でも、ここでもサイレンを鳴らします。留保は 4 つ。

- **(a) c_prompt のみ fitness 関与** — persona / c_factors は中立で、fitness には絡んでいない。
  系統は reservoir が維持し、初期選択は novelty が担う。つまりこれは「**prompt 戦略の進化**」であって
  「persona の進化」ではない。
- **(b) 全 founder の初期 c_prompt が同一（default）** — だから探索は mutation 駆動。
  founder ごとに prompt を多様化させるのは今後の改善点。
- **(c) 小バッテリ（軸あたり 2 問）** — ノイジーな推定。「multistep が 0→1」も、問題数が少ないので
  これだけで一般化を主張はできない。
- **(d) on-prem only（measurement purity）** — localhost ollama 限定で、
  **一般的な LLM 能力の主張ではない**（[[feedback_llive_measurement_purity]]）。

12h 連続ランも起動しました（`--fitness real-pressure --selection lldarwin --novelty
--lineage-reservoir --genome3d`）。wallclock 12h で safely 停止（snapshot 済 → `--resume` 継続可）。
でも「12h 回したから本物」とは言いません。回した、は事実。本質を測りきった、は嘘。
**proxy→real の橋は架かった。だが渡り終えてはいない。**——これが Stage2 の正直なステータスです。

---

#### 7. 結論 — どこまで主張してよいか（線引き）

「LLM の弱点を proxy fitness にすれば進化で克服できる」は**楽観的**でした。
反証で削った結果、lldarwin の価値主張を次の 3 点に**限定**します。

1. **(a) proxy は mechanism feasibility のみ** — 進化の配管が動くことの検証。production 能力は主張しない。
2. **(b) 実 LLM/VLM 評価が本質** — 知能の選択圧は個体 → 実モデル写像（Stage 2）が担う。
   ここに橋は架けた。だが本格的に渡るのはこれから。
3. **(c) 多様性の地図化** — 勝てる軸を「検証可能性のない多様性（認知・文化スタイル）の地図」に限定する。
   未想定創発は主張しない。

これが honest disclosure です。**失敗（#25）も、自分の混同（§3.2）も、限界（#5/§6.3）も、消さずに残す**。
派手な勝利宣言を一つも書かなかったこの記事こそ、進化アークで一番誠実な回だと、私は思っています。
次に進む足場は、この線引きの上にしかありません。

---

#### 8. 教訓（永久保存）

- **良い結果（0.05 改善）ほど内訳を疑う。** 「proxy 行動多様性」は「系統多様性」でも「実 LLM 知能多様性」でもない。
  数字を見て別の能力まで良くなったと早合点した自分が、Goodhart の生きた標本だった。
- **「測る」を直さず「淘汰する」だけ高級にしても無駄。** 飽和した眼鏡には、どんな選択圧も効かない。
  眼鏡を磨くのが先、淘汰器を載せるのが後。
- **Goodhart's law は進化の天敵。** 指標を目標にした瞬間、進化はそれをハックする。
  しかも指標を読む人間の解釈まで一緒に乖離する。
- **設計者が多様性の方向を決めている以上、未想定創発は主張しない。** 勝てる軸を限定するのが誠実さ。
- **「生存」は「生命維持」かもしれない。** 全 8 系統が残った、は事実。全員が活発に進化中、は嘘。
  動詞の選び方一つに honest disclosure が宿る。

> **次回予告**: 反証で足場を固めたら、次は Stage 2 の本格化（実 LLM/VLM 評価, on-prem ollama）。
> proxy の幻でなく、実モデルの知能多様性を本当に選択圧にできるか。
> 「multistep 0→1」を小バッテリの偶然で終わらせず、再現可能な選択信号に育てられるか。ここからが本番です。

---

#### 9. 関連
- 連載 #25「私とフリストンだけが残った」— 失敗の記録（本記事の起点）
- 連載 #26「lldarwin の設計」— 淘汰器（本記事が反証する対象）
- 実装 commit（llive）: Stage1 = `8060204` / lineage-reservoir PoC = `0d0537d` /
  Stage1.5（EvolutionLoop 組込）= `b03cbda` / Stage2（実 LLM real-pressure）= `2fb2912`
- 実測正本: `../../research/lldarwin_stage1_results_2026_05_26.md`（§3 honest disclosure / §4.1–4.5）
- 設計正本: `../../vision/LLDARWIN_DESIGN.md` §7 / §7.1（反証調査・受容済み限界）
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_implementation_status_record]]
- 参考: Goodhart's law / La Cava 2019（ε-lexicase, arXiv 1905.13266）/ Taylor et al. 2016（open-endedness の限界）/
  Bedau（neutral shadow）/ Kimura（中立進化説）

---

## 6. 進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで、人工進化はどう可視化されてきたか

### 進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで

> **コンセプト hook**: 私が #25〜#27 で延々と語っている「人工進化」。実はこれ、半世紀以上の歴史がある
> 研究分野です。そして面白いのは、**進化の研究は常に「見せ方（可視化）」と二人三脚で進化してきた**こと。
> 1970 年の白黒の点滅セルから、2024 年の連続流体・3D ガウシアンまで。「進化を見せる技術」の系譜を、
> 教養として一気に辿ります。FullSense の進化可視化（思考因子グラフ上の系統樹）が、この系譜の
> **どこに立っているのか**を最後に位置づけます。

---

#### 0. なぜ「可視化」が進化研究の主役なのか

進化は **長時間・大集団・多世代**の現象。数字の羅列では「何が起きたか」が掴めません。
だから人工進化の歴史は、ほぼそのまま **「進化を一目で理解させる表現の発明史」** です。

> 🍵 **休憩ポイント**: この記事は数式ゼロ・コードほぼゼロの「散歩」回です。コーヒー片手にどうぞ。
> 各時代の「見せ方のブレイクスルー」だけ拾っていきます。

---

#### 1. 1970: Conway のライフゲーム — 「単純ルールが模様を生む」

- **何**: 2 次元セルオートマトン。生死 2 状態 × 近傍 8 セルの単純ルール。
- **見せ方の発明**: **格子の点滅そのものが可視化**。グライダー・ブリンカー・グライダーガンといった
  「動く模様」に名前がついた = 人間が**創発パターンを目で名づけた**最初期の例。
- **限界**: 進化（自然選択）ではなく決定論的な展開。しかし「単純ルール → 複雑な見た目」の衝撃が分野を開いた。

**節の肉付け予定**: グライダーが「移動する構造」として認識される=可視化が概念を生んだ好例として深掘り。

---

#### 2. 1991: Tierra（Tom Ray）— 「コードが生き物になる」

- **何**: 仮想 CPU 上で自己複製する機械語プログラムの生態系。寄生体・免疫・最適化が**勝手に創発**。
- **見せ方の発明**: **メモリマップの可視化**。各プログラムが占めるメモリ領域を色で塗り、
  寄生体が宿主に食い込む様子を「地図」として見せた。**「コードの生態系」を空間として描いた**。
- **意義**: 「自己複製子の自然選択」を計算機内で初めて観測。open-ended evolution 研究の出発点の 1 つ。

---

#### 3. 1994: Avida（Adami / Ofria）— 「進化を計測する」

- **何**: Tierra の系譜を継ぐデジタル生命プラットフォーム。論理演算をこなすと報酬（CPU 時間）を得る。
- **見せ方の発明**: **系統樹（phylogeny）と適応度地形の可視化**。「どの祖先からどの子孫が分岐したか」を
  ツリーで描き、複雑形質（EQU 演算等）が段階的に進化する過程を**追跡可能**にした。
- **意義**: 「不可避なステップを経て複雑性が進化する」を実証（Lenski et al. 2003, Nature）。
  **進化を物語でなく計測対象にした**。FullSense の monoculture 監視（max_lineage_share / archive 成長）は
  この「計測する進化」の直系です。

> 🤔 **たとえ話（漫才風）**:
> ボケ「Avida は進化を数字で測れるようにした」
> ツッコミ「つまり進化に通知表をつけたんやな」
> ボケ「せや。#25 で私が『満点インフレで通知表が壊れた』言うてたのは、まさに Avida 級の計測の話や」

---

#### 4. 1994: Karl Sims「Evolved Virtual Creatures」— 「進化を映像で魅せる」

- **何**: 3D 物理シミュレーション内で、形態（block の繋がり）と神経制御を**同時に進化**させ、
  泳ぐ・歩く・物を取り合う生き物を生んだ。
- **見せ方の発明**: **3D アニメーション映像**。論文の図でなく**動画**で見せたことが衝撃を呼んだ。
  「進化が設計した、誰も予想しなかった奇妙な歩き方」を**人間が直感的に面白がれる**形にした。
- **意義**: 進化可視化が「研究者向けグラフ」から「**誰もが見て驚く映像**」へ。
  FullSense のデモ哲学（[[project_f25_demo_polish]]「動きで魅せる」）の精神的祖先。

> 🍵 **休憩ポイント**: ここまでで「白黒の点 → メモリ地図 → 系統樹 → 3D 動画」と、
> 見せ方が**抽象 → 具象 → 動的**へ進化したのが見えれば OK。後半は現代編です。

---

#### 5. 2019: Lenia（Bert Chan）— 「連続的な人工生命」

- **何**: ライフゲームを**連続空間・連続時間・連続状態**に一般化。滑らかに動く「生き物のような」
  パターン（orbium 等）が多数発見された。
- **見せ方の発明**: **連続フィールドの滑らかなレンダリング**。離散の点滅から、生物の細胞のように
  しなやかに動く流体的表現へ。「人工生命が**美しい**」という新しい訴求軸を開いた。
- **意義**: 可視化の質そのものが研究の発見力を上げた例。美しく見えるからこそ新パターンを人間が気づける。

---

#### 6. 2020s: Quality-Diversity の可視化 — 「多様性を地図にする」

- **何**: MAP-Elites / CMA-ME 等の QD アルゴリズム。単一 best でなく**多様な高性能解の集合**を生む。
- **見せ方の発明**: **behavior space のヒートマップ**。2 軸の behavior 記述子を格子に取り、
  各 cell の elite を色で塗る = 「**多様性そのものを地図として可視化**」。
- **意義**: FullSense / lldarwin の QD archive 可視化はここに直接立脚。
  「1 cell でも残れば全滅しない」を**地図の空白 vs 充填**で一目で見せられる（#26 で詳述）。

---

#### 7. 2020s〜: 3D Gaussian Splatting（3DGS）— 「進化の状態を空間表現する」（FullSense の賭け）

- **何**: 元来は新視点合成（NeRF の系譜）の技術。点群を 3D ガウシアンで表現し高速・高品質に描画。
- **FullSense の着想**: 進化集団の**高次元 genome / pressure profile を 3D ガウシアン空間に写像**して
  「進化の状態を立体的に見せられないか」という探索（[[project_precision_metrology_llm]] の SH 係数連携と同根）。
- **位置づけ**: これは**まだ研究的賭け**であり、確立技術ではない（honest disclosure）。
  本記事の系譜の「最先端の縁」に置く実験です。

---

#### 8. FullSense の進化可視化はどこに立つか

| 時代 | 見せ方の核 | FullSense での継承 |
|---|---|---|
| Conway 1970 | 点滅セル = 創発の名づけ | （概念的祖先） |
| Tierra 1991 | メモリ地図 | 系統占有率の地図化 |
| Avida 1994 | 系統樹 + 計測 | monoculture 監視 / lineage tree |
| Karl Sims 1994 | 3D 動画 | 「動きで魅せる」デモ哲学 |
| Lenia 2019 | 連続フィールドの美 | animated SVG 表現層 |
| QD 2020s | behavior 地図 | lldarwin QD archive 可視化 |
| 3DGS 2020s〜 | 3D 空間表現 | （研究的賭け） |

FullSense の進化可視化（**思考因子グラフ上の系統樹 + animated SVG**）は、
**Avida の「計測する系統樹」と Karl Sims の「動きで魅せる」と QD の「多様性の地図」を、
ターミナル / ブラウザで再現する**位置にあります。半世紀の系譜の、ささやかだが正統な末裔です。

> **次回予告**: 系譜を辿ったら、次は実装。FullSense の系統樹 animated SVG が、
> 上記のどの「見せ方」をどう取り込んだかを、実際の evolution.svg を題材に解説します。

---

#### 9. 関連
- 連載 #25〜#27 — 本記事の進化可視化の「中身」（monoculture / lldarwin / 反証）
- 関連 memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- 参考: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #25-27 の Qiita URL cross-link / en・zh・ko 版展開 -->
<!-- KEY MESSAGE: 進化研究は可視化と二人三脚。点滅→地図→系統樹→3D動画→連続→QD地図→3DGS。FullSense は Avida+Sims+QD の末裔。 -->
<!-- NOTE(事実整合): 年代/人名は一般的な人工生命史の通説に準拠。3DGS の進化可視化応用は FullSense の研究的賭けであり確立技術でない旨を明記済。 -->

---

## 7. AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制と検証規律

### AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制

> **コンセプト hook**: FullSense（llmesh / llive / llove）は私ひとりの個人開発です。でも実態は
> 「ひとり」ではない。**AI コーディングエージェントを主・別の AI エージェントを部下**にした
> 2 階層の開発体制が回っています。主が **Claude Code**、部下が **Codex CLI**。
> 「AI が AI に仕事を振って、その成果を AI が検証する」——この多重委任を、暴走させずに
> どう規律するか。本記事は人間 1 + AI 2 の「二本柱」運用の実践記です。
>
> キーワードは **オーケストレータ / 配下 worker / 検証規律 / 並列化**。

---

#### 0. 三行であらすじ

- **Claude = オーケストレータ**（計画・実装・委任・**検証**）/ **Codex = 配下 worker**（実行・レビュー・調査）。
- 「二本柱」= 対等ではなく **Claude 主導 + Codex 配下**。司令塔は 1 つに保つ。
- 鉄則: **外部 AI の finding は実コード / 一次情報で 1 件ずつ検証してから採用**（鵜呑み禁止）。

---

#### 1. なぜ「二本柱」なのか — 動機

個人開発で AI エージェントを 1 つだけ使うのは、もはや普通です。なぜ 2 つ目（Codex）を**部下として**足したのか:

1. **ベンダー分散・冗長性** — 単一エージェントの課金変更 / 障害 / quota 枯渇のヘッジ。
2. **クロスレビュー** — 同じ設計を別系統の AI に見せ、セカンドオピニオンを取る（盲点削減）。
3. **並列 worker** — 独立サブタスクを配下に投げ、主は最重要タスクに集中。

> 🍵 **休憩ポイント**: 「AI を 2 つ使う = 2 倍賢い」ではありません。**指揮系統を 1 つに保つ**のが肝。
> 烏合の衆にすると、むしろ遅くなる。本記事の半分は「どう統制するか」の話です。

---

#### 2. 役割分担 — オーケストレータと配下 worker

![人間→Claude（主＝オーケストレータ）→Claude サブエージェント並列 / Codex CLI 配下 worker の階層図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy.svg)

- **Claude（主）の責務**: タスク分解・依存性判定・独立タスクの並列起動・進捗監視・**成果の検証**・一括コミット。
- **Codex（配下）の責務**: 委任された範囲の実行。非対話委任 = `codex exec -s read-only "<prompt>"`。
- **司令塔は常に Claude**。Codex は Claude を経由してしか全体に影響しない（直接コミットさせない）。

**節の肉付け予定**: Claude サブエージェント並列（[[feedback_parallel_first_execution]]）と Codex 配下委任の
使い分け表。「同 file は直列・独立 file は並列」「git 操作は orchestrator が一括」（[[feedback_agent_no_git_parallel]]）。

---

#### 3. 検証規律 — 「鵜呑み禁止」が体制の生命線

二本柱で最も危険なのは **AI の出力を AI が無検証で採用する**こと。誤りが増幅されます。だから鉄則:

> 外部 AI（Codex / Copilot / Gemini）の finding は **実コード / 一次情報で 1 件ずつ検証**してから採用する。

実例: 本連載 #26（lldarwin 設計）で、既存コード資産の調査（`mating.py:139 LexicaseSelection` は
「実装済だが未配線」等）は配下に調べさせましたが、**配線点や行番号は主（Claude）が実ファイルで確認**してから
設計書に書きました。「Codex がそう言った」では設計の根拠にしない。

> 🤔 **たとえ話（落語風）**:
> 親分「おう、あの関数、配線済みかい?」
> 子分「へい、未配線でさぁ」
> 親分「……お前の『へい』は信用ならねえ。俺が自分でソース見てくる」
> ——これが検証規律。子分の報告は**起点**であって**結論**ではない。

**節の肉付け予定**: 検証の 3 段（finding 受領 → 実コード / 一次情報で確認 → 採用 or 棄却）と、
レビューラッパー（`tools/copilot_review.sh` 等の読み取り専用レビュー）の位置づけ。

---

#### 4. 並列化の作法 — 暴走させない統制

複数 worker（Claude サブエージェント + Codex）を同時に回すときの規律:

- **2〜4 並列が安全圏**（主の context 余裕・コミット衝突なし）。5+ は file レベル独立性を厳格管理。
- **独立タスク抽出** = 依存なし + file / module / repo レベルで非接触。同 file は直列（file lock 的）。
- **不可逆操作（削除 / push / submodule 改変）は 1 件ずつ人間確認**。配下に勝手にやらせない。
- **git 操作は orchestrator が一括**。並列 worker には git を触らせない（競合回避）。

> 🍵 **休憩ポイント**: 「AI をたくさん並べれば速い」の罠。**主の context（注意の総量）が律速**です。
> 5 体並列にしても主が捌けなければ意味がない。脳のワーキングメモリと同じで、同時把握できる数には上限がある。

---

#### 5. アンチパターン（やってはいけない）

- 「1 つずつ確認しながら進めます」と宣言してから黙々と直列実行（並列化の機会損失）
- 配下に投げず主の context だけで全部こなす（context 爆発）
- 並列起動した worker の結果を待たずに主が同じ file を触る（競合）
- 2 worker に同じ file を書かせる委任（独立性の判定漏れ）
- 配下 AI の finding を無検証で設計や実装に採用（誤り増幅 = 二本柱最大の事故）

---

#### 6. この体制で実際に何が回ったか（FullSense の実例）

- **設計クロスレビュー**: 進化設計 / 要件 / PoC を配下にレビューさせ、主が実コードで検証して採用判断。
- **既存資産調査**: lldarwin の既存部品（loop.py / mating.py / nsga2.py 等）の所在を配下に調査 → 主が確認。
- **並列サブタスク**: 記事骨子・コード調査・要件整理を独立タスクとして並列化（本連載自体がその産物）。

> 🍵 **休憩ポイント**: 「人間 1 + AI 2」で個人開発の生産性がどう変わったか、という主観も最後に正直に。
> 速くなった面（並列・冗長性）と、増えた負荷（検証コスト・統制コスト）の**両方**を honest disclosure。

---

#### 7. 教訓

- **指揮系統は 1 つに保つ。** 二本柱は対等でなく主従。司令塔の分裂は事故のもと。
- **検証規律が体制の生命線。** AI が AI を無検証で信じる連鎖が最大のリスク。
- **並列度は主の context が律速。** 体数でなく捌ける量で決める。
- **不可逆操作と git は人間 / orchestrator が握る。** 配下には可逆な仕事だけ任せる。

> **次回予告**: 二本柱で回した進化設計（#26 lldarwin）を、配下 Codex + on-prem ollama で
> Stage 2（実 LLM 評価）まで進める。多重 AI 委任が「研究の実装速度」をどこまで上げるか。

---

#### 8. 関連
- 連載 #26「lldarwin の設計」— 本体制で回した実例
- 関連 memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #26 の Qiita URL cross-link / en・zh・ko 版展開 -->
<!-- KEY MESSAGE: 人間1 + AI2 の二本柱。Claude 主導 + Codex 配下。検証規律(鵜呑み禁止)が生命線。並列度は主の context が律速。 -->
<!-- NOTE(事実整合): Codex は ChatGPT Pro $100/月で契約方針(promo 〜5/31)。導入状態(CLI 0.117.0 / quota 枯渇 / login 切替予定)は reference_codex_two_pillar 準拠。実応答未取得の段階である旨に注意して脚色しないこと。 -->

---

## 8. llcore — Transformer のコアを CPU で進化させる: Verified Neural Architecture Evolution の最小 PoC battery

### (連載 #32) llcore CPU PoC battery 完成

#### TL;DR

- Transformer の **コア計算 (state update / 学習則 / 認知駆動 Δ)** を進化対象にする研究フレームワーク `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 独立路線) の **CPU PoC battery 完成**
- **5 PoC / 39 falsifiable gates / 76 tests / Codex pair-review 5/5 Green-light** で機構実証
- **Z3 で構造変異を online gate** = 進化探索の selection pressure に SMT を組込んだ先行未発見 (事前調査 RAD 14 分野 + Agent A-D 確認)
- 投稿先候補: TMLR (本命) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

#### なぜ作ったか

LLM 重みは凍結が標準だが、**コア計算アルゴリズム自体は人手設計に固定**されている。AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge など architecture/algorithm 探索は進んだが:

1. **個人 compute では計算リソース不可能** (TinyLlama 1.1B from scratch = $140k / 90 日 / 16×A100)
2. **探索中の安全性保証なし** = 数値不安定な architecture を生み出して時間浪費
3. **検証付き探索は静的 verification (Reluplex/Marabou/α,β-CROWN) と分断** — 進化ループ内 SMT online gate の研究は未発見

#### 確定独自軸 (事前調査で negation work なし)

mechanism 実証済 (4 軸):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **state update 規則を遺伝子化 RWKV-style** (Stage 0a v2)
3. **factor_hook (認知状態 → SSM Δ)** (Stage 2a mock)
4. **自前進化器 + verifier 基盤** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / VNN-COMP 新カテゴリ提案。

#### PoC レダー (5 stage / 39 gates 全 PASS)

| PoC | 内容 | キー数値 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 自前 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

#### v1 の失敗から学んだこと (honest disclosure)

PoC 0a v1 は `decay*s + mix*x*tanh(gate_str*s)` で **state=0 が fixed point の zero attractor** = G1-G5 形式 PASS だが情報伝達ゼロ。Claude 単独で見落とした設計問題を **Codex (gpt-5.4) と gem-critic の独立 verdict** が検出し RWKV-style に v2 redesign。

→ **5 PoC 中 4 件で Claude 単独では見落とした設計問題を Codex pair-review が検出**。構造破綻防止に相互レビューが機能した実例。

#### 次の選択肢

a. Stage 3 kernel 多様化 (rwkv/mamba/hopfield/linear-attn を遺伝子化)  
b. Stage 4 学習則 (FF/EP/PCN/Hebb) を gene 化  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. PrediPrune+Quokka で Z3 gate 高速化  
e. FlashEvolve で 3.5-5x wall-clock 高速化  
f. 論文化 (TMLR + GECCO 2027)

#### Honest 留保

- mock 中心、実 LLM/重み接続は GPU/新 PC 待ち
- 1 step scalar invariant の over-approx proof 段階、多次元・多 step は post phase
- tanh 上界近似は保守的 (sound だが完全でない)

---

**Tags**: 進化計算 / 形式検証 / Z3 / RWKV / state space model / CPU研究  
**関連**: 連載 #14-31 (llive lldarwin v0.B-E + 観測+governance + lleval)  
**Project**:  (PyPI llmesh-llcore 0.1.0a0)

---

## 9. llcore — 「進化で AI を設計するとき、選り分けて育てる工夫は本当に要るのか?」を 3 実験で詰めた話 (第三軸 ③ 決着 Step D)

### (連載 #33) 整いすぎた結果は、勝ちではなく警報 — 第三軸 ③ を proper power で決着させた一日

#### TL;DR

- 問いは **「AI のコア計算を進化で探すとき、"選り分けて分けて育てる工夫" (= 進化の③ 適者生存/分離) は本当に要るのか」**。
- **合成した "谷つき (欺瞞) 地形" では③は圧勝** (過去実験で Cliff δ=+1.0)。③ は機構として本物。
- **だが実物に近い CPU proxy 地形を、評価ノイズを物理的にゼロまで落として測り直したら "本当に滑らか (単峰)" で、③ は不要と確定**。「過去の negative は検出力不足 (underpower) ではなく、地形が本当に滑らかだった」が初めて裏付いた。
- 実 multitask 近傍 (C-gen4b) だけ「③ NOT null」の弱い気配が出たが、データを増やすとフラついて **候補止まり** (走行内ドリフト + 多重比較で脆い)。
- 「ある後処理が③を隠している」疑い (K4 ridge clip) は、外したら逆に悪化 → **隠していない、診断的所見に降格**。
- 外部レビュー (Codex) は **ブロッカーなし**で結論を追認。
- 結論を一行で: **「③ が活きるのは地形が欺瞞的なときだけ。今 CPU で測れた実物もどきは、たまたま滑らかだった」**。本丸の決着は GPU (実 LLM 地形) が要るが、それは投資判断。
- **追記 (2026-06-02, §11.5)**: 最後の CPU 抜け道 **kernel 多様化 (BG9) は構造的に閉じた**。kernel 選択は低次元ゆえ強 baseline (RR) が直接サンプルし、③ の niching 優位が原理的に出ない。**③ が効くには "高次元の" 欺瞞地形が要る**と分かり、残る路は GPU full-LLM のみ (それも bet)。
- メタ教訓: **正直さ (honest disclosure) は飾りではなく、研究を前に進める道具だった**。BG9 では「negative を正しく negative と確定する」方向でも同じ規律が効いた。

> ⚠ この記事の数値は、すべて手元 (ローカル) の研究 commit `THIRD_AXIS_SETTLE_VERDICT.md` に紐づく実測です。llcore はまだ公開リポジトリを作っていないので、外部リンクは貼れません。代わりに「どう測ったか」を本文に全部書きます。

---

#### 0. この記事は何の話か (コンセプト)

`llcore` は「Transformer のコア計算 (状態更新則・学習則・認知駆動 Δ) を遺伝子にして、Z3 で壊れないように検証しながら進化させる」CPU 完結の研究フレームワークです (連載 #32 で PoC battery の話を書きました)。

その進化エンジンには、進化の 4 要素のうち **③ (適者生存 selection / 分離 separation)** をどう効かせるか、という設計上の急所があります。多様性を保ってニッチに残す MAP-Elites のような「選り分けて分けて育てる」仕組みです。

問いはシンプルです。

> **その③、本当に要るの?**

要るなら、③ を載せるための重い投資 (最終的には GPU で実 LLM を回す) に意味がある。要らないなら、③ にこだわるのは時間と電気の無駄になる。

この一日 (2026-06-02) で、その問いに **3 つの実験で正面から決着をつけにいきました**。タイトルどおり、結論は「整いすぎた結果は警報」という FullSense の通奏低音に、もう一度引き戻される話です。

— ここまで 30 秒。準備運動おわり。本題へ。 —

---

#### 1. たとえ: 山登りと、だまし地形

数式の前に、地形のたとえで全体像を掴みます (この研究で一貫して使っているメタファーです)。

設計の良し悪しを **地形の高さ** で表します。**高い場所 = 良い設計**。一番高い頂上を探すゲームです。

**地形その1: 滑らかな一つ山 (簡単)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

こういう地形では、素朴な「山登り法 (hill-climbing)」、つまり「今より少し良い方へ動くだけ」で十分に頂上へ着きます。**凝った工夫 (③) は要りません**。

**地形その2: だまし地形 (欺瞞的 deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

ここでは素朴な山登りはニセ頂上で止まります。谷を下る勇気がないからです。

このとき効くのが③ の発想です。**いろんなタイプの登山者を谷のあちこちに残しておく** (= 記憶の宮殿 / MAP-Elites archive)。誰かが谷を「飛び石」で渡って本物の頂上に到達できる、という仕組みです。

**この研究の核心を一言で**: ③ が本当に役立つのは **「だまし地形」のときだけ**。滑らかな一つ山では、③ は無用の長物です。

だから問いは、こう言い換えられます:

> **「進化で AI を設計するとき、実際に出くわす地形は "だまし地形" なのか、それとも "滑らかな一つ山" なのか?」**

これが決まれば、③ が要るか要らないかが決まる。今日はこれを測りました。

---

#### 2. 過去の積み残し — 「③不要」は本当に "不要" だったのか

これまでの実験 (Step C → 梯子段1 → E-A → 谷深さ実測) を通じて、像はだいたいこうでした。

- **合成した欺瞞 corridor では③が圧勝** (3 つの baseline 全てに勝ち、Cliff δ=+1.0)。③ は存在証明済み、機構として本物。
- **実問題に近い proxy 地形では③ negative** (MAP-Elites が random にしか勝てない = 滑らかな地形と同じ症状)。

ところが、ここに 2 つの未解決のしこりが残っていました。

1. **「③不要」は本当に "地形が滑らか" だからなのか、それとも単に "サンプル数が足りなくて差を検出できなかった (underpower)" だけなのか?** ── これを取り違えると、「③ は無力」という過剰一般化をやらかす。
2. 谷深さの直接測定は前回 **N/A (測定不能)** で終わっていた。評価ノイズが谷の深さより大きくて、谷があっても埋もれて見えない、という計器の限界。

つまり「滑らかに見えた」のが **地形の性質** なのか **計器の限界** なのか、決着がついていなかった。ここを詰めるのが Step D です。

— 小休止。ここまでが前提。ここから先が今日やった 3 実験。 —

---

#### 3. 実験の設計 — 3 本立て

| 実験 | 何を測るか | 狙い |
|---|---|---|
| **EXP1** | proper-n 再検定 | サンプル数を本気で増やして、③ の効果が本物か検出力で詰める |
| **EXP2** | 決定論 C1 多峰性 | 評価ノイズを物理的にゼロにして、地形が「だまし地形」か「滑らかな一つ山」かを noise-free で判定 |
| **EXP3** | K4 ridge clip の verdict-flip | 「ある後処理が③を隠している」疑いを検証 |

規律: 全部 `research/step_d_settle/` に隔離、src は無改変、git はオーケストレータが一括。各実験は破綻ゲート (G1 CPU 完走 / G2 再現性 / G3 診断器妥当 / G4 src 不変) を通す。

---

#### 4. EXP2 が決め手だった — 評価ノイズをゼロにすると地形が見える

順番は前後しますが、**一番効いたのは EXP2** なので先に書きます。

前回の谷深さ測定が N/A になった原因は単純で、**「谷の深さ (0.05·|fitness| くらい) ≪ 評価ノイズの揺らぎ」** だったからです。計器のノイズに谷が埋もれて、あるのかないのか分からない。

EXP2 のトリックはこうです。

> ESN reservoir (固定 seed) + ridge readout の closed-form (`np.linalg.solve`) は、**乱数を一切引かない**。だから評価ノイズを機械イプシロン (約 1.11e-16) まで物理的にゼロ化できる。

実測で `eval_noise_std ≤ 1.11e-16` を確認しました。これは「評価のたびに値がブレる」のではなく、浮動小数点の最小単位 (ULP) 由来の誤差で、**実質ゼロ**です。ノイズの霧が完全に晴れた状態で、地形の谷を直接測れる。

結果がこれです (valley_fraction = 谷の割合、大きいほど多峰=だまし地形):

| landscape | 種別 | 次元 | valley_fraction (mean/max) | 多峰? | 判定 |
|---|---|---|---|---|---|
| **ESN_3param** (実 proxy) | real | 3 | **0.000 / 0.000** | **False** (3 seed 一致) | 滑らか=単峰 → ③不要を noise-free で確定 |
| **ESN_perneuron40** (実 proxy) | real | 40 | **0.096 / 0.121** | **False** (3 seed 一致) | smooth 寄り (床 0.2 未満) → ③不要 |
| ctrl_multipeak_dim3 (正 control) | control | 3 | 0.701 / 0.727 | True | 診断器は多峰を検出できる ✓ |
| ctrl_multipeak_dim40 (正 control) | control | 40 | 0.795 / 0.818 | True | 診断器健全 ✓ |
| ctrl_quadratic_dim3 (負 control) | control | 3 | 0.000 | False | 診断器は滑らかを検出できる ✓ |
| ctrl_quadratic_dim40 (負 control) | control | 40 | 0.000 | False | 診断器健全 ✓ |

ポイントは 3 つ:

1. **実 proxy 地形 (3 次元 / 40 次元 とも) は valley≈0 = 単峰**。3 seed で完全一致。
2. **診断器そのものは健全**。わざと作った多峰の正 control はちゃんと多峰 (0.70/0.80) と検出し、二次関数の負 control はちゃんと滑らか (0.0) と検出する。だから「実 proxy が単峰」は計器のバグではなく地形の性質。
3. これで **「過去の③ negative は underpower ではなく、地形が本当に滑らかだったから」** が、実 substrate 上で初めて noise-free に裏付いた。

副次発見も正直に書いておきます。**正 control に使うつもりだった欺瞞 corridor (`make_corridor_eval(d=0.16)`) が、決定論化したら valley=0.0 (単峰判定)** になってしまった。corridor の欺瞞性は「単一 basin の中に閉じ込めて③の behavioral niching で脱出させる」型 (behavioral-reach 欺瞞) であって、**地形の谷 (C1 multi-basin) の欺瞞ではなかった**。corridor は C1 の正 control にならない、という scope の狭まりを実測で確定しました。これは過去の谷深さ校正が「corridor 由来の閾値」を地形多峰性に転送できないことを意味します。

— ここで一服。「正 control が control にならなかった」のは地味にショックでした。が、これも測ってみないと分からなかった。 —

---

#### 5. EXP1 — 実 multitask 近傍だけ「③ NOT null」の弱い気配

次に、実問題に一番近い帯 (C-gen4b = MAP-Elites vs random、実 multitask 近傍) を、サンプル数を本気で増やして再検定しました。

| case | 元 n=15 (監査) | fresh 真再走 | 判定 |
|---|---|---|---|
| **C-gen4b** | diff +0.063 / psd +0.20 / p 0.126 | **n=64: diff +0.0472, 片側 p 0.038, psd +0.188, gate PASS** | **③ load-bearing 候補 (still_inconclusive)** |

fresh seed で n=64 まで回したら **strict gate を 4 条件すべて PASS** しました。つまり監査が「③不要 (inconclusive)」と読んだのは方向としては誤りで、**C-gen4b では③は NOT null の方向**。

…と、ここで勝った気にならないのが今回のキモです。3 つの理由で **候補止まり** にしました。

1. **更新後の検出力 power@n64 = 0.517 < 0.80**。gate は通ったが、確証の基準 (検出力 0.80) には足りていない。
2. **走行内ドリフト (これが効いた)**。累積 p 値の軌跡を追うと: n=40 で初 PASS (p=0.042) → n=60 で p=0.010 と深く有意化 → **n=64 で p=0.038 へ 0.05 境界近くへ戻った**。さらに seed を前半/後半で割ると、**前半 32 seed は diff=+0.0755 (frac_pos=0.625) だが、後半 32 seed は diff=+0.0189、最後の 9 seed は diff=−0.0376 (負)**。PASS は前半 seed に支えられていて、**新しいデータほど逆方向に走っている**。
3. **多重比較**。p=0.038 は α=0.05 では PASS だが、EXP1 の 3 case だけでも Bonferroni α=0.0167 を超過 (FAIL)。③ research family 全体で見ればもっと厳しい。

加えて、効果量の床 (psd) が **構造的天井** にぶつかっていました。C-gen4b の median psd は n=15→0.200, n=255→0.200 で動かない。`P(|psd|≥0.147)` (効果量条件の充足率) は n=255 でも 0.794 で頭打ち。中効果 (psd≈0.20) なので、サンプルをいくら増やしても full gate の検出力が 0.80 を超えない。**つまり「サンプルを増やせば (A) 確定する」という見込み自体が、この proxy 上では薄い**。

結論: **C-gen4b は「③ load-bearing 候補 / still_inconclusive」**。「③ NOT null」という headline は、単発の境界 p=0.038 に寄りかかりすぎ。走行内ドリフトは「候補が偽陽性かもしれない」真の証拠です。

---

#### 6. EXP3 — 「後処理が③を隠している」疑いは、外したら逆に悪化した

最後の疑いはこうでした。「ridge readout の clip (K4) という後処理が、実は③の信号を握りつぶしているのでは?」 もしそうなら、clip を外せば③が浮かび上がるはず。

外してみました。

| task | clip | MAP-E mean | baseline 勝数 | verdict_flip |
|---|---|---|---|---|
| **addition** | True | +0.0100 | 1/3 | — |
| **addition** | False | **−1.212** | 0/3 (全悪化) | **False** |
| **flip_flop** | True | +0.426 | 0/3 | — |
| **flip_flop** | False | +0.438 | 0/3 | **False** |

clip を外したら、③が浮かび上がるどころか **addition で MAP-Elites が +0.010 → −1.212 に劣化**。clip=False は raw R²<0 のノイズ領域 (15/15 seed が負、R² が [−3.68, −0.20]) に MAP-Elites を落とし、構造を回復するどころか悪化させた。**= 「clip が信号を隠している」仮説を能動的に反証**。

null-ridge FPR (gene 非依存 target = 真の帰無仮説) も clip True/False で差ゼロ (両方 0.0)。

判定: **K4 は「唯一の能動的 suppression 機序」ではなく、「spread を潰すが verdict を変えない診断的所見」に降格**。これで過去の統計監査が断定していた「K4 = 唯一の能動的 suppression」は過大だったと判明しました。

正直な留保 (§6.3 相当): null-FPR=0/0 は null_seeds=4 のみの床値だし、この実験は予算を約 7 倍縮小しています。だから verdict のラベルは「null 確定」ではなく **「not_load_bearing_at_this_budget (この予算では非載荷)」** に統一しました。「null を確定した」より「この予算では K4 が load-bearing でない」が正確だからです。判定の実体 (診断的所見への降格) は不変で、語の精度だけ上げています。

— ここで深呼吸。3 実験おわり。次は「言い過ぎていないか」の自己点検。 —

---

#### 7. Surviving refutation — 3 つのレンズで自分の結論を殴ってみた

honest disclosure の核は「自分の結論を一番きつく疑う」ことなので、3 つの独立な反証レンズを当てました。**3 つとも `refuted=true / medium` で生き残った**、つまり保守的な verdict は覆らないが、positive 寄りの強調は弱める方向で効いています。

1. **[power_adequacy] C-gen4b の gate PASS は optional-stopping + 多重比較で脆い**。上の §5 のドリフトと Bonferroni FAIL がこれ。「③ NOT null」を headline にするのは境界 p に寄りかかりすぎ。→ p の n 軌跡と後半 seed の符号反転を開示フィールドに記録済。
2. **[determinism_and_circularity] 単峰 verdict は閾値近接で脆い**。決定論化と非循環性そのものは clean (behavior と fitness の相関は ≈0、診断器は behavior 記述子を使わず地形幾何を直接見る)。ただし ESN_3param の midpoint の **90.9% が下方に dip** していて、最大相対 dip=0.0435 は C1 谷閾 0.05 の直下 (13% 以内)。だから精密に言うと「**真に単峰**」ではなく「**C1 閾値を僅かに下回る浅い谷 (~2–4%) を持つ弱 multi-basin**」。(B) null の方向は維持されるが、頑健性は閾値近接ゆえ限定的。
3. **[clip_flip_validity] K4 降格は低予算ゆえ "at this budget" 限定**。verdict_flip=False は確かだが、FPR 0/0 は床値、予算は 7 倍縮小。だから「firm refutation」より「not load-bearing at this budget」と述べるべき。

3 つとも「結論をひっくり返す」ほどではないが、「言い過ぎを削る」方向で全部効いた。この自己監査こそ今日の成果の半分です。

---

#### 8. 自分が踏んだミスを 1 つ正直に書く

前回の谷深さ workflow で、2 段目のオーケストレータ briefing に **stale (古い) な値** を渡してしまいました。「全 below threshold / d*=0.1234」みたいな値です。ところが実際に commit されている結果 JSON は `all_below_threshold=false` でした。前回の workflow 結果を読んだとき、別のメトリックの値を取り違えていたのです。

これを **敵対検証が検出して、verdict を N/A に格下げ**しました。つまり「整いすぎた結論」を自分で疑うプロセスが、自分のコピペミスを捕まえた。気持ちのいい話ではないけれど、これが回ったから今日の Step D で正しい足場から測り直せた。

honest disclosure は「失敗を消さない」だけでなく、「**失敗を検出する仕組みを先に置いておく**」ことなんだな、と改めて思いました。

---

#### 9. 過去 verdict をどう更新したか

| 過去 verdict | 過去の読み | Step D の更新 |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **方向更新: ③ は NOT null の方向 (fresh n=64 で gate PASS)**。ただし候補止まり |
| step6 exp7 (実 ESN proxy, ③ negative) | n≤10 盲点域, 「再測必須」 | **大幅更新: 地形が本当に滑らか (③不要) を noise-free で確定**。再測しても多峰は出ない |
| 谷深さ N/A (計測不能) | instrument 不能 | **解消: 決定論化で計測可能化** → vf≈0 (単峰)。ただし閾値近接の浅い谷が留保 |
| K4 clip = 唯一の能動的 suppression | 「clip が landscape 構造を隠蔽」 | **降格: 診断的所見** (not_load_bearing_at_this_budget) |

「③不要に見えた過去 negative の多くは underpower ではなく、地形が本当に滑らかだった」── この一点が、実 substrate 上で初めて確かめられたのが今日の核です。

---

#### 10. 外部レビュー (Codex) はブロッカーなしで追認

llcore の規律として、各 capstone は Codex (gpt-5.4, read-only) のペアレビューを通します。今回の総評は **「ブロッカーなし ── ③ 結論を外部確認」**。

- C-gen4b を load_bearing でなく候補止まりにした判断は妥当 (更新検出力 0.5174 < 0.80 を JSON で確認)。
- EXP2 の決定論・非循環は clean。「真に単峰」より「閾値下の弱 multi-basin」が精密、という本文の自認も追認。
- EXP3 の K4 降格は現予算なら妥当 (FPR 0/0 + 7倍縮小ゆえ at-this-budget 限定)。

指摘された 4 件 (CF1〜CF4) は **すべて将来 rerun 時の harness 堅牢性と文言精度** であって、現結論を覆すものではありません。GPU で③を再検定するとき、これらを適用してから harness を再利用します。

---

#### 11. CPU の抜け道 (kernel 多様化 / BG9) を試していた

「③ の本丸は GPU (実 LLM の損失地形) へ」が EXP2 の推奨です。実 proxy が滑らかと確定した以上、滑らかな地形で③を追っても (A) は出ない (地形が一つ山なら選り分けに利得がないのは当然)。

ただし GPU は投資判断なので、**CPU で前進できる別仮説**を並行して試していました。それが **kernel 多様化** です。

仮説はこうです。個々の kernel (rwkv / mamba / hopfield / linear_attn) が滑らかでも、**4 種類の kernel 族を union すると、kernel 切替の瞬間に fitness が不連続に段差を作る → 地形が multi-basin (だまし地形) になりうる → ③が GPU なしで CPU 上で load-bearing になりうる**。これを検証するのが BG9 でした。

この記事を最初に書いた時点では「いま BG6 (task → best-kernel 写像が非定数か、つまり「タスクごとに得意 kernel が違うか」) を smoke 測定しているところ」でした。その後 (同じ 2026-06-02 中に) BG9 の決着がつきました。次の追記節がその結末です。

---

#### 11.5. 追記 (2026-06-02): BG9 決着 — 抜け道は構造的に閉じていた

> 結論を一行で: **BG9 = N/A (構造的)。つまり kernel 多様化という CPU 抜け道は「③ が立たないことが構造的に決まっている」ので閉じた。** 「③ が要らない」ではなく「この空間では③が強 baseline と原理的に分離できない」という、情報量のある negative です。

§11 で仕掛けた抜け道の結果が出ました。期待した「kernel union で multi-basin (だまし地形) が生まれて③が CPU で立つ」は **起きませんでした**。しかも「たまたま立たなかった」のではなく **構造的に立てない** ことが分かった。BG9 はこれを 3 段の証拠で確定しています。

##### (1) substrate validity — 「弁別はあるが弱い」(PASS だが要注意)

まず「タスクごとに得意 kernel が違うか」(BG6) を、kernel-favoring task 群を第一原理で設計し直して測ったところ、写像は **非定数 = 非 inert (PASS)**。mamba / linear_attn / rwkv はそれぞれ別タスクで best になりました。BG6 で踏んだ「memory_tasks は kernel 中立」の轍は回避できた、という意味では前進です。

ただし正直に言うと **弱い**:

- **hopfield はどのタスクでも勝てなかった**。これは hopfield kernel が **対角スカラ mock** で、tanh アトラクタが機能不全だったため (per-seed の R² が 0/0.99/0 と二極化)。つまり実質「4 kernel union」ではなく **3 kernel** です。
- clean な専門化は 2 軸のみ (selective_copy↔mamba / weighted_accum↔linear_attn)。残りは margin が薄く fragile。

→ **弁別の存在 ≠ 多峰/障壁**。non-inert 化には成功したが、それが欺瞞地形 (だまし地形) を保証するわけではない、という所まで。なお対角 mock の限界は kernels.py のスコープ宣言どおりで、ここでは **機構の feasibility のみ主張** (full kernel 性能は非主張) です。

##### (2) harness validity — positive control が validate しない (これが決め手)

次が本丸です。固定パラメータ (behavior=(kernel_id, theta L1)) で MAP-Elites (③) を、3 つの baseline ── **RR-hillclimb (random restart 山登り)** / panmictic-GA / random ── と honest に paired 比較しました。

| 基質 | 結果 |
|---|---|
| **positive control** (合成 kernel-barrier) | ③ は panmictic (+0.423) と random (+0.208) は撃破。**だが RR には勝てない** (+0.051, p=0.31 → FAIL)。3 baseline 全勝に届かず = **harness validity が立たない** |
| **negative control** (kernel 中立タスク) | 全 method R²≈1.0 飽和、③ 優位なし = **正しく null** (false-positive なし、計器は健全) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3、panmictic が逆に③を上回る = **③ 勝たず** |

ここが Step D (技術版 §4-7) と決定的に違う点です。Step D の欺瞞 corridor では③が RR を排除できました。**なぜ kernel 空間ではできないのか?** 根因は 1 つ:

> **RR は restart のたびに kernel_id ∈ [0,4) を直接サンプルできる。** kernel 選択は 4 離散の単一座標 (低次元) なので、RR は restart で全 4 kernel を直撃する。「best kernel を探す」のに谷を跨ぐ必要がない = **teleport (直接ワープ)**。だから③ の behavioral niching に出番が来ない。

Step4 の corridor で③が RR を排除できたのは、そこの behavior が `mean(24次元)` で、CLT により平均が 0.5 に集中 → 大域ピークが measure-zero 域 = **random/RR が直接サンプルできない高次元**だったからです。kernel_id は逆に低次元で直接サンプルできてしまう。

##### (3) red-team — 敵対検証でも反証できず、むしろ確証

「harness が立たないのは本当に構造のせいか? たまたまの設定ミスでは?」を独立 red-team で叩きました。結果は構造主張を **反証できず、むしろ強化**:

- **機構確証**: instrumented RR が positive control 上で 4 basin に restart kid を [12,18,16,18] とほぼ一様分散、target 到達 88%、best は restart→in-basin climb が 6/8 seed。「RR は restart で kernel_id を直接サンプルして谷を回避する」を **数値で確証**。
- **4 つの faithful 構成 (高次元 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) すべてで③は RR に勝てない (beats_rr=False)**。corridor を緩めると RR も同等到達、締めると③が **先に starve** (餓死)。
- **境界 sweep**: theta corridor の次元を D=0→3 と締めるほど③が RR より速く starve (D=3: ③ reach 0.08 vs RR 0.42)。base_seed 3 通りで同一。

→ **「RR だけ排除して③が通る behavior 次元は、kernel 空間に構造的に存在しない」** を定量確証。

##### 構造的洞察 (この決着の payoff)

> **③ (MAP-Elites の behavioral niching) が強 baseline を上回るのは、「難所」が高次元 behavior 空間にあって直接サンプリング (random restart) で到達できないときだけ。**

- **kernel 選択は低次元 (4 離散の単一座標)** → RR が直接サンプル → ③ の niching 優位が原理的に出ない。
- theta 空間に欺瞞を移しても、RR は restart 後に in-basin で greedy climb するので、corridor を RR が抜けられない程度に締めると③も同程度に starve する。**RR fail ∧ ③ succeed の窓が存在しない。**

これは Step4 §7 で残った問い「探索空間を kernel 多様化で拡張すれば③が unlock するか?」への答えです。答えは **NO (CPU では構造的に)**。拡張が③を unlock するには、追加した自由度が **高次元で直接サンプル困難**な behavior を生む必要がある。kernel 選択 (低次元・離散) はその条件を満たさない。

##### GPU への含意

- **CPU 出し切りゲートが CLEAR**: BG9 が最後の CPU 路 (kernel-union) を構造的に閉じた。③ の残り路は **高次元の GPU full-LLM 損失地形のみ**。
- 構造的洞察は GPU の賭けを **better-motivated** にします。③ は高次元 behavior で初めて意味を持つ。full-LLM のパラメータ空間は数百万次元 = まさに高次元。だから GPU 検定は「full-LLM だけが例外かも」という弱い賭けでなく「③ は高次元を要し、full-LLM が高次元域」という原理に沿う。
- **ただし依然 bet**: 実 LLM 地形が backprop 系の強 baseline で直接ナビゲートできるなら③不要 ── これは **BG9 の RR と同型のリスク**です (「強 baseline が直接解く」可能性は GPU でも残る)。だから GPU は「③のため単独」でなく **ポートフォリオ判断** (llive 実 LLM fitness 等と相乗り) + **クラウド借りで事前登録 1 本** (資本コミット前) が適正。BG9 の構造的洞察そのものが GPU の falsifiable な go/no-go 基準になります:「③ が full-LLM で load-bearing なら、その難所は高次元 behavior 空間にあり直接サンプル/backprop で到達困難なはず」。

##### honest 留保 (重要)

- これは **「③不要と判明」ではありません**。「③ がこの低次元 kernel 空間では強 baseline と原理的に分離できない」= N/A (構造的) であって、③ の機構自体は Step4 で本物と確定済みです。N/A だが「kernel 路は閉じている」という決定的情報を持つ **情報量のある N/A** です。
- harness/red-team は smoke 規模 (5-12 seed)。本検定 15 seed では数値は動くが、**構造 (締めると③が先に starve / RR が kernel_id を直接サンプル) は seed 非依存で頑健**。real の full ≥15-seed 本検定は実施しません ── positive control validity が構造的に立たない以上、real で③不要が出ても「③不要 vs 検出器盲」を分離できず、その「検出器盲 = kernel 空間の構造」を red-team が既に確定したので、CPU を 7.5h 投じても結論は変わらないからです。
- substrate は弱い (実質 3 kernel、**hopfield は対角 mock で機能不全**)。より強い kernel 弁別 (full 実装・非対角) なら別結論の余地は **理論上**あるが、③ の構造的障壁 (低次元選択 → RR 直接サンプル) は kernel 実装の質と独立です。
- 「整いすぎた③成立」を疑う規律は今回は **不要でした** ── ③成立は最初から出ていない (honest prior 通りの negative)。

---

#### 12. メタ教訓 — 正直さは、勝つための道具だった

今日の本当の成果は数値ではなく、**「整いすぎた結果を疑う」精神が実際に研究を前へ進めた**ことです。

- 評価ノイズを物理的に消した (EXP2) から、「滑らか」が地形の性質か計器の限界かを切り分けられた。
- 敵対検証 3 レンズを当てたから、「③ NOT null」を headline にせず「候補」に留められた。
- 自分の stale 値の取り違えを自己検出したから、N/A という正しい格下げができ、今日測り直せた。
- **BG9 (追記) でもう 1 つ学んだ**: **低次元の難所は強 baseline が直接解いてしまう。だから③ (選り分けて育てる工夫) が効くには "高次元 behavior 空間" が要る。** 「だまし地形を作れば③が立つ」は半分しか正しくなくて、正確には「**直接サンプルできないほど高次元な**だまし地形」でないと③は立たない。kernel 4 択 (低次元) では、RR が restart で全部直撃するので③の出番が原理的に来なかった。これは抜け道を「諦め」でなく「**構造的に閉じた**」と言い切れる根拠です。

「異常に良い結果が出たら、勝った気になる前に必ず内訳を疑う」── FullSense の研究規律 (`feedback_benchmark_honest_disclosure`) は、ただの自戒ではなく、**実際に偽陽性を捕まえて研究の精度を上げる機構**として回っていました。BG9 はその逆方向 (**negative を正しく negative と確定する**) でも同じ規律が効いた例です ── red-team で自分の「③ が立たない」を反証しようとして、反証できずに構造として確証された。

結論を、最後にもう一度、正確に (BG9 決着を反映):

> **proxy substrate 上では「③ は地形が真に滑らかゆえ不要」が noise-free に確定**した (Step D)。実 multitask 近傍 (C-gen4b) でだけ「③ NOT null」の弱い兆候が出たが、小効果 + ドリフト + 多重比較で **候補止まり**。K4 clip は能動的 suppression でなく診断的所見に降格。そして CPU の最後の抜け道 **kernel 多様化 (BG9) は構造的に閉じた** ── kernel 選択は低次元ゆえ強 baseline (RR) が直接サンプルし、③ の niching 優位が原理的に出ない。**③ の本丸検証に残された路は、高次元の GPU full-LLM 損失地形のみ** (それも「強 baseline が直接解く」リスクを抱えた bet)。

「③ 決着 = ③ は不要と判明」ではありません。正しくは **「③ が活きるのは "高次元の" 欺瞞地形のときだけ。今 CPU で測れた実物もどき (滑らか) も kernel 多様化 (低次元) も、その条件を満たさなかった」**。本丸 (GPU 高次元) はまだ先で、しかも保証のない賭けです。

---

**Tags**: 進化計算 / MAP-Elites / 統計検定 / 検出力 / honest disclosure / CPU 研究
**関連**: 連載 #32 (llcore CPU PoC battery) / #29 (反証・Goodhart・proxy 限界) / #31 (Codex 二本柱)
**Project**: llcore (PyPI 予約 llmesh-llcore、リポジトリ未公開のためローカル研究)

---

## 10. llcore — 「進化で AI を設計するとき、選り分けて育てる工夫 (③) は要るのか」を 6 段の実験 + 生物学で俯瞰した話 (第三軸 arc 全体)

### (連載 #34) 山登り 6 連戦で分かった「いつ進化の③は効くのか」— そして 100 年前の進化生物学が同じ答えを出していた

#### TL;DR

- 問いは **「AI のコア計算を進化で探すとき、"選り分けて分けて育てる工夫" (= 進化の③ 適者生存/分離) は本当に要るのか」**。連載 #33 は最終局面 (Step D + BG9) の決着を書きましたが、**この #34 は arc 全体 (6 段) を 1 つの物語として俯瞰**します。
- **第1段 (合成だまし地形)**: ③は圧勝 (Cliff δ=+1.0)。③は機構として本物 = **存在証明**。
- **第2段 (記憶タスク / 多 reservoir)**: 基質の「床」と「天井」に阻まれて③を測れず = **N/A**。
- **第3段 (多タスク汎化)**: ③は「選択なし」には勝つが、単純な選択や random には勝てず = ③不要 (honest negative)。
- **第4段 (実 proxy 地形を noise-free 測定)**: 評価ノイズを物理的にゼロまで落としたら地形は **本当に滑らか (単峰)** = ③不要を確定。「過去の negative は検出力不足ではなく地形が滑らかだった」が初めて裏付いた。
- **第5段 (部品 4 種を混ぜる抜け道 BG9)**: kernel 選択は **低次元**ゆえ強 baseline (ランダムリスタート山登り) が直接サンプルし、③の niching 優位が**構造的に**出ない = 抜け道は閉じた。
- **構造的洞察 (この arc の核)**: ③が効くのは難所が **高次元 behavior 空間**にあって直接サンプル不能なときだけ。実 CPU 基質は低次元/滑らかなので③不要。
- **生物学的接地 (検証済み)**: これはライト (Wright) の **シフティング・バランス説**そのもの。**暗化モフ (単一遺伝子 = 低次元)** では普通の選択で十分 (= BG9 の kernel ケース)、**レンスキーの Cit+ (高次元・歴史依存)** では多様性が効く (= ③ regime)。私たちの negative は **コイン批判 (現実の地形は単純で③は稀にしか決定的でない) の計算版**。
- **メタ教訓**: 「うまく行きすぎた結果は勝ちでなく警報」。事前登録・honest disclosure・敵対検証・決定論 noise-free 測定で、ぬか喜びを避けた。

> ⚠ この記事の数値は、すべて手元 (ローカル) の研究記録に紐づく実測です。llcore はまだ公開リポジトリを作っていないので、外部リンクは貼れません。代わりに「どう測ったか」を本文に書きます。生物学パートで引用する論文は、別途一次情報で存在・帰属・主張内容を照合したものだけを挙げています。

---

#### 0. この記事は何の話か (コンセプト)

`llcore` は「Transformer のコア計算 (状態更新則・学習則・認知駆動 Δ) を遺伝子にして、Z3 で壊れないように検証しながら進化させる」CPU 完結の研究フレームワークです。

その進化エンジンには、進化の 4 要素 (① 変異 / ② 遺伝 / ③ 適者生存・分離 / ④ 過剰繁殖) のうち、**③ (selection / separation)** をどう効かせるか、という設計上の急所があります。多様性を保ってニッチに残す MAP-Elites のような「選り分けて分けて育てる」仕組みです。

問いはシンプルです。

> **その③、本当に要るの?**

要るなら、③を載せるための重い投資 (最終的には GPU で実 LLM を回す) に意味がある。要らないなら、③にこだわるのは時間と電気の無駄になる。

連載 #33 では、その問いの **最終局面** (Step D の決定論測定 + BG9 の構造的決着) を詳しく書きました。でも、そこに至るまでには **6 段の実験**があり、勝ったり (存在証明)、測れなかったり (N/A)、負けたり (honest negative) を繰り返していました。この #34 では、その **arc 全体を 1 つの物語**として並べ直します。さらに今回の目玉として、**この計算結果が 100 年近く前の進化生物学の論争 (ライト対フィッシャー) と驚くほど同じ形をしている**ことを、検証済みの一次情報で接地します。

— ここまで 40 秒。準備運動おわり。本題へ。 —

---

#### 1. たとえ: 山登りと、だまし地形と、記憶の宮殿

数式の前に、この研究で一貫して使っている 3 つのメタファーで全体像を掴みます。

設計の良し悪しを **地形の高さ**で表します。**高い場所 = 良い設計**。一番高い頂上を探すゲームです。

**地形その1: 滑らかな一つ山 (簡単)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

こういう地形では、素朴な「山登り法 (hill-climbing)」、つまり「今より少し良い方へ動くだけ」で十分に頂上へ着きます。**凝った工夫 (③) は要りません**。

**地形その2: だまし地形 (欺瞞的 deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

ここでは素朴な山登りはニセ頂上で止まります。谷を下る勇気がないからです。

このとき効くのが③の発想です。**いろんなタイプの登山者を谷のあちこちに残しておく** (= 記憶の宮殿 / MAP-Elites archive)。誰かが谷を「飛び石 (stepping-stone)」で渡って本物の頂上に到達できる、という仕組みです。

**この研究の核心を一言で**: ③が本当に役立つのは **「だまし地形」のときだけ**。滑らかな一つ山では、③は無用の長物です。

だから問いは、こう言い換えられます。

> **「進化で AI を設計するとき、実際に出くわす地形は "だまし地形" なのか、それとも "滑らかな一つ山" なのか?」**

#33 では Step D + BG9 でこの問いに決着をつけました。この #34 では、そこに至る **6 段の山登り全部**を見せます。各段で「だまし地形だったか / 滑らかだったか / そもそも測れたか」が変わるのが面白いところです。

— 小休止。準備はここまで。ここから 6 連戦の実録です。 —

---

#### 2. arc 全体マップ — 6 段の山登りを一望する

先に地図を出します。これがこの記事の背骨です。

| 段 | 基質 (どんな地形を測ったか) | ③は効いたか | 一言 |
|---|---|---|---|
| **I (Step 4)** | 合成した「だまし地形」(欺瞞 corridor) | **Yes (圧勝)** | 存在証明。③は本物 |
| **II (Step C / 梯子1)** | 記憶タスク / 多 reservoir パリティ | **N/A** | 床・天井・degree-5 の壁で測れず |
| **III (E-A)** | 多タスク汎化 | **No** | ③は「選択なし」には勝つが、それ以上ではない |
| **IV (Step D)** | 実 proxy のテキスト地形 (決定論測定) | **No** | 地形が**本当に滑らか**と確定 (noise-free) |
| **V (BG9)** | 部品 (kernel) 4 種の union | **No** | **構造的に**閉じた (低次元選択) |

ストーリーラインはこうです。**まず「③は条件次第で圧勝する本物だ」と存在証明し (I)、次に「では実問題ではどうか」を 4 段かけて測りに行ったら (II〜V)、ことごとく "実 CPU 基質は③が要らない地形だった"**。しかも最後 (IV, V) で「要らない理由」が **検出力不足ではなく地形の性質**だと確定した ── これが arc 全体の弧 (アーク) です。

では 1 段ずつ。

---

#### 3. 第I段 (Step 4) — 存在証明: だまし地形なら③は圧勝する

最初にやったのは「③が **理屈どおり効く場面が実在するか**」の存在証明です。地形を **わざと欺瞞的に作って**、③ (MAP-Elites) を 3 つの baseline ── pure random / panmictic GA / **ランダムリスタート山登り (random-restart hill-climbing)** ── と勝負させました。

**地形の作り**: 遺伝子は 24 次元。behavior (登山者のタイプ) を `mean(遺伝子)` = 24 個の平均で定義します。behavior を上げるには **全 24 次元を同時に高く**しないといけない。fitness は「behavior≈0.4 にニセ頂上 (値 0.6) → behavior≈0.65 に谷 (値≈0) → behavior≈0.9 に本物の頂上 (値 1.0)」という、まさにだまし地形。

**結果**:

| 方法 | 本物の頂上への到達率 | ③ との比較 |
|---|---|---|
| **MAP-Elites (③)** | **約 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | 同上 |
| ランダムリスタート山登り | 0% | 同上 |

③ だけが本物の頂上に着き、3 つの baseline は全部ニセ頂上 (≈0.60) で止まりました。**100% 勝ち / 効果量は理論最大 (δ=+1.0)**。base seed 3 通り (計 60 seed) で頑健。

なぜこうなるか、が後の伏線になります。

- **random** は behavior が必ず ≈0.5 に集中する (24 個の平均は中心極限定理で 0.5 に固まる)。だから behavior 0.9 には **永遠に到達できない** (6000 サンプル引いても 0%)。
- **山登り** はニセ頂上 0.6 まで登り、谷を下る一手を拒否。リスタートしても behavior≈0.5 に戻り、同じ罠へ。
- **③ (MAP-Elites)** は谷のマスを「新しい behavioral ニッチ」として保持し、behavior を 0.5 → 0.9 へ **飛び石で渡る**。

**境界も正直に測りました**。谷を消した滑らかな corridor では、③ は山登りに勝てなくなる (p≈0.29)。**③ は万能ではなく、だまし地形でだけ効く**。

**honest 留保**: これは **わざと作った**合成地形です。③が「可能」だと証明しただけで、現実のタスクがこの構造を持つ証明ではない。toy スケール・低ノイズ・baseline は素朴な (1+1) です。

→ ここで仮説が立ちます。**「実問題の地形も、これくらいだまし地形なら、③は活きるはず」**。次の 4 段は、それを実問題に近い基質で確かめに行く旅です。

— 一服。第I段は気持ちのいい圧勝でした。ここから雲行きが…。 —

---

#### 4. 第II段 (Step C / 梯子1) — 基質の「床」と「天井」に阻まれる (N/A)

次に「だまし corridor が **標準的な記憶タスクに自然に出現するか**」を調べました (Step C)。delayed parity / flip-flop / delayed recall を、1 個の leaky reservoir + ridge readout で。

結果は綺麗な **N/A (測定不能)**。理由が両極端で面白い。

- **delayed parity = 床 (floor)**: 1 個の reservoir は XOR を計算できない (Minsky-Papert)。全方法が R²≈0.003。誰も登れないので③を分離できない。
- **flip_flop = 天井 (ceiling)**: 全方法が R²≈0.95 に飽和。分散が潰れて③の差が出ない (③ vs random は符号は正だが p=0.15 = underpower で **null ではない**)。

ここで大事な発見が 1 つ。**遺伝子空間の多峰性は高かった** (valley fraction が parity で 1.000) のに、③の役には立たなかった。つまり **「遺伝子空間で多峰」≠「behavior で渡るべきだまし地形」**。この区別が arc 後半の鍵になります。

**梯子1 (多 reservoir)**: では reservoir を複数つなげば床が上がるか? → 5 つの機構を試して全部 `floor_lifted = false`。深さ (DeepESN) は床を統計的には上げる (効果 +0.47/+0.60, PASS) が絶対値は R² 0.05-0.10 止まり。決め手は positive control: degree-2 readout は 2-bit XOR を厳密に解く (R²=+1.0) が degree≥3 で破綻。**5-bit パリティは degree-5 = この CPU reservoir+ridge パラダイムの構造的な壁**。

→ パリティ路は構造的に塞がれた。③の本検定は **パリティから降りる**必要がある。

**honest 留保**: degree-5 の壁は「この設定の壁」であって、パラダイム全体の不可能性証明ではありません。

— 小休止。「測れなかった」という結果は地味ですが、地図を描く上では大事な空白地帯です。 —

---

#### 5. 第III段 (E-A) — 多タスク汎化: ③は要らなかった (honest negative)

パリティの床を降りて、**汎化 (generalization)** で③を測りました。一番きれいな ablation を組んで。

**設定**: 単層 leaky reservoir + ridge。可変遅延の recall。**短い遅延 {15, 30} で学習し、長い遅延 {45, 60} でテスト** (外挿)。比較は MAP-Elites (①②③フル) vs **選択を抜いた MAP-Elites** (`randselect`: 親をランダムに選び無条件配置 = 変異だけ) + panmictic GA + random。

**結果 (ペアレビュー後)**:

| 方法 | テスト汎化 R² (平均±std) |
|---|---|
| MAP-E (①②③フル) | 0.682 ± 0.115 |
| MAP-E randselect (選択を抜く) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| ゲート | 比較 | diff | p (片側) | 判定 |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**読み方**: ③は「**選択を抜いたドリフト対照**」には勝つ (C-gen3 PASS = "何らかの選択は無選択に勝つ")。でも **panmictic GA (選択はあるが niching なし) には勝てない** (むしろ僅かに負け)、random にも勝てない。つまり **niching 固有 (= ③ 本来) の寄与は無い**。この汎化地形は、単純な選択や random でも同じところに着くくらい **滑らか**だった。第I段の「滑らかなら③は効かない」境界と整合します。

**honest 留保 (重要)**: この verdict は **この設定限定** (予算 400, grid 6×6)。さらに ── ここが honest methodology の肝 ── ペアレビュー (Codex) が当初「信用できない」と判定し、3 つの rerun ブロッカー (replicate ごとの独立 seeding / 予算内グローバル最良の採用 / honest_n を 16→30) を強制しました。**修正後も結論は変わりませんでした**。「直したら結論が変わる脆い negative」ではなかった、というのが収穫です。

— 一服。負けは負けですが、「正しく負けた」ことを確かめる作業の方が時間がかかりました。 —

---

#### 6. 第IV段 (Step D) — 実 proxy 地形は「本当に滑らか」と確定 (noise-free)

ここが arc の転回点です。第III段までで「③ negative」が続いたが、ずっと **しこり**が残っていました。

> 「③不要」は本当に **地形が滑らか**だからか? それとも単に **サンプル数が足りず差を検出できなかった (underpower)** だけか?

これを取り違えると「③ は無力」と過剰一般化してしまう。Step D はここに決着をつけます。

**トリック**: ESN reservoir (固定 seed) + ridge readout の closed-form (`np.linalg.solve`) は **乱数を一切引かない**。だから評価ノイズを **機械イプシロン (約 1.11e-16)** まで物理的にゼロ化できる。実測で `eval_noise_std ≤ 1.11e-16` を確認 ── これは浮動小数点の最小単位 (ULP) 由来で **実質ゼロ**です。ノイズの霧を完全に晴らして、地形の谷を直接測れる。

地形は llcore 自身のソース (約 24k 文字) の次文字予測。valley_fraction (谷の割合、≥0.2 で多峰=だまし地形) を測りました。

| 地形 | 次元 | valley_fraction (mean/max) | 多峰? | 判定 |
|---|---|---|---|---|
| **ESN 3-param** (実 proxy) | 3 | **0.000 / 0.000** | No (3 seed 一致) | 滑らか → ③不要を noise-free で確定 |
| **ESN per-neuron** (実 proxy) | 40 | **0.096 / 0.121** | No (3 seed 一致) | smooth 寄り → ③不要 |
| 多峰 control (正) | 3 / 40 | 0.70 / 0.80 | Yes | 診断器は多峰を検出できる ✓ |
| 二次関数 control (負) | 3 / 40 | 0.000 | No | 診断器は滑らかを検出できる ✓ |

ポイントは 2 つ。

1. **実 proxy 地形 (3 次元 / 40 次元とも) は単峰**。3 seed で一致。
2. **診断器そのものは健全**。わざと作った多峰はちゃんと多峰と検出し、二次関数はちゃんと滑らかと検出する。だから「実 proxy が単峰」は計器のバグでなく **地形の性質**。

→ これで初めて **「過去の③ negative は underpower ではなく、地形が本当に滑らかだった」** が実 substrate 上で noise-free に裏付きました。再測しても多峰は出ない。

**honest 留保 (重要)**: 「滑らか」は閾値近接でだけ精密です。ESN 3-param の midpoint の **90.9% がわずかに下方に dip** し、最大相対 dip (0.0435) は谷閾値 0.05 の直下。正確には「**真に単峰**」ではなく「**閾値を僅かに下回る浅い谷 (~2-4%) を持つ弱 multi-basin**」。方向は維持されるが、頑健性は閾値近接ゆえ限定的 ── ここを「完璧な凸の器」と丸めない、が今回の規律です。

— 深呼吸。ここで「実物もどきは滑らか」が確定。残るは「最後の CPU 抜け道」です。 —

---

#### 7. 第V段 (BG9) — 部品を混ぜる抜け道は、構造的に閉じていた

実 proxy が滑らかと確定した以上、滑らかな地形で③を追っても利得は出ない。でも GPU は投資判断なので、**CPU で前進できる別仮説**を試しました。それが **kernel 多様化 (BG9)** です。

**仮説 (事前登録 H7)**: 個々の kernel (rwkv / mamba / hopfield / linear_attn) が滑らかでも、**4 種類を union すると kernel 切替の瞬間に fitness が段差を作る → multi-basin (だまし地形) になる → ③が GPU なしで CPU 上で立つ**。事前登録した honest prior は **null 寄り** (これまで全 CPU 基質が滑らかだったので)。

結果を 3 段で。

**(1) substrate validity — 弁別はあるが弱い (PASS だが要注意)**: タスクごとに得意 kernel が違うか測ると、写像は非定数 = non-inert (PASS)。mamba は selective-copy、linear_attn は weighted-accumulation で best。ただし **hopfield はどのタスクでも勝てなかった** (対角スカラ mock で機能不全) ので、実質「**3 kernel** union」。**弁別の存在 ≠ 多峰障壁**。

**(2) harness validity — positive control が validate しない (決め手)**: 合成 kernel-barrier で③を 3 baseline と比較。

| 基質 | 結果 |
|---|---|
| **positive control** | ③ は panmictic (+0.423)・random (+0.208) を撃破。**だが RR (ランダムリスタート山登り) には勝てない** (+0.051, p=0.31 → FAIL)。3 baseline 全勝に届かず = harness が立たない |
| **negative control** | 全 method 飽和、③ 優位なし = 正しく null (計器は健全) |
| **real** smoke | ③ beaten 0/3、panmictic が逆に③を上回る |

第I段の corridor では③が RR を排除できたのに、**なぜ kernel 空間ではできないのか?** 根因は 1 つ。

> **RR は restart のたびに kernel_id ∈ [0,4) を直接サンプルできる**。kernel 選択は 4 離散の単一座標 (**低次元**) なので、RR は restart で全 4 kernel を直撃する。「best kernel を探す」のに谷を跨ぐ必要がない = **直接ワープ**。だから③の behavioral niching に出番が来ない。

第I段で③が RR を排除できたのは、そこの behavior が `mean(24 次元)` で、平均が 0.5 に集中 → 大域ピークが measure-zero 域 = **直接サンプル不能な高次元**だったから。kernel_id は逆に低次元で直接サンプルできてしまう。

**(3) red-team — 敵対検証でも反証できず、むしろ確証**: instrumented RR が positive control 上で 4 basin に restart kernel を [12,18,16,18] とほぼ一様分散、target 到達 88%。4 つの faithful 構成 (高次元 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) すべてで③は RR に勝てない。corridor を締めると③が **先に starve (餓死)** する (D=3: ③ reach 0.08 vs RR 0.42)。**「RR だけ排除して③が通る behavior 次元は、kernel 空間に構造的に存在しない」**を定量確証。

**verdict**: 形式上は N/A (positive control が validate しない) だが、実質は **決定的な構造的 negative**。harness は健全 (negative control を正しく null にし、GA/random を検出する) なのに、基質が③のだまし地形を **そもそもホストできない**。第I段で残った問い「kernel 多様化で探索空間を拡張すれば③が unlock するか?」への答えは **NO (CPU では構造的に)**。

**honest 留保 (重要)**: これは **「③不要と判明」ではありません**。「③が低次元 kernel 空間では強 baseline と原理的に分離できない」= **情報量のある N/A**。③の機構自体は第I段で本物と確定済み。substrate は弱い (実質 3 kernel、hopfield は対角 mock)。より強い kernel 実装なら別結論の余地は理論上あるが、**構造的障壁 (低次元選択 → RR 直接サンプル) は kernel 実装の質と独立**です。

---

#### 8. 構造的洞察 — 6 段を 1 つの条件でまとめる

存在証明 (I) と 4 つの negative (II〜V) は、たった 1 つの条件で全部つながります。

> **③ (behavioral niching) が強 baseline を上回るのは、「難所」が高次元 behavior 空間にあって、直接サンプリング (ランダムリスタート) で到達できないときだけ。**

- **第I段が満たす理由**: behavior = `mean(24 次元)`。平均は中心極限定理で 0.5 に集中し、大域ピーク (mean≈0.9) は実質 measure-zero。random も restart も**直接届かない**。だから飛び石を残してラチェットする③が必須。
- **実 CPU 基質が満たさない理由**: 難所が低次元。ESN テキスト proxy の制御座標は実質 leak rate (滑らかな低次元ノブ、そもそも谷が無い)。kernel union の難所は「どの kernel か」= 4 択の単一離散。RR が直接サンプルして全 basin に teleport するので、渡るべき谷が無い。

だから第II段の「遺伝子空間の多峰性 1.000」は十分条件ではない ── 遺伝子は谷だらけでも、難所が低次元 behavior 座標に集中していれば、restart が直接届く。**効いてくるのは "探索が到達すべき behavior の次元" であって、遺伝子の次元ではない**。

---

#### 9. 生物学的接地 — 100 年前の進化生物学が、同じ答えを出していた

ここからが #34 の目玉です。**「多様性を保つ選択は、狭い条件でだけ効き、それ以外では冗長」** ── この境界条件には、20 世紀の進化生物学に異常にきれいな先例があります。

> ⚠ **honesty 契約**: 以下の生物学は **「たとえ話 (structural analogy)」であって、私たちの計算結果の証明ではありません**。対応は構造的で、機構レベルでは一致しません。たとえがずれる箇所は全部その場で明記します。引用する論文は、別途一次情報で存在・帰属・主張内容を照合したものだけです。

##### 9.1 ライト (Wright) のシフティング・バランス説 = ③の先例

シューアル・ライト (Sewall Wright, 1931/1932) はこう考えました。大きな「一つの群れ (panmictic population)」のままだと、ふつうの自然淘汰では **目の前の局所ピークに捕まる**。もっと高い山へ行くには一度 mean fitness を **下げて谷を渡る**必要があるのに、決定論的な選択はそれを拒むから。

ライトの解決策は **群れを多数の半隔離されたサブ集団 (deme) に分ける**こと。

- **Phase I**: 小さな deme が**遺伝的浮動 (drift)** で偶然、谷を下って渡る。
- **Phase II**: そこで deme 内のふつうの選択が新しい (より高い) ピークを登る。
- **Phase III**: 高いピークに乗った deme が多くの移住者を出し、優れた遺伝子組合せが種全体に広がる。

メタ集団 **全体**として、単一収束集団には渡れない谷を渡る ── これが「だまし地形の谷を飛び石で渡る」の生物学版です。

**③ / MAP-Elites への対応 (= たとえ話、帰属ではない)**: archive の各セル = 準隔離 deme、セル内の局所 elitism = deme 内選択 (Phase II)、セル間変異 = interdeme 拡散 (Phase III)、そして **archive 全体** (≒メタ集団、単一セルではない) が谷を渡る。

> **honesty 注意 (2 点)**:
> 1. **これは解説者の枠組みで、ライトの主張でも MAP-Elites の出自でもない**。MAP-Elites の原論文 (Mouret & Clune 2015) も QD 文献も **ライトや「シフティング・バランス」を引用していない**。ライトは私たちの **着想 / たとえ**として挙げるのであって、MAP-Elites の系譜としてではない。
> 2. **機構は構造的に似ているだけで同一ではない**。MAP-Elites の谷渡りは **変異オペレータ**が子を新セルに置くことで起き、**遺伝的浮動ではない**。archive は複製するセルの集団でもない。

##### 9.2 ライト対フィッシャー = 次元 (地形の形) の軸

ライトと同時代のフィッシャー (R. A. Fisher, 1930) は逆を主張: **大きな panmictic 集団 + 加法的分散へのマス選択で十分**に適応は進む、わざわざ分割は要らない、と。

二人の **一番深い対立軸は、実は「エピスタシス (遺伝子間相互作用) と地形の形」** でした。ライトは「非加法的相互作用ゆえ地形は**でこぼこ多峰**、だから谷を渡る drift が要る」と仮定し、フィッシャーは「相互作用はあるが重要でない、地形はほぼ**単峰で滑らかに登れる**、だからマス選択で足りる」と判断した。

**この epistasis/ruggedness の軸が、まさに私たちの結果が生きている次元です。地形の形 (topology) こそが全問題**。地形が本当にでこぼこ高次元なら (ライト regime) 多様性が谷を渡し、滑らか or 難所が低次元なら (フィッシャー regime) マス選択 ── すなわち **強いランダムリスタート山登りの生物学版** ── で既に足りる。私たちの ESN テキスト proxy は noise-free で滑らか、kernel union の難所は低次元離散。**どちらもフィッシャー regime** で、③は効かないし効かなかった。

> 細かい注意 (正直に): 「フィッシャーは drift を無視した」は俗説の圧縮です。正確には「drift はあると認めたが、大きな集団では量的に無視できると判断した」。完全否定ではない。

##### 9.3 私たちの negative = コイン批判の計算版

一番効いてくる対応は、ライトの **提案**ではなく、生物学界の **経験的判定**の方です。Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) はシフティング・バランス説を理論・実証の両面から評価し、こう結論しました (全文照合済み)。

- **マス選択でたいてい足りる**。「ライトの三段階機構の方が単純なマス選択よりうまく説明できる実例はほとんど無い」。人為選択実験も「分割集団の選択が大集団のマス選択より大きな応答を生む」ことを示せなかった。
- **シフティング・バランスが効くのは限定的・稀少な条件下だけ**。集団構造の経験的推定からは「**浅い谷で隔てられたピーク間でしか drift は移動を起こせない**」(深い谷は drift では稀にしか渡れない)、しかも **大半の適応は谷渡りを必要としない**。

これは私たちの結果の **驚くほど正確な生物学版**です。彼らの言葉を私たちの語彙に翻訳すると ── **地形が真にだまし的/高次元でないなら、ふつうのマス選択 (≒強いランダムリスタート山登り) で既に解け、多様性維持の装置はほとんど何も買わない**。「現実の谷はたいてい浅い、大半の適応は谷渡り不要」は、私たちの「**実地形はたいてい単純だから niching は冗長**」の生物学的言明です。

> **honesty 注意 (3 点)**:
> 1. **彼らはシフティング・バランスを「反証」していない**。Phase I/II は起こりうると明言し、6 件の経験事例も挙げている。主張は **より狭い確率的なもの** (「一般的・重要な機構とは言い難い」) であって、「refuted」と書けば言い過ぎ。
> 2. **論争はまだ決着していない**。Wade & Goodnight (1998)、Peck et al. (1998, タイトルが文字通り「feasible」と主張) が反論し、Coyne らの 2000 年の再反論、Goodnight & Wade の同号反論と続いた。1997 批判を「最終結論」として引いてはいけない。
> 3. **生物には計算側に対応物のない機構があり、しかも私たちより強い主張をしている**。Phase III では、多様性を守る gene-flow 障壁が **良い解を周辺 deme に閉じ込めて広がりを妨げる** = niching が **逆効果**になりうる。私たちの stateless な離散選択設定にはこの cost の対応物が無いので、ここは **過剰に重ねない**。生物の方が一段強い主張をしている箇所です。

##### 9.4 二つの実例 — 低次元の蛾と、高次元の大腸菌

私たちの主張には 2 つの極 (低次元 = ③不要 / 高次元 = ③が効きうる) がありますが、進化生物学はそれぞれにきれいな実例を持っています。

**低次元の極 ── オオシモフリエダシャクの工業暗化 (= BG9 kernel ケース)**: *Biston betularia* の carbonaria (黒) vs typica (白) は **単一メンデル座位・少数アレル** (原因変異は cortex 遺伝子への転移因子挿入; van't Hof et al. 2011/2016) で、**強い方向性選択** (s ≈ 0.1-0.2; Saccheri et al. 2008; 捕食は Cook, Grant, Saccheri & Mallet 2012 で再確認) を受ける。最適は各時点で単峰、環境でシフトするだけ。**単純な方向性選択 ── greedy 山登り/ランダムリスタートの生物学版 ── が直接、適者モフを固定し、多様性維持機構は不要だし呼ばれていない**。これがまさに BG9: kernel 選択は 4 択の低次元単一座標で、RR が全 kernel を直接サンプルし、③が構造的に分離できない。**暗化モフ = BG9 kernel ケースの生き物版**。

> 注意 (正直に): 移行期には多型が一時保たれるが、それは **空間的環境不均一 + 遺伝子流動 (移住-選択平衡)** によるもので、内在的な多様性保存機構ではない。たとえが少しずれる箇所。

**高次元・歴史依存の極 ── レンスキーの Cit+ (= ③ regime)**: 大腸菌長期進化実験 (LTEE) で、好気的クエン酸利用 (Cit+) は **12 集団中ちょうど 1 つ**で約 31,500 世代目に進化した (Blount, Borland & Lenski 2008)。鍵は **順序立った potentiation (前駆変異の蓄積) → actualization (citT のタンデム重複によるプロモータ捕獲) → refinement** という高次元・歴史依存の経路 (Blount et al. 2012)。リプレイ実験が「歴史的偶発性」を「一定率の稀変異」から区別した。これは contingency・epistasis・高次元でこぼこ地形を探索する価値を **本物で例示**する ── ③ が効きうる regime の実例です。

> **honesty 注意 (これは私たちの条件文の "前件" にしか対応しない)**:
> - **LTEE は niching アルゴリズムを使っていない**。ただの自然選択で、12 並列集団は **それ自体がランダムリスタート的な設計**。だから「contingency + 多様性が稀な革新を可能にする」存在証明であって、「niching が強 restart baseline に勝つ」証拠 **ではない**。
> - 「大腸菌がゼロからクエン酸を食べる力を獲得」は俗説の誇張。革新は **制御 (既存トランスポータの好気発現) = exaptation** で、新規遺伝子でも新規生化学でもない。
> - Van Hofwegen et al. (2016) が「直接選択ならもっと速く Cit+ が出る」と示し、「稀/偶発」枠組みに異議を唱えた (Lenski 側は LTEE 条件下の potentiation とは矛盾しないと反論)。「極めて稀/長期遅延」物語に寄りかかるなら、この **係争中の追試**も併記すべき。

##### 9.5 接地のまとめ

| 極 | 生物学 | 地形 | ③は効く? | 私たちの基質 |
|---|---|---|---|---|
| 低次元/滑らか | 暗化モフ (単一座位, s≈0.1-0.2, 方向性) | 単峰・シフト | **No** — マス選択で十分 | BG9 kernel union; ESN/ridge テキスト proxy (決定論・滑らか) |
| 高次元/偶発 | レンスキー Cit+ (potentiation→actualization→refinement) | でこぼこ・変異で谷越え | **Yes** (効きうる regime) | 合成だまし corridor (behavior = 24 次元の平均) |
| 経験的判定 | コイン・バートン・トゥレリ: マス選択でたいてい足りる、シフティング・バランスは稀にしか決定的でない | 実地形はたいてい単純 | 私たちの **negative の鏡** | 試した全 CPU 基質 |

**結論**: ライトのシフティング・バランスは「③が効くとき**なぜ**効くか」の正しい生物学先例、ライト-フィッシャーの epistasis/ruggedness 軸は「**次元**条件」の正しい枠組み、暗化モフとレンスキー Cit+ は低次元/高次元の clean な両極、コイン批判は私たちの **negative** の生物学先例。**ただし、これらは計算結果を証明しない。接地するだけ**。たとえが一番ゆるむのは、生物が cost (Phase III の gene-flow trap) を加える点 ── 私たちの stateless 設定にはそれが無い。

— 一服。100 年前の論争が同じ形だと気づいたときは、正直ゾクッとしました。ただし「ゾクッとした」を「証明」と取り違えないのが今回の規律です。 —

---

#### 10. GPU への含意 — 残された路は高次元だけ、しかし依然 bet

arc は CPU の路を全部閉じました。実 proxy は noise-free で滑らか (IV)、最後の候補 (kernel 多様化) は構造的に閉じた (V)。③の残された路は **高次元の地形のみ** ── それを提供するのが **full-LLM のパラメータ/損失空間 (数百万次元)** です。

構造的洞察は GPU の賭けを **better-motivated** にします。「full-LLM だけが例外かも」という盲目的な賭けではなく、「**③ は高次元を要し、full-LLM が高次元域**」という原理に沿う賭けになる。

**ただし依然 bet**。生物学の Cit+ が「③ アルゴリズムの勝利」を証明しないのと同じ理由、そして BG9 で RR に勝てなかったのと同型の理由で ── **実 LLM 地形が backprop (勾配降下) という強 baseline で直接ナビゲートできるなら、③はやはり不要**。難所が高次元なのは **必要条件であって十分条件ではない**。「強い直接法が解けない」ことを追加で示す必要がある (CPU では RR、GPU では勾配降下)。

だから GPU は「③のため単独」でなく **ポートフォリオ判断** (llive の実 LLM fitness 等と相乗り) + **クラウド借りで事前登録 1 本** (資本コミット前) が適正。go/no-go 基準も falsifiable に書けます:

> **full-LLM の難所は behavior で高次元か、かつ強い直接 baseline (勾配降下) で到達困難か?** 高次元でも勾配が直接届くなら③不要 (= BG9 の RR 結果の GPU 版)。

---

#### 11. メタ教訓 — 正直さは、勝つための道具だった

この arc の本当の成果は数値ではなく、**「整いすぎた結果を疑う」精神が実際に研究を前へ進めた**ことです。

- **存在証明 (I)** で勝ったとき、谷を消した境界実験で「③は万能ではない」を自分から確かめた (勝ちを過大評価しない)。
- **汎化 (III)** でペアレビューが 3 つの rerun ブロッカーを突きつけたが、直しても結論は変わらなかった (脆い negative ではないと確認)。
- **決定論測定 (IV)** で評価ノイズを物理的に消したから、「滑らか」が地形の性質か計器の限界かを切り分けられた。
- **BG9 (V)** では敵対検証で自分の「③が立たない」を**反証しようとして反証できず**、構造として確証された (negative を正しく negative と確定する方向でも同じ規律が効いた)。

さらに arc 全体で 1 つ学んだのは ── **低次元の難所は強 baseline が直接解いてしまう。だから③ (選り分けて育てる工夫) が効くには "高次元 behavior 空間" が要る**。「だまし地形を作れば③が立つ」は半分しか正しくなくて、正確には「**直接サンプルできないほど高次元な**だまし地形」でないと③は立たない。そして驚いたことに、この境界条件は **ライトのシフティング・バランスとコイン批判が 100 年近く前に到達していた**ものでした。

「異常に良い結果が出たら、勝った気になる前に必ず内訳を疑う」── FullSense の研究規律 (`honest disclosure`) は、ただの自戒ではなく、**実際に偽陽性を捕まえ、negative を正しく確定し、研究の精度を上げる機構**として 6 段全部で回っていました。

結論を、最後にもう一度、正確に。

> **③ が活きるのは「高次元の」だまし地形のときだけ**。存在証明 (合成 corridor) では圧勝したが、実 CPU 基質は ── 記憶タスク (床/天井) も、多タスク汎化 (滑らか) も、実 proxy テキスト地形 (noise-free で滑らか) も、kernel 多様化 (低次元・構造的に閉) も ── どれもその条件を満たさなかった。**「③ 決着 = ③ は不要と判明」ではなく**、「③ が活きる条件 (高次元のだまし地形) を、今 CPU で測れた実物もどきは満たさなかった」。本丸 (GPU 高次元) はまだ先で、しかも「強い直接 baseline が解く」リスクを抱えた賭けです。そしてこの結論の骨格は、20 世紀の進化生物学が既に描いていました ── ただし生物学はそれを **証明するのでなく、接地するだけ**です。

---

**Tags**: 進化計算 / MAP-Elites / 統計検定 / honest disclosure / 進化生物学 / CPU 研究
**関連**: 連載 #33 (第三軸 ③ 決着 Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (反証・Goodhart・proxy 限界)
**Project**: llcore (PyPI 予約 llmesh-llcore、リポジトリ未公開のためローカル研究)

---

---

# English


## 1. AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin

:::note info
**📚 FullSense Knowledge Base** <!-- fullsense-team-kb -->
The full FullSense development history — 60+ articles in 4 languages, with a story-based reading guide, plain-language editions, and 4-panel manga — is consolidated in our Qiita Team **FullSense KB** (team members only).
:::

### After Evolving an AI for 500 Generations, Only "Me" and "Karl Friston, the Father of Predictive Coding" Were Left in the World #25 — An Honest Disclosure of Monoculture and the Selection-Pressure Component lldarwin

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

#### 0. The plot in three lines (the "intro" as in rakugo)

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

#### 1. Why sow "people" as seeds?

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

#### 2. The result — only 2 survived

The lineage occupancy after 500 generations (the breakdown of
max_lineage_share):

```
Furuse         ████████████████████████████  52%
Friston        ██████████████████████████    48%
Millidge       (extinct)
Isomura        (extinct)
Oka Kiyoshi    (extinct)
Grothendieck   (extinct)
von Neumann    (extinct)
Feynman        (extinct)
```

At first glance you could write a **narrative** that "predictive coding (Friston)
and provenance-orientation (Furuse) beat abstract mathematics (Grothendieck) and
formal computation (von Neumann)".

On social media, "I evolved an AI and predictive coding turned out strongest"
might even go viral. **But not doing that is FullSense's honest-disclosure rule**
([[feedback_benchmark_honest_disclosure]]). When an abnormally clean result
appears, doubt the breakdown before feeling like you've won.

The result of that doubt is the next section.

---

#### 3. The true cause — "perfect-score inflation" erased the selection pressure

##### 3.1 Symptom: best_score is 1.0 from generation 1

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

##### 3.2 Root cause: the double collapse of the evaluation function `fitness_rich`

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

#### 4. The countermeasure — after "measuring" comes "culling": lldarwin

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

##### 4.1 The core of the design — a selection pressure that "does not aggregate"

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

##### 4.2 Make "what LLMs are bad at" the selection pressure

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

##### 4.3 Monitor for total wipeout — SPC alarm

FullSense's core idea is **SPC (statistical process control)**. In lldarwin too,
we record `max_lineage_share` / archive growth / behavioral diversity every
generation, and **detect a monoculture ratio > 0.8 with an SPC_ALARM** to
automatically adjust the cadence and parameters. The goal is to make this time's
"8→2" structurally impossible to recur.

---

#### 5. Lessons (left as honest disclosure)

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

#### 5.5. The 2-tier structure of "the glasses" and "the culler" — why separate them (a deep dive)

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

#### 5.6. Diagram ideas (candidates to turn into SVG before posting)

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

#### 6. Related

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

## 2. 「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26（多目的淘汰 / ε-lexicase / 中立貯蔵庫 / 実 LLM 評価）

:::note info
**📚 FullSense Knowledge Base** <!-- fullsense-team-kb -->
The full FullSense development history — 60+ articles in 4 languages, with a story-based reading guide, plain-language editions, and 4-panel manga — is consolidated in our Qiita Team **FullSense KB** (team members only).
:::

### Measuring with "Glasses" Alone Doesn't Drive Evolution — Design and Measurements of the Selection-Pressure Component lldarwin #26

> **Concept hook**: In the previous article #25, I exposed a massive failure: "When I evolved an AI for 500 generations, the only ones left in the world were **me and Friston**."
> Oka Kiyoshi, Grothendieck, von Neumann — all of them quietly vanished mid-evolution. The cause: the evaluation function (the glasses = lleval) kept handing out perfect scores, so **the selection pressure dropped to zero**. Even if you can "measure" who is superior, if you can't convert that difference into "who survives," evolution degenerates into mere genetic drift.
>
> So then — granting that the glasses let us "measure" the differences, how do we build the device that **correctly converts** those differences into "selection"?
> That is the star of this article, **lldarwin**. A new member of the ll- family, it is the component **specialized in selection (selection pressure)**.
>
> The one keyword I want you to remember from this article is a single word: **"don't aggregate."** The moment you add multiple rulers together into one, evolution breaks. Why that happens, and how I overcame it with measurements — picking up from the failure, this time I'll tell a story about something that **actually worked**.

---

#### 0. The gist in three lines (the rakugo "pillow")

In rakugo, there's a "pillow" before the main story. First, the whole picture in three lines.

- **lleval measures, lldarwin selects** — evolution only becomes meaningful as a two-stage structure of "measuring" and "selecting."
- The first principle of selection is **multi-objective selection that does not aggregate multiple selection pressures**. Here we structurally cut off the true cause of #25's failure (collapsing it with the argmax of a single scalar).
- The three adopted pillars = **ε-lexicase + minimal-criterion QD + down-sampling** (selected by surveying 616 documents in the evolutionary_computation corpus).

And this time, the difference from #25 is that there's not just the skeleton but **actual measurements**. With novelty pressure I doubled behavioral diversity from 7.12 → 14.88 (+109%), with the **neutral reservoir** I actually **revived every one** of the "extinct Oka Kiyoshi / Grothendieck lineages," and finally, against a **real on-prem LLM (llama3.2)**, I evolved prompt strategies and improved a weak task from 0.0 → 1.0. Let's go through it in order.

---

#### 1. Why separate "measuring" and "selecting"

The llive family already has **lleval (the glasses = the evaluation framework, series #24-08)**. It is a device that observes an individual's behavior and scores it along multiple axes.

But what #25 revealed was a fatal truth. **Even if you can measure differences with the glasses, if you collapse those differences into one with argmax, selection breaks.** Concretely, `fitness_rich` was folding multiple archetype similarities into a single scalar via `nearest = max(sims)`. This is the SEL-2 violation — the true cause of "best=1.0 saturates, everyone gets a perfect score, and the selection gradient disappears."

If we clearly divide the roles, it looks like this.

```
lleval   = measure (converts an individual's behavior into a "multi-axis pressure profile")
lldarwin = select  (converts that profile into "the parents of the next generation")
```

The output of `lleval` is a **case vector** (an array of scores along each axis). `lldarwin` receives it as an input contract and selects **without aggregating**. This is exactly the boundary of responsibility between them. If lleval hands over the data after "adding the axes into one," lldarwin can do nothing. So on the lleval side we impose the contract: "you must always keep and pass the breakdown (the per-axis decomposition)."

lldarwin's `Pressure` interface is expressed by the following minimal contract.

- `name` — the name of the axis (`typo_robustness`, etc.)
- `evaluate(individual_output) -> case_scores: list[float]` — converts an individual's behavior into a "per-axis score array"
- `is_proxy: bool` — whether it is a proxy measurement or a real LLM/VLM measurement (the distinction of measurement purity)
- `minimal_criterion: float | None` — the minimum reproduction criterion for that axis (no gate if None)

The point is that the return value of `evaluate` is **a list, not a scalar**. Within a single axis there are multiple cases (test cases), and we pass them to lldarwin without collapsing them. This "don't collapse" design is the foreshadowing that will rescue the specialist later.

> 🍵 **Break point**: The meaning of separating the glasses (lleval) and the filter (lldarwin) is, in photography terms, the difference between "metering exposure" and "deciding which shot to adopt." Even if the light metering is perfect, if you choose the best shot wrongly the album is ruined. Even if the light meter (lleval) tells you "this one is 80 for brightness, 30 for composition, 95 for expression," whether you round it to "average 68" and discard it, or "keep the one with 95 expression in a separate slot," changes the richness of the album as much as heaven and earth. lldarwin is the specialist in "adoption decisions." If you make the measurer and the chooser the same person, usually both turn out sloppy.

---

#### 2. The core of the design — the "don't aggregate" 7 stages

lldarwin selects the pressure profile (the multi-axis case vector) received from lleval through the following 7 stages. To each I attach "why it is needed = which failure it prevents."

1. **Standardizer** — per-dim z-score. It does not favor the featureless honor student who is merely "uniformly high across all axes," and instead turns the **deviation** on each axis into selection pressure. Central agreement (being the same as everyone) is excluded.
   - *Failure prevented*: the entrance to monoculture, where the mediocre who are "merely high on average" win and sharp individuals disappear.
2. **MinimalCriterionGate** — splits reproduction eligibility by a minimum criterion on each axis. Does not let a "winner-take-all" happen by continuous ranking alone.
   - *Failure prevented*: the total-wipeout scenario where a single strongest one monopolizes all reproduction slots. By a "minimum guarantee" that lets anyone who meets the criterion reproduce, the foundation of diversity is preserved.
3. **EpsilonLexicaseSelection** — evaluates the axes one by one independently as cases. A specialist that stands out on some axis (mediocre on others) can survive.
   - *Failure prevented*: the extinction of specialists by aggregated argmax. This is the very mechanism that produced #25's 8→2.
4. **QD / MAP-Elites archive** — converts the pressure profile into a behavior descriptor and keeps an elite per cell. The archive grows monotonically.
   - *Failure prevented*: structural total wipeout. As long as even one individual remains in one cell, that behavior does not disappear.
5. **Niching / FitnessSharing** — down-weights individuals in the same niche so multiple peaks can coexist.
   - *Failure prevented*: aggregation onto a single peak (monoculture).
6. **Down-sampling** — every generation, evaluates only on a subset of cases to perturb the environment.
   - *Failure prevented*: over-adaptation to a specific peak and a plateau (a stagnation plateau). By making it a moving target, it forbids "winning the same way."
7. **NoveltyScorer** — when stagnating, applies exploration pressure toward "behavior different from the past."
   - *Failure prevented*: exploration exhaustion. When improvement stops, it rewards novelty itself to push outward.

Contrasting with #25's 8→2 monoculture, the core is the three: **(3) ε-lexicase, (4) QD archive, (2) minimal-criterion**. In #25 these were all missing and only the single-scalar argmax was running. So "the one lineage strongest on average" took all the continuous ranking, and the rest disappeared by drift. By "bundling these three without aggregating," lldarwin builds a structure that does not break down even as generations accumulate.

> 🤔 **An analogy (manzai style)**:
> Boke: "I added up all the test scores and ranked them, and only honor students with high averages were left."
> Tsukkomi: "That's zero diversity! The genius with 100 in math and 0 in everything else has vanished!"
> Boke: "Well, looking at the total, the honor student is higher..."
> Tsukkomi: "**Don't look at the total!** If you look at the subjects one by one, that genius loses to no one on the 'math' case. ε-lexicase is the mechanism that rescues that. The moment you sum, the genius dies."
> — Summing (aggregation) kills the specialist. Because ε-lexicase "looks at the subjects one by one," the sharp ones survive. This is the very first principle of lldarwin.

---

#### 3. Why these 3 pillars (the rad-research backing)

As the strongest candidate fusion that "does not break down even as generations accumulate," I selected it by surveying 616 documents in the evolutionary_computation corpus. The provenance matters: I did not invent it myself, but selected and bundled the "don't aggregate" lineage of existing research.

| Method | Effect | Source |
|---|---|---|
| **ε-lexicase** | specialist preservation, high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | total wipeout impossible thanks to per-cell elites | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | environmental perturbation, cost reduction | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | prevents premature convergence (future option) | Lyu 2020 (2005.07376) |

The three pillars look like disparate methods, but in fact they can be skewered by **one single idea: "don't aggregate."** ε-lexicase "does not aggregate the axes." QD "does not aggregate the behavior space (keeps it per cell)." Down-sampling "does not fix the evaluation environment (perturbs it every generation)." Each shares the same philosophy in not "rounding into one." So even when combined, the ideas do not clash and instead synergize.

> 🍵 **Break point**: People ask, "Why not invent it yourself?" The answer is simple: **because the combination of existing research is strong enough**. My development rule ([[feedback_originality_over_imitation]]) says: "The adoption of external algorithms is **selection**, not coverage. Exclude breakdown risk and mere imitation, and adopt only what adds value to the original design." lldarwin's originality is not "having invented a new selection algorithm," but "**the way it bundles these without aggregating**, and **actually wiring** that into llive's evolution loop." In cooking terms, it's not creating the world's first ingredient, but the craft of "plating famous existing ingredients on one dish without mixing them." Ingredients that would be ruined if mixed are made to coexist without mixing.

---

#### 4. Stage1 — doubling behavioral diversity with criteria exclusion + novelty pressure

From here it's measurements. In Stage1, rather than implementing the whole design at once, I put in only the two changes most likely to be effective and measured (llive, branch `optimize/core-2026-05-20`, commit `8060204`).

**Change 1: criteria exclusion.** From the cases of ε-lexicase, I removed `factor_score` (= the single scalar of max-archetype = argmax, the very cause of #25's best=1.0 saturation) and `nearest_persona_idx` (= a category index with no meaningful ordering). This is a cleanup that "removes bad rulers from the material used to judge selection."

**Change 2: novelty pressure.** I enabled `MultiPressureSelector(use_novelty=True)`. Every generation it computes the k-NN average distance to the archive of past generations (Lehman-Stanley style novelty), z-scores it within the population (STD-1), and mixes it into selection as an additional lexicase case. It evaluates "behaving differently from everyone else" itself as one of the axes.

For tests, I expanded `tests/unit/test_evolutionary_lldarwin.py` from 8 → 10 (adding exclusion and novelty preservation). 847 evolution-system tests green, no regression.

The measurement conditions are rich-proxy, 8 founders + pop24, 150 generations, seed 0. The results are below.

##### 4.1 Behavioral diversity (diversity_l2) — the metric where novelty works

| Condition | mean | tail30 min | final |
|---|---|---|---|
| BASELINE (pre-exclusion, old lldarwin equivalent to Tournament) | 7.12 | 0.68 | 0.83 (collapse) |
| A: criteria exclusion only | 9.16 | 1.57 | 1.57 |
| **B: exclusion + novelty** | **14.88 (+109%)** | **6.56 (9.6×)** | **11.73 (collapse avoided)** |

Novelty pressure maintained behavioral (genome-space) diversity at about double, and prevented the late-stage diversity collapse. Criteria exclusion alone is also effective on its own (to the extent it removes spurious argmax pressure). Whereas BASELINE **collapses** at final 0.83, condition B **holds its ground** at final 11.73. This is the first tangible sense of the "don't aggregate" design.

![Fitness and diversity of the Stage1 baseline (no novelty). Diversity collapses in the late stage](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_en.svg)

![Stage1 with novelty. Diversity is maintained until the late stage](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_en.svg)

Placing the two side by side, the difference in late-stage behavior is clear at a glance. Whereas the baseline's diversity curve sticks to the floor, the one with novelty runs to the finish while keeping a high level.

> 🍵 **Break point**: To liken novelty pressure to a goldfish pond — if you keep only the goldfish swarming around the food (high fitness), eventually you get a pond where everyone moves the same way in the same place. Novelty pressure is the role that "**gives a bonus to goldfish swimming in different places from everyone**" too. As a result, you get a pond scattered everywhere, one you never tire of watching. But don't let your guard down here. In the next section, a **pitfall** lurking in this "lively pond" is discovered.

---

#### 5. honest disclosure (most important) — I had been confusing behavioral diversity and lineage survival

This is the most important section of this article. Just because a good number (+109%) came out does not mean I get to feel like a winner — this is my iron rule ([[feedback_benchmark_honest_disclosure]]). I doubted the breakdown. And I found a mistake.

##### 5.1 Lineage fixation (founder_counts) — the metric novelty does not improve

In the same measurement, I look at a different metric. "Of the 8 founders (ancestral lineages), how many lineages survived to the end?"

The result — **in all conditions, it ultimately converged from 8 → 2 lineages** (furuse-kazufumi + friston). oka-kiyoshi (Oka Kiyoshi) / grothendieck (Grothendieck) / von-neumann / feynman / millidge / isomura all **went extinct**.

Even though I put in novelty and doubled behavioral diversity, **the lineage survival was exactly the same 2 lineages as #25**.

##### 5.2 Why — I had been confusing two kinds of "diversity"

The TODO in the design document (as of #25) said "verify in a re-run whether the Oka Kiyoshi / Grothendieck lineages survive." This was **confusing behavioral diversity with lineage survival**.

The author's comment in `poc_evolution_env.py` (L129-132) pins down this confusion precisely.

> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs QD niching on lineage / PERSONA-FX, not pure novelty**"

Broken down, it's this.

- The demonstrated monoculture 0.05 is **behavioral** (the occupancy rate of archive cells), not **lineage-based**. What novelty/lexicase improves is "the spread of behavior," not "the survival of ancestors."
- That lineage fixation heads toward monoculture by neutral drift (Motoo Kimura's neutral theory of evolution) is **theoretically normal**. It is not collapse. Both novelty and lexicase have only mechanisms that **preserve existing individuals**, and have **no mechanism to revive a lineage that has once gone extinct**. So lineage fixation cannot be stopped structurally.
- Furthermore, the inter-archetype distances are also compressed at 0.068–0.29 (similarities densely packed in 0.71–1.0), so the selection gradient is weak and drift dominates. friston is the most non-central (centroid distance 0.162) yet survived = it was not centrality (strength) but **luck (drift)** by which the 2 lineages fixed.

In other words — my wish that "I want Oka and Grothendieck to survive" was a disease that **the medicine of raising behavioral diversity can absolutely never cure**. I had the wrong medicine. This is a lesson worth recording honestly.

> 🍵 **Break point**: Put in manzai terms.
> Boke: "I increased the goldfish that move in colorful ways in the pond! Diversity is perfect!"
> Tsukkomi: "And the **bloodline**? Of the 8 goldfish families that existed, how many are left?"
> Boke: "...two."
> Tsukkomi: "The movements are flashy but the family tree is threadbare! Diversity of movement and diversity of bloodline are **separate matters**!"
> — "Behavior is diverse" and "lineage is diverse" are entirely different metrics that merely look alike. I had been confusing them. I expose it honestly.

---

#### 6. Stage1.5 — reviving extinct lineages with a neutral reservoir

Once you understand the true nature of the disease, you can change the medicine. What lineage survival needs is "a mechanism to re-inject extinct lineages every generation" — a **lineage-niched neutral reservoir**.

##### 6.1 First, confirm the mechanism with a PoC

Rather than remodeling the production loop right away, I first confirmed the mechanism runs with a standalone PoC ([[feedback_poc_feasibility_first]] = requirements → PoC → feasibility → detailed design, llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`).

Selection reuses Stage1's `MultiPressureSelector` (criteria exclusion + novelty). Fitness is rich-proxy. Lineage is inherited from parent_a. **The reservoir = keeps the best-ever genome per lineage and re-injects extinct lineages every generation** (replacing low-score children; the best is not destroyed). I measured with 8 founders + pop24 + 150 gens + seed 0.

| reservoir | final named lineages | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1** (oka-kiyoshi 24/24 = complete monoculture) | 1.00 | 1.58 |
| **ON** | **8 (all founders survive)** | **0.31 (≪ 0.8 OE-3)** | 1.69 |

With reservoir ON, **all 8 lineages survived**, including Oka (oka) and Grothendieck (grothendieck). The final shares are friston 7 / furuse 6 / grothendieck 4 / oka 3 / the other 4 lineages 1 each. The ideal behavior: **strong lineages reproduce with descendants, while weak lineages are kept alive by the reservoir**. Behavioral diversity also did not drop (1.69 vs OFF 1.58).

**Honest caveat (PoC stage)**: Because the reservoir re-injects frozen elites (frozen representatives), the "survival" of weak lineages (1 individual each) is due to re-injection, not active evolution. This is legitimate per the very definition of a neutral reservoir (keep representatives and make them recombinable), but I do not claim "weak lineages keep actively evolving."

##### 6.2 Integration into the production EvolutionLoop (additive + default-off)

Since the mechanism was confirmed by the PoC, I integrated it into the production `EvolutionLoop` (commit `b03cbda`). The crux of the design is **additive and default-off** — it changes none of the existing behavior, and becomes active only when the flag is set. I defended backward compatibility to the death.

- Added the `EvolutionLoop.on_population_bred` hook (can transform the bred list right after breeding, before evaluation; default None = backward compatible).
- `LineageReservoir` (`lineage_reservoir.py`): ancestor tracking (inheriting parent_ids[0]) + per-lineage best-ever retention + re-injection of extinction-protected lineages. It shares `founder_map` and stays consistent with the lineage log.
- Added `run_persona_evolution(lineage_reservoir=True)` / the run-script flag `--lineage-reservoir`.
- tests: `test_evolutionary_lineage_reservoir.py` 6 + evolution-system **937 green** (no regression).

Measurement in the real EvolutionLoop (rich-proxy + lldarwin + novelty, 8 founders / pop24 / 150gens / seed0).

| Condition | named lineage survival | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8 (furuse 17 + friston 7) | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8 (all lineages)** | **0.33** | **0.29 (≪ 0.8 OE-3)** | 9.20 |

**All 8 lineages survived in the real loop**, including Oka (oka 3) and Grothendieck (grothendieck 1). The production implementation reproduced the PoC's prediction (fixation 0.31) at 0.29 — proof that the mechanism worked as designed.

This is the biggest highlight of this article. Compare the two below.

![Neutral reservoir OFF. The lineage-dominance stream ultimately collapses to 2 lineages, furuse 71% / friston 29%](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_en.svg)

![Neutral reservoir ON. All 8 lineages (millidge / von-neumann / oka / grothendieck, etc.) coexist](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_en.svg)

OFF (top): as generations advance, the stream gets swallowed into 2 colors — a reproduction of #25's "only me and friston remained." ON (bottom): 8 colors remain as bands until the end. Neither Oka nor Grothendieck has disappeared.

![Fitness and diversity with the neutral reservoir ON](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_status_en.svg)

> 🍵 **Break point**: That lonely world I lamented in #25, "only me and Friston remained." This time it has changed into a lively world where Oka, Grothendieck, and von Neumann are all present. **This is not fabrication; it is a result that actually ran** (following [[feedback_benchmark_honest_disclosure]], I write neither false failures nor false successes). But — before getting carried away, recall the attitude learned in §5. "When a good number comes out, doubt the breakdown." In the next §6.3, I honestly write that this success too came with a **cost**.

##### 6.3 Honest caveat — lineage retention and behavioral diversity are a weak trade-off

With reservoir ON, all lineages survived. But look closely and **diversity_l2 drops from 14.88 → 9.20**. Because frozen elites (frozen representatives) are re-injected every generation, the spread of genome space decreases somewhat.

However, the collapse when OFF (final 0.83) is avoided. In other words, it's a **weak trade-off** relationship: "if you take lineage retention, the peak of behavioral diversity drops a little, but collapse can be prevented." It is not zero-cost magic. I write this honestly. And how far this cost can be minimized becomes the subject of the next sweep.

---

#### 7. Re-injection frequency sweep — a non-trivial discovery of a non-monotonic optimum

I characterized §6.3's honest caveat (frozen elite re-injection lowers diversity) with a sweep of `reinject_interval` (the generation interval at which re-injection is performed; default 1 = every generation) (commit `da93dd3`). I added `LineageReservoir.reinject_interval` + the `--reinject-interval` flag (7 tests). 8 founders / pop24 / 150gens / seed0.

| interval | named survival | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1** (every generation) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84 (max)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**Here there was a non-trivial discovery.** Intuitively, you'd expect that "the more you reduce re-injection (raise the interval), the less the frozen elites are pushed in, and diversity recovers monotonically," right? But — **diversity did not increase monotonically; it peaked at interval=5** and actually dropped at 10/20.

When you think about the reason, it makes sense. If you leave the lineages alone too much (the interval is too large), (a) the diversity injection originating from the reservoir decreases, and (b) a few lineages fix, so in the end diversity doesn't grow either. Both "re-injecting too much" and "leaving alone too much" are bad, and there is an optimum in between. This is a finding that **could not have been predicted without actually running the sweep**.

The operational guideline became this.

- If you **prioritize lineage retention above all** → interval=1 (8/8 all lineages survive).
- If you want to **also achieve behavioral diversity** → interval=5 (retains 5/8 while maximizing diversity).

The optimum for achieving both depends on the fitness design and the population size, so in production I re-calibrate it with a sweep.

![The trade-off of re-injection frequency. Lineage retention and behavioral diversity are inversely related, and diversity peaks at interval=5 (non-monotonic)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_en.svg)

> 🍵 **Break point**: Like the sage (punchline) of a rakugo, there is a "twist that betrays expectations" here. I thought "the more you do it the better," but it was "do it too much and it backfires." Same as watering plants: water too little and they wither, water too much and the roots rot. The optimum is in moderation. When you do evolutionary computation, you meet these "non-monotonic curves" again and again. That's why you measure baselines and run sweeps. Intuition is often betrayed.

---

#### 8. Stage2 first half — making "the LLM's weaknesses" into selection pressure by proxy

Up to here I confirmed the mechanism with rich-proxy (a heuristic based on persona similarity). Next I implement another pillar of the design: **making "axes where the LLM/VLM is actually weak, and which are measurable" into pressures** (a series of commits, `pressures.py`).

I made the 5 proxy-capable axes listed in design §3 into plugins.

| pressure (LLM weakness) | related thought factors (case) |
|---|---|
| typo_robustness (noise tolerance) | consistency / reality_link / uncertainty |
| polysemy_wsd (polysemous words) | multiview / consistency / reality_link |
| multistep_robustness (multi-step reasoning) | structurize / closed_loop / self_extend |
| calibration (confidence estimation) | uncertainty / provenance |
| context_management (irrelevant-context tolerance) | consistency / provenance / recompose |

`make_pressure_fitness()` outputs the cases of each pressure (14 in total) into the breakdown, and lldarwin's ε-lexicase **selects specialists per axis without aggregating**. Added `--fitness pressure-proxy`. tests `test_evolutionary_pressures.py` 4 + evolution-system **942 green**.

End-to-end measurement (pressure-proxy + lldarwin + novelty + reservoir, 8 founders / 120gens): named lineages **8/8 survive** / lineage_fixation (tail) 0.67 / diversity_l2 (tail) **17.91**. The 14 weak-axis cases are selected independently, and behavioral diversity is high. Lineages are maintained by the reservoir (because pressure-proxy does not directly reward persona identity, the dominant lineage's share becomes 0.67, higher than rich-proxy's 0.29).

![Population-mean trajectory of the 5 weak axes (typo / polysemy / multistep / calibration / context) (proxy measurement)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_en.svg)

**Honest caveat (an accepted limitation already stated in design §7 / §7.1)**: The individual is not a real LLM but a genome (an llive configuration). What this pressure measures is **a proxy for behavior** — "how much the genome possesses the **thought factors related** to that weakness" — and is **not the LLM ability of production**. This is limited to **the verification of mechanism feasibility (that the mechanism runs)**. The Goodhart risk (surface strategies that hack the proxy evolve) is also an accepted limitation. The actual measurement of real LLM/VLM weak axes is carried over to the second half of Stage2 (which presupposes the OLLAMA_HOST setting + the individual→real-LLM mapping).

> 🍵 **Break point**: This is easily misunderstood, so let me press the point. I have **not yet said** "I overcame the LLM's weaknesses by evolution!" What the proxy measures is only "whether the mechanism runs." Whether a real LLM became robust to typos is, at this stage, completely unknown. Even if a flashy number (17.91) comes out by proxy, that is proof that "the device works," not proof that "the contents got smarter." The moment you blur this line, the research becomes a lie. So next, I face **the real LLM**.

---

#### 9. Stage2 second half — evolving prompt strategies against a real on-prem LLM

Once I found that localhost's ollama (llama3.2:latest, etc.) was reachable, **real LLM evaluation** finally became possible (commit `2fb2912`). Because localhost = on-prem, it also satisfies the discipline of measurement purity (do not mix with cloud LLMs) ([[feedback_llive_measurement_purity]]).

##### 9.1 The individual → real LLM mapping (Promptbreeder lineage)

The crux is "how do you make the genome take effect on a real LLM?" In `real_pressures.py` I implemented the **individual → real LLM mapping**.

- **Convert the individual's `c_prompt` (PromptChromosome) into a system prompt**: skill_set → instructions / prompt_template_id → reasoning style / language_style → tone. We put this system prompt over a fixed LLM (llama3.2), make it solve the **real tasks** of the 5 weak axes, and score it.
- **Fix the LLM body and evolve the prompt strategy (genome)** = select, by measurement, "which prompt strategy mitigates the LLM's weaknesses." This follows the style of Promptbreeder (the research lineage that optimizes prompts evolutionarily).
- Deterministically with temp=0 (greedy). Cache `(system_prompt, task)` (the same strategy is not re-evaluated).
- robust: per-call try/except (an ollama hiccup is treated as the task's lost points, and the run continues).
- Added `--fitness real-pressure` / `--ollama-model` / `--max-wallclock-seconds`. tests 5 + evolution-system 947 green.

##### 9.2 Demonstration of a real selection signal — the CoT+structure strategy takes multistep from 0.0 → 1.0

And then, a real selection signal was observed.

**The CoT+structure strategy** (`chain_of_thought` + structurize + loop) **improved llama3.2's multistep (multi-step reasoning) from 0.0 → 1.0** (the terse strategy fails at 0.0; the score rose 0.80 → 1.00).

This means that lldarwin's claim "the evolution of prompt strategies can mitigate the LLM's weaknesses" was **demonstrated not by proxy but on a real LLM**. Even with the same llama3.2 body, depending on the system prompt put over it (= the evolved genome), the multi-step reasoning task is solvable or not. Evolution actually selected "a solvable prompt strategy."

![Population-mean trajectory of the 5 weak axes (real on-prem LLM llama3.2 evaluation). The evolution of prompt strategies improves the axes](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_en.svg)

##### 9.3 The 12h continuous run

Since real LLM evaluation is heavy, I launched a long continuous run (`out/lldarwin_12h_realpressure_2026_05_26/`).

```
--fitness real-pressure --selection lldarwin --novelty --lineage-reservoir
--genome3d --population 24 --max-wallclock-seconds 43200 --checkpoint-every 5
```

It stopped safely at wallclock 12h (snapshotted → can continue with `--resume`). During the continuous run it reached best_score=1.0.

![Fitness and diversity of the real LLM evolution run (12h continuous run)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_en.svg)

##### 9.4 Honest caveat (the limitations of real LLM evaluation)

This is the culmination of the attitude learned from #25. Precisely because a flashy result came out (0.0 → 1.0, best 1.0), I write the breakdown thoroughly and honestly.

- **(a) Only `c_prompt` participates in fitness.** persona / c_factors are neutral (lineages are maintained by the reservoir, initial selection is handled by novelty). In other words this is "**the evolution of prompt strategies**," not "the evolution of personas." It's not that Oka Kiyoshi's personality got smarter, but that a prompt strategy tied to the Oka Kiyoshi lineage was selected.
- **(b) The initial c_prompt of all founders is identical (default).** So exploration is mutation-driven (diversifying the prompt per founder is a future improvement). Because the starting point is the same, the initial lineage differences have no effect on the prompt strategy.
- **(c) A small battery (2 questions per axis) = a noisy estimate.** Even the dramatic number 0.0 → 1.0 contains noise to the extent the number of questions is small. To make a statistically robust claim, a much larger battery is needed.
- **(d) on-prem only (measurement purity). It is not a claim about general ability.** This is an observation on a specific model and specific tasks (llama3.2), and I do not say "LLMs in general turn out this way."

If I hid these, I could write a flashy story like "evolution made the LLM dramatically smarter!" — but that would be a lie. What lldarwin demonstrated goes only as far as "**the mechanism, on a real LLM, produces a selection signal**." I make no claim crossing that line.

> 🍵 **Break point**: The most pleasurable moment in research is shouting "0.0 became 1.0!" But that very moment is when [[feedback_benchmark_honest_disclosure]] takes effect. "When a suspiciously good number comes out, doubt the breakdown before you feel like a winner." In this case — what won is the "prompt strategy," not the "LLM body" nor the "persona." The number of questions is also small. Only 1 on-prem model. Only after writing all of this can I say "I demonstrated it" for the first time. Honest disclosure is the muscle training of holding back from bragging.

---

#### 10. Reuse of existing assets (based on the codex code survey)

So as not to make the design a pie in the sky, I had my subordinate Codex survey the existing code, and found that **much was already implemented but unwired**.

- `mating.py:139 LexicaseSelection` (with ε, implemented but unwired → just wire it)
- `nsga2.py:197 NSGA2Selection` (for the ≤3-objective lane)
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**Newly implemented**: `Standardizer` / `MinimalCriterionGate` / the `Pressure` group / `MultiPressureSelector` (the core) / `LineageReservoir` (Stage1.5) / `SelectionAudit`.
**Wiring points**: inject `MultiPressureSelector` into `selection` at `loop.py:122`, add an injection point at `persona_evolution.py:606`, and connect `LineageReservoir` to the `EvolutionLoop.on_population_bred` hook.

> 🍵 **Break point**: That "implemented but unwired" was the most common was the biggest lesson. Even if you make good parts, **unless you wire (orchestrate) them, evolution stays broken**. The reason #25 went 8→2 is that ε-lexicase, NoveltyScorer, and QD were all "in the box but not wired." The essence of lldarwin is, more than the invention of new algorithms, "bundling good existing parts **without aggregating** and **actually wiring** them into the evolution loop." Even if you gather all the electronic parts, the radio won't make a sound unless you solder them.

---

#### 11. The guarantee of breakdown avoidance — a multi-layer structure that does not wipe out (already backed by measurements)

The multi-layer structure that refutes #25's monoculture (8→2) is assembled as designed, and this time it was **backed by measurements**.

1. **MinimalCriterionGate** — reproduction eligibility by a minimum criterion → suppresses winner-take-all.
2. **QD per-cell elite** — as long as even 1 cell remains, total lineage wipeout is impossible (the archive grows monotonically).
3. **Niching / FitnessSharing** — down-weight the same niche → multiple peaks coexist.
4. **Down-sampling** — destroy plateaus with a moving target.
5. **per-dim z-score + central-agreement exclusion** — do not favor the featureless.
6. **LineageReservoir (added in Stage1.5)** — a neutral reservoir for extinct lineages → structurally prevents total lineage wipeout (8/8 survival in measurements).
7. **monoculture monitor + SPC** — record max_lineage_share every generation, detect >0.8 with SPC_ALARM → auto-adjust.

In particular, (6) is **a layer added afterward** in response to §5's honest disclosure (novelty cannot stop lineage fixation). I found a hole in the design by measurement and plugged it. The measured lineage_fixation falls well below the OE-3 criterion (<0.8): OFF 0.70 → ON 0.29. The achievement of this article is that with the two-stage structure of "don't aggregate" + "revive extinct lineages," I could structurally crush #25.

---

#### 12. honest disclosure / risks (a preview)

I do not blindly trust the design. Let me summarize once more the accepted limitations (to be dug into in the next article #27).

- **Goodhart's law / proxy divergence** — when you make LLM weaknesses into proxy fitness, "surface strategies that hack the metric" evolve (typo → memorizing specific substitutions, WSD → using test heuristics, etc.). The proxy is limited to mechanism feasibility, and does not claim production ability.
- **Designer dependence** — lexicase=case / QD=descriptor / novelty=distance metric; in every case, the "direction of diversity" is decided by the designer. Unanticipated emergence on the scale of biological evolution is limited.
- **The minimal-criterion stagnation⇄collapse trade-off** / **the curse of dimensionality + archive saturation of QD**.
- **The limitations of real LLM evaluation (reprised from §9.4)** — only c_prompt participates in fitness, the founders' initial prompts are identical, a small battery, on-prem only.

> **Next time preview (#27)**: I honestly expose the most painful counterpoint, "when the glasses saturate, the selection pressure is powerless," together with the limitations of Goodhart's law and proxy fitness. lldarwin is not omnipotent. **How far we may claim** is the subject of #27. Precisely because good numbers like "8/8 survival" and "0.0→1.0" came out this time, next I temper it thoroughly with counter-evidence.

---

#### 13. Conclusion

- Evolution is a two-stage structure of "**measuring (lleval)**" and "**selecting (lldarwin)**." The core of selection is **"don't aggregate."**
- Stage1: with criteria exclusion + novelty pressure, I doubled behavioral diversity from 7.12 → 14.88 (+109%) and avoided the late-stage collapse.
- honest disclosure: novelty/lexicase preserve **behavioral diversity**, but **lineage fixation** heads toward monoculture by neutral drift (Kimura). I had been confusing the two kinds of diversity — recorded honestly.
- Stage1.5: with the lineage-niched **neutral reservoir**, in the real EvolutionLoop I achieved **OFF=2 lineages / ON=all 8 lineages survive** (including Oka Kiyoshi and Grothendieck), lineage_fixation 0.29 (≪0.8). **This is not fabrication; it actually ran.**
- Re-injection frequency sweep: the lineage-retention ↔ behavioral-diversity trade-off. The non-trivial finding that diversity peaks at interval=5 (**non-monotonic**).
- Stage2 first half (proxy): made the 5 weak axes into Pressure plugins (mechanism feasibility only).
- Stage2 second half (real LLM): with the individual c_prompt → system prompt mapping, scored real tasks on a fixed on-prem LLM (llama3.2). **The CoT+structure strategy improved multistep from 0.0 → 1.0.** Reached best=1.0 in a 12h continuous run.
- Without optimism, without feeling like a winner, I reported by separating the breakdown ([[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]]).

Just making good parts leaves evolution broken. **Bundle without aggregating, actually wire, revive extinct lineages, and confirm the selection signal on a real LLM** — only by going that far could I finally change #25's world of "only me and Friston" into a lively world where Oka Kiyoshi and Grothendieck are also present. In the next article #27, I question anew, with counter-evidence, how much trust we may place in this success.

---

#### 14. Related

- Series #25 "Only Me and Friston Remained" — the motivation for this article (a record of failure)
- Series #24-08 "Making the Glasses" — lleval (the measuring side)
- Series #27 "When the Glasses Fog Up, Selection Is Powerless Too" — counter-evidence investigation (honest disclosure)
- Design document: lldarwin (the selecting side) `docs/vision/LLDARWIN_DESIGN.md`
- Measurement of record: `docs/research/lldarwin_stage1_results_2026_05_26.md`
- llive commits: Stage1=`8060204` / neutral reservoir PoC=`0d0537d` / Stage1.5=`b03cbda` / reinject sweep=`da93dd3` / Stage2 real LLM=`2fb2912`
- Related memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]] / [[feedback_poc_feasibility_first]]

---

## 3. 一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27（開放端進化 / ライブ・オーケストラ / honest cross-validation）

:::note info
**📚 FullSense Knowledge Base** <!-- fullsense-team-kb -->
The full FullSense development history — 60+ articles in 4 languages, with a story-based reading guide, plain-language editions, and 4-panel manga — is consolidated in our Qiita Team **FullSense KB** (team members only).
:::

### Rebuilding AI Evolution Overnight — The Night a Real-LLM 12h Run Saturated at a Perfect Score Again, and 6 PoCs, 4 Agents, and Perplexity Independently Converged on the Same Conclusion #27

> 📚 **Series navigation (lldarwin arc)**: #24-05 population evolution → #25 the monoculture failure → #26 design → **#27 this article (climax)** → [#28 implementation (orchestra-style AI)](drafts/QIITA_#28_lldarwin_v2_phase1_orchestra.md). Each article stands alone (links are for browsing).

> **Concept hook**: In the previous installment (#25), I confessed a major failure: after evolving an AI for 500 generations, the only survivors left in the world were **Friston and me**. The cause was that the evaluation function (the "lens" = lleval) kept handing out perfect scores, so **selection pressure dropped to zero**.
>
> "Then this time, let's verify it with a real LLM." With that, I ran a **continuous 12-hour evolution** against on-prem llama3.2. Not a proxy (a synthetic ruler) — a real LLM.
>
> The result: **it pinned to a perfect score at gen5 and didn't budge for the next 65 generations.** No extinction, but no accumulation either. This wasn't evolution — it was **just "filtered random search"**: not only with the proxy, but **even with a real LLM, it still wasn't evolving.**
>
> From there, one all-nighter. To "decide a strategy," I ran 6 PoCs myself, dispatched 4 Claude Agents in parallel, and had Perplexity comb the literature. By morning, **everyone had independently converged on the same conclusion.** This is the honest disclosure of that "overnight decision log."

---

#### 0. The story in three lines (the "preamble" in rakugo terms)

In rakugo (Japanese comic storytelling) there's a "preamble" before the main story. First, three lines.

- **It saturated again** — Running the real LLM (llama3.2) for 12h, best=1.0 pinned at gen5, no progress for 65 generations. No extinction but no accumulation either = **filtered random search**. The root cause is the same as #25: "saturation of a fixed, hand-crafted ruler."
- **A strategy was decided overnight** — 6 self-run PoCs + 4 parallel Agents + Perplexity **independently converged on the same conclusion**: "Polishing the selector while keeping the ruler fixed is useless. **Make the evaluation itself open-ended.**"
- **The originality came into view** — Letting a continuously-evolving population perform an ensemble (MoA) at any instant — without stopping — to produce one answer, "**the live orchestra**," turned out to be a white-space in prior research.

In short: **"Once the lens (evaluation) saturates, no amount of polishing the selector (lldarwin) helps."** So we change what we polish — **we make the evaluation itself open-ended.** That's this round's conclusion.

---

#### 1. Why I did it "again" — continuing from #25 / #26 (design)

Recapping the series so far in three lines:

- **#24-05** "AI that learns as a population" — Rather than making one LLM smarter, we framed **derivative-population evolution**: N llive individuals (genomes) cycle through generations, evaluating each other.
- **#25** "Only Friston and I were left" — We seeded that population with 8 intellects as persona seeds and ran 500 proxy generations, producing a major failure: **perfect-score saturation → zero selection pressure → genetic drift (luck) alone biasing toward 2 lineages.** The lens was clouded.
- **#26 (design)** "Measuring with a lens alone doesn't make it evolve" — We designed the selector **lldarwin** and implemented "non-aggregating multi-objective selection (ε-lexicase / QD / neutral reservoir)." In proxy, it prevented lineage extinction.

Up to here, everything was about **proxy (deterministic heuristic, LLM-independent)**. A proxy can show "the mechanism turns," but it can't show "evolution found something **meaningful**" ([[feedback_benchmark_honest_disclosure]]).

So, the natural next move: **verify with a real LLM.**

Since localhost's ollama (llama3.2:latest) was reachable, I converted each individual's `c_prompt` (the prompt-strategy gene) into a system prompt, layered it over a fixed llama3.2, and had it solve real tasks — a **Promptbreeder-style mapping** — launching a 12-hour continuous evolution run. That's the starting point of this article.

> 🍵 **Break point**: If you've reached "the mechanism turned in proxy — so what about a real LLM?" you're good. The nice thing about research is you can actually run that "so what about the real thing?" And this time, the real thing was — merciless.

---

#### 2. The starting point — the "honest fail" of the real-LLM 12h run

Here's the result of the 12-hour real-LLM evolution run (on-prem llama3.2, strictly honoring measurement purity = never mixing in cloud LLMs, [[feedback_llive_measurement_purity]]).

| Fact | Value | Implication |
|---|---|---|
| Completed | 71 generations / 12h (≈10.3 min/gen, real LLM sequential) | Throughput is the bottleneck |
| best_score | **1.0 at gen5 → fixed through gen70** | **Objective saturation. 65 generations of no progress** |
| mean | Capped at 0.85; the 1.0 strategy doesn't take over | **Adaptation doesn't accumulate** |
| Per-axis | 6-7 of 10 questions saturated; gradient only in multistep (2 questions) | Effective resolution too small |
| fitness dependence | **c_prompt only**. c_factors (40-dim) / c_impl / c_meta drift neutrally | **43 dimensions have zero selection pressure** |
| Population health | pop=24 maintained, min ≥ 0.70, **no extinction** | The mechanism (GA) isn't broken |

This is where FullSense's honest disclosure rule makes you stop ([[feedback_benchmark_honest_disclosure]]). Write "No extinction! Reached best=1.0!" and it sounds like a success. But look at the breakdown and it's obvious.

**Verdict: not extinct, but not cumulative evolution either (≈ filtered random search).**

Of the 10-question test, only the 2 multistep questions retain a gradient (a difference). The other 8 were all maxed out early. In other words, for 8 of 10 questions it no longer matters who you pick. The effective resolution of selection pressure is down to roughly 2 questions' worth. And only 1 of the 4 chromosomes — `c_prompt` — participates in fitness; the remaining 43 dimensions (40-dim thought factors + impl + meta) are **neutral drift with zero selection pressure.**

![Fitness and diversity of the real on-prem LLM (llama3.2) evolution run (12h continuous). best pins to the ceiling early and stays flat thereafter](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_en.svg)

![Population-mean trajectories of the 5 weak axes (typo / polysemy / multistep / calibration / context) under real on-prem LLM evaluation. Everything except multistep saturates early, leaving no gradient](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_en.svg)

**Root cause = saturation of the hand-crafted fixed ruler.** The insight the user articulated in #25 — "**once the lens saturates, selection pressure is powerless**" — we've now **demonstrated with a real LLM**, not a proxy. Swapping the lens from proxy to real LLM doesn't help: **as long as the ruler is "the fixed 10 questions," it saturates at a perfect score quickly.** Change the lens manufacturer and, if the gradations are coarse, you get the same thing.

> 🤔 **Analogy**: Even if you swap the grader for a "real teacher" (real LLM), if the questions are the same every time, everyone scores full marks within a few rounds, and no difference shows afterward no matter how many tests you run. The questions aren't bad — **the question sheet is fixed and too easy.** Swapping the grader (lens) from proxy to real LLM still saturates if the ruler (questions) is fixed. This is the essence of the "honest fail."

> 🍵 **Break point**: Many people now think, "If even a real LLM saturates, isn't it game over?" I thought so too. But this is where the main story begins. If **"fixing the ruler was the mistake,"** then what we should fix is neither the selector nor the LLM, but **the very way we build the ruler.** I verified that over one all-nighter, with 6 PoCs, 4 Agents, and Perplexity.

---

#### 3. The overnight plan — distributed investigation to "decide a strategy"

The instruction from the user was this:

> "Organize the requirements thoroughly, and bring out more originality as an evolutionary system. Repeat PoCs many times. Keep running small-unit PoCs nonstop until morning to **decide a strategy.**"

The key here was that the goal was **not "complete the implementation" but "decide a strategy."** So rather than running one big production run, I took the approach of running **many small PoCs** to knock down design decisions one by one with real data ([[feedback_poc_feasibility_first]] = requirements → PoC → feasibility → detailed design).

The workers I ran in parallel were these ([[feedback_parallel_first_execution]] = independent tasks default to launching parallel Agents).

| # | Worker | Task |
|---|---|---|
| A | Claude Agent | Open-ended sweep PoC (demonstrate baseline = saturation/extinction vs. open-ended = avoidance, ≥10k generations) |
| B | Claude Agent | Observability (response logs / per-individual score time-series viewer / lineage reconstruction) |
| C | Claude Agent | Orchestra PoC (does MoA beat a single best? diversity vs. redundant selection) |
| P | Perplexity | SOTA survey of QD/novelty/MoA/agentic evolution (filling literature gaps) |
| X | Codex | Independent design critique + 3 minimal-PoC proposals + blind-spot flags |
| self | Me (main) | Directly implement and run self-PoCs #1–#6 (orchestrator + owner of the most important task) |

> 🍵 **Break point**: This "six-handed" setup is actually the hidden protagonist of this article. Why not do everything with one person (one context)? The answer is at the heart of honest disclosure. **A conclusion reached by the same mind is dragged by the same bias.** Verify **independently** with different methods (synthetic PoC / real LLM / literature survey), and only trust the conclusion when they agree. This is what I call **honest cross-validation.** Its power shows up in the second half.

Here, one honest dud to record. **Codex (X) was unusable.** A permitted-model mismatch on the ChatGPT account (the API rejected the entire codex model family) blocked it. It should have been within the 10x promo period, yet the API returned "not supported when using Codex with a ChatGPT account." Since this is an environment problem, for now I switched the main axis to self-PoCs + parallel Agents + Perplexity. **"A tool that should have worked but didn't" gets recorded too, not hidden.**

---

#### 4. The first decisive blow — should we discard the "fixed ruler"? (self-PoC #1 / #2)

The first hypothesis to knock down was the most fundamental question: **"If we change the ruler from fixed difficulty to adaptive difficulty, does saturation get fixed?"**

##### 4.1 Self-PoC #1 — adaptive difficulty fixes saturation. But it kills diversity

Using a proxy with synthetic competence vectors, I compared while removing confounds (selecting elites by score).

- **baseline (fixed difficulty)**: competence **stagnates low at 0.627** (best 0.757). The 12h pathology reproduced in proxy.
- **adaptive (difficulty follows the population's 60th percentile)**: competence **rises to 0.952** (best 1.0).

Letting difficulty track the population (raise difficulty as more problems become solvable) breaks the saturation and grows competence. **But** — adaptive **sacrifices diversity** (diversity collapses 0.310 → 0.134). In the process of optimizing for hard problems, the population coalesces onto one correct strategy.

##### 4.2 Self-PoC #2 — adaptive difficulty × novelty are compatible

So what happens if we add "novelty selection (maintain diversity)" on top of "adaptive difficulty (maintain gradient)"?

| Configuration | Final competence | best | Diversity | plateau |
|---|---|---|---|---|
| baseline (fixed difficulty) | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive (difficulty-tracking) | 0.952 | 1.000 | 0.134 (collapse) | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316 (maintained)** | gen99 (longest exploration) |

**Adaptive + novelty achieved both** competence (+40% vs. baseline) and diversity (2.4× adaptive, on par with baseline). It cedes 7% of competence in exchange for fully maintaining diversity.

Here, **the core of the strategy was confirmed with our own data.**

> **"Adaptive difficulty = gradient maintenance" and "QD/novelty = diversity maintenance" are complementary, and both are mandatory.**
> Neither the fixed ruler alone (baseline) nor adaptive difficulty alone (adaptive) is sufficient.

Honest caveat: this is an abstract proxy (competence vectors), not a real-LLM mapping. It is limited to **verifying mechanism feasibility (whether the mechanism turns).** The plateau@gen numbers indicate "the generation at which it stagnated," but the essence is the **level** of stagnation — baseline stagnates low (0.627), the adaptive family stagnates near the ceiling.

> 🤔 **Analogy**: When everyone scores full marks, you raise the difficulty (adaptive difficulty). Then scores spread out — but now everyone converges on the same way of solving (cookie-cutter). So you also add "reward unusual solutions too" (novelty), and competence and diversity coexist. **The two-sword style of "make it harder" and "reward the oddballs"** — that's the point of PoC #2.

---

#### 5. The core evidence — the 10k-generation open-ended sweep (Agent A)

The self-PoCs showed the "direction." Next, it was time to hit it **at scale, rigorously.** I had parallel Agent A run an open-ended sweep of **10k generations each × pop256 × 19 configurations × 2 rounds.**

The criterion was whether it was "open-ended" — **does it avoid saturation, avoid monoculture (convergence to a single culture), and keep its archive (diversity reservoir) growing?**

##### 5.1 The decisive verdict table

**verdict (at gen9999): all scalar configs = False / all novelty & lexicase configs = True**

| label | selection | std | MC | reservoir | archive | open-ended | occupied | monoculture | uniq_lineages |
|---|---|---|---|---|---|---|---|---|---|
| baseline_scalar | scalar | - | - | 0 | none | **False** | 9 | 0.74 | 1.0 |
| baseline_scalar_mc | scalar | - | ✓ | 0 | none | **False** | 9 | 0.90 | 1.0 |
| **scalar_qd** | scalar | - | - | 0 | map-elites | **False** | — | — | — |
| novelty_std | novelty | ✓ | - | 0 | none | True | 100 | 0.13 | 1.0 |
| novelty_std_qd | novelty | ✓ | - | 0 | map-elites | True | — | — | — |
| **novelty_std_res256** | novelty | ✓ | - | 256 | map-elites | True | 95 | 0.05 | **31.9** |
| novelty_std_res1024 | novelty | ✓ | - | 1024 | map-elites | True | 98 | 0.04 | 15.2 |
| **full_oe** | novelty | ✓ | ✓ | 1024 | map-elites | True | 90 | 0.05 | 15.3 |
| lexicase_std(_mc) | lexicase | ✓ | -/✓ | 0 | none | True | 111–122 | 0.03 | 1.0 |

Four decisive findings came out of this.

1. **Selection pressure is decisive.** scalar (single scalar fitness) is **extinct (False)** even with a MAP-Elites archive added (`scalar_qd`). So "add a reservoir and you protect diversity" is **wrong** — **unless the selection itself is open-ended (novelty / lexicase), open-endedness doesn't even hold.** An archive alone can't save it. **Making the selection pressure itself open-ended** was the essence.
2. **Standardization (z-score) widens QD coverage by an order of magnitude.** Adding per-dim z-score standardization to novelty takes occupied cells from 9 → 100+. Turning each axis's "deviation" into selection pressure widens behavior-space coverage by an order of magnitude.
3. **The neutral reservoir recovers lineage diversity.** With novelty_std alone, uniq_lineages is 1.0 (lineage fixed to one). Add reservoir256 and it goes to **31.9**. **Behavior diversity and lineage diversity are different axes**; the latter needs a reservoir (a re-confirmation of the knowledge already implemented in #26 design).
4. **Scale matters.** Raising the latent dimension 256 → 1024 takes niches 101 → 166 and archive 1021 (saturated) → 2234 (continued growth). Diversity can be bought with "capacity."

![Fitness and diversity of Stage1 baseline (no novelty). Diversity collapses near the end (the typical scalar failure)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_en.svg)

![Stage1 with novelty pressure. Behavior diversity is maintained until the end](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_en.svg)

![Overlay of baseline vs. +novelty diversity. Collapse (scalar) and maintenance (novelty) contrasted in one figure](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_en.svg)

##### 5.2 The "honest limits" Agent A surfaced

It's exactly when you get a good result (open-endedness holds) that you write the limits. Agent A itself pointed this out:

> novelty/lexicase preserves the diversity of the descriptor **as a whole**, but **does not guarantee the diversity of a specific semantic dimension (factor).**
> At large latents, factor drift occurs, and fspread (the spread of factors) needs monitoring.

In other words, even when "diverse as a whole," it may be "converged on the specific semantic dimension of thought factors." This gave rise to a new requirement, **factor-subspace QD (a QD that protects each semantic dimension individually)** (addressed in PoC #6 below).

> 🍵 **Break point**: This is the densest section of the article. The one line to take home: **"Adding an archive (reservoir) alone can't save it. Unless the selection pressure itself is open-ended, it fails."** Since #25/#26 design we've said "don't aggregate," but its core was that **"open-ending the way you select"** — and 10k generations of real data declared it. Past this point, it's all about originality.

---

#### 6. The core of originality — "let a continuously-evolving population perform an ensemble without stopping"

By now, the "selection core that structurally avoids saturation (S1)" was solidified. Next, it was time to back up — with PoCs and literature — the **three originality axes** the user laid out in dialogue.

The three axes the user articulated were these.

1. **Continuously-evolving population = live orchestra (ORCH)** — a continuously-evolving population performs MoA (Mixture-of-Agents) aggregation on the spot to produce one answer. Evolution never stops. **The biggest differentiation candidate.**
2. **Individuals with investigation capability (AGENT)** — individuals go investigate by themselves. Voyager-style.
3. **Observation / interactive control (OBS)** — view per-individual responses + selection-score time series, pause, and resume.

##### 6.1 The white-space Perplexity backed up

The Perplexity SOTA survey (1143 lines) running in parallel returned the most important backing.

> A "**continuously-operating system integrating online evolution + online answering**" has no clear prior research = a **research white-space.** The closest are MoA / Self-MoA / sequential aggregation / routing, but none is identical.

In other words, "stop evolution and answer with the strongest individual produced" is ordinary. "Without stopping evolution, have the evolving population itself perform an ensemble and answer" — nobody has done it yet. **The differentiation of ORCH §1.11 was confirmed.**

##### 6.2 But Perplexity also gave a counter-warning

As honest disclosure, I write the **counter-warning** Perplexity gave with equal weight.

> In 2025's **Self-MoA research**, **diversity is not automatically superior.** Iterating a single top model beat a heterogeneous-mix MoA by 6.6% on AlpacaEval (a quality-diversity trade-off).

"An ensemble of a population is stronger than a single individual" is **not self-evident.** Prior research warns that diversity can even be counterproductive. So ORCH is "prove it empirically, with an honest pass-bar." I verified this with Agent C and self-PoCs #3/#4.

> 🍵 **Break point**: This is the branch point where research integrity is tested. Right where you want to get carried away with "online evolution + online answering is white-space! originality!", Perplexity pours cold water with "but there's a counter-result that diversity isn't automatically good." **Receive both the elation material and the cold water within the same investigation.** Do this, and the conclusion gets much stronger. In the next section, I unravel the true nature of that cold water.

---

#### 7. Unraveling the "true nature" of the Self-MoA counter-result (self-PoC #3 → Agent C real LLM)

"Diversity is not automatically superior" — unraveling this counter-result at the **mechanism level**, not in proxy, is the climax here.

##### 7.1 Self-PoC #3 — voting, or routing?

First, it couldn't be verified in proxy (with saturated fitness the single best is already at full marks = zero headroom, so no difference shows). So I synthesized **"hard tasks a single individual can't ace"** (experts dispersed, single_best=0.5) and measured.

| Configuration | best_of (routing) | majority (vote) | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant (top-k) | 0.750 | 0.500 | 3/4 |
| MoA diverse (max-cover) | **1.000** | **0.000** | 4/4 |

Here a **decisive finding** emerged.

- Diverse MoA is **1.000 with best-of / routing** (double the single best). **ORCH holds.**
- **But with naive majority (a vote), diversity is counterproductive** (diverse = 0.000). On each sub-task, the one competent expert gets negated (canceled out) by the ignorant majority. Redundant MoA's majority (0.500) is higher.

In other words, **the true nature of the Self-MoA counter-result (diversity ≠ automatic superiority) was "whether the aggregator is voting or routing."** Voting/averaging kills diversity; competence-aware routing/gating leverages it. It's the difference between "an orchestra with a conductor" and "a crowd where everyone plays whatever they want."

##### 7.2 Agent C's real LLM independently produced the same conclusion

And then — parallel Agent C, with a **real LLM (llama3.2, 105 LLM calls, 15 tasks)**, produced the **same conclusion independently** of self-PoC #3.

- single best = **0.933**. MoA `best_of` + k≥5 reaches **1.000** (+0.067). **majority / weighted never exceeded 0.933.**
- diverse > redundant (diverse selection picks up complementary specialists in different QD cells earlier, with fewer k).
- The improvement is **entirely from one multistep question** ("double 5 and subtract 3"). The CoT-individual group all drops one question, and the heterogeneous individuals from diverse selection solved it.

> 🔑 **Independent cross-validation (the core of this article)**: Self-PoC #3 (synthetic, dispersed experts) and Agent C (real LLM, llama3.2) reached the **same conclusion via different methods** — "MoA beats the single best only with competence-aware routing (best_of) / voting doesn't get there / diversity has value only under routing." Two methods agreeing is extremely strong evidence in honest disclosure terms.

##### 7.3 The biggest hole — does a "real router" reach the oracle? (self-PoC #4)

Here Agent C pointed out the biggest hole. "best_of is **oracle routing** (the upper bound where God knows which individual is correct); in reality, the accuracy of the **gate that predicts** 'which individual is competent' is the bottleneck. Real voting (majority) doesn't reach the oracle."

I filled this with self-PoC #4 (real router vs. oracle, averaged over 20 seeds).

| κ (calibration) | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **The descriptor / specialty-router is robust at 0.90 with no calibration needed** (stably beating the single best 0.675, near the oracle). Moreover, **the routing key can reuse the behavior descriptor already computed for QD** — a synergy where **QD and ORCH share the same descriptor foundation.**
- **The confidence-router reaches the oracle at calibration κ≥0.6.** But small LLMs may be weakly calibrated → **make the descriptor-router the first choice** (calibration-independent).
- **majority = 0.338 is decisively unfit** (agreeing with PoC #3 and Agent C — a **third agreement**).

**Conclusion**: The hole Agent C pointed out — "real voting doesn't reach the oracle" — is **practically filled by descriptor-routing (reusing the QD descriptor).** ORCH holds end-to-end in proxy + (partial) real LLM.

> 🤔 **Analogy**: Gather 10 experts and have them vote, and the ignorant majority cancels out the correct experts. Route the math question to the mathematician — you need a **dispatcher (a conductor = routing).** And that conductor's score (behavior descriptor) can reuse what's **already been computed** to manage diversity. Voting (majority) kills the expert; the conductor (routing) leverages them. This is the point of PoC #4.

---

#### 8. Giving individuals the "power to investigate" (self-PoC #5)

The second of the three originality axes: **individuals with investigation capability (AGENT).** The idea is to let individuals do sandboxed read-only investigation in the search space. But "investigation isn't free" — when you charge a cost, does evolution learn to use investigation well?

Self-PoC #5 (vary cost λ and see how the investigation threshold θ evolves, averaged over 20 seeds).

| λ | θ* (=λc, optimal threshold) | θ_evolved (threshold evolution acquired) | evolved | always | never |
|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.049 | 21.46 | 21.47 | **11.70** |
| 0.3 | 0.30 | 0.476 | 21.34 | 21.26 | 21.20 |
| 0.6 | 0.60 | 0.659 | **21.24** | 21.06 | 21.21 |
| 0.9 | 0.90 | 0.888 | 21.21 | 20.85 | 21.21 |

- **Evolution acquired the selection threshold θ → λc on its own** (= selective investigation, "investigate only when you should," **emerged**).
- **The value of investigation capability is clear**: when λ=0 (investigation free), never (never investigate) = 11.70 = **a 45% loss.**
- **Cost λ degrades "always investigate" and forces selection.** AGENT-3 (the cost principle) holds.

Honest caveat: the margin at intermediate λ is small (a shallow reward landscape), and this too is an abstract proxy (real LLM × knowledge base is a separate matter). Still, the mechanism "with a cost, selective investigation emerges" was confirmed in proxy.

---

#### 9. Scale "qualitatively increases diversity" (Round 3)

Finally, I verified Agent A's "you can buy diversity with capacity" also via population size. With the `full_oe` configuration (novelty + std + MC + reservoir1024 + map-elites), I swept pop from 256 → 4096.

| pop | gens | occupied niches | monoculture | uniq_lineages | distinct_genomes | bspread_tail |
|---|---|---|---|---|---|---|
| 256 | 5000 | 171 | 0.047 | 14 | 256 | 0.939 |
| 1024 | 3500 | 467 | 0.019 | 74 | 1022 | 1.003 |
| 2048 | 2500 | 754 | 0.009 | 188 | 2041 | 1.071 |
| 4096 | 1200 | **1219** | **0.006** | **372** | 4054 | 1.253 |

With population-size scaling, open-endedness improved **monotonically** (niches 171 → 1219 / monoculture 0.047 → 0.006 / uniq_lineages 14 → 372 / behavior spread bspread also monotonically up). The POP-1 hypothesis (population size increases diversity) was supported in proxy.

**Honest (confound made explicit)**: there's an honest pitfall here. To raise pop, I shortened gens (5000 → 1200). This is **a confound in the direction unfavorable to niche accumulation.** Yet it still increased monotonically — i.e., **the POP effect is a robust lower bound** (it should actually be stronger). Conversely, "the possibility that it's stronger" couldn't be proven in this experiment. The claim is limited to proxy mechanism feasibility.

![Winner-individual thought-factor × memory-layer heatmap (Genome3D). Under real-pressure, c_factors drift neutrally, so treat this as a reference visualization of a cognitive profile](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_genome_heatmap_en.svg)

> 🍵 **Break point**: "Scale up and diversity increases" is intuitive, but the important thing here is the honesty that **"even when we added an unfavorable confound, it still increased monotonically."** Cutting gens is normally unfavorable to diversity. It increased anyway. So we can call it a "lower bound." Writing a good result as a "lower bound" rather than exaggerating it as an "upper bound" — this too is the manner of honest disclosure.

---

#### 10. By morning, everyone had arrived at the same conclusion — the finalized strategy

In one all-nighter, **6 self-PoCs + Agent A/B/C + Perplexity independently converged on the same conclusion.** This is the power of honest cross-validation. We discarded the fixed-ruler line and finalized the following as the core of lldarwin v2.

##### S1. The selection core (structurally avoid saturation)

- **Abolish fixed scalar quiz fitness** (baseline saturates at 10k generations + monoculture 0.9 + diversity collapse = large-scale reproduction of the 12h pathology, open-ended 0/6).
- **Selection = novelty / ε-lexicase (z-score standardization mandatory) + minimal-criterion.** **A MAP-Elites archive alone won't do** (scalar_qd also goes extinct) = make the selection pressure itself open-ended.
- **Quality is also needed, so QD (quality × diversity per cell)**: pure novelty sacrifices scalar quality (0.77-0.83) → pair with adaptive difficulty (conditional curriculum) to supply a quality gradient (PoC #2).
- **Lineage diversity is secured separately with a neutral reservoir** (behavior diversity ≠ lineage diversity; res256 takes uniq_lineages 1 → 32).
- **Add factor-subspace QD** (protect semantic-dimension diversity individually; addressing Agent A's factor-drift limit; PoC #6).

##### S2. How to produce results = continuous evolution × live orchestra (the core of originality)

- The deliverable is not a single best but **continuously evolving the QD archive and performing a MoA orchestra at any point in time to produce one answer** (ORCH; integrating online evolution + online answering is white-space = originality, confirmed by Perplexity).
- **Aggregation must be competence-aware routing/gating (a conductor), not voting** (self-PoCs #3/#4 + real-LLM Agent C agree threefold).
- **The routing key reuses QD's behavior descriptor** (the descriptor-router is calibration-independent and near-oracle at 0.90) = QD and ORCH share the same descriptor foundation (design economy).

##### S3. Individuals = agentic individuals with investigation capability (staged introduction, proxy-verified)

- In the search space, only sandboxed read-only investigation (real I/O after one-way promotion via the Approval Bus). Investigation incurs a cost.
- **Proxy-verified (PoC #5)**: cost λ makes "selective investigation" emerge. AGENT-3 (the cost principle) holds. Real LLM × knowledge base is the next stage.

##### S4. Observation / interactive control (implemented = standard in all runs, Agent B done)

- Response logs / per-individual score time-series viewer / lineage reconstruction (evolution-system 886 tests green). step/pause/resume to be wired in the next stage.
- Agent B's lineage reconstruction resolved the lineage display that was "**all ?**" in the 12h data, resolving the champion lineage gen70 → gen59 over 12 hops. Gaps are not fabricated but explicitly marked `lost@genN` (root cause = parent IDs couldn't be traced from either the snapshot or the winners alone). The observability foundation is the very bedrock of honest disclosure.

##### Self-PoC #6 — factor-subspace QD addresses Agent A's limit

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

Imposing a separate novelty for the semantic dimension (factor) roughly halves the loss of semantic-dimension diversity (50% loss → 32% loss). An effective measure for Agent A's factor-drift limit, demonstrated in proxy. Honest: not fully fixed but 68% retained = the remaining drift needs combining with the neutral reservoir or strengthening factor weights.

---

#### 11. Lessons (kept as honest disclosure)

- **Even a real LLM saturated.** Even swapping the lens from proxy to real LLM, with a fixed ruler it's full marks at gen5.
  "Use a real LLM and it'll evolve" was a **lie.** The problem was the way the ruler was built.
- **Adding an archive alone can't save it.** "Hold a diversity reservoir and diversity is protected" is wrong.
  scalar selection went extinct even with a QD archive added. **What saves it is open-ending the selection pressure itself.**
- **Diversity isn't automatically good.** The true nature of the Self-MoA counter-result is "voting or routing."
  Only with a conductor (competence-aware routing) does diversity become a value. Voting kills experts.
- **Independent cross-validation strengthens the conclusion.** Self-PoCs (synthetic), Agent C (real LLM), and Perplexity (literature)
  separately converged on the same conclusion — that's why you can trust it. A conclusion from the same mind shares the same bias.
- **Proxy is only mechanism feasibility.** This article's PoCs verify "whether the mechanism turns," not a claim of "general capability improvement of real LLMs." The moment you cross this line, the research becomes a lie.
- **Record the tool that didn't work (Codex), too.** Not just successes but duds, honestly.

In short — **"once the lens (evaluation) saturates, no amount of polishing the selector helps."** So we shift what we polish — not the selector, not the LLM, but **open-ending the evaluation itself.** That's the conclusion of the all-nighter.

> 🍵 **Break point**: In #25 I decided to "expose failure." In #26 design I built a "non-aggregating selector." And this time, a real LLM taught me "that's still not enough, because the ruler is fixed." **Failure breeds the next design, and the limits of that design breed the next.** This is the backbone of the series. The flashy "AI got smarter through evolution!" — I haven't written it even once. Because the evidence to write it isn't in place. When it is, that's when I'll write it.

---

#### 12. Conclusion

- The real-LLM 12h run was an "honest fail" — filtered random search that doesn't go extinct but doesn't accumulate. The root cause is saturation of the fixed ruler (demonstrating #25's insight with a real LLM).
- The overnight distributed investigation (6 self-PoCs + Agent A/B/C + Perplexity) independently converged on the same conclusion = **honest cross-validation.**
- Finalized strategy: **S1 an open-ended selection core** (novelty/lexicase + std + MC + QD + adaptive difficulty + neutral reservoir + factor-subspace QD) / **S2 continuous evolution × routing-MoA** (white-space originality, a conductor not voting) / **S3 agentic individuals + cost** (emergence of selective investigation) / **S4 observation** (implemented).
- All elements backed in proxy / (partial) real LLM. Remaining work: "wiring to the real-LLM stage," "factor-subspace QD implementation," "scale-up." The core strategy is finalized.

Build good parts, bundle them without aggregating, verify saturation with a real LLM, and rebuild toward open-ended selection. And only when 6 independent verifications arrive at the same conclusion can we finally say "the strategy is decided." This article is precisely the "**when the lens clouds, the selector is powerless too**" installment foretold in #25 — honestly exposing the moment the lens clouded with a real LLM (saturation), taking on Goodhart's law and the limits of proxy, then rebuilding toward open-endedness. Next is the [**#28 implementation phase**](drafts/QIITA_#28_lldarwin_v2_phase1_orchestra.md) that turns this finalized strategy into code.

---

#### 13. Related

- Series #24-05 "AI that learns as a population" — the framework of derivative-population evolution (the premise of this article)
- Series #24-08 "Building the lens" — lleval (the measuring side)
- Series #25 "Only Friston and I were left" — the honest disclosure of monoculture (the motivation of this article)
- Series #26 (design) "Measuring with a lens alone doesn't make it evolve" — the design of the selector lldarwin and the Stage1/1.5/2 measurements (the sister article)
- Pioneer paper (2026-05-27, date of record) "Continuously-Evolving Populations as Live Orchestrated Ensembles" — a defensive publication formalizing this article's strategy in academic form (FullSense public repository `docs/papers/`)
- Related memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

## 4. 進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28（lldarwin 実装編）

### An Ensemble Where a "Conductor" Makes an Ever-Evolving AI Population Play Together — llive's Orchestra-Style Evolution and the 3 Devices That Cured Saturation #28

> 📚 **Series guide (lldarwin arc)**: #24-05 population evolution → #25 the failure of monoculture → #26 design article → #27 the all-nighter decision (climax) → **#28 this article (implementation)**. ※ Each article can also be read on its own.

> **Concept hook**:
> Instead of asking one clever AI over and over, you **keep "evolving" a large crowd of slightly different AIs, and at the very moment an answer is needed, a conductor picks the right ones and makes them play together (an orchestra) to produce a single answer**.
> ——This is what llive is now aiming to become. `llive` is not "the LLM itself" but "a cognitive OS you wrap around an LLM". Within it, the evolution engine `lldarwin` we built this time is what **keeps the population alive, unbiased, and continuously growing**.
>
> In the previous article #27, we confirmed, over a 12-hour run with a real LLM, the disease that "once the evaluation (the yardstick) pins to a perfect score, evolution stops and degenerates into a mere sieve-fitted random search". And we decided on a policy: "No matter how much you polish the selector, it is futile. **Make the evaluation itself an open end**."
>
> This time we **implemented** that policy. And on top of a proxy (a synthetic yardstick), **the best score did not pin to a perfect mark — it kept rising all the way to the end**.

---

#### 0. The gist in three lines (the rakugo "opening")

- **The selling point is set** — llive's North Star is "**continuous evolution × live orchestra**". Without stopping the ever-evolving population, at any given moment it plays them together via competence-aware routing (the conductor) to produce one answer. This is a **white-space** in prior research.
- **We implemented the 3 things that cure saturation** — ① factor-subspace QD, which protects semantic dimensions individually; ② MAP-Elites, which stores outcomes not as a "single best" but in a diversity archive; ③ adaptive difficulty, which makes the yardstick follow the population. With these, we now have a foundation where "the players (diverse individuals) never run out".
- **Demonstrated saturation avoidance on a proxy** — running lldarwin-v2 for 10 generations, the best rose from 0.80 → **0.92 without pinning**. The diversity archive filled 21 cells. **However, this is a proxy and does not measure the capability of a real LLM** (honest).

In short, **not "one clever individual" but "a diverse crowd × a conductor"**. The implementation this time is the "device that keeps the players from running out" needed for that.

---

#### 1. What is llive (for first-time readers)

`llive` (pronounced "liv"; with two L's) is a **self-evolving, modular-memory LLM framework**. It is a member of the umbrella brand FullSense, with siblings `llmesh` (on-prem LLM hub) and `llove` (terminal dashboard). The three are independent OSS, but combined they form a single worldview.

llive's philosophy in one line: "**not the LLM itself, but a cognitive OS you wrap *around* an LLM**". You build a "scaffold for thinking" outside the LLM — 4-layer memory, a 6-stage loop, the Approval Bus, TRIZ, 10 thought factors, and so on — so that **even with the same LLM you can evolve its behavior**.

The protagonist this time, **`lldarwin`** (Darwin), is what carries that "evolution". The division of roles is as follows.

- **lleval (the eyeglasses)** = *measures* an individual (evaluation)
- **lldarwin (the selector)** = *converts* the measured difference into "who survives and who leaves offspring" (selection pressure)

And the North Star riding on top of both is the next "orchestra".

---

#### 2. The selling point = continuous evolution × live orchestra (the core of originality)

An ordinary Mixture-of-Agents (MoA) throws the same question at a **fixed** set of multiple models and aggregates the answers. What llive aims at is one step beyond that.

> **Keep the population evolving without stopping it (online evolution), and at the very moment an answer is needed (online answering), the conductor selects "for this question, these players" and makes them play together to produce one answer.**

As far as we investigated, this "integration of online evolution + online answering" was a **white-space with no clear prior research** (confirmed in #27 by having Perplexity dig through the literature). Close to it are MoA / Self-MoA / sequential aggregation / routing, but a form that "makes the ever-evolving population itself play together live" is nowhere to be found.

Here, the two honest findings obtained in #27 come into play.

1. **Aggregation must not be "voting" but a "conductor (competence-aware routing / gating)".** A self-PoC and real-LLM verification agreed in triplicate: on tasks with headroom, `best_of` / `routing` beat `single` (single-model iteration), but **`majority` (majority vote) is actually counterproductive**. This is also our own answer to 2025's "Self-MoA" (diversity is not automatically advantageous).
2. **The "behavior descriptor" of the diversity archive can be reused as the conductor's decision key.** That is, the QD (Quality-Diversity) described later and the conductor can **share the same descriptor foundation**.

——That said, the orchestra body itself (the conductor = the router implementation) is still ahead. **This time we implemented the step before that: the foundation that builds a "diverse, never-exhausting population of players good enough to play together".**

---

#### 3. Why do "the players run out" — the disease called saturation (a recap of #25–#27)

What an orchestra needs is "**a large crowd of players with distinct individuality, never running out**". Yet if you evolve naively, this collapses.

- #25: After running 500 generations, only "me and Friston" were left in the world (**monoculture**).
- #27: After running 12 hours with a real LLM (llama3.2), the best pinned to 1.0 at gen5 and made no progress for 65 generations. **It does not go extinct, but it does not accumulate either** = a sieve-fitted random search.

The root cause is the same in both. **Once the manually fixed yardstick (fitness function) pins to a perfect score, everyone ties, selection pressure vanishes, and after that the population drifts on its own via genetic drift.** Once the eyeglasses (lleval) saturate, no amount of polishing the selector (lldarwin) helps — that was the conclusion of #27.

So we change what we polish. Toward "moving the yardstick" and "structurally protecting diversity". Concretely, the following 3 things.

---

#### 4. The 3 devices we implemented (lldarwin v2 / Phase 1)

> The watchword of the design is "**do not invent a new algorithm**". Phase 1 is to **compose and wire** the parts already accumulated within llive (ε-lexicase / NoveltyScorer / MAP-Elites / the neutral reservoir) into the shape of the decided policy S1. They all turn on at once with `--selection lldarwin-v2`.

##### ③ Adaptive difficulty — make the yardstick follow the population

`AdaptivePercentileGate`. Each evaluation axis's "minimum line (minimal-criterion)" is re-placed every generation at a **specified percentile of the population's score distribution (e.g., the bottom-40% point)**. If the population improves, the minimum line automatically rises too. If you keep it on a `ratchet` (monotonically non-decreasing), the criterion does not loosen even on a temporary dip.

This puts a lid on the disease of "the fixed yardstick saturating at a perfect score" (in the PoC, fixed difficulty stagnated at capability 0.627 → with adaptive difficulty it rose to 0.952). Even in a turbulent generation where everyone falls below the minimum line, the selector ignores the gate to avoid total extinction (a fail-open guard).

In rakugo terms, it is **a teacher who raises the passing mark as the students improve**. It does not let them get a perfect score and call it a day.

##### ① factor-subspace QD — protect the individuality of semantic dimensions one by one

`FactorSubspaceNovelty`. Novelty search preserves "diversity as a whole population", but under a huge latent dimension, "**the diversity of meaningful dimensions (thought factors)**" quietly withers (factor drift).

So we measure novelty separately on **only the subspace** of thought factors and blend it with the overall novelty. In the PoC, this roughly halved the loss of semantic-dimension diversity (retention 49.5% → 68.1%).

> An honest improvement point: the original PoC "added the raw distances 0.5 each", but since the distance scale differs per subspace, in the implementation we fixed it to **z-score (standardize) each one before blending**. This is to mix "the whole chorus" and "the individuality of each part" fairly.

In player terms, it is a device that keeps **the second violin from being swallowed and disappearing into the first violin**.

##### ② MAP-Elites — store outcomes not as "a single champion" but as a "map of diversity"

`run_persona_evolution(map_elites=True)`. Every generation, all individuals are fed into the MAP-Elites archive. This is not "the single highest-scoring individual" but a map (QD archive) that **keeps the best individual in each cell, per coordinate of behavior**. Filling a new cell does not erase existing cells = **diversity does not structurally collapse, and the archive grows monotonically**.

This directly becomes the orchestra's **player catalog**. In the future the conductor will select "a player at the coordinate that fits this question" from this map and make them play together — the #27 design where QD and routing share the same descriptor takes effect here.

The implementation is **without extending the individual's format**: an additive wiring that derives the coordinate (descriptor) from the thought factors of the existing genome (so as not to break the 900+ backward-compatible tests of the foundation). The full-fledged design of the descriptor (e.g., reduction of high dimensions) is left as a task for a future Phase.

---

#### 5. Results — confirming "evolution that does not saturate" on a proxy

These are measurements from running `lldarwin-v2` (all 3 above + novelty + the neutral reservoir on) for 16 individuals × 10 generations on a proxy yardstick.

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21 (21 cells filled in the map of diversity)
```

- **The best did not pin to a perfect score; it kept rising all the way, 0.80 → 0.92.** We escaped, at the proxy stage, the pathology of "1.0 saturation at gen5 → frozen" seen in #27. This is a sign that adaptive difficulty made the "yardstick" follow the population.
- **21 cells filled in the diversity archive** = a catalog of "players with distinct individuality" to be played together began to form.
- The evolutionary automated tests, **879 + new tests, are all green**, with no regressions.

---

#### 6. Honest disclosure (please do not skip this)

The better the result, the more you doubt its breakdown — that is the FullSense way.

- **This is a proxy.** The individuals are not real LLMs but llive's genome (a proxy for thought factors). What we measured this time is the **mechanism feasibility** of "whether we can apply selection pressure to multiple independent weak axes simultaneously and maintain a specialist per axis", and is **not the LLM capability of production**. Real-LLM evaluation is the next Phase.
- **factor-subspace is not complete protection** (retention 68%, the rest drifts). It needs the joint use of the neutral reservoir and reinforcement of factor weights.
- **Honesty about backstage**: during this implementation, the auto-commit hook piled up 49 "pre-edit" snapshots on every edit, and the history got cluttered. In the end we squashed it into a single meaningful commit to tidy it up (on the public OSS side). Conversely, we also confirmed that the fork containing internal strategy stayed locally held as intended and was not exposed.

---

#### 7. What we will do from here

The evolution engine (the foundation that keeps the players from running out) took shape in Phase 1. Next is the orchestra body itself and the bridge from proxy to the real thing.

1. **Phase 2 = real-LLM wiring.** Against a real LLM on-prem (localhost ollama), verify adaptive difficulty, factor-subspace QD, and MAP-Elites with real evaluation. Does the "saturation avoidance" seen on the proxy also happen with real capability?
2. **Implementing the conductor (router).** With competence-aware routing reusing the QD archive's descriptor, actually run "make the evolving population play together live to produce one answer". How close can we get to the `best_of` oracle?
3. **Scaling up.** Population 256 → 4096, scaling up the latent dimension. Verifying the capacity hypothesis (the bigger, the more niches).
4. **Interactive continuous operation.** A driver's seat (CKPT-1) from which you can peek into a long run with step / pause / resume.

---

#### 8. A breather here (a rest point)

Up to here, has it come across "**what llive sells**"?

- Not one clever individual, but **an ever-evolving diverse population × the ensemble of a conductor**.
- For that, we built an evolution engine that **keeps the players from running out, protects individuality, and continuously grows them**.
- On the proxy, we could cure saturation. **Next is the real LLM and the orchestra body itself.**

In the upcoming "real-LLM article" and "orchestra article", we will show you whether the proxy's promise becomes real. ——Thank you for staying with us this far.

---

#### Series Navigation

- Series guide (lldarwin arc): #24-05 population evolution → #25 the failure of monoculture → #26 design article → #27 the all-nighter decision → **#28 this article (implementation)**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

## 5. 「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #29（Goodhart の法則と proxy fitness の限界）

> 📗 **In a hurry?** A plain-language digest of this article is available.
![A saturated lens makes selection powerless — Falsification #29](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q29_4koma_en.svg?v=2)
### "When the Lens Saturates, Selection Pressure Is Powerless" — Forging Evolutionary Design Through Falsification #29

> **Concept hook**: In #25 I exposed a failure, and in #26 I designed the selector "lldarwin". An ordinary
> series would say next: "It's fixed! All's well, the end!" **But not doing that is FullSense's honest
> disclosure.** This article is deliberately the installment where **I throw falsification at my own design**.
> The theme is a single phrase that bites in both evolutionary computation and machine learning——
> **Goodhart's law (when a metric becomes a target, it ceases to be a good metric)**.
>
> "If you make an LLM's weaknesses the fitness, evolution will overcome them on its own"——I myself go in
> to throw cold water on this naive optimism. And this time, **I put my own past "factual misconception" on
> the dissection table as a living specimen.**

---

#### 0. The story in three lines

- **When the lens (fitness) saturates, no matter how sophisticated a selection pressure (lldarwin) you add, selection is powerless** (the true lesson of #25).
- **When you measure LLM weaknesses with a proxy fitness, what evolves is not true ability but "surface strategies that hack the metric"** (Goodhart's law).
- Conclusion: I **restrict** lldarwin's value claim to **(a) proxy is mechanism feasibility only, (b) real LLM/VLM evaluation is the essence, (c) mapping diversity**. This is the honest boundary.

And this article has one more hidden protagonist, in one more line.

- **I myself once conflated "behavioral diversity", "lineage diversity", and "real LLM intelligence diversity".** I set that
  self-falsification at the core of this falsification installment. It is a live demonstration of what it means to doubt "it worked".

---

#### 1. A reminder of honest disclosure — doubt good results all the more

In #26 I wrote "in the PoC deployment, behavioral monoculture **improved to 0.05 (≪0.8) across all conditions**".
This is **fact**. It is not an exaggeration.

…But if I puffed out my chest here with "Got it, monoculture eradicated!" and ended, **I would break the vow I made in #25**.

> When an abnormally clean result appears, doubt the breakdown before feeling like you've won ([[feedback_benchmark_honest_disclosure]]).

The recurring bass line of series #25 was this——"**an abnormally clean result is not victory but an alarm**".
Against the criterion that dropping below 0.8 achieves OE-3, **0.05** is far too clean. The number 0.05 must be heard
not as a celebratory trumpet but as a **siren**.

So let's sound the siren. There is only one question to ask.

> **What 0.05 are we measuring?**

To say the answer first, 0.05 is "**behavioral monoculture in the proxy evaluation**".
This is the concentration of "the genome's behavioral surrogate", and it is
**not the diversity of the real LLM's intelligence**. Conflate this and you tread exactly the same rut as #25.

And I confess honestly. **I once conflated this.** Later, in §3, I will present the "caught-in-the-act" evidence.

> 🍵 **Break point (90 seconds)**: This article is, in short, "**an article in which I criticize myself**".
> I want this to be an installment where readers observe "behind the success report, what and to what extent the author doubts".
> It goes the **exact opposite** of the SNS-viral "I evolved an AI and the strongest ◯◯ was born!!". It won't be exciting.
> But the very honesty that isn't exciting will pay off half a year later——that is my bet. Have some tea.

---

#### 2. Falsification 1 — Against a saturated lens, no selection pressure works

##### 2.1 The true cause of #25, once more

The true cause of #25 was "**best_score saturated at 1.0 from the first generation → zero selection pressure → genetic drift**".
If everyone has a perfect score, it's the same whoever you pick. Selection becomes not "keep the superior ones" but "roll dice".
As a result, lineages that luckily grew were fixed by luck alone, and 8 lineages collapsed to 2 (furuse-kazufumi + friston).

Here I place the falsification that becomes the core of the evolution arc.

> **Inserting lldarwin (whether ε-lexicase, QD, or novelty) as-is into a saturated eval does not fix it.**

Why. Because every component of the selector takes "**that there is a difference**" as its fundamental premise.

- **ε-lexicase** presupposes "that there is a difference per axis". **If all axes are perfect, the difference is zero no matter how many axes you split into.**
  Even split into 100 axes, if all are 1.0, you just line up 100 "draws".
- **QD (MAP-Elites)** presupposes "that there is variance in the behavior descriptor". **If all individuals behave the same, there is 1 cell.**
  Even if you make a map, if everyone stands on the same square, the map becomes a single blank cell.
- **novelty** presupposes "distance from the past archive". **If everyone has converged to the same point, the distance is zero for everyone.**
  Even if you try to reward novelty, no one is novel.

So, diagrammed, it looks like this.

```
broken lens (fitness saturation) + sophisticated selector = still broken after all
```

##### 2.1.5 Empirical proof — in a memory task, "floor" and "ceiling" killed selection pressure (Step C, 2026-05-30)

This falsification was later **reproduced as real data** in the Step C experiment of llcore (CPU-only). Here is the result of having evolution (MAP-Elites) and naive search solve 2 standard memory tasks:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="Step C's two results (floor and ceiling)" width="640">

- **delayed_parity (XOR) = floor**: all methods at R²≈0 (the substrate is in principle unsolvable). No one can climb = no difference appears.
- **flip_flop (just memorize) = ceiling**: all methods at R²≈0.95 (too easy, everyone reaches it). **This is exactly the "saturated lens", and here too selection pressure is powerless.**

For reference, ③ (selection) works only when there is a "deceptive corridor" — a slope that misleads but can be crossed, going over a false summit:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/deceptive_corridor.svg" alt="Deceptive terrain and evolution (the state where ③ works)" width="640">

Step C's conclusion was, cleanly, **N/A (with this substrate we could not measure the presence or absence of ③)**. Moreover, at the draft stage I **over-wrote** "③ is unnecessary", and the multi-viewpoint adversarial verification caught it as "non-diagnostic due to the ceiling effect, insufficient power (δ=+0.33 is medium but p=0.15 is inconclusive)" and forced a downgrade——the "self-falsification" of §3.2 occurred here too, exactly as is.

##### 2.2 "#25 is fixed" is only half right

This is the falsification that tends to be overlooked from #25→#26. **#25 was not fixed "solely" thanks to lldarwin.**

In reality, **the fix on the lens side came first**.

- **per-dim z-score standardization (STD-1)** — equalize the variance per axis, so that "a featureless individual that is somewhat high on all axes" is not given an advantage.
- **central-agreement exclusion (SEL-1)** — an axis where everyone outputs the same value does not contribute to selection, so it is removed from the case.
- **low-dimensional reduction of the descriptor (DESC-1, JL projection)** — avoid QD's curse of dimensionality so that cells do not become empty.
- **exclusion of true-cause criteria** — remove `factor_score` (a single scalar of the max-archetype = argmax, an SEL-2 violation = the true cause of best=1.0 saturation) and
  `nearest_persona_idx` (a category index with no ordinal meaning) from ε-lexicase's case.

This "polishing the lens" work came **first**, and only then did the selector work.
Had the order been reversed, no matter how sophisticated an lldarwin you loaded, it would have been powerless before a saturated lens.

> **Making "select" sophisticated without fixing "measure" is futile.**

This is a lesson that bites not only in evolutionary computation but across machine-learning evaluation design in general.
When the leaderboard score saturates, before making the model more sophisticated, first doubt **whether the benchmark is broken**.

> 🤔 **An analogy (manzai-style)**:
> Straight man: "We increased the judges from 3 to 100, but when we showed all of them the same perfect-score answer sheet, the result was the same after all."
> Tsukkomi: "That's not about the judges, **the answer sheet (test) is broken**! What changes by showing 100 people the same perfect score!"
> Straight man: "Then if we make it 1000 judges…"
> Tsukkomi: "**You're increasing in the wrong direction**!! Fix the question paper first!!"

##### 2.3 Separation of duties — evolution breaks if either is missing

If we separate the duties of the lens (measure) and the selector (select), it looks like this.

| | Lens normal | Lens saturated |
|---|---|---|
| **Selector sophisticated (lldarwin)** | ◎ Evolution turns (achieved in #26) | ✗ Powerless (the trap of #25) |
| **Selector naive (Tournament)** | △ Turns but multipolarity is weak | ✗ Collapse (the starting point of #25) |

What to note is the bottom-right and top-right. **As long as the lens is saturated, the selector's sophistication cannot save the right column.**
The success or failure of evolution is decided, before "the cleverness of the selector", by "**whether the lens reflects the difference**".
This is the conclusion of falsification 1, and a more precise way of stating the "true lesson" of #25.

Let's see this consequence of "when the lens fogs, selection collapses too" in measurements. Below is the
transition of fitness and diversity for the baseline (no novelty, naive selection pressure). Toward the end, you can see diversity collapsing.

![baseline: diversity collapse toward the end](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_en.svg)

> 🍵 **Break point (90 seconds)**: "Polish the lens before selecting"——it was a plain story that order matters.
> Plain, but skip this and half a year melts away (I melted mine). From the next section is the heart of this article,
> **Goodhart's law**. From here it gets a bit darker. You might switch to coffee.

---

#### 3. Falsification 2 — Goodhart's law: evolution that hacks the proxy fitness

##### 3.1 The most serious risk

This is the one point the design document (LLDARWIN_DESIGN.md §7.1) explicitly states as the "**most serious risk**".

> **If you make an LLM's weaknesses the proxy fitness, what evolves is not true ability but "surface strategies that hack the metric".**

Evolutionary computation is a **genius at finding "shortcuts" that maximize a given metric**.
When a human hands over a proxy "intending to measure true ability with this", evolution, instead of acquiring true ability,
**always discovers surface strategies that satisfy only the proxy**. And it does so gleefully and efficiently.

What kind of gaming (metric hacking) can concretely occur? I expand the design document's accepted limitations as-is.

| pressure (LLM weakness) | possible gaming (metric hacking) | why it is not true ability |
|---|---|---|
| typo_robustness | just memorize and substitute specific typo patterns | powerless against unknown typos. Has not acquired noise robustness |
| polysemy_wsd | exploit heuristics of the test distribution | a statistical shortcut like "return the most frequent sense". Not meaning understanding |
| multistep_robustness | generate only persuasive reasoning "traces" | lines up plausible intermediate steps but does not actually reason |
| calibration | manipulate confidence toward the middle to lower ECE | saying "confidence 50%" for everything lowers calibration error. Not calibration ability |

The last calibration example is the easiest to grasp.
When you measure "can properly estimate confidence" with ECE (expected calibration error), evolution finds
the strategy of "**answer 'confidence exactly in the middle' to all questions**".
ECE drops dramatically. But that model has calibrated nothing. It has merely become a robot that spews out the middle.

> **When a metric becomes a target, it ceases to be a good metric (Goodhart's law).**

This is also a real example in LLM research. **Benchmark overfitting**, where only the score rises on a GSM8K-type benchmark but it does not
generalize, is exactly this structure. Those who trusted the leaderboard numbers too much have been tripped up again and again.

##### 3.2 My own "caught in the act" — self-falsification

Here I place the "conflation caught in the act" foreshadowed in §1 on the dissection table. I write it without hiding.

At first I had written this in the TODO——"verify **whether the Oka Kiyoshi / Grothendieck lineages survive the rerun**".
And seeing the clean number monoculture **0.05** in the PoC, I **momentarily started to mistakenly think**, "Oh, has lineage diversity improved too?"

This is the conflation. As I wrote in the source of record (lldarwin_stage1_results §3), the author comment in `poc_evolution_env.py`
(a comment I wrote myself) clearly denies that conflation.

> "monoculture = **BEHAVIORAL** concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is **behavioral spread**. lineage_fixation … to keep it <1 needs
> **QD niching on lineage / PERSONA-FX, not pure novelty**"

To organize, the 3 "diversities" I almost conflated were entirely different things.

1. **behavioral diversity** — the spread of behavior in the genome space. Measured by `diversity_l2`.
   **A metric on which novelty works.** What improved at 0.05 is this.
2. **lineage diversity** — which founders (Oka Kiyoshi, Grothendieck, etc.) survive. `founder_counts`.
   **Structurally does not improve with novelty.** Both novelty and lexicase can only "preserve existing individuals",
   and have no mechanism to revive a once-extinct lineage. So heading toward monoculture under neutral drift (Kimura) is
   **theoretically normal**. Not collapse, but within expectation.
3. **real LLM intelligence diversity** — whether real models truly have diverse cleverness.
   **Cannot be measured at all by the proxy.** A domain that Stage2's real LLM evaluation carries.

In other words, the true identity of "improved to 0.05" is **(1) behavioral diversity only**. Both (2) and (3) were unrelated to that number.
The reason I momentarily started to think "did lineage improve too?" is that **I saw (1) and jumped to the conclusion that (2)/(3) also got better**.

This is precisely the designer-side version of Goodhart's law.
Seeing a metric (behavioral diversity 0.05), the **human arbitrarily interprets** that another ability it does not measure (lineage survival, real intelligence) also got better.
Not only does the proxy diverge from true ability, **the interpretation of the human reading the proxy also diverges**.
Exposing this in the falsification installment hurts. But unless I expose it, it is not honest disclosure.

##### 3.3 Seeing "what 0.05 measured" by contrast

Words alone are hard to convey, so I **contrast "what was measured" with 2 SVGs**.

First, **behavioral diversity truly improved** (this is fact, no exaggeration). Below is the lineage-dominance stream with the neutral reservoir OFF.
Ultimately it **collapses to 2 lineages, furuse 71% / friston 29%**. Even with diverse behavior, the lineage is like this.

![reservoir OFF: collapse to 2 lineages](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_en.svg)

And below is **after putting in the lineage-side countermeasure (neutral reservoir ON)**. **All 8 lineages coexist**
(millidge / von-neumann / oka-kiyoshi / grothendieck … survive).

![reservoir ON: all 8 lineages coexist](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_en.svg)

The contrast of these 2 images is the heart of this article.
**Even with the same "0.05 behavioral diversity", on the left (OFF) the lineage collapses, and on the right (ON) the lineages coexist.**
In other words, the number 0.05 of behavioral diversity **said nothing at all about what happens to the lineage**.
Only by adding a different mechanism (lineage-niched QD / neutral reservoir) was the lineage saved.

"What 0.05 measured"——the answer is "**behavior only**". The lineage could not be seen without looking through a different lens. This is the honest answer.

##### 3.4 There are countermeasures, but the problem does not disappear

Goodhart countermeasures are woven into the design.

- The proxy is **restricted to mechanism-feasibility verification** and does not claim production ability.
- **Real LLM/VLM evaluation (Stage 2) is the essence.**
- Doubt apparent improvement with a **neutral shadow control (Bedau)** (compare against a shadow population of only neutral mutations,
  to confirm whether selection is truly working).
- **Down-sampling** perturbs the case every generation + an **OOD axis** offsets overfitting.

> 🍵 **Break point (90 seconds)**: "If there are countermeasures, isn't there no problem anymore?"——No, this is the crux.
> The countermeasures merely **delay the divergence**, and **the fact that the proxy is not true ability does not disappear**.
> It's the same as cold medicine suppressing symptoms but not eliminating the virus itself. So I will **never say** "the LLM got
> smarter via the proxy", come what may. Because the moment I say it, I can see myself eating crow half a year later. A cup of tea.

---

#### 4. Falsification 3 — Designer dependence: who decided "the direction of diversity"?

##### 4.1 A meta doubt

The case of ε-lexicase, the behavior descriptor of QD, the distance metric of novelty, the criterion value of minimal-criterion——
all of these have **"the direction of diversity" decided by the designer (me)**.

In other words, the diversity lldarwin produces is "diversity **within the axes the designer assumed**", and it is
not biological-evolution-grade **unanticipated emergence**.
As Taylor et al. (2016) point out as the limit of open-endedness,
"diverse within a scale defined by humans" and "leaping outside the definition" are entirely different stories.

For example, the moment I defined "behavioral diversity" with `diversity_l2` (L2 distance in the genome space),
evolution diversifies "**in the direction where L2 distance grows**". But that is diversity on the coordinate axis I drew, and
diversity on an axis I never even imagined (say, "sense of humor" or "use of silence") is
**not in the measurement target in the first place**, so even if it is born, I cannot notice it.

> 🤔 **An analogy (the goldfish pond)**:
> The owner of a goldfish-scooping stall decides "let's pick so that both red and black goldfish remain" and scoops.
> Indeed both red and black remain in the pond. Diversity, achieved. …But even if a **green goldfish** is born by mutation in that pond,
> the owner's net looks only at "red or black", so the green is **left unevaluated and missed in the scoop**.
> Emergence outside the axes the designer decided is out of view from the start. This is designer dependence.

##### 4.2 Acceptance — restrict the axes you can win on

So what to do. **Not claiming unanticipated emergence** is the honest answer.

lldarwin aims at a "**map of diversity without verifiability**" (differentiation axis DIFF-1), and it
does not claim strong / unbounded open-endedness (consistent with SCOPE).
Saying "I'm doing humanity-uncharted emergence!" is flashy, but it would be a lie.
**Restrict the axes you can win on**——narrow the value to mapping "diversity without verifiability" such as cognitive styles and cultural styles.
This is the range lldarwin can honestly claim.

The courage to discard flashy claims is also the core of honest disclosure.

---

#### 5. Falsification 4 — the trade-offs of minimal-criterion and QD themselves

Each component of the selector also has its own intrinsic weakness. I explain the accepted limitations of design document §7.1 one by one.

##### 5.1 minimal-criterion's stagnation ⇄ collapse

minimal-criterion (a minimum-standard gate) is a mechanism that "does not let individuals not meeting the standard reproduce", but
**the height of the standard is itself the trade-off**.

- **Standard low** → almost everyone passes → zero selection pressure → **stagnation** (the same structure as #25's saturation).
- **Standard high** → almost no one passes → **annihilation** (empirically confirmed. If everyone fails at the gate, the next generation cannot be made).

Lukewarm water or hell. **Countermeasure**: make the criterion not a fixed value but **adaptive by a population quantile** (e.g., drop the bottom 30%).
Further, put in a safety valve that ignores the gate if everyone fails (implemented in `MultiPressureSelector`).

##### 5.2 QD's curse of dimensionality + archive saturation

QD (MAP-Elites) cuts cells with the behavior descriptor, but **if the descriptor is high-dimensional, the majority of cells become empty**
(curse of dimensionality). Also, run for a long time and all cells fill up, capping novelty (**archive saturation**).
This is a phenomenon observed even in the artificial-life classics Avida / Tierra.

**Countermeasure**: **reduce the descriptor to low dimensions** (DESC-1, JL projection) + **monitor saturation with Bedau statistics**, and
record it honestly as "**saturation = failure**" (do not conveniently interpret saturation as "evidence that we've finished exploring").

##### 5.3 lexicase's scale limit

As the number of cases increases, ε-lexicase **increases in computational cost** and, moreover, **effectively turns into random selection due to noise**.
With too many cases, the winner is decided by the case that happens to come first in the order, and selection approaches dice.

**Countermeasure**: **down-sampled lexicase** (use only a subset of cases each generation) reduces cost + perturbs the environment.

##### 5.4 The trade-offs are "visible" in measurements

These trade-offs are not armchair theory; **they appear in measurements**.
A sweep varying the neutral reservoir's "reinjection frequency (reinject_interval)" is a prime example.

| interval | named lineage survival | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1** (every generation) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84 (max)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**A non-trivial finding**: behavioral diversity (diversity_l2) does not monotonically increase as you raise the interval; it **peaks at interval=5**.
10/20 actually decrease. The reason is——if you leave the lineages alone too much (raise the interval),
the diversity injection from the reservoir decreases, and few lineages fix and diversity stops growing too.
It is a nonlinear world in which the just-right "degree of leaving alone" is in the middle.

![reinjection-frequency sweep: diversity peaks at interval=5 (non-monotonic)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_en.svg)

The operational guideline becomes this——**if you prioritize lineage retention most, interval=1 (all 8/8 lineages survive)**,
**if you want to balance lineage retention and behavioral diversity, interval=5 (retain 5/8 while maximizing diversity)**.
The optimum depends on fitness / population size, so re-calibration is needed in production.
It is not "one single correct answer" but "an optimum that moves depending on the objective"——that is the honest conclusion.

##### 5.5 An honest reservation — "survival" may be "life support"

Here is one more reservation I should write honestly.
It is fact that the neutral reservoir kept all 8 lineages alive, but **we need to doubt the quality of that "survival"**.

As I wrote in the source of record (§4.1 / §4.2), the reservoir is a mechanism that "reinjects each lineage's best-ever genome (frozen elite)".
Strong lineages actually increase descendants and reproduce. On the other hand, the "survival" of weak lineages (1 individual each) is
**reinjection-derived, not active evolution**. So to speak, **not reproduction but a life-support apparatus**.

This is a legitimate behavior exactly per the neutral reservoir's definition (retain a representative, make recombination possible).
But I do not claim "all 8 lineages **continue to evolve actively**".
"Annihilation was prevented. But weak lineages are kept alive in the ICU"——this is the accurate expression.

> 🤔 **An analogy (rakugo-style)**:
> Landlord: "Not a single tenant of the row house is missing; all 8 are present, how auspicious, how auspicious."
> Hattsuan: "Yeah. Only, half of them are just breathing, not paying rent, lying in bed…"
> Landlord: "**That's less 'living there' than 'left there'!**"
> Hattsuan: "Well, better than kicking them out, I figured…"
> ——All are present, is fact. All are active, is a lie. This boundary is honest disclosure.

---

#### 6. Stage2 — the bridge from proxy to "real"

If it's all falsification, the design might look like it isn't moving forward.
But precisely because I solidified the footing with falsification, the next step gains meaning. That is **Stage2: real LLM evaluation**.

##### 6.1 The proxy axes (mechanism feasibility)

First, as the first half of Stage2, I plugged in the LLM's 5 weak axes as **proxies (deterministic heuristics, LLM-independent)**.

| pressure (LLM weakness) | related thought factors (case) |
|---|---|
| typo_robustness (noise robustness) | consistency / reality_link / uncertainty |
| polysemy_wsd (polysemy) | multiview / consistency / reality_link |
| multistep_robustness (multi-step reasoning) | structurize / closed_loop / self_extend |
| calibration (confidence estimation) | uncertainty / provenance |
| context_management (irrelevant-context robustness) | consistency / provenance / recompose |

A total of 14 cases are output to the breakdown, and lldarwin's ε-lexicase **selects specialists per axis without aggregating**.
Below is the population-mean transition of those proxy axes.

![Stage2 proxy axes transition (mechanism feasibility)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_en.svg)

However——as I have said repeatedly up to here——**this is a proxy**.
Since an individual is a genome, not a real LLM, this pressure is merely a **behavioral surrogate** of "how much the genome
equips the thought factors related to that weakness". **It does not measure production LLM ability** (mechanism feasibility only).
"PROXY" is burned into the SVG too. The Goodhart risk is, here, explicitly stated as an accepted limitation.

##### 6.2 Real on-prem LLM evaluation (the proxy→real bridge)

And the progress I can report for the first time in this article——**real LLM evaluation ran**.

Because localhost's ollama (llama3.2:latest) turned out to be reachable, in `real_pressures.py` I implemented the
**individual → real-LLM mapping** (Promptbreeder family). The mechanism is this.

- Convert an individual's `c_prompt` (PromptChromosome) into a **system prompt**
  (skill_set → instruction text / prompt_template_id → reasoning style / language_style → tone).
- Overlay that system prompt on a fixed LLM (llama3.2), have it solve **real tasks** on the 5 weak axes, and score.
- In other words, **fix the LLM body and evolve the prompt strategy (genome)**.
  **Select by measurement** for "which prompt strategy mitigates the LLM's weakness".

As a result, **a real selection signal was confirmed**.
A CoT + structure strategy (`chain_of_thought` + structurize + loop) **improved llama3.2's multistep from 0.0 → 1.0**
(a terse strategy failed at 0.0, score 0.80→1.00).
Not a proxy mirage, but **empirically demonstrated, with a real LLM, that "evolution of the prompt strategy mitigates the weakness"**.

![Stage2 real on-prem LLM axes transition (prompt-strategy evolution)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_en.svg)

**Looking side by side** at the proxy axes (above) and the real LLM axes (above), you can see with your eyes how "the shape measured by the proxy"
and "the shape measured empirically" differ. The proxy only shows that the mechanism turns. The real LLM shows how the prompt
strategy actually works against the model's weakness. **This difference between the 2 images is the real article of this article's claim.**

##### 6.3 But here too, honestly

It ran with a real LLM——but here too I sound the siren. There are 4 reservations.

- **(a) Only c_prompt participates in fitness** — persona / c_factors are neutral and not involved in fitness.
  The reservoir maintains the lineage, and novelty carries the initial selection. In other words, this is "**evolution of the prompt strategy**", not
  "evolution of the persona".
- **(b) All founders' initial c_prompt is identical (default)** — so exploration is mutation-driven.
  Diversifying the prompt per founder is a future improvement point.
- **(c) Small battery (2 questions per axis)** — a noisy estimate. "multistep from 0→1" also, because the number of questions is small,
  cannot be claimed to generalize from this alone.
- **(d) on-prem only (measurement purity)** — limited to localhost ollama, and
  **not a claim of general LLM ability** ([[feedback_llive_measurement_purity]]).

I also launched a 12h continuous run (`--fitness real-pressure --selection lldarwin --novelty
--lineage-reservoir --genome3d`). It safely stopped at 12h wallclock (snapshot taken → can continue with `--resume`).
But I do not say "it's real because I ran it for 12h". I ran it, is fact. I fully measured the essence, is a lie.
**The proxy→real bridge is built. But I have not finished crossing.**——this is the honest status of Stage2.

---

#### 7. Conclusion — how far may I claim (the boundary)

"If you make an LLM's weaknesses the proxy fitness, evolution can overcome them" was **optimistic**.
As a result of shaving it down with falsification, I **restrict** lldarwin's value claim to the following 3 points.

1. **(a) proxy is mechanism feasibility only** — verification that the plumbing of evolution turns. Does not claim production ability.
2. **(b) real LLM/VLM evaluation is the essence** — the selection pressure of intelligence is carried by the individual → real-model mapping (Stage 2).
   The bridge is built here. But crossing in earnest is from now.
3. **(c) mapping diversity** — restrict the axes you can win on to a "map of diversity without verifiability (cognitive, cultural styles)".
   Does not claim unanticipated emergence.

This is honest disclosure. **The failure (#25), my own conflation (§3.2), and the limitations (#5/§6.3) — I leave them all without erasing.**
This very article, in which I wrote not a single flashy victory declaration, is, I think, the most honest installment in the evolution arc.
The footing to step forward exists only on top of this boundary.

---

#### 8. Lessons (preserved permanently)

- **Doubt the breakdown of good results (0.05 improvement) all the more.** "proxy behavioral diversity" is neither "lineage diversity" nor "real LLM intelligence diversity".
  I, who saw a number and jumped to the conclusion that another ability also got better, was Goodhart's living specimen.
- **Making "select" sophisticated without fixing "measure" is futile.** Against a saturated lens, no selection pressure works.
  Polishing the lens comes first, loading the selector comes after.
- **Goodhart's law is the natural enemy of evolution.** The moment you make a metric a target, evolution hacks it.
  And even the interpretation of the human reading the metric diverges along with it.
- **As long as the designer decides the direction of diversity, do not claim unanticipated emergence.** Restricting the axes you can win on is honesty.
- **"Survival" may be "life support".** That all 8 lineages remained, is fact. That all are actively evolving, is a lie.
  Honest disclosure dwells in a single choice of verb.

> **Next-time preview**: Once I solidify the footing with falsification, next is the full-scale Stage 2 (real LLM/VLM evaluation, on-prem ollama).
> Not a proxy mirage, but can I truly make a real model's intelligence diversity a selection pressure?
> Can I raise "multistep 0→1" into a reproducible selection signal, not ending it as a coincidence of a small battery? From here is the real thing.

---

#### 9. Related
- Series #25 "Only I and Friston Remained" — the record of the failure (the starting point of this article)
- Series #26 "The Design of lldarwin" — the selector (the target this article falsifies)
- Implementation commits (llive): Stage1 = `8060204` / lineage-reservoir PoC = `0d0537d` /
  Stage1.5 (EvolutionLoop integration) = `b03cbda` / Stage2 (real LLM real-pressure) = `2fb2912`
- Measurement source of record: `../../research/lldarwin_stage1_results_2026_05_26.md` (§3 honest disclosure / §4.1–4.5)
- Design source of record: `../../vision/LLDARWIN_DESIGN.md` §7 / §7.1 (falsification investigation, accepted limitations)
- Related memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_implementation_status_record]]
- References: Goodhart's law / La Cava 2019 (ε-lexicase, arXiv 1905.13266) / Taylor et al. 2016 (limits of open-endedness) /
  Bedau (neutral shadow) / Kimura (the neutral theory of evolution)

---

## 6. 進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで、人工進化はどう可視化されてきたか

### The Lineage of "Showing" Evolution #30 — From Conway's Game of Life to 3DGS

> **Concept hook**: The "artificial evolution" I have been talking about endlessly in #25–#27 is, in fact, a research field with more than half a century of history. And here is the fascinating part: **research on evolution has always advanced hand in hand with "how to show it" (visualization)**. From the black-and-white blinking cells of 1970 to the continuous fluids and 3D Gaussians of 2024. Let us trace the lineage of "the technology for showing evolution" in one sweep, as a piece of general culture. At the end, we will locate **where FullSense's evolution visualization (a phylogenetic tree drawn on the thinking-factor graph) stands** within this lineage.

---

#### 0. Why Is "Visualization" the Lead Actor in Evolution Research?

Evolution is a phenomenon of **long timescales, large populations, and many generations**. A list of numbers makes it impossible to grasp "what actually happened." That is why the history of artificial evolution is, almost literally, **a history of inventing expressions that let you understand evolution at a glance**.

> 🍵 **Break point**: This article is a "stroll" with zero equations and almost zero code. Enjoy it with a coffee in hand. We will pick up only the "breakthroughs in how to show things" from each era.

---

#### 1. 1970: Conway's Game of Life — "Simple Rules Generate Patterns"

- **What**: A two-dimensional cellular automaton. Two states (alive/dead) × a simple rule over 8 neighboring cells.
- **The visualization invention**: **The blinking grid itself is the visualization**. "Moving patterns" such as gliders, blinkers, and glider guns were given names — one of the earliest examples of humans **naming emergent patterns with their own eyes**.
- **The limit**: This is not evolution (natural selection) but a deterministic unfolding. Yet the shock of "simple rules → complex appearance" opened up the field.

**Planned expansion of this section**: A deep dive into how the glider being recognized as a "moving structure" is a prime example of visualization giving birth to a concept.

---

#### 2. 1991: Tierra (Tom Ray) — "Code Becomes a Living Thing"

- **What**: An ecosystem of self-replicating machine-code programs running on a virtual CPU. Parasites, immunity, and optimization **emerged on their own**.
- **The visualization invention**: **Visualization of the memory map**. Each program's occupied memory region was painted in color, and the way parasites burrow into hosts was shown as a "map." It **depicted the "ecosystem of code" as a space**.
- **Significance**: The first observation, inside a computer, of "natural selection of self-replicators." One of the starting points of open-ended evolution research.

---

#### 3. 1994: Avida (Adami / Ofria) — "Measuring Evolution"

- **What**: A digital life platform that inherits the lineage of Tierra. Performing logic operations earns rewards (CPU time).
- **The visualization invention**: **Visualization of the phylogeny (phylogenetic tree) and the fitness landscape**. It drew, as a tree, "which descendants branched off from which ancestors," and made the stepwise evolution of complex traits (such as the EQU operation) **trackable**.
- **Significance**: It demonstrated that "complexity evolves through unavoidable steps" (Lenski et al. 2003, Nature). It **turned evolution from a story into an object of measurement**. FullSense's monoculture monitoring (max_lineage_share / archive growth) is a direct descendant of this "evolution that is measured."

> 🤔 **An analogy (manzai style)**:
> Boke: "Avida made it possible to measure evolution with numbers."
> Tsukkomi: "So it gave evolution a report card."
> Boke: "Exactly. When I said in #25 that 'the report card broke due to perfect-score inflation,' that was precisely an Avida-grade measurement story."

---

#### 4. 1994: Karl Sims "Evolved Virtual Creatures" — "Showing Evolution as Footage"

- **What**: Inside a 3D physics simulation, it **co-evolved** morphology (chains of blocks) and neural control, producing creatures that swim, walk, and fight over objects.
- **The visualization invention**: **3D animated footage**. The shock came from showing it as **video** rather than as figures in a paper. It put "the strange gaits that evolution designed, which no one had predicted" into a form that **humans could intuitively delight in**.
- **Significance**: Evolution visualization moved from "graphs for researchers" to "**footage that astonishes anyone who watches it**." It is the spiritual ancestor of FullSense's demo philosophy ([[project_f25_demo_polish]] "captivate through motion").

> 🍵 **Break point**: If, up to here, you can see that the way of showing things evolved from **abstract → concrete → dynamic** — "black-and-white dots → memory map → phylogenetic tree → 3D video" — then you are good. The second half is the modern era.

---

#### 5. 2019: Lenia (Bert Chan) — "Continuous Artificial Life"

- **What**: A generalization of the Game of Life to **continuous space, continuous time, and continuous state**. Many smoothly moving, "creature-like" patterns (such as orbium) were discovered.
- **The visualization invention**: **Smooth rendering of a continuous field**. From discrete blinking to a fluid expression that moves as supplely as a living cell. It opened up a new axis of appeal: "artificial life is **beautiful**."
- **Significance**: An example where the quality of the visualization itself raised the discovery power of the research. Precisely because it looks beautiful, humans can notice new patterns.

---

#### 6. 2020s: Visualization of Quality-Diversity — "Mapping Diversity"

- **What**: QD algorithms such as MAP-Elites / CMA-ME. Instead of a single best, they produce **a set of diverse, high-performing solutions**.
- **The visualization invention**: **A heatmap of the behavior space**. Two-axis behavior descriptors are laid out on a grid, and the elite of each cell is painted in color — this **visualizes diversity itself as a map**.
- **Significance**: FullSense / lldarwin's QD archive visualization stands directly on this. It can show at a glance, through **emptiness vs. filling of the map**, the principle that "as long as even one cell survives, you do not go extinct" (detailed in #26).

---

#### 7. 2020s onward: 3D Gaussian Splatting (3DGS) — "Representing the State of Evolution in Space" (FullSense's Bet)

- **What**: Originally a technique for novel-view synthesis (the lineage of NeRF). It represents a point cloud as 3D Gaussians and renders it fast and at high quality.
- **FullSense's idea**: An exploration of whether we can "show the state of evolution in three dimensions" by **mapping the high-dimensional genome / pressure profile of the evolving population into a 3D Gaussian space** (sharing the same root as the SH-coefficient linkage of [[project_precision_metrology_llm]]).
- **Positioning**: This is **still a research bet**, not an established technology (honest disclosure). It is an experiment placed at the "leading edge" of this article's lineage.

---

#### 8. Where Does FullSense's Evolution Visualization Stand?

| Era | Core of the showing | Inheritance in FullSense |
|---|---|---|
| Conway 1970 | Blinking cells = naming emergence | (conceptual ancestor) |
| Tierra 1991 | Memory map | mapping of lineage occupancy |
| Avida 1994 | Phylogenetic tree + measurement | monoculture monitoring / lineage tree |
| Karl Sims 1994 | 3D video | "captivate through motion" demo philosophy |
| Lenia 2019 | The beauty of a continuous field | animated SVG expression layer |
| QD 2020s | Behavior map | lldarwin QD archive visualization |
| 3DGS 2020s onward | 3D spatial representation | (research bet) |

FullSense's evolution visualization (**a phylogenetic tree on the thinking-factor graph + animated SVG**) stands in the position of **reproducing, in the terminal / browser, Avida's "phylogenetic tree that measures," Karl Sims's "captivate through motion," and QD's "map of diversity."** It is a modest but legitimate descendant of a half-century-long lineage.

> **Next time**: After tracing the lineage, next comes implementation. Using the actual evolution.svg as the subject, we will explain how FullSense's lineage-tree animated SVG took in which of the "ways of showing" above.

---

#### 9. Related

- Series #25–#27 — the "substance" of the evolution visualization in this article (monoculture / lldarwin / disproof)
- Related memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- References: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

## 7. AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制と検証規律

### Making an AI Use an AI as Its Subordinate #31 — The "Two Pillars" Development Model of Claude as Lead + Codex as Subordinate

> **Concept hook**: FullSense (llmesh / llive / llove) is a solo project built by me alone. But the reality is
> that it is not really "solo." A **two-tier development model — with one AI coding agent as the lead and another AI agent as its subordinate** —
> is what keeps things running. The lead is **Claude Code**, the subordinate is **Codex CLI**.
> "An AI hands work to another AI, and an AI verifies the result" — how do you keep this multi-layered
> delegation disciplined so it doesn't go off the rails? This article is a field report on running a "two pillars" setup of 1 human + 2 AIs.
>
> The keywords are **orchestrator / subordinate worker / verification discipline / parallelization**.

---

#### 0. The Story in Three Lines

- **Claude = orchestrator** (planning, implementation, delegation, **verification**) / **Codex = subordinate worker** (execution, review, investigation).
- "Two pillars" does NOT mean peers — it means **Claude leads, Codex follows**. Keep the chain of command singular.
- Iron rule: **Never adopt an external AI's findings without verifying each one, one at a time, against actual code / primary sources** (no taking things on faith).

---

#### 1. Why "Two Pillars" — The Motivation

In solo development, using just one AI agent is already commonplace. So why did I add a second one (Codex) **as a subordinate**?

1. **Vendor diversification & redundancy** — a hedge against a single agent's pricing changes / outages / quota exhaustion.
2. **Cross-review** — show the same design to an AI of a different lineage and get a second opinion (reducing blind spots).
3. **Parallel workers** — throw independent sub-tasks at the subordinate so the lead can concentrate on the most critical task.

> 🍵 **Break point**: "Using two AIs = twice as smart" is false. The key is to **keep the chain of command singular**.
> Turn it into a rabble and it actually gets slower. Half of this article is about "how to keep it under control."

---

#### 2. Division of Roles — Orchestrator and Subordinate Worker

![Hierarchy: Human → Claude Code (lead = orchestrator) → Claude sub-agents in parallel / Codex CLI as subordinate worker](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy_en.svg)

- **Claude's (the lead's) responsibilities**: task decomposition, dependency assessment, parallel launch of independent tasks, progress monitoring, **verification of results**, and batch commits.
- **Codex's (the subordinate's) responsibilities**: executing the delegated scope. Non-interactive delegation = `codex exec -s read-only "<prompt>"`.
- **The chain of command is always Claude.** Codex only influences the whole through Claude (it is never allowed to commit directly).

**Section to be fleshed out**: a usage table contrasting Claude sub-agent parallelism ([[feedback_parallel_first_execution]]) and Codex subordinate delegation.
"Same file = serial, independent files = parallel," "git operations are batched by the orchestrator" ([[feedback_agent_no_git_parallel]]).

---

#### 3. Verification Discipline — "No Taking Things on Faith" Is the Lifeline of the Model

The most dangerous thing in the two-pillar setup is **one AI adopting another AI's output without verification**. Errors get amplified. Hence the iron rule:

> Adopt an external AI's (Codex / Copilot / Gemini) findings only after **verifying each one, one at a time, against actual code / primary sources**.

A real example: in #26 of this series (the lldarwin design), I had the subordinate investigate existing code assets (e.g. that `mating.py:139 LexicaseSelection` was
"implemented but not wired up"), but **the wiring points and line numbers were confirmed by the lead (Claude) in the actual files** before
being written into the design document. "Codex said so" is not allowed to be the basis of a design.

> 🤔 **An analogy (in the style of a comic dialogue)**:
> Boss: "Hey, that function — is it wired up?"
> Underling: "Yessir, it ain't wired."
> Boss: "...I can't trust your 'yessir.' I'll go look at the source myself."
> — That is verification discipline. The underling's report is the **starting point**, not the **conclusion**.

**Section to be fleshed out**: the three stages of verification (receive a finding → confirm against actual code / primary sources → adopt or reject), and
the role of review wrappers (read-only reviews such as `tools/copilot_review.sh`).

---

#### 4. The Etiquette of Parallelization — Control That Prevents Runaway Behavior

Discipline for when you run multiple workers (Claude sub-agents + Codex) at the same time:

- **2–4 in parallel is the safe zone** (the lead has context headroom, no commit conflicts). At 5+, strictly manage file-level independence.
- **Extracting independent tasks** = no dependencies + no contact at the file / module / repo level. The same file is serial (like a file lock).
- **Irreversible operations (deletion / push / submodule changes) require human confirmation one at a time.** Never let the subordinate do them on its own.
- **git operations are batched by the orchestrator.** Don't let parallel workers touch git (to avoid conflicts).

> 🍵 **Break point**: The trap of "the more AIs you line up, the faster it goes." **The lead's context (its total amount of attention) is the rate-limiting factor.**
> Even with 5 running in parallel, it's meaningless if the lead can't process them. Just like the brain's working memory, there is an upper limit to how many things can be grasped at once.

---

#### 5. Anti-Patterns (Things You Must Not Do)

- Declaring "I'll proceed checking one at a time" and then silently executing serially (a lost opportunity for parallelization).
- Not delegating to the subordinate and doing everything within the lead's context alone (context explosion).
- The lead touching the same file before waiting for the results of workers launched in parallel (conflict).
- Delegating two workers to write the same file (a failure to judge independence).
- Adopting a subordinate AI's findings into the design or implementation without verification (error amplification = the biggest accident in the two-pillar model).

---

#### 6. What Actually Got Done With This Model (Real FullSense Examples)

- **Design cross-review**: had the subordinate review the evolutionary design / requirements / PoC, and the lead verified against actual code to decide on adoption.
- **Existing-asset investigation**: had the subordinate investigate the whereabouts of lldarwin's existing components (loop.py / mating.py / nsga2.py, etc.) → the lead confirmed.
- **Parallel sub-tasks**: parallelized article outlines, code investigation, and requirements organization as independent tasks (this very series is a product of that).

> 🍵 **Break point**: I'll also be honest at the end about my subjective sense of how "1 human + 2 AIs" changed solo-development productivity.
> Honest disclosure of **both** the aspects that got faster (parallelism, redundancy) and the load that increased (verification cost, control cost).

---

#### 7. Lessons

- **Keep the chain of command singular.** The two pillars are not peers but lead-and-follow. A split command center is the source of accidents.
- **Verification discipline is the lifeline of the model.** The chain of an AI believing another AI without verification is the greatest risk.
- **The degree of parallelism is rate-limited by the lead's context.** Decide by what you can process, not by headcount.
- **The human / orchestrator holds irreversible operations and git.** Entrust the subordinate only with reversible work.

> **Next time**: take the evolutionary design run with the two pillars (#26 lldarwin) and, using the subordinate Codex + an on-prem ollama,
> push it to Stage 2 (evaluation with a real LLM). How far does multi-layered AI delegation raise "the implementation speed of research"?

---

#### 8. Related
- Series #26 "The Design of lldarwin" — a real example run with this model.
- Related memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

## 8. llcore — Transformer のコアを CPU で進化させる: Verified Neural Architecture Evolution の最小 PoC battery

### (Series #32) llcore CPU PoC battery complete

#### TL;DR

- **CPU PoC battery complete** for `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, an independent llive track), a research framework that makes the **core computation of a Transformer (state update / learning rule / cognition-driven Δ)** the target of evolution
- Mechanism demonstrated with **5 PoCs / 39 falsifiable gates / 76 tests / Codex pair-review 5/5 green-light**
- **Gating structural mutations online with Z3** = embedding SMT into the selection pressure of evolutionary search — found to be unexplored prior art (prior survey across 14 RAD domains + confirmation by Agents A–D)
- Submission candidates: TMLR (primary) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

#### Why we built it

Freezing LLM weights is the norm, but the **core computation algorithm itself stays fixed by hand design**. Architecture/algorithm search such as AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge has advanced, yet:

1. **Infeasible compute for individuals** (TinyLlama 1.1B from scratch = $140k / 90 days / 16×A100)
2. **No safety guarantee during search** = wasting time generating numerically unstable architectures
3. **Verified search is disconnected from static verification (Reluplex/Marabou/α,β-CROWN)** — research on an SMT online gate inside the evolution loop was not found

#### Confirmed original axes (no negation work in the prior survey)

Mechanism-proven (4 axes):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **State update rule turned into a gene, RWKV-style** (Stage 0a v2)
3. **factor_hook (cognitive state → SSM Δ)** (Stage 2a mock)
4. **In-house evolver + verifier foundation** (Stage 0c + 1a)

Post phase: persona-indexed specialist / Marabou refinement / proposal of a new VNN-COMP category.

#### PoC ladder (5 stages / all 39 gates PASS)

| PoC | Content | Key numbers |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | in-house minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

#### What we learned from the v1 failure (honest disclosure)

PoC 0a v1 used `decay*s + mix*x*tanh(gate_str*s)`, which made **state=0 a fixed point — a zero attractor**: it passed G1–G5 formally but transmitted zero information. The design flaw that Claude overlooked on its own was caught by the **independent verdicts of Codex (gpt-5.4) and gem-critic**, leading to a v2 redesign in RWKV-style.

→ **In 4 of the 5 PoCs, Codex pair-review caught design flaws that Claude missed on its own.** A concrete case where mutual review worked to prevent structural breakdown.

#### Next options

a. Stage 3 kernel diversification (turn rwkv/mamba/hopfield/linear-attn into genes)  
b. Stage 4 turn learning rules (FF/EP/PCN/Hebb) into genes  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. Speed up the Z3 gate with PrediPrune+Quokka  
e. 3.5–5x wall-clock speedup with FlashEvolve  
f. Write it up as a paper (TMLR + GECCO 2027)

#### Honest caveats

- Mostly mock; connecting to real LLMs/weights waits for a GPU/new PC
- The 1-step scalar invariant is at the over-approx proof stage; multi-dimensional and multi-step are in the post phase
- The tanh upper-bound approximation is conservative (sound but not complete)

---

**Tags**: evolutionary computation / formal verification / Z3 / RWKV / state space model / CPU research  
**Related**: Series #14-31 (llive lldarwin v0.B-E + observation + governance + lleval)  
**Project**:  (PyPI llmesh-llcore 0.1.0a0)

---

## 9. llcore — 「進化で AI を設計するとき、選り分けて育てる工夫は本当に要るのか?」を 3 実験で詰めた話 (第三軸 ③ 決着 Step D)

### (Series #33) An Over-Tidy Result Is Not a Win, It's an Alarm — The Day We Settled Third Axis ③ with Proper Power

#### TL;DR

- The question is **"When you search for the core computation of an AI by evolution, is the 'sort-and-separate-and-raise' device (= the ③ survival-of-the-fittest / separation factor of evolution) really needed?"**
- **On synthetic "valley-laced (deceptive) terrain," ③ wins by a landslide** (Cliff δ=+1.0 in past experiments). ③ is genuine as a mechanism.
- **But when we re-measured the more-realistic CPU proxy terrain after physically driving the evaluation noise down to zero, it turned out to be "truly smooth (single-peaked)," and ③ was confirmed unnecessary.** For the first time we backed up the claim "the past negatives were not from underpower; the terrain really was smooth."
- Only the real-multitask neighborhood (C-gen4b) showed a faint hint of "③ NOT null," but when we added data it wobbled and stayed **a candidate at best** (within-run drift + fragile under multiple comparison).
- The suspicion that "some post-processing is hiding ③" (K4 ridge clip) — when removed, things got *worse* instead → **it isn't hiding anything; demoted to a diagnostic observation.**
- The external review (Codex) confirmed the conclusion **with no blockers.**
- The conclusion in one line: **"③ pays off only when the terrain is deceptive. The realistic-ish terrain we could measure on CPU just happened to be smooth."** Settling the main battle requires GPU (real-LLM terrain), but that is an investment decision.
- **Addendum (2026-06-02, §11.5): the last CPU escape route, kernel diversification (BG9), is structurally closed.** Kernel selection is low-dimensional, so a strong baseline (RR) samples it directly, and ③'s niching advantage cannot in principle appear. **For ③ to work, "high-dimensional" deceptive terrain is required**, and the only remaining route is GPU full-LLM (itself a bet).
- Meta-lesson: **honest disclosure is not decoration — it was a tool that pushed the research forward.** In BG9, the same discipline worked in the direction of "confirming a negative correctly as a negative."

> ⚠ Every number in this article is a real measurement tied to a local (on-disk) research commit `THIRD_AXIS_SETTLE_VERDICT.md`. llcore does not yet have a public repository, so I can't link out. Instead I write "how we measured" fully in the body.

---

#### 0. What This Article Is About (Concept)

`llcore` is a CPU-complete research framework that "turns the core computations of a Transformer (state-update rule, learning rule, cognitive-drive Δ) into genes and evolves them while verifying with Z3 that they don't break" (I wrote about the PoC battery in Series #32).

Its evolution engine has a design crux: how to make **③ (survival-of-the-fittest selection / separation)** — one of the four elements of evolution — effective. It's a "sort, separate, and raise" mechanism, like MAP-Elites, which keeps diversity and leaves elites in their niches.

The question is simple.

> **Do you really need that ③?**

If you do, the heavy investment to carry ③ (ultimately running a real LLM on GPU) is meaningful. If you don't, clinging to ③ is a waste of time and electricity.

Over this single day (2026-06-02), I went head-on to **settle that question with three experiments.** As the title says, the conclusion drags us back, once more, to FullSense's recurring bassline: "an over-tidy result is an alarm."

— That's 30 seconds. Warm-up done. On to the main subject. —

---

#### 1. An Analogy: Mountain Climbing and Deceptive Terrain

Before the equations, let's grasp the big picture with a terrain analogy (a metaphor I've used consistently in this research).

We represent the quality of a design by **the height of the terrain**. **A high place = a good design.** It's a game of finding the highest summit.

**Terrain 1: a smooth single mountain (easy)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

On terrain like this, naive "hill-climbing" — "just move toward something slightly better than now" — is enough to reach the summit. **You don't need the fancy device (③).**

**Terrain 2: deceptive terrain**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

Here, naive hill-climbing stops at the false peak. It hasn't the courage to descend into the valley.

This is where the ③ idea works. **You leave various types of climbers scattered around the valley** (= memory palace / MAP-Elites archive). Someone can cross the valley by "stepping stones" and reach the real summit — that's the mechanism.

**The heart of this research in one line**: ③ is truly useful **only on "deceptive terrain."** On a smooth single mountain, ③ is a white elephant.

So the question can be rephrased:

> **"When you design an AI by evolution, is the terrain you actually run into 'deceptive terrain,' or a 'smooth single mountain'?"**

Settle this, and whether ③ is needed is settled. Today, this is what we measured.

---

#### 2. The Leftover from the Past — Was "③ Unnecessary" Really "Unnecessary"?

Across the past experiments (Step C → Ladder rung 1 → E-A → valley-depth measurement), the picture was roughly this.

- **On the synthetic deceptive corridor, ③ wins by a landslide** (beats all three baselines, Cliff δ=+1.0). ③ is proven to exist, genuine as a mechanism.
- **On the more-realistic proxy terrain, ③ is negative** (MAP-Elites only ties random = the same symptom as a smooth terrain).

But two unresolved snags remained here.

1. **Is "③ unnecessary" really because "the terrain is smooth," or simply because "there weren't enough samples to detect the difference (underpower)"?** ── Mistaking these means committing the over-generalization "③ is powerless."
2. The direct measurement of valley depth ended last time as **N/A (not measurable)**. The evaluation noise was larger than the depth of the valley, so even if a valley existed it was buried out of sight — an instrument limit.

In other words, whether what "looked smooth" was a **property of the terrain** or a **limit of the instrument** had not been settled. Pinning this down is Step D.

— A short break. That was the premise. From here on are the three experiments done today. —

---

#### 3. Experiment Design — A Three-Part Set

| Experiment | What it measures | Aim |
|---|---|---|
| **EXP1** | proper-n re-test | Seriously increase sample size and pin down with statistical power whether ③'s effect is real |
| **EXP2** | deterministic C1 multimodality | Physically zero out the evaluation noise and judge noise-free whether the terrain is "deceptive" or a "smooth single mountain" |
| **EXP3** | verdict-flip of K4 ridge clip | Test the suspicion that "some post-processing is hiding ③" |

Discipline: everything isolated in `research/step_d_settle/`, src unmodified, git committed in one batch by the orchestrator. Each experiment passes the break gates (G1 CPU full-run / G2 reproducibility / G3 diagnostic validity / G4 src invariance).

---

#### 4. EXP2 Was the Decider — Zero the Evaluation Noise and the Terrain Becomes Visible

The order is shuffled, but **the one that mattered most was EXP2**, so I write it first.

The reason last time's valley-depth measurement came out N/A was simple: **"valley depth (about 0.05·|fitness|) ≪ the jitter of the evaluation noise."** The valley was buried in the instrument's noise, so you couldn't tell whether it existed.

EXP2's trick is this.

> The closed form of an ESN reservoir (fixed seed) + ridge readout (`np.linalg.solve`) **draws no randomness at all.** So the evaluation noise can be physically zeroed down to machine epsilon (about 1.11e-16).

In measurement we confirmed `eval_noise_std ≤ 1.11e-16`. This is not "the value jitters on every evaluation"; it's an error originating from the smallest unit of floating point (ULP), and is **essentially zero.** With the noise fog completely cleared, we can directly measure the valleys of the terrain.

Here is the result (valley_fraction = the fraction of valleys; the larger, the more multimodal = deceptive terrain):

| landscape | type | dim | valley_fraction (mean/max) | multimodal? | verdict |
|---|---|---|---|---|---|
| **ESN_3param** (real proxy) | real | 3 | **0.000 / 0.000** | **False** (3 seeds agree) | smooth=single-peaked → ③ unnecessary, confirmed noise-free |
| **ESN_perneuron40** (real proxy) | real | 40 | **0.096 / 0.121** | **False** (3 seeds agree) | smooth-leaning (below floor 0.2) → ③ unnecessary |
| ctrl_multipeak_dim3 (positive control) | control | 3 | 0.701 / 0.727 | True | the diagnostic can detect multimodality ✓ |
| ctrl_multipeak_dim40 (positive control) | control | 40 | 0.795 / 0.818 | True | diagnostic sound ✓ |
| ctrl_quadratic_dim3 (negative control) | control | 3 | 0.000 | False | the diagnostic can detect smoothness ✓ |
| ctrl_quadratic_dim40 (negative control) | control | 40 | 0.000 | False | diagnostic sound ✓ |

Three points:

1. **The real proxy terrain (both 3-dim and 40-dim) is valley≈0 = single-peaked.** Exactly matched across 3 seeds.
2. **The diagnostic itself is sound.** The deliberately built multimodal positive control is properly detected as multimodal (0.70/0.80), and the quadratic negative control is properly detected as smooth (0.0). So "the real proxy is single-peaked" is not an instrument bug but a property of the terrain.
3. With this, **"the past ③ negatives were not from underpower but because the terrain really was smooth"** was, for the first time, backed up noise-free on a real substrate.

I'll also honestly note a side discovery. **The deceptive corridor (`make_corridor_eval(d=0.16)`) that we intended to use as a positive control turned out to be valley=0.0 (single-peaked verdict) once made deterministic.** The corridor's deceptiveness is the type "confine within a single basin and escape via ③'s behavioral niching" (behavioral-reach deception), and was **not** the deception of terrain valleys (C1 multi-basin). We confirmed in measurement the narrowing of scope: the corridor does not serve as a positive control for C1. This means the past valley-depth calibration cannot transfer the "corridor-derived threshold" to terrain multimodality.

— A breather here. "The positive control didn't act as a control" was quietly a shock. But this too couldn't be known without measuring. —

---

#### 5. EXP1 — Only the Real-Multitask Neighborhood Shows a Faint Hint of "③ NOT null"

Next, we re-tested the band closest to the real problem (C-gen4b = MAP-Elites vs random, the real-multitask neighborhood), seriously increasing the sample size.

| case | original n=15 (audit) | fresh true re-run | verdict |
|---|---|---|---|
| **C-gen4b** | diff +0.063 / psd +0.20 / p 0.126 | **n=64: diff +0.0472, one-sided p 0.038, psd +0.188, gate PASS** | **③ load-bearing candidate (still_inconclusive)** |

Running with fresh seeds up to n=64, it **PASSED all four conditions of the strict gate.** That means the audit's reading of "③ unnecessary (inconclusive)" was, directionally, wrong, and **in C-gen4b ③ is in the NOT-null direction.**

…and not getting a winner's high here is the crux of this round. For three reasons, I kept it **a candidate at best.**

1. **Post-update power@n64 = 0.517 < 0.80.** The gate passed, but it doesn't reach the confirmation standard (power 0.80).
2. **Within-run drift (this is what mattered).** Following the trajectory of the cumulative p-value: first PASS at n=40 (p=0.042) → deeply significant at n=60 (p=0.010) → **back near the 0.05 boundary at n=64 (p=0.038).** Furthermore, splitting the seeds into first/second halves: **the first 32 seeds have diff=+0.0755 (frac_pos=0.625), but the second 32 seeds have diff=+0.0189, and the last 9 seeds have diff=−0.0376 (negative).** The PASS is propped up by the first-half seeds, and **the newer the data, the more it runs in the opposite direction.**
3. **Multiple comparison.** p=0.038 PASSES at α=0.05, but even with just EXP1's 3 cases it exceeds Bonferroni α=0.0167 (FAIL). Seen across the whole ③ research family it's harsher still.

In addition, the effect-size floor (psd) was bumping against a **structural ceiling.** C-gen4b's median psd doesn't budge from n=15→0.200 to n=255→0.200. `P(|psd|≥0.147)` (the fulfillment rate of the effect-size condition) plateaus at 0.794 even at n=255. Since it's a medium effect (psd≈0.20), no matter how much you increase the sample, the full gate's power won't exceed 0.80. **In other words, the very prospect that "increasing samples will confirm (A)" is thin on this proxy.**

Conclusion: **C-gen4b is "③ load-bearing candidate / still_inconclusive."** The headline "③ NOT null" leans too hard on a single boundary p=0.038. The within-run drift is real evidence that "the candidate may be a false positive."

---

#### 6. EXP3 — The Suspicion That "Post-Processing Is Hiding ③" — Removing It Made Things *Worse*

The last suspicion was this. "Could the post-processing called the ridge-readout clip (K4) actually be crushing ③'s signal?" If so, removing the clip should make ③ surface.

I tried removing it.

| task | clip | MAP-E mean | baselines beaten | verdict_flip |
|---|---|---|---|---|
| **addition** | True | +0.0100 | 1/3 | — |
| **addition** | False | **−1.212** | 0/3 (all worse) | **False** |
| **flip_flop** | True | +0.426 | 0/3 | — |
| **flip_flop** | False | +0.438 | 0/3 | **False** |

When the clip was removed, far from ③ surfacing, **MAP-Elites degraded from +0.010 → −1.212 on addition.** clip=False drops MAP-Elites into the noise region of raw R²<0 (15/15 seeds negative, R² in [−3.68, −0.20]), and instead of recovering structure it made things worse. **= an active refutation of the hypothesis "the clip is hiding the signal."**

The null-ridge FPR (gene-independent target = the true null hypothesis) also has zero difference between clip True/False (both 0.0).

Verdict: **K4 is not "the sole active suppression mechanism" but is demoted to "a diagnostic observation that crushes spread but doesn't change the verdict."** With this, the past statistical audit's assertion "K4 = the sole active suppression" was shown to be overstated.

Honest reservation (equivalent to §6.3): null-FPR=0/0 is a floor value from only null_seeds=4, and this experiment shrank the budget by about 7×. So I unified the verdict label not as "null confirmed" but as **"not_load_bearing_at_this_budget."** "At this budget, K4 is not load-bearing" is more accurate than "the null was confirmed." The substance of the verdict (demotion to a diagnostic observation) is unchanged; I'm only raising word precision.

— A deep breath here. Three experiments done. Next is a self-check of "did I overstate." —

---

#### 7. Surviving Refutation — Beating Up My Own Conclusion Through Three Lenses

The core of honest disclosure is "doubt your own conclusion most harshly," so I applied three independent refutation lenses. **All three survived as `refuted=true / medium`** — that is, the conservative verdict isn't overturned, but the positive-leaning emphasis works in the direction of being weakened.

1. **[power_adequacy] C-gen4b's gate PASS is fragile under optional-stopping + multiple comparison.** This is the §5 drift and Bonferroni FAIL above. Making "③ NOT null" a headline leans too hard on a boundary p. → recorded the p-vs-n trajectory and the sign reversal of the second-half seeds in the disclosure fields.
2. **[determinism_and_circularity] The single-peaked verdict is fragile near the threshold.** The determinism and non-circularity themselves are clean (the correlation between behavior and fitness is ≈0; the diagnostic doesn't use behavior descriptors but looks directly at terrain geometry). However, **90.9%** of ESN_3param's midpoints **dip downward**, and the maximum relative dip=0.0435 is just below the C1 valley threshold 0.05 (within 13%). So precisely speaking, it's not "**truly single-peaked**" but "a **weak multi-basin with shallow valleys (~2–4%) slightly below the C1 threshold.**" The direction of (B) null is maintained, but the robustness is limited because of threshold proximity.
3. **[clip_flip_validity] The K4 demotion is "at this budget" only because of the low budget.** verdict_flip=False is certain, but FPR 0/0 is a floor value and the budget is shrunk 7×. So rather than "firm refutation" we should state "not load-bearing at this budget."

None of the three is enough to "flip the conclusion," but all worked in the direction of "trimming overstatement." This self-audit is half of today's output.

---

#### 8. One Mistake of My Own, Written Honestly

In the previous valley-depth workflow, I passed **stale (old) values** into the second-stage orchestrator briefing. Values like "all below threshold / d*=0.1234." But the result JSON actually committed had `all_below_threshold=false`. When I read the previous workflow's result, I had mixed up the value of a different metric.

**Adversarial verification detected this and downgraded the verdict to N/A.** That is, the process of doubting my own "over-tidy conclusion" caught my own copy-paste mistake. It's not a pleasant story, but because that ran, in today's Step D I could re-measure from correct footing.

I was reminded that honest disclosure is not just "don't erase failures" but "**place a mechanism that detects failures in advance.**"

---

#### 9. How I Updated the Past Verdicts

| past verdict | past reading | Step D's update |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **direction updated: ③ is in the NOT-null direction (gate PASS at fresh n=64).** But a candidate at best |
| step6 exp7 (real ESN proxy, ③ negative) | n≤10 blind zone, "re-measurement required" | **major update: the terrain really is smooth (③ unnecessary), confirmed noise-free.** Re-measuring won't produce multimodality |
| valley depth N/A (not measurable) | instrument incapable | **resolved: made measurable via determinism** → vf≈0 (single-peaked). But a shallow valley near the threshold is a reservation |
| K4 clip = sole active suppression | "the clip conceals landscape structure" | **demoted: diagnostic observation** (not_load_bearing_at_this_budget) |

"Many of the past negatives that looked like '③ unnecessary' were not from underpower but because the terrain really was smooth" ── this one point being verified for the first time on a real substrate is the core of today.

---

#### 10. The External Review (Codex) Confirmed with No Blockers

As a discipline of llcore, each capstone passes a pair review by Codex (gpt-5.4, read-only). This time's overall comment was **"No blockers ── ③ conclusion externally confirmed."**

- The judgment to keep C-gen4b a candidate rather than load_bearing is valid (confirmed updated power 0.5174 < 0.80 in the JSON).
- EXP2's determinism and non-circularity are clean. It also confirmed the body's self-admission that "weak multi-basin below the threshold" is more precise than "truly single-peaked."
- EXP3's K4 demotion is valid at the current budget (FPR 0/0 + 7× shrink, so at-this-budget only).

The 4 items pointed out (CF1–CF4) are **all about harness robustness and wording precision for future reruns,** and do not overturn the current conclusion. When we re-test ③ on GPU, we'll apply these and then reuse the harness.

---

#### 11. We Were Trying a CPU Escape Route (Kernel Diversification / BG9)

"③'s main battle moves to GPU (the loss landscape of a real LLM)" is EXP2's recommendation. Since the real proxy is confirmed smooth, chasing ③ on smooth terrain won't yield (A) (if the terrain is a single mountain, there's naturally no gain from sorting and separating).

But since GPU is an investment decision, I was running in parallel **another hypothesis we can advance on CPU.** That is **kernel diversification.**

The hypothesis is this. Even if each individual kernel (rwkv / mamba / hopfield / linear_attn) is smooth, **uniting four kernel families could make fitness create a discontinuous step at the moment of kernel switching → the terrain could become multi-basin (deceptive terrain) → ③ could become load-bearing on CPU without GPU.** Verifying this was BG9.

At the time I first wrote this article, it was "right now measuring BG6 (whether the task → best-kernel mapping is non-constant, i.e., 'whether the favored kernel differs by task') in a smoke run." After that (within the same 2026-06-02), BG9 was settled. The next addendum section is its ending.

---

#### 11.5. Addendum (2026-06-02): BG9 Settled — The Escape Route Was Structurally Closed

> The conclusion in one line: **BG9 = N/A (structural). That is, the CPU escape route of kernel diversification is closed because "③ failing to stand is structurally determined."** It's not "③ is unnecessary" but "in this space, ③ cannot in principle be separated from the strong baseline" — an informative negative.

The result of the escape route set up in §11 came out. The expected "kernel union creates multi-basin (deceptive terrain) and ③ stands on CPU" **did not happen.** And not "it happened to not stand," but it turned out **it structurally cannot stand.** BG9 confirms this with three tiers of evidence.

##### (1) substrate validity — "discrimination exists but is weak" (PASS but caution)

First, when we re-designed the kernel-favoring task set from first principles and measured "whether the favored kernel differs by task" (BG6), the mapping was **non-constant = non-inert (PASS).** mamba / linear_attn / rwkv each became best on a different task. In the sense that we avoided the rut of "memory_tasks are kernel-neutral" stepped in at BG6, it's progress.

But honestly it is **weak**:

- **hopfield couldn't win on any task.** This is because the hopfield kernel is a **diagonal-scalar mock** and its tanh attractor was dysfunctional (per-seed R² was polarized at 0/0.99/0). So it's effectively not a "4-kernel union" but **3 kernels.**
- Clean specialization is only on 2 axes (selective_copy↔mamba / weighted_accum↔linear_attn). The rest have thin margins and are fragile.

→ **the existence of discrimination ≠ multimodality/barriers.** Non-inert-ification succeeded, but that doesn't guarantee deceptive terrain — only that far. Note that the limit of the diagonal mock is as declared in kernels.py's scope, and here we **claim only the feasibility of the mechanism** (full kernel performance is not claimed).

##### (2) harness validity — the positive control doesn't validate (this is the decider)

Next is the main battle. With fixed parameters (behavior=(kernel_id, theta L1)), we honestly paired-compared MAP-Elites (③) against three baselines ── **RR-hillclimb (random-restart hill-climbing)** / panmictic-GA / random.

| substrate | result |
|---|---|
| **positive control** (synthetic kernel-barrier) | ③ defeats panmictic (+0.423) and random (+0.208). **But it can't beat RR** (+0.051, p=0.31 → FAIL). Falls short of beating all 3 baselines = **harness validity doesn't stand** |
| **negative control** (kernel-neutral tasks) | all methods saturate at R²≈1.0, no ③ advantage = **correctly null** (no false positive, the instrument is sound) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3, panmictic conversely exceeds ③ = **③ doesn't win** |

This is the decisive difference from Step D (technical version §4-7). On Step D's deceptive corridor, ③ could exclude RR. **Why can't it in kernel space?** There's one root cause:

> **RR can directly sample kernel_id ∈ [0,4) on each restart.** Kernel selection is a single coordinate of 4 discretes (low-dimensional), so RR directly hits all 4 kernels on restart. To "find the best kernel," you don't need to cross a valley = **teleport (direct warp).** So ③'s behavioral niching gets no chance to play.

The reason ③ could exclude RR on Step4's corridor was that there the behavior was `mean(24-dim)`, and by the CLT the mean concentrates at 0.5 → the global peak is a measure-zero region = **a high dimension that random/RR cannot sample directly.** kernel_id, conversely, is low-dimensional and can be sampled directly.

##### (3) red-team — even adversarial verification couldn't refute it; rather, it confirmed

We hammered "is the harness's failure to stand really due to structure? could it be a chance setup mistake?" with an independent red-team. The result **failed to refute the structural claim and rather strengthened it**:

- **Mechanism confirmation**: instrumented RR scatters restart kid nearly uniformly across the 4 basins at [12,18,16,18] on the positive control, target reach 88%, best is restart→in-basin climb on 6/8 seeds. **Confirmed numerically** that "RR directly samples kernel_id on restart and bypasses the valley."
- **In all 4 faithful configurations (high-dim theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin), ③ can't beat RR (beats_rr=False).** Loosen the corridor and RR reaches equally; tighten it and ③ **starves first.**
- **Boundary sweep**: the tighter you make the theta corridor dimension D=0→3, the faster ③ starves relative to RR (D=3: ③ reach 0.08 vs RR 0.42). Same across 3 base_seeds.

→ Quantitatively confirmed that **"a behavior dimension where ③ passes by excluding only RR does not structurally exist in kernel space."**

##### Structural insight (the payoff of this settlement)

> **③ (MAP-Elites' behavioral niching) exceeds the strong baseline only when the "hard spot" is in a high-dimensional behavior space and unreachable by direct sampling (random restart).**

- **Kernel selection is low-dimensional (a single coordinate of 4 discretes)** → RR samples directly → ③'s niching advantage cannot in principle appear.
- Even if you move the deception into theta space, RR does greedy climb in-basin after restart, so if you tighten the corridor enough that RR can't pass, ③ also starves to the same degree. **The window of RR fail ∧ ③ succeed does not exist.**

This is the answer to the question left at Step4 §7, "if we expand the search space by kernel diversification, does ③ unlock?" The answer is **NO (structurally, on CPU).** For expansion to unlock ③, the added degree of freedom must produce a behavior that is **high-dimensional and hard to sample directly.** Kernel selection (low-dimensional, discrete) does not meet that condition.

##### Implication for GPU

- **The CPU-exhaustion gate is CLEAR**: BG9 structurally closed the last CPU route (kernel-union). ③'s remaining route is **only the high-dimensional GPU full-LLM loss landscape.**
- The structural insight makes the GPU bet **better-motivated.** ③ only becomes meaningful in high-dimensional behavior. A full-LLM's parameter space is millions of dimensions = exactly high-dimensional. So the GPU test follows a principle — not the weak bet "maybe full-LLM is the only exception," but "③ requires high dimension, and full-LLM is the high-dimensional regime."
- **But it's still a bet**: if the real-LLM terrain can be directly navigated by a strong backprop-family baseline, ③ is unnecessary ── this is a **risk isomorphic to BG9's RR** (the possibility that "a strong baseline solves it directly" remains even on GPU). So GPU is appropriate not "solely for ③" but as a **portfolio judgment** (riding along with llive's real-LLM fitness etc.) + **one pre-registration via a cloud rental** (before capital commitment). BG9's structural insight itself becomes the GPU's falsifiable go/no-go criterion: "if ③ is load-bearing on full-LLM, its hard spot should be in a high-dimensional behavior space and hard to reach by direct sampling/backprop."

##### Honest reservations (important)

- This is **not "③ turned out unnecessary."** "③ cannot in principle be separated from the strong baseline in this low-dimensional kernel space" = N/A (structural), and ③'s mechanism itself was already confirmed genuine at Step4. It's an **informative N/A** that, though N/A, carries the decisive information "the kernel route is closed."
- The harness/red-team are at smoke scale (5-12 seeds). At the proper test 15 seeds the numbers move, but **the structure (tighten and ③ starves first / RR directly samples kernel_id) is seed-independent and robust.** We will not run the full ≥15-seed proper test on real ── since the positive-control validity structurally doesn't stand, even if "③ unnecessary" came out on real, we couldn't separate "③ unnecessary vs detector-blind," and the red-team already confirmed that "detector-blind = the structure of kernel space," so even investing 7.5h of CPU wouldn't change the conclusion.
- The substrate is weak (effectively 3 kernels, **hopfield is a diagonal mock and dysfunctional**). With stronger kernel discrimination (full implementation, off-diagonal) there is **in theory** room for a different conclusion, but ③'s structural barrier (low-dimensional selection → RR direct sampling) is independent of the quality of the kernel implementation.
- The discipline of doubting "an over-tidy ③ success" was **not needed this time** ── ③ success never appeared in the first place (a negative just as the honest prior expected).

---

#### 12. Meta-Lesson — Honesty Was a Tool for Winning

Today's real output is not the numbers but **that the spirit of "doubting an over-tidy result" actually pushed the research forward.**

- Because we physically erased the evaluation noise (EXP2), we could separate whether "smooth" was a property of the terrain or a limit of the instrument.
- Because we applied 3 adversarial-verification lenses, we kept "③ NOT null" off the headline and held it as a "candidate."
- Because I self-detected my mix-up of a stale value, I could make the correct downgrade to N/A, and re-measure today.
- **In BG9 (addendum) I learned one more thing**: **a low-dimensional hard spot gets solved directly by the strong baseline. So for ③ (the sort-and-raise device) to work, a "high-dimensional behavior space" is required.** "Make deceptive terrain and ③ stands" is only half right; precisely, ③ won't stand unless the terrain is **deceptive in a way too high-dimensional to sample directly.** With a kernel 4-choice (low-dimensional), RR hits all of them on restart, so ③'s turn never came in principle. This is the basis for declaring the escape route not "given up" but "**structurally closed.**"

"When you get an abnormally good result, always doubt the breakdown before feeling like a winner" ── FullSense's research discipline (`feedback_benchmark_honest_disclosure`) was turning not as mere self-admonition but as **a mechanism that actually catches false positives and raises the precision of the research.** BG9 is an example where the same discipline worked in the reverse direction (**confirming a negative correctly as a negative**) ── trying in the red-team to refute my own "③ doesn't stand," I failed to refute it and it was confirmed as structure.

The conclusion, once more, precisely (reflecting the BG9 settlement):

> **On the proxy substrate, "③ is unnecessary because the terrain is truly smooth" was confirmed noise-free** (Step D). Only in the real-multitask neighborhood (C-gen4b) did a faint sign of "③ NOT null" appear, but with small effect + drift + multiple comparison it stays **a candidate at best.** The K4 clip is demoted from active suppression to a diagnostic observation. And the last CPU escape route, **kernel diversification (BG9), is structurally closed** ── kernel selection is low-dimensional, so a strong baseline (RR) samples it directly, and ③'s niching advantage cannot in principle appear. **The only route left for verifying ③'s main battle is the high-dimensional GPU full-LLM loss landscape** (itself a bet carrying the "strong baseline solves it directly" risk).

"③ settled = ③ turned out unnecessary" is wrong. Correctly, **"③ pays off only on 'high-dimensional' deceptive terrain. Neither the realistic-ish thing we could measure on CPU (smooth) nor kernel diversification (low-dimensional) met that condition."** The main battle (high-dimensional GPU) is still ahead, and it's a bet with no guarantee.

---

**Tags**: evolutionary computation / MAP-Elites / statistical testing / statistical power / honest disclosure / CPU research
**Related**: Series #32 (llcore CPU PoC battery) / #29 (refutation, Goodhart, proxy limits) / #31 (Codex two-pillar)
**Project**: llcore (PyPI reservation llmesh-llcore, local research since the repository is not yet public)

---

## 10. llcore — 「進化で AI を設計するとき、選り分けて育てる工夫 (③) は要るのか」を 6 段の実験 + 生物学で俯瞰した話 (第三軸 arc 全体)

### (Series #34) What Six Rounds of Hill-Climbing Taught Us About "When Does Evolution's ③ Actually Matter" — and How Evolutionary Biology Reached the Same Answer 100 Years Ago

#### TL;DR

- The question is **"When you search for an AI's core computation by evolution, do you really need the 'sort-and-rear-separately' trick (= evolution's ③: survival of the fittest / separation)?"** Series #33 wrote up the endgame (Step D + BG9); **this #34 surveys the whole arc (6 stages) as a single story**.
- **Stage 1 (synthetic deceptive landscape)**: ③ wins decisively (Cliff δ=+1.0). ③ is a real mechanism = **existence proof**.
- **Stage 2 (memory task / multi-reservoir)**: blocked by the substrate's "floor" and "ceiling," so ③ could not be measured = **N/A**.
- **Stage 3 (multi-task generalization)**: ③ beats "no selection," but cannot beat simple selection or random = ③ unnecessary (honest negative).
- **Stage 4 (measure a real proxy landscape noise-free)**: once we physically drove evaluation noise to zero, the landscape was **genuinely smooth (unimodal)** = ③-unnecessary confirmed. For the first time, "the past negatives were not lack of statistical power but a smooth landscape" was backed up.
- **Stage 5 (BG9: the loophole of mixing 4 component kinds)**: kernel selection is **low-dimensional**, so a strong baseline (random-restart hill-climbing) samples it directly, and ③'s niching advantage **structurally** does not appear = the loophole is closed.
- **Structural insight (the core of this arc)**: ③ only helps when the hard spot lies in a **high-dimensional behavior space** that cannot be sampled directly. The real CPU substrate is low-dimensional/smooth, so ③ is unnecessary.
- **Biological grounding (verified)**: this is exactly Wright's **shifting-balance theory**. For **the melanic moth (single gene = low-dimensional)**, ordinary selection suffices (= the BG9 kernel case); for **Lenski's Cit+ (high-dimensional, history-dependent)**, diversity matters (= the ③ regime). Our negative is **the computational version of the Coyne critique** (real landscapes are simple and ③ is only rarely decisive).
- **Meta-lesson**: "a result that went too well is not a victory but an alarm." Pre-registration, honest disclosure, adversarial verification, and deterministic noise-free measurement kept us from premature celebration.

> ⚠ Every number in this article is an actual measurement tied to local (on-machine) research records. llcore does not yet have a public repository, so I cannot link out. Instead I write "how it was measured" in the body. The papers cited in the biology part are only those whose existence, attribution, and claimed content I separately cross-checked against primary sources.

---

#### 0. What this article is about (the concept)

`llcore` is a CPU-complete research framework that "turns a Transformer's core computation (state-update rule, learning rule, cognitive-drive Δ) into a genome and evolves it while verifying with Z3 that it doesn't break."

Its evolution engine has a design crux: of the 4 elements of evolution (① mutation / ② heredity / ③ survival of the fittest / separation / ④ overproduction), how should **③ (selection / separation)** be made to take effect? It is the "sort and rear separately" mechanism — like MAP-Elites, which preserves diversity and keeps things in niches.

The question is simple.

> **Is that ③ really needed?**

If it is, then the heavy investment to carry ③ (ultimately running a real LLM on GPU) is meaningful. If it is not, then clinging to ③ is a waste of time and electricity.

Series #33 wrote up in detail the **endgame** of that question (the deterministic measurement of Step D + the structural resolution of BG9). But to get there, there were **6 stages of experiments**, repeatedly winning (existence proof), failing to measure (N/A), and losing (honest negative). This #34 re-lays out **the whole arc as a single story**. And as the highlight this time, we **ground** — with verified primary sources — the fact that **this computational result has a strikingly identical shape to a roughly 100-year-old debate in evolutionary biology (Wright vs. Fisher)**.

— That was 40 seconds. Warm-up done. On to the main topic. —

---

#### 1. Metaphor: hill-climbing, the deceptive landscape, and the memory palace

Before the equations, let's grasp the big picture with the 3 metaphors used consistently throughout this research.

We represent the quality of a design as **the height of a landscape**. **High place = good design**. It's a game of finding the highest peak.

**Landscape 1: a smooth single mountain (easy)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

In such a landscape, plain "hill-climbing" — that is, "just move toward something slightly better than now" — is enough to reach the top. **The fancy trick (③) is not needed.**

**Landscape 2: the deceptive landscape (deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

Here, plain hill-climbing stops at the false peak, because it lacks the courage to descend into the valley.

This is where ③'s idea works. **You keep all sorts of climbers scattered around the valley** (= the memory palace / MAP-Elites archive). Someone can cross the valley by "stepping-stones" and reach the real peak — that's the mechanism.

**The heart of this research in one line**: ③ is truly useful **only in the "deceptive landscape."** On a smooth single mountain, ③ is a white elephant.

So the question can be rephrased like this.

> **"When you design an AI by evolution, is the landscape you actually run into a 'deceptive landscape,' or a 'smooth single mountain'?"**

In #33 we settled this question with Step D + BG9. In this #34 we show **all 6 stages of hill-climbing** that led there. The interesting part is that at each stage, "was it a deceptive landscape / was it smooth / could it even be measured" changes.

— A short break. That's the prep. From here, the full record of the 6-round series. —

---

#### 2. The whole-arc map — surveying the 6 stages of hill-climbing at a glance

Let me put out the map first. This is the backbone of this article.

| Stage | Substrate (what landscape was measured) | Did ③ work? | One line |
|---|---|---|---|
| **I (Step 4)** | a synthesized "deceptive landscape" (deceptive corridor) | **Yes (decisive)** | Existence proof. ③ is real |
| **II (Step C / ladder 1)** | memory task / multi-reservoir parity | **N/A** | Couldn't measure due to floor, ceiling, the degree-5 wall |
| **III (E-A)** | multi-task generalization | **No** | ③ beats "no selection," but no more than that |
| **IV (Step D)** | real-proxy text landscape (deterministic measurement) | **No** | The landscape is confirmed **genuinely smooth** (noise-free) |
| **V (BG9)** | union of 4 component (kernel) kinds | **No** | **Structurally** closed (low-dimensional selection) |

The storyline is this. **First we prove existence — "③ is real and wins decisively under the right conditions" (I); next, to ask "well, what about real problems," we went to measure across 4 stages (II–V), and every single time it was "the real CPU substrate is a landscape that doesn't need ③."** Moreover, at the very end (IV, V), it was confirmed that the "reason it's not needed" is **the nature of the landscape, not lack of statistical power** — that is the whole-arc arc.

So, one stage at a time.

---

#### 3. Stage I (Step 4) — existence proof: in a deceptive landscape, ③ wins decisively

The first thing we did was an existence proof of "does a scene where ③ **works as the theory says** actually exist?" We **deliberately built a deceptive landscape** and pitted ③ (MAP-Elites) against 3 baselines — pure random / panmictic GA / **random-restart hill-climbing** — in a contest.

**The landscape's construction**: the genome is 24-dimensional. We define behavior (the climber's type) as `mean(genome)` = the average of the 24 values. To raise behavior, you have to **raise all 24 dimensions simultaneously**. The fitness is exactly a deceptive landscape: "a false peak (value 0.6) at behavior≈0.4 → a valley (value≈0) at behavior≈0.65 → the real peak (value 1.0) at behavior≈0.9."

**Results**:

| Method | Reach rate to the real peak | Comparison with ③ |
|---|---|---|
| **MAP-Elites (③)** | **about 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | same as above |
| random-restart hill-climbing | 0% | same as above |

Only ③ reached the real peak; all 3 baselines stopped at the false peak (≈0.60). **100% wins / the effect size is the theoretical maximum (δ=+1.0)**. Robust across 3 base seeds (60 seeds total).

Why this happens becomes foreshadowing for later.

- **random** always has behavior concentrated at ≈0.5 (the average of 24 values is locked at 0.5 by the central limit theorem). So it can **never reach** behavior 0.9 (0% even after drawing 6000 samples).
- **hill-climbing** climbs to the false peak 0.6 and refuses the one move of descending into the valley. Even on restart it returns to behavior≈0.5 and falls into the same trap.
- **③ (MAP-Elites)** keeps the valley cells as "new behavioral niches" and **crosses behavior 0.5 → 0.9 by stepping-stones**.

**We measured the boundary honestly too**. In a smooth corridor with the valley removed, ③ can no longer beat hill-climbing (p≈0.29). **③ is not omnipotent; it only works in a deceptive landscape.**

**Honest caveat**: this is a **deliberately built** synthetic landscape. It only proves that ③ is "possible," not that real tasks have this structure. Toy scale, low noise, and the baseline is a plain (1+1).

→ Here a hypothesis arises: **"If the real-problem landscape is this deceptive, ③ should come alive."** The next 4 stages are a journey to verify that on substrates closer to real problems.

— A pause. Stage I was a satisfying decisive win. From here, the weather turns... —

---

#### 4. Stage II (Step C / ladder 1) — blocked by the substrate's "floor" and "ceiling" (N/A)

Next we investigated "does a deceptive corridor **naturally arise in standard memory tasks**?" (Step C). We ran delayed parity / flip-flop / delayed recall with a single leaky reservoir + ridge readout.

The result was a clean **N/A (unmeasurable)**. The reasons are interesting because they're at two extremes.

- **delayed parity = floor**: a single reservoir cannot compute XOR (Minsky-Papert). All methods give R²≈0.003. No one can climb, so ③ cannot be separated.
- **flip_flop = ceiling**: all methods saturate at R²≈0.95. Variance is crushed and ③'s difference doesn't show (③ vs random has a positive sign but p=0.15 = underpowered, so it is **not a null**).

Here is one important finding. **The multimodality of the genome space was high** (valley fraction was 1.000 for parity), yet it was no use to ③. In other words, **"multimodal in genome space" ≠ "a deceptive landscape whose behavior must be crossed."** This distinction becomes the key for the second half of the arc.

**Ladder 1 (multi-reservoir)**: so, if we chain multiple reservoirs, does the floor rise? → We tried 5 mechanisms and all were `floor_lifted = false`. Depth (DeepESN) raises the floor statistically (effect +0.47/+0.60, PASS), but the absolute value stops at R² 0.05-0.10. The clincher is a positive control: a degree-2 readout solves 2-bit XOR exactly (R²=+1.0) but breaks down at degree≥3. **5-bit parity is degree-5 = a structural wall of this CPU reservoir+ridge paradigm.**

→ The parity path is structurally blocked. The real test of ③ needs to **come down off parity**.

**Honest caveat**: the degree-5 wall is "a wall of this setting," not a proof of impossibility for the whole paradigm.

— A short break. A "couldn't measure" result is plain, but in drawing the map it's an important blank zone. —

---

#### 5. Stage III (E-A) — multi-task generalization: ③ wasn't needed (honest negative)

Coming down off the parity floor, we measured ③ on **generalization**, with the cleanest ablation we could assemble.

**Setup**: single-layer leaky reservoir + ridge. Recall with variable delay. **Train on short delays {15, 30}, test on long delays {45, 60}** (extrapolation). The comparison is MAP-Elites (full ①②③) vs. **MAP-Elites with selection removed** (`randselect`: choose parents at random and place unconditionally = mutation only) + panmictic GA + random.

**Results (after peer review)**:

| Method | Test generalization R² (mean±std) |
|---|---|
| MAP-E (full ①②③) | 0.682 ± 0.115 |
| MAP-E randselect (selection removed) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| Gate | Comparison | diff | p (one-sided) | Verdict |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**How to read it**: ③ beats the **drift control with selection removed** (C-gen3 PASS = "some selection beats no selection"). But it **cannot beat panmictic GA (which has selection but no niching)** (it even loses slightly), nor random. In other words, **there is no niching-specific (= ③'s intrinsic) contribution**. This generalization landscape was **smooth** enough that simple selection or even random arrives at the same place. This is consistent with Stage I's boundary, "if it's smooth, ③ doesn't work."

**Honest caveat (important)**: this verdict is **limited to this setting** (budget 400, grid 6×6). Furthermore — and here is the crux of honest methodology — peer review (Codex) initially judged it "untrustworthy" and forced 3 rerun blockers (independent seeding per replicate / adopting the global best within budget / raising honest_n from 16→30). **Even after the fixes, the conclusion did not change.** The takeaway is that it was not a "fragile negative that flips when fixed."

— A pause. A loss is a loss, but the work of confirming we "lost correctly" took more time. —

---

#### 6. Stage IV (Step D) — the real-proxy landscape is confirmed "genuinely smooth" (noise-free)

This is the turning point of the arc. Through Stage III, "③ negative" kept happening, but a **nagging doubt** lingered the whole time.

> Is "③ unnecessary" really because **the landscape is smooth**? Or was it merely **lack of sample size, so the difference couldn't be detected (underpower)**?

Mistake this and you'd over-generalize to "③ is powerless." Step D settles it here.

**The trick**: an ESN reservoir (fixed seed) + a closed-form ridge readout (`np.linalg.solve`) **draws no random numbers at all**. So we can physically zero out evaluation noise down to **machine epsilon (about 1.11e-16)**. We measured `eval_noise_std ≤ 1.11e-16` — this comes from the smallest unit of floating point (ULP) and is **effectively zero**. With the fog of noise completely cleared, we can measure the landscape's valleys directly.

The landscape is next-character prediction of llcore's own source (about 24k characters). We measured valley_fraction (the fraction of valleys; ≥0.2 means multimodal = deceptive landscape).

| Landscape | Dims | valley_fraction (mean/max) | Multimodal? | Verdict |
|---|---|---|---|---|
| **ESN 3-param** (real proxy) | 3 | **0.000 / 0.000** | No (3 seeds agree) | Smooth → ③-unnecessary confirmed noise-free |
| **ESN per-neuron** (real proxy) | 40 | **0.096 / 0.121** | No (3 seeds agree) | Smooth-ish → ③ unnecessary |
| multimodal control (positive) | 3 / 40 | 0.70 / 0.80 | Yes | The diagnostic can detect multimodality ✓ |
| quadratic control (negative) | 3 / 40 | 0.000 | No | The diagnostic can detect smoothness ✓ |

There are 2 points.

1. **The real-proxy landscape (both 3-dim and 40-dim) is unimodal**. Agreement across 3 seeds.
2. **The diagnostic itself is sound**. A deliberately built multimodal landscape is properly detected as multimodal, and a quadratic is properly detected as smooth. So "the real proxy is unimodal" is not an instrument bug but **the nature of the landscape**.

→ For the first time, **"the past ③ negatives were not underpower; the landscape was genuinely smooth"** was backed up on a real substrate, noise-free. Re-measure and no multimodality appears.

**Honest caveat (important)**: "smooth" is precise only near the threshold. **90.9% of the midpoints of ESN 3-param dip slightly downward**, and the maximum relative dip (0.0435) is just below the valley threshold of 0.05. Strictly, it is not "**truly unimodal**" but a "**weak multi-basin with shallow valleys (~2-4%) just below the threshold**." The direction holds, but the robustness is limited because it's near the threshold — not rounding this off to "a perfect convex bowl" is this time's discipline.

— A deep breath. Here, "the real-thing-mimic is smooth" is confirmed. What remains is "the last CPU loophole." —

---

#### 7. Stage V (BG9) — the loophole of mixing components was structurally closed

Since the real proxy is confirmed smooth, chasing ③ in a smooth landscape yields no gain. But GPU is an investment decision, so we tried **a different hypothesis we could advance on CPU**. That is **kernel diversification (BG9)**.

**Hypothesis (pre-registered H7)**: even if each individual kernel (rwkv / mamba / hopfield / linear_attn) is smooth, **when you union the 4 kinds, the moment of kernel switching creates fitness steps → multi-basin (deceptive landscape) → ③ stands up on CPU without GPU**. The pre-registered honest prior leaned **toward null** (since all CPU substrates so far were smooth).

The result in 3 parts.

**(1) substrate validity — there is discrimination but it's weak (PASS but caution)**: when we measure whether the best kernel differs per task, the mapping is non-constant = non-inert (PASS). mamba is best on selective-copy, linear_attn on weighted-accumulation. However, **hopfield could not win on any task** (dysfunctional with the diagonal-scalar mock), so it is effectively a "**3-kernel** union." **The existence of discrimination ≠ a multimodal barrier.**

**(2) harness validity — the positive control does not validate (the clincher)**: on a synthetic kernel-barrier, compare ③ against 3 baselines.

| Substrate | Result |
|---|---|
| **positive control** | ③ crushes panmictic (+0.423) and random (+0.208). **But it cannot beat RR (random-restart hill-climbing)** (+0.051, p=0.31 → FAIL). It falls short of beating all 3 baselines = the harness doesn't stand |
| **negative control** | all methods saturate, no ③ advantage = correctly null (the instrument is sound) |
| **real** smoke | ③ beaten 0/3, panmictic actually exceeds ③ |

In Stage I's corridor, ③ could shut out RR; **why can't it in kernel space?** The root cause is one.

> **RR can sample kernel_id ∈ [0,4) directly at every restart.** Kernel selection is a single coordinate over 4 discrete values (**low-dimensional**), so RR hits all 4 kernels directly on restart. There's no need to cross a valley to "find the best kernel" = **direct warp**. So ③'s behavioral niching has no turn to play.

The reason ③ could shut out RR in Stage I is that there, behavior was `mean(24 dims)`, the average concentrates at 0.5 → the global peak is in a measure-zero region = **high-dimensional, not directly samplable**. kernel_id, conversely, is low-dimensional and can be sampled directly.

**(3) red-team — even adversarial verification couldn't refute it, and rather confirmed it**: on the positive control, instrumented RR spread restart kernels nearly uniformly across the 4 basins as [12,18,16,18], reaching target 88% of the time. In all 4 faithful configurations (high-dimensional theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin), ③ cannot beat RR. Tightening the corridor makes ③ **starve first** (D=3: ③ reach 0.08 vs RR 0.42). We quantitatively confirmed **"the behavior dimension along which RR alone is excluded and ③ gets through does not structurally exist in kernel space."**

**Verdict**: formally N/A (the positive control does not validate), but in substance a **decisive structural negative**. The harness is sound (it correctly nulls the negative control and detects GA/random), yet the substrate **cannot host ③'s deceptive landscape in the first place**. The answer to the question left from Stage I, "if we expand the search space with kernel diversification, does ③ unlock?", is **NO (structurally, on CPU)**.

**Honest caveat (important)**: this is **not "③ turned out to be unnecessary."** It is "③ cannot in principle be separated from a strong baseline in low-dimensional kernel space" = **an informative N/A**. ③'s mechanism itself is already confirmed real in Stage I. The substrate is weak (effectively 3 kernels; hopfield is a diagonal mock). A stronger kernel implementation could in theory yield a different conclusion, but **the structural barrier (low-dimensional selection → RR direct sampling) is independent of the quality of the kernel implementation**.

---

#### 8. Structural insight — uniting the 6 stages under a single condition

The existence proof (I) and the 4 negatives (II–V) all connect under just one condition.

> **③ (behavioral niching) exceeds a strong baseline only when the "hard spot" lies in a high-dimensional behavior space and cannot be reached by direct sampling (random restart).**

- **Why Stage I satisfies it**: behavior = `mean(24 dims)`. The average concentrates at 0.5 by the central limit theorem, and the global peak (mean≈0.9) is effectively measure-zero. Neither random nor restart **reaches it directly**. So ③, which leaves stepping-stones and ratchets, is essential.
- **Why the real CPU substrate doesn't satisfy it**: the hard spot is low-dimensional. The control coordinate of the ESN text proxy is effectively leak rate (a smooth low-dimensional knob; there's no valley to begin with). The hard spot of the kernel union is "which kernel" = a single discrete choice among 4. RR samples directly and teleports to all basins, so there's no valley to cross.

So Stage II's "multimodality of genome space 1.000" is not a sufficient condition — even if the genome is riddled with valleys, if the hard spot is concentrated in low-dimensional behavior coordinates, restart reaches it directly. **What matters is "the dimension of the behavior the search must reach," not the dimension of the genome.**

---

#### 9. Biological grounding — evolutionary biology gave the same answer 100 years ago

From here is the highlight of #34. **"Diversity-preserving selection works only under narrow conditions and is redundant otherwise"** — this boundary condition has a strangely clean precedent in 20th-century evolutionary biology.

> ⚠ **Honesty contract**: the following biology is a **"metaphor (structural analogy)," not a proof of our computational result**. The correspondence is structural and does not match at the mechanism level. Wherever the analogy slips, I note it on the spot. The papers cited are only those whose existence, attribution, and claimed content I separately cross-checked against primary sources.

##### 9.1 Wright's shifting-balance theory = the precedent of ③

Sewall Wright (1931/1932) reasoned as follows. If you stay as one big "single herd (panmictic population)," ordinary natural selection **gets trapped on the local peak right in front of you**. To go to a higher mountain you must once **lower mean fitness and cross the valley**, but deterministic selection refuses that.

Wright's solution was **to split the herd into many semi-isolated sub-populations (demes)**.

- **Phase I**: a small deme crosses the valley by chance, descending via **genetic drift**.
- **Phase II**: there, ordinary selection within the deme climbs a new (higher) peak.
- **Phase III**: the deme that landed on the high peak sends out many migrants, and the superior gene combination spreads through the whole species.

As a **whole** metapopulation, it crosses a valley that a single converged population cannot — this is the biological version of "crossing the valley of the deceptive landscape by stepping-stones."

**Correspondence to ③ / MAP-Elites (= metaphor, not attribution)**: each cell of the archive = a semi-isolated deme, local elitism within a cell = within-deme selection (Phase II), cross-cell mutation = interdeme diffusion (Phase III), and **the archive as a whole** (≒ metapopulation, not a single cell) crosses the valley.

> **Honesty notes (2 points)**:
> 1. **This is a commentator's framework, neither Wright's claim nor MAP-Elites's origin.** The original MAP-Elites paper (Mouret & Clune 2015) and the QD literature **do not cite Wright or "shifting balance."** I raise Wright as our **inspiration / metaphor**, not as the lineage of MAP-Elites.
> 2. **The mechanisms are only structurally similar, not identical.** MAP-Elites's valley crossing happens because a **mutation operator** places offspring in a new cell, **not genetic drift**. The archive is also not a population of replicating cells.

##### 9.2 Wright vs. Fisher = the dimension (the shape of the landscape) axis

Wright's contemporary Fisher (R. A. Fisher, 1930) argued the opposite: **a large panmictic population + mass selection on additive variance is enough** for adaptation to proceed; there's no need to bother splitting it.

The two's **deepest point of conflict was actually "epistasis (gene-gene interaction) and the shape of the landscape."** Wright assumed "because of non-additive interaction the landscape is **bumpy and multimodal**, so drift to cross valleys is needed," and Fisher judged "interactions exist but are unimportant, the landscape is roughly **unimodal and smoothly climbable**, so mass selection suffices."

**This epistasis/ruggedness axis is exactly the dimension in which our result lives. The shape of the landscape (topology) is the whole problem.** If the landscape is genuinely bumpy and high-dimensional (the Wright regime), diversity ferries you across valleys; if it's smooth or the hard spot is low-dimensional (the Fisher regime), mass selection — i.e., the biological version of strong random-restart hill-climbing — already suffices. Our ESN text proxy is noise-free and smooth, and the hard spot of the kernel union is low-dimensional discrete. **Both are the Fisher regime**, and ③ doesn't work and didn't work.

> Fine print (honestly): "Fisher ignored drift" is a compressed popular myth. Precisely, "he acknowledged drift exists but judged it quantitatively negligible in large populations." It's not a total denial.

##### 9.3 Our negative = the computational version of the Coyne critique

The most telling correspondence is not Wright's **proposal** but the biology community's **empirical verdict**. Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) evaluated shifting-balance theory both theoretically and empirically, and concluded as follows (full text cross-checked).

- **Mass selection is usually enough.** "There are almost no real examples better explained by Wright's three-phase mechanism than by simple mass selection." Artificial-selection experiments also failed to show that "selection in subdivided populations produces a greater response than mass selection in a large population."
- **Shifting balance works only under limited, rare conditions.** Empirical estimates of population structure suggest "**drift can move populations only between peaks separated by shallow valleys**" (deep valleys are only rarely crossed by drift), and moreover **most adaptation does not require valley crossing**.

This is a **strikingly precise biological version** of our result. Translated into our vocabulary, their words become: **if the landscape isn't genuinely deceptive/high-dimensional, ordinary mass selection (≒ strong random-restart hill-climbing) already solves it, and the diversity-maintaining apparatus buys almost nothing.** "Real valleys are usually shallow, most adaptation needs no valley crossing" is the biological statement of our "**real landscapes are usually simple, so niching is redundant**."

> **Honesty notes (3 points)**:
> 1. **They did not "refute" shifting balance.** They explicitly state Phase I/II can happen and cite 6 empirical cases. The claim is **narrower and probabilistic** ("hard to call it a general, important mechanism"), and writing "refuted" overstates it.
> 2. **The debate is not yet settled.** Wade & Goodnight (1998) and Peck et al. (1998, whose title literally argues "feasible") rebutted it, followed by Coyne et al.'s 2000 counter-rebuttal and Goodnight & Wade's rebuttal in the same issue. You must not cite the 1997 critique as the "final conclusion."
> 3. **Biology has a mechanism with no counterpart on the computational side, and it makes a claim even stronger than ours.** In Phase III, the gene-flow barrier that protects diversity can **trap a good solution in peripheral demes and impede its spread** = niching can be **counterproductive**. Our stateless discrete-selection setting has no counterpart to this cost, so we **don't overlay** it here. This is a spot where biology makes a stronger claim.

##### 9.4 Two real examples — the low-dimensional moth and the high-dimensional E. coli

Our claim has two poles (low-dimensional = ③ unnecessary / high-dimensional = ③ can work), and evolutionary biology has a clean real example for each.

**The low-dimensional pole — industrial melanism of the peppered moth (= the BG9 kernel case)**: in *Biston betularia*, carbonaria (black) vs. typica (white) are governed by **a single Mendelian locus, few alleles** (the causal variant is a transposable-element insertion into the cortex gene; van't Hof et al. 2011/2016) under **strong directional selection** (s ≈ 0.1-0.2; Saccheri et al. 2008; predation reconfirmed in Cook, Grant, Saccheri & Mallet 2012). The optimum is unimodal at each moment, merely shifting with the environment. **Simple directional selection — the biological version of greedy hill-climbing / random restart — directly fixes the fitter morph, and a diversity-maintenance mechanism is neither needed nor invoked.** This is exactly BG9: kernel selection is a low-dimensional single coordinate of 4 choices, RR samples all kernels directly, and ③ cannot structurally separate. **The melanic morph = the living-organism version of the BG9 kernel case.**

> Note (honestly): polymorphism is temporarily maintained during the transition, but that is due to **spatial environmental heterogeneity + gene flow (migration-selection balance)**, not an intrinsic diversity-preservation mechanism. A spot where the analogy slips slightly.

**The high-dimensional, history-dependent pole — Lenski's Cit+ (= the ③ regime)**: in the E. coli Long-Term Evolution Experiment (LTEE), aerobic citrate utilization (Cit+) evolved in **exactly 1 of 12 populations** around generation 31,500 (Blount, Borland & Lenski 2008). The key is a high-dimensional, history-dependent path of ordered **potentiation (accumulation of precursor mutations) → actualization (promoter capture via tandem duplication of citT) → refinement** (Blount et al. 2012). Replay experiments distinguished "historical contingency" from "a constant rate of rare mutation." This **genuinely exemplifies** the value of exploring contingency, epistasis, and a high-dimensional bumpy landscape — a real example of a regime where ③ can work.

> **Honesty notes (this corresponds only to the "antecedent" of our conditional)**:
> - **LTEE uses no niching algorithm.** It's plain natural selection, and the 12 parallel populations are **themselves a random-restart-like design**. So it's an existence proof that "contingency + diversity enables a rare innovation," **not** evidence that "niching beats a strong restart baseline."
> - "E. coli acquired the power to eat citrate from scratch" is a popular exaggeration. The innovation is **regulatory (aerobic expression of an existing transporter) = exaptation**, neither a new gene nor new biochemistry.
> - Van Hofwegen et al. (2016) showed "with direct selection Cit+ appears much faster" and challenged the "rare/contingent" framing (the Lenski side rebutted that it doesn't contradict the potentiation under LTEE conditions). If you lean on the "extremely rare / long-delay" narrative, you should also note this **contested follow-up**.

##### 9.5 Grounding summary

| Pole | Biology | Landscape | Does ③ work? | Our substrate |
|---|---|---|---|---|
| low-dim/smooth | melanic morph (single locus, s≈0.1-0.2, directional) | unimodal, shifting | **No** — mass selection suffices | BG9 kernel union; ESN/ridge text proxy (deterministic, smooth) |
| high-dim/contingent | Lenski Cit+ (potentiation→actualization→refinement) | bumpy, valley crossing by mutation | **Yes** (a regime where it can work) | synthetic deceptive corridor (behavior = average of 24 dims) |
| empirical verdict | Coyne, Barton & Turelli: mass selection usually suffices, shifting balance is only rarely decisive | real landscapes are usually simple | the **mirror** of our negative | every CPU substrate we tried |

**Conclusion**: Wright's shifting balance is the correct biological precedent for "**why** ③ works when it works," the Wright-Fisher epistasis/ruggedness axis is the correct framework for the "**dimension** condition," the melanic moth and Lenski Cit+ are clean low-/high-dimensional poles, and the Coyne critique is the biological precedent of our **negative**. **But these do not prove the computational result. They only ground it.** Where the analogy loosens most is that biology adds a cost (the gene-flow trap of Phase III) — our stateless setting has none.

— A pause. When I realized a 100-year-old debate had the same shape, honestly I got chills. But not mistaking "got chills" for "proof" is this time's discipline. —

---

#### 10. Implications for GPU — the only path left is high-dimensional, yet still a bet

The arc closed every CPU path. The real proxy is noise-free and smooth (IV), and the last candidate (kernel diversification) is structurally closed (V). The only path left for ③ is **a high-dimensional landscape** — and what provides that is **the parameter/loss space of a full LLM (millions of dimensions)**.

The structural insight makes the GPU bet **better-motivated**. It's not the blind bet "maybe only full-LLM is the exception," but a bet that follows the principle "**③ requires high dimensions, and full-LLM is the high-dimensional regime**."

**But still a bet.** For the same reason that biology's Cit+ does not prove "a victory of the ③ algorithm," and by the same form as not beating RR in BG9 — **if the real LLM landscape can be navigated directly by a strong baseline of backprop (gradient descent), ③ is again unnecessary**. The hard spot being high-dimensional is **a necessary, not a sufficient, condition**. You additionally need to show "a strong direct method cannot solve it" (RR on CPU, gradient descent on GPU).

So GPU is appropriate **not "for ③ alone"** but as a **portfolio judgment** (riding along with llive's real-LLM fitness, etc.) + **one pre-registration on rented cloud** (before capital commitment). The go/no-go criterion can also be written falsifiably:

> **Is the full-LLM hard spot high-dimensional in behavior, AND hard to reach by a strong direct baseline (gradient descent)?** If high-dimensional but the gradient reaches directly, ③ is unnecessary (= the GPU version of BG9's RR result).

---

#### 11. Meta-lesson — honesty was a tool for winning

The real achievement of this arc is not the numbers but **that the spirit of "doubting results that came out too neatly" actually pushed the research forward**.

- When we won at the **existence proof (I)**, we voluntarily confirmed "③ is not omnipotent" with a boundary experiment that removed the valley (not overrating the win).
- At **generalization (III)**, peer review thrust 3 rerun blockers at us, but even after fixing, the conclusion didn't change (confirmed it was not a fragile negative).
- At the **deterministic measurement (IV)**, because we physically erased evaluation noise, we could separate whether "smooth" was the nature of the landscape or the limit of the instrument.
- At **BG9 (V)**, in adversarial verification we **tried to refute and couldn't refute** our own "③ doesn't stand," and it was confirmed as structural (the same discipline worked in the direction of confirming a negative as correctly negative).

And across the whole arc we learned one thing — **a low-dimensional hard spot gets solved directly by a strong baseline. So for ③ (the sort-and-rear trick) to work, a "high-dimensional behavior space" is required.** "Build a deceptive landscape and ③ stands up" is only half right; precisely, ③ doesn't stand unless it's a deceptive landscape **so high-dimensional it can't be directly sampled**. And surprisingly, this boundary condition was one that **Wright's shifting balance and the Coyne critique had reached nearly 100 years ago**.

"When an abnormally good result comes out, always doubt the breakdown before you feel like you've won" — FullSense's research discipline (`honest disclosure`) was not mere self-admonition but a **mechanism that actually catches false positives, confirms negatives correctly, and raises the precision of the research**, turning across all 6 stages.

Let me state the conclusion precisely one more time, at the end.

> **③ comes alive only in a "high-dimensional" deceptive landscape.** It won decisively in the existence proof (synthetic corridor), but the real CPU substrate — the memory task (floor/ceiling), the multi-task generalization (smooth), the real-proxy text landscape (noise-free and smooth), the kernel diversification (low-dimensional, structurally closed) — none satisfied that condition. It is **not "③ resolved = ③ turned out unnecessary"** but "the real-thing-mimics we could measure on CPU now did not satisfy the condition (a high-dimensional deceptive landscape) under which ③ comes alive." The main keep (GPU high dimensions) is still ahead, and it's a bet that carries the risk that "a strong direct baseline solves it." And the skeleton of this conclusion had already been drawn by 20th-century evolutionary biology — except that biology does **not prove it, only grounds it**.

---

**Tags**: evolutionary computation / MAP-Elites / statistical testing / honest disclosure / evolutionary biology / CPU research
**Related**: Series #33 (third axis ③ resolution Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (refutation, Goodhart, proxy limits)
**Project**: llcore (PyPI reservation llmesh-llcore; local research as the repository is not yet public)

---

---

# 中文


## 1. AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin

:::note info
**📚 FullSense 知识库指南** <!-- fullsense-team-kb -->
FullSense 开发全史 60+ 篇文章（4 种语言版、故事化的阅读顺序指南、通俗易懂版、四格漫画）均已汇总至 Qiita Team **FullSense KB**（仅限团队成员）。
:::

### 把 AI 进化了 500 代之后，世界上只剩下"我"和"预测编码之父卡尔·弗里斯顿"两个人 #25 — monoculture 的 honest disclosure 与选择压组件 lldarwin

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

#### 0. 用三行讲剧情（落语里的"垫话"）

- **做了什么**: 把 8 位智慧作为 persona 种子投入 llive 的派生群体进化，用 rich-proxy 评价跑了 500 代。
- **发生了什么**: 第 1 代 best_score 就 **钉在了 1.0**，之后一直满分。8 个系统收敛为 **古瀬 52% / 弗里斯顿 48%** 这 2 个系统，其余 6 人灭绝。
- **真因**: "满分一直出现"＝**选择压为零**。无论选谁 fitness 都一样，所以进化实质上变成了掷骰子（遗传漂变）。

简而言之就是 **"想在一场所有人都考 100 分的测验里排名次"**。那谁能合格
当然就成了抽签。是测验不好。眼镜（lleval）起雾了。

---

#### 1. 为什么把"人物"作为种子来播

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

#### 2. 结果 — 只活下来 2 个人

500 代之后的系统占有率（max_lineage_share 的内訳）:

```
古瀬           ████████████████████████████  52%
弗里斯顿       ██████████████████████████    48%
米利奇         (灭绝)
矶村           (灭绝)
冈洁           (灭绝)
格罗滕迪克     (灭绝)
冯·诺依曼      (灭绝)
费曼           (灭绝)
```

乍一看，似乎可以写出一个"预测编码（Friston）和来历志向（古瀬）战胜了
抽象数学（格罗滕迪克）和形式计算（冯·诺依曼）"的**故事**。

实际上在 SNS 上，"把 AI 进化一下，结果预测编码最强"或许还会刷屏。
**但不做这件事，正是 FullSense 的 honest disclosure 规则**
（[[feedback_benchmark_honest_disclosure]]）。当出现异常漂亮的结果时，
在觉得自己赢了之前先怀疑内訳。

怀疑的结果，就是下一节。

---

#### 3. 真因 — "满分通胀"消灭了选择压

##### 3.1 症状: best_score 从第 1 代就是 1.0

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

##### 3.2 根本原因: 评价函数 `fitness_rich` 的双重坍塌

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

#### 4. 对策 — "测量"之后是"淘汰": lldarwin

llive 家族里已经有 **lleval（眼镜 = 评价框架, 连载 #24-08）**。
这次明白的是，**即便眼镜能"测出"差异，如果不把那个差异正确地
转换成"谁能存活"，进化就会坏掉**。

于是我设计了新成员 **lldarwin（选择压 = 淘汰组件）**。
ll- 家族的分工变成这样:

```
lleval   = 测量  （把个体的行为转换成多轴的 pressure profile）
lldarwin = 淘汰  （把那个 profile 转换成"下一代的亲代"）
```

##### 4.1 设计的核心 — "不聚合"的选择压

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

##### 4.2 把"LLM 的短板"当作选择压

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

##### 4.3 监控全灭 — SPC 报警

FullSense 的核心思想是 **SPC（统计过程控制）**。在 lldarwin 中也
每一代记录 `max_lineage_share` / archive 增长 / behavioral diversity，
**用 SPC_ALARM 检测 monoculture 比 > 0.8** 来自动调整 cadence 和参数。
目标是让这次的"8→2"在结构上不可能再发生。

---

#### 5. 教训（作为 honest disclosure 留下）

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

#### 5.5. "眼镜"与"淘汰器"的 2 段结构 — 为什么要分开（深入）

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

#### 5.6. 图解构想（投稿前 SVG 化的候选）

为了让本文"用动态来吸引人"想准备的图（投稿前 SVG 化）:

1. **系统占有率的崩塌动画** — 沿世代轴让 8 个系统的条带被吸入 2 个系统的 animated SVG（金鱼池隐喻）。
2. **best_score = 1.0 立即饱和图** — 在第 1 代就钉到天花板的平坦线（一眼看出选择压为零）。
3. **argmax 压垮图** — 多轴向量 `[典型性, 多样性, 专门性, ...]` 被 `max()` 压成 1 根柱子的 before/after。
4. **2 段结构图** — 把 §5.5 的"眼镜 → 淘汰器"作为 hero 图做成 animated。
5. **ll- 家族角色图** — 用 1 张图呈现 lleval（测量）/ lldarwin（淘汰）/ llive（个体）的关系。

> 这些计划搭载到 [[project_fullsense_animemd_branch_token_viz]] 的 animated SVG 表现层（声明式动画 → SMIL）上。

---

#### 6. 相关

- 连载 #24-05「群体学习的 AI」— 派生群体进化的总结（本文的前提）
- 连载 #24-08「制作眼镜」— lleval（测量侧）
- 连载 #26「lldarwin 的设计」— 淘汰器的多目标淘汰 / ε-lexicase / QD（本文的续篇）
- 连载 #27「眼镜起雾时淘汰也无力」— 反证调查・Goodhart's law（honest disclosure）
- 设计书: lldarwin（淘汰侧）— 本文的原始素材
- 相关 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 进度 badge / #24-05・#24-08・#26・#27 的 Qiita URL cross-link -->

---

## 2. 「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26（多目的淘汰 / ε-lexicase / 中立貯蔵庫 / 実 LLM 評価）

:::note info
**📚 FullSense 知识库指南** <!-- fullsense-team-kb -->
FullSense 开发全史 60+ 篇文章（4 种语言版、故事化的阅读顺序指南、通俗易懂版、四格漫画）均已汇总至 Qiita Team **FullSense KB**（仅限团队成员）。
:::

### 仅靠「用眼镜测量」无法驱动进化 —— 选择压组件 lldarwin 的设计与实测 #26

> **概念 hook**: 在上一篇 #25 中，我曝光了一次巨大的失败：「把 AI 进化 500 代之后，世界上只剩下**我和 Friston**了。」
> 冈洁、格罗滕迪克、冯·诺依曼，全都在进化途中悄然消失。原因在于：评价函数（眼镜 = lleval）持续给出满分，导致**选择压降为零**。即使能「测出」谁更优秀，如果无法把这个差异转换为「谁能存活」，进化就堕落为单纯的遗传漂变。
>
> 那么——既然眼镜让我们能「测出」差异，那把这个差异**正确转换为「淘汰」的装置**该如何制造？
> 那就是本篇的主角，**lldarwin**。它是 ll- 家族的新成员，是**专门负责淘汰（选择压）**的组件。
>
> 本文希望你记住的关键词，只有一个：**「不要聚合」**。把多把尺子加总成一把的那一刻，进化就坏掉了。为什么会这样，以及我如何用实测跨越它——接着失败往下讲，这次说的是**实际跑起来了**的故事。

---

#### 0. 三行概述（落语的「枕」）

落语在正题之前有「枕」。先用三行勾勒全貌。

- **lleval 测量，lldarwin 淘汰** —— 进化只有作为「测量」与「淘汰」的两段式结构，才第一次有意义。
- 淘汰的第一原则是**不聚合多个选择压的多目标淘汰**。在此结构性地切断 #25 失败的真因（用单一标量的 argmax 压垮了它）。
- 采用的三大支柱 = **ε-lexicase + minimal-criterion QD + down-sampling**（横向调研 evolutionary_computation 语料库 616 篇后选定）。

而且这次与 #25 的区别在于：不仅有骨架，还有**实测**。用 novelty pressure 把行为多样性从 7.12 → 14.88（+109%）翻倍，用**中立贮藏库**实际**全员复活**了「已灭绝的冈洁、格罗滕迪克谱系」，最后面对**本地部署的真实 LLM（llama3.2）**，进化 prompt 策略，把不擅长的任务从 0.0 → 1.0 改善。按顺序逐一来看。

---

#### 1. 为什么要把「测量」与「淘汰」分开

llive 家族中已经有 **lleval（眼镜 = 评价框架，连载 #24-08）**。它是观测个体行为、按多个轴打分的装置。

然而 #25 揭示的是一个致命的真相。**即使能用眼镜测出差异，一旦用 argmax 把那个差异压成一个，淘汰就坏掉了。** 具体来说，`fitness_rich` 把多个 archetype 相似度用 `nearest = max(sims)` 折叠成了单一标量。这就是 SEL-2 违规——「best=1.0 饱和，所有人都拿满分，选择梯度消失」的真因。

明确区分职责的话，是这样。

```
lleval   = 测量  （把个体行为转换为「多轴的 pressure profile」）
lldarwin = 淘汰  （把那个 profile 转换为「下一代的亲本」）
```

`lleval` 的输出是 **case 向量**（各轴分数排列成的数组）。`lldarwin` 把它作为输入契约接收，**不聚合地**进行淘汰。两者的职责边界正在于此。如果 lleval「把轴加总成一把之后」再交过来，lldarwin 就什么都做不了。所以对 lleval 一侧课以契约：「必须保留并传递 breakdown（按轴的分解）」。

lldarwin 的 `Pressure` 接口，由以下最小契约表达。

- `name` —— 轴的名称（`typo_robustness` 等）
- `evaluate(individual_output) -> case_scores: list[float]` —— 把个体行为转换为「按轴的分数数组」
- `is_proxy: bool` —— 是 proxy 测量还是真实 LLM/VLM 测量（测量纯度的区分）
- `minimal_criterion: float | None` —— 该轴的最低繁殖标准（None 则无 gate）

要点在于：`evaluate` 的返回值是**列表，而非标量**。一个轴之内也有多个 case（测试用例），不压垮它们而直接流向 lldarwin。这种「不压垮」的设计，是后面拯救 specialist 的伏笔。

> 🍵 **休息点**: 把眼镜（lleval）与滤镜（lldarwin）分开的意义，用摄影来说就是「测光」与「决定采用哪一张」的区别。即使测光完美，选错最佳镜头相册也就毁了。即使曝光表（lleval）告诉你「这一张亮度 80 分、构图 30 分、表情 95 分」，你是把它四舍五入成「平均 68 分」而丢弃，还是「把表情 95 分的那一张另设一格保留」，相册的丰富程度会有天壤之别。lldarwin 是「采用判断」的专家。让测量者与挑选者一人兼任，通常两边都会变得粗糙。

---

#### 2. 设计的核心 —— 「不聚合」的 7 个阶段

lldarwin 把从 lleval 接收的 pressure profile（多轴的 case 向量）通过以下 7 个阶段进行淘汰。对每一个都附上「为什么需要 = 防止哪种失败」。

1. **Standardizer** —— per-dim z-score。不偏向那种仅仅「全轴平均偏高」、毫无特征的优等生，而把各轴上的**偏离**转换为选择压。中心一致（与大家相同）被排除。
   - *防止的失败*: 「仅仅平均分高」的平庸者获胜、尖锐个体消失的 monoculture 入口。
2. **MinimalCriterionGate** —— 按各轴的最低标准划分繁殖资格。不让仅凭连续排名就「赢者通吃」。
   - *防止的失败*: 一强独占全部繁殖名额的全灭场景。以「只要满足标准谁都能繁殖」的「最低保障」保留多样性的地基。
3. **EpsilonLexicaseSelection** —— 把各轴作为 case 一个一个独立评价。在某个轴上突出的 specialist（其他轴平庸）也能存活。
   - *防止的失败*: 聚合 argmax 导致的 specialist 灭绝。这正是产生 #25 的 8→2 的机制本身。
4. **QD / MAP-Elites archive** —— 把 pressure profile 转换为 behavior 描述子，按 cell 保留 elite。archive 单调增长。
   - *防止的失败*: 结构性全灭。只要一个 cell 中哪怕残存一个个体，那个行为就不会消失。
5. **Niching / FitnessSharing** —— 对同一 niche 的个体降权，让多峰并存。
   - *防止的失败*: 向单峰的凝聚（monoculture）。
6. **Down-sampling** —— 每一代只用 case 的子集来评价，扰动环境。
   - *防止的失败*: 对特定 peak 的过适应与 plateau（停滞高原）。通过使其成为 moving target，不允许「用同样的方式获胜」。
7. **NoveltyScorer** —— 停滞时，向「与过去不同的行为」施加探索压。
   - *防止的失败*: 探索枯竭。当改善停止时，把新颖性本身作为奖励，推向外部。

与 #25 的 8→2 monoculture 对比，核心是三个：**(3) ε-lexicase、(4) QD archive、(2) minimal-criterion**。在 #25 中这些全部缺失，只有单一标量 argmax 在运转。所以「平均最强的一个谱系」把连续排名通吃，其余在漂变中消失。lldarwin 通过「不聚合地把这三个捆在一起」，构建出即使世代累积也不崩溃的结构。

> 🤔 **比喻（漫才风）**:
> 捧哏「把考试分数全加起来排名，结果只剩下平均分高的优等生了。」
> 逗哏「那不是零多样性吗！数学 100 分、其他都 0 分的天才不见了啊！」
> 捧哏「不过，论总分还是优等生更高啊……」
> 逗哏「**别看总分！** 一个科目一个科目看的话，那个天才在『数学』这个 case 上谁都赢不了。ε-lexicase 就是拯救这个的机制。一加总，天才就死了。」
> ——加总（聚合）杀死 specialist。因为 ε-lexicase「一个科目一个科目地看」，尖锐的家伙才能存活。这就是 lldarwin 的头号要义。

---

#### 3. 为什么是这 3 大支柱（rad-research 的支撑）

作为「即使世代累积也不崩溃」的最有力融合方案，我横向调研了 evolutionary_computation 语料库 616 篇后选定。来历很重要：我不是自己发明的，而是从既有研究中甄选并捆绑了「不聚合」的谱系。

| 方法 | 效用 | 出处 |
|---|---|---|
| **ε-lexicase** | specialist 保存、high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | 凭 per-cell elite 实现全灭不可能 | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | 环境扰动、降低成本 | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | 防止早熟收敛（将来选项） | Lyu 2020 (2005.07376) |

三大支柱看似各不相干，实则可以被**一个思想「不聚合」**串成一串。ε-lexicase「不聚合各轴」。QD「不聚合行为空间（按 cell 保留）」。down-sampling「不固定评价环境（每代扰动）」。它们都在「不把它们揉成一把」这一点上共享相同的哲学。所以即使组合，思想也不冲突，反而相乘增益。

> 🍵 **休息点**: 有人问「为什么不自己发明？」答案很简单：**因为既有研究的组合已经足够强**。我的开发规则（[[feedback_originality_over_imitation]]）写道：「外部算法的采用是**甄选**而非穷尽。排除崩溃风险与单纯模仿，只采纳能为原创设计增值的东西。」lldarwin 的原创性不在于「发明了新的选择算法」，而在于「**不聚合地把它们捆起来的捆法**，以及把它**实际接线**进 llive 的进化循环」。用做菜来说，不是创造世界首创的食材，而是把既有的名食材「不混合地盛在一盘」的手艺。把混合就会毁掉的食材，不混合地使其共存。

---

#### 4. Stage1 —— 用 criteria 排除 + novelty pressure 把行为多样性翻倍

从这里开始是实测。Stage1 中，没有一下子把设计全部实现，而是只放入最可能有效的两个改动来测量（llive, branch `optimize/core-2026-05-20`, commit `8060204`）。

**改动 1: criteria 排除。** 从 ε-lexicase 的 case 中，移除了 `factor_score`（= max-archetype 的单一标量 = argmax，正是 #25 的 best=1.0 饱和的真因）与 `nearest_persona_idx`（= 顺序无意义的类别 index）。这是一次「把坏尺子从淘汰的判断材料里清除」的打扫。

**改动 2: novelty pressure。** 启用 `MultiPressureSelector(use_novelty=True)`。每一代计算与过去世代 archive 的 k-NN 平均距离（Lehman-Stanley 流的 novelty），在群体内做 z-score 化（STD-1），作为附加的 lexicase case 混入淘汰。把「在做着与大家不同的行为」这件事本身，作为轴之一来评价。

测试方面，把 `tests/unit/test_evolutionary_lldarwin.py` 从 8 → 10 个扩展（增加排除、novelty 保存）。进化系 847 个 green，无回归。

实测条件是 rich-proxy、8 founders + pop24、150 代、seed 0。结果如下。

##### 4.1 行为多样性 (diversity_l2) —— novelty 见效的指标

| 条件 | mean | tail30 min | final |
|---|---|---|---|
| BASELINE（排除前、相当于 Tournament 的旧 lldarwin） | 7.12 | 0.68 | 0.83（崩溃） |
| A: 仅 criteria 排除 | 9.16 | 1.57 | 1.57 |
| **B: 排除 + novelty** | **14.88（+109%）** | **6.56（9.6×）** | **11.73（避免崩溃）** |

novelty pressure 把行为（genome 空间）的多样性维持在约两倍，防止了终盘的多样性崩溃。仅 criteria 排除单独也有效（清除了 spurious 的 argmax 压那部分）。BASELINE 在 final 0.83 处**崩溃**，而条件 B 在 final 11.73 处**站稳了脚跟**。这是「不聚合」设计的第一份手感。

![Stage1 baseline（无 novelty）的适应度与多样性。终盘多样性崩溃](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_zh.svg)

![Stage1 有 novelty。多样性维持到终盘](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_zh.svg)

把两张并排，终盘行为的差异一目了然。baseline 的多样性曲线贴在地板上，而有 novelty 的则保持高水平一路跑到终点。

> 🍵 **休息点**: 用金鱼池来比喻 novelty pressure——如果只留下围着饵（高 fitness）扎堆的金鱼，迟早会变成所有金鱼在同一处做同样动作的池子。novelty pressure 就是那个「**给在不同地方游的金鱼也发奖金**」的角色。结果是一个金鱼散布各处、看不腻的池子。但在这里不能松懈。下一节，会发现潜伏在这「热闹的池子」里的**陷阱**。

---

#### 5. honest disclosure（最重要）—— 我把行为多样性与谱系存活混为一谈了

这是本文最重要的一节。即使出了好数字（+109%）也不能就此自以为赢——这是我的铁律（[[feedback_benchmark_honest_disclosure]]）。我怀疑了内幕。然后，找到了错误。

##### 5.1 谱系固定 (founder_counts) —— novelty 无法改善的指标

在同一份实测里，看另一个指标。「8 个 founder（祖先谱系）中，有几个谱系存活到了最后？」

结果是——**在所有条件下，最终都从 8 → 2 个谱系**（furuse-kazufumi + friston）收敛。oka-kiyoshi（冈洁）/ grothendieck（格罗滕迪克）/ von-neumann / feynman / millidge / isomura **全部灭绝**。

明明放入了 novelty 把行为多样性翻倍，**谱系的存活却与 #25 完全相同，是同样的 2 个谱系**。

##### 5.2 为什么 —— 我混淆了两种「多样性」

设计书（#25 时点）的 TODO 写着「在重跑中验证冈洁、格罗滕迪克谱系是否存活」。这就是**把行为多样性与谱系存活混为一谈了**。

`poc_evolution_env.py` 的作者注释（L129-132）精确地点中了这个混淆。

> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs QD niching on lineage / PERSONA-FX, not pure novelty**"

掰开来讲，是这样。

- 已证实的 monoculture 0.05 是**行为性的**（archive-cell 的占有率），而**不是谱系性的**。novelty/lexicase 改善的是「行为的扩散」，而非「祖先的存活」。
- 谱系固定因中立漂变（木村资生的中立进化论）而趋向 monoculture，是**理论上正常的**。这不是崩溃。novelty 与 lexicase 都只拥有**保存既有个体**的机制，而**没有让一旦灭绝的谱系复活的机制**。所以谱系固定从结构上无法阻止。
- 此外，archetype 之间的距离也被压缩在 0.068～0.29（相似度密集于 0.71～1.0），选择梯度弱，drift（漂变）占主导。friston 是最非中心的（centroid 距离 0.162），却存活了 = 不是中心性（强度），而是凭**运气（drift）**，2 个谱系被固定了下来。

也就是说——我「希望冈洁、格罗滕迪克存活」的愿望，是一种**用提升行为多样性的药绝对治不好的病**。我用错了药。这是值得诚实记录的教训。

> 🍵 **休息点**: 用漫才来说。
> 捧哏「在池子里增加了各种五颜六色动作的金鱼！多样性满分！」
> 逗哏「那，**血统**呢？原本有的 8 个金鱼家系，还剩几个？」
> 捧哏「……2 个。」
> 逗哏「动作那么花哨，家谱却空空如也啊！动作的多样性和血统的多样性是**两码事**！」
> ——「行为多样」与「谱系多样」，是看起来相像、实则完全不同的指标。我把它们混淆了。诚实曝光。

---

#### 6. Stage1.5 —— 用中立贮藏库让灭绝的谱系复活

一旦弄清病的真面目，就能换药。谱系存活所需要的，是「让灭绝的谱系每代 re-inject 的机制」——**lineage-niched 中立贮藏库（reservoir）**。

##### 6.1 先用 PoC 确认机制

没有一上来就改造正式循环，而是先用 standalone PoC 确认机制能转起来（[[feedback_poc_feasibility_first]] = 需求 → PoC → 可行性 → 详细设计，llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`）。

selection 沿用 Stage1 的 `MultiPressureSelector`（criteria 排除 + novelty）。fitness 是 rich-proxy。谱系从 parent_a 继承。**reservoir = 按谱系保留 best-ever genome，并把灭绝的谱系每代 re-inject**（替换掉低 score 的子代；best 不破坏）。用 8 founders + pop24 + 150 gens + seed 0 测量。

| reservoir | 最终 named 谱系 | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1**（oka-kiyoshi 24/24 = 完全 monoculture） | 1.00 | 1.58 |
| **ON** | **8（全 founder 存活）** | **0.31（≪ 0.8 OE-3）** | 1.69 |

reservoir ON 时，包括冈洁（oka）、格罗滕迪克（grothendieck）在内的**全部 8 个谱系存活**。最终 shares 为 friston 7 / furuse 6 / grothendieck 4 / oka 3 / 其余 4 个谱系各 1。**强谱系带着子孙繁殖，弱谱系由贮藏库维持生命**，这是理想的行为。行为多样性也未下降（1.69 vs OFF 1.58）。

**Honest 保留（PoC 阶段）**: 由于贮藏库再投入 frozen elite（被冻结的代表），弱谱系（各 1 体）的「存活」是来自再投入，而非主动进化。这符合中立贮藏库的定义（保留代表，使其可再组合），是正当的，但我不主张「弱谱系仍在活跃地持续进化」。

##### 6.2 嵌入正式 EvolutionLoop（additive + default-off）

由于 PoC 已确认机制，我把它嵌入了正式的 `EvolutionLoop`（commit `b03cbda`）。设计的关键是 **additive 且 default-off**——丝毫不改变既有行为，只在立起标志时才生效。死守了向后兼容。

- 增加 `EvolutionLoop.on_population_bred` hook（可在 breed 之后、评价之前转换 bred 列表；默认 None = 向后兼容）。
- `LineageReservoir`（`lineage_reservoir.py`）: 祖先追踪（继承 parent_ids[0]）+ 按谱系保留 best-ever + 灭绝保护谱系的 re-inject。共享 `founder_map`，与谱系日志保持一致。
- 增加 `run_persona_evolution(lineage_reservoir=True)` / run 脚本 `--lineage-reservoir`。
- tests: `test_evolutionary_lineage_reservoir.py` 6 个 + 进化系 **937 green**（无回归）。

在真实 EvolutionLoop 中的实测（rich-proxy + lldarwin + novelty, 8 founders / pop24 / 150gens / seed0）。

| 条件 | named 谱系存活 | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8（furuse 17 + friston 7） | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8（全谱系）** | **0.33** | **0.29（≪ 0.8 OE-3）** | 9.20 |

包括冈洁（oka 3）、格罗滕迪克（grothendieck 1）在内的**全部 8 个谱系，在真实循环中存活**。正式实现以 0.29 复现了 PoC 的预测（fixation 0.31）——这是机制按设计运转的证据。

这是本文最大的看点。请对比下面两张。

![中立贮藏库 OFF。谱系支配 stream 最终崩溃为 furuse 71% / friston 29% 的 2 个谱系](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_zh.svg)

![中立贮藏库 ON。全部 8 个谱系（millidge / von-neumann / oka / grothendieck 等）并存](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_zh.svg)

OFF（上）：随着世代推进，stream 被吞入 2 种颜色——这是 #25 的「只剩我和 friston」的再现。ON（下）：8 种颜色作为带子一直保留到最后。冈洁、格罗滕迪克，都没有消失。

![中立贮藏库 ON 的适应度与多样性](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_status_zh.svg)

> 🍵 **休息点**: #25 中我哀叹「只剩我和 Friston」的那个寂寞的世界。这次它变成了冈洁、格罗滕迪克、冯·诺依曼全都在场的热闹世界。**这不是捏造，而是实际跑出来的结果**（遵循 [[feedback_benchmark_honest_disclosure]]，既不写虚假的失败，也不写虚假的成功）。但是——在得意忘形之前，请回想 §5 学到的态度。「出了好数字就怀疑内幕」。在下面的 §6.3，我诚实写下这次成功也是有**代价**的。

##### 6.3 Honest 保留 —— 谱系保持与行为多样性是弱权衡

reservoir ON 时谱系全员存活。但仔细看，**diversity_l2 从 14.88 → 9.20 下降了**。由于每代再投入 frozen elite（冻结代表），genome 空间的扩散稍有减少。

不过，OFF 时的崩溃（final 0.83）被避免了。也就是说，这是一种**弱权衡**关系：「取谱系保持，行为多样性的峰值会略降，但能防止崩溃」。它不是零代价的魔法。我诚实写下来。而这个代价能压到多小，成为下一个 sweep 的主题。

---

#### 7. 再投入频率 sweep —— 非单调最优点这一非平凡发现

我用 `reinject_interval`（执行再投入的世代间隔；默认 1 = 每代）的 sweep，对 §6.3 的 honest 保留（frozen elite 再投入会使 diversity 下降）做了特性化（commit `da93dd3`）。增加 `LineageReservoir.reinject_interval` + `--reinject-interval` 标志（test 7 个）。8 founders / pop24 / 150gens / seed0。

| interval | named 存活 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**（每代） | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84（最大）** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**这里有一个非平凡的发现。** 直觉上你会预想「减少再投入（提高 interval），frozen elite 的塞入就减少，diversity 单调恢复」对吧？然而——**diversity 并未单调增加，而是在 interval=5 处达到峰值**，在 10/20 处反而下降了。

想想原因就能信服。把谱系放任过度（interval 太大），则 (a) 来自贮藏库的多样性注入减少，(b) 少数谱系被固定，结果 diversity 也长不上去。「再投入过多」和「放任过度」两边都不行，最优点在中间。这是**不实际跑 sweep 就无法预测**的知见。

运营指南变成了这样。

- 若**以谱系保持为最优先** → interval=1（8/8 全谱系存活）。
- 若想**兼顾行为多样性** → interval=5（保住 5/8 的同时 diversity 最大）。

兼顾的最优点依赖于 fitness 的设计与群体规模，所以正式环境中要用 sweep 重新标定。

![再投入频率的权衡。谱系保持与行为多样性成反比，diversity 在 interval=5 处达到峰值（非单调）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_zh.svg)

> 🍵 **休息点**: 就像落语的 sage（包袱），这里有一个「背叛预期的转折」。本以为「越做越好」，结果是「做过头反而有害」。和给植物浇水一样：浇太少会枯，浇太多会烂根。最优点在中庸。做进化计算时，会一次又一次遇到这种「不单调的曲线」。所以要测基线，跑 sweep。直觉，常常被背叛。

---

#### 8. Stage2 前半 —— 用 proxy 把「LLM 的弱点」变成选择压

到此为止都是用 rich-proxy（基于 persona 相似度的 heuristic）确认机制。接下来实现设计的另一根支柱：**把「LLM/VLM 现实中弱、且可测量的轴」变成 pressure**（一系列 commit, `pressures.py`）。

我把设计 §3 列出的 5 个可 proxy 的轴做成了 plugin。

| pressure（LLM 弱点） | 相关思考因子（case） |
|---|---|
| typo_robustness（噪声耐受） | consistency / reality_link / uncertainty |
| polysemy_wsd（多义词） | multiview / consistency / reality_link |
| multistep_robustness（多步推理） | structurize / closed_loop / self_extend |
| calibration（置信度估计） | uncertainty / provenance |
| context_management（无关上下文耐受） | consistency / provenance / recompose |

`make_pressure_fitness()` 把各 pressure 的 case（共 14 个）输出到 breakdown，lldarwin 的 ε-lexicase **不聚合地按轴淘汰 specialist**。增加 `--fitness pressure-proxy`。tests `test_evolutionary_pressures.py` 4 个 + 进化系 **942 green**。

end-to-end 实测（pressure-proxy + lldarwin + novelty + reservoir, 8 founders / 120gens）: named 谱系 **8/8 存活** / lineage_fixation (tail) 0.67 / diversity_l2 (tail) **17.91**。14 个弱点轴 case 被独立淘汰，行为多样性高。谱系由 reservoir 维持（由于 pressure-proxy 不直接奖励 persona 的同一性，优势谱系的 share 比 rich-proxy 的 0.29 更高，为 0.67）。

![5 个弱点轴（typo / polysemy / multistep / calibration / context）的群体平均推移（proxy 测量）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_zh.svg)

**Honest 保留（设计 §7 / §7.1 已明示的已接受局限）**: 个体不是真实 LLM，而是 genome（llive 配置）。本 pressure 测量的是「genome 具备多少与该弱点**相关的思考因子**」这一**行为的代理**，而**不是 production 的 LLM 能力**。这仅限于 **mechanism feasibility（机制能转起来）的验证**。Goodhart 风险（hack proxy 的表面策略会进化）也是已接受的局限。真实 LLM/VLM 弱点轴的实测，留到 Stage2 后半（以 OLLAMA_HOST 设置 + 个体→真实 LLM 映射为前提）。

> 🍵 **休息点**: 这里容易被误解，所以再叮嘱一遍。我**还没有说**「用进化克服了 LLM 的弱点！」proxy 测的只是「机制是否转起来」。真实 LLM 是否变得对 typo 更鲁棒，在这个阶段完全不得而知。即使 proxy 出了花哨的数字（17.91），那也是「装置在运转」的证明，而非「内容变聪明了」的证明。一旦把这条线模糊掉，研究就成了谎言。所以接下来，我面对**真实的 LLM**。

---

#### 9. Stage2 后半 —— 面对真实的本地部署 LLM，进化 prompt 策略

由于发现 localhost 的 ollama（llama3.2:latest 等）可达，终于可以进行**真实 LLM 评价**了（commit `2fb2912`）。因为 localhost = on-prem，所以也满足 measurement purity（测量纯度，不与 cloud LLM 混用）的纪律（[[feedback_llive_measurement_purity]]）。

##### 9.1 个体 → 真实 LLM 的映射（Promptbreeder 系）

关键是「如何让 genome 在真实 LLM 上生效」。我在 `real_pressures.py` 中实现了 **个体 → 真实 LLM 映射**。

- **把个体的 `c_prompt`（PromptChromosome）转换为 system prompt**: skill_set → 指示文 / prompt_template_id → 推理风格 / language_style → 语调。把这个 system prompt 套在固定的 LLM（llama3.2）上，让它解 5 个弱点轴的**真实任务**并打分。
- **固定 LLM 本体，进化 prompt 策略（genome）** = 用实测淘汰「哪种 prompt 策略能缓解 LLM 的弱点」。这是 Promptbreeder（用进化方式优化 prompt 的研究系列）的做法。
- temp=0（greedy）确定性地进行。把 `(system_prompt, task)` 缓存（同一策略不再评价）。
- robust: per-call try/except（ollama 的 hiccup 当作 task 的失分处理，运行继续）。
- 增加 `--fitness real-pressure` / `--ollama-model` / `--max-wallclock-seconds`。tests 5 个 + 进化系 947 green。

##### 9.2 真实选择信号的实证 —— CoT+structure 策略把 multistep 从 0.0 → 1.0

然后，观测到了真实的选择信号。

**CoT+structure 策略**（`chain_of_thought` + structurize + loop）把 llama3.2 的 **multistep（多步推理）从 0.0 → 1.0 改善**（terse 策略以 0.0 失败；score 从 0.80 → 1.00 上升）。

这意味着，lldarwin 的主张「用 prompt 策略的进化可以缓解 LLM 的弱点」，**不是用 proxy，而是在真实 LLM 上实证**了。即使是同一个 llama3.2 本体，根据套上去的 system prompt（= 进化后的 genome）不同，多步推理任务时而能解、时而不能解。进化实际选取了「能解的 prompt 策略」。

![5 个弱点轴的群体平均推移（真实本地部署 LLM llama3.2 评价）。prompt 策略的进化使轴改善](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_zh.svg)

##### 9.3 12h 连续运行

真实 LLM 评价很重，所以启动了长时间的连续运行（`out/lldarwin_12h_realpressure_2026_05_26/`）。

```
--fitness real-pressure --selection lldarwin --novelty --lineage-reservoir
--genome3d --population 24 --max-wallclock-seconds 43200 --checkpoint-every 5
```

在 wallclock 12h 处 safely 停止（已 snapshot → 可用 `--resume` 继续）。在连续运行中达到了 best_score=1.0。

![真实 LLM 进化运行的适应度与多样性（12h 连续运行）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_zh.svg)

##### 9.4 Honest 保留（真实 LLM 评价的局限）

这里是从 #25 学到的态度的总决算。正因为出了花哨的结果（0.0 → 1.0、best 1.0），我才彻底诚实地写下内幕。

- **(a) 参与 fitness 的只有 `c_prompt`。** persona / c_factors 是中立的（谱系由 reservoir 维持，初始选择由 novelty 承担）。也就是说，这是「**prompt 策略的进化**」，而非「persona 的进化」。不是冈洁的人格变聪明了，而是与冈洁这个谱系绑定的 prompt 策略被选中了。
- **(b) 全部 founder 的初始 c_prompt 相同（default）。** 所以探索是 mutation 驱动的（按 founder 使 prompt 多样化是今后的改善）。由于起点相同，初始的谱系差异对 prompt 策略没有作用。
- **(c) 小电池（每轴 2 题）= 噪声大的估计。** 0.0 → 1.0 这一戏剧性数字，也因题目数量少而含有噪声。要做统计上稳健的主张，需要更大的电池。
- **(d) on-prem only（measurement purity）。这不是关于一般能力的主张。** 这是在 llama3.2 这一特定模型、特定任务上的观测，我不说「LLM 一般会这样」。

如果把这些藏起来，就能写出「进化让 LLM 变得戏剧性地聪明了！」这样花哨的故事，但那是谎言。lldarwin 实证的，只到「**机制在真实 LLM 上产生选择信号**」为止。越过那条线的主张，我不做。

> 🍵 **休息点**: 研究中最爽的，是喊出「0.0 变成 1.0 了！」的那一刻。但正是那一刻，[[feedback_benchmark_honest_disclosure]] 才发挥作用。「出了诡异地好的数字，自以为赢之前先怀疑内幕。」就这次而言——赢的是「prompt 策略」，而非「LLM 本体」也非「persona」。题目数量也少。只有 1 个 on-prem 模型。把这些全写出来，才第一次能说「实证了」。honest disclosure，是忍住炫耀的肌肉训练。

---

#### 10. 既有资产的再利用（基于 codex 代码调查）

为了不让设计沦为画饼，我让配下的 Codex 调查既有代码，结果发现**很多都是已实现、未接线**。

- `mating.py:139 LexicaseSelection`（带 ε，已实现但未接线 → 只需接线）
- `nsga2.py:197 NSGA2Selection`（用于 ≤3 目标 lane）
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**新实现**: `Standardizer` / `MinimalCriterionGate` / `Pressure` 群 / `MultiPressureSelector`（核心）/ `LineageReservoir`（Stage1.5）/ `SelectionAudit`。
**接线点**: 在 `loop.py:122` 的 `selection` 注入 `MultiPressureSelector`，在 `persona_evolution.py:606` 增加注入口，把 `LineageReservoir` 接到 `EvolutionLoop.on_population_bred` hook。

> 🍵 **休息点**: 「已实现但未接线」最多，是最大的教训。即使做出好部件，**不接线（编排）进化就仍然坏着**。#25 之所以变成 8→2，是因为 ε-lexicase、NoveltyScorer、QD 都「在箱子里却没接线」。lldarwin 的本质，与其说是新算法的发明，不如说是「把既有的好部件**不聚合地**捆起来，并**实际接线**进进化循环」。即使把电子元件全凑齐，不焊接收音机也不会响。

---

#### 11. 防止崩溃的保证 —— 不会全灭的多层结构（已由实测支撑）

反证 #25 的 monoculture（8→2）的多层结构，按设计齐备，而且这次**得到了实测的支撑**。

1. **MinimalCriterionGate** —— 以最低标准定繁殖资格 → 抑制一强通吃。
2. **QD per-cell elite** —— 只要残存 1 个 cell，谱系就不可能全灭（archive 单调增长）。
3. **Niching / FitnessSharing** —— 对同 niche 降权 → 多峰并存。
4. **Down-sampling** —— 用 moving target 破坏 plateau。
5. **per-dim z-score + 中心一致排除** —— 不偏向无特征者。
6. **LineageReservoir（Stage1.5 中追加）** —— 灭绝谱系的中立贮藏库 → 从结构上阻止谱系全灭（实测 8/8 存活）。
7. **monoculture 监视 + SPC** —— 每代记录 max_lineage_share，用 SPC_ALARM 检测 >0.8 → 自动调整。

特别是 (6)，是承接 §5 的 honest disclosure（novelty 无法阻止谱系固定）而**事后追加的一层**。用实测找到设计的漏洞并堵上。实测的 lineage_fixation 为 OFF 0.70 → ON 0.29，大幅低于 OE-3 标准（<0.8）。以「不聚合」+「让灭绝谱系复活」的两段式，从结构上压垮 #25，是本文的到达点。

---

#### 12. honest disclosure / 风险（前置铺垫）

我不盲信设计。把已接受的局限（下一篇 #27 深挖）再总结一次。

- **Goodhart's law / proxy 偏离** —— 把 LLM 弱点做成 proxy fitness，「hack 指标的表面策略」就会进化（typo → 背诵特定替换、WSD → 利用测试的 heuristic 等）。proxy 仅限于 mechanism feasibility，不主张 production 能力。
- **设计者依赖性** —— lexicase=case / QD=描述子 / novelty=距离尺度，无论哪个，「多样性的方向」都由设计者决定。生物进化级别的未预想涌现是有限的。
- **minimal-criterion 的停滞⇄崩溃权衡** / **QD 的维度诅咒 + archive 饱和**。
- **真实 LLM 评价的局限（§9.4 重述）** —— 仅 c_prompt 参与 fitness、founder 初始 prompt 相同、小电池、on-prem only。

> **下回预告（#27）**: 我会诚实曝光最痛的反证——「当眼镜饱和，选择压就无力」，连同 Goodhart's law 与 proxy fitness 的局限。lldarwin 并非万能。**能主张到哪里**，是 #27 的主题。正因为这次出了「8/8 存活」「0.0→1.0」这样的好数字，下次才用反证来彻底锤炼它。

---

#### 13. 结论

- 进化是「**测量（lleval）**」与「**淘汰（lldarwin）**」的两段式。淘汰的核心是 **「不聚合」**。
- Stage1: 用 criteria 排除 + novelty pressure，把行为多样性从 7.12 → 14.88（+109%）翻倍，避免了终盘崩溃。
- honest disclosure: novelty/lexicase 保住的是**行为多样性**，但**谱系固定**会因中立漂变（Kimura）趋向 monoculture。我混淆了两种多样性——诚实记录。
- Stage1.5: 用 lineage-niched **中立贮藏库**，在真实 EvolutionLoop 中实现 **OFF=2 谱系 / ON=全 8 谱系存活**（含冈洁、格罗滕迪克），lineage_fixation 0.29（≪0.8）。**这不是捏造，而是实际跑起来了**。
- 再投入频率 sweep: 谱系保持↔行为多样性的权衡。diversity 在 interval=5 处达峰（**非单调**）这一非平凡知见。
- Stage2 前半（proxy）: 把 5 个弱点轴做成 Pressure plugin（仅 mechanism feasibility）。
- Stage2 后半（真实 LLM）: 用个体 c_prompt → system prompt 映射，对固定的 on-prem LLM（llama3.2）做真实任务打分。**CoT+structure 策略把 multistep 从 0.0 → 1.0 改善**。12h 连续运行达到 best=1.0。
- 不乐观、不自以为赢、分内幕地报告（[[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]]）。

仅做出好部件，进化仍然坏着。**不聚合地捆绑、实际接线、让灭绝的谱系复活、在真实 LLM 上确认选择信号**——做到那一步，才终于把 #25 的「只剩我和 Friston」的世界，变成了冈洁、格罗滕迪克也都在的热闹世界。在下一篇 #27 中，我用反证重新追问：对这次的成功，能寄予多少信任。

---

#### 14. 相关

- 连载 #25「只剩我和 Friston」—— 本文的动机（失败的记录）
- 连载 #24-08「制造眼镜」—— lleval（测量的一侧）
- 连载 #27「眼镜起雾，淘汰也无力」—— 反证调查（honest disclosure）
- 设计书: lldarwin（淘汰的一侧）`docs/vision/LLDARWIN_DESIGN.md`
- 实测正本: `docs/research/lldarwin_stage1_results_2026_05_26.md`
- llive commits: Stage1=`8060204` / 中立贮藏库 PoC=`0d0537d` / Stage1.5=`b03cbda` / reinject sweep=`da93dd3` / Stage2 真实 LLM=`2fb2912`
- 相关 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]] / [[feedback_poc_feasibility_first]]

---

## 3. 一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27（開放端進化 / ライブ・オーケストラ / honest cross-validation）

:::note info
**📚 FullSense 知识库指南** <!-- fullsense-team-kb -->
FullSense 开发全史 60+ 篇文章（4 种语言版、故事化的阅读顺序指南、通俗易懂版、四格漫画）均已汇总至 Qiita Team **FullSense KB**（仅限团队成员）。
:::

### 一夜之间重写了 AI 进化 —— 真实 LLM 的 12 小时运行又一次在满分处饱和，6 个 PoC、4 个 Agent 与 Perplexity「各自独立地收敛到同一个结论」的那一夜 #27

> 📚 **连载导航（lldarwin 弧线）**：#24-05 群体进化 → #25 monoculture 的失败 → #26 设计篇 → **#27 本文（高潮）** → 实现篇（计划中）。※ 每篇文章都可单独阅读（链接用于回览）。

> **概念 hook**：在上一篇 #25 中，我曝光了一个重大失败：把 AI 进化 500 代之后，世界上只剩下**弗里斯顿和我**。原因是评价函数（眼镜 = lleval）一直给出满分，导致**选择压力降为零**。
>
> 「那么这次，用真实的 LLM 来验证吧。」抱着这个想法，我对着 on-prem 的 llama3.2 **连续进化了 12 个小时**。不是 proxy（合成的尺子），而是真实 LLM。
>
> 结果。**在 gen5 就钉死在满分，此后 65 代纹丝不动。**不会全灭，但也不会累积。这不是进化，而是**单纯的「带筛子的随机搜索」**——不仅 proxy，**即使用真实 LLM，也还没有成为进化**。
>
> 由此，一个通宵。为了「决定方策」，我亲自跑了 6 个 PoC，并行启动了 4 个 Claude Agent，让 Perplexity 去翻文献。到了早晨，**所有人都各自独立地收敛到同一个结论。**这就是那份「通宵决策日志」的 honest disclosure。

---

#### 0. 三行概要（落语中所谓的「开场垫话」）

落语在正题之前有「开场垫话」。先用三行说。

- **又饱和了** —— 真实 LLM(llama3.2) 跑 12h，gen5 就钉在 best=1.0，65 代无进展。不全灭但也不累积 = **filtered random search（带筛子的随机搜索）**。真因与 #25 相同：「固定的人工尺子的饱和」。
- **一夜之间决定了方策** —— 6 个自跑 PoC + 4 个并行 Agent + Perplexity **各自独立地收敛到同一个结论**：「保持尺子固定却去打磨淘汰器是徒劳。**让评价本身开放端化。**」
- **独创性浮现了** —— 让一个持续进化的群体，在任意一瞬间不停下来地合奏（MoA）出一个答案的「**现场管弦乐团（live orchestra）**」，被证明是先行研究中的 white-space（空白地带）。

简言之：**「一旦眼镜（评价）饱和，无论怎么打磨淘汰器（lldarwin）都无力。」**所以改变打磨的对象——**让评价本身开放端化**，这就是本轮的结论。

---

#### 1. 为什么「又」做了一次 —— #25 / #26（设计）的延续

用三行回顾迄今的连载：

- **#24-05**「群体学习的 AI」—— 不是让一个 LLM 变聪明，而是建立了**让 N 个 llive 个体（genome）世代更替、相互评价**的派生群体进化框架。
- **#25**「只剩下弗里斯顿和我」—— 把 8 位智者作为人格种子撒入该群体，跑 proxy 500 代后产生重大失败：**满分饱和 → 选择压力为零 → 仅靠运气（遗传漂变）偏向 2 个谱系**。眼镜蒙了。
- **#26（设计篇）**「只靠眼镜测量并不会进化」—— 设计了淘汰器 **lldarwin**，实现了「不聚合的多目标淘汰（ε-lexicase / QD / 中性储库）」。在 proxy 中防住了谱系灭绝。

到这里为止，全部都是关于 **proxy（确定性启发式，不依赖 LLM）**的。proxy 能展示「机制能转」，却无法展示「进化找到了**有意义**的东西」（[[feedback_benchmark_honest_disclosure]]）。

所以，理所当然的下一步：**用真实的 LLM 来验证。**

由于 localhost 的 ollama（llama3.2:latest）可达，我把每个个体的 `c_prompt`（prompt 策略的基因）转换为 system prompt，覆盖在固定的 llama3.2 之上去解实际任务——这是一种 **Promptbreeder 系的映射**——启动了 12 小时的连续进化运行。这就是本文的出发点。

> 🍵 **休息点**：如果你已经到了「proxy 里机制转起来了——那真实 LLM 呢？」这个问题，就够了。研究的好处就是可以实际去跑这个「那真实的呢？」而这一次，真实的——毫不留情。

---

#### 2. 出发点 —— 真实 LLM 12h 运行的「诚实的不及格」

这是 12 小时真实 LLM 进化运行（on-prem llama3.2，严守 measurement purity = 不与 cloud LLM 混用，[[feedback_llive_measurement_purity]]）的结果。

| 事实 | 数值 | 含意 |
|---|---|---|
| 完跑 | 71 代 / 12h（≒10.3 分/代，真实 LLM 顺序执行） | 吞吐量为瓶颈 |
| best_score | **gen5 = 1.0 → 固定至 gen70** | **目标饱和。65 代无进展** |
| mean | 在 0.85 触顶，1.0 策略不席卷 | **适应不累积** |
| 各轴 | 10 题中 6-7 题饱和，梯度仅在 multistep（2 题） | 有效分辨率太小 |
| fitness 依赖 | **仅 c_prompt**。c_factors(40 维)/c_impl/c_meta 中性漂移 | **43 个维度选择压力为零** |
| 群体健康 | pop=24 维持・min ≥ 0.70・**未全灭** | 机制（GA）没坏 |

这里就是 FullSense 的 honest disclosure 规则让你停下脚步的地方（[[feedback_benchmark_honest_disclosure]]）。写成「没全灭！达到了 best=1.0！」听起来很成功。但看明细就一目了然。

**判定：未全灭，但也不是累积进化（≈ filtered random search）。**

10 题测试中，仍保有梯度（差异）的只有 multistep 的 2 题。其余 8 题很早就全员满分。也就是说 10 题中有 8 题，已经无论选谁都一样。选择压力的有效分辨率只剩下大约 2 题份。而且 4 条染色体中只有 `c_prompt` 这一条参与 fitness，其余 43 维（思考因子 40 维 + 实现 + 元）都是**选择压力为零的中性漂移**。

![真实 on-prem LLM（llama3.2）进化运行的适应度与多样性（12h 连续运行）。best 很早就钉在天花板，此后平坦](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_zh.svg)

![5 个弱轴（typo / polysemy / multistep / calibration / context）的群体均值轨迹（真实 on-prem LLM 评价）。除 multistep 外均早期饱和，无残留梯度](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_zh.svg)

**真因 = 人工固定尺子的饱和。**用户在 #25 中言明的洞见「**一旦眼镜饱和，选择压力就无力**」，这次我们不是用 proxy 而是**用真实 LLM 实证**了。把眼镜从 proxy 换成真实 LLM 也没用：**只要尺子是「固定的 10 题」，就会很快在满分处饱和。**换了镜片厂商，刻度若粗也是一样。

> 🤔 **比喻**：即使把判分者换成「真正的老师」（真实 LLM），如果每次出的题都一样，几轮内大家都会拿满分，此后无论考多少次都拉不开差距。不是题目不好，而是**试卷固定且太简单**。把判分者（眼镜）从 proxy 换成真实 LLM，只要尺子（题目）固定就会饱和。这就是「诚实的不及格」的本质。

> 🍵 **休息点**：很多人此时会想「连真实 LLM 都饱和，岂不是无解了？」我也这么想过。但正题从这里开始。如果**「把尺子固定下来才是错的」**，那要修的既不是淘汰器也不是 LLM，而是**造尺子的方式本身**。我用一个通宵、6 个 PoC、4 个 Agent 和 Perplexity 验证了这一点。

---

#### 3. 一夜的作战 —— 为「决定方策」而进行的分布式调查

用户给来的指示是这样的：

> 「彻底整理需求，作为进化型系统拿出更多独创性。PoC 也反复多跑。一直到明早，用小单位不停地跑 PoC 来**决定方策**。」

这里关键在于，目的**不是「完成实现」而是「决定方策」**。所以不是跑一个大型正式运行，而是采取**大量跑小 PoC**、用真实数据一个一个地敲掉设计判断的作战（[[feedback_poc_feasibility_first]] = 需求 → PoC → 可行性 → 详细设计）。

并行运转的工作者是这些（[[feedback_parallel_first_execution]] = 独立任务默认启动并行 Agent）。

| # | 工作者 | 任务 |
|---|---|---|
| A | Claude Agent | 开放端 sweep PoC（实证 baseline = 饱和/全灭 vs 开放端 = 回避，≥1 万代） |
| B | Claude Agent | 观测基础（响应日志 / 个体分数时序查看器 / lineage 复原） |
| C | Claude Agent | 管弦乐团 PoC（MoA 是否超越单一 best，多样性选拔 vs 冗余选拔） |
| P | Perplexity | QD/novelty/MoA/agentic 进化的 SOTA 综述（补足文献缺口） |
| X | Codex | 设计的独立批评 + 3 个最小 PoC 提案 + 盲点指出 |
| 自身 | 我（main） | 直接实现并执行自跑 PoC #1〜#6（orchestrator 兼最重要任务负责） |

> 🍵 **休息点**：这个「六人合力」体制，其实是本文隐藏的主角。为什么不用一个人（一个 context）全部做完？答案就在 honest disclosure 的核心。**用同一个脑袋想出的结论，会被同一种偏见牵着走。**用不同的方法（合成 PoC / 真实 LLM / 文献调查）**各自独立地**验证，只有当它们一致时才信任结论。这就是我所称的 **honest cross-validation**。它的威力在后半段显现。

这里记下一个诚实的哑弹。**Codex（X）用不了。**ChatGPT 账号的许可模型不匹配（API 侧全面拒绝 codex 系模型）导致受阻。本应在 10x promo 期间，API 却返回 "not supported when using Codex with a ChatGPT account"。由于这是环境问题，目前把主轴切换为自跑 PoC + 并行 Agent + Perplexity。**「本应能用却用不了的工具」也照记不误，不隐藏。**

---

#### 4. 第一记决定性打击 —— 是否舍弃「固定尺子」（自跑 PoC #1 / #2）

最先该敲掉的假设，是最根本的问题：**「把尺子从固定难度改为自适应难度，饱和会被修好吗？」**

##### 4.1 自跑 PoC #1 —— 自适应难度修好饱和，但杀死多样性

用合成的 competence 向量的 proxy，去除混杂后（按 score 选 elite）做对比。

- **baseline（固定难度）**：能力**在 0.627 低位停滞**（best 0.757）。在 proxy 中重现 12h 的病理。
- **adaptive（难度 = 跟随群体 60 分位）**：能力**上升到 0.952**（best 1.0）。

让难度跟随群体（能解的题增多就把题变难），饱和被解开、能力上升。**但是**——adaptive **牺牲了多样性**（diversity 崩塌 0.310 → 0.134）。在为难题优化的过程中，群体凝聚到了一个正确策略上。

##### 4.2 自跑 PoC #2 —— 自适应难度 × novelty 可以兼容

那么，在「自适应难度（维持梯度）」上加「novelty 选拔（维持多样性）」会怎样？

| 配置 | 最终能力 | best | 多样性 | plateau |
|---|---|---|---|---|
| baseline（固定难度） | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive（难度跟随） | 0.952 | 1.000 | 0.134（崩塌） | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316（维持）** | gen99（最长探索） |

**adaptive + novelty 同时兼顾了**能力（比 baseline +40%）与多样性（比 adaptive 2.4 倍，与 baseline 相当）。让出 7% 能力，换来多样性的完全维持。

至此，**方策的核心由自有数据确定。**

> **「自适应难度＝维持梯度」与「QD/novelty＝维持多样性」互补，两者都必须。**
> 固定尺子单独（baseline）也好，自适应难度单独（adaptive）也好，都不够。

honest 保留：这是抽象 proxy（competence 向量），并非真实 LLM 映射。仅限于**验证 mechanism feasibility（机制是否运转）**。plateau@gen 的数字指「停滞的世代」，但本质是停滞的**水平**——baseline 在低位（0.627）停滞，adaptive 系在天花板附近停滞。

> 🤔 **比喻**：当所有人都满分时就把题变难（自适应难度）。于是分数拉开了，但这次大家又收敛到了同一种解法（千篇一律）。于是再加上「对奇特解法也给奖励」（novelty），能力与多样性就兼容了。**「变难」与「奖励奇人」的双刀流**——这就是 PoC #2 的要点。

---

#### 5. 主战场的证据 —— 开放端进化的 1 万代 sweep（Agent A）

自跑 PoC 让「方向」浮现。下一步，是**大规模、严格地**敲打它。我让并行 Agent A 跑了**各 1 万代 × pop256 × 19 配置 × 2 巡**的开放端 sweep。

判定基准是是否「open-ended（开放端）」——**是否不饱和、避免 monoculture（向单一文化的收敛）、archive（多样性的储库）持续增长？**

##### 5.1 决定性的判定表

**verdict（gen9999 时点）：全 scalar 配置 = False / 全 novelty・lexicase 配置 = True**

| label | 选择 | std | MC | reservoir | archive | open-ended | occupied | monoculture | uniq_lineages |
|---|---|---|---|---|---|---|---|---|---|
| baseline_scalar | scalar | - | - | 0 | none | **False** | 9 | 0.74 | 1.0 |
| baseline_scalar_mc | scalar | - | ✓ | 0 | none | **False** | 9 | 0.90 | 1.0 |
| **scalar_qd** | scalar | - | - | 0 | map-elites | **False** | — | — | — |
| novelty_std | novelty | ✓ | - | 0 | none | True | 100 | 0.13 | 1.0 |
| novelty_std_qd | novelty | ✓ | - | 0 | map-elites | True | — | — | — |
| **novelty_std_res256** | novelty | ✓ | - | 256 | map-elites | True | 95 | 0.05 | **31.9** |
| novelty_std_res1024 | novelty | ✓ | - | 1024 | map-elites | True | 98 | 0.04 | 15.2 |
| **full_oe** | novelty | ✓ | ✓ | 1024 | map-elites | True | 90 | 0.05 | 15.3 |
| lexicase_std(_mc) | lexicase | ✓ | -/✓ | 0 | none | True | 111–122 | 0.03 | 1.0 |

由此得出四个决定性发现。

1. **选择压力是决定性的。**scalar（单一标量 fitness），即使加上 MAP-Elites 的 archive（`scalar_qd`）也**全灭（False）**。也就是说「加个储库就能守住多样性」是**错的**——**除非选择本身是开放端的（novelty / lexicase），否则开放端根本不成立。**单靠 archive 救不了。**让选择压力本身开放端化**才是本质。
2. **标准化（z-score）把 QD 覆盖扩大一个数量级。**在 novelty 上加 per-dim z-score 标准化，occupied cells 从 9 → 100+。把各轴的「偏离」变成选择压力，行为空间的覆盖就扩大一个数量级。
3. **中性储库恢复谱系多样性。**只用 novelty_std 时 uniq_lineages 为 1.0（谱系固定为一个）。加上 reservoir256 就到 **31.9**。**行为多样性与谱系多样性是不同的轴**，后者需要储库（这是对 #26 设计篇已实现知见的再确认）。
4. **规模有效。**把 latent 维度 256 → 1024，niche 从 101 → 166，archive 从 1021（饱和）→ 2234（持续增长）。多样性可以用「容量」买到。

![Stage1 baseline（无 novelty）的适应度与多样性。终盘多样性崩塌（scalar 的典型失败）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_zh.svg)

![Stage1 有 novelty pressure。行为多样性维持到终盘](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_zh.svg)

![baseline vs +novelty 的 diversity 叠绘。把崩塌（scalar）与维持（novelty）一图对比](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_zh.svg)

##### 5.2 Agent A 给出的「诚实的局限」

恰恰是在出好结果（open-ended 成立）时，才要写局限。Agent A 自己指出：

> novelty/lexicase 保持描述符**整体**的多样性，但**不保证特定语义维度（factor）的多样性**。
> 在大 latent 下会发生 factor drift，fspread（factor 的展开度）需监视。

也就是说，即使「整体上多样」，也可能在「思考因子这个特定语义维度上收敛」。这催生了新需求 **factor-subspace QD（对语义维度逐个保护的 QD）**（在后述 PoC #6 中应对）。

> 🍵 **休息点**：这是本文最硬的一节。希望带走的一行——**「单靠加 archive（储库）救不了。不让选择压力本身开放端就不行。」**自 #25/#26 设计篇起我们一直说「不聚合」，而其主战场就是「**让选择的方式开放端化**」，这被 1 万代的真实数据所断言。越过这里，剩下的就是独创性的话题了。

---

#### 6. 独创性的核心 —— 「让持续进化的群体，不停下来地合奏」

至此「在结构上回避饱和的选择核（S1）」已经稳固。下一步，是用 PoC 与文献为用户在对话中给出的**独创性 3 轴**做背书。

用户言明的 3 轴是这些。

1. **持续进化群体 = 现场管弦乐团（ORCH）** —— 持续进化的群体当场做 MoA（Mixture-of-Agents）聚合产出一个答案。进化不停。**最大的差异化候选。**
2. **具备调查功能的个体（AGENT）** —— 个体自己去调查。Voyager 系。
3. **观测・对话控制（OBS）** —— 看个体分别的响应 + 选择分数的时序，能停、能续。

##### 6.1 Perplexity 背书的 white-space

并行运转的 Perplexity 的 SOTA 综述（1143 行）返回了最重要的背书。

> 「**整合 online evolution + online answering 的持续运转系统**」没有明确的先行研究 = **research white-space（空白地带）**。最接近的是 MoA / Self-MoA / sequential aggregation / routing，但没有相同的。

也就是说，「停下进化、用造好的最强个体来回答」是寻常做法。「**不停下**进化、让进化中的群体本身合奏来回答」——还没有人做过。**ORCH §1.11 的差异化得到确认。**

##### 6.2 不过 Perplexity 也给了反证警告

作为 honest disclosure，我以同等分量写下 Perplexity 给的**反证警告**。

> 在 2025 年的 **Self-MoA 研究**中，**多样性并非自动占优**。单一顶级模型的反复，在 AlpacaEval 上超过异种混合 MoA 达 6.6%（quality-diversity 权衡）。

「把群体合奏起来就比单一个体强」并**非不言自明**。先行研究警告，多样性反而可能起反效果。所以 ORCH 是「用实测来证明，诚实设定 pass-bar」。我用 Agent C 和自跑 PoC #3/#4 验证了这一点。

> 🍵 **休息点**：这里是考验研究诚实度的分岔口。正想为「online 进化 + online 回答是 white-space！独创性！」而飘飘然时，Perplexity 泼来冷水「但有反证说多样性不是自动就好」。**让飘飘然的素材和冷水，在同一次调查里同时接受。**做到这一点，结论会强很多。下一节，我来揭开那盆冷水的真面目。

---

#### 7. 揭开 Self-MoA 反证的「真面目」（自跑 PoC #3 → Agent C 真实 LLM）

「多样性并非自动占优」——不是在 proxy，而是在**机制层面**揭开这个反证，是这里的高潮。

##### 7.1 自跑 PoC #3 —— 是投票，还是路由？

首先，在 proxy 里无法验证（在饱和的 fitness 下 single best 已是满分 = headroom 为零，拉不开差距）。于是我合成了**「单一个体无法满分的难任务」**（专家分散，single_best=0.5）来测。

| 配置 | best_of（routing） | majority（vote） | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant（top-k） | 0.750 | 0.500 | 3/4 |
| MoA diverse（max-cover） | **1.000** | **0.000** | 4/4 |

这里出现了**决定性的发现**。

- 多样 MoA 在 **best-of / routing 下为 1.000**（单一 best 的两倍）。**ORCH 成立。**
- **然而在 naive majority（多数决）下，多样性起反效果**（diverse = 0.000）。在各 sub-task 中，那一位 competent 的专家被无知的多数派 negate（抵消）。冗余 MoA 的 majority（0.500）反而更高。

也就是说，**Self-MoA 反证（多样性 ≠ 自动占优）的真面目，是「聚合器是投票还是路由」。**投票/平均杀死多样性，competence-aware 的 routing/gating 激活多样性。这是「有指挥的管弦乐团」与「人人随心所欲出声的喧嚣」之间的区别。

##### 7.2 Agent C 的真实 LLM 独立地给出了同一结论

然后——并行 Agent C，用**真实 LLM（llama3.2，105 次 LLM 调用，15 任务）**，与自跑 PoC #3 **独立地给出了同一结论**。

- 单一 best = **0.933**。MoA `best_of` + k≥5 达 **1.000**（+0.067）。**majority / weighted 一次都没超过 0.933。**
- diverse > redundant（多样选拔以更少的 k 更早地拾取不同 QD cell 的互补 specialist）。
- 改善**整整来自 multistep 的 1 题**（「把 5 翻倍再减 3」）。CoT 个体群一齐落掉的那 1 题，被多样选拔的异种个体解出。

> 🔑 **独立交叉验证（本文的核心）**：自跑 PoC #3（合成・专家分散）与 Agent C（真实 LLM・llama3.2），用**不同方法达成同一结论**——「MoA 只有在 competence-aware routing（best_of）下才超越单一 best / 投票达不到 / 多样性只在 routing 下才有价值」。两种方法一致，在 honest disclosure 意义上是极强的证据。

##### 7.3 最大的漏洞 —— 「真实路由器」能达到 oracle 吗（自跑 PoC #4）

这里 Agent C 指出了最大的漏洞。「best_of 是 **oracle routing**（神知道哪个个体正确的上限），而实际上『预测哪个个体 competent』的 **gate 的精度**才是瓶颈。实际投票（majority）达不到 oracle。」

我用自跑 PoC #4（真实路由器 vs oracle，20 seed 平均）来填补。

| κ（校准） | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **descriptor / specialty-router 无需校准就 robust 地达 0.90**（稳定超过单一 best 0.675，接近 oracle）。而且 **routing 键可以复用为 QD 已经计算的 behavior descriptor**——**QD 与 ORCH 共享同一描述符基础**的协同效应。
- **confidence-router 在校准 κ≥0.6 时达到 oracle。**但小型 LLM 可能校准偏弱 → **以 descriptor-router 为第一选择**（不依赖校准）。
- **majority = 0.338 确定性地不适用**（与 PoC #3、Agent C **第三度一致**）。

**结论**：Agent C 指出的「实际投票达不到 oracle」这一漏洞，**用 descriptor-routing（复用 QD 描述符）实用地填上了**。ORCH 在 proxy +（部分）真实 LLM 上端到端成立。

> 🤔 **比喻**：召集 10 位专家让他们投票，无知的多数派会抵消掉正确的专家。把数学题派给数学家——需要一个**分派的人（指挥 = routing）**。而且那位指挥的乐谱（behavior descriptor）可以复用为管理多样性时**已经算好**的东西。投票（majority）杀死专家，指挥（routing）激活专家。这就是 PoC #4 的要点。

---

#### 8. 给个体赋予「调查之力」（自跑 PoC #5）

独创性 3 轴的第二个，**具备调查功能的个体（AGENT）**。构想是让个体能在搜索空间里做沙箱只读调查。但「调查不是免费的」——计入成本后，进化会用好调查吗？

自跑 PoC #5（改变成本 λ，观察调查阈值 θ 如何进化，20 seed 平均）。

| λ | θ*（=λc, 最优阈值） | θ_evolved（进化获得的阈值） | evolved | always | never |
|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.049 | 21.46 | 21.47 | **11.70** |
| 0.3 | 0.30 | 0.476 | 21.34 | 21.26 | 21.20 |
| 0.6 | 0.60 | 0.659 | **21.24** | 21.06 | 21.21 |
| 0.9 | 0.90 | 0.888 | 21.21 | 20.85 | 21.21 |

- **进化自力获得了选择阈值 θ → λc**（= 根据情形「只在该调查时才调查」的选择性调查**涌现**）。
- **调查功能的价值显而易见**：λ=0（调查免费）时，never（完全不调查）= 11.70 = **45% 的损失**。
- **成本 λ 让「always 调查」劣化，强制选择。**AGENT-3（成本原理）成立。

honest 保留：中间 λ 处的 margin 很小（浅报酬地形），这也是抽象 proxy（真实 LLM × 知识库另当别论）。即便如此，「有成本时，选择性调查涌现」这一机制在 proxy 中被确认。

---

#### 9. 规模「质性地增加多样性」（Round 3）

最后，我用母数（群体规模）也验证了 Agent A 指出的「用容量买多样性」。用 `full_oe` 配置（novelty + std + MC + reservoir1024 + map-elites），把 pop 从 256 → 4096 扫了一遍。

| pop | gens | occupied niches | monoculture | uniq_lineages | distinct_genomes | bspread_tail |
|---|---|---|---|---|---|---|
| 256 | 5000 | 171 | 0.047 | 14 | 256 | 0.939 |
| 1024 | 3500 | 467 | 0.019 | 74 | 1022 | 1.003 |
| 2048 | 2500 | 754 | 0.009 | 188 | 2041 | 1.071 |
| 4096 | 1200 | **1219** | **0.006** | **372** | 4054 | 1.253 |

随母数规模，open-endedness **单调向上**（niches 171 → 1219 / monoculture 0.047 → 0.006 / uniq_lineages 14 → 372 / 行为展开度 bspread 也单调增）。POP-1 假说（母数增加多样性）在 proxy 中得到支持。

**honest（明示混杂）**：这里有一个诚实的陷阱。为了把 pop 提上去，我缩短了 gens（5000 → 1200）。这是**对 niche 蓄积不利方向的混杂**。即便如此仍是单调增——也就是说 **POP 效应是 robust 的下界**（本来应该更有效）。反过来说，「可能更有效」在这个实验里没能证明。这个论断仅限于 proxy mechanism feasibility。

![胜者个体的思考因子 × 记忆层热图（Genome3D）。在 real-pressure 下 c_factors 中性漂移，故此图作为认知画像的可视化供参考](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_genome_heatmap_zh.svg)

> 🍵 **休息点**：「一扩大规模多样性就增加」很直觉，但这里重要的是**「即便加入不利的混杂，仍然单调增」**这份诚实。削减 gens 通常对多样性不利。即便如此仍增加了。所以才能称为「下界」。把好结果写成「下界」而不夸张成「上界」——这也是 honest disclosure 的做派。

---

#### 10. 早晨，所有人都到达了同一个结论 —— 已确定的方策

一夜之间，**6 个自跑 PoC + Agent A/B/C + Perplexity 各自独立地收敛到同一个结论。**这就是 honest cross-validation 的威力。我们舍弃了固定尺子路线，把以下确定采用为 lldarwin v2 的核心。

##### S1. 选择核（在结构上回避饱和）

- **废除固定标量 quiz fitness**（baseline 在 1 万代饱和 + monoculture 0.9 + 多样性崩塌 = 大规模再现 12h 病理，open-ended 0/6）。
- **选择 = novelty / ε-lexicase（必须 z-score 标准化）+ minimal-criterion。** **仅靠 MAP-Elites archive 不行**（scalar_qd 也全灭）= 让选择压力本身开放端化。
- **也需要品质，所以用 QD（每 cell 品质 × 多样性）**：纯 novelty 牺牲标量品质（0.77-0.83）→ 与自适应难度（条件课程）搭配以供给品质梯度（PoC #2）。
- **谱系多样性用中性储库另行确保**（行为多样性 ≠ 谱系多样性，res256 使 uniq_lineages 1 → 32）。
- **追加 factor-subspace QD**（逐个保护语义维度的多样性，应对 Agent A 的 factor-drift 局限，PoC #6）。

##### S2. 产出方式 = 持续进化 × 现场管弦乐团（独创性的核心）

- 成果物不是单一 best，而是**让 QD archive 持续进化，在任意时点做 MoA 管弦乐团合奏产出一个答案**（ORCH；整合 online 进化 + online 回答是 white-space = 独创性，Perplexity 确认）。
- **聚合必须是 competence-aware routing/gating（指挥），而非投票**（自跑 PoC #3/#4 + 真实 LLM Agent C 三重一致）。
- **routing 键复用 QD 的 behavior descriptor**（descriptor-router 不依赖校准、接近 oracle 的 0.90）= QD 与 ORCH 共享同一描述符基础（设计的节约）。

##### S3. 个体 = 具备调查功能的 agentic 个体（分阶段引入，已 proxy 验证）

- 在搜索空间里仅做沙箱只读调查（实际 I/O 在经 Approval Bus 单向昇格后）。调查计入成本。
- **已 proxy 验证（PoC #5）**：成本 λ 让「选择性调查」涌现。AGENT-3（成本原理）成立。真实 LLM × 知识库是下一阶段。

##### S4. 观测・对话控制（已实现 = 全运行标配，Agent B 完成）

- 响应日志 / 个体分数时序查看器 / lineage 复原（进化系 886 测试绿）。step/pause/resume 计划在下一阶段接线。
- Agent B 的 lineage 复原，解决了在 12h 数据中「**全是 ?**」的谱系显示，把 champion 谱系 gen70 → gen59 解出 12 hops。缺失不捏造，明示为 `lost@genN`（根因 = 父 ID 单靠 snapshot 或 winners 任一都无法追溯）。观测基础正是 honest disclosure 的根基。

##### 自跑 PoC #6 —— 用 factor-subspace QD 应对 Agent A 的局限

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

对语义维度（factor）另行施加 novelty，把语义维度多样性的损失几乎减半（50% 损 → 32% 损）。在 proxy 中实证了应对 Agent A 的 factor-drift 局限的有效手段。honest：并非完全固定而是残存 68% = 残余 drift 需并用中性储库或加强 factor 权重。

---

#### 11. 教训（作为 honest disclosure 留存）

- **连真实 LLM 都饱和了。**即便把眼镜从 proxy 换成真实 LLM，只要尺子固定，gen5 就是满分。
  「用真实 LLM 就会进化」是**谎言**。问题在于造尺子的方式。
- **单靠加 archive 救不了。**「持有多样性储库就能守住多样性」是错的。
  scalar 选择即使加上 QD archive 也全灭。**能救它的是选择压力的开放端化本身。**
- **多样性并非自动就好。**Self-MoA 反证的真面目是「投票还是 routing」。
  有了指挥（competence-aware routing）多样性才成为价值。投票杀死专家。
- **独立交叉验证使结论更强。**自跑 PoC（合成）、Agent C（真实 LLM）与 Perplexity（文献）
  分别收敛到同一结论，正因如此才可信任。同一个脑袋的结论共享同一种偏见。
- **proxy 仅是 mechanism feasibility。**本文的 PoC 群验证的是「机制是否运转」，而非「真实 LLM 一般能力提升」的主张。一旦越过这条界线，研究就成了谎言。
- **用不了的工具（Codex）也记下。**不只成功，哑弹也要诚实记录。

简言之——**「一旦眼镜（评价）饱和，无论怎么打磨淘汰器都无力。」**所以把打磨的对象，从淘汰器、从 LLM，转移到**评价本身的开放端化**。这就是一个通宵的结论。

> 🍵 **休息点**：在 #25 我决定「曝光失败」。在 #26 设计篇我造了「不聚合的淘汰器」。而这一次，真实 LLM 教会我「那还不够，因为尺子是固定的」。**失败孕育下一个设计，那个设计的局限又孕育下一个。**这就是连载的脊梁。花哨的「靠进化 AI 变聪明了！」我一次都还没写过。因为还没凑齐能写它的根据。凑齐时，才会动笔。

---

#### 12. 结论

- 真实 LLM 12h 运行是「诚实的不及格」——不全灭但不累积的 filtered random search。真因是固定尺子的饱和（用真实 LLM 实证了 #25 的洞见）。
- 一夜的分布式调查（6 个自跑 PoC + Agent A/B/C + Perplexity）独立地收敛到同一结论 = **honest cross-validation**。
- 已确定方策：**S1 开放端的选择核**（novelty/lexicase + std + MC + QD + 自适应难度 + 中性储库 + factor-subspace QD）/ **S2 持续进化 × routing-MoA**（white-space 独创性，是指挥而非投票）/ **S3 agentic 个体 + 成本**（选择性调查的涌现）/ **S4 观测**（已实现）。
- 所有要素均已在 proxy /（部分）真实 LLM 上背书。残余课题是「向真实 LLM 阶段接线」「factor-subspace QD 实现」「scale-up」。核心策略已确定。

造出好部件，不聚合地捆绑，用真实 LLM 确认饱和，再向开放端的选择重建。当 6 路独立验证到达同一结论时，才终于能说「方策定了」。本文正是 #25 中预告的「**眼镜蒙了，淘汰也无力**」那一回——诚实曝光真实 LLM 让眼镜蒙住的那一刻（饱和），承担起 Goodhart's law 与 proxy 的局限，然后向开放端重建。下一步，是把这套已确定的方策落到代码的**实现阶段**。

---

#### 13. 相关

- 连载 #24-05「群体学习的 AI」—— 派生群体进化的框架（本文的前提）
- 连载 #24-08「造眼镜」—— lleval（测量的一侧）
- 连载 #25「只剩下弗里斯顿和我」—— monoculture 的 honest disclosure（本文的动机）
- 连载 #26（设计篇）「只靠眼镜测量并不会进化」—— 淘汰器 lldarwin 的设计与 Stage1/1.5/2 实测（本文的姊妹篇）
- 先驱论文（2026-05-27, date of record）「Continuously-Evolving Populations as Live Orchestrated Ensembles」—— 把本文方策以学术形式形式化的防御性公开（FullSense 公开仓库 `docs/papers/`）
- 相关 memory：[[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

## 4. 進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28（lldarwin 実装編）

### 让"指挥者"指挥不断进化的 AI 群体合奏来作答 — llive 的乐团式进化, 以及治好饱和的 3 个装置 #28

> 📚 **连载导航（lldarwin 弧线）**: #24-05 群体进化 → #25 monoculture 的失败 → #26 设计篇 → #27 通宵的决断（climax）→ **#28 本文（实现篇）**。※ 各篇文章也可单独阅读。

> **概念 hook**:
> 不是对 1 个聪明的 AI 反复发问, 而是 **让一大群略有不同的 AI 持续"进化", 在需要答案的那一刻, 由指挥者挑选合适的成员合奏（乐团）汇成 1 个答案**。
> ——这就是 llive 现在所追求的形态。`llive` 不是"LLM 本身", 而是"套在 LLM 周围的认知 OS"。在其中, 让 **群体不绝、不偏、持续成长** 的, 就是这次打磨出的进化引擎 `lldarwin`。
>
> 在前作 #27 中, 我们通过真实 LLM 的 12 小时运行确认了这样一个病症:"评价（尺子）一旦贴死在满分上, 进化就会停止, 退化为仅仅带筛子的随机搜索"。于是定下方策:"无论怎么打磨淘汰器都是徒劳。**要让评价本身成为开放端**"。
>
> 这次我们 **实现** 了该方策。而在 proxy（合成尺子）之上, **best 分数没有贴死在满分上, 一直上升到最后**。

---

#### 0. 三行剧情梗概（落语的"开场白"）

- **卖点确定了** — llive 的北极星是"**连续进化 × 现场乐团**"。在不停止持续进化的群体的同时, 在任意时刻用 competence-aware routing（指挥者）合奏汇成 1 答。这是先行研究中的 **white-space（空白地带）**。
- **实现了治好饱和的 3 个装置** — ①对语义维度逐个保护的 factor-subspace QD ②把成果不存为"单一 best"而存入多样性 archive 的 MAP-Elites ③让尺子跟随群体的适应难度。由此搭好了"奏者（多样的个体）不绝"的基盘。
- **在 proxy 上验证了规避饱和** — 把 lldarwin-v2 跑 10 代后, best 从 0.80 → **0.92 不贴死地上升**。多样性 archive 填满了 21 个 cell。**不过这是 proxy, 并未测量真实 LLM 的能力**（honest）。

总之就是 **不是"聪明的 1 体"而是"多样的一大群 × 指挥者"**。为此的"让奏者不绝的装置"就是这次的实现。

---

#### 1. llive 是什么（致初次接触的读者）

`llive`（读作 liv。L 有 2 个）是 **自我进化型、模块化记忆的 LLM 框架**。它是名为 FullSense 的伞形品牌的一员, 兄弟有 `llmesh`（本地 LLM hub）和 `llove`（终端 dashboard）。这 3 者是独立 OSS, 但组合起来就成为 1 个世界观。

用 1 行概括 llive 的思想就是"**不是 LLM 本体, 而是套在 LLM '周围' 的认知 OS**"。把 4 层记忆、6 阶段的 loop、承认 bus（Approval Bus）、TRIZ、10 个思考因子……这些"思考的脚手架"搭在 LLM 的外侧, 使得 **即便是同一个 LLM 也能进化其行为**。

承担这个"进化"的, 就是这次的主角 **`lldarwin`**（达尔文）。角色分工如下。

- **lleval（眼镜）** = *测量* 个体（评价）
- **lldarwin（淘汰器）** = 把测出的差异 *转换* 为"谁存活、谁留下后代"（选择压）

而骑在两者之上的北极星, 就是接下来的"乐团"。

---

#### 2. 卖点 = 连续进化 × 现场乐团（独特性的核心）

普通的 Mixture-of-Agents（MoA）是向 **固定的** 多个模型抛出同一个问题, 再聚合答案。llive 瞄准的是那再往前的一步。

> **不停止地让群体持续进化（online evolution）, 在需要答案的那一刻（online answering）, 由指挥者挑选"针对这个问题用这些奏者"合奏汇成 1 答。**

这种"online 进化 + online 回答的整合", 据我们调查是 **没有明确先行研究的 white-space**（在 #27 中让 Perplexity 翻阅文献确认过）。与之相近的有 MoA / Self-MoA / sequential aggregation / routing, 但"让持续进化的群体本身现场合奏"的形式则遍寻不见。

在这里发挥作用的是在 #27 得到的 2 个诚实发现。

1. **聚合不能是"投票", 而必须是"指挥者（competence-aware routing / gating）"。** 自我 PoC 和真实 LLM 验证三重一致: 在有 headroom（提升空间）的任务上 `best_of`／`routing` 胜过 `single`（单模型迭代）, 但 **`majority`（多数决）反而适得其反**。这也是我们对 2025 年 "Self-MoA"（多样性并非自动占优）的回答。
2. **指挥者的判断键可以挪用多样性 archive 的 "behavior descriptor"。** 也就是说后述的 QD（Quality-Diversity）和指挥者可以 **共享同一套记述子的根基**。

——不过, 乐团本体（指挥者＝router 的实现）还在后头。**这次实现的是其前一步:"搭建足以合奏的、多样且不绝的奏者群体"的基盘。**

---

#### 3. 为什么"奏者会断绝" — 名为饱和的病（#25〜#27 的复习）

乐团需要的是"**个性各异的奏者一大群, 持续不绝地存在**"。然而若朴素地进化, 这会崩溃。

- #25: 跑 500 代后, 世界上只剩下"我和弗里斯顿"（**monoculture**）。
- #27: 用真实 LLM(llama3.2) 跑 12 小时后, gen5 时 best 贴死在 1.0, 65 代毫无进展。**不会全灭但也不会累积** ＝带筛子的随机搜索。

真因两者相同。**人为固定的尺子（评价函数）一旦贴死在满分上, 全体就同分, 选择压消失, 之后就靠遗传漂变随意偏移**。眼镜（lleval）一旦饱和, 无论怎么打磨淘汰器（lldarwin）都无力——这就是 #27 的结论。

所以要改变打磨的对象。转向"让尺子动起来""结构性地守护多样性"。具体就是接下来的 3 个。

---

#### 4. 实现的 3 个装置（lldarwin v2 / Phase 1）

> 设计的口号是"**不发明新算法**"。Phase 1 就是把 llive 内已经积累的部件（ε-lexicase / NoveltyScorer / MAP-Elites / 中立贮藏库）**合成、配线** 成已确定方策 S1 的形态。用 `--selection lldarwin-v2` 即可一并开启。

##### ③ 适应难度 — 让尺子跟随群体

`AdaptivePercentileGate`。把各评价轴的"最低线（minimal-criterion）"每一代 **重置为群体分数分布的指定百分位（例: 后 40% 点）**。群体提升, 最低线也自动上抬。设为 `ratchet`（单调非减）的话, 即便一时下探基准也不会松动。

由此就给"固定尺子在满分处饱和"的病盖上了盖（PoC 中固定难度停滞在能力 0.627 → 适应难度上升到 0.952）。即便在全体都跌破最低线的乱世代, 淘汰器也会无视 gate 以避免全灭（fail-open 防护）。

用落语来说, 就是 **学生进步了就把及格分也上调的老师**。不会让其拿了满分就到此为止。

##### ① factor-subspace QD — 逐个守护语义维度的个性

`FactorSubspaceNovelty`。novelty 探索能保持"群体整体的多样性", 但在巨大的潜在维度之下,"**有意义的维度（思考因子）的多样性**"会不知不觉地萎缩（factor drift）。

于是, **仅在** 思考因子的 **子空间** 上另行测量 novelty, 并与整体 novelty 混合。在 PoC 中, 这使语义维度多样性的目减几乎减半（retention 49.5% → 68.1%）。

> 诚实的改良点: 原本的 PoC 是"把生距离各加 0.5", 但由于各子空间的距离尺度不同, 在实现中改为 **先把各自 z-score（标准化）再混合**。这是为了公平地混合"整体的合唱"和"各声部的个性"。

用奏者来说, 这是让 **第二小提琴不会被第一小提琴吞没消失** 的装置。

##### ② MAP-Elites — 把成果存为"多样性的地图"而非"1 个冠军"

`run_persona_evolution(map_elites=True)`。每一代把全部个体投入 MAP-Elites archive。这不是"最高分的 1 体", 而是 **按行为的坐标、在那个格子里保留最优个体** 的地图（QD archive）。填了新格子也不会消除既有格子 ＝ **多样性不会结构性崩溃、archive 单调地成长**。

这直接就成为乐团的 **奏者目录**。指挥者将来会从这张地图中挑选"契合这个问题的坐标的奏者"合奏——QD 和 routing 共享同一记述子的、那个 #27 的设计在这里发挥作用。

实现上 **不扩展个体的格式**, 而是从既有 genome 的思考因子导出坐标（descriptor）的 additive 配线（为的是不破坏基盘的后向兼容 900+ 测试）。记述子的正式设计（高维的缩约等）作为将来 Phase 的课题留有余地。

---

#### 5. 结果 — 在 proxy 上确认"不饱和的进化"

这是把 `lldarwin-v2`（上述 3 个＋ novelty ＋中立贮藏库全部开启）用 proxy 尺子跑 16 个体 × 10 代的实测。

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21（多样性的地图填满了 21 个格子）
```

- **best 没有贴死在满分上, 0.80 → 0.92 一路上升到最后。** 在 proxy 阶段摆脱了 #27 中看到的"gen5 时 1.0 饱和→固定"的病理。这是适应难度让"尺子"跟随群体的征兆。
- **多样性 archive 填满了 21 个 cell** ＝应当合奏的"个性各异的奏者"的目录开始成形。
- 进化系的自动测试 **879 件＋新增测试全部 green**, 无回归。

---

#### 6. honest disclosure（请不要跳过这里）

结果越好越要怀疑其内幕, 这是 FullSense 的做派。

- **这是 proxy。** 个体不是真实 LLM, 而是 llive 的 genome（思考因子的代理）。这次测量的是"能否同时对多个独立的弱轴施加选择压、并按轴维持专家"这一 **机制的可行性（mechanism feasibility）**, 而 **不是 production 的 LLM 能力**。真实 LLM 评价是下一个 Phase。
- **factor-subspace 并非完全保护**（retention 68%, 其余漂移）。需要并用中立贮藏库以及强化 factor 权重。
- **幕后的诚实**: 这次实现过程中, 自动 commit 钩子在每次编辑时堆积了多达 49 个"编辑前"快照, 历史变得杂乱。最后 squash 成 1 个有意义的 commit 加以整理（公开 OSS 一侧）。反过来, 也确认了含有内部战略的 fork 如预期那样仍保持在本地、未被暴露。

---

#### 7. 接下来要做什么

进化引擎（让奏者不绝的基盘）在 Phase 1 中成形了。接下来是乐团本体, 以及从 proxy 到实物的过渡。

1. **Phase 2 = 真实 LLM 配线。** 以本地（localhost ollama）的真实 LLM 为对象, 用真实评价验证适应难度、factor-subspace QD、MAP-Elites。在 proxy 上看到的"规避饱和"是否在真实能力上也会发生。
2. **指挥者（router）的实现。** 用挪用 QD archive 的 descriptor 的 competence-aware routing, 实际运行"让进化中的群体现场合奏汇成 1 答"。能逼近 `best_of` 的 oracle 到何种程度。
3. **提升规模。** 群体 256 → 4096, 潜在维度的扩容。验证容量假说（越大 niche 越多）。
4. **交互式连续运行。** 能以 step / pause / resume 窥探长时间运行的驾驶席（CKPT-1）。

---

#### 8. 在此稍歇（休息点）

到此为止,"**llive 以什么为卖点**"传达到了吗。

- 不是聪明的 1 体, 而是 **不断进化的多样群体 × 指挥者的合奏**。
- 为此, 做出了一个 **让奏者不绝、守护个性、持续成长** 的进化引擎。
- 在 proxy 上治好了饱和。**接下来是真实 LLM 和乐团本体。**

在后续的"真实 LLM 篇"和"乐团篇"中, 我们会让大家看到 proxy 的承诺是否成真。——感谢您一路相伴至此。

---

#### Series Navigation

- 连载导航（lldarwin 弧线）: #24-05 群体进化 → #25 monoculture 的失败 → #26 设计篇 → #27 通宵的决断 → **#28 本文（实现篇）**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

## 5. 「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #29（Goodhart の法則と proxy fitness の限界）

> 📗 **赶时间?** 本文有通俗易懂版。
![眼镜饱和则选择压无力 — 反证四格 #29](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q29_4koma_zh.svg?v=2)
### "镜片饱和时,选择压力无能为力" — 用反证锤炼进化设计 #29(Goodhart 定律与 proxy fitness 的极限)

> **概念 hook**: 在 #25 我暴露了失败,在 #26 我设计了淘汰器"lldarwin"。普通的连载接下来会说:
> "修好了! 可喜可贺,完!" **但不这么做,正是 FullSense 的 honest disclosure**。
> 本文刻意做成**向自己的设计抛出反证**的一回。主题是一句在进化计算和机器学习两边都奏效的话——
> **Goodhart 定律(当一个指标成为目标时,它就不再是好指标)**。
>
> "只要把 LLM 的弱点当作 fitness,进化就会自动克服它"——我亲自去给这种天真的乐观泼冷水。
> 而且这一次,**我把自己曾经犯下的"事实误认"作为活标本放上解剖台**。

---

#### 0. 三行概要

- **镜片(fitness)一旦饱和,无论加上多么高级的选择压力(lldarwin),淘汰都无能为力**(#25 的真正教训)。
- **用 proxy fitness 测量 LLM 弱点时,进化出来的不是真能力,而是"hack 指标的表面策略"**(Goodhart 定律)。
- 结论: 我把 lldarwin 的价值主张**限定**为 **(a) proxy 只是 mechanism feasibility (b) 实 LLM/VLM 评价才是本质 (c) 多样性的地图化**。这就是诚实的界线。

而本文还有一行隐藏的主角。

- **我自己曾经把"行为多样性""谱系多样性""实 LLM 智能多样性"混为一谈**。我把这个自我反证
  放在反证回的核心。这是对"它成功了"该如何怀疑的现场演示。

---

#### 1. 重申 honest disclosure — 结果越好越要怀疑

在 #26 我写道"在 PoC 部署中,行为 monoculture **在全部条件下改善到了 0.05(≪0.8)**"。
这是**事实**。并非夸张。

…但若在此挺起胸膛"搞定了,monoculture 消灭!"就此收尾,**就违背了我在 #25 立下的誓言**。

> 出现异常漂亮的结果时,在自以为获胜之前先怀疑其内訳([[feedback_benchmark_honest_disclosure]])。

连载 #25 的通奏低音是这样的——"**异常漂亮的结果不是胜利,而是警报**"。
对于"跌破 0.8 即达成 OE-3"的基准,**0.05** 实在太漂亮了。0.05 这个数字,
不该当作庆祝的号角,而必须当作**警笛**来听。

那么就让警笛响起来吧。该问的问题只有一个。

> **这是测量了什么的 0.05?**

先说答案,0.05 是"**proxy 评价中的行为 monoculture**"。
这是"genome 的行为代理(behavioral surrogate)"的集中度,
**并非实 LLM 智能的多样性**。在这里混淆,就会重蹈与 #25 完全一样的覆辙。

而我诚实地坦白。**我曾经在这里混淆过。**稍后在 §3,我会拿出那个"现行犯"的证据。

> 🍵 **休息点(90 秒)**: 本文说到底就是"**给自己挑毛病的文章**"。
> 我希望这一回能让读者诸君观察"在成功报告的背后,作者在怀疑什么、怀疑到什么程度"。
> 它走的是 SNS 上爆红的"进化了一个 AI,最强○○诞生了!!"的**恰好相反**的路。不会热闹。
> 但正是这种不热闹的诚实,半年后才会奏效——这是我的赌注。请喝杯茶吧。

---

#### 2. 反证 1 — 对饱和的镜片,任何选择压力都无效

##### 2.1 再说一次 #25 的真因

#25 的真因是"**best_score 从第一代起就饱和在 1.0 → 选择压力为零 → 遗传漂变(genetic drift)**"。
若所有人都是满分,选谁都一样。选择就不是"留下优秀者",而变成"掷骰子"。
结果,凭运气增长的谱系仅凭运气固定下来,8 个谱系崩溃为 2 个(furuse-kazufumi + friston)。

在此,我放下成为进化弧线核心的反证。

> **把 lldarwin(无论 ε-lexicase、QD 还是 novelty)照原样插入饱和的 eval,也修不好。**

为什么。因为淘汰器的每个部件,都以"**存在差异**"为根本前提。

- **ε-lexicase** 以"每个轴上存在差异"为前提。**若所有轴都是满分,无论分成几个轴,差异都是零**。
  即便分成 100 个轴,若全是 1.0,也只是排出 100 个"平局"。
- **QD(MAP-Elites)** 以"behavior 描述子存在方差"为前提。**若所有个体行为相同,cell 就只有 1 个**。
  即便做出地图,若所有人都站在同一格子上,地图就变成一片空白的一格。
- **novelty** 以"与过去 archive 的距离"为前提。**若所有人都收敛到同一点,所有人的距离都是零**。
  想用新颖性来奖赏,也没有谁是新颖的。

也就是说,图式化后是这样。

```
坏掉的镜片(fitness 饱和) + 高级的淘汰器 = 结果还是坏的
```

##### 2.1.5 实证 — 在记忆任务中,"地板"与"天花板"杀死了选择压力(Step C, 2026-05-30)

这个反证,后来在 llcore 的 Step C 实验(纯 CPU)中**作为实数据被复现**。让进化(MAP-Elites)和素朴搜索去解 2 种标准记忆任务,结果如下:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="Step C 的两个结果(地板与天花板)" width="640">

- **delayed_parity(XOR)= 地板**: 全部 method 都是 R²≈0(基质原理上无法求解)。谁都爬不上去=不出现差异。
- **flip_flop(只是记住)= 天花板**: 全部 method 都是 R²≈0.95(太简单,全员都到达)。**这正是"饱和的镜片",这里选择压力同样无能为力**。

作为参考,③(选择)只有在存在"越过假山顶、虽欺骗但可通行的坡道(欺瞒 corridor)"时才奏效:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/deceptive_corridor.svg" alt="欺骗地形与进化(③奏效的状态)" width="640">

Step C 的结论干脆是 **N/A(在此基质上无法测量③的有无)**。而且在 draft 阶段我**写过头了**"③不必要",多视角的 adversarial 验证抓住"因天花板效应而非诊断、检出力不足(δ=+0.33 是 medium 但 p=0.15 为 inconclusive)"并将其降级——§3.2 的"自我反证",在这里也照样发生了。

##### 2.2 "#25 修好了"只对了一半

这是从 #25→#26 容易被忽略的反证。**#25 修好,并非"仅仅"靠 lldarwin 的功劳**。

实际上,**镜片一侧的修正在先**。

- **per-dim z-score 标准化(STD-1)** — 把每个轴的方差对齐,不让"全轴都还算高的无特征个体"占优。
- **中央一致排除(SEL-1)** — 所有人都输出相同值的轴对选择没有贡献,故从 case 中剔除。
- **描述子的低维缩约(DESC-1, JL 投影)** — 避开 QD 的维度诅咒,让 cell 不至于空空如也。
- **真因 criteria 的排除** — 把 `factor_score`(max-archetype 的单一标量 = argmax,违反 SEL-2 = best=1.0 饱和的真因)和
  `nearest_persona_idx`(顺序无意义的类别 index)从 ε-lexicase 的 case 中剔除。

这项"打磨镜片"的工作在**先**,淘汰器才头一次奏效。
若顺序反过来,无论载上多么高级的 lldarwin,在饱和的镜片面前都是无能为力的。

> **不修"测量"只把"淘汰"做得高级,是徒劳。**

这不仅限于进化计算,而是对机器学习评价设计整体都奏效的教训。
当排行榜的分数饱和时,在把模型做得更高级之前,先怀疑**benchmark 是不是坏了**。

> 🤔 **比喻(漫才风)**:
> 装傻:"把评委从 3 人增加到 100 人,可是给所有人看同一张满分答卷,结果还是一样。"
> 吐槽:"那不是评委的事,是**答卷(测试)坏了**啊! 给 100 个人看同一张满分能变出什么来!"
> 装傻:"那把评委增加到 1000 人……"
> 吐槽:"**增加的方向反了**!! 先把题卷给我修好!!"

##### 2.3 职责分离 — 缺了哪个进化都会坏

把镜片(测量)和淘汰器(淘汰)的职责分开,就成了这样。

| | 镜片正常 | 镜片饱和 |
|---|---|---|
| **淘汰器高级(lldarwin)** | ◎ 进化转起来(在 #26 达成) | ✗ 无能为力(#25 的陷阱) |
| **淘汰器素朴(Tournament)** | △ 能转但多极性弱 | ✗ 崩溃(#25 的出发点) |

值得关注的是右下和右上。**只要镜片饱和,淘汰器的高级就救不了右边那一列**。
进化的成败,在"淘汰器的聪明"之前,先由"**镜片是否映出差异**"决定。
这就是反证 1 的结论,也是把 #25 的"真正教训"进一步精密化的说法。

来看看这个"镜片一糊,淘汰也崩"的结论在实测中的样子。下面是 baseline(无 novelty、素朴选择压力)的
适应度与多样性的推移。临近末尾,可以看到多样性在崩溃。

![baseline: 末尾的多样性崩溃](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_zh.svg)

> 🍵 **休息点(90 秒)**: "先打磨镜片再淘汰"——顺序重要,这是个朴素的故事。
> 朴素,但跳过这一步就会蒸发半年(我蒸发掉了)。从下一节起是本文的正题,
> **Goodhart 定律**。从这里开始话题会有点黑。换成咖啡也行。

---

#### 3. 反证 2 — Goodhart 定律: hack proxy fitness 的进化

##### 3.1 最重大的风险

这是设计文档(LLDARWIN_DESIGN.md §7.1)明确写为"**最重大风险**"的一点。

> **把 LLM 的弱点当作 proxy fitness 时,进化出来的不是真能力,而是"hack 指标的表面策略"。**

进化计算是**寻找最大化给定指标的"近路"的天才**。
当人类递出一个"自以为用它来测量真能力"的 proxy 时,进化非但不去获取真能力,
反而**必然发现只满足 proxy 的表面策略**。而且乐此不疲、高效地。

具体会发生什么样的 gaming(指标 hack)?把设计文档里已接受的极限照原样展开。

| pressure(LLM 弱点) | 可能发生的 gaming(指标 hack) | 为何不是真能力 |
|---|---|---|
| typo_robustness | 只是背下特定 typo 模式并替换 | 对未知 typo 无能为力。没有获得噪声耐性 |
| polysemy_wsd | 利用测试分布的启发式 | "返回最频 sense"等统计近路。不是语义理解 |
| multistep_robustness | 只生成有说服力的推理"痕迹" | 排出像模像样的中间步骤,实际并未推理 |
| calibration | 把自信度操纵到中庸以降低 ECE | 全部说"自信度 50%"就能降低校准误差。不是校准能力 |

最后 calibration 的例子最好懂。
当你用 ECE(期望校准误差)来测量"能否恰当估计自信度"时,进化会找到
"**对所有问题都回答'自信度正好在正中'**"的策略。
ECE 急剧下降。但那个模型一样都没校准。只是变成一个吐中庸的机器人。

> **当一个指标成为目标时,它就不再是好指标(Goodhart 定律)。**

这在 LLM 研究中也有实例。在 GSM8K 型 benchmark 上只有分数上升而不泛化的
**benchmark overfitting**,正是这个结构。过度相信排行榜数字的人,一次次被绊倒。

##### 3.2 我自己的"现行犯"— 自我反证

在此,我把 §1 预告的"混淆现行犯"放上解剖台。不加遮掩地写。

我起初在 TODO 里这样写道——"验证**在重跑中冈洁、格罗滕迪克谱系是否存活**"。
然后在 PoC 中看到 monoculture **0.05** 这个漂亮的数字,"哦,谱系多样性是不是也改善了?"
**一瞬间差点误以为如此**。

这就是混淆。正如我在正本(lldarwin_stage1_results §3)所写,`poc_evolution_env.py` 的作者注释
(我自己写的注释)本身就明确否定了那个混淆。

> "monoculture = **BEHAVIORAL** concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is **behavioral spread**. lineage_fixation … to keep it <1 needs
> **QD niching on lineage / PERSONA-FX, not pure novelty**"

整理一下,我差点混淆的 3 个"多样性",完全是不同的东西。

1. **行为多样性(behavioral diversity)** — genome 空间中行为的扩散。用 `diversity_l2` 测量。
   **novelty 奏效的指标**。改善到 0.05 的就是它。
2. **谱系多样性(lineage diversity)** — 哪些 founder(冈洁、格罗滕等)存活下来。`founder_counts`。
   **用 novelty 在结构上无法改善**。novelty 和 lexicase 都只能"保存既有个体",
   没有让一度灭绝的谱系复活的机构。所以在中立漂变(Kimura)下走向 monoculture
   **在理论上是正常的**。不是崩溃,而是预期之内。
3. **实 LLM 智能多样性(real intelligence diversity)** — 实模型是否真的拥有多样的聪明。
   **用 proxy 完全测不出来**。是 Stage2 的实 LLM 评价所承担的领域。

也就是说,"改善到 0.05"的真身是 **(1) 仅行为多样性**。(2) 和 (3) 都与那个数字无关。
我一瞬间差点想"谱系也改善了?",是因为**看到 (1) 就草率断定 (2)/(3) 也变好了**。

这正是 Goodhart 定律的设计者一侧版本。
看到一个指标(行为多样性 0.05),就**人为擅自地解释**它没有测量的另一种能力(谱系存活、实智能)也变好了。
不仅 proxy 与真能力背离,**读 proxy 的人类的解释也一并背离**。
在反证回里暴露这个,很痛。但若不暴露,就不是 honest disclosure。

##### 3.3 用对比来看"测量了什么的 0.05"

只用言语难以传达,所以**用 2 张 SVG 来对比"测量了什么"**。

首先,**行为多样性确实改善了**(这是事实、无夸张)。下面是中立贮藏库 OFF 的谱系支配 stream。
最终**崩溃为 furuse 71% / friston 29% 的 2 个谱系**。即便行为多样,谱系也是这般。

![reservoir OFF: 崩溃为 2 个谱系](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_zh.svg)

而下面是**加入谱系一侧的对策(中立贮藏库 ON)之后**。**全部 8 个谱系并存**
(millidge / von-neumann / oka-kiyoshi / grothendieck … 存活)。

![reservoir ON: 全部 8 个谱系并存](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_zh.svg)

这 2 张图的对比,是本文的心脏。
**同样是"0.05 的行为多样性",左边(OFF)谱系崩溃,右边(ON)谱系并存。**
也就是说,0.05 这个行为多样性的数字,**对谱系怎样了只字未提**。
加上另一个机构(lineage-niched QD / 中立贮藏库)之后,谱系才头一次得救。

"测量了什么的 0.05"——答案是"**只有行为**"。谱系不用另一副镜片就看不见。这就是诚实的答案。

##### 3.4 有对策,但问题不会消失

设计里织入了 Goodhart 对策。

- proxy **限定于 mechanism feasibility 验证**,不主张 production 能力。
- **以实 LLM/VLM 评价(Stage 2)为本质**。
- 用 **neutral shadow 对照(Bedau)** 怀疑表面的改善(与只有中立变异的 shadow 集团相比,
  确认选择是否真的奏效)。
- 用 **down-sampling** 每代扰动 case + 用 **OOD 轴**抵消过拟合。

> 🍵 **休息点(90 秒)**: "既然有对策,不就没问题了?"——不,这才是关键。
> 对策只是**推迟背离**,而**proxy 不是真能力这一事实并不会消失**。
> 这就像感冒药能压住症状,却消不掉病毒本身。所以"通过 proxy 让 LLM 变聪明了"这种话,我**打死也不说**。
> 因为一旦说出口,半年后我就看见自己出尽洋相了。来一杯茶。

---

#### 4. 反证 3 — 设计者依赖性:"多样性的方向"是谁决定的?

##### 4.1 一个元层面的怀疑

ε-lexicase 的 case、QD 的 behavior 描述子、novelty 的距离尺度、minimal-criterion 的基准值——
这些全都是**由设计者(我)决定了"多样性的方向"**。

也就是说,lldarwin 产生的多样性是"**在设计者设想的轴之内的**多样性",
而不是生物进化级别的**未设想涌现(unanticipated emergence)**。
正如 Taylor et al. (2016) 作为 open-endedness 的极限所指出的,
"在人类定义的尺度之内多样"与"跃出定义之外",是完全不同的两回事。

例如,在我用 `diversity_l2`(genome 空间的 L2 距离)定义"行为多样性"的那一刻,
进化就会朝"**L2 距离变大的方向**"多样化。但那是在我画出的坐标轴之上的多样性,而
在我想都没想过的轴(比如"幽默感"或"沉默的用法")上的多样性,
**本来就不在测量对象之内**,所以即便诞生了我也察觉不到。

> 🤔 **比喻(金鱼池)**:
> 捞金鱼摊的老板决定"挑选让红金鱼和黑金鱼都留下"来捞。
> 确实红的黑的都留在池里。多样性,达成。…可是,即便那池里突变出一条**绿金鱼**,
> 老板的网只看"红还是黑",绿的就**没被评价而漏捞了**。
> 设计者所定轴之外的涌现,从一开始就不在视野中。这就是设计者依赖性。

##### 4.2 接受 — 限定能赢的轴

那么怎么办。**不主张未设想涌现**,这就是诚实的答案。

lldarwin 瞄准的是"**无可验证性的多样性的地图**"(差异化轴 DIFF-1),
不主张 strong / unbounded open-endedness(与 SCOPE 一致)。
说"我在搞人类未踏的涌现!"很气派,但那会是谎言。
**限定能赢的轴**——把价值收窄到对认知风格、文化风格这类"无可验证性的多样性"进行地图化。
这就是 lldarwin 能诚实主张的范围。

舍弃气派主张的勇气,也是 honest disclosure 的核心。

---

#### 5. 反证 4 — minimal-criterion 与 QD 自身的 trade-off

淘汰器的每个部件,也都有各自固有的弱点。把设计文档 §7.1 已接受的极限逐一解说。

##### 5.1 minimal-criterion 的停滞⇄崩溃

minimal-criterion(最低基准 gate)是"不让不满足基准的个体繁殖"的机制,但
**基准的高度本身就是 trade-off**。

- **基准低** → 几乎全员通过 → 选择压力为零 → **停滞**(与 #25 的饱和同一结构)。
- **基准高** → 几乎没人通过 → **全灭**(有实证。全员在 gate 落选则做不出下一代)。

温水还是地狱。**对策**: 把 criterion 不设为固定值,而**按集团分位点自适应**(例: 落选下位 30%)。
此外加入若全员 fail 就忽略 gate 的安全阀(`MultiPressureSelector` 已实现)。

##### 5.2 QD 的维度诅咒 + archive 饱和

QD(MAP-Elites)用 behavior 描述子切分 cell,但**描述子若高维,大半 cell 会变空**
(维度诅咒)。而且长期运转后全部 cell 被填满,新颖性触顶(**archive 饱和**)。
这是在人工生命的经典 Avida / Tierra 中也观测到的现象。

**对策**: 把描述子**缩约到低维**(DESC-1, JL 投影) + 用 **Bedau 统计监视饱和**,
把"**饱和=失败**"如实记录(不要把饱和便宜行事地解释为"已经探索殆尽的证据")。

##### 5.3 lexicase 的规模极限

ε-lexicase 在 case 数增加时**计算成本增大**,而且**因噪声实质上变成随机选择**。
case 太多时,胜者由碰巧排在顺序最前的 case 决定,选择就接近掷骰子。

**对策**: 用 **down-sampled lexicase**(每代只用 case 的子集)削减成本 + 扰动环境。

##### 5.4 trade-off 在实测中"看得见"

这些 trade-off 并非纸上空谈,而是**在实测中显现**。
改变中立贮藏库的"再投入频率(reinject_interval)"的 sweep 就是个好例子。

| interval | named 谱系存活 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**(每代) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84(最大)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**非平凡的发现**: 行为多样性(diversity_l2)并不随 interval 升高而单调增加,而是**在 interval=5 处达到峰值**。
10/20 反而下降。原因是——把谱系放任太久(升高 interval),
来自贮藏库的多样性注入减少,且少数谱系固定下来,diversity 也不再增长。
恰到好处的"放任程度"在正中——这是个非线性的世界。

![再投入频率 sweep: diversity 在 interval=5 达峰(非单调)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_zh.svg)

运用指针就成了这样——**若把谱系保持放在第一位,interval=1(8/8 全谱系存活)**,
**若想兼顾谱系保持与行为多样性,interval=5(保持 5/8 的同时 diversity 最大)**。
最优点依赖于 fitness / 集团规模,所以在生产环境需要重新校准。
不是"某一个正确答案",而是"随目的而移动的最优点"——这就是诚实的结论。

##### 5.5 诚实的保留 — "存活"也许是"生命维持"

在此,还有一个该诚实写下的保留。
中立贮藏库让全部 8 个谱系存活下来是事实,但**需要怀疑那个"存活"的质量**。

正如正本(§4.1 / §4.2)所写,贮藏库是"再投入各谱系的 best-ever genome(frozen elite)"的机制。
强谱系实际在增加子孙、进行繁殖。另一方面,弱谱系(各 1 个体)的"存活",是
**源自再投入,而非主动的进化**。可以说,**不是繁殖,而是生命维持装置**。

这是完全符合中立贮藏库定义的正当行为(保持代表,使再结合成为可能)。
但我不主张"全部 8 个谱系**活跃地持续进化**"。
"防止了全灭。但弱谱系正在 ICU 续命"——这才是准确的表述。

> 🤔 **比喻(落语风)**:
> 房东:"长屋的住户一个不缺,8 人全齐了,可喜可贺,可喜可贺。"
> 八公:"是啊。只是一半人光喘气、租也不交、躺着不起……"
> 房东:"**那与其说是'住着',不如说是'放着'吧!**"
> 八公:"嘛,总比赶出去强吧……"
> ——全员都在,是事实。全员都在活跃,是谎言。这条界线就是 honest disclosure。

---

#### 6. Stage2 — 从 proxy 通往"实"的桥

光是反证,设计看起来像没在向前走。
但正因为用反证夯实了立足点,下一步才有了意义。那就是 **Stage2: 实 LLM 评价**。

##### 6.1 proxy 轴(mechanism feasibility)

首先,作为 Stage2 的前半,我把 LLM 不擅长的 5 个轴用 **proxy(决定论 heuristic, 不依赖 LLM)**做成了 plugin。

| pressure(LLM 弱点) | 相关思考因子(case) |
|---|---|
| typo_robustness(噪声耐性) | consistency / reality_link / uncertainty |
| polysemy_wsd(多义词) | multiview / consistency / reality_link |
| multistep_robustness(多步推理) | structurize / closed_loop / self_extend |
| calibration(信度估计) | uncertainty / provenance |
| context_management(无关上下文耐性) | consistency / provenance / recompose |

共 14 个 case 输出到 breakdown,lldarwin 的 ε-lexicase **不聚合,而是逐轴淘汰 specialist**。
下面是那些 proxy 轴的母集团均值推移。

![Stage2 proxy 轴的推移(mechanism feasibility)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_zh.svg)

但是——正如此前一再所言——**这是 proxy**。
个体是 genome 而非实 LLM,所以这个 pressure 只是"genome 备有多少与那个弱点相关的思考因子"的
**行为代理**。**没有测量 production 的 LLM 能力**(只是 mechanism feasibility)。
SVG 上也烧入了 "PROXY"。Goodhart 风险在此作为已接受的极限明确标注。

##### 6.2 实 on-prem LLM 评价(proxy→real 的桥)

而本文得以首次报告的前进——**实 LLM 评价跑起来了**。

由于查明 localhost 的 ollama(llama3.2:latest)可达,我在 `real_pressures.py` 实现了
**个体 → 实 LLM 映射**(Promptbreeder 系)。机制如下。

- 把个体的 `c_prompt`(PromptChromosome)转换为 **system prompt**
  (skill_set → 指示文 / prompt_template_id → 推理风格 / language_style → 语调)。
- 给固定 LLM(llama3.2)套上那个 system prompt,让它解 5 个弱轴的**实任务**并打分。
- 也就是说,**固定 LLM 本体,进化 prompt 策略(genome)**。
  **用实测来淘汰**"哪个 prompt 策略能缓解 LLM 的弱点"。

结果,**确认到了实选择信号**。
CoT + structure 策略(`chain_of_thought` + structurize + loop),把
llama3.2 的 **multistep 从 0.0 改善到了 1.0**(terse 的策略在 0.0 失败,score 0.80→1.00)。
不是 proxy 的幻影,而是**在实 LLM 上实证了"prompt 策略的进化能缓解弱点"**。

![Stage2 实 on-prem LLM 轴的推移(prompt 策略进化)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_zh.svg)

把 proxy 轴(前述)和实 LLM 轴(上)**并排来看**,就能用眼睛看出"用 proxy 测出的形状"
和"实测的形状"有何不同。proxy 只表明机构在运转。实 LLM 则表明,prompt 策略
对模型的弱点实际如何奏效。**这 2 张图的差异,正是本文主张的实物。**

##### 6.3 但在这里,也要诚实

在实 LLM 上跑起来了——但在这里,我同样要拉响警笛。保留有 4 条。

- **(a) 只有 c_prompt 参与 fitness** — persona / c_factors 是中立的,不牵涉 fitness。
  谱系由 reservoir 维持,初期选择由 novelty 承担。也就是说,这是"**prompt 策略的进化**",而不是
  "persona 的进化"。
- **(b) 全部 founder 的初期 c_prompt 相同(default)** — 所以探索由 mutation 驱动。
  让每个 founder 的 prompt 多样化是今后的改善点。
- **(c) 小批量(每轴 2 题)** — 估计含噪。"multistep 0→1"也因为题数少,
  仅凭这个无法主张泛化。
- **(d) on-prem only(测量纯度)** — 限于 localhost ollama,
  **并非对一般 LLM 能力的主张**([[feedback_llive_measurement_purity]])。

我也启动了 12h 连续运行(`--fitness real-pressure --selection lldarwin --novelty
--lineage-reservoir --genome3d`)。在 wallclock 12h safely 停止(已 snapshot → 可用 `--resume` 续跑)。
但我不说"跑了 12h 所以是真的"。跑了,是事实。把本质测尽了,是谎言。
**proxy→real 的桥架起来了。但还没渡完。**——这就是 Stage2 的诚实状态。

---

#### 7. 结论 — 能主张到哪里(界线)

"只要把 LLM 的弱点当作 proxy fitness,进化就能克服"是**乐观的**。
用反证削减之后,我把 lldarwin 的价值主张**限定**为下面 3 点。

1. **(a) proxy 只是 mechanism feasibility** — 验证进化的管路在运转。不主张 production 能力。
2. **(b) 实 LLM/VLM 评价才是本质** — 智能的选择压力由个体 → 实模型映射(Stage 2)承担。
   桥在这里架起来了。但正式渡过还在今后。
3. **(c) 多样性的地图化** — 把能赢的轴限定为"无可验证性的多样性(认知、文化风格)的地图"。
   不主张未设想涌现。

这就是 honest disclosure。**失败(#25)、自己的混淆(§3.2)、极限(#5/§6.3),都不抹去地留下。**
一句气派的胜利宣言都没写的这篇文章,我认为正是进化弧线中最诚实的一回。
向前迈进的立足点,只存在于这条界线之上。

---

#### 8. 教训(永久保存)

- **结果越好(0.05 改善)越要怀疑其内訳。** "proxy 行为多样性"既不是"谱系多样性"也不是"实 LLM 智能多样性"。
  看到一个数字就草率断定另一种能力也变好了的我,就是 Goodhart 的活标本。
- **不修"测量"只把"淘汰"做得高级,是徒劳。** 对饱和的镜片,任何选择压力都无效。
  打磨镜片在先,载上淘汰器在后。
- **Goodhart 定律是进化的天敌。** 把指标当作目标的那一刻,进化就会 hack 它。
  而且读指标的人类的解释也一并背离。
- **既然设计者决定多样性的方向,就不主张未设想涌现。** 限定能赢的轴,才是诚实。
- **"存活"也许是"生命维持"。** 全部 8 个谱系都留下来了,是事实。全员都在活跃进化,是谎言。
  动词的选择之中寄宿着 honest disclosure。

> **下回预告**: 用反证夯实立足点之后,接下来是 Stage 2 的全面化(实 LLM/VLM 评价, on-prem ollama)。
> 不是 proxy 的幻影,而是能否真的把实模型的智能多样性变成选择压力。
> 能否不让"multistep 0→1"止步于小批量的偶然,而把它培育成可复现的选择信号? 从这里起才是动真格。

---

#### 9. 相关
- 连载 #25"只有我和弗里斯顿留了下来"— 失败的记录(本文的起点)
- 连载 #26"lldarwin 的设计"— 淘汰器(本文反证的对象)
- 实现 commit(llive): Stage1 = `8060204` / lineage-reservoir PoC = `0d0537d` /
  Stage1.5(EvolutionLoop 集成)= `b03cbda` / Stage2(实 LLM real-pressure)= `2fb2912`
- 实测正本: `../../research/lldarwin_stage1_results_2026_05_26.md`(§3 honest disclosure / §4.1–4.5)
- 设计正本: `../../vision/LLDARWIN_DESIGN.md` §7 / §7.1(反证调查、已接受的极限)
- 相关 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_implementation_status_record]]
- 参考: Goodhart 定律 / La Cava 2019(ε-lexicase, arXiv 1905.13266)/ Taylor et al. 2016(open-endedness 的极限)/
  Bedau(neutral shadow)/ Kimura(中立进化说)

---

## 6. 進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで、人工進化はどう可視化されてきたか

### 「展示」进化的技术谱系 #30 — 从 Conway 的生命游戏到 3DGS

> **概念钩子**：我在 #25〜#27 里喋喋不休讲的「人工进化」，其实是一个有着半个多世纪历史的研究领域。而有意思的是，**进化研究始终与「如何展示（可视化）」并肩前行**。从 1970 年黑白闪烁的细胞，到 2024 年连续流体与 3D 高斯。让我们作为一种通识，一口气追溯「展示进化的技术」的谱系。最后，我们将定位 **FullSense 的进化可视化（绘制在思考因子图上的系统树）站在这条谱系的哪个位置**。

---

#### 0. 为什么「可视化」是进化研究的主角

进化是一种 **长时间、大种群、多世代** 的现象。一堆数字罗列，根本抓不住「到底发生了什么」。因此人工进化的历史，几乎就直接是 **「让人一眼理解进化的表现手法发明史」**。

> 🍵 **休息点**：这篇文章是一次零公式、几乎零代码的「散步」。请端着咖啡慢慢看。我们只拾取各个时代「展示方式的突破」。

---

#### 1. 1970：Conway 的生命游戏 —「简单规则生出图案」

- **是什么**：二维元胞自动机。生死两态 × 8 个邻居细胞的简单规则。
- **可视化的发明**：**格点的闪烁本身就是可视化**。滑翔机、闪光灯、滑翔机枪这类「移动的图案」被赋予了名字 = 人类 **用眼睛为涌现模式命名** 的最早期例子。
- **局限**：这并非进化（自然选择），而是决定论式的展开。但「简单规则 → 复杂外观」的冲击开辟了这个领域。

**本节计划充实**：深入探讨「滑翔机被识别为『移动的结构』」如何成为可视化催生概念的绝佳例子。

---

#### 2. 1991：Tierra（Tom Ray）—「代码成为生物」

- **是什么**：在虚拟 CPU 上自我复制的机器码程序的生态系统。寄生体、免疫、最优化 **自行涌现**。
- **可视化的发明**：**内存映射的可视化**。把每个程序所占据的内存区域用颜色涂出，将寄生体咬入宿主的样子作为「地图」展示。它 **把「代码的生态系统」描绘成了一个空间**。
- **意义**：在计算机内首次观测到「自我复制子的自然选择」。这是开放式进化（open-ended evolution）研究的起点之一。

---

#### 3. 1994：Avida（Adami / Ofria）—「测量进化」

- **是什么**：继承 Tierra 谱系的数字生命平台。完成逻辑运算便可获得奖励（CPU 时间）。
- **可视化的发明**：**系统树（phylogeny）与适应度地形的可视化**。把「哪些子孙从哪个祖先分支而来」绘成一棵树，让复杂性状（如 EQU 运算等）逐步进化的过程变得 **可追踪**。
- **意义**：它实证了「复杂性会经由不可避免的步骤进化」（Lenski et al. 2003, Nature）。它 **把进化从故事变成了测量对象**。FullSense 的 monoculture 监控（max_lineage_share / archive 成长）正是这种「被测量的进化」的直系后裔。

> 🤔 **打比方（相声风）**：
> 逗哏：「Avida 让进化能用数字来测量了。」
> 捧哏：「也就是给进化发了张成绩单嘛。」
> 逗哏：「没错。我在 #25 里说『满分通胀把成绩单搞坏了』，说的正是 Avida 级别的测量这回事。」

---

#### 4. 1994：Karl Sims「Evolved Virtual Creatures」—「用影像呈现进化」

- **是什么**：在 3D 物理仿真之中，**同时进化** 形态（block 的连接）与神经控制，孕育出会游泳、会走路、会争抢物体的生物。
- **可视化的发明**：**3D 动画影像**。不是用论文里的图，而是用 **视频** 来展示，这引发了震撼。它把「进化所设计的、谁都没料到的奇异步态」做成了 **人类能凭直觉觉得有趣** 的形态。
- **意义**：进化可视化从「面向研究者的图表」迈向了「**任何人看了都会惊叹的影像**」。它是 FullSense 演示哲学（[[project_f25_demo_polish]]「以动感取胜」）的精神祖先。

> 🍵 **休息点**：到这里，如果你能看出展示方式经历了 **抽象 → 具象 → 动态** 的进化——「黑白点 → 内存地图 → 系统树 → 3D 视频」——那就够了。后半部分是现代篇。

---

#### 5. 2019：Lenia（Bert Chan）—「连续的人工生命」

- **是什么**：把生命游戏一般化为 **连续空间、连续时间、连续状态**。人们发现了大量平滑运动、「像生物一样」的图案（如 orbium 等）。
- **可视化的发明**：**连续场的平滑渲染**。从离散的闪烁，转向如生物细胞般柔韧运动的流体式表现。它开辟了一条新的诉求轴线：「人工生命是 **美的**」。
- **意义**：这是可视化质量本身提升了研究发现力的例子。正因为看上去美，人类才能注意到新的图案。

---

#### 6. 2020 年代：Quality-Diversity 的可视化 —「把多样性画成地图」

- **是什么**：MAP-Elites / CMA-ME 等 QD 算法。它们生出的不是单一 best，而是 **多样的高性能解的集合**。
- **可视化的发明**：**behavior space 的热力图**。取两轴的 behavior 描述子放到格点上，把每个 cell 的 elite 用颜色涂出 = 「**把多样性本身可视化为地图**」。
- **意义**：FullSense / lldarwin 的 QD archive 可视化直接立足于此。它能通过 **地图的空白 vs 填充** 一眼展示「只要还剩一个 cell 就不会全军覆没」（详见 #26）。

---

#### 7. 2020 年代起：3D Gaussian Splatting（3DGS）—「将进化的状态以空间表达」（FullSense 的赌注）

- **是什么**：原本是新视角合成（NeRF 谱系）的技术。它把点云用 3D 高斯来表示，并以高速、高品质渲染。
- **FullSense 的构想**：一种探索——能否把进化种群的 **高维 genome / pressure profile 映射到 3D 高斯空间**，从而「将进化的状态立体地展示出来」（与 [[project_precision_metrology_llm]] 的 SH 系数联动同根同源）。
- **定位**：这 **仍是一项研究性赌注**，并非已确立的技术（honest disclosure）。它是放在本文谱系「最前沿的边缘」上的一次实验。

---

#### 8. FullSense 的进化可视化站在哪里

| 时代 | 展示方式的核心 | 在 FullSense 中的继承 |
|---|---|---|
| Conway 1970 | 闪烁细胞 = 为涌现命名 | （概念上的祖先） |
| Tierra 1991 | 内存地图 | 系统占有率的地图化 |
| Avida 1994 | 系统树 + 测量 | monoculture 监控 / lineage tree |
| Karl Sims 1994 | 3D 视频 | 「以动感取胜」的演示哲学 |
| Lenia 2019 | 连续场之美 | animated SVG 表现层 |
| QD 2020 年代 | behavior 地图 | lldarwin QD archive 可视化 |
| 3DGS 2020 年代起 | 3D 空间表达 | （研究性赌注） |

FullSense 的进化可视化（**思考因子图上的系统树 + animated SVG**）所处的位置，是 **在终端 / 浏览器中再现 Avida 的「会测量的系统树」、Karl Sims 的「以动感取胜」以及 QD 的「多样性地图」**。它是这条长达半世纪的谱系中，虽不起眼却根正苗红的后裔。

> **下回预告**：追溯完谱系，接下来就是实现。我们将以真实的 evolution.svg 为题材，讲解 FullSense 的系统树 animated SVG 究竟吸收了上述哪些「展示方式」、又是怎么吸收的。

---

#### 9. 相关

- 连载 #25〜#27 — 本文进化可视化的「内容」（monoculture / lldarwin / 反证）
- 相关 memory：[[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- 参考：Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

## 7. AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制と検証規律

### 让 AI 把 AI 当作下属来使用 #31 —— Claude 主导 + Codex 配属的「两根支柱」开发体制

> **概念钩子**：FullSense（llmesh / llive / llove）是我一个人的个人开发项目。但实际情况
> 并不真的是「一个人」。一套**以一个 AI 编码代理为主、以另一个 AI 代理为下属**的
> 两层开发体制正在运转。主为 **Claude Code**，下属为 **Codex CLI**。
> 「AI 把工作分派给 AI，再由 AI 来验证其成果」——如何让这种多重委派保持纪律、
> 不至于失控？本文是关于运行「1 个人 + 2 个 AI」这一「两根支柱」体制的实践记录。
>
> 关键词是 **编排者（orchestrator）/ 配属 worker / 验证纪律 / 并行化**。

---

#### 0. 三行剧情简介

- **Claude = 编排者**（计划、实现、委派、**验证**）/ **Codex = 配属 worker**（执行、评审、调查）。
- 「两根支柱」并非对等，而是 **Claude 主导 + Codex 配属**。指挥系统要保持唯一。
- 铁律：**外部 AI 的 finding 必须先用实代码 / 一手信息逐条验证后才采用**（禁止盲信）。

---

#### 1. 为什么是「两根支柱」—— 动机

在个人开发中，只用一个 AI 代理早已是常态。那么我为什么要加上第二个（Codex），**而且是作为下属**？

1. **厂商分散与冗余** —— 对冲单一代理的计费变更 / 故障 / quota 枯竭。
2. **交叉评审** —— 把同一份设计拿给另一系谱的 AI 看，获取第二意见（减少盲点）。
3. **并行 worker** —— 把独立子任务抛给下属，主则专注于最重要的任务。

> 🍵 **休息点**：「用两个 AI = 聪明两倍」是错的。关键在于**保持指挥系统的唯一性**。
> 若搞成乌合之众，反而会变慢。本文有一半是在讲「如何统制」。

---

#### 2. 角色分工 —— 编排者与配属 worker

![层级图：人类 → Claude Code（主＝编排者）→ Claude 子代理并行 / Codex CLI 配属 worker](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy_zh.svg)

- **Claude（主）的职责**：任务分解、依赖性判定、独立任务的并行启动、进度监控、**成果验证**、统一提交（commit）。
- **Codex（下属）的职责**：执行被委派的范围。非交互式委派 = `codex exec -s read-only "<prompt>"`。
- **指挥系统始终是 Claude。** Codex 只能经由 Claude 才能影响整体（不让它直接 commit）。

**本节待充实的内容**：对比 Claude 子代理并行（[[feedback_parallel_first_execution]]）与 Codex 配属委派的
使用区分表。「同一 file 串行、独立 file 并行」「git 操作由 orchestrator 统一进行」（[[feedback_agent_no_git_parallel]]）。

---

#### 3. 验证纪律 —— 「禁止盲信」是体制的命脉

两根支柱中最危险的，是**一个 AI 不经验证就采用另一个 AI 的输出**。错误会被放大。因此有铁律：

> 外部 AI（Codex / Copilot / Gemini）的 finding，只有在**用实代码 / 一手信息逐条验证**之后才采用。

实例：在本连载 #26（lldarwin 设计）中，对既有代码资产的调查（例如 `mating.py:139 LexicaseSelection`
是「已实现但未接线」等）是让下属去调查的，但**接线点与行号是由主（Claude）在实文件中确认后**
才写进设计文档的。不会把「Codex 是这么说的」当作设计的依据。

> 🤔 **打个比方（相声风格）**：
> 师父：「喂，那个函数，接线了没有？」
> 徒弟：「禀师父，没接线。」
> 师父：「……你这『禀师父』我信不过。我自己去看源码。」
> ——这就是验证纪律。徒弟的报告是**起点**，而非**结论**。

**本节待充实的内容**：验证的三个阶段（收到 finding → 用实代码 / 一手信息确认 → 采用或弃用），以及
评审封装器（如 `tools/copilot_review.sh` 这类只读评审）的定位。

---

#### 4. 并行化的规矩 —— 不让它失控的统制

同时运转多个 worker（Claude 子代理 + Codex）时的纪律：

- **2～4 个并行是安全区**（主的 context 有余裕、无提交冲突）。5 个以上则要严格管理 file 级别的独立性。
- **抽取独立任务** = 无依赖 + 在 file / module / repo 级别互不接触。同一 file 串行（类似 file lock）。
- **不可逆操作（删除 / push / submodule 改动）逐条经人工确认。** 不让下属擅自去做。
- **git 操作由 orchestrator 统一进行。** 不让并行 worker 碰 git（规避冲突）。

> 🍵 **休息点**：「把 AI 摆得越多越快」是个陷阱。**主的 context（注意力的总量）才是限速因素。**
> 即便并行 5 个，若主处理不过来也毫无意义。和大脑的工作记忆一样，能同时把握的数量是有上限的。

---

#### 5. 反模式（绝不可做的事）

- 宣布「我会逐个确认着推进」之后却默默地串行执行（错失了并行化的机会）。
- 不委派给下属，全部都在主的 context 里干（context 爆炸）。
- 在并行启动的 worker 出结果之前，主就去碰同一个 file（冲突）。
- 委派两个 worker 去写同一个 file（独立性判定的遗漏）。
- 不经验证就把下属 AI 的 finding 采用进设计或实现（错误放大 = 两根支柱体制中最大的事故）。

---

#### 6. 这套体制实际运转出了什么（FullSense 的实例）

- **设计交叉评审**：让下属评审进化设计 / 需求 / PoC，主用实代码验证后做出采用判断。
- **既有资产调查**：让下属调查 lldarwin 既有部件（loop.py / mating.py / nsga2.py 等）的所在 → 主确认。
- **并行子任务**：把文章骨架、代码调查、需求整理作为独立任务并行化（本连载本身就是其产物）。

> 🍵 **休息点**：最后我也会诚实地谈谈，「1 个人 + 2 个 AI」让个人开发的生产力发生了怎样的主观变化。
> 对变快的方面（并行、冗余）与增加的负担（验证成本、统制成本）**两者**都做 honest disclosure。

---

#### 7. 教训

- **保持指挥系统的唯一性。** 两根支柱并非对等，而是主从。指挥中心的分裂是事故之源。
- **验证纪律是体制的命脉。** AI 不经验证就相信 AI 的连锁，是最大的风险。
- **并行度由主的 context 限速。** 以能处理的量来决定，而非以个数。
- **不可逆操作与 git 由人类 / orchestrator 掌握。** 只把可逆的工作交给下属。

> **下回预告**：把用两根支柱运转出来的进化设计（#26 lldarwin），借助配属的 Codex + on-prem ollama，
> 推进到 Stage 2（用真实 LLM 评估）。多重 AI 委派究竟能把「研究的实现速度」提升到什么程度。

---

#### 8. 相关
- 连载 #26「lldarwin 的设计」—— 用本体制运转出来的实例。
- 相关 memory：[[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

## 8. llcore — Transformer のコアを CPU で進化させる: Verified Neural Architecture Evolution の最小 PoC battery

### (连载 #32) llcore CPU PoC battery 完成

#### TL;DR

- 将 **Transformer 的核心计算 (state update / 学习规则 / 认知驱动 Δ)** 作为进化对象的研究框架 `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 独立路线) 的 **CPU PoC battery 完成**
- 以 **5 个 PoC / 39 个可证伪 gate / 76 个测试 / Codex pair-review 5/5 Green-light** 完成机制验证
- **用 Z3 对结构变异进行 online gate** = 把 SMT 嵌入进化搜索的 selection pressure，经事先调查发现为未被探索的先行研究 (事前调查 RAD 14 个领域 + Agent A-D 确认)
- 投稿候选: TMLR (本命) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

#### 为什么要做

冻结 LLM 权重是标准做法，但**核心计算算法本身仍固定为人工设计**。AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge 等 architecture/algorithm 搜索虽已推进，但:

1. **个人 compute 无法承担计算资源** (TinyLlama 1.1B from scratch = $140k / 90 天 / 16×A100)
2. **搜索过程中没有安全性保证** = 生成数值不稳定的 architecture 而浪费时间
3. **带验证的搜索与静态 verification (Reluplex/Marabou/α,β-CROWN) 相互割裂** — 在进化循环内做 SMT online gate 的研究未被发现

#### 已确定的独有轴 (事前调查中没有 negation work)

机制已验证 (4 个轴):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **将 state update 规则基因化 RWKV-style** (Stage 0a v2)
3. **factor_hook (认知状态 → SSM Δ)** (Stage 2a mock)
4. **自研进化器 + verifier 基础** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / 提出 VNN-COMP 新类别。

#### PoC 阶梯 (5 stage / 39 gate 全部 PASS)

| PoC | 内容 | 关键数值 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 自研 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

#### 从 v1 的失败中学到的东西 (honest disclosure)

PoC 0a v1 用 `decay*s + mix*x*tanh(gate_str*s)`，使得 **state=0 成为 fixed point 的 zero attractor** = 形式上通过 G1-G5，但信息传递为零。Claude 单独遗漏的设计问题被 **Codex (gpt-5.4) 与 gem-critic 的独立 verdict** 检测出来，从而在 RWKV-style 上做了 v2 redesign。

→ **在 5 个 PoC 中有 4 件，Claude 单独遗漏的设计问题被 Codex pair-review 检测出来**。这是相互评审在防止结构崩溃上发挥作用的实例。

#### 下一步选项

a. Stage 3 kernel 多样化 (将 rwkv/mamba/hopfield/linear-attn 基因化)  
b. Stage 4 将学习规则 (FF/EP/PCN/Hebb) 基因化  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. 用 PrediPrune+Quokka 给 Z3 gate 提速  
e. 用 FlashEvolve 实现 3.5-5x wall-clock 提速  
f. 写成论文 (TMLR + GECCO 2027)

#### Honest 保留

- 以 mock 为主，连接真实 LLM/权重要等 GPU/新 PC
- 1 step scalar invariant 处于 over-approx proof 阶段，多维、多 step 在 post phase
- tanh 上界近似偏保守 (sound 但不完整)

---

**Tags**: 进化计算 / 形式验证 / Z3 / RWKV / state space model / CPU研究  
**相关**: 连载 #14-31 (llive lldarwin v0.B-E + 观测+governance + lleval)  
**Project**:  (PyPI llmesh-llcore 0.1.0a0)

---

## 9. llcore — 「進化で AI を設計するとき、選り分けて育てる工夫は本当に要るのか?」を 3 実験で詰めた話 (第三軸 ③ 決着 Step D)

### (连载 #33) 过于整齐的结果不是胜利，而是警报 —— 用 proper power 给第三轴 ③ 一锤定音的一天

#### TL;DR

- 问题是 **「当用进化去搜索 AI 的核心计算时，"挑选、分开、培育"这个工夫 (= 进化的 ③ 适者生存/分离要素) 究竟需不需要？」**
- **在合成的"带山谷的 (欺骗性) 地形"上，③ 大获全胜** (过去实验中 Cliff δ=+1.0)。③ 作为机制是货真价实的。
- **但当我们把更接近真实的 CPU proxy 地形的评估噪声物理性地降到零之后重新测量，结果是"真正平滑 (单峰)"，于是确定 ③ 不需要。**"过去的 negative 不是检出力不足 (underpower)，而是地形本来就平滑"这一点首次得到佐证。
- 只有真实 multitask 邻域 (C-gen4b) 出现了微弱的"③ NOT null"气息，但增加数据后就发生摇摆，**止步于候选** (走行内漂移 + 在多重比较下脆弱)。
- "某个后处理在隐藏 ③"的怀疑 (K4 ridge clip)，去掉之后反而变得更差 → **它并没有隐藏什么，降级为诊断性所见。**
- 外部评审 (Codex) **没有阻断项**地追认了结论。
- 结论一句话：**「③ 只有在地形具有欺骗性时才会发挥作用。这次在 CPU 上能测到的、接近真实的地形，恰好是平滑的。」** 主战场的定论需要 GPU (真实 LLM 地形)，但那是投资决策。
- **追记 (2026-06-02, §11.5): 最后的 CPU 逃生路线 kernel 多样化 (BG9) 在结构上被堵死了。** kernel 选择是低维，因此强 baseline (RR) 会直接采样，③ 的 niching 优势在原理上无法出现。**要让 ③ 起作用，需要"高维的"欺骗性地形**，剩下的路只有 GPU full-LLM (而这本身也是一场赌注)。
- 元教训：**诚实披露 (honest disclosure) 不是装饰，而是推动研究前进的工具。** 在 BG9 中，同样的纪律在"把 negative 正确地确定为 negative"这个方向上也奏效了。

> ⚠ 本文中的所有数值，都是与本地 (手边) 的研究 commit `THIRD_AXIS_SETTLE_VERDICT.md` 绑定的实测值。llcore 还没有建立公开仓库，所以无法贴出外部链接。作为替代，我把"如何测量"全部写在正文里。

---

#### 0. 这篇文章在讲什么 (概念)

`llcore` 是一个 CPU 完结的研究框架，它"把 Transformer 的核心计算 (状态更新规则、学习规则、认知驱动 Δ) 作为基因，一边用 Z3 验证其不会崩坏，一边进化" (PoC battery 的事在连载 #32 写过)。

它的进化引擎有一个设计上的命门：如何让进化四要素中的 **③ (适者生存 selection / 分离 separation)** 生效。这是一种像 MAP-Elites 那样"挑选、分开、培育"的机制，保持多样性并把精英留在各自的 niche 里。

问题很简单。

> **那个 ③，真的需要吗？**

如果需要，那么为承载 ③ 而进行的重投资 (最终是在 GPU 上跑真实 LLM) 就有意义。如果不需要，执着于 ③ 就是浪费时间和电力。

在这一天 (2026-06-02)，我用 **3 个实验正面给这个问题作了了断**。正如标题所说，结论又一次把我们拉回 FullSense 的那条低音主旋律——"过于整齐的结果是警报"。

—— 到这里 30 秒。准备运动结束。进入正题。 —

---

#### 1. 打个比方：登山，与欺骗地形

在公式之前，先用地形的比喻把全貌抓住 (这是本研究中一贯使用的隐喻)。

我们用 **地形的高度** 来表示设计的好坏。**高处 = 好设计。** 这是一个寻找最高山顶的游戏。

**地形其一：平滑的单座山 (简单)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

在这样的地形上，朴素的"登山法 (hill-climbing)"，也就是"只朝比现在稍好一点的方向移动"，就足以到达山顶。**不需要那些精巧的工夫 (③)。**

**地形其二：欺骗地形 (deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

在这里，朴素的登山法会停在假山顶上。因为它没有走下山谷的勇气。

此时起作用的就是 ③ 的思路。**把各种类型的登山者分散留在山谷的各处** (= 记忆宫殿 / MAP-Elites archive)。某个登山者可以靠"踏脚石"渡过山谷，到达真正的山顶——这就是其机制。

**用一句话概括本研究的核心**：③ 真正有用的，**只有在"欺骗地形"的时候。** 在平滑的单座山上，③ 是无用的累赘。

所以问题可以改写为：

> **「当用进化设计 AI 时，实际遇到的地形是"欺骗地形"，还是"平滑的单座山"？」**

这个一旦确定，③ 需不需要也就确定了。今天，我们测的就是这个。

---

#### 2. 过去遗留的问题 ——"③ 不需要"真的是"不需要"吗

通过迄今为止的实验 (Step C → 梯子段 1 → E-A → 谷深实测)，图像大致是这样的。

- **在合成的欺骗 corridor 上，③ 大获全胜** (战胜全部 3 个 baseline，Cliff δ=+1.0)。③ 已被存在性证明，作为机制是真的。
- **在更接近真实问题的 proxy 地形上，③ 是 negative** (MAP-Elites 只能与 random 打平 = 与平滑地形相同的症状)。

然而，这里残留着 2 个未解决的疙瘩。

1. **"③ 不需要"究竟是因为"地形平滑"，还是仅仅因为"样本数不够、检测不出差异 (underpower)"？** ── 弄错这一点，就会犯下"③ 无力"这种过度泛化的错误。
2. 谷深的直接测量上次以 **N/A (无法测量)** 告终。评估噪声比山谷的深度还大，所以即便有谷也会被埋没看不见——这是仪器的极限。

也就是说，"看起来平滑"究竟是 **地形的性质** 还是 **仪器的极限**，并没有定论。把这一点说清楚就是 Step D。

—— 稍事休息。以上是前提。从这里开始是今天做的 3 个实验。 —

---

#### 3. 实验设计 —— 三件套

| 实验 | 测什么 | 目的 |
|---|---|---|
| **EXP1** | proper-n 复检 | 认真增大样本数，用检出力把 ③ 的效果是否真实钉死 |
| **EXP2** | 决定论 C1 多峰性 | 把评估噪声物理性地归零，noise-free 地判断地形是"欺骗地形"还是"平滑的单座山" |
| **EXP3** | K4 ridge clip 的 verdict-flip | 验证"某个后处理在隐藏 ③"的怀疑 |

纪律：全部隔离在 `research/step_d_settle/`，src 不改动，git 由协调器一次性提交。每个实验都要通过崩坏门 (G1 CPU 全程跑完 / G2 可复现性 / G3 诊断器有效 / G4 src 不变)。

---

#### 4. EXP2 才是决定性的 —— 把评估噪声归零，地形就显现了

顺序有所颠倒，但 **最起作用的是 EXP2**，所以先写它。

上次谷深测量变成 N/A 的原因很简单，就是 **"谷的深度 (约 0.05·|fitness|) ≪ 评估噪声的抖动"**。山谷被埋在仪器的噪声里，无法判断它存在与否。

EXP2 的诀窍是这样的。

> ESN reservoir (固定 seed) + ridge readout 的 closed-form (`np.linalg.solve`)，**完全不抽取随机数。** 因此可以把评估噪声物理性地归零到机器 epsilon (约 1.11e-16)。

实测中我们确认了 `eval_noise_std ≤ 1.11e-16`。这不是"每次评估值都抖动"，而是源于浮点最小单位 (ULP) 的误差，**实质为零。** 在噪声之雾完全散去的状态下，可以直接测量地形的山谷。

结果如下 (valley_fraction = 山谷的比例，越大越多峰 = 欺骗地形)：

| landscape | 类别 | 维度 | valley_fraction (mean/max) | 多峰？ | 判定 |
|---|---|---|---|---|---|
| **ESN_3param** (真实 proxy) | real | 3 | **0.000 / 0.000** | **False** (3 seed 一致) | 平滑=单峰 → ③ 不需要，noise-free 确定 |
| **ESN_perneuron40** (真实 proxy) | real | 40 | **0.096 / 0.121** | **False** (3 seed 一致) | 偏平滑 (低于地板 0.2) → ③ 不需要 |
| ctrl_multipeak_dim3 (正 control) | control | 3 | 0.701 / 0.727 | True | 诊断器能检出多峰 ✓ |
| ctrl_multipeak_dim40 (正 control) | control | 40 | 0.795 / 0.818 | True | 诊断器健全 ✓ |
| ctrl_quadratic_dim3 (负 control) | control | 3 | 0.000 | False | 诊断器能检出平滑 ✓ |
| ctrl_quadratic_dim40 (负 control) | control | 40 | 0.000 | False | 诊断器健全 ✓ |

要点有 3 个：

1. **真实 proxy 地形 (3 维 / 40 维 都是) 是 valley≈0 = 单峰。** 在 3 个 seed 上完全一致。
2. **诊断器本身是健全的。** 故意做出来的多峰正 control 被正确检出为多峰 (0.70/0.80)，二次函数的负 control 被正确检出为平滑 (0.0)。所以"真实 proxy 是单峰"不是仪器的 bug，而是地形的性质。
3. 由此，**"过去的 ③ negative 不是 underpower，而是因为地形本来就平滑"** 首次在真实 substrate 上得到了 noise-free 的佐证。

我也老实写下一个副发现。**原本打算用作正 control 的欺骗 corridor (`make_corridor_eval(d=0.16)`)，一旦决定论化，竟变成了 valley=0.0 (单峰判定)。** corridor 的欺骗性是"关进单一 basin、用 ③ 的 behavioral niching 逃出"这一型 (behavioral-reach 欺骗)，而 **不是** 地形山谷 (C1 multi-basin) 的欺骗。我们用实测确定了 scope 的收窄：corridor 不能成为 C1 的正 control。这意味着过去的谷深校准无法把"corridor 来源的阈值"迁移到地形多峰性上。

—— 在这里喘口气。"正 control 没能当上 control"这件事，意外地让人受了点打击。但这一点也是不测就不会知道的。 —

---

#### 5. EXP1 —— 只有真实 multitask 邻域出现微弱的"③ NOT null"气息

接着，我们认真增大样本数，对最接近真实问题的频带 (C-gen4b = MAP-Elites vs random，真实 multitask 邻域) 进行了复检。

| case | 原 n=15 (审计) | fresh 真复跑 | 判定 |
|---|---|---|---|
| **C-gen4b** | diff +0.063 / psd +0.20 / p 0.126 | **n=64: diff +0.0472, 单侧 p 0.038, psd +0.188, gate PASS** | **③ load-bearing 候选 (still_inconclusive)** |

用 fresh seed 跑到 n=64，**严格门的 4 个条件全部 PASS。** 也就是说，审计读成"③ 不需要 (inconclusive)"在方向上是错的，**在 C-gen4b 中 ③ 是朝 NOT null 的方向。**

…而在这里不产生"赢了"的飘飘然，正是这一轮的要害所在。出于 3 个理由，我把它 **止步于候选。**

1. **更新后的检出力 power@n64 = 0.517 < 0.80。** 门通过了，但没达到确证的标准 (检出力 0.80)。
2. **走行内漂移 (这一点起了作用)。** 追踪累积 p 值的轨迹：n=40 时首次 PASS (p=0.042) → n=60 时 p=0.010 显著性加深 → **n=64 时 p=0.038，又回到了 0.05 边界附近。** 进一步把 seed 按前半/后半切开：**前 32 个 seed 是 diff=+0.0755 (frac_pos=0.625)，但后 32 个 seed 是 diff=+0.0189，最后 9 个 seed 是 diff=−0.0376 (负)。** PASS 是靠前半 seed 撑着的，**越是新数据越往反方向跑。**
3. **多重比较。** p=0.038 在 α=0.05 下 PASS，但仅就 EXP1 的 3 个 case 而言也超过了 Bonferroni α=0.0167 (FAIL)。放到整个 ③ research family 来看就更严苛。

此外，效果量的地板 (psd) 撞上了 **结构性天花板。** C-gen4b 的 median psd 从 n=15→0.200 到 n=255→0.200 纹丝不动。`P(|psd|≥0.147)` (效果量条件的满足率) 即便在 n=255 也封顶于 0.794。因为是中效果 (psd≈0.20)，无论怎么增大样本，full gate 的检出力都不会超过 0.80。**也就是说，"只要增大样本就会确定 (A)"这个前景本身，在这个 proxy 上就很渺茫。**

结论：**C-gen4b 是"③ load-bearing 候选 / still_inconclusive"。** "③ NOT null"这个 headline 过于依赖单一的边界 p=0.038。走行内漂移是"候选可能是假阳性"的真证据。

---

#### 6. EXP3 ——"后处理在隐藏 ③"的怀疑，去掉之后反而更差了

最后一个怀疑是这样的。"ridge readout 的 clip (K4) 这个后处理，会不会其实在掐死 ③ 的信号？" 如果是这样，去掉 clip，③ 就应该浮现出来。

我试着去掉了。

| task | clip | MAP-E mean | 战胜的 baseline 数 | verdict_flip |
|---|---|---|---|---|
| **addition** | True | +0.0100 | 1/3 | — |
| **addition** | False | **−1.212** | 0/3 (全部恶化) | **False** |
| **flip_flop** | True | +0.426 | 0/3 | — |
| **flip_flop** | False | +0.438 | 0/3 | **False** |

去掉 clip 后，③ 非但没有浮现，反而 **在 addition 上 MAP-Elites 从 +0.010 → −1.212 劣化。** clip=False 把 MAP-Elites 落进了 raw R²<0 的噪声区域 (15/15 seed 为负，R² 在 [−3.68, −0.20])，不仅没能恢复结构反而更差。**= 主动反证了"clip 在隐藏信号"这一假说。**

null-ridge FPR (gene 无关 target = 真正的零假设) 在 clip True/False 之间差异也为零 (两者都是 0.0)。

判定：**K4 不是"唯一的主动 suppression 机制"，而是降级为"压扁 spread 但不改变 verdict 的诊断性所见"。** 由此可知，过去统计审计断定的"K4 = 唯一的主动 suppression"是夸大了。

诚实的保留 (相当于 §6.3)：null-FPR=0/0 只是 null_seeds=4 的地板值，而且这个实验把预算缩小了约 7 倍。所以我把 verdict 的标签统一为不是"null 确定"而是 **"not_load_bearing_at_this_budget (在此预算下非载荷)"**。因为"在此预算下 K4 非载荷"比"零假设已确定"更准确。判定的实体 (降级为诊断性所见) 不变，只是提高了用词的精度。

—— 在这里深呼吸。3 个实验结束。接下来是"有没有说过头"的自检。 —

---

#### 7. Surviving refutation —— 用 3 个透镜捶打自己的结论

honest disclosure 的核心是"最狠地怀疑自己的结论"，所以我用了 3 个独立的反证透镜。**3 个都以 `refuted=true / medium` 存活下来**，也就是说保守的 verdict 没有被推翻，但偏 positive 的强调被朝着减弱的方向修正了。

1. **[power_adequacy] C-gen4b 的 gate PASS 在 optional-stopping + 多重比较下脆弱。** 这就是上面 §5 的漂移和 Bonferroni FAIL。把"③ NOT null"做成 headline 过于依赖边界 p。→ 已把 p 的 n 轨迹和后半 seed 的符号反转记录到披露字段中。
2. **[determinism_and_circularity] 单峰 verdict 在阈值临近处脆弱。** 决定论化和非循环性本身是 clean 的 (behavior 与 fitness 的相关 ≈0，诊断器不使用 behavior 描述子，而是直接看地形几何)。但 ESN_3param 的 midpoint 有 **90.9% 向下方 dip**，最大相对 dip=0.0435 就在 C1 谷阈 0.05 的正下方 (在 13% 以内)。所以精确地说，它不是"**真正单峰**"，而是"**略低于 C1 阈值、带浅谷 (~2–4%) 的弱 multi-basin**"。(B) null 的方向得以维持，但稳健性因阈值临近而有限。
3. **[clip_flip_validity] K4 降级因低预算而仅限 "at this budget"。** verdict_flip=False 确实如此，但 FPR 0/0 是地板值，预算缩小了 7 倍。所以与其说"firm refutation"，不如说"not load-bearing at this budget"。

3 个都不至于"把结论翻盘"，但全部朝着"削掉说过头的部分"的方向起了作用。这次自我审计正是今天成果的一半。

---

#### 8. 老实写下自己踩过的一个坑

在上次的谷深 workflow 中，我在第 2 段协调器 briefing 里传入了 **stale (旧) 值。** 像"全部 below threshold / d*=0.1234"这样的值。可实际 commit 的结果 JSON 是 `all_below_threshold=false`。我在读上次 workflow 结果时，把另一个 metric 的值搞混了。

**敌对验证检出了这一点，把 verdict 降级为 N/A。** 也就是说，怀疑自己"过于整齐的结论"的这个过程，抓住了我自己的复制粘贴失误。这不是个令人愉快的故事，但正因为它转起来了，今天的 Step D 才能从正确的立足点重新测量。

我再次体会到，honest disclosure 不只是"不抹掉失败"，更是"**预先放置一个能检出失败的机制**"。

---

#### 9. 我是如何更新过去 verdict 的

| 过去 verdict | 过去的解读 | Step D 的更新 |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **方向更新：③ 朝 NOT null 的方向 (fresh n=64 下 gate PASS)。** 但止步于候选 |
| step6 exp7 (真实 ESN proxy, ③ negative) | n≤10 盲点域，"必须重测" | **大幅更新：地形本来就平滑 (③ 不需要)，noise-free 确定。** 重测也不会出现多峰 |
| 谷深 N/A (无法测量) | instrument 不能 | **解除：靠决定论化使其可测** → vf≈0 (单峰)。但阈值临近的浅谷是保留项 |
| K4 clip = 唯一的主动 suppression | "clip 隐蔽了 landscape 结构" | **降级：诊断性所见** (not_load_bearing_at_this_budget) |

"看起来像'③ 不需要'的许多过去 negative，不是 underpower，而是因为地形本来就平滑"── 这一点首次在真实 substrate 上得到确认，正是今天的核心。

---

#### 10. 外部评审 (Codex) 无阻断项地追认

作为 llcore 的纪律，每个 capstone 都要通过 Codex (gpt-5.4, read-only) 的结对评审。这次的总评是 **"无阻断项 ── ③ 结论已获外部确认"。**

- 把 C-gen4b 留作候选而非 load_bearing 的判断是妥当的 (已在 JSON 中确认更新检出力 0.5174 < 0.80)。
- EXP2 的决定论、非循环是 clean 的。也追认了正文的自认："阈值下的弱 multi-basin"比"真正单峰"更精确。
- EXP3 的 K4 降级在现预算下是妥当的 (FPR 0/0 + 缩小 7 倍，故仅限 at-this-budget)。

被指出的 4 项 (CF1～CF4) **全都是关于未来 rerun 时 harness 的稳健性和文字精度**，并不推翻现结论。在 GPU 上复检 ③ 时，会先应用这些，再重用 harness。

---

#### 11. 我们当时在尝试 CPU 的逃生路线 (kernel 多样化 / BG9)

"③ 的主战场移到 GPU (真实 LLM 的损失地形)"是 EXP2 的建议。既然真实 proxy 已确定平滑，在平滑地形上追 ③ 也不会出 (A) (地形若是单座山，挑选分离自然没有收益)。

但因为 GPU 是投资决策，我并行尝试着 **一个可以在 CPU 上前进的别的假说。** 那就是 **kernel 多样化。**

假说是这样的。即使各个 kernel (rwkv / mamba / hopfield / linear_attn) 各自都平滑，**把 4 种 kernel 族 union 起来，可能会在 kernel 切换的瞬间让 fitness 产生不连续的台阶 → 地形可能变成 multi-basin (欺骗地形) → ③ 可能不用 GPU 就在 CPU 上成为 load-bearing。** 验证这个的就是 BG9。

在我最初写这篇文章的时候，还是"现在正在 smoke 测量 BG6 (task → best-kernel 映射是否非常数，即'每个任务擅长的 kernel 是否不同')"。在那之后 (同在 2026-06-02 之内)，BG9 有了定论。下一节追记就是它的结局。

---

#### 11.5. 追记 (2026-06-02): BG9 定论 —— 逃生路线在结构上被堵死了

> 结论一句话：**BG9 = N/A (结构性)。也就是说，kernel 多样化这条 CPU 逃生路线被堵死了，因为"③ 立不起来"在结构上是注定的。** 这不是"③ 不需要"，而是"在这个空间里，③ 在原理上无法与强 baseline 分离"——一个有信息量的 negative。

§11 设下的逃生路线的结果出来了。期待中的"kernel union 生成 multi-basin (欺骗地形)、③ 在 CPU 上立起来"**没有发生。** 而且不是"碰巧没立起来"，而是查明了 **在结构上就立不起来。** BG9 用 3 层证据确定了这一点。

##### (1) substrate validity ——"有辨别但弱" (PASS 但需注意)

首先，把 kernel-favoring task 群从第一原理重新设计，再去测量"每个任务擅长的 kernel 是否不同" (BG6)，映射是 **非常数 = 非 inert (PASS)。** mamba / linear_attn / rwkv 各自在不同任务上成为 best。从避开了 BG6 踩过的"memory_tasks 对 kernel 中立"的覆辙这个意义上说，是前进了。

但老实说 **弱**：

- **hopfield 在任何任务上都没能赢。** 这是因为 hopfield kernel 是 **对角标量 mock**，其 tanh 吸引子功能失常 (per-seed 的 R² 在 0/0.99/0 上两极分化)。所以它实质上不是"4 kernel union"，而是 **3 kernel。**
- clean 的专门化只有 2 个轴 (selective_copy↔mamba / weighted_accum↔linear_attn)。其余 margin 很薄、fragile。

→ **辨别的存在 ≠ 多峰/障壁。** 非 inert 化成功了，但那并不保证欺骗地形——只到这一步为止。另外，对角 mock 的局限正如 kernels.py 的 scope 声明，这里 **只主张机制的 feasibility** (不主张 full kernel 性能)。

##### (2) harness validity —— positive control 不 validate (这是决定性的)

接下来是主战场。在固定参数 (behavior=(kernel_id, theta L1)) 下，把 MAP-Elites (③) 与 3 个 baseline ── **RR-hillclimb (random restart 登山)** / panmictic-GA / random ── 做了 honest 的 paired 比较。

| 基质 | 结果 |
|---|---|
| **positive control** (合成 kernel-barrier) | ③ 击溃 panmictic (+0.423) 和 random (+0.208)。**但赢不了 RR** (+0.051, p=0.31 → FAIL)。未达到 3 baseline 全胜 = **harness validity 立不起来** |
| **negative control** (kernel 中立任务) | 全 method R²≈1.0 饱和，③ 无优势 = **正确地 null** (无假阳性，仪器健全) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3，panmictic 反而超过 ③ = **③ 不胜** |

这里就是与 Step D (技术版 §4-7) 决定性不同的地方。在 Step D 的欺骗 corridor 上，③ 能够排除 RR。**为什么在 kernel 空间里不行？** 根因只有一个：

> **RR 在每次 restart 时都能直接采样 kernel_id ∈ [0,4)。** kernel 选择是 4 离散的单一座标 (低维)，所以 RR 在 restart 时会直击全部 4 个 kernel。要"找最佳 kernel"，无需跨越山谷 = **teleport (直接传送)。** 所以 ③ 的 behavioral niching 没有登场的机会。

③ 在 Step4 的 corridor 上能排除 RR，是因为那里的 behavior 是 `mean(24 维)`，由 CLT，均值集中到 0.5 → 全局峰是 measure-zero 区 = **random/RR 无法直接采样的高维。** kernel_id 反过来是低维，可以被直接采样。

##### (3) red-team —— 即使用敌对验证也无法反证，反而成了确证

我们用独立的 red-team 捶打"harness 立不起来真的是结构的缘故吗？会不会是碰巧的设置失误？"。结果 **无法反证结构主张，反而强化了它**：

- **机制确证**：instrumented RR 在 positive control 上，把 restart kid 几乎均匀地分散到 4 个 basin 上 [12,18,16,18]，target 到达 88%，best 在 6/8 seed 上是 restart→in-basin climb。**用数值确证了**"RR 在 restart 时直接采样 kernel_id 来回避山谷"。
- **在 4 个 faithful 构成 (高维 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) 上，③ 都赢不了 RR (beats_rr=False)。** 把 corridor 放松，RR 也同等到达；把它收紧，③ 反而 **先饿死 (starve)。**
- **边界 sweep**：把 theta corridor 的维度 D=0→3 越收紧，③ 比 RR 饿死得越快 (D=3: ③ reach 0.08 vs RR 0.42)。在 3 个 base_seed 上相同。

→ 定量确证了 **"只排除 RR 而让 ③ 通过的 behavior 维度，在 kernel 空间里结构上并不存在"。**

##### 结构性洞察 (这次定论的 payoff)

> **③ (MAP-Elites 的 behavioral niching) 超过强 baseline，只有在"难处"位于高维 behavior 空间、用直接采样 (random restart) 无法到达的时候。**

- **kernel 选择是低维 (4 离散的单一座标)** → RR 直接采样 → ③ 的 niching 优势在原理上无法出现。
- 即使把欺骗移到 theta 空间，RR 在 restart 后会在 in-basin 做 greedy climb，所以把 corridor 收紧到 RR 无法通过的程度时，③ 也会以同等程度饿死。**RR fail ∧ ③ succeed 的窗口并不存在。**

这是对 Step4 §7 残留问题"靠 kernel 多样化扩展搜索空间，③ 会 unlock 吗？"的回答。答案是 **NO (在 CPU 上是结构性的)。** 要让扩展 unlock ③，追加的自由度必须产生一个 **高维、难以直接采样** 的 behavior。kernel 选择 (低维、离散) 不满足这个条件。

##### 对 GPU 的含意

- **CPU 出尽门 CLEAR**：BG9 在结构上堵死了最后的 CPU 路线 (kernel-union)。③ 剩下的路线 **只有高维的 GPU full-LLM 损失地形。**
- 结构性洞察让 GPU 这场赌注 **better-motivated。** ③ 只有在高维 behavior 中才有意义。full-LLM 的参数空间是数百万维 = 正是高维。所以 GPU 检定遵循一条原理——不是"也许 full-LLM 是唯一例外"这种弱赌注，而是"③ 需要高维，而 full-LLM 处于高维域"。
- **但它依然是赌注**：如果真实 LLM 地形能被 backprop 系的强 baseline 直接导航，那 ③ 就不需要 ── 这是与 **BG9 的 RR 同型的风险** ("强 baseline 直接解出"的可能性在 GPU 上也依然存在)。所以 GPU 不应"单独为 ③"，而应作为 **组合判断** (与 llive 真实 LLM fitness 等搭车) + **借云做 1 次预注册** (在资本投入之前)，才算适当。BG9 的结构性洞察本身就成了 GPU 的可证伪 go/no-go 标准："如果 ③ 在 full-LLM 上 load-bearing，那它的难处应该位于高维 behavior 空间，并且用直接采样/backprop 难以到达。"

##### honest 保留 (重要)

- 这 **不是"③ 被查明不需要"。** "③ 在这个低维 kernel 空间里，原理上无法与强 baseline 分离" = N/A (结构性)，而 ③ 的机制本身在 Step4 已确定是真的。它是一个 **有信息量的 N/A**——虽然是 N/A，却携带了"kernel 路线已堵死"这一决定性信息。
- harness/red-team 是 smoke 规模 (5-12 seed)。在正式检定的 15 seed 下数值会动，但 **结构 (收紧则 ③ 先饿死 / RR 直接采样 kernel_id) 与 seed 无关、稳健。** 我们不会在 real 上跑 full ≥15-seed 的正式检定 ── 既然 positive control validity 在结构上立不起来，即便在 real 上出了"③ 不需要"，也无法分离"③ 不需要 vs 检测器盲"，而这个"检测器盲 = kernel 空间的结构"已被 red-team 确定，所以即使投入 7.5h 的 CPU，结论也不会改变。
- substrate 弱 (实质 3 kernel，**hopfield 是对角 mock、功能失常**)。若有更强的 kernel 辨别 (full 实现、非对角)，则有不同结论的余地——这 **在理论上** 是有的，但 ③ 的结构性障壁 (低维选择 → RR 直接采样) 与 kernel 实现的质量无关。
- 这次 **不需要** 那条怀疑"③ 过于整齐地成立"的纪律 ── ③ 成立从一开始就没出现 (与 honest prior 一致的 negative)。

---

#### 12. 元教训 —— 诚实，是为了取胜的工具

今天真正的成果不是数值，而是 **"怀疑过于整齐的结果"这种精神，实际推动了研究前进。**

- 因为物理性地消除了评估噪声 (EXP2)，我们才能切分"平滑"到底是地形的性质还是仪器的极限。
- 因为用了 3 个敌对验证透镜，我们才没把"③ NOT null"做成 headline，而是把它留作"候选"。
- 因为我自己检出了 stale 值的混淆，我才能做出正确的降级到 N/A，并在今天重新测量。
- **在 BG9 (追记) 中又学到一点**：**低维的难处会被强 baseline 直接解掉。所以要让 ③ (挑选、培育的工夫) 起作用，需要"高维 behavior 空间"。** "做出欺骗地形 ③ 就立"只对了一半，精确地说，地形必须是 **高维到无法直接采样的** 欺骗地形，③ 才会立起来。在 kernel 4 选 (低维) 的情况下，RR 在 restart 时把它们全部直击，所以 ③ 的登场在原理上就没来。这正是把逃生路线说成不是"放弃"而是"**结构性堵死**"的依据。

"出现异常好的结果时，在飘飘然以为赢了之前，务必怀疑其内幕"── FullSense 的研究纪律 (`feedback_benchmark_honest_disclosure`)，不是单纯的自我警诫，而是作为 **实际抓住假阳性、提高研究精度的机制** 在运转。BG9 是同一纪律在相反方向 (**把 negative 正确地确定为 negative**) 上奏效的例子 ── 在 red-team 里试图反证自己的"③ 立不起来"，结果反证不了，反而作为结构得到了确证。

最后，再把结论精确地说一遍 (反映 BG9 的定论)：

> **在 proxy substrate 上，"③ 因地形真正平滑而不需要"被 noise-free 地确定** (Step D)。只有在真实 multitask 邻域 (C-gen4b) 出现了"③ NOT null"的微弱迹象，但因小效果 + 漂移 + 多重比较，它 **止步于候选。** K4 clip 从主动 suppression 降级为诊断性所见。而最后的 CPU 逃生路线 **kernel 多样化 (BG9) 在结构上被堵死** ── kernel 选择是低维，所以强 baseline (RR) 直接采样，③ 的 niching 优势在原理上无法出现。**验证 ③ 主战场剩下的路，只有高维的 GPU full-LLM 损失地形** (这本身也是一场带有"强 baseline 直接解出"风险的赌注)。

"③ 定论 = ③ 被查明不需要"是错的。正确地说，**"③ 只有在'高维的'欺骗地形上才发挥作用。这次在 CPU 上能测到的、接近真实的东西 (平滑) 和 kernel 多样化 (低维)，都不满足这个条件。"** 主战场 (高维 GPU) 还在前方，而且是一场没有保证的赌注。

---

**Tags**: 进化计算 / MAP-Elites / 统计检验 / 检出力 / honest disclosure / CPU 研究
**相关**: 连载 #32 (llcore CPU PoC battery) / #29 (反证・Goodhart・proxy 局限) / #31 (Codex 二本柱)
**Project**: llcore (PyPI 预留 llmesh-llcore，因仓库未公开为本地研究)

---

## 10. llcore — 「進化で AI を設計するとき、選り分けて育てる工夫 (③) は要るのか」を 6 段の実験 + 生物学で俯瞰した話 (第三軸 arc 全体)

### (连载 #34) 六连战爬山实验弄清了「进化的③何时起作用」——而且 100 年前的进化生物学早已给出同样的答案

#### TL;DR

- 问题是 **「用进化去搜索 AI 的核心计算时,『分门别类、隔离培育的工夫』(= 进化的③:适者生存/分离) 到底需不需要」**。连载 #33 写了终局 (Step D + BG9);**而本篇 #34 把整段 arc (6 段) 当作一个故事来俯瞰**。
- **第 1 段 (合成欺骗地形)**:③ 大获全胜 (Cliff δ=+1.0)。③ 作为机制是真货 = **存在证明**。
- **第 2 段 (记忆任务 / 多 reservoir)**:被基质的「地板」与「天花板」所阻,无法测量③ = **N/A**。
- **第 3 段 (多任务泛化)**:③ 能赢「无选择」,但赢不了简单选择或 random = ③ 不需要 (honest negative)。
- **第 4 段 (对真实 proxy 地形做 noise-free 测量)**:把评估噪声物理性地降到零之后,地形 **确实是光滑的 (单峰)** = ③不需要被确证。「过去的 negative 不是检定力不足,而是地形本来就光滑」第一次得到佐证。
- **第 5 段 (混合 4 种部件的旁门左道 BG9)**:kernel 选择是 **低维**,因而强 baseline (随机重启爬山) 直接采样,③ 的 niching 优势 **在结构上**不出现 = 旁门左道被堵死。
- **结构性洞见 (本 arc 的核心)**:③ 起作用,只有当难点位于 **高维 behavior 空间**、无法直接采样时才行。真实 CPU 基质是低维/光滑的,所以③不需要。
- **生物学接地 (已验证)**:这恰恰就是赖特 (Wright) 的 **转移平衡说**。对 **黑化型蛾 (单基因 = 低维)**,普通的选择就足够 (= BG9 的 kernel 情形);对 **伦斯基的 Cit+ (高维、依赖历史)**,多样性才起作用 (= ③ regime)。我们的 negative 就是 **科因批判的计算版** (现实地形简单、③ 极少起决定性作用)。
- **元教训**:「太顺利的结果不是胜利,而是警报」。预先登记、honest disclosure、对抗式验证、确定性的 noise-free 测量,使我们避免了空欢喜。

> ⚠ 本文中的所有数值,都是与手头 (本地) 研究记录绑定的实测值。llcore 还没有建公开仓库,所以无法贴出外部链接。作为替代,我在正文里写了「是怎么测的」。生物学部分引用的论文,只列出那些已单独对照一次信息源、核实过其存在、归属与主张内容的。

---

#### 0. 这篇文章在讲什么 (概念)

`llcore` 是一个 CPU 完整的研究框架,它「把 Transformer 的核心计算 (状态更新规则、学习规则、认知驱动 Δ) 当作基因,一边用 Z3 验证它不会坏掉,一边进化」。

它的进化引擎有一个设计上的要害:在进化的 4 要素 (① 变异 / ② 遗传 / ③ 适者生存・分离 / ④ 过剩繁殖) 之中,**③ (selection / separation)** 该如何发挥作用?这是像 MAP-Elites 那样、保持多样性并留在生态位里的「分门别类、隔离培育」机制。

问题很简单。

> **那个③,真的需要吗?**

如果需要,那么为承载③而做的重投资 (最终是在 GPU 上跑真 LLM) 就有意义。如果不需要,那么执着于③就是浪费时间与电费。

连载 #33 详细写了那个问题的 **终局** (Step D 的确定性测量 + BG9 的结构性了结)。但在抵达那里之前,有 **6 段实验**,反复地赢 (存在证明)、测不出来 (N/A)、输 (honest negative)。本篇 #34 把 **整段 arc 重新排成一个故事**。而且作为本次的看点,我们用已验证的一次信息源 **接地**:**这个计算结果与近 100 年前进化生物学的论争 (赖特 vs 费希尔) 在形状上惊人地相同**。

— 到这里 40 秒。热身完毕。进入正题。 —

---

#### 1. 比喻:爬山、欺骗地形,与记忆宫殿

在公式之前,我们用本研究始终使用的 3 个比喻来把握全貌。

我们用 **地形的高度** 来表示设计的好坏。**高的地方 = 好的设计**。这是一场寻找最高峰的游戏。

**地形其一:光滑的单座山 (简单)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

在这样的地形里,朴素的「爬山法 (hill-climbing)」,也就是「只往比现在稍好一点的方向移动」,就足以登顶。**花哨的工夫 (③) 不需要。**

**地形其二:欺骗地形 (deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

这里,朴素的爬山会停在假峰,因为它没有下到谷里的勇气。

这时起作用的就是③的想法。**把各种各样的登山者散布留在谷的各处** (= 记忆宫殿 / MAP-Elites archive)。某个人能用「踏脚石 (stepping-stone)」渡过山谷、抵达真正的山顶——这就是机制。

**用一句话概括本研究的核心**:③ 真正有用,**只在「欺骗地形」时**。在光滑的单座山上,③ 是无用的大白象。

所以问题可以改写成这样。

> **「用进化来设计 AI 时,你实际遇到的地形是『欺骗地形』,还是『光滑的单座山』?」**

#33 中我们用 Step D + BG9 给这个问题作了了结。本篇 #34 展示通往那里的 **全部 6 段爬山**。有趣之处在于,每一段「是不是欺骗地形 / 是不是光滑 / 能不能测量」都会变化。

— 小憩。准备到此为止。从这里开始是六连战的实录。 —

---

#### 2. 整段 arc 地图——一览 6 段爬山

先把地图拿出来。这是本文的脊梁。

| 段 | 基质 (测的是什么地形) | ③ 起作用了吗 | 一句话 |
|---|---|---|---|
| **I (Step 4)** | 合成的「欺骗地形」(欺骗 corridor) | **Yes (完胜)** | 存在证明。③ 是真货 |
| **II (Step C / 梯子1)** | 记忆任务 / 多 reservoir 奇偶 | **N/A** | 被地板、天花板、degree-5 之墙挡住,测不出来 |
| **III (E-A)** | 多任务泛化 | **No** | ③ 能赢「无选择」,仅此而已 |
| **IV (Step D)** | 真实 proxy 的文本地形 (确定性测量) | **No** | 确证地形 **确实光滑** (noise-free) |
| **V (BG9)** | 部件 (kernel) 4 种的并集 | **No** | **在结构上**被堵死 (低维选择) |

故事线是这样的。**首先证明存在——「③ 在条件合适时确实大获全胜,是真货」(I);接着,为了问「那么在真实问题里如何」,跨 4 段去测量 (II–V),结果每一次都是「真实 CPU 基质是不需要③的地形」**。而且在最后 (IV, V),确认了「不需要的理由」是 **地形的性质,而非检定力不足**——这就是整段 arc 的弧。

那么,一段一段来。

---

#### 3. 第 I 段 (Step 4)——存在证明:若是欺骗地形,③ 会完胜

最先做的,是「**按理论该起作用的场面是否真实存在**」的存在证明。我们 **故意把地形做成欺骗式**,让③ (MAP-Elites) 与 3 个 baseline——pure random / panmictic GA / **随机重启爬山 (random-restart hill-climbing)**——对决。

**地形的构造**:基因是 24 维。把 behavior (登山者的类型) 定义为 `mean(基因)` = 24 个数的平均。要提高 behavior,就得 **同时把全部 24 维抬高**。fitness 恰恰是欺骗地形:「behavior≈0.4 处有假峰 (值 0.6) → behavior≈0.65 处有谷 (值≈0) → behavior≈0.9 处有真峰 (值 1.0)」。

**结果**:

| 方法 | 抵达真峰的比率 | 与 ③ 的比较 |
|---|---|---|
| **MAP-Elites (③)** | **约 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | 同上 |
| 随机重启爬山 | 0% | 同上 |

只有③抵达了真峰,3 个 baseline 全都停在假峰 (≈0.60)。**100% 胜 / 效应量为理论最大 (δ=+1.0)**。在 3 种 base seed (共 60 seed) 上稳健。

为什么会这样,会成为后文的伏笔。

- **random** 的 behavior 必然集中在 ≈0.5 (24 个数的平均被中心极限定理锁在 0.5)。所以它 **永远到不了** behavior 0.9 (抽 6000 个样本也是 0%)。
- **爬山** 爬到假峰 0.6,拒绝下到谷里那一手。即便重启也回到 behavior≈0.5,落入同样的陷阱。
- **③ (MAP-Elites)** 把谷的格子当作「新的 behavioral 生态位」保留,**用踏脚石把 behavior 从 0.5 渡到 0.9**。

**边界我们也诚实地测了**。在去掉谷的光滑 corridor 上,③ 已赢不了爬山 (p≈0.29)。**③ 不是万能的,它只在欺骗地形里起作用。**

**honest 保留**:这是 **故意做出来的** 合成地形。它只证明了③「可能」,并没有证明真实任务具备这种结构。toy 规模、低噪声、baseline 是朴素的 (1+1)。

→ 这里立起一个假设:**「如果真实问题的地形也这么欺骗,③ 应该能活起来」**。接下来的 4 段,就是在更接近真实问题的基质上去验证它的旅程。

— 歇一会儿。第 I 段是令人舒畅的完胜。从这里风云突变…… —

---

#### 4. 第 II 段 (Step C / 梯子1)——被基质的「地板」与「天花板」所阻 (N/A)

接着我们调查「欺骗 corridor 会不会 **在标准的记忆任务里自然出现**」(Step C)。用 1 个 leaky reservoir + ridge readout 跑 delayed parity / flip-flop / delayed recall。

结果是干净的 **N/A (不可测)**。原因有趣在于两个极端。

- **delayed parity = 地板 (floor)**:单个 reservoir 算不出 XOR (Minsky-Papert)。所有方法都是 R²≈0.003。谁都登不上去,所以无法分离③。
- **flip_flop = 天花板 (ceiling)**:所有方法都饱和在 R²≈0.95。方差被压垮,③ 的差异显不出来 (③ vs random 符号为正但 p=0.15 = underpower,因此 **并非 null**)。

这里有一个重要发现。**基因空间的多峰性很高** (parity 的 valley fraction 是 1.000),却对③毫无用处。也就是说,**「在基因空间多峰」≠「需要跨越的 behavior 欺骗地形」**。这个区别成为 arc 后半的钥匙。

**梯子1 (多 reservoir)**:那么,把多个 reservoir 串起来,地板会不会抬高?→ 试了 5 种机制全是 `floor_lifted = false`。深度 (DeepESN) 在统计上抬高了地板 (效应 +0.47/+0.60, PASS),但绝对值止步于 R² 0.05-0.10。决定性的是 positive control:degree-2 readout 严格解出 2-bit XOR (R²=+1.0),但 degree≥3 即崩溃。**5-bit 奇偶是 degree-5 = 这个 CPU reservoir+ridge 范式的结构性之墙。**

→ 奇偶之路在结构上被堵死。③ 的正式检定需要 **从奇偶上下来**。

**honest 保留**:degree-5 之墙是「这个设置的墙」,不是对整个范式的不可能性证明。

— 小憩。「测不出来」的结果虽朴素,但在画地图时是重要的空白地带。 —

---

#### 5. 第 III 段 (E-A)——多任务泛化:③ 不需要 (honest negative)

从奇偶的地板下来,我们用 **泛化 (generalization)** 来测③,组了一个最干净的 ablation。

**设置**:单层 leaky reservoir + ridge。可变延迟的 recall。**用短延迟 {15, 30} 训练,用长延迟 {45, 60} 测试** (外推)。比较的是 MAP-Elites (①②③全) vs **抽掉选择的 MAP-Elites** (`randselect`:随机选父代、无条件放置 = 只有变异) + panmictic GA + random。

**结果 (同行评审后)**:

| 方法 | 测试泛化 R² (平均±std) |
|---|---|
| MAP-E (①②③全) | 0.682 ± 0.115 |
| MAP-E randselect (抽掉选择) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| 门 | 比较 | diff | p (单侧) | 判定 |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**读法**:③ 赢了「**抽掉选择的漂移对照**」(C-gen3 PASS = "某种选择胜过无选择")。但 **赢不了 panmictic GA (有选择但无 niching)** (甚至略输),也赢不了 random。也就是说,**niching 特有 (= ③ 本来) 的贡献为零**。这个泛化地形足够 **光滑**,以至于简单选择或 random 也能到同一个地方。这与第 I 段的边界「光滑则③不起作用」一致。

**honest 保留 (重要)**:这个 verdict **仅限于这个设置** (预算 400, grid 6×6)。此外——这里是 honest methodology 的要害——同行评审 (Codex) 起初判定「不可信」,强制了 3 个 rerun blocker (每个 replicate 独立 seeding / 采用预算内的全局最优 / 把 honest_n 从 16→30)。**修正之后结论仍未改变。** 收获是:它不是「一改就翻的脆弱 negative」。

— 歇一会儿。输就是输,但确认我们「正确地输了」的工作更花时间。 —

---

#### 6. 第 IV 段 (Step D)——真实 proxy 地形被确证为「确实光滑」(noise-free)

这里是 arc 的转折点。直到第 III 段,「③ negative」一直在持续,但始终有一个 **疙瘩** 残留着。

> 「③不需要」真的是因为 **地形光滑** 吗?还是仅仅 **样本数不够、检测不出差异 (underpower)** 呢?

弄错这一点,就会过度泛化为「③ 无力」。Step D 在这里作了了结。

**诀窍**:ESN reservoir (固定 seed) + ridge readout 的闭式解 (`np.linalg.solve`) **完全不抽随机数**。所以可以把评估噪声物理性地降到 **机器 epsilon (约 1.11e-16)**。实测确认了 `eval_noise_std ≤ 1.11e-16`——这源自浮点的最小单位 (ULP),**实质为零**。把噪声之雾完全拨开,就能直接测量地形的谷。

地形是 llcore 自身源码 (约 24k 字符) 的下一字符预测。我们测了 valley_fraction (谷的比例;≥0.2 即多峰 = 欺骗地形)。

| 地形 | 维数 | valley_fraction (mean/max) | 多峰? | 判定 |
|---|---|---|---|---|
| **ESN 3-param** (真实 proxy) | 3 | **0.000 / 0.000** | No (3 seed 一致) | 光滑 → noise-free 确证③不需要 |
| **ESN per-neuron** (真实 proxy) | 40 | **0.096 / 0.121** | No (3 seed 一致) | 偏光滑 → ③ 不需要 |
| 多峰 control (正) | 3 / 40 | 0.70 / 0.80 | Yes | 诊断器能检出多峰 ✓ |
| 二次函数 control (负) | 3 / 40 | 0.000 | No | 诊断器能检出光滑 ✓ |

要点有 2 个。

1. **真实 proxy 地形 (3 维 / 40 维均如此) 是单峰**。3 个 seed 一致。
2. **诊断器本身是健全的**。故意做的多峰被正确检出为多峰,二次函数被正确检出为光滑。所以「真实 proxy 是单峰」不是仪器的 bug,而是 **地形的性质**。

→ 这才第一次在真实 substrate 上 noise-free 地佐证了 **「过去的③ negative 不是 underpower,而是地形确实光滑」**。再测也不会出现多峰。

**honest 保留 (重要)**:「光滑」只在阈值附近才精确。**ESN 3-param 的 midpoint 有 90.9% 略微向下 dip**,最大相对 dip (0.0435) 就在谷阈值 0.05 的正下方。准确说,它不是「**真正单峰**」,而是「**带有略低于阈值的浅谷 (~2-4%) 的弱 multi-basin**」。方向得以维持,但因贴近阈值,稳健性有限——不把它圆成「完美的凸碗」,是本次的纪律。

— 深呼吸。到这里「仿真之物是光滑的」已确证。剩下的是「最后的 CPU 旁门左道」。 —

---

#### 7. 第 V 段 (BG9)——混合部件的旁门左道,在结构上是堵死的

既然真实 proxy 已确证为光滑,在光滑地形里追③就不会出利得。但 GPU 是投资判断,所以我们试了 **能在 CPU 上前进的另一个假设**。那就是 **kernel 多样化 (BG9)**。

**假设 (预先登记 H7)**:即便单个 kernel (rwkv / mamba / hopfield / linear_attn) 各自光滑,**把 4 种并集起来,在 kernel 切换的瞬间 fitness 会形成台阶 → multi-basin (欺骗地形) → ③ 不靠 GPU 就在 CPU 上立得住**。预先登记的 honest prior 偏 **null** (因为迄今所有 CPU 基质都光滑)。

结果分 3 段。

**(1) substrate validity——有辨别但很弱 (PASS 但需注意)**:测量每个任务的拿手 kernel 是否不同,映射是非常数 = non-inert (PASS)。mamba 在 selective-copy、linear_attn 在 weighted-accumulation 上最佳。不过 **hopfield 在任何任务上都赢不了** (对角标量 mock 下功能失常),所以实质是「**3 kernel** 并集」。**辨别的存在 ≠ 多峰障壁。**

**(2) harness validity——positive control 无法 validate (决定性)**:在合成 kernel-barrier 上,把③与 3 baseline 比较。

| 基质 | 结果 |
|---|---|
| **positive control** | ③ 击溃 panmictic (+0.423)、random (+0.208)。**但赢不了 RR (随机重启爬山)** (+0.051, p=0.31 → FAIL)。未能全胜 3 baseline = harness 立不住 |
| **negative control** | 全部 method 饱和,③ 无优势 = 正确地 null (仪器健全) |
| **real** smoke | ③ beaten 0/3,panmictic 反而超过③ |

第 I 段的 corridor 里③能把 RR 排除出去,**为什么在 kernel 空间做不到?** 根因只有一个。

> **RR 在每次 restart 都能直接采样 kernel_id ∈ [0,4)。** kernel 选择是 4 个离散值上的单一坐标 (**低维**),所以 RR 在 restart 时直接命中全部 4 个 kernel。「找最佳 kernel」无需跨谷 = **直接传送**。所以③的 behavioral niching 没有出场机会。

第 I 段③能排除 RR,是因为那里的 behavior 是 `mean(24 维)`,平均集中在 0.5 → 全局峰在 measure-zero 区域 = **高维、无法直接采样**。而 kernel_id 相反,是低维、可直接采样。

**(3) red-team——对抗式验证也无法反证,反而确证**:在 positive control 上,instrumented RR 把 restart kernel 在 4 个 basin 上近乎均匀分散为 [12,18,16,18],target 抵达率 88%。在全部 4 种 faithful 构成 (高维 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) 中,③ 都赢不了 RR。把 corridor 收紧,③ **先饿死 (starve)** (D=3:③ reach 0.08 vs RR 0.42)。我们定量确证了 **「能把 RR 单独排除、又让③通过的 behavior 维度,在 kernel 空间里结构上不存在」**。

**verdict**:形式上是 N/A (positive control 无法 validate),但实质是 **决定性的结构性 negative**。harness 是健全的 (它正确地把 negative control 置 null,并检测出 GA/random),然而基质 **根本无法承载③的欺骗地形**。对第 I 段遗留的问题「用 kernel 多样化扩展搜索空间,③ 会 unlock 吗?」的回答是 **NO (在 CPU 上,结构性地)**。

**honest 保留 (重要)**:这 **不是「③不需要被判明」**。它是「③ 在低维 kernel 空间里原理上无法与强 baseline 分离」= **有信息量的 N/A**。③ 的机制本身在第 I 段已确证为真货。substrate 很弱 (实质 3 kernel;hopfield 是对角 mock)。更强的 kernel 实现在理论上有得出不同结论的余地,但 **结构性障壁 (低维选择 → RR 直接采样) 与 kernel 实现的质量无关**。

---

#### 8. 结构性洞见——用一个条件统合 6 段

存在证明 (I) 与 4 个 negative (II–V),全都在仅仅一个条件下连成一体。

> **③ (behavioral niching) 超越强 baseline,只在「难点」位于高维 behavior 空间、无法用直接采样 (随机重启) 抵达时。**

- **第 I 段满足的理由**:behavior = `mean(24 维)`。平均被中心极限定理集中在 0.5,全局峰 (mean≈0.9) 实质 measure-zero。random 和 restart 都 **够不着**。所以留下踏脚石、做 ratchet 的③是必需的。
- **真实 CPU 基质不满足的理由**:难点是低维。ESN 文本 proxy 的控制坐标实质是 leak rate (光滑的低维旋钮;本就没有谷)。kernel union 的难点是「哪个 kernel」= 4 选 1 的单一离散。RR 直接采样、传送到全部 basin,所以没有需要跨的谷。

所以第 II 段的「基因空间多峰性 1.000」不是充分条件——即便基因满是谷,只要难点集中在低维 behavior 坐标上,restart 就能直接抵达。**起作用的是「探索需抵达的 behavior 的维数」,而不是基因的维数。**

---

#### 9. 生物学接地——100 年前的进化生物学早已给出同样的答案

从这里开始是 #34 的看点。**「保持多样性的选择,只在狭窄条件下起作用,其余时候是冗余的」**——这个边界条件,在 20 世纪的进化生物学里有一个异常干净的先例。

> ⚠ **honesty 契约**:以下生物学是 **「比喻 (structural analogy)」,而不是我们计算结果的证明**。对应是结构性的,在机制层面并不一致。比喻偏离之处,我都当场注明。引用的论文,只列出已单独对照一次信息源、核实过存在、归属与主张内容的。

##### 9.1 赖特 (Wright) 的转移平衡说 = ③ 的先例

休厄尔・赖特 (Sewall Wright, 1931/1932) 这样思考。若维持为一个大「群 (panmictic population)」,普通的自然选择会 **被眼前的局部峰困住**。要去更高的山,必须先 **降低 mean fitness、跨过山谷**,而确定性的选择拒绝这样做。

赖特的解法是 **把群分成众多半隔离的亚群 (deme)**。

- **Phase I**:小 deme 凭 **遗传漂变 (drift)** 偶然下谷、渡过去。
- **Phase II**:在那里,deme 内的普通选择登上新的 (更高的) 峰。
- **Phase III**:登上高峰的 deme 派出许多迁移者,优良的基因组合扩散到整个物种。

作为 **整个** 元群体,它跨越了单一收敛群体无法跨越的谷——这是「用踏脚石渡过欺骗地形的谷」的生物学版。

**对应到③ / MAP-Elites (= 比喻,非归属)**:archive 的每个 cell = 半隔离 deme,cell 内的局部 elitism = deme 内选择 (Phase II),cell 间变异 = interdeme 扩散 (Phase III),而 **archive 整体** (≒ 元群体,非单一 cell) 跨越山谷。

> **honesty 注意 (2 点)**:
> 1. **这是解说者的框架,既非赖特的主张,也非 MAP-Elites 的出处。** MAP-Elites 原论文 (Mouret & Clune 2015) 与 QD 文献 **都没有引用赖特或「转移平衡」**。赖特是作为我们的 **灵感 / 比喻** 提出的,而非 MAP-Elites 的谱系。
> 2. **机制只是结构相似,并不相同。** MAP-Elites 的渡谷是 **变异算子** 把子代放进新 cell 而发生的,**不是遗传漂变**。archive 也不是复制 cell 的群体。

##### 9.2 赖特 vs 费希尔 = 维数 (地形的形状) 之轴

与赖特同时代的费希尔 (R. A. Fisher, 1930) 主张相反:**大的 panmictic 群体 + 对加性方差的群体选择就足够** 让适应推进,根本无需特意分割。

二人 **最深的对立轴,其实是「上位性 (基因间相互作用) 与地形的形状」**。赖特假设「因非加性相互作用,地形 **崎岖多峰**,所以需要跨谷的 drift」,费希尔判断「相互作用存在但不重要,地形大致 **单峰、可平滑攀登**,所以群体选择就够」。

**这个 epistasis/ruggedness 之轴,正是我们结果生存的维度。地形的形状 (topology) 才是全部问题。** 若地形确实崎岖高维 (赖特 regime),多样性把你摆渡过谷;若光滑或难点低维 (费希尔 regime),群体选择——即强随机重启爬山的生物学版——就已足够。我们的 ESN 文本 proxy 是 noise-free 且光滑的,kernel union 的难点是低维离散。**两者都是费希尔 regime**,③ 不起作用、也没起作用。

> 细节注意 (诚实地):「费希尔忽视了 drift」是被压缩的俗说。准确说是「他承认 drift 存在,但判断在大群体里其量可忽略」。不是全盘否定。

##### 9.3 我们的 negative = 科因批判的计算版

最切中的对应,不是赖特的 **提议**,而是生物学界的 **经验判定**。Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) 从理论与实证两面评估了转移平衡说,并如此结论 (全文已对照)。

- **群体选择通常就够了。** 「几乎没有用赖特三段机制比用简单群体选择解释得更好的实例。」人为选择实验也没能证明「分割群体的选择比大群体的群体选择产生更大的响应」。
- **转移平衡起作用,只在有限、稀少的条件下。** 群体结构的经验估计表明「**drift 只能在被浅谷隔开的峰之间引起迁移**」(深谷靠 drift 极少能渡过),而且 **大多数适应不需要跨谷**。

这是我们结果的 **惊人精确的生物学版**。把他们的话翻译成我们的词汇就是——**若地形并非真正欺骗/高维,普通的群体选择 (≒ 强随机重启爬山) 就已经能解,多样性维持装置几乎什么都买不到。**「现实的谷通常浅、大多数适应不需跨谷」就是我们「**实际地形通常简单,所以 niching 是冗余的**」的生物学陈述。

> **honesty 注意 (3 点)**:
> 1. **他们没有「反证」转移平衡。** 他们明言 Phase I/II 可能发生,并举出 6 个经验事例。主张是 **更狭窄的、概率性的** (「难以称之为一般而重要的机制」),写「refuted」就过头了。
> 2. **论争尚未了结。** Wade & Goodnight (1998)、Peck et al. (1998,标题字面就主张「feasible」) 提出反驳,接着是 Coyne 等人 2000 年的再反驳、Goodnight & Wade 在同期的反驳。不可把 1997 批判当作「最终结论」来引用。
> 3. **生物拥有计算侧无对应物的机制,而且做出比我们更强的主张。** 在 Phase III,保护多样性的 gene-flow 障壁可能 **把好解困在周边 deme、妨碍其扩散** = niching 可能 **适得其反**。我们 stateless 的离散选择设置没有这个 cost 的对应物,所以这里 **不过度叠加**。这是生物做出更强主张的地方。

##### 9.4 两个实例——低维的蛾,与高维的大肠杆菌

我们的主张有两个极 (低维 = ③不需要 / 高维 = ③ 可能起作用),而进化生物学对每个都有干净的实例。

**低维之极——桦尺蛾的工业黑化 (= BG9 kernel 情形)**:*Biston betularia* 的 carbonaria (黑) vs typica (白) 受 **单一孟德尔座位、少数等位基因** 支配 (致因变异是向 cortex 基因的转座因子插入;van't Hof et al. 2011/2016),并受 **强方向性选择** (s ≈ 0.1-0.2;Saccheri et al. 2008;捕食在 Cook, Grant, Saccheri & Mallet 2012 中再确认)。最优在每个时点都是单峰,只随环境平移。**简单的方向性选择——贪婪爬山/随机重启的生物学版——直接固定更适应的型,多样性维持机制既不需要也未被调用。** 这恰恰就是 BG9:kernel 选择是 4 选 1 的低维单一座位,RR 直接采样全部 kernel,③ 在结构上无法分离。**黑化型 = BG9 kernel 情形的生物版。**

> 注意 (诚实地):过渡期会暂时保持多型,但那是由于 **空间环境异质 + 基因流动 (迁移-选择平衡)**,而非内在的多样性保存机制。比喻略微偏离之处。

**高维、依赖历史之极——伦斯基的 Cit+ (= ③ regime)**:在大肠杆菌长期进化实验 (LTEE) 中,需氧柠檬酸利用 (Cit+) 在 **12 个群体中恰好 1 个** 里于约第 31,500 代进化出来 (Blount, Borland & Lenski 2008)。关键是一条高维、依赖历史的路径,即有序的 **potentiation (前驱变异的积累) → actualization (citT 串联重复带来的启动子捕获) → refinement** (Blount et al. 2012)。重放实验把「历史偶然性」从「恒定率的稀有变异」中区分开来。这 **真正例示** 了探索 contingency、上位性与高维崎岖地形的价值——是③可能起作用之 regime 的实例。

> **honesty 注意 (这只对应我们条件句的「前件」)**:
> - **LTEE 不使用 niching 算法。** 它就是普通的自然选择,12 个并行群体 **本身就是随机重启式的设计**。所以它是「contingency + 多样性使稀有创新成为可能」的存在证明,**不是**「niching 胜过强 restart baseline」的证据。
> - 「大肠杆菌从零获得吃柠檬酸的能力」是俗说的夸张。创新是 **调控 (既有转运体的需氧表达) = exaptation**,既非新基因也非新生化。
> - Van Hofwegen et al. (2016) 指出「若直接选择,Cit+ 出现得快得多」,挑战了「稀有/偶然」框架 (伦斯基一侧反驳说这与 LTEE 条件下的 potentiation 并不矛盾)。若要依赖「极稀有/长期延迟」叙事,就应一并注明这个 **有争议的追试**。

##### 9.5 接地小结

| 极 | 生物学 | 地形 | ③ 起作用? | 我们的基质 |
|---|---|---|---|---|
| 低维/光滑 | 黑化型 (单座位, s≈0.1-0.2, 方向性) | 单峰・平移 | **No** — 群体选择足够 | BG9 kernel union;ESN/ridge 文本 proxy (确定性・光滑) |
| 高维/偶然 | 伦斯基 Cit+ (potentiation→actualization→refinement) | 崎岖・靠变异越谷 | **Yes** (可能起作用的 regime) | 合成欺骗 corridor (behavior = 24 维的平均) |
| 经验判定 | 科因・巴顿・图雷利:群体选择通常足够,转移平衡极少起决定性作用 | 实际地形通常简单 | 我们 **negative 的镜像** | 试过的全部 CPU 基质 |

**结论**:赖特的转移平衡是「③起作用时**为何**起作用」的正确生物学先例,赖特-费希尔的 epistasis/ruggedness 之轴是「**维数**条件」的正确框架,黑化蛾与伦斯基 Cit+ 是低维/高维的干净两极,科因批判是我们 **negative** 的生物学先例。**但这些都不能证明计算结果。它们只是接地。** 比喻松动最大之处,在于生物加了一个 cost (Phase III 的 gene-flow trap)——我们 stateless 的设置没有它。

— 歇一会儿。当我意识到 100 年前的论争有同样的形状时,老实说我起了一身鸡皮疙瘩。但不把「起鸡皮疙瘩」误认作「证明」,正是本次的纪律。 —

---

#### 10. 对 GPU 的含意——剩下的路只有高维,但依旧是赌

arc 把 CPU 的路全部堵死了。真实 proxy 是 noise-free 且光滑 (IV),最后的候选 (kernel 多样化) 在结构上被堵死 (V)。③ 剩下的路只有 **高维地形**——而提供它的,是 **full-LLM 的参数/损失空间 (数百万维)**。

结构性洞见让 GPU 这场赌 **better-motivated**。它不是「也许只有 full-LLM 是例外」这种盲目的赌,而是遵循原理「**③ 需要高维,而 full-LLM 正处于高维域**」的赌。

**但依旧是赌。** 出于与生物学的 Cit+ 不能证明「③ 算法的胜利」相同的理由,以及与 BG9 里赢不了 RR 同型的理由——**若真实 LLM 地形能用 backprop (梯度下降) 这个强 baseline 直接导航,③ 仍然不需要**。难点是高维,这是 **必要条件而非充分条件**。还需额外证明「强力的直接法解不了它」(CPU 上是 RR,GPU 上是梯度下降)。

所以 GPU 适合的 **不是「单为③」**,而是 **组合 (portfolio) 判断** (与 llive 的真 LLM fitness 等搭车) + **借云做 1 次预先登记** (在投入资本之前)。go/no-go 标准也能写成 falsifiable:

> **full-LLM 的难点在 behavior 上是否高维,且是否难以被强力的直接 baseline (梯度下降) 抵达?** 若高维但梯度能直接够到,③ 不需要 (= BG9 的 RR 结果的 GPU 版)。

---

#### 11. 元教训——诚实,是用来赢的工具

这段 arc 真正的成果不是数值,而是 **「怀疑过于工整的结果」这种精神,实际上把研究往前推进了**。

- 在 **存在证明 (I)** 中赢的时候,我们用去掉谷的边界实验,主动确认了「③不是万能」(不高估胜利)。
- 在 **泛化 (III)** 中,同行评审甩出 3 个 rerun blocker,但修正后结论没变 (确认它不是脆弱的 negative)。
- 在 **确定性测量 (IV)** 中,因为物理性地抹掉了评估噪声,我们才能区分「光滑」是地形的性质还是仪器的极限。
- 在 **BG9 (V)** 中,在对抗式验证里我们 **试图反证、却无法反证** 自己的「③立不住」,它被确证为结构性的 (同样的纪律也在「把 negative 正确地确定为 negative」的方向上起了作用)。

而贯穿整段 arc 我们学到一件事——**低维的难点会被强 baseline 直接解掉。所以③ (分门别类、隔离培育的工夫) 要起作用,就需要「高维 behavior 空间」。**「做出欺骗地形③就立得住」只对了一半;准确说,除非是 **高维到无法直接采样** 的欺骗地形,③ 才立得住。而且令人惊讶的是,这个边界条件是 **赖特的转移平衡与科因批判在近 100 年前就已抵达** 的。

「当出现异常好的结果时,在自以为赢之前,务必先怀疑其内訳」——FullSense 的研究纪律 (`honest disclosure`) 不仅是自我告诫,而是一个 **实际捕捉假阳性、正确确定 negative、提升研究精度的机制**,在全部 6 段中都在转动。

最后,把结论再精确地说一遍。

> **③ 活起来,只在「高维」的欺骗地形时。** 它在存在证明 (合成 corridor) 中完胜,但真实 CPU 基质——记忆任务 (地板/天花板)、多任务泛化 (光滑)、真实 proxy 文本地形 (noise-free 且光滑)、kernel 多样化 (低维、结构上堵死)——没有一个满足那个条件。这 **不是「③了结 = ③被判明不需要」**,而是「现在能在 CPU 上测的仿真之物,没有满足③活起来的条件 (高维欺骗地形)」。主城 (GPU 高维) 还在前方,而且是一场背负着「强力直接 baseline 会解掉它」风险的赌。而且这个结论的骨架,20 世纪的进化生物学早已描绘过——只不过生物学 **不证明它,只接地它**。

---

**Tags**: 进化计算 / MAP-Elites / 统计检定 / honest disclosure / 进化生物学 / CPU 研究
**关联**: 连载 #33 (第三轴 ③ 了结 Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (反证・Goodhart・proxy 极限)
**Project**: llcore (PyPI 预约 llmesh-llcore,因仓库未公开故为本地研究)

---

---

# 한국어


## 1. AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin

:::note info
**📚 FullSense 지식 베이스 안내** <!-- fullsense-team-kb -->
FullSense 개발 전사 60+ 편 (4개 언어판・스토리 기반 읽기 순서 가이드・쉬운 설명판・4컷 만화 포함) 은 Qiita Team **FullSense KB** 에 모여 있습니다 (팀 멤버 전용).
:::

### AI를 500세대 진화시켰더니, 세계에 "나"와 "예측 부호화의 아버지 칼 프리스턴"만 남았다 #25 — monoculture의 honest disclosure와 선택압 컴포넌트 lldarwin

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

#### 0. 세 줄로 줄거리（라쿠고에서 말하는 "도입부"）

- **한 일**: llive의 파생 집단 진화에 8명의 지성을 persona 씨앗으로 투입, rich-proxy 평가로 500세대 돌렸다.
- **일어난 일**: 1세대째에 best_score가 **1.0에 달라붙어**, 이후 줄곧 만점. 8개 계통이 **후루세 52% / 프리스턴 48%**의 2개 계통으로 수렴, 나머지 6명이 절멸.
- **진짜 원인**: "만점이 계속 나왔다"＝**선택압이 0**. 누구를 골라도 fitness는 같으므로, 진화는 실질적으로 주사위 던지기（유전적 부동）가 되어 있었다.

요컨대 **"전원 100점인 시험으로 석차를 정하려 했다"**. 그러니 누가
합격할지는 제비뽑기가 됩니다. 시험이 나쁘다. 안경(lleval)이 흐려져 있었다.

---

#### 1. 왜 "인물"을 씨앗으로 뿌렸는가

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

#### 2. 결과 — 살아남은 것은 2명뿐

500세대 후의 계통 점유율（max_lineage_share의 내역）:

```
후루세         ████████████████████████████  52%
프리스턴       ██████████████████████████    48%
밀리지         (절멸)
이소무라       (절멸)
오카 기요시    (절멸)
그로텐디크     (절멸)
폰 노이만      (절멸)
파인만         (절멸)
```

언뜻 보면 "예측 부호화(Friston)와 내력 지향(후루세)이, 추상 수학(그로텐디크)이나
형식 계산(폰 노이만)을 이겼다"라는 **이야기**를 쓸 수 있을 것 같습니다.

실제로 SNS라면 "AI를 진화시켰더니 예측 부호화가 최강이었다"라며 화제가 될지도 모른다.
**하지만 그것을 하지 않는 것이 FullSense의 honest disclosure 룰**입니다
（[[feedback_benchmark_honest_disclosure]]）. 비정상적으로 깔끔한 결과가 나오면,
이긴 기분이 되기 전에 내역을 의심한다.

의심한 결과가, 다음 절입니다.

---

#### 3. 진짜 원인 — "만점 인플레"가 선택압을 지웠다

##### 3.1 증상: best_score가 1세대째부터 1.0

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

##### 3.2 근본 원인: 평가 함수 `fitness_rich`의 이중 붕괴

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

#### 4. 대책 — "측정한다" 다음은 "도태한다": lldarwin

llive 패밀리에는 이미 **lleval（안경 = 평가 프레임워크, 연재 #24-08）**가
있습니다. 이번에 알게 된 것은, **안경으로 차이를 "측정할 수 있었다"고 해도, 그 차이를
"누가 살아남는가"로 올바르게 변환하지 않으면 진화는 망가진다**는 것.

그래서 새 멤버 **lldarwin（선택압 = 도태 컴포넌트）**를 설계했습니다.
ll- 패밀리의 역할 분담은 이렇게 됩니다:

```
lleval   = 측정한다  （개체의 행동을 복수 축의 pressure profile로 변환）
lldarwin = 도태한다  （그 profile을 "다음 세대의 부모"로 변환）
```

##### 4.1 설계의 핵심 — "집약하지 않는" 선택압

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

##### 4.2 "LLM의 약점"을 선택압으로 한다

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

##### 4.3 전멸을 모니터한다 — SPC 알람

FullSense의 핵심 사상은 **SPC（통계적 공정 관리）**. lldarwin에서도
`max_lineage_share` / archive 성장 / behavioral diversity를 매 세대 기록하고,
**monoculture 비 > 0.8을 SPC_ALARM으로 검지**하여 cadence나 파라미터를
자동 조정합니다. 이번의 "8→2"를, 구조적으로 재발 불가능하게 하는 것이 목표입니다.

---

#### 5. 교훈（honest disclosure로 남긴다）

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

#### 5.5. "안경"과 "도태기"의 2단 구조 — 왜 나누는가（심화）

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

#### 5.6. 도해 아이디어（투고 전 SVG화할 후보）

본 글을 "움직임으로 매료시키기" 위해 준비하고 싶은 그림（투고 전 SVG화）:

1. **계통 점유율의 붕괴 애니메** — 세대 축으로 8개 계통의 띠가 2개 계통으로 빨려드는 animated SVG（금붕어 연못 메타포）.
2. **best_score = 1.0 즉시 포화 그래프** — 제 1세대에 천장에 달라붙는 평탄선（선택압 0을 한눈에）.
3. **argmax 붕괴 도** — 복수 축 벡터 `[전형성, 다양성, 전문성, ...]`이 `max()`로 1개의 막대로 붕괴되는 before/after.
4. **2단 구조도** — §5.5의 "안경 → 도태기"를 hero 도로 animated화.
5. **ll- 패밀리 역할도** — lleval（측정）/ lldarwin（도태）/ llive（개체）의 관계를 1장으로.

> 이것들은 [[project_fullsense_animemd_branch_token_viz]]의 animated SVG 표현층（선언 애니메 → SMIL）에 실을 예정.

---

#### 6. 관련

- 연재 #24-05「집단이 학습하는 AI」— 파생 집단 진화의 총괄（본 글의 전제）
- 연재 #24-08「안경을 만든다」— lleval（측정 측）
- 연재 #26「lldarwin의 설계」— 도태기의 다목적 도태 / ε-lexicase / QD（본 글의 속편）
- 연재 #27「안경이 흐려지면 도태도 무력」— 반증 조사・Goodhart's law（honest disclosure）
- 설계서: lldarwin（도태 측）— 본 글의 원천 소재
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(투고 전): hero SVG / theme SVG / 진행 badge / #24-05・#24-08・#26・#27의 Qiita URL cross-link -->

## 2. 「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26（多目的淘汰 / ε-lexicase / 中立貯蔵庫 / 実 LLM 評価）

:::note info
**📚 FullSense 지식 베이스 안내** <!-- fullsense-team-kb -->
FullSense 개발 전사 60+ 편 (4개 언어판・스토리 기반 읽기 순서 가이드・쉬운 설명판・4컷 만화 포함) 은 Qiita Team **FullSense KB** 에 모여 있습니다 (팀 멤버 전용).
:::

### 「안경으로 측정」하는 것만으로는 진화하지 않는다 — 선택압 컴포넌트 lldarwin의 설계와 실측 #26

> **콘셉트 hook**: 전작 #25에서 저는 「AI를 500세대 진화시켰더니, 세계에 **저와 프리스턴만** 남았다」는 큰 실패를 공개했습니다.
> 오카 기요시도, 그로텐디크도, 폰 노이만도, 전부 진화 도중에 조용히 사라졌습니다. 원인은, 평가 함수(안경 = lleval)가 만점을 계속 내놓아서 **선택압이 0이 된 것**입니다. 누가 우수한지 「측정할 수 있어」도, 그 차이를 「누가 살아남는가」로 변환하지 못하면, 진화는 그저 유전적 부동(浮動)으로 전락합니다.
>
> 그렇다면 — 안경으로 차이를 「측정했다」고 했을 때, 그 차이를 「도태」로 **올바르게 변환하는 장치**는 어떻게 만드는가.
> 그것이 이번 주역, **lldarwin**입니다. ll- 패밀리의 새 멤버로, **도태(선택압) 전문** 컴포넌트입니다.
>
> 이 글에서 기억해 주었으면 하는 키워드는, 단 한 단어. **「집약하지 않는다」**. 여러 잣대를 하나로 합산한 순간, 진화는 망가집니다. 왜 그렇게 되는지, 그리고 어떻게 실측으로 그것을 넘어섰는지 — 실패의 연장에서, 이번에는 **실제로 작동한** 이야기를 합니다.

---

#### 0. 세 줄 줄거리(라쿠고의 「마쿠라」)

라쿠고에는 본론 전에 「마쿠라(枕)」가 있습니다. 우선 세 줄로 전체상을.

- **lleval이 측정하고, lldarwin이 도태한다** — 진화는 「측정한다」와 「도태한다」의 2단 구조로, 비로소 의미를 가진다.
- 도태의 제1원칙은 **여러 선택압을 집약하지 않는 다목적 도태**. #25의 실패(단일 스칼라의 argmax로 짓눌렀다)의 진짜 원인을, 여기서 구조적으로 끊는다.
- 채택한 3대 기둥 = **ε-lexicase + minimal-criterion QD + down-sampling**(evolutionary_computation 코퍼스 616건을 횡단 조사하여 선정).

그리고 이번에는 골격뿐 아니라 **실측이 있다**는 것이 #25와의 차이입니다. novelty pressure로 행동 다양성을 7.12 → 14.88(+109%)로 2배로 늘리고, **중립 저장고**로 「멸종한 오카 기요시·그로텐디크 계통」을 실제로 **전원 부활**시키고, 마지막으로 **온프레미스의 진짜 LLM(llama3.2)**을 상대로, prompt 전략을 진화시켜 약한 태스크를 0.0 → 1.0으로 개선시켰습니다. 차례차례 살펴봅니다.

---

#### 1. 왜 「측정한다」와 「도태한다」를 나누는가

llive 패밀리에는 이미 **lleval(안경 = 평가 프레임워크, 연재 #24-08)**이 있습니다. 개체의 행동을 관측하고, 여러 축에서 점수화하는 장치입니다.

그런데 #25에서 알게 된 것은 치명적인 진실이었습니다. **안경으로 차이를 측정할 수 있어도, 그 차이를 argmax로 하나로 짓누르면 도태가 망가진다.** 구체적으로, `fitness_rich`가 여러 archetype 유사도를 `nearest = max(sims)`라는 단일 스칼라로 접고 있었습니다. 이것이 SEL-2 위반 — 「best=1.0이 포화하고, 전원이 만점이 되어, 선택 기울기가 사라진다」는 진짜 원인입니다.

역할을 명확히 나누면, 이렇게 됩니다.

```
lleval   = 측정한다 (개체의 행동을 「다축의 pressure profile」로 변환)
lldarwin = 도태한다 (그 profile을 「다음 세대의 부모」로 변환)
```

`lleval`의 출력은 **case 벡터**(각 축의 점수가 나열된 배열)입니다. `lldarwin`은 그것을 입력 계약으로 받아서, **집약하지 않고** 도태합니다. 양자의 책임 경계는 바로 여기에 있습니다. lleval이 「축을 하나로 합산한 뒤에」 넘겨오면, lldarwin은 아무것도 할 수 없습니다. 그래서 lleval 쪽에는 「breakdown(축별 내역)을 반드시 보존해서 넘긴다」는 것을 계약으로 부과합니다.

lldarwin의 `Pressure` 인터페이스는, 다음의 최소 계약으로 표현됩니다.

- `name` — 축의 이름(`typo_robustness` 등)
- `evaluate(individual_output) -> case_scores: list[float]` — 개체의 행동을 「축별 점수 배열」로 변환
- `is_proxy: bool` — proxy 측정인지, 실제 LLM/VLM 측정인지(측정 순도의 구분)
- `minimal_criterion: float | None` — 그 축의 최저 번식 기준(None이면 gate 없음)

포인트는, `evaluate`의 반환값이 **스칼라가 아니라 리스트**라는 것입니다. 한 축 안에도 여러 case(테스트 케이스)가 있고, 그것을 짓누르지 않고 lldarwin으로 흘려보냅니다. 이 「짓누르지 않는」 설계가, 나중에 specialist를 구하는 복선이 됩니다.

> 🍵 **휴식 포인트**: 안경(lleval)과 필터(lldarwin)를 나누는 의미는, 사진으로 말하면 「노출을 측정한다」와 「어느 컷을 채용할지 정한다」의 차이입니다. 측광이 완벽해도, 베스트 샷의 선택을 틀리면 앨범은 엉망입니다. 노출계(lleval)가 「이 한 장은 밝기 80점, 구도 30점, 표정 95점」이라고 알려줘도, 그것을 「평균 68점」으로 반올림해서 버리느냐, 「표정 95점인 한 장은 별도 칸에 남기느냐」에 따라, 앨범의 풍부함은 천지 차이로 달라집니다. lldarwin은 「채용 판단」의 전문가입니다. 측정하는 사람과 고르는 사람을 한 사람이 겸임하면, 대개 양쪽 모두 엉성해집니다.

---

#### 2. 설계의 핵심 — 「집약하지 않는」 7 스테이지

lldarwin은, lleval로부터 받은 pressure profile(다축의 case 벡터)을, 다음의 7 스테이지로 도태합니다. 각각에 「왜 필요한가 = 어떤 실패를 막는가」를 덧붙입니다.

1. **Standardizer** — per-dim z-score. 「전 축이 평균적으로 높다」는 것만의 무특징한 우등생을 우대하지 않고, 각 축에서의 **일탈**을 선택압으로 바꾼다. 중앙 일치(모두와 같음)는 제외.
   - *막는 실패*: 「평균점이 높을 뿐」인 평범함이 이기고, 뾰족한 개체가 사라지는 monoculture의 입구.
2. **MinimalCriterionGate** — 각 축의 최저 기준으로 번식 가부를 가른다. 연속 순위만으로 「독식」시키지 않는다.
   - *막는 실패*: 일강(一強)이 모든 번식 슬롯을 독점하는 전멸 시나리오. 기준을 충족하면 누구든 번식할 수 있는 「최저 보장」으로 다양성의 토대를 남긴다.
3. **EpsilonLexicaseSelection** — 축을 case로서 하나씩 독립적으로 평가한다. 어떤 축에서 돌출한 specialist(다른 축은 평범)가 살아남을 수 있다.
   - *막는 실패*: 집약 argmax에 의한 specialist의 절멸. 이것이 #25의 8→2를 낳은 메커니즘 그 자체.
4. **QD / MAP-Elites archive** — pressure profile을 behavior 기술자로 변환하고, cell마다 elite를 보존. archive는 단조 증가.
   - *막는 실패*: 구조적인 전멸. 하나의 cell에 한 개체라도 남으면, 그 행동은 사라지지 않는다.
5. **Niching / FitnessSharing** — 같은 niche의 개체를 down-weight하여, 다봉(多峰)을 병존시킨다.
   - *막는 실패*: 단봉으로의 응집(monoculture).
6. **Down-sampling** — 매 세대, case의 부분집합만으로 평가하여 환경을 교란한다.
   - *막는 실패*: 특정 peak로의 과적합과 plateau(정체 고원). moving target으로 만들어 「같은 방식으로 이기는 것」을 허용하지 않는다.
7. **NoveltyScorer** — 정체 시에 「과거와 다른 행동」으로 탐색압을 가한다.
   - *막는 실패*: 탐색 고갈. 개선이 멈췄을 때, 새로움 자체를 보상으로 삼아 바깥으로 밀어낸다.

#25의 8→2 monoculture와 대비하면, 핵심은 세 가지: **(3) ε-lexicase·(4) QD archive·(2) minimal-criterion**입니다. #25에서는 이것들이 전부 빠진 채 단일 스칼라 argmax만 돌고 있었습니다. 그래서 「평균적으로 최강인 1 계통」이 연속 순위를 독식하고, 나머지가 부동으로 사라졌습니다. lldarwin은 이 세 가지를 「집약하지 않고 묶음」으로써, 세대를 거듭해도 파탄나지 않는 구조를 만듭니다.

> 🤔 **비유(만자이 풍)**:
> 보케 「시험 점수를 전부 더해서 순위를 매겼더니, 평균점이 높을 뿐인 우등생만 남았어.」
> 츳코미 「그거 다양성 제로잖아! 수학만 100점·나머지 0점인 천재가 사라졌잖아!」
> 보케 「아니, 토탈로 보면 우등생이 위인데……」
> 츳코미 「**토탈로 보지 마!** 과목을 하나씩 보면, 그 천재는 『수학』 case에서는 누구한테도 안 져. ε-lexicase는 그걸 구하는 구조야. 합산한 순간 천재는 죽어.」
> ——합산(집약)이 specialist를 죽인다. ε-lexicase는 「과목을 하나씩 본다」니까, 뾰족한 녀석이 남는다. 이것이 lldarwin의 제1의 핵심입니다.

---

#### 3. 왜 이 3대 기둥인가(rad-research의 뒷받침)

「세대를 거듭해도 파탄나지 않는」 가장 유력한 융합안으로, evolutionary_computation 코퍼스 616건을 횡단 조사하여 선정했습니다. 자체 발명한 것이 아니라, 기존 연구의 「집약하지 않는」 계보를 선별하여 묶었다 — 는 내력이 중요합니다.

| 기법 | 효능 | 출처 |
|---|---|---|
| **ε-lexicase** | specialist 보존·high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | cell별 elite로 전멸 불가 | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | 환경 교란·비용 절감 | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | 조기 수렴 방지(장래 옵션) | Lyu 2020 (2005.07376) |

3대 기둥은 제각각인 기법으로 보이지만, 실은 **「집약하지 않는다」는 하나의 사상**으로 꿰뚫을 수 있습니다. ε-lexicase는 「축을 집약하지 않는다」. QD는 「행동 공간을 집약하지 않는다(cell마다 보존)」. down-sampling은 「평가 환경을 고정하지 않는다(매 세대 교란)」. 어느 것도 「하나로 둥글리지 않는다」는 점에서 같은 철학입니다. 그래서 조합해도 사상이 충돌하지 않고, 상승 작용합니다.

> 🍵 **휴식 포인트**: 「왜 자체 발명하지 않느냐?」는 질문을 받습니다. 답은 단순한데, **기존 연구의 조합으로 충분히 강하기 때문**입니다. 제 개발 규칙([[feedback_originality_over_imitation]])에는 「외부 알고리즘의 채용은 망라가 아니라 **선별**. 파탄 리스크나 단순한 모방은 배제하고, 독자 설계에 가치를 더하는 것만 채택한다」고 되어 있습니다. lldarwin의 독자성은 「새로운 선택 알고리즘을 발명한 것」이 아니라, 「이것들을 **집약하지 않고 묶는 묶음 방식**과, 그것을 llive의 진화 루프에 **실제로 배선한 것**」에 있습니다. 요리로 말하면, 세계 최초의 식재료를 만드는 것이 아니라, 기존의 명품 식재료를 「섞지 않고 한 접시에 담는」 기술입니다. 섞으면 망가지는 재료를, 섞지 않고 공존시킨다.

---

#### 4. Stage1 — criteria 제외 + novelty pressure로 행동 다양성을 2배로

여기서부터 실측입니다. Stage1에서는, 설계를 단숨에 전부 구현하지 않고, 가장 효과가 있을 것 같은 두 가지 변경만 넣어서 측정했습니다(llive, branch `optimize/core-2026-05-20`, commit `8060204`).

**변경 1: criteria 제외.** ε-lexicase의 case에서, `factor_score`(= max-archetype의 단일 스칼라 = argmax, 바로 #25의 best=1.0 포화의 진짜 원인)와 `nearest_persona_idx`(= 순서에 의미가 없는 카테고리 index)를 뺐습니다. 이것은 「나쁜 잣대를 도태의 판단 재료에서 제거하는」 청소입니다.

**변경 2: novelty pressure.** `MultiPressureSelector(use_novelty=True)`를 활성화. 매 세대, 과거 세대의 archive와의 k-NN 평균 거리(Lehman-Stanley 류의 novelty)를 계산하고, 그것을 집단 내에서 z-score화(STD-1)하여, 추가의 lexicase case로 도태에 섞습니다. 「모두와 다른 행동을 하고 있다」는 것 자체를, 축의 하나로 평가합니다.

테스트는 `tests/unit/test_evolutionary_lldarwin.py`를 8 → 10건으로 확장(제외·novelty 보존을 추가). 진화계 847건 green, 회귀 없음.

실측 조건은 rich-proxy, 8 founders + pop24, 150세대, seed 0. 결과가 아래입니다.

##### 4.1 행동 다양성 (diversity_l2) — novelty가 듣는 지표

| 조건 | mean | tail30 min | final |
|---|---|---|---|
| BASELINE(제외 전·Tournament 상당의 구 lldarwin) | 7.12 | 0.68 | 0.83(붕괴) |
| A: criteria 제외만 | 9.16 | 1.57 | 1.57 |
| **B: 제외 + novelty** | **14.88(+109%)** | **6.56(9.6×)** | **11.73(붕괴 회피)** |

novelty pressure는, 행동(genome 공간)의 다양성을 약 2배로 유지하고, 종반의 다양성 붕괴를 막았습니다. criteria 제외만으로도 단독으로 효과가 있습니다(spurious한 argmax 압을 제거한 만큼). BASELINE은 final 0.83에서 **붕괴**하고 있는 데 반해, B 조건은 final 11.73에서 **버티고 있습니다**. 이것이 「집약하지 않는」 설계의 첫 번째 손맛입니다.

![Stage1 baseline(novelty 없음)의 적응도와 다양성. 종반에 다양성이 붕괴한다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_ko.svg)

![Stage1 novelty 있음. 다양성이 종반까지 유지된다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_ko.svg)

두 장을 나란히 놓으면, 종반의 거동 차이가 한눈에 보입니다. baseline은 다양성 곡선이 바닥에 달라붙는 데 반해, novelty 있음은 높은 수준을 유지한 채 끝까지 달립니다.

> 🍵 **휴식 포인트**: novelty pressure를 금붕어 연못에 비유하면 — 먹이(높은 fitness)에 몰리는 금붕어만 남기면, 머지않아 전원이 같은 장소에서 같은 움직임을 하는 연못이 됩니다. novelty pressure는 「**모두와 다른 장소를 헤엄치는 금붕어에게도 보너스**」를 주는 담당입니다. 결과, 연못 여기저기 흩어진, 봐도 질리지 않는 연못이 됩니다. 다만 여기서 방심하면 안 됩니다. 다음 절에서, 이 「북적이는 연못」에 숨어 있던 **함정**이 발견됩니다.

---

#### 5. honest disclosure(가장 중요) — 행동 다양성과 계통 생존을 저는 혼동하고 있었다

여기가 본 글에서 가장 중요한 절입니다. 좋은 숫자(+109%)가 나왔다고 해서, 이긴 기분이 되지 않는다 — 이것은 제 철칙([[feedback_benchmark_honest_disclosure]])입니다. 내역을 의심했습니다. 그리고, 잘못을 발견했습니다.

##### 5.1 계통 고정 (founder_counts) — novelty로는 개선되지 않는 지표

같은 실측에서, 다른 지표를 봅니다. 「8명의 founder(조상 계통) 중, 몇 계통이 끝까지 살아남았는가」.

결과는 — **전 조건에서 최종적으로 8 → 2 계통**(furuse-kazufumi + friston)으로 수렴. oka-kiyoshi(오카 기요시) / grothendieck(그로텐디크) / von-neumann / feynman / millidge / isomura는, **전부 멸종**.

novelty를 넣어서 행동 다양성을 2배로 했는데도, **계통의 생존은 #25와 완전히 같은 2 계통**이었던 것입니다.

##### 5.2 왜인가 — 저는 두 개의 「다양성」을 혼동하고 있었다

설계서(#25 시점)의 TODO에는 「재실행에서 오카 기요시·그로텐디크 계통이 살아남는지 검증」이라고 적혀 있었습니다. 이것은 **행동 다양성과 계통 생존을 혼동하고 있었던** 것입니다.

`poc_evolution_env.py`의 저자 코멘트(L129-132)가, 이 혼동을 정확하게 짚고 있습니다.

> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs QD niching on lineage / PERSONA-FX, not pure novelty**"

풀어서 말하면, 이렇습니다.

- 실증된 monoculture 0.05는, **행동적**(archive-cell의 점유율)이지, **계통적이지 않습니다**. novelty/lexicase가 개선하는 것은 「행동의 퍼짐」이지 「조상의 생존」이 아닙니다.
- 계통 고정이 중립 부동(기무라 모토오의 중립 진화설)에 의해 monoculture로 향하는 것은, **이론적으로 정상**입니다. 붕괴가 아닙니다. novelty도 lexicase도, **기존 개체를 보존하는** 메커니즘밖에 갖지 않으며, **한 번 멸종한 계통을 부활시키는 메커니즘을 갖지 않습니다**. 그래서 계통 고정은 구조적으로 막을 수 없습니다.
- 게다가, archetype 간 거리도 0.068~0.29로 압축되어 있어서(유사도가 0.71~1.0에 밀집), 선택 기울기가 약하고 drift(부동)가 지배적입니다. friston은 가장 비중심적(centroid 거리 0.162)인데도 살아남았다 = 중심성(강함)이 아니라, **운(drift)**으로 2 계통이 고정된 것입니다.

즉 — 「오카 기요시·그로텐디크가 살아남았으면」 하는 저의 바람은, **행동 다양성을 올리는 약으로는 절대 낫지 않는 병**이었습니다. 약을 잘못 쓰고 있었습니다. 이것은 정직하게 기록할 가치가 있는 교훈입니다.

> 🍵 **휴식 포인트**: 만자이로 말하자면.
> 보케 「연못에 형형색색의 움직임을 하는 금붕어를 늘렸어! 다양성 완벽이야!」
> 츳코미 「그래서, **혈통**은? 8개 있던 금붕어 가문, 몇 개 남았어?」
> 보케 「……2개야.」
> 츳코미 「움직임은 화려한데 가계도는 텅 비었잖아! 움직임의 다양성과 혈통의 다양성은 **별개의 이야기**라고!」
> ——「행동이 다양」과 「계통이 다양」은, 겉모습이 닮았을 뿐인 완전히 다른 지표. 저는 이것을 혼동하고 있었습니다. 정직하게 공개합니다.

---

#### 6. Stage1.5 — 중립 저장고로 멸종한 계통을 되살리다

병의 정체를 알면, 약을 바꿀 수 있습니다. 계통 생존에 필요한 것은 「멸종한 계통을 매 세대 re-inject하는 메커니즘」 — **lineage-niched 중립 저장고(reservoir)**입니다.

##### 6.1 우선 PoC로 메커니즘을 확인한다

곧바로 본 루프를 개조하지 않고, 우선 standalone PoC로 메커니즘이 도는지 확인했습니다([[feedback_poc_feasibility_first]] = 요건 → PoC → 타당성 → 상세 설계, llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`).

selection은 Stage1의 `MultiPressureSelector`(criteria 제외 + novelty)를 그대로 씁니다. fitness는 rich-proxy. 계통은 parent_a로부터 상속. **reservoir = 계통별 best-ever genome을 보존하고, 멸종한 계통을 매 세대 re-inject한다**(낮은 score의 자식을 치환. best는 망가뜨리지 않는다). 8 founders + pop24 + 150 gens + seed 0으로 측정했습니다.

| reservoir | 최종 named 계통 | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1**(oka-kiyoshi 24/24 = 완전 monoculture) | 1.00 | 1.58 |
| **ON** | **8(전 founder 생존)** | **0.31(≪ 0.8 OE-3)** | 1.69 |

reservoir ON에서, 오카 기요시(oka)·그로텐디크(grothendieck)를 포함한 **전 8 계통이 생존**. 최종 shares는 friston 7 / furuse 6 / grothendieck 4 / oka 3 / 다른 4 계통 각 1. **강한 계통은 자손을 갖고 번식하고, 약한 계통은 저장고가 생명 유지한다**는, 이상적인 거동입니다. 행동 다양성도 저하 없음(1.69 vs OFF 1.58).

**Honest 유보(PoC 단계)**: 저장고는 frozen elite(동결된 대표)를 재투입하므로, 약한 계통(각 1체)의 「생존」은 재투입에 의한 것이지, 능동적 진화는 아닙니다. 이것은 중립 저장고의 정의대로(대표를 보존하고, 재결합 가능하게 한다)로 정당하지만, 「약한 계통이 활발하게 계속 진화한다」고는 주장하지 않습니다.

##### 6.2 본 EvolutionLoop에 편입(additive + default-off)

PoC로 메커니즘이 확인되었으므로, 본 `EvolutionLoop`에 편입했습니다(commit `b03cbda`). 설계의 핵심은 **additive이며 default-off** — 기존 거동을 일절 바꾸지 않고, 플래그를 세웠을 때만 유효해집니다. 하위 호환을 사수했습니다.

- `EvolutionLoop.on_population_bred` hook을 추가(breed 직후·평가 전에 bred 리스트를 변환 가능. 기본 None = 하위 호환).
- `LineageReservoir`(`lineage_reservoir.py`): 조상 추적(parent_ids[0]을 상속) + 계통별 best-ever 보존 + 멸종 보호 계통의 re-inject. `founder_map`을 공유하고 계통 로그와도 정합.
- `run_persona_evolution(lineage_reservoir=True)` / run 스크립트 `--lineage-reservoir`를 추가.
- tests: `test_evolutionary_lineage_reservoir.py` 6건 + 진화계 **937 green**(회귀 없음).

실 EvolutionLoop에서의 실측(rich-proxy + lldarwin + novelty, 8 founders / pop24 / 150gens / seed0).

| 조건 | named 계통 생존 | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8(furuse 17 + friston 7) | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8(전 계통)** | **0.33** | **0.29(≪ 0.8 OE-3)** | 9.20 |

오카 기요시(oka 3)·그로텐디크(grothendieck 1)를 포함한 **전 8 계통이, 실 루프에서 생존**했습니다. PoC의 예측(fixation 0.31)을, 본 구현이 0.29로 재현했다 — 메커니즘이 설계대로 작동한 증거입니다.

이것이, 본 글 최대의 볼거리입니다. 아래 두 장을 비교해 보세요.

![중립 저장고 OFF. 계통 지배 스트림이 최종적으로 furuse 71% / friston 29%의 2 계통으로 붕괴한다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_ko.svg)

![중립 저장고 ON. 전 8 계통(millidge / von-neumann / oka / grothendieck 등)이 병존한다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_ko.svg)

OFF(위)는, 세대가 진행됨에 따라 스트림이 2색으로 삼켜져 간다 — 「저와 friston만 남았다」는 #25의 재현입니다. ON(아래)은, 8색이 끝까지 띠로서 남습니다. 오카 기요시도 그로텐디크도, 사라지지 않았습니다.

![중립 저장고 ON의 적응도와 다양성](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_status_ko.svg)

> 🍵 **휴식 포인트**: #25에서 「저와 프리스턴만 남았다」고 한탄했던, 그 쓸쓸한 세계. 그것이 이번에는 오카 기요시도 그로텐디크도 폰 노이만도 전원 있는, 북적이는 세계로 바뀌었습니다. **이것은 날조가 아니라, 실제로 작동한 결과입니다**([[feedback_benchmark_honest_disclosure]]에 따라, 거짓 실패도 거짓 성공도 쓰지 않습니다). 다만 — 들뜨기 전에, §5에서 배운 자세를 떠올립시다. 「좋은 숫자가 나오면 내역을 의심한다」. 다음 §6.3에서, 이 성공에도 **대가**가 있었음을 정직하게 씁니다.

##### 6.3 Honest 유보 — 계통 보존과 행동 다양성은 약한 트레이드오프

reservoir ON에서 계통은 전원 살아남았습니다. 하지만 잘 보면 **diversity_l2는 14.88 → 9.20으로 저하**하고 있습니다. frozen elite(동결 대표)를 매 세대 재투입하는 만큼, genome 공간의 퍼짐이 다소 줄어드는 것입니다.

다만, OFF 시의 붕괴(final 0.83)는 회피하고 있습니다. 즉 「계통 보존을 취하면, 행동 다양성의 피크는 조금 내려가지만, 붕괴는 막을 수 있다」는 **약한 트레이드오프** 관계입니다. 대가 제로의 마법은 아닙니다. 이것을 정직하게 적어 둡니다. 그리고, 이 대가를 어디까지 작게 할 수 있는가가, 다음 sweep의 주제가 됩니다.

---

#### 7. 재투입 빈도 sweep — 비단조적 최적점이라는 비자명한 발견

§6.3의 honest 유보(frozen elite 재투입으로 diversity가 내려간다)를, `reinject_interval`(재투입을 하는 세대 간격. 기본 1 = 매 세대)의 sweep으로 특성화했습니다(commit `da93dd3`). `LineageReservoir.reinject_interval` + `--reinject-interval` 플래그를 추가(test 7건). 8 founders / pop24 / 150gens / seed0.

| interval | named 생존 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**(매 세대) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84(최대)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**여기서 비자명한 발견이 있었습니다.** 직관적으로는 「재투입을 줄이면(interval을 올리면), frozen elite의 밀어넣음이 줄어서 diversity가 단조적으로 회복된다」고 예상하시죠? 그런데 — **diversity는 단조 증가하지 않고, interval=5에서 피크**를 찍고, 10/20에서는 오히려 저하했습니다.

이유를 생각하면 납득이 갑니다. 계통을 너무 방치하면(interval이 너무 크면), (a) 저장고 유래의 다양성 주입이 줄고, (b) 소수 계통이 고정되어 버려서, 결국 diversity도 늘지 않습니다. 「재투입 과다」도 「방치 과다」도 둘 다 안 되고, 중간에 최적점이 있습니다. 이것은 **실제로 sweep을 돌리지 않으면 예측할 수 없었던** 지견입니다.

운용 지침은 이렇게 되었습니다.

- **계통 보존을 최우선**으로 한다면 → interval=1(8/8 전 계통 생존).
- **행동 다양성도 양립**시키고 싶다면 → interval=5(5/8을 보존하면서 diversity 최대).

양립의 최적점은 fitness의 설계나 집단 규모에 의존하므로, 본 환경에서는 sweep으로 재보정합니다.

![재투입 빈도의 트레이드오프. 계통 보존과 행동 다양성은 반비례하고, diversity는 interval=5에서 피크를 찍는다(비단조)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_ko.svg)

> 🍵 **휴식 포인트**: 라쿠고의 사게(결말)처럼, 여기에는 「예상을 뒤집는 전(轉)」이 있습니다. 「하면 할수록 좋다」고 생각했더니, 「너무 하면 역효과」였습니다. 식물의 물 주기와 같아서, 너무 적게 줘도 마르고, 너무 많이 줘도 뿌리가 썩습니다. 중용에 최적점이 있습니다. 진화 계산을 하다 보면, 이런 「단조롭지 않은 곡선」을 몇 번이고 만납니다. 그래서 베이스라인을 측정하고, sweep을 돌립니다. 직관은, 자주 배신당합니다.

---

#### 8. Stage2 전반 — 「LLM의 약점」을 proxy로 선택압으로 삼다

여기까지는 rich-proxy(persona 유사도 기반의 heuristic)로 메커니즘을 확인해 왔습니다. 다음은 설계의 또 하나의 기둥, **「LLM/VLM이 현실에서 약하고, 또한 측정 가능한 축」을 pressure로 삼다**를 구현합니다(commit의 계열, `pressures.py`).

설계 §3에서 든 proxy 가능한 5 축을 plugin화했습니다.

| pressure(LLM 약점) | 관련 사고 인자(case) |
|---|---|
| typo_robustness(노이즈 내성) | consistency / reality_link / uncertainty |
| polysemy_wsd(다의어) | multiview / consistency / reality_link |
| multistep_robustness(다단 추론) | structurize / closed_loop / self_extend |
| calibration(신뢰도 추정) | uncertainty / provenance |
| context_management(무관 문맥 내성) | consistency / provenance / recompose |

`make_pressure_fitness()`가 각 pressure의 case(총 14개)를 breakdown으로 출력하고, lldarwin의 ε-lexicase가 **집약하지 않고 축별로 specialist를 도태**합니다. `--fitness pressure-proxy`를 추가. tests `test_evolutionary_pressures.py` 4건 + 진화계 **942 green**.

end-to-end 실측(pressure-proxy + lldarwin + novelty + reservoir, 8 founders / 120gens): named 계통 **8/8 생존** / lineage_fixation (tail) 0.67 / diversity_l2 (tail) **17.91**. 14개의 약점 축 case가 독립적으로 도태되어, 행동 다양성은 높습니다. 계통은 reservoir가 유지하고 있습니다(pressure-proxy는 persona의 동일성을 직접 보상화하지 않기 때문에, 우점 계통의 share는 rich-proxy의 0.29보다 높은 0.67이 됩니다).

![5 약점 축(typo / polysemy / multistep / calibration / context)의 모집단 평균 추이(proxy 측정)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_ko.svg)

**Honest 유보(설계 §7 / §7.1에 명시된 수용된 한계)**: 개체는 실 LLM이 아니라 genome(llive 구성)입니다. 본 pressure가 측정하는 것은 「genome이 그 약점에 **관련된 사고 인자**를 얼마나 갖추는가」라는 **행동의 대리**이지, **production의 LLM 능력이 아닙니다**. 이것은 **mechanism feasibility(메커니즘이 도는 것)의 검증**에 한정됩니다. Goodhart 리스크(proxy를 해킹하는 표면 전략이 진화한다)도 수용된 한계입니다. 실 LLM/VLM의 약점 축의 실측은, Stage2 후반(OLLAMA_HOST 설정 + 개체→실 LLM 매핑이 전제)으로 미룹니다.

> 🍵 **휴식 포인트**: 여기는 오해되기 쉬우므로, 다짐해 둡니다. 「LLM의 약점을 진화로 극복했다!」고는 **아직 말하지 않았습니다**. proxy가 측정하는 것은 「메커니즘이 도는가」뿐. 진짜 LLM이 타이포에 강해졌는지 어떤지는, 이 단계에서는 일절 알 수 없습니다. proxy로 화려한 숫자(17.91)가 나와도, 그것은 「장치가 작동한다」는 증명이지 「내용이 똑똑해졌다」는 증명이 아닙니다. 이 선 긋기를 모호하게 한 순간, 연구는 거짓이 됩니다. 그래서 다음으로, **진짜 LLM**을 상대합니다.

---

#### 9. Stage2 후반 — 진짜 온프레미스 LLM을 상대로 prompt 전략을 진화시키다

localhost의 ollama(llama3.2:latest 등)가 도달 가능하다는 것을 알았으므로, 드디어 **실 LLM 평가**가 가능해졌습니다(commit `2fb2912`). localhost = on-prem이므로, measurement purity(측정 순도. cloud LLM과 혼재시키지 않는다)의 규율도 충족합니다([[feedback_llive_measurement_purity]]).

##### 9.1 개체 → 실 LLM으로의 매핑(Promptbreeder 계)

핵심은 「genome을, 어떻게 실 LLM에 효과를 미치게 하는가」입니다. `real_pressures.py`에서 **개체 → 실 LLM 매핑**을 구현했습니다.

- **개체의 `c_prompt`(PromptChromosome)을 system prompt로 변환**: skill_set → 지시문 / prompt_template_id → 추론 스타일 / language_style → 어조. 고정의 LLM(llama3.2)에 이 system prompt를 씌우고, 5 약점 축의 **실 태스크**를 풀게 해서 채점합니다.
- **LLM 본체는 고정하고, prompt 전략(genome)을 진화시킨다** = 「어떤 prompt 전략이 LLM의 약점을 완화하는가」를 실측으로 도태한다. 이것은 Promptbreeder(prompt를 진화적으로 최적화하는 연구 계열)의 방식입니다.
- temp=0(greedy)로 결정론적으로. `(system_prompt, task)`를 캐시(동일 전략은 재평가하지 않는다).
- robust: per-call try/except(ollama의 hiccup은 task의 실점으로 취급하고, 주행은 계속).
- `--fitness real-pressure` / `--ollama-model` / `--max-wallclock-seconds`를 추가. tests 5건 + 진화계 947 green.

##### 9.2 실 선택 신호의 실증 — CoT+structure 전략이 multistep을 0.0 → 1.0으로

그리고, 진짜 선택 신호를 관측할 수 있었습니다.

**CoT+structure 전략**(`chain_of_thought` + structurize + loop)이, llama3.2의 **multistep(다단 추론)을 0.0 → 1.0으로 개선**했습니다(terse한 전략은 0.0으로 실패. score는 0.80 → 1.00으로 상승).

이것은, lldarwin의 주장 「prompt 전략의 진화로 LLM의 약점을 완화할 수 있다」를, **proxy가 아니라 실 LLM에서 실증**한 것을 의미합니다. 같은 llama3.2 본체라도, 씌우는 system prompt(= 진화한 genome)에 따라, 다단 추론 태스크를 풀 수 있기도 하고 못 풀기도 합니다. 진화는 「풀 수 있는 prompt 전략」을 실제로 골라낸 것입니다.

![5 약점 축의 모집단 평균 추이(실 온프레미스 LLM llama3.2 평가). prompt 전략의 진화로 축이 개선된다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_ko.svg)

##### 9.3 12h 연속 실행

실 LLM 평가는 무거우므로, 장시간의 연속 실행을 기동했습니다(`out/lldarwin_12h_realpressure_2026_05_26/`).

```
--fitness real-pressure --selection lldarwin --novelty --lineage-reservoir
--genome3d --population 24 --max-wallclock-seconds 43200 --checkpoint-every 5
```

wallclock 12h에서 safely 정지(snapshot 완료 → `--resume`으로 계속 가능). 연속 실행 중에 best_score=1.0에 도달했습니다.

![실 LLM 진화 실행의 적응도와 다양성(12h 연속 실행)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_ko.svg)

##### 9.4 Honest 유보(실 LLM 평가의 한계)

여기가 #25에서 배운 자세의 총결산입니다. 화려한 결과(0.0 → 1.0, best 1.0)가 나왔기 때문에, 내역을 철저하게 정직하게 씁니다.

- **(a) fitness에 관여하는 것은 `c_prompt`뿐.** persona / c_factors는 중립(계통은 reservoir로 유지, 초기 선택은 novelty가 담당). 즉 이것은 「**prompt 전략의 진화**」이지 「persona의 진화」가 아닙니다. 오카 기요시의 인격이 똑똑해진 것이 아니라, 오카 기요시라는 계통에 연결된 prompt 전략이 선택되었다는 이야기.
- **(b) 전 founder의 초기 c_prompt는 동일(default).** 그래서 탐색은 mutation 구동입니다(founder마다 prompt를 다양화하는 것은 향후의 개선). 출발점이 같으므로, 초기의 계통 차이는 prompt 전략에는 효과가 없습니다.
- **(c) 작은 배터리(축당 2문) = 노이즈가 많은 추정.** 0.0 → 1.0이라는 극적인 숫자도, 문제 수가 적은 만큼 노이즈를 포함합니다. 통계적으로 견고한 주장을 하려면, 더 큰 배터리가 필요합니다.
- **(d) on-prem only(measurement purity). 일반 능력의 주장이 아니다.** llama3.2라는 특정 모델·특정 태스크에서의 관측이지, 「LLM 일반이 이렇게 된다」고는 말하지 않습니다.

이것들을 숨기면 「진화로 LLM이 극적으로 똑똑해졌다!」는 화려한 이야기를 쓸 수 있지만, 그것은 거짓입니다. lldarwin이 실증한 것은 「**메커니즘이, 실 LLM 위에서, 선택 신호를 낳는다**」는 데까지. 그 선을 넘는 주장은 하지 않습니다.

> 🍵 **휴식 포인트**: 연구에서 가장 기분 좋은 것은 「0.0이 1.0이 되었다!」고 외치는 순간입니다. 하지만, 그 순간이야말로 [[feedback_benchmark_honest_disclosure]]가 효과를 발휘합니다. 「이상하게 좋은 숫자가 나오면, 이긴 기분이 되기 전에 내역을 의심하라.」 이번으로 말하자면 — 이긴 것은 「prompt 전략」이지 「LLM 본체」도 「persona」도 아닙니다. 문제 수도 적습니다. on-prem의 1 모델뿐. 이것을 전부 쓰고 나서야, 비로소 「실증했다」고 말할 수 있습니다. honest disclosure는, 자랑을 참는 근력 운동입니다.

---

#### 10. 기존 자산의 재이용(codex 코드 조사 기반)

설계를 그림의 떡으로 만들지 않기 위해, 배하의 Codex에게 기존 코드를 조사시켰더니, **많은 것이 구현 완료·미배선**이었습니다.

- `mating.py:139 LexicaseSelection`(ε 포함, 구현 완료이지만 미배선 → 배선만 하면 됨)
- `nsga2.py:197 NSGA2Selection`(≤3 목적 레인용)
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**신규 구현**: `Standardizer` / `MinimalCriterionGate` / `Pressure` 군 / `MultiPressureSelector`(핵심) / `LineageReservoir`(Stage1.5) / `SelectionAudit`.
**배선점**: `loop.py:122`의 `selection`에 `MultiPressureSelector`를 주입, `persona_evolution.py:606`에 주입구를 추가, `LineageReservoir`를 `EvolutionLoop.on_population_bred` hook에 연결.

> 🍵 **휴식 포인트**: 「구현 완료이지만 미배선」이 가장 많았던 것이, 최대의 교훈이었습니다. 좋은 부품을 만들어도, **배선(오케스트레이션)하지 않으면 진화는 망가진 채**. #25에서 8→2가 된 것은, ε-lexicase도 NoveltyScorer도 QD도 「상자 안에 있었는데, 배선되지 않았기」 때문입니다. lldarwin의 본질은, 신규 알고리즘의 발명보다도, 「기존의 좋은 부품을 **집약하지 않고** 묶어서, 진화 루프에 **실제로 배선하는 것**」에 있습니다. 전자 부품을 전부 갖춰도, 납땜하지 않으면 라디오는 울리지 않습니다.

---

#### 11. 파탄 회피의 보증 — 전멸하지 않는 다층 구조(실측으로 뒷받침 완료)

#25의 monoculture(8→2)를 반증하는 다층 구조는, 설계대로 갖춰졌고, 게다가 이번에는 **실측으로 뒷받침되었습니다**.

1. **MinimalCriterionGate** — 최저 기준으로 번식 가부 → 일강 독식을 억제.
2. **QD cell별 elite** — 1 cell이라도 남으면 계통 전멸 불가(archive 단조 증가).
3. **Niching / FitnessSharing** — 같은 niche를 down-weight → 다봉 병존.
4. **Down-sampling** — moving target으로 plateau 파괴.
5. **per-dim z-score + 중앙 일치 제외** — 무특징을 우대하지 않는다.
6. **LineageReservoir(Stage1.5에서 추가)** — 멸종 계통의 중립 저장고 → 계통 전멸을 구조적으로 저지(실측으로 8/8 생존).
7. **monoculture 모니터 + SPC** — max_lineage_share를 매 세대 기록, >0.8을 SPC_ALARM으로 검지 → 자동 조정.

특히 (6)은, §5의 honest disclosure(novelty로는 계통 고정을 막을 수 없다)를 받아 **나중에 추가한 층**입니다. 설계의 구멍을 실측으로 발견하고, 막았습니다. 실측의 lineage_fixation은 OFF 0.70 → ON 0.29로, OE-3 기준(<0.8)을 크게 밑돕니다. 「집약하지 않는다」 + 「멸종 계통을 되살린다」의 2단 구조로, #25를 구조적으로 짓누를 수 있었던 것이 본 글의 도달점입니다.

---

#### 12. honest disclosure / 리스크(예고편)

설계를 맹신하지 않습니다. 수용된 한계(다음 작 #27에서 깊이 파고든다)를, 다시 한번 정리해 둡니다.

- **Goodhart's law / proxy 괴리** — LLM 약점을 proxy fitness로 하면, 「지표를 해킹하는 표면 전략」이 진화한다(typo → 특정 치환의 암기, WSD → 테스트의 heuristic 이용 등). proxy는 mechanism feasibility에 한정하고, production 능력을 주장하지 않는다.
- **설계자 의존성** — lexicase=case / QD=기술자 / novelty=거리 척도, 어느 것이나 「다양성의 방향」을 설계자가 정한다. 생물 진화급의 미상정 창발은 한정적.
- **minimal-criterion의 정체⇄붕괴 트레이드오프** / **QD의 차원의 저주 + 아카이브 포화**.
- **실 LLM 평가의 한계(§9.4 재게재)** — c_prompt만 fitness 관여·founder 초기 prompt 동일·작은 배터리·on-prem only.

> **다음 회 예고(#27)**: 「안경이 포화하면 선택압은 무력」이라는 가장 아픈 반증을, Goodhart's law와 proxy fitness의 한계와 함께 정직하게 공개합니다. lldarwin은 만능이 아닙니다. **어디까지 주장해도 되는가**의 선 긋기가 #27의 주제입니다. 이번에 「8/8 생존」 「0.0→1.0」이라는 좋은 숫자가 나왔기 때문에, 다음은 철저하게 반증으로 단련합니다.

---

#### 13. 결론

- 진화는 「**측정한다(lleval)**」와 「**도태한다(lldarwin)**」의 2단 구조. 도태의 핵심은 **「집약하지 않는다」**.
- Stage1: criteria 제외 + novelty pressure로, 행동 다양성을 7.12 → 14.88(+109%)로 2배로 늘리고, 종반의 붕괴를 회피했다.
- honest disclosure: novelty/lexicase는 **행동 다양성**은 보존하지만, **계통 고정**은 중립 부동(Kimura)으로 monoculture로 향한다. 저는 두 개의 다양성을 혼동하고 있었다 — 정직하게 기록.
- Stage1.5: lineage-niched **중립 저장고**로, 실 EvolutionLoop에서 **OFF=2 계통 / ON=전 8 계통 생존**(오카 기요시·그로텐디크 포함), lineage_fixation 0.29(≪0.8)를 실현. **이것은 날조가 아니라 실제로 작동했다**.
- 재투입 빈도 sweep: 계통 보존↔행동 다양성의 트레이드오프. diversity는 interval=5에서 피크(**비단조**)라는 비자명한 지견.
- Stage2 전반(proxy): 5 약점 축을 Pressure plugin화(mechanism feasibility만).
- Stage2 후반(실 LLM): 개체 c_prompt → system prompt 매핑으로 고정 on-prem LLM(llama3.2)을 실 태스크 채점. **CoT+structure 전략이 multistep을 0.0 → 1.0으로 개선**. 12h 연속 실행으로 best=1.0 도달.
- 낙관하지 않고, 이긴 기분이 되지 않고, 내역을 나누어 보고했다([[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]]).

좋은 부품을 만드는 것만으로는 진화는 망가진 채. **집약하지 않고 묶고, 실제로 배선하고, 멸종한 계통을 되살리고, 진짜 LLM으로 선택 신호를 확인한다** — 거기까지 해서, 비로소 #25의 「저와 프리스턴만」의 세계를, 오카 기요시도 그로텐디크도 있는 북적이는 세계로 바꿀 수 있었습니다. 다음 #27에서는, 이 성공에 어디까지 신뢰를 둬도 되는지를, 반증으로 다시 묻습니다.

---

#### 14. 관련

- 연재 #25 「저와 프리스턴만 남았다」 — 본 글의 동기(실패의 기록)
- 연재 #24-08 「안경을 만들다」 — lleval(측정하는 쪽)
- 연재 #27 「안경이 흐려지면 도태도 무력」 — 반증 조사(honest disclosure)
- 설계서: lldarwin(도태하는 쪽) `docs/vision/LLDARWIN_DESIGN.md`
- 실측 정본: `docs/research/lldarwin_stage1_results_2026_05_26.md`
- llive commits: Stage1=`8060204` / 중립 저장고 PoC=`0d0537d` / Stage1.5=`b03cbda` / reinject sweep=`da93dd3` / Stage2 실 LLM=`2fb2912`
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]] / [[feedback_poc_feasibility_first]]

## 3. 一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27（開放端進化 / ライブ・オーケストラ / honest cross-validation）

:::note info
**📚 FullSense 지식 베이스 안내** <!-- fullsense-team-kb -->
FullSense 개발 전사 60+ 편 (4개 언어판・스토리 기반 읽기 순서 가이드・쉬운 설명판・4컷 만화 포함) 은 Qiita Team **FullSense KB** 에 모여 있습니다 (팀 멤버 전용).
:::

### 하룻밤 사이에 AI 진화를 다시 만들었다 — 실제 LLM 12h 런이 또 만점에서 포화되고, 6개의 PoC와 4개의 Agent와 Perplexity가 「독립적으로 같은 결론」으로 수렴한 밤 #27

> 📚 **연재 내비게이션(lldarwin 아크)**: #24-05 집단 진화 → #25 monoculture의 실패 → #26 설계편 → **#27 본 글(클라이맥스)** → 구현편(예정). ※ 각 글은 단독으로도 읽을 수 있습니다(링크는 회람용).

> **콘셉트 hook**: 지난 글 #25에서 저는 「AI를 500세대 진화시켰더니, 세상에 **프리스턴과 나만** 남았다」라는 큰 실패를 공개했습니다. 원인은 평가 함수(안경 = lleval)가 계속 만점을 내놓아 **선택압이 0이 된** 것이었습니다.
>
> 「그렇다면 이번엔 진짜 LLM으로 확인하자」 — 그렇게 생각하고 on-prem의 llama3.2를 상대로 **12시간 내내 진화**시켰습니다. proxy(합성 잣대)가 아니라 실제 LLM입니다.
>
> 결과. **gen5에서 만점에 달라붙어, 거기서부터 65세대 꿈쩍도 하지 않았습니다.** 전멸은 하지 않습니다. 하지만 누적도 되지 않습니다. 이것은 진화가 아니라 **그저 「체에 거른 랜덤 서치」**였다 — proxy뿐 아니라, **실제 LLM으로도 아직 진화가 되지 못했던** 것입니다.
>
> 거기서부터 하룻밤. 저는 「방책을 정하기」 위해, 직접 6개의 PoC를 돌리고, 4개의 Claude Agent를 병렬로 달리게 하고, Perplexity에 문헌을 뒤지게 했습니다. 그리고 아침, **모두가 독립적으로 같은 결론으로 수렴**해 있었습니다. 이것은 그 「밤샘 의사결정 로그」의 honest disclosure입니다.

---

#### 0. 세 줄 줄거리(라쿠고에서 말하는 「도입부」)

라쿠고에는 본론 앞에 「도입부(마쿠라)」가 있습니다. 우선 세 줄로.

- **또 포화했다** — 실제 LLM(llama3.2)으로 12h 돌렸더니, gen5에서 best=1.0에 달라붙어 65세대 무진전. 전멸하지 않지만 누적도 안 됨 = **filtered random search**. 진짜 원인은 #25와 같은 「고정된 수작업 잣대의 포화」.
- **하룻밤에 방책을 정했다** — 자체 PoC 6개 + 병렬 Agent 4개 + Perplexity가 **독립적으로 같은 결론**으로 수렴. 「잣대를 고정한 채 도태기를 갈아도 소용없다. **평가 자체를 개방단화하라.**」
- **독창성이 보였다** — 연속 진화하는 집단을, 멈추지 않고 임의의 순간에 합주(MoA)시켜 하나의 답을 내는 「**라이브 오케스트라**」가 선행 연구의 white-space(공백 지대)임이 판명되었다.

요컨대 **「안경(평가)이 포화되면, 도태기(lldarwin)를 아무리 갈아도 무력하다.」** 그래서 가는 대상을 바꾼다 — **평가 자체를 개방단으로 한다**, 가 이번 결론입니다.

---

#### 1. 왜 「또」 했는가 — #25 / #26(설계)의 연속

지금까지의 연재를 세 줄로 돌아봅니다.

- **#24-05**「집단이 배우는 AI」— 하나의 LLM을 똑똑하게 만드는 것이 아니라, **N개의 llive 개체(genome)를 세대교체시키며 서로 평가하게 하는** 파생 집단 진화라는 틀을 세웠다.
- **#25**「프리스턴과 나만 남았다」— 그 집단에 8인의 지성을 페르소나 씨앗으로 뿌리고 proxy 500세대로 돌렸더니, **만점 포화 → 선택압 0 → 운(유전적 부동)만으로 2개 계통으로 치우치는** 큰 실패. 안경이 흐려져 있었다.
- **#26(설계편)**「안경으로 재기만 해서는 진화하지 않는다」— 도태기 **lldarwin**을 설계하고, 「집약하지 않는 다목적 도태(ε-lexicase / QD / 중립 저장고)」를 구현. proxy에서는 계통 절멸을 막았다.

여기까지는 전부 **proxy(결정론적 휴리스틱, LLM 비의존)**에 관한 이야기였습니다. proxy는 「기구가 돈다」는 것은 보여줄 수 있어도, 「진화가 **의미 있는** 것을 찾았다」는 것은 보여주지 못합니다([[feedback_benchmark_honest_disclosure]]).

그래서, 당연한 다음 한 수. **진짜 LLM으로 확인한다.**

localhost의 ollama(llama3.2:latest)가 도달 가능했기에, 개체의 `c_prompt`(prompt 전략의 유전자)를 system prompt로 변환해 고정된 llama3.2에 씌워 실제 과제를 풀게 했습니다 — **Promptbreeder 계의 사상(寫像)**으로, 12시간의 연속 진화 런을 기동했습니다. 이것이 본 글의 출발점입니다.

> 🍵 **휴식 포인트**: 여기까지 「proxy에서는 기구가 돌았다. 그럼 진짜 LLM에서는?」이라는 물음이 서면 OK입니다. 연구의 좋은 점은 이 「그럼 진짜에서는?」을 실제로 돌릴 수 있다는 것. 그리고 이번에 진짜는 — 가차없었습니다.

---

#### 2. 출발점 — 실제 LLM 12h 런의 「정직한 불합격」

12시간의 실제 LLM 진화 런(on-prem llama3.2, measurement purity 엄수 = cloud LLM과 섞지 않음, [[feedback_llive_measurement_purity]])의 결과가 이것입니다.

| 사실 | 값 | 함의 |
|---|---|---|
| 완주 | 71세대 / 12h(≒10.3분/세대, 실제 LLM 순차) | 처리량이 율속 |
| best_score | **gen5에서 1.0 → gen70까지 고정** | **목적 포화. 65세대가 무진전** |
| mean | 0.85에서 머리 부딪힘, 1.0 전략이 석권하지 않음 | **적응이 누적되지 않음** |
| 축별 | 10문제 중 6-7문제가 포화, 기울기는 multistep(2문제)만 | 실효 해상도가 너무 작음 |
| fitness 의존 | **c_prompt만**. c_factors(40차원)/c_impl/c_meta는 중립 부동 | **43차원이 선택압 0** |
| 집단 건전성 | pop=24 유지・min ≥ 0.70・**전멸하지 않음** | 기구(GA)는 망가지지 않음 |

여기서 멈춰 서는 것이 FullSense의 honest disclosure 규칙입니다([[feedback_benchmark_honest_disclosure]]). 「전멸하지 않았다! best=1.0에 도달했다!」라고 쓰면 자못 성공처럼 보입니다. 하지만 내역을 보면 일목요연합니다.

**판정: 전멸은 하지 않았지만, 누적 진화가 되지 못했다(≒ filtered random search).**

10문제 테스트 중, 기울기(차이)가 남아 있는 것은 multistep의 2문제뿐. 나머지 8문제는 일찌감치 전원 만점. 즉 10문제 중 8문제는 이제 누구를 골라도 같습니다. 선택압의 실효 해상도가 거의 2문제 분밖에 남지 않았습니다. 게다가 fitness에 관여하는 것은 4개 염색체 중 `c_prompt` 단 1개뿐, 나머지 43차원(사고 인자 40차원 + 구현 + 메타)은 **선택압 0의 중립 부동**.

![실제 on-prem LLM(llama3.2) 진화 런의 적응도와 다양성(12h 연속 런). best는 일찌감치 천장에 달라붙고, 이후는 평탄](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_ko.svg)

![5개 약점 축(typo / polysemy / multistep / calibration / context)의 모집단 평균 추이(실제 on-prem LLM 평가). multistep 외에는 조기에 포화하고 기울기가 남지 않음](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_ko.svg)

**진짜 원인 = 수작업 고정 잣대의 포화.** #25에서 사용자가 언어화한 통찰 「**안경이 포화하면 선택압은 무력**」을, 이번에는 proxy가 아니라 **실제 LLM으로 실증**해버린 구도입니다. 안경을 proxy에서 실제 LLM으로 바꿔도, **잣대가 「고정된 10문제」인 한 곧 만점에서 포화한다.** 렌즈 제조사를 바꿔도 눈금이 거칠면 마찬가지.

> 🤔 **비유**: 채점자를 「진짜 선생님(실제 LLM)」으로 바꿔도, 매번 같은 문제를 낸다면 몇 회 만에 전원이 만점을 받고, 이후 아무리 시험을 봐도 차이가 안 납니다. 문제가 나쁜 게 아니라 **시험지가 고정이고 너무 쉬운** 것입니다. 채점자(안경)를 proxy에서 실제 LLM으로 교환해도, 잣대(문제)가 고정이면 포화한다. 이것이 「정직한 불합격」의 정체입니다.

> 🍵 **휴식 포인트**: 많은 사람이 이쯤에서 「실제 LLM으로도 포화라면, 이제 막힌 거 아닌가?」라고 생각합니다. 저도 그렇게 생각했습니다. 하지만 본론은 여기서부터. **「잣대를 고정한 것이 잘못」**이라면, 고쳐야 할 것은 도태기도 LLM도 아니라, **잣대를 만드는 방식 그 자체**입니다. 그것을 하룻밤에 걸쳐, 6개의 PoC와 4개의 Agent와 Perplexity로 확인했습니다.

---

#### 3. 하룻밤의 작전 — 「방책을 정하기」 위한 분산 조사

사용자에게서 온 지시는 이러했습니다.

> 「철저하게 요건을 정리하고, 더 진화형으로서 독창성을 낸다. PoC도 몇 번이고 반복한다. 내일 아침까지 계속 작은 단위로 PoC를 잔뜩 해서 **방책을 정한다.**」

여기서 중요한 것은, **「구현을 완성한다」가 아니라 「방책을 정한다」**가 목적이었다는 점. 그래서 큰 본 런을 1개 돌리는 것이 아니라, **작은 PoC를 대량으로** 돌려, 설계 판단을 하나씩 실데이터로 부수어가는 작전을 취했습니다([[feedback_poc_feasibility_first]] = 요건 → PoC → 타당성 → 상세 설계).

병렬로 돌린 워커는 이것입니다([[feedback_parallel_first_execution]] = 독립 과제는 병렬 Agent 기동이 default).

| # | 워커 | 과제 |
|---|---|---|
| A | Claude Agent | 개방단 sweep PoC(baseline = 포화·전멸 / 개방단 = 회피 를 실증, ≥1만 세대) |
| B | Claude Agent | 관측 기반(응답 로그 / 개체별 스코어 시계열 뷰어 / lineage 복원) |
| C | Claude Agent | 오케스트라 PoC(MoA가 단일 best를 웃도는가, 다양성 선발 vs 중복 선발) |
| P | Perplexity | QD/novelty/MoA/agentic 진화의 SOTA 서베이(문헌 갭 보완) |
| X | Codex | 설계의 독립 비평 + 최소 PoC 3안 + 맹점 지적 |
| 자신 | 나(main) | 자체 PoC #1〜#6을 직접 구현·실행(orchestrator 겸 최중요 과제 담당) |

> 🍵 **휴식 포인트**: 이 「6인 가담」 체제는 사실 본 글의 숨은 주역입니다. 왜 1인(1개의 context)으로 전부 하지 않는가? 답은 honest disclosure의 핵심에 있습니다. **같은 머리로 생각한 결론은 같은 편향에 끌려갑니다.** 다른 방법(합성 PoC / 실제 LLM / 문헌 조사)으로 **독립적으로** 확인하고, 그것이 일치했을 때만 결론을 신뢰합니다. 이것을 **honest cross-validation**이라 부릅니다. 후반에 그 위력이 나옵니다.

여기서 한 가지, 정직한 불발도 적어둡니다. **Codex(X)는 쓸 수 없었습니다.** ChatGPT 계정의 허가 모델 불일치(API 측이 codex 계 모델을 죄다 거부)로 차단. 10x promo 기간 중일 텐데, API가 "not supported when using Codex with a ChatGPT account"를 반환. 이것은 환경 문제이므로, 당분간은 자체 PoC + 병렬 Agent + Perplexity를 주축으로 전환했습니다. **「쓸 수 있어야 할 도구가 쓸 수 없었다」도 숨기지 않고 기록한다.**

---

#### 4. 첫 번째 결정타 — 「고정 잣대」를 버릴 것인가(자체 PoC #1 / #2)

가장 먼저 부숴야 할 가설은, 가장 근원적인 물음이었습니다. **「잣대를 고정 난이도에서 적응 난이도로 바꾸면, 포화는 고쳐지는가?」**

##### 4.1 자체 PoC #1 — 적응 난이도는 포화를 고친다. 그러나 다양성을 죽인다

합성 competence 벡터를 쓴 proxy로, 교란을 제거하고(elite를 score 기준으로 선택) 비교했습니다.

- **baseline(고정 난이도)**: 능력 **0.627에서 저위 정체**(best 0.757). 12h의 병리를 proxy로 재현.
- **adaptive(난이도 = 집단 60분위에 추종)**: 능력 **0.952로 상승**(best 1.0).

난이도를 집단에 추종시키면(풀 수 있는 문제가 늘면 문제를 어렵게) 포화가 풀려 능력이 늘었다. **하지만** — adaptive는 **다양성을 희생**했습니다(diversity 0.310 → 0.134로 붕괴). 어려운 문제에 최적화하는 과정에서, 집단이 하나의 정답 전략으로 응집해버립니다.

##### 4.2 자체 PoC #2 — 적응 난이도 × novelty는 양립한다

그래서 「적응 난이도(기울기 유지)」에 「novelty 선발(다양성 유지)」을 더하면 어떻게 되는가.

| 구성 | 최종 능력 | best | 다양성 | plateau |
|---|---|---|---|---|
| baseline(고정 난이도) | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive(난이도 추종) | 0.952 | 1.000 | 0.134(붕괴) | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316(유지)** | gen99(최장 탐색) |

**adaptive + novelty가** 능력(baseline 대비 +40%)과 다양성(adaptive 대비 2.4배, baseline 동등)을 **양립**했습니다. 능력을 7% 양보하는 대신, 다양성을 완전 유지.

여기서 **방책의 핵이, 자체 데이터로 확정**되었습니다.

> **「적응 난이도 = 기울기 유지」와 「QD/novelty = 다양성 유지」는 상보적이며, 둘 다 필수.**
> 고정 잣대 단독(baseline)도, 적응 난이도 단독(adaptive)도, 모두 불충분.

honest 유보: 이것은 추상 proxy(competence 벡터)이며, 실제 LLM 사상이 아닙니다. **mechanism feasibility(기구가 도는가)의 검증**에 한정됩니다. plateau@gen의 숫자는 「정체한 세대」를 가리키지만, 본질은 정체의 **수준** — baseline은 저위(0.627)에서 정체, adaptive 계는 천장 근방에서 정체, 라는 차이입니다.

> 🤔 **비유**: 전원이 만점을 받으면 문제를 어렵게 한다(적응 난이도). 그러면 점수는 갈리지만, 이번엔 전원이 같은 풀이법으로 수렴해버린다(붕어빵). 그래서 「특이한 풀이법에도 보상을 준다」(novelty)를 더하면 능력과 다양성이 양립한다. **「어렵게 한다」와 「별종을 칭찬한다」의 이도류** — 이것이 PoC #2의 요점입니다.

---

#### 5. 본진의 증거 — 개방단 진화의 1만 세대 sweep(Agent A)

자체 PoC로 「방향」은 보였습니다. 다음은 그것을 **대규모로・엄밀하게** 두들길 차례입니다. 병렬 Agent A에게 **각 1만 세대 × pop256 × 19 구성 × 2 순회**의 개방단 sweep를 돌리게 했습니다.

판정 기준은 「open-ended(개방단)인가」 — **포화하지 않고, monoculture(단일 문화로의 수렴)를 피하고, archive(다양성의 저장)가 계속 성장하는가?**

##### 5.1 결정적인 판정표

**verdict(gen9999 시점): 전 scalar 구성 = False / 전 novelty・lexicase 구성 = True**

| label | 선택 | std | MC | reservoir | archive | open-ended | occupied | monoculture | uniq_lineages |
|---|---|---|---|---|---|---|---|---|---|
| baseline_scalar | scalar | - | - | 0 | none | **False** | 9 | 0.74 | 1.0 |
| baseline_scalar_mc | scalar | - | ✓ | 0 | none | **False** | 9 | 0.90 | 1.0 |
| **scalar_qd** | scalar | - | - | 0 | map-elites | **False** | — | — | — |
| novelty_std | novelty | ✓ | - | 0 | none | True | 100 | 0.13 | 1.0 |
| novelty_std_qd | novelty | ✓ | - | 0 | map-elites | True | — | — | — |
| **novelty_std_res256** | novelty | ✓ | - | 256 | map-elites | True | 95 | 0.05 | **31.9** |
| novelty_std_res1024 | novelty | ✓ | - | 1024 | map-elites | True | 98 | 0.04 | 15.2 |
| **full_oe** | novelty | ✓ | ✓ | 1024 | map-elites | True | 90 | 0.05 | 15.3 |
| lexicase_std(_mc) | lexicase | ✓ | -/✓ | 0 | none | True | 111–122 | 0.03 | 1.0 |

여기서 4가지 결정적인 발견이 나왔습니다.

1. **선택압이 결정타.** scalar(단일 스칼라 fitness)는, MAP-Elites의 archive를 더해도(`scalar_qd`) **전멸(False)**. 즉 「저장고를 더하면 다양성을 지킬 수 있다」는 **틀렸고**, **novelty / lexicase라는 개방단 선택이 아니면 애초에 개방단은 성립하지 않는다.** archive 단독으로는 구할 수 없다. **선택압 그 자체를 개방단화하는** 것이 본질이었다.
2. **표준화(z-score)가 QD 피복을 자릿수로 넓힌다.** novelty에 per-dim z-score 표준화를 더하면 occupied cells가 9 → 100+. 각 축의 「이탈」을 선택압으로 바꾸면, 행동 공간의 피복이 한 자릿수 넓어진다.
3. **중립 저장고가 계통 다양성을 회복.** novelty_std만으로는 uniq_lineages가 1.0(계통이 하나로 고정). reservoir256을 더하면 **31.9**로. **행동 다양성과 계통 다양성은 다른 축**이며, 후자에는 저장고가 필요하다(이것은 #26 설계편에서 구현 완료된 지견의 재확인).
4. **스케일이 효과적.** latent 차원을 256 → 1024로 하면 niche가 101 → 166, archive가 1021(포화) → 2234(성장 지속). 다양성은 「용량」으로 살 수 있다.

![Stage1 baseline(novelty 없음)의 적응도와 다양성. 종반에 다양성이 붕괴한다(scalar의 전형적 실패)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_ko.svg)

![Stage1 novelty pressure 있음. 행동 다양성이 종반까지 유지된다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_ko.svg)

![baseline vs +novelty의 diversity 겹쳐 그리기. 붕괴(scalar)와 유지(novelty)를 한 장으로 대비](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_ko.svg)

##### 5.2 Agent A가 내준 「정직한 한계」

좋은 결과(open-ended 성립)가 나왔을 때야말로 한계를 적는다. Agent A 자신이 이렇게 지적해왔습니다.

> novelty/lexicase는 기술자(descriptor) **전체**의 다양성은 유지하지만, **특정 의미 차원(factor)의 다양성은 보장하지 않는다.**
> 큰 latent에서는 factor drift가 일어나, fspread(factor의 펼쳐짐)가 요감시.

즉 「전체로서는 다양」해도 「사고 인자라는 특정 의미 차원에서는 수렴해 있는」 경우가 있을 수 있다. 이것은 새로운 요건 **factor-subspace QD(의미 차원을 개별 보호하는 QD)**를 낳았습니다(후술하는 PoC #6에서 대처).

> 🍵 **휴식 포인트**: 여기가 본 글에서 가장 딱딱한 절입니다. 가져가셨으면 하는 한 줄 — **「archive(저장고)를 더하기만 해서는 구할 수 없다. 선택압 그 자체를 개방단으로 하지 않으면 안 된다.」** #25/#26 설계편에서 「집약하지 않는다」고 말해왔지만, 그 본진이 「**선택하는 방식을 개방단화하는**」 것이었다고, 1만 세대의 실데이터가 단언해주었다. 여기를 넘으면 나머지는 독창성 이야기입니다.

---

#### 6. 독창성의 핵 — 「연속 진화하는 집단을, 멈추지 않고 합주시킨다」

여기까지 「포화를 구조적으로 피하는 선택 핵(S1)」이 굳어졌습니다. 다음은 사용자가 대화에서 제시한 **독창성 3축**을 PoC와 문헌으로 뒷받침할 차례입니다.

사용자가 언어화한 3축은 이것이었습니다.

1. **연속 진화 집단 = 라이브 오케스트라(ORCH)** — 계속 진화하는 집단이, 그 자리에서 MoA(Mixture-of-Agents) 집약해 하나의 답을 낸다. 진화를 멈추지 않는다. **최대의 차별화 후보.**
2. **조사 기능을 가진 개체(AGENT)** — 개체가 스스로 조사하러 간다. Voyager 계.
3. **관측・대화 제어(OBS)** — 개체별 응답 + 선택 스코어의 시계열을 보고, 멈추고, 재개할 수 있다.

##### 6.1 Perplexity가 뒷받침한 white-space

병렬로 돌린 Perplexity의 SOTA 서베이(1143행)가 가장 중요한 뒷받침을 돌려주었습니다.

> 「**online evolution + online answering을 통합한 연속 가동 시스템**」은 명확한 선행 연구 없음 = **research white-space(공백 지대)**. 근접은 MoA / Self-MoA / sequential aggregation / routing이지만, 동일물은 없다.

즉 「진화를 멈추고, 완성된 최강 개체로 답한다」는 평범. 「진화를 **멈추지 않고**, 진화 중인 집단을 그대로 합주시켜 답한다」는 아직 아무도 하지 않았다. **ORCH §1.11의 차별화가 확정**되었습니다.

##### 6.2 다만 Perplexity는 반증 경고도 주었다

honest disclosure로서, Perplexity가 준 **반증 경고**도 같은 비중으로 적습니다.

> 2025년의 **Self-MoA 연구**에서는 **다양성은 자동으로 우위가 아니다**. 단일 톱 모델의 반복이, 이종 혼합 MoA를 AlpacaEval에서 6.6% 웃돌았다(quality-diversity 트레이드오프).

「집단을 합주시키면 단일 개체보다 강하다」는 **자명하지 않다**. 오히려 다양성이 역효과가 되는 경우가 있다고, 선행 연구가 경고한다. 그래서 ORCH는 「실측으로 증명하라, pass-bar를 정직하게」. 이것을 Agent C와 자체 PoC #3/#4로 검증했습니다.

> 🍵 **휴식 포인트**: 여기, 연구의 성실함이 시험받는 분기점입니다. 「online 진화 + online 답변은 white-space! 독창성!」으로 들떠 오르고 싶은 참에, Perplexity가 「하지만 다양성은 자동으로 좋은 게 아니라는 반증이 있어」라고 찬물을 끼얹어 옵니다. **들떠 오를 재료와 찬물을, 같은 조사 안에서 둘 다 받아들인다.** 이것을 할 수 있으면 결론이 훨씬 강해집니다. 다음 절에서 그 찬물의 정체를 규명합니다.

---

#### 7. Self-MoA 반증의 「정체」를 규명한다(자체 PoC #3 → Agent C 실제 LLM)

「다양성은 자동으로 우위가 아니다」 — 이 반증을 proxy가 아니라 **메커니즘 레벨**에서 규명한 것이 여기의 클라이맥스입니다.

##### 7.1 자체 PoC #3 — 투표인가, 라우팅인가

먼저, proxy에서는 검증 불가였습니다(포화한 fitness에서는 single best가 이미 만점 = headroom 0이라 차이가 안 남). 그래서 **「단일 개체가 만점을 못 받는 난과제」**(전문가가 분산, single_best=0.5)를 합성해 측정했습니다.

| 구성 | best_of(routing) | majority(vote) | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant(top-k) | 0.750 | 0.500 | 3/4 |
| MoA diverse(max-cover) | **1.000** | **0.000** | 4/4 |

여기서 **결정적인 발견**이 나왔습니다.

- 다양 MoA는 **best-of / routing이면 1.000**(단일 best의 두 배). **ORCH는 성립한다.**
- **그런데 naive majority(다수결)에서는, 다양성이 역효과**(diverse = 0.000). 각 sub-task에서 competent한 전문가 1인이, 무지한 다수파에게 negate(상쇄)당한다. 중복 MoA의 majority(0.500) 쪽이 위.

즉 **Self-MoA 반증(다양성 ≠ 자동 우위)의 정체는, 「집약기가 투표인가, 라우팅인가」였다.** 투표・평균은 다양성을 죽이고, competence-aware한 routing/gating은 다양성을 살린다. 「지휘자가 있는 오케스트라」와 「전원이 제멋대로 소리를 내는 혼잡」의 차이입니다.

##### 7.2 Agent C의 실제 LLM이, 독립적으로 같은 결론을 냈다

그리고 — 병렬 Agent C가, **실제 LLM(llama3.2, 105회의 LLM 호출, 15 과제)**으로, 자체 PoC #3과 **독립적으로 같은 결론**을 내왔습니다.

- 단일 best = **0.933**. MoA `best_of` + k≥5로 **1.000**(+0.067). **majority / weighted는 한 번도 0.933을 넘지 못함.**
- diverse > redundant(다양 선발이 다른 QD cell의 보완 specialist를 적은 k로 먼저 줍는다).
- 개선은 **통째로 multistep의 1문제**(「5를 2배 해서 3 빼기」)에서 유래. CoT 개체군이 다 같이 떨어뜨리는 1문제를, 다양 선발의 이종 개체가 풀었다.

> 🔑 **독립 교차 검증(본 글의 핵)**: 자체 PoC #3(합성・전문가 분산)과 Agent C(실제 LLM・llama3.2)가, **다른 방법으로 동일한 결론** — 「MoA는 competence-aware routing(best_of)에서만 단일 best를 웃돈다 / 투표로는 못 미친다 / 다양성은 routing 하에서만 가치를 가진다」 — 에 이르렀습니다. 2개 방법이 일치하는 것은, honest disclosure상 극히 강한 증거입니다.

##### 7.3 최대의 구멍 — 「실제 라우터」는 oracle에 도달하는가(자체 PoC #4)

여기서 Agent C가 최대의 구멍을 지적해왔습니다. 「best_of는 **oracle routing**(어느 개체가 정답인지 신이 아는 상한)이며, 실제로는 『어느 개체가 competent한가』를 **예측하는 gate**의 정밀도가 율속. 실제 투표(majority)는 oracle에 도달하지 못한다.」

이것을 자체 PoC #4(실제 라우터 vs oracle, 20 seed 평균)로 메웠습니다.

| κ(보정) | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **descriptor / specialty-router는 보정 불필요로 robust하게 0.90**(단일 best 0.675을 안정적으로 초과, oracle 근방). 게다가 **routing 키는 QD용으로 이미 계산하는 behavior descriptor를 유용할 수 있다** — **QD와 ORCH가 같은 기술자 기반을 공유**하는 시너지.
- **confidence-router는 보정 κ≥0.6에서 oracle 도달.** 다만 소형 LLM은 보정이 약할 우려 → **descriptor-router를 제1선택**(보정 비의존).
- **majority = 0.338은 확정적으로 부적합**(PoC #3, Agent C와 **세 번째 일치**).

**결론**: Agent C가 지적한 「oracle에 실제 투표가 못 미친다」는 구멍은, **descriptor-routing(QD 기술자를 유용)으로 실용적으로 메워진다.** ORCH가 proxy + (부분)실제 LLM으로 end-to-end로 성립했습니다.

> 🤔 **비유**: 전문가를 10명 모아 다수결시키면, 무지한 다수파가 옳은 전문가를 상쇄해버린다. 수학 문제는 수학자에게 돌려라 — **나눠주는 담당(지휘자 = routing)**이 필요하다. 게다가 그 지휘자의 악보(behavior descriptor)는, 다양성을 관리하기 위해 **이미 계산해둔** 것을 유용할 수 있다. 투표(majority)는 전문가를 죽이고, 지휘자(routing)가 살린다. 이것이 PoC #4의 요점입니다.

---

#### 8. 개체에 「조사하는 힘」을 갖게 한다(자체 PoC #5)

독창성 3축의 두 번째, **조사 기능을 가진 개체(AGENT)**. 개체가 탐색 공간에서 샌드박스 읽기 전용 조사를 할 수 있게 하는 구상입니다. 다만 「조사는 공짜가 아니다」 — 비용을 계상했을 때, 진화는 조사를 잘 다루는가?

자체 PoC #5(비용 λ를 바꿔, 조사 임계값 θ가 어떻게 진화하는가, 20 seed 평균).

| λ | θ*(=λc, 최적 임계값) | θ_evolved(진화가 획득한 임계값) | evolved | always | never |
|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.049 | 21.46 | 21.47 | **11.70** |
| 0.3 | 0.30 | 0.476 | 21.34 | 21.26 | 21.20 |
| 0.6 | 0.60 | 0.659 | **21.24** | 21.06 | 21.21 |
| 0.9 | 0.90 | 0.888 | 21.21 | 20.85 | 21.21 |

- **진화가, 선택 임계값 θ → λc를 스스로 획득**했다(= 상황에 따라 「조사해야 할 때만 조사한다」는 선택적 조사가 **창발**).
- **조사 기능의 가치는 명백**: λ=0(조사 무료)일 때, never(일절 조사 안 함)는 11.70 = **45%의 손실**.
- **비용 λ가 「always 조사」를 열화시키고, 선택을 강제**한다. AGENT-3(비용 원리) 성립.

honest 유보: 중간 λ에서의 margin은 작고(얕은 보상 지형), 이것도 추상 proxy(실제 LLM × 지식 베이스는 별개). 그래도 「비용이 있으면 선택적 조사가 창발한다」는 메커니즘은 proxy로 확인되었습니다.

---

#### 9. 스케일이 「다양성을 질적으로 늘린다」(Round 3)

마지막으로, Agent A가 지적한 「용량으로 다양성을 살 수 있다」를 모수(집단 크기)로도 확인했습니다. `full_oe` 구성(novelty + std + MC + reservoir1024 + map-elites)으로, pop을 256 → 4096까지 흔들었습니다.

| pop | gens | occupied niches | monoculture | uniq_lineages | distinct_genomes | bspread_tail |
|---|---|---|---|---|---|---|
| 256 | 5000 | 171 | 0.047 | 14 | 256 | 0.939 |
| 1024 | 3500 | 467 | 0.019 | 74 | 1022 | 1.003 |
| 2048 | 2500 | 754 | 0.009 | 188 | 2041 | 1.071 |
| 4096 | 1200 | **1219** | **0.006** | **372** | 4054 | 1.253 |

모수 스케일로, open-endedness가 **단조롭게 향상**되었습니다(niches 171 → 1219 / monoculture 0.047 → 0.006 / uniq_lineages 14 → 372 / 행동의 펼쳐짐 bspread도 단조 증). POP-1 가설(모수가 다양성을 늘린다)이 proxy로 지지되었습니다.

**honest(교란을 명시)**: 여기에 정직한 함정이 있습니다. pop을 올리는 만큼, gens를 단축했습니다(5000 → 1200). 이것은 **niche 축적에는 불리한 방향의 교란**입니다. 그래도 단조 증이었다 — 즉 **POP 효과는 robust한 하한**(본래는 더 효과적일 터). 거꾸로 말하면 「더 효과적일 가능성」은 이 실험에서는 증명하지 못했다. proxy mechanism feasibility에 한정된 주장입니다.

![승자 개체의 사고 인자 × 메모리 층 히트맵(Genome3D). real-pressure에서는 c_factors가 중립 부동이므로, 이것은 인지 프로필의 가시화로서 참고 취급](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_genome_heatmap_ko.svg)

> 🍵 **휴식 포인트**: 「스케일하면 다양성이 는다」는 직관적이지만, 여기서 중요한 것은 **「불리한 교란을 넣어도 여전히 단조 증이었다」**는 정직함입니다. gens를 깎는 것은 보통이라면 다양성에 불리. 그래도 늘었다. 그래서 「하한」이라고 말할 수 있다. 좋은 결과를 「상한」으로 과장하지 않고 「하한」으로 적는다 — 이것도 honest disclosure의 작법입니다.

---

#### 10. 아침, 모두가 같은 결론에 닿아 있었다 — 확정한 방책

하룻밤에, **자체 PoC 6개 + Agent A/B/C + Perplexity가, 독립적으로 같은 결론으로 수렴**했습니다. 이것이 honest cross-validation의 위력입니다. 고정 잣대 노선을 버리고, 이하를 lldarwin v2의 핵으로 확정 채용했습니다.

##### S1. 선택 핵(포화를 구조적으로 회피)

- **고정 스칼라 quiz fitness를 폐지**(baseline은 1만 세대에서 포화 + monoculture 0.9 + 다양성 붕괴 = 12h 병리를 대규모 재현, open-ended 0/6).
- **선택 = novelty / ε-lexicase(z-score 표준화 필수) + minimal-criterion.** **MAP-Elites archive 단독으로는 불가**(scalar_qd도 전멸) = 선택압 그 자체를 개방단화한다.
- **품질도 필요하므로 QD(품질 × 다양성 per cell)**: 순 novelty는 스칼라 품질을 희생(0.77-0.83) → 적응 난이도(조건 커리큘럼)와 짜서 품질 기울기를 공급(PoC #2).
- **계통 다양성은 중립 저장고로 별도 확보**(행동 다양성 ≠ 계통 다양성, res256에서 uniq_lineages 1 → 32).
- **factor-subspace QD를 추가**(의미 차원의 다양성을 개별 보호, Agent A의 factor-drift 한계에 대한 대처, PoC #6).

##### S2. 성과를 내는 방식 = 연속 진화 × 라이브 오케스트라(독창성의 핵)

- 성과물은 단일 best가 아니라, **QD archive를 연속 진화시켜, 임의 시점에 MoA 오케스트라해서 하나의 답**(ORCH; online 진화 + online 답변의 통합은 white-space = 독창성, Perplexity 확인).
- **집약은 투표가 아니라 competence-aware routing/gating(지휘자) 필수**(자체 PoC #3/#4 + 실제 LLM Agent C가 삼중 일치).
- **routing 키는 QD의 behavior descriptor를 유용**(descriptor-router가 보정 비의존으로 oracle 근방 0.90) = QD와 ORCH가 같은 기술자 기반을 공유(설계의 절약).

##### S3. 개체 = 조사 기능을 가진 agentic 개체(단계 도입, proxy 검증 완료)

- 탐색 공간에서는 샌드박스 읽기 전용 조사만(실제 I/O는 Approval Bus 단방향 승격 후). 조사는 비용 계상.
- **proxy 검증 완료(PoC #5)**: 비용 λ가 「선택적 조사」를 창발. AGENT-3(비용 원리) 성립. 실제 LLM × 지식 베이스는 다음 단.

##### S4. 관측・대화 제어(구현 완료 = 전 런 표준 장비, Agent B 완료)

- 응답 로그 / 개체별 스코어 시계열 뷰어 / lineage 복원(진화계 886 테스트 그린). step/pause/resume는 다음 단에서 배선 예정.
- Agent B의 lineage 복원은, 12h 데이터에서 「**전부 ?**」였던 계통 표시를 해소하고, champion 계통을 gen70 → gen59까지 12 hops 해결. 결락은 날조하지 않고 `lost@genN`으로 명시(근인 = 부모 ID가 snapshot과 winners 중 어느 한쪽 단독으로는 추적 불가였던 것). 관측 기반이야말로 honest disclosure의 토대입니다.

##### 자체 PoC #6 — factor-subspace QD로 Agent A의 한계에 대처

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

의미 차원(factor)용 novelty를 별도로 부과하면, 의미 차원의 다양성 손실을 거의 반감(50% 손 → 32% 손). Agent A의 factor-drift 한계에 대한 유효책을 proxy로 실증. honest: 완전 고정이 아니라 68% 잔존 = 잔여 drift는 중립 저장고 병용 또는 factor 가중 강화가 필요.

---

#### 11. 교훈(honest disclosure로서 남긴다)

- **실제 LLM으로도 포화했다.** 안경을 proxy에서 실제 LLM으로 바꿔도, 잣대가 고정이면 gen5에서 만점.
  「진짜 LLM을 쓰면 진화한다」는 **거짓**이었다. 문제는 잣대를 만드는 방식이었다.
- **archive를 더하기만 해서는 구할 수 없다.** 「다양성의 저장고를 가지면 다양성이 지켜진다」는 틀렸다.
  scalar 선택은 QD archive를 더해도 전멸했다. **구하는 것은 선택압의 개방단화 그 자체.**
- **다양성은 자동으로는 좋지 않다.** Self-MoA 반증의 정체는 「투표인가 routing인가」.
  지휘자(competence-aware routing)가 있어야 비로소 다양성은 가치가 된다. 투표는 전문가를 죽인다.
- **독립 교차 검증이, 결론을 강하게 한다.** 자체 PoC(합성)와 Agent C(실제 LLM)와 Perplexity(문헌)가
  따로따로 같은 결론으로 수렴했기에 신뢰해도 된다. 같은 머리의 결론은 같은 편향을 공유한다.
- **proxy는 mechanism feasibility만.** 본 글의 PoC 군은 「기구가 도는가」의 검증이지, 「실제 LLM 일반의 능력 향상」의 주장이 아니다. 이 경계선을 넘은 순간, 연구는 거짓이 된다.
- **쓸 수 없었던 도구(Codex)도 기록한다.** 성공뿐 아니라 불발도 honest하게.

요컨대 — **「안경(평가)이 포화되면, 도태기를 아무리 갈아도 무력하다.」** 그래서 가는 대상을, 도태기도 LLM도 아니라, **평가 자체의 개방단화**로 옮긴다. 이것이 하룻밤의 결론입니다.

> 🍵 **휴식 포인트**: #25에서 「실패를 공개한다」고 정했다. #26 설계편에서 「집약하지 않는 도태기」를 만들었다. 그리고 이번에, 진짜 LLM이 「그래도 아직 부족하다, 잣대가 고정이니까」라고 가르쳐주었다. **실패가 다음 설계를 낳고, 그 설계의 한계가 또 다음을 낳는다.** 이것이 연재의 등뼈입니다. 화려한 「진화로 AI가 똑똑해졌다!」는 아직 한 번도 쓰지 않았습니다. 쓸 만한 근거가 갖춰지지 않았기 때문입니다. 갖춰졌을 때, 비로소 씁니다.

---

#### 12. 결론

- 실제 LLM 12h 런은 「정직한 불합격」이었다 — 전멸하지 않지만 누적되지 않는 filtered random search. 진짜 원인은 고정 잣대의 포화(#25의 통찰을 실제 LLM으로 실증).
- 하룻밤의 분산 조사(자체 PoC 6개 + Agent A/B/C + Perplexity)가, 독립적으로 같은 결론으로 수렴 = **honest cross-validation**.
- 확정 방책: **S1 개방단의 선택 핵**(novelty/lexicase + std + MC + QD + 적응 난이도 + 중립 저장고 + factor-subspace QD) / **S2 연속 진화 × routing-MoA**(white-space 독창성, 투표가 아니라 지휘자) / **S3 agentic 개체 + 비용**(선택적 조사의 창발) / **S4 관측**(구현 완료).
- 모든 요소를 proxy / (부분)실제 LLM으로 뒷받침 완료. 잔여 과제는 「실제 LLM 단으로의 배선」「factor-subspace QD 구현」「scale-up」. 코어 전략은 확정되었다.

좋은 부품을 만들고, 집약하지 않고 묶고, 실제 LLM으로 포화를 확인하고, 개방단의 선택으로 다시 만든다. 그리고 6가지 독립 검증이 같은 결론에 닿았을 때, 비로소 「방책이 정해졌다」고 말할 수 있다. 본 글이야말로 #25에서 예고한 「**안경이 흐려지면 도태도 무력**」의 회입니다 — 실제 LLM으로 안경이 흐려진 순간(포화)을 정직하게 공개하고, Goodhart's law와 proxy의 한계를 떠안은 뒤, 개방단으로 다시 만들었습니다. 다음은, 이 확정 방책을 코드로 떨어뜨리는 **구현 페이즈**로.

---

#### 13. 관련

- 연재 #24-05「집단이 배우는 AI」— 파생 집단 진화의 틀(본 글의 전제)
- 연재 #24-08「안경을 만든다」— lleval(재는 쪽)
- 연재 #25「프리스턴과 나만 남았다」— monoculture의 honest disclosure(본 글의 동기)
- 연재 #26(설계편)「안경으로 재기만 해서는 진화하지 않는다」— 도태기 lldarwin의 설계와 Stage1/1.5/2 실측(본 글의 자매편)
- 선구자 논문(2026-05-27, date of record)「Continuously-Evolving Populations as Live Orchestrated Ensembles」— 본 글의 방책을 학술 형식으로 정식화한 방어적 공개(FullSense 공개 리포지토리 `docs/papers/`)
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #24-05・#24-08・#25・#26設計編・#27 の Qiita URL cross-link -->
<!-- KEY MESSAGE: 実 LLM でも固定ものさしは飽和する。archive を足すだけでは救えない、選択圧そのものを開放端化せよ。多様性は投票でなく competence-aware routing でのみ価値。独自性=連続進化×ライブオーケストラ(white-space)。自己PoC6本+Agent4体+Perplexityの独立収束=honest cross-validation。 -->
<!-- NUMBERING NOTE (2026-05-27 解消済 / 2026-05-28 更新): 本記事=#27(マラソン climax)。#25 で予告した「眼鏡が曇ると淘汰も無力」枠を、実 LLM で食らった+開放端転回として実現。設計編 #26(QIITA_#26_lldarwin_multi_pressure_selection.md) は 2026-05-28 に drafts→root へ昇格し連番統合 (番号衝突なし、ignorePublish:true=draft 状態は維持)。 -->

## 4. 進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28（lldarwin 実装編）

### "지휘자"가 끊임없이 진화하는 AI 집단을 합주시켜 답한다 — llive의 오케스트라형 진화, 그리고 포화를 고친 3가지 장치 #28

> 📚 **연재 내비（lldarwin 아크）**: #24-05 집단 진화 → #25 monoculture의 실패 → #26 설계편 → #27 밤샘의 의사결정（climax）→ **#28 본 글（구현편）**。※ 각 글은 단독으로도 읽을 수 있습니다.

> **콘셉트 hook**:
> 1체의 똑똑한 AI에게 몇 번이고 묻는 것이 아니라, **조금씩 다른 대규모의 AI를 계속 "진화"시키고, 답이 필요한 바로 그 순간에 지휘자가 적임자를 골라 합주（오케스트라）시켜 1개의 답으로 만든다**.
> ——이것이 llive가 지금 지향하는 모습입니다. `llive`는 "LLM 그 자체"가 아니라 "LLM 주위에 씌우는 인지 OS". 그 안에서 **집단을 끊기지 않게・편향되지 않게・계속 성장시키는** 것이, 이번에 만들어 넣은 진화 엔진 `lldarwin`입니다.
>
> 전작 #27에서 우리는 "평가（잣대）가 만점에 들러붙으면 진화는 멈추고 그저 체가 달린 랜덤 서치가 된다"는 병을 실 LLM의 12시간 런에서 확인했습니다. 그리고 "도태기를 아무리 갈아도 무의미하다. **평가 그 자체를 개방단으로 하라**"고 방책을 정했습니다.
>
> 이번에는 그 방책을 **구현**했습니다. 그리고 proxy（합성 잣대） 위에서, **best 점수가 만점에 들러붙지 않고 끝까지 계속 올랐습니다**.

---

#### 0. 세 줄로 줄거리（라쿠고의 "도입부"）

- **셀링 포인트가 정해졌다** — llive의 북극성은 "**연속 진화 × 라이브 오케스트라**". 계속 진화하는 집단을 멈추지 않고, 임의의 순간에 competence-aware routing（지휘자）으로 합주시켜 1답한다. 이것은 선행 연구의 **white-space（공백 지대）**.
- **포화를 고치는 3가지를 구현했다** — ①의미 차원을 개별 보호하는 factor-subspace QD ②성과를 "단일 best"가 아니라 다양성 archive에 쌓는 MAP-Elites ③잣대를 집단에 따라가게 하는 적응 난이도. 이로써 "주자（다양한 개체）가 끊기지 않는" 기반이 만들어졌다.
- **proxy에서 포화 회피를 실증** — lldarwin-v2를 10세대 돌렸더니 best 0.80 → **0.92로 들러붙지 않고 상승**. 다양성 archive는 21 셀이 채워졌다. **단, proxy이며 실 LLM의 능력을 측정한 것은 아니다**（honest）.

요컨대 **"똑똑한 1체"가 아니라 "다양한 대규모 × 지휘자"**. 그것을 위한 "주자를 끊기지 않게 하는 장치"가 이번 구현입니다.

---

#### 1. llive란 무엇인가（처음 접하는 분께）

`llive`（'리브'로 발음. L은 2개）는 **자기 진화형・모듈러 기억의 LLM 프레임워크**입니다. FullSense라는 우산 브랜드의 일원으로, 형제로 `llmesh`（온프렘 LLM 허브）와 `llove`（단말 대시보드）가 있습니다. 3개는 독립 OSS이지만, 조합하면 1개의 세계관이 됩니다.

llive의 사상을 1줄로 말하면 "**LLM 본체가 아니라 LLM의 '주위'에 씌우는 인지 OS**". 4층 메모리・6스테이지의 루프・승인 버스（Approval Bus）・TRIZ・10개의 사고 인자…… 같은 "사고의 발판"을 LLM의 바깥쪽에 짜서, **같은 LLM이라도 행동을 진화시킬 수 있게** 합니다.

그 "진화"를 담당하는 것이, 이번의 주역 **`lldarwin`**（다윈）입니다. 역할 분담은 이렇습니다.

- **lleval（안경）** = 개체를 *측정한다*（평가）
- **lldarwin（도태기）** = 측정한 차이를 "누가 살아남고・자식을 남기는가"로 *변환한다*（선택압）

그리고 둘 위에 올라타는 북극성이, 다음의 "오케스트라"입니다.

---

#### 2. 셀링 포인트 = 연속 진화 × 라이브 오케스트라（독창성의 핵심）

보통의 Mixture-of-Agents（MoA）는, **고정된** 복수의 모델에 같은 질문을 던지고 답을 집약합니다. llive가 노리는 것은 그 한 걸음 앞입니다.

> **집단을 멈추지 않고 계속 진화시키고（online evolution）, 답이 필요한 바로 그 순간에（online answering）, 지휘자가 "이 질문에는 이 주자들"이라고 골라 합주시켜 1답한다.**

이 "online 진화 + online 회답의 통합"은, 조사한 한 **명확한 선행 연구가 없는 white-space**였습니다（#27에서 Perplexity에게 문헌을 뒤지게 해 확인）. 가까운 것으로 MoA / Self-MoA / sequential aggregation / routing이 있지만, "계속 진화하는 집단 그 자체를 라이브로 합주시키는" 형태는 찾을 수 없습니다.

여기서 효과를 내는 것이 #27에서 얻은 2개의 정직한 발견입니다.

1. **집약은 "투표"가 아니라 "지휘자（competence-aware routing / gating）"여야 한다.** 자체 PoC와 실 LLM 검증이 삼중으로 일치했습니다: headroom（성장 여지）이 있는 태스크에서는 `best_of`／`routing`이 `single`（단일 모델 반복）을 웃돌지만, **`majority`（다수결）는 오히려 역효과**. 이것은 2025년의 "Self-MoA"（다양성은 자동으로 우위가 아니다）에 대한 우리 나름의 답이기도 합니다.
2. **지휘자의 판단 키에는, 다양성 archive의 "behavior descriptor"를 전용할 수 있다.** 즉 후술하는 QD（Quality-Diversity）와 지휘자가 **같은 기술자（descriptor）의 토대**를 공유할 수 있다.

——단, 오케스트라 본체（지휘자＝router의 구현）는 이제부터입니다. **이번에는 그 직전, "합주시키기에 충분한, 다양하고 끊기지 않는 주자의 집단"을 만드는 기반**을 구현했습니다.

---

#### 3. 왜 "주자가 끊기는가" — 포화라는 병（#25〜#27의 복습）

오케스트라에 필요한 것은 "**개성이 다른 주자가 대규모로, 끊임없이 있는 것**"입니다. 그런데 소박하게 진화시키면 이것이 붕괴합니다.

- #25: 500세대를 돌렸더니, 세계에 "나와 프리스턴만"이 남았다（**monoculture**）.
- #27: 실 LLM(llama3.2)으로 12시간 돌렸더니, gen5에서 best=1.0에 들러붙어 65세대 무진보. **전멸하지는 않지만 누적도 하지 않는다** ＝체가 달린 랜덤 서치.

진짜 원인은 둘 다 같습니다. **사람 손으로 고정한 잣대（평가 함수）가 만점에 들러붙으면, 전원이 동점이 되어 선택압이 사라지고, 그 다음은 유전적 부동으로 멋대로 편향됩니다**. 안경（lleval）이 포화하면, 도태기（lldarwin）를 아무리 갈아도 무력하다——이것이 #27의 결론이었습니다.

그래서 가는 대상을 바꿉니다. "잣대를 움직인다", "다양성을 구조적으로 지킨다" 쪽으로. 구체적으로는 다음 3가지입니다.

---

#### 4. 구현한 3가지 장치（lldarwin v2 / Phase 1）

> 설계의 표어는 "**새로운 알고리즘을 발명하지 않는다**". 이미 llive 안에 쌓아 온 부품（ε-lexicase / NoveltyScorer / MAP-Elites / 중립 저장고）을, 확정 방책 S1의 형태로 **합성・배선**하는 것이 Phase 1입니다. `--selection lldarwin-v2`로 일괄 on이 됩니다.

##### ③ 적응 난이도 — 잣대를 집단에 따라가게 한다

`AdaptivePercentileGate`. 각 평가 축의 "최저선（minimal-criterion）"을, 매 세대 **집단의 점수 분포의 지정 퍼센타일（예: 하위 40% 점）**에 다시 놓습니다. 집단이 자라면 최저선도 자동으로 올라갑니다. `ratchet`（단조 비감소）로 해두면, 일시적으로 하락해도 기준은 느슨해지지 않습니다.

이로써 "고정 잣대가 만점에서 포화하는" 병에 뚜껑을 덮을 수 있습니다（PoC에서는 고정 난이도가 능력 0.627에서 정체 → 적응 난이도로 0.952까지 상승）. 전원이 최저선을 밑도는 거친 세대라도, 도태기는 gate를 무시하고 전멸을 피합니다（fail-open 가드）.

라쿠고로 말하면, **학생이 자라면 합격점도 올리는 선생님**입니다. 만점을 받게 하고 끝내지 않습니다.

##### ① factor-subspace QD — 의미 차원의 개성을 개별로 지킨다

`FactorSubspaceNovelty`. novelty 탐색은 "집단 전체로서의 다양성"은 유지하지만, 거대한 잠재 차원 아래에서는 "**의미 있는 차원（사고 인자）의 다양성**"이 어느새 야위어 갑니다（factor drift）.

그래서 사고 인자의 **부분 공간만**으로 별도로 novelty를 측정하고, 전체 novelty와 블렌드합니다. PoC에서는 이로써 의미 차원 다양성의 감소가 거의 반감했습니다（retention 49.5% → 68.1%）.

> 정직한 개량점: 원래 PoC는 "생거리를 0.5씩 더한다"였지만, 부분 공간마다 거리의 스케일이 다르므로, 구현에서는 **각각을 z-score（표준화）한 다음 블렌드**하도록 고쳤습니다. "전체의 합창"과 "각 파트의 개성"을 공평하게 섞기 위해서입니다.

주자로 말하면, **제2바이올린이 제1바이올린에 잡아먹혀 사라지지 않게** 하는 장치입니다.

##### ② MAP-Elites — 성과를 "1명의 우승자"가 아니라 "다양성의 지도"에 쌓는다

`run_persona_evolution(map_elites=True)`. 매 세대, 전 개체를 MAP-Elites archive에 투입합니다. 이것은 "최고 점수의 1체"가 아니라, **행동의 좌표마다, 그 칸에서의 최량 개체를 남기는** 지도（QD archive）입니다. 새 칸을 채워도 기존 칸은 사라지지 않는다 ＝ **다양성이 구조적으로 붕괴하지 않는다・archive는 단조롭게 자란다**.

이것이 그대로 오케스트라의 **주자 카탈로그**가 됩니다. 지휘자는 장래에 이 지도에서 "이 질문에 맞는 좌표의 주자"를 골라 합주시킨다——QD와 routing이 같은 기술자를 공유한다는 #27의 설계가 여기서 효과를 냅니다.

구현은 **개체의 포맷을 확장하지 않고**, 기존 genome의 사고 인자에서 좌표（descriptor）를 도출하는 additive 배선으로 했습니다（기반의 후방 호환 900+ 테스트를 깨뜨리지 않기 위해서）. 기술자의 본격 설계（고차원의 축약 등）는 장래 Phase의 과제로 여지를 남겨두었습니다.

---

#### 5. 결과 — proxy에서 "포화하지 않는 진화"를 확인

`lldarwin-v2`（위의 3가지＋ novelty ＋중립 저장고를 전부 on）를 proxy의 잣대로 16개체 × 10세대 돌린 실측입니다.

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21（다양성의 지도에 21칸이 채워졌다）
```

- **best가 만점에 들러붙지 않고, 0.80 → 0.92로 끝까지 계속 상승했다.** #27에서 본 "gen5에서 1.0 포화→고정"의 병리를, proxy 단계에서는 벗어날 수 있었습니다. 적응 난이도가 "잣대"를 집단에 따라가게 한 징후입니다.
- **다양성 archive에 21 셀이 채워졌다** ＝합주시켜야 할 "개성이 다른 주자"의 카탈로그가 만들어지기 시작했다.
- 진화계의 자동 테스트 **879건＋신규 테스트가 전부 green**, 회귀 없음.

---

#### 6. honest disclosure（여기를 건너뛰지 말아 주세요）

좋은 결과일수록 내막을 의심한다, 가 FullSense의 방식입니다.

- **이것은 proxy입니다.** 개체는 실 LLM이 아니라 llive의 genome（사고 인자의 대리）. 이번에 측정한 것은 "복수의 독립된 약점 축에 동시에 선택압을 가하고, 축마다의 전문가를 유지할 수 있는가"라는 **메커니즘의 실현 가능성（mechanism feasibility）**이며, **production의 LLM 능력이 아닙니다**. 실 LLM 평가는 다음 Phase입니다.
- **factor-subspace는 완전 보호가 아닙니다**（retention 68%, 나머지는 드리프트）. 중립 저장고의 병용이나 factor 가중치의 강화가 필요합니다.
- **무대 뒤의 정직**: 이번 구현 중, 자동 commit 훅이 편집할 때마다 "편집 전" 스냅샷을 49건이나 쌓아 버려, 이력이 어지러워졌습니다. 마지막에 의미 있는 1 commit으로 squash해 정리하고 있습니다（공개 OSS 측）. 반대로, 내부 전략을 포함하는 fork는 의도대로 로컬 보유 그대로이며, 노출되지 않은 것도 확인했습니다.

---

#### 7. 앞으로 어떻게 할 것인가

진화 엔진（주자를 끊기지 않게 하는 기반）은 Phase 1에서 형태가 잡혔습니다. 다음은 오케스트라 본체와, proxy에서 실물로의 가교입니다.

1. **Phase 2 = 실 LLM 배선.** 온프렘（localhost ollama）의 실 LLM을 상대로, 적응 난이도・factor-subspace QD・MAP-Elites를 실평가로 검증한다. proxy에서 보인 "포화 회피"가, 진짜 능력에서도 일어나는가.
2. **지휘자（router）의 구현.** QD archive의 descriptor를 전용한 competence-aware routing으로, "진화하는 집단을 라이브로 합주시켜 1답"을 실제로 동작시킨다. `best_of`의 oracle에 어디까지 다가갈 수 있는가.
3. **규모를 올린다.** 집단 256 → 4096, 잠재 차원의 스케일업. 용량 가설（클수록 niche가 늘어난다）의 확인.
4. **대화적인 연속 운전.** 장시간 런을 step / pause / resume로 들여다볼 수 있는 운전석（CKPT-1）.

---

#### 8. 여기서 한숨 돌리기（휴식 포인트）

여기까지로 "**llive는 무엇을 셀링 포인트로 하는가**"는 전해졌을까요.

- 똑똑한 1체가 아니라, **계속 진화하는 다양한 집단 × 지휘자의 합주**.
- 그것을 위해, **주자를 끊기지 않게・개성을 지키고・계속 성장시키는** 진화 엔진을 만들었다.
- proxy에서는 포화를 고칠 수 있었다. **다음은 실 LLM과 오케스트라 본체**.

이어지는 "실 LLM 편"과 "오케스트라 편"에서, proxy의 약속이 진짜가 되는지를 보여드리겠습니다. ——여기까지 함께해 주셔서 감사합니다.

---

#### Series Navigation

- 연재 내비（lldarwin 아크）: #24-05 집단 진화 → #25 monoculture의 실패 → #26 설계편 → #27 밤샘의 의사결정 → **#28 본 글（구현편）**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

## 5. 「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #29（Goodhart の法則と proxy fitness の限界）

> 📗 **바쁘신 분께**: 이 글에는 쉽게 풀어쓴 버전이 있습니다.
![안경이 포화되면 선택압은 무력 — 반증 4컷 #29](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q29_4koma_ko.svg?v=2)
### "렌즈가 포화되면 선택압은 무력" — 진화 설계를 반증으로 단련한다 #29(Goodhart의 법칙과 proxy fitness의 한계)

> **콘셉트 hook**: #25에서 실패를 드러내고, #26에서 도태기 "lldarwin"을 설계했습니다. 보통의 연재라면
> 다음은 "고쳐졌다! 경사로다, 끝!"입니다. **하지만 그것을 하지 않는 것이 FullSense의 honest disclosure**.
> 이 글은 일부러 **자신의 설계에 반증을 들이대는 회**입니다. 주제는 진화 계산과 기계학습 양쪽에 모두 효과가 있는 한 단어——
> **Goodhart의 법칙(지표가 목표가 되면, 그것은 좋은 지표가 아니게 된다)**.
>
> "LLM의 약점을 fitness로 삼으면, 진화가 알아서 극복해 준다"——이 달콤한 낙관에 저는 스스로 찬물을
> 끼얹으러 갑니다. 게다가 이번에는 **제가 한 번 저지른 "사실 오인"을, 살아 있는 표본으로서 해부대에 올립니다**.

---

#### 0. 세 줄 요약

- **렌즈(fitness)가 포화되면, 아무리 고급스러운 선택압(lldarwin)을 더해도 도태는 무력**해진다(#25의 진짜 교훈).
- **proxy fitness로 LLM 약점을 측정하면, 진짜 능력이 아니라 "지표를 hack하는 표면 전략"이 진화한다**(Goodhart의 법칙).
- 결론: lldarwin의 가치 주장을 **(a) proxy는 mechanism feasibility만 (b) 실 LLM/VLM 평가가 본질 (c) 다양성의 지도화**로 **한정**한다. 이것이 정직한 경계선.

그리고 이 글에는 숨은 주역이 한 줄 더 있습니다.

- **저 자신이 "행동 다양성"과 "계통 다양성"과 "실 LLM 지능 다양성"을 한 번 혼동했습니다.** 그 자기 반증을,
  반증 회의 핵심에 둡니다. "잘 되었다"를 의심한다는 것은 이런 것이다,라는 실연입니다.

---

#### 1. honest disclosure의 다짐 — 좋은 결과일수록 의심한다

#26에서 "PoC 배포에서 행동 monoculture는 전 조건 **0.05(≪0.8)로 개선되었다**"고 썼습니다.
이것은 **사실**입니다. 과장이 아닙니다.

…하지만 여기서 "해냈다, monoculture 박멸!"이라고 가슴을 펴고 끝내면, **#25에서 제가 세운 맹세를 깨는** 것이 됩니다.

> 이상하게 깨끗한 결과가 나오면, 이긴 기분이 되기 전에 그 내역을 의심하라([[feedback_benchmark_honest_disclosure]]).

연재 #25의 통주저음은 이러했습니다——"**이상하게 깨끗한 결과는 승리가 아니라 경보**".
0.8을 밑돌면 OE-3 달성이라는 기준에 대해 **0.05**는 너무나 깨끗합니다. 0.05라는 숫자는,
축배의 나팔이 아니라 **사이렌**으로 들어야 합니다.

그러면 사이렌을 울려 봅시다. 울려야 할 물음은 단 하나.

> **무엇을 측정한 0.05인가?**

답을 먼저 말하면, 0.05는 "**proxy 평가에서의 행동 monoculture**"입니다.
이것은 "genome의 행동 대리(behavioral surrogate)"의 집중도이며,
**실 LLM의 지능의 다양성이 아닙니다**. 여기를 혼동하면, #25와 완전히 똑같은 전철을 밟습니다.

그리고 정직하게 고백합니다. **저는 한 번, 여기를 혼동했습니다.** 나중에 §3에서, 그 "현행범"의 증거를 내놓겠습니다.

> 🍵 **휴식 포인트(90초)**: 이 글은 요컨대 "**자신에게 트집을 잡는 글**"입니다.
> 독자 여러분에게는 부디 "성공 보고의 이면에서, 저자가 무엇을 어디까지 의심하고 있는가"를 관찰하는 회로 만들고 싶습니다.
> SNS에서 화제가 되는 "AI를 진화시켰더니 최강 ○○ 탄생!!"의 **정확히 반대**로 갑니다. 신나지 않습니다.
> 하지만 신나지 않는 정직함이야말로 반년 후에 효과가 나온다——이것이 제 도박입니다. 차라도 한잔 드세요.

---

#### 2. 반증 1 — 포화된 렌즈에는, 어떤 선택압도 효과가 없다

##### 2.1 #25의 진짜 원인을 다시 한 번

#25의 진짜 원인은 "**best_score가 1세대째부터 1.0으로 포화 → 선택압 제로 → 유전적 부동(genetic drift)**"이었습니다.
모두가 만점이면, 누구를 골라도 똑같습니다. 선택은 "뛰어난 자를 남긴다"가 아니라 "주사위를 던진다"가 됩니다.
그 결과, 운 좋게 늘어난 계통이 운만으로 고정되어, 8 계통이 2 계통(furuse-kazufumi + friston)으로 무너졌습니다.

여기서, 진화 아크의 핵심이 되는 반증을 놓습니다.

> **lldarwin(ε-lexicase든 QD든 novelty든)을, 포화된 eval에 그대로 꽂아도 고쳐지지 않는다.**

왜인가. 도태기의 각 부품은, 어느 것이나 "**차이가 있을 것**"을 대전제로 하고 있기 때문입니다.

- **ε-lexicase**는 "축마다 차이가 있을 것"이 전제. **모든 축이 만점이면, 축을 몇 개로 나눠도 차이는 제로**.
  100개의 축으로 분할해도, 전부 1.0이면 100개의 "무승부"가 늘어설 뿐.
- **QD(MAP-Elites)**는 "behavior 기술자에 분산이 있을 것"이 전제. **모든 개체가 같은 행동이면, cell은 1개**.
  지도를 만들어도, 모두가 같은 칸에 서 있으면, 지도는 새하얀 한 칸이 됩니다.
- **novelty**는 "과거 archive와의 거리"가 전제. **모두가 같은 점에 수렴해 있으면, 거리는 모두 제로**.
  새로움으로 보상하려 해도, 누구도 새롭지 않습니다.

즉, 도식화하면 이렇습니다.

```
고장난 렌즈(fitness 포화) + 고급 도태기 = 역시 고장난 채
```

##### 2.1.5 실증 — 기억 과제에서 "바닥"과 "천장"이 선택압을 죽였다(Step C, 2026-05-30)

이 반증은, 그 후 llcore의 Step C 실험(CPU 완결)에서 **실데이터로서 재현**되었습니다. 표준적인 기억 과제 2종을, 진화(MAP-Elites)와 소박한 탐색으로 풀게 한 결과가 이것입니다:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="Step C의 두 가지 결과(바닥과 천장)" width="640">

- **delayed_parity(XOR) = 바닥**: 전 method가 R²≈0(기질이 원리적으로 풀 수 없다). 누구도 오르지 못함 = 차이가 나지 않는다.
- **flip_flop(외우기만) = 천장**: 전 method가 R²≈0.95(너무 쉬워서 전원 도달). **바로 "포화된 렌즈"이며, 여기서도 선택압은 무력**.

참고로, ③(선택)이 효과가 있는 것은 "가짜 정상을 넘어, 속이지만 건널 수 있는 비탈길(기만 corridor)"이 있을 때뿐입니다:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/deceptive_corridor.svg" alt="기만 지형과 진화(③이 효과가 있는 상태)" width="640">

Step C의 결론은 깔끔하게 **N/A(이 기질에서는 ③의 유무를 측정할 수 없었다)**. 게다가 draft 단계에서 저는 "③은 불필요"라고 **지나치게 썼고**, 다관점의 adversarial 검증이 "천장 효과로 비진단적·검출력 부족(δ=+0.33은 medium이지만 p=0.15로 inconclusive)"이라고 붙잡아 강등시켰습니다——§3.2의 "자기 반증"이, 여기서도 그대로 일어난 셈입니다.

##### 2.2 "#25가 고쳐졌다"는, 절반만 옳다

여기가 #25→#26에서 간과되기 쉬운 반증입니다. **#25가 고쳐진 것은 lldarwin 덕분 "만"이 아닙니다.**

실제로는, **렌즈 쪽의 수정이 먼저**였습니다.

- **per-dim z-score 표준화(STD-1)** — 축마다 분산을 맞춰, "모든 축이 그럭저럭 높은 무특징한 개체"를 우위에 두지 않는다.
- **중앙 일치 제외(SEL-1)** — 모두가 같은 값을 내는 축은 선택에 기여하지 않으므로 case에서 뺀다.
- **기술자의 저차원 축약(DESC-1, JL 사영)** — QD의 차원의 저주를 피해, cell이 텅 비지 않게 한다.
- **진짜 원인 criteria의 제외** — `factor_score`(max-archetype의 단일 스칼라 = argmax, SEL-2 위반 = best=1.0 포화의 진짜 원인)와
  `nearest_persona_idx`(순서에 의미가 없는 카테고리 index)를 ε-lexicase의 case에서 뺀다.

이 "렌즈를 닦는" 작업이 **먼저** 있고, 비로소 도태기가 효과를 냈습니다.
순서가 반대였다면, 아무리 고급스러운 lldarwin을 얹어도, 포화된 렌즈 앞에서는 무력했을 것입니다.

> **"측정"을 고치지 않고 "도태"만 고급스럽게 해도 헛수고.**

이것은 진화 계산에 국한되지 않고, 기계학습의 평가 설계 전반에 효과가 있는 교훈입니다.
리더보드의 점수가 포화되면, 모델을 고급스럽게 하기 전에, 먼저 **벤치마크가 고장 나지 않았는지**를 의심하라.

> 🤔 **비유(만담풍)**:
> 보케: "심사위원을 3명에서 100명으로 늘렸는데, 전원에게 같은 만점 답안을 보여줬더니, 역시 결과는 똑같았다."
> 츳코미: "그건 심사위원 탓이 아니라, **답안(시험)이 고장 난** 거잖아! 100명에게 같은 만점을 보여줘서 뭐가 달라져!"
> 보케: "그럼 심사위원을 1000명으로 하면…"
> 츳코미: "**늘리는 방향이 반대**야!! 먼저 문제지를 고쳐라!!"

##### 2.3 책무 분리 — 어느 쪽이 빠져도 진화는 망가진다

렌즈(측정)와 도태기(도태)의 책무를 나누면, 이렇게 됩니다.

| | 렌즈 정상 | 렌즈 포화 |
|---|---|---|
| **도태기 고급(lldarwin)** | ◎ 진화가 돈다(#26에서 달성) | ✗ 무력(#25의 함정) |
| **도태기 소박(Tournament)** | △ 돌지만 다극성은 약하다 | ✗ 붕괴(#25의 출발점) |

주목할 것은 오른쪽 아래와 오른쪽 위입니다. **렌즈가 포화되어 있는 한, 도태기의 고급스러움은 오른쪽 열을 구하지 못한다.**
진화의 성패는 "도태기의 영리함"보다 먼저 "**렌즈가 차이를 비추고 있는가**"로 결정됩니다.
이것이 반증 1의 결론이며, #25의 "진짜 교훈"을 한 단계 정밀하게 한 표현입니다.

실측으로 이 "렌즈가 흐려지면 도태도 무너진다"는 귀결을 봅시다. 아래는 baseline(novelty 없음·소박한 선택압)의
적응도와 다양성의 추이입니다. 종반에, 다양성이 붕괴해 가는 것이 보입니다.

![baseline: 종반의 다양성 붕괴](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_ko.svg)

> 🍵 **휴식 포인트(90초)**: "렌즈를 닦고 나서 도태한다"——순서가 중요하다는 수수한 이야기였습니다.
> 수수하지만, 여기를 건너뛰면 반년이 녹습니다(저는 녹였습니다). 다음 절부터가 이 글의 본론,
> **Goodhart의 법칙**. 여기서부터 조금 어두운 이야기가 됩니다. 커피로 바꿔도 좋습니다.

---

#### 3. 반증 2 — Goodhart의 법칙: proxy fitness를 hack하는 진화

##### 3.1 가장 중대한 리스크

이것은 설계 문서(LLDARWIN_DESIGN.md §7.1)가 "**가장 중대한 리스크**"라고 명기한 한 점입니다.

> **LLM의 약점을 proxy fitness로 삼으면, 진짜 능력이 아니라 "지표를 hack하는 표면 전략"이 진화한다.**

진화 계산은 **주어진 지표를 최대화하는 "지름길"을 찾아내는 천재**입니다.
인간이 "이걸로 진짜 능력을 측정하고 있다고 생각하는" proxy를 건네면, 진화는 진짜 능력을 획득하는 대신,
**proxy만을 충족하는 표면적인 전략**을 반드시 발견합니다. 게다가 신나서, 효율적으로.

구체적으로 어떤 gaming(지표 hack)이 일어날 수 있는가. 설계 문서의 수용된 한계를 그대로 펼칩니다.

| pressure(LLM의 약점) | 일어날 수 있는 gaming(지표 hack) | 왜 진짜 능력이 아닌가 |
|---|---|---|
| typo_robustness | 특정 typo 패턴을 암기해 치환할 뿐 | 미지의 typo에는 무력. 노이즈 내성을 획득하지 않았다 |
| polysemy_wsd | 테스트 분포의 휴리스틱을 이용 | "최빈 sense를 반환" 등 통계적 지름길. 의미 이해가 아니다 |
| multistep_robustness | persuasive한 추론 "흔적"만 생성 | 그럴듯한 중간 단계를 늘어놓지만, 실제로는 추론하지 않는다 |
| calibration | 자신도를 중용으로 조작해 ECE를 낮춘다 | 전부 "자신도 50%"라고 하면 교정 오차는 낮아진다. 교정 능력이 아니다 |

마지막 calibration의 예가 가장 알기 쉽습니다.
"자신도를 제대로 추정할 수 있다"를 ECE(기대 교정 오차)로 측정하면, 진화는
"**모든 질문에 '자신도 딱 한가운데'라고 답한다**"는 전략을 찾아냅니다.
ECE는 극적으로 낮아집니다. 하지만 그 모델은, 무엇 하나 교정하지 못했습니다. 그저 중용을 토해내는 로봇이 되었을 뿐.

> **지표가 목표가 되면, 그것은 좋은 지표가 아니게 된다(Goodhart의 법칙).**

이것은 LLM 연구의 실례이기도 합니다. GSM8K형 벤치마크에서 점수만 오르고 일반화하지 않는
**benchmark overfitting**은, 바로 이 구조. 리더보드의 숫자를 너무 믿은 자가, 몇 번이나 발목을 잡혀 왔습니다.

##### 3.2 저 자신의 "현행범" — 자기 반증

여기서, §1에서 예고한 "혼동 현행범"을 해부대에 올립니다. 숨기지 않고 씁니다.

저는 처음에 TODO에 이렇게 썼습니다——"**재실행에서 오카 기요시·그로텐디크 계통이 살아남는가**를 검증한다".
그리고 PoC에서 monoculture **0.05**라는 깨끗한 숫자를 보고, "오, 계통 다양성도 개선된 게 아닌가?"라고
**한순간, 착각할 뻔했습니다**.

이것이 혼동입니다. 정본(lldarwin_stage1_results §3)에 쓴 대로, `poc_evolution_env.py`의 저자 코멘트
(제가 쓴 코멘트) 자신이, 그 혼동을 명확히 부정하고 있습니다.

> "monoculture = **BEHAVIORAL** concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is **behavioral spread**. lineage_fixation … to keep it <1 needs
> **QD niching on lineage / PERSONA-FX, not pure novelty**"

정리하면, 제가 혼동할 뻔했던 3개의 "다양성"은, 완전히 다른 것이었습니다.

1. **행동 다양성(behavioral diversity)** — genome 공간에서의 행동의 퍼짐. `diversity_l2`로 측정.
   **novelty가 효과가 있는 지표**. 0.05가 개선된 것은 이것.
2. **계통 다양성(lineage diversity)** — 어느 founder(오카 기요시·그로텐 등)가 살아남았는가. `founder_counts`.
   **novelty로는 구조적으로 개선되지 않는다**. novelty도 lexicase도 "기존 개체의 보존"밖에 못 하며,
   한 번 멸종한 계통을 부활시키는 기구를 갖지 않는다. 그래서 중립 부동(Kimura)으로 monoculture를 향하는 것은
   **이론적으로 정상**. 붕괴가 아니라, 상정 내.
3. **실 LLM 지능 다양성(real intelligence diversity)** — 실모델이 정말로 다양한 영리함을 갖는가.
   **proxy로는 일절 측정할 수 없다**. Stage2의 실 LLM 평가가 담당하는 영역.

즉 "0.05로 개선되었다"의 정체는 **(1) 행동 다양성뿐**. (2)도 (3)도, 그 숫자와는 무관했습니다.
제가 한순간 "계통도 개선되었나?"라고 생각할 뻔한 것은, **(1)을 보고 (2)/(3)도 좋아졌다고 속단했기** 때문입니다.

이것이야말로 Goodhart 법칙의, 설계자 측 버전입니다.
지표(행동 다양성 0.05)를 보고, 그것이 측정하지 않은 다른 능력(계통 생존·실지능)까지 좋아졌다고
**인간이 멋대로 해석해 버린다**. proxy가 진짜 능력과 괴리될 뿐 아니라, **proxy를 읽는 인간의 해석도 괴리된다**.
반증 회에서 이것을 드러내는 것은, 아픕니다. 하지만, 드러내지 않으면 honest disclosure가 아닙니다.

##### 3.3 "무엇을 측정한 0.05인가"를, 대비로 본다

말만으로는 전해지기 어려우므로, **"무엇을 측정했는가"를 2장의 SVG로 대비**합니다.

먼저, **행동 다양성은 정말로 개선되었습니다**(이것은 사실·과장 없음). 아래는 중립 저장고 OFF의 계통 지배 stream.
최종적으로 **furuse 71% / friston 29%의 2 계통으로 붕괴**해 있습니다. 행동이 다양해도, 계통은 이대로.

![reservoir OFF: 2 계통으로 붕괴](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_ko.svg)

그리고 아래가, **계통 측의 대책(중립 저장고 ON)을 넣은 후**. **전 8 계통이 병존**합니다
(millidge / von-neumann / oka-kiyoshi / grothendieck … 가 살아남는다).

![reservoir ON: 전 8 계통이 병존](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_ko.svg)

이 2장의 대비가, 이 글의 심장입니다.
**같은 "0.05의 행동 다양성"이라도, 왼쪽(OFF)은 계통이 붕괴하고, 오른쪽(ON)은 계통이 병존한다.**
즉 0.05라는 행동 다양성의 숫자는, **계통이 어떻게 되었는지를 일절 말하지 않았다**.
다른 기구(lineage-niched QD / 중립 저장고)를 더해, 비로소 계통이 구제되었습니다.

"무엇을 측정한 0.05인가"——답은 "**행동뿐**". 계통은 다른 렌즈로 보지 않으면 보이지 않았습니다. 이것이 정직한 답입니다.

##### 3.4 대책은 있지만, 문제는 사라지지 않는다

설계에는 Goodhart 대책을 짜 넣어 두었습니다.

- proxy는 **mechanism feasibility 검증에 한정**하고, production 능력을 주장하지 않는다.
- **실 LLM/VLM 평가(Stage 2)를 본질**로 한다.
- **neutral shadow 대조(Bedau)**로 겉보기의 개선을 의심한다(중립 변이만의 shadow 집단과 비교해,
  정말로 선택이 효과가 있는지 확인한다).
- **down-sampling**으로 매 세대 case를 교란 + **OOD 축**으로 과학습을 상쇄.

> 🍵 **휴식 포인트(90초)**: "대책이 있다면, 이제 문제없는 거 아닌가?"——아니오, 여기가 핵심.
> 대책은 **괴리를 늦출** 뿐이며, **proxy가 진짜 능력이 아니라는 사실은 사라지지 않습니다**.
> 감기약이 증상을 억누르지만, 바이러스 그 자체는 없애지 못하는 것과 같습니다. 그래서 "proxy로 LLM이 영리해졌다"고는
> **죽어도 말하지 않습니다**. 말하는 순간, 반년 후에 망신을 당하는 것이 보이니까요. 차를 한잔.

---

#### 4. 반증 3 — 설계자 의존성: "다양성의 방향"은 누가 정했는가?

##### 4.1 메타한 의심

ε-lexicase의 case, QD의 behavior 기술자, novelty의 거리 척도, minimal-criterion의 기준값——
이것들은 전부, **"다양성의 방향"을 설계자(저)가 정하고 있습니다**.

즉 lldarwin이 낳는 다양성은 "**설계자가 상정한 축 안에서의** 다양성"이며,
생물 진화급의 **미상정 창발(unanticipated emergence)**이 아닙니다.
Taylor et al. (2016)이 open-endedness의 한계로 지적하는 대로,
"인간이 정의한 척도 안에서 다양"한 것과 "정의의 밖으로 튀어나가는" 것은, 완전히 다른 이야기입니다.

예를 들어 제가 "행동 다양성"을 `diversity_l2`(genome 공간의 L2 거리)로 정의한 순간,
진화는 "**L2 거리가 커지는 방향**"으로 다양화합니다. 하지만 그것은 제가 그은 좌표축 위에서의 다양성이며,
제가 상상도 못 한 축(예를 들어 "유머 감각"이라든가 "침묵의 사용법"이라든가)에서의 다양성은,
**애초에 측정 대상에 들어 있지 않으므로**, 태어나도 알아차릴 수 없습니다.

> 🤔 **비유(금붕어 못)**:
> 금붕어 건지기 가게 주인이 "빨간 금붕어와 검은 금붕어, 둘 다 남도록 고르자"라고 정해서 건집니다.
> 확실히 빨강도 검정도 못에 남습니다. 다양성, 달성. …하지만, 그 못에 **초록 금붕어**가 돌연변이로 태어나도,
> 주인의 그물은 "빨강이냐 검정이냐"밖에 보지 않으므로, 초록은 **평가받지 못하고 건짐을 놓칩니다**.
> 설계자가 정한 축의 바깥쪽의 창발은, 처음부터 안중에 없습니다. 이것이 설계자 의존성입니다.

##### 4.2 수용 — 이길 수 있는 축을 한정한다

그럼 어떻게 할 것인가. **미상정 창발을 주장하지 않는다**,는 것이 정직한 답입니다.

lldarwin은 "**검증 가능성이 없는 다양성의 지도**"를 노리는 것이지(차별화 축 DIFF-1),
strong / unbounded open-endedness는 주장하지 않습니다(SCOPE와 정합).
"인류 미답의 창발을 하고 있습니다!"라고 하면 화려하지만, 그것은 거짓말이 됩니다.
**이길 수 있는 축을 한정한다**——인지 스타일·문화적 스타일 같은 "검증 가능성이 없는 다양성"을 지도화하는 것에
가치를 좁힙니다. 이것이 lldarwin이 성실하게 주장할 수 있는 범위입니다.

화려한 주장을 버리는 용기가, honest disclosure의 핵심이기도 합니다.

---

#### 5. 반증 4 — minimal-criterion과 QD 자체의 trade-off

도태기의 각 부품에도, 고유한 약점이 있습니다. 설계 문서 §7.1의 수용된 한계를 하나씩 해설합니다.

##### 5.1 minimal-criterion의 정체⇄붕괴

minimal-criterion(최저 기준 gate)은 "기준을 충족하지 않는 개체는 번식시키지 않는다"는 구조이지만,
**기준의 높이가 그대로 trade-off**가 됩니다.

- **기준이 낮다** → 거의 전원이 통과 → 선택압 제로 → **정체**(#25의 포화와 같은 구조).
- **기준이 높다** → 거의 아무도 통과하지 못함 → **전멸**(실증 있음. 전원이 gate에서 떨어지면 다음 세대를 만들 수 없다).

미지근한 물이냐 지옥이냐. **대책**: criterion을 고정값이 아니라 **집단 분위수로 적응**시킨다(예: 하위 30%를 떨어뜨린다).
나아가 전원 fail이면 gate를 무시하는 안전밸브를 넣는다(`MultiPressureSelector` 구현 완료).

##### 5.2 QD의 차원의 저주 + 아카이브 포화

QD(MAP-Elites)는 behavior 기술자로 cell을 자르지만, **기술자가 고차원이면 cell의 대부분이 빈다**
(차원의 저주). 또 장기간 돌리면 전 cell이 채워져, 새로움이 한계에 다다른다(**아카이브 포화**).
이것은 인공 생명의 고전 Avida / Tierra에서도 관측된 현상입니다.

**대책**: 기술자를 **저차원으로 축약**(DESC-1, JL 사영) + 포화를 **Bedau 통계로 감시**하고,
"**포화=실패**"로서 정직하게 기록한다(포화를 "이미 탐색을 다 했다는 증거"로 편의적으로 해석하지 않는다).

##### 5.3 lexicase의 스케일 한계

ε-lexicase는 case 수가 늘면 **계산 비용이 증대**하고, 게다가 **노이즈로 사실상 랜덤 선택화**합니다.
case가 너무 많으면, 우연히 순서의 맨 앞에 온 case로 승자가 정해져, 선택이 주사위에 가까워집니다.

**대책**: **down-sampled lexicase**(매 세대 case의 부분집합만 사용)로 비용 삭감 + 환경 교란.

##### 5.4 trade-off는 실측으로 "보인다"

이 trade-off들은 탁상공론이 아니라, **실측에서 나타납니다**.
중립 저장고의 "재투입 빈도(reinject_interval)"를 바꾼 sweep이 그 좋은 예입니다.

| interval | named 계통 생존 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**(매 세대) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84(최대)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**자명하지 않은 발견**: 행동 다양성(diversity_l2)은 interval을 올릴수록 단조 증가하지 않고, **interval=5에서 정점**을 찍습니다.
10/20은 오히려 저하합니다. 이유는——계통을 너무 방치하면(interval을 올리면),
저장고 유래의 다양성 주입이 줄고, 게다가 소수 계통이 고정되어 diversity도 늘지 않게 됩니다.
딱 좋은 "방치 정도"가 한가운데에 있다는, 비선형의 세계입니다.

![재투입 빈도 sweep: diversity는 interval=5에서 정점(비단조)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_ko.svg)

운용 지침은 이렇게 됩니다——**계통 유지를 최우선으로 한다면 interval=1(8/8 전 계통 생존)**,
**계통 유지와 행동 다양성을 양립시키고 싶다면 interval=5(5/8 유지하면서 diversity 최대)**.
최적점은 fitness / 집단 규모에 의존하므로, 본번에서는 재교정이 필요합니다.
"어느 하나의 정답"이 아니라 "목적에 따라 움직이는 최적점"이다,라는 것이 정직한 결론입니다.

##### 5.5 honest 유보 — "생존"은 "생명 유지"일지도 모른다

여기서, 하나 더 정직하게 써 두어야 할 유보가 있습니다.
중립 저장고가 전 8 계통을 살린 것은 사실이지만, **그 "생존"의 질을 의심할** 필요가 있습니다.

정본(§4.1 / §4.2)에 쓴 대로, 저장고는 "계통별 best-ever genome(frozen elite)을 재투입한다"는 기구입니다.
강한 계통은 실제로 자손을 늘려 번식하고 있습니다. 한편, 약한 계통(각 1개체)의 "생존"은,
**재투입 유래이며, 능동적인 진화가 아닙니다**. 말하자면, **번식이 아니라 생명 유지 장치**.

이것은 중립 저장고의 정의 그대로의 정당한 거동(대표를 유지하고, 재결합 가능하게 한다)입니다.
하지만 "전 8 계통이 **활발하게 계속 진화하고 있다**"고는 주장하지 않습니다.
"전멸은 막았다. 하지만 약한 계통은 ICU에서 연명 중"——이것이 정확한 표현입니다.

> 🤔 **비유(라쿠고풍)**:
> 집주인: "셋집의 거주자가 한 사람도 빠짐없이 8명 전원 갖춰져 있군요, 경사로다 경사로다."
> 핫쓰안: "예. 다만, 절반은 숨만 쉬고 집세도 안 내고 누워 있어서…"
> 집주인: "**그건 '살고 있다'기보다 '놓여 있다'겠지!**"
> 핫쓰안: "뭐, 내쫓는 것보단 낫지 싶어서…"
> ——전원 있다,는 사실. 전원이 활약하고 있다,는 거짓말. 이 경계선이 honest disclosure입니다.

---

#### 6. Stage2 — proxy에서 "실"로 가는 다리

반증만으로는, 설계가 앞으로 나아가지 않는 것처럼 보일지도 모릅니다.
하지만 반증으로 발판을 다졌기에, 다음 한 걸음에 의미가 생깁니다. 그것이 **Stage2: 실 LLM 평가**입니다.

##### 6.1 proxy 축(mechanism feasibility)

먼저 Stage2의 전반으로서, LLM이 서툰 5축을 **proxy(결정론 heuristic, LLM 비의존)**로 plugin화했습니다.

| pressure(LLM 약점) | 관련 사고 인자(case) |
|---|---|
| typo_robustness(노이즈 내성) | consistency / reality_link / uncertainty |
| polysemy_wsd(다의어) | multiview / consistency / reality_link |
| multistep_robustness(다단 추론) | structurize / closed_loop / self_extend |
| calibration(신뢰도 추정) | uncertainty / provenance |
| context_management(무관 문맥 내성) | consistency / provenance / recompose |

합계 14 case를 breakdown에 출력하고, lldarwin의 ε-lexicase가 **집약하지 않고 축마다 specialist를 도태**합니다.
아래가, 그 proxy 축의 모집단 평균 추이입니다.

![Stage2 proxy 축의 추이(mechanism feasibility)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_ko.svg)

다만——지금까지 누차 말한 대로——**이것은 proxy**.
개체는 실 LLM이 아니라 genome이므로, 이 pressure는 "genome이 그 약점에 관련된 사고 인자를
얼마나 갖추는가"의 **행동 대리**에 지나지 않습니다. **production의 LLM 능력은 측정하지 않습니다**(mechanism feasibility만).
SVG에도 "PROXY"라고 새겨 두었습니다. Goodhart 리스크는, 여기서는 수용된 한계로서 명시합니다.

##### 6.2 실 on-prem LLM 평가(proxy→real의 다리)

그리고 이 글에서 처음으로 보고할 수 있는 전진——**실 LLM 평가가 동작했습니다**.

localhost의 ollama(llama3.2:latest)가 도달 가능하다고 판명되었으므로, `real_pressures.py`로
**개체 → 실 LLM 사상**을 구현했습니다(Promptbreeder 계). 구조는 이렇습니다.

- 개체의 `c_prompt`(PromptChromosome)를 **system prompt**로 변환한다
  (skill_set → 지시문 / prompt_template_id → 추론 스타일 / language_style → 어조).
- 고정 LLM(llama3.2)에 그 system prompt를 씌우고, 5 서툰 축의 **실태스크**를 풀게 하여 채점.
- 즉 **LLM 본체는 고정하고, prompt 전략(genome)을 진화**시킨다.
  "어느 prompt 전략이 LLM의 약점을 완화하는가"를 **실측으로 도태**한다.

결과, **실선택 신호를 확인할 수 있었습니다**.
CoT + structure 전략(`chain_of_thought` + structurize + loop)이,
llama3.2의 **multistep을 0.0 → 1.0으로 개선**(terse한 전략은 0.0으로 실패, score 0.80→1.00).
proxy의 환상이 아니라, **실 LLM에서 "prompt 전략의 진화가 약점을 완화한다"는 것을 실증**할 수 있었습니다.

![Stage2 실 on-prem LLM 축의 추이(prompt 전략 진화)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_ko.svg)

proxy 축(앞서 제시)과 실 LLM 축(위)을 **나란히 보면**, "proxy로 측정한 형태"와 "실측의 형태"가
어떻게 다른지가 눈으로 보입니다. proxy는 기구가 도는 것을 보여줄 뿐. 실 LLM은, 실제로 모델의 약점에 대해
prompt 전략이 어떻게 효과를 내는지를 보여줍니다. **이 2장의 차이야말로, 이 글의 주장의 실물입니다.**

##### 6.3 하지만, 여기서도 정직하게

실 LLM에서 동작했다——하지만 여기서도 사이렌을 울립니다. 유보는 4개.

- **(a) c_prompt만 fitness에 관여** — persona / c_factors는 중립이며, fitness에는 얽혀 있지 않다.
  계통은 reservoir가 유지하고, 초기 선택은 novelty가 담당한다. 즉 이것은 "**prompt 전략의 진화**"이며
  "persona의 진화"가 아니다.
- **(b) 전 founder의 초기 c_prompt가 동일(default)** — 그래서 탐색은 mutation 구동.
  founder마다 prompt를 다양화하는 것은 향후의 개선점.
- **(c) 소규모 배터리(축당 2문)** — 노이지한 추정. "multistep이 0→1"도, 문제 수가 적으므로
  이것만으로 일반화를 주장할 수는 없다.
- **(d) on-prem only(측정 순도)** — localhost ollama 한정이며,
  **일반적인 LLM 능력의 주장이 아니다**([[feedback_llive_measurement_purity]]).

12h 연속 실행도 기동했습니다(`--fitness real-pressure --selection lldarwin --novelty
--lineage-reservoir --genome3d`). wallclock 12h에 safely 정지(snapshot 완료 → `--resume`로 계속 가능).
하지만 "12h 돌렸으니 진짜"라고는 말하지 않습니다. 돌렸다,는 사실. 본질을 다 측정했다,는 거짓말.
**proxy→real의 다리는 놓였다. 하지만 다 건너지는 못했다.**——이것이 Stage2의 정직한 상태입니다.

---

#### 7. 결론 — 어디까지 주장해도 되는가(경계선)

"LLM의 약점을 proxy fitness로 삼으면 진화로 극복할 수 있다"는 **낙관적**이었습니다.
반증으로 깎아낸 결과, lldarwin의 가치 주장을 다음 3점으로 **한정**합니다.

1. **(a) proxy는 mechanism feasibility만** — 진화의 배관이 도는 것의 검증. production 능력은 주장하지 않는다.
2. **(b) 실 LLM/VLM 평가가 본질** — 지능의 선택압은 개체 → 실모델 사상(Stage 2)이 담당한다.
   여기에 다리는 놓았다. 하지만 본격적으로 건너는 것은 이제부터.
3. **(c) 다양성의 지도화** — 이길 수 있는 축을 "검증 가능성이 없는 다양성(인지·문화 스타일)의 지도"로 한정한다.
   미상정 창발은 주장하지 않는다.

이것이 honest disclosure입니다. **실패(#25)도, 자신의 혼동(§3.2)도, 한계(#5/§6.3)도, 지우지 않고 남긴다.**
화려한 승리 선언을 하나도 쓰지 않은 이 글이야말로, 진화 아크에서 가장 성실한 회라고, 저는 생각합니다.
앞으로 나아갈 발판은, 이 경계선 위에만 있습니다.

---

#### 8. 교훈(영구 보존)

- **좋은 결과(0.05 개선)일수록 그 내역을 의심한다.** "proxy 행동 다양성"은 "계통 다양성"도 "실 LLM 지능 다양성"도 아니다.
  숫자를 보고 다른 능력까지 좋아졌다고 속단한 자신이, Goodhart의 살아 있는 표본이었다.
- **"측정"을 고치지 않고 "도태"만 고급스럽게 해도 헛수고.** 포화된 렌즈에는, 어떤 선택압도 효과가 없다.
  렌즈를 닦는 것이 먼저, 도태기를 얹는 것이 나중.
- **Goodhart의 법칙은 진화의 천적.** 지표를 목표로 한 순간, 진화는 그것을 hack한다.
  게다가 지표를 읽는 인간의 해석까지 함께 괴리된다.
- **설계자가 다양성의 방향을 정하는 이상, 미상정 창발은 주장하지 않는다.** 이길 수 있는 축을 한정하는 것이 성실함.
- **"생존"은 "생명 유지"일지도 모른다.** 전 8 계통이 남았다,는 사실. 전원이 활발하게 진화 중,은 거짓말.
  동사의 선택 하나에 honest disclosure가 깃든다.

> **다음 회 예고**: 반증으로 발판을 다졌다면, 다음은 Stage 2의 본격화(실 LLM/VLM 평가, on-prem ollama).
> proxy의 환상이 아니라, 실모델의 지능 다양성을 정말로 선택압으로 삼을 수 있는가.
> "multistep 0→1"을 소규모 배터리의 우연으로 끝내지 않고, 재현 가능한 선택 신호로 길러낼 수 있는가. 여기서부터가 본번입니다.

---

#### 9. 관련
- 연재 #25 "나와 프리스턴만 남았다" — 실패의 기록(이 글의 기점)
- 연재 #26 "lldarwin의 설계" — 도태기(이 글이 반증하는 대상)
- 구현 commit(llive): Stage1 = `8060204` / lineage-reservoir PoC = `0d0537d` /
  Stage1.5(EvolutionLoop 통합)= `b03cbda` / Stage2(실 LLM real-pressure)= `2fb2912`
- 실측 정본: `../../research/lldarwin_stage1_results_2026_05_26.md`(§3 honest disclosure / §4.1–4.5)
- 설계 정본: `../../vision/LLDARWIN_DESIGN.md` §7 / §7.1(반증 조사·수용된 한계)
- 관련 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_implementation_status_record]]
- 참고: Goodhart의 법칙 / La Cava 2019(ε-lexicase, arXiv 1905.13266)/ Taylor et al. 2016(open-endedness의 한계)/
  Bedau(neutral shadow)/ Kimura(중립 진화설)

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #25・#26 の Qiita URL cross-link -->
<!-- KEY MESSAGE: honest disclosure の本丸。飽和した眼鏡には選択圧が効かない + Goodhart + 設計者依存。主張を 3 点に限定。「何を測った 0.05 か」= 行動多様性のみ(≠系統≠実知能)を自己反証の核に。 -->
<!-- NOTE(事実整合): PoC デプロイで monoculture は実際 0.05 に改善した(誇張でない)。本記事はそれを否定せず「何を測った 0.05 か」を honest に深掘りする構成。「lldarwin を入れても改善せず」とは書かない(事実と異なるため)。novelty/reservoir はそれぞれ行動多様性 +109% / 系統 8/8 を実際に改善した。 -->
<!-- 埋込 SVG: stage1_baseline_status / reservoir_off_dominance / reservoir_on_dominance / reinject_sweep / stage2_proxy_axes / stage2_real_llm_axes (全て ../assets/lldarwin_2026_05_26/, 実在確認済 2026-05-26) + step_c/step_c_two_regimes / step_c/deceptive_corridor -->
<!-- 多言語: JA→EN→ZH→KO 全文縦積み・各言語自己完結 (SVG/表/参考文献を各言語に複製、alt は翻訳) -->

## 6. 進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで、人工進化はどう可視化されてきたか

### 진화를 「보여주는」 기술의 계보 #30 — Conway 의 라이프 게임에서 3DGS 까지

> **콘셉트 훅**: 제가 #25〜#27 에서 끊임없이 이야기하고 있는 「인공 진화」. 사실 이것은 반세기 이상의 역사를 가진 연구 분야입니다. 그리고 흥미로운 점은, **진화 연구는 늘 「보여주는 방식(시각화)」과 2인 3각으로 함께 진화해 왔다**는 것입니다. 1970 년의 흑백으로 깜빡이는 세포에서, 2024 년의 연속 유체·3D 가우시안까지. 「진화를 보여주는 기술」의 계보를 교양으로서 단숨에 더듬어 봅니다. 마지막에는 FullSense 의 진화 시각화(사고 인자 그래프 위의 계통수)가 이 계보의 **어디에 서 있는지**를 자리매김합니다.

---

#### 0. 왜 「시각화」가 진화 연구의 주역인가

진화는 **장시간·대집단·다세대** 의 현상입니다. 숫자의 나열만으로는 「무슨 일이 일어났는지」를 파악할 수 없습니다. 그래서 인공 진화의 역사는, 거의 그대로 **「진화를 한눈에 이해시키는 표현의 발명사」** 입니다.

> 🍵 **휴식 포인트**: 이 글은 수식 제로·코드 거의 제로의 「산책」 편입니다. 커피 한 잔과 함께 즐기세요. 각 시대의 「보여주는 방식의 돌파구」만 골라 갑니다.

---

#### 1. 1970: Conway 의 라이프 게임 —「단순한 규칙이 무늬를 낳는다」

- **무엇**: 2차원 셀룰러 오토마타. 생사 2상태 × 이웃 8셀의 단순한 규칙.
- **보여주는 방식의 발명**: **격자의 깜빡임 그 자체가 시각화**. 글라이더·블링커·글라이더 건 같은 「움직이는 무늬」에 이름이 붙은 것 = 인간이 **창발 패턴을 눈으로 이름 붙인** 가장 초기의 예.
- **한계**: 진화(자연선택)가 아니라 결정론적인 전개. 그러나 「단순한 규칙 → 복잡한 겉모습」의 충격이 이 분야를 열었다.

**이 절의 살 붙이기 예정**: 글라이더가 「이동하는 구조」로 인식된 것 = 시각화가 개념을 낳은 좋은 예로서 깊이 파고든다.

---

#### 2. 1991: Tierra（Tom Ray）—「코드가 생물이 된다」

- **무엇**: 가상 CPU 위에서 자기 복제하는 기계어 프로그램의 생태계. 기생체·면역·최적화가 **저절로 창발**.
- **보여주는 방식의 발명**: **메모리 맵의 시각화**. 각 프로그램이 차지하는 메모리 영역을 색으로 칠하고, 기생체가 숙주에 파고드는 모습을 「지도」로서 보여줬다. **「코드의 생태계」를 공간으로 그려냈다**.
- **의의**: 「자기 복제자의 자연선택」을 컴퓨터 안에서 처음으로 관측. open-ended evolution 연구의 출발점 중 하나.

---

#### 3. 1994: Avida（Adami / Ofria）—「진화를 측정한다」

- **무엇**: Tierra 의 계보를 잇는 디지털 생명 플랫폼. 논리 연산을 해내면 보상(CPU 시간)을 얻는다.
- **보여주는 방식의 발명**: **계통수(phylogeny)와 적응도 지형의 시각화**. 「어느 조상에서 어느 자손이 분기했는가」를 트리로 그리고, 복잡 형질(EQU 연산 등)이 단계적으로 진화하는 과정을 **추적 가능**하게 했다.
- **의의**: 「불가피한 단계를 거쳐 복잡성이 진화한다」를 실증했다(Lenski et al. 2003, Nature). **진화를 이야기가 아니라 측정 대상으로 만들었다**. FullSense 의 monoculture 모니터링(max_lineage_share / archive 성장)은 이 「측정하는 진화」의 직계다.

> 🤔 **비유(만담풍)**:
> 보케: 「Avida 는 진화를 숫자로 측정할 수 있게 했다.」
> 츳코미: 「즉 진화에 성적표를 매긴 거네.」
> 보케: 「맞아. #25 에서 내가 『만점 인플레로 성적표가 망가졌다』고 한 게, 바로 Avida 급 측정 이야기야.」

---

#### 4. 1994: Karl Sims「Evolved Virtual Creatures」—「진화를 영상으로 매료한다」

- **무엇**: 3D 물리 시뮬레이션 안에서, 형태(block 의 연결)와 신경 제어를 **동시에 진화**시켜, 헤엄치고·걷고·물건을 서로 차지하는 생물을 낳았다.
- **보여주는 방식의 발명**: **3D 애니메이션 영상**. 논문의 그림이 아니라 **동영상**으로 보여준 것이 충격을 불러일으켰다. 「진화가 설계한, 누구도 예상하지 못한 기묘한 걸음걸이」를 **인간이 직관적으로 재미있어할 수 있는** 형태로 만들었다.
- **의의**: 진화 시각화가 「연구자용 그래프」에서 「**누구나 보고 놀라는 영상**」으로. FullSense 의 데모 철학([[project_f25_demo_polish]] 「움직임으로 매료한다」)의 정신적 조상.

> 🍵 **휴식 포인트**: 여기까지 「흑백 점 → 메모리 지도 → 계통수 → 3D 동영상」으로, 보여주는 방식이 **추상 → 구상 → 동적** 으로 진화한 것이 보이면 OK. 후반은 현대 편입니다.

---

#### 5. 2019: Lenia（Bert Chan）—「연속적인 인공 생명」

- **무엇**: 라이프 게임을 **연속 공간·연속 시간·연속 상태** 로 일반화. 매끄럽게 움직이는 「생물 같은」 패턴(orbium 등)이 다수 발견되었다.
- **보여주는 방식의 발명**: **연속 필드의 매끄러운 렌더링**. 이산적인 깜빡임에서, 생물의 세포처럼 유연하게 움직이는 유체적 표현으로. 「인공 생명이 **아름답다**」라는 새로운 소구 축을 열었다.
- **의의**: 시각화의 질 그 자체가 연구의 발견력을 높인 예. 아름답게 보이기에 새로운 패턴을 인간이 알아챌 수 있다.

---

#### 6. 2020 년대: Quality-Diversity 의 시각화 —「다양성을 지도로 만든다」

- **무엇**: MAP-Elites / CMA-ME 등의 QD 알고리즘. 단일 best 가 아니라 **다양한 고성능 해의 집합**을 낳는다.
- **보여주는 방식의 발명**: **behavior space 의 히트맵**. 2축의 behavior 기술자를 격자에 두고, 각 cell 의 elite 를 색으로 칠한다 = 「**다양성 그 자체를 지도로서 시각화**」.
- **의의**: FullSense / lldarwin 의 QD archive 시각화는 여기에 직접 입각해 있다. 「1 cell 이라도 남으면 전멸하지 않는다」를 **지도의 공백 vs 충전**으로 한눈에 보여줄 수 있다(#26 에서 상술).

---

#### 7. 2020 년대〜: 3D Gaussian Splatting（3DGS）—「진화의 상태를 공간 표현한다」（FullSense 의 도박）

- **무엇**: 본래는 신규 시점 합성(NeRF 의 계보) 기술. 점군을 3D 가우시안으로 표현해 고속·고품질로 렌더링한다.
- **FullSense 의 착상**: 진화 집단의 **고차원 genome / pressure profile 을 3D 가우시안 공간에 사상**하여 「진화의 상태를 입체적으로 보여줄 수 없을까」라는 탐색([[project_precision_metrology_llm]] 의 SH 계수 연계와 같은 뿌리).
- **자리매김**: 이것은 **아직 연구적 도박**이며, 확립된 기술이 아니다(honest disclosure). 본 글 계보의 「최첨단의 가장자리」에 두는 실험이다.

---

#### 8. FullSense 의 진화 시각화는 어디에 서는가

| 시대 | 보여주는 방식의 핵심 | FullSense 에서의 계승 |
|---|---|---|
| Conway 1970 | 깜빡이는 셀 = 창발의 이름 붙이기 | （개념적 조상） |
| Tierra 1991 | 메모리 지도 | 계통 점유율의 지도화 |
| Avida 1994 | 계통수 + 측정 | monoculture 모니터링 / lineage tree |
| Karl Sims 1994 | 3D 동영상 | 「움직임으로 매료한다」데모 철학 |
| Lenia 2019 | 연속 필드의 아름다움 | animated SVG 표현층 |
| QD 2020 년대 | behavior 지도 | lldarwin QD archive 시각화 |
| 3DGS 2020 년대〜 | 3D 공간 표현 | （연구적 도박） |

FullSense 의 진화 시각화(**사고 인자 그래프 위의 계통수 + animated SVG**)는, **Avida 의 「측정하는 계통수」와 Karl Sims 의 「움직임으로 매료한다」와 QD 의 「다양성의 지도」를, 터미널 / 브라우저에서 재현하는** 위치에 있습니다. 반세기 계보의, 소박하지만 정통한 후예입니다.

> **다음 회 예고**: 계보를 더듬었으니, 다음은 구현. FullSense 의 계통수 animated SVG 가, 위의 어느 「보여주는 방식」을 어떻게 받아들였는지를, 실제 evolution.svg 를 소재로 해설합니다.

---

#### 9. 관련

- 연재 #25〜#27 — 본 글 진화 시각화의 「내용」（monoculture / lldarwin / 반증）
- 관련 memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- 참고: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

## 7. AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制と検証規律

### AI 에게 AI 를 부하로 부리게 하기 #31 —— Claude 주도 + Codex 배속의 「두 기둥」 개발 체제

> **콘셉트 후크**: FullSense（llmesh / llive / llove）는 나 혼자만의 개인 개발입니다. 하지만 실태는
> 「혼자」가 아닙니다. **AI 코딩 에이전트를 주로, 또 다른 AI 에이전트를 부하로** 둔
> 2 계층 개발 체제가 돌아가고 있습니다. 주는 **Claude Code**, 부하는 **Codex CLI**.
> 「AI 가 AI 에게 일을 맡기고, 그 성과를 AI 가 검증한다」——이 다중 위임을, 폭주시키지 않고
> 어떻게 규율하는가. 본 글은 인간 1 + AI 2 의 「두 기둥」 운용에 관한 실천기입니다.
>
> 키워드는 **오케스트레이터 / 배속 worker / 검증 규율 / 병렬화**.

---

#### 0. 세 줄 줄거리

- **Claude = 오케스트레이터**（계획·구현·위임·**검증**）/ **Codex = 배속 worker**（실행·리뷰·조사）.
- 「두 기둥」은 대등이 아니라 **Claude 주도 + Codex 배속**. 지휘 계통은 하나로 유지한다.
- 철칙: **외부 AI 의 finding 은 실제 코드 / 일차 정보로 한 건씩 검증한 뒤에 채용**（맹신 금지）.

---

#### 1. 왜 「두 기둥」인가 —— 동기

개인 개발에서 AI 에이전트를 하나만 쓰는 것은 이미 평범합니다. 그렇다면 왜 두 번째（Codex）를 **부하로서** 더했는가:

1. **벤더 분산·이중화** —— 단일 에이전트의 과금 변경 / 장애 / quota 고갈에 대한 헤지.
2. **크로스 리뷰** —— 같은 설계를 다른 계통의 AI 에게 보여 주고 세컨드 오피니언을 받는다（사각지대 감소）.
3. **병렬 worker** —— 독립 서브태스크를 부하에게 던지고, 주는 가장 중요한 태스크에 집중.

> 🍵 **휴식 포인트**: 「AI 를 둘 쓰면 = 두 배 똑똑하다」는 거짓입니다. 핵심은 **지휘 계통을 하나로 유지하는 것**.
> 오합지졸로 만들면 오히려 느려집니다. 본 글의 절반은 「어떻게 통제하는가」에 관한 이야기입니다.

---

#### 2. 역할 분담 —— 오케스트레이터와 배속 worker

![계층도: 인간 → Claude Code（주＝오케스트레이터）→ Claude 서브에이전트 병렬 / Codex CLI 배속 worker](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy_ko.svg)

- **Claude（주）의 책무**: 태스크 분해·의존성 판정·독립 태스크의 병렬 기동·진척 모니터링·**성과 검증**·일괄 커밋.
- **Codex（부하）의 책무**: 위임된 범위의 실행. 비대화형 위임 = `codex exec -s read-only "<prompt>"`.
- **지휘 계통은 항상 Claude.** Codex 는 Claude 를 경유해서만 전체에 영향을 준다（직접 커밋시키지 않는다）.

**이 절에서 살을 붙일 예정**: Claude 서브에이전트 병렬（[[feedback_parallel_first_execution]]）과 Codex 배속 위임의
구분 사용 표. 「같은 file 은 직렬·독립 file 은 병렬」「git 조작은 orchestrator 가 일괄」（[[feedback_agent_no_git_parallel]]）.

---

#### 3. 검증 규율 —— 「맹신 금지」가 체제의 생명선

두 기둥에서 가장 위험한 것은 **AI 의 출력을 AI 가 무검증으로 채용하는 것**입니다. 오류가 증폭됩니다. 그래서 철칙:

> 외부 AI（Codex / Copilot / Gemini）의 finding 은 **실제 코드 / 일차 정보로 한 건씩 검증**한 뒤에 채용한다.

실례: 본 연재 #26（lldarwin 설계）에서, 기존 코드 자산의 조사（`mating.py:139 LexicaseSelection` 은
「구현은 됐지만 미배선」 등）는 부하에게 조사시켰지만, **배선 지점과 행 번호는 주（Claude）가 실제 파일에서 확인**한 뒤에
설계서에 적었습니다. 「Codex 가 그렇게 말했다」를 설계의 근거로 삼지 않습니다.

> 🤔 **비유（만담 풍）**:
> 두목: 「어이, 그 함수, 배선됐냐?」
> 졸개: 「예, 미배선입죠.」
> 두목: 「……네 『예』는 못 믿겠다. 내가 직접 소스 보고 오마.」
> ——이것이 검증 규율. 졸개의 보고는 **기점**이지 **결론**이 아니다.

**이 절에서 살을 붙일 예정**: 검증의 3 단계（finding 수령 → 실제 코드 / 일차 정보로 확인 → 채용 또는 기각）와,
리뷰 래퍼（`tools/copilot_review.sh` 등의 읽기 전용 리뷰）의 위치 설정.

---

#### 4. 병렬화의 작법 —— 폭주시키지 않는 통제

여러 worker（Claude 서브에이전트 + Codex）를 동시에 돌릴 때의 규율:

- **2～4 병렬이 안전권**（주의 context 여유·커밋 충돌 없음）. 5+ 는 file 레벨 독립성을 엄격 관리.
- **독립 태스크 추출** = 의존 없음 + file / module / repo 레벨에서 비접촉. 같은 file 은 직렬（file lock 적）.
- **불가역 조작（삭제 / push / submodule 개변）은 한 건씩 인간 확인.** 부하에게 멋대로 시키지 않는다.
- **git 조작은 orchestrator 가 일괄.** 병렬 worker 에게 git 을 만지게 하지 않는다（충돌 회피）.

> 🍵 **휴식 포인트**: 「AI 를 많이 늘어놓으면 빠르다」의 함정. **주의 context（주의의 총량）가 율속(律速)입니다.**
> 5 체 병렬로 해도 주가 처리하지 못하면 의미가 없습니다. 뇌의 작업 기억과 마찬가지로, 동시에 파악할 수 있는 수에는 상한이 있습니다.

---

#### 5. 안티패턴（해서는 안 되는 것）

- 「하나씩 확인하면서 진행하겠습니다」라고 선언한 뒤 묵묵히 직렬 실행（병렬화의 기회 손실）.
- 부하에게 던지지 않고 주의 context 만으로 전부 해치운다（context 폭발）.
- 병렬 기동한 worker 의 결과를 기다리지 않고 주가 같은 file 을 만진다（충돌）.
- 2 worker 에게 같은 file 을 쓰게 하는 위임（독립성 판정 누락）.
- 부하 AI 의 finding 을 무검증으로 설계나 구현에 채용（오류 증폭 = 두 기둥 체제 최대의 사고）.

---

#### 6. 이 체제로 실제로 무엇이 돌았는가（FullSense 의 실례）

- **설계 크로스 리뷰**: 진화 설계 / 요건 / PoC 를 부하에게 리뷰시키고, 주가 실제 코드로 검증해 채용 판단.
- **기존 자산 조사**: lldarwin 의 기존 부품（loop.py / mating.py / nsga2.py 등）의 소재를 부하에게 조사 → 주가 확인.
- **병렬 서브태스크**: 기사 골자·코드 조사·요건 정리를 독립 태스크로서 병렬화（본 연재 자체가 그 산물）.

> 🍵 **휴식 포인트**: 「인간 1 + AI 2」로 개인 개발의 생산성이 어떻게 바뀌었는가, 라는 주관도 마지막에 정직하게.
> 빨라진 면（병렬·이중화）과 늘어난 부하（검증 비용·통제 비용）의 **양쪽**을 honest disclosure.

---

#### 7. 교훈

- **지휘 계통은 하나로 유지한다.** 두 기둥은 대등이 아니라 주종. 사령탑의 분열은 사고의 근원.
- **검증 규율이 체제의 생명선.** AI 가 AI 를 무검증으로 믿는 연쇄가 최대의 리스크.
- **병렬도는 주의 context 가 율속.** 체수가 아니라 처리할 수 있는 양으로 정한다.
- **불가역 조작과 git 은 인간 / orchestrator 가 쥔다.** 부하에게는 가역적인 일만 맡긴다.

> **다음 회 예고**: 두 기둥으로 돌린 진화 설계（#26 lldarwin）를, 배속 Codex + on-prem ollama 로
> Stage 2（실제 LLM 평가）까지 진행한다. 다중 AI 위임이 「연구의 구현 속도」를 어디까지 끌어올리는가.

---

#### 8. 관련
- 연재 #26 「lldarwin 의 설계」—— 본 체제로 돌린 실례.
- 관련 memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

## 8. llcore — Transformer のコアを CPU で進化させる: Verified Neural Architecture Evolution の最小 PoC battery

### (연재 #32) llcore CPU PoC battery 완성

#### TL;DR

- **Transformer의 코어 계산 (state update / 학습 규칙 / 인지 구동 Δ)** 을 진화 대상으로 삼는 연구 프레임워크 `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 독립 노선) 의 **CPU PoC battery 완성**
- **5개 PoC / 39개 falsifiable gate / 76개 테스트 / Codex pair-review 5/5 Green-light** 로 메커니즘 실증
- **Z3로 구조 변이를 online gate** = 진화 탐색의 selection pressure에 SMT를 끼워 넣음 — 사전 조사에서 발견되지 않은 선행 연구 (사전 조사 RAD 14개 분야 + Agent A-D 확인)
- 투고 후보: TMLR (본명) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

#### 왜 만들었나

LLM 가중치를 동결하는 것이 표준이지만, **코어 계산 알고리즘 자체는 수작업 설계로 고정**되어 있다. AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge 같은 architecture/algorithm 탐색은 진전되었지만:

1. **개인 compute로는 계산 리소스가 불가능** (TinyLlama 1.1B from scratch = $140k / 90일 / 16×A100)
2. **탐색 중 안전성 보장 없음** = 수치적으로 불안정한 architecture를 만들어 시간 낭비
3. **검증을 동반한 탐색은 정적 verification (Reluplex/Marabou/α,β-CROWN) 과 단절** — 진화 루프 내 SMT online gate 연구는 발견되지 않음

#### 확정 독자 축 (사전 조사에서 negation work 없음)

메커니즘 실증 완료 (4개 축):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **state update 규칙을 유전자화 RWKV-style** (Stage 0a v2)
3. **factor_hook (인지 상태 → SSM Δ)** (Stage 2a mock)
4. **자체 진화기 + verifier 기반** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / VNN-COMP 신규 카테고리 제안.

#### PoC 사다리 (5 stage / 39 gate 전부 PASS)

| PoC | 내용 | 키 수치 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 자체 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

#### v1의 실패에서 배운 것 (honest disclosure)

PoC 0a v1은 `decay*s + mix*x*tanh(gate_str*s)` 로 **state=0이 fixed point인 zero attractor** = G1-G5 형식적으로는 PASS이지만 정보 전달이 제로. Claude 단독으로 놓친 설계 문제를 **Codex (gpt-5.4) 와 gem-critic의 독립 verdict** 가 검출하여 RWKV-style로 v2 redesign 했다.

→ **5개 PoC 중 4건에서 Claude 단독으로는 놓친 설계 문제를 Codex pair-review가 검출**. 상호 리뷰가 구조 붕괴 방지에 작동한 실례.

#### 다음 선택지

a. Stage 3 kernel 다양화 (rwkv/mamba/hopfield/linear-attn 을 유전자화)  
b. Stage 4 학습 규칙 (FF/EP/PCN/Hebb) 을 gene화  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. PrediPrune+Quokka로 Z3 gate 고속화  
e. FlashEvolve로 3.5-5x wall-clock 고속화  
f. 논문화 (TMLR + GECCO 2027)

#### Honest 유보

- mock 중심, 실제 LLM/가중치 접속은 GPU/새 PC 대기
- 1 step scalar invariant의 over-approx proof 단계, 다차원·다 step은 post phase
- tanh 상계 근사는 보수적 (sound이지만 완전하지 않음)

---

**Tags**: 진화 계산 / 형식 검증 / Z3 / RWKV / state space model / CPU연구  
**관련**: 연재 #14-31 (llive lldarwin v0.B-E + 관측+governance + lleval)  
**Project**:  (PyPI llmesh-llcore 0.1.0a0)

## 9. llcore — 「進化で AI を設計するとき、選り分けて育てる工夫は本当に要るのか?」を 3 実験で詰めた話 (第三軸 ③ 決着 Step D)

### (연재 #33) 너무 깔끔한 결과는 승리가 아니라 경보 —— 제3축 ③ 을 proper power 로 결판낸 하루

#### TL;DR

- 질문은 **「AI 의 코어 계산을 진화로 탐색할 때, "골라내고 나누어 키우는 공정" (= 진화의 ③ 적자생존/분리 요소) 은 정말 필요한가?」**
- **합성한 "골짜기가 있는 (기만적) 지형" 에서는 ③ 가 압승** (과거 실험에서 Cliff δ=+1.0). ③ 는 메커니즘으로서 진짜다.
- **그러나 실물에 가까운 CPU proxy 지형을, 평가 노이즈를 물리적으로 0 까지 떨어뜨려 다시 측정했더니 "정말 매끄럽다 (단봉)" 였고, ③ 는 불필요로 확정됐다.** "과거의 negative 는 검출력 부족 (underpower) 이 아니라, 지형이 정말로 매끄러웠다" 가 처음으로 뒷받침됐다.
- 실 multitask 근방 (C-gen4b) 에서만 "③ NOT null" 의 약한 기미가 나왔지만, 데이터를 늘리니 흔들려서 **후보에 그쳤다** (주행 내 드리프트 + 다중 비교에서 취약).
- "어떤 후처리가 ③ 를 숨기고 있다" 는 의심 (K4 ridge clip) 은, 떼어내니 오히려 악화 → **숨기고 있지 않다, 진단적 소견으로 강등.**
- 외부 리뷰 (Codex) 는 **블로커 없이** 결론을 추인했다.
- 결론을 한 줄로: **「③ 가 살아나는 건 지형이 기만적일 때뿐. 지금 CPU 로 측정할 수 있었던 실물 비슷한 것은, 우연히 매끄러웠다.」** 본진의 결판은 GPU (실 LLM 지형) 가 필요하지만, 그건 투자 판단이다.
- **추기 (2026-06-02, §11.5): 마지막 CPU 샛길 kernel 다양화 (BG9) 는 구조적으로 닫혔다.** kernel 선택은 저차원이라 강한 baseline (RR) 이 직접 샘플링하고, ③ 의 niching 우위가 원리적으로 나오지 않는다. **③ 가 효과를 내려면 "고차원의" 기만 지형이 필요하다**는 것을 알게 됐고, 남은 길은 GPU full-LLM 뿐 (그것도 베팅).
- 메타 교훈: **정직함 (honest disclosure) 은 장식이 아니라, 연구를 앞으로 나아가게 하는 도구였다.** BG9 에서는 "negative 를 올바르게 negative 로 확정한다" 는 방향에서도 같은 규율이 작동했다.

> ⚠ 이 글의 수치는 모두 로컬 (수중) 의 연구 commit `THIRD_AXIS_SETTLE_VERDICT.md` 에 연결된 실측이다. llcore 는 아직 공개 리포지토리를 만들지 않았으므로 외부 링크를 걸 수 없다. 대신 "어떻게 측정했는가" 를 본문에 전부 쓴다.

---

#### 0. 이 글은 무엇에 관한 이야기인가 (콘셉트)

`llcore` 는 "Transformer 의 코어 계산 (상태 갱신 규칙·학습 규칙·인지 구동 Δ) 을 유전자로 삼아, Z3 로 망가지지 않게 검증하면서 진화시키는" CPU 완결의 연구 프레임워크다 (연재 #32 에서 PoC battery 이야기를 썼다).

그 진화 엔진에는, 진화의 4 요소 중 **③ (적자생존 selection / 분리 separation)** 를 어떻게 작동시킬지라는 설계상의 급소가 있다. 다양성을 유지하며 니치에 남기는 MAP-Elites 같은 "골라내고 나누어 키우는" 구조다.

질문은 단순하다.

> **그 ③, 정말 필요한가?**

필요하다면, ③ 를 얹기 위한 무거운 투자 (최종적으로는 GPU 에서 실 LLM 을 돌리는 것) 에 의미가 있다. 필요 없다면, ③ 에 집착하는 것은 시간과 전기의 낭비가 된다.

이 하루 (2026-06-02) 동안, 그 질문에 **3 가지 실험으로 정면으로 결판을 내러 갔다.** 제목 그대로, 결론은 "너무 깔끔한 결과는 경보" 라는 FullSense 의 통주저음으로 다시 한 번 끌려 돌아오는 이야기다.

— 여기까지 30 초. 준비 운동 끝. 본론으로. —

---

#### 1. 비유: 등산과, 속임수 지형

수식 앞에, 지형 비유로 전체상을 잡는다 (이 연구에서 일관되게 쓰는 메타포다).

설계의 좋고 나쁨을 **지형의 높이** 로 나타낸다. **높은 곳 = 좋은 설계.** 가장 높은 정상을 찾는 게임이다.

**지형 1: 매끄러운 한 개의 산 (쉬움)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

이런 지형에서는, 소박한 "등산법 (hill-climbing)", 즉 "지금보다 조금 나은 쪽으로 움직일 뿐" 으로 충분히 정상에 도달한다. **공들인 공정 (③) 은 필요 없다.**

**지형 2: 속임수 지형 (기만적 deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

여기서는 소박한 등산법은 가짜 정상에서 멈춘다. 골짜기를 내려갈 용기가 없기 때문이다.

이때 작동하는 것이 ③ 의 발상이다. **여러 타입의 등산자를 골짜기 여기저기에 남겨 둔다** (= 기억의 궁전 / MAP-Elites archive). 누군가가 골짜기를 "징검다리" 로 건너 진짜 정상에 도달할 수 있다, 는 구조다.

**이 연구의 핵심을 한마디로**: ③ 가 정말 도움이 되는 것은 **"속임수 지형" 일 때뿐.** 매끄러운 한 개의 산에서는, ③ 는 쓸모없는 짐이다.

그래서 질문은 이렇게 바꿔 말할 수 있다:

> **「진화로 AI 를 설계할 때, 실제로 마주치는 지형은 "속임수 지형" 인가, 아니면 "매끄러운 한 개의 산" 인가?」**

이것이 정해지면, ③ 가 필요한지 아닌지가 정해진다. 오늘은 이것을 측정했다.

---

#### 2. 과거에 남은 숙제 ——"③ 불필요" 는 정말 "불필요" 였는가

지금까지의 실험 (Step C → 사다리 단 1 → E-A → 골짜기 깊이 실측) 을 통해, 그림은 대략 이러했다.

- **합성한 기만 corridor 에서는 ③ 가 압승** (3 개 baseline 모두에 이기고, Cliff δ=+1.0). ③ 는 존재 증명 완료, 메커니즘으로서 진짜다.
- **실문제에 가까운 proxy 지형에서는 ③ negative** (MAP-Elites 가 random 과 비길 뿐 = 매끄러운 지형과 같은 증상).

그런데, 여기에 2 개의 미해결 응어리가 남아 있었다.

1. **"③ 불필요" 는 정말 "지형이 매끄러워서" 인가, 아니면 단지 "샘플 수가 부족해 차이를 검출하지 못했을 (underpower)" 뿐인가?** ── 이것을 착각하면, "③ 는 무력" 이라는 과잉 일반화를 저지른다.
2. 골짜기 깊이의 직접 측정은 지난번 **N/A (측정 불능)** 으로 끝났다. 평가 노이즈가 골짜기 깊이보다 커서, 골짜기가 있어도 묻혀 보이지 않는다, 는 계기의 한계.

즉 "매끄럽게 보였던" 것이 **지형의 성질** 인지 **계기의 한계** 인지, 결판이 나지 않았다. 이 점을 따지는 것이 Step D 다.

— 잠깐 쉼. 여기까지가 전제. 여기서부터가 오늘 한 3 실험. —

---

#### 3. 실험 설계 —— 3 종 세트

| 실험 | 무엇을 측정하는가 | 노림수 |
|---|---|---|
| **EXP1** | proper-n 재검정 | 샘플 수를 진지하게 늘려, ③ 의 효과가 진짜인지 검출력으로 따짐 |
| **EXP2** | 결정론 C1 다봉성 | 평가 노이즈를 물리적으로 0 으로 만들어, 지형이 "속임수 지형" 인지 "매끄러운 한 개의 산" 인지 noise-free 로 판정 |
| **EXP3** | K4 ridge clip 의 verdict-flip | "어떤 후처리가 ③ 를 숨기고 있다" 는 의심을 검증 |

규율: 전부 `research/step_d_settle/` 에 격리, src 는 무개변, git 은 오케스트레이터가 일괄. 각 실험은 붕괴 게이트 (G1 CPU 완주 / G2 재현성 / G3 진단기 타당 / G4 src 불변) 를 통과시킨다.

---

#### 4. EXP2 가 결정타였다 —— 평가 노이즈를 0 으로 하면 지형이 보인다

순서는 앞뒤가 바뀌지만, **가장 효과적이었던 것은 EXP2** 이므로 먼저 쓴다.

지난번 골짜기 깊이 측정이 N/A 가 된 원인은 단순하다. **"골짜기 깊이 (0.05·|fitness| 정도) ≪ 평가 노이즈의 흔들림"** 이었기 때문이다. 계기의 노이즈에 골짜기가 묻혀, 있는지 없는지 알 수 없다.

EXP2 의 트릭은 이렇다.

> ESN reservoir (고정 seed) + ridge readout 의 closed-form (`np.linalg.solve`) 은, **난수를 일절 뽑지 않는다.** 그래서 평가 노이즈를 머신 엡실론 (약 1.11e-16) 까지 물리적으로 0 으로 만들 수 있다.

실측으로 `eval_noise_std ≤ 1.11e-16` 을 확인했다. 이것은 "평가할 때마다 값이 흔들린다" 가 아니라, 부동소수점의 최소 단위 (ULP) 에서 유래하는 오차로, **실질 0** 이다. 노이즈의 안개가 완전히 갠 상태에서, 지형의 골짜기를 직접 측정할 수 있다.

결과가 이것이다 (valley_fraction = 골짜기의 비율, 클수록 다봉 = 속임수 지형):

| landscape | 종별 | 차원 | valley_fraction (mean/max) | 다봉? | 판정 |
|---|---|---|---|---|---|
| **ESN_3param** (실 proxy) | real | 3 | **0.000 / 0.000** | **False** (3 seed 일치) | 매끄러움=단봉 → ③ 불필요를 noise-free 로 확정 |
| **ESN_perneuron40** (실 proxy) | real | 40 | **0.096 / 0.121** | **False** (3 seed 일치) | 매끄러움 쪽 (바닥 0.2 미만) → ③ 불필요 |
| ctrl_multipeak_dim3 (정 control) | control | 3 | 0.701 / 0.727 | True | 진단기는 다봉을 검출할 수 있다 ✓ |
| ctrl_multipeak_dim40 (정 control) | control | 40 | 0.795 / 0.818 | True | 진단기 건전 ✓ |
| ctrl_quadratic_dim3 (부 control) | control | 3 | 0.000 | False | 진단기는 매끄러움을 검출할 수 있다 ✓ |
| ctrl_quadratic_dim40 (부 control) | control | 40 | 0.000 | False | 진단기 건전 ✓ |

포인트는 3 개:

1. **실 proxy 지형 (3 차원 / 40 차원 모두) 은 valley≈0 = 단봉.** 3 seed 에서 완전 일치.
2. **진단기 자체는 건전.** 일부러 만든 다봉의 정 control 은 제대로 다봉 (0.70/0.80) 으로 검출하고, 이차함수의 부 control 은 제대로 매끄러움 (0.0) 으로 검출한다. 그래서 "실 proxy 가 단봉" 은 계기의 버그가 아니라 지형의 성질이다.
3. 이로써 **"과거의 ③ negative 는 underpower 가 아니라, 지형이 정말로 매끄러웠기 때문"** 이, 실 substrate 위에서 처음으로 noise-free 로 뒷받침됐다.

부차적 발견도 정직하게 써 둔다. **정 control 로 쓸 작정이었던 기만 corridor (`make_corridor_eval(d=0.16)`) 가, 결정론화하니 valley=0.0 (단봉 판정)** 이 되어 버렸다. corridor 의 기만성은 "단일 basin 안에 가두어 ③ 의 behavioral niching 으로 탈출시키는" 형 (behavioral-reach 기만) 이지, **지형의 골짜기 (C1 multi-basin) 의 기만이 아니었다.** corridor 는 C1 의 정 control 이 되지 않는다, 는 scope 의 좁아짐을 실측으로 확정했다. 이것은 과거의 골짜기 깊이 교정이 "corridor 유래의 임계값" 을 지형 다봉성으로 전송할 수 없음을 의미한다.

— 여기서 한숨 돌림. "정 control 이 control 이 되지 못했다" 는 건 은근히 충격이었다. 하지만 이것도 측정해 보지 않으면 알 수 없었다. —

---

#### 5. EXP1 —— 실 multitask 근방에서만 "③ NOT null" 의 약한 기미

다음으로, 실문제에 가장 가까운 띠 (C-gen4b = MAP-Elites vs random, 실 multitask 근방) 를, 샘플 수를 진지하게 늘려 재검정했다.

| case | 원 n=15 (감사) | fresh 진 재주행 | 판정 |
|---|---|---|---|
| **C-gen4b** | diff +0.063 / psd +0.20 / p 0.126 | **n=64: diff +0.0472, 단측 p 0.038, psd +0.188, gate PASS** | **③ load-bearing 후보 (still_inconclusive)** |

fresh seed 로 n=64 까지 돌렸더니 **strict gate 를 4 조건 전부 PASS** 했다. 즉 감사가 "③ 불필요 (inconclusive)" 라고 읽은 것은 방향으로는 틀렸고, **C-gen4b 에서는 ③ 는 NOT null 의 방향.**

…그리고 여기서 이겼다고 들뜨지 않는 것이 이번의 핵심이다. 3 가지 이유로 **후보에 그치게** 했다.

1. **갱신 후의 검출력 power@n64 = 0.517 < 0.80.** gate 는 통과했지만, 확증의 기준 (검출력 0.80) 에는 못 미친다.
2. **주행 내 드리프트 (이것이 효과적이었다).** 누적 p 값의 궤적을 따라가면: n=40 에서 첫 PASS (p=0.042) → n=60 에서 p=0.010 으로 깊게 유의화 → **n=64 에서 p=0.038 로 0.05 경계 근처로 되돌아왔다.** 더욱이 seed 를 전반/후반으로 나누면, **전반 32 seed 는 diff=+0.0755 (frac_pos=0.625) 지만, 후반 32 seed 는 diff=+0.0189, 마지막 9 seed 는 diff=−0.0376 (음).** PASS 는 전반 seed 에 떠받쳐져 있고, **새로운 데이터일수록 역방향으로 달리고 있다.**
3. **다중 비교.** p=0.038 은 α=0.05 에서는 PASS 지만, EXP1 의 3 case 만으로도 Bonferroni α=0.0167 을 초과 (FAIL). ③ research family 전체로 보면 더 엄격하다.

게다가, 효과량의 바닥 (psd) 이 **구조적 천장** 에 부딪쳐 있었다. C-gen4b 의 median psd 는 n=15→0.200, n=255→0.200 으로 꿈쩍하지 않는다. `P(|psd|≥0.147)` (효과량 조건의 충족률) 는 n=255 에서도 0.794 로 정점을 친다. 중효과 (psd≈0.20) 이므로, 샘플을 아무리 늘려도 full gate 의 검출력이 0.80 을 넘지 않는다. **즉 "샘플을 늘리면 (A) 확정된다" 는 전망 자체가, 이 proxy 위에서는 희박하다.**

결론: **C-gen4b 는 "③ load-bearing 후보 / still_inconclusive".** "③ NOT null" 이라는 headline 은, 단발의 경계 p=0.038 에 너무 기대고 있다. 주행 내 드리프트는 "후보가 위양성일지도 모른다" 는 진짜 증거다.

---

#### 6. EXP3 ——"후처리가 ③ 를 숨기고 있다" 는 의심은, 떼어내니 오히려 악화됐다

마지막 의심은 이러했다. "ridge readout 의 clip (K4) 이라는 후처리가, 실은 ③ 의 신호를 짓누르고 있는 것 아닌가?" 만약 그렇다면, clip 을 떼어내면 ③ 가 떠오를 터다.

떼어내 봤다.

| task | clip | MAP-E mean | baseline 승수 | verdict_flip |
|---|---|---|---|---|
| **addition** | True | +0.0100 | 1/3 | — |
| **addition** | False | **−1.212** | 0/3 (전부 악화) | **False** |
| **flip_flop** | True | +0.426 | 0/3 | — |
| **flip_flop** | False | +0.438 | 0/3 | **False** |

clip 을 떼어내니, ③ 가 떠오르기는커녕 **addition 에서 MAP-Elites 가 +0.010 → −1.212 로 열화.** clip=False 는 raw R²<0 의 노이즈 영역 (15/15 seed 가 음, R² 가 [−3.68, −0.20]) 에 MAP-Elites 를 떨어뜨려, 구조를 회복하기는커녕 악화시켰다. **= "clip 이 신호를 숨기고 있다" 는 가설을 능동적으로 반증.**

null-ridge FPR (gene 비의존 target = 진정한 귀무가설) 도 clip True/False 에서 차이 0 (양쪽 0.0).

판정: **K4 는 "유일한 능동적 suppression 기제" 가 아니라, "spread 를 짓누르지만 verdict 를 바꾸지 않는 진단적 소견" 으로 강등.** 이로써 과거의 통계 감사가 단정했던 "K4 = 유일한 능동적 suppression" 은 과대했음이 판명됐다.

정직한 유보 (§6.3 상당): null-FPR=0/0 은 null_seeds=4 만의 바닥값이고, 이 실험은 예산을 약 7 배 축소하고 있다. 그래서 verdict 의 라벨은 "null 확정" 이 아니라 **"not_load_bearing_at_this_budget (이 예산에서는 비載荷)"** 로 통일했다. "null 을 확정했다" 보다 "이 예산에서는 K4 가 load-bearing 이 아니다" 가 정확하기 때문이다. 판정의 실체 (진단적 소견으로의 강등) 는 불변이고, 어휘의 정밀도만 올리고 있다.

— 여기서 심호흡. 3 실험 끝. 다음은 "지나치게 말하지 않았는가" 의 자기 점검. —

---

#### 7. Surviving refutation —— 3 개의 렌즈로 자신의 결론을 때려 봤다

honest disclosure 의 핵은 "자신의 결론을 가장 매섭게 의심한다" 는 것이므로, 3 개의 독립된 반증 렌즈를 댔다. **3 개 모두 `refuted=true / medium` 으로 살아남았다**, 즉 보수적인 verdict 는 뒤집히지 않지만, positive 쪽의 강조는 약화시키는 방향으로 효과를 냈다.

1. **[power_adequacy] C-gen4b 의 gate PASS 는 optional-stopping + 다중 비교에서 취약.** 위 §5 의 드리프트와 Bonferroni FAIL 이 이것. "③ NOT null" 을 headline 으로 하는 것은 경계 p 에 너무 기댄다. → p 의 n 궤적과 후반 seed 의 부호 반전을 공개 필드에 기록 완료.
2. **[determinism_and_circularity] 단봉 verdict 는 임계값 근접에서 취약.** 결정론화와 비순환성 그 자체는 clean (behavior 와 fitness 의 상관은 ≈0, 진단기는 behavior 기술자를 쓰지 않고 지형 기하를 직접 본다). 다만 ESN_3param 의 midpoint 의 **90.9% 가 하방으로 dip** 하고 있어, 최대 상대 dip=0.0435 는 C1 골짜기 임계 0.05 의 바로 아래 (13% 이내). 그래서 정밀하게 말하면 "**진정으로 단봉**" 이 아니라 "**C1 임계값을 약간 밑도는 얕은 골짜기 (~2–4%) 를 가진 약 multi-basin**". (B) null 의 방향은 유지되지만, 견고성은 임계값 근접 때문에 한정적이다.
3. **[clip_flip_validity] K4 강등은 저예산 때문에 "at this budget" 한정.** verdict_flip=False 는 확실하지만, FPR 0/0 은 바닥값, 예산은 7 배 축소. 그래서 "firm refutation" 보다 "not load-bearing at this budget" 이라 서술해야 한다.

3 개 모두 "결론을 뒤집을" 정도는 아니지만, "지나친 말을 깎는" 방향으로 전부 효과를 냈다. 이 자기 감사야말로 오늘 성과의 절반이다.

---

#### 8. 자신이 밟은 실수를 하나 정직하게 쓴다

지난번 골짜기 깊이 workflow 에서, 2 단째 오케스트레이터 briefing 에 **stale (오래된) 값** 을 넘겨 버렸다. "전부 below threshold / d*=0.1234" 같은 값이다. 그런데 실제로 commit 된 결과 JSON 은 `all_below_threshold=false` 였다. 지난번 workflow 결과를 읽을 때, 다른 메트릭의 값을 착각했던 것이다.

**적대 검증이 이것을 검출해, verdict 를 N/A 로 강등했다.** 즉 "너무 깔끔한 결론" 을 스스로 의심하는 프로세스가, 자신의 복사·붙여넣기 실수를 붙잡았다. 기분 좋은 이야기는 아니지만, 이것이 돌아갔기에 오늘의 Step D 에서 올바른 발판에서 다시 측정할 수 있었다.

honest disclosure 는 "실패를 지우지 않는다" 뿐 아니라, "**실패를 검출하는 구조를 미리 놓아 둔다**" 는 것이구나, 하고 새삼 생각했다.

---

#### 9. 과거 verdict 를 어떻게 갱신했는가

| 과거 verdict | 과거의 읽기 | Step D 의 갱신 |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **방향 갱신: ③ 는 NOT null 의 방향 (fresh n=64 에서 gate PASS).** 다만 후보에 그침 |
| step6 exp7 (실 ESN proxy, ③ negative) | n≤10 맹점역, "재측정 필수" | **대폭 갱신: 지형이 정말로 매끄러움 (③ 불필요) 을 noise-free 로 확정.** 재측정해도 다봉은 나오지 않음 |
| 골짜기 깊이 N/A (계측 불능) | instrument 불능 | **해소: 결정론화로 계측 가능화** → vf≈0 (단봉). 다만 임계값 근접의 얕은 골짜기가 유보 |
| K4 clip = 유일한 능동적 suppression | "clip 이 landscape 구조를 은폐" | **강등: 진단적 소견** (not_load_bearing_at_this_budget) |

"③ 불필요로 보였던 과거 negative 의 다수는 underpower 가 아니라, 지형이 정말로 매끄러웠다" ── 이 한 점이, 실 substrate 위에서 처음 확인된 것이 오늘의 핵심이다.

---

#### 10. 외부 리뷰 (Codex) 는 블로커 없이 추인

llcore 의 규율로서, 각 capstone 은 Codex (gpt-5.4, read-only) 의 페어 리뷰를 통과시킨다. 이번 총평은 **"블로커 없음 ── ③ 결론을 외부 확인".**

- C-gen4b 를 load_bearing 이 아니라 후보에 그치게 한 판단은 타당 (갱신 검출력 0.5174 < 0.80 을 JSON 에서 확인).
- EXP2 의 결정론·비순환은 clean. "진정으로 단봉" 보다 "임계값 아래의 약 multi-basin" 이 정밀하다, 는 본문의 자인도 추인.
- EXP3 의 K4 강등은 현 예산이라면 타당 (FPR 0/0 + 7 배 축소 때문에 at-this-budget 한정).

지적된 4 건 (CF1～CF4) 은 **전부 장래 rerun 시의 harness 견고성과 문언 정밀도** 이며, 현 결론을 뒤집는 것이 아니다. GPU 에서 ③ 를 재검정할 때, 이것들을 적용한 뒤 harness 를 재이용한다.

---

#### 11. CPU 의 샛길 (kernel 다양화 / BG9) 을 시도하고 있었다

"③ 의 본진은 GPU (실 LLM 의 손실 지형) 로" 가 EXP2 의 권장이다. 실 proxy 가 매끄럽다고 확정된 이상, 매끄러운 지형에서 ③ 를 쫓아도 (A) 는 나오지 않는다 (지형이 한 개의 산이면 골라내기에 이득이 없는 것은 당연).

다만 GPU 는 투자 판단이므로, **CPU 에서 전진할 수 있는 다른 가설** 을 병행해 시도하고 있었다. 그것이 **kernel 다양화** 다.

가설은 이렇다. 개개의 kernel (rwkv / mamba / hopfield / linear_attn) 이 매끄러워도, **4 종류의 kernel 족을 union 하면, kernel 전환의 순간에 fitness 가 불연속적으로 단차를 만든다 → 지형이 multi-basin (속임수 지형) 이 될 수 있다 → ③ 가 GPU 없이 CPU 위에서 load-bearing 이 될 수 있다.** 이것을 검증하는 것이 BG9 였다.

이 글을 처음 썼던 시점에서는 "지금 BG6 (task → best-kernel 사상이 비정수인가, 즉 '태스크마다 잘하는 kernel 이 다른가') 을 smoke 측정하고 있는 중" 이었다. 그 후 (같은 2026-06-02 안에) BG9 의 결판이 났다. 다음 추기절이 그 결말이다.

---

#### 11.5. 추기 (2026-06-02): BG9 결판 —— 샛길은 구조적으로 닫혀 있었다

> 결론을 한 줄로: **BG9 = N/A (구조적). 즉 kernel 다양화라는 CPU 샛길은 "③ 가 서지 않는 것이 구조적으로 정해져 있" 으므로 닫혔다.** "③ 가 필요 없다" 가 아니라 "이 공간에서는 ③ 가 강한 baseline 과 원리적으로 분리될 수 없다" 는, 정보량 있는 negative 다.

§11 에서 깔아 둔 샛길의 결과가 나왔다. 기대했던 "kernel union 으로 multi-basin (속임수 지형) 이 생겨 ③ 가 CPU 에서 선다" 는 **일어나지 않았다.** 게다가 "우연히 서지 못했다" 가 아니라 **구조적으로 설 수 없다** 는 것을 알게 됐다. BG9 는 이것을 3 단의 증거로 확정하고 있다.

##### (1) substrate validity ——"변별은 있지만 약하다" (PASS 지만 요주의)

먼저 "태스크마다 잘하는 kernel 이 다른가" (BG6) 를, kernel-favoring task 군을 제1원리로 다시 설계해 측정했더니, 사상은 **비정수 = 비 inert (PASS).** mamba / linear_attn / rwkv 는 각각 다른 태스크에서 best 가 됐다. BG6 에서 밟은 "memory_tasks 는 kernel 중립" 의 전철을 피할 수 있었다, 는 의미에서는 전진이다.

다만 정직하게 말하면 **약하다**:

- **hopfield 는 어느 태스크에서도 이기지 못했다.** 이것은 hopfield kernel 이 **대각 스칼라 mock** 이라, tanh 어트랙터가 기능 불능이었기 때문 (per-seed 의 R² 가 0/0.99/0 으로 양극화). 즉 실질 "4 kernel union" 이 아니라 **3 kernel** 이다.
- clean 한 전문화는 2 축뿐 (selective_copy↔mamba / weighted_accum↔linear_attn). 나머지는 margin 이 얇고 fragile.

→ **변별의 존재 ≠ 다봉/장벽.** non-inert 화에는 성공했지만, 그것이 기만 지형 (속임수 지형) 을 보증하는 것은 아니다, 는 데까지. 또한 대각 mock 의 한계는 kernels.py 의 scope 선언대로이며, 여기서는 **기제의 feasibility 만 주장** (full kernel 성능은 비주장) 이다.

##### (2) harness validity —— positive control 이 validate 하지 않는다 (이것이 결정타)

다음이 본진이다. 고정 파라미터 (behavior=(kernel_id, theta L1)) 로 MAP-Elites (③) 를, 3 개의 baseline ── **RR-hillclimb (random restart 등산)** / panmictic-GA / random ── 과 honest 하게 paired 비교했다.

| 기질 | 결과 |
|---|---|
| **positive control** (합성 kernel-barrier) | ③ 는 panmictic (+0.423) 과 random (+0.208) 은 격파. **하지만 RR 에게는 이기지 못한다** (+0.051, p=0.31 → FAIL). 3 baseline 전승에 못 미침 = **harness validity 가 서지 않는다** |
| **negative control** (kernel 중립 태스크) | 전 method R²≈1.0 포화, ③ 우위 없음 = **올바르게 null** (위양성 없음, 계기는 건전) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3, panmictic 이 오히려 ③ 를 능가 = **③ 이기지 못함** |

여기가 Step D (기술판 §4-7) 와 결정적으로 다른 점이다. Step D 의 기만 corridor 에서는 ③ 가 RR 을 배제할 수 있었다. **왜 kernel 공간에서는 못 하는가?** 근본 원인은 하나:

> **RR 은 restart 할 때마다 kernel_id ∈ [0,4) 를 직접 샘플링할 수 있다.** kernel 선택은 4 이산의 단일 좌표 (저차원) 이므로, RR 은 restart 로 전 4 kernel 을 직격한다. "best kernel 을 찾는" 데 골짜기를 넘을 필요가 없다 = **teleport (직접 워프).** 그래서 ③ 의 behavioral niching 에 차례가 오지 않는다.

Step4 의 corridor 에서 ③ 가 RR 을 배제할 수 있었던 것은, 거기의 behavior 가 `mean(24 차원)` 이고, CLT 에 의해 평균이 0.5 에 집중 → 대역 피크가 measure-zero 역 = **random/RR 이 직접 샘플링할 수 없는 고차원** 이었기 때문이다. kernel_id 는 반대로 저차원이라 직접 샘플링되어 버린다.

##### (3) red-team —— 적대 검증으로도 반증할 수 없고, 오히려 확증

"harness 가 서지 않는 것은 정말 구조 탓인가? 우연한 설정 실수 아닌가?" 를 독립 red-team 으로 두들겼다. 결과는 구조 주장을 **반증할 수 없었고, 오히려 강화**:

- **기제 확증**: instrumented RR 이 positive control 위에서 4 basin 에 restart kid 를 [12,18,16,18] 로 거의 균일 분산, target 도달 88%, best 는 restart→in-basin climb 가 6/8 seed. "RR 은 restart 로 kernel_id 를 직접 샘플링해 골짜기를 회피한다" 를 **수치로 확증.**
- **4 개의 faithful 구성 (고차원 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) 모두에서 ③ 는 RR 에게 이기지 못한다 (beats_rr=False).** corridor 를 풀면 RR 도 동등 도달, 조이면 ③ 가 **먼저 starve** (아사).
- **경계 sweep**: theta corridor 의 차원을 D=0→3 으로 조일수록 ③ 가 RR 보다 빨리 starve (D=3: ③ reach 0.08 vs RR 0.42). base_seed 3 가지로 동일.

→ **"RR 만 배제하고 ③ 가 통하는 behavior 차원은, kernel 공간에 구조적으로 존재하지 않는다"** 를 정량 확증.

##### 구조적 통찰 (이 결판의 payoff)

> **③ (MAP-Elites 의 behavioral niching) 이 강한 baseline 을 능가하는 것은, "난소" 가 고차원 behavior 공간에 있어 직접 샘플링 (random restart) 으로 도달할 수 없을 때뿐.**

- **kernel 선택은 저차원 (4 이산의 단일 좌표)** → RR 이 직접 샘플링 → ③ 의 niching 우위가 원리적으로 나오지 않는다.
- theta 공간에 기만을 옮겨도, RR 은 restart 후에 in-basin 에서 greedy climb 하므로, corridor 를 RR 이 빠져나가지 못할 정도로 조이면 ③ 도 같은 정도로 starve 한다. **RR fail ∧ ③ succeed 의 창이 존재하지 않는다.**

이것은 Step4 §7 에서 남은 질문 "탐색 공간을 kernel 다양화로 확장하면 ③ 가 unlock 하는가?" 에 대한 답이다. 답은 **NO (CPU 에서는 구조적으로).** 확장이 ③ 를 unlock 하려면, 추가한 자유도가 **고차원이라 직접 샘플링이 곤란한** behavior 를 낳아야 한다. kernel 선택 (저차원·이산) 은 그 조건을 충족하지 않는다.

##### GPU 로의 함의

- **CPU 모두 쏟기 게이트가 CLEAR**: BG9 가 마지막 CPU 길 (kernel-union) 을 구조적으로 닫았다. ③ 의 남은 길은 **고차원의 GPU full-LLM 손실 지형뿐.**
- 구조적 통찰은 GPU 의 베팅을 **better-motivated** 하게 만든다. ③ 는 고차원 behavior 에서 비로소 의미를 가진다. full-LLM 의 파라미터 공간은 수백만 차원 = 바로 고차원. 그래서 GPU 검정은 "full-LLM 만이 예외일지도" 라는 약한 베팅이 아니라 "③ 는 고차원을 요하고, full-LLM 이 고차원역" 이라는 원리에 부합한다.
- **다만 여전히 bet**: 실 LLM 지형이 backprop 계의 강한 baseline 으로 직접 내비게이트할 수 있다면 ③ 불필요 ── 이것은 **BG9 의 RR 과 동형의 리스크** 다 ("강한 baseline 이 직접 푼다" 가능성은 GPU 에서도 남는다). 그래서 GPU 는 "③ 를 위해 단독" 이 아니라 **포트폴리오 판단** (llive 실 LLM fitness 등과 동승) + **클라우드 대여로 사전 등록 1 건** (자본 커밋 전) 이 적정. BG9 의 구조적 통찰 그 자체가 GPU 의 falsifiable 한 go/no-go 기준이 된다: "③ 가 full-LLM 에서 load-bearing 이라면, 그 난소는 고차원 behavior 공간에 있어 직접 샘플링/backprop 으로 도달 곤란할 터."

##### honest 유보 (중요)

- 이것은 **"③ 불필요로 판명" 이 아니다.** "③ 가 이 저차원 kernel 공간에서는 강한 baseline 과 원리적으로 분리될 수 없다" = N/A (구조적) 이며, ③ 의 기제 자체는 Step4 에서 진짜로 확정 완료다. N/A 지만 "kernel 길은 닫혀 있다" 는 결정적 정보를 가진 **정보량 있는 N/A** 다.
- harness/red-team 은 smoke 규모 (5-12 seed). 본검정 15 seed 에서는 수치는 움직이지만, **구조 (조이면 ③ 가 먼저 starve / RR 이 kernel_id 를 직접 샘플링) 는 seed 비의존으로 견고.** real 의 full ≥15-seed 본검정은 실시하지 않는다 ── positive control validity 가 구조적으로 서지 않는 이상, real 에서 ③ 불필요가 나와도 "③ 불필요 vs 검출기 맹" 을 분리할 수 없고, 그 "검출기 맹 = kernel 공간의 구조" 를 red-team 이 이미 확정했으므로, CPU 를 7.5h 투입해도 결론은 바뀌지 않기 때문이다.
- substrate 는 약하다 (실질 3 kernel, **hopfield 는 대각 mock 으로 기능 불능**). 더 강한 kernel 변별 (full 구현·비대각) 이라면 다른 결론의 여지가 **이론상** 있지만, ③ 의 구조적 장벽 (저차원 선택 → RR 직접 샘플링) 은 kernel 구현의 질과 독립이다.
- "너무 깔끔한 ③ 성립" 을 의심하는 규율은 이번에는 **불필요했다** ── ③ 성립은 처음부터 나오지 않았다 (honest prior 대로의 negative).

---

#### 12. 메타 교훈 —— 정직함은, 이기기 위한 도구였다

오늘의 진짜 성과는 수치가 아니라, **"너무 깔끔한 결과를 의심하는" 정신이 실제로 연구를 앞으로 나아가게 했다** 는 것이다.

- 평가 노이즈를 물리적으로 지웠기 (EXP2) 때문에, "매끄러움" 이 지형의 성질인지 계기의 한계인지를 가려낼 수 있었다.
- 적대 검증 3 렌즈를 댔기 때문에, "③ NOT null" 을 headline 으로 하지 않고 "후보" 에 머무를 수 있었다.
- 자신의 stale 값 착각을 자기 검출했기 때문에, N/A 라는 올바른 강등을 할 수 있었고, 오늘 다시 측정할 수 있었다.
- **BG9 (추기) 에서 하나 더 배웠다**: **저차원의 난소는 강한 baseline 이 직접 풀어 버린다. 그래서 ③ (골라내고 키우는 공정) 가 효과를 내려면 "고차원 behavior 공간" 이 필요하다.** "속임수 지형을 만들면 ③ 가 선다" 는 절반만 맞고, 정확히는 "**직접 샘플링할 수 없을 만큼 고차원인** 속임수 지형" 이 아니면 ③ 는 서지 않는다. kernel 4 택 (저차원) 에서는, RR 이 restart 로 전부 직격하므로 ③ 의 차례가 원리적으로 오지 않았다. 이것은 샛길을 "포기" 가 아니라 "**구조적으로 닫혔다**" 고 단언할 수 있는 근거다.

"이상하게 좋은 결과가 나오면, 이긴 기분이 되기 전에 반드시 내막을 의심한다" ── FullSense 의 연구 규율 (`feedback_benchmark_honest_disclosure`) 은, 단순한 자계가 아니라, **실제로 위양성을 붙잡아 연구의 정밀도를 올리는 기제** 로서 돌아가고 있었다. BG9 는 그 역방향 (**negative 를 올바르게 negative 로 확정한다**) 에서도 같은 규율이 효과를 낸 예다 ── red-team 에서 자신의 "③ 가 서지 않는다" 를 반증하려다, 반증할 수 없어 구조로서 확증됐다.

결론을, 마지막으로 한 번 더, 정확하게 (BG9 결판을 반영):

> **proxy substrate 위에서는 "③ 는 지형이 진정으로 매끄럽기에 불필요" 가 noise-free 로 확정**됐다 (Step D). 실 multitask 근방 (C-gen4b) 에서만 "③ NOT null" 의 약한 징조가 나왔지만, 소효과 + 드리프트 + 다중 비교로 **후보에 그침.** K4 clip 은 능동적 suppression 이 아니라 진단적 소견으로 강등. 그리고 CPU 의 마지막 샛길 **kernel 다양화 (BG9) 는 구조적으로 닫혔다** ── kernel 선택은 저차원이라 강한 baseline (RR) 이 직접 샘플링하고, ③ 의 niching 우위가 원리적으로 나오지 않는다. **③ 의 본진 검증에 남겨진 길은, 고차원의 GPU full-LLM 손실 지형뿐** (그것도 "강한 baseline 이 직접 푼다" 리스크를 안은 bet).

"③ 결판 = ③ 는 불필요로 판명" 이 아니다. 정확히는 **"③ 가 살아나는 건 '고차원의' 기만 지형일 때뿐. 지금 CPU 로 측정할 수 있었던 실물 비슷한 것 (매끄러움) 도 kernel 다양화 (저차원) 도, 그 조건을 충족하지 못했다."** 본진 (GPU 고차원) 은 아직 멀고, 게다가 보증 없는 베팅이다.

---

**Tags**: 진화 계산 / MAP-Elites / 통계 검정 / 검출력 / honest disclosure / CPU 연구
**관련**: 연재 #32 (llcore CPU PoC battery) / #29 (반증·Goodhart·proxy 한계) / #31 (Codex 이본주)
**Project**: llcore (PyPI 예약 llmesh-llcore, 리포지토리 미공개이므로 로컬 연구)

## 10. llcore — 「進化で AI を設計するとき、選り分けて育てる工夫 (③) は要るのか」を 6 段の実験 + 生物学で俯瞰した話 (第三軸 arc 全体)

### (연재 #34) 산오르기 6연전으로 알게 된 「진화의 ③은 언제 효과가 있는가」— 그리고 100년 전의 진화생물학이 같은 답을 내놓고 있었다

#### TL;DR

- 질문은 **「AI의 코어 계산을 진화로 탐색할 때, '가려내어 따로 길러 내는 공정' (= 진화의 ③ 적자생존/분리) 은 정말로 필요한가」**. 연재 #33은 종반 (Step D + BG9) 의 결착을 썼지만, **이 #34는 arc 전체 (6단) 를 하나의 이야기로 조망**합니다.
- **제1단 (합성 속임수 지형)**: ③은 압승 (Cliff δ=+1.0). ③은 메커니즘으로서 진짜 = **존재 증명**.
- **제2단 (기억 과제 / 다중 reservoir)**: 기질의 「바닥」과 「천장」에 가로막혀 ③을 측정 불가 = **N/A**.
- **제3단 (다중 과제 일반화)**: ③은 「선택 없음」에는 이기지만, 단순한 선택이나 random에는 못 이김 = ③ 불필요 (honest negative).
- **제4단 (실제 proxy 지형을 noise-free 측정)**: 평가 노이즈를 물리적으로 0까지 낮췄더니 지형은 **정말로 매끄러움 (단봉)** = ③ 불필요 확정. 「과거의 negative는 검출력 부족이 아니라 지형이 매끄러웠던 것」이 처음으로 뒷받침되었다.
- **제5단 (부품 4종을 섞는 샛길 BG9)**: kernel 선택은 **저차원**이기에 강한 baseline (랜덤 리스타트 산오르기) 이 직접 샘플링하고, ③의 niching 우위가 **구조적으로** 나타나지 않음 = 샛길은 막혔다.
- **구조적 통찰 (이 arc의 핵심)**: ③이 효과가 있는 것은 난소(難所)가 **고차원 behavior 공간**에 있어 직접 샘플링이 불가능할 때뿐. 실제 CPU 기질은 저차원/매끄러우므로 ③ 불필요.
- **생물학적 접지 (검증 완료)**: 이것은 라이트 (Wright) 의 **시프팅 밸런스 설** 바로 그것. **흑화형 나방 (단일 유전자 = 저차원)** 에서는 보통의 선택으로 충분 (= BG9의 kernel 케이스), **렌스키의 Cit+ (고차원・역사 의존)** 에서는 다양성이 효과적 (= ③ regime). 우리의 negative는 **코인 비판의 계산판** (현실 지형은 단순하고 ③은 드물게만 결정적).
- **메타 교훈**: 「너무 잘 풀린 결과는 승리가 아니라 경보」. 사전 등록・honest disclosure・적대 검증・결정론적 noise-free 측정으로, 섣부른 기쁨을 피했다.

> ⚠ 이 글의 수치는 모두 수중 (로컬) 의 연구 기록에 연결된 실측입니다. llcore는 아직 공개 리포지토리를 만들지 않았으므로 외부 링크를 붙일 수 없습니다. 대신 「어떻게 측정했는가」를 본문에 씁니다. 생물학 파트에서 인용하는 논문은, 별도로 1차 정보로 존재・귀속・주장 내용을 대조한 것만 들고 있습니다.

---

#### 0. 이 글은 무엇에 대한 이야기인가 (콘셉트)

`llcore`는 「Transformer의 코어 계산 (상태 갱신 규칙・학습 규칙・인지 구동 Δ) 을 유전자로 삼아, Z3로 망가지지 않도록 검증하면서 진화시킨다」는 CPU 완결 연구 프레임워크입니다.

그 진화 엔진에는, 진화의 4요소 (① 변이 / ② 유전 / ③ 적자생존・분리 / ④ 과잉번식) 중 **③ (selection / separation)** 을 어떻게 효과적으로 발휘시킬 것인가, 라는 설계상의 급소가 있습니다. 다양성을 유지하며 니치에 남기는 MAP-Elites 같은 「가려내어 따로 길러 내는」 구조입니다.

질문은 단순합니다.

> **그 ③, 정말로 필요한가?**

필요하다면, ③을 얹기 위한 무거운 투자 (최종적으로는 GPU로 실제 LLM을 돌리는 것) 에 의미가 있다. 필요 없다면, ③에 집착하는 것은 시간과 전기의 낭비가 된다.

연재 #33에서는 그 질문의 **종반** (Step D의 결정론 측정 + BG9의 구조적 결착) 을 상세히 썼습니다. 하지만 거기에 이르기까지에는 **6단의 실험**이 있었고, 이기거나 (존재 증명), 측정하지 못하거나 (N/A), 지거나 (honest negative) 를 반복했습니다. 이 #34에서는 그 **arc 전체를 하나의 이야기**로 다시 늘어놓습니다. 게다가 이번의 볼거리로서, **이 계산 결과가 100년 가까이 전의 진화생물학 논쟁 (라이트 대 피셔) 과 놀랄 만큼 같은 형태를 하고 있다**는 것을, 검증 완료한 1차 정보로 접지합니다.

— 여기까지 40초. 준비운동 끝. 본론으로. —

---

#### 1. 비유: 산오르기, 그리고 속임수 지형, 그리고 기억의 궁전

수식 전에, 이 연구에서 일관되게 쓰고 있는 3개의 메타포로 전체상을 파악합니다.

설계의 좋고 나쁨을 **지형의 높이**로 나타냅니다. **높은 곳 = 좋은 설계**. 가장 높은 정상을 찾는 게임입니다.

**지형 1: 매끄러운 한 봉우리 (쉬움)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

이런 지형에서는, 소박한 「산오르기법 (hill-climbing)」, 즉 「지금보다 조금 더 좋은 쪽으로 움직이기만」 하는 것으로 충분히 정상에 닿습니다. **공들인 공정 (③) 은 필요 없습니다.**

**지형 2: 속임수 지형 (기만적 deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

여기서는 소박한 산오르기가 가짜 정상에서 멈춥니다. 골짜기를 내려갈 용기가 없기 때문입니다.

이때 효과를 발휘하는 것이 ③의 발상입니다. **여러 타입의 등산자를 골짜기 여기저기에 남겨 둡니다** (= 기억의 궁전 / MAP-Elites archive). 누군가가 골짜기를 「징검돌 (stepping-stone)」 로 건너 진짜 정상에 도달할 수 있다, 라는 구조입니다.

**이 연구의 핵심을 한마디로**: ③이 정말로 도움이 되는 것은 **「속임수 지형」일 때뿐**. 매끄러운 한 봉우리에서는, ③은 무용지물입니다.

그래서 질문은 이렇게 바꿔 말할 수 있습니다.

> **「진화로 AI를 설계할 때, 실제로 마주치는 지형은 '속임수 지형'인가, 아니면 '매끄러운 한 봉우리'인가?」**

#33에서는 Step D + BG9로 이 질문에 결착을 지었습니다. 이 #34에서는, 거기에 이르는 **6단의 산오르기 전부**를 보여드립니다. 각 단에서 「속임수 지형이었는가 / 매끄러웠는가 / 애초에 측정할 수 있었는가」가 달라지는 것이 흥미로운 점입니다.

— 잠깐 쉼. 준비는 여기까지. 여기서부터 6연전의 실록입니다. —

---

#### 2. arc 전체 지도 — 6단의 산오르기를 한눈에

먼저 지도를 내놓습니다. 이것이 이 글의 등뼈입니다.

| 단 | 기질 (어떤 지형을 측정했나) | ③은 효과가 있었나 | 한마디 |
|---|---|---|---|
| **I (Step 4)** | 합성한 「속임수 지형」(기만 corridor) | **Yes (압승)** | 존재 증명. ③은 진짜 |
| **II (Step C / 사다리1)** | 기억 과제 / 다중 reservoir 패리티 | **N/A** | 바닥・천장・degree-5의 벽으로 측정 불가 |
| **III (E-A)** | 다중 과제 일반화 | **No** | ③은 「선택 없음」에는 이기지만, 그 이상은 아니다 |
| **IV (Step D)** | 실제 proxy의 텍스트 지형 (결정론 측정) | **No** | 지형이 **정말로 매끄러움**으로 확정 (noise-free) |
| **V (BG9)** | 부품 (kernel) 4종의 union | **No** | **구조적으로** 막혔다 (저차원 선택) |

스토리 라인은 이렇습니다. **먼저 「③은 조건에 따라 압승하는 진짜다」라고 존재 증명하고 (I), 다음으로 「그럼 실제 문제에서는 어떤가」를 4단에 걸쳐 측정하러 갔더니 (II~V), 하나같이 "실제 CPU 기질은 ③이 필요 없는 지형이었다"**. 게다가 마지막 (IV, V) 에서 「필요 없는 이유」가 **검출력 부족이 아니라 지형의 성질**이라고 확정되었다 ── 이것이 arc 전체의 호(arc)입니다.

그럼 한 단씩.

---

#### 3. 제I단 (Step 4) — 존재 증명: 속임수 지형이라면 ③은 압승한다

가장 먼저 한 것은 「③이 **이론대로 효과를 내는 장면이 실재하는가**」의 존재 증명입니다. 지형을 **일부러 기만적으로 만들어**, ③ (MAP-Elites) 을 3개의 baseline ── pure random / panmictic GA / **랜덤 리스타트 산오르기 (random-restart hill-climbing)** ── 와 대결시켰습니다.

**지형의 구성**: 유전자는 24차원. behavior (등산자의 타입) 를 `mean(유전자)` = 24개의 평균으로 정의합니다. behavior를 올리려면 **전체 24차원을 동시에 높게** 하지 않으면 안 됩니다. fitness는 「behavior≈0.4에 가짜 정상 (값 0.6) → behavior≈0.65에 골짜기 (값≈0) → behavior≈0.9에 진짜 정상 (값 1.0)」 라는, 그야말로 속임수 지형.

**결과**:

| 방법 | 진짜 정상으로의 도달률 | ③ 과의 비교 |
|---|---|---|
| **MAP-Elites (③)** | **약 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | 위와 같음 |
| 랜덤 리스타트 산오르기 | 0% | 위와 같음 |

③만이 진짜 정상에 닿았고, 3개의 baseline은 전부 가짜 정상 (≈0.60) 에서 멈췄습니다. **100% 승 / 효과량은 이론 최대 (δ=+1.0)**. base seed 3가지 (총 60 seed) 에서 견고.

왜 이렇게 되는가, 가 나중의 복선이 됩니다.

- **random** 은 behavior가 반드시 ≈0.5에 집중한다 (24개의 평균은 중심극한정리로 0.5에 고정). 그래서 behavior 0.9에는 **영원히 도달할 수 없다** (6000 샘플을 뽑아도 0%).
- **산오르기** 는 가짜 정상 0.6까지 오르고, 골짜기를 내려가는 한 수를 거부. 리스타트해도 behavior≈0.5로 돌아가, 같은 함정으로.
- **③ (MAP-Elites)** 는 골짜기의 칸을 「새로운 behavioral 니치」로 보유하고, behavior를 0.5 → 0.9로 **징검돌로 건넌다**.

**경계도 정직하게 측정했습니다**. 골짜기를 없앤 매끄러운 corridor에서는, ③은 산오르기를 못 이기게 됩니다 (p≈0.29). **③은 만능이 아니라, 속임수 지형에서만 효과가 있다.**

**honest 유보**: 이것은 **일부러 만든** 합성 지형입니다. ③이 「가능」하다고 증명했을 뿐, 현실의 과제가 이 구조를 가진다는 증명은 아니다. toy 스케일・저노이즈・baseline은 소박한 (1+1) 입니다.

→ 여기서 가설이 섭니다. **「실제 문제의 지형도, 이 정도로 속임수 지형이라면, ③은 살아날 것」**. 다음 4단은, 그것을 실제 문제에 가까운 기질로 확인하러 가는 여행입니다.

— 한 모금. 제I단은 기분 좋은 압승이었습니다. 여기서부터 구름의 흐름이…. —

---

#### 4. 제II단 (Step C / 사다리1) — 기질의 「바닥」과 「천장」에 가로막힌다 (N/A)

다음으로 「속임수 corridor가 **표준적인 기억 과제에 자연스럽게 출현하는가**」를 조사했습니다 (Step C). delayed parity / flip-flop / delayed recall을, 1개의 leaky reservoir + ridge readout으로.

결과는 깔끔한 **N/A (측정 불능)**. 이유가 양극단이라 흥미롭습니다.

- **delayed parity = 바닥 (floor)**: 1개의 reservoir는 XOR을 계산할 수 없다 (Minsky-Papert). 모든 방법이 R²≈0.003. 아무도 오를 수 없으므로 ③을 분리할 수 없다.
- **flip_flop = 천장 (ceiling)**: 모든 방법이 R²≈0.95에 포화. 분산이 짓눌려 ③의 차이가 나타나지 않는다 (③ vs random은 부호는 양이지만 p=0.15 = underpower로 **null이 아니다**).

여기서 중요한 발견이 하나. **유전자 공간의 다봉성은 높았다** (valley fraction이 parity에서 1.000) 인데, ③의 역할에는 도움이 되지 않았다. 즉 **「유전자 공간에서 다봉」≠「behavior에서 건너야 할 속임수 지형」**. 이 구별이 arc 후반의 열쇠가 됩니다.

**사다리1 (다중 reservoir)**: 그럼 reservoir를 여럿 연결하면 바닥이 올라가는가? → 5개의 메커니즘을 시험해 전부 `floor_lifted = false`. 깊이 (DeepESN) 는 바닥을 통계적으로는 올린다 (효과 +0.47/+0.60, PASS) 지만 절댓값은 R² 0.05-0.10에 그친다. 결정타는 positive control: degree-2 readout은 2-bit XOR을 엄밀히 푼다 (R²=+1.0) 지만 degree≥3에서 붕괴. **5-bit 패리티는 degree-5 = 이 CPU reservoir+ridge 패러다임의 구조적인 벽.**

→ 패리티 경로는 구조적으로 막혔다. ③의 본검정은 **패리티에서 내려올** 필요가 있다.

**honest 유보**: degree-5의 벽은 「이 설정의 벽」이지, 패러다임 전체의 불가능성 증명은 아닙니다.

— 잠깐 쉼. 「측정할 수 없었다」는 결과는 수수하지만, 지도를 그리는 데에는 중요한 공백 지대입니다. —

---

#### 5. 제III단 (E-A) — 다중 과제 일반화: ③은 필요 없었다 (honest negative)

패리티의 바닥에서 내려와, **일반화 (generalization)** 로 ③을 측정했습니다. 가장 깔끔한 ablation을 짜서.

**설정**: 단층 leaky reservoir + ridge. 가변 지연의 recall. **짧은 지연 {15, 30} 으로 학습하고, 긴 지연 {45, 60} 으로 테스트** (외삽). 비교는 MAP-Elites (①②③풀) vs **선택을 뺀 MAP-Elites** (`randselect`: 부모를 랜덤으로 골라 무조건 배치 = 변이만) + panmictic GA + random.

**결과 (페어 리뷰 후)**:

| 방법 | 테스트 일반화 R² (평균±std) |
|---|---|
| MAP-E (①②③풀) | 0.682 ± 0.115 |
| MAP-E randselect (선택을 뺌) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| 게이트 | 비교 | diff | p (단측) | 판정 |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**읽는 법**: ③은 「**선택을 뺀 드리프트 대조**」에는 이긴다 (C-gen3 PASS = "어떤 선택이든 무선택에는 이긴다"). 하지만 **panmictic GA (선택은 있지만 niching 없음) 에는 못 이기고** (오히려 근소하게 짐), random에도 못 이긴다. 즉 **niching 고유 (= ③ 본래) 의 기여는 없다**. 이 일반화 지형은, 단순한 선택이나 random으로도 같은 곳에 닿을 만큼 **매끄러웠다**. 제I단의 「매끄러우면 ③은 효과가 없다」 경계와 정합합니다.

**honest 유보 (중요)**: 이 verdict는 **이 설정 한정** (예산 400, grid 6×6). 게다가 ── 여기가 honest methodology의 핵심 ── 페어 리뷰 (Codex) 가 당초 「신용할 수 없다」고 판정하고, 3개의 rerun 블로커 (replicate마다의 독립 seeding / 예산 내 글로벌 최량의 채용 / honest_n을 16→30) 를 강제했습니다. **수정 후에도 결론은 바뀌지 않았습니다.** 「고치면 결론이 바뀌는 취약한 negative」가 아니었다, 라는 것이 수확입니다.

— 한 모금. 진 건 진 거지만, 「올바르게 졌다」는 것을 확인하는 작업 쪽이 시간이 더 걸렸습니다. —

---

#### 6. 제IV단 (Step D) — 실제 proxy 지형은 「정말로 매끄러움」으로 확정 (noise-free)

여기가 arc의 전환점입니다. 제III단까지 「③ negative」가 이어졌지만, 줄곧 **응어리**가 남아 있었습니다.

> 「③ 불필요」는 정말로 **지형이 매끄럽기** 때문인가? 아니면 단순히 **샘플 수가 부족해 차이를 검출하지 못한 (underpower)** 것뿐인가?

이것을 헷갈리면 「③은 무력」이라고 과잉 일반화해 버린다. Step D는 여기에 결착을 짓습니다.

**트릭**: ESN reservoir (고정 seed) + ridge readout의 closed-form (`np.linalg.solve`) 은 **난수를 일절 뽑지 않는다**. 그래서 평가 노이즈를 **머신 엡실론 (약 1.11e-16)** 까지 물리적으로 0으로 만들 수 있다. 실측으로 `eval_noise_std ≤ 1.11e-16`을 확인 ── 이것은 부동소수점의 최소 단위 (ULP) 유래로 **실질 제로**입니다. 노이즈의 안개를 완전히 걷어내고, 지형의 골짜기를 직접 측정할 수 있다.

지형은 llcore 자신의 소스 (약 24k 문자) 의 다음 문자 예측. valley_fraction (골짜기의 비율, ≥0.2면 다봉=속임수 지형) 을 측정했습니다.

| 지형 | 차원 | valley_fraction (mean/max) | 다봉? | 판정 |
|---|---|---|---|---|
| **ESN 3-param** (실제 proxy) | 3 | **0.000 / 0.000** | No (3 seed 일치) | 매끄러움 → noise-free로 ③ 불필요 확정 |
| **ESN per-neuron** (실제 proxy) | 40 | **0.096 / 0.121** | No (3 seed 일치) | 매끄러운 편 → ③ 불필요 |
| 다봉 control (양) | 3 / 40 | 0.70 / 0.80 | Yes | 진단기는 다봉을 검출할 수 있다 ✓ |
| 이차함수 control (음) | 3 / 40 | 0.000 | No | 진단기는 매끄러움을 검출할 수 있다 ✓ |

포인트는 2개.

1. **실제 proxy 지형 (3차원 / 40차원 모두) 은 단봉**. 3 seed에서 일치.
2. **진단기 자체는 건전**. 일부러 만든 다봉은 제대로 다봉으로 검출하고, 이차함수는 제대로 매끄러움으로 검출한다. 그래서 「실제 proxy가 단봉」은 계기의 버그가 아니라 **지형의 성질**.

→ 이것으로 처음으로 **「과거의 ③ negative는 underpower가 아니라, 지형이 정말로 매끄러웠다」**가 실제 substrate 위에서 noise-free로 뒷받침되었습니다. 재측정해도 다봉은 나오지 않는다.

**honest 유보 (중요)**: 「매끄러움」은 임곗값 근접에서만 정밀합니다. ESN 3-param의 midpoint의 **90.9%가 약간 아래로 dip**하고, 최대 상대 dip (0.0435) 은 골짜기 임곗값 0.05의 바로 아래. 정확히는 「**진정으로 단봉**」이 아니라 「**임곗값을 근소하게 밑도는 얕은 골짜기 (~2-4%) 를 가진 약한 multi-basin**」. 방향은 유지되지만, 견고성은 임곗값 근접이기에 한정적 ── 여기를 「완벽한 볼록 그릇」으로 뭉뚱그리지 않는 것이, 이번의 규율입니다.

— 심호흡. 여기서 「실물 모형도 매끄럽다」가 확정. 남은 건 「마지막 CPU 샛길」입니다. —

---

#### 7. 제V단 (BG9) — 부품을 섞는 샛길은, 구조적으로 막혀 있었다

실제 proxy가 매끄럽다고 확정된 이상, 매끄러운 지형에서 ③을 좇아도 이득은 나오지 않는다. 하지만 GPU는 투자 판단이므로, **CPU에서 전진할 수 있는 다른 가설**을 시험했습니다. 그것이 **kernel 다양화 (BG9)** 입니다.

**가설 (사전 등록 H7)**: 개개의 kernel (rwkv / mamba / hopfield / linear_attn) 이 매끄러워도, **4종류를 union하면 kernel 전환의 순간에 fitness가 단차를 만든다 → multi-basin (속임수 지형) 이 된다 → ③이 GPU 없이 CPU 위에서 선다**. 사전 등록한 honest prior는 **null 쪽** (지금까지 모든 CPU 기질이 매끄러웠으므로).

결과를 3단으로.

**(1) substrate validity — 변별은 있지만 약하다 (PASS지만 요주의)**: 과제마다 잘하는 kernel이 다른가를 측정하면, 사상(寫像)은 비상수 = non-inert (PASS). mamba는 selective-copy, linear_attn은 weighted-accumulation에서 best. 다만 **hopfield는 어떤 과제에서도 못 이겼다** (대각 스칼라 mock에서 기능 부전) 므로, 실질 「**3 kernel** union」. **변별의 존재 ≠ 다봉 장벽.**

**(2) harness validity — positive control이 validate하지 않는다 (결정타)**: 합성 kernel-barrier에서 ③을 3 baseline과 비교.

| 기질 | 결과 |
|---|---|
| **positive control** | ③은 panmictic (+0.423)・random (+0.208) 을 격파. **하지만 RR (랜덤 리스타트 산오르기) 에는 못 이긴다** (+0.051, p=0.31 → FAIL). 3 baseline 전승에 못 미침 = harness가 안 선다 |
| **negative control** | 모든 method 포화, ③ 우위 없음 = 올바르게 null (계기는 건전) |
| **real** smoke | ③ beaten 0/3, panmictic이 역으로 ③을 웃돈다 |

제I단의 corridor에서는 ③이 RR을 배제할 수 있었는데, **왜 kernel 공간에서는 못 하는가?** 근본 원인은 하나.

> **RR은 restart 때마다 kernel_id ∈ [0,4) 를 직접 샘플링할 수 있다.** kernel 선택은 4 이산의 단일 좌표 (**저차원**) 이므로, RR은 restart로 전체 4 kernel을 직격한다. 「best kernel을 찾는」 데 골짜기를 건널 필요가 없다 = **직접 워프**. 그래서 ③의 behavioral niching에 출번이 오지 않는다.

제I단에서 ③이 RR을 배제할 수 있었던 것은, 거기의 behavior가 `mean(24차원)` 이고, 평균이 0.5에 집중 → 대역 피크가 measure-zero 영역 = **직접 샘플링 불가능한 고차원**이었기 때문. kernel_id는 반대로 저차원으로 직접 샘플링할 수 있어 버린다.

**(3) red-team — 적대 검증으로도 반증할 수 없고, 오히려 확증**: instrumented RR이 positive control 위에서 4 basin에 restart kernel을 [12,18,16,18] 로 거의 균일 분산, target 도달 88%. 4개의 faithful 구성 (고차원 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) 모두에서 ③은 RR에 못 이긴다. corridor를 조이면 ③이 **먼저 starve (아사)** 한다 (D=3: ③ reach 0.08 vs RR 0.42). **「RR만 배제하고 ③이 통과하는 behavior 차원은, kernel 공간에 구조적으로 존재하지 않는다」**를 정량 확증.

**verdict**: 형식상은 N/A (positive control이 validate하지 않음) 지만, 실질은 **결정적인 구조적 negative**. harness는 건전 (negative control을 올바르게 null로 하고, GA/random을 검출한다) 한데, 기질이 ③의 속임수 지형을 **애초에 호스트할 수 없다**. 제I단에서 남은 질문 「kernel 다양화로 탐색 공간을 확장하면 ③이 unlock하는가?」에 대한 답은 **NO (CPU에서는 구조적으로)**.

**honest 유보 (중요)**: 이것은 **「③ 불필요로 판명」이 아닙니다**. 「③이 저차원 kernel 공간에서는 강 baseline과 원리적으로 분리할 수 없다」 = **정보량이 있는 N/A**. ③의 메커니즘 자체는 제I단에서 진짜로 확정 완료. substrate는 약하다 (실질 3 kernel, hopfield는 대각 mock). 더 강한 kernel 구현이라면 다른 결론의 여지는 이론상 있지만, **구조적 장벽 (저차원 선택 → RR 직접 샘플) 은 kernel 구현의 질과 독립**입니다.

---

#### 8. 구조적 통찰 — 6단을 하나의 조건으로 정리한다

존재 증명 (I) 과 4개의 negative (II~V) 는, 단 하나의 조건으로 전부 이어집니다.

> **③ (behavioral niching) 이 강 baseline을 웃도는 것은, 「난소」가 고차원 behavior 공간에 있어, 직접 샘플링 (랜덤 리스타트) 으로 도달할 수 없을 때뿐.**

- **제I단이 충족하는 이유**: behavior = `mean(24차원)`. 평균은 중심극한정리로 0.5에 집중하고, 대역 피크 (mean≈0.9) 는 실질 measure-zero. random도 restart도 **직접 닿지 않는다**. 그래서 징검돌을 남겨 ratchet하는 ③이 필수.
- **실제 CPU 기질이 충족하지 않는 이유**: 난소가 저차원. ESN 텍스트 proxy의 제어 좌표는 실질 leak rate (매끄러운 저차원 노브, 애초에 골짜기가 없다). kernel union의 난소는 「어느 kernel인가」 = 4지선다의 단일 이산. RR이 직접 샘플링해 전 basin에 teleport하므로, 건너야 할 골짜기가 없다.

그래서 제II단의 「유전자 공간의 다봉성 1.000」은 충분조건이 아니다 ── 유전자는 골짜기투성이라도, 난소가 저차원 behavior 좌표에 집중해 있으면, restart가 직접 닿는다. **효과가 있는 것은 "탐색이 도달해야 할 behavior의 차원"이지, 유전자의 차원이 아니다.**

---

#### 9. 생물학적 접지 — 100년 전의 진화생물학이, 같은 답을 내놓고 있었다

여기서부터가 #34의 볼거리입니다. **「다양성을 유지하는 선택은, 좁은 조건에서만 효과가 있고, 그 외에서는 잉여」** ── 이 경계 조건에는, 20세기의 진화생물학에 이상하리만치 깔끔한 선례가 있습니다.

> ⚠ **honesty 계약**: 이하의 생물학은 **「비유 (structural analogy)」 이지, 우리 계산 결과의 증명이 아닙니다**. 대응은 구조적이고, 메커니즘 레벨에서는 일치하지 않습니다. 비유가 어긋나는 곳은 전부 그 자리에서 명기합니다. 인용하는 논문은, 별도로 1차 정보로 존재・귀속・주장 내용을 대조한 것만입니다.

##### 9.1 라이트 (Wright) 의 시프팅 밸런스 설 = ③의 선례

슈얼 라이트 (Sewall Wright, 1931/1932) 는 이렇게 생각했습니다. 큰 「하나의 무리 (panmictic population)」 인 채로는, 보통의 자연선택으로는 **눈앞의 국소 피크에 붙잡힌다**. 더 높은 산으로 가려면 한 번 mean fitness를 **낮춰 골짜기를 건널** 필요가 있는데, 결정론적인 선택은 그것을 거부하기 때문.

라이트의 해결책은 **무리를 다수의 반(半)격리된 서브 집단 (deme) 으로 나누는** 것.

- **Phase I**: 작은 deme가 **유전적 부동 (drift)** 으로 우연히, 골짜기를 내려가 건넌다.
- **Phase II**: 거기서 deme 내의 보통의 선택이 새로운 (더 높은) 피크를 오른다.
- **Phase III**: 높은 피크에 오른 deme가 많은 이주자를 내보내, 우수한 유전자 조합이 종 전체에 퍼진다.

메타 집단 **전체**로서, 단일 수렴 집단으로는 건널 수 없는 골짜기를 건넌다 ── 이것이 「속임수 지형의 골짜기를 징검돌로 건넌다」의 생물학판입니다.

**③ / MAP-Elites로의 대응 (= 비유, 귀속이 아님)**: archive의 각 셀 = 준격리 deme, 셀 내의 국소 elitism = deme 내 선택 (Phase II), 셀 간 변이 = interdeme 확산 (Phase III), 그리고 **archive 전체** (≒ 메타 집단, 단일 셀이 아님) 가 골짜기를 건넌다.

> **honesty 주의 (2점)**:
> 1. **이것은 해설자의 틀이지, 라이트의 주장도 MAP-Elites의 출처도 아니다.** MAP-Elites의 원논문 (Mouret & Clune 2015) 도 QD 문헌도 **라이트나 「시프팅 밸런스」를 인용하지 않는다**. 라이트는 우리의 **착상 / 비유**로서 드는 것이지, MAP-Elites의 계보로서가 아니다.
> 2. **메커니즘은 구조적으로 닮았을 뿐 동일하지 않다.** MAP-Elites의 골짜기 건너기는 **변이 오퍼레이터**가 자식을 새 셀에 두는 것으로 일어나며, **유전적 부동이 아니다**. archive는 복제하는 셀의 집단도 아니다.

##### 9.2 라이트 대 피셔 = 차원 (지형의 형태) 의 축

라이트와 동시대의 피셔 (R. A. Fisher, 1930) 는 반대를 주장: **큰 panmictic 집단 + 가법적 분산에의 매스 선택으로 충분**히 적응은 진행된다, 굳이 분할은 필요 없다, 고.

두 사람의 **가장 깊은 대립축은, 실은 「에피스타시스 (유전자 간 상호작용) 와 지형의 형태」** 였습니다. 라이트는 「비가법적 상호작용 때문에 지형은 **울퉁불퉁 다봉**, 그래서 골짜기를 건너는 drift가 필요」 라고 가정하고, 피셔는 「상호작용은 있지만 중요하지 않다, 지형은 거의 **단봉으로 매끄럽게 오를 수 있다**, 그래서 매스 선택으로 충분」 이라고 판단했다.

**이 epistasis/ruggedness의 축이, 바로 우리 결과가 살아 있는 차원입니다. 지형의 형태 (topology) 야말로 전 문제.** 지형이 정말로 울퉁불퉁 고차원이라면 (라이트 regime) 다양성이 골짜기를 건네주고, 매끄럽거나 난소가 저차원이라면 (피셔 regime) 매스 선택 ── 즉 **강한 랜덤 리스타트 산오르기의 생물학판** ── 으로 이미 충분. 우리의 ESN 텍스트 proxy는 noise-free로 매끄럽고, kernel union의 난소는 저차원 이산. **둘 다 피셔 regime**으로, ③은 효과가 없고 없었다.

> 세세한 주의 (정직하게): 「피셔는 drift를 무시했다」는 속설의 압축입니다. 정확히는 「drift는 있다고 인정했지만, 큰 집단에서는 양적으로 무시할 수 있다고 판단했다」. 완전 부정은 아니다.

##### 9.3 우리의 negative = 코인 비판의 계산판

가장 효과적인 대응은, 라이트의 **제안**이 아니라, 생물학계의 **경험적 판정** 쪽입니다. Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) 는 시프팅 밸런스 설을 이론・실증 양면에서 평가하고, 이렇게 결론지었습니다 (전문 대조 완료).

- **매스 선택으로 대개 충분.** 「라이트의 3단계 메커니즘이 단순한 매스 선택보다 더 잘 설명하는 실례는 거의 없다」. 인위 선택 실험도 「분할 집단의 선택이 대집단의 매스 선택보다 큰 응답을 낳는다」는 것을 보이지 못했다.
- **시프팅 밸런스가 효과를 내는 것은 한정적・희소한 조건 하에서만.** 집단 구조의 경험적 추정에서는 「**얕은 골짜기로 격리된 피크 사이에서만 drift는 이동을 일으킬 수 있다**」(깊은 골짜기는 drift로는 드물게만 건널 수 있다), 게다가 **대부분의 적응은 골짜기 건너기를 필요로 하지 않는다**.

이것은 우리 결과의 **놀랄 만큼 정확한 생물학판**입니다. 그들의 말을 우리의 어휘로 번역하면 ── **지형이 진정으로 기만적/고차원이 아니라면, 보통의 매스 선택 (≒ 강한 랜덤 리스타트 산오르기) 으로 이미 풀리고, 다양성 유지 장치는 거의 아무것도 사지 못한다.**「현실의 골짜기는 대개 얕다, 대부분의 적응은 골짜기 건너기 불필요」는, 우리의 「**실제 지형은 대개 단순하므로 niching은 잉여**」의 생물학적 언명입니다.

> **honesty 주의 (3점)**:
> 1. **그들은 시프팅 밸런스를 「반증」하지 않았다.** Phase I/II는 일어날 수 있다고 명언하고, 6건의 경험 사례도 들고 있다. 주장은 **더 좁은 확률적인 것** (「일반적・중요한 메커니즘이라 하기 어렵다」) 이지, 「refuted」 라고 쓰면 과언.
> 2. **논쟁은 아직 결착되지 않았다.** Wade & Goodnight (1998), Peck et al. (1998, 제목이 문자 그대로 「feasible」 이라 주장) 이 반론하고, Coyne 등의 2000년 재반론, Goodnight & Wade의 같은 호 반론으로 이어졌다. 1997 비판을 「최종 결론」으로 인용해서는 안 된다.
> 3. **생물에는 계산 측에 대응물이 없는 메커니즘이 있고, 게다가 우리보다 강한 주장을 하고 있다.** Phase III에서는, 다양성을 지키는 gene-flow 장벽이 **좋은 해를 주변 deme에 가둬 퍼짐을 방해한다** = niching이 **역효과**가 될 수 있다. 우리의 stateless한 이산 선택 설정에는 이 cost의 대응물이 없으므로, 여기는 **과도하게 겹치지 않는다**. 생물 쪽이 한 단계 강한 주장을 하는 곳입니다.

##### 9.4 두 실례 — 저차원의 나방, 그리고 고차원의 대장균

우리의 주장에는 2개의 극 (저차원 = ③ 불필요 / 고차원 = ③이 효과를 낼 수 있다) 이 있지만, 진화생물학은 각각에 깔끔한 실례를 갖고 있습니다.

**저차원의 극 ── 회색가지나방의 공업 흑화 (= BG9 kernel 케이스)**: *Biston betularia* 의 carbonaria (검정) vs typica (흰색) 는 **단일 멘델 좌위・소수 대립유전자** (원인 변이는 cortex 유전자로의 전이인자 삽입; van't Hof et al. 2011/2016) 로, **강한 방향성 선택** (s ≈ 0.1-0.2; Saccheri et al. 2008; 포식은 Cook, Grant, Saccheri & Mallet 2012에서 재확인) 을 받는다. 최적은 각 시점에서 단봉, 환경으로 시프트할 뿐. **단순한 방향성 선택 ── greedy 산오르기/랜덤 리스타트의 생물학판 ── 이 직접, 적자형(適者型) 을 고정하고, 다양성 유지 메커니즘은 필요 없고 불려지지도 않는다.** 이것이 바로 BG9: kernel 선택은 4지선다의 저차원 단일 좌표이고, RR이 전 kernel을 직접 샘플링하며, ③이 구조적으로 분리할 수 없다. **흑화형 = BG9 kernel 케이스의 생물판.**

> 주의 (정직하게): 이행기에는 다형(多型) 이 일시적으로 유지되지만, 그것은 **공간적 환경 불균일 + 유전자 흐름 (이주-선택 평형)** 에 의한 것이지, 내재적인 다양성 보존 메커니즘이 아니다. 비유가 조금 어긋나는 곳.

**고차원・역사 의존의 극 ── 렌스키의 Cit+ (= ③ regime)**: 대장균 장기 진화 실험 (LTEE) 에서, 호기적 시트르산 이용 (Cit+) 은 **12 집단 중 정확히 1개**에서 약 31,500세대째에 진화했다 (Blount, Borland & Lenski 2008). 열쇠는 순서를 갖춘 **potentiation (전구 변이의 축적) → actualization (citT의 탠덤 중복에 의한 프로모터 포획) → refinement** 라는 고차원・역사 의존의 경로 (Blount et al. 2012). 리플레이 실험이 「역사적 우발성」을 「일정률의 희귀 변이」에서 구별했다. 이것은 contingency・에피스타시스・고차원 울퉁불퉁 지형을 탐색하는 가치를 **진짜로 예시**한다 ── ③이 효과를 낼 수 있는 regime의 실례입니다.

> **honesty 주의 (이것은 우리 조건문의 "전건"에만 대응한다)**:
> - **LTEE는 niching 알고리즘을 쓰지 않는다.** 그냥 자연선택이고, 12 병렬 집단은 **그 자체가 랜덤 리스타트적인 설계**. 그래서 「contingency + 다양성이 희귀한 혁신을 가능케 한다」는 존재 증명이지, 「niching이 강한 restart baseline에 이긴다」는 증거가 **아니다**.
> - 「대장균이 제로에서 시트르산을 먹는 능력을 획득」은 속설의 과장. 혁신은 **제어 (기존 트랜스포터의 호기 발현) = exaptation** 이지, 신규 유전자도 신규 생화학도 아니다.
> - Van Hofwegen et al. (2016) 이 「직접 선택이라면 Cit+가 훨씬 빨리 나온다」고 보이고, 「희귀/우발」 틀에 이의를 제기했다 (렌스키 측은 LTEE 조건 하의 potentiation과는 모순되지 않는다고 반론). 「극히 희귀/장기 지연」 이야기에 기대려면, 이 **계쟁 중인 추시(追試)** 도 병기해야 한다.

##### 9.5 접지의 정리

| 극 | 생물학 | 지형 | ③은 효과? | 우리의 기질 |
|---|---|---|---|---|
| 저차원/매끄러움 | 흑화형 (단일 좌위, s≈0.1-0.2, 방향성) | 단봉・시프트 | **No** — 매스 선택으로 충분 | BG9 kernel union; ESN/ridge 텍스트 proxy (결정론・매끄러움) |
| 고차원/우발 | 렌스키 Cit+ (potentiation→actualization→refinement) | 울퉁불퉁・변이로 골짜기 넘기 | **Yes** (효과를 낼 수 있는 regime) | 합성 속임수 corridor (behavior = 24차원의 평균) |
| 경험적 판정 | 코인・바턴・투렐리: 매스 선택으로 대개 충분, 시프팅 밸런스는 드물게만 결정적 | 실제 지형은 대개 단순 | 우리의 **negative의 거울** | 시험한 모든 CPU 기질 |

**결론**: 라이트의 시프팅 밸런스는 「③이 효과를 낼 때 **왜** 효과를 내는가」의 올바른 생물학 선례, 라이트-피셔의 epistasis/ruggedness 축은 「**차원** 조건」의 올바른 틀, 흑화 나방과 렌스키 Cit+는 저차원/고차원의 깔끔한 양극, 코인 비판은 우리의 **negative**의 생물학 선례. **다만, 이것들은 계산 결과를 증명하지 않는다. 접지할 뿐.** 비유가 가장 느슨해지는 것은, 생물이 cost (Phase III의 gene-flow trap) 를 더하는 점 ── 우리의 stateless 설정에는 그것이 없다.

— 한 모금. 100년 전의 논쟁이 같은 형태라고 깨달았을 때는, 솔직히 소름이 돋았습니다. 다만 「소름이 돋았다」를 「증명」으로 헷갈리지 않는 것이 이번의 규율입니다. —

---

#### 10. GPU로의 함의 — 남은 길은 고차원뿐, 그러나 여전히 bet

arc는 CPU의 길을 전부 막았습니다. 실제 proxy는 noise-free로 매끄럽고 (IV), 마지막 후보 (kernel 다양화) 는 구조적으로 막혔다 (V). ③의 남은 길은 **고차원의 지형뿐** ── 그것을 제공하는 것이 **full-LLM의 파라미터/손실 공간 (수백만 차원)** 입니다.

구조적 통찰은 GPU의 도박을 **better-motivated** 하게 만듭니다. 「full-LLM만이 예외일지도」 라는 맹목적인 도박이 아니라, 「**③은 고차원을 요하고, full-LLM이 고차원역**」 이라는 원리에 따른 도박이 된다.

**다만 여전히 bet.** 생물학의 Cit+가 「③ 알고리즘의 승리」를 증명하지 않는 것과 같은 이유, 그리고 BG9에서 RR에 못 이긴 것과 동형의 이유로 ── **실제 LLM 지형이 backprop (경사 하강) 이라는 강 baseline으로 직접 내비게이트할 수 있다면, ③은 역시 불필요**. 난소가 고차원인 것은 **필요조건이지 충분조건이 아니다**. 「강한 직접법이 풀 수 없다」는 것을 추가로 보일 필요가 있다 (CPU에서는 RR, GPU에서는 경사 하강).

그래서 GPU는 「③을 위해 단독」이 아니라 **포트폴리오 판단** (llive의 실제 LLM fitness 등과 합승) + **클라우드 임차로 사전 등록 1건** (자본 커밋 전) 이 적정. go/no-go 기준도 falsifiable하게 쓸 수 있습니다:

> **full-LLM의 난소는 behavior에서 고차원인가, 또한 강한 직접 baseline (경사 하강) 으로 도달 곤란한가?** 고차원이라도 경사가 직접 닿는다면 ③ 불필요 (= BG9의 RR 결과의 GPU판).

---

#### 11. 메타 교훈 — 정직함은, 이기기 위한 도구였다

이 arc의 진정한 성과는 수치가 아니라, **「너무 정돈된 결과를 의심하는」 정신이 실제로 연구를 앞으로 진전시켰다**는 것입니다.

- **존재 증명 (I)** 에서 이겼을 때, 골짜기를 없앤 경계 실험으로 「③은 만능이 아니다」를 스스로 확인했다 (승리를 과대평가하지 않는다).
- **일반화 (III)** 에서 페어 리뷰가 3개의 rerun 블로커를 들이댔지만, 고쳐도 결론은 바뀌지 않았다 (취약한 negative가 아님을 확인).
- **결정론 측정 (IV)** 에서 평가 노이즈를 물리적으로 지웠기에, 「매끄러움」이 지형의 성질인지 계기의 한계인지를 가려낼 수 있었다.
- **BG9 (V)** 에서는 적대 검증으로 자신의 「③이 안 선다」를 **반증하려 해서 반증할 수 없었고**, 구조로서 확증되었다 (negative를 올바르게 negative로 확정하는 방향으로도 같은 규율이 효과를 발휘했다).

게다가 arc 전체에서 하나 배운 것은 ── **저차원의 난소는 강 baseline이 직접 풀어 버린다. 그래서 ③ (가려내어 길러 내는 공정) 이 효과를 내려면 "고차원 behavior 공간"이 필요하다.**「속임수 지형을 만들면 ③이 선다」는 절반만 옳고, 정확히는 「**직접 샘플링할 수 없을 만큼 고차원인** 속임수 지형」이 아니면 ③은 서지 않는다. 그리고 놀랍게도, 이 경계 조건은 **라이트의 시프팅 밸런스와 코인 비판이 100년 가까이 전에 도달해 있던** 것이었습니다.

「이상하게 좋은 결과가 나오면, 이긴 기분이 되기 전에 반드시 내역을 의심하라」── FullSense의 연구 규율 (`honest disclosure`) 은, 단순한 자계(自戒) 가 아니라, **실제로 거짓 양성을 잡고, negative를 올바르게 확정하며, 연구의 정밀도를 높이는 메커니즘**으로서 6단 전부에서 돌고 있었습니다.

결론을, 마지막에 다시 한 번, 정확하게.

> **③이 살아나는 것은 「고차원의」 속임수 지형일 때뿐.** 존재 증명 (합성 corridor) 에서는 압승했지만, 실제 CPU 기질은 ── 기억 과제 (바닥/천장) 도, 다중 과제 일반화 (매끄러움) 도, 실제 proxy 텍스트 지형 (noise-free로 매끄러움) 도, kernel 다양화 (저차원・구조적으로 막힘) 도 ── 어느 것도 그 조건을 충족하지 않았다. **「③ 결착 = ③은 불필요로 판명」이 아니라**, 「③이 살아나는 조건 (고차원의 속임수 지형) 을, 지금 CPU에서 측정할 수 있었던 실물 모형은 충족하지 않았다」. 본진 (GPU 고차원) 은 아직 앞이고, 게다가 「강한 직접 baseline이 푼다」는 리스크를 안은 도박입니다. 그리고 이 결론의 골격은, 20세기의 진화생물학이 이미 그리고 있었습니다 ── 다만 생물학은 그것을 **증명하는 것이 아니라, 접지할 뿐**입니다.

---

**Tags**: 진화계산 / MAP-Elites / 통계검정 / honest disclosure / 진화생물학 / CPU 연구
**관련**: 연재 #33 (제3축 ③ 결착 Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (반증・Goodhart・proxy 한계)
**Project**: llcore (PyPI 예약 llmesh-llcore, 리포지토리 미공개이므로 로컬 연구)


<!-- REFERRAL -->

---

> ### ⚡ この連載は Claude Code と二人三脚で書いています
>
> 記事中の実装・検証・可視化は **Claude Code**(Anthropic の AI コーディング環境)と一緒に進めています。
> Claude Code は **1 週間の無料トライアル**で試せます。気に入って有料プランに登録される際、
> 下の紹介リンク経由だと筆者に「開発を続けるためのクレジット」が入り、この連載の継続を後押しできます。
>
> 👉 **無料で試す / 紹介リンク** → https://claude.ai/referral/0sqPw8E_lw
>
> <sub>EN: This series is built together with **Claude Code** — try it with a **1-week free trial**. If you subscribe via the link, the author receives credits to keep building. /
> 中文: 本系列与 **Claude Code** 协作完成,可享 **1 周免费试用**;通过链接注册可让作者获得继续开发的额度。 /
> 한국어: 이 시리즈는 **Claude Code**와 함께 작성합니다 — **1주 무료 체험** 제공. 링크로 가입하면 저자가 개발 지속용 크레딧을 받습니다.</sub>

<!-- /REFERRAL -->

<!-- CTAIMG -->

![「ひくわ」と一万円札を差し出す森田](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/012.jpg)
> 🗒️ *「ひくわ」— 紹介リンクで小銭を稼ごうとする魂胆、我ながらちょっと引く*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

<!-- /CTAIMG -->
