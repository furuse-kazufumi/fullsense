---
title: 'AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制と検証規律'
tags:
  - FullSense
  - AIエージェント
  - 開発手法
  - ClaudeCode
  - Codex
private: true
updated_at: '2026-05-25'
id: 71c2304718ad5829d2d7
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

> ⚠ 本記事は **ja 骨子ドラフト**（蓄積目的・完璧不要）。en/zh/ko 展開は後続。投稿前に hero/theme SVG・進捗 badge・関連記事の Qiita URL cross-link を埋める。

# 日本語

# AI に AI を部下として使わせる #31 — Claude 主導 + Codex 配下の「二本柱」開発体制

> **コンセプト hook**: FullSense（llmesh / llive / llove）は私ひとりの個人開発です。でも実態は
> 「ひとり」ではない。**AI コーディングエージェントを主・別の AI エージェントを部下**にした
> 2 階層の開発体制が回っています。主が **Claude Code**、部下が **Codex CLI**。
> 「AI が AI に仕事を振って、その成果を AI が検証する」——この多重委任を、暴走させずに
> どう規律するか。本記事は人間 1 + AI 2 の「二本柱」運用の実践記です。
>
> キーワードは **オーケストレータ / 配下 worker / 検証規律 / 並列化**。

---

## 0. 三行であらすじ

- **Claude = オーケストレータ**（計画・実装・委任・**検証**）/ **Codex = 配下 worker**（実行・レビュー・調査）。
- 「二本柱」= 対等ではなく **Claude 主導 + Codex 配下**。司令塔は 1 つに保つ。
- 鉄則: **外部 AI の finding は実コード / 一次情報で 1 件ずつ検証してから採用**（鵜呑み禁止）。

---

## 1. なぜ「二本柱」なのか — 動機

個人開発で AI エージェントを 1 つだけ使うのは、もはや普通です。なぜ 2 つ目（Codex）を**部下として**足したのか:

1. **ベンダー分散・冗長性** — 単一エージェントの課金変更 / 障害 / quota 枯渇のヘッジ。
2. **クロスレビュー** — 同じ設計を別系統の AI に見せ、セカンドオピニオンを取る（盲点削減）。
3. **並列 worker** — 独立サブタスクを配下に投げ、主は最重要タスクに集中。

> 🍵 **休憩ポイント**: 「AI を 2 つ使う = 2 倍賢い」ではありません。**指揮系統を 1 つに保つ**のが肝。
> 烏合の衆にすると、むしろ遅くなる。本記事の半分は「どう統制するか」の話です。

---

## 2. 役割分担 — オーケストレータと配下 worker

![人間→Claude（主＝オーケストレータ）→Claude サブエージェント並列 / Codex CLI 配下 worker の階層図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy.svg)

- **Claude（主）の責務**: タスク分解・依存性判定・独立タスクの並列起動・進捗監視・**成果の検証**・一括コミット。
- **Codex（配下）の責務**: 委任された範囲の実行。非対話委任 = `codex exec -s read-only "<prompt>"`。
- **司令塔は常に Claude**。Codex は Claude を経由してしか全体に影響しない（直接コミットさせない）。

**節の肉付け予定**: Claude サブエージェント並列（[[feedback_parallel_first_execution]]）と Codex 配下委任の
使い分け表。「同 file は直列・独立 file は並列」「git 操作は orchestrator が一括」（[[feedback_agent_no_git_parallel]]）。

---

## 3. 検証規律 — 「鵜呑み禁止」が体制の生命線

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

## 4. 並列化の作法 — 暴走させない統制

複数 worker（Claude サブエージェント + Codex）を同時に回すときの規律:

- **2〜4 並列が安全圏**（主の context 余裕・コミット衝突なし）。5+ は file レベル独立性を厳格管理。
- **独立タスク抽出** = 依存なし + file / module / repo レベルで非接触。同 file は直列（file lock 的）。
- **不可逆操作（削除 / push / submodule 改変）は 1 件ずつ人間確認**。配下に勝手にやらせない。
- **git 操作は orchestrator が一括**。並列 worker には git を触らせない（競合回避）。

> 🍵 **休憩ポイント**: 「AI をたくさん並べれば速い」の罠。**主の context（注意の総量）が律速**です。
> 5 体並列にしても主が捌けなければ意味がない。脳のワーキングメモリと同じで、同時把握できる数には上限がある。

---

## 5. アンチパターン（やってはいけない）

