# I Made an AI Land a Rocket — and It Couldn't Beat the Hand-Crafted Controller. Then I Disproved My Own "It Won"

> For: anyone curious about reinforcement learning, evolutionary computation, or control engineering / anyone who wants to test the claim "learning beats hand-crafting."
> Prerequisites: if you can read Python, you're fine. Control terms are unpacked as we go.
> This is a pre-publish draft (numbers are measured; publishing is a human decision).

---

## 0. TL;DR (3 lines)

- In MuJoCo, I made a **gimbaled-thrust rocket (booster) land vertically**, and honestly compared a "hand-designed controller (PID)" against a "policy learned by evolution."
- Done naively, learning *looks* like it wins. But **once you make the evaluation rigorous (resample every generation + a soft objective + paired scoring across 10 seeds with bootstrap confidence intervals) and also re-tune the referee PID fairly, learning can't win — it's a draw.** (As we'll see later, what actually mattered was mostly the *statistical rigor*; re-tuning the referee turned out to be hygiene, not the deciding factor.)
- The biggest lesson isn't technical, it's an attitude: **when "learning beat control," your first suspects should be "a weak referee" or "thin statistics."** This article includes the time I fell into that trap myself, and how I disproved my own conclusion.

---

## 1. Glossary (the map first)

| Term | In plain words |
|---|---|
| Terminal descent | We only handle the "last few seconds" as the rocket touches down. No orbital mechanics. |
| Thrust vectoring (gimbaling) | Tilt the engine nozzle to steer the thrust direction = the rudder that keeps an inverted pendulum upright. |
| PD / PID control | Cancel error by proportional (P), derivative (D), and integral (I) terms — the classic of control engineering. **I (integral) is a memory that accumulates "error that keeps pointing the same way" and cancels it.** |
| Residual policy | "PD output + a small neural-net correction." If the net is zero-initialized, it **is just PD** (a warm start for evolution). |
| Overfitting | Getting strong only on the few scenarios used for evaluation, then falling apart on new ones. |
| held-out / TEST | Performance on a "new problem set" never used in training. The only evidence of generalization. |
| Fitness | The landing quality collapsed into a single number (higher = slower, more upright, more on-pad). The quantity evolution maximizes. |
| CI (confidence interval) | The range the true mean is likely to lie in. **Only when the lower bound clears 0 is the result "significantly positive."** |
| Pre-registration | Freezing "what counts as success" **before** you look at the results. It forecloses after-the-fact rationalizations. |

---

## 2. The stage: an inverted pendulum standing on its own exhaust

Using `onocollo.rocket` (a MuJoCo toy that runs on CPU), I build a booster with a free-joint body, four landing legs, and a two-axis hinged gimbal nozzle. There are three controls:

| idx | Actuator | Effect |
|---|---|---|
| 0 | thrust | The lift that stops the fall (0 to TWR × weight, default TWR 2.4) |
| 1 | gimbal_x | Vector thrust into the y-plane = attitude about the x-axis |
| 2 | gimbal_y | Vector thrust into the x-plane = attitude about the y-axis |

(TWR = thrust-to-weight ratio = max thrust ÷ weight. Below 1 you can't arrest the fall.)

The key point is that **left alone, this vehicle always falls over** (an inverted pendulum standing on its exhaust). That's what makes "landing it at all" a control problem. The legs reach below the nozzle, and **the moment they touch down the engine cuts off** (just like the real thing — keep burning and the vehicle gets shoved over after touchdown).

### A debugging aside: calibrating the gimbal sign with physics

One quietly annoying snag while writing the controller was **the gimbal sign**. The two axes "respond with opposite signs" — `gx = -k·(error)` but `gy = +k·(error)`. Rather than agonize over it on paper, I commanded a small deflection on the actual vehicle and *measured* the sign of `d(tilt)/d(gimbal)` to pin it down. For control, "move it once and look at the sign" beats "staring at the equations."

---

## 3. Baseline: a well-tuned PD guidance law

As a strong "hand-crafted" reference, I set up a cascaded PD guidance law:

- **Vertical**: track a descent-speed profile `v_target = -(v_land + v_slope·altitude)`. Near the ground it thins down to `v_land` = a soft touchdown.
- **Lateral/attitude (cascaded)**: when there's lateral offset or drift, command "lean slightly toward the pad" (a vehicle only translates sideways once it tilts), and an inner attitude loop chases that tilt with the gimbal → rights it directly overhead.

**Measured (32 random landings, grid-tuned, honest):** landing rate 1.00 / soft rate ~0.85 / touchdown ~0.68 m/s / tilt at touchdown ~7°. Every random descent lands, and ~85% are "slow, upright, on-pad" soft landings. **Hand-crafted, and quite strong.**

---

## 4. Add learning: a residual policy, and an honest baseline

`ctrl = pd_control(obs) + scale · MLP(obs)`. The MLP (multilayer perceptron = a small neural net) is zero-initialized = at the start it *is* PD. A `(μ+λ)` evolution (breed λ children from μ parents by mutation, keep the better ones) searches for improvements on top of PD. Every candidate and PD are scored on the **same random initial conditions**, so `best > baseline` is a fair test of "did learning surpass the hand-crafted controller?" — or so it should have been.

- **No wind (nominal):** the evolved residual **slightly** beats PD (76.60 → 77.78, **+1.5%**). PD is already strong, so the gap is small. Learning only "adds a little on top of a good hand-crafted controller"; it doesn't rescue a bad one.

## 5. Add wind and a null appears (an honest impasse)

`hard_config()` adds a sustained crosswind (≈0.13× weight, random direction and strength each episode). Here's the interesting part: **a memoryless P(+D) law can only offset a constant lateral force with a constant tilt, and a steady offset it can't erase remains** (it has no integral memory).

- Evolving a memoryless residual under wind with a **small eval (10 episodes)** → +26% in training (52.8→66.4). But on held-out it **loses** to PD (20.5 vs 27.2). The gain was **overfitting to a finite number of evaluation episodes.**
- Raise the eval to 24 → the training gain shrinks (+13%), and held-out is a **draw** with PD. It doesn't transfer.

**Honest conclusion (Act 1):** a memoryless residual does not surpass PD under sustained wind. The reason is clear — **it has no state (memory).** → Next, then: a controller *with* state.

## 6. Add state: PID (the integral) helps "a little"

The hypothesis "it's missing state" is testable, so I tested it. `PIDController` carries the **integral** of the lateral offset (with anti-windup) and cancels a sustained wind over time.

**Measured (hand-tuned `k_i≈0.005`):** a small integral term beats PD **modestly but consistently** (soft rate 0.09→0.16, etc., never worse). But it's not dramatic — terminal descent lasts only ~3 seconds, and the vehicle touches down before the integral fully builds up. Too large a `k_i` gets worse from windup.

→ The punchline of the first half of the arc: **hand-crafted state (the integral) beats memoryless learning that lacks state.**

## 7. Give learning state: a recurrent policy — overfitting again

I give a `RecurrentPolicy` (RNN = recurrent neural network, which can hold "memory" in a hidden state; that hidden state becomes the residual on top of PD, zero-initialized for a warm start) the same "memory" that PID has, and let evolution use it however it likes. The baseline is the **hand-tuned PID.**

- **Training:** `PID 53.8 → recurrent 65.1`, **+21%** — a big-looking win.
- **held-out:** it doesn't transfer. 1 win / 1 loss / 1 draw, and on top of that **the soft rate is lower than PID on every held-out stream.** Evolution **earned the scalar fitness at the expense of soft landings** (objective hacking).

**Honest conclusion (Act 2):** on held-out, the hand-tuned PID beats the learned recurrent policy. The +21% is, again, overfitting plus objective hacking. **The next headroom isn't policy capacity — it's the *evaluation*.**

---

## 8. 【The main event】Pre-registering and testing "the evaluation is the lever"

This is where the new work begins. Since the null pointed to "evaluation is the headroom," I **pre-registered that and settled it.** The design was frozen before looking at results (`feedback_benchmark_honest_disclosure`).

### 8.1 Pre-registering the method adversarially (multi-AI orchestration)

I hardened the design itself with a **6-agent Workflow**, adversarially: four lenses (overfitting / objective design / baseline fairness / honest disclosure) designed in parallel → integrated → **adversarial critique**. The critics precisely skewered the flaws in my initial implementation — "validation selection is done under a gamed objective and is circular," "judging on the selected set is a winner's curse (= pick the best of many candidates and the *picking* catches luck, inflating the estimate)," "the soft bonus is a binary cliff," "seed splitting is defective." I fixed all of them before running.

### 8.2 The eval-signal stack (all OFF by default = don't break the past nulls)

1. **Per-generation resample eval:** forecloses memorizing a fixed set.
2. **Continuous min-margin soft objective:** a smooth bonus proportional to the **minimum** of the three soft margins. Not the **binary `int(soft)` cliff** (a cliff mass-produces marginal "soft" landings that collapse under generalization).
3. **Validation-block selection:** picking "highest training fitness" on the moving eval overfits to a "lucky draw," so I select on a **separate block** and, moreover, under the **original objective (w_soft=0).**
4. **Fairly re-tuned PID:** re-tune the PID under the same objective, wind, and budget as learning.
5. **Leak-free paired evaluation:** split seeds into million-blocks (TRAIN 1M / VAL 2M / TEST 3M / TUNE 4M) + a runtime `assert_no_seed_leakage`, paired differences under common random numbers + bootstrap CIs.

### 8.3 The pre-registered primary decision

Evolve the recurrent policy with the full stack and compare it against the re-tuned PID. **CONFIRM (learning beats a fair PID thanks to the improved evaluation) only holds when**, on TEST (3 streams × 100 episodes, paired), **every stream's fitness CI lower bound > 0 and the soft CI lower bound ≥ 0, and at least 8 of 10 seeds are individually positive.** "Wins on fitness but loses on soft" is automatically classified as an **objective-hacking null.**

---

## 9. Result: a robust NULL — it can't beat a fair PID

| Condition | Policy / evaluation | Training gain | held-out fit Δ | Overfit gap | held-out verdict |
|---|---|---|---|---|---|
| **P (primary)** | recurrent, resample + soft-margin + val-selection | +3.7 | **−0.1** | +3.8 | **draw** (0/10 positive) |
| C_evaldesign | recurrent, resample + **scalar** objective | +9.4 | −4.2 | +13.6 | loss |
| C_sham | recurrent, **fixed** eval + soft-margin | +8.7 | −0.0 | +8.8 | draw/loss |
| C_feedforward | **memoryless** MLP, resample + soft-margin | +6.7 | −1.9 | +8.6 | loss/draw |
| R_nominal | recurrent, no wind (sanity) | +0.5 | −0.1 | +0.6 | draw |

The primary decision P passes none of the gates: **0/10 seeds positive**, and on all three TEST streams the fitness CI straddles 0 (`+0.1`, `-0.1`, `+0.5` = **a draw, not a loss**). The full stack **pushes learning up to a draw**, but no further.

> An honest caveat: the one exception was that on TEST soft, stream s2 produced a positive signal with a CI lower bound above 0, `+0.035[+0.015,+0.055]`. But it's offset by another stream, and that stream's fitness CI straddles 0, so **it's not a win.** To avoid dressing the null up as "clean," I include this single signal too, unhidden.

### 9.1 An honest decomposition — what actually mattered

1. **The apparent win vanished under rigorous statistics.** The old "recurrent wins" was "fit 3/3 across 3 seeds, no CIs, against k_i=0.005" (a run distinct from the 1-win/1-loss/1-draw of §7 — this one I reproduced in this session under a fixed eval and different seeds; also an example of how much the "appearance" can swing with few seeds). Re-measured with paired scoring, 10 seeds, and bootstrap CIs: **0/10, pooled mean fit negative.** It was small-N, no-CI, seed-dependent noise.
2. **The eval improvement is real but tops out at a draw.** The soft-margin objective stops objective hacking (P is a draw; the scalar C_evaldesign loses at −4.2), and resampling halves the overfit gap (P +3.8 vs fixed C_sham +8.8). It pushes **loss → draw**, but doesn't create a win.
3. **The training gain doesn't transfer.** In every condition, training +3.7 to +9.4 collapses to ≈0 on held-out.

---

## 10. 【The climax】Disproving my own "the referee was weak"

This is the most honest part of the whole thing. Partway through I started to write — **"the original PID (k_i=0.005) was under-tuned. Once I re-tuned it fairly (k_i=0.012), the apparent win disappeared."** A clean story. But **that was wrong.**

After the experiment, I ran a separate check to confirm "is the re-tuned PID really a strong bar?":

```
PID on the TEST lanes: k_i=0.005 → fit 49.16 / soft 0.181
                       k_i=0.012 → fit 49.10 / soft 0.167
```

**On TEST, k_i=0.005 ≈ 0.012 (on soft, 0.005 is even marginally ahead).** In other words, my story that "the original bar was under-tuned" **does not hold on TEST** (that claim was about a different seed set).

The true cause is simpler and more honest: **the apparent win was noise from "thin statistics" (small N, no CIs, seed-dependent), not a "weak referee."** Re-tuning was hygiene worth doing, but it was not the dominant factor.

I then stress-tested the null itself with **4 adversarial skeptics (baseline fairness / leakage / objective hacking / statistical power).** None of them could disprove the null — they got no further than caveats:
- Leakage can only manufacture a "false CONFIRM"; it can't explain the null.
- The soft used at decision time is frozen at w_soft=0 = no objective contamination.
- "Isn't this underpowered, mistaking a real effect for a null?" → If so, 6–8 of 10 seeds should be positive. In fact it's 0/10 plus a negative mean = the opposite of the signature of such a mistake.

I also disclose the honest limits: the PID re-tuning covered only `{k_i, k_pos, k_vel, lean_max}`, with `i_max/kv_z/v_land` fixed. But **sweeping the fixed axes too found no PID that beats the reported bar on TEST** (the bar is near-optimal). And the fitness channel is underpowered (effect size d<0.03) = this means "there is no meaningful win," not "a proof of zero effect."

---

## 11. Lessons (gift to the reader)

- **When "learning beat hand-crafting," the first suspects are a "weak baseline" and "thin statistics."** Not a flashy method or policy capacity.
- **Evaluation design > policy capacity.** Here the headroom lay not in making the RNN bigger but in making the evaluation rigorous — and even then, a fair PID was not surpassed.
- **Doubt your own interim conclusions too.** I once wrote "an under-tuned baseline is the cause," and my own follow-up check disproved it. Aim honest disclosure not only at others but at yourself.
- **A null is a first-class result.** Reporting "it couldn't win" honestly, with the breakdown, is the right starting point for the next experiment.

---

## 11.5. Sequel (in progress): under "gusts," does reactivity favor learning?

The draw experiment used a **sustained (constant) crosswind.** That's the regime where "memory" = the integral (PID's I) helps, which is why hand-crafting was strong. So what about a **time-varying gust** — wind whose direction and strength keep flipping around?

The reasoning: PID's integral is a memory it accumulates to cancel a "constant deviation." But if the wind changes faster than the integral can build, **the integral is always a step behind, firing at the wrong target.** So under gusts it's **reactivity** rather than "memory" that helps — a regime where learning might have a chance.

I add time-varying wind to `onocollo.rocket` (a zero-mean Ornstein–Uhlenbeck process, correlation time ~0.4 s, wobbling smoothly) in a backward-compatible way (`gust_config`, OFF by default so existing behavior is unchanged), and re-test with the same rigorous harness. **What's already clear as groundwork:** re-tuning the hand-crafted PID under gusts, the optimum is **`k_i=0` (= pure PD with no integral)** — **the integral is actively harmful**, and a "reactive" pure PD is the best hand-crafted controller (in contrast to `k_i>0` being better under sustained wind). The hypothesized mechanism is confirmed.

The remaining question: **can a learned reactive policy surpass that reactive pure PD?** I ran the pre-registered primary decision (recurrent full stack, 10 seeds, vs the re-tuned PD, paired with bootstrap CIs).

**Result: another draw (NULL) — even in the regime of reactivity, learning did not surpass hand-crafting.**

- **P_gust (recurrent):** **0/10 seeds positive**, and on all three TEST streams the fitness CI straddles 0 (`+0.6/-0.1/+0.3` = tie). On soft it's even slightly negative (`-0.004/-0.033/-0.036`) — the same "fit is a tie, shaves a little soft" pattern as sustained wind.
- **C_gust_ff (feedforward):** just one stream (s0) lit up positive on both fitness `+4.3[+2.3,+6.2]` and soft `+0.058[+0.008]`, but the other 2 streams were negative on soft, held-out (VAL-DEC) was `-0.88`, and seeds were 0/4 positive — **it fails every gate; not a robust win** (that single glimmer is the kind of "fluke-leaning" result a narrowed search occasionally throws up. Per the earlier lesson, I don't call one such line a "win").

**Conclusion:** in the "reactivity" regime where the integral is harmful, even when the hand-crafted optimum becomes pure PD (`k_i=0`), a learned reactive policy does **not clearly surpass** that pure PD. → **The hand-crafted controller is robust under both sustained wind and gusts.** The prediction that "under gusts, reactivity favors learning" — honestly — **was wrong** (the hypothesized mechanism, that the integral stops helping, was right, but that didn't make learning win).

> For the record, I handled the positive suspicion without hiding it: the single both-positive signal from C_gust_ff s0 fails every one of the other-streams / VAL-DEC / seed-agreement checks and doesn't reach the CONFIRM gate. Had a robust win appeared, the policy is to run it through Phase D adversarial verification before headlining it (`feedback_no_solo_ai_judgment`) — but here there's no "win" to run through.

## 12. To be continued

Beyond the gust experiment above lies **connecting to a world model (V/M/C) and learning to land from pixels** — when the observation becomes a "camera image" instead of a "state vector," does this draw move? And then a **moving pad** — in a regime where reactivity matters even more, does learning stand a chance?

(The code is `onocollo.rocket` = a reusable template of a physics model + an honest fitness env + a hand-crafted baseline + a warm-started evolutionary policy + a CLI + tests + honest docs. New experiments slot into the same shape.)

---

> Note: the source of truth for the numbers is the "The evaluation is the lever" section of `docs/rocket_landing.md`. The experiments are reproduced with `scripts/rocket_eval_experiment.py` + `rocket_eval_aggregate.py`, with results in `out/rocket/eval_exp/`. This article is a draft (publishing is a human decision).
