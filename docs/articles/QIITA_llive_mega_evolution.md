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
