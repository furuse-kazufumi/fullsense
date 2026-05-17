---
title: "1 日で要件 32 件追加 + Brief API + COG-FX + MATH 実装まで — llive 開発記 2026-05-17"
tags: LLM,Agent,OnPrem,Ollama,Python
---

# 1 日で要件 32 件追加 + Brief API + COG-FX + MATH 実装まで — llive 開発記 2026-05-17

著者: **古瀬 和文（ぷるやん）**

## はじめに

2026-05-17 の 1 セッション (Claude Opus 4.7 1M context, ccr 経由) で **自己進化型 LLM フレームワーク [llive](https://github.com/furuse-kazufumi/llive)** に対し以下を達成しました:

| 種別 | 件数 | 内容 |
|---|---|---|
| 要件 (FR) 追加 | **32 件** | v0.7-MATH 8 / v0.8-CABT 7 / v0.9-CREAT 5 / v1.0-COG-FX 4 / v2.0-ORG-FX 8 |
| 実装 (LoC) | ~2 200 行 | Brief API end-to-end / Grounder / Governance / Trace Graph / MATH 単位&計算 |
| テスト追加 | **+78 件** | 936 → **1014 PASS / 0 fail / 0 regression** |
| ベンチ 4 種 | 15 + 12 + 10 + 10 セル | progressive matrix / fair bench / quiz Debug / quiz Release |
| 公開記事 | **11 本** | [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17) |
| GitHub push | 2 リポジトリ | llive `349a234` / fullsense `cb346aa` |

llive は **OSS LLM (Qwen / Llama / Mistral) を内蔵する「認知 OS」** という positioning で、4 層メモリ + 6 stage Loop + Approval Bus + TRIZ 40 原理 + 10 思考因子 を統合する研究開発フレームワークです。

本記事は同日 11 本の個別記事をまとめた目次的サマリ。詳細は各章末のリンクから個別記事へ。

---

## 1. Brief API end-to-end (LLIVE-001/002 全 7 step)

外部クライアント (lldesign / lltrade / 計画中の llcad/lleda/llchip) から構造化 work unit を渡せる **Brief API** を 1 セッションで実装完了 (設計見積 5 日を 1 日で完走):

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str
    goal: str
    constraints: tuple[str, ...] = ()
    tools: tuple[str, ...] = ()
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    epistemic_type: EpistemicType = EpistemicType.PRAGMATIC
```

CLI / MCP / Ledger / Approval gate / Tool whitelist を含むフルパス。**append-only JSONL ledger** に全段階を記録、replay 可能。

### Progressive validation matrix (5×3 = 15 セル)

xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b} を on-prem only で実走:

| model | xs (cold) | s | m | l | xl (timeout) |
|---|---|---|---|---|---|
| llama3.2:3b | 8.9 s | 44 s | 89 s | 458 s | 1202 s ⌛ |
| qwen2.5:7b | 59 s | 94 s | 122 s | 723 s | 1202 s ⌛ |
| qwen2.5:14b | 122 s | 122 s | 122 s | 1202 s⌛ | 1202 s ⌛ |

- **Brief API overhead < 1 %** (LLM-only wall / Total wall > 99.8 %)
- **全 15 セル decision=`note`** → loop は token 圧力に対し完全 stable

詳細: [01_brief_api_progressive.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md)

---

## 2. 心理の深層 10 思考因子で整理する llive 思考層 — 9/10 実装済

「心理の深層」YouTube から抽出した 10 思考因子を llive 既存 FR にマッピング:

| 因子 | llive 実装 |
|---|---|
| **構造化** | Brief constraints + Salience/Curiosity gate |
| 再構成 | TRIZ FR-23〜27 (40 原理) |
| **閉ループ** | BriefRunner submit→plan→approval→tool→outcome |
| 自己拡張 | 4 層メモリ + RAD + tools + MATH-08 |
| **不確実性** | FR-21 BayesianSurpriseGate + COG-01 Triple Output |
| 探索 | EVO-* (Z3 + Failed Reservoir) |
| **整合** | Approval Bus + EVO-04 Z3 + COG-02 Scoring |
| **来歴** | Provenance + Ledger + SEC-03 + COG-03 TraceGraph |
| 多視点 | Multi-track Filter A-1.5 |
| 現実接続 | (Phase 4 INT-01〜04 計画中) |

**v1.0 必須 5 因子 (太字) はすべて実装済**。残るは現実接続 (Phase 4 IoT) と多視点強化 (COG-04 + CREAT-04)。

詳細: [02_cognitive_factors.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md)

---

## 3. 数学・単位に強い AI への第一歩 — MATH-01/08

llive の最初の vertical specialisation は「数学・単位特化 AI」。汎用 LLM が苦手な (a) 記号操作の幻覚 (b) 単位次元の取り違え (c) 数値計算の error propagation を、**「LLM に計算させない」決定論的サイドカー** で克服:

```python
from llive.math import Quantity, parse_unit, UnitMismatchError, SafeCalculator

# 単位次元解析 — 「5 m/s + 3 s」を必ず止める
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t  # ✓ dimensions = m

# 内蔵計算エンジン — LLM ではなく決定論的に
calc = SafeCalculator()
r = calc.evaluate("(2.5 * 7.8) / 0.3")  # value=65.0 exact
```

`SafeCalculator` は AST visitor + whitelist (math/statistics 28 関数 + π/e/τ 定数) で、`__import__('os').system('rm')` のような攻撃も attribute access 段階で reject。

詳細: [03_math_vertical.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md)

---

## 4-6. 設計予告 3 本 (実装は次セッション以降)

### CABT - Cognitive-aware Transformer Block (7 アプローチ)

Transformer の `softmax(QK^T)·V` を **「参照ベース選択 + metadata 集約」** に置換する設計。HF transformers の `forward_hook` で **重み凍結のまま** attention 出力に metadata bias を加える。6 列 metadata (provenance_id / trust_score / epistemic_type / timestamp_norm / source_domain_id / surprise_score)。

詳細: [04_next_cabt_block_design.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md)

### CREAT - 創造プロセス層 (KJ法 × MindMap × TRIZ × Six Hats)

人間の創造プロセス (拡散 → 構造化 → 矛盾解決 → 多視点検証 → 構造化変換) を BriefRunner 前段の「拡散層」として実装。最終的に Brief 1 件 → 自動生成された REQUIREMENTS.md を出力する経路。

詳細: [05_next_creat_kj_mindmap.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md)

### MATH-02 - 形式検証ゲート (Z3 + Sympy)

LLM 出力の数式を AST 化 → Sympy で simplify → 差分を flag → Z3 で satisfiability check。`(x+1)² = x² + 2x` のような記号幻覚を必ず止める。EVO-04 (既存 Z3) を数式版に拡張。

詳細: [06_next_math02_formal_gate.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md)

---

## 7. Fair benchmark の罠と honest disclosure

最初のベンチで「llive 4/4 OK 134-184ms」という結果が出たが、ユーザー指摘「変に高速ですね、何か応答におかしな部分はないですか？」を受けて再検査:

### 確認された異常 3 件

1. **llive 側が LLMBackend を attach していない** → `_inner_monologue` が template fallback (rule-based) に落ち、brief の最初 120 文字だけ thought.text に挿入
2. **`chars` メトリクスが JSON 全長を測っている** → llive 884 chars 同一は「同じ JSON 構造を吐いたから」
3. **134-184ms は subprocess RTT + JSON serialize** → LLM 推論レイテンシではない

### 修正後の fair 再走

`bench_run.py::run_llive` を **LLMBackend (ollama:llama3.2) attach 版**に修正:

| brief | llive (+llama3.2:3b) | ollama 直叩き | perplexity |
|---|---|---|---|
| b1 | **32 750 ms** | 12 423 ms | 2 411 ms |
| b2 | **50 936 ms** | 13 024 ms | 3 591 ms |
| b3 | **43 787 ms** | 19 610 ms | 2 104 ms |
| b4 | **43 163 ms** | 21 936 ms | 6 162 ms |

llive (LLM attached) は ollama 直叩きの **2-4 倍遅い** — `build_llm_prompt` がブリーフを `_inner_monologue` 用にラップして長文化させるため。

**結論**: llive の付加価値は速度ではなく構造 (ledger / approval / governance / grounding / 6 stage trace)。速度だけで判断するなら ollama 直叩きの方が良い。

教訓: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

詳細: [07_bench_results.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md)

---

## 8. Quiz bench — Debug vs Release × mean/stdev

`bench_quiz.py` に **mean / stdev 統計列**を追加し、`llama3.2:3b` × {debug, release} × 10 quiz で計測:

| mode | passed | partial mean | partial stdev | ms mean | ms stdev |
|---|---|---|---|---|---|
| Debug | 6/10 | 0.550 | 0.497 | **22 343** | 5 790 |
| Release | 7/10 | 0.650 | 0.474 | **22 750** | 8 356 |

### 観察

- **Debug overhead は wall time +1.8 % で実質ゼロ** — debug=True を常時 ON でも性能ペナルティなし
- 正答率 (6/10 vs 7/10) は確率変動の範囲 (二項検定で p > 0.5)
- ms stdev が release で大きい (LLM 推論時間が問題依存で変動)

### 次回改善

- **N ≥ 30** で各 model 評価 (現在 N=10)
- 複数 model 並列 (llama3.2:3b / qwen2.5:7b / qwen2.5:14b)
- seed 固定で再現性確保
- LLM-as-judge での 2 次採点

詳細: [08_quiz_bench_debug_vs_release.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md)

---

## 9. llive の構造は LLM として独自か？ — 8 要素の点検

ユーザーの問い: 「llive の構造って、LLM として独自の構造になっていってますか？」

### 8 つの差別化要素

1. **Decoder-only LLM コアは凍結 + 周辺で能力拡張** (LoRA / adapter の延長線だが、重み凍結を最優先で replay 可能 / monitorable に)
2. **4 層メモリの責務分離** (semantic / episodic / **structural** / **parameter**) — 特に parameter memory (重みの差分を memory として扱う) が独自
3. **6 stage FullSense Loop** (Salience → Curiosity → Inner Monologue → Ego/Altruism → Action Plan → Output Bus) — 心理学的根拠付き
4. **Multi-track Filter Architecture A-1.5** (EpistemicType による track 切替) — FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC
5. **Approval Bus を Loop 内に組み込み** — HITL を architecture level に、SQLite ledger で replay 可
6. **TRIZ 40 原理を mutation policy として内蔵** (FR-23〜27) — 創造の代替案生成エンジン
7. **Cognitive Factor Framework (CFF) ― 10 因子を policy 分解** — planner / memory / critic / evolution / trace
8. **Brief API ― 構造化 work unit という primitives** — LangChain Chain / CrewAI Task と類似だが frozen + ledger + Approval built-in

### 結論

> **llive は LLM ではなく、LLM を内蔵する「認知 OS」**

8 要素の組合せ × 役割分離 × 心理因子マッピングは LangChain / AutoGen / MemGPT / Self-Refine / AutoML-Zero のいずれにも一致しない。

詳細: [09_llive_structure_originality.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md)

---

## 10. Qwen 依存から離脱する 5 段階ロードマップ (ORG-FX 戦略 A)

ユーザー観察: 「差別化されていないと研究の価値がない。普及している AI を使った方がマシってなりそう」

```
Stage A (短期, 〜3 ヶ月) — LLM コア凍結、周辺差別化を最大化
   ↓
Stage B (中期 1, 3〜6 ヶ月) — LoRA で llive 専用 adapter
   ↓
Stage C (中期 2, 6〜12 ヶ月) — Distillation: qwen2.5:14b → llive-7b
   ↓
Stage D (長期 1, 1〜2 年) — Transformer block を memory-coupled に置換
   ↓
Stage E (長期 2, 2〜3 年) — Transformer 以外 (Mamba / RWKV / Hyena) + Surprise-native pretraining
```

新規 ORG-01〜08 (8 件) を REQUIREMENTS.md v2.0-core に追加。3 つの metric (AOS / LCIR / Replaceability Test) で「Qwen との距離」を測る。

詳細: [10_qwen_divergence_strategy.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md)

---

## 11. Qwen と相互補完する llive — Local 環境で 5 隙間を埋める (戦略 B)

「相互補完の関係を目指すのもあり。もともと llive は Local 環境で動かす想定のもの。隙間をうまく補間できるといい」というユーザー観察を反映した二層戦略:

```
路線 1: 常設の補完戦略 (Local 環境特化)
       └ Qwen / Llama が進化しても不変の価値
路線 2: 研究としての独自化 (ORG-FX 5 段階)
       └ 中長期で研究価値を持続
```

### 5 つの隙間

| 隙間 | llive 補完 |
|---|---|
| 数値計算・記号操作・形式検証 | MATH-01 / 02 / 05 / 08 |
| 長期記憶・経験再生 | 4 層メモリ + Failed Reservoir + Ledger |
| 行動監査・責任所在 | Approval Bus + Governance + SHA-256 chain |
| 認知構造・多視点・矛盾解決 | CREAT (KJ/MindMap/Six Hats) + TRIZ |
| Local on-prem 制約 | 完全 on-prem + Quarantined Zone + llmesh sensor bridge |

cloud LLM (GPT/Claude/Gemini/Perplexity) では **絶対に再現できない領域**。

### 再フレーミング

> 「単独で使うなら Qwen で十分」 → **「Qwen を Local 環境で安全に責任を持って使うなら llive が最短経路」**

詳細: [11_complementary_with_qwen.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md)

---

## まとめ — 1 セッションの成果

### 実装

- **Brief API** (LLIVE-001/002) end-to-end / S1 BriefGrounder / MATH-01/08 / COG-01/02/03
- llive テスト: **1014 PASS / 0 fail / 0 regression**

### 要件追加 (REQUIREMENTS.md)

- v0.7-vertical MATH 8 件 (内 MATH-08 が差別化軸最大)
- v0.8 CABT 7 件 (Transformer ブロック高度化)
- v0.9 CREAT 5 件 (KJ法 / MindMap / Six Hats / Synectics)
- v1.0-frame COG-FX 4 件 (10 思考因子マッピング)
- v2.0-core ORG-FX 8 件 (Qwen 依存からの離脱 5 段階)
- **総 100 件、マッピング完備**

### ベンチマーク

- progressive matrix 5×3 = 15 セル (xs/s/m/l/xl × 3 models)
- fair re-bench 4×6 = 24 セル
- quiz bench debug + release × 10 = 20 セル
- **重要な教訓**: 「ベンチで自社が異常に速かったら、まず内訳を疑う」

### 戦略の二層構造

1. **常設の補完戦略** (Local 環境で 5 隙間補完) — cloud LLM が進化しても不変
2. **研究としての独自化** (ORG-FX 5 段階) — Stage A → B → C → D → E

### 公開資料

`D:/projects/fullsense/docs/articles/2026-05-17/` 配下に 11 本 + 本記事 (QIITA_SUMMARY)。日付別ディレクトリで日々増えていく構造:

```
docs/articles/
  2026-05-17/   ← 本日
  2026-05-18/   ← 翌日以降の予定
  ...
```

### GitHub

- llive: <https://github.com/furuse-kazufumi/llive> (`349a234` push 済)
- fullsense (umbrella ポータル): <https://github.com/furuse-kazufumi/fullsense> (`cb346aa` push 済)
- llove (TUI HITL): <https://github.com/furuse-kazufumi/llove>
- llmesh (LLM hub): <https://github.com/furuse-kazufumi/llmesh>

すべて **Apache-2.0 + Commercial dual-license**。

## おわりに

llive は「LLM そのもの」ではなく「LLM を内蔵する認知 OS」として、Local 環境で 5 つの隙間を補完しつつ、中長期では LLM コア自体の独自化を計画的に進める設計です。1 日で要件 32 件 + 実装 1014 PASS + 公開記事 11 本という「ベンチで自社を疑う honest disclosure」も含む等身大の開発記録として残しました。

質問・指摘・改善提案は GitHub Issues または Twitter / X (@puruyan) までお願いします。

---

> 本記事は Claude Opus 4.7 (1M context) と GitHub Copilot 風に対話しながら執筆。実装と検証も同セッション内で完走。1 日でこの規模を進められるのは、認知 OS が思考の足場をしっかり作っているからこそ。
