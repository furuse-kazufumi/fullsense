---
layout: default
title: "進化 fitness 再設計 — 多峰・多目的・多染色体 (is it really evolving?)"
parent: "Research"
nav_order: 96
---

# 進化 fitness 再設計 (2026-05-25)

> 発端 (ユーザー): 「実際問題、進化として成立してるか気にしている」「ファクターが少なすぎる
> 可能性」「次元をもっと増やそう」「染色体ももっと増やそう」「色々調べてから対応して
> (Perplexity 可)」。本 doc は調査 → 診断 → 段階再設計の単一の真実。
> honest disclosure: 全て **proxy fitness** 上の話 (実 LLM 評価ではない)。

## 1. 診断 — proxy run はなぜ「進化として弱い」か

500 世代 proxy run (`llive out/evo_run_2026_05_25`, genome3d, seed 2, pop 32) の実測:

| 兆候 | 数値 |
|---|---|
| founder 系統 **全絶滅** | **gen23** で 8 persona 全滅 → 以後 `(random)` 起源 = 100% |
| best 頭打ち | gen281 到達後、残り 219 世代 (44%) 改善ゼロ (改善は 500 中 29 ステップ) |
| 多様性急収束 | gen0 2.47 → gen25 1.15 → 最終 0.86 (min 0.80) |

機構としては正当な EA (選択+変異+交叉+遺伝, 適応度は上がる) だが「丘登り→中立ドリフト」。

**根本原因 (`_proxy_fitness`)**: `score = 0.7*balance + 0.3*provenance`、しかも
`c_factors`(10×4) を **層平均で 10 次元に圧縮**。⇒ (1) 実効目的は単峰・凸 (全因子を均等に高く)、
(2) 40 cell 中 30 と層構造が中立、(3) `c_impl/c_prompt/c_meta` の 3 染色体は **fitness 完全中立**
(純粋ドリフト)。persona の個性は偏った affinity に宿るが proxy は均等を報酬化するので persona は
**積極的に淘汰**され、均等高値に近い random 個体が勝つ。

## 2. コード調査 — llive は機構を持っているが未配線

`src/llive/perf/evolutionary/` に **実装済みだが default loop に未配線**:

- `nsga2.py` — NSGA-II (非支配ソート + crowding distance + `NSGA2Selection`, drop-in)
- `quality_diversity.py` — `MAPElitesGrid` (4 軸) + `PersonaOverlapPenalty`
- `diversity.py` — `NoveltyScorer` + `DiversityPreservingBreedFilter` + `DiversityMonitor`
- `speciation.py` — NEAT 種分化 + **fitness sharing** (`shared_fitness = f/種サイズ`)
- `island_model.py` — 島モデル + migration
- `cma_es_diversity.py` — CMA-ES + novelty (唯一 `novelty_weight` を読む)
- **`MetaChromosome.novelty_weight` / `mutation_rate_per_layer` は誰も読まないデッドフィールド**

fitness は `Callable[[Genome], FitnessReport]` で **per-individual** (集団文脈なし) →
頻度依存/fitness sharing は selection 層 (NSGA2/speciation) か post-eval wrapper で行う。

## 3. 先行研究 — 「増やす」の罠と解

