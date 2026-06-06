---
title: 30 年のソフトウェア開発経験 + Perplexity 要約 + Claude Code + TRIZ + 5 万件の論文 RAG = 「第二の脳」
tags:
  - FullSense
  - llive
  - 解説
  - TODO_TAG
  - TODO_TAG
private: false
updated_at: '2026-05-22'
id: a30e7f893874d6901dee
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 30 年のソフトウェア開発経験 + Perplexity 要約 + Claude Code + TRIZ + 5 万件の論文 RAG = 「第二の脳」

> 📚 **連載ナビ**: ← #14 不可視アノテーションチャネル設計 ｜ **#15 本記事** ｜ #16 三自の精神で AI 運用 → ｜ [連載 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 各記事は単独でも読めます（リンクは回遊用）。
>
> 前記事 #14 では、人には見えず機械だけが読むアノテーションチャネルを設計した。本記事はそこから一歩下がって、その機能群を 1 人でどう積み上げているのか——開発を支える「第二の脳」を **どう構築するか** を書く。

**1 行 hook**:
1 人開発で 5 日間に Brief API・OKA-FX・VRB-FX・IND-04 アノテーション・MathVerifier を含む 14 機能と 256 テストを追加し、1270 件全 PASS で回帰ゼロを達成した。秘訣は「第二の脳」をどう組み立てるかにある。

---

## 「第二の脳」の定義

筆者 (30 年超のソフトウェア開発者) は llive (FullSense umbrella の中核プロダクト、L は 2 個) を **1 人で開発**しているが、進度はチーム開発に近い。これは次の 5 要素を組み合わせた「第二の脳」を構築したからだ。

| 要素 | 役割 |
|---|---|
| **30 年の開発経験** | 設計品質・判断のベース。アイデア・ノウハウとして毎セッション渡す |
| **Perplexity 要約** | 取り込みたい外部思想 (書籍・論文・YouTube) を高品質に圧縮 |
| **Claude Code (Opus 4.7 / 1M context)** | 実装エージェント |
| **TRIZ ルール (40 原理)** | 矛盾解決のメタ思考フレーム。特許領域での経験から llive 設計へ |
| **論文 RAG コーパス (RAD 49 分野 / 約 5 万件)** | Claude Code が「研究者の知見」で答える土台 |

これらを **スパイラル開発サイクル** に流すと、外部思想が短時間で実装に着地する。

### ☕ ちょっと脱線

「第二の脳」って言葉、最初は気恥ずかしかった。Tiago Forte の同名書籍に引きずられて陳腐に聞こえる気がして。でも 5 日間で 14 機能を 1 人で積み終えた後に振り返ると、これ以上ピッタリの言葉が見つからない。**気恥ずかしさは正確さの前に折れる**。

## スパイラル 1 サイクル

![スパイラル開発 1 サイクルのフロー図 (外部思想 → Perplexity 要約 → Claude Code 読込 → 要件化 → 実装 → ベンチ → commit → 次サイクル)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q15/spiral_cycle.svg)

実際の例 (本セッション 9 回中の 3 例):

| サイクル | 起点 | 結果 |
|---|---|---|
| 1 | **MBA 言語化トレーニング** (グロービス書籍) | Perplexity が 8 機能に整理 → VRB-FX (Verbalization Framework) 4 件要件化 → VRB-02 PromptLint 実装 (1 セッション) |
| 2 | **岡潔先生の数学観に学ばせていただく** (YouTube『心理の深層』講話より) | 先生が遺された「数学は情緒である」「発見の前に一度行き詰まる」「文章を書くことなしには思索を進められない」「国語が数学を育む」という思想を、Perplexity で要約させていただいた上で **設計の 4 観点** として参照 → OKA-FX 10 要件として記述 → OKA-01〜04 minimal proto 実装。**先生のお考えそのものを実装したと主張するものではなく**、こちらの設計が触発を受けた先生の思想への敬意を表して命名している |
| 3 | **LinkedIn フィードバック**「相互依存を避けたい」 | IND-FX 設計原則 + IND-04 Annotation Channel 実装、`<!-- llive:ns.key=val -->` で独立性と組合せ価値を両立 |

各サイクルが **要件 → 実装 → テスト → commit** まで数時間で完走する。

## なぜスパイラルが回るのか

### Perplexity 要約の役割 — 「入力品質ゲート」

外部思想は本・論文・動画・SNS と形式バラバラ。これを Claude Code に直接放り込むと:
- 元情報が膨大で context window を食う
- 重要部分とノイズが混在
- Claude の解釈にゆらぎが出る

Perplexity に「~3000 字に要約」「実装可能な仕様で」「対比表で」と指示すると、**Claude Code が読み取れる質の入力**に変換される。これが「入力品質ゲート」として機能する。

### TRIZ の役割 — 「矛盾解決のメタ思考」

実装中に何度も矛盾が出る。例:
- 「独立性を担保したい」 vs 「組合せで価値を積み上げたい」
- 「rule-based fallback も残したい」 vs 「LLM 品質を測りたい」
- 「監査ログを完全に取りたい」 vs 「実装オーバヘッドを増やしたくない」

これを **TRIZ 矛盾マトリクス** 視点で解くと、両立解が見える。本セッションの解:
- IND-04 Annotation Channel = 「コメント = renderer 不可視 + 機械可読」で両立 (TRIZ 原理 24: 媒介物)
- echo baseline 残置 = 「同じ rule-based 出力を別カテゴリで表示」で両立 (TRIZ 原理 1: 分割)
- bind_ledger() pattern = 「optional 注入で audit はゼロコスト」で両立 (TRIZ 原理 15: 動的化)

### 論文 RAG (RAD 49 分野 ~5 万件) の役割 — 「研究者の知見を借りる」

