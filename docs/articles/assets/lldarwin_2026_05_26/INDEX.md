# lldarwin 可視化素材カタログ (2026-05-26)

> 投稿素材 (Qiita #25 monoculture / #26 lldarwin multi-pressure / #27 falsification 等)。
> 全 SVG は **依存なし自己完結 + SMIL アニメ** (FullSense house style)。GitHub README /
> Qiita / LinkedIn にそのまま埋め込み可。ローカルパス無し・honest ラベル焼込済。
> 設計/実測の正本: [`docs/research/lldarwin_stage1_results_2026_05_26.md`](../../../research/lldarwin_stage1_results_2026_05_26.md)。

## 素材一覧

| ファイル | 何を示すか | 物語 (記事での使いどころ) |
|---|---|---|
| `lldarwin_stage1_baseline_status.svg` | baseline (novelty なし) の適応度+多様性。終盤 **多様性崩壊** | #25 導入: 素朴な選択圧では monoculture |
| `lldarwin_stage1_novelty_status.svg` | novelty pressure ありの適応度+多様性。**多様性が維持** | #26 Stage1: novelty で行動多様性 +109% |
| `lldarwin_stage1_diversity_overlay.svg` | baseline vs +novelty の diversity_l2 **重ね描き** (崩壊 vs 維持を1枚で対比) | #26/#27 Stage1 の決定的1枚 |
| `lldarwin_genome_heatmap.svg` | 勝者個体の **思考因子×メモリ層ヒートマップ** (Genome3D, P3)。real-pressure では c_factors 中立=参考 | #26/#28 認知プロファイル可視化 |
| `lldarwin_reservoir_off_dominance.svg` | 系統支配ストリーム (中立貯蔵庫 **OFF**)。最終 **furuse 71% / friston 29% = 2系統に崩壊** | #25/#26 ヤマ: 「私と friston だけ生き残る」 |
| `lldarwin_reservoir_on_dominance.svg` | 系統支配ストリーム (中立貯蔵庫 **ON**)。**全 8 系統が並存** (millidge/von-neumann/oka/grothendieck…) | #26 Stage1.5 ヤマ: 貯蔵庫で系統絶滅を防ぐ |
| `lldarwin_reservoir_on_status.svg` | 貯蔵庫 ON の適応度+多様性 | #26 補足 |
| `lldarwin_reinject_sweep.svg` | 再投入頻度のトレードオフ。**系統保持↔行動多様性、diversity は interval=5 でピーク (非単調)** | #26/#27 設計知見: 非自明な最適点 |
| `lldarwin_stage2_proxy_axes.svg` | 5 苦手軸 (typo/polysemy/multistep/calibration/context) の母集団平均推移 (**proxy**) | #26 Stage2 前半: 軸ごと独立淘汰 (mechanism feasibility) |
| `lldarwin_stage2_real_llm_axes.svg` | 同上だが **実 on-prem LLM (llama3.2) 評価**。prompt 戦略進化で軸が改善 | #26 Stage2 後半ヤマ: 実 LLM 弱点緩和 |
| `lldarwin_stage2_real_llm_status.svg` | 実 LLM 進化ランの適応度+多様性 (12h 連続ラン) | #26 Stage2 後半: 実ラン |

## データ来歴 (honest disclosure)

- **proxy 系** (`stage1_*`, `reservoir_*`, `reinject_sweep`, `stage2_proxy_axes`): rich-proxy /
  pressure-proxy = **決定論 heuristic (LLM 非依存)**。機構が回ることを示すが「進化が意味ある
  ものを見つけた」ことは示さない ([[feedback_benchmark_honest_disclosure]])。SVG に "PROXY" 焼込済。
- **実 LLM 系** (`stage2_real_llm_*`): **on-prem ollama (llama3.2:latest) only** (measurement
  purity)。個体 `c_prompt` → system prompt → 固定 LLM を実タスクで採点 (Promptbreeder 系)。
  小バッテリ=ノイジー推定・一般能力主張ではない。**12h 連続ランの途中スナップショット由来**
  なので、ラン完了後に最新版へ差し替え可 (snapshot から再生成)。

## 再生成コマンド (llive)

```
py -3.11 scripts/evolution_lineage_viz.py <run_dir>   # persona dominance stream
py -3.11 scripts/evolution_viz.py        <run_dir>   # fitness + diversity
py -3.11 scripts/evolution_axes_viz.py   <run_dir>   # per-axis (pressure/real-pressure run)
```

run_dir 例: `out/lldarwin_{C_noreservoir,D_reservoir,12h_realpressure}_2026_05_26`。
