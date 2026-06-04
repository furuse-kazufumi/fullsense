---
title: 'CSV/TSV の後継を作りました — USV (Unit-Separated Values) で AI ⇄ 人間の表データ通信を楽にする'
tags:
  - FullSense
  - USV
  - データフォーマット
  - CSV
  - 解説
private: false
id: fda1d13c689095720534
---

# CSV/TSV の後継を作りました — USV (Unit-Separated Values) で AI ⇄ 人間の表データ通信を楽にする

**1 行 hook**:
タブ幅 4 vs 8 の戦争に、60 年前の ASCII が予約していた `U+001F` を再活性化することで終止符を打ちました。Markdown も HTML も改行もタブもセル内に直接書ける。AI と人間の表データ通信が確実に楽になります。

**作者**: furuse-kazufumi (FullSense umbrella OSS 開発者、日本)
**Repo**: https://github.com/furuse-kazufumi/usrs
**SixArm/usv との関係 / revival 提案 Issue**: https://github.com/SixArm/usv/issues/14
**コミュニティ Discussion**: https://github.com/furuse-kazufumi/usrs/discussions/1
**ライセンス**: Apache-2.0 (純 OSS、商用も自由)

---

## なぜ作ったか

LLM (Claude / GPT) と仕事をしていて、何度も同じ問題に遭遇しました:

- **AI に Markdown 表で出力させると、CJK 文字や絵文字で罫線が崩れる**
- **CSV / TSV で出力させると、改行を含む説明文が quoting で破綻**
- **JSON で出力させると、人間が読みづらい (CLI で見たい)**

「表データに罫線とマルチライン cell を両立する format」が存在しない。
これが USV (Unit-Separated Values) を作った直接の動機です。

## USV の核心アイデア

> **U+001E と U+001F を含まない文字列は、すべて cell content として
> そのまま格納可能。**

これが仕様の全て。

| 役割 | 文字 | Unicode 可視変種 |
|---|---|---|
| 列区切り | `U+001F` (US, Unit Separator) | `␟` (U+241F) |
| 行区切り | `U+001E` (RS, Record Separator) | `␞` (U+241E) |

**列区切り = 縦罫線として render**、**行区切り = 横罫線として render**。
区切り文字がそのまま罫線情報を兼ねるので、追加メタデータは要りません。

### ☕ ちょっと脱線

ASCII を作った人達 (Bob Bemer ら、1963) は「Information Separators」として
**US / RS / GS / FS の 4 文字を予約**していました。データレベルの階層を
それぞれ意味する設計だったのですが、半世紀ほぼ表データ format として
普及することはありませんでした。

