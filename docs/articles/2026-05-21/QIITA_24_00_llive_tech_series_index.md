---
title: llive 完全解説 #24-00 — series index: 大分類 8 記事 + 全体図
tags:
  - FullSense
  - llive
  - 解説
  - アルゴリズム
  - SoftwareArchitecture
private: false
updated_at: '2026-05-21'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

<!--
Qiita タグ 5 個 (FullSense / llive / 解説 / アルゴリズム / SoftwareArchitecture).
本 index は series の navigator. 各大分類は個別記事 (QIITA_24_01〜08) に分割.
-->

> 投稿可否は user 判断. これは agent 自律ドラフト. memory
> `feedback_articles_taxonomy_split` 準拠の **大/中/小分類** series 構成.

## 0. この series について

llive (FullSense ™ 思考層) を **構成する技術 / アルゴリズムを名称ごとに
解説する series** です. 1 記事に詰め込むと 8 万字級になるため,
**大分類 8 記事** に分割します.

各記事の構造:
- **冒頭 hook** (8 秒 read で「これは何か」)
- **中分類 3-7 個** に分けた小節
- **各小分類 = 具体的な class / function / 機能名** で解説
- **実コード GitHub link** を中分類ごとに
- **References / 引用文献** (学術 / OSS / 内部)
- **cross-link** (前 / 次 / 本 index / repo)

8 記事は **週 2 本ペース** で 1 ヶ月かけて publish 予定. ja Qiita + en
Medium 並走 (`feedback-overseas-tech-platforms` (内部参照) に従う).

## 1. Series 構成 (8 大分類)

| # | タイトル | 中分類 | 想定文字数 | 状態 |
|---|---|---|---|---|
| 01 | **memory layer** — llive の 4 層メモリ | semantic / episodic / structural / parameter / surprise gating | 8-12k | 🚧 |
| 02 | **思考因子 + COG-MESH** — 10 因子と 9 component | 構造化 / 再構成 / 閉ループ / ... / proactive / quarantine / 5W1H | 10-15k | 🚧 |
| 03 | **構造進化 (TRIZ × bounded modification)** | TRIZ 40 原理 / ChangeOp / verifier / 9 画法 | 8-12k | 🚧 |
| 04 | **収束型最適化 (B-0〜B-9)** | SynapticSelector / UCB1 / Hebbian / B-9 実 production 注入 | 8-12k | 🚧 |
| 05 | **進化型最適化 (v0.B + v0.C)** | Genome / SegmentCrossover / Tournament / Mutation / lineage / checkpoint | 12-15k | 🚧 |
| 06 | **LLM backend 層** — non-transformer 5 案 | Mamba / Jamba / RWKV / Diffusion / 思考因子→SSM Δ Bridge | 10-15k | 🚧 |
| 07 | **観測 + 統治** | runtime_metadata / Approval Bus / governance / honest disclosure | 8-10k | 🚧 |
| 08 | **lleval (eval framework)** | progressive size matrix / 5+1 軸 / judge rotation / bridges/llive | 8-12k | 🚧 |

合計 **~80k 字** (週 2 本 × 4 週). 完走目標 2026-06-20.

## 2. 全体図 (8 layer の関係)

```mermaid
flowchart TB
    subgraph 認知層
      M[01: memory layer<br/>4 層メモリ]
      C[02: 思考因子 + COG-MESH<br/>10 因子 + 9 component]
      S[03: 構造進化<br/>TRIZ + ChangeOp]
    end
    subgraph 最適化層
      OPT_CONV[04: 収束型<br/>SynapticSelector + UCB]
      OPT_EVO[05: 進化型<br/>GA + 19 dim Genome]
    end
    subgraph 実行層
      BE[06: LLM backend<br/>5 案 non-transformer]
    end
    subgraph 横断層
      OBS[07: 観測 + 統治<br/>runtime_metadata + governance]
      EVAL[08: lleval<br/>5+1 軸 eval framework]
    end
    M --> C
    C --> S
    S --> OPT_CONV
    OPT_CONV --> OPT_EVO
    OPT_EVO --> BE
    OBS --> M
    OBS --> OPT_EVO
    EVAL --> BE
    EVAL --> OPT_EVO
```

「**認知層 → 最適化層 → 実行層**」の縦が llive の処理 flow,
「**観測 + 統治**」「**lleval**」が横断層として全 layer に効く構造.

## 3. 命名規約

### 3.1 タイトル形式 (2026-05-22 確定統一規約)

