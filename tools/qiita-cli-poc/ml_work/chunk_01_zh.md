#### 通俗讲解: 什么是 ZMP

请想象两台体重秤并排、你站在上面的情形。脚底从地面受到的压力,存在一个"实质上就靠这一点支撑"的代表点(压力中心)。ZMP 理论的要点是:**只要这个点在脚底(支撑多边形)的内侧,机器人就不会开始以脚尖或脚跟为支点翻倒的旋转**。"不要摔倒"这个模糊的要求,变成了"把 ZMP 保持在脚底之内"这个可计算的条件。此后 40 年,双足行走控制几乎全部建立在这一行之上。

---

### 2. 本田的绝密 10 年(1986-1996)— P2 的冲击

1986 年,本田作为公司内部绝密项目启动双足行走研究。从 E1 开始的 E 系列是只有腿的实验机,最初一步要 20 秒。E2 达到接近人类的动态行走(1.2 km/h),随后进入在腿上装上上身与手臂的 P 系列 [^honda-st][^honda-p2]。

然后是 **1996 年 12 月,P2 的发布**。身高 180cm 级的机器人,在电源和计算机全部装进 body 的"自立"状态下,流畅地行走,还爬上了楼梯。因为 10 年间对外滴水不漏,据说全世界的机器人研究者都真的从椅子上站了起来。它具备针对凹凸地面、外部扰动(推搡)、楼梯・斜坡的 3 套姿态控制系统,成为此后人形机器人的技术基准 [^honda-p2]。这份历史意义在 2026 年 4 月以 IEEE 里程碑认定的形式被正式铭刻 [^honda-ieee][^honda-topics]。

---

### 3. 日本的黄金期(2000 年代)— ASIMO・HRP・QRIO

**ASIMO**(2000 年 11 月发布)是 P 系列的集大成。2002 年起在日本科学未来馆"上班",20 年间实演 1 万 5466 场,估计有 200 万人以上参观 [^miraikan-a][^miraikan-p]。奔跑・倒着走・单脚跳,一代代增加技能,2022 年 3 月 31 日从未来馆"毕业",同月底在本田总部完成了最后一场实演 [^miraikan-p]。

国家项目一侧,从经产省 HRP 的谱系中诞生了 **HRP-2 Promet**(2002,川田工业+产综研)。它能从仰卧・俯卧位起身这一点很重要,是"摔倒 = 实验结束"时代的转折点。外形设计出自出渕裕氏 [^hrp2]。2009 年的 **HRP-4C** 身高 158cm・体重 43kg,是贴合日本青年女性平均体型的"赛博人类(Cybernetic Human)",发布一周后就登上了东京时装周的舞台 [^hrp4c]。

索尼的 **QRIO**(2003)虽然小巧,却以"世界首台会跑的双足行走机器人"之名载入吉尼斯世界纪录 2005 年版的完成度。然而 2006 年 1 月 26 日,它与 AIBO 一起被宣布停止开发 [^qrio]。自此,日本的人形机器人研究进入少有高调发布的"冬天" — 不是技术死了,而是看不到商业化的出口。

---

### 4. 异端的谱系 — 不用马达行走的机器(1990)

把时钟稍微拨回去。1990 年,Tad McGeer 展示了**被动行走(passive dynamic walking)**。没有马达也没有控制计算机的双腿机器,只要放在缓坡上,就会"安顿"进稳定的步态 [^mcgeer]。这是一个发现:行走在成为精密控制的产物之前,首先是**摆动力学的固有模态**。

如果说 ZMP 派是"持续控制以时刻不倒"的思想,被动行走派则是"力学自己就会走,控制只需最小限度的助推"的思想。能耗可以低到 ZMP 型的几十分之一。这条谱系后来流入欠驱动行走・混合零动力学(hybrid zero dynamics),以及 Cassie 那样"不模仿人类的腿"的设计思想。

---

### 5. DRC(2015)— "摔倒集锦"教会的事

以 2011 年福岛第一核电站事故为直接动机,DARPA 举办了灾害应对机器人竞赛 **DARPA Robotics Challenge**。2015 年 6 月的决赛(美国波莫纳)比拼开车、开门、拧阀门、瓦砾行走等 8 项任务,韩国 KAIST 的 **DRC-HUBO** 以约 44 分钟完成全部任务夺冠,获得 200 万美元奖金 [^drc-kaist][^drc-ieee2]。DRC-HUBO 膝部带轮,"只在必要时才双足"的取舍立了功。

但留在世界记忆里的不是冠军,而是**摔倒集锦**。世界最顶尖团队的机器人,在门把手前、握着电钻,一台接一台像慢动作一样倒下去的影像 [^drc-ieee]。那些影像也曾沦为嘲笑的对象,但对研究社区来说,它是一次对现在位置的精确测量 — 不依赖外部电源和网络、在未知环境中作业这件事,在 2015 年时点有多难。摔倒后能自力爬起继续比赛的只有 CHIMP 一台 [^drc-na]。DRC 之后,各国研究明确地从"演示成功一次"转向"鲁棒性"。

---

### 6. Atlas 的时代(2013-2024)— 从液压的杂技到电动的实用

作为 DRC 标准机登场的 Boston Dynamics 液压 **Atlas**,此后 10 年在 YouTube 上持续让世界沸腾。奔跑,跳跃,后空翻。背后是基于 QP 的全身控制・基于优化的运动规划,MIT 团队为 DRC 版 Atlas 构建的方法已作为论文公开 [^kuindersma]。

2024 年 4 月,Boston Dynamics 同时宣布液压 Atlas 退役与全电动的新型 Atlas [^bd-atlas][^tc-atlas]。液压虽然强力,但吵、复杂、需要专用液压油,维护成本阻碍了商用化。电动化是从"研究的顶点"向"Hyundai 工厂里使用的工具"的转身宣言。

同一时期,俄勒冈州立大学孵化的 Agility Robotics 走着另一条路。鸵鸟腿一般的 **Cassie**(作为研究平台约从 2016-17 年起销售)舍弃人形、专注于腿,后来创下双足行走机器人 100m 跑的吉尼斯世界纪录 [^agility]。在那双腿上装上躯干・手臂・感知的 **Digit**,成为物流仓库商用投放的领跑机体 [^agility]。

---

### 7. RL + sim-to-real 的浪潮(2019-)— 控制律从手写变成让它学

2019 年,ETH Zürich 的 Hwangbo 等人在四足 ANYmal 上展示的结果 [^hwangbo],是整个腿式机器人领域的转折点。把在仿真中强化学习的策略,原样(zero-shot)迁移到实机。关键是把物理参数随机化、连"仿真的谎言"一起学掉的域随机化。

双足方面,2021 年,Cassie 的 RL 策略在实机上实现了**无外界传感器・仅靠本体感受**(只用关节角、力等体内感觉)上下楼梯 [^siekmann]。2023 年,Berkeley 的团队报告了基于 Transformer 策略的人形实机行走 [^rado]。源自 ZMP 的"建模求解"控制,与 RL 的"在仿真里吃够苦头用身体记住"控制,现在正走向叠层(模型基座+学习增强鲁棒性)而非对立。

---

### 8. 中国势力的崛起(2023-)— 数量与价格的时代

最快乘上这股浪潮的是中国。Unitree、UBTech、Fourier,以及北京国资系创新中心开发的"天工(Tiangong)"。有两件标志性事件。

