---
layout: default
title: "SPEC-MESH-01 完遂 + B1 stale 訂正 + stdio_server 状態訂正"
parent: "Research"
nav_order: 98
---

# SPEC-MESH-01 完遂 + B1 stale 訂正 + stdio_server 状態訂正 (2026-05-24)

> 本日 llive / llmesh で着地した 3 件を FullSense honest disclosure 文化
> (合成/実測の区別・未実装/部分実装/完了の正確な区別) に沿ってまとめた
> フィードバック資料。表現/予測符号化系の続き
> ([[llrepr_poc_2026_05_24]] / [[predictive_push_poc_2026_05_24]] /
> [[acceleration_poc_matrix_2026_05_24]]) として、高速化 Tier 1 (Speculative
> Mesh) の **要件着手 1 件目** が完了した記録。

**本日の到達点 (3 行サマリ):**

1. **SPEC-MESH-01 完遂** — 分岐予測器 (Frequency / Markov) を実装し hit_rate を
   単体測定。「構造があるときだけ baseline を超える」を確認 (sanity 通過・過剰主張なし)。
2. **致命バグ B1 が「実は修正済み」と確定** — stale 記録を回帰テスト 3 件で訂正。llive
   進化トラック再開の障壁が 1 つ減った。
3. **stdio_server / predictive_push transport は配線完了済**と確認 — NEXT_SESSION の
   「未了」記述は stale。残る未了は **実 LLM explainer のみ**。

---

## 1. 成果1 — SPEC-MESH-01 (分岐予測器 hit_rate 単体測定) 完遂

[[acceleration_poc_matrix_2026_05_24]] の **Tier 1 = Speculative Mesh** が本格導入の
最有力 (要件定義 `llmesh/docs/requirements_speculative_mesh.md` SPEC-MESH-01..10 済) と
判定された。その **本格導入の道筋 step 1 = 「予測器の hit_rate 単体測定」(SPEC-MESH-01)**
を着地した。

### 1.1 実装

llive `src/llive/evolution/branch_predictor.py` (+ `branch_predictor_bench.py` +
`tests/unit/test_branch_predictor.py` **16 tests green**)。最小予測器 2 種:

| 予測器 | 文脈 | 役割 |
|---|---|---|
| `FrequencyPredictor` | なし | **baseline** — 観測頻度の最頻値を常に予測 (order-0)。 |
| `MarkovPredictor` | order-1 | 直前イベントから次イベントを条件付き予測。 |

予測は **opaque branch dict** で出力し、`llmesh.speculative.manifest.SpeculativeManifest.new(branch=...)`
にそのまま渡せる (mesh 投機の入力として接続可能)。online next-step で hit_rate を
単体測定する harness を同梱。

### 1.2 測定結果 (合成系列, k=1)

| 系列 | 構造 | Frequency (baseline) | Markov (order-1) |
|---|---|---|---|
| iid | 構造なし | 0.25 | 0.24 (≈ baseline) |
| skewed (.70) | 偏りのみ | 0.70 | ≈ freq (文脈で増えない) |
| markov-1 noisy (.85) | order-1 文脈あり | 0.23 | **0.87** |
| cyclic | 完全周期 | 0.25 | **0.999** |

**意味**: 予測器は「**構造があるときだけ**」baseline を超える。構造なし (iid) では
Markov ≈ Frequency = **sanity 通過** (文脈を持つだけで過剰に勝つ self-deception が無いこと
の確認)。skewed では Frequency で既に天井 = Markov が文脈で更に増やせる余地がない正常挙動。
order-1 構造・周期構造でのみ Markov が baseline を大きく上回る。

### 1.3 honest disclosure (必須)

1. **合成系列のみ** — 実運用 hit_rate は **ChangeOp 実ログ待ち**。上表の数字は構造の
   有無で予測器の損益が分かれることを示すためのもので、実配線後に上書きする。
