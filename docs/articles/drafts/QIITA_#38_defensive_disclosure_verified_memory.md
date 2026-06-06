---
title: 'llcore 検証 arc (#38) — 自分の研究を 56 体の AI に反証させたら「四隅の空白」が残った日: 特許を出さずに「防衛的公開」で旗を立てる'
tags: [FullSense, llcore, Singularity, AI, 解説]
private: false
updated_at: '2026-06-06'
slide: false
ignorePublish: false
id: fa55b499b45a871a97db
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

# 日本語

## この記事は何か — 1 日で「反証検証 → 特許 clear → 出願見送り → 防衛的公開」まで走った話

2026 年 6 月 6 日、私(筆者)は AI(Claude Code)に **「我々のやっていることが本当に差別化できているか、検証してほしい」** と求めました。AI はこれに **反証検証(adversarial verification)** — 自分の主張をわざと反証しにかかる検証役の AI を多数走らせ、それでも生き残るかを試す手法 — で応えました。56 体の検証エージェントが 7 + 3 の角度から「この主張は先行研究で反証できるはずだ」と反例を探し回り、別働隊が特許データベースまで照会しました。

結果は次のとおりです。

- **学術文献での反証(breaks): 0 件**(44 候補を個別判定して、誰も「四隅同時」を埋めていなかった)
- **特許での反証: 0 件**(英語 14 + 日本語 3 クエリで、交差点を占有する特許なし)
- そこで私は **特許を出さない**(コスト判断)と決め、代わりに **防衛的公開(defensive publication)** という旗を立てました。

この記事は、その 1 日の物語(反証検証の設計と結果、意思決定)と、**公開した中身(=四点交差点の技術)** のかみくだき版です。記事の順番は、いつものとおり ①用語の説明 → ②かみくだき(平易) → ③詳細 で進みます。

---

## ① 用語ミニ辞典(本文で詰まらないために)

| 用語 | ひとことで |
|---|---|
| **反証検証 (adversarial verification)** | 自分の主張を肯定するのでなく、わざと反証・否定しにかかる検証役(AI)を多数走らせ、それでも生き残るかで主張の強さを測る方法。身内の太鼓持ちでなく、批判者を雇うイメージ。 |
| **防衛的公開 (defensive publication)** | 特許を「取る」のではなく、技術を **公開して先行技術にする** こと。誰か(大手含む)が後から同じ発明で特許を取って、こちらや世間を縛れないようにする「先に旗を立てる」防御。 |
| **先行技術 (prior art)** | 「その発明、もう公知ですよ」と言える既存の公開物。新規性を否定する材料。日付が命。 |
| **縮小性 (contraction, ρ<1)** | エコー(過去の揺れ)が時間とともに **減衰** する性質。スペクトル半径 ρ が 1 未満。ばねが必ず止まる位置に戻る、のイメージ。記憶コアが暴走せず「忘れる」性質。 |
| **健全な証明 (sound proof)** | 「証明できた」と言ったら **本当に正しい**(偽の合格を出さない)証明。統計的に「たぶん安全」とは別物。 |
| **prove-then-reject ゲート** | 変異(更新)を **証明してから採用**、ダメなら **棄却** する関所。fail-closed(証明できなければ通さない)。 |
| **記憶コア (memory core)** | LLM の周りに被せる「覚える部品」。本研究では `s_{t+1} = decay⊙s + (1−decay)⊙tanh(W s + V x)` という漏れ・飽和つきの再帰(RWKV 系)。 |
| **進化ループ (evolution loop)** | 変異 → 選択 → 次世代、を回して良い個体を探す最適化。ここではその選択の関所に証明ゲートを置く。 |
| **SMT ソルバ (Z3 等)** | 論理式が充足可能か解く万能ソルバ。重い。本研究では「実は要らなかった(装飾)」が結論。 |
| **tracking tube(追従チューブ)** | 「望ましい軌道」からの実際のずれが収まる **筒(半径 r)** の保証。`r = G·w̄/(1−L)`。 |
| **SSGM** | 「進化する記憶を統べる」write ゲートを **理論だけ** で提案した先行研究(arXiv:2603.11768, 2026)。看板が一番近い相手。 |
| **navigability(探索可能性)** | 進化が「動きやすい地形か」。学習が賢くなることとは別。検証器の効き目はこちら側。 |

![四点交差点 — 4 条件が同時に重なる中心だけが差別化核](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_intersection.svg)

---

## ② かみくだき — 3 分でわかる全体像

漫画でたとえます。主人公(私たちの研究)は「**証明してから採用する関所**を、進化する AI 記憶の心臓部に取り付けた」キャラです。技は 4 つの条件を **同時に** 満たすと発動します。

1. **健全な縮小性証明**(エコーが必ず減衰すると数学的に保証。しかも偽の合格を出さない)
2. それを **LLM の記憶コアの内部** に当てる(制御ロボでも分類器でもなく、「覚える部品」そのもの)
3. **進化ループの中で**、ダメな変異を **棄却**(押し戻し=射影ではなく、捨てる)
4. しかも **動く実装と実験** がある(机上論で終わらない)

この 4 つを **同時に** やっている先行研究は、56 体の反証役 AI に批判的に検証させても、特許 DB を照会しても、見つかりませんでした。1 つ 1 つの条件は先行があります(正直に全部名前を出します)。でも「四隅を同時に占有」した人はいなかった。これが **四点交差点(four-point intersection)** です。

ここで生物学のたとえを 1 つ。進化では「ニッチ(他種がいない隙間)を占めた種」が生き残ります。大手(OpenAI/Google 等)は「平均的に賢い大型種」で平野を支配しています。私たちは平野では勝てない。だから **誰も埋めていない四隅の隙間** に潜り込む。それが今回の戦略です(孫子でいう「実を避け虚を撃つ」)。

そして大事な意思決定。この隙間は **特許でも空白** でした。普通なら「じゃあ特許を取ろう」となります。が、特許はお金と時間がかかる。私はそこを **見送り**、代わりに **「公開して先に旗を立てる」防衛的公開** を選びました。狙いは攻めではなく **防御** です — 後から誰か(大手や、SSGM の後続実装)が同じ概念で特許を取って、こちらや公衆を縛るのを **未然に無効化する**。日付付きで公開してしまえば、それは公知の先行技術になり、後出しの特許は新規性で否定されます。

ただし — ここが私たちの一貫した規律ですが — **盛りません**。「世界初」とは言いません。正しい言い方は **「我々の反証検証の範囲で、四隅を同時に占有した先行はゼロ」** です。探索範囲の外は分からない、という留保を必ず残します。

---

## ③ 詳細 — 1 日のセッションと、公開した技術の中身

### 3.1 反証検証の設計(再現できるように)

「自分の研究は強い」と自分で言っても意味がありません。そこで AI は **反証主導のワークフロー** を組みました。

- **7 角度の反証探索**: 証明ゲートの系譜 / certified training / Transformer 安定性 / 進化 × 検証 / verified memory / runtime assurance / 産業・特許。
- **critic が指摘した盲点 3 角度を追加**: 形式手法会議側の逆引き / certified continual learning の語彙系 / 内部状態・SSM の解釈。
- **44 候補を 5 軸ルーブリックで個別判定**(更新をゲートするか / 健全証明か / LLM 記憶コアか / 進化ループ内か / 実装ありか)。判定役の AI は **一次情報(arXiv の abstract/HTML)を WebFetch で必ず確認**(伝聞禁止)。
- 並行して **内部の AI が自分の論文ドラフトの弱点を抽出**(honest disclosure: 身内の粗探し)。

確定結論は **breaks 0 / narrows 36 / background 8(44 件)**。生き残った差別化核が、上の四点交差点です。

### 3.2 「四隅」それぞれの最近接ライバル(全部名前を出す)

新規性は「全部を 1 文で名指しできるか」で誠実さが決まります。隅ごとに最も近い先行を 1 文で:

