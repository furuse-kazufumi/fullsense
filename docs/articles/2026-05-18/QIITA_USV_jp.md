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

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

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

---

# English

# I Built a Successor to CSV/TSV — USV (Unit-Separated Values) Makes AI ⇄ Human Tabular Data Exchange Effortless

**One-line hook**:
I put an end to the tab-width-4-vs-8 war by reactivating `U+001F`, a code point that ASCII reserved 60 years ago. Markdown, HTML, newlines, and tabs can all go straight into a cell. Tabular data exchange between AI and humans becomes reliably easier.

**Author**: furuse-kazufumi (FullSense umbrella OSS developer, Japan)
**Repo**: https://github.com/furuse-kazufumi/usrs
**Relationship to SixArm/usv / revival proposal Issue**: https://github.com/SixArm/usv/issues/14
**Community Discussion**: https://github.com/furuse-kazufumi/usrs/discussions/1
**License**: Apache-2.0 (pure OSS, free for commercial use)

---

## Why I Built It

While working with LLMs (Claude / GPT), I kept running into the same problems over and over:

- **When you ask an AI to output a Markdown table, the borders break on CJK characters or emoji**
- **When you ask for CSV / TSV output, explanatory text containing newlines falls apart in quoting**
- **When you ask for JSON output, it is hard for humans to read (I want to view it in a CLI)**

There simply was no "format that combines ruled lines with multi-line cells for tabular data."
That was the direct motivation for creating USV (Unit-Separated Values).

## The Core Idea of USV

> **Any string that contains neither U+001E nor U+001F can be stored
> verbatim as cell content.**

That is the entire specification.

| Role | Character | Unicode visible variant |
|---|---|---|
| Column separator | `U+001F` (US, Unit Separator) | `␟` (U+241F) |
| Row separator | `U+001E` (RS, Record Separator) | `␞` (U+241E) |

**The column separator renders as a vertical rule**, and **the row separator renders as a horizontal rule**. Because the separator characters double as the ruled-line information, no additional metadata is required.

### ☕ A Little Detour

The people who created ASCII (Bob Bemer and others, 1963) **reserved four characters — US / RS / GS / FS — as "Information Separators."** They were designed to denote hierarchical levels of data, but for roughly half a century they never caught on as a tabular data format.

