---
title: '進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで、人工進化はどう可視化されてきたか'
tags:
  - FullSense
  - 進化計算
  - 人工生命
  - 可視化
  - 解説
private: true
updated_at: '2026-05-25'
id: 0e221d447b7a8ad66d22
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

> ⚠ 本記事は **ja 骨子ドラフト**（蓄積目的・完璧不要）。en/zh/ko 展開は後続。投稿前に hero/theme SVG・進捗 badge・関連記事の Qiita URL cross-link を埋める。

# 日本語

# 進化を「見せる」技術の系譜 #30 — Conway のライフゲームから 3DGS まで

> **コンセプト hook**: 私が #25〜#27 で延々と語っている「人工進化」。実はこれ、半世紀以上の歴史がある
> 研究分野です。そして面白いのは、**進化の研究は常に「見せ方（可視化）」と二人三脚で進化してきた**こと。
> 1970 年の白黒の点滅セルから、2024 年の連続流体・3D ガウシアンまで。「進化を見せる技術」の系譜を、
> 教養として一気に辿ります。FullSense の進化可視化（思考因子グラフ上の系統樹）が、この系譜の
> **どこに立っているのか**を最後に位置づけます。

---

## 0. なぜ「可視化」が進化研究の主役なのか

進化は **長時間・大集団・多世代**の現象。数字の羅列では「何が起きたか」が掴めません。
だから人工進化の歴史は、ほぼそのまま **「進化を一目で理解させる表現の発明史」** です。

> 🍵 **休憩ポイント**: この記事は数式ゼロ・コードほぼゼロの「散歩」回です。コーヒー片手にどうぞ。
> 各時代の「見せ方のブレイクスルー」だけ拾っていきます。

---

## 1. 1970: Conway のライフゲーム — 「単純ルールが模様を生む」

- **何**: 2 次元セルオートマトン。生死 2 状態 × 近傍 8 セルの単純ルール。
- **見せ方の発明**: **格子の点滅そのものが可視化**。グライダー・ブリンカー・グライダーガンといった
  「動く模様」に名前がついた = 人間が**創発パターンを目で名づけた**最初期の例。
- **限界**: 進化（自然選択）ではなく決定論的な展開。しかし「単純ルール → 複雑な見た目」の衝撃が分野を開いた。

**節の肉付け予定**: グライダーが「移動する構造」として認識される=可視化が概念を生んだ好例として深掘り。

---

## 2. 1991: Tierra（Tom Ray）— 「コードが生き物になる」

- **何**: 仮想 CPU 上で自己複製する機械語プログラムの生態系。寄生体・免疫・最適化が**勝手に創発**。
- **見せ方の発明**: **メモリマップの可視化**。各プログラムが占めるメモリ領域を色で塗り、
  寄生体が宿主に食い込む様子を「地図」として見せた。**「コードの生態系」を空間として描いた**。
- **意義**: 「自己複製子の自然選択」を計算機内で初めて観測。open-ended evolution 研究の出発点の 1 つ。

---

## 3. 1994: Avida（Adami / Ofria）— 「進化を計測する」

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

## 4. 1994: Karl Sims「Evolved Virtual Creatures」— 「進化を映像で魅せる」

- **何**: 3D 物理シミュレーション内で、形態（block の繋がり）と神経制御を**同時に進化**させ、
  泳ぐ・歩く・物を取り合う生き物を生んだ。
- **見せ方の発明**: **3D アニメーション映像**。論文の図でなく**動画**で見せたことが衝撃を呼んだ。
  「進化が設計した、誰も予想しなかった奇妙な歩き方」を**人間が直感的に面白がれる**形にした。
- **意義**: 進化可視化が「研究者向けグラフ」から「**誰もが見て驚く映像**」へ。
  FullSense のデモ哲学（[[project_f25_demo_polish]]「動きで魅せる」）の精神的祖先。

> 🍵 **休憩ポイント**: ここまでで「白黒の点 → メモリ地図 → 系統樹 → 3D 動画」と、
> 見せ方が**抽象 → 具象 → 動的**へ進化したのが見えれば OK。後半は現代編です。

