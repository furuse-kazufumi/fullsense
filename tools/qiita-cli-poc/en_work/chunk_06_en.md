#### 3.1 Humanoid Robot Market Forecasts

##### Investment banks (in the form "Firm X, as of YYYY, predicts Z")

| Source | As of | Forecast | Reference |
|---|---|---|---|
| Goldman Sachs | 2024-02 | TAM of **$38 billion by 2035** (revised upward roughly 6x from the previous $6 billion forecast), 1.4 million units shipped (2035). Reasons for the revision: progress in end-to-end AI training and a 40% drop in component costs | https://www.goldmansachs.com/insights/articles/the-global-market-for-robots-could-reach-38-billion-by-2035 |
| Morgan Stanley | 2025-04 | **~1 billion units in operation and a humanoid-related TAM of $5 trillion by 2050** (revenue $4.7 trillion). ~13 million units in operation by 2035 | https://www.morganstanley.com/insights/articles/humanoid-robot-market-5-trillion-by-2050 / https://www.cnbc.com/2025/04/29/how-to-play-a-5-trillion-market-for-humanoid-robots-by-2050.html |
| Citi (Citi GPS) | 2024-12 to 2025 | **648 million units and a $7 trillion market by 2050**, 2035 TAM of $209 billion | https://www.citigroup.com/global/insights/the-rise-of-ai-robots |
| Bank of America | 2025-04 | Shipments: 90,000 units in 2026 → **1.2 million units in 2030** (86% CAGR), mass-market adoption starting 2028. 3 billion cumulative units in operation by 2060 | https://institute.bankofamerica.com/content/dam/transformation/humanoid-robots.pdf |
| UBS (for reference) | 2025-06 | 300 million units and $1.7 trillion by 2050 | https://www.benzinga.com/markets/tech/25/06/45996879/nvidia-tesla-honeywell-could-ride-1-7-trillion-robot-wave-as-ubs-sees-300-million-humanoids-by-2050 |

##### Market research firms

| Source | Forecast | Reference |
|---|---|---|
| Fortune Business Insights | $3.28 billion in 2024 → **$66 billion by 2032** (45.5% CAGR) | https://www.fortunebusinessinsights.com/humanoid-robots-market-110188 |
| MarketsandMarkets | $2.03 billion in 2024 → **$13.25 billion by 2029** (45.5% CAGR). A separate edition gives $50.27 billion for 2035 | https://www.prnewswire.com/news-releases/humanoid-robot-market-worth-13-25-billion-by-2029---exclusive-report-by-marketsandmarkets-302271115.html |
| AskCI Research Institute (China, as of 2026) | China market: ~1.55 billion yuan in 2025 → 3.4 billion yuan in 2026 → over 20 billion yuan in 2030. Shipments: 14,400 units in 2025 (84.7% of the world) → 380,000 units in 2030 | https://www.askci.com/news/chanye/20260629/090337278269501813828002.shtml |

- Caution: AskCI also published a separate report (2025-02) citing an "industry scale of 5.3 billion yuan for 2025"; "market scale" and "industry scale" use different definitions (the body of the 5.3-billion-yuan report returned a 503 error and could not be checked directly, so it remains partly unverified).

##### Chinese industrial policy (fact-checked)

- MIIT's "Guiding Opinions on the Innovative Development of Humanoid Robots" (工信部科〔2023〕193号) **really was published on 2023-11-02**. Goals: by **2025**, break through the key technologies (brain, cerebellum, limbs) and achieve mass production of complete units; by **2027**, establish the industry chain and reach world-leading level in overall strength. It explicitly calls for cultivating 2-3 globally influential ecosystem companies and 2-3 industry clusters.
- Sources: https://www.news.cn/tech/20231103/f76096318e964b13a8c31011de8cda2a/c.html / full text: https://www.ncsti.gov.cn/zcfg/zcwj/202311/t20231103_140346.html

#### 3.2 The LiDAR Price Collapse

| Item | Figure | Reference |
|---|---|---|
| Livox Mid-360 launch price | Sample price **$749** (launched 2023-01-10) | https://www.livoxtech.com/news/mid360_launch |
| Mid-360 current street price | AliExpress street price $480-550 (2025 purchase reports, unofficial) | https://www.aliexpress.com/s/wiki-ssr/article/livox-mid-360-price-usd-2025 |
| Unitree L1 / L2 | **$249 / $419** (official shop) | https://shop.unitree.com/products/unitree-4d-lidar-l1 / https://shop.unitree.com/products/unitree-4d-lidar-l2 |
| Hesai shipment volume | 222,000 units in 2023 → **over 500,000 in 2024** → 2025 guidance of **1.2-1.5 million units**. Cumulative 1 million units reached around 2025-10 | https://investor.hesaitech.com/news-releases/news-release-details/hesai-group-reports-fourth-quarter-and-full-year-2024-unaudited / https://optics.org/news/16/8/27 |
| Hesai ATX | CEO David Li stated it sells "**for about $200**." Mass production began Q1 2025 | https://optics.org/news/16/3/15 / https://www.hesaitech.com/hesai-launches-new-ultra-wide-fov-long-range-atx-lidar/ |
| Automotive LiDAR market (Yole) | **$860 million** in 2024 (+60% YoY), **~1.6 million units** shipped (of which ~1.5 million by Chinese makers). Yole revised its revenue forecast downward citing "not a drop in shipments but a faster-than-expected collapse in ASP" | https://www.yolegroup.com/strategy-insights/automotive-lidar-deployment-ramps-up-in-2024/ / https://optics.org/news/15/6/25 |

- How to back up "thousands of dollars → hundreds of dollars": a naive estimate from Yole's 2024 data gives an average unit price of ≈ $860M ÷ 1.6M units ≈ **$540/unit** (use it while stating explicitly that it is an estimate). A year-by-year ASP table versus the early mechanical LiDARs (Velodyne HDL-64E, etc.) that cost tens of thousands of dollars sits inside Yole's paid report and is unverified. In the article, the safe way to tell the story is the combination of "Yole's downward revision due to the ASP collapse + the estimate above + Hesai ATX at $200."
- The structure by which low-cost LiDAR mass-produced for cars spills over into robots: the Mid-360 ($749) and Hesai JT16 (€599) are products of the automotive supply chain, and once the $200-class ATX generation spills over, all-around LiDAR for humanoids reaches "depth-camera prices."