**2022 年に Joel Parker Henderson 氏が
[SixArm/usv](https://github.com/SixArm/usv) として初めて汎用 OSS の
USV format を公開**し、2024 年に IETF Draft も提出されました (現在は
expire)。本記事で紹介する `usrs` はその仕様を尊重しつつ、罫線連動
セマンティクス / width metadata / 2-pane viewer の 3 点を拡張した
派生実装です。詳細は記事末「先行プロジェクトとの関係」節を参照。

## 何が cell に入るか — **何でも**

ASCII US/RS 以外、本当に何でも入ります:

| 種別 | 例 |
|---|---|
| 改行 `\n` | マルチライン cell (詩、長文、コードスニペット) |
| タブ `\t` | cell 内インデント |
| Markdown | `**bold**`, `# heading`, `[link](url)`, ``` `code` ``` |
| HTML | `<b>`, `<svg>`, `<kbd>Ctrl</kbd>+<kbd>C</kbd>` |
| LaTeX | `\sum_{i=0}^n \frac{x_i}{2}` |
| URI / data: | `https://...`, `data:image/png;base64,...` |
| 多言語混在 | 日本語 / English / 中文 / 한국어 / العربية |

**CSV のような quoting / escape ルールは存在しません**。`,` も `"` も
`\n` もそのまま入れて OK。

## AI ⇄ 人間コミュニケーションへの効果

ここが USV が **AI 時代に効く** ポイントです:

### LLM 出力の安定化

```python
# LLM に「表で出して」と頼むときのプロンプト:
"""
出力形式は USV。区切りは U+001F (列) と U+001E (行)。
セル内には Markdown / 改行 / タブ / 任意 Unicode が入って良い。
escape は不要。
"""
```

LLM は **「quote しなきゃ / escape しなきゃ」を考えなくて良い**。
出力品質が上がります。

### LLM 入力の token 効率

USV の区切り文字は **UTF-8 で 1 バイト**。CSV のような quote 文字や
JSON の `{ }` `[ ]` `,` `:` を避けられるので、表データを LLM に
渡すとき **token 数が減ります**。

### 人間 → AI の入力負荷削減

人間が表を AI に貼り付けるとき、CSV はカンマ escape を気にする必要が
あり、Markdown 表は CJK で崩れる。USV なら **そのまま貼って終わり**。

### ☕ 余談 — 「AI ⇄ 人間」という言葉

私は llive という LLM フレームワークを 1 人で開発しています。
そこで毎日 LLM と通信していて、**「**フォーマットの揺れ**が会話の最大コスト」** だと
感じていました。format 1 つでこれが消えるなら、AI ⇄ 人間関係そのものが
変わる可能性がある。USV はそのための小さな一手です。

## Quick Start (Python)

```python
# pip install textual  # viewer 用 (optional)

from usrs import dumps, loads, render

rows = [
    ["商品", "個数", "備考"],
    ["Apple", "5", "## 詳細\n- 甘い\n- 旬は秋\n- [link](https://example.com)"],
    ["みかん", "12", "**酸っぱい**\n冬が旬"],
]
text = dumps(rows, with_width=True)
print(render(loads(text)))
```

出力例 (端末):

```
┌──────────┬──────┬──────────────────────────┐
│ 商品     │ 個数 │ 備考                     │
├──────────┼──────┼──────────────────────────┤
│ Apple    │ 5    │ ## 詳細 ⏎ - 甘い ⏎ ...  │
│ みかん   │ 12   │ **酸っぱい** ⏎ 冬が旬     │
└──────────┴──────┴──────────────────────────┘
```

`⏎` は改行を示すマーカー。**2 ペインビューワー** を起動すると、選択した
cell の full content (Markdown rendered, HTML escaped, plain のいずれか)
が右ペインに表示されます。

```bash
python -m usrs_viewer examples/sales.usv
```

## 既存形式との並列

| 形式 | 区切り | 拡張子 | MIME | マルチライン cell | escape 必要 |
|---|---|---|---|---|---|
| CSV | `,` | `.csv` | `text/csv` | `"..."` で quote | あり |
| TSV | `\t` | `.tsv` | `text/tab-separated-values` | 不可 (改行 = 行終了) | あり |
| **USV** | **U+001F + U+001E** | **`.usv`** | **`text/usv`** | **そのまま OK** | **無し** |

### ☕ 60 年前の予約席

ASCII 1967 仕様書を読むと、`U+001C-001F` には 4 つの「Information
Separator」が並んでいます。「データを階層構造で区切るための文字」と
明確に書かれていますが、長らく一般的な表データ format としては定着
していませんでした。

汎用 OSS としては **2022 年に Joel Parker Henderson 氏の
[SixArm/usv](https://github.com/SixArm/usv) が先行**しており、本記事の
`usrs` はその仕様を尊重した派生実装です (拡張 3 点は後述)。
ASCII の予約席を Henderson 氏が最初に発掘し、私はそこに椅子を 1 脚
足したという立ち位置です。

## 普及戦略 — 各種エディタ・ターミナルに広げたい

仕様が極端に簡素 (US + RS の 2 文字、SPEC 1 ページ) なので、各種エディタ
への組み込みコストが低い。以下に広げていきたいです:

- GitHub Linguist (`.usv` を言語として認識)
- VS Code / Neovim / Helix / Zed / JetBrains に extension
- highlight.js / Pygments に lexer
- iTerm2 / Wezterm / Alacritty に terminal renderer hook
- markdown-it / Pandoc に embed plugin

**興味のある方は Issue / Discussion でぜひ**。
私 1 人では各エディタへの PR は手が足りないので、
コントリビューターを募集します。

## 関連プロジェクト

USV は FullSense umbrella から独立した小さなプロジェクトですが、設計判断は
FullSense の哲学に従います:

- **llmesh** (LLM hub): on-prem MCP server、SPC 内蔵、産業 IoT 直結
- **llive** (記憶 LLM framework): 4 層メモリ + 6 stage Loop + TRIZ
- **llove** (TUI dashboard): 端末で Markdown / SVG / Mermaid を再現

llove は USV viewer を `F26: USV Table Widget` として統合予定です
(参照: [SHOWCASE.md](https://github.com/furuse-kazufumi/usrs/blob/main/docs/SHOWCASE.md))。

## ロードマップ

| Phase | 内容 |
|---|---|
| **0.1.0-draft** (現在) | SPEC + Python 参考実装 + 2-pane viewer + 31 tests / 回帰ゼロ |
| 0.2.0 | Tree-sitter grammar、VS Code extension |
| 0.3.0 | Rust / TypeScript 参考実装、Web Component |
| 0.4.0 | gh-pages プレイグラウンド、各種エディタプラグイン群 |
| 1.0.0 | RFC として IETF Draft 提出検討 |

## まとめ

- **USV (Unit-Separated Values) は CSV/TSV の現代版後継**
- **区切りは US + RS の 2 文字だけ**、それ以外は cell content として
  何でも入る
- **AI ⇄ 人間の表データ通信が確実に楽になる** (escape 不要、CJK 崩れ
  なし、マルチライン OK)
- **Apache-2.0 純 OSS**、商用も自由、貢献歓迎

Repo: https://github.com/furuse-kazufumi/usrs
SPEC / README / 参考実装 / 普及戦略すべて含む。Star / Issue / Discussion でぜひ。

**SixArm USV (先行プロジェクト) との関係**:
本記事の発想 (ASCII US/RS 再活性化、Unicode 可視変種併用、cell content
普遍性) は Joel Parker Henderson 氏の [SixArm/usv](https://github.com/SixArm/usv)
プロジェクト (2022 年〜) に多くを負います。2024 年に IETF Draft が
expire していたので、追加 3 点 (罫線連動セマンティクス / width metadata /
2-pane viewer) を持って [revival 提案 Issue](https://github.com/SixArm/usv/issues/14)
を 2026-05-17 (JST) に投稿しました。先人への敬意を込めて。

---

## 参考リンク

- ASCII 1967 / ISO/IEC 646: Information Separators の起源
- Unicode UAX #11: East Asian Width (CJK 配慮の規範)
- Unicode Control Pictures (U+2400-241F): 可視変種の規範
- RFC 4180: CSV の現行規格
- 拙 OSS llive / llove / llmesh: FullSense umbrella

<!-- llive:meta.article_id="QIITA_USV_jp" target=llove -->
<!-- llive:meta.published_date="2026-05-18" -->
<!-- llive:meta.tags=["usv","csv","tsv","ascii","unicode","ai","llm","editor","oss"] target=any -->
<!-- llive:meta.author="furuse-kazufumi" -->
