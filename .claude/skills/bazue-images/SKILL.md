---
name: bazue-images
description: スナックバス江 (bazue_all) のコマ画像を技術記事の挿絵に使う正本手順。出典・ライセンス・埋込形式・クレジット・コマ選定・1記事1コマの再利用ルール・多言語キャプションを規定。AUTO-TRIGGER when ユーザが「バス江」「bazue」「挿絵」「漫画コマ」「manga illustration」と発話、または記事 (Qiita/dev.to 等) に挿絵を入れる作業のとき。
---

# bazue_all 画像の使い方

スナックバス江 (Snack Basue) のコマ画像を FullSense の技術記事に**挿絵**として入れる正本手順。

## 1. 出典とライセンス（これは合法）

- **bazue_all** = 集英社『週刊ヤングジャンプ』**公式 SNS 用素材**ページ <https://youngjump.jp/info/bazue/>（SNS 等で**無料使用可と明記**）。
- 作品: 『スナックバス江』フォビドゥン澁川 / © Forbidden shibukawa / SHUEISHA。
- **生 jpg をそのまま埋め込んでよい**（公式無料素材のため）。
- ⚠️ 別系統の **Alu クロップ**（memory `reference_alu_manga_crops`）は **permalink 埋込のみ・生画像再ホスト禁止**。混同しない。**bazue_all は raw OK**。

## 2. 場所

- 画像: `docs/articles/assets/bazue_all/001.jpg`〜`206.jpg`（連番 206 枚・欠番なし）。
- **索引**: `docs/articles/assets/bazue_all/index.md` — 各コマの **セリフ / 場面 / en・zh・ko キャプション / 使いどころ**。**コマ選定は必ずこの index を読んでから**。

## 3. 埋込形式（Qiita / dev.to 等・実績フォーマット）

画像は **GitHub raw 絶対 URL**（fullsense は public repo）で参照。直後に blockquote でキャプション + クレジット:

```markdown
![<alt: コマの1行説明>](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/NNN.jpg)
> 🗒️ *"<index の該当言語キャプション>" — <この記事の論点との1行の結びつけ>*
> — 出典: 《スナックバス江》／フォビドゥン澁川・集英社（[公式](https://youngjump.jp/info/bazue/)）
```

- `NNN` = ゼロ埋め 3 桁（例 `046`）。
- **alt と blockquote は記事の言語に合わせる**（en 記事は en、ja は ja、zh/ko も同様。index.md にキャプション訳あり）。
- **クレジット `（© Forbidden shibukawa / SHUEISHA・Snack Basue）` は必須**（毎コマ併記）。
- raw URL が **HTTP 200** か確認（画像 200 必須＝memory `feedback_qiita_svg_path_and_cache`）。

## 4. コマ選定と再利用ルール

- **選定**: index.md の「**場面**」「**使いどころ:**」を読み、記事の論点・感情に合うコマを選ぶ。論点と無関係な「とりあえず可愛い」挿絵は避ける。
- **再利用ルール（ユーザー方針 2026-06-14）**: **同じコマは同一記事内で 1 回まで**。**別の記事でなら同じコマを再度使ってよい**。
- **配置**: 章境界 / honest disclosure / オチ / 読者の休憩ポイントに置くと効く（memory `feedback_reader_attention_curve` / `feedback_article_humor_style`）。
- **多言語**: 言語別に別記事（memory `feedback_articles_per_language_separate`）— それぞれにその言語のキャプションで入れる。

## 5. 既知の用途付きコマ（index.md「使いどころ」より抜粋・最新は index.md 参照）

| コマ | 使いどころ |
|---|---|
| `046` | Fable 5 等モデルが急に使えなくなった「突然の別れ」（提供終了 / モデル切替 / 突然の仕様変更 / レート上限）|
| `012` | リファラル / CTA 直後の自虐（「ひくわ」一万円札）|
| `050` / `054` | 待ち時間エッセイ（フリーズ判明 / 天井のシミを数える）|
| `069` | アフターマン（空想進化）・llcore 進化系 |
| `190` | 「検証機より、ちゃんと LLM を開発したい」場面 |
| `006` | 急に良くなった結果を疑う（honest disclosure）|

## 6. 手順チェックリスト

1. `index.md` を読む（該当コマの「場面 / 使いどころ」を確認）。
2. 記事の論点に合うコマを選ぶ（§5 既知用途表 or index の場面検索）。
3. その記事で**未使用**か確認（同一記事 1 コマ 1 回）。
4. §3 フォーマットで埋込 + 記事言語のキャプション + クレジット。
5. raw URL が **200** か確認してから公開。
