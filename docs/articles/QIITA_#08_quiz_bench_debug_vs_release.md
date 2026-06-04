---
layout: default
title: "Quiz bench Debug vs Release 比較 — 統計指標付き 10 問テスト"
date: 2026-05-17
tags: [llm, benchmark, debug, release, statistics, mean, stdev, ollama]
id: 87dc2abff45b488f56a4
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

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

---

# English

# Quiz bench Debug vs Release Comparison — A 10-Question Test with Statistical Metrics

## TL;DR

- Reflects the user's instruction "benchmark DebugMode against the Release build" plus "quiz format + mean and variance"
- Added **mean / stdev** statistics columns to `bench_quiz.py` and measured `llama3.2:3b` × {debug, release} × 10 quizzes
- **Debug overhead has essentially no impact on wall time** (mean 22.3s vs 22.8s)
- The accuracy gap (6/10 vs 7/10) is within the range of **probabilistic noise** — with a 10-question sample it is not a statistically significant difference
- The variance (stdev) is larger for release (5790ms vs 8356ms) — the LLM's response time fluctuates depending on the question

## Benchmark Design

### Quiz set v1

`docs/benchmarks/quizzes/quiz_set_v1.json` — 5 categories × 2 difficulties = 10 questions:

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

Scoring uses **keyword matching** (`scoring=keyword_match` / `keyword_all` / `keyword_any` / `keyword_*_soft`), with each question holding an expected keyword set.

### Evaluation Targets

- model: `llama3.2:3b` (on-prem Ollama)
- mode: `debug=True` (attaches the in-loop trace dict) vs `debug=False` (release)
- The LLMBackend is attached inside llive (fair-benchmark contract, compliant with feedback_benchmark_honest_disclosure)

## Results

### Individual cells (10 questions × 2 modes = 20 cells)

For details, see `docs/benchmarks/2026-05-17-quiz-{debug,release}/quiz_summary.md`.

### Per-model summary (with statistics)

#### Debug mode

| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |
|---|---|---|---|---|---|---|---|
| `llama3.2` | 10 | 6 | **0.550** | 0.497 | **22 343** | 5 790 | 223.4 |

#### Release mode

| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |
|---|---|---|---|---|---|---|---|
| `llama3.2` | 10 | 7 | **0.650** | 0.474 | **22 750** | 8 356 | 227.5 |

### Debug vs Release Differences

| Metric | Debug | Release | Δ (Release − Debug) | Interpretation |
|---|---|---|---|---|
| passed | 6 / 10 | 7 / 10 | +1 | Within probabilistic variation (no LLM seed) |
| partial mean | 0.550 | 0.650 | +0.100 | Same as above |
| partial stdev | 0.497 | 0.474 | -0.023 | Spread is about the same |
| **ms mean** | **22 343** | **22 750** | **+407 (+1.8 %)** | **Debug overhead is effectively zero** |
| ms stdev | 5 790 | 8 356 | +2 566 | The release side shows larger response-time variation across questions |
| wall sum | 223.4 s | 227.5 s | +4.1 s | Essentially the same over all 10 questions |

## Observations and Discussion

### 1. Debug overhead has almost no impact on wall time (+1.8 %)

In llive, `_inner_monologue` adds a trace dict to stages.thought.debug when `debug=True`, but this is only a Python dictionary operation. Against the LLM inference time (10-30 s / brief) it is within the margin of error.

**Conclusion**: During development you can keep debug=True **always ON** with essentially no performance penalty. It can also be left in production as an observability log.

### 2. The accuracy gap is within the range of **probabilistic noise**

Debug 6/10 vs Release 7/10 = 0.6 vs 0.7. This is a difference of a single item out of 10 samples, and a binomial test gives p > 0.5 (no significant difference).

Due to the probabilistic responses of the LLM (llama3.2:3b), the same question can yield different results between debug and release:

| quiz | debug | release |
|---|---|---|
| arith-01 | ❌ pass=False | ✅ pass=True |
| logic-01 | ✅ | ✅ |
| reason-01 | ✅ | ✅ |
| knowledge-01 | ❌ | ❌ |

