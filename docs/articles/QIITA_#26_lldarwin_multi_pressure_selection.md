---
title: '「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26（多目的淘汰 / ε-lexicase / 中立貯蔵庫 / 実 LLM 評価）'
tags:
  - FullSense
  - llive
  - 進化計算
  - 多目的最適化
  - 解説
private: true
updated_at: '2026-05-26'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---
言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 「眼鏡で測る」だけでは進化しない — 選択圧コンポーネント lldarwin の設計と実測 #26

> **コンセプト hook**: 前作 #25 で、私は「AI を 500 世代進化させたら、世界に**私とフリストンだけ**が残った」という大失敗を晒しました。
> 岡潔もグロタンディークもフォン・ノイマンも、全員、進化の途中で静かに消えていった。原因は、評価関数（眼鏡 = lleval）が満点を出し続けて、**選択圧がゼロになった**こと。誰が優れているか「測れて」いても、その差を「誰が生き残るか」に変換できなければ、進化はただの遺伝的浮動に堕ちる。
>
> では——眼鏡で差を「測れた」として、その差を「淘汰」に**正しく変換する装置**はどう作るのか。
> それが今回の主役、**lldarwin**。ll- ファミリーの新メンバーで、**淘汰（選択圧）専門**のコンポーネントです。
>
> この記事で覚えてほしいキーワードは、たった一語。**「集約しない」**。複数の物差しを 1 本に足し算した瞬間、進化は壊れます。なぜそうなるのか、そしてどう実測でそれを乗り越えたのか——失敗の続きから、今度は**実際に動いた**話をします。

---

## 0. 三行であらすじ（落語の「枕」）

落語には本題の前に「枕」があります。まずは三行で全体像を。

- **lleval が測り、lldarwin が淘汰する** — 進化は「測る」と「淘汰する」の 2 段構えで、初めて意味を持つ。
- 淘汰の第一原則は、**複数の選択圧を集約しない多目的淘汰**。#25 の失敗（単一スカラーの argmax で潰した）の真因を、ここで構造的に断つ。
- 採用三本柱 = **ε-lexicase + minimal-criterion QD + down-sampling**（evolutionary_computation コーパス 616 件を横断して選定）。

そして今回は骨子だけでなく、**実測がある**のが #25 との違いです。novelty pressure で行動多様性を 7.12 → 14.88（+109%）に倍増させ、**中立貯蔵庫**で「絶滅した岡潔・グロタンディーク系統」を実際に**全員復活**させ、最後は **on-prem の本物の LLM（llama3.2）**を相手に、prompt 戦略を進化させて苦手タスクを 0.0 → 1.0 に改善させた。順を追って見ていきます。

---

## 1. なぜ「測る」と「淘汰する」を分けるのか

llive ファミリーには、すでに **lleval（眼鏡 = 評価フレームワーク、連載 #24-08）** があります。個体の振る舞いを観測し、複数の軸でスコア化する装置です。

ところが #25 でわかったのは、致命的な真実でした。**眼鏡で差を測れても、その差を argmax で 1 本に潰したら、淘汰が壊れる。** 具体的には、`fitness_rich` が複数の archetype 類似度を `nearest = max(sims)` という単一スカラーに畳んでいた。これが SEL-2 違反——「best=1.0 が飽和し、全員が満点になり、選択勾配が消える」真因です。

役割を明確に分けると、こうなります。

```
lleval   = 測る  （個体の振る舞いを「複数軸の pressure profile」に変換）
lldarwin = 淘汰する（その profile を「次世代の親」に変換）
```

`lleval` の出力は **case ベクトル**（各軸のスコアが並んだ配列）です。`lldarwin` はそれを入力契約として受け取り、**集約せずに**淘汰する。両者の責務境界はここにあります。lleval が「軸を 1 本に足し算してから」渡してきたら、lldarwin は何もできません。だから lleval 側には「breakdown（軸ごとの内訳）を必ず保持して渡す」ことを契約として課す。

lldarwin の `Pressure` インターフェースは、次の最小契約で表現されます。

- `name` — 軸の名前（`typo_robustness` 等）
- `evaluate(individual_output) -> case_scores: list[float]` — 個体の振る舞いを「軸ごとのスコア配列」に変換
- `is_proxy: bool` — proxy 測定か、実 LLM/VLM 測定か（測定純度の区別）
- `minimal_criterion: float | None` — その軸の最低繁殖基準（None なら gate なし）

ポイントは、`evaluate` の戻り値が**スカラーではなくリスト**であること。1 軸の中にも複数の case（テストケース）があり、それを潰さずに lldarwin へ流す。この「潰さない」設計が、後で specialist を救う伏線になります。

> 🍵 **休憩ポイント**: 眼鏡（lleval）とフィルター（lldarwin）を分ける意味は、写真でいう「露出を測る」と「どのカットを採用するか決める」の違いです。測光が完璧でも、ベストショットの選び方を間違えればアルバムは台無し。露出計（lleval）が「この一枚は明るさ 80 点、構図 30 点、表情 95 点」と教えてくれても、それを「平均 68 点」に丸めて捨てるか、「表情 95 点の一枚は別枠で残す」かで、アルバムの豊かさは天と地ほど変わる。lldarwin は「採用判断」の専門家です。測る人と選ぶ人を兼任させると、たいてい両方が雑になる。

---

## 2. 設計の核 — 「集約しない」7 ステージ

lldarwin は、lleval から受け取った pressure profile（複数軸の case ベクトル）を、次の 7 ステージで淘汰します。それぞれに「なぜ必要か = どの失敗を防ぐか」を添えます。

1. **Standardizer** — per-dim z-score。「全軸が平均的に高い」だけの無特徴な優等生を優位にせず、各軸での**逸脱**を選択圧に変える。中央一致（みんなと同じ）は除外。
   - *防ぐ失敗*: 「平均点が高いだけ」の凡庸が勝ち、尖った個体が消える monoculture の入口。
2. **MinimalCriterionGate** — 各軸の最低基準で繁殖の可否を分ける。連続順位だけで「総取り」させない。
   - *防ぐ失敗*: 一強がすべての繁殖枠を独占する全滅シナリオ。基準を満たせば誰でも繁殖できる「最低保証」で多様性の土台を残す。
3. **EpsilonLexicaseSelection** — 軸を case として 1 つずつ独立に評価する。ある軸で突出した specialist（他軸は平凡）が生き残れる。
   - *防ぐ失敗*: 集約 argmax による specialist の絶滅。これが #25 の 8→2 を生んだ機構そのもの。
4. **QD / MAP-Elites archive** — pressure profile を behavior 記述子に変換し、cell ごとに elite を保持。archive は単調成長。
   - *防ぐ失敗*: 構造的な全滅。1 つの cell に 1 個体でも残れば、その振る舞いは消えない。
5. **Niching / FitnessSharing** — 同じ niche の個体を down-weight し、多峰を並存させる。
   - *防ぐ失敗*: 単峰への凝集（monoculture）。
6. **Down-sampling** — 毎世代、case の部分集合だけで評価して環境をかく乱する。
   - *防ぐ失敗*: 特定 peak への過適応と plateau（停滞高原）。moving target にすることで「同じ勝ち方」を許さない。
7. **NoveltyScorer** — 停滞時に「過去と違う振る舞い」へ探索圧をかける。
   - *防ぐ失敗*: 探索枯渇。改善が止まったとき、新規性そのものを報酬にして外へ押し出す。

#25 の 8→2 monoculture と対比すると、核は **(3) ε-lexicase・(4) QD archive・(2) minimal-criterion** の三つです。#25 では、これらがすべて欠けて単一スカラー argmax だけが回っていた。だから「平均的に最強な 1 系統」が連続順位を総取りし、残りが浮動で消えた。lldarwin はこの 3 つを「集約せずに束ねる」ことで、世代を重ねても破綻しない構造を作ります。

