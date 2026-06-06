---
title: HTML で見えないのに、機械では読める。— llive が採用した「不可視アノテーションチャネル」設計
tags:
  - FullSense
  - llive
  - 解説
  - TODO_TAG
  - TODO_TAG
private: false
updated_at: '2026-05-22'
id: 851773b6cfe85c7811a4
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# HTML で見えないのに、機械では読める。— llive が採用した「不可視アノテーションチャネル」設計

> 📚 **連載ナビ**: ← #13 コーパス先行戦略 ｜ **#14 本記事** ｜ #15 「第二の脳」開発論 → ｜ [連載 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 各記事は単独でも読めます（リンクは回遊用）。
>
> 前記事 #13 では、AI が背景でコーパスを参照して **気づかない観点を補ってくれる** 話をした。本記事は視点を内から外へ移す——独立した 3 プロダクトが、互いを知らないまま **どうやって親切にし合えるか** という配線の話だ。

**1 行 hook**:
ある日、SNS にこんなコメントが届いた。「3 つのプロダクトが相互依存していたら、1 つだけ使う価値が半減するよね」。返答は **コメントアウト** だった — `<!-- llive:cog.consensus="proceed" -->`。なぜたった 1 行のコメントが、その矛盾への答えになるのか。

---

## なぜこの記事を書くか

OSS マルチプロダクト構成では、毎回 **「独立して動くこと」と「組み合わせて価値が積み上がること」** が両立しにくい。前者を取れば「結局単体で物足りない」、後者を取れば「全部入れないと壊れる」になる。

llive (`llive` — L は 2 個。L 3 個の `lllive` ではない。tokenizer 問題で過去事故あり) では、この二律背反を **アノテーションを HTML コメント形式に閉じ込める** という一手で解いた。本記事はその設計の経緯と実装、ベンチ結果を共有する。

## 起点 — LinkedIn コメント

```
llive の記憶層が llove の交互データに依存し、llove がまた llmesh の
接続能力に依存しているなら、その中の一つだけを使う価値は半減します。
理想的なのは、各層が独立して価値を提供でき、組み合わせることで効果が
積み上がる設計であり、全部揃えないと動かないという状況は避けるべきです。
```

このコメントを受けて、llive の `src/llive` 全 172 ファイルに対し AST スキャン (`scripts/audit_independence.py`) を走らせた。結果は **hard import leak 0 件**。llive は llove/llmesh への runtime 依存を最初から持っていなかった。

問題は次の段階だった。「**じゃあ独立性を保ったまま、どうやって組合せ価値を増やすか**」。

## 筆者の設計メモ — 「アノテーションを用意したらいいのでは」

そこで筆者は次のような設計メモを残した。

```
応答にアノテーションを用意すれば独立性を保ちながら組み合わせでの
効果も得られるのではないか
```

これが採用された設計の原型。さらに条件を絞った。

```
邪魔にならない程度のアノテーションにしておく必要があるな。
HTML にしたら不可視になるような感じがいいかもしれない。
```

ここで条件が固まった。

1. **emit 側 (llive)** は consumer を知らずに hint を出すだけ
2. **consumer 側 (llove TUI / llmesh visualizer / 外部 agent)** は読んでも無視してもよい
3. 既存の Human-facing 出力を **絶対に汚さない**
4. **HTML/Markdown で renderer が表示しない**

### ☕ ちょっと余談

ここまで「コメントアウトでした」と書いてきたが、実は最初に LinkedIn コメントを読んだとき、3 秒くらい固まった。「いやそれ全部入れないと動かないやつでしょ普通…」と。AST スキャンを回したら 0 件 leak だったので、過去の自分に救われた形になる。設計の判断は時々、未来から見ると正解になる。

## 採用した設計

`src/llive/annotations.py` に以下の最小型を実装した。

```python
@dataclass(frozen=True)
class Annotation:
    namespace: str          # "vrb" / "oka" / "cog" / "math" / "creat" / "core"
    key: str
    value: Any              # JSON-friendly (str/int/float/bool/None/list/dict)
    target_layer: str | None = None   # "llove" / "llmesh" / None=any
```

これを束ねる `AnnotationBundle` が `to_html_comments()` / `from_html_comments()` 双方向のシリアライザを持つ。出力例:

```
<!-- llive:core.brief_completed=true -->
<!-- llive:oka.essence_card={"summary": "..."} target=llove -->
<!-- llive:cog.consensus="proceed" -->
```

Markdown renderer (GitHub / Qiita / Zenn / VS Code Preview) では完全に **不可視**。一方で `AnnotationBundle.from_html_comments(text)` を呼べば、機械側は元の構造を完全に復元できる。

## なぜ HTML コメントなのか

選択肢は他にもあった。

| 案 | 不可視性 | 機械可読性 | 既存ツール互換 |
|---|---|---|---|
| JSON 別ファイル | ◯ | ◯ | ✕ (2 ファイル管理) |
| YAML front matter | △ (一部 renderer で表示) | ◯ | △ |
| **HTML コメント** | ◎ | ◎ | ◎ (Markdown 標準) |
| バイナリ埋込 | ◎ | △ | ✕ |
| zero-width Unicode | ◎ | △ | ✕ (copy-paste で消える) |

HTML コメントの利点は「**Markdown が HTML を passthrough する事実**」を逆手にとっている点。Markdown の歴史的仕様で `<!-- ... -->` は HTML として出力され、ブラウザ / Markdown viewer は HTML コメントを表示しない。結果として「**今あなたが見ている記事の隅々**」に Annotation を仕込んでも、読者は気づかない。

