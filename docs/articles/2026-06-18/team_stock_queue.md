# Team Stock Queue (2026-06-18)

Qiita Team 向けに「難しい内容を後で個別公開できるよう stock しておく」ための local queue。

## この文書の役割

- **正本**: 投稿待ち一覧と現在の blocker をここに集約する。外部判断の記録の canonical field は **POST 後の記録欄 `visible range memo` / `rollback needed` / `note`** とする
- `team_stock_publish_plan.md`: 公開順・human gate 条件・rollback 注意の正本

## 状態定義

- `local_draft`: repo 内に草稿あり。外部 POST はまだしていない
- `dry_run_ok`: `tools/qiita_team_post.py dry-run` は通過
- `blocked_human_gate`: 外部 POST 前の human gate 待ち
- `published`: Team POST 済み。`item id` / URL / visible range を記録済み
- `rollback_applied`: rollback 実施済み。理由と結果を `note` に残す

## Queue

| slug | title | source | status | note |
| --- | --- | --- | --- | --- |
| `team_stock_semantic_governance.md` | Semantic Governance は「AI の権限管理」ではなく「AI の意味管理」 | #43 `2-2. loop engineering にもセキュリティの顔がある` | `published` | 2026-06-18 Team POST 済み。API GET では `private:false`、`group.url_name: general`、`group.private:false` |
| `team_stock_llm_wiki_anti_circulation.md` | LLM Wiki の本当の難所は「知識を集めること」ではなく「思考の循環を止めること」 | #43 `3-2. LLM Wiki — 「育つ知識」のパターン` | `published` | 2026-06-18 Team POST 済み。API GET では `private:false`、`group.url_name: general`、`group.private:false` |
| `team_stock_ctx2549_postmortem.md` | `ctx 2549%` は AI の暴走ではなく人間の計測破綻だった — llterm 障害対応の切り分け記録 | #46 `2. ターン境界と緊急割り込みは、最初から別物として設計する / 3. ctx 2549% は「AI が太った」のではなく、計測が壊れていた / 6. テストも「たまたま緑」を疑う` | `published` | 2026-06-18 Team POST 済み。API GET では `private:false`、`group.url_name: general`、`group.private:false` |

## POST 後の記録欄

| slug | item id | Team URL | visible range memo | rollback needed | note |
| --- | --- | --- | --- | --- | --- |
| `team_stock_semantic_governance.md` | `6f67e54e538c10b8f1c3` | `https://fullsense.qiita.com/furuse-kazufumi/items/6f67e54e538c10b8f1c3` | API GET で `private:false`、`group.url_name: general`、`group.private:false`。2026-06-19 12:41:22 +09:00 の未認証 HTML GET は `302 /login?redirect_to=...` | conditional | team-only と positively 確認できるまでは過剰露出の疑いを優先する。生 evidence は下の `2026-06-19 visibility probe evidence` を参照。`visibility semantics` の不一致は副次論点。`group_url_name` omission 仮説も併記して追う。rollback は別 human-gate 判断 |
| `team_stock_llm_wiki_anti_circulation.md` | `b35b429dc6dc1fde207a` | `https://fullsense.qiita.com/furuse-kazufumi/items/b35b429dc6dc1fde207a` | API GET で `private:false`、`group.url_name: general`、`group.private:false`。2026-06-19 12:41:22 +09:00 の未認証 HTML GET は `302 /login?redirect_to=...` | conditional | team-only と positively 確認できるまでは過剰露出の疑いを優先する。生 evidence は下の `2026-06-19 visibility probe evidence` を参照。`visibility semantics` の不一致は副次論点。`group_url_name` omission 仮説も併記して追う。rollback は別 human-gate 判断 |
| `team_stock_ctx2549_postmortem.md` | `6fe79ab04443f7654eca` | `https://fullsense.qiita.com/furuse-kazufumi/items/6fe79ab04443f7654eca` | API GET で `private:false`、`group.url_name: general`、`group.private:false`。2026-06-19 12:41:22 +09:00 の未認証 HTML GET は `302 /login?redirect_to=...` | conditional | team-only と positively 確認できるまでは過剰露出の疑いを優先する。生 evidence は下の `2026-06-19 visibility probe evidence` を参照。`visibility semantics` の不一致は副次論点。`group_url_name` omission 仮説も併記して追う。rollback は別 human-gate 判断 |

### 2026-06-19 visibility probe evidence

- timestamp:
  - `2026-06-19 12:41:22 +09:00`
- command (API):
  - `py -3.11 -c "import json,sys,urllib.request; sys.path.insert(0, 'tools'); from qiita_team_post import get_token; ... GET https://fullsense.qiita.com/api/v2/items/<id> with Bearer token ..."`
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
  - `qiita.com/furuse-kazufumi/items/<id>` の direct `404` は、Team scope item なら team-only / 過剰露出のどちらでも起こりうるため、**over-exposure 判定の弁別力は無い**
  - したがってこの probe は「今回 probe した 3 本について、2026-06-19 12:41:22 +09:00 時点で public 側の対応記事を直URLでは確認できなかった」という記録に留める
  - 追加で、poster payload 側では当時 `group_url_name` を送っていなかった。`group.url_name: general` / `group.private:false` の観測は、implicit General sharing が起きた可能性を示す **現時点の仮説**として扱う。local source にはこの観測値を再送信既定値として固定しない