→ N=10 is not enough. We need N ≥ 30 × multiple models × fixed seed.

### 3. ms stdev is larger for release (5790 vs 8356)

This is because LLM inference time varies by question. Since debug adds per-stage traces, a similar overhead is layered onto every question, which (paradoxically) has a leveling effect.

## What Was Changed in bench_quiz.py

The following was added to the per-model summary in `scripts/bench_quiz.py::main()`:

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

This puts the 4 columns `partial mean / partial stdev / ms mean / ms stdev` into the summary.

## Tasks for Next Time

### 1. Increase the sample size

- Evaluate each model with **N ≥ 30** (currently N=10)
- Evaluate in parallel across **multiple models** (llama3.2:3b / qwen2.5:7b / qwen2.5:14b / mistral 7b / others)
- Ensure reproducibility with a **fixed seed** (consider adding `OLLAMA_SEED`)

### 2. Improve scoring quality

- The current keyword matching catches natural-language text around the answer → add a second-pass scoring step with LLM-as-judge
- Make the partial score fine-grained rather than 0/1 (e.g. 0.0/0.25/0.5/0.75/1.0)

### 3. Difficulty balance per category

- Currently: arithmetic has the lowest pass rate among categories (debug 0/2, release 1/2) — verify the correlation with model size
- Expand each category to ≥ 3 questions

### 4. Design to suppress variance

- Sample the same question **3 times** and take mean/stdev per-quiz
- Visualize "the response variability of llama3.2 to the same question"

## Sources

- bench runner: `fullsense/scripts/bench_quiz.py` (statistics columns added 2026-05-17)
- quiz set: `fullsense/docs/benchmarks/quizzes/quiz_set_v1.json`
- raw results:
  - `fullsense/docs/benchmarks/2026-05-17-quiz-debug/`
  - `fullsense/docs/benchmarks/2026-05-17-quiz-release/`
- Lesson: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

## Other Materials Published the Same Day

- [01 — Brief API + progressive matrix](./01_brief_api_progressive.md)
- [02 — The Depths of Psychology: 10 Cognitive Factors × llive](./02_cognitive_factors.md)
- [03 — Math/Unit-Specialized AI](./03_math_vertical.md)
- [04-06 — 3 design previews](./README.md)
- [07 — fair bench results (fully revised honest-disclosure edition)](./07_bench_results.md)

---

> **Fair comparison first.** Debug overhead is effectively zero, and the accuracy gap is probabilistic variation. Next we plan a re-run with N≥30 × multiple models × fixed seed.

---

# 中文

# Quiz bench Debug 与 Release 对比 — 带统计指标的 10 题测试

## TL;DR

- 反映用户指示"对 DebugMode 和 Release 版进行基准测试""测验形式 + 平均值与方差"
- 在 `bench_quiz.py` 中新增 **mean / stdev** 统计列，对 `llama3.2:3b` × {debug, release} × 10 道测验进行计测
- **Debug overhead 对 wall time 实质上没有影响**（mean 22.3s vs 22.8s）
- 正确率的差异（6/10 vs 7/10）在 **概率性波动** 的范围内 —— 在 10 题样本下不是统计上显著的差异
- 方差（stdev）在 release 一侧更大（5790ms vs 8356ms）—— LLM 的响应时间会因题目而变动

## 基准设计

### Quiz set v1

`docs/benchmarks/quizzes/quiz_set_v1.json` —— 5 个类别 × 2 个难度 = 10 道题：

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

评分采用 **关键词匹配**（`scoring=keyword_match` / `keyword_all` / `keyword_any` / `keyword_*_soft`），每道题持有一个期望关键词集合。

### 评估对象

- model：`llama3.2:3b`（on-prem Ollama）
- mode：`debug=True`（附加 loop 内部的 trace dict）vs `debug=False`（release）
- LLMBackend 附加在 llive 内部（fair-benchmark contract，遵循 feedback_benchmark_honest_disclosure）

## 结果

### 各单元格（10 题 × 2 mode = 20 个单元格）

详情见 `docs/benchmarks/2026-05-17-quiz-{debug,release}/quiz_summary.md`。

