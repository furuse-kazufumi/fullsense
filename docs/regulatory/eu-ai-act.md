# EU AI Act 対応運用 documentation (draft v0.2)

> **本ドキュメントは法的助言を構成するものではありません.
> Not legal advice / 不构成法律建议.**
> 各企業の法務部門 / EU 規制対応専門弁護士による確認を推奨します.
>
> v0.2 (2026-05-18): Article 別 mapping (12/13/14/18/19/50/72/73/99)、
> 保管期間の Article 分離 (18=技術文書 10 年 / 19=logs 最低 6 か月)、
> post-market monitoring + incident reporting と audit-log 接続を追加.

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

### 5.1 Article 別 mapping (主要条文)

> 各 Article の正確な要件は Regulation (EU) 2024/1689 原文を必ず参照.
> 本表は実装基盤がどの条文に応える設計かを示す技術 mapping.

| Article | 要件 (概要) | FullSense 対応 module / event |
|---|---|---|
| **Art.12** | 自動 logging を備えること (high-risk provider 義務) | llive `BriefRunner` + `llmesh.audit.trace.AuditTrace`. `audit-log-format.md` の event 群がこの logging を満たす |
| **Art.13** | provider が deployer に対し透明性 (intended purpose / 限界 / 性能) を documentation で提供 | `docs/regulatory` シリーズ + REQUIREMENTS.md / ROADMAP.md |
| **Art.14** | human oversight (人間の override / intervention 可能性) を embedded すること | llive HITL Approval Bus + `/api/v1/hitl/respond` (Phase h.5) — architectural-level に組込済 |
| **Art.18** | 技術文書 (Annex IV) を **AI system が市場 placed されてから 10 年保管** | `docs/regulatory` + 各 v0.x の Git 履歴 + zstd archive (`$LLMESH_AUDIT_DIR/archive/`) |
| **Art.19** | 自動生成 logs を **意図用途に応じた期間、最低 6 か月** 保管 | `audit-log-format.md` 5 章: 既定 6 年 (EU 高リスク前提) — `LLMESH_AUDIT_RETENTION_YEARS` で短縮可 |
| **Art.50** | deployer は AI 出力が AI 由来であることを natural person に開示 (限定リスク AI / emotion recognition / deepfake 等) | Annotation Channel `core:ai_generated=true` を llove 描画層が明示。`(EU) AI 由来` ラベルを必須出力 |
| **Art.72** | post-market monitoring system (PMM) — provider 義務 | `outbound_call_attempted` + `risk_alert` + Annotation 集計を週次 `llmesh timeline report` で PMM 報告書化 |
| **Art.73** | serious incident reporting — 15 日以内 (基本) / 即座 (重大障害) | `audit-log-format.md` 9 章 + `data-sovereignty.md` 6.1 incident response プロセスと統合運用 |
| **Art.99** | 罰則 — 禁止 AI 違反 最大 35M EUR or 全世界売上 7%; その他 高額 15M EUR or 3% | FullSense は禁止 AI を構造的に避ける設計 (リスク分類 = High 以下) |

## 6. 推奨運用 (高リスク AI として使う場合)

- Annotation Channel に `eu-ai-act:risk-tier=high` 等を明示
- 全 user action を Approval Bus 経由で監査ログに残す
- 出力 rendering で `ai-generated` ラベル必須 (Art.50)
- 定期的な Risk Score モニタリング + アラート (Art.72 PMM)
- **保管期間** (注: Article 18 と 19 は対象が違うので分離して扱う):
  - 技術文書 (Annex IV) を **市場投入後 10 年** 保管 (Art.18)
  - 自動 logs を **意図用途に応じた期間、最低 6 か月** 保管 (Art.19) —
    FullSense default は 6 年 (高リスク前提)
- serious incident は **15 日以内** に所轄当局へ報告 (Art.73). 重大障害
  (人命 / インフラ / 基本権侵害) は即時報告

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
