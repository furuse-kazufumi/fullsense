#!/usr/bin/env python3
"""bench_run.py — re-run the FullSense A/B benchmark suite.

Replays the 4 Briefs from 2026-05-16 (or any --brief subset) against the
6-model panel (llive, ollama, Anthropic, Gemini, OpenAI Codex, Perplexity),
writes each model's raw response under docs/benchmarks/<date>/<bN>/, and
prints a one-line PASS/FAIL summary per cell.

Models that error (quota, missing CLI, etc.) are reported as 'skip' so the
matrix stays comparable across runs.

Usage::

    # Re-run all 4 Briefs against all 6 models, write under
    # docs/benchmarks/<YYYY-MM-DD>/.
    python3 scripts/bench_run.py --all

    # Just one Brief, one model.
    python3 scripts/bench_run.py --brief b3 --model perplexity

    # Custom output dir (don't overwrite the 2026-05-16 snapshot).
    python3 scripts/bench_run.py --all --out docs/benchmarks/2026-06-01/

Briefs are read from docs/benchmarks/2026-05-16{,_b2,_b3,_b4}/_brief.txt.

Requires: Python 3.11, ollama running on localhost:11434 (for ollama),
codex CLI on PATH (for codex), and D:/api-keys.json or env vars for cloud
keys.
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
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

# Force UTF-8 stdout so Windows cp932 doesn't crash on em dashes / 日本語.
if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = pathlib.Path("D:/projects/fullsense")
BENCH_ROOT = ROOT / "docs/benchmarks"

# Brief id -> brief text source dir (from 2026-05-16 snapshot)
BRIEF_SOURCES = {
    "b1": BENCH_ROOT / "2026-05-16" / "_brief.txt",
    "b2": BENCH_ROOT / "2026-05-16-b2" / "_brief.txt",
    "b3": BENCH_ROOT / "2026-05-16-b3" / "_brief.txt",
    "b4": BENCH_ROOT / "2026-05-16-b4" / "_brief.txt",
}


def load_keys() -> dict:
    """API keys from D:/api-keys.json, fallback to env."""
    p = pathlib.Path("D:/api-keys.json")
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {
        "ANTHROPIC_API_KEY": os.environ.get("ANTHROPIC_API_KEY", ""),
        "GEMINI_API_KEY": os.environ.get("GEMINI_API_KEY", ""),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY", ""),
        "PERPLEXITY_API_KEY": os.environ.get("PERPLEXITY_API_KEY", ""),
    }


def _post(url: str, headers: dict, data: dict, timeout: int = 90) -> tuple[bool, int, str, float]:
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8")
            return True, r.status, body, (time.perf_counter() - t0) * 1000
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return False, e.code, body, (time.perf_counter() - t0) * 1000
    except Exception as e:
        return False, 0, str(e), (time.perf_counter() - t0) * 1000


# ── per-model runners ─────────────────────────────────────────────────────
# Each returns (ok: bool, response_text: str, elapsed_ms: float).

def run_llive(brief: str, _keys: dict) -> tuple[bool, str, float]:
    """Run a Brief through llive with a real LLM backend attached.

    Fair-benchmark contract (per feedback_benchmark_honest_disclosure,
    2026-05-17): llive must call an actual LLM, not template fallback.
    The default backend here is `ollama:qwen2.5:14b` — change via env
    BENCH_LLIVE_BACKEND.

    Response text returned to the caller is `stages.thought.text` (the
    actual LLM-generated monologue), not the JSON envelope, so the chars
    column is measured fairly.
    """
    backend = os.environ.get("BENCH_LLIVE_BACKEND", "ollama:qwen2.5:14b")
    t0 = time.perf_counter()
    try:
        p = subprocess.run(
            [
                "py", "-3.11", "D:/projects/llive/scripts/run_brief.py",
                "--json", "--backend", backend, brief,
            ],
            capture_output=True, text=True, encoding="utf-8", timeout=1800,
        )
        ms = (time.perf_counter() - t0) * 1000
        if p.returncode != 0:
            return False, p.stderr or p.stdout, ms
        try:
            obj = json.loads(p.stdout)
            thought = (
                obj.get("stages", {}).get("thought", {}).get("text")
                or p.stdout
            )
        except Exception:
            thought = p.stdout
        return True, thought, ms
    except FileNotFoundError:
        return False, "py launcher not found (install Python from python.org)", 0.0
    except Exception as e:
        return False, f"llive subprocess error: {e}", 0.0


def run_ollama(brief: str, _keys: dict) -> tuple[bool, str, float]:
    model = os.environ.get("BENCH_OLLAMA_MODEL", "llama3.2")
    ok, _code, body, ms = _post(
        "http://localhost:11434/api/generate", {},
        {"model": model, "prompt": brief, "stream": False,
         "options": {"temperature": 0.2, "num_predict": 1200}},
        timeout=180,
    )
    if ok:
        try:
            return True, json.loads(body).get("response", ""), ms
        except Exception as e:
            return False, f"json parse: {e}", ms
    return False, f"http error: {body[:300]}", ms


def run_anthropic(brief: str, keys: dict) -> tuple[bool, str, float]:
    key = keys.get("ANTHROPIC_API_KEY", "")
    if not key:
        return False, "ANTHROPIC_API_KEY missing", 0.0
    model = os.environ.get("BENCH_ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
    ok, _code, body, ms = _post(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": key, "anthropic-version": "2023-06-01"},
        {"model": model, "max_tokens": 1200,
         "messages": [{"role": "user", "content": brief}]},
    )
    if ok:
        try:
            d = json.loads(body)
            return True, "".join(b.get("text", "") for b in d.get("content", [])), ms
        except Exception as e:
            return False, f"json parse: {e}", ms
    return False, body[:300], ms


def run_gemini(brief: str, keys: dict) -> tuple[bool, str, float]:
    key = keys.get("GEMINI_API_KEY", "")
    if not key:
        return False, "GEMINI_API_KEY missing", 0.0
    model = os.environ.get("BENCH_GEMINI_MODEL", "gemini-2.0-flash")
    ok, _code, body, ms = _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
        {},
        {"contents": [{"parts": [{"text": brief}]}],
         "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1200}},
    )
    if ok:
        try:
            d = json.loads(body)
            text = d.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return True, text, ms
        except Exception as e:
            return False, f"json parse: {e}", ms
    return False, body[:300], ms


def run_perplexity(brief: str, keys: dict) -> tuple[bool, str, float]:
    key = keys.get("PERPLEXITY_API_KEY", "")
    if not key:
        return False, "PERPLEXITY_API_KEY missing", 0.0
    model = os.environ.get("BENCH_PERPLEXITY_MODEL", "sonar")
    ok, _code, body, ms = _post(
        "https://api.perplexity.ai/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {"model": model, "messages": [{"role": "user", "content": brief}],
         "temperature": 0.2, "max_tokens": 1200},
    )
    if ok:
        try:
            d = json.loads(body)
            return True, d.get("choices", [{}])[0].get("message", {}).get("content", ""), ms
        except Exception as e:
            return False, f"json parse: {e}", ms
    return False, body[:300], ms


def run_codex(brief: str, _keys: dict) -> tuple[bool, str, float]:
    # `codex exec` reads prompt from stdin.
    t0 = time.perf_counter()
    try:
        p = subprocess.run(
            ["codex", "exec", "--skip-git-repo-check"],
            input=brief, capture_output=True, text=True, encoding="utf-8",
            timeout=120,
        )
        ms = (time.perf_counter() - t0) * 1000
        out = p.stdout + ("\nSTDERR:\n" + p.stderr if p.returncode != 0 and p.stderr else "")
        return p.returncode == 0, out, ms
    except FileNotFoundError:
        return False, "codex CLI not on PATH", 0.0
    except Exception as e:
        return False, f"codex error: {e}", 0.0


MODELS: dict[str, Callable[[str, dict], tuple[bool, str, float]]] = {
    "llive": run_llive,
    "ollama": run_ollama,
    "anthropic": run_anthropic,
    "gemini": run_gemini,
    "perplexity": run_perplexity,
    "codex": run_codex,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", action="append", choices=sorted(BRIEF_SOURCES) + ["all"],
                        help="Brief id to run (repeatable). 'all' = all 4. Default: all")
    parser.add_argument("--model", action="append", choices=sorted(MODELS) + ["all"],
                        help="Model to run (repeatable). 'all' = all 6. Default: all")
    parser.add_argument("--out", type=pathlib.Path, default=None,
                        help="Output directory root (default: docs/benchmarks/<today>/)")
    parser.add_argument("--all", action="store_true",
                        help="Shortcut for --brief all --model all")
    parser.add_argument("--parallel", type=int, default=3,
                        help="Concurrent model calls per Brief (default: 3)")
    args = parser.parse_args(argv)

    if args.all or not args.brief:
        briefs = sorted(BRIEF_SOURCES)
    elif "all" in args.brief:
        briefs = sorted(BRIEF_SOURCES)
    else:
        briefs = args.brief

    if args.all or not args.model:
        models = sorted(MODELS)
    elif "all" in args.model:
        models = sorted(MODELS)
    else:
        models = args.model

    keys = load_keys()
    today = time.strftime("%Y-%m-%d")
    root = args.out or (BENCH_ROOT / today)

    print(f"bench_run.py: briefs={briefs} models={models} out={root}")

    summary: list[tuple[str, str, str, float, int]] = []  # (brief, model, status, ms, chars)
    for bid in briefs:
        src = BRIEF_SOURCES[bid]
        if not src.exists():
            print(f"!! brief source missing: {src}")
            continue
        brief = src.read_text(encoding="utf-8").strip()
        out_dir = root / bid
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "_brief.txt").write_text(brief, encoding="utf-8")
        print(f"\n=== {bid} ({len(brief)} chars) ===")

        with ThreadPoolExecutor(max_workers=args.parallel) as ex:
            futs = {ex.submit(MODELS[m], brief, keys): m for m in models}
            for fut in as_completed(futs):
                m = futs[fut]
                ok, txt, ms = fut.result()
                (out_dir / f"{m}.txt").write_text(txt, encoding="utf-8")
                status = "OK " if ok else "ERR"
                print(f"  [{status}] {m:11} {ms:7.0f} ms  {len(txt):5d} chars")
                summary.append((bid, m, status, ms, len(txt)))

    # Final matrix
    print("\n=== matrix ===")
    print(f"{'brief':<5} {'model':<11} {'status':<6} {'ms':>7} {'chars':>7}")
    for row in summary:
        print(f"{row[0]:<5} {row[1]:<11} {row[2]:<6} {row[3]:>7.0f} {row[4]:>7d}")

    fails = sum(1 for r in summary if r[2] == "ERR")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
