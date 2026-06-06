# Verified Memory Evolution: A Defensive Publication

## Sound Contraction-Certified Admission Gating of Evolving Transformer/Recurrent Memory Cores — the Four-Point Intersection

**Author:** Kazufumi Furuse (古瀬 和文) — FullSense project (llmesh / llive / llcore)
**Date of record (priority):** 2026-06-06
**Document type:** Defensive publication (prior-art establishment). Reduced-to-practice for the core mechanism; honest limits disclosed.
**License:** Apache-2.0 + Commercial (FullSense dual-license).
**Canonical source:** FullSense public repository; this file's git commit timestamp establishes the date of record.

---

> **Purpose statement (plain language).** This is a **defensive publication**. We have decided **not** to
> file a patent (a cost decision), and this dated, public, enabling disclosure is the chosen substitute. Its
> goal is to place the design described below into the public domain as **prior art**, so that no third party
> — including large incumbents or follow-on memory-governance work (e.g. SSGM-style) — can later obtain a
> patent on, or assert novelty over, the same concept against us or against the public.
>
> We claim **no** unconditional priority. Our claim is scoped and falsifiable: across our adversarial
> differentiation audit (44 candidates over 7 + 3 angles, plus a dedicated patent-database query of 14 English
> and 3 Japanese queries against Google Patents / USPTO), **we found no prior result — academic or patent —
> simultaneously occupying all four corners of the intersection defined below.** We did find a prior for each
> corner *individually*, and we name it. The correct reading is therefore *"within the scope of our adversarial
> audit, the four corners are not jointly occupied,"* **not** *"world first."*

---

## Abstract (EN)

We disclose, as dated prior art, an architecture and a working method for **verified memory evolution**: using a
**sound contraction certificate** as a **prove-then-reject admission gate inside an evolution/update loop** that
governs the **internal dynamics of a Transformer / recurrent memory core**, with a **running implementation and
experiments**. The four properties in bold are the *four-point intersection* that, in our adversarial audit, no
prior academic or patent result occupies simultaneously, though each is individually anticipated. The certifier is
a **sound contraction certifier ladder** — closed-form ∞-norm supremum → vertex SVD → SDP-Lyapunov — each rung
implying `ρ(J) < 1` (spectral radius below one, i.e. contraction) over the reachable Jacobian box; **no SMT/SAT
solver is in the load-bearing path** (we verified a dedicated Z3 contraction track agreed byte-for-identical with
the closed-form ∞-norm certifier, 0/3270 disagreements, so for this invariant class an SMT solver is decorative).
The gate is **fail-closed**: a child whose dynamics cannot be certified is *rejected* (resampled up to a cap, then
a known-safe fallback is substituted), as opposed to projected, regularized, or structurally constrained
by-construction. We additionally disclose a **tracking-tube inspection metric** that reuses the gate's own
quantities — the state Lipschitz bound `L` and input gain `G` — to report a closed-form tracking-error tube
`r = G·w̄/(1−L)` for a feasible reference trajectory under a bounded disturbance `w̄`, at zero additional proof
cost. We disclose two routes for *verified memory evolution* — (a) gating updates to an agent **memory bank**
(distinguished from NLI-theoretic memory-governance architectures by being a sound proof plus a running gate) and
(b) gating the **internal-state dynamics** of the memory core — and their composition with **SPC control-chart
runtime gating** and a **two-tier ethics gate** (exploration free, admission verified). We disclose all of this
*honestly*: the demonstration scale is small (`n = 8`), the verifier's reachability payoff is *navigability*, not
learning, the gate costs roughly **20–60×** in our measurements, and "zero observed false admits" is an empirical
observation, **not** a machine-checked global guarantee.

## 要旨 (JA)

我々は、日付付きの先行技術として、**検証付き記憶進化 (verified memory evolution)** のアーキテクチャと実施方法を
開示する。すなわち、**健全な縮小性証明 (sound contraction certificate)** を、**Transformer / 再帰型記憶コアの
内部 dynamics** を統べる **進化/更新ループ内の prove-then-reject 採用ゲート** として用い、**動く実装と実験** を
伴う、という方法である。この太字 4 条件が *四点交差点* であり、我々の敵対的監査の範囲では、学術・特許のいずれの
先行も 4 隅を同時には占有していない (各隅は個別には先行が存在し、明示する)。証明器は **健全な縮小性証明器の梯子
(sound contraction certifier ladder)** — 閉形式 ∞-ノルム上限 → 頂点 SVD → SDP-Lyapunov — であり、各段が到達可能
ヤコビ箱上で `ρ(J) < 1` (スペクトル半径 < 1 = 縮小性) を含意する。**SMT/SAT ソルバは load-bearing 経路に存在しない**
(専用 Z3 縮小性トラックが閉形式 ∞-ノルム証明器とバイト単位で一致、3270 件中 0 件の不一致 ⇒ この不変量クラスでは
SMT は装飾)。ゲートは **fail-closed**: dynamics を証明できない子は *棄却* される (上限まで resample → 既知安全な
fallback に置換) のであって、射影・正則化・構造的強制ではない。さらに **tracking tube 検査指標** を開示する。これは
ゲート自身の量 — 状態 Lipschitz 上界 `L` と入力ゲイン `G` — を再利用し、有界外乱 `w̄` 下で feasible な参照軌道に
ついて閉形式の追従誤差 tube `r = G·w̄/(1−L)` を **追加証明コストゼロで** 報告する。verified memory evolution の
2 ルート — (a) エージェント **記憶バンク** の更新ゲート (NLI 理論型記憶ガバナンスとの差 = sound 証明 + 動くゲート)
と (b) 記憶コアの **内部状態 dynamics** のゲート — と、**SPC 管理図による runtime ゲート**・**二層倫理ゲート**
(探索は自由・採用は検証) との合成を開示する。すべてを *honest* に開示する: 実証規模は小さく (`n = 8`)、検証器の
payoff は *navigability* であって学習ではなく、ゲートのコストは実測で約 **20–60 倍**、「観測された false admit ゼロ」は
経験的観測であって機械検査された大域保証 **ではない**。

---

## 1. Field and motivation

Self-evolving and continually-updated AI systems mutate their own parameters, memory, or behavior over time. The
standard safety question — *which* mutations to admit — is usually answered by a numerical heuristic (a loss
threshold, a drift budget), a governance rule (schema/duplicate validation, human curation), or a by-construction
structural constraint (spectral-norm projection). What has been missing, and what this document discloses as a
working method, is a gate whose admission criterion is a **sound mathematical proof of an analytic property
(contraction) of the evolving object's own internal dynamics**, applied **per update inside the loop**, and
**fail-closed**.

