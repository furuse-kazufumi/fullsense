# 高速化候補 PoC 技術報告書 (2026-05-24)

> FullSense 技術資料。ユーザー指示「ちゃんと定量的に比較する PoC が必要。効果がありそう
> なら要件定義にまとめて本格導入」「組み合わせごとの PoC も」「単に高速というだけでは
> 少し疑わないといけない」「lleval のような眼鏡で PoC」+ Goal「全 PoC を済ませる」に対応。
> **5 単体 + 3 組み合わせ = 8 PoC + 眼鏡メタ評価**を 1 セッションで実装・実測した技術報告。
>
> 要約 (表) は `docs/research/acceleration_poc_matrix_2026_05_24.md`。本書はその**技術詳細
> 版** (モデル・パラメータ・結果・honest disclosure を 1 本に統合)。

## 0. 方法論と前提 (honest disclosure)

- 規約: 要件 → **PoC (定量比較)** → フィジビリティ → 詳細設計
  ([[feedback_poc_feasibility_first]])。採用は「網羅」でなく「選別」、現状構造を破綻させない
  範囲で使う ([[feedback_originality_over_imitation]])。
- **すべて simulation / toy 環境**。実 transport・実 LLM executor・実 fitness は未配線。
  数値は損益の**構造**を見るためのもので、絶対値は実測で上書きする前提。
- 各 PoC は実コンポーネントを可能な限り駆動 (例: Speculative は実
  `SpeculativeMeshCoordinator`、Antifragile は実 `AntifragileController`) し、その上に
  レイテンシ/コストモデルを重ねる。
- **「単に高速 ≠ 採用」**。§4 の眼鏡で各 PoC を speed 以外の軸 (品質犠牲・隠れコスト・
  汎化リスク・self-preference) で採点し、trust を出す。

---

## 1. 単体 PoC (5)

### 1.1 Speculative Mesh Execution (llmesh)

**仮説**: メイン推論中の予測分岐を idle peer へ Ed25519 署名付きで投機投入し、到達時に
mesh から回収すれば、ローカル swap より速い (LAN 前提)。

**モデル** (`llmesh/speculative/bench.py`): 1 分岐あたり
baseline = `local_ms + swap_ms`、speculative = hit で `pull_ms + sign_ms`、miss で
`sign_ms + miss_penalty_ms + baseline`。break-even hit_rate
`h* = miss_penalty / ((baseline − pull) + miss_penalty)`。

**結果** (n=2000):

| scenario | hit 0.3 / 0.5 / 0.7 / 0.9 | break-even |
|---|---|---|
| LAN fast-fallback | 1.39x / 1.94x / 3.10x / 7.77x | 0.00 |
| LAN slow-fallback(20ms) | 0.93x / 1.31x / 2.11x / 5.52x | 0.34 |
| big-model swap-bound | 1.40x / 1.99x / 3.26x / **9.18x** | 0.00 |
| WAN | 0.70x / 0.57x / 0.49x / 0.43x | 1.00 (勝てない) |

**honest disclosure**: miss が latency-neutral なのは fast-fallback (即ローカル切替) のときだけ。
timeout 待ちが入ると break-even が上がる。低 hit_rate では `wasted_compute`(電力)が大きい。
WAN は pull > baseline で全敗。**要件定義済** (`llmesh/docs/requirements_speculative_mesh.md`,
SPEC-MESH-01..10)。

### 1.2 Antifragile Mutation (llive)

**仮説**: 高 surprise (停滞) を panic mode のトリガにし探索を一時爆発させれば、局所最適から
脱出できる ([[project_idea_antifragile_mutation]] の「未検証」を検証)。

**モデル** (`llive/src/llive/evolution/antifragile_bench.py`): 騙し 2 山 landscape (局所
x=-2/0.85 広, 大域 x=3/1.0 狭, 5 単位離)。全個体を局所 basin 起点。実 `AntifragileController`
に停滞を高 surprise として供給 → panic 中のみ sigma を 8x。pop=30 / 60 世代 / seeds=30。

**結果**: baseline 脱出率 **0%** (mean best 0.850) vs antifragile **100%** (mean best 1.000)。
コスト = panic 平均 **47.7 / 60 世代**。`exploration_multiplier=1` では脱出率が落ちる
(増幅が効いている裏付け)。

**honest disclosure**: landscape を panic 有利に設計した toy 1-D。原理 (探索爆発で脱出) は
実証したが、実 fitness・高次元 genome の ROI は別途要測定。panic コストが高い (cooldown/
recovery で滞在を絞るチューニングが本番必須)。

### 1.3 適応推論予算 (IBPO / early-exit, llive)