> 🤔 **たとえ話（漫才風）**:
> ボケ「テストの点を全部足して順位つけたら、平均点が高いだけの優等生ばっかり残ったわ」
> ツッコミ「それ多様性ゼロや! 数学だけ 100 点・他 0 点の天才が消えてるやんか!」
> ボケ「いや、トータルで見たら優等生のほうが上やし……」
> ツッコミ「**トータルで見るな!** 科目を 1 つずつ見たら、その天才は『数学』の case では誰にも負けへんのや。ε-lexicase はそれを救う仕組みやねん。足し算した瞬間に天才は死ぬ」
> ——足し算（集約）が specialist を殺す。ε-lexicase は「科目を 1 つずつ見る」から、尖った奴が残る。これが lldarwin の一丁目一番地です。

---

## 3. なぜこの 3 本柱なのか（rad-research の裏付け）

「世代を重ねても破綻しない」最有力の融合案として、evolutionary_computation コーパス 616 件を横断して選定しました。自前で発明したのではなく、既存研究の「集約しない」系譜を選別して束ねた——という来歴が大事です。

| 手法 | 効能 | 出典 |
|---|---|---|
| **ε-lexicase** | specialist 保存・high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | cell 別 elite で全滅不可 | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | 環境かく乱・コスト削減 | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | 早期収束防止（将来オプション） | Lyu 2020 (2005.07376) |

三本柱はバラバラの手法に見えて、実は **「集約しない」という 1 つの思想**で串刺しにできます。ε-lexicase は「軸を集約しない」。QD は「振る舞い空間を集約しない（cell ごとに保持）」。down-sampling は「評価環境を固定しない（毎世代かく乱）」。どれも「1 本に丸めない」点で同じ哲学です。だから組み合わせても思想が衝突せず、相乗する。

> 🍵 **休憩ポイント**: 「なぜ自前で発明しないのか?」と訊かれます。答えは単純で、**既存研究の組合せで十分強いから**。私の開発ルール（[[feedback_originality_over_imitation]]）には「外部アルゴリズムの採用は網羅でなく**選別**。破綻リスクや単なる模倣は排除し、独自設計に価値を足すものだけ採る」とあります。lldarwin の独自性は「新しい選択アルゴリズムを発明したこと」ではなく、「これらを**集約せず束ねる束ね方**と、それを llive の進化ループに**実際に配線**したこと」にある。料理でいえば、世界初の食材を作るのではなく、既存の名食材を「混ぜずに一皿に盛りつける」技です。混ぜたら台無しになる素材を、混ぜずに共存させる。

---

## 4. Stage1 — criteria 除外 + novelty pressure で行動多様性を倍にする

ここから実測です。Stage1 では、設計をいきなり全部実装するのではなく、最も効きそうな 2 つの変更だけを入れて測りました（llive, branch `optimize/core-2026-05-20`、commit `8060204`）。

**変更 1: criteria 除外。** ε-lexicase の case から、`factor_score`（= max-archetype の単一スカラー = argmax、まさに #25 の best=1.0 飽和の真因）と `nearest_persona_idx`（= 順序に意味のないカテゴリ index）を外しました。これは「悪い物差しを淘汰の判断材料から除く」掃除です。

**変更 2: novelty pressure。** `MultiPressureSelector(use_novelty=True)` を有効化。毎世代、過去世代の archive との k-NN 平均距離（Lehman-Stanley 流の novelty）を計算し、それを集団内で z-score 化（STD-1）して、追加の lexicase case として淘汰に混ぜます。「みんなと違う振る舞いをしている」こと自体を、軸の 1 つとして評価する。

テストは `tests/unit/test_evolutionary_lldarwin.py` を 8 → 10 件に拡張（除外・novelty 保存を追加）。進化系 847 件 green、回帰なし。

実測条件は rich-proxy、8 founders + pop24、150 世代、seed 0。結果が以下です。

### 4.1 行動多様性 (diversity_l2) — novelty が効く指標

| 条件 | mean | tail30 min | final |
|---|---|---|---|
| BASELINE（除外前・Tournament 相当の旧 lldarwin） | 7.12 | 0.68 | 0.83（崩壊） |
| A: criteria 除外のみ | 9.16 | 1.57 | 1.57 |
| **B: 除外 + novelty** | **14.88（+109%）** | **6.56（9.6×）** | **11.73（崩壊回避）** |

novelty pressure は、行動（genome 空間）の多様性を約 2 倍に維持し、終盤の多様性崩壊を防ぎました。criteria 除外だけでも単独で効いている（spurious な argmax 圧を取り除いたぶん）。BASELINE は final 0.83 で**崩壊**しているのに対し、B 条件は final 11.73 で**踏みとどまっている**。これが「集約しない」設計の第一の手応えです。

![Stage1 baseline（novelty なし）の適応度と多様性。終盤に多様性が崩壊する](../assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg)

![Stage1 novelty あり。多様性が終盤まで維持される](../assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status.svg)

2 枚を並べると、終盤の挙動の違いが一目でわかります。baseline は多様性の曲線が床に張り付くのに対し、novelty ありは高い水準を保ったまま走り切る。

> 🍵 **休憩ポイント**: novelty pressure を金魚の池でたとえると——餌（高 fitness）に群がる金魚ばかり残すと、いずれ全員が同じ場所で同じ動きをする池になります。novelty pressure は「**みんなと違う場所を泳いでる金魚にもボーナス**」を出す係です。結果、池のあちこちに散らばった、見ていて飽きない池になる。ただしここで油断してはいけません。次の節で、この「賑やかな池」に潜んでいた**落とし穴**が見つかります。

---

## 5. honest disclosure（最重要）— 行動多様性と系統生存を私は混同していた

ここが本記事で一番大事な節です。良い数字（+109%）が出たからといって、勝った気にならない——これは私の鉄則（[[feedback_benchmark_honest_disclosure]]）です。内訳を疑いました。そして、間違いを見つけました。

### 5.1 系統固定 (founder_counts) — novelty では改善しない指標

同じ実測で、別の指標を見ます。「8 人の founder（祖先系統）のうち、何系統が最後まで生き残ったか」。

結果は——**全条件で最終的に 8 → 2 系統**（furuse-kazufumi + friston）に収束。oka-kiyoshi（岡潔）/ grothendieck（グロタンディーク）/ von-neumann / feynman / millidge / isomura は、**全部絶滅**。

novelty を入れて行動多様性を倍にしたのに、**系統の生き残りは #25 とまったく同じ 2 系統**だったのです。

### 5.2 なぜか — 私は 2 つの「多様性」を混同していた

設計書（#25 時点）の TODO には「再ランで岡潔・グロタンディーク系統が生き残るか検証」とありました。これは、**行動多様性と系統生存を混同していた**のです。

`poc_evolution_env.py` の著者コメント（L129-132）が、この混同を正確に言い当てています。

> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs QD niching on lineage / PERSONA-FX, not pure novelty**"

噛み砕くと、こうです。

- 実証済の monoculture 0.05 は、**行動的**（archive-cell の占有率）であって、**系統的ではない**。novelty/lexicase が改善するのは「振る舞いの広がり」であって「祖先の生き残り」ではない。
- 系統固定が中立浮動（木村資生の中立進化説）によって monoculture に向かうのは、**理論的に正常**です。崩壊ではない。novelty も lexicase も、**既存個体を保存する**機構しか持たず、**いったん絶滅した系統を復活させる機構を持たない**。だから系統固定は構造的に止められない。
- さらに、archetype 間距離も 0.068〜0.29 と圧縮されていて（類似度が 0.71〜1.0 に密集）、選択勾配が弱く drift（浮動）が支配的。friston は最も非中心的（centroid 距離 0.162）なのに生き残った = 中心性（強さ）ではなく、**運（drift）**で 2 系統が固定したのです。

つまり——「岡潔・グロタンが生き残ってほしい」という私の願いは、**行動多様性を上げる薬では絶対に治らない病気**だった。薬を間違えていた。これは正直に記録する価値のある教訓です。

> 🍵 **休憩ポイント**: 漫才で言うなら。
> ボケ「池に色とりどりの動きをする金魚を増やしたで! 多様性バッチリや!」
> ツッコミ「で、**血統**は? 8 つあった金魚の家系、いくつ残ってんの?」
> ボケ「……2 つや」
> ツッコミ「動きは派手やのに家系図はスカスカやないか! 動きの多様性と血統の多様性は**別の話**やぞ!」
> ——「行動が多様」と「系統が多様」は、見た目が似ているだけのまったく別の指標。私はこれを混同していました。正直に晒します。

