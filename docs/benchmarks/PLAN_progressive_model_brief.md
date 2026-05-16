---
layout: default
title: "Plan — Progressive Model × Brief Benchmark"
nav_order: 66
parent: "Comparison"
---

# Plan — llive Progressive Model × Brief Benchmark

> Test plan derived from the 2026-05-16 user direction: "lliveも小規模から
> 大規模までモデルの段階を踏んでみましょう" + "テスト計画も立ててください。
> 小規模モデル×小規模セッションから、大規模に段階的に上げた方が良いでしょう。"

## Matrix

| | Brief xs (~2 c) | Brief s (~26 c) | Brief m (~150 c) | Brief l (~570 c) | Brief xl (~1650 c) |
|---|---|---|---|---|---|
| **rule-based (no LLM)** | ✅ baseline (`2026-05-16_progressive_llive.md`) | ✅ | ✅ | ✅ | ✅ |
| **tiny: llama3.2:3b** | T1 | T2 | T3 | T4 | T5 |
| **small: qwen2.5:7b** | S1 | S2 | S3 | S4 | S5 |
| **medium: qwen2.5:14b** | M1 | M2 | M3 | M4 | M5 |
| (future) **large: qwen2.5:32b or llama3.1:70b** | L1 | L2 | L3 | L4 | L5 |

20-25 cells. Execute in row-major order (model size ↑, then brief size ↑
within each row) so failures at the *small × xs* corner can be diagnosed
before paying for the larger cells.

## Execution gates (kill-the-row if hit)

For each row, abort to next row if any of:

1. Single cell wall time > 5 minutes (cold-start or hang)
2. Output completely empty (backend returned `""` or `BackendUnavailable`)
3. Response is byte-for-byte identical to a different cell in the same row
   (model collapsed to a degenerate output)

This protects against burning hours on a broken backend.

## Per-cell measurements

| Field | Type | Why |
|---|---|---|
| brief_chars | int | x-axis |
| brief_words | int | secondary x-axis |
| model | str (`ollama:qwen2.5:7b` etc.) | y-axis |
| wall_ms | float | latency curve |
| eval_count | int (Ollama returns) | tokens generated |
| response_chars | int | output volume |
| triz_principles | `list[int]` | TRIZ matcher hit |
| decision | `ActionDecision` | which loop branch fired |
| salience.score | float | pinned, but log anyway |
| curiosity.novelty | float | depends on `known_corpus` |
| ego_score / altruism_score | float | currently constant 0.1 |
| `ll*` typo count | int | `lllive` / `llllive` / `Live` mis-tokenisation count in response |

## Stage gates per model size

### tiny (llama3.2:3b)
- Goal: prove the wiring works end-to-end
- Pass criteria: xs cell returns a non-empty `response.text` within 30 s,
  `decision != note` for at least one cell in {s, m, l, xl}, no
  `BackendUnavailable` raised
- Fail mode: if `lllive` typo appears (it did on text & vision in earlier
  runs), record but continue

### small (qwen2.5:7b, ~4.7 GB pull)
- Goal: a competent on-prem default for lldesign/lltrade install docs
- Pass criteria: xl cell completes within 90 s, `ll*` typo count = 0
  across all 5 cells, `decision` advances past `note` on m+
- Fail mode: if typo count > 0, recommend the next-larger tier

### medium (qwen2.5:14b, ~9 GB pull)
- Goal: confirm the diminishing-returns inflection point
- Pass criteria: xl cell within 4 min (cold) / 2 min (warm), response
  quality measurably better than small on l/xl (subjective rating in
  the report, plus longer / more structured output)
- Fail mode: machine VRAM exhaustion → skip remaining cells in row

### large (qwen2.5:32b or llama3.1:70b) — DEFER
- Goal: ceiling check
- Defer until: small + medium rows have published reports + machine
  warm-up time predictable + ledger CPU budget known
- This row is intentionally left empty in v1 of the report

## Schedule

1. **Now**: wiring (`FullSenseLoop._inner_monologue` opt-in to existing
   `llive.llm` backend), pytest 970+ green, push to llive
2. **+ 5 min**: tiny row (llama3.2:3b — already pulled) all 5 cells
3. **+ 10 min** (parallel to step 2): qwen2.5:7b pull (~3 min on a 50 MB/s link)
4. **+ 20 min**: small row 5 cells
5. **+ 25 min** (parallel): qwen2.5:14b pull (~7 min)
6. **+ 60 min**: medium row 5 cells
7. **+ 75 min**: report write-up + push

Total ~75-90 min. Defer large row to next session.

## Repro script

Per-cell call signature:

```bash
LLIVE_LLM_BACKEND=ollama LLIVE_OLLAMA_MODEL=qwen2.5:7b \
  PYTHONIOENCODING=utf-8 \
  py -3.11 D:/projects/llive/scripts/run_brief.py --json \
  "$(cat D:/projects/fullsense/docs/benchmarks/2026-05-16-progressive/<size>/_brief.txt)" \
  > D:/projects/fullsense/docs/benchmarks/2026-05-16-progressive-model/<model>/<size>.json
```

The matrix runner script will be added as
`D:/projects/fullsense/scripts/bench_model_brief_matrix.py` in the same
PR cluster as the wiring.

## Cross-references

- Rule-based baseline: `2026-05-16_progressive_llive.md` (this session)
- Progressive token memo: `feedback_benchmark_progressive_tokens` (memory)
- llive Brief API design: `D:/projects/llive/docs/proposals/brief_api_design.md`
- llive llm module: `D:/projects/llive/src/llive/llm/backend.py` (already exists; LLIVE-001 corrected — wiring is the gap, not the backend layer)
