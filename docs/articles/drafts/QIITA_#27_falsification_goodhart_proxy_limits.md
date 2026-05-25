---
title: '「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #27（Goodhart の法則と proxy fitness の限界）'
tags:
  - FullSense
  - llive
  - honest_disclosure
  - 進化計算
  - 機械学習
private: true
updated_at: '2026-05-25'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

> ⚠ 本記事は **ja 骨子ドラフト**（蓄積目的・完璧不要）。en/zh/ko 展開は後続。投稿前に hero/theme SVG・進捗 badge・#25/#26 の Qiita URL cross-link を埋める。

# 日本語

# 「眼鏡が飽和すると選択圧は無力」— 進化設計を反証で鍛える #27

> **コンセプト hook**: #25 で失敗を晒し、#26 で「淘汰器 lldarwin」を設計しました。普通の連載なら
> 次は「直りました! めでたし」です。**でも、それをやらないのが FullSense の honest disclosure**。
> この記事はあえて**自分の設計に反証をぶつける回**。テーマは進化計算と機械学習の両方に効く一語——
> **Goodhart's law（指標が目標になると、良い指標でなくなる）**。
>
> 「LLM の弱点を fitness にすれば進化で克服できる」——この楽観に、私は冷や水をかけにいきます。

---

## 0. 三行であらすじ

- **眼鏡（fitness）が飽和すると、どんな高級な選択圧（lldarwin）を足しても淘汰は無力**になる（#25 の真の教訓）。
- **proxy fitness で LLM 弱点を測ると、真能力でなく「指標をハックする表面戦略」が進化する**（Goodhart's law）。
- 結論: lldarwin の価値主張は **(a) proxy は mechanism feasibility のみ (b) 実 LLM/VLM 評価が本質 (c) 多様性の地図化** に**限定**する。これが正直な線引き。

---

## 1. honest disclosure の念押し — 良い結果ほど疑う

#26 で「PoC デプロイで行動 monoculture は全条件 0.05（≪0.8）に改善した」と書きました。
これは事実です。が、ここで終わると **#25 で自分が立てた誓いを破る**ことになる。

> 異常に綺麗な結果が出たら、勝った気になる前に内訳を疑う（[[feedback_benchmark_honest_disclosure]]）。

「0.05 に改善」も、内訳を疑わねばなりません。**何を測った 0.05 なのか?** ——答えは「proxy 評価における
**行動** monoculture」。これは「genome の振る舞い代理」の多様性であって、**実 LLM の知能多様性ではない**。
ここを混同すると、#25 と同じ轍を踏みます。

> 🍵 **休憩ポイント**: この記事は「自分にダメ出しする記事」です。読者の皆さんには
> 「成功報告の裏で、著者が何をどこまで疑っているか」を観察してもらう回。SNS でバズる「AI 進化させたら
> 最強○○が誕生」の逆をいきます。

---

## 2. 反証 1 — 飽和した眼鏡には、どんな選択圧も効かない

#25 の真因は「best_score が 1 世代目から 1.0 に飽和 → 選択圧ゼロ → 遺伝的浮動」でした。
ここで重要な反証: **lldarwin（ε-lexicase でも QD でも）を、飽和した eval にそのまま挿しても直らない**。

なぜか。ε-lexicase は「軸ごとに差があること」が前提。**全軸が満点なら軸を分けても差はゼロ**。
QD は「behavior 記述子に分散があること」が前提。**全個体が同じ振る舞いなら cell も 1 つ**。

```
壊れた眼鏡（fitness 飽和） + 高級な淘汰器 = やっぱり壊れたまま
```

つまり **#25 が直ったのは lldarwin のおかげ「だけ」ではない**。眼鏡側の修正
（per-dim z-score 標準化 + 中央一致除外 + 記述子の低次元縮約）が**先**にあって、初めて淘汰器が効いた。
**「測る」を直さず「淘汰する」だけ高級にしても無駄** ——これが #25→#26 で見落とされがちな反証です。

> 🤔 **たとえ話（漫才風）**:
> ボケ「審査員を 100 人に増やしたのに、全員に同じ満点の答案見せたら結果一緒やった」
> ツッコミ「審査員ちゃう、答案（テスト）が壊れとるんや!」

**節の肉付け予定**: 「眼鏡修正（STD-1/SEL-1/DESC-1）」と「淘汰器（SEL-3/QD-1）」の責務を分けた図。
どちらが欠けても進化が壊れることを 2×2 マトリクスで。

---

## 3. 反証 2 — Goodhart's law: proxy fitness をハックする進化

最重大リスクです。**LLM の弱点を proxy fitness にすると、真能力でなく「指標をハックする表面戦略」が進化する**。

| pressure | 起こりうる gaming（指標ハック） |
|---|---|
| typo_robustness | 特定の typo パターンを暗記して置換するだけ |
| polysemy_wsd | テストの分布ヒューリスティクスを利用（意味理解でなく） |
| multistep_robustness | persuasive な推論「痕跡」だけ生成（実推論せず） |
| calibration | 自信度を中庸に操作して ECE を下げる（較正でなく） |

> **指標が目標になると、それは良い指標でなくなる（Goodhart's law）。**

