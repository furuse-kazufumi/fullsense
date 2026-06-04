---
title: "llmesh → llove → llive — FullSense 3 製品の開発履歴・設計コンセプト・差別化・普及戦略 (2026-05-17 時点)"
tags: LLM 開発履歴 設計思想 オープンソース ローカル環境
id: adaa273817eddff5a677
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# llmesh → llove → llive — FullSense 3 製品の開発履歴・設計コンセプト・差別化・普及戦略 (2026-05-17 時点)

著者: **古瀬 和文（ぷるやん）**

## はじめに — なぜ 3 製品で 1 つの世界観なのか

私 (古瀬 和文 / ぷるやん) は **FullSense ™** という umbrella ブランドで 3 つの OSS プロジェクトを並走開発しています:

| 製品 | 役割 | PyPI | GitHub |
|---|---|---|---|
| **llmesh** | secure LLM hub (on-prem MCP server) | `llmesh` | <https://github.com/furuse-kazufumi/llmesh> |
| **llive** | self-evolving modular memory LLM framework | `llmesh-llive` | <https://github.com/furuse-kazufumi/llive> |
| **llove** | TUI dashboard / HITL workbench | `llmesh-llove` | <https://github.com/furuse-kazufumi/llove> |

すべて **Apache-2.0 + Commercial dual-license**。3 つは独立 OSS でありながら、組み合わせると「**自宅 PC で動く、責任感のある、おせっかいな AI エコシステム**」になります。

本記事は **3 製品の発足から本日 (2026-05-17) までの歴史**、**設計コンセプト**、**競合との差別化**、**多くの人に使ってもらうための工夫** をひとつにまとめたものです。

---

## 1. 開発履歴 — 3 製品の時系列

### llmesh (最古参)

| 時期 | 内容 |
|---|---|
| 〜2026-05-09 以前 | 発足。secure LLM hub + 産業 IoT 連携 |
| 2026-05-09 | v1.5.0 完了 — MTEngine + XbarRChart + CUSUMChart + CLI 統合 |
| 2026-05-14 | llmesh-suite v0.2.0 (one-shot installer for 3 製品) |
| 次 | v1.6.0 OPC-UA + MQTT (llive と連結予定) |

設計思想: **「LLM をハブとして使う」** — 複数の LLM (OpenAI / Anthropic / Ollama 等) を統合し、MCP プロトコルで配信。SPC (統計的工程管理) を埋め込み、産業 IoT に直接接続。

### llove (TUI HITL ワークベンチ)

| 時期 | 内容 |
|---|---|
| 2026-05-09 | v0.2.2 PyPI 初回公開 (llmesh-llove) |
| 2026-05-09 | F17 / F21 / F16 chess (216 PASS、未 push) |
| 2026-05-09 | F15 ブラウザ並み表示 (Markdown / SVG / Mermaid / 折り畳み) |
| 2026-05-09 | F16 マルチゲーム LLM 対局アリーナ (chess/go/mahjong/poker/...) |
| 2026-05-10 | F22 テトリスデモ (LLM × シミュレーション環境) |
| 2026-05-10 | F23 PowerShell 互換シェル / F24 Claude Code 統合 |
| 2026-05-12 | F25 連携基盤 (llove ↔ llmesh ↔ llive を MCP 経由で繋ぐ shim) |
| 2026-05-14 | F25 audience demo 磨き (多言語化 + 商業価値訴求) |

設計思想: **「人が AI を監督するための TUI」** — Textual ベース。SVG / Mermaid / Markdown を端末で再現、デモを多数用意して **「動きで魅せる」** ことで認知拡大。F16 アリーナは LLM 同士の対局という視覚的に派手な機能で SNS 拡散性を狙う。

### llive (本日 5 日目)

| 時期 | 内容 |
|---|---|
| 2026-05-13 | 発足、v0.1.0 — Phase 1 MVR (49 tests) |
| 2026-05-13 夜 | v0.2.0 — Phase 2 Adaptive (308 tests) |
| 2026-05-14 | v0.3 → v0.4 → v0.5 — Phase 3/4/5 (444 tests) |
| 2026-05-16 | v0.6.0 — 9 axes skeleton + Apache 2.0 + FullSense umbrella (970 tests) |
| 2026-05-17 (本日) | Brief API + 32 件要件 + 4 種ベンチ + 14 記事 (1014 tests) |

設計思想: **「LLM 本体ではなく、LLM の周りに被せる認知 OS」** — 4 層メモリ + 6 stage Loop + Approval Bus + TRIZ + 10 思考因子。詳細は同日記事 [09 llive 構造独自性 8 要素](./09_llive_structure_originality.md) 参照。

### 3 製品が交差する場所

```
                    [外部 LLM 提供元]
                Qwen / Llama / Mistral / GPT / Claude / Gemini
                              ↓
                         [llmesh]
                    secure LLM hub
                  MCP / OPC-UA / MQTT
                ↗      ↓       ↘
            llive    llove    産業 IoT
        認知 OS   TUI HITL   sensor bridge
            ↓      ↓
        Brief / 4 層メモリ / Approval Bus
            ↓
          実 use case (lldesign / lltrade / 計画中の llcad/lleda/llchip)
```

---

## 2. 設計コンセプト — 3 製品共通の哲学

### 哲学 1: Local 環境こそ AI の本来の居場所

cloud LLM (GPT / Claude / Gemini / Perplexity) は便利だが、**個人情報・企業機密・医療データ・家族の会話・産業 IoT センサーデータ** を外部に送るのは本来あってはならない領域。FullSense 3 製品は **完全 on-prem 動作** を最優先設計。

memory ルール: `feedback_llive_measurement_purity` — llive ベンチは「on-prem only」「cloud と混在禁止」。

### 哲学 2: 責任所在を architecture level に持ち込む

- **llive Approval Bus** — 危ない動作は必ず人間の承認を経由、SQLite ledger に永続化、replay 可
- **llmesh SPC** — 統計的工程管理で AI の動作を可視化、異常を早期検出
- **llove TUI** — 人間が AI の判断ループに必ず入る (HITL ワークベンチ)

3 製品いずれも「**AI 任せにしない**」設計。

### 哲学 3: 多側面の思考を構造化

llive の **10 思考因子 (構造化 / 再構成 / 閉ループ / 自己拡張 / 不確実性 / 探索 / 整合 / 来歴 / 多視点 / 現実接続)** は、心理の深層 (YouTube) から抽出した人間の思考の癖。これを LLM に持たせることで、AI を「単なる文字生成器」から「思考の足場を持つ知性」に拡張。

### 哲学 4: TRIZ で創造を構造に持ち込む

llive 内蔵の **TRIZ 40 原理 + 39×39 矛盾マトリクス + ARIZ + 9 画法** は、自己進化の mutation policy として動作。「面白い案を出す」のではなく「**矛盾を発見し、原理に従って体系的に解決**」する。

### 哲学 5: Honest disclosure を研究の核に

memory ルール: `feedback_benchmark_honest_disclosure` (2026-05-17 確立) — 自社が異常に速い結果が出たら、勝った気になる前に必ず内訳を疑う。失敗を消さず、教訓として残す。

### 哲学 6: ファミリーで作る

llmesh / llive / llove は **独立 OSS でありながら、組み合わせると 1 つの世界観**。これは PyPI 単独パッケージで完結できる Wolfram Alpha や ChatGPT との根本的な違い。**ユーザーは必要な部分だけ採用** できる。

---

## 3. 差別化要素 — 競合との位置づけ

### vs ChatGPT / Claude / Gemini / Perplexity (cloud LLM)

| 軸 | cloud LLM | FullSense |
|---|---|---|
| on-prem | ❌ | ✅ (完全自宅 PC で動作) |
| 個人情報保護 | ❌ (外部送信) | ✅ (送信ゼロ) |
| 監査ログ | ❌ | ✅ (SQLite ledger + SHA-256 chain) |
| 災害時 | ❌ (ネット切断で停止) | ✅ (Local で継続動作) |
| 月額コスト | ⚠️ ($20〜200/月) | ✅ (電気代のみ) |
| 計算精度 | ⚠️ (LLM 任せで誤算) | ✅ (内蔵電卓 + 単位次元解析) |
| 構造化 work unit | ❌ | ✅ (Brief API) |
| HITL ワークベンチ | ❌ | ✅ (llove TUI) |

### vs LangChain / LlamaIndex / AutoGen / CrewAI (Agent framework)

| 軸 | 既存 Agent framework | FullSense |
|---|---|---|
| Agent loop | ✅ (chain / multi-agent) | ✅ (6 stage Loop + Multi-track Filter) |
| memory | ✅ (vector DB) | ✅ + 4 層メモリ (semantic/episodic/structural/parameter) |
| HITL | ⚠️ (CLI prompt 程度) | ✅ (llove TUI ワークベンチ) |
| HITL audit | ❌ | ✅ (Approval Bus + ledger) |
| 形式検証 | ❌ | ✅ (Z3 / Sympy 統合) |
| 認知因子明示分解 | ❌ | ✅ (10 思考因子 + COG-FX) |
| TRIZ 内蔵 | ❌ | ✅ (40 原理 + ARIZ + 9 画法) |
| 産業 IoT 接続 | ❌ | ✅ (llmesh MQTT / OPC-UA) |
| TUI HITL ワークベンチ | ❌ | ✅ (llove) |

