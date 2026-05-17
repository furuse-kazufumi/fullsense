---
layout: default
title: "Qwen と相互補完する llive — Local 環境で『隙間』を埋める設計"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags: [llm, complementary, on-prem, local, qwen, llive, niche]
---

# Qwen と相互補完する llive — Local 環境で『隙間』を埋める設計

著者: 古瀬 和文（ぷるやん）

## TL;DR

- 前記事 [10]({{ '/articles/2026-05-17/10_qwen_divergence_strategy' | relative_url }}) で「Qwen から離脱する 5 段階」を提示したが、**完全離脱だけが path ではない**
- ユーザー観察 (2026-05-17): 「相互補完の関係を目指すのもあり。もともと llive は Local 環境で動かす想定のもの。隙間をうまく補間できるといい」
- llive の差別化軸を **「Qwen を置換」から「Qwen と相互補完」** に再フレーム
- Local 環境特有の隙間 5 領域 (計算 / 記憶 / 監査 / 認知構造 / オフライン) で llive が Qwen を補う設計

## 「離脱」vs「相互補完」の二択は両立する

実は前記事 10 の Stage A (短期、〜3 ヶ月) は **相互補完戦略** そのもの:

- LLM コアは凍結 (Qwen をそのまま使う)
- 周辺差別化を最大化 (CABT / MATH / CREAT)
- 「Qwen が苦手 → llive が決定論的に補完」

ただし Stage B〜E (中長期) は「独自化路線」。両者は **同時並走** が可能で:

```
        補完路線 (短期持続)        独自化路線 (中長期)
        ──────────────         ──────────────
        Stage A 維持              Stage B → C → D → E
        Qwen + llive               llive-7b → llive-mamba 等
        隙間補完                   完全独立
```

「Local 環境で隙間補完」を **常設のポジション** とし、その上に「研究路線として
独自化」を積む二層構造。

## llive が Qwen を補完する 5 つの「隙間」

### 隙間 1: 数値計算・記号操作・形式検証

| Qwen の弱点 | llive の補完 |
|---|---|
| `(2.5 * 7.8) / 0.3` を間違える | **MATH-08 SafeCalculator** (AST + 決定論) |
| `5 m/s + 3 s = 8` (次元誤り) | **MATH-01 SI 次元解析** |
| `(x+1)² = x² + 2x` (記号幻覚) | **MATH-02 Sympy 検算 + EVO-04 Z3** |
| CODATA 値の捏造 | **MATH-05 物理定数辞書** (grounded) |

LLM は「言語的に妥当な式」を出すのは得意だが「数学的に正しい式」は苦手。
llive が決定論的サイドカーとして補完する。

### 隙間 2: 長期記憶・経験再生

| Qwen の弱点 | llive の補完 |
|---|---|
| context window (32K-128K) の限界 | **4 層メモリ** (semantic / episodic / structural / parameter) |
| session を跨ぐ記憶不能 | **persistent memory** + provenance |
| 同じ間違いを繰り返す | **Failed Reservoir** (EVO-06) + Reverse-Evo Monitor (EVO-07) |
| 「自分が以前何を言ったか」忘れる | **append-only ledger** (BriefLedger / SqliteLedger) |

LLM は stateless。llive が memory layer として補完する。

### 隙間 3: 行動監査・責任所在

| Qwen の弱点 | llive の補完 |
|---|---|
| 危険な動作の architectural gate なし | **Approval Bus** + Policy + SQLite Ledger (C-1) |
| 出力責任の追跡困難 | **Provenance chain** + SHA-256 audit chain (SEC-03) |
| dangerous tokens (rm -rf 等) のフィルタなし | **GovernanceScorer** (COG-02, 4 軸 scoring) |
| 監査ログがエフェメラル | **persistent JSONL + replay** 可 |

LLM 単体ではコンプライアンス対応が困難。llive が監査基盤を提供。

### 隙間 4: 認知構造・多視点・矛盾解決

| Qwen の弱点 | llive の補完 |
|---|---|
| 視野狭窄 (最初の候補に引きずられる) | **CREAT-01 KJ法ノード** (拡散 ≥20 件強制) |
| 思考の浅さ (1 階層展開) | **CREAT-02 MindMap** (DFS depth=3) |
| 偏った楽観 | **CREAT-04 Six Hats** (cautious 観点強制) |
| 既存パターン依存 | **CREAT-05 Synectics** (異分野類比) |
| 矛盾を扱えない | **TRIZ 40 原理** (FR-23〜27) |

LLM の "思考の浅さ" を、llive の認知構造で補完する。

### 隙間 5: Local 環境特有の制約

これは llive の **設計コンセプトと完全一致**:

| Local 環境の特性 | llive の対応 |
|---|---|
| ネットワーク不在 | **完全 on-prem 動作** (Ollama / LM Studio / vLLM) |
| 個人データを外に出せない | **provenance + Quarantined Zone** (SEC-01) |
| 計測機器との直接接続 | **llmesh sensor bridge** (FR-19, MQTT/OPC-UA) |
| エッジ推論 (低スペック) | **MATH-08 等の決定論的層** (LLM を呼ばない) |
| プライバシー (家族の会話、医療情報) | **Local-only ledger** + クラウド送信ゼロ |
| 起動時間・通信遅延の制約 | **Brief API の overhead < 1 %** (実測済) |