(試しに、この段落の末尾にも 1 つ仕込んでみよう。)
<!-- llive:meta.article_id="14_invisible_annotation_channel" target=llove -->

### ☕ ちなみに

HTML コメントを Markdown に仕込むテクは、Jekyll や Hugo の界隈では「**コメント front matter**」と呼ばれて昔からある。新しいのは「**Markdown 本文の任意位置**に機械可読メタデータを置く」発想の方。front matter は冒頭固定、こちらは段落単位で散らせる。

## llive 実装での自然な emit

`BriefRunner.submit(brief)` 内で、毎 Brief 終了時に Annotation 群が自動で emit される。

```python
emitter = AnnotationEmitter()
emitter.add("core", "brief_completed", value=True)
if essence is not None:
    emitter.add("oka", "essence_card",
                value={"summary": essence.essence_summary, "mystery": essence.mystery},
                target_layer="llove")
if perspective_summary is not None:
    emitter.add("cog", "consensus", value=perspective_summary.consensus_recommendation)
    if perspective_summary.risk_score >= 0.6:
        emitter.add("cog", "risk_alert",
                    value={"risk_score": perspective_summary.risk_score},
                    target_layer="llove")
if lint_report is not None and lint_report.findings:
    emitter.add("vrb", "lint_findings_count",
                value=len(lint_report.findings),
                target_layer="llove")
```

ここで重要なのは **誰も `import llove` していない**。llive が単独で動くときも、これらの annotation は単に **使われない hint** として残るだけだ。

llove (将来の TUI) は `AnnotationBundle.from_html_comments(brief_result.body)` を呼ぶことで、`cog.risk_alert` を見つけ次第ハイライト表示する、といったことができる。**llive は llove の存在を知らないまま、llove に親切にする**。

## 性能ベンチ

`scripts/bench_annotations.py` で 1000 件 round-trip を計測した。

| 操作 | レイテンシ |
|---|---|
| Build 1 件 | 7.95 µs |
| Encode (HTML comments) per ann | 6.30 µs |
| Decode per ann | 12.40 µs |
| `for_layer()` 1000 件 bundle | 0.13 ms / call |
| 1000 件 round-trip OK | ✓ |

典型的な BriefResult.annotations は 3 件なので **encoded サイズ 141 バイト**。Markdown 1 ページに 100 個仕込んでも 5 KB 以下。

## 何が「設計の妙」か

この仕組みが面白いのは、**3 つの責務を 1 つのフォーマットで満たした**ところにある。

| 責務 | 担保している要素 |
|---|---|
| **独立性** (IND-01) | emit 側は consumer を知らない、`import` 関係ゼロ |
| **組合せ価値** (IND-02) | consumer が `from_html_comments()` を呼ぶだけで複数 hint を取得 |
| **既存出力の不汚染** | HTML コメントは renderer で完全に消える |

OSS で 3 つのプロダクトを並べるとき、よくある失敗が「protobuf スキーマで bind しすぎて 1 個変えると全部壊れる」「DI コンテナで配線したつもりが暗黙 import になっている」だ。**プレーンテキストの中にコメントを仕込む** という古典的アプローチが、現代的な multi-package OSS の課題を素直に解いた。

## トレーサビリティとの接続

Annotation は `BriefLedger` (append-only JSONL) に書き込まれる `perspectives_observed` / `lint_findings_recorded` などの ledger event とは別系統だ。

| | 用途 | 永続性 |
|---|---|---|
| **Ledger event** | 機械監査 (SEC-03 hash chain)、replay 可能 | 永続 (JSONL) |
| **Annotation** | consumer への hint (UI render / 別 agent 連携) | 揮発 (BriefResult のフィールド) |

両者は重複しない。ledger は **過去の事実**、annotation は **未来の consumer への示唆**。

## まとめ

- LinkedIn のコメント 1 通から始まり、`<!-- llive:ns.key=val -->` という古典フォーマットに着地した
- 独立性監査で 172 ファイル中 hard leak 0 件を機械保証
- 1000 件 encode 6 ms、典型 3 件 bundle 141 バイト = 邪魔にならない footprint
- emit 側は consumer を知らず、consumer 側は emit を要求しない = 完全に optional な connector
- 既存の Markdown/HTML 出力は **完全に汚染されない**

OSS マルチプロダクト構成で「**独立性と組合せ価値の両立**」に悩んでいる方は、ぜひ HTML コメント形式の annotation channel を試してみてほしい。実装は 200 行ちょっとで済む。

---

**Repo**: https://github.com/furuse-kazufumi/llive (Apache-2.0 + Commercial dual-license)

**実装**: `src/llive/annotations.py`, `src/llive/brief/render.py`, `src/llive/brief/runner.py`

**過去の関連記事 (連載)**:
- [12] llive 開発履歴 — 5 日で v0.1 から v0.7 候補へ
- [13] コーパス先行戦略 — AI が気づかない観点を思考フローに補完

## 参考文献 / 参考仕様

- **CommonMark Spec** (Markdown 標準仕様) — HTML コメント passthrough の根拠
  https://spec.commonmark.org/
- **HTML Living Standard** (WHATWG) — `<!-- ... -->` 構文と renderer 動作
  https://html.spec.whatwg.org/multipage/syntax.html#comments
- **Front matter** (Jekyll 等で利用される YAML metadata 形式) — 不採用案として比較
  https://jekyllrb.com/docs/front-matter/
