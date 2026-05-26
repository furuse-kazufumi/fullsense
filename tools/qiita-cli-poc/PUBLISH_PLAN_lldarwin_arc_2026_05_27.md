# 投稿準備計画 — lldarwin アーク + バックログ (2026-05-27)

> **目的**: 未投稿記事を **限定共有 (private: true)** で Qiita に上げて 24h 制限を回避し、
> その後 1 本ずつ公開フリップする準備。**本計画は「準備」段階**＝ Qiita への実アップロード
> (`npx qiita publish`) は **`!` 印の人間手動 / ユーザー go の合図で実行**。Claude は実行しない。
> 詳細手順の正本は [MIGRATION_GUIDE.md](./MIGRATION_GUIDE.md)。

## 1. 現状（2026-05-27 監査）

| 記事 | Qiita 状態 | local frontmatter | 投稿準備 |
|---|---|---|---|
| #14–#23 | 既投稿（LINK_MAP に URL あり） | ignorePublish=true / id=null | 投稿済（再投稿不要） |
| #24-00..08 | CLI 投稿済（id あり、一部 限定共有） | ignorePublish=false / id あり | 済 |
| **#25** monoculture | **未投稿** | private=true / ignorePublish=true / id=null | ★バックログ |
| **#26** 設計編 (drafts/) | 未投稿（draft） | — | 内容詰め後 |
| **#27** marathon climax | **未投稿**（多言語展開中） | private=true / ignorePublish=true / id=null | ★バックログ（B 完了後） |

→ **実バックログ = #25 / #27（+ #26 設計編）**。#14-24 は投稿済なので「溜まっている」のは実質この 3 本＋今後の新規。

## 2. アップロード前チェックリスト（限定共有・private-first）

各記事を上げる前に **ローカルで** 確認（Qiita は CLI 削除不可＝Web UI のみ。投稿前検証を徹底）:

- [ ] frontmatter `private: true`（限定共有＝24h 制限の対象外）。`ignorePublish: false`（CLI が publish 対象に）。`id: null`（新規＝初回 publish で採番）。
- [ ] **🔴 SVG を絶対 raw URL に変換**（重要ギャップ）: #25/#27 は相対 `./assets/lldarwin_2026_05_26/*.svg`。**Qiita は相対パス画像を表示できない** → `https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/lldarwin_2026_05_26/<file>.svg` に置換が必須（[[feedback_animated_svg_static_fallback]]: Qiita は絶対URL / 静的可視 fallback）。**`convert_to_qiita_cli.py` はこの変換を未実装** → 手動 or スクリプト拡張（§4 申し送り）。
- [ ] ローカル D: パス・画像 placeholder が本文に無い（公開規約）。
- [ ] 多言語（#27）は各言語版が自己完結（[[feedback_multilingual_article_structure]]）。
- [ ] アニメ SVG は no-SMIL 静的状態が可視（reveal-gate width=0/opacity=0 事故なし）。

## 3. 実行手順（`!` = 人間手動 / go の合図で）

```
# (1) frontmatter 正規化 + public/ へ出力 (private:true, ignorePublish:false 化)
py -3.11 tools/qiita-cli-poc/convert_to_qiita_cli.py docs/articles/QIITA_#25_*.md docs/articles/QIITA_#27_*.md
#   ↑ SVG 絶対URL変換は別途（§2 チェック / §4 申し送り）。convert 後の public/<name>.md を目視確認。

# (2) ! 人間手動: 限定共有で投稿（24h 制限を受けない）
cd tools/qiita-cli-poc && npx qiita publish QIITA_#25_... && npx qiita publish QIITA_#27_...

# (3) 投稿後: 採番された item id / URL を LINK_MAP (QIITA_#24_LINK_MAP.md の lldarwin アーク表) に記入
# (4) 公開フェーズ: private:true→false を 1 本ずつ flip（公開作成は 24h 上限あり→分割）。URL は /private→/items、item id 不変。
```

## 4. 申し送り（実装すると batch が完全自動化に近づく）

- **convert_to_qiita_cli.py に「相対 assets → 絶対 raw URL」変換を追加**すれば、§2 の🔴手動ステップが消える。`./assets/...` → `https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/...` の正規表現置換。要テスト。
- 投稿後 URL 一括反映 `qiita_url_sync.py`（LINK_MAP 既述の予定スクリプト）も併せて。

## 5. 状態（honest）

- 本計画は **準備のみ**。frontmatter の flip・SVG 変換・`npx qiita publish` は **未実行**（#27 は多言語展開作業中＝内容未確定、かつ外部公開はユーザー go が前提）。
- 「溜める歯がゆさ」への回答: 限定共有は 24h 制限外なので **バックログ 3 本は go が出れば一度に限定共有投稿可**。歯がゆいのは「公開フリップ」だけで、それも URL を知る人には限定共有時点で読める（[[feedback_qiita_limited_share_unlimited]]）。
