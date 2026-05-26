# Continuously-Evolving Populations as Live Orchestrated Ensembles
## An Open-Ended Evolution Architecture for On-Premise LLM Cognitive Diversity

**Author:** Kazufumi Furuse (古瀬 和文) — FullSense project (llmesh / llive / llove)
**Date of record (priority):** 2026-05-27
**Status:** Research note / defensive publication. Proxy-stage evidence (mechanism feasibility). Not a benchmarked state-of-the-art claim.
**License:** Apache-2.0 + Commercial (FullSense dual-license).
**Canonical source:** FullSense public repository, this file's git commit timestamp establishes the date of record.

---

> **Priority statement (plain language).** To our knowledge, as of 2026-05-27 and after a
> literature survey (arXiv/IACR corpora + a Perplexity `sonar-pro` survey), **no prior work
> unifies (a) a continuously-evolving population of agents with (b) a live orchestrated
> ensemble that answers queries in real time, with the evolution loop and the answering loop
> running simultaneously.** We document this architecture — and the specific design choices
> that make it work (competence-aware routing over a quality-diversity behavior descriptor;
> open-ended selection that avoids objective saturation; neutral lineage reservoirs; sandboxed
> agentic investigation behind a one-way approval gate) — as a dated research contribution.
> We make **no** claim of benchmarked superiority over frontier systems; the evidence below is
> proxy-stage (mechanism feasibility), disclosed honestly.

---

## Abstract (EN)

Evolving large language model (LLM) behaviors against a *fixed* scalar objective saturates
quickly: once the objective is maxed, selection pressure vanishes and "evolution" degenerates
into genetic drift — a filtered random search, not cumulative adaptation. We reproduce this
pathology empirically at two scales (a 500-generation proxy run and a 12-hour real-LLM run on
a local Ollama model), then propose and proxy-validate an alternative architecture with two
distinguishing ideas. **First**, *open-ended selection*: replace the fixed scalar objective
with novelty / ε-lexicase selection under per-dimension standardization, a minimal-criterion
gate, a MAP-Elites quality-diversity (QD) archive, and a neutral lineage reservoir. **Second**,
and our central novel claim, *the population is never "finished":* it evolves continuously and,
at any instant, is orchestrated into a single answer by a **competence-aware router** (not a
vote) keyed on the same behavior descriptors the QD archive already maintains. Across a
19-configuration sweep (10,000 generations, population 256) every fixed-scalar configuration
collapses (0/6, including scalar+QD) while every open-ended configuration sustains diversity
(13/13). Population scale monotonically increases open-endedness (occupied niches 171→1219 as
population grows 256→4096). For orchestration, a synthetic study and a real-LLM study agree
independently: a diverse ensemble beats the single best individual **only** under
competence-aware routing (real-LLM single-best 0.933 → routed ensemble 1.000), while majority
voting never beats the single best — explaining a published "diversity is not automatically
better" counter-result as an artifact of the *aggregator*, not of diversity itself. We discuss
agentic individuals (sandboxed investigation with a cost term that makes selective investigation
emerge) and a two-space safety model. All quantitative results are proxy-stage and stated with
their confounds.

## 要旨 (JA)

