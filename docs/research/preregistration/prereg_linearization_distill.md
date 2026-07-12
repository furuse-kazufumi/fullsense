# Pre-registration — 線形化 本訓練 + 蒸留(改造①④): constant-state student への蒸留と held-out 検証

- **日付**: 2026-06-28
- **status**: `pre-registered`(実行は GPU 着荷後 / RTX 5090 32GB)
- **interim agenda 対応**: T1 実験 2/3(`docs/research/interim_research_agenda_2026-06-28.md` §T1、改造①linearize / ④distill)
- **対象コード(実在確認済)**:
  - `D:/projects/llcore/src/llcore/runtime/linearize.py`(`linearize_qwen2` / `hybridize_qwen2` / `LinearAttention(feature_map="diag"|"full")` / `SlidingWindowAttention` / `WindowLinearAttention`)
  - `D:/projects/llcore/src/llcore/runtime/distill.py`(`distill_layer` / `distill_all_layers`)
  - `D:/projects/llcore/scripts/linearize_tolerance.py`(zero-shot 層別耐性)/ `scripts/evolve_linearization.py`(層別 NAS)/ `scripts/nas_pareto.py --proxy-v2 --distill`(held-out 検証)
- **正本知見**: `MODEL_LANDSCAPE_2026_06.md` §13(1) 層別耐性 / §13(2) L7 Hedgehog / §14 実装済(WindowLinearAttention, full feature map)/ `docs/NEXT_SESSION.md`(LoLCATs Step1 同一性の指摘、未実装候補の要約)
- **honest 規律**: `feedback_benchmark_honest_disclosure` / `feedback_implementation_status_record`(実装状態を 4 段で明記)

> **凍結宣言**: レシピ基準・蒸留損失・held-out プロトコル・成功基準を実行前に固定。GPU 着荷後はここに書いた手順のみを実行する。

---

## 1. 背景

constant-state 線形 attention は KV を O(d²) state に畳み込むので会話長が無限でも固定メモリ。代償は **長文脈品質**(SUPRA は全層線形化で MMLU 28 vs 62 へ崩壊 — `docs/NEXT_SESSION.md` の現況要約に記載)。llcore の戦略は **hybrid**(一部の層だけ線形/SWA に変換)+ **蒸留で回復**。

### 実装状態(`feedback_implementation_status_record`、4 段で明記)

| 機能 | 実装状態 | 根拠 |
|---|---|---|
| 内部 attention surgery(softmax→linear、weight 再利用、RoPE 厳密)| **実装+単体検証済**(`tests/unit/test_runtime_linearize.py`、chunk-size 不変性等)| linearize.py |
| 層別 zero-shot 耐性プロファイル | **実走検証済**(0.5B/1.5B、`out/linearize_tolerance_*`)| §13(1) |
| 出力 MSE 蒸留(per-layer、feature map 学習、base 凍結)| **実装+単体検証済**(`distill_layer`/`distill_all_layers`、`mse_before/after`)| distill.py |
| full feature map(per-head 全結合 W∈[H,d,d]、恒等初期化)| **実装+単体検証済**(`feature_map="full"`、4 tests)| §14 |
| WindowLinearAttention(直近 window=softmax + 古い key=線形、単一分母融合)| **実装+単体検証済**(10 tests)| §14 |
| **LoRA Step2 回復**(projection も微調整)| **未実装**(`docs/NEXT_SESSION.md` 要約の未実装候補「LoRA Step2 + logit KD (K, distill.py)」)| 要追加 |
| **logit-level KD**(最終 logit / 層別 hidden の蒸留)| **未実装**(現 distill は attention 出力 MSE のみ)| 要追加 |
| **end-to-end 本訓練**(蒸留後に linearized student を継続学習)| **未実装**(per-layer 蒸留のみ。joint/全体 fine-tune スクリプト無し)| 要追加 |

