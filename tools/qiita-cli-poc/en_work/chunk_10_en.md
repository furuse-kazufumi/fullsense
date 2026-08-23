#### matching (2 ops)

| op | Description |
|---|---|
| `ncc_locate` | matching op (HALCON: find_ncc_model) |
| `shape_locate` | matching op (HALCON: find_shape_model) |

#### noise (2 ops)

| op | Description |
|---|---|
| `add_noise_distribution` | noise op (HALCON: add_noise_distribution) |
| `add_noise_white` | noise op (HALCON: add_noise_white) |

#### Legacy (1 op)

| op | Description |
|---|---|
| `distance_funct_1d` | Distance between two functions (max = upper bound, mean = average; distance_funct_1d). |

#### barcode (1 op)

| op | Description |
|---|---|
| `decode_barcode` | barcode op (HALCON: find_bar_code) |

#### classification (1 op)

| op | Description |
|---|---|
| `classify_shape` | classification op (HALCON: -) |

#### filter (1 op)

| op | Description |
|---|---|
| `Bilateral` | Edge-preserving smoothing (cv2.bilateralFilter; numpy implementation when unavailable) (filter.Bilateral).  [backend=opencv] |

#### filtering (1 op)

| op | Description |
|---|---|
| `tf_gradient_domain_reintegrate` | filtering op (HALCON: -) |

#### intensity-transform (1 op)

| op | Description |
|---|---|
| `xmh_soft` | intensity-transform op (HALCON: -) |

#### misc (1 op)

| op | Description |
|---|---|
| `identity` | misc op (HALCON: copy_image) |

#### morphology/markers (1 op)

| op | Description |
|---|---|
| `xmh_regmin` | morphology/markers op (HALCON: -) |

#### region-morphology (1 op)

| op | Description |
|---|---|
| `xmh_majority` | region-morphology op (HALCON: -) |

#### region-transform (1 op)

| op | Description |
|---|---|
| `xmh_bwperim` | region-transform op (HALCON: -) |

#### self-similarity (1 op)

| op | Description |
|---|---|
| `xmh_selfmatch` | self-similarity op (HALCON: -) |

#### texture-feature (1 op)

| op | Description |
|---|---|
| `xmh_pftas` | texture-feature op (HALCON: -) |

#### texture/shape-feature (1 op)

| op | Description |
|---|---|
| `xmh_zernike` | texture/shape-feature op (HALCON: -) |

## Appendix G: A Future Reading Kit — Sensing, Space, Conferences, Competitions (all URLs verified live)

