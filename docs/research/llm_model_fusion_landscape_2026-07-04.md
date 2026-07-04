---
layout: default
title: "LLM モデル融合 ランドスケープ (2026-07-04)"
parent: "Research"
---

# LLM モデル融合(model merging / fusion)ランドスケープ + 融合設計空間

> 作成: 2026-07-04(ccr, Fable 5, ultracode)。gaitlab で「MJCF body サブツリーを接ぎ木する形態融合(`morphology.py`)」を実装 → 「LLM もモデルを融合できるか / 色々な側面で検討して」への回答。
> 手法: RAPTOR Workflow 2 本(**調査 13 agents** = 6分野 fan-out→一次情報で敵対検証→統合 / **多角検討 10 agents** = 9側面→統合)、計 23 agents。各手法に一次参照(arXiv/repo)、検証で PARTIAL/REFUTED だった主張は明示。honest-disclosure 準拠([[feedback_benchmark_honest_disclosure]])。
> ★arXiv ID の確認状況は §7。**canonical だが数字は記憶依存**の ID は公開記事化の前に再確認。

---

## 0. 結論(3-4 文)

**LLM モデル融合は現実に成立するが、"どの意味での融合か" で成立条件が真っ二つに割れる。** ①**重み空間マージ**(座標ごとに重みを混ぜる)は**同一 base・同一アーキ・ほぼ同一トークナイザ必須**だが多くは**追加勾配学習が不要**(Model Soups/Task Arithmetic/TIES/DARE/SLERP)。②**深さグラフト/frankenmerge**(層ブロックを抜いて積む)は **gaitlab のサブツリー接ぎ木に構造的に最も近く**、接合後の **healing(継続学習)がほぼ必須**。③**知識融合**(FuseLLM 系、出力分布を蒸留)は**異アーキ・異トークナイザ・異 base を跨げる唯一の一般解だが必ず学習が要る**。**「無関係な別モデルの重みを訓練なしで平均して 1 個にする」は原理的に不可能**(座標系不一致=Git Re-Basin の教訓)。可能なのは「同じ祖先の兄弟の重み混合」「学習を払う蒸留融合」「畳まず routing(=llmesh)」のいずれか。

---

## 1. 手法の地図(検証済み・一次参照付き)

凡例 — 同base: 共通事前学習チェックポイントを祖先に要するか / 同arch: 同一アーキ(層形状一致) / 同tok: 同一トークナイザ前提 / 訓練: 追加勾配学習の要否(★=training-free だがハイパラ調整の評価コストは残る)。

