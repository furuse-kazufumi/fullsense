---
title: Will Caster と Andrew NDR114 が目指したもの — llive のビジョン論
tags:
  - FullSense
  - llive
  - 解説
  - TODO_TAG
  - TODO_TAG
private: false
updated_at: '2026-05-22'
id: e72192c75ff461d72601
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# Will Caster と Andrew NDR114 が目指したもの — llive のビジョン論

> 📚 **連載ナビ**: ← #16 三自の精神で AI 運用 ｜ **#17 本記事** ｜ #18 GPU 無し PC 主役の LLM 基盤 → ｜ [連載 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 各記事は単独でも読めます（リンクは回遊用）。

**1 行 hook**:
LinkedIn のプロフィール画像を、自分の顔とロボットを画像生成 AI で融合した一枚にしている。冗談ではない。**いずれ AI と人が融合できたら面白い**と本気で考えている。その第一歩としての llive。

---

## 「第二の脳」シリーズ第 3 部 — ビジョン論

本シリーズはここまで 2 部構成だった。

| 部 | テーマ | 記事 |
|---|---|---|
| 第 1 部 | **構築論** — 30 年経験 + Perplexity + Claude Code + TRIZ + RAG | [15] |
| 第 2 部 | **運用論** — 三自の精神 + マネジメント書籍 | [16] |
| **第 3 部** | **ビジョン論** — Will Caster と Andrew NDR114 | 本記事 |

構築 (どう作るか) → 運用 (どう動かすか) → ビジョン (**なぜ作るか**)。順番が逆だと感じるかもしれない。なぜそうしたかは最後に書く。

## 2 つの映画

筆者は 2 本の映画から強く影響を受けている。

### Transcendence (2014)

Dr. Will Caster (Johnny Depp 演) が、瀕死の状態で自身の意識を AI に **アップロード** する。映画後半、AI 化した Will は人類の知識を吸収し続け、世界規模で介入を始める。賛美と恐怖が同居する描写で、「**もし人間の意識を AI に移せたら何が起きるか**」を真正面から問いかけた作品。

### Bicentennial Man / 邦題「アンドリュー NDR114」(1999)

家庭用ロボット Andrew (Robin Williams 演) が、長い時間をかけて感情・創造性・自由意志・身体性を獲得し、最終的に「**人間として認められる**」ことを求める。原作は Isaac Asimov の同名短編。「ロボットが人間になる」のではなく「**人間とは何か** を AI が問う」物語。

両者は方向が逆だが、共通点は明確: **人と AI の境界が消える未来**。筆者はこの未来を「面白い」と思い、それを **エンジニアリングで前進させる** ことを開発のドライバにしている。

### ☕ ちょっと脱線

Andrew NDR114 の原題 *Bicentennial Man* (200 年生きる男) は、Asimov の短編 *The Bicentennial Man* (1976) が原作。Asimov は「ロボット工学三原則」を発明した人だが、晩年の作品では **三原則そのものを揺さぶる** 方向へ向かった。Andrew はその到達点と言える。技術ルールも、人間の心の動きの前では揺らぐ。

## LinkedIn プロフィール画像 — 視覚的な宣言

筆者の LinkedIn プロフィール画像は、自分の顔と人型ロボットの要素を画像生成 AI で融合させたものを使っている。これはネタではなく、**いずれそうなる未来を既にビジュアルで宣言** している。

技術ブログ・OSS リポ・LinkedIn 投稿のすべてが「将来のあるべき姿に向かう一歩」として整合する。視覚要素もその一部だ。

## llive の各機能はビジョンへの準備層

llive で本セッション 1270 PASS まで積み上げた機能群を、ビジョン視点で読み直すとこうなる。

| llive 機能 | 融合ビジョンへの寄与 |
|---|---|
| **FullSense** (全感覚統合 umbrella) | 人 + AI の境界曖昧化に必要な感覚統合層 |
| **第二の脳** (Claude Code + RAG ~5 万件) | **既に部分的融合** (脳の外延としての知識アクセス) |
| **SIL ledger / SEC-03 hash chain** | 融合時の「誰が責任を持つか」audit 基盤 |
| **Approval Bus + HITL** | 融合移行期の人間判断ゲート保持 |
| **三自の精神 (AI 自律)** | Andrew NDR114 的な自律性獲得プロセス |
| **RAD bci / neuroscience / neural_signal / prosthetic_neural / cognitive_ai / neuromorphic** (6 分野コーパス) | BCI 経由融合の知識基盤 |

特に最後の RAD 6 分野は、本シリーズの「第二の脳」を **物理的な BCI (Brain-Computer Interface)** へ拡張する中期ロードマップ。コーパスは既に構築済、実装は別プロジェクト (mcp-3d 等) との統合待ち。

