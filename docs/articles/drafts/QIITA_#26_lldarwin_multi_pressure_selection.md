---
title: '「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計 #26（多目的淘汰 / ε-lexicase / minimal-criterion QD）'
tags:
  - FullSense
  - llive
  - 進化計算
  - 多目的最適化
  - 解説
private: true
updated_at: '2026-05-25'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

> ⚠ 本記事は **ja 骨子ドラフト**（蓄積目的・完璧不要）。en/zh/ko 展開は後続。投稿前に hero/theme SVG・進捗 badge・#25/#24-08 の Qiita URL cross-link を埋める。

# 日本語

# 「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計 #26

> **コンセプト hook**: 前作 #25 で「AI を 500 世代進化させたら世界に私とフリストンだけが残った」
> 大失敗を晒しました。原因は **評価関数（眼鏡 = lleval）が満点を出し続けて選択圧がゼロになった**こと。
> では、眼鏡で差を「測れた」として、その差を「誰が生き残るか」に**正しく変換する装置**はどう作るのか。
> それが今回の主役 **lldarwin** — ll- ファミリーの新メンバーで、**淘汰（選択圧）専門**のコンポーネントです。
>
> キーは一語だけ覚えてください: **「集約しない」**。複数の物差しを 1 本に足し算した瞬間、進化は壊れる。

---

## 0. 三行であらすじ（落語の「枕」）

- **lleval が測り、lldarwin が淘汰する** — 進化は「測る」と「淘汰する」の 2 段構えで初めて意味を持つ。
- 淘汰の第一原則は **複数選択圧を集約しない多目的淘汰**（#25 の失敗 = 単一スカラー argmax の真因をここで構造的に潰す）。
- 採用三本柱 = **ε-lexicase + minimal-criterion QD + down-sampling**（evolutionary_computation コーパス 616 件横断で選定）。

---

## 1. なぜ「測る」と「淘汰する」を分けるのか

llive ファミリーには既に **lleval（眼鏡 = 評価フレームワーク, 連載 #24-08）** があります。
ところが #25 でわかったのは、**眼鏡で差を測れても、その差を argmax で 1 本に潰したら淘汰が壊れる**こと。

```
lleval   = 測る  （個体の振る舞いを「複数軸の pressure profile」に変換）
lldarwin = 淘汰する（その profile を「次世代の親」に変換）
```

> 🍵 **休憩ポイント**: 眼鏡（lleval）とフィルター（lldarwin）を分ける意味は、写真でいう
> 「露出を測る」と「どのカットを採用するか決める」の違いです。測光が正しくても、ベストショットの
> 選び方を間違えればアルバムは台無し。lldarwin は「採用判断」の専門家です。

**節の肉付け予定**: lleval / lldarwin の責務境界表（測る側の出力スキーマ = case ベクトル、淘汰側の入力契約）。
`Pressure` インターフェース（`name` / `evaluate() -> case_scores` / `is_proxy` / `minimal_criterion`）を提示。

---

## 2. 設計の核 — 「集約しない」7 ステージ

lldarwin は pressure profile（複数軸の case ベクトル）を受けて、次の 7 ステージで淘汰します:

1. **Standardizer** — per-dim z-score（「全軸平均高」＝無特徴を優位にしない、逸脱を選択圧に）
2. **MinimalCriterionGate** — 各軸の最低基準で繁殖可否を分ける（連続順位の総取りを抑制 → 全滅回避）
3. **EpsilonLexicaseSelection** — 軸を case として 1 つずつ独立評価（specialist 保存）
4. **QD / MAP-Elites archive** — pressure profile を behavior 記述子に、cell 別 elite を保持（構造的に全滅不可）
5. **Niching / FitnessSharing** — 多峰並存（monoculture 抑制）
6. **Down-sampling** — 毎世代 case 部分集合で環境かく乱（plateau 破壊）
7. **NoveltyScorer** — 停滞時の探索圧（枯渇回避）

> 🤔 **たとえ話（漫才風）**:
> ボケ「テストの点を全部足して順位つけたら、平均点高いだけの優等生ばっかり残った」
> ツッコミ「それ多様性ゼロや! 数学だけ 100 点・他 0 点の天才が消えてるやんか!」
> ——足し算（集約）が specialist を殺す。ε-lexicase は「科目を 1 つずつ見る」から、尖った奴が残る。

**節の肉付け予定**: §2 の 7 ステージそれぞれに「なぜ必要か（どの失敗を防ぐか）」の 1 行を添える。
特に (3)(4)(2) が「世代を重ねても破綻しない」核であることを #25 の 8→2 と対比して図解。

---

## 3. なぜこの 3 本柱なのか（rad-research の裏付け）

「世代を重ねても破綻しない」最有力融合として、evolutionary_computation コーパス 616 件横断から選定:

| 手法 | 効能 | 出典 |
|---|---|---|
| **ε-lexicase** | specialist 保存・high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | cell 別 elite で全滅不可 | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | 環境かく乱・コスト削減 | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | 早期収束防止（将来オプション） | Lyu 2020 (2005.07376) |

> 🍵 **休憩ポイント**: 「なぜ自前で発明しないのか?」——既存研究の組合せで十分強いから。
> [[feedback_originality_over_imitation]] の原則どおり、**網羅でなく選別**。3 本柱は
> 「集約しない」という 1 つの思想で串刺しにできる組合せだから採った、という来歴をここで語る。

