---
layout: default
title: "llive 開発履歴 — 5 日で v0.1 から v0.7 候補へ"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags: llive 開発履歴 LLM 設計判断 振り返り
id: 504036f1116fcd976dd3
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# llive 開発履歴 — 5 日で v0.1 から v0.7 候補へ

> 📚 **連載ナビ**: ← #11 [Qwen と相互補完する llive（隙間を埋める設計）](./QIITA_#11_complementary_with_qwen.md) ｜ **#12 本記事**（5 日間を時系列で振り返る開発履歴）｜ #13 [コーパス先行戦略（なぜ 5 日で進めたか）](./QIITA_#13_corpus_first_advantage.md) → 。※ 各記事は単独でも読めます。
>
> 前記事 #11 までは llive の **設計の中身**（Qwen との補完、構造の独自性）を扱ってきた。本記事はいったん視点を引いて、その設計が **どんな順番でどう積み上がったか** を 5 日分の時系列で振り返る。

著者: **古瀬 和文（ぷるやん）**

## なぜ開発履歴を残すか

llive (リブ) は 2026-05-13 に発足した自己進化型 LLM フレームワーク。本記事は **発足から本日 (2026-05-17) までの 5 日間で何をどう作り、何で躓き、何を学んだか** を時系列でまとめたものです。

- 設計判断の理由を残す
- 失敗を honest に残す (`feedback_benchmark_honest_disclosure` 教訓)
- 「なぜそうなっているか」が後から分かる状態を維持
- 翌日以降の自分 (および Claude Opus 4.7 ccr 経由) が文脈を読めるように

## 5 日間の超概要

| Day | 日付 | バージョン | キーワード |
|---|---|---|---|
| 1 | 2026-05-13 | v0.1.0 | プロジェクト発足 + Phase 1 MVR 完走 |
| 2 | 2026-05-13 | v0.2.0 | Phase 2 Adaptive Modular System |
| 3 | 2026-05-14 | v0.3.0 → v0.5.0 | Phase 3 (Evolve) + Phase 4 (Security) + Phase 5 (Rust) |
| 4 | 2026-05-16 | v0.6.0 | 9 axes skeleton + Apache 2.0 + FullSense umbrella |
| 5 | 2026-05-17 | v0.7 候補 (本日) | Brief API + COG-FX + MATH + ORG-FX 要件化 |

5 日でテスト数は 49 → 1014 (約 21 倍)、コードは MVR から 9 軸 + 32 件 v0.7+ 要件まで。

## Day 1: 2026-05-13 (Tue) — 発足とPhase 1 MVR

### 発足の背景

llmesh (secure LLM hub) と llove (TUI dashboard) という 2 製品を既に持っていた状態で、第三のメンバーとして **「自己進化型モジュラー記憶 LLM フレームワーク」** を作る判断。命名は `l` から始まる 4 文字 (llmesh / llove / llive) で統一。

### 設計の核 (Day 1 で確立、現在まで不変)

1. 固定 Decoder-only LLM コア + 可変周辺で能力吸収
2. 4 層メモリ (semantic / episodic / structural / parameter) の責務分離
3. 宣言的構造記述 (YAML)
4. 審査付き自己進化 (オンライン制限 + オフライン審査経由のみ昇格)
5. 生物学的記憶モデル (海馬-皮質 consolidation cycle)
6. 形式検証付き promotion (Lean / Z3 / TLA+)
7. llmesh / llove ファミリー統合
8. TRIZ 内蔵 (40 原理 + 矛盾マトリクス)

### v0.1.0 リリース

- GSD `/gsd-new-project` で初期化 → PROJECT.md / REQUIREMENTS.md (46 reqs) / ROADMAP.md (4 phases) / STATE.md / config.json 生成
- src/llive/ 8 層: schema / core / container / memory / router / evolution / observability / triz
- 49 tests pass / 82% coverage
- CLI: `llive run --template specs/templates/qwen2_5_0_5b.yaml --prompt "..." --mock`
- 設計判断: faiss / torch / sentence-transformers は **optional extras** にして、Phase 1 テストは numpy + hash 埋め込み fallback で動かす

### 教訓

- Optional extras 設計が Windows + CI の両立に必須
- GSD ワークフロー (`--auto` モード) で 1 日で Phase 1 完走可能

## Day 2: 2026-05-13 (Tue 夜) — Phase 2 Adaptive

### v0.2.0 リリース

- structural memory (graph) + parameter memory (adapter store) 追加
- Bayesian Surprise Gate (FR-21) でメモリ書き込み閾値を動的化
- Consolidation サイクルが夜間 batch で走る
- llove TUI で route trace + memory link viz
- LLM Wiki 統合 (LLW-04)
- 連続 5 タスク学習で BWT ≥ -1% を達成
- **308 tests / 99% coverage / 0 lint**

### 設計判断

- "Bayesian surprise" として書き込み制御 → 単なる threshold より柔軟
- 4 層メモリの間に **phase transition** (short → mid → long → archived → erased) を入れて life cycle 管理

## Day 3: 2026-05-14 (Wed) — 大規模自律セッション

ここから 1 日で 3 バージョン (v0.3 → v0.4 → v0.5) を進めた。

### v0.3.0 — Phase 3 (Controlled Self-Evolution) + Phase 4 (Production Security) 同時リリース

Phase 3 (Evolve):
- EVO-04 Z3 静的検証
- EVO-06 Failed Reservoir (DuckDB 順序保持)
- EVO-07 Reverse-Evo Monitor (JSONL audit)
- TRIZ-02 Contradiction Detector
- TRIZ-03 Principle Mapper (39×39 matrix)
- TRIZ-04 RAD-Backed Idea Generator (pluggable IdeaLLM Protocol)
- TRIZ-07 Self-Reflection Session
- LLW-04 Wiki Contradiction
- LLW-05 Wiki diff ChangeOp

Phase 4 (Security):
- SEC-01 Quarantined Memory Zone
- SEC-02 Ed25519 Signed Adapter
- SEC-03 SHA-256 audit hash chain (stdlib sqlite3 のみ)

**429 tests / 98% coverage / 0 lint**

### v0.4.0 — Phase 5 Rust skeleton

- `crates/llive_rust_ext/` PyO3 0.22 + maturin scaffold
- RUST-01 (skeleton) / RUST-02 (compute_surprise baseline) / RUST-04 (jaccard baseline) / RUST-13 (Hypothesis parity 1e-6)
- `llive.rust_ext.HAS_RUST` flag + Python fallback
- 439 tests pass

### v0.5.0 — Phase 5 wire-in

- RUST-03 (bulk_time_decay) Rust kernel + Python wrapper + 5 parity tests
- BayesianSurpriseGate.compute_surprise が rust_ext.HAS_RUST 時に自動委譲 (numpy fallback)
- EdgeWeightUpdater.apply_time_decay が rust_ext.bulk_time_decay で 1 pass precompute
- **444 tests / 98% coverage / 0 lint**

### Day 3 の設計判断

- **Rust 移植は意味論固定後** に段階的に (5x 性能向上ゲート設定)
- 全 RUST-XX 拡張は **Python fallback 必須**、Rust 不在環境でも動作維持
- 残 RUST-02 rayon / 05 jsonschema-rs / 06 crossbeam / 07 ChangeOp / 08 hora HNSW / 09 tokio async / 10 phf TRIZ / 11 Z3 bridge は v0.7 まで deferred

### Day 3 の教訓

- 1 日で 3 バージョン進めるには **コア設計** と **Optional extras 設計** が必須
- 「ベンチで 5x 出たら採用、そうでなければ revert」のゲートを明示

## Day 4: 2026-05-16 (Thu) — 9 axes + Apache 2.0 + FullSense umbrella

### v0.6.0 リリース

- **9 axes skeleton** 完成 — KAR / DTKR / APO / ICP / TLB / Math / PM / RPAR / SIL
- C-1 Approval Bus production 化 (Policy + SQLite Ledger)
- C-2 `@govern` + ProductionOutputBus (Policy gate × 副作用 emit)
- C-3 Cross-substrate migration spike (§MI1)
- C-14 ICP IdleCollaborator MVP (idle 中 peer LLM 問い合わせ)
- **970 PASS / 0 lint**

### 法務・ブランド整備

- **Apache-2.0 + Commercial dual-license** 切替
- **FullSense umbrella ブランド** 導入 (llmesh / llive / llove の親)
- NOTICE / CONTRIBUTING(DCO) / SECURITY / TRADEMARK 追加
- SPDX header を 204 .py に付与

### 同日のもう 1 つの動き — Brief A/B run