- **llive リポジトリ** — 本記事で扱った実装の原典
  https://github.com/furuse-kazufumi/llive

---

<!-- llive:meta.next_article="15_..." target=llove -->
<!-- llive:meta.published_date="2026-05-18" -->
<!-- llive:meta.tags=["llive","annotation","design","oss","independence"] target=any -->

---

# English

# Invisible in HTML, readable by machines — the "invisible annotation channel" design llive adopted

> 📚 **Series nav**: **#14 (this article)** ｜ #15 "The Second Brain" Development Theory → ｜ [Series LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ Each article reads fine on its own (links are just for browsing).

**One-line hook**:
One day a comment landed on social media: "If three products all depend on each other, the value of using just one of them is cut in half, isn't it?" The reply was a **comment-out** — `<!-- llive:cog.consensus="proceed" -->`.

---

## Why I'm writing this article

In an OSS multi-product setup, it's perpetually hard to satisfy both **"each piece works independently"** and **"value accumulates when you combine them."** Lean toward the former and you end up with "honestly underwhelming on its own"; lean toward the latter and you get "nothing works unless you install everything."

In llive (`llive` — that's two L's. Not `lllive` with three L's; there was a past incident due to a tokenizer issue), we solved this dilemma with a single move: **confining the annotations to an HTML-comment format**. This article shares the background, implementation, and benchmark results of that design.

## Origin — a LinkedIn comment

```
llive の記憶層が llove の交互データに依存し、llove がまた llmesh の
接続能力に依存しているなら、その中の一つだけを使う価値は半減します。
理想的なのは、各層が独立して価値を提供でき、組み合わせることで効果が
積み上がる設計であり、全部揃えないと動かないという状況は避けるべきです。
```

Prompted by this comment, I ran an AST scan (`scripts/audit_independence.py`) against all 172 files of llive's `src/llive`. The result: **0 hard import leaks**. llive had never carried any runtime dependency on llove/llmesh in the first place.

The problem was the next stage: "**OK, so while preserving independence, how do you actually increase combination value?**"

## The author's design memo — "What if we just provide annotations?"

So I left a design memo like this.

```
応答にアノテーションを用意すれば独立性を保ちながら組み合わせでの
効果も得られるのではないか
```

This became the prototype of the adopted design. I then narrowed the conditions further.

```
邪魔にならない程度のアノテーションにしておく必要があるな。
HTML にしたら不可視になるような感じがいいかもしれない。
```

That nailed down the conditions.

1. **The emit side (llive)** just produces hints without knowing the consumer
2. **The consumer side (llove TUI / llmesh visualizer / external agent)** may read them or ignore them
3. It must **absolutely never pollute** the existing human-facing output
4. The renderer **must not display it in HTML/Markdown**

### ☕ A small aside

I've been writing "it was a comment-out" up to here, but honestly, the first time I read that LinkedIn comment I froze for about three seconds. "Yeah, that's exactly the kind of thing that won't run unless you install everything…" When I ran the AST scan and it came back with 0 leaks, it felt like my past self had bailed me out. Design decisions sometimes turn out, in hindsight from the future, to have been correct.

## The design I adopted

I implemented the following minimal type in `src/llive/annotations.py`.

```python
@dataclass(frozen=True)
class Annotation:
    namespace: str          # "vrb" / "oka" / "cog" / "math" / "creat" / "core"
    key: str
    value: Any              # JSON-friendly (str/int/float/bool/None/list/dict)
    target_layer: str | None = None   # "llove" / "llmesh" / None=any
```

An `AnnotationBundle` that wraps these carries the bidirectional serializers `to_html_comments()` / `from_html_comments()`. Example output:

```
<!-- llive:core.brief_completed=true -->
<!-- llive:oka.essence_card={"summary": "..."} target=llove -->
<!-- llive:cog.consensus="proceed" -->
```

In Markdown renderers (GitHub / Qiita / Zenn / VS Code Preview) it's completely **invisible**. Yet call `AnnotationBundle.from_html_comments(text)` and the machine side can fully reconstruct the original structure.

## Why HTML comments?

There were other options.

| Option | Invisibility | Machine readability | Compatibility with existing tools |
|---|---|---|---|
| Separate JSON file | ◯ | ◯ | ✕ (managing 2 files) |
| YAML front matter | △ (shown by some renderers) | ◯ | △ |
| **HTML comments** | ◎ | ◎ | ◎ (Markdown standard) |
| Binary embedding | ◎ | △ | ✕ |
| zero-width Unicode | ◎ | △ | ✕ (disappears on copy-paste) |

The advantage of HTML comments is that they turn the very fact that **"Markdown passes HTML through"** to our benefit. By Markdown's historical spec, `<!-- ... -->` is emitted as HTML, and browsers / Markdown viewers don't display HTML comments. As a result, you can plant Annotations in **"every corner of the article you're reading right now"** and the reader won't notice.

(As a test, let's plant one at the end of this paragraph too.)
<!-- llive:meta.article_id="14_invisible_annotation_channel" target=llove -->

### ☕ By the way

The trick of planting HTML comments in Markdown has existed for ages in the Jekyll and Hugo communities under the name **"comment front matter."** What's new is the idea of placing machine-readable metadata at **arbitrary positions in the Markdown body**. Front matter is pinned to the top; this scatters it paragraph by paragraph.

## Natural emit in the llive implementation

Inside `BriefRunner.submit(brief)`, a set of Annotations is automatically emitted at the end of every Brief.

```python
emitter = AnnotationEmitter()
emitter.add("core", "brief_completed", value=True)
if essence is not None:
    emitter.add("oka", "essence_card",
                value={"summary": essence.essence_summary, "mystery": essence.mystery},
                target_layer="llove")
if perspective_summary is not None:
    emitter.add("cog", "consensus", value=perspective_summary.consensus_recommendation)
    if perspective_summary.risk_score >= 0.6:
        emitter.add("cog", "risk_alert",
                    value={"risk_score": perspective_summary.risk_score},
                    target_layer="llove")
if lint_report is not None and lint_report.findings:
    emitter.add("vrb", "lint_findings_count",
                value=len(lint_report.findings),
                target_layer="llove")
```

What matters here is that **nobody is doing `import llove`**. Even when llive runs on its own, these annotations simply remain as **unused hints**.

llove (a future TUI) can, by calling `AnnotationBundle.from_html_comments(brief_result.body)`, do things like highlight `cog.risk_alert` the moment it finds it. **llive is being kind to llove without ever knowing that llove exists.**

## Performance benchmark

I measured 1000 round-trips with `scripts/bench_annotations.py`.

| Operation | Latency |
|---|---|
| Build 1 item | 7.95 µs |
| Encode (HTML comments) per ann | 6.30 µs |
| Decode per ann | 12.40 µs |
| `for_layer()` over a 1000-item bundle | 0.13 ms / call |
| 1000-item round-trip OK | ✓ |

A typical BriefResult.annotations has 3 items, so the **encoded size is 141 bytes**. Plant 100 of them in a single Markdown page and it's still under 5 KB.

## What's the "elegance of the design"?

What's interesting about this mechanism is that it **satisfies three responsibilities with a single format.**

| Responsibility | The element that secures it |
|---|---|
| **Independence** (IND-01) | The emit side doesn't know the consumer; zero `import` relationships |
| **Combination value** (IND-02) | The consumer obtains multiple hints just by calling `from_html_comments()` |
| **Non-pollution of existing output** | HTML comments vanish completely in the renderer |

When you line up three products in OSS, the common failures are "binding too tightly with a protobuf schema, so changing one breaks all of them" and "wiring things through a DI container that turns out to be an implicit import." The classic approach of **planting comments inside plain text** straightforwardly solved a problem of modern multi-package OSS.

## Connection to traceability

Annotations are a separate lineage from ledger events such as `perspectives_observed` / `lint_findings_recorded` that get written to the `BriefLedger` (append-only JSONL).

| | Purpose | Persistence |
|---|---|---|
| **Ledger event** | Machine audit (SEC-03 hash chain), replayable | Persistent (JSONL) |
| **Annotation** | Hints for the consumer (UI render / coordination with another agent) | Volatile (a field of BriefResult) |

The two don't overlap. The ledger is **a past fact**; the annotation is **a suggestion to a future consumer**.

## Summary

- It started from a single LinkedIn comment and landed on the classic format `<!-- llive:ns.key=val -->`
- The independence audit machine-guaranteed 0 hard leaks across 172 files
- 6 ms to encode 1000 items, 141 bytes for a typical 3-item bundle = a non-intrusive footprint
- The emit side doesn't know the consumer, and the consumer side doesn't require an emit = a completely optional connector
- The existing Markdown/HTML output is **completely uncontaminated**

If you're wrestling with **"reconciling independence and combination value"** in an OSS multi-product setup, do give the HTML-comment-style annotation channel a try. The implementation fits in just over 200 lines.

---

**Repo**: https://github.com/furuse-kazufumi/llive (Apache-2.0 + Commercial dual-license)

**Implementation**: `src/llive/annotations.py`, `src/llive/brief/render.py`, `src/llive/brief/runner.py`

**Related past articles (series)**:
- [12] llive development history — from v0.1 to a v0.7 candidate in 5 days
- [13] Corpus-first strategy — supplementing the thinking flow with perspectives the AI doesn't notice

## References / referenced specs

- **CommonMark Spec** (the Markdown standard) — the basis for HTML comment passthrough
  https://spec.commonmark.org/
- **HTML Living Standard** (WHATWG) — `<!-- ... -->` syntax and renderer behavior
  https://html.spec.whatwg.org/multipage/syntax.html#comments
- **Front matter** (the YAML metadata format used by Jekyll and others) — compared as a rejected option
  https://jekyllrb.com/docs/front-matter/
- **llive repository** — the source of the implementation covered in this article
  https://github.com/furuse-kazufumi/llive

---

<!-- llive:meta.next_article="15_..." target=llove -->
<!-- llive:meta.published_date="2026-05-18" -->
<!-- llive:meta.tags=["llive","annotation","design","oss","independence"] target=any -->

---

# 中文

# 在 HTML 中不可见，机器却能读取。—— llive 采用的「不可见注释通道」设计

> 📚 **连载导航**：**#14 本文** ｜ #15 「第二大脑」开发论 → ｜ [连载 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 每篇文章都可单独阅读（链接仅供回游）。

**一句话引子**：
某天，社交网络上收到了这样一条评论：「如果三个产品相互依赖，那么只用其中一个的价值就减半了吧。」回复是一段**注释**——`<!-- llive:cog.consensus="proceed" -->`。

---

## 为什么写这篇文章

在 OSS 多产品构成中，每次都很难同时兼顾**「能够独立运行」与「组合起来价值能够累积」**。取前者就会变成「单独用终究不够味」，取后者就会变成「不全部装上就跑不起来」。

在 llive（`llive`——L 有 2 个。不是 3 个 L 的 `lllive`；过去曾因 tokenizer 问题出过事故）中，我们用一招解开了这个二律背反：**把注释封进 HTML 注释格式里**。本文分享这一设计的来龙去脉、实现与基准测试结果。

## 起点 —— 一条 LinkedIn 评论

```
llive の記憶層が llove の交互データに依存し、llove がまた llmesh の
接続能力に依存しているなら、その中の一つだけを使う価値は半減します。
理想的なのは、各層が独立して価値を提供でき、組み合わせることで効果が
積み上がる設計であり、全部揃えないと動かないという状況は避けるべきです。
```

收到这条评论后，我对 llive 的 `src/llive` 全部 172 个文件跑了一遍 AST 扫描（`scripts/audit_independence.py`）。结果是 **hard import leak 0 件**。llive 从一开始就没有对 llove/llmesh 的运行时依赖。

问题在下一阶段：「**那么，在保持独立性的同时，到底该怎么提升组合价值？**」

## 笔者的设计备忘 ——「准备一些注释不就好了吗」

于是笔者留下了这样一条设计备忘。

```
応答にアノテーションを用意すれば独立性を保ちながら組み合わせでの
効果も得られるのではないか
```

这成了被采用设计的原型。随后又进一步收紧了条件。

```
邪魔にならない程度のアノテーションにしておく必要があるな。
HTML にしたら不可視になるような感じがいいかもしれない。
```

至此条件就定下来了。

1. **emit 侧（llive）** 在不知道 consumer 的情况下只负责发出 hint
2. **consumer 侧（llove TUI / llmesh visualizer / 外部 agent）** 读不读都可以
3. **绝对不能弄脏** 既有的面向人类的输出
4. **HTML/Markdown 的 renderer 不显示它**

### ☕ 顺带闲聊

到这里我一直写着「原来是注释啊」，但其实第一次读到那条 LinkedIn 评论时，我僵了大约三秒。「不对，那不就是不全部装上就跑不起来的典型吗……」跑了 AST 扫描发现 0 件 leak 之后，感觉像是被过去的自己救了一把。设计上的判断，有时从未来回看才发现是正解。

## 采用的设计

我在 `src/llive/annotations.py` 中实现了如下的最小类型。

```python
@dataclass(frozen=True)
class Annotation:
    namespace: str          # "vrb" / "oka" / "cog" / "math" / "creat" / "core"
    key: str
    value: Any              # JSON-friendly (str/int/float/bool/None/list/dict)
    target_layer: str | None = None   # "llove" / "llmesh" / None=any
```

将其打包的 `AnnotationBundle` 拥有 `to_html_comments()` / `from_html_comments()` 双向序列化器。输出示例：

```
<!-- llive:core.brief_completed=true -->
<!-- llive:oka.essence_card={"summary": "..."} target=llove -->
<!-- llive:cog.consensus="proceed" -->
```

在 Markdown renderer（GitHub / Qiita / Zenn / VS Code Preview）中完全**不可见**。而只要调用 `AnnotationBundle.from_html_comments(text)`，机器侧就能完整还原出原始结构。

## 为什么是 HTML 注释

其实还有别的选项。

| 方案 | 不可见性 | 机器可读性 | 与既有工具的兼容性 |
|---|---|---|---|
| 独立 JSON 文件 | ◯ | ◯ | ✕（要管理 2 个文件） |
| YAML front matter | △（部分 renderer 会显示） | ◯ | △ |
| **HTML 注释** | ◎ | ◎ | ◎（Markdown 标准） |
| 二进制嵌入 | ◎ | △ | ✕ |
| zero-width Unicode | ◎ | △ | ✕（复制粘贴时会消失） |

HTML 注释的优点在于，它反过来利用了**「Markdown 会原样透传 HTML」这一事实**。按照 Markdown 的历史规范，`<!-- ... -->` 会被作为 HTML 输出，而浏览器 / Markdown viewer 不显示 HTML 注释。结果就是，即便你在**「此刻你正在阅读的这篇文章的每一个角落」**埋入 Annotation，读者也不会察觉。

（试着在这一段的结尾也埋一个看看。）
<!-- llive:meta.article_id="14_invisible_annotation_channel" target=llove -->

### ☕ 顺便一提

在 Markdown 里埋 HTML 注释这一招，在 Jekyll 和 Hugo 圈子里自古就有，被称作**「comment front matter」**。新的地方在于「把机器可读的元数据放到 **Markdown 正文的任意位置**」这一发想。front matter 固定在开头，而这种做法可以按段落散布。

## llive 实现中自然的 emit

在 `BriefRunner.submit(brief)` 内部，每次 Brief 结束时都会自动 emit 一组 Annotation。

```python
emitter = AnnotationEmitter()
emitter.add("core", "brief_completed", value=True)
if essence is not None:
    emitter.add("oka", "essence_card",
                value={"summary": essence.essence_summary, "mystery": essence.mystery},
                target_layer="llove")
if perspective_summary is not None:
    emitter.add("cog", "consensus", value=perspective_summary.consensus_recommendation)
    if perspective_summary.risk_score >= 0.6:
        emitter.add("cog", "risk_alert",
                    value={"risk_score": perspective_summary.risk_score},
                    target_layer="llove")
if lint_report is not None and lint_report.findings:
    emitter.add("vrb", "lint_findings_count",
                value=len(lint_report.findings),
                target_layer="llove")
```

这里重要的是**没有任何人在 `import llove`**。即便 llive 单独运行，这些 annotation 也只是作为**没被使用的 hint** 留在那里而已。

llove（未来的 TUI）通过调用 `AnnotationBundle.from_html_comments(brief_result.body)`，就能做到比如一旦发现 `cog.risk_alert` 就高亮显示之类的事。**llive 在完全不知道 llove 存在的情况下，对 llove 报以善意。**

## 性能基准

我用 `scripts/bench_annotations.py` 测了 1000 件 round-trip。

| 操作 | 延迟 |
|---|---|
| Build 1 件 | 7.95 µs |
| Encode（HTML comments）per ann | 6.30 µs |
| Decode per ann | 12.40 µs |
| 对 1000 件 bundle 调用 `for_layer()` | 0.13 ms / call |
| 1000 件 round-trip OK | ✓ |

典型的 BriefResult.annotations 是 3 件，所以 **encoded 尺寸 141 字节**。即使在一页 Markdown 里埋 100 个，也在 5 KB 以下。

## 何为「设计之妙」

这个机制有意思的地方在于，**用一种格式满足了三项职责**。

| 职责 | 担保它的要素 |
|---|---|
| **独立性**（IND-01） | emit 侧不知道 consumer，`import` 关系为零 |
| **组合价值**（IND-02） | consumer 只需调用 `from_html_comments()` 即可获取多个 hint |
| **既有输出不被弄脏** | HTML 注释在 renderer 中完全消失 |

在 OSS 里并排三个产品时，常见的失败是「用 protobuf schema 绑得太死，改一个全都坏」「以为是用 DI 容器配的线，结果成了隐式 import」。**在纯文本中埋入注释**这一古典做法，干净利落地解决了现代多包 OSS 的课题。

## 与可追溯性的衔接

Annotation 与写入 `BriefLedger`（append-only JSONL）的 `perspectives_observed` / `lint_findings_recorded` 等 ledger event 是不同的体系。

| | 用途 | 持久性 |
|---|---|---|
| **Ledger event** | 机器审计（SEC-03 hash chain）、可 replay | 持久（JSONL） |
| **Annotation** | 给 consumer 的 hint（UI render / 与别的 agent 联动） | 易失（BriefResult 的字段） |

两者并不重叠。ledger 是**过去的事实**，annotation 是**对未来 consumer 的示意**。

## 总结

- 始于一条 LinkedIn 评论，最终落地到 `<!-- llive:ns.key=val -->` 这一古典格式
- 独立性审计在 172 个文件中以机器方式保证 hard leak 0 件
- 1000 件 encode 6 ms，典型 3 件 bundle 141 字节 = 不碍事的 footprint
- emit 侧不知道 consumer，consumer 侧不要求 emit = 完全可选的 connector
- 既有的 Markdown/HTML 输出**完全不被污染**

如果你正为 OSS 多产品构成中「**独立性与组合价值的兼顾**」而烦恼，请务必试试 HTML 注释形式的 annotation channel。实现只要 200 行多一点就够了。

---

**Repo**：https://github.com/furuse-kazufumi/llive （Apache-2.0 + Commercial dual-license）

**实现**：`src/llive/annotations.py`, `src/llive/brief/render.py`, `src/llive/brief/runner.py`

**过去的相关文章（连载）**：
- [12] llive 开发履历 —— 5 天从 v0.1 到 v0.7 候选
- [13] 语料库先行战略 —— 为思考流补足 AI 没察觉的观点

## 参考文献 / 参考规范

- **CommonMark Spec**（Markdown 标准规范）—— HTML 注释 passthrough 的依据
  https://spec.commonmark.org/
- **HTML Living Standard**（WHATWG）—— `<!-- ... -->` 语法与 renderer 行为
  https://html.spec.whatwg.org/multipage/syntax.html#comments
- **Front matter**（Jekyll 等使用的 YAML metadata 格式）—— 作为不采用方案进行比较
  https://jekyllrb.com/docs/front-matter/
- **llive 仓库** —— 本文所涉实现的原典
  https://github.com/furuse-kazufumi/llive

---

<!-- llive:meta.next_article="15_..." target=llove -->
<!-- llive:meta.published_date="2026-05-18" -->
<!-- llive:meta.tags=["llive","annotation","design","oss","independence"] target=any -->

---

# 한국어

# HTML 에서는 보이지 않는데, 기계는 읽을 수 있다. — llive 가 채택한 「비가시 어노테이션 채널」 설계

> 📚 **연재 내비**: **#14 본 글** ｜ #15 「제2의 뇌」 개발론 → ｜ [연재 LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ 각 글은 단독으로도 읽을 수 있습니다(링크는 회유용).

**한 줄 훅**:
어느 날 SNS 에 이런 댓글이 도착했다. 「세 개의 프로덕트가 서로 의존하고 있다면, 하나만 쓰는 가치는 반감되겠죠.」 답변은 **주석**이었다 — `<!-- llive:cog.consensus="proceed" -->`.

---

## 왜 이 글을 쓰는가

OSS 멀티 프로덕트 구성에서는 매번 **「독립적으로 동작할 것」과 「조합해서 가치가 쌓일 것」**을 양립시키기가 어렵다. 전자를 택하면 「결국 단독으로는 아쉽다」가 되고, 후자를 택하면 「전부 넣지 않으면 망가진다」가 된다.

llive(`llive` — L 은 2 개. L 3 개인 `lllive` 가 아니다. tokenizer 문제로 과거에 사고가 있었다)에서는, 이 이율배반을 **어노테이션을 HTML 주석 형식에 가둔다**는 한 수로 풀었다. 본 글은 그 설계의 경위와 구현, 벤치 결과를 공유한다.

## 기점 — LinkedIn 댓글

```
llive の記憶層が llove の交互データに依存し、llove がまた llmesh の
接続能力に依存しているなら、その中の一つだけを使う価値は半減します。
理想的なのは、各層が独立して価値を提供でき、組み合わせることで効果が
積み上がる設計であり、全部揃えないと動かないという状況は避けるべきです。
```

이 댓글을 받고, llive 의 `src/llive` 전 172 파일에 대해 AST 스캔(`scripts/audit_independence.py`)을 돌렸다. 결과는 **hard import leak 0 건**. llive 는 llove/llmesh 에 대한 runtime 의존을 처음부터 갖고 있지 않았다.

문제는 다음 단계였다. 「**그럼 독립성을 유지한 채로, 어떻게 조합 가치를 늘릴 것인가**.」

## 필자의 설계 메모 — 「어노테이션을 준비하면 되지 않을까」

그래서 필자는 다음과 같은 설계 메모를 남겼다.

```
応答にアノテーションを用意すれば独立性を保ちながら組み合わせでの
効果も得られるのではないか
```

이것이 채택된 설계의 원형. 더 나아가 조건을 좁혔다.

```
邪魔にならない程度のアノテーションにしておく必要があるな。
HTML にしたら不可視になるような感じがいいかもしれない。
```

여기서 조건이 굳어졌다.

1. **emit 측(llive)** 은 consumer 를 모른 채 hint 만 낸다
2. **consumer 측(llove TUI / llmesh visualizer / 외부 agent)** 은 읽어도 무시해도 된다
3. 기존 Human-facing 출력을 **절대 더럽히지 않는다**
4. **HTML/Markdown 에서 renderer 가 표시하지 않는다**

### ☕ 잠깐 여담

여기까지 「주석이었습니다」라고 써 왔지만, 사실 처음 LinkedIn 댓글을 읽었을 때 3 초쯤 굳었다. 「아니 그거 전부 넣지 않으면 안 도는 거잖아 보통…」 하고. AST 스캔을 돌렸더니 0 건 leak 이었기에, 과거의 나에게 구원받은 셈이 되었다. 설계 판단은 가끔, 미래에서 보면 정답이 된다.

## 채택한 설계

`src/llive/annotations.py` 에 다음의 최소 타입을 구현했다.

```python
@dataclass(frozen=True)
class Annotation:
    namespace: str          # "vrb" / "oka" / "cog" / "math" / "creat" / "core"
    key: str
    value: Any              # JSON-friendly (str/int/float/bool/None/list/dict)
    target_layer: str | None = None   # "llove" / "llmesh" / None=any
```

이를 묶는 `AnnotationBundle` 이 `to_html_comments()` / `from_html_comments()` 양방향 직렬화기를 가진다. 출력 예:

```
<!-- llive:core.brief_completed=true -->
<!-- llive:oka.essence_card={"summary": "..."} target=llove -->
<!-- llive:cog.consensus="proceed" -->
```

Markdown renderer(GitHub / Qiita / Zenn / VS Code Preview)에서는 완전히 **비가시**. 한편으로 `AnnotationBundle.from_html_comments(text)` 를 호출하면, 기계 측은 원래 구조를 완전히 복원할 수 있다.

## 왜 HTML 주석인가

선택지는 다른 것도 있었다.

| 안 | 비가시성 | 기계 가독성 | 기존 도구 호환 |
|---|---|---|---|
| JSON 별도 파일 | ◯ | ◯ | ✕ (2 파일 관리) |
| YAML front matter | △ (일부 renderer 에서 표시) | ◯ | △ |
| **HTML 주석** | ◎ | ◎ | ◎ (Markdown 표준) |
| 바이너리 임베드 | ◎ | △ | ✕ |
| zero-width Unicode | ◎ | △ | ✕ (copy-paste 로 사라짐) |

HTML 주석의 이점은 **「Markdown 이 HTML 을 passthrough 한다는 사실」**을 역이용한 점. Markdown 의 역사적 사양에서 `<!-- ... -->` 는 HTML 로 출력되고, 브라우저 / Markdown viewer 는 HTML 주석을 표시하지 않는다. 결과적으로 **「지금 당신이 보고 있는 글의 구석구석」**에 Annotation 을 심어도, 독자는 알아채지 못한다.

(시험 삼아, 이 문단 끝에도 하나 심어 보자.)
<!-- llive:meta.article_id="14_invisible_annotation_channel" target=llove -->

### ☕ 참고로

HTML 주석을 Markdown 에 심는 기법은, Jekyll 이나 Hugo 계열에서 **「comment front matter」**라 불리며 예전부터 있었다. 새로운 것은 **「Markdown 본문의 임의 위치」**에 기계 가독 메타데이터를 두는 발상 쪽. front matter 는 첫머리 고정, 이쪽은 문단 단위로 흩뿌릴 수 있다.

## llive 구현에서의 자연스러운 emit

`BriefRunner.submit(brief)` 안에서, 매 Brief 종료 시 Annotation 군이 자동으로 emit 된다.

```python
emitter = AnnotationEmitter()
emitter.add("core", "brief_completed", value=True)
if essence is not None:
    emitter.add("oka", "essence_card",
                value={"summary": essence.essence_summary, "mystery": essence.mystery},
                target_layer="llove")
if perspective_summary is not None:
    emitter.add("cog", "consensus", value=perspective_summary.consensus_recommendation)
    if perspective_summary.risk_score >= 0.6:
        emitter.add("cog", "risk_alert",
                    value={"risk_score": perspective_summary.risk_score},
                    target_layer="llove")
if lint_report is not None and lint_report.findings:
    emitter.add("vrb", "lint_findings_count",
                value=len(lint_report.findings),
                target_layer="llove")
```

여기서 중요한 것은 **누구도 `import llove` 하지 않는다**는 점. llive 가 단독으로 동작할 때도, 이 annotation 들은 그저 **사용되지 않는 hint** 로 남을 뿐이다.

llove(미래의 TUI)는 `AnnotationBundle.from_html_comments(brief_result.body)` 를 호출함으로써, `cog.risk_alert` 를 발견하는 즉시 하이라이트 표시하는 것과 같은 일을 할 수 있다. **llive 는 llove 의 존재를 모른 채, llove 에게 친절을 베푼다.**

## 성능 벤치

`scripts/bench_annotations.py` 로 1000 건 round-trip 을 측정했다.

| 조작 | 레이턴시 |
|---|---|
| Build 1 건 | 7.95 µs |
| Encode (HTML comments) per ann | 6.30 µs |
| Decode per ann | 12.40 µs |
| 1000 건 bundle 에 `for_layer()` | 0.13 ms / call |
| 1000 건 round-trip OK | ✓ |

전형적인 BriefResult.annotations 는 3 건이므로 **encoded 사이즈 141 바이트**. Markdown 1 페이지에 100 개를 심어도 5 KB 이하.

## 무엇이 「설계의 묘」인가

이 구조가 흥미로운 점은, **세 가지 책무를 하나의 포맷으로 충족시켰다**는 데 있다.

| 책무 | 담보하는 요소 |
|---|---|
| **독립성** (IND-01) | emit 측은 consumer 를 모르고, `import` 관계 제로 |
| **조합 가치** (IND-02) | consumer 가 `from_html_comments()` 를 호출하기만 하면 여러 hint 를 취득 |
| **기존 출력의 비오염** | HTML 주석은 renderer 에서 완전히 사라진다 |

OSS 에서 세 개의 프로덕트를 늘어놓을 때 흔한 실패가 「protobuf 스키마로 너무 강하게 bind 해서 하나 바꾸면 전부 망가진다」 「DI 컨테이너로 배선했다고 생각했는데 암묵적 import 가 되어 있다」이다. **플레인 텍스트 안에 주석을 심는다**는 고전적 접근이, 현대적 multi-package OSS 의 과제를 깔끔하게 풀었다.

## 추적 가능성과의 접속

Annotation 은 `BriefLedger`(append-only JSONL)에 기록되는 `perspectives_observed` / `lint_findings_recorded` 같은 ledger event 와는 별개의 계통이다.

| | 용도 | 영속성 |
|---|---|---|
| **Ledger event** | 기계 감사(SEC-03 hash chain), replay 가능 | 영속(JSONL) |
| **Annotation** | consumer 를 향한 hint(UI render / 다른 agent 연계) | 휘발(BriefResult 의 필드) |

둘은 중복되지 않는다. ledger 는 **과거의 사실**, annotation 은 **미래의 consumer 를 향한 시사**.

## 정리

- LinkedIn 의 댓글 한 통에서 시작해, `<!-- llive:ns.key=val -->` 라는 고전 포맷에 착지했다
- 독립성 감사로 172 파일 중 hard leak 0 건을 기계 보증
- 1000 건 encode 6 ms, 전형 3 건 bundle 141 바이트 = 거슬리지 않는 footprint
- emit 측은 consumer 를 모르고, consumer 측은 emit 을 요구하지 않는다 = 완전히 optional 한 connector
- 기존 Markdown/HTML 출력은 **완전히 오염되지 않는다**

OSS 멀티 프로덕트 구성에서 「**독립성과 조합 가치의 양립**」에 고민하는 분은, 꼭 HTML 주석 형식의 annotation channel 을 시험해 보길 바란다. 구현은 200 줄 남짓이면 끝난다.

---

**Repo**: https://github.com/furuse-kazufumi/llive (Apache-2.0 + Commercial dual-license)

**구현**: `src/llive/annotations.py`, `src/llive/brief/render.py`, `src/llive/brief/runner.py`

**과거의 관련 글(연재)**:
- [12] llive 개발 이력 — 5 일 만에 v0.1 에서 v0.7 후보로
- [13] 코퍼스 선행 전략 — AI 가 알아채지 못하는 관점을 사고 흐름에 보완

## 참고 문헌 / 참고 사양

- **CommonMark Spec**(Markdown 표준 사양) — HTML 주석 passthrough 의 근거
  https://spec.commonmark.org/
- **HTML Living Standard**(WHATWG) — `<!-- ... -->` 구문과 renderer 동작
  https://html.spec.whatwg.org/multipage/syntax.html#comments
- **Front matter**(Jekyll 등에서 이용되는 YAML metadata 형식) — 미채택안으로 비교
  https://jekyllrb.com/docs/front-matter/
- **llive 리포지토리** — 본 글에서 다룬 구현의 원전
  https://github.com/furuse-kazufumi/llive

---

<!-- llive:meta.next_article="15_..." target=llove -->
<!-- llive:meta.published_date="2026-05-18" -->
<!-- llive:meta.tags=["llive","annotation","design","oss","independence"] target=any -->