#### 3.3 Commercializing the Event Camera (Sony × Prophesee)

Timeline (all with sources):

- **2020-02**: Sony × Prophesee jointly announced a stacked event sensor at ISSCC 2020. The co-developed IMX636 (1280×720, 4.86 μm, up to 1.06 Geps) is Sony manufacturing × Prophesee Metavision technology. Sources: https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/ / https://www.sony-semicon.com/en/products/is/industry/evs.html
- **2024-10**: Prophesee (cumulative funding €126M) entered judicial reorganization proceedings under French law (redressement judiciaire) after a funding delay. Sources: https://sifted.eu/articles/startups-went-bust-2024 / http://image-sensors-world.blogspot.com/2025/01/prophesee-files-for-insolvency.html
- **2025-12-23**: Co-founder CEO Luca Verre stepped down; Jean Ferré appointed as the new CEO. Recommitment by existing investors (iBionext, 360 Capital, Aramco, Bosch Ventures, et al.) plus new participation by Critical Path Ventures. Source: https://www.prophesee.ai/2025/12/23/prophesee-appoints-jean-ferre-as-chief-executive-officer-to-lead-event-based-vision-sensing-pioneer-in-next-stage-of-growth/
- **2026-06-15**: Announced a **€20M raise (lead: Critical Path Ventures)** plus **Mantara**, an event-based-vision AI drone detection system, and the new SW platform Hearth. Pivoting to civilian + defense dual use. Sources: https://www.prophesee.ai/2026/06/15/prophesee-launches-mantara-event-based-drone-detection/ / https://www.yolegroup.com/industry-news/prophesee-raises-e20-million-and-launches-mantara-the-first-fully-integrated-drone-detection-system-built-onevent-based-vision-and-ai/
- No rescue by acquisition has been confirmed (as of 2026-08). The accurate description is "management crisis → judicial reorganization → CEO change + raise, rebuilding under its own power."

#### 3.4 Fact-Checking China's Humanoid Events (for the article's opening)

##### 2025-04-19 Beijing Yizhuang (E-Town) Half Marathon — confirmed

| Item | Finding | Reference |
|---|---|---|
| Positioning | **The world's first humanoid-robot half marathon** (running alongside ~12,000 humans, in a dedicated lane) | https://english.beijing.gov.cn/latest/news/202504/t20250421_4070140.html / https://www.aljazeera.com/features/2025/4/19/humans-outrun-robots-at-beijing-half-marathon |
| Entrants | **21 robots** (20 teams) | Same as above |
| Finishers | **6 robots** (NPR). However, some outlets report "4 within the 4-hour time limit" (**inconsistency across reports** — the safe wording for the article is "6 finished (4 within the time limit, per some reports)") | https://www.npr.org/2026/04/20/g-s1-118086/humanoid-robot-half-marathon |
| Winner | **Tiangong Ultra**, Beijing Humanoid Robot Innovation Center (X-Humanoid). Time: **2:40:42** | https://english.beijing.gov.cn/latest/news/202504/t20250421_4070140.html |

##### 2025-08-14 to 17: The 1st World Humanoid Robot Games — confirmed

| Item | Finding | Reference |
|---|---|---|
| Dates and venues | Opened 2025-08-14 (opening ceremony = National Stadium, the "Bird's Nest"), competition 8/15-17, closing ceremony = **National Speed Skating Oval (Ice Ribbon)** | https://english.beijing.gov.cn/latest/news/202508/t20250811_4170955.html |
| Scale | **16 countries, 280 teams, 500+ robots, 26 events** | https://www.newsonair.gov.in/500-humanoid-robots-compete-at-world-robot-games-in-beijing |
| Medal leaders | **Unitree topped the table with 11 medals including 4 golds (400m, 1500m, 100m hurdles, 4×100m relay)**; X-Humanoid (Tiangong) took 10 medals including 2 golds. Tiangong won the first-ever robot 100m dash in 21.50 seconds | https://www.scmp.com/tech/tech-trends/article/3322251/chinas-unitree-x-humanoid-top-medal-total-worlds-first-humanoid-robot-games |

##### 2026 follow-ups

- **2nd Yizhuang half marathon (2026-04-19)**: "Lightning" from the Honor team won in **50 minutes 26 seconds**, beating the human half-marathon world record (Jacob Kiplimo, 56:42 — some reports write 57:20; the notation wobbles). **Over 100 robots / 105 teams** entered (11 Chinese provinces plus Germany, Brazil, Portugal). That said, every outlet treats the course conditions and timing as "reference records" without official certification. Sources: https://hongkongfp.com/2026/04/19/humans-far-behind-as-robot-breaks-record-at-beijing-half-marathon/ / https://www.npr.org/2026/04/20/g-s1-118086/humanoid-robot-half-marathon / https://www.aljazeera.com/sports/2026/4/19/humanoid-robot-breaks-half-marathon-world-record-in-beijing / verification article: https://www.scientificamerican.com/article/a-humanoid-robot-beat-the-human-half-marathon-record-at-a-beijing-race-but-what-did-it-actually-prove/
- **2nd World Humanoid Robot Games: opened 2026-08-22 (through 08-26, National Speed Skating Oval)** — opening on the very day of this research. **16 countries/regions, 666 teams, 2,056 robots** (of which China: 641 teams / 1,975 robots). The event count is **inconsistent across reports**: "32 events" (CGTN, April announcement) vs. "51 events (30 competitive + 21 scenario)" (Wikipedia) (possibly expanded between the April announcement and just before August). This edition's headliners are a **fully autonomous category** that bans remote controllers (400m/1500m/4×100m, etc.) and **long-duration autonomous tasks in real environments** such as factories and hotels. Medal results are undecided since the games opened the same day. Sources: https://news.cgtn.com/news/2026-04-22/Beijing-to-host-2nd-World-Humanoid-Robot-Games-in-August-1MxQtTFEhBm/p.html / https://www.globaltimes.cn/page/202608/1368139.shtml / https://english.beijing.gov.cn/latest/news/202608/t20260815_4824032.html

