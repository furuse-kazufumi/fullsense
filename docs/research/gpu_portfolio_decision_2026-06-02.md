# GPU Investment — Decision-Support (FullSense Lab)

**Date:** 2026-06-02
**Status:** Internal decision-support. This document gives analysis, not a directive. **The investment call is the user's.** It lays out the portfolio of GPU-needing experiments, the rent-vs-buy economics, and one concrete first experiment with a pre-registered go/no-go, so the choice can be made on evidence rather than on the appeal of a single research question.

> **One-line stance:** Do not buy hardware yet. The two highest-research-value items can be advanced for ~zero new GPU spend (existing on-prem host) or a single ~$40 cloud rental. Only one portfolio item is genuinely hard-gated on owned hardware, and its "frontal win" is honestly assessed as unlikely. **Rent first, let the portfolio's demand trigger the purchase — not one experiment's promise.**

---

## 1. Executive summary & recommendation

### Recommendation: RENT-FIRST, PORTFOLIO-TRIGGERED

1. **Start what needs no GPU money.** The keystone item (llive real-LLM evolution, small/medium scale) runs on the **existing on-prem Ollama host today**. CPU-slow (~88 s/call), but architecturally unblocked. The only real blockers are a user "go", seed/generation count, and a real-LLM B2 quality rubric. **This is the highest value-per-dollar move and costs nothing new.** Do it before buying anything.

2. **Resolve the open research question with one capped cloud rental, not a purchase.** The llcore ③ ("is selection/niching load-bearing on a real full-LLM loss landscape?") question is the *only* path left for ③, and it is **better-motivated after BG9** (BG9 found ③ needs a high-dimensional hard coordinate; a full LLM is high-dimensional). But it is **still a bet** — backprop is the high-dim analogue of BG9's random-restart baseline and may navigate the landscape directly, making ③ unnecessary. A pre-registered, budget-capped single run answers it cleanly either way. A negative is as publishable as a positive (a paper is already drafted, 7,103 words).

3. **Defer the hardware purchase until portfolio demand crosses the rent-vs-buy line.** Only the "Mythos-surpass full evolution scale" item is hard-gated on owned hardware (explicitly "new PC required", user-confirmed 2026-05-28), and its frontal "beat Mythos 100%" goal is honestly assessed as difficult/unlikely. That makes it the **largest, lumpiest spend with the lowest value-per-dollar** — not the item to justify a purchase on its own. Buy hardware when *sustained* monthly GPU-hours from the whole portfolio cross the threshold in §3, not on this item's promise.

### Concrete first experiment (proposed)

- **What:** BG10 — the pre-registered ③ full-LLM load-bearing test (condensed in §4).
- **Where:** A single rentable 24 GB-class GPU (RTX 4090 / A10 / L4 / 3090-class) on a free-egress GPU-specialist cloud (RunPod, Lambda, or Vast.ai). Use **spot/interruptible** — every (method, seed) chunk is independently checkpointed and re-runnable, so preemption costs at most one chunk.
- **Budget (rough, from §3 economics):** Pre-registered hard cap **≤ 30 GPU-hours**, **≤ ~$40** at ~$1.2/GPU-hr. At marketplace 4090 spot rates (~$0.25–0.40/hr) the *expected* spend is closer to **~$8–12**; the $40 cap is the stop-and-report ceiling, not the estimate. A **2-seed, ¼-budget smoke run (~$2–5)** gates the full spend.
- **Go/no-go is pre-registered** (see §4): if the harness positive control fails, or the task suite is inert, or the circularity probe fires, the run is declared **N/A** and **no hardware decision follows from it**.

### The three go/no-go gates for committing real GPU *capital* (not just a rental)

1. **Is portfolio GPU demand high enough?** Today: **no** — only one item is hard-gated, and it can wait. Re-evaluate when sustained usage approaches the §3 threshold (~300–500 GPU-hr/month for a year+).
2. **Is there a pre-registered, falsifiable experiment with a clear go/no-go?** For ③: **yes** (BG10). This is what makes a *rental* defensible.
3. **Is the measurement instrument non-circular and validated?** BG10 builds in a mandatory circularity probe and a positive-control validity gate precisely because the prior DECEPTIVENESS_MEASURE work failed on circularity. **Do not buy GPU scale to chase a metric that has not cleared its own validity gate.**

