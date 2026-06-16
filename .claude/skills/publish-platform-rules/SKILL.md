---
name: publish-platform-rules
description: |
  技術記事を各投稿サイト (Qiita / Qiita Team / dev.to / Zenn / Medium / LinkedIn)
  へ公開するときの**プラットフォーム別ルール・ツール・トークン・既知の罠**を一括で守る
  skill。add-qiita-article が「記事を作る」側なら、本スキルは「各サイトへ出す」側。
  Auto-trigger when: 「投稿」「publish」「クロス投稿」「dev.to」「Zenn」「Qiita 公開」
  「海外サイト」を発話、または記事を外部公開しようとする直前。外部公開は不可逆 = 実 POST 前に
  必ず本チェックリストを当てる。
---

# publish-platform-rules — 投稿サイト別の公開ルール

## 何を解く skill か

サイトごとに API・認証・タグ制約・描画仕様・**ハマりどころ**が違い、毎回再発見すると時間を溶かす
(2026-06-16 セッションで dev.to の WAF 403 と Qiita のカード描画を都度調べ直して浪費)。本スキルで
プラットフォーム別ルールを 1 か所に固定する。**外部公開は不可逆**なので、実 POST 前に該当節を読む。

## 大原則 (全サイト共通)

- **言語別に別記事で作る** ([[feedback_articles_per_language_separate]])。ja/en/zh/ko を独立記事にし、
  海外サイトへはその言語版をそのまま出す。1 記事 4 セクション併載は default にしない。
- **画像はローカル/相対パス禁止**。Qiita は読めない。public URL かプラットフォーム直アップのみ
  ([[feedback_no_local_path_in_public]] / [[feedback_no_image_placeholders]])。
- **トークンは絶対にハードコードしない**。`D:/api-keys.json` か env から読む ([[reference_api_keys]])。
- **実 POST は人間 GO のとき**。新規は private/draft 既定。迷ったら dry-run。

## プラットフォーム別 早見表

| サイト | ツール | トークン (api-keys.json) | 認証ヘッダ | 既定可視性 | 最大タグ |
|---|---|---|---|---|---|
| Qiita (公開) | qiita-cli or 直 API PATCH | `~/.config/qiita-cli/credentials.json` (`credentials[].accessToken`) | `Authorization: Bearer` | 記事の `private` | 5 (空白不可) |
| Qiita Team | `tools/qiita_team_post.py` | `qiita_team_token` | `Authorization: Bearer` | private (新規) | 5 |
| dev.to | `tools/devto-publish/publish_devto.py` | `devto_api_key` | **`api-key`** (Bearer でない) | draft | 4 (小文字 alnum+`-`) |
| Zenn | `scripts/publish/zenn_convert.py` | (なし=GitHub 連携) | — | repo の published | — |
| Medium | — | — | — | **不可** (API 廃止) | — |
| LinkedIn | 手動 | — | — | — | — |

## Qiita (公開, qiita.com)

- API base `https://qiita.com/api/v2`。`Authorization: Bearer <token>`。token は qiita-cli の
  `~/.config/qiita-cli/credentials.json` → `credentials[]` のうち `name == default` の `accessToken`。
- **公開方法 2 つ**: (a) `npx qiita publish <basename>` (qiita-cli-poc/ で実行) (b) 直 API `PATCH /items/<id>`
  (frontmatter に id があれば更新)。
- ★**罠 (sync 上書き)**: qiita-cli `publish` は実行前に `syncArticlesFromQiita` が走り、ローカルを
  remote 内容で上書きしうる。**ローカル編集を確実に反映したいなら直 API PATCH** を使う (本セッション
  で a96a15 は PATCH で公開)。
- ★**リンクカード (画像を出す唯一の合法手)**: **URL を単独行**に置く (前後に空行) → Qiita が OGP
  リンクカード化 (`<qiita-embed-ogp>` / iframe `embed-contents/link-card`) し **og:image を表示**。
  - `> blockquote 内の [テキスト](URL)` や行内リンクは **ただのテキストリンク = 画像出ない**。
  - oEmbed 公式対応 = X/YouTube/CodePen/Gist/Figma/SpeakerDeck/SlideShare/Docswell/StackBlitz 等
    (alu.jp は非対応)。だが**汎用 OGP リンクカードは任意ドメインで効く**ので alu も単独行 URL でカード化。
