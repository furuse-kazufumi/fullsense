---
title: 「三自の精神」を AI に課す — 圧倒的成果を出し続けるマネジャー流の AI 運用論
tags:
  - FullSense
  - llive
  - 解説
  - TODO_TAG
  - TODO_TAG
private: false
updated_at: '2026-05-22'
id: faca5557d51a06a657f4
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 「三自の精神」を AI に課す — 圧倒的成果を出し続けるマネジャー流の AI 運用論

> 📚 **連載ナビ**: ← #15 「第二の脳」開発論 ｜ **#16 本記事** ｜ #17 人と AI の融合ビジョン → ｜ [連載 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 各記事は単独でも読めます（リンクは回遊用）。

**1 行 hook**:
要件を **消化しきる前に次の要件を積み続けられる**。これは人間チームでは破綻するが AI 開発では優位性になる。条件は 1 つ — AI が **自律して動いてくれる** こと。キヤノンが掲げる「三自の精神」と、Buckingham & Coffman 等のマネジメント書籍がほぼそのまま転用できる。

---

## 起点 — 要件は止まらない

llive 開発の本セッション (2026-05-17) を例にとる。

| 時刻 | 出来事 |
|---|---|
| 開始 | 要件: COG-04 + CREAT-04 統合 |
| +1h | 追加要件: 「9 因子全部入れたら本格的に動作確認」 |
| +2h | 追加要件: 岡潔先生の思想に学ばせていただく (OKA-FX 10 件、敬意を込めて命名) |
| +3h | 追加要件: LinkedIn フィードバック (IND-FX) |
| +4h | 追加要件: ガッツリベンチマーク (12 系統) |
| +5h | 追加要件: Anthropic key 復旧 → 他 LLM 比較 |
| +6h | 追加要件: Qwen 脱却 / VLM 将来 / lllive スペリング |
| +7h | 追加要件: 開発スタイル言語化 (記事化) |
| +8h | 追加要件: 三自の精神 + マネジメント書籍 (本記事) |

人間チームならどこかで「これ以上要件入れないでください」と悲鳴が上がる。AI 開発では **全部消化し終わり、1270 PASS / 回帰ゼロ** で着地した。

## なぜこれが優位性か

人間チームの 1 サイクル = 数日〜数週間 (要件 → 設計 → 実装 → テスト → 検収)。途中で要件追加すると進行が止まる。AI 開発では:

- 1 サイクル = **数分〜数時間** (スパイラル開発)
- 消化しきる前に追加しても、次サイクルで自然に取り込める
- 筆者の「思いつき」が **そのまま要件になりうる速度**

要件定義を「いつ閉じるか」を悩む必要がない。**いつでも開けて、いつでも閉じる**。これは人間チームには真似できない「AI ならではの開発スタイル」だ。

## ただし条件 — AI が自律的に動くこと

要件を積み続けてもよい、ただし AI がいちいち「これ進めていいですか」「次は何しますか」と聞いてくると即破綻する。マネージャー (= 筆者) の頭が常にコンテキストスイッチに奪われる。

これを解く鍵が **キヤノン「三自の精神」** の AI 適用である。

| 自 | 意味 (キヤノン原典) | AI 適用 |
|---|---|---|
| **自発** | 自ら進んで行動する | 人間の指示は「終了条件」のみ、優先順位は AI が決定 |
| **自治** | 自ら管理する | AI が自分の TaskCreate / TaskUpdate を回し進捗管理 |
| **自立** | 自ら判断する | 不要な確認を省き、明確な選択肢 + 推奨で進める |

キヤノン御手洗冨士夫氏が経営理念として掲げる「三自の精神」は、本来 **人間社員の主体性育成** 用だが、これがそのまま AI セッションの設計原則になる。

### ☕ 余談 — 「三自」を AI に喋らせるとどうなるか

ChatGPT や Claude に「キヤノンの三自の精神とは？」と聞くと、ほぼ正確な答えが返ってくる。ところが「これを AI 自身に適用したらどうなる？」と続けると、急に **「私はあくまで道具なので…」** と謙遜モードに入る。AI に自律を求めるなら、**プロンプトで AI 側の謙遜を解除する** ことから始まる。

## マネジメント書籍からの転用

「圧倒的成果を出し続けるマネジャーの最優先事項」(Marcus Buckingham & Curt Coffman 系) 等のマネジメント書籍が共通して説く 4 つの実践は、AI マネジメントにそのまま適用できる。

| 書籍の原則 | 人間マネジャー | AI マネジャー (筆者の運用) |
|---|---|---|
| **Select for talent** | 適材適所、強みで人を選ぶ | Opus 4.7 を選ぶ、Brief パイプライン中の各 stage に最適な component を attach |
| **Define the right outcomes** | 結果を定義、過程を縛らない | `/goal` で終了条件のみ指示、優先順位は AI に任せる |
| **Focus on strengths** | 弱点改善より強み発揮 | mock 不要な所では LLM 使う、deterministic で済む所はそうする (Strategy 注入) |
| **Find the right fit** | 役割の最適配置 | Brief / OKA / VRB / MATH を機能ごとに module 分離、Annotation で連携 |

これらを 1 文に要約すると:

> **「結果を定義し、判断を委ね、強みに集中し、最小限の確認で進める」**

人間→人間でも有効だが、人間→AI では **特に効く**。

## 適用している具体テクニック

筆者が本セッションで使っているテクニック:

### 1. `/goal` 機能で終了条件のみ指示
Claude Code には Stop hook という仕組みがあり、`/goal` で設定した条件が達成されるまでセッションが停止しない。「ベンチマーク 1.5h で」「要件残件可能な限り消化」のように **終了条件のみ** を指定する。

