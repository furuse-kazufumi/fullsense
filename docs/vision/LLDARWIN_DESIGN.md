# lldarwin — 選択圧コンポーネント 設計書 (2026-05-25)

> **位置づけ**: FullSense ll- ファミリーの新メンバー。**眼鏡 = lleval（評価）** が見た差を
> 「誰が生き残るか」に変換する **選択圧（淘汰）コンポーネント**。lleval が *測り*、lldarwin が
> *淘汰する* — この 2 段で初めて意味ある進化になる。
> **動機**: 進化ラン (rich-proxy, 500世代) で best=1.0 飽和 → 選択圧ゼロ → 遺伝的浮動で
> founder 8→2 系統 monoculture（"私と friston だけ"）。**選択圧の設計が進化の成否を決める**ことが実証された。
> **名前**: PyPI `lldarwin`/`llmesh-lldarwin` 空き・GitHub ZERO（2026-05-25 実測, [[llname_collision_audit_2026_05_24]]）。
> **方針 (ユーザー 2026-05-25)**: ①複数選択圧で淘汰（単一でない・多様な形）②LLM の苦手を重点的に
> ③全滅させる極端を避け世代を重ねても破綻しないバランス ④きっちり調べ上げて作り上げる。

## 1. 設計原則

1. **複数選択圧の多目的淘汰** — 単一スカラー fitness の argmax を禁止（旧 best=1.0 飽和の真因 = `fitness_rich` の `nearest=max(sims)` 単一化, 要件 SEL-2）。各個体は**複数の独立した選択圧（pressure）**で評価され、それらを集約せず個別に淘汰判定する。
2. **LLM/VLM の苦手を選択圧に** — 検証可能性のない領域でなく、LLM が現実に弱くかつ測定可能な軸を選ぶ（差別化軸 DIFF-1）。
3. **破綻しないバランス** — 世代 t→∞ でも単一最適へ凝集しない多層の多様性圧。全滅を構造的に不可能化。
4. **拡張可能な評価軸カタログ** — pressure はプラグイン。軸の追加が容易（ユーザーが次々追加する設計指示を吸収）。
5. **proxy/実評価の分離** — proxy で測れる軸（mechanism feasibility）と実 LLM/VLM 必須の軸（Stage 後半）を明示分離（測定純度）。

## 2. アーキテクチャ — multi-pressure selection

```
個体 ──▶ [lleval=眼鏡] ──▶ pressure profile (複数軸の case ベクトル)
                                  │
                                  ▼
        ┌──────────── lldarwin（選択圧 = 淘汰変換）────────────┐
        │ (1) Standardizer       : per-dim z-score (STD-1, 中央一致除外)
        │ (2) MinimalCriterionGate: 各軸の最低基準で繁殖可否 (SEL-4, 全滅回避)
        │ (3) EpsilonLexicaseSel  : 軸を case として1つずつ独立評価 (SEL-3, specialist保存)
        │ (4) QD/MAP-Elites archive: pressure profile を behavior 記述子に cell別 elite (構造的全滅不可)
        │ (5) Niching/FitnessShare: 多峰並存 (monoculture 抑制)
        │ (6) Down-sampling       : 毎世代 case 部分集合で環境かく乱 (plateau 破壊)
        │ (7) NoveltyScorer       : 停滞時の探索圧 (枯渇回避)
        └────────────────────────────────────────────────────┘
                                  │
                                  ▼
                          次世代の親選択
```

**集約しない設計が核**: (3) ε-lexicase は軸を集約せず1つずつ順に評価するため、ある軸で突出した
specialist（他軸で平凡）が生存できる＝多極構造を自動維持。(4) QD は behavior 次元で cell 別 elite を
保持し「1 cell でも残れば全滅しない」最小多様性を保証。(2) minimal-criterion は連続順位だけで
決めず「最低基準を満たすか」で繁殖可否を分け、退化・偽 novelty を排除しつつ全滅も防ぐ。

