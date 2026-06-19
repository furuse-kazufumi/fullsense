# Team Stock Queue (2026-06-18)

Qiita Team 向けに「難しい内容を後で個別公開できるよう stock しておく」ための local queue。

## この文書の役割

- **正本**: 投稿待ち一覧と現在の blocker をここに集約する
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
| `team_stock_semantic_governance.md` | Semantic Governance は「AI の権限管理」ではなく「AI の意味管理」 | #43 `2-2. loop engineering にもセキュリティの顔がある` | `published` | 2026-06-18 Team POST 済み。API GET では `private:false` |
| `team_stock_llm_wiki_anti_circulation.md` | LLM Wiki の本当の難所は「知識を集めること」ではなく「思考の循環を止めること」 | #43 `3-2. LLM Wiki — 「育つ知識」のパターン` | `published` | 2026-06-18 Team POST 済み。API GET では `private:false` |
| `team_stock_ctx2549_postmortem.md` | `ctx 2549%` は AI の暴走ではなく人間の計測破綻だった — llterm 障害対応の切り分け記録 | #46 `2. ターン境界と緊急割り込みは、最初から別物として設計する / 3. ctx 2549% は「AI が太った」のではなく、計測が壊れていた / 6. テストも「たまたま緑」を疑う` | `published` | 2026-06-18 Team POST 済み。API GET では `private:false` |

## POST 後の記録欄

| slug | item id | Team URL | visible range memo | rollback needed | note |
| --- | --- | --- | --- | --- | --- |
| `team_stock_semantic_governance.md` | `6f67e54e538c10b8f1c3` | `https://fullsense.qiita.com/furuse-kazufumi/items/6f67e54e538c10b8f1c3` | API GET で `private:false`。実ブラウザ範囲は未確認 | conditional | `private:true` frontmatter でも Team create 後は public-like state に見える。rollback は別 human-gate 判断 |
| `team_stock_llm_wiki_anti_circulation.md` | `b35b429dc6dc1fde207a` | `https://fullsense.qiita.com/furuse-kazufumi/items/b35b429dc6dc1fde207a` | API GET で `private:false`。実ブラウザ範囲は未確認 | conditional | `private:true` frontmatter でも Team create 後は public-like state に見える。rollback は別 human-gate 判断 |
| `team_stock_ctx2549_postmortem.md` | `6fe79ab04443f7654eca` | `https://fullsense.qiita.com/furuse-kazufumi/items/6fe79ab04443f7654eca` | API GET で `private:false`。実ブラウザ範囲は未確認 | conditional | `private:true` frontmatter でも Team create 後は public-like state に見える。rollback は別 human-gate 判断 |

## blockers

1. 2026-06-19 時点の `tools/qiita_team_post.py` は `ignorePublish` を読み、`ignorePublish:true` の source は `--force-ignore-publish` 無しでは fail-closed で停止する。したがってこのフラグは「未投稿」を意味せず、Team poster でも明示 override を要する source freeze として扱う
2. 2026-06-18 の API GET では 3 本とも `private:false` で返っており、frontmatter `private:true` は Team create 後の可視範囲を保証しなかった
3. rollback / 可視範囲の絞り込みが必要なら、以後は別の human-gate 外部アクションとして扱う

## 状態更新ルール

- POST 成功後:
  - Queue 表の `status` を `published` に更新する
  - `POST 後の記録欄` に `item id` / Team URL / visible range / rollback needed / note を記入する
  - blockers から解消済み事項を外すか、残る不確実性だけに絞る
- rollback 実施後:
  - Queue 表の `status` を `rollback_applied` に更新する
  - `POST 後の記録欄` の `rollback needed` と `note` に理由・結果を記入する
  - handoff にも 1 行で結果を転記する
