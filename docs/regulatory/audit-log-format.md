# 監査ログ仕様 (Audit Log Format Specification, draft v0.1)

> **本ドキュメントは技術仕様です. 法的助言は別 docs 参照.**

## 1. 目的

各国 AI 規制 (中国 AI 弁法 / EU AI Act / 日本金融庁 AI ディスカッションペーパー /
改正サイバーセキュリティ法等) の監査要件を満たすため、FullSense
(llmesh/llive/llove) が生成する監査ログの統一フォーマットを規定.

## 2. 形式の選択

### JSON Lines (JSONL)
- 主要フォーマット
- 1 行 = 1 イベント
- append-only (改ざん検出可能性、HMAC chain で trace 検証)
- llive.brief.ledger.BriefLedger と整合
- llmesh.audit.trace.AuditTrace.verify_chain_detailed で chain 検証

### 補助フォーマット
- CSV (経営報告用、JSONL から変換)
- HTML (調達担当者向け visual、`deps --audit --html` と統合)
- SBOM (CycloneDX / SPDX, `python -m llmesh.cli.sbom`)

## 3. 必須フィールド (全イベント共通)

```jsonl
{
  "seq": 42,
  "timestamp_utc": "2026-05-18T12:34:56.789Z",
  "node_id": "fullsense-node-abc123",
  "session_id": "sess-2026-05-18-001",
  "event_type": "brief_submitted",
  "actor": "user:kazufumi@example.com",
  "hmac": "a1b2c3...",
  "prev_hash": "f7e6d5..."
}
```

- `seq` — 連番 (chain integrity)
- `timestamp_utc` — ISO 8601 UTC
- `node_id` — llmesh ノード identity
- `session_id` — Brief / agent / loop の単位
- `event_type` — イベント種別
- `actor` — user / system / agent の識別子
- `hmac` — HMAC-SHA256 (key は環境変数 `LLMESH_AUDIT_HMAC_KEY` から)
- `prev_hash` — 前 entry の hash (chain 検証用)

## 4. イベント種別 (主要)

| event_type | 発生タイミング | 追加 fields |
|---|---|---|
| `brief_submitted` | Brief API 受信 | `brief_id`, `text_hash`, `source` |
| `stimulus_built` | Stimulus 生成 | `brief_id`, `stimulus_hash` |
| `loop_started` | FullSenseLoop.process() 開始 | `brief_id`, `loop_iteration` |
| `loop_completed` | 6 stage 完了 | `brief_id`, `stages_summary` |
| `decision_made` | ActionPlan 確定 | `brief_id`, `decision`, `rationale` |
| `approval_requested` | HITL Approval Bus | `brief_id`, `action`, `approver` |
| `approval_granted` | 人間が承認 | `brief_id`, `approver`, `decision_at` |
| `approval_denied` | 人間が拒否 | `brief_id`, `approver`, `reason` |
| `tool_invoked` | Tool whitelist 経由 | `brief_id`, `tool_name`, `args_hash` |
| `outcome_recorded` | Brief 終端 | `brief_id`, `outcome`, `result_hash` |
| `pii_redacted` | PII detection (presidio) | `brief_id`, `entity_type`, `count` |
| `annotation_emitted` | IND-04 Annotation Channel | `brief_id`, `namespace`, `key` |
| `risk_alert` | Risk Score >= threshold | `brief_id`, `risk_score`, `reason` |

## 5. 保存期間 / 回転

| 規制 | 推奨保存期間 |
|---|---|
| 中国生成 AI 弁法 | 6 か月以上 (内部 governance 用は推奨 1 年) |
| EU AI Act Article 18 | **6 年以上** (高リスク AI、強制) |
| 改正サイバーセキュリティ法 (2026/01) | 6 か月以上 |
| 日本金融庁 AI ディスカッションペーパー | 業務記録法令に従う (5-10 年) |

→ デフォルト保存期間: **6 年** (EU AI Act 最厳格要件に合わせる).
ローテーション: 月次で zstd 圧縮、検証チェイン維持.

## 6. 検証コマンド

```bash
# Chain integrity
python -m llmesh audit verify <log_path> --key-hex <hmac_key>

# Timeline 表示
python -m llmesh timeline show --limit 50

# 特定 brief の lifecycle
python -m llmesh timeline task <brief_id>
```

## 7. データ越境 (関連: data-sovereignty.md)

監査ログは **PII を含み得る** ため、データ越境規制対象.
全ログを **顧客 own ストレージ** に保存し、海外バックアップ禁止が原則.

## 8. 多言語版予定

- ja (本ドキュメント) — draft v0.1
- en / zh — Week 4 整備

## 9. 関連 docs

- `cn-internal-use.md` — 中国規制
- `eu-ai-act.md` — EU 規制
- `data-sovereignty.md` — 越境
- `llmesh.audit.trace.AuditTrace` — 実装

## 改訂履歴

- 2026-05-18 — draft v0.1 作成
