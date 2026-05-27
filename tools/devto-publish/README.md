# devto-publish

dev.to (DEV Community) への Markdown 記事自動投稿スクリプト。

## 前提

- Python 3.11 (`py -3.11`)
- 標準ライブラリのみ使用 (追加インストール不要)
- dev.to API Key (取得方法は下記)

---

## API Key の取得と設定

### 1. dev.to でキーを発行

1. https://dev.to/settings/extensions を開く
2. **"DEV Community API Keys"** セクション > **"Generate API Key"**
3. Description に任意の名前 (例: `fullsense-autopublish`) を入力して生成
4. 表示されたキーをコピー (画面を閉じると二度と見えない)

### 2. D:\api-keys.json に追記

```json
{
  "devto_api_key": "<YOUR_KEY_HERE>"
}
```

または環境変数で渡す場合:

```powershell
$env:DEVTO_API_KEY = "<YOUR_KEY_HERE>"
```

**キーの値を公開 Git リポジトリにコミットしないこと。**

---

## 使い方

### dry-run (token 不要 — 投稿内容の確認)

```powershell
py -3.11 D:\projects\fullsense\tools\devto-publish\publish_devto.py `
    "D:\projects\fullsense\docs\articles\QIITA_#27_lldarwin_v2_overnight_marathon.md" `
    --dry-run
```

token が未設定の場合も自動で dry-run にフォールバックし、セットアップ手順を案内します。

### 新規投稿 (draft)

```powershell
py -3.11 D:\projects\fullsense\tools\devto-publish\publish_devto.py `
    "D:\projects\fullsense\docs\articles\QIITA_#27_xxx.md"
```

draft 状態で投稿されます。dev.to ダッシュボードで確認後に手動公開できます。

### 新規投稿 (即時公開)

```powershell
py -3.11 D:\projects\fullsense\tools\devto-publish\publish_devto.py `
    "D:\projects\fullsense\docs\articles\QIITA_#27_xxx.md" `
    --published
```

### タグ・タイトル上書き

```powershell
py -3.11 D:\projects\fullsense\tools\devto-publish\publish_devto.py `
    "D:\projects\fullsense\docs\articles\QIITA_#27_xxx.md" `
    --tags "ai,llm,python,evolution" `
    --title-override "Rebuilding AI Evolution Overnight"
```

### 連載 (Series) 指定

```powershell
py -3.11 D:\projects\fullsense\tools\devto-publish\publish_devto.py `
    "D:\projects\fullsense\docs\articles\QIITA_#27_xxx.md" `
    --series "FullSense Development Log"
```

### 既存記事の更新

初回投稿後、同ディレクトリに `<stem>.devto.json` が自動生成されます。
次回の実行では自動的に PUT (更新) になります。

```powershell
# 既に <stem>.devto.json が存在する状態で再実行すると更新
py -3.11 D:\projects\fullsense\tools\devto-publish\publish_devto.py `
    "D:\projects\fullsense\docs\articles\QIITA_#27_xxx.md"
```

---

## 言語セクション抽出

Qiita 多言語記事の構造 (`# English` / `# 日本語` / `# 中文` / `# 한국어`) に対応。
デフォルトは `--lang english` で英語セクションを自動抽出します。

```powershell
# 日本語セクションを投稿
py -3.11 ... --lang japanese

# セクションが見つからない場合は全体を使用
```

---

## サイドカーファイル (.devto.json)

投稿成功後、記事ファイルと同ディレクトリに `.devto.json` が生成されます:

```json
{
  "id": 1234567,
  "url": "https://dev.to/username/article-slug-xxxx",
  "published": false,
  "title": "...",
  "created_at": "2026-05-27T...",
  "updated_at": "2026-05-27T...",
  "source_file": "D:\\projects\\fullsense\\docs\\articles\\..."
}
```

この `id` が存在する限り、以降の実行は PUT (更新) になります (二重投稿防止)。

---

## エラーハンドリング

| HTTP | 意味 | 対処 |
|------|------|------|
| 401  | API token 無効 | dev.to Settings で再発行し api-keys.json を更新 |
| 422  | タイトル重複・タグ制約 | `--title-override` / `--tags` を調整 |
| 429  | レート制限 | しばらく待って再実行 |
| 0    | ネットワーク不通 | 接続確認 + dev.to status page |

---

## 他サイトへの対応可能性 (所見)

| サイト | API | 難易度 | 備考 |
|--------|-----|--------|------|
| **dev.to** | 公式 REST API v1 (無料) | 低 | 本スクリプト対応済み |
| **Hashnode** | GraphQL API (無料) | 中 | `createPublicationStory` mutation。JSON ベース |
| **Medium** | 公式 API (廃止傾向) | 高 | 2023 年以降新規 token 発行停止。非推奨 |
| **Zenn** | 非公式 (GitHub 連携のみ) | 中 | Git push で自動デプロイ。API 無し |
| **Hacker News** | HN API (読み取り専用) | - | 投稿 API なし。Web フォームのみ |
| **Qiita** | 公式 API v2 | 低 | qiita-cli-poc で対応済み |

Hashnode は GraphQL だが token + mutation 方式でシンプルに実装可能。Medium は token 発行停止につき自動化困難。
