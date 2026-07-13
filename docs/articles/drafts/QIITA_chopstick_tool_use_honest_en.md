---
title: "I Made an AI Grasp Objects with Chopsticks — and It Lost to Handwritten Control Again. Measuring 'Slip' and 'Crush' Honestly"
tags:
  - AI
  - ReinforcementLearning
  - Robotics
  - MuJoCo
  - EvolutionaryComputation
private: false
public_private: false
---

# I Made an AI Grasp Objects with Chopsticks — and It Lost to Handwritten Control Again. Measuring 'Slip' and 'Crush' Honestly

> For: people interested in robotic manipulation, reinforcement learning, evolutionary computation, and MuJoCo / anyone who wants to stress-test the claim that "learning beats handcrafting."
> Prerequisites: if you can read Python, you're fine. I break down the robotics and control terms as they come up.
> All numbers were measured locally. This experiment is still **in progress** — I'm writing down an honest interim report and, more importantly, how I measure it, not a conclusion. (In the sequel I'll try "a predictor that reads the moment right before a slip or a crush.") This is a stage-1 preliminary observation; stage-2 has **not** been run yet.

---

## 0. Three-line summary (conclusion first)

- In MuJoCo, I set up a rig where **two chopsticks** pinch an object, and I started comparing "control I wrote by hand" against "a policy learned by evolution," using my usual honest yardstick.
- It's still the easy entry point (pinching a box), but I can already **smell the same ending**: the handwritten scripted controller grasps the box trivially, while a naive linear policy evolved from scratch only **makes it as far as contact**. The same "handcrafting beats naive learning" that showed up in my rocket-landing article has come back for an encore.
- But that's not the point. There is no shortage of research on grasping objects. **What I actually value is an honest way of measuring that attributes failure stage by stage** — judging "grasped" from the *final pose*, and measuring "slipped and dropped it" versus "crushed it" **separately**. This article is the story of how I built that yardstick.

---

## 1. Glossary (a map, first)

| Term | Plain-language version |
|---|---|
| Grasp / grasping | The robot "picking up" an object. Here, pinching it between two chopsticks. |
| Tool-use manipulation | Manipulating an object **through a tool** — the chopsticks — rather than with the hand itself. The contact is more complex than a bare parallel-jaw gripper. |
| Split evaluation | Instead of collapsing the success rate into a single number, measure "alignment / contact / slip / lift" **separately**, so you can attribute which stage failed. |
| Slip | The object you (think you) grasped escaping from the grip. Common with round objects. |
| Crush | Breaking a soft object by squeezing it too hard. Here I use a proxy metric: "if the grip exceeds the force cap, it crushed the object." |
| condim (contact dimensionality) | The degrees of freedom a MuJoCo contact carries. 3 = sliding friction only; 4/6 = **torsional and rolling friction too**. You need it to stop a round object from rotating its way out of the grip. |
| Windowed impulse | Measuring force **averaged over a fixed window** instead of the instantaneous contact force at one moment. Hygiene, so solver noise isn't mistaken for something "predictable." |
| MAP-Elites / ES (evolution strategy) | Optimization that mutates and selects a population of solutions to improve them. Here it evolves the chopstick control policy. |
| held-out | Performance on a brand-new setting never used during training. The only evidence of generalization. |
| budget-matched baseline | A handcrafted opponent tuned with the **same compute budget** as learning. A fair referee that forbids the "I beat a weak opponent" cop-out. |

---

## 2. Why chopsticks, and why I surveyed the prior art first

Before building a new feature, I survey. It's a habit of mine. I did it this time too — and then I **honestly shrank the plan**.

Research on making robots use chopsticks is already thick. A line of work from the University of Washington (*Grasping with Chopsticks*, ICRA 2021 / *CherryBot*, 2023) runs imitation and reinforcement learning on real hardware chopsticks, going as far as grabbing small objects swaying in mid-air. And the decisive one is **Yang, Yin, Liu, *Learning to Use Chopsticks in Diverse Gripping Styles* (SIGGRAPH 2022, arXiv:2205.14313)** — in physics simulation, a **humanoid hand holds the chopsticks, automatically discovers diverse gripping styles, and carries objects around**. The "ambitious final form" I had pictured — a humanoid hand holding chopsticks — was **already done, to a high degree of polish, by that paper**.