2. **hit_rate ≠ speedup** — 当たっても投機が wall-clock を縮めるかは別問題。**ROI は
   SPEC-MESH-07 (実測) 待ち**。hit_rate は投機価値の必要条件であって十分条件ではない。
3. **前提ブロック (重要)** — ChangeOp を**系列的に**出す稼働進化ループが**未稼働**。
   `llive/evolution/bench.py` の `BenchHarness` は単発 candidate diff を 1 回 apply する
   だけで **ops を捨てる** (系列を生成しない)。したがって実測 hit_rate は
   **container 多世代進化ループの稼働が前提**。予測器は出来たが、それを食わせる
   「系列ソース」がまだ無い、という部分実装の正直な計上。

> 言い換えると: SPEC-MESH-01 は **予測器側を完成させ、ボトルネックが「系列を出す
> 稼働進化ループの不在」に移った**ことを定量的に示した。次の本格導入ステップ
> (実 hit_rate / ROI) は進化ループの稼働とセットでないと測れない。

### 1.4 着地物

- 測定 doc: `llive/docs/perf_comparison/branch_predictor_hit_rate_2026_05_24.md`
- commits: llive `6439c8a` (predictor) / `2427c71` (前提ブロック追記) /
  llmesh `9d57c9b` (`requirements_speculative_mesh.md` の SPEC-MESH-01 を完了マーク)

---

## 2. 成果2 — 致命バグ B1 が「実は修正済み」と確定 (stale 記録訂正)

### 2.1 背景 (記録されていた内容)

`claude-projects.json` と memory に、llive 進化トラックの **再開前要修正項目**として
次が記録されていた:

> **B1**: 19-dim persona genome で `backend_id` を**位置で誤読** → on-prem fail-closed で
> 全個体淘汰。

これは [[acceleration_poc_matrix_2026_05_24]] / PROGRESS Phase 0.20/0.21 でも「llive 進化
再開の障壁」として参照されていた。

### 2.2 実態 (検証結果)

`Genome.value_by_label(label, fallback_index)` (genome.py) による **label 解決**が、既に:

- `fitness_llm._genome_field`
- `LlivVariantBuilder.build_config`

の双方に**入っており**、`backend_id` を**位置ではなく label (idx13)** で正しく解決していた。
すなわち **B1 は既に修正済み** = 記録が **stale** だった (Phase 0.21 の commit で解消済みの
内容が、別 doc 側に「未修正」として残っていた drift)。

### 2.3 確定 (回帰テストで pin)

回帰テスト `llive/tests/unit/test_evolutionary_b1_persona_label.py` (**3 件 green**) を追加:

- idx0 に cloud 誤読値 (1.0) を置いても**淘汰されない** (position 誤読が無いことの証明)。
- idx13 の cloud 値は**正しく淘汰される** (label 解決で正しい位置を見ていることの証明)。

commit: llive `9c966a9`。

### 2.4 残課題 (B2 のみ)

- **B2**: quality rubric が「text 長 heuristic」 → instance-specific checklist へ、は**未対応**。
- ただし mock backend は固定出力で checklist 採点が**選択圧にならない** (どの個体も同じ
  text を返すため rubric が個体を区別できない)。したがって B2 は **実 LLM fitness 配線と
  一体で対応すべき** (実 LLM judge が前提)。単独で rubric だけ差し替えても toy のままで意味が
  立たない、という honest disclosure。

### 2.5 含意

「**再開前要修正 B1**」が消えたことで、llive 進化トラック再開の障壁が **1 つ減った**。
残る進化系の本質課題は §A6 (外的 grounding ゼロ = 全 fitness が mock/proxy で rumination)
に集約され、これは実 LLM fitness 配線 (B2 と同じ前提) で初めて解ける。

---

## 3. 成果3 — stdio_server / predictive_push transport は配線完了済 (状態訂正)

FullSense の `docs/NEXT_SESSION.md` に次の記述があった:

> 🤖 未了: stdio_server の protocolVersion 2025-06-18 + outputSchema + 実ツール出力配線。

