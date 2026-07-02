# LINK MAP ― 連載「作って分かった LLM の中身」投稿後 URL 台帳

> Qiita 投稿後に確定する各記事の URL をここに集約し、各記事フッターのナビ（内部参照プレースホルダ）を一括置換する。
> 運用は `QIITA_POST_GUIDE.md` §4（#24 シリーズの LINK_MAP パターン）と同じ。

## 置換の約束

各記事のフッターナビは `<<LINK:キー>>` 形式のプレースホルダで書いてある。投稿後、下表の URL で一括置換する
（未投稿のうちは Qiita 上にそのまま出るため、**投稿直前に必ず置換 or 該当行を削除**）。

## URL 台帳（投稿したら埋める）

> **投稿は完全版2本のみ**(2026-07-02 確定)。MEGA_T / MEGA_G が本番。以下の分割版キーはアーカイブ用(単体投稿しない限り未使用)。

| キー | ローカルファイル | タイトル | Qiita URL |
|---|---|---|---|
| **MEGA_T** | llm_structure_series_MEGA_tech.md | **技術版・完全版** | https://qiita.com/furuse-kazufumi/items/de27af958332c9c38e33 （限定共有中: /private/de27af958332c9c38e33） |
| **MEGA_G** | llm_structure_series_MEGA_general.md | **一般版・完全版** | https://qiita.com/furuse-kazufumi/items/f660b18890687cfd1ed0 （限定共有中: /private/f660b18890687cfd1ed0） |
| INDEX | llm_structure_series_INDEX.md | シリーズ総目次(投稿しない) | — |
| T00 | llm_structure_series_00_intro_tech.md | 技術版 #0 序章 | (未投稿) |
| T01 | llm_structure_series_01_tokens_embeddings_tech.md | 技術版 #1 トークンと埋め込み | (未投稿) |
| T02 | llm_structure_series_02_attention_tech.md | 技術版 #2 注意機構 | (未投稿) |
| T03 | llm_structure_series_03_transformer_block_tech.md | 技術版 #3 Transformer ブロック | (未投稿) |
| T04 | llm_structure_series_04_training_inference_tech.md | 技術版 #4 学習と推論 | (未投稿) |
| T05 | llm_structure_series_05_memory_speed_tech.md | 技術版 #5 メモリと速度の壁 | (未投稿) |
| T06 | llm_structure_series_06_practice_tech.md | 技術版 #6 実務編 | (未投稿) |
| G00 | llm_structure_series_00_intro_general.md | 一般版 #0 導入 | (未投稿) |
| G01 | llm_structure_series_01_tokens_embeddings_general.md | 一般版 #1 意味の地図 | (未投稿) |
| G02 | llm_structure_series_02_attention_general.md | 一般版 #2 気の配り方 | (未投稿) |
| G03 | llm_structure_series_03_transformer_block_general.md | 一般版 #3 知識のありか | (未投稿) |
| G04 | llm_structure_series_04_training_inference_general.md | 一般版 #4 なぜ賢くなる | (未投稿) |
| G05 | llm_structure_series_05_memory_speed_general.md | 一般版 #5 重くなる理由 | (未投稿) |
| G06 | llm_structure_series_06_practice_general.md | 一般版 #6 道具として | (未投稿) |

## 推奨タグ（Qiita 5 件・スペース区切り・重要度順）

| 記事 | tags |
|---|---|
| 技術版 #0 | `LLM Transformer 機械学習 自作 Qwen` |
| 技術版 #1 | `LLM 自然言語処理 機械学習 embedding tokenizer` |
| 技術版 #2 | `LLM Transformer attention 機械学習 深層学習` |
| 技術版 #3 | `LLM Transformer 深層学習 機械学習 アーキテクチャ` |
| 技術版 #4 | `LLM 機械学習 深層学習 事前学習 ローカルLLM` |
| 技術版 #5 | `LLM 量子化 ローカルLLM KVキャッシュ メモリ` |
| 技術版 #6 | `LLM ローカルLLM RAG ライセンス 機械学習` |
| 一般版 #0-6 | `AI 入門 LLM 機械学習 解説`（回により `ChatGPT` 等に差し替え可） |

> タグ規約: スペース区切り・最大5件・重要度順（[[feedback_daily_articles_policy]]）。一般版は業界・用途ベース寄りに。
