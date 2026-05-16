#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""bench_model_brief_matrix.py — llive × {ollama models} × {brief sizes} matrix.

Runs each combination via `FullSenseLoop` (LLIVE_LLM_BACKEND=ollama:<model>)
and captures the per-cell wall time, decision, thought text, triz_principles,
and an `ll*` typo count heuristic. Output goes under
`docs/benchmarks/<date>-matrix/<model>/<size>.json` and a summary
`matrix_summary.md` at the root.

Designed around the purity rules in `feedback_llive_measurement_purity`:
this script only runs models inside `FullSenseLoop` via ollama (on-prem).
For direct cloud-API baselines use `bench_run.py` (no llive in the path).

Kill-the-row gates:
  - single cell wall time > 300 s -> abort the row (cold-start or hang)
  - cell returns "" or BackendUnavailable -> abort the row

Usage:
  python3 scripts/bench_model_brief_matrix.py \\
      --models llama3.2 qwen2.5:7b qwen2.5:14b \\
      --sizes xs s m l xl
"""

from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import time

# Force UTF-8 stdout on Windows cp932.
if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BENCH_ROOT = pathlib.Path("D:/projects/fullsense/docs/benchmarks")
BRIEFS_DIR = BENCH_ROOT / "2026-05-16-progressive"
RUN_BRIEF = "D:/projects/llive/scripts/run_brief.py"

CELL_TIMEOUT_S = 300.0

LL_TYPO_RE = re.compile(r"\bl{3,}[a-z]+\b", re.IGNORECASE)


def safe_model_dirname(model: str) -> str:
    return model.replace(":", "_").replace("/", "_")


def run_cell(model: str, size: str, out_dir: pathlib.Path) -> dict:
    brief_path = BRIEFS_DIR / size / "_brief.txt"
    brief = brief_path.read_text(encoding="utf-8")
    env = {**os.environ, "PYTHONIOENCODING": "utf-8", "LLIVE_LLM_BACKEND": f"ollama:{model}"}
    t0 = time.perf_counter()
    try:
        p = subprocess.run(
            ["py", "-3.11", RUN_BRIEF, "--json", brief],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=CELL_TIMEOUT_S,
            env=env,
        )
        ms = (time.perf_counter() - t0) * 1000
    except subprocess.TimeoutExpired:
        ms = CELL_TIMEOUT_S * 1000
        return {
            "ok": False,
            "ms": ms,
            "error": f"timeout after {CELL_TIMEOUT_S}s",
            "size": size,
            "model": model,
            "brief_chars": len(brief),
        }
    if p.returncode != 0 or not p.stdout.strip():
        return {
            "ok": False,
            "ms": ms,
            "error": p.stderr[:500] or "no stdout",
            "size": size,
            "model": model,
            "brief_chars": len(brief),
        }
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError as e:
        return {
            "ok": False,
            "ms": ms,
            "error": f"json parse: {e}",
            "size": size,
            "model": model,
            "brief_chars": len(brief),
        }

    (out_dir / f"{size}.json").write_text(p.stdout, encoding="utf-8")
    th = d.get("stages", {}).get("thought", {})
    thought_text = th.get("text", "")
    return {
        "ok": True,
        "ms": round(ms, 1),
        "size": size,
        "model": model,
        "brief_chars": len(brief),
        "response_chars": len(thought_text),
        "decision": d.get("plan", {}).get("decision"),
        "triz_principles": th.get("triz_principles"),
        "confidence": th.get("confidence"),
        "salience_score": d.get("stages", {}).get("salience", {}).get("score"),
        "curiosity_score": d.get("stages", {}).get("curiosity", {}).get("score"),
        "ego_score": d.get("stages", {}).get("ego_score"),
        "altruism_score": d.get("stages", {}).get("altruism_score"),
        "ll_typo_count": len(LL_TYPO_RE.findall(thought_text)),
        "thought_text_head": thought_text[:160],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", nargs="+", required=True, help="ollama model names")
    parser.add_argument("--sizes", nargs="+", default=["xs", "s", "m", "l", "xl"])
    parser.add_argument("--out", type=pathlib.Path, default=None)
    parser.add_argument("--abort-on-timeout", action="store_true", default=True)
    args = parser.parse_args()

    today = time.strftime("%Y-%m-%d")
    root = args.out or (BENCH_ROOT / f"{today}-matrix")
    root.mkdir(parents=True, exist_ok=True)

    summary_rows: list[dict] = []
    print(f"bench_model_brief_matrix.py: models={args.models} sizes={args.sizes} out={root}")

    for model in args.models:
        model_dir = root / safe_model_dirname(model)
        model_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n=== row: model={model} ===")
        row_aborted = False
        for size in args.sizes:
            if row_aborted:
                print(f"  [SKIP] {size} (row aborted)")
                summary_rows.append({"ok": False, "ms": 0, "size": size, "model": model,
                                     "error": "row aborted by earlier gate"})
                continue
            print(f"  [run]  {size} ...", end="", flush=True)
            r = run_cell(model, size, model_dir)
            summary_rows.append(r)
            if r["ok"]:
                print(
                    f"  OK  {r['ms']:>6.0f} ms  {r['response_chars']:>5} chars  "
                    f"decision={r['decision']}  triz={r['triz_principles']}  "
                    f"typo={r['ll_typo_count']}"
                )
            else:
                print(f"  ERR  {r.get('error','?')[:80]}")
                if args.abort_on_timeout and "timeout" in str(r.get("error", "")):
                    row_aborted = True

    summary_path = root / "matrix_summary.json"
    summary_path.write_text(json.dumps(summary_rows, indent=2, ensure_ascii=False), encoding="utf-8")

    md_lines = ["# llive Model x Brief Matrix Summary", "",
                f"Generated: {today}", "",
                "| model | size | ok | ms | chars | decision | triz | typo |",
                "|---|---|---|---|---|---|---|---|"]
    for r in summary_rows:
        if r["ok"]:
            md_lines.append(
                f"| `{r['model']}` | {r['size']} | ✅ | {r['ms']:.0f} | "
                f"{r['response_chars']} | {r['decision']} | "
                f"{r['triz_principles']} | {r['ll_typo_count']} |"
            )
        else:
            md_lines.append(
                f"| `{r['model']}` | {r['size']} | ❌ | - | - | - | - | - "
                f"(error: {r.get('error','?')[:60]}) |"
            )
    (root / "matrix_summary.md").write_text("\n".join(md_lines), encoding="utf-8")
    print(f"\nresults under: {root}")
    print(f"summary: {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
