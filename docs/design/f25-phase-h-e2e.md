# F25 Phase h — llove ↔ llmesh ↔ llive E2E 設計 (draft v0.2)

> 2026-05-18 作成. 戦略思索 PART 5 (Engine 抽出) + memory project_llove_f25_bridge
> (Phase 0-g 完了、h=E2E 残) を踏まえ、F25 連携基盤の Phase h (End-to-End) を
> 設計 draft.
>
> v0.2 (2026-05-18 同日): 実コード確認 (llove/llove/engine/http_app.py,
> llive/src/llive/mcp/tools.py::tool_submit_brief, llive annotations) を元に
> API schema / SSE event / env / error handling / skeleton 現状を確定。

## 1. ゴール

3 製品 (llmesh / llive / llove) を MCP プロトコル経由で接続し、ユーザが
**「1 つの Brief を投げると 3 製品が連動して動く」** 体験を実現する.

### 具体的な期待動作

```
User: llove TUI で `:brief <task>` を実行
   ↓
llove → llive MCP submit_brief(text, source, ...) を呼ぶ
   ↓
llive FullSenseLoop:
   ① Salience Gate
   ② Curiosity Drive
   ③ Inner Monologue (LLM 経由)
   ④ Ego/Altruism Scorer
   ⑤ Action Plan
   ⑥ Finalise (Approval Bus + SqliteLedger)
   ↓ Annotation Channel emit
llove pane に逐次 stream される:
   - 思考因子発火 / Memory Layer ヒット / Risk Score / 出典追跡 / etc.
   ↓ ActionPlan が IO を必要とする場合
llmesh → 外部 (LLM API / IoT / Tool) 呼び出し
   ↓ 結果を再度 llive に戻し、llove で表示
```

## 2. Phase 0-g 完了状態 (memory より)

memory `project_llove_f25_bridge` 確認: Phase 0-g 完了, h = E2E 残 (2026-05-14).

- 0: bootstrap / scaffolding
- a-g: 各 MCP tool の skeleton + 単体テスト
- **h (本 phase)**: 3 製品を実際に接続して E2E run できる状態

## 3. アーキテクチャ概観

```
                    ┌─────────────────────┐
                    │  llove TUI / engine │
                    │   (HTTP localhost)  │
                    └──────────┬──────────┘
                               │ MCP client (stdio / TCP)
                               ▼
                    ┌─────────────────────┐
                    │  llive MCP server   │
                    │  src/llive/mcp/     │
                    │   submit_brief etc. │
                    └──────────┬──────────┘
                               │ FullSenseLoop.process()
                               ▼
            ┌──────────────────┴──────────────────┐
            ▼                                      ▼
   ┌────────────────┐                  ┌────────────────────┐
   │ llmesh client  │                  │  Annotation        │
   │ (LLM routing)  │                  │  Channel emit →    │
   │                │                  │  llove subscribe   │
   │ - cn_llm.qwen  │                  │  (SSE / WS)        │
   │ - openai_compat│                  │                    │
   │ - audit log    │                  │  oka.essence_card  │
   │ - HITL gate    │                  │  cog.consensus     │
   └────────┬───────┘                  │  cog.risk_alert    │
            │                          │  vrb.lint_findings │
            ▼                          └────────────────────┘
   ┌────────────────┐
   │ LLM backend    │
   │ (Qwen/DeepSeek │
   │  /GLM/Ollama)  │
   └────────────────┘
```

## 4. Phase h 実装範囲 (Week 2-3)

### h.1 llove → llive submit_brief E2E
- llove engine (Phase-1 skeleton, **2026-05-18 時点で `/healthz` `/api/v1/engine`
  `/api/v1/audit/deps` `/api/v1/audit/offline-check` のみ実装済**) に
  `/api/v1/brief/submit` endpoint を**新規**追加
- 内部で `llive.brief.runner.BriefRunner` を in-process で呼ぶ
  (subprocess pattern は h+1 まで延期 — Phase 1 では同一 Python プロセス前提)
- 引数 / 戻り値は既存 `llive.mcp.tools.tool_submit_brief` と 1:1 対応させ、
  MCP / HTTP どちらからも同じセマンティクスにする
- 結果 `BriefResult` を JSON で返す

### h.2 Annotation Channel SSE / WebSocket stream
- llove engine `/api/v1/annotations/stream` (SSE) を**新規**追加
- llive BriefRunner が emit する :class:`Annotation`
  (namespace ∈ {core, vrb, oka, cog, math, creat, sec, eval}) を
  bounded queue → SSE で push
