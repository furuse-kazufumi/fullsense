---
layout: default
title: "Qiita 投稿準備ガイド (2026-05-22 整備)"
nav_order: 95
---

# Qiita 投稿準備ガイド

> docs/articles/ 直下の `QIITA_#NN_*.md` を Qiita Web UI から投稿するための one-shot ガイド.
> 各記事の状態は `scripts/qiita_preflight.py` で随時確認可能.
> 既存 [`POST_CHEATSHEET.md`]({{ '/articles/2026-05-18/POST_CHEATSHEET' | relative_url }}) (#18/#19 専用) を全 #14〜#24 系列に一般化したもの.

## 1. 現状サマリ (2026-05-22 preflight 結果)

| カテゴリ | 件数 | 状態 |
|---|---|---|
| **NO-FM (frontmatter なし)** | 14 件 | #14〜#19, #20, #24_02〜#24_08, LINK_MAP |
| **ignorePublish: true (draft)** | 5 件 | #21, #22, #23, #24_00, #24_01 |
| **TITLE-LONG (80 字超)** | 3 件 | #22 (89), #24_06 (84), #24_07 (84) — 投稿時に短縮検討 |
| **REFS 未解決** | 1 件 | #24_04 (内部参照 1 件残, 投稿後 URL 確定時に置換) |
| **本文サイズ** | 5KB〜16KB | 全件 Qiita 投稿可能範囲 (上限 1MB) |

## 2. 投稿順序 (推奨)

連載番号の時系列順に投稿:

```
#14 (Annotation Channel)
  → #15 (Second Brain)
  → #16 (Three-Self Spirit)
  → #17 (Human-AI Fusion Vision)
  → #18 (Non-Transformer Low-Spec PC)
  → #19 (GPU-Less AI for Everyone)
  → #20 (One Session Full Stack)
  → #21 (Three-Day Marathon)
  → #22 (Transformer Escape Status)
  → #23 (15h Marathon Mid Report)
  → #24-00 (Tech Series Index)
  → #24-01 (Memory Layer)
  → #24-02 (Thought Factors × COG-MESH)
  → #24-03 (Structural Evolution × TRIZ)
  → #24-04 (B-Series Convergence)
  → #24-05 (Evolutionary v0.B/C/D/E) ★ 連載中核
  → #24-06 (Non-Transformer LLM Backend)
  → #24-07 (Observability + Governance)
  → #24-08 (lleval — Eval Framework)
```

#24-00 の index 投稿後に #24-01〜08 を投稿すると、index が naturally に他の連載へリンクできる.

## 3. 各記事の投稿手順 (共通)

1. <https://qiita.com/drafts/new> を開く
2. **タイトル**: 該当 `.md` ファイル 1 行目 (`# llive 完全解説 #NN_XX — ...` 等) からコピペ
3. **本文**: ファイルの **2 行目以降** をコピペ (タイトル行は手順 2 で別入力済)
   - frontmatter (`---\n...\n---\n`) があれば除外
   - 末尾の `## 投稿時の推奨タグ` セクションは Qiita 上では非表示にしたい場合は除外
4. **タグ**: 5 個まで (frontmatter に `tags:` があればそれを参照、なければ記事末尾の §投稿時の推奨タグ から)
5. **公開設定**:
   - 最初は **「限定共有投稿」** で投稿 → プレビューで表示確認
   - 問題なければ **「全体公開」** に切替
6. **ライセンス**: CC BY (Qiita default)
7. **コメント許可**: ON

### PowerShell で本文 + タイトルをクリップボードに

```powershell
$file = "docs/articles/QIITA_#24_05_evolutionary_v0BCDE.md"
# タイトル (1 行目から '# ' を除く)
$title = (Get-Content $file -Head 1) -replace '^# ',''
$title | Set-Clipboard
Write-Host "Title copied: $title"
# 本文 (2 行目以降全部)
$body = (Get-Content $file | Select-Object -Skip 1) -join "`n"
$body | Set-Clipboard
Write-Host "Body copied: $($body.Length) chars"
```

## 4. 投稿後の cross-link 確定運用

各記事内に `[`QIITA_24_XX_*` (内部参照)]` 形式の cross-link が残っている. 投稿後に確定する Qiita 個別 URL (`https://qiita.com/furuse-kazufumi/items/<hash>`) に **一括置換** が必要.

### 4.1 URL 確定の蓄積場所

[`QIITA_#24_LINK_MAP.md`](QIITA_#24_LINK_MAP.md) に投稿後 URL を表で集約:

```markdown
| 連載 # | ローカル fname | Qiita URL |
|---|---|---|
| #24-00 | QIITA_#24_00_llive_tech_series_index.md | https://qiita.com/furuse-kazufumi/items/<hash00> |
| #24-01 | QIITA_#24_01_memory_layer.md | https://qiita.com/furuse-kazufumi/items/<hash01> |
| ... | ... | ... |
```

### 4.2 一括置換スクリプト (TODO)

`scripts/qiita_url_sync.py` (未実装) — LINK_MAP の表を読み込み、各記事内の cross-link を確定 URL に置換予定. 次セッション以降で実装.

## 5. preflight チェック

投稿前に必ず実行:

```powershell
py -3.11 scripts/qiita_preflight.py
```

各記事ごとに表示される項目:

- **pub**: ignorePublish の状態 (TRUE = まだ非公開, false = 公開準備, NO-FM = frontmatter なし)
- **priv**: private (Qiita 限定公開フラグ)
- **tag**: タグ数 (5 個まで推奨)
- **title**: タイトル文字数 (80 字以内推奨)
- **body**: 本文文字数
- **refs**: 未解決の内部参照数 (`QIITA_#NN_*` (内部参照) 形式が残っている数)

警告: `[TAGS=0]` `[TITLE-LONG]` `[REFS=N]` が表示されたら投稿前に解消推奨.

## 6. ハッシュタグ運用

Qiita タグ (5 個) と LinkedIn/Twitter ハッシュタグは別運用:

| 媒体 | タグ数 | 例 |
|---|---|---|
| Qiita | 5 個 | `LLM` `ローカルLLM` `Mamba` `RWKV` `Python` |
| LinkedIn | 5-11 個 | `#FullSense #llive #HarnessVibeCoding ...` |
| Twitter/X | 1-2 個 | `#FullSense` のみ |

## 7. 投稿フロー全体 (連載 #24 中心)

```
[投稿前]
  1. scripts/qiita_preflight.py で全件警告チェック
  2. NO-FM 14 件は frontmatter 補完 (タグ / title / private 等)
  3. TITLE-LONG 3 件は短縮検討
  4. 内部参照 #24_04 の 1 件を解消

[投稿]
  1. #14 から時系列で投稿 (上記 §2)
  2. 各記事は「限定共有」→ プレビュー → 「全体公開」の 2 段階
  3. 投稿後すぐに [QIITA_#24_LINK_MAP.md] に URL を記録

[投稿後]
  1. LINK_MAP 更新
  2. 連載 #24-00 (index) の cross-link を確定 URL に置換 (手動 or scripts/qiita_url_sync.py)
  3. LinkedIn 投稿 (LinkedIn_2026-05-22_harness_vibe_session.md) の deep link を Qiita URL に差替
  4. README に連載 index を追加
```

## 8. 関連

- [`scripts/qiita_preflight.py`]({{ '/scripts/qiita_preflight.py' | relative_url }}) — 投稿前検査
- [`scripts/qiita_url_sync.py`]({{ '/scripts/qiita_url_sync.py' | relative_url }}) — 投稿後 URL 一括置換 (TODO)
- [`QIITA_#24_LINK_MAP.md`](QIITA_#24_LINK_MAP.md) — 投稿後 URL 集約
- [`2026-05-18/POST_CHEATSHEET.md`](2026-05-18/POST_CHEATSHEET.md) — #18/#19 個別 cheat-sheet (本ガイドの前身)
- 連載 index: [`QIITA_#24_00_llive_tech_series_index.md`](QIITA_#24_00_llive_tech_series_index.md)