→ **honest**: 現コードの「蒸留」は **LoLCATs Step1 = attention 出力 MSE transfer に等しい**(`docs/NEXT_SESSION.md` の現況要約に明記)。本 prereg は (a) **既存=出力 MSE 蒸留**の held-out 効果を確定する部分と、(b) **要追加=logit-KD / LoRA / 本訓練**を実装してから測る部分を **分けて** 登録する。混同して「本訓練済み」と report しない。

### レシピ基準(どれを基準にするか)

| レシピ | 中核 | llcore 既存対応 | 採用判断 |
|---|---|---|---|
| **LoLCATs** | feature map を attention 出力 MSE で蒸留(Step1)→ LoRA で回復(Step2)| **Step1 = `distill_layer` で実装済**。Step2 = 未実装 | **基準に採用**。llcore の core と最短距離。まず Step1 の held-out 効果、次に Step2 を要追加 |
| **SUPRA** | 全層線形化 + uptraining(RoPE→GroupNorm 等)| 部分対応(linearize_qwen2)| 全層は MMLU 崩壊 → **hybrid 比較対象**としてのみ(全層線形 = lower bound) |
| **MOHAWK** | Transformer→SSM の段階蒸留(matrix mixer 整合→hidden→logit)| hidden/logit KD = 未実装 | **段階蒸留の設計参照**(logit-KD 要追加時の手順雛形)|
| **Mamba-in-Llama** | attention 重み流用で SSM 初期化 + 蒸留 | weight 再利用は実装済 | **weight 流用方針の裏付け**(別アーキなので直輸入はしない)|

> arXiv 番号は llcore RAD corpus `efficient_seqmodels_corpus`(750 papers、`.claude/skills/corpus/efficient_seqmodels_corpus/`)で確認可。本 md は llcore コード/doc に実在する名称のみ参照(TTT=2407.04620 / StateX=2509.22630 は llcore コード内で確認済、Katharopoulos 2020=linear attention は linearize.py docstring)。LoLCATs/SUPRA/MOHAWK/Mamba-in-Llama の arXiv ID は corpus 照合を推奨(本 prereg では名称基準で十分)。

---

## 2. 仮説(falsifiable)

- **H1(蒸留の右シフト / 主仮説)**: 出力 MSE 蒸留(既存 `distill_all_layers`)は、同一メモリ予算で **より多くの層を線形化可能**にする = Pareto frontier を右へシフトする。
  - **真なら成功**: `nas_pareto.py --proxy-v2 --distill` の `right_shift_ci` verdict が「shifts the frontier out」(HV gain の 95% CI 下限 > 0)。
  - **棄却**: `right_shift_ci` が「no measurable shift」(CI が 0 跨ぎ)or「regresses」。→ 現行の出力 MSE 蒸留は held-out で効かない。
- **H2(per-layer mse 低下 → held-out 改善の伝播)**: `distill_layer` の `mse_after < mse_before`(学習が効いている)層では、その層を線形化した時の held-out Δnll が zero-shot より小さい。
  - **真なら**: mse 低下幅と Δnll 改善が正相関(層横断)。
  - **棄却(honest null の前例あり)**: §13(2) L7 で「spikiness gap は耐性を予測しない(corr≈0)」という null が出ている。同様に mse 低下が held-out に伝播しない可能性を事前に織り込む。
- **H3(feature_map 容量 diag vs full)**: `feature_map="full"`(per-head 全結合)は `"diag"`(4-param アフィン)より蒸留後 mse / held-out Δnll を改善する(L7 が「elu+1 はほぼ一様」を実証 → spiky 化の動機)。
  - **真なら**: full の `mse_after` < diag、held-out Δnll も改善。
  - **棄却**: 差が CI 内 → 容量増は回復に寄与しない(過適合/最適化困難)。
- **H4(要追加検証・条件付き)**: logit-KD + LoRA Step2(要実装)を加えると、出力 MSE のみより frontier がさらに右シフトする。
  - **注**: H4 は **コード実装(要追加)が前提**。実装前は測れないので「条件付き登録」とし、実装完了後に本 md を版管理して測る。

