---
layout: default
title: "Research"
nav_order: 92
has_children: true
---

# Research Notes

> AI agent (Claude Opus 4.7) が自律的に作成した先行研究 / SOTA 比較 / 競合
> 分析の集約場所. 「設計判断の前提資料」として参照する.

## ll- プロジェクト → FullSense への進捗フィードバック: 単一の真実

> **フィードバックはここに書く**: ll- プロジェクト (llive / llmesh / llove 等) の設計判断・実装完了・実験結果を FullSense portal へ反映する際の **単一の真実の場所 = この `research/index.md`** (詳細) + [`docs/doc_map.md`]({{ '/doc_map' | relative_url }}) (地図)。
>
> - **新しい先行研究 / 実験結果** → この index に行追加 + 対応 `.md` を `docs/research/` に置く
> - **新しいファイルの場所の記録** → `doc_map.md` に行追加
> - **進捗ログ (セッション単位)** → `docs/PROGRESS.md`
> - **次セッションへの引継ぎ** → `docs/NEXT_SESSION.md`
>
> FullSense 外 (Qiita 記事 / 実装 diff) には書かない。portal の index/doc_map を見れば全体が分かる状態を維持する。

## 一覧

| File | 内容 |
|---|---|
| [lleval — SOTA Survey]({{ '/research/lleval_sota' | relative_url }}) | LLM eval framework (OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse / TruLens / Ragas) の SOTA matrix + LM-as-judge bias + 推奨 fork base |
| [llgrow — Prior Art Survey]({{ '/research/llgrow_prior_art' | relative_url }}) | HITL content automation (Jasper / Mautic / Langfuse 等) と academic 2025 研究を比較し、個人開発者 OSS 配信 vertical の gap を整理 |
| [Cognitive Mesh vs SOTA]({{ '/research/cognitive_mesh_vs_sota' | relative_url }}) | llive v0.8 Cognitive Mesh (M8.1〜M8.9) を MemGPT / Generative Agents / A-MEM / Reflexion / Constitutional AI 等と sub-system 毎に対応づけた比較 |
| [llcraft — Creative Material SOTA]({{ '/research/llcraft_sota' | relative_url }}) | on-prem creative material (TTS / 画像 / 動画 / 音楽) の OSS Stack matrix + license tier 管理. C2PA + IPTC 2025.1 への llcraft 拡張案 |
| [llrisk — Continuous Risk Tracking Prior Art]({{ '/research/llrisk_prior_art' | relative_url }}) | AI-driven GRC / DevOps risk monitoring / LLM × risk register / reputation / developer burnout を 6 軸縦割りで整理. 個人開発者向け on-prem 空白 |
| [llgov — AI Governance / Compliance SOTA]({{ '/research/llgov_sota' | relative_url }}) | NeMo Guardrails / OPA / Cedar / MS Agent Governance Toolkit / Credo AI / Holistic AI の matrix + EU AI Act Art.9-15 自動検証 OSS の空白 |
| [LLM × Evolutionary — Prior Art]({{ '/research/llm_evolutionary_prior_art' | relative_url }}) | llive v0.B/v0.C (集団 GA × 19 dim genome × subprocess transport) と類似する LMX / EvoPrompt / Promptbreeder / EUREKA / FunSearch / R2SAEA / MappingEvolve / MASPO の SOTA matrix + 差別化 4 軸 (on-prem / 19 dim 数値 / subprocess / honest disclosure) |
| [AI-that-produces-AI — Competitive SOTA (Stream F)]({{ '/research/evolution_research_competitive_sota_2026_05_25' | relative_url }}) | 「進化で新 AI を生む」競合フロンティア掃討。19 システム表 (NEAT/AutoML-Zero/POET/ELM/FunSearch/Voyager/Promptbreeder/Eureka/STOP/Self-Rewarding/ADAS/OMNI-EPIC/CycleQD/AI Scientist/**AlphaEvolve**/**DGM**/Gödel Agent/AI-GAs) を G(生成)/R(自己改善)/O(開放端) で分類し year/mechanism/限界/on-prem? を整理。FullSense の白地 = 検証可能性無しの主観・文化領域 × 明示文化因子 × pull型獲得 × 迂回不可ガバナンス × on-prem。falsifiable 差別化テーゼ + 反証条件 (F1-F5) + ADOPT 3 件 (island/archive・2 段 LLM ensemble・文化版 interestingness)。honest: アルゴリズム発見の品質では cloud-scale に勝てない/勝とうとすべきでない |
| [Mythos 競合スペック台帳]({{ '/research/mythos_competitor_spec_2026_05_27' | relative_url }}) | ゴール「進化型で Claude Mythos 超え」の競合ベンチ基準。Mythos(Capybara, vetted-only)公開数値=Cybench pass@1 100% / ExploitBench ACE 18/41 を proxy バーに固定。確定 harness=InterCode-CTF→Cybench, on-prem 在庫(qwen2.5:14b/7b/llama3.2), baseline 測定プラン。一次情報裏取り TODO |
| [Mythos 超え 設計正本 (進化型×セキュリティ)]({{ '/research/mythos_surpass_design_2026_05_27' | relative_url }}) | 生成(llive 進化)×検証(RAPTOR 決定論オラクル)×無制限 test-time compute の合流設計。核心 honest=**決定論オラクルが verifier-Goodhart を構造的に回避**(汎用推論との差), 残る壁=coverage 天井→クロスファミリ多様性で突破。RAD 先行研究 7 件 + PoC-CTF-0 進捗(coverage@k harness, mock 教訓=均等多様化は負ける→盲点ターゲット配分) |
| [Mythos 超え — 機構実証と gap の honest 中間報告 (2026-05-28)]({{ '/research/mythos_surpass_status_2026_05_28' | relative_url }}) | 実証の中間報告。何が実機実証/mock のみ/反証かを切り分け。**cross-family 脱相関=反証(全 on-prem が同盲点)**, **tool-exec レバー +0.25 / multi-turn+self-check 0.714 = 実機 ✓**, 進化×multi-turn=mock のみ。gap-to-Mythos=easy picoCTF 0.714 vs Cybench 100%。🔴律速=GPU(新 PC 前提)で本丸棚上げ。honest 結論=機構は健全で GPU-ready / 正面超えは困難 / 研究貢献(弱 on-prem を検証可能タスクで押し上げ)は独立に成立 |
| [表現 × リアルタイム — Ideation Marathon]({{ '/research/ideation_marathon_expression_realtime_2026_05_23' | relative_url }}) | FullSense「表現×リアルタイム」の 6 論点 (manga評価ラダー/一貫生成+licensing/llrepr型コントラクト/near-real-time天井/4コマ脚本/普及) を rad→triz→cross-domain で深掘り. 統合発見=**予測符号化アーキテクチャ** + **制約→強み転化 (TRIZ#22)**. llrepr(旧RepIR)=LLVM-for-expression / warning-zone 先回り生成 |
| [llrepr — PoC 実装着地 (旧 RepIR)]({{ '/research/llrepr_poc_2026_05_24' | relative_url }}) | 実装キュー#1 を llmesh `llmesh/llrepr/` に着地 (typed Representation IR=「LLVM-for-expression」). L1 閉集合ノード+glTF流 used/required 拡張, Markdown(degrade floor)/SVG/TUI writer, MCP `structuredContent`+text併置. **RepIR→llrepr 改名** (衝突回避) の経緯と PyPI/GitHub 衝突確認表も収録 |
| [ll- ファミリー名 衝突監査 + PyPI 予約]({{ '/research/llname_collision_audit_2026_05_24' | relative_url }}) | FullSense ll- 名を GitHub+PyPI で一括監査. **重要発見=旗艦 `llmesh` が HPE "LLM Agentic Tool Mesh" (HewlettPackard/llmesh 90★) と同名・同ドメイン衝突**(要戦略判断). llrepr/lleval/lltrade/lldesign を `llmesh-<n>` で PyPI 予約 (placeholder 0.0.1). 研究段階名(llcraft/llgov/llrisk/llgrow)は hygiene 配慮で見送り |
| [予測符号化 push PoC — 発見A の具現化]({{ '/research/predictive_push_poc_2026_05_24' | relative_url }}) | 実装キュー#2 を llmesh に着地. SPC warning-zone で説明を**投機生成**→確定時は予測 vs 実際の **typed diff(予測誤差)だけ push**(負レイテンシ). llrepr.diff + predictive_push(coordinator/zones/sinks) + MCP 2025-06-18 近代化. 計108 tests. **発見A=予測符号化アーキテクチャ**の最小具現. honest: 主利点は負レイテンシ(ペイロード削減は大型表現のみ), 実LLM explainer 未配線 |
| [高速化候補 全 PoC 判定マトリクス]({{ '/research/acceleration_poc_matrix_2026_05_24' | relative_url }}) | ユーザー指示「定量比較 PoC→効果あれば要件定義→本格導入」+「組み合わせ PoC」+ Goal「全 PoC」に対応。**5 単体 + 3 組み合わせ = 8 PoC** を実装・実測し優先付け。Speculative Mesh (LAN 最大 9.18x, 要件済) / Antifragile (脱出 0%→100%) / 適応推論予算 (44%削減) / 予測検証ゲート (29-80%) / KV-cache 差分 (LAN 29.85x)。Combo A/B/C も synergy 実証。**眼鏡 (lleval 流評価レンズ) で各 PoC を自己採点** (self-preference/simulation-only を flag)。LAN 前提が mesh 系の必須条件 |
| [SPEC-MESH-01 完遂 + B1 stale 訂正 + stdio_server 状態訂正]({{ '/research/spec_mesh_01_b1_feedback_2026_05_24' | relative_url }}) | 本日 llive/llmesh 3 件の着地を honest disclosure 文化で集約。**①SPEC-MESH-01 完遂** = 分岐予測器 (Frequency baseline / Markov order-1) を実装し hit_rate 単体測定 (cyclic 0.999 / markov-noisy 0.87 vs baseline 0.23、構造なし iid は ≈baseline で sanity 通過)。honest: 合成系列のみ / hit_rate≠speedup / 前提ブロック=ChangeOp 系列を出す稼働進化ループ未稼働 (BenchHarness は ops を捨てる)。**②致命バグ B1「実は修正済み」と確定** = genome label 解決 (`value_by_label` idx13) が既に入っており position 誤読は無い。回帰テスト 3 件で pin (commit `9c966a9`)。stale 記録訂正で進化再開の障壁 -1。**③stdio_server / predictive_push transport は配線完了済**と確認 (protocolVersion 2025-06-18 + outputSchema + structuredContent + MQTT/SSE sinks)。残る未了は実 LLM explainer のみ。3 件とも最後の鍵が**実 LLM 配線**に収束 |
| [SPEC-MESH 先行研究 — 被り/独自分析]({{ '/research/spec_mesh_prior_art_2026_05_24' | relative_url }}) | rad-research で SPEC-MESH の先行研究を確認。**核心 (分散 speculative=DSD 2511.11733 / branch-level=B-PASTE / fast-fallback=Speculative Actions) は 2025-2026 に先行研究が厚く、完全な新規ではない**と判明。独自価値は **Ed25519署名+Byzantine結果検証 (SPEC-MESH-11) / SPC grounded トリガ / on-prem 純度** に集中すべき。被り/独自/あえて不採用の3列表。token-level SD は llmesh 範囲外。新知識は RAD コーパス新クラスタ `cluster_08_distributed_agentic_spec` に蓄積 |
| [Gemini ブレスト #3/#4 実装着地]({{ '/research/gemini_brainstorm_impl_2026_05_24' | relative_url }}) | Gemini 4 案のうち **#3 Antifragile Mutation (llive `f2c2d1e`, 28 tests)** = 高 surprise を学習機会に変え panic mode で探索 10x + 対立 TRIZ pair unlock + AuditTrail 署名 (opt-in/fail-closed) と、**#4 Speculative Mesh Execution (llmesh `2a05f64`, 23 tests)** = メイン推論中の予測分岐を idle peer へ Ed25519 署名投機投入し mesh から回収 (LAN-first/fail-closed 検証/honest disclosure) を着地. 両者とも**予測符号化アーキテクチャ**と親和. #1 予測検証 / #2 KV-cache は未実装 |
| [ペルソナ ontology 拡張 — affinity 自動算出]({{ '/research/persona_ontology_expansion_2026_05_24' | relative_url }}) | llive 進化の persona ontology を数百人規模へ段階拡張する基盤。**ユーザー指摘「ハードコードを疑え」→ 手書き factor_affinity を撤回**し、affinity_text (特性記述文) から keyword_extractor で**自動算出** (`persona_extended.py`, commit `d940ff3`)。算出 top 因子が記述意図と整合 (darwin→reality_link, turing→exploration 等)、回帰テスト 6 件。投入候補カタログ約 60 名 (非西洋/女性/古典〜現代の多様性) + 改善メモ (本命=LLM injection) を下調べ。実投入は段階的 |
| [RepIR → llrepr MCP 互換設計 (2026-05-23)]({{ '/research/repir_mcp_compat_2026_05_23' | relative_url }}) | llrepr (LLVM-for-expression) の MCP structuredContent 配線設計。protocolVersion 2025-06-18 + outputSchema + text 後方互換。RepIR→llrepr 改名経緯 (github.com/repir/repir 衝突回避) を収録 |
| [Speculative Mesh 本格配線 (SPEC-MESH-02/03/04)]({{ '/research/spec_mesh_wiring_2026_05_25' | relative_url }}) | llmesh SPEC-MESH-02 (transport)・03 (executor)・04 (fast-fallback) 配線完了 + security 修正 (ingest_result fail-closed 化等)。全 llmesh テスト exit 0 確認 |

## lldarwin 設計ノート 2026-05-25〜27

> 2026-05-25 の開放端進化要件定義モードで 14 本が一括生成。lldarwin v2 PoC マラソン〜Stage1 結果まで含む。

| File | 内容 |
|---|---|
| [開放端進化 — openendedness 調査 (Stream E)]({{ '/research/evolution_research_openendedness_2026_05_25' | relative_url }}) | proxy 進化の自明収束 (gen23 全絶滅 / gen25 頭打ち) を出発点に open-endedness 手法 (novelty/lexicase/QD/MAP-Elites/NSLC/FUSS/minimal-criterion/中立理論) を整理。falsifiable 要件 §1.4-1.10 の根拠 |
| [進化アルゴリズム調査 (Stream A–F 横断)]({{ '/research/evolution_research_algorithm_survey_2026_05_25' | relative_url }}) | novelty search / MAP-Elites / ε-lexicase / NSGA / island / self-adaptive ES / UCB1 AOS / GESMR / Cultural Algorithms / Baldwin Effect を llive 文脈で評価。被り/独自/不採用 3 列表 |
| [表現・選択 再設計 (Stream C)]({{ '/research/evolution_research_representation_selection_2026_05_25' | relative_url }}) | genome 表現方式と選択圧手法の組み合わせ評価。ε-lexicase + z-score 正規化 + QD archive を推奨ベースラインとして確定 |
| [文化進化・生涯学習 (Stream D)]({{ '/research/evolution_research_culture_learning_2026_05_25' | relative_url }}) | CulturalChromosome / belief space 学習層 / persona pull 獲得を falsifiable な要件へ昇格。Baldwin Effect と Lamarckian 学習の適用範囲を整理 |
| [メタ進化研究 — EA 自体の進化]({{ '/research/evolution_research_meta_2026_05_25' | relative_url }}) | 進化アルゴリズム自身を進化させる meta-EA 手法 (CMA-ES σ 自己適応 / GESMR / ANAS 等) の SOTA と llive への適用可否 |
| [AI Safety for Open-Ended Agents (llive #13)]({{ '/research/evolution_research_safety_2026_05_25' | relative_url }}) | 開放端 / 進化エージェントの安全設計。収束停止 / ガバナンスゲート / Approval Bus 迂回防止 / fail-closed 原則の根拠整理 |
| [進化 fitness 再設計 — 多峰・多目的]({{ '/research/evolution_fitness_redesign_2026_05_25' | relative_url }}) | 単峰 proxy fitness の限界 (満点飽和) を解析し、多峰・多目的・多染色体 fitness の設計原理を整理。honest disclosure: "is it really evolving?" の問いを出発点とする |
| [進化設計の緊張関係と未解決決定]({{ '/research/evolution_design_tensions_open_decisions_2026_05_25' | relative_url }}) | 開放端進化設計で対立する選択 (novelty vs. quality / exploration vs. exploitation / complexity vs. tractability 等) を open decisions として整理。設計会議前に読む必読 1 枚 |
| [開放端 PoC 実験設計]({{ '/research/evolution_poc_experiment_design_2026_05_25' | relative_url }}) | sandbox / descriptor metrics / sweep 設計。PoC 実行前のプロトコル (変数の固定・測定指標・stop criterion) を標準化 |
| [開放端 PoC デプロイ結果]({{ '/research/evolution_poc_deployment_results_2026_05_25' | relative_url }}) | deployment sweep の実行結果集計。proxy/実 LLM fitness 切替え・population サイズ別の収束曲線 + honest disclosure (飽和パターン一覧) |
| [進化ラン可視化 計画]({{ '/research/evolution_visualization_plan_2026_05_25' | relative_url }}) | evolution.svg / persona_dominance.svg の現状評価 + 3D Gaussian Splatting 方向への可視化ロードマップ |
| [進化可視化 — 高度化調査 (3DGS・ALife)]({{ '/research/evolution_visualization_advanced_2026_05_25' | relative_url }}) | ユーザー要求「単なるグラフは NG、3DGS 時系列で魅せる」に応えて ALife / ALIFE / Tierra / Avida / Karl Sims 世代の先例を整理。可視化の系譜から llive 独自の表現空間を位置づけ |
| [進化ラン可視化 閲覧ガイド]({{ '/research/evolution_viz_viewing_guide_2026_05_25' | relative_url }}) | `scripts/run_persona_evolution_long.py` 出力ファイルの閲覧手順 (ツール選択・コマンド・トラブルシュート)。「手順が無いと意味が分からない」への恒久回答 |
| [llove Qt GUI アーキテクチャ設計]({{ '/research/llove_qt_gui_architecture_2026_05_25' | relative_url }}) | llove を CLI/TUI (Textual) から Qt 本格 GUI へ移行する際の設計指針。進化ランの可視化フロントとして ll 系プロジェクトを統合するロードマップ |
| [Perplexity × 開放端進化 SOTA (2026-05-26)]({{ '/research/openended_evo_sota_perplexity_2026_05_26' | relative_url }}) | overnight marathon で Perplexity が実施した QD / novelty / ORCH white-space 確認。RAD コーパスの QD/novelty ギャップを補完。鵜呑みせず一次情報で要検証 |
| [lldarwin v2 PoC マラソン — 方策確定ログ]({{ '/research/lldarwin_v2_poc_marathon_2026_05_26' | relative_url }}) | 「方策を決める」Goal の全記録。出発点 (12h ラン満点飽和) → Round 0-3 (6 PoC + Agent 4 体 + Perplexity) → 確定方策 (ORCH / ε-lexicase / factor-subspace QD / agentic 個体) → 実装ロードマップ Phase1-5。**設計意思決定の正本** |
| [lldarwin Stage1 実装結果 (2026-05-26)]({{ '/research/lldarwin_stage1_results_2026_05_26' | relative_url }}) | MultiPressureSelector + ORCH 基盤の Stage1 実装完了報告。テスト通過数・honest disclosure (実 LLM 比較 stub 状態) + 次フェーズ (Stage2 agentic 個体) への引継ぎ |
| [lldarwin v2 運用準備 (2026-05-27)]({{ '/research/lldarwin_v2_ops_readiness_2026_05_27' | relative_url }}) | 今夜の連続稼働に向けた動作テスト結果と ready/blocked 一覧。入力パターン別の挙動確認 + 残課題 (実 LLM 配線・factor-subspace QD スケールアップ) |

## 方針

- 1 ファイル = 1 トピック (spinoff 候補 or 主要設計判断).
- 800 字内外の要約 + Sources 5〜10 件. これ以上深い分析は **個別 spike** に派生.
- 内容は **AI 自律調査**. 人間が裏取りしてから設計に降ろす扱い.
- 引用元の link-rot は portal の Lychee CI で監視.

## llcore (Verified Neural Architecture Evolution) — 2026-05-29 着地

| Doc | 内容 |
|---|---|
| [llcore_cpu_poc_battery_completion_2026_05_29]({{ '/research/llcore_cpu_poc_battery_completion_2026_05_29' \| relative_url }}) | Stage 0-2 完成 (39 gates / 76 tests / Codex 5/5 Green、独自軸 4 軸 mechanism 実証) |

技術詳細・統合 verdict は llcore project `docs/poc/COMPLETION_VERDICT.md`、研究計画書 v1 は `docs/papers/2026-05-29_research_plan_core_evolution.md`。

## いつ更新するか

- `spinoff_ideas_2026_05.md` の Planned / Pattern が新しい段階に進む直前.
- 主要設計判断 (差別化軸) を変更する前.
- 競合 / SOTA が大きく動いたと感じたとき.
