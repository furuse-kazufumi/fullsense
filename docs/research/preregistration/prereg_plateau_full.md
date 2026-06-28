# Pre-registration — Plateau Full (§13(4) 交絡解消) : state-carry × credit-assignment window × capacity/cell

- **日付**: 2026-06-28
- **status**: `pre-registered`(実行は GPU 着荷後 / RTX 5090 32GB)
- **interim agenda 対応**: T1 実験 1/3(`docs/research/interim_research_agenda_2026-06-28.md` §T1)
- **対象スクリプト**: `D:/projects/llcore/scripts/tbptt_plateau_experiment.py`(実在確認済)
- **正本知見**: `D:/projects/llcore/docs/MODEL_LANDSCAPE_2026_06.md` §13(3)(carry-off)/ §13(4)(carry-on, 交絡指摘)/ §14(忠実 Gated DeltaNet 実装)
- **honest 規律**: `feedback_benchmark_honest_disclosure`(異常に良い結果は内訳を疑う / 失敗を消さず教訓に残す)

> **凍結宣言**: 本 md は解析自由度(arm 集合・主要指標・成功基準・compute-matched 対照・棄却条件)を実行前に固定する。GPU 着荷後はここに書いた手順「のみ」を実行し、走らせてから指標や閾値を選び直さない(p-hacking 回避)。

---

## 1. 背景

llcore の headline null: 訓練済み constant-state recurrent LM の `context_length_curve` は `block_size` 付近で **drop-then-plateau** し、訓練窓を超える文脈を活用しない(`past_block_gain ≈ 0`)。なぜ動かないかを 3 因子に分解して切り分けてきた:

- **capacity**: `recurrent` vs `recurrent-wide`(StateX 流の wider state、arXiv:2509.22630 — llcore コード内で確認)
- **update-rule(cell)**: `recurrent` vs `gated-deltanet`(data-dependent α/β delta-rule、`src/llcore/lm/ttt.py`、TTT arXiv:2407.04620 — llcore コード内で確認)
- **training method**: `--carry off`(state-reset)vs `--carry on`(state-carry TBPTT)

### これまでに確定している事実(一次ソース = MODEL_LANDSCAPE §13)

| 設定 | arm | held-out ppl | past_block_gain | ppl_by_ctx(16→1024) |
|---|---|---|---|---|
| carry-off(§13(3))| recurrent / wide / ttt-linear(静的) | 32.47 / 31.76 / 31.52 | −0.0001 / 0.0 / 0.0 | フラット |
| carry-on(§13(4))| recurrent / wide / gated-deltanet(静的) | 32.41 / 33.33 / **25.23** | 0.0003 / 0.0001 / 0.0 | フラット |

2×3 = **全 honest null**(past_block_gain ≈ 0)。副次信号: gated-deltanet は ppl 顕著低(25.23 vs 22.9)= より良い mixer だが、長文脈活用(plateau)とは **直交**。

### §13(4) で自認した重大な交絡(本実験が解く対象)

carry-on 実験は `chunk_size = block_size = 128` で走った。state は持ち越すが **勾配は依然 128 で truncate** = 「128 先のために何を保持すべきか」の credit assignment は切れたまま。**∴ state-carry が plateau を動かすかは未検証**。真の検証 = **(a) `chunk_size > block_size`(勾配をより遠くへ)** + (b) 忠実なデータ依存ゲート版(§14 で実装済)。

### 本日(2026-06-28)の単 seed プローブ(`D:/projects/llcore/out/ttt_chunk_probe/`、一次確認)

`gated-deltanet` のみ・seed 1337・max-iters 400 の chunk sweep プローブ:

| run | chunk_size | best_val_loss | held_out_ppl | past_block_gain | ppl_by_ctx | 状態 |
|---|---|---|---|---|---|---|
| c128 | 128 | 3.654 | 38.26 | **0.0** | 29.598→29.584(フラット)| **完了**(`c128/comparison_carry_on.json`)|
| c512 | 512 | — | — | **未確定** | 未算出 | **走行途中**(upd 399 で train 3.3877 / **val 3.4353**、curve 未書き出し)|