- 「1 つずつ確認しながら進めます」と宣言してから黙々と直列実行（並列化の機会損失）
- 配下に投げず主の context だけで全部こなす（context 爆発）
- 並列起動した worker の結果を待たずに主が同じ file を触る（競合）
- 2 worker に同じ file を書かせる委任（独立性の判定漏れ）
- 配下 AI の finding を無検証で設計や実装に採用（誤り増幅 = 二本柱最大の事故）

---

## 6. この体制で実際に何が回ったか（FullSense の実例）

- **設計クロスレビュー**: 進化設計 / 要件 / PoC を配下にレビューさせ、主が実コードで検証して採用判断。
- **既存資産調査**: lldarwin の既存部品（loop.py / mating.py / nsga2.py 等）の所在を配下に調査 → 主が確認。
- **並列サブタスク**: 記事骨子・コード調査・要件整理を独立タスクとして並列化（本連載自体がその産物）。

> 🍵 **休憩ポイント**: 「人間 1 + AI 2」で個人開発の生産性がどう変わったか、という主観も最後に正直に。
> 速くなった面（並列・冗長性）と、増えた負荷（検証コスト・統制コスト）の**両方**を honest disclosure。

---

## 7. 教訓

- **指揮系統は 1 つに保つ。** 二本柱は対等でなく主従。司令塔の分裂は事故のもと。
- **検証規律が体制の生命線。** AI が AI を無検証で信じる連鎖が最大のリスク。
- **並列度は主の context が律速。** 体数でなく捌ける量で決める。
- **不可逆操作と git は人間 / orchestrator が握る。** 配下には可逆な仕事だけ任せる。

> **次回予告**: 二本柱で回した進化設計（#26 lldarwin）を、配下 Codex + on-prem ollama で
> Stage 2（実 LLM 評価）まで進める。多重 AI 委任が「研究の実装速度」をどこまで上げるか。

---

## 8. 関連
- 連載 #26「lldarwin の設計」— 本体制で回した実例
- 関連 memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #26 の Qiita URL cross-link / en・zh・ko 版展開 -->
<!-- KEY MESSAGE: 人間1 + AI2 の二本柱。Claude 主導 + Codex 配下。検証規律(鵜呑み禁止)が生命線。並列度は主の context が律速。 -->
<!-- NOTE(事実整合): Codex は ChatGPT Pro $100/月で契約方針(promo 〜5/31)。導入状態(CLI 0.117.0 / quota 枯渇 / login 切替予定)は reference_codex_two_pillar 準拠。実応答未取得の段階である旨に注意して脚色しないこと。 -->

---

# English

# Making an AI Use an AI as Its Subordinate #31 — The "Two Pillars" Development Model of Claude as Lead + Codex as Subordinate

> **Concept hook**: FullSense (llmesh / llive / llove) is a solo project built by me alone. But the reality is
> that it is not really "solo." A **two-tier development model — with one AI coding agent as the lead and another AI agent as its subordinate** —
> is what keeps things running. The lead is **Claude Code**, the subordinate is **Codex CLI**.
> "An AI hands work to another AI, and an AI verifies the result" — how do you keep this multi-layered
> delegation disciplined so it doesn't go off the rails? This article is a field report on running a "two pillars" setup of 1 human + 2 AIs.
>
> The keywords are **orchestrator / subordinate worker / verification discipline / parallelization**.

---

## 0. The Story in Three Lines

- **Claude = orchestrator** (planning, implementation, delegation, **verification**) / **Codex = subordinate worker** (execution, review, investigation).
- "Two pillars" does NOT mean peers — it means **Claude leads, Codex follows**. Keep the chain of command singular.
- Iron rule: **Never adopt an external AI's findings without verifying each one, one at a time, against actual code / primary sources** (no taking things on faith).

---

## 1. Why "Two Pillars" — The Motivation

In solo development, using just one AI agent is already commonplace. So why did I add a second one (Codex) **as a subordinate**?

1. **Vendor diversification & redundancy** — a hedge against a single agent's pricing changes / outages / quota exhaustion.
2. **Cross-review** — show the same design to an AI of a different lineage and get a second opinion (reducing blind spots).
3. **Parallel workers** — throw independent sub-tasks at the subordinate so the lead can concentrate on the most critical task.

> 🍵 **Break point**: "Using two AIs = twice as smart" is false. The key is to **keep the chain of command singular**.
> Turn it into a rabble and it actually gets slower. Half of this article is about "how to keep it under control."

---

## 2. Division of Roles — Orchestrator and Subordinate Worker

