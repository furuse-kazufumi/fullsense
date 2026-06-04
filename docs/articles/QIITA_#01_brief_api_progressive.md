---
layout: default
title: "Brief API and progressive matrix — llive overhead < 1 %"
date: 2026-05-17
tags: [llm, agent, on-prem, ollama, benchmark]
id: 60537278f72f8a9fc2dc
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# Brief API 設計と progressive matrix で見える llive の overhead < 1 %

## TL;DR

- llive は OSS LLM (Ollama 経由の Qwen / Llama / Mistral) を **判断者ではなく素材生成者** として呼び出す上位フレームワーク
- 2026-05-17、外部から構造化 work unit を渡せる **Brief API** を end-to-end で実装
- xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b} の **5×3 = 15 セルベンチ**で、Brief API + FullSenseLoop の overhead は **LLM-only / Wall > 99.8 %** = 1 % 未満
- 全 15 セルで loop の意思決定が `note` で安定 → token 圧力に対し決定木が動じない

## なぜ Brief API が必要だったか

llive の FullSense Loop は 6 stage (salience → curiosity → thought → ego/altruism → plan → output) の収束プロセスを持つが、これまで入力は単純な `Stimulus(content, source, surprise)` で、外部クライアント (lldesign / lltrade / 計画中の llcad / lleda / llchip) が「構造化された work unit」を渡せなかった。

つまり llive はそのままでは **thinking-evaluator** であって、 **doing-agent** ではなかった。これは 2026-05-16 の A/B run で 8 件の bug として可視化された (`docs/BUGS_2026-05-16_brief_ab.md`)。

Brief API は:

- `goal` (必須) + `constraints` + `success_criteria` + `tools whitelist` + `approval_required` + `priority` + `epistemic_type` を持つ frozen dataclass
- YAML から read 可、CLI / MCP からも入る
- Brief → Stimulus → loop → Approval gate → tool 実行 → outcome までを 1 トランザクションで実行
- 全ステップを append-only JSONL ledger に記録 (replay 可能)

## アーキテクチャ

![BriefRunner.submit() のトランザクション・フロー（External client → Brief → 10 ステップを 1 トランザクションで実行し append-only JSONL ledger に記録）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q01/architecture.svg)

## Progressive validation matrix (on-prem only)

`feedback_benchmark_progressive_tokens.md` の xs/s/m/l/xl 5 段ラダー + `feedback_llive_measurement_purity.md` の on-prem 純度ルール (cloud LLM は混在禁止) で評価。

### Wall-time matrix (ms)

| model         | xs (cold) | s     | m     | l       | xl (timeout) |
|---------------|-----------|-------|-------|---------|--------------|
| llama3.2:3b   | 8 908     | 43 978| 89 484| 458 400 | 1 202 282 ⌛ |
| qwen2.5:7b    | 59 447    | 94 158|122 134| 722 867 | 1 202 104 ⌛ |
| qwen2.5:14b   |121 560    |122 160|122 160|1 202 263⌛|1 202 199 ⌛ |

### LLM-only / Wall 比

全 15 セルで **> 99.8 %** — Brief API + loop の追加コストは ~1 % 未満。これは「llive は薄い接着剤」という設計意図を実測で確認できた。

### Loop 決定 (decision)

| model \ size | xs | s | m | l | xl |
|---|---|---|---|---|---|
| llama3.2:3b | note | note | note | note | note |
| qwen2.5:7b | note | note | note | note | note |
| qwen2.5:14b | note | note | note | note | note |

**全 15 セル `note`** — loop の決定木が token 圧力に対し完全 stable。これは Brief 構造が誘導的に効いている (Stimulus の `epistemic_type=PRAGMATIC` + `source=bench:progressive` で track が固定された) 結果と解釈できる。

### thought_chars 観察

llama3.2:3b は xs で 494、xl で 222 → 出力 truncate 境界が xl で見える。
qwen2.5:14b は m から 222 で plateau。つまり 800 tokens 以降は要約圧縮モードに入る。

## 実装ポイント

### 1. Brief は frozen dataclass

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str
    goal: str
    constraints: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    ledger_path: Path | None = None
    # ...
