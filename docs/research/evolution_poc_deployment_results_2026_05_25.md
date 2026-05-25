---
layout: default
title: "開放端進化 PoC デプロイ結果 (deployment sweep)"
parent: "Research"
nav_order: 99
---

# 開放端進化 PoC デプロイ結果 (2026-05-25)

> Goal (3) 「導入可能な段階に進める」の実地前進: runnable 環境 `poc_evolution_env.py` を
> **実際に様々な条件で wallclock 予算ラン**し実メトリクスを収集。検証済み核機構
> (標準化 novelty + 中立貯蔵庫 + minimal-criterion + QD archive) を deploy。
> honest: 全 PROXY・決定論。「新しい AI=知能」の最終判定は Stage6 実 LLM (Codex/ollama)。

## 1. 核仮説の実証 (poc_openended_diversity.py, 4 条件)
標準化 novelty 選択は多様性を**持続**、scalar 選択は**崩壊**:
- scalar: 多様性保持 5.9–23.8% (崩壊) / novelty: 83.9–101.1% (持続) / **novelty÷scalar = 4.25–14.17x**。
- → STD-1 / SEL-1 / SEL-2 / OE-3 を実機実証。

## 2. デプロイ sweep (poc_evolution_env.py, wallclock 90s/条件)

| 条件 | gens(90s) | diversity gen0→tail | monoculture(行動) | archive_cells | growth(末20%) | verdict |
|---|---|---|---|---|---|---|
| pop128 / latent256 | 6670 | 0.287→0.156 | 0.05 | 899 | +16 | OPEN-ENDED-ish |
| pop256 / latent512 | 407 | 0.288→0.233 | 0.05 | 448 | +6 | OPEN-ENDED-ish |
| pop128 / latent1024 | 831 | 0.287→0.141 | 0.05 | 722 | +60 | BOUNDED(境界) |

## 3. 実地の発見
- **世代交代は秒オーダー**: pop128/latent256 は 90s で **6670 世代** (≈74 gen/s)。10K 世代 ≈ 2.3 分。
  → 5h+ 連続ランは余裕で実現可 (RUN-2 裏付け)。pop/genome 増で per-gen は重くなる (pop256/latent512 ≈4.5 gen/s)。
- **行動 monoculture は全条件 0.05** (≪0.8): novelty+QD で単一 cell 支配を構造的に回避 (OE-3 達成)。
- **latent1024 が境界判定**: archive 成長 +60・monoculture 0.05 と健全なのに diversity 保持が閾値 0.143 を
  わずかに下回り BOUNDED 判定。= **巨大ゲノムは pop/世代数を釣り合わせる必要** (ユーザー仮説「容量×母数×
  世代を一括スケール」の裏付け)。verdict 閾値自体も要校正 ([SPEC])。
- **checkpoint/resume 検証済** (gen200→350 連続性, full-state + JSON RNG, commit e1a800f) → 5h+ 中断/再開可。

## 4. 導入状態 (deployable)
- 環境: `llive scripts/poc_evolution_env.py` (CLI: scale/sweep/--resume/--max-seconds), 検証済・コミット済。
- 標準ラン recipe: `py -3.11 scripts/poc_evolution_env.py --gens 100000 --pop <N> --latent <M> --max-seconds <s> --out out/<name> --checkpoint-every 500`。
- 次 (校正→本番): 校正で per-gen 実測 → 5h window を埋める pop/latent/gens 確定 → 夜間長時間ラン
  (RUN-2) → Bedau/MODES の本実装で open-endedness 厳密判定 → CulturalChromosome/PERSONA-FX/メタ進化を
  段階追加 → Stage6 実 LLM (部下 Codex / ollama)。

## 関連
- [[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] / [[evolution_poc_experiment_design_2026_05_25]] /
  [[evolution_design_tensions_open_decisions_2026_05_25]] / [[reference_codex_two_pillar]] /
  [[feedback_benchmark_honest_disclosure]]
