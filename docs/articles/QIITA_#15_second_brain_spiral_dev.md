---
title: 30 年のソフトウェア開発経験 + Perplexity 要約 + Claude Code + TRIZ + 5 万件の論文 RAG = 「第二の脳」
tags:
  - FullSense
  - llive
  - 解説
  - TODO_TAG
  - TODO_TAG
private: false
updated_at: '2026-05-22'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

# 30 年のソフトウェア開発経験 + Perplexity 要約 + Claude Code + TRIZ + 5 万件の論文 RAG = 「第二の脳」

**1 行 hook**:
1 人開発で 5 日間に Brief API・OKA-FX・VRB-FX・IND-04 アノテーション・MathVerifier を含む 14 機能と 256 テストを追加し、1270 件全 PASS で回帰ゼロを達成した。秘訣は「第二の脳」をどう組み立てるかにある。

---

## 「第二の脳」の定義

筆者 (30 年超のソフトウェア開発者) は llive (FullSense umbrella の中核プロダクト、L は 2 個) を **1 人で開発**しているが、進度はチーム開発に近い。これは次の 5 要素を組み合わせた「第二の脳」を構築したからだ。

| 要素 | 役割 |
|---|---|
| **30 年の開発経験** | 設計品質・判断のベース。アイデア・ノウハウとして毎セッション渡す |
| **Perplexity 要約** | 取り込みたい外部思想 (書籍・論文・YouTube) を高品質に圧縮 |
| **Claude Code (Opus 4.7 / 1M context)** | 実装エージェント |
| **TRIZ ルール (40 原理)** | 矛盾解決のメタ思考フレーム。特許領域での経験から llive 設計へ |
| **論文 RAG コーパス (RAD 49 分野 / 約 5 万件)** | Claude Code が「研究者の知見」で答える土台 |

これらを **スパイラル開発サイクル** に流すと、外部思想が短時間で実装に着地する。

### ☕ ちょっと脱線

「第二の脳」って言葉、最初は気恥ずかしかった。Tiago Forte の同名書籍に引きずられて陳腐に聞こえる気がして。でも 5 日間で 14 機能を 1 人で積み終えた後に振り返ると、これ以上ピッタリの言葉が見つからない。**気恥ずかしさは正確さの前に折れる**。

## スパイラル 1 サイクル

```
外部思想 → Perplexity 要約 → Claude Code 読込 → 要件化 → 実装 → ベンチ → commit
   ↑                                                                      |
   └──────────────────────────── 次サイクル ────────────────────────────┘
```

実際の例 (本セッション 9 回中の 3 例):

| サイクル | 起点 | 結果 |
|---|---|---|
| 1 | **MBA 言語化トレーニング** (グロービス書籍) | Perplexity が 8 機能に整理 → VRB-FX (Verbalization Framework) 4 件要件化 → VRB-02 PromptLint 実装 (1 セッション) |
| 2 | **岡潔先生の数学観に学ばせていただく** (YouTube『心理の深層』講話より) | 先生が遺された「数学は情緒である」「発見の前に一度行き詰まる」「文章を書くことなしには思索を進められない」「国語が数学を育む」という思想を、Perplexity で要約させていただいた上で **設計の 4 観点** として参照 → OKA-FX 10 要件として記述 → OKA-01〜04 minimal proto 実装。**先生のお考えそのものを実装したと主張するものではなく**、こちらの設計が触発を受けた先生の思想への敬意を表して命名している |
| 3 | **LinkedIn フィードバック**「相互依存を避けたい」 | IND-FX 設計原則 + IND-04 Annotation Channel 実装、`<!-- llive:ns.key=val -->` で独立性と組合せ価値を両立 |

各サイクルが **要件 → 実装 → テスト → commit** まで数時間で完走する。

## なぜスパイラルが回るのか

### Perplexity 要約の役割 — 「入力品質ゲート」

外部思想は本・論文・動画・SNS と形式バラバラ。これを Claude Code に直接放り込むと:
- 元情報が膨大で context window を食う
- 重要部分とノイズが混在
- Claude の解釈にゆらぎが出る

Perplexity に「~3000 字に要約」「実装可能な仕様で」「対比表で」と指示すると、**Claude Code が読み取れる質の入力**に変換される。これが「入力品質ゲート」として機能する。

### TRIZ の役割 — 「矛盾解決のメタ思考」

実装中に何度も矛盾が出る。例:
- 「独立性を担保したい」 vs 「組合せで価値を積み上げたい」
- 「rule-based fallback も残したい」 vs 「LLM 品質を測りたい」
- 「監査ログを完全に取りたい」 vs 「実装オーバヘッドを増やしたくない」

これを **TRIZ 矛盾マトリクス** 視点で解くと、両立解が見える。本セッションの解:
- IND-04 Annotation Channel = 「コメント = renderer 不可視 + 機械可読」で両立 (TRIZ 原理 24: 媒介物)
- echo baseline 残置 = 「同じ rule-based 出力を別カテゴリで表示」で両立 (TRIZ 原理 1: 分割)
- bind_ledger() pattern = 「optional 注入で audit はゼロコスト」で両立 (TRIZ 原理 15: 動的化)

### 論文 RAG (RAD 49 分野 ~5 万件) の役割 — 「研究者の知見を借りる」

