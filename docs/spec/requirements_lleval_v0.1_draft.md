---
layout: default
title: "lleval — v0.1 Requirements Draft"
parent: "Spec"
nav_order: 90
---

# lleval — v0.1 Requirements Draft (2026-05-20)

> **採用優先度 HIGH** (from [spinoff_ideas C-2]({{ '/spinoff_ideas_2026_05' | relative_url }})).
> 本草案は **agent 自律ドラフト**. 着手判断は user. ベンチ復旧と並行で
> promptfoo fork PoC を進められる粒度.
>
> SOTA / Gap 分析: [research/lleval_sota]({{ '/research/lleval_sota' | relative_url }})

## 位置づけ (FullSense ファミリー内)

- **vertical 名**: lleval (代案: llbench / llmeter / llmetrics)
- **目的**: on-prem LLM 評価 + cloud LLM 評価 + on-prem 産業 IoT 環境を **同一 A/B run** で扱う統一 eval framework
- **依存方針** ([[feedback-independence-principle]]):
  - llmesh は **optional** (on-prem LLM provider として呼ぶ場合のみ)
  - llive / llove は依存禁止 (independence principle)
  - 単独 PyPI / GitHub 配布. `pip install lleval` で完結
- **PyPI 名**: 未定 (`lleval` / `llmesh-lleval` どちらでも可, brand 揃え目的で
  後者を仮置き)
- **ライセンス**: Apache-2.0 + Commercial dual (FullSense 標準)

## 設計判断

### D-1. promptfoo fork ベース

[研究結果]({{ '/research/lleval_sota' | relative_url }}) より, **promptfoo を fork base** にする.

- promptfoo: Apache-2.0, YAML test + CI 統合 + red-team 拡張あり.
- on-prem provider 実装が薄いので拡張余地大.
- 観測層 (trace) は **Phoenix (Arize, OpenInference/OTel)** を adapter で接続.
- RAG metric は **Ragas / TruLens** を adapter で吸収.
- unit-test 思想は **DeepEval** を補助に.

### D-2. 差別化軸 4 つ (空白埋め)

| # | 差別化 | 既存ギャップ | 実装 hook |
|---|---|---|---|
| 1 | **on-prem + cloud 統一 A/B** | promptfoo/DeepEval は両対応だが産業 IoT (MQTT/OPC-UA) / 局所 llama.cpp と cloud API を同一 run で扱う設計は不在 | `LLMeshProvider` plugin + `OllamaProvider` (server URL 指定可) |
| 2 | **Progressive size curve** | 既存はどれも固定 prompt 長. xs/s/m/l/xl ([[feedback-benchmark-progressive-tokens]]) を一次クラス指標化した framework 不在 | `progressive_matrix` runner: 同 prompt の token を 5 段階 sweep, 結果は token × latency × quality のテーブル |
| 3 | **Honest disclosure** | 異常値の **内訳自動診断** (backend attach / chars 正規化 / RTT 除外 / cache warmup) は手作業 | `HonestDisclosureAnalyzer`: 1 model の latency 異常を 5 因子 (warmup hit / token normalization / network RTT / attach overhead / system load) に分解 |
| 4 | **Self-preference bias 自動検出** | judge ローテーション + position swap がデファクトにならず | `JudgeRotation` evaluator: pairwise + position swap + multi-judge ensemble を default 化 |

## 要件 (LE-FX 系列)

### LE-01. Multi-provider unified run (must)

- 1 つの YAML から **llmesh / Ollama / Anthropic / OpenAI / Gemini** を同一 prompt で A/B run.
- 各 provider の **license tier** ([[research/llcraft_sota]]) を metadata に保持.

### LE-02. Progressive size matrix (must)

- prompt を **xs(50t) / s(200t) / m(800t) / l(3.2kt) / xl(12.8kt)** の 5 段階に
  自動生成 (template + filler).
- 結果は token × latency × quality (judge score) の 3D テーブル.
- crossover point (on-prem vs cloud が逆転する size) を自動抽出.

### LE-03. Honest disclosure analyzer (must)

- 1 model の latency が他より極端に速い場合,
  - cache warmup hit / token-count normalization / network RTT 除外 /
    LLMBackend attach overhead / system load の 5 因子に分解.
- 出力は **diagnosis report** (markdown + JSON), CI でブロック可能.

### LE-04. Judge rotation + position swap (should)

- LM-as-judge では default で **pairwise + position swap + 2-judge minimum**.
- self-preference bias (Panickssery 2024) を **score 差分**で警告.

### LE-05. OpenInference trace 統合 (should)

- Phoenix / Langfuse の OTel collector に span を流す.
- trace ID で個別 prompt run を deep-link.

### LE-06. RAG / agentic metric adapter (could)

- Ragas (faithfulness / context_recall) / TruLens (groundedness) を
  external adapter として吸収. lleval 本体は thin wrapper.

### LE-07. CLI + Python API (must)

- `lleval run config.yaml` の 1 コマンド.
- `from lleval import Bench; Bench(...).run()` の Python API.

### LE-08. GitHub Action / pre-commit hook (could)

- promptfoo の CI 親和性を引き継ぐ. PR の eval diff を bot コメント.

## 非要件 (Out of scope, v0.1)

- 自前 model 学習 (HuggingFace transformers 直結) — promptfoo provider 経由で十分
- UI / dashboard — Phoenix / Langfuse / TruLens の既存 UI を利用
- 多言語 prompt 自動翻訳 — 別 vertical (lltranslate?) の候補

## 着手 trigger (本草案では決定しない)

1. **ベンチ復旧**: Anthropic / Gemini / OpenAI credential / quota 復旧
   ([NEXT_SESSION 🧑 1]({{ '/NEXT_SESSION' | relative_url }})).
2. **promptfoo fork PoC**: provider plugin extension point の動作確認
   (skeleton で 1 日).
3. **lleval リポ作成**: GitHub `furuse-kazufumi/lleval` (Apache-2.0 + Commercial
   dual).
4. **本要件を normative spec に昇格**: 本 draft → `llive/docs/requirements_v0.A_lleval.md`
   相当, バージョン 0.1 → 1.0.

## 関連

- [spinoff_ideas C-2 採用優先度]({{ '/spinoff_ideas_2026_05' | relative_url }})
- [research/lleval_sota]({{ '/research/lleval_sota' | relative_url }})
- [benchmarks/policy]({{ '/benchmarks/policy/' | relative_url }})
- [comparison.md]({{ '/comparison' | relative_url }}) (Honest disclosure 章と同じ哲学)
- maintainer memory: [[feedback-llive-measurement-purity]] [[feedback-benchmark-honest-disclosure]]
  [[feedback-benchmark-progressive-tokens]] [[feedback-competitor-benchmark]]