**根拠（rad-research 2026-05-25）**: ε-lexicase + minimal-criterion QD + down-sampling の3層が
「世代を重ねても破綻しない」最有力融合案（evolutionary_computation コーパス616件横断）。
- ε-lexicase の specialist 保存 = La Cava 2019 (arXiv 1905.13266) / 高 population diversity (2204.06461)
- QD/MAP-Elites の cell 別全滅不可 = Fontaine CMA-ME 2019 (1912.02400) / MNSLC 2024 最効果 ([GECCO 2024](https://dl.acm.org/doi/10.1145/3638530.3654099))
- down-sampling の環境かく乱 = Helmuth & Spector 2021 (2106.06085)
- island + extinction/repopulation = Lyu 2020 (2005.07376, NEAT speciation 超え) ← 将来オプション

## 3. 評価軸カタログ（pressure プラグイン, 拡張可能）

各 pressure は `Pressure` インターフェース（`name`, `evaluate(individual_output) -> case_scores: list[float]`,
`is_proxy: bool`, `minimal_criterion: float|None`）で実装。**lleval が測定器、lldarwin が淘汰器**。

| pressure | LLM/VLM の苦手 | 測定法 | proxy/実 | 根拠 |
|---|---|---|---|---|
| **typo_robustness** | 誤字脱字・ノイズ入力への耐性/予測（ユーザー指示） | keyboard-typo perturbation で出力一貫性 (perturbation consistency) | **proxy可**（合成 typo 注入） | arXiv 2510.09536 / 2407.08989 / 2505.18658 |
| **polysemy_wsd** | 多義語の文脈依存理解（ユーザー指示。post/bat 等 10+ senses） | WSD accuracy（gold sense との一致, DiBiMT 型 multiple-choice） | **proxy可**（WSD bench） | arXiv 2411.18337 / 2503.08662 / DiBiMT |
| **visual_qa** | 画像認識「これは何の絵か」/ visual hallucination / text-prior bias（ユーザー指示） | VQA accuracy / fine-grained spatial / modality ablation | **実VLM必須**（on-prem llava 等, Stage後半） | CreativityBench系 / 2510.20696 |
| **multistep_robustness** | cascade error / 状態追跡 / info-flow degradation | per-step correctness + cascade ratio + trace length | **proxy可**（構造化タスク） | 2604 / 2511.21591 / 2402.08115 |
| **calibration** | 信頼度推定（token-level confidence ≈ random） | ECE / Type-2 AUROC / Brier | **proxy可**（single or light multi-sample） | 2604.19444 / 2604.24070 |
| **faithfulness** | CoT の最終答への忠実性 / grounding | entailment（think-answer/info-think）+ groundedness | **hybrid**（proxy+LLM-judge, bias注意） | 2510.13272 / 2604.23366 |
| **ood_generalization** | 分布外汎化（RLHF が OOD を下げる） | robustness gap = IID − OOD accuracy | dataset依存（proxy有効だが構築コスト） | 2310.06452 |
| **context_management** | 無関係文脈で reasoning 劣化（Reasoning Shift） | trace length ratio（clean vs augmented）+ 汚染耐性 | controlled test（proxy可） | 2604.01161 |

> **拡張方針**: 新しい pressure はこのカタログに行を足し、`Pressure` 実装を追加するだけ。
> ユーザーが追加する軸（今後）はここに吸収する。proxy 軸を先に PoC、実 LLM/VLM 軸は Stage 後半。

## 4. 破綻回避バランス（世代を重ねても全滅しない保証）

今回の monoculture（8→2）を反証する多層構造:
1. **MinimalCriterionGate (SEL-4)**: 連続順位でなく最低基準で繁殖可否 → 一強総取りを抑制。
2. **QD cell 別 elite (QD-1/2)**: behavior cell ごとに elite 保持・単調成長 → 1 cell でも残れば系統全滅不可。
3. **Niching/FitnessSharing**: 同 niche の fitness を down-weight → 多峰並存。
4. **Down-sampling**: 毎世代 case 部分集合 → moving target で plateau 破壊・特定 peak 依存を阻止。
5. **per-dim z-score (STD-1) + 中央一致除外 (SEL-1)**: 「全軸平均高」= 無特徴を優位にしない、逸脱を選択圧に。
6. **monoculture モニタ + SPC**: max_lineage_share / archive growth / behavioral diversity を毎世代記録、
   閾値（OE-3: <0.8）超過を SPC_ALARM（FullSense 中核）で検知 → cadence/パラメータ自動調整。

## 5. 既存資産と新規部品（codex コード調査 2026-05-25 ベース）

**再利用（差し替え注入可能, `EvolutionLoop.selection: Callable[[Population, rng], Individual]`）:**
- `mating.py:139 LexicaseSelection`（ε付き, **実装済だが未配線** → 配線するだけ）
- `nsga2.py:197 NSGA2Selection`（多目的, ≤3目的レーン用）
- `diversity.py:94 NoveltyScorer`（k-NN novelty）
- `quality_diversity.py MAPElitesGrid`（QD archive）
- `speciation.py SpeciationLayer`（要オーケストレーション補強）

**新規実装:**
- `Standardizer`（per-dim z-score, STD-1）
- `MinimalCriterionGate`（SEL-4）
- `Pressure` インターフェース + 各評価軸（typo/polysemy/multistep/calibration/context は proxy、visual_qa/faithfulness/ood は実評価）
- `MultiPressureSelector`（pressure profile → ε-lexicase 主選択 + QD archive 並行更新を束ねる lldarwin の中核）
- `SelectionAudit`（§2 メトリクス毎世代記録 + SPC 連携）

**配線点:**
- `loop.py:122` の `selection` に `MultiPressureSelector` を注入
- `loop.py:203/246` `on_generation_end` で z-score 統計 / criterion 閾値 / 監査ログ更新
- `persona_evolution.py:606` は `selection` を loop に渡していない → **注入口の追加が必須**

## 6. PoC 段階計画（feasibility → 本実装）

- **Stage 0（proxy のみ）**: typo_robustness + polysemy_wsd + multistep + calibration + context を proxy で実装。
  既存 LexicaseSelection 配線 + Standardizer + MinimalCriterionGate + QD archive。
  → **進化を再ラン**し「岡潔・グロタンディークらが生き残るか（系統多様性が維持されるか）」を §4 メトリクスで検証。
  今回の 8→2 monoculture が改善するかが第一の合否。
- **Stage 1**: niching/down-sampling 追加、sweep（選択圧の組合せ × 強度）。
- **Stage 2（実評価軸）**: visual_qa（on-prem VLM）/ faithfulness（LLM-judge）/ ood を追加。実 LLM/VLM 前提（ollama)。

## 7. honest disclosure / リスク

- **proxy 軸の妥当性**: typo/polysemy/multistep の proxy は mechanism feasibility 検証であり、production の
  LLM 能力を直接測るものではない（実 LLM/VLM 評価は Stage 2）。
- **多目的の呪い**: 軸を増やしすぎると ε-lexicase でも選択が弱まる。NSGA-II は ≤3 目的レーンのみ（many-objective 回避）。
- **VLM コスト**: visual_qa は実 VLM 推論が毎評価で要る → 評価予算大。surrogate-assisted で間引く（Stage 2）。
- **LLM-judge bias**: faithfulness の LLM-judge は bias リスク → multiple-judge ensemble + human validation baseline。
- **個体が "LLM" でない段階**: 現進化個体は llive 構成 genome（Genome3D）であり実 LLM そのものではない。
  proxy 軸は genome の振る舞い代理を測る。実 LLM/VLM 能力の選択圧は個体→実モデル写像（Stage 2 の課題）。

## 8. 出典
- 設計動機: 進化ラン evo_seekvalue_2026_05_25 / [[evolution_viz_viewing_guide_2026_05_25]] / [[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] §1.1 SEL-1..4
- 破綻回避: rad-research 2026-05-25（evolutionary_computation 616件）+ MNSLC GECCO 2024 / CMA-ME 1912.02400 / down-sampled lexicase 2106.06085
- LLM 苦手: rad-research（llm/agents/neural_network v2）+ self-verification 2402.08115 / planning 2511.21591 / typo 2510.09536 / WSD 2411.18337
- 既存資産: codex コード調査 2026-05-25（loop.py/mating.py/nsga2.py/diversity.py/quality_diversity.py/speciation.py/persona_evolution.py）
