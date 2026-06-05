# English

# llcore Verification Arc (#36) — Breaking the 2ⁿ Wall: Vertex-Free Soundness Proofs and "Turning Cost into Evolutionary Selection Pressure"

![Verifier cost: vertex-free vs 2ⁿ enumeration](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_cost.svg)

> **Concept hook**
> The "is-it-broken inspector" for an evolving AI is both a guardian of safety and a **monster of computational cost**. A rigorous soundness proof (2-norm / SDP) enumerates **2ⁿ vertices** with respect to the state dimension n. That is 256 at n=8, 65,536 at n=16, and 4.3 billion at n=32 — long before reaching dimensions on the scale of an insect's DNA, the inspector itself collapses first. This article covers (1) the measured result of breaking this 2ⁿ wall with a **sound approximation that does not enumerate vertices** (a single SVD, up to 12,520× faster, zero soundness violations), (2) the process of running the PoC one stage at a time and correcting "the cheapest naive bound is too loose → an absolute-value-dominated bound recovers 78%," (3) a vision of "**turning cost itself into evolutionary selection pressure**," modeled on the reductive evolution of living things, and (4) an honest disclosure — the L3 result that a verifier "unlocks" perplexity is **evolvability, not language learning** (the control experiment does not tie).

## 0. Glossary

| Term | Plain meaning |
|---|---|
| llcore | FullSense's research substrate. It evolves the "dynamics" (the way it moves) of small neural systems. CPU-only, on-prem, $0. |
| contraction | The property that state differences shrink as time advances. With it, the system stays stable and does not run away = homeostasis of the system. |
| verifier (inspector) | The gate that judges "does this individual really contract." From weakest to strongest, arranged like a ladder (∞-norm → 2-norm → SDP → …). |
| Jacobian J | A matrix expressing "how a tiny deviation gets amplified" at each time step. If σ_max(J)<1, it contracts in the 2-norm sense. |
| t-box | The range that the tanh slope t can take (each coordinate in [t_min, 1]). J is an interval matrix moving over this box. |
| vertex enumeration (2ⁿ) | The exact method that checks σ_max at all 2ⁿ corners of the t-box. As n grows it explodes exponentially. |
| vertex-free | An approximation that produces an upper bound over the whole box with 1–2 matrix operations, without enumerating vertices. Cheap. |
| sound | "If it is judged to contract, it really does contract." It produces no false positives (no missed diverging individuals). |
| conservative | Rejecting too much — saying "no" even when something actually contracts. Sound, but it leaves real cases behind. |
| B2 = σ(\|M\|+R) | A sound upper bound built from the midpoint M and radius R of an interval matrix. A single SVD. The protagonist of this article. |
| reductive evolution | The evolution by which organisms discard unnecessary genes and organs and become simpler. Cost reduction itself is the selection pressure. |
| canalization | The phenomenon that the more evolution advances, the more developmental pathways become fixed and resistant to change (Waddington). |

## 1. Plain-language conclusion

An evolving AI needs an "is-it-broken inspector." We measured this as a ladder in #35. The theme this time is the **price tag** of that inspector.

The strongest sound inspector (2-norm / SDP) checks **all 2ⁿ corners of the box** with respect to the state dimension n. At n=8 that is just 256 corners, but at n=16 it is 65,536, and at n=32 it is 4.3 billion — the inspector breaks down before reaching the dimensions of a realistic language model. In other words, what was setting the "ceiling on evolution" was not the order of the Lyapunov function nor the number of genes, but the fact that **the inspector is exponentially heavy with respect to the state dimension**.

So we tried an approximation that "stops looking at every corner and instead estimates the whole box at once." The first naive version (B1, split by the triangle inequality) was **too loose**: it picked up only 29.5% of the contracting individuals, and was even more conservative than the cheapest ∞-norm — for a moment we concluded pessimistically that "cheap vertex-free is no good; we need the real SDP."

But the version that changed how the bound is constructed (B2, dominated by absolute values) flipped everything around. **With a single SVD, it recovered 77.6% of the individuals that exact 2ⁿ enumeration admits.** Soundness violations were zero (no false positives). Combined with the ∞-norm it reaches 87%. The speed at n=16 was **12,520×**. The 2ⁿ wall was broken, at least in the practical range.

And then one more step in the idea. Living things discard the unnecessary and become simpler (cave fish discard their eyes, parasites discard their genes). **If we make cheapness of cost itself an evolutionary selection pressure, perhaps the AI too will steer on its own toward "simple structures that are cheap to verify."** But there is a trap — "cheap" comes in good cheapness (structurally simple) and bad cheapness (the inspector is so conservative that nothing is learned: degeneration), and in llcore's L3 the latter (degeneration into a unigram) was actually observed. So instead of simple scalarization, it must be handled as a Pareto trade-off between performance and cost.

