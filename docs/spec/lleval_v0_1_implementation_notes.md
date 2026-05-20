---
layout: default
title: "lleval — v0.1 Implementation Notes (PoC scope)"
parent: "Spec"
nav_order: 91
---

# lleval — v0.1 Implementation Notes (2026-05-20 夜)

> [Spec 草案]({{ '/spec/requirements_lleval_v0.1_draft' | relative_url }}) に対する
> **実装スコープ確定メモ**. PoC 着手判断のための具体化レイヤー.
> agent 自律ドラフト, 最終判断は user.

## 0. 結論先出し

| 質問 | 結論 | 理由 |
|---|---|---|
| promptfoo を fork するか? | **No — wrap する** | promptfoo は TypeScript/Node.js. FullSense は Python 主軸. fork は維持コスト 2 倍. wrap なら upstream 追従が自動. |
| 別 PyPI として配るか? | **Yes (v0.1 から)** | independence principle. `pip install lleval`. |
| 別 GitHub repo にするか? | **Yes (`furuse-kazufumi/lleval`)** | FullSense umbrella の 4 つ目の子. portal に link only. |
| v0.1 で実装する LE-FX | LE-01 / 02 / 03 / 07 | LE-04/05/06/08 は v0.2 以降. honest-disclosure を最優先. |
| 実コード起点 | **本 portal 内に置かない** | portal は docs hub. 着手判断が出たら別 repo init. |

## 1. wrap 設計 (promptfoo subprocess)

```text
┌─────────────────────────────────────┐
│ lleval (Python)                     │
│                                     │
│  ┌──────────────────────────────┐   │
│  │ config (YAML / Python API)   │   │
│  └─────────────┬────────────────┘   │
│                ↓                    │
│  ┌──────────────────────────────┐   │
│  │ ProgressiveMatrixRunner      │   │
│  │  - prompt × 5 sizes 展開      │   │
│  │  - provider 行列              │   │
│  └─────────────┬────────────────┘   │
│                ↓                    │
│  ┌──────────────────────────────┐   │
│  │ promptfoo subprocess wrapper │   │
│  │  - npx promptfoo eval        │   │
│  │  - 結果 JSON parse           │   │
│  └─────────────┬────────────────┘   │
│                ↓                    │
│  ┌──────────────────────────────┐   │
│  │ HonestDisclosureAnalyzer     │   │
│  │  - 5 因子分解                  │   │
│  │  - 異常値 diagnosis           │   │
│  └─────────────┬────────────────┘   │
│                ↓                    │
│  ┌──────────────────────────────┐   │
│  │ Report (markdown + JSON)     │   │
│  └──────────────────────────────┘   │
│                                     │
└─────────────────────────────────────┘
```

依存:

- `promptfoo` (npm) — runtime (operator が `npm i -g promptfoo` 想定)
- Python 3.11+
- `pydantic` (YAML validation), `httpx` (Phoenix push), `numpy` (latency stats)

## 2. リポジトリ構成 (skeleton)

```text
lleval/                            # 別 GitHub repo
├── pyproject.toml                 # >=3.11,<3.12  (project_python_311_unification)
├── README.md                      # ja/en 並走, 後で zh/ko 追加
├── LICENSE                        # Apache-2.0
├── LICENSE-COMMERCIAL              # dual-license stub
├── NOTICE
├── CONTRIBUTING.md                # DCO
├── SECURITY.md
├── docs/
│   ├── requirements_v0.1.md        # portal draft を昇格
│   ├── design_decisions.md
│   ├── progressive_matrix.md
│   ├── honest_disclosure.md
│   └── examples/
│       ├── basic.yaml
│       ├── progressive.yaml
│       └── multi_provider.yaml
├── src/lleval/
│   ├── __init__.py
│   ├── config.py                   # pydantic model
│   ├── progressive.py              # xs/s/m/l/xl 展開
│   ├── runner.py                   # promptfoo subprocess
│   ├── analyzer/
│   │   ├── __init__.py
│   │   └── honest_disclosure.py    # 5 因子分解
│   ├── providers/
│   │   ├── __init__.py
│   │   ├── llmesh.py               # llmesh HTTP → promptfoo custom provider gen
│   │   └── ollama.py
│   ├── report/
│   │   ├── __init__.py
│   │   ├── markdown.py
│   │   └── json.py
│   └── cli.py                      # `lleval run config.yaml`
└── tests/
    ├── unit/
    │   ├── test_progressive.py
    │   ├── test_honest_disclosure.py
    │   └── test_config.py
    └── integration/
        └── test_runner_with_fake_promptfoo.py
```

## 3. 最小実装スコープ (LE-01/02/03/07 = MVP)

### LE-01 — Multi-provider unified run

- promptfoo の `providers:` を **template** で生成. llmesh は HTTP API
  endpoint を `custom-provider` 形式で渡す Python helper.
- v0.1 は **llmesh + Ollama + Anthropic + OpenAI** の 4 つ.
  Gemini / Vertex は v0.2 (credential 復旧後).

### LE-02 — Progressive size matrix

- xs(50t) / s(200t) / m(800t) / l(3.2kt) / xl(12.8kt) の filler:
  - 自然な文章 (lorem ipsum 禁止) — `docs/research/` を sample corpus に流用
  - token count は `tiktoken` (cl100k_base) で正確化, fallback は単純 `len(text) // 4`
