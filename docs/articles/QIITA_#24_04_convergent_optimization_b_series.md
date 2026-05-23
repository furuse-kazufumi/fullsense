---
title: llive 完全解説 (4) — 「収束する脳」B-series: SynapticSelector / UCB1 / Hebbian / 本番 hot path
tags:
  - FullSense
  - llive
  - 解説
private: false
updated_at: '2026-05-22'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---
<!-- lead-trans-placed -->
<!-- h2-trans-placed -->

<!-- trilingual-subtitle-placed -->
<small><strong>EN:</strong> “The converging brain” B-series: SynapticSelector / UCB1 / Hebbian / production hot paths / <strong>中:</strong> "收敛的大脑" B-series: SynapticSelector / UCB1 / Hebbian / 生产环境热点</small>
<!-- section-separators-placed -->

# llive 完全解説 (4) — 「収束する脳」B-series: SynapticSelector / UCB1 / Hebbian / 本番 hot path

![hero — UCB1 bandit arm selection and score curve](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_hero.svg)

<!-- progress-svg-placed -->
![連載進捗 (4/8) — 現在: B-series](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_progress.svg)

> **コンセプト hook**: 進化系 (GA / Genetic Algorithm) は世代を回して **探索**
> する. 一方 llive の SynapticSelector は **収束** — 確率的選択を 1 か所に
> 落とし込むエンジン. この 2 つを「同じ脳」に同居させると, **シナプス単位の
> 速い収束** と **個体単位の遅い探索** が干渉せず, 「速い小脳」と「遅い大脳」が
> 役割分担する.
> 
> 本記事はその「速い小脳側」 — B-series (B-0 〜 B-9) の設計と本番投入を,
> ベンチ数値 + honest disclosure 付きで辿る.

>
## 0. 連載中での位置づけ
<small><strong>EN:</strong> 0. Position within the series / <strong>中:</strong> 0. 在系列中的定位</small>

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
<small><strong>EN:</strong> Both can coexist without interference: SynapticSelector picks synapses INSIDE one individual; EvolutionLoop selects ACROSS the population. / <strong>中:</strong> 两者可以共存而不互相干扰: SynapticSelector 在 "同一个体内" 选择 synapse, EvolutionLoop 在 "群体之间" 选择.</small>
GA は **個体間** の競争. 直交.

<!-- theme-svg-placed -->
![theme — B-series ε-greedy bandit + UCB1 (animated)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_04_theme.svg)

## 1. B-series の歴史
<small><strong>EN:</strong> 1. History of the B-series / <strong>中:</strong> 1. B-series 的历史</small>

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
<small><strong>EN:</strong> 2. Core of SynapticSelector - UCB1 / <strong>中:</strong> 2. SynapticSelector 的内核 - UCB1</small>

LLM 推論の各 layer / each token 生成タイミングで, llive は **複数の synapse
<small><strong>EN:</strong> At each LLM layer / each token generation, llive picks among multiple synapse variants using UCB1. / <strong>中:</strong> 在每个 LLM layer / 每次 token 生成时, llive 用 UCB1 在多个 synapse 变体中做选择.</small>
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
<small><strong>EN:</strong> 3. Hebbian - co-occurrence bonus / <strong>中:</strong> 3. Hebbian - 共现奖励</small>

UCB1 だけでは「1 つの variant が単独で当たる」のは検出できるが「**A と B が
<small><strong>EN:</strong> UCB1 alone detects 'this single variant wins'; Hebbian detects 'A and B fire together'. / <strong>中:</strong> 仅靠 UCB1 能检测出 "这个 variant 单独命中"; Hebbian 则能检测出 "A 和 B 一起激活".</small>
一緒のときに当たる**」は検出できない. そこで B-2 で Hebbian 強化:

```
if t-1 で variant_A が選ばれ, t で variant_B が選ばれ, reward が高い
  → bonus(A, B) を +1
```

これで「A の直後に B」のような **時系列共起パターン** が UCB1 の score に
ブーストとして乗る. これは Hebb の "fire together, wire together" を強化学習
の選択器に持ち込んだもの.

## 4. B-9 production hot path
<small><strong>EN:</strong> 4. B-9 production hot path / <strong>中:</strong> 4. B-9 生产环境热路径</small>

B-0 〜 B-8 は **アルゴリズム整備**. B-9 で **本番性能** に踏み込む.
<small><strong>EN:</strong> B-0..B-8 are algorithm groundwork. B-9 enters production-grade performance. / <strong>中:</strong> B-0..B-8 是算法铺底. B-9 进入生产级性能.</small>

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
B-9-b の deque 改善が **既に上限近くで頭打ち**. これは `feedback_benchmark_honest_disclosure`
通り「異常に良い結果が出たら必ず内訳を疑う」の実例. **削減幅は重複領域がある**.

## 5. 5x gate と Rust
<small><strong>EN:</strong> 5. 5x gate and Rust / <strong>中:</strong> 5. 5 倍 gate 与 Rust</small>

