---
title: "連載シリーズ計画 #25 以降 — 進化アーク (lldarwin / honest disclosure / 可視化史 / 二本柱)"
nav_order: 96
---

# 連載シリーズ計画 — #25 以降「進化アーク」

> docs/articles/drafts/ 配下の骨子群を、どの順で・どの媒体に公開するかの計画書。
> 既存連載 #24（llive 完全解説 8 大分類）の**次のアーク**として #25〜#29 を位置づける。
> 状態は骨子段階（蓄積目的）。本文充実 → frontmatter 確定 → preflight → 投稿の流れは [`../QIITA_POST_GUIDE.md`](../QIITA_POST_GUIDE.md) に準拠。

## 0. このアークのテーマ

連載 #24 が「**llive を構成する技術の名称別解説**」（静的な構造）だったのに対し、
#25 以降の「**進化アーク**」は「**進化ランで実際に起きた失敗と、その克服の物語**」（動的な実録）。

通奏低音は連載 #24 と同じ **honest disclosure**: 「異常に綺麗な結果は勝利でなく警報」。
今アークはそれを**自分の進化ランへの反証**として一段深める（[[feedback_benchmark_honest_disclosure]]）。

## 1. アーク構成（#25〜#29）

| # | 仮タイトル | 種別 | コンセプト核 | 骨子ファイル | 状態 |
|---|---|---|---|---|---|
| #25 | 私とフリストンだけが残った — monoculture と lldarwin | 失敗実録 + 設計予告 | 選択圧ゼロ → 遺伝的浮動 → 8→2 monoculture の honest disclosure | `../QIITA_#25_monoculture_evolution_lldarwin.md` | 🟢 充実済（本セッションで §5.5/5.6 追加） |
| #26 | lldarwin の設計 — 多目的淘汰 / ε-lexicase / QD | 設計解説 | 「測る(lleval)」の次は「淘汰する(lldarwin)」。核は「集約しない」 | `QIITA_#26_lldarwin_multi_pressure_selection.md` | 🟡 骨子 |
| #27 | 眼鏡が曇ると淘汰も無力 — 反証調査 | honest disclosure | 飽和 eval には選択圧が効かない + Goodhart + proxy 限界 | `QIITA_#27_falsification_goodhart_proxy_limits.md` | 🟡 骨子 |
| #28 | 進化を「見せる」技術の系譜 | 教養系 | Conway → Tierra → Avida → Karl Sims → Lenia → QD → 3DGS | `QIITA_#28_evolution_visualization_history.md` | 🟡 骨子 |
| #29 | AI に AI を部下として使わせる — 二本柱 | 開発手法系 | Claude 主導 + Codex 配下、検証規律、並列化 | `QIITA_#29_codex_two_pillar_orchestration.md` | 🟡 骨子 |

## 2. 公開順（推奨）

物語の依存関係に沿った順序。**#25 → #26 → #27 が進化アークの本線**（失敗 → 設計 → 反証）。
#28（教養）と #29（手法）は本線の合間に挟む「箸休め」として配置し、読者の集中力を保つ
（[[feedback_reader_attention_curve]] / [[feedback_article_break_points]]）。

```
#25（失敗実録: 私とフリストンだけ）★アーク起点・既に充実
  → #28（教養箸休め: 進化可視化史）   ← #25 で「進化を見せる」に触れた直後に系譜へ広げる
  → #26（設計本線: lldarwin）         ← #25 の続き、淘汰器の設計
  → #29（手法箸休め: 二本柱）         ← #26 が「配下 Codex に調査させた」に触れた直後に体制論へ
  → #27（反証本線: honest disclosure）★アーク帰結・自分の設計に反証
```

**別案（本線優先・箸休め後置）**:
```
#25 → #26 → #27（本線 3 連投で進化アーク完結）
  → #28（教養）→ #29（手法）（外伝として後追い）
```
SNS 反応を見て、本線を一気に出すか箸休めを挟むかを選択する。

## 3. 媒体マッピング

