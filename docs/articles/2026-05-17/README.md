---
layout: default
title: "Articles — 2026-05-17"
nav_order: 70
---

# FullSense — 2026-05-17 articles index

> 当日 1 セッションで実装・検証した内容のうち、外部公開できる粒度で
> 抽出した記事ドラフト集。Qiita / note / dev.to / Medium へそのまま
> 転載できる形式 (frontmatter は GitHub Pages 用、本文は media-agnostic)。

このディレクトリは「**最新公開資料の集約場所**」として運用します。
過去の記事は `docs/articles/<日付>/` で stamping、最新は常に
このフォルダ + 上位 index にリンク。

## 当日の柱 3 本

| # | タイトル | テーマ | 主要対象 |
|---|---|---|---|
| 1 | [Brief API 設計と progressive matrix で見える llive の overhead < 1 %](./01_brief_api_progressive.md) | Brief API + 5×3 ベンチ | OSS LLM コミュニティ / on-prem 推論派 |
| 2 | [心理の深層 10 因子で整理する llive 思考層 — 既に 9/10 実装済](./02_cognitive_factors.md) | COG-FX フレームワーク | 認知科学 / Agent 設計者 |
| 3 | [数学・単位に強い AI を作る最初の一歩](./03_math_vertical.md) | MATH 系 | 精密計測 / 物理シミュ / 教育 |
| 7 | [llive vs 他 LLM ベンチマーク — 動作確認の罠と honest disclosure](./07_bench_results.md) | ⚠️ 当初版は不公平、改訂版で異常 3 件を明示。fair 再走中 (`docs/benchmarks/2026-05-17-fair/`) | 研究開発の罠認識 |

## 一文サマリ (RT 用)

- **記事 1**: llive の Brief API は外部から渡された work unit を 6 stage loop に流す薄い接着剤。15 セルベンチで overhead < 1 % を実測、決定は token 圧力に対し完全 stable
- **記事 2**: 「心理の深層」から抽出した 10 思考因子をマッピングした結果、llive は v1.0 必須の土台 5 因子 (構造化・閉ループ・不確実性・整合・来歴) を既にすべて実装済
- **記事 3**: LLM の数値幻覚に対して「LLM に計算させない」決定論的サイドカーを入れる。SafeCalculator (AST visitor + whitelist) と SI 次元 grounding を先に入れ、`5 m/s + 3 s` のような cross-quantity mismatch 停止は次イテレーションで詰める

## 公開先候補 (転載先)

- Qiita: 日本語技術コミュニティ、tag に `llm` / `agent` / `physics` / `python`
- note: 設計思想・経営判断系の長文向け
- Medium / dev.to: 英語圏向け、記事 1 から翻訳優先
- GitHub: 各プロジェクト docs/blog として併設可

## 関連ソース (記事の裏付け)

- llive Brief API: `llive/src/llive/brief/`
- progressive matrix: `llive/docs/benchmarks/2026-05-16-progressive-full/`
- COG-FX: `llive/.planning/REQUIREMENTS.md` v1.0-frame セクション
- MATH-01/08: `llive/src/llive/math/`
- tests: 1014 PASS (回帰ゼロ)

## 次回の記事候補

- CABT-01 prototype 実装後 → 「Transformer ブロックを高度化する 7 つのアプローチ」
- CREAT-01 KJ法ノード後 → 「LLM × KJ法 × MindMap で要件定義を自動化する」
- MATH-02 Z3 Sympy 検算後 → 「LLM 数式幻覚をどう止めるか — 形式検証ゲートの実装」