### 2. AskUserQuestion で 2-4 選択肢 + 推奨提示
指示が分岐するとき、AI が **2-4 個の具体的選択肢 + 推奨案** を提示する仕組みを用いる。人間は選ぶだけで判断完了、AI 側は推奨で動く準備済なのでロスがない。

### 3. feedback memory で「次回も自律判断するルール」蓄積
本セッションで 35 個以上の feedback memory を積んでいる。例:
- 「進めますか」は最小、即実行 (`feedback_max_plan_autonomy`)
- 次の指示待ちのときは選択肢提示 (`feedback_offer_choices_when_idle`)
- セッションマラソン継続 (`feedback_session_marathon`)
- ベンチで偽性能が出たら必ず内訳を疑え (`feedback_benchmark_honest_disclosure`)

これらは次回セッションで自動参照され、**マネジャー指示なしで AI が同じ判断基準で動く**。

### 4. TaskCreate / TaskUpdate で AI 自身が進捗管理
AI が自分でタスクを切って、状態 (pending / in_progress / completed) を更新する。マイクロマネジメント不要。

### 5. commit/push は明示的確認
ローカル commit は AI 自律、push (remote 公開) は明示確認。CLAUDE.md ルールで「破壊的操作は ASK FIRST」と明文化済。

### ☕ ちなみに

筆者が `/goal` を初めて使ったとき、AI が黙々と 1 時間半ベンチを回し続けるのを見て「これ放置していいやつだ」と気づいた。マネジャーが完全に手を離せる時間は、人間チームでは月 1 日くらいだが、AI チームではセッション単位で発生する。**確認待ちで奪われていた時間が、別の創造に回せる**。

## なぜこの手法が効くか — AI と人間の特性差

| 観点 | 人間チーム | AI チーム |
|---|---|---|
| 文脈ロス速度 | 数日〜数週間 | 数時間〜数セッション |
| やり直しコスト | 高い (時間 + モチベ) | 低い (再生成即時) |
| 休息必要性 | 必須 | ゼロ |
| 説明責任 | 言語化に時間 | audit log で自動追跡 |

→ **AI は「確認を待つコスト > 多少ズレても進む価値」が成立する数少ない働き手**。だからこそ「結果を定義 + 判断を委ねる」マネジング書籍の手法がフィットする。

## マネジャーが手放してはいけないもの

「三自の精神」と「結果定義 + 任せる」は手放す方向だが、**手放してはいけない 4 つ** がある:

1. **要件の質** — 「これは要件 vs 解法を混同している」と即判定して書き直し指示
2. **アーキテクチャ判断** — AI が出した実装案を「これは独立性原則に反する」と即拒否
3. **honest disclosure** — ベンチで偽性能が出たときに「これは echo back の効果」と即見抜く
4. **品質ゲート** — 「lllive (L 3 個) のタイポを書かないように」とパターン認識で指摘

つまり **第一の脳 (30 年経験) が判断ゲートとして居続ける**こと。任せるが、放任ではない。

## まとめ

要件を消化しきる前に追加し続けられる AI 開発の優位性は、AI が自律して動くという条件下で初めて成立する。その条件を満たすために:

- キヤノン「三自の精神」(自発・自治・自立) を AI に課す
- マネジメント書籍 (Buckingham & Coffman 等) の手法をそのまま転用する
- 「結果を定義 + 判断を委ね + 強みに集中 + 最小確認で進める」

これにより 1 人開発がチーム速度に近づく。前記事 [15] が「第二の脳」の **構築論** だったとすれば、本記事はその **運用論** にあたる。

llive は Apache 2.0 + Commercial dual-license の OSS、Repo は https://github.com/furuse-kazufumi/llive 。本記事の AI マネジメント手法に興味のある方は、Issue / Discussion で議論したい。

---

**本記事は「第二の脳」シリーズの第 2 部 (運用論)**。

**過去記事**:
- [14] HTML で見えないのに、機械では読める — 不可視アノテーションチャネル設計
- [15] 30 年のソフトウェア開発経験 + Perplexity + Claude Code + TRIZ + RAG = 「第二の脳」(構築論)

## 参考文献 / 参考リソース

### キヤノン「三自の精神」
- キヤノン株式会社 公式企業理念ページ「キヤノンの企業 DNA」 — https://global.canon/ja/corporate/dna/
- 御手洗冨士夫 著『キヤノン高収益復活の秘密』ダイヤモンド社, 2001 (三自の精神の原典的解説)

### マネジメント書籍
- Marcus Buckingham & Curt Coffman, *First, Break All the Rules: What the World's Greatest Managers Do Differently*, Simon & Schuster, 1999
  - 邦訳: 宮本喜一 訳『最高のリーダー、マネジャーがいつも考えているたったひとつのこと』日本経済新聞出版, 2006
  - (本記事タイトルの「圧倒的成果を出し続けるマネジャーの最優先事項」も同系統の表現で複数版あり)
- Marcus Buckingham & Donald O. Clifton, *Now, Discover Your Strengths*, Free Press, 2001
  - 邦訳: 田口俊樹 訳『さあ、才能（じぶん）に目覚めよう』日本経済新聞出版, 2001

### Claude Code / AI エージェント運用
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Anthropic, *Building effective agents* (2024) — https://www.anthropic.com/research/building-effective-agents

