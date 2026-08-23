### B.1 种类明细(实测 67 模型)

| 种类 | 数 | 代表 |
|---|---|---|
| 人形(双足) | 12 | Unitree G1/H1、Booster T1、Fourier N1、Apptronik Apollo、PAL Talos、Agility Cassie、Berkeley Humanoid、Robotis OP3、PND Adam Lite、ToddlerBot ×2 |
| 四足 | 8 | ANYmal B/C、Boston Dynamics Spot、Google Barkour v0/vB、Unitree A1/Go1/Go2 |
| 机械臂(单臂) | 22 | Franka Panda/FR3、KUKA iiwa14、UR5e/UR10e、Kinova Gen3、xArm7、ViperX 等 |
| 双臂 | 2 | ALOHA、Trossen WXAI |
| 移动机械手 | 7 | Hello Robot Stretch ×2、PAL TIAGo ×2、Google Robot、TidyBot、Rainbow RBY1 |
| 多指灵巧手 | 6 | Shadow Hand、LEAP Hand、Allegro、Shadow DEX-EE 等 |
| 夹爪 | 3 | Robotiq 2F-85 ×2、UMI Gripper |
| 无人机 | 2 | Crazyflie 2、Skydio X2 |
| 肌骨/生物 | 2 | MS-Human-700(700 肌)、flybody(苍蝇) |
| 其他 | 3 | 足球套件、RealSense D435i(传感器材料)、IIT SoftFoot(足部部件) |

![名鉴统计](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_roster_stats.png)
*图: 67 台的种类、执行器类型、keyframe 有无的实测汇总(据盘点 JSON 作图)*

### B.2 盘点中看见的"让它们动起来的地图"

![Go2 肖像](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_go2.png)
*图: Unitree Go2(仿真渲染)*

![Spot 肖像](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_spot.png)
*图: Boston Dynamics Spot(仿真渲染)*

- **四足 8 个机型全部同构(自由度 18、驱动 12)。** 也就是说,写 1 条训练流水线就能把 8 个机型横向扫一遍。四足项目最适合作为运动会的团体项目。
- **机械臂 22 条"不会摔倒",所以只要套上逆运动学(IK,从手端目标位置反算关节角的计算)就能立刻做出演示。** 微分 IK 库(mink,Apache-2.0)的示例事实上成了 Menagerie 的演示集。
- **没有 home 姿势(keyframe)的模型有 19 台。** 全员亮相的第一步"素材制作",是自制站立姿势这种略显朴素的工作。
- **需要注意的个体**: Cassie 是闭链机构,GPU 并行(MJX)受限。多指灵巧手是腱驱动或欠驱动,需要按"关节数与指令数不一致"的前提来设计。
- **人形 12 台中,有扭矩直连型(H1、Talos 等)与位置伺服型(G1、T1 等)。** 正文的 H1 对应中,写了把扭矩型位置伺服化的适配器来吸收这一差异(为了把 G1 的奖励 11 条原样移植)。

### B.3 学习资源的两大支柱,与许可的雷区

OSS 的训练环境,以 (1) **MuJoCo Playground**(Apache-2.0。四足、双足移动 9 机型+操作 4 机型的训练环境与配置)和 (2) **LocoMuJoCo**(MIT。发布 22,000 条以上重定向完毕的动作,人形 10+四足 4)为两大支柱,互为补充。

而盘点最大的收获,是**动作数据的许可地图**。

| 数据源 | 内容 | 许可 |
|---|---|---|
| AMASS | SMPL 统一的大规模动捕集成 | **仅限非商用(商用的神经网络训练也禁止)** |
| LAFAN1(本文的教师) | 4.6 小时的高质量动捕 | **CC BY-NC-ND(非商用、禁止改动)** |
| CMU Mocap | 2,600+ 序列 | **免费、可商用**(仅禁止转卖) |
| GMR(通用重定向器) | SMPL-X/BVH/视频 → 机器人 18 机型 | **MIT** |

作为兴趣的运动会,用 LAFAN1 没有问题;但要把这项技术推向产品,**"CMU mocap(可商用)+ GMR(MIT)"的组合是最干净的谱系**。数据的许可比代码的许可更容易被忽视,而且事后难以替换——这也是产业侧的感觉派上用场的一点。

### B.4 全 67 模型实测表

67 台的"体格测量结果"。nq=广义坐标数(自由度+四元数的份),nv=速度自由度,nu=驱动指令数。执行器类型的含义如正文与 B.2 所述,自由关节为"有"的机体存在跌倒(=平衡成为竞技)。keyframe 是随附的基准姿势。所有行都是实际加载并跑过物理步进采到的值。