---

## 3. 実験デザイン

### 3.1 arm / 要因

| 要因 | 水準 |
|---|---|
| **base/target モデル**| Qwen2.5-0.5B-Instruct(24層、`out/linearize_tolerance/` 既存)を主、**1.5B(28層)を二次**(§13(1) で「規模↑で線形化耐性↑」を確認済 → 規模効果を再現)|
| **変換タイプ**(mixer)| softmax(温存)/ `LinearAttention`(全線形)/ `SlidingWindowAttention` / `WindowLinearAttention`(hybrid SWA)。NAS allele として `nas_pareto` が探索 |
| **feature_map**| `diag`(基準)/ `full`(H3)|
| **蒸留**| zero-shot(蒸留なし)/ 出力 MSE 蒸留(`--distill`、既存)/ ★logit-KD+LoRA(**要追加**、H4)|
| **メモリ予算**(`--budgets`)| 0.02,0.05,0.10,0.15,0.25,0.50(Δnll budget、frontier 構築)|
| **seed**| **0, 1, 2(≥3)**(`--seed`、NAS の確率性 + 蒸留初期化)|

### 3.2 蒸留損失(明示)

- **既存(本 prereg の主対象)**: `distill_layer` の **attention 出力 MSE** = `F.mse_loss(student(x_norm,cos,sin,None,0)[0], teacher)`。teacher = 当該層の softmax attention 出力(`_capture_layer_io` が `input_layernorm` 出力を入力、self_attn 出力を teacher に hook)。学習対象 = feature map パラメータのみ(`student.feature_parameters()`、projection は凍結)。per-layer・pristine teacher から独立蒸留(`distill_all_layers`、誤差非伝播)。
- **要追加(H4)**:
  - **logit-KD**: 全モデル forward の最終 logit に対する KL(teacher softmax model ‖ student linearized model)。temperature τ。→ distill.py に新関数(要追加)。
  - **層別 hidden KD**(MOHAWK 流): 各 block 出力 hidden の MSE。
  - **LoRA Step2**: projection に LoRA を載せて少数 step 回復学習。→ 学習対象に LoRA を追加(要追加)。
- **chunk_size(蒸留内)**: `distill_layer(chunk_size=64)` は線形 attention の再帰チャンク(品質に不変、メモリのみ)。GPU では 128–256 に。

### 3.3 held-out eval プロトコル(★明示)

蒸留が「held-out で効く」ことを winner's curse 抜きで示す:

1. **層別 zero-shot 耐性**: `scripts/linearize_tolerance.py`(既存)で base/各層の Δnll を再測(GPU、より長 context)。
2. **frontier held-out 再評価**: `nas_pareto.py --proxy-v2` が探索した frontier を **fresh disjoint holdout pool**(`make_windows` の offset 分離)で再評価(`reeval_frontier`)。`optimism_gap = selection − heldout` で選択楽観バイアスを定量。
3. **蒸留右シフト**: `--distill` 併用で zero-shot frontier と distilled frontier の HV を **paired window resample** で比較(`right_shift_ci`、共有 reference、CI 下限>0 でのみ「shifts out」)。
4. **context sweep**: 蒸留 frontier の最 aggressive genome を `--context-sweep 256,512,1024,2048` で掃引(短窓で線形劣化を見落とさない)。
5. **needle**(任意・重い): `--needle --needle-lengths 2048,4096` で長文脈 retrieval horizon。

> **honest**: distill.py の per-layer 蒸留は「各層を pristine softmax から独立に蒸留」= joint 多層蒸留(誤差累積)は別実験(docstring 明記)。よって「全層蒸留して frontier が右シフト」を示せても、それは独立蒸留 student の組合せであり、誤差累積した end-to-end とは別物。混同しない。

### 3.4 device

