# Qiita 用 SVG の作り方・扱い方ガイド

> Qiita 記事で SVG を**確実に表示・多言語化**するための実務手順。
> 単一の真実は memory `feedback_qiita_svg_path_and_cache`(必読チェックリスト)。本ガイドはその手順版 + 2026-05-31 の #26 多言語対応の経験反映。
> 「Qiita で図が見えない/動かない」時は、推測や再調査の前に **§8 チェックリストを最初に適用**(再発・時間浪費の既知問題)。

---

## 1. パス・URL のルール（最重要）

- **相対パス禁止**(`../assets/foo.svg`)→ Qiita は解決できず表示されない。
- **raw 絶対 URL を使う**: `https://raw.githubusercontent.com/<owner>/<repo>/main/<path>/foo.svg`
  - 例: `https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg`
- **raw URL は `main` ブランチを指す → アセットを push してからでないと 404**。
  - push 後に **HTTP HEAD で 200 を確認**(git の状態でなく実 HTTP で):
    ```bash
    curl -s -o /dev/null -w "%{http_code}" -I "<raw-url>"   # 200 ならOK
    ```
- アセットを移動したら**記事内の URL も追従**して更新する。

## 2. imgix プロキシとキャッシュ

- Qiita は画像を **imgix プロキシ(`auto=format`)でラスタライズ + キャッシュ**する。
  - 帰結①: **アニメ SVG(SMIL/CSS アニメ)は動かない**(静止画化される)。
  - 帰結②: **同じ URL でアセットを差し替えても古いキャッシュが残る**。
- 差し替えで更新したい時 → `?v=N`(連番)で **cache-bust** + 再 publish。
- **ファイル名が変われば衝突しない**(例: 多言語 `_en/_zh/_ko` は新ファイル名なので cache-bust 不要)。

## 3. アニメ SVG → 静的フォールバック

- Qiita では**アニメは動かない前提**で作る。
- **静的フレームの完成形**を用意する。「最後まで再生しないと意味が分からない」reveal-gate 的演出は**禁止**(静止で完結する図にする)。
- アニメ版(SMIL）は GitHub README 等**アニメ可の場所**用に分ける。Qiita 用は静止完成形。
- 関連 memory: `feedback_animated_svg_static_fallback`。

## 4. 多言語 SVG（ja / en / zh / ko）

各言語版を**完全自己完結**にする(`feedback_multilingual_article_structure`)。SVG 内のテキスト(タイトル・軸ラベル・凡例)も翻訳した変種を作る。

- **ツール**: `llive/scripts/svg_translate.py`
  - base(ja)SVG の `<text>`/`<tspan>` の中身を**翻訳辞書 `TRANSLATIONS`** で置換し、`<name>_en.svg` / `_zh.svg` / `_ko.svg` を生成。
  - **geometry(座標/path)は不変・テキストのみ置換**。XML 妥当性チェック + **残留日本語(かな/カナ)検出**を内蔵(en は CJK も leak 扱い)。
  - 使い方:
    ```bash
    py -3.11 llive/scripts/svg_translate.py --src-dir <assets-dir>   # en/zh/ko 生成
    py -3.11 llive/scripts/svg_translate.py --src-dir <dir> --check-only   # 既存変種の検証のみ
    ```
  - 新しい図を足したら `SOURCE_SVGS` に basename を追加。日本語テキストがある図は `TRANSLATIONS` にエントリ追加(無いと fail = 翻訳漏れを検出)。
  - **ラベルが元々英語/数値だけの図は翻訳不要** = 翻訳エントリ無しで verbatim コピーされ、言語別 URL を揃えられる。
- **記事側**: 各言語セクションで対応する変種を参照(JA=base, EN=`_en`, ZH=`_zh`, KO=`_ko`)。セクション境界で URL に言語サフィックスを付与する。
- 実例(#26): source `QIITA_#26_*.md` と公開版 `0a35e1bf.md` の EN/ZH/KO セクション 9 図を `_en/_zh/_ko` へ差替。新ファイル名なので imgix cache-bust 不要。

## 5. 生成側(matplotlib 等で図を作る場合)

- SVG 出力(テキストは `<text>` として埋まる形式)。ラスタ(png)でなく SVG にすると後段の翻訳・拡大に強い。
- **本筋(band-aid 回避)**: 生成スクリプトに **lang 引数**を持たせ en/zh/ko を出し分けるのが理想。現状は後段で `svg_translate.py` 翻訳。
- 表現の汎用化は FullSense `llrepr`(表現汎用層: markdown/svg/tui writer)へ寄せる将来余地。

## 6. publish（Qiita CLI）

- **hash-ID 名のファイルが公開実体**(custom 名は草稿 = 重複注意)。`feedback_qiita_svg_path_and_cache` / `reference_qiita_cli`。
- 手順:
  ```bash
  cd fullsense/tools/qiita-cli-poc
  npx qiita publish <hash-id>        # 認証 = ~/.config/qiita-cli/credentials.json
  ```
- **publish 後に live 記事で検証**: 各言語セクションが正しい変種 URL を指すか(imgix ラップ後でも URL-encoded ファイル名で確認可)。
- 限定共有(`private: true`)は 24h 投稿数制限の対象外で連投可(`feedback_qiita_limited_share_unlimited`)。

## 7. 標準フロー(まとめ)

```
図を SVG 生成 (テキスト埋込)
  → (日本語あり) svg_translate.py で _en/_zh/_ko 生成 + --check-only 検証
  → assets を repo に commit → origin/main へ push (raw URL は main 参照)
  → 記事の各言語セクションを raw 絶対 URL (言語別変種) へ書換
  → curl -I で全 raw URL が 200 か確認
  → npx qiita publish <hash-id>
  → live 記事で各言語の図表示 + テキストが各言語か確認
```

## 8. 見えない時のチェックリスト（この順で適用）

1. **相対パスになっていないか** → raw 絶対 URL に。
2. **raw URL が HTTP 200 か**(`curl -I`)→ 404 なら assets 未 push or パス間違い。
3. **imgix キャッシュ**(差し替えたのに古い)→ `?v=N` cache-bust or ファイル名変更 + 再 publish。
4. **アニメが動かない** → 仕様(imgix で静止化)。静的フレーム完成形にする。
5. **公開されない/重複** → hash-ID 名で publish(custom 名は草稿)。

## 9. 関連

- memory: `feedback_qiita_svg_path_and_cache`(必読チェックリスト)/ `feedback_animated_svg_static_fallback` / `feedback_multilingual_article_structure` / `reference_qiita_cli` / `feedback_qiita_limited_share_unlimited`
- ツール: `llive/scripts/svg_translate.py`(多言語変種生成)/ `fullsense/tools/qiita-cli-poc`(publish)
- 実例: 本リポジトリ `docs/articles/QIITA_#26_lldarwin_multi_pressure_selection.md` + `assets/lldarwin_2026_05_26/`(多言語 SVG 一式)
