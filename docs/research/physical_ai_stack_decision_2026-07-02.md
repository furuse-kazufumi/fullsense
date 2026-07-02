# フィジカル AI スタック意思決定メモ — 仮想空間で歩行ロボットを進化させる基盤選定

**著者**: 古瀬 和文（ぷるやん）／技術メモ
**日付**: 2026-07-02
**対象読者**: 自分（意思決定者・レビュアー）＋将来の自分
**目的**: 「仮想の物理空間で AI が複数の歩行ロボットを制御し、歩行アルゴリズムを進化的に最適化する」を実現する **シミュレータ／ROS／進化フレームワークの基盤選定**。導入前に最適解を調べて判断する（ROS/Gazebo 前提を疑ってよい、という自分の指示に対する回答）。
**規律**: honest disclosure（数値は出所明示・self-report と一次を区別・不確実は留保）。知識カットオフ 2026 初頭を超える点は各所で留保。5 次元（simulators / ros-role / evolution / cpu-gpu-transfer / legged-practical）の調査を統合。

---

## 1. TL;DR（結論＝推奨スタック）

- **今（GPU 到着前・WSL2 8スレ/~7GB）＝ 素の MuJoCo（C 実装, CPU）一択**。`pip install mujoco` で即動、接触忠実度・実機転移が最良。自作 **lldarwin（ε-lexicase + MAP-Elites/CVT）を pyribs 流の ask/tell QD ドライバとして直結**し、平面歩行器 or 四足（Go1 MJCF）で「進化で歩容が伸びる」ベースラインを **今の PC で完結**させる。（確信度: 高）
- **GPU 後（借り or 到着後）＝ MuJoCo Playground / MJX（JAX）を主軸**。同一 MuJoCo 物理を **CPU→GPU で連続運用**でき、`vmap` で集団評価が自然に並列化。lldarwin の設計資産（behavior descriptor・選択圧）は **QDax（JAX 版 MAP-Elites）へ移植**するか、ε-lexicase を上位のメタ選抜層に格上げして共存。（確信度: 高〜中）
- **ROS 2 は「進化ループの外」**。探索そのものには不要〜律速要因。**実機転移・複数機統合・可視化フェーズで Jazzy（LTS 2029）を後段に**。Gazebo は進化エンジンではなく「ROS 統合・最終検証の場」。（確信度: 高）
- **Isaac Lab は "頭打ちになってから"**。最大スループット・最多ロボット資産だが Omniverse/USD 学習コストと NVIDIA ロックイン、~10GB VRAM が対価。まず MJX、スケール律速で Isaac。（確信度: 高〜中）
- **キーメッセージ**: 「ROS を入れれば AI ロボット開発が近道」は **配線・標準化・実機ドライバの近道であって、歩行進化アルゴリズムの探索効率の近道ではない**。進化コア＝MuJoCo/MJX 直結、ROS＝成果を実機・複数機へ運ぶ層、という **役割分担**が最適解。

---

## 2. 目標と制約の再確認

**目標（将来像）**: 仮想の物理空間で AI がロボットを制御。複数の歩行ロボットを走らせ、歩行アルゴリズムを進化的に最適化する（＝「進化型 AI らしい姿」）。まずは環境構築から。

**きっかけと問い**: ものづくりワールド展のフィジカル AI ブース視察。世界モデルの重要性は感じるが、その前に **ROS を本格活用するのが AI 開発の近道**と判断した。ただし導入前に最適解を調べたい（＝ROS/Gazebo 前提を疑ってよい）。

**環境制約**:
- Windows 11 + WSL2（Ubuntu 24.04, 8 スレッド・RAM ~7GB 割当）+ Docker Desktop。
- **GPU 付き PC が到着予定**（時期未定）。GPU は「借りる」方針も併用（Kaggle/Colab/クラウド spot）。
- ~7GB RAM 制約 → **Isaac Sim（~10GB）は WSL2 では動作困難**、Genesis/Brax も GPU 前提で今は恩恵が出ない。この環境制約からも「GPU 前は MuJoCo 一択」が補強される。（確信度: 高）

**既存資産（活かしたい）**:
- 自作進化計算基盤 **lldarwin**（ε-lexicase 選択 + Quality-Diversity / MAP-Elites / CVT-MAP-Elites）。
- 進化型 AI framework **llive**、責任ゲート（**Approval Bus / HITL / fail-closed**）。
- → 進化側は自作資産を最大活用する方針。

**背景の追い風（設計上の帰結・確信度: 高）**: GPU バッチ型シム（MJX/Brax/Isaac）は「同一環境を数千並列で回す」設計で、これは **1 環境 = 1 個体**に写像すると進化計算と構造的に一致する。`vmap` で個体ごとに異なるポリシーパラメータを流し集団評価を一括ロールアウトできる。lldarwin の本質（多数の独立評価 + 行動記述子抽出）は GPU バッチ評価とそのまま噛み合う。**留意点**: QD の behavior descriptor を env ごとに取り出す配線は自前で書く必要がある（RL ライブラリは報酬前提のため）。

