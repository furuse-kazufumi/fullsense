# RepIR × 汎用 MCP ルーター互換性 設計メモ (2026-05-23)

> **改名 (2026-05-24): RepIR → `llrepr`**（既存 OSS github.com/repir/repir [情報検索] と
> 頭字語衝突のため。本 doc 内の "RepIR" は `llrepr` と読み替え）。
> **実装着地**: llmesh `llmesh/llrepr/` に PoC 着地済（commits 12c1a07 / 6044ba4, 24 tests）。
> 本メモ推奨の `structuredContent` + text(Markdown) 併置形を実装。詳細:
> [`llrepr_poc_2026_05_24.md`]({{ '/research/llrepr_poc_2026_05_24' | relative_url }})。

> ユーザー懸念「RepIR は llama.cpp のような汎用 MCP ルーター/クライアントと互換性が
> あるか」をサブエージェント (general-purpose + WebSearch) で検証した結論。
> RepIR PoC (FullSense 実装キュー #1) の着手前に確定すべき互換性前提。
> 元設計: `ideation_marathon_expression_realtime_2026_05_23.md` §論点3。

---

## 結論

1. **独自 content type 案 (`{type:"representation", ...}`) は互換性が取れない。非推奨。**
   - MCP 2025-06-18 の `content` union 正式メンバーは `text / image / audio /
     resource_link / resource` のみ。`representation` は未定義。
   - spec は「未知 content type を無視して通せ」を MUST/SHOULD で規定して**いない**。
     汎用クライアント (llama.cpp WebUI 含む) の挙動は実装依存 = 無視 / lossy 文字列化 /
     drop のいずれかで、**壊れない保証がない**。← ユーザー懸念が当たるケース。

2. **標準 `structuredContent` + text(Markdown degrade) 併置案が正解。推奨。**
   - MCP spec 原文: 「For backwards compatibility, a tool that returns structured
     content **SHOULD** also return the serialized JSON in a TextContent block.」
     = structuredContent と同内容を text block に併置する degrade を**正規パターンとして
     明文化**。検討中の互換案はこれと同形。
   - `outputSchema` を宣言すれば RepIR-aware consumer は schema validation して typed
     描画でき、非対応 consumer は併置 text を読むだけで壊れない。

3. **「汎用ルーター経由で typed 描画が届く」は幻想。二層構成が現実解。**
   - llama.cpp は MCP **client** (server でない)。tool result content の描画は未文書、
     未知 block は無視/lossy/drop。typed rendering はしない。
   - typed 描画は **RepIR-aware consumer (llove TUI / 自前 manga-SVG writer) を MCP host
     側に置く** か、**MQTT/SSE side-channel** に逃がす二層が現実解。汎用ルーターは
     「壊さず素通しする運搬路」までが役割。

---

## 推奨設計形

```jsonc
result = {
  "structuredContent": { "repIR": { "repSchema": <versioned>, "root": <typed node tree> } },
  "content": [
    { "type": "text", "text": "<RepIR を Markdown に degrade した文字列>" }
    // 大型/SVG/manga-SVG は resource_link で URI 併置
  ]
}
```
+ tool 定義に `outputSchema` を宣言 (llmesh 既存 `TOOL_SCHEMAS` を流用)。

---

## llmesh の現状 (file:line)

- `llmesh/mcp/stdio_server.py`: MCP SDK **非依存**の手書き JSON-RPC。
  `protocolVersion: "2024-11-05"` (`:138`, structuredContent 導入前の旧版)。
  tool result は **text content only** (`:195,212,224,235,249,267,272` — 構造化結果も
  JSON 文字列化して text に詰める)。`outputSchema` 未宣言 (`:144-152`)。
- `llmesh/mcp/schemas.py`: `TOOL_SCHEMAS` が各ツールの出力 JSON Schema を定義済
  (`additionalProperties:false`) → **MCP `outputSchema` にそのまま転用可能**。
- `llmesh/mcp/validator.py`: 512KB hard cap (`:30`) → 大型 RepIR は tool result 不可、
  side-channel へ。
- `llmesh/mcp/server.py`: FastAPI HTTP は MCP 非準拠の独自 REST (汎用 MCP client から
  直接は叩けない)。

---

## RepIR PoC 開始前チェックリスト

- [ ] 独自 content type 不採用。`structuredContent` + text(Markdown) 併置を運搬の基本形に固定
- [ ] `outputSchema` を必ず宣言 (`TOOL_SCHEMAS` 再利用)。`repSchema` を versioned 管理
- [ ] **degrade writer を first-class に**: RepIR→Markdown (最低保証, **PoC 必須**) + RepIR→SVG/TUI (typed)
- [ ] `stdio_server.py` の protocolVersion を `2024-11-05` → `2025-06-18` 更新が structuredContent の前提 (`:138`)
- [ ] MCP SDK 非依存のまま手書き追加 / 公式 SDK 載せ替え の方針決定
- [ ] RepIR-aware consumer の所在決定 (llove を host 側 / 汎用 host は text fallback のみと割り切る)
- [ ] リアルタイム/大型 RepIR は tool result でなく `resource_link` or MQTT/SSE side-channel
- [ ] extensions `used`/`required` の degrade ポリシー (required を解釈できない consumer は描画拒否 or fallback、fail-closed と整合)

---

## 出典

- MCP Spec — Tools (2025-06-18): <https://modelcontextprotocol.io/specification/2025-06-18/server/tools>
- MCP Schema Reference (2025-06-18): <https://modelcontextprotocol.io/specification/2025-06-18/schema>
- Cisco — What's New in MCP: Structured Content / Elicitation / OAuth
- llama.cpp Merges Full MCP Support (PR #18655, 2026-03-06)
- llama.cpp function-calling docs (ggml-org/llama.cpp)
- MCP Apps blog (SEP-1865, `ui://` HTML テンプレ前提)
- MCP `_meta` extensibility discussion #419
- MCPcat — MCP error handling / content fallback
