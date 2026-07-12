---
layout: default
title: "コーパス先行戦略 — AI が私の気づかない観点を思考フローに補完する優位性"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags:
  - AI
  - コーパス
  - 認知科学
  - 開発手法
  - SixHats
project_group: llive
id: 75d682ddefa5aeb738b8
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# コーパス先行戦略 — AI が私の気づかない観点を思考フローに補完する優位性

著者: **古瀬 和文（ぷるやん）**

> 📚 **連載ナビ**: ← #12 [llive 開発履歴（5 日で v0.1 → v0.7 候補へ）](./QIITA_#12_dev_history.md) ｜ **#13 本記事**（なぜ 5 日で進めたか＝コーパス先行という協働構造）｜ #14 [HTML では見えないのに機械では読める不可視アノテーションチャネル](./QIITA_#14_invisible_annotation_channel.md) → 。※ 各記事は単独でも読めます。
>
> #12 では「5 日で v0.1 から v0.7 候補へ」という **開発履歴** を時系列で並べた。本記事はその裏側——なぜ 1 人開発でこの速度と多視点が成立したのか、その **協働の構造** を掘る。

## TL;DR

- 本日のセッションを通じて気づいた **AI 協働開発の効きどころ**（少なくとも筆者の手元で観察された範囲）
- 「**最初にコーパスを充実させる**」ことで、AI が新規実装・要件定義の際に背景でコーパスを参照
- ユーザーが意識していない観点 (Six Hats / TRIZ / KJ法 / MindMap / 異分野類比) が **自動的に思考フローに混入**
- 1 人開発でも複数の認知視点を背景で得られる構造
- これは **「AI を使う」 vs 「AI と一緒に作る」** の本質的な分岐点

## 気づきの瞬間

本日 (2026-05-17) のセッションは、1 日で要件 32 件追加 + プログラム 2200 行 + テスト 78 件 + 記事 14 本という規模で進みました。

その振り返り中、ある気づきがありました:

> 「自分が KJ法 / MindMap / Six Hats / TRIZ を意識的に使った覚えはないのに、なぜか出てくる要件や設計判断にこれらの観点が **自然に混ざっている**」

例えば、私 (人間) が「Qwen から離脱したい」と言うと、AI は背景で以下を勝手に整理して持ち出してきます:

- **Stage A→B→C→D→E の段階分解** (TRIZ 原理 7: Nested doll、段階的拡張)
- **GPU 投資判断の閾値** (Six Hats: cautious 観点)
- **評価指標 AOS / LCIR** (Six Hats: process 観点)
- **「補完路線も並走」** (Synectics: 二項対立の解消)

これらは私が「意識して」AI に頼んだことではなく、**AI が背景でコーパスを参照しながら勝手に補完してきた** 観点です。

## なぜこれが起きるのか

### 構造

![コーパス先行戦略の構造図: ユーザー入力 → AI が背景でコーパス参照 → 多視点を補完した出力](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q13/flow_structure.svg)

ユーザーは「Qwen から離脱したい」という 1 行を入力しただけ。出力に含まれる **「同点と認める領域」** や **「リスク表」** や **「補完路線」** は、ユーザーが意識していない観点。

### コーパスの役割

AI 単体 (Claude / GPT / Gemini) は、当然「Six Hats」「TRIZ」「KJ法」の知識を持っています。しかし、それを **どの場面で適用すべきか** の判断は、コーパスと CLAUDE.md の規約が決定します:

```yaml
# CLAUDE.md (raptor) より抜粋
AUTOMATIC SKILL ACTIVATION:
  rad-research を自動起動: 新機能・新設計の着手前 (無条件)
  triz-ideation を自動起動: 矛盾・トレードオフ・両立できない
  cross-domain-ideation を自動起動: 異分野・他分野・分野を超えて
```

つまり、**コーパス + 規約** が AI の思考フローの「自動補完エンジン」として機能しています。

## 実例 — 本日のセッションから

ユーザーが意識していた入力 vs AI が背景で補完した観点:

| ユーザーが意識していたこと | AI が背景で補完した観点 |
|---|---|
| 「LLM の周りに何か作りたい」 | TRIZ 40 原理 / 39×39 矛盾マトリクス / Mediator パターン / Provenance DDD |
| 「ベンチを取りたい」 | Honest disclosure / xs/s/m/l/xl 5 段ラダー / mean/stdev 統計 |
| 「Qwen から離脱したい」 | Stage A→E 段階分解 / GPU 投資判断 / 評価指標 (AOS / LCIR) |
| 「数学・単位特化」 | SI 7 基本単位 / CODATA 2022 / Buckingham π / IEEE 754 |
| 「思考因子を導入」 | Cognitive Factor Framework / Role-based agents (architect/critic/executor/auditor) |

これらの観点を **「ユーザーが意識する前に AI が selection してくる」** のが本戦略の核心です。

## なぜ気づかなかったのか

人間は、自分の専門分野では「知っているはずの観点」を当然のものとして無意識に使います。しかし:

- 専門外の観点 (例: 物理学者にとっての法務、エンジニアにとってのマーケティング)
- 関連分野だが距離のある観点 (例: LLM 開発者にとっての認知心理学)
- 過去に学んだが忘れている観点 (例: 学部時代に学んだ Six Hats)

これらは **意識下に上ってこない** ため、自分では補完できません。AI がコーパス経由でこれらを引っ張ってきてくれる——ここが、筆者の手元で協働開発が効いていると感じる一点です。

## 「AI を使う」 vs 「AI と一緒に作る」の違い