| 模型 | nq | nv | nu | 执行器 | 自由关节 | keyframe | 网格数 | 许可 |
|---|---|---|---|---|---|---|---|---|
| `agilex_piper` | 8 | 8 | 7 | position+kv×7 | 无 | home | 82 | MIT |
| `agility_cassie` | 35 | 32 | 10 | motor×10 | 有 | home | 25 | custom/see LICENSE |
| `aloha` | 16 | 16 | 14 | position×12, position+kv×2 | 无 | neutral_pose | 24 | custom/see LICENSE |
| `anybotics_anymal_b` | 19 | 18 | 12 | position×12 | 有 | 无 | 46 | custom/see LICENSE |
| `anybotics_anymal_c` | 19 | 18 | 12 | position×12 | 有 | 无 | 24 | custom/see LICENSE |
| `apptronik_apollo` | 39 | 38 | 32 | position×32 | 有 | stand | 44 | Apache-2.0 |
| `arx_l5` | 8 | 8 | 7 | position+kv×7 | 无 | home | 10 | BSD |
| `berkeley_humanoid` | 19 | 18 | 12 | position+kv×12 | 有 | home | 13 | custom/see LICENSE |
| `bitcraze_crazyflie_2` | 7 | 6 | 4 | motor×4 | 有 | hover | 39 | MIT |
| `booster_t1` | 30 | 29 | 23 | position+kv×23 | 有 | home | 24 | Apache-2.0 |
| `boston_dynamics_spot` | 19 | 18 | 12 | position+kv×12 | 有 | home | 23 | BSD |
| `dynamixel_2r` | 2 | 2 | 2 | position+kv×2 | 无 | 无 | 15 | custom/see LICENSE |
| `flexiv_rizon4` | 7 | 7 | 7 | position+kv×7 | 无 | home | 14 | Apache-2.0 |
| `flexiv_rizon4s` | 7 | 7 | 7 | position+kv×7 | 无 | home | 14 | Apache-2.0 |
| `flybody` | 109 | 108 | 78 | position×64, motor×6, adhesion×8 | 有 | key0 | 85 | Apache-2.0 |
| `fourier_n1` | 30 | 29 | 23 | motor×23 | 有 | home | 29 | Apache-2.0 |
| `franka_emika_panda` | 9 | 9 | 8 | position+kv×8 | 无 | home | 67 | Apache-2.0 |
| `franka_fr3` | 7 | 7 | 7 | position+kv×7 | 无 | home | 36 | Apache-2.0 |
| `franka_fr3_v2` | 7 | 7 | 7 | position+kv×7 | 无 | home | 37 | Apache-2.0 |
| `google_barkour_v0` | 19 | 18 | 12 | position+kv×12 | 有 | standing | 14 | Apache-2.0 |
| `google_barkour_vb` | 19 | 18 | 12 | position+kv×12 | 有 | home | 11 | Apache-2.0 |
| `google_robot` | 9 | 9 | 9 | position×9 | 无 | 无 | 47 | Apache-2.0 |
| `hello_robot_stretch` | 31 | 29 | 8 | motor×2, position+kv×3, position×3 | 有 | 无 | 67 | BSD |
| `hello_robot_stretch_3` | 41 | 38 | 10 | velocity×2, position+kv×3, position×5 | 有 | home、stow | 85 | Apache-2.0 |
| `i2rt_yam` | 8 | 8 | 7 | position+kv×7 | 无 | home | 17 | MIT |
| `iit_softfoot` | 93 | 93 | 1 | position×1 | 无 | 无 | 10 | custom/see LICENSE |
| `kinova_gen3` | 7 | 7 | 7 | position+kv×7 | 无 | home、retract | 8 | custom/see LICENSE |
| `kuka_iiwa_14` | 7 | 7 | 7 | position+kv×7 | 无 | home | 13 | BSD |
| `leap_hand` | 16 | 16 | 16 | position+kv×16 | 无 | 无 | 11 | custom/see LICENSE |
| `low_cost_robot_arm` | 6 | 6 | 6 | position+kv×6 | 无 | home | 22 | Apache-2.0 |
| `ms_human_700` | 85 | 85 | 700 | muscle×700 | 无 | init | 189 | Apache-2.0 |
| `pal_talos` | 51 | 50 | 32 | motor×32 | 有 | key0 | 74 | Apache-2.0 |
| `pal_tiago` | 29 | 28 | 14 | motor×7, position×5, velocity×2 | 有 | 无 | 21 | Apache-2.0 |
| `pal_tiago_dual` | 32 | 31 | 25 | velocity×4, position×7, motor×14 | 有 | 无 | 25 | Apache-2.0 |
| `pndbotics_adam_lite` | 32 | 31 | 25 | motor×25 | 有 | 无 | 73 | MIT |
| `rainbow_robotics_rby1` | 35 | 34 | 26 | velocity×2, position+kv×24 | 有 | 无 | 47 | Apache-2.0 |
| `realsense_d435i` | 0 | 0 | 0 | — | 无 | 无 | 9 | Apache-2.0 |
| `rethink_robotics_sawyer` | 7 | 7 | 7 | position+kv×7 | 无 | home | 49 | Apache-2.0 |
| `robot_soccer_kit` | 71 | 70 | 4 | velocity×3, position+kv×1 | 有 | 无 | 29 | custom/see LICENSE |
| `robotiq_2f85` | 15 | 14 | 1 | position+kv×1 | 有 | 无 | 8 | custom/see LICENSE |
| `robotiq_2f85_v4` | 13 | 12 | 1 | position+kv×1 | 有 | 无 | 8 | custom/see LICENSE |
| `robotis_op3` | 27 | 26 | 20 | position×20 | 有 | 无 | 48 | Apache-2.0 |
| `robotstudio_so101` | 6 | 6 | 6 | position+kv×6 | 无 | 无 | 18 | Apache-2.0 |
| `shadow_dexee` | 12 | 12 | 12 | motor×12 | 无 | 无 | 26 | Apache-2.0 |
| `shadow_hand` | 31 | 30 | 20 | position×20 | 有 | 无 | 13 | Apache-2.0 |
| `sharpa_wave` | 22 | 22 | 22 | position+kv×22 | 无 | 无 | 54 | Apache-2.0 |
| `skydio_x2` | 7 | 6 | 4 | motor×4 | 有 | hover | 1 | Apache-2.0 |
| `stanford_tidybot` | 18 | 18 | 11 | position+kv×11 | 无 | home、retract | 20 | MIT |
| `tetheria_aero_hand_open` | 16 | 16 | 7 | position×7 | 无 | home | 27 | Apache-2.0 |
| `toddlerbot_2xc` | 51 | 50 | 30 | motor×30 | 有 | home | 47 | MIT |
| `toddlerbot_2xm` | 51 | 50 | 30 | motor×30 | 有 | home | 47 | MIT |
| `trossen_vx300s` | 8 | 8 | 7 | position×7 | 无 | home | 10 | custom/see LICENSE |
| `trossen_wx250s` | 8 | 8 | 7 | position+kv×7 | 无 | home | 10 | custom/see LICENSE |
| `trossen_wxai` | 16 | 16 | 14 | position×14 | 无 | left/、right/ | 84 | BSD |
| `trs_so_arm100` | 6 | 6 | 6 | position+kv×6 | 无 | home、rest | 18 | Apache-2.0 |
| `ufactory_lite6` | 6 | 6 | 6 | position+kv×6 | 无 | home | 14 | custom/see LICENSE |
| `ufactory_xarm7` | 13 | 13 | 8 | position+kv×8 | 无 | home | 16 | custom/see LICENSE |
| `umi_gripper` | 8 | 8 | 7 | position×1, position+kv×6 | 无 | 无 | 6 | MIT |
| `unitree_a1` | 19 | 18 | 12 | position×12 | 有 | home | 5 | BSD |
| `unitree_g1` | 36 | 35 | 29 | position+kv×29 | 有 | stand | 35 | custom/see LICENSE |
| `unitree_go1` | 19 | 18 | 12 | position×12 | 有 | home | 5 | BSD |
| `unitree_go2` | 19 | 18 | 12 | motor×12 | 有 | home | 16 | custom/see LICENSE |
| `unitree_h1` | 26 | 25 | 19 | motor×19 | 有 | home | 21 | custom/see LICENSE |
| `unitree_z1` | 6 | 6 | 6 | position+kv×6 | 无 | home | 7 | BSD |
| `universal_robots_ur10e` | 6 | 6 | 6 | position+kv×6 | 无 | home | 20 | custom/see LICENSE |
| `universal_robots_ur5e` | 6 | 6 | 6 | position+kv×6 | 无 | home | 20 | custom/see LICENSE |
| `wonik_allegro` | 23 | 22 | 16 | position×16 | 有 | 无 | 11 | custom/see LICENSE |


## 附录 C: 传感器图鉴 — 规格、长短板、融合、市场动向

观测设计就是传感器选型——这是支撑正文这一主张的资料编。