### Per-model summary（带统计）

#### Debug mode

| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |
|---|---|---|---|---|---|---|---|
| `llama3.2` | 10 | 6 | **0.550** | 0.497 | **22 343** | 5 790 | 223.4 |

#### Release mode

| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |
|---|---|---|---|---|---|---|---|
| `llama3.2` | 10 | 7 | **0.650** | 0.474 | **22 750** | 8 356 | 227.5 |

### Debug 与 Release 的差异

| 指标 | Debug | Release | Δ (Release − Debug) | 解读 |
|---|---|---|---|---|
| passed | 6 / 10 | 7 / 10 | +1 | 概率波动的范围（无 LLM seed） |
| partial mean | 0.550 | 0.650 | +0.100 | 同上 |
| partial stdev | 0.497 | 0.474 | -0.023 | 离散程度相当 |
| **ms mean** | **22 343** | **22 750** | **+407 (+1.8 %)** | **Debug overhead 实质为零** |
| ms stdev | 5 790 | 8 356 | +2 566 | release 一侧因题目导致的响应时间变动更大 |
| wall sum | 223.4 s | 227.5 s | +4.1 s | 10 题合计几乎相同 |

## 观察与思考

### 1. Debug overhead 对 wall time 几乎没有影响（+1.8 %）

llive 的 `_inner_monologue` 在 `debug=True` 时会向 stages.thought.debug 添加 trace dict，但这只是 Python 的字典操作。相对于 LLM 推理时间（10-30 s / brief）而言属于误差范围。

**结论**：开发时即使把 debug=True **常时 ON** 也几乎没有性能损失。在 production 中也可以作为观测日志保留。

### 2. 正确率的差异在 **概率性波动** 的范围内

Debug 6/10 vs Release 7/10 = 0.6 vs 0.7。这是 10 个样本中 1 个的差异，二项检验给出 p > 0.5（无显著差异）。

由于 LLM（llama3.2:3b）的概率性响应，即便是同一道题，debug 和 release 也会得到不同结果：

| quiz | debug | release |
|---|---|---|
| arith-01 | ❌ pass=False | ✅ pass=True |
| logic-01 | ✅ | ✅ |
| reason-01 | ✅ | ✅ |
| knowledge-01 | ❌ | ❌ |

→ N=10 不够。需要 N=30 以上 × 多个 model × 固定 seed。

### 3. ms stdev 在 release 更大（5790 vs 8356）

这是因为 LLM 推理时间会因题目而变动。由于 debug 会添加 per-stage trace，每道题都叠加了类似的 overhead，从而（吊诡地）产生了平准化效果。

## bench_quiz.py 的改动内容

在 `scripts/bench_quiz.py::main()` 的 per-model summary 中新增了以下内容：

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

这样就把 `partial mean / partial stdev / ms mean / ms stdev` 这 4 列加入了 summary。

## 下次的课题

### 1. 扩大样本量

- 用 **N ≥ 30** 评估各个 model（当前 N=10）
- 用 **multiple models**（llama3.2:3b / qwen2.5:7b / qwen2.5:14b / mistral 7b / 其他）并行评估
- 用 **固定 seed** 确保可复现性（考虑追加 `OLLAMA_SEED`）

### 2. 提升评分质量

- 当前的关键词匹配会捕捉到答案周边的自然语句 → 追加 LLM-as-judge 的二次评分
- 把 partial score 从 0/1 改为细粒度（例如 0.0/0.25/0.5/0.75/1.0）

### 3. 各类别的难度平衡

- 当前：arithmetic 是各类别中 pass 率最低的（debug 0/2, release 1/2）—— 验证其与 model size 的相关性
- 把各类别扩展到 ≥ 3 题

### 4. 抑制 variance 的设计

- 对同一道题 **采样 3 次**，按 per-quiz 取 mean/stdev
- 可视化"同一道题下 llama3.2 的响应离散程度"

## 来源

