# 投稿ランブック ― 連載「作って分かった LLM の中身」

> このシリーズ（技術版 #0-6 / 一般版 #0-6 / 総目次）を Qiita に出すときの手順書。
> 汎用手順は `QIITA_POST_GUIDE.md`、画像規律は `llm_structure_series_IMAGE_MANIFEST.md` が正本。ここはシリーズ固有の順序とチェックだけ。

## 0. 前提（push が先）

1. **assets/llm_structure_series/*.svg と drafts/ を origin/main に push**（raw URL は push 前は 404）。
2. push 後、任意の1枚を `https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/llm_structure_series/hero_00_intro.svg` で HTTP 200 確認。

## 1. 投稿順（推奨）

```
一般版 #0（導入・軽い）→ 技術版 #0（序章・検証哲学）
  → 以降、回ごとに 一般版 #N → 技術版 #N（N=1..6）
  → 最後に 総目次(INDEX)（全 URL が揃ってから）
```

- 各記事は**限定共有 → Qiita 実機プレビュー確認 → 全体公開**の2段階（house 標準）。
- プレビューで確認する点: (a) SVG が表示されるか（imgix ラスタライズ・JP フォント） (b) Mermaid が描画されるか (c) 表崩れ。
- SVG の JP フォントが崩れた場合のみ、その1枚を PNG/GIF に差し替え（`IMAGE_MANIFEST.md` 参照）。

## 2. 各記事の投稿時チェック

- [ ] タイトル: 1行目から `# ` を外してコピー（80字以内は確認済み）
- [ ] 本文: 2行目以降（フッターの `<<LINK:…>>` ナビは**投稿済み分だけ URL 置換、未投稿分は行ごと削除**）
- [ ] タグ: `llm_structure_series_LINK_MAP.md` の推奨タグ表から5件
- [ ] 投稿後すぐ LINK_MAP の該当行に URL を記入

## 3. 投稿後

1. LINK_MAP が全部埋まったら、各記事の `<<LINK:…>>` を確定 URL に一括置換して再投稿（編集）。
2. INDEX（総目次）を最後に投稿し、全記事の冒頭ナビから INDEX へリンク。
3. 画像を後から差し替えた場合は URL に `?v=2` を付けて cache-bust（imgix キャッシュ対策）。

## 4. 番号運用

既存 Qiita 連載の最大は ~#46。本シリーズは独立ブランド「作って分かった LLM の中身 #N」で運用し、
QIITA_#NN 通し番号とは独立（衝突しない）。
