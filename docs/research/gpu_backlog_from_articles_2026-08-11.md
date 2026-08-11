# GPU 研究バックログ — 公開記事起点の棚卸し

**作成**: 2026-08-11 / **著者**: Claude (raptor セッション) / **依頼**: 「過去記事でやっていて、GPU ではまだそこまでやり込んでいないことがあれば作業計画に入れておいて」

---

## 1. これは何か

### 1-1. 位置づけ

既存の GPU 作業計画 `C:/dev/projects/fullsense/docs/research/gpu_pc_arrival_workplan_2026-07-24.md` の **Part B は「プロジェクト起点」**の棚卸しだった(各リポジトリの未達を並べて優先度を付けた)。
本文書は **「公開記事起点」**の棚卸しであり、Part B を置き換えるものではなく **補完する**。

問いはひとつ:

> **Qiita に公開した記事の中で「CPU 制約ゆえに小さく終わった / null で終わった /『次回に続く』で止まった」実験のうち、GPU で本気でやり直す価値があるものはどれか。**

対象は Qiita 公開記事 71 本(うち日本語オリジナル 25 + 30 本 = 実質的棚卸し対象)。突合先は Part B の B0/B1(P0-P3)/B2。

### 1-2. 前提(この文書を読む前に押さえること)

**(a) 「CPU ノートだけだった」は llcore については不正確。**
2026-06-06 の記事 #37(`6f44575d`)以降、llcore は **Kaggle 無料 T4(16GB / 週 30h)で計 164 runs を $0 で回している**。したがって llcore 系の律速は「GPU ゼロ」ではなく **「T4 16GB × 週 30h × ~0.5M params という机の狭さ」**。5090 は机を広げる道具であって null を破る魔法ではない。
一方 **ロボティクス系(onocollo / gaitlab / evis / myohand / hillco)は本当にノート CPU(i7-1065G7 15W)だけ**だった。ここは机の広さが桁で違う。

**(b) GPU 到着から 2.5 週間の実消化は Part B の優先度順ではない。**
GPU 期(2026-07-25〜)に実際に publishable な成果が出たのは 2 本のみ:

| 実績 | 実測 |
|---|---|
| llcore NAS の GPU フル走(記事 `e6988b226d40a5916522`・公開済) | 同一スクリプト・同一 seed の 751 evals を **CPU 6h06m → GPU 5m09s = 71 倍**。hypervolume **150.483 vs 150.483**(差 0.0005% は丸め順序)= 答えは変わらず待ち時間だけ消えた |
| hillco の MJX 筋歩行 | muscle sim throughput **CPU 3,400 → GPU 118,000 env-steps/s(35 倍)**。envs2048 で 1 本 ~3.9GB、条件違い 2 本並列で **11.4GB/32GB・util 92%** |

GPU 計算のほぼ全量が Part B P2 の hillco に投入され(onocollo-complete が 838 commit)、**P0 の本丸 3 件(箸 MJX rollout / 箸 閉ループ RL / llcore plateau プローブ)はいずれも未着手**。本文書の項目はこの空きスロットに入る。

**(c) Part B 作成後に判明した新規ブロッカー 3 件。**

| ブロッカー | 実測症状 | Part B への影響 |
|---|---|---|
| **Windows Smart App Control** | `HKLM:\SYSTEM\...\CI\Policy\VerifiedAndReputablePolicyState=1` により未署名 `mujoco.dll` のロードが拒否(CodeIntegrity 3077/3033, `WinError 4551`)。Off にすると再 On には Windows 再インストールが要る | Part B は「JAX が Windows 非対応だから MJX だけ WSL」と想定していたが、実際は **MuJoCo そのものが native Windows で動かない**。→ **WSL 経路一択**が MuJoCo を使う全項目に恒久的に効く |
| **XLA のメモリ/コンパイル限界(700 筋)** | BFC allocator で `Check failed: central_gap_` crash。platform allocator では GPU 51% で ~2000 steps/s(CPU 以下)。2026-08-08 再確認でも step-1 に 80 分以上到達せず | 700 筋のままの GPU 学習は**構造的に不可**。torque-twin(nu 700→49 / ntendon 700→0 / メモリ 11GB→4.5GB)か 92 筋経由のみ |
| **MJX 運用の実務制約** | 全 body collision でコンパイル 28 分+に爆発 / 足接地は primitive 必須(mesh 非対応) / `geom_margin=gap=0` / `XLA_PYTHON_CLIENT_MEM_FRACTION=0.7` / brax 0.14 × jax 0.11 非互換(shim 必須) / `nohup` はセッション終了で道連れ / 停止プロセスが VRAM を掴む | 新規モデルを MJX 化するたびに毎回かかる作業コスト。**ソルバ反復 100→4 でも 1.6 倍のみ**(14,727→23,960 substeps/s @512env)= ノブでは桁が動かない |

### 1-3. 規律(この文書が守っていること)

- **実測・実記録のみ**。記事本文・memory・実ファイル(JSON / ログ / git log)で裏を取れたものだけを書く。
- **「GPU を使えば解決する」と書かない**。null の由来を 3 分類する:
  - **予算由来** = 計算量・世代数・seed 数が足りなかった → GPU で破れる公算が高い
  - **表現由来** = モデル/方策/制御器の表現力不足 → **表現クラスを変えた上で** GPU 予算を積んで初めて部分的に破れる
  - **構造由来** = 手法・定式化・実験設計そのものが違う → **GPU を積んでも破れない**(§3・§4 へ回す)
- **29 件の候補を敵対的に検証し、10 件を落とした**。落とした理由は §3 に全部書く(honest disclosure。ここを消さないこと)。

---

## 2. 優先度テーブル(敵対的検証を生き残った 19 件)

`G#` は突合レポート(`gap_analysis.md`)の項目番号。トレーサビリティのため番号を維持している。

### Tier A — 記事が読者に約束した「数字の借金」(小工数・ブロッカーほぼ無し)

記事本文に「測っていない」「次回測る」と明記した数字。工数が小さく、GPU 効果が確実で、返さないと以後の主張が宙に浮く。