## blockers

1. 2026-06-19 時点の `tools/qiita_team_post.py` は `ignorePublish` を読み、`ignorePublish:true` の source は `--force-ignore-publish` 無しでは fail-closed で停止する。したがってこのフラグは「未投稿」を意味せず、Team poster でも明示 override を要する source freeze として扱う
2. 2026-06-18 の API GET では 3 本とも `private:false` で返っており、frontmatter `private:true` は Team create 後の可視範囲を保証しなかった
3. 2026-06-19 の未認証 HTML GET では 3 本とも Login ページへ落ちたが、これは Team サブドメイン全体の auth gate でも説明できる。したがって team-only と positively 確認できるまでは **過剰露出の疑いを優先**し、`private:false` の意味づけは一次情報待ちとする
4. current blocker の主語は「Team API / visibility semantics（プロジェクト内用語）の不一致」ではなく、**過剰露出の疑いを否定できないこと**に置く。不一致は副次論点として記録する
5. 2026-06-19 以降の Team create は、poster が `group_url_name` を明示しないまま implicit share target に依存しないよう fail-closed 化済みで、`group_url_name` の未指定 / `null` / 空値は BLOCK する
6. 2026-06-19 のローカル改修で、通常 PATCH はそのままに **`--patch-group-url-name` 付きの opt-in remediation 経路**を追加した。frontmatter に concrete `group_url_name` が無ければ fail-closed で停止するため、既存 item の可視範囲を寄せ直す候補は `Team UI` と `human-gate 後の opt-in PATCH` の二択になった
7. rollback / 可視範囲の絞り込み自体は、引き続き別の human-gate 外部アクションとして扱う
8. 2026-06-19 の local draft 再確認では、3 本とも frontmatter に `group_url_name` が無く、`dry-run ... --patch-group-url-name` は全件 `PATCH_GROUP_URL_NAME_BLOCK` で停止した。つまり opt-in PATCH 経路は実装済みだが、**human が concrete target を決めて source に入れるまでは実行不能**である
9. 次の外部 remediation 順序は **containment first / Team UI second / opt-in PATCH last** とする。未認証 HTML GET / public direct probe で positive が出た記事はその記事だけ即 containment 候補に上げる。opt-in PATCH はローカル実装と fail-closed guard までは確認済みだが、既共有 item に対する締め直し効果が一次未確認だからである
10. Team UI remediation に進む場合は、`team_stock_publish_plan.md` の **Team UI remediation checklist** を正本として、変更前後の Team API GET / Team UI / 未認証 HTML GET / direct probe / source frontmatter の差分だけを記録する
11. **diagnosis 完了**は、対象 3 本それぞれで **5 ソース** `Team UI の share target / private state`、`Team API GET の group.url_name / private / organization_url_name`、`未認証 HTML GET`、`public direct probe`、`source frontmatter の private / group_url_name`（intended state ラベル）を同じターンで並べ、share target 起因か private state 起因か、または未確定かを 1 行で判定できる状態を指す。`Team API GET / 未認証 HTML GET / public direct probe` は **3 種再取得ソース**として同ターンで採り直す
12. 判定基準は project-local rule として暫定固定する。`share target 起因` は intended `private` 意図が揃っているのに target だけが intended target から外れている場合、`private state 起因` は target が揃っているのに Team UI / API の `private` 系だけが intended state から外れている場合とする。frontmatter は intended state のラベルであり、実露出の証拠には使わない
13. 5 ソースが矛盾したときの裁定順も **我々のローカル運用ルール**として暫定固定する。優先順位は `未認証 HTML GET / public direct probe の外形的事実` > `Team UI 表示` > `Team API GET` > `source frontmatter` とし、**実 Team 記事 URL** への `200` かつ対象記事の title / body 断片を読めた場合だけ `positive` とする。`302 / 403 / 404` や空本文は **未確定** であり、安全証明に使わない。public 面しか叩けない probe は `無情報` と記録する
14. `未確定` は catch-all の保留ではなく、default で **fail-closed 候補**に送る。`現状維持で記録だけ続ける` を選ぶ場合は、`POST 後の記録欄` の `note` に **今回も診断未了のため no-op retain。過剰露出疑いは未解消のまま残る** と、次回の解禁条件を 1 行で残す。同じ理由での no-op retain は 1 回までとし、2 回目に入る前に **暫定 private 化してから再診断する** 選択肢を必ず human-gate に出す。時間上限は次回 human-gate までとする
15. 3 本は一括処理しない。**1 本でも positive が出たらその記事だけ containment / remediation**、残りは diagnosis 継続とする
16. intended state の baseline は option 選択前に 3 本それぞれで固定する。source frontmatter の `private` / `group_url_name` と、人間が意図した公開範囲メモを同じ行で扱う。frontmatter は intended state の根拠であり、実露出の証拠には使わない

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
