## 付録 B: ロボット名鑑 — Menagerie 全 67 モデル棚卸し

「全種類のロボットを動かしたい」という野望のため、MuJoCo Menagerie 収録の全モデルを実際にロードして物理ステップまで回す棚卸しを行いました。結果: **67 モデル中 67 モデルがロード成功・シミュレーション実行成功、失敗ゼロ**。つまり Menagerie は「素材としては全機が即戦力」で、ボトルネックはモデルではなく制御則・報酬・参照モーションの側にあります。


![選手名鑑 1](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/menagerie_gallery_humanoid.png)
*図: Menagerie 実測レンダリング(ヒューマノイド+筋骨格 15 体)*

![選手名鑑 2](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/menagerie_gallery_quadruped_drone.png)
*図: Menagerie 実測レンダリング(四足+ドローン 10 体)*

![選手名鑑 3](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/menagerie_gallery_arm_mobile.png)
*図: Menagerie 実測レンダリング(アーム+双腕+移動マニピュレータ 33 体)*

![選手名鑑 4](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/menagerie_gallery_hand_gripper.png)
*図: Menagerie 実測レンダリング(ハンド+グリッパ 9 体)*

### B.1 種別内訳(実測 67 モデル)

| 種別 | 数 | 代表 |
|---|---|---|
| ヒューマノイド(二足) | 12 | Unitree G1/H1、Booster T1、Fourier N1、Apptronik Apollo、PAL Talos、Agility Cassie、Berkeley Humanoid、Robotis OP3、PND Adam Lite、ToddlerBot ×2 |
| 四足 | 8 | ANYmal B/C、Boston Dynamics Spot、Google Barkour v0/vB、Unitree A1/Go1/Go2 |
| アーム(単腕) | 22 | Franka Panda/FR3、KUKA iiwa14、UR5e/UR10e、Kinova Gen3、xArm7、ViperX ほか |
| 双腕 | 2 | ALOHA、Trossen WXAI |
| 移動マニピュレータ | 7 | Hello Robot Stretch ×2、PAL TIAGo ×2、Google Robot、TidyBot、Rainbow RBY1 |
| 多指ハンド | 6 | Shadow Hand、LEAP Hand、Allegro、Shadow DEX-EE ほか |
| グリッパ | 3 | Robotiq 2F-85 ×2、UMI Gripper |
| ドローン | 2 | Crazyflie 2、Skydio X2 |
| 筋骨格/生物 | 2 | MS-Human-700(700 筋)、flybody(ハエ) |
| その他 | 3 | サッカーキット、RealSense D435i(センサ資材)、IIT SoftFoot(足部品) |

![名鑑統計](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_roster_stats.png)
*図: 67 機の種別・アクチュエータ型・keyframe 有無の実測集計(棚卸し JSON より作図)*

### B.2 棚卸しで見えた「動かすための地図」

![Go2 ポートレート](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_go2.png)
*図: Unitree Go2(シミュレーションレンダ)*

![Spot ポートレート](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_spot.png)
*図: Boston Dynamics Spot(シミュレーションレンダ)*

- **四足 8 機種は全て同型(自由度 18・駆動 12)。** つまり 1 本の学習パイプラインを書けば 8 機種を横並びでスイープできます。四足の部は運動会の団体種目に最適。
- **アーム 22 本は「倒れない」ので、逆運動学(IK。手先の目標位置から関節角を逆算する計算)を当てるだけで即デモが作れる。** 微分 IK ライブラリ(mink、Apache-2.0)のサンプルが事実上の Menagerie デモ集になっています。
- **home 姿勢(keyframe)が無いモデルが 19 体。** 全機お披露目の最初の「素材づくり」は、立ち姿勢の自作というやや地味な作業です。
- **要注意個体**: Cassie は閉リンク機構で GPU 並列(MJX)に制約。多指ハンドは腱駆動や劣駆動で「関節数と指令数が一致しない」前提の設計が必要。
- **ヒューマノイド 12 体には、トルク直結型(H1、Talos 等)と位置サーボ型(G1、T1 等)がある。** 本編の H1 対応では、トルク型を位置サーボ化するアダプタを書いてこの差を吸収しました(G1 の報酬 11 箇条をそのまま移植するため)。

### B.3 学習資源の 2 本柱と、ライセンスの地雷原

OSS の学習環境は、(1) **MuJoCo Playground**(Apache-2.0。四足・二足の移動 9 機種+マニピュレーション 4 機種の学習環境と設定)と (2) **LocoMuJoCo**(MIT。22,000 本超のリターゲット済みモーション配布、ヒューマノイド 10+四足 4)が 2 本柱で、相互補完の関係にあります。

そして棚卸し最大の収穫が**モーションデータのライセンス地図**でした。

| データ源 | 内容 | ライセンス |
|---|---|---|
| AMASS | SMPL 統一の大規模モーキャプ集成 | **非商用限定(商用のニューラルネット学習も禁止)** |
| LAFAN1(本記事の教師) | 4.6 時間の高品質モーキャプ | **CC BY-NC-ND(非商用・改変禁止)** |
| CMU Mocap | 2,600+ シーケンス | **無償・商用可**(転売のみ禁止) |
| GMR(汎用リターゲッタ) | SMPL-X/BVH/動画 → ロボット 18 機種 | **MIT** |

趣味の運動会なら LAFAN1 で問題ありませんが、この技術を製品に近づけていくなら、**「CMU mocap(商用可)+ GMR(MIT)」の組み合わせがいちばんクリーンな系譜**になります。データのライセンスは、コードのライセンスより見落とされがちで、しかも後から差し替えが利きにくい — これも産業側の感覚が役立った点でした。

### B.4 全 67 モデル実測表

67 機ぶんの「体格測定の結果」です。nq=一般化座標の数(自由度+クォータニオン分)、nv=速度自由度、nu=駆動指令の数。アクチュエータ型の意味は本編と B.2 のとおりで、自由関節が「あり」の機体は転倒がある(=バランスが競技になる)機体です。keyframe は同梱の基準姿勢。全行、実際にロードして物理ステップを回して採った値です。

