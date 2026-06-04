---
title: 'FullSense ナレッジベース — 読む順ガイド (INDEX)'
tags:
  - FullSense
  - llive
  - llcore
  - INDEX
  - 解説
private: false
id: 90ea260703fb49065346
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# FullSense ナレッジベース — 開発物語で読む順ガイド

> このチームの記事は投稿日順だと話題が前後して読みにくいので、**FullSense 開発の物語 (10 フェーズ)** に沿って並べ直しました。
> FullSense の製品は **llmesh → llove → llive → llcore** の順に生まれています。各幕は独立して読めますが、上から読むと「local LLM の連携模索」から「進化型 AI の開発」まで一本の物語として繋がります。
> 急ぐ人は **プロローグの 3 本**だけでも全体像が掴めます。

---

## プロローグ — まず 3 本（全体像）

1. [推論する AI から「予測する認知 OS」へ — FullSense 開発 1 週間ダイジェスト](https://fullsense.qiita.com/furuse-kazufumi/items/1f71a3e5bb830cb51b80) — 最短サマリ
2. [AI を『使うだけ』から『AI に秘書を付ける』へ — 自宅 PC で動くおせっかい AI](https://fullsense.qiita.com/furuse-kazufumi/items/cda72a85bf20524eb8f5) — 非エンジニア向けの入口
3. [llive 完全解説 (0) — series index：大分類 8 記事 + 全体図](https://fullsense.qiita.com/furuse-kazufumi/items/d3a411523a01cb9ddd66) — 技術解説の目次

---

## 物語の地図（10 フェーズ）

| 幕 | 何が起きたか | 主な記事 |
|---|---|---|
| 1 | local LLM の連携を模索（出発点） | HISTORY, 開発履歴 |
| 2 | セキュリティ確保のため Raptor 導入 + 布石（コーパス先行） | コーパス先行, 第二の脳螺旋 |
| 3 | 「多数の情報を渡せる形」へ — mcp-3d / llmesh | （記事薄め） |
| 4 | llive で Qwen をラッパー（LLM を素材生成者に） | Brief API, MATH, CABT… |
| 5 | llove という Interface で動作確認 | （記事薄め） |
| 6 | llive に進化プログラムの性質を与える — lldarwin | #24 シリーズ, #25〜#30 |
| 7 | Qwen / Transformer からの脱却を模索 | #18, #19, #22 |
| 8 | llcore — Transformer に進化アルゴリズムを組込み | #32, #33, #34 |
| 9 | 「嘘の進化」が出ないよう徹底評価 — 検証と反証 | #29, #35 シリーズ |
| 10 | 進化型 AI の開発に着手中（現在地） | — |

---

## 第 1 幕 — local LLM の連携を模索する（出発点）

すべての始まりは「自宅 PC の local LLM たちを連携させたい」という素朴な欲求でした。年表として読むならこの 2 本。

- [FullSense 3 製品の開発履歴・設計コンセプト（llmesh → llove → llive）](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) — 物語全体の年表
- [llive 開発履歴 5 日](https://fullsense.qiita.com/furuse-kazufumi/items/504036f1116fcd976dd3)

---

## 第 2 幕 — セキュリティの壁と Raptor、そして布石

外部に出せない情報を扱う以上、セキュリティ確保が先決。Raptor（Claude Code のセキュリティエージェント化 fork）を導入し、その Raptor で論文コーパス（RAD、21+ 分野・約 5 万件）を蓄積したことが、のちの進化アルゴリズム開発の**布石**になります。

- [コーパス先行戦略 — 5 万件の論文を先に集める](https://fullsense.qiita.com/furuse-kazufumi/items/75d682ddefa5aeb738b8)
- [30 年の開発経験 + Perplexity + Claude Code + TRIZ + 5 万件コーパス](https://fullsense.qiita.com/furuse-kazufumi/items/a30e7f893874d6901dee)

> Raptor 自体の専用記事は未投稿（HISTORY 内で言及）。

---

## 第 3 幕 — 「多数の情報を渡せる形」へ: mcp-3d と llmesh

3D/空間アセットの mcp-3d、on-prem LLM hub の llmesh で「LLM に多数の情報を安全に渡せる形」を整えました。この幕の専用記事は薄め — [HISTORY](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) の該当章を参照（専用記事は backlog）。

---

## 第 4 幕 — llive 誕生: Qwen を「素材生成者」としてラップする

LLM を判断者ではなく**素材生成者**として被せる認知 OS = llive の誕生。機能が一気に立ち上がった幕です。

1. [Brief API and progressive matrix — overhead < 1 %](https://fullsense.qiita.com/furuse-kazufumi/items/60537278f72f8a9fc2dc) — 外部から構造化 work unit を渡す
2. [1 日で要件 32 件 + Brief API + COG-FX + MATH + ベンチ](https://fullsense.qiita.com/furuse-kazufumi/items/bfa83d01e79028132438) — 立ち上がりの記録
3. [10 思考因子で整理する llive 思考層](https://fullsense.qiita.com/furuse-kazufumi/items/4de8dcff1cf4c2ab9bdc)
4. 数学に強くする: [最初の一歩](https://fullsense.qiita.com/furuse-kazufumi/items/2c4a993937c373c464f6) → [形式検証ゲート (MATH-02)](https://fullsense.qiita.com/furuse-kazufumi/items/acb5f5e0dabe2020c166) → [実 Brief 6 件で grounding 観察](https://fullsense.qiita.com/furuse-kazufumi/items/29b26774667b3af3a04e)
5. [Transformer ブロック高度化 7 アプローチ (CABT)](https://fullsense.qiita.com/furuse-kazufumi/items/a6804f6b8c47605177a8) ／ [LLM × KJ法 × MindMap で要件定義 (CREAT)](https://fullsense.qiita.com/furuse-kazufumi/items/0c6deb6f462843a71094)
6. [不可視アノテーションチャネル設計](https://fullsense.qiita.com/furuse-kazufumi/items/851773b6cfe85c7811a4) ／ [CSV/TSV の後継 USV (Unit-Separated Values)](https://fullsense.qiita.com/furuse-kazufumi/items/fda1d13c689095720534)
7. Qwen との距離感: [依存から離脱する 5 段階ロードマップ](https://fullsense.qiita.com/furuse-kazufumi/items/ba3a0f41e42ec533a3a1) ／ [Qwen と相互補完する llive](https://fullsense.qiita.com/furuse-kazufumi/items/f400cf06e86b350b055c)
8. [llive の構造は独自か — 8 差別化要素の点検](https://fullsense.qiita.com/furuse-kazufumi/items/0c1d5ebd6b0656ba74e1)

---

## 第 5 幕 — llove という Interface で「動くか」を確かめる

TUI ダッシュボード llove で、llive/llmesh が実際に動く様子を人間が確認できるようにしました。この幕も専用記事は薄め — [HISTORY](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) ／ [非エンジニア向け入口](https://fullsense.qiita.com/furuse-kazufumi/items/cda72a85bf20524eb8f5) を参照。

---

## 第 6 幕 — llive に「進化」を与える: lldarwin

llive を 1 個の AI でなく **N 個体の派生集団**として世代交代させる試み。失敗（monoculture）から学び、選択圧コンポーネント lldarwin が生まれた、この物語の山場のひとつ。

**体系リファレンス（llive 完全解説・8 本）**:

1. [(1) 「忘れない LLM」：4 層メモリ + Bayesian surprise gating](https://fullsense.qiita.com/furuse-kazufumi/items/2732122ed0a4c9ace0af)
2. [(2) 「10 軸で考える AI」：思考因子 × COG-MESH × 三重縞](https://fullsense.qiita.com/furuse-kazufumi/items/94fae20cea5e53d1358f)
3. [(3) 「矛盾は計算できる」：構造進化 × TRIZ 40 原理 × Z3 検証](https://fullsense.qiita.com/furuse-kazufumi/items/198eadaee7c380c426d5)
4. [(4) 「収束する脳」B-series：SynapticSelector / UCB1](https://fullsense.qiita.com/furuse-kazufumi/items/9839392b82e3372dbdc9)
5. [(5) 「集団が学ぶ AI」：v0.B/C/D/E 派生集団進化総括](https://fullsense.qiita.com/furuse-kazufumi/items/c999960660e25bdb5b66)
6. [(6) 「Transformer の外」：Mamba / Jamba / RWKV / Diffusion](https://fullsense.qiita.com/furuse-kazufumi/items/fa9cfbdbdebecf1c7c3b)
7. [(7) 「審査つき AI」：runtime_metadata × Approval Bus](https://fullsense.qiita.com/furuse-kazufumi/items/f3ef0430798ff9df07ab)
8. [(8) 「眼鏡を作る」：lleval — honest disclosure 5+1 因子](https://fullsense.qiita.com/furuse-kazufumi/items/4b98e2a877cf746ce8e3)

**lldarwin 物語（この順に）**:

1. [AI を 500 世代進化させたら 2 人だけ残った — monoculture の honest disclosure #25](https://fullsense.qiita.com/furuse-kazufumi/items/8b510aed45cdfad71909)
2. [「眼鏡で測る」だけでは進化しない — 選択圧 lldarwin #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)（[📗 かみくだき版](https://fullsense.qiita.com/furuse-kazufumi/items/1d9eeb1b739623dbc285)）
3. [一晩で AI 進化を作り直した #27](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)（[📗 かみくだき版](https://fullsense.qiita.com/furuse-kazufumi/items/6b134e5a4f87963681c2)）
4. [進化集団を「指揮者」が合奏させて答える #28](https://fullsense.qiita.com/furuse-kazufumi/items/333165c2d5704e652721)
5. [進化を「見せる」技術の系譜 #30](https://fullsense.qiita.com/furuse-kazufumi/items/0e221d447b7a8ad66d22)

**総まとめ（2 版）**: [📘 かみくだき版 — llive "メガ進化"！](https://fullsense.qiita.com/furuse-kazufumi/items/49f9e2359c77dce0ed4f) ／ [📗 完全版 — evolution arc](https://fullsense.qiita.com/furuse-kazufumi/items/0819897256c2e46831ad)

---

## 第 7 幕 — Transformer からの脱却を模索する

コアの Qwen / Transformer に頼らない道はあるか。Mamba / RWKV など non-Transformer の検討と「脱却の現在地」の整理。

- [GPU の無い古いノート PC でも動く AI を本気で作る](https://fullsense.qiita.com/furuse-kazufumi/items/a10147101bb6b81b811c) ／ [その主役化の話](https://fullsense.qiita.com/furuse-kazufumi/items/2680b5b994d3d4429f56)
- [「Transformer 脱却した」と「脱却が default」のあいだ #22](https://fullsense.qiita.com/furuse-kazufumi/items/d84e4d1f8a8f409861b0)
- 体系編（再掲）: [llive 完全解説 (6) 「Transformer の外」](https://fullsense.qiita.com/furuse-kazufumi/items/fa9cfbdbdebecf1c7c3b)

---

## 第 8 幕 — llcore: Transformer のコアに進化を組み込む

脱却の模索は「コアそのものを進化させる」発想へ。CPU だけで Transformer コアの進化を回す llcore の幕。

- [llcore — Transformer のコアを CPU で進化させる #32](https://fullsense.qiita.com/furuse-kazufumi/items/88ed294aa107330c6894)
- 第三軸③: [3 実験で詰めた話 #33](https://fullsense.qiita.com/furuse-kazufumi/items/21d6c4dcfde204062a89)（[かみくだき版](https://fullsense.qiita.com/furuse-kazufumi/items/9c466e85f3afd5939347)）
- 第三軸 arc: [6 段の実験 + 生物学で俯瞰 #34](https://fullsense.qiita.com/furuse-kazufumi/items/ff1f2b6c29e41abab10d)（[かみくだき版](https://fullsense.qiita.com/furuse-kazufumi/items/5a1124083298fdbcb9e6)）

---

## 第 9 幕 — 「嘘の進化」を許さない: 検証と反証

異常に良い結果が出たら、勝った気になる前に内訳を疑う。FullSense の研究規律 (honest disclosure) が形になった幕。

- ベンチの罠: [llive vs 他 LLM ベンチ — 動作確認の罠](https://fullsense.qiita.com/furuse-kazufumi/items/f2ebf45621d8f85399c9) ／ [Quiz bench Debug vs Release — 統計指標付き](https://fullsense.qiita.com/furuse-kazufumi/items/87dc2abff45b488f56a4)
- [「眼鏡が飽和すると選択圧は無力」反証で鍛える #29](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56)（[📗 かみくだき版](https://fullsense.qiita.com/furuse-kazufumi/items/f822f8c8b01cd7b16713)）
- 検証 arc: [(#35-00) SMT より SDP/Lyapunov](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6)（[📗 かみくだき版](https://fullsense.qiita.com/furuse-kazufumi/items/a8118f557dda5c5e998c)） → [(#35-01) 検査器の梯子](https://fullsense.qiita.com/furuse-kazufumi/items/71f05f901fd9a2de6de5)（[📗 かみくだき版](https://fullsense.qiita.com/furuse-kazufumi/items/6b48b75c99e5d4b7d6b8)） → [(#35-02) 「良すぎる数値」を疑え](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)（[📗 かみくだき版](https://fullsense.qiita.com/furuse-kazufumi/items/146d5e2b27dabc59e799)）

---

## 第 10 幕 — 現在地: 進化型 AI の開発

検証器に守られた進化 (verified evolution) を、おもちゃの Transformer コアから**実 LLM** へ配線する段階に入っています（llcore R-LLM thread / llive 実 LLM 進化本走行）。次の記事はこの幕から生まれます — 最新状況は [#34](https://fullsense.qiita.com/furuse-kazufumi/items/ff1f2b6c29e41abab10d) と [#35 シリーズ](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6) の末尾が現在の前線です。

---

## サイドストーリー（本編と並走する読み物）

**ビジョン / 哲学**:

- [Will Caster と Andrew NDR114 が目指したもの — ビジョン論](https://fullsense.qiita.com/furuse-kazufumi/items/e72192c75ff461d72601)
- [「三自の精神」を AI に課す — マネジャー流 AI 運用論](https://fullsense.qiita.com/furuse-kazufumi/items/faca5557d51a06a657f4)
- [「第二の脳」シリーズ（6 部構成・大著）](https://fullsense.qiita.com/furuse-kazufumi/items/18dd57dcabbc84af9f02)

**開発マラソン記（臨場感ドキュメンタリー）**:

- [1 セッション 5409 テスト緑 #20](https://fullsense.qiita.com/furuse-kazufumi/items/96dc8af5b361ee44877b)
- [3 日 8 リポ #21](https://fullsense.qiita.com/furuse-kazufumi/items/4d4a2083c32acf1d96be)
- [15 時間前倒し #23](https://fullsense.qiita.com/furuse-kazufumi/items/851b516f96fe54c176be)

**開発体制メタ**:

- [AI に AI を部下として使わせる「二本柱」#31](https://fullsense.qiita.com/furuse-kazufumi/items/71c2304718ad5829d2d7)

---

> **メンテ note（編集者向け）**: 本 index は 56 記事の team URL 直リンクを 10 フェーズ物語アーク（正本 = 開発物語: llmesh → llove → llive → llcore）に再配置したもの。記事を再投稿しても URL (item id) は不変なのでリンクは保たれる。第 6 幕の総まとめ 2 版は将来 1 本へ統合候補。SVG 化 / かみくだき版整備 / 公開 Qiita → Team 誘導は backlog。

---

# English

# FullSense Knowledge Base — A Reading-Order Guide Told as a Development Story

> If you read this team's articles in posting order, the topics jump around and it gets hard to follow, so I've rearranged them to trace the **FullSense development story (10 acts)**.
> The FullSense products were born in the order **llmesh → llove → llive → llcore**. Each act stands on its own, but read top-to-bottom they connect into a single story — from "groping toward local-LLM coordination" all the way to "building an evolutionary AI."
> If you're in a hurry, just the **three articles in the Prologue** are enough to grasp the big picture.

---

## Prologue — Start with these 3 (the big picture)

1. [From an AI that reasons to a "cognitive OS that predicts" — a 1-week digest of FullSense development](https://fullsense.qiita.com/furuse-kazufumi/items/1f71a3e5bb830cb51b80) — the shortest summary
2. [From "just using AI" to "giving AI a secretary" — an attentive AI that runs on your home PC](https://fullsense.qiita.com/furuse-kazufumi/items/cda72a85bf20524eb8f5) — the entry point for non-engineers
3. [llive full guide (0) — series index: 8 major-category articles + the overall map](https://fullsense.qiita.com/furuse-kazufumi/items/d3a411523a01cb9ddd66) — the table of contents for the technical guides

---

## Map of the story (10 acts)

| Act | What happened | Main articles |
|---|---|---|
| 1 | Groping toward local-LLM coordination (the starting point) | HISTORY, development log |
| 2 | Introducing Raptor to secure things + laying groundwork (corpus-first) | Corpus-first, Second-brain spiral |
| 3 | Toward "a form that can hand over lots of information" — mcp-3d / llmesh | (thin coverage) |
| 4 | Wrapping Qwen with llive (turning the LLM into a material generator) | Brief API, MATH, CABT… |
| 5 | Verifying behavior through the llove interface | (thin coverage) |
| 6 | Giving llive the nature of an evolutionary program — lldarwin | #24 series, #25–#30 |
| 7 | Groping to break away from Qwen / Transformer | #18, #19, #22 |
| 8 | llcore — embedding an evolutionary algorithm into Transformer | #32, #33, #34 |
| 9 | Thorough evaluation so no "fake evolution" slips through — verification and refutation | #29, #35 series |
| 10 | Currently developing an evolutionary AI (where we are now) | — |

---

## Act 1 — Groping toward local-LLM coordination (the starting point)

It all began with a plain desire: "I want to make the local LLMs on my home PC work together." If you want to read it as a chronicle, start with these two.

- [Development history and design concepts of the three FullSense products (llmesh → llove → llive)](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) — the chronology of the whole story
- [5 days of llive development history](https://fullsense.qiita.com/furuse-kazufumi/items/504036f1116fcd976dd3)

---

## Act 2 — The wall of security and Raptor, and the groundwork

Since we handle information that can't leave the premises, securing it came first. We introduced Raptor (a fork that turns Claude Code into a security agent), and with that Raptor we accumulated a paper corpus (RAD, 21+ fields, ~50,000 documents). That became the **groundwork** for the evolutionary-algorithm development that followed.

- [Corpus-first strategy — collecting 50,000 papers in advance](https://fullsense.qiita.com/furuse-kazufumi/items/75d682ddefa5aeb738b8)
- [30 years of development experience + Perplexity + Claude Code + TRIZ + a 50,000-document corpus](https://fullsense.qiita.com/furuse-kazufumi/items/a30e7f893874d6901dee)

> A dedicated article on Raptor itself isn't posted yet (it's mentioned within HISTORY).

---

## Act 3 — Toward "a form that can hand over lots of information": mcp-3d and llmesh

With mcp-3d for 3D/spatial assets and llmesh as an on-prem LLM hub, we put in place "a form that can safely hand over lots of information to an LLM." Dedicated articles for this act are thin — see the relevant chapter of [HISTORY](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) (a dedicated article is in the backlog).

---

## Act 4 — The birth of llive: wrapping Qwen as a "material generator"

A cognitive OS that wraps the LLM not as a judge but as a **material generator** = the birth of llive. This is the act where features came online all at once.

1. [Brief API and progressive matrix — overhead < 1 %](https://fullsense.qiita.com/furuse-kazufumi/items/60537278f72f8a9fc2dc) — handing structured work units in from the outside
2. [32 requirements + Brief API + COG-FX + MATH + benchmarks in one day](https://fullsense.qiita.com/furuse-kazufumi/items/bfa83d01e79028132438) — a record of the ramp-up
3. [Organizing llive's thinking layer with 10 thought factors](https://fullsense.qiita.com/furuse-kazufumi/items/4de8dcff1cf4c2ab9bdc)
4. Making it strong at math: [the first step](https://fullsense.qiita.com/furuse-kazufumi/items/2c4a993937c373c464f6) → [the formal-verification gate (MATH-02)](https://fullsense.qiita.com/furuse-kazufumi/items/acb5f5e0dabe2020c166) → [observing grounding with 6 real Briefs](https://fullsense.qiita.com/furuse-kazufumi/items/29b26774667b3af3a04e)
5. [7 approaches to advancing the Transformer block (CABT)](https://fullsense.qiita.com/furuse-kazufumi/items/a6804f6b8c47605177a8) / [Requirements definition with LLM × KJ method × MindMap (CREAT)](https://fullsense.qiita.com/furuse-kazufumi/items/0c6deb6f462843a71094)
6. [Designing an invisible annotation channel](https://fullsense.qiita.com/furuse-kazufumi/items/851773b6cfe85c7811a4) / [USV (Unit-Separated Values), the successor to CSV/TSV](https://fullsense.qiita.com/furuse-kazufumi/items/fda1d13c689095720534)
7. Sense of distance from Qwen: [a 5-stage roadmap to break free of the dependency](https://fullsense.qiita.com/furuse-kazufumi/items/ba3a0f41e42ec533a3a1) / [llive complementing Qwen mutually](https://fullsense.qiita.com/furuse-kazufumi/items/f400cf06e86b350b055c)
8. [Is llive's structure original? — an inspection of 8 differentiators](https://fullsense.qiita.com/furuse-kazufumi/items/0c1d5ebd6b0656ba74e1)

---

## Act 5 — Using the llove interface to confirm "does it actually run?"

With the TUI dashboard llove, we made it possible for humans to watch llive/llmesh actually running. This act, too, has thin dedicated coverage — see [HISTORY](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) / [the entry point for non-engineers](https://fullsense.qiita.com/furuse-kazufumi/items/cda72a85bf20524eb8f5).

---

## Act 6 — Giving llive "evolution": lldarwin

An attempt to run llive not as a single AI but as a **derived population of N individuals** that turns over across generations. Learning from failure (monoculture), the selection-pressure component lldarwin was born — one of the climaxes of this story.

**Systematic reference (llive full guide, 8 articles)**:

1. [(1) The "LLM that doesn't forget": 4-layer memory + Bayesian surprise gating](https://fullsense.qiita.com/furuse-kazufumi/items/2732122ed0a4c9ace0af)
2. [(2) The "AI that thinks on 10 axes": thought factors × COG-MESH × triple stripes](https://fullsense.qiita.com/furuse-kazufumi/items/94fae20cea5e53d1358f)
3. [(3) "Contradictions can be computed": structural evolution × TRIZ 40 principles × Z3 verification](https://fullsense.qiita.com/furuse-kazufumi/items/198eadaee7c380c426d5)
4. [(4) The "converging brain" B-series: SynapticSelector / UCB1](https://fullsense.qiita.com/furuse-kazufumi/items/9839392b82e3372dbdc9)
5. [(5) The "AI where the population learns": a summary of v0.B/C/D/E derived-population evolution](https://fullsense.qiita.com/furuse-kazufumi/items/c999960660e25bdb5b66)
6. [(6) "Outside the Transformer": Mamba / Jamba / RWKV / Diffusion](https://fullsense.qiita.com/furuse-kazufumi/items/fa9cfbdbdebecf1c7c3b)
7. [(7) The "AI with review": runtime_metadata × Approval Bus](https://fullsense.qiita.com/furuse-kazufumi/items/f3ef0430798ff9df07ab)
8. [(8) "Making the eyeglasses": lleval — honest disclosure 5+1 factors](https://fullsense.qiita.com/furuse-kazufumi/items/4b98e2a877cf746ce8e3)

**The lldarwin story (in this order)**:

1. [I evolved an AI for 500 generations and only 2 survived — the honest disclosure of monoculture #25](https://fullsense.qiita.com/furuse-kazufumi/items/8b510aed45cdfad71909)
2. [Just "measuring with eyeglasses" doesn't make it evolve — selection pressure lldarwin #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba) ([📗 plain-language digest](https://fullsense.qiita.com/furuse-kazufumi/items/1d9eeb1b739623dbc285))
3. [I rebuilt AI evolution overnight #27](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0) ([📗 plain-language digest](https://fullsense.qiita.com/furuse-kazufumi/items/6b134e5a4f87963681c2))
4. [A "conductor" makes the evolutionary population play in ensemble and answer #28](https://fullsense.qiita.com/furuse-kazufumi/items/333165c2d5704e652721)
5. [A lineage of techniques for "showing" evolution #30](https://fullsense.qiita.com/furuse-kazufumi/items/0e221d447b7a8ad66d22)

**Overall wrap-up (2 editions)**: [📘 Plain-language edition — llive "mega-evolution"!](https://fullsense.qiita.com/furuse-kazufumi/items/49f9e2359c77dce0ed4f) / [📗 Full edition — evolution arc](https://fullsense.qiita.com/furuse-kazufumi/items/0819897256c2e46831ad)

---

## Act 7 — Groping to break away from the Transformer

Is there a path that doesn't rely on the core Qwen / Transformer? An examination of non-Transformer options like Mamba / RWKV, and an account of "where the break-away stands now."

- [Seriously building an AI that runs even on an old laptop with no GPU](https://fullsense.qiita.com/furuse-kazufumi/items/a10147101bb6b81b811c) / [the story of making that the protagonist](https://fullsense.qiita.com/furuse-kazufumi/items/2680b5b994d3d4429f56)
- [Between "we broke away from the Transformer" and "break-away is the default" #22](https://fullsense.qiita.com/furuse-kazufumi/items/d84e4d1f8a8f409861b0)
- Systematic edition (reprise): [llive full guide (6) "Outside the Transformer"](https://fullsense.qiita.com/furuse-kazufumi/items/fa9cfbdbdebecf1c7c3b)

---

## Act 8 — llcore: embedding evolution into the Transformer core

Groping for a break-away led to the idea of "evolving the core itself." This is the act of llcore, which runs the evolution of a Transformer core on CPU alone.

- [llcore — evolving the Transformer core on CPU #32](https://fullsense.qiita.com/furuse-kazufumi/items/88ed294aa107330c6894)
- Third axis ③: [the story of nailing it down with 3 experiments #33](https://fullsense.qiita.com/furuse-kazufumi/items/21d6c4dcfde204062a89) ([plain-language edition](https://fullsense.qiita.com/furuse-kazufumi/items/9c466e85f3afd5939347))
- Third-axis arc: [6 stages of experiments + a bird's-eye view through biology #34](https://fullsense.qiita.com/furuse-kazufumi/items/ff1f2b6c29e41abab10d) ([plain-language edition](https://fullsense.qiita.com/furuse-kazufumi/items/5a1124083298fdbcb9e6))

---

## Act 9 — Allowing no "fake evolution": verification and refutation

When abnormally good results appear, doubt the breakdown before you feel like you've won. This is the act where FullSense's research discipline (honest disclosure) took shape.

- Traps of benchmarking: [llive vs. other LLMs benchmark — the trap of behavior-checking](https://fullsense.qiita.com/furuse-kazufumi/items/f2ebf45621d8f85399c9) / [Quiz bench Debug vs Release — with statistical metrics](https://fullsense.qiita.com/furuse-kazufumi/items/87dc2abff45b488f56a4)
- ["Once the eyeglasses saturate, selection pressure is powerless" — hardened by refutation #29](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56) ([📗 plain-language digest](https://fullsense.qiita.com/furuse-kazufumi/items/f822f8c8b01cd7b16713))
- Verification arc: [(#35-00) SDP/Lyapunov over SMT](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6) ([📗 plain-language digest](https://fullsense.qiita.com/furuse-kazufumi/items/a8118f557dda5c5e998c)) → [(#35-01) the ladder of checkers](https://fullsense.qiita.com/furuse-kazufumi/items/71f05f901fd9a2de6de5) ([📗 plain-language digest](https://fullsense.qiita.com/furuse-kazufumi/items/6b48b75c99e5d4b7d6b8)) → [(#35-02) doubt the "too-good numbers"](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615) ([📗 plain-language digest](https://fullsense.qiita.com/furuse-kazufumi/items/146d5e2b27dabc59e799))

---

## Act 10 — Where we are now: developing an evolutionary AI

We've entered the stage of wiring verified evolution (protected by checkers) from a toy Transformer core to a **real LLM** (the llcore R-LLM thread / the main run of llive real-LLM evolution). The next articles will be born from this act — for the latest status, the tail ends of [#34](https://fullsense.qiita.com/furuse-kazufumi/items/ff1f2b6c29e41abab10d) and the [#35 series](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6) are the current front line.

---

## Side stories (companion reads alongside the main arc)

**Vision / philosophy**:

- [What Will Caster and Andrew NDR114 were aiming for — on vision](https://fullsense.qiita.com/furuse-kazufumi/items/e72192c75ff461d72601)
- [Imposing the "spirit of the three selves" on AI — a manager's theory of AI operations](https://fullsense.qiita.com/furuse-kazufumi/items/faca5557d51a06a657f4)
- [The "second brain" series (6-part magnum opus)](https://fullsense.qiita.com/furuse-kazufumi/items/18dd57dcabbc84af9f02)

**Development marathon logs (immersive documentaries)**:

- [5,409 tests green in one session #20](https://fullsense.qiita.com/furuse-kazufumi/items/96dc8af5b361ee44877b)
- [8 repos in 3 days #21](https://fullsense.qiita.com/furuse-kazufumi/items/4d4a2083c32acf1d96be)
- [15 hours ahead of schedule #23](https://fullsense.qiita.com/furuse-kazufumi/items/851b516f96fe54c176be)

**Development-structure meta**:

- [Making an AI use another AI as a subordinate: the "two pillars" #31](https://fullsense.qiita.com/furuse-kazufumi/items/71c2304718ad5829d2d7)

---

> **Maintenance note (for editors)**: This index rearranges direct team-URL links to 56 articles into a 10-act story arc (the canonical source = the development story: llmesh → llove → llive → llcore). Even if an article is re-posted, its URL (item id) stays the same, so the links hold. The two wrap-up editions in Act 6 are candidates for merging into one in the future. SVG-ification / maintaining the plain-language editions / steering from public Qiita → Team are in the backlog.

---

# 中文

# FullSense 知识库 — 以开发故事串联的阅读顺序指南

> 如果按发布时间顺序阅读本团队的文章，话题会来回跳跃、难以连贯，所以我把它们重新排列，按照 **FullSense 开发故事（10 幕）** 来呈现。
> FullSense 的产品是按 **llmesh → llove → llive → llcore** 的顺序诞生的。每一幕都可以独立阅读，但从上往下读，它们会连成一个完整的故事 —— 从「摸索本地 LLM 协同」一路走到「开发进化型 AI」。
> 时间紧的话，光读 **序章里的 3 篇** 就足以把握全貌。

---

## 序章 — 先读这 3 篇（全貌）

1. [从会推理的 AI 到「会预测的认知 OS」 — FullSense 开发一周摘要](https://fullsense.qiita.com/furuse-kazufumi/items/1f71a3e5bb830cb51b80) — 最短的总结
2. [从「只是使用 AI」到「给 AI 配一个秘书」 — 在家用 PC 上运行的体贴 AI](https://fullsense.qiita.com/furuse-kazufumi/items/cda72a85bf20524eb8f5) — 面向非工程师的入口
3. [llive 完全解说 (0) — 系列索引：8 篇大分类文章 + 全局图](https://fullsense.qiita.com/furuse-kazufumi/items/d3a411523a01cb9ddd66) — 技术解说的目录

---

## 故事地图（10 幕）

| 幕 | 发生了什么 | 主要文章 |
|---|---|---|
| 1 | 摸索本地 LLM 的协同（出发点） | HISTORY、开发履历 |
| 2 | 为确保安全引入 Raptor + 埋下伏笔（语料先行） | 语料先行、第二大脑螺旋 |
| 3 | 走向「能交付大量信息的形态」 — mcp-3d / llmesh | （文章较少） |
| 4 | 用 llive 包装 Qwen（把 LLM 当作素材生成者） | Brief API、MATH、CABT… |
| 5 | 用 llove 这个 Interface 确认是否能运行 | （文章较少） |
| 6 | 赋予 llive 进化程序的性质 — lldarwin | #24 系列、#25–#30 |
| 7 | 摸索摆脱 Qwen / Transformer | #18、#19、#22 |
| 8 | llcore — 把进化算法嵌入 Transformer | #32、#33、#34 |
| 9 | 彻底评估以免出现「虚假的进化」 — 验证与反证 | #29、#35 系列 |
| 10 | 正在着手开发进化型 AI（当前位置） | — |

---

## 第 1 幕 — 摸索本地 LLM 的协同（出发点）

一切始于一个朴素的愿望：「我想让家用 PC 上的本地 LLM 协同起来。」如果要当作编年史来读，就从这两篇开始。

- [FullSense 三款产品的开发履历与设计理念（llmesh → llove → llive）](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) — 整个故事的年表
- [llive 开发履历 5 天](https://fullsense.qiita.com/furuse-kazufumi/items/504036f1116fcd976dd3)

---

## 第 2 幕 — 安全之墙与 Raptor，以及伏笔

既然要处理不能外发的信息，确保安全便是首要之务。我们引入了 Raptor（把 Claude Code 变成安全代理的 fork），并用这个 Raptor 积累了论文语料库（RAD，21+ 个领域、约 5 万件）。这后来成了进化算法开发的**伏笔**。

- [语料先行战略 — 先收集 5 万篇论文](https://fullsense.qiita.com/furuse-kazufumi/items/75d682ddefa5aeb738b8)
- [30 年开发经验 + Perplexity + Claude Code + TRIZ + 5 万件语料库](https://fullsense.qiita.com/furuse-kazufumi/items/a30e7f893874d6901dee)

> Raptor 本身的专用文章尚未发布（在 HISTORY 中有提及）。

---

## 第 3 幕 — 走向「能交付大量信息的形态」：mcp-3d 与 llmesh

借助面向 3D/空间资产的 mcp-3d，以及作为 on-prem LLM hub 的 llmesh，我们搭建出「能安全地把大量信息交给 LLM 的形态」。这一幕的专用文章较少 —— 请参阅 [HISTORY](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) 中相应的章节（专用文章在 backlog 中）。

---

## 第 4 幕 — llive 诞生：把 Qwen 当作「素材生成者」来包装

把 LLM 不作为判断者、而作为**素材生成者**来套上的认知 OS = llive 的诞生。这是各项功能一口气立起来的一幕。

1. [Brief API and progressive matrix — overhead < 1 %](https://fullsense.qiita.com/furuse-kazufumi/items/60537278f72f8a9fc2dc) — 从外部交付结构化的 work unit
2. [一天内 32 项需求 + Brief API + COG-FX + MATH + 基准测试](https://fullsense.qiita.com/furuse-kazufumi/items/bfa83d01e79028132438) — 起步阶段的记录
3. [用 10 个思考因子梳理 llive 的思考层](https://fullsense.qiita.com/furuse-kazufumi/items/4de8dcff1cf4c2ab9bdc)
4. 让它擅长数学：[第一步](https://fullsense.qiita.com/furuse-kazufumi/items/2c4a993937c373c464f6) → [形式验证门 (MATH-02)](https://fullsense.qiita.com/furuse-kazufumi/items/acb5f5e0dabe2020c166) → [用 6 个真实 Brief 观察 grounding](https://fullsense.qiita.com/furuse-kazufumi/items/29b26774667b3af3a04e)
5. [Transformer 块高级化的 7 种方法 (CABT)](https://fullsense.qiita.com/furuse-kazufumi/items/a6804f6b8c47605177a8) ／ [用 LLM × KJ 法 × MindMap 做需求定义 (CREAT)](https://fullsense.qiita.com/furuse-kazufumi/items/0c6deb6f462843a71094)
6. [不可见注释通道的设计](https://fullsense.qiita.com/furuse-kazufumi/items/851773b6cfe85c7811a4) ／ [CSV/TSV 的后继者 USV (Unit-Separated Values)](https://fullsense.qiita.com/furuse-kazufumi/items/fda1d13c689095720534)
7. 与 Qwen 的距离感：[摆脱依赖的 5 阶段路线图](https://fullsense.qiita.com/furuse-kazufumi/items/ba3a0f41e42ec533a3a1) ／ [与 Qwen 相互补完的 llive](https://fullsense.qiita.com/furuse-kazufumi/items/f400cf06e86b350b055c)
8. [llive 的结构是否原创 — 8 个差异化要素的检视](https://fullsense.qiita.com/furuse-kazufumi/items/0c1d5ebd6b0656ba74e1)

---

## 第 5 幕 — 用 llove 这个 Interface 确认「能不能动」

借助 TUI 仪表盘 llove，让人类能够看到 llive/llmesh 实际运行的样子。这一幕的专用文章也较少 —— 请参阅 [HISTORY](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) ／ [面向非工程师的入口](https://fullsense.qiita.com/furuse-kazufumi/items/cda72a85bf20524eb8f5)。

---

## 第 6 幕 — 赋予 llive「进化」：lldarwin

不把 llive 当作单个 AI，而是当作 **N 个个体的派生种群**，让它代际更替的尝试。从失败（monoculture）中学习，选择压组件 lldarwin 由此诞生 —— 这是本故事的高潮之一。

**体系参考（llive 完全解说・8 篇）**:

1. [(1)「不会遗忘的 LLM」：4 层记忆 + Bayesian surprise gating](https://fullsense.qiita.com/furuse-kazufumi/items/2732122ed0a4c9ace0af)
2. [(2)「在 10 个轴上思考的 AI」：思考因子 × COG-MESH × 三重条纹](https://fullsense.qiita.com/furuse-kazufumi/items/94fae20cea5e53d1358f)
3. [(3)「矛盾是可以计算的」：结构进化 × TRIZ 40 原理 × Z3 验证](https://fullsense.qiita.com/furuse-kazufumi/items/198eadaee7c380c426d5)
4. [(4)「收敛的大脑」B-series：SynapticSelector / UCB1](https://fullsense.qiita.com/furuse-kazufumi/items/9839392b82e3372dbdc9)
5. [(5)「种群在学习的 AI」：v0.B/C/D/E 派生种群进化总结](https://fullsense.qiita.com/furuse-kazufumi/items/c999960660e25bdb5b66)
6. [(6)「Transformer 之外」：Mamba / Jamba / RWKV / Diffusion](https://fullsense.qiita.com/furuse-kazufumi/items/fa9cfbdbdebecf1c7c3b)
7. [(7)「带审查的 AI」：runtime_metadata × Approval Bus](https://fullsense.qiita.com/furuse-kazufumi/items/f3ef0430798ff9df07ab)
8. [(8)「制作眼镜」：lleval — honest disclosure 5+1 因子](https://fullsense.qiita.com/furuse-kazufumi/items/4b98e2a877cf746ce8e3)

**lldarwin 故事（按此顺序）**:

1. [让 AI 进化 500 代后只剩下 2 个 — monoculture 的 honest disclosure #25](https://fullsense.qiita.com/furuse-kazufumi/items/8b510aed45cdfad71909)
2. [光「用眼镜测量」并不会进化 — 选择压 lldarwin #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)（[📗 通俗版](https://fullsense.qiita.com/furuse-kazufumi/items/1d9eeb1b739623dbc285)）
3. [一夜之间重做了 AI 进化 #27](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)（[📗 通俗版](https://fullsense.qiita.com/furuse-kazufumi/items/6b134e5a4f87963681c2)）
4. [让「指挥者」带领进化种群合奏作答 #28](https://fullsense.qiita.com/furuse-kazufumi/items/333165c2d5704e652721)
5. [「展示」进化之技术的谱系 #30](https://fullsense.qiita.com/furuse-kazufumi/items/0e221d447b7a8ad66d22)

**总结（2 个版本）**: [📘 通俗版 — llive「超级进化」！](https://fullsense.qiita.com/furuse-kazufumi/items/49f9e2359c77dce0ed4f) ／ [📗 完整版 — evolution arc](https://fullsense.qiita.com/furuse-kazufumi/items/0819897256c2e46831ad)

---

## 第 7 幕 — 摸索摆脱 Transformer

有没有不依赖核心 Qwen / Transformer 的路？对 Mamba / RWKV 等 non-Transformer 的考察，以及对「摆脱的当前位置」的梳理。

- [认真打造一台连没有 GPU 的旧笔记本也能跑的 AI](https://fullsense.qiita.com/furuse-kazufumi/items/a10147101bb6b81b811c) ／ [让它担任主角的故事](https://fullsense.qiita.com/furuse-kazufumi/items/2680b5b994d3d4429f56)
- [在「已摆脱 Transformer」与「摆脱是 default」之间 #22](https://fullsense.qiita.com/furuse-kazufumi/items/d84e4d1f8a8f409861b0)
- 体系篇（再次列出）：[llive 完全解说 (6)「Transformer 之外」](https://fullsense.qiita.com/furuse-kazufumi/items/fa9cfbdbdebecf1c7c3b)

---

## 第 8 幕 — llcore：把进化嵌入 Transformer 的核心

对摆脱的摸索引出了「进化核心本身」的想法。这是 llcore 的一幕 —— 仅用 CPU 来运转 Transformer 核心的进化。

- [llcore — 用 CPU 进化 Transformer 的核心 #32](https://fullsense.qiita.com/furuse-kazufumi/items/88ed294aa107330c6894)
- 第三轴③：[用 3 个实验敲定的故事 #33](https://fullsense.qiita.com/furuse-kazufumi/items/21d6c4dcfde204062a89)（[通俗版](https://fullsense.qiita.com/furuse-kazufumi/items/9c466e85f3afd5939347)）
- 第三轴 arc：[6 个阶段的实验 + 用生物学俯瞰 #34](https://fullsense.qiita.com/furuse-kazufumi/items/ff1f2b6c29e41abab10d)（[通俗版](https://fullsense.qiita.com/furuse-kazufumi/items/5a1124083298fdbcb9e6)）

---

## 第 9 幕 — 不容许「虚假的进化」：验证与反证

当出现异常优异的结果时，在自以为赢了之前先怀疑其内部构成。这是 FullSense 的研究纪律（honest disclosure）成形的一幕。

- 基准测试的陷阱：[llive vs 其他 LLM 基准 — 动作确认的陷阱](https://fullsense.qiita.com/furuse-kazufumi/items/f2ebf45621d8f85399c9) ／ [Quiz bench Debug vs Release — 附统计指标](https://fullsense.qiita.com/furuse-kazufumi/items/87dc2abff45b488f56a4)
- [「眼镜一旦饱和，选择压便无力」用反证来锤炼 #29](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56)（[📗 通俗版](https://fullsense.qiita.com/furuse-kazufumi/items/f822f8c8b01cd7b16713)）
- 验证 arc：[(#35-00) 比起 SMT，选 SDP/Lyapunov](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6)（[📗 通俗版](https://fullsense.qiita.com/furuse-kazufumi/items/a8118f557dda5c5e998c)） → [(#35-01) 检查器的梯子](https://fullsense.qiita.com/furuse-kazufumi/items/71f05f901fd9a2de6de5)（[📗 通俗版](https://fullsense.qiita.com/furuse-kazufumi/items/6b48b75c99e5d4b7d6b8)） → [(#35-02) 怀疑「太好的数字」](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)（[📗 通俗版](https://fullsense.qiita.com/furuse-kazufumi/items/146d5e2b27dabc59e799)）

---

## 第 10 幕 — 当前位置：开发进化型 AI

我们已进入这样的阶段：把受检查器守护的进化（verified evolution）从玩具级 Transformer 核心配线到**真实 LLM**（llcore R-LLM thread / llive 真实 LLM 进化的正式运行）。接下来的文章将从这一幕诞生 —— 最新状况请看 [#34](https://fullsense.qiita.com/furuse-kazufumi/items/ff1f2b6c29e41abab10d) 与 [#35 系列](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6) 的末尾，那是当前的最前线。

---

## 番外篇（与正篇并行的读物）

**愿景 / 哲学**:

- [Will Caster 与 Andrew NDR114 所追求的 — 愿景论](https://fullsense.qiita.com/furuse-kazufumi/items/e72192c75ff461d72601)
- [向 AI 施加「三自精神」 — 经理流 AI 运营论](https://fullsense.qiita.com/furuse-kazufumi/items/faca5557d51a06a657f4)
- [「第二大脑」系列（6 部构成・大著）](https://fullsense.qiita.com/furuse-kazufumi/items/18dd57dcabbc84af9f02)

**开发马拉松记（临场感纪录片）**:

- [一个会话 5409 个测试全绿 #20](https://fullsense.qiita.com/furuse-kazufumi/items/96dc8af5b361ee44877b)
- [3 天 8 个仓库 #21](https://fullsense.qiita.com/furuse-kazufumi/items/4d4a2083c32acf1d96be)
- [提前 15 小时 #23](https://fullsense.qiita.com/furuse-kazufumi/items/851b516f96fe54c176be)

**开发体制 meta**:

- [让 AI 把 AI 当作下属来用的「二本柱」#31](https://fullsense.qiita.com/furuse-kazufumi/items/71c2304718ad5829d2d7)

---

> **维护 note（面向编辑）**: 本 index 把指向 56 篇文章的 team URL 直链，重新配置成 10 幕故事弧（正本 = 开发故事：llmesh → llove → llive → llcore）。即使重新发布文章，其 URL (item id) 也不变，所以链接得以保持。第 6 幕的两个总结版本是将来合并为一篇的候选。SVG 化 / 通俗版的维护 / 从公开 Qiita → Team 的引导都在 backlog 中。

---

# 한국어

# FullSense 지식 베이스 — 개발 이야기로 읽는 순서 가이드

> 이 팀의 글은 게시일 순서로 읽으면 화제가 앞뒤로 오가 읽기 어렵기 때문에, **FullSense 개발 이야기(10막)** 를 따라 다시 배열했습니다.
> FullSense의 제품은 **llmesh → llove → llive → llcore** 순서로 태어났습니다. 각 막은 독립적으로 읽을 수 있지만, 위에서부터 읽으면 「로컬 LLM 연계 모색」에서 「진화형 AI 개발」까지 하나의 이야기로 이어집니다.
> 급한 분은 **프롤로그의 3편** 만으로도 전체 그림을 잡을 수 있습니다.

---

## 프롤로그 — 우선 이 3편 (전체 그림)

1. [추론하는 AI에서 「예측하는 인지 OS」로 — FullSense 개발 1주일 다이제스트](https://fullsense.qiita.com/furuse-kazufumi/items/1f71a3e5bb830cb51b80) — 가장 짧은 요약
2. [AI를 「그냥 쓰는 것」에서 「AI에게 비서를 붙이는 것」으로 — 집 PC에서 동작하는 사려 깊은 AI](https://fullsense.qiita.com/furuse-kazufumi/items/cda72a85bf20524eb8f5) — 비엔지니어를 위한 입구
3. [llive 완전 해설 (0) — 시리즈 인덱스: 대분류 8편 + 전체도](https://fullsense.qiita.com/furuse-kazufumi/items/d3a411523a01cb9ddd66) — 기술 해설의 목차

---

## 이야기의 지도 (10막)

| 막 | 무슨 일이 일어났나 | 주요 글 |
|---|---|---|
| 1 | 로컬 LLM 연계를 모색(출발점) | HISTORY, 개발 이력 |
| 2 | 보안 확보를 위해 Raptor 도입 + 포석(코퍼스 선행) | 코퍼스 선행, 두 번째 뇌 나선 |
| 3 | 「다수의 정보를 건넬 수 있는 형태」로 — mcp-3d / llmesh | (글이 적음) |
| 4 | llive로 Qwen을 래핑(LLM을 소재 생성자로) | Brief API, MATH, CABT… |
| 5 | llove라는 Interface로 동작 확인 | (글이 적음) |
| 6 | llive에 진화 프로그램의 성질을 부여 — lldarwin | #24 시리즈, #25–#30 |
| 7 | Qwen / Transformer로부터의 탈피를 모색 | #18, #19, #22 |
| 8 | llcore — Transformer에 진화 알고리즘을 내장 | #32, #33, #34 |
| 9 | 「거짓 진화」가 나오지 않도록 철저히 평가 — 검증과 반증 | #29, #35 시리즈 |
| 10 | 진화형 AI 개발에 착수 중(현재 위치) | — |

---

## 제 1막 — 로컬 LLM 연계를 모색하다(출발점)

모든 것의 시작은 「집 PC의 로컬 LLM들을 연계시키고 싶다」는 소박한 욕구였습니다. 연표로 읽는다면 이 2편을.

- [FullSense 3개 제품의 개발 이력・설계 콘셉트(llmesh → llove → llive)](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) — 이야기 전체의 연표
- [llive 개발 이력 5일](https://fullsense.qiita.com/furuse-kazufumi/items/504036f1116fcd976dd3)

---

## 제 2막 — 보안의 벽과 Raptor, 그리고 포석

외부로 내보낼 수 없는 정보를 다루는 이상 보안 확보가 우선입니다. Raptor(Claude Code를 보안 에이전트로 만든 fork)를 도입하고, 그 Raptor로 논문 코퍼스(RAD, 21+ 분야・약 5만 건)를 축적한 것이, 훗날 진화 알고리즘 개발의 **포석**이 됩니다.

- [코퍼스 선행 전략 — 5만 건의 논문을 먼저 모은다](https://fullsense.qiita.com/furuse-kazufumi/items/75d682ddefa5aeb738b8)
- [30년의 개발 경험 + Perplexity + Claude Code + TRIZ + 5만 건 코퍼스](https://fullsense.qiita.com/furuse-kazufumi/items/a30e7f893874d6901dee)

> Raptor 자체의 전용 글은 아직 게시하지 않았습니다(HISTORY 내에서 언급).

---

## 제 3막 — 「다수의 정보를 건넬 수 있는 형태」로: mcp-3d와 llmesh

3D/공간 에셋을 위한 mcp-3d, on-prem LLM hub인 llmesh로 「LLM에게 다수의 정보를 안전하게 건넬 수 있는 형태」를 갖추었습니다. 이 막의 전용 글은 적습니다 — [HISTORY](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677)의 해당 장을 참조하세요(전용 글은 backlog).

---

## 제 4막 — llive 탄생: Qwen을 「소재 생성자」로 래핑하다

LLM을 판단자가 아니라 **소재 생성자**로 씌우는 인지 OS = llive의 탄생. 기능이 단번에 일어선 막입니다.

1. [Brief API and progressive matrix — overhead < 1 %](https://fullsense.qiita.com/furuse-kazufumi/items/60537278f72f8a9fc2dc) — 외부에서 구조화된 work unit을 건넨다
2. [하루에 요건 32건 + Brief API + COG-FX + MATH + 벤치](https://fullsense.qiita.com/furuse-kazufumi/items/bfa83d01e79028132438) — 일어선 시기의 기록
3. [10 사고 인자로 정리하는 llive 사고층](https://fullsense.qiita.com/furuse-kazufumi/items/4de8dcff1cf4c2ab9bdc)
4. 수학에 강하게 만들기: [첫걸음](https://fullsense.qiita.com/furuse-kazufumi/items/2c4a993937c373c464f6) → [형식 검증 게이트 (MATH-02)](https://fullsense.qiita.com/furuse-kazufumi/items/acb5f5e0dabe2020c166) → [실제 Brief 6건으로 grounding 관찰](https://fullsense.qiita.com/furuse-kazufumi/items/29b26774667b3af3a04e)
5. [Transformer 블록 고도화 7가지 접근(CABT)](https://fullsense.qiita.com/furuse-kazufumi/items/a6804f6b8c47605177a8) ／ [LLM × KJ법 × MindMap으로 요건 정의(CREAT)](https://fullsense.qiita.com/furuse-kazufumi/items/0c6deb6f462843a71094)
6. [비가시 어노테이션 채널 설계](https://fullsense.qiita.com/furuse-kazufumi/items/851773b6cfe85c7811a4) ／ [CSV/TSV의 후계 USV (Unit-Separated Values)](https://fullsense.qiita.com/furuse-kazufumi/items/fda1d13c689095720534)
7. Qwen과의 거리감: [의존에서 벗어나는 5단계 로드맵](https://fullsense.qiita.com/furuse-kazufumi/items/ba3a0f41e42ec533a3a1) ／ [Qwen과 상호 보완하는 llive](https://fullsense.qiita.com/furuse-kazufumi/items/f400cf06e86b350b055c)
8. [llive의 구조는 독창적인가 — 8가지 차별화 요소의 점검](https://fullsense.qiita.com/furuse-kazufumi/items/0c1d5ebd6b0656ba74e1)

---

## 제 5막 — llove라는 Interface로 「움직이는가」를 확인하다

TUI 대시보드 llove로, llive/llmesh가 실제로 동작하는 모습을 사람이 확인할 수 있게 했습니다. 이 막도 전용 글은 적습니다 — [HISTORY](https://fullsense.qiita.com/furuse-kazufumi/items/adaa273817eddff5a677) ／ [비엔지니어를 위한 입구](https://fullsense.qiita.com/furuse-kazufumi/items/cda72a85bf20524eb8f5)를 참조하세요.

---

## 제 6막 — llive에 「진화」를 부여하다: lldarwin

llive를 한 개의 AI가 아니라 **N 개체의 파생 집단**으로서 세대 교체시키는 시도. 실패(monoculture)에서 배우고, 선택압 컴포넌트 lldarwin이 태어난, 이 이야기의 클라이맥스 중 하나.

**체계 레퍼런스(llive 완전 해설・8편)**:

1. [(1) 「잊지 않는 LLM」: 4층 메모리 + Bayesian surprise gating](https://fullsense.qiita.com/furuse-kazufumi/items/2732122ed0a4c9ace0af)
2. [(2) 「10축으로 생각하는 AI」: 사고 인자 × COG-MESH × 삼중 줄무늬](https://fullsense.qiita.com/furuse-kazufumi/items/94fae20cea5e53d1358f)
3. [(3) 「모순은 계산할 수 있다」: 구조 진화 × TRIZ 40 원리 × Z3 검증](https://fullsense.qiita.com/furuse-kazufumi/items/198eadaee7c380c426d5)
4. [(4) 「수렴하는 뇌」 B-series: SynapticSelector / UCB1](https://fullsense.qiita.com/furuse-kazufumi/items/9839392b82e3372dbdc9)
5. [(5) 「집단이 학습하는 AI」: v0.B/C/D/E 파생 집단 진화 총괄](https://fullsense.qiita.com/furuse-kazufumi/items/c999960660e25bdb5b66)
6. [(6) 「Transformer의 바깥」: Mamba / Jamba / RWKV / Diffusion](https://fullsense.qiita.com/furuse-kazufumi/items/fa9cfbdbdebecf1c7c3b)
7. [(7) 「심사가 붙은 AI」: runtime_metadata × Approval Bus](https://fullsense.qiita.com/furuse-kazufumi/items/f3ef0430798ff9df07ab)
8. [(8) 「안경을 만든다」: lleval — honest disclosure 5+1 인자](https://fullsense.qiita.com/furuse-kazufumi/items/4b98e2a877cf746ce8e3)

**lldarwin 이야기(이 순서로)**:

1. [AI를 500세대 진화시켰더니 둘만 남았다 — monoculture의 honest disclosure #25](https://fullsense.qiita.com/furuse-kazufumi/items/8b510aed45cdfad71909)
2. [「안경으로 측정」만으로는 진화하지 않는다 — 선택압 lldarwin #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba) ([📗 쉬운 버전](https://fullsense.qiita.com/furuse-kazufumi/items/1d9eeb1b739623dbc285))
3. [하룻밤 사이에 AI 진화를 다시 만들었다 #27](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0) ([📗 쉬운 버전](https://fullsense.qiita.com/furuse-kazufumi/items/6b134e5a4f87963681c2))
4. [진화 집단을 「지휘자」가 합주시켜 답한다 #28](https://fullsense.qiita.com/furuse-kazufumi/items/333165c2d5704e652721)
5. [진화를 「보여주는」 기술의 계보 #30](https://fullsense.qiita.com/furuse-kazufumi/items/0e221d447b7a8ad66d22)

**총정리(2판)**: [📘 쉬운 해설판 — llive "메가 진화"!](https://fullsense.qiita.com/furuse-kazufumi/items/49f9e2359c77dce0ed4f) ／ [📗 완전판 — evolution arc](https://fullsense.qiita.com/furuse-kazufumi/items/0819897256c2e46831ad)

---

## 제 7막 — Transformer로부터의 탈피를 모색하다

코어인 Qwen / Transformer에 의존하지 않는 길은 있는가. Mamba / RWKV 등 non-Transformer의 검토와 「탈피의 현재 위치」 정리.

- [GPU가 없는 오래된 노트북 PC에서도 동작하는 AI를 진지하게 만든다](https://fullsense.qiita.com/furuse-kazufumi/items/a10147101bb6b81b811c) ／ [그 주역화 이야기](https://fullsense.qiita.com/furuse-kazufumi/items/2680b5b994d3d4429f56)
- [「Transformer를 탈피했다」와 「탈피가 default」 사이 #22](https://fullsense.qiita.com/furuse-kazufumi/items/d84e4d1f8a8f409861b0)
- 체계편(재게재): [llive 완전 해설 (6) 「Transformer의 바깥」](https://fullsense.qiita.com/furuse-kazufumi/items/fa9cfbdbdebecf1c7c3b)

---

## 제 8막 — llcore: Transformer의 코어에 진화를 내장하다

탈피의 모색은 「코어 그 자체를 진화시킨다」는 발상으로 이어졌습니다. CPU만으로 Transformer 코어의 진화를 돌리는 llcore의 막.

- [llcore — Transformer의 코어를 CPU로 진화시킨다 #32](https://fullsense.qiita.com/furuse-kazufumi/items/88ed294aa107330c6894)
- 제3축③: [3개의 실험으로 다진 이야기 #33](https://fullsense.qiita.com/furuse-kazufumi/items/21d6c4dcfde204062a89)（[쉬운 해설판](https://fullsense.qiita.com/furuse-kazufumi/items/9c466e85f3afd5939347)）
- 제3축 arc: [6단의 실험 + 생물학으로 조망 #34](https://fullsense.qiita.com/furuse-kazufumi/items/ff1f2b6c29e41abab10d)（[쉬운 해설판](https://fullsense.qiita.com/furuse-kazufumi/items/5a1124083298fdbcb9e6)）

---

## 제 9막 — 「거짓 진화」를 허용하지 않는다: 검증과 반증

이상하게 좋은 결과가 나오면, 이긴 기분이 되기 전에 그 내역을 의심하라. FullSense의 연구 규율(honest disclosure)이 형태가 된 막.

- 벤치의 함정: [llive vs 다른 LLM 벤치 — 동작 확인의 함정](https://fullsense.qiita.com/furuse-kazufumi/items/f2ebf45621d8f85399c9) ／ [Quiz bench Debug vs Release — 통계 지표 포함](https://fullsense.qiita.com/furuse-kazufumi/items/87dc2abff45b488f56a4)
- [「안경이 포화되면 선택압은 무력」 반증으로 단련한다 #29](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56) ([📗 쉬운 버전](https://fullsense.qiita.com/furuse-kazufumi/items/f822f8c8b01cd7b16713))
- 검증 arc: [(#35-00) SMT보다 SDP/Lyapunov](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6) ([📗 쉬운 버전](https://fullsense.qiita.com/furuse-kazufumi/items/a8118f557dda5c5e998c)) → [(#35-01) 검사기의 사다리](https://fullsense.qiita.com/furuse-kazufumi/items/71f05f901fd9a2de6de5) ([📗 쉬운 버전](https://fullsense.qiita.com/furuse-kazufumi/items/6b48b75c99e5d4b7d6b8)) → [(#35-02) 「너무 좋은 수치」를 의심하라](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615) ([📗 쉬운 버전](https://fullsense.qiita.com/furuse-kazufumi/items/146d5e2b27dabc59e799))

---

## 제 10막 — 현재 위치: 진화형 AI의 개발

검사기에 의해 지켜지는 진화(verified evolution)를, 장난감 같은 Transformer 코어에서 **실제 LLM**으로 배선하는 단계에 들어섰습니다(llcore R-LLM thread / llive 실제 LLM 진화 본주행). 다음 글들은 이 막에서 태어납니다 — 최신 상황은 [#34](https://fullsense.qiita.com/furuse-kazufumi/items/ff1f2b6c29e41abab10d)와 [#35 시리즈](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6)의 말미가 현재의 최전선입니다.

---

## 사이드 스토리(본편과 나란히 달리는 읽을거리)

**비전 / 철학**:

- [Will Caster와 Andrew NDR114가 지향했던 것 — 비전론](https://fullsense.qiita.com/furuse-kazufumi/items/e72192c75ff461d72601)
- [「삼자의 정신」을 AI에 부과한다 — 매니저류 AI 운용론](https://fullsense.qiita.com/furuse-kazufumi/items/faca5557d51a06a657f4)
- [「두 번째 뇌」 시리즈(6부 구성・대저)](https://fullsense.qiita.com/furuse-kazufumi/items/18dd57dcabbc84af9f02)

**개발 마라톤 기록(현장감 다큐멘터리)**:

- [한 세션에 5409 테스트 그린 #20](https://fullsense.qiita.com/furuse-kazufumi/items/96dc8af5b361ee44877b)
- [3일 8개 리포 #21](https://fullsense.qiita.com/furuse-kazufumi/items/4d4a2083c32acf1d96be)
- [15시간 앞당김 #23](https://fullsense.qiita.com/furuse-kazufumi/items/851b516f96fe54c176be)

**개발 체제 메타**:

- [AI에게 AI를 부하로 부리게 하는 「두 기둥」 #31](https://fullsense.qiita.com/furuse-kazufumi/items/71c2304718ad5829d2d7)

---

> **유지보수 note(편집자용)**: 본 index는 56편의 team URL 직링크를 10막 이야기 아크(정본 = 개발 이야기: llmesh → llove → llive → llcore)로 재배치한 것입니다. 글을 재게시해도 URL (item id)은 불변이므로 링크는 유지됩니다. 제 6막의 총정리 2판은 장래에 한 편으로 통합하는 후보입니다. SVG화 / 쉬운 해설판 정비 / 공개 Qiita → Team 유도는 backlog입니다.