全 9 本 (#24-00 〜 #24-08) は以下の形式に揃える:

```
llive 完全解説 #24-XX — 「キャッチコピー」: <技術名称>
```

3 要素:
1. **「llive 完全解説」** — シリーズ名 (検索性 + ブランド一貫性)
2. **「#24-XX」** — 連番 (内部参照 + 公開時の章番号)
3. **「キャッチ」+「技術名称」** — em-dash (`—`) で区切る

例外: #24-00 (index 記事) はキャッチ無しで
`llive 完全解説 #24-00 — series index: <概要>` 形式.

詳細は `QIITA_24_LINK_MAP.md` 参照.

### 3.2 ファイル名規約

`QIITA_24_<NN>_<topic>.md` (本 series 全体に `24`).

| ファイル | 内容 |
|---|---|
| `QIITA_24_00_llive_tech_series_index.md` | 本 index (本ファイル) |
| `QIITA_24_01_memory_layer.md` | 01 記事 |
| `QIITA_24_02_thought_factors_cog_mesh.md` | 02 記事 |
| `QIITA_24_03_structural_evolution_triz.md` | 03 記事 |
| `QIITA_24_04_convergent_optimization_b_series.md` | 04 記事 |
| `QIITA_24_05_evolutionary_optimization_v0bc.md` | 05 記事 |
| `QIITA_24_06_llm_backend_non_transformer.md` | 06 記事 |
| `QIITA_24_07_observability_governance.md` | 07 記事 |
| `QIITA_24_08_lleval_eval_framework.md` | 08 記事 |

en 版は `_en.md` suffix.

## 4. 共通フォーマット (各記事に適用)

### a. 冒頭 hook (`feedback-articles-concept-hook` (内部参照))

1-2 段落で「**この記事の主題 + 数字 + キー名称**」を凝縮.

### b. 中分類 = `## <名称>` 見出し

中分類 1 つにつき 1500-3000 字目安.

### c. 小分類 = `### <class/function/機能名>` 見出し

実コードへの GitHub link を **必ず** 付ける (`feedback-qiita-github-links` (内部参照)):

```markdown
### SynapticSelector

実装: [`src/llive/perf/synaptic_selector.py`](https://github.com/furuse-kazufumi/llive/blob/main/src/llive/perf/synaptic_selector.py)

ε-greedy + Hebbian-style weight update を組み合わせた variant selector.
bounded modification (§E2) で min/max clip 必須.
```

### d. 教訓 / 設計判断 (3-5 個)

中分類後の小節として「**なぜこの設計か**」を honest disclosure.

### e. References (`feedback-articles-references-section` (内部参照))

学術 / OSS / 内部 の最低 3 区分.

### f. cross-link

```markdown
## Series cross-link

- ← 前: [QIITA #24-NN](link)
- → 次: [QIITA #24-MM](link)
- 全体: [本 series index](QIITA_24_00)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
```

> ⚠ **Cross-link URL は Qiita 投稿後に確定する**. draft 段階では各記事の
> 本文中で `#24-XX` / ``QIITA_24_XX_*` (内部参照)` の **仮表記** で参照し, 投稿後に
> 個別記事 URL (`https://qiita.com/.../items/<hash>`) に **一括置換**.
> mapping は [`QIITA_24_LINK_MAP.md`](QIITA_24_LINK_MAP.md) で唯一の
> source of truth として管理. 投稿時に **追々修正**する運用.

## 5. 想定読者

- **エンジニア** (Python + LLM 基礎知識あり)
- **AI researcher** (LLM の周辺アーキテクチャに興味)
- **個人 OSS author** (実装パターンの参考)
- **企業 R&D** (on-prem LLM stack の検討材料)

## 6. 公開順 (週 2 本ペース)

| 週 | 公開記事 |
|---|---|
| Week 1 (5/22-5/28) | 01 memory + 02 思考因子 |
| Week 2 (5/29-6/4) | 03 構造進化 + 04 収束型 |
| Week 3 (6/5-6/11) | 05 進化型 + 06 LLM backend |
| Week 4 (6/12-6/18) | 07 観測統治 + 08 lleval |

各記事の en 版は **+1 週遅れ** で Medium に投稿.

## 7. References (本 index)

### 内部 cross-reference

- portal `docs/PROGRESS.md` (累積セッション履歴)
- portal `docs/spec/index.md` (Spec hub)
- llive `docs/fullsense_spec_eternal.md` (FullSense Spec v1.1)
- llive `docs/requirements_v0.1〜v0.C` 系
- llive `docs/non-transformer/ROADMAP.md`

### 関連 maintainer memory

- `feedback_articles_taxonomy_split` (本 series 構成方針)
- `feedback_articles_concept_hook` (冒頭 hook)
- `feedback_qiita_long_form` (長文 OK)
- `feedback_qiita_github_links` (GitHub link 積極配置)
- `feedback_articles_references_section` (本セクション必須化)
- `feedback_no_image_placeholders` (Mermaid OK)
- `feedback_article_humor_style` (漫才禁止)
- `feedback_overseas_tech_platforms` (Medium en 並走)
- `feedback_reader_attention_curve` (8 秒/90 秒/5 分)

## 8. 状態 (2026-05-21 着手 → 2026-05-22 更新)

- ✅ index (本ファイル) 着地
- ✅ **#24-01 〜 #24-08 draft 全 9 本着地** (2026-05-22 marathon 内)
- ✅ 命名規約 + 共通フォーマット確定
- ✅ **タイトル統一規約確定** (2026-05-22): `llive 完全解説 #24-XX — 「キャッチ」: <技術名称>`
- ✅ memory `feedback_articles_taxonomy_split` で運用ルール化
- ✅ **Cross-link URL mapping** を `QIITA_24_LINK_MAP.md` に集約 (投稿後 URL 確定→ 一括置換運用)
- 🚧 各記事の full 10x volume (80-120k 字) 版は次セッション以降
- 🚧 Qiita 投稿は user 判断待ち (週 2 本ペース)

### 2026-05-22 追記 — Rust 高速化マラソン成果

連載中核 #24-05 で扱う v0.E 派生集団進化の hot path 3 つを 1 日で Rust 化:

- **RUST-15** persona_dissimilarity_pairwise: avg **x12.71** (batch)
- **RUST-16** collusion_score_kernel: avg **x66.70** (numpy 小 N hot path)
- **RUST-17b** novelty_score_batch (rayon + quickselect): avg **x9.32** (全 A 5x clear)

詳細は #24-04 (B-series 文脈で直交性) / #24-05 (中核) / #24-07 (governance
latency 100x 短縮). 5 パターン判定表は repo
`docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md`.

