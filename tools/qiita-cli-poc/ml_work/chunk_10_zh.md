#### domain(2 个 op)

| op | 说明 |
|---|---|
| `it_crop_domain` | domain op(HALCON: crop_domain) |
| `it_full_domain` | domain op(HALCON: -) |

#### matching(2 个 op)

| op | 说明 |
|---|---|
| `ncc_locate` | matching op(HALCON: find_ncc_model) |
| `shape_locate` | matching op(HALCON: find_shape_model) |

#### noise(2 个 op)

| op | 说明 |
|---|---|
| `add_noise_distribution` | noise op(HALCON: add_noise_distribution) |
| `add_noise_white` | noise op(HALCON: add_noise_white) |

#### Legacy(1 个 op)

| op | 说明 |
|---|---|
| `distance_funct_1d` | 两个函数之间的距离(max=上限, mean=平均、distance_funct_1d)。 |

#### barcode(1 个 op)

| op | 说明 |
|---|---|
| `decode_barcode` | barcode op(HALCON: find_bar_code) |

#### classification(1 个 op)

| op | 说明 |
|---|---|
| `classify_shape` | classification op(HALCON: -) |

#### filter(1 个 op)

| op | 说明 |
|---|---|
| `Bilateral` | 保边平滑(cv2.bilateralFilter,缺失时用 numpy 实现)(filter.Bilateral)。  [backend=opencv] |

#### filtering(1 个 op)

| op | 说明 |
|---|---|
| `tf_gradient_domain_reintegrate` | filtering op(HALCON: -) |

#### intensity-transform(1 个 op)

| op | 说明 |
|---|---|
| `xmh_soft` | intensity-transform op(HALCON: -) |

#### misc(1 个 op)

| op | 说明 |
|---|---|
| `identity` | misc op(HALCON: copy_image) |

#### morphology/markers(1 个 op)

| op | 说明 |
|---|---|
| `xmh_regmin` | morphology/markers op(HALCON: -) |

#### region-morphology(1 个 op)

| op | 说明 |
|---|---|
| `xmh_majority` | region-morphology op(HALCON: -) |

#### region-transform(1 个 op)

| op | 说明 |
|---|---|
| `xmh_bwperim` | region-transform op(HALCON: -) |

#### self-similarity(1 个 op)

| op | 说明 |
|---|---|
| `xmh_selfmatch` | self-similarity op(HALCON: -) |

#### texture-feature(1 个 op)

| op | 说明 |
|---|---|
| `xmh_pftas` | texture-feature op(HALCON: -) |

#### texture/shape-feature(1 个 op)

| op | 说明 |
|---|---|
| `xmh_zernike` | texture/shape-feature op(HALCON: -) |

## 附录 G:未来资料集 — 传感、宇宙、学会、竞赛(URL 已确认实际存在)

这是第 13 章的资料篇。列出的 URL 全部是在撰稿时确认过可以访问的(无法确认的一律没有收录)。如果链接失效,请用站点名称搜索。

### A. 传感技术的最前沿

#### A-1. 事件相机 / 神经形态视觉

