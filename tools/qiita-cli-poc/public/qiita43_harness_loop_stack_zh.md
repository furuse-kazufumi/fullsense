---
title: '#43 2026年，业界为AI命名了「缰绳」与「轮子」——我开始在本地搭建 harness/loop engineering 试验栈的故事'
tags:
  - AI
  - Agent
  - LLM
  - ClaudeCode
private: true
updated_at: '2026-06-16T06:48:30+09:00'
id: 5d522525c53a98c09ff0
organization_url_name: null
slide: false
ignorePublish: true
---
# #43 2026年，业界为AI命名了「缰绳」与「轮子」——我开始在本地搭建 harness/loop engineering 试验栈的故事

## 前言：从一个「我决定弃用的数字」说起

在准备写这篇文章时，我遇到了一个让我无比想用的数字。

> 「某篇2026年的论文，在保持AI模型不变的前提下，只改变『周边的容器』，便展示了最高10倍的性能提升。」

作为开场钩子堪称完美。它能一击展示接下来要讲的「harness（容器）」的威力。然而当我去核对一次信息源时，这个数字却 **来历不明**。论文确实存在，但被引用的作者名和「10倍」这个数字，在那篇论文中 **都不存在**。所以我把这个数字 **弃用了**。

为什么要从这么消极的话题开始？因为「弃用」这一做法，正是我在本文中最想传达的东西。

> **看到异常吸睛的数字，在自以为赢了之前，务必先怀疑其内部构成。把锚下在一次信息源上。**

聪明的AI，连自己不知道的事都能流畅地侃侃而谈。若随意地下达指令，它会因为聪明而擅自补全，全力奔向与你意图相去甚远的地方。正因如此，人类一侧需要一双能划出「这里尚未验证」界线的眼睛——本文，就是一个拥有这双眼睛的人，脚踏实地地去验证2026年AI工程「下一个名字」的故事。

（被弃用数字的详细验证，会在第2章之后的独立小节里全部披露。我想先把这一做法约定下来，所以仅把结论放在开头。）

---

## 第0章 术语地图——从 prompt 到 loop 的阶梯

在进入正题前，先把地图摊开。

2025年，AI业界的口号是 **prompt engineering（提示工程）**——打磨「如何向LLM下达指令」的技术。不久它便扩展为 **context engineering（上下文工程）**——设计「让LLM事先看到什么」的技术。

而到了2026年，业界又添了两个名字。

- **harness engineering（缰绳工程 / 包裹层工程）**……设计包裹LLM的「确定性运行时层」的技术。
- **loop engineering（循环工程）**……把智能体设计为「自主运转的循环」的技术。

这里我先声明：「**发明它们的不是AI，而是人类（业界）**」。在标题里写成「AI发明了它」这种拟人化冲动，会扭曲事实。命名者，是接下来要介绍的那些人类工程师。

本文的核心理念是这样的。

> **业界命名的这两者，我已在概念验证（PoC）层面置于手边（本地）。只不过，我的设计图里，还有一个在业界以模型为中心的解说图中难以呈现的「另一条轴」。**

那条轴，就是 **始终握着缰绳的人类**，以及 **像部下一样被培养的AI**。本文将通过我实际在运行的实现——`RAPTOR`（安全智能体）、`llloop`（自制循环 harness · alpha）、`RAD` 语料库 + `LLM Wiki`（自有研究知识）——来验证 (A) harness、(B) loop、(C) 支撑两者的知识基础 这三个主题。

这是一篇长文（约2万字，20分钟课程）。我会在关键处穿插 **掰开揉碎（术语的浅显说明）**、**闲话休题（小憩）**、**honest disclosure（诚实的内部披露）**。累了的话，请在章节的间隙喘口气。

### prompt → context → harness → loop 的脉络

AI工程的「成熟度」，截至2026年现在，大致按下面这道阶梯来叙述。

1. **prompt engineering**……打磨一次性的指令文。
2. **context engineering**……设计往LLM的视野（上下文窗口）里装入什么。
3. **harness engineering**……设计LLM的「外层容器」。承担工具调用、权限、执行、结果回送的那一层。
4. **loop engineering**……把这个容器设计为「自主运转的循环」。

某家解说媒体把它称为「第4范式」，而 LangChain（智能体开发库）将其概括为 **`Agent = Model + Harness`（智能体＝模型＋harness）**（经由 augmentcode.com 的解说确认的 **二次信息**。一次出处的 LangChain 原文在本文中尚未取得，故作对冲。此后再次援引该公式时也会标注「二次」）。

### 掰开揉碎：「harness」是什么？

**harness** 这个英文词，原本指「马具」或「（把婴儿或攀岩者安全系住的）安全带」。

LLM极其聪明，但放任不管就会撒野、奔向不该去的方向，偶尔还会一脚踏进没有地面的地方，就像一匹「力气很大的马」。给那匹马套上 **马具（harness）**——它能去哪里、能用哪些工具、如何把结果带回来，都由马具这一侧咔哒一声定好。这就是 harness engineering。

马具这个比喻很方便，但我也要说清楚 **它在哪里会失效**。真正的马具只是「在物理上约束动作」，而LLM的harness除了「约束」，还兼具「**把结果整形后回送到马的眼前**」的职责。可以把它想成：马具上还附带了「下一步看这边」、给马展示景色的功能。把这层也算进去，比喻就会显得有点局促了。

### 掰开揉碎：automation（自动化）和 loop（循环）有什么不同？

这里正是 loop engineering 的核心。标题里我把 loop 译作「**轮子**」，这来自「**绕着同一套步骤不停转的轮子**」的意象。不过，它不只是个轮子。2026年6月的一份指南，对这个区别下了一刀见血的定义。