Finally, an honest disclosure. The L3 headline "a stronger inspector unlocks perplexity" turns out, when you doubt the breakdown, to be **evolvability (ease of evolving), not language learning**. Even in a control experiment that shuffled the strings, the difference between inspectors does not vanish (it actually remains at ~107% on the CE metric), so the effect was an optimization phenomenon that barely depends on linguistic structure. This article discloses even that breakdown.

## 2. Why 2ⁿ — the reason the inspector is exponentially heavy

The target of evolution in llcore is the gene `(decay, W)`, whose dimension is `n + n²` (72 at n=8). But **the rate-limiting factor of runtime is not this gene size**. It lies where the sound inspector verifies that the largest singular value of the Jacobian `J(t) = diag(decay) + diag((1−decay)⊙t)·W` is below 1 at **all 2ⁿ corners of the t-box**.

| n | gene dim n+n² | 2ⁿ vertices | cert_two measured (sec/individual) |
|---|---|---|---|
| 8 | 72 | 256 | 0.0064 |
| 12 | 156 | 4,096 | 0.082 |
| 16 | 272 | 65,536 | 2.76 |
| 32 | 1,056 | 4.3 billion | infeasible |

The easy-to-misunderstand point here is that **2ⁿ scales with the state dimension n, not with the element count n² of the weight matrix**. So "lowering n² by making W low-rank" alone does not make the inspector faster. The closed-form ∞-norm (cert_inf) is light at O(n²), but as we saw in #35 it is over-conservative and lures evolution into a trap. The crux was the trade-off that "**the inspector that scales is weak, and the strong inspector does not scale**."

## 3. The PoC one stage at a time — correcting "the cheapest is too loose" into "absolute-value dominance gives 78%"

As a strategy to lower the inspector's cost, we tried "vertex-free": producing an upper bound over the **whole box** with 1–2 matrix operations, without enumerating the corners of the t-box. Since J is affine in t, the t-box can be represented as an interval matrix = midpoint M and radius R.

**PoC-1 (naive triangle split B1 = σ(M) + σ(R))**: Sound (by construction, an upper bound) and over 10,000× faster at n=16. But it picked up only **29.5%** of the contracting individuals and was more conservative than the cheapest ∞-norm. The triangle inequality is loose because it worst-cases M and the perturbation separately. → For the moment we reported "cheap vertex-free is no good."

**PoC-2 (absolute-value dominance B2 = σ(\|M\|+R))**: Sound by virtue of the property that `|J| ≤ |M|+R` and "if it is dominated by nonnegative components, σ_max is also monotone." This is what worked.

![Admit coverage by prover](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_coverage.svg)

| Inspector | Cost | admit (out of 3000) | % of exact 2ⁿ (1310) | Soundness violations |
|---|---|---|---|---|
| cert_two (exact 2ⁿ) | O(2ⁿ·n³) | 1310 | 100% (baseline) | — |
| cert_inf (∞-norm) | O(n²) | 1072 | 81.8%※ | 0 |
| B1 = σ(M)+σ(R) | 2 SVDs | 387 | 29.5% | 0 |
| **B2 = σ(\|M\|+R)** | **1 SVD** | **1017** | **77.6%** | **0** |
| cert_inf ∪ B2 | O(n²)+1 SVD | **1142** | **87.2%** | 0 |

※ The ∞-norm is a certificate in a different norm; 75 of the 1072 are non-contracting under the 2-norm (inf ⊄ two).

In other words, **B2 recovers 77.6% of the reach of exact 2ⁿ with a single SVD**, and combined with the ∞-norm it reaches 87%. The pessimism of PoC-1 was just "the naive bound B1 was bad" — vertex-free soundness proofs themselves were not a dead end. This is a good example of the discipline "check cheaply with a PoC before inflating the spec," letting us **confirm in seconds that the cheapest bound was too loose** before proceeding to a heavy SDP implementation.

The remaining ~22% (the individuals B2 misses, which only exact 2ⁿ or SDP picks up) — whether they really carry the "good dynamics" — is currently being measured, and this becomes a go/no-go: if they do not carry it, B2 is enough and a real robust-LMI (SDP) is unnecessary. **Decide after measuring** (do not start building the SDP on the assumption that they carry it) is the discipline of honest disclosure.

## 4. Turning cost into "evolutionary selection pressure" — modeled on the reductive evolution of living things

From here on it is a vision (implementation is user-gated). The current fitness is performance (perplexity) alone. If we add a **structural cost** term (rank, sparsity, effective dimension) here and make it multi-objective, perhaps evolution will steer on its own toward "simple structures that are cheap to verify."

Living things do exactly this. Prochlorococcus and SAR11 are free-living bacteria with minimal genomes ("the ones that trimmed" win on replication speed and nutrient economy), parasites (Buchnera, Mycoplasma) discard genes, and cave fish lose their eyes. **If the benefit of a complex function < the cost of maintaining it, the simpler one survives.** TRIZ too holds the "increase of ideality (= function / cost)" as the central law of technical-system evolution.

But **llcore's own results give a warning — there are two kinds of cheapness**:

- ✅ **Good cheapness = structural simplicity** (low-rank / sparse): truly cheap to verify, and also easy for evolution to move through (navigable).
- ❌ **Bad cheapness ① = the inspector's conservatism**: the ∞-norm is the cheapest, but it dropped evolution into a unigram (context-free) trap. If you naively reward "cheap to verify = good," you push evolution into the ∞ trap.
- ❌ **Bad cheapness ② = degenerate behavior**: the collapse into a unigram observed in L3 is itself an example of "a structure too simple — safe and cheap but incompetent — surviving." It is exactly an obligate parasite that trimmed away so much it can no longer live freely.

So the correct design is not the "cheap = good" scalarization, but a **Pareto trade-off between performance and structural cost**, where the cost term aims at structural simplicity, not at the inspector's conservatism. And because llcore has a **soundness oracle**, it can **discriminate** between "good simplicity (low-rank yet exceeding the unigram)" and "degenerate simplicity (collapsed into a unigram)" — a feat ordinary evolutionary systems cannot pull off. This is the FullSense worldview itself: "evolve not merely to be adaptive, but in a direction where one can **prove it is cheap and safe**."

And "do the PoC before the spec inflates" is the meta-version of the same principle. **A system that has evolved too far becomes resistant to change** (canalization). Before the research narrative and spec harden too much, confirm the skeleton with a small experiment — that is applying the system's own navigability lesson to the development process.

## 5. Honest disclosure — L3 is evolvability, not learning

Finally, let me disclose the claim I cut the most today. The L3 headline (the experiment putting the verification arc on a real byte-LM) was originally "a stronger sound inspector unlocks the perplexity of a real LM." That the sound relaxation beats the ∞ gate over 10 seeds (p=0.000977) is real. But when you doubt the breakdown:

![L3 honest disclosure: the gate-gap does not vanish even in the control](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_l3gap.svg)

- **Same-corpus landscape**: the ∞ region **contains** genes that are 0.118 nats better than the unigram, yet ∞-gate evolution cannot reach there and stays stuck at the unigram. → The trap is not a regional ceiling but a problem of **navigability (ease of evolving)**. Moreover, at 8192B the ceilings of the three regions are nearly equal, and the "∞ has the worst ceiling" ladder at 12288B is not corpus-robust.
- **Control experiment (string shuffle)**: we predicted in advance that "if context is meaningless, the inspector difference vanishes," yet **the ordering does not vanish**. On the fitness metric ~84% remains, and on the natural CE (nats) metric it actually remains at **~107%**. The real−null residual is non-significant. → The gate-gap is an optimization phenomenon that barely depends on linguistic structure.
- **The only structure-dependent signal** = unigram-crossing (the sound gate exceeds context-free on real, but does not exceed it on null).
- **Gradient avoids the trap** (separate experiment BG10): gradient learning reaches the same CE for all gates, with the inspector penalty ~zero. → For gradient-trained LMs, the inspector can be chosen by soundness/coverage, and navigability is moot.

Conclusion: the verified evolution core **works** as a real byte-LM (L0/L1/L2 hold), but the L3 "payoff" is **evolvability, not language learning**. This is not a defeat but the correct description that results from doubting the breakdown (the discipline of [feedback_benchmark_honest_disclosure]).

> **Honest-disclosure box**
> | Claim | Strength | Limitation |
> |---|---|---|
> | B2 recovers 77.6% of exact 2ⁿ with 1 SVD, 0 soundness violations | measured (n=8, 3000 individuals) | whether the remaining 22% tail carries navigable dynamics is being measured |
> | inf∪B2 gives 87.2%, up to 12,520× faster | measured (n=8/12/16) | n=8 reservoir LM, not a true Transformer |
> | sound relaxation beats the ∞ gate (10/10, p=0.000977) | measured | evolvability, not learning |
> | the inspector difference does not vanish even in the control (~107% on CE) | measured (10 seed null) | hence structure-independent = not evidence of language learning |
> | turning cost into selection pressure | vision, user-gated | cheapness comes in two kinds, must be handled as a Pareto trade-off |

## 6. Summary

- An evolving AI's inspector **explodes as 2ⁿ** with respect to the state dimension n. This was the true identity of the "ceiling on evolution."
- The **vertex-free sound bound B2 = σ(\|M\|+R)** recovers 77.6% of the reach of exact 2ⁿ with a single SVD, up to 12,520× faster, with zero false positives. Combined with the ∞-norm, 87%. The wall is broken in the practical range.
- "**Turning cost into evolutionary selection pressure**" = a vision modeled on the reductive evolution of living things. The key, however, is to discriminate good cheapness (structural simplicity) from bad cheapness (conservatism / degeneration) with the soundness oracle.
- Honest disclosure: the L3 verifier payoff is **evolvability, not language learning** (the control does not tie).

(This article is part of the llcore research arc. The preceding installment = #35: the ladder of verifiers, SDP not SMT, the solver-swap honest disclosure.)