This is the resource companion to Chapter 13. Every URL here was confirmed accessible at the time of writing (anything we couldn't confirm was left out). If a link goes dead, search for the site name.

### A. The Cutting Edge of Sensing

#### A-1. Event Cameras / Neuromorphic Vision

**Why it's amazing (3 lines)**
- A camera that, like the human retina, asynchronously sends only the pixels that changed. Temporal resolution is on the order of microseconds, dynamic range is about 140 dB (a regular camera manages about 60 dB), and motion blur is essentially absent (per the [Gallego et al. survey](https://arxiv.org/abs/1904.08405)).
- The research has rippled outward into an autonomous drone that beat a world champion at drone racing (the Scaramuzza lab at UZH/ETH) and into the vision algorithms of NASA's Mars helicopter.
- Through the Sony–Prophesee collaboration, stacked event sensors with 4.86 µm pixels (IMX636/637) entered mass production — turning the event camera from "lab curiosity" into "a part you can buy."

| Item | Details | URL |
|---|---|---|
| Key paper | Gallego et al., "Event-based Vision: A Survey", IEEE TPAMI 44(1), 2022 (arXiv 2019) | https://arxiv.org/abs/1904.08405 |
| Key patent | US10498977B2 "Event-based vision sensor" (Samsung, issued 2019) | https://patents.google.com/patent/US10498977B2/en |
| Product (primary source) | Sony stacked event sensor IMX636/IMX637 press release (2021) | https://www.sony-semicon.com/en/news/2021/2021090901.html |
| Product (primary source) | Prophesee × Sony IMX636 / EVK4 evaluation kit | https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/ / https://www.prophesee.ai/event-camera-evk4/ |
| Lab | Robotics and Perception Group (UZH & ETH Zurich, Prof. Davide Scaramuzza) | https://rpg.ifi.uzh.ch/ (personal page: https://rpg.ifi.uzh.ch/people_scaramuzza.html ) |
| Lab GitHub | uzh-rpg (ESIM and many other public releases) | https://github.com/uzh-rpg |
| Public dataset | UZH-FPV drone racing dataset (events + IMU + laser ground truth) | https://fpv.ifi.uzh.ch/ |
| Simulator | ESIM: an Open Event Camera Simulator (CoRL 2018) | https://github.com/uzh-rpg/rpg_esim |
| Simulator | v2e: ordinary video → realistic DVS event conversion (CVPRW 2021 Best Paper) | https://github.com/SensorsINI/v2e (explainer: https://sites.google.com/view/video2events/home ) |
| Videos | UZH RPG official YouTube (plenty of autonomous-drone and event-camera demos) | https://www.youtube.com/user/ailabRPG |

#### A-2. Quantum Sensing (NV-Center Magnetometry, Quantum Inertial Navigation)

**Why it's amazing (3 lines)**
- A single atomic defect in diamond (an NV center) becomes a "quantum compass" that can measure magnetic fields down to the cellular scale at room temperature. The textbook-grade review of quantum sensing is [Degen–Reinhard–Cappellaro (Rev. Mod. Phys. 2017)](https://dspace.mit.edu/bitstream/handle/1721.1/124553/RevModPhys.89.035002.pdf).
- Atom interferometers, which interfere cold atoms as "waves," are the leading candidate for inertial navigation that never loses its position even where GPS is unavailable. An on-orbit test of a quantum inertial sensor was planned for the eighth flight of the US military spaceplane X-37B ([The Conversation, 2025](https://theconversation.com/quantum-alternative-to-gps-navigation-will-be-tested-on-us-military-spaceplane-262967)).
- MIT demonstrated integrating NV centers with a CMOS chip (an on-chip quantum sensor); the movement to "make quantum sensors into ordinary semiconductor components" is underway ([MIT News, 2019](https://news.mit.edu/2019/quantum-sensing-chip-0925)).

| Item | Details | URL |
|---|---|---|
| Key paper | Degen, Reinhard, Cappellaro, "Quantum sensing", Rev. Mod. Phys. 89, 035002 (2017) | https://dspace.mit.edu/bitstream/handle/1721.1/124553/RevModPhys.89.035002.pdf (DOI: 10.1103/RevModPhys.89.035002) |
| Key review | Outlook for BEC-based quantum inertial navigation (Applied Physics Reviews, 2025) | https://pubs.aip.org/aip/apr/article/12/3/031306/3351228/Developments-for-quantum-inertial-navigation |
| Key patent | US12424810B1 "Compact atom interferometry inertial navigation sensors with tailored diffractive optics" (Sandia, 2025) | https://patents.google.com/patent/US12424810B1/en |
| Key patent | US7317184B2 "Kinematic sensors employing atom interferometer phases" (2008) | https://patents.google.com/patent/US7317184B2/en |
| Research institute | Sandia National Laboratories – Atom Interferometry | https://www.sandia.gov/quantum/atom-interferometry/ |
| Research institute | QuTech (TU Delft + TNO; world-first demonstrations of quantum networking with NV centers) | https://qutech.nl/ |
| Lab (Japan) | Institute of Science Tokyo (formerly Tokyo Tech), Iwasaki Lab – solid-state quantum sensors | http://dia.pe.titech.ac.jp/en/solid-quantum-sensors/ |
| Explainer article | MIT Technology Review, "Can quantum navigation solve the GPS jamming problem?" (2025-12) | https://www.technologyreview.com/2025/12/16/1129887/quantum-navigation-militarys-gps-jamming-problem/ |
| Home entry point | QuTiP: OSS simulator for open quantum system dynamics (Python) | https://qutip.org/ |

#### A-3. Hyperspectral and Polarization Imaging

**Why it's amazing (3 lines)**
- A technique for capturing images where every pixel carries a full optical spectrum (a hypercube). Materials, moisture, freshness, and lesions that look identical to the human eye can be told apart by their "spectral fingerprints."
- Applications keep expanding: agriculture (crop stress, weed discrimination), food inspection, cancer detection and intraoperative imaging, mineral exploration, and recycling sortation ([Heliyon 2024 review](https://www.sciencedirect.com/science/article/pii/S2405844024092399)).
- In medicine, the frontier includes polarization × hyperspectral fusion (PHSI), hyperspectral endoscopy, and AR integration ([2025 medical HSI review](https://pmc.ncbi.nlm.nih.gov/articles/PMC13003176/)).

| Item | Details | URL |
|---|---|---|
| Key review | "Hyperspectral imaging and its applications: A review", Heliyon (2024) | https://www.sciencedirect.com/science/article/pii/S2405844024092399 |
| Key review | "Modern Trends and Recent Applications of Hyperspectral Imaging: A Review", Technologies (2025) | https://www.mdpi.com/2227-7080/13/5/170 |
| Medical review | Medical hyperspectral imaging: updated review (polarization HSI, endoscopy, AR integration) | https://pmc.ncbi.nlm.nih.gov/articles/PMC13003176/ |

#### A-4. Tactile Skin / Electronic Skin

**Why it's amazing (3 lines)**
- MIT's GelSight achieves tactile sensing with spatial resolution beyond a human fingertip just by "watching gel deformation with a camera." It has since been productized as GelSight, Inc. and now serves as robot fingertips ([MIT News](https://news.mit.edu/2017/gelsight-robots-sense-touch-0605)).
- Electronic skin from Stanford's Bao lab is built up from materials chemistry: it stretches, self-heals, and distinguishes pressure from shear. The goal is to give prosthetic hands their sense of touch back.
- Touch is vision's "last mile." The slip, hardness, and friction at the instant of grasping are invisible to cameras — making tactile sensing the next battleground of Physical AI.

| Item | Details | URL |
|---|---|---|
| Key paper | Yuan, Dong, Adelson, "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force", Sensors 17(12):2762 (2017) | https://www.mdpi.com/1424-8220/17/12/2762 |
| Key patent | WO2023081342A1 "Four-dimensional tactile sensing system, device, and method" (2023) | https://patents.google.com/patent/WO2023081342A1/en |
| Lab | MIT CSAIL (Adelson lineage) GelSight Wedge project | https://gelsight.csail.mit.edu/wedge/ |
| Lab | Stanford Bao Group (electronic skin, stretchable electronics) | https://baogroup.stanford.edu/ |
| Company | GelSight, Inc. (GelSight Mini and others) | https://www.gelsight.com/gelsightmini/ |
| Explainer | MIT News "Giving robots a sense of touch" (2017) | https://news.mit.edu/2017/gelsight-robots-sense-touch-0605 |

#### A-5. Neural-Interface-Style Sensing (sEMG / EIT) — Briefly

**Why it's amazing (3 lines)**
- Meta's wristband (from the former CTRL-labs) decodes fine finger movements from surface electromyography (sEMG) at the wrist alone, with no per-person calibration. It can take mid-air handwriting input at about 20.9 words per minute (published in Nature, 2025).
- Non-invasive neuromotor interfaces that "put no electrodes in the brain" have advanced to the point of contending to be the next standard input after keyboard and mouse.
- There is also research on turning electrical impedance tomography (EIT) into a wristband, with a reported 93% gesture-recognition accuracy at low cost and low power (about 50 mW) ([Biosensors 2026](https://www.mdpi.com/2079-6374/16/4/200)).

| Item | Details | URL |
|---|---|---|
| Key paper | "A generic non-invasive neuromotor interface for human-computer interaction", Nature 645 (2025) | https://www.nature.com/articles/s41586-025-09255-w |
| Primary source | Meta EMG Wristband official page | https://www.meta.com/emerging-tech/emg-wearable-technology/ |
| Related paper | Robust EIT-based gesture recognition (Biosensors, 2026) | https://www.mdpi.com/2079-6374/16/4/200 |

---

### B. Space Development

#### B-1. On-Orbit Servicing and Debris Capture

**Why it's amazing (3 lines)**
- Astroscale's ADRAS-J (JAXA CRD2 Phase I) autonomously approached to within 15 m of a roughly 3-ton rocket upper stage — one with no cooperative features whatsoever — in 2024 and successfully performed fly-around observation. A world-first-class achievement ([Astroscale official](https://www.astroscale.com/en/news/astroscales-adras-j-achieves-historic-15-meter-approach-to-space-debris)).
- The follow-on ADRAS-J2 (CRD2 Phase II) plans to actually capture that same debris with a robotic arm and deorbit it. ESA × ClearSpace's ClearSpace-1 is also preparing a capture demonstration using four arms.
- "Safely approaching and grasping a tumbling, non-cooperative object" — rendezvous and capture of free-floating objects — is a mixed martial art of GNC (guidance, navigation, and control), vision, and contact dynamics. Simulation is exactly where the main event happens.

| Item | Details | URL |
|---|---|---|
| Official mission | Astroscale ADRAS-J mission page | https://www.astroscale.com/en/missions/adras-j |
| Official program | JAXA CRD2 (Commercial Removal of Debris Demonstration) | https://www.kenkai.jaxa.jp/eng/crd2/index.html |
| Primary source | JAXA press: ADRAS-J fly-around observation images of the debris (2024-07) | https://global.jaxa.jp/press/2024/07/20240730-1_e.html |
| Patent (explainer) | Astroscale's official explainer of patent US12,479,603 B2, "method for capturing tumbling objects" | https://www.astroscale.com/en/news/astroscale-patent-advances-docking-and-servicing-of-tumbling-satellites |
| Product | Astroscale docking plate (a "tow hook for satellites" for magnetic capture) | https://www.astroscale.com/en/docking-plate |
| Explainer article | MIT Technology Review: the world's first debris removal mission begins (2024) | https://www.technologyreview.com/2024/02/27/1089065/first-mission-dead-rocket/ |
| Article with video | ADRAS-J fly-around footage (Space.com) | https://www.space.com/astroscale-debris-removal-adras-j-video |

Note: The ClearSpace corporate site is not listed because we could not verify its URL (the state of ClearSpace-1 is covered in the Space.com / MIT Tech Review articles above).

#### B-2. Lunar Robotics

**Why it's amazing (3 lines)**
- The JAXA × Toyota crewed pressurized rover "LUNAR CRUISER" is a "camper van for the Moon" running on hydrogen fuel cells. It is the size of two minibuses and can be ridden without a spacesuit ([Toyota official](https://global.toyota/en/mobility/technology/lunarcruiser/)).
- NASA JPL's CADRE is an autonomous-cooperation demonstration in which three suitcase-sized rovers elect their own "leader," divide up roles, and 3D-map the lunar surface. Earth only hands them the goal: "explore this region" ([JPL official](https://www.jpl.nasa.gov/missions/cadre/)).
- Meanwhile, NASA's water-ice prospecting rover VIPER was cancelled in 2024 (about $450 million already invested). We want to be honest that the cutting edge is not a story in which everything succeeds.

| Item | Details | URL |
|---|---|---|
| Official | Toyota LUNAR CRUISER official page | https://global.toyota/en/mobility/technology/lunarcruiser/ |
| Official | NASA JPL CADRE mission page | https://www.jpl.nasa.gov/missions/cadre/ |
| Primary source | NASA: CADRE rovers packed for their lunar journey (arriving 2026 on IM-3) | https://www.nasa.gov/missions/tech-demonstration/cadre/nasas-mini-rover-team-is-packed-for-lunar-journey/ |
| Company | ispace (HAKUTO-R program) | https://www.ispace-inc.com/aboutus |
| News | How the VIPER cancellation unfolded (Spaceflight Now, 2024) | https://spaceflightnow.com/2024/07/18/nasa-cancels-half-billion-dollar-water-ice-seeking-moon-rover/ |
| Japan | Tohoku University selected to lead a landmark lunar infrastructure project (2026) | https://www.tohoku.ac.jp/en/news/university_news/selected_to_lead_landmark_lunar_infrastructure_project.html |

#### B-3. On-Orbit Manufacturing and Space Construction

**Why it's amazing (3 lines)**
- Varda Space is chasing "more perfect crystals" that can only be made in weightlessness: it manufactured crystals of the antiviral drug Ritonavir on orbit and brought them home in a capsule (the 2024 W-1 mission). It is already on its sixth capsule flight.
- With neither convection nor sedimentation, microgravity is considered the prime manufacturing environment for protein crystals, pharmaceuticals, and specialty optical fiber; Redwire founded SpaceMD, a subsidiary dedicated to space pharma ([CNBC, 2026](https://www.cnbc.com/2026/06/09/space-race-pharma-spacex-varda-redwire-drug-development-orbit.html)).
- The industrial structure itself is novel: "launch the factory, and bring back only the product at Mach 25." The reentry capsule's aerodynamics and thermal protection are also a mountain of simulation.

| Item | Details | URL |
|---|---|---|
| Official | Varda W-Series platform (on-orbit manufacturing + reentry) | https://www.varda.com/platform |
| Official | Redwire (space infrastructure + space pharma SpaceMD) | https://rdw.com/ |
| News | Varda capsule returns carrying space-manufactured drugs (Space.com, 2024) | https://www.space.com/varda-in-space-manufacturing-capsule-landing-success |
| News | Why pharma is heading for LEO (CNBC, 2026-06) | https://www.cnbc.com/2026/06/09/space-race-pharma-spacex-varda-redwire-drug-development-orbit.html |

#### B-4. Space Simulator OSS (all free, all fit on a home PC)

| Tool | What it does | URL |
|---|---|---|
| NASA GMAT | The serious option for mission design and trajectory design (used in actual NASA practice). GUI + scripting | https://sourceforge.net/projects/gmat/ |
| Basilisk | Modular, integrated simulation of spacecraft attitude, orbit, and even flight software (Univ. of Colorado AVS Lab) | https://avslab.github.io/basilisk/ |
| 42 (NASA GSFC) | Attitude and orbital dynamics for multiple spacecraft. Also used in rendezvous and formation-flying research | https://github.com/ericstoneking/42 |
| poliastro | Orbital mechanics in Python. An ideal entry point for education and prototyping | https://github.com/poliastro/poliastro |
| Kerbal Space Program | A game, but the classic educational tool for building orbital-mechanics intuition (an educational edition, KerbalEdu, also exists) | https://www.kerbalspaceprogram.com/ |

#### B-5. Flying Other Planets on Rotors — Ingenuity's Legacy and Dragonfly

**Why it's amazing (3 lines)**
- The Mars helicopter Ingenuity was an experimental craft built to answer "can we fly in an atmosphere 1% as dense as Earth's?" — planned for 5 flights, it flew 72 before retiring in 2024 ([JPL official](https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/)). An $85 million technology demonstration changed the shape of planetary exploration.
- Its successor Dragonfly is a nuclear-powered, 8-rotor craft (car-sized) bound for Saturn's moon Titan. Launch is planned for July 2028; it will search from the air for the chemical origins of life ([JHUAPL official](https://dragonfly.jhuapl.edu/)).
- Because "the air and gravity where you fly are not Earth's," the lead role in the design goes to exhaustive simulation and ground testing. Rotor aerodynamics is an entrance you can reach even with home CFD (computational fluid dynamics — solving flows on a computer) or a physics engine.

| Item | Details | URL |
|---|---|---|
| Official | Dragonfly mission (JHU APL) | https://dragonfly.jhuapl.edu/ (annex: https://www.jhuapl.edu/destinations/missions/dragonfly ) |
| Official gallery | Dragonfly Gallery (concept art, test footage) | https://dragonfly.jhuapl.edu/Gallery/ |
| Official | NASA Ingenuity mission page | https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/ |
| Primary source | JPL: Ingenuity mission-end announcement (72 flights) | https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ |

---

### C. Cutting-Edge Topics You Can "Reproduce at Home" in Simulation

The message of this section: "even without a hundred-million-yen experimental rig, the laws of physics can be downloaded." Everything below is free OSS.

| Cutting-edge theme | Entry point on a home PC + OSS | URL |
|---|---|---|
| Event cameras | Convert your own video into an event stream with **v2e** and experience "the world as the retina sees it." For the serious route, generate events from 3D scenes with **ESIM** | https://github.com/SensorsINI/v2e / https://github.com/uzh-rpg/rpg_esim |
| Debris capture / free-floating objects | In **MuJoCo**, write an MJCF of a zero-gravity, arm-equipped satellite and physically simulate capturing a tumbling object (the official robot model collection Menagerie is the starting point) | https://github.com/google-deepmind/mujoco / https://github.com/google-deepmind/mujoco_menagerie |
| Trajectory planning / mission design | Build an Earth–Moon transfer trajectory in **GMAT**; compute a Hohmann transfer in a few dozen lines with **poliastro** (Python) | https://sourceforge.net/projects/gmat/ / https://github.com/poliastro/poliastro |
| Spacecraft attitude control | Simulate reaction-wheel control and formation flying with **Basilisk** or **42** | https://avslab.github.io/basilisk/ / https://github.com/ericstoneking/42 |
| RL for lunar rovers and legged robots | Reinforcement learning with **Gymnasium** + **MuJoCo Playground** (GPU-accelerated). Low gravity is one gravity line in the XML, and you're on the Moon | https://github.com/Farama-Foundation/Gymnasium / https://github.com/google-deepmind/mujoco_playground |
| Quantum sensing | Numerically experiment in **QuTiP** with spin Rabi oscillations and Ramsey interference (the very principles behind NV-center measurement) | https://qutip.org/ |
| Orbital-mechanics intuition | Learn "gravity turns" and "transfer orbits" in your bones with **Kerbal Space Program** (education slot) | https://www.kerbalspaceprogram.com/ |

---

### D. Resources for Visual Inspiration

#### D-1. Official Galleries and Videos Worth a Look

| Source | Content | URL |
|---|---|---|
| NASA Image and Video Library | Cross-search over 140,000 images, videos, and audio clips | https://images.nasa.gov/ |
| NASA Galleries | Entry point to per-mission galleries | https://www.nasa.gov/gallery/ |
| JAXA Digital Archives | JAXA's photo and video archive (including the terms-of-use page) | https://jda.jaxa.jp/en/service.php |
| ESA Images | ESA official image gallery | https://www.esa.int/ESA_Multimedia/Images |
| UZH Robotics and Perception Group | Demo videos of event cameras and autonomous drone racing | https://www.youtube.com/user/ailabRPG |
| Boston Dynamics | Official Atlas / Spot channel | https://www.youtube.com/@BostonDynamics |
| Unitree Robotics | Official demos of the G1 / Go2 and more | https://www.youtube.com/@unitreerobotics/videos |
| Dragonfly Gallery | Concept art and test footage of the Titan rotorcraft | https://dragonfly.jhuapl.edu/Gallery/ |

#### D-2. Universities and Research Institutes Strong in This Field (lab URLs verified live)

| Institution | Lab / Division | Field | URL |
|---|---|---|---|
| Univ. of Zurich & ETH Zurich | Robotics and Perception Group (Scaramuzza) | Event cameras, autonomous drones | https://rpg.ifi.uzh.ch/ |
| MIT | CSAIL GelSight project (Adelson lineage) | Vision-based tactile sensing | https://gelsight.csail.mit.edu/wedge/ |
| Stanford | Bao Group | Electronic skin, stretchable electronics | https://baogroup.stanford.edu/ |
| Stanford | Interactive Perception and Robot Learning Lab | Robot manipulation and perception | https://iprl.stanford.edu/ |
| CMU | Robotics Institute (founded 1979, among the world's largest) | Robotics across the board | https://www.ri.cmu.edu/ |
| TUM | MIRMI (Munich Institute of Robotics and Machine Intelligence) | Robotics and machine intelligence (70+ professors) | https://www.mirmi.tum.de/en/mirmi/home/ |
| TU Delft | QuTech (+ TNO) | Quantum computing, quantum internet, NV centers | https://qutech.nl/ |
| Sandia National Labs | Atom Interferometry group | Quantum inertial navigation | https://www.sandia.gov/quantum/atom-interferometry/ |
| Tohoku University | Space Robotics Lab (Yoshida Lab; ETS-VII, HAKUTO technology leader) | Space robotics, lunar exploration | https://astro2.mech.tohoku.ac.jp/en/ |
| University of Tokyo | Intelligent Space Systems Laboratory (aerospace) | Spacecraft GNC and autonomy | https://www.space.t.u-tokyo.ac.jp/ |
| University of Tokyo | JSK Robotics Laboratory | Humanoids, intelligent robots | http://www.jsk.t.u-tokyo.ac.jp/information.html |
| Institute of Science Tokyo (formerly Tokyo Tech) | Iwasaki Lab (solid-state quantum sensors) | NV-center quantum sensing | http://dia.pe.titech.ac.jp/en/solid-quantum-sensors/ |
| JHU APL | Dragonfly mission team (PI: Elizabeth Turtle) | Planetary rotorcraft exploration | https://dragonfly.jhuapl.edu/ |
| NASA JPL | CADRE (autonomous cooperative rovers) | Lunar multi-robot systems | https://www.jpl.nasa.gov/missions/cadre/ |

---

### E. Related Conferences, Trade Shows, and Competitions — Paths You Can "Go Watch / Enter"

#### E-1. Academic Conferences (to "read and hear" the research frontier)

| Conference | Intro (1–2 lines) | Typical timing | URL |
|---|---|---|---|
| ICRA | IEEE RAS's flagship and one of the largest robotics conferences. 2026 is Vienna (Jun 1–5); 2027 is late May | Every May–June | https://www.ieee-ras.org/conferences-workshops/fully-sponsored/icra/ (2026: https://2026.ieee-icra.org/ ) |
| IROS | The other largest-class conference, co-sponsored by IEEE/RSJ (since 1988). 2026 is Pittsburgh | Around October each year | https://www.ieee-ras.org/conferences-workshops/financially-co-sponsored/iros/ (2026: https://2026.ieee-iros.org/ ) |
| RSS | A small, selective, oral-presentation-centered "quality first" conference. 2026 is Sydney (Jul 13–17) | Around July each year | https://roboticsconference.org/ |
| CoRL | A young conference (since 2017) dedicated to robot learning (RL, imitation, foundation models). 2026 is Nov 9–12 | Around November each year | https://www.corl.org/ |
| Humanoids | The IEEE-RAS conference dedicated to humanoids (since 2000). The 25th edition is 2026-12 in Silicon Valley | November–December each year | https://2026.ieee-humanoids.org/ |
| NeurIPS (related WS) | The top ML conference. Robot-learning workshops are co-located every year (e.g., the World Models × robot learning WS @ NeurIPS 2026) | Every December | https://neurips.cc/ (WS example: https://robowm-ws.github.io/ ) |
| ICLR (related WS) | The top conference for representation learning. A home for robotics × foundation-model workshops | Every April–May | https://iclr.cc/ |

#### E-2. Trade Shows (to "go see" real machines — easy for students to attend)

| Trade show | Intro (1–2 lines) | Typical timing | URL |
|---|---|---|---|
| iREX, the International Robot Exhibition (Tokyo) | One of the world's largest robot exhibitions, running since 1974. The 2025 edition was at Tokyo Big Sight, Dec 3–6; the next is December 2027 | Biennial, December (odd years) | https://irex.nikkan.co.jp/ |
| World Robot Conference (Beijing) | China's largest combined robotics conference + exhibition + competition. The debut stage for new humanoid products | Around August each year | https://www.worldrobotconference.com/ |
| CES (Las Vegas) | One of the world's largest tech trade shows. In recent years a major launch stage for humanoids and Physical AI | Every January | https://www.ces.tech/ |
| automatica (Munich) | The global trade fair for smart automation and industrial robotics. Next edition: Jun 22–25, 2027 | Biennial, June | https://automatica-munich.com/en/ |
| CEATEC (Makuhari) | Japan's largest IT and electronics show. The 2026 edition is Oct 13–16 at Makuhari Messe. A low barrier to entry for students | Every October | https://www.ceatec.com/en/ |

#### E-3. Competitions (you can "enter" — the doorway for individuals and student teams)

| Competition | Intro (1–2 lines) | Typical timing | URL |
|---|---|---|---|
| **ROBO-ONE (Japan)** ★ featured | A biped-robot combat competition running since 2002. A Japan-born culture where **individuals can compete with self-built humanoids**; a beginner-friendly class, "ROBO-ONE Light," accepts off-the-shelf robots. The best real-world counterpart to this article's "one-person robot games" | About twice a year (spring and autumn) | https://www.robo-one.com/ (explainer: https://www.robo-one.com/abouts/view/aboutroboone/ ) |
| RoboCup | An international competition with the declared goal of "beating the World Cup champions with robots by 2050." Beyond soccer there are rescue, home, and industrial leagues, plus RoboCupJunior for secondary-school students | Around July each year (world championship) | https://www.robocup.org/ |
| World Humanoid Robot Games (Beijing) | First held in August 2025 at the Bird's Nest: 280 teams from 16 countries and 500+ humanoids competing across 26 events (winning 100 m time: 21.50 s). The 2nd edition is August 2026 | Every August | https://english.beijing.gov.cn/whatson/events/sports/202505/t20250509_4085816.html (overview: https://en.wikipedia.org/wiki/World_Humanoid_Robot_Games ) |
| DARPA Robotics Challenge (historical) | The 2012–2015 humanoid disaster-response competition. Robots of that era fell over constantly, yet it is the origin of the current humanoid boom. Great material for telling "look how far we've come in 10 years" | Ended (archive) | https://www.darpa.mil/research/programs/darpa-robotics-challenge |
| DARPA Triage Challenge (current) | An example of a current DARPA challenge: revolutionizing mass-casualty triage with sensing + autonomous systems (finals in 2025) | Program in progress | https://triagechallenge.darpa.mil/ |

> Pathway memo: to "watch," start with CEATEC and iREX (domestic, low cost) → to "enter," ROBO-ONE Light (off-the-shelf robots allowed) → RoboCupJunior (secondary schoolers) → RoboCup and academic conferences at university. There's a staircase you can climb.

---

### "Fact + Source" Notes Usable in Articles (anti-exaggeration insurance)

| Fact | Source |
|---|---|
| Event cameras: microsecond-order temporal resolution, dynamic range about 140 dB (frame cameras about 60 dB) | https://arxiv.org/abs/1904.08405 |
| Sony IMX636/637: the industry's smallest (at announcement) 4.86 µm event pixels, 1280×720 | https://www.sony-semicon.com/en/news/2021/2021090901.html |
| Meta's sEMG band: calibration-free generic decoding, 20.9 words/min mid-air handwriting (Nature 645, 2025) | https://www.nature.com/articles/s41586-025-09255-w |
| ADRAS-J autonomously approached to 15 m of non-cooperative debris (about 11 m long, about 3 tons) (2024) | https://www.astroscale.com/en/news/astroscales-adras-j-achieves-historic-15-meter-approach-to-space-debris |
| Ingenuity flew 72 times in 3 years; mission ended 2024-01. Cost as a technology demonstration: about $85 million | https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ / https://www.space.com/space-exploration/missions/nasa-begins-building-nuclear-powered-dragonfly-drone-for-2028-launch-to-saturn-moon-titan |
| Dragonfly: total mission cost about $3.35 billion, launch planned 2028-07 (Falcon Heavy), CDR passed | https://www.space.com/space-exploration/missions/nasa-begins-building-nuclear-powered-dragonfly-drone-for-2028-launch-to-saturn-moon-titan |
| Varda W-1 manufactured Ritonavir crystals on orbit and recovered them on the ground 2024-02 (a first-of-its-class for a private company) | https://www.space.com/varda-in-space-manufacturing-capsule-landing-success |
| NASA VIPER cancelled 2024-07 (about $450 million already invested; the cancellation saves about $84 million) | https://spaceflightnow.com/2024/07/18/nasa-cancels-half-billion-dollar-water-ice-seeking-moon-rover/ |
| CADRE: three autonomous rovers headed to Reiner Gamma on the IM-3 lander (planned 2026) | https://www.jpl.nasa.gov/missions/cadre/ / https://www.nasa.gov/missions/tech-demonstration/cadre/nasas-mini-rover-team-is-packed-for-lunar-journey/ |
| An on-orbit test of a quantum inertial sensor (atom interferometer) planned for X-37B flight 8 (2025) | https://theconversation.com/quantum-alternative-to-gps-navigation-will-be-tested-on-us-military-spaceplane-262967 |

---

## Appendix H: Training Log Excerpts — 13 Generations of Growth Curves, in Raw Numbers

Raw-data tables excerpting the main values from each generation's training log at the eval rows (roughly every 5.2M steps) — all measured inside the MuJoCo simulation. Coarser than a plot, but you can check against the primary record which generation grew — or got stuck — when and how. (Reward designs differ between generations, so **rewards cannot be compared vertically across generations**; only look at the trend within a single generation.) ep_len is survival steps (×0.02 s), fwd_v is forward velocity in m/s, crash is the collision rate.

### walk10 (through 26M, 6 evals)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 194 | 31 | 1.09 | — |
| 5M | 258 | 42 | 0.93 | — |
| 10M | 338 | 57 | 0.83 | — |
| 16M | 469 | 81 | 0.80 | — |
| 21M | 691 | 126 | 0.72 | — |
| 26M | 1861 | 371 | 0.71 | — |

### walk11 (through 31M, 7 evals)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.09 | — |
| 5M | 265 | 43 | 0.95 | — |
| 10M | 354 | 58 | 0.85 | — |
| 16M | 471 | 78 | 0.78 | — |
| 21M | 685 | 118 | 0.67 | — |
| 26M | 1673 | 316 | 0.67 | — |
| 31M | 3331 | 667 | 0.83 | — |

### walk12 (through 52M, 11 evals)

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

### walk12b (through 58M, 12 evals)

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

### walk12c (through 68M, 14 evals)

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

### walk13 (through 131M, 26 evals)

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

### walk13b (through 126M, 25 evals)

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

### walk13c (through 68M, 14 evals)

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

### walk13d (through 147M, 29 evals)

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

### walk13e (through 147M, 29 evals)

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

### walk4 (through 42M, 9 evals)

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

### walk5 (through 42M, 9 evals)

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

### walk6 (through 37M, 8 evals)

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

### walk8 (through 37M, 8 evals)

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

### walk9 (through 37M, 8 evals)

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

## Appendix I: Questions I Expect to Get (FAQ)

Honest, pre-emptive answers to the questions readers are likely to have.

**Q. How much did it all cost?**
A. The only additional investment was a PC with a GPU (a few hundred thousand yen). The software — physics engine, robot models, motion data, training frameworks — was all free (OSS). The running cost is electricity: a bit under 100 yen per event trained (the measured estimate in Section 12.1). As hobbies go, my honest impression is that it's cheaper than photography or golf.

**Q. How long did it take?**
A. The experiments in this article span roughly a few weeks. But I wasn't glued to the screen all day — it was a loop of "set it up in the evening, check it at night." The GPU's practice hours far exceed my working hours.

**Q. How much programming do I need to know?**
A. I'm an image-processing engineer myself, but most of the implementation work in this article was delegated to AI coding agents (as attributed at the top). What I actually needed was not the ability to write code but the ability to decide "what to measure to catch a lie." I think we're now in an era where even a programming beginner, teamed up with AI, can at least reach the entrance. But **never leave the verification of results to the AI** — that part alone is the human's job.

**Q. Is there any point without real hardware?**
A. I believe there is, which is why I keep going. Three reasons. (1) If you align the observations with a real robot's sensor configuration, the policy can in principle be carried over to real hardware (we're at least standing at the entrance to sim-to-real). (2) Failures that are dangerous or expensive on real hardware (thousands of falls) can only be accumulated in simulation. (3) Even in real-robot development, running simulation first is now the standard procedure anyway. That said, there are certainly factors that break on real hardware even when simulation is perfect (unmodeled friction, latency, flex), and all I can do is say honestly that those remain unverified.

**Q. How much did you leave to the AI, and what did you actually do?**
A. Setting the direction, proposing hypotheses, doubting results, deciding when to stop — that was me. Writing code, running experiments, tallying the numbers — that was the AI. For example, "add an event-camera-style temporal difference" was my idea; "solve the cylinder intersection analytically in that implementation" was the AI's work. Conversely, my job was to lay down the rule: never take a report like "it lifted 48 mm" at face value — always verify on video before granting a pass. And following that rule, it was the AI itself that actually scrutinized the footage and pinned the result down as an illusion (a launch caused by an initialization bug). I'm fond of this as an example of the division of labor actually working.

**Q. Doesn't all the failure get you down?**
A. Some days, yes. But failure in this field is the kind whose cause can always be identified (the physics engine is reproducible). A failure whose cause you understand becomes an asset — as the chronicle in Appendix A in fact became. For the record, the lowest point was when three different cheats were invented in three consecutive weeks.

**Q. Where should I start?**
A. My recommended route: (1) install MuJoCo and get a Menagerie robot on screen (1 day) → (2) stand your favorite model in a keyframe pose and run the physics (1 day) → (3) run the mujoco_playground quadruped locomotion tutorial (a few days) → (4) pick one "event" of your own and write the reward (this is where the swamp begins). Reading Appendix D of this article (the lessons) before step (4) should make the swamp about 30% shallower.

**Q. Can kids and students do this?**
A. The simulation itself is free, so even without a GPU you can run small experiments on CPU (training gets slower, but something like quadruped walking is realistic). The resource kit in Chapter 13 lays out a pathway from fun entry points (official videos) all the way to competitions (ROBO-ONE accepts individual entrants).

**Q. Why a sports day?**
A. Because competition brings in measurement and discipline (Chapter 1). Also, because it's simply fun. If it weren't fun, it wouldn't last for weeks.

**Q. Isn't this article too long?**
A. Yes. But I added a table of contents and the three-course guide (at the top) so you can pick out just the parts you need. Please regard the length as an experiment in "how deep can one pastime be dug" — that, too, is a kind of competition.