### llive 関連
- llive リポジトリ — https://github.com/furuse-kazufumi/llive
- 本記事の「1 セッション 14 機能 / 1270 PASS / 回帰ゼロ」の根拠: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`
- 前作「第二の脳 構築論」: [15] (同シリーズ第 1 部)

<!-- llive:meta.article_id="16_three_self_spirit_ai_management" target=llove -->
<!-- llive:meta.published_date="2026-05-20" -->
<!-- llive:meta.tags=["llive","ai","management","canon","autonomy","leadership"] target=any -->
<!-- llive:meta.series="second_brain_part2_operations" -->

---

# English

# Imposing the "Three Selfs Spirit" on AI — A Manager's Playbook for AI Operations That Keep Delivering Outstanding Results

> 📚 **Series nav**: ← #15 The "Second Brain" Development Theory ｜ **#16 This article** ｜ #17 The Vision of Human-AI Fusion → ｜ [Series LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ Each article stands on its own (links are for browsing).

**One-line hook**:
You can **keep piling on new requirements before the old ones are fully digested**. This breaks a human team, but in AI development it becomes an advantage. There is exactly one condition — the AI has to **act autonomously**. Canon's "Three Selfs Spirit" and management books such as those by Buckingham & Coffman can be ported over almost verbatim.

---

## Starting point — the requirements never stop

Take this session of llive development (2026-05-17) as an example.

| Time | What happened |
|---|---|
| Start | Requirement: integrate COG-04 + CREAT-04 |
| +1h | Added requirement: "Once all 9 factors are in, do a serious operational check" |
| +2h | Added requirement: learn from the thought of Kiyoshi Oka (OKA-FX, 10 items, named with respect) |
| +3h | Added requirement: LinkedIn feedback (IND-FX) |
| +4h | Added requirement: a thorough benchmark (12 series) |
| +5h | Added requirement: recover the Anthropic key → compare other LLMs |
| +6h | Added requirement: break away from Qwen / future VLM / the lllive spelling |
| +7h | Added requirement: articulate the development style (write it up) |
| +8h | Added requirement: the Three Selfs Spirit + management books (this article) |

In a human team, somewhere along the way someone would cry out "please stop adding requirements." In AI development we **digested every single one and landed at 1270 PASS / zero regressions**.

## Why is this an advantage?

One cycle for a human team = days to weeks (requirements → design → implementation → testing → acceptance). Adding requirements midway stalls the process. In AI development:

- One cycle = **minutes to hours** (spiral development)
- Even if you add before fully digesting, the next cycle naturally picks it up
- The author's "passing idea" can become a requirement **at the very speed it occurs**

You never have to agonize over "when to close" the requirements definition. **Open it anytime, close it anytime.** This is a "development style unique to AI" that no human team can imitate.

## But there is a condition — the AI must act autonomously

It is fine to keep piling on requirements, but if the AI keeps asking "may I proceed with this?" or "what should I do next?" one by one, it collapses instantly. The manager's (= the author's) head is constantly robbed by context switching.

The key that unlocks this is the AI application of **Canon's "Three Selfs Spirit."**

| Self | Meaning (Canon original) | AI application |
|---|---|---|
| **Self-motivation** | Act of one's own initiative | The human instruction is only the "termination condition"; the AI decides priorities |
| **Self-management** | Manage oneself | The AI runs its own TaskCreate / TaskUpdate and manages progress |
| **Self-awareness (self-reliance)** | Judge for oneself | Skip unnecessary confirmations, proceed with clear options + a recommendation |

The "Three Selfs Spirit" that Canon's Fujio Mitarai holds up as a management philosophy is originally meant for **cultivating the autonomy of human employees**, yet it maps directly onto the design principles of an AI session.

### ☕ Aside — what happens when you make AI talk about the "Three Selfs"

If you ask ChatGPT or Claude "what is Canon's Three Selfs Spirit?" you get a nearly accurate answer. But the moment you follow up with "so what happens if you apply this to the AI itself?", it suddenly slips into modesty mode: **"I'm just a tool, after all…"**. If you want autonomy from the AI, it starts with **releasing the AI's modesty through the prompt**.

## Porting from management books

The four practices that management books such as *First, Break All the Rules: What the World's Greatest Managers Do Differently* (the Marcus Buckingham & Curt Coffman lineage) all teach in common can be applied directly to AI management.

| Book principle | Human manager | AI manager (the author's operation) |
|---|---|---|
| **Select for talent** | Right person in the right place; pick people for their strengths | Pick Opus 4.7; attach the optimal component to each stage of the Brief pipeline |
| **Define the right outcomes** | Define results, don't constrain the process | With `/goal`, instruct only the termination condition; leave priorities to the AI |
| **Focus on strengths** | Bring out strengths rather than fixing weaknesses | Use the LLM where mock-free is needed; do it deterministically where deterministic suffices (Strategy injection) |
| **Find the right fit** | Optimal placement of roles | Separate Brief / OKA / VRB / MATH into modules per function, linking via Annotation |

Summed up in one sentence:

> **"Define the outcomes, delegate the judgment, focus on strengths, and proceed with minimal confirmation."**

It works human→human too, but it is **especially effective** human→AI.

## Concrete techniques in use

Techniques the author is using in this session:

### 1. Instruct only the termination condition with the `/goal` feature
Claude Code has a mechanism called the Stop hook, where the session does not stop until the condition set with `/goal` is achieved. You specify **only the termination condition**, such as "benchmark for 1.5h" or "digest as many remaining requirements as possible."

### 2. AskUserQuestion presents 2–4 options + a recommendation
When the instruction branches, the AI uses a mechanism to present **2–4 concrete options + a recommended one**. The human only has to pick, and judgment is done; the AI is ready to act on the recommendation, so there is no loss.

### 3. Accumulate "rules to keep judging autonomously next time" via feedback memory
In this session, more than 35 feedback memories have been accumulated. Examples:
- "May I proceed" is minimized; execute immediately (`feedback_max_plan_autonomy`)
- When awaiting the next instruction, present options (`feedback_offer_choices_when_idle`)
- Continue the session marathon (`feedback_session_marathon`)
- If a benchmark shows fake performance, always suspect the breakdown (`feedback_benchmark_honest_disclosure`)

These are automatically referenced in the next session, so **the AI acts on the same judgment criteria without manager instruction**.

### 4. The AI manages its own progress via TaskCreate / TaskUpdate
The AI carves out its own tasks and updates the state (pending / in_progress / completed). No micromanagement.

### 5. commit/push require explicit confirmation
Local commits are AI-autonomous; push (remote publication) requires explicit confirmation. The CLAUDE.md rule already states in writing that "destructive operations are ASK FIRST."

### ☕ By the way

The first time the author used `/goal` and watched the AI quietly keep running benchmarks for an hour and a half, he realized "this is something I can just leave alone." The time a manager can completely take their hands off is about one day a month in a human team, but in an AI team it occurs on a per-session basis. **The time that used to be robbed by waiting for confirmation can now be redirected to other acts of creation.**

## Why this method works — the difference in traits between AI and humans

| Perspective | Human team | AI team |
|---|---|---|
| Context-loss speed | Days to weeks | Hours to a few sessions |
| Redo cost | High (time + motivation) | Low (instant regeneration) |
| Need for rest | Mandatory | Zero |
| Accountability | Verbalization takes time | Automatically tracked via audit log |

→ **AI is one of the few workers for whom "the cost of waiting for confirmation > the value of proceeding even if slightly off" holds.** That is exactly why the management-book method of "define the outcomes + delegate judgment" fits.

## What a manager must never let go of

The "Three Selfs Spirit" and "define outcomes + delegate" point toward letting go, but there are **four things you must never let go of**:

1. **The quality of requirements** — Instantly judge "this confuses requirement vs. solution" and order a rewrite
2. **Architecture decisions** — Instantly reject an implementation proposal the AI puts forward with "this violates the independence principle"
3. **honest disclosure** — When a benchmark shows fake performance, instantly see through it: "this is the effect of echo back"
4. **The quality gate** — Point out by pattern recognition: "don't write the typo lllive (three Ls)"

In other words, **the first brain (30 years of experience) must remain present as the judgment gate.** Delegate, but do not abandon.

## Summary

The advantage of AI development — being able to keep adding before the requirements are fully digested — only holds under the condition that the AI acts autonomously. To satisfy that condition:

- Impose Canon's "Three Selfs Spirit" (self-motivation, self-management, self-reliance) on the AI
- Port the methods of management books (Buckingham & Coffman, etc.) directly
- "Define the outcomes + delegate judgment + focus on strengths + proceed with minimal confirmation"

This brings solo development close to team speed. If the previous article [15] was the **construction theory** of the "Second Brain," this article is its **operations theory**.

llive is OSS under the Apache 2.0 + Commercial dual-license; the repo is https://github.com/furuse-kazufumi/llive . If you are interested in the AI management methods of this article, I would love to discuss them in an Issue / Discussion.

---

**This article is Part 2 (operations theory) of the "Second Brain" series.**

**Past articles**:
- [14] Invisible on the HTML, yet machine-readable — designing an invisible annotation channel
- [15] 30 years of software development experience + Perplexity + Claude Code + TRIZ + RAG = the "Second Brain" (construction theory)

## References / Resources

### Canon's "Three Selfs Spirit"
- Canon Inc. official corporate philosophy page "Canon's Corporate DNA" — https://global.canon/ja/corporate/dna/
- Fujio Mitarai, *The Secret of Canon's High-Profitability Revival*, Diamond Inc., 2001 (the foundational explanation of the Three Selfs Spirit)

### Management books
- Marcus Buckingham & Curt Coffman, *First, Break All the Rules: What the World's Greatest Managers Do Differently*, Simon & Schuster, 1999
  - Japanese translation: trans. Kiichi Miyamoto, *The Single Thing the Greatest Leaders and Managers Always Think About*, Nikkei Publishing, 2006
  - (The article title phrase "a manager's top priority for keeping delivering outstanding results" is of the same lineage and exists in several versions)
- Marcus Buckingham & Donald O. Clifton, *Now, Discover Your Strengths*, Free Press, 2001
  - Japanese translation: trans. Toshiki Taguchi, *Now, Awaken to Your Talent (Yourself)*, Nikkei Publishing, 2001

### Claude Code / AI agent operations
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Anthropic, *Building effective agents* (2024) — https://www.anthropic.com/research/building-effective-agents

### llive related
- llive repository — https://github.com/furuse-kazufumi/llive
- The basis for this article's "14 features / 1270 PASS / zero regressions in one session": `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`
- Previous "Second Brain construction theory": [15] (Part 1 of the same series)

---

# 中文

# 给 AI 套上「三自精神」——持续产出压倒性成果的管理者式 AI 运营论

> 📚 **连载导航**: ← #15「第二大脑」开发论 ｜ **#16 本文** ｜ #17 人与 AI 的融合愿景 → ｜ [连载 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 每篇文章均可单独阅读（链接仅供串读）。

**一行 hook**:
你可以**在尚未消化完上一批需求之前，就不断堆叠新需求**。这在人类团队中会崩溃，但在 AI 开发中却成为一种优势。条件只有一个——AI 必须**自律地行动**。佳能所倡导的「三自精神」，以及 Buckingham & Coffman 等人的管理书籍，几乎可以原封不动地移植过来。

---

## 起点——需求停不下来

以本次 llive 开发的这一段（2026-05-17）为例。

| 时刻 | 发生的事 |
|---|---|
| 开始 | 需求：整合 COG-04 + CREAT-04 |
| +1h | 追加需求：「9 个因子全部加入后，做一次正式的运行确认」 |
| +2h | 追加需求：向冈洁先生的思想学习（OKA-FX 10 项，怀着敬意命名） |
| +3h | 追加需求：LinkedIn 反馈（IND-FX） |
| +4h | 追加需求：彻底的基准测试（12 个系列） |
| +5h | 追加需求：恢复 Anthropic key → 比较其他 LLM |
| +6h | 追加需求：摆脱 Qwen / VLM 的未来 / lllive 拼写 |
| +7h | 追加需求：把开发风格语言化（写成文章） |
| +8h | 追加需求：三自精神 + 管理书籍（本文） |

若是人类团队，途中总会有人喊出「请别再加需求了」。而在 AI 开发中，我们**全部消化完毕，并以 1270 PASS / 零回归收尾**。

## 为什么这是优势

人类团队的一个周期 = 数日至数周（需求 → 设计 → 实现 → 测试 → 验收）。途中追加需求会让进度停滞。在 AI 开发中：

- 一个周期 = **数分钟至数小时**（螺旋式开发）
- 即便在消化完之前追加，下一周期也能自然纳入
- 笔者的「灵光一闪」能**以它产生的速度直接成为需求**

无需为「何时关闭」需求定义而苦恼。**随时打开，随时关闭。** 这是一种人类团队无法模仿的「AI 独有的开发风格」。

## 但有一个条件——AI 必须自律行动

可以不断堆叠需求，但如果 AI 一一来问「这个可以推进吗」「下一步做什么」，就会立刻崩溃。管理者（= 笔者）的头脑会不断被上下文切换所占据。

解开这一点的钥匙，就是**佳能「三自精神」**的 AI 化应用。

| 自 | 含义（佳能原典） | AI 应用 |
|---|---|---|
| **自发** | 主动行动 | 人类指示只给出「终止条件」，优先级由 AI 决定 |
| **自治** | 自我管理 | AI 自己运转 TaskCreate / TaskUpdate 来管理进度 |
| **自立** | 自我判断 | 省去不必要的确认，以明确选项 + 推荐推进 |

佳能御手洗富士夫所倡导的经营理念「三自精神」，本是用于**培养人类员工的主体性**，却能直接成为 AI 会话的设计原则。

### ☕ 闲谈——让 AI 谈「三自」会怎样

若你问 ChatGPT 或 Claude「佳能的三自精神是什么？」，会得到几乎准确的回答。可一旦你追问「那把这套用在 AI 自身上会怎样？」，它会突然进入谦逊模式：**「我终究只是个工具……」**。若想让 AI 自律，就要先**通过提示词解除 AI 的谦逊**。

## 从管理书籍移植

《首先，打破一切常规：世界顶尖管理者的不同之处》（Marcus Buckingham & Curt Coffman 一脉）等管理书籍共同讲述的四项实践，可以直接套用到 AI 管理上。

| 书籍原则 | 人类管理者 | AI 管理者（笔者的运营） |
|---|---|---|
| **Select for talent** | 量才适用，以长处选人 | 选用 Opus 4.7，为 Brief 流水线中各 stage 挂接最优 component |
| **Define the right outcomes** | 定义结果，不束缚过程 | 用 `/goal` 只指示终止条件，优先级交给 AI |
| **Focus on strengths** | 发挥长处胜于弥补短处 | 在需要 mock-free 处用 LLM，能用 deterministic 处就那样做（Strategy 注入） |
| **Find the right fit** | 角色的最优配置 | 把 Brief / OKA / VRB / MATH 按功能拆成 module，用 Annotation 联动 |

用一句话概括：

> **「定义结果、委以判断、专注长处、以最少确认推进」**

人对人也有效，但人对 AI **尤其见效**。

## 正在应用的具体技巧

笔者在本次会话中所用的技巧：

### 1. 用 `/goal` 功能只指示终止条件
Claude Code 有一个叫 Stop hook 的机制，在 `/goal` 设定的条件达成之前会话不会停止。你只需指定**终止条件**，例如「基准测试 1.5h」「尽可能消化剩余需求」。

### 2. AskUserQuestion 提供 2-4 个选项 + 推荐
当指示出现分支时，AI 采用一种机制，提供 **2-4 个具体选项 + 推荐方案**。人类只需选择即可完成判断，AI 一侧已准备好按推荐行动，因而毫无损耗。

### 3. 用 feedback memory 积累「下次也自律判断的规则」
本次会话已积累 35 个以上的 feedback memory。例如：
- 「可以推进吗」降到最少，立即执行（`feedback_max_plan_autonomy`）
- 等待下一指示时给出选项（`feedback_offer_choices_when_idle`）
- 持续会话马拉松（`feedback_session_marathon`）
- 基准出现伪性能时，必须怀疑其内部构成（`feedback_benchmark_honest_disclosure`）

这些会在下次会话中被自动引用，于是**AI 无需管理者指示，便以相同的判断标准行动**。

### 4. AI 自己用 TaskCreate / TaskUpdate 管理进度
AI 自行切分任务，并更新状态（pending / in_progress / completed）。无需微观管理。

### 5. commit/push 需明确确认
本地 commit 由 AI 自律，push（远程公开）需明确确认。CLAUDE.md 规则已明文写明「破坏性操作一律 ASK FIRST」。

### ☕ 顺便一提

笔者第一次使用 `/goal` 时，看着 AI 默默地连续跑了一个半小时的基准测试，意识到「这是可以放着不管的家伙」。管理者能完全撒手的时间，在人类团队中大约一个月一天，而在 AI 团队中则以会话为单位发生。**过去被等待确认所占据的时间，如今可以转投到别的创造之中。**

## 为什么此法奏效——AI 与人的特性差异

| 观点 | 人类团队 | AI 团队 |
|---|---|---|
| 上下文丢失速度 | 数日至数周 | 数小时至数次会话 |
| 返工成本 | 高（时间 + 动力） | 低（即时再生成） |
| 休息必要性 | 必须 | 零 |
| 问责说明 | 语言化耗时 | 经由 audit log 自动追踪 |

→ **AI 是少数能成立「等待确认的成本 > 即便略有偏差也推进的价值」的劳动者。** 正因如此，管理书籍中「定义结果 + 委以判断」的手法才如此契合。

## 管理者绝不能放手的东西

「三自精神」与「定义结果 + 交给它」是朝着放手的方向，但有**四样绝不能放手**：

1. **需求的质量**——立即判定「这是把需求与解法混为一谈」并下令重写
2. **架构判断**——立即否决 AI 提出的实现方案，「这违反了独立性原则」
3. **honest disclosure**——基准出现伪性能时立即看穿，「这是 echo back 的效果」
4. **质量闸门**——用模式识别指出，「别写成 lllive（三个 L）的拼写错误」

也就是说，**第一大脑（30 年经验）必须作为判断闸门持续在场**。委以，但非放任。

## 总结

「在需求消化完之前持续追加」这一 AI 开发的优势，唯有在 AI 自律行动的条件下才成立。为满足该条件：

- 给 AI 套上佳能「三自精神」（自发・自治・自立）
- 把管理书籍（Buckingham & Coffman 等）的手法直接移植
- 「定义结果 + 委以判断 + 专注长处 + 以最少确认推进」

由此，单人开发便接近团队速度。如果说前一篇文章 [15] 是「第二大脑」的**构建论**，那么本文便是其**运营论**。

llive 是采用 Apache 2.0 + Commercial 双重许可的 OSS，仓库为 https://github.com/furuse-kazufumi/llive 。对本文 AI 管理手法感兴趣的朋友，欢迎在 Issue / Discussion 中讨论。

---

**本文是「第二大脑」系列的第 2 部（运营论）。**

**过往文章**:
- [14] 在 HTML 上看不见，机器却能读出——不可见注解通道设计
- [15] 30 年软件开发经验 + Perplexity + Claude Code + TRIZ + RAG =「第二大脑」（构建论）

## 参考文献 / 参考资源

### 佳能「三自精神」
- 佳能株式会社 官方企业理念页「佳能的企业 DNA」 — https://global.canon/ja/corporate/dna/
- 御手洗富士夫 著《佳能高收益复活的秘密》钻石社, 2001（三自精神的原典性解说）

### 管理书籍
- Marcus Buckingham & Curt Coffman, *First, Break All the Rules: What the World's Greatest Managers Do Differently*, Simon & Schuster, 1999
  - 日译: 宫本喜一 译《最优秀的领导者、管理者始终在思考的唯一一件事》日本经济新闻出版, 2006
  - （本文标题「持续产出压倒性成果的管理者最优先事项」亦属同一脉络，存在多个版本）
- Marcus Buckingham & Donald O. Clifton, *Now, Discover Your Strengths*, Free Press, 2001
  - 日译: 田口俊树 译《来吧，唤醒你的才能（你自己）》日本经济新闻出版, 2001

### Claude Code / AI 智能体运营
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Anthropic, *Building effective agents* (2024) — https://www.anthropic.com/research/building-effective-agents

### llive 相关
- llive 仓库 — https://github.com/furuse-kazufumi/llive
- 本文「一次会话 14 个功能 / 1270 PASS / 零回归」的依据: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`
- 前作「第二大脑 构建论」: [15]（同系列第 1 部）