![传感器比较雷达](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_sensor_compare.png)
*图: 主要 5 种传感器的特性比较(由附录 C 的实际规格表做的定性汇总)。没有万能的传感器 — 所以要混着用(融合)*

数值为 2026-08 时点的调查,每一项都附有出处(优先官方数据手册。无法确认的值保留为"未确认"——比起用猜测填上,让人看得出没填上,作为资料才诚实)。

### 1. 主要传感器的规格与长短板

**面向文章的摘要(5 行)**

1. 人形机器人的"眼睛"靠 1 种传感器无法成立 — LiDAR(准确的距离)、深度相机(致密的近距离 3D)、IMU(姿态)、关节编码器(自己的身体)叠加起来,才第一次看得见世界。
2. Livox Mid-360 以 360°×(-7°〜+52°) FOV、20 万点/秒、265 g、行情 $750〜900,成为研究用机器人 LiDAR 的事实标准(高一个数量级的工业级 Hesai XT16 为 $6,650)。
3. Intel RealSense D435i 是 87°×58° FOV 的主动 IR 立体+内置 IMU、$334,2025 年从 Intel 拆分出来的 RealSense Inc. 正在向 D500 系更新。
4. 事件相机(Sony IMX636)拥有 μs 级的时间分辨率和 120 dB(低照度条件)的动态范围,但评估套件仍在数十万日元级,处于"下一位主角候选"阶段。
5. IMU 按等级价格差 3 个数量级(民用 数美元 → 战术级 $8,000 以上),而无 GPS 60 秒的位置误差从 400 m → 5 m 缩小 2 个数量级 — 腿式机器人的定式是用民用〜工业级 IMU+其他传感器融合来作战。

#### 1.0 横向比较表(人形搭载视角)

| 传感器 | 原理(1 行) | 擅长 | 不擅长 | 代表机型与价格带 | 典型用途 |
|---|---|---|---|---|---|
| 旋转式/半球 LiDAR | 用激光飞行时间(ToF)直接测距 | 距离精度(cm 级)、黑暗、宽 FOV | 雨/雾/雪、黑色低反射面、玻璃 | Livox Mid-360 $749〜/ Unitree L2 $419 / Hesai XT16 $6,650 | SLAM、避障、全周感知 |
| 深度相机(主动 IR 立体) | IR 图案投射+左右相机视差得深度 | 近距离的致密 3D、便宜、可同时取 RGB | 直射阳光(IR 打不过)、远距离、透明/镜面 | RealSense D435i $334 / Orbbec Gemini 335 $264 | 脚下地形、操作 |
| 立体相机(被动) | 仅凭左右相机视差得深度(+近年的神经深度) | 室外、长基线的中距离、无需投光 | 无纹理面(白墙)、暗处 | ZED 2i $499〜 / ZED X $549〜(搜索结果值) | 室外导航、车载型感知 |
| ToF 相机 | 调制光的相位差全像素同时测距 | 室内的致密深度、宽 FOV | 直射阳光、黑色低反射、多径 | Orbbec Femto Bolt $418 | 室内建图、手势 |
| 事件相机(DVS) | 每个像素只在亮度变化的瞬间异步输出 | 高速运动、HDR(逆光/隧道)、低延迟 | 静止场景(什么都不出)、已有 CV 资产用不上 | Prophesee EVK4 ≈$5,400(代理商)/ iniVation DVXplorer €3,900 | 高速回避、无人机检测、振动监测 |
| IMU(MEMS) | 角速度与加速度的惯性测量 | 高速率(kHz 级)、自成一体 | 漂移(单独使用位置发散) | BMI088 数美元级 / ADIS16470 $482 / HG4930 $8,300〜 | 姿态估计、LIO/VIO 的脊梁 |
| 6 轴 F/T 传感器 | 用应变片等测 3 力+3 力矩 | 直接算出 ZMP、力控制 | 昂贵、怕冲击/EMI | ATI Axia80(报价制)/ Robotiq FT 300-S 套件 $5,720 | 脚踝的地面反力、抓握力控制 |
| 触觉皮肤 | 凝胶变形的成像(视触觉)或磁式 3 轴分布 | 滑移检测、细微形状、材质 | 单位面积成本、布线、耐久 | GelSight Mini $499 / Meta Digit 360(价格未公布) | 指尖抓握、接触操作 |
| 超声波 | 声波的往返时间 | 透明物、玻璃也看得见,数美元 | 分辨率粗、指向性宽 | HC-SR04 数美元 | 近距保险杠式用途 |
| GNSS/RTK | 卫星定位+基准站补正 | 室外绝对位置 cm 级 | 室内、城市峡谷不可用 | u-blox ZED-F9P 板 $259.95 | 室外导航、地面真值 |
| 关节编码器 | 磁/光学直读关节角 | 高分辨率(17〜23 bit)、低延迟 | 完全看不见外界 | (机体内置) | 本体感受=控制的地基 |

---

#### 1.1 LiDAR

##### Livox Mid-360(最重要·详细)

方式: 非重复扫描(non-repetitive scanning)+旋转机构实现水平 360° 覆盖。FOV 内点的填充率随时间上升的 Livox 独有方式。

| 项目 | 值 | 出处 |
|---|---|---|
| FOV | 水平 360° / 垂直 **-7°〜+52°**(官方已确认) | https://www.livoxtech.com/mid-360/specs |
| 点数/秒 | 200,000 pts/s(first return) | 同上 |
| 测距范围 | 40 m @ 反射率 10% / 70 m @ 反射率 80%(均为环境光 100 klx) | 同上 |
| 测距波动(1σ) | ≤2 cm @ 10 m(至近 0.2 m 时 ≤3 cm) | 同上 |
| 角度精度 | < 0.15°(1σ) | 同上 |
| 质量 | 265 g | 同上 |
| 功耗 | 平均 6.5 W(自加热模式峰值 14 W) | 同上 |
| 帧率 | 10 Hz(typical) | 同上 |
| 波长 | 905 nm | 同上 |
| IMU | 内置(ICM40609) | 同上 |
| 接口 | 100BASE-TX Ethernet,支持 PTPv2/GPS 时刻同步 | 同上 |
| 价格 | 官方样品价 $749(2023-01 发售时。DJI 商店搜索结果也是 $749) | https://www.livoxtech.com/news/mid360_launch / https://store.dji.com/product/livox-mid-360 |
| 实际价格 | 美国代理商 $899(backorder),AliExpress 行情 $480〜550(2025 年的购买报告,非官方) | https://www.roboticscenter.ai/store/product/livox-dji-livox-mid-360 / https://www.aliexpress.com/s/wiki-ssr/article/livox-mid-360-price-usd-2025 |