`distill.py` / `linearize.py` / `nas_pareto.py` は PyTorch なので `model.to("cuda")` で自動 GPU(`migration_manifest §6`: `research/*.py` 系は `DEVICE = cuda if available`)。**ただし** `nas_pareto.py` / `evolve_linearization.py` / `linearize_tolerance.py` に明示 `--device` は無い(grep で確認)→ **モデルロード `load_qwen2` の to(device) 配線が要追加**(experiment と同様に backward-compatible で auto)。CPU では byte-identical。

---

## 4. 測定指標と解析手順

- **主要指標(事前指定・1 つ)**: **distilled frontier の hypervolume 右シフト %**(`right_shift_ci` の `shift_pct_mean` + 95% CI)。これが「蒸留は同一メモリでより多くの層を線形化可能にする」の直接の尺度。
- **副次指標**: per-layer `mse_before`/`mse_after`(蒸留の局所効果)/ `delta_nll_heldout` と `optimism_gap`(frontier 各点)/ `context_sweep` の L 別 Δnll + CI / `needle` horizon。
- **解析手順(事前固定)**:
  1. seed 0/1/2 で `--distill` あり/なしを走らせ、`right_shift_ci`(内部で 2000 bootstrap、paired window resample)。seed 横断で verdict の頑健性を確認。
  2. **H2 相関**: 各層の `mse_after − mse_before` vs その層単独線形化の held-out Δnll(`reeval_frontier` から導出)を散布 + Spearman(`spearman_rho` 実在)。§13(2) の null(corr≈0)を帰無として扱う。
  3. **H3**: `feature_map="full"` vs `"diag"` の `mse_after` / 右シフト % を paired 比較。
  4. **全 verdict は `honest_verdict` / `build_proxy_v2_report` を経由**(scope='next_token_nll_proxy' が pin され、会話品質クレームは出さない設計)。
- **有意性の出し方**: 全 CI は paired bootstrap(window resample、`bootstrap_paired_ci`/`right_shift_ci`、2000 resample)+ 必要に応じ `sign_test`/`wilcoxon_perm`(分布フリー、scipy 不要、実在)。

---

## 5. 成功基準(事前固定)と honest 内訳プラン

### 成功基準

- **PASS(H1)**: 3 seed 中央値で `right_shift_ci` が「shifts the frontier out」(95% CI 下限 > 0)、かつ `context_sweep` の長 L(≥1024)でも distilled が zero-shot を Δnll で下回る(短窓限定の見かけ改善でない)。
- **NULL**: 右シフト CI が 0 跨ぎ / 長 L で改善消失。→「現行の出力 MSE 蒸留(=LoLCATs Step1 相当)は held-out 品質を有意には回復しない」を確定 → H4(logit-KD/LoRA 要実装)へ進む根拠に。

### honest 内訳プラン(`feedback_benchmark_honest_disclosure`)

1. **winner's curse**: frontier は数百 genome から非劣解を拾う = max-of-N の楽観。**必ず `delta_nll_heldout` と `optimism_gap` で語る**(`reeval_frontier` が fresh holdout で再評価)。選択窓 Δnll を headline にしない。
2. **短文脈の盲点**: 線形劣化は長文脈で出る(eval_proxy.py docstring: 256 tok は劣化を過小検出)。`--inner-context 1024` + `--context-sweep …2048` で測り、**短窓だけの改善を「回復」と呼ばない**。
3. **車輪の再発明の正直開示**: 「蒸留が効いた」= LoLCATs Step1 の追試であり llcore 固有の新規性ではない(`docs/NEXT_SESSION.md` の現況要約に明記)。**新規性は層別 hybrid NAS(memetic、`evolve_multiobjective`)**にあると正確に位置づける。
4. **実装状態の正直開示**: logit-KD / LoRA / end-to-end 本訓練は **未実装**。これらを「やった」と書かない。H4 は実装完了をもって別途登録。
5. **per-layer 蒸留の限界**: 独立蒸留 student の寄せ集めであり、誤差累積する joint/e2e とは別物。frontier の良さを e2e 品質と読み替えない。
6. **attention-KL は診断のみ**: `genome_attn_kl` は 256 tok cap・O(T²)・**NAS fitness に絶対 wire しない**(eval_proxy.py 設計)。診断値を品質クレームに昇格させない。

