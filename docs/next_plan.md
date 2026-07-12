# next_plan (working memo)

> 最終更新: 2026-07-12 14:05 JST

> canonical handoff ではない。再開判断の正本は `docs/NEXT_SESSION.md`、approval / execution / push / rollback 来歴は `docs/HANDOFF_LEDGER.md`、auto snapshot は `docs/NEXT_SESSION.auto.md`。

## ✅ 2026-07-12 完了 — onocollo 記事 §9「次に載せられる候補」を live へ PATCH(独立検証済み・クローズ)

- **経緯**: ユーザーが過去セッションで指示した onocollo 上のロボ案5件(海底把持/蛇型救助/箸道具操作/双腕洗濯たたみ/GIF補強)を救出し memory `project_onocollo_robotics_ideation_2026_07_11` に保存 + Workflow 5-agent 評価で優先順位付け(箸4 > 海底3 ≈ GIF3 > 蛇型2 ≈ 双腕2)。§9 に「この土台の上に『次に載せられる』候補」小節(箸→海底→多節→双腕、構想である旨明示、cliffhanger)を追加。
- **前セッションが pending にした理由**: Bash/scratchpad の tool 出力汚染(spoof)申告で post 成否を検証不能だった。
- **本セッション(2026-07-12・正常環境)で完了**: (1)独立チャネル(WebFetch)で §9 が live 未反映を再確認 (2)決定的 probe token + git 状態照合で **Bash 出力は本セッションでは信頼可(spoof 再現せず)** と確認 (3)`preflight` = OK(auth/api/html 200・title/tags 一致・asset 19 全 200)を pre-PATCH fresh readback として実施 (4)ユーザー承認(「今 publish + 独立検証」+「公開してよいよ」)のもと `post --yes` = **`OK (200) [PUBLIC(一般公開)]`** (5)**WebFetch キャッシュ回避 URL(`?v=verify2`)で §9 小見出し + 4候補が live 反映・Last updated 2026-07-12 を独立検証**。
- **記録**: 承認・実行・検証は `docs/HANDOFF_LEDGER.md` の `2026-07-12 — onocollo §9 next-step candidates public PATCH (COMPLETED)` に記載。**git push は未実施(必要なら別 gate)**。この案件はクローズ。

## 2026-07-12 第3レビュー対応(独立再現完了・commit なし)

- **#2 件数決着**: full `tests/` = **301 passed**、私の 2 ファイル subset = 267。矛盾ではなくスコープ差。正本は 301。docs(ledger:142 / NEXT_SESSION:34)を訂正済み。
- **#5 訂正(gemini 前提が逆)**: `a01bf5c` は **origin/main に含まれ push 済み**(承認範囲 fig3/article commit の ancestor)。「unpushed」は誤り。ledger 訂正済み。
- **#3 修正 + 再現**: `is_publish_ready_draft` の nullish 誤検知(`id: null` 等が publish-ready)を再現 → nullish-aware へ修正(`qiita_public_post.py`/`qiita_team_post.py` と整合)。
- **#4 修正**: `TITLE_HITL` の DRAFTS 分岐が `id`/`qiita_item_id` を含みガイドと不一致 → ガイドどおり `public_id` のみへ揃えた(ガイドの「実装は id を混ぜない」主張を真にした)。
- **exit-1 リスク独立再現**: 106 .md は各 `project_group:` を追加、HEAD は欠落。非 DRAFTS public 記事は常に group 必須 → **code のみ checkout で GROUP_MISSING**。working tree(code+md)は preflight `warnings:0 exit 0` で整合。∴ リスクは partial commit のみ。
- full suite 追加修正後も **301 passed**(無回帰)。
- **#1 index 衛生**: 現 index は 4 ファイル mixed partial stage。commit するなら `git reset` → 明示 pathspec re-add → `git diff --cached` 目視が必須(ledger 記載)。
- 以上より安全な commit 単位は「7 code + 106 .md + index file 一括」か「無 commit」。code-only は exit-1 リスク確定のため非推奨。commit せず現状維持で最終 gate を提示。

## 2026-07-12 commit-scope gate 再提示(選択矛盾 + 依存性発見)

- 受領した選択が矛盾: 番号「1)」に対しテキストが「選択肢2 を承認し一気通しで live PATCH」= **完了済みの前 gate の文面**(stale boilerplate)。今回 gate のどの選択肢とも不一致。
- さらに **選択肢1(3 ファイルのみ commit)は技術的に不成立**と実確認: HEAD の `qiita_public_post.py` は `_qiita_title_guard` を import しないが working 版は line 39 で import。`_qiita_title_guard.py` は HEAD 非存在の新規(staged のみ)。3 ファイル限定 commit は import 先を欠く壊れた tree になる。
- 一方、working tree 全体は `267 passed` で整合。→ 安全な commit 単位は「7 code を一括」か「無 commit(現状維持)」。partial は reviewer #2 の警告どおり危険。
- `project_group` 必須 lint(scripts/qiita_preflight.py, working)と 106 .md の group 付与は reviewer #3 の相互依存。code だけ commit すると既存記事 preflight exit 1 の恐れ(未独立再現の risk)。
- よって監督モードで、実態に即した選択肢へ訂正して再 gate。憶測 commit はしない。