```

「同じ Brief を ledger・loop・result が共有する」という invariant を frozen で守る。tuple は hashable のため再現性ベンチでも使える。

### 2. Ledger は append-only JSONL

```python
ledger.append("brief_submitted", {"brief": brief_to_dict(brief)})
ledger.append("decision", {"decision": "note", "rationale": "..."})
# ...
```

`meta` envelope に timestamp / pid を分離 → 同じ Brief を replay すると同じ outcome が再現可能 (timestamp は ignore)。

### 3. Approval Bus は SIL 軸の core

PROPOSE / INTERVENE 決定は必ず Approval Bus を経由する設計。policy で auto-approve/deny / 残りは人手 review。すべて SQLite に永続化。

## Brief API オーバーヘッドが 1 % 未満で済んだ理由

LLM 推論 (Ollama HTTP request) が 9〜1200 秒のオーダーであるのに対し、llive 側の処理 (JSON serialization + ledger write + 6 stage の Python 計算) は 10〜30 ms 程度。比率で見ると常に < 1 %。

これは「llive を入れたら遅くなる」という懸念を実測で否定する強い根拠となる。

## 何が次に来るか

- **CABT-01**: HFAdapter forward hook で attention output に metadata bias 注入 → Transformer ブロックの高度化
- **MATH-01/08**: 数学・単位特化 vertical で「LLM に計算させない」決定論的経路
- **CREAT-01**: KJ法ノードで Brief から拡散的アイデア生成
- **COG-FX**: 10 思考因子のうち残る現実接続因子 (Phase 4 IoT)

## ソース

- 実装: `llive/src/llive/brief/` (types / loader / ledger / runner / grounding / governance)
- 設計 doc: `llive/docs/proposals/brief_api_design.md`
- ベンチ raw: `llive/docs/benchmarks/2026-05-16-progressive-full/`
- テスト: 1014 PASS (回帰ゼロ)

---

> FullSense ™ は llmesh (LLM hub) ・ llive (memory framework) ・ llove (TUI HITL) の 3 製品で構成される on-prem AI スタック。すべて Apache-2.0 + Commercial dual-license。

---

# English

# How the Brief API and the progressive matrix reveal llive's overhead < 1 %

## TL;DR

- llive is an upper-layer framework that calls OSS LLMs (Qwen / Llama / Mistral via Ollama) **as material generators, not as judges**
- On 2026-05-17 we implemented the **Brief API** end-to-end, letting external clients hand in structured work units
- Across a **5×3 = 15-cell benchmark** of xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b}, the overhead of the Brief API + FullSenseLoop stays at **LLM-only / Wall > 99.8 %** = under 1 %
- In all 15 cells the loop's decision settles on `note` → the decision tree does not flinch under token pressure

## Why the Brief API was needed

llive's FullSense Loop runs a convergence process of 6 stages (salience → curiosity → thought → ego/altruism → plan → output), but until now the input was a simple `Stimulus(content, source, surprise)`. External clients (lldesign / lltrade, plus the planned llcad / lleda / llchip) had no way to hand over a "structured work unit."

In other words, llive as-is was a **thinking-evaluator**, not a **doing-agent**. The A/B run of 2026-05-16 made this visible as 8 bugs (`docs/BUGS_2026-05-16_brief_ab.md`).

The Brief API provides:

- A frozen dataclass carrying `goal` (required) + `constraints` + `success_criteria` + `tools whitelist` + `approval_required` + `priority` + `epistemic_type`
- Readable from YAML, and accepted from CLI / MCP as well
- Execution of Brief → Stimulus → loop → Approval gate → tool invocation → outcome as a single transaction
- Recording of every step in an append-only JSONL ledger (replayable)

## Architecture

![BriefRunner.submit() transaction flow (External client → Brief → 10 steps run as a single transaction and recorded in an append-only JSONL ledger)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q01/architecture_en.svg)

## Progressive validation matrix (on-prem only)

Evaluated with the xs/s/m/l/xl 5-step ladder from `feedback_benchmark_progressive_tokens.md` plus the on-prem purity rule from `feedback_llive_measurement_purity.md` (no cloud LLMs may be mixed in).

### Wall-time matrix (ms)

| model         | xs (cold) | s     | m     | l       | xl (timeout) |
|---------------|-----------|-------|-------|---------|--------------|
| llama3.2:3b   | 8 908     | 43 978| 89 484| 458 400 | 1 202 282 ⌛ |
| qwen2.5:7b    | 59 447    | 94 158|122 134| 722 867 | 1 202 104 ⌛ |
| qwen2.5:14b   |121 560    |122 160|122 160|1 202 263⌛|1 202 199 ⌛ |

### LLM-only / Wall ratio

**> 99.8 %** across all 15 cells — the extra cost of the Brief API + loop is under ~1 %. This is empirical confirmation of the design intent that "llive is thin glue."

### Loop decision

| model \ size | xs | s | m | l | xl |
|---|---|---|---|---|---|
| llama3.2:3b | note | note | note | note | note |
| qwen2.5:7b | note | note | note | note | note |
| qwen2.5:14b | note | note | note | note | note |

**`note` in all 15 cells** — the loop's decision tree is fully stable under token pressure. We read this as the Brief structure acting inductively (the track was pinned by `epistemic_type=PRAGMATIC` + `source=bench:progressive` on the Stimulus).

### thought_chars observation

llama3.2:3b goes from 494 at xs to 222 at xl → the output truncation boundary shows up at xl.
qwen2.5:14b plateaus at 222 from m onward. In other words, beyond 800 tokens it enters a summarize-and-compress mode.

## Implementation points

### 1. Brief is a frozen dataclass

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str
    goal: str
    constraints: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    ledger_path: Path | None = None
    # ...
```