So I honestly **cut** that stage. "Discovering diverse grips through evolution" is also already achieved by Yang et al. with a different method (Bayesian optimization), so that alone would not be a differentiator.

Then where, in this subject, is the novelty I can honestly claim? It is not the task. It is exactly one thing: **whether a low-dimensional world model that predicts the moment right before a slip or a crush can be used as the selection pressure (a gate) for evolution.** And before betting on that, I first need **a foundation I can measure honestly**. This article ends at that foundation (the result of the bet comes next time).

> A lesson, front-loaded: when you survey, your "interesting idea" has often already been done by someone. Don't be discouraged — think of it as a map that tells you **where the real gaps are**.

---

## 3. The stage: pinching with two chopsticks, in a minimal build

I built the following minimal rig (rig = test bench) in MuJoCo. A hand slides up and down to lift, and below it two chopsticks (stickL / stickR) slide inward to pinch. The pinched object (block) is a rigid body free to move.

```
world
 └─ hand        (z slide = lift)
     ├─ stickL  (y slide = pinch)
     └─ stickR  (y slide = pinch)
 block           (with free joint · box/sphere/cylinder)
```

![Two chopsticks pinch a box and lift it (scripted control · held = success)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/chopstick/box_grasp.gif?v=1)

Like in the rocket article, I wrote the XML as a raw f-string (small handcrafted scenes are more readable that way than through the procedural API). And here I hit **the first robotics trap**.

**Trap 1: round objects "rotate" their way out of the grip.** A two-chopstick pinch has two contact points that are roughly collinear. The object retains the freedom to rotate around that axis. With the default contact (condim=3, sliding friction only), a sphere spins and slips right through the grip. To stop it you need **torsional and rolling friction (condim=6)**. Conversely, the friction value here is a powerful knob that decides "graspable / not graspable" as a binary — and **tweaking the friction until you get the answer you want is an experimenter's degree of freedom, i.e. cheating**. So I decided friction is "a knob to be pre-registered in stage-2," and I fixed it in stage-1.

```xml
<default>
  <geom condim="6" friction="1.2 0.05 0.02" solref="0.01 1" solimp="0.9 0.95 0.001"/>
</default>
```

**Trap 2 (the crush judgment, below)** has the same smell — contact force is sensitive to the timestep and solver settings and spikes for a single instant. I'll collect on this in §4.

---

## 4. An honest yardstick: judge "grasped" from the final pose; separate "slip" from "crush"

This is the core of the article. Pinching experiments tend to get reported as a single number like "80% success rate," but that erases **which stage failed**. I attribute the following three **exclusively**:

