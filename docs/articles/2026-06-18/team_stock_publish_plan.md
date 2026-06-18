# Team Stock Publish Plan (2026-06-18)

`tools/qiita-cli-poc/public/` に切った Team stock 用 source-only draft を、
後で Qiita Team `fullsense` へ流すときの順番と注意点をまとめる。

## 対象

1. `team_stock_semantic_governance.md`
2. `team_stock_llm_wiki_anti_circulation.md`
3. `team_stock_ctx2549_postmortem.md`

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

1. `tools/qiita_team_post.py` は `ignorePublish: true` を尊重しない
2. `private: true` の Team 上での実効可視範囲は未確定
3. よって、実 POST 前に user GO が必要

## POST 後に追記すること

- 各ファイルの `id`
- Team 上の URL
- visible range について実地でわかったこと
- local draft から public/Team 公開向けに追加した但し書きの有無
