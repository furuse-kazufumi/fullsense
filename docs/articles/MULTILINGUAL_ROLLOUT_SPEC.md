# QIITA #24 series — 多言語 rollout spec (agent briefing)

> 1 記事を **4 言語自己完結形式** (JA→EN→ZH→KO 全文縦積み) に作り替えるための
> 完全手順。#24-02 が公開済テンプレ、#24-03 が本ツール導入後の worked example。

## 形式 (#24-02 / #24-03 に完全に倣う)

1. **frontmatter** (YAML):
   - `title:` は **必ずシングルクオートで囲む** (コロン含みで YAML 誤パース→全フィールド崩壊)
   - `tags:` は `FullSense` / `llive` / `解説` の 3 つ
   - `private:` は記事の可視性に合わせる (公開=false / 限定共有=true)
   - `id:` は指定の hash、`organization_url_name: null`、`slide: false`、`ignorePublish: false`
   - `updated_at: '2026-05-23'`
2. frontmatter 直後に 1 行: `言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)`
3. `---` 区切り → `# 日本語` → (JA 全文) → `---` → `# English` → (EN 全文) → `---` → `# 中文` → (ZH 全文) → `---` → `# 한국어` → (KO 全文)
4. 各言語セクションは **完全自己完結**: その言語の H1 タイトル / hero・progress・theme SVG / コンセプト hook / 全 section / References / Series Navigation を **複製 + 翻訳**。
5. **旧形式は全削除**: `<small><strong>EN:</strong> … / <strong>中:</strong> …</small>` の断片翻訳、`<!-- *-placed -->` placeholder コメント、本文中の不要な裸 `>` 行。

## SVG 参照規則

- JA セクション: `qiita_24_XX_{hero,progress,theme}.svg` (base, 既存)
- EN: `..._{hero,progress,theme}_en.svg` / ZH: `_zh` / KO: `_ko`
- raw URL prefix: `https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/`
- 画像 alt テキストもその言語に翻訳する。

## SVG variant 生成 (手書き禁止、ツール必須)

`scripts/svg_i18n.py` を使う (geometry/animation 不変、`<title>`/`<text>`/`aria-label` のみ翻訳、minidom で well-formed 検証、改行保持)。base が存在する SVG 種別だけ作る (一部記事は theme 無し)。

```bash
cd D:/projects/fullsense
# 1) 各 base SVG から翻訳対象文字列を抽出 (UTF-8 必須)
for t in hero progress theme; do
  PYTHONIOENCODING=utf-8 py -3.11 scripts/svg_i18n.py extract docs/articles/assets/qiita_24_XX_$t.svg > /tmp/24_XX_${t}_keys.json
done
# 2) /tmp/24_XX_*_keys.json を Read tool で読み、scripts/svg_maps/map_24_XX.json を作る
#    形式: { "原文文字列": {"en":"...","zh":"...","ko":"..."}, ... }
#    - 純記号/番号/既英語の技術ラベル (A, B, Z3, TRIZ, "Phase 0" 等) は map に入れない (passthrough)
#    - base が既に英語の文字列は en を "" にして passthrough、zh/ko だけ訳す
# 3) 9 (or 6) variant を生成
for t in hero progress theme; do for l in en zh ko; do
  PYTHONIOENCODING=utf-8 py -3.11 scripts/svg_i18n.py gen docs/articles/assets/qiita_24_XX_$t.svg scripts/svg_maps/map_24_XX.json $l
done; done
# 4) well-formed 検証
PYTHONIOENCODING=utf-8 py -3.11 scripts/svg_i18n.py verify docs/articles/assets/qiita_24_XX_*_en.svg docs/articles/assets/qiita_24_XX_*_zh.svg docs/articles/assets/qiita_24_XX_*_ko.svg
```

## public/ コピー

最後に docs マスターを publish 用にコピー:
```bash
cp "docs/articles/QIITA_#24_XX_<name>.md" "tools/qiita-cli-poc/public/<id>.md"
```

## Series Navigation の URL (LINK_MAP より、可視性で /items/ か /private/ が決まる)

| 章 | id | URL path | 可視性 |
|---|---|---|---|
| (0) index | 07b4882e872994b27b3c | items | 公開 |
| (1) 忘れない LLM | a5ebb3992e4c28862f47 | items | 公開 |
| (2) 10 軸で考える AI | bdfad6db3f2e70c40511 | private | 限定共有 |
| (3) 矛盾は計算できる | fa0890f136636d495ea6 | private | 限定共有 |
| (4) 収束する脳 | e5093e4816b25c1bd4d0 | private | 限定共有 |
| (5) 集団が学ぶ AI | 07b686ea311e06027f94 | private | 限定共有 |
| (6) Transformer の外 | 6da5a883fb2ed651edd8 | private | 限定共有 |
| (7) 審査つき AI | c5f2077a3399d3fc9b26 | private | 限定共有 |
| (8) lleval / 眼鏡を作る | e49b7ab9027d93594402 | private | 限定共有 |

URL 例: `https://qiita.com/furuse-kazufumi/private/fa0890f136636d495ea6` (限定共有) /
`https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c` (公開)。
index は常に `items/07b4882e872994b27b3c`、repo は `https://github.com/furuse-kazufumi/llive`。

## 章キャッチコピー 4 言語 (nav リンク文言、#24-02/#24-03 と統一)

| 章 | JA | EN | ZH | KO |
|---|---|---|---|---|
| (1) | 忘れない LLM | The LLM that Never Forgets | 不会遗忘的 LLM | 잊지 않는 LLM |
| (2) | 10 軸で考える AI | AI that Thinks in 10 Axes | 用 10 个轴思考的 AI | 10개 축으로 사고하는 AI |
| (3) | 矛盾は計算できる | Contradictions Can Be Computed | 矛盾是可以计算的 | 모순은 계산할 수 있다 |
| (4) | 収束する脳 | The Converging Brain | 收敛的大脑 | 수렴하는 뇌 |
| (5) | 集団が学ぶ AI | The Population that Learns | 学习的群体 | 집단이 학습하는 AI |
| (6) | Transformer の外 | Beyond the Transformer | Transformer 之外 | Transformer 의 밖 |
| (7) | 審査つき AI | AI with Built-in Review | 带审查的 AI | 심사가 붙은 AI |
| (8) | 眼鏡を作る | Making the Glasses | 制作眼镜 | 안경을 만든다 |

(0) index は catch 無しで "series index"。

## 翻訳方針

- 技術用語 (ChangeOp / Approval Bus / Z3 / persona / sub-block / RUST-15 等) は原語維持。
- honest disclosure / コンセプト hook の語り口は #24-02 の各言語版のトーンに合わせる。
- 数表・Mermaid・コードブロックは各言語に複製。Mermaid のノードラベルは訳す (技術 ID は維持)。
- 公開資料に D ドライブやローカル絶対パスを書かない。repo 相対パス (`docs/...`, `src/...`) は #24-02 同様そのまま可。
- 画像 placeholder 禁止。

## 完了後の報告 (git / qiita publish は実行しない)

報告に含める: 最終行数、`# 日本語`/`# English`/`# 中文`/`# 한국어` の各カウント (各 1)、
SVG verify 結果 (全 ok)、public/ コピー先。**git commit と `npx qiita publish` は main が行うので絶対に実行しない。**