## 短期 / 中期 / 長期ロードマップ

| Term | 内容 | 現状 |
|---|---|---|
| 短期 (現在) | 第二の脳型開発 (Claude Code + RAG + Perplexity) | **実証済** (本セッション 1270 PASS) |
| 中期 (1-3 年) | BCI 経由インタフェース | RAD 6 分野コーパス準備済、実装は別プロジェクト |
| 長期 (3-10 年) | 意識アップロード or Andrew 的双方向 | ビジョン段階、llive の SIL/Approval が下地 |

短期は既に手元で動いている。本シリーズで何度も触れた「30 年経験 + Claude Code + RAG = チーム速度」は、**脳の外側に第二の脳を構築した状態** だ。これを物理融合に拡張するのが中期、意識アップロードまで拡張するのが長期。

### ☕ ちょっと本音

正直に言うと、BCI まわりは筆者の専門 (画像処理 / 三次元計測) とは少しズレている。だから RAD 6 分野コーパスを準備したのは「**自分が後で困らないため**」でもある。長期ビジョンを描くとき、知識のないドメインに踏み込む覚悟が必要だが、その不安は **先にコーパスを積んでおく** ことで小さくできる。

## なぜビジョン論を最後に書いたか

ビジョン論を最初に書いてしまうと、技術記事が SF やビジョンスピーチに見えてしまう。読者はまず「実装で何が動いているか」「どう運用しているか」を確認したい。それを #15 (構築論) と #16 (運用論) で示した上で、**「実はこの全部はビジョンへの準備層なんですよ」** と明かす方が説得力がある。

技術記事はビジョンから始めると弱くなる。**実装から始めてビジョンで結ぶ** と強くなる。Andrew NDR114 が長い時間をかけて 1 つずつ獲得していったように、llive も 1 機能ずつ積んでいる。その積み重ねが、いつか「人と AI の融合」につながる。

## 結び — 「いずれ」のために今日できること

「いずれ AI と人が融合できたら面白い」というのは漠然とした願望に聞こえるかもしれない。だが、今日できる具体的な準備は確かにある。