---

# 한국어

# AI 에게 「삼자 정신」을 부과한다 — 압도적 성과를 계속 내는 매니저식 AI 운용론

> 📚 **연재 내비**: ← #15 「제2의 뇌」 개발론 ｜ **#16 본 기사** ｜ #17 인간과 AI 의 융합 비전 → ｜ [연재 LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ 각 기사는 단독으로도 읽을 수 있습니다（링크는 회유용）.

**한 줄 hook**:
요건을 **다 소화하기 전에 다음 요건을 계속 쌓아 올릴 수 있다**. 이는 인간 팀에서는 파탄 나지만 AI 개발에서는 우위가 된다. 조건은 단 하나 — AI 가 **자율적으로 움직여 주는** 것. 캐논이 내건 「삼자 정신」과 Buckingham & Coffman 등의 매니지먼트 서적이 거의 그대로 전용된다.

---

## 기점 — 요건은 멈추지 않는다

llive 개발의 이번 세션（2026-05-17）을 예로 든다.

| 시각 | 일어난 일 |
|---|---|
| 시작 | 요건: COG-04 + CREAT-04 통합 |
| +1h | 추가 요건: 「9 인자 전부 넣으면 본격적으로 동작 확인」 |
| +2h | 추가 요건: 오카 기요시 선생의 사상에서 배운다（OKA-FX 10 건, 경의를 담아 명명） |
| +3h | 추가 요건: LinkedIn 피드백（IND-FX） |
| +4h | 추가 요건: 철저한 벤치마크（12 계통） |
| +5h | 추가 요건: Anthropic key 복구 → 다른 LLM 비교 |
| +6h | 추가 요건: Qwen 탈피 / VLM 미래 / lllive 스펠링 |
| +7h | 추가 요건: 개발 스타일 언어화（기사화） |
| +8h | 추가 요건: 삼자 정신 + 매니지먼트 서적（본 기사） |