- llove TUI / VS Code 拡張は EventSource / postMessage 経由で subscribe
- 切断/再接続は `Last-Event-ID` ヘッダで resume (Phase h は best-effort、
  guaranteed delivery は h+1)

### h.3 llive ↔ llmesh LLM backend 接続
- `LLIVE_LLM_BACKEND=ollama:llama3.2` 等の env で動作確認 (既存)
- 中国 LLM 経由の動作確認: `LLIVE_LLM_BACKEND=cnmesh:qwen` (新規)
- llmesh `cn_llm.qwen_backend()` を直接呼べる Adapter 追加
- env: `LLIVE_LLM_BACKEND=cnmesh:<provider>:<model>`

### h.4 llove で観測する 5 pane を結線 (Research IDE F27 への準備)
- Memory Layer pane: llive memory layer state を polling / SSE で取得
- Loop Stages pane: 6 stage の進行状況を SSE で push
- Thought Factors pane: 10 因子の発火状況
- Annotations pane: h.2 の SSE stream
- Brief Output pane: Markdown 出力を MarkdownView で render

### h.5 HITL Approval pane (Phase h+1)
- llive Approval Bus に対する human approve/deny を llove で UI 提供
- POST `/api/v1/hitl/respond` (engine 経由)
- v3.3 / Month 2 で本格化

## 4.6 API / Event schema (h.1 / h.2 確定版)

### 4.6.1 POST `/api/v1/brief/submit`

Request body (`application/json`):

```json
{
  "goal": "string (required, non-empty)",
  "brief_id": "string (optional, server mints mcp-<12hex> if omitted)",
  "constraints": ["string", "..."],
  "source": "string (default: \"engine\")",
  "priority": 0.5,
  "backend": "string (overrides LLIVE_LLM_BACKEND for this brief; empty=use env)",
  "tools": ["string", "..."],
  "success_criteria": ["string", "..."],
  "approval_required": true
}
```

Response (200) — mirror of `tool_submit_brief` shape:

```json
{
  "brief": {
    "brief_id": "string",
    "goal": "string",
    "constraints": ["..."],
    "source": "string",
    "priority": 0.5,
    "backend": "string",
    "tools": ["..."],
    "success_criteria": ["..."],
    "approval_required": true
  },
  "result": {
    "brief_id": "string",
    "status": "ok | needs_approval | rejected | error",
    "rationale": "string",
    "artifacts": ["..."],
    "ledger_entries": ["..."],
    "error": null
  }
}
```

Error codes:

| HTTP | meaning | body |
|---|---|---|
| 400 | empty/invalid `goal` | `{"error":"invalid_goal","detail":"..."}` |
| 422 | schema validation fail | FastAPI standard |
| 503 | llive backend unavailable (e.g. RAD index not loaded) | `{"error":"backend_unavailable"}` |
| 504 | LLM backend timeout (Ollama/cnmesh) | `{"error":"llm_timeout","backend":"..."}` |

### 4.6.2 GET `/api/v1/annotations/stream` (SSE)

Query params:

| name | type | default | meaning |
|---|---|---|---|
| `brief_id` | string | (none) | filter to single brief; omit = all briefs |
| `target_layer` | string | (none) | filter by `target_layer` (`llove` / `llmesh` / `agent`) |
| `namespaces` | csv string | (none) | filter by namespace set |

Event types (all `Content-Type: text/event-stream`):

```
event: annotation
id: 1234
data: {"brief_id":"mcp-abc...","namespace":"oka","key":"essence_card",
       "value":{"summary":"..."},"target_layer":"llove","ts":"2026-05-18T08:00:00Z"}

event: stage_complete
id: 1235
data: {"brief_id":"mcp-abc...","stage":"inner_monologue",
       "stage_index":3,"duration_ms":421,"ts":"..."}

event: brief_done
id: 1236
data: {"brief_id":"mcp-abc...","status":"ok","ts":"..."}

event: heartbeat
id: 1237
data: {"ts":"..."}     # 15s 間隔、idle keepalive
```

Resume semantics: client が `Last-Event-ID: <n>` を投げると、queue に
残っている `id > n` のイベントを replay (best-effort, drop-oldest)。
guaranteed delivery / replay 完全性は Phase h+1 で対応。

### 4.6.3 環境変数

