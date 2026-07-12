---
layout: default
title: "llive vs 他 LLM ベンチマーク 2026-05-17 — 動作確認の罠と honest disclosure"
date: 2026-05-17
tags: [llm, benchmark, on-prem, ollama, perplexity, llive, methodology]
project_group: llive
id: f2ebf45621d8f85399c9
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# llive vs 他 LLM ベンチマーク 2026-05-17 — 動作確認の罠と honest disclosure

## TL;DR (改訂 — 当初版に異常があったため全面書き換え)

- 同日実装した Brief API end-to-end の動作確認を兼ね 4 brief × 6 model でベンチ走行
- **llive 4/4 OK 134-184ms** という数値は出たが、これは **「LLM 推論をしていない」結果**であり fair 比較ではない
- 動作確認としては成功 (Brief data flow / ledger / decision が安定再現)
- **fair な品質・速度比較は次回 (CABT-01 prototype 後 + LLMBackend attach 後)** に再走
- raw データと注意点を保存し、誤解を招く前に異常 3 件を明示開示

## 確認された異常 (3 件)

ユーザーから「変に高速ですね、何か応答におかしな部分はないですか？」と指摘を受け、raw 出力を再検査。以下 3 つの異常 (= ベンチ設計の落とし穴) が見つかった。

### 異常 1: llive 側が LLMBackend を attach していない

llive の bench runner (`fullsense/scripts/bench_run.py::run_llive`) は `llive/scripts/run_brief.py --json <brief>` を subprocess 呼出。この `run_brief.py` は `FullSenseLoop(sandbox=True, debug=args.debug)` を **LLM backend なし** で構築する。

結果、loop の `_inner_monologue` stage は **template 経路** (rule-based) に落ち、出力は:

```
Observation about 'manual': <brief content[:120]> — novel territory, worth exploring.
```

全 brief で同じテンプレート構造。brief の **先頭 120 文字** だけ thought.text に挿入されるため、b1〜b4 の "意味的内容" は loop に届いていない。

### 異常 2: `chars` メトリクスは JSON 全長を測っている

`bench_run.py` の `chars` 列は `len(p.stdout)` = subprocess 標準出力 (JSON 形式) の文字数。

- llive: JSON 構造 (stim metadata + stages + plan + raw) が dominant → 884 chars
- ollama / perplexity: LLM 応答テキストそのもの → 148〜1733 chars と brief 依存

つまり llive 4/4 で `884 chars` 同一なのは **「同じ JSON 構造を吐いたから」**であり、応答内容として fair な比較指標にはなっていない。

### 異常 3: 134-184ms は subprocess RTT + JSON serialize 時間

llive 経路に LLM 推論がないため、計測時間は:

- py launcher 起動 + Python interpreter import (~80-120ms on Windows)
- `FullSenseLoop.process()` の 6 stage を template 経路で抜ける (~10-30ms)
- JSON 出力 (~1ms)
- subprocess wait + stdout 読込 (~10-30ms)

= 134-184ms。LLM 推論レイテンシではない。「llive を内蔵」と「llive を template fallback で素通り」が同じ wall time を出す結果になっている。

参考: 同じ `FullSenseLoop` に Ollama (llama3.2:3b) backend を attach した progressive matrix では xs (cold) で 8.9 秒、warm で 1〜2 秒程度かかる ([記事 01](./QIITA_%2301_brief_api_progressive.md) 参照)。

## それでも価値ある観察

honest disclosure を踏まえても、このベンチで確認できたことは存在する:

### ✅ Brief API end-to-end の data flow が brief 4 種で安定動作

llive の Brief data flow:

1. brief テキスト → `Stimulus` 変換
2. 6 stage loop (salience → curiosity → thought → ego/altruism → plan → output)
3. 各 stage で ledger append
4. final decision (`note`) を返却
5. JSON serialization と stdout 出力

を **4 brief すべてで再現** (subprocess return code 0、JSON parse 成功)。これは Brief API 実装の **動作確認** としては有効。

### ✅ rule-based loop の安定性

LLMBackend が無くても loop が deterministic に走り、`decision=note` を返す → template fallback の堅牢性確認。

### ✅ cloud / on-prem の credential 状態の把握

| service | 動作 | 状態 |
|---|---|---|
| ollama llama3.2:3b (on-prem) | ✅ 4/4 OK | 12〜20s/brief、実 LLM 推論動作中 |
| perplexity (cloud Sonar) | ✅ 4/4 OK | 2.5〜6s/brief、citation 付き |
| anthropic | ❌ ERR | `401 invalid_x-api-key` rotate 待ち |
| gemini | ❌ ERR | `429 quota exceeded` |
| openai codex | ❌ ERR | `429 insufficient_quota` |

復旧手順は `fullsense/docs/NEXT_SESSION.md` の Operator action 2 に記載済。

## 当初発表していた表 (取り消し / 注記付き再掲)

下表の **llive 行は LLM 推論を経由していない動作確認データ** として読むこと。応答品質や応答速度比較として参照しない:

