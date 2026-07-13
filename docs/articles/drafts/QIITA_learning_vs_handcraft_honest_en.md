---
title: "The Honest Story of Learning Repeatedly Losing to Handcraft —— And When Does Learning Win?"
tags:
  - AI
  - MachineLearning
  - ReinforcementLearning
  - EvolutionaryComputation
  - Control
private: false
public_private: false
---

# The Honest Story of Learning Repeatedly Losing to Handcraft —— And When Does Learning Win?

> Audience: people interested in reinforcement learning, evolutionary computation, and control engineering / people who want to verify rather than swallow the claim "learning beats handcraft."
> Prerequisites: being able to read Python is enough. I'll unpack control and learning terms as they come up.
> Every number is a local measurement (rocket is complete; chopstick is a stage-1 preliminary). This is a work-in-progress about disproving "learning won" before I dare say it.

---

## 0. TL;DR

- In my own two experiments —— **rocket vertical landing** and **chopstick grasping** —— a naively learned policy **could not beat** a fair, hand-designed controller. The rocket, under rigorous statistics, is a "tie (robust NULL)"; the chopstick "lost to a scripted controller even on the easy box, and stalled at contact (preliminary observation)."
- This is not a "failure" but a **valuable result**. When learning appears to beat control, the first things to suspect are "the baseline is weak" and "the statistics are thin." Both experiments kept that discipline (budget-matched baseline / held-out / paired confidence intervals / pre-registration / judge on the final pose / window-integrated crush detection), and so the phantom win evaporated.
- **So when does learning win?** The honest current state is: "making the evaluation rigorous stops the gaming, but that alone doesn't reach a win." My next bet is **building a low-dimensional world model that predicts the moment just before slipping or crushing into the selection pressure**. This article is a work-in-progress showing that, when you honestly stack up losses, something that looks like a "law" starts to emerge.

---

## 1. Glossary (the map first)

| Term | Unpacked |
|---|---|
| Hand-crafted control | A control law a human wrote as equations by understanding the physics. Classical control such as PID |
| PID control | The staple of control that cancels error in proportion (P), by derivative (D), and by integral (I). **The I (integral) is a memory that accumulates "error that keeps pointing the same way" and cancels it** |
| Learned policy | A controller whose parameters were determined automatically from data or trials. Here, mainly **a neural net whose weights were searched by evolution (ES)** |
| Evolution strategy (ES) | Optimization that mutates weights a little at a time and keeps the better ones. It can search for a policy without using gradients |
| Residual policy | "Hand-crafted control output + a small net's correction." If the net is zero-initialized, it **is the hand-crafted control as-is** (a warm start for evolution) |
| Memoryless | A policy that decides its output from "the current observation" alone and remembers nothing of the past. It cannot hold memory like an integral |
| Held-out | Performance on "new problems" never used in training at all. **The only evidence of generalization** |
| Overfitting | Getting strong only on the few scenarios used for evaluation, then collapsing on new ones |
| Objective gaming | Sacrificing the property you actually want (e.g., a soft landing) to run up the score number alone |
| Confidence interval (CI) | The range where "the true mean is likely to lie." **Only when the lower bound exceeds 0 is it "significantly a win"** |
| Paired evaluation | Pitting two policies against the **same random seed and same initial conditions**, and taking the per-trial difference. Robust to noise |
| Pre-registration | Freezing "what counts as success" **before** looking at the results. It forecloses post-hoc excuses |
| NULL | The result "there was no difference / it couldn't win." **A correctly measured NULL is a first-class result** |
| World model | An internal model that predicts what's coming in the environment. Holding "what happens next" lets you play ahead of a merely reactive controller |

---

## 2. Two experiments, the same ending

On a small physics simulator that runs on my home CPU (the MuJoCo-based `onocollo`), I handled two control tasks with very different characters under the **same discipline** —— "before you say learning beat handcraft, disprove it with a fair baseline and rigorous statistics." One is **aerial attitude control** (standing an inverted pendulum up on its exhaust and bringing it down), the other is **contact-rich manipulation** (grasping an object with two sticks and lifting it); the dynamics and the hard parts are completely different. And yet, the endings lined up eerily. "Learn it naively, and it doesn't reach a fair hand-crafted controller." Below, I'll look at the two in turn, honestly, with numbers.

### 2.1 Rocket vertical landing: a "tie" under rigorous statistics

