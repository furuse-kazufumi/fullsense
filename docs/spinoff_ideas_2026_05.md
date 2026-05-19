---
layout: default
title: "Spinoff Ideas (Agent-Authored Draft Catalog)"
nav_order: 96
---

# FullSense — Agent-Authored Spinoff & Concept Catalog (2026-05-19)

> 本書は **AI agent (Claude Opus 4.7) が自律的に提案した**プロジェクト
> spinoff 候補・設計パターン・概念群を 1 ヶ所に集約したカタログ.
> いずれも **DRAFT 段階**で、ユーザ判断で採用・改名・廃案を決める前提.
>
> 由来: 2026-05-19 朝〜午後の M8.x 連続実装セッションで agent が自然に
> 思いついた発想群 — 「FullSense の哲学に沿って、まだ FullSense ファミリーに
> 無い vertical を埋めるなら何があるか」.

## 体系図 (位置関係)

```mermaid
flowchart TD
  classDef live fill:#d1fae5,stroke:#10b981;
  classDef proposed fill:#fef3c7,stroke:#f59e0b,stroke-dasharray: 5 3;
  classDef pattern fill:#ede9fe,stroke:#8b5cf6;
  classDef parked fill:#f3f4f6,stroke:#6b7280,stroke-dasharray: 3 3;

  subgraph live [既存 live]
    LM[llmesh]
    LI[llive]
    LO[llove]
    LD[lldesign]
    LT[lltrade]
  end

  subgraph proposed [新規 spinoff 候補 (本書)]
    LG[llgrow — 成長/収益化自動化]
    LE[lleval — ベンチ/評価専用]
    LC[llcraft — クリエイティブ素材生成]
    LB[llbridge — multi-AI 連携]
    LRI[llrisk — リスク自動 track]
    LF[llforen — Forensic (raptor spinoff)]
    LGV[llgov — Governance/Compliance]
  end

  subgraph pattern [設計パターン / 概念]
    P1[3 段ロケット skeleton→本実装→production]
    P2[Cross-repo schema lock pattern]
    P3[Backward-compatible adapter 注入]
    P4[Quiet-Hours-aware autonomy]
  end

  LG -.-> LI
  LG -.-> LO
  LG -.-> LM
  LE -.-> LI
  LC -.-> LI
  LB -.-> LM
  LRI -.-> LI
  LF -.-> LM
  LGV -.-> LI

  class LM,LI,LO,LD,LT live;
  class LG,LE,LC,LB,LRI,LF,LGV proposed;
  class P1,P2,P3,P4 pattern;
```

---

## A. 新規 vertical 候補

### A.1 llgrow — 成長/収益化自動化

**1 行**: コンテンツ生成 / 配信 / 効果測定 / フィードバックループ を on-prem AI で自動化する vertical.

FullSense 哲学を実証するための「自分自身の普及」を AI に任せる試み.
個人開発者の集中力は数分しか持たない ([[feedback-reader-attention-curve]])
ので、記事 / 動画 / コメント返信を AI 下書き + 人間最終承認の HITL ループで
回す. llive Brief API + llove TUI + llmesh peer の薄い orchestration layer
として実装可能. **詳細要件**: `llive/docs/requirements_v0.9_growth_automation.md`
で GROW-01〜10 + リスク章 (RISK-FX A-G).

**先行研究**: [research/llgrow_prior_art]({{ '/research/llgrow_prior_art' | relative_url }})
で Jasper / Mautic / Langfuse / academic 2025 研究の整理あり.
**on-prem + audit log + HITL + 個人開発者 OSS 配信** の 4 条件同時充足は空白.
推奨アプローチ: 基盤を作らず **llive Approval Bus + Langfuse 再利用**, vertical
layer 3 件 (作者 voice memory / channel-specific drafter / 効果メトリクス収集)
のみ新規実装.

代案名: **llmarketing** / **llmonetize** / **llaudience** / **llreach**.

### A.2 lleval — ベンチ・評価専用 vertical

**1 行**: LLM ベンチ・評価フレームワークを on-prem で完結させる vertical.

[[feedback-llive-measurement-purity]] と [[feedback-benchmark-honest-disclosure]]
を踏まえて、ベンチ実行 → 集計 → 内訳分析 → honest disclosure 自動化を担う.
progressive token matrix (xs/s/m/l/xl) ベンチ ([[feedback-benchmark-progressive-tokens]])
を共通 framework にし、競合比較もここで管理. llive / llmesh / 外部 cloud API
の **public benchmark dashboard** をホスト. 「強そうな数字」を出すのではなく
「正直な内訳」を見せるのが差別化. Phoenix / OpenInference 連携も検討.

