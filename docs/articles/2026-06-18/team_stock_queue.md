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
  - 追加で、poster payload 側では当時 `group_url_name` を送っていなかった。`group.url_name: general` / `group.private:false` の観測は、implicit General sharing が起きた可能性を示す **現時点の仮説**として扱う

## blockers

1. 2026-06-19 時点の `tools/qiita_team_post.py` は `ignorePublish` を読み、`ignorePublish:true` の source は `--force-ignore-publish` 無しでは fail-closed で停止する。したがってこのフラグは「未投稿」を意味せず、Team poster でも明示 override を要する source freeze として扱う
2. 2026-06-18 の API GET では 3 本とも `private:false` で返っており、frontmatter `private:true` は Team create 後の可視範囲を保証しなかった
3. 2026-06-19 の未認証 HTML GET では 3 本とも Login ページへ落ちたが、これは Team サブドメイン全体の auth gate でも説明できる。したがって team-only と positively 確認できるまでは **過剰露出の疑いを優先**し、`private:false` の意味づけは一次情報待ちとする
4. current blocker の主語は「Team API / visibility semantics（プロジェクト内用語）の不一致」ではなく、**過剰露出の疑いを否定できないこと**に置く。不一致は副次論点として記録する
5. 2026-06-19 以降の Team create は、poster が `group_url_name` を明示しないまま implicit share target に依存しないよう fail-closed 化済みで、local source 3 本にも `group_url_name: general` を固定した
6. rollback / 可視範囲の絞り込みが必要なら、以後は別の human-gate 外部アクションとして扱う

## 状態更新ルール

- POST 成功後:
  - Queue 表の `status` を `published` に更新する
  - `POST 後の記録欄` に `item id` / Team URL / visible range / rollback needed / note を記入する
  - blockers から解消済み事項を外すか、残る不確実性だけに絞る
- rollback 実施後:
  - Queue 表の `status` を `rollback_applied` に更新する
  - `POST 後の記録欄` の `rollback needed` と `note` に理由・結果を記入する
  - handoff にも 1 行で結果を転記する
