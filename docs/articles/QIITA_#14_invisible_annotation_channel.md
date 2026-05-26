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
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

# HTML で見えないのに、機械では読める。— llive が採用した「不可視アノテーションチャネル」設計

> 📚 **連載ナビ**: **#14 本記事** ｜ #15 「第二の脳」開発論 → ｜ [連載 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 各記事は単独でも読めます（リンクは回遊用）。

**1 行 hook**:
ある日、SNS にこんなコメントが届いた。「3 つのプロダクトが相互依存していたら、1 つだけ使う価値が半減するよね」。返答は **コメントアウト** だった — `<!-- llive:cog.consensus="proceed" -->`。

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