`frozen` protects the invariant that "the ledger, the loop, and the result all share the same Brief." Because tuples are hashable, the Brief is also usable in reproducibility benchmarks.

### 2. The ledger is append-only JSONL

```python
ledger.append("brief_submitted", {"brief": brief_to_dict(brief)})
ledger.append("decision", {"decision": "note", "rationale": "..."})
# ...
```

The `meta` envelope separates out timestamp / pid → replaying the same Brief reproduces the same outcome (timestamps are ignored).

### 3. The Approval Bus is the core of the SIL axis

PROPOSE / INTERVENE decisions are designed to always go through the Approval Bus. Policy handles auto-approve/deny; the rest goes to human review. Everything is persisted to SQLite.

## Why the Brief API overhead came in under 1 %

LLM inference (the Ollama HTTP request) is on the order of 9 to 1200 seconds, whereas llive-side processing (JSON serialization + ledger write + the 6-stage Python computation) is on the order of 10 to 30 ms. As a ratio, it is always < 1 %.

This is strong evidence that empirically refutes the worry that "adding llive will slow things down."

## What comes next

- **CABT-01**: Inject metadata bias into the attention output via an HFAdapter forward hook → sophistication of the Transformer block
- **MATH-01/08**: A deterministic path that "does not let the LLM compute" in a math/units-specialized vertical
- **CREAT-01**: Divergent idea generation from a Brief using KJ-method nodes
- **COG-FX**: The remaining reality-connection factor among the 10 thinking factors (Phase 4 IoT)

## Sources

- Implementation: `llive/src/llive/brief/` (types / loader / ledger / runner / grounding / governance)
- Design doc: `llive/docs/proposals/brief_api_design.md`
- Benchmark raw: `llive/docs/benchmarks/2026-05-16-progressive-full/`
- Tests: 1014 PASS (zero regressions)

---

> FullSense ™ is an on-prem AI stack made up of three products: llmesh (LLM hub), llive (memory framework), and llove (TUI HITL). All are Apache-2.0 + Commercial dual-license.

---

# 中文

# 通过 Brief API 与 progressive matrix 看到的 llive overhead < 1 %

## TL;DR

- llive 是一个上层框架，它把开源 LLM（经由 Ollama 的 Qwen / Llama / Mistral）**作为素材生成者而非判断者**来调用
- 2026-05-17，端到端实现了可以从外部传入结构化 work unit 的 **Brief API**
- 在 xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b} 的 **5×3 = 15 单元基准测试**中，Brief API + FullSenseLoop 的 overhead 保持在 **LLM-only / Wall > 99.8 %** = 不到 1 %
- 全部 15 个单元中 loop 的决策都稳定在 `note` → 决策树在 token 压力下毫不动摇