- **c128 の読み**: chunk=block の fair-compute baseline で past_block_gain=0.0、curve は 16→1024 まで完全フラット。**chunk を広げない限り plateau は動かない**を 1 seed で再確認。
- **c512 の読み(要注意・交絡あり)**: 同 iter 数(upd 399)で **val 3.4353 と c128 の 3.6540 より明確に低い**。しかし `--chunk-size 512` は **fixed max-iters では勾配トークン量が 4× = 単に compute が多いだけ**で val が下がった可能性が拭えない(scripts/tbptt_plateau_experiment.py の summary note が自ら警告する点)。しかも c512 は `context_length_curve` を書き出す前に止まっており **past_block_gain は未確定**。→ **「chunk を広げると plateau が動く」とはまだ一切言えない**。これがフル実験で確定させる中核。

---

## 2. 仮説(falsifiable)

- **H1(credit-assignment 仮説 / 主仮説)**: chunk_size を block_size 超に広げる(勾配を遠くへ伸ばす)と、**compute-matched 対照に対しても** `past_block_gain` が有意に正へ動く。
  - **真なら成功**: chunk∈{256,512,1024} の少なくとも 1 水準で、3 seed 平均 `past_block_gain` の bootstrap 95% CI 下限 > 0、**かつ** compute-matched 対照(§3.4)を上回る。
  - **棄却(null)**: 全 chunk 水準で 95% CI が 0 を跨ぐ、または compute-matched 対照との差が CI で 0 を跨ぐ → 「credit-assignment 窓拡大は plateau を動かさない」を確定。
- **H2(compute 交絡 vs 真の効果)**: c512 で観測した val 改善は **勾配トークン量の増加(4× compute)で説明できる**。
  - **真なら(交絡確定)**: chunk=512 の val 改善が、chunk=128 を 4× iters 走らせた compute-matched 対照の val 改善と CI 上区別できない。→ c512 の「良さ」は plateau とは無関係の compute artifact。
  - **棄却**: compute-matched 対照を超える residual gain が残る → chunk 拡大固有の効果。
- **H3(因子分離)**: plateau の主因が capacity でも cell でもなく training/credit-assignment であるなら、`past_block_gain` の chunk 依存は arm(recurrent / wide / gated-deltanet)を跨いで一貫する(arm より chunk が支配的)。
  - **真なら**: 二元配置で chunk 主効果が arm 主効果より大。
  - **棄却**: arm 間で chunk 応答が割れる → 因子は交互作用的(単純な「訓練法が主因」では説明不能)。

> 事前の予想(honest に記録、当たり外れを後で照合): §13 の null 連発と c128 フラットを踏まえ、**H1 は棄却(null)寄り**と予想する。chunk 拡大は val(訓練適合)を下げても、cold-start `context_length_curve` で測る *有効文脈* は動かさない公算が高い。これが外れたら(=plateau が動いたら)大きな前進なので、内訳(compute 交絡)を最優先で疑う。

---

## 3. 実験デザイン

### 3.1 要因と arm

| 要因 | 水準 |
|---|---|
| **credit-assignment 窓**(`--chunk-size`)| 128, 256, 512, 1024 |
| **arm**(`--arches`)| `recurrent`(capacity 基準)/ `recurrent-wide`(capacity+, StateX 流)/ `gated-deltanet`(cell+, data-dependent delta-rule)|
| **training**(`--carry`)| `on`(state-carry TBPTT, seg_len=2048)を主。`off`(state-reset)は §13(3) 既走と接続する対照として chunk=128 のみ再走 |
| **seed**(`--seed`)| **1337, 1338, 1339(≥3、必須)** |

