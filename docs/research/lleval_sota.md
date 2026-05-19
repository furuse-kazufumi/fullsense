---
layout: default
title: "lleval — SOTA Survey"
parent: "Research"
nav_order: 1
---

# lleval — SOTA Survey (2026-05-20)

> AI agent (Claude Opus 4.7) が WebSearch + 既知 OSS 知識から
> 800 字以内で生成した調査メモ. `spinoff_ideas_2026_05.md` の lleval
> 候補を具体化する前提資料.

## SOTA matrix

| Framework | 主機能 | 差別化 | on-prem | honest disclosure | progressive size |
|---|---|---|---|---|---|
| OpenAI Evals | YAML/Python eval テンプレ | OpenAI 公式・gpt-4 judge 標準 | △ (API 前提) | × | × |
| LMSYS Chatbot Arena | 人間 pairwise + Elo | 人間票ベンチの de facto | × | × | × |
| HELM (Stanford CRFM) | 多軸 (acc/bias/robust/efficiency) | 7+ scenarios × 多軸メトリクス | △ | △ (多軸表示のみ) | × |
| MMLU / BBH / HellaSwag | 静的 benchmark | 知識/推論カバレッジ | ○ | × | × |
| promptfoo | YAML test、CI 統合、red-team | OSS の CI 親和性 | ○ | × | × |
| DeepEval | pytest 風、14+ metric、G-Eval | Python OSS、unit-test 思想 | ○ | △ (metric 分解) | × |
| Phoenix (Arize) | OpenInference trace + eval | OTel trace 統合 | ○ | △ (span 単位 drill) | × |
| Langfuse | trace + eval + cost | LLM ops の cost 可視化 | ○ | △ (cost/latency 分離) | × |
| TruLens | RAG feedback function | RAG triad (groundedness/relevance/context) | ○ | △ | × |
| Ragas | RAG 特化 metric | faithfulness/context_recall 等 | ○ | × | × |

## LM-as-judge の精度

GPT-4 judge は人間と 80%+ 一致するが、

- (a) **position bias** — 先頭/後尾を優遇
- (b) **self-preference bias** — 自モデル出力を高評価 (Panickssery 2024)
- (c) **verbosity bias** — 長文優遇
- (d) **同族モデル相関** — Llama judge → Llama 評価で甘く出る

が再現性高く報告. 緩和策は pairwise + position swap, 複数 judge ensemble,
rubric 明示 (G-Eval CoT), 人間 calibration set. FullSense の honest disclosure
([[feedback-benchmark-honest-disclosure]]) と直結する論点.

## Open gap for lleval

1. **on-prem + cloud 統一**: promptfoo/DeepEval は両対応だが, 産業 IoT
   (MQTT/OPC-UA) や local Ollama+llama.cpp と cloud API を **同一 A/B run**
   で扱う設計は不在.
2. **Progressive size curve (xs/s/m/l/xl)**: 既存はどれも固定 prompt 長.
   token×latency×quality の crossover 曲線を一次クラス指標にした framework
   は皆無 (HELM efficiency 軸が最も近いが size sweep ではない).
3. **Honest disclosure**: 異常値 (例: 自社モデルが不自然に速い) の
   **内訳自動診断** (backend attach / chars 正規化 / RTT 除外 / cache warmup)
   は手作業領域, LLMOps tool は cost/latency 分離どまり.
4. **Self-preference bias 自動検出** も空白 (judge ローテーション + swap
   がデファクトにならず).

## Recommended baseline framework to fork or extend

**promptfoo を fork ベース** (YAML + CI + 多 provider + OSS Apache-2.0,
red-team 拡張あり, on-prem provider 実装が薄いので拡張余地大) に,

(a) llmesh provider plugin,
(b) progressive-size matrix runner,
(c) honest-disclosure analyzer,
(d) judge rotation + position swap

を上載せ. 観測層は **Phoenix (OpenInference/OTel)** を採用し trace 互換確保.
RAG 系は **Ragas/TruLens metric を adapter** で吸収, unit-test 思想は
**DeepEval を補助** に.

## 引用

- OpenAI Evals: <https://github.com/openai/evals>
- LMSYS Chatbot Arena: <https://lmsys.org/blog/2023-05-03-arena/>
- HELM: <https://crfm.stanford.edu/helm/>
- promptfoo: <https://github.com/promptfoo/promptfoo>
- DeepEval: <https://github.com/confident-ai/deepeval>
- Phoenix (Arize): <https://github.com/Arize-ai/phoenix>
- Langfuse: <https://github.com/langfuse/langfuse>
- TruLens: <https://github.com/truera/trulens>
- Ragas: <https://github.com/explodinggradients/ragas>
- Self-preference bias (Panickssery+ 2024): <https://arxiv.org/abs/2404.13076>
- G-Eval (Liu+ 2023): <https://arxiv.org/abs/2303.16634>