「**Rust 化 = 速い」は嘘 / 「numpy = 速い」も嘘** — 実装方法 (FFI 境界 /
batch / numpy zero-copy / 並列度 / partial sort) で結果が桁違い. この
honest disclosure 体験が連載全体の通奏低音.

### 2026-05-22 追記 (セッション末) — ハーネス型バイブコーディング視点

連載全体を貫く方法論として、本日セッション末でユーザーが言語化した
**ハーネス型バイブコーディング (Harness-style Vibe Coding, HVC)** を
追加しておく. Karpathy "vibe coding" との差は、harness (Claude Code 等
agent 駆動環境) を **ユーザーが能動的に握り続ける** こと.

HVC で要る 3 能力:

1. **発想力** — 異分野連想 (例: キン肉星王位争奪編 + ROS 歩行進化 +
   Lehman&Stanley novelty search が同じ構造に収束する)
2. **経験則** — 失敗パターン先読み
3. **アルゴリズムへの理解** — 実装妥当性検証 (RUST-15 単発 0.80x → batch
   12.71x の差を瞬時に評価)

加えて **AI 成長マネジメント力** = 部下育成と同等. 委任範囲 / 進捗確認 /
失敗許容 / 個性尊重 / 多数決抑制 / 世代交代 / 信頼関係構築. キヤノン
「三自の精神」(自発/自治/自立) を AI に転写するのと同じ系譜.

### 2026-05-22 追記 — 派生集団進化の発想原典

#24-05 (EvolutionLoop) と v0.F (2 階建てゲノム) の発想は **技術側と
文化側 2 系統の anchor が同時に手元にあった** から自然に出てきた:

- **技術側**: ROS Population-Based Training (歩行進化), Hillis 1990 Red
  Queen, Lehman & Stanley 2011 novelty search, AlphaStar 2019 PBT,
  Mouret & Clune 2015 MAP-Elites
- **文化側**: キン肉星王位争奪編 (1985-87, ゆでたまご) / リィンカーネー
  ションの花弁 (2013-24, 三栖ハル) / R.O.D シリーズ (1998〜, 倉田英之)

3 漫画の共通項 = (派生個体集団 / 個性継承 / 競争 / 協調 / 進化) が、
v0.F の `Genome = (C-impl: 実装層, C-prompt: 偉人思想層)` 2 階建て設計
とほぼ完全に対応. 技術論文と漫画作品が同じ構造を別経路で示していた
事実そのものが [[project_llive_dev_style]] (第二の脳型スパイラル開発) の
典型例.

詳細は memory `project_llive_kinniku_metaphor` /
`project_llive_reincarnation_rod_metaphor` /
`feedback_harness_vibe_coding` (本 repo `.memory` 配下に近日整理予定).

### 2026-05-22 追記 — v0.F/G/H 要件メモ着地

本日セッションで要件メモ 3 本を新規着地 (llive リポ):

- **v0.F** 2 階建てゲノム + Novelty Lane + Similarity Quota crowding +
  統計駆動評価 → `docs/requirements_v0.F_genome_two_layer_and_novelty.md`
- **v0.G** 漫画読解 (VLM 補助) + HumorKB (構造のみ) + 定着済ネットミーム +
  日本語多義性 (スナックバス江 reference) → `docs/requirements_v0.G_manga_reading_humor.md`
- **v0.H** マスコット/ブランディング (古瀬あい衝突回避 + Transformer 脱却
  後コラボ路線) → `docs/requirements_v0.H_mascot_branding.md`

加えて `.claude/skills/manga-ocr/` に Apache-2.0 ライセンスの kha-white
manga-ocr の skill skeleton を配備. Magi (academic only) は llive 商用
ライセンスと非互換のため不採用.