| カテゴリ | 代表手法 | 一次参照 | 同base | 同arch | 同tok | 訓練 |
|---|---|---|---|---|---|---|
| 重み平均 | Model Soups | arXiv:2203.05482; mlfoundations/model-soups | 必須 | 必須 | 必須 | 不要★ |
| 重み補間 | WiSE-FT | arXiv:2109.01903 | 必須 | 必須 | 必須 | 不要★ |
| 重み補間 | SLERP | Shoemake 1985 (DOI:10.1145/325334.325242) + arcee-ai/mergekit。**LLM 用正典論文なし** | 実質必須 | 必須 | 必須 | 不要★(2モデル) |
| task vector | Task Arithmetic | arXiv:2212.04089 (ICLR2023); mlfoundations/task_vectors | 必須 | 必須 | 必須 | 不要★ |
| +干渉緩和 | TIES-Merging | arXiv:2306.01708 (NeurIPS2023) | 必須 | 必須 | 必須 | 不要★ |
| +疎化 | DARE | arXiv:2311.03099 (ICML2024) | 必須(homologous) | 必須 | 必須 | 不要★ |
| +疎化 | DELLA | arXiv:2406.11617; declare-lab/della | 必須 | 必須 | 必須 | 不要★ |
| +両裾除去 | Model Breadcrumbs | arXiv:2312.06795 (ECCV2024) | 必須 | 必須 | 必須 | 不要★ |
| 重要度重み付け | Fisher-Weighted Averaging | arXiv:2111.09832 (NeurIPS2022) | 必須 | 必須 | 必須 | 不要だが**データ通過要** |
| 活性整合(閉形式) | RegMean | arXiv:2212.09849 (ICLR2023); bloomberg/dataless-model-merging | 必須 | 必須 | 必須 | 不要だが**データ通過要** |
| 幾何 | Model Stock | arXiv:2403.19522 (ECCV2024) | 必須 | 必須 | 必須 | 不要★ |
| 置換整合 | Git Re-Basin | arXiv:2209.04836 (ICLR2023)(土台 Entezari 2110.06296) | init/seed 違い可 | 必須 | 必須 | 整列は無学習(実証は主に小規模 vision) |
| 置換整合(OT) | OT Fusion | arXiv:1910.05653 (NeurIPS2020) | init 違い可 | 層対応必須(**異幅可**) | — | **one-shot 可** |
| **深さグラフト** | passthrough / frankenmerge | arXiv:2403.13257 (mergekit) | 交互積みは同系統 | 必須(hidden 幅一致) | 交互積みは実質必須 | 重み生成は不要・**品質保証なし** |
| **深さグラフト** | Depth Up-Scaling (SOLAR 10.7B) | arXiv:2312.15166 (NAACL2024) | 単一 base 自己マージ | 必須 | 必須 | **healing(継続事前学習)必須** |
| **深さグラフト** | Goliath-120B | HF alpindale/goliath-120b(論文なし) | 同系統(Llama2-70B) | 必須 | 必須 | 事後訓練なし・**厳密 ablation 無** |
| ブロック拡張 | LLaMA Pro | arXiv:2401.02415 | 同一 base 拡張 | 必須 | 必須 | **新ブロックのみ学習**(挿入は恒等=無破壊) |
| 層冗長性(指針) | ShortGPT / Gromov | arXiv:2403.03853 / arXiv:2403.17887 (ICLR2025) | — | — | — | 削除は無学習・**healing 推奨** |
| MoE 化 | Sparse Upcycling | arXiv:2212.05055 | 単一 dense 起点 | 必須 | 自明 | **router+継続学習必須** |
| MoE 化(並列専門家) | Branch-Train-Merge | arXiv:2208.03306 | 共通 seed | 必須 | 必須 | expert 学習要・token router 無 |
| MoE 化(束ね) | Branch-Train-MiX (BTX) | arXiv:2403.07816 (Meta FAIR) | 共通 seed | 必須 | 必須 | **MoE-finetune(router 学習)必須** |
| MoE 化(接ぎ木) | mergekit-moe (frankenMoE) | mergekit docs/moe.md | 同系統 | 同サイズ | 実質必須 | hidden/cheap_embed は**無学習 gate 可**(品質劣) |
| **進化マージ** | Evolutionary Model Merging (Sakana) | arXiv:2403.13187 (NMI s42256-024-00975-8) | PS 必須 / DFS 緩 | PS 必須 | PS 必須 | 重み学習不要・**fitness 評価コスト大** |
| 進化マージ(実装) | mergekit-evolve | mergekit docs/evolve.md | 必須(PS) | 必須 | 必須 | 無学習(CMA-ES) |
| 進化マージ(ライブラリ) | Mergenetic | arXiv:2505.11427 (ACL2025 Demo) | 下層継承 | 下層継承 | 下層継承 | 無学習(軽量 fitness 推定) |
| **知識融合** | FuseLLM | arXiv:2401.10491 (ICLR2024); **github.com/fanqiwan/FuseLLM** | **不要(異可)** | **不要(異可)** | **不要(異可)** | **蒸留=継続学習必須** |
| 知識融合(2段) | FuseChat (+VaRM) | arXiv:2402.16107 / 2408.07990 | 異可(pivot 化) | 異可 | 異可 | **continual training 必須** |
| 知識融合(移植) | GraftLLM | arXiv:2505.18502 | 異可 | 異可 | 異可 | 適用に学習要 |
| cross-tok 蒸留(OT) | ULD / MultiLevelOT / PTA-LLM | 2402.12030 / 2412.14528 / 2509.17276 | 異可 | 異可 | 異可 | student FT 前提 |
| cross-tok 蒸留(空間統一) | DSKD | arXiv:2406.17328 (EMNLP2024) | 異可 | 異可 | 異可 | student FT 前提 |
| cross-tok 蒸留(byte 射影) | BLD | arXiv:2604.07466 (2026) | 異可 | 異可 | 異可 | **未解決問題と当事者明言** |