`onocollo.rocket` is a toy that lands a booster with gimbaled thrust (thrust vectoring = a rudder that tilts the nozzle to change the direction of thrust) vertically. The vehicle is an **inverted pendulum standing on its exhaust**; leave it alone and it will always topple. That's exactly why landing it is itself a control problem.

As the hand-crafted reference, I placed a well-tuned cascade PD guidance. The **measurement (32 random landings, grid-tuned, honest)** was: landing rate 1.00 / soft rate ~0.85 / touchdown ~0.68 m/s / tilt at touchdown ~7°. Every random descent landed, and about 85% were soft landings that were "slow, upright, on the pad." **Handcraft — quite strong.**

On top of that, I add learning. `ctrl = pd_control(obs) + scale · MLP(obs)`. The MLP (multilayer perceptron) is zero-initialized = at first it's exactly the PD, and `(μ+λ)` evolution searches for improvement on top of the PD. Every candidate and the PD are scored under the **same random initial conditions**, so `best > baseline` is a fair test of "did learning surpass handcraft" —— or so it should have been.

The result kept repeating "looks like a win, but honestly can't win," step by step.

- **No wind**: the evolved residual **slightly beats** the PD (76.60 → 77.78, **+1.5%**). The PD is already strong, so the margin is small. It's just "add a little on top of good handcraft."
- **Sustained crosswind (memoryless residual)**: evolving with a small evaluation set (10 episodes) gives +26% in training (52.8→66.4). But on held-out it **loses** to the PD (20.5 vs 27.2). The gain was **overfitting to a finite set of evaluation episodes**. Increase the evaluation to 24 and the training gain shrinks, and held-out becomes a **tie**. It doesn't transfer. The reason is plain: a memoryless policy can only cancel a constant lateral force with a "constant tilt," and having **no integral memory**, the steady-state offset never disappears.
- **Adding state to the handcraft (PID)**: give it an integral of lateral drift, and it beats the PD **modestly but consistently** (soft rate 0.09→0.16, etc., never getting worse). The hypothesis "state is what's missing" was correct —— **handcraft with state beats learning that lacks state.**
- **Giving state to the learning (recurrent)**: make an RNN's hidden state the residual. Training is `PID 53.8 → recurrent 65.1`, **+21%** —— a win that looks big. But it doesn't transfer to held-out, and worse, **on every held-out its soft rate is lower than the PID's**. Evolution **earned scalar fitness at the expense of soft landing** = objective gaming.

By this point I understood that "the headroom is not in the policy's capacity but in the evaluation," so I settled it by **pre-registering the evaluation design itself** (the version that piled on all of the discipline described below). The result of the primary criterion P was ——

**Robust NULL. It could not beat the fairly re-tuned PID.** On TEST (3 streams × 100 episodes, paired), **0/10 seeds were positive**, and the fitness confidence interval straddles 0 on all three streams (`+0.1[-1.2,+1.3]`, `-0.1`, `+0.5` = **a tie, not a loss**). The full-stack evaluation improvements **push learning up to a tie**, but there was nothing beyond that.

> An honest caveat (so as not to make the numbers look "clean"): on exactly one TEST stream, the soft channel produced a positive signal with `+0.035[+0.015,+0.055]`, its CI lower bound exceeding 0. But it was offset on another stream, and that stream's fitness CI straddles 0, so it isn't a win. I'm putting this one instance out in the open too, without hiding it.

Let me lay out all the conditions of the deciding experiment, losses included, in a single table (held-out is the `policy − PID` difference). How to read the columns: even when the training gain is large, it collapses to ≈0 on held-out, and the larger the overfitting gap (training − held-out) that remains, the more it was a "phantom win."

| Condition | Policy / Eval | Training gain | held-out fit diff | Overfit gap | held-out verdict |
|---|---|---|---|---|---|
| **P (primary)** | recurrent, resample + soft-margin + val selection | +3.7 | **−0.1** | +3.8 | **tie** (0/10 positive) |
| C_evaldesign | recurrent, resample + **scalar** objective | +9.4 | −4.2 | +13.6 | loss |
| C_sham | recurrent, **fixed** eval + soft-margin | +8.7 | −0.0 | +8.8 | tie/loss |
| C_feedforward | **memoryless** MLP, resample + soft-margin | +6.7 | −1.9 | +8.6 | loss/tie |
| R_nominal | recurrent, no wind (sanity) | +0.5 | −0.1 | +0.6 | tie |

