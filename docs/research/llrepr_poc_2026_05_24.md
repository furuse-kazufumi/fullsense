---
layout: default
title: "llrepr — PoC 実装着地 (旧 RepIR)"
parent: "Research"
nav_order: 93
---

# llrepr — PoC 実装着地メモ (2026-05-24)

> FullSense 実装キュー #1「RepIR PoC」を **llmesh** に着地。同時に名称衝突が判明し
> **RepIR → llrepr** へ改名。本メモは設計メモ
> [`repir_mcp_compat_2026_05_23.md`]({{ '/research/repir_mcp_compat_2026_05_23' | relative_url }})
> の **実装着地版**（技術資料への取り込み用フィードバック）。

---

## 1. 改名: RepIR → llrepr

旧仮称 **"RepIR"** は既存 OSS と頭字語が衝突していた:

- **github.com/repir/repir** = "Repository for Information Retrieval Experiments"
  (Java 98.7% / Hadoop の**情報検索**フレームワーク, Maven Central 配布)。分野・言語とも無関係だが
  頭字語・GitHub org・検索ブランドが衝突。

FullSense ファミリー (llmesh / llive / llove) に合わせ **`ll-` 始まり**へ改名。PyPI + GitHub の
衝突確認の上 **`llrepr`** を採用:

| 候補 | PyPI | GitHub org | 同名 repo (上位) | 判定 |
|---|---|---|---|---|
| **llrepr** | 空き | 空き | 1 件 (`LLRepresentationConversions` 1★, ゆる一致) | ◎ 採用 |
| llexpr | 空き | 空き | 1 件 (0★, ゆる一致) | ○ 次点 |
| llform | 空き | **取得済** | `TaoWangzj/LLFormer` 236★ ほか 7 件 | △ |
| llumen | 空き | **取得済** | `pinkfuwa/llumen` 89★ **完全同名** | ✗ |
| llir | **取得済** | **取得済** | `llir/llvm` 1274★ (Go の LLVM IR) | ✗ |

> **運用ルール (確立):** 公開ブランド名を提案する前に GitHub org / 同名 repo + PyPI 名の
> 衝突を必ず確認する。以降、portal / 各 doc の "RepIR" は **llrepr** と読み替え。

---

## 2. llrepr とは

**typed Representation IR — 「LLVM-for-expression」。** LLM 出力を**型付きノード木**に一度だけ
落とし、複数の writer がレンダリングする。`producer`（LLM 側）を変えずに renderer を追加できる
（LLVM の「1 IR・多 backend」を表現に持ち込む）。

```
LLM 出力 ──► llrepr (型付きノード木) ──► Markdown(記事) / SVG(Web) / TUI(llove) / 漫画パネル
              ▲ producer は不変                  ▲ writer = backend、追加しても producer 不変
```

FullSense における位置づけ = **表現汎用層**
([`project_llmesh_representation_layer`])。manga-SVG / llove animated SVG / 記事埋込は
すべて llrepr の **consumer**。

---

## 3. 実装 (llmesh `llmesh/llrepr/`)

commits: `12c1a07` (feat) → `6044ba4` (rename RepIR→llrepr) / **tests 24 passed** / Python 3.11 /
依存は stdlib + jsonschema のみ（base install で動く）。

| モジュール | 役割 |
|---|---|
| `model.py` | **L1 閉集合ノードカタログ** + `Style` 値型 + `Document` エンベロープ。fail-closed `validate`。 |
| `writer_base.py` | **capability negotiation**。`required` 拡張を解釈できない writer は描画拒否 (fail-closed)、非 `required` は graceful degrade。 |
| `markdown_writer.py` | **最低保証 degrade floor**。全コアノード → Markdown。 |
| `svg_writer.py` | typed 描画。自己完結 SVG（縦フロー・レイアウト, Web/記事埋込）。 |
| `tui_writer.py` | typed 描画。box-drawing の monospace（llove 端末 consumer）。 |
| `schema.py` | versioned JSON Schema（`$id` でバンドル可）+ MCP `outputSchema` (`llrepr_output_schema`)。 |
| `mcp_result.py` | MCP tool result builder（compat doc 推奨形）。 |

### L1 ノードカタログ (glTF 流の閉集合 + 拡張)

`text / heading / list / table / code_block / figure / panel / container`（+ `Style` 値型）。
`figure` は URI 参照（大型/バイナリは inline せず side-channel）、`panel` は漫画コマ
(`manga-md` consumer の一級ノード)、`container` はレイアウト入れ子 (`document/section/block/row/column`)。

`Document` エンベロープは `repSchema="llrepr/0.1"`（versioned）+ glTF 流
`extensionsUsed` / `extensionsRequired`。`required` を解釈できない consumer は **fail-closed**
（描画拒否）、非 `required` 未知拡張は無視（graceful degrade）。

---

## 4. MCP 配信形 (compat doc 通り実装)

**独自 content type は不採用。** 標準 `structuredContent` に typed 木を載せ、Markdown degrade を
`text` block に併置（MCP spec が SHOULD で明文化する後方互換パターン）。汎用 MCP ルーター
(llama.cpp 等) でも壊れない。

```jsonc
result = {
  "structuredContent": { "llrepr": { "repSchema": "llrepr/0.1", "root": <typed node tree> } },
  "content": [ { "type": "text", "text": "<llrepr を Markdown に degrade した文字列>" } ]
  // 大型 (>512KB) は structuredContent を省き honest degrade → resource_link / MQTT・SSE side-channel
}
```

`outputSchema`（`llrepr_output_schema()`）を宣言すれば llrepr-aware consumer は schema validation
して typed 描画でき、非対応 consumer は併置 text を読むだけで壊れない。

---

## 5. 未配線 / 次 (honest disclosure)

- **未配線**: `llmesh/mcp/stdio_server.py` の `protocolVersion 2024-11-05 → 2025-06-18` 更新、
  実ツール (`generate_code` 等) の結果を llrepr で返す配線、`outputSchema` の tools/list 宣言は
  **未実施**。本 PoC は **llrepr パッケージ単体 + ユニットテスト**までで、stdio_server への統合は別ステップ。
- **名前確保**: GitHub 予約リポジトリは Comet 用指示文を用意済（実行待ち）。PyPI 名確保は
  placeholder package upload が必要（ブラウザ不可）。
- **次キュー #2**: 予測符号化 push PoC（llmesh, prefix-cache + warning-zone 先回り生成 +
  typed diff-stream）。発見A（予測符号化アーキテクチャ）と直結。

---

## Sources / 関連

- 設計メモ: [`repir_mcp_compat_2026_05_23.md`]({{ '/research/repir_mcp_compat_2026_05_23' | relative_url }})
- 上流: [Ideation Marathon (表現×リアルタイム)]({{ '/research/ideation_marathon_expression_realtime_2026_05_23' | relative_url }}) §論点3
- 実装: llmesh `llmesh/llrepr/` (commits `12c1a07`, `6044ba4`)
- MCP Tools spec (2025-06-18): structuredContent / outputSchema の後方互換 degrade
