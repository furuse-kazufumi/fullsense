# PERSONA-FX: 文化的ペルソナ獲得レイヤ (未来計画スケルトン)

> **ステータス**: スケルトン / 未来計画 (現状非破壊・実装は隔離 PoC で後日)。
> **位置づけ**: llive 進化アルゴリズムに「ペルソナ」を意味あるものとして乗せる設計。
> ゲノム進化（自由探索）とは**分離**した**文化レイヤ**。ll- シリーズ将来への種まきの一つ
> ([[project_hyperdimensional_thinking_seed]] と同じ未来計画棚)。
> **由来**: 2026-05-24 ユーザーとの設計対話（4 段の洗練を経て最単純形に収束）。

## 0. 解く問題

現状の persona evolution は、persona の factor_affinity を gen0 founder の genome に書き込む
だけ。交叉で**平均へブレンドして溶け**、persona 同一性は gen0 限り（一代）。「ペルソナが
進化過程で変化・継承される」が実現していない（ユーザー指摘）。

## 1. 核となる仕組み（最単純形）

**ペルソナは遺伝しない。文化ライブラリから、平均を外れた個体が相関で獲得する。**

- **ペルソナプール（ライブラリ）**: 任意個の persona を登録（prototype = factor_affinity 等の素養
  シグネチャ ＋ 専門性 rubric ＋ 任意の学習記憶）。**1 エントリ追加するだけで拡張**できる。
- **毎世代の獲得 pass**（genome 交叉とは独立）:
  1. 各個体の **平均からの逸脱度（novelty / 中心からの距離）** を測る。
  2. **逸脱が大きい（個性的な）個体**について、プール内各 persona prototype との **相関** を測る。
  3. **相関が高い persona を付与**（しきい値で非適用も可）。
- **被らない = persona 側のみ uniqueness（ユーザー確定 2026-05-24, 改訂）**: **1 persona は最大 1 個体**
  （同じ persona が複数個体に重複しない＝「被らない」）。ただし **1 個体は 0..N persona を持てる** —
  複数 persona を帯びる「多才/Renaissance 型」個体も、まったく持たない generic 個体も**一定数出てよい
  （むしろ面白い）**。
  → 機構は**最単純**: **各 persona が独立に「相関最大の個性的個体」を argmax で選ぶ**（しきい値つき）。
  マッチングアルゴリズムすら不要（貪欲/Hungarian も不要、persona ごとの argmax だけ）。persona の重複は
  自動的に無く、個体側の多重/ゼロは**創発**（人気個体＝hub が複数 persona を引き寄せ、平均的個体はゼロ）。
- **継承機構なし**: 親→子の persona 受け渡し・系譜・genome 書き込みは**不要**。毎世代フレッシュに
  再選定。→ 相関する個性的個体が居ない persona は**休眠（隔世待ち）**。**隔世（休眠→後世で再覚醒）が
  特別な管理なしに自然に出る**。
- **genome は完全自由**に進化（persona 制約ゼロ、測定純度を保つ）。

実社会の根拠: 書籍・芸術・思想からの継承は遺伝と無関係（ミーム / 水平的文化伝達,
Dawkins / Boyd & Richerson）。「ドストエフスキーに似た個体」はラベル付け（共鳴）であって血統ではない。

## 2. 構造的な勝ち筋（多様性エンジンの内蔵）

「**平均から外れた個体ほど個性的 persona を獲得できる**」を、獲得が**報酬**（その persona の
専門 rubric で評価され高得点を取れる / 多様性ボーナス）にすると、**「平均から外れること」自体が
選択圧**になり → **個性化＝多様性維持エンジン**が内蔵される。別の島/speciation 機構を足さずに
open-ended 性が出る（=設計対話で先に挙げた「収束で相関が潰れ退化する」リスクを、この形が自前で解く）。

**創発する個体側の多重分布（2026-05-24 ユーザー）**: per-persona argmax の結果、一部の hub 個体が
複数 persona を集め（多才/Renaissance 型）、大半はゼロ（generic）になる — preferential attachment 的に
**自然に「一定数」出る**（強制不要）。これは副産物として 2 つの価値を持つ:
- **共起構造が測れる**: 「どの persona が同一個体に共起しやすいか」= persona 間の親和構造（学べる構造）。
- **退化のバロメータ**: 集団が収束すると **1 個体が全 persona を総取り（退化 hub）**しうる →
  多重分布の偏りが「多様性エンジンが効いているか」の可視化された診断計になる（退化が見える＝good）。

## 3. llive では既存部品でほぼ組める

- **逸脱度** = `diversity.py` の `NoveltyScorer`（中心からの距離）を流用。
- **相関** = persona の `factor_affinity`(10 因子) と個体 genome の因子重みは同空間 → cosine/相関を即計算。
- **眼鏡（専門性 rubric / 報酬軸）** = `lleval` / `poc_lens` を流用（[[project_poc_lens_lleval_integration]]）。
- **新規は「persona ライブラリ（小 store）＋毎世代 matching pass」のみ**。genome / EvolutionLoop は
  無改修・分離（extensibility 契約遵守）。

## 4. honest disclosure / リスク（必読）