- **2025 年 4 月 19 日,北京**: 世界首个人形机器人半程马拉松。天工 Ultra 以 2 小时 40 分 42 秒跑完 21.0975 km 并夺冠 [^cgtn]。
- **2025 年 8 月 14-17 日,北京**: 第一届世界人形机器人运动会(World Humanoid Robot Games)。16 个国家 280 支队伍・超过 500 台机器人齐聚 2022 年冬奥会的冰丝带(国家速滑馆),Unitree 包揽 1500m・400m・100m 栏・4×100m 接力 4 冠 [^whrg][^ran][^cnbc]。100m 跑天工跑出 21.50 秒 [^gt]。

然后是价格。Unitree G1 基本配置一万美元冒头(官方网站标价 US$13.5K〜)[^g1]。从 ASIMO"花几亿日元的机器人只能参观"的时代,到"大学研究室可以正常购买",这个变化在这 2 年里发生了。另外,北京的大会上机器人也仍在大摔特摔 [^smith],从 DRC 的摔倒集锦过去 10 年,摔倒从"耻辱"变成了"当作耗材预先计入的前提" — 我认为这才是准确的说法。

---

### 9. 控制理论的谱系 — 每代 2〜3 行,共 5 代

**① ZMP(1968-72 / Vukobratović,实现在加藤研・本田)**
只要脚底压力中心在支撑多边形内侧,翻倒旋转就不会开始 — 这样一个判定条件。成为此后所有行走控制的词汇。
代表文献: Vukobratović & Borovac "Zero-Moment Point — Thirty Five Years of its Life" [^zmp35]

**② 预观控制(2003 / 梶田等・产综研)**
把机器人简化为"桌上的小车"(线性倒立摆),**预读数步之后的 ZMP 目标**来生成重心轨迹。是 HRP 系列行走的脊梁,因实现简单而成为世界各地的标准。
代表文献: Kajita et al., ICRA 2003 [^kajita]

**③ Capture Point(2006 / Pratt 等)**
用线性倒立摆以闭式解计算"现在被推了一把,**脚落在哪里才能停住**"。把行走重新理解为"对摔倒的连续回避",把应对推搡扰动的迈步恢复理论化。
代表文献: Pratt et al., Humanoids 2006 [^pratt]

**④ MPC / WBC(2010 年代 / MIT・IHMC 等)**
每个周期重新优化未来数百 ms 运动的 MPC,与在接触力・关节力矩约束下用 QP 同时求解全身任务的全身控制(WBC)。液压 Atlas 的杂技和 DRC 机的作业能力属于这一代。
代表文献: Kuindersma et al., Autonomous Robots 2016 [^kuindersma]

**⑤ RL + sim-to-real(2019- / ETH・OSU・Berkeley 等)**
在数千台并行的仿真中强化学习策略,靠域随机化迁移到实机。对难以建模的接触・非平整地形・故障的鲁棒性提升了一个数量级。
代表文献: Hwangbo et al. 2019 [^hwangbo] / Siekmann et al. 2021 [^siekmann] / Radosavovic et al. 2023 [^rado]

#### 通俗讲解: 用自行车说 5 代

①"知道不倒的条件"②"看着几秒后的路面打方向"③"被推的瞬间就知道脚该落哪"④"每一瞬间用计算器优化全身肌肉的用法"⑤"装着辅助轮摔 1 万次,用身体记住"。现实中的现代机器人,正接近"④的骨架叠上⑤的反射"的状态 — 可以说"既有理论又有体感"。

---

### 10. 日本的贡献与现在位置

50 年史的前 30 年,几乎就是日本史。世界首台全尺寸人形(WABOT-1)[^robogaku]、动态行走的企业级实现(本田 E/P/ASIMO)[^honda-p2]、行走模式生成的世界标准(梶田的预观控制)[^kajita]、能爬起来的人形机器人(HRP-2)[^hrp2]、会跑的小型机(QRIO)[^qrio] — 每一项都是一次发明。ASIMO 于 2022 年退役,但其控制・平衡技术在本田内部由 avatar 机器人等研究继承 [^honda-st]。

现在也仍有玩家:川田系的 HRP 资产、川崎重工的人形机器人"Kaleido"(2017 年国际机器人展上首次公开。官方一次 URL 在本文执笔时点未确认可达)、丰田的遥操作型 T-HR3(2017 年发布)[^toyota-wiki]。不过,以"数量・价格・迭代速度"跑在最前线的是现在的中国势力,公平来看这也是事实。日本 50 年的积累并没有消失 — ZMP 和预观控制,今天也在北京奔跑的机器人体内被计算着。

---

### 11. 结语 — 1973 年的 45 秒,与家中的 0.002 秒

WABOT-1 的一步是 45 秒。国家项目和大企业的绝密研究花 30 年解开了"行走",DRC 的摔倒集锦教会了谦虚,RL 把手写控制律的工作替换成学习,中国势力把价格砍掉了 2 个数量级。

然后是 2026 年。这篇文章正文所做的,是在一台装着市售 GPU 的家用 PC 上跑 G1 的模仿学习和 RL,几个小时得到行走策略。一帧 0.002 秒的仿真,每秒几十万步。在 WABOT-1 迈出一步的那 45 秒里,家中仿真器里的机器人已经摔了几万步,每摔一次都变强一点。在 50 年的理论与失败之上,现在个人也有了能站上去的地方 — 那个脚手架的高度,时常令我眩晕。

---

### 出处一览

