---
layout: default
title: "Research"
nav_order: 92
has_children: true
---

# Research Notes

> AI agent (Claude Opus 4.7) が自律的に作成した先行研究 / SOTA 比較 / 競合
> 分析の集約場所. 「設計判断の前提資料」として参照する.

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
| [表現 × リアルタイム — Ideation Marathon]({{ '/research/ideation_marathon_expression_realtime_2026_05_23' | relative_url }}) | FullSense「表現×リアルタイム」の 6 論点 (manga評価ラダー/一貫生成+licensing/llrepr型コントラクト/near-real-time天井/4コマ脚本/普及) を rad→triz→cross-domain で深掘り. 統合発見=**予測符号化アーキテクチャ** + **制約→強み転化 (TRIZ#22)**. llrepr(旧RepIR)=LLVM-for-expression / warning-zone 先回り生成 |
| [llrepr — PoC 実装着地 (旧 RepIR)]({{ '/research/llrepr_poc_2026_05_24' | relative_url }}) | 実装キュー#1 を llmesh `llmesh/llrepr/` に着地 (typed Representation IR=「LLVM-for-expression」). L1 閉集合ノード+glTF流 used/required 拡張, Markdown(degrade floor)/SVG/TUI writer, MCP `structuredContent`+text併置. **RepIR→llrepr 改名** (衝突回避) の経緯と PyPI/GitHub 衝突確認表も収録 |
| [ll- ファミリー名 衝突監査 + PyPI 予約]({{ '/research/llname_collision_audit_2026_05_24' | relative_url }}) | FullSense ll- 名を GitHub+PyPI で一括監査. **重要発見=旗艦 `llmesh` が HPE "LLM Agentic Tool Mesh" (HewlettPackard/llmesh 90★) と同名・同ドメイン衝突**(要戦略判断). llrepr/lleval/lltrade/lldesign を `llmesh-<n>` で PyPI 予約 (placeholder 0.0.1). 研究段階名(llcraft/llgov/llrisk/llgrow)は hygiene 配慮で見送り |
| [予測符号化 push PoC — 発見A の具現化]({{ '/research/predictive_push_poc_2026_05_24' | relative_url }}) | 実装キュー#2 を llmesh に着地. SPC warning-zone で説明を**投機生成**→確定時は予測 vs 実際の **typed diff(予測誤差)だけ push**(負レイテンシ). llrepr.diff + predictive_push(coordinator/zones/sinks) + MCP 2025-06-18 近代化. 計108 tests. **発見A=予測符号化アーキテクチャ**の最小具現. honest: 主利点は負レイテンシ(ペイロード削減は大型表現のみ), 実LLM explainer 未配線 |
| [高速化候補 全 PoC 判定マトリクス]({{ '/research/acceleration_poc_matrix_2026_05_24' | relative_url }}) | ユーザー指示「定量比較 PoC→効果あれば要件定義→本格導入」+「組み合わせ PoC」+ Goal「全 PoC」に対応。**5 単体 + 3 組み合わせ = 8 PoC** を実装・実測し優先付け。Speculative Mesh (LAN 最大 9.18x, 要件済) / Antifragile (脱出 0%→100%) / 適応推論予算 (44%削減) / 予測検証ゲート (29-80%) / KV-cache 差分 (LAN 29.85x)。Combo A/B/C も synergy 実証。**眼鏡 (lleval 流評価レンズ) で各 PoC を自己採点** (self-preference/simulation-only を flag)。LAN 前提が mesh 系の必須条件 |
| [Gemini ブレスト #3/#4 実装着地]({{ '/research/gemini_brainstorm_impl_2026_05_24' | relative_url }}) | Gemini 4 案のうち **#3 Antifragile Mutation (llive `f2c2d1e`, 28 tests)** = 高 surprise を学習機会に変え panic mode で探索 10x + 対立 TRIZ pair unlock + AuditTrail 署名 (opt-in/fail-closed) と、**#4 Speculative Mesh Execution (llmesh `2a05f64`, 23 tests)** = メイン推論中の予測分岐を idle peer へ Ed25519 署名投機投入し mesh から回収 (LAN-first/fail-closed 検証/honest disclosure) を着地. 両者とも**予測符号化アーキテクチャ**と親和. #1 予測検証 / #2 KV-cache は未実装 |

## 方針

- 1 ファイル = 1 トピック (spinoff 候補 or 主要設計判断).
- 800 字内外の要約 + Sources 5〜10 件. これ以上深い分析は **個別 spike** に派生.
- 内容は **AI 自律調査**. 人間が裏取りしてから設計に降ろす扱い.
- 引用元の link-rot は portal の Lychee CI で監視.

## いつ更新するか

- `spinoff_ideas_2026_05.md` の Planned / Pattern が新しい段階に進む直前.
- 主要設計判断 (差別化軸) を変更する前.
- 競合 / SOTA が大きく動いたと感じたとき.
