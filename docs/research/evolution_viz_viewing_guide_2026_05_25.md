# 進化ラン可視化 — 成果物カタログと閲覧ガイド (2026-05-25)

> **目的**: 進化ラン (`llive scripts/run_persona_evolution_long.py`) の出力を **どのツールで
> どう開くか** を手順付きで示す。「コマンドを口頭で言われても技術資料に手順が無いと意味が
> 分からない」(ユーザー 2026-05-25) への恒久回答。サンプル run = `D:/projects/llive/out/evo_seekvalue_2026_05_25/`。

## 0. 結論サマリ (先に読む)

- **SVG (グラフ/系統 stream)** → **モダンブラウザ (Edge/Chrome) で開く**。`.svg` の既定が
  Internet Explorer になっている環境が多い (動くが非推奨)。
- **Mermaid (`.mmd`)** → **VS Code + Mermaid 拡張**、または小さいものは **mermaid.live**。
  `.mmd` は OS 未関連付けなのでダブルクリック/`Start-Process` では「関連付け」ダイアログが出る。
- **JSONL (メトリクス/イベント)** → **`llove tail`** (進化を端末でライブ表示)。ただし
  **変換が必要** (§4)。生の `metrics.jsonl` は llove スキーマ非対応で表示されない。
- **llove は現状 SVG/Mermaid を直接表示するビューアではない** (§5)。SVG はブラウザ、
  Mermaid は VS Code が推奨。llove で見るのは「変換した JSONL イベント」に限る。

## 1. 成果物カタログ (何が・何の証拠か)

| ファイル | 形式 | 中身 | 何の証拠 |
|---|---|---|---|
| `metrics.jsonl` | JSONL | 毎世代 best/mean/std/median/diversity_l2 (501 行) | 適応度・多様性の時系列 |
| `generations.jsonl` | JSONL | 同上を checkpoint 刻み (21 行) | SVG 描画の軽量版 |
| `founder_lineage.jsonl` | JSONL | 毎世代 founder_counts (どの founder 系統が何個体) | **ペルソナ系統の淘汰**(8→2) |
| `winners.jsonl` | JSONL | 世代別 top3: individual_id / **parent_ids** / score | **交配 (2親) / 変異 (1親)** |
| `snapshot_gen_*.json` | JSON | 各世代の全個体 (genome.c_prompt.persona_set 等) | **ペルソナが genome に載る** |
| `lineage.mmd` | Mermaid | 全個体系統樹 (227KB, 巨大) | — (大きすぎて実用外) |
| `evolution.svg` | SVG | fitness/diversity 時系列アニメ | 集団統計 (個体は見えない) |
| `persona_dominance.svg` | SVG | founder 系統 stacked-area アニメ | **進化・淘汰 (8→2収束)** |
| `champion_lineage.mmd` | Mermaid | 最終勝者の親系統 (縮約, 2KB, renderable) | **交配の系譜** |
| `llove_events.jsonl` | JSONL | metrics を llove Event 形式に変換 (§4) | llove tail 用 |

**ペルソナ反映・交配のエビデンス所在** (codex コード追跡 2026-05-25 で確認):
- ペルソナ反映 = `snapshot_*.json` の `individuals[].genome.c_prompt.persona_set` (例 `["polya","triz"]`)、
  founder は `factor_affinity` が `c_factors`/genome[:10] に写像 (`persona_evolution.py:193/237`)。
- 交配 = `winners.jsonl` の `parent_ids` が 2 個 = 2 親交配 (`loop.py:262`)。1 個 = 変異。
- 系統 = `founder_lineage.jsonl` の `founder_counts` (起源は第1親継承, `persona_evolution.py:564`)。

## 2. 推奨ビューアと開き方 (形式別)

### 2.1 SVG — モダンブラウザ
```powershell
# Edge で明示的に開く (関連付けに依存しない・最も確実)
Start-Process msedge "D:\projects\llive\out\evo_seekvalue_2026_05_25\persona_dominance.svg"
Start-Process msedge "D:\projects\llive\out\evo_seekvalue_2026_05_25\evolution.svg"
# Chrome の場合
Start-Process chrome "D:\projects\llive\out\evo_seekvalue_2026_05_25\persona_dominance.svg"
```
SMIL アニメ (左→右の再生) はモダンブラウザで動く。IE でも表示は可だが非推奨。

### 2.2 Mermaid (`.mmd`) — VS Code か mermaid.live
```powershell
# VS Code で開く (Mermaid Preview 拡張があればプレビュー可)
code "D:\projects\llive\out\evo_seekvalue_2026_05_25\champion_lineage.mmd"
```
- **VS Code 拡張**: "Markdown Preview Mermaid Support" または "Mermaid Preview" を入れる。
- **mermaid.live**: <https://mermaid.live> に貼り付け。**`champion_lineage.mmd` (2KB) は可**、
  **`lineage.mmd` (227KB) は重すぎて不可** → `persona_dominance.svg` で代替する。