### vs Wolfram Alpha (数学・科学計算)

| 軸 | Wolfram Alpha | FullSense (MATH vertical) |
|---|---|---|
| 数式の正確性 | ✅ | ✅ (Z3 + Sympy 統合) |
| 単位次元解析 | ✅ | ✅ (SI 7 基本単位) |
| 物理定数 | ✅ | ✅ (CODATA + NIST) |
| 価格 | 有料 (cloud) | 無料 (Apache 2.0) |
| Local 動作 | ❌ | ✅ |
| OSS | ❌ | ✅ |
| LLM 統合 | ⚠️ | ✅ (BriefGrounder で自然) |
| 監査ログ | ❌ | ✅ (BriefLedger) |

### vs MemGPT / LongMem (memory framework)

| 軸 | MemGPT / LongMem | llive |
|---|---|---|
| 階層メモリ | ✅ | ✅ (4 層 + phase transition + 署名 zone) |
| Bayesian Surprise | ❌ | ✅ (FR-21) |
| 形式検証 gate | ❌ | ✅ (EVO-04 Z3) |
| HITL | ❌ | ✅ (llove TUI) |
| 産業 IoT | ❌ | ✅ (llmesh) |
| TRIZ mutation policy | ❌ | ✅ |

---

## 4. 多くの人に使ってもらうための工夫

### 工夫 1: Quick Start 30 秒

```bash
# llive
py -3.11 -m pip install llmesh-llive
llive-demo                              # 10 シナリオを順番に再生

# llove
py -3.11 -m pip install llmesh-llove
llove                                   # TUI 起動

# 3 製品まとめて
py -3.11 -m pip install llmesh-suite
llmesh-suite install                    # one-shot で全部
```

「面倒な設定なしで動く体験」を最優先。

### 工夫 2: Optional extras 設計

faiss / torch / sentence-transformers / Rust 拡張 などの **重い依存は optional**。基本機能は stdlib + numpy だけで動かせるため、Windows / Mac / Linux / 低スペック PC でも動作。

```bash
# 最小
pip install llmesh-llive

# torch を使いたい
pip install 'llmesh-llive[torch]'

# 全部
pip install 'llmesh-llive[all]'
```

### 工夫 3: 多言語ナレーション

llove demo は **ja / en / zh / ko の 4 言語** ナレーション対応:

```bash
llove-demo --lang en      # 英語
llove-demo --lang zh      # 中国語
llove-demo --lang ko      # 韓国語
```

LinkedIn / Qiita / note への投稿も多言語版を用意 (本記事と同フォルダ内の `LinkedIn_*_jp.md` / `_en.md` / `_zh.md` / `_ko.md` 参照)。

### 工夫 4: 多側面の記事を毎日

memory ルール: `feedback_daily_articles_policy` — 技術設計 / 実装報告 / ベンチ / honest disclosure / 戦略 / 哲学 / 業界比較 / 認知科学 / TRIZ / エコシステム / ユーザー体験 / 未来予測 / 教訓 の 13 側面から毎日記事を作る。

技術者向け (`QIITA_SUMMARY.md`) と非エンジニア向け (`QIITA_GENERAL.md`) と開発履歴 (`QIITA_HISTORY.md` = 本記事) を毎日並走。

### 工夫 5: デモを SNS 拡散性で設計

llove F16 マルチゲーム LLM 対局アリーナ (chess / go / mahjong / poker) や F22 テトリスデモは、**動きで魅せる、繰り返し再生される、商業価値が伝わる** ことを最優先に設計。LinkedIn / X / YouTube で拡散しやすい。

memory ルール: `project_f25_demo_polish` — デモは「採用ファネル先頭」「動きで魅せる」「商業価値訴求」を必須要件に。

### 工夫 6: 認知 OS というポジショニング

「llive は LLM ではなく LLM を内蔵する認知 OS」「FullSense は AI を使いこなす秘書エコシステム」と再フレーミング。これにより:

- 既存 LLM (Qwen / Llama / Mistral) との競合関係を回避
- 「単独で使うなら ChatGPT で十分」批判に対抗
- 「**Qwen を Local で安全に責任を持って使うなら FullSense が最短経路**」

### 工夫 7: dual-license で商用利用を促進

- **Apache-2.0** (OSS 開発者向け)
- **Commercial license** (企業の社内利用向け、商業サポート付き)

両方提供することで、研究も商用も同じ codebase で進められる。

### 工夫 8: HITL ワークベンチで AI 失業の不安を緩和

llove TUI では AI が「これでいいですか?」と聞いてきて、人間が承認 / 却下 / 修正可能。**完全自動ではなく、人間が必ず判断ループに入る** 設計。これは AI 失業の不安を減らし、企業導入のハードルを下げる。

### 工夫 9: 産業 IoT との直接接続

llmesh の MQTT / OPC-UA bridge により、製造業 / 計測 / 物理 / 工学 の現場で **AI が現場データを直接受け取り、判断を返す** 経路を提供。汎用 LLM では到達できない領域。

### 工夫 10: 多人数開発を想定した認知 OS

10 思考因子 + Multi-track Filter + Six Hats (CREAT-04) は、**個人開発でも複数の視点を保つ** ための仕組み。「architect / critic / executor / auditor」の 4 ロールが内蔵されているので、1 人開発でも認知の偏りを防げる。

---

## 5. これからの展望 (3 製品共通)

### 短期 (~3 ヶ月)

- llive: MATH-02 形式検証 / CABT-01 forward hook
- llmesh: v1.6.0 OPC-UA + MQTT
- llove: F25 完成 (E2E 連携) + Creative Workbench

### 中期 (~1 年)

- llive: ORG-FX Stage B (LoRA で llive 専用 adapter) → Stage C (qwen2.5:14b → llive-7b 蒸留)
- llmesh: v2.0 P2P mesh (金子勇 EDLA + Winny の局所学習則を技術導入)
- llove: F18 Rust 移植 (ratatui 並走 → 完全 Rust)

### 長期 (~3 年)

- llive: Stage D/E (Transformer 以外 / Surprise-native pretraining) → 論文化
- FullSense umbrella: v1.0.0 で PyPI rename (fullsense-* シリーズ)
- 3 製品統合 SaaS / 商用サポート提供

---

## 6. まとめ

**FullSense ™ = llmesh + llive + llove** の 3 製品で、以下を同時に提供:

- ✅ **完全 on-prem** (cloud LLM では到達できないプライバシー領域)
- ✅ **構造化 work unit** (Brief API で曖昧な依頼を排除)
- ✅ **10 思考因子内蔵** (認知 OS としての設計)
- ✅ **TRIZ 創造性エンジン** (40 原理 + 矛盾マトリクス)
- ✅ **Approval Bus + Ledger** (責任所在の永続化)
- ✅ **計算は決定論的** (LLM 任せの誤算を排除)
- ✅ **形式検証 gate** (Z3 + Sympy で数式幻覚を止める)
- ✅ **HITL ワークベンチ** (llove TUI で人間が判断ループに)
- ✅ **産業 IoT 接続** (MQTT / OPC-UA で現場データ直結)
- ✅ **多言語対応** (ja / en / zh / ko)
- ✅ **Apache-2.0 + Commercial dual** (OSS + 商用両立)

これらは個別 OSS でも価値があるが、**組み合わせると「LLM の周辺すべてが揃った認知 OS エコシステム」** になります。

質問・コラボ・商用利用は GitHub Issues または Twitter / X (@puruyan) までお気軽に。

---

## 関連リンク

- llmesh: <https://github.com/furuse-kazufumi/llmesh>
- llive: <https://github.com/furuse-kazufumi/llive>
- llove: <https://github.com/furuse-kazufumi/llove>
- FullSense umbrella ポータル: <https://github.com/furuse-kazufumi/fullsense>
- llmesh-suite (one-shot installer): <https://github.com/furuse-kazufumi/llmesh-suite>

### 同日記事 (2026-05-17)

- 技術者向け詳細 (11 本): [docs/articles/2026-05-17/](.)
- 技術者向け統合: [QIITA_SUMMARY.md](./QIITA_SUMMARY.md)
- 非エンジニア向け統合: [QIITA_GENERAL.md](./QIITA_GENERAL.md)
- 開発履歴 (llive 単独 5 日): [12_dev_history.md](./12_dev_history.md)
- **本記事 (llmesh + llove + llive 統合履歴 + 設計 + 差別化 + 普及)**

### LinkedIn 投稿用 (本記事と同フォルダ、多言語版)

- [LinkedIn_SUMMARY_jp.md](./LinkedIn_SUMMARY_jp.md) / `_en.md` / `_zh.md` / `_ko.md`
- [LinkedIn_GENERAL_jp.md](./LinkedIn_GENERAL_jp.md) / `_en.md` / `_zh.md` / `_ko.md`
- [LinkedIn_HISTORY_jp.md](./LinkedIn_HISTORY_jp.md) / `_en.md` / `_zh.md` / `_ko.md`

---