---

### List of Unverified Items (honest disclosure)

Do not state these as established fact when writing.

**Sensor specs**
- The Mid-360's $749 on the DJI official store came via search results (the price page is region-blocked and could not be viewed directly). The AliExpress street price of $480-550 is unofficial.
- The accuracy, mass, power consumption, and street price of Ouster's current Rev7/8 (not listed on the official page; datasheet PDF not consulted).
- Unitree L2's points/sec: the official 64k and a reseller's 128k disagree (the official value was adopted). The L2's mass, accuracy, and whether an IMU is built in.
- Hesai XT16's range @10% reflectivity (only the sibling XT32M's 80 m confirmed).
- Official store prices of the ZED 2i / ZED X (search-result values only; store pages blocked).
- Standalone prices of the Orbbec Gemini 336/336L.
- The D435i's 72 g mass is a distributor value (not on the current official page).
- Prophesee EVK4's official direct price (quote-based; only the Taiwanese distributor's NT$175,000).
- The BMI088's bias instability "<2 °/h" is a flyer value obtained via a forum (not in the formal datasheet). Exact unit prices of the BMI088 / ICM-42688-P.
- Unit prices of the ADIS16490 / Meta Digit 360 / uSkin / ATI Axia80 (unpublished, quote-based).
- Whether the Robotiq FT 300-S actually qualifies as "capacitive" (officially described only as "wear-free sensing technology").
- The general price band of ToF cameras (going rates other than the Femto Bolt's $418).

**Real-robot configurations**
- The Unitree G1/H1 official spec pages say only "3D LiDAR + Depth Camera"; the Mid-360 / D435i **model numbers do not appear on the official pages** (confirmed in distributor documents).
- The Unitree G1's IMU model number and grade, and whether it has sole force sensors (only the negative confirmation that the published specs do not mention them).
- Tesla Optimus's camera count (8 comes from third-party reviews; no official primary source confirmed).
- Whether Figure 02's "6 RGB cameras" is stated on a Figure official primary page (the 03's palm camera is confirmed by official announcement).
- Sensor details of Boston Dynamics' new Atlas (no official primary spec sheet exists; relies on third-party summaries).
- The ASIMO/Atlas ankle 6-axis F/T sensors are mentioned in research literature (not in manufacturer primary specs).

