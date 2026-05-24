# SPEC-MESH 先行研究調査 — 分散/branch-level speculative の被りと独自 (2026-05-24)

> rad-research (RAD コーパス llm/vllm の speculative クラスタ 163 docs + WebSearch/外部調査)
> による SPEC-MESH 本格導入の関連研究確認。**結論: SPEC-MESH の核心機構は先行研究が厚く、
> 完全な新規ではない。独自価値は署名/Byzantine 検証/SPC grounded/on-prem 純度に集中すべき。**
> 規約: [[feedback_originality_over_imitation]](網羅でなく選別) /
> [[feedback_benchmark_honest_disclosure]](勝った気になる前に内訳を疑う)。

## 3 行サマリ

1. **被り**: 分散 speculative (DSD)・branch-level 投機 (B-PASTE)・fast-fallback (Speculative
   Actions)・「通信遅延→投機計算」(DSD)・acceptance-rate 依存 ROI — **すべて 2025-2026 に先行研究あり**。
2. **独自**: Ed25519 署名 manifest + **Byzantine 結果検証 (SPEC-MESH-11)**・**SPC warning-zone
   grounded な投機トリガ**・on-prem measurement purity との両立 — 先行研究が薄く、ここに価値を集中すべき。
3. **あえて範囲外**: token-level speculative decoding 自体 (EAGLE3/DART 等) は llmesh が
   推論層でない以上 **不採用が正しい**。SPEC-MESH は task/branch-level に限定。

## 参照した RAD 分野 + 外部

- ローカル RAD: `D:/docs/llm_corpus_v2/cluster_06_speculative_dec`(102 docs: StarSD 分散 serving /
  EAGLE3 / TriSpec・PACER の ternary verification / edge decoding)、
  `D:/docs/vllm_corpus_v2/cluster_03_decoding_specul`(61 docs: **token acceptance ambiguity** /
  **speculative decoding の side-channel 脆弱性** / tree drafting acceptance rate)
- 外部 (arXiv, 2025-2026): 下記 TOP-N。

## 関連研究 TOP-N(横断)

### 分散 / decentralized speculative(SPEC-MESH の mesh 側に直撃）
1. **Speculative Decoding in Decentralized LLM Inference: Turning Communication Latency into
   Computation Throughput** (arXiv 2511.11733) — 通信待ちを投機検証に変換。コスト削減
   `≈ (N-1)·t1·(k-1)/k`(N=node 数, t1=link latency, k=平均 accept token)。**network latency が
   compute を支配する設定で勝つ**(=SPEC-MESH の big-model/swap-bound・LAN 条件と同構造)。
   adaptive token weighting で +15-20%。plug-and-play(再学習不要)。HumanEval 2.56x。
2. **Communication-Efficient Collaborative LLM Inference via Distributed Speculative Decoding**
   (2509.04576) — full vocab 分布送信は通信過大 → **Top-K Sparse Logits Transmission (TK-SLT)**。
   → SPEC-MESH の **typed diff (予測誤差) push** = llrepr CRDT/JSON Patch と同じ発想。
3. **CoSine: Collaborative Speculative Inference** (2503.10325) — heterogeneous GPU multi-node 協調。
   sequential drafting と parallel verification を分離。
4. **StarSD: One-for-Many Speculative Decoding** (2601.21622, ローカル corpus にも収録) —
   単一 draft を multi-accelerator cluster で再利用。FlowSpec (2507.02620) / edge-cloud DSD
   (2511.21669) / heterogeneous edge (2510.11331) も同系統。

### agentic / branch-level speculative(SPEC-MESH の branch=ChangeOp/Brief 投機に直撃）
5. **Speculative Actions: A Lossless Framework for Faster Agentic Systems** (2510.04371) —
   「microprocessor の speculative execution + speculative decoding に着想。agent が faster
   model で次 action を予測・暫定実行し、slower ground-truth executor が追いつく」=
   **SPEC-MESH の fast-fallback (SPEC-MESH-04) と完全に同じ思想**。lossless。
6. **B-PASTE: Beam-Aware Pattern-Guided Speculative Execution** (2604.16469) — tool-level →
   **branch-level**(bounded future subgraphs)に拡張。**raw 実行確率でなく critical-path
   reduction で ranking** し、transient slack に高価値 branch prefix のみスケジュール。
   → SPEC-MESH-01 予測器への示唆(後述)。
7. **PASTE: Pattern-Aware Speculative Tool Execution** (2603.18897) — tool 実行 48% 短縮、
   idle CPU core 1-3 + 250MB で投機。
8. **Can We Predict Before Executing ML Agents?** (2601.05930) / Search Agent speculation
   (2511.20048) — 実行前予測・search agent の投機。

### acceptance / 予測精度(SPEC-MESH-01 hit_rate に直撃）
9. **Speculative Verification: Exploiting Information Gain** (2509.24328) — draft の出力分布と
   companion model の分布を情報理論的に比較し acceptance 尤度を推定。**重要**: 「draft 内部信号や
   **過去の acceptance 履歴で acceptance を予測する手法は batch size 増で無効化**」と指摘。
10. **Learning To Draft (RL adaptive)** (2603.01639) / Confidence-modulated verification —
    drafter の confidence(entropy/margin)で drafting window 長と verification 厳格さを実時間調整。