> 3 製品 = 1 つの世界観 = **「自宅 PC で動く、責任感のある、おせっかいな AI エコシステム」**

---

# English

# llmesh → llove → llive — Development History, Design Concepts, Differentiation, and Adoption Strategy of the Three FullSense Products (as of 2026-05-17)

Author: **Kazufumi Furuse (puruyan)**

## Introduction — Why Three Products Form a Single Worldview

I (Kazufumi Furuse / puruyan) develop three OSS projects in parallel under an umbrella brand called **FullSense ™**:

| Product | Role | PyPI | GitHub |
|---|---|---|---|
| **llmesh** | secure LLM hub (on-prem MCP server) | `llmesh` | <https://github.com/furuse-kazufumi/llmesh> |
| **llive** | self-evolving modular memory LLM framework | `llmesh-llive` | <https://github.com/furuse-kazufumi/llive> |
| **llove** | TUI dashboard / HITL workbench | `llmesh-llove` | <https://github.com/furuse-kazufumi/llove> |

All are **Apache-2.0 + Commercial dual-license**. The three are independent OSS, yet when combined they become a "**responsible, caring AI ecosystem that runs on your home PC**."

This article brings together, in one place, the **history of the three products from their launch up to today (2026-05-17)**, their **design concepts**, their **differentiation from competitors**, and the **techniques used to get many people to adopt them**.

---

## 1. Development History — A Timeline of the Three Products

### llmesh (the most senior)

| Period | Content |
|---|---|
| Before 2026-05-09 | Launch. secure LLM hub + industrial IoT integration |
| 2026-05-09 | v1.5.0 completed — MTEngine + XbarRChart + CUSUMChart + CLI integration |
| 2026-05-14 | llmesh-suite v0.2.0 (one-shot installer for the 3 products) |
| Next | v1.6.0 OPC-UA + MQTT (planned linkage with llive) |

Design philosophy: **"Use the LLM as a hub"** — integrate multiple LLMs (OpenAI / Anthropic / Ollama, etc.) and distribute them via the MCP protocol. Embed SPC (statistical process control) and connect directly to industrial IoT.

### llove (TUI HITL workbench)

| Period | Content |
|---|---|
| 2026-05-09 | v0.2.2 first PyPI release (llmesh-llove) |
| 2026-05-09 | F17 / F21 / F16 chess (216 PASS, not yet pushed) |
| 2026-05-09 | F15 browser-grade rendering (Markdown / SVG / Mermaid / folding) |
| 2026-05-09 | F16 multi-game LLM match arena (chess/go/mahjong/poker/...) |
| 2026-05-10 | F22 Tetris demo (LLM × simulation environment) |
| 2026-05-10 | F23 PowerShell-compatible shell / F24 Claude Code integration |
| 2026-05-12 | F25 linkage foundation (a shim connecting llove ↔ llmesh ↔ llive via MCP) |
| 2026-05-14 | F25 audience demo polish (multilingual + commercial-value appeal) |

Design philosophy: **"A TUI for humans to supervise AI"** — built on Textual. It reproduces SVG / Mermaid / Markdown in the terminal and provides many demos so it can grow awareness by **"impressing through motion."** The F16 arena aims for SNS virality with the visually striking feature of LLMs playing against each other.

### llive (5 days old today)

| Period | Content |
|---|---|
| 2026-05-13 | Launch, v0.1.0 — Phase 1 MVR (49 tests) |
| Night of 2026-05-13 | v0.2.0 — Phase 2 Adaptive (308 tests) |
| 2026-05-14 | v0.3 → v0.4 → v0.5 — Phase 3/4/5 (444 tests) |
| 2026-05-16 | v0.6.0 — 9 axes skeleton + Apache 2.0 + FullSense umbrella (970 tests) |
| 2026-05-17 (today) | Brief API + 32 requirements + 4 kinds of benchmarks + 14 articles (1014 tests) |