**仮説**: 易しい入力に浅く・難しい入力に深く推論すれば、固定深さより同品質で平均計算量が
下がる (予測符号化「誤差がある所だけ計算」, `RecursionDepthGene` = L2 adaptive の裏付け)。

**モデル** (`llive/src/llive/perf/adaptive_budget_bench.py`): 難易度 d→required depth。
fixed は常に max_depth、adaptive は confidence 推定 (ノイズ付) で early-exit。max_depth=8 /
n=4000。

**結果**:

| confidence noise | compute 削減 | adaptive 精度 | fixed 精度 |
|---|---|---|---|
| 0.00 | **44%** | 100.0% | 100.0% |
| 0.05 | 44% | 90.3% | 100.0% |
| 0.10 | 44% | 75.4% | 100.0% |
| 0.20 | 44% | 65.8% | 100.0% |

**honest disclosure**: **「速いが間違える」罠**の典型。削減率は ~44% 一定だが、推定器ノイズで
精度が崩れる。早抜けの confidence 推定器の精度がトレードオフを支配。保守的推定 (深め bias) で
品質を回復する代わりに削減を譲るのが本番。

### 1.4 予測検証メタゲート (Gemini #1, llive)

**仮説**: 高コスト verifier の前段に安価なゲートを置き、明らかに無効な ChangeOp を早期 reject
すれば重い呼び出しを減らせる ([[project_idea_predictive_verification]])。

**モデル** (`llive/src/llive/evolution/predictive_gate_bench.py`): invalid 候補をゲートが
recall で捕捉、通過分だけ重い verifier へ。cheap=0.5ms / verify=50ms。

**結果**:

| invalid 率 | コスト削減 | verify 呼出削減 | 有効候補 誤却下 |
|---|---|---|---|
| 30% | 29% | 30% | 4.4% |
| 60% | 55% | 56% | 3.8% |
| 90% | **80%** | 81% | 2.7% |

**honest disclosure**: invalid 率が高いほど (panic burst 等) 削減大。コスト = 有効候補の
~3-4% を誤却下 (良い ChangeOp を喪失)。recall=0 では純オーバーヘッド。

### 1.5 KV-cache mesh 差分共有 (Gemini #2, llmesh)

**仮説**: mesh 間で KV cache 差分を共有すれば、prefix のローカル再計算 (prefill) より速い
([[project_idea_kv_cache_memory_translator]])。

**モデル** (`llmesh/speculative/kv_diff_bench.py`): transfer =
`net + diff_mb/bw + apply + sign`、`diff_mb = kv_size · diff_ratio`。

**結果**:

| scenario | diff 0.05 / 0.2 / 0.5 / 0.9 | break-even diff_ratio |
|---|---|---|
| LAN long-context | **29.85x** / 8.10x / 3.29x / 1.84x | 1.00 (常に win) |
| LAN short-context | 15.38x / 6.45x / 2.99x / 1.74x | 1.00 |
| WAN long-context | 0.33x / 0.09x / 0.04x / 0.02x | <0.01 (勝てない) |

**honest disclosure**: LAN は全 locality で win、locality 高 (差分小) ほど得。WAN は帯域
ボトルネックで全敗 (200MB 転送が秒単位)。実 KV 一貫性は未検証。

---

## 2. 組み合わせ PoC (3)

### 2.1 Combo-A — Antifragile × Speculative Mesh (llive `combo_bench.py`)

panic の探索候補を idle mesh peer へ並行投機すると、脱出率 100% を保ちつつ 1 世代の
wall-clock が並行度分の 1 に。

| 並行度 W | 脱出率 | wall-clock speedup |
|---|---|---|
| 1 | 100% | 0.91x (mesh overhead で純損) |
| 2 / 4 / 8 | 100% | 1.82x / 3.41x / **6.82x** |

synergy: antifragile が「脱出を可能にし」、mesh が「各 panic 世代を高速化する」二段効果。

### 2.2 Combo-B — Speculative Mesh × KV-cache 差分 (llmesh `combo_bench.py`)

KV 差分暖機で peer の exec_ms が縮む → 投機が lead time 内に終わる確率↑ (実効 hit_rate↑) +
miss 時の無駄計算↓。base_exec=40ms / lead=30ms / acc=0.8。

| 差分率 | exec cold→warm | hit_rate cold→warm | speedup cold→warm | miss 無駄 |
|---|---|---|---|---|
| 0.05 | 40→13.4ms | 0.60→0.80 | 2.40x→**4.52x** | 0.34 |
| 0.50 | 40→26.0ms | 0.60→0.80 | 2.40x→4.52x | 0.65 |
| 0.90 | 40→37.2ms | 0.60→0.65 | 2.40x→2.69x | 0.93 |