新機能設計で必要な分野が出るたび、RAG コーパスを引く。本セッション例:
- OKA-FX 設計 → `mathematics` / `formal_methods` / `metrology` を参照
- VRB-FX 設計 → `mba` (management) / `linguistics` を参照
- IND-04 設計 → `software_engineering` / `oss_governance` を参照

Claude Code が「自分の言葉」で書くと一般論になりがちだが、**RAG で具体的な論文・先行研究を引用** すると質が一段上がる。

## 結果 — 5 日間で起きたこと

| Day | 主な追加 |
|---|---|
| 5/13 | llive プロジェクト立ち上げ、Phase 1 完了 |
| 5/14 | F25 連携基盤完了 (llove↔llmesh↔llive MCP 経由) |
| 5/15 | 9 軸 skeleton (KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL) |
| 5/16 | C-1 Approval Bus + Policy + SQLite Ledger 完了 / 815 PASS |
| 5/16 | Brief API end-to-end / progressive matrix 完走 / 998 PASS |
| 5/17 | **9 セッション** で 14 機能 (COG-04, CREAT-04, MATH-02, OKA-01〜07, VRB-02/04/05/06, CREAT-01〜05, IND-FX, MathVerifier-Runner 統合, etc.) / **256 テスト追加** / **1270 PASS / 回帰ゼロ** |

1 人開発でこの速度を出すのは、5 要素が噛み合う「第二の脳」あってこそ。

### ☕ ここまで読んでくれてありがとう

正直、テスト 256 件のうち 7-8 件は途中で 1 回ずつ落ちている。fuzzing で hypothesis が嬉しそうに edge case を見つけてくれるたび、3 秒くらい「うわ」となる。**1270 PASS / 回帰ゼロ** はゴールであって過程ではない。

## 自身の 30 年経験はどこで効くか

「Claude Code 任せ」だと品質は出ない。30 年経験は次の場面で決定的だった。

1. **要件定義の質** — Perplexity 要約を読んで「これは要件 vs 解法を混同している」と即判定し書き直し指示
2. **TRIZ ルールの選定** — 40 原理から「この場面はこの 3 つ」を即抽出 (TRIZ 経験が無いとここで時間を取られる)
3. **アーキテクチャ判断** — Claude が出した実装案を「これは独立性原則に反する」「これは bind_ledger pattern と整合しない」と即拒否
4. **ベンチの honest disclosure** — rule-based の coverage が高く出たときに「これは echo back の偽性能」と即見抜く (測定経験)
5. **タイポチェック** — 「llive が lllive になってる、tokenizer 問題の再発」と即特定 (パターン認識)

つまり **第二の脳 = Claude Code + RAG + Perplexity + TRIZ** に対し、**第一の脳 = 自身の経験** が判断ゲートとして居続ける。両者の合成が「1 人 + 第二の脳 = チーム」を成立させている。

## 他の開発者への示唆

この「第二の脳」を構築するコスト:
- Claude Code 課金 (Max plan 推奨、context 1M 必須)
- Perplexity Pro (月 $20)
- RAG コーパス構築 (Raptor 等 OSS ツールで自前、本 case は ~5 万件 / 49 分野)
- TRIZ 学習 (書籍数冊 + 実践)
- **何より自身の経験を Claude Code に渡し続ける覚悟**

最後の項目が一番重要。Claude Code に丸投げしては、ありきたりな実装しか出ない。**経験者がレビュアー + アーキテクトとして居続ける** ことで、「研究者チーム + 30 年経験 + 実装エージェント」の合成が成立する。

llive は現時点で Apache 2.0 + Commercial dual-license の OSS、Repo は https://github.com/furuse-kazufumi/llive 。本記事の「第二の脳」型開発スタイルに興味のある方は、Issue / Discussion で議論したい。

### だが「組み立てた」だけでは止まる

ここまでは「第二の脳をどう **構築するか**」の話だった。だが組み立てた脳は、放っておけば動かない。ひとつ問いが残る——5 要素を揃えても、要件は次々に積み上がり、消化しきる前に次が来る。**人間チームなら破綻するこの状況を、なぜ AI 開発では止めずに回し続けられるのか?** 第二の脳を「持つ」ことと「動かし続ける」ことは、別の技術だ。

次回 **#16** では、その問いをまっすぐ扱う——キヤノンの「三自の精神」と成果を出し続けるマネジャーの発想を AI 運用に転用する、第二の脳の **運用論**。本記事で判断ゲートとして据えた「第一の脳 (自身の経験)」が、要件の奔流の中で何を手放し、何を絶対に手放してはいけないのかを確かめにいく。

---

**過去の関連記事**:
- [12] llive 開発履歴 — 5 日で v0.1 から v0.7 候補へ
- [13] コーパス先行戦略 — AI が気づかない観点を思考フローに補完
- [14] HTML で見えないのに、機械では読める — 不可視アノテーションチャネル設計

## 参考文献 / 参考リソース

### TRIZ (発明的問題解決理論)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996
- Karen Gadd, *TRIZ for Engineers: Enabling Inventive Problem Solving*, Wiley, 2011
- TRIZ Journal (オンラインアーカイブ) — https://triz-journal.com/

### RAG / コーパス構築
- Patrick Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 (arXiv:2005.11401)
- Raptor (本記事で参照した RAD コーパス構築ツール) — https://github.com/raptor-rad/raptor (本人 fork: 公開準備中)

### 「第二の脳」概念の原点
- Tiago Forte, *Building a Second Brain: A Proven Method to Organize Your Digital Life and Unlock Your Creative Potential*, Atria Books, 2022
- 邦訳: 春川由香 訳『SECOND BRAIN — 時間に追われない「知的生産術」』ダイヤモンド社, 2022

### 開発エージェント
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Perplexity AI — https://www.perplexity.ai/

