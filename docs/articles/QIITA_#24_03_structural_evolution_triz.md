---
title: llive 完全解説 (3) — 「矛盾は計算できる」: 構造進化 × TRIZ 40 原理 × Z3 検証
tags:
  - FullSense
  - llive
  - 解説
private: false
updated_at: '2026-05-22'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---
<!-- lead-trans-placed -->
<!-- h2-trans-placed -->

<!-- trilingual-subtitle-placed -->
<small><strong>EN:</strong> “Contradictions are computable”: TRIZ 40 principles × ChangeOp × Z3 verifier / <strong>中:</strong> "矛盾可以计算": TRIZ 40 原理 × ChangeOp × Z3 验证器</small>
<!-- section-separators-placed -->

# llive 完全解説 (3) — 「矛盾は計算できる」: 構造進化 × TRIZ 40 原理 × Z3 検証

![hero — TRIZ mutation then Z3 verify](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_03_hero.svg)

<!-- progress-svg-placed -->
![連載進捗 (3/8) — 現在: TRIZ](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_03_progress.svg)

> **コンセプト hook**: TRIZ (発明問題解決理論) は普通「人が紙に書くアイデア
> 出しテク」として知られる. llive は **TRIZ 40 原理を形式記号として組み込み**,
> 構造 mutation の policy として走らせる. しかも mutation で生まれた新構造は
> **Z3 で形式検証** を通ってから集団に入る. 「発想 → 検証」のループが
> 1 つのプログラムに収まる. — 「**矛盾は計算できる**」.
> 
> 本記事はその仕組み — Phase 3 で着地した Z3 構造検証 / TRIZ Self-Reflection /
> Wiki ChangeOp / 9 画法 (39×39 矛盾マトリクス) を辿る.

>
## 0. 連載中での位置づけ
<small><strong>EN:</strong> 0. Position within the series / <strong>中:</strong> 0. 在系列中的定位</small>

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
<small><strong>EN:</strong> This chapter is 'search that rewrites the individual's internal structure itself' — i.e., LoRA / Adapter / the 4-layer memory itself. / <strong>中:</strong> 本章是 "重写个体内部结构本身的搜索" — 即 LoRA / Adapter / 4 层记忆本身.</small>
メモリの sub-block 順列 を mutation する層.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

<!-- theme-svg-placed -->
![theme — TRIZ 40 原理 grid + 矛盾マトリクス flicker (animated)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_03_theme.svg)

## 1. なぜ TRIZ か
<small><strong>EN:</strong> 1. Why TRIZ? / <strong>中:</strong> 1. 为什么选 TRIZ</small>

LLM の自己進化 (self-evolution) で問題なのは「**変えるべき部分**」をどう選ぶか.
<small><strong>EN:</strong> In LLM self-evolution the hard problem is choosing WHICH part to change. TRIZ provides a structured catalogue for that decision. / <strong>中:</strong> 在 LLM 的自我进化中, 难点是选择 "该改哪一部分". TRIZ 为该决策提供了结构化的目录.</small>
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

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 2. llive での具体実装
<small><strong>EN:</strong> 2. Concrete implementation in llive / <strong>中:</strong> 2. 在 llive 中的具体实现</small>

### 2.1 TRIZ Self-Reflection (Phase 3)

llive は構造 mutation の **候補生成段階** で TRIZ self-reflection module を呼ぶ:
<small><strong>EN:</strong> llive calls the TRIZ self-reflection module during the candidate-generation stage of structural mutation. / <strong>中:</strong> llive 在结构 mutation 的候选生成阶段调用 TRIZ self-reflection module.</small>

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

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 3. honest disclosure — 落とし穴
<small><strong>EN:</strong> 3. Honest disclosure - pitfalls / <strong>中:</strong> 3. 诚实披露 - 陷阱</small>

「TRIZ で全部解ける!」は嘘. honest disclosure として:
<small><strong>EN:</strong> 'TRIZ solves everything' is a lie. Honest disclosure follows. / <strong>中:</strong> "TRIZ 能解决一切" 是谎言. 下面是诚实披露.</small>

- **39×39 matrix は時代依存** — Altshuller が 1971 年に確定. 現代の AI 系の
  矛盾 (例: `推論精度 vs バッテリ消費`) は完全には収まらない. llive は
  矛盾の追加列を独自に持つ (実機 metrics ベース).
- **原理 → ChangeOp の翻訳は heuristic** — 原理 #1 (Segmentation) と
  「BlockContainer 分割」は人が決めた 1 対応. これは LLM 自身が広げる余地あり.
- **Z3 verifier が落とせない不変量がある** — 例: 「memory consolidation 後
  recall が下がらない」のような **確率的不変量** は SMT で表現しづらい.
  これは別の verifier (経験的 reservoir test) で見る.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 4. 数字で見る
