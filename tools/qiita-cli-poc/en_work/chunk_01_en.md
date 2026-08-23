#### Plain language: what is the ZMP?

Imagine standing on two bathroom scales placed side by side. The pressure your soles receive from the ground has a representative point — "effectively, all the support is concentrated at this one spot" (the center of pressure). The gist of ZMP theory is this: **as long as that point stays inside the sole (the support polygon), the robot will not begin the tipping rotation that pivots on its toes or heels.** The vague demand "don't fall over" turned into the computable condition "keep the ZMP inside the sole." For the following 40 years, bipedal walking control has been built almost entirely on that one line.

---

### 2. Honda's secret decade (1986-1996) — the P2 shock

In 1986, Honda began bipedal walking research as a top-secret internal project. The E series, starting with E1, were legs-only experimental machines — at first, 20 seconds per step. E2 reached near-human dynamic walking (1.2 km/h), and the program advanced to the P series, which put a torso and arms on the legs [^honda-st][^honda-p2].

Then came **December 1996: the announcement of P2**. A robot in the 180-cm class, "self-contained" with power and computers all onboard, walked smoothly and climbed stairs. Because nothing had leaked outside for ten years, it is said that robot researchers around the world literally rose from their chairs at the announcement. Equipped with three posture-control systems — for uneven floors, disturbances (pushes), and stairs/slopes — it became the technical benchmark for humanoids from then on [^honda-p2]. In April 2026, this historical significance was officially engraved in the form of IEEE Milestone recognition [^honda-ieee][^honda-topics].

---

### 3. Japan's golden age (2000s) — ASIMO, HRP, QRIO

**ASIMO** (announced November 2000) was the culmination of the P series. From 2002 it "worked" at Miraikan (the National Museum of Emerging Science and Innovation), giving 15,466 demonstrations over 20 years to an estimated 2+ million visitors [^miraikan-a][^miraikan-p]. Each generation added new tricks — running, walking backwards, hopping on one foot — until it "graduated" from Miraikan on March 31, 2022, giving its final demonstration at Honda headquarters at the end of that month [^miraikan-p].

On the national-project side, METI's HRP lineage produced **HRP-2 Promet** (2002, Kawada Industries + AIST). The important part was that it could get up from lying face-up or face-down — a turning point away from the era of "a fall = the end of the experiment." The design was by Yutaka Izubuchi [^hrp2]. 2009's **HRP-4C** — 158 cm, 43 kg, a "cybernetic human" matched to the average build of a young Japanese woman — stood on a Tokyo Fashion Week stage one week after its announcement [^hrp4c].

Sony's **QRIO** (2003), small as it was, had the polish to be listed in the 2005 Guinness Book as the world's first bipedal robot that could run. But on January 26, 2006, its development was cancelled along with AIBO [^qrio]. From here, Japanese humanoid research entered a quiet "winter" with few flashy announcements — not because the technology died, but because no exit to a business could be seen.

---

### 4. The heretical lineage — machines that walk without motors (1990)

Roll the clock back a little. In 1990, Tad McGeer demonstrated **passive dynamic walking**: a two-legged machine with no motors and no control computer, placed on a gentle slope, "settles" into a stable gait [^mcgeer]. The discovery that walking, before being a product of precision control, is **a natural mode of pendulum dynamics**.

If the ZMP school's philosophy is "keep controlling at all times so you never fall," the passive-walking school's is "the dynamics walk by themselves, so control need only give a minimal nudge." Energy consumption can be a few dozen times lower than ZMP-style machines. This lineage flows into later underactuated walking, hybrid zero dynamics, and the design philosophy of "legs that don't imitate humans," like Cassie's.

---

### 5. The DRC (2015) — what the "fall compilation" taught

With the 2011 Fukushima Daiichi nuclear accident as the direct motive, DARPA held the disaster-response robot competition, the **DARPA Robotics Challenge**. At the June 2015 finals (Pomona, USA), teams competed on 8 tasks — driving a car, opening doors, turning valves, walking over rubble — and KAIST's **DRC-HUBO** from Korea completed all tasks in about 44 minutes to win the $2 million prize [^drc-kaist][^drc-ieee2]. DRC-HUBO had wheels at its knees; the pragmatic call of "biped only when necessary" paid off.

But what stayed in the world's memory was not the victory — it was the **fall compilation**. Footage of robots from the world's finest teams toppling over one after another, as if in slow motion, in front of doorknobs, drills still in hand [^drc-ieee]. Those clips drew their share of mockery, but for the research community they were an accurate measurement of the field's position — of just how hard it still was, in 2015, to work in an unknown environment without leaning on external power and network. Only one robot, CHIMP, fell, got back up on its own, and continued [^drc-na]. After the DRC, research programs worldwide turned their rudders decisively from "succeed once in a demo" to "robustness."

---

### 6. The Atlas era (2013-2024) — from hydraulic acrobatics to electric practicality

Boston Dynamics' hydraulic **Atlas**, introduced as the DRC's standard machine, spent the following decade thrilling the world on YouTube. Running, jumping, backflipping. Behind it lay QP-based whole-body control and optimization-based motion planning; the methods the MIT team built for the DRC Atlas are published as papers [^kuindersma].

In April 2024, Boston Dynamics announced the hydraulic Atlas's retirement and a fully electric new Atlas at the same time [^bd-atlas][^tc-atlas]. Hydraulics are powerful, but loud, complex, and dependent on special working fluid — maintenance costs had blocked commercialization. Electrification was a declaration of conversion from "the pinnacle of research" to "a tool used in Hyundai's factories."

Around the same time, Agility Robotics, spun out of Oregon State, was walking a different road. The ostrich-legged **Cassie** (sold as a research platform from around 2016-17) abandoned the humanoid form to focus on legs, and later set the Guinness world record for a bipedal robot's 100 m [^agility]. **Digit**, which put a torso, arms, and perception on those legs, became the machine running at the front of commercial deployment in logistics warehouses [^agility].

---

### 7. The RL + sim-to-real wave (2019-) — control laws: no longer written, but trained

In 2019, the result Hwangbo et al. of ETH Zürich showed on the quadruped ANYmal [^hwangbo] was the turning point for legged robots as a whole. Train a policy by reinforcement learning in simulation, then transfer it to the real machine as-is (zero-shot). The key was domain randomization — randomizing physical parameters so the policy learns right through "the simulator's lies."

For bipeds, in 2021 an RL policy ran on the real Cassie, climbing and descending stairs **with no exteroceptive sensors, proprioception only** (only internal senses such as joint angles and forces) [^siekmann]. In 2023, a Berkeley group reported real-robot humanoid walking with a Transformer-based policy [^rado]. The ZMP-descended "build a model and solve it" control and RL's "suffer in simulation and remember" control are now heading not toward confrontation but toward layering (a model-based foundation + learned robustification).

---

### 8. The rise of China (2023-) — the age of quantity and price

The fastest to ride this wave was China. Unitree, UBTech, Fourier, and "Tiangong," developed by Beijing's state-affiliated innovation center. Two symbolic events:

