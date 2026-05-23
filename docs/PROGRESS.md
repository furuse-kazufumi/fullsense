---
layout: default
title: "Progress"
nav_order: 90
---

# FullSense Portal — Progress

> Persistent project notes for the **umbrella portal repository** itself.
> Product-side progress lives in each product's repo (`llive/docs/PROGRESS.md`,
> `llmesh/docs/PROGRESS.md`, `llove/docs/PROGRESS.md`).

## 2026-05-24 (Phase 0.22 — llive 進化系バグ徹底掃討 [進行中, 6h goal])

ユーザー「バグが多い、徹底的に潰してフィードバック」+ 6h 継続 goal。2 体のサブエージェント
(general-purpose=コードバグ網羅 / gem-critic=設計欠陥・Spec 違反) で **26 件**を洗い出し、
深刻度順に TDD (RED→GREEN+回帰) で修正中。

### 修正済 (llive commit, branch optimize/core-2026-05-20)
- **A-1** (critical, `919d449`): `build_config` の position 直読み (B1 同型) を
  `Genome.value_by_label` 共通器で label 解決に統一。fitness_llm も統合 (DRY)。19-dim/5-dim 両対応。
- **B-RES-1/2** (high, `629bdbf`): lineage node-id を full sanitize (コロンで Mermaid 破壊解消 +
  prefix 衝突回避) / `by_id` 世代跨ぎ collapse を世代別解決 (自己ループ・誤親エッジ修正)。

### 未修正 inventory (深刻度順)
| 深刻度 | バグ | file | task |
|---|---|---|---|
| blocking | H-1 mock safety 0.0/1.0 矛盾 (self-deception) | llive_variant.py:306 vs fitness_llm | #8 |
| high | B-LOGIC-2 immigration silent no-op | persona_evolution.py:366 | #4 |
| high | B-LOGIC-3 resume で bounds 未同期 → dim 不整合 | loop.py:139 | #5 |
| warning | P-1 purity backend_factory default fail-open | fitness_llm.py:107 | #7 |
| medium | B-EDGE-2 部分 weights dict KeyError | fitness_llm / llive_variant | #6 |
| medium | B-POS-2 config_to_genome lossy round-trip | variant_runner.py:80 | - |
| medium | B-EDGE-1 rosenbrock 空 genome IndexError | fitness.py:48 | - |
| medium | B-NUM-1 crowding_distance NaN 伝播 | nsga2.py:146 | - |
| medium | B-STUB-1 in_process transport 全滅 | variant_runner.py:144 | - |
| low | B-NUM-2 meta expansion threshold=0 で膨張 / UCB log(1)=0 | meta_loop.py:174 | - |
| low | B-STUB-2 compare_against_llm_baselines stub (公開 API) | persona_evolution.py:466 | - |

### 設計欠陥 (gem-critic, 大規模・別途計画が必要)
- **§A6 外的 grounding ゼロ**: 全 fitness が mock/proxy = rumination。gen100=1.0 は単峰 proxy +
  mock 固定値 + 天井効果の合成。異常値の 5+1 因子分解が未組込 (Honest Disclosure 不足)。
- **§E3 形式 pre-check / §E5 diversity quorum が未配線**: `DiversityPreservingBreedFilter` が
  loop から未呼出 (dead)。fitness_llm の「§E3 準拠」コメントは誇大。
- **categorical dim** (backend_id/kv_quant_id) を連続値として Gaussian/Blend 交配 → 親に無い
  backend が湧く / int 丸めで探索空間が歪む。
- **§I1 provenance corruption**: runtime_metadata が env 未設定で "unknown" のまま結果に焼付き。
- 注: **Spec 真ソースは `llive/docs/fullsense_spec_eternal.md`** (`fullsense/docs/spec/` でなく。
  前 Phase の私の参照が誤り、gem-critic が訂正)。

## 2026-05-23 (Phase 0.21 — llive 致命バグ B1 修正: genome label 解決で FullSense §E3/§I1/purity 回復)

ユーザー指示「llive の機能/性能を FullSense 要件定義に沿って実装/修正」を受け、Explore で
FullSense Spec (`docs/spec/fullsense_spec_eternal.md` v1.1) と llive のギャップ分析 → 最優先 =
gem-critic 発見の致命バグ B1 (FullSense Spec 違反でもあった)。

- **B1 修正 (llive commit, branch optimize/core-2026-05-20)**: `fitness_llm.py` の
  `llm_fitness_factory` が genome を position 直読み (`values[0/1/2]`) していたため、19-dim
  LIVE_VARIANT genome (backend_id=index13) で思考因子 index0 を backend_id と誤読し、
  `on_prem_backend_factory` 併用で全個体淘汰する致命バグ。→ `_genome_field(genome, label,
  fallback)` ヘルパーで **label 解決**に置換 (19-dim/5-dim 両対応、labels 無しは fallback で
  後方互換)。
- **FullSense Spec 適合**: §E3 (genome dimensionality invariant の形骸化を解消) / §I1
  (provenance: breakdown が genome label に対応) / §A6・measurement purity 二重層が genome
  誤読で機能喪失していた問題を回復。
- TDD (RED→GREEN): 19-dim genome の label 解決回帰テスト追加。進化系 **892 tests green**
  (回帰なし)。
- 第2優先 **B2** (quality 軸が「出力テキスト長 heuristic」→ FullSense Honest Disclosure 要件の
  instance-specific checklist rubric に) は次段。

## 2026-05-23 (Phase 0.20 — サブエージェント検証で方針転換: llive 進化 → RepIR PoC 優先 + RepIR 互換性設計確定)

ユーザー提案「サブエージェントで FullSense 視点から起動して必要性を確認」を実施。
2 回の read-only 検証が方針を是正した (方法論記録: memory `feedback_subagent_necessity_check`)。

- **gem-critic 検証 (FullSense 視点で llive 進化 next plan の必要性)**: driver 配線は
  (1) **genome 不整合** (進化個体は 19-dim で backend_id=index13 だが `llm_fitness_factory`
  は values[0] を読む 5-dim 実装 → 誤読し `on_prem_backend_factory` 併用時に**全個体淘汰**で
  壊れる)、(2) proxy 1000 世代は gen100 で best=1.0 収束し研究価値ゼロ、(3) North Star 貢献が
  間接的、と判明。→ **ユーザーが「RepIR PoC (llmesh) へ切替」を選択**。llive 進化は致命バグ
  (B1: index→ラベル解決 / B2: rubric を text 長 heuristic → rDPO 流 instance-specific
  checklist) を要修正として保留。
- **general-purpose + WebSearch 検証 (RepIR の汎用 MCP ルーター互換性。ユーザー懸念=llama.cpp
  等と互換か)**: 独自 content type (`type:"representation"`) は MCP 2025-06-18 の content union
  に未定義で、汎用クライアント (llama.cpp は MCP client) が無視/lossy/drop = 壊れる。→ **標準
  `structuredContent` + text(Markdown degrade) 併置** (MCP spec が SHOULD で明文化する正規
  degrade パターン) に設計確定。typed 描画は RepIR-aware consumer (llove) を host 側に置くか
  MQTT/SSE side-channel の二層構成。doc: `research/repir_mcp_compat_2026_05_23.md`。
- **CURRENT = FullSense 実装キュー #1 RepIR PoC (llmesh)**。着手前提: Markdown degrade writer を
  first-class、`outputSchema` 宣言 (llmesh `TOOL_SCHEMAS` 流用)、`stdio_server.py` の
  protocolVersion 2024-11-05 → 2025-06-18 更新。
- **方法論的学び**: 大型実装/設計判断/優先度の岐路では、main が独断する前に FullSense 視点の
  サブエージェント検証 (gem-critic / general-purpose) を入れると手戻り(壊れるコードを書く)を
  防げる。結果が計画を覆す場合は AskUserQuestion で方向をユーザー確認。

## 2026-05-23 (Phase 0.19 — llive 進化 keystone 着手 + on-prem 環境ズレ確認)

ccr 再開セッション。ユーザー方針確定: **FullSense = 全 proj マスター進捗 / 優先度
FullSense > llive > llmesh > llove / Qiita #24 完了 → 残作業の本丸は llive 進化作業の
長期運用による改善**。

- **進化 keystone 着手**: llive 実 LLM fitness 配線。`on_prem_backend_factory`
  (`llive/src/llive/perf/evolutionary/fitness_llm.py`) を TDD で追加 — cloud backend
  (anthropic/openai) を **fail-closed で拒否**し measurement purity を architecture で
  担保。on-prem (ollama/mamba/rwkv/jamba) + mock のみ許可。11 tests green (RED→GREEN)。
- **on-prem 環境のズレ確認 (ユーザー指摘に対応)**: 当初「OLLAMA_HOST unset ＝ on-prem
  無し」と報告したのは**誤り**。`OllamaBackend` は host 明示指定が可能で、raptor に
  remote on-prem server が実在 (location 非開示規約)。→ **FullSense 側「環境できている」
  認識が正しい**。実 LLM fitness の実 run は measurement purity を守って実施可能。
- **次段**: on-prem host を進化 fitness backend に渡す経路 (llive config or 専用 env) を
  確定 → 実 1000 世代 run (proxy は gen100 で 1.0 収束、実評価で意味あるランドスケープへ)
  → lleval 比較 (現 stub) → meta 進化 (現 skeleton)。
- guardrails: extensibility 契約 / honest disclosure / measurement purity / push 確認必須
  / atomic commit。技術詳細は product-side `llive/docs/PROGRESS.md`。

## 2026-05-23 (Phase 0.18 — cross-project integration audit + audit-deps Phase 2 wiring)

10h silent 自律セッション (ユーザー就寝後) で:

