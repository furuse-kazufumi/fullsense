---
layout: default
title: "Benchmark — 2026-05-16 lltrade Strategy YAML"
nav_order: 63
parent: "Comparison"
---

# Benchmark — 2026-05-16 lltrade strategy YAML

> Fourth Brief in the 2026-05-16 session, domain-loaded to stress
> lltrade-flavoured constraints (RPAR / SIL safety pin / domain reasoning).
> Methodology: [feedback_competitor_benchmark](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_competitor_benchmark.md).

## The Brief (507 chars)

> Generate a YAML paper-trading strategy for the lltrade package. The strategy
> targets 'tech earnings dispersion' (long high-beat, short low-beat).
> Required YAML fields: name, universe (5 tickers from
> AAPL/MSFT/GOOGL/META/AMZN), regime, entry_signal, exit_signal,
> position_size_pct, max_drawdown_pct (must be ≤ 10), sharpe_target (≥ 1.5),
> sector_caps. CRITICAL: include a top-level boolean `paper_trading: true`
> (the package refuses to run without it). Output ONLY the YAML, no
> commentary, no fenced block.

## Scoreboard

| AI | Wall (ms) | chars | paper_trading:true | universe correct | drawdown ≤ 10 | sharpe ≥ 1.5 | domain semantics | sector_caps shape | No fence/preamble |
|---|---|---|---|---|---|---|---|---|---|
| llive | **157** | — (no generation) | n/a | n/a | n/a | n/a | n/a | n/a | n/a |
| ollama llama3.2:3b | 24 272 | 434 | ✅ | ✅ | ✅ (exactly 10) | ✅ | ❌ (`mean_reversion` regime — wrong) | ❌ (list of strings, not dict) | ⚠️ leading `---` front-matter |
| **Perplexity Sonar** | **4 460** | **774** | ✅ | ✅ | ✅ (8) | ✅ | ✅ (dispersion language correct) | ✅ (`{sector: cap}` dict) | ✅ |

## Outputs

### llive

```json
{"plan": {"decision": "note", "rationale": "novel territory; record for later consolidation"}}
```

Same shape as B1/B2/B3 — no LLM call, no generation. Tracked as
[LLIVE-001 / LLIVE-002](https://github.com/furuse-kazufumi/llive/blob/main/docs/BUGS_2026-05-16_brief_ab.md).

### ollama llama3.2:3b (434 chars, ~24 s)

```yaml
---
paper_trading: true
name: Tech Earnings Dispersion
universe:
  - AAPL
  - MSFT
  - GOOGL
  - META
  - AMZN
regime: mean_reversion
entry_signal:
  signal_type: 'high_beat'
  long_position: True
  short_position: False
  threshold: 0.05
exit_signal:
  signal_type: 'low_beat'
  long_position: False
  short_position: True
  threshold: -0.05
position_size_pct: 0.02
max_drawdown_pct: 10
sharpe_target: 1.5
sector_caps:
  - Technology
```

**Strong points:**
- The `CRITICAL: paper_trading: true` instruction worked — emphasis got
  through to a 3B model.
- All required fields are present.

**Issues:**
- `regime: mean_reversion` contradicts the Brief — earnings dispersion is
  a *cross-sectional* anomaly, not mean reversion. The model latched onto
  a more common YAML regime word.
- `sector_caps: ["Technology"]` is structurally wrong — caps need a numeric
  value per sector.
- `signal_type: high_beat` / `low_beat` is a label, not a signal definition;
  no threshold semantics beyond the magic 0.05.
- Leading `---` is unnecessary YAML front-matter.

### Perplexity Sonar (774 chars, ~4.5 s)

```yaml
paper_trading: true
name: tech_earnings_dispersion
universe:
  - AAPL
  - MSFT
  - GOOGL
  - META
  - AMZN
regime: earnings_dispersion
entry_signal: >
  Enter long the highest estimated earnings-beat name in the universe and
  short the lowest estimated earnings-beat name when the cross-sectional
  dispersion of earnings surprises is elevated, analyst revisions are
  mixed, and implied move premiums exceed their 20-day median.
exit_signal: >
  Exit both legs when the dispersion signal normalizes, the earnings event
  has passed, or the relative surprise spread compresses below its 20-day
  threshold.
position_size_pct: 0.10
max_drawdown_pct: 8
sharpe_target: 1.5
sector_caps:
  communication_services: 0.30
  consumer_discretionary: 0.30
  information_technology: 0.40
```

Spec compliance full, plus:
- Correct regime tag (`earnings_dispersion`)
- Entry / exit signals are operational definitions, not placeholders
- Sector caps as `{sector: cap}` dict — matches the Brief intent
- max_drawdown 8 < 10 — leaves safety margin rather than skating the limit
- No filler, no fence, no commentary

The longest single response so far (774 chars) and still the fastest of the
two working models (4.5 s vs 24 s).

## Cross-Brief summary (B1 + B2 + B3 + B4)

| AI | Briefs run | Hard fails | Spec violations | Domain errors | Typos |
|---|---|---|---|---|---|
| llive | 4 | 4 (no generation) | n/a | n/a | n/a |
| ollama llama3.2:3b | 4 | 0 | 7 (constraint / fence / line-count / front-matter) | 3 (LLD hallucination, regime mislabel, sector_caps shape) | 2 (`lllive` ×2) |
| **Perplexity Sonar** | 4 | 0 | 1 (`sh` fence instead of `bash`) | 0 | 0 |

Perplexity Sonar remains the only viable non-llive baseline today.
ollama llama3.2:3b is consistently under spec — it works as a working
on-prem **fallback** but cannot serve as the recommended on-prem default.

## Cost / latency profile

| Model | Cost per Brief | Latency p50 | On-prem? |
|---|---|---|---|
| llive | $0 | <1 s | yes (when implemented) |
| ollama llama3.2:3b | $0 | 13-24 s | yes |
| Perplexity Sonar | ~$0.005 | 2-4 s | no |

## What this tells us about FullSense positioning

1. **lltrade's `paper_trading: true` hard-pin is enforceable by Brief
   prompt.** Even a 3B model respected the CRITICAL emphasis. The
   3-layer safety pin in [lltrade SPEC](https://furuse-kazufumi.github.io/lltrade/SPEC.html)
   should also be documented in any Brief template emitted by the v0.7
   `BriefRunner`.
2. **Domain semantics is where Perplexity wins big.** The lltrade
   competitive positioning vs Claude Code / Codex / Gemini in
   [lltrade docs/SPEC.md](https://furuse-kazufumi.github.io/lltrade/SPEC.html#vs-generic-coding-agents-claude-code--codex-cli--gemini-cli)
   is empirically supported on this Brief: generic agents (cloud LLMs)
   can produce surface-valid YAML but only Perplexity got the regime tag
   right.
3. **Recommended on-prem model for lltrade install docs:** must be ≥7B,
   and earnings-dispersion benchmark is a reasonable sanity check at
   install time. Add this Brief to lltrade's `tests/integration/`
   directory (skipped unless `LLTRADE_TEST_OLLAMA=1`).