固定したスカラー目的に対して大規模言語モデル(LLM)の振る舞いを進化させると、目的は速やかに
飽和する。満点が出た瞬間に選択圧は消え、「進化」は遺伝的浮動——累積的適応ではなく、フィルタ
付きランダム探索——に堕する。本稿はこの病理を二つの規模（500 世代の proxy ラン、ローカル
Ollama 上の 12 時間実 LLM ラン）で実証し、二つの際立つ着想をもつ代替アーキテクチャを提案・
proxy 検証する。**第一に**、*開放端選択*: 固定スカラー目的を、次元別標準化下の novelty /
ε-lexicase 選択、最低基準ゲート、MAP-Elites 品質多様性(QD)アーカイブ、中立系統貯蔵庫で
置き換える。**第二に**、そして本稿の中心的な新規主張として、*集団は決して「完成」しない*：
集団は連続して進化し続け、任意の瞬間に、QD アーカイブが既に保持する behavior descriptor を
鍵とした**competence-aware ルーター**（投票ではない）によって 1 つの回答へ合奏される。
19 構成のスイープ（1万世代・母数256）で、固定スカラー構成は全て崩壊（6 件中 0 件成立、
scalar+QD を含む）、開放端構成は全て多様性を持続（13/13）。母数スケールは開放端性を単調に
増やす（母数 256→4096 で占有ニッチ 171→1219）。合奏については合成実験と実 LLM 実験が独立に
一致する：多様なアンサンブルが単一最良個体を上回るのは**competence-aware ルーティングの
ときだけ**（実 LLM で単一最良 0.933→ルーティング合奏 1.000）であり、多数決は単一最良を一度も
上回らない——既発表の「多様性は自動的に優位ではない」という反証結果が、多様性そのものでなく
*集約器*のアーティファクトであることを説明する。調査機能をもつ個体（サンドボックス調査＋
選択的調査を創発させるコスト項）と二空間安全モデルも論じる。定量結果は全て proxy 段であり、
交絡とともに明示する。

---

## 1. The pathology: fixed objectives saturate (and "evolution" becomes drift)

We evolve *prompt strategies* for a fixed small LLM (each individual maps a genome chromosome
to a system prompt; the LLM weights are fixed). Two runs expose the failure mode:

- **500-generation proxy run.** Eight "founder" cognitive personas were seeded. The best score
  pinned to 1.0 at generation 1 and stayed there; by generation 500 only two lineages survived,
  the rest going extinct — not because they were weaker, but because *with zero selection
  pressure the outcome is a coin flip* (genetic drift).
- **12-hour real-LLM run** (local Ollama, llama-class model, 71 generations, population 24).
  Best score reached 1.0 by generation 5 and never moved through generation 70. Of ten scored
  questions, six to seven were saturated (every individual correct); only two "multi-step"
  questions carried any gradient. The population did **not** collapse (size held; minimum score
  ≥ 0.70) yet adaptation did **not** accumulate. It behaved like filtered random search.

**Diagnosis.** When the measuring instrument saturates, the executioner is powerless: no amount
of selection-operator engineering helps if every survivor scores identically. The fix must act
on *what is measured and how diversity is preserved*, not only on *who is selected*.

## 2. Architecture

### 2.1 Open-ended selection (replaces the fixed scalar objective)

- **Selection** = novelty and/or ε-lexicase, under **per-dimension z-score standardization**
  (so "good at everything" — low variance — earns no advantage), with a **minimal-criterion
  gate** (reproduction requires meeting a *moving* threshold, e.g. a population percentile, not
  a fixed absolute) and a **MAP-Elites QD archive** (per-cell elites make diversity collapse
  structurally impossible).
- **Behavior descriptors** are reduced to low dimension (Johnson–Lindenstrauss random
  projection) so novelty k-NN stays tractable and *all* genes contribute statistically.
- **Neutral lineage reservoir.** Behavioral diversity and *lineage* diversity are different
  axes: novelty preserves the former while lineages still fix to one. A neutral reservoir that
  re-injects extinct lineages restores lineage diversity without harming behavior.
- **Adaptive difficulty (curriculum over conditions, not tasks).** Because a small battery
  saturates, difficulty rises with the population (a moving percentile), supplying a gradient
  indefinitely. Adaptive difficulty and QD/novelty are **complementary, both required**:
  difficulty supplies the gradient; QD preserves diversity.
- **Factor-subspace QD.** Novelty over a large descriptor preserves *overall* diversity but lets
  *semantic* dimensions drift; a second QD/novelty pressure on the semantic subspace protects
  meaning-bearing diversity.