- 出力テーブル: rows = providers, cols = sizes, cells = `{latency_p50, latency_p99, quality_score, token_in, token_out}`
- **crossover detection**: on-prem vs cloud で latency / quality が反転する size を pandas で計算

### LE-03 — Honest disclosure analyzer

- 異常検知 trigger: 同 size で latency 比が **2x 超過**
- 5 因子分解:
  1. **warmup hit**: 1st call と 2nd call の latency 比 (1.5x 超で warmup 計上)
  2. **token-count normalization**: chars / tokens 比が他 model と乖離 (>30%) で警告
  3. **network RTT 除外**: `time.monotonic()` の prompt 送信前後で実 RTT を分離記録
  4. **backend attach overhead**: subprocess RTT (npx promptfoo の起動時間) を baseline 引き算
  5. **system load**: psutil.cpu_percent() の 1 秒 sample
- **+ Runtime metadata (6 因子目, llive v0.A 連携)** — `tests/contract/test_llamacpp_smoke.py` で
  検証された **on-prem runtime の SHA / version 情報** を span metadata として
  必ず保持. これが無い実行は **lleval CI で BLOCK** とする:
  - `llama_cpp_sha` (例 `abc1234`)
  - `llama_cpp_release_tag` (例 `b4501`)
  - `gguf_spec_version` (例 `3`)
  - `sampler_chain_spec` (例 `top_k=40 top_p=0.95 min_p=0.05 temp=0.7`)
  - `kv_cache_quantization` (例 `q8_0`)
  - `model_quant` (例 `q4_k_m`)
- 出力: `out/lleval-<timestamp>/diagnosis.md` + `diagnosis.json`

### LE-07 — CLI + Python API

```bash
lleval run config.yaml
lleval run config.yaml --out reports/
lleval run config.yaml --progressive  # LE-02 を強制有効
lleval run config.yaml --analyze      # LE-03 強制有効
```

```python
from lleval import Bench, Config
cfg = Config.from_yaml("config.yaml")
result = Bench(cfg).run(progressive=True, analyze=True)
result.to_markdown("report.md")
```

## 4. 着手判断のために残る課題

| # | 課題 | 検証方法 | 所要 |
|---|---|---|---|
| C-1 | promptfoo の custom provider API が外部 binary 経由でも安定動作するか | `npx promptfoo eval --providers='exec:bash -c "..."'` で hello world | 30 min |
| C-2 | tiktoken で各 model の token を **正確に** 数えられるか (特に on-prem) | `tiktoken.encoding_for_model("gpt-4o")` と llama.cpp の eval_count 比較 | 1h |
| C-3 | Phoenix の OpenInference span を CLI から push する最小手順 | `arize-phoenix-otel` の subprocess 経由連携 | 1h (LE-05 で必要, v0.1 では skip) |
| C-4 | judge rotation で 2 judge 最小 + position swap の sample size | 既存 OpenAI Evals の `model_graded` ベンチを small dataset で再現 | 1d (LE-04 v0.2) |

## 5. ベンチ復旧との依存

- v0.1 PoC は **mock provider** で先行可能 (Anthropic/Gemini/OpenAI 不要).
- 実 quality 評価のみ credential 必要. PoC スケルトン → unit test green
  まで先に進めて, credential 復旧後に E2E run.

## 6. 作業順 (本 portal 内では着手しない)

1. user に「lleval リポ作る ?」確認 (本 PoC ノートを提示)
2. 承認後: GitHub repo init + Apache-2.0 / Commercial dual license + pyproject
3. LE-02 / LE-03 を unit test first (mock provider)
4. LE-01 を mock + 1 実 provider (Ollama local)
5. LE-07 CLI で `lleval run examples/basic.yaml` が通る最小スケルトン
6. README + 1 sample report
7. PyPI 0.1.0a0 alpha 公開 (lleval / llmesh-lleval どちらも reserve)

## 7. 外部ランタイム追従との接続 (llive v0.A)

llive 側の `docs/requirements_v0.A_external_runtime_tracking.md` で llama.cpp /
GGUF / sampler chain の **月次追従ルール** が定義されている. lleval は本仕様の
**Runtime metadata 6 因子目** で連動する:

- llive 側 `tests/contract/test_llamacpp_smoke.py` で smoke 通過した SHA 情報を
  bench 出力 JSON に注入する.
- lleval は span metadata に同 SHA を持ち, `diagnosis.json` の `runtime_pin`
  フィールドで報告.
- **stable / rolling / edge** の 3 段階 pin ([[feedback-llamacpp-tracking]]) に
  従い, **公開ベンチでは stable SHA 必須**.

これにより「llama.cpp 月次更新で variation が出た」が **CI ブロック + 自動
diagnosis** に縮退する.

## 関連

- [Spec 草案]({{ '/spec/requirements_lleval_v0.1_draft' | relative_url }})
- [SOTA Survey]({{ '/research/lleval_sota' | relative_url }})
- [spinoff_ideas C-2]({{ '/spinoff_ideas_2026_05' | relative_url }})
- llive `docs/requirements_v0.A_external_runtime_tracking.md` (外部 LLM ランタイム追従)
- llive `docs/spec/llamacpp_compat_matrix.md` (互換性 matrix SSoT)
- maintainer memory: [[feedback-benchmark-progressive-tokens]]
  [[feedback-benchmark-honest-disclosure]] [[feedback-independence-principle]]
  [[feedback-competitor-benchmark]] [[feedback-llamacpp-tracking]]