- **many-objective の呪い**: 目的が ~4 を超えると Pareto 支配が崩れ、ほぼ全個体が非支配 =
  **選択圧消失** (20 目的で完全停止)。→ 次元/染色体/目的を素朴に増やすと進化は **悪化**する。
  - 解 = **lexicase selection** (ケース毎評価、高次元でも選択圧+多様性維持。**llive 未実装** =
    独自貢献余地)。[ε-Lexicase, La Cava](http://faculty.hampshire.edu/lspector/pubs/GECCO_lex_reg-corrected.pdf) /
    [analysis](https://arxiv.org/pdf/1709.05394)
- **open-ended evolution**: 変異+遺伝+選択は「限定的進化には十分だが open-ended には不十分」。
  今の plateau/絶滅/多様性崩壊は古典 ArtLife (Tierra/Avida) の peter-out と同型。OEE 要件 =
  無限の可能性空間 + **より複雑な子孫を生める** こと。
  [Requirements for OEE](https://arxiv.org/pdf/1507.07403) /
  [Routes to OEE](https://arxiv.org/pdf/1806.01883)
- **多峰最適化**: fitness sharing / crowding / niching。**QD** は quality と diversity を分離
  (MAP-Elites, NSLC)。
- **結論**: 染色体を増やすのは正しい (表現力=OEE 要件) が、**それを読む目的関数/選択を同時に**
  入れるのが必須。さもないと中立ドリフトが増えて「進化が成立しない」を悪化させる。

## 4. 段階再設計 (測定優先)

### Stage 1 ✅ 着地 (`fitness_rich.py`, `--fitness rich-proxy`)
全 40 次元 c_factors + **persona archetype 多峰** (8 persona = 8 ピーク、affinity を層へ uniform
broadcast = founder が自分の峰に乗る) + 染色体コヒーレンス (mild)。per-archetype 類似度を
`breakdown` に出し Stage 2 の niching/NSGA-II/lexicase が消費可能。**proxy のまま** (honest:
`is_proxy=True` を `run_persona_evolution` に明示)。

**実測比較** (seed 2, 500 世代):

| 指標 | baseline (旧 proxy) | rich-proxy |
|---|---|---|
| founder 全絶滅 | gen23 | **しない** |
| gen500 生存 founder | 0/8 | 2/8 (friston 56% / furuse 44%) |
| `(random)` 占有 | 100% | **0%** |
| 多様性 gen500 (min) | 0.86 (0.80) | **1.68 (1.30)** |
| best 改善ステップ | 29/500 | **0/500 ← 新問題** |

良化: 多峰化で **founder 絶滅解消・(random) 支配消失・多様性大幅維持**。
新問題 (honest): founder を峰ぴったりに seed したため **best=1.0 が gen0 から = 改善勾配ゼロ**
(最適が初手で解けている)。niching 無しで 8 → 2 ニッチに収斂。

### Stage 2 (次) — 非自明な地形 + niching/lexicase
1. **勾配を作る**: archetype を **層分化** (persona ごとに per-layer profile を変える) →
   founder の uniform broadcast は峰から外れ、層構造を進化で獲得する必要 = 真の climb。
   かつ層次元が初めて意味を持つ。
2. **8 ニッチ維持**: `speciation` (fitness sharing) か `MAPElitesGrid` か `PersonaOverlapPenalty`
   を default loop に配線 → 全 persona 共存。
3. **lexicase selection 新規実装**: per-archetype 類似度 (+ 染色体ケース) を集約せず個別評価。
   many-objective の呪いを回避しつつ高次元で選択圧維持。

### Stage 3 — 消費目的つき新染色体 (OEE)
新染色体は **必ず Stage 2 の目的/選択が読む** こととセットで追加 (中立ドリフト回避)。
「より複雑な子孫を生める」設計 (可変長コンポーネント列等) で OEE 要件に寄せる。
デッドフィールド (`novelty_weight` 等) も配線 or 撤去。

### Stage 4 — 実 LLM fitness (真の検証, ユーザー GO 待ち)
`--fitness llm --backend ollama` + OLLAMA_HOST。proxy で機構を磨いてから本番評価へ。

## 5. 可視化連携
`founder_lineage.jsonl` (全集団・正確な root-founder 分布, run が毎世代出力) →
`scripts/evolution_lineage_viz.py` が persona 支配ストリーム (animated SVG) + champion 系統
(Mermaid)。Stage 毎に baseline/rich を並べて「進化が成立したか」を可視化で比較する。

## 関連
- 実装: `llive src/llive/perf/evolutionary/fitness_rich.py`, `scripts/run_persona_evolution_long.py --fitness rich-proxy`
- viz: `llive scripts/evolution_lineage_viz.py` / `evolution_viz.py` / `evolution_genome3d_heatmap.py`(予定)
- 上流: [[goal_evolution_run_and_viz]] / [[project_llive_evolution_next_session]] / [[feedback_benchmark_honest_disclosure]]