## 2026-07-12 第2レビュー対応(fail-closed 修正 + honesty 訂正)

- **🔴1 反映**: `cmd_preflight` の `--refresh-baseline`(`.remote` 書込副作用)が title guard より前にあり、BLOCKED ソースでも baseline が書き換わる fail-closed hole を修正。source-level title guard を refresh より前に置き、will-BLOCK ソースは baseline を触らない。回帰テスト追加。`_preflight_report` は fresh baseline を読む必要があるため refresh の後のまま(read-only 比較で副作用なし)。
- **🔴2/🔴3 は commit-scope の人間確認待ち**: 未 commit code/test は実態 **7 ファイル**(報告「3」は自分の編集分のみで過少申告 → ledger 訂正済み)。うち 4 code + 106 .md + `QIITA_PROJECT_GROUP_INDEX.md`(A)は**私が作成/レビューしていない先行 dirty**。`project_group` 必須 lint と記事側 group 付与の相互依存(code だけ commit すると既存記事が preflight exit 1 のリスク)は**未独立再現の risk として記録**。partial commit 未実施なので現時点の破綻はなし。→ commit 範囲は人間承認を要する(責任者指示 + 「作成していない物は surface」原則)。
- **🟡4 反映**: `test_qiita_preflight.py` の誤解を招くテスト名を実挙動へ改名 + docstring。
- **🟡5 反映**: preflight/post が同一 `_should_block_title_mismatch` 経路を通ることをコメント明記(public poster 経路)。
- テスト `267 passed`。
- **却下確認**: gemini「HANDOFF_LEDGER commit/push 済み推測」は実状態 `AM`(未 commit)で不成立、「a01bf5c 承認範囲超過」は前ターン承認済みの別案件で今回混入なし — いずれも一次確認で却下。

## ✅ 2026-07-12 完了: evolution loop public PATCH

選択肢2 を一気通しで実行完了。`a85434e`(draft のみ、pathspec 限定)push → `cbfc0f7..a85434e` → 事前 fresh readback `preflight: OK` → `post --yes` = `OK (200) [PUBLIC(一般公開)]` → live 確認(`updated_at:2026-07-12T13:20:52+09:00`、body 23314 chars、深掘りマーカー + fig3 画像を rendered_body で確認)。**evolution loop 案件はクローズ。** 残る派生タスク: (a) code 修正 3 ファイル(title guard / frontmatter escape / tests、`266 passed`)は未 commit の local 変更、(b) index の別案件 4 staged、(c) onocollo Team browser-side visibility 確認 pending。詳細は HANDOFF_LEDGER 参照。

## 現在地

- **evolution loop 記事の public PATCH は完了・クローズ**。`public_id 40ba7cc91ac577274b74` へ live PATCH 済み(`OK (200)`、`updated_at:2026-07-12T13:20:52+09:00`、body 23314 chars、fig3 画像 + 深掘り本文を rendered_body で確認)。fig3 asset `cbfc0f7`・article source `a85434e` は push 済み。**HEAD=`a85434e`、origin/main と同期(0 ahead)**。
- **唯一の未決事項は commit-scope gate**。3 レビューラウンド分の修正を反映したが **まだ 1 つも commit していない**。安全な commit 単位は「7 code + 106 .md + `QIITA_PROJECT_GROUP_INDEX.md` を一括」か「無 commit」の二択に収束。**code-only は checkout 時に既存 public 記事が preflight `GROUP_MISSING` exit-1 になるリスクが確定済み**のため除外。
- 未 commit code/test = **7 ファイル**(相互 import 依存): `scripts/qiita_preflight.py` / `tools/_frontmatter.py` / `tools/_qiita_title_guard.py`[AM] / `tools/qiita_public_post.py` / `tools/qiita_team_post.py` / `tests/test_qiita_frontmatter.py` / `tests/test_qiita_preflight.py`[AM]。加えて **106 の .md**(各 `project_group:` 追加)+ `docs/articles/QIITA_PROJECT_GROUP_INDEX.md`[A]。うち 4 code + 106 .md は**私が作成/レビューしていない先行 dirty**。
- index は 4 ファイル mixed partial stage。**素の `git commit` は importer 欠落で壊れる**ため、commit するなら `git reset` → 明示 pathspec re-add → `git diff --cached` 目視が必須。
- full suite = **`301 passed`**(私が触った修正込み・無回帰)。