---

## 2. 融合設計空間 — 2 軸マップ(基質 × 階層)

**縦軸=基質(何を融合するか)**: 深い基質(重み)ほど結合が強く**同一 base 必須+訓練を要す**、浅い基質(logit/state/steering/datastore)ほど **training-free かつ base 非依存**。一本の勾配。
**横軸=階層(どこで畳むか)**: `Ensemble(N 重み保持・干渉ゼロ)→ MoE(1 file・容量 Σ・遅延≈1)→ Weight-merge(1 重み・干渉あり)→ Distill(1 重み・異アーキ可)`。
**削除テスト**: 構成 checkpoint を捨てて single-forward 以外に何も失わないなら「真の融合」→ ensemble/MoE は**共存**、merge/distill/co-train は**融合**。

凡例: **[同]**=同一 base 必須 / **[異]**=異 base/異アーキ可 / **[整]**=整列すれば異 init 可(脆い)

| 基質 ↓ \ 階層 → | Ensemble / 推論時共存 | MoE / 条件分離 | Weight-merge | Distill-fusion |
|---|---|---|---|---|
| **weights** | — | Sparse Upcycling [同] | Task Arith/TIES/DARE/SLERP/Soups [同], Git Re-Basin+OTFusion [整] | FuseChat=distill→merge [異] |
| **layers** | — | Branch-Train-MiX [同] | frankenmerge/passthrough/SOLAR DUS [同・要 heal] | (heal=継続事前学習) |
| **activations** | — | — | ZipIt! / RegMean(closed-form) [整] | model stitching(薄い学習 bridge)[異] |
| **logits** | LLM-Blender / MoA / PoE [異] | — | — | Proxy-tuning/DExperts/Contrastive Decoding [同vocab], EVA=異vocab [異] |
| **knowledge(分布)** | — | — | — | **FuseLLM / FuseChat**(唯一の実績ある異アーキ融合)[異] |
| **adapters(LoRA)** | AdapterSoup | MoLE / X-LoRA / PHATGOOSE(動的 gate) | LoRAHub / TIES-LoRA / Twin-Merging [同] | — |
| **tokenizer/vocab** | — | — | ZeTT/WECHSEL で語彙移植→merge 解禁 [部分緩和] | ULD/ALM(OT logit 整列蒸留)[異] |
| **state / KV** | — | — | StateX head-merge / linear-attn 状態は加法的 [同φ], CacheBlend/MiniCache(KV)[同モデル] | — |
| **persona / steering** | 推論時ベクトル合成(ActAdd/ICV/RepE)[同モデル] | — | persona-LoRA を TIES/MoLE [同] | — |
| **modality** | — | — | — | projector graft=LLaVA/Flamingo [異] |
| **RAG(非パラ)** | kNN-LM(出力分布補間)[同vocab] | — | — | RETRO=chunked cross-attn(要専用事前学習) |
| **tools** | — | ToolkenGPT(toolken=vocab)[同base] | — | — |

**読み方**: 右下(distill)ほど異種を飲めるが訓練コスト、左上~中(ensemble/logit/steering/state/KV)ほど CPU・training-free だが「共存」。**llcore の制約適合ゾーン=中間基質**(adapter 算術 / steering / linear-state / KV 融合)= 最も見落とされている。