## 为什么需要 Brief API

llive 的 FullSense Loop 拥有 6 个 stage（salience → curiosity → thought → ego/altruism → plan → output）的收敛过程，但此前输入只是简单的 `Stimulus(content, source, surprise)`，外部客户端（lldesign / lltrade，以及计划中的 llcad / lleda / llchip）无法传入“结构化的 work unit”。

也就是说，llive 原样只是一个 **thinking-evaluator**，而非 **doing-agent**。这一点在 2026-05-16 的 A/B run 中以 8 个 bug 的形式被可视化（`docs/BUGS_2026-05-16_brief_ab.md`）。

Brief API 提供：

- 一个携带 `goal`（必填）+ `constraints` + `success_criteria` + `tools whitelist` + `approval_required` + `priority` + `epistemic_type` 的 frozen dataclass
- 可从 YAML 读取，也可从 CLI / MCP 传入
- 把 Brief → Stimulus → loop → Approval gate → tool 执行 → outcome 作为一个事务执行
- 把所有步骤记录到 append-only JSONL ledger（可 replay）

## 架构

![BriefRunner.submit() 的事务流程（External client → Brief → 10 个步骤作为一个事务执行并记录到 append-only JSONL ledger）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q01/architecture_zh.svg)

## Progressive validation matrix（仅 on-prem）

采用 `feedback_benchmark_progressive_tokens.md` 的 xs/s/m/l/xl 5 级阶梯 + `feedback_llive_measurement_purity.md` 的 on-prem 纯度规则（禁止混入 cloud LLM）进行评估。

### Wall-time matrix (ms)

| model         | xs (cold) | s     | m     | l       | xl (timeout) |
|---------------|-----------|-------|-------|---------|--------------|
| llama3.2:3b   | 8 908     | 43 978| 89 484| 458 400 | 1 202 282 ⌛ |
| qwen2.5:7b    | 59 447    | 94 158|122 134| 722 867 | 1 202 104 ⌛ |
| qwen2.5:14b   |121 560    |122 160|122 160|1 202 263⌛|1 202 199 ⌛ |

### LLM-only / Wall 比

全部 15 个单元都 **> 99.8 %** —— Brief API + loop 的额外成本不到 ~1 %。这用实测确认了“llive 是一层薄薄的胶水”的设计意图。

### Loop 决策 (decision)

| model \ size | xs | s | m | l | xl |
|---|---|---|---|---|---|
| llama3.2:3b | note | note | note | note | note |
| qwen2.5:7b | note | note | note | note | note |
| qwen2.5:14b | note | note | note | note | note |

**全部 15 个单元均为 `note`** —— loop 的决策树在 token 压力下完全 stable。可解读为 Brief 结构起到了诱导作用（Stimulus 的 `epistemic_type=PRAGMATIC` + `source=bench:progressive` 把 track 固定了下来）的结果。

### thought_chars 观察

llama3.2:3b 在 xs 为 494，在 xl 为 222 → 输出 truncate 边界在 xl 处显现。
qwen2.5:14b 从 m 开始在 222 处 plateau。也就是说，超过 800 tokens 之后进入摘要压缩模式。

## 实现要点

### 1. Brief 是 frozen dataclass

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str
    goal: str
    constraints: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    ledger_path: Path | None = None
    # ...