**SOTA 比較**: [research/lleval_sota]({{ '/research/lleval_sota' | relative_url }})
で OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse /
TruLens / Ragas を整理. **on-prem + cloud 統一**, **progressive size curve**,
**honest disclosure 自動診断**, **self-preference bias 自動検出** の 4 つに
空白あり. 推奨 fork base = **promptfoo** (Apache-2.0 / CI 親和 / on-prem
provider 拡張余地大), 観測層 = **Phoenix** (OpenInference/OTel), RAG metric =
**Ragas/TruLens adapter** 吸収.

代案名: **llbench** / **llmeter** / **llmetrics**.

### A.3 llcraft — クリエイティブ素材生成 (TTS / 画像 / 動画)

**1 行**: on-prem TTS / 画像 / 動画生成を統合する素材工房 vertical.

llgrow の依存層に位置する. VOICEVOX (日本語) + Coqui-TTS XTTS-v2 (多言語)
+ Stable Diffusion XL / Flux.1 + Stable Video Diffusion + Stable Audio を
1 つの API で扱う. 各モデルの **license tier** (商用 OK か NG か) を厳密管理し、
出力に license metadata を埋め込む (LEG-02 リスク mitigation). llmesh の MCP
経由で他 vertical から呼べる.

**SOTA 調査**: [research/llcraft_sota]({{ '/research/llcraft_sota' | relative_url }})
で Stack matrix (TTS / 画像 / 動画 / 音楽 × Tier 1/2/3 license) を整理.
**重要な改訂**: Coqui XTTS-v2 は CPML で商用障壁あり (要許諾) → VoxCPM2
(Apache-2.0) + Irodori-TTS (MIT) + VOICEVOX (キャラ毎契約管理) に置換推奨.
License runtime 強制は **C2PA Content Credentials + IPTC 2025.1** を採用し
独自 `llcraft:license_tier` カスタム assertion を載せる.

代案名: **llmedia** / **llstudio** / **llforge** / **llatelier**.

### A.4 llbridge — Multi-AI Orchestration

**1 行**: Claude / GPT / Gemini / Codex CLI / Cursor を統合的に扱う orchestrator.

`memory/multi_ai_coordination` スキル (raptor) で ActionTracer の構想あり.
これを **on-prem AI bridge** として独立 vertical 化. 役割分担:
- Claude: 思考の深さ / 設計
- GPT: 速度 / API 互換性
- Gemini: マルチモーダル / 巨大コンテキスト
- 各 cloud LLM の "得意分野" を Brief レベルで自動振り分け.

[[feedback-competitor-benchmark]] (Claude / Perplexity / Codex / Gemini を
ベンチ基準) と整合. llmesh の peer 抽象を拡張すれば自然.

**比較研究**: [research/cognitive_mesh_vs_sota]({{ '/research/cognitive_mesh_vs_sota' | relative_url }})
で LangGraph / AutoGen / CrewAI の orchestration を整理. llive Mesh Bridge
(M8.1) は UI (llove TUI) を first-class peer に昇格させるところが差別化.
llbridge は同じ peer 抽象を多 LLM 横断に拡張する自然な拡張.

代案名: **llnexus** / **llrouter** / **llchoir**.

### A.5 llrisk — リスク自動 Track

**1 行**: プロジェクトの法的 / 技術 / ビジネス / 健康 / レピュテーション
/ セキュリティ リスクを継続 track する vertical.

`requirements_v0.9_growth_automation.md` の RISK-FX A-G を一般化. RAD の
risk management / SOX / GRC コーパスを参照しつつ、project context から
自動でリスク抽出 → mitigation 提案 → monthly review 実行. llive Cognitive
Mesh の TonicRiskMonitor ([[project-cog-mesh-m8-complete]] M8.5) を
**メタリスク** (1 メートル上空) に拡張するイメージ.

**先行研究**: [research/llrisk_prior_art]({{ '/research/llrisk_prior_art' | relative_url }})
で AI-driven GRC (ServiceNow / OneTrust) / DevOps scanner (Snyk/Trivy) /
LLM × risk register (Collier 2025) / reputation (Semrush / Brand24) /
developer burnout (CMU Raman / Heath 2025) を 5 縦割り調査. **6 軸統合 + 個人
開発者 + on-prem + LLM-driven** は空白. ポジショニングは「個人 OSS 開発者の
cofounder」, GRC SaaS とは被らない.

代案名: **llguard** / **llcompliance** / **llsentry**.

### A.6 llforen — Forensic (raptor spinoff)

**1 行**: raptor の `/oss-forensics` 部分を FullSense umbrella に取り込んだ
透明性・監査・調査 vertical.

raptor は元々セキュリティ研究 / red-team 向けだが、その **forensic** 機能
(GH Archive クエリ / commit recovery / wayback recovery / 証拠検証) は
FullSense の「ガバナンス + 透明性」哲学と直接整合. RAPTOR 全体を持ち込むのでは
なく、forensic だけ spinoff にして llive / llmesh と統合.