### llive 関連
- llive リポジトリ — https://github.com/furuse-kazufumi/llive
- 本記事の「9 セッション 14 機能 1270 PASS」の根拠: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`

<!-- llive:meta.article_id="15_second_brain_spiral_dev" target=llove -->
<!-- llive:meta.published_date="2026-05-19" -->
<!-- llive:meta.tags=["llive","claude-code","perplexity","triz","rag","development","oss"] target=any -->

---

# English

# 30 Years of Software Development Experience + Perplexity Summaries + Claude Code + TRIZ + a 50,000-Paper RAG = a "Second Brain"

> 📚 **Series nav**: ← #14 Designing the invisible annotation channel ｜ **#15 This article** ｜ #16 Running AI with the "three selves" spirit → ｜ [Series LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ Each article also stands on its own (links are for browsing).
>
> In the previous article #14, I designed an annotation channel that humans cannot see but machines can read. This article steps back one level: how do I stack up that body of features alone—that is, how do I **build** the "second brain" that powers the development?

**One-line hook**:
As a solo developer, over 5 days I added 14 features—including the Brief API, OKA-FX, VRB-FX, IND-04 annotations, and the MathVerifier—plus 256 tests, achieving 1270 all-PASS with zero regressions. The secret lies in how you assemble a "second brain."

---

## Defining the "Second Brain"

I am a software developer with over 30 years of experience, and I develop llive (the core product of the FullSense umbrella; the L appears twice) **entirely on my own**—yet the pace resembles team development. That is because I built a "second brain" by combining the following five elements.

| Element | Role |
|---|---|
| **30 years of dev experience** | The baseline for design quality and judgment. Fed into every session as ideas and know-how |
| **Perplexity summaries** | High-quality compression of the external ideas I want to absorb (books, papers, YouTube) |
| **Claude Code (Opus 4.7 / 1M context)** | The implementation agent |
| **TRIZ rules (40 principles)** | A meta-thinking frame for resolving contradictions. Carried from patent-domain experience into llive design |
| **Paper RAG corpus (RAD 49 fields / ~50,000 items)** | The foundation that lets Claude Code answer with "a researcher's insight" |

When these are fed through a **spiral development cycle**, external ideas land into implementation in a short time.

### ☕ A small digression

The phrase "second brain" felt embarrassing at first. It seemed cliché, dragged down by Tiago Forte's book of the same name. But after stacking 14 features solo in 5 days and looking back, I couldn't find a more fitting term. **Embarrassment folds before accuracy.**

## One Spiral Cycle

![Flow of one spiral development cycle (external ideas → Perplexity summary → Claude Code read-in → requirements → implement → benchmark → commit → next cycle)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q15/spiral_cycle_en.svg)

Real examples (3 of the 9 sessions this run):

| Cycle | Starting point | Result |
|---|---|---|
| 1 | **MBA verbalization training** (a Globis book) | Perplexity organized it into 8 features → 4 VRB-FX (Verbalization Framework) items turned into requirements → VRB-02 PromptLint implemented (1 session) |
| 2 | **Learning from Dr. Kiyoshi Oka's view of mathematics** (from the YouTube talk "The Depths of Psychology") | The ideas Dr. Oka left behind—"mathematics is emotion," "before discovery you hit a wall once," "you cannot advance contemplation without writing," "the native language nurtures mathematics"—were summarized with Perplexity and then referenced as **4 design viewpoints** → written up as 10 OKA-FX requirements → OKA-01 to 04 minimal proto implemented. **This does not claim to implement Dr. Oka's thinking itself**; the naming expresses respect for the ideas of Dr. Oka that inspired this design |
| 3 | **LinkedIn feedback** "I want to avoid mutual dependence" | IND-FX design principle + IND-04 Annotation Channel implemented, achieving both independence and combinatorial value via `<!-- llive:ns.key=val -->` |

Each cycle runs to completion—**requirements → implementation → tests → commit**—within a few hours.

## Why the Spiral Keeps Turning

### The role of Perplexity summaries — an "input quality gate"

External ideas come in scattered formats: books, papers, videos, social posts. Throwing these directly at Claude Code causes:
- The source material is huge and eats the context window
- Important parts and noise are mixed together
- Claude's interpretation wobbles

When you instruct Perplexity with "summarize to ~3000 characters," "in an implementable spec," and "as a comparison table," it converts the material into **input at a quality Claude Code can read**. This works as an "input quality gate."

### The role of TRIZ — "meta-thinking for resolving contradictions"

Contradictions appear repeatedly during implementation. Examples:
- "I want to guarantee independence" vs "I want to stack up value through combination"
- "I want to keep the rule-based fallback too" vs "I want to measure LLM quality"
- "I want to capture complete audit logs" vs "I don't want to add implementation overhead"

Solving these from the **TRIZ contradiction matrix** perspective reveals win-win solutions. This run's solutions:
- IND-04 Annotation Channel = both achieved via "comments = invisible to the renderer + machine-readable" (TRIZ Principle 24: intermediary)
- Leaving the echo baseline in place = both achieved via "show the same rule-based output under a separate category" (TRIZ Principle 1: segmentation)
- The bind_ledger() pattern = both achieved via "optional injection makes audit zero-cost" (TRIZ Principle 15: dynamics)

### The role of the paper RAG (RAD 49 fields, ~50,000 items) — "borrowing a researcher's insight"

Every time a feature design requires a field, I pull from the RAG corpus. Examples this run:
- OKA-FX design → referenced `mathematics` / `formal_methods` / `metrology`
- VRB-FX design → referenced `mba` (management) / `linguistics`
- IND-04 design → referenced `software_engineering` / `oss_governance`

When Claude Code writes "in its own words" it tends toward generalities, but **citing concrete papers and prior work via RAG** raises the quality a notch.

## Results — What Happened in 5 Days

| Day | Main additions |
|---|---|
| 5/13 | llive project launched, Phase 1 completed |
| 5/14 | F25 integration base completed (llove↔llmesh↔llive via MCP) |
| 5/15 | 9-axis skeleton (KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL) |
| 5/16 | C-1 Approval Bus + Policy + SQLite Ledger completed / 815 PASS |
| 5/16 | Brief API end-to-end / progressive matrix completed / 998 PASS |
| 5/17 | **9 sessions** with 14 features (COG-04, CREAT-04, MATH-02, OKA-01–07, VRB-02/04/05/06, CREAT-01–05, IND-FX, MathVerifier-Runner integration, etc.) / **256 tests added** / **1270 PASS / zero regressions** |

Producing this speed in solo development is only possible because of the "second brain" where the five elements mesh together.

### ☕ Thanks for reading this far

Honestly, 7–8 of the 256 tests each failed once along the way. Every time fuzzing's hypothesis gleefully finds an edge case, I go "ugh" for about 3 seconds. **1270 PASS / zero regressions** is the goal, not the process.

## Where My Own 30 Years of Experience Pay Off

"Leave it all to Claude Code" does not yield quality. My 30 years of experience were decisive in the following scenes.

1. **Quality of requirements definition** — Reading a Perplexity summary and instantly judging "this conflates requirement vs solution," then ordering a rewrite
2. **Selecting TRIZ rules** — Instantly extracting "for this scene, these three" from the 40 principles (without TRIZ experience you lose time here)
3. **Architecture judgment** — Instantly rejecting an implementation proposal from Claude with "this violates the independence principle" or "this is inconsistent with the bind_ledger pattern"
4. **Honest disclosure on benchmarks** — Instantly seeing through "this is the fake performance of an echo back" when the rule-based coverage comes out high (measurement experience)
5. **Typo checking** — Instantly identifying "llive became lllive—the tokenizer problem has recurred" (pattern recognition)

In other words, against the **second brain = Claude Code + RAG + Perplexity + TRIZ**, the **first brain = my own experience** remains in place as the judgment gate. The synthesis of the two makes "one person + a second brain = a team" hold.

## Implications for Other Developers

The cost of building this "second brain":
- Claude Code subscription (Max plan recommended, 1M context essential)
- Perplexity Pro ($20/month)
- RAG corpus construction (self-built with an OSS tool like Raptor; this case is ~50,000 items / 49 fields)
- TRIZ study (a few books + practice)
- **Above all, the resolve to keep feeding your own experience to Claude Code**

The last item matters most. If you dump everything on Claude Code, you only get run-of-the-mill implementations. By **keeping an experienced person in place as reviewer + architect**, the synthesis of "a researcher team + 30 years of experience + an implementation agent" holds.

llive is currently OSS under an Apache 2.0 + Commercial dual-license, repo at https://github.com/furuse-kazufumi/llive . If you are interested in this "second brain" style of development, I'd like to discuss it via Issue / Discussion.

### But "assembling it" alone makes it stall

So far this has been about how you **build** the second brain. But an assembled brain does nothing if left alone. One question remains: even with the five elements in place, requirements keep piling on, and the next arrives before you've digested the last. **Why can AI development keep this situation turning—the very situation that would break a human team—instead of stalling?** "Having" a second brain and "keeping it running" are different skills.

In the next article **#16**, I tackle that question head-on—the **operation theory** of the second brain: carrying over Canon's "three selves" spirit and the mindset of managers who keep producing results into running AI. We'll see what the "first brain (my own experience)," seated as the judgment gate in this article, gives up in the torrent of requirements—and what it must never give up.

---

**Past related articles**:
- [12] llive development history — from v0.1 to a v0.7 candidate in 5 days
- [13] Corpus-first strategy — supplementing the thought flow with viewpoints the AI doesn't notice
- [14] Invisible in HTML, yet machine-readable — designing the invisible annotation channel

## References / Resources

### TRIZ (Theory of Inventive Problem Solving)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996
- Karen Gadd, *TRIZ for Engineers: Enabling Inventive Problem Solving*, Wiley, 2011
- TRIZ Journal (online archive) — https://triz-journal.com/

### RAG / Corpus Construction
- Patrick Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 (arXiv:2005.11401)
- Raptor (the RAD corpus construction tool referenced in this article) — https://github.com/raptor-rad/raptor (author's fork: preparing for release)

### The Origin of the "Second Brain" Concept
- Tiago Forte, *Building a Second Brain: A Proven Method to Organize Your Digital Life and Unlock Your Creative Potential*, Atria Books, 2022
- Japanese translation: trans. Yuka Harukawa, *SECOND BRAIN — The "Intellectual Production Technique" Free from Time Pressure*, Diamond, 2022

### Development Agents
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Perplexity AI — https://www.perplexity.ai/

### llive-Related
- llive repository — https://github.com/furuse-kazufumi/llive
- Basis for this article's "9 sessions, 14 features, 1270 PASS": `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`

---

# 中文

# 30 年软件开发经验 + Perplexity 摘要 + Claude Code + TRIZ + 5 万篇论文 RAG =「第二大脑」

> 📚 **连载导航**: ← #14 不可见注释通道设计 ｜ **#15 本文** ｜ #16 以「三自」精神运营 AI → ｜ [连载 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 每篇文章均可独立阅读（链接用于回游）。
>
> 上一篇 #14 设计了人看不见、却能被机器读取的注释通道。本文退后一步：这一整套功能，我是如何一个人堆起来的——也就是，支撑开发的「第二大脑」该 **如何构建**。

**一行 hook**:
作为单人开发者，我在 5 天内追加了包含 Brief API、OKA-FX、VRB-FX、IND-04 注释、MathVerifier 在内的 14 个功能和 256 个测试，实现了 1270 项全部 PASS、零回归。秘诀在于如何组装「第二大脑」。

---

## 「第二大脑」的定义

笔者（拥有 30 余年经验的软件开发者）**独自一人开发** llive（FullSense umbrella 的核心产品，L 有两个），但进度接近团队开发。这是因为构建了组合下列五个要素的「第二大脑」。

| 要素 | 作用 |
|---|---|
| **30 年开发经验** | 设计质量与判断的基础。作为想法与诀窍在每次会话中传递 |
| **Perplexity 摘要** | 把想要吸收的外部思想（书籍、论文、YouTube）高质量地压缩 |
| **Claude Code (Opus 4.7 / 1M context)** | 实现代理 |
| **TRIZ 规则（40 原理）** | 解决矛盾的元思考框架。从专利领域的经验带入 llive 设计 |
| **论文 RAG 语料库（RAD 49 领域 / 约 5 万件）** | 让 Claude Code 以「研究者的见解」作答的基础 |

把这些放进 **螺旋开发周期**，外部思想就能在短时间内落到实现上。

### ☕ 稍微跑题

「第二大脑」这个词，起初让我有点难为情。被 Tiago Forte 的同名书籍牵着走，感觉很俗套。但在 5 天内独自堆完 14 个功能后回头看，再也找不到比它更贴切的词。**难为情会在准确面前折服。**

## 一个螺旋周期

![一个螺旋开发周期的流程图（外部思想 → Perplexity 摘要 → Claude Code 读入 → 要件化 → 实现 → 基准 → commit → 下一周期）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q15/spiral_cycle_zh.svg)

实际示例（本次 9 个会话中的 3 例）:

| 周期 | 起点 | 结果 |
|---|---|---|
| 1 | **MBA 语言化训练**（Globis 书籍） | Perplexity 整理为 8 个功能 → 将 VRB-FX (Verbalization Framework) 4 项要件化 → 实现 VRB-02 PromptLint（1 个会话） |
| 2 | **向冈洁先生的数学观学习**（出自 YouTube《心理的深层》讲话） | 先生留下的「数学是情绪」「发现之前会先碰壁一次」「不写文章就无法推进思索」「国语滋养数学」等思想，先用 Perplexity 加以摘要，再作为 **设计的 4 个观点** 参照 → 记述为 10 项 OKA-FX 要件 → 实现 OKA-01〜04 minimal proto。**并非主张实现了先生的思想本身**，命名是为表达对触发本设计的先生思想的敬意 |
| 3 | **LinkedIn 反馈**「想避免相互依赖」 | 实现 IND-FX 设计原则 + IND-04 Annotation Channel，以 `<!-- llive:ns.key=val -->` 兼顾独立性与组合价值 |

每个周期都能在数小时内跑完 **要件 → 实现 → 测试 → commit**。

## 为什么螺旋能转起来

### Perplexity 摘要的作用 —「输入质量门」

外部思想形式各异：书、论文、视频、社交平台。把这些直接丢给 Claude Code 会导致:
- 原始信息庞大，吞噬 context window
- 重要部分与噪声混杂
- Claude 的解读出现摇摆

向 Perplexity 指示「摘要到约 3000 字」「以可实现的规格」「以对比表」时，便会转换为 **Claude Code 能读取的质量的输入**。这就作为「输入质量门」发挥作用。

### TRIZ 的作用 —「解决矛盾的元思考」

实现过程中矛盾会一再出现。例如:
- 「想保证独立性」 vs 「想通过组合积累价值」
- 「也想保留 rule-based fallback」 vs 「想测量 LLM 质量」
- 「想完整获取审计日志」 vs 「不想增加实现开销」

从 **TRIZ 矛盾矩阵** 视角求解，就能看到两立解。本次会话的解:
- IND-04 Annotation Channel =「注释 = renderer 不可见 + 机器可读」实现两立（TRIZ 原理 24: 中介物）
- 保留 echo baseline =「把相同的 rule-based 输出以另一类别显示」实现两立（TRIZ 原理 1: 分割）
- bind_ledger() pattern =「以 optional 注入使 audit 零成本」实现两立（TRIZ 原理 15: 动态化）

### 论文 RAG（RAD 49 领域 ~5 万件）的作用 —「借用研究者的见解」

每当新功能设计需要某个领域，就检索 RAG 语料库。本次会话示例:
- OKA-FX 设计 → 参照 `mathematics` / `formal_methods` / `metrology`
- VRB-FX 设计 → 参照 `mba` (management) / `linguistics`
- IND-04 设计 → 参照 `software_engineering` / `oss_governance`

Claude Code 用「自己的话」写时容易流于一般论，但**通过 RAG 引用具体论文与先行研究**，质量便会上一个台阶。

## 结果 — 5 天内发生的事

| Day | 主要追加 |
|---|---|
| 5/13 | llive 项目启动，Phase 1 完成 |
| 5/14 | F25 联动基础完成（llove↔llmesh↔llive 经由 MCP） |
| 5/15 | 9 轴 skeleton (KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL) |
| 5/16 | C-1 Approval Bus + Policy + SQLite Ledger 完成 / 815 PASS |
| 5/16 | Brief API end-to-end / progressive matrix 跑完 / 998 PASS |
| 5/17 | **9 个会话** 内 14 个功能 (COG-04, CREAT-04, MATH-02, OKA-01〜07, VRB-02/04/05/06, CREAT-01〜05, IND-FX, MathVerifier-Runner 整合, etc.) / **追加 256 个测试** / **1270 PASS / 零回归** |

单人开发能跑出这种速度，全靠五个要素咬合的「第二大脑」。

### ☕ 谢谢你读到这里

老实说，256 个测试中有 7-8 个在途中各失败过一次。每当 fuzzing 的 hypothesis 兴高采烈地找到 edge case，我就会「呃」上 3 秒左右。**1270 PASS / 零回归** 是目标，而不是过程。

## 自身的 30 年经验在哪里起作用

「全交给 Claude Code」是出不了质量的。30 年经验在下列场景中起了决定性作用。

1. **要件定义的质量** — 读 Perplexity 摘要后立即判定「这把要件 vs 解法混为一谈」，并下达重写指示
2. **TRIZ 规则的选定** — 从 40 原理中立即抽出「这个场景就这 3 个」（没有 TRIZ 经验会在此处耗时）
3. **架构判断** — 立即否决 Claude 给出的实现方案「这违反独立性原则」「这与 bind_ledger pattern 不一致」
4. **基准的 honest disclosure** — 当 rule-based 的 coverage 出得很高时，立即看穿「这是 echo back 的虚假性能」（测量经验）
5. **拼写检查** — 立即识别「llive 变成了 lllive，tokenizer 问题复发」（模式识别）

也就是说，相对于 **第二大脑 = Claude Code + RAG + Perplexity + TRIZ**，**第一大脑 = 自身的经验** 始终作为判断门存在。两者的合成让「一个人 + 第二大脑 = 团队」得以成立。

## 对其他开发者的启示

构建这个「第二大脑」的成本:
- Claude Code 订阅（推荐 Max plan，1M context 必备）
- Perplexity Pro（每月 $20）
- RAG 语料库构建（用 Raptor 等 OSS 工具自建，本 case 约为 5 万件 / 49 领域）
- TRIZ 学习（数本书籍 + 实践）
- **最重要的是持续把自身经验传递给 Claude Code 的觉悟**

最后一项最重要。把一切甩给 Claude Code，只会得到平庸的实现。通过**让有经验者作为评审者 + 架构师持续在场**，「研究者团队 + 30 年经验 + 实现代理」的合成才得以成立。

llive 现阶段为 Apache 2.0 + Commercial dual-license 的 OSS，Repo 在 https://github.com/furuse-kazufumi/llive 。对本文这种「第二大脑」型开发风格感兴趣的朋友，欢迎以 Issue / Discussion 讨论。

### 但只是「组装好了」就会停摆

到这里，讲的都是「第二大脑该 **如何构建**」。可是组装好的大脑，搁着不管就不会动。还剩一个问题——五个要素就位之后，需求仍会一个接一个堆上来，前一个还没消化完，下一个就来了。**这种在人类团队里会崩溃的局面，为什么 AI 开发能不停摆、持续转起来?**「拥有」第二大脑与「让它持续运转」，是两种不同的技术。

下一篇 **#16** 将正面处理这个问题——第二大脑的 **运营论**：把佳能的「三自」精神，以及持续出成果的管理者的发想，转用到 AI 运营上。我们会去看，本文中作为判断门坐镇的「第一大脑（自身的经验）」，在需求的洪流中放下了什么、又绝对不能放下什么。

---

**过去的相关文章**:
- [12] llive 开发历史 — 5 天内从 v0.1 到 v0.7 候选
- [13] 语料库先行战略 — 为思考流程补充 AI 未察觉的观点
- [14] 在 HTML 中不可见，却能被机器读取 — 不可见注释通道设计

## 参考文献 / 参考资源

### TRIZ（发明问题解决理论）
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996
- Karen Gadd, *TRIZ for Engineers: Enabling Inventive Problem Solving*, Wiley, 2011
- TRIZ Journal（在线存档） — https://triz-journal.com/

### RAG / 语料库构建
- Patrick Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 (arXiv:2005.11401)
- Raptor（本文参照的 RAD 语料库构建工具） — https://github.com/raptor-rad/raptor（本人 fork: 公开准备中）

### 「第二大脑」概念的原点
- Tiago Forte, *Building a Second Brain: A Proven Method to Organize Your Digital Life and Unlock Your Creative Potential*, Atria Books, 2022
- 日译: 春川由香 译《SECOND BRAIN — 不被时间追赶的「知性生产术」》钻石社, 2022

### 开发代理
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Perplexity AI — https://www.perplexity.ai/

### llive 相关
- llive 仓库 — https://github.com/furuse-kazufumi/llive
- 本文「9 会话 14 功能 1270 PASS」的依据: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`

