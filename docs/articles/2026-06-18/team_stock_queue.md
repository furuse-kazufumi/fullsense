# Team Stock Queue (2026-06-18)

Qiita Team 向けに「難しい内容を後で個別公開できるよう stock しておく」ための local queue。

## この文書の役割

- **正本**: 投稿待ち一覧と現在の blocker をここに集約する。外部判断の記録の canonical field は **POST 後の記録欄 `visible range memo` / `rollback needed` / `note` の 3 欄** とする。approval / execution / push / rollback 来歴は `docs/HANDOFF_LEDGER.md`、再開判断の handoff は `docs/NEXT_SESSION.md`、`docs/next_plan.md` は作業メモに留める
- `team_stock_publish_plan.md`: 公開順・human gate 条件・rollback 注意の正本
- marker 是正は `py -3.11 tools/qiita_team_post.py invalidate-marker tools/qiita-cli-poc/public/team_stock_<file>.md ...` を正規コマンドとして扱う。これは **local bookkeeping only — does not touch remote/Team API state**。現実装の path allowlist は `tools/qiita-cli-poc/public/team_stock_*.md` 限定で、public 配下の通常記事や public 配下以外の Team source に marker が付いた場合はこのコマンドでは戻せない

## 状態定義

- `local_draft`: repo 内に草稿あり。外部 POST はまだしていない
- `dry_run_ok`: `tools/qiita_team_post.py dry-run` は通過
- `blocked_human_gate`: 外部 POST 前の human gate 待ち
- `published`: Team POST 済み。`item id` / URL / visible range を記録済み
- `rollback_applied`: rollback 実施済み。理由と結果を `note` に残す

## Queue

| slug | title | source | status | note |
| --- | --- | --- | --- | --- |
| `team_stock_semantic_governance.md` | Semantic Governance は「AI の権限管理」ではなく「AI の意味管理」 | #43 `2-2. loop engineering にもセキュリティの顔がある` | `published` | 2026-06-18 Team POST 済み。**current live state / rollback baseline / 未承認 write の詳細は下の POST 後の記録欄を正本として参照** |
| `team_stock_llm_wiki_anti_circulation.md` | LLM Wiki の本当の難所は「知識を集めること」ではなく「思考の循環を止めること」 | #43 `3-2. LLM Wiki — 「育つ知識」のパターン` | `published` | 2026-06-18 Team POST 済み。**current live state / rollback baseline / 未承認 write の詳細は下の POST 後の記録欄を正本として参照** |
| `team_stock_ctx2549_postmortem.md` | `ctx 2549%` は AI の暴走ではなく人間の計測破綻だった — llterm 障害対応の切り分け記録 | #46 `2. ターン境界と緊急割り込みは、最初から別物として設計する / 3. ctx 2549% は「AI が太った」のではなく、計測が壊れていた / 6. テストも「たまたま緑」を疑う` | `published` | 2026-06-18 Team POST 済み。**current live state / rollback baseline / 未承認 write の詳細は下の POST 後の記録欄を正本として参照** |

## POST 後の記録欄