### 2.2 The novel core: a living population that is also a live orchestra

The artifact is **not** a single "best" exported at the end of a run, nor a fixed ensemble.
The QD archive **evolves continuously** and, at any instant, the current population is
**orchestrated into one answer**:

- **Time separation** resolves the apparent contradiction (the population is always changing,
  yet an answer must be stable): evolution runs in the background; an answer is produced from a
  *snapshot* of the current archive. Answering does not block evolution and vice-versa.
- **Competence-aware routing, not voting.** The aggregator must route each sub-problem to the
  member competent for it. A naive majority/average *destroys* the benefit of diversity (the one
  competent specialist is out-voted by the ignorant majority). A router keyed on the **behavior
  descriptors the QD archive already maintains** recovers most of the oracle benefit without
  needing calibrated confidence — so QD and orchestration **share one descriptor substrate**.

### 2.3 Agentic individuals and a two-space safety model

Individuals may carry an **investigation budget** (query a read-only knowledge source before
answering). A **cost term** is essential: free investigation degenerates into "always
investigate"; with cost, *selective* investigation emerges (evolution discovers an
investigate-only-when-worth-it threshold). Safety is enforced by **two-space separation**: in
the exploration space individuals are inert data evaluated by pure, I/O-free functions; any real
tool/web use occurs only in an effect space reachable through a **one-way, fail-closed approval
gate**. Governance lives outside the evolving set, so "a constraint that cannot be reached
cannot be optimized away."

## 3. Proxy experiments and results (mechanism feasibility)

All experiments are deterministic, proxy (no real LLM unless stated), and sandboxed.

| Question | Result | Pass/fail line |
|---|---|---|
| Does open-ended selection avoid the saturation/collapse that fixed-scalar hits? | **13/13 open-ended configs open-ended; 0/6 fixed-scalar (incl. scalar+QD)**. Standardization expands occupied niches 9→100+. Neutral reservoir restores lineages (unique lineages 1→32). | open-ended = monoculture < 0.8, tail-end niche growth, sustained behavioral diversity |
| Does scale qualitatively increase open-endedness? | Population 256→4096: niches 171→1219, monoculture 0.047→0.006, lineages 14→372 (monotone). Latent 256→1024: niches 101→166. | monotone improvement in niches / monoculture / lineages |
| Does adaptive difficulty fix the capability stall, and at what cost? | Fixed difficulty stalls capability at 0.627; adaptive reaches 0.952 but collapses diversity (0.31→0.13); **adaptive + novelty reaches 0.881 capability AND 0.316 diversity** (both retained). | adaptive+novelty ≥ baseline capability and ≈ baseline diversity |
| Does a diverse ensemble beat the single best? | **Only under competence-aware routing.** Synthetic: diverse best-of 1.000 > redundant 0.750 > single 0.500; diverse *majority* = 0.000. Real-LLM: single best 0.933 → routed ensemble 1.000; majority/weighted never beat 0.933. | routed ensemble > single best; majority ≤ single best |
| Can a *realistic* (non-oracle) router approach the oracle? | Descriptor-router 0.90 (calibration-free) vs single best 0.675; confidence-router reaches the oracle once calibration κ ≥ 0.6; majority 0.34. | descriptor-router > single best, near oracle |
| Does a cost term make agentic investigation *selective*? | Evolution finds the value threshold θ→λ·c; no-investigation loses 45% at zero cost; selective ≥ both extremes. | evolved θ tracks λ·c; selective ≥ always/never |
| Does factor-subspace QD protect semantic diversity? | Factor retention 49.5% → 68.1% with a factor-subspace novelty pressure (loss roughly halved). | retention(full+factor) > retention(full-only) |

**Cross-validation.** These conclusions were reached by *independent* methods that agree —
notably the routing result holds in both a synthetic specialist model and a real-LLM run. We
treat such convergence as the main reason to trust proxy findings, per our honest-disclosure
discipline.