---

## 2. Portfolio inventory

Verified 2026-06-02 against the actual project directories (llcore, llive, lleval, llmesh, fullsense) and the named audit/status/memory docs. Items flagged **unverified** rest on point-in-time memory that could not be re-confirmed in code.

| # | Item (project) | GPU role | CPU-vs-GPU verdict | Value | Compute scale | Priority (value/$) |
|---|---|---|---|---|---|---|
| 1 | **llcore ③ full-LLM loss-landscape** (llcore) | Real full-LLM backprop landscape — the only substrate where ③ might be load-bearing (only one with a genuine high-dim hard coordinate) | **GPU-required** (CPU paths structurally exhausted: Step4→StepC→ladder-1→E-A→StepD→BG9 all decisive) | High research (negative-result paper drafted). **Honest bet** — backprop may solve directly. Product value indirect | Modest: one pre-registered run, not a campaign. Audit names RTX 4090 24 GB minimum | **2** (best research value for a *purchase-free* test) |
| 2 | **llive real-LLM fitness + 1000-gen run** (llive) | Real on-prem LLM eval per individual; pop×gens×inference dominates | **CPU/on-prem now**; GPU only for throughput at large pop×gens | High — keystone for "research-meaningful" runs + animated-SVG product narrative | Scales with pop×gens. Small/medium feasible today (CPU-slow ~88 s/call). Large (pop 256→4096) GPU-gated | **1** (highest — ~zero new spend; on-prem host exists) |
| 3 | **Mythos-surpass full evolution scale** (llive ↔ RAPTOR) | Real-LLM agentic evolution at scale (pop 256→4096), multi-turn exploitation, Cybench head-to-head | **GPU hard-gated** — doc states "GPU 必須… 新 PC 購入が前提" (user-confirmed 2026-05-28). 88 s/call CPU → tens of thousands of s = infeasible | Research value real (Goodhart-resistant via deterministic verifier). Frontal "beat Mythos 100%" honestly **difficult/unlikely** | **Largest** — framed as new PC / dedicated box, not a one-off rental | **3** (high absolute value but lumpiest spend, lowest value/$) |
| 4 | **PERSONA-FX evolution** (llive, future) | None structurally new — novelty×correlation matching on top of existing loop | **CPU-fine** (matching is CPU-trivial); inherits #2's scale only if real-LLM reward used | Medium (diversity engine, demo) | Negligible standalone | **6** (no GPU spend warranted) |
| 5 | **lleval on-prem benchmarks** (lleval, `0.1.0a0`) | Throughput for local-model (llama.cpp/ollama) benchmarking | **CPU/mock works**; GPU is convenience not gate | Medium-high (portfolio measurement tool) | Small-medium | **4** (low marginal value; fund only as by-product of a box bought for #1/#3) |
| 6 | **VLM / multimodal** (llive VLM-FX, manga encoder, audio/sensor) | Local vision encoders (SigLIP2, DINOv2, Magi/Manga-OCR) + local VLMs. **Fine-tuning a manga encoder is the one training (not inference) item** | **Inference: small models fit 24 GB.** **Fine-tune: the only item that could justify owned sustained-VRAM multi-GPU** | Medium-high *strategically* (user's domain = image/3D metrology). Near-term low (not started) | Inference small; fine-tune sustained. **unverified — confirm roadmap** | **5** (high strategic fit but least-committed, most training-heavy; defer) |
| 7 | **llmesh** | None identified (SPC/MQTT/OPC-UA/MCP + speculative-mesh = CPU/LAN) | **CPU** | n/a | n/a | — (no GPU) |

### Genuinely-needs-GPU summary

- **Genuinely require GPU (can't be done meaningfully on CPU):** **#3** (hard-gated, new-PC-confirmed), **#1** (only path left for ③; CPU paths exhausted), **#6 manga encoder fine-tune** *if pursued* (training, not inference).
- **GPU only helps throughput, not architecturally required (stay CPU/on-prem now):** **#2** (on-prem host today; GPU for large pop×gens), **#5** (CPU/mock suffices).
- **No GPU at all:** **#4 PERSONA-FX**, **#7 llmesh**, **#6 VLM inference** (small models fit 24 GB — convenience only).

---

## 3. Economics summary (rent vs buy)

**Prices are mid-2026 approximate ranges (±20–30 %), not quotes.** Marketplace/spot prices swing daily; the RTX 4090 is EOL/scarce and the Blackwell ramp is actively moving the market. Verify live rates before committing budget.

### Hourly rental (on-demand, representative mid-points)

| GPU class | Cheapest marketplace | Managed cloud (RunPod/Lambda) | Hyperscaler (AWS/GCP/Azure) |
|---|---|---|---|
| RTX 4090 (24 GB) | $0.18–0.35/hr | $0.34–0.69/hr | n/a |
| L40S (48 GB) | ~$0.50–0.70/hr | $0.72–0.86/hr | higher |
| A100 80 GB | $0.78–1.10/hr | $1.39–1.99/hr | $3.4–5.8/hr |
| H100 80 GB | $1.03–2.50/hr | $2.49–4.29/hr | ~$6.9/hr |

Managed clouds run 2–4× the marketplace floor (reliability/support trade). Hyperscalers run another 2–3× above that. **Lambda has no spot tier.**

### Example workload costs (the relevant shapes for this portfolio)

- **Small LLM fine-tune (100M–1B params, a few GPU-hr):** ~1–5 GPU-hr on a 4090/A100 → **roughly $1–10 total**. *Extrapolated from sourced 7B-QLoRA figures — order-of-magnitude only.*
- **Neuroevolution / loss-landscape probing (many short runs) — this is BG10's shape:** a campaign of ~200 short runs × ~3 min ≈ 10 GPU-hr → **~$2.50 spot, ~$4 on-demand** on a 4090. Even 1,000 GPU-hr of exploration ≈ **~$250–700**. This is the **canonical spot/interruptible workload**: short, idempotent, independently re-runnable — preemption costs one run, not a checkpoint-restore.

### Rent-vs-buy crossover

Breakeven hours ≈ (hardware price) ÷ (hourly rental of the equivalent GPU), before electricity/cooling/depreciation/resale.

- **Hardware prices (mid-2026):** RTX 4090 new ~$2,000–3,700 (EOL/scarce; MSRP $1,599), used ~$1,100–2,300; a full 4090 workstation ~$2,500–3,500. A100 80 GB used ~$4,000–9,000, new $8,000–15,000. H100 ~$25,000–32,000+ (unusual for a small lab).
- **A $3,000 4090 workstation vs renting a 4090 at $0.50/hr → ~6,000 GPU-hr breakeven** (before power). A100 80 GB ($15k) only pays back after **~19,000 hr**; H100 after **~23,000 hr** — for data-center cards, renting almost always wins for a small lab unless utilization is near-continuous for years.
- **Practical rule (synthesized):** owning wins only above ~40–50 % utilization of the depreciation window.
  - **< ~150–200 GPU-hr/month (a few hr/day): rent.** A $3,000 4090 box ÷ $0.40/hr ≈ 7,500 hr ≈ 3+ years to break even on hardware alone.
  - **~300–500+ GPU-hr/month sustained (10–16 hr/day) for a 4090-class workload for a year+:** buying a 4090 box starts to make sense, plus zero-latency local iteration and no egress.
  - **A100/H100-class:** rent unless near-24/7 multi-year demand.

**Hidden costs that move the line:** 4090 ~450 W ≈ $0.067/hr at $0.15/kWh (~$130/yr light use); cooling; ~$1,000+ rest-of-machine; RMA downtime; **resale collapse on the next generation** (4090 already EOL); and an owned 24 GB card can't access the 80 GB you'd rent on demand for a bigger experiment.

**Egress (the silent budget killer):** hyperscaler egress $0.08–0.12/GB (5 TB ≈ $450 AWS / $600 GCP — can rival the compute bill). **RunPod, Lambda, Salad, Voltage Park: free egress; Vast.ai usually free (host-dependent).** This is the main reason a small lab prefers GPU-specialist clouds over AWS/GCP/Azure. Persistent storage ~$0.05–0.15/GB/month — watch idle volumes you forget to delete.

### Bottom line for this lab

For occasional fine-tuning and bursty neuroevolution (likely **well under 200 GPU-hr/month**), **renting wins clearly.** The example workloads cost single-digit-to-low-tens of dollars each. Use a **free-egress GPU-specialist provider**, prefer **spot/interruptible for many-short-runs campaigns** with external checkpointing, reserve on-demand for jobs you can't afford to lose. Only consider a 4090 workstation if sustained usage climbs past ~300–500 GPU-hr/month for a year+, or if you specifically value local control / zero egress / data privacy. **Buying A100/H100-class almost never pencils out for a small lab at current rates.**

---

## 4. The ③ full-LLM pre-registered experiment (BG10, condensed)

> Full spec mirrors `research/kernel_diversification/BG9_PREREGISTRATION.md`. Suggested location for the full file: `D:/projects/llcore/research/llm_qd_loadbearing/BG10_PREREGISTRATION.md` (new isolated dir; `src/llcore` untouched; git one-shot by orchestrator). The file has **not** been created — flag if you want it written and committed before any run.

### Proposition (falsifiable)

**H8:** On a real full-LLM loss landscape (smallest viable transformer LM, ~10M params), a **Quality-Diversity search (MAP-Elites with a pre-registered functional behavior descriptor)** reaches strictly better held-out task loss than **strong gradient baselines at equal compute** — (i) Adam fine-tune, (ii) **gradient-restart** (the high-dim analogue of BG9's random-restart), (iii) panmictic ES/GA — **AND** that advantage is causally attributable to behavioral diversity crossing a deception gradients cannot cross.

**H0 (null):** Gradient descent navigates the landscape directly; QD/niching adds nothing at equal compute. ③ is NOT load-bearing — the same structural negative as the CPU arc, now confirmed at the only remaining venue.

### Honest bet-framing (stated plainly, not hidden)

The **prior leans toward ③ STILL NOT load-bearing**, for two independent reasons:

1. **CPU-arc consistency** — every CPU substrate where the difficulty was real was either low-dimensional or smooth, and a strong direct baseline solved it (Step4 only positive on a *synthetic* corridor; Step C / ladder-1 / E-A smooth; Step D unimodal; BG9 kernel-union closed structurally).
2. **Backprop-as-strong-baseline (the decisive risk)** — BG9's random-restart defeated ③ because it could *teleport* to the answer. On a full LLM, **backprop is an even stronger direct navigator**: it computes the exact local descent direction at every point. High dimensionality is **necessary but not sufficient** for ③ — the landscape must also be **deceptive in a way gradients cannot escape**. If backprop reaches the competitive basin directly, ③ is again unnecessary.

So this is a **real bet, framed honest-symmetric**: a negative ("backprop is strong enough even in 10⁷ dims; QD adds nothing") closes the ③ arc decisively and is publishable; a positive ("there exist real-LM regions where behavioral niching crosses a gradient-impassable deception") is a genuine mechanism discovery. **An over-clean positive is to be distrusted.**

### Design (immutable after commit)

- **Descriptor B (circularity-hardened):** primary = **B1**, an 8-dim *functional* fingerprint (per-probe-category losses/accuracies on 8 held-out probe categories) computed on a **PROBE set disjoint from the QD objective (JUDGE set) and the final FRESH held-out set**. B2 (representational geometry: top-r CKA-to-anchor + activation stats) is a robustness descriptor for the adversarial lenses, not primary. The objective and descriptor live on **disjoint data and are different functionals** — the explicit fix for the DECEPTIVENESS_MEASURE circularity failure (where `behavior = mean(g)` was the very axis fitness was carved on).
- **Mandatory circularity probe (run BEFORE the headline):** measure `corr(fitness_judge, B_dim)` and canonical-corr(B, fitness). If `max |corr| > 0.7` or the QD advantage is explained by a single near-collinear B-dim → **quasi-circular → verdict N/A**. We report it; we do **not** swap descriptors after seeing it.
- **Archive:** CVT-MAP-Elites, C = 512 centroids (grid infeasible at 8-dim); robustness sweep C ∈ {256, 512, 1024}.
- **Equal-compute fairness gate (the single most important control):** budget = total fwd+bwd-equivalent **FLOPs**, not wall-clock or "evaluations". 1 Adam step ≈ 3× forward FLOPs; 1 QD eval = 1 forward pass. All methods get the same `F_budget` (≈ 2,000-Adam-step-equiv). QD uses **gradient-aware emission (ME-ES)** — niching for *selection*, gradients for *local moves* — so the test is "does behavioral niching *on top of* gradient local-search beat gradient local-search alone", isolating ③ from the gradient question (not a gradient-free strawman).
- **Seeds:** n = 12, CRN/paired, same network init per seed across methods. **best = global best-of-budget re-evaluated on a FRESH held-out set** (no archive-max forgetting / elitism carry-over bias).
- **Statistical gate:** beats baseline = one-sided paired Wilcoxon p<0.05 ∧ Cliff |δ|≥0.2 ∧ paired mean diff>0. **③ load-bearing requires QD to beat ALL THREE** baselines (esp. gradient-restart) on FRESH held-out at equal FLOPs.

### Scale & budget (fixed)

- **Model:** single ~10M-param transformer (4-layer, d_model=256, 4-head GPT on a char/byte corpus, or a tiny-LM checkpoint). High-dimensional (10⁷ ≫ the 24-dim CPU corridor and ≫ BG9's 4-discrete kernel_id — the dimensionality BG9 said was the missing ingredient) yet cheap.
- **Adaptation regime** (not from-scratch) on a multi-task suite plausibly inducing a deceptive barrier; suite frozen by a strong-BG6 validity gate (≥2 distinct behavioral specialists win different tasks) **before** the run.
- **Budget:** single 24 GB-class GPU; **≤ 30 GPU-hr total**; **hard $ cap ~$40 at ~$1.2/GPU-hr** → exceed = stop, report partial as N/A-by-budget, do **not** extend. Chunked & resume-by-skip-existing per (method, seed). **Smoke-first gate:** a 2-seed, ¼-budget smoke must show the positive control validating and FLOP-parity confirmed before spending the full 30 GPU-hr.

### Three substrates + three-value verdict

- **Positive control** (synthetic loss-barrier in real-LM weight space): QD must beat all 3 baselines FIRST. **If it can't, the harness can't detect ③ even when present → N/A (instrument invalid)** — exactly the row that fired in BG9.
- **Negative control** (convex single-task fine-tune): QD must show **no** advantage; advantage here = harness false-positive → N/A warning.
- **Real** (the honest test): the strong-BG6-gated multi-task suite. A behaviorally-neutral suite is **inert** → report "real = neutral, ③-not-needed direction".

| Verdict | Conditions (all must hold) |
|---|---|
| **③ load-bearing on full-LLM** | positive control PASS **AND** real QD beats all 3 (incl. gradient-restart) on FRESH at equal FLOPs **AND** advantage vanishes with niching off (attributable to ③) **AND** vanishes with random descriptor **AND** Adam-from-init does NOT reach the QD basin **AND** all 4 adversarial lenses pass |
| **③ NOT load-bearing** | positive control PASS but real QD fails to beat all 3 (esp. gradient-restart) → backprop navigates directly = the structural negative, now at the high-dim venue (**the prior outcome**). Honest, publishable, clean arc-closer |
| **N/A (un-measurable)** | positive control fails to validate **OR** real suite inert (strong-BG6 fail) **OR** circularity probe fires (corr>0.7) **OR** C-sweep / seed-group / budget reversal **OR** $/GPU-hr cap hit before signal |

### Confound ablations (if QD wins, isolate WHY)

- **A1 descriptor-ablation** (random descriptor): if advantage survives → not behavioral-diversity-driven → H8 unsupported.
- **A2 niching-off** (panmictic ES, identical emission/FLOPs): if advantage vanishes → attributable to niching = ③ itself.
- **A3 gradient-restart parity**: same restarts×steps; measure how often gradient-restart lands in the better basin — if ≥ QD, ③ adds nothing.
- **A4 "deception gradients cannot cross"**: pure Adam from init for full `F_budget` must NOT reach the QD-discovered basin. This is the falsifiable heart.

### Capital implication (pre-committed)

- **③ load-bearing** → first positive at a real venue; justifies scaling ③ in llive's real-LLM loop *(prior says unlikely)*.
- **③ NOT load-bearing** → the full arc (Step4→C→D→BG9→BG10) closes coherently: ③ is load-bearing only on synthetic constructions, never on a real substrate with a strong direct baseline. **Decisively closes the ③ investment question** — the expected, publishable outcome.
- **N/A** → the instrument is the limit. **Fix the measurement before any larger capital commitment** — the DECEPTIVENESS_MEASURE lesson: do not buy GPU scale to chase a circular metric.

---

## 5. Honest caveats & what is unverified

**This is a bet, not a sure thing (③):** even though BG9 makes the full-LLM venue better-motivated (③ needs high dimensionality, which a full LLM has), backprop is the high-dim analogue of the random-restart baseline that defeated ③ on CPU. It may solve the landscape directly, in which case ③ is unnecessary and BG10 returns the *expected* negative. That is fine — a negative closes the arc and is publishable — but the user should not read "better-motivated" as "likely to be positive".

**The decision is on the portfolio, not on ③:** ③ alone does **not** justify GPU spend — it is a research question, not a product blocker. The strongest argument *for* buying is item #3 (hard-gated, new-PC-confirmed); the strongest argument *against rushing* is that the two highest-value items (#1, #2) advance first via a cloud rental (#1) or the existing on-prem host (#2). Item #3's frontal "beat Mythos 100%" is honestly difficult/unlikely, so it should not be the lone justification for a lumpy purchase.

**Economics are approximate and volatile:** all prices are mid-2026 ranges (±20–30 %), not quotes. The 100M–1B fine-tune and neuroevolution dollar figures are **extrapolated from sourced 7B-QLoRA costs and hourly rates, not directly measured** — order-of-magnitude only. Marketplace/spot prices (Vast.ai, Salad) swing daily by host; 4090 hardware pricing is unstable due to EOL/scarcity. Verify live rates on provider pages before committing budget.

**Flagged unverified — confirm with the user before acting:**

1. **(item #2)** Whether the llive real-LLM run's *open-ended-evolution* scientific payoff justifies the compute, given the ③ arc's finding that the CPU proxy landscapes are smooth. Confirm whether real-LLM fitness is *expected* to be more deceptive than the CPU proxies before scaling pop×gens.
2. **(item #6)** Whether **manga vision-encoder fine-tuning** is actually on the near-term roadmap or aspirational. This is the only item that could justify owned, sustained-VRAM multi-GPU — but it is the least-committed. Defer until intent is confirmed.
3. **(items #5, #6)** The exact current implementation depth of **lleval** and **llive multimodal** beyond the skeleton memories (`0.1.0a0` pre-PoC; audio/sensor landed 2026-05-22; VLM-02 shape bench not built). Treat depth claims as point-in-time.

**Do-not-buy default:** nothing in this analysis is a directive to spend. The default recommendation is **rent-first**; a hardware purchase becomes defensible only when the *whole portfolio's* sustained monthly GPU-hours cross the §3 threshold (~300–500 GPU-hr/month for a year+), or when the user specifically values local control / zero egress / data privacy enough to pay the premium. **The call is yours.**
