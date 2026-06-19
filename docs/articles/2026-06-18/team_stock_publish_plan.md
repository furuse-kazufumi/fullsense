# Team Stock Publish Plan (2026-06-18)

`tools/qiita-cli-poc/public/` に切った Team stock 用 source-only draft を、
後で Qiita Team `fullsense` へ流すときの順番と注意点をまとめる。

## この文書の役割

- **正本**: 公開順・human gate 条件・rollback 注意をここに集約する
- `team_stock_queue.md`: 投稿待ち一覧と実行記録の正本。canonical field は **POST 後の記録欄 `visible range memo` / `rollback needed` / `note`**
- `next_plan.md` / `SESSION_SUMMARY.md`: `team_stock_queue.md` の **POST 後の記録欄 `note`** を参照するだけに留める

## なぜこの 3 本か

- **Semantic Governance**
  - #43 の中でも、`security face` は記事本文だとどうしても圧縮される
  - Team 向けには `権限管理` と `意味管理` の差だけで 1 本立つ
- **LLM Wiki / thought circulation**
  - #43 の中核だが、一般公開版では `LLM Wiki` と `anti-circulation` を十分に掘り切れない
  - Team 内の設計共有としては、実装前段の危険源整理に価値がある
- **ctx 2549% postmortem**
  - #46 本編は 9 原則が主で、個別障害としての切り分けログは圧縮されている
  - Team 向けには incident postmortem 単体のほうが再利用しやすい

## 推奨順

1. `team_stock_semantic_governance.md`
2. `team_stock_llm_wiki_anti_circulation.md`
3. `team_stock_ctx2549_postmortem.md`

理由:

- まず #43 の「概念と設計原則」側を先に Team に置く
- 次に `LLM Wiki` の設計難所を補う
- 最後に #46 の incident postmortem を置く

こうすると、読む側が

`安全な loop/harness の考え方` → `知識基盤の落とし穴` → `具体 incident の切り分け`

の順で辿れる。

## human gate 前提の注意

1. `ignorePublish` は公式 qiita-cli 側の草稿ガードだが、2026-06-19 時点の `tools/qiita_team_post.py` もこれを読み、`--force-ignore-publish` 無しでは fail-closed で停止する
2. つまり Team poster で `post --yes` を通すには、`ignorePublish: true` の source に対して **human-gate 後の `--force-ignore-publish`** が別途必要である
3. `private: true` の Team 上での実効可視範囲は未確定
4. 2026-06-19 以降の Team create は、`group_url_name` 未指定の implicit share target を避けるため **explicit `group_url_name` 必須**へ fail-closed 化した
4. よって、実 POST 前に user GO が必要

## POST 前に確認すること

- user GO があること
- `private: true` の可視範囲が未確定なまま送ることを user が理解していること
- rollback 経路を確認してあること
  - POST 後に取り消すなら、少なくとも item `id` を控えた上で Team UI または API で body / title を即時差し替えできることを確認する
  - `private` flip は Qiita Team API docs 上で確認できていないため、rollback の主経路として前提にしない
- 承認者は current user 本人、承認基準は「可視範囲未確定のままでも Team stock を優先するか」である

## preflight runbook

