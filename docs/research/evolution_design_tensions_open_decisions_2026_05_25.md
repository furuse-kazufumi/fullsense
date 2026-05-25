---
layout: default
title: "進化設計の緊張関係と未解決決定 (tensions & open decisions)"
parent: "Research"
nav_order: 98
---

# 進化設計の緊張関係 & 未解決決定 (2026-05-25)

> 要件 [[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] が「まとまった」と言えるために潰すべき
> **矛盾(tension)の解決方針**と**実装前に確定すべき決定([SPEC])**を可視化する思考メモ。
> honest disclosure: ここは「考え中」の正直な棚卸し。確定は要件本体へ昇格させる。

## 1. 緊張関係(tension)と解決方針

| # | 緊張 | 解決方針 |
|---|---|---|
| **T1** | token 級ゲノム(32K)×pop1024×float ≈ 130MB+/snapshot。CKPT-1 全状態を頻繁に書くと重い | **疎/差分/圧縮チェックポイント**: c_latent は疎変異(5%)ゆえ**世代間 delta** が小さい→delta+gzip。population 全体は checkpoint_every を粗く(500–1000)。archive/belief は別ファイル追記。**CKPT コスト予算**を設け per-gen 時間を圧迫しない |
| **T2** | 5h+ 長ラン vs 高速 PDCA(Check を回したい) | **Check を run 終了でなく中間で**: metrics を毎世代/チェックポイント毎にストリーミング集計(既存 metrics.jsonl 方式)。改良 side(コード/config)は run と**並行**(両輪 Do)。CADENCE-1 が比率を適応 |
| **T3** | novelty(発散) vs minimal-criterion(可生存) | **MC=床(gate)、novelty=床の上の勾配**(SEL-4/R-PEC-3 で既定)。MC 単独は制約過多、novelty 単独はノイズ→併用 |
| **T4** | proxy で「新しい AI が生まれる」と言えるか | **言えない(過剰主張禁止)**: proxy PoC は「**環境が open-ended 多様性を持続できる機構実証**」まで。真の「新 AI=知能」は **Stage6 実 LLM in the loop** 必須(「知能への踏み石は知能的でない」Stanley)。受入は proxy=機構, real=知能 と二段で正直に分離 |
| **T5** | メタ進化(#12) が自らのガバナンス(#13/SR-3)を進化で迂回しうる | **メタ進化を「検証済み演算子/パラメータの選択進化」に限定**(任意コード生成=R 型自己書換は SCOPE-2 で土俵外)。evolvable なのは vetted operator library からの選択 + 数値パラメータのみ→**ガバナンスは到達不可能な集合の外**(SR-3) を保つ。「制約は知覚・到達できなければ最適化で消せない」 |
| **T6** | 大 pop × token ゲノム × novelty k-NN = 計算量 | **低次元記述子(DESC-1, JL 射影)で k-NN tractable** + **sep-CMA(対角)で高次元 σ** + numpy vectorize。QD archive は cell 数上限 + LRU/elite 保持で有界化 |
| **T7** | 人間文化因子(Hofstede/Schwartz/WVS)の妥当性(Stream D: metaphor で測定的接地でない) | **価値は「対立対という構造」**(openness↔conservation 等→全因子満点が幾何的に不能→多様性源)。**人間意味の正確さではなく構造的性質で正当化**。人間ラベルは解釈の補助であって主張の根拠でない。circular-consistency テストで gross 破綻のみ検出 |
| **T8** | 「規模を上げれば質的変化」仮説が外れる可能性 | falsifiable に: 4 軸スケールしても Bedau で bounded のままなら**仮説反証**→規模でなく機構(選択/記述子)が律速と判断し方針転換(honest, 3 回失敗で転換則) |

## 2. 実装前に確定すべき未解決決定 ([SPEC] / sweep で決める)

| # | 決定事項 | 方針 |
|---|---|---|
| **D1** | reservoir サイズ + 疎度(多様性持続の主制御) | sweep {256,1024,4096,32768}×{0.02,0.05}; 10K 世代末尾の多様性で決定 |
| **D2** | 記述子: JL 射影次元(8–50?) / 学習記述子(AURORA)を使うか | まず JL 固定次元(決定論・再現性) → AURORA は stretch A/B |
| **D3** | QD archive: CVT-MAP-Elites / grid / Dominated Novelty Search、cell 数 | CVT を本命、DNS を A/B、cell 数は pop と釣り合わせ |
| **D4** | ε-lexicase: epsilon(static/semi-dynamic) + 「ケース」の定義 | ケース = per-archetype 類似 + per-cultural-axis + 安全 audit; ε は semi-dynamic(MAD ベース) |
| **D5** | belief space: 知識源 + acceptance/influence 関数 | normative/situational/temporal の 3 源, acceptance=payoff-biased top-p%, influence=変異パラmeterバイアスのみ(Baldwinian) |
| **D6** | persona プール構成(誰を何体) + 相関/uniqueness 操作化 | 既存 8 founder + 拡張; 相関=拡張空間 cosine, per-persona argmax(PERSONA-FX 核) |
| **D7** | チェックポイント形式 + コスト予算(T1) | delta+gzip, 別ファイル(pop/archive/belief/metrics), per-gen 時間の <X% を予算 |
| **D8** | メタ進化エンベロープ(evolvable な operator/param の vetted 範囲, T5) | operator library を列挙し**その選択のみ** evolvable; コード生成は不可 |
| **D9** | 校正ラン(calibration)パラメータ | 小〜中規模で per-gen 実測 → 5h window を埋める本番規模を算出 |

## 3. 「まとまった」判定 = 要件サマリ化のトリガ
- 上記 T1–T8 の解決方針が要件本体に反映され、D1–D9 が「sweep で決める/初期値」まで落ちていること。
- Stream H(llove Qt 可視化)着地で可視化要件が埋まること。
- → 揃ったら **要件サマリ(1 枚)** を作る(ユーザー: 「まとまったら要件をまとめましょう」)。

## 関連
- [[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] / [[OPEN_ENDED_CULTURAL_EVOLUTION]] /
  [[evolution_poc_experiment_design_2026_05_25]] / 研究 A–H findings docs /
  [[feedback_benchmark_honest_disclosure]] / [[feedback_poc_feasibility_first]]
