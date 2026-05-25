# Evolution Research — Stream C: Genome Representation & Selection Schemes

> **Stream**: C (REPRESENTATION & SELECTION) of the llive open-ended cultural-evolution
> requirements sweep (2026-05-25). Parent design: [[OPEN_ENDED_CULTURAL_EVOLUTION]]
> (`docs/vision/OPEN_ENDED_CULTURAL_EVOLUTION.md`).
> **Mandate**: exhaustive literature + RAD corpus sweep on (a) genotype-phenotype maps /
> neutrality / degeneracy, (b) indirect/generative encodings, (c) sparse/structured
> mutation, (d) fitness normalization, (e) selection schemes — then convert to
> **falsifiable requirements** for OUR system.
> **Honest disclosure**: all current llive fitness is **proxy** (deterministic, no LLM
> call). Real-LLM evaluation is the final stage (ollama, GO pending). Items flagged
> **[SPEC]** below are speculative / unverified by us. Codebase line refs are from a
> 2026-05-25 read of `D:/projects/llive/src/llive/perf/evolutionary/`.

---

## 0. Load-bearing finding from the existing code (read first)

The user's principle #4/#10 has a **concrete failure already latent in the code**:

- `LatentReservoirChromosome` (256 genes, sparse mutation `density=0.05`) exists and is
  well-designed (`latent_reservoir.py`).
- **BUT** `Genome3D` (`genome_3d.py:69`) has fields `c_impl / c_prompt / c_meta /
  c_factors` — **there is no `c_latent` field**. The reservoir is not part of the genome
  aggregate.
- The descriptor function every diversity/novelty mechanism reads,
  `genome_flat_vector()` (`genome_3d.py:254`), returns **only `c_factors.as_flat()`**
  (the 40-dim factor matrix). It never touches the reservoir.
- `NoveltyScorer` (`diversity.py:93`), `DiversityMonitor` (`diversity.py:284`), and the
  breed filter (`diversity.py:162`) all consume `genome_flat_vector`.

