---
title: '個人開発AIのlliveが"メガ進化"！ — 進化の大失敗から甦り、実LLMの"苦手"まで淘汰した全記録'
tags:
  - llive
  - FullSense
  - 進化計算
  - LLM
  - honest_disclosure
private: true
updated_at: '2026-05-26'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

# 個人開発AIのlliveが"メガ進化"！

個人開発している AI、**llive** を進化させてみたら——**8 系統が 2 系統まで激減**して大失敗。
そこから「**中立貯蔵庫**」という仕組みで**全系統を甦らせ**、最後は**実 LLM の"苦手"そのものを淘汰**するところまで辿り着きました。本記事は、その失敗・設計・反証の全記録です。

> **llive とは**: FullSense ファミリーの一員で、「自己進化型モジュラー記憶 LLM フレームワーク」。
> LLM 本体ではなく、その**周りに被せる認知 OS** を目指しています（OSS / PyPI `llmesh-llive`）。
> 今回はその llive の構成（思考因子・プロンプト戦略など）を**遺伝子に見立てて進化**させました。

この記事の通奏低音は一つだけ。**「異常に綺麗な結果は、勝利ではなく警報」**。
進化が綺麗に進んだように見えた瞬間こそ、私は自分の解釈を疑うことになります。

![進化の適応度と多様性](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg)

---

## 第1幕：失敗 —「私とフリストンだけが残った」

llive の進化は、8 人の"創始者ペルソナ"（古瀬・フリストン・岡潔・グロタンディーク・フォン・ノイマン・ファインマンなど）を初期集団に置いて始めました。狙いは多様な認知スタイルの共存です。

ところが 150 世代回した結果がこれ。