---

# 한국어

# 30년의 소프트웨어 개발 경험 + Perplexity 요약 + Claude Code + TRIZ + 5만 건의 논문 RAG = 「제2의 뇌」

> 📚 **연재 내비**: ← #14 비가시 주석 채널 설계 ｜ **#15 본 글** ｜ #16 삼자(三自)의 정신으로 AI 운용 → ｜ [연재 LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ 각 글은 단독으로도 읽을 수 있습니다(링크는 회유용).
>
> 앞 글 #14에서는 사람에게는 보이지 않고 기계만 읽는 주석 채널을 설계했다. 본 글은 거기서 한 발 물러서서, 그 기능군을 혼자서 어떻게 쌓아 올리는가——개발을 떠받치는 「제2의 뇌」를 **어떻게 구축하는가** 를 쓴다.

**한 줄 hook**:
1인 개발로 5일간 Brief API・OKA-FX・VRB-FX・IND-04 주석・MathVerifier를 포함한 14개 기능과 256개 테스트를 추가하고, 1270건 전부 PASS로 회귀 제로를 달성했다. 비결은 「제2의 뇌」를 어떻게 조립하느냐에 있다.

---

## 「제2의 뇌」의 정의

필자(30년 넘는 소프트웨어 개발자)는 llive(FullSense umbrella의 핵심 제품, L은 2개)를 **혼자서 개발**하고 있지만, 진도는 팀 개발에 가깝다. 이는 다음 5가지 요소를 조합한 「제2의 뇌」를 구축했기 때문이다.

