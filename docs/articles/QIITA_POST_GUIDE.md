---
layout: default
title: "Qiita 投稿準備ガイド (2026-05-22 整備)"
nav_order: 95
---

# Qiita 投稿準備ガイド

> docs/articles/ 直下の `QIITA_#NN_*.md` を Qiita Web UI から投稿するための one-shot ガイド.
> 各記事の状態は `scripts/qiita_preflight.py` で随時確認可能.
> 既存 [`POST_CHEATSHEET.md`](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-18/POST_CHEATSHEET.md) (#18/#19 専用) を全 #14〜#24 系列に一般化したもの.

## 1. 現状サマリ (2026-05-22 preflight 整備後)

| カテゴリ | 件数 | 状態 |
|---|---|---|
| **frontmatter 整備済** | 19 件 | skeleton 一括挿入 (`scripts/qiita_frontmatter_skeleton.py`) で 14 件補完 + 既存 5 件 |
| **Jekyll-only frontmatter** | 1 件 | #20 (layout/nav_order). Qiita 投稿時に Jekyll fm を削除 → Qiita 用 fm に書換 |
| **TAGS=TODO** | 12 件 | NO-FM 補完時に TODO_TAG プレースホルダ. 投稿前に記事末尾 `## 投稿時の推奨タグ` から差替 |
| **TITLE-LONG (80 字超)** | 4 件 | #22 (89), #24_04 (84), #24_06 (84), #24_07 (84) — 投稿時に短縮検討 |
| **REFS 未解決** | 1 件 | #24_04 (内部参照 1 件残, 投稿後 URL 確定時に置換) |
| **ignorePublish: true** | 19 件 | 全 frontmatter ありで draft 状態. 投稿時に false に切替 |
| **本文サイズ** | 3KB〜16KB | 全件 Qiita 投稿可能範囲 (上限 1MB) |

### 1.1 #20 (Jekyll frontmatter) の特別扱い

`QIITA_#20_one_session_full_stack_progress.md` は Jekyll 用 frontmatter
(`layout: default` / `parent: ...` / `nav_order: 1`) を持っている.
これは GitHub Pages 用なので、Qiita 投稿時には:

1. Jekyll frontmatter (`---...---`) を **削除**
2. 代わりに Qiita 用 frontmatter (title / tags / private / ignorePublish 等) を **追加**
3. 本文の `# 1 セッション...` H1 はそのまま残す (Qiita 上では body 内 H1 として表示)

または Jekyll fm を残したまま Qiita 投稿時にコピペ範囲を「6 行目以降」に限定する形でも可.

### 1.2 TAGS=TODO の解消

frontmatter skeleton 挿入時、記事末尾の `## 投稿時の推奨タグ` セクションが
無い記事には `TODO_TAG` プレースホルダを 2 個入れている. 投稿前に:

1. 記事内容に合うタグを 2 個選定 (例: `LLM`, `アルゴリズム`, `Python`, `自己進化`, `TRIZ` 等)
2. `tags:` の `- TODO_TAG` を該当タグに書換

例: `QIITA_#24_05_evolutionary_v0BCDE.md`

```yaml
tags:
  - FullSense
  - llive
  - 解説
  - TODO_TAG    # → 例: 進化アルゴリズム
  - TODO_TAG    # → 例: 派生集団進化
```

### 1.3 本文は「多ければ多いほど良い」(2026-05-22 ユーザー再強調)

本文文字数 (body) は **上限なし、多ければ多いほど良い**. [[feedback_qiita_long_form]] (2-3 万字級歓迎) からさらに昇格して、**30k / 50k / 100k 字級も全部 OK**. Qiita 投稿の技術的上限 (1MB) までは安心して詰め込んで良い.

理由:

- 連載 #14〜#24 の繋がりが本文ボリュームで補強される (相互参照が増えるほど SEO + retention 向上)
- ベンチ詳細 / 数式展開 / 失敗パターン / honest disclosure 内訳 / コード片 / 表 / 図 を **削らない**
- full 10x volume 版 (各 80-150k 字) は次セッション以降の予定 ([[QIITA_#24_00]] 既述)
- 「冗長なら削れ」は **タイトル限定**. 本文は密度 × リズム ([[feedback_reader_attention_curve]] 3 スケール 8 秒/90 秒/5 分) で長尺維持
- 雑談ポイント ([[feedback_article_break_points]]) も多めに挿入して読み手の集中力を維持しつつ、結果として総量を増やす方向

現状: 最大 16,068 字 (#21). これでもまだ控えめ. 次回拡張時は **倍の 30k 字級** を default に.

### 1.4 TITLE-LONG の短縮候補 (本文ではなくタイトルのみ)

| # | 現タイトル (字数) | 短縮候補 |
|---|---|---|
| #22 | 89 字 | "Transformer 一強を切り崩す" を抜く / "FullSense 進捗" を抜く 等で 60〜70 字へ |
| #24_04 | 84 字 | "「収束する脳」B-series: SynapticSelector / UCB1 / Hebbian" 程度に短縮 |
| #24_06 | 84 字 | "「Transformer の外」: Mamba / Jamba / RWKV / Diffusion" 程度に短縮 |
| #24_07 | 84 字 | "「審査つき AI」: runtime_metadata × Approval Bus × Ed25519" 程度に短縮 |

Qiita タイトルは 80 字以内が見やすいが、80 字超でも投稿自体は可能.

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

- [`scripts/qiita_preflight.py`](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/scripts/qiita_preflight.py) — 投稿前検査
- [`scripts/qiita_url_sync.py`](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/scripts/qiita_url_sync.py) — 投稿後 URL 一括置換 (TODO)
- [`QIITA_#24_LINK_MAP.md`](QIITA_#24_LINK_MAP.md) — 投稿後 URL 集約
- [`2026-05-18/POST_CHEATSHEET.md`](2026-05-18/POST_CHEATSHEET.md) — #18/#19 個別 cheat-sheet (本ガイドの前身)
- 連載 index: [`QIITA_#24_00_llive_tech_series_index.md`](QIITA_#24_00_llive_tech_series_index.md)
