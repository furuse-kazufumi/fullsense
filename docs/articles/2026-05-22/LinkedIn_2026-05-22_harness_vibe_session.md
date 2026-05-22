---
title: LinkedIn post — 2026-05-22 ハーネス型バイブコーディングの夜
created_at: 2026-05-22
language: ja (LinkedIn 組込翻訳に任せる, feedback_linkedin_translation_jp_only 準拠)
audience: LinkedIn (AI 研究 + 経営層 + ロボティクス + 漫画/SF 好きエンジニア)
type: session_wrapup_long
links:
  github_org: https://github.com/furuse-kazufumi
  github_fullsense: https://github.com/furuse-kazufumi/fullsense
  github_llive: https://github.com/furuse-kazufumi/llive
  github_llove: https://github.com/furuse-kazufumi/llove
  github_llmesh: https://github.com/furuse-kazufumi/llmesh
links_deep:
  qiita_24_00: https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-21/QIITA_24_00_llive_tech_series_index.md
  qiita_24_05: https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-21/QIITA_24_05_evolutionary_v0BCDE.md
  req_v0_F: https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.F_genome_two_layer_and_novelty.md
  req_v0_G: https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.G_manga_reading_humor.md
  req_v0_H: https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.H_mascot_branding.md
  hero_svg_24_05: https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/2026-05-21/assets/qiita_24_05_hero.svg
---

# LinkedIn 投稿文 — 2026-05-22 ハーネス型バイブコーディング (日本語版)

> 投稿は日本語のみ. 他言語は LinkedIn 組込翻訳に任せる
> ([[feedback_linkedin_translation_jp_only]]).
> GitHub 内記事への deep link を本文に **5-7 本** 仕込んで, 興味を持った
> 読者が「もっと深く」読める導線を作る ([[feedback_qiita_github_links]] 拡張).

---

## 投稿本文 (LinkedIn 用, 約 2900 字 — 3000 字制限内)

**「Claude Code に *進めます* と宣言させたのが、今日の試合の半分。 残り半分は、私が harness を握り続けた時間でした。」**

— 2026 年 5 月 22 日、深夜セッション終わりの実感です。

---

**■ ハーネス型バイブコーディングという呼び方**

Karpathy の "vibe coding" は AI に全任せで雰囲気でコードを書く流儀。 私のスタイルは少し違って、Claude Code 等の harness を **自分で能動的に握り続ける** 形を取ります。 内輪で **ハーネス型バイブコーディング (Harness-style Vibe Coding, HVC)** と呼んでみることにしました。

HVC でユーザー側に要るのは 3 つの能力。

1. **発想力** — 異分野連想で高次元の方向性を示す
2. **経験則** — 設計判断のショートカット、失敗パターンの先読み
3. **アルゴリズムへの理解** — AI が出した実装の妥当性検証、計算量見積り

加えて重要なのが **AI 成長マネジメント力**。 部下を育てるのと同じくらい、AI を育てる力がユーザーに要ります。 委任範囲を決め、進捗を確認し、失敗を許し、成長を測り、個性を尊重し、多数決に従わず、引退・世代交代を仕組み、信頼関係を作る。 キヤノン「三自の精神」(自発/自治/自立) を AI に転写するのと同じ系譜です。

---

**■ 今日 (2026-05-22) の harness の使い方**

着地した成果:

- QIITA #24 連載 7 本の冒頭に **animated SVG hero** (SMIL only, no script) を着地 → [連載 index](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-21/QIITA_24_00_llive_tech_series_index.md)
- llive v0.F 要件: **2 階建てゲノム** (コード層 + プロンプト層) + Novelty Lane + Similarity Quota crowding + 統計駆動評価 → [v0.F 要件](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.F_genome_two_layer_and_novelty.md)
- llive v0.G 要件: **漫画読解** (VLM 補助) + HumorKB (構造のみ) + 定着済ネットミーム → [v0.G 要件](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.G_manga_reading_humor.md)
- llive v0.H 要件: **マスコット/ブランディング** (古瀬あい衝突回避 + 長期コラボ路線) → [v0.H 要件](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.H_mascot_branding.md)
- manga-ocr (Apache-2.0, kha-white) を `.claude/skills/manga-ocr/` に skill skeleton 化 — license 整合確認 ([Magi は academic only で却下](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.G_manga_reading_humor.md))

