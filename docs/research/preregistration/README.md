# GPU 実験 事前登録(pre-registration)— 索引

- **作成**: 2026-06-28
- **status**: 全実験 `pre-registered`(実行は **RTX 5090 32GB 着荷後** / 2–3 週間先)
- **目的**: 着荷後の GPU 時間を即・結果に変えるため、実験を **今すべて事前登録** して解析自由度を凍結し、p-hacking を回避する(honest disclosure 規律 = `feedback_benchmark_honest_disclosure`)。
- **方針正本**: `../interim_research_agenda_2026-06-28.md` §T1 / `../gpu_pc_migration_plan_2026-06-28.md` §6 / `../migration_manifest_2026-06-28.md` §6(device 配線)

> **凍結方針**: 各 md は arm 集合・seed 数(≥3)・主要指標(1 つ事前指定)・compute-matched 対照・成功基準・棄却条件・honest 内訳プランを **実行前に固定**。GPU 着荷後はここに書いた手順「のみ」を実行し、走らせてから指標・閾値・arm を選び直さない。結果(PASS / NULL いずれも)は削除せず記録する。

## 3 実験の 1 行サマリ

| # | ファイル | 主要仮説 | 主要指標 | seed / arm |
|---|---|---|---|---|
| 1 | [`prereg_plateau_full.md`](prereg_plateau_full.md) | §13(4) の交絡(chunk=block で勾配 truncate)を解消 = chunk_size を広げると有効文脈 plateau が **compute-matched 対照に対しても**動くか | `past_block_gain`(seed 横断 bootstrap CI)| ≥3 seed(1337/1338/1339)× chunk{128,256,512,1024} × arm{recurrent, recurrent-wide, gated-deltanet}+ compute-matched 対照 |
| 2 | [`prereg_linearization_distill.md`](prereg_linearization_distill.md) | 出力 MSE 蒸留(=LoLCATs Step1 相当)は同一メモリでより多層を線形化可能にし frontier を **右シフト**するか | distilled frontier の HV 右シフト %(`right_shift_ci`、95% CI 下限>0)| ≥3 seed(0/1/2)× mixer{softmax/linear/SWA/window-linear} × feature_map{diag,full} × 蒸留{zero-shot, 出力MSE, ★logit-KD/LoRA=要実装} |
| 3 | [`prereg_proxy_v2_full.md`](prereg_proxy_v2_full.md) | 層別 hybrid memetic NAS が greedy/固定ヒューリスティックに **holdout で**勝つか(winner's curse 除去後)| memetic-vs-greedy の holdout HV gain %(`honest_verdict` 経由、CI 下限>0)| ≥3 seed(0/1/2)× {greedy, memetic} × {蒸留 on/off}、K≥12 holdout、context sweep …4096、cross-corpus |

## 共通の前提・honest 注記

- **device 配線(★全実験の前提)**: **実験 1(plateau)経路は ✅ 配線済(2026-06-28)** — `scripts/tbptt_plateau_experiment.py` / `ttt_plateau_experiment.py` / `prove_native_matches_hf.py` に `--device`(default `auto = cuda if available`)、`Trainer`/`TBPTTTrainer`/`eval`/`longctx_eval` が model device を推論し batch を移動(新規 `src/llcore/lm/device.py`)。CPU byte-identical(既存スイート全 green)+ mypy/ruff PASS で確認済。**実験 2/3 経路は未配線**: `nas_pareto.py` / `linearize_tolerance.py` / `evolve_linearization.py` は `load_qwen2` の `to(device)` 未配線 — 着荷後 Day 1 に同様 backward-compatible に追加(`migration_manifest_2026-06-28.md` §6 のパターン踏襲)。
- **実装状態の正直開示**(`feedback_implementation_status_record`): 実験 2 の **logit-KD / LoRA Step2 / end-to-end 本訓練は未実装**(現 distill は per-layer の attention 出力 MSE = LoLCATs Step1 相当のみ)。これらは要実装で、完了後に該当 md を改訂して別 run。
- **要用意データ**: 実験 2/3 の `--cross-corpus` 用 **disjoint コーパス**(aozora と非重複)。
- **検証済み参照コード/doc**(本 prereg が引用した一次ソース):
  - 実験コード: `scripts/tbptt_plateau_experiment.py` / `scripts/ttt_plateau_experiment.py` / `scripts/nas_pareto.py` / `scripts/linearize_tolerance.py` / `scripts/evolve_linearization.py`
  - 指標/中核: `src/llcore/lm/longctx_eval.py`(`context_length_curve` / `past_block_gain` の素・`streaming_metrics_by_band`)/ `src/llcore/lm/eval.py`(`held_out_report_any`)/ `src/llcore/runtime/eval_proxy.py`(proxy-v2)/ `src/llcore/runtime/distill.py` / `src/llcore/runtime/linearize.py`
  - 知見 doc: `docs/MODEL_LANDSCAPE_2026_06.md` §13(1)(2)(3)(4)・§14 / `docs/NEXT_SESSION.md` / `docs/CONVERSATIONAL_LLCORE_FINDINGS.md`
  - 本日プローブ(一次確認): `out/ttt_chunk_probe/c128/comparison_carry_on.json`(past_block_gain=0.0、flat)/ `out/ttt_chunk_probe/run.log`(c512 走行途中、val 改善も curve 未書き出し=未確定)
- **共通 honest 内訳プラン**(`feedback_benchmark_honest_disclosure`): ① compute 交絡(多 compute で良く見えていないか)② 弱ベースライン artifact ③ winner's curse(最良セル cherry-pick 禁止、holdout で語る)④ 短文脈の盲点(長 L で消える改善を「回復」と呼ばない)⑤ 規模の限定性(char-LM/0.5–1.5B/aozora を LLM 一般へ外挿しない)⑥ 失敗(NULL)も削除せず記録。

## 着荷後の実行順(初手 GPU ワークロード、migration plan §6)

1. device 検証 — 実験 1 経路は配線済なので `verify_new_machine.ps1`(`prove_native_matches_hf.py --device cuda` GPU golden 一致 + plateau 小 step smoke)を走らせるだけ。実験 2/3 経路は `nas_pareto.py`/`linearize_tolerance.py` に device 追加(~30分)。
2. **実験 1(plateau full)** — 本日プローブの直接の続き、方向を最も解決する。配線済=即走行可。
3. **実験 3(proxy v2 full)** — NAS の中心主張を holdout で確定。
4. **実験 2(linearization distill)** — 既存=出力 MSE 蒸留の右シフトをまず確定、logit-KD/LoRA は要実装後。