新機能設計で必要な分野が出るたび、RAG コーパスを引く。本セッション例:
- OKA-FX 設計 → `mathematics` / `formal_methods` / `metrology` を参照
- VRB-FX 設計 → `mba` (management) / `linguistics` を参照
- IND-04 設計 → `software_engineering` / `oss_governance` を参照

Claude Code が「自分の言葉」で書くと一般論になりがちだが、**RAG で具体的な論文・先行研究を引用** すると質が一段上がる。

## 結果 — 5 日間で起きたこと

| Day | 主な追加 |
|---|---|
| 5/13 | llive プロジェクト立ち上げ、Phase 1 完了 |
| 5/14 | F25 連携基盤完了 (llove↔llmesh↔llive MCP 経由) |
| 5/15 | 9 軸 skeleton (KAR/DTKR/APO/ICP/TLB/Math/PM/RPAR/SIL) |
| 5/16 | C-1 Approval Bus + Policy + SQLite Ledger 完了 / 815 PASS |
| 5/16 | Brief API end-to-end / progressive matrix 完走 / 998 PASS |
| 5/17 | **9 セッション** で 14 機能 (COG-04, CREAT-04, MATH-02, OKA-01〜07, VRB-02/04/05/06, CREAT-01〜05, IND-FX, MathVerifier-Runner 統合, etc.) / **256 テスト追加** / **1270 PASS / 回帰ゼロ** |

1 人開発でこの速度を出すのは、5 要素が噛み合う「第二の脳」あってこそ。

### ☕ ここまで読んでくれてありがとう

正直、テスト 256 件のうち 7-8 件は途中で 1 回ずつ落ちている。fuzzing で hypothesis が嬉しそうに edge case を見つけてくれるたび、3 秒くらい「うわ」となる。**1270 PASS / 回帰ゼロ** はゴールであって過程ではない。

## 自身の 30 年経験はどこで効くか

「Claude Code 任せ」だと品質は出ない。30 年経験は次の場面で決定的だった。

1. **要件定義の質** — Perplexity 要約を読んで「これは要件 vs 解法を混同している」と即判定し書き直し指示
2. **TRIZ ルールの選定** — 40 原理から「この場面はこの 3 つ」を即抽出 (TRIZ 経験が無いとここで時間を取られる)
3. **アーキテクチャ判断** — Claude が出した実装案を「これは独立性原則に反する」「これは bind_ledger pattern と整合しない」と即拒否
4. **ベンチの honest disclosure** — rule-based の coverage が高く出たときに「これは echo back の偽性能」と即見抜く (測定経験)
5. **タイポチェック** — 「llive が lllive になってる、tokenizer 問題の再発」と即特定 (パターン認識)

つまり **第二の脳 = Claude Code + RAG + Perplexity + TRIZ** に対し、**第一の脳 = 自身の経験** が判断ゲートとして居続ける。両者の合成が「1 人 + 第二の脳 = チーム」を成立させている。

## 他の開発者への示唆

この「第二の脳」を構築するコスト:
- Claude Code 課金 (Max plan 推奨、context 1M 必須)
- Perplexity Pro (月 $20)
- RAG コーパス構築 (Raptor 等 OSS ツールで自前、本 case は ~5 万件 / 49 分野)
- TRIZ 学習 (書籍数冊 + 実践)
- **何より自身の経験を Claude Code に渡し続ける覚悟**

最後の項目が一番重要。Claude Code に丸投げしては、ありきたりな実装しか出ない。**経験者がレビュアー + アーキテクトとして居続ける** ことで、「研究者チーム + 30 年経験 + 実装エージェント」の合成が成立する。

llive は現時点で Apache 2.0 + Commercial dual-license の OSS、Repo は https://github.com/furuse-kazufumi/llive 。本記事の「第二の脳」型開発スタイルに興味のある方は、Issue / Discussion で議論したい。

---

**過去の関連記事**:
- [12] llive 開発履歴 — 5 日で v0.1 から v0.7 候補へ
- [13] コーパス先行戦略 — AI が気づかない観点を思考フローに補完
- [14] HTML で見えないのに、機械では読める — 不可視アノテーションチャネル設計

## 参考文献 / 参考リソース

### TRIZ (発明的問題解決理論)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996
- Karen Gadd, *TRIZ for Engineers: Enabling Inventive Problem Solving*, Wiley, 2011
- TRIZ Journal (オンラインアーカイブ) — https://triz-journal.com/

### RAG / コーパス構築
- Patrick Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 (arXiv:2005.11401)
- Raptor (本記事で参照した RAD コーパス構築ツール) — https://github.com/raptor-rad/raptor (本人 fork: 公開準備中)

### 「第二の脳」概念の原点
- Tiago Forte, *Building a Second Brain: A Proven Method to Organize Your Digital Life and Unlock Your Creative Potential*, Atria Books, 2022
- 邦訳: 春川由香 訳『SECOND BRAIN — 時間に追われない「知的生産術」』ダイヤモンド社, 2022

### 開発エージェント
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Perplexity AI — https://www.perplexity.ai/

### llive 関連
- llive リポジトリ — https://github.com/furuse-kazufumi/llive
- 本記事の「9 セッション 14 機能 1270 PASS」の根拠: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`

<!-- llive:meta.article_id="15_second_brain_spiral_dev" target=llove -->
<!-- llive:meta.published_date="2026-05-19" -->
<!-- llive:meta.tags=["llive","claude-code","perplexity","triz","rag","development","oss"] target=any -->