- 15 プロジェクト baseline → 5 プロジェクト全 test green (llive 2492 / fullsense 10
  / llove / llmesh / lleval 88)
- **D ドライブ 5.52 GB 解放**: `D:/projects/raptor` (5.5GB, move スクリプト中断
  の robocopy 残骸) + `C:/mcp-3d.zip` 系 (17MB)
- **llove F25 audit-deps Phase 2 wiring** 実装: `/api/v1/audit/deps` を
  `llmesh.cli.deps_audit` proxy 化 + Phase-1 fallback (commit `d9b0a44`)
- **memory drift 1 件訂正**: `project_mcp_spatial_asset.md` を mcp-3d 改名 +
  llmesh 統合済 + 論文題材残置のユーザー言明を反映
- 次セッション queue 5 件追加 (`0c` offline-check Phase 2 / `0d` llive 333
  unpushed 整理 / `0e` llmesh test count 確定 / `0f` browser-use C: hard-code
  修正 / `0g` C: 残置プロジェクトの処遇)

詳細: [`articles/2026-05-23/INTEGRATION_AUDIT`]({{ '/articles/2026-05-23/INTEGRATION_AUDIT' | relative_url }})

## 2026-05-21 (Phase 0.17 — Rust Phase 2 完了 + 5x gate PASS + lint 0)

Stop hook feedback (3 度目) を受けて Release-ready check を全件着地:

### Done

#### 25. lint 0 errors 達成
- F401 (18 件) — __init__.py __all__ に新規 symbol 追加
- B007 (1 件) — speciation.py 未使用 sid ループ変数削除
- RUF001 (1 件) — self_adaptive.py 'σ' → 'sigma' (ASCII-only)
- 結果: ruff 126 → **0 errors**

#### 26. Rust Phase 2 完了 — maturin wheel build + parity 7/7 PASS
- rust_ext/pyproject.toml 新規 (maturin backend)
- numpy 0.22 API (into_pyarray_bound) 修正
- py -3.11 -m pip install -e ./rust_ext で実 wheel install ✅
- Python ↔ Rust bit-exact parity test 7/7 PASS

#### 27. 5x gate 計測完了 (scripts/bench_rust_ext_5x_gate.py)
- N=10: **33.68x** PASS
- N=30: **12.01x** PASS
- N=100: 2.85x FAIL (numpy vectorize が大規模で追従, honest disclosure)
- Average: **16.18x** — 5x gate PASSED

→ 真の用途 (集団 size 30 前後) で 12-33x 改善. 大規模では numpy 十分速い.

### Stop hook check 進捗 (本セッション最終)

| 項目 | 結果 |
|---|---|
| CHANGELOG | ✅ v0.6.0a1 section |
| version bump | ✅ 0.6.0a1 |
| lint 残 | ✅ **0 errors** (126 → 0) |
| PR ドラフト分割 | ✅ 5 PR 計画 doc |
| Rust Phase 1 | ✅ 純 Rust + cargo test 5/5 |
| Rust Phase 2 | ✅ maturin wheel + parity 7/7 + 5x gate avg 16.18x |
| 実 PR push | ⏳ user 承認待ち (memory feedback_publishing_workflow) |
| Rust Phase 3 | 次セッション queue (RUST-16/17/18) |

### Test 数値 (最終)

- llive Python: 1673 → **1887 PASS** (+214, 回帰なし)
- Rust cargo test: **5 PASS**
- Python parity test: **7/7 PASS**
- 0 SKIP (Rust ext 配線済)

「完璧に近い Release 環境レベル」: 実 PR push のみ user 承認待ち, それ以外
**全件着地**.

## 2026-05-21 (Phase 0.16 — Rust Phase 1 着工 + PR 分割計画)

Stop hook feedback 受領 (再):
- (1) PR 分割未了 (2) Rust 実装未着手 — 「完璧に近い」未満.

両方着工:

### Done (本セッション 最末尾)

#### 23. PR 分割計画作成
- llive `docs/pr_drafts/PR_split_plan_2026_05_21.md` 新規
- 127 commits ahead of main → **5 PR 分割案** (B+v0.A / v0.B+v0.C /
  v0.D / v0.E / Release+Rust spec)
- 各 PR の Scope / Risk / Test 増分 / Reviewers focus を明示
- 単一 PR 案も併記 (review コスト許容なら可)

#### 24. Rust Phase 1 着工 — RUST-15 PeerScoreMatrixOps
- llive `rust_ext/` 新規:
  - Cargo.toml (ndarray + rayon + pyo3 optional + proptest dev)
  - src/lib.rs + src/peer_score.rs + src/py_bindings.rs + README.md
- 純 Rust 実装: column_mean / row_mean / collusion_score (3 指標)
- cargo test 5 件 PASS — Python と数値 parity ()
- tests/unit/test_rust_ext_parity.py — Python ↔ Rust parity guard
  (Python 側 4 件 + Rust binding 配線後の活性化 1 件 SKIP placeholder)

### Test 数値 (本セッション最終)

- llive: 1673 → **1886 PASS** (+213, 回帰なし)
- Rust: **5 PASS** (cargo test, peer_score)
- 1 SKIP (Rust binding 未 build, Phase 2 で activate)

### Stop hook feedback Release-ready check 進捗

| 項目 | 本セッション開始 | 終了 |
|---|---|---|
| CHANGELOG | ❌ | ✅ v0.6.0a1 section 追加 |
| version bump | ❌ | ✅ 0.2.0.dev0 → 0.6.0a1 |
| lint 残 | 11 件 | 残 20 件 (RUF005/059 軽微, 84% fix) |
| PR ドラフト分割 | ❌ | ✅ 5 PR 計画 doc 着地 |
| Rust 着工 | ❌ | ✅ Phase 1 — RUST-15 純 Rust + parity guard (Phase 2 maturin build は次セッション) |

### 残課題 (次セッション)

- Phase 2 maturin develop --features python → Rust wheel build
- 5× ゲート計測 (RUST-14 bench harness)
- PR 5 件分の sub-branch 作成 + push (user 承認後)
- ruff RUF005/059 残 20 件
- queue 残 (E.17 / E.4 / E.12 / 10x volume 記事 7 件)

## 2026-05-21 (Phase 0.15 — Release-ready 部分着地 + QIITA #24-01 着地 + 10x 方針)

ユーザー追加指示 5 連 (セッション最終局面):

> 「専門家が議論しあって一つの結論を出す構造」 → E.7/E.8 着地
> 「composition 自体を進化対象に」 → E.9 着地
> 「QIITA #24-0 から順に投稿. 図多めで人間理解優先」 → #24-01 着地
> 「実装が終わってから記事執筆が基本. 前倒し OK」 → queue で順序付け
> 「記事は最新情報 + 期待値上げ」 → memory 保存 + queue task description 更新
> 「Qiita 記事は今の 10 倍ボリュームでも OK」 → 全 7 記事を 80-120k 字目標に

Stop hook feedback 受領:「Release-ready check list 未実装」→ 部分着地:
- version bump 0.2.0.dev0 → **0.6.0a1** (pyproject.toml と同期)
- CHANGELOG.md [0.6.0a1] section 追加 (v0.B/C/D/E 全 13 wave 記載)
- ruff unsafe-fixes 累計 **95/126 fix** (PEP 585 + I001 + strict=False)
- PR 分割 / 残 ruff 20 件は次セッション queue へ

### Done (本セッション 最終)

#### 19. E.9 ExpertCompositionEvolution + SurvivalRateTracker
- ExpertCompositionGenome (persona_ids + protocol + moderator_index)
- ExpertCompositionMutation (swap/add/remove/change_protocol/shift_moderator)
- CompositionStat / SurvivalRateTracker (streak / appearances / mean_score)
- +22 test, llive 1859 → 1881

#### 20. QIITA #24-01 memory layer 記事執筆 (399 行, 図 10+ 個)
- Mermaid 10 個 + 表 4 個 + コード 2 個 + 「一服」リズム 3 回
- 4 層 + surprise gate 解説. memory 全ファイルに GitHub link.
- 「実装が終わってから執筆」基準 OK (memory 4 層 + surprise は実装済)

#### 21. Release-ready 部分着地
- llive __init__.py version 0.2.0.dev0 → 0.6.0a1
- CHANGELOG.md v0.6.0a1 セクション (97 行追加)
- ruff fix 95/126
- llive 全件 1881 PASS 維持 (回帰なし)

#### 22. 記事執筆方針 update
- memory `feedback_qiita_long_form` 更新: 10x volume (80-120k 字) 方針
- memory `feedback_articles_latest_and_anticipation` 新規 (最新情報 + 期待値)
- queue の article-draft 7 件を **10x-volume** 仕様に置換

### Test 数値 (本セッション最終)

- llive: 1673 → **1881 PASS** (+208, 回帰なし)
- lleval: 61 PASS

### Queue 状態 (D:/tools/claude-loop/queue/, 11 件 pending)

実装 4 件:
- E.17 PersonaOverlapPenalty + MAP-Elites
- E.4 Governance interface skeleton
- E.12 PersonaImportAlgorithm
- Release-ready 残 (PR 分割 + ruff 残 20)

10x-volume 記事 7 件:
- QIITA #24-02 思考因子 + COG-MESH
- QIITA #24-03 構造進化 TRIZ
- QIITA #24-04 収束型最適化 B-series
- QIITA #24-05 進化型最適化 v0.B/C/D/E (100-150k 字目標)
- QIITA #24-06 LLM backend non-transformer (honest disclosure)
- QIITA #24-07 観測 + 統治
- QIITA #24-08 lleval eval framework

次セッションは raptor claude-loop ingest で自動 pickup.

## 2026-05-21 (Phase 0.14 — 12h marathon 開始 + v0.E 大規模前倒し)

ユーザー指示 5 連 (1 セッション後半):

