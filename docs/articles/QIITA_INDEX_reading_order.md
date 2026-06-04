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
2. [「眼鏡で測る」だけでは進化しない — 選択圧 lldarwin #26](https://fullsense.qiita.com/furuse-kazufumi/items/30a41e73d71e0a36f9ba)
3. [一晩で AI 進化を作り直した #27](https://fullsense.qiita.com/furuse-kazufumi/items/61dda4314c1b786381d0)
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
- [「眼鏡が飽和すると選択圧は無力」反証で鍛える #29](https://fullsense.qiita.com/furuse-kazufumi/items/bb2f19dbf60df28deb56)
- 検証 arc: [(#35-00) SMT より SDP/Lyapunov](https://fullsense.qiita.com/furuse-kazufumi/items/6fc86b4732eeec77adb6) → [(#35-01) 検査器の梯子](https://fullsense.qiita.com/furuse-kazufumi/items/71f05f901fd9a2de6de5) → [(#35-02) 「良すぎる数値」を疑え](https://fullsense.qiita.com/furuse-kazufumi/items/ffef66ddbc48d7649615)

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
