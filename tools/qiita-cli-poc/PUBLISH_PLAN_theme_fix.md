# Publish Plan — #24-02 / #24-08 theme SVG 表示修正の Qiita 反映

## 背景

#24-02 / #24-08 の theme SVG が Qiita 上で表示されなかった根本原因は **2 段**:

1. **SVG 側 (修正済 + push 済)**:
   - `xmlns:xlink` 宣言漏れ → XML malformed (commit `52887ee`)
   - `<mpath xlink:href="#id">` (ID 参照 motion) を Qiita の imgix プロキシがラスタライズできず空画像 (Content-Length:0) を返す → **inline `path=` 形式に変更** (commit `7fc54b8`)
   - raw.githubusercontent は現在 well-formed な修正版を配信中

2. **imgix キャッシュ (未解決 — 本プランで対応)**:
   - Qiita は外部画像を `qiita-user-contents.imgix.net` 経由で配信
   - 壊れていた時の空画像が imgix edge に `max-age=31536000` (1 年) でキャッシュ済
   - **同じ imgix URL は空を serve し続ける** → 記事の画像 URL を変えて Qiita に新しい imgix URL を生成させる必要がある

## 準備済 (このプランの時点で完了)

`docs/articles/QIITA_#24_02_*.md` / `QIITA_#24_08_*.md` を編集済:

- theme SVG URL に cache-buster `?v=2` を付与 (→ Qiita が新 imgix URL を生成 → fresh fetch)
- `private: true` (現在 Qiita 上で限定共有。`false` のまま publish すると公開化するため必須)
- `id:` を LINK_MAP の URL hash から **仮設定** (#24-02=`bdfad6db3f2e70c40511` / #24-08=`e49b7ab9027d93594402`)
- `ignorePublish: false` (publish 対象化)

## ⚠️ login 後の手順 (重複投稿を防ぐ照合を必須化)

### Step 1 — login (ユーザーが手動実行)

```
! npx qiita login
```
token は read_qiita + write_qiita。

### Step 2 — id 照合 (重複防止の最重要ステップ)

仮設定した id が **本当に既存記事の item id か** を必ず確認する。`/private/<hash>` の hash は通常 item id だが、未検証。

```
cd D:/projects/fullsense/tools/qiita-cli-poc
npx qiita pull            # 自分の全記事を public/ に取得 (authoritative な id 付き)
```

- pull した記事群の中に #24-02 / #24-08 (タイトルで照合) があり、その id が
  `bdfad6db3f2e70c40511` / `e49b7ab9027d93594402` と **一致するか確認**。
- **一致** → 仮設定 id は正しい。Step 3 へ。
- **不一致** → 仮設定 id を pull で得た正しい id に修正。**id を直さず publish すると重複記事が作られる**。

### Step 3 — qiita.config.json の gotcha

```
# qiita.config.json に includePrivate: true を設定 (既定 false だと private 記事が publish されない)
```

### Step 4 — 該当記事を qiita-cli ワークスペースに配置

これらは元々 Web エディタ投稿で、qiita-cli ワークスペース (`public/`) には無い。
pull で取得した正しい id 付きファイルに対して theme URL の `?v=2` を適用するのが安全:

- pull 後の `public/<id>.md` (= #24-02 / #24-08) の theme SVG 行に `?v=2` を付与
- (または準備済の `docs/articles/QIITA_#24_0[28]_*.md` を public/ にコピーし、id が照合済なら使用)

### Step 5 — targeted publish (--all は使わない)

```
npx qiita publish <#24-02 の basename>
npx qiita publish <#24-08 の basename>
```

`publish --all` は ignorePublish:false の全記事を投稿するため使わない。**対象 2 件のみ** targeted で。各 publish 前に Claude が「これを更新します」と確認。

### Step 6 — 検証

- Qiita 記事を開き、theme SVG (radar/ring) が表示されることをハードリフレッシュで確認
- 限定共有のままか (公開化していないか) を確認
- imgix URL が新しくなり (新 `s=` 署名)、Content-Length が非ゼロになっていることを確認

## 代替: Qiita Web エディタ (CLI 不要・最速)

2 件だけなら Web エディタが最も安全・簡単:

1. Qiita で #24-02 / #24-08 を編集
2. theme 画像 URL に `?v=2` を付与して保存
3. → Qiita が新 imgix URL を生成 → fresh render

CLI の login / id 照合 / public 配置が不要。重複リスクもゼロ。

## 関連

- 根本原因と検証ログ: 本セッションの調査 (imgix Content-Length:0 / mpath ID 参照問題)
- qiita-cli 全般: `tools/qiita-cli-poc/MIGRATION_GUIDE.md` + memory `reference_qiita_cli`