cloud LLM (GPT / Claude / Gemini / Perplexity) では **絶対に再現できない領域**。
これが llive の **不変の差別化軸**。

## 「隙間補完」のメンタルモデル

```
        ┌─────────────────────────────────┐
        │  Qwen (汎用言語能力)              │
        │  ├ 言語流暢性 ★★★★★              │
        │  ├ 文章生成 ★★★★★               │
        │  ├ 多言語 ★★★★★                 │
        │  ├ 一般知識 ★★★★☆               │
        │  ├ 推論 ★★★★☆                  │
        │  └─ 数値計算 ★★☆☆☆ ← 隙間 ─┐  │
        └────────────────────────────┼───┘
                                     ↓
        ┌─────────────────────────────────┐
        │  llive (認知 OS + 補完層)         │
        │  ├ 数値計算 ★★★★★ (MATH-08)      │
        │  ├ 単位次元 ★★★★★ (MATH-01)      │
        │  ├ 形式検証 ★★★★★ (MATH-02)      │
        │  ├ 長期記憶 ★★★★★ (4 層メモリ)   │
        │  ├ 監査 ★★★★★ (Approval Bus)    │
        │  ├ 認知構造 ★★★★★ (CREAT/TRIZ)  │
        │  └ Local on-prem ★★★★★          │
        └─────────────────────────────────┘
```

Qwen は **言語能力** で強く、llive は **その隙間 (計算・記憶・監査・認知構造・Local)** で強い。両者を組み合わせると、cloud LLM 単独でも、ollama 単独でも到達できない領域に届く。

## 評価ベンチへの示唆

「llive vs Qwen」の **対立構図** で測ると、Qwen の言語能力 × llive の決定論的層が **同じ axis で競合** することになり不公平。

代わりに以下の **協調 axis** で測るべき:

- **Hybrid task score**: Qwen のみ vs llive (= Qwen + 決定論的補完層) の **総合スコア**
- **Niche task score**: Qwen が苦手なタスク (数値計算 / 単位 / 形式検証) で llive がどれだけ補えるか
- **Local capability**: ネットワークなしで完結する task の網羅率
- **Audit completeness**: 出力に対する trace coverage

これらは記事 08 で示した quiz bench のさらに上位の評価軸として、次回 (Phase 4
Production 後) に導入予定。

## 結論

llive の戦略は **二層構造**:

1. **常設の補完路線** (Local 環境特化 + 5 隙間補完): これは Qwen / Llama / Mistral / 等の OSS LLM が進化しても **不変の価値**
2. **研究としての独自化路線** (ORG-FX 5 段階): 中長期的に研究価値を持続

「普及している AI を使った方がマシ」と言われる懸念に対しては、**「llive を使う = Qwen を使う上で Local + 計算 + 監査 + 認知構造 を全部得られる」** という **複合価値** で答える。

「単独で使うなら Qwen で十分」かもしれない。しかし **「Qwen を Local 環境で安全に責任を持って使う」なら llive が最短経路**、というポジションを取る。

## 関連 ORG-FX 要件 (補完視点の再解釈)

| ORG-FX FR | 補完戦略での解釈 |
|---|---|
| ORG-06 Provenance-aware tokens | Qwen の token に llive の trust score を付与 |
| ORG-02 Memory-coupled inference | Qwen 推論時に llive memory を直接参照 |
| ORG-07 Approval-native decoding | Qwen 出力を llive Approval policy で filter |
| ORG-08 llive-specialized distillation | Qwen-shaped, llive-aware な小型 model |

つまり **ORG-* 要件は「Qwen との分離」だけでなく「Qwen との癒着」にも使える**。
どちらの方向に進むかは、各 Stage で再評価する。

## ソース

- 要件: `D:/projects/llive/.planning/REQUIREMENTS.md` v2.0-core ORG-FX (補完視点での再解釈)
- 関連記事: [10 — Qwen 依存から離脱する 5 段階](./10_qwen_divergence_strategy.md)
- 関連 memory:
  - `feedback_llive_measurement_purity` — Local + on-prem 純度ルール
  - `project_llive` — llive 全体 (Local 環境で動かす想定が明記)

## 同日の他公開資料

- [01]({{ '/articles/2026-05-17/01_brief_api_progressive' | relative_url }}) Brief API
- [02]({{ '/articles/2026-05-17/02_cognitive_factors' | relative_url }}) 10 思考因子
- [03]({{ '/articles/2026-05-17/03_math_vertical' | relative_url }}) 数学・単位
- [04-06]({{ '/articles/2026-05-17/README' | relative_url }}) 設計予告 3 本
- [07]({{ '/articles/2026-05-17/07_bench_results' | relative_url }}) fair bench
- [08]({{ '/articles/2026-05-17/08_quiz_bench_debug_vs_release' | relative_url }}) quiz bench
- [09]({{ '/articles/2026-05-17/09_llive_structure_originality' | relative_url }}) llive 独自性 8 要素
- [10]({{ '/articles/2026-05-17/10_qwen_divergence_strategy' | relative_url }}) Qwen 離脱 5 段階

---

> 完全置換だけが path ではない。Local 環境で 5 隙間を補完する llive は、Qwen が進化しても価値が落ちない。