---

## 6. 実行コマンド(具体・既存引数のみ)

> 既存=実在引数のみ使用。`--device auto`(load_qwen2 への配線)と logit-KD/LoRA フラグは **要追加**として明示。

```powershell
# --- (A) 既存: 出力 MSE 蒸留の held-out 右シフト (本 prereg の主対象) ---
foreach ($s in 0,1,2) {
  py -3.11 D:/projects/llcore/scripts/nas_pareto.py `
    --model-dir D:/models/Qwen2.5-0.5B-Instruct `
    --text-file out/corpus_aozora_multi.txt `
    --proxy-v2 `
    --inner-context 1024 --fast-windows 8 --holdout-windows 12 `
    --context-sweep 256,512,1024,2048 `
    --cross-corpus out/corpus_holdout_disjoint.txt `      # DISJOINT コーパス(要用意)
    --budgets 0.02,0.05,0.10,0.15,0.25,0.50 `
    --pop 24 --generations 20 `
    --distill --distill-steps 400 --distill-lr 5e-2 --distill-tokens 512 `
    --needle --needle-lengths 2048,4096 `
    --seed $s `
    --out out/linearize_distill/zs_vs_distill_seed${s}
}

# --- (B) 層別 zero-shot 耐性 (GPU, 長 context 再測) ---
py -3.11 D:/projects/llcore/scripts/linearize_tolerance.py `
  --model-dir D:/models/Qwen2.5-0.5B-Instruct --n-tokens 2048 `
  --out out/linearize_distill/tolerance_0p5b_2048
# 1.5B 規模効果:
py -3.11 D:/projects/llcore/scripts/linearize_tolerance.py `
  --model-dir D:/models/Qwen2.5-1.5B-Instruct --n-tokens 2048 `
  --out out/linearize_distill/tolerance_1p5b_2048

# --- (C) feature_map full vs diag (H3) ---
# nas_pareto は feature_map を直接公開していない → distill_layer(feature_map=...) を呼ぶ
# 小スクリプト(要追加: --feature-map フラグ)で diag/full を比較、または distill_all_layers を
# feature_map="full" で呼ぶ実験ハーネスを追加。

# --- (D) 要追加: logit-KD + LoRA Step2 (H4, 実装後に登録) ---
# distill.py に logit_kd_loss / lora 回復を実装してから本 md を版上げして測る。
```

> 注: `linearize_tolerance.py` の引数(`--n-tokens`/`--budget`/`--out` 等)は grep で確認した範囲のみ使用。`--model-dir` で 1.5B を指すには該当モデルの存在が前提(`D:/models/Qwen2.5-1.5B-Instruct`、§13(1) で 1.5B プロファイル既走なので存在見込みだが要確認)。`--cross-corpus` の DISJOINT ファイルは別途用意(要追加データ)。

---

## 7. 想定アウトプット先

- `D:/projects/llcore/out/linearize_distill/zs_vs_distill_seed{0,1,2}/`(nas_pareto report、`proxy_v2` ブロック + `right_shift_ci`)
- `D:/projects/llcore/out/linearize_distill/tolerance_{0p5b,1p5b}_2048/`
- `D:/projects/llcore/out/linearize_distill/ANALYSIS.md`(seed 集計 + 右シフト CI + mse↔held-out 相関図 + 実装状態 4 段の最終確定)
- 結論は MODEL_LANDSCAPE §13/§14 へ反映。H4(logit-KD/LoRA)は実装完了時に本 md を改訂して別 run。