We disclose this because we have chosen not to patent it, and we want it to remain freely practicable. The
enabling detail below is sufficient for a person skilled in the art to implement the method.

## 2. The four-point intersection (the disclosed core)

The architecture is defined by the *simultaneous* satisfaction of four conditions. Each, individually, has prior
art (named in §7); the disclosure is their intersection.

> **(i) A sound contraction certificate.** A certifier that proves `ρ(J) < 1` (spectral radius of the
> update Jacobian below one — the contraction / echo-state property: perturbations decay, the map forgets its
> initial condition) over the *reachable* operating box, by a *sound* sufficient condition (no false "certified").
>
> **(ii) Applied to a Transformer / recurrent memory core's internal dynamics** — the `decay`/`W` recurrence of a
> memory/reservoir core — **not** a control plant, a classification head, or a generated code/math artifact.
>
> **(iii) Used as a prove-then-reject admission gate inside an evolution/update loop** — fail-closed: a child that
> cannot be certified is *rejected* (resample, then known-safe fallback), as opposed to *projected* into a safe
> set, *regularized*, or *structurally constrained* so the property holds by construction.
>
> **(iv) With a running implementation and experiments.**

### 2.1 The memory-core dynamics being gated

The gated object is the leaky, saturating recurrence of a memory/reservoir core (RWKV-style state-space update):

```
s_{t+1} = decay ⊙ s_t + (1 − decay) ⊙ tanh(W s_t + V x_t),    V = I        … (1)
```

with the evolving genome `gene = (decay ∈ [0,1]^n, W ∈ [−2,2]^{n×n})`. Its Jacobian with respect to the state is

```
J(t) = diag(decay) + diag((1 − decay) ⊙ t) · W,   t_i = sech²(pre_i) ∈ (0,1]   … (2)
```

over the achievable-derivative box `t ∈ [t_min, 1]^n`. The gate certifies `ρ(J) < 1` on this box; by the Banach
fixed-point theorem this yields a unique, bounded (`|s| < 1`) fixed point and the discrete-time incremental
(δ-)stability standard to contraction analysis: any two trajectories converge exponentially.

### 2.2 The sound contraction certifier ladder (and why no SMT solver is load-bearing)

Three sound certifiers, each implying `ρ(J) < 1` over the box, in increasing cost and increasing expressivity:

| Rung | Sufficient condition proved | Method | Cost |
|---|---|---|---|
| `cert_inf` | `sup ‖J‖_∞ < 1` (each row's absolute-sum supremum over the box) | **closed form**, `O(n²)` | cheapest |
| `cert_two` | `σ_max(J_v) < 1` at all `2^n` box vertices | vertex SVD enumeration | `2^n` |
| `cert_sdp` | common quadratic Lyapunov `P ≻ 0`, `P − J_vᵀ P J_v ≻ 0` at all vertices | convex LMI (interior-point SDP, CLARABEL) | `2^n` LMIs |

**No SMT/SAT solver sits in the load-bearing path.** `cert_inf` exploits that each row's absolute-sum is V-shaped
in `t_i`, so the box maximum is attained at an endpoint and the box quantifier collapses to a per-row 1-D
evaluation — a *sound* gate with no solver. We verified this is a property of the problem, not a missed
opportunity: a dedicated coupled-map Z3 (SMT) contraction track produced certificates **byte-for-identical to the
closed-form ∞-norm certifier — 0/3270 disagreements, and 0/8000 under near-boundary stress** — i.e. on this class
of contraction invariant an SMT solver is *decorative*. (We therefore avoid the misleading "Z3-gated" banner and
describe the gate as what it is: a sound contraction certifier ladder. This sidesteps the solver-dependence and
incompleteness an SMT formulation would introduce.) `cert_inf` is *conservative*: it over-rejects some true
`ρ < 1` contractions (median ∞-norm − ρ gap ≈ 0.477 on our pool), which is exactly why the SDP-Lyapunov rung
exists for the non-closed-form (rotational / non-normal) contractions.

**Fail-closed engineering of the SDP rung.** The genuine LMI solve runs only under the CLARABEL solver; if absent,
`cert_sdp` *refuses* (returns `False`) rather than silently falling back to a solver that false-negatives near the
feasibility boundary. The solver's returned `P` is independently re-checked by eigenvalue tests — the certifier is
never solver-blind. A behaviour-preserving fast path rejects any vertex with `ρ(J_v) ≥ 1` (a necessary condition
for LMI feasibility) before invoking the solver.

### 2.3 The prove-then-reject admission gate (fail-closed, resample cap, known-safe fallback)

The disclosed gate, inside the evolution/update loop, operates as:

```
propose child gene g'                                  # mutation / crossover / gradient step
if certifier.certifies(g'):        admit g'            # sound contraction proof passed
else:
    for k in 1..resample_cap:                          # bounded resampling
        g' ← resample/mutate again
        if certifier.certifies(g'): admit g'; break
    else:
        admit known_safe_fallback                      # fail-closed: never admit an uncertified child
```

Two gate modes are disclosed: `gate_mode = "contraction"` (admit iff the contraction certificate passes) and
`gate_mode = "state_norm"` (admit iff a bounded-state condition passes). The default `"none"` reproduces the
unconstrained loop byte-identically, so the gate is a strictly additive overlay on an existing evolutionary
substrate. The distinguishing semantic — versus the adjacent prior art of §7 — is **prove-then-reject**: an
uncertified update is *thrown away*, not clamped/projected into a safe region (which would alter the proposed
update) and not prevented from ever being un-safe by an architectural constraint (which would trade away
expressivity). This is the contraction-theory analogue of the strategic principle "secure victory first, then
give battle" (Sun Tzu, 軍形篇): the population only admits members already proven to be in the winning posture.

## 3. The tracking-tube inspection metric (zero-added-proof reuse of the gate output)

Beyond *"the core contracts to somewhere,"* a practitioner often wants *"the core tracks a desired reference
trajectory."* We disclose a method that obtains a closed-form tracking guarantee **by reusing the gate's own
quantities**, with no new proof.

Write the map (1) as `F(s, x)`, with two trajectories sharing the reference input `x_ref`:
- reference: `s_ref[t+1] = F(s_ref[t], x_ref[t])` (no disturbance, and a *feasible* reference: a true solution of the system),
- actual: `s_act[t+1] = F(s_act[t], x_ref[t] + d[t])` with bounded input disturbance `‖d[t]‖_∞ ≤ w̄`.

Let `L = sup ‖∂F/∂s‖_∞` (the **same** quantity `cert_inf` uses as its contraction witness) and
`G = sup ‖∂F/∂x‖_∞` (input gain, `G = max_i (1 − decay_i) Σ_j |V_ij|`). The triangle inequality plus the mean-value
theorem give, with `e[t] = s_act[t] − s_ref[t]`:

```
‖e[t+1]‖_∞ ≤ L ‖e[t]‖_∞ + G w̄                                              … (3)
```

If `L < 1` (the contraction gate output), the geometric series converges and, from `e[0]=0`,

```
limsup_t ‖e[t]‖_∞ ≤ r := G · w̄ / (1 − L)                                    … (4)
```

**`r` is the disclosed tracking tube radius.** All three of `L`, `G`, `w̄` come from the same box enumeration the
contraction gate already performs — so the tube is reported at *zero added proof cost* and inherits the
fail-closed discipline (`L ≥ 1` ⇒ tube `= ∞` = no guarantee). The disclosed reporter is a **read-only** function
`tracking_tube(gene, x_ref, w̄) → {L, G, tube_radius, feasibility_residual}` that does not alter the admission API.
It is initially scoped to `cert_inf`-passing genes, for which `L = sup‖J_s‖_∞ < 1` holds directly; for
`cert_two/sdp`-only (rotational) contractions the same derivation runs under the `P`-weighted norm returned by
`cert_sdp`, at a `cond(P)` looseness.

**Empirical witness (small-scale).** On three contraction-passing genes, the measured tracking-error/disturbance
ratios (0.50 / 0.78 / 1.04) sat inside the theoretical gain `G/(1−L)` (1.76 / 2.29 / 2.00); on a non-contraction
control gene the gate rejected (`L = 1.68 ≥ 1`, tube `= ∞`) and the empirical error amplified to **9.3×** the
disturbance — i.e. the gate is load-bearing for the tracking guarantee, not cosmetic.

**What is and is not proved (honest).** The tube inequality (3)–(4) is a *theorem* (Banach + Lipschitz
composition). What is **not** proved: (a) the *validity* of the reference trajectory — whether it is a "good"
memory/task trajectory is the responsibility of the task fitness, outside the verifier's reach, exactly as in
control theory where the reference is given; and (b) *feasibility* (that the reference is a true system solution)
is a numerical identification (residual `ρ_feas`), not a proof, in the general inverse-problem case.

## 4. Verified memory evolution — two disclosed routes

We disclose two distinct application routes, both falling under the four-point intersection, and explicitly
distinguish each from its nearest prior.

**Route (a) — gating updates to an agent memory bank.** Each candidate write/update to an agent's external memory
bank is admitted only if it passes a sound contraction/stability certificate on the memory dynamics, fail-closed.
This route shares the *governing-evolving-memory* framing with NLI-theoretic memory-governance architectures
(SSGM, §7), but differs on the two corners those leave open: the admission criterion is a **sound formal proof**
(not NLI-based contradiction detection), and there is a **running gate with experiments** (not a theoretical
architecture / proof sketch). We disclose this route specifically because the implementation-and-sound-proof gap
that such theory-only architectures leave open is the one a follow-on implementation would otherwise be able to
claim; this dated disclosure forecloses that.

**Route (b) — gating the memory-core internal-state dynamics.** Each candidate update to the memory core's own
recurrence parameters (`decay`, `W` in (1)) is admitted only if the contraction certifier proves `ρ(J) < 1` over
the reachable box, fail-closed. This is the route reduced to practice here (§5). It differs from by-construction
contraction/Lipschitz cores (Enforced-Lipschitz Transformers, R2DN, §7) by gating *arbitrary proposed updates*
with a proof and rejecting failures, rather than constraining the architecture so the property holds for free —
the design axis being **prove-then-reject vs. by-construction**, with the honest tradeoff that the gate trades
*navigability cost* for not having to trade away expressivity structurally.

## 5. Reduction to practice (enabling detail)

The mechanism of §2–§4 is reduced to practice in the FullSense `llcore` package (date of record = this commit):

- The proof gate is **wired into the shipping evolution path** — the production `evolve()` carries additive
  `gate_mode` (`"contraction"` / `"state_norm"`) and `resample_cap` parameters; with `gate_mode="none"` the loop
  is byte-identical to the prior unconstrained behavior, and the gated modes were tested to agree with the
  research-side gated-evolution reference across all modes. Admission is fail-closed: resample up to the cap, then
  substitute a known-safe fallback; **an uncertified child is never admitted.**
- The certifier ladder (`cert_inf` closed-form ∞-norm, `cert_two` vertex SVD, `cert_sdp` CLARABEL SDP-Lyapunov)
  is the load-bearing gate; the SMT track exists only as a *decorative-equivalence* check (0/3270 disagreement).
- The **tracking-tube reporter** (`r = G·w̄/(1−L)`, scoped to `cert_inf`) is implemented as an additive read-only
  reporter with state-Lipschitz / input-gain helpers; the existing admission API is unchanged, and golden test
  values match the PoC cases.
- The test suite covering the gate and reporter comprises 294 tests at the date of record.
- **Observed gate cost: roughly 20–60×** overhead in our measurements (the proof cost is real and disclosed, not
  hidden).

## 6. Composition: SPC runtime gating and the two-tier ethics gate

The disclosed gate composes with two further constructs that we also place in the public domain here:

**SPC control-chart runtime gating.** Evolution-loop metrics (drift, diversity, fitness moments) are fed into a
statistical-process-control control chart (X̄–R / CUSUM, as in the llmesh engine); an out-of-control signal acts
as a *runtime* gate on the evolution loop, complementing the per-update contraction proof with a statistical,
online out-of-distribution guard. The contraction proof gates *each update's analytic property*; the SPC chart
gates *the aggregate behavior of the loop over time*. The two are orthogonal and composable.

**Two-tier ethics gate (exploration free / admission verified).** Variation (mutation, novelty search,
antifragile mutation, "deceptive" exploratory moves) is deliberately *unconstrained* — exploration is free.
Admission (selection into the live population) is *verified* — it must pass the fail-closed proof gate and the
approval path, which cannot be bypassed. This separates the ethics of the two tiers: the exploration tier may be
adventurous (the strategic 詭道 / "way of deception" of Sun Tzu, scoped strictly to exploration), while the
admission tier is honest and gated (the 仁 / benevolence-and-rectitude of the Analects: "know what you know and
know what you do not"). A constraint that lives outside the evolving set and cannot be reached cannot be optimized
away. Most contemporary safety layers are single-tier (an output filter); the two-tier separation is an
architectural choice independent of model scale.

## 7. Boundary with prior art (corner by corner)

We name the nearest prior for each corner. Every arXiv identifier below was confirmed against its abstract before
inclusion. The claim is the *intersection*; each line states which corner the prior leaves un-met.

- **SSGM — Governing Evolving Memory in LLM Agents (Stability and Safety Governed Memory, arXiv:2603.11768, 2026):**
  closest to corner (ii); proposes a write-validation gate rejecting memory updates that contradict protected core
  facts — but the gate is NLI-based contradiction detection (not a sound formal proof), the stability theorem is an
  `O(N·ε)` drift bound stated as a proof sketch, and it is explicitly a theoretical architecture with no
  implementation — leaving corners (i) and (iv) open. **It carries the governing-evolving-memory banner and must be
  cited as such; the window it leaves open is the sound-proof-plus-implementation gap this disclosure occupies.**
- **SEVerA — Verified Synthesis of Self-Evolving Agents (arXiv:2603.25111, 2026):** wraps each model call in a
  Dafny/SMT-verified rejection sampler proving a first-order *output contract* — a by-construction guarantee over an
  output contract, not a per-update prove-then-reject gate on an evolving memory core's contraction.
- **PSV — Propose, Solve, Verify (PSV-Verus, arXiv:2512.18160, 2025):** a sound SMT-backed verifier inside a
  self-play loop admitting only verified solutions — but the verified property is *code correctness of generated
  solutions*, not a contraction property of the evolving weights/memory (corners i–ii open).
- **Provably Safe Model Updates / Locally Invariant Domains (LID, arXiv:2512.01899, 2026):** certifies each
  foundation-model update as `δ`-safe via abstract interpretation and a *project-then-accept* clamp — projection,
  not prove-then-reject; the property is an accuracy-preservation bound, not contraction; the target is a
  frozen-embedding classification head, not a memory core.
- **Synthesis of Parametric Programs using GP and Model Checking (Katz & Peled, arXiv:1402.6785, 2014):** the
  *pattern* — a sound model-checking gate inside an evolutionary loop, reject on failure — is therefore pre-LLM and
  established; the verified object is a classical concurrent program, not an evolving memory core. We do **not**
  claim the gate *pattern* as novel, only its application to a Transformer memory core's contraction.
- **Enforced-Lipschitz Transformers (arXiv:2507.13338, 2025) and R2DN (arXiv:2504.01250, 2025):** enforce
  contraction/Lipschitz *by construction* (spectral soft-cap projection; recurrent parameterization) — the
  strongest "build it in, you don't need a gate" counter-design. We contrast **by-construction enforcement vs.
  prove-then-reject** as a design axis: structural constraint trades expressivity for the guarantee, whereas a
  rejection gate inspects arbitrary updates without that structural constraint.
- **Safeguarded AI (ARIA programme, 2024–2026):** the most authoritative proof-gated-gatekeeper concept, but the
  gatekeeper certifies *actions/plans* against a formal world model before they reach the world — an output/behavior
  gate, not a weight/memory-update gate, at programme stage rather than shipped.
- **Emergent Formal Verification / substrate-guard (arXiv:2603.21149, 2026):** a *running* Z3 system that soundly
  verifies AI *outputs* — post-hoc observational monitoring of outputs, not a per-update gate on an evolving memory
  core.

*(Patent-database boundary.* A dedicated query of 14 English + 3 Japanese queries against Google Patents / USPTO
found **zero** patents occupying the four-point intersection. The nearest patents — `US11715005B2` (hash-based NN
authenticity verification), `US10896032` (certify-then-deploy governance gate), `US11868855` (validating model/
weight "stability" in a resiliency/availability sense) — share *vocabulary* but not the gated object (weight/memory
update), the soundness basis (analytic contraction proof, not hash/attestation/operational test), the target (a
Transformer memory core), or the loop location. Queries phrased as "sound proof gates an update/memory/evolution"
returned almost exclusively academic (arXiv) results even when site-restricted to patent databases — indirect
evidence that the concept remains at the academic stage and is not patented.)*

## 8. Honest limitations (disclosed, not hidden)

- **Demonstration scale is small.** The reduced-to-practice core is `n = 8` (a 72-real-valued gene), a 16 KB
  corpus, a byte vocabulary. "Transformer/LLM memory core" is meant in the **mechanism-feasibility** sense; this is
  not a frontier-scale capability claim.
- **The verifier's payoff is *navigability*, not learning (L3).** The certifier's benefit is the search-space
  *navigability* of the evolutionary process (which dynamics are even reachable), not improved learning per se. The
  effect is EA-specific and vanishes (in final cross-entropy) under gradient descent.
- **The gate is not free: ~20–60× overhead** in our measurements. Short training runs make it look "almost free";
  with sufficient training the cost is real and is disclosed.
- **"Zero observed false admits" is empirical, not machine-checked.** We observed no false admission in our runs,
  but this is an *observation*, **not** a machine-checked global soundness guarantee of the implementation. The
  certifier's *condition* is sound (a proven sufficient condition for `ρ(J)<1`); the *implementation* carrying it is
  ordinary software, not formally verified end-to-end.
- **`cert_inf` is conservative** (over-rejects some true `ρ<1` contractions); the sound tube is initially scoped to
  `cert_inf`-passing genes, with rotational contractions requiring the `cond(P)`-loose `P`-norm tube.
- **Reference-trajectory validity and feasibility are outside the proof** (§3): the tube guarantees tracking *to a
  given reference*; whether that reference is desirable, and whether it is a true system solution, are not certified.
- **The "not found" scope.** "No prior occupying all four corners" is bounded by our adversarial audit and a
  surface-level patent search (Web-routed Google Patents / USPTO, not Derwent/PatBase/J-PlatPat full-claim indices;
  Chinese-native CNIPA search not run; patents have up to an 18-month publication lag). We always retain the "within
  the scope of our search" reservation; exhaustive non-existence is not provable.

## 9. Reproducibility and provenance

The certifier ladder, the proof-gated `evolve()`, and the tracking-tube reporter live in the FullSense `llcore`
package; the adversarial differentiation audit, the patent-database query, and the four-point-intersection
related-work positioning live in the FullSense public repository under `docs/research/` and the `llcore` paper
draft. This document's git commit timestamp is the date of record for the priority statement above.

---

### Changelog

- **2026-06-06** — v1, date of record. Defensive publication establishing prior art for the four-point
  intersection (sound contraction certifier ladder × Transformer/recurrent memory-core internal dynamics ×
  prove-then-reject evolution-loop gate × running implementation) and the tracking-tube inspection metric. The
  proof gate is wired into the shipping `evolve()` (fail-closed, resample cap, known-safe fallback; 294 tests). zh/
  ko translations and any future patent decision are out of scope for this dated record.

---
---

# 検証付き記憶進化 — 防御的開示 (日本語全訳)

## Transformer / 再帰型記憶コアの進化を、健全な縮小性証明で採用ゲートする — 四点交差点

**著者:** 古瀬 和文 (Kazufumi Furuse) — FullSense プロジェクト (llmesh / llive / llcore)
**記録日 (priority):** 2026-06-06
**文書種別:** 防御的開示 (先行技術の確立)。中核機構は reduced-to-practice (実施済)、限界は honest に開示。
**ライセンス:** Apache-2.0 + Commercial (FullSense dual-license)。
**正本:** FullSense 公開リポジトリ。本ファイルの git commit タイムスタンプが記録日を確定する。

---

> **目的 (平易な言葉で).** 本書は **防御的開示 (defensive publication)** である。我々は特許出願を **見送る**
> (コスト判断) と決めており、この日付付き・公開・実施可能な開示がその代替である。目的は、以下に記す設計を
> **先行技術 (prior art)** として公有に置き、第三者 — 大手や記憶ガバナンスの後続研究 (例: SSGM 系) を含む — が
> 後から同一概念を特許化したり、我々ないし公衆に対して新規性を主張したりできないようにすることである。
>
> 我々は **無条件の priority を主張しない**。主張は限定的かつ反証可能である: 我々の敵対的差別化監査 (7 + 3 角度
> 44 候補 + Google Patents/USPTO に対する英語 14・日本語 3 の専用特許照会) の範囲で、**以下に定義する交差点の
> 4 隅を同時に占有する先行 — 学術・特許のいずれも — は発見されなかった。** 各隅は *個別には* 先行が存在し、明示する。
> ゆえに正しい読み方は *「我々の敵対的監査の範囲で四隅は同時には占有されていない」* であって、*「世界初」* ではない。

---

## 要旨 (再掲)

我々は日付付きの先行技術として、**検証付き記憶進化** のアーキテクチャと実施方法を開示する。すなわち、**健全な
縮小性証明 (sound contraction certificate)** を、**Transformer / 再帰型記憶コアの内部 dynamics** を統べる
**進化/更新ループ内の prove-then-reject 採用ゲート** として、**動く実装と実験** を伴って用いる方法である。この
4 条件の同時成立が *四点交差点* であり、各隅は個別には先行が存在するが、我々の敵対的監査の範囲で 4 隅同時占有の
先行はゼロである。証明器は **健全な縮小性証明器の梯子** (閉形式 ∞-ノルム → 頂点 SVD → SDP-Lyapunov) であり、
各段が到達可能ヤコビ箱上で `ρ(J) < 1` を含意する。**SMT/SAT ソルバは load-bearing 経路に存在しない** (専用 Z3
トラックが閉形式 ∞-ノルム証明器とバイト一致、3270 件中 0 件不一致 ⇒ この不変量クラスで SMT は装飾)。ゲートは
fail-closed (証明できない子は棄却 → 上限まで resample → 既知安全な fallback)。さらに **tracking tube 検査指標**
(`r = G·w̄/(1−L)`, 追加証明コストゼロ)、**verified memory evolution の 2 ルート** (記憶バンク更新ゲート /
記憶コア内部 dynamics ゲート)、**SPC 管理図 runtime ゲート**、**二層倫理ゲート** (探索自由・採用検証) を開示する。
すべて honest に: 実証規模は小 (`n=8`)、payoff は navigability であって学習でない、ゲートコストは実測 **20–60 倍**、
「観測された false admit ゼロ」は経験的観測であって機械検査された大域保証 **ではない**。

## 1. 分野と動機

自己進化・継続更新型 AI は、自らのパラメータ・記憶・振る舞いを時間とともに変異させる。標準的な安全性の問い —
*どの* 変異を採用するか — は通常、数値ヒューリスティック (loss 閾値・drift 予算)、ガバナンス規則 (スキーマ/重複
検証・人手キュレーション)、あるいは構造的強制 (スペクトルノルム射影) で答えられてきた。欠けていたもの — 本書が
実施方法として開示するもの — は、採用基準が **進化する対象自身の内部 dynamics の解析的性質 (縮小性) の健全な
数学的証明** であり、**毎更新・ループ内** で適用され、**fail-closed** なゲートである。

我々はこれを特許化しないと決めたから開示する。自由に実施可能なままにしておきたいからである。以下の実施可能詳細は、
当業者が本方法を実装するのに十分である。

## 2. 四点交差点 (開示の中核)

アーキテクチャは 4 条件の *同時* 成立で定義される。各々は個別には先行があり (§7 で命名)、開示はその交差点である。

> **(i) 健全な縮小性証明** — 到達可能な作動箱上で `ρ(J) < 1` (更新ヤコビのスペクトル半径 < 1 = 縮小性/エコー
> ステート性: 摂動が減衰し初期条件を忘れる) を、健全な十分条件で証明する (偽の「証明済」を出さない)。
>
> **(ii) Transformer / 再帰型記憶コアの内部 dynamics に適用** — 記憶/リザーバコアの `decay`/`W` 再帰に対して。
> 制御プラント・分類 head・生成コード/数式ではない。
>
> **(iii) 進化/更新ループ内の prove-then-reject 採用ゲートとして使用** — fail-closed: 証明できない子は *棄却*
> (resample → 既知安全 fallback)。安全集合への *射影* でも、*正則化* でも、性質を構造で成立させる *構造強制* でもない。
>
> **(iv) 動く実装と実験を伴う。**

### 2.1 ゲート対象の記憶コア dynamics

ゲート対象は記憶/リザーバコアの漏れ・飽和再帰 (RWKV 型状態空間更新):

```
s_{t+1} = decay ⊙ s_t + (1 − decay) ⊙ tanh(W s_t + V x_t),    V = I        … (1)
```

進化ゲノム `gene = (decay ∈ [0,1]^n, W ∈ [−2,2]^{n×n})`。状態に関するヤコビは

```
J(t) = diag(decay) + diag((1 − decay) ⊙ t) · W,   t_i = sech²(pre_i) ∈ (0,1]   … (2)
```

到達可能微分箱 `t ∈ [t_min, 1]^n` 上で評価される。ゲートはこの箱上で `ρ(J) < 1` を証明し、Banach 不動点定理に
より一意・有界 (`|s| < 1`) な不動点と、縮小性解析の標準帰結である離散時間増分 (δ-) 安定性 (任意の 2 軌道が指数
収束) を保証する。

### 2.2 健全な縮小性証明器の梯子 (なぜ SMT ソルバが load-bearing でないか)

各段が箱上で `ρ(J) < 1` を含意する 3 つの健全な証明器 (コスト・表現力の昇順):

| 段 | 証明する十分条件 | 手段 | コスト |
|---|---|---|---|
| `cert_inf` | `sup ‖J‖_∞ < 1` (各行 abs-sum の箱上限) | **閉形式**, `O(n²)` | 最安 |
| `cert_two` | 全 `2^n` 頂点で `σ_max(J_v) < 1` | 頂点 SVD 列挙 | `2^n` |
| `cert_sdp` | 共通二次 Lyapunov `P ≻ 0`, 全頂点で `P − J_vᵀ P J_v ≻ 0` | 凸 LMI (内点 SDP, CLARABEL) | `2^n` LMI |

**SMT/SAT ソルバは load-bearing 経路に存在しない。** `cert_inf` は各行の abs-sum が `t_i` について V 字である
ことを利用し、箱上限が端点で達成され、箱量化子が行ごとの 1 次元評価に縮約される — ソルバ不要の健全ゲートである。
これが問題の性質であって機会損失でないことを確認した: 専用の Z3 (SMT) 縮小性トラックが、閉形式 ∞-ノルム証明器と
**バイト単位で一致する証明を生成した — 3270 件中 0 件の不一致、境界近傍ストレスでも 8000 件中 0 件** — すなわち
この縮小性不変量クラスでは SMT ソルバは *装飾* である。(ゆえに誤解を招く「Z3-gated」看板を避け、ゲートを実体どおり
「健全な縮小性証明器の梯子」と記す。これは SMT 定式化が招くソルバ依存と不完全性を回避する。) `cert_inf` は *保守的*
であり (真の `ρ < 1` 縮小の一部を過剰棄却、∞-ノルム − ρ ギャップ中央値 ≈ 0.477)、これこそ非閉形式 (回転的/非正規)
縮小のために SDP-Lyapunov 段が存在する理由である。

**SDP 段の fail-closed 設計.** 真の LMI solve は CLARABEL ソルバ下でのみ走る。不在時、`cert_sdp` は feasibility
境界で false-negative を出すソルバへ黙って fallback するのでなく *拒否* する (`False` を返す)。ソルバの返す `P` は
固有値テストで独立に再検査される — 証明器は決してソルバ盲信でない。挙動保存の高速経路が、ソルバ呼出前に
`ρ(J_v) ≥ 1` の頂点 (LMI feasibility の必要条件) を棄却する。

### 2.3 prove-then-reject 採用ゲート (fail-closed, resample cap, known-safe fallback)

開示するゲートは進化/更新ループ内で次のように動作する:

```
子 gene g' を提案                                       # 変異 / 交叉 / 勾配ステップ
if certifier.certifies(g'):        g' を採用            # 健全な縮小性証明が通過
else:
    for k in 1..resample_cap:                          # 上限付き resample
        g' ← 再 resample/mutate
        if certifier.certifies(g'): g' を採用; break
    else:
        known_safe_fallback を採用                      # fail-closed: 未証明の子は決して採用しない
```

2 つのゲートモードを開示する: `gate_mode = "contraction"` (縮小性証明が通れば採用) と `gate_mode = "state_norm"`
(有界状態条件が通れば採用)。既定 `"none"` は無制約ループをバイト単位で再現するので、ゲートは既存進化基盤への純粋に
additive な被せ物である。§7 の近接先行に対する識別的意味は **prove-then-reject** である: 未証明の更新は *棄却*
される (提案更新を改変する射影/clamp でなく、性質を架空に常成立させて表現力を犠牲にする構造制約でもない)。これは
戦略原理「先ず勝ちて而る後に戦う」(孫子・軍形篇) の縮小性理論版である: 集団は既に勝てる態勢にあると証明された
メンバーのみを採用する。

## 3. tracking tube 検査指標 (ゲート出力の追加証明ゼロ再利用)

「コアはどこかへ縮む」の先に、実務では「コアが望ましい *参照軌道* に追従する」を見たい。我々は、**ゲート自身の量
を再利用** して閉形式の追従保証を得る方法を、新規証明なしで開示する。

写像 (1) を `F(s, x)`、参照入力 `x_ref` を共有する 2 軌道:
- 参照: `s_ref[t+1] = F(s_ref[t], x_ref[t])` (外乱なし、かつ *feasible* な参照 = 系の真の解)、
- 実: `s_act[t+1] = F(s_act[t], x_ref[t] + d[t])`、有界入力外乱 `‖d[t]‖_∞ ≤ w̄`。

`L = sup ‖∂F/∂s‖_∞` (`cert_inf` が縮小性の証拠に使う **まさにその量**)、`G = sup ‖∂F/∂x‖_∞` (入力ゲイン,
`G = max_i (1 − decay_i) Σ_j |V_ij|`)。三角不等式 + 平均値定理より、`e[t] = s_act[t] − s_ref[t]` について:

```
‖e[t+1]‖_∞ ≤ L ‖e[t]‖_∞ + G w̄                                              … (3)
```

`L < 1` (縮小性ゲート出力) なら幾何級数が収束し、`e[0]=0` から

```
limsup_t ‖e[t]‖_∞ ≤ r := G · w̄ / (1 − L)                                    … (4)
```

**`r` が開示する tube 半径。** `L`, `G`, `w̄` の 3 つすべてが、縮小性ゲートが既に行う同じ箱列挙から出る — tube は
*追加証明コストゼロ* で報告され、fail-closed 規律を継承する (`L ≥ 1` ⇒ tube `= ∞` = 保証なし)。開示するレポータは
**read-only** 関数 `tracking_tube(gene, x_ref, w̄) → {L, G, tube_radius, feasibility_residual}` で、採用 API を
変えない。初版は `cert_inf` PASS gene に限定 (`L = sup‖J_s‖_∞ < 1` が直接成立)。`cert_two/sdp` のみの回転的縮小
では `cert_sdp` の返す `P`-重みノルム下で同じ導出が `cond(P)` 倍のルーズさで走る。

**経験的裏付け (小規模).** 縮小性 PASS の 3 gene で、実測の追従誤差/外乱比 (0.50 / 0.78 / 1.04) は理論ゲイン
`G/(1−L)` (1.76 / 2.29 / 2.00) の内側にあった。非縮小性の対照 gene ではゲートが棄却し (`L = 1.68 ≥ 1`,
tube `= ∞`)、実測誤差は外乱の **9.3 倍** に増幅した — すなわちゲートは追従保証に load-bearing であって飾りでない。

**何が証明され何が証明されないか (honest).** tube 不等式 (3)–(4) は *定理* (Banach + Lipschitz 合成)。証明され
**ない** もの: (a) 参照軌道の *妥当性* — それが「良い」記憶/タスク軌道かはタスク fitness の責任であり、制御理論で
参照が所与であるのと同様、検証器の射程外。(b) *feasibility* (参照が系の真の解であること) は逆問題一般では数値同定
(残差 `ρ_feas`) であって証明ではない。

## 4. 検証付き記憶進化 — 開示する 2 ルート

四点交差点に属する 2 つの応用ルートを開示し、各々を最近接先行と明示的に区別する。

**ルート (a) — エージェント記憶バンク更新のゲート.** エージェント外部記憶バンクへの各候補書込み/更新は、記憶
dynamics の健全な縮小性/安定性証明を通った場合のみ採用する (fail-closed)。本ルートは *governing-evolving-memory*
の枠組みを NLI 理論型記憶ガバナンス (SSGM, §7) と共有するが、それらが残す 2 隅で異なる: 採用基準が **健全な形式
証明** (NLI 矛盾検出でない) であり、**実験を伴う動くゲート** (理論アーキ/証明スケッチでない) である。この理論
専用アーキが残す「実装 + 健全証明」の窓を後続実装が押さえる前に、本日付開示が閉じる。

**ルート (b) — 記憶コア内部状態 dynamics のゲート.** 記憶コア自身の再帰パラメータ ((1) の `decay`, `W`) への各
候補更新は、縮小性証明器が到達可能箱上で `ρ(J) < 1` を証明した場合のみ採用する (fail-closed)。本書で reduced to
practice したのがこのルート (§5)。by-construction な縮小性/Lipschitz コア (Enforced-Lipschitz Transformers,
R2DN, §7) とは、性質を無料で成立させる構造制約でなく、*任意の提案更新* を証明でゲートし失敗を棄却する点で異なる —
設計軸は **prove-then-reject 対 by-construction** であり、ゲートは表現力を構造で犠牲にしない代わりに *navigability
コスト* を払う、という honest なトレードオフを伴う。

## 5. Reduction to practice (実施可能詳細)

§2–§4 の機構は FullSense `llcore` パッケージで実施済 (記録日 = 本 commit):

- 証明ゲートは **出荷側の進化経路に本配線済** — 出荷 `evolve()` が additive な `gate_mode`
  (`"contraction"` / `"state_norm"`) と `resample_cap` を持つ。`gate_mode="none"` ではループは従前の無制約挙動と
  バイト一致し、ゲート付きモードは research 側の gated-evolution 参照と全モードで一致することをテストで実証。採用は
  fail-closed: 上限まで resample → 既知安全 fallback に置換。**未証明の子は決して採用されない。**
- 証明器の梯子 (`cert_inf` 閉形式 ∞-ノルム, `cert_two` 頂点 SVD, `cert_sdp` CLARABEL SDP-Lyapunov) が load-bearing
  ゲート。SMT トラックは *装飾的等価* 確認 (3270 件 0 件不一致) としてのみ存在。
- **tracking tube レポータ** (`r = G·w̄/(1−L)`, `cert_inf` 限定) は additive な read-only レポータとして実装
  (状態 Lipschitz / 入力ゲイン helper 付き)。既存採用 API は不変、golden テスト値は PoC ケースに一致。
- ゲートとレポータを覆うテストは記録日時点で 294 件。
- **観測ゲートコスト: 実測で約 20–60 倍** のオーバーヘッド (証明コストは実在し、隠さず開示)。

## 6. 合成: SPC runtime ゲートと二層倫理ゲート

開示するゲートは、ここで同じく公有に置く 2 つの構成物と合成される:

**SPC 管理図 runtime ゲート.** 進化ループのメトリクス (drift, diversity, fitness モーメント) を統計的工程管理
管理図 (X̄–R / CUSUM, llmesh エンジンと同様) に入れ、out-of-control 信号が進化ループへの *runtime* ゲートとして
働き、毎更新の縮小性証明を統計的・オンラインな分布外ガードで補完する。縮小性証明は *各更新の解析的性質* を、SPC
管理図は *ループの時間的集約挙動* をゲートする。両者は直交し合成可能。

**二層倫理ゲート (探索は自由 / 採用は検証).** 変異 (mutation, novelty search, antifragile mutation, 「欺瞞的」な
探索手) はあえて *無制約* — 探索は自由。採用 (生きた集団への選択) は *検証* — fail-closed 証明ゲートと承認経路を
通らねばならず、迂回不可。これは二層の倫理を分離する: 探索層は冒険的でよい (孫子の 詭道、探索に厳密に限定) が、
採用層は誠実でゲートされる (論語の 仁: 「知るを知るとし知らざるを知らずとする」)。進化集合の外にあって到達不能な
制約は最適化で消せない。現代の安全層の多くは単層 (出力フィルタ) であり、二層分離はモデル規模と独立な設計判断である。

## 7. 先行技術との境界 (隅ごと)

各隅の最近接先行を命名する。以下の arXiv ID はすべて掲載前に abstract と照合確認済。主張は *交差点* であり、各行は
先行がどの隅を埋めないかを記す。

- **SSGM — Governing Evolving Memory in LLM Agents (arXiv:2603.11768, 2026):** 隅 (ii) に最近接。保護コア事実に
  矛盾する記憶更新を棄却する write-validation ゲートを提案 — だがゲートは NLI 矛盾検出 (健全な形式証明でない)、
  安定性定理は `O(N·ε)` drift bound を証明スケッチで述べたもの、実装なしの理論アーキと明言 — 隅 (i)(iv) が空白。
  **governing-evolving-memory の看板を担い、そう引用されるべき。残す窓 = sound 証明 + 実装の隙間を本開示が占有する。**
- **SEVerA — Verified Synthesis of Self-Evolving Agents (arXiv:2603.25111, 2026):** 各モデル呼出を Dafny/SMT 検証
  rejection sampler で包み一次 *出力契約* を証明 — 出力契約への by-construction 保証であり、進化する記憶コアの縮小性
  への毎更新 prove-then-reject ゲートでない。
- **PSV — Propose, Solve, Verify (PSV-Verus, arXiv:2512.18160, 2025):** self-play ループ内の健全 SMT 検証器が
  検証済解のみ採用 — だが検証対象は *生成解のコード正しさ* であって進化する重み/記憶の縮小性でない (隅 i–ii 空白)。
- **Provably Safe Model Updates / LID (arXiv:2512.01899, 2026):** 各基盤モデル更新を抽象解釈で `δ`-safe と認証し
  *project-then-accept* clamp — 射影であって prove-then-reject でなく、性質は精度保存 bound (縮小性でない)、対象は
  frozen-embedding 分類 head (記憶コアでない)。
- **Synthesis of Parametric Programs using GP and Model Checking (Katz & Peled, arXiv:1402.6785, 2014):** *パターン*
  (進化ループ内の健全モデル検査ゲート、失敗で棄却) は LLM 以前から確立。検証対象は古典並行プログラムで記憶コアでない。
  ゲート *パターン* の新規性は **主張しない**、Transformer 記憶コアの縮小性への適用のみ。
- **Enforced-Lipschitz Transformers (arXiv:2507.13338, 2025) / R2DN (arXiv:2504.01250, 2025):** 縮小性/Lipschitz を
  *by-construction* で強制 (スペクトル soft-cap 射影 / 再帰パラメータ化) — 最強の「構造で組み込めばゲート不要」対抗設計。
  **by-construction 強制 対 prove-then-reject** を設計軸として対比: 構造制約は表現力を保証と引換えに犠牲にし、棄却
  ゲートはその構造制約なしに任意更新を検査する。
- **Safeguarded AI (ARIA programme, 2024–2026):** 最も権威ある proof-gated-gatekeeper 概念だが、gatekeeper は形式
  世界モデルに照らし *行動/計画* を世界到達前に認証 — 出力/行動ゲートであって重み/記憶更新ゲートでなく、programme 段階。
- **Emergent Formal Verification / substrate-guard (arXiv:2603.21149, 2026):** AI *出力* を健全に検証する *動く* Z3
  システム — 出力の post-hoc 観測監視であって進化する記憶コアへの毎更新ゲートでない。

*(特許面の境界.* Google Patents / USPTO に対する英語 14 + 日本語 3 の専用照会で、四点交差点を占有する特許は **ゼロ**
件。最近接特許 — `US11715005B2` (ハッシュ照合 NN 真正性検証)、`US10896032` (certify-then-deploy ガバナンスゲート)、
`US11868855` (resiliency/可用性の意味でのモデル/重み「stability」検証) — は *語彙* が被るが、ゲート対象 (重み/記憶
更新)・健全性根拠 (解析的縮小性証明であってハッシュ/attestation/運用テストでない)・対象 (Transformer 記憶コア)・
ループ位置のいずれも一致しない。「健全証明が更新/記憶/進化をゲートする」と表現したクエリは、特許 DB に site 指定
しても結果がほぼ全て学術 (arXiv) に逸れた — 概念が学術段階に留まり特許化されていない間接証拠である。)*

## 8. honest 限界 (隠さず開示)

- **実証規模は小さい。** reduced-to-practice の核は `n = 8` (72 実数 gene)・16 KB コーパス・byte vocab。
  「Transformer/LLM 記憶コア」は **機構実証** の意味であり、フロンティア規模の能力主張ではない。
- **検証器の payoff は *navigability* であって学習でない (L3).** 証明器の便益は進化過程の探索空間 *navigability*
  (どの dynamics が到達可能か) であって学習改善そのものでない。効果は EA 固有で、勾配法では (最終交差エントロピーで) 消える。
- **ゲートは無料でない: 実測 ~20–60 倍** のオーバーヘッド。短い訓練では「ほぼタダ」に見えるが、十分訓練すると顕在化し、
  ここで開示する。
- **「観測された false admit ゼロ」は経験的であって機械検査でない。** 我々の走行で false admission は観測されなかったが、
  これは *観測* であって、実装の機械検査された大域健全性保証 **ではない**。証明器の *条件* は健全 (`ρ(J)<1` の証明済
  十分条件) だが、それを担う *実装* は通常のソフトウェアであり end-to-end に形式検証されていない。
- **`cert_inf` は保守的** (真の `ρ<1` の一部を過剰棄却)。健全な tube は初版で `cert_inf` PASS gene に限定、回転的縮小は
  `cond(P)` 倍ルーズな `P`-norm tube を要する。
- **参照軌道の妥当性と feasibility は証明外** (§3): tube は *与えられた参照* への追従を保証する。その参照が望ましいか、
  系の真の解かは認証されない。
- **「未発見」の範囲.** 「四隅同時占有の先行なし」は我々の敵対的監査と表層特許検索 (Web 経由 Google Patents / USPTO、
  Derwent/PatBase/J-PlatPat の全クレームインデックスでない。中国語ネイティブ CNIPA 検索未実施。特許は公開まで最長 18 ヶ月
  ラグ) に限られる。「我々の探索範囲で」の留保を常に維持する。網羅的不在は証明不可能。

## 9. 再現性と来歴

証明器の梯子・証明ゲート付き `evolve()`・tracking tube レポータは FullSense `llcore` パッケージに存在する。敵対的
差別化監査・特許 DB 照会・四点交差点の related work 位置付けは FullSense 公開リポジトリの `docs/research/` と `llcore`
論文ドラフトに存在する。本書の git commit タイムスタンプが上記 priority 主張の記録日である。

---

### 変更履歴

- **2026-06-06** — v1, 記録日。四点交差点 (健全な縮小性証明器の梯子 × Transformer/再帰型記憶コア内部 dynamics ×
  prove-then-reject 進化ループゲート × 動く実装) と tracking tube 検査指標の先行技術を確立する防御的開示。証明ゲートは
  出荷 `evolve()` に本配線済 (fail-closed, resample cap, known-safe fallback; 294 テスト)。zh/ko 訳と将来の特許判断は
  本日付記録の範囲外。
