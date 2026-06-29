# 脳構造を目指す FullSense — マッピング・ブリーフィング(ruthless honesty)(2026-06-29)

> **provenance**: 検証ワークフロー `brain-structured-fullsense` (w2li8t45p, 7 agents / 88 tool uses / ~16 min)。
> 6 脳組織原理(CLS / 予測符号化 / 皮質特化+視床ルーティング / Global Workspace / 疎符号化+neuromodulation / sleep-replay)を FullSense アーキに具体マッピング → 機構 vs 比喩を冷徹に仕分け。neuroscience + comp-neuro + ML 文献接地。
> **接続**: memory `project_fullsense_unified_model_vision`(北極星)/ `model_fusion_landscape_2026-06-29.md`(融合手法)/ `option_b_verification_poc1_novelty_2026-06-29.md`(P7 天井 = Schlag fast-weight 容量限界)。
> **規律**: `feedback_benchmark_honest_disclosure`(脳インスパイアは hand-waving の墓場 → 衣装を殺す)。

**一行の主題**: 6 原理を脳の衣装を剥いで並べると、実体は **4 つの ML 機構**に縮約 — ① 誤差訂正(delta-rule)有界状態書込、② 疎/準直交キー、③ オフライン interleaved replay-蒸留 consolidation、④ 有界 shared-workspace ボトルネック。**①②は既に llcore の Qwen3-Next ベース(Gated DeltaNet 3:1 hybrid)に在る**。④は orchestration 専用で north star に直交。**「脳構造を目指す」が FullSense に与えた、まだ使っていない唯一の追加機構は ③(sleep/consolidation を multi-teacher fusion に適用)だけ。**

---

## 1. ★mechanism vs metaphor の仕分け(衣装殺し)

| principle | grade | 一行 engineering payoff |
|---|---|---|
| **sleep-replay** | **concrete_mechanism** | 唯一の「まだ使っていない」レバー。offline interleaved replay-蒸留 consolidation = 多教師を catastrophic forgetting なしで単一 constant-state へ融合し state 利用率も上げる(DER++/生成 replay/「Do LMs Need Sleep?」で測定済 +9〜10%)。 |
| **cls** | partial(構造 concrete / fusion aspirational) | 3-store 構造 +「1 枚の重み行列に詰め込めない」NECESSITY 論証 = llive 外部ストアの存在を強制。実態は sleep-replay の静的双子。fusion 自体への直接レバーは無い。 |
| **sparse-neuromod** | partial(疎キー concrete / neuromod=gating は none) | 疎/準直交キーが crosstalk を下げ固定 state バイト当たりの recoverable binding を増やす(P7 への実レバー、純 numpy 最安)。「neuromod=context-gating」は既存 data-dependent gate の改名=none。 |
| **predictive-coding** | partial(delta-rule concrete だが既にベース内 / 皮質階層 metaphor) | error-correcting 書込(delta rule)+surprise スカラ = 実機構。だが **Gated DeltaNet として既に llcore ベースに在る**=採用対象。cortical hierarchy / PC-as-backprop = metaphor。 |
| **cortical-routing** | partial(価値は guardrail=負の知見) | 正味 payoff は**否定知**: resident MoE を**棄却せよ**(experts 常駐=メモリ非節約・反 fusion、Mixtral-8x7B ~94GB)。正の selective gating は delta-rule gate と冗長。 |
| **global-workspace** | **metaphor_only**(2 north star に対して) | fusion=none、constant-state=解釈のみ。唯一の実機構(有界 M-slot ボトルネック)は llive orchestration にしか効かず、しかも古典 blackboard(Hayes-Roth 1985)。衣装。 |

**冷徹な要点**: concrete_mechanism は **sleep-replay の 1 本のみ**。cls は同じものの静的記述で実質一体。predictive-coding / sparse-neuromod の concrete 部分は既にベースに在るか疎キー 1 レバーに縮む。cortical-routing の価値は「作るな」guardrail。global-workspace は costume。

---

## 2. ★concrete だけ残した時のアーキ素案(diagram-in-prose)