---

## 3. シミュレータ決定マトリクス

進化的最適化の判断軸は **「多数個体 × 多数ロールアウトのスループット」× 「接触忠実度／実機転移」× 「CPU→GPU 連続性」× 「自作資産との接続容易性」**。◎○△× は本目標（歩行 × 大規模並列進化）に対する適性。

| 軸 → / 候補 ↓ | 接触・歩行忠実度 | 並列 throughput | CPU で動く | ROS2 連携 | 成熟度 | 学習コスト | 本目標への総合 | 一言 |
|---|---|---|---|---|---|---|---|---|
| **MuJoCo (素/C, CPU)** | ◎ soft-contact 実機転移有利 | △ CPU 数K steps/s | ◎ pip 即動 | △ 要配線 | ◎ 事実上標準(DeepMind) | ○ | **◎ 今の本命** | GPU 前はこれ一択 |
| **MuJoCo Playground/MJX (JAX)** | ◎ 同上物理 | ◎ GPU 4096env 75K–950K steps/s | ○ 同一コード(遅いが動く) | △ 疎(直叩き) | ◎ | ○ 中庸 | **◎ GPU 後の本命** | CPU→GPU 連続・zero-shot 実績 |
| **Isaac Sim 5.0 + Isaac Lab 2.2** | ◎ PhysX, humanoid 群実績 | ◎ 4096env ≈150K steps/s(RTX4090) | × GPU 必須(~10GB) | ○ Isaac ROS でデプロイ側 | ○ 急拡大(NVIDIA) | × Omniverse/USD | **△→○ 大規模化時** | 最多ロボット資産・ロックイン対価 |
| **Genesis** | △ 要検証 | ？ 公称 43M FPS は疑義 | ○(CPU/GPU) | × 発展途上 | △ 話題先行 | ○ | △ 評価中でよい | 公称値は内訳を疑え |
| **Gazebo (Harmonic / Ionic / Jetty)** | △ ODE fork, 実時間寄り | × 並列非対応 | ◎ | ◎ **純正・最高** | ○ 定番 | ○ | △ 統合・検証専用 | 進化エンジンには非推奨 |
| **Newton (NVIDIA×DeepMind×Disney)** | ◎見込(MuJoCo-Warp) | ○ 70–100×(開発中) | △ GPU 志向 | △ 初期 | × 2025 発足・流動 | × 未成熟 | △ 動く標的・保留 | 将来の収束点、今は賭けない |
| **Brax** | △ 近似接触 | ◎ A100 humanoid ≈950K steps/s | × GPU/TPU 前提 | × | ○ | ○ | ○ MJX の下地 | 今は mujoco-mjx 依存に収斂 |
| **PyBullet** | △ | × CPU 数K | ◎ | △ | △ 保守モード | ◎ | △ MuJoCo の代替 | 無償化 MuJoCo があえて優先 |
| **Webots** | △ ODE fork | × 実時間寄り | ◎ | ○ webots_ros2 | △ Cyberbotics | ◎ | △ | 教育・統合向き |

