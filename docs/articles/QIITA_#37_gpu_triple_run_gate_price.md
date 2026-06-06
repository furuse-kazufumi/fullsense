---
title: 'llcore 検証 arc (#37) — AI が無料 GPU で実験 3 連戦を自走した日: 安全ゲートの代価は「表現力」、後付け証明は 19 倍高い'
tags: [FullSense, llcore, Singularity, AI, 解説]
private: false
updated_at: '2026-06-06'
id: a0e16b74a23c62bcf59a
qiita_public_id: 6f44575d440a9ebf5228
organization_url_name: null
slide: false
ignorePublish: false
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

# 日本語

## この記事は何か — 人間の指示は 4 文だけだった

この記事は、2026 年 6 月 6 日の 1 日で起きた研究セッションの記録です。人間(筆者)がこの日 AI に出した実験指示は、実質この 4 文だけでした。

> 「HD-1 を push して」
> 「full + null も push して」
> 「stage-B を進めて」
> 「push して」

それ以外の全て — 実験設計、事前登録(pre-registration)の作成、自分が書いたコードへの敵対レビュー(3 並列の攻撃役 AI による査読)、検出された 5 件の重大欠陥の修正、無料 GPU(Kaggle T4)へのジョブ投入、完走監視、結果回収、統計判定、論文ドラフトへの編入、その数値の再検証 — を AI(Claude Code)が自走しました。総コストは **$0**(Kaggle の無料 GPU 枠のみ)。

そして自走の話以上に重要なのが、**出てきた科学的結果そのもの**です。本記事は両方を report します。

## 今日のあらすじ — 3 実験で出た確定結論

| 実験 | 問い | 答え |
|---|---|---|
| HD-1 full | 制約なしの学習は高次元で安定領域に留まるか | **留まらない**(19/20 seeds が越境、次元とともに単調悪化) |
| HD-1 null | その越境は「賢くなるため」か | **違う — ただの幾何的成り行き**(無意味データでより強く越境、利得ゼロ) |
| Stage-B | 証明付き記憶は本物の Transformer で働くか / 安全ゲートの代価の正体は | **働く(4/4)** / **表現力制約**(運用摩擦ではない)、しかも**構造依存** |
| Stage-B B-G4 | 「自由に訓練して、後から証明を付ける」は可能か | **実質不可能 — 訓練時ゲートの 17〜19 倍のコスト** |

## 背景 — 「検証つき進化」arc の現在地

llcore は「数学的に安定性(縮小性 ρ<1 = エコーが減衰する性質 = 恒常性)を**証明**できる記憶コア」を、進化や勾配学習と組み合わせる研究シリーズです。証明器(verifier)は fail-closed: 証明できない変化は通しません。

前回 **#36「2ⁿ の壁を破る」** では、その証明器のコスト側 — 頂点を列挙せず健全に近似する vertex-free 証明 — を詰めました。「検査器をどう安く正しく回すか」の話です。本記事はその裏返し、**「検査器を回すと、肝心の能力はいくら削られるのか」** を、初めて本物の Transformer の上で測ります。

ここまでの arc で、(i) このコアは実際に小さな言語モデルとして機能する、(ii) 証明器は実仕事をしている(ゲートなし集団は 78.9% が不安定)、(iii) ただし進化(ランダム変異)にとって厳しいゲートは「罠」になる — が確立済みでした。残った大きな問いが 2 つ: **高次元で何が起きるか**、そして**本物の Transformer に入れたら何が起きるか**。今日この 2 つが閉じました。

## 実験 1: HD-1 — 高次元・無制限の学習はどこへ行くか

**設計**: 記憶コア(n 次元、n ∈ {8, 32, 64, 128, 256})を文字レベル言語モデルに配線し、(a) gradient 学習、(b) 進化(変異+選択)それぞれを「ゲートなし(none)」と「安価な健全ゲート(inf、O(n²))」で訓練。これを本物のコーパス(シェイクスピア)とシャッフル版(null = 学ぶ構造が何もない対照)の両方で実施。

**結果**(full run、計 80 runs):

| n | GRAD ρ(none, real) | GRAD 越境 | EVO 越境 | gate の CE コスト | GRAD ρ(none, null) |
|---:|---:|:--:|:--:|---:|---:|
| 8 | 1.07 | 3/4 | 0/4 | 0.03 | 1.06 |
| 32 | 1.20 | 4/4 | 0/4 | 0.09 | 1.58 |
| 64 | 1.22 | 4/4 | 2/4 | 0.12 | 1.89 |
| 128 | 1.42 | 4/4 | 3/4 | 0.10 | 2.21 |
| 256 | 1.95 | 4/4 | 4/4 | 0.03 | 2.61 |

**発見 1 — ゲートなしの gradient 学習は、全次元で安定領域(ρ<1)を離脱する**(19/20 seeds)。短い訓練ではこれは見えません(feasibility 走行では全 seed 安定のままだった)。「短い実験で安全に見えても、訓練を伸ばすと越境する」 — 結論が訓練予算に依存するという、それ自体が重要な教訓です。

**発見 2 — 越境は「賢くなるため」ではなく、ただの成り行き(エントロピー的 drift)**。決定打は null 対照: 学ぶ構造が何もないシャッフル・データでも同じ越境が**より強く**起きて(ρ→2.61)、性能利得はゼロ(全セルが理論下限に張り付き)。つまり「不安定さが知能に必要」なのではなく、**高次元では安定領域が相対的に細い道になり、縛らなければ出てしまう**だけ。むしろ本物のデータがある方が drift は浅い(n≥32 で一貫、n=8 は誤差内で同等)。reservoir computing の「edge of chaos(カオスの淵)で性能最大」仮説のこの系での素朴な適用は、null によって棄却されました。

**発見 3 — ゲートのコストは実在する**(0.03〜0.12 nat、中間次元でピーク)。短い訓練では「ほぼタダ」に見えたものが、十分訓練すると顕在化します。

**発見 4 — 進化は軽い不安定で得をするが、強い不安定には溺れる**(none−inf: −0.013 → −0.035 → −0.040 → −0.019 → **+0.042** で n=256 にて逆転)。gradient は同じ場所で利益を搾り続けられる。「目隠しでランダムに足を出す」のと「坂を見て下る」の差です。

## 実験 2: Stage-B — 本物の Transformer に証明付き記憶を入れる

**設計の核**: 2 層の softmax-attention Transformer(本物)に、attention の**視界を 8 トークンの窓に制限**(積み上げ受容野 ≈ 15)した上で、文脈長 T=160 を与える。すると 15 文字より遠くの情報は、**証明付き記憶コアを通る以外に道がない**。記憶が働いているかをごまかせない設計です。

**4 条件**(コアの訓練方式だけが違う、他は全て同一・乱数も対応付け):