- bench runner：`fullsense/scripts/bench_quiz.py`（statistics 列于 2026-05-17 追加）
- quiz set：`fullsense/docs/benchmarks/quizzes/quiz_set_v1.json`
- raw 结果：
  - `fullsense/docs/benchmarks/2026-05-17-quiz-debug/`
  - `fullsense/docs/benchmarks/2026-05-17-quiz-release/`
- 教训：[`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

## 同日的其他公开资料

- [01 — Brief API + progressive matrix](./01_brief_api_progressive.md)
- [02 — 心理的深层 10 思考因子 × llive](./02_cognitive_factors.md)
- [03 — 数学・单位特化 AI](./03_math_vertical.md)
- [04-06 — 设计预告 3 篇](./README.md)
- [07 — fair bench 结果（honest disclosure 全面改订版）](./07_bench_results.md)

---

> **fair 对比最优先**。Debug overhead 实质为零，正确率的差异是概率波动。下次计划以 N≥30 × 多个 model × 固定 seed 重跑。

---

# 한국어

# Quiz bench Debug vs Release 비교 — 통계 지표가 포함된 10문항 테스트

## TL;DR

- 사용자 지시 "DebugMode 와 Release 버전으로 벤치마크 테스트해줘" "퀴즈 형식 + 평균값·분산값"을 반영
- `bench_quiz.py` 에 **mean / stdev** 통계 열을 추가하고, `llama3.2:3b` × {debug, release} × 10 quiz 로 계측
- **Debug overhead 는 wall time 에 사실상 영향이 없음** (mean 22.3s vs 22.8s)
- 정답률의 차이 (6/10 vs 7/10) 는 **확률적 흔들림** 의 범위 — 10문항 샘플에서는 통계적으로 유의한 차이가 아님
- 분산 (stdev) 은 release 쪽이 더 큼 (5790ms vs 8356ms) — 출제에 따라 LLM 의 응답 시간이 변동

## 벤치 설계

### Quiz set v1

`docs/benchmarks/quizzes/quiz_set_v1.json` — 5 카테고리 × 2 난이도 = 10문항:

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

채점은 **keyword 일치** (`scoring=keyword_match` / `keyword_all` / `keyword_any` / `keyword_*_soft`) 로, 각 문항에 기대 keyword 집합을 가진다.

### 평가 대상

- model: `llama3.2:3b` (on-prem Ollama)
- mode: `debug=True` (loop 내부의 trace dict 를 attach) vs `debug=False` (release)
- LLMBackend 는 llive 내부에 attach (fair-benchmark contract, feedback_benchmark_honest_disclosure 준수)

## 결과

### 개별 셀 (10문항 × 2 mode = 20 셀)

상세는 `docs/benchmarks/2026-05-17-quiz-{debug,release}/quiz_summary.md`.

### Per-model summary (with statistics)

#### Debug mode

| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |
|---|---|---|---|---|---|---|---|
| `llama3.2` | 10 | 6 | **0.550** | 0.497 | **22 343** | 5 790 | 223.4 |

#### Release mode

| model | total | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum (s) |
|---|---|---|---|---|---|---|---|
| `llama3.2` | 10 | 7 | **0.650** | 0.474 | **22 750** | 8 356 | 227.5 |

### Debug vs Release 의 차분

| 지표 | Debug | Release | Δ (Release − Debug) | 해석 |
|---|---|---|---|---|
| passed | 6 / 10 | 7 / 10 | +1 | 확률 변동의 범위 (LLM seed 없음) |
| partial mean | 0.550 | 0.650 | +0.100 | 상동 |
| partial stdev | 0.497 | 0.474 | -0.023 | 흩어짐은 비슷한 정도 |
| **ms mean** | **22 343** | **22 750** | **+407 (+1.8 %)** | **Debug overhead 는 실질 제로** |
| ms stdev | 5 790 | 8 356 | +2 566 | release 쪽에서 문항에 따른 응답 시간 변동이 큼 |
| wall sum | 223.4 s | 227.5 s | +4.1 s | 10문항 합계로 거의 동일 |

## 관찰과 고찰

### 1. Debug overhead 는 wall time 에 거의 영향을 주지 않음 (+1.8 %)

llive 의 `_inner_monologue` 는 `debug=True` 에서 stages.thought.debug 에 trace dict 를 추가하지만, 이는 Python 의 사전 조작에 불과하다. LLM 추론 시간 (10-30 s / brief) 에 대해서는 오차 수준이다.

**결론**: 개발 시에는 debug=True 를 **상시 ON** 으로 해도 성능 페널티가 거의 제로다. production 에서도 관측 로그로 남겨 두어도 된다.

### 2. 정답률의 차이는 **확률적 흔들림** 의 범위

Debug 6/10 vs Release 7/10 = 0.6 vs 0.7. 이것은 10 샘플 중 1개분의 차이로, 이항 검정에서는 p > 0.5 (유의차 없음) 이다.

LLM (llama3.2:3b) 의 확률적 응답으로 인해, 같은 문항이라도 debug 와 release 에서 다른 결과가 나온다:

| quiz | debug | release |
|---|---|---|
| arith-01 | ❌ pass=False | ✅ pass=True |
| logic-01 | ✅ | ✅ |
| reason-01 | ✅ | ✅ |
| knowledge-01 | ❌ | ❌ |

→ N=10 으로는 부족하다. N=30 이상 × 복수 model × seed 고정 이 필요하다.

### 3. ms stdev 가 release 에서 큼 (5790 vs 8356)

이것은 LLM 추론 시간이 문항에 따라 변동하기 때문이다. debug 는 per-stage trace 를 추가하기 때문에, 매 문항 비슷한 overhead 가 얹혀 평준화되는 효과가 있다 (paradoxically).

## bench_quiz.py 의 개수 내용

`scripts/bench_quiz.py::main()` 의 per-model summary 에 다음을 추가:

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

이로써 `partial mean / partial stdev / ms mean / ms stdev` 의 4개 열이 summary 에 실린다.

## 다음을 위한 과제

### 1. 샘플 크기의 확대

- **N ≥ 30** 으로 각 model 을 평가한다 (현재 N=10)
- **multiple models** (llama3.2:3b / qwen2.5:7b / qwen2.5:14b / mistral 7b / 기타) 으로 병렬 평가
- **seed 고정** 으로 재현 가능성을 확보 (`OLLAMA_SEED` 추가 검토)

### 2. 채점의 질 향상

- 현재의 keyword 일치는 답 주변의 자연문을 잡아 버린다 → LLM-as-judge 에 의한 2차 채점을 추가
- partial score 를 0/1 이 아니라 fine-grained (예: 0.0/0.25/0.5/0.75/1.0) 로

### 3. 카테고리별 난이도 밸런스

- 현재: arithmetic 이 카테고리 중 가장 pass 율이 낮음 (debug 0/2, release 1/2) — model size 와의 상관을 검증
- 각 카테고리 ≥ 3 문항으로 확장

### 4. variance 를 억제하는 설계

- 같은 문항을 **3회 샘플링** 하여 per-quiz 로 mean/stdev 를 취한다
- "같은 문항에 대한 llama3.2 의 응답 편차" 를 가시화

## 소스

- bench runner: `fullsense/scripts/bench_quiz.py` (statistics 열을 2026-05-17 추가)
- quiz set: `fullsense/docs/benchmarks/quizzes/quiz_set_v1.json`
- raw 결과:
  - `fullsense/docs/benchmarks/2026-05-17-quiz-debug/`
  - `fullsense/docs/benchmarks/2026-05-17-quiz-release/`
- 교훈: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

## 같은 날의 다른 공개 자료

- [01 — Brief API + progressive matrix](./01_brief_api_progressive.md)
- [02 — 심리의 심층 10 사고 인자 × llive](./02_cognitive_factors.md)
- [03 — 수학·단위 특화 AI](./03_math_vertical.md)
- [04-06 — 설계 예고 3편](./README.md)
- [07 — fair bench 결과 (honest disclosure 전면 개정판)](./07_bench_results.md)

---

> **fair 비교 최우선**. Debug overhead 는 실질 제로, 정답률의 차이는 확률 변동. 다음은 N≥30 × 복수 model × seed 고정으로 재실행 예정.
