---
title: "Standing, Grasping, Drinking, Dancing a Bones-and-Muscles Human on a Home CPU — 700 Muscles, a Mascot Named \"evis\", and the Honest Wins and Losses"
tags:
  - AI
  - MuJoCo
  - MachineLearning
  - EvolutionaryComputation
  - MotionCapture
private: false
project_group: onocollo
related_groups:
  - gaitlab
---

# Standing, Grasping, Drinking, Dancing a Bones-and-Muscles Human on a Home CPU — 700 Muscles, a Mascot Named "evis", and the Honest Wins and Losses

> Who this is for: anyone interested in robotics, biomechanics, evolutionary computation, MuJoCo, or motion capture / anyone curious about "human models that move by muscle" or "driving an anatomical human body at home" / anyone who would rather read the **honest breakdown, and the process of getting stuck and fixing it**, than a highlight reel of good results.
> Prerequisites: if you can read Python, that's enough. I'll unpack the control, biomechanics, and mocap terminology as it comes up.
> Every number was measured on a laptop CPU. This is not a success story; it's a single continuous record in which **one side honestly lost and one side won — both measured on the same yardstick — and whenever I got stuck I fixed it by measuring, not guessing.**

This article is the **definitive edition** that stitches three previously separate installments — "standing, grasping, carrying," "drinking (a bug hunt)," and "turning it into the evis mascot (mocap)" — into one continuous thread ordered by time and causality. It's long, so feel free to jump to whichever chapter interests you.

---

## 0. Three-line summary (the conclusion up front)

- I took a **full-body human model made of bones, tendons, and 700 muscles** (China's LNS Group `MS-Human-700`, ICRA 2024, Apache-2.0), loaded it into MuJoCo on a home CPU, and **evolved each muscle one by one** to make it "stand," "grasp," "carry," and "drink," finally dressing it up as the **mascot "evis"** and having it **dance from mocap and eat with chopsticks**. The crux is driving it not with torque motors but with **muscles that can only pull (contract)**.
- **Standing was an honest loss, grasping was a win, carrying was a partial win (one out of three).** A skeleton that collapses in about one second if you do nothing was, under closed-loop control, delayed to a typical collapse at 2.5 s — but it couldn't stand for 6 s (a loss). On the other hand, an **arm model with a fixed shoulder, its 81-muscle hand, grasped a water bottle on a desk and lifted and held it 0.82 m** (a win). Adding "carry it to the commanded spot" gives partial success (strictly successful on 1 of 3 commands = one third). **Why the wins and losses split by task** is the star of the first half.
- **The second half is two rounds of "fix it by measuring."** A motion I thought was "drinking" was rejected by a single human remark — "it's not going into the mouth" — and chasing it led to a **bug where the bottle slipped through the floor and sank into the ground** (an off-by-one in the keyframe numbering). It was fixed by **inserting a single 0 in the right place**. Then, after naming the skeleton evis and transplanting mocap, this time a stooped-posture bug: **"the hips bend like an old man's."** I stopped guessing and measured the joint angles, and the real culprit was a "mix-up in the marker heights." **Measure before you guess** — that's the recurring bass line.

> An honest caveat up front: standing, grasping, carrying, and drinking (the arm) are **genuine, muscle-driven**, but part of evis's dancing, chopsticks, and drinking gesture mixes in **kinematic replay (directly feeding joint angles — a presentation-layer effect)**. **Which parts are genuine and which are cosmetic** is stated at each point and in the final chapter.

![evis motion reel](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/evis_mocap/reel.gif?v=1)

*↑ Where this article ends up: walk → run → jump → salsa → kick → eat with chopsticks. It's all the same skeleton (evis), driven by transplanting free mocap onto it. Every "loss" and "bug" along the way is recorded below, number by measured number.*

---

## 1. Terms (the map first)

This is a long article, so let me lay out the vocabulary as a map up front. Feel free to skip any row you already know.

| Term | In plain words |
|---|---|
| musculoskeletal model | A human-body simulation that has not just bones and joints but **muscles and tendons** too. Here it's a full body with 700 muscles |
| muscle actuator | A drive whose power source is a "muscle." Unlike a motor, it can **only pull (contract)**, and its force is a nonlinear function set by an activation from 0 to 1 |
| degrees of freedom (DoF) | The number of joint axes that can move independently. The locomotion model has 36, the manipulation model 48, the full body 85 |
| redundant | A state where there are far more muscles than the degrees of freedom you want to move. There are countless "correct muscle combinations," which makes the search hard |
| muscle synergy | A representation that compresses 100 muscles into a small number (K) of "patterns that move together." The human brain is thought to bundle muscles this way too |
| closed-loop control | Control that adjusts the muscles **while watching** the body's state (tilt, velocity, ground contact). Committing without watching is open-loop |
| inverted pendulum | A rod stood on its end. Left alone, it falls over. The essence of standing on two legs is constantly righting one of these |
| CMA-ES (evolution strategy) | An optimization that mutates and selects a population of solutions to improve them. Here it evolves the several hundred to a thousand numbers of the control policy |
| baseline | The pre-training, no-control control condition. The starting point for measuring "how much better training made things" |
| RTF (real-time factor) | How much faster the simulation runs than real time. 13x means the physics of one second is computed in about 0.08 s (strongly dependent on CPU and parallelism) |
| `qpos` | The array that **lines up the positions of all the model's joints in a single row**. The crux of the second half. Add a joint and this ordering shifts |
| keyframe | Initialization data that writes "the posture at the start of the experiment" in the **exact ordering** of `qpos`. The catch is that it's **determined by position (index)** |
| warm-start | Starting training not "from scratch" but from "a policy that already works" |
| motion capture (mocap) | A time series of joint angles that records a person's movement. Here we use free BVH files |
| retargeting | Transferring the movement of one skeleton onto **a different skeleton whose body type and joint structure differ** |
| inverse kinematics (IK) | The calculation that **works joint angles backward** from "I want to put the fingertip here" |
| kinematic replay | Making a picture by setting joint angles directly, without running physics (forces, muscles). It produces only the look of the movement |
| equality constraint | The coupling rule that "this joint is determined as a function of that joint." Knees and shoulders have loads of them (the trap discussed later) |

---

# Part I — Standing, Grasping, and Carrying a 700-Muscle Skeleton on a Home CPU

## 2. Why a "whole-body skeleton," and why I researched first

Before starting anything new, I research it first. That's a habit of mine. Today's subject is **MS-Human-700**—a whole-body musculoskeletal model built by China's LNS Group and presented at **ICRA 2024** (Zuo, He, Shao, Sui, *Self model for embodied intelligence*). It's released under Apache-2.0 and is even included in MuJoCo's official model collection, **Menagerie**. With bones, tendons, and **700 muscles**, it is a whole-body skeleton in the literal sense.

Then I read the paper and, honestly, adjusted my expectations. The paper's central thrust is to "control the high-dimensional 700 muscles through a **hierarchical low-dimensional representation (≈ muscle synergies)** and learn to walk." In other words, the authors themselves are saying that **a naive approach isn't enough to make it move properly**.

> A lesson stated up front: "making a human body stand on its muscles" is a genuine research problem that remains hard even when you throw a GPU cluster and hierarchical reinforcement learning at it. And here I am trying to do it with a laptop CPU and an evolution strategy—so **I factor in the possibility of losing from the very start**. If I lose, I write that I lost—that's the backbone of this series.

What I value isn't the result of "having gotten it to stand" itself. It's **honestly attributing, on the same yardstick, how far it got and where it stopped**—that's what I want to write about today.

## 3. The stage: putting a 700-muscle human body on a home CPU

First I loaded MS-Human-700 into onocollo, my own research runtime (a typed runtime layered on top of MuJoCo). There are three variants.

| Variant | DoF | Muscles | Purpose |
|---|---|---|---|
| Full body (full) | 85 | **700** | Every muscle of the whole body |
| Locomotion | 36 | 100 | Upper body simplified. Used for standing/walking experiments |
| Manipulation | 48 | 81 | Right arm and a **detailed hand** + a water bottle on a table |

A few important facts.

- **Every actuator is a "muscle."** Unlike a robot's motor, which can drive both directions from "+3 N·m to −3 N·m," a muscle **can only exert force in the contracting (pulling) direction**. Its activation is 0–1, and the force is set by a Hill-type nonlinear model that depends on force, length, and velocity. So you have to provide muscles **in pairs**—"a muscle on the right if you want to rotate the joint right, a muscle on the left for left"—and there are more of them than degrees of freedom (i.e., they're redundant).
- **The knee is biomechanically precise.** Rather than a simple hinge, it reproduces the rolling-and-sliding motion of the femur and tibia through several auxiliary joints and constraint equations.
- The pelvis is a "floating base"—not fixed to the ground, free to move with three translational slides and three rotations. In the initial pose it stands upright at a height of 0.95m.
- **Speed**: on a laptop (Intel Core, an Ice Lake–generation mobile CPU), on a **single thread while idle**, this model runs at **an RTF of about 13×** (6 seconds of physics in about 0.46 s, ~6500 steps/s; dt=0.002s). But that's the figure when it has the machine to itself; **when you run 7 cores in parallel for evolution, it drops to ~3–5× per process** (cores competing with one another). Since the RTF shifts this much with CPU model, degree of parallelism, and integrator settings, always read the numbers together with their conditions. Even so, it's fast enough that evolution, which "rolls out thousands of times," runs realistically.