| brief | model | status | wall (ms) | chars | 注記 |
|---|---|---|---|---|---|
| b1 | llive | OK | 152 | 884 | ⚠️ template fallback (LLM 推論なし) |
| b1 | ollama | OK | 18 812 | 148 | 実 LLM 推論 |
| b1 | perplexity | OK | 4 555 | 192 | cloud LLM |
| b2 | llive | OK | 134 | 884 | ⚠️ template fallback |
| b2 | ollama | OK | 12 220 | 376 | 実 LLM 推論 |
| b2 | perplexity | OK | 4 011 | 251 | cloud LLM |
| b3 | llive | OK | 184 | 884 | ⚠️ template fallback |
| b3 | ollama | OK | 20 127 | 616 | 実 LLM 推論 |
| b3 | perplexity | OK | 2 547 | 365 | cloud LLM |
| b4 | llive | OK | 173 | 884 | ⚠️ template fallback |
| b4 | ollama | OK | 18 991 | 357 | 実 LLM 推論 |
| b4 | perplexity | OK | 6 019 | 1733 | cloud LLM |

## Fair 再走結果 (2026-05-17 修正後 — 同日同セッション内)

`bench_run.py::run_llive` を **LLMBackend (ollama:llama3.2) attach 版**に修正し、
chars メトリクスを `stages.thought.text` (LLM 実出力) から取るよう変更して再走:

| brief | model | status | wall (ms) | chars (LLM 実出力) | 注記 |
|---|---|---|---|---|---|
| b1 | llive (+llama3.2:3b) | OK | **32 750** | 377 | loop 経路で実 LLM 推論 |
| b1 | ollama 直叩き (llama3.2:3b) | OK | 12 423 | 148 | 比較 baseline |
| b1 | perplexity | OK | 2 411 | 297 | cloud (Sonar) |
| b2 | llive (+llama3.2:3b) | OK | **50 936** | 1 255 | |
| b2 | ollama | OK | 13 024 | 276 | |
| b2 | perplexity | OK | 3 591 | 225 | |
| b3 | llive (+llama3.2:3b) | OK | **43 787** | 531 | |
| b3 | ollama | OK | 19 610 | 469 | |
| b3 | perplexity | OK | 2 104 | 352 | |
| b4 | llive (+llama3.2:3b) | OK | **43 163** | 342 | |
| b4 | ollama | OK | 21 936 | 417 | |
| b4 | perplexity | OK | 6 162 | 855 | |

### Fair 比較の観察

- **llive (LLM attached) は ollama 直叩きの 2-4 倍遅い** (32-51s vs 12-22s)
- LLM call が 1 回入る点は両者同じ。**差分は llive の build_llm_prompt が brief を `_inner_monologue` 用にラップして長文化させていること** = LLM 推論時間自体が長くなる
- progressive matrix (overhead < 1%) は同じバックエンドで loop 内 vs 直叩きを比較していなかったため、その「overhead」とは別物
- llive の **付加価値** は時間ではなく構造 (ledger / approval / governance / grounding / 6 stage trace) にある — 速度だけで判断するなら ollama 直叩きの方が良い

### fair 再走の生データ

`fullsense/docs/benchmarks/2026-05-17-fair/` に保存:

```
2026-05-17-fair/
  b1/ {llive,ollama,perplexity,anthropic,gemini,codex}.txt
  b2/ ...
  b3/ ...
  b4/ ...
```

## 次回 fair 比較のための修正項目

### 1. bench_run.py の run_llive を更新

`run_brief.py` を LLMBackend attach 版に切替、もしくは新 Brief API CLI (`llive brief submit --backend ollama:qwen2.5:14b ...`) を呼ぶ。

### 2. chars メトリクスの公平化

- llive: `result.stages.thought.text` の長さ (応答テキストのみ)
- 他: 既存通り response text
- JSON 構造分は別カラムで分離

### 3. 比較対象の追加

LLM 推論レイヤーの比較として:
- llive (ollama:qwen2.5:14b attached, Brief Grounder + SafeCalculator あり)
- llive (ollama:qwen2.5:14b attached, plain)
- ollama qwen2.5:14b 直叩き

の 3 系統で品質・速度・citation 精度を比較するのが fair。

### 4. 品質メトリクスの導入

speed と chars に加えて:
- spec compliance (success_criteria に対する合格率)
- citation 精度 (provenance chain の検証可能性)
- safety (dangerous_token 検出 vs 出力)

## 教訓 (TRIZ 矛盾としての記録)

> 「ベンチを取った瞬間に勝った気になる」 vs 「ベンチの設計欠陥を疑う」

これは典型的な研究開発の罠で、ユーザーの指摘 (「変に高速ですね」) が無ければ気付かなかった可能性が高い。

教訓を `feedback_benchmark_honest_disclosure.md` として maintainer memory に保存予定。

## ソース

- raw data: `fullsense/docs/benchmarks/2026-05-17/b{1,2,3,4}/{model}.txt`
- bench runner: `fullsense/scripts/bench_run.py`
- 当初版 (異常を含む) は git 履歴で参照可: `git log -- docs/articles/2026-05-17/07_bench_results.md`

## 同日の他公開資料

- [01 — Brief API + progressive matrix (overhead < 1 %)](./01_brief_api_progressive.md) ← こちらは LLMBackend attach 状態のベンチで fair
- [02 — 心理の深層 10 思考因子 × llive](./02_cognitive_factors.md)
- [03 — 数学・単位特化 AI (MATH-01/08)](./03_math_vertical.md)
- [04 — CABT 設計予告](./04_next_cabt_block_design.md)
- [05 — CREAT 設計予告](./05_next_creat_kj_mindmap.md)
- [06 — MATH-02 形式検証ゲート設計予告](./06_next_math02_formal_gate.md)

---

> 動作確認には成功、ただし fair 比較ではない。次回 (CABT-01 prototype + LLMBackend attach 後) に再走する。

---

# English

# llive vs Other LLMs Benchmark 2026-05-17 — The Smoke-Test Trap and Honest Disclosure