인간 팀이라면 어딘가에서 「더 이상 요건 넣지 마세요」라는 비명이 터져 나온다. AI 개발에서는 **전부 소화해 내고, 1270 PASS / 회귀 제로** 로 안착했다.

## 왜 이것이 우위인가

인간 팀의 1 사이클 = 수일〜수주（요건 → 설계 → 구현 → 테스트 → 검수）. 도중에 요건을 추가하면 진행이 멈춘다. AI 개발에서는:

- 1 사이클 = **수분〜수시간**（스파이럴 개발）
- 다 소화하기 전에 추가해도 다음 사이클에서 자연히 흡수된다
- 필자의 「떠오른 생각」이 **그대로 요건이 될 수 있는 속도**

요건 정의를 「언제 닫을지」 고민할 필요가 없다. **언제든 열고, 언제든 닫는다.** 이는 인간 팀이 흉내 낼 수 없는 「AI 만의 개발 스타일」이다.

## 다만 조건 — AI 가 자율적으로 움직일 것

요건을 계속 쌓아도 좋지만, AI 가 일일이 「이거 진행해도 되나요」 「다음은 뭘 할까요」라고 물어 오면 즉시 파탄 난다. 매니저（= 필자）의 머리가 늘 컨텍스트 스위치에 빼앗긴다.