- ★**Alu マンガコマ** ([[reference_alu_manga_crops]]): **crop permalink を単独行**に貼る → カードに
  コマ画像 (og:image) が出る。**生画像の再ホストは禁止**。カタログ = `docs/articles/assets/bazue_alu_catalog.md`。
- タグ: 最大 5・**空白不可** (空白タグは 403)。title は YAML folded scalar `title: >-` 可。
- 投稿前検査: `tools/qiita_team_post.py scan` が NO TITLE / NO TAGS / 非 public 画像 / local path を検出。

## Qiita Team (fullsense.qiita.com)

- `tools/qiita_team_post.py` (`verify` / `scan` / `dry-run` / `post <file> --yes`)。token = `qiita_team_token`。
- API base `https://<team>.qiita.com/api/v2`、`Authorization: Bearer`。新規 private 既定。
- ★**用途**: 公開前の**描画プレビュー**に最適。post 後 `GET /items/<id>` の `rendered_body` を見れば、
  カード化されたか (例 `<qiita-embed-ogp>`) を**公開記事に触れず**確認できる。検証後は `DELETE /items/<id>`。

## dev.to (DEV Community)

- `tools/devto-publish/publish_devto.py <file.md> [--published] [--dry-run] [--tags] [--title-override]
  [--canonical-url] [--series]`。token = `devto_api_key` (or env `DEVTO_API_KEY`)。
- API base `https://dev.to/api`、**認証ヘッダは `api-key`** (Bearer でない)、`Accept: application/vnd.forem.api-v1+json`。
- ★**罠1 (WAF 403)**: dev.to の WAF は **無 UA / urllib デフォルト UA を 403 で弾く**。リクエストに
  **browser 風 `User-Agent`** を必ず付ける (publish_devto.py / 疎通チェック両方)。空ボディ 403 はキー不正でなく WAF。
- ★**罠2 (folded title)**: Qiita frontmatter の `title: >-` (折返しスカラ) を素朴な正規表現でパースすると
  title が `>-` になる。block scalar の後続インデント行を結合 or H1 フォールバックで解決 (ツール修正済)。
- ★**罠3 (タグ/タイトル 422)**: dev.to タグは **英数字のみ小文字** = ハイフン/アンダースコア/空白も
  **不可** (`honest-disclosure` は 422 → 除去して連結 `honestdisclosure`)。最大 4。**title は 128 字上限**
  (超過は 422 → 語/区切り境界でトリム、全文は本文 H1 に残す)。両方ツール修正済。
- **既定 draft** (`--published` で公開)。**冪等性**: 初回 POST で `<stem>.devto.json` (sidecar) が生成され、
  次回以降は PUT 更新。`--canonical-url` に Qiita 原典 URL を入れると重複コンテンツ SEO 対策になる。
- **キー発行**: dev.to → Settings → 左メニュー **Extensions** → 最下部「DEV Community API Keys」→ Generate。
- 言語: **英語版をそのまま** 出す (separate-per-language 原則)。日本語版は出さない。

## Zenn

- `scripts/publish/zenn_convert.py` で Qiita md → Zenn 形式へ変換。公開は **Zenn↔GitHub 連携 + push**
  (API token 方式でない)。Zenn repo 連携セットアップが要る (未確認なら先に確認)。

## Medium / LinkedIn

- **Medium**: 投稿 API 廃止 = 自動投稿不可。
- **LinkedIn**: 組込翻訳があるので **日本語版のみ** 投稿 ([[feedback_linkedin_translation_jp_only]])。

## 公開前チェックリスト (実 POST 直前)

1. 言語: 出す言語の独立記事か (separate-per-language)。
2. 画像: local/相対パス無し・public URL or 単独行 URL カード。
3. タグ: そのサイトの上限・文字種に適合。
4. 可視性: 新規は draft/private で出して目視 → OK なら公開。
5. dev.to: User-Agent 付き・`api-key` ヘッダ・title が `>-` でない。
6. Qiita 公開: ローカル反映が要るなら直 API PATCH (sync 上書き回避)。
7. 不可逆操作 = 人間 GO を確認。

関連: [[feedback_articles_per_language_separate]] [[feedback_overseas_tech_platforms]]
[[reference_qiita_team_publish_flow]] [[reference_alu_manga_crops]] [[feedback_qiita_svg_path_and_cache]]
[[reference_api_keys]] [[feedback_article_naming]]