---

## 3. gaitlab 形態融合との対応(直感の核)

gaitlab で行ったのは「MJCF body サブツリーを互換ジョイントで接ぎ木」する形態融合。LLM で構造的に同型なのは**重み平均系ではない**。

| gaitlab の操作 | LLM 側の対応 | 質 |
|---|---|---|
| body サブツリーを丸ごと接ぎ木 | **passthrough/frankenmerge** / SOLAR DUS / Sakana **DFS(data flow space)** | ★構造的に最も近い |
| 接合面を互換ジョイントで合わせる | SOLAR「継ぎ目の中間層を削り不連続を減らす」/ passthrough の hidden 幅一致 | 発想同一 |
| 接いだ後に歩容を再学習 | **healing(継続事前学習/QLoRA)** | ほぼ必須まで一致 |
| 初期は本体を乱さない突然変異 | **LLaMA Pro のブロック恒等初期化** | 安全な拡張オペレータに転用可 |
| 接ぎ木構成を進化探索 | **Sakana Evolutionary Merge**(層経路 I と scaling W を CMA-ES 探索) | ★進化ループごと同型 |

**重要な区別**: 重み平均(soup/TIES/DARE/SLERP)は「構造の接ぎ木」でなく「同一骨格の関節パラメータを座標ごとにブレンド」する操作。gaitlab で言えば「2 個体の同じ関節可動域を平均する」= body 付け替えではない。honest: これは**比喩的対応であって厳密な同型証明ではない**(gaitlab=物理 body 移植は構造合成に寛容 / LLM=Transformer 層連結は表現空間が非寛容で heal-tune 必須)。方向付けとしては正しい(illustrative)。

---

## 4. 異分野アナロジー(遠い分野 → 融合機構)

仮説生成器であって証拠ではない(各写像は小モデルで loss-barrier/能力保持を実測してから信じる)。

| 分野 | 現象 | LLM 融合機構 | 破綻条件 |
|---|---|---|---|
| 進化生物学 | 水平遺伝子移動(HGT)= 遺伝子を att 部位へ挿入、制限酵素で不適合を切る | task-vector τ を Git Re-Basin の相同部位にだけ注入 + TIES sign を制限ゲート化 | 共通祖先(同 base)無しでは相同部位が消え無意味 |
| 細胞生物学 | 内共生(ミトコンドリア)= 別ゲノムを膜で統合→縮退 | CALM(cross-attn 膜で凍結 augment)→ 使う能力だけ段階蒸留 | 縮退経路は SPECULATIVE |
| 園芸 | 接ぎ木(cambium 整合)、非親和は interstock(中間台木)3 段接ぎ | frankenmerge 境界に interstock アダプタ 1 枚(残差統計整合)を短学習 | 表現差が非線形に大きいと 1 層で橋渡し不能 |
| 移植免疫学 | HLA 適合スクリーニング+免疫抑制 | CKA/表現類似で事前適合判定→host 凍結+graft 正則化 | CKA は縫合可能性を弱くしか予測せず |
| 冶金 | 固溶体合金 vs 複合材、共晶、相図 | λ×温度でマージ相図を掃引、低曲率方向へドーピング注入 | 一部 SPECULATIVE(LLM に定量相図なし、低曲率≠未使用) |
| 半導体 | ppm ドーピングで n/p 型が激変 | 合金後 rank-1 steering を微量注入し persona/refusal を tune | rank-1 は脆く off-target、安全機構に頼るのは危険 |
| 音楽(和声) | 協和/不協和=周波数比、2 音は平均せず別周波数で共存 | SVD 主角で協和度を測り直交方向は重畳・不協和だけ sign 解決 | 主角直交は干渉を減らすが消せない |
| 金融 | Markowitz 効率的フロンティア(共分散で配分) | 能力=資産、モデル間相関=共分散として QP でマージ重み最適化 | 信頼できる評価ベクトルが要る |
| 制御工学 | gain scheduling(regime で係数補間) | per-input soft merge(SMEAR/X-LoRA)= 動作点で LoRA 連続補間 | router 未学習だと干渉を推論時に先送り |
| 発酵【ばかげた案】 | コンブチャ SCOBY 連続培養(不死の母に餌) | 恒久「母」に新 fine-tune を薄く混ぜ続ける | **ジョーク枠**。乖離 fine-tune を餌にすると崩壊。恣意ヒューリスティックが実測 mode-connectivity に劣る反面教師 |

