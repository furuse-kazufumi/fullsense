---
project_group: llive
title: lldarwin / 進化 arc 総集編
tags: 解説, 進化計算, llive, FullSense, honest_disclosure
private: false
public_id: 6e107c7dfa0c261ee4d7
---

# lldarwin / 進化 arc 総集編

## 目次

1. [AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin](#第1章-ai-を-500-世代進化させたら世界に私と予測符号化の父カールフリストンだけが残った-25--monoculture-の-honest-disclosure-と選択圧コンポーネント-lldarwin)
2. [「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26](#第2章-眼鏡で測るだけでは進化しない--選択圧コンポーネント-lldarwin-の設計と実測-26)
3. [一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27](#第3章-一晩で-ai-進化を作り直した--実-llm-12h-ランがまた満点で飽和し6-本の-poc-と-4-体の-agent-と-perplexity-が独立に同じ結論へ収束した夜-27)
4. [進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28](#第4章-進化し続ける-ai-集団を指揮者が合奏させて答える--llive-のオーケストラ型進化と飽和を治した-3-つの仕掛け-28)
5. [「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #29](#第5章-眼鏡が飽和すると選択圧は無力-進化設計を反証で鍛える-29)
6. [進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで](#第6章-進化を見せる技術の系譜-30--conway-のライフゲームから-3dgs-まで)
7. [AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制](#第7章-ai-に-ai-を部下として使わせる-31--claude-主導--codex-配下の二本柱開発体制)
8. [(連載 #32) llcore CPU PoC battery 完成](#第8章-連載-32-llcore-cpu-poc-battery-完成)
9. [(連載 #33) 整いすぎた結果は、勝ちではなく警報 — 第三軸 ③ を proper power で決着させた一日](#第9章-連載-33-整いすぎた結果は勝ちではなく警報--第三軸-③-を-proper-power-で決着させた一日)
10. [(連載 #34) 山登り 6 連戦で分かった「いつ進化の③は効くのか」— そして 100 年前の進化生物学が同じ答えを出していた](#第10章-連載-34-山登り-6-連戦で分かったいつ進化の③は効くのか-そして-100-年前の進化生物学が同じ答えを出していた)


---

## 第1章 AI を 500 世代進化させたら、世界に「私」と「予測符号化の父カール・フリストン」だけが残った #25 — monoculture の honest disclosure と選択圧コンポーネント lldarwin

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> ざっくり言うと、AI 集団を 8 人の天才の「思考のクセ」を種にして 500 世代も進化させたのに、生き残ったのは著者とフリストンの 2 人だけ、という大失敗の記録です。一見「予測符号化が最強だった!」という感動譚に見えますが、真相は逆。テストが全員 100 点になってしまい(満点インフレ)、誰を選んでも差がつかず、進化はただの「あみだくじ」に成り下がっていました。たとえるなら、全員満点のクラスで学級委員を選挙したら票が割れて 2 人に絞られた、というだけの話。原因は評価関数(成績をつける眼鏡)が壊れていたことで、そこから「測る」の次に「淘汰する」専門の道具 lldarwin が要る、と気づくまでが本章です。
<!-- KAMI -->

:::note info
**📚 FullSense ナレッジベースのご案内** <!-- fullsense-team-kb -->
FullSense 開発全史 60+ 記事 (4 言語版・物語ベースの読む順ガイド・かみくだき版・4 コマ漫画つき) は Qiita Team **FullSense KB** に集約しています (チームメンバー向け)。
:::



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

### 0. 三行であらすじ（落語でいう「枕」）

- **やったこと**: llive の派生集団進化に 8 人の知性をペルソナ種として投入、rich-proxy 評価で 500 世代回した。
- **起きたこと**: 1 世代目で best_score が **1.0 に張り付き**、以降ずっと満点。8 系統が **古瀬 52% / フリストン 48%** の 2 系統に収束、残り 6 人が絶滅。
- **真因**: 「満点が出続けた」＝**選択圧がゼロ**。誰を選んでも fitness は同じだから、進化は実質サイコロ振り（遺伝的浮動）になっていた。

要するに **「全員 100 点のテストで席次を決めようとした」**。そりゃ誰が
受かるかはくじ引きになります。テストが悪い。眼鏡(lleval)が曇っていた。

---

### 1. なぜ「人物」を種として蒔いたのか

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

### 2. 結果 — 生き残ったのは 2 人だけ

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


![「頭使えよ」と拳を握る明美](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/089.jpg)
> 🗒️ *「頭使えよ」— 生き残った2人が賢いわけではない(drift で残っただけ)の自虐*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

---

### 3. 真因 — 「満点インフレ」が選択圧を消した

#### 3.1 症状: best_score が 1 世代目から 1.0

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

#### 3.2 根本原因: 評価関数 `fitness_rich` の二重の潰れ

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

<!-- TOPICNAV -->
> **🌐 言語**: **日本語** | [English](https://qiita.com/furuse-kazufumi/items/e49b7ab9027d93594402) | [中文](https://qiita.com/furuse-kazufumi/items/93f3cf1bb7b14650bbca) | [한국어](https://qiita.com/furuse-kazufumi/items/951b94cf66d246723004)
>
> **📚 FullSense 総集編シリーズ**
> - [llcore 検証 arc 総集編](https://qiita.com/furuse-kazufumi/items/cc0713ab78a5b390df76)
> - **lldarwin / 進化 arc 総集編（この記事）**
> - [llive 完全解説 総集編](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
> - [llmesh 総集編](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762)
> - [かみくだき総集編](https://qiita.com/furuse-kazufumi/items/bfb20aca3cf1df510c26)
<!-- /TOPICNAV -->


![呆れる明美](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/160.jpg)
> 🗒️ *「思い込みが激しいわねぇ…」— 「予測符号化が最強」と言いたくなる確信過剰を冷ます*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

---

### 4. 対策 — 「測る」の次は「淘汰する」: lldarwin

llive ファミリーには既に **lleval（眼鏡 = 評価フレームワーク, 連載 #24-08）**が
あります。今回わかったのは、**眼鏡で差を「測れた」としても、その差を
「誰が生き残るか」に正しく変換しないと進化は壊れる**ということ。

そこで新メンバー **lldarwin（選択圧 = 淘汰コンポーネント）**を設計しました。
ll- ファミリーの役割分担はこうなります:

```
lleval   = 測る  （個体の振る舞いを複数軸の pressure profile に変換）
lldarwin = 淘汰する（その profile を「次世代の親」に変換）
```

#### 4.1 設計の核 — 「集約しない」選択圧

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

#### 4.2 「LLM の苦手」を選択圧にする

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

#### 4.3 全滅をモニタする — SPC アラーム

FullSense の中核思想は **SPC（統計的工程管理）**。lldarwin でも
`max_lineage_share` / archive 成長 / behavioral diversity を毎世代記録し、
**monoculture 比 > 0.8 を SPC_ALARM で検知**して cadence やパラメータを
自動調整します。今回の「8→2」を、構造的に再発不可能にするのが目標です。

---

### 5. 教訓（honest disclosure として残す）

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

### 5.5. 「眼鏡」と「淘汰器」の 2 段構造 — なぜ分けるのか（深掘り）

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

### 5.6. 図解アイデア（投稿前に SVG 化する候補）

本記事を「動きで魅せる」ために用意したい図（投稿前 SVG 化）:

1. **系統占有率の崩壊アニメ** — 世代軸で 8 系統の帯が 2 系統に吸い込まれる animated SVG（金魚の池メタファ）。
2. **best_score = 1.0 即飽和グラフ** — 第 1 世代で天井に張り付く平坦線（選択圧ゼロを一目で）。
3. **argmax 潰しの図** — 複数軸ベクトル `[典型性, 多様性, 専門性, ...]` が `max()` で 1 本の棒に潰れる before/after。
4. **2 段構造図** — §5.5 の「眼鏡 → 淘汰器」を hero 図として animated 化。
5. **ll- ファミリー役割図** — lleval（測る）/ lldarwin（淘汰する）/ llive（個体）の関係を 1 枚で。

> これらは [[project_fullsense_animemd_branch_token_viz]] の animated SVG 表現層（宣言アニメ → SMIL）に乗せる予定。

---

### 6. 関連

- 連載 #24-05「集団が学ぶ AI」— 派生集団進化の総括（本記事の前提）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #26「lldarwin の設計」— 淘汰器の多目的淘汰 / ε-lexicase / QD（本記事の続き）
- 連載 #27「眼鏡が曇ると淘汰も無力」— 反証調査・Goodhart's law（honest disclosure）
- 設計書: lldarwin（淘汰する側）— 本記事の元ネタ
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #24-05・#24-08・#26・#27 の Qiita URL cross-link -->

---

---

## 第2章 「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> 前章で「眼鏡(評価)が壊れていた」と分かったので、本章では新しい淘汰の道具 lldarwin を設計し、実際に動かします。覚えるキーワードはたった一つ、「集約しない」。複数の物差しの点数を 1 本に足し算した瞬間、数学だけ満点の天才のような「尖った個体」が平均点の優等生に負けて消えてしまうからです。そこで軸を 1 つずつ別々に見る ε-lexicase などを束ねて尖った奴を救い、さらに「絶滅した系統を毎世代こっそり蘇らせる中立貯蔵庫」を足したら、岡潔もグロタンディークも全員復活しました。最後は本物の on-prem LLM を相手に、prompt 戦略を進化させて苦手タスクを 0 点から満点に改善させた、という実測まで届きます。
<!-- KAMI -->

:::note info
**📚 FullSense ナレッジベースのご案内** <!-- fullsense-team-kb -->
FullSense 開発全史 60+ 記事 (4 言語版・物語ベースの読む順ガイド・かみくだき版・4 コマ漫画つき) は Qiita Team **FullSense KB** に集約しています (チームメンバー向け)。
:::



> **コンセプト hook**: 前作 #25 で、私は「AI を 500 世代進化させたら、世界に**私とフリストンだけ**が残った」という大失敗を晒しました。
> 岡潔もグロタンディークもフォン・ノイマンも、全員、進化の途中で静かに消えていった。原因は、評価関数（眼鏡 = lleval）が満点を出し続けて、**選択圧がゼロになった**こと。誰が優れているか「測れて」いても、その差を「誰が生き残るか」に変換できなければ、進化はただの遺伝的浮動に堕ちる。
>
> では——眼鏡で差を「測れた」として、その差を「淘汰」に**正しく変換する装置**はどう作るのか。
> それが今回の主役、**lldarwin**。ll- ファミリーの新メンバーで、**淘汰（選択圧）専門**のコンポーネントです。
>
> この記事で覚えてほしいキーワードは、たった一語。**「集約しない」**。複数の物差しを 1 本に足し算した瞬間、進化は壊れます。なぜそうなるのか、そしてどう実測でそれを乗り越えたのか——失敗の続きから、今度は**実際に動いた**話をします。

---

### 0. 三行であらすじ（落語の「枕」）

落語には本題の前に「枕」があります。まずは三行で全体像を。

- **lleval が測り、lldarwin が淘汰する** — 進化は「測る」と「淘汰する」の 2 段構えで、初めて意味を持つ。
- 淘汰の第一原則は、**複数の選択圧を集約しない多目的淘汰**。#25 の失敗（単一スカラーの argmax で潰した）の真因を、ここで構造的に断つ。
- 採用三本柱 = **ε-lexicase + minimal-criterion QD + down-sampling**（evolutionary_computation コーパス 616 件を横断して選定）。

そして今回は骨子だけでなく、**実測がある**のが #25 との違いです。novelty pressure で行動多様性を 7.12 → 14.88（+109%）に倍増させ、**中立貯蔵庫**で「絶滅した岡潔・グロタンディーク系統」を実際に**全員復活**させ、最後は **on-prem の本物の LLM（llama3.2）**を相手に、prompt 戦略を進化させて苦手タスクを 0.0 → 1.0 に改善させた。順を追って見ていきます。

---

### 1. なぜ「測る」と「淘汰する」を分けるのか

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

### 2. 設計の核 — 「集約しない」7 ステージ

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

### 3. なぜこの 3 本柱なのか（rad-research の裏付け）

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

### 4. Stage1 — criteria 除外 + novelty pressure で行動多様性を倍にする

ここから実測です。Stage1 では、設計をいきなり全部実装するのではなく、最も効きそうな 2 つの変更だけを入れて測りました（llive, branch `optimize/core-2026-05-20`、commit `8060204`）。

**変更 1: criteria 除外。** ε-lexicase の case から、`factor_score`（= max-archetype の単一スカラー = argmax、まさに #25 の best=1.0 飽和の真因）と `nearest_persona_idx`（= 順序に意味のないカテゴリ index）を外しました。これは「悪い物差しを淘汰の判断材料から除く」掃除です。

**変更 2: novelty pressure。** `MultiPressureSelector(use_novelty=True)` を有効化。毎世代、過去世代の archive との k-NN 平均距離（Lehman-Stanley 流の novelty）を計算し、それを集団内で z-score 化（STD-1）して、追加の lexicase case として淘汰に混ぜます。「みんなと違う振る舞いをしている」こと自体を、軸の 1 つとして評価する。

テストは `tests/unit/test_evolutionary_lldarwin.py` を 8 → 10 件に拡張（除外・novelty 保存を追加）。進化系 847 件 green、回帰なし。

実測条件は rich-proxy、8 founders + pop24、150 世代、seed 0。結果が以下です。

#### 4.1 行動多様性 (diversity_l2) — novelty が効く指標

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

### 5. honest disclosure（最重要）— 行動多様性と系統生存を私は混同していた

ここが本記事で一番大事な節です。良い数字（+109%）が出たからといって、勝った気にならない——これは私の鉄則（[[feedback_benchmark_honest_disclosure]]）です。内訳を疑いました。そして、間違いを見つけました。

#### 5.1 系統固定 (founder_counts) — novelty では改善しない指標

同じ実測で、別の指標を見ます。「8 人の founder（祖先系統）のうち、何系統が最後まで生き残ったか」。

結果は——**全条件で最終的に 8 → 2 系統**（furuse-kazufumi + friston）に収束。oka-kiyoshi（岡潔）/ grothendieck（グロタンディーク）/ von-neumann / feynman / millidge / isomura は、**全部絶滅**。

novelty を入れて行動多様性を倍にしたのに、**系統の生き残りは #25 とまったく同じ 2 系統**だったのです。

#### 5.2 なぜか — 私は 2 つの「多様性」を混同していた

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

### 6. Stage1.5 — 中立貯蔵庫で絶滅した系統を蘇らせる

病気の正体がわかれば、薬を変えられます。系統生存に必要なのは「絶滅した系統を毎世代 re-inject する機構」——**lineage-niched 中立貯蔵庫（reservoir）**です。

#### 6.1 まず PoC で機構を確かめる

いきなり本番ループを改造せず、まず standalone PoC で機構が回ることを確かめました（[[feedback_poc_feasibility_first]] = 要件 → PoC → フィジビリティ → 詳細設計、llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`）。

selection は Stage1 の `MultiPressureSelector`（criteria 除外 + novelty）を流用。fitness は rich-proxy。系統は parent_a から継承。**reservoir = 系統別の best-ever genome を保持し、絶滅した系統を毎世代 re-inject する**（低 score の子を置き換える。best は壊さない）。8 founders + pop24 + 150 gens + seed 0 で測りました。

| reservoir | 最終 named 系統 | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1**（oka-kiyoshi 24/24 = 完全 monoculture） | 1.00 | 1.58 |
| **ON** | **8（全 founder 生存）** | **0.31（≪ 0.8 OE-3）** | 1.69 |

reservoir ON で、岡潔（oka）・グロタンディーク（grothendieck）を含む**全 8 系統が生存**。最終 shares は friston 7 / furuse 6 / grothendieck 4 / oka 3 / 他 4 系統各 1。**強い系統は子孫を持って繁殖し、弱い系統は貯蔵庫が生命維持する**という、理想的な挙動です。行動多様性も低下なし（1.69 vs OFF 1.58）。

**Honest 留保（PoC 段階）**: 貯蔵庫は frozen elite（凍結された代表）を再投入するので、弱系統（各 1 体）の「生存」は再投入由来であって、能動的進化ではありません。これは中立貯蔵庫の定義どおり（代表を保持し、再結合可能にする）で正当ですが、「弱系統が活発に進化し続ける」とは主張しません。

#### 6.2 本番 EvolutionLoop へ組込（additive + default-off）

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

#### 6.3 Honest 留保 — 系統保持と行動多様性は弱いトレードオフ

reservoir ON で系統は全員生き残りました。が、よく見ると **diversity_l2 は 14.88 → 9.20 に低下**しています。frozen elite（凍結代表）を毎世代再投入するぶん、genome 空間の広がりがやや減るのです。

ただし、OFF 時の崩壊（final 0.83）は回避しています。つまり「系統保持を取ると、行動多様性のピークは少し下がるが、崩壊は防げる」という**弱いトレードオフ**の関係です。代償ゼロの魔法ではない。これを正直に書いておきます。そして、この代償をどこまで小さくできるかが、次の sweep の主題になります。

---

### 7. 再投入頻度 sweep — 非単調な最適点という非自明な発見

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

### 8. Stage2 前半 — 「LLM の苦手」を proxy で選択圧にする

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

### 9. Stage2 後半 — 本物の on-prem LLM を相手に prompt 戦略を進化させる

localhost の ollama（llama3.2:latest 等）が到達可能とわかったので、ついに**実 LLM 評価**が可能になりました（commit `2fb2912`）。localhost = on-prem なので、measurement purity（測定純度。cloud LLM と混在させない）の規律も満たします（[[feedback_llive_measurement_purity]]）。

#### 9.1 個体 → 実 LLM への写像（Promptbreeder 系）

肝は「genome を、どうやって実 LLM に効かせるか」です。`real_pressures.py` で **個体 → 実 LLM 写像**を実装しました。

- **個体の `c_prompt`（PromptChromosome）を system prompt に変換**: skill_set → 指示文 / prompt_template_id → 推論スタイル / language_style → 語調。固定の LLM（llama3.2）にこの system prompt を被せ、5 苦手軸の**実タスク**を解かせて採点します。
- **LLM 本体は固定し、prompt 戦略（genome）を進化させる** = 「どの prompt 戦略が LLM の弱点を緩和するか」を実測で淘汰する。これは Promptbreeder（prompt を進化的に最適化する研究系列）の流儀です。
- temp=0（greedy）で決定論的に。`(system_prompt, task)` をキャッシュ（同一戦略は再評価しない）。
- robust: per-call try/except（ollama の hiccup は task の失点として扱い、走行は継続）。
- `--fitness real-pressure` / `--ollama-model` / `--max-wallclock-seconds` を追加。tests 5 件 + 進化系 947 green。

#### 9.2 実選択信号の実証 — CoT+structure 戦略が multistep を 0.0 → 1.0 に

そして、本物の選択信号が観測できました。

**CoT+structure 戦略**（`chain_of_thought` + structurize + loop）が、llama3.2 の **multistep（多段推論）を 0.0 → 1.0 に改善**しました（terse な戦略は 0.0 で失敗。score は 0.80 → 1.00 に上昇）。

これは、lldarwin の主張「prompt 戦略の進化で LLM の弱点を緩和できる」を、**proxy ではなく実 LLM で実証**したことを意味します。同じ llama3.2 本体でも、被せる system prompt（= 進化した genome）次第で、多段推論タスクが解けたり解けなかったりする。進化は「解ける prompt 戦略」を実際に選び取ったのです。

![5 苦手軸の母集団平均推移（実 on-prem LLM llama3.2 評価）。prompt 戦略の進化で軸が改善する](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

#### 9.3 12h 連続ラン

実 LLM 評価は重いので、長時間の連続ランを起動しました（`out/lldarwin_12h_realpressure_2026_05_26/`）。

```
--fitness real-pressure --selection lldarwin --novelty --lineage-reservoir
--genome3d --population 24 --max-wallclock-seconds 43200 --checkpoint-every 5
```

wallclock 12h で safely 停止（snapshot 済 → `--resume` で継続可能）。連続ランの中で best_score=1.0 に到達しています。

![実 LLM 進化ランの適応度と多様性（12h 連続ラン）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status.svg)

#### 9.4 Honest 留保（実 LLM 評価の限界）

ここが #25 から学んだ姿勢の総決算です。派手な結果（0.0 → 1.0、best 1.0）が出たからこそ、内訳を徹底的に正直に書きます。

- **(a) fitness に関与するのは `c_prompt` だけ。** persona / c_factors は中立（系統は reservoir で維持、初期選択は novelty が担う）。つまりこれは「**prompt 戦略の進化**」であって「persona の進化」ではありません。岡潔の人格が賢くなったのではなく、岡潔という系統に紐づいた prompt 戦略が選ばれた、という話。
- **(b) 全 founder の初期 c_prompt は同一（default）。** だから探索は mutation 駆動です（founder ごとに prompt を多様化させるのは今後の改善）。スタート地点が同じなので、初期の系統差は prompt 戦略には効いていない。
- **(c) 小バッテリ（軸あたり 2 問）= ノイジーな推定。** 0.0 → 1.0 という劇的な数字も、問題数が少ないぶんノイズを含みます。統計的に堅牢な主張をするには、もっと大きなバッテリが要る。
- **(d) on-prem only（measurement purity）。一般能力の主張ではない。** llama3.2 という特定モデル・特定タスクでの観測であって、「LLM 一般がこうなる」とは言いません。

これらを伏せれば「進化で LLM が劇的に賢くなった!」という派手な物語が書けますが、それは嘘です。lldarwin が実証したのは「**機構が、実 LLM 上で、選択信号を生む**」というところまで。その線を越えた主張はしません。

> 🍵 **休憩ポイント**: 研究で一番気持ちいいのは「0.0 が 1.0 になった!」と叫ぶ瞬間です。でも、その瞬間こそ [[feedback_benchmark_honest_disclosure]] が効いてくる。「変に良い数字が出たら、勝った気になる前に内訳を疑え」。今回でいえば——勝ったのは「prompt 戦略」であって「LLM 本体」でも「persona」でもない。問題数も少ない。on-prem の 1 モデルだけ。これを全部書いてから、初めて「実証した」と言える。honest disclosure は、自慢を我慢する筋トレです。

---

### 10. 既存資産の再利用（codex コード調査ベース）

設計を絵に描いた餅にしないため、配下の Codex に既存コードを調査させたところ、**多くは実装済・未配線**でした。

- `mating.py:139 LexicaseSelection`（ε 付き、実装済だが未配線 → 配線するだけ）
- `nsga2.py:197 NSGA2Selection`（≤3 目的レーン用）
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**新規実装**: `Standardizer` / `MinimalCriterionGate` / `Pressure` 群 / `MultiPressureSelector`（中核）/ `LineageReservoir`（Stage1.5）/ `SelectionAudit`。
**配線点**: `loop.py:122` の `selection` に `MultiPressureSelector` を注入、`persona_evolution.py:606` に注入口を追加、`EvolutionLoop.on_population_bred` hook に `LineageReservoir` を接続。

> 🍵 **休憩ポイント**: 「実装済だが未配線」が一番多かったのが、最大の教訓でした。良い部品を作っても、**配線（オーケストレーション）しなければ進化は壊れたまま**。#25 で 8→2 になったのは、ε-lexicase も NoveltyScorer も QD も「箱の中にあったのに、配線されていなかった」から。lldarwin の本質は、新規アルゴリズムの発明よりも、「既存の良い部品を**集約せず**束ねて、進化ループに**実際に配線する**こと」にあります。電子部品を全部揃えても、半田付けしなければラジオは鳴らない。

---

### 11. 破綻回避の保証 — 全滅しない多層構造（実測で裏付け済）

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

### 12. honest disclosure / リスク（前振り）

設計を盲信しません。受容済みの限界（次作 #27 で深掘り）を、もう一度まとめておきます。

- **Goodhart's law / proxy 乖離** — LLM 弱点を proxy fitness にすると、「指標をハックする表面戦略」が進化する（typo → 特定置換の暗記、WSD → テストのヒューリスティクス利用、等）。proxy は mechanism feasibility に限定し、production 能力を主張しない。
- **設計者依存性** — lexicase=case / QD=記述子 / novelty=距離尺度、いずれも「多様性の方向」を設計者が決める。生物進化級の未想定創発は限定的。
- **minimal-criterion の停滞⇄崩壊トレードオフ** / **QD の次元の呪い + アーカイブ飽和**。
- **実 LLM 評価の限界（§9.4 再掲）** — c_prompt のみ fitness 関与・founder 初期 prompt 同一・小バッテリ・on-prem only。

> **次回予告（#27）**: 「眼鏡が飽和すると選択圧は無力」という最も痛い反証を、Goodhart's law と proxy fitness の限界とともに正直に晒します。lldarwin は万能ではない。**どこまで主張してよいか**の線引きが #27 の主題です。今回「8/8 生存」「0.0→1.0」という良い数字が出たからこそ、次は徹底的に反証で鍛えます。

---

### 13. 結論

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

### 14. 関連

- 連載 #25「私とフリストンだけが残った」— 本記事の動機（失敗の記録）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #27「眼鏡が曇ると淘汰も無力」— 反証調査（honest disclosure）
- 設計書: lldarwin（淘汰する側）`docs/vision/LLDARWIN_DESIGN.md`
- 実測正本: `docs/research/lldarwin_stage1_results_2026_05_26.md`
- llive commits: Stage1=`8060204` / 中立貯蔵庫 PoC=`0d0537d` / Stage1.5=`b03cbda` / reinject sweep=`da93dd3` / Stage2 実 LLM=`2fb2912`
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]] / [[feedback_poc_feasibility_first]]

---


<!-- INTERLUDE -->

### ☕ 閑話休題 — AI が黙る夜 — llterm 開発の楽屋話

本筋から少し離れて、著者の手元で進む別の道具の話を一つ。Claude Code を走らせるための専用ターミナル llterm を自作しているのですが、これがなかなか一筋縄ではいきません。一番ヒヤッとしたのは「AI が突然、黙る」バグでした。長く自走させていると、あるターンを境にぴたりと応答が止まる。落語のオチで客が静まり返るのとは違って、こちらは演者(AI)が無言で固まってしまうので、舞台監督(人間)は冷や汗をかきます。原因は地味で、ターンの境目で渡すべき「指示の一言」が処理の隙間にこぼれ落ち、AI が次に何をすべきか分からなくなっていた、というものでした。

もう一つの楽屋話がカーソルの取り合いです。AI の出力を描く処理と、人間がキー入力する処理が同じ画面のカーソルを奪い合い、文字が変な場所に化ける。さらに日本語入力(IME)が絡むと、変換中の未確定文字まで巻き込まれて表示がぐちゃぐちゃに。こうした「画面の中の小競り合い」は、進化や淘汰といった本記事の華やかな主題とは縁遠い、地味で泥臭い仕事です。でも、AI に長時間まっとうに働いてもらうには、こういう舞台裏の配管が静かに効いている——というのは、本筋の lldarwin が『派手な数字より地味な配線』を大事にするのと、どこか似た話かもしれません。

<!-- INTERLUDE -->



---

## 第3章 一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> 今度こそ本物の LLM(llama3.2)で 12 時間ぶっ通し進化させたら——また 5 世代目で満点に張り付き、65 世代ピクリとも伸びませんでした。つまり「ふるいの付いたランダム探索」で、本物の LLM でもまだ進化になっていなかった。そこで著者は一晩、自分で 6 本の小実験(PoC)を回し、別働の AI を 4 体並列で走らせ、Perplexity に文献を漁らせて「方策を決め」ました。すると朝、全員が独立に同じ結論——「淘汰器をいくら磨いてもムダ。評価(ものさし)そのものを開放端化(満点で止まらない仕組みに)せよ」——にたどり着いていた。別々の道で同じ答えに着いたからこそ信用できる、という徹夜の意思決定ログです。
<!-- KAMI -->

:::note info
**📚 FullSense ナレッジベースのご案内** <!-- fullsense-team-kb -->
FullSense 開発全史 60+ 記事 (4 言語版・物語ベースの読む順ガイド・かみくだき版・4 コマ漫画つき) は Qiita Team **FullSense KB** に集約しています (チームメンバー向け)。
:::



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

### 0. 三行であらすじ（落語でいう「枕」）

落語には本題の前に「枕」があります。まずは三行で。

- **また飽和した** — 実 LLM(llama3.2) で 12h 回したら、gen5 で best=1.0 に張り付き、65 世代無進歩。全滅はしないが累積もしない＝**filtered random search**。真因は #25 と同じ「固定の人手ものさしの飽和」。
- **一晩で方策を決めた** — 自己 PoC 6 本 + 並列 Agent 4 体 + Perplexity が、**独立に同じ結論**へ収束。「ものさしを固定したまま淘汰器を磨いても無駄。**評価そのものを開放端化せよ**」。
- **独自性が見えた** — 連続進化する集団を、止めずに任意の瞬間に合奏（MoA）させて 1 答する「**ライブ・オーケストラ**」が、先行研究の white-space（空白地帯）だと判明した。

要するに **「眼鏡（評価）が飽和したら、淘汰器（lldarwin）をどれだけ磨いても無力」**。
だから磨く対象を変える——**評価そのものを開放端にする**、が今回の結論です。

---

### 1. なぜ「また」やったのか — #25 / #26(設計) の続き

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

### 2. 出発点 — 実 LLM 12h ランの「正直な不合格」

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

### 3. 一晩の作戦 — 「方策を決める」ための分散調査

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

### 4. 最初の決定打 — 「固定ものさし」を捨てるか（自己 PoC #1 / #2）

最初に潰すべき仮説は、いちばん根っこの問いでした。**「ものさしを固定難易度から適応難易度に変えれば、飽和は直るのか?」**

#### 4.1 自己 PoC #1 — 適応難易度は飽和を直す。が、多様性を殺す

合成の competence ベクトルを使った proxy で、交絡を除去して（elite を score 基準で選ぶ）比較しました。

- **baseline（固定難易度）**: 能力 **0.627 で低位停滞**（best 0.757）。12h の病理を proxy で再現。
- **adaptive（難易度 = 集団 60 分位に追従）**: 能力 **0.952 へ上昇**（best 1.0）。

難易度を集団に追従させる（できる問題が増えたら問題を難しくする）と、飽和が解けて能力が伸びた。**だが**——adaptive は**多様性を犠牲**にしました（diversity 0.310 → 0.134 に崩壊）。難しい問題に最適化する過程で、集団が 1 つの正解戦略に凝集してしまう。

#### 4.2 自己 PoC #2 — 適応難易度 × novelty は両立する

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

### 5. 本丸の証拠 — 開放端進化の 1 万世代 sweep（Agent A）

自己 PoC で「方向」は見えました。次は、それを**大規模に・厳密に**叩く番です。並列 Agent A に、**各 1 万世代 × pop256 × 19 構成 × 2 巡**の開放端 sweep を回させました。

判定基準は「open-ended（開放端）かどうか」——**飽和せず、monoculture（単一文化への収束）を避け、archive（多様性の貯蔵）が成長し続けるか**。

#### 5.1 決定的な判定表

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

#### 5.2 Agent A が出してくれた「正直な限界」

良い結果（open-ended 成立）が出たときこそ、限界を書く。Agent A 自身が、こう指摘してきました。

> novelty/lexicase は記述子**全体**の多様性は保つが、**特定の意味次元（factor）の多様性は保証しない**。
> 大きな latent では factor drift が起き、fspread（factor の広がり）が要監視。

つまり「全体としては多様」でも「思考因子という特定の意味次元では収束している」ことがありうる。これは新しい要件 **factor-subspace QD（意味次元を個別に保護する QD）** を生みました（後述の PoC #6 で対処）。

> 🍵 **休憩ポイント**: ここが本記事のいちばん硬い節です。持ち帰ってほしいのは 1 行——
> **「archive（貯蔵庫）を足すだけでは救えない。選択圧そのものを開放端にしないと駄目」**。
> #25/#26 設計編で「集約しない」と言ってきましたが、その本丸が「**選択の仕方を開放端化する**」
> ことだった、と 1 万世代の実データが言い切ってくれた。ここを越えたら、あとは独自性の話です。

---

### 6. 独自性の核 — 「連続進化する集団を、止めずに合奏させる」

ここまでで「飽和を構造的に避ける選択核（S1）」が固まりました。次は、ユーザーが対話で示した**独自性 3 軸**を、PoC と文献で裏付ける番です。

ユーザーが言語化した 3 軸は、これでした。

1. **連続進化集団 = ライブ・オーケストラ（ORCH）** — 進化し続ける集団が、その場で MoA（Mixture-of-Agents）集約して 1 答する。進化を止めない。**最大の差別化候補。**
2. **調査機能を持つ個体（AGENT）** — 個体が自分で調べに行く。Voyager 系。
3. **観測・対話制御（OBS）** — 個体別の応答 + 選択スコアの時系列を見て、止めて、再開できる。

#### 6.1 Perplexity が裏付けた white-space

並列で走らせた Perplexity の SOTA サーベイ（1143 行）が、最重要の裏付けを返してきました。

> 「**online evolution + online answering を統合した連続稼働システム**」は、明確な先行研究なし
> ＝ **research white-space（空白地帯）**。近接は MoA / Self-MoA / sequential aggregation / routing
> だが、同一物はない。

つまり「進化を止めて、できあがった最強個体で答える」のは普通。「進化を**止めずに**、進化中の集団をそのまま合奏させて答える」のは、誰もまだやっていない。**ORCH §1.11 の差別化が確定**しました。

#### 6.2 ただし Perplexity は反証警告もくれた

honest disclosure として、Perplexity がくれた**反証警告**も同じ重みで書きます。

> 2025 年の **Self-MoA 研究**では、**多様性は自動的に優位ではない**。単一トップモデルの反復が、
> 異種混合 MoA を AlpacaEval で 6.6% 上回った（quality-diversity トレードオフ）。

「集団を合奏させれば単一個体より強い」は、**自明ではない**。むしろ多様性が逆効果になる場合がある、と先行研究が警告している。だから ORCH は「実測で証明せよ、pass-bar を正直に」。これを Agent C と自己 PoC #3/#4 で検証しました。

> 🍵 **休憩ポイント**: ここ、研究の誠実さが試される分岐点です。「online 進化 + online 回答は
> white-space！独自性！」で舞い上がりたいところに、Perplexity が「でも多様性は自動的に良くない
> という反証があるよ」と冷や水をかけてくる。**舞い上がる材料と冷や水を、同じ調査の中で両方
> 受け取る。** これができると、結論がぐっと強くなります。次節で、その冷や水の正体を解明します。

---

### 7. Self-MoA 反証の「正体」を解明する（自己 PoC #3 → Agent C 実 LLM）

「多様性は自動的に優位でない」——この反証を、proxy ではなく**メカニズムのレベル**で解明したのが、ここの山場です。

#### 7.1 自己 PoC #3 — 投票か、ルーティングか

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

#### 7.2 Agent C の実 LLM が、独立に同じ結論を出した

そして——並列 Agent C が、**実 LLM（llama3.2、105 回の LLM 呼び出し、15 タスク）**で、自己 PoC #3 と**独立に同じ結論**を出してきました。

- 単一 best = **0.933**。MoA `best_of` + k≥5 で **1.000**（+0.067）。**majority / weighted は一度も 0.933 を超えず。**
- diverse > redundant（多様選抜が異 QD cell の補完 specialist を少ない k で先に拾う）。
- 改善は**丸ごと multistep の 1 問**（「5 を 2 倍して 3 引く」）由来。CoT 個体群が揃って落とす 1 問を、多様選抜の異種個体が解いた。

> 🔑 **独立クロス検証（本記事の核）**: 自己 PoC #3（合成・専門家分散）と Agent C（実 LLM・llama3.2）が、
> **別の手法で同一の結論**——「MoA は competence-aware routing（best_of）でのみ単一 best を上回る /
> 投票では届かない / 多様性は routing 下でのみ価値を持つ」——に達しました。
> 2 手法が一致することは、honest disclosure 上きわめて強い証拠です。

#### 7.3 最大の穴 — 「実ルーター」は oracle に届くのか（自己 PoC #4）

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

### 8. 個体に「調べる力」を持たせる（自己 PoC #5）

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

### 9. スケールが「多様性を質的に増やす」（Round 3）

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

### 10. 朝、全員が同じ結論に着いていた — 確定した方策

一晩で、**自己 PoC 6 本 + Agent A/B/C + Perplexity が、独立に同じ結論へ収束**しました。これが honest cross-validation の威力です。固定ものさし路線を捨て、以下を lldarwin v2 の核に確定採用しました。

#### S1. 選択核（飽和を構造的に回避）

- **固定スカラー quiz fitness を廃止**（baseline は 1 万世代で飽和 + monoculture 0.9 + 多様性崩壊 = 12h 病理を大規模再現、open-ended 0/6）。
- **選択 = novelty / ε-lexicase（z-score 標準化必須）+ minimal-criterion**。**MAP-Elites archive 単独では不可**（scalar_qd も全滅）= 選択圧そのものを開放端化する。
- **品質も要るので QD（品質 × 多様性 per cell）**: 純 novelty は scalar 品質を犠牲（0.77-0.83）→ 適応難易度（条件カリキュラム）と組んで品質勾配を供給（PoC #2）。
- **系統多様性は中立貯蔵庫で別途確保**（行動多様性 ≠ 系統多様性、res256 で uniq_lineages 1 → 32）。
- **factor-subspace QD を追加**（意味次元の多様性を個別保護、Agent A の factor-drift 限界への対処、PoC #6）。

#### S2. 成果の出し方 = 連続進化 × ライブ・オーケストラ（独自性の核）

- 成果物は単一 best でなく、**QD archive を連続進化させ、任意時点で MoA オーケストラして 1 答**（ORCH; online 進化 + online 回答の統合は white-space = 独自性、Perplexity 確認）。
- **集約は投票でなく competence-aware routing/gating（指揮者）必須**（自己 PoC #3/#4 + 実 LLM Agent C が三重一致）。
- **routing キーは QD の behavior descriptor を流用**（descriptor-router が較正非依存で oracle 近傍 0.90）= QD と ORCH が同一記述子基盤を共有（設計の節約）。

#### S3. 個体 = 調査機能を持つ agentic 個体（段階導入、proxy 検証済）

- 探索空間ではサンドボックス読取専用調査のみ（実 I/O は Approval Bus 片方向昇格後）。調査はコスト計上。
- **proxy 検証済（PoC #5）**: コスト λ が「選択的調査」を創発。AGENT-3（コスト原理）成立。実 LLM × 知識ベースは次段。

#### S4. 観測・対話制御（実装済 = 全ランで標準装備、Agent B 完了）

- 応答ログ / 個体別スコア時系列ビューワー / lineage 復元（進化系 886 テスト緑）。step/pause/resume は次段で配線予定。
- Agent B の lineage 復元は、12h データで「**全部 ?**」だった系統表示を解消し、champion 系統を gen70 → gen59 まで 12 hops 解決。欠落は捏造せず `lost@genN` と明示する（根因 = 親 ID が snapshot と winners のどちらか単独では辿れなかったこと）。観測基盤こそが honest disclosure の土台です。

#### 自己 PoC #6 — factor-subspace QD で Agent A の限界に対処

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

意味次元（factor）用の novelty を別途課すと、意味次元の多様性損失をほぼ半減（50% 損 → 32% 損）。Agent A の factor-drift 限界への有効策を proxy で実証。honest: 完全固定ではなく 68% 残存 = 残 drift は中立貯蔵庫併用 or factor 重み強化が要。

---

### 11. 教訓（honest disclosure として残す）

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

### 12. 結論

- 実 LLM 12h ランは「正直な不合格」だった——全滅しないが累積しない filtered random search。真因は固定ものさしの飽和（#25 の洞察を実 LLM で実証）。
- 一晩の分散調査（自己 PoC 6 本 + Agent A/B/C + Perplexity）が、独立に同じ結論へ収束 = **honest cross-validation**。
- 確定方策: **S1 開放端な選択核**（novelty/lexicase + std + MC + QD + 適応難易度 + 中立貯蔵庫 + factor-subspace QD）/ **S2 連続進化 × routing-MoA**（white-space 独自性、投票でなく指揮者）/ **S3 agentic 個体 + コスト**（選択的調査の創発）/ **S4 観測**（実装済）。
- すべての要素を proxy / （部分）実 LLM で裏付け済。残課題は「実 LLM 段への配線」「factor-subspace QD 実装」「scale-up」。コア戦略は確定した。

良い部品を作り、集約せずに束ね、実 LLM で飽和を確かめ、開放端な選択へ作り直す。そして 6 通りの独立検証が同じ結論に着いたとき、ようやく「方策が決まった」と言える。本記事こそ、#25 で予告した「**眼鏡が曇ると淘汰も無力**」の回です——実 LLM で眼鏡が曇った瞬間（飽和）を正直に晒し、Goodhart's law と proxy の限界を引き受けたうえで、開放端へ作り直しました。次は、この確定方策をコードへ落とす [**#28 実装編（オーケストラ型 AI）**](drafts/QIITA_#28_lldarwin_v2_phase1_orchestra.md) へ。

---

### 13. 関連

- 連載 #24-05「集団が学ぶ AI」— 派生集団進化の枠組み（本記事の前提）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #25「私とフリストンだけが残った」— monoculture の honest disclosure（本記事の動機）
- 連載 #26（設計編）「眼鏡で測るだけでは進化しない」— 淘汰器 lldarwin の設計と Stage1/1.5/2 実測（本記事の姉妹編）
- 先駆者論文（2026-05-27, date of record）「Continuously-Evolving Populations as Live Orchestrated Ensembles」— 本記事の方策を学術形式で定式化した防御的公開（FullSense 公開リポジトリ `docs/papers/`）
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

---

## 第4章 進化し続ける AI 集団を「指揮者」が合奏させて答える — llive のオーケストラ型進化と、飽和を治した 3 つの仕掛け #28

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> 前章で決めた方策を、いよいよ実装した報告です。llive が目指すのは「賢い 1 体に何度も聞く」のではなく「少しずつ違う大勢を進化させ続け、答えが要る瞬間に指揮者が適材を選んで合奏させる(ライブ・オーケストラ)」という姿。そのために、満点で飽和する病を治す 3 つの仕掛け——生徒が伸びたら合格点も上げる「適応難易度」、第二バイオリンが消えないよう個性を守る「factor-subspace QD」、成果を 1 人の優勝者でなく多様性の地図に貯める「MAP-Elites」——を組み込みました。結果、ベストスコアが満点に張り付かず最後まで伸び続けた。ただしこれは合成のものさし(proxy)上の話で、本物の LLM の賢さを測ったわけではない、と正直に線を引いています。
<!-- KAMI -->

> 📚 **連載ナビ（lldarwin アーク）**: #24-05 集団進化 → #25 monoculture の失敗 → #26 設計編 → #27 徹夜の意思決定（climax）→ **#28 本記事（実装編）**。※ 各記事は単独でも読めます。

> **コンセプト hook**:
> 1 体の賢い AI に何度も聞くのではなく、**少しずつ違う大勢の AI を「進化」させ続け、答えが要るその瞬間に、指揮者が適材を選んで合奏（オーケストラ）させて 1 つの答えにする**。
> ——これが llive がいま目指している姿です。`llive` は「LLM そのもの」ではなく「LLM の周りに被せる認知 OS」。その中で、**集団を絶やさず・偏らせず・成長させ続ける**のが、今回作り込んだ進化エンジン `lldarwin` です。
>
> 前作 #27 で私たちは「評価（ものさし）が満点に張り付くと、進化は止まってただのふるい付きランダムサーチになる」という病を、実 LLM の 12 時間ランで確認しました。そして「淘汰器をいくら磨いても無駄。**評価そのものを開放端にせよ**」と方策を決めた。
>
> 今回はその方策を **実装** しました。そして proxy（合成のものさし）の上で、**best スコアが満点に張り付かず、最後まで伸び続けた**のです。

---

### 0. 三行であらすじ（落語の「枕」）

- **売りが決まった** — llive の北極星は「**連続進化 × ライブ・オーケストラ**」。進化し続ける集団を止めずに、任意の瞬間に competence-aware routing（指揮者）で合奏させて 1 答する。これは先行研究の **white-space（空白地帯）**。
- **飽和を治す 3 つを実装した** — ①意味次元を個別保護する factor-subspace QD ②成果を「単一 best」でなく多様性アーカイブに貯める MAP-Elites ③ものさしを集団に追従させる適応難易度。これで「奏者（多様な個体）が絶えない」基盤ができた。
- **proxy で飽和回避を実証** — lldarwin-v2 を 10 世代回したら best 0.80 → **0.92 と張り付かずに上昇**。多様性アーカイブは 21 セルが埋まった。**ただし proxy であり、実 LLM の能力を測ったわけではない**（honest）。

要するに **「賢い 1 体」ではなく「多様な大勢 × 指揮者」**。そのための「奏者を絶やさない仕掛け」が今回の実装です。

---

### 1. llive とは何か（はじめての方へ）

`llive`（リブ。L は 2 つ）は **自己進化型・モジュラー記憶の LLM フレームワーク**です。FullSense という傘ブランドの一員で、兄弟に `llmesh`（オンプレ LLM ハブ）と `llove`（端末ダッシュボード）がいます。3 つは独立 OSS ですが、組み合わせると 1 つの世界観になります。

llive の思想を 1 行で言うと「**LLM 本体ではなく、LLM の"周り"に被せる認知 OS**」。4 層メモリ・6 ステージのループ・承認バス（Approval Bus）・TRIZ・10 個の思考因子……といった「考え方の足場」を LLM の外側に組み、**同じ LLM でも振る舞いを進化させられる**ようにします。

その「進化」を担うのが、今回の主役 **`lldarwin`**（ダーウィン）です。役割分担はこうです。

- **lleval（眼鏡）** = 個体を *測る*（評価）
- **lldarwin（淘汰器）** = 測った差を「誰が生き残り・子を残すか」に *変換する*（選択圧）

そして両者の上に乗る北極星が、次の「オーケストラ」です。

---

### 2. 売り = 連続進化 × ライブ・オーケストラ（独自性の核）

普通の Mixture-of-Agents（MoA）は、**固定された**複数モデルに同じ問いを投げ、答えを集約します。llive が狙うのはその一歩先です。

> **集団を止めずに進化させ続け（online evolution）、答えが要るその瞬間に（online answering）、指揮者が「この問いにはこの奏者たち」と選んで合奏させて 1 答する。**

この「online 進化 + online 回答の統合」は、調べた限り**明確な先行研究がない white-space** でした（#27 で Perplexity に文献を漁らせて確認）。近いものに MoA / Self-MoA / sequential aggregation / routing はありますが、「進化し続ける集団そのものをライブで合奏させる」型は見当たりません。

ここで効くのが #27 で得た 2 つの正直な発見です。

1. **集約は「投票」ではなく「指揮者（competence-aware routing / gating）」でなければならない。** 自己 PoC と実 LLM 検証が三重に一致しました：headroom（伸びしろ）のあるタスクでは `best_of`／`routing` が `single`（単一モデル反復）を上回るが、**`majority`（多数決）はむしろ逆効果**。これは 2025 年の "Self-MoA"（多様性は自動的に優位ではない）への、私たちなりの回答でもあります。
2. **指揮者の判断キーには、多様性アーカイブの「behavior descriptor」を流用できる。** つまり後述の QD（Quality-Diversity）と指揮者が、**同じ記述子の土台**を共有できる。

——ただし、オーケストラ本体（指揮者＝router の実装）はこれからです。**今回はその手前、「合奏させるに足る、多様で絶えない奏者の集団」を作る基盤**を実装しました。

---

### 3. なぜ「奏者が絶える」のか — 飽和という病（#25〜#27 のおさらい）

オーケストラに必要なのは「**個性の違う奏者が大勢、絶えずいること**」です。ところが素朴に進化させると、これが崩壊します。

- #25：500 世代回したら、世界に「私とフリストンだけ」が残った（**monoculture**）。
- #27：実 LLM(llama3.2) で 12 時間回したら、gen5 で best=1.0 に張り付き、65 世代無進歩。**全滅しないが累積もしない**＝ふるい付きランダムサーチ。

真因はどちらも同じ。**人手で固定したものさし（評価関数）が満点に張り付くと、全員が同点になって選択圧が消え、あとは遺伝的浮動で勝手に偏る**。眼鏡（lleval）が飽和すると、淘汰器（lldarwin）をどれだけ磨いても無力——これが #27 の結論でした。

だから磨く対象を変える。「ものさしを動かす」「多様性を構造的に守る」方へ。具体的には次の 3 つです。

---

### 4. 実装した 3 つの仕掛け（lldarwin v2 / Phase 1）

> 設計の合言葉は「**新しいアルゴリズムを発明しない**」。すでに llive 内に積み上げた部品（ε-lexicase / NoveltyScorer / MAP-Elites / 中立貯蔵庫）を、確定方策 S1 の形に**合成・配線**するのが Phase 1 です。`--selection lldarwin-v2` で一括 on になります。

#### ③ 適応難易度 — ものさしを集団に追従させる

`AdaptivePercentileGate`。各評価軸の「最低ライン（minimal-criterion）」を、毎世代**集団のスコア分布の指定パーセンタイル（例：下位 40% 点）**に置き直します。集団が伸びれば最低ラインも自動で上がる。`ratchet`（単調非減少）にしておけば、一時的に下振れしても基準は緩まない。

これで「固定ものさしが満点で飽和する」病に蓋ができます（PoC では固定難易度が能力 0.627 で停滞 → 適応難易度で 0.952 まで上昇）。全員が最低ラインを割る荒れた世代でも、淘汰器は gate を無視して全滅を避けます（fail-open ガード）。

落語でいえば、**生徒が伸びたら合格点も上げる先生**です。満点を取らせて終わりにしない。

#### ① factor-subspace QD — 意味次元の個性を個別に守る

`FactorSubspaceNovelty`。novelty 探索は「集団全体としての多様性」は保ちますが、巨大な潜在次元の下では「**意味のある次元（思考因子）の多様性**」が、いつのまにか痩せていきます（factor drift）。

そこで、思考因子の**部分空間だけ**で別途 novelty を測り、全体 novelty とブレンドします。PoC では、これで意味次元の多様性の目減りがほぼ半減しました（retention 49.5% → 68.1%）。

> 正直な改良点：元の PoC は「生の距離を 0.5 ずつ足す」でしたが、部分空間ごとに距離のスケールが違うため、実装では**それぞれを z-score（標準化）してからブレンド**するように直しました。「全体の合唱」と「各パートの個性」を公平に混ぜるためです。

奏者でいえば、**第二バイオリンが第一バイオリンに飲まれて消えない**ようにする仕掛けです。

#### ② MAP-Elites — 成果を「1 人の優勝者」でなく「多様性の地図」に貯める

`run_persona_evolution(map_elites=True)`。毎世代、全個体を MAP-Elites アーカイブに投入します。これは「最高スコアの 1 体」ではなく、**振る舞いの座標ごとに、そのマスでの最良個体を残す**地図（QD アーカイブ）です。新しいマスを埋めても既存のマスは消さない＝**多様性が構造的に崩壊しない・アーカイブは単調に育つ**。

これがそのまま、オーケストラの**奏者カタログ**になります。指揮者は将来、この地図から「この問いに合う座標の奏者」を選んで合奏させる——QD と routing が同じ記述子を共有する、という #27 の設計がここで効いてきます。

実装は **個体のフォーマットを拡張せず**、既存ゲノムの思考因子から座標（descriptor）を導出する additive 配線にしました（基盤の後方互換 900+ テストを壊さないため）。記述子の本格設計（高次元の縮約など）は将来 Phase の課題として余地を残しています。

---

### 5. 結果 — proxy で「飽和しない進化」を確認

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

### 6. honest disclosure（ここを飛ばさないでください）

良い結果ほど内訳を疑う、が FullSense の流儀です。

- **これは proxy です。** 個体は実 LLM ではなく llive のゲノム（思考因子の代理）。今回測ったのは「複数の独立した苦手軸に同時に選択圧をかけ、軸ごとの専門家を維持できるか」という **仕組みの実現可能性（mechanism feasibility）** であって、**production の LLM 能力ではありません**。実 LLM 評価は次の Phase です。
- **factor-subspace は完全保護ではない**（retention 68%、残りはドリフト）。中立貯蔵庫の併用や factor 重みの強化が要ります。
- **舞台裏の正直**：今回の実装中、自動コミットフックが編集のたびに「編集前」スナップショットを 49 件も積んでしまい、履歴が散らかりました。最後に意味のある 1 コミットへ squash して整理しています（公開 OSS 側）。逆に、内部戦略を含む fork は意図通りローカル保持のままで、露出していないことも確認しました。

---

### 7. これからどうするか

進化エンジン（奏者を絶やさない基盤）は Phase 1 で形になりました。次はオーケストラ本体と、proxy から実物への橋渡しです。

1. **Phase 2 = 実 LLM 配線。** オンプレ（localhost ollama）の実 LLM を相手に、適応難易度・factor-subspace QD・MAP-Elites を実評価で検証する。proxy で見えた「飽和回避」が、本物の能力でも起きるか。
2. **指揮者（router）の実装。** QD アーカイブの descriptor を流用した competence-aware routing で、「進化する集団をライブで合奏させて 1 答」を実際に動かす。`best_of` の oracle にどこまで迫れるか。
3. **規模を上げる。** 集団 256 → 4096、潜在次元のスケールアップ。容量仮説（大きいほどニッチが増える）の確認。
4. **対話的な連続運転。** 長時間ランを step / pause / resume で覗ける運転席（CKPT-1）。

---

### 8. ここで一息（休憩ポイント）

ここまでで「**llive は何を売りにするのか**」は伝わったでしょうか。

- 賢い 1 体ではなく、**進化し続ける多様な集団 × 指揮者の合奏**。
- そのために、**奏者を絶やさず・個性を守り・成長させ続ける**進化エンジンを作った。
- proxy では飽和を治せた。**次は実 LLM とオーケストラ本体**。

続きの「実 LLM 編」と「オーケストラ編」で、proxy の約束が本物になるかをお見せします。——ここまでお付き合いありがとうございました。

---

### Series Navigation

- 連載ナビ（lldarwin アーク）: #24-05 集団進化 → #25 monoculture の失敗 → #26 設計編 → #27 徹夜の意思決定 → **#28 本記事（実装編）**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

---

## 第5章 「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #29

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> 普通の連載なら「直りました、めでたし完!」のところを、あえて自分の設計に冷や水をかける「反証回」です。テーマは Goodhart の法則——「指標が目標になると、それは良い指標でなくなる」。LLM の弱点を点数にすると、進化は真の能力でなく「点数だけ稼ぐ表面的な近道」を必ず見つけてしまう。さらに本章の隠れた主役は、著者自身の告白です。「行動が多様」「血統が多様」「本物の知能が多様」という似て非なる 3 つを一瞬混同し、良い数字(0.05)を見て別の能力まで良くなったと早合点しかけた——その現行犯を解剖台に乗せます。派手な勝利宣言を一つも書かない、連載で一番地味で誠実な回です。
<!-- KAMI -->

> 📗 **お急ぎの方へ**: この記事には かみくだき版 があります（比喩多め・短時間で要点だけ）。
![眼鏡が飽和すると選択圧は無力 — 反証4コマ #29](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q29_4koma.svg?v=2)


> **コンセプト hook**: #25 で失敗を晒し、#26 で「淘汰器 lldarwin」を設計しました。普通の連載なら
> 次は「直りました! めでたし、完!」です。**でも、それをやらないのが FullSense の honest disclosure**。
> この記事はあえて**自分の設計に反証をぶつける回**。テーマは進化計算と機械学習の両方に効く一語——
> **Goodhart's law（指標が目標になると、それは良い指標でなくなる）**。
>
> 「LLM の弱点を fitness にすれば、進化で勝手に克服してくれる」——この甘い楽観に、私は自分で冷や水を
> かけにいきます。しかも今回は、**自分が一度やらかした「事実誤認」を、生きた標本として解剖台に乗せます**。

---

### 0. 三行であらすじ

- **眼鏡（fitness）が飽和すると、どんな高級な選択圧（lldarwin）を足しても淘汰は無力**になる（#25 の真の教訓）。
- **proxy fitness で LLM 弱点を測ると、真能力でなく「指標をハックする表面戦略」が進化する**（Goodhart's law）。
- 結論: lldarwin の価値主張は **(a) proxy は mechanism feasibility のみ (b) 実 LLM/VLM 評価が本質 (c) 多様性の地図化** に**限定**する。これが正直な線引き。

そして本記事の隠れた主役は、もう一行あります。

- **私自身が「行動多様性」と「系統多様性」と「実 LLM 知能多様性」を一度混同した**。その自己反証を、
  反証回の核に据えます。「うまくいった」を疑うとは、こういうことだ、という実演です。

---

### 1. honest disclosure の念押し — 良い結果ほど疑う

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


![訝しげに観察するマスター](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/006.jpg)
> 🗒️ *「打って変わって賢い風…?」— 急に良くなった結果を訝る(良い結果ほど疑う)*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

---

### 2. 反証 1 — 飽和した眼鏡には、どんな選択圧も効かない

#### 2.1 #25 の真因をもう一度

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

#### 2.1.5 実証 — 記憶タスクで「床」と「天井」が選択圧を殺した（Step C, 2026-05-30）

この反証は、その後 llcore の Step C 実験（CPU 完結）で**実データとして再現**されました。標準的な記憶タスク 2 種を、進化（MAP-Elites）と素朴な探索で解かせた結果がこれです:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="Step C の2つの結果（床と天井）" width="640">

- **delayed_parity（XOR）= 床**: 全 method が R²≈0（基質が原理的に解けない）。誰も登れない＝差が出ない。
- **flip_flop（覚えるだけ）= 天井**: 全 method が R²≈0.95（簡単すぎて全員到達）。**まさに「飽和した眼鏡」で、ここでも選択圧は無力**。

参考までに、③（選択）が効くのは「ニセ頂上を越える、だましだが渡れる坂道（欺瞞 corridor）」がある時だけです:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/deceptive_corridor.svg" alt="だまし地形と進化（③が効く状態）" width="640">

Step C の結論は、潔く **N/A（この基質では③の有無を測れなかった）**。しかも draft 段階で私は「③は不要」と**書きすぎ**、多視点の adversarial 検証が「天井効果で非診断・検出力不足（δ=+0.33 は medium だが p=0.15 で inconclusive）」と捕まえて格下げさせました——§3.2 の「自己反証」が、ここでもそのまま起きたわけです。

#### 2.2 「#25 が直った」は、半分しか正しくない

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

#### 2.3 責務分離 — どちらが欠けても進化は壊れる

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

### 3. 反証 2 — Goodhart's law: proxy fitness をハックする進化

#### 3.1 最重大リスク

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

#### 3.2 私自身の「現行犯」— 自己反証

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

#### 3.3 「何を測った 0.05 か」を、対比で見る

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

#### 3.4 対策はあるが、問題は消えない

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

### 4. 反証 3 — 設計者依存性: 「多様性の方向」は誰が決めた?

#### 4.1 メタな疑い

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

#### 4.2 受容 — 勝てる軸を限定する

ではどうするか。**未想定創発を主張しない**、というのが正直な答えです。

lldarwin は「**検証可能性のない多様性の地図**」を狙うのであって（差別化軸 DIFF-1）、
strong / unbounded open-endedness は主張しない（SCOPE と整合）。
「人類未踏の創発をやってます!」と言えば派手ですが、それは嘘になる。
**勝てる軸を限定する**——認知スタイル・文化的スタイルといった「検証可能性のない多様性」を地図化することに
価値を絞る。これが lldarwin が誠実に主張できる範囲です。

派手な主張を捨てる勇気が、honest disclosure の核心でもあります。

---

### 5. 反証 4 — minimal-criterion と QD 自身のトレードオフ

淘汰器の各部品にも、固有の弱点があります。設計書 §7.1 の受容済み限界を一つずつ解説します。

#### 5.1 minimal-criterion の停滞⇄崩壊

minimal-criterion（最低基準 gate）は「基準を満たさない個体は繁殖させない」仕組みですが、
**基準の高さがそのままトレードオフ**になります。

- **基準が低い** → ほぼ全員が通る → 選択圧ゼロ → **停滞**（#25 の飽和と同じ構造）。
- **基準が高い** → ほとんど誰も通らない → **全滅**（実証あり。全員 gate で落ちると次世代が作れない）。

ぬるま湯か地獄か。**対策**: criterion を固定値でなく**集団分位点で適応**させる（例: 下位 30% を落とす）。
さらに全員 fail なら gate を無視する安全弁を入れる（`MultiPressureSelector` 実装済）。

#### 5.2 QD の次元の呪い + アーカイブ飽和

QD（MAP-Elites）は behavior 記述子で cell を切りますが、**記述子が高次元だと cell の大半が空**になる
（次元の呪い）。また長期間回すと全 cell が埋まり、新規性が頭打ちになる（**アーカイブ飽和**）。
これは人工生命の古典 Avida / Tierra でも観測された現象です。

**対策**: 記述子を**低次元に縮約**（DESC-1, JL 射影）+ 飽和を **Bedau 統計で監視**し、
「**飽和＝失敗**」として正直に記録する（飽和を「もう探索しきった証拠」と都合よく解釈しない）。

#### 5.3 lexicase のスケール限界

ε-lexicase は case 数が増えると**計算コストが増大**し、しかも**ノイズで実質ランダム選択化**する。
case が多すぎると、たまたま順序の先頭に来た case で勝者が決まり、選択がサイコロに近づく。

**対策**: **down-sampled lexicase**（毎世代 case の部分集合だけ使う）でコスト削減 + 環境かく乱。

#### 5.4 トレードオフは実測で「見える」

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

#### 5.5 honest 留保 — 「生存」は「生命維持」かもしれない

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

### 6. Stage2 — proxy から「実」への橋

反証ばかりでは、設計が前に進まないように見えるかもしれません。
でも反証で足場を固めたからこそ、次の一歩に意味が出ます。それが **Stage2: 実 LLM 評価**です。

#### 6.1 proxy 軸（mechanism feasibility）

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

#### 6.2 実 on-prem LLM 評価（proxy→real の橋）

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

#### 6.3 だが、ここでも正直に

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

### 7. 結論 — どこまで主張してよいか（線引き）

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

### 8. 教訓（永久保存）

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

### 9. 関連
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


<!-- INTERLUDE -->

### ☕ 閑話休題 — 二人羽織で踊る — ccr 自動継続に残る「人間の指一本」

反証続きで頭が疲れたところで、ひと息つく話を。著者は Claude Code を「できるだけ自分で走り続けてほしい」と思って、起動時に作業内容を自動で投入する仕組み(ccr 自動継続)を組んでいます。理想は、寝ている間も勝手に開発が進む全自動マシン。ところが、どう工夫しても最後に一箇所だけ『人間の指一本』が必ず残るのです。具体的には、再起動や再ログインが要求された瞬間——そこだけは AI が自分でボタンを押せず、人間が手で Enter を押すまで世界が止まる。AI は自力で自分を再起動できない、という当たり前の壁です。

これはちょうど、寄席で見る『二人羽織』に似ています。前の人が顔と口を担当し、後ろの人が見えない手で箸を操る。息が合えば見事に蕎麦をすするのですが、肝心なところで必ず『中の人(=人間)』がいないと成立しない。AI の自走も同じで、九割九分は AI が踊っていても、最後の一手だけは人間が袖から手を出す。完全自動という幻に飛びつかず、『どこに人間の介在点が必ず残るか』を正直に認める——これもまた、本記事が貫く『良い結果ほど内訳を疑う』姿勢の、ささやかな実地版です。お茶でもどうぞ。

<!-- INTERLUDE -->



---

## 第6章 進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> 数式ゼロ・コードほぼゼロの「散歩」回。著者が延々と語ってきた人工進化には半世紀以上の歴史があり、面白いことに、その研究はいつも「どう見せるか(可視化)」と二人三脚で進んできました。1970 年の白黒で点滅するライフゲームから始まり、コードが生き物になる Tierra、進化を計測する Avida の系統樹、進化を 3D 動画で魅せた Karl Sims、滑らかで美しい Lenia、多様性を地図にする QD、そして最先端の 3D ガウシアン……と、見せ方が「抽象→具象→動的」へ進化した道のりを一気に辿ります。最後に、FullSense の進化可視化がこの半世紀の系譜のどこに立っているかを位置づけます。
<!-- KAMI -->

> **コンセプト hook**: 私が #25〜#27 で延々と語っている「人工進化」。実はこれ、半世紀以上の歴史がある
> 研究分野です。そして面白いのは、**進化の研究は常に「見せ方（可視化）」と二人三脚で進化してきた**こと。
> 1970 年の白黒の点滅セルから、2024 年の連続流体・3D ガウシアンまで。「進化を見せる技術」の系譜を、
> 教養として一気に辿ります。FullSense の進化可視化（思考因子グラフ上の系統樹）が、この系譜の
> **どこに立っているのか**を最後に位置づけます。

---

### 0. なぜ「可視化」が進化研究の主役なのか

進化は **長時間・大集団・多世代**の現象。数字の羅列では「何が起きたか」が掴めません。
だから人工進化の歴史は、ほぼそのまま **「進化を一目で理解させる表現の発明史」** です。

> 🍵 **休憩ポイント**: この記事は数式ゼロ・コードほぼゼロの「散歩」回です。コーヒー片手にどうぞ。
> 各時代の「見せ方のブレイクスルー」だけ拾っていきます。

---

### 1. 1970: Conway のライフゲーム — 「単純ルールが模様を生む」

- **何**: 2 次元セルオートマトン。生死 2 状態 × 近傍 8 セルの単純ルール。
- **見せ方の発明**: **格子の点滅そのものが可視化**。グライダー・ブリンカー・グライダーガンといった
  「動く模様」に名前がついた = 人間が**創発パターンを目で名づけた**最初期の例。
- **限界**: 進化（自然選択）ではなく決定論的な展開。しかし「単純ルール → 複雑な見た目」の衝撃が分野を開いた。

**節の肉付け予定**: グライダーが「移動する構造」として認識される=可視化が概念を生んだ好例として深掘り。

---

### 2. 1991: Tierra（Tom Ray）— 「コードが生き物になる」

- **何**: 仮想 CPU 上で自己複製する機械語プログラムの生態系。寄生体・免疫・最適化が**勝手に創発**。
- **見せ方の発明**: **メモリマップの可視化**。各プログラムが占めるメモリ領域を色で塗り、
  寄生体が宿主に食い込む様子を「地図」として見せた。**「コードの生態系」を空間として描いた**。
- **意義**: 「自己複製子の自然選択」を計算機内で初めて観測。open-ended evolution 研究の出発点の 1 つ。

---

### 3. 1994: Avida（Adami / Ofria）— 「進化を計測する」

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

### 4. 1994: Karl Sims「Evolved Virtual Creatures」— 「進化を映像で魅せる」

- **何**: 3D 物理シミュレーション内で、形態（block の繋がり）と神経制御を**同時に進化**させ、
  泳ぐ・歩く・物を取り合う生き物を生んだ。
- **見せ方の発明**: **3D アニメーション映像**。論文の図でなく**動画**で見せたことが衝撃を呼んだ。
  「進化が設計した、誰も予想しなかった奇妙な歩き方」を**人間が直感的に面白がれる**形にした。
- **意義**: 進化可視化が「研究者向けグラフ」から「**誰もが見て驚く映像**」へ。
  FullSense のデモ哲学（[[project_f25_demo_polish]]「動きで魅せる」）の精神的祖先。

> 🍵 **休憩ポイント**: ここまでで「白黒の点 → メモリ地図 → 系統樹 → 3D 動画」と、
> 見せ方が**抽象 → 具象 → 動的**へ進化したのが見えれば OK。後半は現代編です。


![擬人化イルカの自己紹介](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/069.jpg)
> 🗒️ *「人類が滅んだあとの動物!?」— 進化を映像で魅せる系譜(空想進化)*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

---

### 5. 2019: Lenia（Bert Chan）— 「連続的な人工生命」

- **何**: ライフゲームを**連続空間・連続時間・連続状態**に一般化。滑らかに動く「生き物のような」
  パターン（orbium 等）が多数発見された。
- **見せ方の発明**: **連続フィールドの滑らかなレンダリング**。離散の点滅から、生物の細胞のように
  しなやかに動く流体的表現へ。「人工生命が**美しい**」という新しい訴求軸を開いた。
- **意義**: 可視化の質そのものが研究の発見力を上げた例。美しく見えるからこそ新パターンを人間が気づける。

---

### 6. 2020s: Quality-Diversity の可視化 — 「多様性を地図にする」

- **何**: MAP-Elites / CMA-ME 等の QD アルゴリズム。単一 best でなく**多様な高性能解の集合**を生む。
- **見せ方の発明**: **behavior space のヒートマップ**。2 軸の behavior 記述子を格子に取り、
  各 cell の elite を色で塗る = 「**多様性そのものを地図として可視化**」。
- **意義**: FullSense / lldarwin の QD archive 可視化はここに直接立脚。
  「1 cell でも残れば全滅しない」を**地図の空白 vs 充填**で一目で見せられる（#26 で詳述）。

---

### 7. 2020s〜: 3D Gaussian Splatting（3DGS）— 「進化の状態を空間表現する」（FullSense の賭け）

- **何**: 元来は新視点合成（NeRF の系譜）の技術。点群を 3D ガウシアンで表現し高速・高品質に描画。
- **FullSense の着想**: 進化集団の**高次元 genome / pressure profile を 3D ガウシアン空間に写像**して
  「進化の状態を立体的に見せられないか」という探索（[[project_precision_metrology_llm]] の SH 係数連携と同根）。
- **位置づけ**: これは**まだ研究的賭け**であり、確立技術ではない（honest disclosure）。
  本記事の系譜の「最先端の縁」に置く実験です。

---

### 8. FullSense の進化可視化はどこに立つか

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

### 9. 関連
- 連載 #25〜#27 — 本記事の進化可視化の「中身」（monoculture / lldarwin / 反証）
- 関連 memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- 参考: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #25-27 の Qiita URL cross-link / en・zh・ko 版展開 -->
<!-- KEY MESSAGE: 進化研究は可視化と二人三脚。点滅→地図→系統樹→3D動画→連続→QD地図→3DGS。FullSense は Avida+Sims+QD の末裔。 -->
<!-- NOTE(事実整合): 年代/人名は一般的な人工生命史の通説に準拠。3DGS の進化可視化応用は FullSense の研究的賭けであり確立技術でない旨を明記済。 -->

---

---

## 第7章 AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> FullSense は著者ひとりの個人開発ですが、実態は「ひとり」ではありません。AI コーディングエージェント Claude Code を「主(司令塔)」、別の AI Codex を「部下」に据えた、人間 1 + AI 2 の 2 階層体制が回っています。本章のポイントは「AI を 2 つ使う=2 倍賢い」ではなく、指揮系統を 1 つに保つこと。最大の危険は「AI の出力を別の AI が無検証で信じる」連鎖で、誤りが増幅されます。だから鉄則は「外部 AI の言うことは実コードや一次情報で 1 件ずつ確かめてから採用」。子分の報告は起点であって結論ではない、という多重委任の統制術を、実例とアンチパターンで語ります。
<!-- KAMI -->

> **コンセプト hook**: FullSense（llmesh / llive / llove）は私ひとりの個人開発です。でも実態は
> 「ひとり」ではない。**AI コーディングエージェントを主・別の AI エージェントを部下**にした
> 2 階層の開発体制が回っています。主が **Claude Code**、部下が **Codex CLI**。
> 「AI が AI に仕事を振って、その成果を AI が検証する」——この多重委任を、暴走させずに
> どう規律するか。本記事は人間 1 + AI 2 の「二本柱」運用の実践記です。
>
> キーワードは **オーケストレータ / 配下 worker / 検証規律 / 並列化**。

---

### 0. 三行であらすじ

- **Claude = オーケストレータ**（計画・実装・委任・**検証**）/ **Codex = 配下 worker**（実行・レビュー・調査）。
- 「二本柱」= 対等ではなく **Claude 主導 + Codex 配下**。司令塔は 1 つに保つ。
- 鉄則: **外部 AI の finding は実コード / 一次情報で 1 件ずつ検証してから採用**（鵜呑み禁止）。

---

### 1. なぜ「二本柱」なのか — 動機

個人開発で AI エージェントを 1 つだけ使うのは、もはや普通です。なぜ 2 つ目（Codex）を**部下として**足したのか:

1. **ベンダー分散・冗長性** — 単一エージェントの課金変更 / 障害 / quota 枯渇のヘッジ。
2. **クロスレビュー** — 同じ設計を別系統の AI に見せ、セカンドオピニオンを取る（盲点削減）。
3. **並列 worker** — 独立サブタスクを配下に投げ、主は最重要タスクに集中。

> 🍵 **休憩ポイント**: 「AI を 2 つ使う = 2 倍賢い」ではありません。**指揮系統を 1 つに保つ**のが肝。
> 烏合の衆にすると、むしろ遅くなる。本記事の半分は「どう統制するか」の話です。

---

### 2. 役割分担 — オーケストレータと配下 worker

![人間→Claude（主＝オーケストレータ）→Claude サブエージェント並列 / Codex CLI 配下 worker の階層図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy.svg)

- **Claude（主）の責務**: タスク分解・依存性判定・独立タスクの並列起動・進捗監視・**成果の検証**・一括コミット。
- **Codex（配下）の責務**: 委任された範囲の実行。非対話委任 = `codex exec -s read-only "<prompt>"`。
- **司令塔は常に Claude**。Codex は Claude を経由してしか全体に影響しない（直接コミットさせない）。

**節の肉付け予定**: Claude サブエージェント並列（[[feedback_parallel_first_execution]]）と Codex 配下委任の
使い分け表。「同 file は直列・独立 file は並列」「git 操作は orchestrator が一括」（[[feedback_agent_no_git_parallel]]）。

---

### 3. 検証規律 — 「鵜呑み禁止」が体制の生命線

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

### 4. 並列化の作法 — 暴走させない統制

複数 worker（Claude サブエージェント + Codex）を同時に回すときの規律:

- **2〜4 並列が安全圏**（主の context 余裕・コミット衝突なし）。5+ は file レベル独立性を厳格管理。
- **独立タスク抽出** = 依存なし + file / module / repo レベルで非接触。同 file は直列（file lock 的）。
- **不可逆操作（削除 / push / submodule 改変）は 1 件ずつ人間確認**。配下に勝手にやらせない。
- **git 操作は orchestrator が一括**。並列 worker には git を触らせない（競合回避）。

> 🍵 **休憩ポイント**: 「AI をたくさん並べれば速い」の罠。**主の context（注意の総量）が律速**です。
> 5 体並列にしても主が捌けなければ意味がない。脳のワーキングメモリと同じで、同時把握できる数には上限がある。

---

### 5. アンチパターン（やってはいけない）

- 「1 つずつ確認しながら進めます」と宣言してから黙々と直列実行（並列化の機会損失）
- 配下に投げず主の context だけで全部こなす（context 爆発）
- 並列起動した worker の結果を待たずに主が同じ file を触る（競合）
- 2 worker に同じ file を書かせる委任（独立性の判定漏れ）
- 配下 AI の finding を無検証で設計や実装に採用（誤り増幅 = 二本柱最大の事故）

---

### 6. この体制で実際に何が回ったか（FullSense の実例）

- **設計クロスレビュー**: 進化設計 / 要件 / PoC を配下にレビューさせ、主が実コードで検証して採用判断。
- **既存資産調査**: lldarwin の既存部品（loop.py / mating.py / nsga2.py 等）の所在を配下に調査 → 主が確認。
- **並列サブタスク**: 記事骨子・コード調査・要件整理を独立タスクとして並列化（本連載自体がその産物）。

> 🍵 **休憩ポイント**: 「人間 1 + AI 2」で個人開発の生産性がどう変わったか、という主観も最後に正直に。
> 速くなった面（並列・冗長性）と、増えた負荷（検証コスト・統制コスト）の**両方**を honest disclosure。

---

### 7. 教訓

- **指揮系統は 1 つに保つ。** 二本柱は対等でなく主従。司令塔の分裂は事故のもと。
- **検証規律が体制の生命線。** AI が AI を無検証で信じる連鎖が最大のリスク。
- **並列度は主の context が律速。** 体数でなく捌ける量で決める。
- **不可逆操作と git は人間 / orchestrator が握る。** 配下には可逆な仕事だけ任せる。

> **次回予告**: 二本柱で回した進化設計（#26 lldarwin）を、配下 Codex + on-prem ollama で
> Stage 2（実 LLM 評価）まで進める。多重 AI 委任が「研究の実装速度」をどこまで上げるか。

---

### 8. 関連
- 連載 #26「lldarwin の設計」— 本体制で回した実例
- 関連 memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #26 の Qiita URL cross-link / en・zh・ko 版展開 -->
<!-- KEY MESSAGE: 人間1 + AI2 の二本柱。Claude 主導 + Codex 配下。検証規律(鵜呑み禁止)が生命線。並列度は主の context が律速。 -->
<!-- NOTE(事実整合): Codex は ChatGPT Pro $100/月で契約方針(promo 〜5/31)。導入状態(CLI 0.117.0 / quota 枯渇 / login 切替予定)は reference_codex_two_pillar 準拠。実応答未取得の段階である旨に注意して脚色しないこと。 -->

---

---

## 第8章 (連載 #32) llcore CPU PoC battery 完成

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> ここから話題が lldarwin から llcore へ移ります。llcore は「LLM の重み」ではなく、その下にある「コア計算の式そのもの(状態更新則・学習則など)」を遺伝子にして進化させる、CPU だけで動く研究フレームワークです。本章は、その土台となる 5 本の小実験(PoC battery)が完成した報告。目玉は、進化が暴走して数値的に壊れた式を生まないよう、Z3(数式が成り立つか機械的に証明する道具)を進化ループの中で門番に使ったこと。これは先行研究に見当たらない独自軸だと事前調査で確認しました。なお実 LLM 接続は GPU 待ち、という限界も正直に添えています。
<!-- KAMI -->

### TL;DR

- Transformer の **コア計算 (state update / 学習則 / 認知駆動 Δ)** を進化対象にする研究フレームワーク `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 独立路線) の **CPU PoC battery 完成**
- **5 PoC / 39 falsifiable gates / 76 tests / Codex pair-review 5/5 Green-light** で機構実証
- **Z3 で構造変異を online gate** = 進化探索の selection pressure に SMT を組込んだ先行未発見 (事前調査 RAD 14 分野 + Agent A-D 確認)
- 投稿先候補: TMLR (本命) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

### なぜ作ったか

LLM 重みは凍結が標準だが、**コア計算アルゴリズム自体は人手設計に固定**されている。AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge など architecture/algorithm 探索は進んだが:

1. **個人 compute では計算リソース不可能** (TinyLlama 1.1B from scratch = $140k / 90 日 / 16×A100)
2. **探索中の安全性保証なし** = 数値不安定な architecture を生み出して時間浪費
3. **検証付き探索は静的 verification (Reluplex/Marabou/α,β-CROWN) と分断** — 進化ループ内 SMT online gate の研究は未発見

### 確定独自軸 (事前調査で negation work なし)

mechanism 実証済 (4 軸):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **state update 規則を遺伝子化 RWKV-style** (Stage 0a v2)
3. **factor_hook (認知状態 → SSM Δ)** (Stage 2a mock)
4. **自前進化器 + verifier 基盤** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / VNN-COMP 新カテゴリ提案。

### PoC レダー (5 stage / 39 gates 全 PASS)

| PoC | 内容 | キー数値 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 自前 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

### v1 の失敗から学んだこと (honest disclosure)

PoC 0a v1 は `decay*s + mix*x*tanh(gate_str*s)` で **state=0 が fixed point の zero attractor** = G1-G5 形式 PASS だが情報伝達ゼロ。Claude 単独で見落とした設計問題を **Codex (gpt-5.4) と gem-critic の独立 verdict** が検出し RWKV-style に v2 redesign。

→ **5 PoC 中 4 件で Claude 単独では見落とした設計問題を Codex pair-review が検出**。構造破綻防止に相互レビューが機能した実例。

### 次の選択肢

a. Stage 3 kernel 多様化 (rwkv/mamba/hopfield/linear-attn を遺伝子化)  
b. Stage 4 学習則 (FF/EP/PCN/Hebb) を gene 化  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. PrediPrune+Quokka で Z3 gate 高速化  
e. FlashEvolve で 3.5-5x wall-clock 高速化  
f. 論文化 (TMLR + GECCO 2027)

### Honest 留保

- mock 中心、実 LLM/重み接続は GPU/新 PC 待ち
- 1 step scalar invariant の over-approx proof 段階、多次元・多 step は post phase
- tanh 上界近似は保守的 (sound だが完全でない)

---

**Tags**: 進化計算 / 形式検証 / Z3 / RWKV / state space model / CPU研究  
**関連**: 連載 #14-31 (llive lldarwin v0.B-E + 観測+governance + lleval)  
**Project**:  (PyPI llmesh-llcore 0.1.0a0)

---


<!-- INTERLUDE -->

### ☕ 閑話休題 — コンテキスト爆発の悲喜劇

ここで、長時間 AI に作業させると必ず出くわす『コンテキスト爆発』の話を一席。AI には一度に覚えていられる作業メモの上限(コンテキスト)があり、長い実験ログや大量のファイルを読み込むと、その枠がみるみる埋まっていきます。人間でいえば、机の上に書類を積み上げすぎて、肝心の一枚がどこにあるか分からなくなる状態。困るのは、枠が一杯になると AI が古い記憶を要約して捨て始めることで、要約に残らなかった『まだ保存していない変更』や『動かしっぱなしのプロセス』が、ふっと意識から消えてしまうのです。

本記事の lldarwin が『満点で飽和すると選択圧が消える』と語ったのと、どこか相似形なのが面白いところ。あちらは評価が天井に張り付いて差がなくなる病で、こちらは記憶が天井に張り付いて細部が消える病。どちらも『容量の限界に張り付くと、大事な情報が均(なら)されてしまう』という同じ構造をしています。だから本編でも、長いランの状態は要約任せにせず、その都度きちんと現状を確かめ直す、という地味な保険をかけている。派手な進化計算の裏に、こういう『記憶の机を片付け続ける』日常仕事がある、という楽屋話でした。

<!-- INTERLUDE -->



---

## 第9章 (連載 #33) 整いすぎた結果は、勝ちではなく警報 — 第三軸 ③ を proper power で決着させた一日

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> 問いはシンプル——「AI のコア計算を進化で探すとき、多様性を保って選り分ける工夫(③)は本当に要るのか?」。本章はその決着をつけた一日の記録です。鍵は地形のたとえ。設計の良さを山の高さで表すと、③が役立つのは「ニセ頂上で素朴な登山者が止まる、だまし地形」のときだけ。滑らかな一つ山では無用の長物です。そこで評価ノイズを物理的にゼロまで落として実物に近い地形を測り直したら、それは「本当に滑らか」で③は不要と確定。整いすぎた良い結果はむしろ警報、という規律で自分の結論を 3 つのレンズから殴り、言い過ぎを削っていく過程が読みどころです。
<!-- KAMI -->

### TL;DR

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

### 0. この記事は何の話か (コンセプト)

`llcore` は「Transformer のコア計算 (状態更新則・学習則・認知駆動 Δ) を遺伝子にして、Z3 で壊れないように検証しながら進化させる」CPU 完結の研究フレームワークです (連載 #32 で PoC battery の話を書きました)。

その進化エンジンには、進化の 4 要素のうち **③ (適者生存 selection / 分離 separation)** をどう効かせるか、という設計上の急所があります。多様性を保ってニッチに残す MAP-Elites のような「選り分けて分けて育てる」仕組みです。

問いはシンプルです。

> **その③、本当に要るの?**

要るなら、③ を載せるための重い投資 (最終的には GPU で実 LLM を回す) に意味がある。要らないなら、③ にこだわるのは時間と電気の無駄になる。

この一日 (2026-06-02) で、その問いに **3 つの実験で正面から決着をつけにいきました**。タイトルどおり、結論は「整いすぎた結果は警報」という FullSense の通奏低音に、もう一度引き戻される話です。

— ここまで 30 秒。準備運動おわり。本題へ。 —

---

### 1. たとえ: 山登りと、だまし地形

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

### 2. 過去の積み残し — 「③不要」は本当に "不要" だったのか

これまでの実験 (Step C → 梯子段1 → E-A → 谷深さ実測) を通じて、像はだいたいこうでした。

- **合成した欺瞞 corridor では③が圧勝** (3 つの baseline 全てに勝ち、Cliff δ=+1.0)。③ は存在証明済み、機構として本物。
- **実問題に近い proxy 地形では③ negative** (MAP-Elites が random にしか勝てない = 滑らかな地形と同じ症状)。

ところが、ここに 2 つの未解決のしこりが残っていました。

1. **「③不要」は本当に "地形が滑らか" だからなのか、それとも単に "サンプル数が足りなくて差を検出できなかった (underpower)" だけなのか?** ── これを取り違えると、「③ は無力」という過剰一般化をやらかす。
2. 谷深さの直接測定は前回 **N/A (測定不能)** で終わっていた。評価ノイズが谷の深さより大きくて、谷があっても埋もれて見えない、という計器の限界。

つまり「滑らかに見えた」のが **地形の性質** なのか **計器の限界** なのか、決着がついていなかった。ここを詰めるのが Step D です。

— 小休止。ここまでが前提。ここから先が今日やった 3 実験。 —

---

### 3. 実験の設計 — 3 本立て

| 実験 | 何を測るか | 狙い |
|---|---|---|
| **EXP1** | proper-n 再検定 | サンプル数を本気で増やして、③ の効果が本物か検出力で詰める |
| **EXP2** | 決定論 C1 多峰性 | 評価ノイズを物理的にゼロにして、地形が「だまし地形」か「滑らかな一つ山」かを noise-free で判定 |
| **EXP3** | K4 ridge clip の verdict-flip | 「ある後処理が③を隠している」疑いを検証 |

規律: 全部 `research/step_d_settle/` に隔離、src は無改変、git はオーケストレータが一括。各実験は破綻ゲート (G1 CPU 完走 / G2 再現性 / G3 診断器妥当 / G4 src 不変) を通す。

---

### 4. EXP2 が決め手だった — 評価ノイズをゼロにすると地形が見える

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

### 5. EXP1 — 実 multitask 近傍だけ「③ NOT null」の弱い気配

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

### 6. EXP3 — 「後処理が③を隠している」疑いは、外したら逆に悪化した

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

### 7. Surviving refutation — 3 つのレンズで自分の結論を殴ってみた

honest disclosure の核は「自分の結論を一番きつく疑う」ことなので、3 つの独立な反証レンズを当てました。**3 つとも `refuted=true / medium` で生き残った**、つまり保守的な verdict は覆らないが、positive 寄りの強調は弱める方向で効いています。

1. **[power_adequacy] C-gen4b の gate PASS は optional-stopping + 多重比較で脆い**。上の §5 のドリフトと Bonferroni FAIL がこれ。「③ NOT null」を headline にするのは境界 p に寄りかかりすぎ。→ p の n 軌跡と後半 seed の符号反転を開示フィールドに記録済。
2. **[determinism_and_circularity] 単峰 verdict は閾値近接で脆い**。決定論化と非循環性そのものは clean (behavior と fitness の相関は ≈0、診断器は behavior 記述子を使わず地形幾何を直接見る)。ただし ESN_3param の midpoint の **90.9% が下方に dip** していて、最大相対 dip=0.0435 は C1 谷閾 0.05 の直下 (13% 以内)。だから精密に言うと「**真に単峰**」ではなく「**C1 閾値を僅かに下回る浅い谷 (~2–4%) を持つ弱 multi-basin**」。(B) null の方向は維持されるが、頑健性は閾値近接ゆえ限定的。
3. **[clip_flip_validity] K4 降格は低予算ゆえ "at this budget" 限定**。verdict_flip=False は確かだが、FPR 0/0 は床値、予算は 7 倍縮小。だから「firm refutation」より「not load-bearing at this budget」と述べるべき。

3 つとも「結論をひっくり返す」ほどではないが、「言い過ぎを削る」方向で全部効いた。この自己監査こそ今日の成果の半分です。

---

### 8. 自分が踏んだミスを 1 つ正直に書く

前回の谷深さ workflow で、2 段目のオーケストレータ briefing に **stale (古い) な値** を渡してしまいました。「全 below threshold / d*=0.1234」みたいな値です。ところが実際に commit されている結果 JSON は `all_below_threshold=false` でした。前回の workflow 結果を読んだとき、別のメトリックの値を取り違えていたのです。

これを **敵対検証が検出して、verdict を N/A に格下げ**しました。つまり「整いすぎた結論」を自分で疑うプロセスが、自分のコピペミスを捕まえた。気持ちのいい話ではないけれど、これが回ったから今日の Step D で正しい足場から測り直せた。

honest disclosure は「失敗を消さない」だけでなく、「**失敗を検出する仕組みを先に置いておく**」ことなんだな、と改めて思いました。

---

### 9. 過去 verdict をどう更新したか

| 過去 verdict | 過去の読み | Step D の更新 |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **方向更新: ③ は NOT null の方向 (fresh n=64 で gate PASS)**。ただし候補止まり |
| step6 exp7 (実 ESN proxy, ③ negative) | n≤10 盲点域, 「再測必須」 | **大幅更新: 地形が本当に滑らか (③不要) を noise-free で確定**。再測しても多峰は出ない |
| 谷深さ N/A (計測不能) | instrument 不能 | **解消: 決定論化で計測可能化** → vf≈0 (単峰)。ただし閾値近接の浅い谷が留保 |
| K4 clip = 唯一の能動的 suppression | 「clip が landscape 構造を隠蔽」 | **降格: 診断的所見** (not_load_bearing_at_this_budget) |

「③不要に見えた過去 negative の多くは underpower ではなく、地形が本当に滑らかだった」── この一点が、実 substrate 上で初めて確かめられたのが今日の核です。

---

### 10. 外部レビュー (Codex) はブロッカーなしで追認

llcore の規律として、各 capstone は Codex (gpt-5.4, read-only) のペアレビューを通します。今回の総評は **「ブロッカーなし ── ③ 結論を外部確認」**。

- C-gen4b を load_bearing でなく候補止まりにした判断は妥当 (更新検出力 0.5174 < 0.80 を JSON で確認)。
- EXP2 の決定論・非循環は clean。「真に単峰」より「閾値下の弱 multi-basin」が精密、という本文の自認も追認。
- EXP3 の K4 降格は現予算なら妥当 (FPR 0/0 + 7倍縮小ゆえ at-this-budget 限定)。

指摘された 4 件 (CF1〜CF4) は **すべて将来 rerun 時の harness 堅牢性と文言精度** であって、現結論を覆すものではありません。GPU で③を再検定するとき、これらを適用してから harness を再利用します。

---

### 11. CPU の抜け道 (kernel 多様化 / BG9) を試していた

「③ の本丸は GPU (実 LLM の損失地形) へ」が EXP2 の推奨です。実 proxy が滑らかと確定した以上、滑らかな地形で③を追っても (A) は出ない (地形が一つ山なら選り分けに利得がないのは当然)。

ただし GPU は投資判断なので、**CPU で前進できる別仮説**を並行して試していました。それが **kernel 多様化** です。

仮説はこうです。個々の kernel (rwkv / mamba / hopfield / linear_attn) が滑らかでも、**4 種類の kernel 族を union すると、kernel 切替の瞬間に fitness が不連続に段差を作る → 地形が multi-basin (だまし地形) になりうる → ③が GPU なしで CPU 上で load-bearing になりうる**。これを検証するのが BG9 でした。

この記事を最初に書いた時点では「いま BG6 (task → best-kernel 写像が非定数か、つまり「タスクごとに得意 kernel が違うか」) を smoke 測定しているところ」でした。その後 (同じ 2026-06-02 中に) BG9 の決着がつきました。次の追記節がその結末です。

---

### 11.5. 追記 (2026-06-02): BG9 決着 — 抜け道は構造的に閉じていた

> 結論を一行で: **BG9 = N/A (構造的)。つまり kernel 多様化という CPU 抜け道は「③ が立たないことが構造的に決まっている」ので閉じた。** 「③ が要らない」ではなく「この空間では③が強 baseline と原理的に分離できない」という、情報量のある negative です。

§11 で仕掛けた抜け道の結果が出ました。期待した「kernel union で multi-basin (だまし地形) が生まれて③が CPU で立つ」は **起きませんでした**。しかも「たまたま立たなかった」のではなく **構造的に立てない** ことが分かった。BG9 はこれを 3 段の証拠で確定しています。

#### (1) substrate validity — 「弁別はあるが弱い」(PASS だが要注意)

まず「タスクごとに得意 kernel が違うか」(BG6) を、kernel-favoring task 群を第一原理で設計し直して測ったところ、写像は **非定数 = 非 inert (PASS)**。mamba / linear_attn / rwkv はそれぞれ別タスクで best になりました。BG6 で踏んだ「memory_tasks は kernel 中立」の轍は回避できた、という意味では前進です。

ただし正直に言うと **弱い**:

- **hopfield はどのタスクでも勝てなかった**。これは hopfield kernel が **対角スカラ mock** で、tanh アトラクタが機能不全だったため (per-seed の R² が 0/0.99/0 と二極化)。つまり実質「4 kernel union」ではなく **3 kernel** です。
- clean な専門化は 2 軸のみ (selective_copy↔mamba / weighted_accum↔linear_attn)。残りは margin が薄く fragile。

→ **弁別の存在 ≠ 多峰/障壁**。non-inert 化には成功したが、それが欺瞞地形 (だまし地形) を保証するわけではない、という所まで。なお対角 mock の限界は kernels.py のスコープ宣言どおりで、ここでは **機構の feasibility のみ主張** (full kernel 性能は非主張) です。

#### (2) harness validity — positive control が validate しない (これが決め手)

次が本丸です。固定パラメータ (behavior=(kernel_id, theta L1)) で MAP-Elites (③) を、3 つの baseline ── **RR-hillclimb (random restart 山登り)** / panmictic-GA / random ── と honest に paired 比較しました。

| 基質 | 結果 |
|---|---|
| **positive control** (合成 kernel-barrier) | ③ は panmictic (+0.423) と random (+0.208) は撃破。**だが RR には勝てない** (+0.051, p=0.31 → FAIL)。3 baseline 全勝に届かず = **harness validity が立たない** |
| **negative control** (kernel 中立タスク) | 全 method R²≈1.0 飽和、③ 優位なし = **正しく null** (false-positive なし、計器は健全) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3、panmictic が逆に③を上回る = **③ 勝たず** |

ここが Step D (技術版 §4-7) と決定的に違う点です。Step D の欺瞞 corridor では③が RR を排除できました。**なぜ kernel 空間ではできないのか?** 根因は 1 つ:

> **RR は restart のたびに kernel_id ∈ [0,4) を直接サンプルできる。** kernel 選択は 4 離散の単一座標 (低次元) なので、RR は restart で全 4 kernel を直撃する。「best kernel を探す」のに谷を跨ぐ必要がない = **teleport (直接ワープ)**。だから③ の behavioral niching に出番が来ない。

Step4 の corridor で③が RR を排除できたのは、そこの behavior が `mean(24次元)` で、CLT により平均が 0.5 に集中 → 大域ピークが measure-zero 域 = **random/RR が直接サンプルできない高次元**だったからです。kernel_id は逆に低次元で直接サンプルできてしまう。

#### (3) red-team — 敵対検証でも反証できず、むしろ確証

「harness が立たないのは本当に構造のせいか? たまたまの設定ミスでは?」を独立 red-team で叩きました。結果は構造主張を **反証できず、むしろ強化**:

- **機構確証**: instrumented RR が positive control 上で 4 basin に restart kid を [12,18,16,18] とほぼ一様分散、target 到達 88%、best は restart→in-basin climb が 6/8 seed。「RR は restart で kernel_id を直接サンプルして谷を回避する」を **数値で確証**。
- **4 つの faithful 構成 (高次元 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) すべてで③は RR に勝てない (beats_rr=False)**。corridor を緩めると RR も同等到達、締めると③が **先に starve** (餓死)。
- **境界 sweep**: theta corridor の次元を D=0→3 と締めるほど③が RR より速く starve (D=3: ③ reach 0.08 vs RR 0.42)。base_seed 3 通りで同一。

→ **「RR だけ排除して③が通る behavior 次元は、kernel 空間に構造的に存在しない」** を定量確証。

#### 構造的洞察 (この決着の payoff)

> **③ (MAP-Elites の behavioral niching) が強 baseline を上回るのは、「難所」が高次元 behavior 空間にあって直接サンプリング (random restart) で到達できないときだけ。**

- **kernel 選択は低次元 (4 離散の単一座標)** → RR が直接サンプル → ③ の niching 優位が原理的に出ない。
- theta 空間に欺瞞を移しても、RR は restart 後に in-basin で greedy climb するので、corridor を RR が抜けられない程度に締めると③も同程度に starve する。**RR fail ∧ ③ succeed の窓が存在しない。**

これは Step4 §7 で残った問い「探索空間を kernel 多様化で拡張すれば③が unlock するか?」への答えです。答えは **NO (CPU では構造的に)**。拡張が③を unlock するには、追加した自由度が **高次元で直接サンプル困難**な behavior を生む必要がある。kernel 選択 (低次元・離散) はその条件を満たさない。

#### GPU への含意

- **CPU 出し切りゲートが CLEAR**: BG9 が最後の CPU 路 (kernel-union) を構造的に閉じた。③ の残り路は **高次元の GPU full-LLM 損失地形のみ**。
- 構造的洞察は GPU の賭けを **better-motivated** にします。③ は高次元 behavior で初めて意味を持つ。full-LLM のパラメータ空間は数百万次元 = まさに高次元。だから GPU 検定は「full-LLM だけが例外かも」という弱い賭けでなく「③ は高次元を要し、full-LLM が高次元域」という原理に沿う。
- **ただし依然 bet**: 実 LLM 地形が backprop 系の強 baseline で直接ナビゲートできるなら③不要 ── これは **BG9 の RR と同型のリスク**です (「強 baseline が直接解く」可能性は GPU でも残る)。だから GPU は「③のため単独」でなく **ポートフォリオ判断** (llive 実 LLM fitness 等と相乗り) + **クラウド借りで事前登録 1 本** (資本コミット前) が適正。BG9 の構造的洞察そのものが GPU の falsifiable な go/no-go 基準になります:「③ が full-LLM で load-bearing なら、その難所は高次元 behavior 空間にあり直接サンプル/backprop で到達困難なはず」。

#### honest 留保 (重要)

- これは **「③不要と判明」ではありません**。「③ がこの低次元 kernel 空間では強 baseline と原理的に分離できない」= N/A (構造的) であって、③ の機構自体は Step4 で本物と確定済みです。N/A だが「kernel 路は閉じている」という決定的情報を持つ **情報量のある N/A** です。
- harness/red-team は smoke 規模 (5-12 seed)。本検定 15 seed では数値は動くが、**構造 (締めると③が先に starve / RR が kernel_id を直接サンプル) は seed 非依存で頑健**。real の full ≥15-seed 本検定は実施しません ── positive control validity が構造的に立たない以上、real で③不要が出ても「③不要 vs 検出器盲」を分離できず、その「検出器盲 = kernel 空間の構造」を red-team が既に確定したので、CPU を 7.5h 投じても結論は変わらないからです。
- substrate は弱い (実質 3 kernel、**hopfield は対角 mock で機能不全**)。より強い kernel 弁別 (full 実装・非対角) なら別結論の余地は **理論上**あるが、③ の構造的障壁 (低次元選択 → RR 直接サンプル) は kernel 実装の質と独立です。
- 「整いすぎた③成立」を疑う規律は今回は **不要でした** ── ③成立は最初から出ていない (honest prior 通りの negative)。

---

### 12. メタ教訓 — 正直さは、勝つための道具だった

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

---

## 第10章 (連載 #34) 山登り 6 連戦で分かった「いつ進化の③は効くのか」— そして 100 年前の進化生物学が同じ答えを出していた

<!-- KAMI -->
> 📖 **ざっくり言うと**
>
> 前章(#33)が決着の「最終局面」だったのに対し、本章は同じ問い「③は要るのか?」をめぐる 6 段の実験を、ひとつの物語として俯瞰します。まず「だまし地形なら③は圧勝する」と存在証明し、次に実問題に近い 4 つの地形で測りに行ったら、ことごとく「③は要らない地形」だった——その弧を辿ります。たどり着いた核心は「③が効くのは、難所が高次元にあって直接たどり着けないときだけ」。そして驚くべきことに、この境界条件は 100 年近く前の進化生物学の論争(ライト対フィッシャー)が既に同じ形で描いていた、という接地まで踏み込みます。ただし生物学は計算結果を「証明」するのでなく「たとえとして接地する」だけ、と慎重に線を引きます。
<!-- KAMI -->

### TL;DR

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


![けだるく目を閉じる明美](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/061.jpg)
> 🗒️ *「バカのフリも疲れるわね…!」— 100年分を語り終えての脱力*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

---

### 0. この記事は何の話か (コンセプト)

`llcore` は「Transformer のコア計算 (状態更新則・学習則・認知駆動 Δ) を遺伝子にして、Z3 で壊れないように検証しながら進化させる」CPU 完結の研究フレームワークです。

その進化エンジンには、進化の 4 要素 (① 変異 / ② 遺伝 / ③ 適者生存・分離 / ④ 過剰繁殖) のうち、**③ (selection / separation)** をどう効かせるか、という設計上の急所があります。多様性を保ってニッチに残す MAP-Elites のような「選り分けて分けて育てる」仕組みです。

問いはシンプルです。

> **その③、本当に要るの?**

要るなら、③を載せるための重い投資 (最終的には GPU で実 LLM を回す) に意味がある。要らないなら、③にこだわるのは時間と電気の無駄になる。

連載 #33 では、その問いの **最終局面** (Step D の決定論測定 + BG9 の構造的決着) を詳しく書きました。でも、そこに至るまでには **6 段の実験**があり、勝ったり (存在証明)、測れなかったり (N/A)、負けたり (honest negative) を繰り返していました。この #34 では、その **arc 全体を 1 つの物語**として並べ直します。さらに今回の目玉として、**この計算結果が 100 年近く前の進化生物学の論争 (ライト対フィッシャー) と驚くほど同じ形をしている**ことを、検証済みの一次情報で接地します。

— ここまで 40 秒。準備運動おわり。本題へ。 —

---

### 1. たとえ: 山登りと、だまし地形と、記憶の宮殿

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

### 2. arc 全体マップ — 6 段の山登りを一望する

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

### 3. 第I段 (Step 4) — 存在証明: だまし地形なら③は圧勝する

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

### 4. 第II段 (Step C / 梯子1) — 基質の「床」と「天井」に阻まれる (N/A)

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

### 5. 第III段 (E-A) — 多タスク汎化: ③は要らなかった (honest negative)

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

### 6. 第IV段 (Step D) — 実 proxy 地形は「本当に滑らか」と確定 (noise-free)

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

### 7. 第V段 (BG9) — 部品を混ぜる抜け道は、構造的に閉じていた

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

### 8. 構造的洞察 — 6 段を 1 つの条件でまとめる

存在証明 (I) と 4 つの negative (II〜V) は、たった 1 つの条件で全部つながります。

> **③ (behavioral niching) が強 baseline を上回るのは、「難所」が高次元 behavior 空間にあって、直接サンプリング (ランダムリスタート) で到達できないときだけ。**

- **第I段が満たす理由**: behavior = `mean(24 次元)`。平均は中心極限定理で 0.5 に集中し、大域ピーク (mean≈0.9) は実質 measure-zero。random も restart も**直接届かない**。だから飛び石を残してラチェットする③が必須。
- **実 CPU 基質が満たさない理由**: 難所が低次元。ESN テキスト proxy の制御座標は実質 leak rate (滑らかな低次元ノブ、そもそも谷が無い)。kernel union の難所は「どの kernel か」= 4 択の単一離散。RR が直接サンプルして全 basin に teleport するので、渡るべき谷が無い。

だから第II段の「遺伝子空間の多峰性 1.000」は十分条件ではない ── 遺伝子は谷だらけでも、難所が低次元 behavior 座標に集中していれば、restart が直接届く。**効いてくるのは "探索が到達すべき behavior の次元" であって、遺伝子の次元ではない**。

---

### 9. 生物学的接地 — 100 年前の進化生物学が、同じ答えを出していた

ここからが #34 の目玉です。**「多様性を保つ選択は、狭い条件でだけ効き、それ以外では冗長」** ── この境界条件には、20 世紀の進化生物学に異常にきれいな先例があります。

> ⚠ **honesty 契約**: 以下の生物学は **「たとえ話 (structural analogy)」であって、私たちの計算結果の証明ではありません**。対応は構造的で、機構レベルでは一致しません。たとえがずれる箇所は全部その場で明記します。引用する論文は、別途一次情報で存在・帰属・主張内容を照合したものだけです。

#### 9.1 ライト (Wright) のシフティング・バランス説 = ③の先例

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

#### 9.2 ライト対フィッシャー = 次元 (地形の形) の軸

ライトと同時代のフィッシャー (R. A. Fisher, 1930) は逆を主張: **大きな panmictic 集団 + 加法的分散へのマス選択で十分**に適応は進む、わざわざ分割は要らない、と。

二人の **一番深い対立軸は、実は「エピスタシス (遺伝子間相互作用) と地形の形」** でした。ライトは「非加法的相互作用ゆえ地形は**でこぼこ多峰**、だから谷を渡る drift が要る」と仮定し、フィッシャーは「相互作用はあるが重要でない、地形はほぼ**単峰で滑らかに登れる**、だからマス選択で足りる」と判断した。

**この epistasis/ruggedness の軸が、まさに私たちの結果が生きている次元です。地形の形 (topology) こそが全問題**。地形が本当にでこぼこ高次元なら (ライト regime) 多様性が谷を渡し、滑らか or 難所が低次元なら (フィッシャー regime) マス選択 ── すなわち **強いランダムリスタート山登りの生物学版** ── で既に足りる。私たちの ESN テキスト proxy は noise-free で滑らか、kernel union の難所は低次元離散。**どちらもフィッシャー regime** で、③は効かないし効かなかった。

> 細かい注意 (正直に): 「フィッシャーは drift を無視した」は俗説の圧縮です。正確には「drift はあると認めたが、大きな集団では量的に無視できると判断した」。完全否定ではない。

#### 9.3 私たちの negative = コイン批判の計算版

一番効いてくる対応は、ライトの **提案**ではなく、生物学界の **経験的判定**の方です。Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) はシフティング・バランス説を理論・実証の両面から評価し、こう結論しました (全文照合済み)。

- **マス選択でたいてい足りる**。「ライトの三段階機構の方が単純なマス選択よりうまく説明できる実例はほとんど無い」。人為選択実験も「分割集団の選択が大集団のマス選択より大きな応答を生む」ことを示せなかった。
- **シフティング・バランスが効くのは限定的・稀少な条件下だけ**。集団構造の経験的推定からは「**浅い谷で隔てられたピーク間でしか drift は移動を起こせない**」(深い谷は drift では稀にしか渡れない)、しかも **大半の適応は谷渡りを必要としない**。

これは私たちの結果の **驚くほど正確な生物学版**です。彼らの言葉を私たちの語彙に翻訳すると ── **地形が真にだまし的/高次元でないなら、ふつうのマス選択 (≒強いランダムリスタート山登り) で既に解け、多様性維持の装置はほとんど何も買わない**。「現実の谷はたいてい浅い、大半の適応は谷渡り不要」は、私たちの「**実地形はたいてい単純だから niching は冗長**」の生物学的言明です。

> **honesty 注意 (3 点)**:
> 1. **彼らはシフティング・バランスを「反証」していない**。Phase I/II は起こりうると明言し、6 件の経験事例も挙げている。主張は **より狭い確率的なもの** (「一般的・重要な機構とは言い難い」) であって、「refuted」と書けば言い過ぎ。
> 2. **論争はまだ決着していない**。Wade & Goodnight (1998)、Peck et al. (1998, タイトルが文字通り「feasible」と主張) が反論し、Coyne らの 2000 年の再反論、Goodnight & Wade の同号反論と続いた。1997 批判を「最終結論」として引いてはいけない。
> 3. **生物には計算側に対応物のない機構があり、しかも私たちより強い主張をしている**。Phase III では、多様性を守る gene-flow 障壁が **良い解を周辺 deme に閉じ込めて広がりを妨げる** = niching が **逆効果**になりうる。私たちの stateless な離散選択設定にはこの cost の対応物が無いので、ここは **過剰に重ねない**。生物の方が一段強い主張をしている箇所です。

#### 9.4 二つの実例 — 低次元の蛾と、高次元の大腸菌

私たちの主張には 2 つの極 (低次元 = ③不要 / 高次元 = ③が効きうる) がありますが、進化生物学はそれぞれにきれいな実例を持っています。

**低次元の極 ── オオシモフリエダシャクの工業暗化 (= BG9 kernel ケース)**: *Biston betularia* の carbonaria (黒) vs typica (白) は **単一メンデル座位・少数アレル** (原因変異は cortex 遺伝子への転移因子挿入; van't Hof et al. 2011/2016) で、**強い方向性選択** (s ≈ 0.1-0.2; Saccheri et al. 2008; 捕食は Cook, Grant, Saccheri & Mallet 2012 で再確認) を受ける。最適は各時点で単峰、環境でシフトするだけ。**単純な方向性選択 ── greedy 山登り/ランダムリスタートの生物学版 ── が直接、適者モフを固定し、多様性維持機構は不要だし呼ばれていない**。これがまさに BG9: kernel 選択は 4 択の低次元単一座標で、RR が全 kernel を直接サンプルし、③が構造的に分離できない。**暗化モフ = BG9 kernel ケースの生き物版**。

> 注意 (正直に): 移行期には多型が一時保たれるが、それは **空間的環境不均一 + 遺伝子流動 (移住-選択平衡)** によるもので、内在的な多様性保存機構ではない。たとえが少しずれる箇所。

**高次元・歴史依存の極 ── レンスキーの Cit+ (= ③ regime)**: 大腸菌長期進化実験 (LTEE) で、好気的クエン酸利用 (Cit+) は **12 集団中ちょうど 1 つ**で約 31,500 世代目に進化した (Blount, Borland & Lenski 2008)。鍵は **順序立った potentiation (前駆変異の蓄積) → actualization (citT のタンデム重複によるプロモータ捕獲) → refinement** という高次元・歴史依存の経路 (Blount et al. 2012)。リプレイ実験が「歴史的偶発性」を「一定率の稀変異」から区別した。これは contingency・epistasis・高次元でこぼこ地形を探索する価値を **本物で例示**する ── ③ が効きうる regime の実例です。

> **honesty 注意 (これは私たちの条件文の "前件" にしか対応しない)**:
> - **LTEE は niching アルゴリズムを使っていない**。ただの自然選択で、12 並列集団は **それ自体がランダムリスタート的な設計**。だから「contingency + 多様性が稀な革新を可能にする」存在証明であって、「niching が強 restart baseline に勝つ」証拠 **ではない**。
> - 「大腸菌がゼロからクエン酸を食べる力を獲得」は俗説の誇張。革新は **制御 (既存トランスポータの好気発現) = exaptation** で、新規遺伝子でも新規生化学でもない。
> - Van Hofwegen et al. (2016) が「直接選択ならもっと速く Cit+ が出る」と示し、「稀/偶発」枠組みに異議を唱えた (Lenski 側は LTEE 条件下の potentiation とは矛盾しないと反論)。「極めて稀/長期遅延」物語に寄りかかるなら、この **係争中の追試**も併記すべき。

#### 9.5 接地のまとめ

| 極 | 生物学 | 地形 | ③は効く? | 私たちの基質 |
|---|---|---|---|---|
| 低次元/滑らか | 暗化モフ (単一座位, s≈0.1-0.2, 方向性) | 単峰・シフト | **No** — マス選択で十分 | BG9 kernel union; ESN/ridge テキスト proxy (決定論・滑らか) |
| 高次元/偶発 | レンスキー Cit+ (potentiation→actualization→refinement) | でこぼこ・変異で谷越え | **Yes** (効きうる regime) | 合成だまし corridor (behavior = 24 次元の平均) |
| 経験的判定 | コイン・バートン・トゥレリ: マス選択でたいてい足りる、シフティング・バランスは稀にしか決定的でない | 実地形はたいてい単純 | 私たちの **negative の鏡** | 試した全 CPU 基質 |

**結論**: ライトのシフティング・バランスは「③が効くとき**なぜ**効くか」の正しい生物学先例、ライト-フィッシャーの epistasis/ruggedness 軸は「**次元**条件」の正しい枠組み、暗化モフとレンスキー Cit+ は低次元/高次元の clean な両極、コイン批判は私たちの **negative** の生物学先例。**ただし、これらは計算結果を証明しない。接地するだけ**。たとえが一番ゆるむのは、生物が cost (Phase III の gene-flow trap) を加える点 ── 私たちの stateless 設定にはそれが無い。

— 一服。100 年前の論争が同じ形だと気づいたときは、正直ゾクッとしました。ただし「ゾクッとした」を「証明」と取り違えないのが今回の規律です。 —

---

### 10. GPU への含意 — 残された路は高次元だけ、しかし依然 bet

arc は CPU の路を全部閉じました。実 proxy は noise-free で滑らか (IV)、最後の候補 (kernel 多様化) は構造的に閉じた (V)。③の残された路は **高次元の地形のみ** ── それを提供するのが **full-LLM のパラメータ/損失空間 (数百万次元)** です。

構造的洞察は GPU の賭けを **better-motivated** にします。「full-LLM だけが例外かも」という盲目的な賭けではなく、「**③ は高次元を要し、full-LLM が高次元域**」という原理に沿う賭けになる。

**ただし依然 bet**。生物学の Cit+ が「③ アルゴリズムの勝利」を証明しないのと同じ理由、そして BG9 で RR に勝てなかったのと同型の理由で ── **実 LLM 地形が backprop (勾配降下) という強 baseline で直接ナビゲートできるなら、③はやはり不要**。難所が高次元なのは **必要条件であって十分条件ではない**。「強い直接法が解けない」ことを追加で示す必要がある (CPU では RR、GPU では勾配降下)。

だから GPU は「③のため単独」でなく **ポートフォリオ判断** (llive の実 LLM fitness 等と相乗り) + **クラウド借りで事前登録 1 本** (資本コミット前) が適正。go/no-go 基準も falsifiable に書けます:

> **full-LLM の難所は behavior で高次元か、かつ強い直接 baseline (勾配降下) で到達困難か?** 高次元でも勾配が直接届くなら③不要 (= BG9 の RR 結果の GPU 版)。

---

### 11. メタ教訓 — 正直さは、勝つための道具だった

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
