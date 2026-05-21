---
layout: default
title: "LLM × Evolutionary — Prior Art Survey"
parent: "Research"
nav_order: 7
---

# LLM × Evolutionary Algorithms — Prior Art Survey

> 2026-05-21 作成. **llive v0.B/v0.C (集団 GA × 19 dim genome × subprocess
> transport) と類似する先行研究**を整理した. 同領域は 2023〜2026 で急速に
> 立ち上がっており, llive の **どの軸が既存と重なり, どこで差別化できるか**
> を把握するための資料.

## 0. なぜこの survey が必要か

ユーザー指示 (2026-05-21): 「LLM に進化的形質を持たせるとか, 既に研究と
して存在してるかもしれないので, 適度に情報収集も進めておいて下さい」.

llive 側で実装したもの:

- **v0.B**: hyperparameter 進化 (UCB1 + Hebbian) + 5 backend Genome PoC
  ([`src/llive/perf/evolutionary/`](https://github.com/furuse-kazufumi/llive/tree/main/src/llive/perf/evolutionary))
- **v0.C**: 1 llive = 1 個体の **派生集団進化** (19 dim genome × 5 chromosome ×
  SegmentCrossover, checkpoint/resume/budget)
  ([`src/llive/perf/evolutionary/llive_variant.py`](https://github.com/furuse-kazufumi/llive/blob/main/src/llive/perf/evolutionary/llive_variant.py))
- **Phase 2 subprocess transport** (本日着地): `VariantSubprocessScheduler`
  ([`src/llive/perf/evolutionary/subprocess_scheduler.py`](https://github.com/furuse-kazufumi/llive/blob/main/src/llive/perf/evolutionary/subprocess_scheduler.py))
- **lineage (LV-10)**: 系統樹 Mermaid 可視化
- **bridges/llive**: Genome → lleval Config bridge

これらと類似 / 重複 / 補完関係にある研究を, **RAD コーパス**横断検索と
WebSearch で抽出した. (memory `feedback_rad_rag_confusion` の呼称ルールに
従い「RAD コーパス」と表記.)

## 1. SOTA matrix — 主要 9 研究

時系列順. **「LLM が何の役を演じるか」**で 4 タイプに分ける:

- **(P) Prompt/Code 進化**: LLM が生成した文字列・コードを GA で進化
- **(O) Operator**: LLM 自体が crossover / mutation 役 (genotype → genotype 変換)
- **(S) Surrogate**: LLM が EA の代理評価器 (expensive evaluation の置換)
- **(M) Meta**: LLM が EA の戦略・パラメータを決める

| 研究 | 出典 | 役 | コア手法 | llive との関係 |
|---|---|---|---|---|
| **LMX** (Meyerson et al.) | [arXiv:2302.12170](https://arxiv.org/abs/2302.12170) (2023-02, ACM TELO 2024) | O | Few-shot prompting で genotype の crossover. binary 文字列・数式・英文・コードに汎用. | llive `SegmentCrossover` は数値 genome 限定. LMX は **テキスト genome** で動く. **将来 llive の thought_factor を自然言語化すれば LMX が直接効く**. |
| **EvoPrompt** (Microsoft) | [arXiv:2309.08532](https://arxiv.org/abs/2309.08532) (2023-09), [GitHub](https://github.com/microsoft/EvoPrompt) | P+O | LLM × EA で離散プロンプト最適化. GA / DE を選択. GPT-3.5 / Alpaca で human prompt を最大 25% 超え. | llive v0.B+ の hyperparameter 探索とは object が違う (prompt vs 数値). **prompt 軸を genome に追加するなら参考実装**. |
| **Promptbreeder** (DeepMind) | [arXiv:2309.16797](https://arxiv.org/abs/2309.16797) (2023-09) | P+M | Self-referential: **mutation prompt 自体も進化させる**. Chain-of-Thought / Plan-and-Solve を上回る. | llive `mutation.py` (GaussianMutation, ResetMutation) は静的. **mutation 自体を進化させる self-referential layer** は llive 未実装. 差別化候補. |
| **EUREKA** (NVIDIA) | [arXiv:2310.12931](https://arxiv.org/abs/2310.12931) (2023-10), [project](https://eureka-research.github.io/) | P+M | RL の reward function を LLM が code として書き, GPU 並列 evaluation で進化. 29 環境で human expert 83% 超え. | llive `mock_variant_fitness_factory` は static 5 軸 mock. **EUREKA は fitness 関数自体を進化**. llive で fitness を LLM 生成にする選択肢あり (要 credential). |
| **FunSearch** (DeepMind) | [Nature 2024](https://www.nature.com/articles/s41586-023-06924-6), [DeepMind blog](https://deepmind.google/blog/funsearch-making-new-discoveries-in-mathematical-sciences-using-large-language-models/) | P+S | Frozen LLM + evaluator の組合せ. online bin packing で **未解決問題に新発見**. 「program search」志向. | llive v0.C は派生 **構成** の進化. FunSearch は **プログラム** の進化. 違う object だが evaluator + checkpoint resume の設計は近い. |
| **LLMize** (Oktavian) | [arXiv:2601.00874](https://arxiv.org/abs/2601.00874) (2025-12) | P+M | OPRO + EA hybrid. 自然言語で制約 / heuristic を注入できる. neural net hyperparameter tuning / TSP / 核燃料格子最適化. | llive 「constraint = bounds」「heuristic = TRIZ 40 原理」と類似. **自然言語制約 injection** は llive 未実装. |
| **MASPO** | [arXiv:2605.06623](https://arxiv.org/abs/2605.06623) (2026-05) | P | LLM-based MAS の prompt を **joint 最適化**. Data-driven evolutionary beam search. 6 task で 2.9% 改善. | llive v0.C の「複数派生が役割分担しつつ共同で best 構成を探す」と概念近い. **multi-agent role-specific genome** は将来候補. |
| **MappingEvolve** | [arXiv:2604.26591](https://arxiv.org/abs/2604.26591) (2026-04) | P+M | Logic synthesis の technology mapping を **Planner / Evolver / Evaluator** の階層 agent で進化. ABC ベースで 10.04% area reduction. | llive v0.C の **3 階層 (variant_runner / scheduler / EvolutionLoop)** と構造が酷似. **bridges/llive の Planner 役を LLM 化すれば MappingEvolve 相当**. |
| **R2SAEA** | [arXiv:2605.02933](https://arxiv.org/abs/2605.02933) (2026-04) | S | LLM (Qwen2.5 + GRPO fine-tune) を **surrogate model** 役で使う SAEA. anchor-based pairwise reasoning で prompt complexity を O(n²) → O(n). | llive `_serial_scheduler` / `VariantSubprocessScheduler` は本物の評価. **expensive evaluation を LLM surrogate で置換** は llive 未実装の高速化候補. |

### Survey (2026 最新)

- [arXiv:2509.08269](https://arxiv.org/html/2509.08269v1) — **A Systematic Survey on
  Large Language Models for Evolutionary Optimization: From Modeling to Solving**
  (2026-09). 本ドメインの体系的サーベイ. llive 系研究の位置づけを確認する一次資料.
- [arXiv:2401.10510](https://arxiv.org/html/2401.10510v2) — *When large language
  models meet evolutionary algorithms* (2024-01). 初期サーベイ.

## 2. llive との overlap / 差別化

### 2.1 overlap (既存研究が先行している領域)

| llive 軸 | 先行する研究 | 状況 |
|---|---|---|
| 集団 GA × LLM-related genome | EvoPrompt / Promptbreeder / FunSearch | 2 年以上の先行. genome の "object" は違うが **GA loop の骨格**は同型. |
| 階層 agent (Planner/Evolver/Evaluator) | MappingEvolve | 構造が直接対応. llive `variant_runner` ↔ Evaluator. |
| Multi-objective fitness | EUREKA / R2SAEA / EvoPrompt | mock fitness 軸 (latency/quality/safety/...) は標準的. |
| Checkpoint + resume | (該当する公開実装は希) | FunSearch が暗黙にやっている程度. **llive `EvolutionConfig.resume_from` は明示 API として珍しい**. |

### 2.2 差別化候補 (llive が先行 or 未実装で差別化可能)

| 差別化軸 | 状況 | 根拠 |
|---|---|---|
| **on-prem LLM backend での集団進化** | 先行例ほぼ無し. EUREKA は GPT-4, FunSearch は PaLM/Codey, EvoPrompt は GPT-3.5/Alpaca. **on-prem (llama-server / RWKV.cpp) で集団規模 30+ × 30 世代を回す実装**は未見. | memory `feedback_llive_measurement_purity` の方針が直接効く. |
| **19 dim 数値 genome + 5 chromosome SegmentCrossover** | 先行例は **prompt 文字列** か **program code** が主. **数値 thought_factor + memory threshold + backend + sampler + proactive を 1 genome に束ねた構成** は llive 独自. | llive `LIVE_VARIANT_GENOME_BOUNDS` の 19 dim は他に類例なし. |
| **subprocess transport で派生プロセス隔離** | 公開実装で fault isolation / data_dir 隔離まで設計に入れたものは少ない. | llive `VariantSubprocessScheduler` の `cleanup` / `retries` / `fail_on_error` / `timeout_sec` は production-ready. |
| **honest disclosure 5+1 因子分解** | (該当研究なし) | lleval `analyzer/honest_disclosure.py` の 5 因子 + mock baseline policy は llive エコシステム独自. |
| **Self-referential mutation (Promptbreeder 型)** | Promptbreeder が先行. llive 未実装. **mutation 自体を genome に入れる** 拡張案. | 検討余地あり. 数値 mutation σ を genome dim に入れれば self-adaptive ES に近い. |
| **LLM-as-surrogate (R2SAEA 型)** | R2SAEA が直近 先行. llive 未実装. expensive evaluation の置換に有効. | credential 復旧後に検討. |

### 2.3 「ない論文」(意識的に探した未踏)

- **集団進化 × Approval Bus / HITL ループ** — Genome の評価結果を HITL で承認する研究は未見. llive `approval/` を組み合わせると差別化軸になる.
- **集団進化 × on-prem only での経時 (週単位) 運用** — Checkpoint resume を前提に「セッション切れごとに世代を進める」運用パターンの研究はほぼなし. llive v0.C の `EvolutionConfig(max_wallclock_seconds, resume_from)` が直接実装.
- **Genome に **思考因子 weight** を含める** — 心理モデル由来の 10 思考因子 (構造化/再構成/閉ループ/...) を GA 上で最適化する研究は未見. llive `THOUGHT_FACTOR_LABELS` 由来.

## 3. 実装インスピレーション (取り込み候補)

優先度高 (HIGH):

1. **Self-referential mutation** (Promptbreeder 由来) — `GaussianMutation` の σ を **genome dim に含める** ことで self-adaptive ES に相当. 19 dim → 20-22 dim 程度の拡張.
2. **LMX による genome 自然言語化** — 思考因子 weight を「重視する思考の傾向 (自然言語記述)」として保持し, LMX が crossover を担う. 数値 genome と並走可能 (hybrid genome).
3. **R2SAEA の LLM-surrogate** — 実 LlivKernel 評価が 5 分 × 30 体 × 30 世代 = 75 時間 のとき, LLM surrogate で 1 桁短縮.

優先度中 (MID):

4. **MASPO の multi-agent role-specific genome** — 派生群を 3-5 roles に分けて role 固有の genome 軸を持つ. llive 'multi-llive collaboration' 構想と連動.
5. **EUREKA の reward (fitness) 関数 LLM 生成** — `mock_variant_fitness_factory` の代わりに LLM が code として fitness 関数を書く.

優先度低 (LOW / 後追い OK):

6. **MappingEvolve の Planner agent** — Evolver/Evaluator は既に llive で対応済. Planner 役 (世代戦略を決める LLM) は将来検討.

## 4. 教訓 — 「全て前例あり」ではない

整理した結果 llive の **9 軸中 4 軸 (on-prem 集団進化 / 19 dim 数値 genome /
subprocess transport / honest disclosure)** は公開研究で類例が見当たらない.
逆に **集団 GA × LLM** という大枠は EvoPrompt / Promptbreeder / FunSearch
で 2 年以上の先行があり, 「枠組み発明」を主張するのは無理がある.

**正しい立場:**

- 「llive は LLM × 集団進化を **on-prem に降ろした実装**」と位置づける.
- 既存研究を引用しつつ「実装パターン (subprocess transport / checkpoint
  resume / honest disclosure)」を差別化軸とする.
- 論文化するなら **比較対象** を [arXiv:2509.08269 survey](https://arxiv.org/html/2509.08269v1) からピックアップする.

memory [[feedback-benchmark-honest-disclosure]] の精神でいくと, 「LLM ×
evolution の枠組みが先行している」事実は最初に明記し, **「llive 固有の
4 軸」だけを差別化軸として打ち出す**のが honest.

## 5. References

### 直接関連 (arXiv / Nature / Microsoft / DeepMind / NVIDIA)

- Meyerson, E. et al. (2023). [Language Model Crossover: Variation through Few-Shot Prompting](https://arxiv.org/abs/2302.12170). arXiv:2302.12170. (ACM TELO 2024)
- Guo, Q. et al. (2023). [EvoPrompt: Connecting LLMs with Evolutionary Algorithms](https://arxiv.org/abs/2309.08532). arXiv:2309.08532. (Microsoft)
- Fernando, C. et al. (2023). [Promptbreeder: Self-Referential Self-Improvement Via Prompt Evolution](https://arxiv.org/abs/2309.16797). arXiv:2309.16797. (DeepMind)
- Ma, Y. et al. (2023). [Eureka: Human-Level Reward Design via Coding Large Language Models](https://arxiv.org/abs/2310.12931). arXiv:2310.12931. (NVIDIA)
- Romera-Paredes, B. et al. (2024). [Mathematical discoveries from program search with large language models (FunSearch)](https://www.nature.com/articles/s41586-023-06924-6). *Nature*. (DeepMind)
- Oktavian, M. R. (2025). [LLMize: A Framework for LLM-Based Numerical Optimization](https://arxiv.org/abs/2601.00874). arXiv:2601.00874.

### 2026 最新 (RAD コーパス ヒット)

- Lu, Y. et al. (2026). [Relation Reasoning with LLMs in Expensive Optimization (R2SAEA)](https://arxiv.org/abs/2605.02933). arXiv:2605.02933.
- Fu, R. et al. (2026). [MappingEvolve: LLM-Driven Code Evolution for Technology Mapping](https://arxiv.org/abs/2604.26591). arXiv:2604.26591.
- Wang, Z. et al. (2026). [MASPO: Joint Prompt Optimization for LLM-based Multi-Agent Systems](https://arxiv.org/abs/2605.06623). arXiv:2605.06623.

### Surveys

- [arXiv:2509.08269](https://arxiv.org/html/2509.08269v1) — A Systematic Survey on LLMs for Evolutionary Optimization (2026-09).
- [arXiv:2401.10510](https://arxiv.org/html/2401.10510v2) — When LLMs meet Evolutionary Algorithms (2024-01).

### llive 内部 cross-reference

- [`docs/requirements_v0.B_evolutionary_optimization.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.B_evolutionary_optimization.md)
- [`docs/requirements_v0.C_llive_variant_evolution.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.C_llive_variant_evolution.md)
- [`docs/experiments/llive_variant_v0_C_2026_05_21.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/experiments/llive_variant_v0_C_2026_05_21.md)
- [`src/llive/perf/evolutionary/subprocess_scheduler.py`](https://github.com/furuse-kazufumi/llive/blob/main/src/llive/perf/evolutionary/subprocess_scheduler.py) (2026-05-21 着地)

### 関連 maintainer memory

- [[feedback-llive-measurement-purity]] — on-prem 限定の測定純度
- [[feedback-benchmark-honest-disclosure]] — 異常に良い結果は内訳を疑う
- [[feedback-rad-rag-confusion]] — RAD コーパス vs RAG vs RAD₂
- [[feedback-research-first]] (implicit) — 着手前にまず先行研究

## 6. 次アクション

- [ ] [arXiv:2509.08269 survey](https://arxiv.org/html/2509.08269v1) を精読 → llive の位置づけを論文化のとき引用
- [ ] [[project-llive-v0B-evolutionary]] 系の memory に「先行研究 9 件あり」を追記
- [ ] Self-referential mutation (Promptbreeder) を `requirements_v0.D` 候補として登録 (将来)
- [ ] credential 復旧後, LLM-as-surrogate (R2SAEA) PoC を検討
