# lldarwin Stage1 — 実測結果と honest disclosure (2026-05-26)

> 設計正本: [`docs/vision/LLDARWIN_DESIGN.md`](../vision/LLDARWIN_DESIGN.md) §6。
> 実装: llive `src/llive/perf/evolutionary/lldarwin.py` (`MultiPressureSelector`)。
> 関連 memory: `project_lldarwin` / `feedback_benchmark_honest_disclosure`。

## 1. Stage1 で入れた変更 (llive, branch `optimize/core-2026-05-20`)

1. **criteria 除外** (`DEFAULT_EXCLUDED_CRITERIA`): `factor_score` (= max-archetype の
   単一スカラー = argmax, SEL-2 違反 = best=1.0 飽和の真因) と `nearest_persona_idx`
   (= 順序に意味のないカテゴリ index) を ε-lexicase の case から外す。
2. **novelty pressure** (`MultiPressureSelector(use_novelty=True)`): 毎世代 k-NN novelty
   (過去世代 archive との平均距離, Lehman-Stanley) を集団内 z-score 化 (STD-1) し
   `breakdown['novelty']` に書いて追加の lexicase case にする。`poc_evolution_env.py` で
   実証済の核機構 (標準化 novelty)。run スクリプトに `--novelty` フラグを追加。

テスト: `tests/unit/test_evolutionary_lldarwin.py` 8→10 件 (除外 / novelty 保存を追加)。
進化系 847 件 green、回帰なし。

## 2. 実測 (rich-proxy, 8 founders + pop24, 150 世代, seed 0)

### 2.1 行動多様性 (diversity_l2) — **novelty が効く指標**

| 条件 | mean | tail30 min | final |
|---|---|---|---|
| BASELINE (除外前・Tournament 相当の旧 lldarwin) | 7.12 | 0.68 | 0.83 (崩壊) |
| A: criteria 除外のみ | 9.16 | 1.57 | 1.57 |
| **B: 除外 + novelty** | **14.88 (+109%)** | **6.56 (9.6×)** | **11.73 (崩壊回避)** |

→ novelty pressure は行動 (genome 空間) 多様性を約 2 倍に維持し、終盤の多様性崩壊を防ぐ。
criteria 除外も単独で寄与 (spurious argmax 圧の除去)。

### 2.2 系統固定 (founder_counts) — **novelty では改善しない指標**

全条件で最終的に **8 → 2 系統** (furuse-kazufumi + friston) に収束。
oka-kiyoshi / grothendieck / von-neumann / feynman / millidge / isomura は絶滅。

## 3. Honest disclosure (最重要)

**TODO の「再ランで岡潔/グロタン系統が生き残るか」は、行動多様性と系統生存を混同していた。**

`poc_evolution_env.py` の著者コメント (L129-132) が明記:
> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs
> QD niching on lineage / PERSONA-FX, not pure novelty**"

- 実証済 monoculture 0.05 は **行動的** (archive-cell 占有) であって **系統的ではない**。
- 系統固定が中立浮動 (Kimura) で monoculture に向かうのは **理論的に正常** であり、
  novelty / lexicase では構造的に止められない (両者は既存個体の保存のみ。絶滅した
  系統を復活させる機構を持たない)。
- archetype 間距離も 0.068〜0.29 と圧縮 (sims が 0.71〜1.0 に密集) しており選択勾配が
  弱く drift 支配。friston は最も非中心的 (centroid 距離 0.162) なのに生存 = 中心性でなく
  drift で 2 系統が固定。

## 4. 次段 (系統生存を本当に達成するには)

**lineage-niched QD / 中立貯蔵庫** (= founder 由来でセル分割し各系統の elite を保持・
毎世代 re-inject) または **PERSONA-FX** (文化的獲得トラック)。これは `MultiPressureSelector`
(親選択のみ) の範囲外で、`EvolutionLoop` レベルの re-injection 支援が要る = Stage1.5/Stage2。

- `fitness_rich` の archetype 層差別化 (層ごとに固有値) で archetype 分離を広げれば選択勾配は
  強まるが、founder seeding (`from_persona_affinity(broadcast="uniform")`) が層差別化 archetype
  と不整合になり「founder が自分のピークに乗る」契約が壊れる → seeding と archetype を同時に
  層差別化する設計が必要 (Stage1.5 で検討)。

## 5. 結論

Stage1 は **行動多様性の維持に成功** (novelty 2×・崩壊回避)。**系統多様性は未達だが、これは
proxy 機構の理論的限界であり honest に記録**。系統保持は lineage-QD / PERSONA-FX の課題として
明確化。楽観せず、勝った気にならず、内訳を分けて報告した ([[feedback_benchmark_honest_disclosure]])。

実測 out: llive `out/lldarwin_{baseline,A_exclude,B_novelty}_2026_05_26/`。
