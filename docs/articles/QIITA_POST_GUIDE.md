---
layout: default
title: "Qiita 投稿準備ガイド (2026-07-12 運用更新)"
nav_order: 95
---

# Qiita 投稿準備ガイド

> docs/articles/ 直下の `QIITA_#NN_*.md` を Qiita Web UI から投稿するための one-shot ガイド.
> 各記事の状態は `scripts/qiita_preflight.py` で随時確認可能.
> 既存 [`POST_CHEATSHEET.md`](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-18/POST_CHEATSHEET.md) (#18/#19 専用) を全 #14〜#24 系列に一般化したもの.

## 1. 現状サマリ (2026-07-12 CPU 整備後)

| カテゴリ | 件数 | 状態 |
|---|---|---|
| **通常 preflight** | metadata lint は clean | `py -3.11 scripts/qiita_preflight.py` で `GROUP-MISSING=0 / TAGS=0=0 / TITLE-LONG=0 / TITLE-MISMATCH=0 / REFS=0`。2026-07-12 時点では `TITLE_HITL=0` で、通常 preflight に残 warning は無い |
| **公開記事の group metadata** | 必須化済 | `docs/articles/QIITA_#*.md` は `project_group` 必須。補助文書 (`#24_LINK_MAP`) は除外 |
| **draft 側 group lint** | opt-in | `--include-drafts` では **publish control / publish identity frontmatter (`ignorePublish` / `private` / `public_private` / `id` / `qiita_public_id` / `public_id`) を持つ publish-ready draft** を group lint 対象にする。これらの draft は group metadata の既存有無にかかわらず `project_group` 必須で、欠落時は `GROUP_MISSING` を出す |
| **Jekyll-only frontmatter** | 1 件 | #20 は Jekyll 用 frontmatter を持つため、Qiita 投稿時は Qiita 用 frontmatter へ置換 |
| **本文サイズ** | 数 KB〜100KB 超 | 全件 Qiita 投稿可能範囲 (上限 1MB)。長文はそのまま許容 |

### 1.1 #20 (Jekyll frontmatter) の特別扱い

`QIITA_#20_one_session_full_stack_progress.md` は Jekyll 用 frontmatter
(`layout: default` / `parent: ...` / `nav_order: 1`) を持っている.
これは GitHub Pages 用なので、Qiita 投稿時には:

1. Jekyll frontmatter (`---...---`) を **削除**
2. 代わりに Qiita 用 frontmatter (title / tags / private / ignorePublish 等) を **追加**
3. 本文の `# 1 セッション...` H1 はそのまま残す (Qiita 上では body 内 H1 として表示)

または Jekyll fm を残したまま Qiita 投稿時にコピペ範囲を「6 行目以降」に限定する形でも可.

### 1.2 TAGS=TODO の解消

frontmatter skeleton 挿入時、記事末尾の `## 投稿時の推奨タグ` セクションが
無い記事には `TODO_TAG` プレースホルダを 2 個入れている. 投稿前に:

1. 記事内容に合うタグを 2 個選定 (例: `LLM`, `アルゴリズム`, `Python`, `自己進化`, `TRIZ` 等)
2. `tags:` の `- TODO_TAG` を該当タグに書換

例: `QIITA_#24_05_evolutionary_v0BCDE.md`

```yaml
tags:
  - FullSense
  - llive
  - 解説
  - TODO_TAG    # → 例: 進化アルゴリズム
  - TODO_TAG    # → 例: 派生集団進化
```

### 1.3 本文は「多ければ多いほど良い」(2026-05-22 ユーザー再強調)

本文文字数 (body) は **上限なし、多ければ多いほど良い**. [[feedback_qiita_long_form]] (2-3 万字級歓迎) からさらに昇格して、**30k / 50k / 100k 字級も全部 OK**. Qiita 投稿の技術的上限 (1MB) までは安心して詰め込んで良い.

理由:

- 連載 #14〜#24 の繋がりが本文ボリュームで補強される (相互参照が増えるほど SEO + retention 向上)
- ベンチ詳細 / 数式展開 / 失敗パターン / honest disclosure 内訳 / コード片 / 表 / 図 を **削らない**
- full 10x volume 版 (各 80-150k 字) は次セッション以降の予定 ([[QIITA_#24_00]] 既述)
- 「冗長なら削れ」は **タイトル限定**. 本文は密度 × リズム ([[feedback_reader_attention_curve]] 3 スケール 8 秒/90 秒/5 分) で長尺維持
- 雑談ポイント ([[feedback_article_break_points]]) も多めに挿入して読み手の集中力を維持しつつ、結果として総量を増やす方向

2026-07-12 時点では、public / draft を通じて **数 KB〜100KB 超**まで許容しており、本文サイズを理由に先に削る運用は取らない。実際に削るのは、Qiita 表示や読者導線を壊す冗長な重複だけに限る。

### 1.4 タイトル長運用

2026-07-12 時点の local 正本では `TITLE-LONG=0`。ただし運用としては引き続き:

- 80 字以内を推奨し、超過したら **末尾の飾り語から削る**
- 見出しの最初 2 語に **固有名 + 到達点** を前置する
- frontmatter だけでなく、**日本語 H1 と各言語 H1** の題名体系も揃える
- 実投稿タイトルの正本は **日本語 H1**。frontmatter `title:` は mirror として保持し、両者がズレると `[TITLE-MISMATCH]`
- ただし **`public_id:` を持つ公開接続済み記事・draft** のタイトル差分は human gate 必須
- `id:` / `qiita_public_id:` を持つ source の title 変更も外部公開物更新になりうるため、**`TITLE_HITL` の current scope 外でも別 manifest で human gate 対象**として扱う

Qiita は 80 字超でも投稿できるが、preflight では `[TITLE-LONG]` として警告する。

## 2. Project Group 単位でも束ねる

今後は `#NN` の連載番号に加えて、**project group 単位の導線**も並走させる。

- 番号連載の役割: 時系列で追う読者向けの主線
- project group の役割: 興味領域ごとに拾い読みする読者向けの再入場導線

現時点の canonical group 定義:

- `gaitlab`: 身体 / 物理 / 進化ロボット
- `spikelab`: 神経 / シナプス / 可塑性
- `onocollo`: 世界モデル / MuJoCo / 制御 toy
- `llcore`: LLM 本体 / 効率アーキ / holdout 検証
- `llive`: 記憶 / 自己進化 / ハーネス
- `llmesh`: ローカル/クラウド統一 / Prompt Firewall / 産業 IoT / P2P swarm

metadata の正本と置き場:

- **主 group / 関連 group の正本**: 各記事の frontmatter
- **group index の正本**: [QIITA_PROJECT_GROUP_INDEX.md](QIITA_PROJECT_GROUP_INDEX.md)
- **運用判断の正本**: この `QIITA_POST_GUIDE.md`

frontmatter の canonical field:

```yaml
project_group: onocollo
related_groups:
  - gaitlab
  - llcore
```

- `project_group`: 公開対象の `docs/articles/QIITA_#*.md` と、publish-ready draft では必須。主 group を 1 つだけ置く
- `related_groups`: 任意。強い関連がある group だけを列挙する
- 値はこの節の canonical group 名だけを使い、別名を増やさない
- 将来記事でも、**公開対象の `docs/articles/QIITA_#*.md` は `project_group` 必須**とする
- 非 publish-ready draft では `project_group` は任意とし、棚卸し対象のまま残してよい。
- **cross-cutting essay / private-only memo** で既存 group (`gaitlab / spikelab / onocollo / llcore / llive / llmesh`) に無理なく収まらない場合は、taxonomy 追加判断まで `GROUP_MISSING` のまま保留してよい。ただし 2026-07-12 時点では、以前 unresolved だった `QIITA_token_economy_*` と `QIITA_wait_essay_ja.md` は **暫定運用分類**として `llmesh` の「ローカル/クラウド運用・周辺工学」側へ寄せて backfill 済みである。将来 taxonomy を増やす場合はこの 5 本を再判定する。

記事本文での導線配置:

- **冒頭**: 置かない。導入の密度を優先する
- **末尾**: `同じ project group の関連記事` を置く
- **複数 group に跨る記事**: 主 group を先、関連 group は 1 行で補助

Qiita タグと project group の役割分担:

- **Qiita タグ**: 外部 discoverability 用。一般読者向けの検索語
- **project group**: repo / 連載内 IA 用。同じプロジェクト線の束ね直し
- したがって、`project group` 名をそのまま Qiita tag へ流用する義務はない

group index の更新方法:

- 当面は **手動更新**
- 投稿 / major rewrite / group 変更時に、その記事の行を index へ追記・修正
- 将来、自動生成に寄せる場合は frontmatter 走査スクリプトの追加対象とする
- **index の掲載範囲**: `docs/articles/QIITA_#*.md` のうち `project_group` を持つ記事を全件載せる。したがって **companion / かみくだき版も含む**。`drafts/` 配下は別枠で、主記事や関連導線のアンカーとして使うものだけを明示的に載せる

運用ルール:

1. 各記事に **主 group を 1 つ**決める
2. 関連が強い記事だけ **関連 group を追加**する
3. 既存の `#NN` を捨てず、**group index を別ページで持つ**
4. 記事本文の**末尾**から、`同じ group の関連記事` へ飛べるようにする
5. canonical な group 定義はこの節からコピペし、別表現を増やさない

記事末尾導線の最小テンプレート:

`docs/articles/` 直下の公開記事用:

```markdown
## 同じ project group の関連記事

- 主 group `onocollo`: 現時点ではこの article が唯一の主記事。追加されたら同じ主 group の記事だけを並べる
- 関連 group `gaitlab`: [Project Group Index](QIITA_PROJECT_GROUP_INDEX.md), [Qiita #48 GPU wait CPU roundup](drafts/QIITA_%2348_gpu_wait_cpu_roundup_ja.md)
```

`docs/articles/drafts/` 配下の草稿用:

```markdown
## 同じ project group の関連記事

- 主 group `onocollo`: 現時点ではこの article が唯一の主記事。追加されたら同じ主 group の記事だけを並べる
- 関連 group `gaitlab`: [Project Group Index](../QIITA_PROJECT_GROUP_INDEX.md), [Qiita #48 GPU wait CPU roundup](QIITA_%2348_gpu_wait_cpu_roundup_ja.md)
```

group index の 1 行フォーマット:

```markdown
| `onocollo` | 世界モデル / MuJoCo / 制御 toy | [Qiita onocollo worldmodel alife](drafts/QIITA_onocollo_worldmodel_alife_ja.md) (主 group) |
```

frontmatter と preflight の注意:

- `project_group` / `related_groups` は **追加 frontmatter key** として扱う
- 通常の `py -3.11 scripts/qiita_preflight.py` でも、公開対象 `docs/articles/QIITA_#*.md` では `project_group` 必須を検査する
- ただし `QIITA_#24_LINK_MAP.md` のような **補助文書**は group 必須チェックから除外する
- `py -3.11 scripts/qiita_preflight.py --include-drafts` を使うと、`docs/articles/drafts/QIITA*.md` まで走査対象を広げられる
- `--include-drafts` の group lint は **`ignorePublish` / `private` / `public_private` / `id` / `qiita_public_id` / `public_id` のいずれかを持つ publish-ready draft** を対象にする。これらの draft は group metadata の既存有無にかかわらず `[GROUP-MISSING]` の対象であり、legacy draft 群へ一律 `[GROUP-MISSING]` を出すわけではない。non publish-ready draft は group 任意で、lint 対象外とする
- group lint では `project_group` / `related_groups` の canonical 名 typo、`related_groups` 内の自己重複、`project_group` の `related_groups` 混入も検査する
- frontmatter に `title:` が無い草稿は本文先頭 H1 を title fallback として使うため、`--include-drafts` の warning 件数は従来から変わりうる
- draft を publish-ready の正本へ昇格させた段階では、通常の preflight (`docs/articles/QIITA_#*.md`) 側でも再確認する
- 2026-07-12 時点の実測では `--include-drafts` は **legacy anthology / essay / multilingual archive** を多く含み、`warnings: 14`。breakdown は **`TITLE_HITL=14`** のみで、これは `public_id` を持つ draft 総集編の title shortener 差分が **human gate 待ち**に移った結果である。以前残っていた `GROUP_MISSING=5` (`QIITA_token_economy_{ja,en,ko,zh}` と `QIITA_wait_essay_ja.md`) は、**暫定運用分類**として `llmesh` の「ローカル/クラウド運用・周辺工学」側へ寄せて backfill して解消済みである。加えて、ここで以前出ていた `NO_FM=2` と `TAGS_EMPTY=21`、および draft 側の `TITLE_LONG=15` は、`#46/#47` の frontmatter 正規化、legacy parser hardening、総集編 draft title の圧縮で解消済みである。parser hardening には **unquoted title の inline comment 除去、single-quoted scalar / inline list item の `'' -> '` 復元、`related_groups` の list 解釈統一、fenced code block 内 `#` の H1 誤検出回避**も含む。このモードは「草稿棚卸し」であり、通常 preflight のように **warnings 0 を合格条件にしない**
- **`public_id` を持つ記事**で、branch baseline から未反映の publish title 差分 (`title:` または日本語 H1 の変更) がある場合は、preflight 上も `[TITLE-HITL]` を出して **human gate 必須**とする。current 実装では `id` / `qiita_public_id` だけを持つ mirror / Team 系記事は `TITLE_HITL` 件数へ混ぜない。summary の `Warning breakdown:` にも件数が出るので、manifest 作成前に対象件数を機械的に拾える。2026-07-12 の current local diff では `TITLE_HITL=0` である
- したがって、**`TITLE_HITL=14` は draft `public_id` 群だけの件数**であり、current diff に混在する `id` / `qiita_public_id` source の title 変更件数を代表しない。後者は別 review / 別 gate で扱う
- さらに `Warning breakdown JSON:` と `Warning files JSON:` で **warning 種別ごとの件数 / 対象ファイル一覧**も出る。`TITLE_HITL` の human-gate manifest は、まずこの JSON を一次一覧として使う
- `git` を使う `TITLE_HITL` / baseline 判定は、すべて **`cwd=REPO_ROOT` 固定**で実行する。repo 外ディレクトリから `py -3.11 scripts/qiita_preflight.py --json` を叩いても、manifest が false negative で消えない前提にする

## 3. 投稿順序 (推奨)

連載番号の時系列順に投稿:

```
#14 (Annotation Channel)
  → #15 (Second Brain)
  → #16 (Three-Self Spirit)
  → #17 (Human-AI Fusion Vision)
  → #18 (Non-Transformer Low-Spec PC)
  → #19 (GPU-Less AI for Everyone)
  → #20 (One Session Full Stack)
  → #21 (Three-Day Marathon)
  → #22 (Transformer Escape Status)
  → #23 (15h Marathon Mid Report)
  → #24-00 (Tech Series Index)
  → #24-01 (Memory Layer)
  → #24-02 (Thought Factors × COG-MESH)
  → #24-03 (Structural Evolution × TRIZ)
  → #24-04 (B-Series Convergence)
  → #24-05 (Evolutionary v0.B/C/D/E) ★ 連載中核
  → #24-06 (Non-Transformer LLM Backend)
  → #24-07 (Observability + Governance)
  → #24-08 (lleval — Eval Framework)
```

#24-00 の index 投稿後に #24-01〜08 を投稿すると、index が naturally に他の連載へリンクできる.

## 4. 各記事の投稿手順 (共通)

1. <https://qiita.com/drafts/new> を開く
2. **タイトル**: 本文側の **日本語 H1** を正本としてコピペ
   - frontmatter に `title:` がある場合は、**`title:` と日本語 H1 を一致**させる
   - `scripts/qiita_preflight.py` は、`title:` と日本語 H1 が食い違うと `[TITLE-MISMATCH]` で fail する
   - `tools/qiita_public_post.py` と `tools/qiita_team_post.py` も同じ規約で、**payload title は日本語 H1 を優先し、frontmatter `title:` は mirror** として扱う
   - mirror がずれたまま投稿しないよう、poster は **frontmatter `title:` と publish H1 が不一致なら BLOCK** する
   - ただし **publish-connected な既存 source が baseline 時点ですでに mismatch を持ち、今回 publish title 自体は変えていない**場合は、その legacy mismatch だけを理由に更新不能にはしない
   - 自動 publish 系の都合で frontmatter `title:` も残すが、**実投稿タイトルとして扱うのは日本語 H1** とする
3. **本文**: frontmatter を除いた本文全体をコピペ
   - **日本語 H1 も本文に残す**。Qiita の title 欄と body 内 H1 が重複して見えても、この repo では source と mirror の一致を優先する
   - frontmatter (`---\n...\n---\n`) だけ除外
   - 末尾の `## 投稿時の推奨タグ` セクションは Qiita 上では非表示にしたい場合は除外
4. **タグ**: 5 個まで (frontmatter に `tags:` があればそれを参照、なければ記事末尾の §投稿時の推奨タグ から)
5. **公開設定**:
   - 最初は **「限定共有投稿」** で投稿 → プレビューで表示確認
   - 問題なければ **「全体公開」** に切替
6. **ライセンス**: CC BY (Qiita default)
7. **コメント許可**: ON

### PowerShell で本文 + タイトルをクリップボードに

```powershell
$file = "docs/articles/QIITA_#24_05_evolutionary_v0BCDE.md"
# タイトル (日本語 H1 を正本として抽出)
$lines = Get-Content $file
$jp = ($lines | Select-String -Pattern '^# 日本語$').LineNumber
$title = if ($jp) {
  ($lines | Select-Object -Skip $jp | Select-String -Pattern '^# ' | Select-Object -First 1).Line -replace '^# ',''
} else {
  ($lines | Select-String -Pattern '^# ' | Select-Object -First 1).Line -replace '^# ',''
}
$title | Set-Clipboard
Write-Host "Title copied: $title"
# 本文 (frontmatter を除いた全体。日本語 H1 は残す)
$bodyStart = if ($lines[0] -eq '---') {
  ((0..($lines.Count - 1) | Where-Object { $lines[$_] -eq '---' })[1] + 1)
} else {
  0
}
$body = ($lines | Select-Object -Skip $bodyStart) -join "`n"
$body | Set-Clipboard
Write-Host "Body copied: $($body.Length) chars"
```

## 5. 投稿後の cross-link 確定運用

各記事内に `[`QIITA_24_XX_*` (内部参照)]` 形式の cross-link が残っている. 投稿後に確定する Qiita 個別 URL (`https://qiita.com/furuse-kazufumi/items/<hash>`) に **一括置換** が必要.

### 5.1 URL 確定の蓄積場所

[`QIITA_#24_LINK_MAP.md`](QIITA_%2324_LINK_MAP.md) に投稿後 URL を表で集約:

```markdown
| 連載 # | ローカル fname | Qiita URL |
|---|---|---|
| #24-00 | QIITA_#24_00_llive_tech_series_index.md | https://qiita.com/furuse-kazufumi/items/<hash00> |
| #24-01 | QIITA_#24_01_memory_layer.md | https://qiita.com/furuse-kazufumi/items/<hash01> |
| ... | ... | ... |
```

### 5.2 一括置換スクリプト (TODO)

`scripts/qiita_url_sync.py` (未実装) — LINK_MAP の表を読み込み、各記事内の cross-link を確定 URL に置換予定. 次セッション以降で実装.

## 6. preflight チェック

投稿前に必ず実行:

```powershell
py -3.11 scripts/qiita_preflight.py
```

draft を含めて確認したいとき:

```powershell
py -3.11 scripts/qiita_preflight.py --include-drafts
```

各記事ごとに表示される項目:

- **pub**: ignorePublish の状態 (TRUE = まだ非公開, false = 公開準備, NO-FM = frontmatter なし)
- **priv**: private (Qiita 限定公開フラグ)
- **tag**: タグ数 (5 個まで推奨)
- **title**: タイトル文字数 (80 字以内推奨)
- **body**: 本文文字数
- **refs**: 未解決の内部参照数 (`QIITA_#NN_*` (内部参照) 形式が残っている数)

警告: `[GROUP-MISSING]` `[TAGS=0]` `[TITLE-LONG]` `[TITLE-MISMATCH]` `[REFS=N]` は投稿前に解消推奨。`[TITLE-HITL]` は **`public_id` を持つ公開接続済み記事 / draft の実タイトル差分**なので、解消ではなく human gate 対象として扱う。current 実装では `id` / `qiita_public_id` だけを持つ mirror / Team 系記事はここへ含めない。exit code 1 は「lint 不整合」だけでなく、この gate signal が残っている場合にも返る。なお **Qiita の 5-tag 上限そのもの**のように、現行 preflight が warning 化していない運用条件は別途このガイドで確認する。

`project_group` は、公開対象の `docs/articles/QIITA_#*.md` では **必須**である。canonical 値は `gaitlab / spikelab / onocollo / llcore / llive / llmesh` に固定し、欠落時は `[GROUP-MISSING]`、許容値外は `[GROUP=...]` / `[RELATED=...]` として検出される。`Warning breakdown JSON:` / `Warning files JSON:` はこの group 系 warning についても同じ key で機械回収できる。なお **`llove` は product family 名ではあるが、2026-07-12 時点の Qiita 記事 taxonomy では独立 group にしていない**。現状の記事は `llive` / `llmesh` / `llcore` など既存 group に収まり、group 値を増やすと index / handoff / backfill の運用コストだけ先に増えるため、意図的に除外している。

### 6.1 `TITLE_HITL` manifest を PowerShell で取り出す

最優先の推奨経路は `--json` である。decorated な標準出力行を `Where-Object` で拾うより、**単一 JSON オブジェクト**をそのまま parse したほうが壊れにくい。`git` ベースの `TITLE_HITL` 判定も `cwd=REPO_ROOT` 固定で、**branch baseline との差分**を見るので、repo 外から叩いても同じ結果になる。

```powershell
$json = py -3.11 scripts/qiita_preflight.py --json | ConvertFrom-Json
$hitl = @()
if ($json.files.PSObject.Properties.Name -contains 'TITLE_HITL') {
  $hitl = @($json.files.TITLE_HITL)
}
$hitl
```

`$json.files` に `TITLE_HITL` key が無いのは **`TITLE_HITL=0` の正常系**として扱う。

### 6.2 旧テキスト出力から `TITLE_HITL` manifest を取り出す

互換性のため `Warning files JSON:` 行も残しているが、これは fallback 扱いにする。

```powershell
$out = py -3.11 scripts/qiita_preflight.py 2>&1
$line = $out | Where-Object { $_ -like 'Warning files JSON:*' } | Select-Object -First 1
if (-not $line) {
  throw "Warning files JSON line not found"
}
$json = ($line -replace '^Warning files JSON:\s*','') | ConvertFrom-Json
$hitl = @()
if ($json.PSObject.Properties.Name -contains 'TITLE_HITL') {
  $hitl = @($json.TITLE_HITL)
}
$hitl
```

この一覧を **human gate 向け manifest の一次ソース**に使う。`Warning files JSON:` 自体が無いのは取得失敗、`TITLE_HITL` key が無いのは **`TITLE_HITL=0` の正常系**として扱う。固定のファイル一覧をガイドや `next_plan` に手書きで埋めず、毎回この JSON から取り直す。

## 7. ハッシュタグ運用

Qiita タグ (5 個) と LinkedIn/Twitter ハッシュタグは別運用:

| 媒体 | タグ数 | 例 |
|---|---|---|
| Qiita | 5 個 | `LLM` `ローカルLLM` `Mamba` `RWKV` `Python` |
| LinkedIn | 5-11 個 | `#FullSense #llive #HarnessVibeCoding ...` |
| Twitter/X | 1-2 個 | `#FullSense` のみ |

## 8. 投稿フロー全体 (連載 #24 中心)

```
[投稿前]
  1. scripts/qiita_preflight.py で全件警告チェック
  2. frontmatter 欠落や legacy scalar 記法が残っていれば補完 / 正規化 (タグ / title / private 等)
  3. `project_group` / `related_groups` と group index の追随を確認
  4. 公開前に `.md` 相対リンク / `%23` を含むローカル向け導線が残っていれば、Qiita URL / GitHub 公開 URL / raw URL へ置換
  5. 内部参照が残っていれば解消

[公開済み記事の追加 gate]
  1. **`public_id:` を持つ記事**で **タイトル差分** (`title:` / 日本語 H1 の変更) がある場合、通常 publish / PATCH に混ぜない
  2. その差分を出す場合は **human gate 必須**。対象記事、commit 範囲、title 変更の意図を manifest 化して承認を取る
  3. 承認が無い限り、公開済み記事のタイトル差分は publish 禁止
  4. 補助文書 (`QIITA_#24_LINK_MAP.md` など) は Qiita 投稿タイトル同期の対象外として扱う

[投稿]
  1. #14 から時系列で投稿 (上記 §3)
  2. 各記事は「限定共有」→ プレビュー → 「全体公開」の 2 段階
  3. 投稿後すぐに [QIITA_#24_LINK_MAP.md] に URL を記録

[投稿後]
  1. LINK_MAP 更新
  2. 連載 #24-00 (index) の cross-link を確定 URL に置換 (手動 or scripts/qiita_url_sync.py)
  3. LinkedIn 投稿 (LinkedIn_2026-05-22_harness_vibe_session.md) の deep link を Qiita URL に差替
  4. README に連載 index を追加
```

## 9. 関連

- [`scripts/qiita_preflight.py`](https://github.com/furuse-kazufumi/fullsense/blob/main/scripts/qiita_preflight.py) — 投稿前検査
- [`scripts/qiita_url_sync.py`](https://github.com/furuse-kazufumi/fullsense/blob/main/scripts/qiita_url_sync.py) — 投稿後 URL 一括置換 (TODO)
- [`QIITA_#24_LINK_MAP.md`](QIITA_%2324_LINK_MAP.md) — 投稿後 URL 集約
- [`2026-05-18/POST_CHEATSHEET.md`](2026-05-18/POST_CHEATSHEET.md) — #18/#19 個別 cheat-sheet (本ガイドの前身)
- 連載 index: [`QIITA_#24_00_llive_tech_series_index.md`](QIITA_%2324_00_llive_tech_series_index.md)

---

## 10. 画像 / アニメーション SVG の Qiita 表示ルール (必読・2026-05-31 確立)

Qiita で画像 (特に animated SVG) が「見えない」事故が #24/#26 で再発。**恒久ルール**:

1. **静的状態が見える SVG にする (家訓)**。Qiita の `<img>` は外部 SVG を表示するが **SMIL を実行しない** → `width="0"`/`opacity="0"` で初期状態を隠し SMIL で reveal する設計は **空白表示**になる。authored 値を最終(可視)値にし `<animate from="0" to="FULL" fill="freeze">` で enhancement にする。
2. **画像 URL は raw.githubusercontent 絶対 URL** + **ファイルは origin/main に push 済が前提** (push 前/パス違いは 404=非表示)。**アセットを移動・整理したら公開済記事の URL も必ず追従**させる (直下↔サブフォルダの不一致が #26 非表示の真因)。
3. **Qiita は外部画像をプロキシ・キャッシュする**。一度 404 をキャッシュすると非表示が続く (移動前にキャッシュ済の古い記事は表示され続けるので「一部だけ見えない」と誤認しやすい)。**URL に `?v=N` cache-bust を付けて再 publish** すると Qiita が再取得する。
4. **判定は git でなく実 HTTP** (`Invoke-WebRequest -Head <raw URL>` で 200/404) **+ Qiita 実機プレビュー**。GitHub/ローカルで見えても当てにならない。
5. **PNG 化は最終手段** (アニメ喪失)。基本は animated SVG を上記 1-4 で見せる (ユーザー方針 2026-05-31)。
6. **Qiita CLI**: hash-ID 名 (`<id>.md`) = 公開実体 (`.remote/` 同期)。custom 名は未公開草稿で **publish すると重複記事**になる。private 可否は `.remote/<id>.md` の frontmatter `private:` で確認。
7. **motion_pack の位置づけ**: `docs/articles/assets/motion_pack/*.svg` は **静止でも意味が通る補助素材**。Qiita 上では animated SVG が静止前提なので、**動きそのものを主メッセージにしたい場合は GIF / 動画へ変換して使い、SVG は fallback / 補助図として扱う**。

## 11. `public/` と `public/.remote/` の扱い

- `tools/qiita-cli-poc/public/<id>.md`: ローカル側の publish 入力 / mirror。review・差分確認・手修正の主対象。
- `tools/qiita-cli-poc/public/.remote/<id>.md`: Qiita live から取得した **参照スナップショット**。live 比較や private 状態確認には使うが、これを手で直しても **Qiita live は更新されない**。
- `scripts/qiita_preflight.py` の通常走査範囲は `docs/articles/` 側の source であり、`public/.remote/` は **honest 化完了の根拠には使わない**。`.remote/` まで見たいときは別途 diff / `rg` / poster 実行前確認で見る。
- live 本文を直す正規フローは、source / mirror を修正したうえで **poster か PATCH** を通すこと。外部公開更新なので human gate 必須。
- したがって、`public/` と `public/.remote/` の取り違えを避けるため、review では **「source を直したか」「mirror を直したか」「live 更新を実行したか」** を分けて書く。

詳細: raptor memory `feedback_qiita_svg_path_and_cache` / `feedback_animated_svg_static_fallback`。
