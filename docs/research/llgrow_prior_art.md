---
layout: default
title: "llgrow — Prior Art Survey"
parent: "Research"
nav_order: 2
---

# llgrow — Prior Art Survey (2026-05-20)

> AI agent (Claude Opus 4.7) が WebSearch + 既知 OSS 知識から 800 字以内で
> 生成した調査メモ. `spinoff_ideas_2026_05.md` の llgrow を具体化する前提資料.

## Prior art

### HITL content automation (商用)

Jasper / copy.ai / ContentBot は LLM テンプレートと人手レビューを組合せる
SaaS 群. すべて cloud-only, 監査ログは限定的, 企業向けで個人開発者用途には
設計されていない. OSS 領域では [Mautic](https://github.com/mautic/mautic)
(marketing automation の de-facto OSS) や
[n8n](https://github.com/topics/marketing-automation) が AI ノードで content
drafting を可能にするが, コンテンツ品質 evaluator や HITL 承認は外付け.

### Academic side

HITL marketing copy 生成は 2025 年に急速に体系化された.

- INFORMS Marketing Science の [Sponsored Search Advertising 研究](https://pubsonline.informs.org/doi/10.1287/mksc.2023.0611) は "HITL > pure LLM > human" を示す
- [LLMs for Customized Marketing at Scale (arXiv 2506.17863)](https://arxiv.org/html/2506.17863v1) は RAG + 人手承認の A/B で engagement 有意増を報告
- [AI-Human Hybrids for Marketing Research (Arora et al., 2025)](https://journals.sagepub.com/doi/abs/10.1177/00222429241276529) は collaborator 型 HITL を一般化

### LLM-as-judge for copy

faithfulness / readability / brand consistency を direct scoring で計る枠組みが
定着しつつあり, [Evidently AI の総説](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
と [arXiv 2506.13639](https://arxiv.org/pdf/2506.13639) が rubric 設計・bias
抑制の現状ベストプラクティス.

### Self-host stack

[Langfuse](https://github.com/langfuse/langfuse) (OSS, self-host) は prompt
mgmt + LLM-as-judge + 監査ログを既に提供, コンテンツ用途への流用が現実的.
OSS 普及自動化に特化した repo は [ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills)
等が散見されるが cloud LLM 前提.

## Differentiation gap

- **on-prem + audit log + HITL + 個人開発者 OSS 配信** の 4 条件同時充足は空白.
  Langfuse は基盤層, Mautic は配信層に留まり, 両者を橋渡しする vertical なし.
- 「OSS 作者本人の文体・哲学 (FullSense 6 規約等) を memory 化して draft する」
  観点は academic にも commercial にも未踏. llive の 4 層メモリ + Approval Bus
  を流用できる優位.
- 効果測定 (Qiita LGTM / GitHub star / PyPI DL の自動フィードバック) を loop に
  閉じた OSS は未確認.

## Recommended approach for llgrow

1. **基盤を作らず llive + Langfuse を再利用** — llive の Approval Bus を
   HITL gate, Langfuse を judge/audit 層に.
2. **vertical layer 3 件のみ新規実装**: (a) 作者 voice memory,
   (b) channel-specific drafter (Qiita / LinkedIn / X / GitHub Issue 返信),
   (c) 効果メトリクス収集 (Qiita / GitHub API).
3. **honest disclosure を内蔵** — engagement 異常値は内訳開示を強制し brand
   毀損を防ぐ.
4. **PR 戦術**: 「llgrow が llgrow 自身を売る」dogfooding demo を SNS 拡散用に
   最初に作る.

## Sources

- INFORMS Marketing Science — LLMs for Sponsored Search: <https://pubsonline.informs.org/doi/10.1287/mksc.2023.0611>
- arXiv 2506.17863 — LLMs for Customized Marketing: <https://arxiv.org/html/2506.17863v1>
- Sage Journals — AI-Human Hybrids for Marketing: <https://journals.sagepub.com/doi/abs/10.1177/00222429241276529>
- Evidently AI — LLM-as-a-judge guide: <https://www.evidentlyai.com/llm-guide/llm-as-a-judge>
- arXiv 2506.13639 — Empirical Study of LLM-as-a-Judge: <https://arxiv.org/pdf/2506.13639>
- Langfuse OSS: <https://github.com/langfuse/langfuse>
- Mautic OSS: <https://github.com/mautic/mautic>
- GitHub topic: marketing-automation: <https://github.com/topics/marketing-automation>
- ericosiu/ai-marketing-skills: <https://github.com/ericosiu/ai-marketing-skills>