**In 2022, Joel Parker Henderson was the first to publish a general-purpose OSS USV format as
[SixArm/usv](https://github.com/SixArm/usv)**, and an IETF Draft was even submitted in 2024 (now expired). The `usrs` introduced in this article respects that specification while extending it on three points: ruled-line-linked semantics, width metadata, and a 2-pane viewer. For details, see the "Relationship to Prior Projects" section at the end.

## What Goes Into a Cell — **Anything**

Other than ASCII US/RS, truly anything goes in:

| Type | Example |
|---|---|
| Newline `\n` | Multi-line cell (poems, long text, code snippets) |
| Tab `\t` | Indentation inside a cell |
| Markdown | `**bold**`, `# heading`, `[link](url)`, ``` `code` ``` |
| HTML | `<b>`, `<svg>`, `<kbd>Ctrl</kbd>+<kbd>C</kbd>` |
| LaTeX | `\sum_{i=0}^n \frac{x_i}{2}` |
| URI / data: | `https://...`, `data:image/png;base64,...` |
| Mixed languages | 日本語 / English / 中文 / 한국어 / العربية |

**There are no quoting / escape rules like CSV has**. You can drop in `,`, `"`, and `\n` as-is and it just works.

## Effect on AI ⇄ Human Communication

This is where USV **shines in the AI era**:

### Stabilizing LLM Output

```python
# LLM に「表で出して」と頼むときのプロンプト:
"""
出力形式は USV。区切りは U+001F (列) と U+001E (行)。
セル内には Markdown / 改行 / タブ / 任意 Unicode が入って良い。
escape は不要。
"""
```

The LLM **does not have to think about "do I need to quote? do I need to escape?"**
Output quality goes up.

### Token Efficiency of LLM Input

USV's separator characters are **1 byte in UTF-8**. Because you avoid CSV-style quote characters and JSON's `{ }` `[ ]` `,` `:`, passing tabular data to an LLM **reduces the token count**.

### Reducing the Human → AI Input Burden

When a human pastes a table into an AI, CSV forces you to worry about escaping commas, and Markdown tables break on CJK. With USV, you **just paste it and you're done**.

### ☕ Aside — the Phrase "AI ⇄ Human"

I develop an LLM framework called llive by myself.
I communicate with LLMs every day there, and I felt that **"format jitter is the biggest cost in a conversation."** If a single format can make that cost disappear, the AI ⇄ human relationship itself might change. USV is one small move toward that.

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

Example output (terminal):

```
┌──────────┬──────┬──────────────────────────┐
│ 商品     │ 個数 │ 備考                     │
├──────────┼──────┼──────────────────────────┤
│ Apple    │ 5    │ ## 詳細 ⏎ - 甘い ⏎ ...  │
│ みかん   │ 12   │ **酸っぱい** ⏎ 冬が旬     │
└──────────┴──────┴──────────────────────────┘
```

`⏎` is a marker indicating a newline. When you launch the **2-pane viewer**, the full content of the selected cell (rendered as Markdown, HTML-escaped, or plain) is shown in the right pane.

```bash
python -m usrs_viewer examples/sales.usv
```

## Side-by-Side With Existing Formats

| Format | Separator | Extension | MIME | Multi-line cell | Escape needed |
|---|---|---|---|---|---|
| CSV | `,` | `.csv` | `text/csv` | quote with `"..."` | yes |
| TSV | `\t` | `.tsv` | `text/tab-separated-values` | not possible (newline = end of row) | yes |
| **USV** | **U+001F + U+001E** | **`.usv`** | **`text/usv`** | **works as-is** | **none** |

### ☕ A Reserved Seat From 60 Years Ago

If you read the 1967 ASCII specification, you'll find four "Information Separators" lined up at `U+001C-001F`. They are clearly described as "characters for separating data into a hierarchical structure," but for a long time they never took hold as a common tabular data format.

As a general-purpose OSS, **Joel Parker Henderson's [SixArm/usv](https://github.com/SixArm/usv) came first in 2022**, and the `usrs` in this article is a derivative implementation that respects that specification (the three extensions are described later). Henderson was the one who first unearthed ASCII's reserved seat; my position is that I simply added one more chair to it.

## Adoption Strategy — I Want to Spread It Across Editors and Terminals

Because the specification is extremely simple (just two characters, US + RS, with a 1-page SPEC), the cost of integrating it into various editors is low. I want to spread it to the following:

- GitHub Linguist (recognize `.usv` as a language)
- Extensions for VS Code / Neovim / Helix / Zed / JetBrains
- Lexers for highlight.js / Pygments
- Terminal renderer hooks for iTerm2 / Wezterm / Alacritty
- Embed plugins for markdown-it / Pandoc

**If you're interested, please join via Issue / Discussion.**
I can't handle PRs to every editor on my own, so I'm recruiting contributors.

## Related Projects

USV is a small project independent of the FullSense umbrella, but its design decisions follow the FullSense philosophy:

- **llmesh** (LLM hub): on-prem MCP server, built-in SPC, direct industrial IoT connectivity
- **llive** (memory LLM framework): 4-layer memory + 6-stage Loop + TRIZ
- **llove** (TUI dashboard): reproduces Markdown / SVG / Mermaid in the terminal

llove plans to integrate the USV viewer as `F26: USV Table Widget`
(see: [SHOWCASE.md](https://github.com/furuse-kazufumi/usrs/blob/main/docs/SHOWCASE.md)).

## Roadmap

| Phase | Contents |
|---|---|
| **0.1.0-draft** (current) | SPEC + Python reference implementation + 2-pane viewer + 31 tests / zero regressions |
| 0.2.0 | Tree-sitter grammar, VS Code extension |
| 0.3.0 | Rust / TypeScript reference implementations, Web Component |
| 0.4.0 | gh-pages playground, plugin set for various editors |
| 1.0.0 | Consider submitting an IETF Draft as an RFC |

## Summary

- **USV (Unit-Separated Values) is a modern successor to CSV/TSV**
- **The separators are just two characters, US + RS**; everything else goes in as cell content, anything at all
- **AI ⇄ human tabular data exchange becomes reliably easier** (no escaping, no CJK breakage, multi-line OK)
- **Apache-2.0 pure OSS**, free for commercial use, contributions welcome

Repo: https://github.com/furuse-kazufumi/usrs
Includes SPEC / README / reference implementation / adoption strategy in full. Please drop by with a Star / Issue / Discussion.

**Relationship to SixArm USV (the prior project)**:
The ideas in this article (reactivating ASCII US/RS, using Unicode visible variants alongside them, and the universality of cell content) owe much to Joel Parker Henderson's [SixArm/usv](https://github.com/SixArm/usv) project (2022 onward). Since the 2024 IETF Draft had expired, I posted a [revival proposal Issue](https://github.com/SixArm/usv/issues/14) on 2026-05-17 (JST), bringing three additions (ruled-line-linked semantics / width metadata / 2-pane viewer). With respect for those who came before.

---

## Reference Links

- ASCII 1967 / ISO/IEC 646: the origin of Information Separators
- Unicode UAX #11: East Asian Width (the normative reference for CJK consideration)
- Unicode Control Pictures (U+2400-241F): the normative reference for visible variants
- RFC 4180: the current CSV standard
- My OSS llive / llove / llmesh: the FullSense umbrella

---

# 中文

# 我做了一个 CSV/TSV 的后继者 —— 用 USV (Unit-Separated Values) 让 AI ⇄ 人类的表格数据通信变轻松

**一行 hook**：
我通过重新激活 60 年前 ASCII 预留的 `U+001F`，为「制表符宽度 4 还是 8」的战争画上了句号。Markdown、HTML、换行、制表符都可以直接写进单元格。AI 与人类之间的表格数据通信一定会变得更轻松。

**作者**：furuse-kazufumi（FullSense umbrella OSS 开发者，日本）
**Repo**：https://github.com/furuse-kazufumi/usrs
**与 SixArm/usv 的关系 / revival 提案 Issue**：https://github.com/SixArm/usv/issues/14
**社区 Discussion**：https://github.com/furuse-kazufumi/usrs/discussions/1
**许可证**：Apache-2.0（纯 OSS，商用也自由）

---

## 为什么要做它

在与 LLM（Claude / GPT）一起工作时，我反复遇到同样的问题：

- **让 AI 用 Markdown 表格输出时，会因 CJK 字符或表情符号导致表格线错乱**
- **让它用 CSV / TSV 输出时，包含换行的说明文字会因为 quoting 而崩坏**
- **让它用 JSON 输出时，人类很难阅读（我想在 CLI 里看）**

「能同时兼顾表格线和多行单元格的表格数据格式」根本不存在。
这就是我创建 USV (Unit-Separated Values) 的直接动机。

## USV 的核心思想

> **任何既不含 U+001E 也不含 U+001F 的字符串，都可以原样
> 作为单元格内容存储。**

这就是规范的全部。

| 角色 | 字符 | Unicode 可见变体 |
|---|---|---|
| 列分隔符 | `U+001F` (US, Unit Separator) | `␟` (U+241F) |
| 行分隔符 | `U+001E` (RS, Record Separator) | `␞` (U+241E) |

**列分隔符渲染为竖线**，**行分隔符渲染为横线**。由于分隔符本身就兼任了表格线信息，因此不需要额外的元数据。

### ☕ 稍微跑个题

创造 ASCII 的人们（Bob Bemer 等人，1963）**把 US / RS / GS / FS 这 4 个字符预留为「Information Separators」**。它们原本被设计用来分别表示数据层级，但半个世纪以来几乎从未作为表格数据格式普及开来。

**2022 年，Joel Parker Henderson 首次以
[SixArm/usv](https://github.com/SixArm/usv) 的形式公开了通用 OSS 的
USV 格式**，并在 2024 年提交了 IETF Draft（目前已 expire）。本文介绍的 `usrs` 在尊重该规范的基础上，扩展了三点：表格线联动语义 / width metadata / 2-pane viewer。详情请参阅文末「与先行项目的关系」一节。

## 单元格里能放什么 —— **什么都行**

除了 ASCII US/RS 之外，真的什么都能放：

| 种类 | 示例 |
|---|---|
| 换行 `\n` | 多行单元格（诗、长文、代码片段） |
| 制表符 `\t` | 单元格内缩进 |
| Markdown | `**bold**`, `# heading`, `[link](url)`, ``` `code` ``` |
| HTML | `<b>`, `<svg>`, `<kbd>Ctrl</kbd>+<kbd>C</kbd>` |
| LaTeX | `\sum_{i=0}^n \frac{x_i}{2}` |
| URI / data: | `https://...`, `data:image/png;base64,...` |
| 多语言混排 | 日本語 / English / 中文 / 한국어 / العربية |

**不存在 CSV 那样的 quoting / escape 规则**。`,`、`"`、`\n` 都可以原样放进去。

## 对 AI ⇄ 人类沟通的效果

这正是 USV **在 AI 时代见效** 的地方：

### 稳定 LLM 输出

```python
# LLM に「表で出して」と頼むときのプロンプト:
"""
出力形式は USV。区切りは U+001F (列) と U+001E (行)。
セル内には Markdown / 改行 / タブ / 任意 Unicode が入って良い。
escape は不要。
"""
```

LLM **不必再去想「要不要 quote？要不要 escape？」**。
输出质量会提升。

### LLM 输入的 token 效率

USV 的分隔符在 **UTF-8 中是 1 字节**。由于可以避开 CSV 式的 quote 字符以及 JSON 的 `{ }` `[ ]` `,` `:`，把表格数据交给 LLM 时 **token 数会减少**。

### 降低人类 → AI 的输入负担

人类把表格粘贴给 AI 时，CSV 需要在意逗号的 escape，Markdown 表格又会在 CJK 上崩坏。用 USV 的话 **直接粘贴就完事了**。

### ☕ 闲话 —— 「AI ⇄ 人类」这个说法

我一个人开发着一个名为 llive 的 LLM 框架。
我每天都在那里与 LLM 通信，并感到 **「**格式抖动**是对话中最大的成本」**。如果仅凭一个格式就能消除它，那么 AI ⇄ 人类关系本身或许就会改变。USV 就是为此迈出的一小步。

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

输出示例（终端）：

```
┌──────────┬──────┬──────────────────────────┐
│ 商品     │ 個数 │ 備考                     │
├──────────┼──────┼──────────────────────────┤
│ Apple    │ 5    │ ## 詳細 ⏎ - 甘い ⏎ ...  │
│ みかん   │ 12   │ **酸っぱい** ⏎ 冬が旬     │
└──────────┴──────┴──────────────────────────┘
```

`⏎` 是表示换行的标记。启动 **2-pane viewer** 后，所选单元格的完整内容（按 Markdown rendered、HTML escaped、plain 之一）会显示在右侧面板。

```bash
python -m usrs_viewer examples/sales.usv
```

## 与既有格式的并列对比

| 格式 | 分隔符 | 扩展名 | MIME | 多行单元格 | 需要 escape |
|---|---|---|---|---|---|
| CSV | `,` | `.csv` | `text/csv` | 用 `"..."` quote | 需要 |
| TSV | `\t` | `.tsv` | `text/tab-separated-values` | 不可（换行 = 行结束） | 需要 |
| **USV** | **U+001F + U+001E** | **`.usv`** | **`text/usv`** | **原样 OK** | **无需** |

### ☕ 60 年前的预留座位

读一读 1967 年的 ASCII 规范书，会发现 `U+001C-001F` 处并排着 4 个「Information Separator」。它们被明确写作「用于把数据按层级结构分隔的字符」，但长期以来从未作为常见的表格数据格式扎根。

作为通用 OSS，**Joel Parker Henderson 的 [SixArm/usv](https://github.com/SixArm/usv) 在 2022 年率先出现**，本文的 `usrs` 是尊重该规范的派生实现（三点扩展见后述）。是 Henderson 最先发掘了 ASCII 的这个预留座位，而我的定位只是给它再添了一把椅子。

## 普及策略 —— 想推广到各种编辑器与终端

由于规范极其简洁（US + RS 两个字符，SPEC 一页），嵌入各种编辑器的成本很低。我想把它推广到以下场景：

- GitHub Linguist（把 `.usv` 识别为一种语言）
- VS Code / Neovim / Helix / Zed / JetBrains 的 extension
- highlight.js / Pygments 的 lexer
- iTerm2 / Wezterm / Alacritty 的 terminal renderer hook
- markdown-it / Pandoc 的 embed plugin

**有兴趣的朋友请务必通过 Issue / Discussion 参与。**
我一个人无暇给每个编辑器都提 PR，所以正在招募贡献者。

## 相关项目

USV 是一个独立于 FullSense umbrella 的小项目，但其设计判断遵循 FullSense 的哲学：

- **llmesh**（LLM hub）：on-prem MCP server、内置 SPC、直连工业 IoT
- **llive**（记忆 LLM framework）：4 层记忆 + 6 stage Loop + TRIZ
- **llove**（TUI dashboard）：在终端中再现 Markdown / SVG / Mermaid

llove 计划将 USV viewer 作为 `F26: USV Table Widget` 集成进来
（参见：[SHOWCASE.md](https://github.com/furuse-kazufumi/usrs/blob/main/docs/SHOWCASE.md)）。

## 路线图

| Phase | 内容 |
|---|---|
| **0.1.0-draft**（当前） | SPEC + Python 参考实现 + 2-pane viewer + 31 tests / 零回归 |
| 0.2.0 | Tree-sitter grammar、VS Code extension |
| 0.3.0 | Rust / TypeScript 参考实现、Web Component |
| 0.4.0 | gh-pages playground、各种编辑器插件群 |
| 1.0.0 | 作为 RFC 探讨提交 IETF Draft |

## 总结

- **USV (Unit-Separated Values) 是 CSV/TSV 的现代版后继者**
- **分隔符只有 US + RS 两个字符**，其余的都可以作为单元格内容放进去，什么都行
- **AI ⇄ 人类的表格数据通信一定会变轻松**（无需 escape、无 CJK 崩坏、支持多行）
- **Apache-2.0 纯 OSS**，商用也自由，欢迎贡献

Repo: https://github.com/furuse-kazufumi/usrs
完整包含 SPEC / README / 参考实现 / 普及策略。欢迎用 Star / Issue / Discussion 来逛逛。

**与 SixArm USV（先行项目）的关系**：
本文的发想（重新激活 ASCII US/RS、并用 Unicode 可见变体、单元格内容的普遍性）很大程度上得益于 Joel Parker Henderson 的 [SixArm/usv](https://github.com/SixArm/usv) 项目（2022 年起）。由于 2024 年的 IETF Draft 已 expire，我于 2026-05-17（JST）带着追加的三点（表格线联动语义 / width metadata / 2-pane viewer）提交了一个 [revival 提案 Issue](https://github.com/SixArm/usv/issues/14)。以此向先行者致敬。

---

## 参考链接

- ASCII 1967 / ISO/IEC 646：Information Separators 的起源
- Unicode UAX #11：East Asian Width（兼顾 CJK 的规范）
- Unicode Control Pictures (U+2400-241F)：可见变体的规范
- RFC 4180：CSV 的现行规格
- 拙作 OSS llive / llove / llmesh：FullSense umbrella

---

# 한국어

# CSV/TSV의 후계자를 만들었습니다 — USV (Unit-Separated Values)로 AI ⇄ 인간의 표 데이터 통신을 편하게

**한 줄 hook**:
탭 폭 4 대 8 전쟁에, 60년 전 ASCII가 예약해 둔 `U+001F`를 재활성화함으로써 종지부를 찍었습니다. Markdown도 HTML도 줄바꿈도 탭도 셀 안에 직접 쓸 수 있습니다. AI와 인간의 표 데이터 통신이 확실히 편해집니다.

**저자**: furuse-kazufumi (FullSense umbrella OSS 개발자, 일본)
**Repo**: https://github.com/furuse-kazufumi/usrs
**SixArm/usv와의 관계 / revival 제안 Issue**: https://github.com/SixArm/usv/issues/14
**커뮤니티 Discussion**: https://github.com/furuse-kazufumi/usrs/discussions/1
**라이선스**: Apache-2.0 (순수 OSS, 상용도 자유)

---

## 왜 만들었는가

LLM (Claude / GPT)과 일하면서, 같은 문제에 몇 번이고 부딪혔습니다:

- **AI에게 Markdown 표로 출력하게 하면, CJK 문자나 이모지에서 괘선이 무너진다**
- **CSV / TSV로 출력하게 하면, 줄바꿈을 포함한 설명문이 quoting에서 깨진다**
- **JSON으로 출력하게 하면, 인간이 읽기 어렵다 (CLI에서 보고 싶다)**

「표 데이터에 괘선과 멀티라인 cell을 양립시키는 format」이 존재하지 않는다.
이것이 USV (Unit-Separated Values)를 만든 직접적인 동기입니다.

## USV의 핵심 아이디어

> **U+001E와 U+001F를 포함하지 않는 문자열은, 모두 cell content로
> 그대로 저장 가능.**

이것이 사양의 전부입니다.

| 역할 | 문자 | Unicode 가시 변종 |
|---|---|---|
| 열 구분자 | `U+001F` (US, Unit Separator) | `␟` (U+241F) |
| 행 구분자 | `U+001E` (RS, Record Separator) | `␞` (U+241E) |

**열 구분자 = 세로 괘선으로 render**, **행 구분자 = 가로 괘선으로 render**. 구분 문자가 그대로 괘선 정보를 겸하므로, 추가 메타데이터는 필요 없습니다.

### ☕ 잠깐 옆길로

ASCII를 만든 사람들 (Bob Bemer 등, 1963)은 「Information Separators」로서 **US / RS / GS / FS의 4문자를 예약**해 두었습니다. 데이터 레벨의 계층을 각각 의미하는 설계였지만, 반세기 가까이 표 데이터 format으로는 거의 보급되지 않았습니다.

**2022년에 Joel Parker Henderson 씨가
[SixArm/usv](https://github.com/SixArm/usv)로서 처음으로 범용 OSS의
USV format을 공개**했고, 2024년에는 IETF Draft도 제출되었습니다 (현재는 expire). 본 기사에서 소개하는 `usrs`는 그 사양을 존중하면서, 괘선 연동 시맨틱스 / width metadata / 2-pane viewer의 3가지를 확장한 파생 구현입니다. 자세한 내용은 기사 말미의 「선행 프로젝트와의 관계」 절을 참조.

## cell에 무엇이 들어가는가 — **무엇이든**

ASCII US/RS 이외에는, 정말로 무엇이든 들어갑니다:

| 종류 | 예 |
|---|---|
| 줄바꿈 `\n` | 멀티라인 cell (시, 장문, 코드 스니펫) |
| 탭 `\t` | cell 내 들여쓰기 |
| Markdown | `**bold**`, `# heading`, `[link](url)`, ``` `code` ``` |
| HTML | `<b>`, `<svg>`, `<kbd>Ctrl</kbd>+<kbd>C</kbd>` |
| LaTeX | `\sum_{i=0}^n \frac{x_i}{2}` |
| URI / data: | `https://...`, `data:image/png;base64,...` |
| 다국어 혼재 | 日本語 / English / 中文 / 한국어 / العربية |

**CSV 같은 quoting / escape 규칙은 존재하지 않습니다**. `,`도 `"`도 `\n`도 그대로 넣어도 OK.

## AI ⇄ 인간 커뮤니케이션에 대한 효과

여기가 USV가 **AI 시대에 효과를 발휘하는** 포인트입니다:

### LLM 출력의 안정화

```python
# LLM に「表で出して」と頼むときのプロンプト:
"""
出力形式は USV。区切りは U+001F (列) と U+001E (行)。
セル内には Markdown / 改行 / タブ / 任意 Unicode が入って良い。
escape は不要。
"""
```

LLM은 **「quote 해야 하나 / escape 해야 하나」를 고민하지 않아도 됩니다**.
출력 품질이 올라갑니다.

### LLM 입력의 token 효율

USV의 구분 문자는 **UTF-8에서 1바이트**. CSV 같은 quote 문자나 JSON의 `{ }` `[ ]` `,` `:`를 피할 수 있으므로, 표 데이터를 LLM에 넘길 때 **token 수가 줄어듭니다**.

### 인간 → AI 입력 부담 절감

인간이 표를 AI에 붙여넣을 때, CSV는 콤마 escape를 신경 써야 하고, Markdown 표는 CJK에서 무너집니다. USV라면 **그냥 붙여넣고 끝**.

### ☕ 여담 — 「AI ⇄ 인간」이라는 말

저는 llive라는 LLM 프레임워크를 혼자서 개발하고 있습니다.
거기서 매일 LLM과 통신하면서, **「**포맷의 흔들림**이 대화의 최대 비용」**이라고 느끼고 있었습니다. format 하나로 이것이 사라진다면, AI ⇄ 인간 관계 그 자체가 바뀔 가능성이 있다. USV는 그것을 위한 작은 한 수입니다.

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

출력 예 (터미널):

```
┌──────────┬──────┬──────────────────────────┐
│ 商品     │ 個数 │ 備考                     │
├──────────┼──────┼──────────────────────────┤
│ Apple    │ 5    │ ## 詳細 ⏎ - 甘い ⏎ ...  │
│ みかん   │ 12   │ **酸っぱい** ⏎ 冬が旬     │
└──────────┴──────┴──────────────────────────┘
```

`⏎`는 줄바꿈을 나타내는 마커. **2-pane viewer**를 실행하면, 선택한 cell의 full content (Markdown rendered, HTML escaped, plain 중 하나)가 오른쪽 pane에 표시됩니다.

```bash
python -m usrs_viewer examples/sales.usv
```

## 기존 형식과의 병렬 비교

| 형식 | 구분자 | 확장자 | MIME | 멀티라인 cell | escape 필요 |
|---|---|---|---|---|---|
| CSV | `,` | `.csv` | `text/csv` | `"..."`로 quote | 있음 |
| TSV | `\t` | `.tsv` | `text/tab-separated-values` | 불가 (줄바꿈 = 행 종료) | 있음 |
| **USV** | **U+001F + U+001E** | **`.usv`** | **`text/usv`** | **그대로 OK** | **없음** |

### ☕ 60년 전의 예약석

ASCII 1967 사양서를 읽으면, `U+001C-001F`에는 4개의 「Information Separator」가 늘어서 있습니다. 「데이터를 계층 구조로 구분하기 위한 문자」라고 명확히 적혀 있지만, 오랫동안 일반적인 표 데이터 format으로는 정착되지 않았습니다.

범용 OSS로서는 **2022년에 Joel Parker Henderson 씨의
[SixArm/usv](https://github.com/SixArm/usv)가 선행**했으며, 본 기사의 `usrs`는 그 사양을 존중한 파생 구현입니다 (확장 3가지는 후술). ASCII의 예약석을 Henderson 씨가 가장 먼저 발굴했고, 저는 거기에 의자를 하나 더 놓았다는 위치입니다.

## 보급 전략 — 각종 에디터·터미널로 넓히고 싶다

사양이 극단적으로 간소하므로 (US + RS의 2문자, SPEC 1페이지), 각종 에디터에 끼워 넣는 비용이 낮습니다. 다음으로 넓혀 가고 싶습니다:

- GitHub Linguist (`.usv`를 언어로 인식)
- VS Code / Neovim / Helix / Zed / JetBrains에 extension
- highlight.js / Pygments에 lexer
- iTerm2 / Wezterm / Alacritty에 terminal renderer hook
- markdown-it / Pandoc에 embed plugin

**관심 있는 분은 Issue / Discussion으로 꼭.**
저 혼자서는 각 에디터에 대한 PR이 일손이 부족하므로, 컨트리뷰터를 모집합니다.

## 관련 프로젝트

USV는 FullSense umbrella에서 독립한 작은 프로젝트지만, 설계 판단은 FullSense의 철학을 따릅니다:

- **llmesh** (LLM hub): on-prem MCP server, SPC 내장, 산업 IoT 직결
- **llive** (기억 LLM framework): 4층 메모리 + 6 stage Loop + TRIZ
- **llove** (TUI dashboard): 터미널에서 Markdown / SVG / Mermaid를 재현

llove는 USV viewer를 `F26: USV Table Widget`으로서 통합 예정입니다
(참조: [SHOWCASE.md](https://github.com/furuse-kazufumi/usrs/blob/main/docs/SHOWCASE.md)).

## 로드맵

| Phase | 내용 |
|---|---|
| **0.1.0-draft** (현재) | SPEC + Python 참고 구현 + 2-pane viewer + 31 tests / 회귀 제로 |
| 0.2.0 | Tree-sitter grammar, VS Code extension |
| 0.3.0 | Rust / TypeScript 참고 구현, Web Component |
| 0.4.0 | gh-pages 플레이그라운드, 각종 에디터 플러그인 군 |
| 1.0.0 | RFC로서 IETF Draft 제출 검토 |

## 정리

- **USV (Unit-Separated Values)는 CSV/TSV의 현대판 후계자**
- **구분자는 US + RS의 2문자뿐**, 그 외에는 cell content로서 무엇이든 들어간다
- **AI ⇄ 인간의 표 데이터 통신이 확실히 편해진다** (escape 불필요, CJK 무너짐 없음, 멀티라인 OK)
- **Apache-2.0 순수 OSS**, 상용도 자유, 기여 환영

Repo: https://github.com/furuse-kazufumi/usrs
SPEC / README / 참고 구현 / 보급 전략 모두 포함. Star / Issue / Discussion으로 꼭.

**SixArm USV (선행 프로젝트)와의 관계**:
본 기사의 발상 (ASCII US/RS 재활성화, Unicode 가시 변종 병용, cell content 보편성)은 Joel Parker Henderson 씨의 [SixArm/usv](https://github.com/SixArm/usv) 프로젝트 (2022년~)에 많은 것을 빚지고 있습니다. 2024년에 IETF Draft가 expire되어 있었으므로, 추가 3가지 (괘선 연동 시맨틱스 / width metadata / 2-pane viewer)를 가지고 [revival 제안 Issue](https://github.com/SixArm/usv/issues/14)를 2026-05-17 (JST)에 투고했습니다. 선인에 대한 경의를 담아.

---

## 참고 링크

- ASCII 1967 / ISO/IEC 646: Information Separators의 기원
- Unicode UAX #11: East Asian Width (CJK 배려의 규범)
- Unicode Control Pictures (U+2400-241F): 가시 변종의 규범
- RFC 4180: CSV의 현행 규격
- 졸작 OSS llive / llove / llmesh: FullSense umbrella