| 項目 | AI を使う (cloud chat) | AI と一緒に作る (本セッションのスタイル) |
|---|---|---|
| AI へのインプット | 1 つの質問 | コーパス + memory + CLAUDE.md + 質問 |
| 補完される観点 | LLM 訓練データの平均的な観点 | プロジェクト固有のコーパスに紐付いた観点 |
| 多視点の自動性 | 限定的 | 高い (auto-trigger 設計あり) |
| 過去の決定の参照 | 不可 | 可 (memory 経由) |
| プロジェクト固有の癖 | 反映不可 | 反映可 (CLAUDE.md と memory) |

本セッションは後者で進めています。**コーパスを先に整え、規約を設計し、memory を蓄積する** ことで、AI が思考フローの自動補完エンジンとして機能します。

## llive 文脈での意義 — CREAT (Creative Thinking Layer)

この気づきは llive の **CREAT** 設計動機を強化します:

- CREAT-01 KJ法ノード — 視野狭窄を防ぐため拡散 ≥20 件強制
- CREAT-02 MindMap — 思考の浅さを防ぐため DFS depth=3
- CREAT-04 Six Hats — 偏った楽観を防ぐため 6 観点強制
- CREAT-05 Synectics — 既存パターン依存を防ぐため異分野類比強制

llive ユーザーは **CREAT を使うだけで** 「自分が意識しない観点」を補完される。これは「AI 開発の優位性」をユーザーにも提供する設計です。

つまり llive は:

![llive の 2 フェーズ図: Phase 1 開発者がコーパスで多視点補完、Phase 2 エンドユーザーが CREAT で同じ優位を獲得](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q13/llive_two_phase.svg)

llive 自体が「コーパス先行戦略の優位性」をユーザーに伝播する仕組みです。

## 翌日以降の運用への示唆

### コーパス品質 = AI 思考品質

- raptor RAD 49 分野は維持・拡張
- hacker_corpus / Exploit-DB / ATT&CK / NVD / Phrack 等の高品質ソースを継続追加
- corpus2skill v2 で要約品質を上げる

### auto-trigger を maximize

- `rad-research` / `triz-ideation` / `cross-domain-ideation` を遠慮なく発火
- 「広く呼ばれるべき補助資料スキル」として CLAUDE.md に明記済

### memory を蓄積し続ける

- セッション内で得た教訓を即 memory 化
- 「ユーザーが意識していない観点」のうち、特に効いたものを記録
- 翌日以降のセッションで再利用

## まとめ — AI 協働開発で効いた 3 つの観察

本日得た気づきから、現時点で言えそうな 3 つの観察:

1. **コーパスの質が出力の質を左右する** — AI 単体ではなく、AI + コーパス + 規約 + memory のセットで効く
2. **意識下にない観点にこそ価値がありそうだ** — ユーザーが気づかない観点を AI が背景で補完してくれる
3. **1 人開発でも複数視点を得られる** — Six Hats / Role-based agents の自動適用で、1 人でも複数視点が混ざる

この 3 つは llive の CREAT 要件群を通じて、エンドユーザーにも届けることを狙っています。

## 残った問い — 補完された観点は、誰がいつ「見る」のか

ここまでは「AI が背景で観点を補完してくれる」という、人間にとって嬉しい話だった。だが裏を返せば、補完された観点 (consensus / risk / 補完路線) は **人間の目には見えない場所** で動いている。出力の最終形だけを見ると、AI がどの観点を背景で参照し、どう判断したのかは表に出てこない。これは協働の利点であると同時に、来歴 (provenance) が霧の中に消えるという弱点でもある。

では、AI が背景で混ぜ込んだ観点を、人間には邪魔にならず・機械には確実に読める形で **どこに刻んでおく** べきか? 出力に痕跡を残せなければ、「なぜこの設計になったのか」は次のセッションで再び意識下に沈む。

次回 **#14「[HTML では見えないのに、機械では読める — 不可視アノテーションチャネル設計](./QIITA_#14_invisible_annotation_channel.md)」** で、その「見えない来歴をどこに置くか」の答えを一つ示す。背景で補完された観点を、人間の読みを妨げずに残す——コーパス先行で得た多視点を、流れ去らせずに固定する側の話だ。

## ソース

- memory: `project_corpus_first_advantage.md` (本日新規)
- 関連 memory: `project_llive_cog_fx_factors` / `project_corpus_overnight_2026_05_12` / `project_hacker_corpus`
- llive 要件: `REQUIREMENTS.md` v0.9 CREAT (CREAT-01〜05)
- raptor CLAUDE.md: AUTOMATIC SKILL ACTIVATION セクション

## 同日記事

- [QIITA_SUMMARY](./QIITA_SUMMARY.md) — 技術者向け統合
- [QIITA_GENERAL](./QIITA_GENERAL.md) — 非エンジニア向け統合
- [QIITA_HISTORY](./QIITA_HISTORY.md) — 3 製品履歴 + 設計 + 差別化 + 普及
- [12_dev_history](./12_dev_history.md) — llive 単独開発履歴
- LinkedIn 多言語版 (SUMMARY / GENERAL / HISTORY × jp/en/zh/ko)

---

> AI と一緒に作る = AI が背景でコーパス参照 + 多視点を補完しながら、設計判断は人間が行う。本セッションは 1 日で要件 32 件 + 1014 PASS + 14 記事という規模を実現。

---

# English

# Corpus-First Strategy — The Advantage of AI Completing My Thought Flow With Perspectives I Never Noticed

