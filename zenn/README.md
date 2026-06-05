# Zenn 投稿基盤 (Phase 1)

FullSense の記事を [Zenn.dev](https://zenn.dev/) へ投稿するための変換成果物を置くディレクトリ。
**single source of truth は `docs/articles/` (GitHub repo)** であり、この `zenn/` 配下は
そこからの **変換出力 (生成物)** である。手で編集せず、変換スクリプトで再生成する。

## ディレクトリ構造 (zenn-cli 規約)

```
zenn/
├── articles/                      # 単発記事 (Zenn article)
│   └── <slug>.md
└── books/
    └── llive-complete-guide/      # 連載 #24 (9 章) を 1 つの Zenn Book に
        ├── config.yaml
        ├── 00-llive-tech-series-index.md
        ├── 01-memory-layer.md
        ├── ...
        └── 08-lleval-eval-framework.md
```

## 変換スクリプト

`scripts/publish/zenn_convert.py` (Python 3.11 / stdlib のみ)。`docs/articles/` を
**読み取り専用**で変換し、`zenn/` 配下に出力する。

```powershell
# 連載 #24 を Book へ変換
py -3.11 scripts\publish\zenn_convert.py book

# 単発記事を変換
py -3.11 scripts\publish\zenn_convert.py article "docs\articles\QIITA_#22_transformer_escape_status.md"

# Book + 主要単発記事を一括変換
py -3.11 scripts\publish\zenn_convert.py all

# 書き込まず内容だけ確認 (dry-run)
py -3.11 scripts\publish\zenn_convert.py book --dry-run
```

### 変換内容

| 項目 | Qiita 形式 (入力) | Zenn 形式 (出力) |
|---|---|---|
| frontmatter | `tags` (array / inline) | `topics` (≤5, 正規化) |
| 公開フラグ | `private` / `ignorePublish` | `published: false` (固定) |
| アイコン | なし | `emoji` 1 文字 (🧬🧠⚖🔬 で統一) |
| 種別 | なし | `type: "tech"` |
| 多言語 | `# 日本語` / `# English` / `# 中文` / `# 한국어` | **ja セクションのみ抽出** |
| 画像 | `raw.githubusercontent.com` 絶対 URL | そのまま維持 (相対パス禁止) |

slug は Zenn 制約 (12〜50 文字, `a-z0-9_-`) を満たすよう自動生成する
(例: `QIITA_#22_transformer_escape_status.md` → `fs-22_transformer_escape_status`)。

emoji の統一規則 (連載 #24): 🧠 記憶 / 🧬 進化・最適化 / ⚖ governance / 🔬 eval・検証 /
📖 index。Book カバーは 🧬。

## canonical URL の扱い (重要)

**Zenn は frontmatter で canonical URL を設定できない** (dev.to の `canonical_url` 相当が無い)。
cross-post の重複扱いを避けるための代替として、変換スクリプトは **各記事の本文冒頭に
出自リンク注記を自動挿入**する:

```
> この記事は [FullSense リポジトリ](https://github.com/.../docs/articles/<file>) の
> 記事を Zenn 向けに変換したものです (原本 = GitHub / single source of truth)。
```

これにより「どこが原本か」を読者と検索エンジンに明示する。GitHub repo が唯一の
source of truth なので、Qiita / Zenn / dev.to のどこから来ても同じ内容に到達する。
ファイル名の `#` は URL fragment と衝突するため `%23` にエンコードしている。

## 投稿 (Phase 2 以降・未実装)

本 Phase 1 は **変換のみ**。実投稿 (zenn-cli の deploy / GitHub Actions 連携) は行わない。
`published: false` 固定なので、変換物を `git push` しても Zenn 上では公開されない。
公開は将来 Phase 2 (GitHub Actions で push 時自動公開) でユーザー判断のもと行う。

実際に Zenn でプレビューする場合 (ユーザー操作):

```powershell
npx zenn preview   # ローカルプレビュー (zenn-cli 導入時)
```

## 多言語版について

Zenn は日本語プラットフォームのため **ja 版のみ**変換対象。EN は dev.to / Medium、
ZH/KO は別 platform で扱う (`scripts/publish/` の他 converter / `tools/devto-publish/`)。

## テスト

```powershell
py -3.11 -m pytest tests\test_zenn_convert.py -q
```
