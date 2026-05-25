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

## 4.1 lineage-niched 中立貯蔵庫 PoC (2026-05-26, llive `scripts/poc_lineage_reservoir.py`)

§4 の「系統生存には lineage-QD/中立貯蔵庫が要る」を、核改修前に standalone PoC で実証
([[feedback_poc_feasibility_first]] = 要件→PoC→フィジビリティ→詳細設計)。selection は Stage1 の
`MultiPressureSelector`(criteria 除外+novelty)を流用、fitness は rich-proxy、系統は parent_a から
継承。reservoir = 系統別 best-ever genome を保持し、**絶滅した系統を毎世代 re-inject**(低 score の子を
置換、best は壊さない)。8 founders + pop24 + 150 gens + seed0:

| reservoir | 最終 named 系統 | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1** (oka-kiyoshi 24/24 = 完全 monoculture) | 1.00 | 1.58 |
| **ON** | **8 (全 founder 生存)** | **0.31 (≪ 0.8 OE-3)** | 1.69 |

reservoir ON で岡潔(oka)・グロタン(grothendieck)含む全 8 系統が生存。最終 shares =
friston 7 / furuse 6 / grothendieck 4 / oka 3 / 他 4 系統各 1。**強系統は子孫を持ち繁殖し、弱系統は
貯蔵庫が生命維持**(理想的挙動)。行動多様性も低下なし(1.69 vs OFF 1.58)。

**Honest 留保**: 貯蔵庫は frozen elite を再投入するため、弱系統(各1体)の「生存」は再投入由来で
能動的進化ではない。これは中立貯蔵庫の定義通り(代表を保持し再結合可能にする)で正当だが、
「系統が活発に進化し続ける」とは主張しない。EvolutionLoop 組込時は (a) 祖先追跡 (b) 再投入頻度/
予算 (c) elitism をスカラー上位→系統別に変える、を詳細設計する。

## 4.2 Stage1.5 実装 — 中立貯蔵庫を EvolutionLoop へ組込 (2026-05-26, llive)

PoC (§4.1) で実証した機構を **本番 EvolutionLoop に additive + default-off で組込**:
- `EvolutionLoop.on_population_bred` hook 追加 (breed 直後・評価前に bred リストを変換、
  既定 None = 後方互換)。
- `LineageReservoir` (`lineage_reservoir.py`): 祖先追跡 (parent_ids[0] 継承) + 系統別
  best-ever 保持 + 絶滅保護系統の re-inject。`founder_map` を共有し系統ログとも整合。
- `run_persona_evolution(lineage_reservoir=True)` / run スクリプト `--lineage-reservoir`。
- tests: `test_evolutionary_lineage_reservoir.py` 6 件 + 進化系 **937 green** (回帰なし)。

**実 EvolutionLoop 実測** (rich-proxy + lldarwin + novelty, 8 founders/pop24/150gens/seed0):

| 条件 | named 系統生存 | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8 (furuse 17 + friston 7) | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8 (全系統)** | **0.33** | **0.29 (≪ 0.8 OE-3)** | 9.20 |

岡潔(oka 3)・グロタン(grothendieck 1)含む全 8 系統が実ループで生存。PoC の予測 (fixation 0.31)
を実装で再現 (0.29)。**Honest 留保**: diversity_l2 は 14.88→9.20 に低下 (frozen elite 再投入で
genome 空間 spread がやや減る) — ただし OFF 時の崩壊 (0.83) は回避。系統保持と行動多様性は
弱いトレードオフ関係。再投入予算/頻度の調整は今後の sweep 課題。

## 4.3 再投入頻度 sweep — 系統保持 ↔ 行動多様性トレードオフ (2026-05-26)

§4.2 の honest 留保 (frozen elite 再投入で diversity が下がる) を、`reinject_interval`
(再投入を行う世代間隔, 既定 1=毎世代) の sweep で特性化。`LineageReservoir.reinject_interval`
+ `--reinject-interval` フラグ追加 (test 7 件)。8 founders/pop24/150gens/seed0:

| interval | named 生存 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1** (毎世代) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84 (最大)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**非自明な発見**: diversity は interval を上げるほど単調増加せず、**interval=5 でピーク**
(10/20 はむしろ低下)。系統を放置しすぎると貯蔵庫由来の多様性注入が減り、かつ少数系統が
固定して diversity も伸びない。**運用指針: 系統保持最優先 → interval=1 (8/8) / 行動多様性も
両立 → interval=5 (5/8 保持しつつ diversity 最大)**。両立の最適点は fitness/集団規模依存なので
本番 sweep で再較正する。

## 5. 結論

Stage1 は **行動多様性の維持に成功** (novelty 2×・崩壊回避)。**系統多様性は未達だが、これは
proxy 機構の理論的限界であり honest に記録**。系統保持は lineage-QD / PERSONA-FX の課題として
明確化。楽観せず、勝った気にならず、内訳を分けて報告した ([[feedback_benchmark_honest_disclosure]])。

実測 out: llive `out/lldarwin_{baseline,A_exclude,B_novelty}_2026_05_26/`。
