---
title: llcore Verification Arc — Collected (#38–#42): Defensive Disclosure × the 2ⁿ Wall × Strong Gradient Beats Evolution × the Langton's-Ant Illusion
tags: FullSense, llcore, Singularity, AI, 解説
private: false
public_id: 525cd01eda5c1ad707ef
---

# llcore Verification Arc — Collected (#38–#42): Defensive Disclosure × the 2ⁿ Wall × Strong Gradient Beats Evolution × the Langton's-Ant Illusion

<!-- TOPICNAV -->
> **🌐 Language**: [日本語](https://qiita.com/furuse-kazufumi/items/cc0713ab78a5b390df76) | **English** | [中文](https://qiita.com/furuse-kazufumi/items/29b100b00f0d58306886) | [한국어](https://qiita.com/furuse-kazufumi/items/a5ebb3992e4c28862f47)
>
> **📚 FullSense Digest Series**
> - **llcore Verification Arc（this）**
> - [lldarwin / Evolution Arc](https://qiita.com/furuse-kazufumi/items/e49b7ab9027d93594402)
> - [llive Complete Guide](https://qiita.com/furuse-kazufumi/items/07b686ea311e06027f94)
> - [llmesh Digest](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762)
> - [Plain-Language Digest](https://qiita.com/furuse-kazufumi/items/bdfad6db3f2e70c40511)
<!-- /TOPICNAV -->

## Contents

1. [a day that ran from "adversarial verification → patent clearance → declining to file → defensive publication"](#chapter-1-a-day-that-ran-from-adversarial-verification--patent-clearance--declining-to-file--defensive-publication)
2. ["the window closed in implementation, but the wall did not budge"](#chapter-2-the-window-closed-in-implementation-but-the-wall-did-not-budge)
3. ["the moment I thought I'd won, my own framework stopped me"](#chapter-3-the-moment-i-thought-id-won-my-own-framework-stopped-me)
4. [binding three installments onto one point: "simple deterministic rules create apparent order"](#chapter-4-binding-three-installments-onto-one-point-simple-deterministic-rules-create-apparent-order)
5. [Chapter 5](#chapter-5-chapter-5)


---

## Chapter 1 a day that ran from "adversarial verification → patent clearance → declining to file → defensive publication"

On June 6, 2026, I (the author) asked an AI (Claude Code) **"to verify whether what we are doing is truly differentiated."** The AI answered with **adversarial verification** — running many verifier AIs that deliberately try to refute and disprove our own claims, to see whether they still survive. Fifty-six verifier agents searched from 7 + 3 angles for counterexamples along the lines of "this claim should be refutable with prior work," and a separate detachment even queried patent databases.

The results were as follows.

- **Refutations (breaks) in academic literature: 0** (we judged 44 candidates individually, and no one had filled "all four corners at once").
- **Refutations in patents: 0** (across 14 English + 3 Japanese queries, no patent occupies the intersection).
- So I decided **not to file a patent** (a cost judgment), and instead planted a flag called **defensive publication**.

This article is a breakdown of the story of that one day (the design and results of the adversarial verification, and the decision-making) plus **what we published (= the technology at the four-point intersection)**. As always, the order is ① term explanations → ② breakdown (plain language) → ③ details.

---

### ① Mini-glossary (so you don't get stuck in the body text)

| Term | In a word |
|---|---|
| **Adversarial verification** | A method that, rather than affirming your own claim, runs many verifier (AI) agents that deliberately try to refute and disprove it, and measures the claim's strength by whether it still survives. Picture hiring critics instead of yes-men. |
| **Defensive publication** | Rather than "obtaining" a patent, **disclosing a technology to turn it into prior art**. A defense that "plants a flag first" so that someone (including a big player) cannot later patent the same invention and bind us or the public. |
| **Prior art** | An existing public document that lets you say "that invention is already public knowledge." Material that negates novelty. The date is everything. |
| **Contraction (ρ<1)** | The property that echoes (past perturbations) **decay** over time. The spectral radius ρ is below 1. Picture a spring that always returns to a resting position. The property by which the memory core "forgets" rather than running away. |
| **Sound proof** | A proof such that when it says "proven," it is **actually correct** (it never issues a false pass). A different thing from a statistical "probably safe." |
| **prove-then-reject gate** | A checkpoint that **adopts a mutation (update) only after proving it**, and **rejects** it if it fails. fail-closed (if it can't be proven, it doesn't pass). |
| **Memory core** | A "remembering part" placed around the LLM. In this research it is a leaky, saturating recurrence (RWKV-family) `s_{t+1} = decay⊙s + (1−decay)⊙tanh(W s + V x)`. |
| **Evolution loop** | An optimization that cycles mutation → selection → next generation to search for good individuals. Here, a proof gate is placed at the checkpoint of that selection. |
| **SMT solver (Z3 etc.)** | A general-purpose solver that decides whether a logical formula is satisfiable. Heavy. In this research the conclusion is that it "turned out to be unnecessary (decorative)." |
| **tracking tube** | A guarantee that the actual deviation from a "desired trajectory" stays within a **tube (radius r)**. `r = G·w̄/(1−L)`. |
| **SSGM** | Prior work that proposed a write gate "to govern evolving memory" **in theory only** ([arXiv:2603.11768](https://arxiv.org/abs/2603.11768), 2026). The closest rival in terms of the banner. |
| **navigability** | Whether evolution is "easy terrain to move through." Distinct from learning getting smarter. This is where the verifier's effect lies. |

![Four-point intersection — only the center where all 4 conditions overlap simultaneously is the differentiation core](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_intersection.svg)

---

### ② Breakdown — the whole picture in 3 minutes

Let's start from the idea of a biological niche. In evolution, "a species that moves into a niche — a gap no other species has occupied yet" survives. The AI world is similar. The big players (OpenAI/Google, etc.) are "large species that are smart on average," occupying the wide plains. We cannot win on those plains. So we look for **a gap no one has filled** and build a part that fits it. The thing that fit that gap precisely, this time, is a concrete system called `llcore`.

In one sentence, `llcore` is **"a system in which an AI part that holds memory imposes a 'checkpoint of proof' on itself, so that it does not run away."** The memory core mutates (evolves) every time it updates, but before any mutation is adopted, it must pass through a checkpoint (gate). The checkpoint admits **only what can be mathematically proven** to keep the memory from running away, and turns away anything that cannot be proven (fail-closed).

This system fits that "gap" precisely because the following 4 conditions **overlap at a single point**.

1. A **sound contraction proof** (a mathematical guarantee that echoes necessarily decay — and it never issues a false pass).
2. Applying it **inside the LLM's memory core** (not a control robot, not a classifier, but the "remembering part" itself).
3. **Inside an evolution loop**, **rejecting** bad mutations (discarding them, not pushing them back = not projection).
4. And there is **a working implementation and experiments** (it doesn't end as armchair theory).

No prior work satisfying all 4 of these **simultaneously** was found, even when we had 56 verifier AIs critically scrutinize it and queried patent DBs. Each individual condition has predecessors (we name them all honestly). But no one had "occupied all four corners at once." This is the **four-point intersection**. In terms of the biological niche, `llcore` sits in **the single-point gap** where the four boundary lines exactly cross (in Sun Tzu's terms, "avoid the solid and strike the void").

And the important decision. This gap was **also empty in patents**. Normally one would then say "OK, let's get a patent." But patents cost money and time. I **passed on that**, and instead chose **"publish and plant the flag first" defensive publication**. The aim is not offense but **defense** — to **preempt** anyone (a big player, or a successor implementation of SSGM) later patenting the same concept and binding us or the public. Once you publish with a date, it becomes public prior art, and a later patent dies on novelty.

That said — and this is our consistent discipline — **we do not inflate**. We do not say "world first." The correct phrasing is **"within the scope of our adversarial verification, there is zero prior work occupying all four corners simultaneously."** We always leave the caveat that we cannot know about what is outside the search scope.

---

### ③ Details — the day's session, and the substance of the technology we published

#### 3.1 Design of the adversarial verification (so it can be reproduced)

Saying "my research is strong" yourself means nothing. So the AI built an **refutation-driven workflow**.

- **Refutation search from 7 angles**: lineage of proof gates / certified training / Transformer stability / evolution × verification / verified memory / runtime assurance / industry and patents.
- **Added 3 blind-spot angles the critic pointed out**: reverse lookup from the formal-methods conference side / the vocabulary system of certified continual learning / interpretation of internal state and SSMs.
- **Judged 44 candidates individually with a 5-axis rubric** (does it gate updates / is the proof sound / is it an LLM memory core / inside an evolution loop / is there an implementation). The adjudicating AI **always checked the primary source (the arXiv abstract/HTML) via WebFetch** (hearsay forbidden).
- In parallel, **an internal AI extracted the weaknesses of our own paper draft** (honest disclosure: nitpicking our own side).

The firm conclusion is **breaks 0 / narrows 36 / background 8 (44 items)**. The differentiation core that survived is the four-point intersection above.

#### 3.2 The closest rival for each "corner" (we name them all)

Novelty's honesty is decided by "whether you can name all of them in one sentence." For each corner, the closest predecessor in one sentence:

- **SSGM ([arXiv:2603.11768](https://arxiv.org/abs/2603.11768))** — preempted the banner "governing evolving memory" **in theory only**. The gate is NLI (contradiction detection), **not a sound formal proof**, and there is no implementation. → **Must be cited** as the party carrying the banner. The window of implementation + proof is open.
- **SEVerA ([arXiv:2603.25111](https://arxiv.org/abs/2603.25111))** — Dafny/SMT verification for self-evolving agents. But the target is **output contracts**, not a per-update gate on the contraction of the memory core.
- **PSV-Verus ([arXiv:2512.18160](https://arxiv.org/abs/2512.18160))** — a sound SMT gate inside a self-play loop. But the verification target is **the correctness of generated code**.
- **Provably Safe Model Updates / LID ([arXiv:2512.01899](https://arxiv.org/abs/2512.01899))** — certifies updates as δ-safe via abstract interpretation. But it is **projection (pushing back)** rather than prove-then-reject, and the target is the classification head of a frozen embedding.
- **GP × model checking (Katz & Peled, [arXiv:1402.6785](https://arxiv.org/abs/1402.6785), 2014)** — a **precedent for the pattern** of placing a sound checking gate in an evolution loop. That is why we **do not claim the gate pattern itself as novel**. Only its application to the contraction of a memory core is unexplored.
- **Enforced-Lipschitz Transformers ([arXiv:2507.13338](https://arxiv.org/abs/2507.13338)) / R2DN ([arXiv:2504.01250](https://arxiv.org/abs/2504.01250))** — enforce contraction **by construction**. This is the strongest counter-design: "you don't need a gate, build it in from the start." We contrast **by-construction vs. prove-then-reject** as a design axis (structural enforcement sacrifices expressiveness; a rejection gate inspects arbitrary updates without structural constraints).
- **Safeguarded AI (ARIA programme)** — the most authoritative proof-gated-gatekeeper concept. But the gate target is **behavior/plans** (an output gate), not a gate on weight/memory updates, and it is still at the programme stage.
- **Emergent FV / substrate-guard ([arXiv:2603.21149](https://arxiv.org/abs/2603.21149))** — a working system that verifies an AI's **outputs** with Z3. But it is post-hoc monitoring, not a per-update gate.

(All arXiv IDs above use only those whose abstracts have been cross-checked in the paper draft.)

#### 3.3 Patent-side inquiry (filling the hole the academic audit left)

The academic audit used **literature only** and did not look at patent DBs (weak as evidence of absence). So a separate detachment queried Google Patents / USPTO with **14 English + 3 Japanese** queries.

- **Patents occupying the intersection: zero.**
- The closest patents are just 3 lineages, all outside the intersection:
  - **[US11715005B2](https://patents.google.com/patent/US11715005B2)** — authenticity verification of NNs by hash matching (cryptographic hash, not a sound proof).
  - **[US10896032](https://patents.google.com/patent/US10896032)** — a certify-then-deploy governance gate (grounded in procedural attestation).
  - **[US11868855](https://patents.google.com/patent/US11868855)** — "stability" verification of models/weights (but very likely in the availability / fault-tolerance sense).
- An interesting structural piece of evidence: when you query "**gate updates/memory/evolution with a sound proof**," even with a site restriction on the patent DB, almost all results **veered off to arXiv**. This is indirect evidence that "this concept still remains at the academic stage and has not been patented."

→ Conclusion: **clear on the patent side too**. However, since US10896032 / US11868855 partially overlap in vocabulary, we proactively put 1–2 sentences of contrast into the paper's related work: "unlike deployment-governance gates / operational-stability verification, this research gates the analytic contraction property of weight updates with a sound proof."

#### 3.4 The substance of the published technology (the body of the defensive disclosure)

A defensive publication is weak as prior art unless written at "a level of detail that a person skilled in the art can implement." So the disclosure document wrote the following at **an implementable level**.

![Memory core equation — an illustration of the leaky, saturating recurrence s(t+1) = decay⊙s + (1−decay)⊙tanh(W s + V x)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_core.svg?v=2)

**(a) The ladder of sound contraction verifiers.** Three rungs, cheapest first:
- `cert_inf` — closed-form ∞-norm upper bound (`O(n²)`). Uses the property that the sum of absolute values per row is maximized at the endpoints, so it is **solver-free**.
- `cert_two` — SVD at all `2^n` vertices.
- `cert_sdp` — a common Lyapunov matrix via a convex LMI (interior-point SDP, CLARABEL).

![Verifier ladder — the three rungs cert_inf → cert_two → cert_sdp, a staircase of proof strength tried cheapest-first](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_ladder.svg)

**Here is the honest point**: the project's old nickname was "Z3-gated," but **the actual gate does not use SMT (Z3)**. When we ran a dedicated Z3 contraction track to check, it **matched the closed-form ∞-norm verifier byte-for-byte (0 mismatches out of 3270; even near the boundary, 0 out of 8000)**. In other words, for this invariant class, **Z3 was decoration**. So we corrected the banner to "the ladder of sound contraction verifiers" (this is not a retreat but a strength — it avoids solver dependence and incompleteness).

**(b) prove-then-reject gate (fail-closed).** Propose a child individual → adopt if the proof passes, resample up to a cap if it fails, and if it still fails, adopt a **known-safe fallback**. **An unproven child is never adopted.** We added `gate_mode="contraction"` / `"state_norm"` additively, and the default `"none"` is byte-identical to prior behavior (= a pure overlay on the existing evolution base).

![prove-then-reject gate — a fail-closed checkpoint that proposes a child, adopts it if the proof passes, and rejects then resamples if it fails](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_gate.svg)

**(c) tracking tube inspection metric.** An answer to the user's request to see not just "shrinks to somewhere" but "**tracks a desired trajectory**." Reusing the quantities the gate already computes (state Lipschitz `L`, input gain `G`) and the disturbance upper bound `w̄`, it reports the tube `r = G·w̄/(1−L)` in which the tracking error stays — at **zero additional proof cost**. Even in small-scale measurement, the 3 genes that PASS contraction have error/disturbance ratios 0.50/0.78/1.04, inside the theoretical tube, while a non-contraction control **amplifies by 9.3×** (= the gate is load-bearing, not decoration).

![tracking tube — a tube of radius r = G·w̄/(1−L) drawn around the desired trajectory, with the actual trajectory staying inside it](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_38/qiita_38_fig_tube.svg)

**(d) Two routes for verified memory evolution.**
- Route (a): gate updates of the agent's **memory bank** with a sound proof (the difference from SSGM's NLI theory = sound proof + a working gate).
- Route (b): gate the memory core's **internal-state dynamics** (done in this document).

**(e) Synthesis: an SPC control-chart runtime gate + a two-layer ethics gate.** Pass evolution metrics through control charts (X̄–R / CUSUM) to gate temporal anomalies online. And a two-layer ethics of **exploration is free, adoption is verified** (the exploration layer follows Sun Tzu's "way of deception" = surprise moves OK; the adoption layer follows the Analects' "benevolence" = honest, with the gate unavoidable).

#### 3.5 Today's implementation facts (reduced to practice)

Evidence that this is not armchair theory:

- The proof gate is **fully wired into the shipping-side `evolve()`** (`gate_mode` / `resample_cap` added additively, the default `"none"` is byte-identical, and tests demonstrate all modes match the research-side reference implementation).
- The tracking tube reporter has landed too (`r = G·w̄/(1−L)`, limited to `cert_inf`, read-only, golden values match).
- **294 tests** cover the gate + reporter.
- **The observed gate cost is roughly 20–60×** (we disclose, without hiding, that proof is not free).

#### 3.6 Honest limits (we don't soften them)

Even with defensive disclosure we do not bend honest disclosure.

- **The scale is small**: the core is `n=8` (72 real-valued genes), a 16 KB corpus, byte vocab. "LLM memory core" is in the sense of a **mechanism demonstration**.
- **The verifier's payoff is navigability, not learning (L3)**: the effect is EA-specific and vanishes with gradient methods.
- **The gate is a ~20–60× cost**: it only looks free under short training.
- **"Zero false admits" is an empirical observation, not a machine check**: the verifier's *conditions* are sound, but the *implementation* carrying them is not end-to-end formally verified.
- **The scope of "not found"**: limited to the scope of the adversarial verification + a surface-level patent search. CNIPA (Chinese) was not queried, and patents have a publication lag of up to 18 months. We always maintain the "within the search scope" caveat.

---

### Summary — the flag was planted for "defense," not "offense"

In a single day, we had 56 verifier AIs critically scrutinize our own research, queried patent DBs, and confirmed the "four-corner gap" that still remained. Normally one would aim for a patent here, but weighing the cost, we **passed on filing** and instead planted a flag with **a dated defensive publication**.

The aim is simple — **to preempt anyone later enclosing this gap with a patent and binding us or the public**. To that end, we published everything at a level of detail a person skilled in the art can implement. And to the end, we keep the non-inflating phrasing: **not "world first," but "within the scope of our verification, zero prior work occupying all four corners at once."**

The body of the defensive publication (the dated disclosure) has been upgraded, as the addendum below describes, to **a public repository containing the implementation and all data**: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore).

Next time (from #39 on), we plan to report the landing of the heart of this four-point intersection — a small PoC of verified memory evolution (the memory-bank update route). Before the window where SSGM took the banner in theory closes in implementation.

### Addendum (2026-06-07) — the flag became an implementation

The day after this article, the promised verified-memory-evolution PoC **was completed, and the defensive publication was upgraded from "a document" to "the real thing."**

- **Public repository**: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) — the paper draft ([PAPER_DRAFT.md](https://github.com/furuse-kazufumi/llcore/blob/main/research/paper/PAPER_DRAFT.md)) plus all experiment code/data (570 files, 318 tests green), published as a single dated commit
- **The trajectory-tube gate** (the promised centerpiece): a pre-registered n=40 decision confirmed the effect on the memory horizon (paper §9)
- **And beyond**: "what happens when the AI holds the verifier itself" — measurements of three memory-formation mechanisms (endogenous foresight / certificate-preserving revival / observational learning) in a lethal environment are also included (paper §9.6)
- **Findings slides (CC BY 4.0)**: [slides/](https://github.com/furuse-kazufumi/llcore/tree/main/slides) — a 10-slide summary (ja/en), usable in corporate settings with attribution. **The current version is a digest with modest information density — we will keep expanding it over the coming year (experiment-design details, full figures, reproduction steps, adoption-decision material) as the research progresses**

The promise — "before the SSGM window closes in implementation" — was kept this way.

---

---

## Chapter 2 "the window closed in implementation, but the wall did not budge"

At the end of #38, we promised: "Next time we will report the heart of the four-point intersection — a small PoC of verified memory evolution. Before the window where SSGM took the banner in theory closes in implementation."

On June 9, 2026, that PoC ran to completion. In one sentence: **"The window closed in implementation. But the wall (the scalability wall) did not budge an inch."**

Concretely:

- We ran a **memory core that evolves with proofs** (including real structural surgery `width_grow`) with **zero observed false-admits** (i.e., it evolved without issuing a single false pass).
- At the same time, we measured for the first time the **cert_sdp (SDP verifier)** that we had honestly left "unmeasured" until now, and found it to be the **most "navigable" sound verifier** (it passes 90–99% of genuinely contracting individuals).
- **Nevertheless, even cert_sdp's cost remains `2^n` (exponential in dimension n).** That is, **a verifier that is "both navigable and cheap at scale" was, once again, not found.** For now, verified structural evolution is limited to **small components (n≤6).**

This article writes, without inflating, both what we "could" and "could not" do that day, in the usual order ① terms → ② breakdown → ③ details. At the end we also disclose the result of having **6 verifier AIs adversarially refute our own numbers in parallel** (zero MAJOR discrepancies).

Source of truth: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) (paper draft + all experiment code/data).

---

### ① Mini-glossary (so you don't get stuck in the body)

| Term | In a word |
|---|---|
| **Plasticity** | The property of being able to "change shape" through learning/evolution. Here, growing the memory core's own structure (matrix size = dimension) after the fact. |
| **Verified-plasticity** | Each time you "change shape," **proving the change is safe (won't run away) before adopting it.** The main axis of this research. |
| **width_grow** | **Structural surgery** that grows a network layer from `n → n+1` (Net2Net family). Actually executed, not on paper. |
| **Contraction (ρ<1)** | The property that past perturbations **decay** over time. Spectral radius ρ below 1. The property by which memory "forgets" rather than running away. |
| **false-admit** | A miss where a verifier passes something actually dangerous (ρ≥1 = can run away) as "safe." Zero of these is the lifeline of soundness. |
| **Sound** | The property that when it says "pass," it is **actually safe** (never a false pass). Different from a statistical "probably safe." |
| **navigability** | "How many genuinely safe individuals it can pass." An overly strict verifier rejects even safe individuals = evolution can't move. The higher, the more freely evolution moves over the terrain. |
| **cert ladder** | Three rungs, cheapest first: `cert_inf` (∞-norm bound, solver-free) → `cert_two` (SVD at all `2^n` vertices) → `cert_sdp` (convex LMI/SDP). |
| **prove-then-reject gate** | A checkpoint that **adopts a mutation only after proving it**, and **rejects** it if it fails. fail-closed (no proof, no pass). |
| **SSGM** | Prior work proposing a write gate "to govern evolving memory" **in theory only** ([arXiv:2603.11768](https://arxiv.org/abs/2603.11768)). The party for whom the window of implementation + sound proof was open. |
| **empirical_rho** | An oracle that approximates the true spectral radius **from below** with many samples. "Zero observed false-admits" is the result of this from-below audit (= strong consistency evidence, but not an absolute proof). |
| **2^n wall** | The limit where proof cost grows exponentially `2^n` in dimension n. `cert_two`/`cert_sdp` look at all vertices, so they hit this wall. |

![Four-point intersection and the 2^n wall — with navigability on the vertical axis and dimension n on the horizontal, cert_sdp raised the ceiling but did not break the wall (2^n)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_39/qiita_39_fig_wall.svg)
> 🗒️ *Note: labels in this figure are in Japanese. (The 2ⁿ wall = the cost of the proof blows up exponentially as the block size grows.)*

---

### ② Breakdown — the whole picture in 3 minutes

The flag planted in #38 was a **"memory core that evolves with proofs."** The memory core mutates (evolves) each update, but before any mutation is adopted it must pass a checkpoint (gate) that admits **only what can be mathematically proven** not to run away; otherwise it is turned away (fail-closed). This is the prove-then-reject gate.

This time we moved that flag **from "a document" to "a working thing."** Three things we "could" do.

**Could ①: Zero false passes, even while growing the shape.** Until now we had only tried "proving mutations (small internal tweaks)." This time we actually ran **structural surgery that grows the shape (`width_grow`, n→n+1)** and confirmed the verifier keeps "safe (ρ<1)" with **zero observed false-admits** even after growing. The divergent region (dangerous individuals reaching ρ 1.85–2.21) was all correctly rejected.

**Could ②: We measured the most "navigable" verifier for the first time.** We filled the hole we had honestly left as "cert_sdp unmeasured." In an environment with an SDP solver (CLARABEL), we measured it for the first time and found **cert_sdp the most "navigable" of the three** — it passes 90–99% of genuinely contracting individuals (the cheap `cert_inf` passes only 20–40%, the middle `cert_two` 40–50%). The "too strict, evolution can't move" problem was substantially relaxed by SDP.

**Could ③: For small components, the computation trivially fits.** For a small core of n≤6, the entire verified-evolution loop eats only **0.04% of a 30-hour budget (0.013 hours).** The worry "isn't proof-gated evolution too heavy to run?" was, at small scale, unfounded.

…So far it sounds like "we won everything." But honest disclosure is our discipline. Here are three things we **could not** win, stated plainly.

**Could not ①: The 2^n wall is not broken.** cert_sdp did raise the "navigability ceiling." But at the cost of a still-`2^n` price (looking at all vertices). `cert_two` is 1.3 s per proof at n=12, out of budget at n=14. **A verifier that is "both navigable and cheap at scale" did not exist this time either.** So verified structural evolution is, for now, limited to **small components (n≤6)** — this conclusion is **unchanged** from last time (Phase −1). SDP did not **cross** the wall; it merely **raised** the ceiling in front of it.

**Could not ②: "Zero false passes" is an empirical observation, not a machine proof.** Zero observed false-admits is the result of searching for refutations with an oracle that approximates the true ρ **from below** (many samples). The verifier's *conditions* are mathematically sound, but the *implementation* carrying them is not end-to-end formally verified. "Zero observed" is strong consistency evidence, not an absolute proof of "safe for all inputs" — we don't exaggerate here.

**Could not ③: The model did not get smarter.** The verifier's payoff is **navigability (how freely evolution moves)**, not the model getting smarter (learning performance going up). And the effect is specific to evolutionary algorithms (EA); it vanishes with gradient methods. Furthermore, this round's fitness is a **synthetic proxy**, and confirmation under real GPU training is deferred to the next phase (Phase 2).

In short, this was a half-won, half-homework day: **"the mechanism was proven in implementation; the scale wall remains, honestly."**

---

### ③ Details — five experiments and the caveats we couldn't kill

The main axis is the **Verified-Plasticity Evaluation Framework.** Before claiming "our method is strong," first build **the ruler to measure with.** With that ruler we ran five experiments (all `$0` / CPU, torch 2.12+cpu, fixed seed, reproducible).

#### 3.1 Verifier soundness and ladder under fixed structure

Sampling hundreds of individuals each at n={4,6,8} spanning contraction–divergence, we cross-checked the three verifiers' passes against true ρ (empirical_rho, 6000 samples).

| n | contracting (ρ<1) | false-admit (inf/two/sdp) | pass rate of genuinely contracting (inf/two/**sdp**) |
|---|---|---|---|
| 4 | 453/600 | **0 / 0 / 0** | 0.41 / 0.51 / **0.95** |
| 6 | 426/600 | **0 / 0 / 0** | 0.29 / 0.43 / **0.94** |
| 8 | 280/400 | **0 / 0 / 0** | 0.23 / 0.40 / **0.91** |

Findings:
1. **All three verifiers have zero observed false-admits** (cert_sdp's soundness confirmed for the first time). Consistent with the verifiers' mathematical soundness.
2. **cert_sdp is overwhelmingly navigable** — of genuinely contracting individuals, the cheap cert_inf passes only 23–41%, cert_two 40–51%, but **cert_sdp passes 91–95%**. Note that `two⊆sdp` (if cert_two passes, cert_sdp passes) is a **structural guarantee (tautology)** from an implementation fast-path, not an empirical finding — we state this so as not to inflate.

#### 3.2 Soundness × non-triviality under real structural surgery (width_grow)

We actually grew the base n→n+1 with `width_grow` (Net2Net/fresh) and judged whether each gate **keeps zero false-admits under growth ∧ opens ≥1 non-trivial pass** (1 cell = 1536 grown individuals).

- **Soundness under growth: zero observed false-admits across all 16 (cell × gate).** Growth ρ up to 1.85–2.21 (divergent region) all correctly rejected. This is the confirmation of **North Star #1 (zero false passes under growth operations)** under real structural surgery.
- **The cheap gate (cert_inf) is sound but fragile at small n** — at the most conservative edge of n=6 (headroom 0), non-trivial passes are **0** → gate FAIL. Even with headroom, non-trivial passes are merely 3, right at the τ margin. = "the cheap gate's navigability is fragile."
- **The navigable gates (cert_two/cert_sdp) PASS all cells** — cert_two opens 114–168, cert_sdp 673–733 non-trivial sound passes. → **"Promote per-component gates to cert_two/sdp, limited to small-n" is justified by data.**

#### 3.3 The blind spot of inter-block coupling

Coupling two blocks residually, we measured with true ρ the **blind spot where "each block passes alone but the composite runs away."**

- **per-block AND (AND-ing each block's individual pass) is genuinely unsound under coupling** — at coupling strength γ≥1.0, **24–34% (γ=1.0) to 80–96% (γ=2.0) of individually-passed cases have composite true ρ≥1** (run away). → **per-block AND is forbidden.**
- **full-system cert (proving the whole system at once) has zero false-admits across all γ = sound.**
- Here too **cert_sdp is the most navigable**, but raising the dimension (block count 2→3) and coupling strength lowers coverage (at full=6, γ=1.0, cert_inf/cert_two are 0%, only cert_sdp 75.8%). = SDP resolves over-conservatism, but **the dimension wall still bites even with SDP.**
- ⚠ Honest caveat: at block count 3 the SDP solver issued a few "solution may be inaccurate" warnings. **Soundness (false-admit=0) is guaranteed by an independent eigenvalue recheck**, but the coverage numbers may include slight wobble from the approximate solution.

#### 3.4 feasibility (does it really run within budget)

We extrapolated measured per-op wall-time to a 30-hour budget.

| n | per eval | total | fits in 30h |
|---|---|---|---|
| 4 | 769μs | **0.011h** | yes |
| 6 | 912μs | **0.013h** | yes |
| 8 | 9.2ms | 0.131h | yes |
| 10 | 38.6ms | 0.550h | yes |
| 12 | 1.31s | **18.6h** | barely |
| 14 | — | (cert_two 2^14 extrapolation = infeasible) | no |

Findings:
1. **small-n (n≤6) is trivially feasible** — 0.04% of the budget.
2. **The 2^n wall binds at n≥10–12** — cert_two is 1.3 s/proof at n=12 (=18.6h, thin margin), out of budget at n=14.
3. ⚠ Caveat: this fitness is a **synthetic adapter proxy** of `RotationNDObjective`; under real GPU training the base forward (CE) becomes dominant. This extrapolation is a "conservative upper bound charging one proof per eval"; real GPU measurement is to be confirmed in Phase 2.

#### 3.5 Portability to a second base (Mamba)

We checked whether the framework rides on bases other than SmolLM2. **Mamba-130M loaded successfully on CPU** (coherent generation confirmed), and on its hidden state the cert_two gate is load-bearing (pass rate moves +0.287 with/without the gate, consistent with SmolLM2's +0.320). = Demonstration of the "swap in a new base" plug-point.
- ⚠ Caveat: the soundness oracle here is not the empirical_rho of §3.1-3.4 but a **weak oracle (single perturbation)**, with a small group of n=7 passes. Mamba's own intrinsic stability (base-level Lyapunov) is unmeasured, deferred to Phase 2. This phase's deliverable is limited to "framework portability + Mamba CPU operation check" (not an intrinsic-stability positive control).

#### 3.6 Integrated verdict — Decision gate 1 = PASS (small-n)

| gate | condition | verdict |
|---|---|---|
| Soundness under growth ∧ non-trivial admit≥1 | false-admit=0 over N width_grow ∧ non-trivial pass≥1 | **PASS** (cheap gate trivial at n=6 → cert_two/sdp required) |
| coupling-aware composite soundness | per-block AND forbidden + full cert sound | **PASS** |
| feasibility | small-n loop within 30h budget | **PASS** (small-n) |

→ **Decision gate 1 = PASS → on to Phase 2 (small-n per-component regime, within the constraint fixed in Phase −1).** Phase 1's deliverable is **"a measurement harness for sound, feasible small-n verified structural adaptation + a full characterization of the verifier ladder (inf/two/sdp)."**

#### 3.7 Honest limits (not yet killed)

Even with defensive disclosure we do not bend honest disclosure. Onto #38's caveats, we overlay what this round's measurement killed / left.

- **The 2^n scalability wall is unchanged (the biggest homework)**: cert_sdp raised the navigability ceiling to ~0.9 (a big improvement from Phase −1's cert_two ~0.45), but the **2^n vertex cost is unchanged.** "A navigable-and-scalable sound verifier remains absent" = the non-viability of high-dimensional verified structural evolution is **upheld.** SDP only raised the ceiling; it did not break the wall.
- **empirical_rho is a from-below estimate**: zero observed false-admits is strong consistency, not an absolute proof of "ρ<1 for all (s,x)." It can miss near-boundary cases.
- **net2net is an incoming-copy approximation** (not exact function-preserving) → the function change Δfunc is an approximate measure.
- **fitness is a synthetic proxy**: a capability side-line (EXISTS/NULL/ARTIFACT) on real SmolLM2 CE is required in Phase 2.
- **Mamba's intrinsic stability is unmeasured**: the gate applies to the adapter; the Mamba base's own Lyapunov is unverified → deferred to Phase 2.

---

### Adversarial verification — having 6 AIs refute our own numbers in parallel

The core of honest disclosure is "when an abnormally good result appears, doubt the breakdown before feeling like you've won" ([feedback_benchmark_honest_disclosure]). So we had **6 independent verifier AIs in parallel** cross-check this verdict's numerical claims against each experiment's `results.json` + implementation `.py`.

**Result = zero MAJOR issues (no discrepancy that overturns the conclusion); all MINOR.** The findings are reflected in the body:
- Fixed 4 transcription rounding errors (maxΔfunc 0.108→0.107, etc.).
- §3.1's `two⊆sdp` stated as an implementation tautology, not an empirical finding.
- Refined "the cheap gate is trivial at n=6" to "trivial only at n=6's most conservative edge, fragile even with headroom."
- "cert_sdp 98% rescue" stated as limited to block count 2; at 3 it is 75.8% / inf·two 0%.
- Made transparent that fitness is a synthetic proxy, the conservatism of the extrapolation, and the CPU→GPU extrapolation premise.

→ **After verification, Decision gate 1 = PASS, the SDP navigability finding, and the small-n-limited conclusion are unchanged.** The findings all improve honest-disclosure precision; none shake the mechanistic conclusion.

---

### Summary — "the window closed, the wall remained"

The flag planted in #38 advanced this time **from a document to a working thing.** We ran a memory core that evolves with proofs, while actually growing its structure, with **zero observed false-admits**, filled in the previously-unmeasured SDP verifier, and confirmed small-n feasibility. The window of "implementation + sound proof" for the banner SSGM took in theory thus closed on the implementation side.

On the other hand, the biggest homework, the **2^n wall**, did not budge this time either. A verifier "both navigable and cheap at scale" still does not exist. So we do not inflate: we uphold last time's conclusion that verified structural evolution is, **for now, limited to small components of n≤6.**

Next time (from #40 on) is Phase 2 — applying the calibrated "multimodality instrument" to a real loss terrain and confirming, with proper power, one thing about how evolution moves over the terrain (the capability side-line). The ruler is built. Next, it's time to measure real terrain with that ruler.

Source of truth: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) — paper draft + all experiment code/data (5 experiments + adversarial-verification workflow).

---

---

## Chapter 3 "the moment I thought I'd won, my own framework stopped me"

In the last installment (#39) we concluded: "We built a memory core that evolves *with a proof* — but only for small parts, n≤6. The scalability wall didn't budge."

This time (2026-06-10) we finally answered the question we'd been putting off:

> **"So does this 'evolving memory' actually get *smart*? Is it better than gradient descent (ordinary learning)?"**

One-line answer: **"On a real terrain made by an actual small LLM, evolution beat ordinary gradient descent 20 games to 0. For a moment I thought I'd won. Then, following my own framework's discipline, I called in a *strong* gradient — and the victory turned out to be an illusion."**

This is a record of the scariest moment in research — **the moment an abnormally good result appears** — and how I doubted myself before celebrating. Same order as always: ① terms → ② plain words → ③ details. No embellishment. At the end I disclose the result of having **verifier AIs adversarially refute** my numerical claims in parallel (zero MAJOR discrepancies).

Source data: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) (all experiment code/data + verdicts).

---

### ① Mini-glossary

| Term | In one line |
|---|---|
| **capability** | "Does it get smart?" Here, how well it predicts what comes next (low cross-entropy / CE). |
| **guarantee** | "Does it avoid blowing up?" Provably stable (contraction ρ<1). **The lifeline of honest-disclosure is never confusing these two.** |
| **MAP-Elites (evolution)** | Evolutionary search that keeps a grid of diverse solutions. The "evolution" side. |
| **finite-diff gradient (weak)** | Naively *estimates* the slope by nudging values. Costs dim+1 evals per step = **slow and weak**. |
| **analytic (exact) gradient (strong)** | Gets the *exact* slope in one pass via autodiff (backprop). What real LLM training actually uses. The decider here. |
| **meta-gate** | When evolution "wins," bring in a **stronger opponent** and check whether the gain survives. If it vanishes, it was an illusion (ARTIFACT). |
| **ARTIFACT** | A fake win caused by the **opponent being weak**, not a real performance gap. |
| **Langton's ant** | A famous system, simple rules, that looks chaotic then suddenly orders. A metaphor for "appearance ≠ essence." |

---

### ② Plain words — "winning 20 straight against a weak opponent says nothing"

A baseball analogy. Your team (evolution) beats an opponent (finite-diff gradient) **20 games to 0**. Strong, no complaints.

…but what if that opponent was a *sandlot* team? 20 straight wins is no proof *you* are strong — maybe the *opponent was weak*.

Do this in research and you get a disaster. You write "evolution beat gradient!" in a paper, and later someone says "no, the gradient method you compared against was just too weak." This is the **capability trap**.

So our framework had a **rule (meta-gate)** baked in from the start:

> **If evolution wins, call in the "pro" for a rematch before you celebrate.**

We called the pro (analytic gradient = the exact gradient real LLM training uses). Result:

- vs sandlot (finite-diff): evolution **20–0** (+0.029 mean CE lead)
- vs pro (analytic gradient): evolution **1–19** (the pro wins)

So **evolution won only because the opponent was weak**. With a strong gradient, gradient was better. **"Evolution gets smarter (capability)" cannot be claimed.**

The key point: **losing here is not a failure.** Our framework's value was never on the "smart" side (capability) — it's on the **"doesn't blow up" side (guarantee)**. This result means that choice was **right, in data** — good thing we didn't sell on smarts.

---

### ③ Details — what we measured on a real LLM terrain, and how

#### 3-1. From "synthetic" to "real" terrain

Earlier capability experiments measured on a **synthetic multi-peaked terrain** (an artificial landscape). We honestly flagged: "this is not a real LLM loss terrain."

This time we closed that gap with the **real SmolLM2-135M** (an Apache-2.0 small LLM):

1. Run text through SmolLM2, extract the **real internal representations (hidden states)** at layer 15.
2. Project to small dimension (n=6) and build a **CE terrain that predicts "the cluster of the next internal representation"** — not synthetic Gaussians, but a **real prediction task derived from the model's own internal dynamics**.
3. On that terrain, run evolution (MAP-Elites) / random / weak gradient / **strong analytic gradient** at the **same budget** (eval count), comparing prediction on **held-out (unseen) sentences** across 20 seeds.

#### 3-2. Results (held-out mean fitness = −CE, higher is better)

| Method | held-out mean | Note |
|---|---|---|
| **strong analytic gradient (torch Adam)** | **−1.446** | **best of all** |
| evolution (MAP-Elites) | −1.454 | 2nd |
| random | −1.473 | |
| weak gradient (more restarts) | −1.481 | |
| weak gradient (finite-diff) | −1.483 | **last** |
| evolution + ρ<1 gate | −1.483 | gating constrains search to finite-diff level |

- evolution vs **weak gradient**: +0.029 mean, **20–0**, p<1e-6 → 4-condition AND **passes** (looks like EXISTS).
- evolution vs **strong analytic gradient**: −0.008 mean, **1–19**, gradient wins at p=3.5e-4 → 4-condition AND **fails**.

**→ Verdict = ARTIFACT+NEGATIVE.** Evolution's win was due to a weak opponent. With a strong gradient, gradient ≥ evolution = **capability is NEGATIVE even on a real LLM terrain**.

#### 3-3. We also checked it holds on both terrains (cross-check)

"Then wasn't the earlier synthetic 'tie (NULL_TIE)' also understated by the weak gradient?" — we checked that **in data** too. Adding the strong analytic gradient to the synthetic terrain, **the analytic gradient had the best mean** (0.575 > evolution 0.535). But the synthetic terrain has high run-to-run variance, so the paired test stayed a tie. The real terrain, with lower variance, let the gradient advantage reach **significance** (19/20).

**Conclusion: capability NEGATIVE is consistent across both terrains** (strong gradient best on both). The only difference is variance.

#### 3-4. The "does the framework see the real thing" side PASSES

Capability can't be sold. So what stands up — the **guarantee (discriminative power)**. Three confirmations in the same session:

- **Discrimination**: an experience-based gate **misses 84%** of "dangerous structures" (passes diverging ones as "safe"). A **sound certificate misses 0%**. In particular cert_sdp has zero false-admits and only 4.6% over-rejection = **sound and most navigable**.
- **Base-level discrimination**: Mamba (a structurally stable SSM) is intrinsically stable across all 24 layers → trivially passes. The standard Transformer SmolLM2 has no state recurrence → **safety must be imposed by a bolted-on gate**. The framework cleanly separates "safe base" from "needs-a-gate base."
- **Extensibility (framework-ness)**: the three plug-points (substrate / objective / certifier) swap with a **single object** (17 unit tests green). But the hypothesis "diversity helps generalization" is **NULL** (doesn't hold) — also disclosed honestly.

#### 3-5. Shown "in motion" — the norm doesn't explode, only the sensitivity does

A side finding. This substrate keeps the state bounded via tanh, so **even when unstable, the output norm does not diverge**. Worse, even a diverging individual (ρ≈2.9) has its perturbation **appear to decay** on one trajectory (exactly Langton's ant — appearance betrays essence). Watching the state norm, or a finite-horizon "forgetting test," **cannot catch ρ≥1**. Only the **certificate's worst-case (box-sup) evaluation** can. The demo captures this "experience is fooled, only the certificate sees" in one figure (`phase2_demo_gate_discrimination.svg`).

---

### Honest disclosure — what I doubted at the scariest moment

The most dangerous moment was **seeing "evolution 20–0."** An SNS-friendly headline flashed by ("Found a real LLM terrain where evolution beats gradient!").

What stopped me wasn't a new insight — it was the **rule baked in from the start (meta-gate)**: "if you win, call the strong opponent." I called, and lost. So I can't write it.

This is not a report of losing — it's a report of **the framework working**. Without the meta-gate, I would have published a falsehood. "Abnormally good results: doubt the breakdown before celebrating" — that discipline actually stopped one false positive, in data.

Remaining honest caveats:
- A hidden-cluster CE proxy, not a full-vocab softmax CE (full-vocab degenerates at small n).
- Gating costs −0.028 performance on the real terrain (it measurably trims plasticity). But since evolution has no capability edge, this doesn't change the conclusion.
- "Strong gradient is best" assumes backprop gives exact gradients for free — which is exactly what real LLM training does, so it's a realistic comparison.

### Verification — I had AIs refute my own claims (MAJOR 0)

Finally, I had **independent verifier AIs adversarially refute** the numerical claims of all three experiments in parallel. For the main result (capability), a verifier AI **loaded SmolLM2 itself and re-ran 3 seeds independently**, deterministically reproducing "strong gradient beats evolution." **Zero MAJOR discrepancies.** All findings improved reproducibility / wording / caveat precision, none overturned a conclusion (one verifier found a non-reproducible RNG defect, which I made deterministic and re-ran on the spot).

---

### Wrap-up — what "evolvable LLM" really is

Across three installments (#38→#39→#40) we landed here:

- **#38**: Defensive disclosure — the window for "proof-carrying memory" opened in theory.
- **#39**: The window closed in implementation. But the **scalability wall** didn't budge (verified evolution only up to n≤6).
- **#40 (this one)**: Does it get smart? → **NO.** Even on a real LLM terrain, a strong gradient beats evolution. **Capability can't be sold.**

So "evolvable LLM" really means: **not "an AI where evolution wins on performance," but "a framework that provably guarantees and measures that online structural adaptation doesn't blow up or catastrophically forget."** It's unglamorous. But having decided to **compete on safety, not inflated smarts**, this is the honest picture.

Next time we plan to summarize this framework under the metaphor "an eye that sees through Langton's-ant illusions." Experience is fooled by appearances; only the certificate sees the essence — and on that single point, three installments of honest disclosure all converge.

---

<a id="中文"></a>

---

## Chapter 4 binding three installments onto one point: "simple deterministic rules create apparent order"

This is the **capstone** of the llcore verification arc (#38 → #39 → #40). At the end of #40 we promised: "Next time we plan to summarize this framework under the metaphor 'an eye that sees through Langton's-ant illusions.' Experience is fooled by appearances; only the certificate sees the essence — and on that single point, three installments of honest disclosure all converge."

We keep that promise. One line first:

> **"AI that gets smarter the more you use it / self-evolves" and "world models will hand you safety" are pleasant headlines. But unless you can falsifiably tell, with a sound certificate, whether "got smarter / got stable" is real or an illusion, it is only an *appearance*. verified-plasticity is exactly that discriminator. Its value lies in GUARANTEE, not capability.**

The concept hook is **Langton's ant**. An ant driven by just a few deterministic rules walks chaotically for a while, then suddenly builds a regular trajectory called the "highway." **Simple rules create apparent order and apparent complexity.** This is the core metaphor: what we kept hitting across #38-#40 is exactly that **empirical observation is fooled by the "appearance" that simple things create**.

- A structure that *should* diverge **looks stable** when observed (#40's Langton's ant).
- Evolution **looks like it beats gradient 20–0** when observed (#40's Langton's ant ver.2).

Both are "appearances," and the essence beneath (true instability, a genuinely weak opponent) was **invisible to experience and seen only by a sound certificate**. On that single point, the three converge.

As always: ① terms → ② plain words → ③ details. No inflation. Only verified numbers; unverified is marked "unverified." We **never confuse** capability (evolution beats gradient) with guarantee (proof-carrying stability) — the lifeline of honest disclosure.

Source: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore).

---

### ① Mini-glossary

| Term | In one line |
|---|---|
| **verified-plasticity** | A framework that takes "does it not diverge / does it contract (keep ρ<1 *soundly*)" as the first-class metric for online structural adaptation of small bolted-on blocks (n≤16 verified recurrent adapters) on a real small LLM, and measures any method falsifiably. The main axis. |
| **capability** | "Does it get smart?" Predictive quality of what comes next (low cross-entropy CE). |
| **guarantee** | "Does it avoid blowing up?" Keeping stability (contraction ρ<1) with a sound certificate. **Not confusing these two is the lifeline of honest disclosure.** |
| **contraction (ρ<1)** | The property that past perturbations are **forgotten (decay)** over time. Spectral radius below 1. The pass condition of the echo-state property. |
| **echo-state property** | State is determined by input history; initial perturbations are forgotten. "Holds (ρ<1)" = safe, "fails (ρ≥1)" = can blow up. |
| **false-admit** | A miss where the gate passes something actually dangerous (ρ≥1) as "safe." Zero of these is the soundness lifeline. |
| **sound** | When it says "pass," it is **actually safe** (never a false pass). Different from a statistical "probably safe." |
| **navigability** | "How many genuinely safe individuals it passes." An overly strict gate rejects even safe ones = evolution can't move. Higher is better. |
| **experience gate** | A gate that judges "looks safe" from finite-horizon observation (forgetting tests, etc.), not a sound proof. One negative comparison (STABLE-style). |
| **sound certificate** | A verifier that bounds the worst case from above with a guarantee (cert_inf / cert_two / cert_sdp). Only this sees through the "appearance." |
| **MAP-Elites** | Evolutionary search keeping a grid of diverse solutions. The "evolution" side. |
| **finite-diff / analytic gradient** | Weak gradient (estimate slope by nudging, dim+1 evals/step) vs strong gradient (exact slope in one backprop pass). |
| **meta-gate** | When evolution "wins," bring in a stronger opponent (analytic gradient) and check whether the gain survives. If it vanishes, it's an illusion (ARTIFACT). |
| **Langton's ant** | An ant on a grid driven by a few deterministic rules; looks chaotic, then suddenly builds a "highway." A metaphor for **simple determinism creating apparent order/complexity**. |

---

### ② Plain words — the Langton's-ant illusion in three scenes

#### Scene 0: What Langton's ant is (why this metaphor)

Langton's ant moves on a grid by just two rules ("on white, turn right and flip the color"; "on black, turn left and flip"). For the first few hundred steps it walks chaotically. But after about 10,000 steps it suddenly builds a regular **104-step-period pattern** called the "highway" and travels straight.

Two cores of this research live here:

1. **Simple deterministic rules create apparent order/complexity.** The rules are trivially simple, yet the result looks complex ("chaos → sudden order").
2. **Appearance and essence diverge.** Observing the ant mid-chaos cannot foresee the highway; and vice versa. **Empirical observation is fooled by the "appearance" simple things create.**

The claim: the same happens in AI. Both "apparent stability" and "apparent evolution (monoculture = apparent superiority)" collapse, underneath, to **deterministic-simple**. Experience is fooled; only the sound certificate sees through the illusion.

#### Scene 1: "Apparent stability" — a diverging structure looks stable when observed

The small memory block bolted onto an LLM keeps its state bounded with `tanh`. So **even when unstable (ρ≥1), the output norm does not diverge**. The state never explodes; it stays bounded.

Result: **even a structure with true ρ = 2.9 (fully divergent), observed along one trajectory, has its initial perturbation "appear to decay"** — measured, perturbation 1 shrinks to `2e-14`, as if safe (contracting). This is a coincidental conjunction of `tanh` saturation and perturbation-direction misalignment (it doesn't ride the divergent direction).

Every naive check fails here:

- Monitor the state norm → bounded, no anomaly (fooled).
- Finite-horizon "forgetting test" → looks forgotten (fooled).
- Single-trajectory perturbation sensitivity → looks decaying (fooled).

This is exactly Langton's ant. **Simple dynamics (tanh-bounded) create the appearance of "safe" for a dangerous structure.** Only one thing sees through: the **sound certificate's worst-case (box-sup) evaluation**, which bounds the maximum amplification over all inputs/states and is not fooled by one accidentally-safe trajectory. It detected `σ_max = 4.87 > 1` and correctly rejected.

#### Scene 2: "The experience gate misses 84%" — the scale of the illusion

At population scale: a 400-gene mix of 95 divergent (truly blow up) + 305 contracting (truly safe). How many dangerous ones does each method miss (false-admit)?

- **No gate**: passes all 95/95 divergent as "safe" = **100% false-admit**.
- **STABLE-style experience gate** (a representative "experience-based stability gate" also used by other camps): **misses 80 of 95 (84.2%)**.
- **sound certificate (cert_inf / cert_two / cert_sdp)**: **0%** false-admit.

The shock of 84% is that it barely improves on "no check = 100%." The experience gate is **fooled by the Langton's-ant illusion 84% of the time while believing it is checking.** Why: as in Scene 1, under `tanh`-bounded dynamics, divergent structures "appear to forget perturbations" under finite-horizon observation, and the experience gate (built on finite-horizon observation) believes that appearance. The sound certificate bounds the worst case with a guarantee, unswayed by appearance. In particular, **cert_sdp keeps 0% false-admit while over-rejecting genuinely-safe individuals by only 4.6%** — sound and most navigable.

#### Scene 3: "Apparent evolution" — evolution looks 20–0 (but it's an illusion)

Langton's ant ver.2 happened on the capability side.

On a real terrain made by an actual SmolLM2, evolution (MAP-Elites) vs the weak gradient (finite-diff) → **evolution 20–0** (+0.029 mean CE, p=9.5e-7). An "order" where evolution beats gradient seemed visible; an SNS-friendly headline flashed by.

But this too was Langton's ant. **The opponent (finite-diff) was just weak.** Our framework had a meta-gate from the start ("if you win, call the strong opponent"). Calling the strong analytic gradient (backprop = the exact gradient real LLM training uses) at the same budget: **gradient overturns evolution 19/20** (diff +0.008, p=3.5e-4). Evolution's win was a weak-opponent artifact. Verdict = **ARTIFACT + NEGATIVE**.

Most importantly: **without the meta-gate (a sound comparison opponent), I would have published the false-positive "evolution wins capability 20/20 on real terrain."** "Doubt the breakdown before celebrating" actually stopped one false-positive, in data. This too is a sound discriminator seeing through Langton's ant.

#### The claim (three scenes unified)

Experience is fooled by appearance. Only the sound certificate (and its capability-side version, the meta-gate) sees the essence. So verified-plasticity's value is not "gets smart" (capability) but "can be guaranteed/measured not to blow up" (GUARANTEE).

---

### ③ Details — H-discriminative numbers, the capability outcome, framework-ness, the small-n wall

#### 3.1 What framework verified-plasticity is

The main axis is the **Verified-Plasticity Evaluation Framework**. Before claiming "our method is strong," build **the ruler**. The ruler is guarded by six devices: (1) pre-registration, (2) Holm conjunctive judgment, (3) artifact discipline, (4) falsification clauses, (5) self-power audit (positive control), (6) anti-over-claim critic.

The methods under test: **VSOA** (cert-gated topology evolution, the headliner), **no-gate** (negative control), **STABLE-style experience gate** (prior-art comparison), **Mamba-130M** (stable-by-construction positive control).

Precisely, the stability metric is not "does the state diverge" but **"echo-state perturbation forgetting."** The kernel is always bounded via `tanh` (the source of Scene 1's illusion); what we measure is "are initial perturbations forgotten (contraction ρ<1 = echo-state property holds)."

#### 3.2 H-discriminative — the framework's discriminative power (core numbers)

n=6, a 95-divergent / 305-contracting gene population.

| method | sound? | false-admit (missed divergent) | over-reject (contracting) |
|---|---|---|---|
| no-gate | ✗ | **95/95 = 100%** | 0% |
| STABLE-style experience gate | ✗ | **80/95 = 84.2%** | (experience gate) |
| cert_inf | ✓ | **0%** | 70.5% |
| cert_two | ✓ | **0%** | 52.8% |
| **cert_sdp** | ✓ | **0%** | **4.6% (most navigable)** |

On a positive-control population (0-divergent safe family, Mamba-style), **all methods have 0 false-admit** — confirming they don't wrongly reject a safe family.

**Why the STABLE-style gate misses 84% (educationally):** the echo-state pass condition is "true ρ < 1." But with a `tanh`-always-bounded kernel, **even a true-ρ≥1 divergent structure appears to forget perturbations under finite-horizon observation** — `tanh` saturation hides the divergent amplification inside the observation window. The STABLE-style gate, built on finite-horizon observation, judges that appearance as "safe." That is the Langton's-ant illusion. A sound certificate bounds the worst case from above (proof, not observation) and is unswayed.

**A deeper illusion (even single-trajectory sensitivity is fooled):** as in Scene 1, even a ρ≈2.9 divergent gene has **even its single-trajectory perturbation sensitivity not diverge** (measured 1 → 2e-14), because `tanh` saturation + perturbation-direction misalignment coincide. So state-norm monitoring, finite forgetting tests, and single-trajectory sensitivity all miss ρ≥1 — only the box-sup sound certificate (rejecting at `σ_max = 4.87 > 1`) catches it. This is the strongest demonstration that "only a sound certificate sees it."

#### 3.3 The honest capability outcome — synthetic NULL_TIE → real CE ARTIFACT+NEGATIVE

**(1) synthetic multi-peaked terrain (K=6 basins) = NULL_TIE.** MAP-Elites ≈ gradient ≈ random. ME vs gradient: mean_diff +0.028 / Wilcoxon p=0.39 / sign_delta=0 (n=20). The 4-condition AND fails in all directions = a **pure tie** = capability superiority **unproven**.

**(2) real SmolLM2-CE terrain = ARTIFACT + NEGATIVE.** Building a "predict the next internal-representation cluster" CE terrain from SmolLM2's layer-15 hidden states, same budget, 4 methods (held-out mean, higher better):

| method | held-out mean | rank |
|---|---|---|
| **analytic gradient (torch Adam)** | **-1.446** | **1st (best of all)** |
| evolution (MAP-Elites) | -1.454 | 2nd |
| random | -1.473 | 3rd |
| finite-diff (weak gradient) | -1.483 | 4th |

- evolution vs finite-diff: ME **beats 20/20** (diff +0.029, p=9.5e-7, looks EXISTS).
- evolution vs analytic gradient: analytic **overturns 19/20** (diff +0.008, p=3.5e-4).

→ ME's win is an **artifact** of finite-diff's weakness (cold-start / dim+1 evals/step / ~95 steps in budget). With a strong gradient, gradient > evolution = **capability NEGATIVE even on real terrain**.

**The real value of honest disclosure (a false-positive stopped):** without the strong-gradient meta-gate, I would have **wrongly concluded the false-positive "evolution wins capability 20/20 on real terrain."** "Doubt the breakdown before celebrating" actually removed one false-positive — Langton's ant ver.2 seen through by a sound discriminator (the meta-gate).

#### 3.4 Framework-ness (F8) — (b) PASS / (a) NULL

**(b) 3 plug-point swap = PASS.** Swapping GeneCodec / Objective / VerifierBackend by a **single object** each, src untouched (empty git diff), pytest 17 green; per-gene two⇒sdp / inf⇒sdp with 0 violations over 3000 genes. The "substrate / objective / certifier" plug-points are swappable, in data.

**(a) structural diversity → generalization load-bearing = NULL.** The hypothesis "structural diversity helps generalization" does **not hold** (held-out diff +0.011, p=0.55, a first-class NULL). Disclosed honestly — swappable, yes; "diversity helps" is not demonstrated.

#### 3.5 Mamba SSM Lyapunov positive control (§7.3) — calibrating the ruler

To audit the ruler's self-power (does it correctly call a safe base safe), we used Mamba. **Mamba-130M has A = -exp(A_log) < 0 across all 24 layers (589,824 ch)** → λ_max ≤ 0 trivially → stable-by-construction, PASS. **SmolLM2 has no SSM** (llama arch, self_attn + mlp only, no state recurrence) → safety must be imposed by a bolted-on gate. So the framework discriminates "safe base (Mamba)" from "needs-a-gate base (SmolLM2)" at the base level (PASS). Caveat: this is the triviality of parameterization — it holds structurally for any valid Mamba, so we test that parameterization guarantees stability, not that stability was learned.

#### 3.6 Adversarial verification — having independent skeptics refute our numbers

We cross-checked this verdict's numerical claims with **3 independent skeptics + a 3-seed re-run on real hardware**. Result = **MAJOR 0 / all MINOR**, zero numerical mismatches, no finding overturning a mechanistic conclusion. For the main result (capability), a verifier loaded SmolLM2 itself and re-ran 3 seeds independently, deterministically reproducing "strong gradient beats evolution."

#### 3.7 The small-n wall (first-class negative)

Guarantee stands, but the **scale wall** remains, honestly. Verified structural evolution is limited to **small-n per-component (n≤4-6)**. A high-dimensional navigable-and-sound certifier is **absent** (first-class negative) — the continuation of #39's 2^n wall. SDP (cert_sdp) only raised the navigability ceiling; it did not break the 2^n cost wall.

---

### Honest caveats (no over-claim)

As the capstone of three installments, all caveats in one place. Read this to avoid confusing capability and guarantee.

- **capability NULL_TIE is a "non-significant tie."** Neither a "decisive proof evolution is worse than gradient" nor a "powered equivalence proof" (power not analyzed). Do not call NULL_TIE "evolution's defeat" = **unproven**.
- **The 40-basin figure may be a high-dim hillclimb non-convergence artifact.** Robustly we say only "multi-peaked (>1)."
- **gate neutrality is observed only on held-out, in a capability-flat regime.** The train side has archive-exploration constraints at a 0.25 gap.
- **STABLE 84% is config-dependent** (EPS_FORGET=1e-2 / T=64 / K_PROBE=8 fixed, sensitivity unmeasured). The direction (STABLE misses danger) is robust, but "84%" is not a config-independent number.
- **empirical_rho is from-below.** 0 observed false-admit is strong consistency, not an absolute or machine proof.
- **real CE is a hidden-cluster CE proxy** (not full-vocab softmax; full-vocab degenerates at small n).
- **verified structural evolution is small-n per-component (n≤4-6) only.** A high-dim navigable-sound certifier is absent (first-class negative).
- **real LLM transfer (load-bearing of tiny→SmolLM2) is unverified.**

---

### On competitors' self-improvement claims — only the fact that they are "unverified," without disparaging

The trend of "AI that gets smarter the more you use it / self-evolves" is real. As of the 2026-06-10 competitor scan: **hermes-agent** (NousResearch, 189k★) — "40% faster with 20+ skills"; **ECC** (211.8k★) — Continuous Learning; **headroom learn** — continual-learning lineage. But all of these performance claims are **third-party-unverified self-benchmarks** (as of 2026-06-10). Star counts prove popularity, not performance superiority.

The point is **not to disparate competitors**. Their "got smarter" claims may be real, or may be a Langton's-ant illusion — **without a tool to tell falsifiably, an outsider cannot distinguish them**. verified-plasticity is exactly that tool. Even our own claim (#40's evolution 20–0) turned out to be an illusion under the meta-gate, so the need for a discriminator is self-demonstrated.

---

### Even world models cannot issue guarantees — distinguishing contribution from guarantee

Another major current is **world models**: an agent holds an internal environment simulator and predicts actions. Powerful, and it contributes to safe design too. As a technical fact, however, world-model approaches generally can contribute to safe design but **do not provide a formal guarantee**. This is an observation widely shared in the technical community (a 2026 lecture by Hironobu Fujiyoshi expressed the same gist). Contribution and guarantee must be treated as distinct.

verified-plasticity's place becomes clear here. Where world-model approaches stay at "contribution," **verified-plasticity issues a GUARANTEE with a sound certificate** — bounding "contracts (ρ<1, doesn't blow up)" by proof, not appearance. Not a replacement but a complement: the world model predicts actions cleverly; verified-plasticity guarantees that its structural adaptation does not blow up.

Technically, this aligns with the general observation that the history of AI has moved toward machines acquiring (evolving) structures we used to hand-design. This research's evolution thesis sits in the same direction. Who guarantees that "self-acquired structure" doesn't blow up? verified-plasticity's answer: "a sound certificate does."

---

### Wrap-up — three arcs converge to one point

- **#38**: defensive disclosure — took the four-point intersection of "proof-carrying memory" in theory, planted a flag by publication not patent.
- **#39**: the window closed in implementation, but the 2^n wall (small-n wall) didn't budge.
- **#40**: does it get smart? → NO. Strong gradient beats evolution even on real terrain. Capability can't be sold (Langton's ant ver.2 seen through by the meta-gate).
- **#41 (this one)**: all of it converges to one point — **"simple determinism creates apparent order/complexity, experience is fooled, only the sound certificate sees the essence."**

The true identity of an "evolvable LLM" is **not "an AI where evolution wins on performance," but "a framework that guarantees and measures, with a sound certificate, that online structural change does not blow up or catastrophically forget."** Unglamorous. But while "gets smarter the more you use it" and "world models hand you safety" are pleasant headlines, **a tool to tell falsifiably whether "got smarter / got stable" is real or an illusion** barely exists. verified-plasticity is that discriminator.

The value is **GUARANTEE, not capability.** World models cannot issue a guarantee (they stay at contribution); verified-plasticity issues one with a sound certificate. Experience is fooled by appearance — only the certificate is the eye that sees through the Langton's-ant illusion.

Source: [github.com/furuse-kazufumi/llcore](https://github.com/furuse-kazufumi/llcore) — paper draft + all experiment code/data.

---

<a id="中文"></a>

---

## Chapter 5 Chapter 5

(To be expanded in a follow-up session)

---

<a id="中文"></a>


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

![「ひくわ」と一万円札を差し出す森田](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/012.jpg)
> 🗒️ *「ひくわ」— 紹介リンクで小銭を稼ごうとする魂胆、我ながらちょっと引く*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

<!-- /CTAIMG -->