Author: **Kazufumi Furuse (Puruyan)**

> 📚 **Series nav**: ← #12 [llive development history (from v0.1 to a v0.7 candidate in 5 days)](./QIITA_#12_dev_history.md) ｜ **#13 This article** (why those 5 days were possible — the corpus-first collaboration structure) ｜ #14 [The invisible annotation channel: unreadable in HTML, but readable by machines](./QIITA_#14_invisible_annotation_channel.md) →. ※ Each article stands on its own.
>
> In #12 we laid out the **development history** in chronological order — "from v0.1 to a v0.7 candidate in 5 days." This article digs into what was behind it: why that speed and that breadth of perspective were possible for a solo developer — the **structure of the collaboration** itself.

## TL;DR

- Something I realized over today's session about **where AI-collaborative development actually pays off** (at least within what I observed on my own machine)
- By **enriching the corpus first**, the AI references that corpus in the background while doing new implementation or requirements definition
- Perspectives the user is not consciously aware of (Six Hats / TRIZ / KJ Method / MindMap / cross-domain analogy) are **automatically mixed into the thought flow**
- A structure where even a solo developer gets multiple cognitive viewpoints in the background
- This is the essential fork in the road between **"using AI" vs. "building together with AI"**

## The Moment of Realization

Today's session (2026-05-17) moved at a scale of 32 requirements added + 2,200 lines of program + 78 tests + 14 articles, all in a single day.

While looking back on it, a realization struck me:

> "I don't recall consciously using the KJ Method / MindMap / Six Hats / TRIZ, and yet somehow these perspectives are **naturally mixed in** to the requirements and design decisions that come out."

For example, when I (the human) say "I want to move away from Qwen," the AI organizes and brings up the following on its own, in the background:

- **Staged decomposition of Stage A→B→C→D→E** (TRIZ Principle 7: Nested doll, staged expansion)
- **Threshold for the GPU investment decision** (Six Hats: cautious perspective)
- **Evaluation metrics AOS / LCIR** (Six Hats: process perspective)
- **"Run a complementary track in parallel too"** (Synectics: resolving a binary opposition)

These are not things I "consciously" asked the AI for — they are perspectives the **AI completed on its own while referencing the corpus in the background**.

## Why Does This Happen?

### The Structure

![Structure of the corpus-first strategy: user input -> AI references the corpus in the background -> output completed with multiple perspectives](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q13/flow_structure_en.svg)

The user only entered the single line "I want to move away from Qwen." The **"areas conceded as a tie,"** the **"risk table,"** and the **"complementary track"** included in the output are perspectives the user was not consciously aware of.

### The Role of the Corpus

A standalone AI (Claude / GPT / Gemini) naturally possesses knowledge of "Six Hats," "TRIZ," and the "KJ Method." But the judgment of **in which situation to apply them** is decided by the corpus and the CLAUDE.md conventions:

```yaml
# Excerpt from CLAUDE.md (raptor)
AUTOMATIC SKILL ACTIVATION:
  rad-research を自動起動: 新機能・新設計の着手前 (無条件)
  triz-ideation を自動起動: 矛盾・トレードオフ・両立できない
  cross-domain-ideation を自動起動: 異分野・他分野・分野を超えて
```

In other words, the **corpus + conventions** function as the "auto-completion engine" of the AI's thought flow.

## A Concrete Example — From Today's Session

The inputs the user was consciously aware of vs. the perspectives the AI completed in the background:

| What the user was consciously aware of | Perspectives the AI completed in the background |
|---|---|
| "I want to build something around the LLM" | TRIZ 40 Principles / 39×39 Contradiction Matrix / Mediator pattern / Provenance DDD |
| "I want to take a benchmark" | Honest disclosure / xs/s/m/l/xl 5-step ladder / mean/stdev statistics |
| "I want to move away from Qwen" | Stage A→E staged decomposition / GPU investment decision / evaluation metrics (AOS / LCIR) |
| "Specialize in math and units" | SI 7 base units / CODATA 2022 / Buckingham π / IEEE 754 |
| "Introduce thinking factors" | Cognitive Factor Framework / Role-based agents (architect/critic/executor/auditor) |

The core of this strategy is precisely that **"the AI selects these perspectives before the user even becomes consciously aware of them."**

## Why Didn't I Notice?

In their own field of expertise, humans use "perspectives they ought to know" unconsciously, as a matter of course. However:

- Perspectives outside one's expertise (e.g., legal matters for a physicist, marketing for an engineer)
- Related but distant perspectives (e.g., cognitive psychology for an LLM developer)
- Perspectives learned in the past but now forgotten (e.g., Six Hats learned in undergraduate days)

Because these **never rise into consciousness**, you cannot complete them on your own. The AI pulling these up via the corpus is the one place where, on my own machine, collaborative development feels like it is working.

## The Difference Between "Using AI" vs. "Building Together With AI"