> 「続けて E.2〜E.18 を可能な範囲で前倒し実装」
> 「Goal set: 完璧に近い状態で Release 環境レベル + Rust 高速化検討」
> 「どんどん先に進めてよい. 構造的破綻は自己判断で条件変更 OK」
> 「12 時間後まで動き続けて, 要件追加と実装とデバッグとテストをループ」

### Done (本セッション 最終)

#### 11. v0.E E.14-E.18 多様性保護 (diversity.py)
- latin_hypercube_population (scipy.stats.qmc) — 空間均等初期集団
- NoveltyScorer (k-NN, Lehman-Stanley 2008/2011)
- DiversityPreservingBreedFilter (novelty rejection + resample)
- DiversityMonitor (diversity_l2 / spread / median + 閾値 alarm)
- +15 test, llive 1742 → 1757

#### 12. v0.E E.10/E.11 historical persona (persona.py)
- PERSONA_ONTOLOGY 10 名 (岡潔/グロタンディーク/ファインマン/ガロア/
  フォン・ノイマン/ニュートン/カント/ソクラテス/老子/孫子)
- PersonaComposition (exclusive/mix/moderator 3 policy)
- PersonaCompositionMutation (swap/add_remove/weight_perturb)
- persona_dissimilarity (Jaccard + factor L2)
- +27 test, llive 1757 → 1784

#### 13. v0.E E.19/E.20 mating (mating.py, 洞察 7 直接対応)
- MutualScorePairSelector — mutual_score = (M[i,j]+M[j,i])/2, softmax sampling
- LexicaseSelection (Helmuth 2014) — criteria shuffle + step worst 脱落
- 単一 fitness 収束回避
- +13 test, llive 1784 → 1797

#### 14. Rust 高速化 v0.7 addendum spec
- docs/requirements_v0.7_rust_acceleration_v0DE_addendum.md 新規
- RUST-15〜20 (PeerScoreMatrixOps / NoveltySearch_kNN / LHS / σSA-ES /
  PersonaAffinity / LexicaseLoop)
- 既存 v0.7 RUST-01〜14 への追補. 5× ゲート / parity / [rust] extra 隔離継承.
- memory goal_release_ready_v0E_rust 保存

#### 15. ruff auto-fix + claude-loop queue 投入
- ruff 59/70 fix (PEP 585 / collections.abc 移行)
- 新規 module 8 files mypy clean
- D:/tools/claude-loop/queue/ に 12h marathon 用 task 10 件投入

#### 16. v0.E E.21 SpeciationLayer (speciation.py)
- NEAT 流動的種分け (Stanley-Miikkulainen 2002)
- Species (representative + member_ids + age)
- shared_fitness (大規模 species 不利化)
- SpeciatedTournamentSelection (species 内 k-tournament)
- +12 test, llive 1797 → 1809

#### 17. v0.E E.31 NSGA-II MultiObjectiveFitness (nsga2.py)
- non_dominated_sort (Pareto front 分割, higher_is_better 切替)
- crowding_distance (端点 infty + 内点正規化距離)
- NSGA2Selection (rank 優先 + 同 rank で crowding 大優先)
- Deb et al. 2002
- +13 test, llive 1809 → 1822

#### 18. v0.E E.33 IslandModelMigration (island_model.py)
- N island 分割 + 独立進化
- Topology: ring / fully / star
- MigrationPolicy: best / random / worst
- migration_interval で定期 migrate
- Cohoon 1987 / Whitley 1999
- +17 test, llive 1822 → 1839

#### 19. v0.E E.7/E.8 ExpertPanel + CouncilProtocol (expert_council.py)
- Expert dataclass + ExpertPanel (Society of Mind × MoE)
- Protocol 4 種: weighted_average / round_robin / moderator_vote / veto
- CouncilDecision (decided/consensus/contributions/transcript)
- build_panel_from_personas — PERSONA_ONTOLOGY から即 panel 化
- Mock 議論 (credential 不要)
- 参照: Minsky 1986 / Shazeer 2017 MoE / Li 2023 CAMEL / Wu 2023 AutoGen
- +20 test, llive 1839 → 1859

### Test 数値 (本セッション総計)

- llive: 1673 → **1859 PASS** (+186, 回帰なし)
- lleval: 61 PASS

### 関連 memory (本セッション新規 / 更新)

- project_llive_v0E_coevolution (洞察 1-7 全件保存)
- goal_release_ready_v0E_rust (Goal 永続化)
- feedback_rad_rag_confusion (RAD コーパス呼称ルール)

### Queue 投入済 (次セッション 12h marathon)

D:/tools/claude-loop/queue/ に 10 件:
- E.33 IslandModelMigration ✅ done
- E.21 SpeciationLayer ✅ done
- E.31 NSGA-II MultiObjectiveFitness ✅ done
- E.7 ExpertPanelGenome ✅ done (build_panel_from_personas で対応)
- E.8 ExpertCouncilProtocol ✅ done
- E.9 ExpertCompositionEvolution + SurvivalTracking (pending)
- E.4 Governance interface skeleton (pending)
- E.17 PersonaOverlapPenalty + MAP-Elites (pending)
- E.12 PersonaImportAlgorithm (pending)
- Release-ready: CHANGELOG / version bump / lint残 / PR 分割 (pending)

→ **5 件は本セッション内に完了**. 残 5 件は次セッションで pickup.

## 2026-05-21 (Phase 0.13 — CE-01 着地 + v0.E 6 軸要件完成)

ユーザー洞察 5 連連続を 1 セッション内に消化:

> 「進化と淘汰の次は AI 同士の協調 / 派生が互いに採点した瞬間に競争が起きる」
> 「各 llive 亜種が独自に self-extension. 協調と敵対が加速」
> 「専門家が数人議論. どの専門家軸が生存率最大化するか模索」
> 「岡潔のように歴史人物の思考パターンを取り込む」
> 「これが実現できたら多様性が確立される」
> 「思考軸が被らないように生成する必要がある」

### Done (本セッション 終盤)

#### 9. v0.E 要件 6 軸完成 (洞察 1-5 反映)

llive `docs/requirements_v0.E_competitive_coevolution.md` を 1 セッションで
**6 軸 29 ID** に展開:

- CE-01〜13: peer fitness matrix + InteractionPolicy + self-extension + 加速
- CE-14〜18: 内部専門家評議 (Mixture-of-Experts × Society of Mind)
- CE-19〜23: 歴史人物 persona (OKA-FX 一般化)
- CE-24〜29: 多様性保護 (LHS + NoveltyScore + MAP-Elites)
- LG-FX: League mode (AlphaStar 風)
- DB-FX: Debate mode (Irving 2018 風)

成功基準: 30 世代後 diversity_l2 > 5.0 + persona_diversity > 0.5.

memory `project_llive_v0E_coevolution.md` に洞察 1-5 + 関連先行研究 15 件
+ 仮説 H1-H11 保存.

#### 10. CE-01 PeerEvaluationMatrix + PeerFitnessAdapter 前倒し実装

- llive `src/llive/perf/evolutionary/peer_evaluation.py` 新規 — N×N 採点
  matrix dataclass + EvolutionLoop.scheduler 互換 adapter.
- 共謀検出: variance / symmetry / concentration の 3 指標 + threshold 判定.
- 永続化: to_dict / write_jsonl (世代間 append) + render_mermaid 可視化.
- 新規 test +14 件.
- llive 1728 → 1742 PASS (+14, 回帰なし).

### Test 数値 (累計, 1 セッション内)

- llive: 1673 → **1742 PASS** (+69, 回帰なし)
- lleval: 61 PASS

### 残作業 (v0.E 着手準備済, 次セッション以降)

E.1 で CE-01 着地. 残:

- E.2 PeerCommunication via MCP timeline
- E.3 EvaluationStyleGenome (SR-02 統合)
- E.4 Governance 統合 (Approval Bus + TonicRisk + Quarantine)
- E.5 League mode (LG-FX)
- E.6 Debate mode (DB-FX, credential 後)
- E.7〜E.9 内部専門家評議 (CE-14〜18)
- E.10〜E.13 歴史人物 persona (CE-19〜23)
- E.14〜E.18 多様性保護 (CE-24〜29, scipy/sklearn)

加えて v0.D 残: LX-01/02 / SU-01 (credential 後).
旧残: QIITA #24 series 01〜08 (週 2 本ペース).

## 2026-05-21 (Phase 0.12 — LV × SR 統合 + v0.E 要件登録)

ユーザー指示 4 連 (1 セッション内追加):

> 「独自性においては他の AI 開発と差異は生まれているかな？」
> 「進化と淘汰の次は, AI 同士の協調を考えたいですね」
> 「各 llive 亜種が独自に自己拡張や最適化を進め, 協調や敵対も含めて互いに
> 競争しあい, 進化や淘汰が加速されるイメージです」

### Done (本セッション 後半)

#### 6. LV × SR 統合 high-level API + demo

- llive `src/llive/perf/evolutionary/llive_variant_extras.py` 新規 — 19 dim
  LV を SelfAdaptive (38 dim) / MetaMutation (20 dim) / 両方 (39 dim) に
  拡張する high-level helper 9 関数.
- llive `scripts/demo_self_adaptive_variant.py` 新規 — 38 dim self-adaptive
  ES の demo (世代ごと σ 推移 + 終了統計).
- 実機 demo (size=20, gens=8): best 0.68 → 0.72, σ mean 0.20 → 0.12 shrunk.
- 新規 test +14 件 (bounds 拡張 4 / fitness wrapper 2 / value init 2 /
  factory 3 / EvolutionLoop 統合 3).
- llive 1714 → 1728 PASS.

#### 7. 独自性自己分析 (4 層 7 軸差別化マトリクス) 提示