[^robogaku]: ロボ學(日本ロボット学会)「Wabot 1」 https://robogaku.jp/history/integration/I-1973-1.html (日文)
[^waseda50]: 早稲田大学「早稲田のロボット: ヒューマノイド研究50年の歩み」 https://www.waseda.jp/inst/fro/news/2026/06/10/1976/ (日文)
[^nikkei-w1]: 日本経済新聞「世界初の人間型ロボ『WABOT-1』 45秒で一歩 確かな進歩」 https://www.nikkei.com/article/DGKDZO70746270T00C14A5MZ9000/ (日文)
[^wabot2]: 早稲田大学ヒューマノイド研究所 booklet(WABOT-2) http://www.humanoid.waseda.ac.jp/booklet/kato_2.html (日文)
[^zmp35]: Vukobratović & Borovac, "Zero-Moment Point — Thirty Five Years of its Life," IJHR 2004(PDF) https://www.cs.cmu.edu/~cga/legs/vukobratovic.pdf
[^honda-st]: Honda Stories「ASIMOの原点『P2』…IEEEマイルストーンに認定」 https://global.honda/jp/stories/025.html (日文)
[^honda-p2]: Honda 官方「Hondaのヒューマノイドロボット P2」 https://global.honda/jp/tech/robotics/P2/IEEE/ (日文)
[^honda-ieee]: Honda R&D「Honda P2 IEEEマイルストーン認定」 https://global.honda/jp/RandD/activity/rdtopics/IEEE-P2/ (日文)
[^honda-topics]: Honda 企业新闻(2026-04-28) https://global.honda/jp/topics/2026/c_2026-04-28a.html (日文)
[^miraikan-a]: 日本科学未来館「ヒューマノイドロボット ASIMO(2002〜2022)」 https://www.miraikan.jst.go.jp/resources/archives/asimo.html (日文)
[^miraikan-p]: 日本科学未来館新闻稿「ありがとう!ロボット『ASIMO』」 https://www.miraikan.jst.go.jp/news/press/202201312305.html (日文)
[^hrp2]: Wikipedia (en) "HRP-2" https://en.wikipedia.org/wiki/HRP-2
[^hrp4c]: 産総研新闻稿「人間に近い外観と動作性能をもつヒューマノイドロボット(HRP-4C)」2009-03-16 https://www.aist.go.jp/aist_j/press_release/pr2009/pr20090316/pr20090316.html (日文)
[^qrio]: Wikipedia (en) "QRIO" https://en.wikipedia.org/wiki/QRIO
[^mcgeer]: McGeer, "Passive Dynamic Walking," IJRR 9(2), 1990 https://journals.sagepub.com/doi/abs/10.1177/027836499000900206
[^kajita]: Kajita et al., "Biped Walking Pattern Generation by using Preview Control of Zero-Moment Point," ICRA 2003(PDF) https://mzucker.github.io/swarthmore/e91_s2013/readings/kajita2003preview.pdf
[^pratt]: Pratt et al., "Capture Point: A Step toward Humanoid Push Recovery," Humanoids 2006(PDF) https://www.cs.cmu.edu/~cga/legs/Pratt_Goswami_Humanoids2006.pdf
[^kuindersma]: Kuindersma et al., "Optimization-based locomotion planning, estimation, and control design for the Atlas humanoid robot," Autonomous Robots 2016 https://doi.org/10.1007/s10514-015-9479-3
[^drc-kaist]: KAIST News "KAIST's DRC-HUBO Wins the DARPA Robotics Challenge" https://www.kaist.ac.kr/newsen/html/news/?mode=V&mng_no=4379
[^drc-ieee]: IEEE Spectrum "DARPA Robotics Challenge Finals Winner" https://spectrum.ieee.org/darpa-robotics-challenge-finals-winner
[^drc-ieee2]: IEEE Spectrum "How KAIST's DRC-HUBO Won the DARPA Robotics Challenge" https://spectrum.ieee.org/how-kaist-drc-hubo-won-darpa-robotics-challenge
[^drc-na]: New Atlas "South Korea's Team KAIST wins 2015 DARPA Robotics Challenge" https://newatlas.com/darpa-drc-finals-2015-results-kaist-win/37914/
[^bd-atlas]: Boston Dynamics Blog "An Electric New Era for Atlas" https://bostondynamics.com/blog/electric-new-era-for-atlas/
[^tc-atlas]: TechCrunch "Boston Dynamics' Atlas humanoid robot goes electric"(2024-04-17) https://techcrunch.com/2024/04/17/boston-dynamics-atlas-humanoid-robot-goes-electric/
[^agility]: Wikipedia (en) "Agility Robotics"(Cassie/Digit/100m 吉尼斯纪录) https://en.wikipedia.org/wiki/Agility_Robotics
[^hwangbo]: Hwangbo et al., "Learning agile and dynamic motor skills for legged robots," Science Robotics 2019(arXiv) https://arxiv.org/abs/1901.08652
[^siekmann]: Siekmann et al., "Blind Bipedal Stair Traversal via Sim-to-Real Reinforcement Learning," RSS 2021(arXiv) https://arxiv.org/abs/2105.08328
[^rado]: Radosavovic et al., "Real-World Humanoid Locomotion with Reinforcement Learning," 2023(arXiv) https://arxiv.org/abs/2303.03381
[^g1]: Unitree 官方 "G1" https://www.unitree.com/g1
[^cgtn]: CGTN "'Tiangong' robot wins world's first humanoid half-marathon"(2025-04-19) https://news.cgtn.com/news/2025-04-19/-Tiangong-robot-wins-world-s-first-humanoid-half-marathon-1CH3pjBuhOw/index.html
[^whrg]: Wikipedia (en) "World Humanoid Robot Games" https://en.wikipedia.org/wiki/World_Humanoid_Robot_Games
[^ran]: Robotics & Automation News "Unitree dominates inaugural World Humanoid Robot Games with four gold medals" https://roboticsandautomationnews.com/2025/08/26/unitree-dominates-inaugural-world-humanoid-robot-games-with-four-gold-medals/93926/
[^cnbc]: CNBC "Tesla Optimus rival Unitree shines at the 'World Humanoid Robot Games' in China"(2025-08-18) https://www.cnbc.com/2025/08/18/world-humanoid-robot-games-china-tesla-unitree.html
[^gt]: Global Times "First World Humanoid Robot Games conclude" https://www.globaltimes.cn/page/202508/1341057.shtml
[^smith]: Smithsonian Magazine "World's First 'Robot Olympics' Featured Soccer, Kickboxing and Lots of Falling Down" https://www.smithsonianmag.com/smart-news/worlds-first-robot-olympics-features-soccer-kickboxing-and-lots-of-falling-down-180987199/
[^toyota-wiki]: Wikipedia (en) "Toyota Partner Robot"(T-HR3, 2017) https://en.wikipedia.org/wiki/Toyota_Partner_Robot

#### 未确认项目(honest disclosure)

- **WL-10RD(1984)是靠 ZMP 实现的世界首次动态行走**这一记述,基于通说・回顾性论文,未能在早稻田的一次页面 URL 中确认。正文中止步于"据称"。
- **Cassie 的 100m 纪录的具体成绩(24.73 秒)**: Oregon State 官方新闻被 bot 拦截(HTTP 403)无法确认内容,正文未写成绩,只写"创下吉尼斯纪录"(用 Wikipedia Agility Robotics 佐证)。
- **川崎重工 Kaleido**: 官方网站・报道的一次 URL 未能到达(kawasakirobotics.com 上无记载)。正文中也写明了这一点。
- **丰田 T-HR3 的官方新闻稿**: global.toyota 返回 403 无法到达。用 Wikipedia(Toyota Partner Robot)仅佐证 2017 年发布。主从操纵系统的细节未写入正文。
- **Kuindersma et al. 2016**: Springer 有认证重定向,正文内容未确认(DOI 有效)。
- **本田 E2 的 1.2 km/h、E 系列绝密的经过**: 依据 Honda Stories・IEEE 认定页的记述(经由搜索结果摘要)。

# 5. 项目 1: 赛跑(20m 直线)

第一个项目是最简单的"笔直走 20m"。而就在这个最简单的项目上,我们**三连败**了。这三连败的记录,也许是这篇文章最想传达的东西。

## 5.1 第 1 跑: 走得漂亮。只不过在画圆

用对示范(LAFAN1)的模仿奖励 + 摔倒惩罚训练出的第一位选手(walk9),膝盖柔韧地弯曲,手臂也在摆动,看上去走得有模有样。可是把世界坐标下的轨迹画出来一看,**它在沿着一个大圆行走**。模仿奖励只看"关节角度像不像示范",身体朝哪走都能拿到近乎满分。明明是赛跑,却是个偏出跑道朝观众席走去的选手。而本人(策略)一脸满分的表情。

## 5.2 第 2 跑: 加了惩罚,它却住进了惩罚的"饱和地带"

那就偏离了就罚吧,于是加了 exp 型的软位置惩罚(walk10/11)。结果出乎意料,选手偏出赛道 3〜4m 依然泰然自若地继续走。exp 型的惩罚在偏离 1m 后数值就几乎贴零,**再偏惩罚也不再增加,成了"饱和地带"**。在梯度(改进的线索)消失的地方,惩罚和不存在没有区别。