---

## 4. 「LLM の苦手」を選択圧にする — pressure カタログ

もう 1 つの設計方針は、**LLM/VLM が現実に弱く、かつ測定可能な軸**を pressure に選ぶこと
（検証できない領域は避ける = 差別化軸 DIFF-1）。

| pressure | LLM/VLM の苦手 | proxy/実 | 根拠 |
|---|---|---|---|
| typo_robustness | 誤字・ノイズ入力への一貫性 | proxy 可 | arXiv 2510.09536 / 2407.08989 |
| polysemy_wsd | 多義語の文脈依存理解 | proxy 可 | arXiv 2411.18337 / DiBiMT |
| multistep_robustness | 多段推論の cascade error | proxy 可 | 2511.21591 / 2402.08115 |
| calibration | 信頼度推定（token confidence ≈ random） | proxy 可 | 2604.19444 |
| faithfulness | CoT の最終答への忠実性 | hybrid | 2510.13272 |
| visual_qa | 画像認識・visual hallucination | 実 VLM 必須 | 2510.20696 |
| ood_generalization | 分布外汎化（RLHF が OOD を下げる） | dataset 依存 | 2310.06452 |
| context_management | 無関係文脈で reasoning 劣化 | proxy 可 | 2604.01161 |

**測定純度の分離**: proxy で測れる軸から PoC、実 LLM/VLM 軸は Stage 後半（[[feedback_llive_measurement_purity]]）。
pressure はプラグイン（行を足し `Pressure` 実装を追加するだけ）で拡張できる。

**節の肉付け予定**: 各 pressure の「proxy で何を測り、実評価で何を上書きするか」を 1 段落ずつ。
特に visual_qa は「これは何の絵か」の VLM 認識を on-prem llava で測る計画を具体化。

---

## 5. 既存資産の再利用（codex コード調査ベース）

設計を絵に描いた餅にしないため、配下の Codex に既存コードを調査させた結果、**多くは実装済・未配線**でした:

- `mating.py:139 LexicaseSelection`（ε 付き, 実装済だが未配線 → 配線するだけ）
- `nsga2.py:197 NSGA2Selection`（≤3 目的レーン用）
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**新規実装**: `Standardizer` / `MinimalCriterionGate` / `Pressure` 群 / `MultiPressureSelector`（中核）/ `SelectionAudit`。
**配線点**: `loop.py:122` の `selection` に `MultiPressureSelector` を注入、`persona_evolution.py:606` に注入口を追加。

> 🍵 **休憩ポイント**: 「実装済だが未配線」が一番多かったのが教訓。良い部品を作っても**配線（オーケストレーション）
> しないと進化は壊れたまま**。lldarwin の本質は新規アルゴリズムより「既存の良い部品を集約せず束ねる束ね方」です。

---

## 6. 破綻回避の保証 — 全滅しない多層構造

#25 の monoculture（8→2）を反証する多層:

1. **MinimalCriterionGate** — 最低基準で繁殖可否 → 一強総取りを抑制
2. **QD cell 別 elite** — 1 cell でも残れば系統全滅不可（archive 単調成長）
3. **Niching/FitnessSharing** — 同 niche を down-weight → 多峰並存
4. **Down-sampling** — moving target で plateau 破壊
5. **per-dim z-score + 中央一致除外** — 無特徴を優位にしない
6. **monoculture モニタ + SPC** — max_lineage_share を毎世代記録、>0.8 を SPC_ALARM で検知 → 自動調整

**実機初速の朗報**: 標準化 novelty + QD を実装した PoC デプロイ sweep（poc_evolution_env.py, wallclock 90s/条件）で、
**行動 monoculture は全条件 0.05（≪0.8）**。novelty÷scalar の多様性保持比は **4.25〜14.17x**。
「集約しない」設計が #25 を構造的に潰せる第一証拠です（詳細と限界は反証調査記事 #27 で正直に）。

---

## 7. honest disclosure / リスク（前振り）

設計を盲信しない。受容済みの限界（次作 #27 で深掘り）:
- **Goodhart's law / proxy 乖離** — LLM 弱点を proxy fitness にすると「指標をハックする表面戦略」が進化する
- **設計者依存性** — lexicase=case / QD=記述子 / novelty=距離尺度、いずれも多様性の方向を設計者が決める
- **minimal-criterion の停滞⇄崩壊トレードオフ** / **QD の次元の呪い + アーカイブ飽和**

> **次回予告（#27）**: 「眼鏡が飽和すると選択圧は無力」という最も痛い反証を、Goodhart's law と
> proxy fitness の限界とともに正直に晒します。lldarwin は万能ではない。**どこまで主張してよいか**の線引きが #27。

---

## 8. 関連
- 連載 #25「私とフリストンだけが残った」— 本記事の動機（失敗の記録）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #27「眼鏡が曇ると淘汰も無力」— 反証調査（honest disclosure）
- 設計書: lldarwin（淘汰する側）
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #25・#24-08・#27 の Qiita URL cross-link / en・zh・ko 版展開 -->
<!-- KEY MESSAGE: 進化は「測る(lleval)」と「淘汰する(lldarwin)」の 2 段。淘汰の核は「集約しない」。良い部品より配線。 -->