synergy: locality が高いほど暖機効果が大きく、speculative の hit_rate と speedup を押し上げる。

### 2.3 Combo-C — Antifragile × 予測検証ゲート (llive `combo_bench.py`)

panic は無効 ChangeOp の burst を生む → 前段ゲートがこの高 invalid burst で最大効果。

- 平均 panic 世代: 47.8 / 60
- panic 区間のみの削減: **80%** (invalid 90%) / 通常区間のみ: 25% (invalid 30%)
- **run 全体の verifier コスト削減: 69%**

synergy: antifragile が gate の価値を増幅 (panic が run の大半を占めるため)。

---

## 3. 横断発見

- **LAN 前提が mesh 系 (Speculative / KV-cache) の必須条件** — WAN は帯域・往復で全敗。
  産業 on-prem (LAN) が FullSense の主戦場であることと整合。
- すべて**予測符号化アーキテクチャ** (発見A) と整合: 予測を先に立て、誤差/差分だけ流す/計算する。
- コストの正直な計上: Antifragile の panic は評価爆発 (電力)、Speculative は低 hit_rate で
  wasted_compute、IBPO は品質劣化。latency が得でも犠牲は残る。

---

## 4. 眼鏡 — PoC メタ評価 (単に高速 ≠ 採用)

`fullsense/tools/poc_lens.py` (lleval 流評価レンズ, 自己検証 assert 込)。自作 PoC の speedup を
そのまま信じず、品質犠牲 / 隠れコスト / 汎化リスク / self-preference で採点し trust 0..1 を出す。

| PoC | trust | verdict |
|---|---|---|
| Speculative Mesh | 0.47 | 実測で再検証 |
| Antifragile | 0.35 | 実測で再検証 (landscape rigged) |
| 適応推論予算 (IBPO) | 0.47 | 実測で再検証 (速いが間違える) |
| 予測検証ゲート (#1) | **0.72** | 有望 (低疑い) |
| KV-cache 差分 (#2) | 0.60 | 実測で再検証 |
| Combo-A | 0.35 | 実測で再検証 |
| Combo-B | 0.60 | 実測で再検証 |
| Combo-C | 0.47 | 実測で再検証 |

**結論**: どの PoC も **trust=1.0 (無条件採用) にならない** (全 simulation)。self-preference が
重い Antifragile / Combo-A,C は採用保留。最も疑い低は予測検証ゲート (#1)。
**速い結果ほど内訳を疑い、実測で上書きする** ([[feedback_benchmark_honest_disclosure]] /
[[feedback_rust_usage_matters]])。

---

## 5. 優先付けと本格導入への道筋

- **Tier 1**: Speculative Mesh (要件済, Combo-A/B の基盤)。本格導入は SPEC-MESH-01
  (予測器 hit_rate 単体測定) から。
- **Tier 2**: 適応推論予算 (IBPO, frozen core 非干渉) + 予測検証ゲート (#1, Antifragile と synergy)。
- **Tier 3**: Antifragile (脱出は決定的だが panic コスト高 + rigged toy), KV-cache 差分
  (LAN 前提, 実装重め)。
- 各 simulation 値は実 transport / executor / fitness 配線後に**実測で上書き**。結合
  (要素統合) 判断は**ユーザー** (FullSense 規約)。

---

## 6. 再現コマンド

```
# llmesh
py -3.11 -m llmesh.speculative.bench          # Speculative Mesh break-even
py -3.11 -m llmesh.speculative.kv_diff_bench   # KV-cache 差分
py -3.11 -m llmesh.speculative.combo_bench     # Combo-B
# llive
py -3.11 -m llive.evolution.antifragile_bench  # Antifragile 脱出
py -3.11 -m llive.perf.adaptive_budget_bench   # IBPO
py -3.11 -m llive.evolution.predictive_gate_bench  # 予測検証ゲート
py -3.11 -m llive.evolution.combo_bench        # Combo-A / Combo-C
# fullsense (眼鏡)
py -3.11 tools/poc_lens.py
```

## 7. Sources / commits

- 単体: llmesh `2a05f64`/`b1d95e6`/`e7ced23` (Speculative/KV) / llive `aff62ab`/`81212a8`/`d9113ae`
  (Antifragile/IBPO/Gate)
- 組み合わせ: llive `5d51f3b` (A/C) / llmesh `65672d5` (B)
- 眼鏡 + 集約: fullsense `8d00650`
- 要約マトリクス: `docs/research/acceleration_poc_matrix_2026_05_24.md`
- 要件 (Tier1): `llmesh/docs/requirements_speculative_mesh.md`
- 上流: [[project_acceleration_poc_program_2026_05_24]] / `docs/research/gemini_brainstorm_impl_2026_05_24.md`