## 4. Novel contributions claimed (with date 2026-05-27)

1. **Continuously-evolving population as a live orchestrated ensemble** (evolution loop and
   answering loop running simultaneously; answer from a current snapshot). We find no prior art
   unifying these.
2. **Shared descriptor substrate for QD and orchestration**: the QD behavior descriptors double
   as competence-routing keys, so diversity-maintenance and answer-routing reuse one structure.
3. **Diagnosis of the "diversity is not automatically better" counter-result** as an *aggregator*
   artifact (voting vs competence-aware routing), with a calibration-free descriptor-router as a
   practical remedy on small on-premise models.
4. **An open-ended cognitive-diversity map** (explicit human cultural/cognitive descriptors +
   novelty/QD) as the differentiation axis, deliberately *not* competing on verifiable code/
   algorithm discovery (where frontier cloud compute wins).
5. A **two-space, fail-closed** safety model for *contained open-endedness* with agentic
   individuals.

## 5. Honest limitations (disclosed, not hidden)

- **Proxy stage.** Quantitative results test *mechanism feasibility*, not real LLM capability.
  The "does it produce a new intelligence" claim requires the real-LLM stage and is **not** made
  here.
- **Confounds stated.** In the scale sweep, generations were shortened as population grew
  (5000→1200); this biases *against* niche growth, so the observed monotone increase is a robust
  lower bound, but archive-cell and raw-novelty counts are confounded and were excluded from the
  verdict.
- **Routing upper bound.** "best-of" is an oracle; a real router's quality is bounded by how well
  descriptors predict competence. Small models may be poorly calibrated, which is why the
  calibration-free descriptor-router is preferred.
- **Factor-subspace QD is partial** (halves, does not eliminate, semantic drift).
- **Deceptive alignment is not solved.** Containment makes real-world effect structurally zero
  and audits every transgression, but cannot *guarantee* detection of observation-only good
  behavior. This is a contain-audit-disclose loop, not a guarantee.
- **Cultural descriptors are metaphor, not measurement.** Human cultural-dimension frameworks
  inspire the descriptor design; proxy agents are not claimed to share that geometry.

## 6. Related work (positioning)

Open-ended evolution and quality-diversity: novelty search (Lehman & Stanley, 2011); MAP-Elites
and CVT-MAP-Elites (Mouret & Clune, 2015); CMA-MAE; Dominated Novelty Search (2025); POET /
Enhanced POET (Wang et al., 2019–2020); AURORA (unsupervised descriptors); AI-GAs (Clune, 2019).
LLM-driven evolution: Promptbreeder, FunSearch, AlphaEvolve, EvoPrompt; Sakana AI CycleQD / ASAL
(on-premise QD precedent). Self-improving agents: Voyager (2023); ADAS; Darwin-Gödel Machine
(2025). Ensembling: Mixture-of-Agents (Wang et al., 2024) and the 2025 Self-MoA counter-result
(diversity not automatically better). **Our position:** we adopt the open-ended/QD machinery and
the MoA aggregation idea, but the *unification* — a continuously-evolving population that is
simultaneously a live, competence-routed orchestra over a shared descriptor substrate — is, to
our knowledge, the white-space we contribute here.

## 7. Reproducibility

Proxy experiment scripts and the full decision log (the overnight "PoC marathon" of 2026-05-26/27)
are in the FullSense public repository under `docs/research/` (per-experiment scripts dated
`2026_05_26`) and the open-ended requirements specification under `docs/vision/`. The evolution
substrate (selection operators, QD archive, novelty lane, lineage reservoir, expert council)
lives in the `llive` package. This document's git commit timestamp is the date of record.

---

### Changelog
- **2026-05-27** — v1, date of record. Proxy-stage evidence; architecture and priority claim
  documented. Real-LLM validation, larger-scale sweeps, and zh/ko translations are future work.
