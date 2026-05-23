---
title: 'llive 完全解説 (4) — 「収束する脳」B-series: SynapticSelector / UCB1 / Hebbian / 本番 hot path'
tags:
  - FullSense
  - llive
  - 解説
private: true
updated_at: '2026-05-23'
id: e5093e4816b25c1bd4d0
organization_url_name: null
slide: false
ignorePublish: false
---
言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# llive 完全解説 (4) — 「収束する脳」B-series: SynapticSelector / UCB1 / Hebbian / 本番 hot path

![hero — UCB1 bandit arm selection and score curve](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_hero.svg)

![連載進捗 (4/8) — 現在: B-series](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_progress.svg)

> **コンセプト hook**: 進化系 (GA / Genetic Algorithm) は世代を回して **探索**
> する. 一方 llive の SynapticSelector は **収束** — 確率的選択を 1 か所に
> 落とし込むエンジン. この 2 つを「同じ脳」に同居させると, **シナプス単位の
> 速い収束** と **個体単位の遅い探索** が干渉せず, 「速い小脳」と「遅い大脳」が
> 役割分担する.
>
> 本記事はその「速い小脳側」 — B-series (B-0 〜 B-9) の設計と本番投入を,
> ベンチ数値 + honest disclosure 付きで辿る.

![theme — B-series ε-greedy bandit + UCB1 (animated)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_theme.svg)

## 0. 連載中での位置づけ

```
#24-00 series index
#24-01 4 層メモリ
#24-02 思考因子 10 軸 + COG-MESH
#24-03 構造進化と TRIZ
#24-04 B-series: SynapticSelector / UCB1 / Hebbian (← 本記事)
#24-05 EvolutionLoop: v0.B/C/D/E 派生集団進化
#24-06 LLM backend: 非 Transformer 系 (Mamba / RWKV)
#24-07 observability + governance
#24-08 lleval — eval framework
```

#24-05 (集団 GA) が「**遅い大脳側**」, 本記事 (#24-04, B-series) が「**速い小脳側**」.
両者は同居しても干渉しない: SynapticSelector は **同一個体内** の synapse 選択,
GA は **個体間** の競争. 直交.

## 1. B-series の歴史

| B-ID | 内容 | 着地 |
|---|---|---|
| B-0 | SynapticSelector skeleton (純 random) | 着地済 |
| B-1 | UCB1 ベースの synapse 選択 (Auer 2002) | 着地済 |
| B-2 | Hebbian 強化 — 共起選択 bonus | 着地済 |
| B-3 | Cool-down 期間 — 同じ synapse 連続選択を緩和 | 着地済 |
| B-4 | A/B parity test (random vs UCB) | 着地済 |
| B-5 | Variant catalog (cosine / decay / blend) | 着地済 |
| B-6 | Per-synapse statistics + JSON snapshot | 着地済 |
| B-7 | Reset on regression — score 急落で priors リセット | 着地済 |
| B-8 | Self-tuning exploration constant | 着地済 |
| **B-9-a** | Production hot path: `assume_normalized` (skip 不要 normalize) | 着地済 |
| **B-9-b** | Production hot path: `GiftValue deque` (O(1) push/pop) | 着地済 |

## 2. SynapticSelector の核 — UCB1

LLM 推論の各 layer / each token 生成タイミングで, llive は **複数の synapse
variant** から 1 つを選んで通す. 純 random でも動くが, それでは「過去にうまく
いった variant」を学習しない. そこで UCB1.

```
score(variant_i) = mean_reward(i) + exploration * sqrt( ln(N) / n_i )
```

- `mean_reward(i)`: その variant が選ばれた過去の reward 平均.
- `exploration`: hyperparameter. B-8 で self-tuning.
- `N`: 全 variant 合計の試行回数.
- `n_i`: variant i の試行回数.

「使った数が少ないやつほど + 結果が良かったやつほど 高 score」 = exploration と
exploitation を 1 式に同居. Auer 2002 の古典. llive の B-1 で synapse 単位に
そのまま適用.

## 3. Hebbian — 共起のボーナス

UCB1 だけでは「1 つの variant が単独で当たる」のは検出できるが「**A と B が
一緒のときに当たる**」は検出できない. そこで B-2 で Hebbian 強化:

```
if t-1 で variant_A が選ばれ, t で variant_B が選ばれ, reward が高い
  → bonus(A, B) を +1
```

これで「A の直後に B」のような **時系列共起パターン** が UCB1 の score に
ブーストとして乗る. これは Hebb の "fire together, wire together" を強化学習
の選択器に持ち込んだもの.

## 4. B-9 production hot path

B-0 〜 B-8 は **アルゴリズム整備**. B-9 で **本番性能** に踏み込む.

### 4.1 B-9-a — `assume_normalized`

llive の中で SynapticSelector は memory 読み出し ↔ generation の hot path に
噛む. 当初は **毎回 vector を l2-normalize** していた:

```python
def select(self, query_vec):
    q = self._normalize(query_vec)  # ← every call
    ...
```

呼び出し前に既に normalized であることを契約として保証できる場面では,
この normalize は **完全に無駄**. そこで `assume_normalized=True` flag を
追加:

```python
selector = SynapticSelector(..., assume_normalized=True)
# 呼び出し側が正規化済を保証
```

Production hot path で **約 12% スループット改善** (実測). B-9-a で着地.

### 4.2 B-9-b — `GiftValue deque`

UCB1 の `mean_reward(i)` は historical reward の **rolling average**. 当初は
`list` を `pop(0)` で先頭から消していた → **O(N)**. variant が 256 個並ぶ
hot path で list pop は SR-02 ベンチで毎秒 8K 回 = 8K × O(N) 浮かぶ.

`collections.deque(maxlen=K)` に置換 → **O(1)**. これだけで:

- list pop O(N) 経路: ~ 1.8μs/call
- deque maxlen 経路: ~ 0.15μs/call → **12x**

production hot path 全体で **約 22% スループット改善**. B-9-b 着地.

### 4.3 honest disclosure — 12% + 22% ≠ 34%

「両方やったら 34% 改善か?」は短絡. ベンチでは:

