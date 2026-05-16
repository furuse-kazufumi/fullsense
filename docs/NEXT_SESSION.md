---
layout: default
title: "Next Session Handoff"
nav_order: 95
---

# Next Session Handoff (2026-05-16 → next)

> Picked up by the next FullSense session. Everything below is ready to
> resume on. Operator actions are flagged 🧑 (user) vs 🤖 (agent).

## ✅ Done in this session (2026-05-16)

Captured in the Phase 0.3 entry of [PROGRESS.md]({{ '/PROGRESS' | relative_url }}).
One-line summary:

- 2 new products bootstrapped (lldesign + lltrade alpha v0.0.1, all repos
  on GitHub with CI green)
- portal Family Tree + roadmap + comparison + 4 empirical benchmark
  reports + bench_run.py + bench_vlm.py
- llive A/B probe + 8 documented bugs + Brief API design proposal
- 3 new memories: `feedback_webpage_research_first` /
  `feedback_competitor_benchmark` / `project_llive_bug_2026_05_16` /
  `project_benchmark_2026_05_16`

## 🧑 Operator actions queued — pick these up first

### 1. UI work — 12 clicks total

Tracked in the session-end summary. URLs and per-click steps documented
there; one-shot verify after completion:

```bash
bash D:/projects/fullsense/scripts/verify_publication.sh
```

Baseline before any UI work: **21 FAIL / 1 PASS**. Target: **0 FAIL**.

### 2. Credential restoration — 3 cloud LLMs

| Service | Status | Where to fix |
|---|---|---|
| Anthropic API key | 401 invalid_x-api-key (revoke) | console.anthropic.com → API Keys → rotate; update `D:/api-keys.json::ANTHROPIC_API_KEY` |
| Gemini API key | 429 quota exceeded | aistudio.google.com → billing or new project |
| OpenAI API key | 429 insufficient_quota | platform.openai.com → billing |

Once any of the three is restored, re-run:

```bash
cd D:/projects/fullsense
PYTHONIOENCODING=utf-8 python3 scripts/bench_run.py --all --out docs/benchmarks/<DATE>/
PYTHONIOENCODING=utf-8 python3 scripts/bench_vlm.py --image docs/assets/images/og-card.png \
    --question "Describe this image in 2 sentences..." --all --out docs/benchmarks/<DATE>-vlm/
```

The scripts read `D:/api-keys.json` automatically; no other edits needed.

### 3. on-prem VLM warm-up (optional)

`ollama llama3.2-vision:11b` is pulled (7.9 GB) but cold-start exceeded
600 s on first inference. To get a useful number out of it:

```bash
ollama run llama3.2-vision    # leave it running once to warm the cache
# then re-run bench_vlm.py with --model llama32vision
```

If even warm runs are slow, downgrade the recommendation in [comparison]({{
'/comparison' | relative_url }}) to `qwen2-vl:7b` or similar.

## 🤖 Agent-side work for the next session

### Priority 1 — llive Brief API (closes LLIVE-001 + LLIVE-002)

Design draft is committed at
`D:/projects/llive/docs/proposals/brief_api_design.md`. ~5 days estimated.
Order:

1. Brief schema + dataclass + YAML loader
2. `LLMBackend` Protocol + `FakeBackend` + `OllamaBackend`
3. `BriefRunner` core (steps 1-3 + 6-7 of the loop integration)
4. Approval Bus integration (closes LLIVE-008)
5. Tool whitelist + execution
6. CLI `llive brief submit ...`
7. MCP `submit_brief` tool
8. TDD tests 1-8 in the proposal (skeleton already in the doc)

After this lands, re-run `bench_run.py --brief b1 b2 b3 b4 --model llive` —
llive should produce actual artifacts, and the docs/benchmarks story
flips from "structural gap" to "head-to-head quality comparison".

### Priority 2 — qwen2.5:14b (or similar) on-prem default

Install docs for lldesign / lltrade should not recommend `llama3.2:3b`
(see [the lltrade YAML benchmark]({{ '/benchmarks/2026-05-16_lltrade_yaml' | relative_url }})
and the `lllive` typo recurrence). Pull a 7B-14B model that doesn't
fumble `ll*` prefixes, re-run B1-B4, and update the install snippets
in:

- `D:/projects/lldesign/README.md`
- `D:/projects/lldesign/docs/index.md`
- `D:/projects/lltrade/README.md`
- `D:/projects/lltrade/docs/index.md`

### Priority 3 — portal Quick Demos link fix (confirmed unnecessary)

`docs/index.md` Quick Demos points at `/llove/scenarios/`,
`/llove/scenarios/anim/shogi/ja.svg`, and `/llmesh/demos/clustering_demo`.
Source files were checked via `gh api` at end-of-session and **all three
paths exist** in the respective repos (`llove/docs/scenarios/{index.md,
anim/shogi/{en,ja}.svg, svg/}`, `llmesh/docs/demos/clustering_demo.md`).
**Once Operator action 1.A (Pages enable) lands, these URLs will resolve
on their own — no portal-side edit needed.** Re-run
`verify_publication.sh` to confirm the portal link sweep goes to 0 FAIL.

### Priority 4 — branch protection follow-on

After Operator action 1.B is done (6 rulesets), expand the ruleset to
include `Require status checks: Test` on lldesign / lltrade (the CI
workflow is already green). For the older repos (llmesh / llive / llove
/ fullsense), add CI first, then the rule.

## State of the world (machine-checkable)

```bash
# Snapshot
gh api repos/furuse-kazufumi/fullsense --jq '{topics, homepage, has_pages}'
gh api repos/furuse-kazufumi/lldesign --jq '{topics, homepage, has_pages}'
gh api repos/furuse-kazufumi/lltrade --jq '{topics, homepage, has_pages}'

# Run end-to-end verify
bash D:/projects/fullsense/scripts/verify_publication.sh

# Re-run all benchmarks
PYTHONIOENCODING=utf-8 python3 D:/projects/fullsense/scripts/bench_run.py --all
PYTHONIOENCODING=utf-8 python3 D:/projects/fullsense/scripts/bench_vlm.py \
  --image D:/projects/fullsense/docs/assets/images/og-card.png \
  --question "Describe this image in 2 sentences. List the products you see and how they appear to be related. Answer in English." \
  --all
```

## Cross-references

- [PROGRESS]({{ '/PROGRESS' | relative_url }}) — full session changelog
- [NOTES]({{ '/NOTES' | relative_url }}) — design decisions
- [roadmap]({{ '/roadmap' | relative_url }}) — parked products + triggers
- [comparison]({{ '/comparison' | relative_url }}) — vs Claude Code / Perplexity / Codex / Gemini
- llive `docs/BUGS_2026-05-16_brief_ab.md` — the 8 llive gaps
- llive `docs/proposals/brief_api_design.md` — the v0.7 design
- maintainer memory: `feedback_competitor_benchmark`,
  `feedback_webpage_research_first`,
  `project_llive_bug_2026_05_16`,
  `project_benchmark_2026_05_16`,
  `project_fullsense_brand`
