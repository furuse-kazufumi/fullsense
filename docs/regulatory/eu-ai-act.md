# EU AI Act 対応運用 documentation (draft v0.1)

> **本ドキュメントは法的助言を構成するものではありません.
> Not legal advice / 不构成法律建议.**
> 各企業の法務部門 / EU 規制対応専門弁護士による確認を推奨します.

## 1. 対象 — EU AI Act の概要

EU AI Act (Regulation (EU) 2024/1689) は 2024 年 8 月発効、段階的施行:

- 2025/02 — 禁止 AI システムの即時禁止
- 2025/08 — 汎用 AI モデル (GPAI) 義務
- 2026/08 — 高リスク AI システムの本格義務化
- 2027/08 — 既存システム移行完了

## 2. リスク分類

| 分類 | 例 | FullSense fit |
|---|---|---|
| 禁止 (Unacceptable) | social scoring / 大規模顔認証 | FullSense は対象外設計 |
| 高リスク (High) | 信用評価 / 採用 / 医療 / 教育 / 重要インフラ | llive HITL + 監査ログで対応 |
| 限定リスク (Limited) | chatbot / deepfake | Annotation Channel で識別 emit |
| 最小リスク (Minimal) | spam filter / 業務効率化 AI | 標準利用 |

## 3. 高リスク AI システムの主要義務

| 義務 | FullSense 対応 |
|---|---|
| リスク管理システム | llive Risk Score (実装済) |
| データガバナンス | llmesh on-prem 完結 + audit log |
| 技術文書 (Technical Documentation) | 本 docs シリーズ + REQUIREMENTS.md + ROADMAP.md |
| 自動ログ | llmesh + llive Approval Bus + SqliteLedger |
| 透明性 (出力が AI 由来であることの明示) | Annotation Channel `ai-generated` ラベル emit |
| 人間による監督 (Human Oversight) | llive HITL Approval Bus (architecture-level) |
| 正確性 / 堅牢性 / サイバーセキュリティ | llmesh deps --audit (origin / supply risk 可視化) |
| 適合性評価 (CE marking) | (各企業の責任、本 OSS は技術基盤を提供) |

## 4. 汎用 AI モデル (GPAI) の義務

| 義務 | FullSense 対応 |
|---|---|
| 学習データの概要公開 | llive memory layer audit log (社内利用) |
| 著作権法遵守 | (LLM 提供元の責任、ファインチューニング時は要追跡) |
| Systemic Risk (10^25 FLOPS 超) | (個人開発者の責任範囲外) |

## 5. FullSense の architecture-level fit

| EU AI Act 要件 | FullSense module | 状態 |
|---|---|---|
| Risk management | llive Risk Score | 実装済 |
| Data governance | llmesh on-prem | 実装済 |
| Logging | llive Approval Bus + SqliteLedger | 実装済 (Brief 経由) |
| Transparency labels | Annotation Channel `ai-generated` | 要設計 (Week 3-4) |
| Human oversight | llive HITL Approval Bus | 実装済 |
| Cybersecurity / robustness | llmesh deps --audit | α 実装済 (本日 commit) |
| Technical documentation | docs/regulatory + REQUIREMENTS.md | 整備中 |

## 6. 推奨運用 (高リスク AI として使う場合)

- Annotation Channel に `eu-ai-act:risk-tier=high` 等を明示
- 全 user action を Approval Bus 経由で監査ログに残す
- 出力 rendering で `ai-generated` ラベル必須
- 定期的な Risk Score モニタリング + アラート
- 技術文書を 6 年以上保管 (Article 18)

## 7. 公開する場合の手続 (参考)

- CE marking — 適合性評価 (内部 or notified body)
- EU Database 登録 (高リスク)
- 市場後監視 (Article 72)
- 重大インシデント報告 (Article 73)

これらは企業の責任で、FullSense は技術基盤を提供.

## 8. 多言語版予定

- ja (本ドキュメント) — draft v0.1
- en — Week 4 整備
- zh — Week 4 整備
- de / fr — Phase 2 (EU 主要市場向け)

## 9. 参考文献

- [Regulation (EU) 2024/1689 — Artificial Intelligence Act](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)
- European Commission AI Act 公式ガイダンス
- EDPB (European Data Protection Board) AI Act + GDPR 接続性ガイドライン

## 改訂履歴

- 2026-05-18 — draft v0.1 作成 (戦略思索 PART 3 章 10 + Week 2 残)