- `scripts/run_brief.py` で 4 brief を回したところ、llive が **doing-agent ではなく thinking-evaluator** であることが判明
- 8 件の bug を `docs/BUGS_2026-05-16_brief_ab.md` に記録
- 設計ドラフト `docs/proposals/brief_api_design.md` を作成 (5 日見積)

### Day 4 の教訓

- 9 軸 (KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL) を明示することで責務分離が visible に
- A/B run が **「ここまで動く」「ここから動かない」** の境界を可視化、Brief API 必要性が確定

## Day 5: 2026-05-17 (Fri, 本日) — Brief API + 32 件要件追加

### Brief API end-to-end (LLIVE-001/002)

設計ドラフト (5 日見積) を **1 日で完走**:

- `src/llive/brief/types.py` — Brief / BriefStatus / BriefResult (COG-01 で confidence/assumptions/missing_evidence 追加)
- `src/llive/brief/loader.py` — YAML loader (unknown-key reject)
- `src/llive/brief/ledger.py` — append-only JSONL + `trace_graph()` (COG-03)
- `src/llive/brief/runner.py` — 7 段パイプライン (Stimulus 変換 / loop / approval / tool 実行 / outcome)
- `src/llive/brief/grounding.py` — BriefGrounder (TRIZ × RAD citation, S1)
- `src/llive/brief/governance.py` — GovernanceScorer (4 軸 scoring, COG-02)
- `src/llive/cli/main.py` — `llive brief submit|ledger`
- `src/llive/mcp/tools.py` — `submit_brief` MCP tool
- テスト 46 → 78 件追加

### 要件追加 32 件

| グループ | 件数 | 内容 |
|---|---|---|
| v0.7-vertical MATH | 8 | SI 単位次元解析 / 内蔵計算エンジン / Sympy 検算 / CODATA 辞書 / 等 |
| v0.8 CABT | 7 | Cognitive-aware Transformer Block (forward hook で attention bias) |
| v0.9 CREAT | 5 | KJ法 / MindMap / Six Hats / Synectics / 構造化変換 |
| v1.0-frame COG-FX | 4 | Triple Output / Governance Scoring / Trace Graph / Role-based Agents |
| v2.0-core ORG-FX | 8 | Qwen 依存からの 5 段階離脱 + 補完戦略 |

### 実装したもの

- **MATH-01** SI 7 基本単位次元解析 + 派生単位 (N/J/W/Pa/Hz/C/V/ohm)
- **MATH-08** SafeCalculator (AST visitor + whitelist 28 関数 + 0 除算検出)
- **COG-01** Triple Output (confidence / assumptions / missing_evidence)
- **COG-02** Governance Scoring (usefulness/feasibility/safety/traceability の 4 軸)
- **COG-03** Trace Graph (evidence_chain / tool_chain / decision_chain の 3 層 view)

### ベンチマーク 4 種

| 種類 | セル数 | 主要観察 |
|---|---|---|
| progressive matrix | 5×3=15 | overhead < 1 %、decision 全 note |
| fair re-bench (誤算定→修正) | 24 | llive (LLM attached) は ollama 直叩きの 2-4 倍遅い |
| quiz Debug | 10 | passed 6/10、ms mean 22.3s |
| quiz Release | 10 | passed 7/10、ms mean 22.8s、Debug overhead +1.8% |

### Honest disclosure 事件

- 最初の bench で llive 4/4 OK 134-184ms という「変に速い」結果
- ユーザー指摘「変に高速ですね、何かおかしくないですか?」
- 調査 → LLMBackend 未 attach + chars 指標が JSON 全長 + 134-184ms は subprocess RTT 起因
- 修正版で再走 → llive 32-51s (ollama 直叩きの 2-4 倍遅い) と正直に開示
- 教訓を memory `feedback_benchmark_honest_disclosure.md` に保存

### 公開記事 11 本 + 統合 2 本

- 01-03: Brief API / 10 思考因子 / 数学 vertical
- 04-06: 設計予告 (CABT / CREAT / MATH-02)
- 07-08: bench (fair / quiz)
- 09-11: 構造独自性 / Qwen 離脱 / Qwen 補完
- QIITA_SUMMARY: 技術者向け統合 (694 行)
- QIITA_GENERAL: 非エンジニア向け統合 (255 行)
- 本記事 (12): 開発履歴

### Day 5 の設計判断

- Brief API は **frozen dataclass + append-only JSONL ledger** で replay 可能性を最優先
- LLM コアは依然 frozen、CABT は forward hook で **重み凍結のまま** attention に bias
- 「ベンチで自社が速かったら疑う」を memory に確立
- 「毎日色んな側面で記事を書く」「Qiita tags はスペース区切り + 5 件以内」「非エンジニア向け版も作る」「開発履歴も書く」を運用ルールに

### Day 5 の教訓

- **Honest disclosure が研究の信頼を支える** — 速い数字が出ても疑う
- **多側面で書くと自分の理解も深まる** — 技術 / 戦略 / 哲学 / 業務応用 を並行で書く
- **「ベンチで勝つ」より「ベンチで何を測っているか把握」** が大事

## 5 日間の累積メトリクス

| メトリクス | Day 1 開始 | Day 5 終了 (本日) | 倍率 |
|---|---|---|---|
| テスト数 | 0 | 1014 PASS | — |
| バージョン | (未) | v0.6.0 + v0.7 候補 | — |
| 要件 (FR) | 0 | 100 | — |
| RAD 分野 | 0 | 49 (raptor 共有) | — |
| Phase | 0/4 | 4/4 完了 + Phase 5-12 計画 | — |
| LoC (推定) | 0 | ~30 000 (テスト含む) | — |
| 公開記事 | 0 | 12 本 + 統合 2 本 | — |
| GitHub repo | 0 | 4 (llive + llmesh + llove + fullsense) | — |
| PyPI 公開 | 0 | 6 versions (v0.1.0 〜 v0.5.0 + suite) | — |

## これから (2026-05-18 以降の予想)

### 短期 (~2 週間)

- MATH-02 Sympy 検算 + EVO-04 数式版
- MATH-05 CODATA 辞書を RAD metrology に append
- S2 CABT-01 HFAdapter forward hook prototype
- 数学・物理 quiz set v2 (現状の v1 を拡張、N≥30)

### 中期 (~3 ヶ月)

- CREAT-01 KJ法ノード + clustering
- CABT-02 Stage-aware Block Routing prototype
- Brief API を lldesign / lltrade に組み込み、実 use case 駆動で改善
- credential 復旧後の 6-model full matrix benchmark

### 長期 (~1 年)

- ORG-FX Stage B (LoRA で llive 用 adapter)
- ORG-FX Stage C (qwen2.5:14b → llive-7b 蒸留)
- llove TUI Creative Workbench
- llmesh-suite v1.0 (4 製品統合インストーラ)

## 5 日間で確立した「llive 哲学」

- **frozen LLM コア + 可変周辺** = replay 可能性を最優先
- **append-only ledger** = 何が起きたか全部後から見える
- **HITL を architecture level に** = Approval Bus は飾りではなく中核
- **TRIZ を mutation policy に内蔵** = 創造性を構造に持ち込む
- **on-prem only** = Local 環境こそ AI の本来の居場所 (feedback_llive_measurement_purity)
- **honest disclosure** = 失敗を消さない、教訓を memory に残す
- **多側面で書く** = 技術 / 戦略 / 哲学 / 業務応用を毎日並行で発信

## 関連ドキュメント

- llive リポジトリ: <https://github.com/furuse-kazufumi/llive>
- llive CHANGELOG: <https://github.com/furuse-kazufumi/llive/blob/main/CHANGELOG.md>
- llive PROGRESS.md: <https://github.com/furuse-kazufumi/llive/blob/main/docs/PROGRESS.md>
- fullsense ポータル: <https://github.com/furuse-kazufumi/fullsense>
- 同日記事:
  - [QIITA_SUMMARY](./QIITA_SUMMARY.md) — 技術者向け統合
  - [QIITA_GENERAL](./QIITA_GENERAL.md) — 非エンジニア向け統合
  - [01〜11 個別記事](./README.md)

## 残った問い — 「5 日で 21 倍」は速さなのか

この 5 日でテストは 49 → 1014、1 日 1 バージョン以上のペースで進んだ。だが速さそのものは自慢にならない。問いは別のところにある——**なぜ個人 1 人 + AI で、このペースが成り立ったのか**。手が速いからではない。Day 1 で固めた設計の核が崩れなかったからでもない。実は、自分でも開発中に言葉にできていなかった「観点を先回りして補う何か」が背後で効いていた、という仮説が残っている。