- **SSGM([arXiv:2603.11768](https://arxiv.org/abs/2603.11768))** — 「進化する記憶を統べる」看板を **理論だけ** で先取り。ゲートは NLI(矛盾検出)で **健全な形式証明ではなく**、実装もなし。→ 看板を担う相手として **必ず引用**。実装 + 証明の窓が空いている。
- **SEVerA([arXiv:2603.25111](https://arxiv.org/abs/2603.25111))** — 自己進化エージェントに Dafny/SMT 検証。ただし対象は **出力契約** で、記憶コアの縮小性の毎更新ゲートではない。
- **PSV-Verus([arXiv:2512.18160](https://arxiv.org/abs/2512.18160))** — self-play ループ内の健全 SMT ゲート。ただし検証対象は **生成コードの正しさ**。
- **Provably Safe Model Updates / LID([arXiv:2512.01899](https://arxiv.org/abs/2512.01899))** — 更新を抽象解釈で δ-safe 認証。ただし **射影(押し戻し)** で prove-then-reject ではなく、対象は frozen-embedding の分類 head。
- **GP × モデル検査(Katz & Peled, [arXiv:1402.6785](https://arxiv.org/abs/1402.6785), 2014)** — 進化ループに健全な検査ゲートを置く **パターンの先例**。だから私たちは **ゲートのパターン自体を新規とは主張しません**。記憶コアの縮小性への適用だけが未踏。
- **Enforced-Lipschitz Transformers([arXiv:2507.13338](https://arxiv.org/abs/2507.13338))/ R2DN([arXiv:2504.01250](https://arxiv.org/abs/2504.01250))** — 縮小性を **構造で強制(by-construction)**。これは「ゲートなんか要らない、最初から組み込め」という最強の対抗設計。私たちは **by-construction 対 prove-then-reject** を設計軸として対比します(構造強制は表現力を犠牲にし、棄却ゲートは任意更新を構造制約なしに検査する)。
- **Safeguarded AI(ARIA programme)** — 最も権威ある proof-gated-gatekeeper 概念。ただしゲート対象は **行動/計画**(出力ゲート)で、重み/記憶の更新ゲートではなく、まだ programme 段階。
- **Emergent FV / substrate-guard([arXiv:2603.21149](https://arxiv.org/abs/2603.21149))** — AI の **出力** を Z3 で検証する動くシステム。ただし post-hoc 監視で、毎更新ゲートではない。

(上記 arXiv ID はすべて論文ドラフトで abstract と照合確認済みのものだけを使っています。)

### 3.3 特許面の照会(学術監査が残した穴埋め)

学術監査は **文献だけ** で、特許 DB を見ていませんでした(不在証拠として弱い)。そこで別働隊が **英語 14 + 日本語 3** のクエリで Google Patents / USPTO を照会しました。

- **交差点を占有する特許: ゼロ件。**
- 最近接の特許は 3 系統だけで、いずれも交差点外:
  - **[US11715005B2](https://patents.google.com/patent/US11715005B2)** — NN をハッシュ照合で真正性検証(健全証明でなく暗号ハッシュ)。
  - **[US10896032](https://patents.google.com/patent/US10896032)** — certify-then-deploy のガバナンスゲート(根拠が手続的 attestation)。
  - **[US11868855](https://patents.google.com/patent/US11868855)** — モデル/重みの「stability」検証(ただし可用性・耐障害の意味の蓋然性大)。
- 面白い構造的証拠: 「**健全証明で更新/記憶/進化をゲートする**」とクエリすると、特許 DB に site 指定しても結果がほぼ全部 **arXiv に逸れた**。これは「この概念がまだ学術段階に留まり、特許化されていない」間接証拠です。

→ 結論: **特許面でも clear**。ただし US10896032 / US11868855 は語彙が部分的に被るので、論文の related work に「展開ガバナンス型ゲート/運用安定性検証とは異なり、本研究は重み更新の解析的 contraction 性質を健全証明でゲートする」という対比を 1〜2 文先回りで入れています。

### 3.4 公開した技術の中身(防衛的開示の本体)

防衛的公開は「当業者が実施できる詳細度」で書かないと先行技術として弱い。なので、開示文書には次を **実装可能なレベル** で書きました。

![記憶コア式 — 漏れと飽和つき再帰 s(t+1) = decay⊙s + (1−decay)⊙tanh(W s + V x) の図解](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_core.svg)

**(a) 健全な縮小性証明器の梯子(ladder)。** 安いものから順に 3 段:
- `cert_inf` — 閉形式の ∞-ノルム上限(`O(n²)`)。各行の絶対値和が端点で最大になる性質を使い、**ソルバ不要**。
- `cert_two` — 全 `2^n` 頂点で SVD。
- `cert_sdp` — 共通 Lyapunov 行列を凸 LMI(内点 SDP, CLARABEL)で。

![証明器ラダー — cert_inf → cert_two → cert_sdp の 3 段、安い順に試す証明強度の階段](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_ladder.svg)

**ここが正直ポイント**: プロジェクトの旧通称は「Z3-gated」でしたが、**実際のゲートに SMT(Z3)は使っていません**。専用の Z3 縮小性トラックを走らせて確認したら、閉形式 ∞-ノルム証明器と **バイト単位で一致(3270 件中 0 件の不一致、境界近傍でも 8000 件中 0 件)**。つまりこの不変量クラスでは **Z3 は装飾** でした。だから看板を「健全な縮小性証明器の梯子」に直しています(これは退却ではなく強み — ソルバ依存と不完全性を回避できる)。

**(b) prove-then-reject ゲート(fail-closed)。** 子個体を提案 → 証明が通れば採用、ダメなら上限まで resample、それでもダメなら **既知安全な fallback** を採用。**未証明の子は決して採用しない**。`gate_mode="contraction"` / `"state_norm"` を additive に追加し、既定 `"none"` は従前挙動とバイト一致(=既存進化基盤への純粋な被せ物)。

![prove-then-reject ゲート — 子個体を提案し、証明が通れば採用・ダメなら棄却して再生成する fail-closed の関所](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_gate.svg)

**(c) tracking tube 検査指標。** 「どこかに縮む」だけでなく「**望ましい軌道に追従する**」を見たい、というユーザー要望への答え。ゲートが既に計算している量(状態 Lipschitz `L`、入力ゲイン `G`)と外乱上界 `w̄` を再利用し、追従誤差が収まる筒 `r = G·w̄/(1−L)` を **追加証明コストゼロ** で報告。小規模実測でも、縮小性 PASS の 3 gene は誤差/外乱比 0.50/0.78/1.04 で理論筒の内側、非縮小性の対照は **9.3 倍** に増幅(=ゲートは飾りでなく load-bearing)。

![tracking tube — 望ましい軌道のまわりに半径 r = G·w̄/(1−L) の筒が張られ、実際の軌道がその内側に収まる図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_tube.svg)

**(d) verified memory evolution の 2 ルート。**
- ルート (a): エージェント **記憶バンク** の更新を健全証明でゲート(SSGM の NLI 理論との差 = 健全証明 + 動くゲート)。
- ルート (b): 記憶コアの **内部状態 dynamics** をゲート(本書で実施済)。

**(e) 合成: SPC 管理図 runtime ゲート + 二層倫理ゲート。** 進化メトリクスを管理図(X̄–R / CUSUM)に通して時間方向の異常を online ゲート。そして **探索は自由・採用は検証** の二層倫理(探索層は孫子の「詭道」=奇手 OK、採用層は論語の「仁」=誠実でゲート不可避)。

### 3.5 本日の実装事実(reduced to practice)

机上論ではないことの証拠:

- 証明ゲートは **出荷側の `evolve()` に本配線済**(`gate_mode` / `resample_cap` を additive 追加、既定 `"none"` は byte-identical、research 側の参照実装と全モード一致をテストで実証)。
- tracking tube レポータも着地(`r = G·w̄/(1−L)`, `cert_inf` 限定、read-only、golden 値一致)。
- ゲート + レポータを覆うテスト **294 件**。
- **観測したゲートのコストは約 20〜60 倍**(証明はタダではない、と隠さず開示)。

### 3.6 honest 限界(弱めない)

防衛的開示でも honest disclosure は曲げません。

- **規模は小**: 核は `n=8`(72 実数 gene)・16 KB コーパス・byte vocab。「LLM 記憶コア」は **機構実証** の意味。
- **検証器の payoff は navigability であって学習ではない(L3)**: 効果は EA 固有で、勾配法では消える。
- **ゲートは ~20〜60 倍のコスト**: 短い訓練ではタダに見えるだけ。
- **「false admit ゼロ」は経験的観測であって機械検査ではない**: 証明器の *条件* は健全だが、それを担う *実装* は end-to-end に形式検証されたわけではない。
- **「未発見」の範囲**: 反証検証 + 表層特許検索の範囲に限る。CNIPA(中国語)未照会、特許は最長 18 ヶ月の公開ラグ。「探索範囲で」の留保は常に維持。

---

## まとめ — 旗は「攻め」ではなく「守り」のために立てた

今日 1 日で、私たちは自分の研究を 56 体の反証役 AI に批判的に検証させ、特許 DB まで照会し、それでも残った「四隅の空白」を確認しました。普通ならここで特許を狙うところですが、コストを天秤にかけて **出願は見送り**、代わりに **日付付きの防衛的公開** で旗を立てました。

狙いはシンプルです — **誰かが後からこの空白を特許で囲い込み、私たちや公衆を縛るのを未然に無効化する**。そのために、当業者が実装できる詳細度で全部公開しました。そして最後まで、**「世界初」とは言わず「我々の検証の範囲で四隅同時の先行ゼロ」** という、盛らない言い方を守っています。

防衛的公開の本体(日付付き開示文書)はこちら: [verified_memory_evolution_defensive_disclosure.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/papers/2026-06-06_verified_memory_evolution_defensive_disclosure.md)。

次回(#39 以降)は、この四点交差点の本丸 — verified memory evolution の小 PoC(記憶バンク更新ルート)の着地を report する予定です。SSGM が理論で看板を取った窓が、実装で閉じる前に。

---

# English

## What this article is — a day that ran from "adversarial verification → patent clearance → declining to file → defensive publication"

On June 6, 2026, I (the author) asked an AI (Claude Code) **"to verify whether what we are doing is truly differentiated."** The AI answered with **adversarial verification** — running many verifier AIs that deliberately try to refute and disprove our own claims, to see whether they still survive. Fifty-six verifier agents searched from 7 + 3 angles for counterexamples along the lines of "this claim should be refutable with prior work," and a separate detachment even queried patent databases.

The results were as follows.

- **Refutations (breaks) in academic literature: 0** (we judged 44 candidates individually, and no one had filled "all four corners at once").
- **Refutations in patents: 0** (across 14 English + 3 Japanese queries, no patent occupies the intersection).
- So I decided **not to file a patent** (a cost judgment), and instead planted a flag called **defensive publication**.

This article is a breakdown of the story of that one day (the design and results of the adversarial verification, and the decision-making) plus **what we published (= the technology at the four-point intersection)**. As always, the order is ① term explanations → ② breakdown (plain language) → ③ details.

---

## ① Mini-glossary (so you don't get stuck in the body text)

| Term | In a word |
|---|---|
| **Adversarial verification** | A method that, rather than affirming your own claim, runs many verifier (AI) agents that deliberately try to refute and disprove it, and measures the claim's strength by whether it still survives. Picture hiring critics instead of yes-men. |
| **Defensive publication** | Rather than "obtaining" a patent, **disclosing a technology to turn it into prior art**. A defense that "plants a flag first" so that someone (including a big player) cannot later patent the same invention and bind us or the public. |
| **Prior art** | An existing public document that lets you say "that invention is already public knowledge." Material that negates novelty. The date is everything. |
| **Contraction (ρ<1)** | The property that echoes (past perturbations) **decay** over time. The spectral radius ρ is below 1. Picture a spring that always returns to a resting position. The property by which the memory core "forgets" rather than running away. |
| **Sound proof** | A proof such that when it says "proven," it is **actually correct** (it never issues a false pass). A different thing from a statistical "probably safe." |
| **prove-then-reject gate** | A checkpoint that **adopts a mutation (update) only after proving it**, and **rejects** it if it fails. fail-closed (if it can't be proven, it doesn't pass). |
| **Memory core** | A "remembering part" placed around the LLM. In this research it is a leaky, saturating recurrence (RWKV-family) `s_{t+1} = decay⊙s + (1−decay)⊙tanh(W s + V x)`. |
| **Evolution loop** | An optimization that cycles mutation → selection → next generation to search for good individuals. Here, a proof gate is placed at the checkpoint of that selection. |
| **SMT solver (Z3 etc.)** | A general-purpose solver that decides whether a logical formula is satisfiable. Heavy. In this research the conclusion is that it "turned out to be unnecessary (decorative)." |
| **tracking tube** | A guarantee that the actual deviation from a "desired trajectory" stays within a **tube (radius r)**. `r = G·w̄/(1−L)`. |
| **SSGM** | Prior work that proposed a write gate "to govern evolving memory" **in theory only** ([arXiv:2603.11768](https://arxiv.org/abs/2603.11768), 2026). The closest rival in terms of the banner. |
| **navigability** | Whether evolution is "easy terrain to move through." Distinct from learning getting smarter. This is where the verifier's effect lies. |

![Four-point intersection — only the center where all 4 conditions overlap simultaneously is the differentiation core](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_intersection.svg)

---

## ② Breakdown — the whole picture in 3 minutes

Let me use a comic-strip metaphor. The protagonist (our research) is a character who "attached a **prove-then-adopt checkpoint** to the heart of an evolving AI memory." The special move activates when 4 conditions are met **simultaneously**.

1. A **sound contraction proof** (a mathematical guarantee that echoes necessarily decay — and it never issues a false pass).
2. Applying it **inside the LLM's memory core** (not a control robot, not a classifier, but the "remembering part" itself).
3. **Inside an evolution loop**, **rejecting** bad mutations (discarding them, not pushing them back = not projection).
4. And there is **a working implementation and experiments** (it doesn't end as armchair theory).

No prior work doing all 4 of these **simultaneously** was found, even when we had 56 verifier AIs critically scrutinize it and queried patent DBs. Each individual condition has predecessors (we name them all honestly). But no one had "occupied all four corners at once." This is the **four-point intersection**.

Here is one biology metaphor. In evolution, "a species that occupies a niche (a gap with no other species)" survives. The big players (OpenAI/Google, etc.) dominate the plains as "large species that are smart on average." We cannot win on the plains. So we slip into **the gap in the four corners that no one has filled**. That is this strategy (in Sun Tzu's terms, "avoid the solid and strike the void").

And the important decision. This gap was **also empty in patents**. Normally one would then say "OK, let's get a patent." But patents cost money and time. I **passed on that**, and instead chose **"publish and plant the flag first" defensive publication**. The aim is not offense but **defense** — to **preempt** anyone (a big player, or a successor implementation of SSGM) later patenting the same concept and binding us or the public. Once you publish with a date, it becomes public prior art, and a later patent dies on novelty.

That said — and this is our consistent discipline — **we do not inflate**. We do not say "world first." The correct phrasing is **"within the scope of our adversarial verification, there is zero prior work occupying all four corners simultaneously."** We always leave the caveat that we cannot know about what is outside the search scope.

---

## ③ Details — the day's session, and the substance of the technology we published

### 3.1 Design of the adversarial verification (so it can be reproduced)

Saying "my research is strong" yourself means nothing. So the AI built an **refutation-driven workflow**.

- **Refutation search from 7 angles**: lineage of proof gates / certified training / Transformer stability / evolution × verification / verified memory / runtime assurance / industry and patents.
- **Added 3 blind-spot angles the critic pointed out**: reverse lookup from the formal-methods conference side / the vocabulary system of certified continual learning / interpretation of internal state and SSMs.
- **Judged 44 candidates individually with a 5-axis rubric** (does it gate updates / is the proof sound / is it an LLM memory core / inside an evolution loop / is there an implementation). The adjudicating AI **always checked the primary source (the arXiv abstract/HTML) via WebFetch** (hearsay forbidden).
- In parallel, **an internal AI extracted the weaknesses of our own paper draft** (honest disclosure: nitpicking our own side).

The firm conclusion is **breaks 0 / narrows 36 / background 8 (44 items)**. The differentiation core that survived is the four-point intersection above.

### 3.2 The closest rival for each "corner" (we name them all)

Novelty's honesty is decided by "whether you can name all of them in one sentence." For each corner, the closest predecessor in one sentence:

- **SSGM ([arXiv:2603.11768](https://arxiv.org/abs/2603.11768))** — preempted the banner "governing evolving memory" **in theory only**. The gate is NLI (contradiction detection), **not a sound formal proof**, and there is no implementation. → **Must be cited** as the party carrying the banner. The window of implementation + proof is open.
- **SEVerA ([arXiv:2603.25111](https://arxiv.org/abs/2603.25111))** — Dafny/SMT verification for self-evolving agents. But the target is **output contracts**, not a per-update gate on the contraction of the memory core.
- **PSV-Verus ([arXiv:2512.18160](https://arxiv.org/abs/2512.18160))** — a sound SMT gate inside a self-play loop. But the verification target is **the correctness of generated code**.
- **Provably Safe Model Updates / LID ([arXiv:2512.01899](https://arxiv.org/abs/2512.01899))** — certifies updates as δ-safe via abstract interpretation. But it is **projection (pushing back)** rather than prove-then-reject, and the target is the classification head of a frozen embedding.
- **GP × model checking (Katz & Peled, [arXiv:1402.6785](https://arxiv.org/abs/1402.6785), 2014)** — a **precedent for the pattern** of placing a sound checking gate in an evolution loop. That is why we **do not claim the gate pattern itself as novel**. Only its application to the contraction of a memory core is unexplored.
- **Enforced-Lipschitz Transformers ([arXiv:2507.13338](https://arxiv.org/abs/2507.13338)) / R2DN ([arXiv:2504.01250](https://arxiv.org/abs/2504.01250))** — enforce contraction **by construction**. This is the strongest counter-design: "you don't need a gate, build it in from the start." We contrast **by-construction vs. prove-then-reject** as a design axis (structural enforcement sacrifices expressiveness; a rejection gate inspects arbitrary updates without structural constraints).
- **Safeguarded AI (ARIA programme)** — the most authoritative proof-gated-gatekeeper concept. But the gate target is **behavior/plans** (an output gate), not a gate on weight/memory updates, and it is still at the programme stage.
- **Emergent FV / substrate-guard ([arXiv:2603.21149](https://arxiv.org/abs/2603.21149))** — a working system that verifies an AI's **outputs** with Z3. But it is post-hoc monitoring, not a per-update gate.

(All arXiv IDs above use only those whose abstracts have been cross-checked in the paper draft.)

### 3.3 Patent-side inquiry (filling the hole the academic audit left)

The academic audit used **literature only** and did not look at patent DBs (weak as evidence of absence). So a separate detachment queried Google Patents / USPTO with **14 English + 3 Japanese** queries.

- **Patents occupying the intersection: zero.**
- The closest patents are just 3 lineages, all outside the intersection:
  - **[US11715005B2](https://patents.google.com/patent/US11715005B2)** — authenticity verification of NNs by hash matching (cryptographic hash, not a sound proof).
  - **[US10896032](https://patents.google.com/patent/US10896032)** — a certify-then-deploy governance gate (grounded in procedural attestation).
  - **[US11868855](https://patents.google.com/patent/US11868855)** — "stability" verification of models/weights (but very likely in the availability / fault-tolerance sense).
- An interesting structural piece of evidence: when you query "**gate updates/memory/evolution with a sound proof**," even with a site restriction on the patent DB, almost all results **veered off to arXiv**. This is indirect evidence that "this concept still remains at the academic stage and has not been patented."

→ Conclusion: **clear on the patent side too**. However, since US10896032 / US11868855 partially overlap in vocabulary, we proactively put 1–2 sentences of contrast into the paper's related work: "unlike deployment-governance gates / operational-stability verification, this research gates the analytic contraction property of weight updates with a sound proof."

### 3.4 The substance of the published technology (the body of the defensive disclosure)

A defensive publication is weak as prior art unless written at "a level of detail that a person skilled in the art can implement." So the disclosure document wrote the following at **an implementable level**.

![Memory core equation — an illustration of the leaky, saturating recurrence s(t+1) = decay⊙s + (1−decay)⊙tanh(W s + V x)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_core.svg)

**(a) The ladder of sound contraction verifiers.** Three rungs, cheapest first:
- `cert_inf` — closed-form ∞-norm upper bound (`O(n²)`). Uses the property that the sum of absolute values per row is maximized at the endpoints, so it is **solver-free**.
- `cert_two` — SVD at all `2^n` vertices.
- `cert_sdp` — a common Lyapunov matrix via a convex LMI (interior-point SDP, CLARABEL).

![Verifier ladder — the three rungs cert_inf → cert_two → cert_sdp, a staircase of proof strength tried cheapest-first](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_ladder.svg)

**Here is the honest point**: the project's old nickname was "Z3-gated," but **the actual gate does not use SMT (Z3)**. When we ran a dedicated Z3 contraction track to check, it **matched the closed-form ∞-norm verifier byte-for-byte (0 mismatches out of 3270; even near the boundary, 0 out of 8000)**. In other words, for this invariant class, **Z3 was decoration**. So we corrected the banner to "the ladder of sound contraction verifiers" (this is not a retreat but a strength — it avoids solver dependence and incompleteness).

**(b) prove-then-reject gate (fail-closed).** Propose a child individual → adopt if the proof passes, resample up to a cap if it fails, and if it still fails, adopt a **known-safe fallback**. **An unproven child is never adopted.** We added `gate_mode="contraction"` / `"state_norm"` additively, and the default `"none"` is byte-identical to prior behavior (= a pure overlay on the existing evolution base).

![prove-then-reject gate — a fail-closed checkpoint that proposes a child, adopts it if the proof passes, and rejects then resamples if it fails](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_gate.svg)

**(c) tracking tube inspection metric.** An answer to the user's request to see not just "shrinks to somewhere" but "**tracks a desired trajectory**." Reusing the quantities the gate already computes (state Lipschitz `L`, input gain `G`) and the disturbance upper bound `w̄`, it reports the tube `r = G·w̄/(1−L)` in which the tracking error stays — at **zero additional proof cost**. Even in small-scale measurement, the 3 genes that PASS contraction have error/disturbance ratios 0.50/0.78/1.04, inside the theoretical tube, while a non-contraction control **amplifies by 9.3×** (= the gate is load-bearing, not decoration).

![tracking tube — a tube of radius r = G·w̄/(1−L) drawn around the desired trajectory, with the actual trajectory staying inside it](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_tube.svg)

**(d) Two routes for verified memory evolution.**
- Route (a): gate updates of the agent's **memory bank** with a sound proof (the difference from SSGM's NLI theory = sound proof + a working gate).
- Route (b): gate the memory core's **internal-state dynamics** (done in this document).

**(e) Synthesis: an SPC control-chart runtime gate + a two-layer ethics gate.** Pass evolution metrics through control charts (X̄–R / CUSUM) to gate temporal anomalies online. And a two-layer ethics of **exploration is free, adoption is verified** (the exploration layer follows Sun Tzu's "way of deception" = surprise moves OK; the adoption layer follows the Analects' "benevolence" = honest, with the gate unavoidable).

### 3.5 Today's implementation facts (reduced to practice)

Evidence that this is not armchair theory:

- The proof gate is **fully wired into the shipping-side `evolve()`** (`gate_mode` / `resample_cap` added additively, the default `"none"` is byte-identical, and tests demonstrate all modes match the research-side reference implementation).
- The tracking tube reporter has landed too (`r = G·w̄/(1−L)`, limited to `cert_inf`, read-only, golden values match).
- **294 tests** cover the gate + reporter.
- **The observed gate cost is roughly 20–60×** (we disclose, without hiding, that proof is not free).

### 3.6 Honest limits (we don't soften them)

Even with defensive disclosure we do not bend honest disclosure.

- **The scale is small**: the core is `n=8` (72 real-valued genes), a 16 KB corpus, byte vocab. "LLM memory core" is in the sense of a **mechanism demonstration**.
- **The verifier's payoff is navigability, not learning (L3)**: the effect is EA-specific and vanishes with gradient methods.
- **The gate is a ~20–60× cost**: it only looks free under short training.
- **"Zero false admits" is an empirical observation, not a machine check**: the verifier's *conditions* are sound, but the *implementation* carrying them is not end-to-end formally verified.
- **The scope of "not found"**: limited to the scope of the adversarial verification + a surface-level patent search. CNIPA (Chinese) was not queried, and patents have a publication lag of up to 18 months. We always maintain the "within the search scope" caveat.

---

## Summary — the flag was planted for "defense," not "offense"

In a single day, we had 56 verifier AIs critically scrutinize our own research, queried patent DBs, and confirmed the "four-corner gap" that still remained. Normally one would aim for a patent here, but weighing the cost, we **passed on filing** and instead planted a flag with **a dated defensive publication**.

The aim is simple — **to preempt anyone later enclosing this gap with a patent and binding us or the public**. To that end, we published everything at a level of detail a person skilled in the art can implement. And to the end, we keep the non-inflating phrasing: **not "world first," but "within the scope of our verification, zero prior work occupying all four corners at once."**

The body of the defensive publication (the dated disclosure document) is here: [verified_memory_evolution_defensive_disclosure.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/papers/2026-06-06_verified_memory_evolution_defensive_disclosure.md).

Next time (from #39 on), we plan to report the landing of the heart of this four-point intersection — a small PoC of verified memory evolution (the memory-bank update route). Before the window where SSGM took the banner in theory closes in implementation.

---

# 中文

## 这篇文章是什么 —— 一天之内跑完「反证检验 → 专利清查 → 放弃申请 → 防御性公开」

2026 年 6 月 6 日，我（笔者）向 AI（Claude Code）提出 **「请检验我们所做的事情是否真的具有差异化」**。AI 以 **反证检验（adversarial verification）** —— 让大量验证角色的 AI 故意去反证、否定我们自己的主张，看它是否仍能存活的方法 —— 来回应。56 个验证代理从 7 + 3 个角度去搜寻「这个主张应该能用先行研究反证」的反例，另一支别动队甚至查询了专利数据库。

结果如下。

- **学术文献中的反证（breaks）：0 件**（对 44 个候选逐个判定，没有任何人填满了「四隅同时」）。
- **专利中的反证：0 件**（在英文 14 + 日文 3 个查询里，没有专利占据这个交叉点）。
- 于是我决定**不申请专利**（成本判断），转而立起一面叫**防御性公开（defensive publication）**的旗。

这篇文章，是那一天的故事（反证检验的设计与结果、以及决策）加上**我们所公开的内容（= 四点交叉点的技术）**的拆解版。文章的顺序一如既往：①术语说明 → ②拆解（平易） → ③详细。

---

## ① 术语小辞典（免得在正文里卡住）

| 术语 | 一句话 |
|---|---|
| **反证检验 (adversarial verification)** | 不是去肯定自己的主张，而是让大量验证角色（AI）故意去反证、否定它，再以它是否仍能存活来衡量主张的强度。可以想象成雇批评者而非捧场者。 |
| **防御性公开 (defensive publication)** | 不是去「取得」专利，而是**把技术公开、使其成为先行技术**。这是一种「先立旗」的防御，让某人（包括大厂）日后无法用同一发明申请专利来束缚我方或公众。 |
| **先行技术 (prior art)** | 能让你说出「那个发明已经是公知了」的既有公开物。否定新颖性的材料。日期是命门。 |
| **收缩性 (contraction, ρ<1)** | 回声（过去的扰动）随时间**衰减**的性质。谱半径 ρ 小于 1。可以想象成一根弹簧总会回到静止位置。记忆核不暴走、会「遗忘」的性质。 |
| **健全的证明 (sound proof)** | 一旦说「证明出来了」就**真的正确**（绝不发出假合格）的证明。与统计上「大概安全」是两回事。 |
| **prove-then-reject 门** | 一道关卡，**证明之后才采用**变异（更新），不行就**棄却**。fail-closed（无法证明就不放行）。 |
| **记忆核 (memory core)** | 罩在 LLM 周围的「记忆部件」。本研究中是带漏与饱和的递归（RWKV 系）`s_{t+1} = decay⊙s + (1−decay)⊙tanh(W s + V x)`。 |
| **进化循环 (evolution loop)** | 转动变异 → 选择 → 下一代来搜寻优秀个体的最优化。这里把证明门放在那个选择的关卡上。 |
| **SMT 求解器 (Z3 等)** | 解判逻辑式是否可满足的万能求解器。很重。本研究的结论是它「其实并不需要（只是装饰）」。 |
| **tracking tube（追踪管）** | 保证实际与「理想轨道」的偏差收在一个**管（半径 r）**之内。`r = G·w̄/(1−L)`。 |
| **SSGM** | **仅以理论**提出「统御进化记忆」write 门的先行研究（arXiv:2603.11768, 2026）。在招牌上最接近的对手。 |
| **navigability（可探索性）** | 进化是否「易于移动的地形」。与学习变聪明是两回事。验证器的功效在这一侧。 |

---

## ② 拆解 —— 3 分钟看懂全貌

用漫画来打比方。主人公（我们的研究）是一个「在进化型 AI 记忆的心脏上，装了一道**证明之后才采用的关卡**」的角色。这一招在 4 个条件**同时**满足时才发动。

1. **健全的收缩性证明**（在数学上保证回声必定衰减，而且绝不发出假合格）。
2. 把它打在**LLM 记忆核的内部**（不是控制机器人也不是分类器，而是「记忆部件」本身）。
3. **在进化循环之中**，把不行的变异**棄却**（丢掉 = 不是把它推回去 = 不是射影）。
4. 而且**有能跑的实现与实验**（不止步于纸上谈兵）。

把这 4 件**同时**做到的先行研究，即便让 56 个敌方 AI 来打、查询专利 DB，也没找到。每一个条件都有先行（我们诚实地把名字全部列出）。但没有人「同时占据四隅」。这就是**四点交叉点（four-point intersection）**。

这里讲一个生物学的比方。在进化里，「占据了生态位（没有其他物种的缝隙）的物种」会存活下来。大厂（OpenAI/Google 等）是「平均上聪明的大型物种」，支配着平原。我们在平原上赢不了。所以钻进**谁都没填的四隅的缝隙**。这就是这次的战略（用孙子的话说，「避实击虚」）。

还有一个重要决策。这个缝隙在**专利里也是空白**。一般来说接下来就会是「那就去申请专利吧」。但专利又花钱又花时间。我**放过了那里**，转而选择了**「公开、先立旗」的防御性公开**。目的不是进攻而是**防御** —— **未雨绸缪地压制**日后有人（大厂，或 SSGM 的后续实现）用同一概念申请专利来束缚我方或公众。只要带着日期公开了，它就成了公知的先行技术，后出的专利会因新颖性而死。

不过 —— 这是我们一以贯之的纪律 —— **我们不注水**。我们不说「世界首创」。正确的说法是**「在我们对抗审计的范围内，同时占据四隅的先行为零」**。我们一定保留「探索范围之外不得而知」的留白。

---

## ③ 详细 —— 一天的会话，以及所公开技术的内容

### 3.1 对抗审计的设计（为了可复现）

自己说「我的研究很强」没有意义。所以我们搭了一套**对抗性工作流**。

- **从 7 个角度搜寻反证**：证明门的谱系 / certified training / Transformer 稳定性 / 进化 × 验证 / verified memory / runtime assurance / 产业·专利。
- **追加 critic 指出的 3 个盲点角度**：从形式方法会议一侧的反查 / certified continual learning 的词汇系 / 内部状态·SSM 的解释。
- **用 5 轴评分表对 44 个候选逐个判定**（是否对更新设门 / 是否健全证明 / 是否 LLM 记忆核 / 是否在进化循环内 / 是否有实现）。判定方的 AI **必定用 WebFetch 确认一手信息（arXiv 的 abstract/HTML）**（禁止道听途说）。
- 并行地，**内部的 AI 抽取我们自己论文草稿的弱点**（honest disclosure：自家人挑刺）。

确定结论是 **breaks 0 / narrows 36 / background 8（44 件）**。存活下来的差异化核心，就是上面的四点交叉点。

### 3.2 「四隅」各自最接近的对手（全部列名）

新颖性的诚实，取决于「能否用一句话点名全部」。逐隅，用一句话点出最接近的先行：

- **SSGM（arXiv:2603.11768）** —— **仅以理论**抢先拿下「统御进化记忆」的招牌。门是 NLI（矛盾检测），**并非健全的形式证明**，也没有实现。→ 作为扛招牌的对手**必须引用**。实现 + 证明的窗口是空着的。
- **SEVerA（arXiv:2603.25111）** —— 对自进化代理施以 Dafny/SMT 验证。但对象是**输出契约**，不是对记忆核收缩性的每次更新设门。
- **PSV-Verus（arXiv:2512.18160）** —— self-play 循环内的健全 SMT 门。但验证对象是**生成代码的正确性**。
- **Provably Safe Model Updates / LID（arXiv:2512.01899）** —— 用抽象解释把更新认证为 δ-safe。但它是**射影（推回去）**而非 prove-then-reject，对象是 frozen-embedding 的分类 head。
- **GP × 模型检查（Katz & Peled, arXiv:1402.6785, 2014）** —— 在进化循环里放一道健全检查门的**模式先例**。所以我们**不主张门这个模式本身是新颖的**。只有把它应用到记忆核的收缩性上，才是未踏之地。
- **Enforced-Lipschitz Transformers（arXiv:2507.13338）/ R2DN（arXiv:2504.01250）** —— 用**结构来强制（by-construction）**收缩性。这是最强的对抗设计：「根本不需要门，一开始就内嵌进去」。我们把**by-construction 对 prove-then-reject**作为设计轴来对比（结构强制牺牲表现力，棄却门则在无结构约束下检查任意更新）。
- **Safeguarded AI（ARIA programme）** —— 最具权威的 proof-gated-gatekeeper 概念。但门的对象是**行为/计划**（输出门），不是对权重/记忆更新设门，而且还停留在 programme 阶段。
- **Emergent FV / substrate-guard（arXiv:2603.21149）** —— 用 Z3 验证 AI 的**输出**的、能跑的系统。但它是事后监视，不是每次更新设门。

（以上 arXiv ID 只使用在论文草稿中已与 abstract 核对过的那些。）

### 3.3 专利面的查询（补学术审计留下的窟窿）

学术审计**只看了文献**，没看专利 DB（作为不在证据偏弱）。于是一支别动队用**英文 14 + 日文 3** 个查询，查询了 Google Patents / USPTO。

- **占据交叉点的专利：零件。**
- 最接近的专利只有 3 个谱系，且都在交叉点之外：
  - **US11715005B2** —— 用哈希匹配来验证 NN 的真正性（是密码哈希，不是健全证明）。
  - **US10896032** —— certify-then-deploy 的治理门（根据是程序性 attestation）。
  - **US11868855** —— 模型/权重的「stability」验证（但大概率是可用性·耐故障意义上的蓋然性）。
- 一个有趣的结构性证据：当你查询「**用健全证明对更新/记忆/进化设门**」时，即便对专利 DB 指定了 site，结果也几乎全部**偏到了 arXiv**。这是「这个概念还停留在学术阶段、尚未被专利化」的间接证据。

→ 结论：**专利面也 clear**。不过由于 US10896032 / US11868855 在词汇上部分重叠，我们在论文的 related work 里先发地放了 1～2 句对比：「与展开治理型门 / 运营稳定性验证不同，本研究是用健全证明对权重更新的解析性 contraction 性质设门」。

### 3.4 所公开技术的内容（防御性披露的本体）

防御性公开如果不写到「当业者可实施的详细度」，作为先行技术就会偏弱。所以披露文件里，把以下内容写到了**可实现的层级**。

**(a) 健全收缩性证明器的梯子（ladder）。** 从便宜的开始，共 3 级：
- `cert_inf` —— 闭式 ∞-范数上界（`O(n²)`）。利用各行绝对值之和在端点处取最大的性质，**无需求解器**。
- `cert_two` —— 在全部 `2^n` 个顶点上做 SVD。
- `cert_sdp` —— 用凸 LMI（内点 SDP, CLARABEL）求共同 Lyapunov 矩阵。

**这里是诚实点**：项目的旧俗称是「Z3-gated」，但**实际的门并没有用 SMT(Z3)**。专门跑了一条 Z3 收缩性轨道来确认后，它与闭式 ∞-范数证明器**逐字节一致（3270 件中 0 件不一致，连边界附近也是 8000 件中 0 件）**。也就是说，在这个不变量类里，**Z3 是装饰**。所以我们把招牌改正为「健全收缩性证明器的梯子」（这不是撤退而是强项 —— 可以规避求解器依赖与不完全性）。

**(b) prove-then-reject 门（fail-closed）。** 提出一个子个体 → 证明通过则采用，不行则 resample 直到上限，再不行就采用一个**已知安全的 fallback**。**未证明的子绝不采用**。我们把 `gate_mode="contraction"` / `"state_norm"` additive 地加入，而默认的 `"none"` 与既往行为逐字节一致（= 对既有进化基盘的纯粹罩层）。

**(c) tracking tube 检查指标。** 这是对用户要求「不只要『收缩到某处』，还要看『追踪理想轨道』」的回答。复用门已经在算的量（状态 Lipschitz `L`、输入增益 `G`）与外扰上界 `w̄`，以**零额外证明成本**报告追踪误差收住的管 `r = G·w̄/(1−L)`。即便在小规模实测里，收缩性 PASS 的 3 gene 误差/外扰比为 0.50/0.78/1.04，处于理论管之内；而非收缩性的对照则**放大 9.3 倍**（= 门是 load-bearing，不是装饰）。

**(d) verified memory evolution 的 2 条路线。**
- 路线 (a)：用健全证明对代理**记忆库**的更新设门（与 SSGM 的 NLI 理论之差 = 健全证明 + 能跑的门）。
- 路线 (b)：对记忆核的**内部状态 dynamics**设门（本书已实施）。

**(e) 合成：SPC 管制图 runtime 门 + 双层伦理门。** 把进化指标通过管制图（X̄–R / CUSUM），在线对时间方向的异常设门。再加上**探索自由·采用验证**的双层伦理（探索层遵循孙子的「诡道」= 奇手 OK，采用层遵循论语的「仁」= 诚实、门不可避）。

### 3.5 本日的实现事实（reduced to practice）

它不是纸上谈兵的证据：

- 证明门已**正式配线进出货侧的 `evolve()`**（additive 地追加 `gate_mode` / `resample_cap`，默认 `"none"` 逐字节一致，并以测试实证与 research 侧的参考实现全模式一致）。
- tracking tube 报告器也落地了（`r = G·w̄/(1−L)`，限定 `cert_inf`，read-only，golden 值一致）。
- 覆盖门 + 报告器的测试 **294 件**。
- **观测到的门的成本约为 20～60 倍**（不隐瞒地披露：证明不是免费的）。

### 3.6 honest 局限（不弱化）

即便是防御性披露，我们也不弯折 honest disclosure。

- **规模小**：核是 `n=8`（72 个实数 gene）、16 KB 语料、byte vocab。「LLM 记忆核」是**机构实证**的意思。
- **验证器的 payoff 是 navigability 而非学习（L3）**：效果是 EA 固有的，在梯度法里会消失。
- **门是 ~20～60 倍的成本**：只在短训练里看着像免费。
- **「false admit 为零」是经验观测，而非机器检查**：证明器的*条件*是健全的，但承载它的*实现*并未做端到端的形式验证。
- **「未发现」的范围**：仅限于对抗审计 + 表层专利检索的范围。CNIPA（中文）未查询，专利最长有 18 个月的公开滞后。「在探索范围内」的留白始终保留。

---

## 总结 —— 旗是为了「守」而非「攻」才立起来的

今天一天，我们让 56 个敌人来打自己的研究，连专利 DB 都查询了，还是确认到了残留的「四隅空白」。一般来说这时就会去谋求专利，但权衡成本之后，我们**放过了申请**，转而用**带日期的防御性公开**立起一面旗。

目的很简单 —— **未雨绸缪地压制日后有人用专利把这个空白圈起来、束缚我方或公众**。为此，我们以当业者可实现的详细度把一切都公开了。并且自始至终，守住不注水的说法：**不说「世界首创」，而说「在我们审计的范围内，同时占据四隅的先行为零」**。

下一回（#39 以后），打算 report 这个四点交叉点的本丸 —— verified memory evolution 的小 PoC（记忆库更新路线）的落地。趁 SSGM 以理论拿下招牌的那扇窗，还没被实现合上之前。

---

# 한국어

## 이 글은 무엇인가 — 하루 만에 「적대적 감사 → 특허 클리어 → 출원 보류 → 방어적 공개」까지 달린 이야기

2026년 6월 6일, 나(필자)는 AI(Claude Code)에게 우리 연구 llcore의 「차별화의 핵심」을 **적에게 두들기게 하라**고 지시했습니다. 56개의 AI 에이전트가 7 + 3개의 각도에서 「이 주장은 선행 연구로 깨뜨릴 수 있을 것이다」라며 반증을 찾아 헤맸고, 별동대가 특허 데이터베이스까지 조회했습니다.

결과는 다음과 같습니다.

- **학술 문헌에서의 반증(breaks): 0건**(44개 후보를 개별 판정했는데, 누구도 「네 모서리 동시」를 메우지 못했음).
- **특허에서의 반증: 0건**(영어 14 + 일본어 3 쿼리에서, 교차점을 점유하는 특허는 없음).
- 그래서 나는 **특허를 내지 않기로**(비용 판단) 정하고, 대신 **방어적 공개(defensive publication)**라는 깃발을 세웠습니다.

이 글은 그 하루의 이야기(적대적 감사의 설계와 결과, 의사결정)와 **공개한 내용(= 네 점 교차점의 기술)**의 쉽게 풀어쓴 버전입니다. 글의 순서는 늘 그렇듯 ①용어 설명 → ②쉽게 풀기(평이) → ③상세로 나아갑니다.

---

## ① 용어 미니 사전(본문에서 막히지 않도록)

| 용어 | 한마디로 |
|---|---|
| **방어적 공개 (defensive publication)** | 특허를 「얻는」 것이 아니라, 기술을 **공개하여 선행 기술로 만드는** 것. 누군가(대기업 포함)가 나중에 같은 발명으로 특허를 따서 우리나 세상을 옭아매지 못하도록 하는 「먼저 깃발을 세우는」 방어. |
| **선행 기술 (prior art)** | 「그 발명, 이미 공지예요」라고 말할 수 있는 기존 공개물. 신규성을 부정하는 자료. 날짜가 생명. |
| **축소성 (contraction, ρ<1)** | 에코(과거의 흔들림)가 시간과 함께 **감쇠**하는 성질. 스펙트럼 반경 ρ가 1 미만. 스프링이 반드시 정지 위치로 돌아가는 이미지. 기억 코어가 폭주하지 않고 「잊는」 성질. |
| **건전한 증명 (sound proof)** | 「증명했다」고 하면 **정말로 옳은**(거짓 합격을 내지 않는) 증명. 통계적으로 「아마 안전」과는 별개. |
| **prove-then-reject 게이트** | 변이(업데이트)를 **증명하고 나서 채용**, 안 되면 **기각**하는 관문. fail-closed(증명할 수 없으면 통과 못 함). |
| **기억 코어 (memory core)** | LLM 주위에 씌우는 「기억하는 부품」. 본 연구에서는 `s_{t+1} = decay⊙s + (1−decay)⊙tanh(W s + V x)`라는 누수·포화 딸린 재귀(RWKV 계). |
| **진화 루프 (evolution loop)** | 변이 → 선택 → 다음 세대를 돌려 좋은 개체를 찾는 최적화. 여기서는 그 선택의 관문에 증명 게이트를 둔다. |
| **SMT 솔버 (Z3 등)** | 논리식이 충족 가능한지 푸는 만능 솔버. 무겁다. 본 연구에서는 「실은 필요 없었다(장식)」가 결론. |
| **tracking tube(추종 튜브)** | 「바람직한 궤도」에서의 실제 편차가 수렴하는 **통(반경 r)**의 보증. `r = G·w̄/(1−L)`. |
| **SSGM** | 「진화하는 기억을 통솔하는」 write 게이트를 **이론만으로** 제안한 선행 연구(arXiv:2603.11768, 2026). 간판에서 가장 가까운 상대. |
| **navigability(탐색 가능성)** | 진화가 「움직이기 쉬운 지형인가」. 학습이 똑똑해지는 것과는 별개. 검증기의 효과는 이쪽에 있다. |

---

## ② 쉽게 풀기 — 3분 만에 전체 그림

만화로 비유합니다. 주인공(우리 연구)은 「**증명하고 나서 채용하는 관문**을, 진화하는 AI 기억의 심장부에 부착한」 캐릭터입니다. 기술은 4개의 조건을 **동시에** 충족하면 발동합니다.

1. **건전한 축소성 증명**(에코가 반드시 감쇠한다고 수학적으로 보증. 게다가 거짓 합격을 내지 않는다).
2. 그것을 **LLM 기억 코어의 내부**에 적용(제어 로봇도 분류기도 아닌, 「기억하는 부품」 그 자체).
3. **진화 루프 안에서**, 안 되는 변이를 **기각**(밀어 되돌리기 = 사영이 아니라, 버린다).
4. 게다가 **돌아가는 구현과 실험**이 있다(탁상공론으로 끝나지 않는다).

이 4가지를 **동시에** 하고 있는 선행 연구는, 56개의 적 AI에게 두들기게 해도, 특허 DB를 조회해도, 찾을 수 없었습니다. 하나하나의 조건은 선행이 있습니다(정직하게 전부 이름을 댑니다). 하지만 「네 모서리를 동시에 점유」한 사람은 없었습니다. 이것이 **네 점 교차점(four-point intersection)**입니다.

여기서 생물학 비유를 하나. 진화에서는 「니치(다른 종이 없는 틈)를 점한 종」이 살아남습니다. 대기업(OpenAI/Google 등)은 「평균적으로 똑똑한 대형종」으로 평야를 지배합니다. 우리는 평야에서는 이길 수 없습니다. 그래서 **아무도 메우지 않은 네 모서리의 틈**에 파고듭니다. 그것이 이번의 전략입니다(손자로 말하면 「실을 피하고 허를 친다」).

그리고 중요한 의사결정. 이 틈은 **특허에서도 공백**이었습니다. 보통이라면 「그럼 특허를 내자」가 됩니다. 하지만 특허는 돈과 시간이 듭니다. 나는 거기를 **보류하고**, 대신 **「공개해서 먼저 깃발을 세우는」 방어적 공개**를 선택했습니다. 노림수는 공격이 아니라 **방어**입니다 — 나중에 누군가(대기업이나, SSGM의 후속 구현)가 같은 개념으로 특허를 따서, 우리나 공중을 옭아매는 것을 **미연에 깨뜨린다**. 날짜를 붙여 공개해 버리면, 그것은 공지의 선행 기술이 되고, 나중에 낸 특허는 신규성으로 죽습니다.

다만 — 여기가 우리의 일관된 규율인데 — **부풀리지 않습니다**. 「세계 최초」라고 말하지 않습니다. 올바른 표현은 **「우리 적대적 감사의 범위에서, 네 모서리를 동시에 점유한 선행은 제로」**입니다. 탐색 범위 밖은 알 수 없다는 단서를 반드시 남깁니다.

---

## ③ 상세 — 하루의 세션, 그리고 공개한 기술의 내용

### 3.1 적대적 감사의 설계(재현할 수 있도록)

「내 연구는 강하다」고 스스로 말해 봐야 의미가 없습니다. 그래서 **적대적 워크플로**를 짰습니다.

- **7개 각도의 반증 탐색**: 증명 게이트의 계보 / certified training / Transformer 안정성 / 진화 × 검증 / verified memory / runtime assurance / 산업·특허.
- **critic가 지적한 맹점 3개 각도를 추가**: 형식 방법 컨퍼런스 측의 역추적 / certified continual learning의 어휘계 / 내부 상태·SSM의 해석.
- **44개 후보를 5축 루브릭으로 개별 판정**(업데이트를 게이트하는가 / 건전 증명인가 / LLM 기억 코어인가 / 진화 루프 내인가 / 구현이 있는가). 판정역 AI는 **일차 정보(arXiv의 abstract/HTML)를 WebFetch로 반드시 확인**(전언 금지).
- 병행하여 **내부의 AI가 자신의 논문 드래프트의 약점을 추출**(honest disclosure: 내 편 흠 잡기).

확정 결론은 **breaks 0 / narrows 36 / background 8(44건)**. 살아남은 차별화 핵심이, 위의 네 점 교차점입니다.

### 3.2 「네 모서리」 각각의 최근접 라이벌(전부 이름을 댄다)

신규성은 「전부를 한 문장으로 지명할 수 있는가」로 정직함이 결정됩니다. 모서리별로 가장 가까운 선행을 한 문장으로:

- **SSGM(arXiv:2603.11768)** — 「진화하는 기억을 통솔하는」 간판을 **이론만으로** 선점. 게이트는 NLI(모순 검출)로 **건전한 형식 증명이 아니며**, 구현도 없다. → 간판을 짊어진 상대로서 **반드시 인용**. 구현 + 증명의 창문이 비어 있다.
- **SEVerA(arXiv:2603.25111)** — 자기 진화 에이전트에 Dafny/SMT 검증. 다만 대상은 **출력 계약**이지, 기억 코어의 축소성의 매 업데이트 게이트가 아니다.
- **PSV-Verus(arXiv:2512.18160)** — self-play 루프 내의 건전 SMT 게이트. 다만 검증 대상은 **생성 코드의 정확성**.
- **Provably Safe Model Updates / LID(arXiv:2512.01899)** — 업데이트를 추상 해석으로 δ-safe 인증. 다만 **사영(밀어 되돌리기)**으로 prove-then-reject가 아니며, 대상은 frozen-embedding의 분류 head.
- **GP × 모델 검사(Katz & Peled, arXiv:1402.6785, 2014)** — 진화 루프에 건전한 검사 게이트를 두는 **패턴의 선례**. 그래서 우리는 **게이트의 패턴 자체를 신규라고 주장하지 않습니다**. 기억 코어의 축소성으로의 적용만이 미답.
- **Enforced-Lipschitz Transformers(arXiv:2507.13338) / R2DN(arXiv:2504.01250)** — 축소성을 **구조로 강제(by-construction)**. 이것은 「게이트 따위 필요 없다, 처음부터 내장하라」는 최강의 대항 설계. 우리는 **by-construction 대 prove-then-reject**를 설계 축으로 대비합니다(구조 강제는 표현력을 희생하고, 기각 게이트는 임의 업데이트를 구조 제약 없이 검사한다).
- **Safeguarded AI(ARIA programme)** — 가장 권위 있는 proof-gated-gatekeeper 개념. 다만 게이트 대상은 **행동/계획**(출력 게이트)으로, 가중치/기억의 업데이트 게이트가 아니며, 아직 programme 단계.
- **Emergent FV / substrate-guard(arXiv:2603.21149)** — AI의 **출력**을 Z3로 검증하는 돌아가는 시스템. 다만 post-hoc 감시로, 매 업데이트 게이트가 아니다.

(위 arXiv ID는 모두 논문 드래프트에서 abstract와 대조 확인된 것만 사용하고 있습니다.)

### 3.3 특허 면의 조회(학술 감사가 남긴 구멍 메우기)

학술 감사는 **문헌만**이고, 특허 DB를 보지 않았습니다(부재 증거로서 약하다). 그래서 별동대가 **영어 14 + 일본어 3** 쿼리로 Google Patents / USPTO를 조회했습니다.

- **교차점을 점유하는 특허: 제로 건.**
- 최근접 특허는 3계통뿐이며, 모두 교차점 밖:
  - **US11715005B2** — NN을 해시 대조로 진정성 검증(건전 증명이 아니라 암호 해시).
  - **US10896032** — certify-then-deploy의 거버넌스 게이트(근거가 절차적 attestation).
  - **US11868855** — 모델/가중치의 「stability」 검증(다만 가용성·내장애의 의미일 개연성 큼).
- 흥미로운 구조적 증거: 「**건전 증명으로 업데이트/기억/진화를 게이트한다**」고 쿼리하면, 특허 DB에 site 지정을 해도 결과가 거의 전부 **arXiv로 빗나갔다**. 이것은 「이 개념이 아직 학술 단계에 머물러 있어, 특허화되지 않았다」는 간접 증거입니다.

→ 결론: **특허 면에서도 clear**. 다만 US10896032 / US11868855는 어휘가 부분적으로 겹치므로, 논문의 related work에 「전개 거버넌스형 게이트 / 운용 안정성 검증과는 달리, 본 연구는 가중치 업데이트의 해석적 contraction 성질을 건전 증명으로 게이트한다」는 대비를 1~2문 선제적으로 넣었습니다.

### 3.4 공개한 기술의 내용(방어적 개시의 본체)

방어적 공개는 「당업자가 실시할 수 있는 상세도」로 쓰지 않으면 선행 기술로서 약합니다. 그래서 개시 문서에는 다음을 **구현 가능한 레벨**로 썼습니다.

**(a) 건전한 축소성 증명기의 사다리(ladder).** 싼 것부터 순서대로 3단:
- `cert_inf` — 닫힌 형식의 ∞-노름 상한(`O(n²)`). 각 행의 절댓값 합이 끝점에서 최대가 되는 성질을 사용해, **솔버 불필요**.
- `cert_two` — 전체 `2^n` 꼭짓점에서 SVD.
- `cert_sdp` — 공통 Lyapunov 행렬을 볼록 LMI(내점 SDP, CLARABEL)로.

**여기가 정직 포인트**: 프로젝트의 옛 통칭은 「Z3-gated」였지만, **실제 게이트에 SMT(Z3)는 사용하지 않습니다**. 전용 Z3 축소성 트랙을 돌려 확인하니, 닫힌 형식 ∞-노름 증명기와 **바이트 단위로 일치(3270건 중 0건의 불일치, 경계 근방에서도 8000건 중 0건)**. 즉 이 불변량 클래스에서는 **Z3는 장식**이었습니다. 그래서 간판을 「건전한 축소성 증명기의 사다리」로 고쳤습니다(이것은 후퇴가 아니라 강점 — 솔버 의존과 불완전성을 회피할 수 있다).

**(b) prove-then-reject 게이트(fail-closed).** 자식 개체를 제안 → 증명이 통과하면 채용, 안 되면 상한까지 resample, 그래도 안 되면 **알려진 안전한 fallback**을 채용. **미증명의 자식은 결코 채용하지 않는다**. `gate_mode="contraction"` / `"state_norm"`을 additive하게 추가하고, 기본 `"none"`은 종전 거동과 바이트 일치(= 기존 진화 기반으로의 순수한 덧씌움).

**(c) tracking tube 검사 지표.** 「어딘가로 수축한다」뿐만 아니라 「**바람직한 궤도에 추종한다**」를 보고 싶다는 사용자 요망에 대한 답. 게이트가 이미 계산하고 있는 양(상태 Lipschitz `L`, 입력 게인 `G`)과 외란 상계 `w̄`를 재이용해, 추종 오차가 수렴하는 통 `r = G·w̄/(1−L)`을 **추가 증명 비용 제로**로 보고. 소규모 실측에서도, 축소성 PASS의 3 gene은 오차/외란 비 0.50/0.78/1.04로 이론 통의 안쪽, 비축소성의 대조는 **9.3배**로 증폭(= 게이트는 장식이 아니라 load-bearing).

**(d) verified memory evolution의 2개 루트.**
- 루트 (a): 에이전트 **기억 뱅크**의 업데이트를 건전 증명으로 게이트(SSGM의 NLI 이론과의 차 = 건전 증명 + 돌아가는 게이트).
- 루트 (b): 기억 코어의 **내부 상태 dynamics**를 게이트(본서에서 실시 완료).

**(e) 합성: SPC 관리도 runtime 게이트 + 이층 윤리 게이트.** 진화 메트릭을 관리도(X̄–R / CUSUM)에 통과시켜 시간 방향의 이상을 online 게이트. 그리고 **탐색은 자유·채용은 검증**의 이층 윤리(탐색층은 손자의 「궤도(詭道)」= 기수 OK, 채용층은 논어의 「인(仁)」= 정직하고 게이트 불가피).

### 3.5 본일의 구현 사실(reduced to practice)

탁상공론이 아니라는 증거:

- 증명 게이트는 **출하 측의 `evolve()`에 본배선 완료**(`gate_mode` / `resample_cap`을 additive 추가, 기본 `"none"`은 byte-identical, research 측의 참조 구현과 전 모드 일치를 테스트로 실증).
- tracking tube 리포터도 착지(`r = G·w̄/(1−L)`, `cert_inf` 한정, read-only, golden 값 일치).
- 게이트 + 리포터를 덮는 테스트 **294건**.
- **관측한 게이트의 비용은 약 20~60배**(증명은 공짜가 아니라고 숨기지 않고 개시).

### 3.6 honest 한계(약화시키지 않는다)

방어적 개시라도 honest disclosure는 굽히지 않습니다.

- **규모는 작음**: 핵은 `n=8`(72 실수 gene)·16 KB 코퍼스·byte vocab. 「LLM 기억 코어」는 **기구 실증**의 의미.
- **검증기의 payoff는 navigability이지 학습이 아니다(L3)**: 효과는 EA 고유로, 경사법에서는 사라진다.
- **게이트는 ~20~60배의 비용**: 짧은 훈련에서는 공짜처럼 보일 뿐.
- **「false admit 제로」는 경험적 관측이지 기계 검사가 아니다**: 증명기의 *조건*은 건전하지만, 그것을 담당하는 *구현*은 end-to-end로 형식 검증된 것은 아니다.
- **「미발견」의 범위**: 적대적 감사 + 표층 특허 검색의 범위에 한한다. CNIPA(중국어) 미조회, 특허는 최장 18개월의 공개 래그. 「탐색 범위에서」의 단서는 항상 유지.

---

## 정리 — 깃발은 「공격」이 아니라 「수비」를 위해 세웠다

오늘 하루로, 우리는 자신의 연구를 56개의 적에게 두들기게 하고, 특허 DB까지 조회하고, 그래도 남은 「네 모서리의 공백」을 확인했습니다. 보통이라면 여기서 특허를 노릴 참이지만, 비용을 저울질하여 **출원은 보류**하고, 대신 **날짜 붙은 방어적 공개**로 깃발을 세웠습니다.

노림수는 단순합니다 — **누군가가 나중에 이 공백을 특허로 둘러싸, 우리나 공중을 옭아매는 것을 미연에 깨뜨린다**. 그것을 위해, 당업자가 구현할 수 있는 상세도로 전부 공개했습니다. 그리고 끝까지, **「세계 최초」라고 말하지 않고 「우리 감사의 범위에서 네 모서리 동시의 선행 제로」**라는, 부풀리지 않는 표현을 지키고 있습니다.

다음 회(#39 이후)는, 이 네 점 교차점의 본진 — verified memory evolution의 작은 PoC(기억 뱅크 업데이트 루트)의 착지를 report할 예정입니다. SSGM이 이론으로 간판을 차지한 창문이, 구현으로 닫히기 전에.