11. **side-channel** (vllm cluster_03): speculative の accept/reject パターンが timing 経由で
    入力を leak しうる。→ SPEC-MESH の fail-closed/署名と接続すべきセキュリティ論点。

## 被り / 独自 / あえて不採用(核の表）

| 観点 | 先行研究(被り) | SPEC-MESH の独自 | あえて不採用/範囲外 |
|---|---|---|---|
| 通信遅延→計算 | **DSD** 2511.11733 | 予測符号化(neuroscience)+ **SPC warning-zone grounded** トリガ(産業 IoT) | — |
| branch-level 投機 | **B-PASTE** 2604.16469 | ChangeOp/Brief という llive 進化の具体ドメイン | — |
| fast-fallback | **Speculative Actions** 2510.04371 | SPEC-MESH-04 を最高優先で最初から組込(後付け不可) | — |
| 結果の信頼 | side-channel 研究のみ(薄い) | **Ed25519 署名 + Byzantine 結果検証 (SPEC-MESH-11)** = 主要差別化 | — |
| acceptance 予測 | Speculative Verification 2509.24328(履歴予測は batch で無効) | hit_rate honest 単体測定 (SPEC-MESH-01) | token-level acceptance |
| 通信量削減 | **TK-SLT** 2509.04576 | typed diff(予測誤差)push = llrepr | — |
| token-level SD | EAGLE3/DART/多数 | — | **llmesh は MCP hub=推論層でない → 範囲外** |
| on-prem 純度 | (先行なし) | measurement purity(cloud fail-closed)と両立 | — |

## SPEC-MESH 要件への含意(honest)

1. **核心は車輪の再発明リスク**: 分散 speculative + branch-level + fast-fallback は 2025-2026 に
   先行研究が厚い。**rad-research を SPEC-MESH 着手前にやるべきだった**(規約=新設計着手前に先行調査)。
   今後の本格導入は「先行研究に対する独自性」を主張できる部分に投資を絞る。
2. **独自に集中**: Ed25519 署名 manifest + **Byzantine 結果検証 (SPEC-MESH-11)** は先行研究が薄い
   (untrusted mesh の *結果汚染* を扱う研究は少ない)。+ **SPC grounded トリガ**(warning-zone 先回り)
   + on-prem 純度。ここが FullSense の真の差別化核。
3. **SPEC-MESH-01 予測器の改良方向**: B-PASTE の「**critical-path reduction で ranking**(raw 確率
   でない)」を取り込み、hit_rate だけでなく **ROI 重み(SPEC-MESH-06 重い分岐優先)を予測器に統合**
   する余地。「履歴予測は batch で無効化」(2509.24328)も honest disclosure に追記すべき(ただし
   SPEC-MESH は token batch でなく branch 投機なので文脈は異なる)。
4. **範囲の確定**: token-level speculative decoding は **不採用が正しい**。llmesh は MCP hub であり
   token 推論を持たない。SPEC-MESH は task/branch-level (ChangeOp/Brief) に限定する。

## 推奨次アクション

- [ ] SPEC-MESH 要件 (`llmesh/docs/requirements_speculative_mesh.md`) に本調査の「被り/独自」を反映し、
      §3 成功基準を「先行研究に対する独自性 (署名/Byzantine/SPC) の実証」に寄せる。
- [ ] SPEC-MESH-01 予測器に critical-path / ROI 重み付けを検討(B-PASTE 流)。
- [ ] Speculative Actions (2510.04371) と DSD (2511.11733) を熟読し、fast-fallback の安全な遅延結果
      破棄の実装を借用(車輪の再発明回避)。
- [ ] 結合判断 (llive↔llmesh) はユーザー領域 — 本調査を判断材料として提示。

## Sources

- [DSD decentralized 2511.11733](https://arxiv.org/abs/2511.11733) / [TK-SLT 2509.04576](https://arxiv.org/abs/2509.04576) / [Fast Collaborative 2512.16273](https://arxiv.org/abs/2512.16273) / [CoSine 2503.10325](https://arxiv.org/pdf/2503.10325) / [StarSD 2601.21622](https://arxiv.org/pdf/2601.21622) / [FlowSpec 2507.02620](https://arxiv.org/pdf/2507.02620) / [heterogeneous edge 2510.11331](https://arxiv.org/abs/2510.11331) / [edge-cloud DSD 2511.21669](https://arxiv.org/pdf/2511.21669)
- [Speculative Actions 2510.04371](https://arxiv.org/pdf/2510.04371) / [B-PASTE 2604.16469](https://arxiv.org/html/2604.16469) / [PASTE 2603.18897](https://arxiv.org/html/2603.18897) / [Search Agent 2511.20048](https://arxiv.org/pdf/2511.20048) / [Predict Before Executing 2601.05930](https://arxiv.org/pdf/2601.05930)
- [Speculative Verification 2509.24328](https://arxiv.org/html/2509.24328v1) / [Learning To Draft 2603.01639](https://arxiv.org/html/2603.01639v1) / [Online Speculative Decoding 2310.07177](https://arxiv.org/pdf/2310.07177)
- ローカル RAD: `D:/docs/llm_corpus_v2/cluster_06_speculative_dec`, `D:/docs/vllm_corpus_v2/cluster_03_decoding_specul`
- 関連: `requirements_speculative_mesh.md` (SPEC-MESH-01..11) / `spec_mesh_01_b1_feedback_2026_05_24.md` / memory `project_idea_speculative_mesh_execution`