1. `py -3.11 tools/qiita_team_post.py verify` を実行し、トークン疎通と team 名を確認する
2. `py -3.11 tools/qiita_team_post.py dry-run <file>` を再実行して title / tags / body 形式を確認する
3. frontmatter の `private: true` / `ignorePublish: true` を見直し、`ignorePublish: true` の source を送る時は `--force-ignore-publish` が必要だと再確認する
4. POST 後に記録する `id` / `URL` / `visible range` の記入先が `team_stock_queue.md` にあることを確認する
5. rollback 手段が Team UI か API のどちらで取れるかを先に決める
6. `private` flip を rollback として使わずに済むか、必要なら Team UI での即時差し替え手順を先に確認する
7. `--patch-group-url-name` を使う remediation 案に進むなら、**先に human が concrete な `group_url_name` を決める**。2026-06-19 時点の local draft 3 本にはこの field が入っていないため、そのままの dry-run / post は fail-closed で `PATCH_GROUP_URL_NAME_BLOCK` になる
8. 実行順は **containment first / diagnosis second / opt-in PATCH last** を原則にする。ただし **diagnosis gate** と **temporary tightening gate** は別の human-gate として扱い、`暫定 private 化 → 再診断` を 1 回の選択で束ねない。temporary tightening 後の after-state は root-cause 判定ではなく **containment 完了確認**として読む
9. **diagnosis 完了**の定義は、対象 3 本それぞれについて **5 ソース** `(a) Team UI 上で確認できた share target / private state` `(b) Team API GET で返る `group.url_name` / `private` / `organization_url_name`` `(c) 未認証 HTML GET の観測結果` `(d) public direct probe の観測結果` `(e) source frontmatter の `private` / `group_url_name`（intended state ラベル）` を同じターンで並べ、**share target 起因 / private state 起因 / slug or URL drift / draft or deleted / org membership or token failure / 未確定** を 1 行で判定できる状態にすることとする。ここで `(b)(c)(d)` は **3 種再取得ソース**、5 ソース突合はその後段の判定ステップとして区別する
10. 上記 9 を満たすまでは、opt-in PATCH は「実行候補」ではなく **診断後の従属候補**としてのみ扱う。temporary tightening が必要でも、先に diagnosis gate で before-state を固め、その次の human-gate で実行する
11. 診断の第 1 工程は **token validity / Team 権限健全性チェック**とする。`401 / 403` をそのまま可視性判定へ混ぜず、token 期限切れ・権限喪失・認証失敗を 먼저切り分ける
12. 判定基準は project-local rule として暫定固定する。`share target 起因` は Team UI / API / intended state の `private` 意図が揃っているのに、share target だけが intended target から外れている場合。`private state 起因` は share target が intended target と揃っているのに、Team UI / API の `private` 系だけが intended state から外れている場合。`slug or URL drift` / `draft or deleted` / `org membership or token failure` は該当ソースの異常系が独立に確認できた場合に分ける。frontmatter は **intended state** のラベルであり、実露出の証拠としては数えない
13. 5 ソースが矛盾したときの裁定順も **我々のローカル運用ルール**として暫定固定する。優先順位は `未認証 HTML GET / public direct probe の外形的事実` > `Team UI 表示` > `Team API GET` > `source frontmatter` とする。ここでいう `positive` は、**実 Team 記事 URL** に対する未認証 HTML GET または public direct probe が `200` かつ対象記事の title / 本文断片を content fingerprint として読める場合に限る。`302 / 403 / 404` や空本文は **negative ではなく未確定** として扱い、安全証明に使わない。public 面しか叩けない probe は **無情報** と明記して判定材料から外す
14. `未確定` は catch-all の保留ではなく、**default で fail-closed 候補**に送る。no-op retain は例外扱いで、同じ理由での no-op retain は 1 回まで、かつ retain 期限は **次回 human-gate まで**に留める。2 回目に入る前に **暫定 private 化**の human-gate を必ず出す
15. intended state は option 選択前に **記事ごと**に固定する。baseline は source frontmatter の `private` / `group_url_name` と、人間が意図した公開範囲メモの組で残す。frontmatter は baseline 根拠に使うが、**実露出の照合源ではない**
16. diagnosis 結果ごとの最終処置も記事ごとに分ける。`share target 起因` は Team UI remediation または opt-in PATCH 候補、`private state 起因` は Team UI での tightening 候補、`slug or URL drift` / `draft or deleted` / `org membership or token failure` は復旧担当へエスカレーション、`未確定` は default で temporary tightening 候補とし、解除は intended state と before/after evidence が揃ってから別 gate で判断する

## execution commands