---

## 6. Stage1.5 — 中立貯蔵庫で絶滅した系統を蘇らせる

病気の正体がわかれば、薬を変えられます。系統生存に必要なのは「絶滅した系統を毎世代 re-inject する機構」——**lineage-niched 中立貯蔵庫（reservoir）**です。

### 6.1 まず PoC で機構を確かめる

いきなり本番ループを改造せず、まず standalone PoC で機構が回ることを確かめました（[[feedback_poc_feasibility_first]] = 要件 → PoC → フィジビリティ → 詳細設計、llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`）。

selection は Stage1 の `MultiPressureSelector`（criteria 除外 + novelty）を流用。fitness は rich-proxy。系統は parent_a から継承。**reservoir = 系統別の best-ever genome を保持し、絶滅した系統を毎世代 re-inject する**（低 score の子を置き換える。best は壊さない）。8 founders + pop24 + 150 gens + seed 0 で測りました。

| reservoir | 最終 named 系統 | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1**（oka-kiyoshi 24/24 = 完全 monoculture） | 1.00 | 1.58 |
| **ON** | **8（全 founder 生存）** | **0.31（≪ 0.8 OE-3）** | 1.69 |

reservoir ON で、岡潔（oka）・グロタンディーク（grothendieck）を含む**全 8 系統が生存**。最終 shares は friston 7 / furuse 6 / grothendieck 4 / oka 3 / 他 4 系統各 1。**強い系統は子孫を持って繁殖し、弱い系統は貯蔵庫が生命維持する**という、理想的な挙動です。行動多様性も低下なし（1.69 vs OFF 1.58）。

**Honest 留保（PoC 段階）**: 貯蔵庫は frozen elite（凍結された代表）を再投入するので、弱系統（各 1 体）の「生存」は再投入由来であって、能動的進化ではありません。これは中立貯蔵庫の定義どおり（代表を保持し、再結合可能にする）で正当ですが、「弱系統が活発に進化し続ける」とは主張しません。

### 6.2 本番 EvolutionLoop へ組込（additive + default-off）

PoC で機構が確かめられたので、本番の `EvolutionLoop` に組み込みました（commit `b03cbda`）。設計の肝は **additive かつ default-off**——既存の挙動を一切変えず、フラグを立てたときだけ有効になる。後方互換を死守しました。

- `EvolutionLoop.on_population_bred` hook を追加（breed 直後・評価前に bred リストを変換できる。既定 None = 後方互換）。
- `LineageReservoir`（`lineage_reservoir.py`）: 祖先追跡（parent_ids[0] を継承）+ 系統別 best-ever 保持 + 絶滅保護系統の re-inject。`founder_map` を共有し系統ログとも整合。
- `run_persona_evolution(lineage_reservoir=True)` / run スクリプト `--lineage-reservoir` を追加。
- tests: `test_evolutionary_lineage_reservoir.py` 6 件 + 進化系 **937 green**（回帰なし）。

実 EvolutionLoop での実測（rich-proxy + lldarwin + novelty, 8 founders / pop24 / 150gens / seed0）。

| 条件 | named 系統生存 | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8（furuse 17 + friston 7） | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8（全系統）** | **0.33** | **0.29（≪ 0.8 OE-3）** | 9.20 |

岡潔（oka 3）・グロタンディーク（grothendieck 1）を含む**全 8 系統が、実ループで生存**しました。PoC の予測（fixation 0.31）を、本番実装が 0.29 で再現した——機構が設計どおり動いた証拠です。

これが、本記事最大の見せ場です。下の 2 枚を見比べてください。

![中立貯蔵庫 OFF。系統支配ストリームが最終的に furuse 71% / friston 29% の 2 系統に崩壊する](../assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

![中立貯蔵庫 ON。全 8 系統（millidge / von-neumann / oka / grothendieck 等）が並存する](../assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

OFF（上）は、世代が進むにつれてストリームが 2 色に呑み込まれていく——「私と friston だけが残った」#25 の再現です。ON（下）は、8 色が最後まで帯として残る。岡潔もグロタンディークも、消えていない。

![中立貯蔵庫 ON の適応度と多様性](../assets/lldarwin_2026_05_26/lldarwin_reservoir_on_status.svg)

> 🍵 **休憩ポイント**: #25 で「私とフリストンだけが残った」と嘆いた、あの寂しい世界。それが今度は岡潔もグロタンディークもフォン・ノイマンも全員いる、賑やかな世界に変わりました。**これは捏造ではなく、実際に動いた結果です**（[[feedback_benchmark_honest_disclosure]] に従い、虚偽の失敗も虚偽の成功も書きません）。ただし——浮かれる前に、§5 で学んだ姿勢を思い出しましょう。「いい数字が出たら内訳を疑う」。次の §6.3 で、この成功にも**代償**があったことを正直に書きます。

### 6.3 Honest 留保 — 系統保持と行動多様性は弱いトレードオフ

reservoir ON で系統は全員生き残りました。が、よく見ると **diversity_l2 は 14.88 → 9.20 に低下**しています。frozen elite（凍結代表）を毎世代再投入するぶん、genome 空間の広がりがやや減るのです。

ただし、OFF 時の崩壊（final 0.83）は回避しています。つまり「系統保持を取ると、行動多様性のピークは少し下がるが、崩壊は防げる」という**弱いトレードオフ**の関係です。代償ゼロの魔法ではない。これを正直に書いておきます。そして、この代償をどこまで小さくできるかが、次の sweep の主題になります。

---

## 7. 再投入頻度 sweep — 非単調な最適点という非自明な発見

§6.3 の honest 留保（frozen elite 再投入で diversity が下がる）を、`reinject_interval`（再投入を行う世代間隔。既定 1 = 毎世代）の sweep で特性化しました（commit `da93dd3`）。`LineageReservoir.reinject_interval` + `--reinject-interval` フラグを追加（test 7 件）。8 founders / pop24 / 150gens / seed0。

| interval | named 生存 | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1**（毎世代） | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84（最大）** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**ここで非自明な発見がありました。** 直感的には「再投入を減らす（interval を上げる）ほど、frozen elite の押し込みが減って diversity が単調に回復する」と予想しますよね。ところが——**diversity は単調増加せず、interval=5 でピーク**を打ち、10/20 ではむしろ低下したのです。

理由を考えると腑に落ちます。系統を放置しすぎる（interval が大きすぎる）と、(a) 貯蔵庫由来の多様性注入が減り、(b) 少数系統が固定してしまって、結局 diversity も伸びない。「再投入しすぎ」も「放置しすぎ」も両方ダメで、中間に最適点がある。これは**実際に sweep を回さなければ予測できなかった**知見です。

運用指針はこうなりました。

- **系統保持を最優先**するなら → interval=1（8/8 全系統生存）。
- **行動多様性も両立**させたいなら → interval=5（5/8 を保持しつつ diversity 最大）。

両立の最適点は fitness の設計や集団規模に依存するので、本番では sweep で再較正します。

![再投入頻度のトレードオフ。系統保持と行動多様性は反比例し、diversity は interval=5 でピークを打つ（非単調）](../assets/lldarwin_2026_05_26/lldarwin_reinject_sweep.svg)

> 🍵 **休憩ポイント**: 落語のサゲ（オチ）のように、ここには「予想を裏切る転」があります。「やればやるほど良い」と思っていたら、「やりすぎると逆効果」だった。植物の水やりと同じで、あげなさすぎても枯れるし、あげすぎても根腐れする。中庸に最適点がある。進化計算をやっていると、こういう「単調じゃない曲線」に何度も出会います。だからベースラインを測り、sweep を回す。直感は、よく裏切られる。

---

## 8. Stage2 前半 — 「LLM の苦手」を proxy で選択圧にする

ここまでは rich-proxy（persona 類似度ベースの heuristic）で機構を確かめてきました。次は設計のもう 1 つの柱、**「LLM/VLM が現実に弱く、かつ測定可能な軸」を pressure にする**を実装します（commit の系列、`pressures.py`）。

設計 §3 で挙げた proxy 可能な 5 軸を plugin 化しました。

| pressure（LLM 弱点） | 関連思考因子（case） |
|---|---|
| typo_robustness（ノイズ耐性） | consistency / reality_link / uncertainty |
| polysemy_wsd（多義語） | multiview / consistency / reality_link |
| multistep_robustness（多段推論） | structurize / closed_loop / self_extend |
| calibration（信頼度推定） | uncertainty / provenance |
| context_management（無関係文脈耐性） | consistency / provenance / recompose |

`make_pressure_fitness()` が各 pressure の case（計 14）を breakdown に出力し、lldarwin の ε-lexicase が**集約せず軸ごとに specialist を淘汰**します。`--fitness pressure-proxy` を追加。tests `test_evolutionary_pressures.py` 4 件 + 進化系 **942 green**。

end-to-end の実測（pressure-proxy + lldarwin + novelty + reservoir, 8 founders / 120gens）: named 系統 **8/8 生存** / lineage_fixation (tail) 0.67 / diversity_l2 (tail) **17.91**。14 個の苦手軸 case が独立に淘汰され、行動多様性は高い。系統は reservoir が維持しています（pressure-proxy は persona の同一性を直接報酬化しないため、優占系統の share は rich-proxy の 0.29 より高い 0.67 になります）。

![5 苦手軸（typo / polysemy / multistep / calibration / context）の母集団平均推移（proxy 測定）](../assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes.svg)

**Honest 留保（設計 §7 / §7.1 に明記済の受容済み限界）**: 個体は実 LLM ではなく genome（llive 構成）です。本 pressure が測るのは「genome がその弱点に**関連する思考因子**をどれだけ備えるか」という**振る舞いの代理**であって、**production の LLM 能力ではありません**。これは **mechanism feasibility（機構が回ること）の検証**に限定されます。Goodhart リスク（proxy をハックする表面戦略が進化する）も受容済みの限界です。実 LLM/VLM の苦手軸の実測は、Stage2 後半（OLLAMA_HOST 設定 + 個体→実 LLM 写像が前提）に持ち越します。

> 🍵 **休憩ポイント**: ここは誤解されやすいので、念押しします。「LLM の苦手を進化で克服した!」とは**まだ言っていません**。proxy が測っているのは「機構が回るか」だけ。本物の LLM がタイポに強くなったかどうかは、この段階では一切わからない。proxy で派手な数字（17.91）が出ても、それは「装置が動く」証明であって「中身が賢くなった」証明ではない。この線引きを曖昧にした瞬間、研究は嘘になります。だから次に、**本物の LLM**を相手にします。

---

## 9. Stage2 後半 — 本物の on-prem LLM を相手に prompt 戦略を進化させる

localhost の ollama（llama3.2:latest 等）が到達可能とわかったので、ついに**実 LLM 評価**が可能になりました（commit `2fb2912`）。localhost = on-prem なので、measurement purity（測定純度。cloud LLM と混在させない）の規律も満たします（[[feedback_llive_measurement_purity]]）。

### 9.1 個体 → 実 LLM への写像（Promptbreeder 系）

肝は「genome を、どうやって実 LLM に効かせるか」です。`real_pressures.py` で **個体 → 実 LLM 写像**を実装しました。

- **個体の `c_prompt`（PromptChromosome）を system prompt に変換**: skill_set → 指示文 / prompt_template_id → 推論スタイル / language_style → 語調。固定の LLM（llama3.2）にこの system prompt を被せ、5 苦手軸の**実タスク**を解かせて採点します。
- **LLM 本体は固定し、prompt 戦略（genome）を進化させる** = 「どの prompt 戦略が LLM の弱点を緩和するか」を実測で淘汰する。これは Promptbreeder（prompt を進化的に最適化する研究系列）の流儀です。
- temp=0（greedy）で決定論的に。`(system_prompt, task)` をキャッシュ（同一戦略は再評価しない）。
- robust: per-call try/except（ollama の hiccup は task の失点として扱い、走行は継続）。
- `--fitness real-pressure` / `--ollama-model` / `--max-wallclock-seconds` を追加。tests 5 件 + 進化系 947 green。

### 9.2 実選択信号の実証 — CoT+structure 戦略が multistep を 0.0 → 1.0 に

そして、本物の選択信号が観測できました。

**CoT+structure 戦略**（`chain_of_thought` + structurize + loop）が、llama3.2 の **multistep（多段推論）を 0.0 → 1.0 に改善**しました（terse な戦略は 0.0 で失敗。score は 0.80 → 1.00 に上昇）。

これは、lldarwin の主張「prompt 戦略の進化で LLM の弱点を緩和できる」を、**proxy ではなく実 LLM で実証**したことを意味します。同じ llama3.2 本体でも、被せる system prompt（= 進化した genome）次第で、多段推論タスクが解けたり解けなかったりする。進化は「解ける prompt 戦略」を実際に選び取ったのです。

![5 苦手軸の母集団平均推移（実 on-prem LLM llama3.2 評価）。prompt 戦略の進化で軸が改善する](../assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

### 9.3 12h 連続ラン

実 LLM 評価は重いので、長時間の連続ランを起動しました（`out/lldarwin_12h_realpressure_2026_05_26/`）。

```
--fitness real-pressure --selection lldarwin --novelty --lineage-reservoir
--genome3d --population 24 --max-wallclock-seconds 43200 --checkpoint-every 5
```

wallclock 12h で safely 停止（snapshot 済 → `--resume` で継続可能）。連続ランの中で best_score=1.0 に到達しています。

![実 LLM 進化ランの適応度と多様性（12h 連続ラン）](../assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status.svg)

### 9.4 Honest 留保（実 LLM 評価の限界）

ここが #25 から学んだ姿勢の総決算です。派手な結果（0.0 → 1.0、best 1.0）が出たからこそ、内訳を徹底的に正直に書きます。

- **(a) fitness に関与するのは `c_prompt` だけ。** persona / c_factors は中立（系統は reservoir で維持、初期選択は novelty が担う）。つまりこれは「**prompt 戦略の進化**」であって「persona の進化」ではありません。岡潔の人格が賢くなったのではなく、岡潔という系統に紐づいた prompt 戦略が選ばれた、という話。
- **(b) 全 founder の初期 c_prompt は同一（default）。** だから探索は mutation 駆動です（founder ごとに prompt を多様化させるのは今後の改善）。スタート地点が同じなので、初期の系統差は prompt 戦略には効いていない。
- **(c) 小バッテリ（軸あたり 2 問）= ノイジーな推定。** 0.0 → 1.0 という劇的な数字も、問題数が少ないぶんノイズを含みます。統計的に堅牢な主張をするには、もっと大きなバッテリが要る。
- **(d) on-prem only（measurement purity）。一般能力の主張ではない。** llama3.2 という特定モデル・特定タスクでの観測であって、「LLM 一般がこうなる」とは言いません。

これらを伏せれば「進化で LLM が劇的に賢くなった!」という派手な物語が書けますが、それは嘘です。lldarwin が実証したのは「**機構が、実 LLM 上で、選択信号を生む**」というところまで。その線を越えた主張はしません。

> 🍵 **休憩ポイント**: 研究で一番気持ちいいのは「0.0 が 1.0 になった!」と叫ぶ瞬間です。でも、その瞬間こそ [[feedback_benchmark_honest_disclosure]] が効いてくる。「変に良い数字が出たら、勝った気になる前に内訳を疑え」。今回でいえば——勝ったのは「prompt 戦略」であって「LLM 本体」でも「persona」でもない。問題数も少ない。on-prem の 1 モデルだけ。これを全部書いてから、初めて「実証した」と言える。honest disclosure は、自慢を我慢する筋トレです。

---

## 10. 既存資産の再利用（codex コード調査ベース）

設計を絵に描いた餅にしないため、配下の Codex に既存コードを調査させたところ、**多くは実装済・未配線**でした。

- `mating.py:139 LexicaseSelection`（ε 付き、実装済だが未配線 → 配線するだけ）
- `nsga2.py:197 NSGA2Selection`（≤3 目的レーン用）
- `diversity.py:94 NoveltyScorer` / `quality_diversity.py MAPElitesGrid` / `speciation.py SpeciationLayer`

**新規実装**: `Standardizer` / `MinimalCriterionGate` / `Pressure` 群 / `MultiPressureSelector`（中核）/ `LineageReservoir`（Stage1.5）/ `SelectionAudit`。
**配線点**: `loop.py:122` の `selection` に `MultiPressureSelector` を注入、`persona_evolution.py:606` に注入口を追加、`EvolutionLoop.on_population_bred` hook に `LineageReservoir` を接続。

> 🍵 **休憩ポイント**: 「実装済だが未配線」が一番多かったのが、最大の教訓でした。良い部品を作っても、**配線（オーケストレーション）しなければ進化は壊れたまま**。#25 で 8→2 になったのは、ε-lexicase も NoveltyScorer も QD も「箱の中にあったのに、配線されていなかった」から。lldarwin の本質は、新規アルゴリズムの発明よりも、「既存の良い部品を**集約せず**束ねて、進化ループに**実際に配線する**こと」にあります。電子部品を全部揃えても、半田付けしなければラジオは鳴らない。

---

## 11. 破綻回避の保証 — 全滅しない多層構造（実測で裏付け済）

#25 の monoculture（8→2）を反証する多層構造は、設計どおりに揃い、しかも今回は**実測で裏付けられました**。

1. **MinimalCriterionGate** — 最低基準で繁殖可否 → 一強総取りを抑制。
2. **QD cell 別 elite** — 1 cell でも残れば系統全滅不可（archive 単調成長）。
3. **Niching / FitnessSharing** — 同 niche を down-weight → 多峰並存。
4. **Down-sampling** — moving target で plateau 破壊。
5. **per-dim z-score + 中央一致除外** — 無特徴を優位にしない。
6. **LineageReservoir（Stage1.5 で追加）** — 絶滅系統の中立貯蔵庫 → 系統全滅を構造的に阻止（実測で 8/8 生存）。
7. **monoculture モニタ + SPC** — max_lineage_share を毎世代記録、>0.8 を SPC_ALARM で検知 → 自動調整。

特に (6) は、§5 の honest disclosure（novelty では系統固定を止められない）を受けて**後から追加した層**です。設計の穴を実測で見つけ、塞いだ。実測の lineage_fixation は OFF 0.70 → ON 0.29 と、OE-3 基準（<0.8）を大きく下回ります。「集約しない」+「絶滅系統を蘇らせる」の二段構えで、#25 を構造的に潰せたのが本記事の到達点です。

---

## 12. honest disclosure / リスク（前振り）

設計を盲信しません。受容済みの限界（次作 #27 で深掘り）を、もう一度まとめておきます。

- **Goodhart's law / proxy 乖離** — LLM 弱点を proxy fitness にすると、「指標をハックする表面戦略」が進化する（typo → 特定置換の暗記、WSD → テストのヒューリスティクス利用、等）。proxy は mechanism feasibility に限定し、production 能力を主張しない。
- **設計者依存性** — lexicase=case / QD=記述子 / novelty=距離尺度、いずれも「多様性の方向」を設計者が決める。生物進化級の未想定創発は限定的。
- **minimal-criterion の停滞⇄崩壊トレードオフ** / **QD の次元の呪い + アーカイブ飽和**。
- **実 LLM 評価の限界（§9.4 再掲）** — c_prompt のみ fitness 関与・founder 初期 prompt 同一・小バッテリ・on-prem only。

> **次回予告（#27）**: 「眼鏡が飽和すると選択圧は無力」という最も痛い反証を、Goodhart's law と proxy fitness の限界とともに正直に晒します。lldarwin は万能ではない。**どこまで主張してよいか**の線引きが #27 の主題です。今回「8/8 生存」「0.0→1.0」という良い数字が出たからこそ、次は徹底的に反証で鍛えます。

---

## 13. 結論

- 進化は「**測る（lleval）**」と「**淘汰する（lldarwin）**」の 2 段構え。淘汰の核は **「集約しない」**。
- Stage1: criteria 除外 + novelty pressure で、行動多様性を 7.12 → 14.88（+109%）に倍増し、終盤の崩壊を回避した。
- honest disclosure: novelty/lexicase は**行動多様性**は保つが、**系統固定**は中立浮動（Kimura）で monoculture に向かう。私は 2 つの多様性を混同していた——正直に記録。
- Stage1.5: lineage-niched **中立貯蔵庫**で、実 EvolutionLoop において **OFF=2 系統 / ON=全 8 系統生存**（岡潔・グロタンディーク含む）、lineage_fixation 0.29（≪0.8）を実現。**これは捏造ではなく実際に動いた**。
- 再投入頻度 sweep: 系統保持↔行動多様性のトレードオフ。diversity は interval=5 でピーク（**非単調**）という非自明な知見。
- Stage2 前半（proxy）: 5 苦手軸を Pressure plugin 化（mechanism feasibility のみ）。
- Stage2 後半（実 LLM）: 個体 c_prompt → system prompt 写像で固定 on-prem LLM（llama3.2）を実タスク採点。**CoT+structure 戦略が multistep を 0.0 → 1.0 に改善**。12h 連続ランで best=1.0 到達。
- 楽観せず、勝った気にならず、内訳を分けて報告した（[[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]]）。

良い部品を作るだけでは進化は壊れたまま。**集約せずに束ね、実際に配線し、絶滅した系統を蘇らせ、本物の LLM で選択信号を確かめる**——そこまでやって、ようやく #25 の「私とフリストンだけ」の世界を、岡潔もグロタンディークもいる賑やかな世界に変えられました。次の #27 では、この成功にどこまで信を置いてよいかを、反証で問い直します。

---

## 14. 関連

- 連載 #25「私とフリストンだけが残った」— 本記事の動機（失敗の記録）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #27「眼鏡が曇ると淘汰も無力」— 反証調査（honest disclosure）
- 設計書: lldarwin（淘汰する側）`docs/vision/LLDARWIN_DESIGN.md`
- 実測正本: `docs/research/lldarwin_stage1_results_2026_05_26.md`
- llive commits: Stage1=`8060204` / 中立貯蔵庫 PoC=`0d0537d` / Stage1.5=`b03cbda` / reinject sweep=`da93dd3` / Stage2 実 LLM=`2fb2912`
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_originality_over_imitation]] / [[feedback_poc_feasibility_first]]

---

# English

# Measuring with "Glasses" Alone Doesn't Drive Evolution — Design and Measurements of the Selection-Pressure Component lldarwin #26

> **Concept hook**: In the previous article #25, I exposed a massive failure: "When I evolved an AI for 500 generations, the only ones left in the world were **me and Friston**."
> Oka Kiyoshi, Grothendieck, von Neumann — all of them quietly vanished mid-evolution. The cause: the evaluation function (the glasses = lleval) kept handing out perfect scores, so **the selection pressure dropped to zero**. Even if you can "measure" who is superior, if you can't convert that difference into "who survives," evolution degenerates into mere genetic drift.
>
> So then — granting that the glasses let us "measure" the differences, how do we build the device that **correctly converts** those differences into "selection"?
> That is the star of this article, **lldarwin**. A new member of the ll- family, it is the component **specialized in selection (selection pressure)**.
>
> The one keyword I want you to remember from this article is a single word: **"don't aggregate."** The moment you add multiple rulers together into one, evolution breaks. Why that happens, and how I overcame it with measurements — picking up from the failure, this time I'll tell a story about something that **actually worked**.

---

## 0. The gist in three lines (the rakugo "pillow")

In rakugo, there's a "pillow" before the main story. First, the whole picture in three lines.

- **lleval measures, lldarwin selects** — evolution only becomes meaningful as a two-stage structure of "measuring" and "selecting."
- The first principle of selection is **multi-objective selection that does not aggregate multiple selection pressures**. Here we structurally cut off the true cause of #25's failure (collapsing it with the argmax of a single scalar).
- The three adopted pillars = **ε-lexicase + minimal-criterion QD + down-sampling** (selected by surveying 616 documents in the evolutionary_computation corpus).

And this time, the difference from #25 is that there's not just the skeleton but **actual measurements**. With novelty pressure I doubled behavioral diversity from 7.12 → 14.88 (+109%), with the **neutral reservoir** I actually **revived every one** of the "extinct Oka Kiyoshi / Grothendieck lineages," and finally, against a **real on-prem LLM (llama3.2)**, I evolved prompt strategies and improved a weak task from 0.0 → 1.0. Let's go through it in order.

---

## 1. Why separate "measuring" and "selecting"

The llive family already has **lleval (the glasses = the evaluation framework, series #24-08)**. It is a device that observes an individual's behavior and scores it along multiple axes.

But what #25 revealed was a fatal truth. **Even if you can measure differences with the glasses, if you collapse those differences into one with argmax, selection breaks.** Concretely, `fitness_rich` was folding multiple archetype similarities into a single scalar via `nearest = max(sims)`. This is the SEL-2 violation — the true cause of "best=1.0 saturates, everyone gets a perfect score, and the selection gradient disappears."

If we clearly divide the roles, it looks like this.

```
lleval   = measure (converts an individual's behavior into a "multi-axis pressure profile")
lldarwin = select  (converts that profile into "the parents of the next generation")
```

The output of `lleval` is a **case vector** (an array of scores along each axis). `lldarwin` receives it as an input contract and selects **without aggregating**. This is exactly the boundary of responsibility between them. If lleval hands over the data after "adding the axes into one," lldarwin can do nothing. So on the lleval side we impose the contract: "you must always keep and pass the breakdown (the per-axis decomposition)."

lldarwin's `Pressure` interface is expressed by the following minimal contract.

- `name` — the name of the axis (`typo_robustness`, etc.)
- `evaluate(individual_output) -> case_scores: list[float]` — converts an individual's behavior into a "per-axis score array"
- `is_proxy: bool` — whether it is a proxy measurement or a real LLM/VLM measurement (the distinction of measurement purity)
- `minimal_criterion: float | None` — the minimum reproduction criterion for that axis (no gate if None)

The point is that the return value of `evaluate` is **a list, not a scalar**. Within a single axis there are multiple cases (test cases), and we pass them to lldarwin without collapsing them. This "don't collapse" design is the foreshadowing that will rescue the specialist later.

> 🍵 **Break point**: The meaning of separating the glasses (lleval) and the filter (lldarwin) is, in photography terms, the difference between "metering exposure" and "deciding which shot to adopt." Even if the light metering is perfect, if you choose the best shot wrongly the album is ruined. Even if the light meter (lleval) tells you "this one is 80 for brightness, 30 for composition, 95 for expression," whether you round it to "average 68" and discard it, or "keep the one with 95 expression in a separate slot," changes the richness of the album as much as heaven and earth. lldarwin is the specialist in "adoption decisions." If you make the measurer and the chooser the same person, usually both turn out sloppy.

---

## 2. The core of the design — the "don't aggregate" 7 stages

lldarwin selects the pressure profile (the multi-axis case vector) received from lleval through the following 7 stages. To each I attach "why it is needed = which failure it prevents."

1. **Standardizer** — per-dim z-score. It does not favor the featureless honor student who is merely "uniformly high across all axes," and instead turns the **deviation** on each axis into selection pressure. Central agreement (being the same as everyone) is excluded.
   - *Failure prevented*: the entrance to monoculture, where the mediocre who are "merely high on average" win and sharp individuals disappear.
2. **MinimalCriterionGate** — splits reproduction eligibility by a minimum criterion on each axis. Does not let a "winner-take-all" happen by continuous ranking alone.
   - *Failure prevented*: the total-wipeout scenario where a single strongest one monopolizes all reproduction slots. By a "minimum guarantee" that lets anyone who meets the criterion reproduce, the foundation of diversity is preserved.
3. **EpsilonLexicaseSelection** — evaluates the axes one by one independently as cases. A specialist that stands out on some axis (mediocre on others) can survive.
   - *Failure prevented*: the extinction of specialists by aggregated argmax. This is the very mechanism that produced #25's 8→2.
4. **QD / MAP-Elites archive** — converts the pressure profile into a behavior descriptor and keeps an elite per cell. The archive grows monotonically.
   - *Failure prevented*: structural total wipeout. As long as even one individual remains in one cell, that behavior does not disappear.
5. **Niching / FitnessSharing** — down-weights individuals in the same niche so multiple peaks can coexist.
   - *Failure prevented*: aggregation onto a single peak (monoculture).
6. **Down-sampling** — every generation, evaluates only on a subset of cases to perturb the environment.
   - *Failure prevented*: over-adaptation to a specific peak and a plateau (a stagnation plateau). By making it a moving target, it forbids "winning the same way."
7. **NoveltyScorer** — when stagnating, applies exploration pressure toward "behavior different from the past."
   - *Failure prevented*: exploration exhaustion. When improvement stops, it rewards novelty itself to push outward.

Contrasting with #25's 8→2 monoculture, the core is the three: **(3) ε-lexicase, (4) QD archive, (2) minimal-criterion**. In #25 these were all missing and only the single-scalar argmax was running. So "the one lineage strongest on average" took all the continuous ranking, and the rest disappeared by drift. By "bundling these three without aggregating," lldarwin builds a structure that does not break down even as generations accumulate.

> 🤔 **An analogy (manzai style)**:
> Boke: "I added up all the test scores and ranked them, and only honor students with high averages were left."
> Tsukkomi: "That's zero diversity! The genius with 100 in math and 0 in everything else has vanished!"
> Boke: "Well, looking at the total, the honor student is higher..."
> Tsukkomi: "**Don't look at the total!** If you look at the subjects one by one, that genius loses to no one on the 'math' case. ε-lexicase is the mechanism that rescues that. The moment you sum, the genius dies."
> — Summing (aggregation) kills the specialist. Because ε-lexicase "looks at the subjects one by one," the sharp ones survive. This is the very first principle of lldarwin.

---

## 3. Why these 3 pillars (the rad-research backing)

As the strongest candidate fusion that "does not break down even as generations accumulate," I selected it by surveying 616 documents in the evolutionary_computation corpus. The provenance matters: I did not invent it myself, but selected and bundled the "don't aggregate" lineage of existing research.

| Method | Effect | Source |
|---|---|---|
| **ε-lexicase** | specialist preservation, high population diversity | La Cava 2019 (arXiv 1905.13266) / 2204.06461 |
| **QD / MAP-Elites** | total wipeout impossible thanks to per-cell elites | Fontaine CMA-ME 2019 (1912.02400) / MNSLC GECCO 2024 |
| **down-sampled lexicase** | environmental perturbation, cost reduction | Helmuth & Spector 2021 (2106.06085) |
| island + extinction/repopulation | prevents premature convergence (future option) | Lyu 2020 (2005.07376) |

The three pillars look like disparate methods, but in fact they can be skewered by **one single idea: "don't aggregate."** ε-lexicase "does not aggregate the axes." QD "does not aggregate the behavior space (keeps it per cell)." Down-sampling "does not fix the evaluation environment (perturbs it every generation)." Each shares the same philosophy in not "rounding into one." So even when combined, the ideas do not clash and instead synergize.

> 🍵 **Break point**: People ask, "Why not invent it yourself?" The answer is simple: **because the combination of existing research is strong enough**. My development rule ([[feedback_originality_over_imitation]]) says: "The adoption of external algorithms is **selection**, not coverage. Exclude breakdown risk and mere imitation, and adopt only what adds value to the original design." lldarwin's originality is not "having invented a new selection algorithm," but "**the way it bundles these without aggregating**, and **actually wiring** that into llive's evolution loop." In cooking terms, it's not creating the world's first ingredient, but the craft of "plating famous existing ingredients on one dish without mixing them." Ingredients that would be ruined if mixed are made to coexist without mixing.

---

## 4. Stage1 — doubling behavioral diversity with criteria exclusion + novelty pressure

From here it's measurements. In Stage1, rather than implementing the whole design at once, I put in only the two changes most likely to be effective and measured (llive, branch `optimize/core-2026-05-20`, commit `8060204`).

**Change 1: criteria exclusion.** From the cases of ε-lexicase, I removed `factor_score` (= the single scalar of max-archetype = argmax, the very cause of #25's best=1.0 saturation) and `nearest_persona_idx` (= a category index with no meaningful ordering). This is a cleanup that "removes bad rulers from the material used to judge selection."

**Change 2: novelty pressure.** I enabled `MultiPressureSelector(use_novelty=True)`. Every generation it computes the k-NN average distance to the archive of past generations (Lehman-Stanley style novelty), z-scores it within the population (STD-1), and mixes it into selection as an additional lexicase case. It evaluates "behaving differently from everyone else" itself as one of the axes.

For tests, I expanded `tests/unit/test_evolutionary_lldarwin.py` from 8 → 10 (adding exclusion and novelty preservation). 847 evolution-system tests green, no regression.

The measurement conditions are rich-proxy, 8 founders + pop24, 150 generations, seed 0. The results are below.

### 4.1 Behavioral diversity (diversity_l2) — the metric where novelty works

| Condition | mean | tail30 min | final |
|---|---|---|---|
| BASELINE (pre-exclusion, old lldarwin equivalent to Tournament) | 7.12 | 0.68 | 0.83 (collapse) |
| A: criteria exclusion only | 9.16 | 1.57 | 1.57 |
| **B: exclusion + novelty** | **14.88 (+109%)** | **6.56 (9.6×)** | **11.73 (collapse avoided)** |

Novelty pressure maintained behavioral (genome-space) diversity at about double, and prevented the late-stage diversity collapse. Criteria exclusion alone is also effective on its own (to the extent it removes spurious argmax pressure). Whereas BASELINE **collapses** at final 0.83, condition B **holds its ground** at final 11.73. This is the first tangible sense of the "don't aggregate" design.

![Fitness and diversity of the Stage1 baseline (no novelty). Diversity collapses in the late stage](../assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg)

![Stage1 with novelty. Diversity is maintained until the late stage](../assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status.svg)

Placing the two side by side, the difference in late-stage behavior is clear at a glance. Whereas the baseline's diversity curve sticks to the floor, the one with novelty runs to the finish while keeping a high level.

> 🍵 **Break point**: To liken novelty pressure to a goldfish pond — if you keep only the goldfish swarming around the food (high fitness), eventually you get a pond where everyone moves the same way in the same place. Novelty pressure is the role that "**gives a bonus to goldfish swimming in different places from everyone**" too. As a result, you get a pond scattered everywhere, one you never tire of watching. But don't let your guard down here. In the next section, a **pitfall** lurking in this "lively pond" is discovered.

---

## 5. honest disclosure (most important) — I had been confusing behavioral diversity and lineage survival

This is the most important section of this article. Just because a good number (+109%) came out does not mean I get to feel like a winner — this is my iron rule ([[feedback_benchmark_honest_disclosure]]). I doubted the breakdown. And I found a mistake.

### 5.1 Lineage fixation (founder_counts) — the metric novelty does not improve

In the same measurement, I look at a different metric. "Of the 8 founders (ancestral lineages), how many lineages survived to the end?"

The result — **in all conditions, it ultimately converged from 8 → 2 lineages** (furuse-kazufumi + friston). oka-kiyoshi (Oka Kiyoshi) / grothendieck (Grothendieck) / von-neumann / feynman / millidge / isomura all **went extinct**.

Even though I put in novelty and doubled behavioral diversity, **the lineage survival was exactly the same 2 lineages as #25**.

### 5.2 Why — I had been confusing two kinds of "diversity"

The TODO in the design document (as of #25) said "verify in a re-run whether the Oka Kiyoshi / Grothendieck lineages survive." This was **confusing behavioral diversity with lineage survival**.

The author's comment in `poc_evolution_env.py` (L129-132) pins down this confusion precisely.

> "monoculture = BEHAVIORAL concentration (max archive-cell occupancy)…
> neutral drift (Kimura) regardless of mechanism — that is expected, not collapse.
> The OE signal is behavioral spread. **lineage_fixation … to keep it <1 needs QD niching on lineage / PERSONA-FX, not pure novelty**"

Broken down, it's this.

- The demonstrated monoculture 0.05 is **behavioral** (the occupancy rate of archive cells), not **lineage-based**. What novelty/lexicase improves is "the spread of behavior," not "the survival of ancestors."
- That lineage fixation heads toward monoculture by neutral drift (Motoo Kimura's neutral theory of evolution) is **theoretically normal**. It is not collapse. Both novelty and lexicase have only mechanisms that **preserve existing individuals**, and have **no mechanism to revive a lineage that has once gone extinct**. So lineage fixation cannot be stopped structurally.
- Furthermore, the inter-archetype distances are also compressed at 0.068–0.29 (similarities densely packed in 0.71–1.0), so the selection gradient is weak and drift dominates. friston is the most non-central (centroid distance 0.162) yet survived = it was not centrality (strength) but **luck (drift)** by which the 2 lineages fixed.

In other words — my wish that "I want Oka and Grothendieck to survive" was a disease that **the medicine of raising behavioral diversity can absolutely never cure**. I had the wrong medicine. This is a lesson worth recording honestly.

> 🍵 **Break point**: Put in manzai terms.
> Boke: "I increased the goldfish that move in colorful ways in the pond! Diversity is perfect!"
> Tsukkomi: "And the **bloodline**? Of the 8 goldfish families that existed, how many are left?"
> Boke: "...two."
> Tsukkomi: "The movements are flashy but the family tree is threadbare! Diversity of movement and diversity of bloodline are **separate matters**!"
> — "Behavior is diverse" and "lineage is diverse" are entirely different metrics that merely look alike. I had been confusing them. I expose it honestly.

---

## 6. Stage1.5 — reviving extinct lineages with a neutral reservoir

Once you understand the true nature of the disease, you can change the medicine. What lineage survival needs is "a mechanism to re-inject extinct lineages every generation" — a **lineage-niched neutral reservoir**.

### 6.1 First, confirm the mechanism with a PoC

Rather than remodeling the production loop right away, I first confirmed the mechanism runs with a standalone PoC ([[feedback_poc_feasibility_first]] = requirements → PoC → feasibility → detailed design, llive `scripts/poc_lineage_reservoir.py`, commit `0d0537d`).

Selection reuses Stage1's `MultiPressureSelector` (criteria exclusion + novelty). Fitness is rich-proxy. Lineage is inherited from parent_a. **The reservoir = keeps the best-ever genome per lineage and re-injects extinct lineages every generation** (replacing low-score children; the best is not destroyed). I measured with 8 founders + pop24 + 150 gens + seed 0.

| reservoir | final named lineages | lineage_fixation (tail30 mean) | diversity_l2 (tail30) |
|---|---|---|---|
| OFF | **1** (oka-kiyoshi 24/24 = complete monoculture) | 1.00 | 1.58 |
| **ON** | **8 (all founders survive)** | **0.31 (≪ 0.8 OE-3)** | 1.69 |

With reservoir ON, **all 8 lineages survived**, including Oka (oka) and Grothendieck (grothendieck). The final shares are friston 7 / furuse 6 / grothendieck 4 / oka 3 / the other 4 lineages 1 each. The ideal behavior: **strong lineages reproduce with descendants, while weak lineages are kept alive by the reservoir**. Behavioral diversity also did not drop (1.69 vs OFF 1.58).

**Honest caveat (PoC stage)**: Because the reservoir re-injects frozen elites (frozen representatives), the "survival" of weak lineages (1 individual each) is due to re-injection, not active evolution. This is legitimate per the very definition of a neutral reservoir (keep representatives and make them recombinable), but I do not claim "weak lineages keep actively evolving."

### 6.2 Integration into the production EvolutionLoop (additive + default-off)

Since the mechanism was confirmed by the PoC, I integrated it into the production `EvolutionLoop` (commit `b03cbda`). The crux of the design is **additive and default-off** — it changes none of the existing behavior, and becomes active only when the flag is set. I defended backward compatibility to the death.

- Added the `EvolutionLoop.on_population_bred` hook (can transform the bred list right after breeding, before evaluation; default None = backward compatible).
- `LineageReservoir` (`lineage_reservoir.py`): ancestor tracking (inheriting parent_ids[0]) + per-lineage best-ever retention + re-injection of extinction-protected lineages. It shares `founder_map` and stays consistent with the lineage log.
- Added `run_persona_evolution(lineage_reservoir=True)` / the run-script flag `--lineage-reservoir`.
- tests: `test_evolutionary_lineage_reservoir.py` 6 + evolution-system **937 green** (no regression).

Measurement in the real EvolutionLoop (rich-proxy + lldarwin + novelty, 8 founders / pop24 / 150gens / seed0).

| Condition | named lineage survival | max_share | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|---|
| reservoir OFF (Stage1) | 2/8 (furuse 17 + friston 7) | 0.71 | 0.70 | 14.88 |
| **reservoir ON (Stage1.5)** | **8/8 (all lineages)** | **0.33** | **0.29 (≪ 0.8 OE-3)** | 9.20 |

**All 8 lineages survived in the real loop**, including Oka (oka 3) and Grothendieck (grothendieck 1). The production implementation reproduced the PoC's prediction (fixation 0.31) at 0.29 — proof that the mechanism worked as designed.

This is the biggest highlight of this article. Compare the two below.

![Neutral reservoir OFF. The lineage-dominance stream ultimately collapses to 2 lineages, furuse 71% / friston 29%](../assets/lldarwin_2026_05_26/lldarwin_reservoir_off_dominance.svg)

![Neutral reservoir ON. All 8 lineages (millidge / von-neumann / oka / grothendieck, etc.) coexist](../assets/lldarwin_2026_05_26/lldarwin_reservoir_on_dominance.svg)

OFF (top): as generations advance, the stream gets swallowed into 2 colors — a reproduction of #25's "only me and friston remained." ON (bottom): 8 colors remain as bands until the end. Neither Oka nor Grothendieck has disappeared.

![Fitness and diversity with the neutral reservoir ON](../assets/lldarwin_2026_05_26/lldarwin_reservoir_on_status.svg)

> 🍵 **Break point**: That lonely world I lamented in #25, "only me and Friston remained." This time it has changed into a lively world where Oka, Grothendieck, and von Neumann are all present. **This is not fabrication; it is a result that actually ran** (following [[feedback_benchmark_honest_disclosure]], I write neither false failures nor false successes). But — before getting carried away, recall the attitude learned in §5. "When a good number comes out, doubt the breakdown." In the next §6.3, I honestly write that this success too came with a **cost**.

### 6.3 Honest caveat — lineage retention and behavioral diversity are a weak trade-off

With reservoir ON, all lineages survived. But look closely and **diversity_l2 drops from 14.88 → 9.20**. Because frozen elites (frozen representatives) are re-injected every generation, the spread of genome space decreases somewhat.

However, the collapse when OFF (final 0.83) is avoided. In other words, it's a **weak trade-off** relationship: "if you take lineage retention, the peak of behavioral diversity drops a little, but collapse can be prevented." It is not zero-cost magic. I write this honestly. And how far this cost can be minimized becomes the subject of the next sweep.

---

## 7. Re-injection frequency sweep — a non-trivial discovery of a non-monotonic optimum

I characterized §6.3's honest caveat (frozen elite re-injection lowers diversity) with a sweep of `reinject_interval` (the generation interval at which re-injection is performed; default 1 = every generation) (commit `da93dd3`). I added `LineageReservoir.reinject_interval` + the `--reinject-interval` flag (7 tests). 8 founders / pop24 / 150gens / seed0.

| interval | named survival | lineage_fixation (tail30) | diversity_l2 (tail30) |
|---|---|---|---|
| **1** (every generation) | **8/8** | 0.32 | 9.91 |
| 5 | 5/8 | 0.37 | **12.84 (max)** |
| 10 | 3/8 | 0.41 | 11.41 |
| 20 | 2/8 | 0.44 | 10.75 |

**Here there was a non-trivial discovery.** Intuitively, you'd expect that "the more you reduce re-injection (raise the interval), the less the frozen elites are pushed in, and diversity recovers monotonically," right? But — **diversity did not increase monotonically; it peaked at interval=5** and actually dropped at 10/20.

When you think about the reason, it makes sense. If you leave the lineages alone too much (the interval is too large), (a) the diversity injection originating from the reservoir decreases, and (b) a few lineages fix, so in the end diversity doesn't grow either. Both "re-injecting too much" and "leaving alone too much" are bad, and there is an optimum in between. This is a finding that **could not have been predicted without actually running the sweep**.

The operational guideline became this.

- If you **prioritize lineage retention above all** → interval=1 (8/8 all lineages survive).
- If you want to **also achieve behavioral diversity** → interval=5 (retains 5/8 while maximizing diversity).

The optimum for achieving both depends on the fitness design and the population size, so in production I re-calibrate it with a sweep.

![The trade-off of re-injection frequency. Lineage retention and behavioral diversity are inversely related, and diversity peaks at interval=5 (non-monotonic)](../assets/lldarwin_2026_05_26/lldarwin_reinject_sweep.svg)

> 🍵 **Break point**: Like the sage (punchline) of a rakugo, there is a "twist that betrays expectations" here. I thought "the more you do it the better," but it was "do it too much and it backfires." Same as watering plants: water too little and they wither, water too much and the roots rot. The optimum is in moderation. When you do evolutionary computation, you meet these "non-monotonic curves" again and again. That's why you measure baselines and run sweeps. Intuition is often betrayed.

---

## 8. Stage2 first half — making "the LLM's weaknesses" into selection pressure by proxy

Up to here I confirmed the mechanism with rich-proxy (a heuristic based on persona similarity). Next I implement another pillar of the design: **making "axes where the LLM/VLM is actually weak, and which are measurable" into pressures** (a series of commits, `pressures.py`).

I made the 5 proxy-capable axes listed in design §3 into plugins.

| pressure (LLM weakness) | related thought factors (case) |
|---|---|
| typo_robustness (noise tolerance) | consistency / reality_link / uncertainty |
| polysemy_wsd (polysemous words) | multiview / consistency / reality_link |
| multistep_robustness (multi-step reasoning) | structurize / closed_loop / self_extend |
| calibration (confidence estimation) | uncertainty / provenance |
| context_management (irrelevant-context tolerance) | consistency / provenance / recompose |

`make_pressure_fitness()` outputs the cases of each pressure (14 in total) into the breakdown, and lldarwin's ε-lexicase **selects specialists per axis without aggregating**. Added `--fitness pressure-proxy`. tests `test_evolutionary_pressures.py` 4 + evolution-system **942 green**.

End-to-end measurement (pressure-proxy + lldarwin + novelty + reservoir, 8 founders / 120gens): named lineages **8/8 survive** / lineage_fixation (tail) 0.67 / diversity_l2 (tail) **17.91**. The 14 weak-axis cases are selected independently, and behavioral diversity is high. Lineages are maintained by the reservoir (because pressure-proxy does not directly reward persona identity, the dominant lineage's share becomes 0.67, higher than rich-proxy's 0.29).

![Population-mean trajectory of the 5 weak axes (typo / polysemy / multistep / calibration / context) (proxy measurement)](../assets/lldarwin_2026_05_26/lldarwin_stage2_proxy_axes.svg)

**Honest caveat (an accepted limitation already stated in design §7 / §7.1)**: The individual is not a real LLM but a genome (an llive configuration). What this pressure measures is **a proxy for behavior** — "how much the genome possesses the **thought factors related** to that weakness" — and is **not the LLM ability of production**. This is limited to **the verification of mechanism feasibility (that the mechanism runs)**. The Goodhart risk (surface strategies that hack the proxy evolve) is also an accepted limitation. The actual measurement of real LLM/VLM weak axes is carried over to the second half of Stage2 (which presupposes the OLLAMA_HOST setting + the individual→real-LLM mapping).

> 🍵 **Break point**: This is easily misunderstood, so let me press the point. I have **not yet said** "I overcame the LLM's weaknesses by evolution!" What the proxy measures is only "whether the mechanism runs." Whether a real LLM became robust to typos is, at this stage, completely unknown. Even if a flashy number (17.91) comes out by proxy, that is proof that "the device works," not proof that "the contents got smarter." The moment you blur this line, the research becomes a lie. So next, I face **the real LLM**.

---