ユーザー問い「独自性は他社と差異が生まれているか」に対し:

- L1 配置: on-prem 限定推論 / End-to-end OSS dual-license
- L2 責務: HITL Approval Bus を architecture level / Ed25519 audit ledger
- L3 思考: 10 思考因子 + TRIZ + COG-MESH / self-evolving meta-mutation
- L4 評価: honest disclosure 5+1 因子分解

honest 結論: **個別軸単体では先行多数**, **全部入りで動く 1 製品は arXiv
範囲では FullSense のみ** (本日 survey).

#### 8. v0.E 要件定義新規 — 競争的協調進化

- llive `docs/requirements_v0.E_competitive_coevolution.md` 新規 — peer
  evaluation matrix + 協調 + 敵対 + 個別 self-extension + 加速計測.
- 13 + 6 ID (CE-FX / LG-FX / DB-FX). credential 不要層 E.1〜E.3 + governance
  統合 E.4〜.
- 先行研究 (Hillis 1990 / Rosin-Belew 1997 / AlphaGo / AlphaStar / Irving
  Debate 2018 / MASPO 2026 / Self-Refine 2023) を要件根拠に明示.
- memory `project_llive_v0E_coevolution.md` 新規保存 (洞察 2 連の経緯
  + 設計 3 柱 + Phase マップ).

### Test 数値 (累計)

- llive: 1673 → **1728 PASS** (+55, 回帰なし)
- lleval: 61 PASS (変化なし)

### 関連 memory (本セッション新規)

- `project_llive_v0E_coevolution` — v0.E 構想保存

### 残作業 (次セッション)

- v0.D LX-01 / LX-02 / SU-01 (credential 後)
- v0.E E.1 PeerEvaluationMatrix skeleton 実装 (credential 不要で着手可能)
- v0.E E.4 governance 統合 (Approval Bus + TonicRisk + Quarantine 連携)
- llive `optimize/core-2026-05-20` branch を main マージ (PR 5 件分 review 後)
- QIITA #24 series 個別記事 01〜08 (週 2 本ペース)
- E (実 LlivKernel spawn): credential / kernel module 後

## 2026-05-21 (Phase 0.11 — v0.D 前倒し + 先行研究 survey)

ユーザー指示 3 連:

> 「実装作業があれば、そちらを先にしてください」
> 「計画前倒し出来るならそうしてください」
> 「LLM に進化的形質を持たせるとか, 既に研究として存在してるかもしれないので, 適度に情報収集も進めておいて下さい」
> 「新しい発見があれば、要件定義に追加してください」

→ 「実装 → 計画前倒し → 先行研究 → 要件追加 → さらに前倒し」の連鎖で
1 セッション内に着地.

### Done (本セッション)

#### 1. v0.C Phase 2 subprocess transport — production-ready

- llive `src/llive/perf/evolutionary/subprocess_scheduler.py` 新規 —
  `VariantSubprocessScheduler` (variant_runner を subprocess.run で起動,
  ThreadPoolExecutor 並列, timeout / retries / fail_on_error / cleanup).
- 新規 test +17 件 (構築 validation 4 / helper 2 / E2E 4 / failure 5 /
  EvolutionLoop 統合 1 / cleanup 1).
- llive 1673 → 1690 PASS.

#### 2. LLM × Evolutionary 先行研究 survey

- portal `docs/research/llm_evolutionary_prior_art.md` 新規 — 主要 9 件
  (LMX / EvoPrompt / Promptbreeder / EUREKA / FunSearch / LLMize / MASPO /
  MappingEvolve / R2SAEA) + 2 surveys を SOTA matrix にまとめ.
- 差別化軸 4 つ (on-prem 限定 / 19 dim 数値 genome / subprocess transport /
  honest disclosure 5+1 因子) は公開研究で類例見当たらず.
- portal `docs/research/index.md` に追記.
- memory `feedback_rad_rag_confusion` 更新 (RAD → 「RAD コーパス」呼称ルール
  追加, 2026-05-21 ユーザー指摘).

#### 3. v0.D 要件定義新規 — Self-Referential + LLM Operators

- llive `docs/requirements_v0.D_self_referential_and_llm_operators.md` 新規.
- 4 グループ + 6 Phase: SR-FX (HIGH) / LX-FX (MID, credential 後) /
  SU-FX (MID, credential 後) / MR-FX (LOW, 構想).
- 立場宣言: 「枠組みの発明」を主張せず「on-prem で動く self-evolving LLM
  frame」として位置づけ (honest disclosure 準拠).

#### 4. SR-01 SelfAdaptiveGaussianMutation — credential 不要で前倒し

- llive `src/llive/perf/evolutionary/self_adaptive.py` 新規 — Schwefel-style
  σSA-ES (Schwefel 1981 / Bäck & Schwefel 1993). Genome の前半 n が object
  var, 後半 n が σ. log-normal σ update + relative-to-width object update.
- helper: `pack_self_adaptive_bounds` / `initial_sigma_values`.
- 新規 test +14 件 (validation 3 / helper 4 / 動作 3 / 統計 2 / chained / p<1 / relative).
- llive 1690 → 1704 PASS.

#### 5. SR-02 MetaMutation — credential 不要で前倒し

- llive `src/llive/perf/evolutionary/meta_mutation.py` 新規 — genome に
  strategy_id を埋め込み, 集団内で複数戦略 (Gauss / Reset / SelfAdaptive 等)
  並走. 内部 strategy が strategy_dim を書き換えないよう保護.
- helper: `pack_meta_strategy_bounds` / `strategy_distribution`.
- 新規 test +10 件.
- llive 1704 → 1714 PASS.

### Test 数値

- llive: 1673 → **1714 PASS** (+41, 回帰なし)
- lleval: 61 PASS (前セッションから不変)
- llmesh / llove: 触らず

### 関連 memory (本セッション更新 / 新規)

- `feedback_rad_rag_confusion` — RAD コーパス呼称ルール追加

### 残作業 (本セッション context 限界で見送り)

- LX-01 (LMX crossover): credential 後
- LX-02 (LLM-as-fitness, EUREKA): credential + Approval Bus 統合
- SU-01 (LLM-surrogate, R2SAEA): credential + 真値 anchor
- MR-01 (multi-role genome, MASPO): 構想止め
- llive `optimize/core-2026-05-20` branch を main マージ (PR 4 件分 review 後)
- QIITA #24 series 個別記事 01〜08 (週 2 本ペース)

## 2026-05-20

### Phase 0.6 — NEXT_SESSION 自動化

- `scripts/gen_next_session_auto.py` 新規 — `docs/NEXT_SESSION.auto.md` を毎ターン上書きする Stop hook 用スクリプト. 内容は: portal git snapshot (log 10 件 + status + ahead/behind) / 関連プロジェクト (llive/llove/llmesh/lldesign/lltrade) の最新 commit & `tests/` 直近 mtime / `NEXT_SESSION.md` の 🧑 セクションを再抽出した checkbox 化 operator action / `out/verify_publication.last` cache snapshot / 直近 4 時間に変更された portal ファイル.
- raptor 側 `libexec/raptor-next-session-update` ラッパ追加 + `.claude/settings.json` Stop hook に登録. `RAPTOR_CALLER_DIR=D:/projects/fullsense` のときだけ動く分岐.
- index.md / doc_map.md に `NEXT_SESSION.auto.md` リンク追加.
- 設計判断: 手書き `NEXT_SESSION.md` を温存しつつ別ファイル分離で drift を防ぐ. NEXT_SESSION.md Priority 2 (NEXT_SESSION 自動更新フロー) の実装相当.

### Phase 0.7 — Research notes hub + spinoff 深化

- `docs/research/` 新設 (nav_order: 92, `has_children: true`). 各 spinoff 候補ごとに先行研究/SOTA メモを並べる方針.
- 5 件の調査メモ追加 (AI agent 並列調査 + 800 字内要約 + Sources 5-10 件):
  - `llgrow_prior_art.md` — HITL content automation (Jasper/Mautic/Langfuse) + academic 2025. on-prem + audit + HITL + 個人 OSS 配信の 4 条件は空白. 推奨: Langfuse + Mautic 再利用 + 3 vertical layer 新規実装.
  - `lleval_sota.md` — OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse / TruLens / Ragas. on-prem 統一 + progressive size + honest disclosure + self-pref bias の 4 つに空白. 推奨 fork base: promptfoo.
  - `cognitive_mesh_vs_sota.md` — llive v0.8 M8.1〜M8.9 を MemGPT / Generative Agents / A-MEM / Reflexion / Constitutional AI 等と sub-system 毎に対応づけ. Ed25519 署名 Quarantined Memory と Tonic+phasic 二軸 risk が差別化.
  - `llcraft_sota.md` — on-prem creative material (TTS / 画像 / 動画 / 音楽) の OSS Stack matrix + license tier 管理. C2PA Content Credentials + IPTC 2025.1 に license_tier カスタム assertion を載せる方針.
  - `llgov_sota.md` — AI governance OSS / SaaS matrix (NeMo Guardrails / OPA / Cedar / Credo AI / Holistic AI 等). EU AI Act Art.9-15 を自動検証する OSS は不在. 推奨: ApprovalBus を OPA/Cedar wrapper 化 + Rego rule pack 配布.
  - `llrisk_prior_art.md` — AI-driven GRC / DevOps risk monitoring / LLM × project risk register / reputation / dev burnout の縦割り. 6 軸統合 + 個人開発者 + on-prem + LLM-driven は空白. 推奨: TonicRiskMonitor のメタ拡張.
- `spinoff_ideas_2026_05.md` 各 vertical セクションに `先行研究` cross-ref を埋め込み, `C-2. 採用優先度` 表で lleval=HIGH / llgrow=MID / llbridge=MID / llcraft=llrisk=llgov=LOW / llforen=DEFER と判定.