| 요소 | 역할 |
|---|---|
| **30년의 개발 경험** | 설계 품질・판단의 기반. 아이디어・노하우로서 매 세션마다 전달 |
| **Perplexity 요약** | 받아들이고 싶은 외부 사상(서적・논문・YouTube)을 고품질로 압축 |
| **Claude Code (Opus 4.7 / 1M context)** | 구현 에이전트 |
| **TRIZ 규칙(40 원리)** | 모순 해결의 메타 사고 프레임. 특허 영역에서의 경험에서 llive 설계로 |
| **논문 RAG 코퍼스(RAD 49 분야 / 약 5만 건)** | Claude Code가 「연구자의 견해」로 답하는 토대 |

이것들을 **스파이럴 개발 사이클**에 흘리면, 외부 사상이 짧은 시간에 구현으로 안착한다.

### ☕ 잠깐 곁길로

「제2의 뇌」라는 말, 처음에는 좀 쑥스러웠다. Tiago Forte의 동명 서적에 끌려가 진부하게 들리는 느낌이 들어서. 하지만 5일간 14개 기능을 혼자 다 쌓은 후 돌아보니, 이보다 더 딱 맞는 말을 찾을 수 없었다. **쑥스러움은 정확함 앞에서 꺾인다.**

## 스파이럴 1 사이클