![The initial upright pose of the MS-Human-700 locomotion variant. The red on the legs are the muscles and tendons. It stands with the pelvis at a height of 0.95m](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo/locomotion_init.png?v=1)

## 4. An honest baseline first — and then the existing controller "breaks"

Before building any new control, I always measure the **no-learning baseline**. Nail down the starting point up front, so that later I can be suspicious of any suspiciously good number. Using the walking model (with a floor), I ran 6-second rollouts and defined a fall as "the pelvis dropping below 0.6 m."

| Control | Time to fall | Outcome |
|---|---|---|
| No control (all muscles slack) | **0.50 s** | Collapse |
| All muscles at max contraction | 0.99 s | Collapse |
| Random every step | 1.00 s | Collapse |

**Do nothing, and the human skeleton crumples in about a second.** Clamping every muscle to maximum raises stiffness and buys a sliver of extra life, but it still can't stay upright. This is the starting line for the standing task.

And here is where I **measured the existing tooling breaking** — the most technically interesting finding of this whole effort. onocollo already has a controller that "evolves the control of a Menagerie robot." But it was designed to have each actuator read **the angle of the joint it's responsible for** and act on that. A muscle, however, has no single "joint it's responsible for" (it spans multiple joints through its tendons). The result: **all 100 muscles receive the same (zero) input, and because they share weights, all 100 emit exactly the same activation.**

100 muscles contracting with exactly the same strength at every instant — you can't possibly stand on two legs like that. **I confirmed this degeneration numerically (number of unique activation values = 1).** So the muscle model needs a new representation that "looks at the whole-body state and issues a different command per muscle." The need lined up exactly with what the paper calls a "hierarchical low-dimensional representation."

## 5. The standing task: muscle synergies × evolution — and falling over, honestly

Here's the control I built.

1. **Read whole-body proprioception (self-sensing):** the pelvis-height error, its tilt (pitch/roll/yaw) and their angular velocities, the pelvis translational velocity, and left/right foot contact — 14 quantities that matter for balance.
2. **Map to muscle synergies:** linearly map that state into **K "move-together patterns"** (`tanh`), then expand it through a `K×100` matrix into 100 muscle activations (`sigmoid` to squash into 0–1). At K=6 the policy has about 790 numbers. This is my own implementation of what the paper calls the "low-dimensional representation."
3. **Evolve with CMA-ES:** optimize those numbers with an evolution strategy. The reward: "while standing, score higher the closer the height is to target, the more upright the torso, and the smaller the pelvis velocity; terminate on a fall."

> An honest design correction: my first reward only awarded "closeness of height to target." Evolution promptly got sneaky and racked up points with a **policy that "falls slowly and gracefully"** (the height stays reasonably high on the way down, after all). It doesn't look like standing. So I added a **penalty on pelvis velocity**, fixing things so that "coming to a quiet standstill" scores higher than "falling slowly." A tuning of the yardstick to foreclose the cheating.

To spend compute without waste, I also wrote machinery that **loads the model just once and evaluates in parallel across 7 cores** (loading the model takes about 2 s and a single rollout is a few hundred milliseconds, so reloading every time would let loading dominate). By having each worker load once and reuse it, you get a speedup proportional to the degree of parallelism.

The result — **candidly, it fell short.** Reporting only the best value would "present a spike as if it were representative," so I also list the typical value (the median of the late-generation bests). First, the results for a **single random seed** were:

| Control (single seed) | Policy numbers | Typical (median) | Best | Outcome |
|---|---|---|---|---|
| Baseline (no control) | 0 | — | 0.5–1.0 s | Collapse |
| Static muscle tone (constant) | 100 | ~2 s | 3.02 s | Falls in the end |
| Muscle synergy (closed-loop) | 790–1020 | ~2.5 s | 3.71 s | Falls in the end |
| Muscle synergy + memory (integral term) | 808 | ~3.0 s | 4.53 s | Falls in the end |

Looking at this table, for a moment I thought: "**Adding memory (the integral term) stretched it from 3.71 to 4.53 s. Just as hypothesized, balance needs the integral of the error.**" Since that's textbook for balance control (integral control), it made for a clean story, too.

### Nearly fooled by n=1 — the difference vanished once I ran three seeds

But CMA-ES is stochastic. **A single-seed difference might just be a lucky or unlucky seed.** So I ran "memory on / off" for **three seeds each** and took the medians (a fair comparison).