- create:
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_semantic_governance.md --yes --force-ignore-publish`
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_llm_wiki_anti_circulation.md --yes --force-ignore-publish`
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_ctx2549_postmortem.md --yes --force-ignore-publish`
- verify:
  - Team API / UI で title, private 状態, URL を確認する
  - `team_stock_queue.md` に `id` / URL / visible range を転記する
- Team UI remediation checklist (human-gate 後のみ):
  - この checklist は Team UI の read-only diagnosis と remediation の両方に適用する。変更を入れない read-only turn でも、5 ソースの before snapshot は同じ粒度で取る
  - probe 実行前に対象を固定する: `GET https://fullsense.qiita.com/api/v2/items/<id>`、`GET https://fullsense.qiita.com/furuse-kazufumi/items/<id>`、`GET https://qiita.com/furuse-kazufumi/items/<id>`。静的 mirror の cache-bust は `?v=<ts>` を併用してよいが、**API / 認証エンドポイントでは query cache-bust を過信せず実レスポンス本文と取得時刻を残す**
  - Team 面 URL に打てていることを先に確認する。public 面しか叩けない probe は `無情報` とラベルし、可視性判定の根拠には使わない
  - **変更前**に token validity を確認し、Team UI と Team API GET の両方で、対象 3 本の `title` / `private` / `group.url_name` / `organization_url_name` を控える
  - **変更前**に同じターンで未認証 HTML GET / direct probe / source frontmatter (`private` / `group_url_name`) も控え、`記事ID / 取得時刻 / HTTP status / 認証有無 / share target` を固定列として 5 ソースを 3 本ぶん横並びにする
  - human が intended share target と intended private state を 3 本それぞれで明示してから UI を触る
  - Team UI 上で `private` 変更が実際に可視範囲 tightening として効くかを、その turn の before/after evidence で一次確認する。効力未確認のまま PATCH 経路へ飛ばない
  - remediation 中は delete を使わず、まず UI 上で share target / private state / body 差し替えのどれが可能かを切り分ける
  - `body 差し替え` を行った場合は、変更前後の本文または該当 anchor / セクション差分も同ターンで控える
  - 変更直後に Team UI を再読込し、Team API GET でも同じ値になったことを確認する
  - **変更後**に未認証 HTML GET と `qiita.com/furuse-kazufumi/items/<id>?v=<ts>` direct probe も再取得し、before/after を並べて記録する
  - 結果は成功/失敗にかかわらず、`team_stock_queue.md` の `visible range` / `rollback needed` / `note` を正本として先に反映し、その後 `docs/next_plan.md`、最後に `docs/SESSION_SUMMARY.md` では queue の該当行参照だけを同ターンに反映する
- article-by-article handling:
  - 3 本は一括で扱わず、**1 本ごとに** `positive / unresolved / cleared` を判定する
  - 1 本でも未認証 HTML GET / public direct probe で positive が出たら、その記事だけ即 containment / remediation gate へ送る
  - `302 / 403 / 404` だけでは cleared にせず `unresolved` とする
  - 残りの記事は diagnosis を継続し、一括 retain に巻き戻さない
- no-op retain checklist (human-gate 後のみ):
  - 新しい外部 remediation を打たず、`team_stock_queue.md` の各行と `2026-06-19 visibility probe evidence` を見直し、**今回も診断未了のため no-op retain。過剰露出疑いは未解消のまま残る**と 1 行追記する
  - `note` には「なぜ今回は動かなかったか」「次回の解禁条件は何か」「retain_count=<n>」「retain_deadline=<timestamp>」「human_exemption=<reason/approver>」までを短く残す
  - その後 `docs/next_plan.md`、`docs/SESSION_SUMMARY.md` の順で、queue の該当 note を参照しつつ、今回 no-op retain を選んだことと次に必要な診断条件だけを追記する
- fail-closed temporary tightening (human-gate 後のみ):
  - 診断未了のまま retain を繰り返さないため、必要なら **暫定 private 化してから containment 完了確認を取る**
  - この分岐は Team UI diagnosis と別の外部状態変更なので、必ず別 human-gate で GO を取ってから触る
  - 実行前に before-state と intended state、rollback 責任者、業務影響メモを記事ごとに記録する
  - 解禁条件は、private 化後に Team UI / Team API GET / 未認証 HTML GET / direct probe の before/after が揃い、intended share target / intended private state と矛盾しないこと。public へ戻すときは Team URL / public URL のどちらを触るかを記事ごとに明記し、URL 変化や重複草稿の副作用も記録する
