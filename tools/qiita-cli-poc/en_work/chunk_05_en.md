## Appendix B: Robot Roster — Taking Stock of All 67 Menagerie Models

In service of the ambition "I want to run every kind of robot," we took stock of every model in MuJoCo Menagerie by actually loading each one and stepping its physics. Result: **67 out of 67 models loaded and simulated successfully — zero failures**. In other words, as raw material Menagerie is "all hands ready for action"; the bottleneck is not the models but the side of control laws, rewards, and reference motions.


![Athlete roster 1](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/menagerie_gallery_humanoid.png)
*Figure: measured Menagerie renders (humanoids + musculoskeletal, 15 bodies)*

![Athlete roster 2](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/menagerie_gallery_quadruped_drone.png)
*Figure: measured Menagerie renders (quadrupeds + drones, 10 bodies)*

![Athlete roster 3](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/menagerie_gallery_arm_mobile.png)
*Figure: measured Menagerie renders (arms + dual-arm + mobile manipulators, 33 bodies)*

![Athlete roster 4](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/menagerie_gallery_hand_gripper.png)
*Figure: measured Menagerie renders (hands + grippers, 9 bodies)*

### B.1 Breakdown by Type (67 Models, Measured)

| Type | Count | Representatives |
|---|---|---|
| Humanoid (biped) | 12 | Unitree G1/H1, Booster T1, Fourier N1, Apptronik Apollo, PAL Talos, Agility Cassie, Berkeley Humanoid, Robotis OP3, PND Adam Lite, ToddlerBot ×2 |
| Quadruped | 8 | ANYmal B/C, Boston Dynamics Spot, Google Barkour v0/vB, Unitree A1/Go1/Go2 |
| Arm (single) | 22 | Franka Panda/FR3, KUKA iiwa14, UR5e/UR10e, Kinova Gen3, xArm7, ViperX, and more |
| Dual-arm | 2 | ALOHA, Trossen WXAI |
| Mobile manipulator | 7 | Hello Robot Stretch ×2, PAL TIAGo ×2, Google Robot, TidyBot, Rainbow RBY1 |
| Dexterous hand | 6 | Shadow Hand, LEAP Hand, Allegro, Shadow DEX-EE, and more |
| Gripper | 3 | Robotiq 2F-85 ×2, UMI Gripper |
| Drone | 2 | Crazyflie 2, Skydio X2 |
| Musculoskeletal / biological | 2 | MS-Human-700 (700 muscles), flybody (a fly) |
| Other | 3 | Soccer kit, RealSense D435i (sensor asset), IIT SoftFoot (foot component) |

![Roster statistics](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_roster_stats.png)
*Figure: measured tallies of the 67 machines by type, actuator type, and keyframe presence (plotted from the inventory JSON)*

### B.2 The "Map for Getting Things Moving" That the Inventory Revealed

![Go2 portrait](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_go2.png)
*Figure: Unitree Go2 (simulation render)*

![Spot portrait](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_spot.png)
*Figure: Boston Dynamics Spot (simulation render)*

- **All 8 quadrupeds share the same layout (18 DoF, 12 actuated).** Write one training pipeline and you can sweep 8 models side by side. The quadruped events are perfect as the games' team competition.
- **The 22 arms "don't fall over," so applying inverse kinematics (IK — computing joint angles backward from a target hand position) yields an instant demo.** The samples of the differential-IK library (mink, Apache-2.0) are effectively the de facto Menagerie demo collection.
- **19 models lack a home posture (keyframe).** The first bit of "material prep" for a full-roster debut is the rather unglamorous task of authoring standing poses.
- **Individuals requiring care**: Cassie's closed-linkage mechanism constrains GPU parallelism (MJX). Dexterous hands need designs that assume tendon-driven or underactuated setups where "joint count and command count don't match."
- **The 12 humanoids split into direct-torque types (H1, Talos, etc.) and position-servo types (G1, T1, etc.).** For the main text's H1 support we wrote an adapter that turns the torque types into position servos to absorb this difference (so the G1's 11 reward clauses port over unchanged).

### B.3 The Two Pillars of Training Resources — and the License Minefield

The OSS training environments rest on two pillars: (1) **MuJoCo Playground** (Apache-2.0; training environments and configs for 9 quadruped/biped locomotion models + 4 manipulation models) and (2) **LocoMuJoCo** (MIT; distributes 22,000+ retargeted motions, 10 humanoids + 4 quadrupeds) — complementary to each other.

And the inventory's biggest harvest was the **license map of motion data**.