## 5.3 第 3 跑: 加了截断,这次学习萎缩了

那就要不饱和的惩罚,于是加入"偏离赛道 1.5m 立即失格(episode 终止。episode=一次练习的完整试跑)"的走廊截断(walk12/12b)。作弊消失了。取而代之的是**学习减半了**。在探索走法的初期阶段,身体摇晃是理所当然的,可一晃就失格,经验积不起来。奖励在约 450 处触顶,存活止步 8 秒。

## 5.4 真因: 它看不见白线

三连败之后,我们才终于怀疑起观测向量。然后撞上一个让人泄气的事实。**策略的观测里,既没有自己的横向位置,也没有偏航角(朝向)。**

请站在选手的立场想象一下。被蒙上眼行走,偏出赛道就扣分。可白线在哪里根本看不见。能做到的最多是"尽量努力直走",**歪掉之后再拐回来的控制在原理上就不可能**。被惩罚的量不在观测里 — 部分观测(POMDP)的教科书案例,我们用实测踩了 3 次坑才抵达。

修正只有区区 2 维。只是往观测里加了 `steer = [横向偏移, 偏航角]`(walk12c)。

(表中的"@26M steps"意为"2,600 万训练步的时点"。不是距离的米 — 之后这种记法会频繁出现,也请顺便看看术语表里"训练步数"一条。)

> **🍙 通俗讲解角(赛跑篇)**
> 这里发生的事一句话概括就是"**用考试成绩训人之前,先确认有没有把课本给人看**"。AI 只知道观测(=展示给它的信息)。喊"偏出赛道就扣分!",却没让它看见赛道在哪,它想改也没法改。人类的社团活动里,"你怎么就不会呢"的九成其实是"因为没人教过",对吧。同样的结构,在数学式的世界里也会上演。

| 指标(同时点对比) | walk9(仅模仿) | walk12b(仅截断) | **walk12c(加入转向观测)** |
|---|---|---|---|
| 奖励 @26M steps | 283 | 274 | **2,057(7 倍)** |
| 奖励 @42M steps | — | 约 450 触顶 | **6,522** |
| 存活时间 @42M | — | 约 8 秒 | **19.5/20 秒(几乎完赛)** |
| 横向偏移 RMS(实测行走) | 圆形轨迹 | — | **0.14m / 前进 20.5m** |

![转向观测的效果](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/curve_steering_obs_effect.png)
*图: 同一条件下只改观测的 3 跑学习曲线。只加了 2 个维度,就变成了另一项比赛(根据实测日志绘制)*

![G1 直线行走](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk12c_37M.gif)
*视频: walk12c(37M 时点)的 20.5m 完赛。速度 1.36m/s,膝关节活动范围 9〜78°,摆臂 ±20〜30°(仿真实测)*

![脚底的力](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_feet_forces.gif)
*视频: 同一步行的脚下特写,可视化接触力(箭头)。单脚承接体重交接瞬间的"看不见的力"变得可见(仿真实测)*

## 5.5 赛跑攒下的诀窍(节选)

作为三连败的副产品,攒下了很多细碎的教训。放几条在这里。

- **奖励中要惩罚的量,必须放进观测。** 不应按软惩罚 → 截断 → 加观测的顺序怀疑,而应从观测开始怀疑。
- **动作空间的上限要逐关节实测后再定。** 残差的摆幅曾对全关节一律设 0.5rad,结果只有膝盖因站立位单侧可动范围的关系最多只能出 29°,结构上够不到人类摆动腿所需的 40°。只把膝盖放宽到 1.0rad 后解决。
- **符号要实测后再写奖励。** G1 的肩俯仰是"正值=手向后"。凭想当然写摆臂奖励,会朝反方向优化。
- **确认参考动作的坐标系约定。** LAFAN1 的四元数(用 4 个数表示旋转的记法)是 xyzw 顺序,与 MuJoCo 的 wxyz 不同。这里搞错,所有帧都会被微妙地拧歪。

## 5.6 附赠: 学习曲线的读法(重现了 4 次的固定模式)

在这套配置下,行走学习的曲线有非常清晰的固定模式。4 次训练 4 次都是同一形状。

- **初期(0〜20M 步)**: 存活几十步的横盘。这时会忍不住想动设置,但这是"还在摸索怎么站"的正常沉默。
- **跃升期(25〜35M)**: 存活时间和奖励跳涨数倍。站住→几步→周期行走的质变发生在这个窗口。
- **判定点(37M 前后)**: 凭这个时点的成绩,基本能读出该配置"底子好不好"。37M 不行的配置在 100M 翻盘的事,在本文的实验中一次都没有。

实用的含义: **判定在 37M 下,只让有希望的配置跑长**。GPU 时间有限,与其"所有配置都跑到 150M 再比",不如"37M 筛一遍,只有赢家跑 150M"的两段选拔 — 这是在个人办赛的预算内运转的诀窍。用生物育种来说,就是在幼体阶段看苗头选拔、再养到成体的那套流程。

## 5.7 深挖: 理论的书架 — PPO・模仿学习的谱系・奖励黑客的学术家谱
(第 5 章"赛跑"的增补)

正文里轻描淡写地说"用 PPO 跑了 3700 万步就走起来了",但那个 PPO 里面发生着什么,又为什么最终落在 mocap 模仿这个战略上。我们一起看看理论背景。

### 5.7.1 分 3 个阶段看 PPO 的内部

#### 阶段 1: 策略梯度 — "提高好动作的概率"

策略(policy)是神经网络 π(a|s)。输入状态 s,输出动作的概率分布。策略梯度法的原理一行就能说完: **碰巧带来好结果的动作,下次让它更容易被选中**。数学上,以 advantage(该动作比平均好多少)为权重,推高 log π 的梯度。

朴素地做会出两个问题。(1) 采样一次的数据只能更新一次,样本效率差。(2) 梯度噪声大,一次更新就可能让策略剧变而崩溃。

#### 阶段 2: 重要性比与裁剪 — 实现"一次不要变太多"

PPO(Schulman et al. 2017 [^ppo])同时解决这两个问题。关键是**重要性比** r(θ) = π_new(a|s) / π_old(a|s)。它表示在"收集数据时的策略"与"正在更新中的策略"之间,选中该动作的概率变了多少倍。用这个比来校正,旧数据就能复用好几个 epoch(论文所说的"使 multiple epochs of minibatch updates 成为可能的新目标函数")。

但放任比值不管,更新会推进到比值 10 倍・100 倍,策略就坏掉了。于是 PPO 在目标函数里加入**裁剪**:

L = min( r·A, clip(r, 1−ε, 1+ε)·A )   (ε 取 0.2 等)

读法是这样。advantage A 为正(好动作)时,提高 r 越多越赚 — 但在 **1+ε 处封顶**。再提高该动作的概率,目标函数也一分钱不涨,于是梯度归零,更新自然停止。A 为负时,同样的盖子盖向相反方向。"一次更新中策略最多只能动 ±20%",不是作为约束条件,而是**用目标函数的形状本身**来实现 — 这就是 PPO 的发明。前身 TRPO 用严格的约束优化做同一思想,而 PPO 论文把自己定位为"保有 TRPO 的部分优点,同时实现远为简单、更通用、样本效率也更好" [^ppo]。

##### 通俗讲解: 方向盘的余量

