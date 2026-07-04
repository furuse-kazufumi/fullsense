---
layout: default
title: "実 LLM QD-of-merges PoC (2026-07-04)"
parent: "Research"
---

# 実 LLM QD-of-merges — gaitlab の MAP-Elites でモデル融合を照らす(SmolLM2-135M)

> 作成: 2026-07-04(ccr, Fable 5)。融合調査 `llm_model_fusion_landscape_2026-07-04` の最有力 lead #1「QD-of-merges」を、toy(numpy 線形回帰 2 エキスパート)から **実 LLM 重み**へ載せた CPU PoC。派生計画 memory `project_gaitlab_derivative_plan_2026_07_03` #22「実 LLM 化」。honest-disclosure 準拠(memory `feedback_benchmark_honest_disclosure`)。
> 実装: `gaitlab/gaitlab/llm_merge.py` + `scripts/merge_llm_qd.py` + `tests/test_llm_merge.py`(8 件)。成果物: `gaitlab/out/merge_llm_qd/{merge_llm_qd.json,merge_llm_qd.png}`。local commit のみ(push は human-go)。

## 0. 結論(TL;DR)

**gaitlab の歩容進化に使った `MapElitesArchive` を一字も変えず、実 LLM の重みマージへ転用でき、そこで非自明な発見が出た。** 同一 base 兄弟(SmolLM2-135M base ↔ Instruct)を「単一 task-vector の**層別**グラフト」で融合し、held-out perplexity の実トレードオフ(素テキスト=base 有利 / 指示応答=instruct 有利)を MAP-Elites で照らした。**均一な補間(全層同一 λ)は概ね破壊的**(λ=0.22 で素テキスト PPL が 6.40→7.77 に悪化=部分グラフトがモデルを壊す)で、7 点グリッド中まともなのは λ=0.65 の 1 点(balanced fitness 0.727)のみ。対して **QD は「早期層は base 保持・後期層は instruct 接ぎ木」という層別配分を自動発見**し(band λ=[0.09, 0.0, 0.86, 1.18, 0.71, 1.06])、均一曲線の外側に balanced fitness 0.797 の点(plain 6.582 / chat 3.904)を置いた。**均一補間では届かない釣り合い点に、層別自由度で到達できる**という honest な結果。ただし単一 seed・小コーパス・balanced fitness 定義依存の限界は §4。

## 1. なぜこの PoC か

