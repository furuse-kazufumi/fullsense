---
layout: default
title: "Comparison"
nav_order: 60
---

# FullSense ™ vs. the field

> Honest competitive positioning. We list capabilities we're behind on too —
> hiding them would just delay the gap-closing work.

## At a glance

| Capability | Claude Code | Perplexity | Codex CLI | Gemini CLI | **FullSense (llive + ll*)** |
|---|---|---|---|---|---|
| Code editing (SOTA) | **A** | C | A | A− | A |
| Web research + citations | B | **A+** | C | B+ (Google) | A (RAD-backed) |
| Autonomous resident loop | C (Stop on prompt) | F | C (full-auto) | C | **A** (ResidentRunner) |
| HITL workbench | F | F | C (approval mode) | C (approval mode) | **A** (llove TUI) |
| Memory persistence | C (file) | C (chat) | C (session) | C | **A** (SQLite Ledger) |
| **On-prem inference** | F (cloud) | F (cloud) | F (cloud) | F (cloud) | **A** (Ollama / LM Studio / vLLM) |
| CLI OSS | F | F | A (Apache-2.0) | A (Apache-2.0) | A |
| **Backend OSS (end-to-end)** | F | F | F | F | **A** (full OSS stack) |
| Audit Ledger (SIL) | F | F | F | F | **A** (per-action persistent log) |
| Dangerous-op gate | C (warning only) | F | A (approval mode) | A (approval mode) | A (Approval Bus) |
| MCP tool ecosystem | **A** | F | C | B (recent) | B (ll{domain} family) |
| Domain-specific adapters | C (generic) | C | C | C | **A** (lldesign / lltrade / planned llcad/lleda/llchip) |

Letter grades reflect 2026-05-16 state of the art. We update this page when
any row shifts ±1 grade.

## Where we are clearly ahead

- **On-prem inference** — All four competitors are cloud-only. FullSense runs
  end-to-end against your own Ollama / LM Studio / vLLM / TGI deployment.
- **End-to-end OSS** — Codex / Gemini publish OSS *CLIs*, but their backends
  (GPT, Gemini) are closed cloud APIs. FullSense lets you swap in any OSS
  model.
- **Audit Ledger** — None of the competitors persist a per-action audit log
  for compliance / law / reproducibility. llive's SQLite Ledger does.
- **HITL workbench** — Competitors that have approval modes (Codex / Gemini)
  show one signal at a time in a CLI prompt. llove gives you a full TUI
  workbench where the human stays in the loop.

## Where we are behind (and what we're doing about it)

### vs. Claude Code

- **Coding precision** — Claude Code is the current SOTA. We compete on
  *safety* (Approval Bus blocks dangerous ops at the API level, not as a
  text warning) and *audit* (every edit lands in the Ledger).
- **MCP tool ecosystem** — Anthropic ships dozens of MCP servers. Our path
  is **domain-specific** MCP servers from the ll{domain} family. Generic MCP
  parity is not the goal.

### vs. Perplexity

- **Citation UX** — Perplexity's citation rendering is excellent. We have
  the data (RAD 49 domains, ~49K documents, frozen so citations don't rot),
  but the UX has to be built in llove.
- **Reasoning UI** — Perplexity Pro shows step-by-step thinking. The llive
  Ledger has this data; llove needs a timeline view to surface it.

### vs. Codex CLI

- **Approval mode polish** — Codex's `suggest / auto-edit / full-auto` is
  battle-tested. The llive Approval Bus has the right architecture but needs
  UX work: timeout policies, retry semantics, grouped approvals.

### vs. Gemini CLI

- **Web search integration** — Gemini's Google Search integration is
  first-class. Our RAD is frozen (great for stability, bad for "what
  happened this week"). The plan is to add WebFetch / SearXNG / Brave Search
  MCP integration through the ll{domain} layer, keeping the RAD as the
  high-trust tier.

## Benchmark methodology

For every new feature in FullSense, we:

1. Define a Brief that exercises the feature
2. Run the same Brief against Claude Code, Perplexity, Codex CLI, Gemini CLI,
   and the FullSense stack
3. Score on: correctness, speed, citation quality, dangerous-op handling,
   cost, on-prem capability, backend OSS, audit log presence
4. Publish the per-product benchmark results under each product's
   `docs/benchmarks/<date>.md`
5. Open issues for any axis where FullSense lost

Methodology details: [`feedback_competitor_benchmark`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_competitor_benchmark.md)
in the maintainer's tooling repo.

## Empirical benchmarks (2026-05-16)

Four Briefs run against llive (`FullSenseLoop.process`) + ollama
`llama3.2:3b` (on-prem) + Perplexity Sonar (cloud). Anthropic Haiku 4.5,
Gemini 2.0 Flash, OpenAI Codex were attempted but failed for credential /
quota reasons (operator action queued).

- [Mermaid family-tree generation]({{ '/benchmarks/2026-05-16_mermaid_brief' | relative_url }})
- [Quick Start section + MCP sequence diagram]({{ '/benchmarks/2026-05-16_quickstart_seqdiag' | relative_url }})
- [lltrade paper-trading strategy YAML]({{ '/benchmarks/2026-05-16_lltrade_yaml' | relative_url }})

Headline of the day:

- llive does not yet generate (LLIVE-001 / LLIVE-002 in
  [`docs/BUGS_2026-05-16_brief_ab.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/BUGS_2026-05-16_brief_ab.md))
- ollama `llama3.2:3b` is the working on-prem option but produces the
  `lllive` typo (3 Ls) twice across 4 Briefs — tokenisation hostility to
  the `ll*` naming convention. Recommended replacement: qwen2.5:14b+
- Perplexity Sonar scores 4/4 on spec compliance at ~$0.005/brief

## Last updated

2026-05-16 — initial publication + first 4-Brief A/B run. Reviewed at:
portal-side `PROGRESS.md` *Phase 0.3 — umbrella expansion* and *Phase 0.3
— competitive positioning* entries.