- remediation patch template (human-gate 後のみ):
  - `py -3.11 tools/qiita_team_post.py dry-run tools/qiita-cli-poc/public/team_stock_semantic_governance.md --patch-group-url-name`
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_semantic_governance.md --yes --force-ignore-publish --patch-group-url-name`
  - `py -3.11 tools/qiita_team_post.py dry-run tools/qiita-cli-poc/public/team_stock_llm_wiki_anti_circulation.md --patch-group-url-name`
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_llm_wiki_anti_circulation.md --yes --force-ignore-publish --patch-group-url-name`
  - `py -3.11 tools/qiita_team_post.py dry-run tools/qiita-cli-poc/public/team_stock_ctx2549_postmortem.md --patch-group-url-name`
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_ctx2549_postmortem.md --yes --force-ignore-publish --patch-group-url-name`
  - 前提: 実行前に対象 source の frontmatter へ human が選んだ concrete `group_url_name` を入れておく。現状の local source は未設定なので、そのままでは全件 BLOCK する

## rollback notes

- 最低限、POST 直後に返る `id` を控える
- rollback は delete 前提ではなく、まず Team UI または API で body / title を差し替えられるかを確認する
- `private` の変更で可視範囲を狭められるかは未検証なので、rollback の主手段としては使わない
- 可視範囲が想定より広い場合は、その事実を blocker として queue / handoff に即記録し、続く非表示化 / 差し替えは別の human-gate 外部アクションとして切り出す
- rollback 実施時は、理由と結果を `team_stock_queue.md` と handoff に 1 行残す

## 2026-06-18 実行結果メモ

- 3 本とも `post --yes` は 201 Created で成功した
- 返却 item id:
  - `6f67e54e538c10b8f1c3`
  - `b35b429dc6dc1fde207a`
  - `6fe79ab04443f7654eca`
- POST 後の API GET では 3 本とも `private:false` で返った
- 同じ API GET では 3 本とも `group.url_name: general` / `group.private:false` / `organization_url_name:null` も返った
- 2026-06-19 12:41:22 +09:00 の未認証 HTML GET では、3 本とも Team URL に対して `302` / `Location: /login?redirect_to=...` が返った
- 2026-06-19 12:41:22 +09:00 の direct probe では、`https://qiita.com/furuse-kazufumi/items/<id>` 側に 3 本とも `404` が返った
- ただし Team サブドメイン全体が private/public にかかわらず auth gate される可能性は残る。したがって Login redirect だけでは item の可視範囲を断定できず、**team-only と positively 確認できるまでは過剰露出の疑いを優先**する
- なおこの `qiita.com` 側 `404` は Team scope item なら team-only / 過剰露出のどちらでも起こりうるため、**over-exposure 判定の弁別力は無い**。今回 probe した 3 本について、同時点で public 側の対応記事を直URLでは確認できなかった、という記録としてのみ使う
- `private:false` の意味づけ自体も一次情報待ちであり、ここで言う `visibility semantics` は **プロジェクト内用語**に過ぎない。rollback / visibility tightening は別の human-gate 外部アクションとして扱う
- 追加の現時点仮説として、2026-06-18 の poster payload では `group_url_name` を明示しておらず、観測された `group.url_name: general` は implicit General sharing を示している可能性がある。これは root-cause 仮説であって、team-only の証明でも否定でもない。local source にはこの観測値を resend default として固定せず、将来の create は explicit target を再判断する
- 2026-06-19 のローカル改修で、**既定 PATCH は維持したまま** `--patch-group-url-name` を付けたときだけ `group_url_name` を再送できる remediation 経路を追加した。これは **共有先 (`group_url_name`) を寄せ直すための経路**であり、`private` 範囲の tightening そのものではない。dry-run でも `private` は frontmatter 値を再送する旨を明示する。現在の 3 本は source が `private:false` のため、この経路だけでは露出疑いを縮めず、`private:true` へ直す別アクションが要る
- Qiita API docs の `PATCH /api/v2/items/:item_id` に `group_url_name` 記載がある可能性はあるが、この点自体は現時点で一次未確認である。したがって現状ここで確定しているのは、ローカル実装として resend 経路を持たせたことだけであり、**既に共有済み item に対し、この PATCH が実際に共有先や可視範囲を締め直す効果を持つかは一次未確認**のまま扱う
- 従って、以後の remediation 候補は Team UI と **human-gate 後の opt-in PATCH** の二択まで狭まったが、後者を「visibility 是正が実証済み」とは扱わない。frontmatter に concrete target が無い場合は fail-closed で停止し、通常更新では再送しない
- 2026-06-19 のローカル dry-run 再確認では、local draft 3 本すべてが `--patch-group-url-name` 付きで `PATCH_GROUP_URL_NAME_BLOCK` になった。理由は source 側 frontmatter に `group_url_name` が無いからであり、これは意図どおりの fail-closed 挙動である
- 2026-06-19 のローカル整理として、次の human-gate に向けた **Team UI remediation checklist** もこの runbook に追加した。趣旨は、UI 編集それ自体よりも前後の evidence capture と queue / handoff 反映順を固定することにある

## POST 後の記録先

- `id` / Team URL / visible range / rollback の要否は `team_stock_queue.md` の `POST 後の記録欄` を正本として更新する
- local draft から public/Team 公開向けに追加した但し書きの有無も、同欄の `note` へ集約する