| # | 項目 | 由来記事 | 未消化の中身 | null 由来 | GPU で期待できること | 規模 | 既知ブロッカー | Part B との関係 |
|---|---|---|---|---|---|---|---|---|
| **G18** | **形式検証が弾いた promote の「節約された GPU 秒」実測** | `6ea53d9a`(llive v0.5.0) | 「構造的に矛盾する promote を GPU を回す前に弾ける。検証時間と GPU コストの両方に効く」は **設計主張のみで実測ゼロ** | 予算 | 弾かれた promote 群を記録し、意図的に通した場合の GPU 秒を対照測定 → 設計主張が初めて数字になる | S | **なし** | **新規** |
| **G4** | **自作推論エンジンの長文脈での逐点一致耐久** | `de27af958332c9c38e33` / `f660b18890687cfd1ed0` | 本文が「**測ったのはターン数の耐久であって文脈長ではない**(台本全体が文脈窓に収まる短さ)」と明記 | 予算(RAM 律速) | 128GB RAM + 32GB VRAM で長文脈 forward が素直に回る。公式実装との誤差ゼロ再現が長文脈でも成立するか確定 = **全 llcore ランタイム主張の土台** | S | なし(単発 forward 比較で済む) | **新規** |
| **G5** | **進化ループ多コア化の実測倍率 + ConvVAE 画素訓練の GPU クロスオーバー点** | `a65b9e84428fc7b7e63e` | 本文が「**この記事の GPU 高速化も MJX バッチも、まだ一度も走っていない**」と明記し、次回に (a) `--workers` の実測倍率 (b) ConvVAE 画素訓練がどこから GPU 有利に転じるか (c) MJX go/no-go の 3 数字を約束。(c) は hillco 側で実質達成(118k env-steps/s)だが **(a)(b) は公開用の数字として未払い** | 予算 | Core Ultra 7(24 コア)+ 128GB の携行 win が数字になる。ConvVAE のクロスオーバー点は以後の世界モデル計画の見積り根拠 | S〜M | **(a) は GPU 不要**(多コア CPU 測定)。GPU 枠として計上しない | 既載だが不足(P0/P1/P2 に散在。「記事が約束した 3 数字」という括りが無い) |
| **G1** | **「良い HW ほど効く」3 点の速度実測**(int8 GPU GEMM / mmap 大 RAM 共有ページ / 定数状態の長文脈) | `55b9cec764b7fdd96db8` / `c53c97d9eab745404982` | 本文が「**いずれも設計仮説で未計測、速度は本連載では測っていない**」と明記。CPU int8 は 0.7 tok/s で「解は GPU の int8 カーネルか GGUF 待ち」と書いた | 予算(ハード律速) | 記事が読者に約束した速度表を返せる。**★fp16 ベースライン併記が必須**(32GB では 1.5-4B は fp16 で余裕 → int8 の意義が 7B+/edge 配布寄りに再定義されるなら、その honest disclosure 自体が成果) | M | **int8 カーネルの sm_120 対応が未検証**。★実測訂正: 速度ベンチは `decode_latency_sweep.py` / `recurrent_latency_sweep.py` と CPU 実測 JSON(`out/latency_offload/latency-results/`)が**実在する**。書き下ろしが要るのは **int8 GEMM と mmap の 2 本だけ**。**mmap 大 RAM は GPU 不要** | 既載だが不足(P2「llcore int8 GPU カーネル」に速度表が無い) |
| **G2** | **needle 検索を signal のある base(1.5B/3B)で測り直す** | `55b9cec764b7fdd96db8` | ★実測訂正: 「2048 needle は UNTESTED」は誤り。`out/nas_pareto_v2needle`(2026-07-31)で GPU 実行済。だが **全 6 深度で `argmax_acc=0.0` / `horizon=null`**、`control_acc` は 0.40〜0.80 で非単調 = **Qwen2.5-0.5B base に passkey 検索能力が無く測定器に信号が無い**。メモリの壁(CPU 物理 RAM 3.6GB)は消えたが借金は返っていない | 予算 | 32GB VRAM で 1.5B/3B の probe を回せる。長文脈 needle で線形化ゲノムの良し悪しを初めて分離できる。分離しなければ「この規模では測れない」と正直に閉じられる | M | `nas_pareto_1p5b` では needle=null(未実行)。**まず `control_acc` と `argmax_acc` が分離することを確認してから frontier に適用する順序**が要る | 既載だが不足(P1 proxy v2 の context sweep は PPL/HV 側の話) |

### Tier B — 予算由来で見込みが最も高い(単調な効果が既に実測されている)