主格子 = chunk(4)× arm(3)× seed(3)= **36 run**(carry on)。+ compute-matched 対照(§3.4)+ carry-off 接続対照。

### 3.2 compute-matched 対照(★交絡排除の核)

`tbptt_plateau_experiment.py` の summary note が明記するとおり、**fixed max-iters では compute が chunk_size に比例して増える**(chunk=512 は chunk=128 の 4× 勾配トークン)。よって chunk 水準間の比較は **総勾配トークン数を揃える**:

- **基準 budget**: chunk=128 × max_iters=`N₀`。総勾配トークン ∝ `chunk × batch × max_iters`。
- **対照 A(iters 補正)**: chunk=128 を `4×N₀` iters(= chunk=512 と総勾配トークン一致)。これを chunk=512(`N₀` iters)と比較 → 「chunk 拡大の効果」から「単なる多 compute」を差し引く。
- 同様に chunk=256 ↔ chunk=128×2N₀、chunk=1024 ↔ chunk=128×8N₀。
- **判定**: chunk=512(`N₀`)の past_block_gain/val が、対照 A(chunk=128, 4N₀)を **CI 上超えるか**。超えなければ H2 = 交絡確定(c512 の良さは compute artifact)。

### 3.3 コーパス・モデルサイズ・ハイパラ(GPU 拡大版)

- **コーパス**: `--corpus-file out/corpus_aozora_multi.txt`(現プローブと同一、char-LM、vocab≈4358、~330万字)。指標方法論を CPU プローブと連続させるため **同コーパスを維持**(初手)。スケール検証は別途 §6 の拡張で。
- **モデルサイズ(GPU で拡大)**: CPU プローブは `--n-layer 2 --n-embd 128`(~1.2M params)。GPU では現実的規模へ:
  - **主格子**: `--n-layer 4 --n-embd 256 --state-size 256 --wide-state-size 512 --ttt-state-dim 192`
  - `--batch-size 64`(CPU 24→GPU 余裕)/ `--max-iters 4000`(基準 N₀。CPU 1200→拡大)/ `--lr 1e-3`(据え置き、必要なら別途 LR sweep)
  - `--seg-len 2048`(state-carry 範囲、据え置き)
- **評価**: `--context-lens 16,32,64,128,256,512,1024,2048`(現状 1024 まで → **2048 追加で訓練窓×16 まで掃引**。`context_length_curve` は `step` 駆動で context cap が無いことをコード(`longctx_eval.py`)で確認済)/ `--n-positions 256`(CPU 160→増やして CI を締める)。
- **seed ごとにモデル再初期化**(スクリプトは arm ループ先頭で `torch.manual_seed(args.seed)`、seed は run 単位で渡す)。

### 3.4 device(★コード要追加)

`tbptt_plateau_experiment.py` には **`--device` 引数が存在しない**(Read で全 argparse 確認済)。`Trainer`/`TBPTTTrainer` も CPU-only(`migration_manifest_2026-06-28.md` §6 が「未配線」と明記)。

- **要追加(backward-compatible、§6 記載)**: ① experiment に `--device`(default `auto = "cuda" if torch.cuda.is_available() else "cpu"`)② trainer で `model.to(device)` + 各 batch `.to(device)` + `init_state(device=device)` ③ `longctx_eval` / `held_out_report_any` も device 統一。
- CPU 機では auto→cpu で **byte-identical**(現プローブ方法論に影響なし)。**この配線が本実験の前提**(着荷後 Day 1 か本日プローブ完了後・~30分)。
- 配線完了の検証 = `scripts/prove_native_matches_hf.py` を GPU で(次トークン argmax 一致)+ 小 step smoke(plan §5-2,3)。

---

## 4. 測定指標と解析手順