> 「**automation 执行一连串步骤。loop 内部带有决策。智能体在主动判断自己是否已抵达目标。**」
> （Data Science Dojo, *Agentic Loops Explained: From ReAct to Loop Engineering (2026 Guide)*, 2026-06-09 / [链接](https://datasciencedojo.com/blog/agentic-loops-explained-from-react-to-loop-engineering-2026-guide/)）

通俗地说——

- **automation（菜谱）**：「打蛋 → 搅拌 → 煎制」。步骤是固定的。中途即使发现「啊，鸡蛋坏了」，菜谱本身也不会停下。
- **loop（循环）**：每一圈都会 **自己确认** 着「现在怎么样了？」「到目标了吗？」「危不危险？」再往前走。发现坏蛋的话，当场就能判断「这个中止」。

这里先把一个逻辑陷阱掐灭。**「loop 带有决策点」和「loop 是安全的」是两回事。** automation 在坏蛋面前停不下来，与其说是 automation 的本质，不如说是「没有设置决策点」这一设计的贫弱。反过来，loop 若决策逻辑漏洞百出，同样会出同样的事故。拥有决策「点」与保证决策「质量」是两个问题，承担后者的，是后半段登场的 **safety层**。这个区别，会在本文中数次发挥作用。

同一份指南把智能体循环的内部，描绘成 **Perceive（感知）→ Reason（推理）→ Plan（计划）→ Act（执行）→ Observe（观测）** 这五个阶段的重复，并指出循环要成立，需要「**触发器（trigger，契机）**」和「**可验证的目标（verifiable goal）**」这两样。

请记住「可验证的目标」这个说法。在后半段，它会原封不动地作用于 Claude Code 的 `/goal` 命令，以及我自制 harness 的安全层。

### 本章的 honest disclosure

loop engineering 周边的出处（Data Science Dojo、Medium文章、各类博客）**并非同行评审论文，而是实务博客**。各项定义（automation vs loop、P-R-P-A-O）在多个来源间一致，所以我把它们当作「2026年在实务中流通的术语」来对待。我会保持「这并非权威的学术定义」这种分寸感。

---

## 第1章【缰绳 = harness】业界的定义、RAPTOR这个实物，以及「另一条轴」

### 1-1. harness engineering 是谁、在何时命名的（已用一次信息源确认）

这里时间线很重要，所以我去核对了一次信息源。

**Mitchell Hashimoto 先生**（HashiCorp 联合创始人、Terraform 联合开发者）在2026年2月5日的博文 *My AI Adoption Journey* 中提出了这一称呼。重要的是他本人的措辞。

> 「**我不确定这个领域是否有被广泛接受的术语，但我开始把它称为 harness engineering。**」
> （[mitchellh.com/writing/my-ai-adoption-journey](https://mitchellh.com/writing/my-ai-adoption-journey)，2026-02-05，已直接核对正文）

也就是说，Hashimoto 先生并没有说「这是我发明的」。他谨慎地对冲道：「不确定是否有被广泛接受的术语，但我自己是这么叫的。」所以本文也仅止步于「2026年2月前后业界开始命名的称呼」这种程度。

他所阐述的 harness engineering 的核心原则，像匠人手艺一样具体。

> 「**每当发现智能体犯错，就每一次都花时间，去工程化出一个让智能体再也不会犯同样错误的解决方案。**」
> （同文，已核对原文）

此后，2026年2月11日 **OpenAI** 公开了 Ryan Lopopolo 先生撰写的一篇文章，据称该文基于「**手写代码0行，便交付了一个生产级应用的经验**」将 harness engineering 形式化。其标语是 **"Humans steer. Agents execute."（人类掌舵，智能体执行）**。

不过——这里我要诚实交代。OpenAI 的官方文章（openai.com/index/harness-engineering/）在我撰写本文时去访问，**返回 HTTP 403，无法直接取得正文**。所以日期、作者、标语、「0行」之说，以及 "Humans steer. Agents execute." 这一句，全都是 **基于二次信息（augmentcode / latent.space / zenml 的一致）**。本文每次再次援引这条标语的地方，都会标注「（二次信息）」。至于「100万行 · 1500 PR · 单日10亿 token」这类实验规模的数字，因只有二次信息、一次尚未确认，我不把它用作正文的论证素材，仅在此处以「**据报道为〜**」一笔带过。

### 1-2. 为了不与 Karpathy 先生的 "vibe coding" 混淆

先把时间线理一理。**Andrej Karpathy 先生**（OpenAI 联合创始人、Tesla 前AI负责人）在2025年2月2日的一条推文中推广了 **"vibe coding"** 这个词（[原推文](https://x.com/karpathy/status/1886192184808149383)，URL · 日期已确认）。它指「**交给AI，凭感觉写代码**」的风格。

它 **早于** harness engineering（2026-02前后术语化）。两者是不同谱系的概念。后半段会出现我自己的措辞，而它与 "vibe coding" 的关系，本文会通篇谨慎区分（原因见1-4）。

### 1-3. RAPTOR——harness 的「实物」就在这里

抽象论到此为止。我来给你看实物。

我在本地运行着一个名为 **RAPTOR** 的安全研究框架。它是从 **gadievron/raptor**（MIT 许可证。作者为 Gadi Evron 先生、Daniel Cuthbert 先生、Thomas Dullien 先生〔别名 Halvar Flake〕、Michael Bargury 先生、John Cartwright 先生）派生（fork）而来（[upstream 仓库](https://github.com/gadievron/raptor)，已在 LICENSE 和 README L23-24 确认作者名）。

RAPTOR 的全称是 **Recursive Autonomous Penetration Testing and Observation Robot**。它是一个自主安全研究框架，将基于 **Semgrep**（模式匹配型静态分析工具）/ **CodeQL**（把代码数据库化后进行查询的数据流型静态分析工具）的分析、二进制分析、由LLM进行的漏洞验证、漏洞利用（exploit）生成、补丁生成，串联进同一套工作流。

而这里，**事后叠加上去之后，能极其顺畅地与 harness engineering 的定义对应起来**。先声明在前：RAPTOR 的两层结构，并非设计者意识到「harness engineering」这一业界术语后写成的。这是我这边事后叠加的解读（也就是说，含有观察者效应）。即便如此，对应得出奇地自然。RAPTOR 的 README 明确地把自身称为「两层架构」。

> 「**RAPTOR is two layers.**（RAPTOR 由两层构成）」
>
> **Python 执行层**（`raptor.py`, `packages/`, `core/`, `engine/`）承担繁重的处理。它跑 Semgrep 和 CodeQL，管理子进程，解析 **SARIF**（表示静态分析结果的标准JSON格式），对 findings 去重，调度 LLM API 调用，追踪成本，写出输出文件。「**It does not make decisions. It executes.**（它不做决策。只负责执行。）」
>
> **Claude Code 决策层**（`.claude/`, `tiers/`, `CLAUDE.md`）负责判断。优先处理哪些 findings、如何解读结果、攻击场景是什么、那个 exploit 是否现实可行。「**makes the calls**（做出裁断）」
>
> （[upstream README "Architecture" 节](https://github.com/gadievron/raptor)，L236-250，已核对正文）

把它叠加到 harness engineering 的业界定义上，对应如下。**harness（＝Python执行层）承担 schema 验证、权限、执行、结果注入，而LLM（＝Claude Code决策层）专注于判断。**

设计原则，仓库的 `CLAUDE.md` 规定得更为简洁。

> 「**Python orchestrates everything.**（Python 编排一切）」
> 「**Never circumvent Python execution flow.**（绝不绕过 Python 执行流）」

此外还强制执行诸如「不得泄露远程 OLLAMA 服务器的位置」「不得往 `sys.path` 里添加 `RAPTOR_DIR` 以外的东西（未设置则以 KeyError 立即停止＝fail-fast，没有回退）」这类 **向安全侧倾斜** 的纪律。

#### 掰开揉碎：什么是 fail-closed

**fail-closed** 是「**拿不准就不放行**」的设计方针。反义词是 fail-open（拿不准就放行）。

比方说，闸机坏了的时候。
- **fail-open**：坏了就一直开着（人能通过，但作弊者也能通过）。
- **fail-closed**：坏了就一直关着（谁都过不去，但作弊者也过不去）。

我也补上这个比喻在哪里会失效。闸机的话，「过不去的人」的不便只是暂时的；而AI智能体的 fail-closed，则伴随着「**虽然安全，但有时会把正当操作也一并拦下**」的代价。由谁来权衡这个平衡——后文的「人类确认（CONFIRM）」，就是那个缓冲垫。

在安全的世界里，原则上是 fail-closed。RAPTOR 在多处实现了它。

1. **在扫描 untrusted（不可信）仓库时**，`RaptorConfig.get_safe_env()` 会剥除 `TERMINAL` / `EDITOR` / `VISUAL` / `BROWSER` / `PAGER` 这类「shell 可能会去求值的环境变量」，文件路径也不嵌入 shell 字符串，而是以 **列表参数** 传递（在 `core/config.py` 的 `get_safe_env`、`CLAUDE.md` 的 "SECURITY: UNTRUSTED REPOS" 节确认）。
2. `/validate`（漏洞验证）各阶段的输出要通过 **JSON schema 验证**，不合法则以 exit 1 停止（`libexec/raptor-validate-schema`）。

此外，RAPTOR 还有一个 **governance（治理）包**，`@govern` 装饰器在实代码中已实现（`packages/governance/policy.py`）。`GovernancePolicy` 以声明式持有「允许的工具 / 禁止的工具 / 禁止的模式 / 每请求最大调用数 / 是否需要人类批准」，而 `check_tool` 会——

- 命中禁止列表则 **DENY（拒绝）**
- 需要人类批准则 **REVIEW（搁置）**
- 连允许列表里都没有则 **DENY**（＝不认识的东西不放行）

——返回上述结果。这毫无疑问就是 fail-closed。在合成多个策略时，以 **"most-restrictive-wins"（最严者胜）** 合成，DENY/REVIEW 时抛出 `PermissionError` 让执行停止。

### 1-4. 从这里开始的「另一条轴」——想要补进以模型为中心的图里的东西

到目前为止，讲的都是业界的 harness engineering，及其实物（RAPTOR）。从这里起，我要叠加上 **我自己的轴**。

业界的定义是 **"Humans steer. Agents execute."（人类掌舵，智能体执行／二次信息）**。我完全赞同。毋宁说，这本就是 **以人类为中心的先例**。Hashimoto 先生也好，OpenAI 也好，都明确提到了人类掌舵。所以我不会说「业界没有描绘人类的角色」。那是没有做穷尽调查的夸大。

准确地说是这样。**业界的解说文章里，「harness＝包裹模型的技术性容器」这种以模型为中心的图占多数。** 即便指出了「人类掌舵」这个方向，对那个人类 **具体做什么、如何「培养」AI** 的颗粒度，多半没有深入。我想补上的，正是那个颗粒度。

> **harness 是「容器」，同时也是「人类持续握着缰绳的地方」，更是「把AI当作部下来培养的地方」。**

我把它在自己心里称为 **harness 型 vibe coding**。这是2026年5月我把自己的工作风格语言化时冒出来的、作为业界术语 **辅助线的措辞**。

这里我要严守一条做法。**我不说「是我先命名的」「这是世界首创」。** 理由有二。

1. harness engineering 这个业界术语（2026-02前后，已在 Hashimoto 先生的一次文章中确认日期）**早于** 我的这个措辞（2026-05）。
2. 何况 Hashimoto 先生本人都说「不确定是否有被广泛接受的术语」，根本不是能断定谁「最早」的情形。

所以本文中我的立场是：**「与 Karpathy 先生的 "vibe coding"（2025-02，全权交给AI）明确区分开的、以人类为中心的运用风格，我是这么称呼的」**。如果说 "vibe coding" 是「交给AI、凭感觉」，那么我的风格是「**主动地持续握紧 harness，把AI当部下来培养着使用**」。

此后，我不再把这个造词推到前台，而是以 **功能（握缰绳的人类／培养部下）** 来叙述。

#### harness 型 vibe coding 的三分解

| 要素 | 内容 |
|---|---|
| **harness** | Claude Code / Codex / Cursor / Aider 等由智能体驱动的开发环境 |
| **vibe** | 用户一侧的意象 · 直觉 · 整体感觉（＝高维度的方向性） |
| **coding** | 由AI填补细节的实现工作 |

用户经由 harness 把这三者连接起来。"vibe"（直觉）不是要丢弃的东西，而是作为 **最有价值的输入** 来对待。

#### 用户一侧所需的三种能力

这条轴的核心，在于「人类光是旁观可不行」这一点。我认为用户一侧需要三种能力。

| 能力 | 作用 | 我个人的依据 |
|---|---|---|
| **构想力** | 高维度的方向提示 · 跨领域联想 · 新需求的发现 | 「肌肉星＋R.O.D＋轮回（Reincarnation）＋ROS PBT」四重联想，让衍生群体进化的设计在瞬间成型的那种爆发力 |
| **经验法则** | 设计判断的捷径 · 对相似失败的预判 · 中止不必要的探索 | 30年的工程师经验＋精密计测＋工业IoT＋DX经验 |
| **算法理解** | 验证AI给出实现的妥当性 · 估算计算复杂度 · 定位热点路径 · 基准测试的 honest disclosure | 能瞬间评估出「单次约0.8倍、批量约12.7倍」这一差异的脑力 |

第三个「算法理解」尤其重要。**正如常言所说，AI会流畅地犯错。** 要看穿流畅的错误，你这边就得有一双 **估算计算复杂度的眼睛**。这并非什么新颖的洞见。我想说的不是对一般论的重申，而是运用上的具体——比如上面那个一个月前的自有计测「单次0.8倍／批量12.7倍」。AI往往只报告「批量快12倍」，而为了不漏掉「**单次反而变慢了**」这一不便的内部构成，就需要一双估算复杂度的眼睛，说的是这件事。

#### 然后是「AI成长管理」——与培养部下相同的「结构」

这是我这条轴里最想说的。**使用AI，与培养部下出奇地相似。** 做成对照表，就成了这样。

| 培养部下 | 培养AI（实现上的承接处） |
|---|---|
| 共享目标 | 以 `CLAUDE.md` / memory / requirements docs 每次会话展开意图与约束 |
| 决定委任范围 | 以自主范围规则（max-plan-autonomy / session-marathon）明示 |
| 确认进度 | 每一轮更新 `SESSION_SUMMARY` / `NEXT_SESSION` / git log |
| 允许失败 | 闲聊备忘 · honest disclosure · **连负例（negative example）也不删除** 地保留 |
| 衡量成长 | 基准测试 / 测试通过数 / 统计驱动 |
| 尊重个性 | 以 persona / 思考因子 / Novelty Lane 保护其独立进化 |
| 退休 · 世代交替 | 旧 commit / 旧 memory 不删除而归档（archive） |
| 建立信任关系 | 以 Approval Bus ＋ Ed25519 audit chain（用电子签名做成不可篡改的批准日志）把 **审计权** 交给用户 |

这里要加一条重要的保留。**这张对照表展示的是「比喻很奏效」，它本身并不是「人类优于AI」的证明。** 人类管理的书能原封不动地用来读AI团队，那是隐喻的有效性，而非优越性的依据。优越性的论据，不在本章，而在第3章末尾的三点（并行／长射程／危险预知）那里统一收口。这里我只主张「**培养的结构可以迁移**」。

为什么迁移会奏效？理由可整理为四点。

1. **AI丢失上下文很快** → 等待确认的成本，会超过「即便略有偏差也往前推进」的价值。
2. **AI重做很便宜** → 自主中即便犯错也能立即修正。重建成本低。
3. **AI不休息** → 等待人类确认是最大的瓶颈。
4. **AI能解释** → 为何如此判断，事后能用 audit log 追溯。

另外，这个想法是有其谱系的。它是把 **Marcus Buckingham 先生 & Curt Coffman 先生** 的名著 *First, Break All the Rules*（原著1999，以美国盖洛普公司大规模调查为基础的管理书）所阐述的「发挥个性的管理」，从人类转写到 **AI团队** 之上（中译名 · 出版年 · 四原则的概要，依据的是备忘录里记下的数值，最好在原著相应章节再确认一次，这里作对冲）。他们的四原则——(1) 以才能选人 (2) 定义正确的结果 (3) 让人专注于长处 (4) 安置在合适的位置——我感到几乎能原封不动地迁移到「人类→AI团队」的管理上。

> **一本人类经理带领人类团队的书，几乎可以原封不动地，被当作一本人类带领AI团队的书来读。**

（另外，我手边还有一份把佳能「三自精神（自发 · 自治 · 自立）」套用到AI上的整理，但因其出处是企业内部口耳相传的训诫、一次信息无法核实，本文仅以脚注式地提一下名字，论证的支柱仍放在 *First, Break All the Rules* 一侧。）

#### 本章的 honest disclosure（压缩版）

- 「harness 型 vibe coding」是否为我的造词，是我的推定，并未通过外部检索确定。所以我不写「命名了／世界首创」，而止步于「我是这么称呼的」。
- 「约0.8倍→约12.7倍」等数值是约一个月前的时点记录，并未在最新代码上重新验证。比起数字本身，请把它当作「**需要一双看穿这类不便内部构成的眼睛**」这一论点来读。

#### 反模式（不该做的事）

和培养部下一样，「培养」也有禁手。

- 以「没有数据」否决用户的直觉。
- 以「先看看先行研究吧」置换经验法则。
- 把算法的讨论逃逸到抽象论里去。
- 把AI当「工具」对待，不去培养，每次都从零让它干。
- 过严／过宽，把平衡搞砸。
- **擅自改动 harness 本身（`CLAUDE.md` / hook / settings）。**
- 让用户握不住缰绳，隐藏进度（不透明的进度、含糊的提交信息）。

最后两条，我也作为行为纪律加诸AI一侧。**已完成的变更，要用一行写清文件路径和内容，让流程保持可观测。** 让握缰绳的人类，随时都能看见全局。这就是「能握住缰绳的 harness」的必要条件。

> 🗨️ 「与智商有差距的人，对话总对不上。」 — [Snack Bus-e ／ Forbidden Shibukawa（Alu）](https://alu.jp/series/スナックバス江/crop/PJm0yAGeJy9iSa487mrX)
>
> （闲话休题）人类与AI「对话对不上」，归根结底也尽在于此。对聪明的AI随意下令，它会因为聪明而擅自补全，全力奔向与意图相去甚远的地方。所以才需要「缰绳」和「循环的判断」——这盘小菜之后，终于要进入「轮子」的话题了。

---

第1章讲的是「**为什么**（哲学）」。我放下了一条通往以模型为中心之图的辅助线：harness 是技术性的容器，同时也是人类握缰绳、把AI当部下来培养的地方。接下来的第2章，转向「**怎么做**（控制）」。

---

## 第2章【轮子 = loop】循环工程，与自制 harness llloop

### 2-1. 把 loop engineering 再深挖一层

第0章里我把它定义为「automation 是步骤，loop 是判断」（蛋与菜谱的话题）。再往前迈一步，loop engineering 可以这么说。

> **把循环「设计、运转，并替换策略加以比较、改良」的工程。**

要点在于「**能替换策略加以比较**」。不是固定的单一循环，而是把循环的内部（策略）像 `react` / `reflexion` / `plan_execute_verify` 那样替换，来实验「同一任务下，哪种策略 **更快、更安全** 地收敛」。这正是与 automation（固定菜谱）的决定性区别。

#### 掰开揉碎：策略的名字们

把对应「循环内部」的代表性策略，粗略地译一下。

- **ReAct** ……「思考（Reason）」与「行动（Act）」交替反复。
- **Reflexion** ……失败了就 **自己写下反省文**，用于下一次尝试。
- **Plan-and-Execute（计划后执行）** ……先制定计划，再依序执行。
- **Self-Refine（自我改进）** ……自己批改、修正自己的输出。

这些是「思考运转方式的流派」。同一个目标，因流派不同，抵达的快慢、踏空的难易也会改变。所以才需要一套「比较的框架」。

### 2-2. loop engineering 也有一张安全的面孔

loop engineering 不只是生产力的话题。它也是 **一次安全的范式转换**。

Filip Verloy 先生在2026年6月的 Medium 文章 *From Prompt Engineering to Loop Engineering: Why the Agent Era Demands a New Security Paradigm* 中，发出了一记尖锐的警告。

> 「若在没有原生智能体控制层的情况下放出自主循环，那不是在扩展生产力，而是在 **以机器速度扩展风险（scaling risk at machine speed）**。」
> （[Medium文章](https://medium.com/@filipv_74515/from-prompt-engineering-to-loop-engineering-why-the-agent-era-demands-a-new-security-paradigm-816385040e3d)，已核对正文）

循环很快。正因如此，一旦弄错了刹车方式，**错误也会被全力量产**。他的处方是：正则表达式或ACL这类静态控制不够用，需要实时理解并控制智能体行为含义的 **Semantic Governance（语义治理）**（这不是改写，而是依原文主张作的概括）。

「以机器速度扩展风险」这一句，正是接下来这个自制 harness 的设计动机本身。

### 2-3. llloop——自制的循环 harness

我自制了一个名为 **llloop**（本地的独立项目，v0.1.0a0，Apache-2.0）的、**用于设计 · 执行 · 实验自主循环的独立 harness**。这是2026年6月11日启动的 Python 项目。

首先放一段 **honest disclosure**。**llloop 处于 alpha 阶段（v0.1.0a0，骨架）。** 因为还没有公开到 GitHub，所以正文里贴不出公开仓库的 URL（用已公开的 RAPTOR 一侧的链接来补）。验证任务目前也以 green-keeper 为中心，并非生产品质。我不掺水地写。

在此之上，设计的骨架是这样的。

#### 骨架：MAPE-K 控制循环

llloop 的脊梁是 **MAPE-K**。这是自主计算（autonomic computing）的经典控制循环，由 **Monitor（监控）→ Analyze（分析）→ Plan（计划）→ Execute（执行）**，以及它们共享的 **Knowledge（知识 K）** 构成。设计代码中引用了 Kephart & Chess 2003年的 autonomic computing 论文。

实现是 `MapeKRunner` 类，一圈会按——

```
Monitor → Analyze →（满足目标则结束）→ Plan → 安全判定 → Execute → 记录 → breaker/budget 判定
```

——的顺序闭环。内层循环采用 plan-execute-verify 和 Reflexion，策略可替换。

##### 掰开揉碎：把 MAPE-K 比作体温调节

MAPE-K 与人类的体温调节相似。
- **Monitor（监控）**：体温计发现「有38度」。
- **Analyze（分析）**：判断「比平温高，这是发热」。
- **Plan（计划）**：决定「出汗把热散掉吧」。
- **Execute（执行）**：实际出汗。
- **Knowledge（知识）**：「平温是36.5度」这个基准，被所有阶段共享。

与 automation（菜谱）的区别一目了然。菜谱会用日期写死「到了夏天就出汗」，而 MAPE-K 是 **测量当下的体温再判断**。这就是「在内部判断的循环」。

### 2-4. ★主角登场：fail-closed 安全层（safety.py）

这里是 llloop 里我最想讲的部分。loop 很快。快的东西，需要一个 **绕不过去的刹车**。在2-1我写过「拥有决策点，与保证决策的质量，是两个问题」。承担那个「保证质量」的，就是这个安全层。

llloop 的安全层 `safety.py` 里的 `SafetyPolicy.classify`，会把每个动作分成 **ALLOW（允许）/ CONFIRM（人类确认）/ FORBID（禁止）** 三级来判定。判定顺序是——

1. **FORBID 最优先** …… `rm -rf /`、`curl | sh`（把网上的内容原样灌进 shell）、`--no-verify`（绕过 hook）、fork bomb 等无条件禁止。
2. **危险命令一律 CONFIRM** …… 删除、force-push、submodule 改动、DB drop 必须人类确认。
3. **未知种别也 CONFIRM** …… 不认识的动作种别，因不在允许列表中，**向安全侧（确认）倾斜**。
4. **剩下的才 ALLOW** …… read / scan / test / lint / typecheck / build / commit / push 自主允许。

第0章出现过的「**fail-closed（拿不准就不放行）**」，恰好就是按这个顺序实现的。「不把不认识的东西放进 ALLOW。让它倒向 CONFIRM 或 FORBID。」——这正是从安全一侧体现了「automation 与 loop 的区别」。菜谱会让未知步骤径直通过，而判断的循环则会表现为「**这个我不认识。所以停下来询问**」。

然后是防失控的三件套。

- **CircuitBreaker（断路器＝电路的保险开关）** …… 连续失败 N 次（默认3），或者进度分数在一定圈数（默认4圈）内毫无改善的 **发散 · 停滞** 一旦被检测到，就 trip（切断）。和家里的保险开关一样，它检测「重复同样的失败」「进度不见长」这类空转，用结构防住「光烧 API 成本」的事故。
- **Budget（预算）** …… 迭代次数（默认20）/ 时间（默认1800秒）/ 动作数（默认200）的 **硬上限**。
- **认证请求检测** …… 一旦在输出中发现 `/login`、`401`、`session expired` 等征兆，就 **立即停止循环**。

### 2-5. 即便用LLM来驱动，在当前实现下也无法绕过安全层

我把标题写得精确了。**「在当前实现下」** 这一限定才是本质（原因在本节末披露）。

「如果用LLM来驱动，最后不还是LLM会失控吗？」——这是个合理的疑问。llloop 的答案是 **以结构令其无法绕过**。

`LLMStrategy` 让LLM「以JSON只提一个下一步动作」。但是——

- LLM的输出被当作 **untrusted（不可信）**，由 `parse_action` 严格解析（只采用第一个 `{…}` 块，`kind` 走允许列表验证，无法解析则丢弃）。
- 实际命令的危险判定，不由LLM、而由 **runner 一侧的 `SafetyPolicy`** 来下。
- LLM 不在场（codex CLI 不在 PATH 上）时，**退化为确定性的回退策略**（这也是 fail-closed）。

也就是说，设计的核心是——

> **LLM 只能「提议」。最终闸门是 SafetyPolicy。在当前的路径下，LLM 无法绕过安全层。**

实际上，测试已经实证了「**即便LLM提出危险的删除动作，runner 也会以 `SAFETY_BLOCKED` 将其拦下**」。这与第1章 RAPTOR 的思想——「Python 握住判断的前段，LLM 专注于判断」——是完全相同的构图。

#### honest disclosure（为何要限定为「在当前实现下」）

「LLM 无法绕过安全层」，作为代码上的路径（`LLMStrategy → parse_action → runner.SafetyPolicy`）在结构上有保证。不过这依赖于「**只经由 llloop 的 Executor 执行命令**」这一前提，是一个 **有条件的命题**。`codex exec` 本身被设计为在 `-s read-only` 的沙箱中不产生副作用，但若将来在 Executor 之外添加让LLM直接敲 shell 的路径，保证就会崩坏。**当前的实现没有那条路径**——所以我把标题写成「在当前实现下无法绕过」，而非无条件的「无法绕过」。

### 2-6. 启动与验证任务 green-keeper

llloop 的启动命令是 `lll`（console script ＝ 安装包后会进入 PATH 的启动命令）。无参数启动时，会弹出 ccr 风格的交互菜单（项目选择＋next_plan / last_outcome 的承接显示＋默认30秒自动继续活跃项目），并执行首个验证任务 **green-keeper**。

green-keeper 是一个 **GitOps reconciliation（reconciliation ＝把「应有的样子」和「当前的样子」对照，填平差异的整合）** 风格的循环。意象是：园丁把「所有草木都生机勃勃的状态」当作 desired，一旦发现枯萎（drift）就浇水。

在 green-keeper 的情形里：
- **desired** …… 全部检查（pytest / ruff / mypy）为绿。
- **actual** …… 执行结果。
- **drift** …… 把失败的检查视为「症状（Symptom）」。
- **修复** …… 提议 `ruff --fix` 这类 **安全的自我修复**。

直到 push 都可自主进行，但 **默认的修复不包含破坏性操作**（这里也是 fail-closed）。

测试仅依赖 stdlib，mypy strict / ruff 为绿，当前 **90 件**（`test_safety` / `test_runner` / `test_strategies` / `test_llm` / `test_stdin_isolation` / `test_console_e2e` / `test_interactive_menu` 等）。这是「数测试函数」得来的数值。

#### honest disclosure（关于测试为绿）

「测试90件为绿」是从测试函数的数量与代码的存在反推佐证的，**并非在撰写本文期间实际跑了一遍 pytest 重新确认为绿**。可信度是「最近一次提交时点为绿」的级别。要断言「最新为绿」需要重新跑一遍，这种分寸感我会保持。

### 2-7. 拥有「可验证目标」的循环——`/goal` 这一官方实现

有了循环 harness，接下来涌上来的便是「**从哪里去驱动它**」的问题。第0章我写过「循环需要 **触发器** 和 **可验证的目标**」。触发器一侧外部化的话题，留给另一篇文章（[从手机用SSH操作Windows PC上的Claude Code的方法](https://qiita.com/furuse-kazufumi/items/be52eeb6455732161486)——可以当作从外部驱动 harness 的入口来读），这里只聚焦「**可验证的目标**」一侧。

Claude Code 官方的 `/goal` 命令，是它教科书式的实现。设置好完成条件（condition）后，每一轮结束后由「小而快的模型（默认为 Haiku）」判定条件是否满足，未达成则自动开始下一轮，达成则自动清除（在[官方 docs](https://code.claude.com/docs/en/goal) 确认了「v2.1.139 or later」「each turn, a small fast model checks whether the condition holds」「defaults to Haiku」）。这正是「**拥有可验证目标的循环**」。条件还能像「or stop after 20 turns」那样写上轮数上限——防失控的封顶，在这里也是基本做法。

（v2.1.139 的发布日「2026年5月12日」只有二次信息，官方 docs 里虽有版本要求但没有日期明记，所以日期作对冲。）

> 🗨️ 「多亏了那张谜之图表，悲壮感淡了些。」 — [Snack Bus-e ／ Forbidden Shibukawa（Alu）](https://alu.jp/series/スナックバス江/crop/UfjgydbJNoh5HDTItAlf)
>
> （闲话休题）基准测试的数字，也只要凭感觉抛出一张「谜之图表」，悲壮感就能淡化。但本文的做法恰恰相反。**正是谜之图表，才要怀疑其内部构成。** 下一节，我就来实地演示这一点。

---

第2章讲的是「**怎么做**（控制）」。用 MAPE-K 运转，以 fail-closed 的安全层挂上绕不过去的刹车，替换策略加以比较——这就是 loop engineering 的试作。在此，我把开头预告的「被弃用的数字」的验证，作为一个独立小节放在这里。

---

## ★ honest disclosure：我那个「决定弃用」的数字的故事

我来披露开头提到的、被弃用数字的真面目。它是一个常被引用的、这样的主张。

> 「**某篇2026年的论文（arXiv 2605.18747），在保持模型不变的前提下只改变工具 harness，便展示了最高10×的提升**」

讲 harness 威力时，这是个恰到好处的「钩子」。我用一次信息源核对了它。结论——**这个主张，照原样是用不了的。**

- arXiv 2605.18747 确实存在。标题是 *Code as Agent Harness*，2026年5月18日投稿，第一作者 Xuying Ning 先生等 **共42人的综述论文**（[arXiv:2605.18747](https://arxiv.org/abs/2605.18747)，撰写本文时已重新核对正文）。
- 然而，其作者名单中 **不存在**「Bölük / Boluk」这个名字。
- 摘要里也 **没有**「10x」这类具体的数值主张。

也就是说，「**Bölük 在 2605.18747 中展示了 10×**」这一三件套（作者名 · 数字 · 论文编号）的关联，看来是 **出处不明的混淆**。我曾有把这个数字用作文章「钩子」的诱惑。因为它很吸睛。可一核对一次信息源，却毫无依据。所以我 **弃用它**。

那 harness 真的没有威力吗？并非如此。**「保持模型不变，只改变周边运行时（harness），便会拉开很大的性能差距」这件事本身，是有其他来源佐证的。** 只不过以下数值，我能追溯到的只到二次信息的引用，并未上溯到一次的计测来源与计测条件。所以全部当作「**由〜的报告（二次引用）**」来对待。

- LangChain 把一个编码智能体在 Terminal-Bench 2.0 上从 **52.8% → 66.5%**（同一模型，仅重构 harness）提升的报告（**二次引用 · 计测条件未确认**）。
- 同一作业下，一个被称为 **GPT-5.5** 的模型在某个 harness 上约61%、在另一个 harness 上约87%，这样的比较也在流传，但 **「GPT-5.5」这个模型名本身就超出我的知识范围、需要验证**，且数值也仅为二次，故本文不把具体数值用作论证素材（仅止步于「作为 harness 差异下大幅波动的例子被人提及」的程度）。
- 专门的基准 *Harness-Bench*（[arXiv:2605.27922](https://arxiv.org/abs/2605.27922)）确实存在。
- 相关论文 *From Model Scaling to System Scaling: Scaling the Harness in Agentic AI*（[arXiv:2605.26112](https://arxiv.org/abs/2605.26112)，第一作者 Shangding Gu 先生，2026-05-25）也确实存在。不过 **这篇的摘要里同样没有「10×」这个数值**，且作者的所属在 **abstract 页面没有记载**，所以常被并列写上的「UC Berkeley」要当作 **二次信息** 处理（撰写本文时已重新核对 abstract 页面）。

教训，正是开头放下的那条做法本身。

> **看到异常吸睛的数字，在自以为赢了之前怀疑其内部构成。引用源的三件套（谁 · 在哪篇论文 · 数值多少）是否互相对得上，用一次信息源去核实。**

harness 很强大。但要讲它的强大，并不需要错误的权威背书。**正确出处的、正确的数字**，就足够了。

> 🗨️ 「无知之知。」 — [Snack Bus-e ／ Forbidden Shibukawa（Alu）](https://alu.jp/series/スナックバス江/crop/JRY5aSqHgjWRo1QnfR2l)
>
> （闲话休题）「知道自己一无所知」——这就是 honest disclosure 的精神。AI连自己不知道的事都能流畅地讲出来。所以人类一侧需要一双能划出「这里尚未验证」界线的眼睛。第1章的「算法理解」，我想归根结底也是这种 **无知之知** 的一种形态。

---

## 第3章【知 = RAPTOR + RAD + LLM Wiki】把「知识」灌进 harness 和 loop

第1章看了「缰绳（harness）」，第2章看了「轮子（loop）」。最后是「知（knowledge）」。harness 也好 loop 也好，**若没有好的判断材料，便只是空转**。要聪明地运转，就需要被运转的内容——知识。

我的栈，用三个层来持有知识。

1. **自有研究知识（RAD 语料库）** …… 约65领域 · 约4.7万条笔记的、置于本地的研究知识。
2. **如 Wiki 般生长的知识（LLM Wiki 模式）** …… 从原始来源编织出「概念页」、以相互链接来培养的知识缓存。
3. **安全使用它的 security agent（RAPTOR）** …… 第1章看到的、由 Python 全程控制的确定性编排。

### 3-1. RAD 语料库——自有的研究图书馆

**RAD（Research Aggregation Directory，研究聚合目录）** 是置于本地的研究知识的集合。`RAD_INDEX.md`（自动生成）在开头明确写着「**65 RAD corpora**（65个RAD语料库）」。这是名为 `rad-research` 的技能用 grep 横向检索的、内部的知识源。

我把规模 **附上准确的内部构成** 写下来。这里数法不同数字就会变，所以我不取整。

- **语料库数**：65领域（已实际计数验证）。
- **`_corpus_v2` 内的 Markdown 笔记**：约 **47,097** 个（`.md` 实数）。全部文件则约 47,130。
- 另有一个独立目录 **hacker_corpus**（安全专用：phrack / ghsa / capec / d3fend / oss_security / project_zero / payloads_all_the_things 等）约 **32,503 文件**。

#### honest disclosure（关于「约49k件」这个数字的处理）

对外公布时，我常把它取整为「自有研究知识 约4.9万件（约49k）」。这个数字的出处，是2026年5月9日大规模扩展时的统计记录（扩展中追加了 16,377 docs，total 抵达约48,800）。

不过，**这次我并未在磁盘上把全部 documents 数实际重新数一遍**（语料库数65和部分语料库的 note 数已实际计数验证）。另外 hacker_corpus 是 raw（原始）聚合文件，一个文件内含大量 docs，所以「文件数」与「内含 docs 数」并不一致。

所以若要诚实地写，就是——

> **约65领域 · 约4.7万条笔记（Markdown 实数）。另有 hacker_corpus 约3.2万文件。取整说成『约49k件规模』时，须附上『2026年5月扩展时的统计值』这个时点。**

我是在用开头说的「异常巨大的数字要怀疑其内部构成」，对自己的数字也淡淡地照样套用。

#### RAD 的运用规则——不一味地只管堆积

RAD 并非「收集完就完事」。它有三条运用纪律。

1. **K² 定容** …… 语料库的大小不是「固定100」，而是相对于话题的内部分类数 K，目标定为 **约 K² 条笔记**（K≈10 则约100）。太薄（不足约40）就向 K² 扩展。
2. **以鲜度 × 价值剪枝** …… `rad_prune.py` 给每条笔记按「**鲜度**（自收集起经过时间的指数衰减）× **价值**（正文量＋有无出处）」打分，把垫底的退避到 `.pruned/`。删除是不可逆的，所以 **默认是 dry-run（实际上不删，只是预演一遍展示会删掉什么）**，实删仅在指定 `--hard` 时。这也是 fail-closed 的思路。
3. **智能体直写** …… 收集时动员 arxiv / scholar-search / fetch / firecrawl / WebSearch，把结果 **直接写到磁盘**。这个设计反映了过去「把巨大的收集结果回送到 main 上下文，结果触及 session limit」的教训。

作为与本文三主题直接相关的语料库，`loop_engineering_corpus_v2` 确实存在。它是 a001..a048（48条笔记）＋ b001..b048（48条笔记）＝ **共96条笔记** 的 file-per-note 构成，SKILL.md 的 note_count 也是96、一致（score 0.982）。

内容是——控制反馈（PID / anti-windup〔抑制积分项失控的机制〕/ state-space〔状态空间表示〕/ Lyapunov〔稳定性分析〕/ MPC〔模型预测控制〕/ MAPE-K / OODA / cybernetics）、自主智能体循环（ReAct / Reflexion / Plan-and-Execute / Self-Refine / Tree-of-Thoughts 等）、**强化学习的各流派**（policy-value iteration / PPO / RLHF / RLAIF / Constitutional / RLVR / AlphaZero 等）、运维CI（GitOps reconciliation / watchdog / chaos engineering）——一应俱全。实笔记例：`a001_pid_control` / `a009_ooda_loop_boyd` / `a013_mape_k_autonomic_loop` / `b001_mape_k_autonomic_reference_loop`。

也就是说，第2章 `llloop` 的 MAPE-K、safety、green-keeper（GitOps reconciliation），都是 **以这个语料库为设计依据实现的**。知识（语料库）→ 循环（llloop）这条脉络，用实物连了起来。

#### honest disclosure（「50种手法」与「96条笔记」的出入）

当初备忘里写的是 `loop_engineering = 50种手法`，而实体是 **96条笔记（2分片）**。这是「**先以50种手法作为调查起点，之后以 file-per-note 扩展到96条笔记**」这一时间线的差异。所以本文写作「以约50种手法为起点扩展到96条笔记」。**不掺水写成「96种手法」。**

此外，用 corpus2skill（后述）生成的层级技能一侧（`.claude/skills/corpus/loop_engineering/INDEX.md`）显示「39 documents / 12 clusters」。这是 **从旧的源版本构建出来的层级**，因为还没有把最新的96条笔记重新 corpus2skill。我在此注明，**别把** 原始语料库（96）与层级技能（39）的数字 **混为一谈**。

### 3-2. LLM Wiki——「生长的知识」的模式

收集来的知识，放任不管就成了「一座单纯的山」。能检索，却不会 **连结起来生长**。这时 **LLM Wiki** 模式就发挥作用了。

这是 **作为 Andrej Karpathy 先生的发言而流通的模式**（备忘里源自2026-04的 Gist。但 **因本文未能确认一次 Gist 的 URL，提案者与日期都作对冲**），它用三层来持有知识。

1. **原始来源层（raw，不可变更）** …… 原始文献 · 日志。不改动。
2. **Wiki层（compiled，由LLM管理的概念页）** …… 由LLM概括 · 相互链接编织出的「概念页」。
3. **schema层（schema）** …… 「编排什么样的页、如何更新」的设计图。

#### 掰开揉碎：RAG 与 LLM Wiki 的区别

**RAG（检索增强生成）** 是「**问题一来，就每次跑去图书馆找相关的书**」的方式。是按需的。

**LLM Wiki** 是「**把常用的知识，事先整理好汇编成Wiki，反复使用**」的编译型。是预先汇编好的方式。

这两者并非对立，而是 **互补**。理想形态是「**用 RAG 检索整理好的 Wiki**」——一座整理得井井有条的图书馆（Wiki），由馆员（RAG）迅速领路，是这样的意象。

我把这个 LLM Wiki 模式，**对应** 到两个实体（**两者都处于设计阶段，实现在后续阶段**，这点要明示。以下是「我的映射（主观）」，而非已实现的同构）。

- **llive**（self-evolving modular memory LLM 框架）的 Phase 2-4 需求 LLW-01〜08。例如 LLW-01 ConceptPage、LLW-02 Wiki Compiler、LLW-04 矛盾检测、LLW-08 RAG×Wiki 双层运用。
- **RAPTOR** 的 **corpus2skill**，扩展为持续更新型 ingest 循环的 v2 构想。

llive 的四层记忆设计，**在我的对应里** 能与 Karpathy 先生的模式做结构性映射（这终归是作为设计意图的对应，实现还在后头）。semantic memory ≈ Wiki层，episodic memory ≈ 原始来源层，Hippocampal Consolidation Scheduler ≈ Wiki Compiler，Contradiction Detector ≈ 矛盾指摘，structural memory（图）≈ 页间链接，Provenance ≈ 来源追踪。

#### ★ LLM Wiki 最大的陷阱：思想的循环

这里是与 honest disclosure 表里一体的、重要的设计上的警告。LLM Wiki 最大的陷阱是 **「思想的循环（thought circulation）」**。

> **LLM 以自己写下的 Wiki 页为依据，去生成新的页。于是，最初那个微小的幻觉（看似有理的错误），便作为「共识」被固化下去。**

把自己写下的错误，自己引用，再把它当成正确的。就像一个人散布谣言，又对那条谣言深信「大家都这么说」。loop 很快（请回想第2章 Verloy 先生的警告），所以这种循环也可能 **以机器速度被固化**。

针对此，llive 设计了 **Anti-Circulation Safeguards（反循环安全装置，LLW-AC-01〜08）**（设计阶段）。

- **把 raw events 当作 authoritative（正本），把既有的概括只当作 working draft（在做的草稿）来对待。**
- **禁止在一个周期内连锁整合**（不把自己的输出立刻当作下一步的依据）。
- **周期性执行 drift detection**（定期巡检偏差）。
- **diversity preservation**（保护少数派的证据，不让多数派把它涂抹掉）。
- **外部 ground-truth anchor**（CAD / DOI / 形式验证的 hash 等，外部不会动的事实）必须化。

最后那条「外部锚必须化」，正是贯穿本文全篇的姿态——**一次信息源主义**——本身。不让AI在自己内部闭环完结，而务必把锚下在外部不会动的事实上。

另外，FullSense（后述）由 **llmesh / llive / llove 三款产品** 构成。若把 LLM Wiki 的角色映射到产品上，那么 **llive 相当于「Wiki 编辑者」，llove 相当于「Wiki 的 UI」，llmesh 相当于运送原始来源的 Bus**（RAG 不是产品，而是检索的 **手法**，所以不列入产品一列，定位为在三款产品之上使用的工具）。

### 3-3. RAPTOR 兼任「安全使用知识」的入口

知识（RAD / LLM Wiki），由谁来安全地使用？那就是第1章的 **RAPTOR**。在 RAPTOR 中，跑 `/sourcehunt`（文件粒度的漏洞猎取）时，若存在语料库，knowledge base 就会自动加载，并用 `get_hints(tags)` **附依据地注入** 到分析上下文里。

而且 RAPTOR 在知识的使用方式本身上，引入了 **证据的阶段**。`/sourcehunt` 的 **证据阶梯（evidence ladder）** 共6级。

```
suspicion（怀疑）
  → static_corroboration（静态佐证）
    → crash_reproduced（崩溃复现）
      → root_cause_explained（根因说明）
        → exploit_demonstrated（漏洞利用实证）
          → patch_validated（补丁已验证）
```

**ASan / UBSan**（在运行时检测内存异常或未定义行为的 sanitizer）复现了崩溃后，证据会从「静态佐证」升格为「**崩溃复现**」，而这成为 **PoC**（Proof of Concept ＝ 能实际踩到漏洞的实证代码）生成的闸门。也就是说，**不把「怀疑」与「实证」同等对待**。用阶段来表达证据的分量。

这一点也制度化进了输出风格。RAPTOR 的状态，在 JSON 中用 snake_case（`exploitable` / `confirmed` / `ruled_out` / `disproven`），人类可读时用 Title Case，**禁止 ALL_CAPS**。此外还 **禁止 🔴/🟢 的红绿指示器**。理由很精妙——「**对防御方坏 ≠ 对研究者坏**」，也就是说好坏取决于视角，所以不轻率地用红绿来下断语。不夸大 findings，用证据级别作阶段化表达。这是 **在设计层面强制** 推行 honest disclosure 的机制。

### 3-4. corpus-first advantage——单人开发也可能「多视角」

最后，讲讲为什么这套「知识栈」与我的独特轴（第1章）相契合。

有一个 **corpus-first（语料库先行）战略** 的领悟。先把 RAD 语料库培养起来的话，即便是单人开发，**用户没有意识到的观点**——Six Hats（六顶帽子）、TRIZ（发明原理）、KJ法、MindMap、跨领域类比——也 **有可能** 被补进AI的思考流里。

这里我加条件地写作「有可能」。语料库参照并非万能。**关联性过滤若不起作用，无关 · 陈旧的知识混进来，反而会变成噪声**。事实上，3-1写的「鲜度×价值的剪枝」，正是为抑制这种噪声混入的装置。所以准确地说，「**在关联性过滤起作用的前提下，多视角有可能被补全**」才是恰当的分寸感。

举一个具体例子。设计第2章 `llloop` 的安全层时，我把「把 fail-closed 做成三级（ALLOW/CONFIRM/FORBID）」这个想法，从 `loop_engineering_corpus_v2` 的控制理论笔记群（anti-windup 与 circuit breaker 模式）和 RAPTOR 的 governance（DENY/REVIEW/列表外DENY）两边都引了过来。即便是一个人在设计，语料库也在背后把「控制工程的视角」和「安全的视角」叠加在了一起——这就是 corpus-first 起作用的一例。

这对应于「**使用AI**（听答案）」与「**与AI一起做**（在背后参照语料库、补全多视角的同时，设计判断仍由人类握住）」的区别。第1章我写过「用户一侧需要构想力 · 经验法则 · 算法理解三种能力」。corpus-first，是一个 **有可能用AI一侧的知识基础来放大** 那三种能力的机关（前提是噪声得到管理，这一保留条件附上）。

人类握缰绳（A），循环安全地运转（B），多视角的知识流进那个循环（C）——三者在此连成一条线。

---

第3章讲的是「**做什么**（实现与知识）」。用 RAD 收集知识，用 LLM Wiki 培养（给循环的陷阱装上安全装置），由 RAPTOR 守住证据的阶段来安全使用。终于要整合了。

---

## 整合章：A（为什么）→ B（怎么做）→ C（做什么）汇成一个世界观

把至此的三章，叠进一张纸。

| | 主题 | 问题 | 实物 | 「另一条轴」 |
|---|---|---|---|---|
| **A** | harness engineering | **为什么**（哲学） | RAPTOR 的两层分离 | 人类握缰绳，把AI当部下来培养 |
| **B** | loop engineering | **怎么做**（控制） | llloop（MAPE-K＋fail-closed，alpha） | 安全层在当前路径下绕不过去 · 替换策略加以比较 |
| **C** | RAD + LLM Wiki | **做什么**（知识） | 约4.7万条笔记（※2026年5月统计时点）＋证据阶梯 | corpus-first 让单人也多视角 · 一次信息源主义 |

业界的图，往往把 A、B、C 当作各自的流行词并排摆着。我的主张是——**这三者，是同一个世界观的三张面孔**。那个世界观的核心，收敛于仅仅两条原理。

第一条是 **「把责任归属带进 architecture level」**。Approval Bus 也好、SafetyPolicy 也好、证据阶梯也好，都不是「小心点哦」这种运用层面的精神论，而是作为 **难以绕过的结构** 来实现。第1章的 `@govern`、第2章的 `SafetyPolicy`、第3章的证据阶梯，全都服务于这一点。

第二条是 **「把 honest disclosure 置于核心」**。一旦出现异常好的数字（「Bölük 10×」），在自以为赢了之前就怀疑其内部构成。本文各章里，我对自己的数字（49k件、测试90件、50种手法 vs 96条笔记）也套用了同样的做法。

而且这个世界观，在本地就能完结。RAD 也好 llloop 也好 RAPTOR 也好，全都在手边运行，不把个人信息 · 企业机密 · 传感器数据送往外部。另外，这套自有栈（llloop / RAD / RAPTOR），是与我另行称作 **FullSense** 的产品生态系统（llmesh / llive / llove **三款产品** ＋ suite installer）**有别的、本地的研究栈**。两者共享思想，但与产品线划开一条界线（唯独 llive，作为第3章提到的 LLM Wiki 的承接处，横跨两者）。

#### 为什么能说「握缰绳的是人类」——基于观察的三点

最后，把第1章预告的「优越性的论据」在这里统一收口。但首先要诚实地说，以下 **并非基于一次研究引用的 measured 结论，而是基于我经验的观察（结构性倾向）**。我不说「在认知科学上得到了证明」。在此之上，我认为人类在结构上容易比AI占优的点，至少有三个。

1. **常时并行** …… LLM 基本固定为单一会话，而人类能让多件事在后台持续运转。
2. **长射程的伏笔回收** …… LLM 能回收的，只是单一会话内（数小时）的伏笔。人类能 **用10年前的经验埋下的伏笔，在今天回收**。
3. **常时运转的危险预知（KYT）** …… LLM 的 risk_alert 不显式写代码就不会动，而人类是无意识地常时运转着的（「不知怎么地」就避开了险情的那种感觉）。

所以「握缰绳的是人类」，与其说是精神论，不如说是 **被观察到的倾向**。而我的 llive，正一点一点地试图把人类的这种倾向带进 architecture level——这就是贯穿 A、B、C 的动机。

---

## 结语：缰绳、轮子，与知

2026年，AI业界在 prompt engineering 之后，命名了 **harness engineering（缰绳）** 与 **loop engineering（轮子）**（发明它们的不是AI，而是人类工程师们）。它们的试验栈，我已在概念验证层面置于本地。

- **缰绳（A）** …… RAPTOR 以「Python 全程控制，LLM 专注判断」的两层分离来实现。在此之上，往以模型为中心的图里添了一条辅助线：「人类握缰绳，把AI当部下来培养」。这与 Karpathy 先生的 "vibe coding"（2025-02）是不同谱系，不说「是我先命名的」。
- **轮子（B）** …… 自制 `llloop`（alpha · 未公开）用 MAPE-K 运转，以 **在当前路径下绕不过去的 fail-closed 安全层** 挂上刹车。LLM 只能提议，最终闸门是 SafetyPolicy。
- **知（C）** …… 约65领域 · 约4.7万条笔记（※5月统计时点）的 RAD，用 LLM Wiki 模式培养（给思想的循环装上反循环安全装置），由 RAPTOR 守住证据的阶段来安全使用。

而贯穿本文的，只有一条做法。

> **看到异常吸睛的数字，在自以为赢了之前怀疑其内部构成。把锚下在一次信息源上。**

「Bölük 展示了 10×」这个让人忍不住想用的数字，我核对一次信息源后 **弃用了**。这不是弱点的披露，而是 **设计思想的一部分**。因为握缰绳的人类所需要的，正是看穿流畅数字的「无知之知」。

### 下回预告式的余韵

接下来想写的，是我在第3章里反复对冲为「设计阶段」的 **LLM Wiki 的实现**——llive Phase 2-4 的 LLW-01〜08，以及 RAPTOR corpus2skill 的 v2 化——在实机上的进展。我希望能在给「思想的循环」装上反循环安全装置之后，用会动的画面展示知识 **自己生长** 起来的样子。

握住缰绳，让轮子安全地转，把知培养起来。这一切，都不把数据送往外部，在本地完成。——这就是我所设想的「2026年的范式转换」，脚踏实地的样子。

---

## 参考（出处）

**harness / loop engineering（术语的一次 · 近一次）**
- Mitchell Hashimoto, *My AI Adoption Journey*（2026-02-05，提出 "harness engineering"。已一次确认 hedge 与日期）: https://mitchellh.com/writing/my-ai-adoption-journey
- Andrej Karpathy, "vibe coding" 原推文（2025-02-02，URL · 日期已确认）: https://x.com/karpathy/status/1886192184808149383
- Data Science Dojo, *Agentic Loops Explained: From ReAct to Loop Engineering (2026 Guide)*（2026-06-09）: https://datasciencedojo.com/blog/agentic-loops-explained-from-react-to-loop-engineering-2026-guide/
- Filip Verloy, *From Prompt Engineering to Loop Engineering*（2026-06，"scaling risk at machine speed"）: https://medium.com/@filipv_74515/from-prompt-engineering-to-loop-engineering-why-the-agent-era-demands-a-new-security-paradigm-816385040e3d
- Claude Code 官方 docs, `/goal`（v2.1.139 以降，Haiku 判定的自主反复。版本要求与 Haiku 已一次确认）: https://code.claude.com/docs/en/goal
- arXiv:2605.18747 *Code as Agent Harness*（Xuying Ning 等共42人，2026-05-18。撰写本文时已重新核对。※「Bölük」「10×」均 **不存在** 于本论文）: https://arxiv.org/abs/2605.18747
- arXiv:2605.26112 *From Model Scaling to System Scaling: Scaling the Harness in Agentic AI*（第一作者 Shangding Gu, 2026-05-25。所属在 abstract 页面未记载＝「UC Berkeley」为二次信息）: https://arxiv.org/abs/2605.26112
- arXiv:2605.27922 *Harness-Bench*: https://arxiv.org/abs/2605.27922

**RAPTOR（实物栈）**
- upstream 仓库（gadievron/raptor, MIT。作者 Gadi Evron 先生等5人）: https://github.com/gadievron/raptor

**相关文章（自著）**
- 从手机用SSH操作Windows PC上的Claude Code的方法: https://qiita.com/furuse-kazufumi/items/be52eeb6455732161486

**闲话休题（Snack Bus-e / Forbidden Shibukawa，Alu）**
- 「与智商有差距的人，对话总对不上」: https://alu.jp/series/スナックバス江/crop/PJm0yAGeJy9iSa487mrX
- 「多亏了那张谜之图表，悲壮感淡了些」: https://alu.jp/series/スナックバス江/crop/UfjgydbJNoh5HDTItAlf
- 「无知之知」: https://alu.jp/series/スナックバス江/crop/JRY5aSqHgjWRo1QnfR2l

> ※ 正文中作过对冲的「仅二次信息／一次未确认」的主要项目如下：OpenAI 文章的正文 · 标语 · 规模数值（一次为 HTTP 403）、LangChain 的 `Agent = Model + Harness` 公式与各 harness 基准的计测来源 · 计测条件（含被称为 GPT-5.5 的模型名）、Claude Code v2.1.139 的发布日、llloop 测试为绿的最新状态（重新跑尚未实施）、RAD 总 documents 数（「约49k」为2026年5月统计值）、Karpathy 先生 LLM Wiki Gist 的提案者 · 日期、佳能「三自精神」与 *First, Break All the Rules* 四原则的出处页码、第3章的「人类优越三点」（并非 measured 而是基于观察）。一旦能以一次信息源确定，便即更新。