| # | 項目 | 由来記事 | 未消化の中身 | null 由来 | GPU で期待できること | 規模 | 既知ブロッカー | Part B との関係 |
|---|---|---|---|---|---|---|---|---|
| **G13** | **lldarwin 容量仮説: 集団 256→4096 / 潜在次元スケールアップを実 LLM で** | `6e107c7dfa0c261ee4d7` 第3章 §5.1,§9 / 第4章(#28)§7 | #28 §7 が「**規模を上げる。集団 256 → 4096、潜在次元のスケールアップ。容量仮説の確認**」と明記。**実 LLM 評価では一度も試していない**(実 LLM は 12h/71 世代/10.3 分per世代/小 pop のみ) | **予算**(proxy で単調な効果が実測済: latent 256→1024 で niche 101→166、archive 1021(飽和)→2234(成長継続)。母数スケールで niches 171→1219 / monoculture 0.047→0.006 / uniq_lineages 14→372) | ★**棚卸し全体で GPU で破れる見込みが最も高い項目**。単調性が測れているので予算由来と断定できる | M | ★**実測訂正: 順序制約は外れた**。依存ブロックだった飽和対策(旧 G14)は GPU 期に解消済(§3-2)なので**先行してよい**。残る注意は「gen9〜12 の局所最適収束」という別の壁 | **新規** |
| **G15** | **進化要素 PoC バッテリ 6 件(MODES / MCC / AURORA / 動的島 / CVT-MAP-Elites / persona-indexed)の実 llive 配線** | `project_lldarwin`(#27-#29 系記事群の派生棚卸し) | memory が明示的に「**全 PoC は proxy = 機構 feasibility のみ・実機スケールは GPU(新 PC)gated = 別フェーズ**」と書いた、棚卸し中で最も明快な GPU 待ち | 予算 | 6 要素すべて falsifiable gate 通過済(MODES: adaptive A_new **914** ≫ neutral 0.79 / MCC: frontier **1.565 vs 0.654 = 2.39x** / AURORA: coverage **0.574 vs handcoded 0.168 = 3.42x**、捕捉分散 2717x / 動的島: 占有 peak 2.0 vs 1.0 / CVT: D=8 で grid 2e-5 に対し **0.984**)。実 llive で本物の能力に効くか決着 | L | 横断教訓「**単一スカラー指標は誤判定しやすく AND gate 採用**」を実配線でも維持すること。**実 LLM fitness(Part B P1)の実走が先行依存** | **新規** |
| **G16** | **llive 非 Transformer: 低スペック bench harness の l / xl を実 backend で実走** | `aff262808a35cb7f7d3b`(2026-05-18) / `24ac90fb12c4e332d2b5`(2026-05-23)§5 | 記事に「**l / xl は GPU 環境が手に入るまで measurement paused**」と明記。実装済 = `benchmark/low_spec.py` に xs/s/m/l/xl × 5 backend の progressive matrix runner(cloud backend は `allow_cloud=True` 無しで refuse する on-prem 純度ガードつき) | 予算 | 実 backend での初の公開可能ベンチ。現状の **5,389,354 tok/s は echo backend の per-call overhead** で本文が「公開ベンチには絶対に使用禁止」と自己申告済 = 差し替えが必要。**2026-05-18「GPU の無い私の古いノート PC を主役にする」の完全な対**として連載の弧を閉じられる | M | `llive/docs/non-transformer/` は 2026-05-21 で凍結。**Part B に「非 Transformer」の語が 1 つも出てこない**。`feedback_llive_measurement_purity` に従い on-prem 単体で測ること | **新規** |
| **G17** | **llive 非 Transformer: MambaBackend(`transport='mamba_ssm'`)の直 in-process 実装 + Mamba 7B 実機 latency** | `7fa693bc2f1ae43ba5ba`(2026-05-21)§3 / `aff262808a35cb7f7d3b` §5 | ★**GPU 不在が唯一のブロッカーだったと本文に明記されている項目**:「**CUDA 依存。低スペック PC primary 方針と矛盾するため後回し**」。実物確認: `llive/src/llive/llm/backend.py:571` に `NotImplementedError` 現存(`RwkvBackend(transport='rwkv_py')` も 680 行で同様) | 予算(CUDA 不在) | 記事が公開ベンチ報告からの**想定値**として整理した Codestral-Mamba 7B Q4 の CPU only latency(xs ~500tok で 30-60 秒 / s ~2k tok で 3-5 分)を **5090 実機の実測値に置き換えられる**。「TRIZ で美しく整理した Mamba は O(L) で軽い、も GPU が無い人には届かない」という設計理想と実装現実の差が初めて数字になる | M | **`mamba_ssm` の sm_120 ビルド可否が未検証**(Triton/CUDA 依存)。native Windows は難所なので **WSL2 経路が現実的** | **新規** |

### Tier C — 記事が「GPU が来たら」と明記したのに Part B に項目が無い(新規ライン)

| # | 項目 | 由来記事 | 未消化の中身 | null 由来 | GPU で期待できること | 規模 | 既知ブロッカー | Part B との関係 |
|---|---|---|---|---|---|---|---|---|
| **G9** | **spikelab(SNN)の GPU 化・大規模化** | `44508c48f38a68abad35` | 記事が「`use_backend("cupy")` の **1 行で同じコードが GPU で走る設計**」「ここで作ったのは動く最小構成で、**まだ小さな玩具課題しか解いていない。派手な精度もまだない**」「**GPU が来たら、まずこの脳を大きくします**」と明記 | 予算 | cupy 導入 + スケール実測だけで記事の約束を返せる。LIF/発火の波/STDP/短期可塑性/サロゲート勾配が揃っているので、規模を上げた時に何が壊れるかが即わかる | M | **cupy の sm_120 対応版導入が最初の関門**。実在確認: `spikelab/src/spikelab/backend.py` に `use_backend()` 実装済(cupy 不在なら黙って numpy に縮退する fail-safe つき)= 移植コストはほぼゼロ。**最終 commit 2026-07-10 = GPU 期の活動ゼロ** | **新規** |
| **G10** | **性格ダイヤル(activation steering)を 3B 級で + 自作対話ツールへ搭載** | `44508c48f38a68abad35` | 実測 = 推論中の活性介入で感情と形式度が**直交して効く**(感情+で **+5.3**、形式度+で **+5.1**、合成も可)、可逆・再訓練不要。未消化 =「**今回のモデルは 1.35 億パラメータと小さいので、ダイヤルを回しすぎると文が壊れる(過剰操舵)**」「ゆくゆくは自作の対話ツールに載せて、その場で性格を回せるようにしたい」 | **表現**(135M の容量不足) | 32GB なら 3B fp16 は余裕で、過剰操舵は素直に規模で解ける公算。ActAdd は綺麗に効いた数少ない positive なので効果幅の拡大が期待できる。出口 = llove/llive への搭載 | M | 実在: `gaitlab/scripts/{persona_dial_demo,persona_steer_demo}.py`(最終 commit 2026-07-06)。**3B base は商用可ライセンスで選ぶこと**(`feedback_qwen_commercial_barrier`) | **新規** |
| **G11** | **openevolve(LLM 変異役のコード進化ループ)の実走と報酬ハッキング記録** | `40ba7cc91ac577274b74` | 末尾が「**次回は、この最小構成(openevolve + 手元の歩行シミュレーター)を実際に自宅 PC で回してみて、本当に CPU だけで進化するのか、報酬ハッキングは何回目で出るのかを正直に記録する**」と明言。加えて「ASI-Arch 的な設計図そのものを進化させる側は GPU が来た後」 | 予算 | 報酬ハッキングの発生回数という **honest disclosure 規律の教材**が取れる。ASI-Arch 的な設計図進化は GPU がないと始まらない | M | **実在確認: 専用 repo なし(完全未着手)**。LLM 変異役の on-prem backend(ollama)配線が先。設計(4 部品分解 / 評価器 3 層 sanity-task-audit+hold-out / ログ 7 項目 / 最初に踏む 3 失敗)は整理済 | **新規** |
| **G7** | **ロボット相撲 self-play 対戦 AI** | `44508c48f38a68abad35` | 記事が「**強い相撲 AI・対戦 AI は GPU が来てから。CPU 期でできたのは土俵・当たり判定・勝敗・簡易操作という遊べる場と骨組みまで**」と明記 | 予算 | 公開済 OSS(`gaitlab-arena`, Apache-2.0)に「強い AI」が載る。**self-play は対戦相手が強くなるので固定ものさし飽和(lldarwin #27 の病理)を構造的に回避でき**、並列数がそのまま効く = lldarwin 側の教訓の実証にもなる | L | **実在確認: 最終 commit 2026-07-05 = GPU 期の活動ゼロ**。**RL(PPO)スタックが onocollo/gaitlab に未配線**(Part B B0 が指摘する全 RL 共通ブロッカー)。§1-2(c) により MuJoCo は WSL 経路一択 | **新規** |
| **G8** | **産業用アームの学習方策 + 知覚(vision)化** — 記事が「FullSense フィジカル AI の本丸」と明記 | `44508c48f38a68abad35` | 「**やったのは幾何ベースの IK 制御であって学習ベースではない。学習で賢く掴むほうは GPU 待ち**」「残るはこの土管を学習した方策/タスク計画に差し替える部分。**カメラで箱の色を見て仕分けるように知覚を挟むのが AI 化の入口。これが FullSense のフィジカル AI の本丸**」 | 予算(ただし後述の注意) | CPU 期に Franka/UR5e/KUKA/Kinova の 4 機種で到達・pick-and-place・整列・パレタイジング・色仕分けを fail-closed で通した基盤がある。知覚(vision)を挟めば VLM 側(Part B P2)とも合流する | L | ★**記事が「本丸」と書いた項目が Part B に無いのが最大の抜け**。コード実在 `gaitlab/scripts/{arm_reach,pick_place,production_line,reach_fail_closed}.py` だが GPU 期の活動ゼロ。RL スタック未配線。**★honest 注意: 「学習が幾何 IK に勝つ」型の主張は自前に決定的な反例がある**(rocket robust NULL 0/10 seeds、2.5 倍予算頑健性)。**価値は RL 側でなく知覚(vision)側にある**と位置づけること | **新規** |
| **G6** | **坂・階段・不整地の踏破学習 + 背高機体(ANYmal C)の閉ループ制御** | `44508c48f38a68abad35` / `d7e3f943e9a2e68aca5d` | 記事が「**環境を作るところまでが CPU 期の仕事で、本格的な学習は GPU 待ち**」「背の高い機体ほど閉ループや学習した制御が要る。**ここも GPU 後の宿題に足しておきます**」と明言 | **表現**(CPU 期に 3 直感=重心を上げる/高摩擦にする/足上げ報酬を強める、を**すべて対照実験で反証**済。摩擦 1.2→2.5 は登坂を悪化 → 上限はバランス/歩容にある、と分離済み) | 6-8° 止まりの斜面上限(9°~0 / 10° 滑落)を超え、**階段(第 1 段 0.08m)の登破に初めて挑める**。数千環境並列 RL は一度も試していない。開ループ正弦波で数秒で転ぶ ANYmal C を閉ループ化できる | L | **MJX の hfield(階段・不整地)接触対応が未確認**。gaitlab 最終 commit 2026-07-06 = GPU 期の活動ゼロ。WSL 経路一択。★**GPU は探索を速くするだけで、破るのは「高クリアランス歩容」という制御構造**である点を明記して着手すること | **新規**(Part B の gaitlab 項は factorial/hybrid の大予算再測定であって地形踏破学習を含まない) |

### Tier D — llcore の「机を広げる」(Kaggle T4 → 5090)

| # | 項目 | 由来記事 | 未消化の中身 | null 由来 | GPU で期待できること | 規模 | 既知ブロッカー | Part B との関係 |
|---|---|---|---|---|---|---|---|---|
| **G20** | **合成 proxy fitness → 実 GPU 訓練での feasibility 実測** | `cc0713ab78a5b390df76` 第2章 §3.4 | 本文に「**ここの fitness は RotationNDObjective の合成 adapter proxy で、実 GPU 訓練では base forward(CE)が dominant になる。この外挿は保守的上限見積りで、実 GPU 実測は Phase 2 で要確認**」と明記。per-op 実測 wall-time から 30 時間予算へ外挿し small-n(n≤6)は予算の 0.04%、2ⁿ 壁は n≥10-12 で binding と判定した、**その外挿の検算が未実施** | 予算(未実施) | **予算表そのものの妥当性が確定**し、他の llcore GPU 作業(G22/G19)の見積り根拠になる | M | 実 GPU 訓練では base forward(CE)が支配的になるため proxy とは別の律速要因が現れる可能性。**外挿が楽観だった場合は他項目の計画も縮む** | **新規** |
| **G22** | **vertex-free 証明器の ground truth 生成を n=20 前後まで押す** | `cc0713ab78a5b390df76` 第4章 §3.7 / `llcore/research/verifier_cost_reduction/poc_scale_results.json` | vertex-free 証明器(poly(n))は PoC 実装済で **n=8/12/16 の coverage 78.46 / 69.28 / 57.14%・soundness 違反 0**。ボトルネックは **n=16 の ground truth 生成に 510.2 秒** | **予算(ただし ground truth 側だけ)** | coverage 曲線を n=20 前後まで延ばせる。57.1%(n=16)から先の傾きが見えれば「高次元で navigable かつ sound な証明器は不在」という**第一級 negative の輪郭が確定する** | M | ★**証明器本体の指数は消えない**(GPU は定数倍で n=14→20 程度)。**「2ⁿ の壁を GPU で破る」と書いてはいけない**。対象は ground truth の 2ⁿ 頂点 SVD バッチ化のみ。**n≥20 のバッチが 32GB に載るかは未計算** | **新規** |
| **G19** | **安全ゲートの「税率」はスケールで同じ顔か + HD-1 の実モデル接地** | `6f44575d440a9ebf5228`(2026-06-06) | 記事末が明示的宿題: 「**今日の値段表は ~0.5M params・文字レベル・1 コーパスという小さな机の上で測ったもの。この税率はモデルを大きくしても同じ顔のままなのか?**」 | 予算 | 実測済の内容 = ゲートなし gradient は全次元で安定領域を離脱(**19/20 seeds、n=256 で ρ→1.95**)、越境は entropic drift(null=shuffle でより強く **ρ→2.61** かつ CE 利得ゼロ = edge-of-chaos 棄却)、記憶コアは load-bearing(4/4)、後付け証明は訓練ループ内の **17-19 倍**高い。**★HD-1 自身が「feasibility で安全に見えた結論が full で符号ごと変わる」を実証済**なので、**予算依存性は仮説でなく実測済の性質** | L | T4 16GB × 週 30h → 5090 32GB 無制限へ「机が広がる」だけで、**税率が変わらない保証はない**。1 年スパン方針で submission を急がない前提 | **新規** |

### Tier E — 非 GPU だが順序上これを先にやらないと GPU 予算を捨てる

| # | 項目 | 由来記事 | 未消化の中身 | null 由来 | 何が起きるか | 規模 | Part B との関係 |
|---|---|---|---|---|---|---|---|
| **G29** | **gaitlab 派生 #4/#5: 多目的 QD-score の導入と目的の脱相関** | `project_gaitlab_derivative_plan_2026_07_03` / `44508c48f38a68abad35` | #4 =「現 `qd_score` が**単目的(前進距離)**で MOME の多目的保持を credit しない」。#5 =「speed/forward・uprightness/height の相関で**実効目的数が ~4-5、`gait_symmetry` は全 arm 0.0 = 退化**」と実測 | 予算(だが**作業自体は GPU 不要**) | ★**過去の比較が apples-to-oranges だったという自己申告の是正**。放置すると以後の全 gaitlab 比較が汚染される。要る作業 = hypervolume ベースの多目的 QD-score + PCA/whitening による目的脱相関。lexicase×MOME の条件付き相乗(文献未発表)という CPU 期の成果が、正しい指標で測り直されて publishable 強度になる | M | **新規**(Part B P3 の「gaitlab K×ε sweep・QDax 化」とは別項目)。★**Part B P1 の gaitlab MJX 大予算再測定をこの是正の前に走らせると、汚染された指標で大予算を捨てる。順序が load-bearing** |

### 2-1. 着手前に潰すべき技術ブロッカー(横断)

| ブロッカー | 影響する項目 | 状態 |
|---|---|---|
| `cupy` の sm_120 対応版導入 | G9 | 未検証 |
| `mamba_ssm` の sm_120 ビルド(Triton/CUDA、WSL2 経路) | G17 | 未検証 |
| int8 カーネルの sm_120 対応 | G1 | 未検証 |
| MJX の hfield(階段・不整地)接触対応 | G6 | 未検証 |
| n≥20 の ground truth バッチが 32GB に載るか | G22 | 未計算 |
| RL(PPO)スタックの onocollo/gaitlab への配線 | G6 / G7 / G8 | 未配線(Part B B0 が指摘済の共通ブロッカー) |

---

## 3. 却下した候補と理由(honest disclosure — ここを消さないこと)

候補 29 件を実ファイル・実 JSON・memory で裏取りして敵対的に判定し、**10 件を落とした**。内訳は「構造由来で GPU では破れない」4 件、「既に実施済み」4 件、「GPU を必要としない/GPU 枠に入れると誤配分」2 件。

### 3-1. 構造由来 — GPU では破れない(GPU 予算として計上してはいけない)

| # | 候補 | 却下理由(一次確認できた事実) | 再登録の条件 |
|---|---|---|---|
| **G3** | memetic-vs-greedy verdict の決着 | ★**計算量では絶対に破れないことが記録から確定**。`nas_pareto{_1p5b,_gpu_f32,_v2cross,_v2distill,_v2full,_v2long,_v2needle}` の **全 7 本で `verdict.confidence="suppressed"`**。notes は v2needle で「**max optimism_gap 0.0517 > CI half-width floor 0.0150**」、1p5b で「**0.0368 > 0.0264**」。全本が `holdout_windows=12.0` / `holdout_offset=8192` を払い済で、cross-corpus(shakespeare)も 4096 sweep も 1.5B も払い済。suppression は「**選択楽観 vs CI 半幅の床**」という決定論的規則で、**窓や seed を増やすと床が縮むので判定はむしろ厳しくなる**。記事の想定「K≥12・seed 増で決着可能」は反証された | 中身自体は正しいので **非 GPU の評価設計タスク**として別枠に置く(§4)。nested selection / genome の事前登録 / floor を optimism 込みに再定義 |
| **G23** | 地形改造 E/F/G(verifier-shell / しりとり / 折句) | ★**決定力が両方向で低い**。③QD は M3(Kaggle T4, 88 runs)で **NEGATIVE(decisive)**、原因は素の next-token-CE 地形が擂り鉢 = **目的関数の幾何**であり構造由来。人工的に多峰な地形を作って ③ が立っても「そう作ったから立った」= **Goodhart 型の自作自演**で実 LM 目的に戻らない。立たなければ negative が 1 件増えるだけ。実在確認: `llcore/research/` 全 40 ディレクトリに terrain/shiritori/verifier_shell 系は皆無 = **L のうち大半が GPU でなく実装工数**。記事の実測「admit は σ=0.005 で 0.21、σ≥0.01 で 0」は多峰というより**許容帯が極端に狭い針の穴**を示唆し、多峰化の前提自体が怪しい。★**実測訂正: `PHASE_2_VERDICT.md`(2026-06-09)が既に「合成多峰地形でも MAP-Elites は gradient/random と held-out で区別不能(NULL_TIE)」を出している** | しりとりのみを **S 工数の tiny probe として CPU で実装**し、地形が実際に多峰(複数の分離した局所最適)であることを可視化で示すこと。それが出てから初めて GPU の話 |
| **G24** | memetic NAS の mixer allele 拡張(SSM / RWKV) | 実測確認: `nas_pareto_v2needle` / `nas_pareto_1p5b` とも `mixers=['softmax','sliding','linear']` で現状把握は正しい。**しかし 2 つの反証で失格**。(1) **訓練済み重みの無い SSM/RWKV mixer を allele に足しても、その層はランダム初期化相当で NLL が壊滅し、探索は構造的にその allele を選ばない** = frontier は現状のまま。真に要るのは**層ごとの蒸留レシピ**(linear 化で per-layer 91-98% を出したのと同等のもの)= 探索予算でなく手法開発。(2) allele を増やすと候補数が増え **optimism_gap が拡大** → G3 の suppression 規則により **探索空間を広げるほど verdict は出なくなる** | (a) SSM/RWKV の per-layer 蒸留レシピが small スケールで動くこと (b) G3 の評価設計修正が入ること。**両方が揃ってから** |
| **G27** | 自作 ape ロボへの mocap retarget → 模倣学習 | 提案自身が「**GPU が破るのではない**」と書いており GPU 項目として失格。さらに強い反証: 同じ「自前モデルへ mocap を retarget して追従させる」を **evis で既に実施し失敗**している。参照 `evis_cpg_cycle_seg.npy` に対し PD 追従(kp60)は関節 RMS 5.8° で追従できるのに **1.15s で転倒**、診断は両足浮き 60% / 単脚 38%。参照自体は健全(キネマ再生で両足浮き 0 / 単脚 98%)と分離済 = **問題は参照の不在ではなく execution(単脚支持を再現できない)**。結論は「per-joint PD では force-closure を保持できない、WBC-QP + 単側接地拘束が要る」。∴「良い参照さえあれば模倣できる」という前提が同チームの実測で既に反証されている。★実測訂正: 「retarget パイプライン未実装」も誤りで、`src/onocollo/evolve/mocap_retarget.py` + CMU BVH 取得(商用可ライセンス検証済)が既存。未なのは ape への適用と動力学模倣 | **安い再登録ゲート**: ape ロボの足が bc3 の成功した box 足に近い**平板・広接地**なら BC は通り得る(足裏を 6 割に縮めただけで BC 11m→2m に崩壊した実測が示すとおり、成否は接地形状が支配する)。**まず ape の足ジオメトリを確認する S 工数だけを実施し、平板でなければ着手しない** |

### 3-2. 既に実施済み(GPU 期にやってある — 新規計上すると重複)

| # | 候補 | 実施の証拠 |
|---|---|---|
| **G14** | lldarwin 飽和対策 3 点(適応難易度 / factor-subspace QD / MAP-Elites)の実 LLM 検証 | ①天井効果は hard_v2 バッテリで解消済(`out/persona_evo_main_realpressure_s2/run_manifest.json` = fitness real-pressure / battery hard_v2 / selection lldarwin-v2 / lineage_reservoir true / novelty_filter on、best が 1.0 に張り付かない)。②それでも進化しなかった真因は多様性機構ではなく **genome→phenotype gap(変異が表現型に届かない)** と特定・修理済(`llive/docs/genome_phenotype_gap_2026-07-28.md`, `fitness_llm_scoring_repair_2026-07-28.md`)。③修理後の実 LLM 実走(`llive/docs/evolution_50gen_3seed_2026-07-29.md`、seed 0/1/2 各 50 世代・**計 171.9 分**)で mean が **+0.095 / +0.125 / +0.111** と 3 seed 再現して上昇し、「#27 の gen5 で 1.0 飽和 = filtered random search」病理は**脱却済**。残る壁は gen9〜12 の局所最適収束で、想定した「固定ものさし飽和」とは別物。→ **残余があるとすれば「修理後の fitness の上で factor-subspace QD / MAP-Elites を再評価する」というより狭い別項目** |
| **G21** | Mamba 固有安定性(base-level Lyapunov)の測定 | `llcore/research/rllm_pivot/phase2_mamba_lyapunov.py` + `phase2_mamba_lyapunov_results.json`(2026-06-09)が `state-spaces/mamba-130m-hf`(n_layer=24, d_inner=1536, state_size=16)に対し **A=-exp(A_log)<0、離散 Ā=exp(Δ·A) から λ_max=max(Δ·A)≤0 を Δ∈[1e-4, 1e2] の全域で閉形式に確定**。結果 JSON 自身が honest_caveats で「**Not a weak oracle: A_log / dt_proj.bias are first-party weights; λ_max is exact for the diagonal SSM eigenspectrum**」と明記。記事が「Phase 2 送り」とした base-level Lyapunov はここで払われている。加えて **GPU 無関係**(130M の摂動応答測定に 5090 が要る根拠がない)。未測定として残るのは SSM 状態再帰ではなく **Mamba ブロック全体(conv1d / SiLU ゲート / in-out projection / MLP)の Lipschitz 定数**で、これは別の(より重い)項目 |
| **G25** | 解剖学的足(box 無し)の持続歩行と押し耐性ロバスト化 | **GPU 期の現行主線そのもの**で「まだやり込んでいない」に当たらない。onocollo-complete は 2026-08-10〜08-11 に稼働中: `out/rl_footflat_long2.log` FINAL は feet='anat' で under_push 評価つき(**VERDICT_walks false / VERDICT_robust false / survive_s 3.77 / pelvis_fwd_m 4.287**)、`out/rl_robust_s1.log` は 5.98M step まで回して EVAL survive_s 2.23、`out/rl_robust_track.log` は bc=0.49 の追従つきで survive_s 1.75。`scripts/evis_video/sweep_out5`(08-10)の kl×sf グリッド掃引、`walk_search.py` / `walk_verify.py` も 08-10 更新。さらに 2026-08-11 の `docs/hillco_body_language_requirements_2026_08_11.md` が「**end-to-end 49 自由度 PPO は 19.66M step 使っても 2 秒しか立てない**」「**桁削減は PPO を捨てて決定変数を接地点に落とす構造変更からのみ来る**」と結論し、ポーズ語彙+状態機械への構造変更へ既に方針転換済(§4) |
| **G26** | 700 筋人体の立位: 制御表現の変更(recurrent / 明示的な足首・腰戦略 / 階層) | **2026-08-04 に実施済**。`onocollo-complete/scripts/evis_video` に `recurrent_train.py`(GRU バランス方策を ES で end-to-end 学習)、`synergy_train.py`(100 筋を残したまま解剖学マクロで制御 = 階層化)、`capture_point_train.py`(明示的な capture-point/CoP 法則)、`posture_train.py`(stand→onefoot→crouch→squat のカリキュラム)、`ppo_stand.py` が実装され、成果物も `out/musculo/evis_balance/` に `gru_{gru_raw,gru_syn,stand_hard,stand_long}.json` + `gruchampion_*.npy`、`ppo_{of_w20,ppo_alt,ppo_crouch}.{json,pt}` として残る。**実測は厳しい**: 解析的 CoP 法則は honest negative(0.24s→0.66s→gain 掃引 35 セルで 1.10s→姿勢 PD 掃引 45 セルで 1.16s、既存線形方策の 4.8s に届かず、しかも 0.27-0.53m ドリフトで anti-topple ゲート不合格)、GRU+F12 synergy **4.61s** / GRU+F12 raw 1.87s、**ES は制御クラス・行動空間・特徴・目的・初期条件・最適化器を跨ぐ 10 試行すべてで 8 秒エピソードの ~4.6s 天井**、**held-out ゲートは全条件 0/8**。加えて計算経路も塞がっている(700 筋 MJX-GPU は XLA 限界)。**記事の宿題は払われ、表現を変えても天井は動かなかったという答えが出ている** |

### 3-3. GPU を必要としない — GPU 枠に入れると誤配分になる

| # | 候補 | 却下理由 | 置き場所 |
|---|---|---|---|
| **G12** | 箸 stage-2: 滑り/潰し予測の低次元世界モデルを進化の QD gate に | ★**自前に直撃の反証記録がある**。(1) **世界モデル h\*=0**(`project_onocollo_freefloat_2026_07_20`): Dreamer RSSM は reacher で **ConstantVelocityPredictor(qpos+=qvel*dt という物理なしベースライン)に短 horizon で負け、長 horizon でも CI が重なり一度も CI-separated win なし**。今回提案する「低次元で滑り/潰れを予測するモデル」は**まさに同じ形の学習予測器**で、同チームで直近に null が出ている。(2) stage-1 で素朴な線形方策が易しい箱でも scripted 制御に負けた(contact ~0.5 vs held ~6)のは、予算というより**方策表現が弱い証拠**。(3) Part B P0 が既に「箸 閉ループ力制御 RL」を最重要枠で押さえており**資源競合**。∴ GPU 予算 L を割く根拠が立たない | **再登録の条件**: 学習モデルの前に**自明ベースライン(接触力と摩擦円錐から解析的に滑りを判定する式)**を実装し、学習予測器がそれを CI 分離で上回ることを **S 工数**で示すこと。上回れなければ QD gate として無価値であり、これは GPU では変わらない |
| **G28** | 宇宙ゴミ捕捉: 学習型コントローラ vs 強い手設計反応ベースラインの決着 | 「予算由来」という自己判定に対し**同チームの反証が 2 件**。(1) rocket 着陸の eval-signal 実験は**完全に同型の問い**(学習は公平にチューニングされた PID に勝つか)を事前登録 + 10 seeds + 4 skeptic で検証し **robust NULL**(0/10 seeds positive、TEST 全 3 stream で CI が 0 をまたぐ)。しかも「評価を良くすれば勝てる」という仮説自体が検証されて**タイ止まり**。(2) 本プロジェクト内でも**2.5 倍予算でも greedy は 2-3 節に収束 = 「探索問題≠予算」**と明記済。さらに手設計側は制御 knob 調整だけで難タスク捕捉を **0.40→1.00** に上げており、ベースラインが極めて強い。∴ GPU 予算 M を積んで学習が勝つ見込みは低く、「予算由来の null」という分類は支持できない | honest な決着自体には価値があるので、**GPU バックログではなく「予測 = タイ」と事前登録した S 工数の締めくくりタスク**として残す。**運動量保存オラクルの維持**(偽陽性摘発の実績あり)と **paired CI** は必須 |

### 3-4. 分類の訂正(記録として残す)

- **「GPU で破れる」と書けない構造由来が 5 件**あった: G3(評価設計)、G12(世界モデル h\*=0 の前例)、G23(目的関数の幾何)、G26(前額面安定 + XLA 限界)、G27(execution = force-closure)。
- **そもそも GPU を必要としない項目が 3 件混入していた**: G5 の `--workers` 多コア測定、G21 Mamba Lyapunov、G29 gaitlab 指標是正。**G1 の mmap 大 RAM も同様**で、これらは GPU 到着から 2.5 週間ずっと measurable だった = **ブロッカーは資源でなく着手順**。
- **「学習が手設計に勝つか」型**は自前に決定的な前例(rocket robust NULL、2.5 倍予算頑健性)があるため、G8 の RL 半分と G28 は**予測 null として小さく事前登録**すべき。G8 の価値は知覚(vision)側にある。
- **G25 は割ると片方だけ生きていた**: 持続歩行は長 run で 1.3→2.0→5.3s と実際に壁が動いた**予算由来**、押し耐性は RL 3/3 崩壊で**表現由来**。ただし現行主線なので新規計上しない。**best ckpt(5.3s / 6.6m / 11.3 歩)と最終 ckpt ログ(survive_s 3.77 / VERDICT_walks false / 完走率 0.0)の乖離は必ず併記すること**。

---

## 4. 構造変更が要るもの(GPU の問題ではない)

以下は「GPU 予算を積む」ではなく「**手法・定式化・実験設計を変える**」タスク。GPU バックログとは別に管理する。

| 項目 | なぜ GPU では破れないか | 本当の一手 |
|---|---|---|
| **memetic-vs-greedy verdict**(G3) | suppression は「選択楽観 > CI 半幅の床」という決定論的規則。**窓を増やすと床が縮んで判定は厳しくなる** | **nested selection**(選択そのものを holdout の外に出す)/ **genome の事前登録**(選択楽観をゼロにする)/ **floor の定義を optimism 込みに変える**。いずれも評価設計の変更で計算量ではない |
| **llcore plateau の実験設計交絡**(Part B P0 の実行前提) | ★**Part B P0 をそのまま実行すると計算を捨てる**。2×3 ablation の全 null を自己摘発済 =「**carry-on も `chunk_size = block_size = 128` で勾配が依然 128 truncate = credit assignment が切れたまま = 未完全検証**」。文献側の帰属も「plateau null の本命 = TTT。本質は容量でなく **BPTT 越えの credit assignment**。StateX は容量を足すだけで未解決」 | **`chunk_size > 128` へ設計修正**してから GPU フル走。加えて忠実データ依存ゲート版、full-BPTT segment × train_seq_len 掃引、TTT-Linear 層の試作 |
| **hillco 歩行の桁削減**(現行主線の方針転換) | `docs/hillco_body_language_requirements_2026_08_11.md` が「**end-to-end 49 自由度 PPO は 19.66M step 使っても 2 秒しか立てない**」「桁削減は PPO を捨てて**決定変数を接地点に落とす構造変更**からのみ来る」と結論。ソルバノブも 100→4 で 1.6 倍のみ | **ポーズトークン(埋め込み + 128bit 識別子)+ 内容アドレス状態機械 + 学習遷移**への再設計。survey → 要件定義 → PoC |
| **march_qp(QP-WBC)の前額面安定化** | ~110 run のどの領域でも **3.4-3.5s 天井**で、転倒モードは前額面(COMy)の横倒れ。真因は**コントローラの自家撞着** = 両足支持中の横 COM 目標が「両足の真ん中」固定なのに踏み替えトリガは「片側に寄ったら」で両立不能、**一度も発火しない** | `march_qp.py --ds-shift`(**実質 1 行**)+ `sweep_fwd_qp` の前進加点除去 → 生存≥5s / 両足浮き<0.15 / 片足支持≥0.3 で判定。股側方・脊柱側屈・足配置の横成分を破ること |
| **700 筋の GPU 学習** | XLA のメモリ/コンパイル限界。VRAM を増やしてもグラフ構築が通らない | **torque-twin(nu 700→49)or 92 筋で先に歩行を実証 → 筋へ蒸留**。700 筋のままの GPU 学習は放棄が正解 |
| **世界モデルが実タスクでランダムに負ける** | 「もっと計算すれば良くなる」を測ったら**逆に悪化**した(world-model exploitation)。ドリフト誤差は persistence ベースラインの数百〜千倍 | **DreamerV3 忠実化**(categorical / symlog / two-hot / REINFORCE)が前提。Part B P2 が「V3 化とセットで」と書いているのは正しい |
| **ロケット風あり held-out の robust NULL** | 機構が判明済 =「**定常横風を打ち消すには積分や内部状態が要るのに memoryless な残差にはそれが無い**」。recurrent も転移せず。eval 改善は負け→引き分けまで押すが勝ちは作らない | GPU で破れる筋は無い。Part B P1 が「throughput 実証のみ」に限定しているのは**正しい判断**。併記すべき留保 =「fit チャネルは検出力不足(d<0.03)= 意味ある勝ちが無いのであって効果ゼロの証明ではない」 |
| **LLM マージ(QD/TIES)の 2 連続 null** | 進化探索 0.797 を細かくした素朴な task arithmetic 0.838 と比較して**偽陽性を自己摘発**(粗 7 点グリッドの解像度アーティファクト、λ=0.68 で逆転)。「単一の差分を層別に混ぜる問題は**結局ほぼ 1 次元**で、たった一つの均一な λ をちゃんと調整すれば足りた」 | 探索量を増やしても均一 λ には勝てない。破るなら設定を変える = **より大きい / 真に衝突する expert 集合**での再検証 |
| **虫(flybody)のホバリング** | 前主張「翼 150Hz で thorax +0.97cm = 飛行 feasible」は**床の脚押し上げ artifact と自己摘発**。床なしでは無羽ばたき −128.9cm/1s 落下、最良 open-loop 翼打ちでも約 23% 抑制のみ | 空力モデル・羽ばたき運動学の作り直し → その後に閉ループ学習制御(flybody 論文は figure-8 + 学習制御で hover 達成)。**GPU 予算の話にしない** |
| **Step C 5-bit パリティの床** | positive control が決め手: **degree-2 readout は 2-bit XOR を厳密に解く(R²=+1.0)が degree≥3 で破綻**。5-bit パリティ = degree-5 = CPU reservoir + ridge パラダイムの構造的限界 | **readout の非線形化**(パラダイム変更)。reservoir を大きくしても ridge の次数の壁は動かない |
| **筋の体積表現 b2(force-from-volume)** | **MuJoCo に能動収縮体積が存在しない**(flex = 受動 tet のみ、skin = visual 専用)。全身 active-FE は motion 毎に数時間 | **S5 に隔離**: FEBio/ArtiSynth で単筋 ground truth を offline 生成 → neural surrogate。**offline batch は GPU が効く経路なので b2 本体と混同しないこと** |
| **MyoHand → evis graft** / **蛇の 3D 立体登攀** | 前者は壁がモデル接続・weld 位置・箸先幾何。後者は `morphology.py` が**単軸関節のまま** = そもそも 3D 登攀の自由度が無い | 前者は「配置時に接触力が 0 であることを assert してから閉じる」等の実測手順。後者は **2 軸関節化**してはじめて予算問題になる |

---

## 5. 着手順序の提案

### 5-0. 原則

1. **是正を先に**(飛ばすと後の大予算が汚染される): G29 gaitlab 多目的 QD-score → **その後で** Part B P1 の MJX 大予算再測定 / plateau の `chunk_size > 128` 設計修正 → **その後で** Part B P0 のフル走。
2. **借金を小工数で返す**(Tier A)。ブロッカーが無く、返さないと以後の記事主張が宙に浮く。
3. **ブロッカー検証は先に単独で潰す**(cupy / mamba_ssm / int8 の sm_120)。本作業とセットにすると「環境で 2 日溶けた」になる。
4. GPU は 1 枚だが **envs2048 の学習が ~3.9GB / 32GB** と実測されており「GPU 1 枚 = 学習 1 本」は撤回済。**短い CPU 寄りタスクと長い GPU 学習は並走させる**。

### 5-1. 最初の 3 件と go/no-go 判定基準

#### 第 1 件: G18 — 形式検証が弾いた promote の「節約された GPU 秒」実測(規模 S・ブロッカー無し)

- **やること**: llive の形式検証で弾かれた promote 群を記録 → **意図的にゲートを外して通した場合に消費したはずの GPU 秒**を対照測定する。
- **go 判定**: 弾かれた promote が **N≥20 件**集まり、「通した場合の GPU 秒」の中央値と分布が出る。→ 記事化し、FullSense の設計哲学(責任所在を architecture level に / Approval Bus を迂回しない)を支える数字として公開。
- **no-go 判定**: 弾かれた promote が実運用でほとんど発生しない(N が小さい)場合 → 「**主張は成立するが量的に無意味**」と honest に閉じ、次へ進む。ここで「サンプルを増やすために人工的な矛盾 promote を作る」ことは**しない**(Goodhart)。
- **なぜ最初か**: ブロッカー無し・工数 S・GPU 占有ほぼゼロで、設計哲学を直接支える数字が取れる。費用対効果が最も高い。

#### 第 2 件: G4 — 自作推論エンジンの長文脈での逐点一致耐久(規模 S・ブロッカー無し)

- **やること**: 自作推論エンジンと公式実装を、**短文脈で確認済の逐点一致(誤差ゼロ)が長文脈でも成立するか**単発 forward 比較で検証する。文脈長を段階的に伸ばして乖離開始点を探す。
- **go 判定**: 長文脈でも max abs diff が短文脈と同オーダー → **PASS**。「多ターン耐久しか測っていない」という記事の自己申告を解消し、以後の llcore ランタイム主張(線形化・蒸留・定数状態)の土台が固まる。
- **no-go 判定**: ある文脈長から乖離する → **乖離開始長と数値誤差の増え方を特定して honest に開示**。これも成果(むしろ重要な発見)。ただしその場合、**乖離長を超える文脈での既存主張はすべて留保に変更**する必要がある。
- **なぜ 2 番目か**: 工数 S・ブロッカー無しで、**他の llcore 項目(G1 / G2 / G20)の前提**になる。ランタイムが長文脈で正しくないなら、その上で測る速度も needle も意味を失う。

#### 第 3 件: G2 — needle 検索を signal のある base(1.5B/3B)で測り直す(規模 M)

- **やること**: **段階 1 = 測定器の健全性確認**。1.5B(最低)〜3B で `--needle --needle-lengths 2048,4096` を回し、`control_acc` と `argmax_acc` が**分離すること**を先に確認する。**段階 2** はそれが通ってから frontier(線形化ゲノム)に適用する。
- **go 判定(段階 1)**: `argmax_acc` が **深度依存で有意に > 0** になり、`control_acc` と分離する(0.5B では全深度 `argmax_acc=0.0` / `horizon=null` だった)。→ 段階 2 へ進み、長文脈 needle で線形化ゲノムの良し悪しを初めて分離する。
- **no-go 判定**: 3B でも `argmax_acc` が 0 に張り付く / `control_acc` と分離しない → **「この規模では測れない」と正直に閉じる**。needle probe を frontier 評価から外し、記事の「2048 needle」項目は未達のまま据え置く。**この場合に「もっと大きい base で」と際限なく積まないこと**(それは測定器の設計問題であって予算問題ではない)。
- **なぜ 3 番目か**: 記事が読者に約束した数字であり、かつ**壊れた測定器で frontier を測ると全部無駄になる**ため、順序が load-bearing。

#### 並走させる長時間 GPU ジョブ: G13 — lldarwin 容量仮説(集団 256→4096 / 潜在次元)

上記 3 件はいずれも GPU 占有が小さいので、**バックグラウンドで G13 を回す**。依存ブロックだった飽和対策は GPU 期に解消済(§3-2)なので先行可能。

- **go 判定**: 集団 256 → 1024 → 4096 の 3 点で **niches / uniq_lineages / monoculture が proxy と同じ向きに単調変化**する。→ 記事 #28 §7 が明記した「容量仮説の確認」を実 LLM で返せる。
- **no-go 判定**: 実 LLM では単調性が再現しない(例: 4096 でも niches が飽和する)→ **「多様性は容量で買える」は proxy 固有の性質だった**と honest に開示。この場合、gen9〜12 の局所最適収束(実測済の別の壁)が真のボトルネックであることを示す証拠になる。
- **中止条件**: 1 世代あたりの実 LLM 評価が予定の 3 倍を超える → 集団サイズでなく**バッチ推論のスループット**が律速なので、先にそちらを直す。

### 5-2. 第 4 件以降(参考順)

1. **ブロッカー検証 3 本**(cupy sm_120 / `mamba_ssm` sm_120 / int8 カーネル sm_120)を独立に潰す — 各 S。通らなければ G9 / G17 / G1 の計画を書き換える。
2. **G5 → G1** — 記事が約束した数字を返し切る(`--workers` は CPU 測定なので GPU 待ちにしない)。
3. **G29** — gaitlab 指標是正(**Part B P1 の MJX 大予算再測定より前**)。
4. **G9 spikelab → G10 性格ダイヤル → G11 openevolve** — いずれも M。記事が「GPU が来たら」と明記した新規ラインの中で最も安い。
5. **G17 → G16** — llive 非 Transformer トラック(2026-05-21 凍結)の復活。連載の弧を閉じる。
6. **G20 → G22 → G19** — llcore の机を広げる。G20 は他項目の見積り根拠なので先。
7. **G7 相撲 self-play / G8 アーム学習+知覚 / G6 地形踏破** — いずれも L で **RL スタック配線が共通の前提**。3 件まとめて配線してから着手するのが経済的。G8 は**知覚(vision)側を主目的**にすること。
8. **G15** — 進化要素 PoC 6 件の実 llive 配線(Part B P1 の実 LLM fitness 実走に後続)。

---

## 6. 未確認事項(調べきれなかったこと)

### 6-1. 技術ブロッカーの可否(すべて未検証)

| 項目 | 何が未確認か |
|---|---|
| `cupy` sm_120 | Blackwell 対応版の入手可否と、`spikelab` の `use_backend("cupy")` が実際に numpy と同じ結果を返すか(fail-safe が黙って numpy に落ちる設計なので、**落ちたことに気づかず「GPU で測った」と誤報告するリスク**がある。ログで backend を明示すること) |
| `mamba_ssm` sm_120 | Triton / CUDA 依存のビルド可否。native Windows は難所なので WSL2 経路が現実的だが、WSL2 上で llive の他部分と繋がるかは未確認 |
| int8 カーネル sm_120 | どの実装(bitsandbytes / torch native / 自前)を使うか未決。fp16 ベースラインとの公平比較の作法も未設計 |
| MJX の hfield | 階段・不整地の接触が MJX で動くか未検証。記事の階段環境は MuJoCo native MJCF で、MJX は mesh 接地非対応・primitive 必須という制約がある |
| n≥20 の ground truth | 2ⁿ 頂点 × 次元の SVD バッチが 32GB VRAM に載るか未計算。載らなければ n=18 前後で打ち止め |

### 6-2. 本文書の検証を通していない候補(取りこぼしの可能性)

以下は survey 段階では挙がったが、今回の 29 候補リストに含まれず、敵対的検証も通していない。**次回の棚卸しで拾うこと**。

- **VLM: 漫画コマの人物同定・話者帰属ベンチ + manga 特化 encoder fine-tune** — 整備済 = `bazue_all` 206 コマの人間検証済み GT、Vision Encoder も来歴クリーン制約で選定済(**SigLIP2 = Apache が本命、CLIP は CC-BY-NC で商用不可**)。「manga 特化 encoder fine-tune が未存在 = SigLIP2/DINOv2 を Manga109+YManga で fine-tune すれば一次研究」。Part B P2 の VLM 項は「7B ローカル推論 + LoRA」までで、この具体が未記載。**優先度は高い可能性がある**。
- **VTLA(Vision-Tactile-Language-Action)の S1 / S2 / S3** — 2026-08-02 のユーザー宣言による本筋 pivot で、Part B(07-24)より新しいため丸ごと未載。S0 GATE は通過済(触覚 1.00 / proprio 0.44 / gain +0.56 / z=2.63, p<0.05 = TACTILE WINS)、**SmolVLA full FT は RTX5090 32GB で可能と一次検証済**。
- **freefloat z-cliff(off-plane 汎化)の単一 policy 集約** — per-fly-by CMA で **解の存在証明済**(in-plane 1.00 / z_low 1.00 / z_high 0.83)なのに単一 policy への集約が探索の壁で失敗 = **予算由来の見込みが高い**。ただし当該セッションは偽ログが多発しており「大 policy 検証は偽ログで未確定」と記録されている(**再確認が要る**)。
- **行動条件付き動画世界モデル(S3)の記憶長を自宅 32GB で実測** — memory 自身が「frontier 1 分 vs 自宅 数秒〜十数秒(**要検証**)」と書いた未測定項目。VRAM 律速なので 32GB が手元にある今はじめて測れる。
- **ossa(骨格 platform)S1.5 / S2 / S3** / **imgevolve の op 被覆拡大** — いずれも GPU 必然性が未実測。着手するなら「GPU が要るのか」をまず測ること。
- **llcraft(on-prem 生成メディア)** — 記事が「GPU 要件高」を理由に LOW と判定した派生案。32GB は Flux.1-schnell / Open-Sora クラスを回せるので「GPU が来て解禁された選択肢」ではあるが、実装ゼロ・FullSense 3 製品の優先度からは外れる。**着手可否はユーザー判断**。
- **llcore 2bit QAT の cap-gate 突破** — retention は RTN 22% → GPTQ 33% → 固定 scale QAT 82.9% → LSQ 84.0% と単調改善するが strict 97% cap-gate は全滅。「床を動かすのは手法でなく規模/学習予算/VQ codebook」を自前実測で確定(prior-art 一致 = 2bit 90%+ は 7B+ のみ)。★**パーク理由は計算量でなくユーザー方針**(「bit は下げない方針継続・VQ-2bit 不採用」)→ **計画に入れるなら方針の再確認が先**。

### 6-3. 見積りの不確かさ

- **規模(S/M/L)は実装工数と GPU 時間を分けていない**。特に G7 / G8 / G6 は「L のうち大半が RL スタック配線という実装工数」であり、GPU 時間は相対的に小さい可能性がある。
- **G19(安全ゲート税率)を L としたが、どこまでスケールを上げるかで工数が桁で変わる**。0.5M → 数千万 params なのか 1B なのかを決めていない。
- **記事の未消化点は「日本語オリジナル 25 本 + 2026-06-15 以降 30 本」から抽出**した。翻訳版(en/zh/ko)13 本・読む順ガイド 4 本・スタブ 2 本は本文重複として除外しており、**翻訳版固有の未解決事項が無いことは目視確認だが全文照合はしていない**。

---

## 付録: 参照した一次資料

- `C:/dev/projects/fullsense/docs/research/gpu_pc_arrival_workplan_2026-07-24.md`(Part A/B/C/D 全文 — 突合先)
- `C:/dev/projects/fullsense/docs/articles/drafts/QIITA_gpu_effect_rtx5090.md`(public_id `e6988b226d40a5916522`・公開済 — 71 倍の一次記録)
- `C:/dev/projects/llcore/out/nas_pareto_{v2long,v2needle,v2cross,v2distill,v2full,gpu_f32,1p5b}/nas_pareto.json`(verdict / needle / mixers の一次確認)
- `C:/dev/projects/llcore/research/verifier_cost_reduction/poc_scale_results.json`(n=8/12/16 の coverage と 510.2 秒)
- `C:/dev/projects/llcore/research/rllm_pivot/phase2_mamba_lyapunov{.py,_results.json}`(G21 実施済の証拠)
- `C:/dev/projects/llcore/src/llcore/runtime/distill.py`(joint 蒸留 未実装の一次証拠)
- `C:/dev/projects/llive/src/llive/llm/backend.py:571`(MambaBackend `NotImplementedError` の現存)
- `C:/dev/projects/llive/benchmark/low_spec.py`(xs/s/m/l/xl × 5 backend の progressive matrix)
- `C:/dev/projects/llive/docs/{genome_phenotype_gap_2026-07-28.md, fitness_llm_scoring_repair_2026-07-28.md, evolution_50gen_3seed_2026-07-29.md}`
- `C:/dev/projects/spikelab/src/spikelab/backend.py`(`use_backend()` の fail-safe 縮退)
- `C:/dev/projects/onocollo-complete/out/rl_footflat_long2.log`(FINAL = VERDICT_walks false / survive_s 3.77)
- `C:/dev/projects/onocollo-complete/docs/{MUSCLE_RL_RECIPE.md, hillco_body_language_requirements_2026_08_11.md}`
- `C:/dev/projects/onocollo-complete/scripts/evis_video/{recurrent_train,synergy_train,capture_point_train,posture_train,ppo_stand}.py` + `out/musculo/evis_balance/`
- memory: `project_gpu_pc_arrival_prep_2026_07_24` / `feedback_gpu_parallel_conditions_by_headroom` / `reference_evis_700muscle_xla_blocker_2026_08_08` / `project_hillco_locomujoco_robust_walk_2026_08_10` / `project_evis_eat_wsl_stereo_2026_08_03` / `project_lldarwin` / `project_llcore_gpu_3experiments_2026_06_06` / `project_onocollo_freefloat_2026_07_20` / `project_onocollo_rocket_eval_signal_null_2026_07_13` / `project_gaitlab_derivative_plan_2026_07_03`
- Qiita 公開記事(記事 ID は各項目の「由来記事」列に記載)