![스파이럴 개발 1 사이클의 플로우 다이어그램 (외부 사상 → Perplexity 요약 → Claude Code 읽기 → 요건화 → 구현 → 벤치 → commit → 다음 사이클)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q15/spiral_cycle_ko.svg)

실제 예(이번 세션 9회 중 3예):

| 사이클 | 기점 | 결과 |
|---|---|---|
| 1 | **MBA 언어화 트레이닝**(Globis 서적) | Perplexity가 8개 기능으로 정리 → VRB-FX (Verbalization Framework) 4건 요건화 → VRB-02 PromptLint 구현(1 세션) |
| 2 | **오카 기요시 선생의 수학관에서 배움**(YouTube『심리의 심층』 강화에서) | 선생이 남기신 「수학은 정서다」「발견 전에 한 번 막힌다」「글을 쓰지 않고는 사색을 진전시킬 수 없다」「국어가 수학을 키운다」라는 사상을, Perplexity로 요약한 뒤 **설계의 4 관점**으로 참조 → OKA-FX 10 요건으로 기술 → OKA-01〜04 minimal proto 구현. **선생의 생각 그 자체를 구현했다고 주장하는 것은 아니며**, 이쪽 설계가 영감을 받은 선생의 사상에 대한 경의를 표하여 명명하고 있다 |
| 3 | **LinkedIn 피드백**「상호 의존을 피하고 싶다」 | IND-FX 설계 원칙 + IND-04 Annotation Channel 구현, `<!-- llive:ns.key=val -->`로 독립성과 조합 가치를 양립 |