이를 푸는 열쇠가 **캐논 「삼자 정신」** 의 AI 적용이다.

| 자(自) | 의미（캐논 원전） | AI 적용 |
|---|---|---|
| **자발** | 스스로 나서서 행동한다 | 인간의 지시는 「종료 조건」만, 우선순위는 AI 가 결정 |
| **자치** | 스스로 관리한다 | AI 가 자신의 TaskCreate / TaskUpdate 를 돌려 진척 관리 |
| **자립** | 스스로 판단한다 | 불필요한 확인을 생략하고, 명확한 선택지 + 추천으로 진행 |

캐논 미타라이 후지오 씨가 경영 이념으로 내건 「삼자 정신」은 본래 **인간 사원의 주체성 육성** 용이지만, 이것이 그대로 AI 세션의 설계 원칙이 된다.

### ☕ 여담 — 「삼자」를 AI 에게 말하게 하면 어떻게 되나

ChatGPT 나 Claude 에게 「캐논의 삼자 정신이란?」이라고 물으면 거의 정확한 답이 돌아온다. 그런데 「이걸 AI 자신에게 적용하면 어떻게 되나?」라고 이어서 물으면 갑자기 **「저는 어디까지나 도구라서…」** 라며 겸손 모드에 들어간다. AI 에게 자율을 요구한다면 **프롬프트로 AI 쪽의 겸손을 해제하는** 것에서 시작된다.