次回 **#13「[コーパス先行戦略 — AI が私の気づかない観点を思考フローに補完する](./QIITA_#13_corpus_first_advantage.md)」** では、その正体を解剖する。21 分野 4.9 万件の RAD コーパスを先に積んでおくと、AI が私の盲点を埋める形で協働が回る——この「5 日で進めた」ペースの裏側にあった協働構造を、開発履歴の数字から一歩踏み込んで言語化していく。

---

> 5 日で v0.1 → v0.7 候補。1 日 1 バージョン以上のペースで進めながら、その都度
> honest disclosure を残す。AI と一緒に開発する時代の研究記録として残します。

---

# English

# llive Development History — From v0.1 to a v0.7 Candidate in 5 Days

> 📚 **Series nav**: ← #11 [llive complementing Qwen (filling the gaps)](./QIITA_#11_complementary_with_qwen.md) ｜ **#12 this article** (a chronological look back at the 5 days) ｜ #13 [The corpus-first strategy (why we moved so fast in 5 days)](./QIITA_#13_corpus_first_advantage.md) → . Each article also reads on its own.
>
> Up through #11 the focus was on the **substance of llive's design** (complementing Qwen, structural originality). This article pulls back for a moment to look at **in what order, and how, that design was stacked up** — a chronological retrospective over 5 days.

Author: **Kazufumi Furuse (Puruyan)**

## Why Keep a Development History

llive is a self-evolving LLM framework launched on 2026-05-13. This article is a chronological summary of **what we built and how, where we got stuck, and what we learned over the 5 days from launch to today (2026-05-17)**.

- Record the reasons behind design decisions
- Keep failures honestly on the record (the `feedback_benchmark_honest_disclosure` lesson)
- Maintain a state where "why it is the way it is" can be understood later
- So that my future self (and Claude Opus 4.7 via ccr) can read the context the next day onward

## The 5 Days in Ultra-Brief

| Day | Date | Version | Keyword |
|---|---|---|---|
| 1 | 2026-05-13 | v0.1.0 | Project launch + Phase 1 MVR completed |
| 2 | 2026-05-13 | v0.2.0 | Phase 2 Adaptive Modular System |
| 3 | 2026-05-14 | v0.3.0 → v0.5.0 | Phase 3 (Evolve) + Phase 4 (Security) + Phase 5 (Rust) |
| 4 | 2026-05-16 | v0.6.0 | 9 axes skeleton + Apache 2.0 + FullSense umbrella |
| 5 | 2026-05-17 | v0.7 candidate (today) | Brief API + COG-FX + MATH + ORG-FX turned into requirements |

In 5 days the test count went from 49 → 1014 (about 21×), and the code grew from an MVR to 9 axes + 32 v0.7+ requirements.

## Day 1: 2026-05-13 (Tue) — Launch and Phase 1 MVR

### Background of the Launch

Already holding two products — llmesh (secure LLM hub) and llove (TUI dashboard) — the decision was to build a third member: a **"self-evolving modular-memory LLM framework."** The naming is unified as four-letter words starting with `l` (llmesh / llove / llive).

### The Design Core (established on Day 1, unchanged to this day)

1. Fixed Decoder-only LLM core + variable periphery to absorb capabilities
2. Separation of responsibilities across 4 memory layers (semantic / episodic / structural / parameter)
3. Declarative structure description (YAML)
4. Reviewed self-evolution (promotion only via online restriction + offline review)
5. Biological memory model (hippocampus-cortex consolidation cycle)
6. Promotion with formal verification (Lean / Z3 / TLA+)
7. llmesh / llove family integration
8. Built-in TRIZ (40 principles + contradiction matrix)

### v0.1.0 Release

- Initialized with GSD `/gsd-new-project` → generated PROJECT.md / REQUIREMENTS.md (46 reqs) / ROADMAP.md (4 phases) / STATE.md / config.json
- src/llive/ 8 layers: schema / core / container / memory / router / evolution / observability / triz
- 49 tests pass / 82% coverage
- CLI: `llive run --template specs/templates/qwen2_5_0_5b.yaml --prompt "..." --mock`
- Design decision: faiss / torch / sentence-transformers are **optional extras**, and Phase 1 tests run on a numpy + hash embedding fallback

### Lessons

- Optional extras design is essential for keeping both Windows and CI working
- With the GSD workflow (`--auto` mode), Phase 1 can be completed in a single day

## Day 2: 2026-05-13 (Tue night) — Phase 2 Adaptive

### v0.2.0 Release

- Added structural memory (graph) + parameter memory (adapter store)
- The Bayesian Surprise Gate (FR-21) makes the memory-write threshold dynamic
- The consolidation cycle runs as a nightly batch
- Route trace + memory link viz in the llove TUI
- LLM Wiki integration (LLW-04)
- Achieved BWT ≥ -1% over 5 consecutive task learnings
- **308 tests / 99% coverage / 0 lint**

### Design Decisions

- Write control as "Bayesian surprise" → more flexible than a plain threshold
- Inserted a **phase transition** (short → mid → long → archived → erased) between the 4 memory layers to manage their life cycle

## Day 3: 2026-05-14 (Wed) — A Large Autonomous Session

From here, three versions (v0.3 → v0.4 → v0.5) were advanced in a single day.

### v0.3.0 — Phase 3 (Controlled Self-Evolution) + Phase 4 (Production Security) released together

Phase 3 (Evolve):
- EVO-04 Z3 static verification
- EVO-06 Failed Reservoir (DuckDB order-preserving)
- EVO-07 Reverse-Evo Monitor (JSONL audit)
- TRIZ-02 Contradiction Detector
- TRIZ-03 Principle Mapper (39×39 matrix)
- TRIZ-04 RAD-Backed Idea Generator (pluggable IdeaLLM Protocol)
- TRIZ-07 Self-Reflection Session
- LLW-04 Wiki Contradiction
- LLW-05 Wiki diff ChangeOp

Phase 4 (Security):
- SEC-01 Quarantined Memory Zone
- SEC-02 Ed25519 Signed Adapter
- SEC-03 SHA-256 audit hash chain (stdlib sqlite3 only)

**429 tests / 98% coverage / 0 lint**

### v0.4.0 — Phase 5 Rust skeleton

- `crates/llive_rust_ext/` PyO3 0.22 + maturin scaffold
- RUST-01 (skeleton) / RUST-02 (compute_surprise baseline) / RUST-04 (jaccard baseline) / RUST-13 (Hypothesis parity 1e-6)
- `llive.rust_ext.HAS_RUST` flag + Python fallback
- 439 tests pass

### v0.5.0 — Phase 5 wire-in

- RUST-03 (bulk_time_decay) Rust kernel + Python wrapper + 5 parity tests
- BayesianSurpriseGate.compute_surprise delegates automatically when rust_ext.HAS_RUST (numpy fallback)
- EdgeWeightUpdater.apply_time_decay does a 1-pass precompute via rust_ext.bulk_time_decay
- **444 tests / 98% coverage / 0 lint**

### Design Decisions on Day 3

- **Rust porting happens after the semantics are fixed**, done incrementally (with a 5× performance-improvement gate)
- All RUST-XX extensions **must have a Python fallback**, keeping operation alive even in Rust-absent environments
- The remaining RUST-02 rayon / 05 jsonschema-rs / 06 crossbeam / 07 ChangeOp / 08 hora HNSW / 09 tokio async / 10 phf TRIZ / 11 Z3 bridge are deferred until v0.7

### Lessons on Day 3

- To advance three versions in a single day, **core design** and **optional extras design** are essential
- Make the gate explicit: "adopt if the bench shows 5×, otherwise revert"

## Day 4: 2026-05-16 (Thu) — 9 axes + Apache 2.0 + FullSense umbrella

### v0.6.0 Release

- **9 axes skeleton** completed — KAR / DTKR / APO / ICP / TLB / Math / PM / RPAR / SIL
- C-1 Approval Bus made production-grade (Policy + SQLite Ledger)
- C-2 `@govern` + ProductionOutputBus (Policy gate × side-effect emit)
- C-3 Cross-substrate migration spike (§MI1)
- C-14 ICP IdleCollaborator MVP (querying a peer LLM while idle)
- **970 PASS / 0 lint**

### Legal and Branding Work

- Switched to **Apache-2.0 + Commercial dual-license**
- Introduced the **FullSense umbrella brand** (parent of llmesh / llive / llove)
- Added NOTICE / CONTRIBUTING(DCO) / SECURITY / TRADEMARK
- Applied SPDX headers to 204 .py files

### Another Move the Same Day — Brief A/B run