- **主要指標(事前指定・1 つ)**: **`past_block_gain`**(= `context_length_curve` の `nll_by_context` から、block_size でのNLL → 最長 context でのNLL への相対 NLL 低下)。`tbptt_plateau_experiment.py` / `longctx_eval.py` に実在。`> 0` = 訓練窓を超えて文脈を使えている。
  - **honest 注記(コード由来)**: past_block_gain は **block_size と最長 c の 2 点差分**(粗い)。主張前に **full `ppl_by_context` 曲線**(2048 まで)を必ず目視し、単調 drop-then-plateau か、途中で再上昇(OOD 外挿崩れ)していないかを確認。
- **副次指標**: `held_out_ppl`(`held_out_report_any` の `model_ppl`)/ `best_val_loss`(Trainer/TBPTTTrainer)/ `ppl_by_context` 全曲線 / `unigram_ppl`(floor 確認)。
- **解析手順(事前固定)**:
  1. 各 (chunk, arm) について seed=1337/1338/1339 の `past_block_gain` を集計 → **seed をまたいだ bootstrap 95% CI**(2000 resample、`feedback_benchmark_honest_disclosure` 準拠)。seed が 3 と少ないので CI は seed 平均の不確実性として報告し、断定は CI 下限>0 のときだけ。
  2. **二元配置の可視化**: chunk(横)× arm(系列)で past_block_gain と held_out_ppl をプロット。chunk 主効果 vs arm 主効果を目視 + 効果量で比較(H3)。
  3. **compute-matched 差分**: chunk=512(N₀)− chunk=128(4N₀)の past_block_gain / best_val_loss、seed 対応の paired 差で CI(H2)。
  4. **副次の mixer 効果**: gated-deltanet の held_out_ppl 優位(§13(4) で 25.23)が GPU 規模・複数 seed でも再現するかを確認(plateau とは別建てで記録、誇張しない)。

---

## 5. 成功基準(事前固定)と honest 内訳プラン

### 成功基準

- **PASS(H1 支持)**: ある chunk 水準で 3-seed past_block_gain の 95% CI 下限 > 0 **かつ** compute-matched 対照(§3.4)を CI 上超える。→「credit-assignment 窓拡大が有効文脈を伸ばす」を初めて実証。
- **NULL(H1 棄却・これも価値ある結論)**: 全 chunk で CI が 0 を跨ぐ、または compute-matched 対照と区別不能。→「state-carry も credit-assignment 窓拡大も plateau を動かさない」を §13 の交絡を解消した上で確定。次は別レバー(明示メモリ/retrieval/より大規模)へ。

### honest 内訳プラン(`feedback_benchmark_honest_disclosure`)

1. **compute 交絡(最優先)**: chunk 拡大で良く見えたら、**まず §3.4 の compute-matched 対照を疑う**。c512 の val 改善は 4× 勾配トークンで説明される可能性が高い(本日プローブの宿題)。
2. **弱ベースライン artifact**: past_block_gain が動いても、ベース(c==block_size)の NLL がそもそも高い(訓練不足)せいで「下げ代」が大きいだけかもしれない。`best_val_loss` 収束と `unigram_ppl` floor を併記して、絶対水準で語る。
3. **winner's curse**: chunk×arm×seed = 36 run から「一番良い 1 マス」を拾わない。主張は事前指定の主要指標(past_block_gain)× CI でのみ行い、最良セル cherry-pick を禁止。
4. **2 点指標の粗さ**: past_block_gain 単独でなく full curve を出す。途中で曲線が暴れる場合は「有効文脈が伸びた」とは言わない。
5. **規模の限定性**: char-LM・aozora 単一・~数M params の結論を「LLM 一般」へ外挿しない。「この設定で動いた/動かない」と書く。
6. **失敗を残す**: null でも全 run の JSON とこの md を保存し、「chunk を広げても動かなかった」を教訓として記録(削除しない)。

---

## 6. 実行コマンド(具体・既存引数のみ)

