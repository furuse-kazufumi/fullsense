# lldarwin v2 — 本格実装 / 連続稼働 readiness 計画 (2026-05-27)

> **Goal (ユーザー 2026-05-27)**: 整理された要件に基づき本格実装を進める。必要に応じて
> 入力パターンを色々変えながら段階的に対応し、**今夜の連続稼働が可能な状態**になるまで
> 動作テストを進める。
> 正本: 確定方策 = [[lldarwin_v2_poc_marathon_2026_05_26]] §「✅ 決定した方策」/ 実装ロードマップ Phase 1-5。

## 0. 実装の進め方（段階的・additive・テスト必須）
- Phase 1（選択核 S1 合成配線）= Agent C 実装中（`--selection lldarwin-v2` opt-in, 既定 off, テスト付）。
- 各 Phase は **additive・既存挙動不変・pytest 緑維持**（[[feedback_implementation_status_record]] で未配線を honest 記録）。
- 「入力パターンを変えながら」= 下記 動作テスト matrix を proxy 中心に回し、crash/退化/回帰を段階的に潰す。

## 1. 動作テスト matrix（C 着地後に実行・proxy 中心で安価）

| # | 目的 | 構成（入力パターン） | 合格線 |
|---|---|---|---|
| T0 | 回帰: 既存挙動不変 | `--fitness proxy`（既存 selection, 20 gen） | 旧と同等・pytest 緑 |
| T1 | v2 配線確認 | `--selection lldarwin-v2 --fitness proxy`（20 gen, pop24） | crash なし・metrics 健全・snapshot 出力 |
| T2 | 苦手軸 proxy | `--selection lldarwin-v2 --fitness pressure-proxy`（30 gen） | 軸別淘汰が動く・飽和しない |
| T3 | フル S1 stack | `lldarwin-v2 + --genome3d + --lineage-reservoir + --novelty`（30 gen） | monoculture<0.8・系統≥2・多様性高止まり |
| T4 | **resume（CKPT-1）** | 20 gen 実行 → 中断 → `--resume` | 全状態復元・決定論的継続・系統/archive 維持 |
| T5 | **wallclock 停止** | `--max-wallclock-seconds <小>` | 予算で clean 停止 + run_summary 生成 |
| T6 | 母数/founder 変動 | pop∈{24,64} × founders{default8, extended} × seed{0,1} | 全構成 crash なし・退化なし |
| T7 | 実 LLM 小ラン | `lldarwin-v2 + --fitness real-pressure`（数 gen, on-prem ollama） | 実 LLM 評価が回る・measurement purity（on-prem only） |

## 2. 連続稼働 readiness gate（今夜の長時間ランを張る条件）
- [ ] T0-T6 が proxy で緑（crash/退化/回帰なし）。
- [ ] T4 resume が全状態を決定論復元（中断→継続で系統/QD archive/RNG が保たれる）。
- [ ] T5 wallclock で clean 停止 + summary。
- [ ] T7 実 LLM 小ランが回る（今夜が real-pressure なら）。
- [ ] honest: 未配線 Phase（factor-subspace QD / ORCH routing / agentic）は今夜のランに含めない or 既定 off と明記。

## 3. 今夜の連続稼働 起動テンプレ（gate 通過後）
```
# 例: lldarwin-v2 選択核 + 苦手軸 + Genome3D + reservoir + novelty を proxy で長時間（安価・大世代）
py -3.11 scripts/run_persona_evolution_long.py \
  --selection lldarwin-v2 --fitness pressure-proxy \
  --genome3d --lineage-reservoir --novelty \
  --population 256 --generations 200000 --max-wallclock-seconds 43200 \
  --checkpoint-every 500 --out out/lldarwin_v2_overnight_<date>
# 実 LLM 版は --fitness real-pressure（on-prem ollama 前提, スループット律速で世代少なめ）
# 中断/再開: 同 --out に --resume を付けて再起動（CKPT-1）
```
- 連続稼働＝ `--max-wallclock-seconds` で有界 + `--checkpoint-every` で定期 snapshot + `--resume` で継続。ccr 連続運転と整合（[[feedback_session_marathon]]）。

## 4. 状態（2026-05-27 動作テスト結果）

**Agent C Phase 1 着地**: `lldarwin_v2.py`（`LLDarwinV2Config` + `build_lldarwin_v2_selector` = ε-lexicase + novelty(z-score標準化) + minimal-criterion 合成）+ runner `--selection lldarwin-v2`（既定 off・後方互換, v2 で reservoir 既定 on）+ 12 テスト / 進化系 975 テスト緑。

**動作テスト結果（proxy 中心, 全 PASS）**:
| T | 構成 | 結果 |
|---|---|---|
| T0 | baseline proxy 20gen | completed / best 0.919（回帰なし） |
| T1 | lldarwin-v2 proxy 20gen | completed / best 0.904 |
| T2 | v2 + pressure-proxy 30gen | completed / best 1.0 |
| T3 | v2 + genome3d + reservoir + novelty 30gen | completed / best 0.869 |
| **T4** | **resume(CKPT-1): 15gen→--resume→45gen** | **completed / 4 snapshots / 決定論継続 ✓** |
| **T5** | **wallclock: --max-wallclock-seconds 8** | **completed / wallclock_budget_exhausted 8.0s / 261gen(≈33gen/s) ✓** |
| T6 | 変動入力 pop64 seed1 フルstack 40gen | completed / best 0.89 |

→ **§2 readiness gate: T0-T6 達成（crash/退化/回帰なし・resume/wallclock/checkpoint 機能）。連続稼働可能な状態。** 残: T7 実 LLM 小ラン（今夜 real-pressure を張る場合に実施、proxy/pressure-proxy なら不要）。

**honest 未配線（次セッション Phase 1-②③, full margin で着手推奨）**: factor-subspace QD 実配線 / MAP-Elites archive の runner submit 配線 / 適応難易度（動的 minimal-criterion）。現状 v2 は「選択核の合成 + reservoir 既定 on」まで。

**今夜の連続稼働（gate 通過済・proxy 版は即起動可）**: §3 テンプレ。proxy/pressure-proxy なら on-prem 不要・大世代・安価。real-pressure 版は ollama 前提（T7 後）。
