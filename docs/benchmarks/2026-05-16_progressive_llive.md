---
layout: default
title: "Benchmark — 2026-05-16 Progressive llive"
nav_order: 65
parent: "Comparison"
---

# Benchmark — 2026-05-16 llive Progressive Token Stress

> Five Briefs spanning xs → xl (2 → 1650 chars) run through
> `FullSenseLoop.process()`, observing how each of the 6-stage pipeline's
> outputs varies with input size and content.
> Methodology: [feedback_benchmark_progressive_tokens](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_progressive_tokens.md).

## Briefs

| size | chars | words | content gist |
|---|---|---|---|
| xs | 2 | 1 | `hi` |
| s | 26 | 4 | `List three primary colors.` |
| m | 153 | 22 | `Write a one-paragraph summary of the FullSense umbrella project, listing llmesh, llive, llove, lldesign, and lltrade with a one-line description of each.` |
| l | 564 | 81 | trade-off resolution Brief embedding TRIZ keywords *segmentation*, *asymmetry*, *contradiction* |
| xl | 1650 | 226 | 6-axis integration plan embedding TRIZ keywords *segmentation*, *asymmetric distribution*, *preliminary anti-action* |

Stored under `docs/benchmarks/2026-05-16-progressive/{xs,s,m,l,xl}/_brief.txt`,
raw responses in the same dirs as `llive.json`.

## Stage values vs input size

| Stage | xs | s | m | l | xl | Verdict |
|---|---|---|---|---|---|---|
| salience.score | 0.7 | 0.7 | 0.7 | 0.7 | 0.7 | ⚠️ pinned to `--surprise 0.7` flag, no per-content computation |
| salience.pass | T | T | T | T | T | passes everything above the 0.4 threshold |
| curiosity.score | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | ❌ `known_corpus` is empty → novelty always 1.0 → no discrimination |
| curiosity.novelty | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | (same as above) |
| curiosity.known_overlap | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | (same as above) |
| **thought.triz_principles** | `[]` | `[]` | `[]` | **`[1]`** | **`[1]`** | ⚠️ only `segmentation` (P1) hit. P4 (asymmetry) and P11 (preliminary anti-action) missed despite being literal substrings of the Brief |
| thought.confidence | 0.8 | 0.8 | 0.8 | 0.8 | 0.8 | ❌ constant, not input-dependent |
| thought.text length | 66 | 90 | 184 | 205 | 205 | ✅ input prefix reflected; **plateaus at 205** chars (truncation at content[:140] + template) |
| ego_score | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | ❌ constant (LLIVE-005) |
| altruism_score | 0.1 | 0.1 | 0.1 | 0.1 | 0.1 | ❌ constant (LLIVE-005) |
| plan.decision | note | note | note | note | note | ❌ always `note` because the three discriminators above are constant |
| wall time (ms) | 314 | 150 | 141 | 158 | 138 | ⚠️ first call has Python interpreter cold start; subsequent calls ~140-160 ms (≈ subprocess+JSON IO, the loop itself runs in < 1 ms) |

## What varied (only 2 things)

1. **`thought.text` content prefix** — the f-string template
   `"Observation about '{source}': {content[:140]} — novel territory, worth exploring."`
   echoes the first 140 chars of the input. Genuine reflection of input,
   but no reasoning.
2. **`thought.triz_principles`** — `[1]` (Segmentation) at sizes l and xl
   because the literal token `segmentation` appears. The other planted
   TRIZ tokens (`asymmetry` for P4, `preliminary anti-action` for P11)
   were ignored — so the matcher is keyword-exact and biased toward a
   subset of the 40 principles.

## What did NOT vary (5 stages)

- `salience`: pinned to the `--surprise` argument
- `curiosity`: `known_corpus` not loaded → discriminator inert
- `ego_score`, `altruism_score`: constant 0.1 (LLIVE-005)
- `plan.decision`: always `note` because nothing above it varies

## Verdict on response soundness

The pipeline runs, but the **answer is structurally the same for every
input that meets the salience threshold**. The two things that vary
(text echo, partial TRIZ detection) cannot make the cycle reach
`PROPOSE` or `INTERVENE`, so no externally-visible artifact ever lands.

This is consistent with — and now empirically confirmed across 5 token
sizes for — what `project_llive_bug_2026_05_16` reported on m-size
Briefs alone:

- **LLIVE-001** (no LLM backend) → `thought.text` is a template, not a thought
- **LLIVE-003** (template, not generation) → confirmed at all 5 sizes
- **LLIVE-004** (TRIZ matcher) → **further refined**: matcher catches
  `segmentation` (P1) but misses `asymmetry`/`asymmetric distribution`
  (P4) and `preliminary anti-action` (P11). The keyword list inside
  `_inner_monologue` needs an audit against the 40 principles glossary.
- **LLIVE-005** (ego/altruism constant) → confirmed at all 5 sizes

## New findings beyond the earlier bug list

- The pipeline's wall time is **input-size-insensitive** in the 100x
  range we tested (xs is 2 chars, xl is 1650). The cycle truly is rule-
  based; there's no n^2 cost anywhere. Once LLIVE-001 lands, the wall
  time picture will change radically (LLM call dominates).
- `thought.text` plateaus at 205 chars regardless of input size beyond
  ~300 chars. The `content[:140]` cap inside `_inner_monologue` is the
  hard ceiling — long Briefs are observably truncated. When LLM is
  wired in, this cap should likely move (or vanish) so the model sees
  the full Brief.

## Implications for the v0.7 Brief API design

The benchmark validates the [Brief API design draft](https://github.com/furuse-kazufumi/llive/blob/main/docs/proposals/brief_api_design.md):

- Section 4 (`LLMBackend` Protocol) is the *only* way to break the constant
  output pattern. Static analysis of the Brief content can never produce
  the discrimination needed for `PROPOSE` / `INTERVENE`.
- Section 5 (Tool whitelist + execution) is needed because once the LLM
  produces a real plan, the cycle has to *do* something — currently the
  `note` decision means "log only, no externalised action".

## Repro

```bash
PYTHONIOENCODING=utf-8 python3 - <<'PY'
import json, subprocess, pathlib, time
ROOT = pathlib.Path('D:/projects/fullsense/docs/benchmarks/2026-05-16-progressive')
for s in ('xs','s','m','l','xl'):
    brief = (ROOT/s/'_brief.txt').read_text(encoding='utf-8')
    p = subprocess.run(['py','-3.11','D:/projects/llive/scripts/run_brief.py','--json',brief],
                       capture_output=True, text=True, encoding='utf-8', timeout=30)
    (ROOT/s/'llive.json').write_text(p.stdout, encoding='utf-8')
PY
```
