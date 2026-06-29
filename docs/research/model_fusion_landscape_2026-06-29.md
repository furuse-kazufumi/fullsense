# モデル融合(異種モデルを1つにする)ブリーフィング — llcore/FullSense 向け (2026-06-29)

> **provenance**: 検証ワークフロー `model-fusion-landscape` (weg2ivhtx, 13 agents / 178 tool uses / ~11 min)。
> 6 融合ファミリー(weight-merge / cross-arch knowledge-fusion / composition / MoE-merge / evolutionary / 2025-26 frontier)を web + arXiv 一次メタデータで照合 → 敵対 fact-check → 統合。過大主張を §6 で補正。
> **接続(北極星)**: memory `project_fullsense_unified_model_vision`(llcore モデル × llive OS の縦統合)/ `feedback_qwen_commercial_barrier`(GLM-MIT = permissive teacher, `zhipu_glm_landscape_2026-06-29.md`)/ `distill_protocol_and_differentiation_2026-06-28.md`。

対象問題: **構造(architecture)もトークナイザ(tokenizer)も異なる学習済みモデルを 1 つにする**。結論を先に: weight-merge(重み空間マージ)は **同一 architecture + 同一 tokenizer が数学的前提**で、GLM→Qwen を重みでは絶対に混ぜられない。「全く別」を 1 モデルにする唯一の経路は **distillation(蒸留)= knowledge-fusion 系**。

---

## 1. ★決定木 — 「どれくらい別か」で手法を選ぶ