**Therefore the neutral reservoir, as wired today, is pure bloat: it mutates but is read
by no descriptor and no objective — the exact "just bloat / neutral drift" failure mode
(principle #10, OPEN_ENDED §1).** Fixing this wiring is requirement R-NEUT-1 below and is
the single highest-leverage change for Stream C. This is fact (code read), not speculation.

---

## 1. Techniques table

| # | Technique | One line | Citation / URL | Maturity |
|---|-----------|----------|----------------|----------|
| T1 | **Degeneracy ≠ redundancy** | Partial functional overlap of *different* parts; only degeneracy (not pure redundancy) yields high evolvability | Whitacre & Bender (2010), *J. Theor. Biol.* — [arxiv 0910.2586](https://arxiv.org/abs/0910.2586) | Established (cited design principle) |
| T2 | **Neutral networks** | Connected sets of genotypes with same phenotype; large neutral nets ⇒ both robust *and* evolvable (paradox resolved) | Schuster/Fontana (RNA); Wagner (2008); [Greenbury et al. 2022, Nat.Eco.Evo.](https://www.nature.com/articles/s41559-022-01867-z) | Established |
| T3 | **Neutral drift / cryptic variation** | Mutations accumulate on a neutral net, unlocking new adaptive phenotypes later (exaptation) | Kimura (1968); [adaptive walks need neutral intermediates](https://www.sciencedirect.com/science/article/abs/pii/S0040580910000924) | Established |
| T4 | **NEAT complexification** | Start minimal, grow topology via mutation; historical markings + speciation protect innovation | Stanley & Miikkulainen (2002) | Mature (widely used) |
| T5 | **CPPN / HyperNEAT** | Indirect/generative encoding: a small genome *generates* a large regular phenotype (symmetry, repetition) | [HyperNEAT (Stanley et al.)](https://en.wikipedia.org/wiki/HyperNEAT) | Mature |
| T6 | **Evo-devo / cis-regulatory locus** | Adaptive change concentrates in small *regulatory* loci; small genetic Δ → large phenotypic effect; modular = low pleiotropy | [Hoekstra & Coyne (2007)](http://bejerano.stanford.edu/readings/dave/HoekstraCoyne_aBitLong.pdf); cis-reg review 2024 | Established (biology) |
| T7 | **Novelty search + archive** | Reward behavioral sparseness vs population+archive; abandon the objective | [Lehman & Stanley (2011)](https://www.cs.swarthmore.edu/~meeden/DevelopmentalRobotics/lehman_ecj11.pdf) | Mature |
| T8 | **MAP-Elites (QD)** | Illuminate a descriptor grid; keep one elite per cell ⇒ a *map* of diverse high performers | [Mouret & Clune (2015), arXiv:1504.04909](https://arxiv.org/abs/1504.04909) | Mature |
| T9 | **Rank-based fitness / fitness scaling** | Select on rank, not raw value ⇒ outlier-robust, bounded, constant pressure | [Selection (EA), Wikipedia](https://en.wikipedia.org/wiki/Selection_(evolutionary_algorithm)); MATLAB GADS scaling | Mature |
| T10 | **z-score standardization** | Per-descriptor (x−μ)/σ removes absolute magnitude, keeps relative structure | Standard; principle #1 of OPEN_ENDED | Mature |
| T11 | **Tournament selection** | Sample k, take best; pressure tuned by k; favors generalists | Goldberg/Deb (1991) | Mature |
| T12 | **Lexicase selection** | Per selection: shuffle cases, filter to best-on-each in turn ⇒ rewards specialists, huge behavioral diversity | [Helmuth & La Cava (2021)](https://cavalab.org/assets/papers/Helmuth%20and%20La%20Cava%20-%202021%20-%20Lexicase%20Selection.pdf) | Mature |
| T13 | **ε-lexicase** | Lexicase for continuous errors; "best ± ε" pass-band; analysed for *many*-objective | [La Cava et al. (2019), Evol.Comput.](https://pmc.ncbi.nlm.nih.gov/articles/PMC9453780/); [La Cava & Moore (2018)](http://cavalab.org/assets/papers/La%20Cava%20and%20Moore%20-%202018%20-%20An%20analysis%20of%20%CF%B5-lexicase%20selection%20for%20large-scal.pdf) | Mature |
| T14 | **Fitness sharing / niching** | Derate fitness by # neighbors inside a sharing radius σ_share ⇒ stable sub-populations | [Goldberg & Richardson (1987)](https://sci2s.ugr.es/sites/default/files/files/Teaching/OtherPostGraduateCourses/Metaheuristicas/IEEETEC-1998-V2-97-106-Sareni-Fitnes-sharing-niching-methods.pdf) | Mature (σ_share tuning fragile) |
| T15 | **NSGA-II / crowding** | Non-dominated sort + crowding distance; elitist Pareto MOO (≤3 obj) | [Deb et al. (2002)] (impl: `nsga2.py`) | Mature |
| T16 | **NSGA-III** | Reference-point–guided MOO for many objectives | [Deb & Jain (2014)] | Mature (struggles on irregular fronts) |
| T17 | **FUSS** (Fitness Uniform Selection) | Sample a fitness *value* uniformly, pick nearest individual ⇒ pressure toward *sparse* fitness regions | [Hutter & Legg (2006), arXiv:cs/0610126](https://arxiv.org/abs/cs/0610126) | Niche but proven |
| T18 | **Self-adaptive σ / CMA-ES** | Evolve mutation step-size / covariance; CMA captures inter-locus correlation | Hansen (2016) (impl skeleton: `cma_es.py`, DIV-01) | Mature |

---

## 2. Falsifiable requirements

Letters: **R-STD** standardization, **R-NEUT** neutral reservoir, **R-SPARSE** sparse
differentiation, **R-PEC** peculiarity selection, **R-SEL** selection scheme. Each is
phrased so a test can pass/fail it.

### Standardization / normalization (principle #1)

- **R-STD-1 (MUST)** The novelty/diversity descriptor **MUST** be **z-score standardized
  per dimension across the current population** before any distance is computed:
  `d_i = (x_i − μ_i)/(σ_i + ε)`. *Falsifier*: feed a population where every individual
  has all factors = 1.0; the standardized descriptor MUST collapse to ~0 variance and the
  pairwise distances MUST be ~0 (so "everyone maxed" is *featureless*, not dominant).
- **R-STD-2 (MUST)** Selection **MUST NOT** consume raw scalar magnitude of any descriptor
  as a quality signal in the diversity path. *Falsifier*: scaling one descriptor axis by
  10× MUST NOT change selection outcomes (z-score is scale-invariant; raw L2 is not — the
  current `genome_flat_vector` L2 in `diversity.py:143` **fails** this and must be fixed).
- **R-STD-3 (SHOULD)** Where a scalar quality objective is unavoidable (e.g. real-LLM
  fitness, Stage 6), it **SHOULD** be converted to **rank or z-score** before combining
  with novelty, so no single objective dominates by units alone (T9/T10).

### Neutral reservoir (principles #3, #4, #10)

- **R-NEUT-1 (MUST)** `LatentReservoirChromosome` **MUST** be an actual field of the
  evolved genome (`Genome3D.c_latent`) **and MUST be read by the standardized descriptor**.
  *Falsifier*: with the reservoir present but disconnected (today's state), a mutation that
  changes only reservoir genes MUST currently produce **zero** descriptor change — that test
  passing proves the bloat failure mode; after the fix it MUST produce a non-zero change.
- **R-NEUT-2 (MUST)** The reservoir **MUST NOT** enter the *quality* objective (it stays
  neutral wrt fitness) but **MUST** enter the *novelty/diversity* descriptor. This is the
  degeneracy design (T1): redundant-but-read material, neutral wrt quality, expressed in
  behavior space. *Falsifier*: reservoir genes appear in `objective_fn` inputs ⇒ FAIL.
- **R-NEUT-3 (SHOULD)** A **latent→behavior bridge** SHOULD exist so reservoir genes can
  *occasionally* be co-opted into phenotype (exaptation, T3). Without it the reservoir
  only adds descriptor noise. *Falsifier*: over a long run, no reservoir locus ever
  influences a behavioral/factor output ⇒ the reservoir is still latent-only (acceptable
  for Stage 2, but R-NEUT-3 unmet until the bridge lands). **[SPEC]** the bridge design is
  not yet specified; flag as open.
- **R-NEUT-4 (MUST)** Reservoir size **MUST** be large relative to the meaningful genome
  (degeneracy needs surplus), but its *contribution weight* to the descriptor **MUST** be
  controllable, so it cannot drown the meaningful factors. *Falsifier*: a single weight
  knob `w_latent ∈ [0,1]`; at `w_latent=0` behavior reduces to factor-only descriptor.

### Sparse differentiation (principle #5)

- **R-SPARSE-1 (MUST)** Per-generation mutation **MUST** be **sparse** (only a small
  fraction of loci change). Reservoir already does this (`density=0.05`,
  `latent_reservoir.py:53`). *Falsifier*: count changed loci between parent and child;
  median fraction MUST be ≤ ~5% for the reservoir. Today the **meaningful** chromosomes
  mutate *all* loci every step (`Genome3D.sample_neighborhood` `genome_3d.py:160` perturbs
  every factor) — that **violates** the biological-ratio principle and must change.
- **R-SPARSE-2 (MUST)** The differentiating fraction **MUST** be tunable to approximate the
  biological ratio (human ~0.1% between individuals; code-region ~1–2%). The literal 0.1%
  is impractical at 256 genes; **adopt a structured analogue** (small k loci/gen) and
  document the chosen ratio (T6 evo-devo: small regulatory Δ, large effect). **[SPEC]** the
  *exact* ratio for a 256-gene reservoir is a design choice, not derived from biology.
- **R-SPARSE-3 (SHOULD)** Mutation SHOULD be **modular** (a per-locus mask), so some loci
  are quasi-frozen and differentiation concentrates, mirroring cis-regulatory modularity
  (T6) and respecting existing `FrozenGene` semantics.

### Peculiarity selection (principles #2, #3)

- **R-PEC-1 (MUST)** Fitness for selection **MUST** reward *deviation from the population
  centroid* in standardized descriptor space (novelty), **not** proximity to a center/mean.
  *Falsifier*: place a clone at the population mean; it MUST receive the *lowest* novelty,
  never a bonus (T7).
- **R-PEC-2 (MUST)** The system **MUST NOT** collapse to a single global optimum as its
  deliverable; the artifact **MUST** be a **QD archive / map** of diverse cells
  (MAP-Elites, T8; principle #11). *Falsifier*: end-of-run output is a single "best"
  genome ⇒ FAIL; it must be a populated descriptor map.
- **R-PEC-3 (SHOULD)** A **minimal-criterion** guard SHOULD bound pure peculiarity so the
  search does not reward *degenerate* novelty (e.g. NaN/boundary-saturated genomes that are
  "novel" only because broken). Pure novelty has a known degeneracy failure (see §4).
  *Falsifier*: a boundary-saturated/invalid genome receives a high novelty reward ⇒ FAIL.

### Selection scheme (principles #2, #3, #11; many-objective)

- **R-SEL-1 (MUST)** The primary selector **MUST** preserve behavioral diversity under
  many descriptor dimensions **without** relying on Pareto dominance over >3 objectives
  (dominance fails in many-objective: most solutions become mutually non-dominated —
  curse of dimensionality, NSGA-II/SPEA2 degrade). *Falsifier*: with ≥4 objectives, fraction
  of mutually non-dominated individuals → ~1.0 ⇒ NSGA-II loses pressure ⇒ MUST switch
  selector.
- **R-SEL-2 (MUST)** Selection **MUST** maintain measurable diversity above the
  `DiversityMonitor` alarm thresholds for the bulk of a run (no collapse-by-gen-25 as in
  the Stage-0 diagnostic). *Falsifier*: `diversity_l2` falls below threshold and stays
  there ⇒ FAIL.
- **R-SEL-3 (SHOULD)** Selection SHOULD reward **specialists** (good on a subset of
  descriptor axes) not only generalists — this is the mechanism by which "peculiar" genomes
  survive (lexicase, T12/T13). *Falsifier*: an individual best-on-one-axis-worst-on-rest is
  never selected ⇒ generalist-only pressure ⇒ FAIL.

---

## 3. Mapping requirements → user principles

| Principle (OPEN_ENDED §1) | Mechanism (research) | Requirement(s) |
|---|---|---|
| #1 standardize, "all-maxed ⇒ featureless" | z-score (T10), rank fitness (T9) | R-STD-1/2/3 |
| #2 conservatism/center must not win | novelty not centrality (T7); FUSS pressure to sparse regions (T17) | R-PEC-1, R-SEL-1 |
| #3 peculiarity survives (mutation-driven) | novelty search (T7); lexicase specialists (T12/13) | R-PEC-1, R-SEL-3 |
| #4 surplus "extraneous" genes for exaptation | degeneracy (T1), neutral nets (T2), cryptic variation (T3) | R-NEUT-1/2/3/4 |
| #5 differentiation from a *limited* part of genome | evo-devo / cis-regulatory (T6) | R-SPARSE-1/2/3 |
| #10 add chromosomes *with a consumer* (avoid neutral-drift bloat) | reservoir MUST be read | **R-NEUT-1** (the headline fix) |
| #11 not single optimum but a *map* | MAP-Elites / QD (T8) | R-PEC-2 |

---

## 4. ADOPT vs AVOID (honest)

### ADOPT

- **z-score per-dimension standardization of the descriptor (T10)** — directly implements
  principle #1, cheap, scale-invariant, kills the "all-maxed dominates" pathology. Highest
  confidence.
- **Wire the neutral reservoir into the standardized descriptor (T1/T2/T3)** — the
  reservoir already exists and is the user's explicit principle #4; today it is disconnected
  (§0). Adopting = the single most impactful Stream-C change.
- **Sparse, modular per-locus mutation on *all* chromosomes (T6)** — extend the reservoir's
  `density` model to the meaningful factor chromosome (which currently mutates every locus).
- **MAP-Elites QD archive as the deliverable (T8)** — already in repo
  (`quality_diversity.py MAPElitesGrid`); implements principle #11; reuse, don't reinvent.
- **ε-lexicase as the primary many-objective selector (T13)** — see §5. Adopt with care.

### AVOID (with reasons)

- **AVOID pure novelty search with no quality floor / no minimal criterion.** Documented
  failure modes: archive *cycling* in bounded behavior spaces; k-NN distance loses meaning
  in high-dim; greedy per-generation novelty can *reduce* long-run diversity; and it can
  reward **degenerate "novelty"** (broken/boundary genomes that are different only because
  invalid). Mitigation = R-PEC-3 minimal criterion + bounded archive.
  ([BR-NS](https://arxiv.org/pdf/2104.03936), [geodesics/archive](https://arxiv.org/pdf/2205.03162))
- **AVOID NSGA-II/NSGA-III as the *primary* selector when descriptor objectives exceed ~3.**
  Pareto dominance fails in many-objective (almost everything becomes non-dominated ⇒ no
  pressure); NSGA-III needs reference points and struggles on irregular fronts. Keep
  `nsga2.py` for ≤3 explicit objectives only (e.g. quality vs novelty vs persona-diversity),
  not for the 40-dim factor + 256-dim reservoir descriptor.
- **AVOID classic fitness sharing (T14) as the main engine.** σ_share is notoriously
  fragile to tune and degrades in high dimensions; lexicase achieves niche maintenance
  *without* a radius. Keep sharing only as an optional persona-overlap penalty (already in
  repo as `PersonaOverlapPenalty`).
- **AVOID a large reservoir with NO consumer (the bloat trap, principle #10).** This is not
  hypothetical — it is the *current* state (§0). Adding more neutral dims without a
  descriptor/exaptation consumer just slows the run and adds k-NN noise.
- **AVOID raw-L2 distance over un-normalized descriptors** (current `diversity.py:143`):
  large-magnitude axes dominate, defeating principle #1.

---

## 5. Concrete recommendation for OUR system

**Selection scheme: ε-lexicase over a standardized, multi-axis descriptor, feeding a
MAP-Elites archive.** Rationale:

1. **ε-lexicase needs no scalar aggregation and no Pareto dominance**, so it sidesteps both
   the units-domination problem (#1) and the many-objective curse (R-SEL-1). Continuous
   factors fit ε's pass-band ("within ε of the best on this axis"). It is analysed
   specifically for *large-scale many-objective* problems (La Cava & Moore 2018).
2. **ε-lexicase rewards specialists** → peculiar individuals (good on a *subset* of
   standardized axes) survive (R-SEL-3, principle #3) — exactly the user's "peculiarity
   survives" requirement, achieved *structurally* rather than by hand-tuned weights.
3. **MAP-Elites is the deliverable** (principle #11, R-PEC-2): the run produces a *map* of
   diverse elites, not one optimum. ε-lexicase selects parents; MAP-Elites stores the
   illuminated archive. Both already exist in the repo — this is *extend*, not new-build.
4. **Novelty (T7) stays as one descriptor axis / one MAP-Elites behavior dimension**, with
   a **minimal-criterion quality floor** (R-PEC-3) to avoid the degenerate-novelty trap.
   Do *not* make raw novelty the sole scalar objective.

**Normalization: per-generation z-score of every descriptor axis** (R-STD-1), computed over
the live population, with `ε` floor on σ. Use **rank** (T9) only for any external scalar
quality (real-LLM fitness, Stage 6) before mixing.

**Genome representation fixes (prerequisite, Stream C core):**
- Add `c_latent` to `Genome3D`; make `genome_flat_vector` return
  `zscore(concat(c_factors.as_flat(), w_latent · c_latent.as_flat()))` (R-NEUT-1/2/4, R-STD-1).
- Extend sparse/modular mutation to the factor chromosome (R-SPARSE-1/3).
- Keep `nsga2.py` for the ≤3-objective lane only; route the high-dim descriptor through
  ε-lexicase + MAP-Elites.

**Sequencing** (aligns with OPEN_ENDED §4 Stage 2): (a) z-score + wire reservoir into
descriptor → measure that "all-maxed" collapses and reservoir mutations now move the
descriptor; (b) swap selector to ε-lexicase, confirm diversity no longer collapses by gen
~25 and specialists persist; (c) add minimal-criterion floor; (d) latent→behavior bridge
(exaptation) **[SPEC]**.

---

## 6. RAD corpus note (honest disclosure on corpus coverage)

The RAD corpora at `D:/docs/{optimization,neural_network,agents}_corpus_v2` are dominated
by mainstream ML/optimization papers (Adam/SGD, simplex, Mamba/attention, NeRF, RAG). They
contain **degeneracy** material mostly in the *linear-programming* sense (simplex pivots),
not the evolvability sense, and metaheuristic coverage is generic (PSO/GA/NAS overview,
`cluster_04_metaheuristic_swarm_genetic`). The evolutionary-computation specifics above
(NEAT/CPPN, lexicase, FUSS, novelty search, MAP-Elites, Whitacre-Bender degeneracy, RNA
neutral networks, evo-devo) came from **web sources**, cited inline. The corpus did not add
unique evo-comp findings for this stream — flag for a future RAD ingest of an
evolutionary-computation / artificial-life corpus.

---

## References (primary)
- Whitacre & Bender (2010) Degeneracy: a design principle for robustness and evolvability — arXiv:0907.0510 / 0910.2586
- Kimura (1968) Neutral theory; Schuster/Fontana (RNA neutral nets); Wagner (2008) robustness↔evolvability; Greenbury et al. (2022) navigable GP-maps
- Stanley & Miikkulainen (2002) NEAT; Stanley et al. HyperNEAT/CPPN
- Hoekstra & Coyne (2007) The Locus of Evolution (evo-devo / cis-regulatory)
- Lehman & Stanley (2011) Abandoning Objectives (novelty search)
- Mouret & Clune (2015) Illuminating search spaces by mapping elites (MAP-Elites) — arXiv:1504.04909
- Helmuth & La Cava (2021) Lexicase Selection; La Cava et al. (2019) ε-lexicase; La Cava & Moore (2018) ε-lexicase many-objective
- Goldberg & Richardson (1987) fitness sharing/niching
- Deb et al. (2002) NSGA-II; Deb & Jain (2014) NSGA-III
- Hutter & Legg (2006) Fitness Uniform Optimization (FUSS) — arXiv:cs/0610126
- Code: `D:/projects/llive/src/llive/perf/evolutionary/{genome_3d,latent_reservoir,diversity,nsga2,quality_diversity}.py`