---

## 5. 2019: Lenia（Bert Chan）— 「連続的な人工生命」

- **何**: ライフゲームを**連続空間・連続時間・連続状態**に一般化。滑らかに動く「生き物のような」
  パターン（orbium 等）が多数発見された。
- **見せ方の発明**: **連続フィールドの滑らかなレンダリング**。離散の点滅から、生物の細胞のように
  しなやかに動く流体的表現へ。「人工生命が**美しい**」という新しい訴求軸を開いた。
- **意義**: 可視化の質そのものが研究の発見力を上げた例。美しく見えるからこそ新パターンを人間が気づける。

---

## 6. 2020s: Quality-Diversity の可視化 — 「多様性を地図にする」

- **何**: MAP-Elites / CMA-ME 等の QD アルゴリズム。単一 best でなく**多様な高性能解の集合**を生む。
- **見せ方の発明**: **behavior space のヒートマップ**。2 軸の behavior 記述子を格子に取り、
  各 cell の elite を色で塗る = 「**多様性そのものを地図として可視化**」。
- **意義**: FullSense / lldarwin の QD archive 可視化はここに直接立脚。
  「1 cell でも残れば全滅しない」を**地図の空白 vs 充填**で一目で見せられる（#26 で詳述）。

---

## 7. 2020s〜: 3D Gaussian Splatting（3DGS）— 「進化の状態を空間表現する」（FullSense の賭け）

- **何**: 元来は新視点合成（NeRF の系譜）の技術。点群を 3D ガウシアンで表現し高速・高品質に描画。
- **FullSense の着想**: 進化集団の**高次元 genome / pressure profile を 3D ガウシアン空間に写像**して
  「進化の状態を立体的に見せられないか」という探索（[[project_precision_metrology_llm]] の SH 係数連携と同根）。
- **位置づけ**: これは**まだ研究的賭け**であり、確立技術ではない（honest disclosure）。
  本記事の系譜の「最先端の縁」に置く実験です。

---

## 8. FullSense の進化可視化はどこに立つか

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

## 9. 関連
- 連載 #25〜#27 — 本記事の進化可視化の「中身」（monoculture / lldarwin / 反証）
- 関連 memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- 参考: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #25-27 の Qiita URL cross-link / en・zh・ko 版展開 -->
<!-- KEY MESSAGE: 進化研究は可視化と二人三脚。点滅→地図→系統樹→3D動画→連続→QD地図→3DGS。FullSense は Avida+Sims+QD の末裔。 -->
<!-- NOTE(事実整合): 年代/人名は一般的な人工生命史の通説に準拠。3DGS の進化可視化応用は FullSense の研究的賭けであり確立技術でない旨を明記済。 -->

---

# English

# The Lineage of "Showing" Evolution #30 — From Conway's Game of Life to 3DGS

> **Concept hook**: The "artificial evolution" I have been talking about endlessly in #25–#27 is, in fact, a research field with more than half a century of history. And here is the fascinating part: **research on evolution has always advanced hand in hand with "how to show it" (visualization)**. From the black-and-white blinking cells of 1970 to the continuous fluids and 3D Gaussians of 2024. Let us trace the lineage of "the technology for showing evolution" in one sweep, as a piece of general culture. At the end, we will locate **where FullSense's evolution visualization (a phylogenetic tree drawn on the thinking-factor graph) stands** within this lineage.

---

## 0. Why Is "Visualization" the Lead Actor in Evolution Research?

Evolution is a phenomenon of **long timescales, large populations, and many generations**. A list of numbers makes it impossible to grasp "what actually happened." That is why the history of artificial evolution is, almost literally, **a history of inventing expressions that let you understand evolution at a glance**.

> 🍵 **Break point**: This article is a "stroll" with zero equations and almost zero code. Enjoy it with a coffee in hand. We will pick up only the "breakthroughs in how to show things" from each era.

---

## 1. 1970: Conway's Game of Life — "Simple Rules Generate Patterns"

