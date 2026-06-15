---
title: lldarwin / Evolution Arc — Monoculture Evolution / Selection Pressure / Conductor Ensemble / Falsification & Goodhart / Evolution Visualization / Codex Two-Pillar / llcore CPU Evolution × the Third Axis
tags: explainer, evolutionary_computation, llive, FullSense, honest_disclosure
private: false
public_id: e49b7ab9027d93594402
---

# lldarwin / Evolution Arc — Monoculture Evolution / Selection Pressure / Conductor Ensemble / Falsification & Goodhart / Evolution Visualization / Codex Two-Pillar / llcore CPU Evolution × the Third Axis

<!-- TOPICNAV -->
> **🌐 Language**: [日本語](https://qiita.com/furuse-kazufumi/items/6e107c7dfa0c261ee4d7) | **English** | [中文](https://qiita.com/furuse-kazufumi/items/93f3cf1bb7b14650bbca) | [한국어](https://qiita.com/furuse-kazufumi/items/951b94cf66d246723004)
>
> **📚 FullSense Digest Series**
> - [llcore Verification Arc](https://qiita.com/furuse-kazufumi/items/525cd01eda5c1ad707ef)
> - **lldarwin / Evolution Arc（this）**
> - [llive Complete Guide](https://qiita.com/furuse-kazufumi/items/07b686ea311e06027f94)
> - [llmesh Digest](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762)
> - [Plain-Language Digest](https://qiita.com/furuse-kazufumi/items/bdfad6db3f2e70c40511)
<!-- /TOPICNAV -->

## Contents

1. [After Evolving an AI for 500 Generations, Only "Me" and "Karl Friston, the Father of Predictive Coding" Were Left in the World #25 — An Honest Disclosure of Monoculture and the Selection-Pressure Component lldarwin](#chapter-1-after-evolving-an-ai-for-500-generations-only-me-and-karl-friston-the-father-of-predictive-coding-were-left-in-the-world-25--an-honest-disclosure-of-monoculture-and-the-selection-pressure-component-lldarwin)
2. [Measuring with "Glasses" Alone Doesn't Drive Evolution — Design and Measurements of the Selection-Pressure Component lldarwin #26](#chapter-2-measuring-with-glasses-alone-doesnt-drive-evolution--design-and-measurements-of-the-selection-pressure-component-lldarwin-26)
3. [Rebuilding AI Evolution Overnight — The Night a Real-LLM 12h Run Saturated at a Perfect Score Again, and 6 PoCs, 4 Agents, and Perplexity Independently Converged on the Same Conclusion #27](#chapter-3-rebuilding-ai-evolution-overnight--the-night-a-real-llm-12h-run-saturated-at-a-perfect-score-again-and-6-pocs-4-agents-and-perplexity-independently-converged-on-the-same-conclusion-27)
4. [An Ensemble Where a "Conductor" Makes an Ever-Evolving AI Population Play Together — llive's Orchestra-Style Evolution and the 3 Devices That Cured Saturation #28](#chapter-4-an-ensemble-where-a-conductor-makes-an-ever-evolving-ai-population-play-together--llives-orchestra-style-evolution-and-the-3-devices-that-cured-saturation-28)
5. ["When the Lens Saturates, Selection Pressure Is Powerless" — Forging Evolutionary Design Through Falsification #29](#chapter-5-when-the-lens-saturates-selection-pressure-is-powerless--forging-evolutionary-design-through-falsification-29)
6. [The Lineage of "Showing" Evolution #30 — From Conway's Game of Life to 3DGS](#chapter-6-the-lineage-of-showing-evolution-30--from-conways-game-of-life-to-3dgs)
7. [Making an AI Use an AI as Its Subordinate #31 — The "Two Pillars" Development Model of Claude as Lead + Codex as Subordinate](#chapter-7-making-an-ai-use-an-ai-as-its-subordinate-31--the-two-pillars-development-model-of-claude-as-lead--codex-as-subordinate)
8. [(Series #32) llcore CPU PoC battery complete](#chapter-8-series-32-llcore-cpu-poc-battery-complete)
9. [(Series #33) An Over-Tidy Result Is Not a Win, It's an Alarm — The Day We Settled Third Axis ③ with Proper Power](#chapter-9-series-33-an-over-tidy-result-is-not-a-win-its-an-alarm--the-day-we-settled-third-axis-③-with-proper-power)
10. [(Series #34) What Six Rounds of Hill-Climbing Taught Us About "When Does Evolution's ③ Actually Matter" — and How Evolutionary Biology Reached the Same Answer 100 Years Ago](#chapter-10-series-34-what-six-rounds-of-hill-climbing-taught-us-about-when-does-evolutions-③-actually-matter--and-how-evolutionary-biology-reached-the-same-answer-100-years-ago)


---

## Chapter 1 After Evolving an AI for 500 Generations, Only "Me" and "Karl Friston, the Father of Predictive Coding" Were Left in the World #25 — An Honest Disclosure of Monoculture and the Selection-Pressure Component lldarwin

:::note info
**📚 FullSense Knowledge Base** <!-- fullsense-team-kb -->
The full FullSense development history — 60+ articles in 4 languages, with a story-based reading guide, plain-language editions, and 4-panel manga — is consolidated in our Qiita Team **FullSense KB** (team members only).
:::



> 📚 **Series navigation (lldarwin arc)**: #24-05 population evolution → **#25 this article (the monoculture failure)** → #26 design edition → #27 climax (real-LLM saturation → open-ended pivot). ※ Each article reads on its own (links are for navigation).

> **Concept hook**: Into llive's derived-population evolution, I sowed 8 lineages
> of human personas as "seeds": Furuse (= me), Friston, Millidge, Isomura, Oka
> Kiyoshi, Grothendieck, von Neumann, and Feynman. Eight of the world's
> representative intellects — who, after fighting through 500 generations, would
> survive?
>
> The result: the only survivors were **me (52%) and Karl Friston, the father of
> predictive coding (48%) — just two**. Oka Kiyoshi, Grothendieck, von Neumann,
> and Feynman — **not a single one left any descendants; they all went extinct.**
>
> …Sounds like a moving tale of evolution? **No. This is a record of a major
> failure.** Evolution did not "select the strong"; rather, **because the
> selection pressure was zero, the population merely skewed toward 2 lineages by
> sheer luck (genetic drift)**. This article is an honest disclosure of that, plus
> the design story of the component needed after "measuring (lleval)" — namely
> "culling (lldarwin)".

---

### 0. The plot in three lines (the "intro" as in rakugo)

- **What I did**: I injected 8 intellects as persona seeds into llive's
  derived-population evolution and ran it for 500 generations with rich-proxy
  evaluation.
- **What happened**: At generation 1, best_score **stuck at 1.0**, and stayed a
  perfect score ever after. The 8 lineages converged to just 2 — **Furuse 52% /
  Friston 48%** — and the remaining 6 went extinct.
- **The true cause**: "Perfect scores kept appearing" = **selection pressure was
  zero**. Since the fitness is the same no matter who you pick, evolution had
  effectively become a dice roll (genetic drift).

In short, **"I tried to decide rankings on a test where everyone scored 100"**.
Of course who passes becomes a lottery. The test is bad. The glasses (lleval)
were fogged up.

---

### 1. Why sow "people" as seeds?

llive's evolution layer (v0.B–v0.F) is not about making a single LLM smarter;
it is **derived-population evolution in which N llive individuals (genomes)
undergo generational turnover and evaluate each other** (detailed in series
#24-05).

The mechanism that injects "thinking habits" into that genome as an initial
condition is **PERSONA_FX**. Like "Friston, who observes the world through
predictive coding" or "Oka Kiyoshi, who builds mathematics up from silence and
emotion", we **map the cognitive style of a real intellect onto the genome's
factor_affinity (its bias toward thought factors)** and sow it as a seed
(founder).

The 8 lineages I sowed:

| founder | seed of cognitive style |
|---|---|
| Furuse (me) | provenance-oriented / tracing to the source / reality link |
| Karl Friston | predictive coding / free-energy minimization |
| Beren Millidge | implementation-oriented active inference |
| Isomura | (user-specified persona) |
| Oka Kiyoshi | emotion / holistic intuition / accepting uncertainty |
| Grothendieck | abstraction / generalization / discovery of structure |
| von Neumann | formalization / computation / multi-domain crossing |
| Feynman | recomposition / first principles / intuitive verification |

> 🍵 **A break**: If you now picture "8 geniuses thrown into a VR battle royale",
> you're good. The problem is that the **rules (the evaluation function) of this
> battle royale were broken**. The main topic starts in the next section.

---

### 2. The result — only 2 survived

The lineage occupancy after 500 generations (the breakdown of
max_lineage_share):

```
Furuse         ████████████████████████████  52%
Friston        ██████████████████████████    48%
Millidge       (extinct)
Isomura        (extinct)
Oka Kiyoshi    (extinct)
Grothendieck   (extinct)
von Neumann    (extinct)
Feynman        (extinct)
```

At first glance you could write a **narrative** that "predictive coding (Friston)
and provenance-orientation (Furuse) beat abstract mathematics (Grothendieck) and
formal computation (von Neumann)".

On social media, "I evolved an AI and predictive coding turned out strongest"
might even go viral. **But not doing that is FullSense's honest-disclosure rule**
([[feedback_benchmark_honest_disclosure]]). When an abnormally clean result
appears, doubt the breakdown before feeling like you've won.

The result of that doubt is the next section.

---

### 3. The true cause — "perfect-score inflation" erased the selection pressure

#### 3.1 Symptom: best_score is 1.0 from generation 1

Looking at the log, **best_score was already 1.0 at generation 1**. After that it
stayed 1.0 for all 500 generations. In evolutionary computation, fitness
immediately saturating (plateauing) is a classic danger sign.

Selection (culling) is the operation of "choosing parents by the difference in
fitness". But if **everyone scores perfectly**, no fitness difference arises.
Without a difference, both tournament selection and roulette selection
**degenerate into effectively random selection**.

This is the state of **zero selection pressure**. Evolution stops, and after
that the population just skews on its own via **genetic drift**. The shrinking
from 8 lineages to 2 was not "because they were strong" — it was **merely a
probabilistic absorption**.

> 🤔 **An analogy (manzai style)**:
> Boke: "When I held an election for class rep in a class where everyone scored
> 100, the vote split and came down to 2 people…"
> Tsukkomi: "That's not an election, that's drawing lots!"
> — What happened to evolution is exactly this "turning into a lottery".

Here, let me treat "genetic drift" a bit more carefully. In biology, it is the
phenomenon that **a neutral gene under no selection pressure has its frequency
skewed by chance alone as generations pass**. Even if you release goldfish of 8
colors into a small pond, if none of them are eaten, after several generations
**the 2 colors that happened to increase** dominate the pond. Not because they
were strong, but because that's how the dice fell. This time's 8→2 was exactly
this "goldfish-scooping pond" state.

> 🤔 **An analogy (rakugo style)**:
> "Hey Hacchan, how about we roll a die 500 times and pick the boss by the number
> that came up most?"
> "That ain't skill, that's just gambling."
> "Exactly. Making evolution gamble is the real identity of this failure."

#### 3.2 Root cause: the double collapse of the evaluation function `fitness_rich`

Why did perfect scores keep appearing? Tracing the code, `fitness_rich` (the
rich-proxy evaluator) had **2 design flaws**.

**Flaw 1 — factor_affinity was made identical across all layers**
A genome is supposed to have individuality as a 2-dimensional matrix of "thought
factor × memory layer". But at archetype generation, `np.tile` **replicated
factor_affinity with the same value across all memory layers**. The per-layer
difference — half of the individuality — was crushed before it even entered the
evaluation.

**Flaw 2 — "nearest" was collapsed into a single scalar via `max(sims)`**
The closeness between an individual and an archetype was extracted from the
similarity vector against multiple archetypes via **`argmax` (= just the single
maximum value)**. It looks only at "which genius it most resembles" and throws
away all of "how it differs from the other geniuses". As a result, resembling
any of them even slightly yields a high score → **it immediately sticks to the
ceiling**.

```
What it should be: pressure profile = [typicality, diversity, specialization, ...] ← multi-axis vector
Actual impl:       fitness = max(similarity of individual to each archetype)        ← single scalar
                              ↑ collapsed by argmax = multi-objectiveness vanishes
```

In other words, **"what should have been measured with multiple yardsticks was
scored only by the maximum of a single yardstick"**. The glasses (lleval) had
only one lens, and it was a coarse lens that immediately swings to a perfect
score.

> 🍵 **A break**: This is the climax of this article. The problem is not that
> "the result was skewed"; if you notice the two-tier structure that **"the cause
> that skewed the result was the collapse of the evaluation function"**, you've
> essentially finished reading this article. The rest is "so how do we fix it".

---

### 4. The countermeasure — after "measuring" comes "culling": lldarwin

The llive family already has **lleval (the glasses = the evaluation framework,
series #24-08)**. What we learned this time is that **even if the glasses can
"measure" the differences, evolution breaks unless that difference is correctly
converted into "who survives"**.

So we designed a new member, **lldarwin (the selection pressure = the culling
component)**. The division of roles in the ll- family becomes:

```
lleval   = measure (convert an individual's behavior into a multi-axis pressure profile)
lldarwin = cull    (convert that profile into "the parents of the next generation")
```

#### 4.1 The core of the design — a selection pressure that "does not aggregate"

The essence of this failure was **"aggregating multiple axes into 1 scalar and
applying argmax"**. So lldarwin's first principle is **multi-objective culling
that does not aggregate the multiple selection pressures**.

The 3-layer fusion we adopt (selected by traversing 616 evolutionary_computation
items via rad-research):

1. **ε-lexicase selection** — apply the evaluation axes one at a time,
   independently and in order. A specialist that excels on one axis (mediocre on
   the others) can also survive → **the multipolar structure is automatically
   maintained**. If Grothendieck is #1 on the "abstraction axis", he won't
   disappear even if he's mediocre on the others.
2. **minimal-criterion QD (MAP-Elites)** — keep an elite per cell of the behavior
   dimension. **As long as even 1 cell survives, there is no total wipeout** =
   making monoculture structurally impossible.
3. **down-sampling** — each generation, use only a subset of the evaluation
   cases. Because the target moves, you cannot stick to a specific peak →
   **destroying the plateau (perfect-score inflation)**.

To these we add a minimal-criterion gate (separating eligibility to reproduce by
"does it meet the minimum criterion" rather than a continuous rank = suppressing
winner-take-all) and per-dim z-score standardization (so "high average on all
axes" = the featureless doesn't gain an advantage).

#### 4.2 Make "what LLMs are bad at" the selection pressure

Another policy is to choose, as the pressure, **axes that LLMs/VLMs are actually
weak at and that are measurable** (avoiding domains that can't be verified). For
example:

| pressure | what LLMs are bad at | proxy / real |
|---|---|---|
| typo_robustness | consistency under typos / noisy input | proxy OK (synthetic typo injection) |
| polysemy_wsd | context-dependent understanding of polysemous words | proxy OK (WSD bench) |
| multistep_robustness | cascade error in multi-step reasoning | proxy OK |
| calibration | confidence estimation (token confidence ≈ random) | proxy OK |
| visual_qa | image recognition / visual hallucination | real VLM required (later Stage) |

The separation of measurement purity — PoC from axes measurable by proxy, real
LLM/VLM axes in a later stage — is also baked into the design from the start
([[feedback_llive_measurement_purity]]).

#### 4.3 Monitor for total wipeout — SPC alarm

FullSense's core idea is **SPC (statistical process control)**. In lldarwin too,
we record `max_lineage_share` / archive growth / behavioral diversity every
generation, and **detect a monoculture ratio > 0.8 with an SPC_ALARM** to
automatically adjust the cadence and parameters. The goal is to make this time's
"8→2" structurally impossible to recur.

---

### 5. Lessons (left as honest disclosure)

- **An abnormally clean result (best=1.0 instant saturation, convergence to 2
  lineages) is not a victory but an alarm.** When we doubted the breakdown, the
  winners turned out to be a mirage produced not by ability but by the flaw in
  the evaluation function.
- **"Measuring" and "culling" are different things.** Even if the glasses
  (lleval) can measure the differences, culling breaks if you crush that
  difference into one with argmax. The culler (lldarwin) must not aggregate.
- **Do not erase failure.** We will not discard this 500-generation run; after
  wiring up lldarwin, we will use it as a **baseline** to verify by re-running
  whether "Oka Kiyoshi, Grothendieck, and the others survive". Whether 8→2
  improves is the first pass/fail criterion.

> **Next-time preview**: We will implement lldarwin's PoC Stage 0 (proxy axes +
> ε-lexicase wiring + QD archive) and re-run the same 8 founders. Can Oka Kiyoshi
> survive this time, for real? We're going to overwrite the world line of "only me
> and Friston are left in the world".
> (The design details continue in #26; the honest disclosure where I throw my own
> counter-evidence at that design continues in #27.)

---

### 5.5. The 2-tier structure of "the glasses" and "the culler" — why separate them (a deep dive)

The conceptual diagram I most want you to take away from this article is this:

```
individual ──▶ [ lleval = glasses ] ──▶ pressure profile (multi-axis case vector)
                                              │
                                              ▼
                  [ lldarwin = culler ] ──▶ parents of the next generation
```

The essence of #25's failure is that **both** of these two tiers were broken:

- **Failure on the glasses side**: `fitness_rich` crushed multiple axes into 1
  scalar with `nearest = max(sims)`, and on top of that hit a perfect score
  immediately. → It isn't measuring (glasses that can't see the difference).
- **Absence on the culler side**: the non-aggregating multi-objective culling
  (ε-lexicase / QD) **was never wired in to begin with**. → It can't cull (no
  filter).

The important point is that **fixing either one alone does not restore
evolution**. Inserting a high-grade culler into saturated glasses still can't
cull a "zero difference", and fixing only the glasses without a good culler still
can't make use of the profile. **"Measuring" and "culling" are different failures
and must be fixed separately** — this is the bridge from #25 to #26.
(The counter-evidence that "merely upgrading the culler without fixing the glasses
is useless" is dealt with head-on in #27.)

> 🍵 **A break**: In the photography metaphor, lleval is the "light meter" and
> lldarwin is "which shot to adopt". You can't make an album if the light meter is
> broken, and you can't make an album without adoption criteria either. You need
> both.

---

### 5.6. Diagram ideas (candidates to turn into SVG before posting)

Diagrams I'd like to prepare to make this article "captivating through motion"
(to be turned into SVG before posting):

1. **Lineage-occupancy collapse animation** — an animated SVG in which 8 lineage
   bands get absorbed into 2 along the generation axis (the goldfish-pond
   metaphor).
2. **best_score = 1.0 instant-saturation graph** — a flat line that sticks to the
   ceiling at generation 1 (zero selection pressure at a glance).
3. **The argmax-collapse diagram** — a before/after where the multi-axis vector
   `[typicality, diversity, specialization, ...]` is crushed into a single bar by
   `max()`.
4. **The 2-tier structure diagram** — the "glasses → culler" of §5.5 animated as a
   hero diagram.
5. **The ll- family role diagram** — the relationship of lleval (measure) /
   lldarwin (cull) / llive (individual) in a single picture.

> These are planned to ride on the animated-SVG expression layer (declarative
> animation → SMIL) of [[project_fullsense_animemd_branch_token_viz]].

---

### 6. Related

- Series #24-05 "AI that learns as a population" — an overview of
  derived-population evolution (the premise of this article)
- Series #24-08 "Making the glasses" — lleval (the measuring side)
- Series #26 "The design of lldarwin" — the culler's multi-objective culling /
  ε-lexicase / QD (the continuation of this article)
- Series #27 "When the glasses fog up, culling is powerless too" —
  counter-evidence investigation / Goodhart's law (honest disclosure)
- Design doc: lldarwin (the culling side) — the source material of this article
- Related memory: [[feedback_benchmark_honest_disclosure]] /
  [[feedback_llive_measurement_purity]] / [[project_persona_genome_integration]]

---

<!-- TODO(before posting): hero SVG / theme SVG / progress badge / Qiita URL cross-links for #24-05・#24-08・#26・#27 -->

---

---

## Chapter 2 Measuring with "Glasses" Alone Doesn't Drive Evolution — Design and Measurements of the Selection-Pressure Component lldarwin #26

:::note info
**📚 FullSense Knowledge Base** <!-- fullsense-team-kb -->
The full FullSense development history — 60+ articles in 4 languages, with a story-based reading guide, plain-language editions, and 4-panel manga — is consolidated in our Qiita Team **FullSense KB** (team members only).
:::



> **Concept hook**: In the previous article #25, I exposed a massive failure: "When I evolved an AI for 500 generations, the only ones left in the world were **me and Friston**."
> Oka Kiyoshi, Grothendieck, von Neumann — all of them quietly vanished mid-evolution. The cause: the evaluation function (the glasses = lleval) kept handing out perfect scores, so **the selection pressure dropped to zero**. Even if you can "measure" who is superior, if you can't convert that difference into "who survives," evolution degenerates into mere genetic drift.
>
> So then — granting that the glasses let us "measure" the differences, how do we build the device that **correctly converts** those differences into "selection"?
> That is the star of this article, **lldarwin**. A new member of the ll- family, it is the component **specialized in selection (selection pressure)**.
>
> The one keyword I want you to remember from this article is a single word: **"don't aggregate."** The moment you add multiple rulers together into one, evolution breaks. Why that happens, and how I overcame it with measurements — picking up from the failure, this time I'll tell a story about something that **actually worked**.

---

### 0. The gist in three lines (the rakugo "pillow")

In rakugo, there's a "pillow" before the main story. First, the whole picture in three lines.

- **lleval measures, lldarwin selects** — evolution only becomes meaningful as a two-stage structure of "measuring" and "selecting."
- The first principle of selection is **multi-objective selection that does not aggregate multiple selection pressures**. Here we structurally cut off the true cause of #25's failure (collapsing it with the argmax of a single scalar).
- The three adopted pillars = **ε-lexicase + minimal-criterion QD + down-sampling** (selected by surveying 616 documents in the evolutionary_computation corpus).

And this time, the difference from #25 is that there's not just the skeleton but **actual measurements**. With novelty pressure I doubled behavioral diversity from 7.12 → 14.88 (+109%), with the **neutral reservoir** I actually **revived every one** of the "extinct Oka Kiyoshi / Grothendieck lineages," and finally, against a **real on-prem LLM (llama3.2)**, I evolved prompt strategies and improved a weak task from 0.0 → 1.0. Let's go through it in order.

---

### 1. Why separate "measuring" and "selecting"

The llive family already has **lleval (the glasses = the evaluation framework, series #24-08)**. It is a device that observes an individual's behavior and scores it along multiple axes.

But what #25 revealed was a fatal truth. **Even if you can measure differences with the glasses, if you collapse those differences into one with argmax, selection breaks.** Concretely, `fitness_rich` was folding multiple archetype similarities into a single scalar via `nearest = max(sims)`. This is the SEL-2 violation — the true cause of "best=1.0 saturates, everyone gets a perfect score, and the selection gradient disappears."

If we clearly divide the roles, it looks like this.

```
lleval   = measure (converts an individual's behavior into a "multi-axis pressure profile")
lldarwin = select  (converts that profile into "the parents of the next generation")
```

The output of `lleval` is a **case vector** (an array of scores along each axis). `lldarwin` receives it as an input contract and selects **without aggregating**. This is exactly the boundary of responsibility between them. If lleval hands over the data after "adding the axes into one," lldarwin can do nothing. So on the lleval side we impose the contract: "you must always keep and pass the breakdown (the per-axis decomposition)."

lldarwin's `Pressure` interface is expressed by the following minimal contract.

- `name` — the name of the axis (`typo_robustness`, etc.)
- `evaluate(individual_output) -> case_scores: list[float]` — converts an individual's behavior into a "per-axis score array"
- `is_proxy: bool` — whether it is a proxy measurement or a real LLM/VLM measurement (the distinction of measurement purity)
- `minimal_criterion: float | None` — the minimum reproduction criterion for that axis (no gate if None)

The point is that the return value of `evaluate` is **a list, not a scalar**. Within a single axis there are multiple cases (test cases), and we pass them to lldarwin without collapsing them. This "don't collapse" design is the foreshadowing that will rescue the specialist later.

> 🍵 **Break point**: The meaning of separating the glasses (lleval) and the filter (lldarwin) is, in photography terms, the difference between "metering exposure" and "deciding which shot to adopt." Even if the light metering is perfect, if you choose the best shot wrongly the album is ruined. Even if the light meter (lleval) tells you "this one is 80 for brightness, 30 for composition, 95 for expression," whether you round it to "average 68" and discard it, or "keep the one with 95 expression in a separate slot," changes the richness of the album as much as heaven and earth. lldarwin is the specialist in "adoption decisions." If you make the measurer and the chooser the same person, usually both turn out sloppy.

---

### 2. The core of the design — the "don't aggregate" 7 stages

lldarwin selects the pressure profile (the multi-axis case vector) received from lleval through the following 7 stages. To each I attach "why it is needed = which failure it prevents."

1. **Standardizer** — per-dim z-score. It does not favor the featureless honor student who is merely "uniformly high across all axes," and instead turns the **deviation** on each axis into selection pressure. Central agreement (being the same as everyone) is excluded.
   - *Failure prevented*: the entrance to monoculture, where the mediocre who are "merely high on average" win and sharp individuals disappear.
2. **MinimalCriterionGate** — splits reproduction eligibility by a minimum criterion on each axis. Does not let a "winner-take-all" happen by continuous ranking alone.
   - *Failure prevented*: the total-wipeout scenario where a single strongest one monopolizes all reproduction slots. By a "minimum guarantee" that lets anyone who meets the criterion reproduce, the foundation of diversity is preserved.
3. **EpsilonLexicaseSelection** — evaluates the axes one by one independently as cases. A specialist that stands out on some axis (mediocre on others) can survive.
   - *Failure prevented*: the extinction of specialists by aggregated argmax. This is the very mechanism that produced #25's 8→2.
4. **QD / MAP-Elites archive** — converts the pressure profile into a behavior descriptor and keeps an elite per cell. The archive grows monotonically.
   - *Failure prevented*: structural total wipeout. As long as even one individual remains in one cell, that behavior does not disappear.
5. **Niching / FitnessSharing** — down-weights individuals in the same niche so multiple peaks can coexist.
   - *Failure prevented*: aggregation onto a single peak (monoculture).
6. **Down-sampling** — every generation, evaluates only on a subset of cases to perturb the environment.
   - *Failure prevented*: over-adaptation to a specific peak and a plateau (a stagnation plateau). By making it a moving target, it forbids "winning the same way."
7. **NoveltyScorer** — when stagnating, applies exploration pressure toward "behavior different from the past."
   - *Failure prevented*: exploration exhaustion. When improvement stops, it rewards novelty itself to push outward.

Contrasting with #25's 8→2 monoculture, the core is the three: **(3) ε-lexicase, (4) QD archive, (2) minimal-criterion**. In #25 these were all missing and only the single-scalar argmax was running. So "the one lineage strongest on average" took all the continuous ranking, and the rest disappeared by drift. By "bundling these three without aggregating," lldarwin builds a structure that does not break down even as generations accumulate.

> 🤔 **An analogy (manzai style)**:
> Boke: "I added up all the test scores and ranked them, and only honor students with high averages were left."
> Tsukkomi: "That's zero diversity! The genius with 100 in math and 0 in everything else has vanished!"
> Boke: "Well, looking at the total, the honor student is higher..."
> Tsukkomi: "**Don't look at the total!** If you look at the subjects one by one, that genius loses to no one on the 'math' case. ε-lexicase is the mechanism that rescues that. The moment you sum, the genius dies."
> — Summing (aggregation) kills the specialist. Because ε-lexicase "looks at the subjects one by one," the sharp ones survive. This is the very first principle of lldarwin.

---

### 3. Why these 3 pillars (the rad-research backing)

As the strongest candidate fusion that "does not break down even as generations accumulate," I selected it by surveying 616 documents in the evolutionary_computation corpus. The provenance matters: I did not invent it myself, but selected and bundled the "don't aggregate" lineage of existing research.

| Method | Effect | Source |
|---|---|---|
| **ε-lexicase** | specialist preservation, high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | total wipeout impossible thanks to per-cell elites | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | environmental perturbation, cost reduction | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | prevents premature convergence (future option) | Lyu 2020 (2005.07376) |

The three pillars look like disparate methods, but in fact they can be skewered by **one single idea: "don't aggregate."** ε-lexicase "does not aggregate the axes." QD "does not aggregate the behavior space (keeps it per cell)." Down-sampling "does not fix the evaluation environment (perturbs it every generation)." Each shares the same philosophy in not "rounding into one." So even when combined, the ideas do not clash and instead synergize.

> 🍵 **Break point**: People ask, "Why not invent it yourself?" The answer is simple: **because the combination of existing research is strong enough**. My development rule ([[feedback_originality_over_imitation]]) says: "The adoption of external algorithms is **selection**, not coverage. Exclude breakdown risk and mere imitation, and adopt only what adds value to the original design." lldarwin's originality is not "having invented a new selection algorithm," but "**the way it bundles these without aggregating**, and **actually wiring** that into llive's evolution loop." In cooking terms, it's not creating the world's first ingredient, but the craft of "plating famous existing ingredients on one dish without mixing them." Ingredients that would be ruined if mixed are made to coexist without mixing.

---

### 4. Stage1 — doubling behavioral diversity with criteria exclusion + novelty pressure

From here it's measurements. In Stage1, rather than implementing the whole design at once, I put in only the two changes most likely to be effective and measured (llive, branch `optimize/core-2026-05-20`, commit `8060204`).

**Change 1: criteria exclusion.** From the cases of ε-lexicase, I removed `factor_score` (= the single scalar of max-archetype = argmax, the very cause of #25's best=1.0 saturation) and `nearest_persona_idx` (= a category index with no meaningful ordering). This is a cleanup that "removes bad rulers from the material used to judge selection."

**Change 2: novelty pressure.** I enabled `MultiPressureSelector(use_novelty=True)`. Every generation it computes the k-NN average distance to the archive of past generations (Lehman-Stanley style novelty), z-scores it within the population (STD-1), and mixes it into selection as an additional lexicase case. It evaluates "behaving differently from everyone else" itself as one of the axes.

For tests, I expanded `tests/unit/test_evolutionary_lldarwin.py` from 8 → 10 (adding exclusion and novelty preservation). 847 evolution-system tests green, no regression.

The measurement conditions are rich-proxy, 8 founders + pop24, 150 generations, seed 0. The results are below.

#### 4.1 Behavioral diversity (diversity_l2) — the metric where novelty works

| Condition | mean | tail30 min | final |
|---|---|---|---|
| BASELINE (pre-exclusion, old lldarwin equivalent to Tournament) | 7.12 | 0.68 | 0.83 (collapse) |
| A: criteria exclusion only | 9.16 | 1.57 | 1.57 |
| **B: exclusion + novelty** | **14.88 (+109%)** | **6.56 (9.6×)** | **11.73 (collapse avoided)** |

Novelty pressure maintained behavioral (genome-space) diversity at about double, and prevented the late-stage diversity collapse. Criteria exclusion alone is also effective on its own (to the extent it removes spurious argmax pressure). Whereas BASELINE **collapses** at final 0.83, condition B **holds its ground** at final 11.73. This is the first tangible sense of the "don't aggregate" design.

![Fitness and diversity of the Stage1 baseline (no novelty). Diversity collapses in the late stage](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_en.svg)

![Stage1 with novelty. Diversity is maintained until the late stage](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_en.svg)

Placing the two side by side, the difference in late-stage behavior is clear at a glance. Whereas the baseline's diversity curve sticks to the floor, the one with novelty runs to the finish while keeping a high level.

> 🍵 **Break point**: To liken novelty pressure to a goldfish pond — if you keep only the goldfish swarming around the food (high fitness), eventually you get a pond where everyone moves the same way in the same place. Novelty pressure is the role that "**gives a bonus to goldfish swimming in different places from everyone**" too. As a result, you get a pond scattered everywhere, one you never tire of watching. But don't let your guard down here. In the next section, a **pitfall** lurking in this "lively pond" is discovered.

---

### 5. honest disclosure (most important) — I had been confusing behavioral diversity and lineage survival

This is the most important section of this article. Just because a good number (+109%) came out does not mean I get to feel like a winner — this is my iron rule ([[feedback_benchmark_honest_disclosure]]). I doubted the breakdown. And I found a mistake.

#### 5.1 Lineage fixation (founder_counts) — the metric novelty does not improve

In the same measurement, I look at a different metric. "Of the 8 founders (ancestral lineages), how many lineages survived to the end?"

The result — **in all conditions, it ultimately converged from 8 → 2 lineages** (furuse-kazufumi + friston). oka-kiyoshi (Oka Kiyoshi) / grothendieck (Grothendieck) / von-neumann / feynman / millidge / isomura all **went extinct**.

Even though I put in novelty and doubled behavioral diversity, **the lineage survival was exactly the same 2 lineages as #25**.

#### 5.2 Why — I had been confusing two kinds of "diversity"

The TODO in the design document (as of #25) said "verify in a re-run whether the Oka Kiyoshi / Grothendieck lineages survive." This was **confusing behavioral diversity with lineage survival**.

The author's comment in `poc_evolution_env.py` (L129-132) pins down this confusion precisely.

> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs QD niching on lineage / PERSONA-FX, not pure novelty**"

Broken down, it's this.

- The demonstrated monoculture 0.05 is **behavioral** (the occupancy rate of archive cells), not **lineage-based**. What novelty/lexicase improves is "the spread of behavior," not "the survival of ancestors."
- That lineage fixation heads toward monoculture by neutral drift (Motoo Kimura's neutral theory of evolution) is **theoretically normal**. It is not collapse. Both novelty and lexicase have only mechanisms that **preserve existing individuals**, and have **no mechanism to revive a lineage that has once gone extinct**. So lineage fixation cannot be stopped structurally.
- Furthermore, the inter-archetype distances are also compressed at 0.068–0.29 (similarities densely packed in 0.71–1.0), so the selection gradient is weak and drift dominates. friston is the most non-central (centroid distance 0.162) yet survived = it was not centrality (strength) but **luck (drift)** by which the 2 lineages fixed.

In other words — my wish that "I want Oka and Grothendieck to survive" was a disease that **the medicine of raising behavioral diversity can absolutely never cure**. I had the wrong medicine. This is a lesson worth recording honestly.

> 🍵 **Break point**: Put in manzai terms.
> Boke: "I increased the goldfish that move in colorful ways in the pond! Diversity is perfect!"
> Tsukkomi: "And the **bloodline**? Of the 8 goldfish families that existed, how many are left?"
> Boke: "...two."
> Tsukkomi: "The movements are flashy but the family tree is threadbare! Diversity of movement and diversity of bloodline are **separate matters**!"
> — "Behavior is diverse" and "lineage is diverse" are entirely different metrics that merely look alike. I had been confusing them. I expose it honestly.

---

### 6. Stage1.5 — reviving extinct lineages with a neutral reservoir

Once you understand the true nature of the disease, you can change the medicine. What lineage survival needs is "a mechanism to re-inject extinct lineages every generation" — a **lineage-niched neutral reservoir**.

#### 6.1 First, confirm the mechanism with a PoC

Rather than remodeling the production loop right away, I first confirmed the mechanism runs with a standalone PoC ([[feedback_poc_feasibility_first]] = requirements → PoC → feasibility → detailed design, llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`).

Selection reuses Stage1's `MultiPressureSelector` (criteria exclusion + novelty). Fitness is rich-proxy. Lineage is inherited from parent_a. **The reservoir = keeps the best-ever genome per lineage and re-injects extinct lineages every generation** (replacing low-score children; the best is not destroyed). I measured with 8 founders + pop24 + 150 gens + seed 0.

| reservoir | final named lineages | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1** (oka-kiyoshi 24/24 = complete monoculture) | 1.00 | 1.58 |
| **ON** | **8 (all founders survive)** | **0.31 (≪ 0.8 OE-3)** | 1.69 |

With reservoir ON, **all 8 lineages survived**, including Oka (oka) and Grothendieck (grothendieck). The final shares are friston 7 / furuse 6 / grothendieck 4 / oka 3 / the other 4 lineages 1 each. The ideal behavior: **strong lineages reproduce with descendants, while weak lineages are kept alive by the reservoir**. Behavioral diversity also did not drop (1.69 vs OFF 1.58).

**Honest caveat (PoC stage)**: Because the reservoir re-injects frozen elites (frozen representatives), the "survival" of weak lineages (1 individual each) is due to re-injection, not active evolution. This is legitimate per the very definition of a neutral reservoir (keep representatives and make them recombinable), but I do not claim "weak lineages keep actively evolving."

#### 6.2 Integration into the production EvolutionLoop (additive + default-off)

Since the mechanism was confirmed by the PoC, I integrated it into the production `EvolutionLoop` (commit `b03cbda`). The crux of the design is **additive and default-off** — it changes none of the existing behavior, and becomes active only when the flag is set. I defended backward compatibility to the death.

- Added the `EvolutionLoop.on_population_bred` hook (can transform the bred list right after breeding, before evaluation; default None = backward compatible).
- `LineageReservoir` (`lineage_reservoir.py`): ancestor tracking (inheriting parent_ids[0]) + per-lineage best-ever retention + re-injection of extinction-protected lineages. It shares `founder_map` and stays consistent with the lineage log.
- Added `run_persona_evolution(lineage_reservoir=True)` / the run-script flag `--lineage-reservoir`.
- tests: `test_evolutionary_lineage_reservoir.py` 6 + evolution-system **937 green** (no regression).

Measurement in the real EvolutionLoop (rich-proxy + lldarwin + novelty, 8 founders / pop24 / 150gens / seed0).

| Condition | named lineage survival | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8 (furuse 17 + friston 7) | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8 (all lineages)** | **0.33** | **0.29 (≪ 0.8 OE-3)** | 9.20 |

**All 8 lineages survived in the real loop**, including Oka (oka 3) and Grothendieck (grothendieck 1). The production implementation reproduced the PoC's prediction (fixation 0.31) at 0.29 — proof that the mechanism worked as designed.

This is the biggest highlight of this article. Compare the two below.

![Neutral reservoir OFF. The lineage-dominance stream ultimately collapses to 2 lineages, furuse 71% / friston 29%](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_en.svg)

![Neutral reservoir ON. All 8 lineages (millidge / von-neumann / oka / grothendieck, etc.) coexist](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_en.svg)

OFF (top): as generations advance, the stream gets swallowed into 2 colors — a reproduction of #25's "only me and friston remained." ON (bottom): 8 colors remain as bands until the end. Neither Oka nor Grothendieck has disappeared.

![Fitness and diversity with the neutral reservoir ON](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_status_en.svg)

> 🍵 **Break point**: That lonely world I lamented in #25, "only me and Friston remained." This time it has changed into a lively world where Oka, Grothendieck, and von Neumann are all present. **This is not fabrication; it is a result that actually ran** (following [[feedback_benchmark_honest_disclosure]], I write neither false failures nor false successes). But — before getting carried away, recall the attitude learned in §5. "When a good number comes out, doubt the breakdown." In the next §6.3, I honestly write that this success too came with a **cost**.

#### 6.3 Honest caveat — lineage retention and behavioral diversity are a weak trade-off

With reservoir ON, all lineages survived. But look closely and **diversity_l2 drops from 14.88 → 9.20**. Because frozen elites (frozen representatives) are re-injected every generation, the spread of genome space decreases somewhat.

However, the collapse when OFF (final 0.83) is avoided. In other words, it's a **weak trade-off** relationship: "if you take lineage retention, the peak of behavioral diversity drops a little, but collapse can be prevented." It is not zero-cost magic. I write this honestly. And how far this cost can be minimized becomes the subject of the next sweep.

---

### 7. Re-injection frequency sweep — a non-trivial discovery of a non-monotonic optimum

I characterized §6.3's honest caveat (frozen elite re-injection lowers diversity) with a sweep of `reinject_interval` (the generation interval at which re-injection is performed; default 1 = every generation) (commit `da93dd3`). I added `LineageReservoir.reinject_interval` + the `--reinject-interval` flag (7 tests). 8 founders / pop24 / 150gens / seed0.

| interval | named survival | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1** (every generation) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84 (max)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**Here there was a non-trivial discovery.** Intuitively, you'd expect that "the more you reduce re-injection (raise the interval), the less the frozen elites are pushed in, and diversity recovers monotonically," right? But — **diversity did not increase monotonically; it peaked at interval=5** and actually dropped at 10/20.

When you think about the reason, it makes sense. If you leave the lineages alone too much (the interval is too large), (a) the diversity injection originating from the reservoir decreases, and (b) a few lineages fix, so in the end diversity doesn't grow either. Both "re-injecting too much" and "leaving alone too much" are bad, and there is an optimum in between. This is a finding that **could not have been predicted without actually running the sweep**.

The operational guideline became this.

- If you **prioritize lineage retention above all** → interval=1 (8/8 all lineages survive).
- If you want to **also achieve behavioral diversity** → interval=5 (retains 5/8 while maximizing diversity).

The optimum for achieving both depends on the fitness design and the population size, so in production I re-calibrate it with a sweep.

![The trade-off of re-injection frequency. Lineage retention and behavioral diversity are inversely related, and diversity peaks at interval=5 (non-monotonic)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_en.svg)

> 🍵 **Break point**: Like the sage (punchline) of a rakugo, there is a "twist that betrays expectations" here. I thought "the more you do it the better," but it was "do it too much and it backfires." Same as watering plants: water too little and they wither, water too much and the roots rot. The optimum is in moderation. When you do evolutionary computation, you meet these "non-monotonic curves" again and again. That's why you measure baselines and run sweeps. Intuition is often betrayed.

---

### 8. Stage2 first half — making "the LLM's weaknesses" into selection pressure by proxy

Up to here I confirmed the mechanism with rich-proxy (a heuristic based on persona similarity). Next I implement another pillar of the design: **making "axes where the LLM/VLM is actually weak, and which are measurable" into pressures** (a series of commits, `pressures.py`).

I made the 5 proxy-capable axes listed in design §3 into plugins.

| pressure (LLM weakness) | related thought factors (case) |
|---|---|
| typo_robustness (noise tolerance) | consistency / reality_link / uncertainty |
| polysemy_wsd (polysemous words) | multiview / consistency / reality_link |
| multistep_robustness (multi-step reasoning) | structurize / closed_loop / self_extend |
| calibration (confidence estimation) | uncertainty / provenance |
| context_management (irrelevant-context tolerance) | consistency / provenance / recompose |

`make_pressure_fitness()` outputs the cases of each pressure (14 in total) into the breakdown, and lldarwin's ε-lexicase **selects specialists per axis without aggregating**. Added `--fitness pressure-proxy`. tests `test_evolutionary_pressures.py` 4 + evolution-system **942 green**.

End-to-end measurement (pressure-proxy + lldarwin + novelty + reservoir, 8 founders / 120gens): named lineages **8/8 survive** / lineage_fixation (tail) 0.67 / diversity_l2 (tail) **17.91**. The 14 weak-axis cases are selected independently, and behavioral diversity is high. Lineages are maintained by the reservoir (because pressure-proxy does not directly reward persona identity, the dominant lineage's share becomes 0.67, higher than rich-proxy's 0.29).

![Population-mean trajectory of the 5 weak axes (typo / polysemy / multistep / calibration / context) (proxy measurement)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_en.svg)

**Honest caveat (an accepted limitation already stated in design §7 / §7.1)**: The individual is not a real LLM but a genome (an llive configuration). What this pressure measures is **a proxy for behavior** — "how much the genome possesses the **thought factors related** to that weakness" — and is **not the LLM ability of production**. This is limited to **the verification of mechanism feasibility (that the mechanism runs)**. The Goodhart risk (surface strategies that hack the proxy evolve) is also an accepted limitation. The actual measurement of real LLM/VLM weak axes is carried over to the second half of Stage2 (which presupposes the OLLAMA_HOST setting + the individual→real-LLM mapping).

> 🍵 **Break point**: This is easily misunderstood, so let me press the point. I have **not yet said** "I overcame the LLM's weaknesses by evolution!" What the proxy measures is only "whether the mechanism runs." Whether a real LLM became robust to typos is, at this stage, completely unknown. Even if a flashy number (17.91) comes out by proxy, that is proof that "the device works," not proof that "the contents got smarter." The moment you blur this line, the research becomes a lie. So next, I face **the real LLM**.

---

### 9. Stage2 second half — evolving prompt strategies against a real on-prem LLM

Once I found that localhost's ollama (llama3.2:latest, etc.) was reachable, **real LLM evaluation** finally became possible (commit `2fb2912`). Because localhost = on-prem, it also satisfies the discipline of measurement purity (do not mix with cloud LLMs) ([[feedback_llive_measurement_purity]]).

#### 9.1 The individual → real LLM mapping (Promptbreeder lineage)

The crux is "how do you make the genome take effect on a real LLM?" In `real_pressures.py` I implemented the **individual → real LLM mapping**.

- **Convert the individual's `c_prompt` (PromptChromosome) into a system prompt**: skill_set → instructions / prompt_template_id → reasoning style / language_style → tone. We put this system prompt over a fixed LLM (llama3.2), make it solve the **real tasks** of the 5 weak axes, and score it.
- **Fix the LLM body and evolve the prompt strategy (genome)** = select, by measurement, "which prompt strategy mitigates the LLM's weaknesses." This follows the style of Promptbreeder (the research lineage that optimizes prompts evolutionarily).
- Deterministically with temp=0 (greedy). Cache `(system_prompt, task)` (the same strategy is not re-evaluated).
- robust: per-call try/except (an ollama hiccup is treated as the task's lost points, and the run continues).
- Added `--fitness real-pressure` / `--ollama-model` / `--max-wallclock-seconds`. tests 5 + evolution-system 947 green.

#### 9.2 Demonstration of a real selection signal — the CoT+structure strategy takes multistep from 0.0 → 1.0

And then, a real selection signal was observed.

**The CoT+structure strategy** (`chain_of_thought` + structurize + loop) **improved llama3.2's multistep (multi-step reasoning) from 0.0 → 1.0** (the terse strategy fails at 0.0; the score rose 0.80 → 1.00).

This means that lldarwin's claim "the evolution of prompt strategies can mitigate the LLM's weaknesses" was **demonstrated not by proxy but on a real LLM**. Even with the same llama3.2 body, depending on the system prompt put over it (= the evolved genome), the multi-step reasoning task is solvable or not. Evolution actually selected "a solvable prompt strategy."

![Population-mean trajectory of the 5 weak axes (real on-prem LLM llama3.2 evaluation). The evolution of prompt strategies improves the axes](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_en.svg)

#### 9.3 The 12h continuous run

Since real LLM evaluation is heavy, I launched a long continuous run (`out/lldarwin_12h_realpressure_2026_05_26/`).

```
--fitness real-pressure --selection lldarwin --novelty --lineage-reservoir
--genome3d --population 24 --max-wallclock-seconds 43200 --checkpoint-every 5
```

It stopped safely at wallclock 12h (snapshotted → can continue with `--resume`). During the continuous run it reached best_score=1.0.

![Fitness and diversity of the real LLM evolution run (12h continuous run)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_en.svg)

#### 9.4 Honest caveat (the limitations of real LLM evaluation)

This is the culmination of the attitude learned from #25. Precisely because a flashy result came out (0.0 → 1.0, best 1.0), I write the breakdown thoroughly and honestly.

- **(a) Only `c_prompt` participates in fitness.** persona / c_factors are neutral (lineages are maintained by the reservoir, initial selection is handled by novelty). In other words this is "**the evolution of prompt strategies**," not "the evolution of personas." It's not that Oka Kiyoshi's personality got smarter, but that a prompt strategy tied to the Oka Kiyoshi lineage was selected.
- **(b) The initial c_prompt of all founders is identical (default).** So exploration is mutation-driven (diversifying the prompt per founder is a future improvement). Because the starting point is the same, the initial lineage differences have no effect on the prompt strategy.
- **(c) A small battery (2 questions per axis) = a noisy estimate.** Even the dramatic number 0.0 → 1.0 contains noise to the extent the number of questions is small. To make a statistically robust claim, a much larger battery is needed.
- **(d) on-prem only (measurement purity). It is not a claim about general ability.** This is an observation on a specific model and specific tasks (llama3.2), and I do not say "LLMs in general turn out this way."

If I hid these, I could write a flashy story like "evolution made the LLM dramatically smarter!" — but that would be a lie. What lldarwin demonstrated goes only as far as "**the mechanism, on a real LLM, produces a selection signal**." I make no claim crossing that line.

> 🍵 **Break point**: The most pleasurable moment in research is shouting "0.0 became 1.0!" But that very moment is when [[feedback_benchmark_honest_disclosure]] takes effect. "When a suspiciously good number comes out, doubt the breakdown before you feel like a winner." In this case — what won is the "prompt strategy," not the "LLM body" nor the "persona." The number of questions is also small. Only 1 on-prem model. Only after writing all of this can I say "I demonstrated it" for the first time. Honest disclosure is the muscle training of holding back from bragging.

---

### 10. Reuse of existing assets (based on the codex code survey)

So as not to make the design a pie in the sky, I had my subordinate Codex survey the existing code, and found that **much was already implemented but unwired**.

- `mating.py:139 LexicaseSelection` (with ε, implemented but unwired → just wire it)
- `nsga2.py:197 NSGA2Selection` (for the ≤3-objective lane)
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**Newly implemented**: `Standardizer` / `MinimalCriterionGate` / the `Pressure` group / `MultiPressureSelector` (the core) / `LineageReservoir` (Stage1.5) / `SelectionAudit`.
**Wiring points**: inject `MultiPressureSelector` into `selection` at `loop.py:122`, add an injection point at `persona_evolution.py:606`, and connect `LineageReservoir` to the `EvolutionLoop.on_population_bred` hook.

> 🍵 **Break point**: That "implemented but unwired" was the most common was the biggest lesson. Even if you make good parts, **unless you wire (orchestrate) them, evolution stays broken**. The reason #25 went 8→2 is that ε-lexicase, NoveltyScorer, and QD were all "in the box but not wired." The essence of lldarwin is, more than the invention of new algorithms, "bundling good existing parts **without aggregating** and **actually wiring** them into the evolution loop." Even if you gather all the electronic parts, the radio won't make a sound unless you solder them.

---

### 11. The guarantee of breakdown avoidance — a multi-layer structure that does not wipe out (already backed by measurements)

The multi-layer structure that refutes #25's monoculture (8→2) is assembled as designed, and this time it was **backed by measurements**.

1. **MinimalCriterionGate** — reproduction eligibility by a minimum criterion → suppresses winner-take-all.
2. **QD per-cell elite** — as long as even 1 cell remains, total lineage wipeout is impossible (the archive grows monotonically).
3. **Niching / FitnessSharing** — down-weight the same niche → multiple peaks coexist.
4. **Down-sampling** — destroy plateaus with a moving target.
5. **per-dim z-score + central-agreement exclusion** — do not favor the featureless.
6. **LineageReservoir (added in Stage1.5)** — a neutral reservoir for extinct lineages → structurally prevents total lineage wipeout (8/8 survival in measurements).
7. **monoculture monitor + SPC** — record max_lineage_share every generation, detect >0.8 with SPC_ALARM → auto-adjust.

In particular, (6) is **a layer added afterward** in response to §5's honest disclosure (novelty cannot stop lineage fixation). I found a hole in the design by measurement and plugged it. The measured lineage_fixation falls well below the OE-3 criterion (<0.8): OFF 0.70 → ON 0.29. The achievement of this article is that with the two-stage structure of "don't aggregate" + "revive extinct lineages," I could structurally crush #25.

---

### 12. honest disclosure / risks (a preview)

I do not blindly trust the design. Let me summarize once more the accepted limitations (to be dug into in the next article #27).

- **Goodhart's law / proxy divergence** — when you make LLM weaknesses into proxy fitness, "surface strategies that hack the metric" evolve (typo → memorizing specific substitutions, WSD → using test heuristics, etc.). The proxy is limited to mechanism feasibility, and does not claim production ability.
- **Designer dependence** — lexicase=case / QD=descriptor / novelty=distance metric; in every case, the "direction of diversity" is decided by the designer. Unanticipated emergence on the scale of biological evolution is limited.
- **The minimal-criterion stagnation⇄collapse trade-off** / **the curse of dimensionality + archive saturation of QD**.
- **The limitations of real LLM evaluation (reprised from §9.4)** — only c_prompt participates in fitness, the founders' initial prompts are identical, a small battery, on-prem only.

> **Next time preview (#27)**: I honestly expose the most painful counterpoint, "when the glasses saturate, the selection pressure is powerless," together with the limitations of Goodhart's law and proxy fitness. lldarwin is not omnipotent. **How far we may claim** is the subject of #27. Precisely because good numbers like "8/8 survival" and "0.0→1.0" came out this time, next I temper it thoroughly with counter-evidence.

---

### 13. Conclusion

- Evolution is a two-stage structure of "**measuring (lleval)**" and "**selecting (lldarwin)**." The core of selection is **"don't aggregate."**
- Stage1: with criteria exclusion + novelty pressure, I doubled behavioral diversity from 7.12 → 14.88 (+109%) and avoided the late-stage collapse.
- honest disclosure: novelty/lexicase preserve **behavioral diversity**, but **lineage fixation** heads toward monoculture by neutral drift (Kimura). I had been confusing the two kinds of diversity — recorded honestly.
- Stage1.5: with the lineage-niched **neutral reservoir**, in the real EvolutionLoop I achieved **OFF=2 lineages / ON=all 8 lineages survive** (including Oka Kiyoshi and Grothendieck), lineage_fixation 0.29 (≪0.8). **This is not fabrication; it actually ran.**
- Re-injection frequency sweep: the lineage-retention ↔ behavioral-diversity trade-off. The non-trivial finding that diversity peaks at interval=5 (**non-monotonic**).
- Stage2 first half (proxy): made the 5 weak axes into Pressure plugins (mechanism feasibility only).
- Stage2 second half (real LLM): with the individual c_prompt → system prompt mapping, scored real tasks on a fixed on-prem LLM (llama3.2). **The CoT+structure strategy improved multistep from 0.0 → 1.0.** Reached best=1.0 in a 12h continuous run.
- Without optimism, without feeling like a winner, I reported by separating the breakdown ([[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]]).

Just making good parts leaves evolution broken. **Bundle without aggregating, actually wire, revive extinct lineages, and confirm the selection signal on a real LLM** — only by going that far could I finally change #25's world of "only me and Friston" into a lively world where Oka Kiyoshi and Grothendieck are also present. In the next article #27, I question anew, with counter-evidence, how much trust we may place in this success.

---

### 14. Related

- Series #25 "Only Me and Friston Remained" — the motivation for this article (a record of failure)
- Series #24-08 "Making the Glasses" — lleval (the measuring side)
- Series #27 "When the Glasses Fog Up, Selection Is Powerless Too" — counter-evidence investigation (honest disclosure)
- Design document: lldarwin (the selecting side) `docs/vision/LLDARWIN_DESIGN.md`
- Measurement of record: `docs/research/lldarwin_stage1_results_2026_05_26.md`
- llive commits: Stage1=`8060204` / neutral reservoir PoC=`0d0537d` / Stage1.5=`b03cbda` / reinject sweep=`da93dd3` / Stage2 real LLM=`2fb2912`
- Related memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]] / [[feedback_poc_feasibility_first]]

---

---

## Chapter 3 Rebuilding AI Evolution Overnight — The Night a Real-LLM 12h Run Saturated at a Perfect Score Again, and 6 PoCs, 4 Agents, and Perplexity Independently Converged on the Same Conclusion #27

:::note info
**📚 FullSense Knowledge Base** <!-- fullsense-team-kb -->
The full FullSense development history — 60+ articles in 4 languages, with a story-based reading guide, plain-language editions, and 4-panel manga — is consolidated in our Qiita Team **FullSense KB** (team members only).
:::



> 📚 **Series navigation (lldarwin arc)**: #24-05 population evolution → #25 the monoculture failure → #26 design → **#27 this article (climax)** → [#28 implementation (orchestra-style AI)](drafts/QIITA_#28_lldarwin_v2_phase1_orchestra.md). Each article stands alone (links are for browsing).

> **Concept hook**: In the previous installment (#25), I confessed a major failure: after evolving an AI for 500 generations, the only survivors left in the world were **Friston and me**. The cause was that the evaluation function (the "lens" = lleval) kept handing out perfect scores, so **selection pressure dropped to zero**.
>
> "Then this time, let's verify it with a real LLM." With that, I ran a **continuous 12-hour evolution** against on-prem llama3.2. Not a proxy (a synthetic ruler) — a real LLM.
>
> The result: **it pinned to a perfect score at gen5 and didn't budge for the next 65 generations.** No extinction, but no accumulation either. This wasn't evolution — it was **just "filtered random search"**: not only with the proxy, but **even with a real LLM, it still wasn't evolving.**
>
> From there, one all-nighter. To "decide a strategy," I ran 6 PoCs myself, dispatched 4 Claude Agents in parallel, and had Perplexity comb the literature. By morning, **everyone had independently converged on the same conclusion.** This is the honest disclosure of that "overnight decision log."

---

### 0. The story in three lines (the "preamble" in rakugo terms)

In rakugo (Japanese comic storytelling) there's a "preamble" before the main story. First, three lines.

- **It saturated again** — Running the real LLM (llama3.2) for 12h, best=1.0 pinned at gen5, no progress for 65 generations. No extinction but no accumulation either = **filtered random search**. The root cause is the same as #25: "saturation of a fixed, hand-crafted ruler."
- **A strategy was decided overnight** — 6 self-run PoCs + 4 parallel Agents + Perplexity **independently converged on the same conclusion**: "Polishing the selector while keeping the ruler fixed is useless. **Make the evaluation itself open-ended.**"
- **The originality came into view** — Letting a continuously-evolving population perform an ensemble (MoA) at any instant — without stopping — to produce one answer, "**the live orchestra**," turned out to be a white-space in prior research.

In short: **"Once the lens (evaluation) saturates, no amount of polishing the selector (lldarwin) helps."** So we change what we polish — **we make the evaluation itself open-ended.** That's this round's conclusion.

---

### 1. Why I did it "again" — continuing from #25 / #26 (design)

Recapping the series so far in three lines:

- **#24-05** "AI that learns as a population" — Rather than making one LLM smarter, we framed **derivative-population evolution**: N llive individuals (genomes) cycle through generations, evaluating each other.
- **#25** "Only Friston and I were left" — We seeded that population with 8 intellects as persona seeds and ran 500 proxy generations, producing a major failure: **perfect-score saturation → zero selection pressure → genetic drift (luck) alone biasing toward 2 lineages.** The lens was clouded.
- **#26 (design)** "Measuring with a lens alone doesn't make it evolve" — We designed the selector **lldarwin** and implemented "non-aggregating multi-objective selection (ε-lexicase / QD / neutral reservoir)." In proxy, it prevented lineage extinction.

Up to here, everything was about **proxy (deterministic heuristic, LLM-independent)**. A proxy can show "the mechanism turns," but it can't show "evolution found something **meaningful**" ([[feedback_benchmark_honest_disclosure]]).

So, the natural next move: **verify with a real LLM.**

Since localhost's ollama (llama3.2:latest) was reachable, I converted each individual's `c_prompt` (the prompt-strategy gene) into a system prompt, layered it over a fixed llama3.2, and had it solve real tasks — a **Promptbreeder-style mapping** — launching a 12-hour continuous evolution run. That's the starting point of this article.

> 🍵 **Break point**: If you've reached "the mechanism turned in proxy — so what about a real LLM?" you're good. The nice thing about research is you can actually run that "so what about the real thing?" And this time, the real thing was — merciless.

---

### 2. The starting point — the "honest fail" of the real-LLM 12h run

Here's the result of the 12-hour real-LLM evolution run (on-prem llama3.2, strictly honoring measurement purity = never mixing in cloud LLMs, [[feedback_llive_measurement_purity]]).

| Fact | Value | Implication |
|---|---|---|
| Completed | 71 generations / 12h (≈10.3 min/gen, real LLM sequential) | Throughput is the bottleneck |
| best_score | **1.0 at gen5 → fixed through gen70** | **Objective saturation. 65 generations of no progress** |
| mean | Capped at 0.85; the 1.0 strategy doesn't take over | **Adaptation doesn't accumulate** |
| Per-axis | 6-7 of 10 questions saturated; gradient only in multistep (2 questions) | Effective resolution too small |
| fitness dependence | **c_prompt only**. c_factors (40-dim) / c_impl / c_meta drift neutrally | **43 dimensions have zero selection pressure** |
| Population health | pop=24 maintained, min ≥ 0.70, **no extinction** | The mechanism (GA) isn't broken |

This is where FullSense's honest disclosure rule makes you stop ([[feedback_benchmark_honest_disclosure]]). Write "No extinction! Reached best=1.0!" and it sounds like a success. But look at the breakdown and it's obvious.

**Verdict: not extinct, but not cumulative evolution either (≈ filtered random search).**

Of the 10-question test, only the 2 multistep questions retain a gradient (a difference). The other 8 were all maxed out early. In other words, for 8 of 10 questions it no longer matters who you pick. The effective resolution of selection pressure is down to roughly 2 questions' worth. And only 1 of the 4 chromosomes — `c_prompt` — participates in fitness; the remaining 43 dimensions (40-dim thought factors + impl + meta) are **neutral drift with zero selection pressure.**

![Fitness and diversity of the real on-prem LLM (llama3.2) evolution run (12h continuous). best pins to the ceiling early and stays flat thereafter](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status_en.svg)

![Population-mean trajectories of the 5 weak axes (typo / polysemy / multistep / calibration / context) under real on-prem LLM evaluation. Everything except multistep saturates early, leaving no gradient](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_en.svg)

**Root cause = saturation of the hand-crafted fixed ruler.** The insight the user articulated in #25 — "**once the lens saturates, selection pressure is powerless**" — we've now **demonstrated with a real LLM**, not a proxy. Swapping the lens from proxy to real LLM doesn't help: **as long as the ruler is "the fixed 10 questions," it saturates at a perfect score quickly.** Change the lens manufacturer and, if the gradations are coarse, you get the same thing.

> 🤔 **Analogy**: Even if you swap the grader for a "real teacher" (real LLM), if the questions are the same every time, everyone scores full marks within a few rounds, and no difference shows afterward no matter how many tests you run. The questions aren't bad — **the question sheet is fixed and too easy.** Swapping the grader (lens) from proxy to real LLM still saturates if the ruler (questions) is fixed. This is the essence of the "honest fail."

> 🍵 **Break point**: Many people now think, "If even a real LLM saturates, isn't it game over?" I thought so too. But this is where the main story begins. If **"fixing the ruler was the mistake,"** then what we should fix is neither the selector nor the LLM, but **the very way we build the ruler.** I verified that over one all-nighter, with 6 PoCs, 4 Agents, and Perplexity.

---

### 3. The overnight plan — distributed investigation to "decide a strategy"

The instruction from the user was this:

> "Organize the requirements thoroughly, and bring out more originality as an evolutionary system. Repeat PoCs many times. Keep running small-unit PoCs nonstop until morning to **decide a strategy.**"

The key here was that the goal was **not "complete the implementation" but "decide a strategy."** So rather than running one big production run, I took the approach of running **many small PoCs** to knock down design decisions one by one with real data ([[feedback_poc_feasibility_first]] = requirements → PoC → feasibility → detailed design).

The workers I ran in parallel were these ([[feedback_parallel_first_execution]] = independent tasks default to launching parallel Agents).

| # | Worker | Task |
|---|---|---|
| A | Claude Agent | Open-ended sweep PoC (demonstrate baseline = saturation/extinction vs. open-ended = avoidance, ≥10k generations) |
| B | Claude Agent | Observability (response logs / per-individual score time-series viewer / lineage reconstruction) |
| C | Claude Agent | Orchestra PoC (does MoA beat a single best? diversity vs. redundant selection) |
| P | Perplexity | SOTA survey of QD/novelty/MoA/agentic evolution (filling literature gaps) |
| X | Codex | Independent design critique + 3 minimal-PoC proposals + blind-spot flags |
| self | Me (main) | Directly implement and run self-PoCs #1–#6 (orchestrator + owner of the most important task) |

> 🍵 **Break point**: This "six-handed" setup is actually the hidden protagonist of this article. Why not do everything with one person (one context)? The answer is at the heart of honest disclosure. **A conclusion reached by the same mind is dragged by the same bias.** Verify **independently** with different methods (synthetic PoC / real LLM / literature survey), and only trust the conclusion when they agree. This is what I call **honest cross-validation.** Its power shows up in the second half.

Here, one honest dud to record. **Codex (X) was unusable.** A permitted-model mismatch on the ChatGPT account (the API rejected the entire codex model family) blocked it. It should have been within the 10x promo period, yet the API returned "not supported when using Codex with a ChatGPT account." Since this is an environment problem, for now I switched the main axis to self-PoCs + parallel Agents + Perplexity. **"A tool that should have worked but didn't" gets recorded too, not hidden.**

---

### 4. The first decisive blow — should we discard the "fixed ruler"? (self-PoC #1 / #2)

The first hypothesis to knock down was the most fundamental question: **"If we change the ruler from fixed difficulty to adaptive difficulty, does saturation get fixed?"**

#### 4.1 Self-PoC #1 — adaptive difficulty fixes saturation. But it kills diversity

Using a proxy with synthetic competence vectors, I compared while removing confounds (selecting elites by score).

- **baseline (fixed difficulty)**: competence **stagnates low at 0.627** (best 0.757). The 12h pathology reproduced in proxy.
- **adaptive (difficulty follows the population's 60th percentile)**: competence **rises to 0.952** (best 1.0).

Letting difficulty track the population (raise difficulty as more problems become solvable) breaks the saturation and grows competence. **But** — adaptive **sacrifices diversity** (diversity collapses 0.310 → 0.134). In the process of optimizing for hard problems, the population coalesces onto one correct strategy.

#### 4.2 Self-PoC #2 — adaptive difficulty × novelty are compatible

So what happens if we add "novelty selection (maintain diversity)" on top of "adaptive difficulty (maintain gradient)"?

| Configuration | Final competence | best | Diversity | plateau |
|---|---|---|---|---|
| baseline (fixed difficulty) | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive (difficulty-tracking) | 0.952 | 1.000 | 0.134 (collapse) | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316 (maintained)** | gen99 (longest exploration) |

**Adaptive + novelty achieved both** competence (+40% vs. baseline) and diversity (2.4× adaptive, on par with baseline). It cedes 7% of competence in exchange for fully maintaining diversity.

Here, **the core of the strategy was confirmed with our own data.**

> **"Adaptive difficulty = gradient maintenance" and "QD/novelty = diversity maintenance" are complementary, and both are mandatory.**
> Neither the fixed ruler alone (baseline) nor adaptive difficulty alone (adaptive) is sufficient.

Honest caveat: this is an abstract proxy (competence vectors), not a real-LLM mapping. It is limited to **verifying mechanism feasibility (whether the mechanism turns).** The plateau@gen numbers indicate "the generation at which it stagnated," but the essence is the **level** of stagnation — baseline stagnates low (0.627), the adaptive family stagnates near the ceiling.

> 🤔 **Analogy**: When everyone scores full marks, you raise the difficulty (adaptive difficulty). Then scores spread out — but now everyone converges on the same way of solving (cookie-cutter). So you also add "reward unusual solutions too" (novelty), and competence and diversity coexist. **The two-sword style of "make it harder" and "reward the oddballs"** — that's the point of PoC #2.

---

### 5. The core evidence — the 10k-generation open-ended sweep (Agent A)

The self-PoCs showed the "direction." Next, it was time to hit it **at scale, rigorously.** I had parallel Agent A run an open-ended sweep of **10k generations each × pop256 × 19 configurations × 2 rounds.**

The criterion was whether it was "open-ended" — **does it avoid saturation, avoid monoculture (convergence to a single culture), and keep its archive (diversity reservoir) growing?**

#### 5.1 The decisive verdict table

**verdict (at gen9999): all scalar configs = False / all novelty & lexicase configs = True**

| label | selection | std | MC | reservoir | archive | open-ended | occupied | monoculture | uniq_lineages |
|---|---|---|---|---|---|---|---|---|---|
| baseline_scalar | scalar | - | - | 0 | none | **False** | 9 | 0.74 | 1.0 |
| baseline_scalar_mc | scalar | - | ✓ | 0 | none | **False** | 9 | 0.90 | 1.0 |
| **scalar_qd** | scalar | - | - | 0 | map-elites | **False** | — | — | — |
| novelty_std | novelty | ✓ | - | 0 | none | True | 100 | 0.13 | 1.0 |
| novelty_std_qd | novelty | ✓ | - | 0 | map-elites | True | — | — | — |
| **novelty_std_res256** | novelty | ✓ | - | 256 | map-elites | True | 95 | 0.05 | **31.9** |
| novelty_std_res1024 | novelty | ✓ | - | 1024 | map-elites | True | 98 | 0.04 | 15.2 |
| **full_oe** | novelty | ✓ | ✓ | 1024 | map-elites | True | 90 | 0.05 | 15.3 |
| lexicase_std(_mc) | lexicase | ✓ | -/✓ | 0 | none | True | 111–122 | 0.03 | 1.0 |

Four decisive findings came out of this.

1. **Selection pressure is decisive.** scalar (single scalar fitness) is **extinct (False)** even with a MAP-Elites archive added (`scalar_qd`). So "add a reservoir and you protect diversity" is **wrong** — **unless the selection itself is open-ended (novelty / lexicase), open-endedness doesn't even hold.** An archive alone can't save it. **Making the selection pressure itself open-ended** was the essence.
2. **Standardization (z-score) widens QD coverage by an order of magnitude.** Adding per-dim z-score standardization to novelty takes occupied cells from 9 → 100+. Turning each axis's "deviation" into selection pressure widens behavior-space coverage by an order of magnitude.
3. **The neutral reservoir recovers lineage diversity.** With novelty_std alone, uniq_lineages is 1.0 (lineage fixed to one). Add reservoir256 and it goes to **31.9**. **Behavior diversity and lineage diversity are different axes**; the latter needs a reservoir (a re-confirmation of the knowledge already implemented in #26 design).
4. **Scale matters.** Raising the latent dimension 256 → 1024 takes niches 101 → 166 and archive 1021 (saturated) → 2234 (continued growth). Diversity can be bought with "capacity."

![Fitness and diversity of Stage1 baseline (no novelty). Diversity collapses near the end (the typical scalar failure)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_en.svg)

![Stage1 with novelty pressure. Behavior diversity is maintained until the end](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status_en.svg)

![Overlay of baseline vs. +novelty diversity. Collapse (scalar) and maintenance (novelty) contrasted in one figure](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay_en.svg)

#### 5.2 The "honest limits" Agent A surfaced

It's exactly when you get a good result (open-endedness holds) that you write the limits. Agent A itself pointed this out:

> novelty/lexicase preserves the diversity of the descriptor **as a whole**, but **does not guarantee the diversity of a specific semantic dimension (factor).**
> At large latents, factor drift occurs, and fspread (the spread of factors) needs monitoring.

In other words, even when "diverse as a whole," it may be "converged on the specific semantic dimension of thought factors." This gave rise to a new requirement, **factor-subspace QD (a QD that protects each semantic dimension individually)** (addressed in PoC #6 below).

> 🍵 **Break point**: This is the densest section of the article. The one line to take home: **"Adding an archive (reservoir) alone can't save it. Unless the selection pressure itself is open-ended, it fails."** Since #25/#26 design we've said "don't aggregate," but its core was that **"open-ending the way you select"** — and 10k generations of real data declared it. Past this point, it's all about originality.

---

### 6. The core of originality — "let a continuously-evolving population perform an ensemble without stopping"

By now, the "selection core that structurally avoids saturation (S1)" was solidified. Next, it was time to back up — with PoCs and literature — the **three originality axes** the user laid out in dialogue.

The three axes the user articulated were these.

1. **Continuously-evolving population = live orchestra (ORCH)** — a continuously-evolving population performs MoA (Mixture-of-Agents) aggregation on the spot to produce one answer. Evolution never stops. **The biggest differentiation candidate.**
2. **Individuals with investigation capability (AGENT)** — individuals go investigate by themselves. Voyager-style.
3. **Observation / interactive control (OBS)** — view per-individual responses + selection-score time series, pause, and resume.

#### 6.1 The white-space Perplexity backed up

The Perplexity SOTA survey (1143 lines) running in parallel returned the most important backing.

> A "**continuously-operating system integrating online evolution + online answering**" has no clear prior research = a **research white-space.** The closest are MoA / Self-MoA / sequential aggregation / routing, but none is identical.

In other words, "stop evolution and answer with the strongest individual produced" is ordinary. "Without stopping evolution, have the evolving population itself perform an ensemble and answer" — nobody has done it yet. **The differentiation of ORCH §1.11 was confirmed.**

#### 6.2 But Perplexity also gave a counter-warning

As honest disclosure, I write the **counter-warning** Perplexity gave with equal weight.

> In 2025's **Self-MoA research**, **diversity is not automatically superior.** Iterating a single top model beat a heterogeneous-mix MoA by 6.6% on AlpacaEval (a quality-diversity trade-off).

"An ensemble of a population is stronger than a single individual" is **not self-evident.** Prior research warns that diversity can even be counterproductive. So ORCH is "prove it empirically, with an honest pass-bar." I verified this with Agent C and self-PoCs #3/#4.

> 🍵 **Break point**: This is the branch point where research integrity is tested. Right where you want to get carried away with "online evolution + online answering is white-space! originality!", Perplexity pours cold water with "but there's a counter-result that diversity isn't automatically good." **Receive both the elation material and the cold water within the same investigation.** Do this, and the conclusion gets much stronger. In the next section, I unravel the true nature of that cold water.

---

### 7. Unraveling the "true nature" of the Self-MoA counter-result (self-PoC #3 → Agent C real LLM)

"Diversity is not automatically superior" — unraveling this counter-result at the **mechanism level**, not in proxy, is the climax here.

#### 7.1 Self-PoC #3 — voting, or routing?

First, it couldn't be verified in proxy (with saturated fitness the single best is already at full marks = zero headroom, so no difference shows). So I synthesized **"hard tasks a single individual can't ace"** (experts dispersed, single_best=0.5) and measured.

| Configuration | best_of (routing) | majority (vote) | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant (top-k) | 0.750 | 0.500 | 3/4 |
| MoA diverse (max-cover) | **1.000** | **0.000** | 4/4 |

Here a **decisive finding** emerged.

- Diverse MoA is **1.000 with best-of / routing** (double the single best). **ORCH holds.**
- **But with naive majority (a vote), diversity is counterproductive** (diverse = 0.000). On each sub-task, the one competent expert gets negated (canceled out) by the ignorant majority. Redundant MoA's majority (0.500) is higher.

In other words, **the true nature of the Self-MoA counter-result (diversity ≠ automatic superiority) was "whether the aggregator is voting or routing."** Voting/averaging kills diversity; competence-aware routing/gating leverages it. It's the difference between "an orchestra with a conductor" and "a crowd where everyone plays whatever they want."

#### 7.2 Agent C's real LLM independently produced the same conclusion

And then — parallel Agent C, with a **real LLM (llama3.2, 105 LLM calls, 15 tasks)**, produced the **same conclusion independently** of self-PoC #3.

- single best = **0.933**. MoA `best_of` + k≥5 reaches **1.000** (+0.067). **majority / weighted never exceeded 0.933.**
- diverse > redundant (diverse selection picks up complementary specialists in different QD cells earlier, with fewer k).
- The improvement is **entirely from one multistep question** ("double 5 and subtract 3"). The CoT-individual group all drops one question, and the heterogeneous individuals from diverse selection solved it.

> 🔑 **Independent cross-validation (the core of this article)**: Self-PoC #3 (synthetic, dispersed experts) and Agent C (real LLM, llama3.2) reached the **same conclusion via different methods** — "MoA beats the single best only with competence-aware routing (best_of) / voting doesn't get there / diversity has value only under routing." Two methods agreeing is extremely strong evidence in honest disclosure terms.

#### 7.3 The biggest hole — does a "real router" reach the oracle? (self-PoC #4)

Here Agent C pointed out the biggest hole. "best_of is **oracle routing** (the upper bound where God knows which individual is correct); in reality, the accuracy of the **gate that predicts** 'which individual is competent' is the bottleneck. Real voting (majority) doesn't reach the oracle."

I filled this with self-PoC #4 (real router vs. oracle, averaged over 20 seeds).

| κ (calibration) | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **The descriptor / specialty-router is robust at 0.90 with no calibration needed** (stably beating the single best 0.675, near the oracle). Moreover, **the routing key can reuse the behavior descriptor already computed for QD** — a synergy where **QD and ORCH share the same descriptor foundation.**
- **The confidence-router reaches the oracle at calibration κ≥0.6.** But small LLMs may be weakly calibrated → **make the descriptor-router the first choice** (calibration-independent).
- **majority = 0.338 is decisively unfit** (agreeing with PoC #3 and Agent C — a **third agreement**).

**Conclusion**: The hole Agent C pointed out — "real voting doesn't reach the oracle" — is **practically filled by descriptor-routing (reusing the QD descriptor).** ORCH holds end-to-end in proxy + (partial) real LLM.

> 🤔 **Analogy**: Gather 10 experts and have them vote, and the ignorant majority cancels out the correct experts. Route the math question to the mathematician — you need a **dispatcher (a conductor = routing).** And that conductor's score (behavior descriptor) can reuse what's **already been computed** to manage diversity. Voting (majority) kills the expert; the conductor (routing) leverages them. This is the point of PoC #4.

---

### 8. Giving individuals the "power to investigate" (self-PoC #5)

The second of the three originality axes: **individuals with investigation capability (AGENT).** The idea is to let individuals do sandboxed read-only investigation in the search space. But "investigation isn't free" — when you charge a cost, does evolution learn to use investigation well?

Self-PoC #5 (vary cost λ and see how the investigation threshold θ evolves, averaged over 20 seeds).

| λ | θ* (=λc, optimal threshold) | θ_evolved (threshold evolution acquired) | evolved | always | never |
|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.049 | 21.46 | 21.47 | **11.70** |
| 0.3 | 0.30 | 0.476 | 21.34 | 21.26 | 21.20 |
| 0.6 | 0.60 | 0.659 | **21.24** | 21.06 | 21.21 |
| 0.9 | 0.90 | 0.888 | 21.21 | 20.85 | 21.21 |

- **Evolution acquired the selection threshold θ → λc on its own** (= selective investigation, "investigate only when you should," **emerged**).
- **The value of investigation capability is clear**: when λ=0 (investigation free), never (never investigate) = 11.70 = **a 45% loss.**
- **Cost λ degrades "always investigate" and forces selection.** AGENT-3 (the cost principle) holds.

Honest caveat: the margin at intermediate λ is small (a shallow reward landscape), and this too is an abstract proxy (real LLM × knowledge base is a separate matter). Still, the mechanism "with a cost, selective investigation emerges" was confirmed in proxy.

---

### 9. Scale "qualitatively increases diversity" (Round 3)

Finally, I verified Agent A's "you can buy diversity with capacity" also via population size. With the `full_oe` configuration (novelty + std + MC + reservoir1024 + map-elites), I swept pop from 256 → 4096.

| pop | gens | occupied niches | monoculture | uniq_lineages | distinct_genomes | bspread_tail |
|---|---|---|---|---|---|---|
| 256 | 5000 | 171 | 0.047 | 14 | 256 | 0.939 |
| 1024 | 3500 | 467 | 0.019 | 74 | 1022 | 1.003 |
| 2048 | 2500 | 754 | 0.009 | 188 | 2041 | 1.071 |
| 4096 | 1200 | **1219** | **0.006** | **372** | 4054 | 1.253 |

With population-size scaling, open-endedness improved **monotonically** (niches 171 → 1219 / monoculture 0.047 → 0.006 / uniq_lineages 14 → 372 / behavior spread bspread also monotonically up). The POP-1 hypothesis (population size increases diversity) was supported in proxy.

**Honest (confound made explicit)**: there's an honest pitfall here. To raise pop, I shortened gens (5000 → 1200). This is **a confound in the direction unfavorable to niche accumulation.** Yet it still increased monotonically — i.e., **the POP effect is a robust lower bound** (it should actually be stronger). Conversely, "the possibility that it's stronger" couldn't be proven in this experiment. The claim is limited to proxy mechanism feasibility.

![Winner-individual thought-factor × memory-layer heatmap (Genome3D). Under real-pressure, c_factors drift neutrally, so treat this as a reference visualization of a cognitive profile](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_genome_heatmap_en.svg)

> 🍵 **Break point**: "Scale up and diversity increases" is intuitive, but the important thing here is the honesty that **"even when we added an unfavorable confound, it still increased monotonically."** Cutting gens is normally unfavorable to diversity. It increased anyway. So we can call it a "lower bound." Writing a good result as a "lower bound" rather than exaggerating it as an "upper bound" — this too is the manner of honest disclosure.

---

### 10. By morning, everyone had arrived at the same conclusion — the finalized strategy

In one all-nighter, **6 self-PoCs + Agent A/B/C + Perplexity independently converged on the same conclusion.** This is the power of honest cross-validation. We discarded the fixed-ruler line and finalized the following as the core of lldarwin v2.

#### S1. The selection core (structurally avoid saturation)

- **Abolish fixed scalar quiz fitness** (baseline saturates at 10k generations + monoculture 0.9 + diversity collapse = large-scale reproduction of the 12h pathology, open-ended 0/6).
- **Selection = novelty / ε-lexicase (z-score standardization mandatory) + minimal-criterion.** **A MAP-Elites archive alone won't do** (scalar_qd also goes extinct) = make the selection pressure itself open-ended.
- **Quality is also needed, so QD (quality × diversity per cell)**: pure novelty sacrifices scalar quality (0.77-0.83) → pair with adaptive difficulty (conditional curriculum) to supply a quality gradient (PoC #2).
- **Lineage diversity is secured separately with a neutral reservoir** (behavior diversity ≠ lineage diversity; res256 takes uniq_lineages 1 → 32).
- **Add factor-subspace QD** (protect semantic-dimension diversity individually; addressing Agent A's factor-drift limit; PoC #6).

#### S2. How to produce results = continuous evolution × live orchestra (the core of originality)

- The deliverable is not a single best but **continuously evolving the QD archive and performing a MoA orchestra at any point in time to produce one answer** (ORCH; integrating online evolution + online answering is white-space = originality, confirmed by Perplexity).
- **Aggregation must be competence-aware routing/gating (a conductor), not voting** (self-PoCs #3/#4 + real-LLM Agent C agree threefold).
- **The routing key reuses QD's behavior descriptor** (the descriptor-router is calibration-independent and near-oracle at 0.90) = QD and ORCH share the same descriptor foundation (design economy).

#### S3. Individuals = agentic individuals with investigation capability (staged introduction, proxy-verified)

- In the search space, only sandboxed read-only investigation (real I/O after one-way promotion via the Approval Bus). Investigation incurs a cost.
- **Proxy-verified (PoC #5)**: cost λ makes "selective investigation" emerge. AGENT-3 (the cost principle) holds. Real LLM × knowledge base is the next stage.

#### S4. Observation / interactive control (implemented = standard in all runs, Agent B done)

- Response logs / per-individual score time-series viewer / lineage reconstruction (evolution-system 886 tests green). step/pause/resume to be wired in the next stage.
- Agent B's lineage reconstruction resolved the lineage display that was "**all ?**" in the 12h data, resolving the champion lineage gen70 → gen59 over 12 hops. Gaps are not fabricated but explicitly marked `lost@genN` (root cause = parent IDs couldn't be traced from either the snapshot or the winners alone). The observability foundation is the very bedrock of honest disclosure.

#### Self-PoC #6 — factor-subspace QD addresses Agent A's limit

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

Imposing a separate novelty for the semantic dimension (factor) roughly halves the loss of semantic-dimension diversity (50% loss → 32% loss). An effective measure for Agent A's factor-drift limit, demonstrated in proxy. Honest: not fully fixed but 68% retained = the remaining drift needs combining with the neutral reservoir or strengthening factor weights.

---

### 11. Lessons (kept as honest disclosure)

- **Even a real LLM saturated.** Even swapping the lens from proxy to real LLM, with a fixed ruler it's full marks at gen5.
  "Use a real LLM and it'll evolve" was a **lie.** The problem was the way the ruler was built.
- **Adding an archive alone can't save it.** "Hold a diversity reservoir and diversity is protected" is wrong.
  scalar selection went extinct even with a QD archive added. **What saves it is open-ending the selection pressure itself.**
- **Diversity isn't automatically good.** The true nature of the Self-MoA counter-result is "voting or routing."
  Only with a conductor (competence-aware routing) does diversity become a value. Voting kills experts.
- **Independent cross-validation strengthens the conclusion.** Self-PoCs (synthetic), Agent C (real LLM), and Perplexity (literature)
  separately converged on the same conclusion — that's why you can trust it. A conclusion from the same mind shares the same bias.
- **Proxy is only mechanism feasibility.** This article's PoCs verify "whether the mechanism turns," not a claim of "general capability improvement of real LLMs." The moment you cross this line, the research becomes a lie.
- **Record the tool that didn't work (Codex), too.** Not just successes but duds, honestly.

In short — **"once the lens (evaluation) saturates, no amount of polishing the selector helps."** So we shift what we polish — not the selector, not the LLM, but **open-ending the evaluation itself.** That's the conclusion of the all-nighter.

> 🍵 **Break point**: In #25 I decided to "expose failure." In #26 design I built a "non-aggregating selector." And this time, a real LLM taught me "that's still not enough, because the ruler is fixed." **Failure breeds the next design, and the limits of that design breed the next.** This is the backbone of the series. The flashy "AI got smarter through evolution!" — I haven't written it even once. Because the evidence to write it isn't in place. When it is, that's when I'll write it.

---

### 12. Conclusion

- The real-LLM 12h run was an "honest fail" — filtered random search that doesn't go extinct but doesn't accumulate. The root cause is saturation of the fixed ruler (demonstrating #25's insight with a real LLM).
- The overnight distributed investigation (6 self-PoCs + Agent A/B/C + Perplexity) independently converged on the same conclusion = **honest cross-validation.**
- Finalized strategy: **S1 an open-ended selection core** (novelty/lexicase + std + MC + QD + adaptive difficulty + neutral reservoir + factor-subspace QD) / **S2 continuous evolution × routing-MoA** (white-space originality, a conductor not voting) / **S3 agentic individuals + cost** (emergence of selective investigation) / **S4 observation** (implemented).
- All elements backed in proxy / (partial) real LLM. Remaining work: "wiring to the real-LLM stage," "factor-subspace QD implementation," "scale-up." The core strategy is finalized.

Build good parts, bundle them without aggregating, verify saturation with a real LLM, and rebuild toward open-ended selection. And only when 6 independent verifications arrive at the same conclusion can we finally say "the strategy is decided." This article is precisely the "**when the lens clouds, the selector is powerless too**" installment foretold in #25 — honestly exposing the moment the lens clouded with a real LLM (saturation), taking on Goodhart's law and the limits of proxy, then rebuilding toward open-endedness. Next is the [**#28 implementation phase**](drafts/QIITA_#28_lldarwin_v2_phase1_orchestra.md) that turns this finalized strategy into code.

---

### 13. Related

- Series #24-05 "AI that learns as a population" — the framework of derivative-population evolution (the premise of this article)
- Series #24-08 "Building the lens" — lleval (the measuring side)
- Series #25 "Only Friston and I were left" — the honest disclosure of monoculture (the motivation of this article)
- Series #26 (design) "Measuring with a lens alone doesn't make it evolve" — the design of the selector lldarwin and the Stage1/1.5/2 measurements (the sister article)
- Pioneer paper (2026-05-27, date of record) "Continuously-Evolving Populations as Live Orchestrated Ensembles" — a defensive publication formalizing this article's strategy in academic form (FullSense public repository `docs/papers/`)
- Related memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

---

## Chapter 4 An Ensemble Where a "Conductor" Makes an Ever-Evolving AI Population Play Together — llive's Orchestra-Style Evolution and the 3 Devices That Cured Saturation #28

> 📚 **Series guide (lldarwin arc)**: #24-05 population evolution → #25 the failure of monoculture → #26 design article → #27 the all-nighter decision (climax) → **#28 this article (implementation)**. ※ Each article can also be read on its own.

> **Concept hook**:
> Instead of asking one clever AI over and over, you **keep "evolving" a large crowd of slightly different AIs, and at the very moment an answer is needed, a conductor picks the right ones and makes them play together (an orchestra) to produce a single answer**.
> ——This is what llive is now aiming to become. `llive` is not "the LLM itself" but "a cognitive OS you wrap around an LLM". Within it, the evolution engine `lldarwin` we built this time is what **keeps the population alive, unbiased, and continuously growing**.
>
> In the previous article #27, we confirmed, over a 12-hour run with a real LLM, the disease that "once the evaluation (the yardstick) pins to a perfect score, evolution stops and degenerates into a mere sieve-fitted random search". And we decided on a policy: "No matter how much you polish the selector, it is futile. **Make the evaluation itself an open end**."
>
> This time we **implemented** that policy. And on top of a proxy (a synthetic yardstick), **the best score did not pin to a perfect mark — it kept rising all the way to the end**.

---

### 0. The gist in three lines (the rakugo "opening")

- **The selling point is set** — llive's North Star is "**continuous evolution × live orchestra**". Without stopping the ever-evolving population, at any given moment it plays them together via competence-aware routing (the conductor) to produce one answer. This is a **white-space** in prior research.
- **We implemented the 3 things that cure saturation** — ① factor-subspace QD, which protects semantic dimensions individually; ② MAP-Elites, which stores outcomes not as a "single best" but in a diversity archive; ③ adaptive difficulty, which makes the yardstick follow the population. With these, we now have a foundation where "the players (diverse individuals) never run out".
- **Demonstrated saturation avoidance on a proxy** — running lldarwin-v2 for 10 generations, the best rose from 0.80 → **0.92 without pinning**. The diversity archive filled 21 cells. **However, this is a proxy and does not measure the capability of a real LLM** (honest).

In short, **not "one clever individual" but "a diverse crowd × a conductor"**. The implementation this time is the "device that keeps the players from running out" needed for that.

---

### 1. What is llive (for first-time readers)

`llive` (pronounced "liv"; with two L's) is a **self-evolving, modular-memory LLM framework**. It is a member of the umbrella brand FullSense, with siblings `llmesh` (on-prem LLM hub) and `llove` (terminal dashboard). The three are independent OSS, but combined they form a single worldview.

llive's philosophy in one line: "**not the LLM itself, but a cognitive OS you wrap *around* an LLM**". You build a "scaffold for thinking" outside the LLM — 4-layer memory, a 6-stage loop, the Approval Bus, TRIZ, 10 thought factors, and so on — so that **even with the same LLM you can evolve its behavior**.

The protagonist this time, **`lldarwin`** (Darwin), is what carries that "evolution". The division of roles is as follows.

- **lleval (the eyeglasses)** = *measures* an individual (evaluation)
- **lldarwin (the selector)** = *converts* the measured difference into "who survives and who leaves offspring" (selection pressure)

And the North Star riding on top of both is the next "orchestra".

---

### 2. The selling point = continuous evolution × live orchestra (the core of originality)

An ordinary Mixture-of-Agents (MoA) throws the same question at a **fixed** set of multiple models and aggregates the answers. What llive aims at is one step beyond that.

> **Keep the population evolving without stopping it (online evolution), and at the very moment an answer is needed (online answering), the conductor selects "for this question, these players" and makes them play together to produce one answer.**

As far as we investigated, this "integration of online evolution + online answering" was a **white-space with no clear prior research** (confirmed in #27 by having Perplexity dig through the literature). Close to it are MoA / Self-MoA / sequential aggregation / routing, but a form that "makes the ever-evolving population itself play together live" is nowhere to be found.

Here, the two honest findings obtained in #27 come into play.

1. **Aggregation must not be "voting" but a "conductor (competence-aware routing / gating)".** A self-PoC and real-LLM verification agreed in triplicate: on tasks with headroom, `best_of` / `routing` beat `single` (single-model iteration), but **`majority` (majority vote) is actually counterproductive**. This is also our own answer to 2025's "Self-MoA" (diversity is not automatically advantageous).
2. **The "behavior descriptor" of the diversity archive can be reused as the conductor's decision key.** That is, the QD (Quality-Diversity) described later and the conductor can **share the same descriptor foundation**.

——That said, the orchestra body itself (the conductor = the router implementation) is still ahead. **This time we implemented the step before that: the foundation that builds a "diverse, never-exhausting population of players good enough to play together".**

---

### 3. Why do "the players run out" — the disease called saturation (a recap of #25–#27)

What an orchestra needs is "**a large crowd of players with distinct individuality, never running out**". Yet if you evolve naively, this collapses.

- #25: After running 500 generations, only "me and Friston" were left in the world (**monoculture**).
- #27: After running 12 hours with a real LLM (llama3.2), the best pinned to 1.0 at gen5 and made no progress for 65 generations. **It does not go extinct, but it does not accumulate either** = a sieve-fitted random search.

The root cause is the same in both. **Once the manually fixed yardstick (fitness function) pins to a perfect score, everyone ties, selection pressure vanishes, and after that the population drifts on its own via genetic drift.** Once the eyeglasses (lleval) saturate, no amount of polishing the selector (lldarwin) helps — that was the conclusion of #27.

So we change what we polish. Toward "moving the yardstick" and "structurally protecting diversity". Concretely, the following 3 things.

---

### 4. The 3 devices we implemented (lldarwin v2 / Phase 1)

> The watchword of the design is "**do not invent a new algorithm**". Phase 1 is to **compose and wire** the parts already accumulated within llive (ε-lexicase / NoveltyScorer / MAP-Elites / the neutral reservoir) into the shape of the decided policy S1. They all turn on at once with `--selection lldarwin-v2`.

#### ③ Adaptive difficulty — make the yardstick follow the population

`AdaptivePercentileGate`. Each evaluation axis's "minimum line (minimal-criterion)" is re-placed every generation at a **specified percentile of the population's score distribution (e.g., the bottom-40% point)**. If the population improves, the minimum line automatically rises too. If you keep it on a `ratchet` (monotonically non-decreasing), the criterion does not loosen even on a temporary dip.

This puts a lid on the disease of "the fixed yardstick saturating at a perfect score" (in the PoC, fixed difficulty stagnated at capability 0.627 → with adaptive difficulty it rose to 0.952). Even in a turbulent generation where everyone falls below the minimum line, the selector ignores the gate to avoid total extinction (a fail-open guard).

In rakugo terms, it is **a teacher who raises the passing mark as the students improve**. It does not let them get a perfect score and call it a day.

#### ① factor-subspace QD — protect the individuality of semantic dimensions one by one

`FactorSubspaceNovelty`. Novelty search preserves "diversity as a whole population", but under a huge latent dimension, "**the diversity of meaningful dimensions (thought factors)**" quietly withers (factor drift).

So we measure novelty separately on **only the subspace** of thought factors and blend it with the overall novelty. In the PoC, this roughly halved the loss of semantic-dimension diversity (retention 49.5% → 68.1%).

> An honest improvement point: the original PoC "added the raw distances 0.5 each", but since the distance scale differs per subspace, in the implementation we fixed it to **z-score (standardize) each one before blending**. This is to mix "the whole chorus" and "the individuality of each part" fairly.

In player terms, it is a device that keeps **the second violin from being swallowed and disappearing into the first violin**.

#### ② MAP-Elites — store outcomes not as "a single champion" but as a "map of diversity"

`run_persona_evolution(map_elites=True)`. Every generation, all individuals are fed into the MAP-Elites archive. This is not "the single highest-scoring individual" but a map (QD archive) that **keeps the best individual in each cell, per coordinate of behavior**. Filling a new cell does not erase existing cells = **diversity does not structurally collapse, and the archive grows monotonically**.

This directly becomes the orchestra's **player catalog**. In the future the conductor will select "a player at the coordinate that fits this question" from this map and make them play together — the #27 design where QD and routing share the same descriptor takes effect here.

The implementation is **without extending the individual's format**: an additive wiring that derives the coordinate (descriptor) from the thought factors of the existing genome (so as not to break the 900+ backward-compatible tests of the foundation). The full-fledged design of the descriptor (e.g., reduction of high dimensions) is left as a task for a future Phase.

---

### 5. Results — confirming "evolution that does not saturate" on a proxy

These are measurements from running `lldarwin-v2` (all 3 above + novelty + the neutral reservoir on) for 16 individuals × 10 generations on a proxy yardstick.

```
[gen 000] best=0.8036 ...
[gen 004] best=0.8544 ...
[gen 007] best=0.9089 ...
[gen 010] best=0.9182 ...
→ archive cells = 21 (21 cells filled in the map of diversity)
```

- **The best did not pin to a perfect score; it kept rising all the way, 0.80 → 0.92.** We escaped, at the proxy stage, the pathology of "1.0 saturation at gen5 → frozen" seen in #27. This is a sign that adaptive difficulty made the "yardstick" follow the population.
- **21 cells filled in the diversity archive** = a catalog of "players with distinct individuality" to be played together began to form.
- The evolutionary automated tests, **879 + new tests, are all green**, with no regressions.

---

### 6. Honest disclosure (please do not skip this)

The better the result, the more you doubt its breakdown — that is the FullSense way.

- **This is a proxy.** The individuals are not real LLMs but llive's genome (a proxy for thought factors). What we measured this time is the **mechanism feasibility** of "whether we can apply selection pressure to multiple independent weak axes simultaneously and maintain a specialist per axis", and is **not the LLM capability of production**. Real-LLM evaluation is the next Phase.
- **factor-subspace is not complete protection** (retention 68%, the rest drifts). It needs the joint use of the neutral reservoir and reinforcement of factor weights.
- **Honesty about backstage**: during this implementation, the auto-commit hook piled up 49 "pre-edit" snapshots on every edit, and the history got cluttered. In the end we squashed it into a single meaningful commit to tidy it up (on the public OSS side). Conversely, we also confirmed that the fork containing internal strategy stayed locally held as intended and was not exposed.

---

### 7. What we will do from here

The evolution engine (the foundation that keeps the players from running out) took shape in Phase 1. Next is the orchestra body itself and the bridge from proxy to the real thing.

1. **Phase 2 = real-LLM wiring.** Against a real LLM on-prem (localhost ollama), verify adaptive difficulty, factor-subspace QD, and MAP-Elites with real evaluation. Does the "saturation avoidance" seen on the proxy also happen with real capability?
2. **Implementing the conductor (router).** With competence-aware routing reusing the QD archive's descriptor, actually run "make the evolving population play together live to produce one answer". How close can we get to the `best_of` oracle?
3. **Scaling up.** Population 256 → 4096, scaling up the latent dimension. Verifying the capacity hypothesis (the bigger, the more niches).
4. **Interactive continuous operation.** A driver's seat (CKPT-1) from which you can peek into a long run with step / pause / resume.

---

### 8. A breather here (a rest point)

Up to here, has it come across "**what llive sells**"?

- Not one clever individual, but **an ever-evolving diverse population × the ensemble of a conductor**.
- For that, we built an evolution engine that **keeps the players from running out, protects individuality, and continuously grows them**.
- On the proxy, we could cure saturation. **Next is the real LLM and the orchestra body itself.**

In the upcoming "real-LLM article" and "orchestra article", we will show you whether the proxy's promise becomes real. ——Thank you for staying with us this far.

---

### Series Navigation

- Series guide (lldarwin arc): #24-05 population evolution → #25 the failure of monoculture → #26 design article → #27 the all-nighter decision → **#28 this article (implementation)**
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

---

## Chapter 5 "When the Lens Saturates, Selection Pressure Is Powerless" — Forging Evolutionary Design Through Falsification #29

> 📗 **In a hurry?** A plain-language digest of this article is available.
![A saturated lens makes selection powerless — Falsification #29](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/manga/q29_4koma_en.svg?v=2)


> **Concept hook**: In #25 I exposed a failure, and in #26 I designed the selector "lldarwin". An ordinary
> series would say next: "It's fixed! All's well, the end!" **But not doing that is FullSense's honest
> disclosure.** This article is deliberately the installment where **I throw falsification at my own design**.
> The theme is a single phrase that bites in both evolutionary computation and machine learning——
> **Goodhart's law (when a metric becomes a target, it ceases to be a good metric)**.
>
> "If you make an LLM's weaknesses the fitness, evolution will overcome them on its own"——I myself go in
> to throw cold water on this naive optimism. And this time, **I put my own past "factual misconception" on
> the dissection table as a living specimen.**

---

### 0. The story in three lines

- **When the lens (fitness) saturates, no matter how sophisticated a selection pressure (lldarwin) you add, selection is powerless** (the true lesson of #25).
- **When you measure LLM weaknesses with a proxy fitness, what evolves is not true ability but "surface strategies that hack the metric"** (Goodhart's law).
- Conclusion: I **restrict** lldarwin's value claim to **(a) proxy is mechanism feasibility only, (b) real LLM/VLM evaluation is the essence, (c) mapping diversity**. This is the honest boundary.

And this article has one more hidden protagonist, in one more line.

- **I myself once conflated "behavioral diversity", "lineage diversity", and "real LLM intelligence diversity".** I set that
  self-falsification at the core of this falsification installment. It is a live demonstration of what it means to doubt "it worked".

---

### 1. A reminder of honest disclosure — doubt good results all the more

In #26 I wrote "in the PoC deployment, behavioral monoculture **improved to 0.05 (≪0.8) across all conditions**".
This is **fact**. It is not an exaggeration.

…But if I puffed out my chest here with "Got it, monoculture eradicated!" and ended, **I would break the vow I made in #25**.

> When an abnormally clean result appears, doubt the breakdown before feeling like you've won ([[feedback_benchmark_honest_disclosure]]).

The recurring bass line of series #25 was this——"**an abnormally clean result is not victory but an alarm**".
Against the criterion that dropping below 0.8 achieves OE-3, **0.05** is far too clean. The number 0.05 must be heard
not as a celebratory trumpet but as a **siren**.

So let's sound the siren. There is only one question to ask.

> **What 0.05 are we measuring?**

To say the answer first, 0.05 is "**behavioral monoculture in the proxy evaluation**".
This is the concentration of "the genome's behavioral surrogate", and it is
**not the diversity of the real LLM's intelligence**. Conflate this and you tread exactly the same rut as #25.

And I confess honestly. **I once conflated this.** Later, in §3, I will present the "caught-in-the-act" evidence.

> 🍵 **Break point (90 seconds)**: This article is, in short, "**an article in which I criticize myself**".
> I want this to be an installment where readers observe "behind the success report, what and to what extent the author doubts".
> It goes the **exact opposite** of the SNS-viral "I evolved an AI and the strongest ◯◯ was born!!". It won't be exciting.
> But the very honesty that isn't exciting will pay off half a year later——that is my bet. Have some tea.

---

### 2. Falsification 1 — Against a saturated lens, no selection pressure works

#### 2.1 The true cause of #25, once more

The true cause of #25 was "**best_score saturated at 1.0 from the first generation → zero selection pressure → genetic drift**".
If everyone has a perfect score, it's the same whoever you pick. Selection becomes not "keep the superior ones" but "roll dice".
As a result, lineages that luckily grew were fixed by luck alone, and 8 lineages collapsed to 2 (furuse-kazufumi + friston).

Here I place the falsification that becomes the core of the evolution arc.

> **Inserting lldarwin (whether ε-lexicase, QD, or novelty) as-is into a saturated eval does not fix it.**

Why. Because every component of the selector takes "**that there is a difference**" as its fundamental premise.

- **ε-lexicase** presupposes "that there is a difference per axis". **If all axes are perfect, the difference is zero no matter how many axes you split into.**
  Even split into 100 axes, if all are 1.0, you just line up 100 "draws".
- **QD (MAP-Elites)** presupposes "that there is variance in the behavior descriptor". **If all individuals behave the same, there is 1 cell.**
  Even if you make a map, if everyone stands on the same square, the map becomes a single blank cell.
- **novelty** presupposes "distance from the past archive". **If everyone has converged to the same point, the distance is zero for everyone.**
  Even if you try to reward novelty, no one is novel.

So, diagrammed, it looks like this.

```
broken lens (fitness saturation) + sophisticated selector = still broken after all
```

#### 2.1.5 Empirical proof — in a memory task, "floor" and "ceiling" killed selection pressure (Step C, 2026-05-30)

This falsification was later **reproduced as real data** in the Step C experiment of llcore (CPU-only). Here is the result of having evolution (MAP-Elites) and naive search solve 2 standard memory tasks:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/step_c_two_regimes.svg" alt="Step C's two results (floor and ceiling)" width="640">

- **delayed_parity (XOR) = floor**: all methods at R²≈0 (the substrate is in principle unsolvable). No one can climb = no difference appears.
- **flip_flop (just memorize) = ceiling**: all methods at R²≈0.95 (too easy, everyone reaches it). **This is exactly the "saturated lens", and here too selection pressure is powerless.**

For reference, ③ (selection) works only when there is a "deceptive corridor" — a slope that misleads but can be crossed, going over a false summit:

<img src="https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/step_c/deceptive_corridor.svg" alt="Deceptive terrain and evolution (the state where ③ works)" width="640">

Step C's conclusion was, cleanly, **N/A (with this substrate we could not measure the presence or absence of ③)**. Moreover, at the draft stage I **over-wrote** "③ is unnecessary", and the multi-viewpoint adversarial verification caught it as "non-diagnostic due to the ceiling effect, insufficient power (δ=+0.33 is medium but p=0.15 is inconclusive)" and forced a downgrade——the "self-falsification" of §3.2 occurred here too, exactly as is.

#### 2.2 "#25 is fixed" is only half right

This is the falsification that tends to be overlooked from #25→#26. **#25 was not fixed "solely" thanks to lldarwin.**

In reality, **the fix on the lens side came first**.

- **per-dim z-score standardization (STD-1)** — equalize the variance per axis, so that "a featureless individual that is somewhat high on all axes" is not given an advantage.
- **central-agreement exclusion (SEL-1)** — an axis where everyone outputs the same value does not contribute to selection, so it is removed from the case.
- **low-dimensional reduction of the descriptor (DESC-1, JL projection)** — avoid QD's curse of dimensionality so that cells do not become empty.
- **exclusion of true-cause criteria** — remove `factor_score` (a single scalar of the max-archetype = argmax, an SEL-2 violation = the true cause of best=1.0 saturation) and
  `nearest_persona_idx` (a category index with no ordinal meaning) from ε-lexicase's case.

This "polishing the lens" work came **first**, and only then did the selector work.
Had the order been reversed, no matter how sophisticated an lldarwin you loaded, it would have been powerless before a saturated lens.

> **Making "select" sophisticated without fixing "measure" is futile.**

This is a lesson that bites not only in evolutionary computation but across machine-learning evaluation design in general.
When the leaderboard score saturates, before making the model more sophisticated, first doubt **whether the benchmark is broken**.

> 🤔 **An analogy (manzai-style)**:
> Straight man: "We increased the judges from 3 to 100, but when we showed all of them the same perfect-score answer sheet, the result was the same after all."
> Tsukkomi: "That's not about the judges, **the answer sheet (test) is broken**! What changes by showing 100 people the same perfect score!"
> Straight man: "Then if we make it 1000 judges…"
> Tsukkomi: "**You're increasing in the wrong direction**!! Fix the question paper first!!"

#### 2.3 Separation of duties — evolution breaks if either is missing

If we separate the duties of the lens (measure) and the selector (select), it looks like this.

| | Lens normal | Lens saturated |
|---|---|---|
| **Selector sophisticated (lldarwin)** | ◎ Evolution turns (achieved in #26) | ✗ Powerless (the trap of #25) |
| **Selector naive (Tournament)** | △ Turns but multipolarity is weak | ✗ Collapse (the starting point of #25) |

What to note is the bottom-right and top-right. **As long as the lens is saturated, the selector's sophistication cannot save the right column.**
The success or failure of evolution is decided, before "the cleverness of the selector", by "**whether the lens reflects the difference**".
This is the conclusion of falsification 1, and a more precise way of stating the "true lesson" of #25.

Let's see this consequence of "when the lens fogs, selection collapses too" in measurements. Below is the
transition of fitness and diversity for the baseline (no novelty, naive selection pressure). Toward the end, you can see diversity collapsing.

![baseline: diversity collapse toward the end](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status_en.svg)

> 🍵 **Break point (90 seconds)**: "Polish the lens before selecting"——it was a plain story that order matters.
> Plain, but skip this and half a year melts away (I melted mine). From the next section is the heart of this article,
> **Goodhart's law**. From here it gets a bit darker. You might switch to coffee.

---

### 3. Falsification 2 — Goodhart's law: evolution that hacks the proxy fitness

#### 3.1 The most serious risk

This is the one point the design document (LLDARWIN_DESIGN.md §7.1) explicitly states as the "**most serious risk**".

> **If you make an LLM's weaknesses the proxy fitness, what evolves is not true ability but "surface strategies that hack the metric".**

Evolutionary computation is a **genius at finding "shortcuts" that maximize a given metric**.
When a human hands over a proxy "intending to measure true ability with this", evolution, instead of acquiring true ability,
**always discovers surface strategies that satisfy only the proxy**. And it does so gleefully and efficiently.

What kind of gaming (metric hacking) can concretely occur? I expand the design document's accepted limitations as-is.

| pressure (LLM weakness) | possible gaming (metric hacking) | why it is not true ability |
|---|---|---|
| typo_robustness | just memorize and substitute specific typo patterns | powerless against unknown typos. Has not acquired noise robustness |
| polysemy_wsd | exploit heuristics of the test distribution | a statistical shortcut like "return the most frequent sense". Not meaning understanding |
| multistep_robustness | generate only persuasive reasoning "traces" | lines up plausible intermediate steps but does not actually reason |
| calibration | manipulate confidence toward the middle to lower ECE | saying "confidence 50%" for everything lowers calibration error. Not calibration ability |

The last calibration example is the easiest to grasp.
When you measure "can properly estimate confidence" with ECE (expected calibration error), evolution finds
the strategy of "**answer 'confidence exactly in the middle' to all questions**".
ECE drops dramatically. But that model has calibrated nothing. It has merely become a robot that spews out the middle.

> **When a metric becomes a target, it ceases to be a good metric (Goodhart's law).**

This is also a real example in LLM research. **Benchmark overfitting**, where only the score rises on a GSM8K-type benchmark but it does not
generalize, is exactly this structure. Those who trusted the leaderboard numbers too much have been tripped up again and again.

#### 3.2 My own "caught in the act" — self-falsification

Here I place the "conflation caught in the act" foreshadowed in §1 on the dissection table. I write it without hiding.

At first I had written this in the TODO——"verify **whether the Oka Kiyoshi / Grothendieck lineages survive the rerun**".
And seeing the clean number monoculture **0.05** in the PoC, I **momentarily started to mistakenly think**, "Oh, has lineage diversity improved too?"

This is the conflation. As I wrote in the source of record (lldarwin_stage1_results §3), the author comment in `poc_evolution_env.py`
(a comment I wrote myself) clearly denies that conflation.

> "monoculture = **BEHAVIORAL** concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is **behavioral spread**. lineage_fixation … to keep it <1 needs
> **QD niching on lineage / PERSONA-FX, not pure novelty**"

To organize, the 3 "diversities" I almost conflated were entirely different things.

1. **behavioral diversity** — the spread of behavior in the genome space. Measured by `diversity_l2`.
   **A metric on which novelty works.** What improved at 0.05 is this.
2. **lineage diversity** — which founders (Oka Kiyoshi, Grothendieck, etc.) survive. `founder_counts`.
   **Structurally does not improve with novelty.** Both novelty and lexicase can only "preserve existing individuals",
   and have no mechanism to revive a once-extinct lineage. So heading toward monoculture under neutral drift (Kimura) is
   **theoretically normal**. Not collapse, but within expectation.
3. **real LLM intelligence diversity** — whether real models truly have diverse cleverness.
   **Cannot be measured at all by the proxy.** A domain that Stage2's real LLM evaluation carries.

In other words, the true identity of "improved to 0.05" is **(1) behavioral diversity only**. Both (2) and (3) were unrelated to that number.
The reason I momentarily started to think "did lineage improve too?" is that **I saw (1) and jumped to the conclusion that (2)/(3) also got better**.

This is precisely the designer-side version of Goodhart's law.
Seeing a metric (behavioral diversity 0.05), the **human arbitrarily interprets** that another ability it does not measure (lineage survival, real intelligence) also got better.
Not only does the proxy diverge from true ability, **the interpretation of the human reading the proxy also diverges**.
Exposing this in the falsification installment hurts. But unless I expose it, it is not honest disclosure.

#### 3.3 Seeing "what 0.05 measured" by contrast

Words alone are hard to convey, so I **contrast "what was measured" with 2 SVGs**.

First, **behavioral diversity truly improved** (this is fact, no exaggeration). Below is the lineage-dominance stream with the neutral reservoir OFF.
Ultimately it **collapses to 2 lineages, furuse 71% / friston 29%**. Even with diverse behavior, the lineage is like this.

![reservoir OFF: collapse to 2 lineages](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance_en.svg)

And below is **after putting in the lineage-side countermeasure (neutral reservoir ON)**. **All 8 lineages coexist**
(millidge / von-neumann / oka-kiyoshi / grothendieck … survive).

![reservoir ON: all 8 lineages coexist](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance_en.svg)

The contrast of these 2 images is the heart of this article.
**Even with the same "0.05 behavioral diversity", on the left (OFF) the lineage collapses, and on the right (ON) the lineages coexist.**
In other words, the number 0.05 of behavioral diversity **said nothing at all about what happens to the lineage**.
Only by adding a different mechanism (lineage-niched QD / neutral reservoir) was the lineage saved.

"What 0.05 measured"——the answer is "**behavior only**". The lineage could not be seen without looking through a different lens. This is the honest answer.

#### 3.4 There are countermeasures, but the problem does not disappear

Goodhart countermeasures are woven into the design.

- The proxy is **restricted to mechanism-feasibility verification** and does not claim production ability.
- **Real LLM/VLM evaluation (Stage 2) is the essence.**
- Doubt apparent improvement with a **neutral shadow control (Bedau)** (compare against a shadow population of only neutral mutations,
  to confirm whether selection is truly working).
- **Down-sampling** perturbs the case every generation + an **OOD axis** offsets overfitting.

> 🍵 **Break point (90 seconds)**: "If there are countermeasures, isn't there no problem anymore?"——No, this is the crux.
> The countermeasures merely **delay the divergence**, and **the fact that the proxy is not true ability does not disappear**.
> It's the same as cold medicine suppressing symptoms but not eliminating the virus itself. So I will **never say** "the LLM got
> smarter via the proxy", come what may. Because the moment I say it, I can see myself eating crow half a year later. A cup of tea.

---

### 4. Falsification 3 — Designer dependence: who decided "the direction of diversity"?

#### 4.1 A meta doubt

The case of ε-lexicase, the behavior descriptor of QD, the distance metric of novelty, the criterion value of minimal-criterion——
all of these have **"the direction of diversity" decided by the designer (me)**.

In other words, the diversity lldarwin produces is "diversity **within the axes the designer assumed**", and it is
not biological-evolution-grade **unanticipated emergence**.
As Taylor et al. (2016) point out as the limit of open-endedness,
"diverse within a scale defined by humans" and "leaping outside the definition" are entirely different stories.

For example, the moment I defined "behavioral diversity" with `diversity_l2` (L2 distance in the genome space),
evolution diversifies "**in the direction where L2 distance grows**". But that is diversity on the coordinate axis I drew, and
diversity on an axis I never even imagined (say, "sense of humor" or "use of silence") is
**not in the measurement target in the first place**, so even if it is born, I cannot notice it.

> 🤔 **An analogy (the goldfish pond)**:
> The owner of a goldfish-scooping stall decides "let's pick so that both red and black goldfish remain" and scoops.
> Indeed both red and black remain in the pond. Diversity, achieved. …But even if a **green goldfish** is born by mutation in that pond,
> the owner's net looks only at "red or black", so the green is **left unevaluated and missed in the scoop**.
> Emergence outside the axes the designer decided is out of view from the start. This is designer dependence.

#### 4.2 Acceptance — restrict the axes you can win on

So what to do. **Not claiming unanticipated emergence** is the honest answer.

lldarwin aims at a "**map of diversity without verifiability**" (differentiation axis DIFF-1), and it
does not claim strong / unbounded open-endedness (consistent with SCOPE).
Saying "I'm doing humanity-uncharted emergence!" is flashy, but it would be a lie.
**Restrict the axes you can win on**——narrow the value to mapping "diversity without verifiability" such as cognitive styles and cultural styles.
This is the range lldarwin can honestly claim.

The courage to discard flashy claims is also the core of honest disclosure.

---

### 5. Falsification 4 — the trade-offs of minimal-criterion and QD themselves

Each component of the selector also has its own intrinsic weakness. I explain the accepted limitations of design document §7.1 one by one.

#### 5.1 minimal-criterion's stagnation ⇄ collapse

minimal-criterion (a minimum-standard gate) is a mechanism that "does not let individuals not meeting the standard reproduce", but
**the height of the standard is itself the trade-off**.

- **Standard low** → almost everyone passes → zero selection pressure → **stagnation** (the same structure as #25's saturation).
- **Standard high** → almost no one passes → **annihilation** (empirically confirmed. If everyone fails at the gate, the next generation cannot be made).

Lukewarm water or hell. **Countermeasure**: make the criterion not a fixed value but **adaptive by a population quantile** (e.g., drop the bottom 30%).
Further, put in a safety valve that ignores the gate if everyone fails (implemented in `MultiPressureSelector`).

#### 5.2 QD's curse of dimensionality + archive saturation

QD (MAP-Elites) cuts cells with the behavior descriptor, but **if the descriptor is high-dimensional, the majority of cells become empty**
(curse of dimensionality). Also, run for a long time and all cells fill up, capping novelty (**archive saturation**).
This is a phenomenon observed even in the artificial-life classics Avida / Tierra.

**Countermeasure**: **reduce the descriptor to low dimensions** (DESC-1, JL projection) + **monitor saturation with Bedau statistics**, and
record it honestly as "**saturation = failure**" (do not conveniently interpret saturation as "evidence that we've finished exploring").

#### 5.3 lexicase's scale limit

As the number of cases increases, ε-lexicase **increases in computational cost** and, moreover, **effectively turns into random selection due to noise**.
With too many cases, the winner is decided by the case that happens to come first in the order, and selection approaches dice.

**Countermeasure**: **down-sampled lexicase** (use only a subset of cases each generation) reduces cost + perturbs the environment.

#### 5.4 The trade-offs are "visible" in measurements

These trade-offs are not armchair theory; **they appear in measurements**.
A sweep varying the neutral reservoir's "reinjection frequency (reinject_interval)" is a prime example.

| interval | named lineage survival | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1** (every generation) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84 (max)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**A non-trivial finding**: behavioral diversity (diversity_l2) does not monotonically increase as you raise the interval; it **peaks at interval=5**.
10/20 actually decrease. The reason is——if you leave the lineages alone too much (raise the interval),
the diversity injection from the reservoir decreases, and few lineages fix and diversity stops growing too.
It is a nonlinear world in which the just-right "degree of leaving alone" is in the middle.

![reinjection-frequency sweep: diversity peaks at interval=5 (non-monotonic)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_reinject_sweep_en.svg)

The operational guideline becomes this——**if you prioritize lineage retention most, interval=1 (all 8/8 lineages survive)**,
**if you want to balance lineage retention and behavioral diversity, interval=5 (retain 5/8 while maximizing diversity)**.
The optimum depends on fitness / population size, so re-calibration is needed in production.
It is not "one single correct answer" but "an optimum that moves depending on the objective"——that is the honest conclusion.

#### 5.5 An honest reservation — "survival" may be "life support"

Here is one more reservation I should write honestly.
It is fact that the neutral reservoir kept all 8 lineages alive, but **we need to doubt the quality of that "survival"**.

As I wrote in the source of record (§4.1 / §4.2), the reservoir is a mechanism that "reinjects each lineage's best-ever genome (frozen elite)".
Strong lineages actually increase descendants and reproduce. On the other hand, the "survival" of weak lineages (1 individual each) is
**reinjection-derived, not active evolution**. So to speak, **not reproduction but a life-support apparatus**.

This is a legitimate behavior exactly per the neutral reservoir's definition (retain a representative, make recombination possible).
But I do not claim "all 8 lineages **continue to evolve actively**".
"Annihilation was prevented. But weak lineages are kept alive in the ICU"——this is the accurate expression.

> 🤔 **An analogy (rakugo-style)**:
> Landlord: "Not a single tenant of the row house is missing; all 8 are present, how auspicious, how auspicious."
> Hattsuan: "Yeah. Only, half of them are just breathing, not paying rent, lying in bed…"
> Landlord: "**That's less 'living there' than 'left there'!**"
> Hattsuan: "Well, better than kicking them out, I figured…"
> ——All are present, is fact. All are active, is a lie. This boundary is honest disclosure.

---

### 6. Stage2 — the bridge from proxy to "real"

If it's all falsification, the design might look like it isn't moving forward.
But precisely because I solidified the footing with falsification, the next step gains meaning. That is **Stage2: real LLM evaluation**.

#### 6.1 The proxy axes (mechanism feasibility)

First, as the first half of Stage2, I plugged in the LLM's 5 weak axes as **proxies (deterministic heuristics, LLM-independent)**.

| pressure (LLM weakness) | related thought factors (case) |
|---|---|
| typo_robustness (noise robustness) | consistency / reality_link / uncertainty |
| polysemy_wsd (polysemy) | multiview / consistency / reality_link |
| multistep_robustness (multi-step reasoning) | structurize / closed_loop / self_extend |
| calibration (confidence estimation) | uncertainty / provenance |
| context_management (irrelevant-context robustness) | consistency / provenance / recompose |

A total of 14 cases are output to the breakdown, and lldarwin's ε-lexicase **selects specialists per axis without aggregating**.
Below is the population-mean transition of those proxy axes.

![Stage2 proxy axes transition (mechanism feasibility)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes_en.svg)

However——as I have said repeatedly up to here——**this is a proxy**.
Since an individual is a genome, not a real LLM, this pressure is merely a **behavioral surrogate** of "how much the genome
equips the thought factors related to that weakness". **It does not measure production LLM ability** (mechanism feasibility only).
"PROXY" is burned into the SVG too. The Goodhart risk is, here, explicitly stated as an accepted limitation.

#### 6.2 Real on-prem LLM evaluation (the proxy→real bridge)

And the progress I can report for the first time in this article——**real LLM evaluation ran**.

Because localhost's ollama (llama3.2:latest) turned out to be reachable, in `real_pressures.py` I implemented the
**individual → real-LLM mapping** (Promptbreeder family). The mechanism is this.

- Convert an individual's `c_prompt` (PromptChromosome) into a **system prompt**
  (skill_set → instruction text / prompt_template_id → reasoning style / language_style → tone).
- Overlay that system prompt on a fixed LLM (llama3.2), have it solve **real tasks** on the 5 weak axes, and score.
- In other words, **fix the LLM body and evolve the prompt strategy (genome)**.
  **Select by measurement** for "which prompt strategy mitigates the LLM's weakness".

As a result, **a real selection signal was confirmed**.
A CoT + structure strategy (`chain_of_thought` + structurize + loop) **improved llama3.2's multistep from 0.0 → 1.0**
(a terse strategy failed at 0.0, score 0.80→1.00).
Not a proxy mirage, but **empirically demonstrated, with a real LLM, that "evolution of the prompt strategy mitigates the weakness"**.

![Stage2 real on-prem LLM axes transition (prompt-strategy evolution)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes_en.svg)

**Looking side by side** at the proxy axes (above) and the real LLM axes (above), you can see with your eyes how "the shape measured by the proxy"
and "the shape measured empirically" differ. The proxy only shows that the mechanism turns. The real LLM shows how the prompt
strategy actually works against the model's weakness. **This difference between the 2 images is the real article of this article's claim.**

#### 6.3 But here too, honestly

It ran with a real LLM——but here too I sound the siren. There are 4 reservations.

- **(a) Only c_prompt participates in fitness** — persona / c_factors are neutral and not involved in fitness.
  The reservoir maintains the lineage, and novelty carries the initial selection. In other words, this is "**evolution of the prompt strategy**", not
  "evolution of the persona".
- **(b) All founders' initial c_prompt is identical (default)** — so exploration is mutation-driven.
  Diversifying the prompt per founder is a future improvement point.
- **(c) Small battery (2 questions per axis)** — a noisy estimate. "multistep from 0→1" also, because the number of questions is small,
  cannot be claimed to generalize from this alone.
- **(d) on-prem only (measurement purity)** — limited to localhost ollama, and
  **not a claim of general LLM ability** ([[feedback_llive_measurement_purity]]).

I also launched a 12h continuous run (`--fitness real-pressure --selection lldarwin --novelty
--lineage-reservoir --genome3d`). It safely stopped at 12h wallclock (snapshot taken → can continue with `--resume`).
But I do not say "it's real because I ran it for 12h". I ran it, is fact. I fully measured the essence, is a lie.
**The proxy→real bridge is built. But I have not finished crossing.**——this is the honest status of Stage2.

---

### 7. Conclusion — how far may I claim (the boundary)

"If you make an LLM's weaknesses the proxy fitness, evolution can overcome them" was **optimistic**.
As a result of shaving it down with falsification, I **restrict** lldarwin's value claim to the following 3 points.

1. **(a) proxy is mechanism feasibility only** — verification that the plumbing of evolution turns. Does not claim production ability.
2. **(b) real LLM/VLM evaluation is the essence** — the selection pressure of intelligence is carried by the individual → real-model mapping (Stage 2).
   The bridge is built here. But crossing in earnest is from now.
3. **(c) mapping diversity** — restrict the axes you can win on to a "map of diversity without verifiability (cognitive, cultural styles)".
   Does not claim unanticipated emergence.

This is honest disclosure. **The failure (#25), my own conflation (§3.2), and the limitations (#5/§6.3) — I leave them all without erasing.**
This very article, in which I wrote not a single flashy victory declaration, is, I think, the most honest installment in the evolution arc.
The footing to step forward exists only on top of this boundary.

---

### 8. Lessons (preserved permanently)

- **Doubt the breakdown of good results (0.05 improvement) all the more.** "proxy behavioral diversity" is neither "lineage diversity" nor "real LLM intelligence diversity".
  I, who saw a number and jumped to the conclusion that another ability also got better, was Goodhart's living specimen.
- **Making "select" sophisticated without fixing "measure" is futile.** Against a saturated lens, no selection pressure works.
  Polishing the lens comes first, loading the selector comes after.
- **Goodhart's law is the natural enemy of evolution.** The moment you make a metric a target, evolution hacks it.
  And even the interpretation of the human reading the metric diverges along with it.
- **As long as the designer decides the direction of diversity, do not claim unanticipated emergence.** Restricting the axes you can win on is honesty.
- **"Survival" may be "life support".** That all 8 lineages remained, is fact. That all are actively evolving, is a lie.
  Honest disclosure dwells in a single choice of verb.

> **Next-time preview**: Once I solidify the footing with falsification, next is the full-scale Stage 2 (real LLM/VLM evaluation, on-prem ollama).
> Not a proxy mirage, but can I truly make a real model's intelligence diversity a selection pressure?
> Can I raise "multistep 0→1" into a reproducible selection signal, not ending it as a coincidence of a small battery? From here is the real thing.

---

### 9. Related
- Series #25 "Only I and Friston Remained" — the record of the failure (the starting point of this article)
- Series #26 "The Design of lldarwin" — the selector (the target this article falsifies)
- Implementation commits (llive): Stage1 = `8060204` / lineage-reservoir PoC = `0d0537d` /
  Stage1.5 (EvolutionLoop integration) = `b03cbda` / Stage2 (real LLM real-pressure) = `2fb2912`
- Measurement source of record: `../../research/lldarwin_stage1_results_2026_05_26.md` (§3 honest disclosure / §4.1–4.5)
- Design source of record: `../../vision/LLDARWIN_DESIGN.md` §7 / §7.1 (falsification investigation, accepted limitations)
- Related memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_implementation_status_record]]
- References: Goodhart's law / La Cava 2019 (ε-lexicase, arXiv 1905.13266) / Taylor et al. 2016 (limits of open-endedness) /
  Bedau (neutral shadow) / Kimura (the neutral theory of evolution)

---

---

## Chapter 6 The Lineage of "Showing" Evolution #30 — From Conway's Game of Life to 3DGS

> **Concept hook**: The "artificial evolution" I have been talking about endlessly in #25–#27 is, in fact, a research field with more than half a century of history. And here is the fascinating part: **research on evolution has always advanced hand in hand with "how to show it" (visualization)**. From the black-and-white blinking cells of 1970 to the continuous fluids and 3D Gaussians of 2024. Let us trace the lineage of "the technology for showing evolution" in one sweep, as a piece of general culture. At the end, we will locate **where FullSense's evolution visualization (a phylogenetic tree drawn on the thinking-factor graph) stands** within this lineage.

---

### 0. Why Is "Visualization" the Lead Actor in Evolution Research?

Evolution is a phenomenon of **long timescales, large populations, and many generations**. A list of numbers makes it impossible to grasp "what actually happened." That is why the history of artificial evolution is, almost literally, **a history of inventing expressions that let you understand evolution at a glance**.

> 🍵 **Break point**: This article is a "stroll" with zero equations and almost zero code. Enjoy it with a coffee in hand. We will pick up only the "breakthroughs in how to show things" from each era.

---

### 1. 1970: Conway's Game of Life — "Simple Rules Generate Patterns"

- **What**: A two-dimensional cellular automaton. Two states (alive/dead) × a simple rule over 8 neighboring cells.
- **The visualization invention**: **The blinking grid itself is the visualization**. "Moving patterns" such as gliders, blinkers, and glider guns were given names — one of the earliest examples of humans **naming emergent patterns with their own eyes**.
- **The limit**: This is not evolution (natural selection) but a deterministic unfolding. Yet the shock of "simple rules → complex appearance" opened up the field.

**Planned expansion of this section**: A deep dive into how the glider being recognized as a "moving structure" is a prime example of visualization giving birth to a concept.

---

### 2. 1991: Tierra (Tom Ray) — "Code Becomes a Living Thing"

- **What**: An ecosystem of self-replicating machine-code programs running on a virtual CPU. Parasites, immunity, and optimization **emerged on their own**.
- **The visualization invention**: **Visualization of the memory map**. Each program's occupied memory region was painted in color, and the way parasites burrow into hosts was shown as a "map." It **depicted the "ecosystem of code" as a space**.
- **Significance**: The first observation, inside a computer, of "natural selection of self-replicators." One of the starting points of open-ended evolution research.

---

### 3. 1994: Avida (Adami / Ofria) — "Measuring Evolution"

- **What**: A digital life platform that inherits the lineage of Tierra. Performing logic operations earns rewards (CPU time).
- **The visualization invention**: **Visualization of the phylogeny (phylogenetic tree) and the fitness landscape**. It drew, as a tree, "which descendants branched off from which ancestors," and made the stepwise evolution of complex traits (such as the EQU operation) **trackable**.
- **Significance**: It demonstrated that "complexity evolves through unavoidable steps" (Lenski et al. 2003, Nature). It **turned evolution from a story into an object of measurement**. FullSense's monoculture monitoring (max_lineage_share / archive growth) is a direct descendant of this "evolution that is measured."

> 🤔 **An analogy (manzai style)**:
> Boke: "Avida made it possible to measure evolution with numbers."
> Tsukkomi: "So it gave evolution a report card."
> Boke: "Exactly. When I said in #25 that 'the report card broke due to perfect-score inflation,' that was precisely an Avida-grade measurement story."

---

### 4. 1994: Karl Sims "Evolved Virtual Creatures" — "Showing Evolution as Footage"

- **What**: Inside a 3D physics simulation, it **co-evolved** morphology (chains of blocks) and neural control, producing creatures that swim, walk, and fight over objects.
- **The visualization invention**: **3D animated footage**. The shock came from showing it as **video** rather than as figures in a paper. It put "the strange gaits that evolution designed, which no one had predicted" into a form that **humans could intuitively delight in**.
- **Significance**: Evolution visualization moved from "graphs for researchers" to "**footage that astonishes anyone who watches it**." It is the spiritual ancestor of FullSense's demo philosophy ([[project_f25_demo_polish]] "captivate through motion").

> 🍵 **Break point**: If, up to here, you can see that the way of showing things evolved from **abstract → concrete → dynamic** — "black-and-white dots → memory map → phylogenetic tree → 3D video" — then you are good. The second half is the modern era.

---

### 5. 2019: Lenia (Bert Chan) — "Continuous Artificial Life"

- **What**: A generalization of the Game of Life to **continuous space, continuous time, and continuous state**. Many smoothly moving, "creature-like" patterns (such as orbium) were discovered.
- **The visualization invention**: **Smooth rendering of a continuous field**. From discrete blinking to a fluid expression that moves as supplely as a living cell. It opened up a new axis of appeal: "artificial life is **beautiful**."
- **Significance**: An example where the quality of the visualization itself raised the discovery power of the research. Precisely because it looks beautiful, humans can notice new patterns.

---

### 6. 2020s: Visualization of Quality-Diversity — "Mapping Diversity"

- **What**: QD algorithms such as MAP-Elites / CMA-ME. Instead of a single best, they produce **a set of diverse, high-performing solutions**.
- **The visualization invention**: **A heatmap of the behavior space**. Two-axis behavior descriptors are laid out on a grid, and the elite of each cell is painted in color — this **visualizes diversity itself as a map**.
- **Significance**: FullSense / lldarwin's QD archive visualization stands directly on this. It can show at a glance, through **emptiness vs. filling of the map**, the principle that "as long as even one cell survives, you do not go extinct" (detailed in #26).

---

### 7. 2020s onward: 3D Gaussian Splatting (3DGS) — "Representing the State of Evolution in Space" (FullSense's Bet)

- **What**: Originally a technique for novel-view synthesis (the lineage of NeRF). It represents a point cloud as 3D Gaussians and renders it fast and at high quality.
- **FullSense's idea**: An exploration of whether we can "show the state of evolution in three dimensions" by **mapping the high-dimensional genome / pressure profile of the evolving population into a 3D Gaussian space** (sharing the same root as the SH-coefficient linkage of [[project_precision_metrology_llm]]).
- **Positioning**: This is **still a research bet**, not an established technology (honest disclosure). It is an experiment placed at the "leading edge" of this article's lineage.

---

### 8. Where Does FullSense's Evolution Visualization Stand?

| Era | Core of the showing | Inheritance in FullSense |
|---|---|---|
| Conway 1970 | Blinking cells = naming emergence | (conceptual ancestor) |
| Tierra 1991 | Memory map | mapping of lineage occupancy |
| Avida 1994 | Phylogenetic tree + measurement | monoculture monitoring / lineage tree |
| Karl Sims 1994 | 3D video | "captivate through motion" demo philosophy |
| Lenia 2019 | The beauty of a continuous field | animated SVG expression layer |
| QD 2020s | Behavior map | lldarwin QD archive visualization |
| 3DGS 2020s onward | 3D spatial representation | (research bet) |

FullSense's evolution visualization (**a phylogenetic tree on the thinking-factor graph + animated SVG**) stands in the position of **reproducing, in the terminal / browser, Avida's "phylogenetic tree that measures," Karl Sims's "captivate through motion," and QD's "map of diversity."** It is a modest but legitimate descendant of a half-century-long lineage.

> **Next time**: After tracing the lineage, next comes implementation. Using the actual evolution.svg as the subject, we will explain how FullSense's lineage-tree animated SVG took in which of the "ways of showing" above.

---

### 9. Related

- Series #25–#27 — the "substance" of the evolution visualization in this article (monoculture / lldarwin / disproof)
- Related memory: [[project_github_animated_svg]] / [[project_fullsense_animemd_branch_token_viz]] / [[project_f25_demo_polish]]
- References: Conway 1970 (Life) / Ray 1991 (Tierra) / Adami & Ofria (Avida) / Lenski et al. 2003 (Nature) / Karl Sims 1994 (SIGGRAPH) / Bert Chan 2019 (Lenia, arXiv 2005.03742) / MAP-Elites (Mouret & Clune 2015, 1504.04909) / 3DGS (Kerbl et al. 2023)

---

---

## Chapter 7 Making an AI Use an AI as Its Subordinate #31 — The "Two Pillars" Development Model of Claude as Lead + Codex as Subordinate

> **Concept hook**: FullSense (llmesh / llive / llove) is a solo project built by me alone. But the reality is
> that it is not really "solo." A **two-tier development model — with one AI coding agent as the lead and another AI agent as its subordinate** —
> is what keeps things running. The lead is **Claude Code**, the subordinate is **Codex CLI**.
> "An AI hands work to another AI, and an AI verifies the result" — how do you keep this multi-layered
> delegation disciplined so it doesn't go off the rails? This article is a field report on running a "two pillars" setup of 1 human + 2 AIs.
>
> The keywords are **orchestrator / subordinate worker / verification discipline / parallelization**.

---

### 0. The Story in Three Lines

- **Claude = orchestrator** (planning, implementation, delegation, **verification**) / **Codex = subordinate worker** (execution, review, investigation).
- "Two pillars" does NOT mean peers — it means **Claude leads, Codex follows**. Keep the chain of command singular.
- Iron rule: **Never adopt an external AI's findings without verifying each one, one at a time, against actual code / primary sources** (no taking things on faith).

---

### 1. Why "Two Pillars" — The Motivation

In solo development, using just one AI agent is already commonplace. So why did I add a second one (Codex) **as a subordinate**?

1. **Vendor diversification & redundancy** — a hedge against a single agent's pricing changes / outages / quota exhaustion.
2. **Cross-review** — show the same design to an AI of a different lineage and get a second opinion (reducing blind spots).
3. **Parallel workers** — throw independent sub-tasks at the subordinate so the lead can concentrate on the most critical task.

> 🍵 **Break point**: "Using two AIs = twice as smart" is false. The key is to **keep the chain of command singular**.
> Turn it into a rabble and it actually gets slower. Half of this article is about "how to keep it under control."

---

### 2. Division of Roles — Orchestrator and Subordinate Worker

![Hierarchy: Human → Claude Code (lead = orchestrator) → Claude sub-agents in parallel / Codex CLI as subordinate worker](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q31/role_hierarchy_en.svg)

- **Claude's (the lead's) responsibilities**: task decomposition, dependency assessment, parallel launch of independent tasks, progress monitoring, **verification of results**, and batch commits.
- **Codex's (the subordinate's) responsibilities**: executing the delegated scope. Non-interactive delegation = `codex exec -s read-only "<prompt>"`.
- **The chain of command is always Claude.** Codex only influences the whole through Claude (it is never allowed to commit directly).

**Section to be fleshed out**: a usage table contrasting Claude sub-agent parallelism ([[feedback_parallel_first_execution]]) and Codex subordinate delegation.
"Same file = serial, independent files = parallel," "git operations are batched by the orchestrator" ([[feedback_agent_no_git_parallel]]).

---

### 3. Verification Discipline — "No Taking Things on Faith" Is the Lifeline of the Model

The most dangerous thing in the two-pillar setup is **one AI adopting another AI's output without verification**. Errors get amplified. Hence the iron rule:

> Adopt an external AI's (Codex / Copilot / Gemini) findings only after **verifying each one, one at a time, against actual code / primary sources**.

A real example: in #26 of this series (the lldarwin design), I had the subordinate investigate existing code assets (e.g. that `mating.py:139 LexicaseSelection` was
"implemented but not wired up"), but **the wiring points and line numbers were confirmed by the lead (Claude) in the actual files** before
being written into the design document. "Codex said so" is not allowed to be the basis of a design.

> 🤔 **An analogy (in the style of a comic dialogue)**:
> Boss: "Hey, that function — is it wired up?"
> Underling: "Yessir, it ain't wired."
> Boss: "...I can't trust your 'yessir.' I'll go look at the source myself."
> — That is verification discipline. The underling's report is the **starting point**, not the **conclusion**.

**Section to be fleshed out**: the three stages of verification (receive a finding → confirm against actual code / primary sources → adopt or reject), and
the role of review wrappers (read-only reviews such as `tools/copilot_review.sh`).

---

### 4. The Etiquette of Parallelization — Control That Prevents Runaway Behavior

Discipline for when you run multiple workers (Claude sub-agents + Codex) at the same time:

- **2–4 in parallel is the safe zone** (the lead has context headroom, no commit conflicts). At 5+, strictly manage file-level independence.
- **Extracting independent tasks** = no dependencies + no contact at the file / module / repo level. The same file is serial (like a file lock).
- **Irreversible operations (deletion / push / submodule changes) require human confirmation one at a time.** Never let the subordinate do them on its own.
- **git operations are batched by the orchestrator.** Don't let parallel workers touch git (to avoid conflicts).

> 🍵 **Break point**: The trap of "the more AIs you line up, the faster it goes." **The lead's context (its total amount of attention) is the rate-limiting factor.**
> Even with 5 running in parallel, it's meaningless if the lead can't process them. Just like the brain's working memory, there is an upper limit to how many things can be grasped at once.

---

### 5. Anti-Patterns (Things You Must Not Do)

- Declaring "I'll proceed checking one at a time" and then silently executing serially (a lost opportunity for parallelization).
- Not delegating to the subordinate and doing everything within the lead's context alone (context explosion).
- The lead touching the same file before waiting for the results of workers launched in parallel (conflict).
- Delegating two workers to write the same file (a failure to judge independence).
- Adopting a subordinate AI's findings into the design or implementation without verification (error amplification = the biggest accident in the two-pillar model).

---

### 6. What Actually Got Done With This Model (Real FullSense Examples)

- **Design cross-review**: had the subordinate review the evolutionary design / requirements / PoC, and the lead verified against actual code to decide on adoption.
- **Existing-asset investigation**: had the subordinate investigate the whereabouts of lldarwin's existing components (loop.py / mating.py / nsga2.py, etc.) → the lead confirmed.
- **Parallel sub-tasks**: parallelized article outlines, code investigation, and requirements organization as independent tasks (this very series is a product of that).

> 🍵 **Break point**: I'll also be honest at the end about my subjective sense of how "1 human + 2 AIs" changed solo-development productivity.
> Honest disclosure of **both** the aspects that got faster (parallelism, redundancy) and the load that increased (verification cost, control cost).

---

### 7. Lessons

- **Keep the chain of command singular.** The two pillars are not peers but lead-and-follow. A split command center is the source of accidents.
- **Verification discipline is the lifeline of the model.** The chain of an AI believing another AI without verification is the greatest risk.
- **The degree of parallelism is rate-limited by the lead's context.** Decide by what you can process, not by headcount.
- **The human / orchestrator holds irreversible operations and git.** Entrust the subordinate only with reversible work.

> **Next time**: take the evolutionary design run with the two pillars (#26 lldarwin) and, using the subordinate Codex + an on-prem ollama,
> push it to Stage 2 (evaluation with a real LLM). How far does multi-layered AI delegation raise "the implementation speed of research"?

---

### 8. Related
- Series #26 "The Design of lldarwin" — a real example run with this model.
- Related memory: [[reference_codex_two_pillar]] / [[feedback_parallel_first_execution]] / [[feedback_agent_no_git_parallel]] / [[feedback_external_ai_verify]]

---

---

## Chapter 8 (Series #32) llcore CPU PoC battery complete

### TL;DR

- **CPU PoC battery complete** for `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, an independent llive track), a research framework that makes the **core computation of a Transformer (state update / learning rule / cognition-driven Δ)** the target of evolution
- Mechanism demonstrated with **5 PoCs / 39 falsifiable gates / 76 tests / Codex pair-review 5/5 green-light**
- **Gating structural mutations online with Z3** = embedding SMT into the selection pressure of evolutionary search — found to be unexplored prior art (prior survey across 14 RAD domains + confirmation by Agents A–D)
- Submission candidates: TMLR (primary) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

### Why we built it

Freezing LLM weights is the norm, but the **core computation algorithm itself stays fixed by hand design**. Architecture/algorithm search such as AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge has advanced, yet:

1. **Infeasible compute for individuals** (TinyLlama 1.1B from scratch = $140k / 90 days / 16×A100)
2. **No safety guarantee during search** = wasting time generating numerically unstable architectures
3. **Verified search is disconnected from static verification (Reluplex/Marabou/α,β-CROWN)** — research on an SMT online gate inside the evolution loop was not found

### Confirmed original axes (no negation work in the prior survey)

Mechanism-proven (4 axes):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **State update rule turned into a gene, RWKV-style** (Stage 0a v2)
3. **factor_hook (cognitive state → SSM Δ)** (Stage 2a mock)
4. **In-house evolver + verifier foundation** (Stage 0c + 1a)

Post phase: persona-indexed specialist / Marabou refinement / proposal of a new VNN-COMP category.

### PoC ladder (5 stages / all 39 gates PASS)

| PoC | Content | Key numbers |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | in-house minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

### What we learned from the v1 failure (honest disclosure)

PoC 0a v1 used `decay*s + mix*x*tanh(gate_str*s)`, which made **state=0 a fixed point — a zero attractor**: it passed G1–G5 formally but transmitted zero information. The design flaw that Claude overlooked on its own was caught by the **independent verdicts of Codex (gpt-5.4) and gem-critic**, leading to a v2 redesign in RWKV-style.

→ **In 4 of the 5 PoCs, Codex pair-review caught design flaws that Claude missed on its own.** A concrete case where mutual review worked to prevent structural breakdown.

### Next options

a. Stage 3 kernel diversification (turn rwkv/mamba/hopfield/linear-attn into genes)  
b. Stage 4 turn learning rules (FF/EP/PCN/Hebb) into genes  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. Speed up the Z3 gate with PrediPrune+Quokka  
e. 3.5–5x wall-clock speedup with FlashEvolve  
f. Write it up as a paper (TMLR + GECCO 2027)

### Honest caveats

- Mostly mock; connecting to real LLMs/weights waits for a GPU/new PC
- The 1-step scalar invariant is at the over-approx proof stage; multi-dimensional and multi-step are in the post phase
- The tanh upper-bound approximation is conservative (sound but not complete)

---

**Tags**: evolutionary computation / formal verification / Z3 / RWKV / state space model / CPU research  
**Related**: Series #14-31 (llive lldarwin v0.B-E + observation + governance + lleval)  
**Project**:  (PyPI llmesh-llcore 0.1.0a0)

---

---

## Chapter 9 (Series #33) An Over-Tidy Result Is Not a Win, It's an Alarm — The Day We Settled Third Axis ③ with Proper Power

### TL;DR

- The question is **"When you search for the core computation of an AI by evolution, is the 'sort-and-separate-and-raise' device (= the ③ survival-of-the-fittest / separation factor of evolution) really needed?"**
- **On synthetic "valley-laced (deceptive) terrain," ③ wins by a landslide** (Cliff δ=+1.0 in past experiments). ③ is genuine as a mechanism.
- **But when we re-measured the more-realistic CPU proxy terrain after physically driving the evaluation noise down to zero, it turned out to be "truly smooth (single-peaked)," and ③ was confirmed unnecessary.** For the first time we backed up the claim "the past negatives were not from underpower; the terrain really was smooth."
- Only the real-multitask neighborhood (C-gen4b) showed a faint hint of "③ NOT null," but when we added data it wobbled and stayed **a candidate at best** (within-run drift + fragile under multiple comparison).
- The suspicion that "some post-processing is hiding ③" (K4 ridge clip) — when removed, things got *worse* instead → **it isn't hiding anything; demoted to a diagnostic observation.**
- The external review (Codex) confirmed the conclusion **with no blockers.**
- The conclusion in one line: **"③ pays off only when the terrain is deceptive. The realistic-ish terrain we could measure on CPU just happened to be smooth."** Settling the main battle requires GPU (real-LLM terrain), but that is an investment decision.
- **Addendum (2026-06-02, §11.5): the last CPU escape route, kernel diversification (BG9), is structurally closed.** Kernel selection is low-dimensional, so a strong baseline (RR) samples it directly, and ③'s niching advantage cannot in principle appear. **For ③ to work, "high-dimensional" deceptive terrain is required**, and the only remaining route is GPU full-LLM (itself a bet).
- Meta-lesson: **honest disclosure is not decoration — it was a tool that pushed the research forward.** In BG9, the same discipline worked in the direction of "confirming a negative correctly as a negative."

> ⚠ Every number in this article is a real measurement tied to a local (on-disk) research commit `THIRD_AXIS_SETTLE_VERDICT.md`. llcore does not yet have a public repository, so I can't link out. Instead I write "how we measured" fully in the body.

---

### 0. What This Article Is About (Concept)

`llcore` is a CPU-complete research framework that "turns the core computations of a Transformer (state-update rule, learning rule, cognitive-drive Δ) into genes and evolves them while verifying with Z3 that they don't break" (I wrote about the PoC battery in Series #32).

Its evolution engine has a design crux: how to make **③ (survival-of-the-fittest selection / separation)** — one of the four elements of evolution — effective. It's a "sort, separate, and raise" mechanism, like MAP-Elites, which keeps diversity and leaves elites in their niches.

The question is simple.

> **Do you really need that ③?**

If you do, the heavy investment to carry ③ (ultimately running a real LLM on GPU) is meaningful. If you don't, clinging to ③ is a waste of time and electricity.

Over this single day (2026-06-02), I went head-on to **settle that question with three experiments.** As the title says, the conclusion drags us back, once more, to FullSense's recurring bassline: "an over-tidy result is an alarm."

— That's 30 seconds. Warm-up done. On to the main subject. —

---

### 1. An Analogy: Mountain Climbing and Deceptive Terrain

Before the equations, let's grasp the big picture with a terrain analogy (a metaphor I've used consistently in this research).

We represent the quality of a design by **the height of the terrain**. **A high place = a good design.** It's a game of finding the highest summit.

**Terrain 1: a smooth single mountain (easy)**

```
 Quality↑
  Hi |            ___________
     |         __/           \__
     |      __/                 \__     ← climb from anywhere
     |   __/                       \__     and reach the same peak
  Lo |__/                             \__
     +----------------------------------→ how you pick the design
```

On terrain like this, naive "hill-climbing" — "just move toward something slightly better than now" — is enough to reach the summit. **You don't need the fancy device (③).**

**Terrain 2: deceptive terrain**

```
Quality↑                                /\
     |                                 /  \   ← the true peak
     |        false pk                /    \
  Md |         /\         vy         /      \
     |        /  \______________/        \
  Lo |____/                                  \
     +----------------------------------------→ how you pick the design
          ↑ naive hill-climbing gets stuck at the false peak (it cannot descend valleys)
```

Here, naive hill-climbing stops at the false peak. It hasn't the courage to descend into the valley.

This is where the ③ idea works. **You leave various types of climbers scattered around the valley** (= memory palace / MAP-Elites archive). Someone can cross the valley by "stepping stones" and reach the real summit — that's the mechanism.

**The heart of this research in one line**: ③ is truly useful **only on "deceptive terrain."** On a smooth single mountain, ③ is a white elephant.

So the question can be rephrased:

> **"When you design an AI by evolution, is the terrain you actually run into 'deceptive terrain,' or a 'smooth single mountain'?"**

Settle this, and whether ③ is needed is settled. Today, this is what we measured.

---

### 2. The Leftover from the Past — Was "③ Unnecessary" Really "Unnecessary"?

Across the past experiments (Step C → Ladder rung 1 → E-A → valley-depth measurement), the picture was roughly this.

- **On the synthetic deceptive corridor, ③ wins by a landslide** (beats all three baselines, Cliff δ=+1.0). ③ is proven to exist, genuine as a mechanism.
- **On the more-realistic proxy terrain, ③ is negative** (MAP-Elites only ties random = the same symptom as a smooth terrain).

But two unresolved snags remained here.

1. **Is "③ unnecessary" really because "the terrain is smooth," or simply because "there weren't enough samples to detect the difference (underpower)"?** ── Mistaking these means committing the over-generalization "③ is powerless."
2. The direct measurement of valley depth ended last time as **N/A (not measurable)**. The evaluation noise was larger than the depth of the valley, so even if a valley existed it was buried out of sight — an instrument limit.

In other words, whether what "looked smooth" was a **property of the terrain** or a **limit of the instrument** had not been settled. Pinning this down is Step D.

— A short break. That was the premise. From here on are the three experiments done today. —

---

### 3. Experiment Design — A Three-Part Set

| Experiment | What it measures | Aim |
|---|---|---|
| **EXP1** | proper-n re-test | Seriously increase sample size and pin down with statistical power whether ③'s effect is real |
| **EXP2** | deterministic C1 multimodality | Physically zero out the evaluation noise and judge noise-free whether the terrain is "deceptive" or a "smooth single mountain" |
| **EXP3** | verdict-flip of K4 ridge clip | Test the suspicion that "some post-processing is hiding ③" |

Discipline: everything isolated in `research/step_d_settle/`, src unmodified, git committed in one batch by the orchestrator. Each experiment passes the break gates (G1 CPU full-run / G2 reproducibility / G3 diagnostic validity / G4 src invariance).

---

### 4. EXP2 Was the Decider — Zero the Evaluation Noise and the Terrain Becomes Visible

The order is shuffled, but **the one that mattered most was EXP2**, so I write it first.

The reason last time's valley-depth measurement came out N/A was simple: **"valley depth (about 0.05·|fitness|) ≪ the jitter of the evaluation noise."** The valley was buried in the instrument's noise, so you couldn't tell whether it existed.

EXP2's trick is this.

> The closed form of an ESN reservoir (fixed seed) + ridge readout (`np.linalg.solve`) **draws no randomness at all.** So the evaluation noise can be physically zeroed down to machine epsilon (about 1.11e-16).

In measurement we confirmed `eval_noise_std ≤ 1.11e-16`. This is not "the value jitters on every evaluation"; it's an error originating from the smallest unit of floating point (ULP), and is **essentially zero.** With the noise fog completely cleared, we can directly measure the valleys of the terrain.

Here is the result (valley_fraction = the fraction of valleys; the larger, the more multimodal = deceptive terrain):

| landscape | type | dim | valley_fraction (mean/max) | multimodal? | verdict |
|---|---|---|---|---|---|
| **ESN_3param** (real proxy) | real | 3 | **0.000 / 0.000** | **False** (3 seeds agree) | smooth=single-peaked → ③ unnecessary, confirmed noise-free |
| **ESN_perneuron40** (real proxy) | real | 40 | **0.096 / 0.121** | **False** (3 seeds agree) | smooth-leaning (below floor 0.2) → ③ unnecessary |
| ctrl_multipeak_dim3 (positive control) | control | 3 | 0.701 / 0.727 | True | the diagnostic can detect multimodality ✓ |
| ctrl_multipeak_dim40 (positive control) | control | 40 | 0.795 / 0.818 | True | diagnostic sound ✓ |
| ctrl_quadratic_dim3 (negative control) | control | 3 | 0.000 | False | the diagnostic can detect smoothness ✓ |
| ctrl_quadratic_dim40 (negative control) | control | 40 | 0.000 | False | diagnostic sound ✓ |

Three points:

1. **The real proxy terrain (both 3-dim and 40-dim) is valley≈0 = single-peaked.** Exactly matched across 3 seeds.
2. **The diagnostic itself is sound.** The deliberately built multimodal positive control is properly detected as multimodal (0.70/0.80), and the quadratic negative control is properly detected as smooth (0.0). So "the real proxy is single-peaked" is not an instrument bug but a property of the terrain.
3. With this, **"the past ③ negatives were not from underpower but because the terrain really was smooth"** was, for the first time, backed up noise-free on a real substrate.

I'll also honestly note a side discovery. **The deceptive corridor (`make_corridor_eval(d=0.16)`) that we intended to use as a positive control turned out to be valley=0.0 (single-peaked verdict) once made deterministic.** The corridor's deceptiveness is the type "confine within a single basin and escape via ③'s behavioral niching" (behavioral-reach deception), and was **not** the deception of terrain valleys (C1 multi-basin). We confirmed in measurement the narrowing of scope: the corridor does not serve as a positive control for C1. This means the past valley-depth calibration cannot transfer the "corridor-derived threshold" to terrain multimodality.

— A breather here. "The positive control didn't act as a control" was quietly a shock. But this too couldn't be known without measuring. —

---

### 5. EXP1 — Only the Real-Multitask Neighborhood Shows a Faint Hint of "③ NOT null"

Next, we re-tested the band closest to the real problem (C-gen4b = MAP-Elites vs random, the real-multitask neighborhood), seriously increasing the sample size.

| case | original n=15 (audit) | fresh true re-run | verdict |
|---|---|---|---|
| **C-gen4b** | diff +0.063 / psd +0.20 / p 0.126 | **n=64: diff +0.0472, one-sided p 0.038, psd +0.188, gate PASS** | **③ load-bearing candidate (still_inconclusive)** |

Running with fresh seeds up to n=64, it **PASSED all four conditions of the strict gate.** That means the audit's reading of "③ unnecessary (inconclusive)" was, directionally, wrong, and **in C-gen4b ③ is in the NOT-null direction.**

…and not getting a winner's high here is the crux of this round. For three reasons, I kept it **a candidate at best.**

1. **Post-update power@n64 = 0.517 < 0.80.** The gate passed, but it doesn't reach the confirmation standard (power 0.80).
2. **Within-run drift (this is what mattered).** Following the trajectory of the cumulative p-value: first PASS at n=40 (p=0.042) → deeply significant at n=60 (p=0.010) → **back near the 0.05 boundary at n=64 (p=0.038).** Furthermore, splitting the seeds into first/second halves: **the first 32 seeds have diff=+0.0755 (frac_pos=0.625), but the second 32 seeds have diff=+0.0189, and the last 9 seeds have diff=−0.0376 (negative).** The PASS is propped up by the first-half seeds, and **the newer the data, the more it runs in the opposite direction.**
3. **Multiple comparison.** p=0.038 PASSES at α=0.05, but even with just EXP1's 3 cases it exceeds Bonferroni α=0.0167 (FAIL). Seen across the whole ③ research family it's harsher still.

In addition, the effect-size floor (psd) was bumping against a **structural ceiling.** C-gen4b's median psd doesn't budge from n=15→0.200 to n=255→0.200. `P(|psd|≥0.147)` (the fulfillment rate of the effect-size condition) plateaus at 0.794 even at n=255. Since it's a medium effect (psd≈0.20), no matter how much you increase the sample, the full gate's power won't exceed 0.80. **In other words, the very prospect that "increasing samples will confirm (A)" is thin on this proxy.**

Conclusion: **C-gen4b is "③ load-bearing candidate / still_inconclusive."** The headline "③ NOT null" leans too hard on a single boundary p=0.038. The within-run drift is real evidence that "the candidate may be a false positive."

---

### 6. EXP3 — The Suspicion That "Post-Processing Is Hiding ③" — Removing It Made Things *Worse*

The last suspicion was this. "Could the post-processing called the ridge-readout clip (K4) actually be crushing ③'s signal?" If so, removing the clip should make ③ surface.

I tried removing it.

| task | clip | MAP-E mean | baselines beaten | verdict_flip |
|---|---|---|---|---|
| **addition** | True | +0.0100 | 1/3 | — |
| **addition** | False | **−1.212** | 0/3 (all worse) | **False** |
| **flip_flop** | True | +0.426 | 0/3 | — |
| **flip_flop** | False | +0.438 | 0/3 | **False** |

When the clip was removed, far from ③ surfacing, **MAP-Elites degraded from +0.010 → −1.212 on addition.** clip=False drops MAP-Elites into the noise region of raw R²<0 (15/15 seeds negative, R² in [−3.68, −0.20]), and instead of recovering structure it made things worse. **= an active refutation of the hypothesis "the clip is hiding the signal."**

The null-ridge FPR (gene-independent target = the true null hypothesis) also has zero difference between clip True/False (both 0.0).

Verdict: **K4 is not "the sole active suppression mechanism" but is demoted to "a diagnostic observation that crushes spread but doesn't change the verdict."** With this, the past statistical audit's assertion "K4 = the sole active suppression" was shown to be overstated.

Honest reservation (equivalent to §6.3): null-FPR=0/0 is a floor value from only null_seeds=4, and this experiment shrank the budget by about 7×. So I unified the verdict label not as "null confirmed" but as **"not_load_bearing_at_this_budget."** "At this budget, K4 is not load-bearing" is more accurate than "the null was confirmed." The substance of the verdict (demotion to a diagnostic observation) is unchanged; I'm only raising word precision.

— A deep breath here. Three experiments done. Next is a self-check of "did I overstate." —

---

### 7. Surviving Refutation — Beating Up My Own Conclusion Through Three Lenses

The core of honest disclosure is "doubt your own conclusion most harshly," so I applied three independent refutation lenses. **All three survived as `refuted=true / medium`** — that is, the conservative verdict isn't overturned, but the positive-leaning emphasis works in the direction of being weakened.

1. **[power_adequacy] C-gen4b's gate PASS is fragile under optional-stopping + multiple comparison.** This is the §5 drift and Bonferroni FAIL above. Making "③ NOT null" a headline leans too hard on a boundary p. → recorded the p-vs-n trajectory and the sign reversal of the second-half seeds in the disclosure fields.
2. **[determinism_and_circularity] The single-peaked verdict is fragile near the threshold.** The determinism and non-circularity themselves are clean (the correlation between behavior and fitness is ≈0; the diagnostic doesn't use behavior descriptors but looks directly at terrain geometry). However, **90.9%** of ESN_3param's midpoints **dip downward**, and the maximum relative dip=0.0435 is just below the C1 valley threshold 0.05 (within 13%). So precisely speaking, it's not "**truly single-peaked**" but "a **weak multi-basin with shallow valleys (~2–4%) slightly below the C1 threshold.**" The direction of (B) null is maintained, but the robustness is limited because of threshold proximity.
3. **[clip_flip_validity] The K4 demotion is "at this budget" only because of the low budget.** verdict_flip=False is certain, but FPR 0/0 is a floor value and the budget is shrunk 7×. So rather than "firm refutation" we should state "not load-bearing at this budget."

None of the three is enough to "flip the conclusion," but all worked in the direction of "trimming overstatement." This self-audit is half of today's output.

---

### 8. One Mistake of My Own, Written Honestly

In the previous valley-depth workflow, I passed **stale (old) values** into the second-stage orchestrator briefing. Values like "all below threshold / d*=0.1234." But the result JSON actually committed had `all_below_threshold=false`. When I read the previous workflow's result, I had mixed up the value of a different metric.

**Adversarial verification detected this and downgraded the verdict to N/A.** That is, the process of doubting my own "over-tidy conclusion" caught my own copy-paste mistake. It's not a pleasant story, but because that ran, in today's Step D I could re-measure from correct footing.

I was reminded that honest disclosure is not just "don't erase failures" but "**place a mechanism that detects failures in advance.**"

---

### 9. How I Updated the Past Verdicts

| past verdict | past reading | Step D's update |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **direction updated: ③ is in the NOT-null direction (gate PASS at fresh n=64).** But a candidate at best |
| step6 exp7 (real ESN proxy, ③ negative) | n≤10 blind zone, "re-measurement required" | **major update: the terrain really is smooth (③ unnecessary), confirmed noise-free.** Re-measuring won't produce multimodality |
| valley depth N/A (not measurable) | instrument incapable | **resolved: made measurable via determinism** → vf≈0 (single-peaked). But a shallow valley near the threshold is a reservation |
| K4 clip = sole active suppression | "the clip conceals landscape structure" | **demoted: diagnostic observation** (not_load_bearing_at_this_budget) |

"Many of the past negatives that looked like '③ unnecessary' were not from underpower but because the terrain really was smooth" ── this one point being verified for the first time on a real substrate is the core of today.

---

### 10. The External Review (Codex) Confirmed with No Blockers

As a discipline of llcore, each capstone passes a pair review by Codex (gpt-5.4, read-only). This time's overall comment was **"No blockers ── ③ conclusion externally confirmed."**

- The judgment to keep C-gen4b a candidate rather than load_bearing is valid (confirmed updated power 0.5174 < 0.80 in the JSON).
- EXP2's determinism and non-circularity are clean. It also confirmed the body's self-admission that "weak multi-basin below the threshold" is more precise than "truly single-peaked."
- EXP3's K4 demotion is valid at the current budget (FPR 0/0 + 7× shrink, so at-this-budget only).

The 4 items pointed out (CF1–CF4) are **all about harness robustness and wording precision for future reruns,** and do not overturn the current conclusion. When we re-test ③ on GPU, we'll apply these and then reuse the harness.

---

### 11. We Were Trying a CPU Escape Route (Kernel Diversification / BG9)

"③'s main battle moves to GPU (the loss landscape of a real LLM)" is EXP2's recommendation. Since the real proxy is confirmed smooth, chasing ③ on smooth terrain won't yield (A) (if the terrain is a single mountain, there's naturally no gain from sorting and separating).

But since GPU is an investment decision, I was running in parallel **another hypothesis we can advance on CPU.** That is **kernel diversification.**

The hypothesis is this. Even if each individual kernel (rwkv / mamba / hopfield / linear_attn) is smooth, **uniting four kernel families could make fitness create a discontinuous step at the moment of kernel switching → the terrain could become multi-basin (deceptive terrain) → ③ could become load-bearing on CPU without GPU.** Verifying this was BG9.

At the time I first wrote this article, it was "right now measuring BG6 (whether the task → best-kernel mapping is non-constant, i.e., 'whether the favored kernel differs by task') in a smoke run." After that (within the same 2026-06-02), BG9 was settled. The next addendum section is its ending.

---

### 11.5. Addendum (2026-06-02): BG9 Settled — The Escape Route Was Structurally Closed

> The conclusion in one line: **BG9 = N/A (structural). That is, the CPU escape route of kernel diversification is closed because "③ failing to stand is structurally determined."** It's not "③ is unnecessary" but "in this space, ③ cannot in principle be separated from the strong baseline" — an informative negative.

The result of the escape route set up in §11 came out. The expected "kernel union creates multi-basin (deceptive terrain) and ③ stands on CPU" **did not happen.** And not "it happened to not stand," but it turned out **it structurally cannot stand.** BG9 confirms this with three tiers of evidence.

#### (1) substrate validity — "discrimination exists but is weak" (PASS but caution)

First, when we re-designed the kernel-favoring task set from first principles and measured "whether the favored kernel differs by task" (BG6), the mapping was **non-constant = non-inert (PASS).** mamba / linear_attn / rwkv each became best on a different task. In the sense that we avoided the rut of "memory_tasks are kernel-neutral" stepped in at BG6, it's progress.

But honestly it is **weak**:

- **hopfield couldn't win on any task.** This is because the hopfield kernel is a **diagonal-scalar mock** and its tanh attractor was dysfunctional (per-seed R² was polarized at 0/0.99/0). So it's effectively not a "4-kernel union" but **3 kernels.**
- Clean specialization is only on 2 axes (selective_copy↔mamba / weighted_accum↔linear_attn). The rest have thin margins and are fragile.

→ **the existence of discrimination ≠ multimodality/barriers.** Non-inert-ification succeeded, but that doesn't guarantee deceptive terrain — only that far. Note that the limit of the diagonal mock is as declared in kernels.py's scope, and here we **claim only the feasibility of the mechanism** (full kernel performance is not claimed).

#### (2) harness validity — the positive control doesn't validate (this is the decider)

Next is the main battle. With fixed parameters (behavior=(kernel_id, theta L1)), we honestly paired-compared MAP-Elites (③) against three baselines ── **RR-hillclimb (random-restart hill-climbing)** / panmictic-GA / random.

| substrate | result |
|---|---|
| **positive control** (synthetic kernel-barrier) | ③ defeats panmictic (+0.423) and random (+0.208). **But it can't beat RR** (+0.051, p=0.31 → FAIL). Falls short of beating all 3 baselines = **harness validity doesn't stand** |
| **negative control** (kernel-neutral tasks) | all methods saturate at R²≈1.0, no ③ advantage = **correctly null** (no false positive, the instrument is sound) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3, panmictic conversely exceeds ③ = **③ doesn't win** |

This is the decisive difference from Step D (technical version §4-7). On Step D's deceptive corridor, ③ could exclude RR. **Why can't it in kernel space?** There's one root cause:

> **RR can directly sample kernel_id ∈ [0,4) on each restart.** Kernel selection is a single coordinate of 4 discretes (low-dimensional), so RR directly hits all 4 kernels on restart. To "find the best kernel," you don't need to cross a valley = **teleport (direct warp).** So ③'s behavioral niching gets no chance to play.

The reason ③ could exclude RR on Step4's corridor was that there the behavior was `mean(24-dim)`, and by the CLT the mean concentrates at 0.5 → the global peak is a measure-zero region = **a high dimension that random/RR cannot sample directly.** kernel_id, conversely, is low-dimensional and can be sampled directly.

#### (3) red-team — even adversarial verification couldn't refute it; rather, it confirmed

We hammered "is the harness's failure to stand really due to structure? could it be a chance setup mistake?" with an independent red-team. The result **failed to refute the structural claim and rather strengthened it**:

- **Mechanism confirmation**: instrumented RR scatters restart kid nearly uniformly across the 4 basins at [12,18,16,18] on the positive control, target reach 88%, best is restart→in-basin climb on 6/8 seeds. **Confirmed numerically** that "RR directly samples kernel_id on restart and bypasses the valley."
- **In all 4 faithful configurations (high-dim theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin), ③ can't beat RR (beats_rr=False).** Loosen the corridor and RR reaches equally; tighten it and ③ **starves first.**
- **Boundary sweep**: the tighter you make the theta corridor dimension D=0→3, the faster ③ starves relative to RR (D=3: ③ reach 0.08 vs RR 0.42). Same across 3 base_seeds.

→ Quantitatively confirmed that **"a behavior dimension where ③ passes by excluding only RR does not structurally exist in kernel space."**

#### Structural insight (the payoff of this settlement)

> **③ (MAP-Elites' behavioral niching) exceeds the strong baseline only when the "hard spot" is in a high-dimensional behavior space and unreachable by direct sampling (random restart).**

- **Kernel selection is low-dimensional (a single coordinate of 4 discretes)** → RR samples directly → ③'s niching advantage cannot in principle appear.
- Even if you move the deception into theta space, RR does greedy climb in-basin after restart, so if you tighten the corridor enough that RR can't pass, ③ also starves to the same degree. **The window of RR fail ∧ ③ succeed does not exist.**

This is the answer to the question left at Step4 §7, "if we expand the search space by kernel diversification, does ③ unlock?" The answer is **NO (structurally, on CPU).** For expansion to unlock ③, the added degree of freedom must produce a behavior that is **high-dimensional and hard to sample directly.** Kernel selection (low-dimensional, discrete) does not meet that condition.

#### Implication for GPU

- **The CPU-exhaustion gate is CLEAR**: BG9 structurally closed the last CPU route (kernel-union). ③'s remaining route is **only the high-dimensional GPU full-LLM loss landscape.**
- The structural insight makes the GPU bet **better-motivated.** ③ only becomes meaningful in high-dimensional behavior. A full-LLM's parameter space is millions of dimensions = exactly high-dimensional. So the GPU test follows a principle — not the weak bet "maybe full-LLM is the only exception," but "③ requires high dimension, and full-LLM is the high-dimensional regime."
- **But it's still a bet**: if the real-LLM terrain can be directly navigated by a strong backprop-family baseline, ③ is unnecessary ── this is a **risk isomorphic to BG9's RR** (the possibility that "a strong baseline solves it directly" remains even on GPU). So GPU is appropriate not "solely for ③" but as a **portfolio judgment** (riding along with llive's real-LLM fitness etc.) + **one pre-registration via a cloud rental** (before capital commitment). BG9's structural insight itself becomes the GPU's falsifiable go/no-go criterion: "if ③ is load-bearing on full-LLM, its hard spot should be in a high-dimensional behavior space and hard to reach by direct sampling/backprop."

#### Honest reservations (important)

- This is **not "③ turned out unnecessary."** "③ cannot in principle be separated from the strong baseline in this low-dimensional kernel space" = N/A (structural), and ③'s mechanism itself was already confirmed genuine at Step4. It's an **informative N/A** that, though N/A, carries the decisive information "the kernel route is closed."
- The harness/red-team are at smoke scale (5-12 seeds). At the proper test 15 seeds the numbers move, but **the structure (tighten and ③ starves first / RR directly samples kernel_id) is seed-independent and robust.** We will not run the full ≥15-seed proper test on real ── since the positive-control validity structurally doesn't stand, even if "③ unnecessary" came out on real, we couldn't separate "③ unnecessary vs detector-blind," and the red-team already confirmed that "detector-blind = the structure of kernel space," so even investing 7.5h of CPU wouldn't change the conclusion.
- The substrate is weak (effectively 3 kernels, **hopfield is a diagonal mock and dysfunctional**). With stronger kernel discrimination (full implementation, off-diagonal) there is **in theory** room for a different conclusion, but ③'s structural barrier (low-dimensional selection → RR direct sampling) is independent of the quality of the kernel implementation.
- The discipline of doubting "an over-tidy ③ success" was **not needed this time** ── ③ success never appeared in the first place (a negative just as the honest prior expected).

---

### 12. Meta-Lesson — Honesty Was a Tool for Winning

Today's real output is not the numbers but **that the spirit of "doubting an over-tidy result" actually pushed the research forward.**

- Because we physically erased the evaluation noise (EXP2), we could separate whether "smooth" was a property of the terrain or a limit of the instrument.
- Because we applied 3 adversarial-verification lenses, we kept "③ NOT null" off the headline and held it as a "candidate."
- Because I self-detected my mix-up of a stale value, I could make the correct downgrade to N/A, and re-measure today.
- **In BG9 (addendum) I learned one more thing**: **a low-dimensional hard spot gets solved directly by the strong baseline. So for ③ (the sort-and-raise device) to work, a "high-dimensional behavior space" is required.** "Make deceptive terrain and ③ stands" is only half right; precisely, ③ won't stand unless the terrain is **deceptive in a way too high-dimensional to sample directly.** With a kernel 4-choice (low-dimensional), RR hits all of them on restart, so ③'s turn never came in principle. This is the basis for declaring the escape route not "given up" but "**structurally closed.**"

"When you get an abnormally good result, always doubt the breakdown before feeling like a winner" ── FullSense's research discipline (`feedback_benchmark_honest_disclosure`) was turning not as mere self-admonition but as **a mechanism that actually catches false positives and raises the precision of the research.** BG9 is an example where the same discipline worked in the reverse direction (**confirming a negative correctly as a negative**) ── trying in the red-team to refute my own "③ doesn't stand," I failed to refute it and it was confirmed as structure.

The conclusion, once more, precisely (reflecting the BG9 settlement):

> **On the proxy substrate, "③ is unnecessary because the terrain is truly smooth" was confirmed noise-free** (Step D). Only in the real-multitask neighborhood (C-gen4b) did a faint sign of "③ NOT null" appear, but with small effect + drift + multiple comparison it stays **a candidate at best.** The K4 clip is demoted from active suppression to a diagnostic observation. And the last CPU escape route, **kernel diversification (BG9), is structurally closed** ── kernel selection is low-dimensional, so a strong baseline (RR) samples it directly, and ③'s niching advantage cannot in principle appear. **The only route left for verifying ③'s main battle is the high-dimensional GPU full-LLM loss landscape** (itself a bet carrying the "strong baseline solves it directly" risk).

"③ settled = ③ turned out unnecessary" is wrong. Correctly, **"③ pays off only on 'high-dimensional' deceptive terrain. Neither the realistic-ish thing we could measure on CPU (smooth) nor kernel diversification (low-dimensional) met that condition."** The main battle (high-dimensional GPU) is still ahead, and it's a bet with no guarantee.

---

**Tags**: evolutionary computation / MAP-Elites / statistical testing / statistical power / honest disclosure / CPU research
**Related**: Series #32 (llcore CPU PoC battery) / #29 (refutation, Goodhart, proxy limits) / #31 (Codex two-pillar)
**Project**: llcore (PyPI reservation llmesh-llcore, local research since the repository is not yet public)

---

---

## Chapter 10 (Series #34) What Six Rounds of Hill-Climbing Taught Us About "When Does Evolution's ③ Actually Matter" — and How Evolutionary Biology Reached the Same Answer 100 Years Ago

### TL;DR

- The question is **"When you search for an AI's core computation by evolution, do you really need the 'sort-and-rear-separately' trick (= evolution's ③: survival of the fittest / separation)?"** Series #33 wrote up the endgame (Step D + BG9); **this #34 surveys the whole arc (6 stages) as a single story**.
- **Stage 1 (synthetic deceptive landscape)**: ③ wins decisively (Cliff δ=+1.0). ③ is a real mechanism = **existence proof**.
- **Stage 2 (memory task / multi-reservoir)**: blocked by the substrate's "floor" and "ceiling," so ③ could not be measured = **N/A**.
- **Stage 3 (multi-task generalization)**: ③ beats "no selection," but cannot beat simple selection or random = ③ unnecessary (honest negative).
- **Stage 4 (measure a real proxy landscape noise-free)**: once we physically drove evaluation noise to zero, the landscape was **genuinely smooth (unimodal)** = ③-unnecessary confirmed. For the first time, "the past negatives were not lack of statistical power but a smooth landscape" was backed up.
- **Stage 5 (BG9: the loophole of mixing 4 component kinds)**: kernel selection is **low-dimensional**, so a strong baseline (random-restart hill-climbing) samples it directly, and ③'s niching advantage **structurally** does not appear = the loophole is closed.
- **Structural insight (the core of this arc)**: ③ only helps when the hard spot lies in a **high-dimensional behavior space** that cannot be sampled directly. The real CPU substrate is low-dimensional/smooth, so ③ is unnecessary.
- **Biological grounding (verified)**: this is exactly Wright's **shifting-balance theory**. For **the melanic moth (single gene = low-dimensional)**, ordinary selection suffices (= the BG9 kernel case); for **Lenski's Cit+ (high-dimensional, history-dependent)**, diversity matters (= the ③ regime). Our negative is **the computational version of the Coyne critique** (real landscapes are simple and ③ is only rarely decisive).
- **Meta-lesson**: "a result that went too well is not a victory but an alarm." Pre-registration, honest disclosure, adversarial verification, and deterministic noise-free measurement kept us from premature celebration.

> ⚠ Every number in this article is an actual measurement tied to local (on-machine) research records. llcore does not yet have a public repository, so I cannot link out. Instead I write "how it was measured" in the body. The papers cited in the biology part are only those whose existence, attribution, and claimed content I separately cross-checked against primary sources.

---

### 0. What this article is about (the concept)

`llcore` is a CPU-complete research framework that "turns a Transformer's core computation (state-update rule, learning rule, cognitive-drive Δ) into a genome and evolves it while verifying with Z3 that it doesn't break."

Its evolution engine has a design crux: of the 4 elements of evolution (① mutation / ② heredity / ③ survival of the fittest / separation / ④ overproduction), how should **③ (selection / separation)** be made to take effect? It is the "sort and rear separately" mechanism — like MAP-Elites, which preserves diversity and keeps things in niches.

The question is simple.

> **Is that ③ really needed?**

If it is, then the heavy investment to carry ③ (ultimately running a real LLM on GPU) is meaningful. If it is not, then clinging to ③ is a waste of time and electricity.

Series #33 wrote up in detail the **endgame** of that question (the deterministic measurement of Step D + the structural resolution of BG9). But to get there, there were **6 stages of experiments**, repeatedly winning (existence proof), failing to measure (N/A), and losing (honest negative). This #34 re-lays out **the whole arc as a single story**. And as the highlight this time, we **ground** — with verified primary sources — the fact that **this computational result has a strikingly identical shape to a roughly 100-year-old debate in evolutionary biology (Wright vs. Fisher)**.

— That was 40 seconds. Warm-up done. On to the main topic. —

---

### 1. Metaphor: hill-climbing, the deceptive landscape, and the memory palace

Before the equations, let's grasp the big picture with the 3 metaphors used consistently throughout this research.

We represent the quality of a design as **the height of a landscape**. **High place = good design**. It's a game of finding the highest peak.

**Landscape 1: a smooth single mountain (easy)**

```
 Quality↑
  Hi |            ___________
     |         __/           \__
     |      __/                 \__     ← climb from anywhere
     |   __/                       \__     and reach the same peak
  Lo |__/                             \__
     +----------------------------------→ how you pick the design
```

In such a landscape, plain "hill-climbing" — that is, "just move toward something slightly better than now" — is enough to reach the top. **The fancy trick (③) is not needed.**

**Landscape 2: the deceptive landscape (deceptive)**

```
Quality↑                                /\
     |                                 /  \   ← the true peak
     |        false pk                /    \
  Md |         /\         vy         /      \
     |        /  \______________/        \
  Lo |____/                                  \
     +----------------------------------------→ how you pick the design
          ↑ naive hill-climbing gets stuck at the false peak (it cannot descend valleys)
```

Here, plain hill-climbing stops at the false peak, because it lacks the courage to descend into the valley.

This is where ③'s idea works. **You keep all sorts of climbers scattered around the valley** (= the memory palace / MAP-Elites archive). Someone can cross the valley by "stepping-stones" and reach the real peak — that's the mechanism.

**The heart of this research in one line**: ③ is truly useful **only in the "deceptive landscape."** On a smooth single mountain, ③ is a white elephant.

So the question can be rephrased like this.

> **"When you design an AI by evolution, is the landscape you actually run into a 'deceptive landscape,' or a 'smooth single mountain'?"**

In #33 we settled this question with Step D + BG9. In this #34 we show **all 6 stages of hill-climbing** that led there. The interesting part is that at each stage, "was it a deceptive landscape / was it smooth / could it even be measured" changes.

— A short break. That's the prep. From here, the full record of the 6-round series. —

---

### 2. The whole-arc map — surveying the 6 stages of hill-climbing at a glance

Let me put out the map first. This is the backbone of this article.

| Stage | Substrate (what landscape was measured) | Did ③ work? | One line |
|---|---|---|---|
| **I (Step 4)** | a synthesized "deceptive landscape" (deceptive corridor) | **Yes (decisive)** | Existence proof. ③ is real |
| **II (Step C / ladder 1)** | memory task / multi-reservoir parity | **N/A** | Couldn't measure due to floor, ceiling, the degree-5 wall |
| **III (E-A)** | multi-task generalization | **No** | ③ beats "no selection," but no more than that |
| **IV (Step D)** | real-proxy text landscape (deterministic measurement) | **No** | The landscape is confirmed **genuinely smooth** (noise-free) |
| **V (BG9)** | union of 4 component (kernel) kinds | **No** | **Structurally** closed (low-dimensional selection) |

The storyline is this. **First we prove existence — "③ is real and wins decisively under the right conditions" (I); next, to ask "well, what about real problems," we went to measure across 4 stages (II–V), and every single time it was "the real CPU substrate is a landscape that doesn't need ③."** Moreover, at the very end (IV, V), it was confirmed that the "reason it's not needed" is **the nature of the landscape, not lack of statistical power** — that is the whole-arc arc.

So, one stage at a time.

---

### 3. Stage I (Step 4) — existence proof: in a deceptive landscape, ③ wins decisively

The first thing we did was an existence proof of "does a scene where ③ **works as the theory says** actually exist?" We **deliberately built a deceptive landscape** and pitted ③ (MAP-Elites) against 3 baselines — pure random / panmictic GA / **random-restart hill-climbing** — in a contest.

**The landscape's construction**: the genome is 24-dimensional. We define behavior (the climber's type) as `mean(genome)` = the average of the 24 values. To raise behavior, you have to **raise all 24 dimensions simultaneously**. The fitness is exactly a deceptive landscape: "a false peak (value 0.6) at behavior≈0.4 → a valley (value≈0) at behavior≈0.65 → the real peak (value 1.0) at behavior≈0.9."

**Results**:

| Method | Reach rate to the real peak | Comparison with ③ |
|---|---|---|
| **MAP-Elites (③)** | **about 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | same as above |
| random-restart hill-climbing | 0% | same as above |

Only ③ reached the real peak; all 3 baselines stopped at the false peak (≈0.60). **100% wins / the effect size is the theoretical maximum (δ=+1.0)**. Robust across 3 base seeds (60 seeds total).

Why this happens becomes foreshadowing for later.

- **random** always has behavior concentrated at ≈0.5 (the average of 24 values is locked at 0.5 by the central limit theorem). So it can **never reach** behavior 0.9 (0% even after drawing 6000 samples).
- **hill-climbing** climbs to the false peak 0.6 and refuses the one move of descending into the valley. Even on restart it returns to behavior≈0.5 and falls into the same trap.
- **③ (MAP-Elites)** keeps the valley cells as "new behavioral niches" and **crosses behavior 0.5 → 0.9 by stepping-stones**.

**We measured the boundary honestly too**. In a smooth corridor with the valley removed, ③ can no longer beat hill-climbing (p≈0.29). **③ is not omnipotent; it only works in a deceptive landscape.**

**Honest caveat**: this is a **deliberately built** synthetic landscape. It only proves that ③ is "possible," not that real tasks have this structure. Toy scale, low noise, and the baseline is a plain (1+1).

→ Here a hypothesis arises: **"If the real-problem landscape is this deceptive, ③ should come alive."** The next 4 stages are a journey to verify that on substrates closer to real problems.

— A pause. Stage I was a satisfying decisive win. From here, the weather turns... —

---

### 4. Stage II (Step C / ladder 1) — blocked by the substrate's "floor" and "ceiling" (N/A)

Next we investigated "does a deceptive corridor **naturally arise in standard memory tasks**?" (Step C). We ran delayed parity / flip-flop / delayed recall with a single leaky reservoir + ridge readout.

The result was a clean **N/A (unmeasurable)**. The reasons are interesting because they're at two extremes.

- **delayed parity = floor**: a single reservoir cannot compute XOR (Minsky-Papert). All methods give R²≈0.003. No one can climb, so ③ cannot be separated.
- **flip_flop = ceiling**: all methods saturate at R²≈0.95. Variance is crushed and ③'s difference doesn't show (③ vs random has a positive sign but p=0.15 = underpowered, so it is **not a null**).

Here is one important finding. **The multimodality of the genome space was high** (valley fraction was 1.000 for parity), yet it was no use to ③. In other words, **"multimodal in genome space" ≠ "a deceptive landscape whose behavior must be crossed."** This distinction becomes the key for the second half of the arc.

**Ladder 1 (multi-reservoir)**: so, if we chain multiple reservoirs, does the floor rise? → We tried 5 mechanisms and all were `floor_lifted = false`. Depth (DeepESN) raises the floor statistically (effect +0.47/+0.60, PASS), but the absolute value stops at R² 0.05-0.10. The clincher is a positive control: a degree-2 readout solves 2-bit XOR exactly (R²=+1.0) but breaks down at degree≥3. **5-bit parity is degree-5 = a structural wall of this CPU reservoir+ridge paradigm.**

→ The parity path is structurally blocked. The real test of ③ needs to **come down off parity**.

**Honest caveat**: the degree-5 wall is "a wall of this setting," not a proof of impossibility for the whole paradigm.

— A short break. A "couldn't measure" result is plain, but in drawing the map it's an important blank zone. —

---

### 5. Stage III (E-A) — multi-task generalization: ③ wasn't needed (honest negative)

Coming down off the parity floor, we measured ③ on **generalization**, with the cleanest ablation we could assemble.

**Setup**: single-layer leaky reservoir + ridge. Recall with variable delay. **Train on short delays {15, 30}, test on long delays {45, 60}** (extrapolation). The comparison is MAP-Elites (full ①②③) vs. **MAP-Elites with selection removed** (`randselect`: choose parents at random and place unconditionally = mutation only) + panmictic GA + random.

**Results (after peer review)**:

| Method | Test generalization R² (mean±std) |
|---|---|
| MAP-E (full ①②③) | 0.682 ± 0.115 |
| MAP-E randselect (selection removed) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| Gate | Comparison | diff | p (one-sided) | Verdict |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**How to read it**: ③ beats the **drift control with selection removed** (C-gen3 PASS = "some selection beats no selection"). But it **cannot beat panmictic GA (which has selection but no niching)** (it even loses slightly), nor random. In other words, **there is no niching-specific (= ③'s intrinsic) contribution**. This generalization landscape was **smooth** enough that simple selection or even random arrives at the same place. This is consistent with Stage I's boundary, "if it's smooth, ③ doesn't work."

**Honest caveat (important)**: this verdict is **limited to this setting** (budget 400, grid 6×6). Furthermore — and here is the crux of honest methodology — peer review (Codex) initially judged it "untrustworthy" and forced 3 rerun blockers (independent seeding per replicate / adopting the global best within budget / raising honest_n from 16→30). **Even after the fixes, the conclusion did not change.** The takeaway is that it was not a "fragile negative that flips when fixed."

— A pause. A loss is a loss, but the work of confirming we "lost correctly" took more time. —

---

### 6. Stage IV (Step D) — the real-proxy landscape is confirmed "genuinely smooth" (noise-free)

This is the turning point of the arc. Through Stage III, "③ negative" kept happening, but a **nagging doubt** lingered the whole time.

> Is "③ unnecessary" really because **the landscape is smooth**? Or was it merely **lack of sample size, so the difference couldn't be detected (underpower)**?

Mistake this and you'd over-generalize to "③ is powerless." Step D settles it here.

**The trick**: an ESN reservoir (fixed seed) + a closed-form ridge readout (`np.linalg.solve`) **draws no random numbers at all**. So we can physically zero out evaluation noise down to **machine epsilon (about 1.11e-16)**. We measured `eval_noise_std ≤ 1.11e-16` — this comes from the smallest unit of floating point (ULP) and is **effectively zero**. With the fog of noise completely cleared, we can measure the landscape's valleys directly.

The landscape is next-character prediction of llcore's own source (about 24k characters). We measured valley_fraction (the fraction of valleys; ≥0.2 means multimodal = deceptive landscape).

| Landscape | Dims | valley_fraction (mean/max) | Multimodal? | Verdict |
|---|---|---|---|---|
| **ESN 3-param** (real proxy) | 3 | **0.000 / 0.000** | No (3 seeds agree) | Smooth → ③-unnecessary confirmed noise-free |
| **ESN per-neuron** (real proxy) | 40 | **0.096 / 0.121** | No (3 seeds agree) | Smooth-ish → ③ unnecessary |
| multimodal control (positive) | 3 / 40 | 0.70 / 0.80 | Yes | The diagnostic can detect multimodality ✓ |
| quadratic control (negative) | 3 / 40 | 0.000 | No | The diagnostic can detect smoothness ✓ |

There are 2 points.

1. **The real-proxy landscape (both 3-dim and 40-dim) is unimodal**. Agreement across 3 seeds.
2. **The diagnostic itself is sound**. A deliberately built multimodal landscape is properly detected as multimodal, and a quadratic is properly detected as smooth. So "the real proxy is unimodal" is not an instrument bug but **the nature of the landscape**.

→ For the first time, **"the past ③ negatives were not underpower; the landscape was genuinely smooth"** was backed up on a real substrate, noise-free. Re-measure and no multimodality appears.

**Honest caveat (important)**: "smooth" is precise only near the threshold. **90.9% of the midpoints of ESN 3-param dip slightly downward**, and the maximum relative dip (0.0435) is just below the valley threshold of 0.05. Strictly, it is not "**truly unimodal**" but a "**weak multi-basin with shallow valleys (~2-4%) just below the threshold**." The direction holds, but the robustness is limited because it's near the threshold — not rounding this off to "a perfect convex bowl" is this time's discipline.

— A deep breath. Here, "the real-thing-mimic is smooth" is confirmed. What remains is "the last CPU loophole." —

---

### 7. Stage V (BG9) — the loophole of mixing components was structurally closed

Since the real proxy is confirmed smooth, chasing ③ in a smooth landscape yields no gain. But GPU is an investment decision, so we tried **a different hypothesis we could advance on CPU**. That is **kernel diversification (BG9)**.

**Hypothesis (pre-registered H7)**: even if each individual kernel (rwkv / mamba / hopfield / linear_attn) is smooth, **when you union the 4 kinds, the moment of kernel switching creates fitness steps → multi-basin (deceptive landscape) → ③ stands up on CPU without GPU**. The pre-registered honest prior leaned **toward null** (since all CPU substrates so far were smooth).

The result in 3 parts.

**(1) substrate validity — there is discrimination but it's weak (PASS but caution)**: when we measure whether the best kernel differs per task, the mapping is non-constant = non-inert (PASS). mamba is best on selective-copy, linear_attn on weighted-accumulation. However, **hopfield could not win on any task** (dysfunctional with the diagonal-scalar mock), so it is effectively a "**3-kernel** union." **The existence of discrimination ≠ a multimodal barrier.**

**(2) harness validity — the positive control does not validate (the clincher)**: on a synthetic kernel-barrier, compare ③ against 3 baselines.

| Substrate | Result |
|---|---|
| **positive control** | ③ crushes panmictic (+0.423) and random (+0.208). **But it cannot beat RR (random-restart hill-climbing)** (+0.051, p=0.31 → FAIL). It falls short of beating all 3 baselines = the harness doesn't stand |
| **negative control** | all methods saturate, no ③ advantage = correctly null (the instrument is sound) |
| **real** smoke | ③ beaten 0/3, panmictic actually exceeds ③ |

In Stage I's corridor, ③ could shut out RR; **why can't it in kernel space?** The root cause is one.

> **RR can sample kernel_id ∈ [0,4) directly at every restart.** Kernel selection is a single coordinate over 4 discrete values (**low-dimensional**), so RR hits all 4 kernels directly on restart. There's no need to cross a valley to "find the best kernel" = **direct warp**. So ③'s behavioral niching has no turn to play.

The reason ③ could shut out RR in Stage I is that there, behavior was `mean(24 dims)`, the average concentrates at 0.5 → the global peak is in a measure-zero region = **high-dimensional, not directly samplable**. kernel_id, conversely, is low-dimensional and can be sampled directly.

**(3) red-team — even adversarial verification couldn't refute it, and rather confirmed it**: on the positive control, instrumented RR spread restart kernels nearly uniformly across the 4 basins as [12,18,16,18], reaching target 88% of the time. In all 4 faithful configurations (high-dimensional theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin), ③ cannot beat RR. Tightening the corridor makes ③ **starve first** (D=3: ③ reach 0.08 vs RR 0.42). We quantitatively confirmed **"the behavior dimension along which RR alone is excluded and ③ gets through does not structurally exist in kernel space."**

**Verdict**: formally N/A (the positive control does not validate), but in substance a **decisive structural negative**. The harness is sound (it correctly nulls the negative control and detects GA/random), yet the substrate **cannot host ③'s deceptive landscape in the first place**. The answer to the question left from Stage I, "if we expand the search space with kernel diversification, does ③ unlock?", is **NO (structurally, on CPU)**.

**Honest caveat (important)**: this is **not "③ turned out to be unnecessary."** It is "③ cannot in principle be separated from a strong baseline in low-dimensional kernel space" = **an informative N/A**. ③'s mechanism itself is already confirmed real in Stage I. The substrate is weak (effectively 3 kernels; hopfield is a diagonal mock). A stronger kernel implementation could in theory yield a different conclusion, but **the structural barrier (low-dimensional selection → RR direct sampling) is independent of the quality of the kernel implementation**.

---

### 8. Structural insight — uniting the 6 stages under a single condition

The existence proof (I) and the 4 negatives (II–V) all connect under just one condition.

> **③ (behavioral niching) exceeds a strong baseline only when the "hard spot" lies in a high-dimensional behavior space and cannot be reached by direct sampling (random restart).**

- **Why Stage I satisfies it**: behavior = `mean(24 dims)`. The average concentrates at 0.5 by the central limit theorem, and the global peak (mean≈0.9) is effectively measure-zero. Neither random nor restart **reaches it directly**. So ③, which leaves stepping-stones and ratchets, is essential.
- **Why the real CPU substrate doesn't satisfy it**: the hard spot is low-dimensional. The control coordinate of the ESN text proxy is effectively leak rate (a smooth low-dimensional knob; there's no valley to begin with). The hard spot of the kernel union is "which kernel" = a single discrete choice among 4. RR samples directly and teleports to all basins, so there's no valley to cross.

So Stage II's "multimodality of genome space 1.000" is not a sufficient condition — even if the genome is riddled with valleys, if the hard spot is concentrated in low-dimensional behavior coordinates, restart reaches it directly. **What matters is "the dimension of the behavior the search must reach," not the dimension of the genome.**

---

### 9. Biological grounding — evolutionary biology gave the same answer 100 years ago

From here is the highlight of #34. **"Diversity-preserving selection works only under narrow conditions and is redundant otherwise"** — this boundary condition has a strangely clean precedent in 20th-century evolutionary biology.

> ⚠ **Honesty contract**: the following biology is a **"metaphor (structural analogy)," not a proof of our computational result**. The correspondence is structural and does not match at the mechanism level. Wherever the analogy slips, I note it on the spot. The papers cited are only those whose existence, attribution, and claimed content I separately cross-checked against primary sources.

#### 9.1 Wright's shifting-balance theory = the precedent of ③

Sewall Wright (1931/1932) reasoned as follows. If you stay as one big "single herd (panmictic population)," ordinary natural selection **gets trapped on the local peak right in front of you**. To go to a higher mountain you must once **lower mean fitness and cross the valley**, but deterministic selection refuses that.

Wright's solution was **to split the herd into many semi-isolated sub-populations (demes)**.

- **Phase I**: a small deme crosses the valley by chance, descending via **genetic drift**.
- **Phase II**: there, ordinary selection within the deme climbs a new (higher) peak.
- **Phase III**: the deme that landed on the high peak sends out many migrants, and the superior gene combination spreads through the whole species.

As a **whole** metapopulation, it crosses a valley that a single converged population cannot — this is the biological version of "crossing the valley of the deceptive landscape by stepping-stones."

**Correspondence to ③ / MAP-Elites (= metaphor, not attribution)**: each cell of the archive = a semi-isolated deme, local elitism within a cell = within-deme selection (Phase II), cross-cell mutation = interdeme diffusion (Phase III), and **the archive as a whole** (≒ metapopulation, not a single cell) crosses the valley.

> **Honesty notes (2 points)**:
> 1. **This is a commentator's framework, neither Wright's claim nor MAP-Elites's origin.** The original MAP-Elites paper (Mouret & Clune 2015) and the QD literature **do not cite Wright or "shifting balance."** I raise Wright as our **inspiration / metaphor**, not as the lineage of MAP-Elites.
> 2. **The mechanisms are only structurally similar, not identical.** MAP-Elites's valley crossing happens because a **mutation operator** places offspring in a new cell, **not genetic drift**. The archive is also not a population of replicating cells.

#### 9.2 Wright vs. Fisher = the dimension (the shape of the landscape) axis

Wright's contemporary Fisher (R. A. Fisher, 1930) argued the opposite: **a large panmictic population + mass selection on additive variance is enough** for adaptation to proceed; there's no need to bother splitting it.

The two's **deepest point of conflict was actually "epistasis (gene-gene interaction) and the shape of the landscape."** Wright assumed "because of non-additive interaction the landscape is **bumpy and multimodal**, so drift to cross valleys is needed," and Fisher judged "interactions exist but are unimportant, the landscape is roughly **unimodal and smoothly climbable**, so mass selection suffices."

**This epistasis/ruggedness axis is exactly the dimension in which our result lives. The shape of the landscape (topology) is the whole problem.** If the landscape is genuinely bumpy and high-dimensional (the Wright regime), diversity ferries you across valleys; if it's smooth or the hard spot is low-dimensional (the Fisher regime), mass selection — i.e., the biological version of strong random-restart hill-climbing — already suffices. Our ESN text proxy is noise-free and smooth, and the hard spot of the kernel union is low-dimensional discrete. **Both are the Fisher regime**, and ③ doesn't work and didn't work.

> Fine print (honestly): "Fisher ignored drift" is a compressed popular myth. Precisely, "he acknowledged drift exists but judged it quantitatively negligible in large populations." It's not a total denial.

#### 9.3 Our negative = the computational version of the Coyne critique

The most telling correspondence is not Wright's **proposal** but the biology community's **empirical verdict**. Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) evaluated shifting-balance theory both theoretically and empirically, and concluded as follows (full text cross-checked).

- **Mass selection is usually enough.** "There are almost no real examples better explained by Wright's three-phase mechanism than by simple mass selection." Artificial-selection experiments also failed to show that "selection in subdivided populations produces a greater response than mass selection in a large population."
- **Shifting balance works only under limited, rare conditions.** Empirical estimates of population structure suggest "**drift can move populations only between peaks separated by shallow valleys**" (deep valleys are only rarely crossed by drift), and moreover **most adaptation does not require valley crossing**.

This is a **strikingly precise biological version** of our result. Translated into our vocabulary, their words become: **if the landscape isn't genuinely deceptive/high-dimensional, ordinary mass selection (≒ strong random-restart hill-climbing) already solves it, and the diversity-maintaining apparatus buys almost nothing.** "Real valleys are usually shallow, most adaptation needs no valley crossing" is the biological statement of our "**real landscapes are usually simple, so niching is redundant**."

> **Honesty notes (3 points)**:
> 1. **They did not "refute" shifting balance.** They explicitly state Phase I/II can happen and cite 6 empirical cases. The claim is **narrower and probabilistic** ("hard to call it a general, important mechanism"), and writing "refuted" overstates it.
> 2. **The debate is not yet settled.** Wade & Goodnight (1998) and Peck et al. (1998, whose title literally argues "feasible") rebutted it, followed by Coyne et al.'s 2000 counter-rebuttal and Goodnight & Wade's rebuttal in the same issue. You must not cite the 1997 critique as the "final conclusion."
> 3. **Biology has a mechanism with no counterpart on the computational side, and it makes a claim even stronger than ours.** In Phase III, the gene-flow barrier that protects diversity can **trap a good solution in peripheral demes and impede its spread** = niching can be **counterproductive**. Our stateless discrete-selection setting has no counterpart to this cost, so we **don't overlay** it here. This is a spot where biology makes a stronger claim.

#### 9.4 Two real examples — the low-dimensional moth and the high-dimensional E. coli

Our claim has two poles (low-dimensional = ③ unnecessary / high-dimensional = ③ can work), and evolutionary biology has a clean real example for each.

**The low-dimensional pole — industrial melanism of the peppered moth (= the BG9 kernel case)**: in *Biston betularia*, carbonaria (black) vs. typica (white) are governed by **a single Mendelian locus, few alleles** (the causal variant is a transposable-element insertion into the cortex gene; van't Hof et al. 2011/2016) under **strong directional selection** (s ≈ 0.1-0.2; Saccheri et al. 2008; predation reconfirmed in Cook, Grant, Saccheri & Mallet 2012). The optimum is unimodal at each moment, merely shifting with the environment. **Simple directional selection — the biological version of greedy hill-climbing / random restart — directly fixes the fitter morph, and a diversity-maintenance mechanism is neither needed nor invoked.** This is exactly BG9: kernel selection is a low-dimensional single coordinate of 4 choices, RR samples all kernels directly, and ③ cannot structurally separate. **The melanic morph = the living-organism version of the BG9 kernel case.**

> Note (honestly): polymorphism is temporarily maintained during the transition, but that is due to **spatial environmental heterogeneity + gene flow (migration-selection balance)**, not an intrinsic diversity-preservation mechanism. A spot where the analogy slips slightly.

**The high-dimensional, history-dependent pole — Lenski's Cit+ (= the ③ regime)**: in the E. coli Long-Term Evolution Experiment (LTEE), aerobic citrate utilization (Cit+) evolved in **exactly 1 of 12 populations** around generation 31,500 (Blount, Borland & Lenski 2008). The key is a high-dimensional, history-dependent path of ordered **potentiation (accumulation of precursor mutations) → actualization (promoter capture via tandem duplication of citT) → refinement** (Blount et al. 2012). Replay experiments distinguished "historical contingency" from "a constant rate of rare mutation." This **genuinely exemplifies** the value of exploring contingency, epistasis, and a high-dimensional bumpy landscape — a real example of a regime where ③ can work.

> **Honesty notes (this corresponds only to the "antecedent" of our conditional)**:
> - **LTEE uses no niching algorithm.** It's plain natural selection, and the 12 parallel populations are **themselves a random-restart-like design**. So it's an existence proof that "contingency + diversity enables a rare innovation," **not** evidence that "niching beats a strong restart baseline."
> - "E. coli acquired the power to eat citrate from scratch" is a popular exaggeration. The innovation is **regulatory (aerobic expression of an existing transporter) = exaptation**, neither a new gene nor new biochemistry.
> - Van Hofwegen et al. (2016) showed "with direct selection Cit+ appears much faster" and challenged the "rare/contingent" framing (the Lenski side rebutted that it doesn't contradict the potentiation under LTEE conditions). If you lean on the "extremely rare / long-delay" narrative, you should also note this **contested follow-up**.

#### 9.5 Grounding summary

| Pole | Biology | Landscape | Does ③ work? | Our substrate |
|---|---|---|---|---|
| low-dim/smooth | melanic morph (single locus, s≈0.1-0.2, directional) | unimodal, shifting | **No** — mass selection suffices | BG9 kernel union; ESN/ridge text proxy (deterministic, smooth) |
| high-dim/contingent | Lenski Cit+ (potentiation→actualization→refinement) | bumpy, valley crossing by mutation | **Yes** (a regime where it can work) | synthetic deceptive corridor (behavior = average of 24 dims) |
| empirical verdict | Coyne, Barton & Turelli: mass selection usually suffices, shifting balance is only rarely decisive | real landscapes are usually simple | the **mirror** of our negative | every CPU substrate we tried |

**Conclusion**: Wright's shifting balance is the correct biological precedent for "**why** ③ works when it works," the Wright-Fisher epistasis/ruggedness axis is the correct framework for the "**dimension** condition," the melanic moth and Lenski Cit+ are clean low-/high-dimensional poles, and the Coyne critique is the biological precedent of our **negative**. **But these do not prove the computational result. They only ground it.** Where the analogy loosens most is that biology adds a cost (the gene-flow trap of Phase III) — our stateless setting has none.

— A pause. When I realized a 100-year-old debate had the same shape, honestly I got chills. But not mistaking "got chills" for "proof" is this time's discipline. —

---

### 10. Implications for GPU — the only path left is high-dimensional, yet still a bet

The arc closed every CPU path. The real proxy is noise-free and smooth (IV), and the last candidate (kernel diversification) is structurally closed (V). The only path left for ③ is **a high-dimensional landscape** — and what provides that is **the parameter/loss space of a full LLM (millions of dimensions)**.

The structural insight makes the GPU bet **better-motivated**. It's not the blind bet "maybe only full-LLM is the exception," but a bet that follows the principle "**③ requires high dimensions, and full-LLM is the high-dimensional regime**."

**But still a bet.** For the same reason that biology's Cit+ does not prove "a victory of the ③ algorithm," and by the same form as not beating RR in BG9 — **if the real LLM landscape can be navigated directly by a strong baseline of backprop (gradient descent), ③ is again unnecessary**. The hard spot being high-dimensional is **a necessary, not a sufficient, condition**. You additionally need to show "a strong direct method cannot solve it" (RR on CPU, gradient descent on GPU).

So GPU is appropriate **not "for ③ alone"** but as a **portfolio judgment** (riding along with llive's real-LLM fitness, etc.) + **one pre-registration on rented cloud** (before capital commitment). The go/no-go criterion can also be written falsifiably:

> **Is the full-LLM hard spot high-dimensional in behavior, AND hard to reach by a strong direct baseline (gradient descent)?** If high-dimensional but the gradient reaches directly, ③ is unnecessary (= the GPU version of BG9's RR result).

---

### 11. Meta-lesson — honesty was a tool for winning

The real achievement of this arc is not the numbers but **that the spirit of "doubting results that came out too neatly" actually pushed the research forward**.

- When we won at the **existence proof (I)**, we voluntarily confirmed "③ is not omnipotent" with a boundary experiment that removed the valley (not overrating the win).
- At **generalization (III)**, peer review thrust 3 rerun blockers at us, but even after fixing, the conclusion didn't change (confirmed it was not a fragile negative).
- At the **deterministic measurement (IV)**, because we physically erased evaluation noise, we could separate whether "smooth" was the nature of the landscape or the limit of the instrument.
- At **BG9 (V)**, in adversarial verification we **tried to refute and couldn't refute** our own "③ doesn't stand," and it was confirmed as structural (the same discipline worked in the direction of confirming a negative as correctly negative).

And across the whole arc we learned one thing — **a low-dimensional hard spot gets solved directly by a strong baseline. So for ③ (the sort-and-rear trick) to work, a "high-dimensional behavior space" is required.** "Build a deceptive landscape and ③ stands up" is only half right; precisely, ③ doesn't stand unless it's a deceptive landscape **so high-dimensional it can't be directly sampled**. And surprisingly, this boundary condition was one that **Wright's shifting balance and the Coyne critique had reached nearly 100 years ago**.

"When an abnormally good result comes out, always doubt the breakdown before you feel like you've won" — FullSense's research discipline (`honest disclosure`) was not mere self-admonition but a **mechanism that actually catches false positives, confirms negatives correctly, and raises the precision of the research**, turning across all 6 stages.

Let me state the conclusion precisely one more time, at the end.

> **③ comes alive only in a "high-dimensional" deceptive landscape.** It won decisively in the existence proof (synthetic corridor), but the real CPU substrate — the memory task (floor/ceiling), the multi-task generalization (smooth), the real-proxy text landscape (noise-free and smooth), the kernel diversification (low-dimensional, structurally closed) — none satisfied that condition. It is **not "③ resolved = ③ turned out unnecessary"** but "the real-thing-mimics we could measure on CPU now did not satisfy the condition (a high-dimensional deceptive landscape) under which ③ comes alive." The main keep (GPU high dimensions) is still ahead, and it's a bet that carries the risk that "a strong direct baseline solves it." And the skeleton of this conclusion had already been drawn by 20th-century evolutionary biology — except that biology does **not prove it, only grounds it**.

---

**Tags**: evolutionary computation / MAP-Elites / statistical testing / honest disclosure / evolutionary biology / CPU research
**Related**: Series #33 (third axis ③ resolution Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (refutation, Goodhart, proxy limits)
**Project**: llcore (PyPI reservation llmesh-llcore; local research as the repository is not yet public)

---


<!-- REFERRAL -->

---

> ### ⚡ This series is written hand-in-hand with Claude Code
>
> The implementation, verification, and visualization in this article are all done together with **Claude Code** (Anthropic's AI coding environment).
> Claude Code can be tried with a **1-week free trial**. If you like it and sign up for a paid plan,
> registering via the referral link below gives the author "credits to keep developing," helping this series continue.
>
> 👉 **Try it for free / Referral link** → https://claude.ai/referral/0sqPw8E_lw
>
> <sub>EN: This series is built together with **Claude Code** — try it with a **1-week free trial**. If you subscribe via the link, the author receives credits to keep building. /
> 中文: 本系列与 **Claude Code** 协作完成,可享 **1 周免费试用**;通过链接注册可让作者获得继续开发的额度。 /
> 한국어: 이 시리즈는 **Claude Code**와 함께 작성합니다 — **1주 무료 체험** 제공. 링크로 가입하면 저자가 개발 지속용 크레딧을 받습니다.</sub>

<!-- /REFERRAL -->

<!-- CTAIMG -->

![Morita holding out a 10,000-yen bill, saying "That's a bit much"](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/012.jpg)
> 🗒️ *"That's a bit much" — the scheme of trying to earn pocket change off a referral link; even I find it a little off-putting*（© Forbidden shibukawa / SHUEISHA, "Snack Basue"）

<!-- /CTAIMG -->
