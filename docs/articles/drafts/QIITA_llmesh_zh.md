---
title: llmesh 合集 — 本地/云端统一 × Prompt Firewall × Rust 加速 × 工业 IoT (Modbus/OPC-UA/DNP3 GOOSE) × P2P Swarm × 生态系统
tags: OpenAI, LLM, LLaMA, Anthropic, ollama
private: false
---

# llmesh 合集 — 本地/云端统一 × Prompt Firewall × Rust 加速 × 工业 IoT (Modbus/OPC-UA/DNP3 GOOSE) × P2P Swarm × 生态系统

<!-- TOPICNAV -->
> **🌐 语言**: [日本語](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762) | English | **中文** | 한국어
>
> **📚 FullSense 合集系列**
> - [llcore 验证 arc 合集](https://qiita.com/furuse-kazufumi/items/29b100b00f0d58306886)
> - [lldarwin / 进化 arc 合集](https://qiita.com/furuse-kazufumi/items/93f3cf1bb7b14650bbca)
> - [llive 完全解说合集](https://qiita.com/furuse-kazufumi/items/6da5a883fb2ed651edd8)
> - **llmesh 合集（this）**
> - [通俗版合集](https://qiita.com/furuse-kazufumi/items/fa0890f136636d495ea6)
<!-- /TOPICNAV -->

## 目录

1. [用「相同写法」处理本地 LLM 和云端 LLM 的 LLMesh — 30 秒就能跑起来的 Python 框架](#第1章-用相同写法处理本地-llm-和云端-llm-的-llmesh--30-秒就能跑起来的-python-框架)
2. [用 4 层统制「该往 LLM 的提示里放什么」— 我做了 LLMesh 的 Prompt Firewall](#第2章-用-4-层统制该往-llm-的提示里放什么-我做了-llmesh-的-prompt-firewall)
3. [比 Pure Python 快 6 倍的 Rust 扩展，外加流式重传、HTTP DoS 防护一并塞进去的 Python 库 — LLMesh 性能与可靠性的故事](#第3章-比-pure-python-快-6-倍的-rust-扩展外加流式重传http-dos-防护一并塞进去的-python-库--llmesh-性能与可靠性的故事)
4. [把本地 LLM × 工业 IoT × 提示防火墙装进一个 Python 框架 — 我做了 LLMesh v3.1.0 的故事](#第4章-把本地-llm--工业-iot--提示防火墙装进一个-python-框架--我做了-llmesh-v310-的故事)
5. [把 Modbus / OPC-UA / DNP3 / IEC 61850 GOOSE 都灌进一个 SensorEvent，用 CUSUM 抓异常并让 LLM 解释 — LLMesh 工业 IoT 篇](#第5章-把-modbus--opc-ua--dnp3--iec-61850-goose-都灌进一个-sensorevent用-cusum-抓异常并让-llm-解释--llmesh-工业-iot-篇)
6. [LLMesh: 做了一个用 MCP 安全连接 Local LLM 的 P2P Swarm PoC](#第6章-llmesh-做了一个用-mcp-安全连接-local-llm-的-p2p-swarm-poc)
7. [llmesh: 本地 LLM 集群 × 工业 IoT × 研究自动化](#第7章-llmesh-本地-llm-集群--工业-iot--研究自动化)


---

## 第1章 用「相同写法」处理本地 LLM 和云端 LLM 的 LLMesh — 30 秒就能跑起来的 Python 框架

<!-- KAMI -->
> 📖 **简单来说**
>
> 简单来说，本章讲的是「让在你自己电脑上跑的 AI，和网络那头的付费 AI，能用完全一样的方式调用」这件事。通常每个服务的接入方式和报错形式都各不相同，每换一家就得重写一遍代码。LLMesh 把这些差异吸收掉，让你在开发时用本地、上线时用云端这样的切换实质上只需 1 行。此外，即便不另起一个外部数据库，也能让文档检索（RAG）跑起来——这套机制只要 `pip install` 一发就附带过来了。
<!-- KAMI -->

:::note info
**📚 FullSense 知识库指南** <!-- fullsense-team-kb -->
FullSense 开发全史 60+ 篇文章（4 种语言版、故事化的阅读顺序指南、通俗易懂版、四格漫画）均已汇总至 Qiita Team **FullSense KB**（仅限团队成员）。
:::


> 用同一套 ABC 处理 Ollama / OpenAI / Azure / Anthropic / OpenRouter / Groq / Together / Mistral / DeepSeek
> `pip install llmesh-mcp`

---

#### 先跑起来（30 秒）

```bash
pip install llmesh-mcp
```

```python
### 无论哪家 LLM 都是相同的接口
from llmesh.llm import OllamaBackend

llm = OllamaBackend(model="llama3.2")          # 本地的话不需要 API 密钥
print(llm.complete("Pythonの`yield`を1行で説明して"))
```

切换到云端只需这些：

```python
from llmesh.llm import openai_backend

llm = openai_backend(api_key="sk-...", model="gpt-4o-mini")
print(llm.complete("Pythonの`yield`を1行で説明して"))
```

**调用代码一个字都不用改。** 这正是想要做到的点。

---

#### 有什么好处（只说 3 个）

1. **更换 backend 只要 1 行代码**：开发用本地 Ollama，生产用 OpenAI，验证用 Anthropic，压成本用 OpenRouter。
2. **错误类型、超时、重试都统一**：不必为每家供应商分别写 try/except。
3. **在 LLM 前后免费叠加安全层**：Prompt Firewall / OutputValidator / Audit Log 都可以**按需选配地插入**。

---

#### 支持的 backend 一览

| backend | 用途 | 需要的东西 |
|---|---|---|
| `OllamaBackend` | 本地 LLM | 先把 `ollama` 启动起来（`ollama serve`） |
| `LlamaCppBackend` | 本地 GGUF | `llama-cpp-python` |
| `openai_backend(...)` | OpenAI / Azure OpenAI / OpenRouter / Together / Groq / Mistral / DeepSeek（只要是 OpenAI 兼容 API 全都行） | API 密钥 |
| `anthropic_backend(...)` | Claude (Haiku / Sonnet / Opus) | API 密钥 |

**OpenAI 兼容 API 用一个函数全部吸收**，所以即便出了新的供应商，也只需改一下 `base_url` 就能用。

```python
### 经由 OpenRouter 比较多个模型
or_llm = openai_backend(
    api_key=OR_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="anthropic/claude-haiku-4-5",
)
```

---

#### 5 分钟跑通「第一个 RAG」

里面内置了一个外部 DB 为零、全部用 stdlib + numpy 跑起来的 RAG。

```python
from llmesh.rag import Retriever, MockEmbedder, NumpyVectorStore, Document

store = NumpyVectorStore(path="kb.npz")        # 持久化到 .npz
embedder = MockEmbedder(dim=128)               # 确定性哈希（零依赖）

### 放入文档
store.add([
    Document(id="d1", text="LLMesh はローカル LLM とクラウド LLM を同じ ABC で扱う"),
    Document(id="d2", text="PromptFirewall は注入・PII・シークレットを 4 層で塞ぐ"),
    Document(id="d3", text="SensorEvent は産業プロトコル 20+ を 1 つに統一する"),
], embedder=embedder)
store.save()

### 检索
retriever = Retriever(embedder=embedder, store=store)
hits = retriever.search("プロンプトインジェクション対策は？", k=2)
for h in hits:
    print(h.score, h.document.text)
```

实现成熟后可以**直接换成 Ollama Embedder**。

```python
from llmesh.rag import OllamaEmbedder
embedder = OllamaEmbedder(model="nomic-embed-text")  # 只用 urllib 就能跑
```

数据多起来后，从**三档存储**里挑选。

| 存储 | 条数参考 | 持久化 | 检索 |
|---|---:|---|---|
| `NumpyVectorStore` | 〜10⁵ | `.npz` | O(n) cosine |
| `SqliteVectorStore` | 〜10⁶ | sqlite3 (WAL) | O(n) cosine |
| `LSHVectorStore` | 10⁶〜 | `.npz` | LSH ANN（recall@10 ≥ 0.92） |

**不需要另起外部 DB** 正是其理念。不需要 Docker，也不需要 Postgres，`pip install` 即可全部搞定。

---

#### 带护栏地调用 LLM（推荐模式）

```python
from llmesh import PromptFirewall
from llmesh.llm import openai_backend

fw  = PromptFirewall(presidio_enabled=True)    # 启用 PII 层（需要 [presidio]）
llm = openai_backend(api_key=KEY, model="gpt-4o-mini")

def safe_complete(prompt: str) -> str:
    v = fw.check(prompt)
    if v.action == "BLOCK":
        raise PermissionError(f"blocked at {v.layer}: {v.reason}")
    if v.action == "SUMMARIZE":
        prompt = v.summarized          # PII 已占位符化
    return llm.complete(prompt)
```

**这 8 行**就能一并堵住「密钥泄露、提示注入、PII 外泄」。

---

#### 从 Claude Code / MCP 使用（可复制粘贴）

贴到 `claude_desktop_config.json` 或 Claude Code 的设置 JSON 里。

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

仅此而已，就能从 Claude Code 调用 `llmesh` 的 tool 群（读取传感器、SPC 判定、RAG 检索）。
**MCP 的输出必定会经过 OutputValidator**，因此也封堵了来自 tool 侧的输出注入。

---

#### 故障排查（常见卡点）

| 症状 | 原因 | 解决 |
|---|---|---|
| `ModuleNotFoundError: presidio_analyzer` | 未安装 extras | `pip install "llmesh-mcp[presidio]"` |
| `ModuleNotFoundError: numpy` | 用裸的 `pip install llmesh-mcp` 去用 RAG/SPC | `pip install "llmesh-mcp[rag]"` 或 `pip install numpy` |
| Ollama 连接失败 | 服务器未启动 | `ollama serve`，或在构造函数里指定 `base_url=` |
| 乱码（Windows） | 默认是 `cp932` | `set PYTHONUTF8=1`（PowerShell 是 `$env:PYTHONUTF8=1`） |
| OpenAI 兼容 API 的模型名通不过 | 供应商专属前缀 | 确认 `model="provider/model-name"` 格式 |

遇到问题先：

```bash
python -m llmesh.cli.doctor
```

这是一个专门往「把跑不起来的原因全部列出来」方向打造的诊断 CLI。**首次搭建时它最快**。

---

#### 路线图层面的当前位置

| ver | 加入了什么 |
|---|---|
| v2.13 | Presidio PII / RAG MVP / 多变量 SPC 核心 |
| v2.14 | ExplainedCUSUM / VideoCUSUM / SqliteVectorStore / DNP3 / GOOSE |
| v2.15 | LSHVectorStore（ANN）/ 公开 API 层 / `API_STABILITY.md` |
| v2.16 | OWASP 静态审计干净 |
| v2.17 | HTTP DoS hardening（给所有 HTTP 客户端加响应大小上限） |
| v2.18 | 8 种文档新增（CONTRIBUTING / DEPLOYMENT / OBSERVABILITY / TROUBLESHOOTING …） |
| v3.0.0 | **API Stability Release**（正式采用 SemVer，`__all__` 契约化） |
| **v3.1.0** | **云端 LLM 集成（OpenAI / Azure / Anthropic / OpenRouter / Together / Groq / Mistral / DeepSeek）** |

**从 v3.0.0 起正式采用 SemVer**。`docs/API_STABILITY.md` 中的公开符号清单就是契约（minor 向后兼容，仅 major 做破坏性变更）。

---

#### 下一步

```bash
### 想看看到底跑得起来哪些东西
pip install "llmesh-mcp[industrial,vision,presidio,rag]"
python -m llmesh.cli.doctor
python -m llmesh.cli.status

### 先跑 Quickstart 脚本
python -c "from llmesh.llm import OllamaBackend; print(OllamaBackend(model='llama3.2').complete('hi'))"
```

- GitHub: <https://github.com/furuse-kazufumi/llmesh>
- PyPI: <https://pypi.org/project/llmesh-mcp/>
- License: MIT
- 欢迎 Issue: <https://github.com/furuse-kazufumi/llmesh/issues>

---

#### 结语

「本地和云端用同一套接口」「安全层可以事后插入」「不要外部 DB 也能跑 RAG」——单凭这 3 点，就能让你从最初的 LLM 原型一路到生产**用同一份代码扩展上去**，这正是这个框架的目标。
欢迎 PR / Issue / 「想要某某 backend」「想要某某向量 DB」。