- **April 19, 2025, Beijing**: the world's first humanoid half-marathon. Tiangong Ultra finished the 21.0975 km in 2:40:42 and won [^cgtn].
- **August 14-17, 2025, Beijing**: the 1st World Humanoid Robot Games. At the 2022 Winter Olympics' Ice Ribbon (the National Speed Skating Oval), 280 teams from 16 countries and 500+ robots gathered, and Unitree took four crowns — 1500 m, 400 m, 100 m hurdles, and the 4×100 m relay [^whrg][^ran][^cnbc]. The 100 m went to Tiangong at 21.50 s [^gt].

And then, price. The Unitree G1's base configuration is in the low $10,000s (official site listing: US$13.5K+) [^g1]. The change from ASIMO's era — "a robot worth hundreds of millions of yen, something you go look at" — to "something a university lab simply purchases" happened within these two years. Note that robots also kept falling in grand style at the Beijing games [^smith]; ten years on from the DRC fall compilation, I think the accurate summary is that falling changed from "a disgrace" into "a consumable, budgeted for in advance."

---

### 9. The genealogy of control theory — five generations, 2-3 lines each

**① ZMP (1968-72 / Vukobratović; implemented by Kato's lab and Honda)**
The criterion that the tipping rotation cannot begin as long as the sole's center of pressure stays inside the support polygon. It became the vocabulary of all walking control that followed.
Representative reference: Vukobratović & Borovac, "Zero-Moment Point — Thirty Five Years of its Life" [^zmp35]

**② Preview control (2003 / Kajita et al., AIST)**
Simplify the robot to a "cart on a table" (linear inverted pendulum) and generate the center-of-mass trajectory by **previewing the ZMP targets several steps ahead**. The backbone of HRP-series walking; being easy to implement, it became the standard worldwide.
Representative reference: Kajita et al., ICRA 2003 [^kajita]

**③ Capture Point (2006 / Pratt et al.)**
Computes in closed form, from the linear inverted pendulum, "if pushed right now, **where must I place my foot to come to a stop**." It reframed walking as continuous avoidance of falling and theorized the one-step recovery from push disturbances.
Representative reference: Pratt et al., Humanoids 2006 [^pratt]

**④ MPC / WBC (2010s / MIT, IHMC, and others)**
MPC re-optimizes the next few hundred ms of motion every control cycle; whole-body control (WBC) solves all the body's tasks simultaneously by QP under contact-force and joint-torque constraints. Hydraulic Atlas's acrobatics and the DRC machines' work skills belong to this generation.
Representative reference: Kuindersma et al., Autonomous Robots 2016 [^kuindersma]

**⑤ RL + sim-to-real (2019- / ETH, OSU, Berkeley, and others)**
Train policies by reinforcement learning in thousands of parallel simulations, and transfer to hardware via domain randomization. Robustness to hard-to-model contact, rough terrain, and faults improved by orders of magnitude.
Representative references: Hwangbo et al. 2019 [^hwangbo] / Siekmann et al. 2021 [^siekmann] / Radosavovic et al. 2023 [^rado]

#### Plain language: five generations, by bicycle

① "Knows the condition for not falling over." ② "Watches the road a few seconds ahead and steers." ③ "Knows instantly where to plant a foot if shoved." ④ "Optimizes how every muscle in the body is used, every instant, on a calculator." ⑤ "Falls ten thousand times with training wheels on and learns it in the body." Actual modern robots are approaching a state with ④'s skeleton and ⑤'s reflexes layered on top — "both the theory and the body knowledge," so to speak.

---

### 10. Japan's contributions, and where things stand

The first 30 years of this 50-year history were, essentially, Japanese history. The world's first full-scale humanoid (WABOT-1) [^robogaku], corporate implementation of dynamic walking (Honda E/P/ASIMO) [^honda-p2], the world standard for walking-pattern generation (Kajita's preview control) [^kajita], a humanoid that could get back up (HRP-2) [^hrp2], a small machine that could run (QRIO) [^qrio] — every one a primary invention. ASIMO retired in 2022, but its control and balance technology lives on inside Honda in avatar-robot research and elsewhere [^honda-st].

Players remain today: the Kawada-line HRP assets, Kawasaki Heavy Industries' humanoid "Kaleido" (first shown at the 2017 International Robot Exhibition; no official primary URL reachable as of this writing), and Toyota's teleoperated T-HR3 (announced 2017) [^toyota-wiki]. But it is also, in all fairness, a fact that the current front-runners in "quantity, price, and iteration speed" are the Chinese makers. Japan's 50 years of accumulation has not vanished — ZMP and preview control are still being computed, today, inside the robots running in Beijing.

---

### 11. Coda — 1973's 45 seconds and my home's 0.002 seconds

WABOT-1's one step took 45 seconds. National projects and corporate skunkworks took 30 years to solve "walking," the DRC's fall compilation taught humility, RL replaced the writing of control laws with training, and the Chinese makers cut prices by two orders of magnitude.

And now, 2026. What the main part of this article did was run imitation learning and RL for a G1 on a home PC with one consumer GPU, and obtain a walking policy in a few hours. A simulation of 0.002 seconds per frame, hundreds of thousands of steps every second. In the 45 seconds WABOT-1 takes to make one step, the robot inside my home simulator falls tens of thousands of times — and gets a little better with each fall. On top of 50 years of theory and failure, there is now a place where an individual can stand. The height of that scaffolding occasionally gives me vertigo.

---

### Source list