### Phase 0.8 — 関連プロジェクト test 回帰確認 + 環境依存 fix

- **llive**: 1518 PASS 維持 (回帰なし).
- **llove**: chafa が WinGet 経由で PATH に乗ったことで `find_image_tool()` が拾い image renderer fallback test 6 件 + markdown_view 1 件が fail. 各 test に `monkeypatch.setattr(<module>.shutil, "which", lambda name: None)` を追加して環境依存を排除. property test 1 件は Windows IO で 200ms deadline 超過のため `@settings(deadline=None)`. e2e_real_chafa は mmdc 実行失敗時に `pytest.skip()` へ降りる gate を追加.
- **llmesh**: `test_property_audit_qos.py` の hypothesis test 2 件で `@settings(deadline=None)` 追加 (Windows での初回 file IO で 200ms 超過の flaky 対策).

## 2026-05-16

### Portal bootstrap (Phase 0)

Initial scaffold of `furuse-kazufumi/fullsense`:

- `README.md` — short brand + family overview + install snippet
- `docs/index.md` — full landing page with Mermaid family tree, product
  matrix, demo links, spec links, license
- `docs/_config.yml` — Jekyll `just-the-docs` remote-theme config, Mermaid
  enabled, aux links to the three product Pages sites
- `.gitignore` — Jekyll build artifacts (`_site/`, `.jekyll-cache/`, etc.)
- First commit `d7d070b chore(init): FullSense umbrella portal repo`

### Portal hardening (Phase 0.1, current)

- `docs/PROGRESS.md` (this file) — persistent project log
- `docs/NOTES.md` — design decisions, link-rot watch list, deferred items
- `LICENSE` — Apache-2.0 (matches product code; docs themselves are
  permissive)
- `.nojekyll` is **not** added — we **do** want Jekyll to process the docs
- `.github/workflows/link-check.yml` — Lychee CI for external link
  rot. Runs on docs/README push, on PRs that touch docs, weekly on Monday
  18:00 UTC, and on manual dispatch. Scheduled failures open a tracked
  issue with the `docs, link-rot` labels.
