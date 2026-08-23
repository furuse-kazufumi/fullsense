#### Plain-Language Corner: Mountain Climbing in the Fog

A fitness landscape is the game of "find the highest peak on a mountain where fog limits visibility to 10 m, with nothing but an altimeter to go on." Keep stepping uphill and you will always arrive at some peak — but nothing guarantees it is the highest one. Populations (many climbers), mutation (the occasional huge leap), and diversity maintenance (deliberately scattering the climbers) can all be read as strategies for beating this game.

### 14.6.5 Crossing Paths with Speculative Zoology — From After Man to Xenobots

Evolution simulation has a parallel lineage of enjoyment quite separate from engineering: **speculative evolution**. Its flagship is Dougal Dixon's *After Man* (1981)[^afterman], which earnestly depicted "the fauna 50 million years after human extinction." The game of designing "creatures that could have existed," inside the constraints of science (anatomy, ecology), shares its spirit with Sims's virtual creatures. The difference: the selection Dixon ran in his head, Sims actually ran on a computer.

Today this crossing is starting to take physical form. Cheney et al.'s "Unshackling Evolution" (GECCO 2013)[^cheney] evolved **soft virtual creatures** from voxels (3D pixels — little cubes) of bone, muscle (two kinds contracting in opposite phase), and soft tissue, producing galloping block-shaped creatures and caterpillar-like things. Then Kriegman et al.'s "A scalable pipeline for designing reconfigurable organisms" (PNAS 2020)[^xenobots] took morphologies that an evolutionary algorithm had designed inside a simulator and **actually assembled them from living frog (Xenopus) cells** — the so-called xenobots. From "drawing imaginary creatures" through "evolving them in simulators" to "manufacturing them from living tissue," it is now one continuous road. Our own game with evis — searching for plausible movement in an anatomically correct body — sits at the humble end of that lineage's table.

---

# 15. Exhibition Events — Arm, Air, and Hand (All of It Real Physics)

## 15.0 Track Events: The 100m — A Challenge Letter to the Real Games (Which Is to Say, a Finishing Report)

The Beijing games have a 100m dash, and the first edition's winning time was 21.50 seconds. Our footrace champion (walk12c) has only ever run 20m — more precisely, **its training episodes are cut off at 20 seconds, so it has never once experienced the world beyond that**. There was no guarantee it could stay on its feet for 73 seconds. We tried it anyway.

![The 100m dash](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_100m_dash.gif)
*Video: time-lapse of the 100m (73 seconds of real time → about 5× speed). It covered 3.6 times its 20-second training horizon without a single stumble (measured in simulation)*

**Result: 100m in 73.0 seconds, zero falls.** It kept walking stably for 3.6 times the duration it had ever experienced in training. Once you settle into the "steady state" of a periodic gait, the sheer length of time stops being the enemy — a clean example of generalization (working outside the range seen in training). (Note this is straight-line walking without vision, so the run is deterministic: it clocked 73.0 seconds every single time. No rerolling the dice for a faster time.)

The gap to the real games' 21.50 seconds is 3.4×. They are running (moments with both feet airborne); we are still walking (always at least one foot on the ground), so the next headroom is the "phase transition to running." Swap the reference motion from a walk clip to a run clip and the same pipeline should be able to take the challenge — adding it to the event list for the second games.

The non-walking events have opened as well. The following four are **all physics simulation**: grasping is friction, flying is thrust, sinking the shot is a parabola. Only "what to do" is scripted — "whether it works" is graded by the physics engine.

![Arm event: pick-and-place](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/panda_pick.gif)
*Video: the arm event. A Franka Panda grasps a cube with nothing but finger friction and moves it next door (no adhesive). The 31cm lift is a measured value (measured in simulation)*

![Basketball](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_basket.gif)
*Video: the basketball event. We solved the high-school parabola formula for a release velocity of 5.29m/s, fed it in, and got a first-attempt swish even under contact physics (measured off-center error at the rim plane: 7mm). The arm swing is scripted; the ball's flight and passage through the net are physics (measured in simulation, with slow-motion replay)*

![Air event: PID square flight](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/crazyflie_square.gif)
*Video: the air event. All the Crazyflie was given was 4 corner coordinates — drawing the square is the work of cascaded PID (real closed-loop control). Steady-state error 3.7cm. After 8 rounds of gain tuning (measured in simulation)*

![Three dexterous hands](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_hands.png)
*Figure: the dexterous-hand athletes — Shadow Hand (tendon-driven, 24 degrees of freedom), LEAP Hand, Allegro (simulation render)*

![Hand event: holding](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/leap_ball.gif)
*Video: the hand event. The LEAP Hand closes around a ball and does not let go even with gravity tilted 60°. No adhesive — just friction and finger geometry (measured in simulation)*

## 15.0.1 Soccer (Penalty Kick) and Dance — Chasing Beijing's Program

We are chasing the Beijing games' marquee events too. First, the soccer penalty kick. Stepping up a level from basketball (where the ball was directly given a computed initial velocity), this time **no initial velocity was injected — the kick came entirely from the leg swing and the ball's contact physics**. Foot-tip speed 5.68m/s → ball launch speed 8.85m/s (the knee snap makes the ball outrun the foot — the same speed amplification as real soccer). Result: **goal on the very first attempt** (in-frame passage judged numerically; the ball settled to rest in the net).

![Penalty kick: success](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_penalty_kick.gif)
*Video: the soccer event, penalty kick. The kicking leg's swing is scripted; the ball is pure contact physics (no injected velocity). With slow motion (measured in simulation)*

![Penalty kick: the blooper take](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_penalty_kick_blooper.gif)
*Video: the failure take, in fairness (this one is a shank with the yaw deliberately thrown off). It went in on the first attempt, so we had to go out of our way to film a miss (measured in simulation)*

The dance event opens with the reference. LAFAN1 contains entire dance motion-capture sequences, already retargeted for the G1. From a single-leg leg-lift through torso twists to whirling arms, a rather intense 9 seconds peaking at 15.7rad/s of joint velocity:

![Dance reference](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_dance_preview.gif)
*Video: the dance event's reference (kinematic playback, no physics — also stated inside the GIF). Whether RL can dance this under physics is an event for the next games (simulation)*

The "reference + residual RL" pipeline from walking can head into dance or combat just by swapping the reference file (the combat-clip conversion is already staged). Whether it can dance — or trade blows — under physics, we will try in order, negotiating with the GPU's free slots.

Two small asides. For basketball we had even prepared an "aim-correction loop for misses," but the physics-formula launch went in on attempt one and the loop never got a turn — a live demonstration that the laws of physics do not betray you. Conversely, the drone's PID (the classic controller that cancels error with proportional, integral, and derivative terms) needed 8 rounds of gain tuning — this airframe is a deliberately underpowered configuration with a very small ceiling on turning moment, and the textbook mountain of control design, "how do you tame an underpowered airframe," was waiting for us right on schedule.

