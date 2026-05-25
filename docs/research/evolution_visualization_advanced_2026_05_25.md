# 進化可視化の高度化 — 3DGS 時系列 + 魅せ方史（2026-05-25）

> **動機（ユーザー 2026-05-25）**: 「**単なるグラフ表示はダメ**。3D Gaussian Splatting を
> 時系列で変化させるくらいの魅せ方が欲しい。進化ゲームの**見せ方・魅せ方の進化を昔から段階的に**
> 調べた方が良い」。現状の `evolution.svg`（適応度/多様性の時系列線）・`persona_dominance.svg`
> （系統 stacked-area）は集団統計どまりで、個体・交配・ペルソナという進化の実体を魅せられない。
> 本書は調査（codex 段階調査 + WebSearch + rad-research）を統合し、段階的実装方針を定める。
> FullSense デモ哲学（動きで魅せる, [[project_f25_demo_polish]]）の進化可視化版。

## 1. 進化 / 人工生命 可視化史（段階表）

| 年代 | システム | 見せ方（魅せ方） | 技術要素 |
|---|---|---|---|
| 1970 | Conway's Game of Life | 2D セルの自己組織化を「動き」で見せる観察型 | 離散 CA、単純ルール反復、パターン図鑑 |
| 1991–94 | Tierra (Tom Ray) | デジタル生態系を**ログと系統的振る舞い**（寄生/共生）で。見た目より進化ダイナミクス | 自己複製コード、CPU/メモリ競合、突然変異注入 |
| 1990s–2004 | Avida | 集団・ゲノム・適応の**計測を可視化**。教育版 Avida-ED は GUI 観察 | デジタル生物、実験プロトコル、計測後処理 |
| 1994 | Karl Sims (Evolved Virtual Creatures / Galápagos) | 3D 形態+運動を進化 + **観客選択を進化圧にする参加型演出** | 物理シミュレーション、形態+神経制御、対話選択、展示 |
| 1996〜 | Framsticks | 3D 仮想生物の体・脳・環境を同時提示、GUI 観察 | 3D 身体シミュレーション、複数 genotype encoding |
| 1996–2008 | Creatures / Spore | 進化を**研究画面から体験 UI へ**（育成・創作・共有） | 遺伝/学習 AI、プレイヤー生成形態への手続きアニメ |
| 2018〜 | Lenia (Chan) | 連続系セル生命の**有機的運動を高密度に**。種/科の分類で自然史的に | 連続空間時間 CA、インタラクティブ進化探索、生命カタログ |
| 2015〜 | open-ended evolution 可視化 | 「最適解1個」から「**多様なエリート地図 + 問題生成**」へ。系統樹・生態地図・多様性面 | MAP-Elites, POET, objective-less, 多様性アーカイブ可視化 |

**読み取り**: 魅せ方は「観察 → 計測 → 参加（観客選択）→ 体験 UI → 多様性の地図化」と進化。
FullSense は現在「計測（グラフ）」段階。目標は「**多様性の地図化 + 体験**」（系統・個体・3DGS）。

## 2. 魅せ方カタログ（動きで魅せる具体手法）

- **系統樹アニメ**: 世代ごとの枝伸長、絶滅枝フェード、現存系統ハイライト。
- **phenotype 可視化**: 形態サムネイルのモーフィング、骨格/関節ヒートマップ、行動ベクトル重畳。
- **集団の空間/ニッチ配置**: MAP-Elites の 2D グリッド地形化、密度等高線、ニッチ占有率アニメ。
- **リアルタイム進化演出**: 「選択→交叉→突然変異→誕生」を 1 サイクル演出として可視化。
- **個体間相互作用**: 捕食・協調・競合をエッジ（色/太さ/寿命）で時間表示。
- **タイムラプス**（100世代圧縮）と等速再生の切替、**世代スライダ + 祖先へ巻き戻し**。
- **チャンピオン血統の一人称追跡カメラ**、**失敗突然変異のゴースト再生**（探索の豊かさを見せる）。

→ 現 `persona_dominance.svg`（系統 stacked-area）は「系統樹アニメ」の入口。次は phenotype + 相互作用 + 一人称追跡。

## 3. 3D Gaussian Splatting 時系列表示