---

## 5. TRIZ 矛盾と解決(融合の中心矛盾)

**中核の物理的矛盾**: 共有パラメータ W は同座標で **W_A かつ W_B** であれ。線形平均 (W_A+W_B)/2 は非凸損失面の高損失域(干渉/崩壊)に落ちる。既存マージ手法はすべて「別々の分離原理の適用」と読める。

| # | 矛盾 | 解決原理 | 対応手法 |
|---|---|---|---|
| 1 | 能力 B を足すと能力 A が劣化(破壊的干渉) | #1 分割 + #3 局所性質(空間分離) | DARE(delta 疎化)→ TIES(座標ごと符号選挙) |
| 2 | 安い異種融合 vs 品質(座標系非互換) | #24 仲介 + #10 先取り作用 | 蒸留=出力分布空間で橋渡し(FuseLLM) / 先に homolog 化(FuseChat) / Git Re-Basin で整列後平均 |
| 3 | 汎化 vs 専門(平均への回帰) | #15 ダイナミック性(条件分離) | router/MoE / FFN を非マージで MoE 化(BTX) / 進化探索で recipe 自己設計(Sakana) |
| 4 | 融合で増える vs 軽さ(llcore の北極星と逆行) | #35 パラメータ状態変化 + #34 排除再生 | 低ランク/低ビット delta(LoRAHub) / merge→prune/distill で畳む |

**分離原理での俯瞰**: (a)空間分離=層・ニューロン単位で配合(Sakana PS + MAP-Elites)/ (b)条件分離=入力ごとに選ぶ(routing/MoE)/ (c)時間分離=base 固定+能力アダプタ hot-swap で同時共存させない(S-LoRA, StateX head-merge)/ (d)仲介=stitch 層・projector・語彙アライン射影・Approval Bus を接合部に挿す。

**★llcore 特例**: 線形化アテンション(LoLCATs)vs softmax teacher は**座標対応が無く、空間分離・条件分離が全滅**。残る手は (a)蒸留で homolog 化してから merge / (b)シームアダプタ層グラフト / (c)アダプタ時間分離 hot-swap の 3 つだけ。

---

## 6. 異種融合の現実解 — align → stitch → distill

「本当に別々のモデル」の融合はほぼ絶対に重み平均を意味しない(共有座標系が無く無意味)。現実解は 3 段のインターフェース化(融合は「平均」より「移植・接木・通訳」)。

```
[A: align 整列]  表現を比較可能に(重みは触らない)
   ├ Git Re-Basin(置換整列, 同アーキ・等幅)         2209.04836 ✓
   ├ OTFusion / ZipIt!(最適輸送・異幅/部分融合)       1910.05653 / 2305.03053
   ├ 相対表現アンカー(学習不要・CPU可)                Moschella ICLR2023 (2209.15430)
   └ 適合性スクリーニング CKA / loss barrier            1905.00414 / 1912.05671
        ↓ 障壁が低い(同一 basin)ペアだけ次段へ
[B: stitch 縫合]  凍結両モデルを薄い学習 bridge で接続(まだ 2 モデル保持)
   ├ model stitching(下位A+学習中間層+上位B)         2106.07682 ✓
   ├ CALM cross-attention 膜(重み凍結・臓器接続)       2401.02412 ✓
   ├ interstock アダプタ(接合部の残差統計整合)          (SOLAR 2312.15166 の CPU 廉価版)
   └ 出力分布 co-generation / PoE(重み・表現に触れない)  llmesh hub に自然に載る
        ↓ 1 モデルが要るときだけ最終段へ
[C: distill 蒸留]  合成挙動を 1 生徒へ(異アーキ可・唯一の真の異種融合実績)
   ├ FuseLLM / FuseChat(確率分布統合+tokenizer 整列)   2401.10491 / 2402.16107 ✓
   └ 異 tokenizer は ULD/ALM の OT logit 整列 or ZeTT 前処理  2402.12030 / 2503.20083 / 2405.07883 ✓
```