- Running 4 briefs with `scripts/run_brief.py` revealed that llive is **a thinking-evaluator, not a doing-agent**
- Recorded 8 bugs in `docs/BUGS_2026-05-16_brief_ab.md`
- Created the design draft `docs/proposals/brief_api_design.md` (estimated 5 days)

### Lessons on Day 4

- Making the 9 axes (KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL) explicit makes the separation of responsibilities visible
- The A/B run visualized the boundary of **"works up to here" / "stops working from here"**, confirming the need for the Brief API

## Day 5: 2026-05-17 (Fri, today) — Brief API + 32 added requirements

### Brief API end-to-end (LLIVE-001/002)

The design draft (estimated at 5 days) was **completed in a single day**:

- `src/llive/brief/types.py` — Brief / BriefStatus / BriefResult (confidence/assumptions/missing_evidence added in COG-01)
- `src/llive/brief/loader.py` — YAML loader (unknown-key reject)
- `src/llive/brief/ledger.py` — append-only JSONL + `trace_graph()` (COG-03)
- `src/llive/brief/runner.py` — 7-stage pipeline (Stimulus conversion / loop / approval / tool execution / outcome)
- `src/llive/brief/grounding.py` — BriefGrounder (TRIZ × RAD citation, S1)
- `src/llive/brief/governance.py` — GovernanceScorer (4-axis scoring, COG-02)
- `src/llive/cli/main.py` — `llive brief submit|ledger`
- `src/llive/mcp/tools.py` — `submit_brief` MCP tool
- 46 → 78 tests added

### 32 Added Requirements

| Group | Count | Content |
|---|---|---|
| v0.7-vertical MATH | 8 | SI unit dimensional analysis / built-in calculation engine / Sympy verification / CODATA dictionary / etc. |
| v0.8 CABT | 7 | Cognitive-aware Transformer Block (attention bias via forward hook) |
| v0.9 CREAT | 5 | KJ method / MindMap / Six Hats / Synectics / structured transformation |
| v1.0-frame COG-FX | 4 | Triple Output / Governance Scoring / Trace Graph / Role-based Agents |
| v2.0-core ORG-FX | 8 | 5-stage departure from Qwen dependence + complementary strategy |

### What Was Implemented

- **MATH-01** SI 7-base-unit dimensional analysis + derived units (N/J/W/Pa/Hz/C/V/ohm)
- **MATH-08** SafeCalculator (AST visitor + whitelist of 28 functions + division-by-zero detection)
- **COG-01** Triple Output (confidence / assumptions / missing_evidence)
- **COG-02** Governance Scoring (4 axes: usefulness/feasibility/safety/traceability)
- **COG-03** Trace Graph (3-layer view: evidence_chain / tool_chain / decision_chain)

### Four Kinds of Benchmark

| Type | Cells | Key observation |
|---|---|---|
| progressive matrix | 5×3=15 | overhead < 1 %, decision noted for all |
| fair re-bench (miscalculation → fixed) | 24 | llive (LLM attached) is 2-4× slower than calling ollama directly |
| quiz Debug | 10 | passed 6/10, ms mean 22.3s |
| quiz Release | 10 | passed 7/10, ms mean 22.8s, Debug overhead +1.8% |

### The Honest Disclosure Incident

- The first bench gave a "suspiciously fast" result of llive 4/4 OK at 134-184ms
- The user pointed out, "That's suspiciously fast — isn't something off?"
- Investigation → LLMBackend not attached + the chars metric was the full JSON length + the 134-184ms came from subprocess RTT
- Re-ran a fixed version → honestly disclosed llive at 32-51s (2-4× slower than calling ollama directly)
- Saved the lesson in the memory `feedback_benchmark_honest_disclosure.md`

### 11 Published Articles + 2 Integrated Ones

- 01-03: Brief API / 10 thinking factors / math vertical
- 04-06: design previews (CABT / CREAT / MATH-02)
- 07-08: bench (fair / quiz)
- 09-11: structural originality / Qwen departure / Qwen complement
- QIITA_SUMMARY: integrated for engineers (694 lines)
- QIITA_GENERAL: integrated for non-engineers (255 lines)
- This article (12): development history

### Design Decisions on Day 5

- The Brief API prioritizes replayability above all with a **frozen dataclass + append-only JSONL ledger**
- The LLM core remains frozen; CABT biases attention via a forward hook **with weights still frozen**
- Established "be suspicious if your own bench is fast" in memory
- Made into operational rules: "write articles from various angles every day," "Qiita tags are space-separated and within 5," "also make a non-engineer version," "also write a development history"

### Lessons on Day 5

- **Honest disclosure underpins the trust of the research** — be suspicious even when fast numbers come up
- **Writing from multiple angles deepens your own understanding** — write tech / strategy / philosophy / business applications in parallel
- **"Grasping what the bench measures" matters more than "winning the bench"**

## Cumulative Metrics Over the 5 Days

| Metric | Day 1 start | Day 5 end (today) | Ratio |
|---|---|---|---|
| Test count | 0 | 1014 PASS | — |
| Version | (none) | v0.6.0 + v0.7 candidate | — |
| Requirements (FR) | 0 | 100 | — |
| RAD fields | 0 | 49 (shared with raptor) | — |
| Phase | 0/4 | 4/4 done + Phase 5-12 planned | — |
| LoC (estimated) | 0 | ~30,000 (including tests) | — |
| Published articles | 0 | 12 + 2 integrated | — |
| GitHub repos | 0 | 4 (llive + llmesh + llove + fullsense) | — |
| PyPI releases | 0 | 6 versions (v0.1.0 to v0.5.0 + suite) | — |

## What Comes Next (expectations from 2026-05-18 onward)

### Short term (~2 weeks)

- MATH-02 Sympy verification + the formula version of EVO-04
- MATH-05 append the CODATA dictionary to RAD metrology
- S2 CABT-01 HFAdapter forward hook prototype
- Math/physics quiz set v2 (expanding the current v1, N≥30)

### Mid term (~3 months)

- CREAT-01 KJ-method nodes + clustering
- CABT-02 Stage-aware Block Routing prototype
- Embed the Brief API into lldesign / lltrade, improving it driven by real use cases
- The 6-model full matrix benchmark after credential recovery

### Long term (~1 year)

- ORG-FX Stage B (a llive adapter via LoRA)
- ORG-FX Stage C (distillation from qwen2.5:14b → llive-7b)
- llove TUI Creative Workbench
- llmesh-suite v1.0 (a 4-product integrated installer)

## The "llive Philosophy" Established Over 5 Days

- **Frozen LLM core + variable periphery** = replayability above all
- **Append-only ledger** = everything that happened is visible afterward
- **HITL at the architecture level** = the Approval Bus is core, not decoration
- **TRIZ built into the mutation policy** = bring creativity into structure
- **on-prem only** = the local environment is AI's true home (feedback_llive_measurement_purity)
- **Honest disclosure** = don't erase failures, leave lessons in memory
- **Write from multiple angles** = broadcast tech / strategy / philosophy / business applications in parallel every day

## Related Documents

- llive repository: <https://github.com/furuse-kazufumi/llive>
- llive CHANGELOG: <https://github.com/furuse-kazufumi/llive/blob/main/CHANGELOG.md>
- llive PROGRESS.md: <https://github.com/furuse-kazufumi/llive/blob/main/docs/PROGRESS.md>
- fullsense portal: <https://github.com/furuse-kazufumi/fullsense>
- Same-day articles:
  - [QIITA_SUMMARY](./QIITA_SUMMARY.md) — integrated for engineers
  - [QIITA_GENERAL](./QIITA_GENERAL.md) — integrated for non-engineers
  - [01–11 individual articles](./README.md)

## An Open Question — Is "21× in 5 Days" Really About Speed?

Over these 5 days the test count went 49 → 1014, advancing at more than one version per day. But speed itself is nothing to boast about. The real question lies elsewhere — **why did this pace hold for a single person plus AI?** Not because the hands were fast. Not only because the design core fixed on Day 1 never broke. A hypothesis remains: something that "anticipates and fills in perspectives," which I couldn't even put into words during development, was quietly working in the background.

In the next article, **#13 "[The corpus-first strategy — how AI complements the perspectives I miss in my thinking flow](./QIITA_#13_corpus_first_advantage.md)"**, I dissect what that something is. Stack a 49,000-document RAD corpus across 21 fields up front, and collaboration starts to flow in a way where the AI fills my blind spots — I'll step beyond the development-history numbers and put into words the collaborative structure behind this "5-day" pace.

---

> From v0.1 → v0.7 candidate in 5 days. Advancing at a pace of more than one version per day,
> while leaving honest disclosure each time. We keep it as a research record of an era of developing alongside AI.

---

# 中文