**出典**: [MJX/Brax 論文 arXiv:2407.05148](https://arxiv.org/pdf/2407.05148)（humanoid A100 batch8192 ≈95万 steps/s、PPO 2億 steps を RTX4090 で約56分）/ [MuJoCo Playground GitHub](https://github.com/google-deepmind/mujoco_playground) ・ [技術レポート](https://playground.mujoco.org/assets/playground_technical_report.pdf)（quadruped/biped zero-shot sim-to-real）/ [Isaac Sim GitHub (Apache-2.0)](https://github.com/isaac-sim/IsaacSim) ・ [Isaac Lab 論文 arXiv:2511.04831](https://arxiv.org/html/2511.04831v1) / [MuJoCo vs Isaac 第三者比較 (2026)](https://www.roboticscenter.ai/rl-environments/mujoco-vs-isaac-sim)（Isaac 4096env≈15万 / MJX≈7.5万 steps/s、CPU 32コア 64env≈8K steps/s。**単一ブログ=確信度中**）/ [Genesis 批判的検証 (Stone Tao)](https://stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is)（低接触限定の数字、manipulation では ManiSkill より 3–10× 遅い）/ [Newton 発表 (NVIDIA)](https://developer.nvidia.com/blog/announcing-newton-an-open-source-physics-engine-for-robotics-simulation/) ・ [LF 寄贈](https://www.linuxfoundation.org/press/) / [Gazebo Ionic (Intrinsic)](https://www.intrinsic.ai/blog/posts/advancing-real-world-robotics-through-simulation-with-gazebo-ionic) ・ [Gazebo Classic EOL](https://www.therobotreport.com/gazebo-classic-robotics-simulator-reaches-end-of-life/)。

**honest な数値注記（確信度: 中）**: throughput は **機種・ロボット・定義がバラバラで直接比較不可**（A100 と RTX4090、steps/s と env-steps/s と FPS が混在。多くがベンダ self-report のピーク値）。上表は **桁感の目安**として扱い、最終判断は自分の GPU PC で歩行タスクを実測してからが honest。WSL2 8スレでは CPU MuJoCo は 8K×(8/32)≒**2K steps/s オーダー**が現実線（フェルミ、確信度: 中）。

---

## 4. ROS 2 の位置づけ（どのフェーズで何に使うか／使わない判断も明記）

**結論**: 目標を 2 フェーズに割ると答えが明快。**探索ループ（進化そのもの）には ROS 2 は不要〜有害寄り。真価は実機転移・統合・標準化フェーズ**。「ROS が近道」は本目標に限れば **半分正しく半分ミスリード**。（確信度: 高）

| フェーズ | ROS 2 の要否 | 理由 | 確信度 |
|---|---|---|---|
| **歩行進化の探索ループ**（数千〜数百万 rollout、lldarwin の MAP-Elites/ε-lexicase 評価） | **不要〜有害寄り** | GPU 並列シム(MJX/Isaac)は Python/tensor API で直結。ROS の pub/sub・DDS・プロセス分離は per-step overhead でスループット律速。legged_gym / Isaac Lab / MuJoCo Playground は **いずれも学習ループに ROS を挟まない** | 高 |
| **可視化・単体プロトタイプ** | あると便利 | RViz / rosbag / URDF 資産の再利用 | 中 |
| **実機転移・統合**（Nav2 / MoveIt / ros2_control、複数機協調、センサ配線） | **必須級** | 標準メッセージ・HW 抽象・既製ドライバ。ここで初めて「配線の標準化」の価値 | 高 |

**一次的裏付け**: NVIDIA/Isaac Lab の公式ワークフローは「Isaac Lab で **学習（ROS なし）→ Isaac ROS で実機デプロイ（ROS 2）**」と明記（[NVIDIA Spot sim-to-real](https://developer.nvidia.com/blog/closing-the-sim-to-real-gap-training-spot-quadruped-locomotion-with-nvidia-isaac-lab/) / [Isaac Lab policy deployment docs](https://isaac-sim.github.io/IsaacLab/main/source/policy_deployment/index.html)）。MAP-Elites は「並列実装が容易で PPO と競合的、ただし ~1 兆フレーム級」を要する（[arXiv:2009.08438](https://arxiv.org/pdf/2009.08438)）—**この規模を ROS 経由で回すのは非現実的**で、lldarwin も評価関数＝シミュレータを直叩きする形が自然。

**ros2_control で脚歩行を回せるか**: できる。ただし Gazebo は CPU バウンドで大規模並列に不向き（複数機を「見せる/検証する」用途）。`gz_ros2_control` は Jazzy 標準の Gazebo **Harmonic** に対し effort/velocity/position の command interface で controller manager を注入（[control.ros.org/jazzy](https://control.ros.org/jazzy/doc/gz_ros2_control/doc/index.html)）。脚歩行の実戦事例は [`legubiao/quadruped_ros2_control`](https://github.com/legubiao/quadruped_ros2_control) が最充実（OCS2-MPC / RL / Unitree Guide の 3 コントローラを ros2_control 上で、Gazebo/MuJoCo 両対応、sim2real まで）。→ **進化は自作、コントローラ枠だけ ros2_control** という分業が可能。（確信度: 高）

**実機の ROS 2 対応**: **Unitree Go2/B2/G1/H1** は公式 [`unitree_ros2`](https://github.com/unitreerobotics/unitree_ros2)（CycloneDDS ベース）+ コミュニティ SDK 多数で **入門実機として最も厚い**。G1（二足）は [`g1pilot`](https://github.com/hucebot/g1pilot) 等。ANYmal は研究界の標準脚ロボだが ROS 2 一次情報が薄く商用寄り（**留保・確信度: 中**）。

**distro 選択 = Jazzy Jalisco（LTS, EOL 2029-05）が本命**。WSL2 Ubuntu 24.04 にそのまま乗り、`gz_ros2_control`・Nav2・Unitree パッケージ・チュートリアルが最も揃う（[endoflife.date/ros-2](https://endoflife.date/ros-2) / [control.ros.org/jazzy](https://control.ros.org/jazzy/)、確信度: 高）。Kilted Kaiju は非LTS で 2026-12 EOL のため回避。Lyrical Luth（2026-05 新 LTS, EOL 2031、Ubuntu 版は 26.04 と推定）は長寿命が魅力だが今始めるなら成熟度で Jazzy（**Ubuntu 版は secondary source 間で 24.04/26.04 の食い違い、採用前に docs.ros.org で一次確認・確信度: 低**）。

**使わない判断（明記）**: **Gazebo を進化のロールアウト基盤にはしない**。実時間寄り・1 体志向で数千ロールアウトに向かないため。進化は MuJoCo/MJX 直叩き、Gazebo は上位個体の検証・可視化に限定する。

---

## 5. 進化／QD の配線（lldarwin をどう活かすか、既存 QDax 等との損得）

**歩行進化の教科書的正解は MAP-Elites 系**。起点は Cully et al. 2015 (Nature) の六脚ロボット damage-recovery で、これが QD をロボティクスの主流に押し上げた（[nature14422](https://www.nature.com/articles/nature14422)、コード [resibots/map_elites_hexapod](https://github.com/resibots/map_elites_hexapod)）。**本人のビジョン「壊れても歩ける多様な repertoire を進化的に敷き詰める」は QD/MAP-Elites の本丸**であり、lldarwin がそのまま最先端系譜に乗る。（確信度: 高）

**behavior descriptor（BD）の定番（確信度: 高〜中）**:

| descriptor | 中身 | 使われ方 |
|---|---|---|
| **接地デューティ比（feet contact time）** | 各脚の接地時間割合。QDax locomotion 標準 measure＝「脚の地面接触回数 ÷ 軌道長」 | Cully 2015 / QDax 標準（第一選択） |
| **最終 (x,y) 到達位置** | omnidirectional 歩行の到達点を 2D descriptor に | MAP-Elites omni-directional 系 |
| 体幹の平均高さ・姿勢 | 低姿勢/直立でスタイル分離 | soft/legged QD |
| 歩幅・周期・エネルギー(CoT) | 効率/歩容タイプの分離 | 各種 gait QD |

出典: [Nature 2015](https://www.nature.com/articles/nature14422) / [PPGA arXiv:2305.13795](https://arxiv.org/pdf/2305.13795)（QDax measure = leg-contact/trajectory-length）。

**framework × simulator 相性（確信度: 高）**:

| framework | 言語/実行 | 相性の良い sim | 得意 | 状態 |
|---|---|---|---|---|
| **QDax** | JAX / GPU・TPU | Brax, MJX | 大規模 NN 制御器の QD を GPU 並列で分単位 | v0.5.0(2025-05)、PGA-ME/CMA-ME/DCRL-ME/AURORA 実装 |
| **pyribs** | Python/numpy(CPU) | **任意**(Gym/MuJoCo/PyBullet/Isaac をユーザ eval で) | simulator 非依存・ask/tell 明快、CMA-ME/CMA-MAE 本家 | v0.7 系、ICAROS 維持 |
| **evosax** | JAX / GPU | Brax | 純 ES(CMA-ES/OpenAI-ES/PGPE/SNES 30+)を GPU で | 活発 |
| **Isaac Lab / MJX Playground** | PyTorch or JAX / GPU | Isaac Sim, MJX | **RL(PPO)** で locomotion、sim-to-real 実績(Anymal/Spot/Go1 等) | 2024-25 主流 |

現在の王道は **「JAX 系 QD/ES ↔ Brax/MJX の GPU 並列」**。Brax は今や mujoco-mjx 依存（実質 MJX が physics バックエンド）で、QDax/evosax/Playground は MJX 系で束ねられつつある。出典: [QDax GitHub](https://github.com/adaptive-intelligent-robotics/QDax) / [pyribs.org](https://pyribs.org/) / [evosax](https://github.com/RobertTLange/evosax) / [MuJoCo Playground arXiv:2502.08844](https://arxiv.org/html/2502.08844v1)。

**lldarwin を活かす 3 択（損得）— これが配線の核心**:

**前提の honest な注意**: QDax の速さは **「評価ループ丸ごと JAX で jit/vmap」** から来る。numpy の lldarwin をそのまま QDax に「繋ぐ」ことはできず、恩恵を得るには **JAX 移植**が必要。一方 lldarwin の QD（MAP-Elites/CVT）は構造上 **pyribs と同型の ask/tell**。

| 選択肢 | 得 | 損 | 向く局面 | 確信度 |
|---|---|---|---|---|
| **A. lldarwin を CPU QD ドライバとして sim に直結**（MuJoCo-CPU/PyBullet、pyribs 流 ask/tell） | 自作資産(ε-lexicase・CVT-MAP-Elites・Approval Bus)を丸ごと活用／simulator 非依存／GPU 不要=今の WSL2 で即着手 | CPU 律速で個体数・世代数が限られる(8スレ/7GB では小規模) | **GPU 前の第一歩**、責任ゲート統合の PoC | 中〜高 |
| **B. QDax に寄せる**（lldarwin 一部を JAX 移植 or 捨てて PGA-ME 採用） | GPU で 100–1000×、深い NN 制御器、PGA-ME で RL 勾配併用 | ε-lexicase/独自選択圧は **そのまま乗らない**(要再実装)／JAX 学習コスト／自作資産の一部を失う | GPU 到着後の **本番スケール** | 中 |
| **C. ハイブリッド**: QDax/Brax で歩容 archive を高速生成 → lldarwin(ε-lexicase・QD 指標・HITL)を **上位のメタ選択/評価層**に | 速度と自作思想を両取り／lldarwin を「価値判断・多目的ロバスト化」層に格上げ | 2 層の I/F 設計が要る | 中長期の本命構成 | 中 |

**ε-lexicase と MAP-Elites の関係（重要 honest）**: 両者は **役割が半分重なる**。MAP-Elites は archive の niche 競争で多様性を担保するので、その中に ε-lexicase をそのまま入れる例は稀。**ε-lexicase の真価は「多数のテストケース/多地形・多目的でケース毎に勝ち抜く親選択」**。自然な配線は **「MAP-Elites = 歩容空間の illumination 軸」「ε-lexicase = 多地形ロバスト性の親選択 or 上位選抜」と軸を分担**させること（cf. "Blending notions of diversity for MAP-Elites", GECCO 2019）。（確信度: 中）
出典: [pyribs paper arXiv:2303.00191](https://arxiv.org/pdf/2303.00191) / [PGA-MAP-Elites (GECCO2021)](https://dl.acm.org/doi/10.1145/3449639.3459304) / [Blending diversity (GECCO2019)](https://dl.acm.org/doi/10.1145/3319619.3321987)。

**進化(QD/ES) vs 勾配(RL) — 公平な整理**: 「1 個の最強歩行」なら **RL(PPO on Isaac/MJX)が今の実務標準**（Anymal/Spot/Go1 zero-shot 実績豊富）。「多様解の archive を敷き詰める」本人ビジョンは **QD/MAP-Elites の本丸**。両者は排他でなく、**PGA-ME / DCRL-ME が RL 勾配を QD に取り込む橋**として最有力。RL は別トラックで併走させ、QD archive と比較・蒸留すると良い。（確信度: 高）
出典: [OpenAI ES](https://openai.com/index/evolution-strategies/) / [ES vs RL 定性差 arXiv:2205.07592](https://arxiv.org/pdf/2205.07592) / [DCG-MAP-Elites arXiv:2303.03832](https://arxiv.org/abs/2303.03832)。

---

## 6. 推奨スタック（本命 1 つ ＋ 橋渡し／代替）

### 本命（進化コア）: MuJoCo → MJX/Playground の連続ライン ＋ lldarwin QD ドライバ

- **物理**: 今 = 素の MuJoCo（C, CPU）／GPU 後 = MuJoCo Playground（MJX/JAX）。**同一 MuJoCo 物理・同一 MJCF を CPU→GPU で連続運用**できるのが最大の利点。書き直し最小・接触忠実度最良・quadruped/biped の zero-shot sim-to-real 実績あり。
- **進化**: lldarwin を QD ドライバとして直結（今）→ QDax へ移植 or 上位メタ層へ格上げ（GPU 後）。
- **理由**: (1) 「CPU↔GPU 同一コード」を最も素直に満たすのは JAX 系。(2) lldarwin の設計資産（BD・ε-lexicase・CVT）が pyribs/QDax と概念一致で活きる。(3) ~7GB RAM の WSL2 で今すぐ着手でき、GPU 期に投資が 100% 生きる。

### 橋渡し（実機・統合・複数機）: ROS 2 Jazzy ＋ Gazebo Harmonic ＋ ros2_control

- 進化ループの **外側**。良個体を `quadruped_ros2_control` のコントローラ枠に載せ、Unitree Go2 等で実機転移。複数機の協調・センサ配線・可視化はここで標準化。

### 代替／スケール時: Isaac Lab 2.2（GPU 到着後・MJX が頭打ちになってから）

- 最大スループット・最多ロボット資産（Spot/ANYmal/Unitree G1・H1 等 11 形態）。Apache-2.0 で OSS 化済（[NVIDIA GA blog](https://developer.nvidia.com/blog/isaac-sim-and-isaac-lab-are-now-available-for-early-developer-preview/)）。対価は Omniverse/USD 学習コストと NVIDIA ロックイン、~10GB VRAM。**まず MJX、頭打ちで Isaac** が費用対効果的。

### モデル正本化（全フェーズの橋）: URDF ＋ MJCF を正本として同期

- **URDF** = ROS/Gazebo/実機の lingua franca（物理表現は貧弱）。**MJCF** = MuJoCo/MJX ネイティブ（接触・アクチュエータ表現が最豊富、locomotion 研究の主流）。**MuJoCo は URDF を直接読まない**ので URDF→MJCF は手当てが必要（ROS2 側 `make_mjcf_from_robot_description`、複雑モデルは手調整前提）。2025 に DeepMind が **mujoco-usd-converter**（MJCF↔USD）を公開し、将来の USD（Isaac/Newton）へも橋渡し可能。
出典: [control.ros.org tools](https://control.ros.org/rolling/doc/mujoco_ros2_control/mujoco_ros2_control/docs/tools.html) / [mujoco discussion #3176](https://github.com/google-deepmind/mujoco/discussions/3176) / [NVIDIA Omniverse libraries blog](https://developer.nvidia.com/blog/developers-build-fast-and-reliable-robot-simulations-with-nvidia-omniverse-libraries/)。

---

## 7. 段階ロードマップ

### Phase 0 — 今すぐ（CPU / WSL2 8スレ・~7GB）: 環境構築とパイプライン検証

- **入れるもの**: `pip install mujoco`（素の MuJoCo, C 実装）。DM Control の planar walker（walker2d）か Unitree Go1 の MJCF。（任意で ROS 2 **Jazzy** + Gazebo Harmonic を別トラックで入れ、URDF/RViz/`gz_ros2_control` に慣れる。）
- **作るもの**:
  1. Go1 MJCF を読み込み **PD 制御で 1 体を立たせる**（接触・アクチュエータの手触りを掴む）。
  2. **lldarwin の MAP-Elites を planar walker/低次元パラメトリック歩容に接続**（pyribs 流 ask/tell ドライバとして）。descriptor = 接地デューティ比 ×（歩行速度／COM 高さ）、fitness = 前進距離 − エネルギー − 非現実ペナルティ。
  3. 「複数体を走らせる」= 集団の各個体を **CPU multiprocessing で独立環境並列評価**（数十〜百個体）。
  4. **報酬ハック対策の型を先に作る**: state 依存トルク上限、action rate/energy ペナルティ、BD に「接地時間・COM 高さ」を入れて非現実解を淘汰。
- **到達点**: 「進化で歩容が伸びる」ベースラインを 1 本取る。**URDF/MJCF を正本化**し同期の仕組みを作る。lldarwin の BD・選択圧・Approval Bus/HITL 統合の PoC。**ここまで今の PC で完結**。
- **確信度**: 高（環境制約・一次情報で裏取り済）。

### Phase 1 — 借り GPU で先取り（GPU PC 到着前でも可）

- **入れるもの**: Kaggle 無料 T4（30h/週）or Colab or spot A100/4090。QDax + Brax/MJX の MAP-Elites × walker サンプル。
- **作るもの**:
  1. QDax の MAP-Elites×Brax walker サンプルを Kaggle 無料 T4 で **1 ラン回す**。
  2. lldarwin の BD/選択圧を QDax へ **移植（選択肢 B の一部）**、または ε-lexicase を上位メタ層に据える（選択肢 C）。
  3. spot A100 で **1e6 評価ランの wall-clock を実測**してベースライン化（推定 0.5〜5h を検証、§8）。
- **到達点**: 「今すぐ大規模並列歩行進化」を現金ゼロ〜数ドルで回せることを実証。GPU 期のスループット基準値を得る。
- **確信度**: 中〜高（無料枠可用性・CU レートは 2026 変動、要都度確認）。

### Phase 2 — GPU PC 到着後: 本番スケール

- **入れるもの**: MuJoCo Playground（MJX）を主軸。頭打ちで Isaac Lab 2.2 を追加。実機トラックに Unitree Go2 等 + `unitree_ros2`。
- **作るもの**:
  1. 同じ MJCF を **Playground(MJX)** へ。Go1 joystick を PPO で数分学習（reality gap 対策 = **actuator net** + domain randomization）。
  2. **QDax + Brax/MJX で PGA-ME を本番スケール**。MAP-Elites = 歩容 illumination、ε-lexicase = 多地形ロバスト選抜、で軸分担共存。
  3. 上位個体を ros2_control コントローラ枠（`quadruped_ros2_control` 参照）に載せ、**Gazebo → 実機（Unitree）へ sim-to-real**。複数機協調を ROS 2 で統合。
  4. 二足/humanoid（G1 等）は四足の知見が固まってから。
- **到達点**: 「複数歩行ロボット × 進化最適化」の将来像を、進化コア（MJX+QDax）と実機/統合層（ROS 2）の役割分担アーキで実現。Newton の成熟を見つつ移行を判断。
- **確信度**: 中（Newton 成熟度・バージョンは 2026 要再確認）。

**reality gap の分水嶺（Phase 2 の勘所・確信度: 高）**: アクチュエータが reality gap の主因。Hwangbo et al.(ANYmal, Science Robotics 2019) の **actuator net**（位置/速度誤差履歴→実トルクを予測する NN をシムに挿入）が四足 RL の分水嶺。理想トルク源のまま学習した歩容は実機で崩れる。**制御25年の勘所どおりモータ/減速機/帯域のモデル化が命**。出典: [survey arXiv:2406.01152](https://arxiv.org/pdf/2406.01152) / [RAI Institute Spot arXiv:2511.04831](https://arxiv.org/pdf/2511.04831)（5.2 m/s zero-shot、**self-report 含む**）。

---

## 8. コスト／throughput のフェルミ推定

### 目的
「借りる GPU で 1 回の実用的な QD 歩行進化ラン」の wall-clock とコストの桁を見積もる。

### 分解式
```
総時間 T = (個体評価数 E × 1エピソード sim ステップ L) / 集約スループット S
総コスト = T × spot 時間単価
```

### 係数の出所と幅
- **E（総評価数）**: MAP-Elites で 1024 個体/世代 × 1000 世代 = **≈1e6 評価**（仮置き）。
- **L（1 エピソード steps）**: **1000 steps/episode**（公式ベンチ相当の仮置き）。
- → 総 sim ステップ ≈ **1e9**。
- **S（集約スループット, A100/4090, バッチ MJX/Brax, 脚ロボット・接触あり）**: **1e5〜5e5 steps/s** と保守的に置く。根拠幅:
  - 30-DoF humanoid, RTX4090・8192 並列 = **≈6万 steps/s（学習込み実測, [arXiv:2407.05148](https://arxiv.org/pdf/2407.05148)）**。
  - A100 単体 humanoid **sim-only ≈95万 steps/s**（同系、self-report ピーク）。
  - QDax は A100 で **≈3万 evaluations/s**（[QDax massive parallelization](https://spiral.imperial.ac.uk/server/api/core/bitstreams/6948508a-91c9-4974-b767-43b7c22a3360/content)）。
  - → いずれも **self-report ピーク含む**ので実効は下振れとして幅で扱う。

### 計算
- T = 1e9 / S → **S=1e5 で ≈2.8 時間 / S=5e5 で ≈34 分**。
- **結論**: 1 回の実用的 QD ランは **単一 A100/4090 で約 0.5〜5 時間**。

### コスト相場（確信度: 中〜高、市況変動あり）
| 手段 | GPU | 実効コスト | 制約 |
|---|---|---|---|
| Kaggle 無料 | T4×2 / P100 16GB | **無料 30h/週** | 9h/セッション、16GB VRAM |
| Colab | 無料T4〜Pro/Pro+ | Pro $9.99、$9.99/100CU(T4≈57h, A100≈7h) | プリエンプト・可用性変動 |
| Spot | A100 80GB | **≈$0.6–0.7/h**（Vast/Spheron） | 中断あり |
| Spot | RTX4090 / L4 | **≈$0.34–2.5/h**（RunPod community 等） | 同上 |

→ **1 ラン ≈ $0.3〜$5**。Kaggle 無料 30h/週なら **現金ゼロで週に数ラン**。「今すぐ大規模並列歩行進化を回す」は十分現実的。**ボトルネックは金でなく T4/16GB VRAM とセッション 9h・プリエンプト**（ロボット複雑度とバッチサイズを絞れば回避可）。
出典: [Kaggle GPU docs](https://www.kaggle.com/docs/efficient-gpu-usage) / [Colab 料金](https://colab.research.google.com/signup) / [RunPod pricing](https://www.runpod.io/pricing) / [QDax (JMLR)](https://www.jmlr.org/papers/volume25/23-1027/23-1027.pdf)。

### CPU 現況の桁（今の WSL2, 参考）
CPU MuJoCo 32コア 64env ≈8K steps/s（第三者ブログ）→ WSL2 8スレでは **≈2K steps/s オーダー**（フェルミ: 8K×8/32）。上記 1e9 ステップを CPU 単独で回すと **≈140 時間** となり、Phase 0 は **評価数を 1e6→数千に絞った小規模 PoC** に留めるのが現実的（確信度: 中）。

---

## 9. honest な留保・リスク・未確認事項（知識カットオフ由来の要再確認点）

1. **throughput 数値は測定条件が非統一・self-report ピーク多数**。Isaac/MJX/Genesis/Brax の倍率をそのまま比較しない。**最終判断は自分の GPU PC で歩行タスクを実測**してから。（確信度: 高）
2. **Genesis の「43M FPS / 430,000×実時間 / 四足 26 秒学習」は公称値で異論あり**。低接触シーン限定で、接触が増える現実タスクでは既存 GPU シムより 3–10× 遅い場合があると第三者検証（[Stone Tao](https://stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is)、[issue #181](https://github.com/Genesis-Embodied-AI/Genesis/issues/181)）。**上限値として扱う**。honest disclosure の典型例。
3. **Newton（NVIDIA×DeepMind×Disney）は 2025-09 に Linux Foundation 寄贈された早期・移動標的**。「1.0 / GTC 2026 リリース」との一部記述は **一次確認できず（確信度: 低）**、公式は 2025 時点で beta/alpha。アーキ選定を賭ける前に現行版を要一次確認。MuJoCo-Warp が Newton/Playground 双方の共通コアに向かう点だけ確度が高い。
4. **ROS 2 distro**: Lyrical Luth（2026-05 新 LTS, EOL 2031）の **Ubuntu 版が 24.04/26.04 で secondary source 間に食い違い**。採用前に [docs.ros.org](https://docs.ros.org) で一次確認。当面は Jazzy（LTS 2029）で確定。
5. **各 framework の 2026 年中頃の正確なバージョン番号**（QDax v0.5.0 以降、pyribs、MuJoCo Playground 等）は 2025 一次情報までしか確認できず **留保**。素の MuJoCo で始めれば陳腐化リスク最小。
6. **lldarwin の実装言語**（numpy 想定は本人記述からの推定）。**JAX 実装なら選択肢 B の移植コストが大幅減**し推奨が変わる。実装言語を要確認。
7. **ANYmal の ROS 2 対応は一次情報が薄く留保**。実機入口は Unitree 系が現実的。
8. **無料枠の可用性・CU 消費レートは 2026 に変動**（Colab の CU/h は公式で都度確認）。§8 の相場は 2025〜2026 初頭の実測レンジ。
9. **sim-to-real の数値（5.2 m/s、26 秒学習、70–100× 等）は開発元 self-report を含む**。採用判断は自前ベンチで。
10. **「四足 < 二足（四足が楽）」は統計的傾向**で、パルクール等タスク次第で逆転しうる。

---

## 10. 次の一手（GO を出したら最初に動かすもの）

**題材**: Phase 0 の最小 PoC = 「MuJoCo で 1 体を立たせ、lldarwin の MAP-Elites で planar walker の歩容を進化させ、進化で伸びるベースラインを 1 本取る」。すべて今の WSL2（CPU）で完結。

**最初のコマンド（WSL2 Ubuntu 24.04 内）**:
```bash
# 1. MuJoCo + DM Control を入れる（GPU 不要）
python3 -m pip install --upgrade pip
python3 -m pip install mujoco dm_control numpy

# 2. 動作確認: MuJoCo の walker2d が読めるか
python3 -c "import mujoco, dm_control; from dm_control import suite; \
env = suite.load('walker','walk'); print('OK', env.action_spec())"

# 3. lldarwin を QD ドライバとして使うための下地確認（自作資産のパスに合わせて）
#    - ask/tell I/F があるか、descriptor 抽出フックを差せるか
#    - なければ pyribs を参考実装として入れて型合わせ
python3 -m pip install ribs  # 参考: pyribs（ask/tell の型見本）
```

**その直後の作業順**:
1. Go1 MJCF（または planar walker）で PD 制御 1 体の立位を確認。
2. lldarwin の MAP-Elites に **descriptor = 接地デューティ比 ×（速度 or COM 高さ）**、**fitness = 前進距離 − エネルギー − 非現実ペナルティ** を配線。
3. CPU multiprocessing で数十個体を独立並列評価 → archive が埋まり fitness が世代で伸びることを確認。
4. 並行して（任意）ROS 2 **Jazzy** + Gazebo Harmonic を別トラックで入れ、URDF↔MJCF 正本同期の仕組みを作る。

**GO 判断のポイント**: この Phase 0 は現金ゼロ・GPU 不要・陳腐化リスク最小。ここで「進化で歩容が伸びる」体験とパイプライン（BD 設計・報酬ハック対策・責任ゲート統合）を先に固めれば、GPU 到着後は物理を MJX に差し替えるだけでスケールできる。**まず動かして、数値は自前ベンチで確かめる**（feedback_benchmark_honest_disclosure に従い、借り GPU の実測で §8 のフェルミを検証）。

---

### 主要出典一覧（再掲・一次優先）
- MJX/Brax 論文: [arXiv:2407.05148](https://arxiv.org/pdf/2407.05148)
- MuJoCo Playground: [GitHub](https://github.com/google-deepmind/mujoco_playground) / [論文 arXiv:2502.08844](https://arxiv.org/html/2502.08844v1) / [技術レポート](https://playground.mujoco.org/assets/playground_technical_report.pdf)
- Isaac Sim: [GitHub(Apache-2.0)](https://github.com/isaac-sim/IsaacSim) / Isaac Lab: [論文 arXiv:2511.04831](https://arxiv.org/html/2511.04831v1) / [Spot sim-to-real](https://developer.nvidia.com/blog/closing-the-sim-to-real-gap-training-spot-quadruped-locomotion-with-nvidia-isaac-lab/) / [policy deployment docs](https://isaac-sim.github.io/IsaacLab/main/source/policy_deployment/index.html)
- QD: [Cully 2015 Nature](https://www.nature.com/articles/nature14422) / [QDax GitHub](https://github.com/adaptive-intelligent-robotics/QDax) / [QDax JMLR](https://www.jmlr.org/papers/volume25/23-1027/23-1027.pdf) / [pyribs](https://pyribs.org/) / [MAP-Elites vs PPO arXiv:2009.08438](https://arxiv.org/pdf/2009.08438)
- ROS: [endoflife.date/ros-2](https://endoflife.date/ros-2) / [gz_ros2_control (Jazzy)](https://control.ros.org/jazzy/doc/gz_ros2_control/doc/index.html) / [quadruped_ros2_control](https://github.com/legubiao/quadruped_ros2_control) / [unitree_ros2](https://github.com/unitreerobotics/unitree_ros2)
- 検証・留保: [Genesis 批判 (Stone Tao)](https://stoneztao.substack.com/p/the-new-hyped-genesis-simulator-is) / [Newton (NVIDIA)](https://developer.nvidia.com/blog/announcing-newton-an-open-source-physics-engine-for-robotics-simulation/) / [sim-to-real survey arXiv:2406.01152](https://arxiv.org/pdf/2406.01152)
- コスト: [Kaggle GPU](https://www.kaggle.com/docs/efficient-gpu-usage) / [Colab 料金](https://colab.research.google.com/signup) / [RunPod pricing](https://www.runpod.io/pricing)
