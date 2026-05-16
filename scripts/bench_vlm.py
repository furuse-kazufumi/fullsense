#!/usr/bin/env python3
"""bench_vlm.py — Vision Language Model A/B runner.

Same shape as bench_run.py but for VLM (image-in, text-out). Targets the
6-VLM panel — Anthropic Claude (vision), Gemini Flash (vision), OpenAI
GPT-4o-mini (vision), Perplexity sonar-pro-vision (when available),
ollama llava, ollama llama3.2-vision.

For 2026-05-16 the only working VLM is `ollama llava` (cloud keys all
errored — see docs/benchmarks/2026-05-16_vlm.md). The script still tries
all six so reports show which credentials need restoration.

Usage::

    python3 scripts/bench_vlm.py --image docs/assets/images/og-card.png \
        --question "Describe this image in 2 sentences."

    # All 6 VLMs in parallel
    python3 scripts/bench_vlm.py --image <path> --question <text> --all

    # Just one
    python3 scripts/bench_vlm.py --image <path> --question <text> --model llava
"""

from __future__ import annotations

import argparse
import base64
import io
import json
import os
import pathlib
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Callable

if isinstance(sys.stdout, io.TextIOWrapper):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def load_keys() -> dict:
    p = pathlib.Path("D:/api-keys.json")
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {k: os.environ.get(k, "") for k in
            ("ANTHROPIC_API_KEY", "GEMINI_API_KEY", "OPENAI_API_KEY", "PERPLEXITY_API_KEY")}


def _post(url, headers, data, timeout=120):
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"),
                                  headers={"Content-Type": "application/json", **headers})
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return True, r.status, r.read().decode("utf-8"), (time.perf_counter() - t0) * 1000
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else str(e)
        return False, e.code, body, (time.perf_counter() - t0) * 1000
    except Exception as e:
        return False, 0, str(e), (time.perf_counter() - t0) * 1000


def run_anthropic(img_b64: str, q: str, keys: dict) -> tuple[bool, str, float]:
    key = keys.get("ANTHROPIC_API_KEY", "")
    if not key:
        return False, "ANTHROPIC_API_KEY missing", 0.0
    model = os.environ.get("BENCH_ANTHROPIC_VLM", "claude-haiku-4-5-20251001")
    ok, _code, body, ms = _post(
        "https://api.anthropic.com/v1/messages",
        {"x-api-key": key, "anthropic-version": "2023-06-01"},
        {"model": model, "max_tokens": 600,
         "messages": [{"role": "user", "content": [
             {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
             {"type": "text", "text": q},
         ]}]},
    )
    if ok:
        try:
            d = json.loads(body)
            return True, "".join(b.get("text", "") for b in d.get("content", [])), ms
        except Exception as e:
            return False, f"json parse: {e}", ms
    return False, body[:300], ms


def run_gemini(img_b64: str, q: str, keys: dict) -> tuple[bool, str, float]:
    key = keys.get("GEMINI_API_KEY", "")
    if not key:
        return False, "GEMINI_API_KEY missing", 0.0
    model = os.environ.get("BENCH_GEMINI_VLM", "gemini-2.0-flash")
    ok, _code, body, ms = _post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}",
        {},
        {"contents": [{"parts": [
            {"text": q},
            {"inline_data": {"mime_type": "image/png", "data": img_b64}},
        ]}], "generationConfig": {"temperature": 0.2, "maxOutputTokens": 600}},
    )
    if ok:
        try:
            d = json.loads(body)
            txt = d.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "")
            return True, txt, ms
        except Exception as e:
            return False, f"json parse: {e}", ms
    return False, body[:300], ms


def run_openai(img_b64: str, q: str, keys: dict) -> tuple[bool, str, float]:
    key = keys.get("OPENAI_API_KEY", "")
    if not key:
        return False, "OPENAI_API_KEY missing", 0.0
    model = os.environ.get("BENCH_OPENAI_VLM", "gpt-4o-mini")
    ok, _code, body, ms = _post(
        "https://api.openai.com/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {"model": model, "max_tokens": 600,
         "messages": [{"role": "user", "content": [
             {"type": "text", "text": q},
             {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
         ]}]},
    )
    if ok:
        try:
            d = json.loads(body)
            return True, d.get("choices", [{}])[0].get("message", {}).get("content", ""), ms
        except Exception as e:
            return False, f"json parse: {e}", ms
    return False, body[:300], ms


def _ollama_vlm(model: str, img_b64: str, q: str) -> tuple[bool, str, float]:
    ok, _code, body, ms = _post(
        "http://localhost:11434/api/generate", {},
        {"model": model, "prompt": q, "images": [img_b64], "stream": False,
         "options": {"temperature": 0.2, "num_predict": 600}},
        timeout=300,
    )
    if ok:
        try:
            return True, json.loads(body).get("response", ""), ms
        except Exception as e:
            return False, f"json parse: {e}", ms
    return False, body[:300], ms


def run_ollama_llava(img_b64: str, q: str, _keys: dict) -> tuple[bool, str, float]:
    return _ollama_vlm(os.environ.get("BENCH_OLLAMA_VLM_LLAVA", "llava:7b"), img_b64, q)


def run_ollama_l32v(img_b64: str, q: str, _keys: dict) -> tuple[bool, str, float]:
    return _ollama_vlm(os.environ.get("BENCH_OLLAMA_VLM_LLAMA32V", "llama3.2-vision"), img_b64, q)


VLM: dict[str, Callable[[str, str, dict], tuple[bool, str, float]]] = {
    "anthropic":     run_anthropic,
    "gemini":        run_gemini,
    "openai":        run_openai,
    "llava":         run_ollama_llava,
    "llama32vision": run_ollama_l32v,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--image", type=pathlib.Path, required=True, help="image file (PNG)")
    parser.add_argument("--question", required=True, help="question text")
    parser.add_argument("--model", action="append", choices=sorted(VLM) + ["all"], help="VLM to run (repeatable)")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--out", type=pathlib.Path, default=None, help="output dir for raw responses")
    parser.add_argument("--parallel", type=int, default=3)
    args = parser.parse_args(argv)

    if args.all or not args.model:
        models = sorted(VLM)
    elif "all" in args.model:
        models = sorted(VLM)
    else:
        models = args.model

    img = args.image.read_bytes()
    img_b64 = base64.b64encode(img).decode("ascii")
    keys = load_keys()

    today = time.strftime("%Y-%m-%d")
    root = args.out or pathlib.Path(f"D:/projects/fullsense/docs/benchmarks/{today}-vlm")
    root.mkdir(parents=True, exist_ok=True)
    (root / "_question.txt").write_text(args.question, encoding="utf-8")
    (root / "_image.png").write_bytes(img)

    print(f"bench_vlm.py: image={args.image}({len(img)} bytes) models={models} out={root}")

    summary = []
    with ThreadPoolExecutor(max_workers=args.parallel) as ex:
        futs = {ex.submit(VLM[m], img_b64, args.question, keys): m for m in models}
        for fut in as_completed(futs):
            m = futs[fut]
            ok, txt, ms = fut.result()
            (root / f"{m}.txt").write_text(txt, encoding="utf-8")
            status = "OK " if ok else "ERR"
            print(f"  [{status}] {m:14} {ms:7.0f} ms  {len(txt):5d} chars")
            summary.append((m, status, ms, len(txt)))

    print(f"\nresults under: {root}")
    fails = sum(1 for r in summary if r[1] == "ERR")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