- **held (grasped)** = in the trailing hold window, both sides are in contact, the object is lifted, and (if there's a cap) it isn't crushed. Here's the crux of honesty: a mere fleeting touch mid-run does not count as a grasp. **Judge from the final resting state** (judging from a transient xy position or a momentary lift produces false positives — a painful lesson from earlier kinematic-grasp work).
- **slipped** = not held, not crushed, and either "grasped but escaped" or "rolled away without ever being gripped." The failure mode of round objects.
- **crushed** = the **windowed-impulse (maximum) force** in the hold window exceeds the grip force cap. **Averaging over a window instead of taking the instantaneous peak** is the countermeasure to Trap 2: so that spikes from solref/solimp/timestep aren't mistakenly claimed as something we "predicted."

Turned into code, failures fall into stages:

```python
capped   = spec.force_cap > 0.0
crushed  = capped and grip_force_max > spec.force_cap      # squeezed too hard
held     = final_two_sided and lifted and not crushed       # lifted without crushing
slipped  = (not held) and (not crushed) and (contacted or xy_escape > slip_threshold)
```

And simply by changing the object's shape, you get a **real difficulty gradient** (all measured):

| Object | Result of handwritten scripted control |
|---|---|
| Box | **held** (grasped) |
| Sphere | **slipped** (it can even roll away before contact) |
| Box + low grip cap (cap 0.3N) | **crushed** (the same grip exceeds the cap) |
| Control that never closes | none of the above = **clean miss** (not miscounted as "slipped") |

![Trying to pinch a sphere with the same scripted control: it rolls out of the grip (slipped = failure)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/chopstick/sphere_slip.gif?v=1)

What these four lines mean is that I can **observe "box is trivial, sphere is hard, squeeze and you crush it" as separate metrics**. As an experiment, this is the foundation.

---

## 5. Adding learning: evolving a reactive controller

The handwritten script is **open-loop** (a hardcoded time schedule) and can't respond when the sphere starts to roll. So I evolve a **closed-loop** policy: a small linear policy that maps observations (block position, chopstick position, lift amount, two-sided contact flag) to a symmetric pinch amount and lift amount. The optimizer is `SimpleGaussianES` (CMA-ES if cma is available), reusing the **exact same core** I used for rocket and gait evolution, unmodified.

```python
def linear_controller(genome, spec):
    w = genome.reshape(2, 6)          # [pinch, lift] × [bias, bx, by, blift, handlift, two_sided]
    def command(t, obs):
        out = w @ features(obs)
        return np.array([pinch, pinch, lift])  # clipping omitted
    return command
```

---

## 6. The "honest preliminary result" already showed up — even the easy box loses to handcrafting

Here, **not overclaiming** is everything. This is not the stage-2 main experiment. It's just a mechanism check on an easy box, at a tiny budget. But that preliminary result is honest — and familiar.

- The fitness of the do-nothing zero policy = **0.00** (of course — it grasps nothing).
- Evolving it raises fitness to around **0.61 → 0.50**. Looking inside: **contacted=True (contact latched) but held=False**. In other words, it **starts to grasp but never makes it to a lift**.
- Meanwhile, the handwritten scripted control **trivially holds** the same box (fitness ~6).

Evolve a naive linear policy from scratch on a small budget, and it **reaches contact but comes nowhere near the handwritten controller**. This is the same geological layer as the **robust NULL (learning can't beat a fair PID and only ties)** I saw in the rocket-landing article. Handcrafted control is beating naive learning, again.

Let me lay on the honest caveats thickly: the budget is small, the initialization is zero, and the linear policy has low expressive power. **I am not claiming "learning can't win with chopsticks."** It's a **preliminary observation** that "in the easy entry point, in a naive setting, handcrafting is strong." But it is exactly this reproducibility that motivates the next bet.

---

## 7. Why I celebrate a "loss" (a gift to the reader)

- **When you lose to handcrafting, celebrate first.** It's evidence that "the baseline is strong." Learning that only beats a weak referee isn't an achievement — it's a measurement failure.
- **Say "learning won" only after you've tried to disprove it.** Split evaluation, a budget-matched baseline, judging from the final pose, windowed-impulse crush detection — these are all machinery for killing your own optimism.
- **An honest null, when it reproduces, becomes a "law."** Once with the rocket, once more with chopsticks. If "naive learning can't beat handcrafted control" shows up twice, the question to ask becomes "then *when* does it win?"
- **Don't chase task novelty.** Chopstick grasping is already out there. Put the value on the side of "a method to measure all the way to the end, with the same honest yardstick."

---

## 8. To be continued

The foundation is in place: the chopstick rig, a yardstick that separates slip / crush / grasped, and the evolution machinery. The difficulty gradient (box → sphere → crush) is observable too. What remains is the most interesting question —

> **If I build a low-dimensional world model that predicts "the moment right before a slip / right before a crush," and give it to evolution as the selection pressure (a gate), can learning surpass handcrafting on spheres and soft objects?**

If it can, that would be the first evidence that **"prediction"** was what mattered — not "reaction speed," not "memory." And if it can't — well, that just adds one more honest null to the map. Either way, I'll write it up.

Next time, I'll pit that predictor against a fair referee (a budget-matched baseline) on held-out settings, with pre-registration. Before the good numbers arrive, you should first get to see how it fails.

---

> Source of record: `onocollo/chopstick/` (model.py / rollout.py / evolve.py), plus the prior-art review (the UW chopstick-grasping trilogy / Yang et al. SIGGRAPH 2022 arXiv:2205.14313). All numbers measured on CPU locally. This is a stage-1 preliminary result; stage-2 has not been run.