<small><strong>EN:</strong> 4. By the numbers / <strong>中:</strong> 4. 用数字看</small>

| 指標 | 値 |
|---|---|
| llive Phase 3 着地 | 2026-05-14 (v0.3.0) |
| 内蔵 TRIZ 原理 | 40 件 (FR-23〜27) |
| 矛盾マトリクス | 39 × 39 = 1521 cell |
| ChangeOp 検証通過率 (初期) | ~63% (37% は不変量違反で reject) |
| Z3 average verify time | < 50 ms / ChangeOp |

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 5. 「発想 → 検証」 ループの構造的意義
<small><strong>EN:</strong> 5. Structural significance of the ideate-to-verify loop / <strong>中:</strong> 5. 构想 -> 验证 循环的结构意义</small>

これは TRIZ の哲学 + 形式検証の哲学を結ぶ:
<small><strong>EN:</strong> This connects TRIZ philosophy with formal-verification philosophy. / <strong>中:</strong> 这把 TRIZ 哲学与形式验证哲学连了起来.</small>

- TRIZ: **「面白い発想ではなく原理から導かれる発想」** を求める. 体系的.
- 形式検証: **「想像力で書かれた変更を機械的に妥当性チェック」**. 機械的.

両者は人と機械の協働の典型. llive はそれを **同一 module 内** で回す.

> **未来予測**: AI が自己進化するとき, **「発想は機械的, 検証も機械的」**
> な閉ループを持つことが必須. llive はその雛形を 1 OSS に同居させた最小例.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 6. 次に来るもの
<small><strong>EN:</strong> 6. What comes next / <strong>中:</strong> 6. 接下来要做的</small>

- **#24-04** で「速い小脳側」 — B-series の収束を見る.
- **#24-05** で「遅い大脳側」 — EvolutionLoop の探索. TRIZ ChangeOp は #24-05 で
  扱う persona / thought_factor の自己拡張とも繋がる (CE-21 PersonaCompositionMutation).
<small><strong>EN:</strong> Also wires into the self-extension of personas / thought factors (CE-21 PersonaCompositionMutation). / <strong>中:</strong> 也与 persona / thought_factor 的自我扩展 (CE-21 PersonaCompositionMutation) 相连.</small>

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 7. 2026-05-22 追記 — TRIZ 的アプローチが Rust 高速化判定にも効く
<small><strong>EN:</strong> 7. 2026-05-22 addendum - TRIZ-style approach also works for Rust speedup decisions / <strong>中:</strong> 7. 2026-05-22 追记 - TRIZ 方法对 Rust 加速判定同样有效</small>

本記事の TRIZ は「**矛盾 (improving X / worsening Y) を 39×39 マトリクスで
<small><strong>EN:</strong> This chapter's TRIZ is 'taking improving X / worsening Y contradictions and looking them up in a 39×39 matrix'. / <strong>中:</strong> 本章的 TRIZ 是 "把改善 X / 恶化 Y 的矛盾在 39×39 矩阵中查表".</small>
構造化解決する**」という方法論だが, 同じ思想が **エンジニアリング判断全般**
に応用できる. 同日 (2026-05-22) 着地した llive Rust 高速化判定で具体例:

「**Rust 化 = 速い vs Python = 遅い**」の単一軸対立 (= TRIZ で言う矛盾) を
**Python 経路の特性別 5 パターン** (#24-05 §13.3) に分解した. 結果:

- 純 Python ループ 1-pair → 単発 FAIL, batch 必須 (RUST-15)
- numpy 小 N の API 多用 → **単発でも x66** (RUST-16)
- numpy 中規模 BLAS → **境界線上, rayon で挽回** (RUST-17 → 17b)

これは TRIZ 矛盾マトリクスの **構造的解決** と同型 — 「**矛盾の原因を
パラメータ空間で分解 → 原理に対応させる**」. 39×39 を **6 (Python 経路) ×
3 (Rust 化戦略: 単発 / batch / 並列+algorithmic)** の小さな表に縮めた版.

詳細: `docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md` の
**5 パターン判定表**. これは TRIZ の発想を **AI / HPC 工学** に転用した実例.

---

> draft (10x volume フル版は次セッション). 骨子 + 7 main section + 数字裏付け
> + honest disclosure 3 件 + TRIZ 方法論の Rust 化判定への転用 (2026-05-22 追記).

---

## Series Navigation

- ← 前: [llive 完全解説 (2) 「10 軸で考える AI」](https://qiita.com/furuse-kazufumi/private/bdfad6db3f2e70c40511)
- → 次: [llive 完全解説 (4) 「収束する脳」](https://qiita.com/furuse-kazufumi/private/e5093e4816b25c1bd4d0)
- 全体: [llive 完全解説 (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