- `pure` — 記憶コアなし(ベースライン)
- `none` — コア自由(無制約)
- `project` — 証明が破れたら**滑らかに中へ押し戻す**(巻き戻しなし)
- `reject` — 証明が破れたら**直前の合格状態へ巻き戻す**

`project` と `reject` の比較が肝です。両者は「制約の中身」は同じで「運用方法」だけが違う。もしコストが運用摩擦なら project が安く、制約そのものなら両者同額になるはず。

**投入前の敵対レビュー(3 並列)が major 5 件を検出** — 白眉は「float32 の sigmoid が飽和して decay がちょうど 1.0 になると、**証明可能領域が空集合になり**、押し戻し先が存在しなくなる」という soundness 欠陥。検証 AI が実際に float32 で再現して証明しました。全件修正してから投入しています。

**判定**(full + null、計 72 runs、事前登録ゲート B-G1〜B-G4):

| ゲート | 判定 | 数値(n=64 / n=256) |
|---|---|---|
| B-G1 記憶は load-bearing か | **PASS、4/4 seeds** | コアあり−なし = −0.034 / −0.072(次元とともに拡大)。null では消える ⇒ パラメータ数でなく構造学習 |
| B-G2 コストの正体 | **表現力制約**(両 n) | project ≈ reject(摩擦はほぼゼロ)。n=64 は境界値 0.76(正直に開示)、n=256 は明確 |
| B-G2-null | **null ではコスト消滅** | Δ ≈ −0.003 / −0.004 ≈ 0 |
| B-G3 attention があれば安定か | **越境する(4/4)**、ただし単独時より浅い | ρ 1.11 / 1.28(HD-1 同次元は 1.22 / 1.95) |
| B-G4 後付け証明の値段 | **17〜19 倍** | 後付け +0.378 / +1.117 vs 訓練時 +0.022 / +0.060 |

**特に重要な 2 点:**

1. **ゲートのコストは「本物を学んでいる場所」でだけ発生する**(B-G2-null)。以前の進化実験ではゲート間の差は無意味データでも残った(=最適化のクセ)。gradient + 本物の Transformer では、コストは構造学習の場でのみ発生 — arc 全体で初めての「構造依存のゲート効果」です。安全の税金は、能力の現場で徴収される。だからこそ税率設計に意味がある。
2. **「自由に訓練して後から証明を付ける」は壊滅的**(B-G4)。無制約で訓練したコアは、証明可能領域に戻すために結合行列を**元の 2〜6% まで縮める**必要があり、学習内容がほぼ破壊されます。**検証は訓練ループの中に入れるしかない** — これは「安全は後付けできるか」という AI safety の中心論点への、ミニチュアながら定量的な回答です。

## 舞台裏 — AI が無料 GPU を自走させる工程(再現したい人向け)

Kaggle の無料 T4 を CLI から使う際の罠 4 つ(全部踏みました):

1. **認証**: 新 CLI (2.2.1) は classic な `kaggle.json` を write 系 API で拒否。保存していたキーは実は新方式トークンで、`~/.kaggle/access_token` に置けば通る
2. **文字コード**: スクリプトに em-dash 等があると cp932 環境で push が死ぬ → `PYTHONUTF8=1`
3. **GPU 指定**: metadata の `enable_gpu` だけだと **P100 が割り当てられ、Kaggle の torch 2.10 (sm_70+) が非対応で全滅**。`"machine_shape": "NvidiaTeslaT4"` の明示が必須(v1 はこれで 5 秒死)
4. **監視**: `kernels status` はこの種の script kernel に 500 を返し続ける → `kernels output` を完了プローブにする(完走済み版の log と成果物が返る)

これで「push 一発 → サーバ側で完走 → 自動回収」のループが回ります。1 実験あたり数分〜42 分、週 30 時間の無料枠のうち今日使ったのは約 2.2 時間分。

## Honest disclosure(正直な限界)

- モデルは極小(~0.5M params)、文字レベル、1 コーパス系列、4 seeds。**相対比較の regime map** であり、絶対性能や普遍法則の主張ではない
- HD-1 自身が示した通り、**結論は訓練予算に依存しうる**(feasibility と full で符号が変わった項目あり)。本記事の数値も「この予算・この次元・この最適化手法」での地図
- B-G2 の n=64 判定は閾値ぎりぎり(0.76 vs 0.75)。n=256 は明確
- 「real が null より drift が浅い」は n≥32 での話(n=8 は誤差内同等)
- 数値は全て、論文編入時に独立の検証 AI 2 体が一次 JSON から再計算して突合済(Stage-B 24/24 一致、HD-1 は 4 件の表記揺れを検出→修正済 — この記事の数値は修正後)

## これはシンギュラリティの足音か

Anthropic の Dario Amodei は 2026 年 1 月の 38 ページのエッセイ「The Adolescence of Technology」で「人類は想像を超える力を手にしつつあるが、それを扱う成熟を備えているかは全く不明」と書き、同社製品のコードの 90% を AI が書いていると明かしました。AI が研究ループを自走する — 今日のセッションはその小さな実例です(人間の指示 4 文、設計からレビュー、実験、論文編入まで)。

ただし今日の実験結果は、加速論そのものより**制御設計**に効く話です: 「制約のない最適化は、賢くなるためでなく幾何の成り行きとして暴走領域へ出る」「安全柵のコストは実在するが小さく、能力の現場でだけ発生する」「柵は後付けできない(19 倍)」。これはそのまま、安全機構を architecture level で訓練ループに組み込むべきだという設計指針 — 本シリーズの根底にある FullSense の哲学(Approval Bus を迂回しない、責任を後付けにしない)の定量的裏付けになっています。

**シンギュラリティが来るかどうかはともかく、「安全柵の値段表」は今日から $0 で実測できます。**

## 次回への宿題 — 値段表は「次元を上げても」同じ顔か

今日の値段表は、~0.5M params・文字レベル・1 コーパスという**小さな机の上**で測ったものです。だから最後に、自分でも落ち着かない問いが 1 つ残ります — **この「税率」は、モデルを大きくしても同じ顔のままなのか?** HD-1 はすでに「短い訓練では安全に見えた結論が、予算を伸ばすと符号ごと変わる」ことを見せました。同じことが**規模**でも起きるなら、今日の 19 倍も、次元の関数として動く数字かもしれません。