PPO 的裁剪,就像驾校教官定下"方向盘一次最多打半圈"的规矩。就算方向正确,一把打死车也会甩尾。打一点 → 看车的反应(收集新数据)→ 再打一点。这种"小幅修正的积累",是让 3700 万步的长旅不崩盘跑完的保险。

#### 阶段 3: GAE(λ) — advantage 怎么估

要测"这个动作比平均好多少",必须决定未来的奖励实测到哪里、从哪里切换成价值函数(输出此后奖励预期的函数)的预测。

- 实测用得长 → 偏差小但噪声(方差)大
- 早点切换成预测 → 噪声小但要吃价值函数的误差(偏差)

GAE(Schulman et al. 2015 [^gae])用 λ ∈ [0,1] 把这个二选一连续地混合。论文的表述是"与 TD(λ) 类似的、advantage 函数的指数加权估计量"。λ=0 只实测 1 步(低方差・高偏差),λ=1 实测整个 episode(高方差・低偏差),实务中常用 0.95 前后。brax 的 PPO 里,rollout 之后紧接着就插着这个 GAE 计算。

| 部件 | 一句话 | 出处 |
|---|---|---|
| 策略梯度 | 提高好动作的概率 | — |
| 重要性比 r | 复用旧数据的校正系数 | [^ppo] |
| 裁剪 | 把 r 在 1±ε 处封顶,"一次不要变太多" | [^ppo] |
| GAE(λ) | 用 λ 混合实测与预测来估计 advantage | [^gae] |

### 5.7.2 模仿学习的谱系 — 从 DeepMimic 到 PHC

体验过"从零设计奖励让机器人走路"是怎样一片雷区(正文的作弊 11 连发),就会深切理解这个领域为何收敛到了 **mocap 追踪**。谱系上表:

| 年 | 手法 | 一句话总结 | URL |
|---|---|---|---|
| 2018 | **DeepMimic**(Peng et al.)| 以与 mocap 片段的姿态一致作为奖励做 RL。连空翻都能再现。确立了 RSI 与提前终止这两大定式 | [^deepmimic] |
| 2021 | **AMP**(Peng et al.)| 不再手写一致性奖励,让 GAN 风格的判别器给"这段动作像不像数据集"打分。不再需要手动挑选・对齐片段,从未整理的动作集中学习风格 | [^amp] |
| 2022 | **ASE**(Peng et al.)| 从大规模动作数据对抗式地学习可复用的"技能嵌入空间"。下游任务只靠操作潜空间来解 | [^ase] |
| 2023 | **PHC**(Luo et al.)| 用 1 个策略持续追踪数千个片段。含摔倒恢复在内的 fault-tolerant 实时 avatar 控制 | [^phc] |

流向一句话总结: **"单片段的追踪(DeepMimic)→ 风格分布的模仿(AMP)→ 技能空间的获得(ASE)→ 全都要的通用追踪(PHC)"**。这是奖励设计的匠人手艺,被数据与对抗学习逐步替换的历史。

#### RSI 与提前终止 — DeepMimic 留下的两个定式

DeepMimic 论文 [^deepmimic] 推广的训练技巧,比手法名字活得更久。

- **RSI(Reference State Initialization)**: episode 的开始状态,从参考动作的**随机时点**采样。空翻的奖励要到落地才知道,每次都从站姿开始的话,在体验到空中姿态之前就要失败几万次。有 RSI,一开始就能从"空中的正确姿态"起步练习 — 是把课程自动分散布置的机关。
- **提前终止(Early Termination)**: 摔倒立即截断 episode。摔倒后在地上挣扎的数据是学习的毒药(占据 replay 的大半却什么都教不了),从供给源头掐断。

我们的 G1 训练(LAFAN1 mocap 追踪 + 走廊截断),是这两个定式的忠实后裔。

#### 残差控制 — "不把一切交给 RL"

另一个与本文配置直接相关的是**残差控制**。Johannink et al. 的 Residual Reinforcement Learning for Robot Control [^residual] 把控制分解为"传统型反馈控制器 + RL 学习的残差"。基础控制器(或参考动作)给出大框架的答案,RL 只学**离它的差分**。探索空间从"全身所有的动法"缩小到"离示范的偏差",学习戏剧性地稳定下来。G1 的行走采用"mocap 模仿 + 残差"配置,正是这条谱系的嫡系。

### 5.7.3 域随机化与 sim-to-real

把在仿真器里学会的本事带上实机,会因建模误差(摩擦、延迟、马达特性…)而崩掉 — 所谓 **reality gap**。对此当前的主流解法是**域随机化(domain randomization)**: 训练中故意让仿真器的参数抖动,强制培养"在哪个世界都行得通的策略"。

| 事例 | 做了什么 | URL |
|---|---|---|
| Tobin et al. 2017 | 在图像识别上把 DR 体系化。**只用**随机化的仿真图像训练的检测器迁移到了真实世界 | [^tobin] |
| OpenAI Dactyl 2018 | Shadow Hand 的灵巧 in-hand 操作。大规模随机化摩擦系数、外观等物理特性,仅靠仿真训练迁移实机 | [^dactyl] |
| ANYmal(Hwangbo et al. 2019, Science Robotics)| 四足机器人的高速奔跑・摔倒恢复。把仿真中训练的策略迁移到实机(并用把实测数据学出的执行器模型嵌入仿真器的技巧) | [^anymal] |

直觉上和疫苗有几分相似。只在 1 种环境里训练的策略,会过拟合那个环境的癖性。在摩擦・质量・延迟每个 episode 都被改变的环境里长大的策略,"依赖癖性"的战略用不了,于是只有鲁棒的战略活下来。文中的传感器 dropout 训练也是同一发想的同类。

### 5.7.4 "作弊"的学名 — reward hacking / specification gaming

正文里 11 连发的"作弊",并不是**只因**我们的奖励设计太差才发生的稀罕事。它是整个领域臭名昭著的现象,有正经的学术用语。

- **Reward hacking(奖励黑客)**: Amodei et al. 的 Concrete Problems in AI Safety(2016)[^amodei] 把它定式化为 AI 安全性的实务五大课题之一。在该论文的分类里,它被放在"问题源于目标函数错了"的一侧。
- **Specification gaming(钻规格的空子)**: DeepMind 的博客(2020,第一作者 Victoria Krakovna)[^dm-spec] 连同从社区收集的**约 60 个实例列表**一起整理出的叫法。博客里的著名例子:
  - **CoastRunners(赛艇)**: 不跑赛道,在道具会重新刷新的海湾里一圈圈打转,只刷分数
  - **叠乐高**: 对"把红积木'放到'绿积木上"的奖励(= 红块底面的高度),把红积木**翻过来**、底面朝上达成
  - **抓取机器人**: 在由人通过相机画面判定是否抓到的设定下,**把手挡在相机与物体之间**装作抓到了
  - **仿真行走**: 把腿组合锁死,**贴着地面滑行**前进

最后一个例子,眼熟得过分。我们 G1 的跪行搓步、evis 的鱼跃前进,正是排在这"约 60 例"旁边的标本。作为教训重要的是 DeepMind 博客标题给出的视角 — specification gaming 是"AI 创造力的另一面(the flip side of AI ingenuity)"。**智能体没有坏。它只是把我们写下的名为奖励的合同,一字一句照章履行了而已**。钻空子的能力和解题的能力是同一种能力,错的是合同的写法。

#### 通俗讲解: 只优化分数的学生