**厉害在哪(3 行)**
- 像人类视网膜一样,只把"发生变化的像素"异步发送出去的相机。时间分辨率达微秒量级,动态范围约 140 dB(普通相机约 60 dB),几乎没有运动模糊(出自 [Gallego et al. survey](https://arxiv.org/abs/1904.08405))。
- 研究成果已经波及在无人机竞速中战胜人类世界冠军的自主无人机(UZH/ETH 的 Scaramuzza 实验室),以及 NASA 火星直升机的视觉系统算法。
- 通过 Sony 与初创公司 Prophesee 的合作,4.86 µm 像素的堆栈式事件传感器(IMX636/637)实现量产,从"实验室里的稀罕物"变成了"买得到的零件"。

| 项目 | 内容 | URL |
|---|---|---|
| 代表论文 | Gallego et al., "Event-based Vision: A Survey", IEEE TPAMI 44(1), 2022(arXiv 2019) | https://arxiv.org/abs/1904.08405 |
| 代表专利 | US10498977B2 "Event-based vision sensor"(Samsung, 2019 授权) | https://patents.google.com/patent/US10498977B2/en |
| 产品一手信息 | Sony 堆栈式事件传感器 IMX636/IMX637 新闻稿(2021) | https://www.sony-semicon.com/en/news/2021/2021090901.html |
| 产品一手信息 | Prophesee × Sony IMX636 / 评估套件 EVK4 | https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/ / https://www.prophesee.ai/event-camera-evk4/ |
| 研究室 | Robotics and Perception Group(UZH & ETH Zurich,Davide Scaramuzza 教授) | https://rpg.ifi.uzh.ch/ (个人页面: https://rpg.ifi.uzh.ch/people_scaramuzza.html ) |
| 研究室 GitHub | uzh-rpg(公开了 ESIM 等大量项目) | https://github.com/uzh-rpg |
| 公开数据集 | UZH-FPV 无人机竞速数据集(事件+IMU+激光真值) | https://fpv.ifi.uzh.ch/ |
| 模拟器 | ESIM: an Open Event Camera Simulator(CoRL 2018) | https://github.com/uzh-rpg/rpg_esim |
| 模拟器 | v2e: 普通视频→逼真 DVS 事件流转换(CVPRW 2021 Best Paper) | https://github.com/SensorsINI/v2e (解说: https://sites.google.com/view/video2events/home ) |
| 视频 | UZH RPG 官方 YouTube(大量自主无人机、事件相机演示) | https://www.youtube.com/user/ailabRPG |

#### A-2. 量子传感(NV 色心磁测量、量子惯性导航)

**厉害在哪(3 行)**
- 钻石中的一个原子缺陷(NV 色心)就能成为"量子罗盘",在常温下测到细胞尺度的磁场。量子传感的标准教科书级综述是 [Degen–Reinhard–Cappellaro (Rev. Mod. Phys. 2017)](https://dspace.mit.edu/bitstream/handle/1721.1/124553/RevModPhys.89.035002.pdf)。
- 让冷却原子作为"波"发生干涉的原子干涉仪,是在 GPS 不可用的地方也不会迷失位置的惯性导航的头号种子。美军空天飞机 X-37B 的第 8 次飞行计划在轨测试量子惯性传感器([The Conversation, 2025](https://theconversation.com/quantum-alternative-to-gps-navigation-will-be-tested-on-us-military-spaceplane-262967))。
- MIT 演示了 NV 色心与 CMOS 芯片的集成(片上量子传感器),"把量子传感器变成普通半导体零件"的潮流正在进行中([MIT News, 2019](https://news.mit.edu/2019/quantum-sensing-chip-0925))。

| 项目 | 内容 | URL |
|---|---|---|
| 代表论文 | Degen, Reinhard, Cappellaro, "Quantum sensing", Rev. Mod. Phys. 89, 035002 (2017) | https://dspace.mit.edu/bitstream/handle/1721.1/124553/RevModPhys.89.035002.pdf (DOI: 10.1103/RevModPhys.89.035002) |
| 代表综述 | 基于 BEC 的量子惯性导航展望(Applied Physics Reviews, 2025) | https://pubs.aip.org/aip/apr/article/12/3/031306/3351228/Developments-for-quantum-inertial-navigation |
| 代表专利 | US12424810B1 "Compact atom interferometry inertial navigation sensors with tailored diffractive optics"(Sandia, 2025) | https://patents.google.com/patent/US12424810B1/en |
| 代表专利 | US7317184B2 "Kinematic sensors employing atom interferometer phases"(2008) | https://patents.google.com/patent/US7317184B2/en |
| 研究机构 | Sandia National Laboratories – Atom Interferometry | https://www.sandia.gov/quantum/atom-interferometry/ |
| 研究机构 | QuTech(TU Delft + TNO。用 NV 色心完成了量子网络的多项世界首次演示) | https://qutech.nl/ |
| 研究室(日本国内) | 东京科学大学(原东工大)岩崎研 – 固态量子传感器 | http://dia.pe.titech.ac.jp/en/solid-quantum-sensors/ |
| 解说文章 | MIT Technology Review「量子导航能否解决 GPS 干扰问题」(2025-12) | https://www.technologyreview.com/2025/12/16/1129887/quantum-navigation-militarys-gps-jamming-problem/ |
| 在家入口 | QuTiP: 开放量子系统动力学 OSS 模拟器(Python) | https://qutip.org/ |

#### A-3. 高光谱、偏振成像

**厉害在哪(3 行)**
- 给每个像素都附上"分光光谱"的图像(高光谱立方体)拍摄技术。在人眼看来颜色相同的东西,通过"光谱指纹"就能分辨出材质、水分、新鲜度、病变。
- 应用正扩展到农业(作物胁迫、杂草判别)、食品检测、癌症检出与术中成像、矿物勘探、回收分拣([Heliyon 2024 综述](https://www.sciencedirect.com/science/article/pii/S2405844024092399))。
- 在医疗领域,偏振×高光谱融合(PHSI)、高光谱内窥镜、AR 集成等是最前线([2025 医疗 HSI 综述](https://pmc.ncbi.nlm.nih.gov/articles/PMC13003176/))。

| 项目 | 内容 | URL |
|---|---|---|
| 代表综述 | "Hyperspectral imaging and its applications: A review", Heliyon (2024) | https://www.sciencedirect.com/science/article/pii/S2405844024092399 |
| 代表综述 | "Modern Trends and Recent Applications of Hyperspectral Imaging: A Review", Technologies (2025) | https://www.mdpi.com/2227-7080/13/5/170 |
| 医疗综述 | Medical hyperspectral imaging: updated review(偏振 HSI、内窥镜、AR 集成) | https://pmc.ncbi.nlm.nih.gov/articles/PMC13003176/ |

#### A-4. 触觉皮肤、电子皮肤

**厉害在哪(3 行)**
- MIT 的 GelSight 仅靠"用相机观察凝胶的形变",就实现了空间分辨率超过人类指尖的触觉。如今已由 GelSight 公司产品化,装上了机器人的指尖([MIT News](https://news.mit.edu/2017/gelsight-robots-sense-touch-0605))。
- 斯坦福 Bao 实验室的电子皮肤,从材料化学层面做出了可拉伸、可自愈、能区分压力与剪切力的特性。目标是把"触觉"还给假肢。
- 触觉是视觉的"最后一英里"。抓取瞬间的打滑、软硬、摩擦是相机看不见的,已成为 Physical AI 的下一个主战场。

| 项目 | 内容 | URL |
|---|---|---|
| 代表论文 | Yuan, Dong, Adelson, "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force", Sensors 17(12):2762 (2017) | https://www.mdpi.com/1424-8220/17/12/2762 |
| 代表专利 | WO2023081342A1 "Four-dimensional tactile sensing system, device, and method"(2023) | https://patents.google.com/patent/WO2023081342A1/en |
| 研究室 | MIT CSAIL(Adelson 系)GelSight Wedge 项目 | https://gelsight.csail.mit.edu/wedge/ |
| 研究室 | Stanford Bao Group(电子皮肤、可拉伸电子学) | https://baogroup.stanford.edu/ |
| 企业 | GelSight, Inc.(GelSight Mini 等) | https://www.gelsight.com/gelsightmini/ |
| 解说 | MIT News "Giving robots a sense of touch" (2017) | https://news.mit.edu/2017/gelsight-robots-sense-touch-0605 |

#### A-5. 神经接口式传感(肌电 / EIT)— 简单提一下

**厉害在哪(3 行)**
- Meta(原 CTRL-labs)的腕带只靠手腕的表面肌电(sEMG),无需针对个人校准就能解码手指的细微动作。可以以每分钟约 20.9 个词的速度输入空中手写文字(刊于 Nature 2025)。
- "不往脑子里插电极"的非侵入式神经运动接口,已经走到了瞄准键盘、鼠标之后下一代标准输入的位置。
- 还有把电气阻抗断层成像(EIT)做成手环的研究,有低成本、低功耗(约 50 mW)下手势识别精度 93% 的报告([Biosensors 2026](https://www.mdpi.com/2079-6374/16/4/200))。

| 项目 | 内容 | URL |
|---|---|---|
| 代表论文 | "A generic non-invasive neuromotor interface for human-computer interaction", Nature 645 (2025) | https://www.nature.com/articles/s41586-025-09255-w |
| 一手信息 | Meta EMG Wristband 官方页面 | https://www.meta.com/emerging-tech/emg-wearable-technology/ |
| 相关论文 | 基于 EIT 的鲁棒手势识别(Biosensors, 2026) | https://www.mdpi.com/2079-6374/16/4/200 |

---

### B. 宇宙开发

#### B-1. 在轨服务、太空垃圾捕获

**厉害在哪(3 行)**
- Astroscale 的 ADRAS-J(JAXA CRD2 第 I 阶段)在 2024 年自主接近一个"完全不具备协作功能"的约 3 吨火箭上面级至 15 m,并成功环绕观测。属世界首创级的成绩([Astroscale 官方](https://www.astroscale.com/en/news/astroscales-adras-j-achieves-historic-15-meter-approach-to-space-debris))。
- 接下来的 ADRAS-J2(CRD2 第 II 阶段)计划用机械臂实际捕获该垃圾并使其降轨。ESA × ClearSpace 的 ClearSpace-1 也在准备用 4 条机械臂进行捕获验证。
- "安全接近并抓住翻滚的非合作物体" = 自由漂浮物体的交会与捕获,是 GNC(制导、导航、控制)、视觉、接触力学的综合格斗。仿真正是这里的主战场。

| 项目 | 内容 | URL |
|---|---|---|
| 官方任务 | Astroscale ADRAS-J 任务页面 | https://www.astroscale.com/en/missions/adras-j |
| 官方项目 | JAXA CRD2(商业太空垃圾清除验证) | https://www.kenkai.jaxa.jp/eng/crd2/index.html |
| 一手信息 | JAXA 新闻稿: ADRAS-J 的垃圾环绕观测图像(2024-07) | https://global.jaxa.jp/press/2024/07/20240730-1_e.html |
| 专利(解说) | Astroscale 专利 US12,479,603 B2「翻滚物体的捕获方法」官方解说 | https://www.astroscale.com/en/news/astroscale-patent-advances-docking-and-servicing-of-tumbling-satellites |
| 产品 | Astroscale 对接板(用于磁捕获的"卫星拖车钩") | https://www.astroscale.com/en/docking-plate |
| 解说文章 | MIT Technology Review: 世界首个垃圾清除任务启动(2024) | https://www.technologyreview.com/2024/02/27/1089065/first-mission-dead-rocket/ |
| 带视频的报道 | ADRAS-J 的绕飞影像(Space.com) | https://www.space.com/astroscale-debris-removal-adras-j-video |

※ ClearSpace 公司官网因 URL 未能确认而未收录(ClearSpace-1 的概况在上述 Space.com / MIT Tech Review 文章内有提及)。

#### B-2. 月面机器人

**厉害在哪(3 行)**
- JAXA × 丰田的载人加压月球车「LUNAR CRUISER」是靠氢燃料电池行驶的"月面房车"。有两辆小巴那么大,不穿宇航服也能乘坐([丰田官方](https://global.toyota/en/mobility/technology/lunarcruiser/))。
- NASA JPL 的 CADRE 是自主协作验证项目: 3 台行李箱大小的月球车自己选出"队长",分工协作对月面做 3D 测绘。地球那边只下达"探索这片区域"的目标([JPL 官方](https://www.jpl.nasa.gov/missions/cadre/))。
- 另一方面,NASA 的水冰勘探月球车 VIPER 于 2024 年被取消(已投入约 4.5 亿美元)。也想诚实地告诉大家: 最前沿并不是"全部成功的故事"。

| 项目 | 内容 | URL |
|---|---|---|
| 官方 | 丰田 LUNAR CRUISER 官方页面 | https://global.toyota/en/mobility/technology/lunarcruiser/ |
| 官方 | NASA JPL CADRE 任务页面 | https://www.jpl.nasa.gov/missions/cadre/ |
| 一手信息 | NASA: CADRE 月球车整装待发奔赴月球(计划 2026 年随 IM-3 抵达) | https://www.nasa.gov/missions/tech-demonstration/cadre/nasas-mini-rover-team-is-packed-for-lunar-journey/ |
| 企业 | ispace(HAKUTO-R 计划) | https://www.ispace-inc.com/aboutus |
| 报道 | VIPER 计划取消的来龙去脉(Spaceflight Now, 2024) | https://spaceflightnow.com/2024/07/18/nasa-cancels-half-billion-dollar-water-ice-seeking-moon-rover/ |
| 日本国内 | 东北大学牵头月面基础设施大型项目(2026) | https://www.tohoku.ac.jp/en/news/university_news/selected_to_lead_landmark_lunar_infrastructure_project.html |

#### B-3. 在轨制造、太空建筑

**厉害在哪(3 行)**
- Varda Space 瞄准只有在失重环境下才能制成的"更完美的晶体",成功在轨道上制造抗病毒药 Ritonavir 的晶体并用返回舱带回地面(2024 年 W-1 任务)。返回舱飞行已推进到第 6 次。
- 微重力环境没有对流也没有沉降,被视为蛋白质晶体、药品、特种光纤的理想制造环境,Redwire 还成立了太空制药专业子公司 SpaceMD([CNBC, 2026](https://www.cnbc.com/2026/06/09/space-race-pharma-spacex-varda-redwire-drug-development-orbit.html))。
- "把工厂发射上天,只让产品以 25 马赫带回来"这一产业结构本身就是全新的。再入舱的气动、热防护也是一大坨仿真。

| 项目 | 内容 | URL |
|---|---|---|
| 官方 | Varda W-Series 平台(在轨制造+再入) | https://www.varda.com/platform |
| 官方 | Redwire(太空基础设施+太空制药 SpaceMD) | https://rdw.com/ |
| 报道 | Varda 返回舱载着太空制造的药品归来(Space.com, 2024) | https://www.space.com/varda-in-space-manufacturing-capsule-landing-success |
| 报道 | 制药业为何奔向 LEO(CNBC, 2026-06) | https://www.cnbc.com/2026/06/09/space-race-pharma-spacex-varda-redwire-drug-development-orbit.html |

#### B-4. 宇宙用模拟器 OSS(全部免费,家用 PC 装得下)

| 工具 | 能做什么 | URL |
|---|---|---|
| NASA GMAT | 任务设计、轨道设计的正规派(NASA 实务中也在用)。GUI+脚本 | https://sourceforge.net/projects/gmat/ |
| Basilisk | 把航天器的姿态、轨道乃至飞行软件模块化地集成仿真(科罗拉多大学 AVS Lab) | https://avslab.github.io/basilisk/ |
| 42 (NASA GSFC) | 多航天器的姿态、轨道动力学。也可用于交会、编队飞行研究 | https://github.com/ericstoneking/42 |
| poliastro | 用 Python 做轨道力学。教育、原型开发的最佳入口 | https://github.com/poliastro/poliastro |
| Kerbal Space Program | 虽是游戏,却是建立轨道力学直觉的经典教材(还有教育版 KerbalEdu) | https://www.kerbalspaceprogram.com/ |

#### B-5. 用旋翼飞越行星 — Ingenuity 的遗产与 Dragonfly

**厉害在哪(3 行)**
- 火星直升机 Ingenuity 本是验证"能否在大气密度只有地球 1% 的天空飞行"的实验机,原计划飞 5 次,结果飞了 72 次,2024 年退役([JPL 官方](https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/))。这个花费 8,500 万美元的技术验证改变了行星探索的形态。
- 后继者 Dragonfly 是送往土星卫星泰坦的核动力 8 旋翼机(汽车大小)。计划 2028 年 7 月发射,从空中探寻生命的化学起源([JHUAPL 官方](https://dragonfly.jhuapl.edu/))。
- 因为"飞行地点的大气、重力与地球不同",设计的主角是彻底的仿真与地面试验。旋翼气动力学用家里的 CFD(用计算机求解流动的数值流体力学)/物理引擎也能站上入口。

| 项目 | 内容 | URL |
|---|---|---|
| 官方 | Dragonfly 任务(JHU APL) | https://dragonfly.jhuapl.edu/ (别馆: https://www.jhuapl.edu/destinations/missions/dragonfly ) |
| 官方图库 | Dragonfly Gallery(想象图、试验影像) | https://dragonfly.jhuapl.edu/Gallery/ |
| 官方 | NASA Ingenuity 任务页面 | https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/ |
| 一手信息 | JPL: Ingenuity 任务结束发布(72 次飞行) | https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ |

---

### C. 用仿真在"家里复现"最前沿的例子

"就算没有上亿日元级的实验装置,物理定律是可以下载的" —— 这是本章想传达的信息。以下全部是免费 OSS。

| 最前沿主题 | 家用 PC + OSS 的入口 | URL |
|---|---|---|
| 事件相机 | 用 **v2e** 把手头的视频转换成事件流,体验"视网膜眼中的世界"。硬核派可用 **ESIM** 从 3D 场景生成事件 | https://github.com/SensorsINI/v2e / https://github.com/uzh-rpg/rpg_esim |
| 太空垃圾捕获、自由漂浮物体 | 用 **MuJoCo** 写一个零重力+带机械臂卫星的 MJCF,对翻滚物体的捕获做物理仿真(官方机器人模型集 Menagerie 是出发点) | https://github.com/google-deepmind/mujoco / https://github.com/google-deepmind/mujoco_menagerie |
| 轨道规划、任务设计 | 用 **GMAT** 搭一条地月转移轨道,用 **poliastro**(Python)几十行算出霍曼转移 | https://sourceforge.net/projects/gmat/ / https://github.com/poliastro/poliastro |
| 航天器姿态控制 | 用 **Basilisk** 或 **42** 仿真反作用轮控制、编队飞行 | https://avslab.github.io/basilisk/ / https://github.com/ericstoneking/42 |
| 月面巡视器、步行机器人的 RL | 用 **Gymnasium** + **MuJoCo Playground**(GPU 加速)做强化学习。低重力只需改 XML 里 gravity 一行就变成月球 | https://github.com/Farama-Foundation/Gymnasium / https://github.com/google-deepmind/mujoco_playground |
| 量子传感 | 用 **QuTiP** 对自旋的 Rabi 振荡、Ramsey 干涉(正是 NV 色心测量的原理)做数值实验 | https://qutip.org/ |
| 轨道力学的直觉 | 用 **Kerbal Space Program** 用身体记住"重力转弯""转移轨道"(教育名额) | https://www.kerbalspaceprogram.com/ |

---

### D. 看了能获得刺激的资料

#### D-1. 看了能获得刺激的官方图库、视频

| 来源 | 内容 | URL |
|---|---|---|
| NASA Image and Video Library | 横跨 14 万件以上的图像、视频、音频检索 | https://images.nasa.gov/ |
| NASA Galleries | 按任务分类的图库入口 | https://www.nasa.gov/gallery/ |
| JAXA 数字档案馆 | JAXA 的照片、影像档案(含使用条件页面) | https://jda.jaxa.jp/en/service.php |
| ESA Images | ESA 官方图像图库 | https://www.esa.int/ESA_Multimedia/Images |
| UZH Robotics and Perception Group | 事件相机、自主无人机竞速的演示视频 | https://www.youtube.com/user/ailabRPG |
| Boston Dynamics | Atlas / Spot 官方频道 | https://www.youtube.com/@BostonDynamics |
| Unitree Robotics | G1 / Go2 等的官方演示 | https://www.youtube.com/@unitreerobotics/videos |
| Dragonfly Gallery | 泰坦探测器的想象图、试验影像 | https://dragonfly.jhuapl.edu/Gallery/ |

#### D-2. 在这一领域实力强劲的大学、研究机构(研究室 URL 已确认实际存在)

| 大学、机构 | 研究室 / 部门 | 领域 | URL |
|---|---|---|---|
| Univ. of Zurich & ETH Zurich | Robotics and Perception Group(Scaramuzza) | 事件相机、自主无人机 | https://rpg.ifi.uzh.ch/ |
| MIT | CSAIL GelSight 项目(Adelson 系) | 基于视觉的触觉 | https://gelsight.csail.mit.edu/wedge/ |
| Stanford | Bao Group | 电子皮肤、可拉伸电子学 | https://baogroup.stanford.edu/ |
| Stanford | Interactive Perception and Robot Learning Lab | 机器人操作、感知 | https://iprl.stanford.edu/ |
| CMU | Robotics Institute(1979 年创立,世界最大级) | 机器人学全领域 | https://www.ri.cmu.edu/ |
| TUM | MIRMI(Munich Institute of Robotics and Machine Intelligence) | 机器人学、机器智能(70+ 位教授) | https://www.mirmi.tum.de/en/mirmi/home/ |
| TU Delft | QuTech(+ TNO) | 量子计算机、量子互联网、NV 色心 | https://qutech.nl/ |
| Sandia National Labs | Atom Interferometry 团队 | 量子惯性导航 | https://www.sandia.gov/quantum/atom-interferometry/ |
| 东北大学 | Space Robotics Lab(吉田研。ETS-VII、HAKUTO 技术负责人) | 太空机器人、月面探索 | https://astro2.mech.tohoku.ac.jp/en/ |
| 东京大学 | Intelligent Space Systems Laboratory(航空航天) | 航天器 GNC、自主化 | https://www.space.t.u-tokyo.ac.jp/ |
| 东京大学 | JSK Robotics Laboratory | 人形机器人、智能机器人 | http://www.jsk.t.u-tokyo.ac.jp/information.html |
| 东京科学大学(原东工大) | 岩崎研(固态量子传感器) | NV 色心量子传感 | http://dia.pe.titech.ac.jp/en/solid-quantum-sensors/ |
| JHU APL | Dragonfly 任务团队(PI: Elizabeth Turtle) | 行星旋翼探索 | https://dragonfly.jhuapl.edu/ |
| NASA JPL | CADRE(自主协作巡视器) | 月面多机器人 | https://www.jpl.nasa.gov/missions/cadre/ |

---

### E. 相关学会、展会、竞赛 — "能去看 / 能参赛"的路线

#### E-1. 学会("阅读、聆听"研究的最前线)

| 学会 | 介绍(1〜2 行) | 大致举办时间 | URL |
|---|---|---|---|
| ICRA | IEEE RAS 旗舰、机器人领域最大级会议。2026 年在维也纳(6/1–5),2027 年在 5 月下旬 | 每年 5〜6 月 | https://www.ieee-ras.org/conferences-workshops/fully-sponsored/icra/ (2026: https://2026.ieee-icra.org/ ) |
| IROS | IEEE/RSJ 共同主办的另一个最大级会议(1988 年〜)。2026 年在匹兹堡 | 每年 10 月前后 | https://www.ieee-ras.org/conferences-workshops/financially-co-sponsored/iros/ (2026: https://2026.ieee-iros.org/ ) |
| RSS | 少而精、以口头报告为主的"重质量"会议。2026 年在悉尼(7/13–17) | 每年 7 月前后 | https://roboticsconference.org/ |
| CoRL | 专注机器人学习(RL、模仿、基础模型)的年轻会议(2017 年〜)。2026 年为 11/9–12 | 每年 11 月前后 | https://www.corl.org/ |
| Humanoids | IEEE-RAS 人形机器人专门会议(2000 年〜)。第 25 届于 2026-12 在硅谷 | 每年 11〜12 月 | https://2026.ieee-humanoids.org/ |
| NeurIPS(相关 WS) | ML 最高峰会议。每年附设 Robot Learning 系工作坊(例: World Models × 机器人学习 WS @ NeurIPS 2026) | 每年 12 月 | https://neurips.cc/ (WS 示例: https://robowm-ws.github.io/ ) |
| ICLR(相关 WS) | 表示学习的最高峰会议。机器人×基础模型系 WS 的载体 | 每年 4〜5 月 | https://iclr.cc/ |

#### E-2. 展会("去看"实机 — 学生也容易入场)

| 展会 | 介绍(1〜2 行) | 大致举办时间 | URL |
|---|---|---|---|
| 国际机器人展 iREX(东京) | 从 1974 年延续至今的世界最大级机器人展。2025 年 12/3–6 在东京 Big Sight 举办,下一届是 2027 年 12 月 | 隔年 12 月(奇数年) | https://irex.nikkan.co.jp/ |
| World Robot Conference(北京) | 中国最大级的机器人会议+展示+竞赛综合活动。是人形机器人新品的首发舞台 | 每年 8 月前后 | https://www.worldrobotconference.com/ |
| CES(拉斯维加斯) | 世界最大级的科技展。近年是人形机器人、Physical AI 的主要发布舞台 | 每年 1 月 | https://www.ces.tech/ |
| automatica(慕尼黑) | 智能自动化、工业机器人的世界级展会。下一届 2027 年 6/22–25 | 隔年 6 月 | https://automatica-munich.com/en/ |
| CEATEC(幕张) | 日本最大级的 IT、电子展。2026 年 10/13–16 在幕张 Messe。学生入场门槛低 | 每年 10 月 | https://www.ceatec.com/en/ |

#### E-3. 竞赛("能参赛" — 个人、学生队伍的入口)

| 竞赛 | 介绍(1〜2 行) | 大致举办时间 | URL |
|---|---|---|---|
| **ROBO-ONE(日本)** ★重点 | 从 2002 年延续至今的双足机器人格斗竞赛。**个人可以带自制人形机器人参赛**,是发源于日本的文化,还有可用市售机参赛的新手向「ROBO-ONE Light」。作为本文"个人版机器人运动会"的现实世界版本,契合度最高 | 每年约 2 次(春、秋) | https://www.robo-one.com/ (解说: https://www.robo-one.com/abouts/view/aboutroboone/ ) |
| RoboCup | 高举"2050 年用机器人战胜世界杯冠军队"旗帜的国际竞赛。除足球外还有救援、家庭、工业联赛,以及面向中学生的 RoboCupJunior | 每年 7 月前后(世界大赛) | https://www.robocup.org/ |
| World Humanoid Robot Games(北京) | 2025 年 8 月在鸟巢首次举办。16 个国家 280 支队伍、500 多台人形机器人在 26 个项目中竞技(100 m 跑冠军成绩 21.50 秒)。第 2 届为 2026 年 8 月 | 每年 8 月 | https://english.beijing.gov.cn/whatson/events/sports/202505/t20250509_4085816.html (概要: https://en.wikipedia.org/wiki/World_Humanoid_Robot_Games ) |
| DARPA Robotics Challenge(历史) | 2012–2015 年的人形机器人灾害应对竞赛。当时的机器人频频摔倒,却是当前人形机器人热潮的原点。是讲述"10 年走到了这一步"的好素材 | 已结束(存档) | https://www.darpa.mil/research/programs/darpa-robotics-challenge |
| DARPA Triage Challenge(现行) | DARPA 现行挑战赛的例子。用传感+自主系统革新大规模伤员分诊的竞赛(2025 年决赛) | 项目进行中 | https://triagechallenge.darpa.mil/ |

> 路线备忘: 可以画出这样一级级台阶 —— "观赛"选 CEATEC、iREX(日本国内、低成本)→"参赛"选 ROBO-ONE Light(可用市售机)→ RoboCupJunior(中学生)→ 到大学再走 RoboCup/学会。

---

### 可用于文章的"事实+出处"备忘(防夸大用)

| 事实 | 出处 |
|---|---|
| 事件相机的时间分辨率为微秒级,动态范围约 140 dB(帧相机约 60 dB) | https://arxiv.org/abs/1904.08405 |
| Sony IMX636/637 为业界最小(发布当时)的 4.86 µm 事件像素、1280×720 | https://www.sony-semicon.com/en/news/2021/2021090901.html |
| Meta 的 sEMG 腕带无需校准即可通用解码,空中手写 20.9 词/分(Nature 645, 2025) | https://www.nature.com/articles/s41586-025-09255-w |
| ADRAS-J 自主接近非合作垃圾(全长约 11 m、约 3 吨)至 15 m(2024) | https://www.astroscale.com/en/news/astroscales-adras-j-achieves-historic-15-meter-approach-to-space-debris |
| Ingenuity 3 年间飞行 72 次,2024-01 任务结束。作为技术验证的费用约 8,500 万美元 | https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ / https://www.space.com/space-exploration/missions/nasa-begins-building-nuclear-powered-dragonfly-drone-for-2028-launch-to-saturn-moon-titan |
| Dragonfly 任务总额约 33.5 亿美元,计划 2028-07 发射(Falcon Heavy),已通过 CDR | https://www.space.com/space-exploration/missions/nasa-begins-building-nuclear-powered-dragonfly-drone-for-2028-launch-to-saturn-moon-titan |
| Varda W-1 在轨制造 Ritonavir 晶体并于 2024-02 地面回收(民间首创级) | https://www.space.com/varda-in-space-manufacturing-capsule-landing-success |
| NASA VIPER 于 2024-07 决定取消(已投入约 4.5 亿美元,取消节省约 8,400 万美元) | https://spaceflightnow.com/2024/07/18/nasa-cancels-half-billion-dollar-water-ice-seeking-moon-rover/ |
| CADRE 的 3 台自主巡视器将随 IM-3 着陆器前往 Reiner Gamma(预定 2026) | https://www.jpl.nasa.gov/missions/cadre/ / https://www.nasa.gov/missions/tech-demonstration/cadre/nasas-mini-rover-team-is-packed-for-lunar-journey/ |
| X-37B 第 8 次飞行计划在轨测试量子惯性传感器(原子干涉仪)(2025) | https://theconversation.com/quantum-alternative-to-gps-navigation-will-be-tested-on-us-military-spaceplane-262967 |

---

## 附录 H:学习日志实测摘录 — 13 个世代的成长曲线,原样奉上数字

这是从各世代的训练日志中,摘录 eval 行(约每 5.2M 步一次)主要数值的原始数据表(均为 MuJoCo 仿真内的实测值)。虽然比图表粗糙,但可以在原始记录里确认"哪个世代、在何时、如何成长/卡住"(reward 在世代之间的奖励设计不同,**不能做纵向比较**,请只看同一世代内的走势)。ep_len 为存活步数(×0.02 秒),fwd_v 为前进速度 m/s,crash 为碰撞率。

### walk10(至 26M・eval 6 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 194 | 31 | 1.09 | — |
| 5M | 258 | 42 | 0.93 | — |
| 10M | 338 | 57 | 0.83 | — |
| 16M | 469 | 81 | 0.80 | — |
| 21M | 691 | 126 | 0.72 | — |
| 26M | 1861 | 371 | 0.71 | — |

### walk11(至 31M・eval 7 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.09 | — |
| 5M | 265 | 43 | 0.95 | — |
| 10M | 354 | 58 | 0.85 | — |
| 16M | 471 | 78 | 0.78 | — |
| 21M | 685 | 118 | 0.67 | — |
| 26M | 1673 | 316 | 0.67 | — |
| 31M | 3331 | 667 | 0.83 | — |

### walk12(至 52M・eval 11 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.09 | — |
| 5M | 260 | 42 | 0.95 | — |
| 10M | 327 | 54 | 0.84 | — |
| 16M | 479 | 80 | 0.77 | — |
| 21M | 687 | 118 | 0.70 | — |
| 26M | 1256 | 223 | 0.73 | — |
| 31M | 1536 | 277 | 0.72 | — |
| 37M | 1791 | 320 | 0.76 | — |
| 42M | 1701 | 305 | 0.80 | — |
| 47M | 1945 | 344 | 0.81 | — |
| 52M | 1996 | 355 | 0.80 | — |

### walk12b(至 58M・eval 12 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.09 | 0.00 |
| 5M | 255 | 41 | 0.93 | 0.00 |
| 10M | 332 | 54 | 0.84 | 0.00 |
| 16M | 463 | 77 | 0.76 | 0.00 |
| 21M | 700 | 119 | 0.67 | 0.00 |
| 26M | 1525 | 274 | 0.76 | 0.00 |
| 31M | 1909 | 350 | 0.83 | 0.00 |
| 37M | 2124 | 391 | 0.88 | 0.00 |
| 42M | 2322 | 426 | 0.85 | 0.00 |
| 47M | 2181 | 400 | 0.84 | 0.00 |
| 52M | 2489 | 458 | 0.79 | 0.00 |
| 58M | 2328 | 428 | 0.79 | 0.00 |

### walk12c(至 68M・eval 14 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.08 | 0.00 |
| 5M | 258 | 42 | 0.95 | 0.00 |
| 10M | 359 | 59 | 0.89 | 0.00 |
| 16M | 552 | 92 | 0.74 | 0.00 |
| 21M | 957 | 161 | 0.76 | 0.00 |
| 26M | 2057 | 343 | 0.85 | 0.00 |
| 31M | 4520 | 725 | 0.91 | 0.00 |
| 37M | 5725 | 882 | 1.09 | 0.00 |
| 42M | 6522 | 975 | 1.19 | 0.00 |
| 47M | 6828 | 989 | 1.29 | 0.00 |
| 52M | 7043 | 999 | 1.35 | 0.00 |
| 58M | 7148 | 992 | 1.40 | 0.00 |
| 63M | 7313 | 1000 | 1.41 | 0.00 |
| 68M | 7410 | 1000 | 1.43 | 0.00 |

### walk13(至 131M・eval 26 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 197 | 31 | 1.07 | 0.01 |
| 10M | 286 | 46 | 0.93 | 0.01 |
| 21M | 504 | 84 | 0.78 | 0.14 |
| 31M | 834 | 142 | 0.67 | 0.27 |
| 42M | 1095 | 192 | 0.67 | 0.27 |
| 52M | 1256 | 223 | 0.61 | 0.23 |
| 63M | 1335 | 240 | 0.53 | 0.20 |
| 73M | 1297 | 230 | 0.62 | 0.20 |
| 84M | 1496 | 266 | 0.54 | 0.20 |
| 94M | 1932 | 351 | 0.38 | 0.19 |
| 105M | 2282 | 418 | 0.33 | 0.13 |
| 115M | 2706 | 495 | 0.22 | 0.16 |
| 126M | 3007 | 553 | 0.22 | 0.14 |
| 131M | 3300 | 601 | 0.20 | 0.12 |

### walk13b(至 126M・eval 25 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.08 | 0.01 |
| 10M | 297 | 48 | 0.89 | 0.03 |
| 21M | 535 | 89 | 0.73 | 0.08 |
| 31M | 919 | 162 | 0.72 | 0.23 |
| 42M | 1329 | 247 | 0.61 | 0.22 |
| 52M | 1816 | 355 | 0.57 | 0.12 |
| 63M | 2058 | 398 | 0.47 | 0.10 |
| 73M | 2357 | 459 | 0.39 | 0.12 |
| 84M | 2774 | 540 | 0.38 | 0.09 |
| 94M | 3009 | 591 | 0.25 | 0.09 |
| 105M | 3072 | 606 | 0.24 | 0.10 |
| 115M | 3266 | 627 | 0.30 | 0.10 |
| 126M | 3338 | 642 | 0.28 | 0.15 |

### walk13c(至 68M・eval 14 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 193 | 31 | 1.06 | 0.01 |
| 5M | 243 | 39 | 0.96 | 0.03 |
| 10M | 303 | 49 | 0.93 | 0.02 |
| 16M | 402 | 66 | 0.78 | 0.06 |
| 21M | 602 | 100 | 0.71 | 0.12 |
| 26M | 831 | 140 | 0.64 | 0.18 |
| 31M | 976 | 162 | 0.61 | 0.30 |
| 37M | 1152 | 195 | 0.53 | 0.23 |
| 42M | 1634 | 284 | 0.43 | 0.20 |
| 47M | 1783 | 311 | 0.35 | 0.20 |
| 52M | 2293 | 406 | 0.32 | 0.29 |
| 58M | 2851 | 500 | 0.29 | 0.27 |
| 63M | 3668 | 637 | 0.23 | 0.26 |
| 68M | 3994 | 686 | 0.20 | 0.20 |

### walk13d(至 147M・eval 29 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 193 | 31 | 1.06 | 0.01 |
| 10M | 259 | 42 | 0.98 | 0.02 |
| 21M | 340 | 56 | 0.87 | 0.07 |
| 31M | 503 | 82 | 0.83 | 0.15 |
| 42M | 683 | 112 | 0.77 | 0.24 |
| 52M | 846 | 143 | 0.69 | 0.21 |
| 63M | 989 | 166 | 0.71 | 0.27 |
| 73M | 1112 | 188 | 0.67 | 0.27 |
| 84M | 1372 | 229 | 0.77 | 0.34 |
| 94M | 1431 | 246 | 0.70 | 0.28 |
| 105M | 1552 | 268 | 0.77 | 0.30 |
| 115M | 1960 | 342 | 0.76 | 0.28 |
| 126M | 1930 | 335 | 0.83 | 0.31 |
| 136M | 2515 | 436 | 0.90 | 0.30 |
| 147M | 2575 | 448 | 0.91 | 0.37 |

### walk13e(至 147M・eval 29 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 222 | 31 | 1.06 | 0.01 |
| 10M | 294 | 42 | 0.99 | 0.00 |
| 21M | 401 | 59 | 0.93 | 0.08 |
| 31M | 542 | 80 | 0.88 | 0.15 |
| 42M | 731 | 106 | 0.95 | 0.26 |
| 52M | 829 | 118 | 0.96 | 0.41 |
| 63M | 996 | 144 | 0.96 | 0.47 |
| 73M | 1054 | 152 | 0.99 | 0.52 |
| 84M | 1335 | 195 | 0.95 | 0.49 |
| 94M | 1481 | 216 | 0.98 | 0.53 |
| 105M | 1516 | 225 | 0.95 | 0.52 |
| 115M | 1890 | 290 | 0.90 | 0.41 |
| 126M | 1936 | 296 | 0.93 | 0.52 |
| 136M | 2450 | 374 | 0.96 | 0.42 |
| 147M | 2889 | 439 | 0.96 | 0.47 |

### walk4(至 42M・eval 9 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 147 | 44 | -0.18 | — |
| 5M | 221 | 59 | 0.05 | — |
| 10M | 496 | 126 | 0.06 | — |
| 16M | 2505 | 635 | 0.19 | — |
| 21M | 4158 | 924 | 0.45 | — |
| 26M | 4777 | 976 | 0.57 | — |
| 31M | 5132 | 993 | 0.62 | — |
| 37M | 5476 | 1000 | 0.57 | — |
| 42M | 5591 | 1000 | 0.62 | — |

### walk5(至 42M・eval 9 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 193 | 40 | -0.12 | — |
| 5M | 258 | 53 | -0.10 | — |
| 10M | 427 | 84 | -0.03 | — |
| 16M | 1864 | 382 | 0.09 | — |
| 21M | 4572 | 919 | 0.27 | — |
| 26M | 5193 | 965 | 0.45 | — |
| 31M | 5486 | 969 | 0.56 | — |
| 37M | 5922 | 997 | 0.57 | — |
| 42M | 6080 | 1000 | 0.61 | — |

### walk6(至 37M・eval 8 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 245 | 40 | -0.12 | — |
| 5M | 322 | 49 | -0.10 | — |
| 10M | 416 | 57 | -0.05 | — |
| 16M | 635 | 84 | 0.05 | — |
| 21M | 1607 | 217 | 0.03 | — |
| 26M | 5380 | 715 | 0.20 | — |
| 31M | 7299 | 928 | 0.33 | — |
| 37M | 7957 | 979 | 0.47 | — |

### walk8(至 37M・eval 8 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 174 | 34 | 0.98 | — |
| 5M | 214 | 42 | 0.82 | — |
| 10M | 273 | 54 | 0.74 | — |
| 16M | 369 | 74 | 0.66 | — |
| 21M | 583 | 119 | 0.67 | — |
| 26M | 1470 | 315 | 0.63 | — |
| 31M | 2821 | 612 | 0.71 | — |
| 37M | 3678 | 801 | 0.80 | — |

### walk9(至 37M・eval 8 次)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 164 | 31 | 1.09 | — |
| 5M | 219 | 42 | 0.95 | — |
| 10M | 288 | 56 | 0.86 | — |
| 16M | 386 | 75 | 0.84 | — |
| 21M | 629 | 125 | 0.77 | — |
| 26M | 1364 | 283 | 0.73 | — |
| 31M | 2800 | 589 | 0.85 | — |
| 37M | 4085 | 856 | 1.02 | — |

## 附录 I:可能会被问到的问题(FAQ)

把读者可能会问的问题,提前诚实地回答在这里。

**Q. 总共花了多少钱?**
A. 追加投资只有一台含 GPU 的整机 PC(几十万日元级)。软件方面,从物理引擎到机器人模型、动作数据、训练框架,全部是免费(OSS)。日常开销就是电费,每训练一个项目不到一百日元(12.1 节的实测估算)。作为爱好,体感上比摄影或高尔夫便宜。

**Q. 花了多长时间?**
A. 本文的这批实验大约是数周。不过并不是整天守在电脑前,而是"傍晚布置好,晚上看结果"的循环往复。GPU 的练习时间远比人类的工作时间长。

**Q. 需要会多少编程?**
A. 我本人是图像处理工程师,但本文实现工作的大部分都交给了 AI 编程代理(如开头的署名所述)。真正需要的,与其说是写代码的能力,不如说是决定"测什么才能识破谎言"的能力。我认为现在已经是编程新手与 AI 搭档也能站上入口的时代了。但是**结果的验证不能交给 AI** —— 只有这一点是人类的工作。

**Q. 没有实体机器人,有意义吗?**
A. 我认为有,所以一直在继续。理由有 3 个: ①只要把观测对齐到实机的传感器配置,策略原理上就能迁移到实机(已经站在 sim-to-real 的入口)。②在实机上危险且昂贵的失败(几千次摔倒)只能在仿真里积累。③本来在实机的开发现场,先在仿真里跑通如今也是标准流程。不过,即使在仿真里完美,到了实机也会崩掉的因素(未建模的摩擦、延迟、形变)肯定存在,这部分只能诚实地说尚未验证。

**Q. 交给 AI 到什么程度,你自己做了什么?**
A. 定方向、提假设、怀疑结果、决定何时收手,是我;写代码、跑实验、汇总数值,是 AI。比如"加入事件相机式的时间差分"是我的发案,"在该实现中解析地求解圆柱相交"是 AI 的工作。反过来,不轻信"抬起了 48mm"的报告、预先立下"必须用视频验证后才算合格"的规则,是我这边的工作;而遵照这条规则实际审看视频、查明那是幻影(初始化 bug 造成的弹射)的,又是 AI 自己。作为分工奏效的例子,我很喜欢这一段。

**Q. 尽是失败,不会烦吗?**
A. 也有烦的日子。不过,这个领域的失败属于"原因一定能查明"的类型(因为物理引擎是可复现的)。能查明原因的失败会变成资产 —— 附录 A 的编年史实际上就是这么来的。顺便说,最让我沮丧的一次,是连续 3 周被发明了 3 种不同的作弊。

**Q. 该从哪里开始?**
A. 推荐路线: ① 装上 MuJoCo,把 Menagerie 的机器人显示到屏幕上(1 天)→ ② 让喜欢的模型以 keyframe 姿态站立,跑起物理(1 天)→ ③ 跑通 mujoco_playground 的四足步行教程(数天)→ ④ 定下一个自己的"比赛项目",开始写奖励(从这里开始入沼)。在 ④ 之前读一读本文的附录 D(教训集),沼的深度应该能浅三成。

**Q. 小孩子或学生也能做吗?**
A. 仿真本身是免费的,即使没有 GPU,用 CPU 也能做小实验(训练会变慢,但四足步行这种量级还算现实)。第 13 章的资料集里,从看着开心的入口(官方视频)到竞赛(ROBO-ONE 可以个人参赛)的路线都整理好了。

**Q. 为什么是运动会?**
A. 因为竞技会带来测量与纪律(第 1 章)。还有,单纯因为好玩。不好玩的话坚持不了几个星期。

**Q. 这篇文章,是不是太长了?**
A. 是的。不过开头附了目录和 3 条阅读路线,需要哪里就取哪里。请把这个长度看作"一个玩法能挖多深"的实验。这也算一种竞技。
