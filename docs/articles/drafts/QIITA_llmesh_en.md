---
title: llmesh Digest — Unified Local/Cloud × Prompt Firewall × Rust Acceleration × Industrial IoT (Modbus/OPC-UA/DNP3 GOOSE) × P2P Swarm × Ecosystem
tags: OpenAI, LLM, LLaMA, Anthropic, ollama
private: false
---

# llmesh Digest — Unified Local/Cloud × Prompt Firewall × Rust Acceleration × Industrial IoT (Modbus/OPC-UA/DNP3 GOOSE) × P2P Swarm × Ecosystem

<!-- TOPICNAV -->
> **🌐 Language**: [日本語](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762) | **English** | 中文 | 한국어
>
> **📚 FullSense Digest Series**
> - [llcore Verification Arc](https://qiita.com/furuse-kazufumi/items/525cd01eda5c1ad707ef)
> - [lldarwin / Evolution Arc](https://qiita.com/furuse-kazufumi/items/e49b7ab9027d93594402)
> - [llive Complete Guide](https://qiita.com/furuse-kazufumi/items/07b686ea311e06027f94)
> - **llmesh Digest（this）**
> - [Plain-Language Digest](https://qiita.com/furuse-kazufumi/items/bdfad6db3f2e70c40511)
<!-- /TOPICNAV -->

## Contents

1. [LLMesh for People Who Want to Use Local LLMs and Cloud LLMs "the Same Way" — A Python Framework You Can Run in 30 Seconds](#chapter-1-llmesh-for-people-who-want-to-use-local-llms-and-cloud-llms-the-same-way--a-python-framework-you-can-run-in-30-seconds)
2. [Governing "What You May Pass to an LLM Prompt" in 4 Layers — I Built LLMesh's Prompt Firewall](#chapter-2-governing-what-you-may-pass-to-an-llm-prompt-in-4-layers--i-built-llmeshs-prompt-firewall)
3. [A Rust Extension 6× Faster Than Pure Python, Plus Streaming Retransmission and HTTP DoS Defenses — The Performance and Reliability Story of LLMesh](#chapter-3-a-rust-extension-6-faster-than-pure-python-plus-streaming-retransmission-and-http-dos-defenses--the-performance-and-reliability-story-of-llmesh)
4. [Local LLM × Industrial IoT × Prompt Firewall in One Python Framework — The Story of Building LLMesh v3.1.0](#chapter-4-local-llm--industrial-iot--prompt-firewall-in-one-python-framework--the-story-of-building-llmesh-v310)
5. [Pouring Modbus / OPC-UA / DNP3 / IEC 61850 GOOSE into a Single SensorEvent, Catching Anomalies with CUSUM, and Letting the LLM Explain Them — LLMesh Industrial IoT Edition](#chapter-5-pouring-modbus--opc-ua--dnp3--iec-61850-goose-into-a-single-sensorevent-catching-anomalies-with-cusum-and-letting-the-llm-explain-them--llmesh-industrial-iot-edition)
6. [LLMesh: I Built a P2P Swarm PoC That Safely Connects Local LLMs over MCP](#chapter-6-llmesh-i-built-a-p2p-swarm-poc-that-safely-connects-local-llms-over-mcp)
7. [llmesh: Local LLM Swarm × Industrial IoT × Research Automation](#chapter-7-llmesh-local-llm-swarm--industrial-iot--research-automation)


---

## Chapter 1 LLMesh for People Who Want to Use Local LLMs and Cloud LLMs "the Same Way" — A Python Framework You Can Run in 30 Seconds

<!-- KAMI -->
> 📖 **In a nutshell**
>
> In a nutshell, this chapter is about "making it so that the AI running on your own PC and the paid AI on the far side of the internet can both be used with exactly the same way of calling them." Normally, the connection method and the way errors surface differ from service to service, so every time you switch you end up rewriting your code. LLMesh absorbs that difference, so swapping between, say, local during development and cloud in production takes effectively one line. As a bonus, it even ships — with a single `pip install` — a mechanism that runs document search (RAG) without standing up an external database.
<!-- KAMI -->

:::note info
**📚 FullSense Knowledge Base** <!-- fullsense-team-kb -->
The full FullSense development history — 60+ articles in 4 languages, with a story-based reading guide, plain-language editions, and 4-panel manga — is consolidated in our Qiita Team **FullSense KB** (team members only).
:::


> Ollama / OpenAI / Azure / Anthropic / OpenRouter / Groq / Together / Mistral / DeepSeek — all under the same ABC
> `pip install llmesh-mcp`

---

#### Run it first (30 seconds)

```bash
pip install llmesh-mcp
```

```python
### The same interface for any LLM
from llmesh.llm import OllamaBackend

llm = OllamaBackend(model="llama3.2")          # no API key needed if local
print(llm.complete("Explain Python's `yield` in one line"))
```

Switching to the cloud is just this.

```python
from llmesh.llm import openai_backend

llm = openai_backend(api_key="sk-...", model="gpt-4o-mini")
print(llm.complete("Explain Python's `yield` in one line"))
```

**The calling code does not change by a single character.** That was the whole point.

---

#### What's nice about it (just 3 things)

1. **Swapping backends is one line of code**: develop on local Ollama, run production on OpenAI, validate on Anthropic, squeeze costs with OpenRouter.
2. **Error types, timeouts, and retries are unified**: no need to write per-provider try/except.
3. **A security layer rides on the LLM for free**: Prompt Firewall / OutputValidator / Audit Log can be **inserted optionally**.

---

#### List of supported backends

| backend | Use | What you need |
|---|---|---|
| `OllamaBackend` | Local LLM | Have `ollama` running (`ollama serve`) |
| `LlamaCppBackend` | Local GGUF | `llama-cpp-python` |
| `openai_backend(...)` | OpenAI / Azure OpenAI / OpenRouter / Together / Groq / Mistral / DeepSeek (any OpenAI-compatible API) | API key |
| `anthropic_backend(...)` | Claude (Haiku / Sonnet / Opus) | API key |

**OpenAI-compatible APIs are absorbed by a single function**, so when a new provider appears you can use it just by changing `base_url`.

```python
### Compare multiple models via OpenRouter
or_llm = openai_backend(
    api_key=OR_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="anthropic/claude-haiku-4-5",
)
```

---

#### "Your first RAG" in 5 minutes

It includes a RAG that runs with zero external DB — all stdlib + numpy.

```python
from llmesh.rag import Retriever, MockEmbedder, NumpyVectorStore, Document

store = NumpyVectorStore(path="kb.npz")        # persisted to .npz
embedder = MockEmbedder(dim=128)               # deterministic hash (zero dependencies)

### Insert documents
store.add([
    Document(id="d1", text="LLMesh treats local LLMs and cloud LLMs under the same ABC"),
    Document(id="d2", text="PromptFirewall blocks injection, PII, and secrets in 4 layers"),
    Document(id="d3", text="SensorEvent unifies 20+ industrial protocols into one"),
], embedder=embedder)
store.save()

### Search
retriever = Retriever(embedder=embedder, store=store)
hits = retriever.search("What are the countermeasures for prompt injection?", k=2)
for h in hits:
    print(h.score, h.document.text)
```

Once your implementation matures, you can **swap it straight over to the Ollama Embedder**.

```python
from llmesh.rag import OllamaEmbedder
embedder = OllamaEmbedder(model="nomic-embed-text")  # runs on urllib alone
```

As your data grows, you choose from **three tiers of stores**.

| Store | Rough count | Persistence | Search |
|---|---:|---|---|
| `NumpyVectorStore` | ~10⁵ | `.npz` | O(n) cosine |
| `SqliteVectorStore` | ~10⁶ | sqlite3 (WAL) | O(n) cosine |
| `LSHVectorStore` | 10⁶~ | `.npz` | LSH ANN (recall@10 ≥ 0.92) |

**No need to stand up an external DB** — that's the concept. No Docker, no Postgres; it's self-contained via `pip install`.

---

#### Calling an LLM with a guard (recommended pattern)

```python
from llmesh import PromptFirewall
from llmesh.llm import openai_backend

fw  = PromptFirewall(presidio_enabled=True)    # enable the PII layer (requires [presidio])
llm = openai_backend(api_key=KEY, model="gpt-4o-mini")

def safe_complete(prompt: str) -> str:
    v = fw.check(prompt)
    if v.action == "BLOCK":
        raise PermissionError(f"blocked at {v.layer}: {v.reason}")
    if v.action == "SUMMARIZE":
        prompt = v.summarized          # PII already turned into placeholders
    return llm.complete(prompt)
```

**These 8 lines** block "secret leaks, prompt injection, PII exfiltration" in one set.

---

#### Using it from Claude Code / MCP (copy-paste)

Paste this into `claude_desktop_config.json` or Claude Code's settings JSON.

```json
{
  "mcpServers": {
    "llmesh": {
      "command": "python",
      "args": ["-m", "llmesh", "serve-mcp"],
      "env": {
        "LLMESH_BACKEND": "ollama",
        "LLMESH_MODEL": "llama3.2"
      }
    }
  }
}
```

That alone lets Claude Code call `llmesh`'s tool set (sensor reads, SPC checks, RAG search).
**MCP output always passes through OutputValidator**, so output injection from the tool side is sealed off too.

---

#### Troubleshooting (common sticking points)

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError: presidio_analyzer` | extras not installed | `pip install "llmesh-mcp[presidio]"` |
| `ModuleNotFoundError: numpy` | used RAG/SPC with a bare `pip install llmesh-mcp` | `pip install "llmesh-mcp[rag]"` or `pip install numpy` |
| Ollama connection failure | server not running | `ollama serve`, or pass `base_url=` to the constructor |
| Mojibake (Windows) | `cp932` is the default | `set PYTHONUTF8=1` (PowerShell: `$env:PYTHONUTF8=1`) |
| Model name not accepted by an OpenAI-compatible API | provider-specific prefix | check the `model="provider/model-name"` format |

When stuck, first run:

```bash
python -m llmesh.cli.doctor
```

A diagnostic CLI tuned to "print every reason it isn't working." **This is the fastest path through initial setup.**

---

#### Where we are, roadmap-wise

| ver | What it added |
|---|---|
| v2.13 | Presidio PII / RAG MVP / multivariate SPC core |
| v2.14 | ExplainedCUSUM / VideoCUSUM / SqliteVectorStore / DNP3 / GOOSE |
| v2.15 | LSHVectorStore (ANN) / public API layer / `API_STABILITY.md` |
| v2.16 | OWASP static-audit clean |
| v2.17 | HTTP DoS hardening (response-size cap on every HTTP client) |
| v2.18 | 8 new docs (CONTRIBUTING / DEPLOYMENT / OBSERVABILITY / TROUBLESHOOTING …) |
| v3.0.0 | **API Stability Release** (SemVer formally applied, `__all__` contracted) |
| **v3.1.0** | **Cloud LLM integration (OpenAI / Azure / Anthropic / OpenRouter / Together / Groq / Mistral / DeepSeek)** |

**SemVer is formally applied from v3.0.0.** The list of public symbols in `docs/API_STABILITY.md` is the contract (minor = backward-compatible, only major = breaking changes).

---

#### Next steps

```bash
### Want to see everything that works
pip install "llmesh-mcp[industrial,vision,presidio,rag]"
python -m llmesh.cli.doctor
python -m llmesh.cli.status

### Try the Quickstart script first
python -c "from llmesh.llm import OllamaBackend; print(OllamaBackend(model='llama3.2').complete('hi'))"
```

- GitHub: <https://github.com/furuse-kazufumi/llmesh>
- PyPI: <https://pypi.org/project/llmesh-mcp/>
- License: MIT
- Issues welcome: <https://github.com/furuse-kazufumi/llmesh/issues>

---

#### In closing

"Local and cloud through the same interface," "a security layer you can slot in later," "RAG that runs with no external DB" — even just these three points let you **scale from your first LLM prototype to production with the same code**. That is the aim of this framework.
PRs / Issues / "I want a ○○ backend" / "I want a △△ vector DB" are all welcome.
