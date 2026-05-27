# LinkedIn Post — 2026-05-17 Engineering Summary (English)

🚀 **32 requirements + 2,200 LoC + 78 tests + 4 benchmarks in a single day — Building llive, a self-evolving modular memory LLM framework**

Today (2026-05-17), the self-evolving modular memory LLM framework **llive** progressed as follows:

✅ **Brief API end-to-end shipped** — Structured work-unit API for external clients (lldesign / lltrade / MCP). Schema / loader / ledger / runner / CLI / MCP all implemented in a single session (5-day estimate finished in 1 day).
✅ **+32 requirements** — v0.7-MATH 8 / v0.8-CABT 7 / v0.9-CREAT 5 / v1.0-COG-FX 4 / v2.0-ORG-FX 8.
✅ **Tests: 936 → 1,014 PASS / 0 fail / 0 regression**
✅ **4 benchmark families** — progressive matrix 15 cells / fair re-bench / quiz Debug + Release (with mean / stdev statistics).
✅ **Honest disclosure** — Initial benchmark showed llive at 134-184 ms (4/4 OK), suspiciously fast. Investigation revealed an unwired LLMBackend (template fallback). Lesson stored in memory; fair re-run (32-51 s) published openly.

💡 **Key insight**: "llive's value is structure (ledger / approval / governance / grounding / 6-stage trace), not speed." Positioning: "Run Qwen / Llama / Mistral safely and accountably on your local PC."

📊 **Progressive matrix highlights** (xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b}, on-prem only):
- Brief API overhead < 1 %
- All 15 cells decision=note (loop is stable under token pressure)

🔗 Full articles (11 + 2 integrated) and raw data:
<https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17>

#LLM #Agent #OnPrem #Ollama #Python

Author: Kazufumi Furuse (puruyan)