![Hierarchy: Human → Claude Code (lead = orchestrator) → Claude sub-agents in parallel / Codex CLI as subordinate worker](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy_en.svg)

- **Claude's (the lead's) responsibilities**: task decomposition, dependency assessment, parallel launch of independent tasks, progress monitoring, **verification of results**, and batch commits.
- **Codex's (the subordinate's) responsibilities**: executing the delegated scope. Non-interactive delegation = `codex exec -s read-only "<prompt>"`.
- **The chain of command is always Claude.** Codex only influences the whole through Claude (it is never allowed to commit directly).

**Section to be fleshed out**: a usage table contrasting Claude sub-agent parallelism ([[feedback_parallel_first_execution]]) and Codex subordinate delegation.
"Same file = serial, independent files = parallel," "git operations are batched by the orchestrator" ([[feedback_agent_no_git_parallel]]).

---

## 3. Verification Discipline — "No Taking Things on Faith" Is the Lifeline of the Model

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

## 4. The Etiquette of Parallelization — Control That Prevents Runaway Behavior

Discipline for when you run multiple workers (Claude sub-agents + Codex) at the same time:

- **2–4 in parallel is the safe zone** (the lead has context headroom, no commit conflicts). At 5+, strictly manage file-level independence.
- **Extracting independent tasks** = no dependencies + no contact at the file / module / repo level. The same file is serial (like a file lock).
- **Irreversible operations (deletion / push / submodule changes) require human confirmation one at a time.** Never let the subordinate do them on its own.
- **git operations are batched by the orchestrator.** Don't let parallel workers touch git (to avoid conflicts).

> 🍵 **Break point**: The trap of "the more AIs you line up, the faster it goes." **The lead's context (its total amount of attention) is the rate-limiting factor.**
> Even with 5 running in parallel, it's meaningless if the lead can't process them. Just like the brain's working memory, there is an upper limit to how many things can be grasped at once.

---

## 5. Anti-Patterns (Things You Must Not Do)

- Declaring "I'll proceed checking one at a time" and then silently executing serially (a lost opportunity for parallelization).
- Not delegating to the subordinate and doing everything within the lead's context alone (context explosion).
- The lead touching the same file before waiting for the results of workers launched in parallel (conflict).
- Delegating two workers to write the same file (a failure to judge independence).
- Adopting a subordinate AI's findings into the design or implementation without verification (error amplification = the biggest accident in the two-pillar model).

---

## 6. What Actually Got Done With This Model (Real FullSense Examples)

- **Design cross-review**: had the subordinate review the evolutionary design / requirements / PoC, and the lead verified against actual code to decide on adoption.
- **Existing-asset investigation**: had the subordinate investigate the whereabouts of lldarwin's existing components (loop.py / mating.py / nsga2.py, etc.) → the lead confirmed.
- **Parallel sub-tasks**: parallelized article outlines, code investigation, and requirements organization as independent tasks (this very series is a product of that).

> 🍵 **Break point**: I'll also be honest at the end about my subjective sense of how "1 human + 2 AIs" changed solo-development productivity.
> Honest disclosure of **both** the aspects that got faster (parallelism, redundancy) and the load that increased (verification cost, control cost).

---

## 7. Lessons

- **Keep the chain of command singular.** The two pillars are not peers but lead-and-follow. A split command center is the source of accidents.
- **Verification discipline is the lifeline of the model.** The chain of an AI believing another AI without verification is the greatest risk.
- **The degree of parallelism is rate-limited by the lead's context.** Decide by what you can process, not by headcount.
- **The human / orchestrator holds irreversible operations and git.** Entrust the subordinate only with reversible work.

