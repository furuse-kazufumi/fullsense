---
title: "llmesh → llove → llive — FullSense 3 製品の開発履歴・設計コンセプト・差別化・普及戦略 (2026-05-17 時点)"
tags: LLM 開発履歴 設計思想 オープンソース ローカル環境
---

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
