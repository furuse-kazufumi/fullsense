# 間奏期(GPU 着荷待ち ~2-3週間)研究アジェンダ — 2026-06-28

> 方針(ユーザー 2026-06-28): GPU 付き PC(RTX 5090/32GB/128GB)着荷後に本格研究。
> **それまでは重い compute を避け、低 compute・高レバレッジな調査と設計を主体に**=
> 着荷後すぐ走らせる「弾込め」期間。規律 = `feedback_claude_max_compute_priority`
> (Max 計算は decision-relevant: 方向研究・**事前登録の実験設計**・honest 実測)。
> 関連 = `gpu_pc_migration_plan_2026-06-28.md` / `migration_manifest_2026-06-28.md`
> / memory `project_llcore_efficient_arch_landscape_2026_06_26` / `project_fullsense_unified_model_vision`。

## 優先順位つきタスク(低 compute・GPU 不要)

### T1. ★GPU 実験の事前登録設計(最優先・純 design)
着荷後の GPU 時間を**即・結果**に変えるため、実験を今すべて pre-register する(p-hacking 回避=honest)。
- **plateau フル(§13(4))**: chunk∈{128,256,512,1024} × {recurrent, recurrent-wide, gated-deltanet} × **≥3 seeds** + **compute-matched 対照**(chunk=128 を 4× iters)。成功基準・解析手順・honest 内訳を先に固定。本日プローブ(c128/c512 単 seed)の結果を踏まえて確定。
- **線形化 本訓練 + 蒸留**(改造①④): base/target 再帰・distill loss・held-out eval プロトコルを明文化。
- **proxy v2 フル**: K≥12・context sweep 2048–4096・cross-corpus・指標を確定。
- 出力: `docs/research/` の事前登録設計 md(各実験 1 枚)。

### T2. 線形化レシピ深掘り(rad-research)
design-space map は「amenability」止まり → **実レシピ**(LoLCATs / SUPRA / MOHAWK / Mamba-in-Llama)の手順・損失・どの層から・RoPE 処理を比較し、llcore の採用方針を 1 本に。
- RAD: `open_model_architectures` / `llm` / `neural_network` / `vllm`。出力: レシピ比較 + 採用案。

### T3. 蒸留 for constant-state students(rad-research)
線形 attn/SSM student への蒸留(feature-map matching / logit / 層別)の有効プロトコル。
- RAD: `deep_learning` / `neural_network` / `mlops`。出力: distill 手順の確定。

### T4. 効率アーキ landscape refresh(rad-research)
`project_llcore_efficient_arch_landscape_2026_06_26`(L1-7 leads / コア=LoLCATs / plateau 本命=TTT)を 6/26 以降の新着で更新。Hermes 等の競合地図も refresh。
- RAD: `open_model_architectures` / `llm` / `deep_learning`。出力: landscape memo 更新。

### T5. 北極星=メモリ効率統合モデルの差別化(調査+整理)
memory-efficient LLM の SOTA と、llcore の gap/貢献(`project_fullsense_unified_model_vision`)を整理。新規性軸を明文化。

### T6.(パーク)VLM スコープ
着手は北極星を緑にしてから(option a)。32GB ローカル VLM × manga/comic(`vlm_comic_comprehension`/`manga_craft` corpus)。pursue 決定時のみ rad-research → hello-world。

## 進め方
- **rad-research / triz / cross-domain は低 compute = 間奏期に最適**。重い GPU 実験(本走)は着荷後。
- 調査は `feedback_research_to_rad_autoingest` に従い結果を RAD へ取込み、設計は事前登録 md に。
- 記事・SVG 等 content は方向確定後(`feedback_claude_max_compute_priority`)— 間奏期は研究/設計が主。
- 1 セッション = T1（設計）を軸に、T2-T5 の調査を 1-2 本ずつ。
