---
layout: default
title: "進化ラン可視化 計画 (evolution status visualization)"
parent: "Research"
nav_order: 95
---

# 進化ラン可視化 計画 (2026-05-25)

> Goal (ユーザー設定): 「進化ランに移行、その間 進化状況の可視化方法を計画」。
> 進化ランは runnable 実証済 (proxy 即動 / 実 LLM fitness は ollama 起動が前提・GO 待ち)。
> 本計画は **既存 FullSense 資産を活用** ([[project_github_animated_svg]] /
> [[project_llove_animated_svg_program]] / [[project_fullsense_animemd_branch_token_viz]] の
> `evolution.svg` proto / raptor `/diagram` Mermaid renderer) し、車輪を再発明しない。
> honest disclosure: proxy run の綺麗な曲線を実進化と誤認しない ([[feedback_benchmark_honest_disclosure]])。

## 1. データ源 (進化ランが既に出力。サンプル = llive `out/evo_run_2026_05_25/`)

| ファイル | スキーマ | 可視化用途 |
|---|---|---|
| `generations.jsonl` / `metrics.jsonl` | `{generation, n_individuals, best/mean/median/std_score, diversity_l2, seed}` | 適応度トラジェクトリ / 多様性推移 |
| `winners.jsonl` | `{generation, individual_id, parent_ids, score, rank}` | 系統・founder persona 支配率 |
| `lineage.mmd` | Mermaid `graph TD` (founder→子孫) | 系統樹 (既に Mermaid) |
| `snapshot_gen_*.json` (Genome3D) | 4 層 (impl/prompt/meta/c_factors[思考因子10×メモリ層4]) | ゲノム層の変遷 heatmap |
| `run_manifest.json` | commit/設定/founder/環境 | 来歴ラベル (proxy vs llm, seed, gen 数) |

## 2. 可視化ビュー (進化「状況」を読む)

1. **適応度トラジェクトリ**: best/mean/median + std バンド / 世代。「改善しているか」の核。
2. **多様性推移** (`diversity_l2`): 収束 vs 崩壊。`max_stall`/collapse-guard と並置し「健全に多様性を保ちつつ収束か」を読む (最重要・proxy でも構造把握可)。
3. **系統樹** (`lineage.mmd`): どの founder persona 系統が生き残るか。`/diagram` か mermaid-cli で描画。
4. **persona 支配ストリーム** (`winners.jsonl`): 世代×founder 系統の占有率 (stacked area / stream)。「von_neumann 系が席巻」等を一目で。
5. **Genome3D 層 heatmap**: 思考因子 10×メモリ層 4 の c_factors が世代でどう動くか ([[project_llive_thought_factor_per_layer]])。`evolution.svg` proto の発展先。
6. **(将来) PERSONA-FX 獲得**: 文化的ペルソナ獲得・隔世 ([[project_persona_fx]]) を系統上に重畳。

## 3. レンダリング手段 (FullSense house style を踏襲)

- **animated SVG (主)**: 宣言 → SMIL。`evolution.svg` proto #1 を拡張し、世代を再生する適応度+多様性+系統創発アニメ。portal/README/記事に自己完結で埋め込み (普及ファネル先頭)。
- **Mermaid**: `lineage.mmd` → raptor `/diagram` or mermaid-cli。系統樹は半完成。
- **llove panel (研究 IDE live)**: run の generations を scenario 再生 + c_factors を thought_factor_ring 表示 ([[project_llove_animated_svg_program]] C 案)。
- **Telegram per-run サマリ**: 既存 status チャネルに「best / diversity / stopped_reason + 小チャート」を push (本日の Telegram 基盤を再利用)。
- **matplotlib/plotly (分析用)**: 即席の curve 確認 (portal 非公開・解析専用)。

## 4. live vs post-hoc

- **post-hoc** (先): `generations.jsonl` 等を読み replay → SVG/Mermaid/チャート。実装容易、まず着手。
- **live** (後): run 中に metrics を SSE/MQTT で stream → llove panel / 予測符号化 push と接続
  ([[project_fullsense_expression_realtime_marathon]] real-time テーマ)。near-real-time 改修 Top-3 と整合。

## 5. 段階計画

| Phase | 内容 | 依存 |
|---|---|---|
| P0 | `generations.jsonl`→適応度+多様性 静的チャート (matplotlib) で「健全性」を即読み | 完了データあり |
| P1 | `evolution.svg` proto 拡張: 世代再生の animated SVG (適応度+多様性+honest ラベル) | P0 |
| P2 | `lineage.mmd`→Mermaid 描画 + winners→persona 支配ストリーム | — |
| P3 | Genome3D 層 heatmap (c_factors 10×4 の世代変遷) | snapshot 解析 |
| P4 | llove live panel + Telegram per-run サマリ | P1/P2 |
| P5 | **実 LLM run のデータで全 viz を上書き** (proxy ラベル→real) | ollama 起動 (ユーザー GO) |

## 6. honest disclosure

run は `run_summary.json` / stdout に `proxy fitness, NOT real LLM eval` を明示。**全 viz に
proxy/real ラベルを焼き込む** (proxy の収束曲線は「機構が動く」証拠であって「進化が良い」証拠ではない)。
実進化評価は実 LLM fitness 配線後 (P5)。

## 関連
- 進化ラン: llive `scripts/run_persona_evolution_long.py` (`--genome3d`, `--fitness {proxy,llm}`)
- 既存 viz 資産: `evolution.svg` proto / animated SVG program / raptor `/diagram`
- 上流: [[project_llive_evolution_next_session]] / [[project_persona_fx]]
