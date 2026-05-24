---
layout: default
title: "ペルソナ ontology 拡張 — affinity 自動算出 (ハードコード排除)"
nav_order: 100
parent: Research
---

# ペルソナ ontology 拡張 — affinity 自動算出 (ハードコード排除)

> 2026-05-24。llive 進化ゲノムの persona ontology を段階的に数百人規模へ拡張する基盤整備。
> 核心の教訓 = **手で付けた factor_affinity はハードコードで疑わしい → 記述文から自動算出**
> ([[feedback_benchmark_honest_disclosure]] の実践)。投入自体は段階的 (急がない、ユーザー方針)。

## 3 行サマリ

1. 最初に拡張 7 名へ手で付けた `factor_affinity` (数値) を **ユーザー指摘「ハードコードを疑え」で撤回**。
2. `persona_extended.py` で各人物の `affinity_text` (特性記述文) から **keyword_extractor +
   affinity_from_counts で自動算出** (数値ハードコードなし、根拠が記述に残り疑える)。
3. 数百人投入の**下調べ完了** — 分野横断・多様性 (非西洋/女性/古典〜現代) の候補カタログ約 60 名 +
   投入手順 + 改善メモ。実投入は段階的に。

## 経緯と設計判断

llive `PERSONA_ONTOLOGY` (古典 10 + 研究方法論 4 = 14) に歴史人物を増やす作業で、最初は 7 名
(darwin/altshuller/helmholtz/shannon/turing/poincare/kahneman) に `factor_affinity` を**手で付与**した。
これに対しユーザーから「ハードコード部分はちょっと疑った方が良い」との指摘。

→ 手書きの affinity ベクトルは**根拠が弱く捏造に近い**ため撤回。代わりに:

- 各人物に **`affinity_text`** (FACTOR_KEYWORDS が拾える特性記述文) を持たせ、
  `persona_corpus_loader.keyword_extractor` + `affinity_from_counts` で factor_affinity を**自動算出**。
- `thought_patterns` (意味ある特性語) は別途保持 (抽出語は FACTOR_KEYWORDS の語そのものになり意味が薄いため、affinity 算出と役割を分離)。
- 数値の根拠が `affinity_text` に残るので「なぜこの因子が高いか」を**追える=疑える**形。

**検証**: 算出 top 因子が記述意図と整合 (darwin→reality_link/exploration、altshuller→structurize/recompose、
turing→exploration、poincare→recompose、shannon→consistency/uncertainty…)。全員 affinity_text 由来
(全 0.5 = 情報なし中央 はゼロ)。回帰テスト 6 件 + 既存 persona テストの件数 hard-code を下限チェックに緩和。

## 着地物 (commit `d940ff3`, branch optimize/core-2026-05-20)

- `llive/src/llive/perf/evolutionary/persona_extended.py` — affinity 自動算出 + `register_extended_personas()` (冪等 merge, import 副作用で登録)
- `persona.py` — 手動ハードコードの 7 名を撤回 (古典 14 に戻す)
- `tests/unit/test_evolutionary_persona_extended.py` (6 件) + `test_evolutionary_persona.py` 柔軟化
- RAD コーパス (D:/docs, git 管理外): `persona_ontology_v2/SKILL.md` (21 名) + `_CANDIDATES.md` (投入候補約 60 名 + 改善メモ)

## 段階的投入の下調べ (候補カタログ)

`D:/docs/persona_ontology_v2/_CANDIDATES.md` に分野横断 15 分野・約 60 名の名簿。**多様性を意識**:
非西洋 (関孝和/イブン=ハイサム/班昭/Rabia of Basra/Nana Asma'u)、女性研究者 (キュリー/マクリントック/
ラブレス/ホッパー/メドウズ/ヒュパティア)、古典〜現代 (カルパシー/サットン/ヒントン)。

投入手順: バッチ選定 → `affinity_text` 記述 → 自動登録 → top 因子検算 → 偏り補正。後は記述文を書くだけ。

## honest disclosure

- `affinity_text` 方式も「FACTOR_KEYWORDS に当たる語を選んで書く」点で**なお heuristic**。手動数値より
  透明 (根拠が text に残る) だが、真の精緻化ではない。
- **本命 = LLM injection**: `ThoughtPatternExtractor` Protocol に on-prem LLM を注入し伝記から直接抽出
  (キーワード埋め込み不要、measurement purity 遵守)。
- RAD は論文メタデータ中心で**伝記が薄い** → 実伝記 corpus (公開 snippet 等、ライセンス確認) が別途要る。
- **既存の古典 14 + 研究方法論 4 の affinity も手動**。ハードコード排除の一貫適用なら段階的に自動算出へ
  移行する余地があるが、既存テストが特定値を assert しているため慎重に。

## Sources / 関連

- 実装: `llive/.../persona_extended.py` (commit `d940ff3`) / `persona.py` / `persona_corpus_loader.py` (CE-23 skeleton)
- RAD: `D:/docs/persona_ontology_v2/` (SKILL.md + _CANDIDATES.md)
- 多様性補完: [Women Philosophers from Non-Western Traditions (Springer)](https://link.springer.com/book/10.1007/978-3-031-28563-9) / [Project Vox (Duke)](https://today.duke.edu/2025/02/lost-and-found-bringing-historys-female-philosophers-forefront)
- memory: project_persona_genome_integration / feedback_provenance_research_method / feedback_benchmark_honest_disclosure