| モデル | nq | nv | nu | アクチュエータ | 自由関節 | keyframe | メッシュ数 | ライセンス |
|---|---|---|---|---|---|---|---|---|
| `agilex_piper` | 8 | 8 | 7 | position+kv×7 | なし | home | 82 | MIT |
| `agility_cassie` | 35 | 32 | 10 | motor×10 | あり | home | 25 | custom/see LICENSE |
| `aloha` | 16 | 16 | 14 | position×12, position+kv×2 | なし | neutral_pose | 24 | custom/see LICENSE |
| `anybotics_anymal_b` | 19 | 18 | 12 | position×12 | あり | なし | 46 | custom/see LICENSE |
| `anybotics_anymal_c` | 19 | 18 | 12 | position×12 | あり | なし | 24 | custom/see LICENSE |
| `apptronik_apollo` | 39 | 38 | 32 | position×32 | あり | stand | 44 | Apache-2.0 |
| `arx_l5` | 8 | 8 | 7 | position+kv×7 | なし | home | 10 | BSD |
| `berkeley_humanoid` | 19 | 18 | 12 | position+kv×12 | あり | home | 13 | custom/see LICENSE |
| `bitcraze_crazyflie_2` | 7 | 6 | 4 | motor×4 | あり | hover | 39 | MIT |
| `booster_t1` | 30 | 29 | 23 | position+kv×23 | あり | home | 24 | Apache-2.0 |
| `boston_dynamics_spot` | 19 | 18 | 12 | position+kv×12 | あり | home | 23 | BSD |
| `dynamixel_2r` | 2 | 2 | 2 | position+kv×2 | なし | なし | 15 | custom/see LICENSE |
| `flexiv_rizon4` | 7 | 7 | 7 | position+kv×7 | なし | home | 14 | Apache-2.0 |
| `flexiv_rizon4s` | 7 | 7 | 7 | position+kv×7 | なし | home | 14 | Apache-2.0 |
| `flybody` | 109 | 108 | 78 | position×64, motor×6, adhesion×8 | あり | key0 | 85 | Apache-2.0 |
| `fourier_n1` | 30 | 29 | 23 | motor×23 | あり | home | 29 | Apache-2.0 |
| `franka_emika_panda` | 9 | 9 | 8 | position+kv×8 | なし | home | 67 | Apache-2.0 |
| `franka_fr3` | 7 | 7 | 7 | position+kv×7 | なし | home | 36 | Apache-2.0 |
| `franka_fr3_v2` | 7 | 7 | 7 | position+kv×7 | なし | home | 37 | Apache-2.0 |
| `google_barkour_v0` | 19 | 18 | 12 | position+kv×12 | あり | standing | 14 | Apache-2.0 |
| `google_barkour_vb` | 19 | 18 | 12 | position+kv×12 | あり | home | 11 | Apache-2.0 |
| `google_robot` | 9 | 9 | 9 | position×9 | なし | なし | 47 | Apache-2.0 |
| `hello_robot_stretch` | 31 | 29 | 8 | motor×2, position+kv×3, position×3 | あり | なし | 67 | BSD |
| `hello_robot_stretch_3` | 41 | 38 | 10 | velocity×2, position+kv×3, position×5 | あり | home、stow | 85 | Apache-2.0 |
| `i2rt_yam` | 8 | 8 | 7 | position+kv×7 | なし | home | 17 | MIT |
| `iit_softfoot` | 93 | 93 | 1 | position×1 | なし | なし | 10 | custom/see LICENSE |
| `kinova_gen3` | 7 | 7 | 7 | position+kv×7 | なし | home、retract | 8 | custom/see LICENSE |
| `kuka_iiwa_14` | 7 | 7 | 7 | position+kv×7 | なし | home | 13 | BSD |
| `leap_hand` | 16 | 16 | 16 | position+kv×16 | なし | なし | 11 | custom/see LICENSE |
| `low_cost_robot_arm` | 6 | 6 | 6 | position+kv×6 | なし | home | 22 | Apache-2.0 |
| `ms_human_700` | 85 | 85 | 700 | muscle×700 | なし | init | 189 | Apache-2.0 |
| `pal_talos` | 51 | 50 | 32 | motor×32 | あり | key0 | 74 | Apache-2.0 |
| `pal_tiago` | 29 | 28 | 14 | motor×7, position×5, velocity×2 | あり | なし | 21 | Apache-2.0 |
| `pal_tiago_dual` | 32 | 31 | 25 | velocity×4, position×7, motor×14 | あり | なし | 25 | Apache-2.0 |
| `pndbotics_adam_lite` | 32 | 31 | 25 | motor×25 | あり | なし | 73 | MIT |
| `rainbow_robotics_rby1` | 35 | 34 | 26 | velocity×2, position+kv×24 | あり | なし | 47 | Apache-2.0 |
| `realsense_d435i` | 0 | 0 | 0 | — | なし | なし | 9 | Apache-2.0 |
| `rethink_robotics_sawyer` | 7 | 7 | 7 | position+kv×7 | なし | home | 49 | Apache-2.0 |
| `robot_soccer_kit` | 71 | 70 | 4 | velocity×3, position+kv×1 | あり | なし | 29 | custom/see LICENSE |
| `robotiq_2f85` | 15 | 14 | 1 | position+kv×1 | あり | なし | 8 | custom/see LICENSE |
| `robotiq_2f85_v4` | 13 | 12 | 1 | position+kv×1 | あり | なし | 8 | custom/see LICENSE |
| `robotis_op3` | 27 | 26 | 20 | position×20 | あり | なし | 48 | Apache-2.0 |
| `robotstudio_so101` | 6 | 6 | 6 | position+kv×6 | なし | なし | 18 | Apache-2.0 |
| `shadow_dexee` | 12 | 12 | 12 | motor×12 | なし | なし | 26 | Apache-2.0 |
| `shadow_hand` | 31 | 30 | 20 | position×20 | あり | なし | 13 | Apache-2.0 |
| `sharpa_wave` | 22 | 22 | 22 | position+kv×22 | なし | なし | 54 | Apache-2.0 |
| `skydio_x2` | 7 | 6 | 4 | motor×4 | あり | hover | 1 | Apache-2.0 |
| `stanford_tidybot` | 18 | 18 | 11 | position+kv×11 | なし | home、retract | 20 | MIT |
| `tetheria_aero_hand_open` | 16 | 16 | 7 | position×7 | なし | home | 27 | Apache-2.0 |
| `toddlerbot_2xc` | 51 | 50 | 30 | motor×30 | あり | home | 47 | MIT |
| `toddlerbot_2xm` | 51 | 50 | 30 | motor×30 | あり | home | 47 | MIT |
| `trossen_vx300s` | 8 | 8 | 7 | position×7 | なし | home | 10 | custom/see LICENSE |
| `trossen_wx250s` | 8 | 8 | 7 | position+kv×7 | なし | home | 10 | custom/see LICENSE |
| `trossen_wxai` | 16 | 16 | 14 | position×14 | なし | left/、right/ | 84 | BSD |
| `trs_so_arm100` | 6 | 6 | 6 | position+kv×6 | なし | home、rest | 18 | Apache-2.0 |
| `ufactory_lite6` | 6 | 6 | 6 | position+kv×6 | なし | home | 14 | custom/see LICENSE |
| `ufactory_xarm7` | 13 | 13 | 8 | position+kv×8 | なし | home | 16 | custom/see LICENSE |
| `umi_gripper` | 8 | 8 | 7 | position×1, position+kv×6 | なし | なし | 6 | MIT |
| `unitree_a1` | 19 | 18 | 12 | position×12 | あり | home | 5 | BSD |
| `unitree_g1` | 36 | 35 | 29 | position+kv×29 | あり | stand | 35 | custom/see LICENSE |
| `unitree_go1` | 19 | 18 | 12 | position×12 | あり | home | 5 | BSD |
| `unitree_go2` | 19 | 18 | 12 | motor×12 | あり | home | 16 | custom/see LICENSE |
| `unitree_h1` | 26 | 25 | 19 | motor×19 | あり | home | 21 | custom/see LICENSE |
| `unitree_z1` | 6 | 6 | 6 | position+kv×6 | なし | home | 7 | BSD |
| `universal_robots_ur10e` | 6 | 6 | 6 | position+kv×6 | なし | home | 20 | custom/see LICENSE |
| `universal_robots_ur5e` | 6 | 6 | 6 | position+kv×6 | なし | home | 20 | custom/see LICENSE |
| `wonik_allegro` | 23 | 22 | 16 | position×16 | あり | なし | 11 | custom/see LICENSE |