# llive 开发历程 — 5 天内从 v0.1 到 v0.7 候选版

> 📚 **连载导航**: ← #11 [与 Qwen 相互补充的 llive（填补“隙间”的设计）](./QIITA_#11_complementary_with_qwen.md) ｜ **#12 本文**（按时间顺序回顾这 5 天的开发历程）｜ #13 [语料先行战略（为什么能在 5 天里推进）](./QIITA_#13_corpus_first_advantage.md) → 。※ 各篇均可独立阅读。
>
> 到 #11 为止，关注的是 llive **设计的内容**（与 Qwen 的互补、结构的独创性）。本文先把视角拉远一下，看一看那套设计是**以怎样的顺序、如何一层层垒起来的**——一份横跨 5 天的时间顺序回顾。

作者：**古濑和文（Puruyan）**

## 为什么要留下开发历程

llive 是于 2026-05-13 启动的自进化型 LLM 框架。本文按时间顺序总结了**从启动到今天（2026-05-17）的这 5 天里，做了什么、怎么做的、在哪里卡住、学到了什么**。

- 记录设计判断的理由
- 诚实地保留失败记录（`feedback_benchmark_honest_disclosure` 的教训）
- 保持一种事后能够理解“为什么会是这样”的状态
- 让次日之后的自己（以及经由 ccr 的 Claude Opus 4.7）能够读懂上下文

## 5 天的超级概要

| Day | 日期 | 版本 | 关键词 |
|---|---|---|---|
| 1 | 2026-05-13 | v0.1.0 | 项目启动 + Phase 1 MVR 完成 |
| 2 | 2026-05-13 | v0.2.0 | Phase 2 Adaptive Modular System |
| 3 | 2026-05-14 | v0.3.0 → v0.5.0 | Phase 3 (Evolve) + Phase 4 (Security) + Phase 5 (Rust) |
| 4 | 2026-05-16 | v0.6.0 | 9 axes skeleton + Apache 2.0 + FullSense umbrella |
| 5 | 2026-05-17 | v0.7 候选版（今天） | Brief API + COG-FX + MATH + ORG-FX 转化为需求 |

5 天里测试数从 49 → 1014（约 21 倍），代码从 MVR 增长到 9 个轴 + 32 项 v0.7+ 需求。

## Day 1：2026-05-13（周二）— 启动与 Phase 1 MVR

### 启动的背景

在已经拥有 llmesh（secure LLM hub）与 llove（TUI dashboard）这两个产品的状态下，决定打造第三个成员：一个**“自进化型模块化记忆 LLM 框架”**。命名统一为以 `l` 开头的四字母词（llmesh / llove / llive）。

### 设计的核心（Day 1 确立，至今不变）

1. 固定的 Decoder-only LLM 核心 + 可变的外围以吸收能力
2. 4 层记忆（semantic / episodic / structural / parameter）的职责分离
3. 声明式结构描述（YAML）
4. 带审查的自进化（仅经由在线限制 + 离线审查才能晋升）
5. 生物学记忆模型（海马-皮质 consolidation cycle）
6. 带形式化验证的 promotion（Lean / Z3 / TLA+）
7. llmesh / llove 家族整合
8. 内置 TRIZ（40 原理 + 矛盾矩阵）

### v0.1.0 发布

- 用 GSD `/gsd-new-project` 初始化 → 生成 PROJECT.md / REQUIREMENTS.md (46 reqs) / ROADMAP.md (4 phases) / STATE.md / config.json
- src/llive/ 8 层：schema / core / container / memory / router / evolution / observability / triz
- 49 tests pass / 82% coverage
- CLI: `llive run --template specs/templates/qwen2_5_0_5b.yaml --prompt "..." --mock`
- 设计判断：faiss / torch / sentence-transformers 设为 **optional extras**，Phase 1 测试以 numpy + hash 嵌入 fallback 运行

### 教训

- Optional extras 设计对于同时兼顾 Windows 与 CI 是必不可少的
- 借助 GSD 工作流（`--auto` 模式），Phase 1 可以在一天内完成

## Day 2：2026-05-13（周二夜）— Phase 2 Adaptive

### v0.2.0 发布

- 增加 structural memory（graph）+ parameter memory（adapter store）
- Bayesian Surprise Gate（FR-21）使记忆写入阈值动态化
- Consolidation 周期作为夜间 batch 运行
- 在 llove TUI 中实现 route trace + memory link viz
- LLM Wiki 整合（LLW-04）
- 在连续 5 项任务学习中达成 BWT ≥ -1%
- **308 tests / 99% coverage / 0 lint**

### 设计判断

- 以 “Bayesian surprise” 进行写入控制 → 比单纯阈值更灵活
- 在 4 层记忆之间加入 **phase transition**（short → mid → long → archived → erased）来管理生命周期

## Day 3：2026-05-14（周三）— 大规模自主会话

从这里开始，一天内推进了三个版本（v0.3 → v0.4 → v0.5）。

### v0.3.0 — Phase 3 (Controlled Self-Evolution) + Phase 4 (Production Security) 同时发布

Phase 3 (Evolve):
- EVO-04 Z3 静态验证
- EVO-06 Failed Reservoir（DuckDB 保持顺序）
- EVO-07 Reverse-Evo Monitor（JSONL audit）
- TRIZ-02 Contradiction Detector
- TRIZ-03 Principle Mapper（39×39 matrix）
- TRIZ-04 RAD-Backed Idea Generator（可插拔 IdeaLLM Protocol）
- TRIZ-07 Self-Reflection Session
- LLW-04 Wiki Contradiction
- LLW-05 Wiki diff ChangeOp

Phase 4 (Security):
- SEC-01 Quarantined Memory Zone
- SEC-02 Ed25519 Signed Adapter
- SEC-03 SHA-256 audit hash chain（仅 stdlib sqlite3）

**429 tests / 98% coverage / 0 lint**

### v0.4.0 — Phase 5 Rust skeleton

- `crates/llive_rust_ext/` PyO3 0.22 + maturin scaffold
- RUST-01 (skeleton) / RUST-02 (compute_surprise baseline) / RUST-04 (jaccard baseline) / RUST-13 (Hypothesis parity 1e-6)
- `llive.rust_ext.HAS_RUST` flag + Python fallback
- 439 tests pass

### v0.5.0 — Phase 5 wire-in

- RUST-03 (bulk_time_decay) Rust kernel + Python wrapper + 5 parity tests
- 当 rust_ext.HAS_RUST 时，BayesianSurpriseGate.compute_surprise 自动委派（numpy fallback）
- EdgeWeightUpdater.apply_time_decay 通过 rust_ext.bulk_time_decay 进行 1 pass precompute
- **444 tests / 98% coverage / 0 lint**

### Day 3 的设计判断

- **Rust 移植在语义固定之后** 分阶段进行（设置 5x 性能提升 gate）
- 所有 RUST-XX 扩展 **必须有 Python fallback**，在 Rust 不存在的环境中也维持运行
- 余下的 RUST-02 rayon / 05 jsonschema-rs / 06 crossbeam / 07 ChangeOp / 08 hora HNSW / 09 tokio async / 10 phf TRIZ / 11 Z3 bridge 延后到 v0.7

### Day 3 的教训

- 要在一天内推进三个版本，**核心设计** 与 **Optional extras 设计** 是必不可少的
- 明示这个 gate：“bench 出 5x 就采用，否则 revert”

## Day 4：2026-05-16（周四）— 9 axes + Apache 2.0 + FullSense umbrella

### v0.6.0 发布

- **9 axes skeleton** 完成 — KAR / DTKR / APO / ICP / TLB / Math / PM / RPAR / SIL
- C-1 Approval Bus 生产化（Policy + SQLite Ledger）
- C-2 `@govern` + ProductionOutputBus（Policy gate × 副作用 emit）
- C-3 Cross-substrate migration spike（§MI1）
- C-14 ICP IdleCollaborator MVP（idle 期间向 peer LLM 询问）
- **970 PASS / 0 lint**

### 法务与品牌整备

- 切换为 **Apache-2.0 + Commercial dual-license**
- 引入 **FullSense umbrella 品牌**（llmesh / llive / llove 的母品牌）
- 增加 NOTICE / CONTRIBUTING(DCO) / SECURITY / TRADEMARK
- 为 204 个 .py 添加 SPDX header

### 同一天的另一项动作 — Brief A/B run

- 用 `scripts/run_brief.py` 跑了 4 个 brief，发现 llive **是 thinking-evaluator 而非 doing-agent**
- 将 8 个 bug 记录在 `docs/BUGS_2026-05-16_brief_ab.md`
- 创建设计草案 `docs/proposals/brief_api_design.md`（估算 5 天）