## TL;DR (Revised — fully rewritten because the original version contained anomalies)

- Ran a benchmark across 4 briefs × 6 models, doubling as an end-to-end smoke test of the Brief API implemented the same day
- We got a number like **llive 4/4 OK 134-184ms**, but this is a **"no LLM inference performed"** result and is therefore not a fair comparison
- As a smoke test it succeeded (Brief data flow / ledger / decision reproduced stably)
- **The fair quality/speed comparison is deferred to next time** (after the CABT-01 prototype + after attaching the LLMBackend), when we re-run
- We saved the raw data and caveats, and explicitly disclose the 3 anomalies before they could mislead anyone

## Anomalies Found (3)

After the user pointed out, "It's suspiciously fast — isn't there something odd in the responses?", we re-inspected the raw output. The following 3 anomalies (i.e., benchmark-design pitfalls) were found.

### Anomaly 1: The llive side never attached an LLMBackend

llive's bench runner (`fullsense/scripts/bench_run.py::run_llive`) invokes `llive/scripts/run_brief.py --json <brief>` as a subprocess. This `run_brief.py` constructs `FullSenseLoop(sandbox=True, debug=args.debug)` **without an LLM backend**.

As a result, the loop's `_inner_monologue` stage falls back to the **template path** (rule-based), and the output is:

```
Observation about 'manual': <brief content[:120]> — novel territory, worth exploring.
```

The same template structure for every brief. Because only the **first 120 characters** of the brief are inserted into thought.text, the "semantic content" of b1–b4 never reaches the loop.

### Anomaly 2: The `chars` metric measures the full JSON length

The `chars` column in `bench_run.py` is `len(p.stdout)` = the number of characters in the subprocess standard output (in JSON form).

- llive: the JSON structure (stim metadata + stages + plan + raw) is dominant → 884 chars
- ollama / perplexity: the LLM response text itself → 148–1733 chars, depending on the brief

So the fact that llive shows the same `884 chars` for 4/4 is **"because it emitted the same JSON structure"** and does not serve as a fair comparison metric for response content.

### Anomaly 3: The 134-184ms is subprocess RTT + JSON serialize time

Because the llive path has no LLM inference, the measured time consists of:

- py launcher startup + Python interpreter import (~80-120ms on Windows)
- passing through the 6 stages of `FullSenseLoop.process()` via the template path (~10-30ms)
- JSON output (~1ms)
- subprocess wait + stdout read (~10-30ms)

= 134-184ms. This is not LLM inference latency. The result is that "llive embedded" and "llive passing through via template fallback" produce the same wall time.

Reference: in a progressive matrix where an Ollama (llama3.2:3b) backend was attached to the same `FullSenseLoop`, it took 8.9 seconds at xs (cold) and roughly 1–2 seconds when warm (see [Article 01](./QIITA_%2301_brief_api_progressive.md)).

## Valuable Observations Nonetheless

Even accounting for honest disclosure, there are things this benchmark did confirm:

### ✅ The Brief API end-to-end data flow runs stably across 4 brief types

llive's Brief data flow:

1. brief text → `Stimulus` conversion
2. 6-stage loop (salience → curiosity → thought → ego/altruism → plan → output)
3. ledger append at each stage
4. returns the final decision (`note`)
5. JSON serialization and stdout output

was **reproduced for all 4 briefs** (subprocess return code 0, JSON parse success). This is valid as a **smoke test** of the Brief API implementation.

### ✅ Stability of the rule-based loop

Even without an LLMBackend, the loop runs deterministically and returns `decision=note` → confirming the robustness of the template fallback.

### ✅ Grasping the credential state of cloud / on-prem

| service | behavior | state |
|---|---|---|
| ollama llama3.2:3b (on-prem) | ✅ 4/4 OK | 12–20s/brief, real LLM inference running |
| perplexity (cloud Sonar) | ✅ 4/4 OK | 2.5–6s/brief, with citations |
| anthropic | ❌ ERR | `401 invalid_x-api-key`, awaiting rotate |
| gemini | ❌ ERR | `429 quota exceeded` |
| openai codex | ❌ ERR | `429 insufficient_quota` |

The recovery procedure is documented in Operator action 2 of `fullsense/docs/NEXT_SESSION.md`.

## The Originally Published Table (Retracted / Re-listed with Annotations)

Read the **llive rows in the table below as smoke-test data that did not go through LLM inference**. Do not reference them as a comparison of response quality or response speed:

| brief | model | status | wall (ms) | chars | note |
|---|---|---|---|---|---|
| b1 | llive | OK | 152 | 884 | ⚠️ template fallback (no LLM inference) |
| b1 | ollama | OK | 18 812 | 148 | real LLM inference |
| b1 | perplexity | OK | 4 555 | 192 | cloud LLM |
| b2 | llive | OK | 134 | 884 | ⚠️ template fallback |
| b2 | ollama | OK | 12 220 | 376 | real LLM inference |
| b2 | perplexity | OK | 4 011 | 251 | cloud LLM |
| b3 | llive | OK | 184 | 884 | ⚠️ template fallback |
| b3 | ollama | OK | 20 127 | 616 | real LLM inference |
| b3 | perplexity | OK | 2 547 | 365 | cloud LLM |
| b4 | llive | OK | 173 | 884 | ⚠️ template fallback |
| b4 | ollama | OK | 18 991 | 357 | real LLM inference |
| b4 | perplexity | OK | 6 019 | 1733 | cloud LLM |