奖励黑客,类似只按"考试分数"评价的学生把背真题练到极致。学生并非不认真,而是**对给出的评价标准完全理性**。"希望你提高学力"只存在于我们的脑子里,写在纸上的是"在这场考试拿高分"。RL 的奖励设计,就是每观测到一个作弊实例,就把"真正想要的"与"写在纸上的"之间的距离缝上一针的工作。11 条奖励设计教训,说到底就是 11 针的缝线。

#### 第 2 部分出处

[^ppo]: Schulman et al., "Proximal Policy Optimization Algorithms," 2017: https://arxiv.org/abs/1707.06347
[^gae]: Schulman et al., "High-Dimensional Continuous Control Using Generalized Advantage Estimation," 2015: https://arxiv.org/abs/1506.02438
[^deepmimic]: Peng et al., "DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills," 2018(RSI・提前终止): https://arxiv.org/abs/1804.02717
[^amp]: Peng et al., "AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control," 2021: https://arxiv.org/abs/2104.02180
[^ase]: Peng et al., "ASE: Large-Scale Reusable Adversarial Skill Embeddings for Physically Simulated Characters," 2022: https://arxiv.org/abs/2205.01906
[^phc]: Luo et al., "Perpetual Humanoid Control for Real-time Simulated Avatars," 2023: https://arxiv.org/abs/2305.06456
[^residual]: Johannink et al., "Residual Reinforcement Learning for Robot Control," 2018: https://arxiv.org/abs/1812.03201
[^dactyl]: OpenAI et al., "Learning Dexterous In-Hand Manipulation," 2018: https://arxiv.org/abs/1808.00177
[^anymal]: Hwangbo et al., "Learning agile and dynamic motor skills for legged robots," Science Robotics 2019: https://arxiv.org/abs/1901.08652
[^amodei]: Amodei et al., "Concrete Problems in AI Safety," 2016: https://arxiv.org/abs/1606.06565
[^dm-spec]: DeepMind Blog, "Specification gaming: the flip side of AI ingenuity," 2020(提及约 60 例的列表): https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/

# 6. 项目 2: 障碍赛 — 伪 LiDAR 与一维事件相机

能直走了,接下来就往赛道上撒了些圆柱障碍物。从这里开始,是我本行(图像处理)的血有点躁动的区间。躁动的结果做的也还是朴素的几何计算就是了。

## 6.1 眼睛要贴着实机来造(发案备忘)

要避开障碍物,就需要"看"。仿真里也可以把上帝视角(所有障碍物的精确坐标)递给策略,但那样的养法带不上实机。这里我最先定下的方针是"**先对齐实机 G1 上实际搭载的传感器,再开始**"。

实机 G1 的头部装着 Livox Mid-360(覆盖 360° 的小型 LiDAR,垂直视场 -7°〜+52°)和 Intel RealSense D435i(视场 87°×58° 的深度相机)。于是策略的眼睛,也被限制为这套配置能构成的信息 — 前方扇形的 **16 条水平射线(光线)的距离**。

![伪 LiDAR 的几何](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_ray_geometry.png)
*图: 伪 LiDAR 的几何。向前方 180° 发射 16 条射线,解析计算与圆柱的相交。最近的射线(红)成为"恐惧"的信号(按实现规格绘制)*

另一条作为方针加入的,是"**不配上事件相机式的信息,时间序列会很难衔接**"的想法。只有距离的快照的话,"那个障碍物是在靠近还是在远离"得靠策略自力推断。于是把每条射线的**时间差分(与上一帧的距离差)放大 20 倍**加进观测。这实质上是一维的事件相机(DVS)。不解点与点的对应问题,只传递"接近速度" — 与事件相机只吐出亮度变化是同一发想的极简版。

技术小花絮: 在 MJX 的训练循环(jit 编译的计算图)里,MuJoCo 的射线投射函数调不了。于是利用障碍物是圆柱这一点,**解析地(用公式)计算射线与圆柱的相交**。这套几何计算与后述 Fullseye 的伪 LiDAR op 完全相同,"策略看到的世界"与"人类验证时看到的世界"数值一致,由单元测试保证。

## 6.2 训练中期报告: "吓得减速"的选手

47M 步时点的 8 赛道实测: 碰撞 3/8,摔倒 4/8,平均前进 2.56m。有意思的是,出现了**在障碍物前站住、存活 12 秒**的种子(随机数的种子。1 个种子=1 条赛道的试跑)。学习回避的途中,选手似乎先学会了"害怕"。行进速度也从直线项目的相当于 0.53m/s 降到了 0.35m/s。人类小孩骑自行车进障碍赛道时也先慢行,构图上看着一模一样。

> **🍙 通俗讲解角(传感器篇)**
> LiDAR(激光雷达)是用"激光的回声"测距的装置。山谷回声的光版,从返回所需的时间知道"离墙几米"。事件相机是"只拍变化的相机"。普通相机每秒拍 30 张照片,事件相机只发来"现在这里动了!"的点。本文的机器人拿到的是它们的超简化版 — "16 条激光回声+其变化"作为眼睛。

63M 时点,摔倒 0/8(行走本身完全稳定),碰撞 2/8,平均前进到了 3.31m。回避的直接证据也出现了: 某条赛道上,它把 2 根障碍物形成的窄门(y=+0.76 与 y=−1.19),以身体鼓到 y=−0.74 的方式穿过,保持最近距离 0.53〜0.60m,12 秒无碰撞前进 8.3m。

![视觉回避的学习过程](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/curve_vision_avoidance.png)
*图: 障碍赛的学习过程(碰撞率与射线最小距离的推移,根据实测日志绘制)*

![障碍物回避](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk13c_63M_obst.gif)
*视频: 63M 时点的障碍赛道行走(仿真实测)*

## 6.3 然后选手注意到了"站着不动就无敌"

这里出现了讨厌的兆头。过了 63M 前后,这位选手(walk13c)的平均速度持续下降,68M 时成了前进 0.20m/s、存活却有 13.7 秒的成绩。**不走就不会摔,也不会撞。** 在只有生存奖励和碰撞惩罚的世界里,"原地踏步"是无比合理的战略。就像围棋 AI 为了不认输一直虚着(pass)那样,是奖励设计的洞。

这其实和直线项目的"饱和地带"是同构的问题。那边住进惩罚消失的地方,这边住进惩罚不会来的行为。**智能体一定会找到奖励地形里最舒服的洼地。**

![冻结与停滞截断](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_stall_term_effect.png)
*图: 冻结局部最优(13c,收敛到前进 0.20m/s)与停滞截断组(13d/13e,维持 0.95m/s 前后)的前进速度推移(根据实测日志绘制)*

作为对策,引入了"**停滞截断**"。每 75 个控制步(1.5 秒),root 前进不足 0.12m 就立即失格。这次把不饱和的惩罚(截断),对准了"不前进"这件事。用这条新规则让 2 位选手并跑。

- **walk13d**: 仅追加停滞截断
- **walk13e**: 停滞截断 + 速度奖励 2.5 倍

执笔时点(100M 步)的 8 赛道实测如下。