- **眼鏡/相関尺度の信頼性が土台**: `poc_lens` 結論「全 trust<1.0・単に高速≠採用・実測で上書き要」。
  「素養（逸脱の測り方）」と「相関/専門性 rubric」の**操作的定義を検証**してから採用。spurious な
  相関で獲得すると無意味。
- **報酬設計**: 多様性駆動は「獲得が benefit を伴う」場合のみ。単なるラベルなら多様性効果なし。
  逆に報酬が強すぎると persona に過剰適合する**“偽の個性”で gaming** するリスク（非自明性テスト＝
  Hyperdimensional の偽の拡張検出と同型の guard が要る）。
- **測定純度**: 遺伝 fitness と persona 専門性スコアは**別信号として分離記録**（混ぜない）。学習記憶
  更新は on-prem のみ・Approval Bus で監査可能に。

## 5. 任意の拡張（最単純形には不要）

設計対話で出た richer variants は、この核の**任意拡張**に格下げできる（必須でない）。
なお **uniqueness（1 persona ≤1 個体, MAP-Elites の 1 cell 1 elite 相当）は §1 で核に昇格済**。
- **学習記憶の蓄積**: persona プール側に「その persona を embody した個体が学んだ成功パターン」を
  累積（cultural memory / Cultural Algorithm の belief space）→ 連続性・洗練を付加。
- **襲名の物語化（cross-gen 連続性）**: 同 persona の歴代 bearer を「名跡の系譜」として可視化
  （割当自体は毎世代フレッシュ、その時系列を物語として束ねる。落語/歌舞伎の名跡 demo 訴求）。
- **島 / speciation**: 文化集団化（核が多様性を自前で駆動するなら不要かもしれない）。

## 6. 差別化（正直に）

基盤（cultural transmission / novelty / QD / 文化アルゴリズム）はいずれも**既存**。FullSense 独自性は
**novelty(逸脱) × lleval 眼鏡(相関/専門性) × 文化ライブラリ × genome 進化からの分離 × on-prem 監査**
という**統合**と、「遺伝しない・平均を外れた個体が獲得・隔世で再覚醒」という単純で一般的な核の置き方。

## 7. 立項判断 / 次ステップ

- 当面スケルトンで保留。実装は **隔離 PoC**（persona ライブラリ stub + novelty×相関 matching pass +
  lleval rubric stub）から。
- 着手前に **rad-research（済: cultural/memetic/QD 確認）＋ TRIZ（持続 vs 自由探索の分離原理）＋
  cross-domain（書籍/芸術の文化伝達 → EC）** を正式に回して根拠を固める。
- 進化走行の安全弁（collapse guard / eval_timeout, [[project_llive_evolution_next_session]]）の上に乗せる。

## 8. PoC 設計（隔離・合成・falsifiable, 2026-05-24 着手合意）

**目的**: 核機構の feasibility と創発特性を、実 LLM・実 genome ループ無しで検証
（`feedback_poc_feasibility_first`: 要件→PoC→フィジビリティ）。**実社会との相似**
（親和/実力での文化継承・多才 hub・思想の休眠と隔世復活）が設計の妥当性の傍証
（`現実接続` 因子）。

**隔離**: standalone `scripts/demo_persona_fx.py`（stdlib+numpy, 決定論/seed）。
EvolutionLoop / genome に**非接触・無改修**。

**入力（合成）**: 集団 N 個体 × 10-dim factor ベクトル（思考因子の代用）/ persona プール
M × 10-dim affinity prototype（+任意 rubric weight）。

**機構**:
1. centroid → 各個体の逸脱度 = centroid 距離（novelty 代用）
2. eligible = 逸脱 top-p%（or しきい値）
3. 各 persona が独立に eligible との cosine 相関 → argmax（しきい値超）を bearer に
4. 記録: per-persona bearer / per-individual persona 数

**検証する falsifiable 主張（成功基準）**:
- **U** persona 側 uniqueness（各 persona ≤1 bearer）が常に成立
- **M** 個体多重が創発（0/1/≥2 混在）— 分布を出力
- **D（隔世）** スクリプト化世代列で「相関個体不在→休眠→後世で出現→再付与」を再現
- **H（退化診断）** 集団を centroid に潰すと 1 個体が多数 persona を総取り → 偏り指標が跳ねる
- **(stretch) E（多様性エンジン）** 付与=報酬で toy 選択を回すと、無報酬 baseline より逸脱多様性が維持される（核の非自明主張・重ければ次段）

**出力**: assignment 表 + 多重分布 +(stretch) 多様性時系列。honest: 合成 factor・proxy
報酬であり production 値ではない（mechanism feasibility のみ検証）。

**実装後の接続（PoC では stub）**: 逸脱→`NoveltyScorer` / 相関→`factor_affinity` / 報酬→`lleval`,`poc_lens`。

**規模**: ~1 ファイル ~150-250 行 + テスト。

## 関連
- [[project_llive_evolution_next_session]] — 進化基盤 (G1-G8 / turnkey / hang guard)
- [[project_poc_lens_lleval_integration]] — 眼鏡 (専門性判定器の流用元)
- [[project_hyperdimensional_thinking_seed]] — 非自明性テスト (偽の個性検出と同型)
- [[project_llive_reincarnation_rod_metaphor]] — 隔世＝転生メタファー
- [[project_llive_cog_fx_factors]] — 10 思考因子 (素養シグネチャの空間)