| Data source | Contents | License |
|---|---|---|
| AMASS | Large-scale mocap aggregation unified on SMPL | **Non-commercial only (commercial neural-net training also prohibited)** |
| LAFAN1 (this article's teacher) | 4.6 hours of high-quality mocap | **CC BY-NC-ND (non-commercial, no derivatives)** |
| CMU Mocap | 2,600+ sequences | **Free, commercial use OK** (only resale prohibited) |
| GMR (general-purpose retargeter) | SMPL-X/BVH/video → 18 robot models | **MIT** |

For a hobby games, LAFAN1 is fine — but if this technology is to inch toward products, **"CMU mocap (commercial OK) + GMR (MIT)" is the cleanest pedigree**. Data licenses get overlooked more often than code licenses, and they are much harder to swap out later — another place where the industrial instincts came in handy.

### B.4 The Complete 67-Model Measurement Table

The "physical exam results" for all 67 machines. nq = number of generalized coordinates (DoF + quaternion slots), nv = velocity degrees of freedom, nu = number of actuation commands. Actuator types mean what they did in the main text and B.2; a machine with a free joint of "yes" is one that can fall over (= balance becomes the competition). keyframe is the bundled reference posture. Every row's values were taken by actually loading the model and stepping the physics.

| Model | nq | nv | nu | Actuators | Free joint | keyframe | Meshes | License |
|---|---|---|---|---|---|---|---|---|
| `agilex_piper` | 8 | 8 | 7 | position+kv×7 | no | home | 82 | MIT |
| `agility_cassie` | 35 | 32 | 10 | motor×10 | yes | home | 25 | custom/see LICENSE |
| `aloha` | 16 | 16 | 14 | position×12, position+kv×2 | no | neutral_pose | 24 | custom/see LICENSE |
| `anybotics_anymal_b` | 19 | 18 | 12 | position×12 | yes | none | 46 | custom/see LICENSE |
| `anybotics_anymal_c` | 19 | 18 | 12 | position×12 | yes | none | 24 | custom/see LICENSE |
| `apptronik_apollo` | 39 | 38 | 32 | position×32 | yes | stand | 44 | Apache-2.0 |
| `arx_l5` | 8 | 8 | 7 | position+kv×7 | no | home | 10 | BSD |
| `berkeley_humanoid` | 19 | 18 | 12 | position+kv×12 | yes | home | 13 | custom/see LICENSE |
| `bitcraze_crazyflie_2` | 7 | 6 | 4 | motor×4 | yes | hover | 39 | MIT |
| `booster_t1` | 30 | 29 | 23 | position+kv×23 | yes | home | 24 | Apache-2.0 |
| `boston_dynamics_spot` | 19 | 18 | 12 | position+kv×12 | yes | home | 23 | BSD |
| `dynamixel_2r` | 2 | 2 | 2 | position+kv×2 | no | none | 15 | custom/see LICENSE |
| `flexiv_rizon4` | 7 | 7 | 7 | position+kv×7 | no | home | 14 | Apache-2.0 |
| `flexiv_rizon4s` | 7 | 7 | 7 | position+kv×7 | no | home | 14 | Apache-2.0 |
| `flybody` | 109 | 108 | 78 | position×64, motor×6, adhesion×8 | yes | key0 | 85 | Apache-2.0 |
| `fourier_n1` | 30 | 29 | 23 | motor×23 | yes | home | 29 | Apache-2.0 |
| `franka_emika_panda` | 9 | 9 | 8 | position+kv×8 | no | home | 67 | Apache-2.0 |
| `franka_fr3` | 7 | 7 | 7 | position+kv×7 | no | home | 36 | Apache-2.0 |
| `franka_fr3_v2` | 7 | 7 | 7 | position+kv×7 | no | home | 37 | Apache-2.0 |
| `google_barkour_v0` | 19 | 18 | 12 | position+kv×12 | yes | standing | 14 | Apache-2.0 |
| `google_barkour_vb` | 19 | 18 | 12 | position+kv×12 | yes | home | 11 | Apache-2.0 |
| `google_robot` | 9 | 9 | 9 | position×9 | no | none | 47 | Apache-2.0 |
| `hello_robot_stretch` | 31 | 29 | 8 | motor×2, position+kv×3, position×3 | yes | none | 67 | BSD |
| `hello_robot_stretch_3` | 41 | 38 | 10 | velocity×2, position+kv×3, position×5 | yes | home, stow | 85 | Apache-2.0 |
| `i2rt_yam` | 8 | 8 | 7 | position+kv×7 | no | home | 17 | MIT |
| `iit_softfoot` | 93 | 93 | 1 | position×1 | no | none | 10 | custom/see LICENSE |
| `kinova_gen3` | 7 | 7 | 7 | position+kv×7 | no | home, retract | 8 | custom/see LICENSE |
| `kuka_iiwa_14` | 7 | 7 | 7 | position+kv×7 | no | home | 13 | BSD |
| `leap_hand` | 16 | 16 | 16 | position+kv×16 | no | none | 11 | custom/see LICENSE |
| `low_cost_robot_arm` | 6 | 6 | 6 | position+kv×6 | no | home | 22 | Apache-2.0 |
| `ms_human_700` | 85 | 85 | 700 | muscle×700 | no | init | 189 | Apache-2.0 |
| `pal_talos` | 51 | 50 | 32 | motor×32 | yes | key0 | 74 | Apache-2.0 |
| `pal_tiago` | 29 | 28 | 14 | motor×7, position×5, velocity×2 | yes | none | 21 | Apache-2.0 |
| `pal_tiago_dual` | 32 | 31 | 25 | velocity×4, position×7, motor×14 | yes | none | 25 | Apache-2.0 |
| `pndbotics_adam_lite` | 32 | 31 | 25 | motor×25 | yes | none | 73 | MIT |
| `rainbow_robotics_rby1` | 35 | 34 | 26 | velocity×2, position+kv×24 | yes | none | 47 | Apache-2.0 |
| `realsense_d435i` | 0 | 0 | 0 | — | no | none | 9 | Apache-2.0 |
| `rethink_robotics_sawyer` | 7 | 7 | 7 | position+kv×7 | no | home | 49 | Apache-2.0 |
| `robot_soccer_kit` | 71 | 70 | 4 | velocity×3, position+kv×1 | yes | none | 29 | custom/see LICENSE |
| `robotiq_2f85` | 15 | 14 | 1 | position+kv×1 | yes | none | 8 | custom/see LICENSE |
| `robotiq_2f85_v4` | 13 | 12 | 1 | position+kv×1 | yes | none | 8 | custom/see LICENSE |
| `robotis_op3` | 27 | 26 | 20 | position×20 | yes | none | 48 | Apache-2.0 |
| `robotstudio_so101` | 6 | 6 | 6 | position+kv×6 | no | none | 18 | Apache-2.0 |
| `shadow_dexee` | 12 | 12 | 12 | motor×12 | no | none | 26 | Apache-2.0 |
| `shadow_hand` | 31 | 30 | 20 | position×20 | yes | none | 13 | Apache-2.0 |
| `sharpa_wave` | 22 | 22 | 22 | position+kv×22 | no | none | 54 | Apache-2.0 |
| `skydio_x2` | 7 | 6 | 4 | motor×4 | yes | hover | 1 | Apache-2.0 |
| `stanford_tidybot` | 18 | 18 | 11 | position+kv×11 | no | home, retract | 20 | MIT |
| `tetheria_aero_hand_open` | 16 | 16 | 7 | position×7 | no | home | 27 | Apache-2.0 |
| `toddlerbot_2xc` | 51 | 50 | 30 | motor×30 | yes | home | 47 | MIT |
| `toddlerbot_2xm` | 51 | 50 | 30 | motor×30 | yes | home | 47 | MIT |
| `trossen_vx300s` | 8 | 8 | 7 | position×7 | no | home | 10 | custom/see LICENSE |
| `trossen_wx250s` | 8 | 8 | 7 | position+kv×7 | no | home | 10 | custom/see LICENSE |
| `trossen_wxai` | 16 | 16 | 14 | position×14 | no | left/, right/ | 84 | BSD |
| `trs_so_arm100` | 6 | 6 | 6 | position+kv×6 | no | home, rest | 18 | Apache-2.0 |
| `ufactory_lite6` | 6 | 6 | 6 | position+kv×6 | no | home | 14 | custom/see LICENSE |
| `ufactory_xarm7` | 13 | 13 | 8 | position+kv×8 | no | home | 16 | custom/see LICENSE |
| `umi_gripper` | 8 | 8 | 7 | position×1, position+kv×6 | no | none | 6 | MIT |
| `unitree_a1` | 19 | 18 | 12 | position×12 | yes | home | 5 | BSD |
| `unitree_g1` | 36 | 35 | 29 | position+kv×29 | yes | stand | 35 | custom/see LICENSE |
| `unitree_go1` | 19 | 18 | 12 | position×12 | yes | home | 5 | BSD |
| `unitree_go2` | 19 | 18 | 12 | motor×12 | yes | home | 16 | custom/see LICENSE |
| `unitree_h1` | 26 | 25 | 19 | motor×19 | yes | home | 21 | custom/see LICENSE |
| `unitree_z1` | 6 | 6 | 6 | position+kv×6 | no | home | 7 | BSD |
| `universal_robots_ur10e` | 6 | 6 | 6 | position+kv×6 | no | home | 20 | custom/see LICENSE |
| `universal_robots_ur5e` | 6 | 6 | 6 | position+kv×6 | no | home | 20 | custom/see LICENSE |
| `wonik_allegro` | 23 | 22 | 16 | position×16 | yes | none | 11 | custom/see LICENSE |


## Appendix C: Sensor Encyclopedia — Specs, Strengths and Weaknesses, Fusion, and Market Trends

The reference section supporting the main text's claim that observation design is sensor selection.

![Sensor comparison radar](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_sensor_compare.png)
*Figure: qualitative comparison of the 5 major sensors (summarized from Appendix C's real spec tables). No sensor does everything — which is why you end up mixing them (fusion)*

Figures come from a survey as of 2026-08, with a source attached to each item (official datasheets preferred; values we could not confirm are left marked "unconfirmed" — a document is more honest when you can see what is not filled in than when guesses fill it).

### 1. Major Sensors: Specs, Strengths, and Weaknesses

**Summary for the article (5 lines)**

1. A humanoid's "eyes" cannot be one kind of sensor — the world becomes visible only by layering LiDAR (accurate distance), depth cameras (dense near-field 3D), an IMU (attitude), and joint encoders (your own body).
2. The Livox Mid-360 — 360°×(-7° to +52°) FOV, 200k points/s, 265 g, street price $750–900 — has become the de facto LiDAR for research robots (the industrial-grade Hesai XT16, an order of magnitude up, is $6,650).
3. The Intel RealSense D435i is an 87°×58°-FOV active IR stereo unit with built-in IMU at $334; RealSense Inc., spun off from Intel in 2025, is refreshing the line toward the D500 series.
4. Event cameras (Sony IMX636) offer μs-class temporal resolution and 120 dB (low-light conditions) of dynamic range, but eval kits still cost several hundred thousand yen — the "next leading candidate" stage.
5. IMUs span 3 orders of magnitude in price across grades (consumer a few dollars → tactical $8,000+), while GPS-free 60-second position error shrinks by 2 orders, 400 m → 5 m — the standard play for legged robots is consumer-to-industrial IMUs plus fusion with other sensors.

#### 1.0 Cross-Comparison Table (From a Humanoid-Mounting Perspective)

| Sensor | Principle (1 line) | Good at | Bad at | Representative models and prices | Typical uses |
|---|---|---|---|---|---|
| Spinning/hemispherical LiDAR | Measures distance directly by laser time-of-flight (ToF) | Distance accuracy (cm-class), darkness, wide FOV | Rain/fog/snow, black low-reflectance surfaces, glass | Livox Mid-360 $749– / Unitree L2 $419 / Hesai XT16 $6,650 | SLAM, obstacle avoidance, all-around perception |
| Depth camera (active IR stereo) | IR pattern projection + left/right camera disparity for depth | Dense near-field 3D, cheap, simultaneous RGB | Direct sunlight (the IR loses), long range, transparent/mirror surfaces | RealSense D435i $334 / Orbbec Gemini 335 $264 | Footing terrain, manipulation |
| Stereo camera (passive) | Depth from left/right disparity alone (+ neural depth of late) | Outdoors, mid-range with long baselines, no projector needed | Textureless surfaces (white walls), darkness | ZED 2i $499– / ZED X $549– (search-result values) | Outdoor navigation, automotive-style perception |
| ToF camera | Distance at every pixel simultaneously from the phase shift of modulated light | Dense indoor depth, wide FOV | Direct sunlight, black low-reflectance, multipath | Orbbec Femto Bolt $418 | Indoor mapping, gestures |
| Event camera (DVS) | Each pixel asynchronously outputs only the instants brightness changes | Fast motion, HDR (backlight/tunnels), low latency | Static scenes (nothing comes out), existing CV assets don't apply | Prophesee EVK4 ≈$5,400 (distributor) / iniVation DVXplorer €3,900 | Fast avoidance, drone detection, vibration monitoring |
| IMU (MEMS) | Inertial measurement of angular velocity and acceleration | High rate (kHz-class), self-contained | Drift (position diverges on its own) | BMI088 a few dollars / ADIS16470 $482 / HG4930 $8,300– | Attitude estimation; the backbone of LIO/VIO |
| 6-axis F/T sensor | 3 forces + 3 moments via strain gauges etc. | Direct ZMP computation, force control | Expensive, weak to shock/EMI | ATI Axia80 (quote-only) / Robotiq FT 300-S kit $5,720 | Ankle ground-reaction force, grip-force control |
| Tactile skin | Imaging of gel deformation (vision-based touch) or magnetic 3-axis arrays | Slip detection, fine geometry, material | Cost per area, wiring, durability | GelSight Mini $499 / Meta Digit 360 (price unannounced) | Fingertip grasping, contact manipulation |
| Ultrasonic | Round-trip time of a sound wave | Sees transparent objects and glass too, a few dollars | Coarse resolution, wide directivity | HC-SR04 a few dollars | Proximity-bumper duty |
| GNSS/RTK | Satellite positioning + base-station correction | cm-class absolute position outdoors | Not viable indoors or in urban canyons | u-blox ZED-F9P board $259.95 | Outdoor navigation, ground truth |
| Joint encoder | Direct magnetic/optical readout of joint angle | High resolution (17–23 bit), low latency | Sees nothing of the outside world | (built into the machine) | Proprioception = the foundation of control |

---

#### 1.1 LiDAR

##### Livox Mid-360 (Most Important — In Detail)

Method: non-repetitive scanning plus a rotating mechanism for 360° horizontal coverage — Livox's own scheme in which point fill within the FOV increases over time.

| Item | Value | Source |
|---|---|---|
| FOV | Horizontal 360° / vertical **-7° to +52°** (officially confirmed) | https://www.livoxtech.com/mid-360/specs |
| Points/s | 200,000 pts/s (first return) | Ibid. |
| Range | 40 m @ 10% reflectivity / 70 m @ 80% reflectivity (both at 100 klx ambient light) | Ibid. |
| Range precision (1σ) | ≤2 cm @ 10 m (≤3 cm at close range, 0.2 m) | Ibid. |
| Angular precision | < 0.15° (1σ) | Ibid. |
| Mass | 265 g | Ibid. |
| Power | 6.5 W average (peak 14 W in self-heating mode) | Ibid. |
| Frame rate | 10 Hz (typical) | Ibid. |
| Wavelength | 905 nm | Ibid. |
| IMU | Built in (ICM40609) | Ibid. |
| Interface | 100BASE-TX Ethernet, PTPv2/GPS time sync supported | Ibid. |
| Price | Official sample price $749 (at the 2023-01 launch; DJI store search results also $749) | https://www.livoxtech.com/news/mid360_launch / https://store.dji.com/product/livox-mid-360 |
| Street price | US distributor $899 (backorder); AliExpress street $480–550 (2025 purchase reports, unofficial) | https://www.roboticscenter.ai/store/product/livox-dji-livox-mid-360 / https://www.aliexpress.com/s/wiki-ssr/article/livox-mid-360-price-usd-2025 |

- Good at: low price, light weight, built-in IMU, all-around FOV. FAST-LIO2 / Point-LIO ship official config files for it (see below) — LIO runs straight out of the box.
- Bad at: vertically it looks down only to -7° (the G1 school covers directly underfoot with a depth camera). Being 905 nm optical, rain, fog, and black low-reflectance surfaces are unfavorable in principle.
- Typical uses: 360° proximity perception and indoor/outdoor SLAM for quadrupeds/humanoids. The research-robot de facto.
- Also of note: Livox additionally ships the Avia (70.4°×77.2°, 240k pts/s, 450 m @ 80%, 498 g — drone surveying, https://www.livoxtech.com/avia/specs) and HAP (automotive, 120°×25°, 452k pts/s, 150 m @ 10% — https://www.livoxtech.com/hap/specs).

##### Competing LiDARs

| Product | Method | Range @10% reflectivity | Points/s | Mass | Street price | Source |
|---|---|---|---|---|---|---|
| Unitree L1 | Hemispherical "4D LiDAR" 360°×90° | Unconfirmed (max 30 m) | 21,600 | 230 g | **$249** (official) | https://shop.unitree.com/products/unitree-4d-lidar-l1 |
| Unitree L2 | Hemispherical 360°×96° | Unconfirmed (max 30 m) | 64,000 (official; some retailers list 128,000 — mismatch, so the official value is adopted) | Unconfirmed | **$419** (official) | https://shop.unitree.com/products/unitree-4d-lidar-l2 |
| Livox Mid-360 | Non-repetitive 360°×59° | 40 m | 200,000 | 265 g | $749–899 | See above |
| Hesai JT16 | 16ch mini-dome 360°×40° | 30 m | 48,000 | 199.7 g / 4.3 W | €599 (sale; normally €739) | https://www.hesaitech.com/product/jt16/ / https://openelab.io/products/hesai-jt16-mini-3d-lidar |
| Hesai XT16 | 16ch mechanical spinning 360°×30° | Unconfirmed (0.05–120 m; sibling XT32M does 80 m @10%) | 320,000 | 800 g | **$6,650** (US distributor) | https://www.hesaitech.com/product/xt16-32-32m/ / https://robostore.com/products/hesai-xt16-3d-lidar |
| Ouster OS0 | Digital LiDAR (SPAD+ASIC), up to 128ch, 90° vertical | 35 m | 10,400,000 | Unconfirmed | Inquiry only (reference: OS1-32 was $8,000 at announcement) | https://ouster.com/products/hardware/os0-lidar-sensor |
| Ouster OS1 | Same, 128ch, 45° vertical | 90 m | 10,400,000 | Unconfirmed | Inquiry only | https://ouster.com/products/hardware/os1-lidar-sensor / https://www.geoweeknews.com/articles/32-channel-lidar-for-8k-ousters-newest-lidar-finds-a-sweet-spot/ |

Notes on individual entries:

- **Hesai XT16**: ±1 cm accuracy / 0.5 cm (1σ) precision, with zero blind spot as the selling point — industrial grade. Aimed at AGV/AMR and cm-class indoor/outdoor navigation (https://www.hesaitech.com/product/xt16-32-32m/).
- **Hesai JT16**: the CES-announced robot-oriented mini-dome. At 200 g and IP6K6, a direct Mid-360 competitor. Targets cleaning and delivery robots.
- **Ouster OS series**: "digital LiDAR" that integrates the receiver side into SPAD + a custom ASIC. Its 10.4 M pts/s point density is 50× the Mid-360, but price and mass are a different class. The OS0's 90° vertical FOV is strong for floor-to-ceiling perception by warehouse robots. Accuracy, mass, power, and street price for the current Rev7/8 are not on the official pages (unconfirmed; datasheets at https://ouster.com/downloads ).
- **The state of Velodyne (fact-checked)**: Velodyne completed a merger of equals with Ouster on 2023-02-10; the surviving company is Ouster (NYSE: OUST). Former Velodyne shares were delisted (1 share = 0.8204 Ouster shares). Sources: https://investors.ouster.com/news-releases/news-release-details/ouster-and-velodyne-complete-merger-equals-accelerate-lidar / https://www.therobotreport.com/lidar-makers-ouster-velodyne-complete-merger/

#### 1.2 Depth Cameras

##### Intel RealSense D435i (Most Important — In Detail)

Method: active IR stereo (IR pattern projector + disparity between left and right IR cameras).

| Item | Value | Source |
|---|---|---|
| Depth FOV | **87°×58° (officially confirmed)**. Datasheet precise values 87°±3° × 58°±1° (diagonal 95°±3°) | https://www.intel.com/content/www/us/en/products/sku/190004/intel-realsense-depth-camera-d435i/specifications.html / https://cdrdv2-public.intel.com/841984/Intel-RealSense-D400-Series-Datasheet.pdf |
| Depth range | Ideal 0.3–3 m (Min-Z ≈ 28 cm; 0.105 m at 848×480). Beyond 3 m possible, with degraded accuracy | https://www.realsenseai.com/products/depth-camera-d435i/ |
| Depth resolution/fps | Up to 1280×720 / up to 90 fps | Ibid. |
| Depth accuracy | <2% @ 2 m | Ibid. |
| RGB | 1920×1080 @30 fps (rolling shutter) | Ibid. |
| IMU | **Bosch BMI055 (6-axis) built in — confirmed** | https://github.com/realsenseai/librealsense/blob/master/doc/d435i.md |
| Mass | ≈72 g (distributor value; not on the current official page) | https://framos.com/products/3d/3d-cameras/depth-camera-d435i-bulk-22610/ |
| Dimensions/interface | 90×25×25 mm, USB-C 3.1 Gen 1 | https://www.realsenseai.com/products/depth-camera-d435i/ |
| Price | **$334.00 (official store)** | https://store.realsenseai.com/buy-intel-realsense-depth-camera-d435i.html |

The state of the RealSense business:

- Intel announced a scale-down in 2021, but the D400 line continued. **The spin-out from Intel as RealSense Inc. completed on 2025-07-11**, with a $50M Series A (Intel Capital and MediaTek Innovation Fund participating). Sources: https://www.realsenseai.com/news-insights/news/realsense-completes-spin-out-from-intel-raises-50-million-to-accelerate-ai-powered-vision-for-robotics-and-biometrics/ / https://www.tomshardware.com/tech-industry/realsense-completes-spin-out-from-intel-gets-usd50-million-in-funding-from-intel-capital-and-mediatek
- First post-independence release = the **D555** (D500 series): Vision SoC V5 (5 TOPS), PoE power + global shutter. Source: https://www.vision-systems.com/embedded/article/55303384/intel-completes-realsense-spinoff
- The company claims adoption in "60% of the world's AMRs/humanoids" (self-reported figure).

##### Competing Depth Cameras

| Product | Method | Depth specs | Price | Source |
|---|---|---|---|---|
| Orbbec Gemini 335 | Active stereo (MX6800 ASIC) | 0.1–20 m+, 1280×800@30fps, FOV 90°×65° | **$264** (official store) | https://store.orbbec.com/products/gemini-335 |
| Orbbec Gemini 335L | Same, 95 mm baseline, IP65 | Accuracy ≤0.8% @ 2 m | $359 | https://www.hackster.io/news/orbbec-unveils-the-robust-fakra-connectable-gemini-335lg-depth-camera-for-autonomous-robots-and-more-e23d922b5158 |
| Orbbec Femto Bolt | Microsoft iToF (same depth technology as Azure Kinect) | 0.25–5.46 m, WFOV 120°×120°, RGB 4K, IMU built in | **$418** (official store) | https://store.orbbec.com/products/femto-bolt |
| Stereolabs ZED 2i | Passive stereo + Neural Depth | 0.2–20 m, 110° wide angle, IMU + barometer + magnetometer | $499– (search-result value, recheck needed) | https://store.stereolabs.com/products/zed-2i/ |
| Stereolabs ZED X | Same (Gen2) + global shutter | 0.3–20 m (2.2mm) / 1–35 m (4mm), GMSL2 interface (Jetson assumed) | $549–599 (search-result values) | https://static.generation-robots.com/media/zed-x-datasheet-v1.2.pdf |

- **Azure Kinect DK EOL (fact-checked)**: Microsoft announced end of production in 2023-08, with sales ending October 2023; the SDK repository was archived 2024-08-22. As successors, under an official Microsoft partnership, Orbbec's Femto Bolt/Mega implement the licensed iToF technology (the same depth modes as Azure Kinect, with a K4A API-compatible wrapper). Sources: https://hackaday.com/2023/08/26/microsoft-discontinues-kinect-again/ / https://github.com/microsoft/Azure-Kinect-Sensor-SDK/issues/1971 / https://www.orbbec.com/microsoft-collaboration/ / https://www.orbbec.com/documentation/comparison-with-azure-kinect-dk/
- The Orbbec SDK has native ROS1/ROS2 support (https://store.orbbec.com/products/gemini-335le).

#### 1.3 Event Cameras (DVS)

Principle (1 line): each pixel independently and asynchronously outputs an event (x, y, timestamp, polarity) only at the instant its log-brightness change crosses a threshold — no frames are captured. Source: https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/

##### Prophesee / Sony IMX636

| Item | Value | Source |
|---|---|---|
| Development | Jointly developed by Sony (stacked BSI process) × Prophesee (event pixels) | https://www.prophesee.ai/2022/04/13/new-sony-imx636es-hd-sensor-realized-in-collaboration-between-sony-and-prophesee/ |
| Resolution / pixel pitch | **1280×720 / 4.86 μm (confirmed)** | https://www.prophesee.ai/wp-content/uploads/2024/05/IMX636-Product-Brief-2024-v3.0.pdf |
| Temporal resolution | Timestamp precision 1 μs, pixel latency <100 μs @1000 lux (equivalent to >10k fps) | Ibid. / https://www.prophesee.ai/event-camera-evk4/ |
| Dynamic range | **Official figures: >86 dB (typ) / >120 dB (low-light conditions, 0.08–100,000 lux)** — the "120 dB" is a value with measurement conditions attached | https://support.prophesee.ai/portal/en/kb/articles/evk4-hd-product-brief |
| Max event rate | ~1.06 Geps class (Sony figure) | https://www.sony-semicon.com/en/products/is/industry/evs.html |
| SDK | Metavision SDK (OSS build: OpenEB) | https://github.com/prophesee-ai/openeb |
| EVK4 eval kit | IMX636, USB 3.0, 30×30×36 mm, 40 g. Official direct sales are quote-based (unconfirmed); Taiwan distributor street price NT$175,000 ≈ **$5,400** | https://www.prophesee.ai/event-camera-evk4/ / https://store.edomtech.com/products/evk4 |

##### iniVation DVXplorer

| Item | Value | Source |
|---|---|---|
| Resolution | VGA 640×480 | https://docs.inivation.com/hardware/current-products/dvxplorer.html |
| Dynamic range | Up to 110 dB | Ibid. |
| Temporal resolution | 200 μs, latency <1 ms, up to 165 Meps | Ibid. |
| Price | **€3,900 (commercial) / €3,400 (academic)** | https://shop.inivation.com/collections/dvxplorer |

- Good at: fast motion (no motion blur), HDR environments (tunnel mouths, backlight), low power, μs-class low latency.
- Bad at: static scenes are invisible in principle (ego-motion or active lighting required) / frame-based CV and deep-learning assets don't apply directly — representation conversion needed (voxel grids, time surfaces, etc.) / the event rate is scene-dependent and bursty (design bandwidth and processing for the worst case).
- Data-rate character: output is scene-dependent and sparse. Near zero when static; can spike to Geps class under violent motion plus high texture.
- Typical uses: fast obstacle avoidance, drone detection/tracking, fast VO/SLAM, vibration monitoring, low-latency grasping.

#### 1.4 IMU (MEMS) — Grades and Drift

Four grades by industry convention. Position error grows roughly as time cubed, and the gyro's in-run bias instability is the dominant term (https://www.vectornav.com/resources/detail/what-is-an-inertial-navigation-system).

| Grade | Typical gyro bias instability | Position error after 60 s of GPS-free inertial navigation | Typical uses |
|---|---|---|---|
| Consumer | ~100 °/h | **400 m** | Phones, drone FCs, hobby |
| Industrial | ~10 °/h | **40 m** | Robots, agricultural machinery, AGVs |
| Tactical | ~1 °/h | **5 m** | UAVs, military, surveying |
| Navigation | ~0.01 °/h | **50 cm** | Aircraft, ships, submarines |

(Source: VectorNav, above. Note that grade definitions have no strict standard across vendors — https://ez.analog.com/mems/w/documents/4111/what-does-tactical-grade-mean-for-a-mems-imu )

Measured specs of representative devices:

| Device | Grade | Gyro bias instability | Noise | Price | Source |
|---|---|---|---|---|---|
| Bosch BMI088 | Consumer (drone-oriented) | Not in the datasheet (a forum answer cites <2 °/h — flyer value) | gyro 0.014 °/s/√Hz | A few dollars (unit price unconfirmed) | https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi088-ds001.pdf |
| TDK ICM-42688-P | Consumer (FPV staple) | Not in the datasheet | gyro 2.8 mdps/√Hz | A few dollars (unconfirmed) | https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/ds-000347-icm-42688-p-v1.6.pdf |
| ADI ADIS16470 | Industrial | **8 °/h** | 0.008 °/s/√Hz | **$481.53** (DigiKey) | https://www.analog.com/media/en/technical-documentation/data-sheets/adis16470.pdf / https://www.digikey.com/en/products/detail/analog-devices-inc/ADIS16470AMLZ/7932982 |
| ADI ADIS16490 | Tactical | **1.8 °/h** | ARW 0.09 °/√h | Thousands of dollars (unconfirmed) | https://www.analog.com/media/en/technical-documentation/data-sheets/adis16490.pdf |
| Honeywell HG4930 | Tactical | **0.25 °/h** | ARW 0.04 °/√h | **$8,300–$13,500** (DigiKey, by part number) | https://media.digikey.com/pdf/data%20sheets/honeywell%20pdfs/hg4930_perfandenvriomanual_jul2017.pdf / https://www.digikey.com/en/products/detail/honeywell-aerospace/HG4930CA51/6562993 |

- Bottom line: consumer → tactical is 3 orders of magnitude in price for 2+ orders of improvement in bias instability. 400 m vs 5 m over 60 seconds without GPS.
- Adoption examples: the Pixhawk 6X (Rev 8) runs triple-redundant ICM-45686 ×3 — consumer-grade IMUs operated via redundancy + fusion (https://www.getfpv.com/electronics/flight-controllers/holybro-pixhawk-6x-fc-v2a-standard-set-icm-45686.html). The Unitree G1 discloses only "6-axis IMU"; part number and grade unconfirmed (https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications).
- Typical uses: attitude estimation; the predict step of LIO/VIO. For legged robots the key is handling landing impacts (high bandwidth, saturation) — see Point-LIO below.

#### 1.5 Force/Torque, Foot Soles, and Touch

##### 6-Axis F/T Sensors

| Product | Principle | Specs | Price | Source |
|---|---|---|---|---|
| ATI (now Novanta) Axia80 | Silicon strain gauges (75× the signal strength of foil gauges) | Force ~500 N / torque ~20 Nm, 5–12.5× overload tolerance, EtherCAT/Ethernet | Quote-based (unconfirmed; reputedly several thousand dollars on the market) | https://ati.novanta.com/product/axia80-force-torque-sensor-kit/ |
| Robotiq FT 300-S | "Wear-free sensing technology" (whether capacitive is not officially stated = unconfirmed) | ±300 N / ±30 Nm, 100 Hz, IP65, 500% overload | Kit **$5,720** (distributor) | https://robotiq.com/products/ft-300-force-torque-sensor / https://www.kingbarcode.com/FTS-300-S-KIT-001 |

##### Humanoid Sole Contact Detection — 3 Approaches Compared

| Method | Information obtained | Pros | Cons | Adoption examples |
|---|---|---|---|---|
| Ankle 6-axis F/T | 3 forces + 3 moments of ground reaction → direct ZMP computation | Ideal for ZMP control, high precision | Expensive, heavy, weak to landing shock/EMI | ASIMO, HRP-4, etc. (research-literature basis: https://www.researchgate.net/publication/257672554_Signal_Processing_and_Application_of_Six-axis_ForceTorque_Sensor_Integrated_in_Humanoid_Robot_Foot ) |
| Sole pressure distribution (FSR/pressure mat) | Normal-direction pressure distribution | Cheap, thin, shows the contact-patch shape | No shear forces/moments, hysteresis | Widely used in hobby/research machines (no individual primary source confirmed) |
| Joint current (torque) estimation | External force estimated from joint torques | No extra sensor, zero cost | Precision limited by gearbox friction | The recent trend in mass-produced humanoids |

- **Unitree G1**: the published specs list no sole force sensor (the sensor table shows only depth camera / 3D LiDAR / microphones / joint encoders / IMU) → contact detection is presumably joint-side estimation (not confirmed as definite). Source: https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications

##### Tactile Skins

| Product | Principle | Status and price | Source |
|---|---|---|---|
| GelSight Mini | Vision-based touch (camera images the gel's deformation) | On general sale at **$499** (replacement gel $49). The most widespread in research | https://www.gelsight.com/gelsightmini/ |
| Meta Digit 360 | All-around fingertip vision-touch + multimodal (1 mN force detection) | Manufactured by GelSight. Announced 2024-10, price unannounced (unconfirmed) | https://www.businesswire.com/news/home/20241031980322/en/GelSight-and-Meta-AI-Introduce-Digit-360-Tactile-Sensor |
| uSkin (XELA Robotics) | Magnetic 3-axis (normal + shear) high-density arrays | In commercial rollout (2025-12 Tesollo DG-5F integration, CES 2026 demo). Price unannounced | https://roboticsandautomationnews.com/2025/12/04/xela-robotics-adds-high-precision-tactile-sensing-to-tesollo-robot-hand/97352/ |

#### 1.6 The Rest (Briefly)

- **ToF cameras**: distance at all pixels at once from the phase of modulated light. The Orbbec Femto Bolt has systematic error <11 mm + 0.1% of distance, σ≤17 mm (https://www.orbbec.com/products/tof-camera/femto-bolt/). Strong for dense indoor depth; weak to direct sunlight, black low-reflectance surfaces, and multipath.
- **Ultrasonic**: the HC-SR04 covers 2 cm–4 m with 0.3 cm resolution for a few dollars (https://www.dfrobot.com/blog-13482.html). The differentiator: it reacts to transparent objects and glass, which optical sensors struggle with.
- **GNSS/RTK**: the u-blox ZED-F9P achieves 1 cm horizontal with RTK (2.5 m standalone). $259.95 on a SparkFun board (https://www.sparkfun.com/sparkfun-gps-rtk2-board-zed-f9p-qwiic-gps-15136.html). cm-class requires a base station or NTRIP corrections. Ideal for ground truth in outdoor experiments.
- **Joint encoders**: absolute 17 bit = 131,072 divisions/revolution; 23 bit ≈ 8.39 million (https://www.dynapar.com/knowledge/encoder-basics/encoder-resolution/single-turn-vs-multi-turn-encoders/). Humanoid joints are predominantly absolute-type. The Unitree G1 has dual encoders on each joint (motor side + output side) (https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications).

---

### 2. Sorting Out Multi-Sensor Fusion Methods

**Summary for the article (5 lines)**

1. The fusion classic is "sequential Bayesian estimation weighted by each sensor's error characteristics (covariance)" — the Kalman filter (EKF/UKF) — and ROS's robot_localization is its de facto standard implementation.
2. LiDAR-inertial odometry (LIO — accumulating motion increments into self-position) evolved from the factor-graph LIO-SAM (2020) → iterated-EKF + ikd-Tree FAST-LIO2 (2021, 100 Hz) → per-point-update Point-LIO (2023, 4–8 kHz), and all of them ship official Mid-360 configurations.
3. On the learning side, the main currents are BEVFusion (2022), which mixes camera + LiDAR in a bird's-eye-view (BEV) feature space, and robustification via modality dropout — dropping an entire sensor channel during training.
4. The legged-robot monument is teacher-student distillation: a teacher that sees privileged in-sim information (contact forces, terrain) is distilled into a student that uses only the proprioception available on hardware (Lee et al. 2020 / Miki et al. 2022, Science Robotics).
5. Real humanoids split into a "LiDAR + depth camera" camp (Unitree, Agility) and a "camera-purist" camp (Tesla, Figure); reports of LiDAR being removed from the production Atlas suggest a merge into the camera camp.

#### 2.1 Classics: Kalman Filters and Factor Graphs

##### EKF / UKF

| Item | EKF | UKF |
|---|---|---|
| Handling nonlinearity | First-order linearization via Jacobians | Pass sigma points straight through the nonlinear function (unscented transform) |
| Pros | Light, vast track record | Second-order accuracy, no Jacobian derivation needed |
| Cons | Prone to divergence under strong nonlinearity or large attitude error | Somewhat heavier |

- Typical setup: IMU (high-rate, drifting) for prediction; encoders and GNSS (absolute, low-rate) integrated as observations. ROS standard implementation = robot_localization (supports both EKF/UKF): https://github.com/cra-ros-pkg/robot_localization
- The essence: sequential Bayesian estimation that blends complementary sensors weighted by their error covariances.
- Bibliography: Kalman 1960 is the original; the UKF is Julier & Uhlmann 1997 (primary URL unconfirmed).

##### Factor Graphs / the LIO Lineage

| Method | Year/authors | Key idea | Performance claim | URL |
|---|---|---|---|---|
| GTSAM | Georgia Tech Borg Lab (iSAM2: Kaess et al., IJRR 2012) | C++ foundation for factor graphs + Bayes trees. Provides IMU preintegration factors | Incremental updates via iSAM2 | https://github.com/borglab/gtsam |
| LIO-SAM | 2020 IROS / Tixiao Shan et al. (MIT/Stevens) | LiDAR-inertial formulated as a factor graph (uses GTSAM). Loop closure and GPS can be added as factors | Real-time, high-accuracy trajectory + map | https://github.com/TixiaoShan/LIO-SAM / https://arxiv.org/abs/2007.00258 |
| FAST-LIO2 | 2021 arXiv / 2022 T-RO / Wei Xu, Fu Zhang et al. (HKU MARS) | Registers raw point clouds directly with no feature extraction. Tightly-coupled iterated EKF + incremental kd-tree, ikd-Tree | "Higher accuracy at far lower compute than SOTA," "up to 100 Hz" | https://github.com/hku-mars/FAST_LIO / https://arxiv.org/abs/2107.06829 |
| Point-LIO | 2023 Advanced Intelligent Systems / He, Xu, Zhang et al. (HKU MARS) | Updates state per point, eliminating in-frame distortion by principle. Treats the IMU as an "output," keeping estimation alive even under saturation | 4–8 kHz odometry; operates through violent motion at 75 rad/s angular velocity | https://github.com/hku-mars/Point-LIO / https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202200459 |

- **Mid-360 support**: the FAST-LIO repository carries an official `config/mid360.yaml` (https://github.com/hku-mars/FAST_LIO/blob/main/config/mid360.yaml), and Point-LIO, from the same lineage, provides Mid-360 configs too — the ecosystem where LIO runs as-is on the G1's standard Mid-360 is fully stocked.
- Rules of thumb: want loop closure and GPS integration → LIO-SAM / thin compute or fast maneuvering → FAST-LIO2 / vibration and violent motion like a legged robot's foot strikes → Point-LIO.

#### 2.2 Learning-Based

##### BEV Fusion

| Paper | Origin | Key idea | URL |
|---|---|---|---|
| BEVFusion (MIT version) | MIT Han Lab, 2022 (ICRA 2023) | Brings both camera and LiDAR features into a shared BEV space and fuses them. BEV pooling optimization speeds the view transform 40×+. Multi-task capable | https://arxiv.org/abs/2205.13542 / https://github.com/mit-han-lab/bevfusion |
| BEVFusion (PKU version, same-name different paper) | Peking University + Alibaba, NeurIPS 2022 | BEV-izes the camera stream and LiDAR stream independently, then fuses. Training with simulated LiDAR failure claims SOTA +15.7–28.9% mAP | https://arxiv.org/abs/2205.13790 / https://github.com/ADLab-AutoDrive/BEVFusion |

##### Modality Dropout (Robustness to Sensor Loss)

- The idea: where ordinary dropout deletes neurons, drop one entire sensor channel during training (zero-fill/mask) → the network learns internal representations in which "the remaining sensors compensate," surviving real-world sensor failure and occlusion. Overview: https://www.emergentmind.com/topics/modality-dropout
- Representative examples: the PKU BEVFusion's failure-inclusive training (above) / MoME (2025, reporting NDS 87.9% retained under total camera loss — https://arxiv.org/abs/2503.19776) / precursor Sensor Dropout (Liu et al., CoRL 2017 — https://arxiv.org/abs/1705.10422 , details unverified).

##### Privileged Learning / Teacher-Student Distillation (the Legged-Robot Monument)

| Paper | Citation | Key idea | URL |
|---|---|---|---|
| Lee et al. "Learning quadrupedal locomotion over challenging terrain" | Science Robotics Vol.5, Issue 47, eabc5986, 2020-10-21 | The teacher trains via RL on privileged information available only in sim (contact state, contact forces, terrain shape, friction) → the student imitates the teacher from only the proprioceptive history usable on hardware (joint angles, IMU). A blind ANYmal traverses mud, snow, vegetation, rubble | https://doi.org/10.1126/scirobotics.abc5986 / https://arxiv.org/abs/2010.11251 |
| Miki et al. "Learning robust perceptive locomotion for quadrupedal robots in the wild" | Science Robotics Vol.7, Issue 62, eabk2822, 2022 | Integrates exteroception (height maps) + proprioception with an attention-based recurrent belief-state encoder. When external sensing turns unreliable, weight shifts automatically to the proprioceptive side = a "learned fusion gate." ANYmal completes a 1-hour Alpine hiking route | https://www.science.org/doi/10.1126/scirobotics.abk2822 |

- Humanoid imports: Humanoid Parkour Learning (Zhuang et al., CoRL 2024) zero-shot-transferred a distilled policy to the Unitree H1 (https://arxiv.org/abs/2406.10759). ExBody2 does whole-body tracking on H1/G1 via teacher-student distillation (said to be arXiv:2412.13196, primary confirmation pending). The construct established on quadrupeds is flowing straight into 2024–2026 humanoid RL locomotion.

#### 2.3 Sensor Suites of Real Humanoids (Published Information)

| Machine | Sensor suite (as published) | Source | Notes |
|---|---|---|---|
| Unitree G1 | Official spec sheet lists "Depth Camera + 3D LiDAR" + 4-ch mic array + speaker | https://www.unitree.com/g1 | **The official page names no models**. The Livox Mid-360 + RealSense D435(i) part numbers appear on the distributor/technical-doc side (https://docs.quadruped.de/projects/g1/html/g1_overview.html) |
| Unitree H1 | Official: "360° depth perception via 3D LIDAR + Depth Camera" | https://www.unitree.com/h1 | Part numbers not officially listed (distribution info says Mid-360 + D435i) |
| Tesla Optimus | Camera-centric (Autopilot-derived vision) + fingertip touch + sole force/torque. "8 cameras" is a third-party review figure with no official primary source confirmed | https://briandcolwell.com/a-complete-review-of-teslas-optimus-robot/ | LiDAR-free, camera-purist line |
| Figure 02 / 03 | 02: 6 RGB cameras + VLM (primary-page statement of "6" unconfirmed). 03: palm cameras + tactile sensors officially announced | https://www.figure.ai/news/introducing-figure-03 | No LiDAR; vision + touch line |
| Boston Dynamics new Atlas (electric) | 2024 research build: ToF + RGB-D/stereo + LiDAR, IMU at 1 kHz, joint encoders at 4 kHz (third-party roundup). The 2026 production version reportedly drops LiDAR for a 360° camera + touch configuration | https://www.aparobot.com/robots/atlas | No official primary sensor spec sheet exists (treated as unconfirmed) |
| Agility Digit | Velodyne VLP-16 (torso top) + RealSense depth cameras ×4 (incl. D430 ×2 front/rear on the pelvis). LiDAR = distant mapping/obstacles; depth cameras = footing surface estimation | https://robotsguide.com/robots/digit / https://agilityrobotics.com/content/check-out-these-big-advancements-in-digits-development | The flagship of the classic LiDAR + depth fusion suite |

Observation: the industry splits in two — ① the LiDAR + depth camera camp (Unitree, Agility, the research Atlas), which can reuse §2.1's LIO assets as-is; ② the camera purists (Tesla, Figure), estimating geometry with learning (§2.2). The production Atlas dropping LiDAR suggests convergence toward ②.

#### 2.4 "At Which Layer Do You Mix?" — Early / Mid / Late Fusion (a 3-Step Plain-Language Take)

##### ① An Analogy (Cooking)

- **Early fusion (mix the raw data)** = put every ingredient into the same pot from the start. The flavors marry beautifully — but one rotten ingredient ruins the whole pot.
- **Mid fusion (mix the features)** = prep each ingredient separately, then combine. Easier to combine, and a bad ingredient gets caught during prep.
- **Late fusion (mix the conclusions)** = three chefs each cook a finished dish, and the judges take a vote. One can fail and the meal recovers — but no chemistry ever happens between ingredients.

##### ② The Engineering Explanation

| Layer | What gets mixed | Pros | Cons |
|---|---|---|---|
| Early (raw) | Raw point clouds, raw pixels, raw IMU values | Zero information loss. Exploits correlation to the fullest (e.g., Point-LIO updates state with the IMU per individual LiDAR point) | Extremely sensitive to time sync and extrinsic calibration. Rate gaps (IMU at hundreds of Hz vs camera at 30 Hz) are hard to absorb. One sensor's failure contaminates the whole |
| Mid (features) | Feature maps, BEV features, embeddings | Fuses densely while using the best encoder per modality. BEVFusion and Miki 2022's belief encoder both live at this layer | Requires designing a shared representation space. Weak to out-of-distribution dropouts → reinforce with modality dropout |
| Late (decisions) | Each pipeline's estimates (positions, detections, verdicts) | Modules stay independent — easy to develop, verify, and swap. Natural fault isolation (fusing LIO output + GNSS + odometry in an EKF is this layer) | Information each pipeline discarded never comes back. Arbitration is hard when the verdicts disagree |

##### ③ Implementation Considerations

- **Time synchronization is the foundation of everything**: the earlier you fuse, the more you need PTP/hardware-trigger-class sync. The Mid-360 has its IMU built in and pre-synchronized, which makes early fusion (LIO) easy.
- **Propagation of calibration error**: at early/mid, errors in the inter-sensor extrinsics smear into the feature space and poison learning. Late keeps them contained within each pipeline.
- **Failure-mode design**: late makes degraded operation easy to design (LiDAR dies → continue at reduced speed on cameras alone). If you want equal robustness at mid, always train with modality dropout (the PKU BEVFusion lesson).
- **Compute budget and rates**: early runs at the fastest sensor's rate (Point-LIO at 4–8 kHz). The real-hardware standard is a hybrid, layer by layer: state estimation wired into the control loop = early/classic; semantic understanding = mid/learned; action decisions and redundancy = late (example: G1 = Mid-360 + IMU early-fused by FAST-LIO2 → depth-camera detections overlaid at mid/late).

---

### 3. Market Trends (2024–2026)

**Summary for the article (5 lines)**

1. Humanoid market forecasts span nearly two orders of magnitude across investment banks, from Goldman Sachs's "$38 billion by 2035" (revised upward 6× in 2024) through Morgan Stanley's "$5 trillion TAM by 2050" to Citi's "$7 trillion by 2050."
2. China's MIIT published its industrial policy — "mass production in 2025, world-leading level by 2027" — in 2023-11, and the China Commercial Industry Research Institute estimates 2025 Chinese shipments at 14,400 units = 84.7% of the world (as of 2026).
3. LiDAR is mid-price-collapse — Mid-360 $749, Unitree L1 $249; Hesai is mass-producing the "roughly $200 ATX" with 2025 shipment guidance of 1.2–1.5 million units. Yole revised its revenue forecast downward citing "not fewer shipments — plunging unit prices."
4. Event-camera standard-bearer Prophesee entered court-supervised restructuring in 2024-10 → changed CEO → in 2026-06 raised €20M and announced the Mantara drone-detection system, rebuilding under its own power (not an acquisition).
5. Beijing held the world's first humanoid half-marathon in 2025-04 (winner: Tiangong Ultra, 2:40:42) and the first World Humanoid Robot Games in 2025-08 (16 countries, 500+ robots); at the second marathon in 2026-04 a robot beat the human world record with 50:26, and the second Games opens 2026-08-22 (2,056 robots).
