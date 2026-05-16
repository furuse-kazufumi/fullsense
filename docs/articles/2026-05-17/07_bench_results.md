---
layout: default
title: "llive vs 他 LLM ベンチマーク 2026-05-17 — 動作確認の罠と honest disclosure"
date: 2026-05-17
tags: [llm, benchmark, on-prem, ollama, perplexity, llive, methodology]
---

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

llive の bench runner (`fullsense/scripts/bench_run.py::run_llive`) は `D:/projects/llive/scripts/run_brief.py --json <brief>` を subprocess 呼出。この `run_brief.py` は `FullSenseLoop(sandbox=True, debug=args.debug)` を **LLM backend なし** で構築する。

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

参考: 同じ `FullSenseLoop` に Ollama (llama3.2:3b) backend を attach した progressive matrix では xs (cold) で 8.9 秒、warm で 1〜2 秒程度かかる ([記事 01]({{ '/articles/2026-05-17/01_brief_api_progressive' | relative_url }}) 参照)。

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

復旧手順は `D:/projects/fullsense/docs/NEXT_SESSION.md` の Operator action 2 に記載済。

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

- raw data: `D:/projects/fullsense/docs/benchmarks/2026-05-17/b{1,2,3,4}/{model}.txt`
- bench runner: `D:/projects/fullsense/scripts/bench_run.py`
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
