# 画像アセット・マニフェスト ― 連載「作って分かった LLM の中身」

> ビジュアルは**ベクター(SVG)で統一**した。各記事の図はすべて自作 SVG か Mermaid で、生成 AI 依存なしで完結する。
> ラスタ画像に頼らないので「push すれば表示される」状態。プロンプト集は `llm_structure_series_IMAGE_PROMPTS.md`（当初はラスタ委譲用に作成、現在は予備）。

## raw URL のルール（家訓・必読）

- Qiita は相対パスを解決しない。**必ず raw 絶対 URL**:
  `https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/llm_structure_series/<file>`
- **URL は push 済みが前提**（origin/main に push する前は 404＝非表示）。新記事は最初から raw URL で書いてよい（push 後に表示）。
- Qiita は SVG を imgix でラスタライズする（SMIL アニメ不可・静止1枚が上限）。作成した SVG は**すべて静的表示で完成**（家訓準拠・reveal-gate なし・検証済み）。JP フォントが落ちる場合のみ PNG フォールバック。判定は **Qiita 実機プレビュー**で。
- 赤緑の善悪対比なし・整形式検証済み（全 16 枚 `py -3.11 xml.dom.minidom.parse` OK）。

---

## SVG 一覧（`docs/articles/assets/llm_structure_series/`）＝ 全 28 枚・配線済み・はみ出し検査 0 件

### シリーズ横断（#0 / INDEX）
| ファイル | 役割 | 配線先 |
|---|---|---|
| `hero_00_intro.svg` | シリーズ表紙バナー（誤差ゼロ再現バッジ＋パイプライン地図） | 技術版#0 冒頭 / 一般版#0 冒頭 |
| `pipeline_map.svg` | 全体地図（①〜⑤＋壁⑥⑦、章タグ） | INDEX |
| `career_bridge.svg` | 異分野ブリッジ（計測・制御 ↔ LLM） | INDEX |
| `two_kinds_of_zero.svg` | 検証哲学の核（logits 2e-4 と max\|Δ\|=0.0 の対比） | 技術版#0 §3-2 |

### 各章ヒーロー（ダーク 1200×360）＝ tech/general 両記事の冒頭に配線
`hero_01_tokens` / `hero_02_attention` / `hero_03_block` / `hero_04_training` / `hero_05_memory` / `hero_06_practice`

### 各章コンセプト図（ライト 960×540）＝ tech 記事の該当箇所に配線
| ファイル | 内容 | 配線先 |
|---|---|---|
| `diagram_01_embedding_space.svg` | 埋め込み空間（王−男+女≈女王、「≈≠」注記） | 技術版#1 |
| `diagram_02_qkv_attention.svg` | QKV注意（softmax(QKᵀ/√d)V・O(T²)/KV O(T)） | 技術版#2 |
| `diagram_03_knowledge_location.svg` | 知識の分業（attention=検索 / FFN=貯蔵庫、×N層） | 技術版#3 |
| `diagram_04_training_loop.svg` | 学習ループ=校正ループ＋文字LM会話不能のnull | 技術版#4 |
| `diagram_05_kv_growth.svg` | KVキャッシュ膨張（4.72→37.75MB ×8 vs 定数状態平坦・交差点227） | 技術版#5 |
| `diagram_06_eval_traps.svg` | 評価の罠（勝者の呪い / PPLだけは危険 2bit top1 -13.5pp） | 技術版#6 |

### 補助図（ライト 960×540）＝ tech 記事の各節に配線済み
| ファイル | 内容 | 配線先 |
|---|---|---|
| `aux_01_tied_embeddings.svg` | 重み共有＝入口と出口が同じ1枚の行列（ゴースト第2行列で「二重に持たない」を可視化） | 技術版#1 §3-4 |
| `aux_02_template_matching.svg` | 相関（テンプレートマッチング）↔ 注意スコアの左右対比＋argmax/softmax | 技術版#2 §3.2 |
| `aux_02_rope_phase_clock.svg` | RoPE＝周波数ごとの位相時計（針角度は厳密計算・シフト定理） | 技術版#2 §3.6 |
| `aux_02_cost_curves.svg` | 計算 O(T²) 放物線 vs メモリ O(T) 直線（概形・→第5回） | 技術版#2 §3.8 |
| `aux_03_swiglu_gate.svg` | SwiGLU「広げて畳む」＝門番の枝×素材の枝の要素積 | 技術版#3 |
| `aux_04_pretrain_vs_scratch.svg` | ゼロから学習（11.9M・ppl38＝会話不能）vs 事前学習済み（差は重み） | 技術版#4 |
| `aux_04_sampling.svg` | 次トークン分布と greedy / temperature・top-p の選び方 | 技術版#4 |
| `aux_05_crossover.svg` | per-token 損益分岐（交差点≈227トークン、T=8192で36×） | 技術版#5 |
| `aux_05_bitwidth_cliff.svg` | 量子化ビット幅の崖（int8安全牌／3bit=PTQ床／2bit=QAT領域＋97%ゲート） | 技術版#5 |
| `aux_06_context_sweep.svg` | 文脈長スイープ（短文脈proxyは長文脈コストを過小検出） | 技術版#6 |
| `aux_06_knowledge_injection.svg` | RAG vs 微調整 vs 蒸留の三択比較 | 技術版#6 |
| `aux_06_responsible_pillars.svg` | 責任ある設計の四柱（ローカル完結・HITL・fail-closed・誠実な開示） | 技術版#6 |

---

## Mermaid（各記事の本文に埋め込み済み・そのまま描画）

構造図の一部は Mermaid コードブロックとしても本文に入っており、Qiita/GitHub がネイティブ描画する。SVG と併存。追加作業なし。

---

## 残りの任意スロット（未配線・非ブロッキング）

一部の tech 記事本文に、担当図と重複しない補助スロットが `**[画像プレースホルダ]**`（太字テキスト）として残っている（例: #2 の RoPE 時計・相関対比、#4 の pretrain_vs_scratch、#5 の per-token 損益分岐、#6 の RAG 三択・文脈長スイープ・責任四柱）。**壊れ画像にはならない**（画像リンクでなく太字テキスト）。必要なら後日 SVG 追加 or 削除。プロンプトは `IMAGE_PROMPTS.md` に残置。

---

## 配線状態（まとめ）

- **SVG 16 枚すべて作成・整形式検証済み・raw URL で配線済み**（INDEX / #0 tech・general / #1-6 tech は hero+diagram / #1-6 general は hero）。
- **未 push**: raw URL は push 前は 404。**push は要ユーザー判断**（no-push 規律）。push 後、Qiita 実機で SVG 表示（特に JP フォント）を確認し、落ちるものだけ PNG フォールバックへ。
- ラスタ生成は不要になった（ベクターで統一）。`IMAGE_PROMPTS.md` は予備として残置。