- **What**: A two-dimensional cellular automaton. Two states (alive/dead) × a simple rule over 8 neighboring cells.
- **The visualization invention**: **The blinking grid itself is the visualization**. "Moving patterns" such as gliders, blinkers, and glider guns were given names — one of the earliest examples of humans **naming emergent patterns with their own eyes**.
- **The limit**: This is not evolution (natural selection) but a deterministic unfolding. Yet the shock of "simple rules → complex appearance" opened up the field.

**Planned expansion of this section**: A deep dive into how the glider being recognized as a "moving structure" is a prime example of visualization giving birth to a concept.

---

## 2. 1991: Tierra (Tom Ray) — "Code Becomes a Living Thing"

- **What**: An ecosystem of self-replicating machine-code programs running on a virtual CPU. Parasites, immunity, and optimization **emerged on their own**.
- **The visualization invention**: **Visualization of the memory map**. Each program's occupied memory region was painted in color, and the way parasites burrow into hosts was shown as a "map." It **depicted the "ecosystem of code" as a space**.
- **Significance**: The first observation, inside a computer, of "natural selection of self-replicators." One of the starting points of open-ended evolution research.

---

## 3. 1994: Avida (Adami / Ofria) — "Measuring Evolution"

- **What**: A digital life platform that inherits the lineage of Tierra. Performing logic operations earns rewards (CPU time).
- **The visualization invention**: **Visualization of the phylogeny (phylogenetic tree) and the fitness landscape**. It drew, as a tree, "which descendants branched off from which ancestors," and made the stepwise evolution of complex traits (such as the EQU operation) **trackable**.
- **Significance**: It demonstrated that "complexity evolves through unavoidable steps" (Lenski et al. 2003, Nature). It **turned evolution from a story into an object of measurement**. FullSense's monoculture monitoring (max_lineage_share / archive growth) is a direct descendant of this "evolution that is measured."

> 🤔 **An analogy (manzai style)**:
> Boke: "Avida made it possible to measure evolution with numbers."
> Tsukkomi: "So it gave evolution a report card."
> Boke: "Exactly. When I said in #25 that 'the report card broke due to perfect-score inflation,' that was precisely an Avida-grade measurement story."

---

## 4. 1994: Karl Sims "Evolved Virtual Creatures" — "Showing Evolution as Footage"

- **What**: Inside a 3D physics simulation, it **co-evolved** morphology (chains of blocks) and neural control, producing creatures that swim, walk, and fight over objects.
- **The visualization invention**: **3D animated footage**. The shock came from showing it as **video** rather than as figures in a paper. It put "the strange gaits that evolution designed, which no one had predicted" into a form that **humans could intuitively delight in**.
- **Significance**: Evolution visualization moved from "graphs for researchers" to "**footage that astonishes anyone who watches it**." It is the spiritual ancestor of FullSense's demo philosophy ([[project_f25_demo_polish]] "captivate through motion").

> 🍵 **Break point**: If, up to here, you can see that the way of showing things evolved from **abstract → concrete → dynamic** — "black-and-white dots → memory map → phylogenetic tree → 3D video" — then you are good. The second half is the modern era.

---

## 5. 2019: Lenia (Bert Chan) — "Continuous Artificial Life"

- **What**: A generalization of the Game of Life to **continuous space, continuous time, and continuous state**. Many smoothly moving, "creature-like" patterns (such as orbium) were discovered.
- **The visualization invention**: **Smooth rendering of a continuous field**. From discrete blinking to a fluid expression that moves as supplely as a living cell. It opened up a new axis of appeal: "artificial life is **beautiful**."
- **Significance**: An example where the quality of the visualization itself raised the discovery power of the research. Precisely because it looks beautiful, humans can notice new patterns.

---

## 6. 2020s: Visualization of Quality-Diversity — "Mapping Diversity"