## 15.0.2 Jumping Event (Flash Report) — The Backflip Wasn't on the Roster

This event began with a whim: "couldn't it do a backflip or something?" First, the reference hunt — after combing every clip in LAFAN1, no somersault-family motion is included (an honest disappointment to report. Somersaults are a production to motion-capture in the first place, so their scarcity in public datasets stands to reason). There is, however, a continuous-jumping clip (jumps1, 9 seconds), so we are holding this as the jumping event.

![Jumping reference](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_jump_preview.gif)
*Video: the jumping event's reference (kinematic playback, no physics — reference footage of the skeleton simply riding on rails). 9 seconds linking continuous hops into one big jump (LAFAN1 jumps1 retargeted to the G1)*

Training is underway in the same "reference + residual RL" mold as walking and dance. The interim diagnosis at the 22M mark (M = million training steps): **the aerial phase (the moment every foot leaves the ground) has already been reproduced 5 times** (airtime 0.14–0.44 seconds, foot clearance 6–7cm). The first 3 hops land and settle for a full second, but from the 4th hop's landing the error accumulates, the posture sinks, and it falls on the 5th — "it can jump, but landing again and again is hard," a failure mode that could not be more characteristically jumping.

![Jumping: interim diagnosis at 22M](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_jump_22M_diag.gif)
*Video: interim diagnosis at 22M of training (measured in physics simulation). The aerial phase and the first 3 hops' landings hold; things break down from the 4th. Training continues — graduation exam results in a follow-up*

The pre-declared gate is "reproduce the aerial phase + stay stable for 1 second after landing." At 22M the verdict was aerial phase pass, consecutive landings fail (from the 4th hop) — but after running training out to an effective 54M, the scenery changed.

**Graduation exam: passed.** A 20-second deterministic run (no randomness — one take, for keeps) with **zero falls**. 28 aerial phases (airtime 0.14–0.34 seconds), and of the landings with a fully observable 1-second window, all 26 were **stable** — "breaks down on the 4th hop" is now ancient history. Survival time during training has also stretched past the full length of the reference clip (11.2 seconds) into a second lap.

![Jumping RL, the real run](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_jump_rl.gif)
*Video: the trained policy's continuous hops (measured in physics simulation, part of the deterministic run). Aerial phase and settled landing, over and over — from "breaks down on the 4th hop" at 22M to 20 seconds without a fall at 54M (measured)*

One backstage story. The first gate verdict came back as a fail — but the culprit was not the athlete; it was **a bug on the test-equipment side** (the verification run ignored the course-width setting and falsely called "course departure" at a narrower width than regulation). The result above is after fixing and re-judging. Auditing the referee: the work never runs out, whatever the event. The next challenge is the long-jump segment of the same clip (0.4 seconds of airtime, 0.8m of distance).

## 15.0.3 Running Event (Prep Report) — The Line Between Walking and Running Is the Flight Phase

The footrace (20m) finishing time works out to about 4.9km/h — honestly, a brisk walk. Which makes the next itch obvious: "**can it truly run — can it run fast?**" We started the prep.

The boundary between walking and running is not speed but the presence of a **flight phase** (a moment when both feet are off the ground at once). Race walking's rule — "one foot on the ground at all times" — is exactly this in reverse. So the running event's pre-declared gate became: ① a flight phase genuinely exists in the steady cycle in physics simulation, and ② clearly exceed the walking champion's 1.37m/s.

For the reference hunt we measured the speed of all 6 LAFAN1 running-family clips (4 run + 2 sprint) and adopted **sprint1_subject4** (4.04m/s, cadence 3.75 steps/s, stride 2.15m), the fastest one with a straight-line window. The same prep as walking (cycle extraction → loop closure → straightening) turned it into a reference cycle. The reference contains one flight phase per side, with an **airborne ratio of 37.5%** — running, no arguments.

![Running reference](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_run_preview.gif)
*Video: the running event's reference (kinematic playback, no physics). The AIRBORNE overlay marks the flight phase — both feet leave the ground for 37.5% of the cycle (LAFAN1 sprint1_subject4 retargeted to the G1, straightened)*

We measured the hardware's limits up front too. Running exactly per the reference, joint velocities sit at a comfortable 0.4–0.5× of the official Unitree spec limits at the hips and 0.4× at the ankles — but **the left knee runs at 0.88×**, only 12% of margin. A human sprint's knee swing is very nearly a limit-spec motion for this machine. Since training (in simulation) can physically push knee speed beyond the reference, a velocity penalty will be needed with real-hardware transfer in mind — a caveat we are writing down already at the prep stage.