```

用 `frozen` 守住“同一个 Brief 被 ledger、loop、result 共享”这一 invariant。由于 tuple 是 hashable 的，因此在可复现性基准测试中也能使用。

### 2. Ledger 是 append-only JSONL

```python
ledger.append("brief_submitted", {"brief": brief_to_dict(brief)})
ledger.append("decision", {"decision": "note", "rationale": "..."})
# ...
```

`meta` envelope 把 timestamp / pid 分离出来 → replay 同一个 Brief 即可复现同一个 outcome（timestamp 被忽略）。

### 3. Approval Bus 是 SIL 轴的 core

PROPOSE / INTERVENE 决策的设计是必定经由 Approval Bus。由 policy 进行 auto-approve/deny，其余交由人工 review。所有内容都持久化到 SQLite。

## 为什么 Brief API 的 overhead 能控制在 1 % 以内

LLM 推理（Ollama HTTP request）在 9～1200 秒的量级，而 llive 一侧的处理（JSON serialization + ledger write + 6 stage 的 Python 计算）只有 10～30 ms 左右。从比例看始终 < 1 %。

这成为用实测否定“引入 llive 会变慢”这一担忧的有力依据。

## 接下来会发生什么

- **CABT-01**：通过 HFAdapter forward hook 把 metadata bias 注入到 attention output → Transformer 块的高级化
- **MATH-01/08**：在数学・单位特化 vertical 中“不让 LLM 计算”的确定性路径
- **CREAT-01**：用 KJ 法节点从 Brief 生成发散式创意
- **COG-FX**：10 个思考因子中剩余的现实接续因子（Phase 4 IoT）

## 来源

- 实现：`llive/src/llive/brief/`（types / loader / ledger / runner / grounding / governance）
- 设计 doc：`llive/docs/proposals/brief_api_design.md`
- 基准 raw：`llive/docs/benchmarks/2026-05-16-progressive-full/`
- 测试：1014 PASS（零回归）

---

> FullSense ™ 是由 llmesh（LLM hub）、llive（memory framework）、llove（TUI HITL）这 3 个产品构成的 on-prem AI 栈。全部为 Apache-2.0 + Commercial dual-license。

---

# 한국어

# Brief API 설계와 progressive matrix 로 보이는 llive 의 overhead < 1 %

## TL;DR

- llive 는 OSS LLM(Ollama 경유의 Qwen / Llama / Mistral)을 **판단자가 아닌 소재 생성자**로 호출하는 상위 프레임워크
- 2026-05-17, 외부에서 구조화된 work unit 을 넘길 수 있는 **Brief API** 를 end-to-end 로 구현
- xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b} 의 **5×3 = 15 셀 벤치**에서 Brief API + FullSenseLoop 의 overhead 는 **LLM-only / Wall > 99.8 %** = 1 % 미만
- 전체 15 셀에서 loop 의 의사결정이 `note` 로 안정 → 결정 트리가 token 압력에 흔들리지 않음

## 왜 Brief API 가 필요했는가

llive 의 FullSense Loop 는 6 stage(salience → curiosity → thought → ego/altruism → plan → output)의 수렴 프로세스를 가지고 있지만, 지금까지 입력은 단순한 `Stimulus(content, source, surprise)` 였고, 외부 클라이언트(lldesign / lltrade, 계획 중인 llcad / lleda / llchip)가 “구조화된 work unit”을 넘길 수 없었다.

즉 llive 는 그대로는 **thinking-evaluator** 이지 **doing-agent** 가 아니었다. 이는 2026-05-16 의 A/B run 에서 8 건의 bug 로 가시화되었다(`docs/BUGS_2026-05-16_brief_ab.md`).

Brief API 는:

- `goal`(필수) + `constraints` + `success_criteria` + `tools whitelist` + `approval_required` + `priority` + `epistemic_type` 를 가지는 frozen dataclass
- YAML 에서 read 가능, CLI / MCP 에서도 입력 가능
- Brief → Stimulus → loop → Approval gate → tool 실행 → outcome 까지를 하나의 트랜잭션으로 실행
- 모든 스텝을 append-only JSONL ledger 에 기록(replay 가능)

## 아키텍처

![BriefRunner.submit() 의 트랜잭션 흐름 (External client → Brief → 10 개 스텝을 하나의 트랜잭션으로 실행하고 append-only JSONL ledger 에 기록)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q01/architecture_ko.svg)

## Progressive validation matrix (on-prem only)

`feedback_benchmark_progressive_tokens.md` 의 xs/s/m/l/xl 5 단 래더 + `feedback_llive_measurement_purity.md` 의 on-prem 순도 규칙(cloud LLM 혼재 금지)으로 평가.

### Wall-time matrix (ms)

| model         | xs (cold) | s     | m     | l       | xl (timeout) |
|---------------|-----------|-------|-------|---------|--------------|
| llama3.2:3b   | 8 908     | 43 978| 89 484| 458 400 | 1 202 282 ⌛ |
| qwen2.5:7b    | 59 447    | 94 158|122 134| 722 867 | 1 202 104 ⌛ |
| qwen2.5:14b   |121 560    |122 160|122 160|1 202 263⌛|1 202 199 ⌛ |

### LLM-only / Wall 비

전체 15 셀에서 **> 99.8 %** — Brief API + loop 의 추가 비용은 ~1 % 미만. 이는 “llive 는 얇은 접착제”라는 설계 의도를 실측으로 확인할 수 있었다.

### Loop 결정 (decision)

| model \ size | xs | s | m | l | xl |
|---|---|---|---|---|---|
| llama3.2:3b | note | note | note | note | note |
| qwen2.5:7b | note | note | note | note | note |
| qwen2.5:14b | note | note | note | note | note |

**전체 15 셀 `note`** — loop 의 결정 트리가 token 압력에 대해 완전히 stable. 이는 Brief 구조가 유도적으로 작용한(Stimulus 의 `epistemic_type=PRAGMATIC` + `source=bench:progressive` 로 track 이 고정된) 결과로 해석할 수 있다.

### thought_chars 관찰

llama3.2:3b 는 xs 에서 494, xl 에서 222 → 출력 truncate 경계가 xl 에서 보인다.
qwen2.5:14b 는 m 부터 222 에서 plateau. 즉 800 tokens 이후는 요약 압축 모드에 들어간다.

## 구현 포인트

### 1. Brief 는 frozen dataclass

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str
    goal: str
    constraints: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    ledger_path: Path | None = None
    # ...
```