Design philosophy: **"Not the LLM itself, but a cognitive OS draped around the LLM"** — 4-layer memory + 6-stage Loop + Approval Bus + TRIZ + 10 thinking factors. For details, see the same-day article [09 The 8 Elements of llive's Structural Originality](./09_llive_structure_originality.md).

### Where the Three Products Intersect

```
                    [外部 LLM 提供元]
                Qwen / Llama / Mistral / GPT / Claude / Gemini
                              ↓
                         [llmesh]
                    secure LLM hub
                  MCP / OPC-UA / MQTT
                ↗      ↓       ↘
            llive    llove    産業 IoT
        認知 OS   TUI HITL   sensor bridge
            ↓      ↓
        Brief / 4 層メモリ / Approval Bus
            ↓
          実 use case (lldesign / lltrade / 計画中の llcad/lleda/llchip)
```

---

## 2. Design Concepts — A Philosophy Shared by All Three Products

### Philosophy 1: The Local Environment Is Where AI Truly Belongs

Cloud LLMs (GPT / Claude / Gemini / Perplexity) are convenient, but **personal information, corporate secrets, medical data, family conversations, and industrial IoT sensor data** belong to a realm that should never be sent outside. The three FullSense products prioritize **fully on-prem operation** above all else.

memory rule: `feedback_llive_measurement_purity` — llive benchmarks are "on-prem only," "no mixing with the cloud."

### Philosophy 2: Bring Accountability Down to the Architecture Level

- **llive Approval Bus** — risky actions always pass through human approval, are persisted to a SQLite ledger, and can be replayed
- **llmesh SPC** — statistical process control makes AI behavior visible and detects anomalies early
- **llove TUI** — humans are always inside the AI's decision loop (HITL workbench)

All three products are designed to **"never leave it all to the AI."**

### Philosophy 3: Structure Multi-faceted Thinking

llive's **10 thinking factors (structuring / reconstruction / closed loop / self-expansion / uncertainty / exploration / consistency / provenance / multi-perspective / reality connection)** are quirks of human thought extracted from "The Depths of Psychology" (YouTube). By giving these to an LLM, the AI is expanded from a "mere character generator" into "an intelligence with scaffolding for thought."

### Philosophy 4: Use TRIZ to Bring Creativity into Structure

llive's built-in **TRIZ 40 principles + 39×39 contradiction matrix + ARIZ + 9-windows method** operate as a mutation policy for self-evolution. Rather than "producing interesting ideas," it **"discovers contradictions and resolves them systematically according to principles."**

### Philosophy 5: Make Honest Disclosure the Core of Research

memory rule: `feedback_benchmark_honest_disclosure` (established 2026-05-17) — when your own results come out abnormally fast, always doubt the breakdown before feeling like you've won. Don't erase failures; keep them as lessons.

### Philosophy 6: Build as a Family

llmesh / llive / llove are **independent OSS, yet when combined they form a single worldview**. This is a fundamental difference from Wolfram Alpha or ChatGPT, which are complete in a single standalone package. **Users can adopt only the parts they need.**

---

## 3. Differentiators — Positioning Against Competitors

### vs ChatGPT / Claude / Gemini / Perplexity (cloud LLM)

| Axis | cloud LLM | FullSense |
|---|---|---|
| on-prem | ❌ | ✅ (runs entirely on a home PC) |
| personal-data protection | ❌ (sent externally) | ✅ (zero transmission) |
| audit log | ❌ | ✅ (SQLite ledger + SHA-256 chain) |
| during disasters | ❌ (stops when the network is cut) | ✅ (keeps running locally) |
| monthly cost | ⚠️ ($20–200/month) | ✅ (electricity only) |
| computational accuracy | ⚠️ (miscalculations left to the LLM) | ✅ (built-in calculator + unit-dimension analysis) |
| structured work unit | ❌ | ✅ (Brief API) |
| HITL workbench | ❌ | ✅ (llove TUI) |

### vs LangChain / LlamaIndex / AutoGen / CrewAI (Agent framework)

| Axis | existing Agent framework | FullSense |
|---|---|---|
| Agent loop | ✅ (chain / multi-agent) | ✅ (6-stage Loop + Multi-track Filter) |
| memory | ✅ (vector DB) | ✅ + 4-layer memory (semantic/episodic/structural/parameter) |
| HITL | ⚠️ (about the level of a CLI prompt) | ✅ (llove TUI workbench) |
| HITL audit | ❌ | ✅ (Approval Bus + ledger) |
| formal verification | ❌ | ✅ (Z3 / Sympy integration) |
| explicit decomposition of cognitive factors | ❌ | ✅ (10 thinking factors + COG-FX) |
| TRIZ built in | ❌ | ✅ (40 principles + ARIZ + 9-windows method) |
| industrial IoT connection | ❌ | ✅ (llmesh MQTT / OPC-UA) |
| TUI HITL workbench | ❌ | ✅ (llove) |

### vs Wolfram Alpha (mathematics & scientific computing)

| Axis | Wolfram Alpha | FullSense (MATH vertical) |
|---|---|---|
| formula accuracy | ✅ | ✅ (Z3 + Sympy integration) |
| unit-dimension analysis | ✅ | ✅ (SI 7 base units) |
| physical constants | ✅ | ✅ (CODATA + NIST) |
| price | paid (cloud) | free (Apache 2.0) |
| local operation | ❌ | ✅ |
| OSS | ❌ | ✅ |
| LLM integration | ⚠️ | ✅ (natural with BriefGrounder) |
| audit log | ❌ | ✅ (BriefLedger) |

### vs MemGPT / LongMem (memory framework)

| Axis | MemGPT / LongMem | llive |
|---|---|---|
| hierarchical memory | ✅ | ✅ (4 layers + phase transition + signed zone) |
| Bayesian Surprise | ❌ | ✅ (FR-21) |
| formal-verification gate | ❌ | ✅ (EVO-04 Z3) |
| HITL | ❌ | ✅ (llove TUI) |
| industrial IoT | ❌ | ✅ (llmesh) |
| TRIZ mutation policy | ❌ | ✅ |

---

## 4. Techniques to Get Many People to Adopt It

### Technique 1: 30-Second Quick Start

```bash
# llive
py -3.11 -m pip install llmesh-llive
llive-demo                              # 10 シナリオを順番に再生

# llove
py -3.11 -m pip install llmesh-llove
llove                                   # TUI 起動

# 3 製品まとめて
py -3.11 -m pip install llmesh-suite
llmesh-suite install                    # one-shot で全部
```

Top priority is "an experience that just works with no tedious setup."

### Technique 2: Optional Extras Design

**Heavy dependencies** such as faiss / torch / sentence-transformers / Rust extensions are **optional**. Because the core features run on just stdlib + numpy, they work on Windows / Mac / Linux and even low-spec PCs.

```bash
# 最小
pip install llmesh-llive

# torch を使いたい
pip install 'llmesh-llive[torch]'

# 全部
pip install 'llmesh-llive[all]'
```

### Technique 3: Multilingual Narration

llove demo supports narration in **4 languages: ja / en / zh / ko**:

```bash
llove-demo --lang en      # 英語
llove-demo --lang zh      # 中国語
llove-demo --lang ko      # 韓国語
```

Posts to LinkedIn / Qiita / note also come in multilingual versions (see `LinkedIn_*_jp.md` / `_en.md` / `_zh.md` / `_ko.md` in the same folder as this article).

### Technique 4: Multi-faceted Articles Every Day

memory rule: `feedback_daily_articles_policy` — create articles every day from 13 facets: technical design / implementation reports / benchmarks / honest disclosure / strategy / philosophy / industry comparison / cognitive science / TRIZ / ecosystem / user experience / future forecasts / lessons learned.

A version for engineers (`QIITA_SUMMARY.md`), a version for non-engineers (`QIITA_GENERAL.md`), and a development history (`QIITA_HISTORY.md` = this article) run in parallel every day.

### Technique 5: Design Demos for SNS Virality

The llove F16 multi-game LLM match arena (chess / go / mahjong / poker) and the F22 Tetris demo are designed with top priority on being **impressive through motion, replayed repeatedly, and conveying commercial value**. They are easy to spread on LinkedIn / X / YouTube.

memory rule: `project_f25_demo_polish` — demos must satisfy the requirements of "front of the adoption funnel," "impress through motion," and "appeal to commercial value."

### Technique 6: Positioning as a Cognitive OS

Reframing it as "llive is not an LLM but a cognitive OS that embeds an LLM" and "FullSense is a secretarial ecosystem for mastering AI." This achieves:

- Avoiding a competitive relationship with existing LLMs (Qwen / Llama / Mistral)
- Countering the criticism "if you're going to use it alone, ChatGPT is enough"
- "**If you want to use Qwen locally, safely, and responsibly, FullSense is the shortest path**"

### Technique 7: Promote Commercial Use with Dual-licensing

- **Apache-2.0** (for OSS developers)
- **Commercial license** (for in-house corporate use, with commercial support)

By offering both, research and commercial use can proceed on the same codebase.

### Technique 8: Ease the Fear of AI-driven Job Loss with a HITL Workbench

In the llove TUI, the AI asks "Is this okay?" and humans can approve / reject / revise. It is designed so that **it is not fully automatic; humans are always inside the decision loop.** This reduces the fear of AI-driven job loss and lowers the barrier to corporate adoption.

### Technique 9: Direct Connection to Industrial IoT

Via llmesh's MQTT / OPC-UA bridge, it provides a path where **AI directly receives field data and returns decisions** in manufacturing / metrology / physics / engineering settings. This is a domain that general-purpose LLMs cannot reach.

### Technique 10: A Cognitive OS Designed for Multi-person Development

The 10 thinking factors + Multi-track Filter + Six Hats (CREAT-04) are mechanisms for **maintaining multiple perspectives even in solo development**. Because the four roles "architect / critic / executor / auditor" are built in, even a single developer can prevent cognitive bias.

---

## 5. The Road Ahead (Common to All Three Products)

### Short term (~3 months)

- llive: MATH-02 formal verification / CABT-01 forward hook
- llmesh: v1.6.0 OPC-UA + MQTT
- llove: F25 completion (E2E linkage) + Creative Workbench

### Medium term (~1 year)

- llive: ORG-FX Stage B (a llive-specific adapter via LoRA) → Stage C (distilling qwen2.5:14b → llive-7b)
- llmesh: v2.0 P2P mesh (technically adopting the local learning rules of Isamu Kaneko's EDLA + Winny)
- llove: F18 Rust port (running alongside ratatui → fully Rust)

### Long term (~3 years)

- llive: Stage D/E (non-Transformer / Surprise-native pretraining) → publish as a paper
- FullSense umbrella: PyPI rename at v1.0.0 (the fullsense-* series)
- Three-product integrated SaaS / commercial support offering

---

## 6. Summary

**FullSense ™ = llmesh + llive + llove**, three products that simultaneously provide:

- ✅ **Fully on-prem** (a privacy realm cloud LLMs cannot reach)
- ✅ **Structured work units** (the Brief API eliminates vague requests)
- ✅ **10 thinking factors built in** (designed as a cognitive OS)
- ✅ **TRIZ creativity engine** (40 principles + contradiction matrix)
- ✅ **Approval Bus + Ledger** (persistence of accountability)
- ✅ **Deterministic computation** (eliminating miscalculations left to the LLM)
- ✅ **Formal-verification gate** (stopping formula hallucinations with Z3 + Sympy)
- ✅ **HITL workbench** (humans in the decision loop via the llove TUI)
- ✅ **Industrial IoT connection** (direct field-data link via MQTT / OPC-UA)
- ✅ **Multilingual support** (ja / en / zh / ko)
- ✅ **Apache-2.0 + Commercial dual** (OSS and commercial coexist)

Each is valuable as standalone OSS, but **when combined they become "a cognitive OS ecosystem with everything around the LLM in place."**

For questions, collaboration, or commercial use, feel free to reach out via GitHub Issues or Twitter / X (@puruyan).

---

## Related Links

- llmesh: <https://github.com/furuse-kazufumi/llmesh>
- llive: <https://github.com/furuse-kazufumi/llive>
- llove: <https://github.com/furuse-kazufumi/llove>
- FullSense umbrella portal: <https://github.com/furuse-kazufumi/fullsense>
- llmesh-suite (one-shot installer): <https://github.com/furuse-kazufumi/llmesh-suite>

### Same-day Articles (2026-05-17)

- Detailed for engineers (11 articles): [docs/articles/2026-05-17/](.)
- Engineer-facing integration: [QIITA_SUMMARY.md](./QIITA_SUMMARY.md)
- Non-engineer-facing integration: [QIITA_GENERAL.md](./QIITA_GENERAL.md)
- Development history (llive alone, 5 days): [12_dev_history.md](./12_dev_history.md)
- **This article (integrated history + design + differentiation + adoption of llmesh + llove + llive)**

### For LinkedIn Posts (same folder as this article, multilingual versions)

- [LinkedIn_SUMMARY_jp.md](./LinkedIn_SUMMARY_jp.md) / `_en.md` / `_zh.md` / `_ko.md`
- [LinkedIn_GENERAL_jp.md](./LinkedIn_GENERAL_jp.md) / `_en.md` / `_zh.md` / `_ko.md`
- [LinkedIn_HISTORY_jp.md](./LinkedIn_HISTORY_jp.md) / `_en.md` / `_zh.md` / `_ko.md`

---

> Three products = one worldview = **"a responsible, caring AI ecosystem that runs on your home PC"**

---

# 中文

# llmesh → llove → llive — FullSense 三款产品的开发历程、设计理念、差异化与普及策略（截至 2026-05-17）

作者：**古濑和文（puruyan）**

## 引言 —— 为什么用三款产品构成同一个世界观

我（古濑和文 / puruyan）以一个名为 **FullSense ™** 的 umbrella 品牌并行开发三个 OSS 项目：

| 产品 | 角色 | PyPI | GitHub |
|---|---|---|---|
| **llmesh** | secure LLM hub（on-prem MCP server） | `llmesh` | <https://github.com/furuse-kazufumi/llmesh> |
| **llive** | self-evolving modular memory LLM framework | `llmesh-llive` | <https://github.com/furuse-kazufumi/llive> |
| **llove** | TUI dashboard / HITL workbench | `llmesh-llove` | <https://github.com/furuse-kazufumi/llove> |

三者均为 **Apache-2.0 + Commercial dual-license**。它们既是独立的 OSS，组合起来又会成为「**运行在家用 PC 上、有责任感、爱管闲事的 AI 生态系统**」。

本文将 **三款产品从创立到今日（2026-05-17）的历史**、**设计理念**、**与竞品的差异化**、以及 **让更多人使用的种种巧思** 汇集于一处。

---

## 1. 开发历程 —— 三款产品的时间线

### llmesh（资历最老）

| 时期 | 内容 |
|---|---|
| 2026-05-09 之前 | 创立。secure LLM hub + 工业 IoT 联动 |
| 2026-05-09 | v1.5.0 完成 —— MTEngine + XbarRChart + CUSUMChart + CLI 集成 |
| 2026-05-14 | llmesh-suite v0.2.0（面向 3 款产品的 one-shot installer） |
| 下一步 | v1.6.0 OPC-UA + MQTT（计划与 llive 连接） |

设计思想：**「把 LLM 当作枢纽来用」** —— 整合多个 LLM（OpenAI / Anthropic / Ollama 等），通过 MCP 协议进行分发。内嵌 SPC（统计过程控制），直接连接工业 IoT。

### llove（TUI HITL 工作台）

| 时期 | 内容 |
|---|---|
| 2026-05-09 | v0.2.2 首次在 PyPI 发布（llmesh-llove） |
| 2026-05-09 | F17 / F21 / F16 chess（216 PASS，尚未 push） |
| 2026-05-09 | F15 浏览器级渲染（Markdown / SVG / Mermaid / 折叠） |
| 2026-05-09 | F16 多游戏 LLM 对局竞技场（chess/go/mahjong/poker/...） |
| 2026-05-10 | F22 俄罗斯方块演示（LLM × 模拟环境） |
| 2026-05-10 | F23 PowerShell 兼容 shell / F24 Claude Code 集成 |
| 2026-05-12 | F25 联动基础（通过 MCP 连接 llove ↔ llmesh ↔ llive 的 shim） |
| 2026-05-14 | F25 audience demo 打磨（多语言化 + 商业价值诉求） |

设计思想：**「供人监督 AI 的 TUI」** —— 基于 Textual。在终端中再现 SVG / Mermaid / Markdown，准备大量演示，以 **「用动态吸引眼球」** 来扩大认知。F16 竞技场以 LLM 之间对局这一在视觉上华丽的功能瞄准 SNS 的传播性。

### llive（今天是第 5 天）

| 时期 | 内容 |
|---|---|
| 2026-05-13 | 创立，v0.1.0 —— Phase 1 MVR（49 tests） |
| 2026-05-13 夜 | v0.2.0 —— Phase 2 Adaptive（308 tests） |
| 2026-05-14 | v0.3 → v0.4 → v0.5 —— Phase 3/4/5（444 tests） |
| 2026-05-16 | v0.6.0 —— 9 axes skeleton + Apache 2.0 + FullSense umbrella（970 tests） |
| 2026-05-17（今日） | Brief API + 32 项需求 + 4 种基准测试 + 14 篇文章（1014 tests） |

设计思想：**「不是 LLM 本体，而是套在 LLM 周围的认知 OS」** —— 4 层记忆 + 6 stage Loop + Approval Bus + TRIZ + 10 个思考因子。详情请参见同日文章 [09 llive 结构独创性 8 要素](./09_llive_structure_originality.md)。

### 三款产品交汇之处

```
                    [外部 LLM 提供元]
                Qwen / Llama / Mistral / GPT / Claude / Gemini
                              ↓
                         [llmesh]
                    secure LLM hub
                  MCP / OPC-UA / MQTT
                ↗      ↓       ↘
            llive    llove    産業 IoT
        認知 OS   TUI HITL   sensor bridge
            ↓      ↓
        Brief / 4 層メモリ / Approval Bus
            ↓
          実 use case (lldesign / lltrade / 計画中の llcad/lleda/llchip)
```

---

## 2. 设计理念 —— 三款产品共通的哲学

### 哲学 1：本地环境才是 AI 真正的归宿

cloud LLM（GPT / Claude / Gemini / Perplexity）固然方便，但 **个人信息、企业机密、医疗数据、家人对话、工业 IoT 传感器数据** 本来就属于不应外发的领域。FullSense 三款产品将 **完全 on-prem 运行** 作为最优先的设计。

memory 规则：`feedback_llive_measurement_purity` —— llive 基准测试坚持「仅 on-prem」「禁止与 cloud 混用」。

### 哲学 2：把责任归属下沉到 architecture 层面

- **llive Approval Bus** —— 危险动作必经人类审批，持久化到 SQLite ledger，可 replay
- **llmesh SPC** —— 以统计过程控制将 AI 的动作可视化，及早检测异常
- **llove TUI** —— 人类必定进入 AI 的判断回路（HITL 工作台）

三款产品无一不是「**绝不全权交给 AI**」的设计。

### 哲学 3：把多侧面的思考结构化

llive 的 **10 个思考因子（结构化 / 重构 / 闭环 / 自我扩张 / 不确定性 / 探索 / 一致 / 来历 / 多视角 / 现实连接）** 是从「心理的深层」（YouTube）中提取出的人类思维的习性。让 LLM 拥有这些，便能把 AI 从「单纯的文字生成器」扩展为「拥有思考立足点的智能」。

### 哲学 4：用 TRIZ 把创造带入结构

llive 内置的 **TRIZ 40 原理 + 39×39 矛盾矩阵 + ARIZ + 9 画法** 作为自我进化的 mutation policy 运转。它不是「提出有趣的点子」，而是 **「发现矛盾，并依据原理系统性地解决」**。

### 哲学 5：把 Honest disclosure 作为研究的核心

memory 规则：`feedback_benchmark_honest_disclosure`（2026-05-17 确立）—— 当自家出现异常快的结果时，在自以为获胜之前务必怀疑其内幕。不抹去失败，而是作为教训保留。

### 哲学 6：作为一个家族来打造

llmesh / llive / llove **既是独立的 OSS，组合起来又构成同一个世界观**。这正是与可在单个独立包内自成一体的 Wolfram Alpha 或 ChatGPT 的根本区别。**用户可以只采用所需的部分。**

---

## 3. 差异化要素 —— 相对竞品的定位

### vs ChatGPT / Claude / Gemini / Perplexity（cloud LLM）

| 轴 | cloud LLM | FullSense |
|---|---|---|
| on-prem | ❌ | ✅（完全运行于家用 PC） |
| 个人信息保护 | ❌（外发） | ✅（零外发） |
| 审计日志 | ❌ | ✅（SQLite ledger + SHA-256 chain） |
| 灾害时 | ❌（断网即停止） | ✅（在本地持续运行） |
| 月费 | ⚠️（20～200 美元/月） | ✅（仅电费） |
| 计算精度 | ⚠️（交给 LLM 而误算） | ✅（内置计算器 + 单位量纲分析） |
| 结构化 work unit | ❌ | ✅（Brief API） |
| HITL 工作台 | ❌ | ✅（llove TUI） |

### vs LangChain / LlamaIndex / AutoGen / CrewAI（Agent framework）

| 轴 | 现有 Agent framework | FullSense |
|---|---|---|
| Agent loop | ✅（chain / multi-agent） | ✅（6 stage Loop + Multi-track Filter） |
| memory | ✅（vector DB） | ✅ + 4 层记忆（semantic/episodic/structural/parameter） |
| HITL | ⚠️（约为 CLI prompt 程度） | ✅（llove TUI 工作台） |
| HITL audit | ❌ | ✅（Approval Bus + ledger） |
| 形式验证 | ❌ | ✅（Z3 / Sympy 集成） |
| 认知因子显式分解 | ❌ | ✅（10 个思考因子 + COG-FX） |
| 内置 TRIZ | ❌ | ✅（40 原理 + ARIZ + 9 画法） |
| 工业 IoT 连接 | ❌ | ✅（llmesh MQTT / OPC-UA） |
| TUI HITL 工作台 | ❌ | ✅（llove） |

### vs Wolfram Alpha（数学・科学计算）

| 轴 | Wolfram Alpha | FullSense（MATH vertical） |
|---|---|---|
| 公式正确性 | ✅ | ✅（Z3 + Sympy 集成） |
| 单位量纲分析 | ✅ | ✅（SI 7 基本单位） |
| 物理常数 | ✅ | ✅（CODATA + NIST） |
| 价格 | 付费（cloud） | 免费（Apache 2.0） |
| 本地运行 | ❌ | ✅ |
| OSS | ❌ | ✅ |
| LLM 集成 | ⚠️ | ✅（用 BriefGrounder 很自然） |
| 审计日志 | ❌ | ✅（BriefLedger） |

### vs MemGPT / LongMem（memory framework）

| 轴 | MemGPT / LongMem | llive |
|---|---|---|
| 分层记忆 | ✅ | ✅（4 层 + phase transition + 签名 zone） |
| Bayesian Surprise | ❌ | ✅（FR-21） |
| 形式验证 gate | ❌ | ✅（EVO-04 Z3） |
| HITL | ❌ | ✅（llove TUI） |
| 工业 IoT | ❌ | ✅（llmesh） |
| TRIZ mutation policy | ❌ | ✅ |

---

## 4. 让更多人使用的种种巧思

### 巧思 1：30 秒 Quick Start

```bash
# llive
py -3.11 -m pip install llmesh-llive
llive-demo                              # 10 シナリオを順番に再生

# llove
py -3.11 -m pip install llmesh-llove
llove                                   # TUI 起動

# 3 製品まとめて
py -3.11 -m pip install llmesh-suite
llmesh-suite install                    # one-shot で全部
```

最优先「无需繁琐设置即可运行的体验」。

### 巧思 2：Optional extras 设计

faiss / torch / sentence-transformers / Rust 扩展 等 **沉重的依赖均为 optional**。核心功能仅靠 stdlib + numpy 即可运行，因此在 Windows / Mac / Linux / 低配 PC 上也能运行。

```bash
# 最小
pip install llmesh-llive

# torch を使いたい
pip install 'llmesh-llive[torch]'

# 全部
pip install 'llmesh-llive[all]'
```

### 巧思 3：多语言旁白

llove demo 支持 **ja / en / zh / ko 四种语言** 的旁白：

```bash
llove-demo --lang en      # 英語
llove-demo --lang zh      # 中国語
llove-demo --lang ko      # 韓国語
```

向 LinkedIn / Qiita / note 的投稿也准备了多语言版本（参见与本文同一文件夹中的 `LinkedIn_*_jp.md` / `_en.md` / `_zh.md` / `_ko.md`）。

### 巧思 4：每天产出多侧面的文章

memory 规则：`feedback_daily_articles_policy` —— 从技术设计 / 实现报告 / 基准 / honest disclosure / 战略 / 哲学 / 行业对比 / 认知科学 / TRIZ / 生态系统 / 用户体验 / 未来预测 / 教训 这 13 个侧面，每天产出文章。

面向技术者（`QIITA_SUMMARY.md`）、面向非工程师（`QIITA_GENERAL.md`）、以及开发历程（`QIITA_HISTORY.md` = 本文）每天并行推进。

### 巧思 5：以 SNS 传播性设计演示

llove F16 多游戏 LLM 对局竞技场（chess / go / mahjong / poker）和 F22 俄罗斯方块演示，都以 **用动态吸引眼球、被反复回放、传达商业价值** 为最优先来设计。它们易于在 LinkedIn / X / YouTube 上传播。

memory 规则：`project_f25_demo_polish` —— 演示必须满足「采用漏斗的最前端」「用动态吸引眼球」「诉求商业价值」的要件。

### 巧思 6：以认知 OS 进行定位

将其重新框定为「llive 不是 LLM，而是内置 LLM 的认知 OS」「FullSense 是驾驭 AI 的秘书生态系统」。由此：

- 回避与现有 LLM（Qwen / Llama / Mistral）的竞争关系
- 对抗「若是单独使用，ChatGPT 就够了」的批评
- 「**若要在本地安全且有责任地使用 Qwen，FullSense 是最短路径**」

### 巧思 7：以 dual-license 促进商用

- **Apache-2.0**（面向 OSS 开发者）
- **Commercial license**（面向企业内部使用，附带商业支持）

两者皆提供，使得研究与商用都能在同一 codebase 上推进。

### 巧思 8：以 HITL 工作台缓解对 AI 失业的不安

在 llove TUI 中，AI 会询问「这样可以吗？」，人类可以批准 / 驳回 / 修改。它被设计成 **并非完全自动，而是人类必定进入判断回路**。这能减轻对 AI 失业的不安，降低企业引入的门槛。

### 巧思 9：与工业 IoT 的直接连接

借助 llmesh 的 MQTT / OPC-UA bridge，在制造业 / 计测 / 物理 / 工程 的现场，提供一条 **AI 直接接收现场数据并返回判断** 的路径。这是通用 LLM 无法触及的领域。

### 巧思 10：面向多人开发设想的认知 OS

10 个思考因子 + Multi-track Filter + Six Hats（CREAT-04）是用于 **即便在个人开发中也保持多重视角** 的机制。由于内置了「architect / critic / executor / auditor」四个角色，即使是一人开发也能防止认知偏差。

---

## 5. 今后的展望（三款产品共通）

### 短期（~3 个月）

- llive：MATH-02 形式验证 / CABT-01 forward hook
- llmesh：v1.6.0 OPC-UA + MQTT
- llove：F25 完成（E2E 联动）+ Creative Workbench

### 中期（~1 年）

- llive：ORG-FX Stage B（用 LoRA 做 llive 专用 adapter）→ Stage C（qwen2.5:14b → llive-7b 蒸馏）
- llmesh：v2.0 P2P mesh（技术引入金子勇 EDLA + Winny 的局部学习规则）
- llove：F18 Rust 移植（ratatui 并行 → 完全 Rust）

### 长期（~3 年）

- llive：Stage D/E（非 Transformer / Surprise-native pretraining）→ 论文化
- FullSense umbrella：在 v1.0.0 进行 PyPI rename（fullsense-* 系列）
- 三款产品集成 SaaS / 提供商业支持

---

## 6. 总结

**FullSense ™ = llmesh + llive + llove** 三款产品，同时提供：

- ✅ **完全 on-prem**（cloud LLM 无法触及的隐私领域）
- ✅ **结构化 work unit**（用 Brief API 排除含糊的委托）
- ✅ **内置 10 个思考因子**（作为认知 OS 的设计）
- ✅ **TRIZ 创造性引擎**（40 原理 + 矛盾矩阵）
- ✅ **Approval Bus + Ledger**（责任归属的持久化）
- ✅ **计算是确定性的**（排除交给 LLM 的误算）
- ✅ **形式验证 gate**（用 Z3 + Sympy 阻止公式幻觉）
- ✅ **HITL 工作台**（用 llove TUI 让人类进入判断回路）
- ✅ **工业 IoT 连接**（用 MQTT / OPC-UA 直连现场数据）
- ✅ **多语言支持**（ja / en / zh / ko）
- ✅ **Apache-2.0 + Commercial dual**（OSS 与商用兼容）

它们作为独立 OSS 也各有价值，但 **组合起来便成为「LLM 周边一切齐备的认知 OS 生态系统」**。

如有疑问、合作或商用意向，欢迎通过 GitHub Issues 或 Twitter / X（@puruyan）随时联系。

---

## 相关链接

- llmesh：<https://github.com/furuse-kazufumi/llmesh>
- llive：<https://github.com/furuse-kazufumi/llive>
- llove：<https://github.com/furuse-kazufumi/llove>
- FullSense umbrella 门户：<https://github.com/furuse-kazufumi/fullsense>
- llmesh-suite（one-shot installer）：<https://github.com/furuse-kazufumi/llmesh-suite>

### 同日文章（2026-05-17）

- 面向技术者的详细（11 篇）：[docs/articles/2026-05-17/](.)
- 面向技术者的整合：[QIITA_SUMMARY.md](./QIITA_SUMMARY.md)
- 面向非工程师的整合：[QIITA_GENERAL.md](./QIITA_GENERAL.md)
- 开发历程（仅 llive 5 天）：[12_dev_history.md](./12_dev_history.md)
- **本文（llmesh + llove + llive 整合历程 + 设计 + 差异化 + 普及）**

### 用于 LinkedIn 投稿（与本文同一文件夹，多语言版本）

- [LinkedIn_SUMMARY_jp.md](./LinkedIn_SUMMARY_jp.md) / `_en.md` / `_zh.md` / `_ko.md`
- [LinkedIn_GENERAL_jp.md](./LinkedIn_GENERAL_jp.md) / `_en.md` / `_zh.md` / `_ko.md`
- [LinkedIn_HISTORY_jp.md](./LinkedIn_HISTORY_jp.md) / `_en.md` / `_zh.md` / `_ko.md`

---

> 三款产品 = 一个世界观 = **「运行在家用 PC 上、有责任感、爱管闲事的 AI 生态系统」**

---

# 한국어

# llmesh → llove → llive — FullSense 3개 제품의 개발 이력・설계 콘셉트・차별화・보급 전략 (2026-05-17 시점)

저자: **후루세 카즈후미(puruyan)**

## 들어가며 — 왜 3개 제품으로 하나의 세계관인가

저(후루세 카즈후미 / puruyan)는 **FullSense ™** 라는 umbrella 브랜드 아래 3개의 OSS 프로젝트를 병행 개발하고 있습니다:

| 제품 | 역할 | PyPI | GitHub |
|---|---|---|---|
| **llmesh** | secure LLM hub (on-prem MCP server) | `llmesh` | <https://github.com/furuse-kazufumi/llmesh> |
| **llive** | self-evolving modular memory LLM framework | `llmesh-llive` | <https://github.com/furuse-kazufumi/llive> |
| **llove** | TUI dashboard / HITL workbench | `llmesh-llove` | <https://github.com/furuse-kazufumi/llove> |

모두 **Apache-2.0 + Commercial dual-license**. 셋은 독립 OSS이면서도, 조합하면 「**가정용 PC에서 동작하는, 책임감 있고, 참견 잘하는 AI 에코시스템**」이 됩니다.

본 글은 **3개 제품의 출범부터 오늘(2026-05-17)까지의 역사**, **설계 콘셉트**, **경쟁사와의 차별화**, **많은 사람에게 써 보게 하기 위한 궁리** 를 하나로 정리한 것입니다.

---

## 1. 개발 이력 — 3개 제품의 시계열

### llmesh (최고참)

| 시기 | 내용 |
|---|---|
| ~2026-05-09 이전 | 출범. secure LLM hub + 산업 IoT 연동 |
| 2026-05-09 | v1.5.0 완료 — MTEngine + XbarRChart + CUSUMChart + CLI 통합 |
| 2026-05-14 | llmesh-suite v0.2.0 (3개 제품용 one-shot installer) |
| 다음 | v1.6.0 OPC-UA + MQTT (llive와 연결 예정) |

설계 사상: **「LLM을 허브로 사용한다」** — 여러 LLM(OpenAI / Anthropic / Ollama 등)을 통합하고 MCP 프로토콜로 배포. SPC(통계적 공정 관리)를 내장하고 산업 IoT에 직접 접속.

### llove (TUI HITL 워크벤치)

| 시기 | 내용 |
|---|---|
| 2026-05-09 | v0.2.2 PyPI 최초 공개 (llmesh-llove) |
| 2026-05-09 | F17 / F21 / F16 chess (216 PASS, 미 push) |
| 2026-05-09 | F15 브라우저급 표시 (Markdown / SVG / Mermaid / 접기) |
| 2026-05-09 | F16 멀티게임 LLM 대국 아레나 (chess/go/mahjong/poker/...) |
| 2026-05-10 | F22 테트리스 데모 (LLM × 시뮬레이션 환경) |
| 2026-05-10 | F23 PowerShell 호환 셸 / F24 Claude Code 통합 |
| 2026-05-12 | F25 연동 기반 (llove ↔ llmesh ↔ llive 를 MCP 경유로 잇는 shim) |
| 2026-05-14 | F25 audience demo 다듬기 (다국어화 + 상업 가치 소구) |

설계 사상: **「사람이 AI를 감독하기 위한 TUI」** — Textual 기반. SVG / Mermaid / Markdown을 터미널에서 재현하고, 데모를 다수 준비하여 **「움직임으로 매료시키는」** 것으로 인지를 확대. F16 아레나는 LLM끼리의 대국이라는 시각적으로 화려한 기능으로 SNS 확산성을 노립니다.

### llive (오늘로 5일째)

| 시기 | 내용 |
|---|---|
| 2026-05-13 | 출범, v0.1.0 — Phase 1 MVR (49 tests) |
| 2026-05-13 밤 | v0.2.0 — Phase 2 Adaptive (308 tests) |
| 2026-05-14 | v0.3 → v0.4 → v0.5 — Phase 3/4/5 (444 tests) |
| 2026-05-16 | v0.6.0 — 9 axes skeleton + Apache 2.0 + FullSense umbrella (970 tests) |
| 2026-05-17 (오늘) | Brief API + 32건 요건 + 4종 벤치 + 14개 기사 (1014 tests) |

설계 사상: **「LLM 본체가 아니라, LLM 주위에 덮어씌우는 인지 OS」** — 4층 메모리 + 6 stage Loop + Approval Bus + TRIZ + 10 사고 인자. 자세한 내용은 같은 날 기사 [09 llive 구조 독자성 8요소](./09_llive_structure_originality.md) 참조.

### 3개 제품이 교차하는 곳

```
                    [外部 LLM 提供元]
                Qwen / Llama / Mistral / GPT / Claude / Gemini
                              ↓
                         [llmesh]
                    secure LLM hub
                  MCP / OPC-UA / MQTT
                ↗      ↓       ↘
            llive    llove    産業 IoT
        認知 OS   TUI HITL   sensor bridge
            ↓      ↓
        Brief / 4 層メモリ / Approval Bus
            ↓
          実 use case (lldesign / lltrade / 計画中の llcad/lleda/llchip)
```

---

## 2. 설계 콘셉트 — 3개 제품 공통의 철학

### 철학 1: Local 환경이야말로 AI의 본래 거처

cloud LLM(GPT / Claude / Gemini / Perplexity)은 편리하지만, **개인정보・기업기밀・의료데이터・가족의 대화・산업 IoT 센서 데이터** 를 외부로 보내는 것은 본래 있어서는 안 될 영역. FullSense 3개 제품은 **완전 on-prem 동작** 을 최우선으로 설계.

memory 규칙: `feedback_llive_measurement_purity` — llive 벤치는 「on-prem only」「cloud와 혼재 금지」.

### 철학 2: 책임 소재를 architecture 레벨로 끌어들인다

- **llive Approval Bus** — 위험한 동작은 반드시 사람의 승인을 거치고, SQLite ledger에 영속화, replay 가능
- **llmesh SPC** — 통계적 공정 관리로 AI의 동작을 가시화하고, 이상을 조기 검출
- **llove TUI** — 사람이 AI의 판단 루프에 반드시 들어간다 (HITL 워크벤치)

3개 제품 모두 「**AI에게 맡기지 않는다**」는 설계.

### 철학 3: 다측면의 사고를 구조화

llive의 **10 사고 인자(구조화 / 재구성 / 폐루프 / 자기확장 / 불확실성 / 탐색 / 정합 / 내력 / 다관점 / 현실접속)** 는, 심리의 심층(YouTube)에서 추출한 인간 사고의 버릇. 이것을 LLM에게 갖게 함으로써, AI를 「단순한 문자 생성기」에서 「사고의 발판을 가진 지성」으로 확장.

### 철학 4: TRIZ로 창조를 구조에 끌어들인다

llive 내장의 **TRIZ 40 원리 + 39×39 모순 매트릭스 + ARIZ + 9 화법** 은, 자기진화의 mutation policy로서 동작. 「재미있는 안을 낸다」가 아니라 「**모순을 발견하고, 원리에 따라 체계적으로 해결**」한다.

### 철학 5: Honest disclosure를 연구의 핵심으로

memory 규칙: `feedback_benchmark_honest_disclosure` (2026-05-17 확립) — 자사가 이상하게 빠른 결과가 나오면, 이긴 기분이 들기 전에 반드시 내역을 의심한다. 실패를 지우지 않고, 교훈으로 남긴다.

### 철학 6: 패밀리로 만든다

llmesh / llive / llove는 **독립 OSS이면서도, 조합하면 하나의 세계관**. 이것은 PyPI 단독 패키지로 완결할 수 있는 Wolfram Alpha나 ChatGPT와의 근본적인 차이. **사용자는 필요한 부분만 채택** 할 수 있습니다.

---

## 3. 차별화 요소 — 경쟁사와의 위치 정립

### vs ChatGPT / Claude / Gemini / Perplexity (cloud LLM)

| 축 | cloud LLM | FullSense |
|---|---|---|
| on-prem | ❌ | ✅ (완전히 가정용 PC에서 동작) |
| 개인정보 보호 | ❌ (외부 송신) | ✅ (송신 제로) |
| 감사 로그 | ❌ | ✅ (SQLite ledger + SHA-256 chain) |
| 재해 시 | ❌ (네트워크 단절로 정지) | ✅ (Local에서 계속 동작) |
| 월 비용 | ⚠️ ($20~200/월) | ✅ (전기료뿐) |
| 계산 정밀도 | ⚠️ (LLM에 맡겨 오산) | ✅ (내장 계산기 + 단위 차원 해석) |
| 구조화 work unit | ❌ | ✅ (Brief API) |
| HITL 워크벤치 | ❌ | ✅ (llove TUI) |

### vs LangChain / LlamaIndex / AutoGen / CrewAI (Agent framework)

| 축 | 기존 Agent framework | FullSense |
|---|---|---|
| Agent loop | ✅ (chain / multi-agent) | ✅ (6 stage Loop + Multi-track Filter) |
| memory | ✅ (vector DB) | ✅ + 4층 메모리 (semantic/episodic/structural/parameter) |
| HITL | ⚠️ (CLI prompt 정도) | ✅ (llove TUI 워크벤치) |
| HITL audit | ❌ | ✅ (Approval Bus + ledger) |
| 형식 검증 | ❌ | ✅ (Z3 / Sympy 통합) |
| 인지 인자 명시 분해 | ❌ | ✅ (10 사고 인자 + COG-FX) |
| TRIZ 내장 | ❌ | ✅ (40 원리 + ARIZ + 9 화법) |
| 산업 IoT 접속 | ❌ | ✅ (llmesh MQTT / OPC-UA) |
| TUI HITL 워크벤치 | ❌ | ✅ (llove) |

### vs Wolfram Alpha (수학・과학 계산)

| 축 | Wolfram Alpha | FullSense (MATH vertical) |
|---|---|---|
| 수식의 정확성 | ✅ | ✅ (Z3 + Sympy 통합) |
| 단위 차원 해석 | ✅ | ✅ (SI 7 기본 단위) |
| 물리 상수 | ✅ | ✅ (CODATA + NIST) |
| 가격 | 유료 (cloud) | 무료 (Apache 2.0) |
| Local 동작 | ❌ | ✅ |
| OSS | ❌ | ✅ |
| LLM 통합 | ⚠️ | ✅ (BriefGrounder로 자연스럽게) |
| 감사 로그 | ❌ | ✅ (BriefLedger) |

### vs MemGPT / LongMem (memory framework)

| 축 | MemGPT / LongMem | llive |
|---|---|---|
| 계층 메모리 | ✅ | ✅ (4층 + phase transition + 서명 zone) |
| Bayesian Surprise | ❌ | ✅ (FR-21) |
| 형식 검증 gate | ❌ | ✅ (EVO-04 Z3) |
| HITL | ❌ | ✅ (llove TUI) |
| 산업 IoT | ❌ | ✅ (llmesh) |
| TRIZ mutation policy | ❌ | ✅ |

---

## 4. 많은 사람에게 써 보게 하기 위한 궁리

### 궁리 1: Quick Start 30초

```bash
# llive
py -3.11 -m pip install llmesh-llive
llive-demo                              # 10 シナリオを順番に再生

# llove
py -3.11 -m pip install llmesh-llove
llove                                   # TUI 起動

# 3 製品まとめて
py -3.11 -m pip install llmesh-suite
llmesh-suite install                    # one-shot で全部
```

「번거로운 설정 없이 동작하는 체험」을 최우선.

### 궁리 2: Optional extras 설계

faiss / torch / sentence-transformers / Rust 확장 등의 **무거운 의존은 optional**. 기본 기능은 stdlib + numpy 만으로 동작시킬 수 있기 때문에, Windows / Mac / Linux / 저사양 PC에서도 동작.

```bash
# 最小
pip install llmesh-llive

# torch を使いたい
pip install 'llmesh-llive[torch]'

# 全部
pip install 'llmesh-llive[all]'
```

### 궁리 3: 다국어 내레이션

llove demo는 **ja / en / zh / ko 4개 언어** 내레이션 대응:

```bash
llove-demo --lang en      # 英語
llove-demo --lang zh      # 中国語
llove-demo --lang ko      # 韓国語
```

LinkedIn / Qiita / note에의 투고도 다국어판을 준비 (본 글과 같은 폴더 안의 `LinkedIn_*_jp.md` / `_en.md` / `_zh.md` / `_ko.md` 참조).

### 궁리 4: 다측면의 기사를 매일

memory 규칙: `feedback_daily_articles_policy` — 기술 설계 / 구현 보고 / 벤치 / honest disclosure / 전략 / 철학 / 업계 비교 / 인지과학 / TRIZ / 에코시스템 / 사용자 경험 / 미래 예측 / 교훈 의 13 측면에서 매일 기사를 만든다.

기술자용(`QIITA_SUMMARY.md`)과 비엔지니어용(`QIITA_GENERAL.md`)과 개발 이력(`QIITA_HISTORY.md` = 본 글)을 매일 병행.

### 궁리 5: 데모를 SNS 확산성으로 설계

llove F16 멀티게임 LLM 대국 아레나(chess / go / mahjong / poker)나 F22 테트리스 데모는, **움직임으로 매료시키고, 반복 재생되고, 상업 가치가 전해지는** 것을 최우선으로 설계. LinkedIn / X / YouTube에서 확산되기 쉽다.

memory 규칙: `project_f25_demo_polish` — 데모는 「채용 퍼널 선두」「움직임으로 매료」「상업 가치 소구」를 필수 요건으로.

### 궁리 6: 인지 OS라는 포지셔닝

「llive는 LLM이 아니라 LLM을 내장하는 인지 OS」「FullSense는 AI를 능숙하게 다루는 비서 에코시스템」이라고 재프레이밍. 이로써:

- 기존 LLM(Qwen / Llama / Mistral)과의 경쟁 관계를 회피
- 「단독으로 쓸 거라면 ChatGPT로 충분」이라는 비판에 대항
- 「**Qwen을 Local에서 안전하게 책임지고 쓰려면 FullSense가 최단 경로**」

### 궁리 7: dual-license로 상업 이용을 촉진

- **Apache-2.0** (OSS 개발자용)
- **Commercial license** (기업의 사내 이용용, 상업 지원 포함)

양쪽 모두 제공함으로써, 연구도 상업도 같은 codebase에서 진행할 수 있다.

### 궁리 8: HITL 워크벤치로 AI 실업의 불안을 완화

llove TUI에서는 AI가 「이걸로 괜찮은가요?」라고 물어 오고, 사람이 승인 / 기각 / 수정 가능. **완전 자동이 아니라, 사람이 반드시 판단 루프에 들어가는** 설계. 이것은 AI 실업의 불안을 줄이고, 기업 도입의 허들을 낮춘다.

### 궁리 9: 산업 IoT와의 직접 접속

llmesh의 MQTT / OPC-UA bridge에 의해, 제조업 / 계측 / 물리 / 공학 의 현장에서 **AI가 현장 데이터를 직접 받고, 판단을 돌려주는** 경로를 제공. 범용 LLM으로는 도달할 수 없는 영역.

### 궁리 10: 다인원 개발을 상정한 인지 OS

10 사고 인자 + Multi-track Filter + Six Hats(CREAT-04)는, **개인 개발에서도 복수의 관점을 유지하기** 위한 구조. 「architect / critic / executor / auditor」의 4 역할이 내장되어 있으므로, 1인 개발에서도 인지의 편향을 막을 수 있다.

---

## 5. 앞으로의 전망 (3개 제품 공통)

### 단기 (~3개월)

- llive: MATH-02 형식 검증 / CABT-01 forward hook
- llmesh: v1.6.0 OPC-UA + MQTT
- llove: F25 완성 (E2E 연동) + Creative Workbench

### 중기 (~1년)

- llive: ORG-FX Stage B (LoRA로 llive 전용 adapter) → Stage C (qwen2.5:14b → llive-7b 증류)
- llmesh: v2.0 P2P mesh (카네코 이사무 EDLA + Winny의 국소 학습 규칙을 기술 도입)
- llove: F18 Rust 이식 (ratatui 병행 → 완전 Rust)

### 장기 (~3년)

- llive: Stage D/E (Transformer 이외 / Surprise-native pretraining) → 논문화
- FullSense umbrella: v1.0.0에서 PyPI rename (fullsense-* 시리즈)
- 3개 제품 통합 SaaS / 상업 지원 제공

---

## 6. 정리

**FullSense ™ = llmesh + llive + llove** 의 3개 제품으로, 다음을 동시에 제공:

- ✅ **완전 on-prem** (cloud LLM으로는 도달할 수 없는 프라이버시 영역)
- ✅ **구조화 work unit** (Brief API로 모호한 의뢰를 배제)
- ✅ **10 사고 인자 내장** (인지 OS로서의 설계)
- ✅ **TRIZ 창조성 엔진** (40 원리 + 모순 매트릭스)
- ✅ **Approval Bus + Ledger** (책임 소재의 영속화)
- ✅ **계산은 결정론적** (LLM에 맡긴 오산을 배제)
- ✅ **형식 검증 gate** (Z3 + Sympy로 수식 환각을 멈춘다)
- ✅ **HITL 워크벤치** (llove TUI로 사람이 판단 루프에)
- ✅ **산업 IoT 접속** (MQTT / OPC-UA로 현장 데이터 직결)
- ✅ **다국어 대응** (ja / en / zh / ko)
- ✅ **Apache-2.0 + Commercial dual** (OSS + 상업 양립)

이것들은 개별 OSS로도 가치가 있지만, **조합하면 「LLM의 주변 전부가 갖춰진 인지 OS 에코시스템」** 이 됩니다.

질문・협업・상업 이용은 GitHub Issues 또는 Twitter / X (@puruyan)로 부담 없이.

---

## 관련 링크

- llmesh: <https://github.com/furuse-kazufumi/llmesh>
- llive: <https://github.com/furuse-kazufumi/llive>
- llove: <https://github.com/furuse-kazufumi/llove>
- FullSense umbrella 포털: <https://github.com/furuse-kazufumi/fullsense>
- llmesh-suite (one-shot installer): <https://github.com/furuse-kazufumi/llmesh-suite>

### 같은 날 기사 (2026-05-17)

- 기술자용 상세 (11개): [docs/articles/2026-05-17/](.)
- 기술자용 통합: [QIITA_SUMMARY.md](./QIITA_SUMMARY.md)
- 비엔지니어용 통합: [QIITA_GENERAL.md](./QIITA_GENERAL.md)
- 개발 이력 (llive 단독 5일): [12_dev_history.md](./12_dev_history.md)
- **본 글 (llmesh + llove + llive 통합 이력 + 설계 + 차별화 + 보급)**

### LinkedIn 투고용 (본 글과 같은 폴더, 다국어판)

- [LinkedIn_SUMMARY_jp.md](./LinkedIn_SUMMARY_jp.md) / `_en.md` / `_zh.md` / `_ko.md`
- [LinkedIn_GENERAL_jp.md](./LinkedIn_GENERAL_jp.md) / `_en.md` / `_zh.md` / `_ko.md`
- [LinkedIn_HISTORY_jp.md](./LinkedIn_HISTORY_jp.md) / `_en.md` / `_zh.md` / `_ko.md`

---

> 3개 제품 = 하나의 세계관 = **「가정용 PC에서 동작하는, 책임감 있고, 참견 잘하는 AI 에코시스템」**
