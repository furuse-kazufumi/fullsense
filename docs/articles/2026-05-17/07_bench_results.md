---
layout: default
title: "llive vs 他 LLM 比較ベンチマーク 2026-05-17 — 動作確認 + 速度"
date: 2026-05-17
tags: [llm, benchmark, on-prem, ollama, perplexity, llive]
---

# llive vs 他 LLM 比較ベンチマーク 2026-05-17 — 動作確認 + 速度

## TL;DR

- 同日実装した Brief API end-to-end の動作確認を兼ね、4 brief × 6 model のセル行列で実走
- **llive Brief API 経路は 4/4 で安定応答 (134-184 ms / brief)** — 構造データ flow + ledger + decision が全 brief で機能
- ollama (llama3.2:3b on-prem) は 4/4 OK で実 LLM 推論 12-20 s
- perplexity (cloud Sonar) は 4/4 OK で 2.5-6 s
- anthropic / gemini / codex は credential 復旧待ちで全 ERR (NEXT_SESSION 既知の制約)
- raw 結果は `docs/benchmarks/2026-05-17/` に保存

## 重要な前提 (honest disclosure)

このベンチは **「動作確認 + データ flow 速度」が主目的**で、「品質比較」ではありません。理由:

llive 側は **LLMBackend を attach せず template fallback で実走**しています。つまり「llive が LLM を呼んで生成した」ではなく「llive が Brief を受けて 6 stage loop を回し、構造化された応答テンプレートを出した」結果。

公正な品質比較は CABT-01 (S2, HF forward hook) や Brief Grounder × LLM backend を attach した経路で別途取ります。今回は:

- ✅ Brief API → BriefRunner → Loop → ledger → decision の data flow 動作確認
- ✅ 各クライアント (cloud, on-prem) の応答時間プロファイル
- ⚠️ Quality 比較は **次回 (CABT-01 prototype 後)**

## ベンチマーク matrix

### Run config

- 4 brief: `b1` Mermaid 図 / `b2` Quick Start + MCP seq diag / `b3` lltrade strategy YAML / `b4` lltrade backtest config
- 6 model: codex / gemini / llive / anthropic / perplexity / ollama (llama3.2:3b)
- 出力 root: `D:/projects/fullsense/docs/benchmarks/2026-05-17/`
- runner: `D:/projects/fullsense/scripts/bench_run.py`

### Wall-time / status matrix

| brief | model | status | wall-time (ms) | response chars |
|---|---|---|---|---|
| b1 | codex | **ERR** | 0 | 21 (error) |
| b1 | gemini | **ERR** | 189 | 300 (error) |
| b1 | **llive** | **OK** | **152** | 884 |
| b1 | anthropic | **ERR** | 307 | 130 (error) |
| b1 | perplexity | **OK** | 4 555 | 192 |
| b1 | ollama | **OK** | 18 812 | 148 |
| b2 | codex | **ERR** | 0 | 21 |
| b2 | gemini | **ERR** | 136 | 300 |
| b2 | **llive** | **OK** | **134** | 884 |
| b2 | anthropic | **ERR** | 317 | 130 |
| b2 | perplexity | **OK** | 4 011 | 251 |
| b2 | ollama | **OK** | 12 220 | 376 |
| b3 | codex | **ERR** | 0 | 21 |
| b3 | gemini | **ERR** | 138 | 300 |
| b3 | **llive** | **OK** | **184** | 884 |
| b3 | anthropic | **ERR** | 303 | 130 |
| b3 | perplexity | **OK** | 2 547 | 365 |
| b3 | ollama | **OK** | 20 127 | 616 |
| b4 | codex | **ERR** | 0 | 21 |
| b4 | gemini | **ERR** | 120 | 300 |
| b4 | **llive** | **OK** | **173** | 884 |
| b4 | anthropic | **ERR** | 281 | 130 |
| b4 | perplexity | **OK** | 6 019 | 1733 |
| b4 | ollama | **OK** | 18 991 | 357 |

### Summary by model