- 擅长: 低价、轻量、内置 IMU、全周 FOV。FAST-LIO2 / Point-LIO 有官方配置文件(后述),开箱即可跑 LIO。
- 不擅长: 垂直只能向下看到 -7°(脚下正下方用深度相机补足是 G1 流)。905 nm 光学式,雨、雾、黑色低反射面在原理上不利。
- 典型用途: 四足/人形的 360° 近距感知、室内外 SLAM。研究用机器人的事实标准。
- 补充: Livox 另有 Avia(70.4°×77.2°,240k pts/s,450 m @ 80%,498 g — 面向无人机测绘 https://www.livoxtech.com/avia/specs)、HAP(车载,120°×25°,452k pts/s,150 m @ 10% — https://www.livoxtech.com/hap/specs)在售。

##### 竞品 LiDAR 比较

| 产品 | 方式 | 量程 @10% 反射率 | 点数/秒 | 质量 | 实际价格 | 出处 |
|---|---|---|---|---|---|---|
| Unitree L1 | 半球"4D LiDAR"360°×90° | 未确认(最大 30 m) | 21,600 | 230 g | **$249**(官方) | https://shop.unitree.com/products/unitree-4d-lidar-l1 |
| Unitree L2 | 半球 360°×96° | 未确认(最大 30 m) | 64,000(官方值。销售店有 128,000 的表述,不一致→采用官方值) | 未确认 | **$419**(官方) | https://shop.unitree.com/products/unitree-4d-lidar-l2 |
| Livox Mid-360 | 非重复 360°×59° | 40 m | 200,000 | 265 g | $749〜899 | 见上 |
| Hesai JT16 | 16ch 迷你穹顶 360°×40° | 30 m | 48,000 | 199.7 g / 4.3 W | €599(促销,平时 €739) | https://www.hesaitech.com/product/jt16/ / https://openelab.io/products/hesai-jt16-mini-3d-lidar |
| Hesai XT16 | 16ch 机械旋转 360°×30° | 未确认(0.05〜120 m。兄弟机 XT32M 为 80 m @10%) | 320,000 | 800 g | **$6,650**(美国代理商) | https://www.hesaitech.com/product/xt16-32-32m/ / https://robostore.com/products/hesai-xt16-3d-lidar |
| Ouster OS0 | digital LiDAR(SPAD+ASIC)最大 128ch、垂直 90° | 35 m | 10,400,000 | 未确认 | 需询价(参考: OS1-32 发布时 $8,000) | https://ouster.com/products/hardware/os0-lidar-sensor |
| Ouster OS1 | 同上 128ch、垂直 45° | 90 m | 10,400,000 | 未确认 | 需询价 | https://ouster.com/products/hardware/os1-lidar-sensor / https://www.geoweeknews.com/articles/32-channel-lidar-for-8k-ousters-newest-lidar-finds-a-sweet-spot/ |

各论:

- **Hesai XT16**: 精度 ±1 cm(accuracy)/ 0.5 cm(1σ precision),以零盲区为卖点的工业级。面向 AGV/AMR、cm 级室内外导航(https://www.hesaitech.com/product/xt16-32-32m/)。
- **Hesai JT16**: CES 发布的面向机器人的迷你穹顶。200 g、IP6K6,是 Mid-360 的直接竞品。瞄准扫地机器人、配送机器人。
- **Ouster OS 系列**: 把接收端集成为 SPAD+定制 ASIC 的"digital LiDAR"。点密度 10.4 M pts/s 是 Mid-360 的 50 倍,但价格、质量是另一个级别。OS0 的垂直 90° FOV 在仓库机器人的地板〜天花板感知上很强。现行 Rev7/8 的精度、质量、功耗、实售价官方页面未刊载(未确认,数据手册在 https://ouster.com/downloads )。
- **Velodyne 的现状(事实已确认)**: Velodyne 于 2023-02-10 与 Ouster 完成对等合并,存续公司为 Ouster(NYSE: OUST)。原 Velodyne 股票退市(1 股 = Ouster 0.8204 股)。出处: https://investors.ouster.com/news-releases/news-release-details/ouster-and-velodyne-complete-merger-equals-accelerate-lidar / https://www.therobotreport.com/lidar-makers-ouster-velodyne-complete-merger/

#### 1.2 深度相机

##### Intel RealSense D435i(最重要·详细)

方式: 主动 IR 立体(IR 图案投射+左右 IR 相机的视差)。

| 项目 | 值 | 出处 |
|---|---|---|
| 深度 FOV | **87°×58°(官方已确认)**。数据手册精密值 87°±3° × 58°±1°(对角 95°±3°) | https://www.intel.com/content/www/us/en/products/sku/190004/intel-realsense-depth-camera-d435i/specifications.html / https://cdrdv2-public.intel.com/841984/Intel-RealSense-D400-Series-Datasheet.pdf |
| 深度范围 | 理想 0.3〜3 m(Min-Z 约 28 cm,848×480 时 0.105 m)。超过 3 m 也可但精度下降 | https://www.realsenseai.com/products/depth-camera-d435i/ |
| 深度分辨率/fps | 最大 1280×720 / 最大 90 fps | 同上 |
| 深度精度 | <2% @ 2 m | 同上 |
| RGB | 1920×1080 @30 fps(卷帘快门) | 同上 |
| IMU | **Bosch BMI055(6 轴)内置 — 已确认** | https://github.com/realsenseai/librealsense/blob/master/doc/d435i.md |
| 质量 | 约 72 g(代理商值。官方现行页面未刊载) | https://framos.com/products/3d/3d-cameras/depth-camera-d435i-bulk-22610/ |
| 尺寸/接口 | 90×25×25 mm,USB-C 3.1 Gen 1 | https://www.realsenseai.com/products/depth-camera-d435i/ |
| 价格 | **$334.00(官方商店)** | https://store.realsenseai.com/buy-intel-realsense-depth-camera-d435i.html |

RealSense 事业的现状:

- 2021 年 Intel 宣布收缩该业务,但 D400 系延续。**2025-07-11 作为 RealSense Inc. 完成从 Intel 的拆分**,Series A 融资 $50M(Intel Capital、MediaTek Innovation Fund 参与)。出处: https://www.realsenseai.com/news-insights/news/realsense-completes-spin-out-from-intel-raises-50-million-to-accelerate-ai-powered-vision-for-robotics-and-biometrics/ / https://www.tomshardware.com/tech-industry/realsense-completes-spin-out-from-intel-gets-usd50-million-in-funding-from-intel-capital-and-mediatek
- 独立后第 1 弹 = **D555**(D500 系): 搭载 Vision SoC V5(5 TOPS),PoE 供电+全局快门。出处: https://www.vision-systems.com/embedded/article/55303384/intel-completes-realsense-spinoff
- 该公司主张"被全球 60% 的 AMR/人形机器人采用"(自家发布值)。

##### 竞品深度相机

| 产品 | 方式 | 深度规格 | 价格 | 出处 |
|---|---|---|---|---|
| Orbbec Gemini 335 | 主动立体(MX6800 ASIC) | 0.1〜20 m+,1280×800@30fps,FOV 90°×65° | **$264**(官方商店) | https://store.orbbec.com/products/gemini-335 |
| Orbbec Gemini 335L | 同上·基线 95 mm·IP65 | 精度 ≤0.8% @ 2 m | $359 | https://www.hackster.io/news/orbbec-unveils-the-robust-fakra-connectable-gemini-335lg-depth-camera-for-autonomous-robots-and-more-e23d922b5158 |
| Orbbec Femto Bolt | Microsoft iToF(与 Azure Kinect 同一深度技术) | 0.25〜5.46 m,WFOV 120°×120°,RGB 4K,内置 IMU | **$418**(官方商店) | https://store.orbbec.com/products/femto-bolt |
| Stereolabs ZED 2i | 被动立体+Neural Depth | 0.2〜20 m,110° 广角,IMU+气压+磁 | $499〜(搜索结果值,需再确认) | https://store.stereolabs.com/products/zed-2i/ |
| Stereolabs ZED X | 同上(Gen2)+全局快门 | 0.3〜20 m(2.2mm)/1〜35 m(4mm),GMSL2 接口(以 Jetson 为前提) | $549〜599(搜索结果值) | https://static.generation-robots.com/media/zed-x-datasheet-v1.2.pdf |

- **Azure Kinect DK 的 EOL(事实已确认)**: Microsoft 于 2023-08 宣布停产,2023 年 10 月停售。SDK 仓库于 2024-08-22 归档。作为后继,在 Microsoft 官方合作下,Orbbec Femto Bolt/Mega 以许可方式实现 iToF 技术(与 Azure Kinect 同一深度模式,有 K4A API 兼容包装)。出处: https://hackaday.com/2023/08/26/microsoft-discontinues-kinect-again/ / https://github.com/microsoft/Azure-Kinect-Sensor-SDK/issues/1971 / https://www.orbbec.com/microsoft-collaboration/ / https://www.orbbec.com/documentation/comparison-with-azure-kinect-dk/
- Orbbec SDK 原生支持 ROS1/ROS2(https://store.orbbec.com/products/gemini-335le)。

#### 1.3 事件相机(DVS)

原理(1 行): 每个像素独立、异步地只在"亮度的对数变化超过阈值的瞬间"输出 (x, y, 时间戳, 极性) 形式的事件 — 不拍帧。出处: https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/

##### Prophesee / Sony IMX636

| 项目 | 值 | 出处 |
|---|---|---|
| 开发 | Sony(堆叠 BSI 工艺)× Prophesee(事件像素)共同开发 | https://www.prophesee.ai/2022/04/13/new-sony-imx636es-hd-sensor-realized-in-collaboration-between-sony-and-prophesee/ |
| 分辨率 / 像素间距 | **1280×720 / 4.86 μm(已确认)** | https://www.prophesee.ai/wp-content/uploads/2024/05/IMX636-Product-Brief-2024-v3.0.pdf |
| 时间分辨率 | 时间戳精度 1 μs,像素延迟 <100 μs @1000 lux(等效 >10k fps) | 同上 / https://www.prophesee.ai/event-camera-evk4/ |
| 动态范围 | **官方表述为 >86 dB(typ)/ >120 dB(低照度条件 0.08〜100,000 lux)** — "120 dB"是带测量条件的值 | https://support.prophesee.ai/portal/en/kb/articles/evk4-hd-product-brief |
| 最大事件率 | 1.06 Geps 级(Sony 公布) | https://www.sony-semicon.com/en/products/is/industry/evs.html |
| SDK | Metavision SDK(OSS 版 OpenEB) | https://github.com/prophesee-ai/openeb |
| 评估套件 EVK4 | IMX636,USB 3.0,30×30×36 mm,40 g。官方直销为报价制(未确认),台湾代理商实售 NT$175,000 ≈ **$5,400** | https://www.prophesee.ai/event-camera-evk4/ / https://store.edomtech.com/products/evk4 |

##### iniVation DVXplorer

| 项目 | 值 | 出处 |
|---|---|---|
| 分辨率 | VGA 640×480 | https://docs.inivation.com/hardware/current-products/dvxplorer.html |
| 动态范围 | 最大 110 dB | 同上 |
| 时间分辨率 | 200 μs,延迟 <1 ms,最大 165 Meps | 同上 |
| 价格 | **€3,900(商用)/ €3,400(学术)** | https://shop.inivation.com/collections/dvxplorer |

- 擅长: 高速运动(无运动模糊)、HDR 环境(隧道出入口、逆光)、低功耗、μs 级低延迟。
- 不擅长: 静止场景原理上什么也看不见(需要自身运动或主动照明)/以帧为前提的 CV、深度学习资产不能直接用,需要表示变换(voxel grid、time surface 等)/事件率依赖场景且呈突发性(带宽、处理系统须按最坏情况设计)。
- 数据率的性质: 输出依赖场景、稀疏。静止时几乎为零,激烈运动+高纹理时可尖峰到 Geps 级。
- 典型用途: 高速避障、无人机检测与追踪、高速 VO/SLAM、振动监测、低延迟抓取。

#### 1.4 IMU(MEMS)— 等级与漂移

业界惯用 4 个等级。位置误差约按时间的 3 次方增长,陀螺的 in-run bias instability 是主导项(https://www.vectornav.com/resources/detail/what-is-an-inertial-navigation-system)。

| 等级 | Gyro bias instability 大致值 | 无 GPS 惯性导航 60 秒的位置误差 | 代表用途 |
|---|---|---|---|
| 民用级 | ~100 °/h | **400 m** | 手机、无人机 FC、业余爱好 |
| 工业级 | ~10 °/h | **40 m** | 机器人、农机、AGV |
| 战术级 | ~1 °/h | **5 m** | UAV、军用、测绘 |
| 导航级 | ~0.01 °/h | **50 cm** | 飞机、舰船、潜艇 |

(出处: VectorNav 见上。注意等级定义在厂商之间没有严格标准 — https://ez.analog.com/mems/w/documents/4111/what-does-tactical-grade-mean-for-a-mems-imu )

代表器件的实际规格:

| 器件 | 等级 | Gyro bias instability | 噪声 | 价格 | 出处 |
|---|---|---|---|---|---|
| Bosch BMI088 | 民用(面向无人机) | 数据手册未记载(论坛回答告知 <2 °/h ※flyer 值) | gyro 0.014 °/s/√Hz | 数美元级(单价未确认) | https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi088-ds001.pdf |
| TDK ICM-42688-P | 民用(FPV 常用) | 数据手册未记载 | gyro 2.8 mdps/√Hz | 数美元级(未确认) | https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/ds-000347-icm-42688-p-v1.6.pdf |
| ADI ADIS16470 | 工业级 | **8 °/h** | 0.008 °/s/√Hz | **$481.53**(DigiKey) | https://www.analog.com/media/en/technical-documentation/data-sheets/adis16470.pdf / https://www.digikey.com/en/products/detail/analog-devices-inc/ADIS16470AMLZ/7932982 |
| ADI ADIS16490 | 战术级 | **1.8 °/h** | ARW 0.09 °/√h | 数千美元级(未确认) | https://www.analog.com/media/en/technical-documentation/data-sheets/adis16490.pdf |
| Honeywell HG4930 | 战术级 | **0.25 °/h** | ARW 0.04 °/√h | **$8,300〜$13,500**(DigiKey 按型号) | https://media.digikey.com/pdf/data%20sheets/honeywell%20pdfs/hg4930_perfandenvriomanual_jul2017.pdf / https://www.digikey.com/en/products/detail/honeywell-aerospace/HG4930CA51/6562993 |

- 总结: 民用→战术,价格差 3 个数量级,bias instability 改善 2 个数量级以上。无 GPS 60 秒为 400 m vs 5 m。
- 采用例: Pixhawk 6X(Rev 8)为 ICM-45686 ×3 的三重冗余 — 以民用级 IMU 的冗余构成+融合来运用(https://www.getfpv.com/electronics/flight-controllers/holybro-pixhawk-6x-fc-v2a-standard-set-icm-45686.html)。Unitree G1 仅公布"6 轴 IMU",型号、等级未确认(https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications)。
- 典型用途: 姿态估计、LIO/VIO 的 predict 步。腿式机器人的关键是落地冲击(高带宽、饱和)的对策(后述 Point-LIO)。

#### 1.5 力/扭矩、足底、触觉

##### 6 轴 F/T 传感器

| 产品 | 原理 | 规格 | 价格 | 出处 |
|---|---|---|---|---|
| ATI(现 Novanta)Axia80 | 硅应变片(箔式应变片 75 倍的信号强度) | 力 ~500 N / 扭矩 ~20 Nm,过载耐受 5〜12.5 倍,EtherCAT/Ethernet | 报价制(未确认。市场上据称数千美元级) | https://ati.novanta.com/product/axia80-force-torque-sensor-kit/ |
| Robotiq FT 300-S | "wear-free sensing technology"(是否电容式官方未明记=未确认) | ±300 N / ±30 Nm,100 Hz,IP65,过载 500% | 套件 **$5,720**(代理商) | https://robotiq.com/products/ft-300-force-torque-sensor / https://www.kingbarcode.com/FTS-300-S-KIT-001 |

##### 人形足底的触地检测 — 3 方式比较

| 方式 | 可得信息 | 长处 | 短处 | 采用例 |
|---|---|---|---|---|
| 脚踝 6 轴 F/T | 地面反力 3 力+3 力矩 → 直接算出 ZMP | 最适合 ZMP 控制、高精度 | 昂贵、重、怕落地冲击/EMI | ASIMO、HRP-4 等(基于研究文献: https://www.researchgate.net/publication/257672554_Signal_Processing_and_Application_of_Six-axis_ForceTorque_Sensor_Integrated_in_Humanoid_Robot_Foot ) |
| 足底分布压(FSR/压力垫) | 法向的压力分布 | 便宜、薄、可知触地面形状 | 剪切力/力矩不可测,迟滞 | 业余/研究机广泛使用(个别一次来源未确认) |
| 关节电流(扭矩)推定 | 从关节扭矩推定外力 | 无需额外传感器、成本 0 | 减速器摩擦限制精度 | 近年量产人形的主流倾向 |

- **Unitree G1**: 公布规格中无足底力传感器的记载(传感器表只有 Depth 相机/3D LiDAR/麦克风/关节编码器/IMU)→ 触地判定推测为关节侧推定(断定未确认)。出处: https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications

##### 触觉皮肤

| 产品 | 原理 | 状况·价格 | 出处 |
|---|---|---|---|
| GelSight Mini | 视触觉(用相机拍摄凝胶变形) | **$499**(更换凝胶 $49)一般在售。研究中最普及 | https://www.gelsight.com/gelsightmini/ |
| Meta Digit 360 | 指尖全周的视触觉+多模态(1 mN 的力检测) | GelSight 制造。2024-10 发布,价格未公布(未确认) | https://www.businesswire.com/news/home/20241031980322/en/GelSight-and-Meta-AI-Introduce-Digit-360-Tactile-Sensor |
| uSkin(XELA Robotics) | 磁式 3 轴(法向+剪切)高密度分布 | 商用展开中(2025-12 集成 Tesollo DG-5F,CES 2026 演示)。价格未公布 | https://roboticsandautomationnews.com/2025/12/04/xela-robotics-adds-high-precision-tactile-sensing-to-tesollo-robot-hand/97352/ |

#### 1.6 其他(简洁)

- **ToF 相机**: 调制光的相位差全像素同时测距。Orbbec Femto Bolt 系统误差 <11 mm + 距离的 0.1%,σ≤17 mm(https://www.orbbec.com/products/tof-camera/femto-bolt/)。强在室内的致密深度,弱点是直射阳光、黑色低反射、多径。
- **超声波**: HC-SR04 量程 2 cm〜4 m,分辨率 0.3 cm,数美元(https://www.dfrobot.com/blog-13482.html)。对光学式不擅长的透明物、玻璃有反应是差异化点。
- **GNSS/RTK**: u-blox ZED-F9P 在 RTK 时水平 1 cm(单独 2.5 m)。SparkFun 板 $259.95(https://www.sparkfun.com/sparkfun-gps-rtk2-board-zed-f9p-qwiic-gps-15136.html)。要 cm 级必须有基准站或 NTRIP 补正。最适合室外实验取地面真值。
- **关节编码器**: 绝对值式 17 bit = 131,072 分割/转,23 bit = 约 839 万分割(https://www.dynapar.com/knowledge/encoder-basics/encoder-resolution/single-turn-vs-multi-turn-encoders/)。人形关节以绝对值式为主流。Unitree G1 每个关节为双编码器(电机侧+输出侧)(https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications)。

---

### 2. 多传感器融合方法的梳理

**面向文章的摘要(5 行)**

1. 融合的经典是"按各传感器的误差特性(协方差)加权的逐次贝叶斯估计"= 卡尔曼滤波(EKF/UKF),ROS 的 robot_localization 是事实标准实现。
2. LiDAR-惯性里程计(LIO。累计移动量得出自身位置的方法)从因子图的 LIO-SAM(2020)→ 迭代 EKF+ikd-Tree 的 FAST-LIO2(2021,100 Hz)→ 逐点更新的 Point-LIO(2023,4〜8 kHz)一路演进,且都官方提供 Mid-360 对应配置。
3. 学习路线上,把相机+LiDAR 在鸟瞰(BEV)特征空间里混合的 BEVFusion(2022),以及训练中把某 1 路传感器整个丢弃的 modality dropout 鲁棒化,是主要潮流。
4. 腿式机器人的金字塔是 teacher-student 蒸馏: 把在仿真内观看特权信息(接触力、地形)的教师,蒸馏为只用实机可用的本体感受的学生(Lee et al. 2020 / Miki et al. 2022, Science Robotics)。
5. 实机人形分为"LiDAR+深度相机派"(Unitree、Agility)与"相机纯化派"(Tesla、Figure)两派,量产版 Atlas 撤下 LiDAR 的报道暗示其向相机派合流。

#### 2.1 经典: 卡尔曼滤波与因子图

##### EKF / UKF

| 项目 | EKF | UKF |
|---|---|---|
| 非线性的处理 | 用雅可比做 1 次线性化 | 让 sigma 点直接通过非线性函数(Unscented 变换) |
| 长处 | 轻、实绩庞大 | 2 阶精度、无需推导雅可比 |
| 短处 | 强非线性、大姿态误差下容易发散 | 略重 |

- 典型构成: IMU(高速率、有漂移)做预测,编码器、GNSS(绝对、低速率)作为观测进行统合。ROS 标准实现 = robot_localization(EKF/UKF 双支持): https://github.com/cra-ros-pkg/robot_localization
- 本质: 把互补的传感器按误差协方差加权混合的逐次贝叶斯估计。
- 书志: Kalman 1960 为原典,UKF 为 Julier & Uhlmann 1997(一次 URL 未确认)。

##### 因子图 / LIO 谱系

| 方法 | 年份/作者 | 要点 | 性能主张 | URL |
|---|---|---|---|---|
| GTSAM | Georgia Tech Borg Lab(iSAM2 为 Kaess et al., IJRR 2012) | 因子图+贝叶斯树的 C++ 基础设施。提供 IMU 预积分 factor | 以 iSAM2 做增量更新 | https://github.com/borglab/gtsam |
| LIO-SAM | 2020 IROS / Tixiao Shan 等(MIT/Stevens) | 用因子图形式化 LiDAR-惯性(使用 GTSAM)。回环、GPS 可作为 factor 追加 | 实时的高精度轨迹+地图 | https://github.com/TixiaoShan/LIO-SAM / https://arxiv.org/abs/2007.00258 |
| FAST-LIO2 | 2021 arXiv / 2022 T-RO / Wei Xu, Fu Zhang 等(HKU MARS) | 不做特征提取、直接配准原始点云。tightly-coupled 迭代 EKF+增量 kd 树 ikd-Tree | "比 SOTA 高精度且大幅降低计算负荷""最大 100 Hz" | https://github.com/hku-mars/FAST_LIO / https://arxiv.org/abs/2107.06829 |
| Point-LIO | 2023 Advanced Intelligent Systems / He, Xu, Zhang 等(HKU MARS) | 逐点更新状态,在原理上消除帧内畸变。把 IMU 作为"输出"来处理,饱和之下也能持续估计 | 4〜8 kHz 里程计,角速度 75 rad/s 的激烈运动下也工作 | https://github.com/hku-mars/Point-LIO / https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202200459 |

- **Mid-360 对应**: FAST-LIO 仓库有官方 `config/mid360.yaml`(https://github.com/hku-mars/FAST_LIO/blob/main/config/mid360.yaml),Point-LIO 同系也提供 Mid-360 配置 — G1 标配的 Mid-360 开箱即得 LIO 的生态已经齐备。
- 使用区分的行情观: 想要回环、GPS 统合 → LIO-SAM / 计算资源紧、高速机动 → FAST-LIO2 / 腿式机器人足部触地冲击那样的振动、激烈运动 → Point-LIO。

#### 2.2 学习路线

##### BEV 融合

| 论文 | 出处 | 要点 | URL |
|---|---|---|---|
| BEVFusion(MIT 版) | MIT Han Lab, 2022(ICRA 2023) | 把相机、LiDAR 两种特征带入共享 BEV 空间融合。BEV pooling 优化把 view 变换加速 40 倍以上。支持多任务 | https://arxiv.org/abs/2205.13542 / https://github.com/mit-han-lab/bevfusion |
| BEVFusion(PKU 版·同名另一篇) | 北京大学+Alibaba, NeurIPS 2022 | 相机流与 LiDAR 流各自独立 BEV 化后融合。含 LiDAR 故障模拟的训练,主张 SOTA +15.7〜28.9% mAP | https://arxiv.org/abs/2205.13790 / https://github.com/ADLab-AutoDrive/BEVFusion |

##### 模态 dropout(对传感器缺失的鲁棒化)

- 思路: 普通的 dropout 消掉神经元,而这里在训练中把某 1 路传感器整个丢掉(填零/掩码)→ 学到"用剩下的传感器补上"的内部表示,耐受实际运用中的传感器故障、遮挡。概述: https://www.emergentmind.com/topics/modality-dropout
- 代表例: PKU 版 BEVFusion 的含故障训练(见上)/ MoME(2025,报告相机全损时仍维持 NDS 87.9% — https://arxiv.org/abs/2503.19776)/ 先行例 Sensor Dropout(Liu et al., CoRL 2017 — https://arxiv.org/abs/1705.10422 ,细节未确认)。

##### Privileged learning / Teacher-Student 蒸馏(腿式机器人的金字塔)

| 论文 | 书志 | 要点 | URL |
|---|---|---|---|
| Lee et al. "Learning quadrupedal locomotion over challenging terrain" | Science Robotics Vol.5, Issue 47, eabc5986, 2020-10-21 | 教师用只有仿真内才能得到的特权信息(触地状态、接触力、地形形状、摩擦)做 RL 训练 → 学生只用实机可用的本体感受(关节角、IMU)的历史来模仿教师。盲眼的 ANYmal 踏破泥、雪、植被、瓦砾 | https://doi.org/10.1126/scirobotics.abc5986 / https://arxiv.org/abs/2010.11251 |
| Miki et al. "Learning robust perceptive locomotion for quadrupedal robots in the wild" | Science Robotics Vol.7, Issue 62, eabk2822, 2022 | 用基于 attention 的递归 belief state encoder 统合外受感觉(高度图)+本体感受。外界传感器不可靠的场合自动把权重移向本体感受一侧 ="学到的融合门"。ANYmal 完成阿尔卑斯登山道 1 小时路线 | https://www.science.org/doi/10.1126/scirobotics.abk2822 |

- 向人形的引进例: Humanoid Parkour Learning(Zhuang et al., CoRL 2024)把蒸馏策略 zero-shot 移植到 Unitree H1(https://arxiv.org/abs/2406.10759)。ExBody2 用 teacher-student 蒸馏做 H1/G1 的全身跟踪(据称为 arXiv:2412.13196,一次确认未完成)。四足上确立的构图,正原样流入 2024〜2026 的人形 RL 行走。

#### 2.3 实机人形的传感器构成(公开信息)

| 机体 | 传感器构成(公开部分) | 出处 | 备注 |
|---|---|---|---|
| Unitree G1 | 官方规格表为"Depth Camera + 3D LiDAR"+4ch 麦克风阵列+扬声器 | https://www.unitree.com/g1 | **官方未明记型号**。Livox Mid-360 + RealSense D435(i) 的型号是代理商/技术文档一侧的记载(https://docs.quadruped.de/projects/g1/html/g1_overview.html) |
| Unitree H1 | 官方: "3D LIDAR + Depth Camera 的 360° 深度感知" | https://www.unitree.com/h1 | 型号官方未记载(流通信息为 Mid-360 + D435i) |
| Tesla Optimus | 以相机为中心(Autopilot 系视觉)+指尖触觉+足底力/扭矩。"8 相机"为第三方评测值,官方一次来源未确认 | https://briandcolwell.com/a-complete-review-of-teslas-optimus-robot/ | 不搭载 LiDAR 的相机纯化路线 |
| Figure 02 / 03 | 02: RGB 相机 6 台+VLM(6 台的一次页面明记未确认)。03: 官方发布手掌相机+触觉传感器 | https://www.figure.ai/news/introducing-figure-03 | 无 LiDAR、视觉+触觉路线 |
| Boston Dynamics 新 Atlas(电动) | 2024 研究机: ToF+RGB-D/立体+LiDAR,IMU 1 kHz、关节编码器 4 kHz(第三方汇总)。据报道 2026 量产版撤下 LiDAR,改为 360° 相机+触觉构成 | https://www.aparobot.com/robots/atlas | 不存在官方的一次传感器规格书(按未确认处理) |
| Agility Digit | Velodyne VLP-16(躯干顶部)+ RealSense 深度相机×4(含骨盆前后的 D430 ×2)。LiDAR=远方地图/障碍物,深度相机=脚下的面估计 | https://robotsguide.com/robots/digit / https://agilityrobotics.com/content/check-out-these-big-advancements-in-digits-development | LiDAR+深度这一经典融合构成的代表 |

观察: 业界分两派 — ① LiDAR+深度相机派(Unitree、Agility、研究版 Atlas): 可原样使用 §2.1 的 LIO 资产。② 相机纯化派(Tesla、Figure): 用学习路线(§2.2)估计几何。量产 Atlas 撤下 LiDAR 暗示向②合流。

#### 2.4 "在哪一层混合"— early / mid / late fusion(3 段通俗讲解)

##### ① 比喻(做菜)

- **Early fusion(用生数据混合)** = 把所有材料从一开始就放进同一口锅。食材彼此充分交融,但只要有一样坏了,整锅报废。
- **Mid fusion(用特征混合)** = 各种材料分别做好预处理后再合起来。容易合,奇怪的材料在预处理阶段就能发现。
- **Late fusion(用结论混合)** = 3 位厨师各自做出成品,评委多数决。一人失手也能挽回,但食材之间的化学反应不会发生。

##### ② 工程学说明

| 层 | 混合的对象 | 长处 | 短处 |
|---|---|---|---|
| Early(raw) | 原始点云、原始像素、原始 IMU 值 | 信息损失为零。最大限度利用相关(例: Point-LIO 对每 1 个 LiDAR 点都与 IMU 做状态更新) | 对时刻同步、外参标定极其敏感。速率差(IMU 数百 Hz vs 相机 30 Hz)难以吸收。1 个传感器的故障污染全体 |
| Mid(特征) | 特征图、BEV 特征、嵌入 | 各模态用最优编码器的同时做致密融合。BEVFusion 与 Miki 2022 的 belief encoder 都在这一层 | 需要设计共同表示空间。对训练分布外的缺失弱 → 用 modality dropout 补强 |
| Late(判断) | 各系统的估计结果(位置、检测、判定) | 模块独立,开发、验证、更换容易。故障隔离自然(用 EKF 统合 LIO 输出+GNSS+里程计就在这一层) | 各系统丢掉的信息回不来。判断分歧时的仲裁困难 |

##### ③ 实现上的考虑

- **时刻同步是一切的地基**: 越往 early 越需要 PTP/硬件触发级的同步。Mid-360 内置 IMU、已同步,所以 early fusion(LIO)好做。
- **标定误差的传播**: early/mid 中,传感器间外参的误差会以特征空间"晕染"的形式污染学习。late 在各系统内部闭合。
- **故障模式设计**: late 容易设计降级运行(LiDAR 死亡→仅相机减速继续)。想在 mid 得到同等鲁棒性,训练时必须加入 modality dropout(PKU 版 BEVFusion 的教训)。
- **计算预算与速率**: early 以最快传感器的速率运转(Point-LIO 4〜8 kHz)。直连控制回路的状态估计用 early/经典,语义理解用 mid/学习,行为判断、冗余化用 late — 按层分工的混合是实机的定石(例: G1 = Mid-360+IMU 用 FAST-LIO2 做 early 融合 → 深度相机的检测在 mid/late 叠加)。

---

### 3. 市场动向(2024〜2026)

**面向文章的摘要(5 行)**

1. 人形机器人市场预测,从 Goldman Sachs"2035 年 380 亿美元"(2024 年上调至此前的 6 倍),到 Morgan Stanley"2050 年 5 万亿美元 TAM"、Citi"2050 年 7 万亿美元",投行之间有接近 2 个数量级的幅度。
2. 中国工信部已于 2023-11 公布"2025 年量产、2027 年世界先进水平"的产业政策,中商产业研究院估计 2025 年中国出货 1.44 万台=全球的 84.7%(2026 年时点)。
3. LiDAR 的价格破坏进行中 — Mid-360 $749、Unitree L1 $249,Hesai 量产"约 $200 的 ATX",2025 年出货指引 120〜150 万台。Yole 以"不是出货减少而是单价急跌"为由下调了金额预测。
4. 事件相机的旗手 Prophesee 于 2024-10 进入司法重整 → CEO 更替 → 2026-06 融资 €20M+发布无人机检测系统 Mantara,实现自主重建(并非被收购)。
5. 北京于 2025-04 举办世界首个人形机器人半程马拉松(冠军: 天工 Ultra,2:40:42),2025-08 举办第 1 届世界人形机器人运动会(16 国、500 台以上),2026-04 的第 2 届马拉松上机器人跑出超过人类世界纪录的 50 分 26 秒,第 2 届运动会于 2026-08-22 开幕(2,056 台)。