```
                    ┌──────────────────────────────────────────────┐
   WAKE(online)     │  llive = 海馬 / episodic store(4層メモリ)    │
   入力・教師I/O ──► │  疎・1-shot書込・pattern-separated・retrieval │  ← HippoRAG 写像
                    │  rare/teacher-specific fact はここに残す      │
                    └───────────────┬──────────────────────────────┘
                                    │ surprise scalar ‖v−Sk‖ が
                                    │ write/promote gate(高=長期へ昇格, 低=減衰)
                                    ▼
        ┌───────────── SLEEP(offline consolidation stage) ──────────────┐
        │  ・頻繁retrieveされた llive episode を replay                   │
        │  ・記録済み teacher logit(Qwen / GLM-MIT)を replay             │ ← DER++ logit-replay
        │  ・両者を INTERLEAVE して蒸留(generative + dark replay)        │   = distillation-as-replay
        │  ・Approval Bus gate: 教師Aのforgettingが悪化したら昇格をblock │   (fail-closed)
        └───────────────────────────┬──────────────────────────────────┘
                                    ▼
                    ┌──────────────────────────────────────────────┐
   constant state   │  llcore = 新皮質 / 遅い意味重み(有界 state)  │
   (per-token,      │  delta-rule(誤差訂正)書込 ＋ 疎/準直交キー     │  ← Gated DeltaNet(既にベース)
    working memory) │  = bindings/byte 最大化、Schlag 容量上限=P7   │     ＋ 疎キーで crosstalk 低減
                    └──────────────────────────────────────────────┘
```

**★重要な訂正(初期マッピングの反転是正)**: 「llcore 定数状態=海馬 / llive=皮質」は**部分的に逆**。正しい 3-store = 新皮質(遅い semantic)= **llcore 学習済み重み** / 海馬(速い episodic・疎・one-shot)= **llive 外部メモリ**(HippoRAG) / working memory(第3 store)= **llcore 定数状態**(海馬速度だが小・容量限界)。そして **Schlag(2102.11174)の fast-weight 容量限界 = P7 天井そのもの**で、これが llive 外部 store の存在を必然化する。

**両 north star を同時に満たす**: memory-efficiency = 有界 state × delta-rule × 疎キーでバイト当たり知識最大化 + rare 知識は llive へ offload。multi-teacher fusion = 「Qwen→GLM 逐次蒸留で B が A を消す」continual-distillation の既知失敗を、offline で A の logit を interleave replay して修正(= consolidation stage の中身)。

---

## 3. 最有望 1〜2 本

### 第1位: **sleep-replay / CLS consolidation bridge**
- スコア: payoff=高(測定済 prior art・両 north star 直撃)/ 反証=中(教師 logit 生成は重いが小教師・小プロンプトで一度きり→CPU 可)/ novelty=中(**sleep + 有界 constant-state + MULTI-teacher の三つ組は未公刊** = FullSense の合成貢献)。
- **CPU-first PoC**: 学生=小 Qwen ベース。教師=やや大きい Qwen + GLM-MIT。① ~1–5k プロンプトで各教師の top-K logit を一度だけ記録(教師非常駐)。② Phase A: 教師A を KL 蒸留。③ Phase B: 教師B を蒸留しつつ stored-A-logit を interleave replay(DER++ = KL-to-current + KL-to-stored-A)。④ **baseline = replay 無しの素朴逐次蒸留(教師A を本当に忘れることをまず実測)**。⑤ metric = Phase B 後の教師A retention(replay 有無)+ 教師B gain。⑥ honest gate: 教師別 retention を分け、no-replay baseline が忘れなければ勝ちは幻。stretch = 「Do LMs Need Sleep?」offline-recurrence で state 利用率も測定。
- **closest prior art**: Deep Generative Replay(1705.08690)/ DER++(2004.07211, logit-replay=蒸留)/「Do LMs Need Sleep?」(2605.26099)/ WSCL(2401.08623)。三つ組同時は未発見=novelty の源。

### 第2位: **sparse-neuromod の「疎キー → 容量」レバー**(最安反証・P7 直撃・第1位と相補)
- スコア: payoff=中(P7 容量=fusion の前提)/ 反証=最高(純 numpy・分単位)/ novelty=中。
- **CPU-first PoC**: 固定 state S∈R^{d×d}, d=64。N 個 random key→value を外積書込、read v̂=Sk。**dense Gaussian キー vs k-疎キー(2%/5%, L2 整合)** を N でスイープし recall 比較。事前登録仮説: crosstalk∝mean|⟨kᵢ,kⱼ⟩| が疎キーで小、より大きい N まで recall 保持。負ければ棄却。
- **closest prior art**: Kanerva SDM / sparse-Hopfield 容量論 / Hedgehog 疎 feature map(2402.04347)。