| 媒体 | 対象 | 言語 | 備考 |
|---|---|---|---|
| Qiita | #25〜#29 全部（技術者向け） | ja → en/zh/ko 後続 | private-first（限定共有）で連投 → 全体公開昇格（[[feedback_qiita_limited_share_unlimited]]） |
| Medium | #25〜#29 en 版 | en | Qiita ja と並走（連載 #24 と同パターン） |
| LinkedIn | #28（教養）/ #29（手法）が拡散向き | ja（組込翻訳） | 非エンジニア層に届きやすい 2 本を優先 |

非エンジニア向け（QIITA_GENERAL 系）には #25（金魚の池メタファ）と #28（進化可視化散歩）が向く。

## 4. 連載 #24 との接続

#24 の各章から進化アークへの自然なリンク:
- #24-05（進化型最適化 v0.B/C/D/E）→ #25（その進化ランで実際に起きた monoculture）
- #24-08（lleval 評価フレームワーク）→ #26（測る lleval の次の淘汰 lldarwin）
- #24-07（観測 + 統治 / honest disclosure）→ #27（honest disclosure の本丸）

#24-00（series index）に「**次アーク = 進化アーク #25〜#29**」の 1 行を投稿後に追記すると連載が繋がる。

## 5. 充実フェーズの TODO（骨子 → 本文）

各骨子を本文化する際の共通作業（[[feedback_qiita_long_form]] 本文は長いほど良い、30k 字級を default に）:

1. 「節の肉付け予定」コメントの内容を本文に展開（各記事内に明記済）。
2. ユーモア（漫才 / 落語 / 金魚の池等）を各節に 1 つ以上、休憩ポイント 🍵 を 90 秒間隔目安で配置。
3. 図解アイデア（#25 §5.6 に列挙）を animated SVG 化（[[project_fullsense_animemd_branch_token_viz]] 表現層に乗せる）。
4. 事実根拠を `../../vision/LLDARWIN_DESIGN.md` / `../../research/evolution_poc_deployment_results_2026_05_25.md` /
   `../../vision/OPEN_ENDED_EVOLUTION_REQUIREMENTS.md` に厳密準拠（捏造禁止・脚色は比喩 / 構成のみ）。
5. en/zh/ko 版を各言語完全自己完結で縦積み（[[feedback_multilingual_article_structure]]）。
6. frontmatter 確定（tags 5 個 / title 80 字以内検討 / private: true → 投稿時 false / ignorePublish 切替）。
7. `py -3.11 scripts/qiita_preflight.py` で警告チェック → 投稿。

## 6. 事実整合の注意（honest disclosure 厳守）

- **#27 の最重要注意**: PoC デプロイで行動 monoculture は**実際 0.05 に改善した**（`evolution_poc_deployment_results_2026_05_25.md` §2）。
  「lldarwin を入れても改善せず」と書くと**事実と異なる**。#27 は「改善は事実。だが**何を測った 0.05 か**
  （proxy 行動多様性 ≠ 実 LLM 知能多様性）」を honest に深掘りする構成にした。**虚偽の失敗を捏造しない**。
- **#29 の注意**: Codex は ChatGPT Pro 契約方針（promo 〜5/31）だが、導入状態は CLI 0.117.0 / quota 枯渇 /
  login 切替予定で**実応答未取得の段階**（`reference_codex_two_pillar`）。「実際にバリバリ回した」と脚色しない。
  既に回した範囲（既存資産調査 / クロスレビュー方針）に限って実例として書く。
- **#28 の注意**: 年代・人名は人工生命史の通説に準拠。3DGS の進化可視化応用は FullSense の**研究的賭け**で
  確立技術ではない旨を明記済。

## 7. 関連
- 投稿ガイド: [`../QIITA_POST_GUIDE.md`](../QIITA_POST_GUIDE.md)
- 既存連載 index: [`../QIITA_#24_00_llive_tech_series_index.md`](../QIITA_#24_00_llive_tech_series_index.md)
- URL 集約: [`../QIITA_#24_LINK_MAP.md`](../QIITA_#24_LINK_MAP.md)
- 設計根拠: `../../vision/LLDARWIN_DESIGN.md` / `../../vision/OPEN_ENDED_EVOLUTION_REQUIREMENTS.md`
- 実測根拠: `../../research/evolution_poc_deployment_results_2026_05_25.md`
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_daily_articles_policy]] / [[feedback_article_numbering_mandatory]] / [[reference_codex_two_pillar]]
