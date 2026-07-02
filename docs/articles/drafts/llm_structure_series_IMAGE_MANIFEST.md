# 画像アセット・マニフェスト ― 連載「作って分かった LLM の中身」

> 各記事の画像スロットを「埋め込むだけ」にするための対応表。3 系統に分ける:
> **(A) SVG（作成済・このリポジトリ内）** / **(B) Mermaid（各記事の本文にコード埋め込み済＝そのまま描画）** / **(C) ラスタ（画像AIに委譲）**。
> プロンプトの本体は `llm_structure_series_IMAGE_PROMPTS.md`。本ファイルはファイル名・URL・alt・配線状態の管理台帳。

## raw URL のルール（家訓・必読）

- Qiita は相対パスを解決しない。**必ず raw 絶対 URL**:
  `https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/llm_structure_series/<file>`
- **URL は push 済みが前提**（origin/main に push する前は 404＝非表示）。新記事は最初から raw URL で書いてよい（push 後に表示される）。
- Qiita は SVG を imgix で**ラスタライズ**する（SMIL アニメ不可・静止1枚が上限）。**動きが要るならアニメ GIF**。JP フォントが落ちる場合は PNG フォールバック。判定は必ず **Qiita 実機プレビュー**で。
- SVG は authored 属性を最終可視値にする（reveal-gate 禁止＝静的表示で完成形が見える）。作成済み 3 枚はこの規律に準拠。

---

## (A) 作成済み SVG（`docs/articles/assets/llm_structure_series/`）

| ファイル | 役割 | 主な使用先 | alt |
|---|---|---|---|
| `two_kinds_of_zero.svg` | 検証哲学の核。logits 2e-4（実質ゼロ）と max\|Δ\|=0.0（ビット一致）を対比 | 技術版#0 / 一般版#2 | 二種類のゼロ。自作 forward は公式と logits 2e-4 で一致、メモリ最適化ローダーは max\|Δ\|=0.0 のビット一致 |
| `pipeline_map.svg` | シリーズ全体地図（①〜⑤＋現実の壁⑥⑦、章タグつき） | INDEX / 技術版#0 | LLM の処理の流れ。トークン化→埋め込み→注意機構→順伝播層→次の一語、を自己回帰で繰り返す |
| `career_bridge.svg` | 異分野ブリッジ（計測・制御の道具 ↔ LLM の部品） | INDEX / 技術版#0 | 計測・制御の道具と LLM 部品の対応。フーリエ↔RoPE、相関↔QKᵀ、PCA↔埋め込み、校正↔学習、品質規律↔honest ゲート |

**貼り付け用（push 後に表示。技術版#0・INDEX には配線済み）:**

```markdown
![二種類のゼロ ― 自作 forward は公式と logits 2e-4、ローダーは max|Δ|=0.0](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/llm_structure_series/two_kinds_of_zero.svg)

![LLM の処理の流れ ― 次の一語を当て続ける全体地図](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/llm_structure_series/pipeline_map.svg)

![現場の道具は AI の中で顔を出す ― 計測・制御 × LLM の対応](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/llm_structure_series/career_bridge.svg)
```

---

## (B) Mermaid（各記事の本文にコード埋め込み済み・そのまま描画）

Qiita も GitHub も Mermaid コードブロックをネイティブ描画する。**追加作業なし**。正確なラベル・数値が要る構造図（パイプライン、QKV、KVキャッシュの膨張、メモリ↔品質トレードオフ、RAG 構成 等）はこちらで担保済み。Mermaid のソース一覧は `llm_structure_series_IMAGE_PROMPTS.md` の各 §「Mermaid」を参照。

---

## (C) ラスタのヒーロー画像（画像AIに委譲）

情感・比喩の効いた「顔」画像は画像AIで生成する。プロンプト（日英）は `llm_structure_series_IMAGE_PROMPTS.md` の各章 §「ヒーロー」。**推奨ファイル名と raw URL 割り当て**（生成後、下記名で assets に置けば貼り付けは機械的）:

| 記事 | ファイル名（推奨） | プロンプト参照 |
|---|---|---|
| 技術版#0 / 一般版#0 | `hero_00_intro.png` | IMAGE_PROMPTS §#0 ヒーロー |
| #1 トークン・埋め込み | `hero_01_tokens.png` | §#1 ヒーロー |
| #2 注意機構 | `hero_02_attention.png` | §#2 ヒーロー |
| #3 Transformer ブロック | `hero_03_block.png` | §#3 ヒーロー |
| #4 学習と推論 | `hero_04_training.png` | §#4 ヒーロー |
| #5 メモリと速度 | `hero_05_memory.png` | §#5 ヒーロー |
| #6 実務編 | `hero_06_practice.png` | §#6 ヒーロー |

- スタイル指定: クリーンな技術イラスト、赤緑の善悪対比を使わない、画像内テキストは崩れやすいので英語ラベル or ラベルなし推奨（詳細は IMAGE_PROMPTS）。
- 生成 → `assets/llm_structure_series/` に配置 → raw URL `.../llm_structure_series/hero_0N_*.png` で各記事冒頭に配線。

---

## 配線状態

- **技術版#0 / INDEX**: (A) の 3 SVG を raw URL で配線済み（push 後に表示）。
- **各記事の Mermaid**: 埋め込み済み・描画OK。
- **ラスタ (C)**: 未生成（画像AI委譲待ち）。生成後、上表の名前で置けば配線は機械的。
- **未 push**: SVG も記事も push 前は raw URL が 404。**push は要ユーザー判断**（no-push 規律）。push 後、Qiita 実機で SVG 表示を確認し、JP フォント欠落なら PNG フォールバックへ。