> predictive-coding の delta-rule+surprise-gate は payoff 高だが novelty 低(既に llcore ベース内)=「採用」枠。surprise スカラは第1位 consolidation の promote-gate として同梱。

---

## 4. ★honest 評価

**判定: 「脳構造を目指す」は新機構の源としては inspirational、選別と組立の発見的手法としては生産的。** 混同しないことが honesty の核。

**具体的に効く 3 点(実利)**: ① **棄却の指示(最重要)**: cortical-routing の唯一の硬い payoff は「resident MoE を作るな」(常駐 expert はメモリ非節約・反 fusion)。脳枠は「作るな」を教えた=負の知見だが本物。② **一貫した組立**: CLS 3-store + sleep consolidation が llcore+llive+offline-stage を 1 枚に束ね両 north star に同時に効く。③ **監査可能な統治セマンティクス**: surprise(write/promote)・consolidation gate(不可逆 weights 昇格=fail-closed)・ignition 閾値が Approval Bus に写る(ただし framing であって新機構でない)。

**story にすぎない部分(衣装)**: predictive-coding の cortical hierarchy / global-workspace の fusion(none)+constant-state(解釈のみ)/ sparse-neuromod の「neuromod=gating」(改名)/ cortical-routing の素朴 MoE 読み。

**先行知見との接続(決定的)**: fusion の退屈な答え=暗黙の多教師蒸留は**既に動く**。脳枠はこれを**置換せず**、正味 **2 つだけ**足す — (i) 素朴蒸留が間違う唯一点(教師A の catastrophic forgetting)と修正(interleaved replay)、(ii) どこで蒸留**しない**か(rare/episodic → llive へ offload)。**結論: 暗黙多教師蒸留を続けよ。そこに脳由来アップグレード 1 つ(offline interleaved replay-consolidation)と offload 規則 1 つ(rare→llive)を足す。それ以外は narrative。**

---

## 5. 推奨 first step + next_plan 1 行

**First step**: 第1位 sleep-replay の **minimal-viable leg のみ** = 2 教師 dark-replay 蒸留(小 Qwen + GLM-MIT、~1–5k プロンプト、top-K logit 一度記録、Phase A→B、replay 有/無比較、DER++ objective)。**baseline=素朴逐次蒸留が本当に教師A を忘れることを最初に実測**(忘れなければ実験全体が無意味)。SSM offline-recurrence と疎キー PoC は即時 follow-on でパーク。完全 CPU。

**next_plan(1 行)**: `次回最優先: sleep-replay PoC — 小Qwen+GLM-MITの2教師をdark-replay(DER++ logit蒸留)で単一constant-stateへ逐次fusion。baseline=素朴逐次蒸留の教師A忘却を実測し interleaved replayがA保持を回復するかを教師別retentionのhonest開示で1本検証。CPU完結、勝因がRAGでなくconsolidationかをgateで確認。`

---

## 6. 未検証・留保(ruthless)

- **三つ組は賭け**: sleep-replay + 有界 constant-state + MULTI-teacher を同時に行った公刊結果は無い(novelty の源でありリスク)。
- **容量上限は廃止できない**: 有界 state ゆえ fusion は容量制限付き。2 大教師を小 state に無損失で詰めるのは不可能。replay は干渉を減らすが ceiling を消さない。超過分は llive へ offload=その "fusion" は実質 RAG → honest gate で「勝因=retrieval か consolidation か」を必ず内訳分解。
- **頻度閾値も router も CLS 由来でない**(エンジニア指定)。LLM 教師知識が episodic/semantic に綺麗に分解する証拠は無い。
- **surprise-gate の多教師 fusion 転移は未検証** / **疎キーの実モデル副作用は未検証**(疎性が表現力を削る恐れ)。
- predictive-coding / cortical-routing / global-workspace は新機構を足さない(framing として扱い機構として数えない)。
- 前提依存: GLM-MIT 教師のライセンス/入手性、小 Qwen ベースに linear-attention/SSM head を足す実装コスト。