代案名: **lltrace** / **llaudit-fx** / **llwitness**.

### A.7 llgov — Governance / Compliance Layer

**1 行**: 既存 ApprovalBus / SqliteLedger / PromptLinter を 1 vertical に集約.

llive 内部に分散している governance 機能を独立 vertical に. EU AI Act /
中国 AI 弁法 / GDPR / SOC 2 / ISO 27001 等の規制を **要件として要件定義に
組み込む automated compliance** を目指す. [[project-cn-ai-compliance-internal-use-exemption]]
で「社内専用利用は filing 免除」の知見あり. 大手企業向けの「AI 導入時に
コンプライアンス自動付帯」が販売ポイント.

**SOTA 調査**: [research/llgov_sota]({{ '/research/llgov_sota' | relative_url }})
で OSS / SaaS matrix (NeMo Guardrails / OPA / Cedar / MS Agent Governance
Toolkit / Credo AI / Holistic AI 等) を整理. **EU AI Act Art.9-15 を自動検証
する OSS は不在**. 推奨アプローチ: ApprovalBus + SqliteLedger を
**OPA / Cedar policy engine の wrapper** として再構成し, Rego rule + YAML
evidence schema を regulatory pack として配布 (Credo AI policy pack の OSS 版).

代案名: **llcompliance** / **llcomply** / **llwatch**.

---

## B. 設計パターン / 概念

### B.1 3 段ロケット — Skeleton → 本実装 → Production Wire

**1 行**: 大規模機能を 3 段に分けて、各段で backward compatible を維持する設計則.

本セッションの COG-MESH M8.x 実装で実証. skeleton (API 凍結) → 本実装 (
adapter 注入可能化) → production wire (auth / retry / batch). 各段で「注入なし
= 従来挙動」を維持すると、既存テストの回帰がゼロになる. 70 点運用
([[feedback-response-timing]]) との相性が良い. 他 vertical の設計にも展開可能.

### B.2 Cross-repo Schema Lock Pattern

**1 行**: 複数リポをまたぐ contract を両側 unit test でロックする pattern.

llive (event 生成) ↔ llmesh (受信) ↔ llove (表示) の M8.1 で実証.
両側で「expected schema」を unit test として書いて、互いに依存せず守る.
contract drift が即座に test 失敗で検出される. 大規模 microservice
アーキテクチャでも有効. `test_timeline_contract.py` が reference 実装.

### B.3 Backward-compatible Adapter 注入

**1 行**: 機能拡張は constructor 引数追加でなく adapter 注入で行う設計則.

LoveApp の `CognitiveMeshPanel` 統合 (env-gated) や TitleRecallPlanner の
`similarity_fn` 注入で実証. constructor 引数を変えると既存 caller を全て
書き換える必要があるが、`field(default=None)` で adapter 注入すると 注入なし
= 従来挙動を維持できる. Brief API / GROW-FX / llbridge 等にも適用すべき.

### B.4 Quiet-Hours-aware Autonomy

**1 行**: 自律 AI が人間の生活リズムを技術的に強制リスペクトする仕組み.

[[feedback-quiet-hours]] + COG-MESH-07 QuietHoursGuard で実証.
ProactiveLoop / IdleTrainingScheduler が depth=1 で QuietHoursGuard を
**必須依存**に持つ. None だと TypeError. env 欠落で fail-closed.
これは llgrow (深夜投稿しない) / llrisk (深夜アラート抑制) /
llbridge (深夜 cloud API 呼び出し抑制) でも適用すべき汎用 pattern.

### B.5 Honest Disclosure as Architecture

**1 行**: 「正直な内訳開示」をシステム要件として組み込む設計則.

[[feedback-benchmark-honest-disclosure]] と整合. ベンチで自社が異常に
速い結果が出たら勝った気になる前に必ず内訳を疑う、を組織文化ではなく
**技術的に強制**する. BriefRunner の `lint_report` / governance scorer
/ `recommend_block` 等が既に部分実装. lleval / llgrow / llgov に標準
搭載すべき.

### B.6 Independence Principle

**1 行**: 各 vertical は単独で価値を持ち、ファミリー全体で組み合わせ価値を
積み上げる設計則.

[[feedback-independence-principle]] (LinkedIn フィードバック由来). FullSense
3 層 (llmesh / llive / llove) は **runtime 相互依存禁止**. Annotation で
組合せ価値を積み上げる. 本書で提案する spinoff 群も同じ原則を守ること.
llgrow が llive 必須にしたら本則違反 (現状は依存と書いているが、それぞれ
optional な書き換えが必要).

---

## C. 命名規則の整理

FullSense ファミリーの `ll-` 接頭辞 + 短い英単語が暗黙のルール:

| 既存 | 意味 |
|---|---|
| llmesh | mesh (network) |
| llive | live (自己進化) |
| llove | love (HITL = 愛のこもったレビュー) |
| lldesign | design |
| lltrade | trade |
| llcad | CAD |
| lleda | EDA |
| llchip | chip |
| llmed | medical |
| llpaper | paper (academic) |
| llmaterial | material |
| llops | ops |
| llhft | HFT |

本書提案:

| 案 | 意味 | 競合チェック |
|---|---|---|
| llgrow | growth | OK |
| lleval | evaluation | OK |
| llcraft | craft (creative) | OK |
| llbridge | bridge | OK |
| llrisk | risk | OK |
| llforen | forensic | OK |
| llgov | governance | OK |

いずれも `ll-` + 4-7 文字の英単語 + 既存衝突なし.

---

## C-2. 採用優先度 (research 結果ベース, 2026-05-20)

[research/]({{ '/research/' | relative_url }}) に集めた先行研究 / SOTA 調査結果から
逆引きした優先度.

| vertical | 採用優先度 | 根拠 | リスク |
|---|---|---|---|
| **lleval** | HIGH | promptfoo を fork base に 4 つの明確空白 (on-prem 統一 / progressive size / honest disclosure / self-pref bias) を埋める. [SOTA Survey]({{ '/research/lleval_sota' | relative_url }}) | promptfoo 本流の OSS 政治 (Apache-2.0 だが Confident AI 主導) |
| **llgrow** | MID | Langfuse + Mautic 再利用で基盤新規不要, 新規実装は voice memory / channel drafter / 効果メトリクス 3 件のみ. [Prior Art]({{ '/research/llgrow_prior_art' | relative_url }}) | brand 毀損リスク (honest disclosure を内蔵で mitigate) |
| **llbridge** | MID | LangGraph/AutoGen/CrewAI に対し UI を first-class peer 化, llmesh の peer 抽象拡張. [Cognitive Mesh vs SOTA]({{ '/research/cognitive_mesh_vs_sota' | relative_url }}) | multi-AI コスト管理, [feedback_competitor_benchmark] と整合 |
| **llcraft** | LOW (research 待ち) | license tier 自動化が差別化候補. 詳細 [研究待ち]({{ '/research/' | relative_url }}) | model license diff (商用 / Non-Commercial), GPU 要件 |
| **llrisk** | LOW (research 待ち) | TonicRiskMonitor のメタ拡張. 詳細 [研究待ち]({{ '/research/' | relative_url }}) | scope 過大 (法務/技術/ビジネス/健康/レピュ/セキュ の 6 軸) |
| **llgov** | LOW (research 待ち) | EU AI Act / 中国 弁法 / SOC 2 / ISO 27001 自動化. 詳細 [研究待ち]({{ '/research/' | relative_url }}) | 規制の地域別差・改定頻度 |
| **llforen** | DEFER | raptor 依存が強い, FullSense umbrella に取込む前に raptor 側の安定化を待つ | upstream raptor との同期 |

「HIGH」の lleval は本書発の最初の **本格 spinoff** 候補. 着手 trigger:
ベンチ復旧 (Anthropic / Gemini / OpenAI credential 復活) と並行で promptfoo
fork PoC が動けば即着手判断可能.

---

## D. 採用フロー (案)

```
1. user が紹介文を読む (本書)
   ↓
2. 採用 / 改名 / 廃案 を決める
   ↓
3. 採用なら fullsense portal roadmap.md の Planned に追加
   ↓
4. trigger condition を明示 (例: "user MAU > 100 になったら llgrow 着手")
   ↓
5. trigger 発火で本格要件化 (requirements_vN.M_XXX.md)
   ↓
6. skeleton 実装 → 本実装 → production wire (3 段ロケット)
   ↓
7. PyPI / GitHub に分離 spinoff
```

---

## E. 注意

- 本書は **agent 提案の draft 集**であり、user 採用を経るまでは正式な
  プロジェクトではない.
- 命名は **仮称**. user 判断で改名・統合・廃案あり.
- 「いっぱい紹介文書作って」というご要望に応えた catalog だが、**着手は
  優先順位を user が決める**.
- 短期 (3 ヶ月) で着手するなら **llgrow + lleval** がコスト対効果高い
  (既存 llive 機能の薄い orchestration + 既存ベンチコードの整理).

---

## 関連

- `roadmap.md` — 既存 product Live / Planned マトリクス
- `cognitive-mesh.md` — M8.x 実装記録 (3 段ロケット patternの実証)
- llive `docs/requirements_v0.9_growth_automation.md` — llgrow 詳細要件
- llive `docs/ai_dev_env_2026_05.md` — 環境投資ロードマップ
- llive `docs/legal/trademark/CHECKLIST_2026_05.md` — 商標出願準備

## Last updated

2026-05-19 — agent 自律提案を catalog 化. user 採用待ち.
