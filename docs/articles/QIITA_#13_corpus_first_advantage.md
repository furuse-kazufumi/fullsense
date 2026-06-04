---
layout: default
title: "コーパス先行戦略 — AI が私の気づかない観点を思考フローに補完する優位性"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags: AI コーパス 認知科学 開発手法 SixHats
id: 75d682ddefa5aeb738b8
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# コーパス先行戦略 — AI が私の気づかない観点を思考フローに補完する優位性

著者: **古瀬 和文（ぷるやん）**

## TL;DR

- 本日のセッションを通じて気づいた **AI 協働開発の本質的優位性**
- 「**最初にコーパスを充実させる**」ことで、AI が新規実装・要件定義の際に背景でコーパスを参照
- ユーザーが意識していない観点 (Six Hats / TRIZ / KJ法 / MindMap / 異分野類比) が **自動的に思考フローに混入**
- 1 人開発でも複数の認知視点を背景で得られる構造
- これは **「AI を使う」 vs 「AI と一緒に作る」** の本質的な分岐点

## 気づきの瞬間

本日 (2026-05-17) のセッションは、1 日で要件 32 件追加 + プログラム 2200 行 + テスト 78 件 + 記事 14 本という規模で進みました。

その振り返り中、ある気づきがありました:

> 「自分が KJ法 / MindMap / Six Hats / TRIZ を意識的に使った覚えはないのに、なぜか出てくる要件や設計判断にこれらの観点が **自然に混ざっている**」

例えば、私 (人間) が「Qwen から離脱したい」と言うと、AI は背景で以下を勝手に整理して持ち出してきます:

- **Stage A→B→C→D→E の段階分解** (TRIZ 原理 7: Nested doll、段階的拡張)
- **GPU 投資判断の閾値** (Six Hats: cautious 観点)
- **評価指標 AOS / LCIR** (Six Hats: process 観点)
- **「補完路線も並走」** (Synectics: 二項対立の解消)

これらは私が「意識して」AI に頼んだことではなく、**AI が背景でコーパスを参照しながら勝手に補完してきた** 観点です。

## なぜこれが起きるのか

### 構造

```
[ユーザー (人間)]
     │ 「Qwen から離脱したい」
     ▼
[AI (Claude Opus 4.7)]
     │ 背景で参照:
     │  ├ raptor RAD 49 分野 (4.9 万 documents)
     │  ├ hacker_corpus (Exploit-DB + ATT&CK + NVD + Phrack)
     │  ├ memory 60+ ファイル (過去の決定 + 教訓)
     │  ├ CLAUDE.md 規約 (auto-trigger: rad-research / triz-ideation / cross-domain-ideation)
     │  └ Six Hats / TRIZ / KJ法 / MindMap の構造化された知識
     ▼
[出力]
     5 段階ロードマップ + GPU 判断 + 評価指標 + 補完路線 +
     関連先行研究 + 同点と認める領域 + リスク表 + ...
```

ユーザーは「Qwen から離脱したい」という 1 行を入力しただけ。出力に含まれる **「同点と認める領域」** や **「リスク表」** や **「補完路線」** は、ユーザーが意識していない観点。

### コーパスの役割

AI 単体 (Claude / GPT / Gemini) は、当然「Six Hats」「TRIZ」「KJ法」の知識を持っています。しかし、それを **どの場面で適用すべきか** の判断は、コーパスと CLAUDE.md の規約が決定します:

```yaml
# CLAUDE.md (raptor) より抜粋
AUTOMATIC SKILL ACTIVATION:
  rad-research を自動起動: 新機能・新設計の着手前 (無条件)
  triz-ideation を自動起動: 矛盾・トレードオフ・両立できない
  cross-domain-ideation を自動起動: 異分野・他分野・分野を超えて
```

つまり、**コーパス + 規約** が AI の思考フローの「自動補完エンジン」として機能しています。

## 実例 — 本日のセッションから

ユーザーが意識していた入力 vs AI が背景で補完した観点:

| ユーザーが意識していたこと | AI が背景で補完した観点 |
|---|---|
| 「LLM の周りに何か作りたい」 | TRIZ 40 原理 / 39×39 矛盾マトリクス / Mediator パターン / Provenance DDD |
| 「ベンチを取りたい」 | Honest disclosure / xs/s/m/l/xl 5 段ラダー / mean/stdev 統計 |
| 「Qwen から離脱したい」 | Stage A→E 段階分解 / GPU 投資判断 / 評価指標 (AOS / LCIR) |
| 「数学・単位特化」 | SI 7 基本単位 / CODATA 2022 / Buckingham π / IEEE 754 |
| 「思考因子を導入」 | Cognitive Factor Framework / Role-based agents (architect/critic/executor/auditor) |

これらの観点を **「ユーザーが意識する前に AI が selection してくる」** のが本戦略の核心です。

## なぜ気づかなかったのか

