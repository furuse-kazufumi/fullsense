---
layout: default
title: "Quiz bench Debug vs Release 比較 — 統計指標付き 10 問テスト"
date: 2026-05-17
tags: [llm, benchmark, debug, release, statistics, mean, stdev, ollama]
id: 87dc2abff45b488f56a4
---

# Quiz bench Debug vs Release 比較 — 統計指標付き 10 問テスト

## TL;DR

- ユーザー指示「DebugMode と Release 版でベンチマークテストして」「クイズ形式 + 平均値・分散値」を反映
- `bench_quiz.py` に **mean / stdev** 統計列を追加し、`llama3.2:3b` × {debug, release} × 10 quiz で計測
- **Debug overhead は wall time に実質影響なし** (mean 22.3s vs 22.8s)
- 正答率の差 (6/10 vs 7/10) は **確率的揺らぎ** の範囲 — 10 問サンプルでは統計的有意な差ではない
- 分散 (stdev) は release の方が大きい (5790ms vs 8356ms) — 出題によって LLM の応答時間が変動

## ベンチ設計

### Quiz set v1

`docs/benchmarks/quizzes/quiz_set_v1.json` — 5 カテゴリ × 2 難易度 = 10 問:

| id | category | difficulty |
|---|---|---|
| arith-01 | arithmetic | easy |
| arith-02 | arithmetic | medium |
| logic-01 | logic | easy |
| logic-02 | logic | medium |
| knowledge-01 | knowledge | easy |
| knowledge-02 | knowledge | medium |
| reason-01 | reasoning | easy |
| reason-02 | reasoning | medium |
| creative-01 | creativity | easy |
| creative-02 | creativity | medium |

採点は **keyword 一致** (`scoring=keyword_match` / `keyword_all` / `keyword_any` / `keyword_*_soft`) で、各問に期待 keyword 集合を持つ。

### 評価対象

- model: `llama3.2:3b` (on-prem Ollama)
- mode: `debug=True` (loop 内部の trace dict を attach) vs `debug=False` (release)
- LLMBackend は llive 内部に attach (fair-benchmark contract、feedback_benchmark_honest_disclosure 準拠)

## 結果

### 個別セル (10 問 × 2 mode = 20 セル)

詳細は `docs/benchmarks/2026-05-17-quiz-{debug,release}/quiz_summary.md`。

### Per-model summary (with statistics)

#### Debug mode

| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |
|---|---|---|---|---|---|---|---|
| `llama3.2` | 10 | 6 | **0.550** | 0.497 | **22 343** | 5 790 | 223.4 |

#### Release mode

| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |
|---|---|---|---|---|---|---|---|
| `llama3.2` | 10 | 7 | **0.650** | 0.474 | **22 750** | 8 356 | 227.5 |

### Debug vs Release の差分

| 指標 | Debug | Release | Δ (Release − Debug) | 解釈 |
|---|---|---|---|---|
| passed | 6 / 10 | 7 / 10 | +1 | 確率変動の範囲 (LLM seed なし) |
| partial mean | 0.550 | 0.650 | +0.100 | 同上 |
| partial stdev | 0.497 | 0.474 | -0.023 | 散らばりは同程度 |
| **ms mean** | **22 343** | **22 750** | **+407 (+1.8 %)** | **Debug overhead は実質ゼロ** |
| ms stdev | 5 790 | 8 356 | +2 566 | release 側で問題による応答時間変動が大きい |
| wall sum | 223.4 s | 227.5 s | +4.1 s | 10 問合計でほぼ同じ |

## 観察と考察

### 1. Debug overhead は wall time にほぼ影響しない (+1.8 %)

llive の `_inner_monologue` は `debug=True` で stages.thought.debug に trace dict を追加するが、これは Python の辞書操作のみ。LLM 推論時間 (10-30 s / brief) に対し誤差。

**結論**: 開発時は debug=True を **常時 ON** にしても性能ペナルティはほぼゼロ。production でも観測ログとして残してよい。

### 2. 正答率の差は **確率的揺らぎ** の範囲

Debug 6/10 vs Release 7/10 = 0.6 vs 0.7。これは 10 サンプルの 1 個分の差で、二項検定では p > 0.5 (有意差なし)。

LLM (llama3.2:3b) の確率的応答により、同じ問題でも debug と release で異なる結果が出る:

| quiz | debug | release |
|---|---|---|
| arith-01 | ❌ pass=False | ✅ pass=True |
| logic-01 | ✅ | ✅ |
| reason-01 | ✅ | ✅ |
| knowledge-01 | ❌ | ❌ |

→ N=10 では足りない。N=30 以上 × 複数 model × seed 固定 が必要。

### 3. ms stdev が release で大きい (5790 vs 8356)

これは LLM 推論時間が問題によって変動するため。debug は per-stage trace を追加するため、毎問似たような overhead が乗って平準化される効果がある (paradoxically)。

## bench_quiz.py の改修内容

`scripts/bench_quiz.py::main()` の per-model summary に以下を追加:

```python
import statistics as _stat

# ok_cells に対する mean / stdev を計算
partials = [c.get("partial_score", 0.0) for c in ok_cells]
mss = [c.get("ms", 0.0) for c in ok_cells]
p_mean = sum(partials) / len(partials) if partials else 0.0
p_std = _stat.stdev(partials) if len(partials) > 1 else 0.0
m_mean = sum(mss) / len(mss) if mss else 0.0
m_std = _stat.stdev(mss) if len(mss) > 1 else 0.0
```

これで `partial mean / partial stdev / ms mean / ms stdev` の 4 列が summary に乗る。

## 次回のための課題

### 1. サンプルサイズの拡大

- **N ≥ 30** で各 model を評価する (現在 N=10)
- **multiple models** (llama3.2:3b / qwen2.5:7b / qwen2.5:14b / mistral 7b / 他) で並列評価
- **seed 固定** で再現可能性を確保 (`OLLAMA_SEED` を追加検討)

### 2. 採点の質向上

- 現在の keyword 一致は答え周辺の自然文を捕まえてしまう → LLM-as-judge での 2 次採点を追加
- partial score を 0/1 でなく fine-grained (e.g. 0.0/0.25/0.5/0.75/1.0) に

### 3. カテゴリ別の難易度バランス

- 現在: arithmetic がカテゴリで最も pass 率低い (debug 0/2, release 1/2) — model size との相関を検証
- 各カテゴリ ≥ 3 問に拡張

### 4. variance を抑える設計

- 同じ問題を **3 回サンプリング** して mean/stdev を per-quiz で取る
- 「同じ問題に対する llama3.2 の応答ばらつき」を可視化

## ソース

- bench runner: `fullsense/scripts/bench_quiz.py` (statistics 列を 2026-05-17 追加)
- quiz set: `fullsense/docs/benchmarks/quizzes/quiz_set_v1.json`
- raw 結果:
  - `fullsense/docs/benchmarks/2026-05-17-quiz-debug/`
  - `fullsense/docs/benchmarks/2026-05-17-quiz-release/`
- 教訓: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

## 同日の他公開資料

- [01 — Brief API + progressive matrix](./01_brief_api_progressive.md)
- [02 — 心理の深層 10 思考因子 × llive](./02_cognitive_factors.md)
- [03 — 数学・単位特化 AI](./03_math_vertical.md)
- [04-06 — 設計予告 3 本](./README.md)
- [07 — fair bench 結果 (honest disclosure 全面改訂版)](./07_bench_results.md)

---

> **fair 比較最優先**。Debug overhead は実質ゼロ、正答率の差は確率変動。次は N≥30 × 複数 model × seed 固定で再走予定。