- **第二の脳** を脳の外側に構築する (構築論 #15)
- **三自の精神** で AI に自律性を渡す訓練を積む (運用論 #16)
- **audit 可能な意思決定基盤** を SIL ledger で残す (本記事 §llive 機能)
- **BCI / neuroscience コーパス** を準備しておく
- **視覚的ブランディング** で未来を先取りする (LinkedIn 画像)

これらは「いつか」のためにではなく、**今日からチームの生産性を上げる手段**として既に有効だ。融合は副産物として、または最終形として、自然に近づいてくる。

llive は Apache 2.0 + Commercial dual-license の OSS、Repo は https://github.com/furuse-kazufumi/llive 。本シリーズ 3 部 (構築論 / 運用論 / ビジョン論) に共感する方は、Issue / Discussion でぜひ。

---

**「第二の脳」シリーズ完結**:
- [15] 30 年経験 + Perplexity + Claude Code + TRIZ + RAG = 第二の脳 (**構築論**)
- [16] 三自の精神 — 圧倒的成果マネジャー流の AI 運用論 (**運用論**)
- [17] Will Caster と Andrew NDR114 が目指したもの (**本記事 / ビジョン論**)

## 参考文献 / 参考リソース

### 映画
- *Transcendence*, Wally Pfister 監督, Warner Bros., 2014
- *Bicentennial Man* (邦題「アンドリュー NDR114」), Chris Columbus 監督, Touchstone Pictures, 1999
- Isaac Asimov, *The Bicentennial Man and Other Stories*, Doubleday, 1976 (映画原作)

### BCI / 神経工学
- Miguel A. L. Nicolelis, *Beyond Boundaries: The New Neuroscience of Connecting Brains with Machines—and How It Will Change Our Lives*, Times Books, 2011
- Rajesh P. N. Rao, *Brain-Computer Interfacing: An Introduction*, Cambridge University Press, 2013
- Neuralink 公式 — https://neuralink.com/
- BCI Society — https://bcisociety.org/

### 人間-AI 共生研究
- Stuart Russell, *Human Compatible: Artificial Intelligence and the Problem of Control*, Viking, 2019
- Pattie Maes (MIT Media Lab) Fluid Interfaces Group — https://www.media.mit.edu/groups/fluid-interfaces/overview/

### llive 関連
- llive リポジトリ — https://github.com/furuse-kazufumi/llive
- 本シリーズ第 1 部 [15] (構築論) / 第 2 部 [16] (運用論)
- 本セッション SUMMARY.md — `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`

<!-- llive:meta.article_id="17_human_ai_fusion_vision" target=llove -->
<!-- llive:meta.published_date="2026-05-21" -->
<!-- llive:meta.tags=["llive","ai","vision","transcendence","bci","fusion","human-ai"] target=any -->
<!-- llive:meta.series="second_brain_part3_vision" -->

---

# English

# What Will Caster and Andrew NDR114 Were Aiming For — The Vision Behind llive

> 📚 **Series Navigation**: ← #16 Operating AI in the Spirit of "Three Selves" ｜ **#17 This Article** ｜ #18 A PC Without a GPU as the Star of an LLM Platform → ｜ [Series LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ Each article can be read on its own (links are for browsing across the series).

**One-line hook**:
My LinkedIn profile picture is a single image that fuses my own face with a robot, generated by an image-generation AI. It is not a joke. I seriously believe that **it would be fascinating if humans and AI could one day merge**. llive is the first step toward that.

---

## "The Second Brain" Series, Part 3 — The Vision

So far this series has consisted of two parts.

| Part | Theme | Article |
|---|---|---|
| Part 1 | **The Construction** — 30 years of experience + Perplexity + Claude Code + TRIZ + RAG | [15] |
| Part 2 | **The Operation** — The Spirit of "Three Selves" + management books | [16] |
| **Part 3** | **The Vision** — Will Caster and Andrew NDR114 | This article |

Construction (how to build it) → Operation (how to run it) → Vision (**why build it**). You might feel the order is backward. I will explain at the end why I did it this way.

## Two Movies

I have been strongly influenced by two movies.

### Transcendence (2014)

Dr. Will Caster (played by Johnny Depp), on the brink of death, **uploads** his own consciousness into an AI. In the latter half of the film, the AI-ified Will keeps absorbing humanity's knowledge and begins intervening on a global scale. With a portrayal in which admiration and fear coexist, it confronts head-on the question of "**what would happen if a human consciousness could be transferred into an AI**."

### Bicentennial Man / Japanese title "Andrew NDR114" (1999)

A household robot, Andrew (played by Robin Williams), takes a long time to acquire emotion, creativity, free will, and physicality, ultimately seeking to be "**recognized as human**." The original work is a short story of the same name by Isaac Asimov. Rather than "a robot becoming human," it is a story in which "**an AI asks what it means to be human**."

The two films point in opposite directions, but the common ground is clear: **a future in which the boundary between humans and AI disappears**. I find this future "fascinating," and **advancing it through engineering** is the driver of my development work.

### ☕ A Little Detour

The original title of Andrew NDR114, *Bicentennial Man* (a man who lives 200 years), is based on Asimov's short story *The Bicentennial Man* (1976). Asimov was the person who invented the "Three Laws of Robotics," but in his later works he moved in a direction that **shook the Three Laws themselves**. Andrew can be considered the culmination of that. Technical rules, too, waver before the movements of the human heart.

## The LinkedIn Profile Picture — A Visual Declaration

My LinkedIn profile picture uses an image that fuses my own face with elements of a humanoid robot, generated by an image-generation AI. This is not a gag; it is **a visual declaration, made already, of a future that will one day come to be**.

My tech blog, OSS repos, and LinkedIn posts all align as "a step toward what things should one day look like." The visual elements are part of that, too.

## Each Feature of llive Is a Preparation Layer for the Vision

Re-reading, from the perspective of the vision, the set of features I built up to 1270 PASS in this session in llive, it looks like this.

| llive Feature | Contribution to the Fusion Vision |
|---|---|
| **FullSense** (the all-senses-integration umbrella) | The sensory-integration layer needed to blur the boundary between human + AI |
| **The Second Brain** (Claude Code + RAG, ~50,000 entries) | **Already a partial fusion** (knowledge access as an extension of the brain) |
| **SIL ledger / SEC-03 hash chain** | The audit foundation for "who holds responsibility" at the time of fusion |
| **Approval Bus + HITL** | Preserving a human-judgment gate during the transition to fusion |
| **The Spirit of "Three Selves" (AI autonomy)** | An Andrew-NDR114-style process of acquiring autonomy |
| **RAD bci / neuroscience / neural_signal / prosthetic_neural / cognitive_ai / neuromorphic** (6-field corpus) | The knowledge foundation for fusion via BCI |

The last item, the 6 RAD fields in particular, is a medium-term roadmap that extends this series' "second brain" into a **physical BCI (Brain-Computer Interface)**. The corpus is already built; the implementation awaits integration with other projects (such as mcp-3d).

## Short-term / Medium-term / Long-term Roadmap

| Term | Content | Status |
|---|---|---|
| Short-term (now) | Second-brain-style development (Claude Code + RAG + Perplexity) | **Proven** (1270 PASS this session) |
| Medium-term (1–3 years) | An interface via BCI | RAD 6-field corpus prepared; implementation in a separate project |
| Long-term (3–10 years) | Consciousness upload or Andrew-style bidirectionality | At the vision stage; llive's SIL/Approval form the groundwork |

The short-term is already running at hand. The "30 years of experience + Claude Code + RAG = team speed" that I have touched on repeatedly in this series is **a state in which a second brain has been built outside the brain**. Extending this to a physical fusion is the medium-term; extending it as far as consciousness upload is the long-term.

### ☕ A Little Honesty

To be honest, the area around BCI is a little off from my specialty (image processing / 3D measurement). So part of the reason I prepared the RAD 6-field corpus was "**so that I won't be in trouble later**." When painting a long-term vision, you need the resolve to step into a domain you have no knowledge of, but that anxiety can be made smaller by **stacking up the corpus in advance**.

## Why I Wrote the Vision Last

If you write the vision first, the technical article ends up looking like science fiction or a vision speech. Readers first want to confirm "what is actually running in the implementation" and "how it is being operated." It is more persuasive to show that in #15 (the construction) and #16 (the operation), and then to reveal, **"actually, all of this is a preparation layer for the vision."**

A technical article becomes weaker when it starts from the vision. It becomes stronger when you **start from the implementation and tie it together with the vision**. Just as Andrew NDR114 acquired things one at a time over a long period, llive too is stacking up one feature at a time. That accumulation will, someday, lead to "the fusion of humans and AI."

## Closing — What Can Be Done Today for the Sake of "Someday"

"It would be fascinating if humans and AI could one day merge" may sound like a vague wish. But there really are concrete preparations that can be done today.

- Build **a second brain** outside the brain (the construction, #15)
- Accumulate training in handing autonomy to AI through **the Spirit of "Three Selves"** (the operation, #16)
- Leave **an auditable decision-making foundation** in the SIL ledger (this article, §llive Features)
- Prepare **the BCI / neuroscience corpus** in advance
- Get ahead of the future through **visual branding** (the LinkedIn picture)

These are not just for "someday"; they are already effective as **a means to raise team productivity starting today**. Fusion will approach naturally, as a by-product or as the final form.

llive is OSS under an Apache 2.0 + Commercial dual-license; the repo is https://github.com/furuse-kazufumi/llive . If the three parts of this series (the construction / the operation / the vision) resonate with you, please come by via Issues / Discussions.

---

**"The Second Brain" Series, Concluded**:
- [15] 30 years of experience + Perplexity + Claude Code + TRIZ + RAG = a second brain (**the construction**)
- [16] The Spirit of "Three Selves" — AI operation in the style of an overwhelming-results manager (**the operation**)
- [17] What Will Caster and Andrew NDR114 were aiming for (**this article / the vision**)

## References / Resources

### Movies
- *Transcendence*, directed by Wally Pfister, Warner Bros., 2014
- *Bicentennial Man* (Japanese title "Andrew NDR114"), directed by Chris Columbus, Touchstone Pictures, 1999
- Isaac Asimov, *The Bicentennial Man and Other Stories*, Doubleday, 1976 (the film's source material)

### BCI / Neural Engineering
- Miguel A. L. Nicolelis, *Beyond Boundaries: The New Neuroscience of Connecting Brains with Machines—and How It Will Change Our Lives*, Times Books, 2011
- Rajesh P. N. Rao, *Brain-Computer Interfacing: An Introduction*, Cambridge University Press, 2013
- Neuralink official — https://neuralink.com/
- BCI Society — https://bcisociety.org/

### Human-AI Symbiosis Research
- Stuart Russell, *Human Compatible: Artificial Intelligence and the Problem of Control*, Viking, 2019
- Pattie Maes (MIT Media Lab) Fluid Interfaces Group — https://www.media.mit.edu/groups/fluid-interfaces/overview/

### llive-related
- llive repository — https://github.com/furuse-kazufumi/llive
- This series' Part 1 [15] (the construction) / Part 2 [16] (the operation)
- This session's SUMMARY.md — `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`

---

# 中文

# Will Caster 与 Andrew NDR114 所追求的目标 —— llive 的愿景论

> 📚 **连载导航**: ← #16 以"三自"精神运营 AI ｜ **#17 本文** ｜ #18 以无 GPU 的 PC 为主角的 LLM 平台 → ｜ [连载 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 每篇文章都可单独阅读（链接用于在连载间回游）。

**一句话 hook**:
我把 LinkedIn 的头像设成了用图像生成 AI 将自己的脸与机器人融合在一起的一张图。这不是开玩笑。我真心认为**如果将来人与 AI 能够融合，会很有意思**。llive 就是迈向那一步的第一步。

---

## "第二大脑"系列第 3 部 —— 愿景论

本系列到目前为止是两部构成。

| 部 | 主题 | 文章 |
|---|---|---|
| 第 1 部 | **构建论** —— 30 年经验 + Perplexity + Claude Code + TRIZ + RAG | [15] |
| 第 2 部 | **运营论** —— 三自精神 + 管理类书籍 | [16] |
| **第 3 部** | **愿景论** —— Will Caster 与 Andrew NDR114 | 本文 |

构建（如何做）→ 运营（如何运行）→ 愿景（**为何做**）。你也许会觉得顺序反了。为什么这样安排，我会在最后写明。

## 两部电影

笔者受到两部电影的强烈影响。

### Transcendence（超验骇客，2014）

Dr. Will Caster（Johnny Depp 饰）在濒死之际，将自己的意识**上传**到 AI。影片后半，AI 化的 Will 不断吸收人类的知识，并开始在全球范围进行介入。以赞美与恐惧并存的描绘，正面叩问了"**如果能把人的意识移植到 AI 会发生什么**"这一命题。

### Bicentennial Man / 日译名"安德鲁 NDR114"（1999）

家用机器人 Andrew（Robin Williams 饰）历经漫长岁月获得了情感、创造力、自由意志与身体性，最终寻求"**被承认为人**"。原著是 Isaac Asimov 的同名短篇。这并非"机器人成为人"，而是"**AI 叩问何为人**"的故事。

两者方向相反，但共同点很明确：**人与 AI 的边界消失的未来**。笔者认为这个未来"很有意思"，并把**用工程学去推进它**作为开发的驱动力。

### ☕ 稍微岔开一下

Andrew NDR114 的原题 *Bicentennial Man*（活 200 年的男人），原著是 Asimov 的短篇 *The Bicentennial Man*（1976）。Asimov 是发明了"机器人学三定律"的人，但在晚年的作品中却转向了**动摇三定律本身**的方向。Andrew 可以说是那个方向的终点。技术规则，在人心的波动面前，同样会动摇。

## LinkedIn 头像 —— 视觉上的宣言

笔者的 LinkedIn 头像，用的是用图像生成 AI 把自己的脸与人型机器人元素融合而成的一张图。这不是噱头，而是**已经用视觉宣告了那个终将到来的未来**。

技术博客、OSS 仓库、LinkedIn 发帖，全都作为"迈向未来应有之姿的一步"而保持一致。视觉要素也是其中的一部分。

## llive 的各项功能都是通往愿景的准备层

把笔者在本次会话中于 llive 累积到 1270 PASS 的功能群，从愿景的视角重新解读，便是如此。

| llive 功能 | 对融合愿景的贡献 |
|---|---|
| **FullSense**（全感觉整合 umbrella） | 模糊人 + AI 边界所需的感觉整合层 |
| **第二大脑**（Claude Code + RAG 约 5 万条） | **已是部分融合**（作为大脑外延的知识访问） |
| **SIL ledger / SEC-03 hash chain** | 融合时"由谁负责"的审计基础 |
| **Approval Bus + HITL** | 在向融合过渡期保留人类判断的闸门 |
| **三自精神（AI 自主）** | Andrew NDR114 式的自主性获得过程 |
| **RAD bci / neuroscience / neural_signal / prosthetic_neural / cognitive_ai / neuromorphic**（6 领域语料） | 经由 BCI 实现融合的知识基础 |

尤其是最后的 6 个 RAD 领域，是把本系列的"第二大脑"扩展到**物理性的 BCI（Brain-Computer Interface，脑机接口）**的中期路线图。语料已经构建完成，实现则有待与其他项目（如 mcp-3d）的整合。

## 短期 / 中期 / 长期路线图

| Term | 内容 | 现状 |
|---|---|---|
| 短期（当前） | 第二大脑型开发（Claude Code + RAG + Perplexity） | **已实证**（本次会话 1270 PASS） |
| 中期（1-3 年） | 经由 BCI 的接口 | RAD 6 领域语料已就绪，实现在另一项目中 |
| 长期（3-10 年） | 意识上传 or Andrew 式双向 | 处于愿景阶段，llive 的 SIL/Approval 为其铺垫 |

短期已经在手边运行。本系列中多次提到的"30 年经验 + Claude Code + RAG = 团队速度"，正是**在大脑之外构建了第二大脑的状态**。把它扩展到物理融合是中期，扩展到意识上传是长期。

### ☕ 稍微说点真心话

老实说，BCI 这一带与笔者的专业（图像处理 / 三维测量）略有偏离。所以我准备 RAD 6 领域语料，也有"**为了不让自己以后犯难**"的一面。描绘长期愿景时，需要踏入自己毫无知识的领域的觉悟，而这份不安，可以通过**事先把语料积累起来**来减小。

## 为何把愿景论放在最后写

如果一开始就写愿景论，技术文章就会看起来像科幻或愿景演讲。读者首先想确认"实现中究竟有什么在运行""如何运营"。在 #15（构建论）和 #16（运营论）中展示了这些之后，再揭晓**"其实这一切都是通往愿景的准备层"**，会更有说服力。

技术文章从愿景开始会变弱。**从实现开始、用愿景收尾**则会变强。正如 Andrew NDR114 历经漫长岁月一件件地获得，llive 也在一项项地累积功能。这份累积，终有一天会通向"人与 AI 的融合"。

## 结语 —— 为了"终有一天"，今天能做的事

"如果将来人与 AI 能够融合，会很有意思"，听起来或许像一个模糊的愿望。但今天确实有可以做的具体准备。

- 在大脑之外构建**第二大脑**（构建论 #15）
- 以**三自精神**积累把自主性交给 AI 的训练（运营论 #16）
- 用 SIL ledger 留下**可审计的决策基础**（本文 §llive 功能）
- 事先准备好 **BCI / neuroscience 语料**
- 用**视觉品牌化**抢先一步迎接未来（LinkedIn 头像）

这些并非只为"某一天"，而是作为**从今天起提升团队生产力的手段**，已然有效。融合，会作为副产物、或作为最终形态，自然而然地靠近。

llive 是 Apache 2.0 + Commercial dual-license 的 OSS，Repo 在 https://github.com/furuse-kazufumi/llive 。对本系列三部（构建论 / 运营论 / 愿景论）有共鸣的朋友，欢迎在 Issue / Discussion 交流。

---

**"第二大脑"系列完结**:
- [15] 30 年经验 + Perplexity + Claude Code + TRIZ + RAG = 第二大脑（**构建论**）
- [16] 三自精神 —— 压倒性成果型经理人式的 AI 运营论（**运营论**）
- [17] Will Caster 与 Andrew NDR114 所追求的目标（**本文 / 愿景论**）

## 参考文献 / 参考资源

### 电影
- *Transcendence*，Wally Pfister 导演，Warner Bros.，2014
- *Bicentennial Man*（日译名"安德鲁 NDR114"），Chris Columbus 导演，Touchstone Pictures，1999
- Isaac Asimov, *The Bicentennial Man and Other Stories*, Doubleday, 1976（电影原著）

### BCI / 神经工程
- Miguel A. L. Nicolelis, *Beyond Boundaries: The New Neuroscience of Connecting Brains with Machines—and How It Will Change Our Lives*, Times Books, 2011
- Rajesh P. N. Rao, *Brain-Computer Interfacing: An Introduction*, Cambridge University Press, 2013
- Neuralink 官方 —— https://neuralink.com/
- BCI Society —— https://bcisociety.org/

### 人机共生研究
- Stuart Russell, *Human Compatible: Artificial Intelligence and the Problem of Control*, Viking, 2019
- Pattie Maes (MIT Media Lab) Fluid Interfaces Group —— https://www.media.mit.edu/groups/fluid-interfaces/overview/

### llive 相关
- llive 仓库 —— https://github.com/furuse-kazufumi/llive
- 本系列第 1 部 [15]（构建论）/ 第 2 部 [16]（运营论）
- 本次会话 SUMMARY.md —— `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`

---

# 한국어

# Will Caster 와 Andrew NDR114 가 지향한 것 — llive 의 비전론

> 📚 **연재 내비**: ← #16 삼자(三自)의 정신으로 AI 운영 ｜ **#17 본 글** ｜ #18 GPU 없는 PC 가 주역인 LLM 기반 → ｜ [연재 LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ 각 글은 단독으로도 읽을 수 있습니다(링크는 연재 간 회유용).

**한 줄 hook**:
LinkedIn 프로필 사진을, 자신의 얼굴과 로봇을 이미지 생성 AI 로 융합한 한 장으로 해 두었다. 농담이 아니다. **언젠가 AI 와 사람이 융합할 수 있다면 재미있겠다**고 진심으로 생각하고 있다. 그 첫걸음으로서의 llive.

---

## "두 번째 뇌" 시리즈 제 3 부 — 비전론

본 시리즈는 지금까지 2 부 구성이었다.

| 부 | 테마 | 글 |
|---|---|---|
| 제 1 부 | **구축론** — 30 년 경험 + Perplexity + Claude Code + TRIZ + RAG | [15] |
| 제 2 부 | **운영론** — 삼자의 정신 + 매니지먼트 서적 | [16] |
| **제 3 부** | **비전론** — Will Caster 와 Andrew NDR114 | 본 글 |

구축(어떻게 만드는가) → 운영(어떻게 굴리는가) → 비전(**왜 만드는가**). 순서가 거꾸로라고 느낄지도 모른다. 왜 그렇게 했는지는 마지막에 적는다.

## 두 편의 영화

필자는 두 편의 영화로부터 강한 영향을 받았다.

### Transcendence (트랜센던스, 2014)

Dr. Will Caster(Johnny Depp 연기)가 빈사 상태에서 자신의 의식을 AI 에 **업로드**한다. 영화 후반, AI 화한 Will 은 인류의 지식을 계속 흡수하며 세계 규모로 개입을 시작한다. 찬미와 공포가 공존하는 묘사로, "**만약 인간의 의식을 AI 로 옮길 수 있다면 무슨 일이 일어날까**"를 정면으로 묻는 작품.

### Bicentennial Man / 한국 제목 "바이센테니얼 맨", 일본 제목 "앤드류 NDR114" (1999)

가정용 로봇 Andrew(Robin Williams 연기)가 오랜 시간에 걸쳐 감정·창의성·자유의지·신체성을 획득하고, 끝내 "**인간으로 인정받기**"를 추구한다. 원작은 Isaac Asimov 의 동명 단편. "로봇이 인간이 되는" 것이 아니라 "**인간이란 무엇인가를 AI 가 묻는**" 이야기.

양자는 방향이 반대지만, 공통점은 분명하다: **사람과 AI 의 경계가 사라지는 미래**. 필자는 이 미래를 "재미있다"고 여기고, 그것을 **엔지니어링으로 전진시키는** 것을 개발의 드라이버로 삼고 있다.

### ☕ 잠깐 곁길로

Andrew NDR114 의 원제 *Bicentennial Man*(200 년 사는 남자)은 Asimov 의 단편 *The Bicentennial Man*(1976)이 원작이다. Asimov 는 "로봇공학 삼원칙"을 발명한 사람이지만, 만년의 작품에서는 **삼원칙 자체를 흔드는** 방향으로 향했다. Andrew 는 그 도달점이라 할 수 있다. 기술 규칙도, 인간 마음의 움직임 앞에서는 흔들린다.

## LinkedIn 프로필 사진 — 시각적인 선언

필자의 LinkedIn 프로필 사진은, 자신의 얼굴과 인간형 로봇의 요소를 이미지 생성 AI 로 융합시킨 것을 쓰고 있다. 이것은 장난이 아니라, **언젠가 그렇게 될 미래를 이미 비주얼로 선언**하고 있는 것이다.

기술 블로그·OSS 리포·LinkedIn 게시물 모두가 "장차 마땅히 있어야 할 모습으로 향하는 한 걸음"으로서 정합한다. 시각 요소도 그 일부다.

## llive 의 각 기능은 비전을 향한 준비층

llive 에서 이번 세션에 1270 PASS 까지 쌓아 올린 기능군을, 비전의 관점에서 다시 읽으면 이렇게 된다.

| llive 기능 | 융합 비전에 대한 기여 |
|---|---|
| **FullSense**(전감각 통합 umbrella) | 사람 + AI 의 경계 모호화에 필요한 감각 통합층 |
| **두 번째 뇌**(Claude Code + RAG 약 5 만 건) | **이미 부분적 융합**(뇌의 외연으로서의 지식 접근) |
| **SIL ledger / SEC-03 hash chain** | 융합 시 "누가 책임을 지는가" 의 audit 기반 |
| **Approval Bus + HITL** | 융합 이행기의 인간 판단 게이트 유지 |
| **삼자의 정신(AI 자율)** | Andrew NDR114 적인 자율성 획득 과정 |
| **RAD bci / neuroscience / neural_signal / prosthetic_neural / cognitive_ai / neuromorphic**(6 분야 코퍼스) | BCI 경유 융합의 지식 기반 |

특히 마지막 RAD 6 분야는, 본 시리즈의 "두 번째 뇌"를 **물리적인 BCI(Brain-Computer Interface, 뇌-컴퓨터 인터페이스)**로 확장하는 중기 로드맵이다. 코퍼스는 이미 구축 완료, 구현은 다른 프로젝트(mcp-3d 등)와의 통합 대기 중이다.

## 단기 / 중기 / 장기 로드맵

| Term | 내용 | 현황 |
|---|---|---|
| 단기(현재) | 두 번째 뇌형 개발(Claude Code + RAG + Perplexity) | **실증 완료**(본 세션 1270 PASS) |
| 중기(1-3 년) | BCI 경유 인터페이스 | RAD 6 분야 코퍼스 준비 완료, 구현은 다른 프로젝트에서 |
| 장기(3-10 년) | 의식 업로드 or Andrew 적 양방향 | 비전 단계, llive 의 SIL/Approval 이 바탕 |

단기는 이미 손 안에서 돌아가고 있다. 본 시리즈에서 몇 번이나 언급한 "30 년 경험 + Claude Code + RAG = 팀 속도"는, **뇌의 바깥에 두 번째 뇌를 구축한 상태**다. 이를 물리 융합으로 확장하는 것이 중기, 의식 업로드까지 확장하는 것이 장기다.

### ☕ 잠깐 속마음

솔직히 말하면, BCI 주변은 필자의 전문(이미지 처리 / 삼차원 계측)과는 조금 어긋나 있다. 그래서 RAD 6 분야 코퍼스를 준비한 것은 "**나중에 자신이 곤란해지지 않기 위해서**"이기도 하다. 장기 비전을 그릴 때, 지식이 없는 도메인에 발을 들여놓을 각오가 필요하지만, 그 불안은 **먼저 코퍼스를 쌓아 두는 것**으로 작게 만들 수 있다.

## 왜 비전론을 마지막에 썼는가

비전론을 처음에 써 버리면, 기술 기사가 SF 나 비전 스피치처럼 보여 버린다. 독자는 우선 "구현으로 무엇이 돌아가고 있는가" "어떻게 운영하고 있는가"를 확인하고 싶어 한다. 그것을 #15(구축론)과 #16(운영론)에서 보여 준 다음, **"실은 이 전부가 비전을 향한 준비층이에요"**라고 밝히는 편이 설득력이 있다.

기술 기사는 비전에서 시작하면 약해진다. **구현에서 시작해 비전으로 매듭짓는** 편이 강해진다. Andrew NDR114 가 오랜 시간에 걸쳐 하나씩 획득해 갔듯이, llive 도 한 기능씩 쌓고 있다. 그 축적이 언젠가 "사람과 AI 의 융합"으로 이어진다.

## 맺음말 — "언젠가"를 위해 오늘 할 수 있는 것

"언젠가 AI 와 사람이 융합할 수 있다면 재미있겠다"는 것은 막연한 바람처럼 들릴지도 모른다. 하지만, 오늘 할 수 있는 구체적인 준비는 분명히 있다.

- **두 번째 뇌**를 뇌의 바깥에 구축한다(구축론 #15)
- **삼자의 정신**으로 AI 에 자율성을 넘기는 훈련을 쌓는다(운영론 #16)
- **audit 가능한 의사결정 기반**을 SIL ledger 로 남긴다(본 글 §llive 기능)
- **BCI / neuroscience 코퍼스**를 준비해 둔다
- **시각적 브랜딩**으로 미래를 선취한다(LinkedIn 사진)

이것들은 "언젠가"를 위해서가 아니라, **오늘부터 팀의 생산성을 높이는 수단**으로서 이미 유효하다. 융합은 부산물로서, 혹은 최종형으로서, 자연스럽게 가까워진다.

llive 는 Apache 2.0 + Commercial dual-license 의 OSS, Repo 는 https://github.com/furuse-kazufumi/llive . 본 시리즈 3 부(구축론 / 운영론 / 비전론)에 공감하는 분은, Issue / Discussion 으로 꼭.

---

**"두 번째 뇌" 시리즈 완결**:
- [15] 30 년 경험 + Perplexity + Claude Code + TRIZ + RAG = 두 번째 뇌(**구축론**)
- [16] 삼자의 정신 — 압도적 성과 매니저 식의 AI 운영론(**운영론**)
- [17] Will Caster 와 Andrew NDR114 가 지향한 것(**본 글 / 비전론**)

## 참고 문헌 / 참고 리소스

### 영화
- *Transcendence*, Wally Pfister 감독, Warner Bros., 2014
- *Bicentennial Man*(일본 제목 "앤드류 NDR114"), Chris Columbus 감독, Touchstone Pictures, 1999
- Isaac Asimov, *The Bicentennial Man and Other Stories*, Doubleday, 1976(영화 원작)

### BCI / 신경공학
- Miguel A. L. Nicolelis, *Beyond Boundaries: The New Neuroscience of Connecting Brains with Machines—and How It Will Change Our Lives*, Times Books, 2011
- Rajesh P. N. Rao, *Brain-Computer Interfacing: An Introduction*, Cambridge University Press, 2013
- Neuralink 공식 — https://neuralink.com/
- BCI Society — https://bcisociety.org/

### 인간-AI 공생 연구
- Stuart Russell, *Human Compatible: Artificial Intelligence and the Problem of Control*, Viking, 2019
- Pattie Maes (MIT Media Lab) Fluid Interfaces Group — https://www.media.mit.edu/groups/fluid-interfaces/overview/

### llive 관련
- llive 리포지토리 — https://github.com/furuse-kazufumi/llive
- 본 시리즈 제 1 부 [15](구축론) / 제 2 부 [16](운영론)
- 본 세션 SUMMARY.md — `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`
