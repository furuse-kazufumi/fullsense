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
| [LLM モデル融合ランドスケープ+設計空間 (2026-07-04)]({{ '/research/llm_model_fusion_landscape_2026-07-04' | relative_url }}) | gaitlab 形態融合(morphology.py)発の「LLM もモデル融合できるか」を Workflow 2本(調査13+多角検討10=23 agents, 一次検証)で網羅。**3分類=①重み空間マージ(同一base必須・訓練不要: Soups/TIES/DARE/SLERP)②深さグラフト/frankenmerge(gaitlab接ぎ木に最も近い・healing必須: SOLAR DUS)③知識融合(異アーキ可・唯一の一般解だが蒸留=学習: FuseLLM)**。「無関係な別モデルの重みを訓練なしで平均」は原理的に不可能(Git Re-Basin)。設計空間=基質×階層 2軸マップ+異分野アナロジー(HGT/接木/合金)+TRIZ+align→stitch→distill。**FullSense適用: ①gaitlab QD-of-merges(MapElites転用)②llcore専門家蒸留マージ③llive進化マージ(Sakana直系)④persona=steering合成⑤state/KV融合**。最初の一歩=mergekit CPU SLERP。honest訂正=Sakana"70B超え"は日本語ベンチ限定/異tok橋渡し未実証, RegMean正典=2212.09849 |
| [Grok「AI革新的機能スタック」検証 (2026-07-03)]({{ '/research/grok_capability_stack_verification_2026-07-03' | relative_url }}) | claude-loop タスク経由の Grok 提案(agent/physical-AI/量子/BCI)を raptor Workflow 8 agent で一次情報裏取り。**Grok の手軽さ順は概ね正だが量子/BCI を実行可能 phase として並べた点が誇張**。ユーザー価値順=①on-prem reasoning model(gpt-oss-20b で Qwen 障壁回避)②GPU 並列 QD(既決 MuJoCo→MJX→Isaac は Newton 1.0 GA で補強)③framework 導入(置換で低価値)④量子=SKIP(QML 優位ゼロ/BP-free は古典模倣可)⑤BCI=SKIP(thought-to-text は teacher-forcing インフレ)。誇張補正=vLLM 19x→single-stream 同等/AutoGen 1.0 は存在せず MS Agent Framework/Cosmos 5090 で 2B すら borderline |
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
| [特許 DB 照会 — 差別化の特許面検証]({{ '/research/patent_search_2026_06_06' | relative_url }}) | 監査の既知の穴 (特許未照会) を閉じる調査。**結論 = clear**: 四点交差点を同時 claim する特許ゼロ (英 14 + 日 3 クエリ + assignee 観点)。narrows (弱) 2 件 (US10896032 認証→展開ガバナンス / US11868855 stability 語彙被り) は related work で先回り対比推奨。「証明ゲート×更新」系は検索結果が arXiv に逸れる = 概念が学術段階に留まる間接証拠。D2' (verified memory evolution) は特許面でも空白 = 出願による先取りも理論上可能。限界: 専門 DB 非使用/未公開出願 18 ヶ月不可視 |
| [包括計画 — 特別 DNA × 全やり残し統合]({{ '/research/master_plan_2026_06_06' | relative_url }}) | ユーザー Goal「包括的な計画」への回答。5 トラック (T1 llcore 本線 / T2 llive+Sakana / T3 発信 / T4 防御調査 / T5 台帳掃除) に全やり残しを統合し、次 3 セッションの推奨実行順を確定 (Phase 0 文言再定義 → Phase 1 配線 → Phase 2a verified memory ★時間窓)。llive 本走行 06-02 停止の発見と再開判断、user-gate 一覧も収録 |
| [llterm spec — Claude Code 自走端末]({{ '/research/llterm_spec_2026_06_06' | relative_url }}) | ユーザー発案の Claude Code 専用端末。主目的 = **Claude の自己制御拡張 (自走・自律)**。閉ループ PoC 実証済 (`--session-id`/`--resume` で文脈保持、session は cwd ごと)。3 層 (制御プレーン llterm-ctl / stream-json セッションホスト / PowerShell 同等シェル+自前レンダリング表示)。要件の肝 = 長テキストで固まらない (Warp の轍) / ちらつき根治 / ①② 桁ずれ根治 (East Asian Width) / HITL gate+監査内蔵 / protocol 再発明しない。先行調査 honest: 7 割既存 (ccr が prototype)・3 割新規 |
| [Phase 2a verified memory evolution 設計]({{ '/research/phase2a_verified_memory_evolution_design_2026_06_06' | relative_url }}) | Workflow (research 3 + 設計 2 案 + 敵対 6 verdicts) の統合設計 doc。推奨 = Case B (Trajectory-Tube Memory Invariant Gate) 主軸 + Case A の scalar named-slot を bridge anchor に。最小 PoC = `gate_mode="trajectory_tube"` を minimal_ga に additive 追加し tracking_tube.admits を呼ぶ + 3-arm A/B (none/contraction/trajectory_tube)。**最大リスク = VLA (arXiv 2605.11196) が memory 更新写像の contraction を先に解析証明済の可能性** + tube gate は Z3-exact でなく閉形式 numpy (over-claim 注意、doc 内で先回り訂正済) |
| [差別化監査 + 特別 DNA ロードマップ]({{ '/research/differentiation_audit_dna_roadmap_2026_06_06' | relative_url }}) | 敵対的差別化監査の確定結果: **breaks 0 / narrows 36 / background 8** (44 候補 + 盲点 3 角度追加探索)。生存差別化核 = 「sound contraction 証明 × Transformer 記憶コア × 進化ループ内 prove-then-reject × 動く実装」の四点交差点。D1'-D4' クレーム限定再定義 (SSGM 看板先取り/SEVerA 別レイヤ/Z3 看板乖離/出荷 evolve() 未配線) + 防御壁 15 件 + **Phase 0-4 優先度ロードマップ** (文言→配線→verified memory 小PoC→防御深掘り→地形合流) |
| [古典 DNA マッピング (孫子・論語)]({{ '/research/classics_dna_mapping_2026_06_06' | relative_url }}) | 計算力で大手に追いつけない前提下で差別化 trait を積層する「特別な DNA」戦略。孫子 13 篇 + 論語から FullSense/llcore に翻訳できる原理を**20 個**抽出 (廟算/先勝/避実撃虚/兵は詭道/勢/温故知新/過則勿憚改/学思並重/和而不同/知之為知之/利器/正名 等)。各原理を (a) 研究戦略 / (b) 設計遺伝子 / (c) 検問・統治 に写像 + 篇名一次裏取り。**新設遺伝子座 5 件 (G14 先勝文化 / G15 二層倫理=詭道≠仁 / G16 避実撃虚 niche / G17 勢 / G18 正名+利器)** を提案。raptor の既存タスク discipline 版とは別翻訳 (アーキ level DNA)。llive ontology に `sun-tzu-strategist`/`confucius` ペルソナ追加済 |
| [CAV/TACAS 逆引き 2 巡目 — 交差点脅威監査]({{ '/research/cav_tacas_reverse_lookup_round2_2026_06_07' | relative_url }}) | 監査 critic 指摘の最優先盲点 (FM venue 逆引き 1 巡のみ) を Workflow 36 agents で閉じた。**結論 = breaks 0 / narrows 17 / SSGM 後続実装なし** (verified memory evolution の実装先取り窓は開いたまま)。新規 Tier 1 narrows = Scrivens 2026 ペア (weight 更新 prove-then-reject の最近接, ただし Lipschitz-ball≠contraction) / CART (記憶コア ρ<1 だが learned≠proven) / RNN-SDP。Tier 2 = α,β-CROWN Jacobian (将来 certifier 候補兼用) / SpectralGuard / adaptive-RTA 系。PAPER_DRAFT four-point intersection 節へ同日編入済 + 特許照会済の事実で provenance 文も訂正 |
| [内部状態安定性解析の防御地図 (T4 4-3)]({{ '/research/internal_state_stability_defense_2026_06_07' | relative_url }}) | D4' 最脆部 (「Hopfield/SSM はとっくに安定性解析している」) の先回り。Workflow 38 agents・4 系統 sweep。**結論 = breaks 0 / must_cite 27**: 隣接は成熟分野だが全候補が (a)解析・診断 (b)by-construction (c)監視 のいずれかで、**prove-then-reject 採否ゲートはどの系統にも無い**。「gate」語彙衝突 (Gated DeltaNet の forget gate ≠ admission gate) の明示対比が必須と判明。系統 5 群・代表 ~14 件を PAPER_DRAFT に同日編入 (新グループ「Stability analyses of memory-core internal dynamics」) |
| [SPEC-MESH 先行研究 — 被り/独自分析]({{ '/research/spec_mesh_prior_art_2026_05_24' | relative_url }}) | rad-research で SPEC-MESH の先行研究を確認。**核心 (分散 speculative=DSD 2511.11733 / branch-level=B-PASTE / fast-fallback=Speculative Actions) は 2025-2026 に先行研究が厚く、完全な新規ではない**と判明。独自価値は **Ed25519署名+Byzantine結果検証 (SPEC-MESH-11) / SPC grounded トリガ / on-prem 純度** に集中すべき。被り/独自/あえて不採用の3列表。token-level SD は llmesh 範囲外。新知識は RAD コーパス新クラスタ `cluster_08_distributed_agentic_spec` に蓄積 |
| [Gemini ブレスト #3/#4 実装着地]({{ '/research/gemini_brainstorm_impl_2026_05_24' | relative_url }}) | Gemini 4 案のうち **#3 Antifragile Mutation (llive `f2c2d1e`, 28 tests)** = 高 surprise を学習機会に変え panic mode で探索 10x + 対立 TRIZ pair unlock + AuditTrail 署名 (opt-in/fail-closed) と、**#4 Speculative Mesh Execution (llmesh `2a05f64`, 23 tests)** = メイン推論中の予測分岐を idle peer へ Ed25519 署名投機投入し mesh から回収 (LAN-first/fail-closed 検証/honest disclosure) を着地. 両者とも**予測符号化アーキテクチャ**と親和. #1 予測検証 / #2 KV-cache は未実装 |
| [ペルソナ ontology 拡張 — affinity 自動算出]({{ '/research/persona_ontology_expansion_2026_05_24' | relative_url }}) | llive 進化の persona ontology を数百人規模へ段階拡張する基盤。**ユーザー指摘「ハードコードを疑え」→ 手書き factor_affinity を撤回**し、affinity_text (特性記述文) から keyword_extractor で**自動算出** (`persona_extended.py`, commit `d940ff3`)。算出 top 因子が記述意図と整合 (darwin→reality_link, turing→exploration 等)、回帰テスト 6 件。投入候補カタログ約 60 名 (非西洋/女性/古典〜現代の多様性) + 改善メモ (本命=LLM injection) を下調べ。実投入は段階的 |
| [RepIR → llrepr MCP 互換設計 (2026-05-23)]({{ '/research/repir_mcp_compat_2026_05_23' | relative_url }}) | llrepr (LLVM-for-expression) の MCP structuredContent 配線設計。protocolVersion 2025-06-18 + outputSchema + text 後方互換。RepIR→llrepr 改名経緯 (github.com/repir/repir 衝突回避) を収録 |
| [Speculative Mesh 本格配線 (SPEC-MESH-02/03/04)]({{ '/research/spec_mesh_wiring_2026_05_25' | relative_url }}) | llmesh SPEC-MESH-02 (transport)・03 (executor)・04 (fast-fallback) 配線完了 + security 修正 (ingest_result fail-closed 化等)。全 llmesh テスト exit 0 確認 |
| [HeyGen Hyperframes 調査 — HTML→決定論的 MP4]({{ '/research/hyperframes_heygen_survey_2026_06_12' | relative_url }}) | Telegram 経由ユーザー送付の調査。HeyGen の agent-first OSS (Apache-2.0, 3 ヶ月で 26.9k★): data 属性付き HTML + seekable animation adapter → headless Chrome + FFmpeg で決定論的 MP4。判定 = animemd/mangamd/SVG 戦略と**競合せず隣接** (出力メディア相補)、llrepr の typed-representation 路線の大手裏付け、frame.md (design.md のカメラ向け反転契約) は llrepr writer 設計に直接示唆。提案 (human-go) = llcore gate デモの MP4 化 PoC → X/YouTube 発信チャネル拡張 |

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
| [検問体系監査 (A-Evolve 三重検問棚卸し)]({{ '/research/gate_taxonomy_audit_2026_06_06' \| relative_url }}) | A-Evolve (arXiv 2602.00359) の AST/スキーマ/sandbox 三重検問 + 来歴/rollback/HITL を実コードで棚卸し。我々だけの 4 軸 (llcore 形式証明 / llcore null harness / llmesh SPC / raptor 供給網) を明示し、あり得る検問 16 種を 4 段階 (変異/採用/実行/事後) で体系化。TOP-3 = SPC 管理図 runtime gate / llcore 証明ゲート src 配線 / llive metamorphic gate |
| [Telegram共有AIツール調査 + 競合スキャン (2026-06-10)]({{ '/research/telegram_ai_tools_scan_2026_06_10' \| relative_url }}) | ユーザーTelegram共有4件(ui-skills/NotebookLM-MCP/GitHub急上昇10選)を一次情報で網羅調査。★FullSense個別機能は深刻に先行(hermes-agent 189k★がllive, ECC 211.8k★がraptor, codegraph/headroomがrtkを先行)。FullSense優位4点=産業接続/責任architecture/verified-plasticity/二重設計は全件に皆無。競合の自己改善主張は全て第三者未検証ベンチ |
| [画像認識25年パラダイムシフト (藤吉2026) + FullSense接続]({{ '/research/image_recognition_25yr_paradigm_2026_06' \| relative_url }}) | 藤吉弘亘講演(①ハンドクラフト→②CNN→③ViT自己教師→④MLLM→⑤世界モデル×VLA)のFullSense戦略接続。★p.51「世界モデルは安全に寄与するが保証でない」⇔llcore verified-plasticity=sound certで保証=記事決定的対比。予測符号化テーマの学術裏付け |
| [Zhipu AI / GLM ランドスケープ (2026-06-29)]({{ '/research/zhipu_glm_landscape_2026-06-29' \| relative_url }}) | Zhipu/Z.ai GLM 系列の一次検証ブリーフィング(WF 11 agents・敵対 fact-check)。最新=GLM-5.2(2026-06-16, ~744B/40B MoE, 1M ctx, MIT)。★ライセンス判定=大型 teacher は GLM-MIT が Qwen 優位だが **sub-2B 蒸留ターゲットには MIT GLM 無し**(最小 MIT dense=9B / GLM-Edge は glm-4 license)→ llcore 蒸留 base は Qwen Apache-2.0 維持。効率転用=DSA dense→sparse retrofit が LoLCATs 型と同型 / Glyph 視覚 token 圧縮。VLM=GLM-4.1V-9B(MIT)を Qwen-VL 代替候補。honest caveat: MIT は card metadata 由来(LICENSE blob 404 未読)+ 米 Entity List リスク |
| [option-b 一次検証 — PoC-1 未踏性ほか (2026-06-29)]({{ '/research/option_b_verification_poc1_novelty_2026-06-29' \| relative_url }}) | llcore option-b 研究深掘りの一次本文検証(WF 25 agents・12 task・敵対反証)。★**PoC-1 の iterative-read 機構は非新規**(N3 flip: Resonator/VSA cleanup memory が codebook sparse-recovery 反復readを既占有 / Schlag で「linear-attn state」限定詞は無意味)→ 未占有は application wrapper のみ=domain-transfer。P6 kill-risk=非転移(a-priori-dead 否定だが softmax-only 防御も無効)。**P2: write 側は飽和せず**(GDN-2 純 erase/write で +9-10pt, contradicts prior)。**F1: Qwen3.5 base 乗換 NO-GO**(multimodal+18/24層GatedDeltaNet)→ Qwen3-0.6B/1.7B 推奨。T6 VLM=PARK→2条件gate。P7 天井=honest(read-only on vanilla-additive は最弱→gated/delta へ)。triz/efficient_arch doc の 10 箇所を矛盾・修正 |
| [モデル融合ランドスケープ (2026-06-29)]({{ '/research/model_fusion_landscape_2026-06-29' \| relative_url }}) | 異種モデルを 1 つにする手法の一次検証(WF 13 agents・6 family・arXiv ID 全件照合)。★**weight-merge は同 arch+同 tokenizer 必須=GLM→Qwen は重みで混ぜられない**。「全く別」を 1 weight にできるのは **蒸留(knowledge-fusion)のみ**。決定木=別の度合いで手法選択(soups/TIES/DARE→Git-Rebasin/ZipIt→MergeKit/EvoLLM→FuseLLM/FuseChat/CALM→VLM bridge)。**llcore 推奨=FuseChat-3.0 流 implicit multi-teacher 蒸留(GLM-MIT+Qwen→constant-state student, SFT+DPO で student arch 非依存)本命 / weight-merge は同 Qwen-base expert 統合のみ / MoE-merge・ensemble は全 expert 常駐で memory north star と衝突=却下**。softmax→linear の state 圧縮は別ステージ |
| [脳構造を目指す FullSense (2026-06-29)]({{ '/research/brain_structured_fullsense_2026-06-29' \| relative_url }}) | 脳組織 6 原理→FullSense アーキの具体マッピング(WF 7 agents・機構 vs 比喩を冷徹仕分け)。★衣装を剥ぐと実体は 4 機構=delta-rule書込/疎キー/sleep-consolidation/workspaceボトルネック。**①②は既に llcore ベース(Gated DeltaNet)内、④は orchestration 専用 → 脳が足す唯一の新機構は ③ sleep/consolidation を multi-teacher fusion に適用する 1 本だけ**。★CLS 3-store 訂正: 新皮質=llcore学習済み重み / 海馬=llive外部メモリ(HippoRAG) / working memory=llcore定数状態。**Schlag fast-weight 容量限界=P7 天井**で llive 外部 store を必然化。第1位 PoC=2教師 dark-replay(DER++)で逐次fusion+教師A忘却を baseline 実測。honest: 脳枠は新機構の源としては inspirational、選別/組立/統治の発見的手法としては生産的(resident MoE 却下が硬い負の知見) |
| [★FullSense 統合 capstone — 融合×脳×PoC (2026-06-29)]({{ '/research/fullsense_fusion_brain_capstone_2026-06-29' \| relative_url }}) | fusion deep-dive(WF 8 agents, frontier 全文検証+レシピ+TRIZ/異分野)と brain WF を実行可能 1 枚に統合。★両者収束=**CLS 3-store=hot/cold split が breadth アーキ / sleep=採用すべき DER++(新機構でない)/ 真の net-new=T1 operator-union write-rule + X1 CDMA 割当のみ(medium)**。frontier 4本(AC/DC=oracle Coverage・param数, HeteroFusion=hypernet transfer で weight-merge 再確認, FusionRoute=ensemble 反O(1), BLD=cross-tokenizer bridge で OFF既定ablation)は実在も推奨を覆さず。本命=FuseChat-3.0 IMF+WRPO に interference-staging rule。★first PoC(CPU並行)=runtime/fusion.py IMF plumbing+axis-D baseline / multi-source MQAR で T1+X1 vs logit-KD を falsify。P7 は allocate するだけ・脳枠は選別/統治の発見的手法 |

技術詳細・統合 verdict は llcore project `docs/poc/COMPLETION_VERDICT.md`、研究計画書 v1 は `docs/papers/2026-05-29_research_plan_core_evolution.md`。

### 2026-05-31 進捗 — ③(選択圧)研究の特性化 + VNN-COMP 新カテゴリ準備

**(A) ③ 研究 arc の総括** (llcore `docs/poc/`、全 Codex pair-review 済):
進化4要素の③(適者生存・選択 = MAP-Elites の behavioral niching)が「実問題でペイするか」を CPU で詰めた。
Step C(記憶タスク=N/A: 床/天井で非診断)→ 梯子段1(複数 reservoir 結合でも 5-bit parity は degree-5 床で
解けず)→ **E-A(多タスク汎化で honest negative: ③ load-bearing でない)** → **適用条件の特性化(`STEP_C_APPLICABILITY_VERDICT.md`)**。
**核心: ③は「欺瞞性(谷の深さ)が閾値 d\*=0.16 を超える」landscape でのみ load-bearing**(3 seed 一致)。
過去の binary negative は「③無力」でなく「実問題の欺瞞性が閾値未満(smooth 側)だった」で統一説明できる(現状は
定性的 fingerprint、**numeric 実測は workflow 進行中**)。honest 現状 = 「実 AI 設計探索で③がペイする証拠は CPU 範囲では乏しい」、
本物の検定は GPU(実 LLM 損失地形の欺瞞性測定)。

**(B) VNN-COMP `online-arch-evo` 新カテゴリ提案** (確定独自軸 #7、最も明快に validated):
論文 `docs/papers/vnn_comp_online_arch_evolution_proposal.md` を **workshop 投稿可能水準に改訂**(VNN-COMP 2025=6th edition
反映 / 「contract mismatch」framing / IVAN(PLDI2023)等の最近接先行を §2.9.1 補完 / §9 honest 限界)。reference impl で
**§9 item 10(実 `.onnx`/`.vnnlib` パーサ)+ item 11(sat-verdict witness, grid-confirmed・spurious は unknown)** を実装、
**seed ベース benchmark generator** も着地。Path B = VNN-COMP organizers へ 2027 サイクルで提案(rules 和訳 + RFC ドラフト準備済)。

詳細・honest 内訳の単一の真実 = memory `project_llcore_init_2026_05_29`。llcore 本流 221 tests pass。push 未(llcore は GitHub repo 未作成)。

### 2026-06-02 進捗 — ③「谷深さ」決着(Step D)+ kernel 多様化 CPU 代替路 着手

**(A) ③ 第三軸 proper-power 決着** (llcore `research/step_d_settle/THIRD_AXIS_SETTLE_VERDICT.md`、capstone Codex pair-review ブロッカーなし):
2026-05-31 の「谷深さ実測 = N/A(循環論法で magnitude 測定不能)」を受け、**決定論 C1 多峰性測定**(ESN+ridge が rng を取らない性質で eval noise を機械eps化→noisy-flat 偽陽性を構造的に除去)が決め手となり、**実 text proxy 地形は valley≈0 で真に滑らか=単峰 → ③不要を (B) noise-free 確定**。「③不要に見えた過去 negative は underpower でなく地形が本当に滑らかだったから」が実 substrate 上で初めて裏付いた。実 multitask 近傍(C-gen4b)のみ「③ NOT null」の弱い兆候(fresh n=64 gate PASS)だが小効果+走行内ドリフト+多重比較で **load-bearing 候補/still_inconclusive 止まり**。K4 ridge clip は「能動的 suppression」→「診断的所見」に降格。verdict §7 推奨次手 = (b) GPU full LLM 損失地形(proxy 滑らか確定ゆえ③の本丸は多峰性が期待できる full LLM 地形)、**ただし投資判断=ユーザー**。

**(B) kernel 多様化 = ③ の CPU 代替路** (llcore `research/kernel_diversification/`):
GPU を待たず CPU で③に迫る別仮説 = **個々の kernel が滑らかでも 4 kernel 族(rwkv/mamba/hopfield/linear_attn)を union すると kernel 切替=不連続 fitness 段差で地形が multi-basin になりうる→③が GPU 無しで CPU load-bearing(BG9 最終目標)**。Stage 3a(BG1-5 mechanism feasibility)smoke PASS 済。Stage 3b BG6(task→best-kernel 写像が非定数か=specialist 出現)に着手。honest: 全 task 同一 kernel = 「kernel 中立」の valid negative。詳細・honest 内訳は引き続き memory `project_llcore_init_2026_05_29`(Step D Settle 節 + 2026-06-02 セッション節)。

**(C) BG9 決着 = N/A(構造的)= CPU kernel 抜け道は閉じている** (llcore `research/kernel_diversification/BG9_VERDICT.md`、事前登録 + 敵対 red-team で確定):
kernel-favoring task で substrate は非 inert 化(PASS)だが弱い(実質 3 kernel、hopfield は対角 mock で機能不全)。**harness validity が立たない** — ③(MAP-Elites の kernel_id niching)が強 baseline RR-hillclimb を排除できない。理由 = **kernel 選択は 4 離散の単一低次元座標で、RR は restart で kernel_id を直接サンプルして欺瞞 corridor を回避する**(Step4 の corridor が RR を排除できたのは behavior=mean(24次元)の CLT 不到達ゆえ)。red-team が faithful 4 構成 + 次元 sweep で敵対確証(③が RR を排除できる behavior 次元は kernel 空間に存在しない)。**構造的洞察 = ③ が load-bearing になるには高次元 behavior 空間が要る。kernel 選択(低次元)は条件を満たさない → 「探索空間を kernel 多様化で拡張すれば③が unlock するか」(Step4 §7) の答え = NO(CPU 構造的に)**。**GPU 含意**: CPU 抜け道が閉じたので③の残り路は高次元 GPU full-LLM 地形のみ(但し依然 bet=強 baseline が直接解くリスク=RR と同型)、ポートフォリオ判断 + クラウド借り事前登録1本が適正。詳細 = memory `project_llcore_init_2026_05_29`(BG9 決着節)。

**(D) ③ arc 結晶化** (2026-06-02): arc 全体を研究資産化。**論文 draft** `llcore docs/papers/third_axis_selection_arc_2026-06-02.md`(英語7103w「When Is Darwinian Selection Load-Bearing? A High-Dimensionality Condition for QD over Neural Dynamics」, honest negative + 高次元条件, TMLR/workshop/arXiv 候補)+ **検証済み生物学接地** `biological_grounding_third_axis.md`(Wright shifting balance↔③/Coyne 批判↔negative の鏡/暗化モフ↔低次元/Lenski Cit+↔高次元、7-agent web 検証 + caveat)+ **公開記事** QIITA_#34(arc 6段俯瞰+生物学, 技術版+かみくだき版, push 済)。残(投稿前)=repro code 公開/図/bib。詳細=memory `project_llcore_init_2026_05_29`(③ arc 結晶化節)。

### 2026-06-06 進捗 — L3 §3c 確定 + 検証器コスト削減スレッド + 論文 第一ドラフト

**(A) L3 §3c 最終化 + 3-lens 敵対検証** (llcore `research/verified_lm_evolution/VERDICT.md`):
null 対照 10 paired seed 確定 → 検証 Workflow (数値/過大主張/事前登録整合, 全 lens pass=false) の指摘を
一次データ再検算で反映。**「~84% で残存」は fitness スケール限定→CE(nats)では ~107%**(gate-gap は shuffle で
縮まない)を明記、**gate-gap は essentially structure-independent** と訂正、structure-dependent「gate-gap
residual」主張を撤回(real−null 残差非有意)。唯一の構造依存 signal=unigram-crossing に一本化。inf collapse
「8 sig figs/= unigram」→「~3 sig figs/0.0003 nats だけ上」訂正。**結論=L3 payoff は evolvability であって
language learning ではない**。

**(B) 検証器コスト削減スレッド = decisive 完了** (llcore `research/verifier_cost_reduction/SKETCH.md`,
memory `project_llcore_verifier_cost_reduction`): 律速=cert の **2^n 頂点列挙(状態次元 n)**。PoC を 3 段:
PoC-1 naive 境界 B1=σ(M)+σ(R) は緩すぎ(29.5%)→ **PoC-2 絶対値支配 B2=σ(\|M\|+R) が exact 2^n の 77.6% を
SVD 1 回・n=16 で 12,520x・偽陽性 0 で回収**, inf∪B2=87.2% で inf 単独超え → **PoC-2.5 で B2 取り逃し tail に
LM payoff 無し(最良遺伝子は B2 側, tail 優位は 0.001-0.003 nats=ノイズ)→ SDP(robust-LMI/R-LLM-1)は LM 目標で
NO-GO**。**結論: n は inf∪B2 でスケール、SDP は作らない**。L1 低ランク/L3 MOR/L4 コストを選択圧に(生物の還元進化,
良い安さ vs inf 罠/退化, パレート)を SKETCH に設計記録(user-gate)。

**(C) 論文 第一ドラフト** (llcore `research/paper/PAPER_DRAFT.md`, 1117 行): arc(SDP gate rigor)+R-LLM
(L0-L2)+L3(honest scope)+BG10(gradient escapes)+dimension thread+cost reduction を統合。9-agent Workflow
(証拠接地 §2-§8 並列起草→統合→over-claim 批評)で生成、批評 **overturns_core:false**(minor 2 件=abstract の
カバレッジ/tail 取り違え + inf∪B2 を single-SVD 誤称、反映済)。CPU/宣言的 SVG 図 3 枚 (`research/paper_assets/`,
matplotlib 不要) を配線。§6 に BG10 honest caveat(EVO 罠は wrapper で CE masked, admit-rate に出る)追加。来歴=CRITIQUE.md。

**(D) 公開記事** QIITA #36(本体+かみくだき, `fullsense docs/articles/QIITA_#36_*`): 「2^n の壁を破る vertex-free
健全証明 + コストを選択圧に」。**JA/EN/ZH/KO 4 言語完全版 + 図 3 枚 assets 同梱**(翻訳 Workflow で組成済)。
private/ignorePublish ドラフト。**honest 整合**: PoC-2.6 (coverage は n で 87→60% に劣化) は記事執筆後の
発見だったため、冒頭に **4 言語 addendum box (n=8 限定 + degradation を明示)** を追加済 (論文 PAPER_DRAFT.md
は本文反映済)。**かみくだき版にも 4 言語 addendum 追加済**。残 publish-polish: 本文中 n=8 値の文中注記
(addendum で up-front 開示済なので軽微)。

詳細・honest 内訳の単一の真実 = memory `project_llcore_verifier_cost_reduction` + `project_llcore_real_llm_pivot_2026_06_04`
+ `project_llcore_init_2026_05_29`。push 未(llcore は GitHub repo 未作成)。

## いつ更新するか

- `spinoff_ideas_2026_05.md` の Planned / Pattern が新しい段階に進む直前.
- 主要設計判断 (差別化軸) を変更する前.
- 競合 / SOTA が大きく動いたと感じたとき.