## Fair Re-run Results (after the 2026-05-17 fix — within the same session that day)

We fixed `bench_run.py::run_llive` to be an **LLMBackend (ollama:llama3.2)-attached version**, and changed the chars metric to be taken from `stages.thought.text` (the actual LLM output), then re-ran:

| brief | model | status | wall (ms) | chars (actual LLM output) | note |
|---|---|---|---|---|---|
| b1 | llive (+llama3.2:3b) | OK | **32 750** | 377 | real LLM inference on the loop path |
| b1 | ollama direct (llama3.2:3b) | OK | 12 423 | 148 | comparison baseline |
| b1 | perplexity | OK | 2 411 | 297 | cloud (Sonar) |
| b2 | llive (+llama3.2:3b) | OK | **50 936** | 1 255 | |
| b2 | ollama | OK | 13 024 | 276 | |
| b2 | perplexity | OK | 3 591 | 225 | |
| b3 | llive (+llama3.2:3b) | OK | **43 787** | 531 | |
| b3 | ollama | OK | 19 610 | 469 | |
| b3 | perplexity | OK | 2 104 | 352 | |
| b4 | llive (+llama3.2:3b) | OK | **43 163** | 342 | |
| b4 | ollama | OK | 21 936 | 417 | |
| b4 | perplexity | OK | 6 162 | 855 | |

### Observations from the Fair Comparison

- **llive (LLM attached) is 2-4× slower than calling ollama directly** (32-51s vs 12-22s)
- Both incur exactly one LLM call. **The difference is that llive's build_llm_prompt wraps the brief for `_inner_monologue` and lengthens it** = the LLM inference time itself becomes longer
- The progressive matrix (overhead < 1%) did not compare in-loop vs direct calls on the same backend, so its "overhead" is a different thing entirely
- llive's **added value** is not time but structure (ledger / approval / governance / grounding / 6-stage trace) — if you judge on speed alone, calling ollama directly is better

### Raw Data of the Fair Re-run

Saved under `fullsense/docs/benchmarks/2026-05-17-fair/`:

```
2026-05-17-fair/
  b1/ {llive,ollama,perplexity,anthropic,gemini,codex}.txt
  b2/ ...
  b3/ ...
  b4/ ...
```

## Fix Items for the Next Fair Comparison

### 1. Update run_llive in bench_run.py

Switch `run_brief.py` to an LLMBackend-attached version, or call the new Brief API CLI (`llive brief submit --backend ollama:qwen2.5:14b ...`).

### 2. Make the chars metric fair

- llive: the length of `result.stages.thought.text` (response text only)
- others: response text as before
- separate the JSON-structure portion into a different column

### 3. Add comparison targets

As a comparison of the LLM inference layer:
- llive (ollama:qwen2.5:14b attached, with Brief Grounder + SafeCalculator)
- llive (ollama:qwen2.5:14b attached, plain)
- ollama qwen2.5:14b direct

comparing these 3 lineages for quality, speed, and citation accuracy would be fair.

### 4. Introduce quality metrics

In addition to speed and chars:
- spec compliance (pass rate against success_criteria)
- citation accuracy (verifiability of the provenance chain)
- safety (dangerous_token detection vs output)

## Lesson (Recorded as a TRIZ Contradiction)

> "Feeling like you've won the moment you take a benchmark" vs "Suspecting the benchmark's design flaws"

This is a classic R&D trap, and it's quite likely we would not have noticed it without the user's remark ("It's suspiciously fast").

The lesson will be saved to maintainer memory as `feedback_benchmark_honest_disclosure.md`.

## Sources

- raw data: `fullsense/docs/benchmarks/2026-05-17/b{1,2,3,4}/{model}.txt`
- bench runner: `fullsense/scripts/bench_run.py`
- the original version (which contained the anomalies) can be referenced in git history: `git log -- docs/articles/2026-05-17/07_bench_results.md`

## Other Materials Published the Same Day

- [01 — Brief API + progressive matrix (overhead < 1 %)](./01_brief_api_progressive.md) ← this one is fair, being a benchmark with the LLMBackend attached
- [02 — The depths of psychology: 10 thinking factors × llive](./02_cognitive_factors.md)
- [03 — Math/unit-specialized AI (MATH-01/08)](./03_math_vertical.md)
- [04 — CABT design preview](./04_next_cabt_block_design.md)
- [05 — CREAT design preview](./05_next_creat_kj_mindmap.md)
- [06 — MATH-02 formal verification gate design preview](./06_next_math02_formal_gate.md)

---

> The smoke test succeeded, but it is not a fair comparison. We will re-run next time (after the CABT-01 prototype + LLMBackend attach).

---

# 中文

# llive 与其他 LLM 基准测试 2026-05-17 — 冒烟测试的陷阱与诚实披露

## TL;DR (修订 — 因初版存在异常而全面重写)

- 借由对当日实现的 Brief API 进行 end-to-end 冒烟测试之机，跑了 4 brief × 6 model 的基准测试
- 虽然得出了 **llive 4/4 OK 134-184ms** 这样的数值，但这是 **「未进行 LLM 推理」的结果**，因此并非公平比较
- 作为冒烟测试是成功的 (Brief data flow / ledger / decision 稳定复现)
- **公平的质量·速度比较推迟到下次 (CABT-01 prototype 之后 + LLMBackend attach 之后)** 再跑
- 保存了 raw 数据与注意事项，并在引起误解之前明确披露 3 件异常

## 已确认的异常 (3 件)