**Bibliographic / market**
- The primary URL of Julier & Uhlmann 1997 (UKF), the arXiv number of ExBody2 (said to be 2412.13196), and the details of Sensor Dropout (CoRL 2017).
- The original report date of Goldman Sachs' pre-revision forecast ($6B) (said to be November 2022, but no primary confirmation) — the safe wording is only "revised upward from the previous $6B forecast to $38B in 2024-02."
- The body of AskCI's "industry scale 5.3 billion yuan" report (503 error; could not be checked directly).
- The year-by-year ASP table for automotive LiDAR (inside Yole's paid report).
- The 2025 marathon finisher count (6 vs. 4 within the time limit), the 2026 games' event count (32 vs. 51), and the notation of the human half-marathon world record (56:42 vs. 57:20) — all inconsistent across reports.


## Appendix D: Collected Lessons — the 11 Rules of Reward Design, and Their Companions

### D.1 The 11 Rules of Reward Design (distilled from 13 generations of G1 walking)

1. **Style does not emerge automatically from task success.** Reward only forward progress and survival, and you get the most energy-efficient oddity (shuffling feet, straight legs, stick arms). If appearance carries meaning, reward it explicitly.
2. **A reward is meaningless if the action space cannot reach it.** For each joint, first measure whether the motion that satisfies the reward can actually be commanded physically (the knee-0.5rad incident).
3. **Geometric targets can be satisfied by substitute motions.** "Lift the foot 10cm" can be achieved by swinging the hip around without bending the knee. Specifying the joint angle itself is more reliable.
4. **A position anchor cannot be replaced by a velocity penalty.** Drifting slowly costs almost nothing.
5. **Evaluate in world coordinates too.** Neither turning nor drift is visible in a body-fixed frame (the four-way dx/dy check works well).
6. **Apply style reward weights before the local optimum forms.** Once straight knees have set in, adding a knee reward will not break them out. 3x from the very start.
7. **One mocap teacher beats a pile of handcrafted style rewards.** Knees, arms, and naturalness all transfer at once. But idealize the teacher first — period extraction, straightening, loop closure.
8. **Residual control = feed the teacher forward; the policy learns only corrections.** Reachability is guaranteed structurally, and training starts out with a high imitation score.
9. **The soft position reward exp(−k·d²) saturates at deviations around 1m and the gradient dies** (measured three times in a row). Constrain the course fail-closed with termination, not with a reward.
10. **Do not give one reward multiple responsibilities.** Decompose: gait = mocap tracking, course = corridor, speed = reference-speed tracking, forcing forward progress = stall termination.
11. **The anti-rewind kit for a looping teacher has three pieces.** Joints: crossfade closure; reference velocity: remove difference spikes; position: wrapped accumulation (or do not track it).

![Lessons map](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_reward_lessons_map.png)
*Figure: The 11 reward-design rules laid out across the four quadrants of observation, action, reward, and termination*

### D.2 The Musculoskeletal (evis) Five

1. **Muscles pull. They cannot push.** Crush one sign and the antagonists become comrades, dragging the joint into the end of its range.
2. **In a muscle-driven body there is no such thing as an "unrelated joint."** Command only part of it and the rest goes limp and everything collapses. Always command the whole body.
3. **Anatomical couplings (equality constraints) belong outside the allocator's jurisdiction — handle them mechanically.** Hand-maintained exclusion lists always leak. Auto-generate them from the model's constraint definitions.
4. **Test weighting functions at extreme values.** 1/max(|τ|, 2) was causing a 40x inversion that deprioritized exactly the joints with the largest demands. Lay a floor (12Nm in this case).
5. **Angle error at a joint in contact cannot be erased with torque.** Feeding extra torque to a toe pressing the floor only presses the floor harder. First find which joint the error "lives" in.

### D.3 The Referee (honest measurement) Five

1. **Measure forward progress at the feet.** Measure at the torso or head, and a forward dive gets counted as "progress."
2. **Always watch the video (or the trajectory numbers).** A high-scoring run that was in fact doing nothing — that has happened more than once.
3. **Beat the null before making claims.** Always measure the "no control" record first.
4. **Freeze the pass/fail criteria before measuring.** As long as criteria can be moved after the fact, humans will move them.
5. **When a result is unusually good, suspect the breakdown before celebrating.** The bigger the win, the sooner you should look for changed environment parameters, loosened termination conditions, and mixed-up coordinate frames.

### D.4 The Operations Three (the practicalities of hosting solo)

1. **Build tools during training wait time.** The cycle of building referee instruments and broadcast rigs while a multi-hour training run goes on determines the throughput of a one-person event.
2. **Declare the judgment criteria before starting a long unattended run.** A run for which you have not decided "what output stops it" cannot be stopped by any output.
3. **Record failed experiments instead of deleting them.** walk7 (retired without ever running) and the two consecutive saturation deaths became the design grounds for the next generation. The chronicle is an asset.

## Appendix E: Extended Glossary

A dictionary that goes one level deeper than the main text's glossary (Chapter 2), so you can look up the concepts that appeared in this article.

- **RSI (Reference State Initialization)** — Initialization that starts each episode from a random phase of the reference motion. Prevents the policy from getting good only at the opening because every run starts from the same pose. A staple of imitation learning.
- **XLA (Accelerated Linear Algebra)** — The compiler working behind JAX. Strong at fixed-shape dense matrix computation, weak at variable-length, sparse computation (such as the 700-muscle tension paths). This profile of strengths and weaknesses decides the hardware plan (the GPU/CPU division of labor).
- **Early fusion / mid fusion / late fusion** — The three stages of combining multi-sensor information: mixing at raw data / at features / at decisions. Concatenating observation vectors is the simplest form of early fusion.
- **Episode** — One trial of training. It ends by falling, disqualification, or running out of time. How episodes are ended (termination) is a design variable as important as the reward.
- **Observation normalization** — Preprocessing that scales each observation dimension to mean 0, variance 1. The statistics accumulate during training. Checkpoints contain these statistics, and inference needs them too (the first thing ported in the numpy bridge).
- **Co-contraction** — Stiffening a joint by tensing antagonist muscles simultaneously. Humans do it unconsciously during unfamiliar work. In evis's measurements, the stiffness benefit under the current configuration was neutral (an honest null result, separate from Appendix D.2).
- **Quaternion** — A way to represent 3D rotation with four numbers. **There are two schools, wxyz order and xyzw order**, and when the dataset and the engine follow different schools, every frame quietly twists.
- **Corridor termination** — A rule that ends the episode the instant the robot strays a set distance off course. A punishment that does not saturate.
- **Residual** — The difference from a reference value. Residual control and residual RL turn "learn from scratch" into "learn only the correction from the reference," making training easier by orders of magnitude.
- **Posture-indexed capacity map** — A component of evis's muscle allocator. Because the joint torque a muscle can produce changes with posture (moment arms), this mechanism re-derives the "muscle→torque conversion capacity" at the current posture on the fly.
- **Termination** — The condition that cuts an episode short. A kind of punishment, but unlike a reward it never saturates, and it changes the distribution of experience itself. Strong medicine (see also walk12's atrophy).
- **Gradient vanishing (of the learning curve)** — When the cues for improvement run out and learning flatlines. It appears three times in this article: the reward saturation zone, the freeze local optimum, and standing RL's 1.7-second oscillation.
- **Contact-consistent equilibrium** — A state where whole-body gravity, inertia, joint torques, and contact forces all balance without contradiction. The final wall of musculoskeletal standing. Matching positions and posture alone is not enough — if the forces do not balance, it collapses the next instant.
- **Soft reward / hard constraint** — Gentle exp-shaped rewards versus absolute rules like termination. "Wide reach but thin" vs. "narrow reach but absolute." Their division of labor is one of the main themes of this whole article.
- **Distillation / teacher-student learning** — Transferring the behavior of a teacher policy raised on privileged information (exact ray distances, etc.) into a student policy that has only the sensors a real robot could carry. The main battlefield of sensor-comparison research.
- **Stall termination** — Disqualification for failing to move forward within a set time. Introduced in this article as the counter-rule to the freeze local optimum (stand still and you are invincible).
- **Privileged information** — Ground truth you can peek at only because it is simulation (exact positions, contact forces, and so on). Fine as scaffolding for training, but leave it in the final policy's observations and you cannot take it to a real robot.
- **Moment arm** — The lever-arm length by which muscle tension converts into joint torque. It changes with posture. Alongside the scapulohumeral-rhythm equality constraints, the prime culprit that makes musculoskeletal control interesting (and hard).
- **Rollout** — Stopping training and running the policy deterministically to take a record. The referee trusts only rollouts (evaluation values during training differ in both distribution and conditions).

## Appendix F: The Fullseye Op Catalog (full index of the measured registry)

An index of every op registered in Studio for Fullseye, the vision toolkit introduced in Chapter 11 of the main text. The fact that industrial image processing (2D/3D) lives in a single registry alongside robot pseudo-sensors and trained-policy execution is itself the current state of the "Physical AI IDE" idea, so I am posting the whole thing without embarrassment. Note that this index is the measured full count of the unified registry (1,606), of which 791 are exposed in Studio's interactive UI (the rest are API-only, experimental, or internal ops). Individual ops are a mixed bag, and many are far from the polish of commercial libraries — I would be grateful if you read the index not as "what exists" but as a map of "what we are trying to build."

### F.0 The Toolbox by Use — the ops that actually worked in this article

Before entering the index, the important part first. A tool's worth is not the row count of its catalog but "what work it actually did." Here are the jobs the ops in this toolbox actually carried in the main text of this article, presented as working examples.

| Use (real work in this article) | Ops that did the work | Where in the article |
|---|---|---|
| The walking policy's "eyes" (the training observation itself) | Pseudo-LiDAR, ray time-difference (specops) | Event 2 (Chapter 6) — called at every one of 152M training steps |
| Referee rollout measurement (all the measured 20.46m, 10.21m, etc.) | g1_walk_policy (policy-execution op) | Every scoreboard in Chapters 5-6 |
| Real-sensor verification (Mid-360/D435i reproduction) | perceive_g1_real (BEV point cloud, depth) | The video in Section 6.4 |
| Handing perception to every athlete | Reuse of the above (rays, depth, POV) | The five-robot scouting in Section 6.7 + the Go2 main event |
| Sourcing material for the 3D broadcast | depth_to_points and the mesh ops | The browser viewer in Chapter 10 |
| Generating the article's figures | Calibration, transform, and visualization ops | Figures throughout |

And the sample-code collection is also shown through "working examples." Everything below is genuine output from running Studio's samples.

![Point tracking on G1 walking](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_g1_tracks.png)
*Example: feature-point tracking applied to this article's G1 walking video. A setup usable as-is for robot video analysis (automatic measurement from motion logs) (sample run output; the input is the G1 walking rollout video generated for this article)*

![Policy frame analysis](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_g1_policy_frames.png)
*Example: a sample that frame-analyzes a rollout of the trained walking policy. "Inspect the products of training with vision ops" — this article's refereeing philosophy in a nutshell (sample run output; the input is the same self-generated rollout video)*

![Counting inspection](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_count_blobs.png)
*Example: counting inspection. Binarize → connected components → count — the first street corner of inspection machinery (sample run output; the input is the coins sample bundled with skimage)*

![Edges + automatic threshold](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_edge_sobel_otsu.png)
*Example: Sobel + Otsu automatic threshold. The classic setup that extracts edges with no manual tuning even when the lighting changes (sample run output; the input is the coins sample bundled with skimage)*

![Distance transform](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_distance_transform.png)
*Example: distance transform. Measuring the "clearance margin" between parts — the foundation of interference checking (sample run output; the input is the coins sample bundled with skimage)*

![Event camera](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_event_camera.png)
*Example: event camera simulation. Synthesizing the "eye that sees only change" — outputting nothing but luminance changes — from an ordinary video (sample run output; the input is a video clip synthesized from scratch in numpy)*

![Grasp pose estimation](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_grasp_pose.png)
*Example: grasp pose estimation. Deriving "where to grip" from an object's shape — the backstage crew for the chopstick and hand events (sample run output; the input is a self-synthesized point cloud — no file input)*

![Bilateral smoothing](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_denoise_bilateral.png)
*Example: edge-preserving noise removal (bilateral). A staple of pre-measurement conditioning (sample run output; the input is a self-synthesized checker + noise image)*

![Gabor texture](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/sample_out_texture_gabor.png)
*Example: texture analysis with Gabor filters. A tool for surface inspection (scratches, unevenness) (sample run output; the input is a procedurally generated brick texture of my own)*

Explaining each op with its applications would never fit in this article, so **a dedicated article is planned separately**. Please use the index below as a floor map of what is inside.

### F.1 How to Read the Catalog

An index of op names with one-line descriptions (chapters = processing domains). Major chapters open with an explanation of "what this domain's tools do" plus an actual processing-example image — it should convey the feel of "actually running" better than tables alone. Auto-generated from the measured registry, totaling **1606 ops / 94 chapters**. Rows whose description reads only "... op (HALCON: xxx)" show just the name correspondence — which operator of the HALCON-compatible API the op maps to — with individual functional descriptions omitted.

#### Tools (82 ops)

The proverbial "toolbox of the toolbox": coordinate-transform utilities, type conversions, visualization helpers — chore ops that underpin every other category. As the glue of pipelines, they are also among the most frequently called.


![fops_tools](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_tools.png)
*Figure: A real Tools example — filling missing pixels (satellite scanline dropouts, scratches) with a constant leaves visible seams, but interpolate_scattered_data_image fills them smoothly by scattered-data interpolation of the surviving pixels (actual Fullseye output). Inputs are a Martian dune field by NASA/JPL-Caltech/Univ. of Arizona (HiRISE, PIA18244, public domain), skimage camera, and an AI-generated image (Gemini). The missing pixels were artificially added in all three.*

| op | Description |
|---|---|
| `abs_funct_1d` | Absolute value of the y values (abs_funct_1d). |
| `adjust_mosaic_images` | Adjust brightness differences between mosaic images toward the mean (adjust_mosaic_images). |
| `angle_ll` | Angle between two lines [rad] (angle_ll). |
| `angle_lx` | Angle between a line and the x (column) axis [rad] (angle_lx). |
| `apply_distance_transform_xld` | Evaluate correspondences/distances of points along an XLD contour using a distance field (apply_distance_transform_xld). |
| `area_intersection_rectangle2` | Intersection area of two oriented rectangles (Monte Carlo approximation, area_intersection_rectangle2). |
| `bundle_adjust_mosaic` | Least-squares adjustment of a set of homographies from correspondences across all image pairs (bundle_adjust_mosaic). |
| `compose_funct_1d` | Composition of two functions y1(y2) (range values looked up as indices, compose_funct_1d). |
| `connect_grid_points` | Connect grid points into rows/columns by nearest neighbor and return the adjacency (connect_grid_points). |
| `create_distance_transform_xld` | Generate a per-pixel shortest-distance field from an XLD contour (dict {cs:[Nx2]}) (create_distance_transform_xld). |
| `create_funct_1d_array` | Create a 1D function from an array of equally spaced samples (create_funct_1d_array). |
| `create_rectification_grid` | Generate the ideal grid points (world) for rectification (create_rectification_grid). |
| `create_scattered_data_interpolator` | Build an interpolator from irregular points (N,2) and values (N,) (create_scattered_data_interpolator). |
| `derivate_funct_1d` | 1D derivative (central differences, derivate_funct_1d). |
| `distance_cc` | Mean point-to-point distance between two contours (distance_cc). |
| `distance_cc_min` | Minimum point-to-point distance between two contours (distance_cc_min). |
| `distance_cc_min_points` | Return the minimum distance between two contours together with the closest point pair (distance_cc_min_points). |
| `distance_contours_xld` | Maximum distance from each point of contour_from to contour_to (distance_contours_xld). |
| `distance_lc` | Minimum distance from a line to a contour (distance_lc). |
| `distance_lr` | Minimum distance from a line to a region (binary) (distance_lr). |
| `distance_pl` | Perpendicular distance from a point to an (infinite) line (distance_pl). |
| `distance_point_line` | Distance from a 3D point to a line (point l + direction d) (distance_point_line). |
| `distance_point_pluecker_line` | Distance between a 3D point and a Plücker line (distance_point_pluecker_line). |
| `distance_pp` | Distance between two points (distance_pp). |
| `distance_ps` | Distance from a point to a line segment (distance_ps). |
| `distance_rr_min` | Minimum pixel distance between two regions (binary masks) (distance_rr_min). |
| `distance_rr_min_dil` | Minimum distance between two regions computed via distance transform (distance_rr_min_dil). |
| `distance_sl` | Minimum distance from a segment to a line (the smaller of the endpoints' perpendicular distances, distance_sl). |
| `distance_sr` | Minimum distance from a segment to a region (distance_sr). |
| `distance_ss` | Minimum distance between two segments (distance_ss). |
| `find_rectification_grid` | Detect a rectification grid (intersections/dots) in an image (find_rectification_grid). |
| `funct_1d_to_pairs` | Convert a 1D function into (x, y) pairs (funct_1d_to_pairs). |
| `gen_arbitrary_distortion_map` | Build a distortion map from an arbitrary displacement field (gen_arbitrary_distortion_map). |
| `gen_bundle_adjusted_mosaic` | Generate a mosaic using bundle-adjusted homographies (gen_bundle_adjusted_mosaic). |
| `gen_cube_map_mosaic` | Tile six faces in a cube-map layout (gen_cube_map_mosaic). |
| `gen_grid_rectification_map` | Interpolate a rectification (inverse-distortion) map from observed (distorted) grid points (gen_grid_rectification_map). |
| `gen_projective_mosaic` | Composite multiple images into a single mosaic via homographies (gen_projective_mosaic). |
| `gen_spherical_mosaic` | Mosaic composition in spherical panorama coordinates (simplified: cylindrical-projection approximation) (gen_spherical_mosaic). |
| `get_pair_funct_1d` | Return the (x, y) pair at an index (get_pair_funct_1d). |
| `get_points_ellipse` | Return n points on an ellipse boundary (get_points_ellipse). |
| `get_y_value_funct_1d` | The y value at a given x (linear interpolation available) (get_y_value_funct_1d). |
| `hough_line_trans_dir` | Directed Hough line transform using the gradient direction (hough_line_trans_dir). |
| `hough_lines_dir` | Detect lines (rho, angle) from the peaks of the directed Hough transform (hough_lines_dir). |
| `integrate_funct_1d` | Cumulative 1D integral (trapezoidal rule, integrate_funct_1d). |
| `interpolate_scattered_data` | Evaluate an interpolator at arbitrary query points (interpolate_scattered_data). |
| `interpolate_scattered_data_image` | Fill a missing region in an image by scattered interpolation of the remaining pixels (interpolate_scattered_data_image). |
| `interpolate_scattered_data_points_to_image` | Interpolate values at irregular points onto a dense grid image (interpolate_scattered_data_points_to_image). |
| `intersection_circle_contour_xld` | Intersection points of a circle and a contour (intersection_circle_contour_xld). |
| `intersection_circles` | Return the intersection points (0/1/2) of two circles (intersection_circles). |
| `intersection_contours_xld` | Return the intersection points of two contours (intersection_contours_xld). |
| `intersection_line_circle` | Return the intersection points of a line and a circle (0/1/2 points) (intersection_line_circle). |
| `intersection_line_contour_xld` | Intersection points of a line (2 endpoints) and a contour (intersection_line_contour_xld). |
| `intersection_lines` | Return the intersection (row, col) of two lines (2 points each) (intersection_lines). None if parallel. |
| `intersection_segment_circle` | Intersections of a segment and a circle (within the segment only) (intersection_segment_circle). |
| `intersection_segment_contour_xld` | Intersection points of a segment and a contour (intersection_segment_contour_xld). |
| `intersection_segment_line` | Intersection of a segment and a line (within the segment only) (intersection_segment_line). |
| `intersection_segments` | Intersection of two segments (within both segments only) (intersection_segments). |
| `invert_funct_1d` | Invert a function y=f(x) into x=f^-1(y) (linear interpolation on monotonic intervals) (invert_funct_1d). |
| `line_orientation` | Orientation of a segment (radians, -pi/2..pi/2, line_orientation). |
| `line_position` | Midpoint, length, and orientation of a segment (line_position). |
| `local_min_max_funct_1d` | Return the indices of local maxima/minima (local_min_max_funct_1d). |
| `match_funct_1d_trans` | Estimate the best shift between two 1D functions (cross-correlation peak) (match_funct_1d_trans). |
| `negate_funct_1d` | Negate the y values (negate_funct_1d). |
| `num_points_funct_1d` | Number of points of a function (num_points_funct_1d). |
| `pluecker_line_to_point_direction` | Recover a point on the line and its direction from Plücker coordinates (pluecker_line_to_point_direction). |
| `pluecker_line_to_points` | Return two points on a Plücker line (pluecker_line_to_points). |
| `point_direction_to_pluecker_line` | Return Plücker coordinates from a 3D point and a direction (point_direction_to_pluecker_line). |
| `points_to_pluecker_line` | Return the Plücker coordinates (direction d, moment m) of the line through two 3D points (points_to_pluecker_line). |
| `proj_match_points_distortion_ransac` | RANSAC homography from point correspondences with distortion (distortion assumed small) |
| `proj_match_points_distortion_ransac_guided` | Guided RANSAC with distortion (proj_match_points_distortion_ransac_guided). |
| `proj_match_points_ransac` | Estimate a projective transform (homography) from point correspondences with RANSAC (proj_match_points_ransac). |
| `proj_match_points_ransac_guided` | RANSAC guided by an initial homography (uses nearby correspondences only) (proj_match_points_ransac_guided). |
| `projection_pl` | Return the foot of the orthogonal projection of a point onto a line (projection_pl). |
| `sample_funct_1d` | Resample a function at step intervals (sample_funct_1d). |
| `scale_y_funct_1d` | Linear transform of the y values mult*y+add (scale_y_funct_1d). |
| `select_matching_lines` | Pair up lines that are close in orientation and position (select_matching_lines). |
| `smooth_funct_1d_gauss` | 1D Gaussian smoothing (smooth_funct_1d_gauss). |
| `smooth_funct_1d_mean` | 1D moving-average smoothing (smooth_funct_1d_mean). |
| `transform_funct_1d` | Affine transform of a 1D function (x and y independently, transform_funct_1d). Returns (x,y) pairs. |
| `x_range_funct_1d` | The x range (min,max) of a function (x_range_funct_1d). |
| `y_range_funct_1d` | The y range (min,max) of a function (y_range_funct_1d). |
| `zero_crossings_funct_1d` | Return the indices where the sign changes (zero crossings) (zero_crossings_funct_1d). |

#### halcon_ext (81 ops)

A group of ops extended with the operator system of the commercial HALCON library as reference, aiming for compatible ergonomics. The naming also follows HALCON style (verb_object), with an eye toward a vocabulary that HDevelop veterans can read as-is. The table in this chapter lists only the HALCON-compatible name correspondence (which operator each op maps to) and omits individual functional descriptions.

| op | Description |
|---|---|
| `hx_add_noise_contour` | Add white Gaussian noise to contour points (std is a; deterministic with a fixed seed). |
| `hx_char_threshold` | Extract dark characters from a bright background (region): select below thresh = mean - k*std (k is a). |
| `hx_clip_contours` | Clip contours to the image domain (a rectangle keeping the central margin a/b) (removes out-of-range points). |
| `hx_clip_end_points` | Cut k points off each end of every contour (k is a). |
| `hx_clip_region_rel` | Clip a region relative to its bounding rectangle (trim a fraction a from each side). |
| `hx_close_edges` | Close gaps in an edge-amplitude image: binarize at threshold a → morphological closing (radius b). |
| `hx_close_edges_length` | On top of close_edges, remove short edge fragments whose length (pixel count) falls below a threshold. |
| `hx_closing` | halcon_ext op (HALCON: closing) |
| `hx_cooc_feature` | Quantize, build a horizontal co-occurrence matrix at distance d, and return the Haralick contrast (a=distance, b selects the angle). |
| `hx_crop_contours` | Crop contours to a central a×b-fraction rectangle (keeps only the points inside). |
| `hx_detect_edge_segments` | Detect straight edge fragments: thin with NMS → keep connected components that are elongated (line-like) by PCA. |
| `hx_dilation1` | halcon_ext op (HALCON: dilation1) |
| `hx_dilation2` | Dilation with a reference point: apply the reference-point offset after dilation (translate by b). |
| `hx_disparity_to_xyz` | Compute depth Z = f*baseline/disparity from a disparity image (focal length/baseline adjustable via a,b). Normalized Z. |
| `hx_dist_ellipse_contour` | Return the mean distance of contour points from the fitted ellipse boundary (small = close to an ellipse, feature). |
| `hx_dist_ellipse_points` | Return the maximum distance of each contour point from the fitted ellipse boundary (per-point distances aggregated by max, feature). |
| `hx_dist_rect2_points` | Mean normalized distance of contour points from the center of the minimum-area bounding rectangle (feature). |
| `hx_distance_pc` | Minimum distance from a query point (normalized a,b) to a contour (feature). |
| `hx_distance_pr` | Minimum distance from a query point (normalized a,b) to a region (feature). Via distance transform. |
| `hx_distance_sc` | Minimum distance from a horizontal segment (row a*H) to a contour (feature). |
| `hx_erosion1` | halcon_ext op (HALCON: erosion1) |
| `hx_estimate_al_am` | Estimate albedo (reflectance) and ambient light: albedo ~ luminance range; returns the albedo here. |
| `hx_estimate_sl_al_lr` | Lee-Rosenfeld: estimate the light source slant (zenith angle, 0=frontal to pi/2=sideways). Normalized to [0,1]. |
| `hx_estimate_sl_al_zc` | Zheng-Chellappa: estimate the slant corrected by gradient energy. |
| `hx_estimate_tilt_lr` | Lee-Rosenfeld: light source azimuth tilt = atan2(<Ey>, <Ex>) (mean gradient direction). Normalized to [0,1]. |
| `hx_estimate_tilt_zc` | Zheng-Chellappa: estimate the tilt from the mean direction of normalized gradients (independent of local contrast). |
| `hx_expand_region` | Fill gaps between regions (region -> region): dilate the binary regions to encourage connection. |
| `hx_fill_interlace` | Interpolate two video half-images (replace odd rows with the average of adjacent even rows = deinterlacing). |
| `hx_fit_circle_contour` | Fit a circle to contour points with the Kåsa algebraic method and return the fit residual (RMS) (small = close to a circle). |
| `hx_fit_ellipse_contour` | Fit an ellipse from second moments and return the axis ratio (minor/major = 1 for a perfect circle, toward 0 as it elongates). |
| `hx_fit_rectangle2_contour` | Fit the minimum-area bounding rectangle and return its aspect ratio (short/long side) (feature). |
| `hx_fit_surface1` | halcon_ext op (HALCON: fit_surface_first_order) |
| `hx_fit_surface2` | halcon_ext op (HALCON: fit_surface_second_order) |
| `hx_full_domain` | halcon_ext op (HALCON: full_domain) |
| `hx_fuzzy_measure_pairs` | Count edge pairs (rising boundary → falling boundary of bright bars) on the central horizontal profile (1D measurement). |
| `hx_gabor` | Gabor filter (orientation theta=a*pi, frequency freq=b). Returns the response magnitude. |
| `hx_gen_bandfilter` | Ideal band-filter image (frequency annulus, center radius a, width b). A separate operator from gen_bandpass. |
| `hx_gen_bandpass` | Ideal bandpass (annulus mask in the frequency domain, inner radius a, bandwidth b). |
| `hx_gen_checker_region` | halcon_ext op (HALCON: gen_checker_region) |
| `hx_gen_circle` | halcon_ext op (HALCON: gen_circle) |
| `hx_gen_circle_sector` | Circle sector region (start angle b*2pi, sweep a*2pi). |
| `hx_gen_derivative_filter` | Derivative filter in the frequency domain (stronger at higher frequencies = proportional to the frequency radius). |
| `hx_gen_disc_se` | Generate a disc structuring element as a region (radius a). |
| `hx_gen_ellipse` | halcon_ext op (HALCON: gen_ellipse) |
| `hx_gen_ellipse_sector` | halcon_ext op (HALCON: gen_ellipse_sector) |
| `hx_gen_empty_region` | halcon_ext op (HALCON: gen_empty_region) |
| `hx_gen_grid_region` | halcon_ext op (HALCON: gen_grid_region) |
| `hx_gen_highpass` | halcon_ext op (HALCON: gen_highpass) |
| `hx_gen_image_proto` | Generate a constant gray image (value a) the same size as the input. |
| `hx_gen_lowpass` | Ideal lowpass filter image (central disc mask in the frequency domain, cutoff radius a). |
| `hx_gen_parallel_contour` | Generate a parallel (normal-offset) contour for each contour (signed distance via (a-0.5)). |
| `hx_gen_rectangle2` | halcon_ext op (HALCON: gen_rectangle2) |
| `hx_get_domain` | Get the image's domain as a region (defaults to the full image). |
| `hx_histo_to_thresh` | Binarize with a threshold picked from histogram valleys (valley detection, not Otsu's variance criterion = a separate op). |
| `hx_lowlands` | Detect gray-value hollows (flat areas of local minima): the region of pixels equal to the neighborhood minimum. |
| `hx_mean_shape` | Mean smoothing with an arbitrary mask (disk). Radius r adjustable via a (a separate op from the rectangular mean). |
| `hx_moments_any_xld` | Return the second central moments (spread) of all contour points (normalized feature). |
| `hx_move_region` | Translate a region (dy=a, dx=b as offsets centered on 0). |
| `hx_nonmax_dir` | Non-maximum suppression along the gradient direction (the NMS stage of Canny). Thins edges to 1 pixel. |
| `hx_opening` | halcon_ext op (HALCON: opening) |
| `hx_plane_deviation` | Deviation from a first-order plane fit of the gray values /v - plane/ (flatness/defect inspection). |
| `hx_plateaus_center` | Detect the centers of gray-value plateaus (gradient ~0): centroid pixels of flat connected components as a marker region. |
| `hx_polar_trans_inv` | Treat contour points as (radius, angle) and invert them to Cartesian coordinates (inverse of polar_trans). |
| `hx_radial_distort_contour` | Apply radial distortion r' = r(1 + k r^2) to a contour (k via (a-0.5), barrel/pincushion). |
| `hx_rectangle1_domain` | Shrink the image domain to an axis-parallel rectangle (central a×b fraction) region. |
| `hx_region_to_label` | Convert the connected components of the region binarized at threshold a into a label image (normalized). |
| `hx_region_to_mean` | Paint each connected region with its mean gray value (image -> image). Split foreground/background at threshold a and labelize. |
| `hx_regress_contours` | Fit a regression line to each contour and return the mean residual (deviation from the line) (feature). Small = straight. |
| `hx_select_xld_point` | Select only contours whose bounding rectangle contains the query point (normalized a,b) (filter). |
| `hx_shade_height_field` | Render a height field v with Lambertian shading (normals × light source). Light at azimuth a, elevation b. |
| `hx_smallest_circle_xld` | Return the radius of the minimum enclosing circle of all contour points (approximation = centered on the centroid) (normalized feature). |
| `hx_smallest_rect1_xld` | Return the area ratio of the axis-parallel bounding rectangle of all contour points (feature). |
| `hx_smallest_rect2_xld` | Area ratio of the minimum-area bounding rectangle (rectangle area / image area) (feature). |
| `hx_sort_contours` | Sort contours by relative position (centroid row→col). |
| `hx_split_contours` | Split each contour into segments at dominant points (RDP) (tolerance eps is a). |
| `hx_split_skeleton_region` | Split a 1-pixel-wide skeleton at branch points: remove junctions with >=3 neighbors and separate into connected components. |
| `hx_test_closed_xld` | Return the fraction of contours that are closed (endpoint distance below threshold = closed, feature). |
| `hx_test_region_point` | Whether the region contains the point (normalized a=row, b=col) (1/0, test_region_point). |
| `hx_test_region_points` | The fraction of a grid of points contained in the region (test_region_points). |
| `hx_test_self_intersect` | Return the fraction of self-intersecting contours (feature). Tests non-adjacent segment pairs. |
| `hx_union_adjacent` | Greedily connect contours whose endpoints are close (threshold a). |