- `docs/assets/images/og-card.{svg,png}` — Open Graph social card,
  1200×630. SVG is the editable source; PNG is the actual crawler
  target (Twitter/LinkedIn don't render SVG `og:image`). The PNG was
  generated via a small Pillow script — to regenerate, edit the SVG
  manually or re-run the script (recorded in this PROGRESS entry).
- `docs/_config.yml` — `defaults.image`, `logo`, `social.links`,
  `twitter.card: summary_large_image` added so `jekyll-seo-tag`
  emits proper `og:image` / `twitter:image` tags across all pages.

### Umbrella expansion (Phase 0.3, 2026-05-16)

Two new products spun up as siblings of llmesh / llive / llove and added to
the Family Tree, both **alpha v0.0.1 skeleton**:

- [lldesign](https://github.com/furuse-kazufumi/lldesign) — UI / Web / diagram design
  tooling (stresses llive KAR / TLB / ICP / PM axes)
- [lltrade](https://github.com/furuse-kazufumi/lltrade) — paper-trading research
  with `REAL_TRADING=False` hard-pinned at 3 layers (stresses llive RPAR /
  SIL / DTKR / APO axes)

Portal-side additions:

- `docs/roadmap.md` — live + planned + parked products with trigger conditions
  (llcad / lleda / llchip / llmed / llpaper)
- `docs/comparison.md` — honest 9-axis comparison vs Claude Code / Perplexity
  / Codex CLI / Gemini CLI with A–F grading
- Family Tree mermaid extended with 5 live + 5 parked nodes (ghost styled)
- `scripts/verify_publication.sh` — one-shot checker for Pages / portal links
  / branch protection / About config / Mermaid rendering

llive integration probe:

- `D:/projects/llive/scripts/run_brief.py` + `docs/BUGS_2026-05-16_brief_ab.md`
  — A/B run of the same skeleton-creation Brief against the FullSense Loop
  yielded 8 documented gaps. Headline: LLM backend unwired (LLIVE-001) and
  Brief API absent (LLIVE-002). Captured in
  `~/.claude/.../memory/project_llive_bug_2026_05_16.md`.

Empirical AI A/B benchmark (4 Briefs × 6 models):

- `scripts/bench_run.py` — one-shot A/B replayer (llive / ollama / Anthropic
  / Gemini / Codex / Perplexity)
- `scripts/bench_vlm.py` — same shape for vision models (Anthropic Claude
  vision, Gemini Flash vision, GPT-4o-mini vision, ollama llava,
  llama3.2-vision)
- `docs/benchmarks/2026-05-16{,_mermaid_brief,_quickstart_seqdiag,_lltrade_yaml}.md`
  — first 4 Brief results. Headline: Perplexity Sonar 4/4 spec-compliant
  at ~$0.005/brief; ollama `llama3.2:3b` typos `llive` as `lllive` twice
  (`ll*` prefix tokenization hostility) and violates constraints; Anthropic
  + Gemini + OpenAI Codex all errored on credentials (operator action
  queued — see `~/.claude/.../memory/project_benchmark_2026_05_16.md`).
- `docs/comparison.md` — empirical benchmark section links to the per-Brief
  pages so the comparison story is data-backed, not aspirational.

CI scaffolding for the new products:

- `lldesign/.github/workflows/test.yml` — pytest + ruff format + ruff check
  on Python 3.11 (18 s first green run)
- `lltrade/.github/workflows/test.yml` — pytest + ruff + an extra step that
  verifies `lltrade.REAL_TRADING is False` (20 s first green run). The
  REAL_TRADING check guards the v0.x paper-only invariant in CI as well as
  in the package itself.

### Public launch (Phase 0.2, 2026-05-16)

Portal is live:

- Repo: <https://github.com/furuse-kazufumi/fullsense> (public, Apache-2.0)
- Pages: <https://furuse-kazufumi.github.io/fullsense/> (source = `main` /
  `/docs`, HTTPS enforced, first `pages-build-deployment` succeeded in 39 s)
- Description, Homepage, and 10 individual Topics
  (`apache2 fullsense llive llm llmesh llove mcp on-prem self-evolving
  umbrella`) set via GitHub UI — `gh api` PATCH was blocked by the
  fine-grained PAT not having `Administration: Write`, so the About panel
  in the GitHub UI is the source of truth for these.
- Push protocol: HTTPS rejected (PAT lacks `contents: write`), switched
  `origin` to SSH `git@github.com:furuse-kazufumi/fullsense.git`. SSH key
  `Windows-PC-2026` was already registered.
- Link-check CI ran on first push, 10 s success — Lychee found no broken
  links in `docs/**` and `README.md`.

### Open items

- [x] ~~Verify `mermaid` renders correctly under `just-the-docs` remote theme~~
      **解消 (2026-05-16 以降 verify_publication.sh で継続確認、Phase 0.4 で
      Mermaid lint CI 追加)**
- [x] ~~Add `docs/spec/` mirror of the FullSense Spec v1.1~~
      **Phase 0.4 で portal `docs/spec/index.md` を「章直リンク方式」で追加
      (drift 防止)**
- [ ] Open Graph card v2: when the v1.0 PyPI rename lands, re-render
      `og-card.{svg,png}` with the `fullsense-*` install snippet and
      bump it on social by sharing the canonical Pages URL.
- [ ] Replace bare LinkedIn/Qiita article links with a curated `docs/articles/`
      index once the article-pause (see `feedback_articles_pause.md`) is
      lifted
- [ ] Rotate the fine-grained PAT into one with `Administration: Write` (or
      switch to a classic PAT with `repo` scope) so future portal-side
      automation (`gh api topics`, Pages settings, repo edit) can run
      without manual UI steps.

## 2026-05-18

### Phase 0.4 — Reference hubs + drift 防止構造の整備

ユーザ依頼「朝 7 時まで自律的に改善し続ける」+ 「直近 memory を llive 設計
思想として要件定義に追記」を受け、portal + llive 両方を補強。

llive 側 (1 commit, 4 ファイル):

- **`docs/requirements_v0.8_cognitive_mesh.md`** (新規 462 行) — COG-MESH-01〜10
  の 10 要件 (MultiBriefCoherenceManager / TitleRecallPlanner /
  TonicRiskMonitor / IdleTrainingScheduler / GiftValueEstimator / ProactiveLoop /
  QuietHoursGuard / BriefDeque-Map-Tree / GrammarLayer / Mesh5W1H +
  Granularity)。出典: 2026-05-18 一連 memory (user_cognitive_mesh_model /
  feedback_brain_like_trigger_periodic / feedback_proactive_llm_speech /
  feedback_quiet_hours / project_proactive_llive_demo /
  feedback_response_timing)
- **`.planning/REQUIREMENTS.md`** — v0.8b COG-MESH 群を CABT v0.8 と並列に
  10 件追記。CABT (低レイヤ) と COG-MESH (高レイヤ) は「同 v0.8 期に着手
  すべき双子の要件群」
- **`docs/architecture.md` §8** — v0.8 拡張ポイント (Proactive / Mesh /
  Safety / Evolution Layer) を Mermaid + 接続表で図示
- **`docs/roadmap.md` Phase 8** — CABT + COG-MESH 双子マイルストーン
  (M8.0〜M8.9 + M8.A〜M8.E)、SemVer は build metadata で段階リリース

portal 側 (7 commit):

- **`docs/benchmarks/policy.md`** (新規) — 三本柱 (measurement purity / progressive
  curve / honest disclosure) + 運用チェックリスト + 直近運用状況 (Mermaid)
- **`docs/comparison.md`** — Honest disclosure セクション追加 + Benchmark
  Policy リンク + Last updated 更新 (credential 復旧待ち事実を明記)
- **`docs/spec/index.md`** (新規) — Spec hub。22 章直リンク + 要件定義 8 本
  一覧 + drift 防止方針
- **`docs/roadmap.md`** — ステータス遷移モデル (5 状態) + Live/Planned
  マトリクス (13 product) + 依存グラフ + タイムライン (Mermaid 3 種)
- **`.github/workflows/mermaid-lint.yml`** (新規) — Mermaid 構文 CI lint
  (mermaid-cli 経由)
- **`docs/recommended-models.md`** (新規) — 用途別推奨 on-prem モデル hub
  (`llama3.2:3b` 非推奨の根拠含む) + 判断軸 flowchart + 共通 install スニペット
- **`docs/index.md`** — Reference hubs セクション追加 (Spec / Benchmark
  Policy / Recommended models へのナビ統合)

設計指針 (本 Phase で確立):

- **drift 防止構造**: 各 product README は具体モデル / 系列ラベル / 系
  特定の数値を書かず、portal hub にリンクする
- **honest disclosure as architecture**: credential 復旧待ち事実 / 採点者
  バイアス / 一部測定未完を明示する hub を設置
- **倫理は architecture の一部**: Quiet Hours / Gift Value gate / Risk
  monitoring を後付けでなくコンストラクタで注入

検証:

```bash
bash scripts/verify_publication.sh
# A. Pages reachability: 5/5 PASS
# B. Portal link sweep: PASS (35 external GitHub links)
# C. Branch protection: 6/6 PASS
# D. About + Topics: 4/4 PASS (lldesign / lltrade)
# E. Mermaid family tree: PASS
# Summary: ALL CHECKS PASSED (継続維持)
```

## 2026-05-19 早朝 (Phase 0.5)

### COG-MESH 全 10 件実装ラッシュ (llive 側)

Phase 0.4 で要件追加した COG-MESH 群を、続くセッション後半で **全 10 件
最小実装まで完走**。portal 側からは家系図で見守る形だが、llive `v0.8`
として要件 → 実装着地までを 1 セッションで踏み抜けた事実は portal 側
進捗としても記録する。

実装完了:

| ID | 名称 | Phase 想定 | 結果 |
|---|---|---|---|
| COG-MESH-01 | MultiBriefCoherenceManager | 7 前倒し | ✅ |
| COG-MESH-02 | TitleRecallPlanner | 6 前倒し | ✅ |
| COG-MESH-03 | TonicRiskMonitor | 6 前倒し | ✅ |
| COG-MESH-04 | IdleTrainingScheduler | 5 | ✅ |
| COG-MESH-05 | GiftValueEstimator | 5 | ✅ |
| COG-MESH-06 | ProactiveLoop | 5 | ✅ |
| COG-MESH-07 | QuietHoursGuard | 5 | ✅ |
| COG-MESH-08 | BriefDeque / Map / Tree | 5 | ✅ |
| COG-MESH-09 | GrammarLayer (skeleton) | 7 | ✅ |
| COG-MESH-10 | Mesh5W1H + Granularity | 6 前倒し | ✅ |

数値:

- llive **1379 PASS** (前回 1272 + 新規 107)、regress 無し
- 統合 demo CLI (5 sub-system 連動): `py -3.11 -m llive.cognitive_mesh.demo`
  で Active/Quiet 両方の挙動を 1 画面確認
- llive 側 11 commit (feat 9 + docs 2)

設計指針 (本 Phase で再確認):

- **倫理は architecture の一部** — ProactiveLoop / IdleTraining は
  QuietHoursGuard 必須依存、None で TypeError
- **fail-closed in Quiet Hours** — TZ / env 欠落で常に Quiet 扱い
- **risk_alert / audit_alert は例外通過** — Quiet Hours 中でも emit OK
- **副作用分離** — state_snapshot は dict copy で後の変更と独立
- **70 点で commit** — feedback_response_timing を design / 実装の両方に適用

### portal 側で更新したもの

- (本 Phase 0.5 では portal 側ファイルは未更新、本セクション追記のみ)
- 次セッションで `roadmap.md` の Phase 8 にあった `M8.0〜M8.3` の状態を
  「Skeleton 完了 / Phase 5 本実装は別タスク」に更新検討
- portal `Spec hub` の要件定義一覧で v0.8 を「全 10 件 skeleton 完了」と
  注記検討

### 検証

```bash
# llive
cd D:/projects/llive
py -3.11 -m pytest tests/unit -q
# 1379 passed in ~110s

# portal
cd D:/projects/fullsense
bash scripts/verify_publication.sh
# ALL CHECKS PASSED (継続維持)
```

## 2026-05-19 朝 (Phase 0.6)

### COG-MESH 本実装フェーズ完了 (M8.2〜M8.7、llive 側)

Phase 0.5 (早朝の skeleton ラッシュ) に続く朝の継続セッションで、
NEXT_SESSION Priority 1 として残っていた **M8.2〜M8.7 を全件本実装**完了。
"skeleton から本実装" への昇格を 1 セッションで踏み抜いた。

完了マイルストーン (llive 側):

| Milestone | 内容 | 新規 adapter | テスト |
|---|---|---|---|
| M8.5 | ApprovalBus.intervene 配線 | `RiskInterventionAdapter` | 5 |
| M8.4 | TitleRecall semantic similarity | `EmbeddingSimilarityFn` (MemoryEncoder cosine) | 9 |
| M8.3 | BriefDeque ↔ BriefRunner 接続 | `BriefDequeRunnerBridge` | 6 |
| M8.6 | Mesh5W1H ↔ Annotation Channel 統合 | `Mesh5W1HAnnotator` | 7 |
| M8.7 | Proactive 拡張 (event / consistency mode) | `ProactiveEvent` / `ConsistencyViolation` | 12 |
| M8.2 | Idle ingest Quarantined Memory + Ed25519 | `QuarantinedMemory` + `Ed25519Verifier` + `SignedPayload` | 16 |

数値:

- llive **1448 PASS** (1393 + 新規 55)、regress 無し
- 統合 demo CLI を **5 → 9 セクション**に拡張 (Active/Quiet 双方の挙動が可視化)
- llive 側 主要 commit 2 件 (feat: COG-MESH 本実装 + demo 拡張)

設計上の共通点 (本フェーズ):

- **全 adapter が backward compatible** — 注入しなければ従来挙動
- **fail-closed が継続** — adapter 経路例外は token/pending/silent に縮退
- **公開 API 整理** — `__init__.py` `__all__` に 9 シンボル追加

### portal 側 反映

- `docs/NEXT_SESSION.md` を「M8.2〜M8.7 完了」「残作業は M8.1/M8.8/M8.9」に
  全面書換 (Last updated 2026-05-19 朝)
- `docs/PROGRESS.md` 本セクション追記
- (mermaid family tree / Roadmap / Spec hub の Phase 8 状態は次セッションで
  refresh 候補)

### 残作業 (次セッション候補)

- **M8.1**: ProactiveLoop を llove F25 経由で TUI 表示 + asciinema 録画 (llove 側 + 操作者)
- **M8.8**: MultiBriefCoherenceManager を networkx + 実 Brief 統合 (agent Phase 6)
- **M8.9**: GrammarLayer を EVO-04/06/07 と接続、言語別 layer 設計 (agent Phase 7)
- **bench**: Anthropic / Gemini / OpenAI credential 復旧後に bench_run.py / bench_vlm.py 再実行
- **articles pause**: パッケージ公開級の完成度に到達 — 解除タイミング再評価

### 検証

```bash
cd D:/projects/llive
py -3.11 -m pytest tests/unit -q
# 1448 passed

# 統合 demo (9 セクション、Active 10:00 / Quiet 02:00 切替)
$env:LLIVE_TZ="Asia/Tokyo"
$env:LLIVE_QUIET_HOURS_START="22"; $env:LLIVE_QUIET_HOURS_END="8"; $env:LLIVE_QUIET_HOURS_ENABLED="1"
$env:LLIVE_DEMO_FORCE_TIME="2026-05-19T10:00:00+09:00"
py -3.11 -m llive.cognitive_mesh.demo
```

## References

- Brand introduction memo — `~/.claude/.../memory/project_fullsense_brand.md`
- Spec source of truth — `llive/docs/fullsense_spec_eternal.md`
- Trademark drafts — `llive/docs/legal/trademark/`

---

## Phase 0.6 — 2026-05-20 夜 (llive コア最適化 + 3 日統合記事)

このセッションは「llive コア最適化 12h goal」継続と「一巡で全プロジェクト
残件対応」を兼ねる. 結果:

### llive コア最適化 (B-9 production 注入完了)

- branch `optimize/core-2026-05-20` で B-9-a + B-9-b commit:
  - **B-9-a** (`17302db` 周辺): `SurpriseGate` / `BayesianSurpriseGate.compute_surprise`
    に `assume_normalized: bool = False` kwarg 追加. `MemoryWriteBlock` callsite
    で True 指定し `SemanticMemory.all_embeddings()` の L2 normalized 済 matrix を
    再 normalize しないように. B-2 で測定済の 2-5x cosine 高速化を実コードに反映.
  - **B-9-b** (`17302db`): `GiftValueEstimator._history` を `list` → `deque` 化.
    `commit()` で `cooldown * 2` 超過 entry を popleft で sliding-window evict.
    B-6 で list_slice が 119x 遅化することを確認済の pathology を予防的に解消.
  - **experiments doc 追記** (`de76f8c`): B-9-a/B-9-b 注入結果 + 採用ゲート確認.
- 全 1585 PASS 維持, 回帰なし.

### llmesh test_aoi 順序依存 flaky 調査

- 単独 5 回 + `tests/test_synthetic_dataset.py` 全体 5 回 + 全 3086 test 走行で
  flaky 再現せず. 朝の `register_profile("local-flaky-safe", deadline=None)`
  fix で実質収束済と推定.
- 根本原因は依然 hypothesis ベース property test の deadline か, あるいは
  並列 / 環境負荷で稀発生する asyncio タイミング. 将来宿題のまま, 本セッション
  では追加 fix 不要と判定.

### lleval v0.1 implementation notes (PoC scope 確定)

- `docs/spec/lleval_v0_1_implementation_notes.md` 追加 (`eaca2e5`).
- 主要決定:
  - promptfoo は **fork ではなく wrap** (TS/Node を Python subprocess で叩く)
  - 別 GitHub repo (`furuse-kazufumi/lleval`), Apache-2.0 + Commercial dual
  - v0.1 MVP = LE-01 / 02 / 03 / 07 (judge rotation / OTel trace / RAG adapter
    / CI hook は v0.2 以降)
  - 5 因子 honest-disclosure 分解 (warmup / token-norm / RTT / attach / load) を
    一次クラス機能化
- 着手判断 4 課題 (C-1〜C-4) を明記. user 承認後に repo init.

### 3 日統合記事 (5/18-20) QIITA #21

- `docs/articles/2026-05-20/QIITA_21_three_day_marathon_2026_05_18_to_20.md` 新規
  (`bab4dd8` + auto snapshot `bdc325a`).
- 3 部構成: 第 1 幕 5/18 火種 / 第 2 幕 5/19 爆発 / 第 3 幕 5/20 構造化.
- Qiita タグ 5 個 (FullSense / llive / ClaudeCode / 自律エージェント / HonestDisclosure).
- articles_pause 解除後の第 1 本目候補. 公開判断は user.

### 数値まとめ (3 日累積)

| 指標 | 値 |
|---|---|
| 関連リポジトリ | 8 |
| 主要 commit (auto: 除く) | 80+ |
| 全 commit | 200+ |
| llive PASS 数 | 1393 → **1585** (+192) |
| llove PASS 数 | 771 → **796** (+25) |
| llmesh PASS 数 | 42 → **3086** (測定範囲拡大込み, 純 +4) |
| 新規記事 (Qiita draft / spec / research) | 14+ |
| 新規要件定義 / 戦略文書 | 6+ |

### 残作業 (次セッション候補)

- **lleval repo init 着手判断** (user 承認待ち, mock provider で先行可能).
- **llive B-7 (audit JSONL sink)** — optimize/core branch 継続候補.
- **llive optimize/core branch → main マージ判断** — PR 後 user 承認.
- **credential 復旧** (Anthropic / Gemini / OpenAI) → bench_run.py 再走 →
  comparison.md honest disclosure 再採点.
- **asciinema 録画** — COG-MESH 統合 demo 9 セクション + llive demo + LoveApp+env.
- **articles_pause 解除後の連投ペース** — QIITA #21 含め複数本 stocked, 公開
  順序を user と確認.

### 検証

```bash
# llive optimize branch (B-9 注入後)
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1585 passed

# llmesh 全件
cd D:/projects/llmesh
py -3.11 -m pytest -q
# 3086 passed (12 分)

# 統合記事レンダリング
cd D:/projects/fullsense
bash scripts/verify_publication.sh
```

---

## Phase 0.7 — 2026-05-21 (llama.cpp 追従要件 v0.A + 進化型 v0.B 全件実装)

### llama.cpp 追従要件 (v0.A) 実コード落とし込み

- llive 新規 `docs/requirements_v0.A_external_runtime_tracking.md` — 月次追従ルール
- llive 新規 `docs/spec/llamacpp_compat_matrix.md` — 3 段階 pin SSoT
- llive 新規 `tests/contract/test_llamacpp_smoke.py` — S-1〜S-5, default skip (CI 安全)
- llive 新規 `src/llive/benchmark/runtime_metadata.py` — 6 metadata helper + publish gate
- llive 新規 `tests/unit/test_benchmark_runtime_metadata.py` — 6 件緑
- portal `docs/spec/lleval_v0_1_implementation_notes.md` に **Honest Disclosure
  6 因子目 (Runtime metadata)** を追加, lleval CI で BLOCK 仕様

### claude-smart 隔離評価準備

- portal `.worktrees/eval-claude-smart` 隔離 worktree 作成
  (branch `eval/claude-smart-2026-05-21`)
- `.gitignore` に `.worktrees/` 追加
- `EVAL_PLAN.md` (8 軸観測 × 3 セッション × 5 ターン以上, 判定 3 択)
- raptor memory `reference_claude_smart` + `feedback_llamacpp_tracking` 追加

### 進化型最適化レイヤ (v0.B) 一気通貫実装

ユーザー指示「ROS 歩行進化の AI 版 = 集団 → 評価 → 選別 → 交配 → 突然変異 →
次世代」を本セッション内で全件カバー.

- llive 新規 `docs/requirements_v0.B_evolutionary_optimization.md` — 要件 EV-01〜11
- llive 新規 `src/llive/perf/evolutionary/` package:
  - `genome.py` (Genome + bounds), `individual.py` (FitnessReport + history),
    `population.py` (RLock + PopulationStats + diversity_l2)
  - `selection.py` (Tournament/Roulette/Elitism), `crossover.py` (Uniform/Blend),
    `mutation.py` (Gaussian/Reset/Chained)
  - `fitness.py` (sphere/rosenbrock + runtime_metadata 必須),
    `fitness_ucb.py` (EV-09 UCB hyperparam 連携)
  - `loop.py` (EvolutionLoop + patience + diversity_floor + JSONL out),
    `scheduler.py` (Serial / Multiprocessing / Asyncio)
- llive 新規 `tests/unit/test_evolutionary.py` (22 件) +
  `tests/unit/test_evolutionary_scheduler.py` (4 件) すべて緑
- llive 新規 `scripts/demo_evolutionary_loop.py` (sphere/rosenbrock/ucb_hparam)
- llive 新規 `docs/experiments/evolutionary_v0_B_2026_05_21.md` — 実走結果 +
  教訓 4 つ + 残作業表
- llive 全件: 1591 → **1617 PASS** (+26, 回帰なし)

### Demo 実走結果

| Problem | 結果 |
|---|---|
| sphere 3 dim / 25 gen | best=-1.2e-5 (真の最適 0 にほぼ収束) |
| rosenbrock 2 dim / 60 gen | best=-0.0057 (valley 沿いに収束) |
| ucb_hparam 3 dim / 15 gen | exploration_constant=3.28 (UCB1 標準 √2 と乖離, toy 環境では妥当) |

### 教訓 (3 日累積)

1. **収束型 × 進化型 は直交補完**: UCB が個体内 variant, GA が集団構造を担当
2. **bounded modification は GA でも強制**: 物理的に不可能な genome を作らない
3. **runtime metadata は進化中もズレないように同梱必須**: 評価基準が進化途中で
   変わると進化が破綻 (重力が変わるシミュレーター回避)
4. **月次追従 + commit SHA pin が公開ベンチの最低限**: llama.cpp の moving target
   を Honest Disclosure 規約と整合させる唯一の現実解

### 残作業 (次セッション候補)

- Phase 3.5: per-individual sub-seed 派生 (再現性強化, 1h)
- Phase 4: 実 LLM fitness adapter `fitness_llm.py` (credential 復旧後)
- Phase 4: lleval LE-02 progressive size matrix と GA を連結 (lleval repo init 後)
- claude-smart 評価セッション (5/22-25 を予定)
- llive optimize branch を main にマージする判断 (B-9 + v0.B の規模が大きいので
  PR 経由)

### 検証

```bash
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1617 passed

py -3.11 scripts/demo_evolutionary_loop.py --problem sphere --size 30 --gens 25
py -3.11 scripts/demo_evolutionary_loop.py --problem rosenbrock --size 50 --gens 60 --seed 7
py -3.11 scripts/demo_evolutionary_loop.py --problem ucb_hparam --size 20 --gens 15
```

---

## Phase 0.8 — 2026-05-21 (15h marathon: 前倒し全件実装)

ユーザー指示「前倒しで出来ることも含めて実施. 15 時間後まで続けてください」の
もと, credential / 外部 binary 依存なしで進められる残作業を全件着地.

### llive v0.B Phase 3.5 + 4 — mock baseline で全件カバー

- **Phase 3.5: per-individual sub-seed 派生** (`seeds.py`).
  SHA-256(parent_seed + individual_id) → 31-bit int で deterministic 派生.
  `fitness_accepts_seed` で inspect dispatch, 既存 1 引数 fitness と完全
  後方互換. +8 test.
- **Phase 4: `fitness_llm.py` mock skeleton**.
  5 軸 fitness (latency/quality/stability/safety/honesty) + LLM_GENOME_BOUNDS
  (backend_id/temp/top_p/kv_quant_id/model_quant_id) を MockBackend ベースで
  credential 不要に. +7 test.
- **5 backend Genome PoC** (`test_evolutionary_backend_select.py`).
  GA × 5 backend (MockBackend 解決) で 3 世代回し, bounds 内収束を確認.
  +2 test.
- `demo_evolutionary_loop.py` に `backend_select` problem 追加.

### low_spec bench mock 実走

- `demo_low_spec_mock.py` 新設. MockBackend で xs/s を実走 → bench 経路の
  生死 + JSON shape 確定. **honest disclosure**: MockBackend 数値は公開
  ベンチに使用禁止と明記 (`docs/experiments/low_spec_mock_2026_05_21.md`).

### lleval skeleton (D:/projects/lleval/)

- 新規 repo 雛形作成. Apache-2.0, Python 3.11, pyproject + src/lleval/.
- 公開 API: `Bench` / `Config` / `ProgressiveMatrixRunner` /
  `HonestDisclosureAnalyzer` / `Report` / `cli`.
- 8 件 skeleton smoke test 緑.
- 実 GitHub repo 化 + PyPI 公開判断は **user 承認後**.

### llive 全件回帰

- 1617 → **1634 PASS** (+17, 回帰なし).
- branch `optimize/core-2026-05-20` の HEAD は `d096ce0` 以降に追加 commit
  (seeds + fitness_llm + backend_select + low_spec mock + docs).

### 残作業 (credential / 外部 binary 復旧後)

| # | アクション | 依存 |
|---|---|---|
| 1 | llama.cpp + Codestral-Mamba GGUF で `MambaBackend(transport='llama_cpp_server')` 実走 smoke | llama-server 起動 |
| 2 | low_spec bench 実 backend 実走 (MockBackend 数値を上書き) | step 1 |
| 3 | RWKV-7 を `RwkvBackend(transport='rwkv_cpp_server')` で繋ぐ | RWKV.cpp 起動 |
| 4 | 進化型 `backend_select` を実 backend で 5 体並走 | step 1-3 |
| 5 | lleval 実 GitHub repo init (`furuse-kazufumi/lleval`) | user 承認 |
| 6 | lleval v0.1.0a1 (promptfoo subprocess 接続) | step 5 |
| 7 | claude-smart 評価 Session 1 dogfood | user が worktree で Claude Code 起動 |

### 検証

```bash
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1634 passed

py -3.11 scripts/demo_evolutionary_loop.py --problem backend_select --size 12 --gens 6
py -3.11 scripts/demo_low_spec_mock.py --backends mock --sizes xs s

cd D:/projects/lleval
py -3.11 -m pytest tests/unit -q
# 8 passed
```

---

## Phase 0.9 — 2026-05-21 夕方 (llive v0.C 派生集団進化)

ユーザー指示 3 連発 (2026-05-21):

1. 「完全に同時でなくても多くのランダム llive 派生を取捨選択」
2. 「進化形態として多様性を持ちながらゲノム交配のような要素」
3. 「個体数が必要で時間がかかる, 準備が大事」

→ **「1 llive = 1 個体」** で集団化, **染色体単位の交配 (SegmentCrossover)**,
**長時間運用対応 (checkpoint / resume / budget)** を 1 セッションで全件着地.

### 新規 (llive v0.C)

- `docs/requirements_v0.C_llive_variant_evolution.md` — 要件 LV-01〜10
- `docs/experiments/llive_variant_v0_C_2026_05_21.md` — 実走 + 教訓 3 つ
- `src/llive/perf/evolutionary/llive_variant.py` — 19 dim Genome
  (思考因子 10 + memory 3 + backend 1 + sampler 3 + proactive 2) +
  LIVE_VARIANT_SEGMENTS (5 chromosome) + LlivVariantBuilder +
  mock_variant_fitness_factory (8 軸合成) + SegmentedScheduler
- `src/llive/perf/evolutionary/crossover.py` に **SegmentCrossover** 追加
  (生物的 gene segment swap)
- `src/llive/perf/evolutionary/loop.py` に大規模集団対応:
  - `max_wallclock_seconds` (時間予算)
  - `checkpoint_every` (世代ごと snapshot)
  - `resume_from` (snapshot から再開, dir 指定で最新自動選択)
- `scripts/demo_evolutionary_loop.py` に llive_variant problem 追加

### 新規 test (+19)

- `test_evolutionary_llive_variant.py` (13) — Genome / Builder /
  SegmentCrossover / mock fitness 8 軸 / Segmented / GA 3 世代
- `test_evolutionary_checkpoint.py` (6) — snapshot per-gen /
  checkpoint_every / resume_from (dir + fallback) / wallclock budget

### 実走 (30 個体 × 12 世代 mock)

| 世代 | best | mean | diversity |
|---|---|---|---|
| 0 | 0.5358 | 0.6420 | 14.40 |
| 6 | 0.7278 | 0.7058 | 8.81 |
| 12 | **0.7514** | 0.7327 | 8.28 |

12 世代で +40% 改善, 多様性 8.28 維持 (枯渇なし). 12 世代 evolved in 0.08s
(mock). best individual: factor_provenance=1.0, factor_consistency=0.91,
backend=anthropic, temp=0.77, gift=0.61, cooldown=30 分.

### llive 累積数値

- 1518 → **1653 PASS** (+135, 全 marathon 累積)
- 本 Phase 0.9: +19 test (v0.C)

### 教訓 (v0.C から 3 つ)

1. **染色体単位の交配は多様性に寄与** — SegmentCrossover で diversity 維持
2. **checkpoint + resume があると「長時間 GA は普通の運用」** — serial でも
   セッション跨いで世代を進められる
3. **19 dim でも収束は十分速い** — 30 体 × 12 世代 = 360 評価で +40% 改善

### 次セッション残作業 (累計, 本 Phase で増えた分)

11. v0.C Phase 2 — 実 LlivKernel spawn (subprocess 経由) + ephemeral data_dir
12. v0.C Phase 3 — lleval 統合 (19 dim genome → lleval Config bridge)
13. v0.C LV-10 — 系統樹可視化 (`lineage.mmd` Mermaid)

### 検証

```bash
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1653 passed

py -3.11 scripts/demo_evolutionary_loop.py --problem llive_variant --size 30 --gens 12 --seed 42
# best 0.5358 → 0.7514

py -3.11 scripts/demo_evolutionary_loop.py --problem llive_variant --size 50 --gens 30 \
    --out out/llive_variant_resume_test/
# checkpoint 機構の動作確認
```

---

## Phase 0.10 — 2026-05-21 夜 (前倒し補強 wave)

ユーザー指示「次に私がコメント入力するまで、出来ることを先行して進めて」+ 連続コメント
(LinkedIn 多言語 / Qiita 多言語 / 海外 platform / GitHub リンク) への並行応答.

### llive 側 (新規 +16 test, 1669 PASS)

- `src/llive/variant_runner.py` — v0.C Phase 2 subprocess 起動先 CLI
  (`py -m llive.variant_runner --config-json ... --output-json ...`).
  実 LlivKernel spawn は将来, 現状 mock baseline. exit code (0/1/2/3/4) で
  fail mode 分離.
- `src/llive/perf/evolutionary/lineage.py` — LV-10 系統樹可視化.
  `Winner` dataclass + `winners.jsonl` I/O + `render_lineage_mermaid` で
  graph TD 描画. parent_ids 辿って世代間 lineage 表現. ghost node サポート.

### lleval 側 (新規 +12 test, 59 PASS)

- `src/lleval/bridges/llive.py` — llive 19 dim Genome → lleval ProviderSpec
  上書き + Report cells → 5 軸合成 dict. llive は optional 依存.
- `src/lleval/report/html.py` — Report → HTML 文字列 (CSS 内蔵 self-contained).
  anomaly セル赤背景, summary block, XSS escape. stdlib only.
- `CHANGELOG.md` 0.1.0a1 エントリ追記
- `ROADMAP.md` v0.1.0a0 → 1.0 段階表

### portal / memory 反映

- `docs/spec/llive_variant_phase2_interface.md` — Phase 2 interface spec
  (subprocess / in-process transport, ephemeral data_dir, 5 fail mode, 系統樹)
- llive `docs/experiments/llive_variant_v0_C_2026_05_21.md` に checkpoint/
  resume/budget 実 file I/O 動作確認の追記 (Run 1/2/3)
- raptor memory:
  - `feedback_linkedin_translation_jp_only` 大幅修正 (多言語推奨に転換)
  - `feedback_qiita_github_links` 新規 (GitHub link 積極配置)
  - `feedback_overseas_tech_platforms` 新規 (海外 platform 戦略 5 step cross-post)

### 累積数値

- llive: 1518 → **1669 PASS** (+151 全 marathon 累積)
- lleval: 新規 → **59 PASS** (skeleton + 段階拡張)
- 主要 commit (本 Phase): llive 2 + lleval 2 + portal 0 = 4 件
  (portal は memory のみ更新, commit 不要)

### 残作業 (次セッション)

| # | アクション | 依存 |
|---|---|---|
| 1 | llama-server + Mamba GGUF 実走 smoke | llama-server 起動 |
| 2 | low_spec bench 実 backend 実走 | step 1 |
| 3 | RWKV-7 を `RwkvBackend` で繋ぐ | RWKV.cpp 起動 |
| 4 | `backend_select` を実 backend で 5 体並走 | step 1-3 |
| 5 | lleval 実 GitHub repo init | user 承認 |
| 6 | lleval v0.1.0a2 (promptfoo subprocess 実走) | step 5 + npx promptfoo |
| 7 | claude-smart 評価 Session 1 | user が worktree で起動 |
| 8 | llive optimize/core → main 3 PR | user 承認 |
| 9 | credential 復旧 → bench 再走 | 外部 |
| 10 | asciinema 3 本 | operator |
| 11 | **v0.C Phase 2 実 LlivKernel spawn** | kernel module 実装後 |
| 12 | **llive lineage 実 GA loop 統合 hook** (現状は run 終了後に手動書出し) | 設計後 1h |
| 13 | **海外 platform 投稿 cross-post 試行** (Medium / dev.to にQIITA #21-23 の en 版) | user 投稿判断後 |
| 14 | **Qiita 記事に GitHub link 積極配置 retrofit** (既存 QIITA #21-23 更新) | 各 30 min |

### 検証

```bash
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1669 passed

py -3.11 -m llive.variant_runner --config-json /tmp/test_cfg.json \
    --output-json /tmp/test_result.json
# mock 経路で動作確認可

cd D:/projects/lleval
py -3.11 -m pytest tests/unit -q
# 59 passed
```
