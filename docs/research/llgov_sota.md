---
layout: default
title: "llgov — AI Governance / Compliance SOTA"
parent: "Research"
nav_order: 5
---

# llgov — AI Governance / Compliance SOTA (2026-05-20)

> AI agent (Claude Opus 4.7) が WebSearch + 既知 OSS 知識から 800 字以内で
> 生成した調査メモ. `spinoff_ideas_2026_05.md` の llgov 候補を具体化する
> 前提資料.

## OSS / SaaS matrix

| 層 | 代表 | 強み | 弱み |
|---|---|---|---|
| **Runtime guardrails (OSS)** | NeMo Guardrails (Colang, 5 rail), Guardrails AI, ShieldGemma, **MS Agent Governance Toolkit (2026-04)** | 入出力/対話制御, OWASP Agentic 10 全網羅 | ガードレール止まりで規制マッピング無し |
| **Policy-as-code** | OPA/Rego, AWS Cedar (formal verif), Toolkit が両対応 | tool-calling 層で sub-ms 拒否, エージェントを信用しない設計 | 規制条文 → policy 変換は手作業 |
| **Tamper-evident log (OSS)** | AIR Blackbox (HMAC-SHA256), VeritasChain Protocol, agent-audit-log-examples | EU AI Act Art.12 logging を直接満たす | 単体機能のみ, 規制全体は別途 |
| **Governance SaaS** | Credo AI, Holistic AI, OneTrust, MS Purview AI Hub, IBM OpenPages | EU AI Act / NIST RMF / ISO 42001 policy pack, evidence 自動収集 | クラウド前提, 年額数千万円, on-prem 不可 |

## Regulatory coverage gap

- EU AI Act Art.9-15 (risk mgmt / data gov / logging / transparency /
  human oversight / accuracy) を **自動検証する OSS は不在** — Prediction Guard
  が API 層で部分実装. Support instruments は EU 公式が 2026 Q2 公開予定で未確定.
- 中国 AI 弁法 (内部利用 filing 免除) を扱う OSS / SaaS は皆無.
- 既存 SaaS は SOC2 / GDPR 寄り, HIPAA + EU AI Act + 中国弁法 を
  **横断する on-prem スタックは空白**.
- 個人 / 小規模 (年商 $1M 未満) 向け価格帯製品が無い.

## Recommended approach for llgov

1. **基盤**: ApprovalBus + SqliteLedger + PromptLinter を OPA/Cedar policy engine
   の **wrapper** として再構成 (MS Toolkit と相互運用, Anthropic / Bedrock /
   Ollama 共通 hook).
2. **Audit**: AuditTrace を HMAC chain (BLAKE3 推奨) に強化, VeritasChain
   互換でエクスポート → Art.12 ready.
3. **Regulatory pack**: EU AI Act Art.9-15 / 中国弁法 / GDPR / SOC2 を
   **Rego rule + YAML evidence schema** で配布 (Credo AI policy pack の OSS 版).
4. **差別化 4 軸**: on-prem inference / 多規制横断 / policy-as-code / HMAC ledger
   — **FullSense Approval Bus と直結**して enterprise SaaS の年額数千万から
   個人 $0 まで連続スペクトルを構成.

## References

- MS Agent Governance Toolkit: <https://opensource.microsoft.com/blog/2026/04/02/introducing-the-agent-governance-toolkit-open-source-runtime-security-for-ai-agents/>
- NeMo Guardrails: <https://github.com/NVIDIA-NeMo/Guardrails>
- OPA vs Cedar (Permit.io): <https://www.permit.io/blog/opa-vs-cedar>
- AIR Blackbox HMAC chain: <https://airblackbox.ai/>
- VeritasChain audit trail: <https://dev.to/veritaschain/building-tamper-evident-audit-trails-a-developers-guide-to-cryptographic-logging-for-ai-systems-4o64>
- EU AI Act Art.9-15 deadline 2026-08: <https://www.raconteur.net/global-business/eu-ai-act-compliance-a-technical-audit-guide-for-the-2026-deadline>
- Credo AI vs OneTrust: <https://www.credo.ai/lp/onetrust-vs-credo-ai>
- MS Purview AI Hub limits: <https://www.epcgroup.net/microsoft-purview-ai-governance-compliance-guide>
- Prediction Guard EU AI Act tools: <https://predictionguard.com/blog/best-eu-ai-act-compliance-tools-for-enterprise-ai-programs-in-2026>