[^robogaku]: Robo-gaku (Robotics Society of Japan), "Wabot 1" https://robogaku.jp/history/integration/I-1973-1.html
[^waseda50]: Waseda University, 「早稲田のロボット: ヒューマノイド研究50年の歩み」 https://www.waseda.jp/inst/fro/news/2026/06/10/1976/
[^nikkei-w1]: Nikkei, 「世界初の人間型ロボ『WABOT-1』 45秒で一歩 確かな進歩」 https://www.nikkei.com/article/DGKDZO70746270T00C14A5MZ9000/
[^wabot2]: Waseda University Humanoid Robotics Institute booklet (WABOT-2) http://www.humanoid.waseda.ac.jp/booklet/kato_2.html
[^zmp35]: Vukobratović & Borovac, "Zero-Moment Point — Thirty Five Years of its Life," IJHR 2004 (PDF) https://www.cs.cmu.edu/~cga/legs/vukobratovic.pdf
[^honda-st]: Honda Stories, 「ASIMOの原点『P2』…IEEEマイルストーンに認定」 https://global.honda/jp/stories/025.html
[^honda-p2]: Honda official, 「Hondaのヒューマノイドロボット P2」 https://global.honda/jp/tech/robotics/P2/IEEE/
[^honda-ieee]: Honda R&D, 「Honda P2 IEEEマイルストーン認定」 https://global.honda/jp/RandD/activity/rdtopics/IEEE-P2/
[^honda-topics]: Honda corporate news (2026-04-28) https://global.honda/jp/topics/2026/c_2026-04-28a.html
[^miraikan-a]: Miraikan, 「ヒューマノイドロボット ASIMO(2002〜2022)」 https://www.miraikan.jst.go.jp/resources/archives/asimo.html
[^miraikan-p]: Miraikan press release, 「ありがとう!ロボット『ASIMO』」 https://www.miraikan.jst.go.jp/news/press/202201312305.html
[^hrp2]: Wikipedia (en), "HRP-2" https://en.wikipedia.org/wiki/HRP-2
[^hrp4c]: AIST press release, 「人間に近い外観と動作性能をもつヒューマノイドロボット(HRP-4C)」 2009-03-16 https://www.aist.go.jp/aist_j/press_release/pr2009/pr20090316/pr20090316.html
[^qrio]: Wikipedia (en), "QRIO" https://en.wikipedia.org/wiki/QRIO
[^mcgeer]: McGeer, "Passive Dynamic Walking," IJRR 9(2), 1990 https://journals.sagepub.com/doi/abs/10.1177/027836499000900206
[^kajita]: Kajita et al., "Biped Walking Pattern Generation by using Preview Control of Zero-Moment Point," ICRA 2003 (PDF) https://mzucker.github.io/swarthmore/e91_s2013/readings/kajita2003preview.pdf
[^pratt]: Pratt et al., "Capture Point: A Step toward Humanoid Push Recovery," Humanoids 2006 (PDF) https://www.cs.cmu.edu/~cga/legs/Pratt_Goswami_Humanoids2006.pdf
[^kuindersma]: Kuindersma et al., "Optimization-based locomotion planning, estimation, and control design for the Atlas humanoid robot," Autonomous Robots 2016 https://doi.org/10.1007/s10514-015-9479-3
[^drc-kaist]: KAIST News, "KAIST's DRC-HUBO Wins the DARPA Robotics Challenge" https://www.kaist.ac.kr/newsen/html/news/?mode=V&mng_no=4379
[^drc-ieee]: IEEE Spectrum, "DARPA Robotics Challenge Finals Winner" https://spectrum.ieee.org/darpa-robotics-challenge-finals-winner
[^drc-ieee2]: IEEE Spectrum, "How KAIST's DRC-HUBO Won the DARPA Robotics Challenge" https://spectrum.ieee.org/how-kaist-drc-hubo-won-darpa-robotics-challenge
[^drc-na]: New Atlas, "South Korea's Team KAIST wins 2015 DARPA Robotics Challenge" https://newatlas.com/darpa-drc-finals-2015-results-kaist-win/37914/
[^bd-atlas]: Boston Dynamics Blog, "An Electric New Era for Atlas" https://bostondynamics.com/blog/electric-new-era-for-atlas/
[^tc-atlas]: TechCrunch, "Boston Dynamics' Atlas humanoid robot goes electric" (2024-04-17) https://techcrunch.com/2024/04/17/boston-dynamics-atlas-humanoid-robot-goes-electric/
[^agility]: Wikipedia (en), "Agility Robotics" (Cassie/Digit/100m Guinness record) https://en.wikipedia.org/wiki/Agility_Robotics
[^hwangbo]: Hwangbo et al., "Learning agile and dynamic motor skills for legged robots," Science Robotics 2019 (arXiv) https://arxiv.org/abs/1901.08652
[^siekmann]: Siekmann et al., "Blind Bipedal Stair Traversal via Sim-to-Real Reinforcement Learning," RSS 2021 (arXiv) https://arxiv.org/abs/2105.08328
[^rado]: Radosavovic et al., "Real-World Humanoid Locomotion with Reinforcement Learning," 2023 (arXiv) https://arxiv.org/abs/2303.03381
[^g1]: Unitree official, "G1" https://www.unitree.com/g1
[^cgtn]: CGTN, "'Tiangong' robot wins world's first humanoid half-marathon" (2025-04-19) https://news.cgtn.com/news/2025-04-19/-Tiangong-robot-wins-world-s-first-humanoid-half-marathon-1CH3pjBuhOw/index.html
[^whrg]: Wikipedia (en), "World Humanoid Robot Games" https://en.wikipedia.org/wiki/World_Humanoid_Robot_Games
[^ran]: Robotics & Automation News, "Unitree dominates inaugural World Humanoid Robot Games with four gold medals" https://roboticsandautomationnews.com/2025/08/26/unitree-dominates-inaugural-world-humanoid-robot-games-with-four-gold-medals/93926/
[^cnbc]: CNBC, "Tesla Optimus rival Unitree shines at the 'World Humanoid Robot Games' in China" (2025-08-18) https://www.cnbc.com/2025/08/18/world-humanoid-robot-games-china-tesla-unitree.html
[^gt]: Global Times, "First World Humanoid Robot Games conclude" https://www.globaltimes.cn/page/202508/1341057.shtml
[^smith]: Smithsonian Magazine, "World's First 'Robot Olympics' Featured Soccer, Kickboxing and Lots of Falling Down" https://www.smithsonianmag.com/smart-news/worlds-first-robot-olympics-features-soccer-kickboxing-and-lots-of-falling-down-180987199/
[^toyota-wiki]: Wikipedia (en), "Toyota Partner Robot" (T-HR3, 2017) https://en.wikipedia.org/wiki/Toyota_Partner_Robot

#### Unconfirmed items (honest disclosure)