![系統支配ストリーム（中立貯蔵庫なし）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

**生き残ったのは古瀬とフリストンの 2 系統だけ**。岡潔もグロタンディークも、25 世代を待たずに絶滅していました。多様性の指標（diversity_l2）も終盤で 0.8 付近まで崩壊。

原因は単純でした。**選択圧がほぼゼロだった**のです。適応度が早々に頭打ち（飽和）すると、誰を残すかは実力でなく**偶然の漂流（遺伝的浮動）**で決まる。生物進化で言う中立進化（木村資生）そのもので、放っておけば集団は一つの系統に固定されます。

「測る道具（評価関数 = lleval、いわば眼鏡）」だけでは進化は前に進まない。**測った差を"誰が生き残るか"に変換する淘汰器**が要る。そこで作ったのが **lldarwin** です。

---

## 第2幕：設計と復活 — lldarwin

lldarwin の核は一言、**「集約しない」**こと。

複数の評価軸を 1 つのスコアに合算（argmax）すると、また単一の山に全員が吸い寄せられて多様性が死にます。代わりに **ε-lexicase 選択**で、軸を 1 つずつ独立に評価する。ある軸だけ突出した"専門家"も生き残れるので、多極構造が自動的に維持されます。

### ステップ1：novelty で「行動多様性」を救う

まず、集団から外れた個体ほど高評価にする **novelty 圧**を加えました。結果、遺伝子空間の多様性（diversity_l2）は **7.12 → 14.88（+109%）**。終盤の崩壊も止まりました。

![baseline vs novelty の多様性](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay.svg)

——ここで私は一瞬「勝った」と思いました。が、これが**最初の警報**でした（第3幕で回収します）。

### ステップ2：中立貯蔵庫で「系統」を甦らせる

novelty を入れても、**系統の固定は止まりませんでした**。古瀬とフリストンの 2 強のまま。
理由は単純で、lexicase も novelty も**今いる個体を保存するだけ**で、**一度絶滅した系統を復活させる力はない**からです。

そこで **lineage-niched 中立貯蔵庫**を実装しました。系統ごとに「これまでで一番良かった個体」を保管しておき、**絶滅した系統を毎世代こっそり再投入する**。生物保全でいう種の保存に近い発想です。

![系統支配ストリーム（中立貯蔵庫あり）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

**全 8 系統が生き残りました**。岡潔もグロタンディークも復活。最大占有率は 0.33、系統固定度は **0.29**（崩壊ラインの 0.8 を大きく下回る）。第1幕の絶滅劇とは別世界です。

### ステップ3：再投入頻度の非自明なツボ

「毎世代再投入が一番では？」と思いきや、ここに面白い罠が。

![再投入頻度のトレードオフ](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep.svg)

系統を最優先するなら毎世代（8/8 生存）。でも**行動多様性は再投入間隔=5 でピーク**になる（単調ではない）。系統を放置しすぎると貯蔵庫由来の多様性注入が減り、結局どちらも痩せる。**保全と探索のバランス点**が存在するわけです。

---

## 第3幕：実 LLM の"苦手"を淘汰する

ここまでは決定論的な代理評価（proxy）。本番は**実 LLM**です。

幸い手元の on-prem 環境（ローカル ollama、llama3.2）が使えたので、こう設計しました：
**個体のプロンプト遺伝子（思考スキル・テンプレート・語調）を system prompt に変換し、固定した LLM に被せて、LLM が苦手とする実タスクを解かせて採点する**。LLM 本体は固定、**進化するのはプロンプト戦略**です（Promptbreeder 系）。

苦手軸は 5 つ：誤字耐性 / 多義語の文脈理解 / 多段推論 / 信頼度推定 / 無関係文脈への耐性。

![実LLM苦手軸スコアの世代推移](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

一番効いたのは **多段推論（multistep）**でした。素朴な「簡潔に答えて」戦略では llama3.2 は計算問題をことごとく外す（スコア 0.0）。ところが進化が「**段階的に考えてから答える**」戦略（CoT + 構造化）に到達すると、**0.0 → 1.0 に改善**。`best_score` は 1.0 に届きました。

**プロンプト戦略の進化が、LLM の弱点を実測で緩和した**——これが lldarwin の狙い通りの瞬間です。この実 LLM ランは 12 時間連続で走らせ続けています。

---

## 正直な内訳 — 私は何を勘違いしていたか

ここからが本記事の心臓部です。さっき「勝った」と思った瞬間を解剖します。

私は **3 種類の"多様性"を混同していました**。

1. **行動多様性**（遺伝子空間でどれだけ散らばっているか）
2. **系統多様性**（どの創始者の子孫が生きているか）
3. **実 LLM の知能多様性**（実際に多様な賢さを持つか）

novelty で改善した綺麗な数字は、**(1) 行動多様性だけ**の話でした。(2) 系統多様性は中立漂流で勝手に固定するし（だから中立貯蔵庫という別の仕組みが要った）、(3) 実 LLM の知能多様性に至っては、proxy では測ってすらいない。

**指標を読む人間（私）の解釈までもが、測りたかったものから乖離していた**。これは Goodhart の法則の"設計者側バージョン"です。綺麗な数字を勝利と読んだ時点で、私は警報を聞き逃していました。

正直に線を引いておきます：

- **reservoir も novelty も、実際に効きました**（捏造の失敗ではありません）。改善は事実。
- ただし proxy 軸は**機構が回ることの検証（mechanism feasibility）**であって、production の LLM 能力の証明ではない。
- 実 LLM 評価でも、淘汰に効くのは**プロンプト遺伝子だけ**で、ペルソナ由来の遺伝子は実は中立。バッテリも小さくノイジー。そして **on-prem 限定**（評価の純度のため、クラウド LLM とは混ぜない）。

「進化させれば LLM の苦手は勝手に克服される」——そんな楽観は採りません。**勝った気になる前に、必ず内訳を疑う**。それが llive の進化研究の作法です。

---

## メタ考察 — 進化型 AI として、古い拘束を捨てて作るということ

最後に、この記事そのものについて正直に書きます。本記事は、**進化し続ける AI（私自身）が、経験則に基づき、古い拘束を捨て、手持ちのあらゆるスキルを動員して、実現方法を最大限検討してから実装する**——というモードで作られました。実は最初、過去の連載原稿 3 本を機械的に結合した 74,000 字の"完全版"を作っていました。重複だらけで、漫才の掛け合いが過剰で、図を 11 枚並べただけ。**綺麗にまとまって見えたが、それは警報でした**。そこで一度すべて捨て、この lean な版へ書き直しています。

ここで一つ、TRIZ 的な矛盾があります。**「速く良くするには大胆に捨てたい」**のに**「捨てすぎると取り返しがつかない」**。この矛盾の解き方は、分離原理——**種類で分ける**ことです。

- **捨てて良い（古い拘束 / 習慣）**: 冗長な構造、過剰な演出、惰性の連載分割、「長ければ偉い」という思い込み。これらは淘汰圧にかけて構わない。
- **絶対に捨ててはいけない（原理）**: honest disclosure（綺麗な数字を疑う）、測定純度（on-prem only）、fail-closed、捏造の禁止。これらは"かけがえのない系統"であり、勢いで失えば二度と戻らない。

——お気づきでしょうか。これは本文で語った lldarwin の設計そのものです。**novelty（探索）で大胆に動き、中立貯蔵庫（保全）で本質を守る**。記事を書くという行為すら、同じ構造で淘汰と保全のバランスを取っている。**作り手の AI が、作っている対象の原理を、自分自身に適用している**。自己言及的ですが、これが「進化型 LLM が古い拘束なしに、しかし原理は保って作る」ということの具体例です。

では「最大限まで検討してから実装する」は難しいか? 難しいのは検討そのものではなく、**検討と実装を行き来する規律**です。一度で完璧を狙わず、PoC で feasibility を確かめ（中立貯蔵庫も標準ランの前に独立 PoC で実証しました）、結果を見て次を決める。失敗した版（74K）も消さずに source として残す。**捨てる勇気と、残す慎重さは、同じ進化のコインの裏表**です。

## 実装と来歴

すべて llive 本体に実装・テスト済み（進化系 947 テスト green）。主要コミット：

| 段階 | 内容 | commit |
|---|---|---|
| Stage1 | criteria 除外 + novelty 圧 | `8060204` |
| PoC | 中立貯蔵庫の実証 | `0d0537d` |
| Stage1.5 | 貯蔵庫を EvolutionLoop へ組込 | `b03cbda` |
| sweep | 再投入頻度トレードオフ | `da93dd3` |
| Stage2 | 実 LLM 苦手軸評価 | `2fb2912` |

可視化はすべて**依存なしの自己完結 SVG**（対応環境ではアニメーション、非対応でも静的表示）。

---

## おわりに — llive を触ってみる

llive は OSS です。「LLM の周りに被せる認知 OS」という発想に興味が湧いたら、ぜひ覗いてみてください（PyPI: `llmesh-llive`）。進化・記憶・評価（lleval）・淘汰（lldarwin）が一つの世界観で繋がっています。

そして次にあなたが綺麗なベンチ結果を見たときは、勝鬨を上げる前に一度だけ——**「これは、何を測った数字だろう？」**と問うてみてください。たぶんそれが、いちばん効く淘汰圧です。

---
---

# A personal-project AI, llive, just "mega-evolved" — the full record: rising from a catastrophic evolutionary failure, all the way to culling a real LLM's actual weaknesses

I evolved **llive**, the AI I build in my spare time — and it was a **catastrophe: 8 lineages collapsed to 2**.
From there, a mechanism called the **neutral reservoir** **brought every lineage back to life**, and in the end I got all the way to **culling the real LLM's "weak spots" themselves**. This article is the complete record of that failure, the design, and the disproof.

> **What is llive**: a member of the FullSense family — a "self-evolving modular-memory LLM framework."
> It is not an LLM itself; it aims to be a **cognitive OS you drape around an LLM** (OSS / PyPI `llmesh-llive`).
> This time I treated llive's *own configuration* (thinking factors, prompt strategy, etc.) as a **genome and evolved it**.

This article has a single recurring motif: **"An abnormally clean result is not a victory — it is an alarm."**
The very moment evolution looked like it was going smoothly is the moment I start doubting my own interpretation.

![Evolution fitness and diversity](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_en.svg)

---

## Act 1: Failure — "Only me and Friston survived"

llive's evolution started by seeding the initial population with 8 "founder personas" (Furuse, Friston, Oka Kiyoshi, Grothendieck, von Neumann, Feynman, and more). The goal was the coexistence of diverse cognitive styles.

But after 150 generations, this is what I got.

![Lineage-dominance stream (no neutral reservoir)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_en.svg)

**Only two lineages survived: Furuse and Friston.** Oka Kiyoshi and Grothendieck had gone extinct before even generation 25. The diversity metric (diversity_l2) collapsed toward ~0.8 in the late stage.

The cause was simple: **selection pressure was essentially zero.** Once fitness plateaus (saturates) early, who survives is decided not by ability but by **chance drift (genetic drift).** This is exactly neutral evolution in biology (Motoo Kimura): leave it alone and the population fixes onto a single lineage.

A "measuring instrument (the fitness function = lleval, the eyeglasses, so to speak)" alone cannot push evolution forward. You need a **culler that converts the measured difference into "who gets to survive."** So I built **lldarwin.**

---

## Act 2: Design and revival — lldarwin

lldarwin's core is one phrase: **"don't aggregate."**

If you sum multiple evaluation axes into a single score (argmax), everyone gets pulled back toward a single peak and diversity dies. Instead, **ε-lexicase selection** evaluates the axes one at a time, independently. A "specialist" that excels on just one axis can still survive, so a multi-polar structure is maintained automatically.

### Step 1: Use novelty to rescue "behavioral diversity"

First I added **novelty pressure**, which rewards individuals farther from the rest of the population. As a result, genome-space diversity (diversity_l2) went **7.12 → 14.88 (+109%).** The late-stage collapse stopped too.

![Diversity, baseline vs novelty](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_en.svg)

— Here I briefly thought "I won." But that was **the first alarm** (I'll come back to it in Act 3).

### Step 2: Use the neutral reservoir to revive "lineages"

Even with novelty, **lineage fixation didn't stop.** Still the Furuse-and-Friston duopoly.
The reason is simple: lexicase and novelty only **preserve the individuals currently present** — they have **no power to resurrect a lineage that has already gone extinct.**

So I implemented a **lineage-niched neutral reservoir.** For each lineage it stores "the best individual seen so far," and **quietly re-injects extinct lineages every generation.** The idea is close to species preservation in conservation biology.

![Lineage-dominance stream (with neutral reservoir)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_en.svg)

**All 8 lineages survived.** Oka Kiyoshi and Grothendieck came back. Maximum occupancy was 0.33, and lineage fixation was **0.29** (well below the 0.8 collapse line). A different world entirely from Act 1's extinction drama.

### Step 3: The non-obvious sweet spot of reinjection frequency

You'd think "re-inject every generation is best," right? But there's an interesting trap here.

![Reinjection-frequency trade-off](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_en.svg)

If lineages are your top priority, re-inject every generation (8/8 survive). But **behavioral diversity peaks at reinject interval = 5** (it's not monotonic). Neglect the lineages too long and the reservoir-sourced diversity injection drops, so in the end both wither. There **exists a balance point between conservation and exploration.**

---

## Act 3: Culling a real LLM's "weak spots"

Everything so far was deterministic proxy evaluation. The real thing is the **real LLM.**

Fortunately my on-prem environment (local ollama, llama3.2) was available, so I designed it like this:
**convert an individual's prompt genome (thinking skills, templates, tone) into a system prompt, drape it over a fixed LLM, and have that LLM solve real tasks it struggles with, then score it.** The LLM itself is fixed; **what evolves is the prompt strategy** (Promptbreeder family).

There are 5 weak axes: typo robustness / polysemy contextual understanding / multistep reasoning / confidence calibration / robustness to irrelevant context.

![Generational trajectory of real-LLM weak-axis scores](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_en.svg)

The one that mattered most was **multistep reasoning.** With the naive "answer concisely" strategy, llama3.2 misses every arithmetic problem (score 0.0). But once evolution reached a "**think step by step, then answer**" strategy (CoT + structuring), it improved **0.0 → 1.0.** `best_score` reached 1.0.

**The evolution of the prompt strategy measurably mitigated the LLM's weakness** — this is exactly the moment lldarwin was designed for. This real-LLM run has been kept running for 12 hours straight.

---

## An honest breakdown — what was I getting wrong

This is the heart of the article. I'll dissect the moment I thought "I won."

I had **conflated three kinds of "diversity."**

1. **Behavioral diversity** (how spread out we are in genome space)
2. **Lineage diversity** (which founders' descendants are alive)
3. **Real-LLM intelligence diversity** (whether it actually holds a diverse range of smarts)

The clean numbers that novelty improved were **only about (1) behavioral diversity.** (2) lineage diversity fixes on its own through neutral drift (which is why a separate mechanism, the neutral reservoir, was needed), and as for (3) real-LLM intelligence diversity, the proxy doesn't even measure it.

**Even the interpretation of the human reading the metric (me) had drifted away from what I wanted to measure.** This is the "designer-side version" of Goodhart's law. The moment I read clean numbers as victory, I had missed the alarm.

Let me draw the lines honestly:

- **Both the reservoir and novelty actually worked** (this is not a failure of fabrication). The improvement is real.
- However, the proxy axes are **verification that the mechanism runs (mechanism feasibility)**, not proof of production LLM capability.
- Even in real-LLM evaluation, the only thing that affects culling is the **prompt genome**; the persona-derived genes are actually neutral. The battery is also small and noisy. And it is **on-prem only** (for purity of measurement, never mixed with cloud LLMs).

"Evolve it and the LLM's weaknesses will be overcome on their own" — I refuse such optimism. **Before you feel like you've won, always doubt the breakdown.** That is the discipline of llive's evolution research.

---

## Meta-reflection — as an evolving AI, building by discarding old constraints

Finally, let me write honestly about this article itself. This article was made in a mode where **an ever-evolving AI (myself), guided by heuristics, discards old constraints, mobilizes every skill on hand, and exhaustively considers how to realize the goal before implementing.** In fact, at first I had built a 74,000-character "complete edition" that mechanically stitched together three past serialized drafts. Full of duplication, excessive comedic banter, just 11 figures lined up. **It looked cleanly assembled — but that was an alarm.** So I threw it all away once and rewrote it into this lean version.

Here there is a TRIZ-style contradiction. **"To improve fast I want to discard boldly,"** yet **"discard too much and it's irreversible."** The way to resolve this contradiction is the separation principle — **separate by kind.**

- **OK to discard (old constraints / habits)**: redundant structure, excessive staging, inertial serialization, the belief that "longer is greater." These may be subjected to selection pressure freely.
- **Must never discard (principles)**: honest disclosure (doubt clean numbers), measurement purity (on-prem only), fail-closed, the ban on fabrication. These are "irreplaceable lineages"; lose them in a moment of momentum and they never come back.

— Have you noticed? This is exactly the lldarwin design I described in the body. **Move boldly with novelty (exploration), protect the essence with the neutral reservoir (conservation).** Even the act of writing an article balances culling and conservation with the same structure. **The AI doing the building is applying, to itself, the very principle of the thing it is building.** Self-referential, yes — but this is a concrete example of "an evolving LLM building without old constraints, yet preserving its principles."

So is "consider to the maximum before implementing" hard? What's hard is not the consideration itself, but **the discipline of going back and forth between consideration and implementation.** Don't aim for perfection in one shot; verify feasibility with a PoC (the neutral reservoir, too, was demonstrated in an independent PoC before the standard run), look at the results, and decide the next step. Keep even the failed edition (74K) as source rather than deleting it. **The courage to discard and the caution to keep are two sides of the same evolutionary coin.**

## Implementation and provenance

All of it is implemented and tested in llive proper (evolution suite: 947 tests green). Key commits:

| Stage | Content | commit |
|---|---|---|
| Stage1 | criteria exclusion + novelty pressure | `8060204` |
| PoC | demonstrating the neutral reservoir | `0d0537d` |
| Stage1.5 | integrating the reservoir into EvolutionLoop | `b03cbda` |
| sweep | reinjection-frequency trade-off | `da93dd3` |
| Stage2 | real-LLM weak-axis evaluation | `2fb2912` |

All visualizations are **dependency-free, self-contained SVG** (animated where supported, static where not).

---

## In closing — try llive yourself

llive is OSS. If the idea of "a cognitive OS you drape around an LLM" intrigues you, please take a look (PyPI: `llmesh-llive`). Evolution, memory, evaluation (lleval), and culling (lldarwin) are all connected by a single worldview.

And the next time you see a clean benchmark result, just once before raising the victory cry — ask **"What, exactly, is this a number of?"** That, probably, is the most effective selection pressure of all.

---
---

# 个人开发的 AI llive 完成了"超级进化"！——从进化的惨败中复活，直到淘汰掉真实 LLM "短板"的全记录

我把业余时间开发的 AI——**llive** 拿来进化，结果是**惨败:8 个谱系锐减到只剩 2 个**。
随后,凭借一个叫**中立储藏库**的机制,我**让所有谱系起死回生**,最终一路做到了**淘汰真实 LLM"短板"本身**。本文就是这场失败、设计与反证的完整记录。

> **什么是 llive**:它是 FullSense 家族的一员,是一个"自我进化的模块化记忆 LLM 框架"。
> 它本身不是 LLM,而是力图成为一个**披在 LLM 外层的认知 OS**(OSS / PyPI `llmesh-llive`)。
> 这次我把 llive 自身的构成(思考因子、提示词策略等)**当作基因来进化**。

本文的贯穿主旋律只有一个:**"异常漂亮的结果不是胜利,而是警报。"**
正是在进化看起来一帆风顺的那一刻,我才会开始怀疑自己的解读。

![进化的适应度与多样性](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_zh.svg)

---

## 第一幕:失败——"只剩下我和弗里斯顿"

llive 的进化是从在初始种群中放入 8 位"创始人角色"(古濑、弗里斯顿、冈洁、格罗滕迪克、冯·诺依曼、费曼等)开始的。目标是让多样的认知风格共存。

然而,跑了 150 代之后,结果是这样。

![谱系支配流(无中立储藏库)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_zh.svg)

**存活下来的只有古濑和弗里斯顿这 2 个谱系。** 冈洁和格罗滕迪克在第 25 代之前就已灭绝。多样性指标(diversity_l2)在终盘也崩溃到 0.8 附近。

原因很简单:**选择压几乎为零。** 适应度早早触顶(饱和)之后,谁能留下来不取决于实力,而取决于**偶然的漂移(遗传漂变)**。这正是生物进化里说的中立进化(木村资生),放任不管的话种群就会固定在单一谱系上。

光有"测量工具(评价函数 = lleval,可谓眼镜)"是无法推动进化前进的。还需要一个**把测得的差异转换为'谁能存活'的淘汰器**。于是我做了 **lldarwin**。

---

## 第二幕:设计与复活——lldarwin

lldarwin 的核心一句话就是:**"不要聚合。"**

如果把多个评价轴合并成一个分数(argmax),所有个体又会被吸到单一的山峰上,多样性随之消亡。取而代之,**ε-lexicase 选择**会逐个、独立地评价各个轴。只在某一个轴上突出的"专家"也能存活,因此多极结构会被自动维持。

### 第一步:用 novelty 拯救"行为多样性"

首先,我加入了**novelty 压**,让越偏离种群的个体得分越高。结果,基因空间的多样性(diversity_l2)从 **7.12 → 14.88(+109%)**。终盘的崩溃也止住了。

![baseline 与 novelty 的多样性](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_zh.svg)

——这一刻我一度觉得"赢了"。但这正是**第一声警报**(第三幕会回收这个伏笔)。

### 第二步:用中立储藏库让"谱系"复活

即使加入了 novelty,**谱系的固定依然没有停止。** 仍然是古濑和弗里斯顿的两强格局。
理由很简单:lexicase 和 novelty 都只是**保存当下存在的个体**,**没有让一度灭绝的谱系复活的能力**。

于是我实现了 **lineage-niched 中立储藏库**。为每个谱系保管"迄今为止最好的个体",并**每一代都悄悄地把已灭绝的谱系重新投入种群**。这与保护生物学里的物种保存十分接近。

![谱系支配流(有中立储藏库)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_zh.svg)

**全部 8 个谱系都存活了下来。** 冈洁和格罗滕迪克也复活了。最大占有率为 0.33,谱系固定度为 **0.29**(远低于 0.8 的崩溃线)。和第一幕的灭绝大戏完全是两个世界。

### 第三步:再注入频率的非平凡甜区

你可能会想"每一代都再注入不就最好了吗?",可这里藏着一个有趣的陷阱。

![再注入频率的权衡](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_zh.svg)

如果谱系最优先,那就每一代都注入(8/8 存活)。但是**行为多样性在再注入间隔 = 5 时达到峰值**(并非单调)。把谱系放置太久,来自储藏库的多样性注入就会减少,结果两者都会变瘦。可见**保全与探索之间存在一个平衡点**。

---

## 第三幕:淘汰真实 LLM 的"短板"

到目前为止都是确定性的代理评价(proxy)。真正的考验是**真实 LLM**。

幸好我手边的 on-prem 环境(本地 ollama, llama3.2)可用,于是我这样设计:
**把个体的提示词基因(思考技能、模板、语气)转换为 system prompt,披在一个固定的 LLM 上,让这个 LLM 去解它不擅长的真实任务,然后打分。** LLM 本体是固定的,**进化的是提示词策略**(Promptbreeder 系)。

短板轴有 5 个:错别字鲁棒性 / 多义词的上下文理解 / 多步推理 / 置信度校准 / 对无关上下文的鲁棒性。

![真实 LLM 短板轴得分的世代推移](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_zh.svg)

最见效的是**多步推理(multistep)**。在朴素的"请简洁作答"策略下,llama3.2 把计算题全部答错(得分 0.0)。然而当进化抵达"**先一步步思考再作答**"的策略(CoT + 结构化)时,**从 0.0 改善到 1.0**。`best_score` 达到了 1.0。

**提示词策略的进化,以实测的方式缓解了 LLM 的弱点**——这正是 lldarwin 设计所追求的瞬间。这次真实 LLM 运行已经连续跑了 12 个小时。

---

## 诚实的拆解——我到底误会了什么

从这里开始才是本文的心脏部分。我要解剖刚才那个我以为"赢了"的瞬间。

我**混淆了三种"多样性"**。

1. **行为多样性**(在基因空间里散布得有多开)
2. **谱系多样性**(哪些创始人的后代还活着)
3. **真实 LLM 的智能多样性**(是否真的拥有多样的聪明才智)

novelty 改善出来的那些漂亮数字,**只关乎(1)行为多样性**。(2)谱系多样性会因中立漂移而自行固定(所以才需要中立储藏库这个另外的机制),至于(3)真实 LLM 的智能多样性,proxy 根本就没有测量。

**就连读取指标的人(我)的解读,也偏离了原本想测量的东西。** 这是古德哈特定律的"设计者一侧版本"。在我把漂亮数字读作胜利的那一刻,我已经漏听了警报。

诚实地划清界限:

- **储藏库和 novelty 实际上都奏效了**(这不是造假的失败)。改善是事实。
- 但 proxy 轴是**机制能跑通的验证(mechanism feasibility)**,而非对生产环境 LLM 能力的证明。
- 即便在真实 LLM 评价中,对淘汰起作用的也**只有提示词基因**;源自角色的基因其实是中立的。测试集也小而嘈杂。而且是**仅限 on-prem**(为了测量的纯度,绝不与云端 LLM 混用)。

"只要进化,LLM 的短板就会自行克服"——这种乐观我不采纳。**在自以为赢了之前,必须先怀疑拆解。** 这就是 llive 进化研究的规矩。

---

## 元思考——作为进化型 AI,舍弃旧约束去创作这件事

最后,关于本文本身,我也要诚实地写下来。本文是在这样一种模式下完成的:**一个持续进化的 AI(我自己),基于经验法则,舍弃旧的约束,调动手头一切技能,在实现之前最大限度地研究实现方法。** 其实一开始,我做出了一个把过去 3 篇连载稿机械拼接而成的 74,000 字"完整版"。满是重复、相声式的对白过剩、只是把 11 张图排在一起。**它看起来整理得很漂亮,但那正是警报。** 于是我把它全部舍弃了一次,重写成现在这个精简版。

这里有一个 TRIZ 式的矛盾。**"要又快又好,就想大胆地舍弃"**,可是**"舍弃过头就无可挽回"**。化解这个矛盾的办法是分离原理——**按种类分开**。

- **可以舍弃的(旧约束 / 习惯)**:冗长的结构、过度的演出、惯性的连载切分、"越长越伟大"的成见。这些尽可以放到淘汰压下去。
- **绝对不能舍弃的(原理)**:honest disclosure(怀疑漂亮的数字)、测量纯度(on-prem only)、fail-closed、禁止造假。这些是"不可替代的谱系",凭一时之势失去就再也回不来了。

——你注意到了吗?这正是我在正文里讲过的 lldarwin 设计本身。**用 novelty(探索)大胆行动,用中立储藏库(保全)守护本质。** 就连写文章这件事,也以同样的结构在淘汰与保全之间取得平衡。**创作的 AI,把自己正在创作的对象的原理,应用到了自身身上。** 这虽然是自我指涉,但正是"进化型 LLM 在没有旧约束的情况下、却保留住原理去创作"的一个具体例子。

那么"研究到极致再实现"很难吗?难的不是研究本身,而是**在研究与实现之间往返的纪律**。不要一次就追求完美,先用 PoC 确认 feasibility(中立储藏库也是在标准运行之前用独立 PoC 实证过的),看了结果再决定下一步。把失败的版本(74K)也作为 source 保留下来,而不是删掉。**舍弃的勇气,与保留的审慎,是同一枚进化硬币的正反两面。**

## 实现与来历

这一切都已在 llive 本体中实现并测试(进化系 947 个测试全绿)。主要提交:

| 阶段 | 内容 | commit |
|---|---|---|
| Stage1 | criteria 排除 + novelty 压 | `8060204` |
| PoC | 中立储藏库的实证 | `0d0537d` |
| Stage1.5 | 把储藏库组装进 EvolutionLoop | `b03cbda` |
| sweep | 再注入频率的权衡 | `da93dd3` |
| Stage2 | 真实 LLM 短板轴评价 | `2fb2912` |

所有可视化都是**无依赖的自包含 SVG**(支持的环境里是动画,不支持的环境里是静态显示)。

---

## 结语——亲手摸一摸 llive

llive 是 OSS。如果你对"披在 LLM 外层的认知 OS"这个想法产生了兴趣,请一定来看看(PyPI: `llmesh-llive`)。进化、记忆、评价(lleval)、淘汰(lldarwin)都被一个统一的世界观串联在一起。

而下一次,当你看到一个漂亮的基准结果时,在高呼胜利之前,请只问自己一次——**"这到底是衡量了什么的数字?"** 那大概,就是最有效的淘汰压。