| model | OK | ERR | avg wall (ms) | comment |
|---|---|---|---|---|
| **llive (Brief API, template path)** | **4/4** | 0 | **161** | 構造データ flow 動作確認、極高速 |
| ollama llama3.2:3b (on-prem) | 4/4 | 0 | 17 538 | 実 LLM 推論、応答長は brief 依存 |
| perplexity (cloud Sonar) | 4/4 | 0 | 4 283 | citation 付き、長文化が brief 依存 |
| anthropic (cloud) | 0/4 | 4 | — | credential 復旧待ち (`401 invalid_x-api-key`) |
| gemini (cloud) | 0/4 | 4 | — | quota 復旧待ち (`429`) |
| codex (cloud) | 0/4 | 4 | — | quota 復旧待ち (`429`) |

## 解釈

### 1. Brief API end-to-end が brief 4 種で完走

これが今日の主目的。llive の Brief data flow が:

- 入力 brief を Stimulus に変換
- 6 stage loop (salience → curiosity → thought → ego/altruism → plan → output) を回す
- 各 stage で ledger に append
- final decision (`note`) を返す

を **どの brief でも安定再現**することを確認しました。raw JSON は `docs/benchmarks/2026-05-17/b*/llive.txt` に保存。

### 2. llive 4/4 で全て `decision=note`

これは progressive matrix (xs/s/m/l/xl × 3 models = 15 セル) でも観察された性質。**loop は brief の token 量・内容に対し決定木が動じない**。Brief を受け取って template 経路で応答する設計の堅牢性確認。

### 3. on-prem (ollama) の応答時間は 12-20 秒

cold start を含むため初回が遅い (xs progressive で 8.9 s だった llama3.2:3b が brief b3 で 20 s)。secondary 効果として、brief の token 量で LLM 出力が膨張すると wall も伸びる (b4: 18.9 s で 357 chars)。

### 4. cloud (perplexity) は 2.5-6 秒

citation の質は次節 (品質ベンチ) で別途検証予定。今日は速度プロファイルのみ。

### 5. 他 3 cloud は credential 復旧待ち

| service | error | 復旧方法 |
|---|---|---|
| anthropic | 401 invalid_x-api-key | console.anthropic.com → API Keys → rotate |
| gemini | 429 quota exceeded | aistudio.google.com → billing or new project |
| openai codex | 429 insufficient_quota | platform.openai.com → billing |

復旧後は `D:/api-keys.json` を更新するだけで `bench_run.py --all` が動きます (NEXT_SESSION.md `🧑 Operator action 2`)。

## 残作業

このベンチで「動作確認」は完了。次のステップ:

1. **CABT-01 prototype 後**: llive に LLMBackend (ollama:qwen2.5:14b) を attach → 「llive 経由」vs「ollama 直叩き」の品質比較
2. **MATH-08 grounder 統合後**: Brief 内の式が SafeCalculator で grounded → 計算精度品質比較
3. **credential 復旧後**: anthropic Haiku 4.5 / gemini 2.0 / openai codex も含む 6-model full matrix

## ソース

- raw data: `D:/projects/fullsense/docs/benchmarks/2026-05-17/b{1,2,3,4}/{model}.txt`
- bench runner: `D:/projects/fullsense/scripts/bench_run.py`
- 4 brief 出典: `D:/projects/fullsense/docs/benchmarks/2026-05-16{,-b2,-b3,-b4}/_brief.txt`
- methodology: [`feedback_competitor_benchmark`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_competitor_benchmark.md)
- 純度ルール: [`feedback_llive_measurement_purity`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_llive_measurement_purity.md)

## 同日の他公開資料

- [01 — Brief API + progressive matrix (overhead < 1 %)](./01_brief_api_progressive.md)
- [02 — 心理の深層 10 思考因子 × llive (9/10 実装済)](./02_cognitive_factors.md)
- [03 — 数学・単位特化 AI (MATH-01/08)](./03_math_vertical.md)
- [04 — Transformer ブロック高度化 7 アプローチ (CABT 設計予告)](./04_next_cabt_block_design.md)
- [05 — LLM × KJ法 × MindMap で要件定義自動化 (CREAT 設計予告)](./05_next_creat_kj_mindmap.md)
- [06 — 形式検証ゲートで LLM 数式幻覚を止める (MATH-02 設計予告)](./06_next_math02_formal_gate.md)

---

> 動作確認ベンチ。「llive 4/4 OK 134-184ms」は data flow と決定論的応答経路の安定性を示すもので、生成品質比較は次回 (CABT-01 prototype 後 + credential 復旧後) に行います。