## 付録 C: センサ図鑑 — スペック・長所短所・フュージョン・市場動向

観測設計はセンサ選定である、という本編の主張を支える資料編です。

![センサ比較レーダー](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_sensor_compare.png)
*図: 主要 5 センサの特性比較(付録 C の実スペック表からの定性要約)。万能なセンサは無い — だから混ぜる(フュージョン)ことになる*

数値は 2026-08 時点の調査で、各項目に出典を付けています(公式データシート優先。確認できなかった値は「未確認」のまま残しています — 推測で埋めるより、埋まっていないことがわかる方が資料として誠実だからです)。

### 1. 主要センサのスペックと長所・短所

**記事向け要約(5 行)**

1. ヒューマノイドの「眼」は 1 種類では成立しない — LiDAR(正確な距離)、深度カメラ(密な近距離 3D)、IMU(姿勢)、関節エンコーダ(自分の体)を重ねて初めて世界が見える。
2. Livox Mid-360 は 360°×(-7°〜+52°) FOV・20 万点/秒・265 g・実勢 $750〜900 で、研究用ロボット LiDAR のデファクトになった(1 桁上の産業級 Hesai XT16 は $6,650)。
3. Intel RealSense D435i は 87°×58° FOV のアクティブ IR ステレオ+IMU 内蔵 $334 で、2025 年に Intel からスピンオフした RealSense Inc. が D500 系へ更新中。
4. イベントカメラ(Sony IMX636)は μs 級の時間分解能と 120 dB(低照度条件)のダイナミックレンジを持つが、評価キットは依然数十万円級で「次の主役候補」段階。
5. IMU は等級で価格が 3 桁違う(民生 数ドル → 戦術級 $8,000 超)一方、GPS なし 60 秒の位置誤差は 400 m → 5 m と 2 桁縮む — 脚ロボは民生〜産業級 IMU+他センサ融合で戦うのが定石。

#### 1.0 横断比較表(ヒューマノイド搭載観点)

| センサ | 原理(1 行) | 得意 | 苦手 | 代表機種と価格帯 | 典型用途 |
|---|---|---|---|---|---|
| 回転式/半球 LiDAR | レーザー飛行時間(ToF)で距離を直接測る | 距離精度(cm 級)・暗闇・広 FOV | 雨/霧/雪、黒色低反射面、ガラス | Livox Mid-360 $749〜/ Unitree L2 $419 / Hesai XT16 $6,650 | SLAM・障害物回避・全周知覚 |
| 深度カメラ(アクティブ IR ステレオ) | IR パターン投光+左右カメラ視差で深度 | 近距離の密な 3D、安価、RGB 同時取得 | 直射日光(IR が負ける)、遠距離、透明/鏡面 | RealSense D435i $334 / Orbbec Gemini 335 $264 | 足元の地形・マニピュレーション |
| ステレオカメラ(パッシブ) | 左右カメラの視差のみで深度(+近年はニューラル深度) | 屋外・長基線で中距離、投光不要 | 無テクスチャ面(白壁)、暗所 | ZED 2i $499〜 / ZED X $549〜(検索結果値) | 屋外ナビ・車載型知覚 |
| ToF カメラ | 変調光の位相差で全画素同時に距離 | 屋内の密な深度、広 FOV | 直射日光、黒色低反射、マルチパス | Orbbec Femto Bolt $418 | 屋内マッピング・ジェスチャ |
| イベントカメラ(DVS) | 画素ごとに輝度変化の瞬間だけ非同期出力 | 高速運動・HDR(逆光/トンネル)・低レイテンシ | 静止シーン(何も出ない)、既存 CV 資産が使えない | Prophesee EVK4 ≈$5,400(代理店)/ iniVation DVXplorer €3,900 | 高速回避・ドローン検知・振動監視 |
| IMU(MEMS) | 角速度と加速度の慣性計測 | 高レート(kHz 級)・自己完結 | ドリフト(単独では位置が発散) | BMI088 数ドル級 / ADIS16470 $482 / HG4930 $8,300〜 | 姿勢推定・LIO/VIO の背骨 |
| 6 軸 F/T センサ | ひずみゲージ等で 3 力+3 モーメント | ZMP 直接算出・力制御 | 高価・衝撃/EMI に弱い | ATI Axia80(見積制)/ Robotiq FT 300-S キット $5,720 | 足首の床反力・把持力制御 |
| 触覚スキン | ゲル変形の撮像(視触覚)や磁気式 3 軸分布 | すべり検知・微細形状・材質 | 面積あたりコスト・配線・耐久 | GelSight Mini $499 / Meta Digit 360(価格未公表) | 指先の把持・接触操作 |
| 超音波 | 音波の往復時間 | 透明物・ガラスも見える、数ドル | 分解能が粗い、指向性が広い | HC-SR04 数ドル | 近接バンパー的用途 |
| GNSS/RTK | 衛星測位+基準局補正 | 屋外で絶対位置 cm 級 | 屋内・都市谷間は不可 | u-blox ZED-F9P ボード $259.95 | 屋外ナビ・グラウンドトゥルース |
| 関節エンコーダ | 磁気/光学で関節角を直読 | 高分解能(17〜23 bit)・低遅延 | 外界は一切見えない | (機体組込み) | 固有受容感覚=制御の土台 |

---

#### 1.1 LiDAR

##### Livox Mid-360(最重要・詳細)

方式: 非反復スキャン(non-repetitive scanning)+回転機構による水平 360° カバー。時間経過とともに FOV 内の点充填率が上がる Livox 独自方式。

| 項目 | 値 | 出典 |
|---|---|---|
| FOV | 水平 360° / 垂直 **-7°〜+52°**(公式確認済) | https://www.livoxtech.com/mid-360/specs |
| 点数/秒 | 200,000 pts/s(first return) | 同上 |
| 測距範囲 | 40 m @ 反射率 10% / 70 m @ 反射率 80%(いずれも環境光 100 klx) | 同上 |
| 測距ばらつき(1σ) | ≤2 cm @ 10 m(至近 0.2 m では ≤3 cm) | 同上 |
| 角度精度 | < 0.15°(1σ) | 同上 |
| 質量 | 265 g | 同上 |
| 消費電力 | 平均 6.5 W(自己加熱モード時ピーク 14 W) | 同上 |
| フレームレート | 10 Hz(typical) | 同上 |
| 波長 | 905 nm | 同上 |
| IMU | 内蔵(ICM40609) | 同上 |
| 接続 | 100BASE-TX Ethernet、PTPv2/GPS 時刻同期対応 | 同上 |
| 価格 | 公式サンプル価格 $749(2023-01 発売時。DJI ストア検索結果でも $749) | https://www.livoxtech.com/news/mid360_launch / https://store.dji.com/product/livox-mid-360 |
| 実勢価格 | 米代理店 $899(backorder)、AliExpress 実勢 $480〜550(2025 年の購入報告、非公式) | https://www.roboticscenter.ai/store/product/livox-dji-livox-mid-360 / https://www.aliexpress.com/s/wiki-ssr/article/livox-mid-360-price-usd-2025 |