### Day 4 的教训

- 明示 9 个轴（KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL）使职责分离变得可见
- A/B run 把 **“到这里能动”“从这里不能动”** 的边界可视化，确定了 Brief API 的必要性

## Day 5：2026-05-17（周五，今天）— Brief API + 追加 32 项需求

### Brief API end-to-end (LLIVE-001/002)

设计草案（估算 5 天）**在一天内完成**：

- `src/llive/brief/types.py` — Brief / BriefStatus / BriefResult（COG-01 中增加 confidence/assumptions/missing_evidence）
- `src/llive/brief/loader.py` — YAML loader（unknown-key reject）
- `src/llive/brief/ledger.py` — append-only JSONL + `trace_graph()`（COG-03）
- `src/llive/brief/runner.py` — 7 段 pipeline（Stimulus 转换 / loop / approval / tool 执行 / outcome）
- `src/llive/brief/grounding.py` — BriefGrounder（TRIZ × RAD citation, S1）
- `src/llive/brief/governance.py` — GovernanceScorer（4 轴 scoring, COG-02）
- `src/llive/cli/main.py` — `llive brief submit|ledger`
- `src/llive/mcp/tools.py` — `submit_brief` MCP tool
- 测试 46 → 78 项追加

### 追加需求 32 项

| 分组 | 件数 | 内容 |
|---|---|---|
| v0.7-vertical MATH | 8 | SI 单位量纲分析 / 内置计算引擎 / Sympy 验算 / CODATA 词典 / 等 |
| v0.8 CABT | 7 | Cognitive-aware Transformer Block（用 forward hook 实现 attention bias） |
| v0.9 CREAT | 5 | KJ 法 / MindMap / Six Hats / Synectics / 结构化变换 |
| v1.0-frame COG-FX | 4 | Triple Output / Governance Scoring / Trace Graph / Role-based Agents |
| v2.0-core ORG-FX | 8 | 从 Qwen 依赖中的 5 阶段脱离 + 补充策略 |

### 实现的内容

- **MATH-01** SI 7 个基本单位量纲分析 + 派生单位（N/J/W/Pa/Hz/C/V/ohm）
- **MATH-08** SafeCalculator（AST visitor + whitelist 28 函数 + 除零检测）
- **COG-01** Triple Output（confidence / assumptions / missing_evidence）
- **COG-02** Governance Scoring（usefulness/feasibility/safety/traceability 的 4 个轴）
- **COG-03** Trace Graph（evidence_chain / tool_chain / decision_chain 的 3 层 view）

### 4 种基准测试

| 种类 | 单元数 | 主要观察 |
|---|---|---|
| progressive matrix | 5×3=15 | overhead < 1 %，decision 全部记录 |
| fair re-bench（误算定→修正） | 24 | llive (LLM attached) 比直接调用 ollama 慢 2-4 倍 |
| quiz Debug | 10 | passed 6/10，ms mean 22.3s |
| quiz Release | 10 | passed 7/10，ms mean 22.8s，Debug overhead +1.8% |

### Honest disclosure 事件

- 最初的 bench 给出了 llive 4/4 OK 134-184ms 这种“奇怪地快”的结果
- 用户指出“奇怪地快啊，是不是哪里有问题？”
- 调查 → LLMBackend 未 attach + chars 指标是 JSON 全长 + 134-184ms 源自 subprocess RTT
- 修正版再跑 → 诚实地披露 llive 32-51s（比直接调用 ollama 慢 2-4 倍）
- 把教训保存到 memory `feedback_benchmark_honest_disclosure.md`

### 公开文章 11 篇 + 整合 2 篇

- 01-03：Brief API / 10 思考因子 / 数学 vertical
- 04-06：设计预告（CABT / CREAT / MATH-02）
- 07-08：bench（fair / quiz）
- 09-11：结构独创性 / Qwen 脱离 / Qwen 补充
- QIITA_SUMMARY：面向技术者的整合（694 行）
- QIITA_GENERAL：面向非工程师的整合（255 行）
- 本文（12）：开发历程

### Day 5 的设计判断

- Brief API 以 **frozen dataclass + append-only JSONL ledger** 将可重放性放在最优先
- LLM 核心依然 frozen，CABT 通过 forward hook 在 **权重冻结的状态下** 为 attention 加 bias
- 在 memory 中确立“自家 bench 快就要怀疑”
- 将以下确立为运营规则：“每天从各种侧面写文章”“Qiita tags 用空格分隔且不超过 5 个”“也做面向非工程师的版本”“也写开发历程”

### Day 5 的教训

- **Honest disclosure 支撑着研究的信任** — 即使出了快的数字也要怀疑
- **从多个侧面书写会加深自己的理解** — 并行地写技术 / 战略 / 哲学 / 业务应用
- **比起“在 bench 中获胜”，“把握 bench 在测什么”更重要**

## 5 天的累积指标

| 指标 | Day 1 开始 | Day 5 结束（今天） | 倍率 |
|---|---|---|---|
| 测试数 | 0 | 1014 PASS | — |
| 版本 | （无） | v0.6.0 + v0.7 候选版 | — |
| 需求 (FR) | 0 | 100 | — |
| RAD 分野 | 0 | 49（与 raptor 共享） | — |
| Phase | 0/4 | 4/4 完成 + Phase 5-12 计划 | — |
| LoC（推定） | 0 | ~30 000（含测试） | — |
| 公开文章 | 0 | 12 篇 + 整合 2 篇 | — |
| GitHub repo | 0 | 4（llive + llmesh + llove + fullsense） | — |
| PyPI 公开 | 0 | 6 versions（v0.1.0 〜 v0.5.0 + suite） | — |

## 接下来（2026-05-18 之后的预想）

### 短期（~2 周）

- MATH-02 Sympy 验算 + EVO-04 公式版
- MATH-05 将 CODATA 词典 append 到 RAD metrology
- S2 CABT-01 HFAdapter forward hook prototype
- 数学・物理 quiz set v2（扩展当前的 v1，N≥30）

### 中期（~3 个月）

- CREAT-01 KJ 法节点 + clustering
- CABT-02 Stage-aware Block Routing prototype
- 将 Brief API 嵌入 lldesign / lltrade，由真实 use case 驱动改进
- credential 恢复后的 6-model full matrix benchmark

### 长期（~1 年）

- ORG-FX Stage B（用 LoRA 制作 llive 用 adapter）
- ORG-FX Stage C（qwen2.5:14b → llive-7b 蒸馏）
- llove TUI Creative Workbench
- llmesh-suite v1.0（4 产品整合安装器）

## 5 天里确立的“llive 哲学”

- **frozen LLM 核心 + 可变外围** = 将可重放性放在最优先
- **append-only ledger** = 发生了什么事后全部可见
- **HITL 置于 architecture level** = Approval Bus 不是装饰而是核心
- **将 TRIZ 内置于 mutation policy** = 把创造性带入结构
- **on-prem only** = 本地环境才是 AI 真正的归宿（feedback_llive_measurement_purity）
- **honest disclosure** = 不抹去失败，把教训留在 memory
- **从多个侧面书写** = 每天并行地发布技术 / 战略 / 哲学 / 业务应用

## 相关文档

- llive 仓库：<https://github.com/furuse-kazufumi/llive>
- llive CHANGELOG：<https://github.com/furuse-kazufumi/llive/blob/main/CHANGELOG.md>
- llive PROGRESS.md：<https://github.com/furuse-kazufumi/llive/blob/main/docs/PROGRESS.md>
- fullsense 门户：<https://github.com/furuse-kazufumi/fullsense>
- 同日文章：
  - [QIITA_SUMMARY](./QIITA_SUMMARY.md) — 面向技术者的整合
  - [QIITA_GENERAL](./QIITA_GENERAL.md) — 面向非工程师的整合
  - [01〜11 单篇文章](./README.md)

## 留下的问题 — “5 天 21 倍”真的是速度吗

这 5 天里测试数从 49 → 1014，以每天一个以上版本的节奏推进。但速度本身并不值得夸耀。真正的问题在别处——**为什么个人一人 + AI，能撑住这样的节奏？** 不是因为手快。也不只是因为 Day 1 定下的设计核心没有崩。其实还留着一个假设：一种“提前补上视角”的东西，连我自己在开发时都没能用语言说清，却在背后悄悄起着作用。

下一篇 **#13「[语料先行战略 — AI 在我的思考流中补上我没察觉的视角](./QIITA_#13_corpus_first_advantage.md)」** 将解剖这个东西的真面目。先把横跨 21 个领域、4.9 万件的 RAD 语料垒起来，协作便会以 AI 填补我盲点的形式运转起来——我会从开发历程的数字再往前一步，把这“5 天推进”节奏背后的协作结构用语言讲清楚。