### 2.3 JSONL (進化を llove でライブ表示) — §4 で変換後に `llove tail`

## 3. OS 関連付けの確認と設定 (手順)

### 3.1 現状確認
```powershell
cmd /c "assoc .svg"    # 例: .svg=svgfile → さらに ftype svgfile で実体
cmd /c "assoc .mmd"    # 空欄 = 未関連付け (本環境はこれ)
cmd /c "assoc .html"
```
本環境の実測 (2026-05-25): `.svg` = Internet Explorer / `.mmd` = **未関連付け** / `.html` = ブラウザ。

### 3.2 関連付けを変える (任意・ユーザー実行推奨)
関連付けは OS 設定変更なので **手順を提示し、実行はユーザー判断** とする (可逆だが環境を変える)。

**GUI (推奨・安全)**: 設定 → アプリ → 既定のアプリ → ファイルの種類で既定を選ぶ
(`.svg` を Edge、`.mmd` を VS Code)。

**CLI (管理者権限・上級者向け)**:
```powershell
# 例: .svg を Edge に (HKCU なら管理者不要)
# GUI の方が安全。CLI は ftype/assoc がシステム全体に効くため注意。
```
> **注意**: `.mmd` を llove に関連付けるのは **非推奨** — llove は `.mmd` を表示できない (§5)。
> Mermaid は VS Code、SVG はブラウザに関連付けるのが正しい。

## 4. llove で進化ランを見る (変換 → tail)

`metrics.jsonl` は llove のイベントスキーマ (各行 `kind` 必須) でないため `llove tail` で
**何も流れない**。ブリッジで変換する:
```powershell
$env:PYTHONUTF8="1"
$d = "D:\projects\llive\out\evo_seekvalue_2026_05_25"
# 1) 変換: metrics.jsonl → llove_events.jsonl (kind=sensor/narration/spc_alarm)
py -3.11 D:\projects\fullsense\tools\evolution_to_llove.py $d
# 2) llove で時系列ライブ表示 (--no-follow で全 501 世代を一気に流す)
py -3.11 -m llove tail --no-follow "$d\llove_events.jsonl"
```
変換は best/mean/diversity を SENSOR、系統崩壊 (8→2) を **SPC_ALARM**、honest ラベルを
NARRATION で出す。`PYTHONUTF8=1` は llove の絵文字 cp932 クラッシュ回避に必須。

実装: `fullsense/tools/evolution_to_llove.py` (llive/llove 本体を改変しない疎結合ブリッジ)。

## 5. llove の現状と位置づけ (前提の正直な開示)

ユーザー要望「llove が表示できることが前提」に対する事実:
- **llove CLI のコマンド** = `demo / tail / export / export-svg / play / version` のみ
  (`llove/cli.py`)。docstring に `llove view` とあるが **未実装**。
- **llove は SVG/Mermaid ファイルのスタンドアロンビューアではない**。表示できるのは
  (a) JSONL イベントストリーム (`tail`)、(b) demo シナリオ、(c) HTML/SVG への **出力** (`export`)。
- したがって **進化の SVG/`.mmd` を llove で直接開くことは現状できない**。
  → SVG はブラウザ、Mermaid は VS Code が正しい閲覧ルート。llove で見るのは §4 の変換 JSONL。

**将来ロードマップ (llove 開発)**: `llove view <file>` を実装し、SVG/Mermaid/Markdown を
端末描画 (F15「ブラウザ並み表示」) できれば、`.svg`/`.mmd` を llove に関連付けて開ける。
現状は未実装のため本ガイドは推奨ビューア (ブラウザ/VS Code) を案内する。

## 6. 見極め結論 (この run から何が言えるか)

- **best=1.0 が gen0–500 平坦** (fitness 飽和) / **std 0.084→0.030** (中央収束) /
  **founder 系統 8→2** (furuse 52% / friston 48%, 6 founder 絶滅)。
- → **現構成 (rich-proxy + classic GA) では open-endedness (価値ある進化) は出ない**。
  best 飽和は SEL-2 (argmax 単峰禁止)、系統収束は OE-3 (monoculture 禁止) が反証すべき旧症状。
- **根本原因の一つ**: rich-proxy archetype が `factor_affinity` を 10×4 ブロードキャスト
  (全層同値) → 個体 c_factors も層方向同値 = SPARSE-1 違反、fitness が層を区別しない。
- **見込み = 条件付き YES**: 既存資産 (NoveltyScorer/MAPElitesGrid/nsga2/speciation/novelty_lane)
  が揃い、要件 §1 機構 (per-dim 標準化・novelty/QD 選択・ε-lexicase・minimal criterion) を
  配線すればこの飽和/収束は構造的に解ける。次の一手 = 実装着手ゲート §4 のコード側残作業。
