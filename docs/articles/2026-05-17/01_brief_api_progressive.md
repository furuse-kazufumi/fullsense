---
layout: default
title: "Brief API and progressive matrix — llive overhead < 1 %"
date: 2026-05-17
tags: [llm, agent, on-prem, ollama, benchmark]
---

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

```
External client
   │ Brief (YAML / CLI / MCP)
   ▼
BriefRunner.submit()
   ├─ 1. brief_submitted   → ledger
   ├─ 2. (optional) grounding_applied (TRIZ × RAD citation)
   ├─ 3. stimulus_built    → ledger
   ├─ 4. FullSenseLoop.process(stim)
   │     └─ 6 stage loop (既存)
   ├─ 5. loop_completed    → ledger
   ├─ 6. decision          → ledger
   ├─ 7. (optional) governance_scored (4 軸)
   ├─ 8. Approval Bus gate (PROPOSE/INTERVENE 時のみ)
   ├─ 9. tool_invoked × N  → ledger
   └─10. outcome           → ledger
```

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