| env | default | scope | 用途 |
|---|---|---|---|
| `LLOVE_ENGINE_HOST` | `127.0.0.1` | llove engine | bind host |
| `LLOVE_ENGINE_PORT` | `7869` | llove engine | bind port |
| `LLOVE_BRIEF_QUEUE_MAX` | `1024` | llove engine | h.2 bounded queue 上限 |
| `LLOVE_BRIEF_QUEUE_POLICY` | `drop_oldest` | llove engine | overflow 時方針 (`drop_oldest` / `block`) |
| `LLIVE_LLM_BACKEND` | `ollama:llama3.2` | llive | LLM backend 指定 (`cnmesh:qwen` 等も可) |
| `LLIVE_BRIEF_APPROVAL_REQUIRED` | `1` | llive | global default for `approval_required` |
| `LLOVE_ENGINE_BIND_AUTH` | `none` | llove engine | Phase 1 は `none` 固定、Pattern C で `bearer` / `mtls` |

### 4.6.4 in-process vs subprocess の選択

Phase h は **in-process** (FastAPI app と FullSenseLoop が同一プロセス) で行く。
理由:

- BriefRunner は同期 API、threading だけで queue → SSE が成立
- subprocess pattern (MCP stdio) は Annotation Channel を pipe で運ぶ
  必要があり、emit-side の hook 追加が必要 → Phase h+1
- Phase 1 想定の Pattern B (VS Code 拡張) は localhost subprocess で十分

## 5. テスト戦略

### h.1-h.3 (E2E run)
- pytest 統合テスト: subprocess で llmesh + llive + llove engine を起動 → Brief 投入 → 結果検証
- mock LLM backend で deterministic test
- `tests/integration/test_f25_phase_h_e2e.py` を新規追加

### h.4 (観測 pane)
- llove pane の単体テスト: SSE message を inject して描画確認
- Textual snapshot test

### h.5 (HITL)
- Phase h+1 で対応

## 6. 既存資産との接続

| 既存資産 | F25 Phase h への使い方 |
|---|---|
| llive Brief API (LLIVE-002, resolved 2026-05-16) | h.1 の入口 |
| llive Annotation Channel (IND-04, 実装済) | h.2 の出口 |
| llive HITL Approval Bus + SqliteLedger (C-1 完了) | h.5 用 |
| llmesh.llm.cn_llm presets (2026-05-18, 本日 commit) | h.3 用 |
| llmesh.audit.trace (HMAC audit log) | h.3 用、各 LLM call を audit |
| llove engine skeleton (2026-05-18, 本日 commit) | h.1 + h.4 の base |
| llove views/* (markdown / annotations / etc.) | h.4 の描画層 |

## 7. 開発タイムライン (Week 2-3)

### Week 2 残 (5/19-5/24)
- **Day 1 (5/19)**: h.1 設計詰め + llove engine `/api/v1/brief/submit` PoC
- **Day 2 (5/20)**: h.2 SSE stream PoC
- **Day 3 (5/21)**: h.3 cnmesh:<provider> LLM backend adapter
- **Day 4 (5/22)**: pytest integration test (h.1-h.3)
- **Day 5-6 (5/23-5/24)**: h.4 5 pane 結線 (Research IDE F27 base)

### Week 3 (5/25-5/31)
- **Day 1-3**: h.4 完成 + Textual snapshot test
- **Day 4-5**: Research IDE F27 α 統合
- **Day 6-7**: 振り返り + 残バグ整理

## 8. リスク

| Risk | 対応 |
|---|---|
| MCP stdio / TCP の選択判断 | TCP localhost で始め、stdio は subprocess pattern (Phase 2) |
| Annotation Channel の back-pressure | bounded queue + drop-oldest policy で latency 確保 |
| 中国 LLM API timeout / quota | httpx timeout + circuit breaker |
| 既存 llove views と新 engine の状態同期 | engine が source of truth、views は read-only consumer に統一 |
| 既存 chess / shogi / typing demo との競合 | 別 mode (e.g. `llove brief <task>`) で分離 |

## 9. 撤退条件

- Week 2 Day 4 まで h.1-h.3 E2E が動かない → h.4 着手禁止、設計簡素化検討
- Week 3 Day 5 まで h.4 5 pane が動かない → F27 を Phase 2 (Month 2) に延期
- Annotation Channel back-pressure が解消不能 → polling 方式に fallback

## 10. 関連 docs / memory

- `D:/projects/audit/STRATEGY_EAR_LOCAL_LLM_2026-05-17_PART5_ENGINE.md`
- memory `project_llove_f25_bridge`
- memory `project_llove_research_ide_pivot`
- memory `project_llive_brief_api_done`
- `D:/projects/llmesh/docs/market/roadmap-v4-draft.md` v3.2.0 Week 2-3 must
- `D:/projects/llmesh/docs/market/feature-pruning.md` F-NEW-10

## 改訂履歴

- 2026-05-18 — draft v0.1 (F25 Phase h 着手前の設計固め)