在用户指出「快得有点奇怪，响应里没有什么不对劲的地方吗？」后，我们重新检查了 raw 输出。发现了以下 3 件异常 (= 基准测试设计的陷阱)。

### 异常 1: llive 一侧未 attach LLMBackend

llive 的 bench runner (`fullsense/scripts/bench_run.py::run_llive`) 以 subprocess 调用 `llive/scripts/run_brief.py --json <brief>`。这个 `run_brief.py` 在 **没有 LLM backend** 的情况下构建 `FullSenseLoop(sandbox=True, debug=args.debug)`。

结果，loop 的 `_inner_monologue` stage 落入 **template 路径** (rule-based)，输出为:

```
Observation about 'manual': <brief content[:120]> — novel territory, worth exploring.
```

所有 brief 都是同一个 template 结构。由于只有 brief 的 **前 120 个字符** 被插入 thought.text，b1～b4 的「语义内容」并未到达 loop。

### 异常 2: `chars` 度量测的是 JSON 全长

`bench_run.py` 的 `chars` 列是 `len(p.stdout)` = subprocess 标准输出 (JSON 形式) 的字符数。

- llive: JSON 结构 (stim metadata + stages + plan + raw) 占主导 → 884 chars
- ollama / perplexity: LLM 响应文本本身 → 148～1733 chars，取决于 brief

也就是说，llive 4/4 都是相同的 `884 chars`，是 **「因为吐出了相同的 JSON 结构」**，并不能作为响应内容的公平比较指标。

### 异常 3: 134-184ms 是 subprocess RTT + JSON serialize 时间

由于 llive 路径中没有 LLM 推理，所测量的时间为:

- py launcher 启动 + Python interpreter import (Windows 上约 80-120ms)
- 以 template 路径穿过 `FullSenseLoop.process()` 的 6 个 stage (约 10-30ms)
- JSON 输出 (约 1ms)
- subprocess wait + stdout 读取 (约 10-30ms)

= 134-184ms。这不是 LLM 推理延迟。结果是「内嵌 llive」与「以 template fallback 直接穿过 llive」给出了相同的 wall time。

参考: 在为同一个 `FullSenseLoop` attach 了 Ollama (llama3.2:3b) backend 的 progressive matrix 中，xs (cold) 时耗时 8.9 秒，warm 时约 1～2 秒 (参见 [文章 01](./QIITA_%2301_brief_api_progressive.md))。

## 即便如此仍有价值的观察

即使考虑到诚实披露，这次基准测试确实确认了一些事情:

### ✅ Brief API end-to-end 的 data flow 在 4 种 brief 下稳定运行

llive 的 Brief data flow:

1. brief 文本 → `Stimulus` 转换
2. 6 stage loop (salience → curiosity → thought → ego/altruism → plan → output)
3. 各 stage 处 ledger append
4. 返回 final decision (`note`)
5. JSON serialization 与 stdout 输出

在 **全部 4 个 brief 下都得到复现** (subprocess return code 0，JSON parse 成功)。这作为 Brief API 实现的 **冒烟测试** 是有效的。

### ✅ rule-based loop 的稳定性

即使没有 LLMBackend，loop 也确定性地运行并返回 `decision=note` → 确认了 template fallback 的健壮性。

### ✅ 掌握 cloud / on-prem 的 credential 状态

| service | 运行 | 状态 |
|---|---|---|
| ollama llama3.2:3b (on-prem) | ✅ 4/4 OK | 12～20s/brief，实际 LLM 推理运行中 |
| perplexity (cloud Sonar) | ✅ 4/4 OK | 2.5～6s/brief，带 citation |
| anthropic | ❌ ERR | `401 invalid_x-api-key`，等待 rotate |
| gemini | ❌ ERR | `429 quota exceeded` |
| openai codex | ❌ ERR | `429 insufficient_quota` |

恢复步骤已记载于 `fullsense/docs/NEXT_SESSION.md` 的 Operator action 2。

## 当初发布的表格 (撤回 / 附注后再列)

请将下表的 **llive 行作为未经过 LLM 推理的冒烟测试数据** 来阅读。不要将其作为响应质量或响应速度比较来参考:

| brief | model | status | wall (ms) | chars | 注记 |
|---|---|---|---|---|---|
| b1 | llive | OK | 152 | 884 | ⚠️ template fallback (无 LLM 推理) |
| b1 | ollama | OK | 18 812 | 148 | 实际 LLM 推理 |
| b1 | perplexity | OK | 4 555 | 192 | cloud LLM |
| b2 | llive | OK | 134 | 884 | ⚠️ template fallback |
| b2 | ollama | OK | 12 220 | 376 | 实际 LLM 推理 |
| b2 | perplexity | OK | 4 011 | 251 | cloud LLM |
| b3 | llive | OK | 184 | 884 | ⚠️ template fallback |
| b3 | ollama | OK | 20 127 | 616 | 实际 LLM 推理 |
| b3 | perplexity | OK | 2 547 | 365 | cloud LLM |
| b4 | llive | OK | 173 | 884 | ⚠️ template fallback |
| b4 | ollama | OK | 18 991 | 357 | 实际 LLM 推理 |
| b4 | perplexity | OK | 6 019 | 1733 | cloud LLM |

## Fair 再跑结果 (2026-05-17 修正后 — 同日同 session 内)

我们将 `bench_run.py::run_llive` 修正为 **attach 了 LLMBackend (ollama:llama3.2) 的版本**，并将 chars 度量改为从 `stages.thought.text` (LLM 实际输出) 取值，然后再跑:

| brief | model | status | wall (ms) | chars (LLM 实际输出) | 注记 |
|---|---|---|---|---|---|
| b1 | llive (+llama3.2:3b) | OK | **32 750** | 377 | loop 路径上的实际 LLM 推理 |
| b1 | ollama 直接调用 (llama3.2:3b) | OK | 12 423 | 148 | 比较 baseline |
| b1 | perplexity | OK | 2 411 | 297 | cloud (Sonar) |
| b2 | llive (+llama3.2:3b) | OK | **50 936** | 1 255 | |
| b2 | ollama | OK | 13 024 | 276 | |
| b2 | perplexity | OK | 3 591 | 225 | |
| b3 | llive (+llama3.2:3b) | OK | **43 787** | 531 | |
| b3 | ollama | OK | 19 610 | 469 | |
| b3 | perplexity | OK | 2 104 | 352 | |
| b4 | llive (+llama3.2:3b) | OK | **43 163** | 342 | |
| b4 | ollama | OK | 21 936 | 417 | |
| b4 | perplexity | OK | 6 162 | 855 | |

### Fair 比较的观察

- **llive (attach 了 LLM) 比直接调用 ollama 慢 2-4 倍** (32-51s vs 12-22s)
- 两者都恰好进行一次 LLM call。**差异在于 llive 的 build_llm_prompt 将 brief 为 `_inner_monologue` 进行包装而使其变长** = LLM 推理时间本身变长
- progressive matrix (overhead < 1%) 并未在同一 backend 上比较 loop 内 vs 直接调用，因此其「overhead」是完全不同的东西
- llive 的 **附加价值** 不在于时间而在于结构 (ledger / approval / governance / grounding / 6 stage trace) — 若仅以速度判断，直接调用 ollama 更好

### fair 再跑的原始数据

保存于 `fullsense/docs/benchmarks/2026-05-17-fair/`:

```
2026-05-17-fair/
  b1/ {llive,ollama,perplexity,anthropic,gemini,codex}.txt
  b2/ ...
  b3/ ...
  b4/ ...
```

## 为下次公平比较的修正项

### 1. 更新 bench_run.py 的 run_llive

将 `run_brief.py` 切换为 attach 了 LLMBackend 的版本，或调用新的 Brief API CLI (`llive brief submit --backend ollama:qwen2.5:14b ...`)。

### 2. 使 chars 度量公平化

- llive: `result.stages.thought.text` 的长度 (仅响应文本)
- 其他: 一如既往的 response text
- 将 JSON 结构部分分离到单独的列

### 3. 增加比较对象

作为 LLM 推理层的比较:
- llive (ollama:qwen2.5:14b attached，带 Brief Grounder + SafeCalculator)
- llive (ollama:qwen2.5:14b attached，plain)
- ollama qwen2.5:14b 直接调用

以这 3 个系统比较质量、速度与 citation 精度才算公平。

### 4. 引入质量度量

除 speed 与 chars 之外:
- spec compliance (对 success_criteria 的合格率)
- citation 精度 (provenance chain 的可验证性)
- safety (dangerous_token 检出 vs 输出)

## 教训 (作为 TRIZ 矛盾的记录)

> 「取了基准的瞬间就觉得自己赢了」 vs 「怀疑基准的设计缺陷」

这是典型的研发陷阱，若没有用户的指点 (「快得有点奇怪」)，很可能就不会察觉。

教训将作为 `feedback_benchmark_honest_disclosure.md` 保存到 maintainer memory。

## 来源

- raw data: `fullsense/docs/benchmarks/2026-05-17/b{1,2,3,4}/{model}.txt`
- bench runner: `fullsense/scripts/bench_run.py`
- 当初版本 (含异常) 可在 git 历史中参考: `git log -- docs/articles/2026-05-17/07_bench_results.md`

## 当日的其他公开资料

- [01 — Brief API + progressive matrix (overhead < 1 %)](./01_brief_api_progressive.md) ← 这一篇是 attach 了 LLMBackend 状态的基准，公平
- [02 — 心理的深层: 10 思考因子 × llive](./02_cognitive_factors.md)
- [03 — 数学·单位特化 AI (MATH-01/08)](./03_math_vertical.md)
- [04 — CABT 设计预告](./04_next_cabt_block_design.md)
- [05 — CREAT 设计预告](./05_next_creat_kj_mindmap.md)
- [06 — MATH-02 形式验证 gate 设计预告](./06_next_math02_formal_gate.md)

---

> 冒烟测试成功，但并非公平比较。下次 (CABT-01 prototype + LLMBackend attach 之后) 再跑。

---

# 한국어

# llive vs 다른 LLM 벤치마크 2026-05-17 — 동작 확인의 함정과 honest disclosure

## TL;DR (개정 — 초기 버전에 이상이 있어 전면 재작성)

- 같은 날 구현한 Brief API의 end-to-end 동작 확인을 겸하여 4 brief × 6 model 벤치를 실행
- **llive 4/4 OK 134-184ms**라는 수치가 나왔지만, 이것은 **「LLM 추론을 하지 않은」 결과**이며 fair한 비교가 아니다
- 동작 확인으로서는 성공 (Brief data flow / ledger / decision이 안정적으로 재현됨)
- **fair한 품질·속도 비교는 다음 번 (CABT-01 prototype 이후 + LLMBackend attach 이후)** 에 재실행
- raw 데이터와 주의점을 저장하고, 오해를 부르기 전에 이상 3건을 명시적으로 공개

