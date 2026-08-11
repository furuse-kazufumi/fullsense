---
title: 'NAS 週次レポート(2026-08-01) — TODO: 本題'
tags:
  - 機械学習
  - NAS
public_id: null
public_private: false
---

<!-- 機械生成の下書き。散文(背景/手法/考察)と画像は人手で肉付けする。 -->
<!-- generated: 2026-08-01 · runs: 5 -->

## 背景

<!-- TODO: 散文(人間) -->

## 手法

<!-- TODO: 散文(人間) -->

## 結果

| run | model | base nll | real evals | frontier (greedy→memetic) | hypervolume (greedy→memetic) | holdout gain (CI) | verdict |
|---|---|---|---|---|---|---|---|
| `nas-1p5b-r2` | Qwen2.5-1.5B-Instruct | 3.9010 | 515 | 5→16 | 63.73 → 109.13 | 71.6% (CI 68.8–74.4, p_win=1.0) | memetic frontier dominates greedy: hypervolume +71.2% |
| `nas-collapse-band-r2` | Qwen2.5-0.5B-Instruct | 4.4154 | 751 | 5→20 | 105.55 → 150.48 | 43.1% (CI 42.5–43.8, p_win=1.0) | memetic frontier dominates greedy: hypervolume +42.6% |
| `nas-cross-corpus-r2` | Qwen2.5-0.5B-Instruct | 4.4154 | 751 | 5→20 | 105.55 → 150.48 | 43.1% (CI 42.5–43.8, p_win=1.0) | memetic frontier dominates greedy: hypervolume +42.6% |
| `nas-distill-shift-r2` | Qwen2.5-0.5B-Instruct | 4.4154 | 751 | 5→20 | 105.55 → 150.48 | 43.1% (CI 42.5–43.8, p_win=1.0) | memetic frontier dominates greedy: hypervolume +42.6% |
| `nas-needle-r2` | Qwen2.5-0.5B-Instruct | 4.4154 | 751 | 5→20 | 105.55 → 150.48 | 43.1% (CI 42.5–43.8, p_win=1.0) | memetic frontier dominates greedy: hypervolume +42.6% |

## Honest disclosure

<!-- TODO: 散文(人間)。各 run の未計測項目は次節に機械保持されている。 -->

## Still unmeasured

- `nas-1p5b-r2`: `right_shift_ci` (needs `--distill`); `needle` (needs `--needle`); `cross_corpus` (needs `--cross-corpus <file>`)
- `nas-collapse-band-r2`: `right_shift_ci` (needs `--distill`); `needle` (needs `--needle`); `cross_corpus` (needs `--cross-corpus <file>`)
- `nas-cross-corpus-r2`: `right_shift_ci` (needs `--distill`); `needle` (needs `--needle`)
- `nas-distill-shift-r2`: `needle` (needs `--needle`); `cross_corpus` (needs `--cross-corpus <file>`)
- `nas-needle-r2`: `right_shift_ci` (needs `--distill`); `cross_corpus` (needs `--cross-corpus <file>`)

## 再現

<!-- TODO: 再現コマンド(人間) -->
