---
title: llcore 验证 arc 合集(#38–#42):防御性公开 × 2ⁿ 壁垒 × 强梯度胜过进化 × 兰顿蚂蚁的幻象
tags: FullSense, llcore, Singularity, AI, 解説
private: false
public_id: 29b100b00f0d58306886
---

# llcore 验证 arc 合集(#38–#42):防御性公开 × 2ⁿ 壁垒 × 强梯度胜过进化 × 兰顿蚂蚁的幻象

<!-- TOPICNAV -->
> **🌐 语言**: [日本語](https://qiita.com/furuse-kazufumi/items/cc0713ab78a5b390df76) | [English](https://qiita.com/furuse-kazufumi/items/525cd01eda5c1ad707ef) | **中文** | [한국어](https://qiita.com/furuse-kazufumi/items/a5ebb3992e4c28862f47)
>
> **📚 FullSense 合集系列**
> - **llcore 验证 arc 合集（this）**
> - [lldarwin / 进化 arc 合集](https://qiita.com/furuse-kazufumi/items/93f3cf1bb7b14650bbca)
> - [llive 完全解说合集](https://qiita.com/furuse-kazufumi/items/6da5a883fb2ed651edd8)
> - [llmesh 合集](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762)
> - [通俗版合集](https://qiita.com/furuse-kazufumi/items/fa0890f136636d495ea6)
<!-- /TOPICNAV -->

## 目录

1. [— 一天之内跑完「反证检验 → 专利清查 → 放弃申请 → 防御性公开」](#第1章--一天之内跑完反证检验--专利清查--放弃申请--防御性公开)
2. [— 「窗在实现里关上了，但墙纹丝不动」的报告](#第2章--窗在实现里关上了但墙纹丝不动的报告)
3. [这是什么 — "我以为赢了的那一刻，自己的框架把自己拦住了"](#第3章-这是什么--我以为赢了的那一刻自己的框架把自己拦住了)
4. [这是什么 —— 把三篇束于一点：「简单的确定性规则制造出表面的秩序」](#第4章-这是什么--把三篇束于一点简单的确定性规则制造出表面的秩序)
5. [第5章](#第5章-第5章)


---

## 第1章 — 一天之内跑完「反证检验 → 专利清查 → 放弃申请 → 防御性公开」

2026 年 6 月 6 日，我（笔者）向 AI（Claude Code）提出 **「请检验我们所做的事情是否真的具有差异化」**。AI 以 **反证检验（adversarial verification）** —— 让大量验证角色的 AI 故意去反证、否定我们自己的主张，看它是否仍能存活的方法 —— 来回应。56 个验证代理从 7 + 3 个角度去搜寻「这个主张应该能用先行研究反证」的反例，另一支别动队甚至查询了专利数据库。

结果如下。

- **学术文献中的反证（breaks）：0 件**（对 44 个候选逐个判定，没有任何人填满了「四隅同时」）。
- **专利中的反证：0 件**（在英文 14 + 日文 3 个查询里，没有专利占据这个交叉点）。
- 于是我决定**不申请专利**（成本判断），转而立起一面叫**防御性公开（defensive publication）**的旗。

这篇文章，是那一天的故事（反证检验的设计与结果、以及决策）加上**我们所公开的内容（= 四点交叉点的技术）**的拆解版。文章的顺序一如既往：①术语说明 → ②拆解（平易） → ③详细。

---

### ① 术语小辞典（免得在正文里卡住）

| 术语 | 一句话 |
|---|---|
| **反证检验 (adversarial verification)** | 不是去肯定自己的主张，而是让大量验证角色（AI）故意去反证、否定它，再以它是否仍能存活来衡量主张的强度。可以想象成雇批评者而非捧场者。 |
| **防御性公开 (defensive publication)** | 不是去「取得」专利，而是**把技术公开、使其成为先行技术**。这是一种「先立旗」的防御，让某人（包括大厂）日后无法用同一发明申请专利来束缚我方或公众。 |
| **先行技术 (prior art)** | 能让你说出「那个发明已经是公知了」的既有公开物。否定新颖性的材料。日期是命门。 |
| **收缩性 (contraction, ρ<1)** | 回声（过去的扰动）随时间**衰减**的性质。谱半径 ρ 小于 1。可以想象成一根弹簧总会回到静止位置。记忆核不暴走、会「遗忘」的性质。 |
| **健全的证明 (sound proof)** | 一旦说「证明出来了」就**真的正确**（绝不发出假合格）的证明。与统计上「大概安全」是两回事。 |
| **prove-then-reject 门** | 一道关卡，**证明之后才采用**变异（更新），不行就**棄却**。fail-closed（无法证明就不放行）。 |
| **记忆核 (memory core)** | 罩在 LLM 周围的「记忆部件」。本研究中是带漏与饱和的递归（RWKV 系）`s_{t+1} = decay⊙s + (1−decay)⊙tanh(W s + V x)`。 |
| **进化循环 (evolution loop)** | 转动变异 → 选择 → 下一代来搜寻优秀个体的最优化。这里把证明门放在那个选择的关卡上。 |
| **SMT 求解器 (Z3 等)** | 解判逻辑式是否可满足的万能求解器。很重。本研究的结论是它「其实并不需要（只是装饰）」。 |
| **tracking tube（追踪管）** | 保证实际与「理想轨道」的偏差收在一个**管（半径 r）**之内。`r = G·w̄/(1−L)`。 |
| **SSGM** | **仅以理论**提出「统御进化记忆」write 门的先行研究（[arXiv:2603.11768](https://arxiv.org/abs/2603.11768), 2026）。在招牌上最接近的对手。 |
| **navigability（可探索性）** | 进化是否「易于移动的地形」。与学习变聪明是两回事。验证器的功效在这一侧。 |

![四点交叉点 —— 只有 4 个条件同时重叠的中心才是差异化核心](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_intersection.svg)

---

### ② 拆解 —— 3 分钟看懂全貌

先从生物学的生态位（niche）讲起。在进化里，「钻进了一个生态位 —— 一个还没有其他物种占据的缝隙 —— 的物种」会存活下来。AI 的世界也类似。大厂（OpenAI/Google 等）是「平均上聪明的大型物种」，占据着广阔的平原。我们在那片平原上赢不了。所以我们去找**谁都没填的缝隙**，再造一个正好嵌进去的部件。这一次，恰好嵌进那个缝隙的，是一个叫 `llcore` 的具体系统。

`llcore` 用一句话说，就是 **「一个拥有记忆的 AI 部件，为了不让自己暴走，给自己加上了一道『证明的关卡』的系统」**。记忆核每更新一次就会变异（进化），但在采用任何变异之前，都必须先通过这道关卡（门）。关卡只放行**能在数学上证明「即便加入这次更新、记忆也不会暴走」**的那些变异，证明不出来就一律拒之门外（fail-closed）。

这个系统之所以能恰好嵌进那个「缝隙」，是因为下面 4 个条件在**同一个点上重叠**。

1. **健全的收缩性证明**（在数学上保证回声必定衰减，而且绝不发出假合格）。
2. 把它打在**LLM 记忆核的内部**（不是控制机器人也不是分类器，而是「记忆部件」本身）。
3. **在进化循环之中**，把不行的变异**棄却**（丢掉 = 不是把它推回去 = 不是射影）。
4. 而且**有能跑的实现与实验**（不止步于纸上谈兵）。

把这 4 件**同时**满足的先行研究，即便让 56 个验证角色 AI 来批判性地检验、查询专利 DB，也没找到。每一个条件都有先行（我们诚实地把名字全部列出）。但没有人「同时占据四隅」。这就是**四点交叉点（four-point intersection）**。用生物学的生态位来说，`llcore` 正好坐落在那四条边界线交汇的**那一个点的缝隙**里（用孙子的话说，「避实击虚」）。

还有一个重要决策。这个缝隙在**专利里也是空白**。一般来说接下来就会是「那就去申请专利吧」。但专利又花钱又花时间。我**放过了那里**，转而选择了**「公开、先立旗」的防御性公开**。目的不是进取而是**防御** —— **未雨绸缪地使其失效**：日后有人（大厂，或 SSGM 的后续实现）用同一概念申请专利来束缚我方或公众。只要带着日期公开了，它就成了公知的先行技术，后出的专利会因新颖性而被否定。

不过 —— 这是我们一以贯之的纪律 —— **我们不注水**。我们不说「世界首创」。正确的说法是**「在我们反证检验的范围内，同时占据四隅的先行为零」**。我们一定保留「探索范围之外不得而知」的留白。

---

### ③ 详细 —— 一天的会话，以及所公开技术的内容

#### 3.1 反证检验的设计（为了可复现）

自己说「我的研究很强」没有意义。所以 AI 搭了一套**反证主导的工作流**。

- **从 7 个角度搜寻反证**：证明门的谱系 / certified training / Transformer 稳定性 / 进化 × 验证 / verified memory / runtime assurance / 产业·专利。
- **追加 critic 指出的 3 个盲点角度**：从形式方法会议一侧的反查 / certified continual learning 的词汇系 / 内部状态·SSM 的解释。
- **用 5 轴评分表对 44 个候选逐个判定**（是否对更新设门 / 是否健全证明 / 是否 LLM 记忆核 / 是否在进化循环内 / 是否有实现）。判定方的 AI **必定用 WebFetch 确认一手信息（arXiv 的 abstract/HTML）**（禁止道听途说）。
- 并行地，**内部的 AI 抽取我们自己论文草稿的弱点**（honest disclosure：自家人挑刺）。

确定结论是 **breaks 0 / narrows 36 / background 8（44 件）**。存活下来的差异化核心，就是上面的四点交叉点。

#### 3.2 「四隅」各自最接近的对手（全部列名）

新颖性的诚实，取决于「能否用一句话点名全部」。逐隅，用一句话点出最接近的先行：

- **SSGM（[arXiv:2603.11768](https://arxiv.org/abs/2603.11768)）** —— **仅以理论**抢先拿下「统御进化记忆」的招牌。门是 NLI（矛盾检测），**并非健全的形式证明**，也没有实现。→ 作为扛招牌的对手**必须引用**。实现 + 证明的窗口是空着的。
- **SEVerA（[arXiv:2603.25111](https://arxiv.org/abs/2603.25111)）** —— 对自进化代理施以 Dafny/SMT 验证。但对象是**输出契约**，不是对记忆核收缩性的每次更新设门。
- **PSV-Verus（[arXiv:2512.18160](https://arxiv.org/abs/2512.18160)）** —— self-play 循环内的健全 SMT 门。但验证对象是**生成代码的正确性**。
- **Provably Safe Model Updates / LID（[arXiv:2512.01899](https://arxiv.org/abs/2512.01899)）** —— 用抽象解释把更新认证为 δ-safe。但它是**射影（推回去）**而非 prove-then-reject，对象是 frozen-embedding 的分类 head。
- **GP × 模型检查（Katz & Peled, [arXiv:1402.6785](https://arxiv.org/abs/1402.6785), 2014）** —— 在进化循环里放一道健全检查门的**模式先例**。所以我们**不主张门这个模式本身是新颖的**。只有把它应用到记忆核的收缩性上，才是未踏之地。
- **Enforced-Lipschitz Transformers（[arXiv:2507.13338](https://arxiv.org/abs/2507.13338)）/ R2DN（[arXiv:2504.01250](https://arxiv.org/abs/2504.01250)）** —— 用**结构来强制（by-construction）**收缩性。这是最强的对抗设计：「根本不需要门，一开始就内嵌进去」。我们把**by-construction 对 prove-then-reject**作为设计轴来对比（结构强制牺牲表现力，棄却门则在无结构约束下检查任意更新）。
- **Safeguarded AI（ARIA programme）** —— 最具权威的 proof-gated-gatekeeper 概念。但门的对象是**行为/计划**（输出门），不是对权重/记忆更新设门，而且还停留在 programme 阶段。
- **Emergent FV / substrate-guard（[arXiv:2603.21149](https://arxiv.org/abs/2603.21149)）** —— 用 Z3 验证 AI 的**输出**的、能跑的系统。但它是事后监视，不是每次更新设门。

（以上 arXiv ID 只使用在论文草稿中已与 abstract 核对过的那些。）

#### 3.3 专利面的查询（补学术审计留下的窟窿）

学术审计**只看了文献**，没看专利 DB（作为不在证据偏弱）。于是一支别动队用**英文 14 + 日文 3** 个查询，查询了 Google Patents / USPTO。

- **占据交叉点的专利：零件。**
- 最接近的专利只有 3 个谱系，且都在交叉点之外：
  - **[US11715005B2](https://patents.google.com/patent/US11715005B2)** —— 用哈希匹配来验证 NN 的真正性（是密码哈希，不是健全证明）。
  - **[US10896032](https://patents.google.com/patent/US10896032)** —— certify-then-deploy 的治理门（根据是程序性 attestation）。
  - **[US11868855](https://patents.google.com/patent/US11868855)** —— 模型/权重的「stability」验证（但大概率是可用性·耐故障意义上的蓋然性）。
- 一个有趣的结构性证据：当你查询「**用健全证明对更新/记忆/进化设门**」时，即便对专利 DB 指定了 site，结果也几乎全部**偏到了 arXiv**。这是「这个概念还停留在学术阶段、尚未被专利化」的间接证据。

→ 结论：**专利面也 clear**。不过由于 US10896032 / US11868855 在词汇上部分重叠，我们在论文的 related work 里先发地放了 1～2 句对比：「与展开治理型门 / 运营稳定性验证不同，本研究是用健全证明对权重更新的解析性 contraction 性质设门」。

#### 3.4 所公开技术的内容（防御性披露的本体）

防御性公开如果不写到「当业者可实施的详细度」，作为先行技术就会偏弱。所以披露文件里，把以下内容写到了**可实现的层级**。

![记忆核公式 —— 带漏与饱和的递归 s(t+1) = decay⊙s + (1−decay)⊙tanh(W s + V x) 的图解](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_core.svg?v=2)

**(a) 健全收缩性证明器的梯子（ladder）。** 从便宜的开始，共 3 级：
- `cert_inf` —— 闭式 ∞-范数上界（`O(n²)`）。利用各行绝对值之和在端点处取最大的性质，**无需求解器**。
- `cert_two` —— 在全部 `2^n` 个顶点上做 SVD。
- `cert_sdp` —— 用凸 LMI（内点 SDP, CLARABEL）求共同 Lyapunov 矩阵。

![证明器梯子 —— cert_inf → cert_two → cert_sdp 三级，按便宜优先逐级尝试的证明强度阶梯](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_ladder.svg)

**这里是诚实点**：项目的旧俗称是「Z3-gated」，但**实际的门并没有用 SMT(Z3)**。专门跑了一条 Z3 收缩性轨道来确认后，它与闭式 ∞-范数证明器**逐字节一致（3270 件中 0 件不一致，连边界附近也是 8000 件中 0 件）**。也就是说，在这个不变量类里，**Z3 是装饰**。所以我们把招牌改正为「健全收缩性证明器的梯子」（这不是撤退而是强项 —— 可以规避求解器依赖与不完全性）。

**(b) prove-then-reject 门（fail-closed）。** 提出一个子个体 → 证明通过则采用，不行则 resample 直到上限，再不行就采用一个**已知安全的 fallback**。**未证明的子绝不采用**。我们把 `gate_mode="contraction"` / `"state_norm"` additive 地加入，而默认的 `"none"` 与既往行为逐字节一致（= 对既有进化基盘的纯粹罩层）。

![prove-then-reject 门 —— 一道 fail-closed 关卡：提出子个体，证明通过则采用，不行则棄却并重新采样](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_gate.svg)

**(c) tracking tube 检查指标。** 这是对用户要求「不只要『收缩到某处』，还要看『追踪理想轨道』」的回答。复用门已经在算的量（状态 Lipschitz `L`、输入增益 `G`）与外扰上界 `w̄`，以**零额外证明成本**报告追踪误差收住的管 `r = G·w̄/(1−L)`。即便在小规模实测里，收缩性 PASS 的 3 gene 误差/外扰比为 0.50/0.78/1.04，处于理论管之内；而非收缩性的对照则**放大 9.3 倍**（= 门是 load-bearing，不是装饰）。

![tracking tube —— 在理想轨道周围张起半径 r = G·w̄/(1−L) 的管，实际轨道收在其内部的图](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_tube.svg)

**(d) verified memory evolution 的 2 条路线。**
- 路线 (a)：用健全证明对代理**记忆库**的更新设门（与 SSGM 的 NLI 理论之差 = 健全证明 + 能跑的门）。
- 路线 (b)：对记忆核的**内部状态 dynamics**设门（本书已实施）。

**(e) 合成：SPC 管制图 runtime 门 + 双层伦理门。** 把进化指标通过管制图（X̄–R / CUSUM），在线对时间方向的异常设门。再加上**探索自由·采用验证**的双层伦理（探索层遵循孙子的「诡道」= 奇手 OK，采用层遵循论语的「仁」= 诚实、门不可避）。

#### 3.5 本日的实现事实（reduced to practice）

它不是纸上谈兵的证据：

- 证明门已**正式配线进出货侧的 `evolve()`**（additive 地追加 `gate_mode` / `resample_cap`，默认 `"none"` 逐字节一致，并以测试实证与 research 侧的参考实现全模式一致）。
- tracking tube 报告器也落地了（`r = G·w̄/(1−L)`，限定 `cert_inf`，read-only，golden 值一致）。
- 覆盖门 + 报告器的测试 **294 件**。
- **观测到的门的成本约为 20～60 倍**（不隐瞒地披露：证明不是免费的）。

#### 3.6 honest 局限（不弱化）

即便是防御性披露，我们也不弯折 honest disclosure。

- **规模小**：核是 `n=8`（72 个实数 gene）、16 KB 语料、byte vocab。「LLM 记忆核」是**机构实证**的意思。
- **验证器的 payoff 是 navigability 而非学习（L3）**：效果是 EA 固有的，在梯度法里会消失。
- **门是 ~20～60 倍的成本**：只在短训练里看着像免费。
- **「false admit 为零」是经验观测，而非机器检查**：证明器的*条件*是健全的，但承载它的*实现*并未做端到端的形式验证。
- **「未发现」的范围**：仅限于反证检验 + 表层专利检索的范围。CNIPA（中文）未查询，专利最长有 18 个月的公开滞后。「在探索范围内」的留白始终保留。

---

### 总结 —— 旗是为了「守」而非「攻」才立起来的

今天一天，我们让 56 个验证角色 AI 批判性地检验自己的研究，连专利 DB 都查询了，还是确认到了残留的「四隅空白」。一般来说这时就会去谋求专利，但权衡成本之后，我们**放过了申请**，转而用**带日期的防御性公开**立起一面旗。

目的很简单 —— **未雨绸缪地使日后有人用专利把这个空白圈起来、束缚我方或公众的企图失效**。为此，我们以当业者可实现的详细度把一切都公开了。并且自始至终，守住不注水的说法：**不说「世界首创」，而说「在我们检验的范围内，同时占据四隅的先行为零」**。

防御性公开的本体（带日期的开示），如下方追记所述，已升格为**包含实现与全部数据的 public 仓库**：[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)。

下一回（#39 以后），打算 report 这个四点交叉点的本丸 —— verified memory evolution 的小 PoC（记忆库更新路线）的落地。趁 SSGM 以理论拿下招牌的那扇窗，还没被实现合上之前。

### 追记（2026-06-07）—— 旗变成了实现

本文的次日，预告过的 verified memory evolution PoC **完成了，防御性公开也从「文件」升格为「实物」**。

- **public 仓库**: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) —— 论文草稿（[PAPER_DRAFT.md](https://github.com/furuse-kazufumi/llcore/blob/main/research/paper/PAPER_DRAFT.md)）+ 全部实验代码/数据（570 个文件、318 个测试 green），以带日期的单一提交公开
- **trajectory-tube gate**（预告过的本丸）: 以预注册 n=40 的决着确认了对记忆 horizon 的效果（论文 §9）
- **更进一步**: 「让 AI 自己持有验证器会怎样」—— 在可致死环境中对记忆形成 3 机构（自我预见/复活修复/社会观察）的测量也包含在公开内容里（论文 §9.6）
- **知见幻灯片（CC BY 4.0）**: [slides/](https://github.com/furuse-kazufumi/llcore/tree/main/slides) —— 注明出处即可商用的 10 页摘要（日英）。**当前版本是信息密度有限的摘要版 —— 随着研究推进，今后一年将持续扩充（实验设计细节、完整图表、复现步骤、采用决策材料）**

「趁 SSGM 的窗被实现合上之前」的预告，就这样兑现了。

---

---

## 第2章 — 「窗在实现里关上了，但墙纹丝不动」的报告

上一回（#38）结尾，我们这样预告：「下一回将 report 四点交叉点的本丸 —— verified memory evolution 的小 PoC。趁 SSGM 以理论拿下招牌的那扇窗，还没被实现合上之前。」

2026 年 6 月 9 日，那个 PoC 跑完了。用一句话说结论：**「窗在实现里关上了。但墙（可扩展性的墙）纹丝不动。」**

具体来说：

- 我们让**带证明地进化的记忆核**（包含真正把结构变大的手术 `width_grow`）在 **零观测 false-admit** 下跑了起来（= 一件假合格都没发，就完成了进化）。
- 同时，把此前一直诚实地留作「未测定」的 **cert_sdp（SDP 证明器）首次测量**，发现它是**最「易通过」（navigable）的健全证明器**（把真正收缩的个体的 90～99% 判为合格）。
- **尽管如此，包括 cert_sdp 在内，计算成本仍是 `2^n`（维度 n 的指数）。** 也就是说，**「既易通过、在大规模下又便宜」的证明器，这次也没找到。** 目前能 verified 地做结构进化的，仅限于**小部件（n≤6）。**

这篇文章，按惯例的顺序 ①术语 → ②拆解 → ③详细，不注水地写下那一天「能做到的」与「做不到的」。最后还公开把自己的数值主张**让 6 个验证 AI 并行反证**的结果（零 MAJOR 不一致）。

正本数据：[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)（论文草稿 + 全部实验代码/数据）。

---

### ① 术语小辞典（免得在正文里卡住）

| 术语 | 一句话 |
|---|---|
| **可塑性 (plasticity)** | 通过学习/进化能「改变形状」的性质。这里指事后把记忆核自身的结构（矩阵大小=维度）变大。 |
| **verified-plasticity（带验证的可塑性）** | 每次「改变形状」时，都**先证明该变更安全（不暴走）再采用**。本研究的主轴。 |
| **width_grow（宽度成长）** | 把网络层从 `n → n+1` 变大的**结构手术**（Net2Net 系）。是实际执行的，不是纸上。 |
| **收缩性 (contraction, ρ<1)** | 过去的扰动随时间**衰减**的性质。谱半径 ρ 小于 1。记忆不暴走、会「遗忘」的性质。 |
| **false-admit（假合格）** | 明明危险（ρ≥1=可能暴走），证明器却放行为「安全」的漏检。这一项为零是健全性的命门。 |
| **健全 (sound)** | 一旦说「合格」就**真的安全**（绝不发假合格）的性质。与统计上「大概安全」是两回事。 |
| **navigability（易通过/可探索性）** | 「能把多少真正安全的个体判为合格」。过严的证明器连安全个体也弹掉=进化动不了。越高，进化越能在地形上自由移动。 |
| **证明器格子 (cert ladder)** | 按便宜优先三级：`cert_inf`（∞-范数上界、无需求解器）→ `cert_two`（全 `2^n` 顶点 SVD）→ `cert_sdp`（凸 LMI/SDP）。 |
| **prove-then-reject 门** | **证明之后才采用**变异，不行则**棄却**的关卡。fail-closed（无法证明就不放行）。 |
| **SSGM** | **仅以理论**提出「统御进化记忆」write 门的先行研究（[arXiv:2603.11768](https://arxiv.org/abs/2603.11768)）。实现 + 健全证明的窗口对它而言是空着的。 |
| **empirical_rho（经验 ρ）** | 用大量采样**从下方**逼近真谱半径的预言机。「零观测 false-admit」是这种从下方审计的结果（=强一致性证据，但非绝对证明）。 |
| **2^n 墙** | 证明成本对维度 n 呈指数 `2^n` 增长的极限。`cert_two`/`cert_sdp` 要看全部顶点，所以撞上这堵墙。 |

![四点交叉点与 2^n 墙 —— 纵轴取易通过性(navigability)、横轴取维度 n，cert_sdp 抬高了天花板，但没破墙(2^n)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_39/qiita_39_fig_wall.svg)
> 🗒️ *注：此图标签为日语。（2ⁿ 壁垒＝随着块尺寸增大，证明成本呈指数级膨胀。）*

---

### ② 拆解 —— 3 分钟看懂全貌

#38 立的旗是**「带证明地进化的记忆核」**。记忆核每次更新都会变异（进化），但在采用任何变异前，都必须先过关卡（门），只放行**能在数学上证明不暴走**的变异，证明不出来就拒之门外（fail-closed）。这就是 prove-then-reject 门。

这次做的，是把那面旗**从「文件」推进到「能跑的实物」**。有三件「能做到」。

**能做到①：一边把形状变大，一边零假合格。** 此前只试到「证明变异（内部微调）」。这次实际跑了**把结构本身变大的手术（`width_grow`，n→n+1）**，确认变大之后证明器仍以**零观测 false-admit**保持「安全（ρ<1）」。发散域（ρ 达 1.85～2.21 的危险个体）全部被正确棄却。

**能做到②：第一次测到了最「易通过」的证明器。** 把此前诚实留下的「cert_sdp 未测定」这个洞补上了。在能用 SDP 求解器（CLARABEL）的环境里首次测量，发现 **cert_sdp 是三级证明器中最「易通过」的** —— 把真正收缩的个体的 90～99% 判合格（便宜的 `cert_inf` 只通 20～40%，中位的 `cert_two` 40～50%）。「太严、进化动不了」的问题，被 SDP 大幅缓解。

**能做到③：小部件的话，计算轻松够用。** n≤6 的小核，verified 进化的整个循环只吃 **30 小时预算的 0.04%（0.013 小时）**。「带证明的进化是不是太重跑不动？」的担心，在小规模下是杞人忧天。

…听到这里像是「全赢了」。但 honest disclosure（诚实开示）是我们的纪律。把**没赢的三件事**明明白白写下来。

**没做到①：2^n 墙没破。** cert_sdp 确实抬高了「易通过性的天花板」。但代价是成本仍为 `2^n`（看全部顶点）。`cert_two` 在 n=12 是 1 次证明 1.3 秒，n=14 超预算。**「既易通过、大规模下又便宜」的证明器，这次也不存在。** 所以目前能 verified 地做结构进化的仅限**小部件（n≤6）** —— 这个结论与上一回（Phase −1）**没有变**。SDP 不是**翻过**了墙，而只是在墙前**抬高**了天花板。

**没做到②：「零假合格」是经验观测，并非机器证明出来的。** 零观测 false-admit，是用**从下方**逼近真 ρ 的预言机（大量采样）去找反证的结果。证明器的*条件*在数学上健全，但承载它的*实现*并未做端到端的形式验证。「零观测」是强一致性证据，不是「对所有输入都安全」的绝对证明 —— 这里不夸张。

**没做到③：模型并没变聪明。** 证明器的功效是 **navigability（进化的可移动性）**，不是模型变聪明（学习性能提升）。而且效果是进化算法（EA）固有的，在梯度法里会消失。再者这次的适应度（fitness）是**合成 proxy**，实 GPU 训练下的确认留到下一阶段（Phase 2）。

总之这一天是「机构在实现里证明了，规模的墙诚实地留着」—— 赢一半、作业留一半的一天。

---

### ③ 详细 —— 五个实验，以及没能潰掉的留白

主轴是 **Verified-Plasticity Evaluation Framework**（带验证的可塑性测量框架）。在主张「我们的方法强」之前，先造**度量的尺子**。用那把尺子跑了五个实验（全部 `$0` / CPU、torch 2.12+cpu、固定 seed、可复现）。

#### 3.1 固定结构下证明器的健全性与格子

在 n={4,6,8} 各采样数百个跨越收缩～发散的个体，把 3 证明器的合格与真 ρ（empirical_rho 6000 采样）做突合。

| n | 收缩(ρ<1) | false-admit (inf/two/sdp) | 真正收缩个体的合格率 (inf/two/**sdp**) |
|---|---|---|---|
| 4 | 453/600 | **0 / 0 / 0** | 0.41 / 0.51 / **0.95** |
| 6 | 426/600 | **0 / 0 / 0** | 0.29 / 0.43 / **0.94** |
| 8 | 280/400 | **0 / 0 / 0** | 0.23 / 0.40 / **0.91** |

确定知见：
1. **三个证明器全部零观测 false-admit**（首次确认 cert_sdp 的健全性）。与证明器的数学健全性一致。
2. **cert_sdp 压倒性 navigable** —— 真正收缩的个体中，便宜的 cert_inf 只通 23～41%、cert_two 40～51%，而 **cert_sdp 通 91～95%**。注：`two⊆sdp`（cert_two 通则 cert_sdp 通）是实现 fast-path 带来的**结构性保证（同义反复）**，不是经验发现 —— 为不注水而写明。

#### 3.2 实结构手术（width_grow）下的健全性 × 非平凡性

实际用 `width_grow`（Net2Net/fresh）把 base 从 n→n+1 变大，判定各门是否**在成长下仍保持零 false-admit ∧ 开出≥1 个非平凡合格**（1 格 = 1536 个成长后个体）。

- **成长下健全性：全 16（格×门）零观测 false-admit。** 成长 ρ 最大 1.85～2.21（发散域）全部正确棄却。这是 **North Star #1（成长操作下零假合格）** 在实结构手术下的确认。
- **便宜门（cert_inf）健全但在小 n 脆弱** —— n=6 最保守边缘（headroom 0）非平凡合格 **0 个** → 门 FAIL。即便有 headroom，非平凡合格也仅 3 个，卡在 τ 边缘。= 「便宜门的 navigability 脆弱」。
- **navigable 门（cert_two/cert_sdp）全格 PASS** —— cert_two 开 114～168、cert_sdp 开 673～733 个非平凡健全合格。→ **「把 per-component 门升级到 cert_two/sdp、限定 small-n」由数据正当化。**

#### 3.3 块间结合（coupling）的盲点

把 2 个块残差结合，用真 ρ 测**「各块单独合格、合成却暴走」的盲点**。

- **per-block AND（把各块单独合格做 AND）在结合下确实不健全** —— 结合强度 γ≥1.0 时，单独合格里的 **24～34%（γ=1.0）～ 80～96%（γ=2.0）合成真 ρ≥1**（暴走）。→ **per-block AND 禁止确定。**
- **full-system cert（把整个系统一次性证明）全 γ 零 false-admit = 健全。**
- 这里同样 **cert_sdp 最 navigable**，但抬高维度（块数 2→3）与结合强度，coverage 会下降（full=6、γ=1.0 时 cert_inf/cert_two 为 0%，仅 cert_sdp 75.8%）。= SDP 解决过保守，但**维度墙对 SDP 也起作用。**
- ⚠ 诚实留白：块数 3 时 SDP 求解器发了几条「解可能不准确」警告。**用独立特征值复检保证健全性（false-admit=0）**，但 coverage 数值可能含近似解带来的微小抖动。

#### 3.4 feasibility（是否真能在预算内跑）

由实测 per-op wall-time 外推到 30 小时预算。

| n | 每次 eval | 总时间 | 30h 内 |
|---|---|---|---|
| 4 | 769μs | **0.011h** | 是 |
| 6 | 912μs | **0.013h** | 是 |
| 8 | 9.2ms | 0.131h | 是 |
| 10 | 38.6ms | 0.550h | 是 |
| 12 | 1.31s | **18.6h** | 勉强 |
| 14 | — | (cert_two 2^14 外推 = 不能) | 否 |

确定知见：
1. **small-n（n≤6）计算上自明 feasible** —— 预算的 0.04%。
2. **2^n 墙在 n≥10～12 binding** —— cert_two 在 n=12 是 1.3 秒/证明（=18.6h，余量薄），n=14 超预算。
3. ⚠ 留白：此处 fitness 是 `RotationNDObjective` 的**合成 adapter proxy**，实 GPU 训练里 base forward（CE）会成为 dominant。该外推是「每次 eval 课金一次证明的保守上限」，实 GPU 实测留待 Phase 2 确认。

#### 3.5 向第 2 个 base（Mamba）的可移植性

确认框架是否能载到 SmolLM2 以外的 base。**Mamba-130M 在 CPU 上 load 成功**（确认了 coherent 生成），在其 hidden 上 cert_two 门 load-bearing（有/无门合格率移动 +0.287，与 SmolLM2 的 +0.320 相洽）。= 「换上新 base」plug-point 的实证。
- ⚠ 留白：此处健全性预言机不是 §3.1-3.4 的 empirical_rho，而是**弱预言机（单一摄动）**，合格 n=7 的小集团。Mamba 自身的固有稳定性（base-level Lyapunov）未测定，留待 Phase 2。本阶段 deliverable 仅限「框架可移植性 + Mamba CPU 动作确认」（不是固有稳定性的正对照）。

#### 3.6 综合判定 —— Decision gate 1 = PASS（small-n）

| gate | 条件 | 判定 |
|---|---|---|
| 成长下 soundness ∧ 非平凡 admit≥1 | width_grow N 次 false-admit=0 ∧ 非平凡合格≥1 | **PASS**（便宜门在 n=6 trivial → 必须 cert_two/sdp） |
| coupling-aware 合成 soundness | per-block AND 禁止 + full cert 健全 | **PASS** |
| feasibility | small-n 循环在 30h 预算内 | **PASS**（small-n） |

→ **Decision gate 1 = PASS → 进入 Phase 2（small-n per-component 域，在 Phase −1 确定的约束内）。** Phase 1 的 deliverable 是**「健全·feasible 的 small-n verified 结构适应测量框架 + 证明器格子（inf/two/sdp）的完整特性评价」**。

#### 3.7 honest 局限（没能潰掉的）

即便是防御性开示，honest disclosure 也不弯折。把这次测量潰掉/留下的，叠在 #38 的留白之上。

- **2^n scalability 墙不变（最大作业）**：cert_sdp 把 navigability 天花板抬到 ~0.9（从 Phase −1 的 cert_two ~0.45 大幅改善），但 **2^n 顶点成本不变**。「navigable 且 scalable 的健全证明器依然不在」= 高维 verified 结构进化不成立 **堅持**。SDP 只抬了天花板，没破墙。
- **empirical_rho 是从下方估计**：零观测 false-admit 是强一致性，不是「对全部 (s,x) ρ<1」的绝对证明。可能漏掉 near-boundary。
- **net2net 是 incoming-copy 近似**（非 exact function-preserving）→ 函数变化 Δfunc 是近似评估。
- **fitness 是合成 proxy**：实 SmolLM2 CE 上的 capability 副线（EXISTS/NULL/ARTIFACT）是 Phase 2 必须。
- **Mamba 固有稳定性未测定**：门挂在 adapter 上，Mamba base 自身的 Lyapunov 未验证 → 留待 Phase 2。

---

### 敌对验证 —— 让 6 个 AI 并行反证自己的数值

honest disclosure 的核心是「出现异常好的结果时，在自觉赢之前先怀疑内訳」（[feedback_benchmark_honest_disclosure]）。于是把本 verdict 的数值主张，对各实验的 `results.json` + 实现 `.py`，让**6 个独立验证 AI 并行**突合。

**结果 = 零 MAJOR issue（无能覆盖结论的不一致），全是 MINOR。** 检出的指摘已反映进正文：
- 修正 4 件转记舍入误差（maxΔfunc 0.108→0.107 等）。
- §3.1 的 `two⊆sdp` 写明是实现上的同义反复，而非经验发现。
- 把「便宜门在 n=6 trivial」精炼为「仅 n=6 最保守边缘 trivial、有 headroom 也脆弱」。
- 「cert_sdp 98% 救济」写明限块数 2，块数 3 是 75.8% / inf·two 0%。
- 透明化 fitness 是合成 proxy、外推的保守性、CPU→GPU 外推前提。

→ **验证后 Decision gate 1 = PASS、SDP navigability 知见、small-n 限定结论不变。** 指摘全是 honest-disclosure 的精度提升，无一动摇机构性结论。

---

### 总结 —— 「窗关上了，墙留下了」

#38 立的旗，这次**从文件推进到了能跑的实物**。我们让带证明地进化的记忆核，一边真把结构变大，一边以**零观测 false-admit**跑起来，补上了此前未测定的 SDP 证明器，确认了 small-n 的 feasibility。SSGM 以理论拿下招牌的「实现 + 健全证明」的窗，就这样在实现侧关上了。

另一方面，最大作业 **2^n 墙** 这次也纹丝不动。「既易通过、大规模下又便宜」的证明器依然不存在。所以我们不注水：堅持上一回的结论 —— 能 verified 地做结构进化的，**目前仅限 n≤6 的小部件**。

下一回（#40 以后）是 Phase 2 —— 把校准好的「多峰性 instrument」当到实损失地形上，以 proper power 确定一件关于进化如何在地形上移动的事（capability 副线）。尺子造好了。下一步，是用那把尺子去量实地形。

正本：[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) —— 论文草稿 + 全部实验代码/数据（5 实验 + 敌对验证 workflow）。

---

---

## 第3章 这是什么 — "我以为赢了的那一刻，自己的框架把自己拦住了"

上一篇(#39)我们这样收尾："带证明地进化的记忆核心做出来了。但只到 n≤6 的小部件。可扩展性的墙纹丝不动。"

这次(2026 年 6 月 10 日)我们终于回答了一直被搁置的**核心问题**：

> **"那么，这个'会进化的记忆'真的会变聪明吗？比梯度法(普通的学习)更强吗？"**

一句话结论：**"在真实小型 LLM 生成的真实地形上，进化以 20 比 0 战胜了普通梯度法。一瞬间我以为赢了。但遵循自己框架的纪律换上'强对手'之后，那场胜利只是幻觉。"**

这是研究中最可怕的瞬间 —— **"出现了异常好的结果的瞬间"** —— 在得意之前如何怀疑自己的记录。仍按 ①术语 → ②通俗解释 → ③细节 的顺序，不夸张地写。最后公开让**验证 AI 并行反驳**我的数值主张的结果(零个 MAJOR 不一致)。

正本数据：[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)(全部实验代码/数据 + verdict)。

---

### ① 术语小词典

| 术语 | 一句话 |
|---|---|
| **capability(性能)** | "会变聪明吗"。这里指预测下一个的好坏(交叉熵 CE 越小越好)。 |
| **guarantee(保证)** | "会不会失控"。带证明地保持稳定(收缩 ρ<1)。本研究的主轴。**不混淆这两者是 honest-disclosure 的生命线。** |
| **MAP-Elites(进化)** | 在格子里囤积多样解同时搜索的进化式探索。这里的"进化"方。 |
| **finite-diff 梯度(弱)** | 通过微调函数值来**估计**斜率的朴素梯度法。每步要维数+1 次评估＝**慢而弱**。 |
| **解析(exact)梯度(强)** | 用自动微分(backprop)一次得到**精确**斜率。真实 LLM 训练用的就是它。本次的决定因素。 |
| **meta-gate** | 当进化"赢了"，换上**更强的对手**确认增益是否消失。消失则是幻觉(ARTIFACT)。 |
| **ARTIFACT(假象)** | 不是真实性能差，而是因**对手太弱**产生的表面胜利。 |
| **兰顿蚂蚁** | 规则简单却先显混乱后突现秩序的著名系统。比喻"表象 ≠ 本质"。 |

---

### ② 通俗解释 — "对弱对手 20 连胜，什么也说明不了"

用棒球打比方。你的队(进化)对某对手(finite-diff 梯度)**20 比 0**。强，没话说。

…但如果那对手是**业余球队**呢？20 连胜不能证明*你*强 —— 也许只是*对手弱*。

在研究里这么干会出大事故。你在论文里写"进化赢了梯度！"，后来有人说"不，你比的那个梯度法太弱了"。这就是 **capability 的陷阱**。

所以我们的框架从一开始就内置了**规矩(meta-gate)**：

> **进化赢了，得意之前先请"职业选手"再战。**

我们请来了职业选手(解析梯度＝真实 LLM 训练用的精确梯度)。结果：

- 对业余(finite-diff)：进化 **20–0**(平均 CE 领先 +0.029)
- 对职业(解析梯度)：进化 **1–19**(职业反超)

也就是说**进化能赢只是因为对手弱**。换上强梯度，梯度更好。**"进化会变聪明(capability)"无法主张。**

关键在于：**输本身不是失败。** 我们框架的价值从一开始就不在"聪明"一侧(capability)，而在**"不失控"一侧(guarantee)**。这次的结果意味着那个方针**在数据上是对的** —— 没拿聪明来卖是对的。

---

### ③ 细节 — 在真实 LLM 地形上，测了什么、怎么测

#### 3-1. 地形从"合成"到"真实"

此前的 capability 实验在**人工多峰地形**(造出来的有多个山的地貌)上测。我们诚实地留了保留："这不是真实 LLM 的损失地形。"

这次用**真实的 SmolLM2-135M**(Apache-2.0 小型 LLM)补上：

1. 让文本通过 SmolLM2，取出中间层(layer 15)的**真实内部表示(hidden state)**。
2. 投影到小维度(n=6)，构造**预测"下一个内部表示的簇"的 CE 地形** —— 不是合成高斯，而是**源自模型自身内部动态的真实预测任务**。
3. 在该地形上，用同样的预算(评估次数)跑进化(MAP-Elites)/随机/弱梯度/**强解析梯度**，在**未见过的句子(held-out)**上以 20 个种子比较。

#### 3-2. 结果(held-out 平均 fitness = −CE，越高越好)

| 方法 | held-out 平均 | 备注 |
|---|---|---|
| **强解析梯度(torch Adam)** | **−1.446** | **全部最佳** |
| 进化(MAP-Elites) | −1.454 | 第 2 |
| 随机 | −1.473 | |
| 弱梯度(多重启) | −1.481 | |
| 弱梯度(finite-diff) | −1.483 | **最末** |
| 进化+ρ<1 gate | −1.483 | 加 gate 后探索被约束到 finite-diff 水平 |

- 进化 vs **弱梯度**：+0.029 平均，**20–0**，p<1e-6 → 4 条件 AND **成立**(看似 EXISTS)。
- 进化 vs **强解析梯度**：−0.008 平均，**1–19**，梯度以 p=3.5e-4 反超 → 4 条件 AND **不成立**。

**→ 判定 = ARTIFACT+NEGATIVE。** 进化的胜利源于对手弱。换强梯度，梯度 ≥ 进化 = **即便在真实 LLM 地形上 capability 也是 NEGATIVE**。

#### 3-3. 还确认了两种地形上一致(cross-check)

"那之前合成地形的'平局(NULL_TIE)'是不是也被弱梯度低估了？" —— 这个疑问也**用数据确认了**。给合成地形加上强解析梯度重跑，**解析梯度平均最高**(0.575 > 进化 0.535)。只是合成地形运气波动(方差)大，配对检验止于平局。真实地形波动小，梯度的优势达到了**显著**(19/20)。

**结论：capability NEGATIVE 在两种地形上一致**(强梯度在两边都最佳)。区别只在方差。

#### 3-4. "框架看穿真相"的一侧 PASS

capability 卖不了。那么立得住的是 —— **guarantee(安全性的判别力)**。同一节里确认了三点：

- **判别力**：基于经验的 gate **漏掉 84%** 的"危险结构"(会失控却当作"安全"放行)。**健全证明器漏 0%**。尤其 cert_sdp 零误许且过度拒绝仅 4.6%＝**健全且最易通过**。
- **base 级判别**：Mamba(结构上稳定的 SSM)全 24 层固有稳定 → 自明通过。标准 Transformer 的 SmolLM2 没有状态递归 → **安全性必须靠后加的 gate 才被赋予**。框架能在 base 级分开"安全底座"和"需要 gate 的底座"。
- **可扩展性(framework 性)**：基质·目的·证明器三个插口，可用**单对象替换**载入(单元测试 17 项 green)。但"多样性帮助泛化"的假说为 **NULL**(不成立) —— 也诚实公开。

#### 3-5. 用"动"来看 —— 范数不会暴走，只有敏感度暴走

附带发现。这个基质用 tanh 让状态始终有界，所以**即使不稳定，输出范数也不发散**。更甚，ρ≈2.9 的失控个体在某一条轨道上扰动**看起来在衰减**(正是兰顿蚂蚁＝表象背叛本质)。看状态范数、做有限视野的"遗忘测试"，**都看不穿 ρ≥1**。能看穿的只有**证明器的最坏情况评估(box-sup)**。demo 把这"经验被骗、唯证明器能看穿"做成了一张图(`phase2_demo_gate_discrimination.svg`)。

---

### honest disclosure — 最可怕的瞬间，我怀疑了什么

最危险的是**看到"进化 20–0"的瞬间**。一个适合社交媒体的标题闪过("发现进化战胜梯度的真实 LLM 地形！")。

拦住我的不是新灵感，而是**从一开始就内置的规矩(meta-gate)**："赢了就请强对手。"请了，输了。所以不能写。

这不是输的报告，而是**框架奏效的报告**。没有 meta-gate，我就会发布一个谎言。"异常好的结果，得意之前先怀疑内幕" —— 这条纪律，在数据上实实在在地拦下了一个假阳性。

剩余的诚实保留：
- 是隐藏簇 CE 的 proxy，不是全词表 softmax CE(小 n 下全词表会退化)。
- 加 gate 在真实地形上掉 −0.028 性能(可测量地削减可塑性)。但因进化没有 capability 优势，不影响结论。
- "强梯度最佳"的前提是 backprop 免费给出精确梯度 —— 这正是真实 LLM 训练所做的，所以是现实的比较。

### 验证 — 让 AI 反驳我自己的主张(MAJOR 0)

最后，让**独立的验证 AI 并行反驳**三个实验的数值主张。尤其主结果(capability)，验证 AI **自己加载 SmolLM2 独立重跑 3 个种子**，确定性地重现"强梯度胜过进化"。**零个 MAJOR 不一致。** 所有指摘都是改善可复现性/措辞/保留精度，无一推翻结论(一处发现验证用随机数不可复现的缺陷，当场改为确定性并重跑)。

---

### 总结 — "可进化的 LLM"的真面目

三篇(#38→#39→#40)的弧，我们落到这里：

- **#38**：防御性公开 —— "带证明的记忆"的窗在理论上打开。
- **#39**：窗在实现上关闭。但**可扩展性的墙**纹丝不动(带证明地进化只到 n≤6)。
- **#40(本篇)**：那会变聪明吗？→ **不会。** 即便在真实 LLM 地形上，强梯度也胜过进化。**capability 卖不了。**

所以"可进化的 LLM"的真面目是：**不是"进化在性能上取胜的 AI"，而是"对在线改变结构也不失控·不灾难性遗忘这一点，带证明地保证并测量的框架"。** 朴素。但既然决定**不夸大聪明、以安全取胜**，这就是诚实的样子。

下次计划用"看穿兰顿蚂蚁幻象之眼"这一比喻来总结这个框架。经验被表象欺骗；唯证明器看见本质 —— 在这一点上，三篇的 honest disclosure 全部汇聚。

---

<a id="한국어"></a>

---

## 第4章 这是什么 —— 把三篇束于一点：「简单的确定性规则制造出表面的秩序」

这是 llcore 验证 arc(#38 → #39 → #40)的**总括(capstone)**。上一篇(#40)结尾我们预告："下次计划用'看穿兰顿蚂蚁幻象之眼'这一比喻来总结这个框架。经验被表象欺骗；唯证明器看见本质 —— 在这一点上，三篇的 honest disclosure 全部汇聚。"

兑现这个承诺。先说一句话：

> **"越用越聪明/自我进化的 AI"和"世界模型给你安全"都是悦耳的标题。但若不能用 sound certificate(健全证明)falsifiable 地判别"变聪明了/稳定了"是真是幻，那就只是"表象"。verified-plasticity 正是那个判别器。价值在 GUARANTEE(保证)，不在 capability(聪明)。**

概念钩子是**兰顿蚂蚁**。仅由几条确定性规则驱动的蚂蚁，先无序地走一阵，然后突然开始建造称为"高速公路"的规则轨迹。**简单的规则制造出表面的秩序与表面的复杂。** 这是核心比喻：我们在 #38-#40 反复撞到的，正是"**经验观测被简单之物制造的'表象'所欺骗**"。

- 本该发散(暴走)的结构，观测起来**看似稳定**(#40 的兰顿蚂蚁)。
- 进化，观测起来**像是 20 比 0 战胜梯度**(#40 的兰顿蚂蚁 ver.2)。

两者都是"表象"，其下的本质(真正的不稳定、真正弱的对手)**经验看不穿，唯 sound certificate 看穿**。在这一点上，三篇合为一体。

仍按 ①术语 → ②通俗 → ③详细。不注水。只用确定的 verified 数值，未验证就写"未验证"。**绝不混淆** capability(进化胜过梯度)与 guarantee(带证明的稳定) —— honest disclosure 的生命线。

正本：[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore)。

---

### ① 术语小词典

| 术语 | 一句话 |
|---|---|
| **verified-plasticity** | 在真实小型 LLM 上后加小结构块(n≤16 的 verified recurrent adapter),把其在线结构适应"是否不发散/是否收缩(健全地保持 ρ<1)"作为第一级指标,可证伪地衡量任意方法的评价框架。本研究主轴。 |
| **capability(性能)** | "会变聪明吗"。预测下一个的好坏(交叉熵 CE 越小越好)。 |
| **guarantee(保证)** | "会不会失控"。用 sound certificate 保持稳定(收缩 ρ<1)。**不混淆这两者是 honest disclosure 的生命线。** |
| **收缩性 (contraction, ρ<1)** | 过去的扰动随时间被**遗忘(衰减)**。谱半径小于 1。echo-state property 的合格条件。 |
| **echo-state property** | 状态由输入历史决定,初始扰动被遗忘。"成立(ρ<1)"=安全,"失败(ρ≥1)"=可能暴走。 |
| **false-admit(假合格)** | 明明危险(ρ≥1)却被 gate 当作"安全"放行的漏检。为零是健全性命门。 |
| **sound(健全)** | 一旦说"合格"就**真的安全**(绝不假合格)。与统计"大概安全"是两回事。 |
| **navigability(易通过)** | "能把多少真正安全的个体判为合格"。过严的 gate 连安全个体也弹掉=进化动不了。越高越好。 |
| **经验 gate** | 不是健全证明,而靠有限视野观测(遗忘测试等)判"看似安全"的 gate。本研究负对照之一(STABLE 风)。 |
| **sound certificate(健全证明器)** | 带保证地从上方压住最坏情况的证明器(cert_inf / cert_two / cert_sdp)。唯它看穿"表象"。 |
| **MAP-Elites(进化)** | 在格子里囤多样解同时搜索的进化探索。"进化"方。 |
| **finite-diff / 解析梯度** | 弱梯度(微调估计斜率,dim+1 评估/步) vs 强梯度(backprop 一次得精确斜率)。 |
| **meta-gate** | 进化"赢了"时换更强对手(解析梯度)确认增益是否消失。消失则是幻觉(ARTIFACT)。 |
| **兰顿蚂蚁** | 由几条确定性规则驱动的蚂蚁;先无序后突现"高速公路"。**简单确定性制造表面秩序/复杂**的比喻。 |

---

### ② 通俗 —— 兰顿蚂蚁的幻象,三个场景

#### 场景 0: 兰顿蚂蚁是什么(为何用此比喻)

兰顿蚂蚁在格子上只靠两条规则("白格右转并翻色"/"黑格左转并翻色")移动。最初几百步无序乱走,但约一万步后突然建出称为"高速公路"的**104 步周期规则模式**并径直前进。

这里藏着本研究两大核心:(1)**简单的确定性规则制造表面的秩序/复杂** —— 规则极简,结果却看似复杂("无序→突现秩序")。(2)**表象与本质相背** —— 观测乱走中的蚂蚁无法预见高速公路,反之亦然。**经验观测被简单之物制造的"表象"欺骗。**

主张:AI 世界也如此。"表面的稳定"和"表面的进化(monoculture=表面优势)"在其下都坍缩为 **deterministic-simple(简单确定性)**。经验被骗,唯 sound certificate 看穿幻象。

#### 场景 1: "表面的稳定" —— 暴走结构观测起来看似稳定

后加于 LLM 的小记忆块用 `tanh` 让状态始终有界。所以**即便不稳定(ρ≥1),输出范数也不发散**。

于是:**真 ρ=2.9(完全发散域)的结构,沿某一条轨道观测,初始扰动也"看似在衰减"** —— 实测扰动 1 缩到 `2e-14`,宛如安全。这是 `tanh` 饱和 + 扰动方向错位偶然叠加之果。

朴素手段全军覆没:看状态范数→有界无异常(被骗);有限视野"遗忘测试"→看似遗忘(被骗);单一轨道扰动敏感度→看似衰减(被骗)。这正是兰顿蚂蚁。**简单力学(tanh 有界)给危险结构制造"安全"表象。** 唯一看穿的是 **sound certificate 的最坏情况评估(box-sup)** —— 它压住所有输入/状态的最大放大,不被偶然安全的一条轨道骗。实测 `σ_max = 4.87 > 1` 并正确 reject。

#### 场景 2: "经验 gate 漏掉 84%" —— 幻象的规模

群体规模:95 个发散 gene(真暴走)+ 305 个收缩 gene(真安全)的 400 个集团,各方法漏检多少危险(false-admit)?

- **无 gate**:把 95/95 发散全当"安全" = **false-admit 100%**。
- **STABLE 风经验 gate**:95 个发散中**漏 80 个(84.2%)**。
- **sound certificate**:发散 false-admit **0%**。

84% 的冲击在于:它几乎没比"不检查 100%"改善。经验 gate **以为在检查,却被兰顿蚂蚁幻象骗了 84%**。原因如场景 1:`tanh` 有界力学下,发散结构在有限视野观测里"看似遗忘扰动",经验 gate 立足于有限视野观测,便照单全收。sound certificate 带保证地压最坏情况,不被表象左右。尤其 **cert_sdp 保持 false-admit 0% 而过度拒绝仅 4.6%** —— 健全且最易通过。

#### 场景 3: "表面的进化" —— 进化看似 20 比 0 取胜(却是幻)

兰顿蚂蚁 ver.2 发生在 capability 侧。

在真实 SmolLM2 造的真实地形上,进化(MAP-Elites)对弱梯度(finite-diff)→ **进化 20 比 0**(平均 CE +0.029,p=9.5e-7)。看似出现进化胜梯度的"秩序",适合社媒的标题闪过。

但这也是兰顿蚂蚁。**对手(finite-diff)只是弱。** 框架从一开始就内置 meta-gate(赢了就请强对手)。换强解析梯度(backprop=真实 LLM 训练用的精确梯度)同预算,**梯度以 19/20 反超**(diff +0.008,p=3.5e-4)。进化的胜利是弱对手的 artifact。判定 = **ARTIFACT + NEGATIVE**。

最关键:**没有 meta-gate(健全的比较对手),我就会发布"进化在真实地形 20/20 capability 取胜"的 false-positive。**"得意之前先怀疑内幕"在数据上拦下一个假阳性 —— 这也是健全判别器看穿兰顿蚂蚁。

---

### ③ 详细 —— H-discriminative 数值、capability 顛末、framework 性、small-n 墙

#### 3.1 verified-plasticity 测什么

主轴是 **Verified-Plasticity Evaluation Framework**。主张"我们强"前先造**尺子**。尺子由六装置守护:(1)预登记 (2)Holm 连言判定 (3)artifact 纪律 (4)反证条款 (5)自检出力审计(正对照) (6)反 over-claim critic。

被测方法四个:**VSOA**(cert-gated 拓扑进化,本命)、**无 gate**(负对照)、**STABLE 风经验 gate**(既踏比较)、**Mamba-130M**(stable-by-construction 正对照)。

准确说,稳定性指标不是"状态是否发散"而是 **"echo-state 扰动遗忘"**。kernel 用 `tanh` 始终有界(场景 1 幻象之源),测的是"初始扰动是否被遗忘(收缩 ρ<1 = echo-state property 成立)"。

#### 3.2 H-discriminative —— 框架判别力(核心数值)

n=6,95 发散 / 305 收缩 集团。

| method | 是否 sound | false-admit(漏检发散) | 过度拒绝(收缩) |
|---|---|---|---|
| 无 gate | ✗ | **95/95 = 100%** | 0% |
| STABLE 风经验 gate | ✗ | **80/95 = 84.2%** | (经验 gate) |
| cert_inf | ✓ | **0%** | 70.5% |
| cert_two | ✓ | **0%** | 52.8% |
| **cert_sdp** | ✓ | **0%** | **4.6%(最易通过)** |

正对照(0 发散安全 family 集团,Mamba 风)中**全 method 0 false-admit** —— 不会误弃安全 family。

**为何 STABLE 风 gate 漏 84%(教育性):** echo-state 合格条件是"真 ρ<1"。但 kernel `tanh` 始终有界时,**真 ρ≥1 的发散结构在有限视野观测里也看似遗忘扰动** —— `tanh` 饱和把暴走放大藏在观测窗内。STABLE 风 gate 立足有限视野观测,便把此表象判为"安全"。这就是兰顿蚂蚁幻象。sound certificate 从上方压最坏情况(证明而非观测),不被左右。

**更深的幻象(连单轨道敏感度都被骗):** ρ≈2.9 的发散 gene **连单轨道扰动敏感度都不发散**(实测 1→2e-14),因 `tanh` 饱和 + 扰动方向错位叠加。于是状态范数监视、有限遗忘测试、单轨道敏感度三重漏掉 ρ≥1 —— 唯 box-sup sound certificate(`σ_max=4.87>1` reject)看穿。这是"非 sound certificate 看不穿"最强实证。

#### 3.3 capability 诚实顛末 —— synthetic NULL_TIE → 实 CE ARTIFACT+NEGATIVE

**(1) synthetic 多峰地形(K=6 basin)= NULL_TIE。** ME ≈ gradient ≈ random。ME vs gradient mean_diff +0.028 / Wilcoxon p=0.39 / sign_delta=0(n=20)。四条件 AND 全向不成立 = **纯平局** = capability 优势**未实证**。

**(2) 实 SmolLM2-CE 地形 = ARTIFACT + NEGATIVE。** 由 SmolLM2 layer 15 hidden state 造"预测下一内部表示簇"的 CE 地形,同预算四法对战(held-out 平均,越高越好):

| 方法 | held-out 平均 | 名次 |
|---|---|---|
| **解析梯度(torch Adam)** | **-1.446** | **第 1(全部最佳)** |
| 进化(MAP-Elites) | -1.454 | 第 2 |
| random | -1.473 | 第 3 |
| finite-diff(弱梯度) | -1.483 | 第 4 |

- 进化 vs finite-diff:ME **20/20 胜**(diff +0.029,p=9.5e-7,看似 EXISTS)。
- 进化 vs 解析梯度:解析 **19/20 反超**(diff +0.008,p=3.5e-4)。

→ ME 的胜是 finite-diff 弱(cold-start / dim+1 评估/步 / 预算内 ~95 步)的 **artifact**。强梯度下 gradient > evolution = **实地形上 capability 也 NEGATIVE**。

**honest disclosure 真价(拦下假阳性):** 没有 strong-gradient meta-gate,我就会**误结论"进化在实地形 20/20 capability 取胜"的 false-positive**。"得意前疑内幕"实际排除一个假阳性 —— 健全判别器(meta-gate)看穿兰顿蚂蚁 ver.2。

#### 3.4 framework 性(F8)—— (b) PASS / (a) NULL

**(b) 3 plug-point swap = PASS。** GeneCodec / Objective / VerifierBackend 三插口各以**单对象替换**,src 无改(git diff 空),pytest 17 green;per-gene two⇒sdp / inf⇒sdp 在 3000 gene 上 0 违反。

**(a) 结构多样性 → 泛化 load-bearing = NULL。** "结构多样性帮助泛化"假说**不成立**(held-out diff +0.011,p=0.55,第一级 NULL)。诚实公开 —— 可替换属实,但"多样性有效"未实证。

#### 3.5 Mamba SSM Lyapunov 正对照(§7.3)

为审计尺子自检出力(能否把安全底座正确判安全),用 Mamba。**Mamba-130M 全 24 层 A=-exp(A_log)<0(589,824 ch)** → λ_max≤0 自明 → stable-by-construction PASS。**SmolLM2 无 SSM**(llama 架构,仅 self_attn+mlp,无状态递归)→ 安全须靠后加 gate。框架在 base 级区分"安全底座(Mamba)"与"需 gate 底座(SmolLM2)"(PASS)。留保:这是 parameterization 的自明性 —— 任意 valid Mamba 结构性成立,检定的是"参数化保证稳定"而非"学到稳定"。

#### 3.6 敌对验证

用 **3 独立 skeptic + 实机 3 seed 再跑** 突合本 verdict 数值主张。结果 = **MAJOR 0 / 全 MINOR**,数值零 mismatch,无推翻机构结论的指摘。尤其主结果(capability),验证方实际加载 SmolLM2 独立再跑 3 seed,确定性重现"强梯度胜进化"。

#### 3.7 small-n 墙(第一级 negative)

guarantee 立得住,但**规模墙**诚实地留着。verified 结构进化仅限 **small-n per-component(n≤4-6)**。高维 navigable 且 sound 的 certifier **不存在**(第一级 negative)—— #39 的 2^n 墙之续。SDP(cert_sdp)只抬高 navigability 天花板,没破 2^n 成本墙。

---

### honest 留保(禁止 over-claim)

作为三篇总括,所有留保集于一处。为不混淆 capability 与 guarantee,务必一读。

- **capability NULL_TIE 是"非显著平局"**。既非"进化劣于梯度的 decisive proof",也非"powered 等价 proof"(power 未分析)。不可把 NULL_TIE 断定为"进化的失败" = **未实证**。
- **40 basin 可能是高维 hillclimb 不收敛 artifact**。稳健只说"多峰(>1)"。
- **gate 中立性仅限 held-out、capability flat regime 观测**。train 侧在 0.25 差有 archive 探索约束。
- **STABLE 84% 设定依赖**(EPS_FORGET=1e-2 / T=64 / K_PROBE=8 固定,敏感度未测)。方向(STABLE 漏危险)稳健,但"84%"非设定无关数值。
- **empirical_rho 从下方**。0 观测 false-admit 是强一致性,非绝对/机械证明。
- **实 CE 是 hidden 簇 CE proxy**(非全词表 softmax;小 n 全词表退化)。
- **verified 结构进化仅 small-n per-component(n≤4-6)**。高维 navigable-sound certifier 不在(第一级 negative)。
- **实 LLM transfer(tiny→SmolLM2 的 load-bearing)未验证**。

---

### 关于竞品的自我改进主张 —— 不贬低,只述"未验证"之事实

"越用越聪明/自我进化"的潮流是真的。2026-06-10 竞品扫描:**hermes-agent**(NousResearch, 189k★)—"20+ 技能快 40%";**ECC**(211.8k★)— Continuous Learning;**headroom learn** — 持续学习系。但这些性能主张**全为第三方未验证的自家 benchmark**(截至 2026-06-10)。star 数证明人气,不证明性能优势。

重点**不是贬低竞品**。它们"变聪明"的主张可能真,可能是兰顿蚂蚁幻象 —— **没有可证伪判别工具,外人无法区分**。verified-plasticity 正是此工具。连我们自己的主张(#40 进化 20-0)都在 meta-gate 下被证为幻,判别器的必要性已自证。

---

### 连世界模型都开不出保证 —— 区分贡献与保证

另一大潮流是**世界模型**:agent 内置环境模拟器预测行动。很强,也有助于安全设计。但作为技术事实,世界模型系手法一般有助于安全设计,**却不给出形式化的保证(guarantee)**。这是技术社区广泛共有的观察(2026 年的讲演也表达了同旨。藤吉弘亘氏)。贡献(contribution)与保证(guarantee)须作为两回事对待。

verified-plasticity 的定位由此清晰。世界模型系手法止于"贡献",而 **verified-plasticity 用 sound certificate 开出 GUARANTEE** —— 用证明而非表象压住"收缩(ρ<1,不暴走)"。非替代而是互补:世界模型聪明地预测行动,verified-plasticity 保证其结构适应不暴走。

从技术上说,这与一个一般观察一致:AI 历史一直朝着"机器自我获得(进化)原先靠人手设计的结构"的方向前进。本研究的进化命题也在同一方向上。谁来保证那"自我获得的结构"不暴走?verified-plasticity 的回答:"sound certificate 保证。"

---

### 总结 —— 三弧汇于一点

- **#38**:防御性公开 —— 理论上拿下"带证明记忆"的四点交叉点,以公开而非专利立旗。
- **#39**:窗在实现关闭,但 2^n 墙(small-n 墙)纹丝不动。
- **#40**:会变聪明吗?→ 不会。实地形上强梯度也胜进化。capability 卖不了(meta-gate 看穿兰顿蚂蚁 ver.2)。
- **#41(本篇)**:全部汇于一点 —— **"简单确定性制造表面秩序/复杂,经验被骗,唯 sound certificate 看见本质。"**

"可进化的 LLM"的真面目是 **"不是进化在性能取胜的 AI,而是用 sound certificate 保证并测量在线结构改变不暴走·不灾难性遗忘的框架"**。朴素。但"越用越聪明"和"世界模型给你安全"虽是悦耳标题,**可证伪地判别"变聪明了/稳定了"是真是幻的工具**却几乎没有。verified-plasticity 就是那个判别器。

价值在 **GUARANTEE 而非 capability**。世界模型开不出保证(止于贡献);verified-plasticity 用 sound certificate 开出保证。经验被表象欺骗 —— 唯证明器是看穿兰顿蚂蚁幻象之眼。

正本:[github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) — 论文草稿 + 全部实验代码/数据。

---

<a id="한국어"></a>

---

## 第5章 第5章

(後続セッションで展開予定 / 将在后续会话中展开)

---

<a id="한국어"></a>


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

<!-- CTAIMG -->

![「ひくわ」と一万円札を差し出す森田](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/012.jpg)
> 🗒️ *「ひくわ」— 紹介リンクで小銭を稼ごうとする魂胆、我ながらちょっと引く*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

<!-- /CTAIMG -->
