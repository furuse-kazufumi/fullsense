# Alu 挿絵 埋込デモ（スナックバス江 × AI 記事テーマ）

> 試作: 2026-06-15。Alu（[alu.jp](https://alu.jp/)）= 出版社公認のマンガ「コマ」共有/埋込サービス。
> 『スナックバス江』（**フォビドゥン澁川** / 集英社、© alu inc.）のコマを **crop permalink で合法に**記事挿絵化する。
> ルール: **必ず crop permalink（oEmbed）で貼る。Fastly の `.jpg` 直リンク・再ホストはしない**（[[reference_alu_manga_crops]]）。

---

## 先に結論：どこで「絵」が出るか

Alu の埋込は **oEmbed**（URL を 1 行で貼ると自動でカード展開）。公式対応は **note / WordPress / はてなブログ / Ameba**。
**Qiita / Zenn は Alu を oEmbed allowlist に持たない**（＝コマ画像は出ない）。
→ **方針確定（2026-06-15）**: 「絵を出したい」記事は **note / はてな**。**Qiita は出典付きリンクで割り切る**（埋込展開は狙わない）。

| プラットフォーム | crop URL を貼ると | 方法 |
|---|---|---|
| note | コマ画像が展開 ✓ | URL を 1 行で貼る（oEmbed） |
| WordPress | コマ画像が展開 ✓ | URL 貼付 or 公式 HTML |
| はてなブログ | コマ画像が展開 ✓ | URL → 「埋め込み」選択 |
| Ameba | コマ画像が展開 ✓ | HTML 表示で公式コード貼付 |
| Qiita | リンクのみ（**出典付きで割り切る＝確定**） | 出典付きリンク |
| Zenn | リンクのみ | 出典付きリンク |
| GitHub README | リンクのみ | — |

---

## 使い方＝「閑話休題」程度（箸休め）

**主役の挿絵ではなく、軽い箸休め。** 重い節の合間に**たまに**1コマ挟んで集中を回復させる休憩ポイント（[[feedback_article_break_points]] / [[feedback_reader_attention_curve]]）。各概念に毎回は貼らない（入れすぎるとネタが安くなる）。リード文に「閑話休題。」を添えて“脱線→本筋復帰”を明示する。

下の 4 例は**候補ストック**。実記事では本筋の流れを見て、このうち 1〜2 個を箸休めとして差すイメージ。

---

## デモ 1 — AI と人間の対話ズレ（AI communication）

> 本文例（箸休めの差し込みイメージ）: 「——と、ここまで設計の話が続いた。**閑話休題**。LLM と話が噛み合わないのは知能差じゃなく“見ている世界”のズレ、と言われて私はこのコマを思い出す。……さて本筋に戻ろう——」

**埋込（note / はてな / WordPress 用・この URL を 1 行で貼る）:**

https://alu.jp/series/スナックバス江/crop/PJm0yAGeJy9iSa487mrX

**Qiita 標準（出典付きリンク・確定方針）:**

> 🗨️ 「IQに差がある者とは会話が噛み合わない…という事は…?」
> — [スナックバス江／フォビドゥン澁川（アル）](https://alu.jp/series/スナックバス江/crop/PJm0yAGeJy9iSa487mrX)

---

## デモ 2 — かみくだき説明の前提ミスマッチ（説明・UX）

> 本文例: 「初学者向けに“かみくだく”比喩は、相手の世界に無い喩えを使うと逆効果。LLM への指示も同じで、**相手が持っていない前提で例えない**——」

**埋込用 URL:**

https://alu.jp/series/スナックバス江/crop/vZiE4UJF8WUuZFhyUfEk

**Qiita 標準（出典付きリンク）:**

> 🗨️ 「貴方の世界にある筈もない例えでかみ砕きなさるな!」
> — [スナックバス江／フォビドゥン澁川（アル）](https://alu.jp/series/スナックバス江/crop/vZiE4UJF8WUuZFhyUfEk)

---

## デモ 3 — ベンチの honest disclosure（数字で取り繕う戒め）

> 本文例: 「“なんか凄そうなグラフ”は悲壮感を薄めるが、**内訳を疑え**。異常に良い結果ほど、勝った気になる前に分解する（[[feedback_benchmark_honest_disclosure]]）——」

**埋込用 URL:**

https://alu.jp/series/スナックバス江/crop/UfjgydbJNoh5HDTItAlf

**Qiita 標準（出典付きリンク）:**

> 🗨️ 「クソ! 謎のグラフのおかげで悲壮感が薄いぜ!!」
> — [スナックバス江／フォビドゥン澁川（アル）](https://alu.jp/series/スナックバス江/crop/UfjgydbJNoh5HDTItAlf)

---

## デモ 4 — 評価方式：減点 vs 加点（スコアリング章扉）

> 本文例: 「満点から引く“減点法”か、0 点から足す“加点方式”か。AI 評価も**どちらの土俵に乗るかで結論が変わる**——」

**埋込用 URL:**

https://alu.jp/series/スナックバス江/crop/llQmydCCdUnqFoOusBCk

**Qiita 標準（出典付きリンク）:**

> 🗨️ 「減点法って事は満点からのスタート…つまり加点方式では0点のワイにもチャンスがある…?」
> — [スナックバス江／フォビドゥン澁川（アル）](https://alu.jp/series/スナックバス江/crop/llQmydCCdUnqFoOusBCk)

---

## コンプライアンス・メモ

- 上の **crop permalink は全て実機 200 確認済**（2026-06-15, WebFetch）。著者=フォビドゥン澁川、出典=スナックバス江、© alu inc.。
- **画像は Alu が配信**（oEmbed 経由）。当方リポ/Qiita に `.jpg` を**再ホストしない**。Fastly CDN の `cropped_images/...jpg` を直 `![]()` で貼るのも**不可**（Alu 公認ルート＝oEmbed/permalink のみ）。
- キャプションは OCR ベースで誤字混入あり。**本文に台詞を引用する時は埋込コマの実画像で原文確認**。
- 既存 `docs/articles/assets/bazue_all/*.jpg`（生画像）は再配布リスク → 公開時は Alu 埋込へ寄せるのが綺麗（任意）。