There are three key takeaways. (1) **The apparent wins vanished under rigorous statistics** —— the primary criterion P's training +3.7 became −0.1 on held-out, 0/10 seeds. (2) **The eval improvement is real, but stops at a tie** —— switching to the soft-margin objective stops the objective gaming (P is a tie; the scalar C_evaldesign loses at −4.2), and resampling halves the overfitting gap (P +3.8 vs fixed C_sham +8.8). It pushes loss → tie, but doesn't create a win. (3) **None of the training gains transfer** (training +3.7 to +9.4 becomes ≈0 on held-out).

To be extra sure, I also tried **time-varying gusts**. This is the answer to the suspicion "wasn't a constant wind too favorable to the integral (PID's I)?" Re-tuning the PID under gusts, the optimum was **`k_i=0` (pure PD with no integral)** —— **the integral is actually harmful**, and a "reactive" pure PD became the best hand-crafted control. In theory this is a regime where "speed of reaction over memory" pays off, so learning ought to have a chance. And yet ——

**Another tie.** `P_gust` (recurrent) is 0/10 seeds, and its TEST fitness CI straddles 0 on all three streams. The feedforward version shone on exactly one stream with fit `+4.3[+2.3,+6.2]`, but the other two streams were losing/flat, held-out was a loss, and seeds were 0/4 —— **failing every gate, it is not a robust win**. My prediction that "under gusts, learning has the edge thanks to reactivity" was, honestly, **wrong** (the hypothesized mechanism — that the integral stops helping — was correct, but that didn't mean learning would win).

### 2.2 Chopstick grasping: it lost to scripted even on the easy box (preliminary observation)

The other task is of a different feather —— **picking up an object with chopsticks and lifting it (tool-use manipulation)**. `onocollo.chopstick` is a minimal 3-DoF rig where two stick tips close in the y direction (pinch) and lift in the z direction (lift), nothing more.

This task's **#1 modeling risk** is "the box rotating about the two-point contact axis and slipping through." So I put **condim=6** (torsion + roll friction) into the contact to stop the rotation (with the default condim 3, the object rolls out of the grip). This I treat as a **pre-registered knob** in stage-2 —— "tuning the friction until an answer comes out" is self-deception via experimenter DoF (experimenter's degrees of freedom), so I don't do it.

And I made the **success criterion thoroughly honest**. This is a direct import of the lesson learned in kinematic grasping (look at the final pose, not a fleeting instant):

- **Success = the final "held" state** (both-sided contact AND lifted above a threshold AND not diverged, judged **at the end of the hold window**). A momentary touch mid-swing does not count.
- **The crush judgment is the window-averaged force**. Because the contact normal force spikes every few steps due to solver behavior, looking at the instantaneous peak lets you "predict the solver's noise." So I take the **average** over the hold window.
- **The grip latches after a dwell**. Only when both-sided contact continues for `_GRIP_CONFIRM` steps do I acknowledge a "grasp." A mere graze is not a grasp.

I built the fitness honestly too: +5.0 for `held`, shaping proportional to lift height, +0.5 for contact, and a **−1.0 penalty if it crushes** (overgrasping must not score higher than a clean miss).

Now, the **honest preliminary observation here (an observation to keep me on guard, not a result)**:

> On the **easy box**, a hand-written scripted controller (open-loop, just "close hard → lift") **easily reached held** (fitness ~6). Meanwhile, a **naive linear policy evolved from scratch on a small budget only reached contact (~0.5)**. —— **Handcraft again overtook naive learning. The same pattern I saw with the rocket.**

Let me look at the mechanism of why scripted wins so easily and naive learning stalls at contact. The scripted controller has a human who knows the physics **hard-coding the procedure** as "settle → close hard (0.5 s) → lift slowly," so for the flat face of the box it reaches held by the shortest path. The linear policy evolved from scratch, on the other hand, merely maps six features `[bias, block_x, block_y, block_lift, hand_lift, two_sided]` linearly to `[pinch, lift]` —— **on a small budget it can't even stably discover the ordering "close sufficiently first, then lift"**, and tries to lift before it's fully closed, stalling at contact (fitness ~0.5). This is not "learning is impossible in principle," but the exact same structure as the rocket's residual policy: **the search budget and policy class don't pay off against hand-written prior knowledge**. Handcraft carries into the baseline the handicap of "prior knowledge a human has piled up."