---

> 5 天内 v0.1 → v0.7 候选版。以每天一个以上版本的节奏推进，
> 同时每次都留下 honest disclosure。我们将其作为与 AI 一同开发的时代的研究记录留存下来。

---

# 한국어

# llive 개발 이력 — 5일 만에 v0.1에서 v0.7 후보까지

저자: **후루세 가즈후미(Puruyan)**

## 왜 개발 이력을 남기는가

llive는 2026-05-13에 시작한 자기진화형 LLM 프레임워크다. 본 글은 **시작부터 오늘(2026-05-17)까지의 5일간 무엇을 어떻게 만들고, 어디서 막히고, 무엇을 배웠는지**를 시간순으로 정리한 것이다.

- 설계 판단의 이유를 남긴다
- 실패를 정직하게 기록으로 남긴다(`feedback_benchmark_honest_disclosure` 교훈)
- “왜 그렇게 되어 있는가”를 나중에 알 수 있는 상태를 유지한다
- 다음 날 이후의 자신(그리고 ccr 경유 Claude Opus 4.7)이 맥락을 읽을 수 있도록

## 5일간의 초개요

| Day | 날짜 | 버전 | 키워드 |
|---|---|---|---|
| 1 | 2026-05-13 | v0.1.0 | 프로젝트 시작 + Phase 1 MVR 완주 |
| 2 | 2026-05-13 | v0.2.0 | Phase 2 Adaptive Modular System |
| 3 | 2026-05-14 | v0.3.0 → v0.5.0 | Phase 3 (Evolve) + Phase 4 (Security) + Phase 5 (Rust) |
| 4 | 2026-05-16 | v0.6.0 | 9 axes skeleton + Apache 2.0 + FullSense umbrella |
| 5 | 2026-05-17 | v0.7 후보(오늘) | Brief API + COG-FX + MATH + ORG-FX 요건화 |

5일 만에 테스트 수는 49 → 1014(약 21배), 코드는 MVR에서 9개 축 + 32건 v0.7+ 요건까지.

## Day 1: 2026-05-13 (화) — 시작과 Phase 1 MVR

### 시작의 배경

llmesh(secure LLM hub)와 llove(TUI dashboard)라는 두 제품을 이미 가진 상태에서, 세 번째 멤버로서 **“자기진화형 모듈식 기억 LLM 프레임워크”**를 만드는 판단. 명명은 `l`로 시작하는 4글자(llmesh / llove / llive)로 통일.

### 설계의 핵심(Day 1에 확립, 현재까지 불변)

1. 고정 Decoder-only LLM 코어 + 가변 주변으로 능력 흡수
2. 4층 메모리(semantic / episodic / structural / parameter)의 책임 분리
3. 선언적 구조 기술(YAML)
4. 심사를 거친 자기진화(온라인 제한 + 오프라인 심사를 통해서만 승격)
5. 생물학적 기억 모델(해마-피질 consolidation cycle)
6. 형식 검증을 포함한 promotion(Lean / Z3 / TLA+)
7. llmesh / llove 패밀리 통합
8. TRIZ 내장(40 원리 + 모순 매트릭스)

### v0.1.0 릴리스

- GSD `/gsd-new-project`로 초기화 → PROJECT.md / REQUIREMENTS.md (46 reqs) / ROADMAP.md (4 phases) / STATE.md / config.json 생성
- src/llive/ 8층: schema / core / container / memory / router / evolution / observability / triz
- 49 tests pass / 82% coverage
- CLI: `llive run --template specs/templates/qwen2_5_0_5b.yaml --prompt "..." --mock`
- 설계 판단: faiss / torch / sentence-transformers는 **optional extras**로 하고, Phase 1 테스트는 numpy + hash 임베딩 fallback으로 동작시킨다

### 교훈

- Optional extras 설계가 Windows + CI 양립에 필수
- GSD 워크플로(`--auto` 모드)로 하루 만에 Phase 1 완주 가능

## Day 2: 2026-05-13 (화 밤) — Phase 2 Adaptive

### v0.2.0 릴리스

- structural memory(graph) + parameter memory(adapter store) 추가
- Bayesian Surprise Gate(FR-21)로 메모리 쓰기 임계값을 동적화
- Consolidation 사이클이 야간 batch로 실행
- llove TUI에서 route trace + memory link viz
- LLM Wiki 통합(LLW-04)
- 연속 5 태스크 학습에서 BWT ≥ -1% 달성
- **308 tests / 99% coverage / 0 lint**

### 설계 판단

- “Bayesian surprise”로서 쓰기 제어 → 단순 threshold보다 유연
- 4층 메모리 사이에 **phase transition**(short → mid → long → archived → erased)을 넣어 life cycle 관리

## Day 3: 2026-05-14 (수) — 대규모 자율 세션

여기서부터 하루 만에 세 버전(v0.3 → v0.4 → v0.5)을 진행했다.

### v0.3.0 — Phase 3 (Controlled Self-Evolution) + Phase 4 (Production Security) 동시 릴리스

Phase 3 (Evolve):
- EVO-04 Z3 정적 검증
- EVO-06 Failed Reservoir(DuckDB 순서 보존)
- EVO-07 Reverse-Evo Monitor(JSONL audit)
- TRIZ-02 Contradiction Detector
- TRIZ-03 Principle Mapper(39×39 matrix)
- TRIZ-04 RAD-Backed Idea Generator(pluggable IdeaLLM Protocol)
- TRIZ-07 Self-Reflection Session
- LLW-04 Wiki Contradiction
- LLW-05 Wiki diff ChangeOp

Phase 4 (Security):
- SEC-01 Quarantined Memory Zone
- SEC-02 Ed25519 Signed Adapter
- SEC-03 SHA-256 audit hash chain(stdlib sqlite3만)

**429 tests / 98% coverage / 0 lint**

### v0.4.0 — Phase 5 Rust skeleton

- `crates/llive_rust_ext/` PyO3 0.22 + maturin scaffold
- RUST-01 (skeleton) / RUST-02 (compute_surprise baseline) / RUST-04 (jaccard baseline) / RUST-13 (Hypothesis parity 1e-6)
- `llive.rust_ext.HAS_RUST` flag + Python fallback
- 439 tests pass

### v0.5.0 — Phase 5 wire-in

- RUST-03 (bulk_time_decay) Rust kernel + Python wrapper + 5 parity tests
- BayesianSurpriseGate.compute_surprise가 rust_ext.HAS_RUST일 때 자동 위임(numpy fallback)
- EdgeWeightUpdater.apply_time_decay가 rust_ext.bulk_time_decay로 1 pass precompute
- **444 tests / 98% coverage / 0 lint**

### Day 3의 설계 판단

- **Rust 이식은 의미론 고정 후**에 단계적으로(5x 성능 향상 게이트 설정)
- 모든 RUST-XX 확장은 **Python fallback 필수**, Rust 부재 환경에서도 동작 유지
- 잔여 RUST-02 rayon / 05 jsonschema-rs / 06 crossbeam / 07 ChangeOp / 08 hora HNSW / 09 tokio async / 10 phf TRIZ / 11 Z3 bridge는 v0.7까지 deferred

### Day 3의 교훈

- 하루 만에 세 버전을 진행하려면 **코어 설계**와 **Optional extras 설계**가 필수
- “bench에서 5x 나오면 채용, 그렇지 않으면 revert”의 게이트를 명시

## Day 4: 2026-05-16 (목) — 9 axes + Apache 2.0 + FullSense umbrella

### v0.6.0 릴리스

- **9 axes skeleton** 완성 — KAR / DTKR / APO / ICP / TLB / Math / PM / RPAR / SIL
- C-1 Approval Bus 프로덕션화(Policy + SQLite Ledger)
- C-2 `@govern` + ProductionOutputBus(Policy gate × 부작용 emit)
- C-3 Cross-substrate migration spike(§MI1)
- C-14 ICP IdleCollaborator MVP(idle 중 peer LLM 질의)
- **970 PASS / 0 lint**

### 법무·브랜드 정비

- **Apache-2.0 + Commercial dual-license**로 전환
- **FullSense umbrella 브랜드** 도입(llmesh / llive / llove의 부모)
- NOTICE / CONTRIBUTING(DCO) / SECURITY / TRADEMARK 추가
- SPDX header를 204개 .py에 부여

### 같은 날의 또 하나의 움직임 — Brief A/B run