각 사이클이 **요건 → 구현 → 테스트 → commit**까지 수 시간 안에 완주한다.

## 왜 스파이럴이 돌아가는가

### Perplexity 요약의 역할 — 「입력 품질 게이트」

외부 사상은 책・논문・동영상・SNS와 형식이 제각각이다. 이것을 Claude Code에 직접 던져 넣으면:
- 원 정보가 방대하여 context window를 잡아먹는다
- 중요 부분과 노이즈가 뒤섞인다
- Claude의 해석에 흔들림이 생긴다

Perplexity에 「~3000자로 요약」「구현 가능한 사양으로」「대비 표로」라고 지시하면, **Claude Code가 읽어낼 수 있는 품질의 입력**으로 변환된다. 이것이 「입력 품질 게이트」로서 기능한다.

### TRIZ의 역할 — 「모순 해결의 메타 사고」

구현 중에 몇 번이고 모순이 나온다. 예:
- 「독립성을 담보하고 싶다」 vs 「조합으로 가치를 쌓아 올리고 싶다」
- 「rule-based fallback도 남기고 싶다」 vs 「LLM 품질을 측정하고 싶다」
- 「감사 로그를 완전하게 남기고 싶다」 vs 「구현 오버헤드를 늘리고 싶지 않다」

이것을 **TRIZ 모순 매트릭스** 관점으로 풀면, 양립 해가 보인다. 이번 세션의 해:
- IND-04 Annotation Channel = 「주석 = renderer 비가시 + 기계 가독」으로 양립(TRIZ 원리 24: 매개물)
- echo baseline 잔존 = 「같은 rule-based 출력을 다른 카테고리로 표시」로 양립(TRIZ 원리 1: 분할)
- bind_ledger() pattern = 「optional 주입으로 audit는 제로 코스트」로 양립(TRIZ 원리 15: 동적화)

### 논문 RAG (RAD 49 분야 ~5만 건)의 역할 — 「연구자의 견해를 빌린다」

새 기능 설계에서 필요한 분야가 나올 때마다 RAG 코퍼스를 끌어온다. 이번 세션 예:
- OKA-FX 설계 → `mathematics` / `formal_methods` / `metrology` 참조
- VRB-FX 설계 → `mba` (management) / `linguistics` 참조
- IND-04 설계 → `software_engineering` / `oss_governance` 참조

Claude Code가 「자기 말」로 쓰면 일반론이 되기 쉽지만, **RAG로 구체적인 논문・선행 연구를 인용**하면 품질이 한 단계 올라간다.

## 결과 — 5일간 일어난 일

| Day | 주요 추가 |
|---|---|
| 5/13 | llive 프로젝트 출범, Phase 1 완료 |
| 5/14 | F25 연계 기반 완료(llove↔llmesh↔llive MCP 경유) |
| 5/15 | 9축 skeleton (KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL) |
| 5/16 | C-1 Approval Bus + Policy + SQLite Ledger 완료 / 815 PASS |
| 5/16 | Brief API end-to-end / progressive matrix 완주 / 998 PASS |
| 5/17 | **9 세션**으로 14개 기능 (COG-04, CREAT-04, MATH-02, OKA-01〜07, VRB-02/04/05/06, CREAT-01〜05, IND-FX, MathVerifier-Runner 통합, etc.) / **256개 테스트 추가** / **1270 PASS / 회귀 제로** |