> 前提: §3.4 の `--device` 配線が済んでいること。以下は配線後の想定形(`--device auto` は **要追加**引数)。引数 `--chunk-size`/`--arches`/`--carry`/`--seg-len`/`--seed`/`--context-lens`/`--n-positions`/`--max-iters`/`--n-layer`/`--n-embd`/`--state-size`/`--wide-state-size`/`--ttt-state-dim`/`--batch-size`/`--out` は **すべて実在確認済**。

```powershell
# --- 主格子: chunk × arm × seed (carry on) ---
# 例: chunk=512, 全 arm, seed 1337/1338/1339 を順に
foreach ($s in 1337,1338,1339) {
  foreach ($c in 128,256,512,1024) {
    py -3.11 D:/projects/llcore/scripts/tbptt_plateau_experiment.py `
      --device auto `                                # ★要追加(migration_manifest §6)
      --corpus-file out/corpus_aozora_multi.txt `
      --arches recurrent,recurrent-wide,gated-deltanet `
      --carry on --seg-len 2048 --chunk-size $c `
      --block-size 128 `
      --n-layer 4 --n-embd 256 --state-size 256 --wide-state-size 512 --ttt-state-dim 192 `
      --max-iters 4000 --batch-size 64 --lr 1e-3 `
      --context-lens 16,32,64,128,256,512,1024,2048 --n-positions 256 `
      --seed $s `
      --out out/plateau_full/chunk${c}_seed${s}
  }
}

# --- compute-matched 対照 (chunk=128 を 2x/4x/8x iters: 256/512/1024 と勾配トークン一致) ---
foreach ($s in 1337,1338,1339) {
  py -3.11 D:/projects/llcore/scripts/tbptt_plateau_experiment.py --device auto `
    --arches recurrent,recurrent-wide,gated-deltanet --carry on --seg-len 2048 `
    --chunk-size 128 --block-size 128 `
    --n-layer 4 --n-embd 256 --state-size 256 --wide-state-size 512 --ttt-state-dim 192 `
    --max-iters 16000 --batch-size 64 --lr 1e-3 `                 # 4x N0 = chunk512 と総勾配トークン一致
    --context-lens 16,32,64,128,256,512,1024,2048 --n-positions 256 --seed $s `
    --out out/plateau_full/cm_chunk128x4_seed${s}
}

# --- carry-off 接続対照 (§13(3) と接続, chunk=128 相当) ---
foreach ($s in 1337,1338,1339) {
  py -3.11 D:/projects/llcore/scripts/tbptt_plateau_experiment.py --device auto `
    --arches recurrent,recurrent-wide,gated-deltanet --carry off --block-size 128 `
    --n-layer 4 --n-embd 256 --state-size 256 --wide-state-size 512 --ttt-state-dim 192 `
    --max-iters 4000 --batch-size 64 --lr 1e-3 `
    --context-lens 16,32,64,128,256,512,1024,2048 --n-positions 256 --seed $s `
    --out out/plateau_full/carryoff_seed${s}
}
```

> compute-matched の iters は「総勾配トークン ∝ chunk × max_iters」を揃える素朴版。`batch_size` を全 run 共通にしておけば chunk×max_iters の積一致で十分。LR スケジュール(warmup/decay は max_iters 連動)が iters で変わる点は honest 注記に残し、必要なら固定スケジュールで追試。

---

## 7. 想定アウトプット先

- `D:/projects/llcore/out/plateau_full/chunk{128,256,512,1024}_seed{1337,1338,1339}/comparison_carry_on.json`
- `D:/projects/llcore/out/plateau_full/cm_chunk128x{2,4,8}_seed*/comparison_carry_on.json`(compute-matched)
- `D:/projects/llcore/out/plateau_full/carryoff_seed*/comparison_carry_off.json`
- 集計・図・CI は別途 `out/plateau_full/ANALYSIS.md`(seed 集計 + bootstrap CI + 二元配置プロット)。本走後に MODEL_LANDSCAPE §13(4) を「交絡解消済み」で更新。