- `scripts/run_brief.py`로 4개 brief를 돌린 결과, llive가 **doing-agent가 아니라 thinking-evaluator**임이 판명
- 8건의 bug를 `docs/BUGS_2026-05-16_brief_ab.md`에 기록
- 설계 초안 `docs/proposals/brief_api_design.md`를 작성(5일 견적)

### Day 4의 교훈

- 9개 축(KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL)을 명시함으로써 책임 분리가 visible해짐
- A/B run이 **“여기까지 동작” “여기서부터 동작 안 함”**의 경계를 가시화, Brief API 필요성이 확정

## Day 5: 2026-05-17 (금, 오늘) — Brief API + 32건 요건 추가

### Brief API end-to-end (LLIVE-001/002)

설계 초안(5일 견적)을 **하루 만에 완주**:

- `src/llive/brief/types.py` — Brief / BriefStatus / BriefResult(COG-01에서 confidence/assumptions/missing_evidence 추가)
- `src/llive/brief/loader.py` — YAML loader(unknown-key reject)
- `src/llive/brief/ledger.py` — append-only JSONL + `trace_graph()`(COG-03)
- `src/llive/brief/runner.py` — 7단 파이프라인(Stimulus 변환 / loop / approval / tool 실행 / outcome)
- `src/llive/brief/grounding.py` — BriefGrounder(TRIZ × RAD citation, S1)
- `src/llive/brief/governance.py` — GovernanceScorer(4축 scoring, COG-02)
- `src/llive/cli/main.py` — `llive brief submit|ledger`
- `src/llive/mcp/tools.py` — `submit_brief` MCP tool
- 테스트 46 → 78건 추가

### 요건 추가 32건

| 그룹 | 건수 | 내용 |
|---|---|---|
| v0.7-vertical MATH | 8 | SI 단위 차원 해석 / 내장 계산 엔진 / Sympy 검산 / CODATA 사전 / 등 |
| v0.8 CABT | 7 | Cognitive-aware Transformer Block(forward hook으로 attention bias) |
| v0.9 CREAT | 5 | KJ법 / MindMap / Six Hats / Synectics / 구조화 변환 |
| v1.0-frame COG-FX | 4 | Triple Output / Governance Scoring / Trace Graph / Role-based Agents |
| v2.0-core ORG-FX | 8 | Qwen 의존으로부터의 5단계 이탈 + 보완 전략 |

### 구현한 것

- **MATH-01** SI 7 기본 단위 차원 해석 + 파생 단위(N/J/W/Pa/Hz/C/V/ohm)
- **MATH-08** SafeCalculator(AST visitor + whitelist 28 함수 + 0 나눗셈 검출)
- **COG-01** Triple Output(confidence / assumptions / missing_evidence)
- **COG-02** Governance Scoring(usefulness/feasibility/safety/traceability의 4축)
- **COG-03** Trace Graph(evidence_chain / tool_chain / decision_chain의 3층 view)

### 벤치마크 4종

| 종류 | 셀 수 | 주요 관찰 |
|---|---|---|
| progressive matrix | 5×3=15 | overhead < 1 %, decision 전부 note |
| fair re-bench(오산정→수정) | 24 | llive (LLM attached)는 ollama 직접 호출의 2-4배 느림 |
| quiz Debug | 10 | passed 6/10, ms mean 22.3s |
| quiz Release | 10 | passed 7/10, ms mean 22.8s, Debug overhead +1.8% |

### Honest disclosure 사건

- 처음 bench에서 llive 4/4 OK 134-184ms라는 “이상하게 빠른” 결과
- 사용자 지적 “이상하게 빠르네요, 뭔가 이상하지 않나요?”
- 조사 → LLMBackend 미 attach + chars 지표가 JSON 전체 길이 + 134-184ms는 subprocess RTT 기인
- 수정판으로 재실행 → llive 32-51s(ollama 직접 호출의 2-4배 느림)로 정직하게 공개
- 교훈을 memory `feedback_benchmark_honest_disclosure.md`에 저장

### 공개 글 11편 + 통합 2편

- 01-03: Brief API / 10 사고 인자 / 수학 vertical
- 04-06: 설계 예고(CABT / CREAT / MATH-02)
- 07-08: bench(fair / quiz)
- 09-11: 구조 독자성 / Qwen 이탈 / Qwen 보완
- QIITA_SUMMARY: 기술자용 통합(694행)
- QIITA_GENERAL: 비엔지니어용 통합(255행)
- 본 글(12): 개발 이력

### Day 5의 설계 판단

- Brief API는 **frozen dataclass + append-only JSONL ledger**로 replay 가능성을 최우선
- LLM 코어는 여전히 frozen, CABT는 forward hook으로 **가중치 동결한 채로** attention에 bias
- “bench에서 자사가 빠르면 의심한다”를 memory에 확립
- “매일 다양한 측면으로 글을 쓴다” “Qiita tags는 공백 구분 + 5건 이내” “비엔지니어용 버전도 만든다” “개발 이력도 쓴다”를 운영 규칙으로

### Day 5의 교훈

- **Honest disclosure가 연구의 신뢰를 떠받친다** — 빠른 숫자가 나와도 의심한다
- **다측면으로 쓰면 자신의 이해도 깊어진다** — 기술 / 전략 / 철학 / 업무 응용을 병행해 쓴다
- **“bench에서 이긴다”보다 “bench에서 무엇을 측정하는지 파악한다”**가 중요

## 5일간의 누적 메트릭

| 메트릭 | Day 1 시작 | Day 5 종료(오늘) | 배율 |
|---|---|---|---|
| 테스트 수 | 0 | 1014 PASS | — |
| 버전 | (없음) | v0.6.0 + v0.7 후보 | — |
| 요건 (FR) | 0 | 100 | — |
| RAD 분야 | 0 | 49(raptor 공유) | — |
| Phase | 0/4 | 4/4 완료 + Phase 5-12 계획 | — |
| LoC(추정) | 0 | ~30 000(테스트 포함) | — |
| 공개 글 | 0 | 12편 + 통합 2편 | — |
| GitHub repo | 0 | 4(llive + llmesh + llove + fullsense) | — |
| PyPI 공개 | 0 | 6 versions(v0.1.0 〜 v0.5.0 + suite) | — |

## 앞으로(2026-05-18 이후의 예상)

### 단기(~2주)

- MATH-02 Sympy 검산 + EVO-04 수식 버전
- MATH-05 CODATA 사전을 RAD metrology에 append
- S2 CABT-01 HFAdapter forward hook prototype
- 수학·물리 quiz set v2(현재의 v1을 확장, N≥30)

### 중기(~3개월)

- CREAT-01 KJ법 노드 + clustering
- CABT-02 Stage-aware Block Routing prototype
- Brief API를 lldesign / lltrade에 도입, 실 use case 구동으로 개선
- credential 복구 후의 6-model full matrix benchmark

### 장기(~1년)

- ORG-FX Stage B(LoRA로 llive용 adapter)
- ORG-FX Stage C(qwen2.5:14b → llive-7b 증류)
- llove TUI Creative Workbench
- llmesh-suite v1.0(4 제품 통합 인스톨러)

## 5일 만에 확립한 “llive 철학”

- **frozen LLM 코어 + 가변 주변** = replay 가능성을 최우선
- **append-only ledger** = 무엇이 일어났는지 전부 나중에 보인다
- **HITL을 architecture level에** = Approval Bus는 장식이 아니라 핵심
- **TRIZ를 mutation policy에 내장** = 창조성을 구조에 가져온다
- **on-prem only** = 로컬 환경이야말로 AI 본래의 거처(feedback_llive_measurement_purity)
- **honest disclosure** = 실패를 지우지 않고, 교훈을 memory에 남긴다
- **다측면으로 쓴다** = 기술 / 전략 / 철학 / 업무 응용을 매일 병행해 발신

## 관련 문서

- llive 저장소: <https://github.com/furuse-kazufumi/llive>
- llive CHANGELOG: <https://github.com/furuse-kazufumi/llive/blob/main/CHANGELOG.md>
- llive PROGRESS.md: <https://github.com/furuse-kazufumi/llive/blob/main/docs/PROGRESS.md>
- fullsense 포털: <https://github.com/furuse-kazufumi/fullsense>
- 같은 날 글:
  - [QIITA_SUMMARY](./QIITA_SUMMARY.md) — 기술자용 통합
  - [QIITA_GENERAL](./QIITA_GENERAL.md) — 비엔지니어용 통합
  - [01〜11 개별 글](./README.md)

---

> 5일 만에 v0.1 → v0.7 후보. 하루 1버전 이상의 페이스로 진행하면서, 그때마다
> honest disclosure를 남긴다. AI와 함께 개발하는 시대의 연구 기록으로 남긴다.