llive Rust 拡張 (RUST-FX) は「Python 比 **5x 以上** の速度向上」を要件にする
<small><strong>EN:</strong> llive's Rust extension (RUST-FX) demands at least 5× speedup over Python as a hard gate. / <strong>中:</strong> llive 的 Rust 扩展 (RUST-FX) 把 "相对 Python 至少 5 倍提速" 设为硬 gate.</small>
(`project_llive_rust_acceleration`). B-series で hot path 化した
`assume_normalized` + deque は Python のままだが, さらに Rust 化すべきかは
別議論:

- 現状 production 28% 改善で **Python 維持の方が安全** (依存複雑性が低い).
- Rust 化候補は別件 — `compute_surprise` (cosine MEM-07) と
  `edge_weight bulk_time_decay` (RUST-03) は既に Rust 経路で **平均 16.18x**.

つまり「B-series は Python でチューニングを着地. その隣で Rust kernel が
別 hot path を持っている」が現状の design split.

## 6. 「速い小脳」と「遅い大脳」が干渉しない理由
<small><strong>EN:</strong> 6. Why fast cerebellum and slow cerebrum do not interfere / <strong>中:</strong> 6. 为什么快速小脑和慢速大脑不互相干扰</small>

llive は同一プロセスで:
<small><strong>EN:</strong> llive runs them in the same process, separated by time scale (per-token vs per-generation). / <strong>中:</strong> llive 在同一进程中以时间尺度分离 (每 token vs 每代) 运行两者.</small>

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
<small><strong>EN:</strong> 7. B-series landing by the numbers / <strong>中:</strong> 7. 用数字看 B-series 的着地</small>

| 指標 | 着地時 |
|---|---|
| B-0/B-1 着地時 throughput baseline | 100% |
| B-9-a 着地後 | **112%** (+12.3%) |
| B-9-b 着地後 | **122%** (+21.7%) |
| B-9-a + B-9-b 同時 | **128%** (+28.4%) |
| Rust kernel (MEM-07 + RUST-03) | 上記とは別 hot path で **16.18x** 平均 |

ベンチは `benches/bench_synaptic_b9_production.py` および
<small><strong>EN:</strong> Benches live at benches/bench_synaptic_b9_production.py and friends. / <strong>中:</strong> 基准测试位于 benches/bench_synaptic_b9_production.py 等.</small>
`benches/bench_rust_ext_5x_gate.py` を参照 (リポジトリ内). 95% CI と
方法論は同 dir の README に.

## 8. 次に来るもの
<small><strong>EN:</strong> 8. What comes next / <strong>中:</strong> 8. 接下来要做的</small>

- **#24-05** で「遅い大脳側」 — EvolutionLoop / v0.B/C/D/E 派生集団進化を
  扱う. B-series で固めた「速い収束」とどう同居するかをそこで対比する.
<small><strong>EN:</strong> How #24-05 (EvolutionLoop, slow cerebrum) coexists with the fast convergence of this chapter is the next topic. / <strong>中:</strong> #24-05 (EvolutionLoop, 慢大脑) 如何与本章的快速收敛共存, 是下一个话题.</small>
- **RUST-15** (v0.7) — persona_dissimilarity を Rust 化. これは B-series
  ではなく E.17 quality-diversity の hot path. 5x gate 適用.

## 9. 2026-05-22 追記 — 「速い小脳 (Python 最適化)」と「遅い大脳 (Rust 化)」が直交する実例
<small><strong>EN:</strong> 9. 2026-05-22 addendum - orthogonality of Python-optimised fast cerebellum vs Rust-accelerated slow cerebrum / <strong>中:</strong> 9. 2026-05-22 追记 - 快小脑 (Python 优化) 与 慢大脑 (Rust 化) 正交的实例</small>

本記事 (B-series) と #24-05 (EvolutionLoop) は **時間スケール 1000x 違う**
<small><strong>EN:</strong> This chapter (B-series) and #24-05 (EvolutionLoop) operate at time scales 1000× apart. / <strong>中:</strong> 本章 (B-series) 与 #24-05 (EvolutionLoop) 的时间尺度相差 1000 倍.</small>
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

---

> **draft note**: full 10x volume (80-120k 字) 版は次セッションで.
> 本 draft は骨子 + 9 main section + 数字裏付け + honest disclosure 2 件
> (新規: 小脳/大脳の最適化手段が直交する).
> 連載 #24 シリーズ index (`QIITA_#24_00_llive_tech_series_index`) と整合.

---

## Series Navigation

- ← 前: [llive 完全解説 (3) 「矛盾は計算できる」](https://qiita.com/furuse-kazufumi/private/fa0890f136636d495ea6)
- → 次: [llive 完全解説 (5) 「集団が学ぶ AI」](https://qiita.com/furuse-kazufumi/private/07b686ea311e06027f94)
- 全体: [llive 完全解説 (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