| 別の度合い | 具体例 | 使える手法 | 学習コスト | 主要参照 |
|---|---|---|---|---|
| **same-arch + 共有base** | 同一 Qwen-base から fine-tune した複数 expert | Model Soups / Task Arithmetic / **TIES** / **DARE** / SLERP / Fisher / RegMean | training-free | [2203.05482](https://arxiv.org/abs/2203.05482) / [2212.04089](https://arxiv.org/abs/2212.04089) / [2306.01708](https://arxiv.org/abs/2306.01708) / [2311.03099](https://arxiv.org/abs/2311.03099) |
| **same-arch + 別init** | 同 arch・別初期化 | **Git Re-Basin**(neuron permutation)/ **ZipIt!**(feature 相関 zip) | training-free(+data pass) | [2209.04836](https://arxiv.org/abs/2209.04836) / [2305.03053](https://arxiv.org/abs/2305.03053) |
| **compatible-arch(同 family)** | Mistral 系 layer-stack / recipe 探索 | **MergeKit** passthrough / **EvoLLM**(CMA-ES) / SOLAR depth-up-scaling | training-free / light | [2403.13257](https://arxiv.org/abs/2403.13257) / [2403.13187](https://arxiv.org/abs/2403.13187) / [2312.15166](https://arxiv.org/abs/2312.15166) |
| **different-arch + different-tokenizer(= Qwen + GLM)** | 異 arch・異 vocab を 1 weight に | **knowledge-fusion / 蒸留のみ**: FuseLLM / FuseChat / **FuseChat-3.0**(implicit) / cross-tokenizer KD(ULD・MultiLevelOT・DSKD・PTA-LLM) / **composition**: CALM | **distillation corpus + 継続学習(無料でない)** | [2401.10491](https://arxiv.org/abs/2401.10491) / [2402.16107](https://arxiv.org/abs/2402.16107) / [2503.04222](https://arxiv.org/abs/2503.04222) / [2402.12030](https://arxiv.org/abs/2402.12030) / [2401.02412](https://arxiv.org/abs/2401.02412) |
| **different-modality(LLM + 視覚/音声)** | frozen encoder を LLM に接続 | **composition bridge のみ**: BLIP-2 Q-Former / LLaVA projector / Flamingo gated cross-attn | distillation corpus(paired) / light | [2301.12597](https://arxiv.org/abs/2301.12597) / [2304.08485](https://arxiv.org/abs/2304.08485) / [2204.14198](https://arxiv.org/abs/2204.14198) |

**核**: 行が下がる = 重み空間の整合が不可能になる。`different-arch/tokenizer` 以降は **重みを混ぜる手法はゼロ**。behavior(logit/data)を移す蒸留か、frozen 接続(composition)のみ。

> 注: same-arch でも、student が **linear-attention(constant-state)** で expert が **softmax-attention Qwen** なら attention テンソルが非互換 → 「同 family」でもマージは壊れる。

---

## 2. 「全く別」を本当に 1 モデルにする 3 経路

### (1) Knowledge Fusion(蒸留)— 唯一の本命
- **機構**: weight でなく **behavior** を移すので異種 teacher 可。2 系統:
  - **explicit logit fusion**: **FuseLLM**([2401.10491](https://arxiv.org/abs/2401.10491))= per-token 確率を MinED で target tokenizer に整列→融合分布へ継続学習。**FuseChat**([2402.16107](https://arxiv.org/abs/2402.16107))= 「fuse→merge」。MinED の後継 = **OT(最適輸送)logit loss**: ULD([2402.12030](https://arxiv.org/abs/2402.12030))/ MultiLevelOT([2412.14528](https://arxiv.org/abs/2412.14528))/ DSKD([2406.17328](https://arxiv.org/abs/2406.17328))/ PTA-LLM([2509.17276](https://arxiv.org/abs/2509.17276))。
  - **implicit fusion**: **FuseChat-3.0**([2503.04222](https://arxiv.org/abs/2503.04222))と **InfiFPO**([2505.13878](https://arxiv.org/abs/2505.13878))は vocab/logit 整列を完全回避し **データ/選好レベル**(SFT + DPO)でのみ異種 teacher を蒸留。
- **コスト**: distillation corpus + 継続学習。
- **壊れる点**: cross-tokenizer 整列は本質的に lossy。素朴な複数 teacher 平均は単一最良 teacher に劣る compromise(FuseChat-3.0 は per-task 最強 source 選択で緩和)。

### (2) Composition(frozen + 学習 bridge)— 異 modality を含む唯一の branch
- **機構**: 各メンバ frozen のまま推論、学習可能 connector(cross-attn / projector)で activation 整列。LLM↔LLM = **CALM**([2401.02412](https://arxiv.org/abs/2401.02412))。modality = BLIP-2 / LLaVA / Flamingo。
- **壊れる点**: **推論メモリ加算的**(全メンバ常駐)→ 縮まない。GLM↔Qwen cross-tokenizer は未実証(CALM の公開実験は同 family PaLM2)。

### (3) MoE-merge(BTX 等)— ★これは「別モデル融合」ではない
- **機構**: 別々学習した expert の FFN を 1 MoE に並べ router 学習。**BTX**([2403.07816](https://arxiv.org/abs/2403.07816))。
- **非交渉の前提 = 共有 seed/base**(意図的に同 arch/tokenizer expert を製造)。異種融合の真逆。
- **llcore に致命的**: sparse 活性は compute は節約するが **RAM は節約しない**(全 expert 常駐)。かつ全て softmax upcycle で constant-state を生まない。

**まとめ**: 異 arch/tokenizer を真に 1 weight にできるのは **(1) 蒸留のみ**。(2) は繋ぐが縮まない。(3) は同 seed 専用で memory を増やす。

---

## 3. 2025-2026 の新展開

### 検証済み(cutoff 以前)
- **implicit multi-teacher fusion の確立**: **FuseChat-3.0**([2503.04222](https://arxiv.org/abs/2503.04222))が Gemma-2-27B + Mistral-Large + Qwen-2.5-72B + Llama-3.1-70B を小 target に SFT+DPO で融合。**student arch が融合機構に無関係** = constant-state student でもそのまま回る、が最大の新規性。InfiFPO([2505.13878](https://arxiv.org/abs/2505.13878))は sequence-level 確率を保持。
- **cross-tokenizer KD の OT 化**: MinED → **PTA-LLM**([2509.17276](https://arxiv.org/abs/2509.17276), NeurIPS'25)/ MultiLevelOT([2412.14528](https://arxiv.org/abs/2412.14528), AAAI'25)。
- **population/QD 進化(llive/lldarwin に 1:1)**: **CycleQD**([2410.14735](https://arxiv.org/abs/2410.14735), ICLR'25)/ **M2N2**([2508.16204](https://arxiv.org/abs/2508.16204))/ 効率化 **MERGE³**([2502.10436](https://arxiv.org/abs/2502.10436), ~50x 削減・consumer GPU 1 枚)/ **Mergenetic**([2505.11427](https://arxiv.org/abs/2505.11427))。

### ★cross-architecture weight-merge への挑戦(新しいが未確立)
- **HeteroFusion**([2604.01674](https://arxiv.org/abs/2604.01674), 2026-04, **post-cutoff・要検証**): family を跨ぐ near-weight-space 融合を狙う唯一の 2026 試み。ただし同 paradigm decoder-only 限定・単一論文・低被引用・heavy。

### post-cutoff lead(resolve 確認・結果未独立検証)
- AC/DC([2604.14969](https://arxiv.org/abs/2604.14969), model+task 共進化で**より大きいモデルを低 GPU メモリで凌駕**主張 → memory north star 直結)/ Byte-Level Distillation([2604.07466](https://arxiv.org/abs/2604.07466), tokenizer 非依存 KD)/ FusionRoute([2601.05106](https://arxiv.org/abs/2601.05106), functional fusion)/ Cross-Tokenizer Likelihood([2512.14954](https://arxiv.org/abs/2512.14954))。

---

## 4. ★honest 現実 — 融合が「害」になる時

- **interference は構造的**: task vector を混ぜると sign 衝突 + magnitude 冗長 = TIES/DARE が存在する動機そのもの。マージ後は通常 **Pareto compromise**(幅は得るがピークに届かない)。
- **融合が HURT する時**: ① 複数 teacher 素朴平均は単一最良に劣りうる ② cross-tokenizer 整列の近似ノイズ ③ load-balancing loss が専門性を潰す ④ multi-teacher logit 同時利用は未 battle-tested(data/preference 経路が現状最も実証的)。
- **"training_free" の正直化**: 勾配は無いが compute は無料でない(Fisher/RegMean/ZipIt/Evolutionary は data pass や世代評価が要る)。
- **ensemble が正直な答えになる時**: 「1 つの小モデルに縮める」必要が無いなら functional fusion(MoA [2406.04692](https://arxiv.org/abs/2406.04692) / LLM-Blender [2306.02561](https://arxiv.org/abs/2306.02561))が最も素直。代償 = 全 expert 常駐 + 推論倍化 → **llcore の memory north star と正面衝突=却下**、品質最大化サービスでのみ妥当。

---

## 5. llcore / FullSense 推奨

**制約**: constant-state + on-prem + multi-teacher 蒸留(Qwen base + GLM-MIT teacher)+ GGUF serving + llive governance。

### 大原則
- **vertical stack(蒸留 → 1 つの小 constant-state モデル)が weight-fusion / ensemble に勝つ**。memory-efficiency が北極星なら**蒸留一択**。
- **2 つの直交問題を分離**: (a) knowledge fusion(GLM+Qwen → student)と (b) **architecture distillation / state 圧縮**(softmax → linear-attention, LoLCATs/MoHawk)。**(b) はどの fusion family も解かない** = 別ステージ。

### ランキング(llcore 向け)
1. **【本命】implicit multi-teacher fusion = FuseChat-3.0 / InfiFPO**([2503.04222](https://arxiv.org/abs/2503.04222) / [2505.13878](https://arxiv.org/abs/2505.13878))。GLM-MIT teacher は生成テキスト + 選好だけ使う(logit/vocab 不要)→ SFT + DPO。**student が constant-state でも機構不変**。問題文ほぼそのもの。
2. **【補強・任意】white-box cross-tokenizer logit KD = ULD/MultiLevelOT/DSKD/PTA-LLM**。GLM の richer logit が欲しい時に implicit の上に重ねる(multi-teacher OT は noisy → 単一 teacher 単位で慎重に)。
3. **【下流 consolidation のみ】weight-merge TIES/DARE(MergeKit)**。**前提: 既に同一 Qwen-base 由来 expert が複数ある時だけ**。cross-arch GLM→Qwen 段では使えない。+ Qwen-family expert の探索的合成は EvoLLM/CycleQD/M2N2 が llive QD + lldarwin に 1:1 対応。
4. **【却下】MoE-merge(BTX)= 全 expert 常駐で memory 増 / functional ensemble = 全常駐 / GLM を Qwen に直接 weight-merge = 数学的に不可能**。

### 1 行推奨
> **GLM-MIT → 小 Qwen(constant-state)は FuseChat-3.0 流 implicit fusion(SFT + 重み付き reward DPO)を本命とし、必要時に単一 teacher 単位で cross-tokenizer OT-KD(ULD/PTA-LLM)を補強、同 Qwen-base expert の統合だけ TIES/DARE で行う。softmax→linear-attention の state 圧縮は別ステージ。weight-merge / MoE-merge / 常駐 ensemble は memory north star と衝突するため不採用。**

---

## 6. 未検証・要追跡(過大主張の補正含む)

- **post-cutoff 2026(resolve 確認・結果未独立検証=lead 扱い)**: HeteroFusion [2604.01674] / AC/DC [2604.14969](memory north star に最重要だが abstract のみ)/ Byte-Level Distillation [2604.07466] / FusionRoute [2601.05106] / Cross-Tokenizer Likelihood [2512.14954]。search-listing のみ(更に低信頼): FusionFactory [2507.10540] / DWA-KD [2602.21669] / SRA [2605.01205]。
- **構造的に未探索**: **merge ベースの constant-state MoE は存在しない**(MoE-FFN + linear-attention は scratch 学習なら共存 = EDA [2606.26560] だが merge/upcycle 経路は皆無 = net-new research)。linear-attention student への蒸留は tokenizer gap の上に arch gap を積む(cross-tokenizer KD はほぼ Transformer student 前提)。
- **過大主張の補正**: ① **FuseChat-3.0 の headline 数値は Qwen student でなく Llama-3.1-8B target**(Qwen-7B student の gain は別)② InfiFPO は logit を捨てない(sequence-level 確率保持)③ ZipIt!/Git Re-Basin は vision 由来(「同 tokenizer 必要」は LLM への外挿)④ DSKD "ANY two vocabularies" は過大(近似で gap を縮めるだけ)⑤ CALM の GLM↔Qwen cross-tokenizer は未実証 ⑥ EvoLLM/M2N2 の "cross-domain" は cross-TASK(parents は同 arch Mistral)で cross-architecture ではない。