- **What**: QD algorithms such as MAP-Elites / CMA-ME. Instead of a single best, they produce **a set of diverse, high-performing solutions**.
- **The visualization invention**: **A heatmap of the behavior space**. Two-axis behavior descriptors are laid out on a grid, and the elite of each cell is painted in color — this **visualizes diversity itself as a map**.
- **Significance**: FullSense / lldarwin's QD archive visualization stands directly on this. It can show at a glance, through **emptiness vs. filling of the map**, the principle that "as long as even one cell survives, you do not go extinct" (detailed in #26).

---

## 7. 2020s onward: 3D Gaussian Splatting (3DGS) — "Representing the State of Evolution in Space" (FullSense's Bet)

- **What**: Originally a technique for novel-view synthesis (the lineage of NeRF). It represents a point cloud as 3D Gaussians and renders it fast and at high quality.
- **FullSense's idea**: An exploration of whether we can "show the state of evolution in three dimensions" by **mapping the high-dimensional genome / pressure profile of the evolving population into a 3D Gaussian space** (sharing the same root as the SH-coefficient linkage of [[project_precision_metrology_llm]]).
- **Positioning**: This is **still a research bet**, not an established technology (honest disclosure). It is an experiment placed at the "leading edge" of this article's lineage.

---

## 8. Where Does FullSense's Evolution Visualization Stand?

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

## 9. Related

- Series #25–#27 — the "substance" of the evolution visualization in this article (monoculture / lldarwin / disproof)
- Related memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- References: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

# 中文

# 「展示」进化的技术谱系 #30 — 从 Conway 的生命游戏到 3DGS

> **概念钩子**：我在 #25〜#27 里喋喋不休讲的「人工进化」，其实是一个有着半个多世纪历史的研究领域。而有意思的是，**进化研究始终与「如何展示（可视化）」并肩前行**。从 1970 年黑白闪烁的细胞，到 2024 年连续流体与 3D 高斯。让我们作为一种通识，一口气追溯「展示进化的技术」的谱系。最后，我们将定位 **FullSense 的进化可视化（绘制在思考因子图上的系统树）站在这条谱系的哪个位置**。

---

## 0. 为什么「可视化」是进化研究的主角

进化是一种 **长时间、大种群、多世代** 的现象。一堆数字罗列，根本抓不住「到底发生了什么」。因此人工进化的历史，几乎就直接是 **「让人一眼理解进化的表现手法发明史」**。

> 🍵 **休息点**：这篇文章是一次零公式、几乎零代码的「散步」。请端着咖啡慢慢看。我们只拾取各个时代「展示方式的突破」。

---

## 1. 1970：Conway 的生命游戏 —「简单规则生出图案」

- **是什么**：二维元胞自动机。生死两态 × 8 个邻居细胞的简单规则。
- **可视化的发明**：**格点的闪烁本身就是可视化**。滑翔机、闪光灯、滑翔机枪这类「移动的图案」被赋予了名字 = 人类 **用眼睛为涌现模式命名** 的最早期例子。
- **局限**：这并非进化（自然选择），而是决定论式的展开。但「简单规则 → 复杂外观」的冲击开辟了这个领域。

**本节计划充实**：深入探讨「滑翔机被识别为『移动的结构』」如何成为可视化催生概念的绝佳例子。

---

## 2. 1991：Tierra（Tom Ray）—「代码成为生物」

- **是什么**：在虚拟 CPU 上自我复制的机器码程序的生态系统。寄生体、免疫、最优化 **自行涌现**。
- **可视化的发明**：**内存映射的可视化**。把每个程序所占据的内存区域用颜色涂出，将寄生体咬入宿主的样子作为「地图」展示。它 **把「代码的生态系统」描绘成了一个空间**。
- **意义**：在计算机内首次观测到「自我复制子的自然选择」。这是开放式进化（open-ended evolution）研究的起点之一。

---

## 3. 1994：Avida（Adami / Ofria）—「测量进化」

- **是什么**：继承 Tierra 谱系的数字生命平台。完成逻辑运算便可获得奖励（CPU 时间）。
- **可视化的发明**：**系统树（phylogeny）与适应度地形的可视化**。把「哪些子孙从哪个祖先分支而来」绘成一棵树，让复杂性状（如 EQU 运算等）逐步进化的过程变得 **可追踪**。
- **意义**：它实证了「复杂性会经由不可避免的步骤进化」（Lenski et al. 2003, Nature）。它 **把进化从故事变成了测量对象**。FullSense 的 monoculture 监控（max_lineage_share / archive 成长）正是这种「被测量的进化」的直系后裔。