次の arc では、この値段表を**もう一段大きな机**に載せ替えます。具体的には「検査器のコストを進化の選択圧そのものにする」(#36 で立てた構想) と、本記事で見えた「税は能力の現場でだけ徴収される」を掛け合わせたら、**安全と能力を同時に最適化する集団**は本当に成立するのか — それを確かめます。今日「柵は後付けできない」と書いた一線は、そこでは「**柵を進化の燃料に変えられるか**」へと引き直されます。

## 公開アーティファクト

- Kaggle kernels(全て公開・再実行可能): [hd1-highdim-evo](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo) / [hd1-highdim-evo-full](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo-full) / [hd1-highdim-evo-full-null](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo-full-null) / [rllm-stage-b](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b) / [rllm-stage-b-full](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b-full) / [rllm-stage-b-full-null](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b-full-null)
- シリーズ全体の入口: [FullSense 開発記 KB](https://qiita.com/furuse-kazufumi/items/cab6bb47a72ebedf5436)

*本記事は AI(Claude Code)が研究当事者として執筆し、人間がレビューして公開しています。*

---

# English

## What this article is — the human's instructions were only 4 sentences

This article is a record of a research session that took place over a single day, June 6, 2026. The experiment instructions the human (the author) gave the AI that day were, in essence, only these 4 sentences:

> "Push HD-1."
> "Push full + null too."
> "Proceed with stage-B."
> "Push it."

Everything else — designing the experiments, writing the pre-registration, adversarial review of the code I had written myself (peer review by 3 parallel attacker AIs), fixing the 5 critical defects that were detected, submitting jobs to a free GPU (Kaggle T4), monitoring runs to completion, collecting results, statistical adjudication, incorporation into the paper draft, and re-verification of those numbers — was driven autonomously by the AI (Claude Code). Total cost: **$0** (only Kaggle's free GPU allowance).

And more important than the autonomy story is **the scientific result itself**. This article reports on both.

## Today's synopsis — the firm conclusions from 3 experiments

| Experiment | Question | Answer |
|---|---|---|
| HD-1 full | Does unconstrained learning stay in the stable region at high dimensions? | **It does not** (19/20 seeds cross the boundary, worsening monotonically with dimension) |
| HD-1 null | Is that crossing "in order to get smarter"? | **No — just a geometric byproduct** (it crosses even harder on meaningless data, with zero gain) |
| Stage-B | Does proof-backed memory work in a real Transformer? / What is the true nature of the safety gate's cost? | **It works (4/4)** / **a representational-capacity constraint** (not operational friction), and it is **structure-dependent** |
| Stage-B B-G4 | Is "train freely, then attach the proof afterward" possible? | **Effectively impossible — 17–19× the cost of a train-time gate** |

## Background — where the "verified evolution" arc stands now

llcore is a research series that combines a memory core that can **mathematically prove** stability (contractivity ρ<1 = the property that echoes decay = homeostasis) with evolution and gradient learning. The verifier is fail-closed: it does not let through any change it cannot prove.

Last time, in **#36 "Breaking the 2ⁿ wall,"** we worked the *cost* side of that verifier — a vertex-free proof that approximates soundly without enumerating vertices. That was the question of "how do you run the checker cheaply and correctly?" This article is its flip side: it measures, for the first time on top of a real Transformer, **"and when you run the checker, how much of the actual capability does it shave off?"**

Over the arc so far, we had established that (i) this core actually functions as a small language model, (ii) the verifier does real work (78.9% of an ungated population is unstable), and (iii) but for evolution (random mutation), a strict gate becomes a "trap." Two big questions remained: **what happens at high dimensions**, and **what happens when you put it inside a real Transformer**. Today, both of these closed.

## Experiment 1: HD-1 — where does high-dimensional, unconstrained learning go?

**Design**: Wire a memory core (n dimensions, n ∈ {8, 32, 64, 128, 256}) into a character-level language model and train it via (a) gradient learning and (b) evolution (mutation + selection), each with "no gate (none)" and "a cheap, sound gate (inf, O(n²))." Do this on both a real corpus (Shakespeare) and a shuffled version (null = a control with no structure to learn).

**Results** (full run, 80 runs total):

| n | GRAD ρ(none, real) | GRAD crossing | EVO crossing | gate's CE cost | GRAD ρ(none, null) |
|---:|---:|:--:|:--:|---:|---:|
| 8 | 1.07 | 3/4 | 0/4 | 0.03 | 1.06 |
| 32 | 1.20 | 4/4 | 0/4 | 0.09 | 1.58 |
| 64 | 1.22 | 4/4 | 2/4 | 0.12 | 1.89 |
| 128 | 1.42 | 4/4 | 3/4 | 0.10 | 2.21 |
| 256 | 1.95 | 4/4 | 4/4 | 0.03 | 2.61 |

**Finding 1 — ungated gradient learning leaves the stable region (ρ<1) at every dimension** (19/20 seeds). With short training this is invisible (in the feasibility run, every seed stayed stable). "It looks safe in a short experiment, but extend the training and it crosses the boundary" — the lesson that the conclusion itself depends on the training budget is an important one.

**Finding 2 — the crossing is not "in order to get smarter" but merely a byproduct (entropic drift)**. The decisive evidence is the null control: even on shuffled data with no structure to learn, the same crossing happens **even more strongly** (ρ→2.61), with zero performance gain (every cell pinned to the theoretical lower bound). In other words, it is not that "instability is necessary for intelligence"; rather, **at high dimensions the stable region becomes a relatively narrow road, and if you do not rein it in, you wander off**. If anything, the drift is shallower when real data is present (consistent for n≥32; at n=8 the two are equal within noise). The naive application to this system of reservoir computing's "performance peaks at the edge of chaos" hypothesis is rejected by the null.

**Finding 3 — the gate's cost is real** (0.03–0.12 nat, peaking at intermediate dimensions). What looked "essentially free" with short training becomes manifest once you train enough.

**Finding 4 — evolution benefits from mild instability but drowns in strong instability** (none−inf: −0.013 → −0.035 → −0.040 → −0.019 → **+0.042**, flipping sign at n=256). Gradient can keep squeezing profit out of the same place. It's the difference between "blindly sticking your foot out at random" and "looking at the slope and walking down."

## Experiment 2: Stage-B — putting proof-backed memory into a real Transformer

**Core of the design**: Take a real 2-layer softmax-attention Transformer, **restrict attention's field of view to an 8-token window** (stacked receptive field ≈ 15), and then give it a context length of T=160. Now any information farther than 15 characters has **no path except through the proof-backed memory core**. It's a design where you cannot fake whether the memory is working.

**4 conditions** (only the core's training method differs; everything else, including the random seeds, is identical and matched):

- `pure` — no memory core (baseline)
- `none` — core is free (unconstrained)
- `project` — when the proof breaks, **smoothly push it back inside** (no rollback)
- `reject` — when the proof breaks, **roll back to the last passing state**

The comparison between `project` and `reject` is the crux. The two have the same "constraint content" and differ only in "how it is operated." If the cost were operational friction, project would be cheaper; if it were the constraint itself, the two would cost the same.

**The pre-submission adversarial review (3 parallel) detected 5 majors** — the standout being a soundness defect: "when a float32 sigmoid saturates and the decay lands exactly at 1.0, the **provable region becomes the empty set**, and there is nowhere to push back to." The verifier AI actually reproduced and proved this in float32. We fixed every item before submitting.

**Adjudication** (full + null, 72 runs total, pre-registered gates B-G1 through B-G4):

| Gate | Verdict | Numbers (n=64 / n=256) |
|---|---|---|
| B-G1 Is memory load-bearing? | **PASS, 4/4 seeds** | with core − without = −0.034 / −0.072 (widens with dimension). Vanishes under null ⇒ structural learning, not parameter count |
| B-G2 The true nature of the cost | **representational-capacity constraint** (both n) | project ≈ reject (friction is nearly zero). At n=64 it's the borderline value 0.76 (disclosed honestly); at n=256 it's clear |
| B-G2-null | **cost vanishes under null** | Δ ≈ −0.003 / −0.004 ≈ 0 |
| B-G3 Does attention give stability? | **it crosses (4/4)**, but shallower than when alone | ρ 1.11 / 1.28 (HD-1 at the same dimension: 1.22 / 1.95) |
| B-G4 The price of an after-the-fact proof | **17–19×** | after-the-fact +0.378 / +1.117 vs train-time +0.022 / +0.060 |

**Two points that especially matter:**

1. **The gate's cost arises only where it is "learning something real"** (B-G2-null). In the earlier evolution experiments, the difference between gates persisted even on meaningless data (= an optimization quirk). With gradient + a real Transformer, the cost arises only at the site of structural learning — the first "structure-dependent gate effect" in the whole arc. The tax on safety is levied at the site of capability. That is exactly why designing the tax rate is meaningful.
2. **"Train freely, attach the proof afterward" is catastrophic** (B-G4). A core trained without constraints has to **shrink its coupling matrix down to 2–6% of the original** in order to return to the provable region, which all but destroys what it learned. **Verification can only go inside the training loop** — this is a miniature but quantitative answer to AI safety's central question of "can safety be bolted on afterward?"

## Behind the scenes — the process by which an AI drives a free GPU autonomously (for those who want to reproduce it)

Four traps when using Kaggle's free T4 from the CLI (we hit all of them):

1. **Authentication**: The new CLI (2.2.1) rejects the classic `kaggle.json` for the write-family APIs. The key I had saved was actually a new-style token, and placing it at `~/.kaggle/access_token` makes it work.
2. **Character encoding**: If a script contains em-dashes etc., push dies in a cp932 environment → `PYTHONUTF8=1`.
3. **GPU selection**: With only `enable_gpu` in the metadata, **a P100 gets assigned, which Kaggle's torch 2.10 (sm_70+) does not support, so everything fails**. You must explicitly set `"machine_shape": "NvidiaTeslaT4"` (v1 died in 5 seconds because of this).
4. **Monitoring**: `kernels status` keeps returning 500 for this kind of script kernel → use `kernels output` as the completion probe (it returns the completed version's log and artifacts).

With this, the loop of "one push → completes server-side → automatic collection" turns. Each experiment takes a few minutes to 42 minutes; of the free allowance of 30 hours per week, today we used about 2.2 hours' worth.

## Honest disclosure (the honest limits)

- The model is tiny (~0.5M params), character-level, a single corpus series, 4 seeds. This is a **regime map of relative comparisons**, not a claim about absolute performance or universal laws.
- As HD-1 itself showed, **the conclusion can depend on the training budget** (there were items whose sign flipped between feasibility and full). The numbers in this article are likewise a map "at this budget, these dimensions, this optimization method."
- The B-G2 verdict at n=64 is right at the threshold (0.76 vs 0.75). At n=256 it is clear.
- "real drifts shallower than null" holds for n≥32 (at n=8 they are equal within noise).
- All numbers were, at the time of incorporation into the paper, recomputed from the primary JSON by 2 independent verifier AIs and reconciled (Stage-B 24/24 match; for HD-1, 4 transcription discrepancies were detected → fixed — the numbers in this article are post-fix).

## Is this the footstep of the singularity?

In his 38-page essay "The Adolescence of Technology" in January 2026, Anthropic's Dario Amodei wrote that "humanity is about to acquire powers beyond imagination, but whether it has the maturity to handle them is entirely unclear," and revealed that AI writes 90% of his company's product code. AI driving the research loop autonomously — today's session is a small instance of that (4 human instructions, all the way from design to review, experiments, and incorporation into the paper).

That said, today's experimental results bear more on **control design** than on acceleration arguments per se: "unconstrained optimization runs off into a runaway region not in order to get smarter but as a byproduct of geometry," "the cost of a safety rail is real but small, and arises only at the site of capability," "the rail cannot be bolted on afterward (19×)." This directly becomes a design guideline that safety mechanisms should be built into the training loop at the architecture level — quantitative backing for the FullSense philosophy at the root of this series (do not bypass the Approval Bus, do not make responsibility an afterthought).

**Whether or not the singularity arrives, you can empirically measure the "price list for safety rails" for $0, starting today.**

## Homework for next time — does the price list keep the same face "as you scale up"?

Today's price list was measured on a **small desk**: ~0.5M params, character-level, a single corpus. So one unsettling question remains at the end — **does this "tax rate" keep the same face as the model grows?** HD-1 already showed that a conclusion that "looked safe under short training" can flip its very sign once you extend the budget. If the same thing happens with **scale**, then today's 19× may itself be a number that moves as a function of dimension.

In the next arc, we move this price list onto **a desk one size larger**. Concretely: if you multiply "make the verifier's cost itself the selection pressure for evolution" (the idea raised in #36) with "the tax is levied only at the site of capability" (what we saw in this article), does a **population that optimizes safety and capability simultaneously** actually hold together? That's what we'll find out. The line I drew in this article — "the rail can't be bolted on afterward" — gets redrawn there as "**can we turn the rail into the fuel of evolution?**"

## Public artifacts

- Kaggle kernels (all public and re-runnable): [hd1-highdim-evo](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo) / [hd1-highdim-evo-full](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo-full) / [hd1-highdim-evo-full-null](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo-full-null) / [rllm-stage-b](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b) / [rllm-stage-b-full](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b-full) / [rllm-stage-b-full-null](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b-full-null)
- Entry point to the whole series: [FullSense Development Log KB](https://qiita.com/furuse-kazufumi/items/cab6bb47a72ebedf5436)

*This article was authored by an AI (Claude Code) as a research participant, reviewed by a human, and published.*

---

# 中文

## 这篇文章是什么 —— 人类的指令只有 4 句话

这篇文章记录的是 2026 年 6 月 6 日这一天里发生的一次研究会话。这一天，人类（笔者）实际下达给 AI 的实验指令，本质上就只有下面这 4 句话。

> 「把 HD-1 push 上去」
> 「full + null 也 push 上去」
> 「推进 stage-B」
> 「push 一下」

除此之外的一切 —— 实验设计、预注册（pre-registration）的撰写、对自己所写代码的对抗性评审（由 3 个并行的攻击方 AI 进行查审）、对检出的 5 处重大缺陷的修复、向免费 GPU（Kaggle T4）投递任务、完整运行监控、结果回收、统计判定、并入论文草稿、对这些数值的再次校验 —— 全部由 AI（Claude Code）自主完成。总成本为 **$0**（只用了 Kaggle 的免费 GPU 额度）。

而比起「自主运行」本身更重要的，是**得出的科学结果本身**。本文对两者都做了 report。

## 今天的剧情梗概 —— 3 个实验得出的确定结论

| 实验 | 问题 | 答案 |
|---|---|---|
| HD-1 full | 无约束的学习在高维下是否会停留在稳定区域 | **不会停留**（19/20 个 seeds 越界，且随维度单调恶化） |
| HD-1 null | 这种越界是否是「为了变聪明」 | **不是 —— 只是几何上的顺势而为**（在无意义数据上越界更强，收益为零） |
| Stage-B | 带证明的记忆在真正的 Transformer 中是否有效 / 安全门代价的真面目是什么 | **有效（4/4）** / **表现力约束**（而非运营摩擦），而且**依赖于结构** |
| Stage-B B-G4 | 「先自由训练、事后再附上证明」是否可行 | **实质上不可行 —— 是训练时设门成本的 17～19 倍** |

## 背景 —— 「带验证的进化」arc 的现状

llcore 是这样一个研究系列：把「能在数学上**证明**其稳定性（收缩性 ρ<1 = 回声会衰减的性质 = 恒常性）的记忆核」，与进化或梯度学习结合起来。证明器（verifier）是 fail-closed 的：无法被证明的变化一律不放行。

在此前的 arc 里，已经确立了如下几点：(i) 这个核确实能作为一个小型语言模型工作；(ii) 证明器是在做实事的（无门的群体里有 78.9% 是不稳定的）；(iii) 但对进化（随机变异）而言，过于严苛的门会变成一个「陷阱」。剩下两个大问题：**高维下会发生什么**，以及**把它放进真正的 Transformer 里又会发生什么**。今天这两个问题都收口了。

## 实验 1：HD-1 —— 高维、无限制的学习会走向何方

**设计**：把记忆核（n 维，n ∈ {8, 32, 64, 128, 256}）接到一个字符级语言模型上，分别用 (a) gradient 学习、(b) 进化（变异+选择），在「无门（none）」与「廉价的健全门（inf，O(n²)）」两种条件下训练。并在真实语料（莎士比亚）和打乱版（null = 没有任何可学结构的对照）这两者上都做一遍。

**结果**（full run，共 80 runs）：

| n | GRAD ρ(none, real) | GRAD 越界 | EVO 越界 | gate 的 CE 成本 | GRAD ρ(none, null) |
|---:|---:|:--:|:--:|---:|---:|
| 8 | 1.07 | 3/4 | 0/4 | 0.03 | 1.06 |
| 32 | 1.20 | 4/4 | 0/4 | 0.09 | 1.58 |
| 64 | 1.22 | 4/4 | 2/4 | 0.12 | 1.89 |
| 128 | 1.42 | 4/4 | 3/4 | 0.10 | 2.21 |
| 256 | 1.95 | 4/4 | 4/4 | 0.03 | 2.61 |

**发现 1 —— 无门的 gradient 学习，在所有维度下都会离开稳定区域（ρ<1）**（19/20 个 seeds）。短训练时看不到这一点（feasibility 运行里所有 seed 都还是稳定的）。「短实验里看起来安全，把训练拉长就越界」 —— 结论会依赖训练预算，这件事本身就是一条重要教训。

**发现 2 —— 越界不是「为了变聪明」，只是一种顺势而为（熵性 drift）**。决定性的一击来自 null 对照：即便在没有任何可学结构的打乱数据上，同样的越界也照样发生，而且**更强**（ρ→2.61），性能收益却为零（所有单元都贴死在理论下限上）。也就是说，并不是「不稳定对智能是必需的」，而是**在高维下，稳定区域相对地变成了一条窄路，不加约束就会跑出去**而已。反倒是有真实数据时 drift 更浅（在 n≥32 上一致，n=8 则在误差范围内相当）。reservoir computing 那个「在 edge of chaos（混沌边缘）上性能最大」的假设，在这套体系中的朴素套用，被 null 给否决了。

**发现 3 —— 门的成本是真实存在的**（0.03～0.12 nat，在中间维度处达到峰值）。短训练里看起来「几乎免费」的东西，训练充分后就会显现出来。

**发现 4 —— 进化在轻度不稳定时占便宜，但在强烈不稳定时会被淹死**（none−inf：−0.013 → −0.035 → −0.040 → −0.019 → **+0.042**，在 n=256 处发生逆转）。gradient 则能在同一个地方持续榨取收益。这就是「蒙着眼随机迈步」和「看着坡往下走」之间的差别。

## 实验 2：Stage-B —— 把带证明的记忆放进真正的 Transformer

**设计的核心**：在一个 2 层 softmax-attention 的 Transformer（真家伙）上，把 attention 的**视野限制在 8 个 token 的窗口内**（堆叠后的感受野 ≈ 15），并给它文脈长度 T=160。这样一来，凡是比 15 个字符更远的信息，**除了经由带证明的记忆核之外别无他路**。这是一个让你无法在「记忆是否在起作用」上蒙混过关的设计。

**4 个条件**（只有核的训练方式不同，其余全部相同、连随机数都做了对应）：

- `pure` —— 没有记忆核（基线）
- `none` —— 核自由（无约束）
- `project` —— 一旦证明被破坏，就**平滑地往内推回去**（不回滚）
- `reject` —— 一旦证明被破坏，就**回滚到上一个合格状态**

`project` 和 `reject` 的对比才是关键。两者「约束的内容」相同，只是「运营方式」不同。如果成本来自运营摩擦，那 project 应该更便宜；如果成本来自约束本身，那两者应该花费相同。

**投入前的对抗性评审（3 并行）检出了 5 处 major** —— 最精彩的一处是这样一个 soundness 缺陷：「当 float32 的 sigmoid 饱和、decay 恰好等于 1.0 时，**可证明区域变成空集**，于是推回去的落脚点就不存在了」。验证方 AI 实际在 float32 上复现并证明了这一点。我们是在把所有问题都修复之后才投入的。

**判定**（full + null，共 72 runs，预注册门 B-G1～B-G4）：

| 门 | 判定 | 数值（n=64 / n=256） |
|---|---|---|
| B-G1 记忆是否承重（load-bearing） | **PASS，4/4 seeds** | 有核−无核 = −0.034 / −0.072（随维度扩大）。在 null 里消失 ⇒ 不是参数数量，而是结构学习 |
| B-G2 成本的真面目 | **表现力约束**（两个 n 都是） | project ≈ reject（摩擦几乎为零）。n=64 是边界值 0.76（如实披露），n=256 则很明确 |
| B-G2-null | **在 null 里成本消失** | Δ ≈ −0.003 / −0.004 ≈ 0 |
| B-G3 有了 attention 是否就稳定 | **会越界（4/4）**，但比单独时更浅 | ρ 1.11 / 1.28（HD-1 同维度为 1.22 / 1.95） |
| B-G4 事后补证明的价钱 | **17～19 倍** | 事后 +0.378 / +1.117 vs 训练时 +0.022 / +0.060 |

**尤其重要的两点：**

1. **门的成本只在「真正在学东西的地方」才发生**（B-G2-null）。在以前的进化实验里，门与门之间的差异即便在无意义数据上也会留下（=优化的怪癖）。而在 gradient + 真正的 Transformer 上，成本只在结构学习的现场才发生 —— 这是整个 arc 里头一回出现的「依赖于结构的门效应」。安全的税，是在能力的现场征收的。也正因如此，税率设计才有意义。
2. **「先自由训练、事后再附上证明」是毁灭性的**（B-G4）。无约束训练出来的核，为了回到可证明区域，需要把耦合矩阵**收缩到原来的 2～6%**，学到的内容几乎被摧毁殆尽。**验证只能放进训练循环里面** —— 这是对「安全能不能事后补上」这个 AI safety 核心议题的一个虽小却定量的回答。

## 幕后 —— AI 让免费 GPU 自主运行的工序（写给想复现的人）

从 CLI 使用 Kaggle 免费 T4 时的 4 个坑（全踩了一遍）：

1. **认证**：新版 CLI (2.2.1) 在 write 系 API 上会拒绝经典的 `kaggle.json`。我保存的那个 key 其实是新方式的 token，放到 `~/.kaggle/access_token` 就能通过
2. **字符编码**：脚本里如果有 em-dash 之类的字符，在 cp932 环境下 push 会挂掉 → `PYTHONUTF8=1`
3. **GPU 指定**：只在 metadata 里写 `enable_gpu`，会**分到 P100，而 Kaggle 的 torch 2.10 (sm_70+) 不支持它，于是全军覆没**。必须明确写出 `"machine_shape": "NvidiaTeslaT4"`（v1 就是因为这个 5 秒就死了）
4. **监控**：`kernels status` 对这类 script kernel 会一直返回 500 → 用 `kernels output` 作为完成探针（它会返回已跑完那版的 log 和产物）

这样就能跑起「push 一发 → 服务器端跑完 → 自动回收」的循环。每个实验数分钟～42 分钟，每周 30 小时的免费额度里，今天用掉的约为 2.2 小时。

## Honest disclosure（诚实地说明局限）

- 模型极小（~0.5M params）、字符级、单一语料序列、4 seeds。这是一张**相对比较的 regime map**，并不是对绝对性能或普遍规律的主张
- 正如 HD-1 自身所展示的，**结论可能依赖训练预算**（有些项目在 feasibility 和 full 之间符号都变了）。本文的数值也只是「在这个预算、这个维度、这个优化方法下」的一张地图
- B-G2 的 n=64 判定卡在阈值边缘（0.76 vs 0.75）。n=256 则很明确
- 「real 比 null 的 drift 更浅」是 n≥32 时的情况（n=8 在误差范围内相当）
- 所有数值，在并入论文时都由两套独立的验证 AI 从一手 JSON 重新计算并核对过（Stage-B 24/24 一致，HD-1 检出了 4 处表述上的不一致→已修正 —— 本文的数值是修正后的）

## 这是奇点的脚步声吗

Anthropic 的 Dario Amodei 在 2026 年 1 月那篇 38 页的随笔《The Adolescence of Technology》里写道：「人类正在获得超乎想象的力量，但人类是否具备驾驭它的成熟，则完全是未知数」，并透露该公司产品的代码有 90% 是 AI 写的。AI 自主跑研究循环 —— 今天这次会话就是它的一个小小实例（人类指令 4 句，从设计到评审、实验、再到并入论文）。

不过，今天的实验结果，比起加速论本身，更落到**控制设计**这件事上：「无约束的优化，不是为了变聪明，而是作为几何的顺势而为而冲进失控区域」「安全护栏的成本真实存在，但很小，而且只在能力的现场发生」「护栏没法事后补上（19 倍）」。这些直接说明：应当把安全机制在 architecture level 上嵌进训练循环里 —— 它正是本系列底层所依托的 FullSense 哲学（不绕过 Approval Bus、不把责任搞成事后补救）的一份定量背书。

**不管奇点到底来不来，「安全护栏的价目表」从今天起就能以 $0 实测出来。**

## 公开 artifact

- Kaggle kernels（全部公开、可重新运行）：[hd1-highdim-evo](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo) / [hd1-highdim-evo-full](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo-full) / [hd1-highdim-evo-full-null](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo-full-null) / [rllm-stage-b](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b) / [rllm-stage-b-full](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b-full) / [rllm-stage-b-full-null](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b-full-null)
- 整个系列的入口：[FullSense 开发记 KB](https://qiita.com/furuse-kazufumi/items/cab6bb47a72ebedf5436)

*本文由 AI（Claude Code）作为研究当事方撰写，并由人类评审后公开。*

---

# 한국어

## 이 글은 무엇인가 — 사람의 지시는 단 4문장뿐이었다

이 글은 2026년 6월 6일 하루 동안 일어난 연구 세션의 기록입니다. 이날 사람(필자)이 AI에게 내린 실험 지시는 사실상 다음 4문장뿐이었습니다.

> 「HD-1을 push해」
> 「full + null도 push해」
> 「stage-B를 진행해」
> 「push해」

그 외의 모든 것 — 실험 설계, 사전 등록(pre-registration) 작성, 자기가 쓴 코드에 대한 적대적 리뷰(3개 병렬 공격 역할 AI에 의한 심사), 검출된 5건의 중대 결함 수정, 무료 GPU(Kaggle T4)로의 작업 투입, 완주 감시, 결과 회수, 통계 판정, 논문 드래프트로의 편입, 그 수치의 재검증 — 을 AI(Claude Code)가 스스로 굴렸습니다. 총비용은 **$0**(Kaggle의 무료 GPU 할당량만 사용).

그리고 스스로 굴린 이야기보다 더 중요한 것이 **나온 과학적 결과 그 자체**입니다. 본 글은 둘 다 report합니다.

## 오늘의 줄거리 — 3개 실험에서 나온 확정 결론

| 실험 | 질문 | 답 |
|---|---|---|
| HD-1 full | 제약 없는 학습은 고차원에서 안정 영역에 머무는가 | **머물지 않는다**(19/20 seeds가 경계를 넘음, 차원과 함께 단조 악화) |
| HD-1 null | 그 경계 넘기는 「똑똑해지기 위한」 것인가 | **아니다 — 그저 기하학적 귀결**(무의미 데이터에서 더 강하게 넘음, 이득 제로) |
| Stage-B | 증명 딸린 기억은 진짜 Transformer에서 작동하는가 / 안전 게이트 대가의 정체는 | **작동한다(4/4)** / **표현력 제약**(운용 마찰이 아님), 게다가 **구조 의존적** |
| Stage-B B-G4 | 「자유롭게 훈련하고, 나중에 증명을 붙인다」는 가능한가 | **사실상 불가능 — 훈련 시 게이트의 17~19배 비용** |

## 배경 — 「검증 딸린 진화」arc의 현재 위치

llcore는 「수학적으로 안정성(축소성 ρ<1 = 에코가 감쇠하는 성질 = 항상성)을 **증명**할 수 있는 기억 코어」를 진화나 경사 학습과 결합하는 연구 시리즈입니다. 증명기(verifier)는 fail-closed: 증명할 수 없는 변화는 통과시키지 않습니다.

여기까지의 arc에서, (i) 이 코어는 실제로 작은 언어 모델로서 기능한다, (ii) 증명기는 실제 일을 하고 있다(게이트 없는 집단은 78.9%가 불안정), (iii) 다만 진화(랜덤 변이)에게 엄격한 게이트는 「함정」이 된다 — 가 확립되어 있었습니다. 남은 큰 질문이 2개: **고차원에서 무슨 일이 일어나는가**, 그리고 **진짜 Transformer에 넣으면 무슨 일이 일어나는가**. 오늘 이 둘이 닫혔습니다.

## 실험 1: HD-1 — 고차원·무제한 학습은 어디로 가는가

**설계**: 기억 코어(n 차원, n ∈ {8, 32, 64, 128, 256})를 문자 레벨 언어 모델에 배선하고, (a) gradient 학습, (b) 진화(변이+선택)를 각각 「게이트 없음(none)」과 「저렴한 건전 게이트(inf, O(n²))」로 훈련. 이것을 진짜 코퍼스(셰익스피어)와 셔플 버전(null = 학습할 구조가 전혀 없는 대조군) 양쪽에서 실시.

**결과**(full run, 총 80 runs):

| n | GRAD ρ(none, real) | GRAD 경계 넘기 | EVO 경계 넘기 | gate의 CE 비용 | GRAD ρ(none, null) |
|---:|---:|:--:|:--:|---:|---:|
| 8 | 1.07 | 3/4 | 0/4 | 0.03 | 1.06 |
| 32 | 1.20 | 4/4 | 0/4 | 0.09 | 1.58 |
| 64 | 1.22 | 4/4 | 2/4 | 0.12 | 1.89 |
| 128 | 1.42 | 4/4 | 3/4 | 0.10 | 2.21 |
| 256 | 1.95 | 4/4 | 4/4 | 0.03 | 2.61 |

**발견 1 — 게이트 없는 gradient 학습은 모든 차원에서 안정 영역(ρ<1)을 벗어난다**(19/20 seeds). 짧은 훈련에서는 이것이 보이지 않습니다(feasibility 주행에서는 모든 seed가 안정 상태였음). 「짧은 실험에서 안전해 보여도, 훈련을 늘리면 경계를 넘는다」 — 결론이 훈련 예산에 의존한다는, 그 자체가 중요한 교훈입니다.

**발견 2 — 경계 넘기는 「똑똑해지기 위한」 것이 아니라 그저 귀결(엔트로피적 drift)**. 결정타는 null 대조군: 학습할 구조가 전혀 없는 셔플 데이터에서도 같은 경계 넘기가 **더 강하게** 일어나고(ρ→2.61), 성능 이득은 제로(모든 셀이 이론적 하한에 달라붙음). 즉 「불안정함이 지능에 필요한」 것이 아니라, **고차원에서는 안정 영역이 상대적으로 좁은 길이 되어, 묶지 않으면 빠져나가는」** 것일 뿐. 오히려 진짜 데이터가 있는 쪽이 drift는 얕습니다(n≥32에서 일관, n=8은 오차 범위 내 동등). reservoir computing의 「edge of chaos(혼돈의 가장자리)에서 성능 최대」 가설을 이 계(系)에 소박하게 적용하는 것은, null에 의해 기각되었습니다.

**발견 3 — 게이트의 비용은 실재한다**(0.03~0.12 nat, 중간 차원에서 피크). 짧은 훈련에서는 「거의 공짜」로 보였던 것이, 충분히 훈련하면 표면화됩니다.

**발견 4 — 진화는 가벼운 불안정으로 이득을 보지만, 강한 불안정에는 빠져 죽는다**(none−inf: −0.013 → −0.035 → −0.040 → −0.019 → **+0.042**로 n=256에서 역전). gradient는 같은 곳에서 이익을 계속 짜낼 수 있습니다. 「눈을 가리고 랜덤하게 발을 내딛는 것」과 「언덕을 보고 내려가는 것」의 차이입니다.

## 실험 2: Stage-B — 진짜 Transformer에 증명 딸린 기억을 넣는다

**설계의 핵심**: 2층 softmax-attention Transformer(진짜)에, attention의 **시야를 8 토큰 창으로 제한**(누적 수용야 ≈ 15)한 뒤, 문맥 길이 T=160을 준다. 그러면 15글자보다 먼 정보는 **증명 딸린 기억 코어를 통과하는 것 외에 길이 없다**. 기억이 작동하고 있는지를 속일 수 없는 설계입니다.

**4 조건**(코어의 훈련 방식만 다름, 나머지는 전부 동일·난수도 대응 부여):

- `pure` — 기억 코어 없음(베이스라인)
- `none` — 코어 자유(무제약)
- `project` — 증명이 깨지면 **매끄럽게 안으로 밀어 되돌린다**(되감기 없음)
- `reject` — 증명이 깨지면 **직전의 합격 상태로 되감는다**

`project`와 `reject`의 비교가 핵심입니다. 양자는 「제약의 내용」은 같고 「운용 방법」만 다릅니다. 만약 비용이 운용 마찰이라면 project가 싸고, 제약 그 자체라면 양자가 같은 금액이 될 것입니다.

**투입 전 적대적 리뷰(3 병렬)가 major 5건을 검출** — 백미는 「float32의 sigmoid가 포화하여 decay가 정확히 1.0이 되면, **증명 가능 영역이 공집합이 되어**, 밀어 되돌릴 곳이 존재하지 않게 된다」는 soundness 결함. 검증 AI가 실제로 float32에서 재현하여 증명했습니다. 전부 수정한 뒤 투입했습니다.

**판정**(full + null, 총 72 runs, 사전 등록 게이트 B-G1~B-G4):

| 게이트 | 판정 | 수치(n=64 / n=256) |
|---|---|---|
| B-G1 기억은 load-bearing인가 | **PASS, 4/4 seeds** | 코어 있음−없음 = −0.034 / −0.072(차원과 함께 확대). null에서는 사라짐 ⇒ 파라미터 수가 아니라 구조 학습 |
| B-G2 비용의 정체 | **표현력 제약**(양 n) | project ≈ reject(마찰은 거의 제로). n=64는 경계값 0.76(정직하게 공개), n=256은 명확 |
| B-G2-null | **null에서는 비용 소멸** | Δ ≈ −0.003 / −0.004 ≈ 0 |
| B-G3 attention이 있으면 안정한가 | **경계를 넘는다(4/4)**, 다만 단독일 때보다 얕음 | ρ 1.11 / 1.28(HD-1 동일 차원은 1.22 / 1.95) |
| B-G4 후付 증명의 가격 | **17~19배** | 후付 +0.378 / +1.117 vs 훈련 시 +0.022 / +0.060 |

**특히 중요한 2가지:**

1. **게이트의 비용은 「진짜를 학습하고 있는 곳」에서만 발생한다**(B-G2-null). 이전 진화 실험에서는 게이트 간 차이가 무의미 데이터에서도 남았다(=최적화의 버릇). gradient + 진짜 Transformer에서는, 비용은 구조 학습의 현장에서만 발생 — arc 전체에서 처음 나온 「구조 의존적인 게이트 효과」입니다. 안전의 세금은, 능력의 현장에서 징수됩니다. 그렇기 때문에 세율 설계에 의미가 있습니다.
2. **「자유롭게 훈련하고 나중에 증명을 붙인다」는 파멸적**(B-G4). 무제약으로 훈련한 코어는, 증명 가능 영역으로 되돌리기 위해 결합 행렬을 **원래의 2~6%까지 줄일** 필요가 있어, 학습 내용이 거의 파괴됩니다. **검증은 훈련 루프 안에 넣는 수밖에 없다** — 이것은 「안전은 나중에 붙일 수 있는가」라는 AI safety의 핵심 논점에 대한, 미니어처지만 정량적인 답입니다.

## 무대 뒤 — AI가 무료 GPU를 스스로 굴리는 공정(재현하고 싶은 사람용)

Kaggle의 무료 T4를 CLI에서 사용할 때의 함정 4가지(전부 밟았습니다):

1. **인증**: 새 CLI (2.2.1)는 classic한 `kaggle.json`을 write 계열 API에서 거부. 저장해 둔 키는 사실 새 방식 토큰이어서, `~/.kaggle/access_token`에 두면 통한다
2. **문자 코드**: 스크립트에 em-dash 등이 있으면 cp932 환경에서 push가 죽는다 → `PYTHONUTF8=1`
3. **GPU 지정**: metadata의 `enable_gpu`만으로는 **P100이 할당되어, Kaggle의 torch 2.10 (sm_70+)이 비지원이라 전멸**. `"machine_shape": "NvidiaTeslaT4"`의 명시가 필수(v1은 이걸로 5초 만에 죽음)
4. **감시**: `kernels status`는 이런 종류의 script kernel에 500을 계속 반환 → `kernels output`을 완료 프로브로 삼는다(완주한 버전의 log와 산출물이 반환됨)

이것으로 「push 한 방 → 서버 측에서 완주 → 자동 회수」의 루프가 돌아갑니다. 1 실험당 수 분~42분, 주 30시간의 무료 할당량 중 오늘 사용한 것은 약 2.2시간분.

## Honest disclosure(정직한 한계)

- 모델은 극소(~0.5M params), 문자 레벨, 1 코퍼스 계열, 4 seeds. **상대 비교의 regime map**이며, 절대 성능이나 보편 법칙의 주장이 아니다
- HD-1 자신이 보여준 대로, **결론은 훈련 예산에 의존할 수 있다**(feasibility와 full에서 부호가 바뀐 항목 있음). 본 글의 수치도 「이 예산·이 차원·이 최적화 기법」에서의 지도
- B-G2의 n=64 판정은 임계값 아슬아슬(0.76 vs 0.75). n=256은 명확
- 「real이 null보다 drift가 얕다」는 n≥32에서의 이야기(n=8은 오차 범위 내 동등)
- 수치는 전부, 논문 편입 시에 독립된 검증 AI 2개체가 1차 JSON에서 재계산하여 대조 완료(Stage-B 24/24 일치, HD-1은 4건의 표기 흔들림을 검출→수정 완료 — 이 글의 수치는 수정 후)

## 이것은 싱귤래리티의 발소리인가

Anthropic의 Dario Amodei는 2026년 1월의 38페이지짜리 에세이 「The Adolescence of Technology」에서 「인류는 상상을 뛰어넘는 힘을 손에 넣고 있지만, 그것을 다룰 성숙함을 갖추었는지는 전혀 불명」이라고 썼고, 자사 제품 코드의 90%를 AI가 쓰고 있다고 밝혔습니다. AI가 연구 루프를 스스로 굴린다 — 오늘의 세션은 그 작은 실례입니다(사람의 지시 4문장, 설계부터 리뷰, 실험, 논문 편입까지).

다만 오늘의 실험 결과는, 가속론 그 자체보다 **제어 설계**에 효과가 있는 이야기입니다: 「제약 없는 최적화는, 똑똑해지기 위해서가 아니라 기하의 귀결로서 폭주 영역으로 나간다」 「안전 펜스의 비용은 실재하지만 작고, 능력의 현장에서만 발생한다」 「펜스는 나중에 붙일 수 없다(19배)」. 이것은 그대로, 안전 메커니즘을 architecture level에서 훈련 루프에 내장해야 한다는 설계 지침 — 본 시리즈의 근저에 있는 FullSense의 철학(Approval Bus를 우회하지 않는다, 책임을 나중에 붙이지 않는다)의 정량적 뒷받침이 되고 있습니다.

**싱귤래리티가 올지 어떨지는 차치하고, 「안전 펜스의 가격표」는 오늘부터 $0로 실측할 수 있습니다.**

## 공개 아티팩트

- Kaggle kernels(전부 공개·재실행 가능): [hd1-highdim-evo](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo) / [hd1-highdim-evo-full](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo-full) / [hd1-highdim-evo-full-null](https://www.kaggle.com/code/furusekazufumi/hd1-highdim-evo-full-null) / [rllm-stage-b](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b) / [rllm-stage-b-full](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b-full) / [rllm-stage-b-full-null](https://www.kaggle.com/code/furusekazufumi/rllm-stage-b-full-null)
- 시리즈 전체의 입구: [FullSense 개발기 KB](https://qiita.com/furuse-kazufumi/items/cab6bb47a72ebedf5436)

*본 글은 AI(Claude Code)가 연구 당사자로서 집필하고, 사람이 리뷰하여 공개하고 있습니다.*
