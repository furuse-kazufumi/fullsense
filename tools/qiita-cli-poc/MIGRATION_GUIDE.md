# Qiita CLI 一括移行ガイド (FullSense 連載 ~18 記事)

`@qiita/qiita-cli` v1.8.0 (Apache-2.0, Node 20+) を使い、`docs/articles/QIITA_*.md` の
連載記事を `private: true` (限定共有) で一括投稿し、24h 投稿数制限を回避してから
段階的に公開する手順。

> 検証環境: Node v24.14.0 / npm 11.9.0 / qiita-cli v1.8.0。
> このガイドのコマンドのうち **`!` 印は人間が手動実行**するもの (token/外部公開が必要なため
> 自動化エージェントは実行しない)。

---

## 0. 前提と戦略

- **制限回避戦略**: Qiita の 24h 投稿数制限は **新規「公開」記事** に掛かる。
  **限定共有 (`private: true`)** は対象外なので、まず全 18 記事を `private: true` で一括投稿し、
  その後 1 記事ずつ `private: false` に flip して公開すれば、制限のボトルネックを移行作業から切り離せる。
- **公開フェーズの制限は残る**: flip 公開そのものは公開記事の作成扱いになるため、
  公開数が 24h 上限を超える場合はそこで分割が必要 (詳細は §6)。
- **削除は CLI 不可**: 誤投稿の削除は Qiita Web UI からのみ。投稿前のローカル検証を徹底する。

---

## 1. ディレクトリ構成

```
tools/qiita-cli-poc/
├── qiita.config.json          # ← includePrivate を要編集 (§4)
├── .github/workflows/publish.yml
├── .gitignore                 # .remote / node_modules
├── convert_to_qiita_cli.py    # frontmatter 変換スクリプト
├── input_copies/              # 実記事のコピー (実ファイルは触らない)
└── public/                    # ← qiita-cli の publish 対象。変換結果がここに入る
```

`npx qiita` は **カレントディレクトリの `public/`** を記事置き場とみなす。

---

## 2. Frontmatter mapping table

| 既存 `QIITA_*.md` | qiita-cli schema | 変換ルール |
|---|---|---|
| `title: ...` | `title: ...` | そのまま |
| `tags:` (block seq) | `tags:` (block seq) | プレースホルダ `TODO_TAG` を除去、上限 5 個に切り詰め |
| `private: false` | `private: true` | **強制上書き** (制限回避のため移行時は全て true) |
| `id: null` | `id: null` | そのまま (publish 時に Qiita 側で UUID 採番) |
| `organization_url_name: null` | 同左 | そのまま |
| `slide: false` | `slide: false` | そのまま |
| `ignorePublish: true` | `ignorePublish: false` | **上書き** (移行後は publish 対象にする) |
| `updated_at: '...'` | (除去) | qiita-cli は許容するが PoC では最小 schema 化のため除去 |
| `hero_svg: '...'` | (除去) | FullSense 独自フィールド。本文側で参照するなら frontmatter から外す |
| `layout: default` (Jekyll) | (除去) | Jekyll 専用。qiita-cli では不要 |
| `permalink: /...` (Jekyll) | (除去) | Jekyll 専用 |

### 要注意な対応 3 点

1. **`TODO_TAG` プレースホルダ** — #14/#16 等に `- TODO_TAG` が残っている。変換で除去されるが、
   タグ 0 個だと Qiita が publish を拒否する。**移行前に実タグへ差し替え必須**。
2. **`private` の強制上書き** — 元記事が `private: false` でも、変換は問答無用で `true` にする。
   公開タイミングを移行と切り離すための意図的挙動。公開は §5 で明示的に flip する。
3. **`ignorePublish` の反転** — 元記事は全て `ignorePublish: true` (現状 publish 対象外)。
   変換で `false` にしないと `publish --all` がスキップする。

---

## 3. 変換 (自動化エージェント実行可)