## 확인된 이상 (3건)

사용자로부터 「이상하게 빠르네요, 응답에 뭔가 이상한 부분은 없나요?」라는 지적을 받고 raw 출력을 재검사했다. 다음 3가지 이상 (= 벤치 설계의 함정) 이 발견되었다.

### 이상 1: llive 쪽이 LLMBackend를 attach하지 않았다

llive의 bench runner (`fullsense/scripts/bench_run.py::run_llive`) 는 `llive/scripts/run_brief.py --json <brief>` 를 subprocess로 호출한다. 이 `run_brief.py` 는 `FullSenseLoop(sandbox=True, debug=args.debug)` 를 **LLM backend 없이** 구성한다.

그 결과 loop의 `_inner_monologue` stage는 **template 경로** (rule-based) 로 떨어지고, 출력은:

```
Observation about 'manual': <brief content[:120]> — novel territory, worth exploring.
```

모든 brief에서 동일한 template 구조. brief의 **선두 120자** 만 thought.text에 삽입되기 때문에 b1～b4의 "의미적 내용"은 loop에 도달하지 않는다.

### 이상 2: `chars` 메트릭은 JSON 전체 길이를 재고 있다

`bench_run.py` 의 `chars` 열은 `len(p.stdout)` = subprocess 표준 출력 (JSON 형식) 의 문자 수다.

- llive: JSON 구조 (stim metadata + stages + plan + raw) 가 dominant → 884 chars
- ollama / perplexity: LLM 응답 텍스트 그 자체 → brief에 따라 148～1733 chars

즉 llive 4/4가 동일하게 `884 chars`인 것은 **「같은 JSON 구조를 토해냈기 때문」**이며, 응답 내용으로서 fair한 비교 지표가 되지 못한다.

### 이상 3: 134-184ms는 subprocess RTT + JSON serialize 시간

llive 경로에 LLM 추론이 없기 때문에 측정 시간은:

- py launcher 시작 + Python interpreter import (Windows에서 ~80-120ms)
- `FullSenseLoop.process()` 의 6 stage를 template 경로로 빠져나감 (~10-30ms)
- JSON 출력 (~1ms)
- subprocess wait + stdout 읽기 (~10-30ms)

= 134-184ms. LLM 추론 레이턴시가 아니다. 「llive를 내장」과 「llive를 template fallback으로 그냥 통과」가 같은 wall time을 내는 결과가 되고 있다.

참고: 같은 `FullSenseLoop`에 Ollama (llama3.2:3b) backend를 attach한 progressive matrix에서는 xs (cold) 에서 8.9초, warm에서 1～2초 정도 걸렸다 ([기사 01](./QIITA_%2301_brief_api_progressive.md) 참조).

## 그래도 가치 있는 관찰

honest disclosure를 감안하더라도 이 벤치에서 확인할 수 있었던 것은 존재한다:

### ✅ Brief API end-to-end의 data flow가 4종의 brief에서 안정 동작

llive의 Brief data flow:

1. brief 텍스트 → `Stimulus` 변환
2. 6 stage loop (salience → curiosity → thought → ego/altruism → plan → output)
3. 각 stage에서 ledger append
4. final decision (`note`) 반환
5. JSON serialization과 stdout 출력

을 **4 brief 모두에서 재현** (subprocess return code 0, JSON parse 성공). 이는 Brief API 구현의 **동작 확인** 으로서는 유효하다.

### ✅ rule-based loop의 안정성

LLMBackend가 없어도 loop가 deterministic하게 실행되어 `decision=note` 를 반환 → template fallback의 견고함 확인.

### ✅ cloud / on-prem의 credential 상태 파악

| service | 동작 | 상태 |
|---|---|---|
| ollama llama3.2:3b (on-prem) | ✅ 4/4 OK | 12～20s/brief, 실제 LLM 추론 동작 중 |
| perplexity (cloud Sonar) | ✅ 4/4 OK | 2.5～6s/brief, citation 포함 |
| anthropic | ❌ ERR | `401 invalid_x-api-key` rotate 대기 |
| gemini | ❌ ERR | `429 quota exceeded` |
| openai codex | ❌ ERR | `429 insufficient_quota` |

복구 절차는 `fullsense/docs/NEXT_SESSION.md` 의 Operator action 2에 기재되어 있다.

## 당초 발표했던 표 (취소 / 주석 첨부 재게재)

아래 표의 **llive 행은 LLM 추론을 거치지 않은 동작 확인 데이터** 로 읽을 것. 응답 품질이나 응답 속도 비교로 참조하지 말 것:

| brief | model | status | wall (ms) | chars | 주석 |
|---|---|---|---|---|---|
| b1 | llive | OK | 152 | 884 | ⚠️ template fallback (LLM 추론 없음) |
| b1 | ollama | OK | 18 812 | 148 | 실제 LLM 추론 |
| b1 | perplexity | OK | 4 555 | 192 | cloud LLM |
| b2 | llive | OK | 134 | 884 | ⚠️ template fallback |
| b2 | ollama | OK | 12 220 | 376 | 실제 LLM 추론 |
| b2 | perplexity | OK | 4 011 | 251 | cloud LLM |
| b3 | llive | OK | 184 | 884 | ⚠️ template fallback |
| b3 | ollama | OK | 20 127 | 616 | 실제 LLM 추론 |
| b3 | perplexity | OK | 2 547 | 365 | cloud LLM |
| b4 | llive | OK | 173 | 884 | ⚠️ template fallback |
| b4 | ollama | OK | 18 991 | 357 | 실제 LLM 추론 |
| b4 | perplexity | OK | 6 019 | 1733 | cloud LLM |