## 매니지먼트 서적에서의 전용

『먼저, 모든 규칙을 깨라: 세계 최고의 매니저들이 다르게 하는 것』（Marcus Buckingham & Curt Coffman 계열） 등의 매니지먼트 서적이 공통으로 설파하는 4 가지 실천은, AI 매니지먼트에 그대로 적용할 수 있다.

| 서적의 원칙 | 인간 매니저 | AI 매니저（필자의 운용） |
|---|---|---|
| **Select for talent** | 적재적소, 강점으로 사람을 고른다 | Opus 4.7 을 고른다, Brief 파이프라인 중 각 stage 에 최적 component 를 attach |
| **Define the right outcomes** | 결과를 정의, 과정을 묶지 않는다 | `/goal` 로 종료 조건만 지시, 우선순위는 AI 에 맡긴다 |
| **Focus on strengths** | 약점 개선보다 강점 발휘 | mock 이 불필요한 곳에선 LLM 사용, deterministic 으로 되는 곳은 그렇게 한다（Strategy 주입） |
| **Find the right fit** | 역할의 최적 배치 | Brief / OKA / VRB / MATH 를 기능별로 module 분리, Annotation 으로 연계 |

이를 한 문장으로 요약하면:

> **「결과를 정의하고, 판단을 위임하고, 강점에 집중하고, 최소한의 확인으로 진행한다」**

인간→인간으로도 유효하지만, 인간→AI 에서는 **특히 잘 듣는다**.

## 적용하고 있는 구체 테크닉

필자가 이번 세션에서 쓰고 있는 테크닉:

### 1. `/goal` 기능으로 종료 조건만 지시
Claude Code 에는 Stop hook 이라는 구조가 있어, `/goal` 로 설정한 조건이 달성될 때까지 세션이 멈추지 않는다. 「벤치마크 1.5h 로」 「요건 잔여분 가능한 한 소화」처럼 **종료 조건만** 지정한다.

### 2. AskUserQuestion 으로 2-4 선택지 + 추천 제시
지시가 분기할 때, AI 가 **2-4 개의 구체적 선택지 + 추천안** 을 제시하는 구조를 쓴다. 인간은 고르기만 하면 판단 완료, AI 쪽은 추천으로 움직일 준비가 되어 있으므로 로스가 없다.

### 3. feedback memory 로 「다음에도 자율 판단하는 규칙」 축적
이번 세션에서 35 개 이상의 feedback memory 를 쌓았다. 예:
- 「진행할까요」는 최소화, 즉시 실행（`feedback_max_plan_autonomy`）
- 다음 지시 대기일 때는 선택지 제시（`feedback_offer_choices_when_idle`）
- 세션 마라톤 지속（`feedback_session_marathon`）
- 벤치에서 거짓 성능이 나오면 반드시 내역을 의심하라（`feedback_benchmark_honest_disclosure`）

이것들은 다음 세션에서 자동 참조되어, **매니저 지시 없이 AI 가 같은 판단 기준으로 움직인다**.