> **Next time**: take the evolutionary design run with the two pillars (#26 lldarwin) and, using the subordinate Codex + an on-prem ollama,
> push it to Stage 2 (evaluation with a real LLM). How far does multi-layered AI delegation raise "the implementation speed of research"?

---

## 8. Related
- Series #26 "The Design of lldarwin" — a real example run with this model.
- Related memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

# 中文

# 让 AI 把 AI 当作下属来使用 #31 —— Claude 主导 + Codex 配属的「两根支柱」开发体制

> **概念钩子**：FullSense（llmesh / llive / llove）是我一个人的个人开发项目。但实际情况
> 并不真的是「一个人」。一套**以一个 AI 编码代理为主、以另一个 AI 代理为下属**的
> 两层开发体制正在运转。主为 **Claude Code**，下属为 **Codex CLI**。
> 「AI 把工作分派给 AI，再由 AI 来验证其成果」——如何让这种多重委派保持纪律、
> 不至于失控？本文是关于运行「1 个人 + 2 个 AI」这一「两根支柱」体制的实践记录。
>
> 关键词是 **编排者（orchestrator）/ 配属 worker / 验证纪律 / 并行化**。

---

## 0. 三行剧情简介

- **Claude = 编排者**（计划、实现、委派、**验证**）/ **Codex = 配属 worker**（执行、评审、调查）。
- 「两根支柱」并非对等，而是 **Claude 主导 + Codex 配属**。指挥系统要保持唯一。
- 铁律：**外部 AI 的 finding 必须先用实代码 / 一手信息逐条验证后才采用**（禁止盲信）。

---

## 1. 为什么是「两根支柱」—— 动机

在个人开发中，只用一个 AI 代理早已是常态。那么我为什么要加上第二个（Codex），**而且是作为下属**？

1. **厂商分散与冗余** —— 对冲单一代理的计费变更 / 故障 / quota 枯竭。
2. **交叉评审** —— 把同一份设计拿给另一系谱的 AI 看，获取第二意见（减少盲点）。
3. **并行 worker** —— 把独立子任务抛给下属，主则专注于最重要的任务。

> 🍵 **休息点**：「用两个 AI = 聪明两倍」是错的。关键在于**保持指挥系统的唯一性**。
> 若搞成乌合之众，反而会变慢。本文有一半是在讲「如何统制」。

---

## 2. 角色分工 —— 编排者与配属 worker

![层级图：人类 → Claude Code（主＝编排者）→ Claude 子代理并行 / Codex CLI 配属 worker](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy_zh.svg)

- **Claude（主）的职责**：任务分解、依赖性判定、独立任务的并行启动、进度监控、**成果验证**、统一提交（commit）。
- **Codex（下属）的职责**：执行被委派的范围。非交互式委派 = `codex exec -s read-only "<prompt>"`。
- **指挥系统始终是 Claude。** Codex 只能经由 Claude 才能影响整体（不让它直接 commit）。

**本节待充实的内容**：对比 Claude 子代理并行（[[feedback_parallel_first_execution]]）与 Codex 配属委派的
使用区分表。「同一 file 串行、独立 file 并行」「git 操作由 orchestrator 统一进行」（[[feedback_agent_no_git_parallel]]）。

---

## 3. 验证纪律 —— 「禁止盲信」是体制的命脉

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

## 4. 并行化的规矩 —— 不让它失控的统制

同时运转多个 worker（Claude 子代理 + Codex）时的纪律：

- **2～4 个并行是安全区**（主的 context 有余裕、无提交冲突）。5 个以上则要严格管理 file 级别的独立性。
- **抽取独立任务** = 无依赖 + 在 file / module / repo 级别互不接触。同一 file 串行（类似 file lock）。
- **不可逆操作（删除 / push / submodule 改动）逐条经人工确认。** 不让下属擅自去做。
- **git 操作由 orchestrator 统一进行。** 不让并行 worker 碰 git（规避冲突）。

> 🍵 **休息点**：「把 AI 摆得越多越快」是个陷阱。**主的 context（注意力的总量）才是限速因素。**
> 即便并行 5 个，若主处理不过来也毫无意义。和大脑的工作记忆一样，能同时把握的数量是有上限的。

---

## 5. 反模式（绝不可做的事）

- 宣布「我会逐个确认着推进」之后却默默地串行执行（错失了并行化的机会）。
- 不委派给下属，全部都在主的 context 里干（context 爆炸）。
- 在并行启动的 worker 出结果之前，主就去碰同一个 file（冲突）。
- 委派两个 worker 去写同一个 file（独立性判定的遗漏）。
- 不经验证就把下属 AI 的 finding 采用进设计或实现（错误放大 = 两根支柱体制中最大的事故）。

---

## 6. 这套体制实际运转出了什么（FullSense 的实例）

- **设计交叉评审**：让下属评审进化设计 / 需求 / PoC，主用实代码验证后做出采用判断。
- **既有资产调查**：让下属调查 lldarwin 既有部件（loop.py / mating.py / nsga2.py 等）的所在 → 主确认。
- **并行子任务**：把文章骨架、代码调查、需求整理作为独立任务并行化（本连载本身就是其产物）。

> 🍵 **休息点**：最后我也会诚实地谈谈，「1 个人 + 2 个 AI」让个人开发的生产力发生了怎样的主观变化。
> 对变快的方面（并行、冗余）与增加的负担（验证成本、统制成本）**两者**都做 honest disclosure。

---

## 7. 教训

- **保持指挥系统的唯一性。** 两根支柱并非对等，而是主从。指挥中心的分裂是事故之源。
- **验证纪律是体制的命脉。** AI 不经验证就相信 AI 的连锁，是最大的风险。
- **并行度由主的 context 限速。** 以能处理的量来决定，而非以个数。
- **不可逆操作与 git 由人类 / orchestrator 掌握。** 只把可逆的工作交给下属。

> **下回预告**：把用两根支柱运转出来的进化设计（#26 lldarwin），借助配属的 Codex + on-prem ollama，
> 推进到 Stage 2（用真实 LLM 评估）。多重 AI 委派究竟能把「研究的实现速度」提升到什么程度。

---

## 8. 相关
- 连载 #26「lldarwin 的设计」—— 用本体制运转出来的实例。
- 相关 memory：[[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

# 한국어

# AI 에게 AI 를 부하로 부리게 하기 #31 —— Claude 주도 + Codex 배속의 「두 기둥」 개발 체제

> **콘셉트 후크**: FullSense（llmesh / llive / llove）는 나 혼자만의 개인 개발입니다. 하지만 실태는
> 「혼자」가 아닙니다. **AI 코딩 에이전트를 주로, 또 다른 AI 에이전트를 부하로** 둔
> 2 계층 개발 체제가 돌아가고 있습니다. 주는 **Claude Code**, 부하는 **Codex CLI**.
> 「AI 가 AI 에게 일을 맡기고, 그 성과를 AI 가 검증한다」——이 다중 위임을, 폭주시키지 않고
> 어떻게 규율하는가. 본 글은 인간 1 + AI 2 의 「두 기둥」 운용에 관한 실천기입니다.
>
> 키워드는 **오케스트레이터 / 배속 worker / 검증 규율 / 병렬화**.

---

## 0. 세 줄 줄거리

- **Claude = 오케스트레이터**（계획·구현·위임·**검증**）/ **Codex = 배속 worker**（실행·리뷰·조사）.
- 「두 기둥」은 대등이 아니라 **Claude 주도 + Codex 배속**. 지휘 계통은 하나로 유지한다.
- 철칙: **외부 AI 의 finding 은 실제 코드 / 일차 정보로 한 건씩 검증한 뒤에 채용**（맹신 금지）.

---

## 1. 왜 「두 기둥」인가 —— 동기

개인 개발에서 AI 에이전트를 하나만 쓰는 것은 이미 평범합니다. 그렇다면 왜 두 번째（Codex）를 **부하로서** 더했는가:

1. **벤더 분산·이중화** —— 단일 에이전트의 과금 변경 / 장애 / quota 고갈에 대한 헤지.
2. **크로스 리뷰** —— 같은 설계를 다른 계통의 AI 에게 보여 주고 세컨드 오피니언을 받는다（사각지대 감소）.
3. **병렬 worker** —— 독립 서브태스크를 부하에게 던지고, 주는 가장 중요한 태스크에 집중.

> 🍵 **휴식 포인트**: 「AI 를 둘 쓰면 = 두 배 똑똑하다」는 거짓입니다. 핵심은 **지휘 계통을 하나로 유지하는 것**.
> 오합지졸로 만들면 오히려 느려집니다. 본 글의 절반은 「어떻게 통제하는가」에 관한 이야기입니다.

---

## 2. 역할 분담 —— 오케스트레이터와 배속 worker

![계층도: 인간 → Claude Code（주＝오케스트레이터）→ Claude 서브에이전트 병렬 / Codex CLI 배속 worker](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy_ko.svg)

- **Claude（주）의 책무**: 태스크 분해·의존성 판정·독립 태스크의 병렬 기동·진척 모니터링·**성과 검증**·일괄 커밋.
- **Codex（부하）의 책무**: 위임된 범위의 실행. 비대화형 위임 = `codex exec -s read-only "<prompt>"`.
- **지휘 계통은 항상 Claude.** Codex 는 Claude 를 경유해서만 전체에 영향을 준다（직접 커밋시키지 않는다）.

**이 절에서 살을 붙일 예정**: Claude 서브에이전트 병렬（[[feedback_parallel_first_execution]]）과 Codex 배속 위임의
구분 사용 표. 「같은 file 은 직렬·독립 file 은 병렬」「git 조작은 orchestrator 가 일괄」（[[feedback_agent_no_git_parallel]]）.

---

## 3. 검증 규율 —— 「맹신 금지」가 체제의 생명선

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

## 4. 병렬화의 작법 —— 폭주시키지 않는 통제

여러 worker（Claude 서브에이전트 + Codex）를 동시에 돌릴 때의 규율:

- **2～4 병렬이 안전권**（주의 context 여유·커밋 충돌 없음）. 5+ 는 file 레벨 독립성을 엄격 관리.
- **독립 태스크 추출** = 의존 없음 + file / module / repo 레벨에서 비접촉. 같은 file 은 직렬（file lock 적）.
- **불가역 조작（삭제 / push / submodule 개변）은 한 건씩 인간 확인.** 부하에게 멋대로 시키지 않는다.
- **git 조작은 orchestrator 가 일괄.** 병렬 worker 에게 git 을 만지게 하지 않는다（충돌 회피）.

> 🍵 **휴식 포인트**: 「AI 를 많이 늘어놓으면 빠르다」의 함정. **주의 context（주의의 총량）가 율속(律速)입니다.**
> 5 체 병렬로 해도 주가 처리하지 못하면 의미가 없습니다. 뇌의 작업 기억과 마찬가지로, 동시에 파악할 수 있는 수에는 상한이 있습니다.

---

## 5. 안티패턴（해서는 안 되는 것）

- 「하나씩 확인하면서 진행하겠습니다」라고 선언한 뒤 묵묵히 직렬 실행（병렬화의 기회 손실）.
- 부하에게 던지지 않고 주의 context 만으로 전부 해치운다（context 폭발）.
- 병렬 기동한 worker 의 결과를 기다리지 않고 주가 같은 file 을 만진다（충돌）.
- 2 worker 에게 같은 file 을 쓰게 하는 위임（독립성 판정 누락）.
- 부하 AI 의 finding 을 무검증으로 설계나 구현에 채용（오류 증폭 = 두 기둥 체제 최대의 사고）.

---

## 6. 이 체제로 실제로 무엇이 돌았는가（FullSense 의 실례）

- **설계 크로스 리뷰**: 진화 설계 / 요건 / PoC 를 부하에게 리뷰시키고, 주가 실제 코드로 검증해 채용 판단.
- **기존 자산 조사**: lldarwin 의 기존 부품（loop.py / mating.py / nsga2.py 등）의 소재를 부하에게 조사 → 주가 확인.
- **병렬 서브태스크**: 기사 골자·코드 조사·요건 정리를 독립 태스크로서 병렬화（본 연재 자체가 그 산물）.

> 🍵 **휴식 포인트**: 「인간 1 + AI 2」로 개인 개발의 생산성이 어떻게 바뀌었는가, 라는 주관도 마지막에 정직하게.
> 빨라진 면（병렬·이중화）과 늘어난 부하（검증 비용·통제 비용）의 **양쪽**을 honest disclosure.

---

## 7. 교훈

- **지휘 계통은 하나로 유지한다.** 두 기둥은 대등이 아니라 주종. 사령탑의 분열은 사고의 근원.
- **검증 규율이 체제의 생명선.** AI 가 AI 를 무검증으로 믿는 연쇄가 최대의 리스크.
- **병렬도는 주의 context 가 율속.** 체수가 아니라 처리할 수 있는 양으로 정한다.
- **불가역 조작과 git 은 인간 / orchestrator 가 쥔다.** 부하에게는 가역적인 일만 맡긴다.

> **다음 회 예고**: 두 기둥으로 돌린 진화 설계（#26 lldarwin）를, 배속 Codex + on-prem ollama 로
> Stage 2（실제 LLM 평가）까지 진행한다. 다중 AI 위임이 「연구의 구현 속도」를 어디까지 끌어올리는가.

---

## 8. 관련
- 연재 #26 「lldarwin 의 설계」—— 본 체제로 돌린 실례.
- 관련 memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

<!-- NAV -->
---
**FullSense KB ナビ**: [← #30 進化を「見せる」技術の系譜 #30 — Conw](https://fullsense.qiita.com/furuse-kazufumi/items/0e221d447b7a8ad66d22) ・ [📑 目次](https://fullsense.qiita.com/furuse-kazufumi/items/1ad8db4b854194e2d215) ・ [#32 llcore — Transformer のコア →](https://fullsense.qiita.com/furuse-kazufumi/items/88ed294aa107330c6894)
<!-- /NAV -->


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
