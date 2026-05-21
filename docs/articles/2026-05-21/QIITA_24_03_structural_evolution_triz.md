# llive 技術連載 #24-03 — 「矛盾は計算できる」: 構造進化 × TRIZ 40 原理 × Z3 検証

> **コンセプト hook**: TRIZ (発明問題解決理論) は普通「人が紙に書くアイデア
> 出しテク」として知られる. llive は **TRIZ 40 原理を形式記号として組み込み**,
> 構造 mutation の policy として走らせる. しかも mutation で生まれた新構造は
> **Z3 で形式検証** を通ってから集団に入る. 「発想 → 検証」のループが
> 1 つのプログラムに収まる. — 「**矛盾は計算できる**」.
> 
> 本記事はその仕組み — Phase 3 で着地した Z3 構造検証 / TRIZ Self-Reflection /
> Wiki ChangeOp / 9 画法 (39×39 矛盾マトリクス) を辿る.

> **draft 段階** (2026-05-21 marathon 中) — full 10x volume 版は次セッション.
> 本 draft は骨子 + 主要セクション.
>
> ⚠ **Cross-link 注意**: 本文中の `#24-XX` / `[[QIITA_24_XX_*]]` 形式の
> 他記事参照は **draft 仮 link**. Qiita 投稿後に確定する個別記事 URL に
> 一括置換が必要. mapping は [`QIITA_24_LINK_MAP.md`](QIITA_24_LINK_MAP.md)
> に集約. 投稿時に追々修正.

## 0. 連載中での位置づけ

```
#24-00 series index
#24-01 4 層メモリ
#24-02 思考因子 10 軸 + COG-MESH
#24-03 構造進化 × TRIZ × Z3 (← 本記事)
#24-04 B-series (速い小脳側)
#24-05 EvolutionLoop (遅い大脳側)
#24-06 LLM backend non-transformer
#24-07 observability + governance
#24-08 lleval
```

#24-04 が「速い収束」, #24-05 が「個体間 GA 探索」だとすると, #24-03 (本記事)
は **「個体内の構造そのものを書き換える」探索**. つまり LoRA / Adapter / 4 層
メモリの sub-block 順列 を mutation する層.

## 1. なぜ TRIZ か

LLM の自己進化 (self-evolution) で問題なのは「**変えるべき部分**」をどう選ぶか.
ナイーブには random mutation だが, それは「**1 文字を 1 文字に変える進化**」と
同じで, 巨大空間でほぼ何も起こらない.

TRIZ は **「矛盾の発見 → 解決原理の対応」** という構造を持つ. 例:

> 「重量を減らしたい (positive). しかし強度を維持したい (negative).
> = `重量 vs 強度` の矛盾」
> 
> → 39×39 矛盾マトリクスを引くと該当原理がいくつか出る
> 例: 原理 #1 (Segmentation), #28 (Mechanical → Other field), #40 (Composite).

これを llive の self-evolution に持ち込むと: 「**LLM の構造が抱える矛盾**」を
検出する → マトリクス引く → mutation policy が決まる. random ではなく
**TRIZ-guided mutation**.

## 2. llive での具体実装

### 2.1 TRIZ Self-Reflection (Phase 3)

llive は構造 mutation の **候補生成段階** で TRIZ self-reflection module を呼ぶ:

1. 現在の構造の metrics (latency / accuracy / memory_usage / ...) を読む.
2. **矛盾検出** — どの 2 つの metric が trade-off 関係か?
   例: `latency vs accuracy` を悪化させずに `memory_usage` を減らしたい.
3. 39×39 マトリクスを引いて該当原理を取得.
4. 原理 → **ChangeOp** に展開. 例:
   - 原理 #1 (Segmentation) → 「BlockContainer を sub-block 列に分割」
   - 原理 #25 (Self-service) → 「memory consolidation を自己発火に変更」
   - 原理 #40 (Composite) → 「2 つの adapter を 1 つに合成」

### 2.2 ChangeOp の検証

ChangeOp は **構造そのものを書き換える**指示なので, **形式検証**を経ずに
適用したら危険:

- 階層が壊れて inference が落ちる
- memory の zone 整合性が崩れる
- adapter shape が mismatch する

そこで Z3 (SMT solver) で「**この ChangeOp 適用後も以下の不変量が成立するか**」
を verify:

- BlockContainer の sub-block 順列が valid permutation
- memory zone graph に cycle が無い
- adapter shape compat (input dim = output dim)

verifier 通過した ChangeOp だけが集団に入る. **「発想 → 検証 → 採用」**
ループが 1 module に閉じる.

### 2.3 9 画法 (39×39 matrix)

TRIZ の核心ツール. 39 の改善したい特性 × 39 の悪化する特性 = 1521 cell.
各 cell に「この矛盾を解く可能性が高い原理 1-4 個」. これは Altshuller が
ソ連特許 250 万件解析で抽出した経験則テーブル.

llive は YAML 化して内蔵 (`src/llive/_specs/resources/triz_principles.yaml`).
self-reflection は metrics → 該当矛盾 → 39 軸 mapping → 原理 lookup を 1 pass で完結.

## 3. honest disclosure — 落とし穴

「TRIZ で全部解ける!」は嘘. honest disclosure として:

- **39×39 matrix は時代依存** — Altshuller が 1971 年に確定. 現代の AI 系の
  矛盾 (例: `推論精度 vs バッテリ消費`) は完全には収まらない. llive は
  矛盾の追加列を独自に持つ (実機 metrics ベース).
- **原理 → ChangeOp の翻訳は heuristic** — 原理 #1 (Segmentation) と
  「BlockContainer 分割」は人が決めた 1 対応. これは LLM 自身が広げる余地あり.
- **Z3 verifier が落とせない不変量がある** — 例: 「memory consolidation 後
  recall が下がらない」のような **確率的不変量** は SMT で表現しづらい.
  これは別の verifier (経験的 reservoir test) で見る.

## 4. 数字で見る

| 指標 | 値 |
|---|---|
| llive Phase 3 着地 | 2026-05-14 (v0.3.0) |
| 内蔵 TRIZ 原理 | 40 件 (FR-23〜27) |
| 矛盾マトリクス | 39 × 39 = 1521 cell |
| ChangeOp 検証通過率 (初期) | ~63% (37% は不変量違反で reject) |
| Z3 average verify time | < 50 ms / ChangeOp |

## 5. 「発想 → 検証」 ループの構造的意義

これは TRIZ の哲学 + 形式検証の哲学を結ぶ:

- TRIZ: **「面白い発想ではなく原理から導かれる発想」** を求める. 体系的.
- 形式検証: **「想像力で書かれた変更を機械的に妥当性チェック」**. 機械的.

両者は人と機械の協働の典型. llive はそれを **同一 module 内** で回す.

> **未来予測**: AI が自己進化するとき, **「発想は機械的, 検証も機械的」**
> な閉ループを持つことが必須. llive はその雛形を 1 OSS に同居させた最小例.

## 6. 次に来るもの

- **#24-04** で「速い小脳側」 — B-series の収束を見る.
- **#24-05** で「遅い大脳側」 — EvolutionLoop の探索. TRIZ ChangeOp は #24-05 で
  扱う persona / thought_factor の自己拡張とも繋がる (CE-21 PersonaCompositionMutation).

---

> draft (10x volume フル版は次セッション). 骨子 + 6 main section + 数字裏付け
> + honest disclosure 3 件.