“같은 Brief 를 ledger・loop・result 가 공유한다”는 invariant 를 frozen 으로 지킨다. tuple 은 hashable 이므로 재현성 벤치에서도 사용할 수 있다.

### 2. Ledger 는 append-only JSONL

```python
ledger.append("brief_submitted", {"brief": brief_to_dict(brief)})
ledger.append("decision", {"decision": "note", "rationale": "..."})
# ...
```

`meta` envelope 에 timestamp / pid 를 분리 → 같은 Brief 를 replay 하면 같은 outcome 이 재현 가능(timestamp 은 ignore).

### 3. Approval Bus 는 SIL 축의 core

PROPOSE / INTERVENE 결정은 반드시 Approval Bus 를 경유하는 설계. policy 로 auto-approve/deny, 나머지는 사람 손으로 review. 모두 SQLite 에 영속화.

## Brief API 오버헤드가 1 % 미만으로 끝난 이유

LLM 추론(Ollama HTTP request)이 9〜1200 초 오더인 데 비해, llive 측의 처리(JSON serialization + ledger write + 6 stage 의 Python 계산)는 10〜30 ms 정도. 비율로 보면 항상 < 1 %.

이는 “llive 를 넣으면 느려진다”는 우려를 실측으로 부정하는 강력한 근거가 된다.

## 다음에 무엇이 오는가

- **CABT-01**: HFAdapter forward hook 으로 attention output 에 metadata bias 주입 → Transformer 블록의 고도화
- **MATH-01/08**: 수학・단위 특화 vertical 에서 “LLM 에게 계산시키지 않는” 결정론적 경로
- **CREAT-01**: KJ법 노드로 Brief 에서 확산적 아이디어 생성
- **COG-FX**: 10 사고 인자 중 남은 현실 접속 인자(Phase 4 IoT)

## 소스

- 구현: `llive/src/llive/brief/` (types / loader / ledger / runner / grounding / governance)
- 설계 doc: `llive/docs/proposals/brief_api_design.md`
- 벤치 raw: `llive/docs/benchmarks/2026-05-16-progressive-full/`
- 테스트: 1014 PASS (회귀 제로)

---

> FullSense ™ 는 llmesh(LLM hub)・llive(memory framework)・llove(TUI HITL)의 3 제품으로 구성되는 on-prem AI 스택. 모두 Apache-2.0 + Commercial dual-license.