- B-9-a 単独: +12.3% (95% CI ±0.8%)
- B-9-b 単独: +21.7% (95% CI ±1.2%)
- B-9-a + B-9-b 同時: **+28.4%** (95% CI ±1.5%)

= 重ねがけは複合せず. なぜか? B-9-a で normalize 削った分の処理時間に
B-9-b の deque 改善が **既に上限近くで頭打ち**. これは「異常に良い結果が出たら
必ず内訳を疑う」の実例. **削減幅は重複領域がある**.

## 5. 5x gate と Rust

llive Rust 拡張 (RUST-FX) は「Python 比 **5x 以上** の速度向上」を要件にする.
B-series で hot path 化した `assume_normalized` + deque は Python のままだが,
さらに Rust 化すべきかは別議論:

- 現状 production 28% 改善で **Python 維持の方が安全** (依存複雑性が低い).
- Rust 化候補は別件 — `compute_surprise` (cosine MEM-07) と
  `edge_weight bulk_time_decay` (RUST-03) は既に Rust 経路で **平均 16.18x**.

つまり「B-series は Python でチューニングを着地. その隣で Rust kernel が
別 hot path を持っている」が現状の design split.

## 6. 「速い小脳」と「遅い大脳」が干渉しない理由

llive は同一プロセスで:

- **SynapticSelector** (B-series, 同一個体内 synapse 単位の収束)
- **EvolutionLoop** (#24-05, 個体間 GA の探索)

を同時に回す. これが「衝突しないか?」は当然問われる. 答え:

- SynapticSelector は **個体内 state**. 1 回の inference に対し 256 synapse
  まで選択を回す. これは **ミリ秒〜マイクロ秒** スケール.
- EvolutionLoop は **個体間 state**. 64 個体集団を 1 世代回すのは **秒〜分**.
- 両者は時間スケールが 1000x 違う = 干渉する余地がほぼない.

これは生物の脳でも同じ: 小脳 (motor / reflex) と大脳 (planning) は時間スケールが
全く違う. llive は意図せずその二重時間スケール構造を持っている.

## 7. 数字で見る B-series 着地

| 指標 | 着地時 |
|---|---|
| B-0/B-1 着地時 throughput baseline | 100% |
| B-9-a 着地後 | **112%** (+12.3%) |
| B-9-b 着地後 | **122%** (+21.7%) |
| B-9-a + B-9-b 同時 | **128%** (+28.4%) |
| Rust kernel (MEM-07 + RUST-03) | 上記とは別 hot path で **16.18x** 平均 |

ベンチは `benches/bench_synaptic_b9_production.py` および
`benches/bench_rust_ext_5x_gate.py` を参照 (リポジトリ内). 95% CI と
方法論は同 dir の README に.

## 8. 次に来るもの

- **#24-05** で「遅い大脳側」 — EvolutionLoop / v0.B/C/D/E 派生集団進化を
  扱う. B-series で固めた「速い収束」とどう同居するかをそこで対比する.
- **RUST-15** (v0.7) — persona_dissimilarity を Rust 化. これは B-series
  ではなく E.17 quality-diversity の hot path. 5x gate 適用.

## 9. 2026-05-22 追記 — 「速い小脳 (Python 最適化)」と「遅い大脳 (Rust 化)」が直交する実例

本記事 (B-series) と #24-05 (EvolutionLoop) は **時間スケール 1000x 違う**
と書いた. 翌日 (2026-05-22) の RUST 高速化マラソンで, この直交性が **実装
レベルでも保たれる**ことが実証された.

### 9.1 B-series 側 — Python 最適化が効く

B-9 (`assume_normalized` + `GiftValue deque`) は **Python のままで +28%**.
これは **推論 hot path** (synapse 1 個あたり μs 単位) で, **FFI overhead を
払う余裕が無い**ため Rust 化は逆に遅くなる (`feedback_rust_usage_matters`
判定表 A).

### 9.2 EvolutionLoop 側 — Rust 化が効く

世代単位 (秒〜分) の集団進化では数値が真逆:

- **RUST-15** persona_dissimilarity batch: avg **x12.71** (N=64 で x17.07)
- **RUST-16** collusion_score: avg **x66.70** (N=8 で x115.04)
- **RUST-17** novelty_score_batch: avg x5.01 (archive 大で境界線)

### 9.3 直交性が崩れない理由

| 層 | 時間スケール | 最適化手段 | 理由 |
|---|---|---|---|
| **小脳 (B-series)** | μs/call | **Python チューニング** (normalize スキップ / deque) | FFI 払えないほど call が短い |
| **大脳 (EvolutionLoop)** | 秒〜分/generation | **Rust 化** (batch / numpy zero-copy) | numpy 小 N の API overhead が支配的 |

これは **生物の脳の小脳 / 大脳** と同じ. 違う時間スケールの計算には違う
最適化手段が要る — 同じ言語 / 同じツールで両方を解こうとすると失敗する.

### 9.4 honest disclosure — 「Rust 化 = 速い」も「Python 最適化 = 限界」も嘘

両方とも条件付き. 判定軸は **どの時間スケールで何を回しているか**:

- **μs スケールの hot path** → Python 最適化が主. FFI は overhead.
- **秒スケールの batch** → Rust + numpy zero-copy + batch が主. Python だと
  numpy API 多用の Python overhead が支配的.

詳細は `docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md`
の **5 パターン判定表** (A/B/C/D/E).

## 10. References

- Auer, P., Cesa-Bianchi, N. & Fischer, P. (2002). *Finite-time analysis of the multiarmed bandit problem*.
- Hebb, D. O. (1949). *The Organization of Behavior*.
- Sutton, R. & Barto, A. (2018). *Reinforcement Learning: An Introduction* (2nd ed.).
- 完全リストは v0.6.0a1 リリース時に references.bib に同梱予定.

---

## Series Navigation

- ← 前: [llive 完全解説 (3) 「矛盾は計算できる」](https://qiita.com/furuse-kazufumi/private/fa0890f136636d495ea6)
- → 次: [llive 完全解説 (5) 「集団が学ぶ AI」](https://qiita.com/furuse-kazufumi/private/07b686ea311e06027f94)
- 全体: [llive 完全解説 (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

# English

# llive Complete Guide (4) — "The Converging Brain" B-series: SynapticSelector / UCB1 / Hebbian / production hot paths

![hero — UCB1 bandit arm selection and score curve](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_hero_en.svg)

![series progress (4/8) — current: B-series](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_progress_en.svg)

> **Concept hook**: An evolutionary system (GA / Genetic Algorithm) runs
> generations to **explore**. llive's SynapticSelector, by contrast, **converges** —
> an engine that pins probabilistic choice into one place. When you co-house these
> two in "the same brain", the **fast convergence per synapse** and the **slow
> exploration per individual** do not interfere, and a "fast cerebellum" and a
> "slow cerebrum" divide the labor.
>
> This article traces that "fast cerebellum side" — the design and production
> rollout of the B-series (B-0 .. B-9), with benchmark numbers + honest disclosure.

![theme — B-series ε-greedy bandit + UCB1 (animated)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_theme_en.svg)

## 0. Position within the series

```
#24-00 series index
#24-01 4-layer memory
#24-02 thought factors (10 axes) + COG-MESH
#24-03 structural evolution and TRIZ
#24-04 B-series: SynapticSelector / UCB1 / Hebbian (← this article)
#24-05 EvolutionLoop: v0.B/C/D/E derived-population evolution
#24-06 LLM backend: non-Transformer (Mamba / RWKV)
#24-07 observability + governance
#24-08 lleval — eval framework
```

#24-05 (population GA) is the "**slow cerebrum side**"; this article (#24-04,
B-series) is the "**fast cerebellum side**". The two coexist without interference:
SynapticSelector picks synapses **inside one individual**, while the GA is a
competition **across individuals**. Orthogonal.

## 1. History of the B-series

| B-ID | Content | Status |
|---|---|---|
| B-0 | SynapticSelector skeleton (pure random) | landed |
| B-1 | UCB1-based synapse selection (Auer 2002) | landed |
| B-2 | Hebbian reinforcement — co-occurrence selection bonus | landed |
| B-3 | Cool-down period — relaxes consecutive selection of the same synapse | landed |
| B-4 | A/B parity test (random vs UCB) | landed |
| B-5 | Variant catalog (cosine / decay / blend) | landed |
| B-6 | Per-synapse statistics + JSON snapshot | landed |
| B-7 | Reset on regression — reset priors on a score crash | landed |
| B-8 | Self-tuning exploration constant | landed |
| **B-9-a** | Production hot path: `assume_normalized` (skip unneeded normalize) | landed |
| **B-9-b** | Production hot path: `GiftValue deque` (O(1) push/pop) | landed |

## 2. Core of SynapticSelector — UCB1

At each LLM layer / each token-generation timing, llive picks one from **multiple
synapse variants** to pass through. Pure random works, but then it does not learn
"the variant that worked well in the past". Hence UCB1.

```
score(variant_i) = mean_reward(i) + exploration * sqrt( ln(N) / n_i )
```

- `mean_reward(i)`: the past reward average when this variant was chosen.
- `exploration`: hyperparameter. Self-tuned in B-8.
- `N`: total number of trials across all variants.
- `n_i`: number of trials for variant i.

"the fewer times it has been used + the better it scored → the higher its score" =
exploration and exploitation co-housed in a single formula. The Auer 2002 classic.
Applied directly per synapse in llive's B-1.

## 3. Hebbian — the co-occurrence bonus

UCB1 alone can detect "one variant wins on its own", but not "**A and B win when
together**". Hence Hebbian reinforcement in B-2:

```
if variant_A was chosen at t-1, variant_B at t, and reward is high
  → bonus(A, B) += 1
```

This makes a **time-series co-occurrence pattern** like "B right after A" ride on
top of the UCB1 score as a boost. This brings Hebb's "fire together, wire together"
into a reinforcement-learning selector.

## 4. B-9 production hot path

B-0 .. B-8 are **algorithm groundwork**. B-9 steps into **production performance**.

### 4.1 B-9-a — `assume_normalized`

Inside llive, SynapticSelector bites into the hot path of memory readout ↔
generation. Initially it would **l2-normalize the vector every time**:

```python
def select(self, query_vec):
    q = self._normalize(query_vec)  # ← every call
    ...
```

In situations where we can guarantee, as a contract, that the input is already
normalized before the call, this normalize is **completely wasted**. So we added an
`assume_normalized=True` flag:

```python
selector = SynapticSelector(..., assume_normalized=True)
# the caller guarantees it is already normalized
```

**About 12% throughput improvement** in the production hot path (measured). Landed
in B-9-a.

### 4.2 B-9-b — `GiftValue deque`

UCB1's `mean_reward(i)` is a **rolling average** of historical reward. Initially we
deleted from the front of a `list` with `pop(0)` → **O(N)**. In a hot path where
256 variants line up, list pop runs 8K times per second in the SR-02 benchmark =
8K × O(N).

Replacing with `collections.deque(maxlen=K)` → **O(1)**. With just this:

- list pop O(N) path: ~ 1.8μs/call
- deque maxlen path: ~ 0.15μs/call → **12x**

**About 22% throughput improvement** across the whole production hot path. Landed
in B-9-b.

### 4.3 honest disclosure — 12% + 22% ≠ 34%

"If you do both, is it 34% improvement?" is a shortcut. In the benchmark:

- B-9-a alone: +12.3% (95% CI ±0.8%)
- B-9-b alone: +21.7% (95% CI ±1.2%)
- B-9-a + B-9-b together: **+28.4%** (95% CI ±1.5%)

= stacking does not compound. Why? In the processing time freed by removing the
normalize in B-9-a, B-9-b's deque improvement is **already near its ceiling**. This
is a worked example of "when an abnormally good result appears, always doubt the
breakdown". **The reduction has an overlapping region**.

## 5. The 5x gate and Rust

llive's Rust extension (RUST-FX) makes "at least **5x** speedup vs Python" a
requirement. The `assume_normalized` + deque that we hot-pathed in the B-series stay
in Python, but whether to Rust-port them further is a separate discussion:

- At the current 28% production improvement, **staying in Python is safer** (lower
  dependency complexity).
- The Rust-port candidates are separate — `compute_surprise` (cosine MEM-07) and
  `edge_weight bulk_time_decay` (RUST-03) are already **avg 16.18x** on the Rust path.

So "the B-series lands tuning in Python, while a Rust kernel holds a different hot
path next to it" is the current design split.

## 6. Why the "fast cerebellum" and "slow cerebrum" do not interfere

llive runs, in the same process:

- **SynapticSelector** (B-series, convergence per synapse inside one individual)
- **EvolutionLoop** (#24-05, exploration of the GA across individuals)

at the same time. "Won't they collide?" is naturally asked. The answer:

- SynapticSelector is **per-individual state**. For one inference it runs selection
  across up to 256 synapses. This is a **millisecond–microsecond** scale.
- EvolutionLoop is **cross-individual state**. Running one generation of a 64-individual
  population is **seconds–minutes**.
- The two are 1000x apart in time scale = almost no room to interfere.

This is the same in the biological brain: the cerebellum (motor / reflex) and the
cerebrum (planning) operate at completely different time scales. llive
unintentionally has that dual-time-scale structure.

## 7. The B-series landing by the numbers

| Metric | At landing |
|---|---|
| throughput baseline at B-0/B-1 landing | 100% |
| after B-9-a landing | **112%** (+12.3%) |
| after B-9-b landing | **122%** (+21.7%) |
| B-9-a + B-9-b together | **128%** (+28.4%) |
| Rust kernel (MEM-07 + RUST-03) | **16.18x** avg on a separate hot path |

The benchmarks are at `benches/bench_synaptic_b9_production.py` and
`benches/bench_rust_ext_5x_gate.py` (in the repo). The 95% CI and methodology are
in the README of the same dir.

## 8. What comes next

- **#24-05** covers the "slow cerebrum side" — EvolutionLoop / v0.B/C/D/E
  derived-population evolution. There we contrast how it coexists with the "fast
  convergence" solidified in the B-series.
- **RUST-15** (v0.7) — Rust-port persona_dissimilarity. This is not the B-series but
  the hot path of E.17 quality-diversity. The 5x gate applies.

## 9. 2026-05-22 addendum — a worked example where "fast cerebellum (Python optimization)" and "slow cerebrum (Rust port)" are orthogonal

We wrote that this article (B-series) and #24-05 (EvolutionLoop) operate at **time
scales 1000x apart**. In the next day's (2026-05-22) Rust-speedup marathon, this
orthogonality was demonstrated to **hold at the implementation level too**.

### 9.1 The B-series side — Python optimization works

B-9 (`assume_normalized` + `GiftValue deque`) is **+28% while staying in Python**.
This is an **inference hot path** (microseconds per synapse), where there is **no
room to pay FFI overhead**, so a Rust port is actually slower (`feedback_rust_usage_matters`
decision table, pattern A).

### 9.2 The EvolutionLoop side — the Rust port works

For per-generation (seconds–minutes) population evolution the numbers are reversed:

- **RUST-15** persona_dissimilarity batch: avg **x12.71** (x17.07 at N=64)
- **RUST-16** collusion_score: avg **x66.70** (x115.04 at N=8)
- **RUST-17** novelty_score_batch: avg x5.01 (borderline with a large archive)

### 9.3 Why the orthogonality does not break

| Layer | Time scale | Optimization means | Reason |
|---|---|---|---|
| **cerebellum (B-series)** | μs/call | **Python tuning** (skip normalize / deque) | calls too short to pay FFI |
| **cerebrum (EvolutionLoop)** | sec–min/generation | **Rust port** (batch / numpy zero-copy) | numpy small-N API overhead dominates |

This is the same as the cerebellum / cerebrum of the biological brain. Computations
at different time scales need different optimization means — trying to solve both
with the same language / same tool fails.

### 9.4 honest disclosure — "Rust = fast" and "Python optimization = limited" are both lies

Both are conditional. The deciding axis is **at which time scale you are running
what**:

- **μs-scale hot path** → Python optimization is primary. FFI is overhead.
- **second-scale batch** → Rust + numpy zero-copy + batch is primary. In Python the
  Python overhead of heavy numpy API use dominates.

Details in the **5-pattern decision table** (A/B/C/D/E) in
`docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md`.

## 10. References

- Auer, P., Cesa-Bianchi, N. & Fischer, P. (2002). *Finite-time analysis of the multiarmed bandit problem*.
- Hebb, D. O. (1949). *The Organization of Behavior*.
- Sutton, R. & Barto, A. (2018). *Reinforcement Learning: An Introduction* (2nd ed.).
- The full list will be bundled in references.bib at the v0.6.0a1 release.

---

## Series Navigation

- ← Prev: [llive Complete Guide (3) "Contradictions Can Be Computed"](https://qiita.com/furuse-kazufumi/private/fa0890f136636d495ea6)
- → Next: [llive Complete Guide (5) "The Population that Learns"](https://qiita.com/furuse-kazufumi/private/07b686ea311e06027f94)
- All: [llive Complete Guide (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

# 中文

# llive 完全解说 (4) — "收敛的大脑" B-series: SynapticSelector / UCB1 / Hebbian / 生产环境热点

![hero — UCB1 bandit arm selection and score curve](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_hero_zh.svg)

![连载进度 (4/8) — 当前: B-series](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_progress_zh.svg)

> **概念 hook**: 进化系 (GA / Genetic Algorithm) 通过跑世代来 **探索**. 而 llive 的
> SynapticSelector 是 **收敛** — 把概率性选择落到 1 处的引擎. 把这两者同居在「同一个
> 大脑」里, **synapse 级的快速收敛** 与 **个体级的慢速探索** 不互相干扰,「快速小脑」
> 和「慢速大脑」分工合作.
>
> 本文追溯其「快速小脑侧」 — B-series (B-0 〜 B-9) 的设计与生产投入, 附带基准数值 +
> honest disclosure.

![theme — B-series ε-greedy bandit + UCB1 (animated)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_theme_zh.svg)

## 0. 在系列中的定位

```
#24-00 series index
#24-01 4 层记忆
#24-02 思考因子 10 轴 + COG-MESH
#24-03 结构进化与 TRIZ
#24-04 B-series: SynapticSelector / UCB1 / Hebbian (← 本文)
#24-05 EvolutionLoop: v0.B/C/D/E 派生群体进化
#24-06 LLM backend: 非 Transformer 系 (Mamba / RWKV)
#24-07 observability + governance
#24-08 lleval — eval framework
```

#24-05 (群体 GA) 是「**慢速大脑侧**」, 本文 (#24-04, B-series) 是「**快速小脑侧**」.
两者同居也不互相干扰: SynapticSelector 在 **同一个体内** 选择 synapse, GA 是
**个体间** 的竞争. 正交.

## 1. B-series 的历史

| B-ID | 内容 | 着地 |
|---|---|---|
| B-0 | SynapticSelector skeleton (纯 random) | 已着地 |
| B-1 | 基于 UCB1 的 synapse 选择 (Auer 2002) | 已着地 |
| B-2 | Hebbian 强化 — 共现选择 bonus | 已着地 |
| B-3 | Cool-down 期间 — 缓和同一 synapse 连续选择 | 已着地 |
| B-4 | A/B parity test (random vs UCB) | 已着地 |
| B-5 | Variant catalog (cosine / decay / blend) | 已着地 |
| B-6 | Per-synapse statistics + JSON snapshot | 已着地 |
| B-7 | Reset on regression — score 急落时 reset priors | 已着地 |
| B-8 | Self-tuning exploration constant | 已着地 |
| **B-9-a** | Production hot path: `assume_normalized` (跳过不必要的 normalize) | 已着地 |
| **B-9-b** | Production hot path: `GiftValue deque` (O(1) push/pop) | 已着地 |

## 2. SynapticSelector 的内核 — UCB1

在 LLM 推理的每个 layer / 每次 token 生成时, llive 从 **多个 synapse variant** 中选 1
个通过. 纯 random 也能跑, 但那样不会学习「过去成功的 variant」. 于是 UCB1.

```
score(variant_i) = mean_reward(i) + exploration * sqrt( ln(N) / n_i )
```

- `mean_reward(i)`: 该 variant 被选中时过去的 reward 平均.
- `exploration`: hyperparameter. 在 B-8 中 self-tuning.
- `N`: 全部 variant 合计的试验次数.
- `n_i`: variant i 的试验次数.

「用过次数越少 + 结果越好 → 分越高」= 把 exploration 与 exploitation 同居在 1 个式子里.
Auer 2002 的经典. 在 llive 的 B-1 中直接按 synapse 应用.

## 3. Hebbian — 共现的奖励

仅靠 UCB1 能检测出「1 个 variant 单独命中」, 但检测不出「**A 和 B 一起时命中**」.
于是 B-2 的 Hebbian 强化:

```
if t-1 选了 variant_A, t 选了 variant_B, 且 reward 高
  → bonus(A, B) += 1
```

这样「A 之后紧接 B」这样的 **时序共现模式** 就作为 boost 加到 UCB1 的 score 上.
这是把 Hebb 的 "fire together, wire together" 带进强化学习的选择器.

## 4. B-9 生产环境热路径

B-0 〜 B-8 是 **算法铺底**. B-9 进入 **生产级性能**.

### 4.1 B-9-a — `assume_normalized`

在 llive 中, SynapticSelector 咬住 memory 读出 ↔ generation 的 hot path. 最初是
**每次都对 vector 做 l2-normalize**:

```python
def select(self, query_vec):
    q = self._normalize(query_vec)  # ← every call
    ...
```

在能以契约保证调用前已 normalized 的场景下, 这个 normalize **完全是浪费**. 于是加了
`assume_normalized=True` flag:

```python
selector = SynapticSelector(..., assume_normalized=True)
# 调用方保证已正规化
```

在 production hot path 中 **约 12% 吞吐改善** (实测). 在 B-9-a 着地.

### 4.2 B-9-b — `GiftValue deque`

UCB1 的 `mean_reward(i)` 是 historical reward 的 **rolling average**. 最初用 `list`
的 `pop(0)` 从头删 → **O(N)**. 在排着 256 个 variant 的 hot path 中, list pop 在
SR-02 基准里每秒 8K 次 = 8K × O(N).

换成 `collections.deque(maxlen=K)` → **O(1)**. 仅此:

- list pop O(N) 路径: ~ 1.8μs/call
- deque maxlen 路径: ~ 0.15μs/call → **12x**

整个 production hot path **约 22% 吞吐改善**. B-9-b 着地.

### 4.3 honest disclosure — 12% + 22% ≠ 34%

「两个都做就是 34% 改善吗?」是短路. 在基准里:

- B-9-a 单独: +12.3% (95% CI ±0.8%)
- B-9-b 单独: +21.7% (95% CI ±1.2%)
- B-9-a + B-9-b 同时: **+28.4%** (95% CI ±1.5%)

= 叠加不会复合. 为什么? 在 B-9-a 削掉 normalize 所释放的处理时间里, B-9-b 的 deque 改善
**已经接近上限封顶**. 这是「出现异常好的结果必须怀疑其内訳」的实例. **削减幅度有重叠区域**.

## 5. 5 倍 gate 与 Rust

llive 的 Rust 扩展 (RUST-FX) 把「相对 Python **5 倍以上** 的提速」设为要件. B-series 中
hot path 化的 `assume_normalized` + deque 仍是 Python, 是否进一步 Rust 化是另一议题:

- 当前 production 28% 改善下 **维持 Python 更安全** (依赖复杂性低).
- Rust 化候选是另一件事 — `compute_surprise` (cosine MEM-07) 与
  `edge_weight bulk_time_decay` (RUST-03) 已在 Rust 路径上 **平均 16.18x**.

也就是「B-series 用 Python 把调优着地. 其旁边 Rust kernel 持有另一个 hot path」是当前的
design split.

## 6. 为什么「快速小脑」和「慢速大脑」不互相干扰

llive 在同一进程中:

- **SynapticSelector** (B-series, 同一个体内 synapse 级的收敛)
- **EvolutionLoop** (#24-05, 个体间 GA 的探索)

同时运行. 「会不会冲突?」当然会被问. 答案:

- SynapticSelector 是 **个体内 state**. 对 1 次 inference 跑最多 256 synapse 的选择.
  这是 **毫秒〜微秒** 尺度.
- EvolutionLoop 是 **个体间 state**. 把 64 个体群体跑 1 代是 **秒〜分**.
- 两者时间尺度相差 1000x = 几乎没有干扰的余地.

这与生物的大脑相同: 小脑 (motor / reflex) 和大脑 (planning) 的时间尺度完全不同. llive
无意间拥有那种双时间尺度结构.

## 7. 用数字看 B-series 的着地

| 指标 | 着地时 |
|---|---|
| B-0/B-1 着地时 throughput baseline | 100% |
| B-9-a 着地后 | **112%** (+12.3%) |
| B-9-b 着地后 | **122%** (+21.7%) |
| B-9-a + B-9-b 同时 | **128%** (+28.4%) |
| Rust kernel (MEM-07 + RUST-03) | 在另一个 hot path 上 **16.18x** 平均 |

基准在 `benches/bench_synaptic_b9_production.py` 与
`benches/bench_rust_ext_5x_gate.py` (仓库内). 95% CI 与方法论在同 dir 的 README.

## 8. 接下来要做的

- **#24-05** 看「慢速大脑侧」 — EvolutionLoop / v0.B/C/D/E 派生群体进化. 在那里对比它如何
  与本章固定的「快速收敛」共存.
- **RUST-15** (v0.7) — 把 persona_dissimilarity Rust 化. 这不是 B-series, 而是 E.17
  quality-diversity 的 hot path. 适用 5x gate.

## 9. 2026-05-22 追记 — 「快小脑 (Python 优化)」与「慢大脑 (Rust 化)」正交的实例

本文 (B-series) 与 #24-05 (EvolutionLoop) **时间尺度相差 1000x**, 我们如此写过. 在次日
(2026-05-22) 的 RUST 加速马拉松中, 这种正交性被证明 **在实现层面也成立**.

### 9.1 B-series 侧 — Python 优化有效

B-9 (`assume_normalized` + `GiftValue deque`) 是 **保持 Python 而 +28%**. 这是
**推理 hot path** (每个 synapse μs 级), **没有余地支付 FFI overhead**, 所以 Rust 化反而更慢
(`feedback_rust_usage_matters` 判定表 A).

### 9.2 EvolutionLoop 侧 — Rust 化有效

在世代级 (秒〜分) 的群体进化里数值正好相反:

- **RUST-15** persona_dissimilarity batch: avg **x12.71** (N=64 时 x17.07)
- **RUST-16** collusion_score: avg **x66.70** (N=8 时 x115.04)
- **RUST-17** novelty_score_batch: avg x5.01 (archive 大时在边界线)

### 9.3 正交性不崩溃的理由

| 层 | 时间尺度 | 优化手段 | 理由 |
|---|---|---|---|
| **小脑 (B-series)** | μs/call | **Python 调优** (跳过 normalize / deque) | call 太短付不起 FFI |
| **大脑 (EvolutionLoop)** | 秒〜分/generation | **Rust 化** (batch / numpy zero-copy) | numpy 小 N 的 API overhead 占主导 |

这与 **生物大脑的小脑 / 大脑** 相同. 不同时间尺度的计算需要不同的优化手段 — 用同一语言 /
同一工具想解决两者会失败.

### 9.4 honest disclosure — 「Rust 化 = 快」与「Python 优化 = 极限」都是谎言

两者都是有条件的. 判定轴是 **在哪个时间尺度上跑什么**:

- **μs 尺度的 hot path** → Python 优化为主. FFI 是 overhead.
- **秒尺度的 batch** → Rust + numpy zero-copy + batch 为主. Python 下 numpy API 多用的
  Python overhead 占主导.

详情见 `docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md` 的
**5 模式判定表** (A/B/C/D/E).

## 10. References

- Auer, P., Cesa-Bianchi, N. & Fischer, P. (2002). *Finite-time analysis of the multiarmed bandit problem*.
- Hebb, D. O. (1949). *The Organization of Behavior*.
- Sutton, R. & Barto, A. (2018). *Reinforcement Learning: An Introduction* (2nd ed.).
- 完整列表将在 v0.6.0a1 发布时随 references.bib 一同提供.

---

## Series Navigation

- ← 上一篇: [llive 完全解说 (3) 「矛盾是可以计算的」](https://qiita.com/furuse-kazufumi/private/fa0890f136636d495ea6)
- → 下一篇: [llive 完全解说 (5) 「学习的群体」](https://qiita.com/furuse-kazufumi/private/07b686ea311e06027f94)
- 全部: [llive 完全解说 (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)

---

# 한국어

# llive 완전 해설 (4) — "수렴하는 뇌" B-series: SynapticSelector / UCB1 / Hebbian / 프로덕션 hot path

![hero — UCB1 bandit arm selection and score curve](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_hero_ko.svg)

![연재 진행 (4/8) — 현재: B-series](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_progress_ko.svg)

> **콘셉트 hook**: 진화계 (GA / Genetic Algorithm)는 세대를 돌려 **탐색**한다. 한편
> llive의 SynapticSelector는 **수렴** — 확률적 선택을 한 곳에 떨어뜨리는 엔진이다.
> 이 둘을 「같은 뇌」에 동거시키면, **시냅스 단위의 빠른 수렴**과 **개체 단위의 느린
> 탐색**이 간섭하지 않고, 「빠른 소뇌」와 「느린 대뇌」가 역할을 분담한다.
>
> 본 글은 그 「빠른 소뇌 측」 — B-series (B-0 〜 B-9)의 설계와 프로덕션 투입을, 벤치
> 수치 + honest disclosure와 함께 따라간다.

![theme — B-series ε-greedy bandit + UCB1 (animated)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_theme_ko.svg)

## 0. 연재에서의 위치

```
#24-00 series index
#24-01 4층 메모리
#24-02 사고 인자 10축 + COG-MESH
#24-03 구조 진화와 TRIZ
#24-04 B-series: SynapticSelector / UCB1 / Hebbian (← 본 글)
#24-05 EvolutionLoop: v0.B/C/D/E 파생 집단 진화
#24-06 LLM backend: 비 Transformer 계 (Mamba / RWKV)
#24-07 observability + governance
#24-08 lleval — eval framework
```

#24-05 (집단 GA)가 「**느린 대뇌 측**」, 본 글 (#24-04, B-series)이 「**빠른 소뇌 측**」.
양자는 동거해도 간섭하지 않는다: SynapticSelector는 **동일 개체 내**의 synapse 선택,
GA는 **개체 간**의 경쟁. 직교.

## 1. B-series의 역사

| B-ID | 내용 | 착지 |
|---|---|---|
| B-0 | SynapticSelector skeleton (순수 random) | 착지됨 |
| B-1 | UCB1 기반의 synapse 선택 (Auer 2002) | 착지됨 |
| B-2 | Hebbian 강화 — 공기 선택 bonus | 착지됨 |
| B-3 | Cool-down 기간 — 같은 synapse 연속 선택 완화 | 착지됨 |
| B-4 | A/B parity test (random vs UCB) | 착지됨 |
| B-5 | Variant catalog (cosine / decay / blend) | 착지됨 |
| B-6 | Per-synapse statistics + JSON snapshot | 착지됨 |
| B-7 | Reset on regression — score 급락 시 priors 리셋 | 착지됨 |
| B-8 | Self-tuning exploration constant | 착지됨 |
| **B-9-a** | Production hot path: `assume_normalized` (불필요한 normalize 스킵) | 착지됨 |
| **B-9-b** | Production hot path: `GiftValue deque` (O(1) push/pop) | 착지됨 |

## 2. SynapticSelector의 핵심 — UCB1

LLM 추론의 각 layer / 매 token 생성 타이밍에서, llive는 **여러 synapse variant** 중 1개를
골라 통과시킨다. 순수 random으로도 동작하지만, 그래서는 「과거에 잘 된 variant」를 학습하지
않는다. 그래서 UCB1.

```
score(variant_i) = mean_reward(i) + exploration * sqrt( ln(N) / n_i )
```

- `mean_reward(i)`: 그 variant가 선택되었을 때 과거의 reward 평균.
- `exploration`: hyperparameter. B-8에서 self-tuning.
- `N`: 전 variant 합계의 시행 횟수.
- `n_i`: variant i의 시행 횟수.

「쓴 횟수가 적을수록 + 결과가 좋았을수록 높은 score」 = exploration과 exploitation을 1개의
식에 동거. Auer 2002의 고전. llive의 B-1에서 synapse 단위로 그대로 적용.

## 3. Hebbian — 공기의 보너스

UCB1만으로는 「1개의 variant가 단독으로 적중」은 검출할 수 있지만 「**A와 B가 함께일 때
적중**」은 검출할 수 없다. 그래서 B-2의 Hebbian 강화:

```
if t-1에서 variant_A가 선택되고, t에서 variant_B가 선택되며, reward가 높음
  → bonus(A, B) += 1
```

이로써 「A 직후에 B」 같은 **시계열 공기 패턴**이 UCB1의 score에 boost로 얹힌다. 이것은
Hebb의 "fire together, wire together"를 강화학습의 선택기에 가져온 것이다.

## 4. B-9 프로덕션 hot path

B-0 〜 B-8은 **알고리즘 정비**. B-9에서 **프로덕션 성능**에 들어간다.

### 4.1 B-9-a — `assume_normalized`

llive 안에서 SynapticSelector는 memory 읽기 ↔ generation의 hot path에 물린다. 처음에는
**매번 vector를 l2-normalize** 했다:

```python
def select(self, query_vec):
    q = self._normalize(query_vec)  # ← every call
    ...
```

호출 전에 이미 normalized임을 계약으로 보장할 수 있는 상황에서는, 이 normalize는 **완전히
낭비**다. 그래서 `assume_normalized=True` flag를 추가:

```python
selector = SynapticSelector(..., assume_normalized=True)
# 호출 측이 정규화됨을 보장
```

Production hot path에서 **약 12% 스루풋 개선** (실측). B-9-a에서 착지.

### 4.2 B-9-b — `GiftValue deque`

UCB1의 `mean_reward(i)`는 historical reward의 **rolling average**다. 처음에는 `list`를
`pop(0)`으로 앞에서 지웠다 → **O(N)**. variant가 256개 늘어선 hot path에서 list pop은
SR-02 벤치에서 초당 8K회 = 8K × O(N).

`collections.deque(maxlen=K)`로 교체 → **O(1)**. 이것만으로:

- list pop O(N) 경로: ~ 1.8μs/call
- deque maxlen 경로: ~ 0.15μs/call → **12x**

production hot path 전체에서 **약 22% 스루풋 개선**. B-9-b 착지.

### 4.3 honest disclosure — 12% + 22% ≠ 34%

「둘 다 하면 34% 개선인가?」는 단락이다. 벤치에서는:

- B-9-a 단독: +12.3% (95% CI ±0.8%)
- B-9-b 단독: +21.7% (95% CI ±1.2%)
- B-9-a + B-9-b 동시: **+28.4%** (95% CI ±1.5%)

= 겹쳐쓰기는 복합되지 않는다. 왜인가? B-9-a에서 normalize를 깎은 만큼의 처리 시간에 B-9-b의
deque 개선이 **이미 상한 가까이서 천장에 닿았다**. 이것은 「이상하게 좋은 결과가 나오면 반드시
내역을 의심한다」의 실례다. **삭감 폭에는 중복 영역이 있다**.

## 5. 5x gate와 Rust

llive의 Rust 확장 (RUST-FX)은 「Python 대비 **5x 이상**의 속도 향상」을 요건으로 한다.
B-series에서 hot path화한 `assume_normalized` + deque는 Python 그대로지만, 추가로 Rust화해야
하는가는 별도 논의다:

- 현재 production 28% 개선이면 **Python 유지가 더 안전** (의존 복잡성이 낮음).
- Rust화 후보는 별건 — `compute_surprise` (cosine MEM-07)와
  `edge_weight bulk_time_decay` (RUST-03)는 이미 Rust 경로에서 **평균 16.18x**.

즉 「B-series는 Python으로 튜닝을 착지. 그 옆에서 Rust kernel이 다른 hot path를 가진다」가
현재의 design split.

## 6. 「빠른 소뇌」와 「느린 대뇌」가 간섭하지 않는 이유

llive는 동일 프로세스에서:

- **SynapticSelector** (B-series, 동일 개체 내 synapse 단위의 수렴)
- **EvolutionLoop** (#24-05, 개체 간 GA의 탐색)

을 동시에 돌린다. 「충돌하지 않는가?」는 당연히 물어진다. 답:

- SynapticSelector는 **개체 내 state**. 1회의 inference에 대해 256 synapse까지 선택을 돌린다.
  이것은 **밀리초〜마이크로초** 스케일.
- EvolutionLoop는 **개체 간 state**. 64 개체 집단을 1세대 돌리는 것은 **초〜분**.
- 양자는 시간 스케일이 1000x 다르다 = 간섭할 여지가 거의 없다.

이것은 생물의 뇌에서도 같다: 소뇌 (motor / reflex)와 대뇌 (planning)는 시간 스케일이 전혀
다르다. llive는 의도치 않게 그 이중 시간 스케일 구조를 가지고 있다.

## 7. 숫자로 본 B-series 착지

| 지표 | 착지 시 |
|---|---|
| B-0/B-1 착지 시 throughput baseline | 100% |
| B-9-a 착지 후 | **112%** (+12.3%) |
| B-9-b 착지 후 | **122%** (+21.7%) |
| B-9-a + B-9-b 동시 | **128%** (+28.4%) |
| Rust kernel (MEM-07 + RUST-03) | 위와는 별도 hot path에서 **16.18x** 평균 |

벤치는 `benches/bench_synaptic_b9_production.py` 및
`benches/bench_rust_ext_5x_gate.py`를 참조 (리포지토리 내). 95% CI와 방법론은 같은 dir의
README에.

## 8. 다음에 오는 것

- **#24-05**에서 「느린 대뇌 측」 — EvolutionLoop / v0.B/C/D/E 파생 집단 진화를 다룬다.
  B-series에서 굳힌 「빠른 수렴」과 어떻게 동거하는지를 거기서 대비한다.
- **RUST-15** (v0.7) — persona_dissimilarity를 Rust화. 이것은 B-series가 아니라 E.17
  quality-diversity의 hot path. 5x gate 적용.

## 9. 2026-05-22 추기 — 「빠른 소뇌 (Python 최적화)」와 「느린 대뇌 (Rust화)」가 직교하는 실례

본 글 (B-series)과 #24-05 (EvolutionLoop)는 **시간 스케일 1000x 다르다**고 썼다. 다음 날
(2026-05-22)의 RUST 고속화 마라톤에서, 이 직교성이 **구현 레벨에서도 유지됨**이 실증되었다.

### 9.1 B-series 측 — Python 최적화가 효과적

B-9 (`assume_normalized` + `GiftValue deque`)는 **Python 그대로 +28%**. 이것은
**추론 hot path** (synapse 1개당 μs 단위)로, **FFI overhead를 지불할 여유가 없기** 때문에
Rust화는 오히려 느려진다 (`feedback_rust_usage_matters` 판정표 A).

### 9.2 EvolutionLoop 측 — Rust화가 효과적

세대 단위 (초〜분)의 집단 진화에서는 수치가 정반대:

- **RUST-15** persona_dissimilarity batch: avg **x12.71** (N=64에서 x17.07)
- **RUST-16** collusion_score: avg **x66.70** (N=8에서 x115.04)
- **RUST-17** novelty_score_batch: avg x5.01 (archive 클 때 경계선)

### 9.3 직교성이 무너지지 않는 이유

| 층 | 시간 스케일 | 최적화 수단 | 이유 |
|---|---|---|---|
| **소뇌 (B-series)** | μs/call | **Python 튜닝** (normalize 스킵 / deque) | call이 짧아 FFI를 못 지불 |
| **대뇌 (EvolutionLoop)** | 초〜분/generation | **Rust화** (batch / numpy zero-copy) | numpy 작은 N의 API overhead가 지배적 |

이것은 **생물 뇌의 소뇌 / 대뇌**와 같다. 다른 시간 스케일의 계산에는 다른 최적화 수단이
필요하다 — 같은 언어 / 같은 도구로 둘 다 풀려고 하면 실패한다.

### 9.4 honest disclosure — 「Rust화 = 빠름」도 「Python 최적화 = 한계」도 거짓

둘 다 조건부다. 판정 축은 **어느 시간 스케일에서 무엇을 돌리는가**:

- **μs 스케일의 hot path** → Python 최적화가 주. FFI는 overhead.
- **초 스케일의 batch** → Rust + numpy zero-copy + batch가 주. Python이면 numpy API 다용의
  Python overhead가 지배적.

자세히는 `docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md`의
**5 패턴 판정표** (A/B/C/D/E).

## 10. References

- Auer, P., Cesa-Bianchi, N. & Fischer, P. (2002). *Finite-time analysis of the multiarmed bandit problem*.
- Hebb, D. O. (1949). *The Organization of Behavior*.
- Sutton, R. & Barto, A. (2018). *Reinforcement Learning: An Introduction* (2nd ed.).
- 완전한 목록은 v0.6.0a1 릴리스 시 references.bib에 동봉할 예정.

---

## Series Navigation

- ← 이전: [llive 완전 해설 (3) 「모순은 계산할 수 있다」](https://qiita.com/furuse-kazufumi/private/fa0890f136636d495ea6)
- → 다음: [llive 완전 해설 (5) 「집단이 학습하는 AI」](https://qiita.com/furuse-kazufumi/private/07b686ea311e06027f94)
- 전체: [llive 완전 해설 (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