**実際は配線完了済**であることを確認した (状態訂正)。`llmesh/llmesh/mcp/stdio_server.py`:

| ハンドラ | 実装状況 |
|---|---|
| `_handle_initialize` | protocolVersion **"2025-06-18"** を返す ✅ |
| `_handle_tools_list` | **outputSchema** を宣言 ✅ |
| `_handle_tools_call` | **structuredContent + text 併置** (後方互換) ✅ |

加えて predictive_push の **MQTT/SSE transport** も `llmesh/predictive_push/sinks.py`
(`SsePushSink` / `MqttPushSink` / `JsonlSink` / `CallbackSink`) で**着地済**
([[predictive_push_poc_2026_05_24]] の egress sinks と同一)。

**残る未了**は **実 LLM explainer のみ** (現状テンプレ。`LLMExplainer` の `llm` callable に
on-prem backend + PromptFirewall / PrivacySummarizer を通す配線が残)。これは [[llrepr_poc_2026_05_24]] §5 /
[[predictive_push_poc_2026_05_24]] §3 の honest disclosure と一致する (どちらも「実 LLM
explainer は未配線」を既に明記しており、stdio_server / transport の方は完了済だった)。

> drift の原因: NEXT_SESSION.md は手書きで、stdio_server 配線が完了した時点 (予測符号化
> push PoC 着地時) に「未了」記述が更新されなかった。本資料で訂正し、NEXT_SESSION.md /
> PROGRESS.md にも反映した。

---

## 4. まとめ — 本格導入トラックの現在地

| 候補 (Tier 1) | step | 状態 |
|---|---|---|
| Speculative Mesh | SPEC-MESH-01 (予測器 hit_rate 単体測定) | ✅ 完遂 (合成系列。実 hit_rate は進化ループ稼働待ち) |
| Speculative Mesh | SPEC-MESH-07 (ROI 実測) | 進化ループ稼働 + 実 transport 配線後 |
| llive 進化トラック | B1 (genome label 誤読) | ✅ 既修正と確定 (回帰テストで pin) |
| llive 進化トラック | B2 (quality rubric) / §A6 (外的 grounding) | 実 LLM fitness 配線と一体で対応 |
| llmesh MCP / push | stdio_server 2025-06-18 + outputSchema + transport | ✅ 配線完了済 |
| llmesh MCP / push | 実 LLM explainer | 残る唯一の未了 |

**共通の前提ブロック**: 3 件とも実測/本格導入の最後の鍵が **実 LLM 配線** (進化 fitness /
explainer / 稼働進化ループ) に収束している。合成/proxy の段階は出揃い、honest disclosure
としては「**仕組みは出来た、実 LLM を繋ぐと初めて意味のある数字が出る**」が本日の正確な
現在地。

---

## Sources / 関連

- 高速化判定: [[acceleration_poc_matrix_2026_05_24]] (Tier 1 = Speculative Mesh / 本格導入の道筋 step 1)
- 表現層 / 予測符号化: [[llrepr_poc_2026_05_24]] / [[predictive_push_poc_2026_05_24]]
- 測定 doc: `llive/docs/perf_comparison/branch_predictor_hit_rate_2026_05_24.md`
- 実装:
  - llive `src/llive/evolution/branch_predictor.py` (+ bench + tests) — commits `6439c8a` / `2427c71`
  - llive `tests/unit/test_evolutionary_b1_persona_label.py` — commit `9c966a9`
  - llmesh `requirements_speculative_mesh.md` SPEC-MESH-01 完了マーク — commit `9d57c9b`
  - llmesh `llmesh/mcp/stdio_server.py` + `llmesh/predictive_push/sinks.py` (配線完了済)
- 規約: [[feedback_benchmark_honest_disclosure]] (異常に良い数字は内訳を疑う) /
  [[feedback_implementation_status_record]] (未実装/部分実装/完了の正確な区別) /
  [[feedback_poc_feasibility_first]] (要件→PoC→フィジビリティ)
