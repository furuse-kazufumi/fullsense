# Team Stock Publish Plan (2026-06-18)

`tools/qiita-cli-poc/public/` に切った Team stock 用 source-only draft を、
後で Qiita Team `fullsense` へ流すときの順番と注意点をまとめる。

## この文書の役割

- **正本**: 公開順・human gate 条件・rollback 注意をここに集約する
- `team_stock_queue.md`: 投稿待ち一覧の正本
- `next_plan.md` / `SESSION_SUMMARY.md`: この正本への参照だけを持つ

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
8. 実行順は **Team UI first / opt-in PATCH second** を原則にする。opt-in PATCH はローカル実装済みだが、既共有 item に対する締め直し効果が一次未確認なため、まず UI 上で intended share target / private state を確認・是正できるかを先に見る

## execution commands

- create:
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_semantic_governance.md --yes --force-ignore-publish`
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_llm_wiki_anti_circulation.md --yes --force-ignore-publish`
  - `py -3.11 tools/qiita_team_post.py post tools/qiita-cli-poc/public/team_stock_ctx2549_postmortem.md --yes --force-ignore-publish`
- verify:
  - Team API / UI で title, private 状態, URL を確認する
  - `team_stock_queue.md` に `id` / URL / visible range を転記する
- Team UI remediation checklist (human-gate 後のみ):
  - 変更前に Team UI と Team API GET の両方で、対象 3 本の `title` / `private` / `group.url_name` / `organization_url_name` を控える
  - human が intended share target と intended private state を 3 本それぞれで明示してから UI を触る
  - remediation 中は delete を使わず、まず UI 上で share target / private state / body 差し替えのどれが可能かを切り分ける
  - `body 差し替え` を行った場合は、変更前後の本文または該当 anchor / セクション差分も同ターンで控える
  - 変更直後に Team UI を再読込し、Team API GET でも同じ値になったことを確認する
  - 未認証 HTML GET と `qiita.com/furuse-kazufumi/items/<id>` direct probe も再取得し、**直近の visibility probe evidence の時刻**との差分だけを記録する
  - 結果は成功/失敗にかかわらず、`team_stock_queue.md` の `visible range` / `rollback needed` / `note` へ先に反映し、その後 `docs/next_plan.md`、最後に `docs/SESSION_SUMMARY.md` の順で同ターンに反映する
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