## 直近の成果

- **evolution loop 記事**: 深掘り本文(4部品比較 / 審査員チェックリスト / `evaluate()`・logging・hold-out・rerank 骨格 / 30→100世代昇格条件 / runbook / FullSense 写像)+ fig3 差し替えを、fig3 asset push → source push → PATCH 前 fresh readback → `post --yes` → live 確認まで完遂。
- **3 レビューラウンド対応(code 修正・commit 前)**:
  - `tools/qiita_public_post.py`: `cmd_preflight`/`cmd_dry_run` に title guard を追加(post と整合)。`--refresh-baseline` の fail-closed 順序修正(title guard を `.remote` 書込より前へ)。
  - `tools/_frontmatter.py`: inline-list の double-quote 内 `\"` エスケープ実装(`["a\"b", x]` の `x` 脱落を修正)。
  - `scripts/qiita_preflight.py`: `is_publish_ready_draft` を nullish-aware に(`id: null` 等の `GROUP_MISSING` 誤検知を除去)。`TITLE_HITL` の DRAFTS 分岐を guide どおり `public_id` のみへ。
  - `tests/`: 回帰テスト追加(title guard preflight/dry-run、inline-list escape、fail-closed refresh、テスト名改名)。full `301 passed`。
- **honesty 訂正**: 未 commit は「3」ではなく **7 ファイル**。test 件数は full `301`(2 ファイル subset `267` はスコープ差)。`a01bf5c` は **push 済み**(gemini「unpushed」は逆)。すべて ledger/NEXT_SESSION へ反映済み。
- **exit-1 リスク独立再現**: 106 .md は `project_group` 追加・HEAD 欠落、非 DRAFTS 記事は常に group 必須 → code-only checkout で `GROUP_MISSING`。working tree(code+md)は preflight `warnings:0 exit 0` で整合 → リスクは partial commit のみ。

## 2026-07-12 決定(責任者統合指示 → 自律継続)

責任者の統合レビューにより、🔴1(live readback 実態化 + PATCH 前 readback を順序化)・🟠2(ledger の team_stock create 記述訂正)・🟠3(NEXT_SESSION 最優先二重化解消)を反映済み。**選択肢2(source push + PATCH の一気通し)は 🔴 未解消を理由に承認不可だったが、選択肢1(fig3 asset の 2 ファイルのみ commit/push → raw HTTP 200 確認まで)は 🔴 影響外として先行実行を許容された。** よって本 turn は選択肢1のみ実行する: `fig3_you_have_three.png/.svg` の 2 ファイルを explicit pathspec で commit(別案件 4 staged ファイルは巻き込まない)→ push → 本文参照 PNG(query 除去後)の raw 200 確認。選択肢2 は 🔴 解消後に改めて human gate へ提示する。

## 2026-07-12 read-only 再確認(fig3 push 後)

fig3 push 後に `preflight` を read-only で再実行 → `preflight: OK`(全出力は HANDOFF_LEDGER に記録済み: `auth/api/html_status:200` / `api_private:False` / title・tag 一致 / `asset_count:3` 全 `200 image/png`)。草稿の 479-insertion 差分は未 PATCH のまま = 選択肢2 の実行準備は整っている(※ただし後述 pending 項目を残したうえでの準備完了)。選択肢2(source push + 不可逆 live PATCH = 外部公開)は安全弁対象のため、human gate 未承認の間は実行しない。

## 2026-07-12 責任者統合指示 第2弾への対応(自律継続)

- **🔴1(反映)**: 選択肢2 の article source commit も明示 pathspec(`QIITA_evolution_loop_cooking_ja.md` 限定)+ `git diff --cached` 事前チェックを mandatory rule 化(HANDOFF_LEDGER 記載)。index には fig3 無関係の 4 staged が残るため `git add -A` / `git commit -a` 禁止。
- **🟠2(検証のうえ反映)**: `tools/qiita_public_post.py` の `cmd_preflight`/`cmd_dry_run` に title guard を追加し、`cmd_post` と整合(preflight OK が post 通過を保証)。回帰テスト 3 本追加。
- **🟠3(検証のうえ反映)**: `tools/_frontmatter.py parse_inline_list_value` の double-quote 内 `\"` エスケープを実装(`["a\"b", x]` が `x` を脱落する実バグを再現確認 → 修正)。追跡ファイルに実例なしのため hardening。回帰テスト 1 本追加。合計 `266 passed`。
- **🟠4(不採用・理由添付)**: frontmatter 終端後の leading blank line 保持は**意図的・テスト済みの byte-faithful 設計**(`test_shared_split_frontmatter_keeps_empty_frontmatter_and_body_newline` が `body == "\n# body\n"` を assert)。Qiita は先頭空行を無視し、baseline 比較も line-subsequence の寛容照合。剥がすと fidelity 低下 + 既存テスト破壊で実益なしのため、旧挙動復帰も差分正規化も行わない。
- **🟡5(反映)**: fig3 push 後の full preflight 出力(BLOCKED→OK の根拠)を HANDOFF_LEDGER に記録済み。raw 200 の言い換えではない旨も明記。PATCH 直前 fresh readback は別途必須。
- **🟡6(反映・pending 宣言)**: onocollo Team post の browser-side visibility 確認は**未完了(pending)**。本 evolution loop 案件の「push 準備完了」は onocollo とは別案件であり、onocollo visibility pending を残したうえでの準備完了である。両者を混同しない。