**llcore への含意**: Stage B(stitch/co-gen)は**メモリ 2 倍・遅延 2 倍**で llcore のメモリ効率目標と逆行。llcore に効くのは「align → teacher として stitch → distill で 1 小型モデルに畳む」経路のみ。既出 StateX head-merge / xLSTM 蒸留 expert-merging はその内側(同 base)、外側(異 base head を混ぜたい)を相対表現/OT 整列が埋める。

---

## 7. FullSense 適用ショートリスト(採点)

採点軸: **新規性** / **実現性(CPU 可否)** / **影響度**(★1–3)。

| 順位 | 案 | 新規性 | 実現性(CPU) | 影響度 | 一次参照 |
|---|---|---|---|---|---|
| **1** | **gaitlab QD-of-merges**: `MapElitesArchive` を一字も変えず「歩容」→「マージレシピ」に転用。genome=マージ係数, fitness=タスクスコア, descriptor=出力長/ja:en 比/拒否率。多様かつ精鋭なマージの palette | ★★★ | ★★★(gaitlab 資産流用・sub-2B) | ★★★ | MAP-Elites 1504.04909, Sakana 2403.13187, gaitlab `map_elites.py` |
| **2** | **llcore 専門家蒸留マージ**: 同一 Qwen base へ JP/数学/コードを個別蒸留 → 3 task-vector を Soup/TIES 平均で capability patching。xLSTM 蒸留 expert-merging の横展開 | ★☆☆ | ★★☆(平均=CPU可, 蒸留=GPU) | ★★★ | Model Soups 2203.05482, TIES 2306.01708, xLSTM expert-merging(内部検証済) |
| **3** | **llive 進化マージ**: マージ係数(層別 SLERP t / DARE density / TIES 閾値)を genome、tiny eval を fitness、CMA-ES/ε-lexicase で探索。persona ゲノム↔層別マージベクトルが自然対応 | ★★☆ | ★★★(マージは weight 算術で安価) | ★★☆ | Sakana 2403.13187, llive lldarwin(ε-lexicase+QD) |
| **4** | **persona=steering ベクトル合成**(llive/llove): persona を活性差分ベクトルとして抽出し h←h+Σα_i v_i。遺伝子操作=ベクトル算術、可逆・ダイヤル可能・再訓練不要 | ★★★ | ★★★(推論時加算のみ) | ★★☆ | ActAdd 2308.10248, RepE 2310.01405, Function Vectors 2310.15213 |
| **5** | **llcore 状態/KV 融合**: linear-attn 状態の加法性で runtime に state 分岐→並列→統合、softmax は CacheBlend で KV 部分再計算融合。StateX head-merge の動的化 | ★★★ | ★★☆(線形は加法的で安価, 要検証) | ★★☆ | Transformers-are-RNNs 2006.16236, CacheBlend 2405.16444 ✓, StateX head-merge(隣接) |

**次点**: llmesh=RouteLLM/LLM-Blender/co-decode の推論時融合(意図的に「merge せず route せよ」の honest 境界)。gaitlab morphology-graft↔層 graft の研究アーティファクト化(4 言語記事+共有 `graft()` メンタルモデル)。

### 最有力(#1)の最初の一歩 — mergekit CPU 粒度