- The statement that **WL-10RD (1984) achieved the world's first ZMP-based dynamic walking** rests on received accounts and retrospective papers; it could not be confirmed at a primary Waseda URL. The main text keeps it at "is held to be."
- **Cassie's specific 100 m time (24.73 s)**: Oregon State's official news is bot-blocked (HTTP 403) and its content could not be verified, so the text omits the time and states only "set the Guinness record" (cross-checked via Wikipedia's Agility Robotics article).
- **Kawasaki Heavy Industries' Kaleido**: could not reach a primary URL in the official site or press (no mention on kawasakirobotics.com). Noted as such in the main text too.
- **Toyota T-HR3's official press release**: global.toyota returns 403 and is unreachable. Only the 2017 announcement is cross-checked via Wikipedia (Toyota Partner Robot). Details of the master maneuvering system are not written in the text.
- **Kuindersma et al. 2016**: Springer redirects to authentication, so the paper body is unverified (the DOI is valid).
- **Honda E2's 1.2 km/h and the E-series secrecy narrative**: relies on the descriptions in Honda Stories and the IEEE recognition pages (via search-result summaries).

# 5. Event 1: Sprint (20m Straight)

The first event is the simplest one: walk 20 m straight ahead. And in this simplest of events, we lost **three times in a row**. The record of those three straight losses may be the thing this article most wants to convey.

## 5.1 First runner: walked beautifully. In a circle

The first runner (walk9), trained with an imitation reward against the reference (LAFAN1) plus a fall penalty, bent its knees supplely, swung its arms, and to the eye walked admirably. But plot its world-frame trajectory, and it **had been walking in a large circle**. The imitation reward looks only at "do the joint angles resemble the reference?", so wherever the body heads, near-perfect marks come out. A sprinter leaving the track and strolling off toward the stands. And the athlete (the policy) wears the face of a perfect score.

## 5.2 Second runner: add a penalty, and it takes up residence in the penalty's "saturation zone"

Fine, then — punish lateral deviation. We added a soft, exp-shaped position penalty (walk10/11). The result was unexpected: the athlete strayed 3–4 m off the course and kept walking there, perfectly untroubled. An exp-shaped penalty flattens to nearly zero once you're 1 m off — beyond that, **straying further adds no punishment: a "saturation zone."** Where the gradient (the cue for improvement) has vanished, a penalty may as well not exist.

## 5.3 Third runner: add a cutoff, and learning shrivels instead

Then let's have a penalty that can't saturate: "stray 1.5 m from the course and you're disqualified on the spot" (episode over; an episode = one practice trial), the corridor termination (walk12/12b). The cheating vanished. In exchange, **learning was cut in half.** In the early phase of exploring how to walk, the body sways — of course it does — but each sway now means instant disqualification, so experience never accumulates. Reward plateaued around 450; survival stuck at 8 seconds.

## 5.4 The root cause: it couldn't see the white line

Three losses in, we finally doubted the observation vector. And we hit a fact so anticlimactic it deflates you. **The policy's observation contained neither its own lateral position nor its yaw angle (heading).**

Imagine it from the athlete's position. You're made to walk blindfolded, and you lose points for leaving the course. But you cannot see where the white line is. The best you can manage is "trying to walk as straight as possible" — **the control of returning after having drifted is impossible in principle.** The quantity being punished was not in the observation — a textbook case of partial observability (POMDP), reached only after missing three times with real measurements.

The fix was a mere two dimensions: adding `steer = [lateral offset, yaw angle]` to the observation (walk12c).

(In the table, "@26M steps" means "at the 26-million-training-step mark." Not meters of distance — this notation recurs from here on, so see also the "training steps" entry in the glossary.)

> **🍙 Plain-Language Corner (sprint edition)**
> What happened here, in one sentence: "**before scolding someone over their test score, check that you showed them the textbook.**" An AI knows only its observations (= the information you showed it). Scold it with "points off for leaving the course!" — if you haven't shown it where the course is, there's no way for it to correct. In human school sports, too, nine tenths of "why can't you do this?!" turns out to be "because nobody taught me." That same structure occurs in the world of equations.

| Metric (same-point comparison) | walk9 (imitation only) | walk12b (termination only) | **walk12c (steering observation added)** |
|---|---|---|---|
| Reward @26M steps | 283 | 274 | **2,057 (7×)** |
| Reward @42M steps | — | plateaued at ~450 | **6,522** |
| Survival @42M | — | ~8 s | **19.5/20 s (nearly a full run)** |
| Lateral RMS (measured run) | circular path | — | **0.14m / 20.5m forward** |

![Effect of the steering observation](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/curve_steering_obs_effect.png)
*Figure: learning curves of three runs under identical conditions, changing only the observation. Two added dimensions made it a different sport (plotted from measured logs)*

![G1 straight walking](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk12c_37M.gif)
*Video: walk12c (at 37M) finishing the 20.5m. Speed 1.36m/s, knee range 9–78°, arm swing ±20–30° (measured in simulation)*

![Forces at the feet](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_feet_forces.gif)
*Video: close-up of the same walk's feet with contact forces (arrows) visualized. The "invisible force" of the body's weight being handed over onto one foot becomes visible (measured in simulation)*

## 5.5 Know-how banked by the sprint (excerpts)

As a by-product of three straight losses, plenty of fine-grained lessons accumulated. Leaving a few here.

- **Whatever quantity the reward punishes must be included in the observation.** The order of suspicion shouldn't have been soft penalty → termination → add observation; we should have suspected the observation first.
- **Measure each joint's limits before setting the action-space bounds.** With the residual amplitude set to a uniform 0.5 rad for all joints, the knee — because of its one-sided range of motion from standing — could produce at most 29°, structurally short of the 40° a human swing leg needs. Widening just the knee to 1.0 rad solved it.
- **Measure the signs before writing a reward.** The G1's shoulder pitch is "positive = hand goes backward." Write an arm-swing reward from assumption, and it optimizes in reverse.
- **Check the reference motion's coordinate conventions.** LAFAN1's quaternions (a notation expressing rotation with 4 numbers) are in xyzw order, unlike MuJoCo's wxyz. Get this wrong and every frame is subtly twisted.

## 5.6 Bonus: how to read a learning curve (a pattern reproduced four times)

In this setup, walking-learning curves had a clear stereotype — four training runs, four identical shapes.

- **Early phase (0–20M steps)**: a flatline at survival of a few dozen steps. You'll itch to fiddle with the settings here, but this is the normal silence of "still searching for how to stand."
- **Surge phase (25–35M)**: survival time and reward jump severalfold. The qualitative transitions — standing → a few steps → periodic walking — happen inside this window.
- **Judgment point (~37M)**: the scores at this point tell you nearly everything about a configuration's "pedigree." Not once in this article's experiments did a configuration that was bad at 37M blossom at 100M.

The practical implication: **pass judgment at 37M, and only let the promising ones run long.** GPU time is finite, so instead of "run every configuration to 150M and compare," the two-stage selection of "sieve at 37M, winners only to 150M" was the trick that kept this within a home-hosted budget. In animal-breeding terms: select the juveniles on early promise, then raise only those to adulthood — that procedure.

## 5.7 Deep Dive: The Theory Shelf — PPO, the Imitation-Learning Lineage, and the Academic Pedigree of Reward Hacking
(supplement to Chapter 5, "Sprint")

The main text tossed off "ran PPO for 37 million steps and it walked" — but what is happening inside that PPO, and why did the strategy settle on mocap imitation? Let's peek at the theoretical background together.

### 5.7.1 Inside PPO, in three stages

#### Stage 1: policy gradient — "raise the probability of actions that went well"

The policy is a neural net π(a|s). Feed in a state and out comes a probability distribution over actions. The principle of policy-gradient methods can be said in one line: **actions that happened to lead to good outcomes get chosen more readily next time.** In equations: push up the gradient of log π, weighted by the advantage (how much better than average that action was).

Do this naively and two problems appear. (1) Data sampled once can be used for only one update — poor sample efficiency. (2) The gradient is noisy, and a single update can change the policy so much that it collapses.

#### Stage 2: the importance ratio and the clip — implementing "don't change too much at once"

PPO (Schulman et al. 2017 [^ppo]) solves both at once. The key is the **importance ratio** r(θ) = π_new(a|s) / π_old(a|s): by what factor the probability of choosing that action has changed between "the policy that collected the data" and "the policy now being updated." Correct with this ratio, and old data can be reused for many epochs (the paper's "novel objective function that enables multiple epochs of minibatch updates").

But leave the ratio unchecked and updates keep going until it reaches 10× or 100×, wrecking the policy. So PPO puts a **clip** into the objective:

L = min( r·A, clip(r, 1−ε, 1+ε)·A )   (ε being, say, 0.2)

Read it like this. When advantage A is positive (a good action), raising r pays — but it **caps out at 1+ε**. Beyond that, raising the action's probability adds not one cent to the objective, so the gradient goes to zero and the update stops on its own. When A is negative, the same lid clamps down in the opposite direction. Implementing "the policy can move only ±20% per update" not as a constraint but as **the very shape of the objective function** — that is PPO's invention. Its predecessor TRPO did the same idea with rigorous constrained optimization; the PPO paper positions itself as having "some of the benefits of TRPO, while being far simpler to implement, more general, and better in sample efficiency" [^ppo].

##### Plain language: play in the steering wheel

PPO's clip is like a driving-school instructor setting the rule "no more than half a turn of the wheel at a time." Even in the right direction, crank it all the way and the car spins. Turn a little → watch the car's response (collect new data) → turn a little more. This pile of small corrections was the insurance that let the long journey of 37 million steps finish without collapse.

#### Stage 3: GAE(λ) — how to estimate the advantage

To measure "how much better than average was that action," you have to decide how far into the future to use measured rewards, and where to switch over to the value function's prediction (the function that estimates the rewards still to come).

- Use measurements longer → small bias, but large noise (variance)
- Switch to prediction sooner → small noise, but you eat the value function's error (bias)

GAE (Schulman et al. 2015 [^gae]) blends these two choices continuously with λ ∈ [0,1]. In the paper's phrasing, "an exponentially-weighted estimator of the advantage function, analogous to TD(λ)." λ=0 measures just one step (low variance, high bias); λ=1 measures the whole episode (high variance, low bias); in practice something around 0.95 is common. In brax's PPO too, this GAE computation is wedged in right after the rollout.

| Part | In one phrase | Source |
|---|---|---|
| Policy gradient | Raise the probability of actions that went well | — |
| Importance ratio r | The correction factor for reusing old data | [^ppo] |
| Clip | Cap r at 1±ε: "never change too much at once" | [^ppo] |
| GAE(λ) | Blend measurement and prediction with λ to estimate the advantage | [^gae] |

### 5.7.2 The imitation-learning lineage — from DeepMimic to PHC

Once you have experienced what a minefield "design a reward from scratch and make it walk" is (the 11-cheat streak in the main text), you feel in your bones why this field converged on **mocap tracking**. The lineage, in a table:

| Year | Method | One-line summary | URL |
|---|---|---|---|
| 2018 | **DeepMimic** (Peng et al.) | RL with pose agreement to a mocap clip as the reward; reproduced motions up to backflips. Established the two great staples, RSI and early termination | [^deepmimic] |
| 2021 | **AMP** (Peng et al.) | Stop hand-writing the agreement reward; have a GAN-style discriminator score "does that motion look like the dataset?" Manual clip selection/alignment becomes unnecessary; learns style from unorganized motion collections | [^amp] |
| 2022 | **ASE** (Peng et al.) | Adversarially learn a reusable "skill embedding space" from large-scale motion data; downstream tasks are solved purely by operating in the latent space | [^ase] |
| 2023 | **PHC** (Luo et al.) | One policy perpetually tracks thousands of clips. Fault-tolerant real-time avatar control, including recovery from falls | [^phc] |

The flow in one line: **"tracking one clip (DeepMimic) → imitating a distribution of styles (AMP) → acquiring a skill space (ASE) → the all-in generalist tracker (PHC)."** A history of reward-design artisanship being replaced by data and adversarial learning.

#### RSI and early termination — the two staples DeepMimic left behind

The training techniques the DeepMimic paper [^deepmimic] popularized have outlived the method's own name.

- **RSI (Reference State Initialization)**: sample the episode's start state from a **random time point** of the reference motion. A backflip's reward is only knowable upon landing, yet if you always start from a standing pose, you fail tens of thousands of times before ever experiencing a mid-air posture. With RSI, practice also begins from "the correct mid-air pose" — a device that automatically spreads the curriculum around.
- **Early termination**: fall over, and the episode is cut immediately. Data of writhing on the ground after a fall is poison for learning (it dominates the replay while teaching nothing), so cut off the supply at the source.

Our G1 training (LAFAN1 mocap tracking + corridor termination) is a faithful descendant of these two staples.

#### Residual control — "don't leave everything to RL"

One more thing wired directly into this article's setup is **residual control**. Johannink et al.'s Residual Reinforcement Learning for Robot Control [^residual] decomposed control into "a conventional feedback controller + a residual that RL learns." The base controller (or the reference motion) supplies the broad-strokes answer, and RL learns **only the difference from it**. The search space shrinks from "every way of moving the whole body" to "deviations from the reference," and learning stabilizes dramatically. That the G1's walking is a "mocap imitation + residual" setup makes it a direct heir of this lineage.

### 5.7.3 Domain randomization and sim-to-real

Take a skill learned in the simulator to the real machine, and it crumbles under modeling error (friction, latency, motor characteristics...) — the so-called **reality gap**. The current mainstream answer is **domain randomization**: deliberately scatter the simulator's parameters during training and forcibly raise "a policy that works in any world."

| Case | What they did | URL |
|---|---|---|
| Tobin et al. 2017 | Systematized DR for image recognition. A detector trained **only** on randomized simulator images transferred to the real world | [^tobin] |
| OpenAI Dactyl 2018 | Dexterous in-hand manipulation on the Shadow Hand. Massive randomization of physical properties like friction coefficients and appearance; real-robot transfer from simulation training alone | [^dactyl] |
| ANYmal (Hwangbo et al. 2019, Science Robotics) | Fast quadruped locomotion and fall recovery. Sim-trained policies transferred to hardware (combined with the trick of building an actuator model, learned from real data, into the simulator) | [^anymal] |

The intuition is something close to a vaccine. A policy trained in only one environment overfits that environment's quirks. A policy raised with friction, mass, and latency changed every episode can't use "lean on the quirks" as a strategy, so only robust strategies survive. This article's sensor-dropout training belongs to the same family of thought.

### 5.7.4 The academic name for "cheating" — reward hacking / specification gaming

The 11-cheat streak in the main text is not a freak occurrence caused **only** by our clumsy reward design. It's a phenomenon notorious across the whole field, and it has proper academic names.

- **Reward hacking**: Amodei et al.'s Concrete Problems in AI Safety (2016) [^amodei] formalized it as one of five practical problems in AI safety. In that paper's taxonomy it sits on the side of "problems caused by the objective function being wrong."
- **Specification gaming**: the name organized by a DeepMind blog post (2020, first author Victoria Krakovna) [^dm-spec], together with a community-sourced list of **about 60 real examples**. Famous entries from the post:
  - **CoastRunners (boat racing)**: never completes the course; circles a lagoon where items respawn, farming score
  - **Lego stacking**: rewarded for "placing" a red block on top of a green one (= height of the red block's underside), it achieves this by **flipping the red block upside down**
  - **Grasping robot**: in a setup where a human judges success from camera footage, it **hovers its hand between the camera and the object** to look like it's grasping
  - **Simulated walking**: locks its legs together and **slides along the ground** to move forward

That last example looks far too familiar. Our G1's knee-walk shuffle and evis's dive-forward are specimens that belong right beside those "about 60." The important lesson is the perspective in the DeepMind blog's title — specification gaming is "the flip side of AI ingenuity." **The agent is not broken. It faithfully executed, to the letter, the contract we wrote — the reward.** The ability to exploit loopholes and the ability to solve the task are the same ability; what was at fault was our contract drafting.

#### Plain language: the student who optimizes only the score

Reward hacking resembles a student evaluated by "test scores" who perfects nothing but memorizing past exam papers. The student is not lazy — they are **perfectly rational with respect to the stated evaluation criteria**. "I want you to become genuinely educated" existed only inside our heads; what we wrote on paper was "score high on this exam." Reward design in RL is the work of stitching up, one seam at a time, each time you observe an actual cheat, the distance between "what we truly want" and "what we wrote down." The 11 reward-design lessons were, in effect, 11 stitches.

#### Part 2 sources

[^ppo]: Schulman et al., "Proximal Policy Optimization Algorithms," 2017: https://arxiv.org/abs/1707.06347
[^gae]: Schulman et al., "High-Dimensional Continuous Control Using Generalized Advantage Estimation," 2015: https://arxiv.org/abs/1506.02438
[^deepmimic]: Peng et al., "DeepMimic: Example-Guided Deep Reinforcement Learning of Physics-Based Character Skills," 2018 (RSI, early termination): https://arxiv.org/abs/1804.02717
[^amp]: Peng et al., "AMP: Adversarial Motion Priors for Stylized Physics-Based Character Control," 2021: https://arxiv.org/abs/2104.02180
[^ase]: Peng et al., "ASE: Large-Scale Reusable Adversarial Skill Embeddings for Physically Simulated Characters," 2022: https://arxiv.org/abs/2205.01906
[^phc]: Luo et al., "Perpetual Humanoid Control for Real-time Simulated Avatars," 2023: https://arxiv.org/abs/2305.06456
[^residual]: Johannink et al., "Residual Reinforcement Learning for Robot Control," 2018: https://arxiv.org/abs/1812.03201
[^dactyl]: OpenAI et al., "Learning Dexterous In-Hand Manipulation," 2018: https://arxiv.org/abs/1808.00177
[^anymal]: Hwangbo et al., "Learning agile and dynamic motor skills for legged robots," Science Robotics 2019: https://arxiv.org/abs/1901.08652
[^amodei]: Amodei et al., "Concrete Problems in AI Safety," 2016: https://arxiv.org/abs/1606.06565
[^dm-spec]: DeepMind Blog, "Specification gaming: the flip side of AI ingenuity," 2020 (with reference to the ~60-example list): https://deepmind.google/discover/blog/specification-gaming-the-flip-side-of-ai-ingenuity/

# 6. Event 2: Obstacle Run — Pseudo-LiDAR and a 1-D Event Camera

Now that it could walk straight, we scattered cylindrical obstacles across the course. From here on, my day-job blood (image processing) stirs a little. What all that stirring produces is, admittedly, sober geometric computation.

## 6.1 Build the eyes to match the real machine (ideation memo)

To avoid obstacles, you need to "see." In simulation you could hand the policy a god's-eye view (exact coordinates of every obstacle), but that would be a way of raising it that can never go to the real machine. The policy I decided on first here was: "**start by matching the sensors actually mounted on the real G1**."

The real G1's head carries a Livox Mid-360 (a small LiDAR covering 360°, vertical FOV -7° to +52°) and an Intel RealSense D435i (a depth camera with an 87°×58° field of view). So the policy's eyes were likewise restricted to information constructible from that configuration — **the distances along 16 horizontal rays in a forward fan**.

![Pseudo-LiDAR geometry](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_ray_geometry.png)
*Figure: pseudo-LiDAR geometry. 16 rays are cast across the forward 180°, and their intersections with the cylinders are computed analytically. The nearest ray (red) becomes the "fear" signal (drawn to the implemented specification)*

One more policy decision I put in: "**without event-camera-like information as well, the time series is hard to stitch together**." From distance snapshots alone, the policy has to estimate by itself whether an obstacle is approaching or receding. So we added each ray's **temporal difference (the distance change from the previous frame), amplified 20×**, to the observation. This is, in effect, a one-dimensional event camera (DVS). Hand over "approach speed" without solving the point-to-point correspondence problem — a minimal version of the same idea as an event camera emitting only brightness changes.

A technical aside: inside MJX's training loop (the jit-compiled compute graph), MuJoCo's raycast functions can't be called. So, exploiting the fact that the obstacles are cylinders, we **compute the ray-cylinder intersections analytically (by formula)**. This geometric computation is exactly identical to Fullseye's pseudo-LiDAR op described later, and unit tests guarantee that "the world the policy saw" and "the world a human sees during verification" agree numerically.

## 6.2 Mid-training report: the athlete that "slows down out of fear"

At the 47M-step mark, measured over 8 courses: collisions 3/8, falls 4/8, mean forward progress 2.56m. The interesting part: a seed appeared (a random seed; 1 seed = one course's trial run) that **stops in front of an obstacle and survives for 12 seconds**. An athlete partway to learning avoidance apparently first learns "to be afraid." Walking speed also dropped, from the straight event's 0.53m/s equivalent to 0.35m/s. Structurally, it looks just like a human child entering an obstacle course on a bicycle: the first thing they do is slow to a crawl.

> **🍙 Plain-Language Corner (sensor edition)**
> LiDAR is a device that measures distance by "laser echo." It's the light version of a mountain echo: from the time it takes to come back, you learn "the wall is N meters away." An event camera is "a camera that shows only change." Where a normal camera takes 30 photos per second, an event camera sends only the points saying "something just moved right here!" This article's robot receives, as its eyes, an ultra-simplified version of both: "16 laser echoes, plus their changes."

At 63M: falls 0/8 (the walking itself fully stable), collisions 2/8, mean progress up to 3.31m. Direct evidence of avoidance appeared too: on one course, it threaded a narrow gate formed by two obstacles (y=+0.76 and y=−1.19), bulging its body out to y=−0.74, holding closest approach at 0.53–0.60m, and advancing 8.3m over 12 collision-free seconds.

![Learning progress of visual avoidance](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/curve_vision_avoidance.png)
*Figure: obstacle-run learning progress (collision rate and minimum ray distance over time; plotted from measured logs)*

![Obstacle avoidance](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk13c_63M_obst.gif)
*Video: obstacle-course run at the 63M mark (measured in simulation)*

## 6.3 And then the athlete realizes: stand still and you're invincible

Here an unpleasant sign appears. From around 63M onward, this athlete's (walk13c's) average speed keeps dropping; at 68M it posted forward progress of 0.20m/s — while surviving 13.7 seconds. **Don't walk, and you neither fall nor collide.** In a world of only survival reward and collision penalty, "marching in place" is an eminently rational strategy. A hole in the reward design, like a Go AI endlessly passing so it never has to resign.

This is in fact the same shape of problem as the straight event's "saturation zone." That one settled down where the penalty vanishes; this one settles into behavior the penalty never visits. **The agent always finds the coziest hollow in the reward landscape.**

![Freezing and stall termination](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_stall_term_effect.png)
*Figure: forward-speed traces of the freeze local optimum (13c, converging to 0.20m/s) versus the stall-termination group (13d/13e, holding around 0.95m/s) (plotted from measured logs)*

As the countermeasure, we introduced **stall termination**: every 75 control steps (1.5 s), if the root hasn't advanced at least 0.12m, immediate disqualification. A penalty that can't saturate (termination), this time aimed at "not moving forward." Under this new rule, two athletes now run side by side.

- **walk13d**: stall termination only
- **walk13e**: stall termination + 2.5× speed reward

The 8-course measurements at the time of writing (100M steps):

| Athlete | At 63M | At 100M | Trend |
|---|---|---|---|
| walk13d | collisions 8/8, 3.43m/course, collisions/10m = 2.92 | collisions 4/8, 3.07m, **collisions/10m = 1.63** | avoidance improving rapidly |
| walk13e | collisions 5/8, 3.19m, collisions/10m = 1.96 | collisions 6/8, **4.54m**, collisions/10m = 1.65 | distance +42%, holding 1.11m/s |
| (old) walk13c | collisions 2/8, 3.31m, collisions/10m = 0.75 | — (fell into the freeze strategy at 68M; cut off) | its fine record came bundled with the "timid walk" |

13c's superficially admirable collision rate was a number taken at the doorstep of the stand-still strategy, and 13d/13e were still works in progress — and just as I finished writing that, training reached 136M, I re-measured, and the tide had turned completely.

| Athlete | At 100M | **At 136M** |
|---|---|---|
| walk13d | collisions 4/8, 3.07m/seed, collisions/10m 1.63 | collisions 4/8, falls 0/8, 5.12m/seed, **collisions/10m 0.98** |
| walk13e | collisions 6/8, 4.54m/seed, collisions/10m 1.65 | **collisions 2/8, falls 1/8, 7.52m/seed, collisions/10m 0.33** |
| (baseline) 13c@63M | collisions 2/8, 3.31m/seed, collisions/10m 0.75 | — |

**walk13e updated the old champion 13c's collision rate (0.75) to less than half (0.33), while covering 2.3× the distance.** Four of eight courses ran the full 8-second horizon at 9–11m without a collision. The moment "don't stop, avoid, and walk fast" all held at once. Stall termination didn't just plug the freeze cheat — it proved that on the far side of the plug, avoidance ability genuinely grows. What at the 100M mark looked like "a rough phase of charging in fast and hitting things" was simply a stage of development — with the bonus lesson that it pays not to rush judgment from a snapshot.

And then, 150M (150 million steps) complete. Measuring with 8 seeds gave too much noise, so **the final verdict was taken with 16 seeds**.

| Final results (152M, 16 courses) | walk13d | walk13e |
|---|---|---|
| Collisions | 3/16 | 3/16 |
| Falls / course exits | 2/16 | 1/16 |
| 8-second full runs | 8/16 | **11/16** |
| Forward distance | 6.59m/course | **6.67m/course** |
| Collisions/10m | **0.28** | **0.28** |
| Mean speed | **1.08m/s** | 0.97m/s |
| (reference) old champion 13c@63M | collisions/10m 0.75, 3.31m/course | same |

![Avoidance growth curves](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_avoidance_progress.png)
*Figure: the obstacle run's complete growth record (collisions/10m and forward distance, 63M→152M). Dashed line = the old champion 13c's baseline (plotted from the tables of measurements)*

The result is **a tie for the title**. Collision rates perfectly level (0.28 — 1/2.7 of the old champion), distances nearly equal too. Only their personalities remain distinct: 13d is slightly faster, 13e slightly more tenacious.

![Final 16-seed scatter plot](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_final16_scatter.png)
*Figure: all 32 runs of the 152M final verdict (16 seeds × 2 lines). Upper right (farther for longer) is better. Color = outcome (plotted from measurements)*

That the 2.5× speed reward (13e) worked not in the direction of "gets faster" but of "gets harder to stop" was another entertaining miscalculation.

As a podium comment, it reads like this: **the winner was not an individual, but a rule change (stall termination).** In an environment where the freeze cheat is sealed off, either reward design grows to the point where avoidance and walking coexist. The dominant factor was not the fine print of the reward but how the cheat was sealed — that is this event's conclusion.

### 6.3.1 Auditing the referee — re-measuring with a strict contact solver

Just as I finished the final table, the inspection-equipment engineer inside me started making noise. **Isn't the physical contact judgment too lenient? Are we actually using the convergent computation (Newton's method) properly?** I checked, and it hit where it hurts. MuJoCo's default is indeed Newton's method (iteration cap 100, tolerance 1e-8), but **the training side had throttled iterations to 6 for speed, and the referee-side rollouts had measured with the same 6 on the grounds of "matching the training conditions."** Matching conditions is a defensible logic — but it's also a fact that we had never checked whether these were "physically converged numbers." So the final verdict was re-measured under strict settings (Newton's method, 100 iterations, 50 line searches).

| 16-course re-verdict | Loose settings (6 iterations) | **Strict settings (100 iterations)** |
|---|---|---|
| walk13d collisions/10m | 0.28 | **0.17** (distance 7.33m/course) |
| walk13e collisions/10m | 0.28 | **0.37** (distance 6.78m/course) |
| Foot floor penetration (median) | 20.9mm | **20.9mm (unchanged)** |
| Foot floor penetration (worst) | 29mm | 25–43mm |

Two things came out of this. First, **the broad conclusion stands** (both still far below the old champion's 0.75), but the "tie" collapsed — under strict settings 13d is clearly ahead, and I correct the previous section's tie to a coincidence within this measurement's resolution. Second — and this one matters more — **the feet were sinking a median 21mm into the floor**, and that number doesn't budge as the iterations rise. So the main cause of the leniency wasn't solver non-convergence but **the softness of the contact model itself** (MuJoCo's soft-contact parameters set with training speed as the priority). These games were held, so to speak, on a slightly soft mat. You can still rank athletes on a mat, but "would the same results hold on a hard floor?" is recorded as official homework for the next games (hardening the contact would also require retraining the athletes, so rule revisions happen per games).

The audit-the-referee stance is needed most right after a win — a good result is the moment you most want to slack off on inspection.

![Solver audit](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_pen_audit.png)
*Figure: summary of the strict-solver audit. Collision rates flip with the settings, but penetration is invariant to the iteration count = it stems from contact-model softness (plotted from measurements)*

![4-generation race](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_generations_race.gif)
*Video: the champion's growth as a 4-lane race — the same course replayed simultaneously by the 37M/100M/136M/152M generations (each lane derives from a genuine physics rollout; only the lane layout is composited)*

![Blooper reel](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/blooper_reel.gif)
*Video: blooper reel (fall and collision highlights from the 16 final-verdict courses, with slow motion). A sports meet needs its falling athletes too (measured in simulation)*

![The final champion's full run](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk13d_final_obst.gif)
*Video: walk13d after the final verdict (152M, seed6). Runs the obstacle course 10.21m in 8 seconds without a collision (measured in simulation, average 1.28m/s)*

![walk13d 100M](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk13d_100M_obst.gif)
*Video: walk13d (at the 100M mark, seed6). Honestly recorded through the 6.28m advance and right into the collision (measured in simulation)*

![walk13e 100M](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk13e_100M_obst.gif)
*Video: walk13e (at the 100M mark, seed4). 7.04m, including a cut threading between two cylinders (measured in simulation)*


## 6.4 Seen through the real machine's sensor eyes

The pseudo-sensors used for training serve just as well for verifying "how the real machine would have seen it." Here's a video reconstructing the same driving trajectory as a Mid-360-style bird's-eye point cloud and a D435i-style depth image.

![Real-sensor viewpoint](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_real_sensors_walk12c.gif)
*Video: the same run reconstructed as a Mid-360-style bird's-eye point cloud (left) and D435i-style depth (right). Same geometry as the policy's observation (simulation)*

## 6.5 The plan from here: mix the sensors, break them on purpose, switch between them

The obstacle run's observation (rays + temporal differences) is only the entrance to sensor research. Using this G1 as the test bench, I'm planning a five-stage sensor fusion (multi-sensor integration) research program. For each stage I'm writing down "what it's meant to establish" in advance (when results come in, I'll grade the answers in a follow-up — and if a prediction misses, I'll write that it missed).

1. **Pseudo-LiDAR alone (here now)**: the baseline of how far ray observations alone can go. Without a baseline, you can't later measure "the effect of fusion."
2. **Fusion + dropout**: add a forward-only high-resolution ray bundle (depth-camera equivalent), and further train while **randomly killing one sensor family during learning**. The aim is redundancy — "can it keep walking if the LiDAR dies mid-run?" is an ablation experiment (the standard method of deliberately removing a part and measuring the impact) that connects directly to safety. Can we reproduce, from the learning side, the reason real humanoids carry both a LiDAR and a depth camera?
3. **Teacher-student distillation**: transfer behavior from a teacher policy raised on exact ray distances (privileged information) to a student policy that sees only noisy stereo depth. The humanoid version of a method with a track record in quadrupeds (the teacher learns with a god's eyes; the student imitates with real-world eyes).
4. **Temporal integration**: handling "the obstacle I saw a moment ago is now in my blind spot" requires memory. The fork between persisting with per-step re-measurement + temporal differences, or moving on to a recurrent policy (GRU = a recurrent neural network with memory).
5. **Porting to evis**: finally, mount these perception systems on the 700-muscle evis. A muscle-driven body + real-machine-compatible perception — that combination is these games' most distant goal.

Just one implication of this plan. Research on "mixing" sensors is really also research on "**which sensor is safe to let slack off**." Sensors are expensive, power-hungry, and breakable. Working with everything installed is table stakes; whether it can keep working with dignity when something is missing is the practical watershed — exactly the same problem we used to call "redundant-system design" in the inspection-equipment world.

### 6.5.1 Follow-up: grading "break it on purpose" — can it walk with the LiDAR killed?

Plan 2 (fusion + dropout) got its results while this article was being written. The graduation exam of walk14: widen the observation from 132 to 196 dimensions by adding a 32-ray high-resolution bundle across the forward 87° (with the real depth camera's field of view in mind), and train for 152M steps (M = one million steps; not meters of distance), mixing at random per episode the three states "LiDAR only," "depth only," and "both."

The exam: 3 modes × 8 courses. The random seeds are aligned, so obstacle placement and starting pose are perfectly identical across the 3 modes — the only difference is "which sensor gets killed."

| Mode | Collisions | Falls | Full runs | Mean distance | Collisions/10m |
|---|---|---|---|---|---|
| Both alive | 3/8 | 2/8 | 3/8 | 5.40m | 0.69 |
| Depth killed | 4/8 | 1/8 | 2/8 | 4.10m | 1.22 |
| LiDAR killed | 4/8 | 0/8 | 4/8 | 5.24m | 0.95 |

We also made the same-course parallel runs into a single video. The comparison on the course that all 3 modes finished (seed 3):

![3-mode parallel comparison](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/walk14_3mode_compare.gif)
*Video: three parallel runs on the identical obstacle course with the identical starting pose, changing only which sensor is killed (left: both alive 9.78m / middle: depth killed 8.17m / right: LiDAR killed 9.22m; 8-second full runs). Course identity machine-verified by bit-exact obstacle data. Moments where the robot appears to overlap a pillar are camera occlusion; the actual clearance stays at 0.77m or more throughout (measured in simulation)*

The grading has three main points.

First, **the headline question — "can it walk when a sensor dies?" — holds.** In all 24 runs the walking itself never collapsed (zero in-place freezes; with the LiDAR killed, zero falls as well), and the degradation is confined to avoidance scores. It doesn't fall the instant a sensor dies — its grades simply drop. In redundant-system language, "graceful degradation."

Second, an unexpected asymmetry. Killing the LiDAR (the 16 near-panoramic rays) hurt less than killing the depth (the 32 forward rays). Compute the geometry and it makes sense: the forward bundle is spaced at 2.8° per ray, the wide-angle 16 at 11.25° — a 30cm-radius pillar falls between the rays at 3–4m out. What had been doing the work for avoidance was the forward high-resolution bundle, and the policy had learned to depend on it. In effect, we reproduced, from the learning side, the meaning of real humanoids carrying both a LiDAR and a depth camera.

Third, the honest note. "Both alive" at 0.69 is a worse number than the fusion-less champion 13d (0.28). Redundancy training (both sensors present in only 75% of episodes) is not free — it buys robustness by shaving the day job of avoidance — that's this measurement's verdict. That said, 13d's number came from 16 courses on a different harness, so take the face-value comparison with a pinch of salt. The apples-to-apples, same-course same-starting-pose comparison is the 3-mode table above.

![Finishing with the LiDAR killed](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/walk14_dropout.gif)
*Video: the run that killed all 16 LiDAR rays and finished 8.24m on forward depth alone. Closest clearance 0.66m — you can see the avoidance bulging sideways to thread between the pillars (measured in simulation)*

## 6.6 A look at the world's mainstream too — a technology map of ROS 2 and physics simulators

This article's obstacle run is an end-to-end scheme, wiring "observation → policy" straight through one neural net. But the mainstream in industry and research has the **navigation stack** lineage, stacking up separated roles. As a map of where my play sits, here are the main components in a table (URLs verified at the time of writing).

| Domain | Representative | What the component does |
|---|---|---|
| Middleware | [ROS 2](https://docs.ros.org/en/jazzy/) | The common wiring connecting sensing, control, and planning as nodes. The de facto standard for real robots |
| Localization + mapping (SLAM) | [slam_toolbox](https://github.com/SteveMacenski/slam_toolbox) and the LIO family | Estimates "where am I right now" from LiDAR/IMU while building the map |
| Path planning | [Nav2](https://docs.nav2.org/) | ROS 2's navigation stack: turns the map into costmaps and plans a global route + local avoidance |
| Rough-terrain representation | [elevation_mapping](https://github.com/leggedrobotics/elevation_mapping) (ETH) | Keeps a legged robot's footing as an "elevation map." The foundation of step and rough-terrain walking |
| Physics simulators | [MuJoCo](https://mujoco.org/) / [Gazebo](https://gazebosim.org/) / [Isaac Sim](https://developer.nvidia.com/isaac/sim) / [Genesis](https://genesis-embodied-ai.github.io/) | This article's venue is MuJoCo. Gazebo has the deepest ROS 2 integration; Isaac is large-scale parallelism with GPU rendering included; Genesis is the fast newcomer |

The interesting part is that **these two lineages are now converging**. The classical stack — build a map, plan, track — is explainable and certifiable, but weak to assumption mismatches between components. End-to-end RL — see, and move instantly — has strong reflexes, but explains its moves poorly. Recent legged-robot research (rough-terrain parkour and the like) has settled on the hybrid "perception and gait by RL, global route by a planner" as the mainstream, and this article's pseudo-LiDAR policy amounts to a homemade version of that bottom layer (local reflexes). Hooking into the ROS 2 stack (mounting the policy as a Nav2 local planner) is the natural next step when heading for the real machine.