## 2026-07-12 決定: 選択肢2 承認 → 実行

人間が選択肢2(一気通し)を承認。統合指示 6 件(🔴1 / 🟠2 / 🟠3 反映、🟠4 不採用・理由添付、🟡5 / 🟡6 反映)対応済みで 🔴 ブロッカーは解消済み。実行順序は **`QIITA_evolution_loop_cooking_ja.md` を明示 pathspec で commit(別案件 4 staged + code 修正 3 ファイルは巻き込まない)→ push → PATCH 直前 fresh live readback(preflight 再実行で差分/可視性/タグ再確認)→ `40ba7cc91ac577274b74` へ PATCH(`post --yes`)→ API / live HTML で反映確認**。結果は HANDOFF_LEDGER へ記録する。

## 次の一手

> evolution loop 記事は完了済み。残るのは **commit-scope gate の決着だけ**。次セッションは以下をそのまま実行できる。

1. `docs/NEXT_SESSION.md` 冒頭と本ファイル `## 現在地` を読み、「未 commit 7 code + 106 .md、commit 単位は "全部一括" か "無 commit" の二択」という状態を把握する。
2. commit-scope を人間へ再提示する(⟦LLTERM_CHOICE⟧、行頭)。選択肢は **(A) 7 code + 106 .md + `QIITA_PROJECT_GROUP_INDEX.md` を一括 1 commit(push はしない)**、**(B) 無 commit で現状維持**。code-only は exit-1 リスク確定のため提示しない。
3. **(A) を選ばれた場合の手順**(この順で厳守):
   a. `git reset`(index を空に)→ `git status --short` で 4 ファイル partial stage が消えたことを確認。
   b. `git add -- scripts/qiita_preflight.py tools/_frontmatter.py tools/_qiita_title_guard.py tools/qiita_public_post.py tools/qiita_team_post.py tests/test_qiita_frontmatter.py tests/test_qiita_preflight.py docs/articles/QIITA_PROJECT_GROUP_INDEX.md` と、106 の記事 .md を明示 pathspec で add(`git add -- 'docs/articles/**/*.md'` など。ただし handoff docs `docs/NEXT_SESSION.md`/`docs/next_plan.md`/`docs/SESSION_SUMMARY.md`/`docs/HANDOFF_LEDGER.md` を含めるか別 commit にするかを分けて判断)。
   c. `git diff --cached --name-only` を目視し、意図した集合だけであることを確認。
   d. `py -3.11 -m pytest tests/ -q` が `301 passed`、`py -3.11 scripts/qiita_preflight.py --json` が `warnings:0 exit 0` を確認。
   e. 1 commit を作成(**push はしない**。push は別途 human gate)。
4. **(B) の場合**: commit せず、必要なら記事側 group 付与の追加点検や read-only 検証だけ進める。
5. 独立残タスク: onocollo Team item `f8017acc1f50112f3c9e` の browser-side visibility 確認(pending)。

## 環境メモ

- repo は `D:\\projects\\fullsense`、PowerShell、JST。HEAD=`a85434e`、origin/main と同期(0 ahead)。
- **push は行わない**。commit(選択肢A)は不可逆ではないが、非作成物 106 .md を含むため人間承認を要する。push は別 gate。
- **index が 4 ファイル mixed partial stage**。commit 前に必ず `git reset` → 明示 pathspec re-add。素の `git commit` / `git add -A` / `git commit -a` は importer 欠落 or 巻き込みで壊すため禁止。
- 7 code は相互 import 依存(posters + preflight → `_qiita_title_guard.py` / `_frontmatter.py`)。partial commit は broken tree になる。
- 106 .md は `project_group` を追加するもので、code の group 必須 lint と不可分。code だけ commit すると checkout 時に既存記事が `GROUP_MISSING` exit-1。
- `docs/SESSION_SUMMARY.md` は自動生成物で restart 正本ではない。再開は `docs/NEXT_SESSION.md`、実行来歴は `docs/HANDOFF_LEDGER.md`、実行前メモは本ファイル。
- test 件数の正本は full `tests/` = `301 passed`。2 ファイル subset の `267` はスコープ差(矛盾ではない)。