| Control | Median of best (3 seeds) | Spread of best | Median of typical (median-late) |
|---|---|---|---|
| No memory (plain) | **3.55 s** | 3.16–3.80 s | **2.71 s** |
| With memory (integral term) | **3.56 s** | 3.34–4.17 s | **2.39 s** |

**The conclusion reversed.** The median of the best is 3.55 ≈ 3.56 — **essentially the same** — and on the typical value, memory-on is if anything **lower** (2.39 < 2.71). In other words, the 4.53 s I saw with a single seed was **just a high spike from the same distribution**, and is **no evidence that the memory term did anything**. My clean hypothesis that "memory helps" was **not supported** at n=3.

- The closed-loop control delayed the collapse from **about 1 s to a typical 2.5 s and a best of around 3.5 s.** It clearly beats the baseline, and closed-loop beats static muscle tone. For the denominator of the multiplier I conservatively take "no control ~1.0 s" (using the 0.50 s of all-muscles-slack as the denominator would double the number, but that would be exaggeration). **Within this range, the presence or absence of memory makes no significant difference.**
- But **it cannot keep standing for 6 seconds.** Even the best policy is lying on the floor by the final frame.
- **Lesson:** an n=1 "it worked!" is often a lie under stochastic optimization. The cleaner the hypothesis, the less you should believe it until you've taken a median across multiple seeds. This case is a concrete example of my practice of running a **separate-process fact-check** before publishing actually paying off (the fact-check flagged "the single-seed causal claim is too strong" → I verified with 3 seeds → it reversed).

![Learning curves. The time standing rises with generations but plateaus at 2–2.7 s (spiking to 3.7–4.5 s). The dotted line is the ~1 s of no control. It never reaches 6 s (the episode length).](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo/learning_curves.png?v=1)

![Even the best standing policy ends up on the floor like this after about 3.7 s. I leave the "loss" in without exaggeration.](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo/stand_warm.gif?v=1)

Why does it fall short? Put plainly, **optimizing a linear synergy policy with ~800 dimensions via CMA-ES simply isn't powerful enough for the persistent stabilization of an inverted pendulum** (adding a simple integral memory didn't rescue it either, as we saw above). This is consistent with the paper needing hierarchical reinforcement learning. It would be easy to round this off and write "I got it to stand!" here — but since it doesn't actually keep standing, I'll refrain from writing that.

## 6. The Grasping Task: Change the Stage, and We Could Win

Standing is hard because it's an inverted pendulum. So what about a task with **no risk of falling over**? The manipulation variant is fixed from the shoulders up and has no free pelvis joint. In other words, **there's no way to lose your balance**. It becomes a pure "do something with the arm and hand" task.

So we had **a right hand built from 81 muscles grasp a water bottle on a table and lift it**. The hand starts out about 0.1 m from the bottle, so the real task isn't "reaching" — it's **grasping, lifting, and holding**.

We evolved the same muscle-synergy policy, this time with "the higher you lift the bottle, the more points." The results:

| Generation | Bottle lift height |
|---|---|
| 0 (initial) | 0.006 m (≈ zero) |
| 20 | 0.39 m |
| 50 (converged) | **0.825 m** |

**The 81-muscle right hand grasped the water bottle on the table, lifted it 0.82 m, and held it still** (which corresponds to the stage before the drinking motion — up to just short of "bringing it to the mouth").

![The manipulation full-body muscle model grasps the water bottle on the table, lifts it overhead, and holds it. This is a "hold" that keeps the distance between palm and bottle constant, not a toss](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo/grasp_final.gif?v=1)

### Honestly Questioning "Tossing" and "Scooping"

A reward that maximizes height **also pays out for the cheat of "batting the bottle upward."** So we verified in two stages.