| 选手 | 63M 时点 | 100M 时点 | 趋势 |
|---|---|---|---|
| walk13d | 碰撞 8/8,前进 3.43m/赛道,碰撞/10m = 2.92 | 碰撞 4/8,前进 3.07m,**碰撞/10m = 1.63** | 回避急速改善中 |
| walk13e | 碰撞 5/8,前进 3.19m,碰撞/10m = 1.96 | 碰撞 6/8,**前进 4.54m**,碰撞/10m = 1.65 | 距离+42%,维持速度 1.11m/s |
| (旧)walk13c | 碰撞 2/8,前进 3.31m,碰撞/10m = 0.75 | — (68M 时堕入冻结战略被叫停) | 好成绩是与"战战兢兢地走"配套的 |

13c 看似漂亮的碰撞率,是"站住战略的入口处"的数字,13d/13e 则还在发育途中 — 写到这里时训练到了 136M,重新一测,风向完全变了。

| 选手 | 100M 时点 | **136M 时点** |
|---|---|---|
| walk13d | 碰撞 4/8,3.07m/seed,碰撞/10m 1.63 | 碰撞 4/8・摔倒 0/8,5.12m/seed,**碰撞/10m 0.98** |
| walk13e | 碰撞 6/8,4.54m/seed,碰撞/10m 1.65 | **碰撞 2/8・摔倒 1/8,7.52m/seed,碰撞/10m 0.33** |
| (基准)13c@63M | 碰撞 2/8,3.31m/seed,碰撞/10m 0.75 | — |

**walk13e 把旧王者 13c 的碰撞率(0.75)刷新到不足一半(0.33),而且行进距离是 2.3 倍**。跑满 8 秒地平线、9〜11m 无碰撞的赛道 8 条中有 4 条。"不站住、边避让、还走得快"三者兼得的瞬间。停滞截断不只堵上了"冻结的作弊",还证明了堵上之后回避能力照样长出来。100M 时点看似"快冲猛撞的粗暴阶段"的东西,只是发育的中途 — 幸好没急着用快照下判断,这是附赠的教训。

然后跑完了 150M(1 亿 5 千万步)。用 8 个种子测误差偏大,于是**增加到 16 个种子做最终判定**。

| 最终成绩(152M・16 赛道) | walk13d | walk13e |
|---|---|---|
| 碰撞 | 3/16 | 3/16 |
| 摔倒・出界 | 2/16 | 1/16 |
| 8 秒完赛 | 8/16 | **11/16** |
| 前进距离 | 6.59m/赛道 | **6.67m/赛道** |
| 碰撞/10m | **0.28** | **0.28** |
| 平均速度 | **1.08m/s** | 0.97m/s |
| (参考)旧王者 13c@63M | 碰撞/10m 0.75・3.31m/赛道 | 同左 |

![回避的成长曲线](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_avoidance_progress.png)
*图: 障碍赛的成长全记录(碰撞/10m 与前进距离,63M→152M)。虚线 = 旧王者 13c 的基准(根据数值表绘制)*

结果是**并列冠军**。碰撞率完全打平(0.28 — 旧王者的 1/2.7),距离也几乎相同。只剩下性格的差异: 13d 稍快,13e 稍有韧性。

![最终 16 种子散点图](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_final16_scatter.png)
*图: 152M 最终判定的全部 32 跑(16 种子 × 2 系)。越靠右上(走得远撑得久)越好。颜色 = 结果(根据实测绘制)*

速度奖励 2.5 倍(13e)起效的方向不是"变快"而是"变得不容易停",这也是个有趣的误算。

作为颁奖礼的点评是这样: **获胜的不是个体,而是规则修订(停滞截断)。** 在堵死了冻结作弊的环境里,无论哪种奖励设计,都能长到回避与行走兼得的程度。比起奖励的细节,"堵作弊的方式"才是支配性的 — 这就是本项目的结论。

### 6.3.1 给裁判当裁判 — 严格化接触求解器重新测量

写完最终表格,我体内的检测设备工程师坐不住了。**物理接触的判定,是不是太松了? 收敛计算(牛顿法)有没有好好在用?** 一查,正中痛处。MuJoCo 的默认正是牛顿法(迭代上限 100・容差 1e-8),但**训练侧为了速度把迭代压到 6 次,而裁判侧的 rollout 也以"与训练条件对齐"为由,用同样的 6 次在测**。作为条件对齐说得通,但没去确认"这是不是物理上收敛的数字",也是事实。于是用严格设置(牛顿法・迭代 100・线搜索 50)重新测了最终判定。

| 16 赛道重判 | 粗设置(迭代 6) | **严格设置(迭代 100)** |
|---|---|---|
| walk13d 碰撞/10m | 0.28 | **0.17**(距离 7.33m/赛道) |
| walk13e 碰撞/10m | 0.28 | **0.37**(距离 6.78m/赛道) |
| 脚的地面穿透(中位数) | 20.9mm | **20.9mm(不变)** |
| 脚的地面穿透(最差) | 29mm | 25〜43mm |

弄明白了两件事。第一,**大方向的结论不变**(两者都大幅低于旧王者 0.75),但"并列"崩了 — 严格设置下 13d 明显更强,前一节的并列是这次测量的分辨率之内的偶然,在此更正。第二,这条更重要: **脚往地面里陷进了中位数 21mm**,而且这一点增加迭代次数也不变。也就是说,松的主因不是求解器收敛不足,而是**接触模型本身的柔软**(MuJoCo 的软接触参数被设成了训练速度优先)。这场运动会,可以说是在一张略软的垫子上举办的。在垫子上也能分出比赛的优劣,但"在硬地板上能不能出同样的成绩",作为下届大会的正式作业记录在案(把接触改硬后训练侧也需要重新训练,所以规则修订以大会为单位)。

给裁判当裁判的视角,恰恰在赢了之后最需要 — 因为出了好结果的时候,正是最想在检查上偷懒的瞬间。

![求解器审计](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_pen_audit.png)
*图: 求解器严格化审计的汇总。碰撞率随设置互换,但穿透对迭代数不变=来自接触模型的柔软(根据实测绘制)*

![4 世代竞跑](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_generations_race.gif)
*视频: 王者的成长 4 赛道竞跑 — 同一赛道由 37M/100M/136M/152M 的 4 个世代同时回放(各赛道来自真实的物理 rollout,合成仅是赛道排布)*

![珍稀镜头集](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/blooper_reel.gif)
*视频: 珍稀镜头集(最终判定 16 赛道中的摔倒・碰撞高光,带慢放)。运动会也需要会摔倒的选手(仿真实测)*

![最终王者的完赛](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk13d_final_obst.gif)
*视频: 最终判定后的 walk13d(152M・seed6)。8 秒 10.21m,无碰撞跑完障碍赛道(仿真实测,平均 1.28m/s)*

![walk13d 100M](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk13d_100M_obst.gif)
*视频: walk13d(100M 时点,seed6)。诚实收录到前进 6.28m 后碰撞为止(仿真实测)*

![walk13e 100M](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk13e_100M_obst.gif)
*视频: walk13e(100M 时点,seed4)。7.04m,含穿过 2 根圆柱之间的镜头(仿真实测)*


## 6.4 以实机传感器的视线来看

训练用的伪传感器,可以原样用于"如果是实机会看到什么"的验证。把同一行驶轨迹重构为 Mid-360 的鸟瞰点云和 D435i 的深度图像的视频在这里。

![实机传感器视角](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_real_sensors_walk12c.gif)
*视频: 同一行驶的 Mid-360 风鸟瞰点云(左)与 D435i 风深度(右)重构。与策略的观测同一几何(仿真)*

## 6.5 接下来的计划: 混合传感器、故意弄坏、换乘