```powershell
# 実記事を input_copies/ にコピー (実ファイルは編集しない)
Copy-Item D:\projects\fullsense\docs\articles\QIITA_#1*.md tools\qiita-cli-poc\input_copies\
Copy-Item D:\projects\fullsense\docs\articles\QIITA_#2*.md tools\qiita-cli-poc\input_copies\

# 変換 (public/*.md を生成)
cd tools\qiita-cli-poc
py -3.11 convert_to_qiita_cli.py
```

出力された `public/*.md` の frontmatter diff を目視し、`TODO_TAG` 警告が出た記事は
実タグへ手で差し替える。

---

## 4. config 編集 (限定共有を publish 対象に含める) — 重要

`qiita init` が生成する `qiita.config.json` は既定で:

```json
{ "includePrivate": false, "host": "localhost", "port": 8888 }
```

**`includePrivate: false` のままだと `private: true` 記事は publish されない。**
制限回避戦略を成立させるには `true` に変更する:

```json
{ "includePrivate": true, "host": "localhost", "port": 8888 }
```

---

## 5. 投稿フロー (人間が手動実行)

```powershell
# ! 手動: token 作成 (Qiita 設定 > アプリケーション)。スコープ read_qiita + write_qiita
! npx qiita login

# ! 手動: ローカルプレビューで表示確認 (任意)
! npx qiita preview

# ! 手動: private:true で全記事を一括投稿 (includePrivate:true 必須。限定共有=制限対象外)
! npx qiita publish --all

# --- 検証 --- 限定共有 URL を開いてレイアウト/タグ/コード/SVG を確認 ---

# ! 手動: 公開する記事だけ private: false に変更し、個別 publish
#   (一括ではなく 24h 上限を見ながら段階的に)
#   public/<記事>.md の private: true → false に編集
! npx qiita publish <記事のファイル名(拡張子なし)>
```

`publish --all` 後、各記事の `id` が Qiita から採番され `public/*.md` に書き戻される。
2 回目以降の publish はこの id で同一記事の更新になる (重複投稿にならない)。

---

## 6. 18 記事移行の見積りと最大の障害

- **所要見積り**:
  - 変換 (自動): 数秒。
  - `TODO_TAG` 差し替え (手動): ~18 記事 × 数分 = **30〜60 分** (最も時間が掛かる人手作業)。
  - `publish --all` (限定共有一括): API 呼び出し 18 回で **数分**。制限対象外なので 1 回で完走。
  - 検証 + 段階公開: 公開数が 24h 上限内なら同日完了。超える場合は数日に分割。
- **最大の障害**: **`TODO_TAG` プレースホルダの実タグ化**。タグ 0 個では Qiita が publish を
  拒否するため、変換だけでは投稿できない記事が複数ある。ここだけは LLM 補助があっても
  最終的に人手レビューが要る (記事内容に即したタグ選定)。

---

## 7. GitHub Actions による自動投稿 (任意)

`qiita init` は `.github/workflows/publish.yml` を生成済み。リポジトリの
**Secrets に `QIITA_TOKEN`** (read_qiita + write_qiita) を登録し、`public/*.md` を含む
コミットを `main` / `master` に push すると `increments/qiita-cli/actions/publish@v1` が
自動で publish する。CI で回す場合も `qiita.config.json` の `includePrivate` 設定が効くため、
限定共有→公開の段階移行は frontmatter の `private` を git で管理して push するだけで再現できる。
ただし誤公開のリスクがあるため、移行初回は手動 publish を推奨。

---

## 付録: 安全境界 (この PoC で実行しなかったこと)

- `npx qiita login` / `publish` / `preview` / `pull` は **未実行** (credential / 外部公開が必要)。
- 実記事 `docs/articles/QIITA_*.md` は **コピーのみ**、一切編集していない。
- npm install は `tools/qiita-cli-poc/` 内に閉じている (グローバル install なし)。