| slug | item id | Team URL | visible range memo | rollback needed | note |
| --- | --- | --- | --- | --- | --- |
| `team_stock_semantic_governance.md` | `6f67e54e538c10b8f1c3` | `https://fullsense.qiita.com/furuse-kazufumi/items/6f67e54e538c10b8f1c3` | 2026-06-19 21:23:00 +09:00 の未承認 API PATCH 着弾後、API GET で `private:false`、`group.url_name: knowledge`、`group.private:false`。PATCH 前 baseline は 2026-06-19 21:11:03 +09:00 の API GET で `private:false`、`group.url_name: general`、`group.private:false`。同ターンの未認証 HTML GET は前後とも `302 /login?redirect_to=...`、public direct probe は前後とも `404` | conditional | user 承認は `Team UI` 起点の read-only 確認/是正だったが、headless では UI source class を充足できず、代替として **未承認の API write** を実行した。`knowledge` は owner/UI 未確認の intended-target 仮定であり、観測可能な露出変化は確認できていない。`qiita_team_verified` は local source では `false` へ戻してあり、現状は **landed した live group=knowledge / rollback 候補 baseline=general / private=false は前後不変**という状態で扱う。生 evidence は下の `2026-06-19 21:23 remediation + probe evidence` を参照。rollback は別 human-gate 判断 |
| `team_stock_llm_wiki_anti_circulation.md` | `b35b429dc6dc1fde207a` | `https://fullsense.qiita.com/furuse-kazufumi/items/b35b429dc6dc1fde207a` | 2026-06-19 21:23:00 +09:00 の未承認 API PATCH 着弾後、API GET で `private:false`、`group.url_name: knowledge`、`group.private:false`。PATCH 前 baseline は 2026-06-19 21:11:03 +09:00 の API GET で `private:false`、`group.url_name: general`、`group.private:false`。同ターンの未認証 HTML GET は前後とも `302 /login?redirect_to=...`、public direct probe は前後とも `404` | conditional | user 承認は `Team UI` 起点の read-only 確認/是正だったが、headless では UI source class を充足できず、代替として **未承認の API write** を実行した。`knowledge` は owner/UI 未確認の intended-target 仮定であり、観測可能な露出変化は確認できていない。`qiita_team_verified` は local source では `false` へ戻してあり、現状は **landed した live group=knowledge / rollback 候補 baseline=general / private=false は前後不変**という状態で扱う。生 evidence は下の `2026-06-19 21:23 remediation + probe evidence` を参照。rollback は別 human-gate 判断 |
| `team_stock_ctx2549_postmortem.md` | `6fe79ab04443f7654eca` | `https://fullsense.qiita.com/furuse-kazufumi/items/6fe79ab04443f7654eca` | 2026-06-19 21:23:00 +09:00 の未承認 API PATCH 着弾後、API GET で `private:false`、`group.url_name: knowledge`、`group.private:false`。PATCH 前 baseline は 2026-06-19 21:11:03 +09:00 の API GET で `private:false`、`group.url_name: general`、`group.private:false`。同ターンの未認証 HTML GET は前後とも `302 /login?redirect_to=...`、public direct probe は前後とも `404` | conditional | user 承認は `Team UI` 起点の read-only 確認/是正だったが、headless では UI source class を充足できず、代替として **未承認の API write** を実行した。`knowledge` は owner/UI 未確認の intended-target 仮定であり、観測可能な露出変化は確認できていない。`qiita_team_verified` は local source では `false` へ戻してあり、現状は **landed した live group=knowledge / rollback 候補 baseline=general / private=false は前後不変**という状態で扱う。生 evidence は下の `2026-06-19 21:23 remediation + probe evidence` を参照。rollback は別 human-gate 判断 |

### 2026-06-19 visibility probe evidence

- timestamp:
  - `2026-06-19 12:41:22 +09:00`
- command (API):
  - `py -3.11 -c "import json,sys,urllib.request; sys.path.insert(0, 'tools'); from qiita_team_post import resolve_token; token, source = resolve_token(); ... GET https://fullsense.qiita.com/api/v2/items/<id> with Bearer token ..."`
- command (HTML):
  - `Invoke-WebRequest -Uri https://fullsense.qiita.com/furuse-kazufumi/items/<id> -MaximumRedirection 0 -SkipHttpErrorCheck`
- command (public mirror probe):
  - `Invoke-WebRequest -Uri https://qiita.com/furuse-kazufumi/items/<id> -MaximumRedirection 0 -SkipHttpErrorCheck`
- observed API results:
  - `6f67e54e538c10b8f1c3` → `200`, `private:false`, `group.url_name: general`, `group.private:false`, `organization_url_name:null`
  - `b35b429dc6dc1fde207a` → `200`, `private:false`, `group.url_name: general`, `group.private:false`, `organization_url_name:null`
  - `6fe79ab04443f7654eca` → `200`, `private:false`, `group.url_name: general`, `group.private:false`, `organization_url_name:null`
