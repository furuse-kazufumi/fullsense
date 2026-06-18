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
| `team_stock_semantic_governance.md` | Semantic Governance は「AI の権限管理」ではなく「AI の意味管理」 | #43 `2-2. loop engineering にもセキュリティの顔がある` | `local_draft / dry_run_ok / blocked_human_gate` | `ignorePublish: true` のまま。実 POST は user GO 待ち |
| `team_stock_llm_wiki_anti_circulation.md` | LLM Wiki の本当の難所は「知識を集めること」ではなく「思考の循環を止めること」 | #43 `3-2. LLM Wiki — 「育つ知識」のパターン` | `local_draft / dry_run_ok / blocked_human_gate` | anti-circulation の境界を公開前に再確認 |
| `team_stock_ctx2549_postmortem.md` | `ctx 2549%` は AI の暴走ではなく人間の計測破綻だった | #46 `2. ターン境界と緊急割り込みは、最初から別物として設計する / 3. ctx 2549% は「AI が太った」のではなく、計測が壊れていた / 6. テストも「たまたま緑」を疑う` | `local_draft / dry_run_ok / blocked_human_gate` | internal logs / evidence snapshot の非公開境界を維持 |

## POST 後の記録欄

| slug | item id | Team URL | visible range memo | rollback needed | note |
| --- | --- | --- | --- | --- | --- |
| `team_stock_semantic_governance.md` |  |  |  |  |  |
| `team_stock_llm_wiki_anti_circulation.md` |  |  |  |  |  |
| `team_stock_ctx2549_postmortem.md` |  |  |  |  |  |

## blockers

1. `tools/qiita_team_post.py` は `ignorePublish` を読まず、`post --yes` でそのまま外部 POST する
2. `private: true` が Qiita Team `fullsense` 上でどの範囲に見えるか、一次情報で十分に確定できていない
3. よって、実行前に human gate で明示確認が必要

## 状態更新ルール

- POST 成功後:
  - Queue 表の `status` を `published` に更新する
  - `POST 後の記録欄` に `item id` / Team URL / visible range / rollback needed / note を記入する
  - blockers から解消済み事項を外すか、残る不確実性だけに絞る
- rollback 実施後:
  - Queue 表の `status` を `rollback_applied` に更新する
  - `POST 後の記録欄` の `rollback needed` と `note` に理由・結果を記入する
  - handoff にも 1 行で結果を転記する
