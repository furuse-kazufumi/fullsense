---
layout: default
title: "llrisk — Continuous Risk Tracking Prior Art"
parent: "Research"
nav_order: 6
---

# llrisk — Continuous AI Risk Tracking Prior Art (2026-05-20)

> AI agent (Claude Opus 4.7) が WebSearch + 既知 OSS 知識から 800 字以内で
> 生成した調査メモ. `spinoff_ideas_2026_05.md` の llrisk 候補を具体化する
> 前提資料.

## Prior art

### AI-driven GRC (Layer L4)

ServiceNow は 2025 に AI Control Tower + AI Agent Fabric を投入し, AI agent の
compliance metrics / risk score をダッシュボード化. OneTrust は privacy 起点で
third-party risk + ESG + AI insights を拡張. LogicGate は no-code モジュール型.
いずれも **enterprise SaaS, cloud-first, AI は predictive analytics 補助** に
留まり, LLM が継続的に risk register を生成・更新する vertical ではない.

### Continuous risk monitoring in DevOps

Snyk は reachability analysis + EPSS / CVSS 合成 score でノイズ 30-70% 削減.
Trivy (OSS, Apache-2.0) は severity ベース, Dependabot は自動 PR 生成.
**AI scoring は Snyk のみ "curated metadata" 程度で, LLM 推論はしていない** —
静的 DB ルックアップ + heuristic.

### LLM × project risk register

Collier 2025 (Risk Analysis 誌) は ChatGPT が FMEA 自動化より **brainstorm
失敗モード + mitigation 案** に強いと結論. arXiv 2510.06343 は林業 cyber-physical
で LLM が draft 報告書を生成し expert oversight 必須. arXiv 2505.17084 は
非確率的 risk management を LLM 系に応用. **専門 vertical で個別実装はあるが,
汎用 "AI が continuous に risk register を保守" する OSS は未確立**.

### Reputation monitoring

Semrush / Meltwater GenAI Lens / Brand24 / Profound 等が **LLM の brand 言及 +
sentiment** を tracking. ただし **全て commercial SaaS** で, OSS + on-prem は
事実上空白.

### Developer burnout / mental health

CMU Raman 2020 + Heath 2025 が OSS maintainer の trace data (PR コメント /
commit cadence) から burnout 兆候を検出する mixed-method 研究を提示. Aquant 等の
commercial 予測モデルもあるが, **個人開発者向け on-prem framework は不在** —
研究止まりで実装は trace 分析プロトタイプのみ.

## Gap

**6 軸 (法務 / 技術 / ビジネス / 健康 / レピュ / セキュ) × 個人開発者 +
on-prem + LLM-driven + 持続トラッキング** を全部満たす OSS は皆無:

- GRC SaaS は enterprise 専用, 個人非対象, cloud 強制
- DevOps scanner は技術 / セキュ 2 軸のみ, LLM 推論なし
- Burnout / reputation 研究は単軸プロトタイプ
- **Multi-dimensional risk fusion (phasic + tonic, 短期×長期)** という Cognitive
  Mesh TonicRiskMonitor の発想は学術側にも未踏

## Recommended approach

1. **llive TonicRiskMonitor の 1m 上空拡張** として実装. 既存 phasic / tonic
   二層を 6 dimension に並列化.
2. **OSS trace + LLM brainstorm hybrid**: Raman 2020 の trace 手法 + Collier 2025
   の "LLM = mitigation brainstorm" を fusion.
3. **OneTrust / ServiceNow を見ない**: enterprise GRC は別物. **個人開発者の
   "毎朝の risk 6 軸ダッシュボード"** を MVP に.
4. **FullSense 整合**: on-prem LLM (llmesh) + 監査ログ (Approval Bus) + HITL (llove)
   を再利用 — 新規実装は risk fusion engine のみ.
5. **差別化軸**: "個人 OSS 開発者の cofounder" ポジショニング. GRC SaaS と被らない.

## Sources

1. ServiceNow FY2025 8-K (AI Control Tower): <https://www.sec.gov/Archives/edgar/data/0001373715/000137371525000274/erq2fy25.htm>
2. Top 10 GRC Tools 2025 (OneTrust / LogicGate): <https://www.cloudnuro.ai/blog/top-10-governance-risk-and-compliance-grc-tools-for-it-leaders-2025-guide>
3. Snyk vs Trivy 2026 (reachability + EPSS): <https://www.aikido.dev/blog/snyk-vs-trivy>
4. Collier 2025: LLM × product risk assessment: <https://onlinelibrary.wiley.com/doi/10.1111/risa.14351>
5. arXiv 2510.06343: LLM Cybersecurity Risk Assessment: <https://arxiv.org/pdf/2510.06343>
6. arXiv 2505.17084: Non-probabilistic risk for LLM systems: <https://arxiv.org/pdf/2505.17084>
7. Semrush: 8 Best LLM Brand Monitoring Tools 2026: <https://www.semrush.com/blog/llm-monitoring-tools/>
8. Raman et al. 2020 (CMU): Stress & Burnout in OSS: <https://cmustrudel.github.io/papers/raman20toxicity.pdf>
9. Heath 2025: OSS Burnout Report: <https://mirandaheath.website/static/oss_burnout_report_mh_25.pdf>
10. Aquant Employee Burnout Prediction Model: <https://discover.aquant.ai/employee-burnout-prediction>
