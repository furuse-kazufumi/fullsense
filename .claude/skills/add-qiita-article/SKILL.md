---
name: add-qiita-article
description: |
  Qiita 投稿用記事 (`QIITA_*_jp.md`) を fullsense 配下に作成するための
  テンプレ skill。命名規則・配置場所 (明日のフォルダ)・必須要素 (1 行 hook、
  休憩ポイント ☕ 数分ごと、参考文献、HTML annotation メタタグ末尾) を
  自動で守る。岡潔先生関連の言及は礼節文面、「ユーザー」表現は使わず
  「筆者」「人間」へ統一。
  Auto-trigger when: 「Qiita 記事」「投稿用記事」「QIITA_*.md 作成」「公開資料追加」
  を発話、または `feedback_articles_pause` 解除中の記事生成タスク時。
---

# add-qiita-article — Qiita 記事作成テンプレ

## 何を解く skill か

公開資料は命名規則・配置・トーン・必須要素が複数の feedback memory に
分散している ([[feedback_article_naming]], [[feedback_articles_concept_hook]],
[[feedback_article_break_points]], [[feedback_linkedin_translation_jp_only]],
[[feedback_articles_pause]] 他)。毎回これらを再導出すると規約抜けが起きる。
本スキルで一括チェック。

## 入力

- ユーザーから明示的に「記事化指示」が出ている (`feedback_articles_pause` は
  明示指示で一時解除される)
- 記事の主題が決まっている

## ファイル命名 / 配置

| 媒体 | ファイル名 | 配置 |
|---|---|---|
| Qiita 単独 | `QIITA_<SLUG>_jp.md` | `docs/articles/YYYY-MM-DD/` (今日が `YYYY-MM-DD` なら **翌日** フォルダ) |
| Qiita シリーズ統合版 | `QIITA_<SLUG>_SERIES.md` | 同上 |
| LinkedIn | `LinkedIn_<SLUG>_jp.md` (jp のみ、[[feedback_linkedin_translation_jp_only]]) | 同上 |
| Eight 名刺 | `Eight_<SLUG>_jp.md` (1 度書いたら更新不要 [[feedback_eight_bio_final]]) | 同上 |
| 多言語 (Qiita 以外で必要なら) | `<MEDIA>_<SLUG>_{en,zh,ko}.md` | 同上 (新 CLAUDE.md `多言語対応プロジェクトでの記事生成時は 4 言語版を意識`) |

## 必須要素 (チェックリスト)

```markdown
# <タイトル>

**1 行 hook**:
<読者の興味を即座に掴む 1-3 行> ([[feedback_articles_concept_hook]])

---

## はじめに / 背景

<本記事のスコープ、なぜ書くか>

---

## <本論セクション 1>

<内容>

### ☕ <休憩トピック>

<関連雑談 / 補足、~2-3 行>([[feedback_article_break_points]])

## <本論セクション 2>

<内容>

### ☕ <休憩トピック>

...

---

## まとめ / 教訓 / 残課題

| 観点 | 内容 |
|---|---|
| ... | ... |

---

## 参考文献 / 参考リソース

### <カテゴリ>
- 著者『書名』出版社, 年
- URL

<!-- llive:meta.article_id="QIITA_<SLUG>_jp" target=llove -->
<!-- llive:meta.published_date="YYYY-MM-DD" -->
<!-- llive:meta.tags=["llive","tag1","tag2"] target=any -->
```

## 休憩ポイント (☕) のルール

- **数分ごと** に挟む。記事 1500 字に 1 個程度が目安
- 統合版 / 大型記事 (300+ 行) で 3-4 個まで、それ以上は noise
- 雑談・脱線・教訓・「ちなみに」「ところで」系の小ネタ
- 本論の流れを切らない範囲で

## トーン規約

- **岡潔先生** 等の人物言及は礼節文面 (「先生」敬称、「学ばせていただく」、
  「実装したと主張するものではない」明示)
- **「ユーザー」を筆者の意味で使わない** — 「筆者」「人間」「私」に置換
- LinkedIn コメント主など外部の発言者は「LinkedIn でコメントを下さった方」等

## NG パターン

- ファイル名に lowercase だけ (例: `14_invisible_annotation.md`) — `QIITA_` prefix なし
- 配置: 当日フォルダや過去日付フォルダ — `YYYY-MM-(DD+1)` (明日) を使う
- 休憩ポイントが 0 個 or 8 個以上
- 1 行 hook が無い、または抽象的すぎる
- 数値根拠 (テスト数、ベンチ結果) の出典リンク無し

## 後処理

記事作成完了後:
1. `git status` で他に変更されたファイルが無いか確認
2. intentional commit:
   ```
   docs(qiita): <タイトル要約>
   
   - 配置: docs/articles/YYYY-MM-DD/QIITA_<SLUG>_jp.md
   - 構成: <セクション概要>
   - 主題: <feedback_daily_articles_policy 13 側面のうち X>
   ```
3. `[[skill: record-implementation]]` 適用 (memory への記事リスト反映が
   必要な場合のみ)
4. LinkedIn 投稿文を別途用意 (`LinkedIn_<SLUG>_jp.md`) — 850 字以内、本記事への誘導 hook + 4 部の概要

## 関連 feedback memory

- `[[feedback_article_naming]]` — QIITA_/LinkedIn_ prefix + 明日フォルダ
- `[[feedback_articles_concept_hook]]` — 1 行 hook 必須
- `[[feedback_article_break_points]]` — ☕ 休憩ポイント
- `[[feedback_linkedin_translation_jp_only]]` — LinkedIn は jp のみ
- `[[feedback_articles_pause]]` — 投稿用記事は当面保留、明示指示時のみ
- `[[feedback_daily_articles_policy]]` — 13 側面で記事
- `[[feedback_eight_bio_final]]` — Eight 名刺は更新不要
