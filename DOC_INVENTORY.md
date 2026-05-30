# 📚 ドキュメント目録 — fullsense

> 自動生成 (`py -3.11 D:\tools\gen_doc_inventory.py <repo>`)。ファイル追加後に再実行で更新。
> **公開/内部フラグはヒューリスティックの仮判定**。公開前に必ず人手で確認すること。

- 総ドキュメント数: **274** （🌐 公開候補 12 / 🔒 内部? 46 / ❓ 要判断 216）
- コーパス・依存・仮想環境・.git は除外。

## 目次

- [(ルート)](#g0) (3)
- [docs](#g1) (14)
- [docs/architecture](#g2) (1)
- [docs/articles](#g3) (42)
- [docs/articles/2026-05-17](#g4) (29)
- [docs/articles/2026-05-18](#g5) (6)
- [docs/articles/2026-05-20](#g6) (1)
- [docs/articles/2026-05-21](#g7) (1)
- [docs/articles/2026-05-22](#g8) (3)
- [docs/articles/2026-05-23](#g9) (1)
- [docs/articles/archive/2026-05-17](#g10) (29)
- [docs/articles/archive/2026-05-18](#g11) (6)
- [docs/articles/archive/pre-numbered](#g12) (6)
- [docs/articles/assets/lldarwin_2026_05_26](#g13) (1)
- [docs/articles/drafts](#g14) (6)
- [docs/benchmarks](#g15) (8)
- [docs/benchmarks/2026-05-16-matrix](#g16) (1)
- [docs/benchmarks/2026-05-16-quiz-debug](#g17) (1)
- [docs/benchmarks/2026-05-16-quiz-release](#g18) (1)
- [docs/benchmarks/2026-05-17-quiz-debug](#g19) (1)
- [docs/benchmarks/2026-05-17-quiz-release](#g20) (1)
- [docs/design](#g21) (2)
- [docs/papers](#g22) (1)
- [docs/regulatory](#g23) (7)
- [docs/research](#g24) (42)
- [docs/spec](#g25) (3)
- [docs/vision](#g26) (8)
- [tools/devto-publish](#g27) (1)
- [tools/qiita-cli-poc](#g28) (3)
- [tools/qiita-cli-poc/input_copies](#g29) (2)
- [tools/qiita-cli-poc/public](#g30) (43)

<a id="g0"></a>

## (ルート) (3)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributing to FullSense (Portal) | Thanks for your interest in the FullSense umbrella portal. | 2026-05-16 | 🌐 公開候補 |
| [README.md](README.md) | FullSense ™ | FullSense is the parent brand under which three open-source products are | 2026-05-16 | 🌐 公開候補 |
| [SECURITY.md](SECURITY.md) | Security Policy — FullSense Portal | This repository is the brand portal for FullSense. It contains only | 2026-05-16 | 🌐 公開候補 |

<a id="g1"></a>

## docs (14)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [cognitive-mesh.md](docs/cognitive-mesh.md) | FullSense ™ — Cognitive Mesh (llive v0.8) | ユーザ (Kazufumi Furuse, 2026-05-18) が言語化した 人間の認知構造: | 2026-05-19 | ❓ 要判断 |
| [comparison.md](docs/comparison.md) | FullSense ™ vs. the field | Letter grades reflect 2026-05-16 state of the art. We update this page when | 2026-05-18 | ❓ 要判断 |
| [doc_map.md](docs/doc_map.md) | FullSense ™ — Document Map | — | 2026-05-28 | ❓ 要判断 |
| [index.md](docs/index.md) | FullSense ™ | Umbrella brand & spec for llmesh / llive / llove | 2026-05-28 | 🌐 公開候補 |
| [NEXT_SESSION.auto.md](docs/NEXT_SESSION.auto.md) | Next Session — auto-generated snapshot | - HEAD vs upstream (左=ahead 右=behind): 0	0 | 2026-05-23 | 🔒 内部? |
| [NEXT_SESSION.md](docs/NEXT_SESSION.md) | Next Session Handoff (2026-05-19 朝 → next) | overnight PoC マラソン（ユーザー Goal「徹底的に要件整理＋進化型として独自性＋PoC何度も」）で | 2026-05-27 | 🔒 内部? |
| [NOTES.md](docs/NOTES.md) | FullSense Portal — Design Notes | - Brand neutrality — FullSense ™ is the parent; pinning the portal inside | 2026-05-19 | ❓ 要判断 |
| [PROGRESS.md](docs/PROGRESS.md) | FullSense Portal — Progress | ユーザー指示 5 連 (1 セッション後半): | 2026-05-27 | 🔒 内部? |
| [PROGRESS_archive_2026_05.md](docs/PROGRESS_archive_2026_05.md) | FullSense Portal — Progress Archive (Phase 0.4〜0.13 / 〜2026-05-21) | 取引(Alpaca)自動化 20 タスクを全 Disable（可逆）+ 取引プロセス停止 / Telegram を FullSense 状況 | 2026-05-27 | 🔒 内部? |
| [recommended-models.md](docs/recommended-models.md) | FullSense ™ — Recommended on-prem models | feedbackcompetitorbenchmark の 2026-05-16 progressive validation matrix | 2026-05-18 | ❓ 要判断 |
| [roadmap.md](docs/roadmap.md) | FullSense ™ — Roadmap | A "parked" product is a name + 1-line scope + trigger condition. It is not: | 2026-05-21 | ❓ 要判断 |
| [session_report_2026_05_24.md](docs/session_report_2026_05_24.md) | セッション報告書 — 2026-05-24 深夜（トレーサビリティ確保） | 1. 取引(Alpaca)自動化を全停止（無駄なリソースを FullSense へ委譲する方針に基づく）。 | 2026-05-24 | 🔒 内部? |
| [SESSION_SUMMARY.md](docs/SESSION_SUMMARY.md) | Session Summary — 2026-05-29〜30 (llcore S1/S2 + 進化機構監査 + CPU手順1 + 14proj health) | fullsense (umbrella) — D:\projects\fullsense / 主作業 = llcore (D:\projects\llcore) | 2026-05-30 | 🔒 内部? |
| [spinoff_ideas_2026_05.md](docs/spinoff_ideas_2026_05.md) | FullSense — Agent-Authored Spinoff & Concept Catalog (2026-05-19) | flowchart TD | 2026-05-20 | ❓ 要判断 |

<a id="g2"></a>

## docs/architecture (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [triz-ssm-vs-transformer.md](docs/architecture/triz-ssm-vs-transformer.md) | TRIZ 検討: SSM (Mamba) vs Transformer — FullSense (llive on-prem) 文脈 (draft v0.1) | 「Transformer は強い、でも長コンテキスト × on-prem には重い」という現象は | 2026-05-18 | ❓ 要判断 |

<a id="g3"></a>

## docs/articles (42)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [MULTILINGUAL_ROLLOUT_SPEC.md](docs/articles/MULTILINGUAL_ROLLOUT_SPEC.md) | QIITA 24 series — 多言語 rollout spec (agent briefing) | 1. frontmatter (YAML): | 2026-05-23 | 🔒 内部? |
| [QIITA_#01_brief_api_progressive.md](docs/articles/QIITA_#01_brief_api_progressive.md) | Brief API 設計と progressive matrix で見える llive の overhead < 1 % | - llive は OSS LLM (Ollama 経由の Qwen / Llama / Mistral) を 判断者ではなく素材生成者 として呼び出す上位フレームワーク | 2026-05-28 | 🔒 内部? |
| [QIITA_#02_cognitive_factors.md](docs/articles/QIITA_#02_cognitive_factors.md) | 「心理の深層」10 因子で整理する llive 思考層 — 既に 9/10 実装済 | - 「心理の深層」YouTube から抽出された 10 思考因子 (構造化・再構成・閉ループ・自己拡張・不確実性・探索・整合・来歴・多視点・現実接続) を llive 既存 FR にマッピング | 2026-05-28 | ❓ 要判断 |
| [QIITA_#03_math_vertical.md](docs/articles/QIITA_#03_math_vertical.md) | 数学・単位に強い AI を作る最初の一歩 — MATH-01/08 内蔵計算エンジン | - llive 最初の specialised vertical として「数学・単位特化 AI」を選定 (ユーザー戦略指示) | 2026-05-28 | ❓ 要判断 |
| [QIITA_#04_next_cabt_block_design.md](docs/articles/QIITA_#04_next_cabt_block_design.md) | Transformer ブロックを高度化する 7 つのアプローチ — CABT 設計予告 | - Transformer の softmax(QK^T)·V は値そのものを混合する → 付加情報 (provenance / trust / epistemictype) を持たせる場所がない | 2026-05-28 | ❓ 要判断 |
| [QIITA_#05_next_creat_kj_mindmap.md](docs/articles/QIITA_#05_next_creat_kj_mindmap.md) | LLM × KJ法 × MindMap で要件定義を自動化する — CREAT 設計予告 | - 現在の LLM (GPT / Claude / Gemini) は 収束的思考が得意 (input → answer) だが、拡散的思考は弱い | 2026-05-28 | ❓ 要判断 |
| [QIITA_#06_next_math02_formal_gate.md](docs/articles/QIITA_#06_next_math02_formal_gate.md) | LLM 数式幻覚をどう止めるか — 形式検証ゲート (MATH-02 設計予告) | - LLM が出力した数式は文字列としては妥当でも、等式として偽であることが多い | 2026-05-28 | ❓ 要判断 |
| [QIITA_#07_bench_results.md](docs/articles/QIITA_#07_bench_results.md) | llive vs 他 LLM ベンチマーク 2026-05-17 — 動作確認の罠と honest disclosure | - 同日実装した Brief API end-to-end の動作確認を兼ね 4 brief × 6 model でベンチ走行 | 2026-05-28 | ❓ 要判断 |
| [QIITA_#08_quiz_bench_debug_vs_release.md](docs/articles/QIITA_#08_quiz_bench_debug_vs_release.md) | Quiz bench Debug vs Release 比較 — 統計指標付き 10 問テスト | - ユーザー指示「DebugMode と Release 版でベンチマークテストして」「クイズ形式 + 平均値・分散値」を反映 | 2026-05-28 | ❓ 要判断 |
| [QIITA_#09_llive_structure_originality.md](docs/articles/QIITA_#09_llive_structure_originality.md) | llive の構造は LLM として独自になっているか — 8 つの差別化要素の点検 | これは LoRA / adapter の延長線にあるが、「重みを更新しないことで replay 可能 / monitorable な学習軌跡」を最優先にしている点が独自。CABT (S2 で計画中) では forward hook で attention に bias を加えるが、これも重み凍結のまま。 | 2026-05-28 | ❓ 要判断 |
| [QIITA_#10_qwen_divergence_strategy.md](docs/articles/QIITA_#10_qwen_divergence_strategy.md) | Qwen 依存から離脱する 5 段階ロードマップ — llive の独自性をコアに移植する | - 現状の llive (v0.6) は 周辺認知 OS としては独自だが、LLM コアは Qwen / Llama / Mistral に依存 している | 2026-05-28 | 🔒 内部? |
| [QIITA_#11_complementary_with_qwen.md](docs/articles/QIITA_#11_complementary_with_qwen.md) | Qwen と相互補完する llive — Local 環境で『隙間』を埋める設計 | - 前記事 10(./QIITA%2310qwendivergencestrategy.md) で「Qwen から離脱する 5 段階」を提示したが、完全離脱だけが path ではない | 2026-05-28 | ❓ 要判断 |
| [QIITA_#12_dev_history.md](docs/articles/QIITA_#12_dev_history.md) | llive 開発履歴 — 5 日で v0.1 から v0.7 候補へ | llive (リブ) は 2026-05-13 に発足した自己進化型 LLM フレームワーク。本記事は 発足から本日 (2026-05-17) までの 5 日間で何をどう作り、何で躓き、何を学んだか を時系列でまとめたものです。 | 2026-05-28 | ❓ 要判断 |
| [QIITA_#13_corpus_first_advantage.md](docs/articles/QIITA_#13_corpus_first_advantage.md) | コーパス先行戦略 — AI が私の気づかない観点を思考フローに補完する優位性 | - 本日のセッションを通じて気づいた AI 協働開発の本質的優位性 | 2026-05-28 | ❓ 要判断 |
| [QIITA_#14_invisible_annotation_channel.md](docs/articles/QIITA_#14_invisible_annotation_channel.md) | HTML で見えないのに、機械では読める。— llive が採用した「不可視アノテーションチャネル」設計 | ある日、SNS にこんなコメントが届いた。「3 つのプロダクトが相互依存していたら、1 つだけ使う価値が半減するよね」。返答は コメントアウト だった — <!-- llive:cog.consensus="proceed" --。 | 2026-05-27 | ❓ 要判断 |
| [QIITA_#15_second_brain_spiral_dev.md](docs/articles/QIITA_#15_second_brain_spiral_dev.md) | 30 年のソフトウェア開発経験 + Perplexity 要約 + Claude Code + TRIZ + 5 万件の論文 RAG = 「第二の脳」 | 1 人開発で 5 日間に Brief API・OKA-FX・VRB-FX・IND-04 アノテーション・MathVerifier を含む 14 機能と 256 テストを追加し、1270 件全 PASS で回帰ゼロを達成した。秘訣は「第二の脳」をどう組み立てるかにある。 | 2026-05-27 | ❓ 要判断 |
| [QIITA_#16_three_self_spirit_ai_management.md](docs/articles/QIITA_#16_three_self_spirit_ai_management.md) | 「三自の精神」を AI に課す — 圧倒的成果を出し続けるマネジャー流の AI 運用論 | 要件を 消化しきる前に次の要件を積み続けられる。これは人間チームでは破綻するが AI 開発では優位性になる。条件は 1 つ — AI が 自律して動いてくれる こと。キヤノンが掲げる「三自の精神」と、Buckingham & Coffman 等のマネジメント書籍がほぼそのまま転用できる。 | 2026-05-27 | ❓ 要判断 |
| [QIITA_#17_human_ai_fusion_vision.md](docs/articles/QIITA_#17_human_ai_fusion_vision.md) | Will Caster と Andrew NDR114 が目指したもの — llive のビジョン論 | LinkedIn のプロフィール画像を、自分の顔とロボットを画像生成 AI で融合した一枚にしている。冗談ではない。いずれ AI と人が融合できたら面白いと本気で考えている。その第一歩としての llive。 | 2026-05-27 | ❓ 要判断 |
| [QIITA_#18_non_transformer_low_spec_pc.md](docs/articles/QIITA_#18_non_transformer_low_spec_pc.md) | 「GPU の無い、私の古いノート PC」を主役にする LLM フレームワークを本気で作る話 | FullSense 3 層と non-transformer backend の関係: | 2026-05-27 | ❓ 要判断 |
| [QIITA_#19_general_gpu_less_ai_for_everyone.md](docs/articles/QIITA_#19_general_gpu_less_ai_for_everyone.md) | GPU の無い、私のあの古いノート PC でも動く AI を、本気で作っている話 | 今日の話の地図 (2 つの世界を並べると): | 2026-05-27 | ❓ 要判断 |
| [QIITA_#20_one_session_full_stack_progress.md](docs/articles/QIITA_#20_one_session_full_stack_progress.md) | 1 セッションで 5409 テスト緑 + research hub 6 本開設 — FullSense の一日 | 1 セッションで以下を達成した: | 2026-05-27 | 🔒 内部? |
| [QIITA_#21_three_day_marathon_2026_05_18_to_20.md](docs/articles/QIITA_#21_three_day_marathon_2026_05_18_to_20.md) | <!-- | Qiita タグは 5 個上限. 本記事の主役順で: | 2026-05-27 | ❓ 要判断 |
| [QIITA_#22_transformer_escape_status.md](docs/articles/QIITA_#22_transformer_escape_status.md) | <!-- | Qiita タグ 5 個上限. 本記事の主役順: | 2026-05-27 | ❓ 要判断 |
| [QIITA_#23_15h_marathon_mid_report.md](docs/articles/QIITA_#23_15h_marathon_mid_report.md) | <!-- | Qiita タグ 5 個上限. 本記事の主役順: | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_00_llive_tech_series_index.md](docs/articles/QIITA_#24_00_llive_tech_series_index.md) | ﻿--- | organizationurlname: null | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_01_memory_layer.md](docs/articles/QIITA_#24_01_memory_layer.md) | ﻿--- | organizationurlname: null | 2026-05-27 | 🔒 内部? |
| [QIITA_#24_02_thought_factors_cog_mesh.md](docs/articles/QIITA_#24_02_thought_factors_cog_mesh.md) | ﻿--- | organizationurlname: null | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_03_structural_evolution_triz.md](docs/articles/QIITA_#24_03_structural_evolution_triz.md) | ﻿--- | organizationurlname: null | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_04_convergent_optimization_b_series.md](docs/articles/QIITA_#24_04_convergent_optimization_b_series.md) | ﻿--- | organizationurlname: null | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_05_evolutionary_v0BCDE.md](docs/articles/QIITA_#24_05_evolutionary_v0BCDE.md) | ﻿--- | organizationurlname: null | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_06_llm_backend_non_transformer.md](docs/articles/QIITA_#24_06_llm_backend_non_transformer.md) | ﻿--- | organizationurlname: null | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_07_observability_governance.md](docs/articles/QIITA_#24_07_observability_governance.md) | ﻿--- | organizationurlname: null | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_08_lleval_eval_framework.md](docs/articles/QIITA_#24_08_lleval_eval_framework.md) | ﻿--- | organizationurlname: null | 2026-05-27 | ❓ 要判断 |
| [QIITA_#24_LINK_MAP.md](docs/articles/QIITA_#24_LINK_MAP.md) | QIITA Series — Cross-link URL mapping (投稿後に埋める) | — | 2026-05-28 | ❓ 要判断 |
| [QIITA_#25_monoculture_evolution_lldarwin.md](docs/articles/QIITA_#25_monoculture_evolution_lldarwin.md) | ⚠ 本記事は ja 素案 (骨子 + 書き出しドラフト)。en/zh/ko 展開は後続。投稿前に hero/theme SVG・進捗 badge・cross-link URL を埋める。 | 要するに 「全員 100 点のテストで席次を決めようとした」。そりゃ誰が | 2026-05-27 | ❓ 要判断 |
| [QIITA_#26_lldarwin_multi_pressure_selection.md](docs/articles/QIITA_#26_lldarwin_multi_pressure_selection.md) | ⚠ 本記事は ja 本文ドラフト（蓄積目的）。投稿前に hero/theme SVG・進捗 badge・25/24-08/27 の Qiita URL cross-link を埋める。en/zh/ko 展開は後続。 | 落語には本題の前に「枕」があります。まずは三行で全体像を。 | 2026-05-26 | ❓ 要判断 |
| [QIITA_#27_lldarwin_v2_overnight_marathon.md](docs/articles/QIITA_#27_lldarwin_v2_overnight_marathon.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | 落語には本題の前に「枕」があります。まずは三行で。 | 2026-05-28 | ❓ 要判断 |
| [QIITA_evolution_arc_lldarwin_complete.md](docs/articles/QIITA_evolution_arc_lldarwin_complete.md) | 日本語 | まずは全体像を。本記事は連載 25・26・27 を 1 本に統合した完全版で、物語は三幕です。 | 2026-05-26 | ❓ 要判断 |
| [QIITA_llive_mega_evolution.md](docs/articles/QIITA_llive_mega_evolution.md) | 個人開発AIのlliveが"メガ進化"！ | 個人開発している AI、llive を進化させてみたら——8 系統が 2 系統まで激減して大失敗。 | 2026-05-26 | ❓ 要判断 |
| [QIITA_POST_GUIDE.md](docs/articles/QIITA_POST_GUIDE.md) | Qiita 投稿準備ガイド | QIITA20onesessionfullstackprogress.md は Jekyll 用 frontmatter | 2026-05-23 | ❓ 要判断 |
| [QIITA_SERIES_INDEX.md](docs/articles/QIITA_SERIES_INDEX.md) | Qiita 連載インデックス (1〜31) | — | 2026-05-28 | ❓ 要判断 |
| [QIITA_WEEKLY_DIGEST_2026-05-17_to_24.md](docs/articles/QIITA_WEEKLY_DIGEST_2026-05-17_to_24.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | 2026-05-17、私は 1 セッションで自己進化型 LLM フレームワーク | 2026-05-24 | ❓ 要判断 |

<a id="g4"></a>

## docs/articles/2026-05-17 (29)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [01_brief_api_progressive.md](docs/articles/2026-05-17/01_brief_api_progressive.md) | Brief API 設計と progressive matrix で見える llive の overhead < 1 % | - llive は OSS LLM (Ollama 経由の Qwen / Llama / Mistral) を 判断者ではなく素材生成者 として呼び出す上位フレームワーク | 2026-05-24 | 🔒 内部? |
| [02_cognitive_factors.md](docs/articles/2026-05-17/02_cognitive_factors.md) | 「心理の深層」10 因子で整理する llive 思考層 — 既に 9/10 実装済 | - 「心理の深層」YouTube から抽出された 10 思考因子 (構造化・再構成・閉ループ・自己拡張・不確実性・探索・整合・来歴・多視点・現実接続) を llive 既存 FR にマッピング | 2026-05-24 | ❓ 要判断 |
| [03_math_vertical.md](docs/articles/2026-05-17/03_math_vertical.md) | 数学・単位に強い AI を作る最初の一歩 — MATH-01/08 内蔵計算エンジン | - llive 最初の specialised vertical として「数学・単位特化 AI」を選定 (ユーザー戦略指示) | 2026-05-24 | ❓ 要判断 |
| [04_next_cabt_block_design.md](docs/articles/2026-05-17/04_next_cabt_block_design.md) | Transformer ブロックを高度化する 7 つのアプローチ — CABT 設計予告 | - Transformer の softmax(QK^T)·V は値そのものを混合する → 付加情報 (provenance / trust / epistemictype) を持たせる場所がない | 2026-05-24 | ❓ 要判断 |
| [05_next_creat_kj_mindmap.md](docs/articles/2026-05-17/05_next_creat_kj_mindmap.md) | LLM × KJ法 × MindMap で要件定義を自動化する — CREAT 設計予告 | - 現在の LLM (GPT / Claude / Gemini) は 収束的思考が得意 (input → answer) だが、拡散的思考は弱い | 2026-05-17 | ❓ 要判断 |
| [06_next_math02_formal_gate.md](docs/articles/2026-05-17/06_next_math02_formal_gate.md) | LLM 数式幻覚をどう止めるか — 形式検証ゲート (MATH-02 設計予告) | - LLM が出力した数式は文字列としては妥当でも、等式として偽であることが多い | 2026-05-17 | ❓ 要判断 |
| [07_bench_results.md](docs/articles/2026-05-17/07_bench_results.md) | llive vs 他 LLM ベンチマーク 2026-05-17 — 動作確認の罠と honest disclosure | - 同日実装した Brief API end-to-end の動作確認を兼ね 4 brief × 6 model でベンチ走行 | 2026-05-24 | ❓ 要判断 |
| [08_quiz_bench_debug_vs_release.md](docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md) | Quiz bench Debug vs Release 比較 — 統計指標付き 10 問テスト | - ユーザー指示「DebugMode と Release 版でベンチマークテストして」「クイズ形式 + 平均値・分散値」を反映 | 2026-05-24 | ❓ 要判断 |
| [09_llive_structure_originality.md](docs/articles/2026-05-17/09_llive_structure_originality.md) | llive の構造は LLM として独自になっているか — 8 つの差別化要素の点検 | これは LoRA / adapter の延長線にあるが、「重みを更新しないことで replay 可能 / monitorable な学習軌跡」を最優先にしている点が独自。CABT (S2 で計画中) では forward hook で attention に bias を加えるが、これも重み凍結のまま。 | 2026-05-24 | ❓ 要判断 |
| [10_qwen_divergence_strategy.md](docs/articles/2026-05-17/10_qwen_divergence_strategy.md) | Qwen 依存から離脱する 5 段階ロードマップ — llive の独自性をコアに移植する | - 現状の llive (v0.6) は 周辺認知 OS としては独自だが、LLM コアは Qwen / Llama / Mistral に依存 している | 2026-05-24 | 🔒 内部? |
| [11_complementary_with_qwen.md](docs/articles/2026-05-17/11_complementary_with_qwen.md) | Qwen と相互補完する llive — Local 環境で『隙間』を埋める設計 | - 前記事 10({{ '/articles/2026-05-17/10qwendivergencestrategy' \| relativeurl }}) で「Qwen から離脱する 5 段階」を提示したが、完全離脱だけが path ではない | 2026-05-24 | ❓ 要判断 |
| [12_dev_history.md](docs/articles/2026-05-17/12_dev_history.md) | llive 開発履歴 — 5 日で v0.1 から v0.7 候補へ | llive (リブ) は 2026-05-13 に発足した自己進化型 LLM フレームワーク。本記事は 発足から本日 (2026-05-17) までの 5 日間で何をどう作り、何で躓き、何を学んだか を時系列でまとめたものです。 | 2026-05-17 | ❓ 要判断 |
| [13_corpus_first_advantage.md](docs/articles/2026-05-17/13_corpus_first_advantage.md) | コーパス先行戦略 — AI が私の気づかない観点を思考フローに補完する優位性 | - 本日のセッションを通じて気づいた AI 協働開発の本質的優位性 | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_GENERAL_en.md](docs/articles/2026-05-17/LinkedIn_GENERAL_en.md) | LinkedIn Post — 2026-05-17 General Audience (English) | 🤖 From "just using AI" to "giving AI a secretary" — FullSense, the local-first AI framework | 2026-05-17 | 🔒 内部? |
| [LinkedIn_GENERAL_jp.md](docs/articles/2026-05-17/LinkedIn_GENERAL_jp.md) | LinkedIn 投稿 — 2026-05-17 一般向け (日本語版) | 🤖 AI を「使うだけ」から「AI に秘書を付ける」へ — 自宅 PC で動くおせっかい AI フレームワーク llive | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_GENERAL_ko.md](docs/articles/2026-05-17/LinkedIn_GENERAL_ko.md) | LinkedIn 게시물 — 2026-05-17 일반 청중 (한국어판) | 🤖 AI 를 「쓰기만」에서 「AI 에게 비서를 붙이기」로 — Local PC 에서 동작하는 책임감 있는 AI 프레임워크 FullSense | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_GENERAL_zh.md](docs/articles/2026-05-17/LinkedIn_GENERAL_zh.md) | LinkedIn 投稿 — 2026-05-17 大众向 (简体中文版) | 🤖 从"只是使用 AI"到"给 AI 配秘书" — 在本地 PC 上运行的负责任 AI 框架 FullSense | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_HISTORY_en.md](docs/articles/2026-05-17/LinkedIn_HISTORY_en.md) | LinkedIn Post — 2026-05-17 Project History (English) | 📜 llmesh → llove → llive — Development history and design concepts of the FullSense triad | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_HISTORY_jp.md](docs/articles/2026-05-17/LinkedIn_HISTORY_jp.md) | LinkedIn 投稿 — 2026-05-17 開発履歴版 (日本語版) | 📜 llmesh → llove → llive — FullSense 3 製品の開発履歴と設計コンセプト | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_HISTORY_ko.md](docs/articles/2026-05-17/LinkedIn_HISTORY_ko.md) | LinkedIn 게시물 — 2026-05-17 프로젝트 이력 (한국어판) | 📜 llmesh → llove → llive — FullSense 3 제품의 개발 이력 및 설계 컨셉 | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_HISTORY_zh.md](docs/articles/2026-05-17/LinkedIn_HISTORY_zh.md) | LinkedIn 投稿 — 2026-05-17 项目历史版 (简体中文版) | 📜 llmesh → llove → llive — FullSense 三个产品的开发历史和设计理念 | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_SUMMARY_en.md](docs/articles/2026-05-17/LinkedIn_SUMMARY_en.md) | LinkedIn Post — 2026-05-17 Engineering Summary (English) | 🚀 32 requirements + 2,200 LoC + 78 tests + 4 benchmarks in a single day — Building llive, a self-evolving modular memory LLM framework | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_SUMMARY_jp.md](docs/articles/2026-05-17/LinkedIn_SUMMARY_jp.md) | LinkedIn 投稿 — 2026-05-17 技術者向け統合 (日本語版) | 🚀 1 日で要件 32 件 + 実装 2200 行 + テスト 78 件 + ベンチ 4 種 — 自己進化型 LLM フレームワーク llive 開発記 | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_SUMMARY_ko.md](docs/articles/2026-05-17/LinkedIn_SUMMARY_ko.md) | LinkedIn 게시물 — 2026-05-17 엔지니어 요약 (한국어판) | 🚀 하루 만에 요구사항 32건 + 코드 2,200줄 + 테스트 78건 + 벤치마크 4종 — 자기 진화형 모듈식 메모리 LLM 프레임워크 llive 개발기 | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_SUMMARY_zh.md](docs/articles/2026-05-17/LinkedIn_SUMMARY_zh.md) | LinkedIn 投稿 — 2026-05-17 工程师向 (简体中文版) | 🚀 一天内完成 32 项需求 + 2,200 行代码 + 78 项测试 + 4 种基准测试 — 自进化型模块化记忆 LLM 框架 llive 开发记录 | 2026-05-17 | ❓ 要判断 |
| [QIITA_GENERAL.md](docs/articles/2026-05-17/QIITA_GENERAL.md) | AI を『使うだけ』から『AI に秘書を付ける』へ — 自宅 PC で動くおせっかい AI フレームワーク llive 開発日記 | 最近、ChatGPT や Claude、Gemini など、便利な AI が次々と出てきました。仕事の文章を書かせたり、コードを書かせたり、子どもの宿題のヒントを聞いたり、ちょっとした調べ物に使ったり。 | 2026-05-17 | ❓ 要判断 |
| [QIITA_HISTORY.md](docs/articles/2026-05-17/QIITA_HISTORY.md) | llmesh → llove → llive — FullSense 3 製品の開発履歴・設計コンセプト・差別化・普及戦略 (2026-05-17 時点) | 私 (古瀬 和文 / ぷるやん) は FullSense ™ という umbrella ブランドで 3 つの OSS プロジェクトを並走開発しています: | 2026-05-17 | ❓ 要判断 |
| [QIITA_SUMMARY.md](docs/articles/2026-05-17/QIITA_SUMMARY.md) | 1 日で要件 32 件追加 + Brief API + COG-FX + MATH 実装 + ベンチ 4 種 — 自己進化型 LLM フレームワーク llive 開発記 2026-05-17 | 2026-05-17 の 1 セッション (Claude Opus 4.7 1M context, ccr 経由) で 自己進化型 LLM フレームワーク llive(https://github.com/furuse-kazufumi/llive) に対し以下を達成しました: | 2026-05-24 | ❓ 要判断 |
| [README.md](docs/articles/2026-05-17/README.md) | FullSense — 2026-05-17 articles index | このディレクトリは「最新公開資料の集約場所」として運用します。 | 2026-05-24 | 🌐 公開候補 |

<a id="g5"></a>

## docs/articles/2026-05-18 (6)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [Eight_BIO_addition_jp.md](docs/articles/2026-05-18/Eight_BIO_addition_jp.md) | Eight 名刺プロフィール — 自己紹介文への追記案 | 趣味で OSS の LLM フレームワーク llive を 1 人開発中。Apache 2.0。 | 2026-05-17 | ❓ 要判断 |
| [LinkedIn_SECOND_BRAIN_SERIES_jp.md](docs/articles/2026-05-18/LinkedIn_SECOND_BRAIN_SERIES_jp.md) | LinkedIn 投稿文 — 「第二の脳」シリーズ統合版 (4 部) | LinkedIn のコメント 1 通が、HTML コメントへの着地になった話 — 「llive の各層が相互依存していたら、1 つだけ使う価値は半減する」。 | 2026-05-17 | ❓ 要判断 |
| [POST_CHEATSHEET.md](docs/articles/2026-05-18/POST_CHEATSHEET.md) | 投稿 cheat-sheet — QIITA18 / QIITA19 を Qiita Web UI に投稿する手順 | (タイトル行と「 投稿時の推奨タグ」以降は含めない) | 2026-05-22 | ❓ 要判断 |
| [QIITA_OBSERVATION_GROUNDING_jp.md](docs/articles/2026-05-18/QIITA_OBSERVATION_GROUNDING_jp.md) | 実 Brief 6 件で MATH grounding を観察したら、1 セッションで 6 周のバグ修正サイクルが回った | (1.38e-23  300) をボルツマン定数 × 300 K として grounded 化したいだけだったのに、観察スクリプトが「23  300 = 6,900」と出してきた。指数表記の regex バグが 1 件目。そこから 6 周のサイクルで 1,270 → 1,314 PASS、UNKNOWN unit 0 件、TRIZ 偽陽性 0 件まで辿り着いた話。 | 2026-05-17 | ❓ 要判断 |
| [QIITA_SECOND_BRAIN_SERIES.md](docs/articles/2026-05-18/QIITA_SECOND_BRAIN_SERIES.md) | 「第二の脳」シリーズ — llive 全景 × 不可視 Annotation × 構築論 × 運用論 × ビジョン論 × 実装の深層 | 1 人開発で 5 日間に 14 機能・256 テストを追加し、1,276 件全 PASS で回帰ゼロ を達成した。LinkedIn のコメント 1 通から HTML コメントへの着地、Perplexity と TRIZ と 5 万件論文コーパスの組み合わせ、キヤノン「三自の精神」を AI に課す運用、そして Will Caster と Andrew NDR114 のビジョン — 6 部構成で公開す | 2026-05-22 | ❓ 要判断 |
| [QIITA_USV_jp.md](docs/articles/2026-05-18/QIITA_USV_jp.md) | CSV/TSV の後継を作りました — USV (Unit-Separated Values) で AI ⇄ 人間の表データ通信を楽にする | タブ幅 4 vs 8 の戦争に、60 年前の ASCII が予約していた U+001F を再活性化することで終止符を打ちました。Markdown も HTML も改行もタブもセル内に直接書ける。AI と人間の表データ通信が確実に楽になります。 | 2026-05-17 | ❓ 要判断 |

<a id="g6"></a>

## docs/articles/2026-05-20 (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [README.md](docs/articles/2026-05-20/README.md) | FullSense — 2026-05-20 articles index | spinoff 採用優先度を決定 → portal NEXTSESSION 自動化 → lleval v0.1 | 2026-05-22 | 🌐 公開候補 |

<a id="g7"></a>

## docs/articles/2026-05-21 (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [_appendix_2026_05_22_harness_vibe.md](docs/articles/2026-05-21/_appendix_2026_05_22_harness_vibe.md) | <!-- | 共通追補テンプレート (2026-05-22 セッション末). 各 QIITA 記事の末尾に | 2026-05-22 | ❓ 要判断 |

<a id="g8"></a>

## docs/articles/2026-05-22 (3)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [LinkedIn_2026-05-22_harness_vibe_session.md](docs/articles/2026-05-22/LinkedIn_2026-05-22_harness_vibe_session.md) | LinkedIn 投稿文 — 2026-05-22 ハーネス型バイブコーディング (日本語版) | 「Claude Code に 進めます と宣言させたのが、今日の試合の半分。 残り半分は、私が harness を握り続けた時間でした。」 | 2026-05-22 | ❓ 要判断 |
| [LinkedIn_2026-05-22_qiita_14_15_announce.md](docs/articles/2026-05-22/LinkedIn_2026-05-22_qiita_14_15_announce.md) | LinkedIn 投稿 — Qiita 連載 14 / 15 投稿告知 | Qiita 連載「FullSense / llive 完全解説」のドラフトを公開し始めました。 全 20 本の予定で、今日は 14 と 15 が走りました。 | 2026-05-22 | ❓ 要判断 |
| [LinkedIn_2026-05-22_rust_marathon.md](docs/articles/2026-05-22/LinkedIn_2026-05-22_rust_marathon.md) | LinkedIn 投稿文 — 2026-05-22 FullSense 進捗 (4 言語版) | FullSense マラソン (2026-05-22) — llive Rust 高速化と「Rust 化 = 速い」の嘘 | 2026-05-24 | ❓ 要判断 |

<a id="g9"></a>

## docs/articles/2026-05-23 (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [INTEGRATION_AUDIT.md](docs/articles/2026-05-23/INTEGRATION_AUDIT.md) | 2026-05-23 — FullSense 系 cross-project 整合性監査 (silent 自律セッション) | baseline で全 15 プロジェクトを並列スキャンした結果: | 2026-05-23 | 🔒 内部? |

<a id="g10"></a>

## docs/articles/archive/2026-05-17 (29)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [01_brief_api_progressive.md](docs/articles/archive/2026-05-17/01_brief_api_progressive.md) | Brief API 設計と progressive matrix で見える llive の overhead < 1 % | - llive は OSS LLM (Ollama 経由の Qwen / Llama / Mistral) を 判断者ではなく素材生成者 として呼び出す上位フレームワーク | 2026-05-27 | 🔒 内部? |
| [02_cognitive_factors.md](docs/articles/archive/2026-05-17/02_cognitive_factors.md) | 「心理の深層」10 因子で整理する llive 思考層 — 既に 9/10 実装済 | - 「心理の深層」YouTube から抽出された 10 思考因子 (構造化・再構成・閉ループ・自己拡張・不確実性・探索・整合・来歴・多視点・現実接続) を llive 既存 FR にマッピング | 2026-05-27 | ❓ 要判断 |
| [03_math_vertical.md](docs/articles/archive/2026-05-17/03_math_vertical.md) | 数学・単位に強い AI を作る最初の一歩 — MATH-01/08 内蔵計算エンジン | - llive 最初の specialised vertical として「数学・単位特化 AI」を選定 (ユーザー戦略指示) | 2026-05-27 | ❓ 要判断 |
| [04_next_cabt_block_design.md](docs/articles/archive/2026-05-17/04_next_cabt_block_design.md) | Transformer ブロックを高度化する 7 つのアプローチ — CABT 設計予告 | - Transformer の softmax(QK^T)·V は値そのものを混合する → 付加情報 (provenance / trust / epistemictype) を持たせる場所がない | 2026-05-27 | ❓ 要判断 |
| [05_next_creat_kj_mindmap.md](docs/articles/archive/2026-05-17/05_next_creat_kj_mindmap.md) | LLM × KJ法 × MindMap で要件定義を自動化する — CREAT 設計予告 | - 現在の LLM (GPT / Claude / Gemini) は 収束的思考が得意 (input → answer) だが、拡散的思考は弱い | 2026-05-27 | ❓ 要判断 |
| [06_next_math02_formal_gate.md](docs/articles/archive/2026-05-17/06_next_math02_formal_gate.md) | LLM 数式幻覚をどう止めるか — 形式検証ゲート (MATH-02 設計予告) | - LLM が出力した数式は文字列としては妥当でも、等式として偽であることが多い | 2026-05-27 | ❓ 要判断 |
| [07_bench_results.md](docs/articles/archive/2026-05-17/07_bench_results.md) | llive vs 他 LLM ベンチマーク 2026-05-17 — 動作確認の罠と honest disclosure | - 同日実装した Brief API end-to-end の動作確認を兼ね 4 brief × 6 model でベンチ走行 | 2026-05-27 | ❓ 要判断 |
| [08_quiz_bench_debug_vs_release.md](docs/articles/archive/2026-05-17/08_quiz_bench_debug_vs_release.md) | Quiz bench Debug vs Release 比較 — 統計指標付き 10 問テスト | - ユーザー指示「DebugMode と Release 版でベンチマークテストして」「クイズ形式 + 平均値・分散値」を反映 | 2026-05-27 | ❓ 要判断 |
| [09_llive_structure_originality.md](docs/articles/archive/2026-05-17/09_llive_structure_originality.md) | llive の構造は LLM として独自になっているか — 8 つの差別化要素の点検 | これは LoRA / adapter の延長線にあるが、「重みを更新しないことで replay 可能 / monitorable な学習軌跡」を最優先にしている点が独自。CABT (S2 で計画中) では forward hook で attention に bias を加えるが、これも重み凍結のまま。 | 2026-05-27 | ❓ 要判断 |
| [10_qwen_divergence_strategy.md](docs/articles/archive/2026-05-17/10_qwen_divergence_strategy.md) | Qwen 依存から離脱する 5 段階ロードマップ — llive の独自性をコアに移植する | - 現状の llive (v0.6) は 周辺認知 OS としては独自だが、LLM コアは Qwen / Llama / Mistral に依存 している | 2026-05-27 | 🔒 内部? |
| [11_complementary_with_qwen.md](docs/articles/archive/2026-05-17/11_complementary_with_qwen.md) | Qwen と相互補完する llive — Local 環境で『隙間』を埋める設計 | - 前記事 10({{ '/articles/2026-05-17/10qwendivergencestrategy' \| relativeurl }}) で「Qwen から離脱する 5 段階」を提示したが、完全離脱だけが path ではない | 2026-05-27 | ❓ 要判断 |
| [12_dev_history.md](docs/articles/archive/2026-05-17/12_dev_history.md) | llive 開発履歴 — 5 日で v0.1 から v0.7 候補へ | llive (リブ) は 2026-05-13 に発足した自己進化型 LLM フレームワーク。本記事は 発足から本日 (2026-05-17) までの 5 日間で何をどう作り、何で躓き、何を学んだか を時系列でまとめたものです。 | 2026-05-27 | ❓ 要判断 |
| [13_corpus_first_advantage.md](docs/articles/archive/2026-05-17/13_corpus_first_advantage.md) | コーパス先行戦略 — AI が私の気づかない観点を思考フローに補完する優位性 | - 本日のセッションを通じて気づいた AI 協働開発の本質的優位性 | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_GENERAL_en.md](docs/articles/archive/2026-05-17/LinkedIn_GENERAL_en.md) | LinkedIn Post — 2026-05-17 General Audience (English) | 🤖 From "just using AI" to "giving AI a secretary" — FullSense, the local-first AI framework | 2026-05-27 | 🔒 内部? |
| [LinkedIn_GENERAL_jp.md](docs/articles/archive/2026-05-17/LinkedIn_GENERAL_jp.md) | LinkedIn 投稿 — 2026-05-17 一般向け (日本語版) | 🤖 AI を「使うだけ」から「AI に秘書を付ける」へ — 自宅 PC で動くおせっかい AI フレームワーク llive | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_GENERAL_ko.md](docs/articles/archive/2026-05-17/LinkedIn_GENERAL_ko.md) | LinkedIn 게시물 — 2026-05-17 일반 청중 (한국어판) | 🤖 AI 를 「쓰기만」에서 「AI 에게 비서를 붙이기」로 — Local PC 에서 동작하는 책임감 있는 AI 프레임워크 FullSense | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_GENERAL_zh.md](docs/articles/archive/2026-05-17/LinkedIn_GENERAL_zh.md) | LinkedIn 投稿 — 2026-05-17 大众向 (简体中文版) | 🤖 从"只是使用 AI"到"给 AI 配秘书" — 在本地 PC 上运行的负责任 AI 框架 FullSense | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_HISTORY_en.md](docs/articles/archive/2026-05-17/LinkedIn_HISTORY_en.md) | LinkedIn Post — 2026-05-17 Project History (English) | 📜 llmesh → llove → llive — Development history and design concepts of the FullSense triad | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_HISTORY_jp.md](docs/articles/archive/2026-05-17/LinkedIn_HISTORY_jp.md) | LinkedIn 投稿 — 2026-05-17 開発履歴版 (日本語版) | 📜 llmesh → llove → llive — FullSense 3 製品の開発履歴と設計コンセプト | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_HISTORY_ko.md](docs/articles/archive/2026-05-17/LinkedIn_HISTORY_ko.md) | LinkedIn 게시물 — 2026-05-17 프로젝트 이력 (한국어판) | 📜 llmesh → llove → llive — FullSense 3 제품의 개발 이력 및 설계 컨셉 | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_HISTORY_zh.md](docs/articles/archive/2026-05-17/LinkedIn_HISTORY_zh.md) | LinkedIn 投稿 — 2026-05-17 项目历史版 (简体中文版) | 📜 llmesh → llove → llive — FullSense 三个产品的开发历史和设计理念 | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_SUMMARY_en.md](docs/articles/archive/2026-05-17/LinkedIn_SUMMARY_en.md) | LinkedIn Post — 2026-05-17 Engineering Summary (English) | 🚀 32 requirements + 2,200 LoC + 78 tests + 4 benchmarks in a single day — Building llive, a self-evolving modular memory LLM framework | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_SUMMARY_jp.md](docs/articles/archive/2026-05-17/LinkedIn_SUMMARY_jp.md) | LinkedIn 投稿 — 2026-05-17 技術者向け統合 (日本語版) | 🚀 1 日で要件 32 件 + 実装 2200 行 + テスト 78 件 + ベンチ 4 種 — 自己進化型 LLM フレームワーク llive 開発記 | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_SUMMARY_ko.md](docs/articles/archive/2026-05-17/LinkedIn_SUMMARY_ko.md) | LinkedIn 게시물 — 2026-05-17 엔지니어 요약 (한국어판) | 🚀 하루 만에 요구사항 32건 + 코드 2,200줄 + 테스트 78건 + 벤치마크 4종 — 자기 진화형 모듈식 메모리 LLM 프레임워크 llive 개발기 | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_SUMMARY_zh.md](docs/articles/archive/2026-05-17/LinkedIn_SUMMARY_zh.md) | LinkedIn 投稿 — 2026-05-17 工程师向 (简体中文版) | 🚀 一天内完成 32 项需求 + 2,200 行代码 + 78 项测试 + 4 种基准测试 — 自进化型模块化记忆 LLM 框架 llive 开发记录 | 2026-05-27 | ❓ 要判断 |
| [QIITA_GENERAL.md](docs/articles/archive/2026-05-17/QIITA_GENERAL.md) | AI を『使うだけ』から『AI に秘書を付ける』へ — 自宅 PC で動くおせっかい AI フレームワーク llive 開発日記 | 最近、ChatGPT や Claude、Gemini など、便利な AI が次々と出てきました。仕事の文章を書かせたり、コードを書かせたり、子どもの宿題のヒントを聞いたり、ちょっとした調べ物に使ったり。 | 2026-05-27 | ❓ 要判断 |
| [QIITA_HISTORY.md](docs/articles/archive/2026-05-17/QIITA_HISTORY.md) | llmesh → llove → llive — FullSense 3 製品の開発履歴・設計コンセプト・差別化・普及戦略 (2026-05-17 時点) | 私 (古瀬 和文 / ぷるやん) は FullSense ™ という umbrella ブランドで 3 つの OSS プロジェクトを並走開発しています: | 2026-05-27 | ❓ 要判断 |
| [QIITA_SUMMARY.md](docs/articles/archive/2026-05-17/QIITA_SUMMARY.md) | 1 日で要件 32 件追加 + Brief API + COG-FX + MATH 実装 + ベンチ 4 種 — 自己進化型 LLM フレームワーク llive 開発記 2026-05-17 | 2026-05-17 の 1 セッション (Claude Opus 4.7 1M context, ccr 経由) で 自己進化型 LLM フレームワーク llive(https://github.com/furuse-kazufumi/llive) に対し以下を達成しました: | 2026-05-27 | ❓ 要判断 |
| [README.md](docs/articles/archive/2026-05-17/README.md) | FullSense — 2026-05-17 articles index | このディレクトリは「最新公開資料の集約場所」として運用します。 | 2026-05-27 | 🌐 公開候補 |

<a id="g11"></a>

## docs/articles/archive/2026-05-18 (6)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [Eight_BIO_addition_jp.md](docs/articles/archive/2026-05-18/Eight_BIO_addition_jp.md) | Eight 名刺プロフィール — 自己紹介文への追記案 | 趣味で OSS の LLM フレームワーク llive を 1 人開発中。Apache 2.0。 | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_SECOND_BRAIN_SERIES_jp.md](docs/articles/archive/2026-05-18/LinkedIn_SECOND_BRAIN_SERIES_jp.md) | LinkedIn 投稿文 — 「第二の脳」シリーズ統合版 (4 部) | LinkedIn のコメント 1 通が、HTML コメントへの着地になった話 — 「llive の各層が相互依存していたら、1 つだけ使う価値は半減する」。 | 2026-05-27 | ❓ 要判断 |
| [POST_CHEATSHEET.md](docs/articles/archive/2026-05-18/POST_CHEATSHEET.md) | 投稿 cheat-sheet — QIITA18 / QIITA19 を Qiita Web UI に投稿する手順 | (タイトル行と「 投稿時の推奨タグ」以降は含めない) | 2026-05-27 | ❓ 要判断 |
| [QIITA_OBSERVATION_GROUNDING_jp.md](docs/articles/archive/2026-05-18/QIITA_OBSERVATION_GROUNDING_jp.md) | 実 Brief 6 件で MATH grounding を観察したら、1 セッションで 6 周のバグ修正サイクルが回った | (1.38e-23  300) をボルツマン定数 × 300 K として grounded 化したいだけだったのに、観察スクリプトが「23  300 = 6,900」と出してきた。指数表記の regex バグが 1 件目。そこから 6 周のサイクルで 1,270 → 1,314 PASS、UNKNOWN unit 0 件、TRIZ 偽陽性 0 件まで辿り着いた話。 | 2026-05-27 | ❓ 要判断 |
| [QIITA_SECOND_BRAIN_SERIES.md](docs/articles/archive/2026-05-18/QIITA_SECOND_BRAIN_SERIES.md) | 「第二の脳」シリーズ — llive 全景 × 不可視 Annotation × 構築論 × 運用論 × ビジョン論 × 実装の深層 | 1 人開発で 5 日間に 14 機能・256 テストを追加し、1,276 件全 PASS で回帰ゼロ を達成した。LinkedIn のコメント 1 通から HTML コメントへの着地、Perplexity と TRIZ と 5 万件論文コーパスの組み合わせ、キヤノン「三自の精神」を AI に課す運用、そして Will Caster と Andrew NDR114 のビジョン — 6 部構成で公開す | 2026-05-27 | ❓ 要判断 |
| [QIITA_USV_jp.md](docs/articles/archive/2026-05-18/QIITA_USV_jp.md) | CSV/TSV の後継を作りました — USV (Unit-Separated Values) で AI ⇄ 人間の表データ通信を楽にする | タブ幅 4 vs 8 の戦争に、60 年前の ASCII が予約していた U+001F を再活性化することで終止符を打ちました。Markdown も HTML も改行もタブもセル内に直接書ける。AI と人間の表データ通信が確実に楽になります。 | 2026-05-27 | ❓ 要判断 |

<a id="g12"></a>

## docs/articles/archive/pre-numbered (6)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [_appendix_2026_05_22_harness_vibe.md](docs/articles/archive/pre-numbered/_appendix_2026_05_22_harness_vibe.md) | <!-- | 共通追補テンプレート (2026-05-22 セッション末). 各 QIITA 記事の末尾に | 2026-05-27 | ❓ 要判断 |
| [INTEGRATION_AUDIT.md](docs/articles/archive/pre-numbered/INTEGRATION_AUDIT.md) | 2026-05-23 — FullSense 系 cross-project 整合性監査 (silent 自律セッション) | baseline で全 15 プロジェクトを並列スキャンした結果: | 2026-05-27 | 🔒 内部? |
| [LinkedIn_2026-05-22_harness_vibe_session.md](docs/articles/archive/pre-numbered/LinkedIn_2026-05-22_harness_vibe_session.md) | LinkedIn 投稿文 — 2026-05-22 ハーネス型バイブコーディング (日本語版) | 「Claude Code に 進めます と宣言させたのが、今日の試合の半分。 残り半分は、私が harness を握り続けた時間でした。」 | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_2026-05-22_qiita_14_15_announce.md](docs/articles/archive/pre-numbered/LinkedIn_2026-05-22_qiita_14_15_announce.md) | LinkedIn 投稿 — Qiita 連載 14 / 15 投稿告知 | Qiita 連載「FullSense / llive 完全解説」のドラフトを公開し始めました。 全 20 本の予定で、今日は 14 と 15 が走りました。 | 2026-05-27 | ❓ 要判断 |
| [LinkedIn_2026-05-22_rust_marathon.md](docs/articles/archive/pre-numbered/LinkedIn_2026-05-22_rust_marathon.md) | LinkedIn 投稿文 — 2026-05-22 FullSense 進捗 (4 言語版) | FullSense マラソン (2026-05-22) — llive Rust 高速化と「Rust 化 = 速い」の嘘 | 2026-05-27 | ❓ 要判断 |
| [README.md](docs/articles/archive/pre-numbered/README.md) | FullSense — 2026-05-20 articles index | spinoff 採用優先度を決定 → portal NEXTSESSION 自動化 → lleval v0.1 | 2026-05-27 | 🌐 公開候補 |

<a id="g13"></a>

## docs/articles/assets/lldarwin_2026_05_26 (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [INDEX.md](docs/articles/assets/lldarwin_2026_05_26/INDEX.md) | lldarwin 可視化素材カタログ (2026-05-26) | - proxy 系 (stage1, reservoir, reinjectsweep, stage2proxyaxes): rich-proxy / | 2026-05-26 | 🌐 公開候補 |

<a id="g14"></a>

## docs/articles/drafts (6)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [QIITA_#28_lldarwin_v2_phase1_orchestra.md](docs/articles/drafts/QIITA_#28_lldarwin_v2_phase1_orchestra.md) | ⚠️ DRAFT — 連載番号は portal 整理で確定（lldarwin アーク 25→26→27→本記事=実装編）。多言語版（en/zh/ko）は ja 確定後に展開。 | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English (TODO) \| 中文 (TODO) \| 한국어 (TODO) | 2026-05-27 | 🔒 内部? |
| [QIITA_#29_falsification_goodhart_proxy_limits.md](docs/articles/drafts/QIITA_#29_falsification_goodhart_proxy_limits.md) | ⚠ 本記事は ja 本文ドラフト（蓄積目的）。en/zh/ko 展開は後続。投稿前に hero/theme SVG・進捗 badge・25/26 の Qiita URL cross-link を埋める。 | - 眼鏡（fitness）が飽和すると、どんな高級な選択圧（lldarwin）を足しても淘汰は無力になる（25 の真の教訓）。 | 2026-05-28 | 🔒 内部? |
| [QIITA_#30_evolution_visualization_history.md](docs/articles/drafts/QIITA_#30_evolution_visualization_history.md) | ⚠ 本記事は ja 骨子ドラフト（蓄積目的・完璧不要）。en/zh/ko 展開は後続。投稿前に hero/theme SVG・進捗 badge・関連記事の Qiita URL cross-link を埋める。 | 進化は 長時間・大集団・多世代の現象。数字の羅列では「何が起きたか」が掴めません。 | 2026-05-28 | 🔒 内部? |
| [QIITA_#31_codex_two_pillar_orchestration.md](docs/articles/drafts/QIITA_#31_codex_two_pillar_orchestration.md) | ⚠ 本記事は ja 骨子ドラフト（蓄積目的・完璧不要）。en/zh/ko 展開は後続。投稿前に hero/theme SVG・進捗 badge・関連記事の Qiita URL cross-link を埋める。 | - Claude = オーケストレータ（計画・実装・委任・検証）/ Codex = 配下 worker（実行・レビュー・調査）。 | 2026-05-28 | 🔒 内部? |
| [QIITA_#32_llcore_cpu_poc_battery.md](docs/articles/drafts/QIITA_#32_llcore_cpu_poc_battery.md) | (連載 32) llcore CPU PoC battery 完成 | - Transformer の コア計算 (state update / 学習則 / 認知駆動 Δ) を進化対象にする研究フレームワーク llcore (PyPI: llmesh-llcore 0.1.0a0, llive 独立路線) の CPU PoC battery 完成 | 2026-05-28 | 🔒 内部? |
| [SERIES_PLAN_#25_onwards_evolution_arc.md](docs/articles/drafts/SERIES_PLAN_#25_onwards_evolution_arc.md) | 連載シリーズ計画 — 25 以降「進化アーク」 | 連載 24 が「llive を構成する技術の名称別解説」（静的な構造）だったのに対し、 | 2026-05-27 | 🔒 内部? |

<a id="g15"></a>

## docs/benchmarks (8)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [2026-05-16_llive_llm_validation.md](docs/benchmarks/2026-05-16_llive_llm_validation.md) | llive LLM Validation Report (2026-05-16) | - ✅ FullSenseLoop.innermonologue now wires to llive.llm.OllamaBackend | 2026-05-16 | ❓ 要判断 |
| [2026-05-16_lltrade_yaml.md](docs/benchmarks/2026-05-16_lltrade_yaml.md) | Benchmark — 2026-05-16 lltrade strategy YAML | Same shape as B1/B2/B3 — no LLM call, no generation. Tracked as | 2026-05-16 | ❓ 要判断 |
| [2026-05-16_mermaid_brief.md](docs/benchmarks/2026-05-16_mermaid_brief.md) | Benchmark — 2026-05-16 Mermaid Brief | Stored at docs/benchmarks/2026-05-16/brief.txt. Raw responses under the | 2026-05-16 | ❓ 要判断 |
| [2026-05-16_progressive_llive.md](docs/benchmarks/2026-05-16_progressive_llive.md) | Benchmark — 2026-05-16 llive Progressive Token Stress | Stored under docs/benchmarks/2026-05-16-progressive/{xs,s,m,l,xl}/brief.txt, | 2026-05-16 | 🔒 内部? |
| [2026-05-16_quickstart_seqdiag.md](docs/benchmarks/2026-05-16_quickstart_seqdiag.md) | Benchmark — 2026-05-16 Quick Start + SeqDiag | To get started with lldesign, first install the required packages by | 2026-05-16 | ❓ 要判断 |
| [2026-05-16_vlm.md](docs/benchmarks/2026-05-16_vlm.md) | Benchmark — 2026-05-16 Vision LM (og-card description) | — the FullSense Open Graph card with the umbrella title, the | 2026-05-16 | ❓ 要判断 |
| [PLAN_progressive_model_brief.md](docs/benchmarks/PLAN_progressive_model_brief.md) | Plan — llive Progressive Model × Brief Benchmark | 20-25 cells. Execute in row-major order (model size ↑, then brief size ↑ | 2026-05-16 | 🔒 内部? |
| [policy.md](docs/benchmarks/policy.md) | FullSense ™ — Benchmark Policy | ベンチに 3 つの不変原則を置く。逸脱した結果は honest disclosure | 2026-05-18 | 🔒 内部? |

<a id="g16"></a>

## docs/benchmarks/2026-05-16-matrix (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [matrix_summary.md](docs/benchmarks/2026-05-16-matrix/matrix_summary.md) | llive Model x Brief Matrix Summary | Generated: 2026-05-16 | 2026-05-16 | ❓ 要判断 |

<a id="g17"></a>

## docs/benchmarks/2026-05-16-quiz-debug (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [quiz_summary.md](docs/benchmarks/2026-05-16-quiz-debug/quiz_summary.md) | Quiz Reasoning Benchmark | Generated: 2026-05-16 \| mode: debug \| debug=True | 2026-05-16 | ❓ 要判断 |

<a id="g18"></a>

## docs/benchmarks/2026-05-16-quiz-release (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [quiz_summary.md](docs/benchmarks/2026-05-16-quiz-release/quiz_summary.md) | Quiz Reasoning Benchmark | Generated: 2026-05-16 \| mode: release \| debug=False | 2026-05-16 | ❓ 要判断 |

<a id="g19"></a>

## docs/benchmarks/2026-05-17-quiz-debug (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [quiz_summary.md](docs/benchmarks/2026-05-17-quiz-debug/quiz_summary.md) | Quiz Reasoning Benchmark | Generated: 2026-05-17 \| mode: debug \| debug=True | 2026-05-17 | ❓ 要判断 |

<a id="g20"></a>

## docs/benchmarks/2026-05-17-quiz-release (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [quiz_summary.md](docs/benchmarks/2026-05-17-quiz-release/quiz_summary.md) | Quiz Reasoning Benchmark | Generated: 2026-05-17 \| mode: release \| debug=False | 2026-05-17 | ❓ 要判断 |

<a id="g21"></a>

## docs/design (2)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [acceleration_poc_technical_report_2026_05_24.md](docs/design/acceleration_poc_technical_report_2026_05_24.md) | 高速化候補 PoC 技術報告書 (2026-05-24) | (feedbackpocfeasibilityfirst)。採用は「網羅」でなく「選別」、現状構造を破綻させない | 2026-05-24 | ❓ 要判断 |
| [f25-phase-h-e2e.md](docs/design/f25-phase-h-e2e.md) | F25 Phase h — llove ↔ llmesh ↔ llive E2E 設計 (draft v0.2) | 3 製品 (llmesh / llive / llove) を MCP プロトコル経由で接続し、ユーザが | 2026-05-18 | ❓ 要判断 |

<a id="g22"></a>

## docs/papers (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [2026-05-27_continuously_evolving_orchestra_open_ended.md](docs/papers/2026-05-27_continuously_evolving_orchestra_open_ended.md) | Continuously-Evolving Populations as Live Orchestrated Ensembles | Date of record (priority): 2026-05-27 | 2026-05-27 | ❓ 要判断 |

<a id="g23"></a>

## docs/regulatory (7)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [audit-log-format.md](docs/regulatory/audit-log-format.md) | 監査ログ仕様 (Audit Log Format Specification, draft v0.3) | 各国 AI 規制 (中国 AI 弁法 / EU AI Act / 日本金融庁 AI ディスカッションペーパー / | 2026-05-18 | 🔒 内部? |
| [cn-internal-use.en.md](docs/regulatory/cn-internal-use.en.md) | China's Generative AI Regulation — Internal Use Pattern (operational docs, draft v0.1) | This document summarises how the following PRC regulations apply when an | 2026-05-18 | 🔒 内部? |
| [cn-internal-use.md](docs/regulatory/cn-internal-use.md) | 中国生成式 AI 規制と社内利用パターン (运用 documentation, draft v0.1) | 本ドキュメントは、以下の中国法規における「公衆向けサービスでない社内利用」の | 2026-05-17 | 🔒 内部? |
| [cn-internal-use.zh.md](docs/regulatory/cn-internal-use.zh.md) | 中国生成式 AI 监管 — 内部使用模式 (运维文档, draft v0.1) | 本文档梳理企业内部 (非面向公众) 部署 FullSense (llmesh / llive / llove) | 2026-05-18 | 🔒 内部? |
| [cn-public-service.md](docs/regulatory/cn-public-service.md) | 中国生成 AI 弁法 — 公衆向けサービス filing 手順 (draft v0.2) | → 社内専用利用は filing 不要. 詳細は cn-internal-use.md 参照. | 2026-05-18 | ❓ 要判断 |
| [data-sovereignty.md](docs/regulatory/data-sovereignty.md) | データ越境 / データ主権 運用 documentation (draft v0.2) | AI サービス / LLM 推論において、入力 / 学習データ / 出力データの越境移転を | 2026-05-18 | ❓ 要判断 |
| [eu-ai-act.md](docs/regulatory/eu-ai-act.md) | EU AI Act 対応運用 documentation (draft v0.2) | EU AI Act (Regulation (EU) 2024/1689) は 2024 年 8 月発効、段階的施行: | 2026-05-18 | ❓ 要判断 |

<a id="g24"></a>

## docs/research (42)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [acceleration_poc_matrix_2026_05_24.md](docs/research/acceleration_poc_matrix_2026_05_24.md) | 高速化候補 全 PoC 判定マトリクス (2026-05-24) | すべて simulation / toy 環境 であり実測ハードウェアではない (honest disclosure)。 | 2026-05-24 | ❓ 要判断 |
| [cognitive_mesh_vs_sota.md](docs/research/cognitive_mesh_vs_sota.md) | llive Cognitive Mesh v0.8 vs SOTA LLM Agent Memory (2026-05-20) | 1. On-prem first — MemGPT / Generative Agents は cloud LLM 前提. | 2026-05-20 | ❓ 要判断 |
| [evolution_design_tensions_open_decisions_2026_05_25.md](docs/research/evolution_design_tensions_open_decisions_2026_05_25.md) | 進化設計の緊張関係 & 未解決決定 (2026-05-25) | - 上記 T1–T8 の解決方針が要件本体に反映され、D1–D9 が「sweep で決める/初期値」まで落ちていること。 | 2026-05-25 | ❓ 要判断 |
| [evolution_fitness_redesign_2026_05_25.md](docs/research/evolution_fitness_redesign_2026_05_25.md) | 進化 fitness 再設計 (2026-05-25) | 500 世代 proxy run (llive out/evorun20260525, genome3d, seed 2, pop 32) の実測: | 2026-05-25 | ❓ 要判断 |
| [evolution_poc_deployment_results_2026_05_25.md](docs/research/evolution_poc_deployment_results_2026_05_25.md) | 開放端進化 PoC デプロイ結果 (2026-05-25) | 標準化 novelty 選択は多様性を持続、scalar 選択は崩壊: | 2026-05-25 | ❓ 要判断 |
| [evolution_poc_experiment_design_2026_05_25.md](docs/research/evolution_poc_experiment_design_2026_05_25.md) | 開放端進化 PoC 実験設計 (2026-05-25) | 「新しい AI を生む環境」の本体は 探索空間（search） と 効果空間（effect） の分離: | 2026-05-25 | ❓ 要判断 |
| [evolution_research_algorithm_survey_2026_05_25.md](docs/research/evolution_research_algorithm_survey_2026_05_25.md) | 進化研究 — 広域アルゴリズムサーベイ & 適合評価 (Stream G) | 我々の系の制約は他の進化系と質的に異なる。評価はこの 5 軸で行う: | 2026-05-25 | ❓ 要判断 |
| [evolution_research_competitive_sota_2026_05_25.md](docs/research/evolution_research_competitive_sota_2026_05_25.md) | Evolution Research — Competitive / State-of-the-Art Landscape (Stream F) | stream F の射程は「最適化」ではなく 「生成・自己改善・開放端」. 3 系統に分ける: | 2026-05-25 | ❓ 要判断 |
| [evolution_research_culture_learning_2026_05_25.md](docs/research/evolution_research_culture_learning_2026_05_25.md) | Evolution Research — Stream D: Culture & Learning (Cultural Algorithms / Baldwin / Human-Factor Genome) | - 学習層の背骨 = Reynolds Cultural Algorithm (1994) の belief space。5 知識源 (normative / situational / domain / temporal / spatial) + acceptance 関数 (上位個体が belief を更新) + influence 関数 (belief が変異を誘導)。これが 9 「best | 2026-05-25 | ❓ 要判断 |
| [evolution_research_meta_2026_05_25.md](docs/research/evolution_research_meta_2026_05_25.md) | Meta-Evolution — 進化アルゴリズム自体を進化させる (Research Stream A) | 挙動に結線する dispatch 層 と、メタ層を「進化」させた時に必ず起きる病理（mutation rate→0 collapse / | 2026-05-25 | ❓ 要判断 |
| [evolution_research_openendedness_2026_05_25.md](docs/research/evolution_research_openendedness_2026_05_25.md) | Evolution Research — Stream B: Open-Endedness & Quality-Diversity | — | 2026-05-25 | ❓ 要判断 |
| [evolution_research_representation_selection_2026_05_25.md](docs/research/evolution_research_representation_selection_2026_05_25.md) | Evolution Research — Stream C: Genome Representation & Selection Schemes | The user's principle 4/10 has a concrete failure already latent in the code: | 2026-05-25 | 🔒 内部? |
| [evolution_research_safety_2026_05_25.md](docs/research/evolution_research_safety_2026_05_25.md) | AI Safety for Open-Ended / Evolved Agents — Research Stream E | 3 つが同時に成立しなければならない、という TRIZ 的矛盾： | 2026-05-25 | ❓ 要判断 |
| [evolution_visualization_advanced_2026_05_25.md](docs/research/evolution_visualization_advanced_2026_05_25.md) | 進化可視化の高度化 — 3DGS 時系列 + 魅せ方史（2026-05-25） | FullSense は現在「計測（グラフ）」段階。目標は「多様性の地図化 + 体験」（系統・個体・3DGS）。 | 2026-05-25 | ❓ 要判断 |
| [evolution_visualization_plan_2026_05_25.md](docs/research/evolution_visualization_plan_2026_05_25.md) | 進化ラン可視化 計画 (2026-05-25) | 1. 適応度トラジェクトリ: best/mean/median + std バンド / 世代。「改善しているか」の核。 | 2026-05-25 | ❓ 要判断 |
| [evolution_viz_viewing_guide_2026_05_25.md](docs/research/evolution_viz_viewing_guide_2026_05_25.md) | 進化ラン可視化 — 成果物カタログと閲覧ガイド (2026-05-25) | - SVG (グラフ/系統 stream) → モダンブラウザ (Edge/Chrome) で開く。.svg の既定が | 2026-05-25 | 🔒 内部? |
| [gemini_brainstorm_impl_2026_05_24.md](docs/research/gemini_brainstorm_impl_2026_05_24.md) | Gemini ブレスト 3/4 実装着地メモ (2026-05-24) | 分散版。3 は「予測誤差 (高 surprise) を学習トリガに変える」= 予測誤差を捨てずに活かす。 | 2026-05-24 | 🔒 内部? |
| [ideation_marathon_expression_realtime_2026_05_23.md](docs/research/ideation_marathon_expression_realtime_2026_05_23.md) | FullSense「表現 × リアルタイム」ideation marathon | - 既知の課題（前セッション）: llmesh は前半(センサ→SPC)のみ real-time、後半(LLM説明+push)が gap。あらゆる表現の根は llmesh の表現汎用層で、manga-SVG/llove SVG/記事埋込は consumer。 | 2026-05-23 | 🔒 内部? |
| [index.md](docs/research/index.md) | Research Notes | — | 2026-05-28 | 🌐 公開候補 |
| [llcore_cpu_poc_battery_completion_2026_05_29.md](docs/research/llcore_cpu_poc_battery_completion_2026_05_29.md) | llcore CPU PoC Battery 完成 — Stage 0-2 全 PoC 完走 | Transformer のコアアルゴリズム (state update / 学習則 / 認知駆動 Δ) に進化形態を与え、Z3 verifier で破綻させずに 異アルゴリズムへ進化させる研究フレームワーク llcore の CPU PoC battery が Stage 0-2 完走。 | 2026-05-28 | 🔒 内部? |
| [llcraft_sota.md](docs/research/llcraft_sota.md) | llcraft — On-prem Creative Material Generation OSS SOTA (2026-05-20) | cloud 依存 (ElevenLabs / Kling 等を内部呼出). on-prem で TTS+画像+動画+音楽を | 2026-05-20 | ❓ 要判断 |
| [lldarwin_stage1_results_2026_05_26.md](docs/research/lldarwin_stage1_results_2026_05_26.md) | lldarwin Stage1 — 実測結果と honest disclosure (2026-05-26) | 1. criteria 除外 (DEFAULTEXCLUDEDCRITERIA): factorscore (= max-archetype の | 2026-05-26 | ❓ 要判断 |
| [lldarwin_v2_ops_readiness_2026_05_27.md](docs/research/lldarwin_v2_ops_readiness_2026_05_27.md) | lldarwin v2 — 本格実装 / 連続稼働 readiness 計画 (2026-05-27) | - Phase 1（選択核 S1 合成配線）= Agent C 実装中（--selection lldarwin-v2 opt-in, 既定 off, テスト付）。 | 2026-05-27 | ❓ 要判断 |
| [lldarwin_v2_poc_marathon_2026_05_26.md](docs/research/lldarwin_v2_poc_marathon_2026_05_26.md) | lldarwin v2 — overnight PoC マラソン台帳 (2026-05-26 → 翌朝) | 12h 実 LLM 進化ラン out/lldarwin12hrealpressure20260526 の分析: | 2026-05-27 | ❓ 要判断 |
| [lleval_sota.md](docs/research/lleval_sota.md) | lleval — SOTA Survey (2026-05-20) | GPT-4 judge は人間と 80%+ 一致するが、 | 2026-05-20 | ❓ 要判断 |
| [llgov_sota.md](docs/research/llgov_sota.md) | llgov — AI Governance / Compliance SOTA (2026-05-20) | - EU AI Act Art.9-15 (risk mgmt / data gov / logging / transparency / | 2026-05-20 | ❓ 要判断 |
| [llgrow_prior_art.md](docs/research/llgrow_prior_art.md) | llgrow — Prior Art Survey (2026-05-20) | Jasper / copy.ai / ContentBot は LLM テンプレートと人手レビューを組合せる | 2026-05-20 | ❓ 要判断 |
| [llm_evolutionary_prior_art.md](docs/research/llm_evolutionary_prior_art.md) | LLM × Evolutionary Algorithms — Prior Art Survey | ユーザー指示 (2026-05-21): 「LLM に進化的形質を持たせるとか, 既に研究と | 2026-05-21 | ❓ 要判断 |
| [llname_collision_audit_2026_05_24.md](docs/research/llname_collision_audit_2026_05_24.md) | ll- ファミリー名 衝突監査 + PyPI 予約 (2026-05-24) | bare llmesh (PyPI / GitHub) は Hewlett Packard (HPE) が保有: | 2026-05-25 | 🔒 内部? |
| [llove_qt_gui_architecture_2026_05_25.md](docs/research/llove_qt_gui_architecture_2026_05_25.md) | llove Qt GUI / OS-like Front — アーキテクチャ設計 (Research Stream H) | - Textual TUI。llove/app.py の LoveApp(App) が複数ペインをホストし、DataSource.stream() | 2026-05-25 | 🔒 内部? |
| [llrepr_poc_2026_05_24.md](docs/research/llrepr_poc_2026_05_24.md) | llrepr — PoC 実装着地メモ (2026-05-24) | 旧仮称 "RepIR" は既存 OSS と頭字語が衝突していた: | 2026-05-24 | ❓ 要判断 |
| [llrisk_prior_art.md](docs/research/llrisk_prior_art.md) | llrisk — Continuous AI Risk Tracking Prior Art (2026-05-20) | ServiceNow は 2025 に AI Control Tower + AI Agent Fabric を投入し, AI agent の | 2026-05-20 | ❓ 要判断 |
| [mythos_competitor_spec_2026_05_27.md](docs/research/mythos_competitor_spec_2026_05_27.md) | 競合スペック台帳 — Claude Mythos (2026-05-27) | - Anthropic のフロンティアモデル。コードネーム Capybara。Opus ティアの上位。 | 2026-05-27 | 🔒 内部? |
| [mythos_surpass_design_2026_05_27.md](docs/research/mythos_surpass_design_2026_05_27.md) | 設計正本 — 進化型オーケストラで Claude Mythos を超える (セキュリティ領域, 2026-05-27) | 決定論的セキュリティオラクルがある検証可能タスクでは、弱い on-prem モデルでも「進化で多様化した生成 × 無制限 test-time サンプリング × オラクル選別」でフロンティア級カバレッジに到達できる。 | 2026-05-28 | ❓ 要判断 |
| [mythos_surpass_status_2026_05_28.md](docs/research/mythos_surpass_status_2026_05_28.md) | Mythos 超え — 機構実証と gap の honest 中間報告 (2026-05-28) | - 検証 = precision: RAPTOR の 決定論オラクル（flag 一致 / exploit 成立 / crash 再現 / ASan・UBSan）が「効く 1 答」を機械判定。 | 2026-05-28 | ❓ 要判断 |
| [openended_evo_sota_perplexity_2026_05_26.md](docs/research/openended_evo_sota_perplexity_2026_05_26.md) | 開放端進化 SOTA サーベイ (Perplexity sonar-pro, 2026-05-26) | The methods you list all attack specific failures of objective-driven search (deception, premature convergence, mode-collapse in behavior space, misspecification of fitness) by explicitly rewarding no | 2026-05-26 | ❓ 要判断 |
| [persona_ontology_expansion_2026_05_24.md](docs/research/persona_ontology_expansion_2026_05_24.md) | ペルソナ ontology 拡張 — affinity 自動算出 (ハードコード排除) | 1. 最初に拡張 7 名へ手で付けた factoraffinity (数値) を ユーザー指摘「ハードコードを疑え」で撤回。 | 2026-05-24 | 🔒 内部? |
| [predictive_push_poc_2026_05_24.md](docs/research/predictive_push_poc_2026_05_24.md) | 予測符号化 push PoC — 発見A の具現化 (2026-05-24) | 神経科学の予測符号化（予測を先に生成し、予測誤差だけを伝播）を、SPC アラーム説明に適用: | 2026-05-24 | ❓ 要判断 |
| [repir_mcp_compat_2026_05_23.md](docs/research/repir_mcp_compat_2026_05_23.md) | RepIR × 汎用 MCP ルーター互換性 設計メモ (2026-05-23) | 1. 独自 content type 案 ({type:"representation", ...}) は互換性が取れない。非推奨。 | 2026-05-24 | ❓ 要判断 |
| [spec_mesh_01_b1_feedback_2026_05_24.md](docs/research/spec_mesh_01_b1_feedback_2026_05_24.md) | SPEC-MESH-01 完遂 + B1 stale 訂正 + stdioserver 状態訂正 (2026-05-24) | 1. SPEC-MESH-01 完遂 — 分岐予測器 (Frequency / Markov) を実装し hitrate を | 2026-05-24 | ❓ 要判断 |
| [spec_mesh_prior_art_2026_05_24.md](docs/research/spec_mesh_prior_art_2026_05_24.md) | SPEC-MESH 先行研究調査 — 分散/branch-level speculative の被りと独自 (2026-05-24) | Actions)・「通信遅延→投機計算」(DSD)・acceptance-rate 依存 ROI — すべて 2025-2026 に先行研究あり。 | 2026-05-24 | 🔒 内部? |
| [spec_mesh_wiring_2026_05_25.md](docs/research/spec_mesh_wiring_2026_05_25.md) | Speculative Mesh 本格配線 (SPEC-MESH-02/03/04) + セキュリティ修正 (2026-05-25) | - SPEC-MESH-02 実 mesh transport: 派遣先 peer の endpoint を node registry で解決し、 | 2026-05-25 | ❓ 要判断 |

<a id="g25"></a>

## docs/spec (3)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [index.md](docs/spec/index.md) | FullSense ™ — Spec hub | 著者の苗字 Furuse (古瀬) に由来。さらに author given name Kazufumi | 2026-05-21 | 🌐 公開候補 |
| [lleval_v0_1_implementation_notes.md](docs/spec/lleval_v0_1_implementation_notes.md) | lleval — v0.1 Implementation Notes (2026-05-20 夜) | ┌─────────────────────────────────────┐ | 2026-05-21 | ❓ 要判断 |
| [requirements_lleval_v0.1_draft.md](docs/spec/requirements_lleval_v0.1_draft.md) | lleval — v0.1 Requirements Draft (2026-05-20) | - 依存方針 (feedback-independence-principle): | 2026-05-20 | 🔒 内部? |

<a id="g26"></a>

## docs/vision (8)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [hyperdimensional_connection_map.md](docs/vision/hyperdimensional_connection_map.md) | Hyperdimensional Thinking — FullSense 接続マップ & 採用方針 | - Hyperdimensional Thinking は シンギュラリティを起こすために必要な因子の「一つ」 である | 2026-05-24 | ❓ 要判断 |
| [HYPERDIMENSIONAL_THINKING.md](docs/vision/HYPERDIMENSIONAL_THINKING.md) | Hyperdimensional Thinking: 次世代AIの発想法のための開発指針 | 本ドキュメントは 開発実務のための指針(B) である。 | 2026-05-24 | ❓ 要判断 |
| [LLDARWIN_DESIGN.md](docs/vision/LLDARWIN_DESIGN.md) | lldarwin — 選択圧コンポーネント 設計書 (2026-05-25) | 1. 複数選択圧の多目的淘汰 — 単一スカラー fitness の argmax を禁止（旧 best=1.0 飽和の真因 = fitnessrich の nearest=max(sims) 単一化, 要件 SEL-2）。各個体は複数の独立した選択圧（pressure）で評価され、それらを集約せず個別に淘汰判定する。 | 2026-05-25 | ❓ 要判断 |
| [llive_north_star_architecture_2026_05_27.md](docs/vision/llive_north_star_architecture_2026_05_27.md) | llive 北極星アーキテクチャ — ブロック図と「矛盾→単純化」設計 (2026-05-27) | 連続進化 × ライブ MoA オーケストラ — 進化し続ける多様な個体集団を、答えが要る瞬間に competence-aware routing (指揮者) で合奏させ 1 答する。 | 2026-05-27 | ❓ 要判断 |
| [OPEN_ENDED_CULTURAL_EVOLUTION.md](docs/vision/OPEN_ENDED_CULTURAL_EVOLUTION.md) | 開放端・文化的進化 — 統合マスター設計 (Open-Ended Cultural Evolution) | 旧 proxyfitness = 0.7balance + 0.3provenance、cfactors(10×4) を層平均10次元に圧縮。 | 2026-05-25 | ❓ 要判断 |
| [OPEN_ENDED_EVOLUTION_REQUIREMENTS.md](docs/vision/OPEN_ENDED_EVOLUTION_REQUIREMENTS.md) | 開放端進化 AI 環境 — 要件定義 (Requirements Definition) | 進化ランが「新しい AI を生む」とは、次を同時に満たす個体が継続的に出現すること: | 2026-05-27 | ❓ 要判断 |
| [PERSONA_FX.md](docs/vision/PERSONA_FX.md) | PERSONA-FX: 文化的ペルソナ獲得レイヤ (未来計画スケルトン) | 現状の persona evolution は、persona の factoraffinity を gen0 founder の genome に書き込む | 2026-05-24 | ❓ 要判断 |
| [SINGULARITY_REQUIREMENTS.md](docs/vision/SINGULARITY_REQUIREMENTS.md) | Singularity Requirements: 次世代AIの認知拡張に関する要件定義(スケルトン) | 本書を正式な要件定義として立ち上げるかどうかは、以下が揃ったときに判断する: | 2026-05-24 | ❓ 要判断 |

<a id="g27"></a>

## tools/devto-publish (1)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [README.md](tools/devto-publish/README.md) | devto-publish | dev.to (DEV Community) への Markdown 記事自動投稿スクリプト。 | 2026-05-27 | 🌐 公開候補 |

<a id="g28"></a>

## tools/qiita-cli-poc (3)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [MIGRATION_GUIDE.md](tools/qiita-cli-poc/MIGRATION_GUIDE.md) | Qiita CLI 一括移行ガイド (FullSense 連載 ~18 記事) | @qiita/qiita-cli v1.8.0 (Apache-2.0, Node 20+) を使い、docs/articles/QIITA.md の | 2026-05-23 | ❓ 要判断 |
| [PUBLISH_PLAN_lldarwin_arc_2026_05_27.md](tools/qiita-cli-poc/PUBLISH_PLAN_lldarwin_arc_2026_05_27.md) | 投稿準備計画 — lldarwin アーク + バックログ (2026-05-27) | → 実バックログ = 25 / 27（+ 26 設計編）。14-24 は投稿済なので「溜まっている」のは実質この 3 本＋今後の新規。 | 2026-05-27 | ❓ 要判断 |
| [PUBLISH_PLAN_theme_fix.md](tools/qiita-cli-poc/PUBLISH_PLAN_theme_fix.md) | Publish Plan — 24-02 / 24-08 theme SVG 表示修正の Qiita 反映 | 1. SVG 側 (修正済 + push 済): | 2026-05-23 | 🔒 内部? |

<a id="g29"></a>

## tools/qiita-cli-poc/input_copies (2)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [QIITA_#16_three_self_spirit_ai_management.md](tools/qiita-cli-poc/input_copies/QIITA_#16_three_self_spirit_ai_management.md) | 「三自の精神」を AI に課す — 圧倒的成果を出し続けるマネジャー流の AI 運用論 | 要件を 消化しきる前に次の要件を積み続けられる。これは人間チームでは破綻するが AI 開発では優位性になる。条件は 1 つ — AI が 自律して動いてくれる こと。キヤノンが掲げる「三自の精神」と、Buckingham & Coffman 等のマネジメント書籍がほぼそのまま転用できる。 | 2026-05-22 | ❓ 要判断 |
| [QIITA_#20J_jekyll_synthetic.md](tools/qiita-cli-poc/input_copies/QIITA_#20J_jekyll_synthetic.md) | Jekyll 合成テスト記事 | これは Jekyll frontmatter (layout: default, permalink) を持つ合成記事で、 | 2026-05-23 | ❓ 要判断 |

<a id="g30"></a>

## tools/qiita-cli-poc/public (43)

| ファイル | タイトル | 説明 | 更新 | 区分 |
|---|---|---|---|---|
| [07b4882e872994b27b3c.md](tools/qiita-cli-poc/public/07b4882e872994b27b3c.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — llive 完全解説 9 本連載 (認知/最適化/実行/横断 4 層 × 8 章 animated)(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2400hero.svg) | 2026-05-29 | ❓ 要判断 |
| [07b686ea311e06027f94.md](tools/qiita-cli-poc/public/07b686ea311e06027f94.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — N=64 派生集団の世代を超えた fitness 進化(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2405hero.svg) | 2026-05-29 | ❓ 要判断 |
| [1e7af6bde0f9ffcbd913.md](tools/qiita-cli-poc/public/1e7af6bde0f9ffcbd913.md) | Will Caster と Andrew NDR114 が目指したもの — llive のビジョン論 | LinkedIn のプロフィール画像を、自分の顔とロボットを画像生成 AI で融合した一枚にしている。冗談ではない。いずれ AI と人が融合できたら面白いと本気で考えている。その第一歩としての llive。 | 2026-05-29 | ❓ 要判断 |
| [24ac90fb12c4e332d2b5.md](tools/qiita-cli-poc/public/24ac90fb12c4e332d2b5.md) | 0. 冒頭 hook | 15 時間 marathon で 7 件着地, 全件 credential / 外部 binary 不要の前倒し | 2026-05-29 | ❓ 要判断 |
| [25fd4cae8aed848d3a3c.md](tools/qiita-cli-poc/public/25fd4cae8aed848d3a3c.md) | AI を『使うだけ』から『AI に秘書を付ける』へ — 自宅 PC で動くおせっかい AI フレームワーク llive 開発日記 | 最近、ChatGPT や Claude、Gemini など、便利な AI が次々と出てきました。仕事の文章を書かせたり、コードを書かせたり、子どもの宿題のヒントを聞いたり、ちょっとした調べ物に使ったり。 | 2026-05-29 | ❓ 要判断 |
| [33b70c801894b91ca826.md](tools/qiita-cli-poc/public/33b70c801894b91ca826.md) | HTML で見えないのに、機械では読める。— llive が採用した「不可視アノテーションチャネル」設計 | ある日、SNS にこんなコメントが届いた。「3 つのプロダクトが相互依存していたら、1 つだけ使う価値が半減するよね」。返答は コメントアウト だった — <!-- llive:cog.consensus="proceed" --。 | 2026-05-29 | ❓ 要判断 |
| [3b49820306ea9e11666b.md](tools/qiita-cli-poc/public/3b49820306ea9e11666b.md) | 1 セッションで 5409 テスト緑 + research hub 6 本開設 — FullSense の一日 | 1 セッションで以下を達成した: | 2026-05-29 | ❓ 要判断 |
| [42a555f691ebc44cb040.md](tools/qiita-cli-poc/public/42a555f691ebc44cb040.md) | ローカル LLM × 産業 IoT × プロンプトファイアウォールを 1 つの Python フレームワークで — LLMesh v3.1.0 を作った話 | - LLMesh は、ローカル LLM（Ollama / llama.cpp）とクラウド LLM（OpenAI / Azure / Anthropic / OpenRouter / Groq / Together / Mistral / DeepSeek）を 同一 ABC で透過運用 できる Python 統合フレームワークです。 | 2026-05-29 | ❓ 要判断 |
| [4d94bde146b83b31d24c.md](tools/qiita-cli-poc/public/4d94bde146b83b31d24c.md) | 「三自の精神」を AI に課す — 圧倒的成果を出し続けるマネジャー流の AI 運用論 | 要件を 消化しきる前に次の要件を積み続けられる。これは人間チームでは破綻するが AI 開発では優位性になる。条件は 1 つ — AI が 自律して動いてくれる こと。キヤノンが掲げる「三自の精神」と、Buckingham & Coffman 等のマネジメント書籍がほぼそのまま転用できる。 | 2026-05-29 | ❓ 要判断 |
| [520193281514396d65c2.md](tools/qiita-cli-poc/public/520193281514396d65c2.md) | Modbus / OPC-UA / DNP3 / IEC 61850 GOOSE を 1 個の SensorEvent に流し込んで、CUSUM で異常を捕まえて LLM に説明させる — LLMesh 産業 IoT 編 | pip install "llmesh-mcpindustrial" | 2026-05-29 | ❓ 要判断 |
| [559e2d59b7646adb95bd.md](tools/qiita-cli-poc/public/559e2d59b7646adb95bd.md) | MCPで3D空間アセットを扱うための Spatial Asset Profile v2 を作った | 3Dデータや空間計測データを、LLMエージェントや外部ツールから扱いやすくするための試作仕様として、MCP Spatial Asset Profile Version 2.0 を公開しました。 | 2026-05-29 | ❓ 要判断 |
| [64fac910780f59ab61f9.md](tools/qiita-cli-poc/public/64fac910780f59ab61f9.md) | 1 日で要件 32 件追加 + Brief API + COG-FX + MATH 実装 + ベンチ 4 種 — 自己進化型 LLM フレームワーク llive 開発記 2026-05-17 | 2026-05-17 の 1 セッション (Claude Opus 4.7 1M context, ccr 経由) で 自己進化型 LLM フレームワーク llive(https://github.com/furuse-kazufumi/llive) に対し以下を達成しました: | 2026-05-29 | ❓ 要判断 |
| [6da5a883fb2ed651edd8.md](tools/qiita-cli-poc/public/6da5a883fb2ed651edd8.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — SSM state stream vs Transformer attention(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2406hero.svg) | 2026-05-29 | ❓ 要判断 |
| [6ea53d9ad19f60a23f07.md](tools/qiita-cli-poc/public/6ea53d9ad19f60a23f07.md) | LLM の「忘却」に正面から向き合う ― 4 層メモリ × 形式検証 × TRIZ 自演化 × Rust ホットパスを Python で実装した話 (llive v0.5.0) | - llive は、固定 LLM コアの周りに 4 層外部記憶 (semantic / episodic / structural / parameter) と 可変長 BlockContainer を配置し、コア重みを再学習せずに能力を継続的に取り込む Python フレームワーク。 | 2026-05-29 | ❓ 要判断 |
| [7c28cd65d25308e3a1b1.md](tools/qiita-cli-poc/public/7c28cd65d25308e3a1b1.md) | Pure Python の 6 倍速い Rust 拡張と、ストリーミング再送・HTTP DoS 対策まで詰め込んだ Python ライブラリ — LLMesh 性能と信頼性の話 | ポイントは 「Rust が無くても動く」。Rust 拡張は import に失敗したら 静かに Pure Python にフォールバック します（明示的に環境チェックをかけたいなら python -m llmesh.cli.doctor）。 | 2026-05-29 | ❓ 要判断 |
| [7fa693bc2f1ae43ba5ba.md](tools/qiita-cli-poc/public/7fa693bc2f1ae43ba5ba.md) | 0. 冒頭 hook — 「脱却した」と「default が脱却」のあいだに広がる谷 | 「Transformer から脱却した」と「default の実行経路が non-transformer」は | 2026-05-29 | ❓ 要判断 |
| [932c4cfc6cfca636504a.md](tools/qiita-cli-poc/public/932c4cfc6cfca636504a.md) | 「LLM 観測ダッシュボードを TUI で書く」設計の話 ― llove v0.3.0a1 (Textual / layout.toml / F25 連携基盤) | - llove は、LLMesh 系のデータ (SensorEvent / SPC / RAG / Audit / Trace + llive の BWT / routetrace / conceptupdate) を 1 枚のターミナル で観測する Textual ベースの TUI。 | 2026-05-29 | ❓ 要判断 |
| [93f3cf1bb7b14650bbca.md](tools/qiita-cli-poc/public/93f3cf1bb7b14650bbca.md) | ローカル LLM とクラウド LLM を「同じ書き方」で扱いたい人のための LLMesh — 30 秒で動かせる Python フレームワーク | pip install llmesh-mcp | 2026-05-29 | ❓ 要判断 |
| [951b94cf66d246723004.md](tools/qiita-cli-poc/public/951b94cf66d246723004.md) | LLM のプロンプトに「何を渡してよいか」を 4 層で統制する — LLMesh の Prompt Firewall を作った | pip install "llmesh-mcppresidio" | 2026-05-29 | ❓ 要判断 |
| [99e4558953df57ccaffb.md](tools/qiita-cli-poc/public/99e4558953df57ccaffb.md) | llmesh: ローカル LLM スウォーム × 産業 IoT × 研究自動化 | llmesh は、ローカル LLM (Ollama) ノード群を MCP | 2026-05-29 | ❓ 要判断 |
| [a5ebb3992e4c28862f47.md](tools/qiita-cli-poc/public/a5ebb3992e4c28862f47.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — 4 層メモリ + Bayesian surprise gate(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2401hero.svg) | 2026-05-29 | ❓ 要判断 |
| [ab3839f8b5b3ea91311e.md](tools/qiita-cli-poc/public/ab3839f8b5b3ea91311e.md) | 30 年のソフトウェア開発経験 + Perplexity 要約 + Claude Code + TRIZ + 5 万件の論文 RAG = 「第二の脳」 | 1 人開発で 5 日間に Brief API・OKA-FX・VRB-FX・IND-04 アノテーション・MathVerifier を含む 14 機能と 256 テストを追加し、1270 件全 PASS で回帰ゼロを達成した。秘訣は「第二の脳」をどう組み立てるかにある。 | 2026-05-29 | ❓ 要判断 |
| [ac398349ec42e40913f1.md](tools/qiita-cli-poc/public/ac398349ec42e40913f1.md) | LLMesh: Local LLMをMCPで安全につなぐP2P Swarm PoCを作った | Local LLMを複数台で協調させたい。しかし、秘密コードや社内ノウハウを外部ノードへ渡したくない。LLMeshはこの問題意識から作った、セキュリティファーストなLocal LLM SwarmのPoCです。 | 2026-05-29 | ❓ 要判断 |
| [aff262808a35cb7f7d3b.md](tools/qiita-cli-poc/public/aff262808a35cb7f7d3b.md) | 「GPU の無い、私の古いノート PC」を主役にする LLM フレームワークを本気で作る話 | FullSense 3 層と non-transformer backend の関係: | 2026-05-29 | ❓ 要判断 |
| [architecturelandscap.md](tools/qiita-cli-poc/public/architecturelandscap.md) | llcore Architecture Landscape — アーキ体系俯瞰 | llcore は Transformer のコアアルゴリズム (state update / 学習則 / 認知駆動 Δ) に進化形態を与え、Z3 verifier で破綻させずに異アルゴリズムへ進化させる研究フレームワーク。CPU 完結。「同じ design pattern (gene 化 + Z3 invariant gate + 進化 + open-ended 機構) が複数アーキで成立するか | 2026-05-29 | ❓ 要判断 |
| [ba832a58b99c6a9103c4.md](tools/qiita-cli-poc/public/ba832a58b99c6a9103c4.md) | 3 つの Python プロジェクトを MCP 経由で連携させた話 ― llove × llmesh × llive (F25 連携基盤、2026-05-14 時点) | - 3 つの独立 Python プロジェクト (llove / llmesh / llive) を、llmesh の既存 TimelineStore を経由する だけの最小侵襲で連携させた。 | 2026-05-29 | ❓ 要判断 |
| [bdfad6db3f2e70c40511.md](tools/qiita-cli-poc/public/bdfad6db3f2e70c40511.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — 10 思考因子が同時に回る(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2402hero.svg) | 2026-05-29 | ❓ 要判断 |
| [be52eeb6455732161486.md](tools/qiita-cli-poc/public/be52eeb6455732161486.md) | スマホからSSHでWindows PCのClaude Codeを操作する方法 | 自宅WindowsのPCでClaude Codeを使って自動売買システムを動かしているが、外出先からスマホで操作したい場面が出てきた。本記事では、Termiusアプリを使ってスマホ→Windows SSH→Claude Code を実現した手順と、ハマりポイントをまとめる。 | 2026-05-29 | 🔒 内部? |
| [c543014188744262ec83.md](tools/qiita-cli-poc/public/c543014188744262ec83.md) | Pure Python の 6 倍速い Rust 拡張と、ストリーミング再送・HTTP DoS 対策まで詰め込んだ Python ライブラリ — LLMesh 性能と信頼性の話 | ポイントは 「Rust が無くても動く」。Rust 拡張は import に失敗したら 静かに Pure Python にフォールバック します（明示的に環境チェックをかけたいなら python -m llmesh.cli.doctor）。 | 2026-05-29 | ❓ 要判断 |
| [c5f2077a3399d3fc9b26.md](tools/qiita-cli-poc/public/c5f2077a3399d3fc9b26.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — Approval Bus verdict flow + Ed25519 audit chain(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2407hero.svg) | 2026-05-29 | ❓ 要判断 |
| [cab6bb47a72ebedf5436.md](tools/qiita-cli-poc/public/cab6bb47a72ebedf5436.md) | llmesh → llove → llive — FullSense 3 製品の開発履歴・設計コンセプト・差別化・普及戦略 (2026-05-17 時点) | 私 (古瀬 和文 / ぷるやん) は FullSense ™ という umbrella ブランドで 3 つの OSS プロジェクトを並走開発しています: | 2026-05-29 | ❓ 要判断 |
| [cd954f57f510e03954e6.md](tools/qiita-cli-poc/public/cd954f57f510e03954e6.md) | 0. コンセプト hook — 「火種, 爆発, 構造化」 | - 5/18 = 火種を撒く日. F25 Phase h, llove Day-0 gap audit, 中国 LLM presets, | 2026-05-29 | ❓ 要判断 |
| [cdeea496af01dd424a09.md](tools/qiita-cli-poc/public/cdeea496af01dd424a09.md) | GPU の無い、私のあの古いノート PC でも動く AI を、本気で作っている話 | 今日の話の地図 (2 つの世界を並べると): | 2026-05-29 | ❓ 要判断 |
| [da2a2822dabe7b17b8c8.md](tools/qiita-cli-poc/public/da2a2822dabe7b17b8c8.md) | なぜ開発履歴を残すか | llive (リブ) は 2026-05-13 に発足した自己進化型 LLM フレームワーク。本記事は 発足から本日 (2026-05-17) までの 5 日間で何をどう作り、何で躓き、何を学んだか を時系列でまとめたものです。 | 2026-05-29 | ❓ 要判断 |
| [e49b7ab9027d93594402.md](tools/qiita-cli-poc/public/e49b7ab9027d93594402.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — lleval 5+1 honest-disclosure radar across iterations(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2408hero.svg) | 2026-05-29 | ❓ 要判断 |
| [e5093e4816b25c1bd4d0.md](tools/qiita-cli-poc/public/e5093e4816b25c1bd4d0.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — UCB1 bandit arm selection and score curve(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2404hero.svg) | 2026-05-29 | ❓ 要判断 |
| [edaef9aa56ae66b8423e.md](tools/qiita-cli-poc/public/edaef9aa56ae66b8423e.md) | ローカル LLM × 産業 IoT × プロンプトファイアウォールを 1 つの Python フレームワークで — LLMesh v3.1.0 を作った話 | - LLMesh は、ローカル LLM（Ollama / llama.cpp）とクラウド LLM（OpenAI / Azure / Anthropic / OpenRouter / Groq / Together / Mistral / DeepSeek）を 同一 ABC で透過運用 できる Python 統合フレームワークです。 | 2026-05-29 | ❓ 要判断 |
| [fa0890f136636d495ea6.md](tools/qiita-cli-poc/public/fa0890f136636d495ea6.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — TRIZ mutation then Z3 verify(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita2403hero.svg) | 2026-05-29 | ❓ 要判断 |
| [fcb43968a5c642610762.md](tools/qiita-cli-poc/public/fcb43968a5c642610762.md) | LLMesh 紹介記事まとめ — どれから読めばいい？ | LLMesh は 117 章 / 500+ 要件項目 / 2300+ テスト全 PASS の Python 統合フレームワークで、 | 2026-05-29 | ❓ 要判断 |
| [qiita2401memorylayer.md](tools/qiita-cli-poc/public/qiita2401memorylayer.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — 4 層メモリ + Bayesian surprise gate(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita24/qiita2401hero.svg) | 2026-05-29 | 🔒 内部? |
| [qiita2402thoughtfact.md](tools/qiita-cli-poc/public/qiita2402thoughtfact.md) | 言語 / Language / 语言 / 언어: 日本語(日本語) \| English(english) \| 中文(中文) \| 한국어(한국어) | hero — 10 思考因子が同時に回る(https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita24/qiita2402hero.svg) | 2026-05-29 | ❓ 要判断 |
| [QIITA_#16_three_self_spirit_ai_management.md](tools/qiita-cli-poc/public/QIITA_#16_three_self_spirit_ai_management.md) | 「三自の精神」を AI に課す — 圧倒的成果を出し続けるマネジャー流の AI 運用論 | 要件を 消化しきる前に次の要件を積み続けられる。これは人間チームでは破綻するが AI 開発では優位性になる。条件は 1 つ — AI が 自律して動いてくれる こと。キヤノンが掲げる「三自の精神」と、Buckingham & Coffman 等のマネジメント書籍がほぼそのまま転用できる。 | 2026-05-23 | ❓ 要判断 |
| [QIITA_#20J_jekyll_synthetic.md](tools/qiita-cli-poc/public/QIITA_#20J_jekyll_synthetic.md) | Jekyll 合成テスト記事 | これは Jekyll frontmatter (layout: default, permalink) を持つ合成記事で、 | 2026-05-23 | ❓ 要判断 |
