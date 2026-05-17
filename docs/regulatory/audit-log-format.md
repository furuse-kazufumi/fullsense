# 監査ログ仕様 (Audit Log Format Specification, draft v0.2)

> **本ドキュメントは技術仕様です. 法的助言は別 docs 参照.**
>
> v0.2 (2026-05-18): HMAC chain アルゴリズム / hash 規則 / PII redaction 順序 /
> F25 Phase h との接続を確定. ファイルパス default / key rotation 規則も追加.

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

- `seq` — 連番 (chain integrity, 0 起点、非負整数)
- `timestamp_utc` — ISO 8601 UTC, ミリ秒精度 (`YYYY-MM-DDTHH:MM:SS.sssZ`)
- `node_id` — llmesh ノード identity (3.3)
- `session_id` — Brief / agent / loop の単位 (3.3)
- `event_type` — イベント種別 (4)
- `actor` — user / system / agent の識別子 (`user:<email>` / `system:<component>` / `agent:<id>`)
- `hmac` — HMAC-SHA256 hex (key は env `LLMESH_AUDIT_HMAC_KEY`, 計算規則は 3.1)
- `prev_hash` — 前 entry の `hmac` 値 (genesis は 64 個の `0`)

### 3.1 HMAC chain アルゴリズム

各 entry の `hmac` は以下で計算する:

```
canonical = json.dumps(entry_without_hmac, sort_keys=True, separators=(",", ":"))
hmac      = HMAC-SHA256(key=LLMESH_AUDIT_HMAC_KEY, msg=canonical).hexdigest()
```

- `entry_without_hmac` は当該 entry から `hmac` フィールドを **除外** した
  dict (他フィールドはすべて含む、`prev_hash` も含む).
- `prev_hash` は 1 つ前の entry の `hmac` 値 (16 進 64 文字). 最初の
  entry は `prev_hash = "0" * 64` (genesis).
- JSON シリアライズは **キーの辞書順ソート + space 圧縮** (`sort_keys=True`,
  `separators=(",", ":")`) で deterministic に固定. Python 標準
  `json.dumps` のこの 2 設定を変えないこと.
- 検証は逆順 — `verify_chain_detailed` は seq=0 から再計算し、
  `hmac` と `prev_hash` 両方を検査する.

### 3.2 hash 計算規則 (text_hash / args_hash / result_hash)

各 hash フィールドは **SHA-256 hex** (`hashlib.sha256(b).hexdigest()`).

| field | 入力 |
|---|---|
| `text_hash` | Brief.goal を UTF-8 encode したバイト列 (**PII redaction 後**) |
| `stimulus_hash` | Stimulus.content を UTF-8 encode (**PII redaction 後**) |
| `args_hash` | tool 呼び出し時 `args` dict を 3.1 と同じ canonical JSON にして UTF-8 |
| `result_hash` | tool / Brief outcome `result` dict を canonical JSON にして UTF-8 |

PII redaction 前の原文は **ログに残さない** (3.4 と PII docs 参照).

### 3.3 node_id / session_id 生成規則

`node_id`:
- 初回起動時に `~/.llmesh/node_id` に永続化 (`uuid.uuid4().hex[:16]`).
- 環境変数 `LLMESH_NODE_ID` が設定されていればそれを優先 (cluster 用途).
- 形式: 16 文字 hex (`[a-f0-9]{16}`). 接頭辞 `fullsense-node-` は表示専用.

`session_id`:
- Brief / agent / loop の生存期間に紐づく. 1 つの `submit_brief` 呼び出し
  = 1 つの `session_id`.
- 形式: `sess-YYYY-MM-DD-<8hex>` (`sess-2026-05-18-a1b2c3d4`).
- HITL Approval の `approval_requested` / `approval_granted` も同一
  `session_id` を継承.

### 3.4 PII redaction 順序

Brief 受信から audit log 記録までの順序:

```
1. raw Brief 受信 (HTTP / MCP)
2. PII detector (presidio) で entity 抽出 → `pii_redacted` event を emit
3. redacted text で text_hash を計算
4. brief_submitted event を emit (text_hash 入り、原文は含まない)
5. 以降の stimulus_built / loop_started / ... も redacted 入力で進む
```