> 🤔 **打比方（相声风）**：
> 逗哏：「Avida 让进化能用数字来测量了。」
> 捧哏：「也就是给进化发了张成绩单嘛。」
> 逗哏：「没错。我在 #25 里说『满分通胀把成绩单搞坏了』，说的正是 Avida 级别的测量这回事。」

---

## 4. 1994：Karl Sims「Evolved Virtual Creatures」—「用影像呈现进化」

- **是什么**：在 3D 物理仿真之中，**同时进化** 形态（block 的连接）与神经控制，孕育出会游泳、会走路、会争抢物体的生物。
- **可视化的发明**：**3D 动画影像**。不是用论文里的图，而是用 **视频** 来展示，这引发了震撼。它把「进化所设计的、谁都没料到的奇异步态」做成了 **人类能凭直觉觉得有趣** 的形态。
- **意义**：进化可视化从「面向研究者的图表」迈向了「**任何人看了都会惊叹的影像**」。它是 FullSense 演示哲学（[[project_f25_demo_polish]]「以动感取胜」）的精神祖先。

> 🍵 **休息点**：到这里，如果你能看出展示方式经历了 **抽象 → 具象 → 动态** 的进化——「黑白点 → 内存地图 → 系统树 → 3D 视频」——那就够了。后半部分是现代篇。

---

## 5. 2019：Lenia（Bert Chan）—「连续的人工生命」

- **是什么**：把生命游戏一般化为 **连续空间、连续时间、连续状态**。人们发现了大量平滑运动、「像生物一样」的图案（如 orbium 等）。
- **可视化的发明**：**连续场的平滑渲染**。从离散的闪烁，转向如生物细胞般柔韧运动的流体式表现。它开辟了一条新的诉求轴线：「人工生命是 **美的**」。
- **意义**：这是可视化质量本身提升了研究发现力的例子。正因为看上去美，人类才能注意到新的图案。

---

## 6. 2020 年代：Quality-Diversity 的可视化 —「把多样性画成地图」

- **是什么**：MAP-Elites / CMA-ME 等 QD 算法。它们生出的不是单一 best，而是 **多样的高性能解的集合**。
- **可视化的发明**：**behavior space 的热力图**。取两轴的 behavior 描述子放到格点上，把每个 cell 的 elite 用颜色涂出 = 「**把多样性本身可视化为地图**」。
- **意义**：FullSense / lldarwin 的 QD archive 可视化直接立足于此。它能通过 **地图的空白 vs 填充** 一眼展示「只要还剩一个 cell 就不会全军覆没」（详见 #26）。

---

## 7. 2020 年代起：3D Gaussian Splatting（3DGS）—「将进化的状态以空间表达」（FullSense 的赌注）

- **是什么**：原本是新视角合成（NeRF 谱系）的技术。它把点云用 3D 高斯来表示，并以高速、高品质渲染。
- **FullSense 的构想**：一种探索——能否把进化种群的 **高维 genome / pressure profile 映射到 3D 高斯空间**，从而「将进化的状态立体地展示出来」（与 [[project_precision_metrology_llm]] 的 SH 系数联动同根同源）。
- **定位**：这 **仍是一项研究性赌注**，并非已确立的技术（honest disclosure）。它是放在本文谱系「最前沿的边缘」上的一次实验。

---

## 8. FullSense 的进化可视化站在哪里

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

## 9. 相关