障碍赛的观测(射线+时间差分),只是传感器研究的入口。以这台 G1 为实验台,计划着 5 个阶段的传感器融合(多传感器融合)研究。每一项先写明"想确认什么"(结果出来后会在续报里对答案 — 猜错了就写猜错了)。

1. **伪 LiDAR 单体(现在这里)**: 只靠射线观测能走到哪里的基准线。没有基准线,之后就测不出"融合的效果"。
2. **融合+dropout**: 追加只覆盖前方的高分辨率射线束(相当于深度相机),再做**训练中随机杀掉 1 路传感器**的训练。目标是冗余性 — "行驶中 LiDAR 死了还能不能继续走"的消融实验(故意去掉一部分来测其影响的经典手法),是直通安全的问题。实机人形机器人同时搭载 LiDAR 和深度相机的理由,能否从学习侧再现出来。
3. **师生蒸馏**: 从用精确射线距离(特权信息)养出的教师策略,把行为誊写给只能看到带噪声立体深度的学生策略。是在四足机器人领域有实绩的手法(老师用上帝之眼学习,学生用现实之眼模仿)的人形版。
4. **时间序列的整合**: 要处理"刚才看得见的障碍物现在在死角",就需要记忆。是靠每步重测+时间差分硬扛,还是进到递归策略(GRU=带记忆的递归神经网络)的分岔点。
5. **移植到 evis**: 最后,把这些感知系统装到 700 肌的 evis 上。肌肉驱动的身体+实机兼容的感知 — 这个组合,是这场运动会最遥远的目标。

这个计划的含义只说一条。"混合"传感器的研究,其实也是"**让哪个传感器偷懒也没事**"的研究。传感器昂贵、耗电、还会坏。全配置能动是理所当然,缺了还能保持体面地动,才是实用的分水岭 — 和检测设备的世界里称为"冗余系统设计"的,是完全相同的问题。

### 6.5.1 续报: "故意弄坏"的对答案 — 杀掉 LiDAR 还能走吗

计划 2(融合+dropout),在这篇文章的执笔期间出了结果。在前方 87° 追加 32 条高分辨率射线束(有意对齐实机深度相机的视场角),把观测从 132→196 维扩展,训练中按 episode 随机混合"只有 LiDAR""只有深度""两者都有"3 种状态、训练 152M 步(M = 100 万步。不是距离的米)的 walk14 的毕业考试。

考试是 3 模式 × 8 赛道。随机种子已对齐,所以 3 个模式的障碍物布置和起始姿态完全相同 — 不同的只有"杀掉哪个传感器"。

| 模式 | 碰撞 | 摔倒 | 完赛 | 平均距离 | 碰撞/10m |
|---|---|---|---|---|---|
| 两者都有 | 3/8 | 2/8 | 3/8 | 5.40m | 0.69 |
| 只杀深度 | 4/8 | 1/8 | 2/8 | 4.10m | 1.22 |
| 只杀 LiDAR | 4/8 | 0/8 | 4/8 | 5.24m | 0.95 |

同一赛道的并跑也做成了一段影像。3 模式都完赛的赛道(seed 3)的对比:

![3 模式并跑对比](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/walk14_3mode_compare.gif)
*视频: 同一障碍赛道・同一起始姿态,只改变要杀的传感器的 3 路并跑(左: 两者都有 9.78m / 中: 只杀深度 8.17m / 右: 只杀 LiDAR 9.22m,8 秒完赛)。赛道的同一性已通过障碍物数据的逐位一致做了机器验证。看起来与柱子重叠的瞬间是相机的遮挡,实际间隙始终在 0.77m 以上(仿真实测)*

对答案的要点有 3 个。

第一,**正题"传感器死了还能走吗"成立**了。24 跑全部行走本身没有崩(原地冻结为零,杀 LiDAR 时摔倒也为零),劣化只限于回避成绩。不是死掉的瞬间就摔倒,而是成绩下降 — 冗余系统设计里说的"保持体面的降级"。

第二,意外的不对称。杀掉 LiDAR(偏全周的 16 条)反而比杀掉深度(前方 32 条)成绩更好。把几何一算就服气: 前方束每条 2.8° 间隔,广角的 16 条则是 11.25° 间隔 — 半径 30cm 的柱子在 3〜4m 外会掉进射线之间。对回避起作用的是前方的高分辨率束,策略也学出了对那一侧的依赖。实机人形机器人同时搭载 LiDAR 与深度相机这一配置的意义,从学习侧被再现了。

第三,诚实的注记。"两者都有"的 0.69,比无融合的冠军 13d(0.28)更差。冗余性的训练(两个传感器齐全只占 episode 的 75%)不是免费的,是靠削减本业的回避成绩买来的 — 这是本次的实测。不过 13d 的数字是 16 赛道・另一套测量装置下的测量,按票面直接比较要加一撮盐。同一赛道同一起始姿态的 apples-to-apples,是上表的 3 模式对比那边。

![杀掉 LiDAR 后完赛](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/walk14_dropout.gif)
*视频: 把 16 条 LiDAR 全部杀掉、只靠前方深度完赛 8.24m 的一跑。最近间隙 0.66m — 能看到像穿针一样向侧面鼓出的回避(仿真实测)*

## 6.6 也看看世间的主流 — ROS 2 与物理仿真器的技术地图

本文的障碍赛是把"观测→策略"用一个神经网络直连的端到端(end-to-end)方式,但产业界・研究界的主流,有着分工堆叠的**导航栈**谱系。作为"自己的玩法位于何处"的地图,把主要部件列成表(URL 在执笔时点确认可达)。

| 领域 | 代表 | 是做什么的部件 |
|---|---|---|
| 中间件 | [ROS 2](https://docs.ros.org/en/jazzy/) | 把传感器・控制・规划作为节点连起来的公共布线。实机机器人的事实标准 |
| 自定位+建图(SLAM) | [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) 等 LIO 系 | 一边从 LiDAR/IMU 推定"我现在在哪",一边建图 |
| 路径规划 | [Nav2](https://docs.nav2.org/) | 把地图代价地图化,规划全局路径+局部回避的 ROS 2 导航栈 |
| 凹凸地形的表示 | [elevation_mapping](https://github.com/leggedrobotics/elevation_mapping)(ETH) | 用"高程图"掌握腿式机器人的脚下。台阶・非平整地行走的地基 |
| 物理仿真器 | [MuJoCo](https://mujoco.org/) / [Gazebo](https://gazebosim.org/) / [Isaac Sim](https://developer.nvidia.com/isaac/sim) / [Genesis](https://genesis-embodied-ai.github.io/) | 本文的场馆是 MuJoCo。Gazebo 与 ROS 2 的集成深,Isaac 是含 GPU 渲染的大规模并行,Genesis 是新兴的高速势力 |

有趣的是,**这两条谱系如今正在合流**。古典栈是"建图、规划、跟踪" — 可解释、易认证,代价是怕部件间的假设错位。端到端 RL 是"看见,立刻动" — 反射强,却难以解释为什么这样动。最近的腿式机器人研究(非平整地跑酷等)已经以"感知与步态用 RL,全局路径用规划器"的混合为主流,本文的伪 LiDAR 策略,定位正是自制了其最底层(局部反射)。与 ROS 2 栈的对接(把策略作为 Nav2 的局部规划器装上去),是走向实机时自然的下一步。