`pii_redacted` event が `brief_submitted` より **先** に来る (`seq` が小さい)。
順序逆転は chain integrity 違反として `verify_chain_detailed` が flag する.

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

## 8. ファイルパス default と key rotation

### 8.1 default パス

| データ | path | 形式 |
|---|---|---|
| 当月 active ログ | `$LLMESH_AUDIT_DIR/active/YYYY-MM.jsonl` | JSONL |
| 月次 archive | `$LLMESH_AUDIT_DIR/archive/YYYY-MM.jsonl.zst` | zstd |
| HMAC key (active) | `$LLMESH_AUDIT_DIR/keys/current.key` | 32B random |
| HMAC key (rotated) | `$LLMESH_AUDIT_DIR/keys/<seq-range>.key` | 32B random |

`LLMESH_AUDIT_DIR` 既定: `~/.llmesh/audit/` (Windows: `%APPDATA%\llmesh\audit\`).

### 8.2 key rotation

- 月次または `LLMESH_AUDIT_HMAC_ROTATE_AFTER` (env, default 1,000,000 entries)
  到達時に rotate.
- rotate 時に **`hmac_key_rotated` event** を新 key で書き、当該 entry の
  `meta.previous_key_fingerprint` に旧 key の SHA-256[:16] を残す.
- 旧 key は `keys/<start_seq>-<end_seq>.key` で archive (削除しない、
  EU AI Act 6 年要件と同期間保持).
- 検証時は `seq` レンジに対応する key を読み込む — `verify_chain_detailed`
  が自動で切り替える.

## 9. F25 Phase h との接続 (audit-log と Brief E2E)

F25 Phase h (`docs/design/f25-phase-h-e2e.md`) で実装する llove engine
→ llive Brief Runner の HTTP/SSE 経路は、すべて本 spec の event を発火する.

| Phase h step | 発火する audit event | 備考 |
|---|---|---|
| `POST /api/v1/brief/submit` 受信 | `brief_submitted` | request body は redaction 後 hash で記録 |
| Stimulus 構築 | `stimulus_built` | |
| FullSenseLoop 6 stage 進行 | `loop_started` → 各 stage は内部、`loop_completed` | |
| Inner monologue (LLM call) | `tool_invoked` (`tool_name="llm.generate"`) | `cnmesh:<model>` の場合は actor に backend を含める |
| Annotation Channel emit | `annotation_emitted` (`namespace`/`key`) | SSE で配信される value はログには含めない (hash のみ) |
| ActionPlan → HITL | `approval_requested` (h.5) | `/api/v1/hitl/respond` で `approval_granted` / `approval_denied` |
| Brief 終端 | `outcome_recorded` | |

実装は llive 側 `BriefRunner` の各 stage hook で `llmesh.audit.trace.AuditTrace`
に書き込む. llove engine は **書き込みを行わず**、SSE と HTTP の薄い proxy
に徹する (audit log の source of truth は llive 側 1 箇所).

## 10. 多言語版予定

- ja (本ドキュメント) — draft v0.1
- en / zh — Week 4 整備

## 9. 関連 docs

- `cn-internal-use.md` — 中国規制
- `eu-ai-act.md` — EU 規制
- `data-sovereignty.md` — 越境
- `llmesh.audit.trace.AuditTrace` — 実装

## 改訂履歴

- 2026-05-18 — draft v0.1 作成
- 2026-05-18 — draft v0.2:
  - 3.1 HMAC chain アルゴリズム確定 (canonical JSON + sort_keys + HMAC-SHA256)
  - 3.2 hash 計算規則 (text_hash / args_hash / result_hash) を SHA-256 で固定、
    すべて PII redaction 後の値であることを明示
  - 3.3 node_id / session_id 生成規則 (LLMESH_NODE_ID env / sess-YYYY-MM-DD-<8hex>)
  - 3.4 PII redaction 順序を確定 (pii_redacted → brief_submitted の seq 順序固定)
  - 8 ファイルパス default (active/archive/keys ディレクトリ構成) と
    key rotation 規則 (hmac_key_rotated event, 月次 or 100 万 entry)
  - 9 F25 Phase h との接続 — Phase h の各 step が発火する event 表を追加.
    audit log の source of truth は llive 側に集約.