toy PoC(`project_gaitlab_derivative_plan_2026_07_03` #22)は「gaitlab の `MapElitesArchive` を genome=マージレシピに無改変転用できる」ことを numpy 合成 2 タスクで示したが、評価器は線形回帰の擬似能力で LLM ではなかった。本 PoC は **同じマージ数学(SLERP/DARE/TIES-trim)と同じ QD ループを、実モデルの実重みと実 perplexity に載せ**、「toy の枠組みは実 LLM に転移するか」を最小コストで検証する。融合調査の「最初の一歩」= 同一 base 兄弟を task-vector/SLERP でマージ → held-out perplexity → 負コントロール(異 base=破綻)→ 係数を gaitlab archive の genome に露出、をそのまま実装した。

## 2. セットアップ(honest scope)

- **モデル**: `HuggingFaceTB/SmolLM2-135M`(base)↔ `SmolLM2-135M-Instruct`。**同一 base の兄弟**(param 集合完全一致・shape 不一致 0・‖τ‖₂≈199)。CPU / float32 / HF キャッシュのみ(追加 DL 無し)。30 層を `n_bands=6` に量子化。
- **融合 = 単一 task-vector の層別グラフト**: `merged = base + λ_band · trim_density( DARE_p( τ ) )`(τ = instruct − base)。band ごとに λ。巨大テンソル(embed/lm_head ≈ 28M 要素)は per-eval コスト支配のため線形グラフトのみ(実マージでも埋め込みの疎化は稀)。`--method slerp` で per-tensor SLERP も可。
  - ★honest 制約: **真の多エキスパート TIES(符号選挙)は同一 base の第 2 エキスパートを要する**(未 DL)ので toy 側に留めた。本 PoC は「1 つの expert(instruct)をどの層に・どれだけ・どれだけ疎に接ぐか」= DARE / task-arithmetic / layer-wise の範囲。
- **評価 = 2 つの held-out perplexity のトレードオフ**(下流精度でない):
  - `plain`: 素の説明文 4 本 → **base 有利**(素の言語モデル質)。
  - `chat`: 指示応答 4 対、chat テンプレの assistant 部のみ NLL → **instruct 有利**。
- **fitness** = 2 端点(base=plain 側 / instruct=chat 側)を 0–1 アンカーにした goodness の調和平均(釣り合いを報いる)。**descriptor** = (mean λ 正規化, merged-delta 疎性)= 挙動記述子(fitness と分離)。
- **対照(ベースラインを必ず先に測る)**: base(λ=0)/ instruct(λ=1)/ uniform(λ=0.5)/ **global-λ grid**(全 band 同一 λ=層別自由度なしの最良)。QD の対抗馬は grid。
- **QD**: budget 54(n-init 14 + n-gen 5 × batch 8)、8×8 bins、Iso+LineDD 変異(歩容 QD と同一)、seed 0。

## 3. 結果

### 3.1 端点とベースライン(held-out perplexity, 低いほど良い)

| arm | plain PPL | chat PPL | balanced fitness | 備考 |
|---|---|---|---|---|
| base (λ=0) | **6.396** | 5.302 | 0.000 | 素テキスト専門・指示は弱 |
| instruct (λ=1) | 7.252 | **3.581** | 0.000 | 指示専門・素テキストは弱 |
| uniform (λ=0.5) | 7.363 | 3.710 | 0.000 | **素朴中点が破壊的**(plain が両端より悪化) |
| global-λ grid best (λ=0.65) | 6.783 | 3.446 | 0.727 | 7 点中唯一まともな均一補間 |
| **QD best (層別 λ)** | **6.582** | 3.904 | **0.797** | 均一曲線の外側の釣り合い点 |

`fitness=0.000` は goodness_plain が 0 にクリップ(plain PPL が instruct 端点 7.252 を超えた=素テキスト質が両親より悪い)を意味する。**均一グラフトは大半が「両親より悪い」**。

### 3.2 global-λ 曲線は非単調で概ね破壊的

| λ | 0.00 | 0.22 | 0.43 | 0.65 | 0.87 | 1.08 | 1.30 |
|---|---|---|---|---|---|---|---|
| plain PPL | 6.40 | 7.77 | 7.58 | 6.78 | 7.01 | 7.46 | 8.58 |
| chat PPL | 5.30 | 4.64 | 4.03 | 3.45 | 3.46 | 3.71 | 4.53 |

**全層を一律 λ で混ぜると λ≈0.2–0.5 で素テキスト PPL がむしろ悪化**(部分グラフトが表現を壊す)。λ=0.65 でたまたま両立が良くなる谷があるが、それ以外は destructive。均一補間は「壊れた中間」を通ることが多い。

### 3.3 QD が発見した層別配分(核心)

QD best の band λ = **[0.086, 0.0, 0.859, 1.175, 0.705, 1.061]**(density 0.70, drop_p 0.27)。
- **早期層(band 0–1 ≒ 層 0–9)は λ≈0 = base をほぼ保持** → 素の言語モデル質を守る。
- **後期層(band 2–5 ≒ 層 10–29)は λ≈0.7–1.2 = instruct を接ぎ木**(一部外挿)→ 指示追従を獲得。

→ これは grid 解像度のアーティファクトではない(**非一様**な配分)。「表現は前段・振る舞いは後段」という直感に一致し、**均一 λ の 1 次元曲線では原理的に届かない点**(plain 6.582 は grid best の 6.783 より良く、かつ chat 3.904 を維持)に到達した。coverage 0.28 / 18 cells / budget 54。

### 3.4 負コントロール

SmolLM2-135M vs Qwen2.5-0.5B は共有キー 219/273・**shape 不一致 219** → 座標系不一致で weight-space マージ不能(Git Re-Basin 2209.04836 の予言通り)。「同一 base 兄弟だから混ざる」ことの対照。

## 4. honest な限界

- **単一 seed・小コーパス**(plain/chat 各 4 サンプル)。QD の勝ち(0.797 vs 0.727)は balanced=調和平均 fitness 上の勝ちで、**定義が釣り合いを報いる**ことに依る。順位(base=plain 有利 / instruct=chat 有利)は端点差が大きく頑健だが、絶対 PPL は corpus 依存。
- **dominator は 0**: QD best は両端点を**同時支配**しない(plain 6.582 > base 6.396、chat 3.904 > instruct 3.581)。照らしたのは既存能力の**より良い配分**であって、両親に無い新能力ではない(容量保存則)。
- **grid は 7 点と粗い**が、§3.2 の非単調・破壊性から、細かい均一 sweep でも QD の層別点には届きにくい(均一曲線の最良が層別点から離れている)。とはいえ細粒度 global sweep の明示測定は次段の宿題。
- **単一 τ の層別グラフト**は本質的に低次元。真の多エキスパート TIES(符号選挙)は未実測。

## 5. 再現

```
cd D:/projects/gaitlab
PYTHONUNBUFFERED=1 PYTHONUTF8=1 HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 PYTHONPATH=. \
  py -3.11 scripts/merge_llm_qd.py --n-init 14 --n-gen 5 --batch 8 --grid 7 --bins 8
# per-layer SLERP 版: --method slerp
```
テスト(torch↔numpy マージ数学の parity): `pytest tests/test_llm_merge.py`(8 件)。所要 ≈ 8 分(CPU, budget 54, per-eval ≈ 4.5s)。

## 6. 次段

- **細粒度 global-λ sweep**を明示測定し、層別優位の大きさを厳密化(honest 補強)。
- **多エキスパート TIES 化**: SmolLM2-135M の第 2 finetune(JP or code)を DL し、真の符号選挙マージを実測(#22 の完成形)。
- **llive 進化マージ(#23)**: マージ係数 genome を lldarwin ε-lexicase+QD の選択圧に載せる(Sakana CMA-ES の代替)。
- **記事化(#26)**: 「形態融合 ↔ frankenmerge」の構造対応 + 本 honest 実験(均一=破壊的 / 層別=QD が救う)を career-grade 教材に。

関連: memory `reference_llm_model_fusion_2026_07_04` / `project_gaitlab_derivative_plan_2026_07_03` / `project_ros_physical_ai_2026_07_02` / `feedback_benchmark_honest_disclosure`。正本 landscape = `llm_model_fusion_landscape_2026-07-04.md`。