Training (50M; the termination criterion scales walking's 0.12m/1.5s in proportion to speed, giving 0.3m) ran on the GPU slot vacated when evis's walking training finished. The result —

**It ran. And it fell. We'll show you both.**

Graduation exam (deterministic run, no randomness) measurements: **16 flight phases** (both feet airborne, median airtime 120ms, airborne ratio 46–49% of the cycle) — gate ① passed. Average speed **4.15m/s**, **3.0×** the walking champion (1.37m/s) — gate ② passed. "Did it just pad the distance with a dive?" — also checked: excluding the fall segment, speeds per 1-second window hold steady at 4.08–4.19m/s, so this is genuine cruising speed with no padding. Cadence of 4.08 steps/s nearly matches the reference (3.75) — a robot running on physics at the rhythm of a human sprint.

![Running RL, the real run](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_run_rl.gif)
*Video: the trained policy running (measured in physics simulation, the full deterministic run). At the AIRBORNE overlay both feet are fully off the ground. Forward lean, arm swing, knee fold — proper running form for 16.2m — then a forward dive and fall at 3.92 seconds. This is where we currently stand (measured)*

But as an honest report card: **it ran for 3.92 seconds**. Short of the 20-second finish, ending face-first in a dive — "run fast" achieved, "keep running" not; a sprinter who hit the ground instead of the tape. The other caveat is the knee: the RL policy was swinging the right knee to 97% of the real-hardware velocity limit (exactly as predicted at prep — essentially spending the whole 12% margin). A knee-velocity penalty is mandatory before this goes anywhere near a real machine. We queued continued training (+50M) — and the result arrived before this section was even finished.

**"Keep running": also achieved.** The continued training's (106M total equivalent) deterministic run went **20 seconds, no falls** (84m forward). 80 flight phases, 50.7% airborne ratio, average 4.21m/s — endurance grew while the quality of the running held. It also got smarter with its knees: margin against the real-hardware velocity limit went from 3% (last time) to 10% — you would expect faster to mean sloppier, but instead it learned restraint.

![Continued-training cruise](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_run_rl2.gif)
*Video: the cruise segment after continued training (measured in physics simulation, deterministic run, t=8–12 seconds). Stable cruising in running form, flight phases included — last time it had already fallen before this point in the tape (measured)*

And the challenge letter to the real games, round two. A 30-second deterministic run covered 125.8m, **passing 100m at 23.77 seconds**. That is **2.3 seconds — silver-medal range —** behind Beijing's 100m champion (Tiangong Ultra, 21.50 seconds), and a 3.1× cut from walking's 73.0 seconds. Of course, theirs is a real machine with gravity, wear, and an audience; ours lives inside a simulation — read it as an exhibition record on a different playing field. Honest note: this record amounts to a flying start at reference speed (a standing start would add several seconds), so next to official records it carries the "exhibition record" asterisk — even so, we now live in a time when an athlete raised on a single GPU at home can put up numbers in the same ballpark as a national-scale championship's winning time.

## 15.0.4 Stairs Event (Prep Report) — Horizontal Eyes Cannot See Low Stairs

After running, stairs. LAFAN1 has no reference for this, so the plan changes: ① build a staircase in the venue, ② design an observation that "sees" the steps, ③ a curriculum that starts from the flat-ground walking cycle and raises the step height from low to high. Not imitation — this is a terrain-and-vision event.

The venue is already built. Aiming ultimately at the 17cm standard riser of building stairs, three stages: 5cm → 10cm → 17cm:

![Stairs venue](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_stairs_venue.gif)
*Video: the stairs venue (17cm risers × 10 steps) climbed by the G1 in IK poses (kinematic display, no physics, no policy — also stated inside the GIF). The goal of the main event is to reproduce this under physics with RL*

Three key measurements from the prep.

First, **the body reaches**. Climbing a 17cm riser needs joint angles of knee 83.4°, hip 63.0°, ankle 20.5° — all within range of motion (the knee has ample slack against its 165° limit). The "knee can't reach" trap we wept over in the footrace came up clean in the pre-check this time. The static straddle posture — one foot placed a step up — also shows zero violations across all 3 riser heights × 2 placements.

Second, **horizontal eyes cannot see low stairs**. Showing the staircase to the horizontal rays used in the obstacle course (cast forward from pelvis height), a 5cm-riser staircase is hit by 0 of 32 rays — the entire 50cm-tall staircase sits below the pelvis, and every ray sails clean over it. A sensor is not about "whether it is attached" but "where it is pointed" — tilting them down 10° turned every riser height into a strong signal. What we adopted is a 13-point foot-level height scan sweeping 0–1.3m ahead. Why real humanoids carry a separate downward-facing depth camera for their feet — we re-lived the reason from the training side.

Third, an **honest constraint**. The staircase is baked into the scene as a static structure, so riser height cannot be randomized per episode — structurally impossible. So the curriculum raises 3 policies in series, one per riser height (each stage's graduate enrolls in the next). Training waits its turn on the GPU (after running); results in a follow-up.

The stage 1 (5cm risers) results are in. **It can climb 3–5 steps, then loses speed and falls** — that is where we stand:

![Stairs stage 1, the real run](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_stairs_rl_5cm.gif)
*Video: the stage-1 trained policy (measured in physics simulation, deterministic run). It approaches on flat ground with a normal gait and mounts steps 1–3 onto the treads without catching a toe — then loses its rhythm, stalls, and falls while backing down (measured)*

Visual diagnosis shows zero toe-catching (the classic stairs failure); the failures are purely "cannot keep cadence on the steps." And verification produced a fact running opposite to expectation: **zeroing out the foot scan (the 13-point height observation) climbed farther on all 3 seeds** (mean 6.3 steps vs 4.0). The "eyes" we so carefully designed were not merely unused by this policy — it had learned them as actively harmful. Our hypothesis points at the resets: every episode starts on flat ground, so the only time the policy ever experiences "the scan is firing" is right before a stall. To the policy, the scan was most likely conditioned not as "terrain information" but as "an omen of death." If you add an observation, **you must also add experience that starts from states where that observation is alive** — we are implementing the countermeasure (mixing in resets that start on the staircase) and redoing stage 2. Between "attaching" a sensor and "getting it used," there is one more piece of design — tonight's finest teaching material.

And now, grading that countermeasure. Stage 2 (10cm risers, enrolling the 5cm graduate), with half of all resets changed to "start partway up the stairs," ran the same 100M —

![Stairs stage 2, the real run](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_stairs_rl_10cm.gif)
*Video: the stage-2 trained policy (10cm risers, measured in physics simulation, deterministic run). A clean, toe-catch-free climb through step 3. At step 3 it leans back, descends one step "still under control," and ends in stall termination on the flat — no longer a fall (measured)*

**The inverse correlation is gone.** Rerunning the same ablation, this time zeroing out the foot scan made all 3 seeds worse (−1 step reached; survival time halved, every seed crashing). In other words, merely by changing how experience was served, the policy began using the scan — formerly "an omen of death" — as terrain information. With risers twice as tall, survival time still grew 1.5× (2.98→4.50 seconds), and the failure mode shifted from "falling" to "controlled retreat → stall" — turning a crash into a mere deduction is real growth for an athlete.

The one remaining wall: "cannot commit to the next step at steps 3–5." And then the final stage — the graduation exam at 17cm risers (the public-stairs standard).

**17cm was a wall.** The 10-step-course deterministic runs stopped at **step 1 on all 3 seeds**. Swapping in the same 3-step course as the CMU teacher, the best run gets both feet onto the tread of step 3 but collapses backward on the final step up onto the top landing. That one last step will not come.

![The 17cm wall](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_stairs_rl_17cm.gif)
*Video: the assault on the final 17cm stage (measured in physics simulation, deterministic run). Foot placement onto step 1 is precise (no toe-catch) — but with the center of mass left behind, it cannot commit to the push up to step 2 and falls backward. The true face of the wall is right here in the frame (measured)*

The anatomy of the loss is this chapter's biggest harvest. With the checks exhausted, **we can state in numbers everything the missing piece is *not***: joint range is sufficient (per the prep geometry check). Residual budget is left over (saturation rate 0%). The eyes see (foot placement is precise). The only thing missing is **the motion itself that carries the center of mass forward and upward** — and in this approach, built on the flat-ground walking cycle, that motion appears nowhere in the reference.

So the conclusion reads: 5cm and 10cm could be climbed with "flat-ground walking + vision." From 17cm, a **different vocabulary** — "how to climb stairs" — is required. And a teacher for that vocabulary already finished prep in this article's 15.9: CMU motion capture from 40 years ago (16.7cm risers — uncannily, almost identical dimensions) and a knee-95° teacher waveform extracted from a video found on the internet. **The stairs event will return next games with this teacher in tow.** Wall identified, countermeasure loaded — this games' stairs event stops here.

On teacher data, we are also running the parallel thread "couldn't a stairs-climbing teacher be made from side-view video too" (see the follow-up in 15.9 — the side-view fix for the knee ceiling was exactly this groundwork). The public-motion-data survey also hit: the CMU public motion capture database (a storied database running since the 1980s, with exceptionally generous terms — free for any use, embedding in commercial products included) contains stair-climbing clips, and converting one of them (Subject 83) to the G1:

![CMU stairs teacher preview](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_stairclimb_teacher_preview.gif)
*Video: CMU mocap stair climbing (83_32) retargeted to the G1, kinematic playback (no physics, no policy — also stated inside the GIF). The staircase is rebuilt at actual size back-calculated from the clip (16.7cm risers). It climbs 3 steps with alternating legs (measured)*

The fun part: **back-calculating this clip's riser height from the foot-tip height trajectory gives 16.7cm** — landing squarely inside the typical public-stairs range (16–18cm). From a motion filmed nearly 40 years ago, you can read off the dimensions of the staircase at the capture site. Conversion quality is solid too: all 29 G1 joints within range of motion, sagittal-plane reproduction residual 0.4cm, joint velocities within real-hardware limits. The stairs teacher now comes in **two lineages — live-action video (Pexels) and public mocap (CMU)** — lined up for a three-way bout with terrain RL (no teacher, curriculum only) over which school is strongest on stairs.

## 15.1 Dexterity Event (Chopsticks) Qualifier Report — The Story of the Broken Measuring Instrument

![The chopstick twin's dinner table](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_chopstick_twin.png)
*Figure: the dexterity event venue — the torque-twin's forearm and chopsticks, a bean (green), and a plate. The plate appearing to float is by the model's design (simulation render)*

The dexterity event — pinch a bean with chopsticks and carry it — has also opened its qualifiers under the same system as walking (reference trajectory + residual RL + pre-declared gates). On the torque-twin (a twin with the muscles replaced by joint torques), it passed actuation verification (3.8-second hold, 9.5cm chopstick-tip travel), and 1 million steps of training reached "bean lift 48mm" — or so it appeared.

**Video diagnosis revealed that this number was a mirage.**

![Chopstick diagnostic footage](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/chopmimic_1M_diag.gif)
*Video: diagnostic footage of the trained policy (slow-motion at the start). Immediately after start, initialization penetration "launches" the bean upward, and the apex of that parabola was being booked as "48mm of lift." For the following 7.9 seconds, contact force is zero — the chopsticks alone drift forlornly through the air (measured in simulation)*

The diagnosis pinned down two facts. (1) At initialization the bean was embedded 3mm into the chopsticks, and the rebound when the policy moved **launched** the bean straight up at up to 2m/s — the "48mm lift" was the apex of that ballistic arc. (2) More seriously, at the ceiling of reference trajectory + residual, the gap at the chopstick tips can only close to 3.5mm wider than the bean's diameter — meaning **this athlete was, by the rules, incapable of even touching the bean**. The same "action space doesn't reach" trap as the footrace knee (0.5rad cannot reach 40°), back again in a different event.

![Chopstick ejection diagnosis](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_chop_eject.png)
*Figure: the true identity of the "48mm lift." A parabola peaking at 43mm at 0.036 seconds after start (= ejection), zero contact force thereafter (plotted from measured CSV)*

![Chopstick 1M training curves](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_chop_100k_vs_1M.png)
*Figure: train reward (rising) and lift height (flat at 48mm = the ejection apex) for the chopstick RL 1M run. The textbook pattern of "the reward climbs while nothing is actually being grasped" (plotted from measured logs)*

The 1M training verdict was "0/8 successes = abort," but that was **a verdict from a broken instrument**, so we voided it and are re-measuring with the environment fixed (the judging criteria themselves do not move). "Before you celebrate an anomalous number — and before you give up on one — audit its breakdown first." The referee crew's family motto has one more case on file.

**Follow-up — within the very night of the re-measurement, one wall came down.**

Introduced alongside the environment fix is the "oracle feasibility gate." Before running RL, a script (the oracle) that plays the verified grip force and postures exactly by the book is made to attempt the same task — the rule being that **you must not assign RL a task the oracle itself cannot solve**. And on the first post-fix measurement, the oracle failed the 5cm lift. The pinch force is alive and well (1.4–2.5N at 2 points), yet 0.3–0.5 seconds into the lift, only the bean stays behind on the plate.

![The chopstick oracle leaves the bean behind](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/chop_oracle_attempt.gif)
*Video: the oracle's moment of failure — the chopsticks rise, the green bean stays on the plate. Traced with 1ms-resolution contact forces, the "2.4N of grip" turns out to be a downward force pressing the bean into the plate; upward holding force was zero (measured in simulation)*

The root cause, per the 1ms force trace, was over-faith in friction. Lifting a round bean with round chopsticks, the instant the rods slip even slightly on the bean's surface at liftoff, the friction force's downward component devours the normal force's upward component. Raising the friction coefficient does not fix it (physically impossible even at an unrealistic μ=4; it passes only at the knife-edge point μ=1.0, and shifting ±0.1 kills everything) — the answer was in real-world tools: **a slippery bean is held by groove geometry, not friction**. Just like real training chopsticks, we cut a shallow V-groove into the tips (two parallel cylinders, 4.5mm deep) to "box in" the bean with 4-point contact — and the moment we switched to that form closure, even **lowering** friction to a realistic μ=0.3, the full 8-second course passed: 49mm lift, 3.1-second hold, 10cm carry, and return to the plate. It passes across the entire μ 0.2–0.4 band — a plateau, not a knife edge.

![Chopstick oracle success](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/chop_oracle_success.gif)
*Video: the full cycle with the V-grooved chopsticks (shown semi-transparent so the bean stays visible) — grasp, 5cm lift, 10cm carry, hold, return to plate. Counting from the footrace's "knee can't reach," this makes example number 3 of "body and geometry before learning" (measured in simulation)*

With the problem now legitimately posed, the dexterity event's RL has earned its restart. Now that the script can solve it, RL's job changes from "invent grasping from scratch" to "keep this robust under disturbances and residuals." The same lesson the footrace taught with knee range showed up in chopsticks as tip geometry — **before you doubt the learning, measure whether the body can solve the task at all**. This gate is now permanent equipment in every event's qualifiers.

**And the rerun — this time, a genuine 8/8.**

Recalibrating the residual had its own mountain. We suspected the chopstick open-close (hinge) residual width and tried 3 settings — all failed. Probe measurements fingered the real culprit: **the arm-side residual width**. Add a constant offset of a mere +0.02rad (about 1.1°) across the arm joints, and a successfully pinched bean is lost partway through the lift. For a task demanding millimeter precision at the chopstick tips, an arm residual cap of 0.2rad grants 10× the freedom of the breakage boundary. The residual width that paid off so generously in walking becomes a weapon in manipulation — a measured example of the right dose changing with the event.

After calibration (arm 0.02rad, hinge 0.015rad), the 1M run (M = million training steps) held **8/8 successes** from the 50k interim eval all the way to the end. Final marks: 52.8mm lift, 3.2 seconds holding at 45mm — the trained policy slightly outdid the oracle (the script) at 49.0mm and 3.16 seconds.

![Chopstick 1M v2, the real run](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/chopmimic_1M_v2.gif)
*Video: the 1M trained policy's real rollout (semi-transparent chopsticks keep the bean visible). Grasp → ~5cm lift (plate empty) → carry → set down, with the bean in the tip groove the whole way — confirmed by frame-by-frame inspection to be a real grasp this time, not an ejection (measured in simulation)*

One honest note. This environment's initial state restores from a fixed snapshot, so the 8 eval runs are deterministic reruns of identical initial conditions (effectively 1 condition × 8). We cannot yet claim distributional robustness — "can grasp the bean however it happens to lie." The next qualifier, with perturbed bean positions, will be that examination. Even so, an athlete that by the rules "could not even touch the bean" came all the way to beating the script, via two instrument repairs and one geometry discovery. The medal that took the longest of these entire games.

### 15.1.1 Giving the Chopsticks Eyes — Pilot Experiments in Applying Vision

The chopstick event still has a mountain of open problems, but the "eyes" moved ahead. This is the pilot, on the manipulation side, of the second games' theme (vision changes the events).

![Chopstick-tip camera](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/chop_vision_tipcam.gif)
*Video: rewatching the ejection incident from the chopstick-tip camera (slow-motion at the start). What third-person view could not show — "how the bean looked" — is now visible; when the policy gets eyes, this view becomes its observation (measured in simulation)*

![Seeing the bean in binocular stereo](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/chop_vision_stereo.gif)
*Video: stereo vision of the bean through evis's two eyes (64mm interocular). Disparity 51.5 pixels → estimated distance 516.6mm vs true value 517.8mm = **error −0.23%**. Binocular disparity alone yields distance precision sufficient to bring the chopsticks in (measured in simulation)*

![Visual bean detection](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/chop_vision_bean_detect.gif)
*Video: bean detection on the tip-camera feed (green-blob centroid tracking). Detected in 164/241 frames — the misses are segments where the bean left the field of view, which is itself the correct behavior. The parts for "find the bean by vision and bring the chopsticks in" are all present (measured in simulation)*

And the same night the 1M policy's success came in, we re-filmed that successful rollout with the **tip-view camera + bean-detection overlay**. A trailer for "see, aim, pinch":

![The 1M success seen from the chopstick tip](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/chop_1M_tipcam.gif)
*Video: the 1M trained policy's successful episode replayed from the chopstick tip. The amber crosshair is the green-blob detection centroid (detected 81/81 frames). The bean enters view, settles into the groove, the plate recedes below — when the policy gets eyes, this is what its observation will be (measured in simulation)*

The vision parts (distance −0.23%, centroid within 3px agreement) reached passing marks ahead of the event itself. The body side, per the follow-up above, went from oracle pass to a trained policy at 8/8. What remains is connecting the two — find the bean by vision, close in on the estimated distance, pinch with the trained policy. Unifying "see, aim, pinch" is the headline event of the next games.

## 15.9 Side Research: Making Our Own References with Image Processing — The Road from Video to Mocap

This article's references (LAFAN1) are borrowed goods, with a non-commercial license attached. "**If only image processing could produce mocap too**" — "**then we could use it as training material**." We took this direction into a PoC the same night. We happen to own the finest verification environment there is: with evis footage, we know the 3D ground truth of every joint, so **pose-estimation error can be measured with a ruler**.

What we did: render evis's pose transitions to video from a front camera → run a general-purpose human pose estimator (MediaPipe) on it → compare the estimated skeleton against ground truth.

![Mocap from video](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/mocap_from_video.gif)
*Video: a robotic render of bones and muscles, tracked by a human-targeted pose estimator with 100% frame detection (yellow = estimate, cyan = ground truth). Whether it would even be recognized as a person was itself part of the experiment — an unqualified positive (measured)*

![Joint-angle comparison](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/mocap_angle_compare.png)
*Figure: joint angles estimated from video vs ground truth. The elbow, after removing a definitional offset (body surface vs joint center, roughly a constant −15°), is at RMSE 2.5° — one calibration away from teacher-grade. Deep knee flexion tops out at 120° due to front-view monocular depth ambiguity (measured)*

The key results: **2D tracking within 6% of body height (1.6% at the shoulders), elbow joint angle 2.5° after calibration** — homemade references get a "feasible (with work)" verdict. The weaknesses are equally clear: (1) flexion along the viewing direction (a knee seen from a front camera) is fundamentally ambiguous in monocular, and (2) when the legs cross, occlusion (being hidden behind the nearer leg) sends the ankle flying. The fixes are adding a side camera, or switching to a 3D reconstruction stack (monocular video → SMPL-X recovery → general-purpose retargeter); the latter dissolves the joint-definition problem along the way.

Of these, the "side camera" fix got all the way to verification the same night. The trigger was the next idea: "**couldn't stairs-climbing teacher data also be made from video?**" Stair-climbing motion lies almost entirely in the sagittal plane (the plane seen from straight-on side), so filming from the side should make the depth ambiguity unnecessary in the first place — we checked this read with an A/B comparison of the same pose transition with only the camera moved to the true side.

![Side view removes the knee ceiling](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/mocap_sideview_knee.png)
*Figure: identical motion and settings with only the camera moved front → true side. The front view (left) saturates the knee estimate at 120° and cannot follow deep flexion; the side view (right) tracks down to the true 82.5° deep flexion — deep-flexion-range RMSE 66.6° → 15.1° (measured)*

The side view's marks: knee RMSE 11.1° (15.1° in the deep-flexion range, no saturation), 100% detection. In other words, **the core range of stair climbing and squats (80–90° deep knee flexion) looks set to become a teacher waveform from a single sideways phone video**. The honest remaining issues, duly noted: the leg on the far side of the camera degrades behind occlusion (the realistic recipe: teacher = camera-side leg + a phase shift to make it two legs), the hip during deep flexion is still rough (RMSE 28.8°, smoothing assumed), and robustness to real-world clothing and backgrounds is untested — this validation used rendered footage, so next comes the answer check on real stairs video.

That answer check was also finished the same night. Prompted by the observation "surely stair-climbing scenes exist on the internet," we surveyed license-clean material (Pexels — commercial use allowed, no attribution required — had one ideal clip: true side view, full body, no occlusion). Running the pipeline on live action:

![Skeleton tracking on real stairs footage](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/stair_video_track.gif)
*Video: skeleton tracking on real-world stair climbing (source: Pexels video 7866005, filmed by Barbara Olsen — the Pexels License requires no attribution, but we note it with gratitude). Tracking is stable while the person is in frame; the skeleton hugs the body precisely (measured)*

![Stair-climbing teacher waveform](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/stair_teacher_waveform.png)
*Figure: cycle-averaged waveforms of 5 stair-climbing cycles extracted from live action (knee, hip, ankle, with ±spread bands). The knee peak of 95.3±2.7° agrees with literature values (80–100°), and cycle-to-cycle spread is small (measured)*

From live action — clothes, background and all — we extracted a clean periodic waveform with a knee peak of 95.3°±2.7°. The step height can also be back-calculated from the video (riser ≈ 10.6cm from the staircase-shaped clusters of ankle contact heights, consistent with a cross-check from the pelvis-center total rise), so "read both the teacher waveform and the venue dimensions out of a single video" actually runs end to end. Honest note: this person is trotting up the stairs, so the 0.78-second cycle is much faster than normal walking (about 1.4 seconds), and the steps are shallower than standard (16–18cm) — time scaling is a prerequisite before feeding this to the G1. Even so, **"a video lying around on the internet" has become a candidate teacher for the stairs event** — a big move on these games' strategy board. Two more material lines are already staged, including the parallel conversion of the stairs clips from CMU's public motion capture (the storied database with famously loose terms).

If this goes through, the conversation changes register. **A video shot on your own phone becomes, as-is, a teacher for imitation RL.** Film radio calisthenics and load them into evis; record your grandparents' gait as a reference for locomotion research; go commercial without license anxiety. Image processing (my old home turf) becomes these games' choreographer — that is the picture. And the "ground-truth-scored ruler" built in tonight's PoC carries over unchanged as the quality-inspection rig for that pipeline.

# 16. Closing Ceremony and the Next Events

The results of the first Home Humanoid Games, summarized.

| Event | Athlete | Result | One-liner |
|---|---|---|---|
| Footrace 20m | G1 | **Finished** (20.5m, 1.36m/s, lateral RMS 0.14m) | Solved by adding 2 observation dimensions, after 3 straight losses |
| Obstacle course | G1 | **Finished** (winner 13d, strict-solver-judged collisions/10m 0.17) | The bout with the "invincible if you stand still" cheat is the real story |
| 100m (walking) | G1 | **Finished in 73.0 seconds** | A brisk walk at 4.9km/h. Foreshadowing, as it turned out |
| Running (with flight phase) | G1 | **Passed** (4.21m/s, 50.7% airborne ratio, 20-second finish) | 23.77 seconds per 100m (simulation exhibition record) |
| Jumping (continuous hops) | G1 | **Passed** (20 seconds no falls, landings 26/26 stable) | At 22M it was still collapsing on the 4th hop |
| Dexterity (bean with chopsticks) | evis arm | **Passed 8/8** (52.8mm lift, 3.2-second hold) | Via two instrument repairs and the V-groove discovery |
| Stairs | G1 | **5cm and 10cm cleared / 17cm is a wall** (stopped at step 1) | The wall's identity: center-of-mass transfer. Returning next games with a teacher |
| Group routine (4 poses) | evis | **Succeeded** (error 1.4–3.8°) | A 5-episode debugging chronicle that begins with "muscles pull" |
| Balance beam (static standing) | evis | **Not achieved** (hand-tuned 1.2 s / RL 1.8 s vs the 3.6 s standard) | Lost to contact-consistent equilibrium. The next plan is already decided |
| Walking (evis twin) | evis twin | **Gate passed** (median survival 1.77 seconds, 1.49m forward) | The twin of a body that could not stand — walked |

This scoreboard doubles as an interim review of the past several months of research as a whole. It was a games where the lost events, and the bouts with cheating, gave us more to write about than the victories. But I believe that is exactly what reinforcement learning really is. **Reward design is inspection-criteria design; observation design is sensor selection; cheat detection is instrument building** — the habits of suspicion picked up over years of living with inspection equipment turned out, unexpectedly, to be directly useful in these games. I thought I had come to a new world, and found myself doing my old job.

A preview of preparations already in motion for the next games.

- **H1 enters the field**: multi-robot support in the training pipeline was completed while this article was being written (a converter + abstraction of the robot config), and H1's real practice (GPU training) also **began during the writing of this article**. The G1's sensor-fusion build (walk14) ran its 152M to completion mid-writing as well, all the way through grading "can it walk with the LiDAR killed" (results in section 6.5.1).

H1's debut result is in too — **a fall at 2.3 seconds**. In-training evals had reached the 4-second range, but the deterministic real run went 2.3 seconds. That said, this is generation 1 — the G1 equivalent of walk8 (the generation that used the teacher as-is) — with none of the prep that paid off on the G1 (cycle extraction, loop closure, straightening) applied yet. With 13 generations of recipes in hand, we are not pessimistic.

![H1's debut](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/h1_walk1_debut.gif)
*Video: H1's debut (deterministic run after 105M of training). A fall at 2.3 seconds — first-ever debuts are like that. The G1's 13 generations of recipes get ported next (measured in simulation)*

![H1 and walk14, early stages](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_h1_walk14_early.png)
*Figure: the two runs training at time of writing (H1's debut and G1 sensor fusion). Both still in the "early silence" — waiting for the surge past 25M (plotted from measured logs)*
- **Expanding to every model**: the measured inventory of all 67 Menagerie models is complete (every one loads successfully). Quadruped events, arm events, hand events, air events — the roster grows in Appendix B.
- **Dexterity event (carrying a bean with chopsticks)**: the "pinched the bean but drops it on lifting" problem reported in a separate article received a full port of the system established in this article's walking (reference motion + residual RL + pre-declared gates), and the results landed mid-writing — after instrument repairs and the oracle gate (the V-groove discovery), 1M of training reached 8/8 success on lift + carry (the full story is in section 15.1). The grasping events and the walking events have genuinely met on the same toolbox.
- **Obstacle course final verdict**: the 150M full-run judgment of walk13d and 13e. In a follow-up.

## 16.0 Translating Beijing's 51 Events for the Home

Before the closing ceremony, an answer check against the real games' program. Beijing's second edition: 51 events, 1,301 matches (the first had 26 events). Picking the events out of primary reporting and translating them into a "home simulation games" gives this:

| Category | Events | Examples |
|---|---|---|
| **Done in this article** | 7 | 100m (finished in 73.0 seconds) / obstacle course (walk13) / proto-combat (sumo) / dance (up to the reference) / medicine-sorting equivalent (pick-and-place + chopsticks) / industrial-sorting equivalent (bin-pick) / and "fully autonomous" |
| **Doable tonight with existing assets** | 5 | 400m and 1500m (extensions of the 100m) / 2 jumping events (references already converted) / weightlifting (an application of whole-body control) |
| **Future work** | 9 | Relay (the handoff!) / soccer matches / table tennis / tug of war / firefighting rescue, and more |

Two discoveries worth smiling at. First, the real games' centerpiece — the **"fully autonomous" category** (400m, 1500m, and relay with remote operation banned) — is, in a home simulation, **the only thing there ever was**: our athletes never had a remote control to begin with. Environments where the constraint comes first sometimes preview the real games' future. Second, the second edition grew its applied (scenario) events roughly 4× from 6 to 21 and added a brand-new specialist program for dexterous hands (8 precision tasks: tool use, weighing, bottle opening). Our chopstick-strained dexterity event was standing in the dead center of the real games' current. Losing style included.

## 16.1 Event Candidates for the Second Games (Vision Changes the Events)

"What changes once eyes are attached," one line per event. Half of these, in fact, we have done before (without eyes) — the assets lie dormant.

| Candidate event | Groundwork | Limit without eyes | What vision changes |
|---|---|---|---|
| Sumo | Past venue experiments exist | Just pushes without knowing where the opponent is | Watch the opponent's weight shift to time grips and sidesteps |
| Swimming (underwater) | Swim experiments done with evis (assets on hand) | Blind swimming on proprioception alone | Avoiding floating objects, walls, other swimmers; approaching underwater debris |
| Basketball shot | **First-attempt success in chapter 15** (launch velocity from the formula) | Limited to a stationary hoop at known distance | See the hoop, estimate distance → shoot from anywhere |
| Space-debris catch | Free-floating capture experiments done (assets on hand) | "God's-eye" capture fed ground-truth coordinates | Capture out of tracking = the shape of real operations |
| Sea-surface debris recovery | Untouched (water surface + grasping combined) | — | On a surface scrambled by reflections and waves, sensor selection (polarization cameras, at last) is what pays |

The common structure is this: **an athlete without eyes can only ever be "world champion of the script."** If obstacle positions are fixed, memorization wins; move them and it collapses (proven in event 2). Only when vision enters does it become, for the first time, a judge-on-the-spot competition — that is the second games' theme.

Excavated from the warehouse, footage from the "eyeless era," posted here in advance. In the second games, these get eyes.

![Robot sumo](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/robot_sumo.gif)
*Video: robot sumo between two Unitree Go2s (past experiment). After a shoving match, settled by a push-out at the ring's edge (measured in simulation)*

![evis swimming](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/evis_swim.gif)
*Video: evis's torque-driven swimming (150 generations of evolution, past experiment). From upright into a prone posture, then kicking — 0.26m of progress in 5 seconds (measured in simulation)*

![Free-floating catch](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/freefloat_catch.gif)
*Video: the zero-gravity free-floating catch (past experiment, slow-motion opening). While reaching out sends the chassis drifting in recoil, a 4-DoF redundant arm + learned correction captures 24/24 first-seen incoming objects. After the grab, conservation of momentum sets the whole body co-rotating — space physics does not take excuses (measured in simulation)*

And one honest story while we are at it. The space catch actually had another champion that appeared to be at 100% capture — until we tried it on first-seen courses (a holdout) and got 0%. A memorization athlete. The one in the footage above was posted only after reconfirming 24 captures out of 24 first-seen throws. The referee crew's job (chapter 9) stays the same, whatever the event.

In the Beijing venue, someone's free idea is surely taking shape and running this very day. The tools now exist to watch that through a screen and not stop at "how nice" — in the end, that single point may be all this article wanted to say. Inspiration can be imported, translated, and continued at a desk at home. There is still plenty of hope. And if I may be greedy: if this toy-like research were someday to become someone else's "footage from Beijing" and get translated off in yet another direction — that would be the happiest possible ending.

![The article's growth](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_article_media_growth.png)
*Figure: a bonus — the growth log of this article itself (character count and media count). The article was an event too*

The venue lights are still on, and the GPU fans are spinning again tonight. The electricity bill is a problem for another day. See you at the second games.

---

> **Acknowledgments and Credits**
> This game stands on the work of those who publish theirs: the MuJoCo physics engine and its GPU build MJX, the MuJoCo Menagerie robot model collection (each model carries its maker's own license), and the brax training framework (all by Google DeepMind and others). For motion data we used, as non-commercial hobby research, the public dataset in which Unitree Robotics retargeted Ubisoft La Forge's LAFAN1 (CC BY-NC-ND 4.0, non-commercial) for robots. Thanks also to Unitree for the G1/H1 models and public data. Stair motion came from the CMU Graphics Lab Motion Capture Database (mocap.cs.cmu.edu) — The data used in this project was obtained from mocap.cs.cmu.edu. The database was created with funding from NSF EIA-0196217. HALCON is a trademark of MVTec Software GmbH; the op-name correspondences in this article are compatibility guides only. The implementation, measurement, and figure-making in this article were carried out by an AI coding agent (Claude Code); direction, ideation, acceptance, and review were the author's.
>
> **Disclaimer**: this article is a record of personal hobby research and is unrelated to any organization the author belongs to. Vendor specs and market figures are quoted from public information at the time of writing; please check each source for accuracy. Simulation results do not guarantee real-hardware performance (rather, as the text shows, things refuse to go as planned even inside the simulation).

> **Related Articles**
> - Prequel to the walking chapters: [My Homemade Evolutionary Gait Was a "Beautiful Lie"](https://qiita.com/furuse-kazufumi/items/5621780636b374585ede) — the story of a loophole in fall detection, out of which this article's refereeing philosophy was born
> - Dexterity event interim report: pinched the bean with chopsticks, dropped it the moment it lifted (limited-share article)
> - Full development history: [article index](https://qiita.com/furuse-kazufumi)

---

# Appendices — Reference Materials

From here on is the reference section that supports the main text. Use it like an encyclopedia.

## Appendix A: Experiment Chronicle — The Complete Record of 13 Generations of G1 Walking

The G1 walking lineage, digested in the main text, is written out here generation by generation. Every number in every line is measured. (The "57M," "42M," etc. after a generation name is the training step count — the practice volume; 57M means 57 million steps. M = million training steps, unrelated to meters of distance.) Read it as the raw log of "in what order we were fooled by what, and what fixed it."

![Training curves for all generations](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_walk_curves_all.png)
*Figure: training curves (survival steps) across all 16 panels. walk7's panel is blank because it "retired without ever running" (plotted from measured logs)*

### A.1 Prehistory: The Age of Shuffling and Straight Legs (walk2–walk6)

**walk2 (57M steps) — the zero-cost U-turn incident.** A 20-second finish, with clean 0.90 left-right alternating foot contact. But the world-frame trajectory read "+1.4m forward → a 209° turn → arcs away off the course" (the notes at the time said "turned 180° and came back," but re-measuring the trajectory for this article's video, it never even came back: after the turn it wandered 1.8m off toward nowhere in particular. Measurement over memory). The reward had only a penalty on yaw **angular velocity**, so a slow U-turn cost approximately nothing. Evaluation in a body-fixed frame cannot see a U-turn — the first lesson. The countermeasure: an absolute-heading anchor, exp(−4·yaw²).

![walk2 overhead trajectory](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk2_circle.gif)
*Video: walk2 from overhead (straight down). The red dots trace the root. After 1.4m forward it turns 209° and arcs away (measured in simulation)*

**walk4 (42M) — discovery of the straight-leg compass gait.** Going straight (+4.07m) succeeded. But it looked wrong. Prompted by (my) observation that "the knees aren't bending, the thighs aren't lifting," measurement put the knees at −7° to −1° — practically rods. Two culprits. (1) The foot-contact test was loose (contact = ankle-origin height < 0.06m), so even a 3cm shuffle collected the airborne reward in full. (2) Even after adding a foot-clearance reward (a +10cm arc during swing), **swinging the leg from the hip alone like a compass, knees locked, still gets the foot tip to 10.5–11.1cm**. Geometric targets can be satisfied by substitute motions — the first appearance of that lesson. Plus a 3.6m lateral drift over 20 seconds (y position unconstrained).

![walk4 shuffling](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk4_shuffle.gif)
*Video: walk4 side view. Knee range −7 to −1° (essentially locked), 8cm foot lift — the straight-leg compass shuffle (measured in simulation)*

**walk5 (42M) — the action space wasn't reaching.** The knee residual scale was widened 0.5→1.0rad (because a uniform 0.5rad caps knee commands at 29°, **structurally unable to reach** the 40° a swing leg needs). Knee flexion during swing was rewarded against a sine-wave target (0.7rad peak, weight 1.0), and a y-position anchor was added. Forward progress doubled to 8.29m/20s, straight and fast. Yet the knees still stopped at −7° to +16°. The knee metric read 0.43–0.48 — essentially the theoretical average obtainable with straight knees (0.45). In other words, **at weight 1.0 the knee reward could not pry the athlete out of the straight-knee local optimum**.

**walk6 (37M) — apply the weight before the local optimum forms.** Raising the knee reward's weight to 3.0 — that alone — **won the ±40° bent-knee gait**. Local optima form early in training, so adding weight afterward is too late; it has to bite hard from the very start. Still remaining: a habit of drifting left and reversing late in the run, and arms still hanging like rods (a lonely sight).

![walk6 wins its knees](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk6_knee.gif)
*Video: walk6, same framing as walk4. The knees now work through −7 to +41° (measured in simulation)*

**walk7 (retired without ever running) — realizing the limits of handmade rewards.** We stopped right after designing a contralateral arm-swing reward (shoulder pitch ±0.25rad; measured note: "positive shoulder pitch = arm back"). Two generations burned on knees — and now several more on arms? Rewarding style elements one by one and tuning their weights is a road without end. Here we changed course: **use human motion capture as the teacher**. walk7 is the only generation that retired without ever running.

### A.2 The Age of Imitation (walk8–walk12c)

**walk8 (37M) — proof of mocap transfer.** With Unitree's official LAFAN1 retarget as the teacher (30fps, a (T,36) sequence of qpos — the vector of all joint positions — though the quaternions need xyzw→wxyz conversion), we implemented a simplified DeepMimic-style setup. The decisive piece was **residual control**: ctrl = teacher reference + 0.4 × policy output. The teacher's knee 82° and hip −56° are angles the policy's action scale cannot output directly; laying the reference underneath as feedforward is what makes them reachable at all. Result: knees 6–92°, shoulders ±30° — the walking style transferred wholesale. Five generations of handmade rewards, replaced by one teacher. But the teacher clip itself meanders, and a new problem appeared: it trips on the discontinuity when the 10-second loop rewinds.

**walk9 (37M) — idealizing the teacher.** From the teacher clip we extracted exactly one gait cycle (a lag of 30 frames detected by autocorrelation of the left knee angle), picked the start point where the loop closes best, cross-faded 4 frames at the seam, removed the yaw component, and rebuilt the root as straight +x travel at 1.47m/s. Now: 20-second finish, style intact. Except that in world coordinates it was walking in **a large circle** (main text 5.1). All that work — and a circle.

![walk9's great circle](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/g1_walk9_bigcircle.gif)
*Video: walk9 from overhead. Exactly one lap in 21 seconds (+368°), a circle several meters across. Style stays clean at knees 4–81° (measured in simulation)*

**walk10 (saturation death #1).** Tracking the root's absolute xy position with an exp-type soft reward: the moment it fell behind the teacher (1.47m/s) early on, position error hit 4.6m → the reward saturated to zero gradient, and the athlete could learn nothing.

**walk11 (saturation death #2).** Fine — restrict the soft tracking to the lateral direction (the y line) only → drifted 3.0m and saturated. Final record: **exp(−k·d²)-type soft position rewards die of saturation, three in a row, once deviation passes about 1m**.

**walk12/12b (corridor termination).** We gave up pulling it back with rewards: |y − ref_y| > 1.5m now **ends the episode** (a fail-closed design that cannot saturate — when in doubt, disqualify). The cheat died, but exploration shriveled with it: reward plateaued at 450, survival at 8 seconds (main text 5.3). The training curve has a set shape: the first 20M survive a few dozen steps, a surge at 25–35M, judgment point at 37M (reproduced 4 times).

**walk12c (steering observation) — one stroke.** Two dimensions added to the observation: steer = [y − ref_y, yaw]. At 26M the reward is 7× (283/274 → 2,057); at 42M, 6,522; survival 19.5/20 seconds, 20.5m actually walked, lateral RMS 0.14m. The moment it became final that three generations of symptomatic treatment (soft penalties → termination) had been the opening act for the causal treatment (observation). 1000-step finishes (20 seconds); by 68M the position error had simmered down to 0.06–0.09.

### A.3 The Age of Vision (the walk13 line, ongoing)

**walk13/13b — discovery of the freeze local optimum.** The first two runs with obstacles + pseudo-LiDAR converged to around 0.2m/s of forward progress even when run out to 131M/126M. Against rewards for survival and collision avoidance, "don't move" becomes optimal — the pit of main text 6.3. The sheer length of the runs itself became the decisive evidence that this convergence was no accident (two independent lines fell into the same hollow).

**walk13c — the first evidence of avoidance, and the freeze returns.** 47M "slows down out of fear" → 63M "threads the gates, 8.3m collision-free" → 68M "enters the 0.20m/s freeze." That the good score (collisions/10m = 0.75) came bundled with the on-ramp to the freeze strategy becomes visible only by placing 63M and 68M side by side. **A single-snapshot evaluation guarantees nothing about where a strategy is heading.**

**walk13d/13e (training at time of writing) — the stall-termination A/B.** Both received stall termination — under 0.12m in 75 control steps means disqualification — and 13e additionally got a 2.5× velocity reward. From 63M→100M, 13d's collisions/10m halved from 2.92 to 1.63; 13e's forward distance grew +42%. The 150M final verdict in a follow-up.

### A.4 How to Read the Chronicle

Three threads run through all 13 generations.

1. **The evaluation-frame trap** (walk2's U-turn, walk9's circle, 13c's freeze): when the frame the athlete sees differs from the frame the referee scores in, an accident is guaranteed.
2. **The range where the reward gradient is alive** (walk10/11's saturation, walk12's shriveling): design a penalty's effective range before you place it. Outside that range is termination's job.
3. **The right information to the right place** (walk5's action space, walk12c's observation): polish the reward all you like — if the action space cannot reach it, it cannot be performed, and if it is not in the observation, it cannot be controlled.