- 得意: 低価格・軽量・IMU 内蔵・全周 FOV。FAST-LIO2 / Point-LIO に公式設定ファイルがあり(後述)、箱から出して LIO が回る。
- 苦手: 垂直 -7° までしか下を向かない(足元直下は深度カメラで補完するのが G1 流)。905 nm 光学式なので雨・霧・黒色低反射面は原理的に不利。
- 典型用途: 四足/ヒューマノイドの 360° 近接知覚・屋内外 SLAM。研究用ロボットのデファクト。
- 補足: Livox は他に Avia(70.4°×77.2°、240k pts/s、450 m @ 80%、498 g — ドローン測量向け https://www.livoxtech.com/avia/specs)、HAP(車載、120°×25°、452k pts/s、150 m @ 10% — https://www.livoxtech.com/hap/specs)を展開。

##### 競合 LiDAR 比較

| 製品 | 方式 | レンジ @10% 反射率 | 点数/秒 | 質量 | 実勢価格 | 出典 |
|---|---|---|---|---|---|---|
| Unitree L1 | 半球「4D LiDAR」360°×90° | 未確認(最大 30 m) | 21,600 | 230 g | **$249**(公式) | https://shop.unitree.com/products/unitree-4d-lidar-l1 |
| Unitree L2 | 半球 360°×96° | 未確認(最大 30 m) | 64,000(公式。販売店に 128,000 表記もあり不一致→公式値採用) | 未確認 | **$419**(公式) | https://shop.unitree.com/products/unitree-4d-lidar-l2 |
| Livox Mid-360 | 非反復 360°×59° | 40 m | 200,000 | 265 g | $749〜899 | 上記 |
| Hesai JT16 | 16ch ミニドーム 360°×40° | 30 m | 48,000 | 199.7 g / 4.3 W | €599(セール、通常 €739) | https://www.hesaitech.com/product/jt16/ / https://openelab.io/products/hesai-jt16-mini-3d-lidar |
| Hesai XT16 | 16ch 機械式回転 360°×30° | 未確認(0.05〜120 m。兄弟機 XT32M は 80 m @10%) | 320,000 | 800 g | **$6,650**(米代理店) | https://www.hesaitech.com/product/xt16-32-32m/ / https://robostore.com/products/hesai-xt16-3d-lidar |
| Ouster OS0 | digital LiDAR(SPAD+ASIC)最大 128ch、垂直 90° | 35 m | 10,400,000 | 未確認 | 要問合せ(参考: OS1-32 発表時 $8,000) | https://ouster.com/products/hardware/os0-lidar-sensor |
| Ouster OS1 | 同 128ch、垂直 45° | 90 m | 10,400,000 | 未確認 | 要問合せ | https://ouster.com/products/hardware/os1-lidar-sensor / https://www.geoweeknews.com/articles/32-channel-lidar-for-8k-ousters-newest-lidar-finds-a-sweet-spot/ |

各論:

- **Hesai XT16**: 精度 ±1 cm(accuracy)/ 0.5 cm(1σ precision)、ゼロブラインドスポットが売りの産業グレード。AGV/AMR・cm 級屋内外ナビ向け(https://www.hesaitech.com/product/xt16-32-32m/)。
- **Hesai JT16**: CES 発表のロボット向けミニドーム。200 g・IP6K6 で Mid-360 の直接競合。掃除ロボ・配送ロボ狙い。
- **Ouster OS シリーズ**: 受光側を SPAD+カスタム ASIC に集積した「digital LiDAR」。点密度 10.4 M pts/s は Mid-360 の 50 倍だが、価格・質量は別クラス。OS0 の垂直 90° FOV は倉庫内ロボットの床〜天井知覚に強い。現行 Rev7/8 の精度・質量・電力・実売は公式ページ非掲載(未確認、データシートは https://ouster.com/downloads )。
- **Velodyne の現状(事実確認済)**: Velodyne は 2023-02-10 に Ouster と対等合併を完了し、存続会社は Ouster(NYSE: OUST)。旧 Velodyne 株は上場廃止(1 株 = Ouster 0.8204 株)。出典: https://investors.ouster.com/news-releases/news-release-details/ouster-and-velodyne-complete-merger-equals-accelerate-lidar / https://www.therobotreport.com/lidar-makers-ouster-velodyne-complete-merger/

#### 1.2 深度カメラ

##### Intel RealSense D435i(最重要・詳細)

方式: アクティブ IR ステレオ(IR パターン投光+左右 IR カメラの視差)。

| 項目 | 値 | 出典 |
|---|---|---|
| 深度 FOV | **87°×58°(公式確認済)**。データシート精密値 87°±3° × 58°±1°(対角 95°±3°) | https://www.intel.com/content/www/us/en/products/sku/190004/intel-realsense-depth-camera-d435i/specifications.html / https://cdrdv2-public.intel.com/841984/Intel-RealSense-D400-Series-Datasheet.pdf |
| 深度範囲 | 理想 0.3〜3 m(Min-Z 約 28 cm、848×480 時 0.105 m)。3 m 超も可だが精度低下 | https://www.realsenseai.com/products/depth-camera-d435i/ |
| 深度解像度/fps | 最大 1280×720 / 最大 90 fps | 同上 |
| 深度精度 | <2% @ 2 m | 同上 |
| RGB | 1920×1080 @30 fps(ローリングシャッター) | 同上 |
| IMU | **Bosch BMI055(6 軸)内蔵 — 確認済** | https://github.com/realsenseai/librealsense/blob/master/doc/d435i.md |
| 質量 | 約 72 g(代理店値。公式現行ページ非掲載) | https://framos.com/products/3d/3d-cameras/depth-camera-d435i-bulk-22610/ |
| 寸法/接続 | 90×25×25 mm、USB-C 3.1 Gen 1 | https://www.realsenseai.com/products/depth-camera-d435i/ |
| 価格 | **$334.00(公式ストア)** | https://store.realsenseai.com/buy-intel-realsense-depth-camera-d435i.html |

RealSense 事業の現状:

- 2021 年に Intel が事業縮小を発表したが D400 系は継続。**2025-07-11 に RealSense Inc. として Intel からスピンオフ完了**、Series A で $50M 調達(Intel Capital、MediaTek Innovation Fund 参加)。出典: https://www.realsenseai.com/news-insights/news/realsense-completes-spin-out-from-intel-raises-50-million-to-accelerate-ai-powered-vision-for-robotics-and-biometrics/ / https://www.tomshardware.com/tech-industry/realsense-completes-spin-out-from-intel-gets-usd50-million-in-funding-from-intel-capital-and-mediatek
- 独立後第 1 弾 = **D555**(D500 系): Vision SoC V5(5 TOPS)搭載、PoE 給電+グローバルシャッター。出典: https://www.vision-systems.com/embedded/article/55303384/intel-completes-realsense-spinoff
- 同社は「世界の AMR/ヒューマノイドの 60% に採用」と主張(自社発表値)。

##### 競合深度カメラ

| 製品 | 方式 | 深度スペック | 価格 | 出典 |
|---|---|---|---|---|
| Orbbec Gemini 335 | アクティブステレオ(MX6800 ASIC) | 0.1〜20 m+、1280×800@30fps、FOV 90°×65° | **$264**(公式ストア) | https://store.orbbec.com/products/gemini-335 |
| Orbbec Gemini 335L | 同・基線 95 mm・IP65 | 精度 ≤0.8% @ 2 m | $359 | https://www.hackster.io/news/orbbec-unveils-the-robust-fakra-connectable-gemini-335lg-depth-camera-for-autonomous-robots-and-more-e23d922b5158 |
| Orbbec Femto Bolt | Microsoft iToF(Azure Kinect と同一深度技術) | 0.25〜5.46 m、WFOV 120°×120°、RGB 4K、IMU 内蔵 | **$418**(公式ストア) | https://store.orbbec.com/products/femto-bolt |
| Stereolabs ZED 2i | パッシブステレオ+Neural Depth | 0.2〜20 m、110° 広角、IMU+気圧+磁気 | $499〜(検索結果値、要再確認) | https://store.stereolabs.com/products/zed-2i/ |
| Stereolabs ZED X | 同(Gen2)+グローバルシャッター | 0.3〜20 m(2.2mm)/1〜35 m(4mm)、GMSL2 接続(Jetson 前提) | $549〜599(検索結果値) | https://static.generation-robots.com/media/zed-x-datasheet-v1.2.pdf |

- **Azure Kinect DK の EOL(事実確認済)**: Microsoft は 2023-08 に生産終了を発表、2023 年 10 月販売終了。SDK リポジトリは 2024-08-22 アーカイブ。後継として Microsoft 公式提携のもと Orbbec Femto Bolt/Mega が iToF 技術をライセンス実装(Azure Kinect と同一深度モード、K4A API 互換ラッパーあり)。出典: https://hackaday.com/2023/08/26/microsoft-discontinues-kinect-again/ / https://github.com/microsoft/Azure-Kinect-Sensor-SDK/issues/1971 / https://www.orbbec.com/microsoft-collaboration/ / https://www.orbbec.com/documentation/comparison-with-azure-kinect-dk/
- Orbbec SDK は ROS1/ROS2 ネイティブ対応(https://store.orbbec.com/products/gemini-335le)。

#### 1.3 イベントカメラ(DVS)

原理(1 行): 各画素が独立・非同期に「輝度の対数変化が閾値を超えた瞬間」だけを (x, y, タイムスタンプ, 極性) のイベントとして出力する — フレームを撮らない。出典: https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/

##### Prophesee / Sony IMX636

| 項目 | 値 | 出典 |
|---|---|---|
| 開発 | Sony(積層 BSI プロセス)× Prophesee(イベント画素)共同開発 | https://www.prophesee.ai/2022/04/13/new-sony-imx636es-hd-sensor-realized-in-collaboration-between-sony-and-prophesee/ |
| 解像度 / 画素ピッチ | **1280×720 / 4.86 μm(確認済)** | https://www.prophesee.ai/wp-content/uploads/2024/05/IMX636-Product-Brief-2024-v3.0.pdf |
| 時間分解能 | タイムスタンプ精度 1 μs、画素レイテンシ <100 μs @1000 lux(等価 >10k fps) | 同上 / https://www.prophesee.ai/event-camera-evk4/ |
| ダイナミックレンジ | **公式表記は >86 dB(typ)/ >120 dB(低照度条件 0.08〜100,000 lux)** — 「120 dB」は測定条件付きの値 | https://support.prophesee.ai/portal/en/kb/articles/evk4-hd-product-brief |
| 最大イベントレート | 1.06 Geps 級(Sony 公表) | https://www.sony-semicon.com/en/products/is/industry/evs.html |
| SDK | Metavision SDK(OSS 版 OpenEB) | https://github.com/prophesee-ai/openeb |
| 評価キット EVK4 | IMX636、USB 3.0、30×30×36 mm、40 g。公式直販は見積制(未確認)、台湾代理店実売 NT$175,000 ≈ **$5,400** | https://www.prophesee.ai/event-camera-evk4/ / https://store.edomtech.com/products/evk4 |

##### iniVation DVXplorer

| 項目 | 値 | 出典 |
|---|---|---|
| 解像度 | VGA 640×480 | https://docs.inivation.com/hardware/current-products/dvxplorer.html |
| ダイナミックレンジ | 最大 110 dB | 同上 |
| 時間分解能 | 200 μs、レイテンシ <1 ms、最大 165 Meps | 同上 |
| 価格 | **€3,900(商用)/ €3,400(アカデミック)** | https://shop.inivation.com/collections/dvxplorer |

- 得意: 高速運動(モーションブラーなし)・HDR 環境(トンネル出入口・逆光)・低消費・μs 級低レイテンシ。
- 苦手: 静止シーンは原理的に何も見えない(自己運動かアクティブ照明が必要)/フレーム前提の CV・深層学習資産が直接使えず表現変換(voxel grid、time surface 等)が必要/イベントレートがシーン依存でバースト的(帯域・処理系はワーストケース設計)。
- データレートの性質: 出力はシーン依存・スパース。静止でほぼゼロ、激しい動き+高テクスチャで Geps 級までスパイクしうる。
- 典型用途: 高速障害物回避、ドローン検知・追跡、高速 VO/SLAM、振動監視、低レイテンシ把持。

#### 1.4 IMU(MEMS)— 等級とドリフト

業界慣用 4 等級。位置誤差は時間の約 3 乗で成長し、ジャイロの in-run bias instability が支配項(https://www.vectornav.com/resources/detail/what-is-an-inertial-navigation-system)。

| 等級 | Gyro bias instability 目安 | GPS なし慣性航法 60 秒の位置誤差 | 代表用途 |
|---|---|---|---|
| 民生級 | ~100 °/h | **400 m** | スマホ・ドローン FC・ホビー |
| 産業級 | ~10 °/h | **40 m** | ロボット・農機・AGV |
| 戦術級 | ~1 °/h | **5 m** | UAV・軍用・測量 |
| 航法級 | ~0.01 °/h | **50 cm** | 航空機・艦船・潜水艦 |

(出典: VectorNav 上記。等級定義はメーカー間で厳密標準がない点に注意 — https://ez.analog.com/mems/w/documents/4111/what-does-tactical-grade-mean-for-a-mems-imu )

代表デバイス実スペック:

| デバイス | 等級 | Gyro bias instability | ノイズ | 価格 | 出典 |
|---|---|---|---|---|---|
| Bosch BMI088 | 民生(ドローン向け) | データシート非記載(フォーラム回答で <2 °/h と案内 ※flyer 値) | gyro 0.014 °/s/√Hz | 数ドル級(単価未確認) | https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi088-ds001.pdf |
| TDK ICM-42688-P | 民生(FPV 定番) | データシート非記載 | gyro 2.8 mdps/√Hz | 数ドル級(未確認) | https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/ds-000347-icm-42688-p-v1.6.pdf |
| ADI ADIS16470 | 産業級 | **8 °/h** | 0.008 °/s/√Hz | **$481.53**(DigiKey) | https://www.analog.com/media/en/technical-documentation/data-sheets/adis16470.pdf / https://www.digikey.com/en/products/detail/analog-devices-inc/ADIS16470AMLZ/7932982 |
| ADI ADIS16490 | 戦術級 | **1.8 °/h** | ARW 0.09 °/√h | 数千ドル級(未確認) | https://www.analog.com/media/en/technical-documentation/data-sheets/adis16490.pdf |
| Honeywell HG4930 | 戦術級 | **0.25 °/h** | ARW 0.04 °/√h | **$8,300〜$13,500**(DigiKey 型番別) | https://media.digikey.com/pdf/data%20sheets/honeywell%20pdfs/hg4930_perfandenvriomanual_jul2017.pdf / https://www.digikey.com/en/products/detail/honeywell-aerospace/HG4930CA51/6562993 |

- まとめ: 民生→戦術で価格 3 桁、bias instability 2 桁以上改善。GPS なし 60 秒で 400 m vs 5 m。
- 採用例: Pixhawk 6X(Rev 8)は ICM-45686 ×3 の三重冗長 — 民生級 IMU の冗長構成+フュージョンで運用(https://www.getfpv.com/electronics/flight-controllers/holybro-pixhawk-6x-fc-v2a-standard-set-icm-45686.html)。Unitree G1 は「6 軸 IMU」とのみ公表、型番・等級は未確認(https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications)。
- 典型用途: 姿勢推定、LIO/VIO の predict ステップ。脚ロボは着地衝撃(高帯域・飽和)対策が鍵(後述 Point-LIO)。

#### 1.5 力/トルク・足裏・触覚

##### 6 軸 F/T センサ

| 製品 | 原理 | スペック | 価格 | 出典 |
|---|---|---|---|---|
| ATI(現 Novanta)Axia80 | シリコンひずみゲージ(箔ゲージ比 75 倍の信号強度) | 力 ~500 N / トルク ~20 Nm、過負荷耐性 5〜12.5 倍、EtherCAT/Ethernet | 見積制(未確認。市場では数千ドル級とされる) | https://ati.novanta.com/product/axia80-force-torque-sensor-kit/ |
| Robotiq FT 300-S | 「wear-free sensing technology」(静電容量式かは公式明記なし=未確認) | ±300 N / ±30 Nm、100 Hz、IP65、過負荷 500% | キット **$5,720**(代理店) | https://robotiq.com/products/ft-300-force-torque-sensor / https://www.kingbarcode.com/FTS-300-S-KIT-001 |

##### ヒューマノイド足裏の接地検知 — 3 方式比較

| 方式 | 得られる情報 | 長所 | 短所 | 採用例 |
|---|---|---|---|---|
| 足首 6 軸 F/T | 床反力 3 力+3 モーメント → ZMP 直接算出 | ZMP 制御に最適・高精度 | 高価・重い・着地衝撃/EMI に弱い | ASIMO、HRP-4 等(研究文献ベース: https://www.researchgate.net/publication/257672554_Signal_Processing_and_Application_of_Six-axis_ForceTorque_Sensor_Integrated_in_Humanoid_Robot_Foot ) |
| 足裏分布圧(FSR/圧力マット) | 法線方向の圧力分布 | 安価・薄い・接地面形状が分かる | せん断力/モーメント不可、ヒステリシス | ホビー/研究機で広く使用(個別一次ソース未確認) |
| 関節電流(トルク)推定 | 関節トルクから外力推定 | 追加センサ不要・コスト 0 | 減速機摩擦で精度限界 | 近年の量産ヒューマノイドの主流傾向 |

- **Unitree G1**: 公表仕様に足裏力センサの記載なし(センサ表は Depth カメラ/3D LiDAR/マイク/関節エンコーダ/IMU のみ)→ 接地判定は関節側推定とみられる(断定は未確認)。出典: https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications

##### 触覚スキン

| 製品 | 原理 | 状況・価格 | 出典 |
|---|---|---|---|
| GelSight Mini | 視触覚(ゲル変形をカメラ撮像) | **$499**(交換ゲル $49)で一般販売中。研究で最普及 | https://www.gelsight.com/gelsightmini/ |
| Meta Digit 360 | 指先全周の視触覚+多モーダル(1 mN の力検出) | GelSight 製造。2024-10 発表、価格未公表(未確認) | https://www.businesswire.com/news/home/20241031980322/en/GelSight-and-Meta-AI-Introduce-Digit-360-Tactile-Sensor |
| uSkin(XELA Robotics) | 磁気式 3 軸(法線+せん断)高密度分布 | 商用展開中(2025-12 Tesollo DG-5F 統合、CES 2026 デモ)。価格未公表 | https://roboticsandautomationnews.com/2025/12/04/xela-robotics-adds-high-precision-tactile-sensing-to-tesollo-robot-hand/97352/ |

#### 1.6 その他(簡潔)

- **ToF カメラ**: 変調光の位相差で全画素同時測距。Orbbec Femto Bolt は系統誤差 <11 mm + 距離の 0.1%、σ≤17 mm(https://www.orbbec.com/products/tof-camera/femto-bolt/)。屋内の密な深度に強く、直射日光・黒色低反射・マルチパスが弱点。
- **超音波**: HC-SR04 でレンジ 2 cm〜4 m、分解能 0.3 cm、数ドル(https://www.dfrobot.com/blog-13482.html)。光学式が苦手な透明物・ガラスに反応するのが差別化点。
- **GNSS/RTK**: u-blox ZED-F9P は RTK 時水平 1 cm(単独 2.5 m)。SparkFun ボードで $259.95(https://www.sparkfun.com/sparkfun-gps-rtk2-board-zed-f9p-qwiic-gps-15136.html)。cm 級には基準局か NTRIP 補正が必須。屋外実験のグラウンドトゥルース取りに最適。
- **関節エンコーダ**: 絶対値式 17 bit = 131,072 分割/回転、23 bit = 約 839 万分割(https://www.dynapar.com/knowledge/encoder-basics/encoder-resolution/single-turn-vs-multi-turn-encoders/)。ヒューマノイド関節は絶対値式が主流。Unitree G1 は各関節にデュアルエンコーダ(モータ側+出力側)(https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications)。

---

### 2. マルチセンサフュージョン手法の整理

**記事向け要約(5 行)**

1. フュージョンの古典は「各センサの誤差特性(共分散)で重み付けした逐次ベイズ推定」= カルマンフィルタ(EKF/UKF)であり、ROS の robot_localization が事実上の標準実装。
2. LiDAR-慣性オドメトリ(LIO。移動量を積算して自己位置を出す手法)はファクターグラフの LIO-SAM(2020)→ 反復 EKF+ikd-Tree の FAST-LIO2(2021、100 Hz)→ 点単位更新の Point-LIO(2023、4〜8 kHz)へと進化し、いずれも Mid-360 対応設定が公式提供されている。
3. 学習ベースでは、カメラ+LiDAR を鳥瞰(BEV)特徴空間で混ぜる BEVFusion(2022)と、訓練中にセンサ 1 系統を丸ごと落とす modality dropout による頑健化が主要潮流。
4. 脚ロボの金字塔は teacher-student 蒸留: シミュ内の特権情報(接触力・地形)を見る教師を、実機で使える固有受容感覚のみの生徒へ蒸留する(Lee et al. 2020 / Miki et al. 2022, Science Robotics)。
5. 実機ヒューマノイドは「LiDAR+深度カメラ派」(Unitree、Agility)と「カメラ純化派」(Tesla、Figure)に二分され、量産版 Atlas の LiDAR 撤去報道はカメラ派への合流を示唆する。

#### 2.1 古典: カルマンフィルタとファクターグラフ

##### EKF / UKF

| 項目 | EKF | UKF |
|---|---|---|
| 非線形の扱い | ヤコビアンで 1 次線形化 | シグマ点を非線形関数にそのまま通す(Unscented 変換) |
| 長所 | 軽い・実績膨大 | 2 次精度・ヤコビアン導出不要 |
| 短所 | 強非線形・大姿勢誤差で発散しやすい | やや重い |

- 典型構成: IMU(高レート・ドリフト)を予測、エンコーダ・GNSS(絶対・低レート)を観測として統合。ROS 標準実装 = robot_localization(EKF/UKF 両対応): https://github.com/cra-ros-pkg/robot_localization
- 本質: 相補的なセンサを誤差共分散で重み付けして混ぜる逐次ベイズ推定。
- 書誌: Kalman 1960 が原典、UKF は Julier & Uhlmann 1997(一次 URL 未確認)。

##### ファクターグラフ / LIO 系譜

| 手法 | 年/著者 | 要点 | 性能主張 | URL |
|---|---|---|---|---|
| GTSAM | Georgia Tech Borg Lab(iSAM2 は Kaess et al., IJRR 2012) | ファクターグラフ+ベイズ木の C++ 基盤。IMU 事前積分 factor 提供 | iSAM2 でインクリメンタル更新 | https://github.com/borglab/gtsam |
| LIO-SAM | 2020 IROS / Tixiao Shan ら(MIT/Stevens) | LiDAR-慣性をファクターグラフで定式化(GTSAM 使用)。ループ閉合・GPS を factor として追加可能 | リアルタイム高精度軌跡+地図 | https://github.com/TixiaoShan/LIO-SAM / https://arxiv.org/abs/2007.00258 |
| FAST-LIO2 | 2021 arXiv / 2022 T-RO / Wei Xu, Fu Zhang ら(HKU MARS) | 特徴抽出なしで生点群を直接レジストレーション。tightly-coupled 反復 EKF+増分 kd 木 ikd-Tree | 「SOTA 比で高精度かつ大幅に低計算負荷」「最大 100 Hz」 | https://github.com/hku-mars/FAST_LIO / https://arxiv.org/abs/2107.06829 |
| Point-LIO | 2023 Advanced Intelligent Systems / He, Xu, Zhang ら(HKU MARS) | 点単位で状態更新しフレーム内歪みを原理的に排除。IMU を「出力」として扱い飽和下でも推定継続 | 4〜8 kHz オドメトリ、角速度 75 rad/s の激運動でも動作 | https://github.com/hku-mars/Point-LIO / https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202200459 |

- **Mid-360 対応**: FAST-LIO リポジトリに公式 `config/mid360.yaml` があり(https://github.com/hku-mars/FAST_LIO/blob/main/config/mid360.yaml)、Point-LIO も同系で Mid-360 設定を提供 — G1 標準搭載の Mid-360 でそのまま LIO が回るエコシステムが揃っている。
- 使い分け相場観: ループ閉合・GPS 統合まで欲しい → LIO-SAM / 計算資源が細い・高速機動 → FAST-LIO2 / 脚ロボの足接地衝撃のような振動・激運動 → Point-LIO。

#### 2.2 学習ベース

##### BEV 融合

| 論文 | 出所 | 要点 | URL |
|---|---|---|---|
| BEVFusion(MIT 版) | MIT Han Lab, 2022(ICRA 2023) | カメラ・LiDAR 両特徴を共有 BEV 空間に持ち込み融合。BEV pooling 最適化で view 変換 40 倍以上高速化。マルチタスク対応 | https://arxiv.org/abs/2205.13542 / https://github.com/mit-han-lab/bevfusion |
| BEVFusion(PKU 版・同名別論文) | 北京大+Alibaba, NeurIPS 2022 | カメラ流と LiDAR 流を独立に BEV 化して融合。LiDAR 故障シミュレーション込み訓練で SOTA +15.7〜28.9% mAP を主張 | https://arxiv.org/abs/2205.13790 / https://github.com/ADLab-AutoDrive/BEVFusion |

##### モダリティドロップアウト(センサ欠損への頑健化)

- 考え方: 通常の dropout がニューロンを消すのに対し、訓練中にセンサ 1 系統を丸ごと落とす(ゼロ埋め/マスク)→「残ったセンサで埋め合わせる」内部表現を学び、実運用のセンサ故障・遮蔽に耐える。概説: https://www.emergentmind.com/topics/modality-dropout
- 代表例: PKU 版 BEVFusion の故障込み訓練(上記)/ MoME(2025、カメラ全損で NDS 87.9% 維持と報告 — https://arxiv.org/abs/2503.19776)/ 先行例 Sensor Dropout(Liu et al., CoRL 2017 — https://arxiv.org/abs/1705.10422 、細部未確認)。

##### Privileged learning / Teacher-Student 蒸留(脚ロボの金字塔)

| 論文 | 書誌 | 要点 | URL |
|---|---|---|---|
| Lee et al. "Learning quadrupedal locomotion over challenging terrain" | Science Robotics Vol.5, Issue 47, eabc5986, 2020-10-21 | 教師はシミュ内でのみ得られる特権情報(接地状態・接触力・地形形状・摩擦)で RL 学習 → 生徒は実機で使える固有受容感覚(関節角・IMU)の履歴のみで教師を模倣。盲目の ANYmal が泥・雪・植生・瓦礫を踏破 | https://doi.org/10.1126/scirobotics.abc5986 / https://arxiv.org/abs/2010.11251 |
| Miki et al. "Learning robust perceptive locomotion for quadrupedal robots in the wild" | Science Robotics Vol.7, Issue 62, eabk2822, 2022 | 外受容(高さマップ)+固有受容を attention ベースの再帰的 belief state encoder で統合。外界センサが当てにならない場面では固有受容側へ自動的に重みを移す =「学習されたフュージョンゲート」。ANYmal がアルプス登山道 1 時間コースを完走 | https://www.science.org/doi/10.1126/scirobotics.abk2822 |

- ヒューマノイドへの輸入例: Humanoid Parkour Learning(Zhuang et al., CoRL 2024)は蒸留方策を Unitree H1 に zero-shot 移植(https://arxiv.org/abs/2406.10759)。ExBody2 は teacher-student 蒸留で H1/G1 の全身トラッキング(arXiv:2412.13196 とされるが一次確認未了)。四足で確立した構図が 2024〜2026 のヒューマノイド RL 歩行へそのまま流入している。

#### 2.3 実機ヒューマノイドのセンサ構成(公表情報)

| 機体 | センサ構成(公表分) | 出典 | 備考 |
|---|---|---|---|
| Unitree G1 | 公式仕様表は「Depth Camera + 3D LiDAR」+4ch マイクアレイ+スピーカ | https://www.unitree.com/g1 | **公式はモデル名を明記せず**。Livox Mid-360 + RealSense D435(i) という型番は代理店/技術ドキュメント側の記載(https://docs.quadruped.de/projects/g1/html/g1_overview.html) |
| Unitree H1 | 公式:「3D LIDAR + Depth Camera による 360° 深度知覚」 | https://www.unitree.com/h1 | 型番は公式非記載(流通情報では Mid-360 + D435i) |
| Tesla Optimus | カメラ中心(Autopilot 由来ビジョン)+指先触覚+足裏力/トルク。「8 カメラ」は第三者レビュー値で公式一次ソース未確認 | https://briandcolwell.com/a-complete-review-of-teslas-optimus-robot/ | LiDAR 非搭載のカメラ純化路線 |
| Figure 02 / 03 | 02: RGB カメラ 6 台+VLM(6 台の一次ページ明記は未確認)。03: 手のひらカメラ+触覚センサを公式発表 | https://www.figure.ai/news/introducing-figure-03 | LiDAR なし・視覚+触覚路線 |
| Boston Dynamics 新 Atlas(電動) | 2024 研究機: ToF+RGB-D/ステレオ+LiDAR、IMU 1 kHz・関節エンコーダ 4 kHz(第三者まとめ)。2026 量産版は LiDAR を外し 360° カメラ+触覚構成へ変更との報 | https://www.aparobot.com/robots/atlas | 公式の一次センサ仕様書は存在せず(未確認扱い) |
| Agility Digit | Velodyne VLP-16(胴体頂部)+ RealSense 深度カメラ×4(骨盤前後の D430 ×2 含む)。LiDAR=遠方地図/障害物、深度カメラ=足元の面推定 | https://robotsguide.com/robots/digit / https://agilityrobotics.com/content/check-out-these-big-advancements-in-digits-development | LiDAR+深度の古典的フュージョン構成の代表 |

観察: 業界は二派 — ① LiDAR+深度カメラ派(Unitree、Agility、研究版 Atlas): §2.1 の LIO 資産をそのまま使える。② カメラ純化派(Tesla、Figure): 学習ベース(§2.2)で幾何を推定。量産 Atlas の LiDAR 撤去は②への合流を示唆。

#### 2.4 「どの層で混ぜるか」— early / mid / late fusion(3 段かみ砕き)

##### ① たとえ話(料理)

- **Early fusion(生データで混ぜる)** = 材料を全部同じ鍋に最初から入れる。素材同士がよく馴染むが、一つ腐っていたら鍋ごと台無し。
- **Mid fusion(特徴で混ぜる)** = 各材料を別々に下ごしらえしてから合わせる。合わせやすく、変な材料は下ごしらえ段階で気づける。
- **Late fusion(結論で混ぜる)** = 3 人の料理人がそれぞれ完成品を作り、審査員が多数決。一人が失敗しても挽回できるが、素材同士の化学反応は起きない。

##### ② 工学的説明

| 層 | 混ぜるもの | 長所 | 短所 |
|---|---|---|---|
| Early(raw) | 生点群・生画素・生 IMU 値 | 情報損失ゼロ。相関を最大限利用(例: Point-LIO は LiDAR 点 1 個ごとに IMU と状態更新) | 時刻同期・外部キャリブレーションに極めて敏感。レート差(IMU 数百 Hz vs カメラ 30 Hz)の吸収が難しい。1 センサの故障が全体を汚染 |
| Mid(特徴) | 特徴マップ・BEV 特徴・埋め込み | モダリティごとに最適なエンコーダを使いつつ密に融合。BEVFusion も Miki 2022 の belief encoder もこの層 | 共通表現空間の設計が必要。訓練分布外の欠損に弱い → modality dropout で補強 |
| Late(判断) | 各系統の推定結果(位置・検出・判定) | モジュール独立で開発・検証・交換が容易。故障隔離が自然(EKF で LIO 出力+GNSS+オドメトリを統合するのはこの層) | 各系統が捨てた情報は戻らない。判断が割れたときの調停が難しい |

##### ③ 実装上の考慮

- **時刻同期が全ての土台**: early に行くほど PTP/ハードウェアトリガ級の同期が必須。Mid-360 は IMU 内蔵・同期済みなので early fusion(LIO)がやりやすい。
- **キャリブレーション誤差の伝播**: early/mid はセンサ間外部パラメータの誤差が特徴空間の「にじみ」として学習を汚す。late は各系統内で閉じる。
- **故障モード設計**: late は縮退運転(LiDAR 死亡→カメラのみで減速継続)を設計しやすい。mid で同等の頑健性が欲しければ modality dropout を訓練時に必ず入れる(PKU 版 BEVFusion の教訓)。
- **計算予算とレート**: early は最速センサのレートで回る(Point-LIO 4〜8 kHz)。制御ループ直結の状態推定は early/古典、意味理解は mid/学習、行動判断・冗長化は late — と層ごとに使い分けるハイブリッドが実機の定石(例: G1 = Mid-360+IMU を FAST-LIO2 で early 融合 → 深度カメラの検出を mid/late で重畳)。

---

### 3. 市場動向(2024〜2026)

**記事向け要約(5 行)**

1. ヒューマノイド市場予測は Goldman Sachs「2035 年 380 億ドル」(2024 年に従来比 6 倍へ上方修正)から Morgan Stanley「2050 年 5 兆ドル TAM」、Citi「2050 年 7 兆ドル」まで、投資銀行間で 2 桁近い幅がある。
2. 中国は工信部が 2023-11 に「2025 年量産・2027 年世界先進水準」の産業政策を公表済みで、中商産業研究院は 2025 年の中国出荷 1.44 万台=世界の 84.7% と推計する(2026 年時点)。
3. LiDAR は価格破壊が進行中 — Mid-360 $749、Unitree L1 $249、Hesai は「約 $200 の ATX」を量産し 2025 年出荷ガイダンス 120〜150 万台。Yole は「出荷減ではなく単価急落」を理由に金額予測を下方修正した。
4. イベントカメラの旗手 Prophesee は 2024-10 に司法再建入り → CEO 交代 → 2026-06 に €20M 調達+ドローン検知システム Mantara 発表で自力再建(買収ではない)。
5. 北京は 2025-04 に世界初のヒューマノイドハーフマラソン(優勝: 天工 Ultra、2:40:42)、2025-08 に第 1 回世界ヒューマノイドロボット運動会(16 カ国・500 台超)を開催し、2026-04 の第 2 回マラソンではロボットが人間の世界記録を上回る 50 分 26 秒を記録、第 2 回運動会は 2026-08-22 開幕(2,056 台)。