**(1) Is it a toss?** For the 3 seconds after lifting, the distance between the palm (the central carpal bone) and the bottle center **stayed at 0.052–0.062 m** (it didn't diverge). If it were a toss, the distance would diverge. They're moving together.

**(2) Is it really "gripping with the fingers" (not a scoop)?** A constant distance only shows they "moved together." To rule out the possibility of pinning the bottle against the forearm and carrying it (a scoop), we examined the **contact forces** during the hold. The bottle is touched by **nine finger and hand bones** — the thumb (40 N at the distal segment), the index finger (33 N at the metacarpal), the middle finger, and the ring finger — with **the thumb opposing the other fingers (thumb opposition) to grip.** The bottle weighs 5.3 N, so it's being pinched with an opposing force that far exceeds that. This isn't a scoop; it's **a genuine grasp with the fingers closed (force-closure).**

> Honest disclosure: this grasp holds up under contact with a **friction coefficient of μ=1.0** (fairly high friction, close to rubber). The higher the friction, the easier grasping becomes. Lower μ and there's a real chance the same policy would let it slip away — I want to be explicit that "we could grasp it" is a statement about *this* friction condition.

This is also **a genuine, anatomical-hand answer** to a piece of unfinished business left over from an earlier article, where I wrote about "having an AI prosthetic hand hold chopsticks" — the problem that "there was no hand (the chopsticks were being moved directly)." A hand complete down to the thumb, lumbricals, and interossei grasped an object using muscle force alone.

## 7. Beyond Grasping: Carrying to a Commanded Location (Controllable Manipulation)

"Grasp and lift" was, in truth, a one-directional task of "upward, anywhere is fine." Real manipulation means **carrying the grasped object to a location we command.** So we showed the policy the "target − bottle" vector (adding 3 dimensions to the observation) and tested whether **a single control** could follow **three different targets** (straight up / a drinking pose at the side of the body / slightly up and forward). If one policy can change where it carries the object on command, then it's "controllable."

But doing it naively fell into **reward hacking yet again.** With only "the closer the bottle is to the target, the more points," **the gradient toward grasping vanishes.** Because the bottle's initial position already banks the floor value of the closest-approach term, the optimizer scored points by "relaxing the muscles and leaving the bottle sitting on the table" — by not moving. Even after running 200 generations, the closest-approach distance to the target never improved and stayed frozen — **the score climbs, yet nothing is grasped or carried.** It's a sibling of the "fall over slowly" deception from §5.

There were two fixes:

- **Warm-start:** use the verified grasping policy from §6 as the initial value. The observation dimensions differ (grasp 19 → carry 22), so we filled the input weights for the added command vector with zero, making it **initially identical to the grasping policy.** That way evolution's job becomes "add only command-following on top of a grasp that already moves," and it clears the "leave it alone" basin from the start.
- **Grasp-maintenance reward + terminal gate:** reward the closeness of the hand and bottle, and make the terminal bonus **valid only while still holding** (dropping or tossing it scores 0).

As a result, the score jumped from the floor value of the leave-it-alone hack (about 18.9) to **about 1021**, and the substance became genuine too:

| Commanded target | Closest approach | Kept grasping? | Placed at target? (within 12 cm) |
|---|---|---|---|
| Straight up +0.30 m | **0.103 m** | ✓ | **✓** (final 0.108 m) |
| At the side, drinking pose | 0.265 m | ✓ | ✗ |
| Slightly up and forward | 0.120 m | ✓ | Borderline |

**It kept grasping the bottle for all three commands** (palm–bottle 0.043–0.046 m) and carried it in the commanded direction. Straight up succeeded all the way to placing it; slightly up and forward was borderline. The **honest limit** was the "drinking pose at the side," which fell short at 0.27 m — **a single linear synergy** warm-started from the straight-up grasp doesn't have the capacity for the posture of pulling the arm back to the body's side. **The grasp is complete; command-following succeeds strictly in one out of three.** Without exaggeration, I'll place it as a partial "controllable manipulation."

![The full-body skeleton's right hand keeps grasping the water bottle and carries it to the commanded "straight up" target and holds it. This isn't a toss; it carries while still gripping](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo/place_carry.gif?v=1)

And the most interesting application of this carrying is "**bringing it to the mouth**" — that is, the eating and drinking motion. When we switch the commanded target to "at the side, at the mouth," the musculoskeletal hand tries to pull the grasped bottle toward the body (the GIF below). But — this is precisely **the hardest target that stopped 0.27 m short in the table above**, and at this point it still didn't reach the mouth.

![When the same policy is commanded "to the side, to the mouth," the seed of a "drinking/eating motion" pulling the grasped bottle toward the mouth. At this point it stops 0.27 m short and doesn't yet fully reach the mouth](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo/musculo_drink.gif?v=1)

At this point I nearly concluded that "the reason it can't reach is the capacity shortfall of a single linear synergy." — But **that was wrong.** The next Part II is the story of measuring that error and exposing it.

## 8. Why Did One Lose and the Other Win?

The same model, the same control representation, the same optimization — yet standing lost and grasping won. I believe **the decisive difference is the physical stability of the task.**

- **Standing is unstable equilibrium.** In an inverted pendulum, the slightest tilt grows exponentially. The controller has to keep righting itself "constantly, quickly, and correctly," and the smallest mistake makes it diverge and fall. That's too heavy a load for a memoryless linear policy.
- **Grasping is (in this setup) stable.** The shoulder is fixed, and the target (lift it high) is easy to maintain once reached. Some coarseness in the control isn't fatal.

That said, it wouldn't be honest to declare stability the **only** difference. There are at least three confounds: **① reaching is already solved** (in grasping, the hand starts out just 0.1 m from the bottle), **② the reward is straightforward** (grasping has a monotonic, dense "higher is better" reward / standing was survival-time-based and produced the "fall over slowly" deception), and **③ the difference in degrees of freedom** (grasping has a fixed shoulder and lacks the unstable 6-DoF floating base that kills standing). **The main cause is stability, but these are in play too** — a story that's too clean makes a single cause look bigger than it is.

And the carrying (place) task in §7 is **the third data point** for this reading. The stage is the same stable manipulation variant as grasping (it doesn't fall over), yet the moment we added the controllability demand of "carry it to the commanded location," it dropped from a complete win (grasping) to a **partial win (one out of three).** Difficulty rises not only with the task's stability but also with the "cleverness" of the control it demands.

The takeaway can be summed up like this: **what an AI can and can't do is decided not just by the cleverness of the policy, but by the stability of the task itself (along with the footing, the reward, the degrees of freedom, and the controllability demanded).** With the same tools, choose your arena and you can win; don't, and you honestly fall. And across all three tasks, **we crushed — with a single check before publishing — the deception of "the score climbs but the substance doesn't follow" (falling over slowly / leaving the bottle alone)** — that's the consistent discipline of this article.

---

# Part II — Drinking: From the Remark "It's Not Reaching the Mouth" to Chasing a Bottle That Fell Through the Floor

> In Part I, §7, I wrote that the drinking motion "stopped 0.27m short — a capacity limit." From here on is the process of measuring, realizing **that conclusion was wrong**, and fixing it. The star of this article isn't "it drank," but **the humble bug just short of that — one that everyone who touches MuJoCo steps on at least once**.

## 9. The Trigger: The Remark "It's Not Reaching the Mouth"

After Part I, I judged that once I repositioned the target point at the "actual mouth," it **reached the mouth with the same control capacity**. Numerically it did reach (the distance between the bottle's center and the target point was a few centimeters). I started to write "the drinking motion worked."

But the human who watched the rendered video (the one who directs me) came back with **three rejections**.

1. **"It's not reaching the mouth"** — the bottle stops around the throat and collarbone, never reaching the actual jaw.
2. **"The mouth isn't even open"** — the mouth stays shut in the first place. It doesn't look like drinking.
3. **"I can't tell what it's doing"** — with a single front camera, the arm's motion is unreadable.

This was the moment the practice this series has always upheld — **"when a result comes out abnormally good, question the breakdown before you let yourself feel you've won"** — was triggered by someone else's eyes. I **trusted the number** — "the distance is a few centimeters" — **and didn't doubt the picture**. The human looked at the picture and saw through the number's lie. I'll start, honestly, by withdrawing the claim.

## 10. First Correction: The Target Was at "Throat" Height

Start with (1). The target point I had set as the "mouth" was `(0.07, 0, 1.46)`. But when I measured the actual jaw geometry, the bottom of the lower jaw sits at height **1.50m** and the lips are around **1.55m**. My target `1.46` was **below the bottom of the jaw — that is, at throat and collarbone height**.

The bottle was carried to the "base of the throat," not the "mouth," and stopped there. The distance number was small because it had properly reached the *wrong* target — **if the target is placed wrong, the higher the achievement rate, the worse the quality**. I corrected the target to the actual lip height, `(0.05, 0, 1.55)`.

This is also a correction to myself — to the explanation I wrote in Part I, §7: "a single linear synergy lacks the capacity to pull the arm back toward the body (so it can't reach)." **The real cause of not reaching wasn't capacity — it was placing the target wrong.** Blaming capacity is always the easiest escape hatch. But to avoid any misunderstanding: what gets overturned here is only the misattribution that "the cause of not reaching the mouth is capacity"; the capacity limit of a single linear synergy itself — the one we saw in §7, that "the precision of placing exactly at any arbitrary single point is one-third" — is still alive.

> Lesson, spoiled early: before you conclude "it's the algorithm's limit," **doubt whether your scoring sheet (target, reward) is correct**. Attributing a plateau to capability is, more often than not, premature.

## 11. But This Model Has No Mouth

Next, (2) "the mouth isn't open." This wasn't a mistake in my setup — it was a **limit of the model itself**. The manipulation variant, in exchange for building the arm and hand with utter precision, treats the **head as a single rigid body**. There's no jaw joint and no facial muscles. All 81 muscles belong to the arm, hand, and trunk — there's **not a single means to open the mouth**.

The instruction was clear: "**modify it into a model whose jaw opens**." So I copied the entire original model (a 251MB bundle of assets) and left it untouched, editing only the manipulation variant's torso definition file to carve the head's jaw geometry out as an **independent child body `mandible` (lower jaw) plus a hinge joint `jaw_open`**. Give this joint an angle and the lower jaw drops, opening the mouth.

But there's an **honest line drawn here from the start**. **This jaw has no muscles attached.** So opening and closing the jaw isn't a motion solved by muscles — it's a **script that writes the position directly (kinematic)**. **The arm's grasping and carrying are genuinely solved by 81 muscles, but the mouth opening is cosmetic** — I carry this distinction all the way to the end.

The modified model loaded fine. With one joint added, the degrees of freedom went 48 → 49. Since the muscle count (81) is unchanged, **the learned control should have loaded as-is**. I checked the jaw-closed and jaw-open frames individually, and the open-close itself worked. — But the moment I loaded the learned drinking control onto it, things went strange.

## 12. The Bug: Add a Jaw, and the Bottle Fell Through the Floor

On the modified jaw model, I replayed the control that had learned grasping and carrying (the champion from §7). The expectation: "grasp and carry to the mouth just like the original." What actually happened was this.

![The bug: replaying the learned control on a model with nothing but a jaw added, the arm rises to the mouth as if to drink, yet there's nothing in the hand. The bottle has fallen through the floor and vanished](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo_drink/drink_jaw_broken.gif?v=1)

The musculoskeletal model raises its arm to the mouth as if to drink. **But the hand is empty, and the bottle on the stand has vanished too.** The control tries to grasp the place where the bottle should be, and since there's nothing there, the arm swipes through empty air and diverges. Adding just one jaw completely broke the grasp — even though I touched nothing, not the muscle count, not the arm joints.

## 13. Hunting the Culprit: Drop the Guess, Measure First

At times like this, **deciding the cause by guessing and slapping on a patch** is the most dangerous thing. At first I had a hunch: "since I added one joint, the arm joints' initial angles must have shifted, and it must be starting from a weird posture." Plausible. But this series' discipline is: "**rather than 'X is probably the cause,' say 'I'll confirm X; the way to confirm is Y.'**"

So I wrote a diagnostic that **measures the immediately-post-start state of the original model and the jaw model side by side**. Across both models it compares the angles of the arm's seven main joints, the palm's world coordinates, and the bottle's world coordinates. Here's the result.

| Quantity measured | Original model | Jaw model | Difference |
|---|---|---|---|
| Angles of the 7 arm reach joints | (reference) | (same) | **max 0.0** |
| Palm world coordinates | (reference) | (same) | **0.0** |
| **Bottle height z** | **0.94 m** | **−0.63 m** | **−1.57 m** |
| Hand-to-bottle distance | 0.108 m | 1.667 m | — |

My guess was **wrong**. Both the arm joints and the hand position **match the original exactly** (the initial posture wasn't broken). The only thing broken was **the bottle** — the bottle, which should sit on the desk at z=0.94m, was starting from **z=−0.63m, that is, underground, having punched through the floor**. The hand is in the correct initial posture. Only its grasping target, the bottle, has dropped below the ground. So the arm correctly moves to "where the bottle on the desk should be," yet there's nothing there. **This is the true identity of the whiff.**

> Had I convinced myself here that "the arm must have shifted" and started fiddling with the code, I wouldn't just have failed to fix it — I'd have broken the arm control that was already correct. **Measuring prevents the wrong repair.**
## 14. The real culprit: a keyframe is decided by "slot number." Add a joint, and everything shifts

Why did only the bottle drop, and by a full 1.57 m at that? This is the lesson that applies to everyone who touches MuJoCo (and physics engines in general).

MuJoCo **packs the positions of every joint in the model into a single array, `qpos`**. Each joint is assigned a **place (a slot)** — "from index N to index M" in `qpos` — in the order of the body's tree structure. And the **keyframe**, which defines "the pose at the start of the experiment," is nothing more than a sequence of numbers written out **as the raw ordering of that `qpos`** — like `qpos="-0.07 0.03 ... 0.94 ..."`. **The i-th value goes into the i-th slot.** It's decided by position.

Now, I added the jaw hinge `jaw_open` to the head. MuJoCo assigned it **slot 42**. And as a result — **every joint from slot 42 onward shifts back by one**. The slot that holds the bottle's position moved too, from 42 to 43. But **the keyframe's number sequence was still 48 entries long**, still dragging along the original model's ordering (I'd added the jaw but hadn't updated the start-pose number sequence). The model's `qpos` had grown to 49 entries, yet the keyframe was 48. MuJoCo pads the missing entry with a 0 at the tail. The result: **everything from slot 42 onward was read shifted by one**.

In a diagram, it looks like this.

```
Slot number:   ... 41    42(new)   43       44       45      46      47      48
Intended:      ... arm   [jaw=0]   bottle-x bottle-y bottle-z rot…    rot…    rot…
keyframe real: ... arm    0        0        0        -1.57   0.32    0       0(padding)
                          ↑ from here on, every value is read one slot early
```

The arm (slots 41 and earlier) was unharmed — **because the shift began at slot 42**. But the bottle was another matter. Here I need to insert one important premise: **this bottle rides on a "vertical slide joint whose origin is the desk height (0.94 m)," and the value that goes into the keyframe represents the relative displacement (in meters) from that origin.** The bottle's vertical slide should have been 0 (i.e., sitting right on the desk).

But because of the one-slot shift, into that height field flowed **the value `-1.57`, which was originally the rotation angle of the neighboring joint**. −1.57 was meant to be a **rotation angle measured in radians (about −90 degrees)**. That number **was read straight as a vertical-slide displacement (−1.57 meters)** — a number that was an angle mutated into a number that was a distance. So the bottle sank 1.57 m below the desk height and appeared **at 0.94 − 1.57 ≈ −0.63 m, buried underground through the floor**.

The reason "0.94 − 1.57 = −0.63" is an addition (of a relative displacement) rather than a subtraction is that the bottle's height is **a slide amount from the desk, not an absolute coordinate** — skip this point and you'll be left suspicious: "shouldn't z have been overwritten entirely to −1.57? Isn't this match too neat?" In fact, a separate process that verified the breakdown of this article almost ruled it "inconsistent" at one point, until it confirmed the model definition (that the bottle rides on a vertical slide joint) against the primary source. **The neater the numbers line up, the more you trace back to the mechanism to confirm** — that's the very creed of this series.

**Adding a single joint means shifting every keyframe slot by one**, and yet I had left the number sequence in its old state. The green tests were passing (the model loads, and the joint count and muscle count are correct). **It's a quiet bug — a positional shift that tests can't detect.** And what exposed it was not a test but — **one line from a human who watched the video: "it's not going into the mouth."**

## 15. The fix: one 0, in the right place

Once you know the cause, the fix is almost anticlimactically simple. **Into the original 48-entry keyframe, insert one `0` (the jaw is closed = angle 0) at the jaw's slot (number 42), making it 49 entries.** Then everything from slot 42 onward shifts correctly into its intended slot, and the bottle returns to the top of the desk.

```
Before (48 entries): ... 0.3141  0 0 0  -1.57 0.32 0
After  (49 entries): ... 0.3141  0 0 0 0  -1.57 0.32 0
                              ↑ one 0 for the jaw inserted
```

Apply it and re-measure, and the jaw model **matched the original model down to the numbers**.

| Quantity measured | Original model | Jaw model (after fix) |
|---|---|---|
| Bottle start z | 0.94 m | **0.94 m** |
| Lift amount | +0.62 m (to z=1.56) | **+0.62 m (to z=1.56)** |
| Kept its grip? (hand–bottle) | ✓ (0.043 m) | **✓ (0.043 m)** |
| Final distance to mouth (lips) | 0.050 m | **0.048 m** |

The difference in the hand–bottle relative position vector was **0.0 (matching to within a measurement precision below 1e-6)** — in other words, the jaw model reproduced motion **indistinguishable** from the original model with respect to grasping and carrying. No retraining was needed at all. What had broken was not the control but the ordering of the initialization data.

## 16. It drank

With the repair done, we finally get the picture I'd wanted all along. The hand reaches for the bottle on the stand, grasps it, carries it to the mouth, and there the jaw opens.

![After the fix: the musculoskeletal right hand grasps the water bottle on the desk, lifts it 0.62 m, carries it to the lips, and the mouth opens. 81 muscles drive the arm in a closed loop (only the jaw open-close is scripted)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo_drink/drink_jaw2.gif?v=1)

"Is the mouth open" was also hard to see, hidden behind the arm and the bottle, so I cropped out just the head and placed the start and end side by side.

![Head comparison. Left = at the start the mouth is closed. Right = at the end the lower jaw is clearly lowered, the mouth is open, and the bottle is at the lips](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/musculo_drink/jaw_open_compare2.png?v=1)

On the left (start) the mouth is closed; on the right (end) **the lower jaw is lowered, the mouth is open, and the bottle has reached the lips**. The human's three rejections — it doesn't reach the mouth, the mouth doesn't open, you can't tell what it's doing — are all resolved by this. The bottle is carried to around the lips (z=1.56 m, just above the lip point of 1.55 m defined in §10), the mouth opens, and from an angled side view the arm's motion can be read.

> What to take away (the three lessons of Part II): **① Before attributing a stall or a failure to "the limits of capacity," suspect the scoring sheet (the goal, the data).** — "It can't reach the mouth because of insufficient capacity" turned out to be "because I'd placed the goal at throat height." **② Before fixing code on a guess, measure and pin down the culprit.** — "The arm shifted" was wrong when I measured it; the real culprit was the bottle's initial position. **③ A keyframe or any initialization data is decided by "number (position)." If you add structure (a joint), always rebuild it.** — forget to update position-based initialization and the tests stay green while only the object quietly falls to the floor. And what exposed that quiet bug was not a test but the unease of a human who saw the picture. **Keeping a human in the loop (Human-in-the-Loop)** exists for exactly these moments.

---

# Part III — evis: This Skeleton Became a Mascot, Danced, and Ate with Chopsticks

> From here on, this is the record of what happened when I took that 700-muscle skeleton — the one that, up above, I honestly tipped over while trying to make it stand — turned it into a mascot, and drove it with mocap. And once again the star of the show is not a success story, but **the process of catching, by measurement rather than guesswork, the true culprit behind "when I made it walk, it hunched over like an old man."**

An honest caveat up front: Part III is **kinematic replay** (each frame's joint angles are set directly), not muscle-driven actuation. The chopsticks, too, are a "held-looking" rigid prop; the fingers aren't actually gripping. **What is genuine and what is cosmetic** I'll spell out at the very end.

## 17. Starting point — evis, a "human body whose insides you can see"

evis's base body is the same **MS-Human-700** from Part I. It's a biomechanics-research human model with 85 whole-body degrees of freedom and **700 muscles**. It has no skin — the bones (white) and the muscles and tendons (red) are laid bare. This "flesh-stripped" look became, as-is, the character's appeal. I settled on the name **evis**. The origin is two-layered:

- **Ebisu** — one of the Seven Lucky Gods. Auspicious.
- **eviscerate** — to remove the viscera and flesh. Exactly the figure of evis, reduced to nothing but bone and muscle.

The house style is "white bones + dark studio + red muscles that flare up as if igniting + comical white eyes + a stray cowlick swaying at the crown of the head (a secondary motion that lags behind the head's movement)." There's a trick to how the muscles light up: in kinematic replay there's no muscle activation, so **I make them flare red by the 'speed' of each body part** — an arm swung fast lights up in a flash. In effect, the motion pattern the movement demands is made visible.

## 18. Why mocap, and why the first wall was not "technology" but "licensing"

Even swinging the arms with hand-made sine waves, the motion is stiff. **I wanted to transplant real mocap.** But the first thing I ran into was not technology — it was **licensing**. FullSense, evis included, is under a commercial dual-license, so the mocap data also has to be usable commercially. Surveying the well-known sources:

| Source | Format | Commercial | SMPL dependency | Verdict |
|--------|--------|------------|-----------------|---------|
| **CMU MoCap** (cgspeed BVH conversion) | BVH | **Yes** | None | **Adopted** |
| AMASS / AIST++ | SMPL parameters | No | **Requires SMPL (non-commercial)** | Excluded |
| Mixamo | FBX | OK within a product | None | Requires an account; data redistribution prohibited |
| Bandai-Namco / LaFAN1 | BVH | **No (NC)** | None | Excluded |

`SMPL` is the standard model for human body meshes, but it's under a **research-only (non-commercial)** license, and both AMASS and AIST++ depend on it. It's widely used, but you can't carry it into a commercial product. The answer was the **CMU Graphics Lab Motion Capture Database**. Its license text reads "This data is free for use in **research and commercial** projects worldwide." It's self-contained as BVH (no SMPL needed) and can be fetched automatically via git. There is one caveat, though: **you must not resell "the data itself" (even in converted form).** So distributing a "retargeted animation" is OK, but **I made sure not to bundle the BVH files themselves in the repository** (they're pulled down by a fetch script when needed).

> Lesson: "technically best" and "distributable" are different things. If a research demo might morph into a commercial product, you're better off **adversarially verifying the license first.**

## 19. How retargeting works — moving "positions," not "rotations"

The BVH skeleton (a standard humanoid) and MS-Human-700 have utterly different joint structures. MS-Human-700 is OpenSim-derived: for example, the pelvis root is not a quaternion free joint but **six independent 1-DoF joints**, and the shoulder is a complex shoulder girdle with a "ghost body" interposed. Transferring rotation angles directly is hell.

So I made it **position-based**. I solve the BVH with forward kinematics and extract **only the "world coordinates (a point cloud)" of each joint**. Rotations are not transferred at all. After that, I solve for the joint angles with **differential IK (Levenberg-Marquardt)** so that evis's corresponding body parts land on top of that point cloud. It targets about 16 points — hands, elbows, knees, feet, head, and so on — and because it solves warm-started from the previous frame, one frame takes about 30 ms, and a 5-second clip can be retargeted in a few seconds. Since rotation isn't transferred, even that troublesome shoulder girdle gets distributed into a good shape by the IK on its own.

**Here there was a trap peculiar to kinematics.** MS-Human-700 has **42 equality constraints** on the knees, shoulder girdle, and wrists ("this ghost joint is determined by a polynomial of the shoulder angle"). But **in a replay that sets joint angles directly, these constraints aren't enforced by MuJoCo.** Leave them alone and the IK twists the shoulder-blade ghost body off in some wrong direction, and the shoulder breaks. So every frame, I **evaluate the polynomials myself and write the dependent joints in.** This makes the knee's screw-home and the shoulder's rhythm move correctly. (—As you've noticed, the same theme as the keyframe bug in Part II — "data determined by position, you have to take care of yourself" — shows up here again, wearing a different face.)

## 20. The main event — catching the real culprit behind the "old-man stoop" by measuring it

I made it walk. It moved. But when I had it reviewed, the verdict was one line: **"the back bends like an old man's."** Seen from the side, sure enough, the head jutted forward and the back was rounded — a textbook stooped posture. This is where this chapter's real subject begins: **the process of cornering the true culprit by measurement, not guesswork.**

**Hypothesis 1: is the head thrust forward?** Measuring the fore-aft gap between head and pelvis gives **0.3cm**. Almost directly overhead. **Rejected.**

**Hypothesis 2: was the source mocap stooped to begin with?** Measuring the neck's forward lean in the original BVH gives **9.5°** (mild), and the torso 1.6°. Nearly upright. **The source data isn't stooped. The retargeting is amplifying it.**

**Hypothesis 3: is the posture regularization too weak?** I added a term that weakly pulls the spine and neck toward neutral, but it made **almost no visible difference**. It's losing to the pull of the markers.

I stopped guessing and **measured the joint angles one by one**. And the culprit appeared:

```
T12_L1_FE      = -28.6°   (range [-29, +29] → pinned at the negative limit)
T1_head_neck_FE = +28.6°  (range [-29, +29] → pinned at the positive limit)
```

The mid-back (thoracolumbar spine) was jammed against one limit, the neck against the opposite one — **both saturated**. This was the real nature of the stoop. So why did the IK bend the joints all the way to their limits?

**The real culprit was a mix-up in marker heights.** evis's `thoracic1` (the topmost thoracic vertebra) sits **0.50m above** the pelvis (shoulder height). But I had assigned to it the BVH's `Spine1` (**0.26m above** the pelvis = mid-back). **I was trying to drag a body at shoulder height down to mid-back height, and the spine — which has only 3 segments — got compressed, folding the joints to their limits.**

The fix was simple: **change the correspondence to one where the heights match** — `thoracic12` (0.23m above) ← `Spine1` (0.26m). I removed the over-constraining `thoracic1` / `lumbar5` / crown-of-head markers, and let the posture regularization bite a little. As a result, the walk stood upright — and yet **the expressive back-arching of the dance (bending forward, leaning back) survived**, because that is a motion the markers genuinely demand.

> Lesson (the thing I most want to say in Part III): **if you try to fix it with "the head is probably thrust forward," you'll miss.** When I measured the breakdown behind the score (the joint angles), the culprit was an unexpected "marker height." It's exactly the same spirit as Part II's "measure first" — **measure before you guess.**

## 21. Once I made the eyes 3D, all the tricks vanished

evis's expressions (＞＜ or ◎◎) were, at first, **2D overlays**. Project the head's 3D position onto the camera to find the eyes' on-screen coordinates, use the depth buffer to decide "is this eye visible right now (or turned away and hidden behind bone)," then paste the whites and the emoticon on top — that was the mechanism. It worked, after a fashion, but a bug remained where **in profile, the far eye got projected onto the background and floated in midair.**

Then came a single remark: **"What if you make the whites a 3D sphere fused into the model, and paint the expression directly onto the eyeball as a texture?"** This was the right answer. I embedded eyeballs into the head as spheres baked with a **cube texture** per expression (the emoticon on the front face, white sclera on the others), prepared one for each emotion, and swapped them in by **leaving only the one set to display visible and making the rest transparent.** With that:

- The eyes **rotate together with the head.**
- **The bone (skull) hides the eyes naturally** — face away and the eyes disappear. No depth test, no projection math needed.
- It's correct at every angle. Whether the head spins in a dance or points down in a fall, it just becomes correct on its own.

The 2D projection-plus-depth trickery vanished wholesale (about 80 lines). There are 8 emotions (neutral's round eyes ●●, joy ＞＜, surprise ◎◎, love ♥♥ as a color-emoji texture, dead ×× …) plus arbitrary characters. Incidentally, I also fixed a bug here where the full-width ＞＜ was misjudged as an emoji and drawn faintly (a mix-up in the detection range).

![evis expressions](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/evis_mocap/evis_expressions.png?v=1)

Wired into a physics fall rollout, it even becomes a "live commentary" of evis changing expression as it topples — **neutral → ◎◎ (falling) → ×× (collapse).**

![evis reaction fall](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/evis_mocap/reaction.gif?v=1)

## 22. Motion library — walking, running, jumping, dancing, eating with chopsticks

Once the retargeting works, anything can dance just by swapping the BVH. I gathered these from CMU and moved them onto evis:

- **Walking / running / jumping** (subject 7 / 9 / 13)
- **Modern dance / salsa** (subject 5 / 60)
- **A soccer kick** (subject 10)
- **Eating with chopsticks** — I retargeted CMU's "drinking a soda" (the motion of bringing a hand to the mouth) and had evis grip **two chopsticks + a morsel of food** in its hand. I measured the "hand → mouth" direction and fixed the chopsticks' orientation in the hand's local coordinates, so as the arm rises, the tips of the chopsticks point toward the mouth.
- **A physics fall + a reacting face**

![evis walk](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/evis_mocap/walk.gif?v=1)

*↑ The walk after fixing the posture. The head is up, the spine straight. The moving leg fires red.*

![evis eats with chopsticks](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/evis_mocap/chopsticks.gif?v=1)

*↑ Eating with chopsticks. The two chopsticks gripped in the hand, plus a morsel of food, point toward the mouth as the arm rises.*

![evis motion showcase](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/evis_mocap/evis_motion_showcase.png?v=1)

---

# Part IV —— The Honest Limits of the Whole, and What Comes Next

## 23. What's Genuine and What's Cosmetic (Consolidated)

Honest disclosure is the core of this series, so let me gather the boundary line for the whole article into one place and state it plainly.

- **Genuine (research layer, muscle-driven)**: The standing, grasping, and carrying in Part I, and the **arm grasp and carry** of the drinking motion in Part II, are **closed-loop, muscle-driven** behaviors learned by evolutionary computation over 81 (or 100) muscles. The IK, force-closure, and keyframe-parity verifications are genuine too. The "loss" on standing, and the "no effect of memory" I refuted with n=3, are measurements I've left in without exaggeration.
- **Cosmetic (character layer)**: The **jaw open-close** in Part II is kinematic (scripted, because there are no facial muscles fitted), and moreover it opens to +0.6 rad—overwriting `qpos` directly—well past the designed range of motion (+0.05 rad); I state clearly that this is cosmetic, ignoring physics. evis's dancing, running, and chopsticks in Part III are **kinematic replay**: the red muscle firing is a proxy for "speed" (not muscle activation), the eyes and cowlick are rig, and the chopsticks are a **rigid prop** (not gripped by the fingers).
- **The "drinking" itself is not happening.** It isn't simulating the intake of liquid; it's the gesture of carrying the bottle to an opened mouth. It's a drinking *gesture*, not the *physiology* of drinking.
- **Omissions**: The **costal cartilage** of the ribcage is omitted, because this is a bones-only model (which is why the front looks hollow). I traced the anatomy down to the correct form (ribs 1–7 join the sternum, 8–10 form the costal arch), but it was hard to pull off as an approximation aimed at a character, so I left it off by default.

In short: **what the muscles are truly driving reaches only as far as "standing (though candidly a loss), grasping, carrying, and the drinking arm."** "Opening the mouth," "dancing," and "gripping the chopsticks" are a visual layer laid on top of that. Showing the GIFs while leaving this line blurred would be exaggeration, so I keep it here in bold.

## 24. What Comes Next

Having crossed three peaks, evis got as far as "trying to stand and honestly toppling, grasping, carrying, drinking, dancing, and eating with chopsticks." But the homework I've left is clear.

- **"Actually gripping the chopsticks with the fingers"** is not an extension of the kinematic approach; it's a separate peak that means **learning muscles by evolution**. Can an 81-muscle hand pinch a real pair of chopsticks—not a rigid prop—and carry food to the mouth?
- **Take back the loss on standing.** Simple integrator-based memory wasn't enough, so next I'll try a recurrent policy, an explicit ankle/hip strategy, or a hierarchy.
- **Put a face on the evaluation (eval) itself.** Just as I wired evis's expression to toppling this time, when the walking learner falls it goes ×× and when it makes progress it laughs with ＞＜—a mascot where **the simulation narrates itself**.

> Measure, honestly leave the losses in, and climb the next one. Question the breakdown most when the result looks good, and when you get stuck, measure rather than guess—that's the one point I hold to throughout this series. The story of evis, all bones and muscles, still continues.

---

## Appendix: Methods (notes for reproduction)

Reporting numbers without their conditions is dishonest, so here are the premises.

- **Model**: MS-Human-700 (Apache-2.0) / MuJoCo 3.10 / integration step dt=0.002s. Three variants: full body 85 DoF / 700 muscles, walking 36 DoF / 100 muscles, manipulation 48 DoF / 81 muscles.
- **CPU**: Intel Core (Ice Lake-generation mobile), 8 cores. Evolutionary evaluation runs **7 workers in parallel**; single-shot timing is **1 thread, idle**.
- **Standing**: walking scene (with floor), 6 s episodes, fall threshold = pelvis height 0.6m (initial 0.95m). CMA-ES, pop 16–40, generations 60–250. The policy is a muscle synergy (K=6 or 8). For the with-memory / without-memory comparison I took the median over 3 random seeds each, and confirmed that the apparent single-seed difference (4.53 s) disappears.
- **Grasping**: manipulation scene (shoulder fixed), 3 s episodes, CMA-ES pop 28, K=8, best at gen50 out of 250 generations. Contact friction μ=1.0.
- **Carry (place)**: same manipulation scene, scored on the average over 3 target points (straight up / at the side of the body / slightly forward and up). Observation = 19-dim grasp state + 3-dim command vector. Warm-start from the grasp champion (command-input weights zero-filled), sigma0=0.25. Converges to fitness ~1021 at gen30-50.
- **Drinking (jaw model)**: a derived model in which the head jaw geometry of the manipulation variant is split into a child body `mandible` + a hinge `jaw_open` (axis z, design range of motion −0.7 to 0.05 rad). Degrees of freedom go 48→49; the 81 muscles are unchanged. The jaw opening shown in the render pushes qpos directly (limits not applied) up to +0.6 rad, beyond the design range of motion — this is cosmetic. The bug: the jaw hinge lands at index 42 of `qpos` and shifts every subsequent slot by one. With the keyframe still 48 entries and zero-padded, the rotation angle −1.57 ends up in the bottle's up/down slide column (displacement relative to the desk at 0.94m), so it drops to z=0.94−1.57=−0.63m. The fix: insert `0.0` at index 42 of the original 48-entry keyframe to make it 49.

```python
import numpy as np
# orig_key48 = the original model's keyframe (48 values)
broken = np.concatenate([orig_key48, [0.0]])   # just appending 0 at the end = equivalent to MuJoCo's automatic padding (broken)
fixed  = np.insert(orig_key48, 42, 0.0)         # inserting the jaw's 0 at index 42 (0-indexed) = correct (49 values)
# measuring the bottle's world z right after reset:
#   broken -> z = -0.63 (below the floor)   /   fixed -> z = 0.94 (on the desk) = matches the original model
```

- **evis (mocap)**: mocap = CMU Graphics Lab Motion Capture Database (commercial use allowed, no SMPL dependency). Fetched via `scripts/fetch_cmu_dance.py --motion` (the BVH files can't be redistributed, so they aren't bundled and are pulled on-demand). Position-based differential IK (Levenberg-Marquardt, numpy + mujoco only, no scipy, ~30ms/frame). The 42 equality constraints for the knees, shoulder girdle, and wrists evaluate a polynomial every frame and write into the dependent joints. Facial expressions embed per-emotion cube-texture eyeballs in the head and swap them in via alpha.
- **Implementation**: retargeter `src/onocollo/evolve/mocap_retarget.py`, mascot `scripts/musculo_mascot.py`, muscle control `src/onocollo/evolve/musculo.py`. Output is mp4 (h264, for Qiita embedding) / gif, auto-switched by extension.
- **Provenance of the numbers**: everything comes from `out/musculo/*.json` and from re-running saved policies. Every quantitative claim in this article passed a **fact-check against the primary data and the real code in an independent, separate process + an editorial review** before publication. Spelling out the RTF conditions, refuting the standing memory effect at n=3, verifying grasp force-closure, confirming the mechanism of the keyframe bug, and disclosing the jaw's out-of-range opening are all things I fixed in response to those findings.

---