**SOTA（実現済の下地）**:
- [4D Gaussian Splatting (CVPR 2024)](https://guanjunwu.github.io/4dgs/) — deformation field で canonical 3DGS を各時刻に変形。
- [4D-Rotor GS (SIGGRAPH 2024)](https://weify627.github.io/4drotorgs/) — XYZT 異方性 4D ガウシアン。
- [1000+ FPS 4DGS (NeurIPS 2025)](https://openreview.net/forum?id=YbKdduMtyN) — 短命/不活性ガウシアン削減。
- Deformable 3D Gaussians — 変形場学習で単眼動的再構成。

**進化個体への適用（設計推論, codex）**:
- `genome → phenotype` で得た形態/行動状態を、各世代で**ガウシアン集合**として保存。
- 時間軸 `t = 世代` で属性（位置・共分散・色・不透明度・SH 係数）を補間。
- **1 個体内時系列**（歩行など）と**世代時系列**（進化）を 2 軸で再生可能に。
- Web 表示は `GaussianSplats3D` / `antimatter15/splat` で現実的。MVP は「世代ごと静的 3DGS + 補間」。

**SH 係数の縁**: [[project_precision_metrology_llm]]（3DGS の SH 係数）と接続 — 既に FullSense ビジョンに 3DGS-SH の素地あり（[[project_hyperdimensional_thinking_seed]]）。

## 4. FullSense / llove 段階実装（codex 案）

**既存資産（llive 側）**: `docs/llove_jsonl_v1.md`（JSONL 連携仕様）/ `scripts/evolution_dashboard.py` / `scripts/evolution_lineage_viz.py`（系統 SVG・血統, 本セッションで活用）/ `src/llive/observability/llove_bridge.py` / `docs/family_integration.md`。

| Phase | 内容 | リスク |
|---|---|---|
| **1 (TUI 強化)** | 既存 JSONL に「系統シェア / ニッチ占有 / 相互作用イベント」を追記。llove はポーリングで時系列アニメを ASCII/SVG 強化。`evolution_to_llove.py`（本セッション作成）の拡張。 | 低 |
| **2 (Qt 2.5D)** | TUI 横に Qt で 2.5D ビュー（系統樹 + 個体プレビュー）。高負荷 3D は分離プロセス。 | 中 |
| **3 (Web Three.js)** | `GaussianSplats3D` で世代スライダ再生・比較モード（親子/島間）。MVP=静的 splat 列 + 補間。 | 中 |
| **4 (4DGS 本格化)** | 上位候補のみ 4D/Deformable GS 化で計算制御。Candidate Arena に「見た目の進化」人間評価軸。 | 高 |
| **5 (Open-ended 演出)** | MAP-Elites 面 + 系統樹 + 3DGS 再生を同期、探索そのものを主役化。「最良個体」でなく「新奇性の歴史」を見せる。 | 高 |

## 5. honest disclosure / 反証（"魅せる" と "正直" の両立）

- **可視化が誇張にならない**: 3DGS の見栄えで「進化が成功しているように見せる」のは禁物。今回の monoculture（8→2、"私と friston だけ"）のような**失敗も魅せる**（失敗突然変異ゴースト / 系統絶滅フェード）= honest disclosure を可視化に焼き込む（[[feedback_benchmark_honest_disclosure]]）。proxy/real ラベルは全可視化に継続。
- **技術課題（codex）**: 同一個体トラッキング ID、トポロジ変化時の対応付け、データ容量、LOD、比較 UI。研究用途=忠実度 / デモ用途=フレームレート の二系統設計。
- **3DGS 学習コスト**: 4DGS 学習は重い → 「静的 3DGS + 補間」から段階導入（Phase 3 MVP）。
- **個体→phenotype 写像が前提**: 現進化個体は Genome3D（数値ベクトル）であり視覚的 phenotype を持たない。3DGS 化には「genome → 視覚表現」のデコーダ設計が別途必要（Karl Sims 的な形態 encoding）。これは大きな未解決課題。まず系統樹 + MAP-Elites 地形（Phase 1-2）で「多様性の地図化」を達成し、3DGS（Phase 3+）は phenotype デコーダ確立後。

## 6. 次アクション

1. **Phase 1 先行**: `evolution_to_llove.py` を拡張し系統シェア/ニッチ/相互作用を JSONL イベント化 → llove tail で時系列アニメ。
2. **MAP-Elites 地形可視化**: lldarwin の QD アーカイブ（Stage 1）を 2D グリッド地形で（多様性の地図化の核）。
3. **phenotype デコーダ調査**: genome → 視覚表現の写像（Karl Sims 形態 encoding / 3DGS 適用）を rad-research。
4. Phase 3 Web MVP は phenotype デコーダ確立後。

## 出典
- 可視化史: Conway (Sci.Am. 1970) / [Tierra (Ray 1991)](https://tomray.me/pubs/alife2/Ray1991AnApproachToTheSynthesisOfLife.pdf) / [Karl Sims SIGGRAPH'94](https://www.karlsims.com/papers/siggraph94.pdf) / [Lenia](https://arxiv.org/abs/1812.05433) / [MAP-Elites](https://arxiv.org/abs/1504.04909) / [POET](https://arxiv.org/abs/1901.01753)
- 3DGS: 4DGS CVPR2024 / 4D-Rotor SIGGRAPH2024 / 1000FPS NeurIPS2025
- 調査: codex 段階調査 2026-05-25 + WebSearch + rad-research。関連: [[LLDARWIN_DESIGN]] / [[evolution_viz_viewing_guide_2026_05_25]] / [[project_fullsense_animemd_branch_token_viz]]