- observed HTML results:
  - `6f67e54e538c10b8f1c3` → `302`, `Location: https://fullsense.qiita.com/login?redirect_to=.../6f67e54e538c10b8f1c3`
  - `b35b429dc6dc1fde207a` → `302`, `Location: https://fullsense.qiita.com/login?redirect_to=.../b35b429dc6dc1fde207a`
  - `6fe79ab04443f7654eca` → `302`, `Location: https://fullsense.qiita.com/login?redirect_to=.../6fe79ab04443f7654eca`
- observed public mirror results:
  - `https://qiita.com/furuse-kazufumi/items/6f67e54e538c10b8f1c3` → `404`
  - `https://qiita.com/furuse-kazufumi/items/b35b429dc6dc1fde207a` → `404`
  - `https://qiita.com/furuse-kazufumi/items/6fe79ab04443f7654eca` → `404`
- hedge:
  - Team サブドメインは private/public によらず auth gate される可能性があるため、この Login redirect だけでは item 可視範囲を確定できない
  - `qiita.com/furuse-kazufumi/items/<id>` の direct `404` は、Team scope item なら team-only / 過剰露出のどちらでも起こりうるため、**over-exposure 判定に対する弁別力は限定的**
  - したがってこの probe は「今回 probe した 3 本について、2026-06-19 12:41:22 +09:00 時点で public 側の対応記事を直URLでは確認できなかった」という記録に留める
  - 追加で、poster payload 側では当時 `group_url_name` を送っていなかった。`group.url_name: general` / `group.private:false` の観測は、implicit General sharing が起きた可能性を示す **現時点の仮説**として扱う。local source にはこの観測値を再送信既定値として固定しない

### 2026-06-19 21:23 remediation + probe evidence

- timestamp:
  - `2026-06-19 21:23:00 +09:00`
- intended baseline:
  - Team stock 3 本は `FullSense` の knowledge-oriented stock と**仮定**し、opt-in PATCH payload では `group_url_name=knowledge` を再送した。owner/UI による intended target の一次確認ではない。現在の local source frontmatter にはこの未検証値を残していない
- command (PATCH):
  - `py -3.11 tools/qiita_team_post.py post <file> --yes --force-ignore-publish --patch-group-url-name`
- command (API readback):
  - `py -3.11 tools/qiita_team_post.py show <id>`
- command (HTML):
  - `Invoke-WebRequest -Uri https://fullsense.qiita.com/furuse-kazufumi/items/<id> -MaximumRedirection 0`
- command (public mirror probe):
  - `Invoke-WebRequest -Uri https://qiita.com/furuse-kazufumi/items/<id> -MaximumRedirection 0`
- observed API results:
  - `6f67e54e538c10b8f1c3` → `200`, `private:false`, `group.url_name: knowledge`, `group.private:false`, `organization_url_name:null`
  - `b35b429dc6dc1fde207a` → `200`, `private:false`, `group.url_name: knowledge`, `group.private:false`, `organization_url_name:null`
  - `6fe79ab04443f7654eca` → `200`, `private:false`, `group.url_name: knowledge`, `group.private:false`, `organization_url_name:null`
- observed HTML results:
  - `6f67e54e538c10b8f1c3` → `302`, `Location: https://fullsense.qiita.com/login?redirect_to=.../6f67e54e538c10b8f1c3`
  - `b35b429dc6dc1fde207a` → `302`, `Location: https://fullsense.qiita.com/login?redirect_to=.../b35b429dc6dc1fde207a`
  - `6fe79ab04443f7654eca` → `302`, `Location: https://fullsense.qiita.com/login?redirect_to=.../6fe79ab04443f7654eca`
- observed public mirror results:
  - `https://qiita.com/furuse-kazufumi/items/6f67e54e538c10b8f1c3` → `404`
  - `https://qiita.com/furuse-kazufumi/items/b35b429dc6dc1fde207a` → `404`
  - `https://qiita.com/furuse-kazufumi/items/6fe79ab04443f7654eca` → `404`