```powershell
py -3.11 -m pip install mergekit
# config.yml: base=Qwen/Qwen2.5-0.5B-Instruct, models=[base, <同base community fine-tune>],
#             merge_method=slerp, parameters={t:0.5}, dtype=float32
mergekit-yaml config.yml ./merged --lazy-unpickle   # --cuda 無し=CPU, 0.5B なら数分・数GB RAM
# → held-out 数十プロンプトで perplexity/一致率を measure(マージ vs 両親)= ベースライン
# → 負のコントロール: 異 base をマージ → perplexity 爆発で「同一 base 制約」を可視化
# → マージ係数(層別 t)を gaitlab MapElitesArchive の genome に露出し archive を CPU で照らす
```
`layer_range` は実チェックポイントの層数に合わせる(Qwen2.5-0.5B は 24 層想定だが**要実測**)。gaitlab の `MapElitesArchive`(genome=np.ndarray, descriptor は caller 供給)/ `MultiPressureSelector`(ε-lexicase)は fitness 差し替えだけで薄いアダプタで載る。

---

## 8. honest な限界(誇張しない)

1. **容量保存則**: 単一重みへの真の融合は容量固定。7B×2 を merge しても 14B にはならず干渉で妥協した 7B が得られるだけ。**重み空間マージは全親に無い capability を創れない**(上限=親スキルの和集合)。
2. **「同一 base」は理論的核だが経験則**: weight-merge が合法なのは単一の線形連結ベイスン(LMC, Frankle 1912.05671)の内側だけ。Git Re-Basin は permutation で部分整列しうるが **attention/LN/residual を持つ大型 Transformer では脆く production 級に届きにくい**(REPAIR 2211.08403 が幅依存・活性再正規化を要すと指摘)=「整列すれば異 base もマージできる」は LLM では過大宣伝。
3. **llcore 線形化の壁**: LoLCATs 線形化は多くの weight-merge 前提を壊す。線形化後は logit/steering/datastore/state という浅い基質のほうが安全側。異アーキの真の融合は蒸留しか実績が無く、生徒は概ね ≤ 最良教師、tokenizer 跨ぎ整列は lossy(cross-tokenizer distillation は 2026 時点でも「全ベンチ一貫改善は未達」と当事者 BLD が明言)。
4. **training-free は超パラメタに敏感**: task-vector/steering/KV 融合/kNN-LM も λ,α に敏感で off-manifold 崩壊が定番。専門家/persona を 3〜8 個超で破壊的干渉が顕在化(文献一致)。
5. **推論時融合は速度と交換**: ensemble/MoA は単一良モデルを超えることが稀で N 倍コスト。投機的デコードは速度のみ(能力は増えない)。「融合できる」と「実用速度で回る」は別問題(要実測)。
6. **メモリ→重み焼込みの二重リスク**: episodic を base 重みへ書き戻すと catastrophic forgetting + **PII 焼込みの privacy 漏洩**(FullSense 哲学に反する)→ Approval Bus gate 必須。
7. **MoE は llcore の北極星と逆行**: 全 expert FFN 常駐で N× パラメータ = メモリ効率の anti-goal。

### 検証で PARTIAL/REFUTED(誇張防止)
- **REFUTED**: 「RegMean は Fisher 論文の一部」→ 誤り。RegMean の正典は **arXiv:2212.09849**(Fisher 2111.09832 とは別論文)。
- **PARTIAL**: Sakana「70B 超え」= 特定日本語ベンチで一部の 70B を上回る(全面 SOTA でない、MGSM-JA PS=52.0/PS+DFS=55.2、親 9.6/18.4/30.0)。**DFS の異トークナイザ橋渡しは未実証**(EvoLLM-JP の 3 ソースは全て Mistral-7B-v0.1 派生=同一トークナイザ。"cross-domain" は能力ドメインの横断でトークナイザ横断ではない)。
- **PARTIAL**: OT Fusion は one-shot でも動く/異幅も扱える(「整列後微調整必須」「同一幅必須」は言い過ぎ)。
- **PARTIAL**: mergekit は `tokenizer_source: union` で語彙統合・embedding 再マップ可(トークナイザ差を全く吸収しないは過小)。ただしこれは embedding/lm_head の語彙整合に留まり、異 base 由来の内部 Transformer 重みの表現空間不一致は解消しない → 素朴な深部座標平均が破綻する結論は保たれる。
- **引用訂正**: FuseLLM repo は `github.com/fanqiwan/FuseLLM`(allthingsllm ではない)。