| Item | Using AI (cloud chat) | Building together with AI (this session's style) |
|---|---|---|
| Input to the AI | A single question | Corpus + memory + CLAUDE.md + question |
| Perspectives completed | The average perspective of the LLM's training data | Perspectives tied to the project-specific corpus |
| Automaticity of multiple viewpoints | Limited | High (auto-trigger design exists) |
| Reference to past decisions | Not possible | Possible (via memory) |
| Project-specific quirks | Cannot be reflected | Can be reflected (CLAUDE.md and memory) |

This session proceeds in the latter mode. By **arranging the corpus first, designing the conventions, and accumulating memory**, the AI functions as an auto-completion engine for the thought flow.

## Significance in the llive Context — CREAT (Creative Thinking Layer)

This realization reinforces llive's **CREAT** design motivation:

- CREAT-01 KJ Method node — forces divergence ≥20 items to prevent tunnel vision
- CREAT-02 MindMap — DFS depth=3 to prevent shallowness of thought
- CREAT-04 Six Hats — forces 6 perspectives to prevent biased optimism
- CREAT-05 Synectics — forces cross-domain analogy to prevent dependence on existing patterns

llive users get "perspectives they are not consciously aware of" completed for them **just by using CREAT**. This is a design that provides the "advantage of AI development" to the user as well.

In other words, llive is:

![Two-phase diagram of llive: Phase 1 developer gets multiple viewpoints from the corpus, Phase 2 end user gets the same advantage via CREAT](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q13/llive_two_phase_en.svg)

llive itself is a mechanism that propagates "the advantage of the corpus-first strategy" to the user.

## Implications for Operations From the Next Day Onward

### Corpus Quality = AI Thinking Quality

- Maintain and expand raptor RAD's 49 fields
- Continue adding high-quality sources such as hacker_corpus / Exploit-DB / ATT&CK / NVD / Phrack
- Raise summarization quality with corpus2skill v2

### Maximize auto-trigger

- Fire `rad-research` / `triz-ideation` / `cross-domain-ideation` without hesitation
- Already documented in CLAUDE.md as "auxiliary reference skills that should be called broadly"

### Keep Accumulating memory

- Turn lessons gained within a session into memory immediately
- Record, among the "perspectives the user is not consciously aware of," the ones that were especially effective
- Reuse them in sessions from the next day onward

## Summary — 3 Observations on Where AI-Collaborative Development Pays Off

Three observations that seem safe to make at this point, from what I noticed today:

1. **Corpus quality tends to drive output quality** — It works as a set: AI + corpus + conventions + memory, not the AI alone
2. **The perspectives not in your consciousness may be exactly the valuable ones** — The AI completes, in the background, the perspectives the user does not notice
3. **Even a solo developer can get multiple viewpoints** — Through automatic application of Six Hats / Role-based agents, multiple viewpoints get mixed in even for one person

We aim to deliver all three to the end user as well, through llive's CREAT requirement group.

## The Question That Remains — Who Sees the Completed Perspectives, and When?

So far this has been a happy story for the human: the AI completes perspectives in the background. But the flip side is that those completed perspectives (consensus / risk / complementary track) operate in a place **invisible to human eyes**. Looking only at the final output, you cannot tell which perspectives the AI referenced in the background or how it judged. That is at once the benefit of the collaboration and its weakness — the provenance vanishes into the fog.

So where should we **inscribe** the perspectives the AI mixed in behind the scenes, in a form that does not get in the human's way yet is reliably readable by machines? If we leave no trace in the output, "why this design?" sinks back below consciousness in the next session.

In the next article, **#14 "[Invisible in HTML, but readable by machines — the invisible annotation channel design](./QIITA_#14_invisible_annotation_channel.md)"**, I offer one answer to "where to put that invisible provenance." Leaving the perspectives completed in the background without obstructing the human's reading — this is the other side: how to pin down, rather than let drift away, the multiple viewpoints that the corpus-first strategy gave us.

## Sources

- memory: `project_corpus_first_advantage.md` (newly added today)
- Related memory: `project_llive_cog_fx_factors` / `project_corpus_overnight_2026_05_12` / `project_hacker_corpus`
- llive requirements: `REQUIREMENTS.md` v0.9 CREAT (CREAT-01 to 05)
- raptor CLAUDE.md: AUTOMATIC SKILL ACTIVATION section

## Same-Day Articles

- [QIITA_SUMMARY](./QIITA_SUMMARY.md) — Integrated, for engineers
- [QIITA_GENERAL](./QIITA_GENERAL.md) — Integrated, for non-engineers
- [QIITA_HISTORY](./QIITA_HISTORY.md) — 3-product history + design + differentiation + adoption
- [12_dev_history](./12_dev_history.md) — llive standalone development history
- LinkedIn multilingual editions (SUMMARY / GENERAL / HISTORY × jp/en/zh/ko)

---

> Building together with AI = the AI references the corpus in the background and completes multiple viewpoints, while the human makes the design decisions. This session achieved a scale of 32 requirements + 1014 PASS + 14 articles in a single day.

---

# 中文

# 语料库先行策略 —— AI 在思考流程中补全我未曾察觉的视角的优势

作者: **古濑 和文（Puruyan）**

> 📚 **连载导航**: ← #12 [llive 开发历程（5 天内从 v0.1 到 v0.7 候选）](./QIITA_#12_dev_history.md) ｜ **#13 本文**（为何 5 天能推进 = 语料库先行这一协作结构）｜ #14 [HTML 中看不见、机器却能读取的不可见注释通道](./QIITA_#14_invisible_annotation_channel.md) →。※ 各文均可单独阅读。
>
> #12 以时间顺序排列了「5 天内从 v0.1 到 v0.7 候选」这段 **开发历程**。本文挖掘其背后——单人开发为何能成立这样的速度与多视角，也就是这套 **协作的结构** 本身。

## TL;DR

- 通过今天的整场会话所领悟到的 **AI 协作开发的发力之处**（至少是笔者在自己机器上观察到的范围）
- 通过 **首先充实语料库**，AI 在进行新实现、需求定义时会在后台参照该语料库
- 用户未曾有意识察觉的视角（Six Hats / TRIZ / KJ 法 / MindMap / 跨领域类比）会 **自动混入思考流程**
- 即使是单人开发，也能在后台获得多种认知视角的结构
- 这是 **「使用 AI」与「与 AI 一起创作」** 的本质性分岔点

## 领悟的瞬间

今天（2026-05-17）的会话以一天内追加需求 32 件 + 程序 2200 行 + 测试 78 件 + 文章 14 篇的规模推进。

在回顾过程中，我有了一个领悟:

> 「我并不记得自己有意识地使用过 KJ 法 / MindMap / Six Hats / TRIZ，然而不知为何，产出的需求和设计判断中却 **自然地混入了** 这些视角。」

例如，当我（人类）说「想从 Qwen 撤离」时，AI 会在后台擅自整理并提出以下内容:

- **Stage A→B→C→D→E 的分阶段分解**（TRIZ 原理 7: Nested doll、阶段性扩展）
- **GPU 投资判断的阈值**（Six Hats: cautious 视角）
- **评估指标 AOS / LCIR**（Six Hats: process 视角）
- **「补充路线也并行推进」**（Synectics: 二元对立的消解）

这些并非我「有意识地」请求 AI 去做的，而是 **AI 在后台一边参照语料库一边擅自补全的** 视角。

## 为何会发生这种情况

### 结构

![语料库先行策略的结构图: 用户输入 → AI 在后台参照语料库 → 补全多视角的输出](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q13/flow_structure_zh.svg)

用户只输入了「想从 Qwen 撤离」这一行。输出中包含的 **「承认打平的领域」**、**「风险表」**、**「补充路线」**，都是用户未曾有意识察觉的视角。

### 语料库的角色

AI 本体（Claude / GPT / Gemini）当然拥有「Six Hats」「TRIZ」「KJ 法」的知识。但是，**应在何种场景下应用** 的判断，则由语料库和 CLAUDE.md 的规约来决定:

```yaml
# CLAUDE.md (raptor) より抜粋
AUTOMATIC SKILL ACTIVATION:
  rad-research を自動起動: 新機能・新設計の着手前 (無条件)
  triz-ideation を自動起動: 矛盾・トレードオフ・両立できない
  cross-domain-ideation を自動起動: 異分野・他分野・分野を超えて
```

也就是说，**语料库 + 规约** 作为 AI 思考流程的「自动补全引擎」在发挥作用。

## 实例 —— 来自今天的会话

用户有意识的输入 vs AI 在后台补全的视角:

| 用户有意识到的事情 | AI 在后台补全的视角 |
|---|---|
| 「想在 LLM 周围做点什么」 | TRIZ 40 原理 / 39×39 矛盾矩阵 / Mediator 模式 / Provenance DDD |
| 「想跑个基准测试」 | Honest disclosure / xs/s/m/l/xl 5 级阶梯 / mean/stdev 统计 |
| 「想从 Qwen 撤离」 | Stage A→E 分阶段分解 / GPU 投资判断 / 评估指标 (AOS / LCIR) |
| 「专精数学・单位」 | SI 7 基本单位 / CODATA 2022 / Buckingham π / IEEE 754 |
| 「引入思考因子」 | Cognitive Factor Framework / Role-based agents (architect/critic/executor/auditor) |

**「在用户意识到之前，AI 就把这些视角 selection 出来」**，正是本策略的核心。

## 为何当时没有察觉

人类在自己的专业领域中，会理所当然地、无意识地使用「本应知道的视角」。然而:

- 专业之外的视角（例如: 对物理学家而言的法务、对工程师而言的市场营销）
- 相关但距离较远的视角（例如: 对 LLM 开发者而言的认知心理学）
- 过去学过但已遗忘的视角（例如: 本科时代学过的 Six Hats）

由于这些 **无法浮现到意识层面**，自己便无法补全。AI 经由语料库把这些拉取出来——这正是笔者在自己机器上感到协作开发奏效的一处。

## 「使用 AI」与「与 AI 一起创作」的区别

| 项目 | 使用 AI (cloud chat) | 与 AI 一起创作 (本会话的风格) |
|---|---|---|
| 向 AI 的输入 | 一个问题 | 语料库 + memory + CLAUDE.md + 问题 |
| 被补全的视角 | LLM 训练数据的平均视角 | 与项目特有语料库绑定的视角 |
| 多视角的自动性 | 有限 | 高 (有 auto-trigger 设计) |
| 对过去决定的参照 | 不可 | 可 (经由 memory) |
| 项目特有的习性 | 无法反映 | 可反映 (CLAUDE.md 与 memory) |

本会话以后者推进。通过 **先整理好语料库、设计规约、积累 memory**，AI 便能作为思考流程的自动补全引擎运作。

## 在 llive 语境中的意义 —— CREAT (Creative Thinking Layer)

这一领悟强化了 llive 的 **CREAT** 设计动机:

- CREAT-01 KJ 法节点 —— 为防止视野狭窄，强制发散 ≥20 件
- CREAT-02 MindMap —— 为防止思考浅薄，DFS depth=3
- CREAT-04 Six Hats —— 为防止偏颇的乐观，强制 6 视角
- CREAT-05 Synectics —— 为防止依赖既有模式，强制跨领域类比

llive 用户 **只需使用 CREAT**，便能被补全「自己未曾意识的视角」。这是把「AI 开发的优势」也提供给用户的设计。

也就是说，llive 是:

![llive 的两阶段图: Phase 1 开发者通过语料库补全多视角, Phase 2 终端用户通过 CREAT 获得同样的优势](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q13/llive_two_phase_zh.svg)

llive 本身就是把「语料库先行策略的优势」传播给用户的机制。

## 对次日及之后运营的启示

### 语料库质量 = AI 思考质量

- 维护并扩展 raptor RAD 49 领域
- 持续追加 hacker_corpus / Exploit-DB / ATT&CK / NVD / Phrack 等高质量来源
- 用 corpus2skill v2 提升摘要质量

### 最大化 auto-trigger

- 毫不犹豫地触发 `rad-research` / `triz-ideation` / `cross-domain-ideation`
- 已在 CLAUDE.md 中明确写为「应被广泛调用的辅助资料 skill」

### 持续积累 memory

- 把会话内获得的教训立即转化为 memory
- 在「用户未曾意识的视角」中，记录尤其有效的那些
- 在次日及之后的会话中重复利用

## 总结 —— AI 协作开发发力之处的 3 点观察

从今天获得的领悟，目前能说的 3 点观察:

1. **语料库的质量会左右输出的质量** —— 不是 AI 本体，而是 AI + 语料库 + 规约 + memory 的整套在起作用
2. **不在意识层面的视角，或许才是价值所在** —— AI 在后台补全用户未察觉的视角
3. **单人开发也能获得多视角** —— 通过 Six Hats / Role-based agents 的自动应用，单人也能混入多视角

我们希望这 3 点也经由 llive 的 CREAT 需求群，送达终端用户。

## 残留的问题 —— 被补全的视角，由谁、在何时「看见」

至此都是对人类而言令人欣喜的故事: AI 在后台补全视角。但反过来说，被补全的视角（consensus / risk / 补充路线）运行在 **人眼看不见的地方**。只看输出的最终形态，无法得知 AI 在后台参照了哪些视角、又是如何判断的。这既是协作的优点，也是其弱点——来历（provenance）消散于雾中。

那么，AI 在后台混入的视角，应当以「不妨碍人类阅读、机器却能确实读取」的形式 **刻在何处**? 若在输出里不留痕迹，「为何会是这个设计」便会在下一场会话里再次沉入意识之下。

下一篇 **#14「[HTML 中看不见、机器却能读取 —— 不可见注释通道设计](./QIITA_#14_invisible_annotation_channel.md)」** 将给出「把这看不见的来历放在哪里」的一个答案。把后台补全的视角，以不妨碍人类阅读的方式留存下来——这是另一面的话题: 如何把语料库先行所得的多视角固定下来，而非任其流走。

## 来源

- memory: `project_corpus_first_advantage.md` (本日新增)
- 相关 memory: `project_llive_cog_fx_factors` / `project_corpus_overnight_2026_05_12` / `project_hacker_corpus`
- llive 需求: `REQUIREMENTS.md` v0.9 CREAT (CREAT-01〜05)
- raptor CLAUDE.md: AUTOMATIC SKILL ACTIVATION 章节

## 同日文章

- [QIITA_SUMMARY](./QIITA_SUMMARY.md) —— 面向技术人员的整合
- [QIITA_GENERAL](./QIITA_GENERAL.md) —— 面向非工程师的整合
- [QIITA_HISTORY](./QIITA_HISTORY.md) —— 3 产品历史 + 设计 + 差异化 + 普及
- [12_dev_history](./12_dev_history.md) —— llive 单独开发历史
- LinkedIn 多语言版 (SUMMARY / GENERAL / HISTORY × jp/en/zh/ko)

---

> 与 AI 一起创作 = AI 在后台参照语料库 + 补全多视角，而设计判断由人类来做。本会话在一天内实现了需求 32 件 + 1014 PASS + 14 篇文章的规模。

---

# 한국어

# 코퍼스 선행 전략 — AI가 내가 알아차리지 못한 관점을 사고 흐름에 보완해 주는 우위

저자: **후루세 가즈후미（Puruyan）**

> 📚 **연재 내비**: ← #12 [llive 개발 이력（5일 만에 v0.1에서 v0.7 후보로）](./QIITA_#12_dev_history.md) ｜ **#13 본 기사**（왜 5일 만에 진행할 수 있었는가 = 코퍼스 선행이라는 협업 구조）｜ #14 [HTML에서는 보이지 않지만 기계는 읽을 수 있는 불가시 어노테이션 채널](./QIITA_#14_invisible_annotation_channel.md) →. ※ 각 기사는 단독으로도 읽을 수 있습니다.
>
> #12에서는 「5일 만에 v0.1에서 v0.7 후보로」라는 **개발 이력** 을 시계열로 늘어놓았다. 본 기사는 그 이면——1인 개발에서 이 속도와 다시점이 어떻게 성립했는가, 그 **협업의 구조** 자체를 파고든다.

## TL;DR

- 오늘 세션 전체를 통해 깨달은 **AI 협업 개발이 효과를 내는 지점**（적어도 필자의 손끝에서 관찰된 범위）
- **먼저 코퍼스를 충실하게** 함으로써, AI가 신규 구현·요건 정의 시 백그라운드에서 코퍼스를 참조
- 사용자가 의식하지 못한 관점（Six Hats / TRIZ / KJ법 / MindMap / 이종 분야 유추）이 **자동으로 사고 흐름에 섞여 들어옴**
- 1인 개발이라도 여러 인지 시점을 백그라운드에서 얻을 수 있는 구조
- 이것은 **「AI를 쓴다」 vs 「AI와 함께 만든다」** 의 본질적인 갈림길

## 깨달음의 순간

오늘（2026-05-17）의 세션은 하루에 요건 32건 추가 + 프로그램 2200줄 + 테스트 78건 + 기사 14편이라는 규모로 진행되었습니다.

그 회고 중에 한 가지 깨달음이 있었습니다:

> 「내가 KJ법 / MindMap / Six Hats / TRIZ를 의식적으로 사용한 기억은 없는데, 어째서인지 나오는 요건이나 설계 판단에 이러한 관점들이 **자연스럽게 섞여 있다**」

예를 들어, 내가（인간이）「Qwen에서 벗어나고 싶다」고 말하면, AI는 백그라운드에서 다음을 알아서 정리해 꺼내 옵니다:

- **Stage A→B→C→D→E의 단계 분해**（TRIZ 원리 7: Nested doll, 단계적 확장）
- **GPU 투자 판단의 임계값**（Six Hats: cautious 관점）
- **평가 지표 AOS / LCIR**（Six Hats: process 관점）
- **「보완 노선도 병행」**（Synectics: 이항 대립의 해소）

이것들은 내가 「의식해서」 AI에게 부탁한 것이 아니라, **AI가 백그라운드에서 코퍼스를 참조하면서 알아서 보완해 온** 관점입니다.

## 왜 이런 일이 일어나는가

### 구조

![코퍼스 선행 전략의 구조도: 사용자 입력 → AI가 백그라운드에서 코퍼스 참조 → 다시점을 보완한 출력](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q13/flow_structure_ko.svg)

사용자는 「Qwen에서 벗어나고 싶다」라는 한 줄을 입력했을 뿐. 출력에 포함된 **「동점으로 인정하는 영역」**, **「리스크 표」**, **「보완 노선」** 은 사용자가 의식하지 못한 관점입니다.

### 코퍼스의 역할

AI 단독（Claude / GPT / Gemini）은 당연히 「Six Hats」「TRIZ」「KJ법」의 지식을 가지고 있습니다. 그러나 그것을 **어느 장면에서 적용해야 하는가** 의 판단은, 코퍼스와 CLAUDE.md의 규약이 결정합니다:

```yaml
# CLAUDE.md (raptor) より抜粋
AUTOMATIC SKILL ACTIVATION:
  rad-research を自動起動: 新機能・新設計の着手前 (無条件)
  triz-ideation を自動起動: 矛盾・トレードオフ・両立できない
  cross-domain-ideation を自動起動: 異分野・他分野・分野を超えて
```

즉, **코퍼스 + 규약** 이 AI 사고 흐름의 「자동 보완 엔진」으로서 기능하고 있습니다.

## 실례 — 오늘 세션에서

사용자가 의식하고 있던 입력 vs AI가 백그라운드에서 보완한 관점:

| 사용자가 의식하고 있던 것 | AI가 백그라운드에서 보완한 관점 |
|---|---|
| 「LLM 주변에 뭔가 만들고 싶다」 | TRIZ 40 원리 / 39×39 모순 매트릭스 / Mediator 패턴 / Provenance DDD |
| 「벤치마크를 측정하고 싶다」 | Honest disclosure / xs/s/m/l/xl 5단 사다리 / mean/stdev 통계 |
| 「Qwen에서 벗어나고 싶다」 | Stage A→E 단계 분해 / GPU 투자 판단 / 평가 지표 (AOS / LCIR) |
| 「수학・단위 특화」 | SI 7 기본 단위 / CODATA 2022 / Buckingham π / IEEE 754 |
| 「사고 인자를 도입」 | Cognitive Factor Framework / Role-based agents (architect/critic/executor/auditor) |

이러한 관점을 **「사용자가 의식하기 전에 AI가 selection 해 온다」** 는 것이 본 전략의 핵심입니다.

## 왜 알아차리지 못했는가

인간은, 자신의 전문 분야에서는 「알고 있을 법한 관점」을 당연한 것으로 무의식적으로 사용합니다. 그러나:

- 전문 외의 관점（예: 물리학자에게의 법무, 엔지니어에게의 마케팅）
- 관련 분야이지만 거리가 있는 관점（예: LLM 개발자에게의 인지심리학）
- 과거에 배웠지만 잊고 있는 관점（예: 학부 시절에 배운 Six Hats）

이것들은 **의식 위로 떠오르지 않기** 때문에, 스스로는 보완할 수 없습니다. AI가 코퍼스를 경유해 이것들을 끌어와 주는 것——여기가 필자의 손끝에서 협업 개발이 효과를 내고 있다고 느끼는 한 지점입니다.

## 「AI를 쓴다」 vs 「AI와 함께 만든다」의 차이

| 항목 | AI를 쓴다 (cloud chat) | AI와 함께 만든다 (본 세션의 스타일) |
|---|---|---|
| AI에의 입력 | 하나의 질문 | 코퍼스 + memory + CLAUDE.md + 질문 |
| 보완되는 관점 | LLM 학습 데이터의 평균적인 관점 | 프로젝트 고유의 코퍼스에 연결된 관점 |
| 다시점의 자동성 | 한정적 | 높음 (auto-trigger 설계 있음) |
| 과거 결정의 참조 | 불가 | 가능 (memory 경유) |
| 프로젝트 고유의 버릇 | 반영 불가 | 반영 가능 (CLAUDE.md와 memory) |

본 세션은 후자로 진행하고 있습니다. **코퍼스를 먼저 정비하고, 규약을 설계하고, memory를 축적함** 으로써, AI가 사고 흐름의 자동 보완 엔진으로서 기능합니다.

## llive 맥락에서의 의의 — CREAT (Creative Thinking Layer)

이 깨달음은 llive의 **CREAT** 설계 동기를 강화합니다:

- CREAT-01 KJ법 노드 — 시야 협착을 방지하기 위해 발산 ≥20건 강제
- CREAT-02 MindMap — 사고의 얕음을 방지하기 위해 DFS depth=3
- CREAT-04 Six Hats — 편향된 낙관을 방지하기 위해 6관점 강제
- CREAT-05 Synectics — 기존 패턴 의존을 방지하기 위해 이종 분야 유추 강제

llive 사용자는 **CREAT를 쓰기만 하면** 「자신이 의식하지 못한 관점」을 보완받습니다. 이것은 「AI 개발의 우위」를 사용자에게도 제공하는 설계입니다.

즉 llive는:

![llive의 2 페이즈 도식: Phase 1 개발자가 코퍼스로 다시점 보완, Phase 2 엔드유저가 CREAT로 같은 우위를 획득](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q13/llive_two_phase_ko.svg)

llive 자체가 「코퍼스 선행 전략의 우위」를 사용자에게 전파하는 구조입니다.

## 다음 날 이후의 운용에 대한 시사점

### 코퍼스 품질 = AI 사고 품질

- raptor RAD 49 분야는 유지·확장
- hacker_corpus / Exploit-DB / ATT&CK / NVD / Phrack 등의 고품질 소스를 계속 추가
- corpus2skill v2로 요약 품질을 높임

### auto-trigger를 maximize

- `rad-research` / `triz-ideation` / `cross-domain-ideation` 을 거리낌 없이 발화
- 「폭넓게 호출되어야 할 보조 자료 skill」로서 CLAUDE.md에 명기 완료

### memory를 계속 축적

- 세션 내에서 얻은 교훈을 즉시 memory화
- 「사용자가 의식하지 못한 관점」 중, 특히 효과적이었던 것을 기록
- 다음 날 이후의 세션에서 재이용

## 정리 — AI 협업 개발이 효과를 낸 3가지 관찰

오늘 얻은 깨달음에서, 현시점에 말할 수 있을 듯한 3가지 관찰:

1. **코퍼스의 질이 출력의 질을 좌우한다** — AI 단독이 아니라, AI + 코퍼스 + 규약 + memory의 세트로 효과가 난다
2. **의식 아래에 없는 관점에야말로 가치가 있어 보인다** — 사용자가 알아차리지 못한 관점을 AI가 백그라운드에서 보완해 준다
3. **1인 개발이라도 복수 시점을 얻을 수 있다** — Six Hats / Role-based agents의 자동 적용으로, 1인이라도 복수 시점이 섞인다

이 3가지를 llive의 CREAT 요건군을 통해, 엔드유저에게도 전하는 것을 노리고 있습니다.

## 남은 물음 — 보완된 관점은, 누가 언제 「본다」는 것인가

여기까지는 「AI가 백그라운드에서 관점을 보완해 준다」는, 인간에게 반가운 이야기였다. 그러나 뒤집어 보면, 보완된 관점（consensus / risk / 보완 노선）은 **인간의 눈에는 보이지 않는 곳** 에서 움직이고 있다. 출력의 최종 형태만 보면, AI가 어떤 관점을 백그라운드에서 참조하고 어떻게 판단했는지는 겉으로 드러나지 않는다. 이는 협업의 이점인 동시에, 내력（provenance）이 안갯속으로 사라진다는 약점이기도 하다.

그렇다면, AI가 백그라운드에서 섞어 넣은 관점을, 인간의 읽기를 방해하지 않으면서 기계는 확실히 읽을 수 있는 형태로 **어디에 새겨 두어야** 하는가? 출력에 흔적을 남기지 못하면, 「왜 이 설계가 되었는가」는 다음 세션에서 다시 의식 아래로 가라앉는다.

다음 편 **#14「[HTML에서는 보이지 않는데 기계는 읽을 수 있다 — 불가시 어노테이션 채널 설계](./QIITA_#14_invisible_annotation_channel.md)」** 에서, 그 「보이지 않는 내력을 어디에 둘 것인가」에 대한 하나의 답을 제시한다. 백그라운드에서 보완된 관점을, 인간의 읽기를 방해하지 않고 남긴다——코퍼스 선행으로 얻은 다시점을, 흘려보내지 않고 고정하는 쪽의 이야기다.

## 소스

- memory: `project_corpus_first_advantage.md` (본일 신규)
- 관련 memory: `project_llive_cog_fx_factors` / `project_corpus_overnight_2026_05_12` / `project_hacker_corpus`
- llive 요건: `REQUIREMENTS.md` v0.9 CREAT (CREAT-01〜05)
- raptor CLAUDE.md: AUTOMATIC SKILL ACTIVATION 섹션

## 같은 날 기사

- [QIITA_SUMMARY](./QIITA_SUMMARY.md) — 기술자 대상 통합
- [QIITA_GENERAL](./QIITA_GENERAL.md) — 비엔지니어 대상 통합
- [QIITA_HISTORY](./QIITA_HISTORY.md) — 3 제품 이력 + 설계 + 차별화 + 보급
- [12_dev_history](./12_dev_history.md) — llive 단독 개발 이력
- LinkedIn 다국어판 (SUMMARY / GENERAL / HISTORY × jp/en/zh/ko)

---

> AI와 함께 만든다 = AI가 백그라운드에서 코퍼스 참조 + 다시점을 보완하면서, 설계 판단은 인간이 한다. 본 세션은 하루에 요건 32건 + 1014 PASS + 14 기사라는 규모를 실현.