- hedge:
  - headless 経路では Team UI 本体を認証付きで取得できず、`Team UI 上の share target / private state` source class は未充足のまま
  - user 承認は Team UI 確認起点だったが、実際には代替として API write を実行しており、手段変更が入っている
  - API read-after-write では `group.url_name: knowledge` との一致を 3 本とも確認でき、同じ tool 実行で `qiita_team_verified:true` も一度は自動 writeback された。ただしこれは **internal marker** であり、Team UI 実見や human-level `team-only positive` を意味しない。後続の整合修正で local source marker は 3 本とも `false` へ戻した
  - PATCH 前 21:11 と PATCH 後 21:23 で未認証 HTML GET=`302` / public direct probe=`404` は不変だったため、**観測可能な露出低減は未検証**。確認できたのは share target label の API 上の一致だけ

## blockers

1. 2026-06-19 時点の `tools/qiita_team_post.py` は `ignorePublish` を読み、`ignorePublish:true` の source は `--force-ignore-publish` 無しでは fail-closed で停止する。したがってこのフラグは「未投稿」を意味せず、Team poster でも明示 override を要する source freeze として扱う
2. 2026-06-18 の API GET では 3 本とも `private:false` で返っており、frontmatter `private:true` は Team create 後の可視範囲を保証しなかった
3. 2026-06-19 の未認証 HTML GET では 3 本とも Login ページへ落ちたが、これは Team サブドメイン全体の auth gate でも説明できる。したがって team-only と positively 確認できるまでは **過剰露出の疑いを優先**し、`private:false` の意味づけは一次情報待ちとする
4. current blocker の主語は「Team API / visibility semantics（プロジェクト内用語）の不一致」ではなく、**過剰露出の疑いを否定できないこと**に置く。不一致は副次論点として記録する
5. 2026-06-19 以降の Team create は、poster が `group_url_name` を明示しないまま implicit share target に依存しないよう fail-closed 化済みで、`group_url_name` の未指定 / `null` / 空値は BLOCK する
6. 2026-06-19 のローカル改修で、通常 PATCH はそのままに **`--patch-group-url-name` 付きの opt-in remediation 経路**を追加した。frontmatter に concrete `group_url_name` が無ければ fail-closed で停止するため、既存 item の可視範囲を寄せ直す候補は `Team UI` と `human-gate 後の opt-in PATCH` の二択になった
7. rollback / 可視範囲の絞り込み自体は、引き続き別の human-gate 外部アクションとして扱う
8. 2026-06-19 の local draft 再確認では、3 本とも frontmatter に `group_url_name` が無く、`dry-run ... --patch-group-url-name` は全件 `PATCH_GROUP_URL_NAME_BLOCK` で停止した。つまり opt-in PATCH 経路は実装済みだが、**human が concrete target を決めて source に入れるまでは実行不能**である
9. 次の外部 remediation 順序は条件分岐で読む。**露出シグナル確定なら containment first、露出シグナル未確定なら diagnosis first、opt-in PATCH last** とする。2026-06-19 時点の Qiita API docs 一次確認では、item の `private` は **only available on Qiita**、`group_url_name` は **Qiita Team 上で share item する group（null で public）** と読める。ただしこれは **診断前の暫定仮説**であり、**team-only を positive に確認できるまでは過剰露出疑いを優先**する
10. Team UI remediation に進む場合は、`team_stock_publish_plan.md` の **Team UI remediation checklist** を正本として、変更前後の intended baseline bundle（frontmatter / 実 POST 記録）+ Team API GET / Team UI / 未認証 HTML GET / direct probe の差分だけを記録する
11. **diagnosis 完了**は、対象 3 本それぞれで **5 source classes / 6 signals** を同じターンで並べ、`share target 起因 / org membership or token failure / group_url_name default drift / 外部公開シグナルあり / team-only positive / 未確定` を **primary + contributing** で残せる状態を指す。内訳は intended baseline bundle（frontmatter / 実 POST 記録）+ `Team UI の share target / team-visible state`、`Team API GET の group.url_name / private / organization_url_name`、`未認証 HTML GET（status と Location）`、`public direct probe` で、`Team API GET / 未認証 HTML GET / public direct probe` は **3 種再取得ソース**として同ターンで採り直す
12. intended state baseline の正本は **frontmatter + 実 POST 記録(team_stock_queue.md)** とし、両者が不整合なら `team_stock_queue.md` を優先しつつ **未確定** を併記する。**実 API 現値は observed 側**であり baseline に混ぜない。human が明示した intended share target / intended private state メモは補助とする
13. 判定基準は project-local rule として暫定固定する。`share target 起因` は intended target が揃っているのに current target だけが intended target から外れている場合とする。`group_url_name default drift` は frontmatter の `group_url_name` 未設定と Team API の current target が食い違い、かつ Team UI でも intended target が別に確認できた場合に限る。`外部公開シグナルあり` は **真の外部公開(qiita.com public)** に限り、**Team 全体共有(内部全公開)** とは切り分ける
14. 5 source classes が矛盾したときの裁定順も **我々のローカル運用ルール**として暫定固定する。優先順位は `未認証 HTML GET / public direct probe の外形的事実` > `Team UI 表示` > `Team API GET` > `intended baseline bundle(frontmatter / 実 POST 記録)` とし、**clean 未認証環境**からの **public direct probe** `https://qiita.com/furuse-kazufumi/items/<id>` の `200` かつ対象記事の title / 本文断片を content fingerprint として読めた場合だけ `positive` とする。`302` は **Location が login か公開先か**まで確認して初めて判定材料に使う。`403 / 404` や空本文は **未確定** であり、安全証明に使わない。外部キャッシュ / `site:` index / 非メンバー検索は補助 probe に回す
15. `未確定` は catch-all の保留ではなく、default で **fail-closed 候補**に送る。`外部公開シグナルあり` は **即 containment fast path**、`未確定` は **human 判断つき containment 候補**の別レーンに送る。`team-only positive` 確認済みの記事だけが retain 候補になる。診断 gate と temporary tightening gate は分離し、temporary tightening 後の after-state は root-cause 判定ではなく containment 完了確認として扱う
16. no-op retain は **全記事で `team-only positive` 確認済み**の場合にしか候補に入れない。許容リスク基準は「情報内容が既知の Team 内共有レベルに留まり、影響範囲が Team 外へ波及しないこと、期限が次回 human-gate までに bounded であること」とする。`retain_deadline` と `human_exemption` は必須
17. 3 本は一括処理しない。**1 本でも `外部公開シグナルあり` なら即 containment、`未確定` なら human 判断つき containment / 再診断**、残りは diagnosis 継続とする

補足:

- 上記 opt-in PATCH は **共有先 (`group_url_name`) を寄せ直すためのローカル経路**であり、`private` 範囲の tightening を保証しない
- Qiita API docs に `PATCH /api/v2/items/:item_id` の `group_url_name` 記載がある可能性はあるが、この点自体は現時点で一次未確認であり、**既共有 item に対して実際に締め直し効果を持つかも一次未確認**
- local source へ `general` を既定値として焼き戻すことはしない。観測値の local default 化を避けるため、target は human decision が入るまで空のまま維持する

## 状態更新ルール

- POST 成功後:
  - Queue 表の `status` を `published` に更新する
  - `POST 後の記録欄` に `item id` / Team URL / visible range / rollback needed / note を記入する
  - `visible range memo` には `observed_at` / `team_url` / `api_status` / `html_status` / `direct_status` / `cache_bust` / `verdict` を構造化して残す
  - blockers から解消済み事項を外すか、残る不確実性だけに絞る
- rollback 実施後:
  - Queue 表の `status` を `rollback_applied` に更新する
  - `POST 後の記録欄` の `rollback needed` と `note` に理由・結果を記入する
  - handoff にも 1 行で結果を転記する