1인 개발로 이 속도를 내는 것은, 5가지 요소가 맞물리는 「제2의 뇌」가 있어야 비로소 가능하다.

### ☕ 여기까지 읽어 주셔서 감사합니다

솔직히 256개 테스트 중 7-8건은 도중에 한 번씩 떨어졌다. fuzzing이 hypothesis로 기쁜 듯이 edge case를 찾아낼 때마다 3초 정도 「으악」 하게 된다. **1270 PASS / 회귀 제로**는 골이지 과정이 아니다.

## 자신의 30년 경험은 어디서 효과를 발휘하는가

「Claude Code에 맡기기」만으로는 품질이 나오지 않는다. 30년 경험은 다음 장면에서 결정적이었다.

1. **요건 정의의 질** — Perplexity 요약을 읽고 「이건 요건 vs 해법을 혼동하고 있다」고 즉시 판정하여 재작성 지시
2. **TRIZ 규칙의 선정** — 40 원리에서 「이 장면은 이 3개」를 즉시 추출(TRIZ 경험이 없으면 여기서 시간을 빼앗긴다)
3. **아키텍처 판단** — Claude가 내놓은 구현안을 「이건 독립성 원칙에 어긋난다」「이건 bind_ledger pattern과 정합하지 않는다」고 즉시 거부
4. **벤치의 honest disclosure** — rule-based의 coverage가 높게 나왔을 때 「이건 echo back의 가짜 성능」이라고 즉시 간파(측정 경험)
5. **오타 체크** — 「llive가 lllive로 되어 있다, tokenizer 문제의 재발」이라고 즉시 특정(패턴 인식)

즉 **제2의 뇌 = Claude Code + RAG + Perplexity + TRIZ**에 대해, **제1의 뇌 = 자신의 경험**이 판단 게이트로서 계속 존재한다. 양자의 합성이 「1인 + 제2의 뇌 = 팀」을 성립시키고 있다.

## 다른 개발자들에게 주는 시사점

이 「제2의 뇌」를 구축하는 비용:
- Claude Code 구독(Max plan 권장, context 1M 필수)
- Perplexity Pro(월 $20)
- RAG 코퍼스 구축(Raptor 등 OSS 도구로 자체 제작, 본 case는 ~5만 건 / 49 분야)
- TRIZ 학습(서적 몇 권 + 실천)
- **무엇보다 자신의 경험을 Claude Code에 계속 전달할 각오**

마지막 항목이 가장 중요하다. Claude Code에 통째로 맡기면 흔해 빠진 구현밖에 나오지 않는다. **경험자가 리뷰어 + 아키텍트로서 계속 존재**함으로써, 「연구자 팀 + 30년 경험 + 구현 에이전트」의 합성이 성립한다.

llive는 현시점에서 Apache 2.0 + Commercial dual-license의 OSS이며, Repo는 https://github.com/furuse-kazufumi/llive 이다. 본 글의 「제2의 뇌」형 개발 스타일에 관심 있는 분은 Issue / Discussion으로 논의하고 싶다.

### 하지만 「조립한」 것만으로는 멈춘다

여기까지는 「제2의 뇌를 어떻게 **구축하는가**」의 이야기였다. 하지만 조립한 뇌는, 내버려 두면 움직이지 않는다. 한 가지 물음이 남는다——5가지 요소를 갖춰도 요건은 계속 쌓이고, 다 소화하기 전에 다음이 온다. **인간 팀이라면 무너지는 이 상황을, 왜 AI 개발에서는 멈추지 않고 계속 돌릴 수 있는가?** 제2의 뇌를 「가지는」 것과 「계속 움직이는」 것은 별개의 기술이다.

다음 글 **#16**에서는 그 물음을 정면으로 다룬다——캐논의 「삼자(三自)의 정신」과 성과를 계속 내는 매니저의 발상을 AI 운용에 전용하는, 제2의 뇌의 **운용론**. 본 글에서 판단 게이트로 앉혀 둔 「제1의 뇌(자신의 경험)」가, 요건의 격류 속에서 무엇을 놓고 무엇을 절대 놓아서는 안 되는지를 확인하러 간다.

---

**과거의 관련 기사**:
- [12] llive 개발 이력 — 5일 만에 v0.1에서 v0.7 후보로
- [13] 코퍼스 선행 전략 — AI가 깨닫지 못하는 관점을 사고 흐름에 보완
- [14] HTML에서는 보이지 않지만, 기계로는 읽힌다 — 비가시 주석 채널 설계

## 참고문헌 / 참고 리소스

### TRIZ (발명적 문제 해결 이론)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996
- Karen Gadd, *TRIZ for Engineers: Enabling Inventive Problem Solving*, Wiley, 2011
- TRIZ Journal (온라인 아카이브) — https://triz-journal.com/

### RAG / 코퍼스 구축
- Patrick Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 (arXiv:2005.11401)
- Raptor (본 글에서 참조한 RAD 코퍼스 구축 도구) — https://github.com/raptor-rad/raptor (본인 fork: 공개 준비 중)

### 「제2의 뇌」 개념의 원점
- Tiago Forte, *Building a Second Brain: A Proven Method to Organize Your Digital Life and Unlock Your Creative Potential*, Atria Books, 2022
- 일본어 번역: 하루카와 유카 옮김 『SECOND BRAIN — 시간에 쫓기지 않는 「지적 생산술」』 다이아몬드사, 2022

### 개발 에이전트
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Perplexity AI — https://www.perplexity.ai/

### llive 관련
- llive 리포지토리 — https://github.com/furuse-kazufumi/llive
- 본 글의 「9 세션 14 기능 1270 PASS」의 근거: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`