人間は、自分の専門分野では「知っているはずの観点」を当然のものとして無意識に使います。しかし:

- 専門外の観点 (例: 物理学者にとっての法務、エンジニアにとってのマーケティング)
- 関連分野だが距離のある観点 (例: LLM 開発者にとっての認知心理学)
- 過去に学んだが忘れている観点 (例: 学部時代に学んだ Six Hats)

これらは **意識下に上ってこない** ため、自分では補完できません。AI がコーパス経由でこれらを引っ張ってきてくれるのが、協働開発の本質的な優位性です。

## 「AI を使う」 vs 「AI と一緒に作る」の違い

| 項目 | AI を使う (cloud chat) | AI と一緒に作る (本セッションのスタイル) |
|---|---|---|
| AI へのインプット | 1 つの質問 | コーパス + memory + CLAUDE.md + 質問 |
| 補完される観点 | LLM 訓練データの平均的な観点 | プロジェクト固有のコーパスに紐付いた観点 |
| 多視点の自動性 | 限定的 | 高い (auto-trigger 設計あり) |
| 過去の決定の参照 | 不可 | 可 (memory 経由) |
| プロジェクト固有の癖 | 反映不可 | 反映可 (CLAUDE.md と memory) |

本セッションは後者で進めています。**コーパスを先に整え、規約を設計し、memory を蓄積する** ことで、AI が思考フローの自動補完エンジンとして機能します。

## llive 文脈での意義 — CREAT (Creative Thinking Layer)

この気づきは llive の **CREAT** 設計動機を強化します:

- CREAT-01 KJ法ノード — 視野狭窄を防ぐため拡散 ≥20 件強制
- CREAT-02 MindMap — 思考の浅さを防ぐため DFS depth=3
- CREAT-04 Six Hats — 偏った楽観を防ぐため 6 観点強制
- CREAT-05 Synectics — 既存パターン依存を防ぐため異分野類比強制

llive ユーザーは **CREAT を使うだけで** 「自分が意識しない観点」を補完される。これは「AI 開発の優位性」をユーザーにも提供する設計です。

つまり llive は:

```
[Phase 1: llive 開発者 (= 私)]
  raptor コーパス + memory + CLAUDE.md → AI が多視点補完 → 1 日で 32 件要件

[Phase 2: llive エンドユーザー]
  llive CREAT + Brief Grounder (TRIZ × RAD) → llive が多視点補完 → ユーザーは観点を意識しなくて OK
```

llive 自体が「コーパス先行戦略の優位性」をユーザーに伝播する仕組みです。

## 翌日以降の運用への示唆

### コーパス品質 = AI 思考品質

- raptor RAD 49 分野は維持・拡張
- hacker_corpus / Exploit-DB / ATT&CK / NVD / Phrack 等の高品質ソースを継続追加
- corpus2skill v2 で要約品質を上げる

### auto-trigger を maximize

- `rad-research` / `triz-ideation` / `cross-domain-ideation` を遠慮なく発火
- 「広く呼ばれるべき補助資料スキル」として CLAUDE.md に明記済

### memory を蓄積し続ける

- セッション内で得た教訓を即 memory 化
- 「ユーザーが意識していない観点」のうち、特に効いたものを記録
- 翌日以降のセッションで再利用

## まとめ — AI 協働開発の優位性 3 公理

本日得た気づきから 3 つの公理:

1. **コーパスの質 = 出力の質** — AI 単体ではなく、AI + コーパス + 規約 + memory のセット
2. **意識下にない観点こそ価値** — ユーザーが気づかない観点を AI が背景で補完
3. **1 人開発 = 多人数開発** — Six Hats / Role-based agents の自動適用で、1 人でも複数視点

この 3 公理は llive の CREAT 要件群を通じて、エンドユーザーにも提供されます。

## ソース

- memory: `project_corpus_first_advantage.md` (本日新規)
- 関連 memory: `project_llive_cog_fx_factors` / `project_corpus_overnight_2026_05_12` / `project_hacker_corpus`
- llive 要件: `REQUIREMENTS.md` v0.9 CREAT (CREAT-01〜05)
- raptor CLAUDE.md: AUTOMATIC SKILL ACTIVATION セクション

## 同日記事

- [QIITA_SUMMARY](./QIITA_SUMMARY.md) — 技術者向け統合
- [QIITA_GENERAL](./QIITA_GENERAL.md) — 非エンジニア向け統合
- [QIITA_HISTORY](./QIITA_HISTORY.md) — 3 製品履歴 + 設計 + 差別化 + 普及
- [12_dev_history](./12_dev_history.md) — llive 単独開発履歴
- LinkedIn 多言語版 (SUMMARY / GENERAL / HISTORY × jp/en/zh/ko)

---

> AI と一緒に作る = AI が背景でコーパス参照 + 多視点を補完しながら、設計判断は人間が行う。本セッションは 1 日で要件 32 件 + 1014 PASS + 14 記事という規模を実現。