- 连载 #25〜#27 — 本文进化可视化的「内容」（monoculture / lldarwin / 反证）
- 相关 memory：[[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- 参考：Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

# 한국어

# 진화를 「보여주는」 기술의 계보 #30 — Conway 의 라이프 게임에서 3DGS 까지

> **콘셉트 훅**: 제가 #25〜#27 에서 끊임없이 이야기하고 있는 「인공 진화」. 사실 이것은 반세기 이상의 역사를 가진 연구 분야입니다. 그리고 흥미로운 점은, **진화 연구는 늘 「보여주는 방식(시각화)」과 2인 3각으로 함께 진화해 왔다**는 것입니다. 1970 년의 흑백으로 깜빡이는 세포에서, 2024 년의 연속 유체·3D 가우시안까지. 「진화를 보여주는 기술」의 계보를 교양으로서 단숨에 더듬어 봅니다. 마지막에는 FullSense 의 진화 시각화(사고 인자 그래프 위의 계통수)가 이 계보의 **어디에 서 있는지**를 자리매김합니다.

---

## 0. 왜 「시각화」가 진화 연구의 주역인가

진화는 **장시간·대집단·다세대** 의 현상입니다. 숫자의 나열만으로는 「무슨 일이 일어났는지」를 파악할 수 없습니다. 그래서 인공 진화의 역사는, 거의 그대로 **「진화를 한눈에 이해시키는 표현의 발명사」** 입니다.

> 🍵 **휴식 포인트**: 이 글은 수식 제로·코드 거의 제로의 「산책」 편입니다. 커피 한 잔과 함께 즐기세요. 각 시대의 「보여주는 방식의 돌파구」만 골라 갑니다.

---

## 1. 1970: Conway 의 라이프 게임 —「단순한 규칙이 무늬를 낳는다」

- **무엇**: 2차원 셀룰러 오토마타. 생사 2상태 × 이웃 8셀의 단순한 규칙.
- **보여주는 방식의 발명**: **격자의 깜빡임 그 자체가 시각화**. 글라이더·블링커·글라이더 건 같은 「움직이는 무늬」에 이름이 붙은 것 = 인간이 **창발 패턴을 눈으로 이름 붙인** 가장 초기의 예.
- **한계**: 진화(자연선택)가 아니라 결정론적인 전개. 그러나 「단순한 규칙 → 복잡한 겉모습」의 충격이 이 분야를 열었다.

**이 절의 살 붙이기 예정**: 글라이더가 「이동하는 구조」로 인식된 것 = 시각화가 개념을 낳은 좋은 예로서 깊이 파고든다.

---

## 2. 1991: Tierra（Tom Ray）—「코드가 생물이 된다」

- **무엇**: 가상 CPU 위에서 자기 복제하는 기계어 프로그램의 생태계. 기생체·면역·최적화가 **저절로 창발**.
- **보여주는 방식의 발명**: **메모리 맵의 시각화**. 각 프로그램이 차지하는 메모리 영역을 색으로 칠하고, 기생체가 숙주에 파고드는 모습을 「지도」로서 보여줬다. **「코드의 생태계」를 공간으로 그려냈다**.
- **의의**: 「자기 복제자의 자연선택」을 컴퓨터 안에서 처음으로 관측. open-ended evolution 연구의 출발점 중 하나.

---

## 3. 1994: Avida（Adami / Ofria）—「진화를 측정한다」

- **무엇**: Tierra 의 계보를 잇는 디지털 생명 플랫폼. 논리 연산을 해내면 보상(CPU 시간)을 얻는다.
- **보여주는 방식의 발명**: **계통수(phylogeny)와 적응도 지형의 시각화**. 「어느 조상에서 어느 자손이 분기했는가」를 트리로 그리고, 복잡 형질(EQU 연산 등)이 단계적으로 진화하는 과정을 **추적 가능**하게 했다.
- **의의**: 「불가피한 단계를 거쳐 복잡성이 진화한다」를 실증했다(Lenski et al. 2003, Nature). **진화를 이야기가 아니라 측정 대상으로 만들었다**. FullSense 의 monoculture 모니터링(max_lineage_share / archive 성장)은 이 「측정하는 진화」의 직계다.

> 🤔 **비유(만담풍)**:
> 보케: 「Avida 는 진화를 숫자로 측정할 수 있게 했다.」
> 츳코미: 「즉 진화에 성적표를 매긴 거네.」
> 보케: 「맞아. #25 에서 내가 『만점 인플레로 성적표가 망가졌다』고 한 게, 바로 Avida 급 측정 이야기야.」

---

## 4. 1994: Karl Sims「Evolved Virtual Creatures」—「진화를 영상으로 매료한다」

- **무엇**: 3D 물리 시뮬레이션 안에서, 형태(block 의 연결)와 신경 제어를 **동시에 진화**시켜, 헤엄치고·걷고·물건을 서로 차지하는 생물을 낳았다.
- **보여주는 방식의 발명**: **3D 애니메이션 영상**. 논문의 그림이 아니라 **동영상**으로 보여준 것이 충격을 불러일으켰다. 「진화가 설계한, 누구도 예상하지 못한 기묘한 걸음걸이」를 **인간이 직관적으로 재미있어할 수 있는** 형태로 만들었다.
- **의의**: 진화 시각화가 「연구자용 그래프」에서 「**누구나 보고 놀라는 영상**」으로. FullSense 의 데모 철학([[project_f25_demo_polish]] 「움직임으로 매료한다」)의 정신적 조상.

> 🍵 **휴식 포인트**: 여기까지 「흑백 점 → 메모리 지도 → 계통수 → 3D 동영상」으로, 보여주는 방식이 **추상 → 구상 → 동적** 으로 진화한 것이 보이면 OK. 후반은 현대 편입니다.

---

## 5. 2019: Lenia（Bert Chan）—「연속적인 인공 생명」

- **무엇**: 라이프 게임을 **연속 공간·연속 시간·연속 상태** 로 일반화. 매끄럽게 움직이는 「생물 같은」 패턴(orbium 등)이 다수 발견되었다.
- **보여주는 방식의 발명**: **연속 필드의 매끄러운 렌더링**. 이산적인 깜빡임에서, 생물의 세포처럼 유연하게 움직이는 유체적 표현으로. 「인공 생명이 **아름답다**」라는 새로운 소구 축을 열었다.
- **의의**: 시각화의 질 그 자체가 연구의 발견력을 높인 예. 아름답게 보이기에 새로운 패턴을 인간이 알아챌 수 있다.

---

## 6. 2020 년대: Quality-Diversity 의 시각화 —「다양성을 지도로 만든다」

- **무엇**: MAP-Elites / CMA-ME 등의 QD 알고리즘. 단일 best 가 아니라 **다양한 고성능 해의 집합**을 낳는다.
- **보여주는 방식의 발명**: **behavior space 의 히트맵**. 2축의 behavior 기술자를 격자에 두고, 각 cell 의 elite 를 색으로 칠한다 = 「**다양성 그 자체를 지도로서 시각화**」.
- **의의**: FullSense / lldarwin 의 QD archive 시각화는 여기에 직접 입각해 있다. 「1 cell 이라도 남으면 전멸하지 않는다」를 **지도의 공백 vs 충전**으로 한눈에 보여줄 수 있다(#26 에서 상술).

---

## 7. 2020 년대〜: 3D Gaussian Splatting（3DGS）—「진화의 상태를 공간 표현한다」（FullSense 의 도박）

- **무엇**: 본래는 신규 시점 합성(NeRF 의 계보) 기술. 점군을 3D 가우시안으로 표현해 고속·고품질로 렌더링한다.
- **FullSense 의 착상**: 진화 집단의 **고차원 genome / pressure profile 을 3D 가우시안 공간에 사상**하여 「진화의 상태를 입체적으로 보여줄 수 없을까」라는 탐색([[project_precision_metrology_llm]] 의 SH 계수 연계와 같은 뿌리).
- **자리매김**: 이것은 **아직 연구적 도박**이며, 확립된 기술이 아니다(honest disclosure). 본 글 계보의 「최첨단의 가장자리」에 두는 실험이다.

---

## 8. FullSense 의 진화 시각화는 어디에 서는가

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

## 9. 관련

- 연재 #25〜#27 — 본 글 진화 시각화의 「내용」（monoculture / lldarwin / 반증）
- 관련 memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- 참고: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)
