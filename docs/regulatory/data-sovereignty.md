# データ越境 / データ主権 運用 documentation (draft v0.2)

> **本ドキュメントは法的助言を構成するものではありません.
> Not legal advice / 不构成法律建议.**
>
> v0.2 (2026-05-18): 「越境」の技術的定義 / runtime-check 仕様 /
> audit-log-format との接続 / 越境発生時 incident response を追加.

## 1. 概要

AI サービス / LLM 推論において、入力 / 学習データ / 出力データの越境移転を
各国規制で制限しているケースが急増. FullSense (llmesh/llive/llove) の
on-prem 完結設計は構造的にこれらの規制と整合.

## 2. 主要規制マトリックス

| 国 / 地域 | 規制 | FullSense 対応 |
|---|---|---|
| 中国 | 数据出境安全评估办法 (CAC, 2022/09) | on-prem 完結 → 越境発生せず |
| 中国 | 个人信息保护法 (PIPL, 2021/11) | 同上 |
| EU | GDPR Article 44+ (third country transfers) | 同上、Schrems II 対応 |
| EU | EU AI Act + GDPR 連携 | docs/regulatory/eu-ai-act.md 参照 |
| ロシア | 152-FZ Personal Data Act | on-prem 完結 |
| インド | DPDP Act (2023) | on-prem 完結 |
| 日本 | 改正個人情報保護法 (2022 改正) | on-prem 完結 |
| 韓国 | PIPA (2024 改正) | on-prem 完結 |
| カナダ | PIPEDA / CPPA | on-prem 完結 |
| ブラジル | LGPD | on-prem 完結 |
| 米国 | HIPAA / GLBA / 州法 (CCPA 等) | on-prem 完結 |

## 2.1 「越境」の技術的定義 (FullSense における運用基準)

各国規制で「データ越境 (cross-border data transfer)」の定義は微妙に異なるが、
FullSense は以下を **満たすか満たさないか** で機械判定する:

> **顧客の管理ネットワーク境界外 (= 顧客が直接 IP/DNS/firewall を制御
> していない宛先) への outbound network call が発生したか.**

これに該当する具体例:

| 行為 | 越境とみなすか |
|---|---|
| 顧客 LAN 内の Ollama / vLLM へ HTTP | **越境せず** |
| 顧客 VPC 内の S3-compatible storage | **越境せず** (同一物理国の場合) |
| OpenAI / Anthropic / Gemini API 呼び出し | **越境する** |
| Hugging Face Hub からのモデル download (runtime) | **越境する** |
| PyPI / Docker Hub / GitHub からの依存解決 (runtime) | **越境する** (建設時のみ実施し runtime では発生させない設計) |
| 顧客社内 mirror (gitee / 中国 pip / Nexus 等) | **越境せず** (顧客管理境界内なら) |
| クラウド telemetry / observability SaaS (Datadog 等) | **越境する** |

「物理的領土を出る瞬間」を補足する各国規制との整合性は、
**outbound network call の発生地点** をログに残すことで対応する (4.2).

## 3. なぜ on-prem 完結が全規制に対応するのか

データ越境規制の根幹は「データが該当国の物理的領域を出る瞬間」を捕捉する.
FullSense は:

- LLM 推論を **顧客 own インフラ内で完結** (cloud LLM 不要)
- メモリ層 / 監査ログ / 出典追跡 すべて **顧客 own ストレージ**
- MCP プロトコル経由通信は **顧客 own ネットワーク内**
- 外部 API call は **オプトイン** で、デフォルトはゼロ

→ データが顧客の管理境界を越える瞬間が architecture-level で発生しない.
これは越境規制の compliance を構造的に担保する.

## 4. 検証可能性

`llmesh deps --audit --runtime-check` (Phase 2 実装予定) で:
- 起動時 / 実行時の外部 API call を監視
- 検出された outbound traffic を log + alert
- 「ゼロ越境」を data で証明可能

Phase 1 (本 v3.2 α) は静的解析のみ. 動的検証は Phase 2.

## 5. 推奨運用

- 全 LLM backend を **on-prem deployment** にする (Ollama / vLLM / MindServe 等)
- llmesh `--no-external-llm` flag (Phase 2) で外部 API 完全禁止
- 監査ログを **顧客 own ストレージ** に保存 (`LLIVE_BRIEF_LEDGER_DIR` 等)
- 定期的な `deps --audit --runtime-check` で外部通信ゼロを検証

## 6. データ越境が発生し得るシナリオ (注意)

以下は越境が発生し得るため、規制対応企業では特に注意:

- 外部 LLM API (OpenAI / Anthropic / Gemini) を呼び出す場合
- クラウドストレージ (S3 / Azure Blob) を使う場合
- 外部 monitoring / observability SaaS を併用する場合
- パッケージマネージャ (PyPI / Docker Hub) のレジストリは原則越境

FullSense は最後の点 (PyPI 等) を gitee mirror / 中国 pip mirror /
社内 marketplace で対応可能.

## 7. 多言語版予定

- ja (本ドキュメント) — draft v0.1
- en / zh — Week 4 整備

## 8. 参考文献

- 中国 CAC 数据出境安全评估办法
- EU GDPR Article 44 - 50
- 個人情報保護委員会 (PPC) 越境移転ガイドライン
- IAPP Cross-Border Data Transfer Guide
- Schrems II (CJEU C-311/18) judgment

## 改訂履歴

- 2026-05-18 — draft v0.1 作成