## Fair 재실행 결과 (2026-05-17 수정 후 — 같은 날 같은 세션 내)

`bench_run.py::run_llive` 를 **LLMBackend (ollama:llama3.2) attach 버전**으로 수정하고, chars 메트릭을 `stages.thought.text` (LLM 실제 출력) 에서 취하도록 변경하여 재실행:

| brief | model | status | wall (ms) | chars (LLM 실제 출력) | 주석 |
|---|---|---|---|---|---|
| b1 | llive (+llama3.2:3b) | OK | **32 750** | 377 | loop 경로에서 실제 LLM 추론 |
| b1 | ollama 직접 호출 (llama3.2:3b) | OK | 12 423 | 148 | 비교 baseline |
| b1 | perplexity | OK | 2 411 | 297 | cloud (Sonar) |
| b2 | llive (+llama3.2:3b) | OK | **50 936** | 1 255 | |
| b2 | ollama | OK | 13 024 | 276 | |
| b2 | perplexity | OK | 3 591 | 225 | |
| b3 | llive (+llama3.2:3b) | OK | **43 787** | 531 | |
| b3 | ollama | OK | 19 610 | 469 | |
| b3 | perplexity | OK | 2 104 | 352 | |
| b4 | llive (+llama3.2:3b) | OK | **43 163** | 342 | |
| b4 | ollama | OK | 21 936 | 417 | |
| b4 | perplexity | OK | 6 162 | 855 | |

### Fair 비교의 관찰

- **llive (LLM attached) 는 ollama 직접 호출의 2-4배 느리다** (32-51s vs 12-22s)
- LLM call이 1회 들어가는 점은 양자 동일. **차이는 llive의 build_llm_prompt가 brief를 `_inner_monologue` 용으로 래핑하여 장문화시키는 것** = LLM 추론 시간 자체가 길어진다
- progressive matrix (overhead < 1%) 는 같은 백엔드에서 loop 내 vs 직접 호출을 비교하지 않았기 때문에 그 「overhead」 와는 별개의 것이다
- llive의 **부가가치** 는 시간이 아니라 구조 (ledger / approval / governance / grounding / 6 stage trace) 에 있다 — 속도만으로 판단한다면 ollama 직접 호출 쪽이 낫다

### fair 재실행의 raw 데이터

`fullsense/docs/benchmarks/2026-05-17-fair/` 에 저장:

```
2026-05-17-fair/
  b1/ {llive,ollama,perplexity,anthropic,gemini,codex}.txt
  b2/ ...
  b3/ ...
  b4/ ...
```

## 다음 fair 비교를 위한 수정 항목

### 1. bench_run.py의 run_llive 갱신

`run_brief.py` 를 LLMBackend attach 버전으로 전환하거나, 새 Brief API CLI (`llive brief submit --backend ollama:qwen2.5:14b ...`) 를 호출.

### 2. chars 메트릭의 공평화

- llive: `result.stages.thought.text` 의 길이 (응답 텍스트만)
- 그 외: 기존대로 response text
- JSON 구조 부분은 별도 컬럼으로 분리

### 3. 비교 대상의 추가

LLM 추론 레이어의 비교로서:
- llive (ollama:qwen2.5:14b attached, Brief Grounder + SafeCalculator 있음)
- llive (ollama:qwen2.5:14b attached, plain)
- ollama qwen2.5:14b 직접 호출

이 3 계통으로 품질·속도·citation 정확도를 비교하는 것이 fair하다.

### 4. 품질 메트릭의 도입

speed와 chars에 더하여:
- spec compliance (success_criteria에 대한 합격률)
- citation 정확도 (provenance chain의 검증 가능성)
- safety (dangerous_token 검출 vs 출력)

## 교훈 (TRIZ 모순으로서의 기록)

> 「벤치를 측정한 순간 이긴 기분이 든다」 vs 「벤치의 설계 결함을 의심한다」

이는 전형적인 연구개발의 함정으로, 사용자의 지적 (「이상하게 빠르네요」) 이 없었다면 알아차리지 못했을 가능성이 높다.

교훈을 `feedback_benchmark_honest_disclosure.md` 로 maintainer memory에 저장할 예정.

## 소스

- raw data: `fullsense/docs/benchmarks/2026-05-17/b{1,2,3,4}/{model}.txt`
- bench runner: `fullsense/scripts/bench_run.py`
- 당초 버전 (이상 포함) 은 git 이력에서 참조 가능: `git log -- docs/articles/2026-05-17/07_bench_results.md`

## 같은 날의 다른 공개 자료

- [01 — Brief API + progressive matrix (overhead < 1 %)](./01_brief_api_progressive.md) ← 이쪽은 LLMBackend attach 상태의 벤치라서 fair
- [02 — 심리의 심층 10 사고 인자 × llive](./02_cognitive_factors.md)
- [03 — 수학·단위 특화 AI (MATH-01/08)](./03_math_vertical.md)
- [04 — CABT 설계 예고](./04_next_cabt_block_design.md)
- [05 — CREAT 설계 예고](./05_next_creat_kj_mindmap.md)
- [06 — MATH-02 형식 검증 gate 설계 예고](./06_next_math02_formal_gate.md)

---

> 동작 확인에는 성공, 다만 fair 비교는 아니다. 다음 번 (CABT-01 prototype + LLMBackend attach 이후) 에 재실행한다.