### 残る uncertainties(正直に)
- 線形化+重い蒸留で basin を離れた llcore 兄弟同士で soup/TIES が機能するかは**未検証**(PoC 必須)。
- 線形 attention アーキ上での MoE 化(Sparse Upcycling/BTX 移植)の成立可否は**一次情報で未確認**。
- 「同一 base 必須」の厳密な線引き(同一 checkpoint か同族の別 checkpoint でも可か)は手法・層依存で定量境界は未確立(実務は試行錯誤)。
- 各手法の相対性能は自己申告 SOTA が多く独立同一設定の横並び再現は限定的(内訳を疑う)。

**メタ注記**: 異分野グラウンディング(接木・移植・冶金・音楽)は**仮説生成器であって証拠ではない**。gaitlab↔LLM グラフトは isomorphic でなく illustrative(MuJoCo 物理は構造合成に寛容、Transformer 表現は非寛容で heal-tune 必須)。arXiv ID は §冒頭の「記憶依存」群を公開記事化の前に再検証。

---

## 9. 一次参照インデックス(arXiv / repo)

- 重み平均: 2203.05482, 2109.01903, 2212.04089, 2306.01708, 2311.03099, 2406.11617, 2312.06795, 2111.09832, **2212.09849(RegMean)**, 2403.19522 / Shoemake 1985 (DOI:10.1145/325334.325242)
- 整合: 2209.04836, 2110.06296, 1910.05653, 2211.08403(REPAIR), 1912.05671(LMC), 2305.03053(ZipIt!), 2106.07682(stitching), 2209.15430(相対表現)
- 深さグラフト: 2403.13257(mergekit), 2312.15166(SOLAR), 2401.02415(LLaMA Pro), 2403.03853(ShortGPT), 2403.17887(Gromov) / HF alpindale/goliath-120b
- MoE: 2212.05055, 2208.03306, 2403.07816 / mergekit docs/moe.md
- 進化: 2403.13187(Sakana, NMI s42256-024-00975-8), 2505.11427(Mergenetic), 2605.12326, 2606.28373, 2503.18008(PriME) / mergekit docs/evolve.md
- 知識融合: 2401.10491(FuseLLM → github.com/fanqiwan/FuseLLM), 2402.16107/2408.07990(FuseChat), 2505.18502(GraftLLM), 2509.17276(PTA-LLM), 2402.12030(ULD), 2406.17328(DSKD), 2412.14528(MultiLevelOT), 2502.11104(CDM), 2503.20083(ALM), 2604.07466(BLD), 2405.07883(ZeTT), 2401.02412(CALM)
- 動的/推論時/基質: 2308.10248(ActAdd), 2310.01405(RepE), 2310.15213(Function Vectors), 2006.16236(Transformers-are-RNNs), 2405.16444(CacheBlend), 2404.09492(EVA), 1504.04909(MAP-Elites)
- ツール: github.com/arcee-ai/mergekit (arXiv:2403.13257)

---

> 関連: [[project_ros_physical_ai_2026_07_02]](gaitlab morphology-fusion 起点) / [[project_fullsense_unified_model_vision]](llcore×llive 統合の北極星) / [[project_llive_evolution_next_session]] / [[reference_low_memory_llm_wave_2026_06]] / open_model_architectures corpus(StateX head-merge, xLSTM expert-merging)。
> 生成: RAPTOR Workflow wf_46830988-559(調査 13 agents) + wf_707e48f0-838(多角検討 10 agents)。
