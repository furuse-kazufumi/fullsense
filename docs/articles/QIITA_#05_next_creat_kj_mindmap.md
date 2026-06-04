---
layout: default
title: "LLM × KJ法 × MindMap で要件定義を自動化する — CREAT 設計予告"
date: 2026-05-17
tags: [llm, agent, creative-thinking, kj-method, mindmap, triz]
draft: true
id: 0c6deb6f462843a71094
---

# LLM × KJ法 × MindMap で要件定義を自動化する — CREAT 設計予告

> **Status**: 設計予告。実装は v0.9 Phase 9 (CREAT-01〜05) で順次着手予定。
> 本記事はユーザー観察「人間の思考の流れは KJ法 / MindMap / TRIZ 等を経て
> 要件定義に入る」を技術設計に落としたもの。

## TL;DR

- 現在の LLM (GPT / Claude / Gemini) は **収束的**思考が得意 (input → answer) だが、**拡散的**思考は弱い
- 人間の創造プロセス: 拡散 (KJ法) → 構造化 (MindMap) → 矛盾解決 (TRIZ) → 多視点検証 (Six Hats) → 構造化変換 (要件 spec)
- llive にこのフルパスを **明示的な拡散層** として組み込み、Brief から要件 spec を自動生成する経路を作る
- 5 件の FR (CREAT-01〜05) として要件化、Phase 9 で段階実装

## 人間の思考フロー vs llive 思考層

```
[人間の思考]                          [llive の対応]
  Brief (問題定義)            ←→     Brief API (LLIVE-002, 実装済 2026-05-17)
       ↓
  KJ法 (拡散 + 親和)          ←→     CREAT-01 KJ法ノード (計画)
       ↓
  MindMap (構造化)            ←→     CREAT-02 MindMap ノード (計画)
       ↓
  TRIZ (矛盾解決)             ←→     既存 FR-23〜27 + CREAT-05 類比 (計画)
       ↓
  Six Hats (多視点検証)       ←→     CREAT-04 + EpistemicType (計画)
       ↓
  要件定義 (構造化変換)        ←→     CREAT-03 構造化変換 (計画)
       ↓
  実装                          ←→    BriefRunner.submit → FullSenseLoop (実装済)
```

## 5 つの FR

### CREAT-01: KJ法ノード

Brief を起点に拡散的にアイデア集合 (≥20 件) を **LLM mixture sampling** で生成。各アイデアを embedding clustering で親和グループ化し、グループ命名と関係線を ledger に記録。

```python
# 設計案
from llive.creat import KjNode

node = KjNode(backend=ollama_backend, target_count=20)
result = node.diverge(brief)
# result.ideas: tuple[str, ...]
# result.clusters: dict[str, list[int]]  # group_name -> idea_indices
# result.relations: list[tuple[int, int, str]]  # (idx_a, idx_b, kind)
```

### CREAT-02: MindMap ノード

中心テーマ → 階層的 sub-topic 展開 (DFS, 深さ 3)。各枝は LLM の 1 呼び出しで分岐。tree 構造を ledger に保存。

### CREAT-03: 構造化変換

KJ + MindMap + TRIZ + Six Hats の 4 出力を統合し、**要件 spec (REQUIREMENTS.md 形式の Markdown 表)** を自動生成。

最終的には: Brief 1 件 → 自動生成された REQUIREMENTS.md フラグメント を出力できる状態。

### CREAT-04: Six Hats Multi-track

Brief を 6 観点 (factual / emotional / cautious / optimistic / creative / process) で多視点評価。各観点が独立した sub-Brief を発行 → 並列実行 → 結論を統合。

既存 `EpistemicType` の拡張 + Multi-track Filter Architecture A-1.5 と統合。

### CREAT-05: Synectics 類比エンジン

RAD コーパス (49 分野) から「Brief と意味的に遠いが構造的に類似」な doc を取得 → TRIZ 原理に紐付けて発想資源化。raptor の `cross_domain_ideation` skill と連携。

## なぜ「明示的な拡散層」か

LLM の単一回答に頼ると、いくつかの典型的な失敗が起きる:

| 典型的失敗 | 原因 | 拡散層での対策 |
|---|---|---|
| 視野狭窄 | 最初の候補に引きずられる | KJ法 ≥20 候補を**強制** |
| 思考の浅さ | 1 階層しか展開しない | MindMap で深さ 3 を**強制** |
| 偏った楽観 | "良い案ばかり" 出す | Six Hats で cautious 観点を**強制** |
| 既存パターン依存 | 知っている解の組合せに終始 | Synectics で異分野類比を**強制** |

## スパイラル開発 (C1-C6)

| Iter | スコープ | 評価 | リスク |
|---|---|---|---|
| C1 | CREAT-01 KJ法ノード — 拡散 sampling + clustering | 1 Brief で ≥20 件 + group ≥3 | 中 (LLM 呼出回数増) |
| C2 | CREAT-02 MindMap ノード — DFS depth=3 | tree 構造の妥当性、leaf の具体性 | 中 (token コスト) |
| C3 | CREAT-04 Six Hats — 6 sub-Brief 並列発行 | 観点間独立性、結論多様性 | 中 |
| C4 | CREAT-05 類比エンジン — cross-domain RAD bridge | 類比の有用性 (人間評価) | 高 (semantic distance metric 設計) |
| C5 | CREAT-03 構造化変換 — 4 種出力を要件 spec に合成 | spec の網羅性 + 矛盾検出 | 高 (出力品質測定が困難) |
| C6 | 統合 — KJ → MindMap → TRIZ → Six Hats → 構造化変換 のフルパス | end-to-end Brief → REQUIREMENTS.md 自動生成 | 高 (アーキ統合) |

## llove TUI との統合

C6 完成時には llove TUI に **Creative Workbench** モードを追加:

- KJ 付箋ボード (drag & drop で再グルーピング可)
- MindMap 樹形図 (折り畳み可)
- Six Hats 6 タブ (観点切替で同じ Brief を異なる視点で表示)
- 構造化変換結果のリアルタイムプレビュー

HITL (Human-in-the-loop) の力を最大化するインタフェース設計。

## 既存研究との位置づけ

- **Tree of Thoughts** (Yao 2023): DFS 推論
- **Self-Refine** (Madaan 2023): 自己批評ループ
- **Reflexion** (Shinn 2023): エピソード記憶からの改善
- **CoT / Auto-CoT** (Wei 2022 / Zhang 2023): 推論パス露出

llive の差別化: **拡散プロセスを明示的に構造化 + ledger に固定記録** → 後から replay / audit / 学習データ抽出可能。

## ソース (実装前)

- 要件: REQUIREMENTS.md v0.9 CREAT セクション
- ロードマップ: ROADMAP.md Phase 9
- 既存 TRIZ 連携: `src/llive/triz/`

## 完成版記事の予告

C1 (CREAT-01 KJ法ノード) 実装後に draft 解除し:
- 実 Brief × CREAT-01 拡散結果の可視化 (clusters)
- LLM 呼出コストの実測
- 比較: 単一回答 vs KJ法経由の意思決定品質
を追加してリリースします。

---

> 設計記事段階。実装が進んだ時点で内容を更新します。
