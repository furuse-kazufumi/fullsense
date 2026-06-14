---
title: llmesh 모음 — 로컬/클라우드 통합 × Prompt Firewall × Rust 고속화 × 산업 IoT (Modbus/OPC-UA/DNP3 GOOSE) × P2P Swarm × 에코시스템
tags: OpenAI, LLM, LLaMA, Anthropic, ollama
private: false
---

# llmesh 모음 — 로컬/클라우드 통합 × Prompt Firewall × Rust 고속화 × 산업 IoT (Modbus/OPC-UA/DNP3 GOOSE) × P2P Swarm × 에코시스템

<!-- TOPICNAV -->
> **🌐 언어**: [日本語](https://qiita.com/furuse-kazufumi/items/fcb43968a5c642610762) | English | 中文 | **한국어**
>
> **📚 FullSense 모음 시리즈**
> - [llcore 검증 arc 모음](https://qiita.com/furuse-kazufumi/items/a5ebb3992e4c28862f47)
> - [lldarwin / 진화 arc 모음](https://qiita.com/furuse-kazufumi/items/951b94cf66d246723004)
> - [llive 완전 해설 모음](https://qiita.com/furuse-kazufumi/items/c5f2077a3399d3fc9b26)
> - **llmesh 모음（this）**
> - [쉬운 설명 모음](https://qiita.com/furuse-kazufumi/items/e5093e4816b25c1bd4d0)
<!-- /TOPICNAV -->

## 목차

1. [로컬 LLM 과 클라우드 LLM 을 「같은 작성법」으로 다루고 싶은 사람을 위한 LLMesh — 30 초로 실행 가능한 Python 프레임워크](#제1장-로컬-llm-과-클라우드-llm-을-같은-작성법으로-다루고-싶은-사람을-위한-llmesh--30-초로-실행-가능한-python-프레임워크)
2. [LLM 의 프롬프트에 「무엇을 넘겨도 되는가」를 4 층으로 통제한다 — LLMesh 의 Prompt Firewall 을 만들었다](#제2장-llm-의-프롬프트에-무엇을-넘겨도-되는가를-4-층으로-통제한다--llmesh-의-prompt-firewall-을-만들었다)
3. [Pure Python 의 6 배 빠른 Rust 확장과, 스트리밍 재전송・HTTP DoS 대책까지 담은 Python 라이브러리 — LLMesh 성능과 신뢰성 이야기](#제3장-pure-python-의-6-배-빠른-rust-확장과-스트리밍-재전송http-dos-대책까지-담은-python-라이브러리--llmesh-성능과-신뢰성-이야기)
4. [로컬 LLM × 산업 IoT × 프롬프트 파이어월을 1 개의 Python 프레임워크로 — LLMesh v3.1.0 을 만든 이야기](#제4장-로컬-llm--산업-iot--프롬프트-파이어월을-1-개의-python-프레임워크로--llmesh-v310-을-만든-이야기)
5. [Modbus / OPC-UA / DNP3 / IEC 61850 GOOSE 를 1 개의 SensorEvent 에 흘려넣고, CUSUM 으로 이상을 잡아 LLM 에게 설명시킨다 — LLMesh 산업 IoT 편](#제5장-modbus--opc-ua--dnp3--iec-61850-goose-를-1-개의-sensorevent-에-흘려넣고-cusum-으로-이상을-잡아-llm-에게-설명시킨다--llmesh-산업-iot-편)
6. [LLMesh: Local LLM 을 MCP 로 안전하게 연결하는 P2P Swarm PoC 를 만들었다](#제6장-llmesh-local-llm-을-mcp-로-안전하게-연결하는-p2p-swarm-poc-를-만들었다)
7. [llmesh: 로컬 LLM 스웜 × 산업 IoT × 연구 자동화](#제7장-llmesh-로컬-llm-스웜--산업-iot--연구-자동화)


---

## 제1장 로컬 LLM 과 클라우드 LLM 을 「같은 작성법」으로 다루고 싶은 사람을 위한 LLMesh — 30 초로 실행 가능한 Python 프레임워크

<!-- KAMI -->
> 📖 **간단히 말하면**
>
> 간단히 말하면, 이 장은 「내 PC 에서 돌아가는 AI 도, 인터넷 너머에 있는 유료 AI 도, 완전히 같은 호출 방식으로 쓸 수 있게 했다」는 이야기입니다. 보통은 서비스마다 연결 방식과 에러가 나는 방식이 제각각이라, 갈아탈 때마다 코드를 다시 짜는 신세가 됩니다. LLMesh 는 그 차이를 흡수해서, 개발 중에는 로컬・운영에서는 클라우드 같은 전환을 사실상 1 줄로 끝냅니다. 덤으로, 외부 데이터베이스를 띄우지 않아도 문서 검색(RAG)이 돌아가는 구조까지 `pip install` 한 방으로 따라옵니다.
<!-- KAMI -->

:::note info
**📚 FullSense 지식 베이스 안내** <!-- fullsense-team-kb -->
FullSense 개발 전사 60+ 편 (4개 언어판・스토리 기반 읽기 순서 가이드・쉬운 설명판・4컷 만화 포함) 은 Qiita Team **FullSense KB** 에 모여 있습니다 (팀 멤버 전용).
:::


> Ollama / OpenAI / Azure / Anthropic / OpenRouter / Groq / Together / Mistral / DeepSeek 를 같은 ABC 로
> `pip install llmesh-mcp`

---

#### 먼저 실행한다(30 초)

```bash
pip install llmesh-mcp
```

```python
### 어느 LLM 이든 같은 인터페이스
from llmesh.llm import OllamaBackend

llm = OllamaBackend(model="llama3.2")          # 로컬이면 API 키 불필요
print(llm.complete("Python의 `yield`를 한 줄로 설명해줘"))
```

클라우드로 전환하는 건 이것뿐입니다.

```python
from llmesh.llm import openai_backend

llm = openai_backend(api_key="sk-...", model="gpt-4o-mini")
print(llm.complete("Python의 `yield`를 한 줄로 설명해줘"))
```

**호출 코드는 한 글자도 바뀌지 않습니다.** 이게 하고 싶었던 핵심입니다.

---

#### 무엇이 좋은가(3 가지만)

1. **backend 교체가 코드 1 줄**: 개발은 로컬 Ollama, 운영은 OpenAI, 검증은 Anthropic, 비용 압축이면 OpenRouter.
2. **에러 타입・타임아웃・리트라이가 통일**: 프로바이더마다 try/except 를 나눠 쓸 필요가 없다.
3. **LLM 의 앞뒤에 보안 층이 공짜로 얹힌다**: Prompt Firewall / OutputValidator / Audit Log 를 **옵션으로 끼워넣을 수 있다**.

---

#### 지원 backend 목록

| backend | 용도 | 필요한 것 |
|---|---|---|
| `OllamaBackend` | 로컬 LLM | `ollama` 를 띄워둘 것(`ollama serve`) |
| `LlamaCppBackend` | 로컬 GGUF | `llama-cpp-python` |
| `openai_backend(...)` | OpenAI / Azure OpenAI / OpenRouter / Together / Groq / Mistral / DeepSeek(OpenAI 호환 API 라면 전부) | API 키 |
| `anthropic_backend(...)` | Claude (Haiku / Sonnet / Opus) | API 키 |

**OpenAI 호환 API 는 하나의 함수로 흡수**하므로, 새로운 프로바이더가 나와도 `base_url` 만 바꾸면 쓸 수 있습니다.

```python
### OpenRouter 경유로 여러 모델 비교
or_llm = openai_backend(
    api_key=OR_KEY,
    base_url="https://openrouter.ai/api/v1",
    model="anthropic/claude-haiku-4-5",
)
```

---

#### 「첫 RAG」를 5 분 만에

외부 DB 제로・전부 stdlib + numpy 로 돌아가는 RAG 가 들어 있습니다.

```python
from llmesh.rag import Retriever, MockEmbedder, NumpyVectorStore, Document

store = NumpyVectorStore(path="kb.npz")        # .npz 에 영속화
embedder = MockEmbedder(dim=128)               # 결정론 해시(의존성 제로)

### 문서를 넣는다
store.add([
    Document(id="d1", text="LLMesh 는 로컬 LLM 과 클라우드 LLM 을 같은 ABC 로 다룬다"),
    Document(id="d2", text="PromptFirewall 은 주입・PII・시크릿을 4 층으로 막는다"),
    Document(id="d3", text="SensorEvent 는 산업 프로토콜 20+ 를 하나로 통합한다"),
], embedder=embedder)
store.save()

### 검색
retriever = Retriever(embedder=embedder, store=store)
hits = retriever.search("프롬프트 인젝션 대책은?", k=2)
for h in hits:
    print(h.score, h.document.text)
```

구현이 자라면 **그대로 Ollama Embedder 로 교체** 가능합니다.

```python
from llmesh.rag import OllamaEmbedder
embedder = OllamaEmbedder(model="nomic-embed-text")  # urllib 만으로 동작
```

데이터가 늘어나면 **3 단계 스토어** 에서 고릅니다.

| 스토어 | 건수 기준 | 영속화 | 검색 |
|---|---:|---|---|
| `NumpyVectorStore` | ~10⁵ | `.npz` | O(n) cosine |
| `SqliteVectorStore` | ~10⁶ | sqlite3 (WAL) | O(n) cosine |
| `LSHVectorStore` | 10⁶~ | `.npz` | LSH ANN(recall@10 ≥ 0.92) |

**외부 DB 를 띄울 필요가 없다** 는 것이 콘셉트입니다. Docker 도 Postgres 도 불필요, `pip install` 로 완결됩니다.

---

#### 가드를 붙여서 LLM 을 호출한다(권장 패턴)

```python
from llmesh import PromptFirewall
from llmesh.llm import openai_backend

fw  = PromptFirewall(presidio_enabled=True)    # PII 층 활성화(요 [presidio])
llm = openai_backend(api_key=KEY, model="gpt-4o-mini")

def safe_complete(prompt: str) -> str:
    v = fw.check(prompt)
    if v.action == "BLOCK":
        raise PermissionError(f"blocked at {v.layer}: {v.reason}")
    if v.action == "SUMMARIZE":
        prompt = v.summarized          # PII 를 플레이스홀더화 완료
    return llm.complete(prompt)
```

**이 8 줄** 로 「시크릿 유출・프롬프트 주입・PII 유출」을 한 세트 막을 수 있습니다.

---

#### Claude Code / MCP 에서 쓴다(복붙용)

`claude_desktop_config.json` 또는 Claude Code 의 설정 JSON 에 붙여넣습니다.

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

이것만으로 Claude Code 에서 `llmesh` 의 tool 군(센서 읽기・SPC 판정・RAG 검색)을 호출할 수 있습니다.
**MCP 의 출력은 OutputValidator 를 반드시 통과** 하므로, tool 쪽에서의 출력 주입도 봉쇄하고 있습니다.

---

#### 트러블슈팅(흔히 막히는 곳)

| 증상 | 원인 | 해결 |
|---|---|---|
| `ModuleNotFoundError: presidio_analyzer` | extras 미설치 | `pip install "llmesh-mcp[presidio]"` |
| `ModuleNotFoundError: numpy` | RAG/SPC 를 맨 `pip install llmesh-mcp` 로 사용 | `pip install "llmesh-mcp[rag]"` 또는 `pip install numpy` |
| Ollama 접속 실패 | 서버 미기동 | `ollama serve`, 또는 생성자에 `base_url=` 지정 |
| 문자 깨짐(Windows) | `cp932` 가 기본값 | `set PYTHONUTF8=1`(PowerShell 은 `$env:PYTHONUTF8=1`) |
| OpenAI 호환 API 에서 모델명이 안 통함 | 프로바이더 고유의 prefix | `model="provider/model-name"` 형식을 확인 |

곤란하면 먼저:

```bash
python -m llmesh.cli.doctor
```

「동작하지 않는 이유를 전부 출력한다」에 집중한 진단 CLI 입니다. **초기 셋업에서 이게 제일 빠릅니다**.

---

#### 로드맵상의 현재 위치

| ver | 무엇이 들어왔나 |
|---|---|
| v2.13 | Presidio PII / RAG MVP / 다변량 SPC 코어 |
| v2.14 | ExplainedCUSUM / VideoCUSUM / SqliteVectorStore / DNP3 / GOOSE |
| v2.15 | LSHVectorStore(ANN) / 공개 API 레이어 / `API_STABILITY.md` |
| v2.16 | OWASP 정적 감사 클린 |
| v2.17 | HTTP DoS hardening(모든 HTTP 클라이언트에 응답 사이즈 상한) |
| v2.18 | 8 종 문서 신규(CONTRIBUTING / DEPLOYMENT / OBSERVABILITY / TROUBLESHOOTING …) |
| v3.0.0 | **API Stability Release**(SemVer 정식 적용, `__all__` 계약화) |
| **v3.1.0** | **클라우드 LLM 통합(OpenAI / Azure / Anthropic / OpenRouter / Together / Groq / Mistral / DeepSeek)** |

**v3.0.0 부터 SemVer 정식 적용**. `docs/API_STABILITY.md` 의 공개 심볼 목록이 계약입니다(minor 는 후방 호환, major 만 파괴적 변경).

---

#### 다음 단계

```bash
### 무엇이 동작하는지 전부 보고 싶다
pip install "llmesh-mcp[industrial,vision,presidio,rag]"
python -m llmesh.cli.doctor
python -m llmesh.cli.status

### 우선 Quickstart 스크립트
python -c "from llmesh.llm import OllamaBackend; print(OllamaBackend(model='llama3.2').complete('hi'))"
```

- GitHub: <https://github.com/furuse-kazufumi/llmesh>
- PyPI: <https://pypi.org/project/llmesh-mcp/>
- License: MIT
- Issue 환영: <https://github.com/furuse-kazufumi/llmesh/issues>

---

#### 마치며

「로컬과 클라우드를 같은 인터페이스로」「보안 층을 나중에 끼워넣을 수 있게」「외부 DB 없이 RAG 가 동작」 — 이 3 가지만으로도, 최초의 LLM 프로토타입부터 운영까지 **같은 코드로 스케일할 수 있는** 것이 이 프레임워크의 노림수입니다.
PR / Issue / 「○○ backend 가 갖고 싶다」「△△ 벡터 DB 가 갖고 싶다」 환영합니다.