これは LLM 研究の実例でもあります（GSM8K 型でスコアだけ上がり汎化しない benchmark overfitting）。
進化はこの種の「近道」を見つける天才。**proxy が真能力と乖離する**のは時間の問題。

**対策（設計に織り込み済）**:
- proxy は **mechanism feasibility 検証に限定**し、production 能力を主張しない
- **実 LLM/VLM 評価（Stage 2）を本質**とする
- **neutral shadow 対照**（Bedau）で見かけの改善を疑う
- **down-sampling** で環境かく乱 + **OOD 軸**で過学習を相殺

> 🍵 **休憩ポイント**: 「対策があるなら問題ないのでは?」——いいえ。対策は**乖離を遅らせる**だけで、
> proxy が真能力でない事実は消えません。だから「proxy で LLM が賢くなった」とは**口が裂けても言わない**。

---

## 4. 反証 3 — 設計者依存性: 「多様性の方向」は誰が決めた?

ε-lexicase の case、QD の behavior 記述子、novelty の距離尺度、minimal-criterion の基準値——
**いずれも「多様性の方向」を設計者（私）が決めています**。

つまり lldarwin が生む多様性は「**設計者が想定した軸の中での**多様性」であって、
生物進化級の**未想定創発**ではない（Taylor et al. 2016 が指摘する open-endedness の限界）。

**受容**: lldarwin は「検証可能性のない多様性の**地図**」を狙うのであって（DIFF-1）、
strong / unbounded open-endedness は主張しない（SCOPE と整合）。**勝てる軸を限定する**のが正直さです。

---

## 5. 反証 4 — minimal-criterion と QD 自身のトレードオフ

淘汰器の各部品にも固有の弱点があります:

- **minimal-criterion の停滞⇄崩壊**: 基準が低い → 選択圧ゼロで停滞 / 高い → 全滅（実証あり）。
  対策: criterion を集団分位点で適応 + 全員 fail なら gate 無視。
- **QD の次元の呪い + アーカイブ飽和**: 記述子が高次元だと cell が空、長期で飽和し新規性頭打ち
  （Avida/Tierra も同様）。対策: 低次元縮約（JL 射影）+ 飽和を Bedau 統計で監視し「飽和＝失敗」として正直に記録。
- **lexicase のスケール限界**: case 数が多いとコスト増 + ノイズでランダム選択化。対策: down-sampled lexicase。

> 🤔 **たとえ話（漫才風）**:
> ボケ「全滅させない最低ラインを設けたら、今度は誰も成長せえへんようになった」
> ツッコミ「ぬるま湯と地獄の二択かい! 中間（適応的基準）を探せや!」

---

## 6. 結論 — どこまで主張してよいか（線引き）

「LLM の弱点を proxy fitness にすれば進化で克服できる」は**楽観的**。lldarwin の価値主張を**限定**します:

1. **(a) proxy は mechanism feasibility のみ** — 進化の配管が動くことの検証。production 能力は主張しない。
2. **(b) 実 LLM/VLM 評価が本質** — 知能の選択圧は個体→実モデル写像（Stage 2）が担う。ここがまだ未踏。
3. **(c) 多様性の地図化** — 勝てる軸を「検証可能性のない多様性（認知・文化スタイル）の地図」に限定する。

これが honest disclosure。**失敗（#25）も、限界（#27）も消さずに残す**。次に進む足場はこの線引きの上にあります。

---

## 7. 教訓（永久保存）

- **良い結果（0.05 改善）ほど内訳を疑う。** 「proxy 行動多様性」は「実 LLM 知能多様性」ではない。
- **「測る」を直さず「淘汰する」だけ高級にしても無駄。** 飽和した眼鏡にはどんな選択圧も効かない。
- **Goodhart's law は進化の天敵。** 指標を目標にした瞬間、進化はそれをハックする。
- **設計者が多様性の方向を決めている以上、未想定創発は主張しない。** 勝てる軸を限定するのが誠実さ。

> **次回予告**: 反証で足場を固めたら、次は Stage 2（実 LLM/VLM 評価, on-prem ollama）。
> proxy の幻でなく、実モデルの知能多様性を選択圧にできるか。ここからが本番です。

---

## 8. 関連
- 連載 #25「私とフリストンだけが残った」— 失敗の記録（本記事の起点）
- 連載 #26「lldarwin の設計」— 淘汰器（本記事が反証する対象）
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_implementation_status_record]]
- 参考: Goodhart's law / La Cava 2019 (lexicase) / Taylor et al. 2016 (open-endedness の限界) / Bedau (neutral shadow)

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #25・#26 の Qiita URL cross-link / en・zh・ko 版展開 -->
<!-- KEY MESSAGE: honest disclosure の本丸。飽和した眼鏡には選択圧が効かない + Goodhart + 設計者依存。主張を 3 点に限定。 -->
<!-- NOTE(事実整合): PoC デプロイで monoculture は実際 0.05 に改善した(誇張でない)。本記事はそれを否定せず「何を測った 0.05 か」を honest に深掘りする構成。「lldarwin を入れても改善せず」とは書かない(事実と異なるため)。 -->