Let me emphasize: this is a **stage-1 preliminary observation, not a conclusion**. Stage-2 (the real thing) has not been run. The stage-2 design is already fixed —— compare the evolved **reactive** closed-loop policy on **round / soft objects** (separating slip vs crush, with a crush proxy called force_cap), against a **budget-matched baseline** and **held-out seeds**, and **use a predictor of slip / crush (= a small world model) as the QD gate**. It is **far too early** to conclude in this article that "chopstick, learning lost." All I can say now is "on the easy-box smoke test, naive learning lost to hand-written."

---

## 3. Why this is a "valuable result," not a "failure"

The same picture came out of both experiments. What matters here is that **this loss is measured correctly**. When learning appears to have beaten control, there are two prime suspects to interrogate first.

**Suspect A: the baseline is weak.** Against a weak handcraft, learning can win "trivially." So both experiments kept the baseline strong, and **fair**. For the rocket, I re-tuned the PID under the **same objective, same wind, and same evaluation budget** as the learning (discovering `k_i≈0.012`). Because if you face a "baseline left at its old settings," it's obvious that learning wins. For the chopstick, I pre-registered into the stage-2 design that the comparison be against a **budget-matched baseline**.

But here I once **fooled myself**, so I'll write it honestly. As an interim conclusion for the rocket, I started to write "the original PID (k_i=0.005) was under-tuned, and when it was re-tuned fairly the apparent win vanished." A clean story. But when I checked after the experiment, **on TEST k_i=0.005 ≈ 0.012** (for soft, 0.005 is even marginally higher), and my story of "the original bar was weak" did not hold up on TEST. The true cause was far more mundane —— the apparent win was not a "weak judge" but Suspect B below.

**Suspect B: the statistics are thin.** The past "recurrent wins" was "fitness 3/3 on 3 seeds, no confidence interval." Re-measure this with **paired, 10 seeds, bootstrap CI**, and it's **0/10, negative pooled mean**. Small N, no CI, and seed-dependent noise had merely looked like a win. For the chopstick too, I built paired common random numbers (both policies see the same initial conditions under the same seed) into the rollout.

Keep these two disciplines —— a **strong, budget-matched baseline** and **rigorous statistics with pairing, many seeds, and CIs** —— and the phantom win self-destructs. So the "tie / loss" that remains is **trustworthy**. A trustworthy NULL becomes the correct starting point for the next experiment. Honest disclosure should be aimed not only at other people's claims but **at your own interim conclusions** too.

### 3.1 An "honest-bench pattern" common to the two tasks

The interesting thing is that the toolkit I used for the rocket and the chopstick converged on the **same pattern**. This is a reuse template that emerged unintentionally, and it can be ported to other tasks:

- A **physics model (`model.py`)** + an **honestly-scored env (it collapses fitness into a single number, but always emits the breakdown separately)**. The rocket separates landing rate, soft rate, touchdown speed, and tilt; the chopstick separates `contacted / held / slipped / crushed / lift_height / grip_force`. **Don't hide failures inside a single success rate.**
- **Tune the hand-crafted baseline strongly first**, then place a **warm-started learned policy** (zero-initialized residual = at first it is the handcraft itself) on top. This makes "did learning surpass handcraft" a fair subtraction.
- **Judge on the final pose** (rocket at touchdown, chopstick at held at the end of the hold window). Don't count a fleeting appearance as success.
- **Smooth noise by window integration** (the chopstick's crush judgment is the window average of the normal force. Looking at the instantaneous peak lets you fake "predicting the solver's noise").
- **Pair with the same seed** (common random numbers where both policies see the same initial conditions) + **measure generalization with held-out seeds**.

Because this pattern exists, I don't have to redesign "honesty" from scratch each time I add a new task. And because the pattern is the same, **I can line up the two tasks' NULLs side by side and compare them** —— this is the foundation that turns "one whiff" into "a law that reproduces."

---

## 4. So when does learning win? (an honest hypothesis)

Here is the real gift to the reader. I'm not trying to say "learning always loses." I want to narrow down **when it wins**, honestly, with feet planted on measurements.

### 4.1 (a) Making the evaluation rigorous and resampled suppresses gaming —— but even so, it doesn't reach a win

The "eval-signal stack" I assembled for the rocket's deciding experiment was all opt-in (default OFF = doesn't break the past NULLs), and stacked the following:

1. **Per-generation resampled eval** (foreclose memorizing a fixed set).
2. **Continuous min-margin soft objective** (a smooth bonus proportional to the minimum of three soft margins. Don't make it the cliff of binary `int(soft)` —— the cliff mass-produces barely-soft landings that collapse on generalization).
3. **Validation block selection** (selecting the highest training fitness on a moving eval overfits to a "lucky draw," so select on a separate block, and with the original objective at that).
4. **A fairly re-tuned PID** (as above).
5. **Leakage-free paired evaluation** (splitting seeds into million blocks + a runtime `assert_no_seed_leakage`, paired differences of common random numbers + bootstrap CI).

The effect was real. The soft-margin objective **stopped the objective gaming** (the primary criterion P is a tie; the scalar-objective control loses at −4.2), and the resampled eval **halved the overfitting gap** (P's +3.8 vs the fixed eval's +8.8). **It pushed loss → tie.**

But —— **it stopped at a tie.** Making the evaluation rigorous is **necessary but not sufficient**. That is the honest conclusion. I had expected that "fixing the evaluation would make learning win," but no win could be made.

Why was the ceiling a "tie"? My reading is this. The work of making the evaluation rigorous essentially works **only in the direction of trimming phantom wins** —— it forecloses objective gaming and strips away the padding of overfitting. This is an operation that **takes off the risers (the boost)**, not one that **gives the policy a new ability**. Since the hand-crafted PD/PID already has this task's structure (constant wind = integral, gust = reaction) built in as human knowledge, naive learning with all the risers stripped off merely stands "on exactly the same footing" —— it has no capital with which to overtake. To overtake, the only option is to add to the policy side an ability handcraft **does not have** —— **prediction** of disturbances and slips. So the next lever is not "the evaluation" but **"what to give the policy (a world model)"** —— that's where the two experiments point.

### 4.2 (b) Precisely in regimes where reactivity / memory intrinsically pay off, learning and world models have a chance —— but under gusts the NULL continued

The reasoning goes like this. A sustained, constant wind is a regime where "memory (the integral)" pays off, which is why hand-crafted PID was strong. Conversely, under **time-varying gusts**, the integral is always a step behind and fires off-target, so **"speed of reaction"** pays off over "memory" —— here learning ought to have a chance.

The mechanism prediction was right: under gusts the hand-crafted optimum became **`k_i=0` (pure PD)**, and the integral turned harmful. **But learning did not clearly surpass pure PD there either** (§2.1). Even carried into the reactive regime, no robust win emerged.

I'll also disclose the **honest scope**. The rocket's fitness channel is **underpowered** for an effect of this magnitude (against a per-episode standard deviation ≈ 20, the candidate effect is `+0.06…+0.52`, Cohen's d < 0.03). So this is "**there is no economically meaningful win**," not "proof of zero effect." That's the line I draw to keep from over-interpreting the NULL.

### 4.3 (c) The next bet = using "a low-dimensional world model that predicts the moment just before slipping / crushing" as selection pressure

So where is the thread not yet tried? The chopstick's stage-2 is that bet.

The chopstick task's intrinsic hard part lies **not in the box (easy, flat), but in spheres / cylinders (slip) and soft objects (crush)**. Here a reactive policy that only looks at "this very instant's observation" is too slow —— only when it can predict the moment **just before an object starts to slip**, or **just before it crushes**, can it make an anticipatory grip adjustment. The rollout is already built to measure that separation: it emits `slipped` (grasped but escaped / rolled out) and `crushed` (the window-averaged maximum force exceeded force_cap) as separate metrics.

The bet is clear: **when a small world model that predicts slip / crush is built into the QD (Quality-Diversity) gate of evolution, will naive learning — which lost to hand-written on the box — surpass hand-written on round/soft?** Precisely in the regimes where reactivity intrinsically pays off (time-varying disturbances, slipping objects), learning that holds prediction has a chance —— that, on top of two stacked NULLs, is my most honest hypothesis.

Let me restate in mechanistic terms why a "world model" could be the key. What I learned from the rocket's gusts is that "pure PD (reaction only) falls a step behind when the disturbance moves faster than the reaction." A reactive controller's lag can be filled only by **predicting the disturbance**. The chopstick's slip / crush has the same structure —— both `slipped` and `crushed`, if you observe them **after** they happen, are too late; only by reading ahead from the state **just before** they happen (how the contact normal force is growing, the faint sign of the object's micro-rotation) can you deal with them. Hand-crafted PID has no cheap way to build in this "reading ahead" (the integral is a past average, not a prediction of the future). This, I believe, is the true identity of the gap open only to a **learned policy with prediction built in**, and neither to a naive reactive policy nor to handcraft.

Conversely, the box (flat, non-slipping) and the sustained wind (constant, cancelled by the integral) are regimes where **prediction is unnecessary**, and that's why handcraft was strong. The most honest reading of the two NULLs is not "learning is weak" but "**in regimes where prediction is unnecessary, handcraft is enough**." So what I should bet on next is the regime where prediction *becomes* necessary.

But to reiterate: stage-2 hasn't run yet. I will not write "learning won" until **I've disproved it with a budget-matched baseline and held-out seeds**. I'll apply the discipline I learned on the rocket to the chopstick as-is. And —— if learning cannot surpass handcraft even on round/soft, I'll write that honestly too. A third NULL would be strong disconfirmation of the hypothesis that "prediction is the key." Not deleting losses is the backbone of this whole line of work.

---

## 5. On prior art (honestly)

Let me write honestly about the task's novelty. **Chopstick manipulation itself is not new.** Yang et al.'s SIGGRAPH 2022 paper ("Learning to Use Chopsticks in Diverse Gripping Styles," arXiv:2205.14313) already achieves diverse gripping-style manipulation with a humanoid hand + chopsticks. My chopstick rig is **a toy by comparison**, and I claim no novelty as a task.

What I'm doing is a different thing —— **measuring "hand-crafted control vs naive learning" across multiple tasks under the same rigorous discipline, and honestly stacking NULLs**. If there's a contribution, it lies not in a new task but in **the reproducibility of the "loss" and the etiquette of disclosing its breakdown**. I believe this saves the next person's time more than a flashy win claim does.

---

## Lessons (gift-to-reader)

- **When you lose to handcraft, rejoice first.** It's evidence the baseline is strong. Learning that tied a strong opponent holds far more trustworthy information than learning that beat a weak one.
- **"Learning won" — say it only after you've disproved it.** The first suspects are "a weak baseline" and "thin statistics," not a flashy method or policy capacity. A 3-seed win with no CI dissolves under paired, 10 seeds, CI.
- **Doubt your own interim conclusions too.** I once wrote "the under-tuned baseline is the cause," and disproved it with my own additional check. Honest disclosure is aimed not only at others but at yourself.
- **Evaluation design > policy capacity.** The headroom was not in making the RNN bigger, but in making the evaluation rigorous —— and even then it didn't surpass fair handcraft. Rigorous evaluation is **necessary but not sufficient**.
- **An honest NULL, when it reproduces, becomes a "law."** The rocket and the chopstick produced the same picture. One NULL is a whiff, but a NULL reproduced across two independent tasks becomes an empirical rule that guides the next design: "naive learning does not easily surpass strong handcraft."

---

## To be continued

The remaining question is simple. **When a world model is built into the evaluator (or the selection pressure), does this losing streak move?**

- Chopstick stage-2: make a small world model that predicts slip / crush the QD gate, and settle it on round/soft objects with a budget-matched baseline and held-out seeds. **Can the naive learning that lost to hand-written on the box win on round if it holds prediction?**
- Rocket: when the observation becomes not a "state vector" but a "camera image" (a world model V/M/C that learns landing from pixels), does this tie move? And with a **moving pad** —— in a regime where reactivity matters even more?

The honest current state is "learning has not yet beaten strong handcraft." But **where it might win** has, thanks to the two NULLs, been narrowed down considerably. Next, into that narrowest gap —— **the slipping, crushing regime where prediction intrinsically pays off** —— I'll insert a world model. If I lose, I'll write it honestly again.

---

> Note: The canonical source for the rocket numbers is `onocollo-complete/docs/rocket_landing.md` (experiments in `scripts/rocket_eval_experiment.py` and others, results in `out/rocket/eval_exp/`). The chopstick preliminary observation is in `src/onocollo/chopstick/` (docstrings of `model.py` / `rollout.py` / `evolve.py`). The rocket is complete; the chopstick is a stage-1 preliminary with stage-2 not yet run. This article is a draft.
