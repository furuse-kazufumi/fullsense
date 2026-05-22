---
title: llive 完全解説 (8) — 「眼鏡を作る」: lleval — honest disclosure 5+1 因子分解で AI を評価する
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

# llive 完全解説 (8) — 「眼鏡を作る」: lleval — honest disclosure 5+1 因子分解で AI を評価する

![hero — lleval 5+1 honest-disclosure radar across iterations](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_08_hero.svg)

<!-- progress-svg-placed -->
![連載進捗 (8/8) — 現在: lleval](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_08_progress.svg)

> **コンセプト hook**: AI を作るだけでは足りない. **AI を見る眼鏡** が要る.
> lleval は llive と並走する **evaluation framework** で, 「LLM が異常に
> 良い結果を出したら必ず内訳を疑う」という `feedback_benchmark_honest_disclosure` (内部参照)
> ルールを **コードの一級概念** に昇格させた. progressive size matrix で
> stress curve を取り, judge rotation で position bias を消す.
> 
> 結論を先に出すと: **「速い AI」ではなく「速いと思い込ませる構成」** を見抜く
> 道具.

> **draft 段階** (2026-05-21 marathon). full 10x volume 版は次セッション.
>
> ⚠ **Cross-link 注意**: 本文中の `#24-XX` / ``QIITA_#24_XX_*` (内部参照)` 形式の
> 他記事参照は **draft 仮 link**. Qiita 投稿後に確定する個別記事 URL に
> 一括置換が必要. mapping は [`QIITA_#24_LINK_MAP.md`](QIITA_#24_LINK_MAP.md)
> に集約. 投稿時に追々修正.

## 0. 連載中での位置づけ

```
#24-00 series index
#24-01 4 層メモリ
#24-02 思考因子 × COG-MESH
#24-03 構造進化 × TRIZ × Z3
#24-04 B-series
#24-05 EvolutionLoop
#24-06 LLM backend non-transformer
#24-07 observability + governance
#24-08 lleval — eval framework (← 本記事)
```

#24-07 が「**何を残すか**」(audit) だとすると, 本記事は「**何を測るか**」.
測定なしに改善はない.

## 1. lleval の出自 — honest disclosure 事件

事の発端は 2026-05-17 の benchmark. llive が他社 LLM API より **異常に速く**
出た数字があった. 普通なら勝った気になるところを, ユーザーは「**内訳を
疑え**」と指示. 蓋を開けると:

- **LLMBackend が attach されていなかった** (mock で動いていた)
- **chars 指標が不公平** (英語 token を文字数換算)
- **subprocess RTT を除外** (起動コストを無視)

3 つの artifact が複合していた. これを記録 (`feedback_benchmark_honest_disclosure` (内部参照))
してから, 「ベンチで異常結果が出たら必ず 5 つの artifact を疑う」を
**外部化** したくなった. それが lleval.

## 2. 5+1 因子分解 — honest disclosure の構造化

lleval `HonestDisclosureAnalyzer` (2026-05-21 朝着地) は出力差分を 5+1 因子に
分解:

| 因子 | 意味 | 検出方法 |
|---|---|---|
| F1: prompt difference | 同 prompt が本当に同じか | 文字列 diff + token diff |
| F2: model id mismatch | model id が runtime と spec で一致か | `runtime_metadata.model_id` 比較 |
| F3: backend swap | LLMBackend が attach されているか | runtime hook で trace |
| F4: chars vs tokens | 評価指標が言語非依存か | tokenizer count |
| F5: RTT exclusion | subprocess / network RTT が時間に含まれるか | wall-clock vs CPU time |
| +1: env drift | 並走負荷 / OS schedule / thermal | 環境 fingerprint snapshot |

5+1 が **すべて clean** で初めて「数値は信頼できる」. 1 つでも怪しいと
**honest disclosure note** が結果に sticky される.

## 3. progressive size matrix — stress curve を取る

固定 token 数のベンチは情報量が低い. lleval は xs/s/m/l/xl の 5 段階 ×
複数 model の **matrix** を回す:

```
size:  xs (128)  s (512)   m (2k)    l (8k)    xl (32k)
mock     0.05      0.18      0.62      2.41      9.82
llive    0.07      0.24      0.71      2.55      9.96   ← 大差ない
gpt-4o   0.31      0.52      1.20      3.40      11.2   ← crossover at l
```

これで「**どのサイズで crossover が起きるか**」が一目. 単一サイズで「勝った」
と言ってもサイズ違いでは負ける. fair.

## 4. judge rotation — position bias を消す

LLM-as-judge で 2 案 (A, B) を比較するとき, 順序が score に effect する
ことが知られている (Zheng et al. 2023). lleval は:

1. (A, B) で 1 回 judge
2. (B, A) で 1 回 judge
3. 2 つの verdict が一致しないとき **inconsistency flag**

これは judge LLM 自身の bias を量子化する手段. inconsistency が **30% 超**
なら judge LLM を切り替える運用 (judge rotation).

## 5. bridges/llive — llive Genome → ProviderSpec mapper

lleval は **llive の派生個体** を直接食えるよう設計. `bridges/llive.py`
(2026-05-21 朝着地):

```python
from llive.perf.evolutionary import Individual
from lleval.bridges.llive import individual_to_provider_spec

ind: Individual = ...  # 派生集団から 1 個体
spec = individual_to_provider_spec(ind)
# spec.model_id, spec.temperature, spec.top_p, ... を ind.genome.values から復元
result = lleval.run(spec, dataset="qa_50")
```

これで「**派生集団の進化** と **派生集団の評価**」が ループする. llive 内の
EvolutionLoop fitness にそのまま渡せる.

## 6. honest disclosure (lleval 自身について)

メタにも honest disclosure を適用:

- **lleval test 数 61** — 本日 2026-05-21 時点. 上位フレームワーク (Promptfoo
  本体) は数千 test を持つ. lleval は wrap であり置換ではない.
- **判定の絶対基準は無い** — F1〜F5 + 環境 fingerprint が clean でも
  「ベンチが正しい」とは限らない. 「**怪しいサイン**」 を消した状態に過ぎない.
- **judge rotation はコストがかかる** — 2 倍呼び出すので credential 使用量も
  2 倍. honest 検出のためのコスト.
- **progressive matrix のサイズ等比は heuristic** — 4x ずつ (128 → 512 → 2k
  → 8k → 32k) で取っているが, 真の crossover が 2k と 8k の間にある場合
  解像度不足. 必要に応じ細密化.
- **環境 fingerprint は完璧ではない** — Windows / Linux / macOS 間の thermal
  throttling 違いまでは捉えていない. 「ベンチを別 OS で取り直す」が最終手段.

## 7. 数字 (本日 2026-05-21 時点)

| 項目 | 値 |
|---|---|
| lleval test PASS | 61 |
| 着地 module | 13 (config / runner / analyzer / providers / bridges /
report html+md / cli / ...) |
| 5+1 因子検出ロジック | 着地済 |
| progressive matrix runner | 着地済 |
| judge rotation | 着地済 |
| bridges/llive.py | 着地済 (skeleton) |
| v0.1.0a1 PyPI 公開準備 | (credential 復旧後) |
| 連載 #24 への登場 | 本記事 (#24-08) |

## 8. 期待値 — 次に来るもの

- **v0.1.0a2** で promptfoo 実走 + llive Genome → ProviderSpec mapping 完成.
- **v0.2** で judge rotation + position swap + Phoenix OpenInference trace.
- **v1.0** で plugin marketplace + 商用 dual-license.

## 9. References

- Zheng, L. et al. (2023). *Judging LLM-as-a-judge with MT-Bench and Chatbot Arena*.
- Promptfoo OSS (https://github.com/promptfoo/promptfoo).
- Anthropic Eval framework (2023).
- 完全リストは v0.1.0 リリース時に references.bib に同梱予定.

## 10. 2026-05-22 追記 — 5+1 因子分解 と Rust 化 5 パターン判定表の方法論的共通点

lleval の honest disclosure **5+1 因子分解** (prompt diff / model id /
backend swap / chars vs tokens / RTT / env drift) と, 同日着地した
llive Rust 高速化の **5 パターン判定表** (#24-05 §13.3) は **構造的に同じ
発想** で書かれている.

| 共通する思想 | lleval 5+1 因子 | Rust 化 5 パターン |
|---|---|---|
| 「結果」を信じる前に **要素分解** | 速度差を 6 因子に分解 | 速度比を Python 経路の特性別 5 パターンに分類 |
| **異常結果は内訳を疑う** | F1〜F5 + env を疑う | 単発 0.80x も x66.70 も「内訳」で説明できる |
| 観察が外部化されている | analyzer で自動検出 | 判定表 + bench script で自動測定 |
| **honest disclosure を一級概念に** | 数値に sticky note | judgment 表で **どこが境界線か** を明示 |

両者とも「**「速い」「正しい」「正確」の単一仮定を捨てる**」という
`feedback_benchmark_honest_disclosure` (内部参照) の延長線上にある. これは lleval が
AI を見るだけでなく **AI / システム / アルゴリズム 全般** に展開できる
発想 = 連載 #24-08 のメタ的意義.

詳細: `docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md`.

---

> draft (10x volume 版は次セッション). 骨子 + 10 main section + honest
> disclosure 5 件 + 5+1 因子と Rust 化判定表の方法論的共通点 (2026-05-22 追記).

---

## Series Navigation

- ← 前: [llive 完全解説 (7) 「審査つき AI」](https://qiita.com/furuse-kazufumi/private/c5f2077a3399d3fc9b26)
- 全体: [llive 完全解説 (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