すべて atomic commit で着地。 [git log](https://github.com/furuse-kazufumi/fullsense/commits/main) に時系列で並んでいます。

---

**■ 派生集団進化の発想は、技術と漫画が同じ構造に収束した結果**

llive の派生集団進化 (v0.B 〜 v0.E) と 2 階建てゲノム (v0.F) は、私の頭の中で **技術側 anchor と文化側 anchor が同時に手元にあった** から自然に出てきたものでした。

**技術側**: ROS Population-Based Training (歩行進化), Hillis 1990 (Red Queen), Lehman & Stanley 2011 (novelty search), AlphaStar 2019 (PBT), Mouret & Clune 2015 (MAP-Elites).

**文化側**: キン肉星王位争奪編 (1985-87, ゆでたまご) — 5 大超人の王位争奪。 リィンカーネーションの花弁 (2013-24, 三栖ハル) — 偉人能力の宿る異才同士の戦い。 R.O.D シリーズ (1998〜, 倉田英之) — 偉人クローン軍団。

3 漫画の構造的共通項 = (派生個体集団 / 個性継承 / 競争 / 協調 / 進化) は、ROS PBT 系の **コード層染色体 `C-impl`** (実装言語 / 並列戦略 / アルゴリズム選択) と、偉人能力継承系の **プロンプト層染色体 `C-prompt`** (岡潔 / Polya / TRIZ / Six Hats の persona bitmask) で構成される v0.F 2 階建てゲノム設計とほぼ完全に対応します。

技術論文と漫画作品が **同じ構造を別経路で示していた** という事実が、「発想は単発のひらめきではなく、複数の anchor が交差した自然な帰結」というのを実証してくれました。

詳細解説は連載 [#24-05 EvolutionLoop](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-21/QIITA_24_05_evolutionary_v0BCDE.md) に。 hero SVG (animated SMIL) は [こちら](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/2026-05-21/assets/qiita_24_05_hero.svg)。

---

**■ 多数決を弱めて独自進化を保護する**

「最強だけ残す」と Lehman & Stanley が言う通り **局所最適に陥る**。 v0.F では:

- **Novelty Lane** — 振る舞いが他個体と離れている個体は専用 subprocess lane で評価
- **Similarity Quota** — 似すぎた個体は一定数で打ち止め (cluster_quota=4 デフォルト)
- **Multi-Objective Selection** — fitness top-N + novelty top-M ハイブリッド

部下育成でも同じです。 チームを優秀な人材だけで揃えると同じ思考の堂々巡りになる。 異質を一定数残し、似すぎた個体は世代交代させる。 AI 育成も同じ。

評価方法は静的固定せず、HELM / BIG-bench / Arena / SWE-bench / AgentBench を月次で追跡更新。 すべての設計判断は統計データ + A/B + 有意性で。 「速い AI」ではなく「速いと思い込ませる構成」を見抜く道具が lleval (5+1 honest disclosure 因子分解) → [#24-08 lleval](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-21/QIITA_24_08_lleval_eval_framework.md)。

---

**■ ブランドと長期コラボ路線**

llive のマスコット (v0.H) では、SELF株式会社「古瀬あい」(2017〜) との **短期切り離し** と **長期コラボ路線** を分けて設計しています。 名前衝突するのでまずは独立ブランドで立てる。 Transformer 脱却 (Mamba / Jamba / RWKV / Diffusion text) が普及した暁には、兄弟キャラ位置づけで歩み寄る余地を残す → [v0.H 要件](https://github.com/furuse-kazufumi/llive/blob/main/docs/requirements_v0.H_mascot_branding.md)。

---

**■ Repo の歩き方**

- 連載目次 (Qiita 用 markdown, GitHub 内): [QIITA #24 series index](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-21/QIITA_24_00_llive_tech_series_index.md)
- llive 本体: [github.com/furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
- llove (TUI dashboard): [github.com/furuse-kazufumi/llove](https://github.com/furuse-kazufumi/llove)
- llmesh (on-prem LLM hub): [github.com/furuse-kazufumi/llmesh](https://github.com/furuse-kazufumi/llmesh)
- セッション wrap-up (本記事の元): [fullsense portal](https://github.com/furuse-kazufumi/fullsense)

「派生集団進化 × 漫画メタファー × harness 型開発」のような交点に興味がある方、お気軽にコメント / DM / star ください。 連載は #24-00〜08 で 9 本構成、現在 draft 段階で、full 10x volume (各 80-150k 字) は次セッション以降の予定です。

---

#FullSense #llive #HarnessVibeCoding #ハーネス型バイブコーディング #派生集団進化 #PopulationBasedTraining #自己進化AI #honest_disclosure #ローカルLLM #TransformerEscape #Mamba #RWKV

---

## 投稿運用メモ

- **言語**: 日本語版のみ ([[feedback_linkedin_translation_jp_only]] 準拠, LinkedIn 組込翻訳に任せる). 既存 5/22 rust_marathon 投稿の 4 言語化はユーザー指示の例外で、本投稿は元のルール に戻す.
- **長さ**: 約 2900 字 (LinkedIn 3000 字制限を満たす). 短い段落 + 中見出しでリズム ([[feedback_reader_attention_curve]]).
- **冒頭 hook**: 1 行で読者の関心を掴む 「Claude Code に *進めます* と宣言させた...」 ([[feedback_articles_concept_hook]]).
- **deep link**: 本文中に GitHub 内 markdown / raw / commits / repo の 7 本リンクを散らし、興味を持った読者がそのまま潜れる構造 ([[feedback_qiita_github_links]] 拡張).
- **避けたもの**: 架空対話 / 落語枕 / AI 擬人化 / 過剰オノマトペ ([[feedback_article_humor_style]] 2026-05-20 NG 整合).
- **休憩ポイント**: 「部下育成でも同じです」「私の頭の中で 〜 同時に手元にあった」「— 2026 年 5 月 22 日、深夜セッション終わりの実感です」 が雑談的リズム切替 ([[feedback_article_break_points]]).
- **ハッシュタグ**: 11 個 (LinkedIn 推奨 3-5 を超過するが、SEO 多角化を優先. 通常運用なら 5 個に絞る).
- **公開後**: Qiita series URL が確定したら本文中の `github.com/.../QIITA_24_*.md` を Qiita 投稿 URL に差し替え検討 ([[QIITA_24_LINK_MAP]] と同様の運用).