### 4. TaskCreate / TaskUpdate 로 AI 자신이 진척 관리
AI 가 스스로 태스크를 쪼개고, 상태（pending / in_progress / completed）를 갱신한다. 마이크로매니지먼트 불필요.

### 5. commit/push 는 명시적 확인
로컬 commit 은 AI 자율, push（remote 공개）는 명시 확인. CLAUDE.md 규칙으로 「파괴적 조작은 ASK FIRST」라고 명문화 완료.

### ☕ 덧붙여

필자가 `/goal` 을 처음 썼을 때, AI 가 묵묵히 1 시간 반 벤치를 계속 돌리는 것을 보고 「이건 방치해도 되는 녀석이다」라고 깨달았다. 매니저가 완전히 손을 뗄 수 있는 시간은 인간 팀에서는 한 달에 하루 정도지만, AI 팀에서는 세션 단위로 발생한다. **확인 대기로 빼앗기던 시간을 다른 창조에 돌릴 수 있다.**

## 왜 이 수법이 잘 듣는가 — AI 와 인간의 특성 차

| 관점 | 인간 팀 | AI 팀 |
|---|---|---|
| 문맥 손실 속도 | 수일〜수주 | 수시간〜수 세션 |
| 다시 하기 비용 | 높다（시간 + 동기） | 낮다（재생성 즉시） |
| 휴식 필요성 | 필수 | 제로 |
| 설명 책임 | 언어화에 시간 | audit log 로 자동 추적 |

→ **AI 는 「확인을 기다리는 비용 > 다소 어긋나도 진행하는 가치」가 성립하는 몇 안 되는 일꾼이다.** 그렇기에 「결과를 정의 + 판단을 위임한다」는 매니징 서적의 수법이 들어맞는다.

## 매니저가 놓아서는 안 되는 것

「삼자 정신」과 「결과 정의 + 맡긴다」는 놓는 방향이지만, **놓아서는 안 되는 4 가지** 가 있다:

1. **요건의 질** — 「이건 요건 vs 해법을 혼동하고 있다」고 즉시 판정해 재작성 지시
2. **아키텍처 판단** — AI 가 내놓은 구현안을 「이건 독립성 원칙에 반한다」고 즉시 거부
3. **honest disclosure** — 벤치에서 거짓 성능이 나왔을 때 「이건 echo back 의 효과」라고 즉시 간파
4. **품질 게이트** — 「lllive（L 3 개）의 오타를 쓰지 않도록」 패턴 인식으로 지적

즉 **제1의 뇌（30 년 경험）가 판단 게이트로 계속 자리하는** 것. 맡기되, 방임은 아니다.

## 정리

요건을 다 소화하기 전에 계속 추가할 수 있는 AI 개발의 우위는, AI 가 자율적으로 움직인다는 조건 아래서 비로소 성립한다. 그 조건을 충족하기 위해:

- 캐논 「삼자 정신」（자발・자치・자립）을 AI 에게 부과한다
- 매니지먼트 서적（Buckingham & Coffman 등）의 수법을 그대로 전용한다
- 「결과를 정의 + 판단을 위임 + 강점에 집중 + 최소 확인으로 진행」

이로써 1 인 개발이 팀 속도에 가까워진다. 앞 기사 [15] 가 「제2의 뇌」의 **구축론** 이었다면, 본 기사는 그 **운용론** 에 해당한다.

llive 는 Apache 2.0 + Commercial 듀얼 라이선스의 OSS, Repo 는 https://github.com/furuse-kazufumi/llive . 본 기사의 AI 매니지먼트 수법에 관심 있는 분은 Issue / Discussion 에서 논의하고 싶다.

---

**본 기사는 「제2의 뇌」 시리즈의 제 2 부（운용론）.**

**과거 기사**:
- [14] HTML 에서는 보이지 않는데, 기계로는 읽을 수 있다 — 비가시 어노테이션 채널 설계
- [15] 30 년의 소프트웨어 개발 경험 + Perplexity + Claude Code + TRIZ + RAG = 「제2의 뇌」（구축론）

## 참고 문헌 / 참고 리소스

### 캐논 「삼자 정신」
- 캐논 주식회사 공식 기업 이념 페이지 「캐논의 기업 DNA」 — https://global.canon/ja/corporate/dna/
- 미타라이 후지오 저 『캐논 고수익 부활의 비밀』 다이아몬드사, 2001（삼자 정신의 원전적 해설）

### 매니지먼트 서적
- Marcus Buckingham & Curt Coffman, *First, Break All the Rules: What the World's Greatest Managers Do Differently*, Simon & Schuster, 1999
  - 일역: 미야모토 기이치 역 『최고의 리더, 매니저가 늘 생각하는 단 하나의 것』 일본경제신문출판, 2006
  - （본 기사 제목의 「압도적 성과를 계속 내는 매니저의 최우선 사항」도 같은 계열의 표현으로 여러 판이 있음）
- Marcus Buckingham & Donald O. Clifton, *Now, Discover Your Strengths*, Free Press, 2001
  - 일역: 다구치 도시키 역 『자, 재능(자신)에 눈뜨자』 일본경제신문출판, 2001

### Claude Code / AI 에이전트 운용
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Anthropic, *Building effective agents* (2024) — https://www.anthropic.com/research/building-effective-agents

### llive 관련
- llive 리포지토리 — https://github.com/furuse-kazufumi/llive
- 본 기사의 「1 세션 14 기능 / 1270 PASS / 회귀 제로」의 근거: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`
- 전작 「제2의 뇌 구축론」: [15]（동 시리즈 제 1 부）
