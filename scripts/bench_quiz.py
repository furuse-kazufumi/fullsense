#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""bench_quiz.py — probe llive's LLM reasoning depth with 10 quizzes x N models.

Runs each quiz through `FullSenseLoop` with `LLIVE_LLM_BACKEND=ollama:<model>`
and `--debug` (so the trace contains the LLM prompt / response / wall time).
Scores answers with simple keyword matching (case-insensitive substring).

Designed around the purity rules in `feedback_llive_measurement_purity`:
this script only exercises on-prem ollama models inside the FullSense
pipeline. Cloud baselines belong in `bench_run.py`.

Usage:
  python3 scripts/bench_quiz.py --models llama3.2 qwen2.5:7b qwen2.5:14b
  python3 scripts/bench_quiz.py --models llama3.2 --release  # debug off
"""

from __future__ import annotations

import argparse
import io
import json
import os
import pathlib
import subprocess
import sys
import time

if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BENCH_ROOT = pathlib.Path("D:/projects/fullsense/docs/benchmarks")
QUIZ_SET = BENCH_ROOT / "quizzes/quiz_set_v1.json"
RUN_BRIEF = "D:/projects/llive/scripts/run_brief.py"

CELL_TIMEOUT_S = 300.0


def score_answer(answer: str, expected: list[str], scoring: str) -> tuple[bool, float]:
    """Return (passed, partial_score 0-1)."""
    a = (answer or "").lower()
    hits = sum(1 for kw in expected if kw.lower() in a)
    total = len(expected) if expected else 1
    if scoring == "keyword_match":
        return (hits >= 1, 1.0 if hits >= 1 else 0.0)
    if scoring == "keyword_all":
        return (hits == total, hits / total)
    if scoring == "keyword_any":
        return (hits >= 1, hits / total)
    if scoring in ("keyword_all_soft", "keyword_any_soft"):
        # creative — pass if any keyword matched (partial credit is the ratio)
        return (hits >= 1, hits / total)
    return (False, 0.0)


def run_quiz(model: str, quiz: dict, debug: bool, out_dir: pathlib.Path) -> dict:
    env = {
        **os.environ,
        "PYTHONIOENCODING": "utf-8",
        "LLIVE_LLM_BACKEND": f"ollama:{model}",
    }
    args = ["py", "-3.11", RUN_BRIEF, "--json"]
    if debug:
        args.append("--debug")
    args.append(quiz["question"])
    t0 = time.perf_counter()
    try:
        p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8",
                           timeout=CELL_TIMEOUT_S, env=env)
        ms = (time.perf_counter() - t0) * 1000
    except subprocess.TimeoutExpired:
        return {"ok": False, "ms": CELL_TIMEOUT_S * 1000, "error": "timeout",
                "quiz_id": quiz["id"], "model": model}
    if p.returncode != 0 or not p.stdout.strip():
        return {"ok": False, "ms": ms, "error": (p.stderr[:300] or "no stdout"),
                "quiz_id": quiz["id"], "model": model}
    try:
        d = json.loads(p.stdout)
    except json.JSONDecodeError as e:
        return {"ok": False, "ms": ms, "error": f"json parse: {e}",
                "quiz_id": quiz["id"], "model": model}
    answer = d.get("stages", {}).get("thought", {}).get("text", "")
    passed, partial = score_answer(answer, quiz["expected_keywords"], quiz["scoring"])
    cell = {
        "ok": True,
        "quiz_id": quiz["id"],
        "category": quiz["category"],
        "difficulty": quiz["difficulty"],
        "model": model,
        "ms": round(ms, 1),
        "answer_chars": len(answer),
        "answer_head": answer[:300],
        "answer_full": answer,
        "passed": passed,
        "partial_score": round(partial, 2),
    }
    (out_dir / f"{quiz['id']}.json").write_text(p.stdout, encoding="utf-8")
    return cell


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--quizzes", nargs="*", default=None,
                        help="quiz ids to run (default: all)")
    parser.add_argument("--out", type=pathlib.Path, default=None)
    parser.add_argument("--release", action="store_true",
                        help="run with debug=False (default = debug on)")
    args = parser.parse_args()

    quiz_set = json.loads(QUIZ_SET.read_text(encoding="utf-8"))
    quizzes = quiz_set["quizzes"]
    if args.quizzes:
        ids = set(args.quizzes)
        quizzes = [q for q in quizzes if q["id"] in ids]

    today = time.strftime("%Y-%m-%d")
    suffix = "release" if args.release else "debug"
    root = args.out or (BENCH_ROOT / f"{today}-quiz-{suffix}")
    root.mkdir(parents=True, exist_ok=True)
    (root / "_quiz_set.json").write_text(json.dumps(quiz_set, indent=2, ensure_ascii=False),
                                          encoding="utf-8")

    debug = not args.release
    print(f"bench_quiz.py: models={args.models} quizzes={len(quizzes)} debug={debug} out={root}")
    cells = []
    for model in args.models:
        model_dir = root / model.replace(":", "_").replace("/", "_")
        model_dir.mkdir(parents=True, exist_ok=True)
        print(f"\n== {model} ==")
        for q in quizzes:
            print(f"  [{q['id']:<11}] {q['category']:<10} {q['difficulty']:<6} ...", end="", flush=True)
            r = run_quiz(model, q, debug, model_dir)
            cells.append(r)
            if r.get("ok"):
                print(f" {r['ms']:>6.0f}ms  pass={r['passed']}  partial={r['partial_score']}  ans:{r['answer_head'][:80]!r}")
            else:
                print(f" ERR {r.get('error','?')[:60]}")

    # summary md
    md = ["# Quiz Reasoning Benchmark", "",
          f"Generated: {today} | mode: {suffix} | debug={debug}", "",
          "| model | quiz | cat | diff | ms | pass | partial | answer head |",
          "|---|---|---|---|---|---|---|---|"]
    for c in cells:
        if c.get("ok"):
            md.append(f"| `{c['model']}` | {c['quiz_id']} | {c['category']} | {c['difficulty']} | "
                      f"{c['ms']:.0f} | {'✅' if c['passed'] else '❌'} | {c['partial_score']} | "
                      f"{c['answer_head'][:80].strip().replace('|', '/')} |")
        else:
            md.append(f"| `{c['model']}` | {c['quiz_id']} | - | - | - | ❌ | - | error: {c.get('error','?')[:60]} |")
    md.append("")
    md.append("## Per-model summary (with statistics — added 2026-05-17)")
    md.append("")
    md.append("| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |")
    md.append("|---|---|---|---|---|---|---|---|")
    import statistics as _stat

    for model in args.models:
        cells_m = [c for c in cells if c.get("model") == model]
        ok_cells = [c for c in cells_m if c.get("ok")]
        passed = sum(1 for c in ok_cells if c.get("passed"))
        partials = [c.get("partial_score", 0.0) for c in ok_cells]
        mss = [c.get("ms", 0.0) for c in ok_cells]
        wall = sum(c.get("ms", 0) for c in cells_m) / 1000.0
        p_mean = (sum(partials) / len(partials)) if partials else 0.0
        p_std = _stat.stdev(partials) if len(partials) > 1 else 0.0
        m_mean = (sum(mss) / len(mss)) if mss else 0.0
        m_std = _stat.stdev(mss) if len(mss) > 1 else 0.0
        md.append(
            f"| `{model}` | {len(cells_m)} | {passed} | "
            f"{p_mean:.3f} | {p_std:.3f} | "
            f"{m_mean:.0f} | {m_std:.0f} | {wall:.1f} |"
        )

    (root / "quiz_summary.md").write_text("\n".join(md), encoding="utf-8")
    (root / "quiz_summary.json").write_text(json.dumps(cells, indent=2, ensure_ascii=False),
                                             encoding="utf-8")
    print(f"\nresults under: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
