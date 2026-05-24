---
layout: default
title: "予測符号化 push PoC — 発見A の具現化"
parent: "Research"
nav_order: 95
---

# 予測符号化 push PoC — 発見A の具現化 (2026-05-24)

> FullSense 実装キュー #2「予測符号化 push」を **llmesh** に着地。ideation marathon
> ([[ideation_marathon_expression_realtime_2026_05_23]]) の **発見A=予測符号化アーキテクチャ**を
> 産業アラーム説明で実証した記録。表現層は [[llrepr_poc_2026_05_24]]。

---

## 1. 何を実証したか

神経科学の**予測符号化**（予測を先に生成し、**予測誤差だけ**を伝播）を、SPC アラーム説明に適用:

```
センサ → SPC ──warning-zone──> [説明を投機生成し llrepr 化してキャッシュ]   ← 先回り(負レイテンシ)
                  │
                  └──alarm確定──> 予測 vs 実際の typed diff(=予測誤差)だけ push
                  └──warning解除─> 投機を破棄(空振りを安く回避)
                  └──cold alarm──> 投機なし → full document push
```

確定の瞬間に説明を**作り始めない**（warning 時に済ませてある）。流れるのは**差分だけ**。

## 2. 実装 (llmesh, commits 12c1a07/6044ba4/e628d10/ea0ba16/308efab/5fbdb07)

- **`llmesh/llrepr/diff.py`** — 2 つの llrepr Document 間の typed diff/patch（JSON-Patch 風,
  round-trip 保証）。`prediction_error(ops)=op 数`が投機精度。表現を再送せず**差分=予測誤差**を運ぶ核。
- **`llmesh/predictive_push/`** — `PredictivePush` 状態機械（warning→投機 / alarm→diff push
  (incident_id 再利用) / nominal→破棄 / cold→full）+ `zones`(Shewhart 2σ-3σ / CUSUM warn_frac×h)
  + `report_repr`(IncidentReport→安定形 llrepr) + `PredictiveMetrics` + 実行可能 `demo`。
  既存 `CUSUMChart` + `LLMExplainer` を**合成**（置換せず）。
- **egress sinks** — `CallbackSink`(host が WebSocket/SSE/独自 bus へ) / `JsonlSink`(依存なしの実
  typed diff-stream) / `MqttPushSink`(optional, paho)。compat note の「MQTT/SSE side-channel」を実体化。
- **MCP 2025-06-18 近代化** (`llmesh/mcp/stdio_server.py`) — protocolVersion 更新 + `outputSchema` +
  `structuredContent` 併置。llrepr が structuredContent で MCP を渡る前提（後方互換維持）。
- 計 **108 tests green**（llrepr + diff + predictive_push + sinks + mcp）。

## 3. honest disclosure

- **主たる利点は「負レイテンシ」**（説明が確定前に出来ている）。ペイロード削減は**大型表現でのみ**効く
  — 小さな doc では 1-op diff（JSON pointer + 値）は full doc より小さくない。誇張しない。
- **実 LLM explainer は未配線**（現状テンプレ。`LLMExplainer` の `llm` callable に backend +
  PromptFirewall/PrivacySummarizer を通す配線が残）。
- 投機が外れた warning（空振り）は計算を捨てる — `speculations_wasted` で正直に計上。
- server-initiated 連続 push の MCP 標準は未確定 → 当面 side-channel（sink）で運ぶ二層構成。

## 4. 発見A との接続

論点1（評価=予測 vs 観測の誤差）/論点3（push は typed diff）/論点4（warning-zone 先回り）を**1 原理で貫く**
という marathon の統合発見が、最小だが動く形で具現化した。llrepr（表現の型）+ diff（予測誤差）+
predictive_push（先回り）+ sink（差分伝播）が発見A の 4 部品に対応する。

## Sources / 関連

- [[ideation_marathon_expression_realtime_2026_05_23]] §論点3/4 + 発見A
- [[llrepr_poc_2026_05_24]] — 表現層
- 実装: llmesh `llmesh/llrepr/` + `llmesh/predictive_push/` + `llmesh/mcp/stdio_server.py`
