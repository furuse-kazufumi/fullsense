# Next Plan

最終更新: 2026-06-18

## 現在地

- Qiita 草稿と handoff 文書の整合調整が一段落している。
- staged 差分は 11 ファイル。
- `.llterm/loop_ledger.jsonl` は **未 restore** で、tracked ノイズ差分が worktree に残っている。
- handoff 3 文書（`docs/NEXT_SESSION.md` / `docs/SESSION_SUMMARY.md` / `docs/next_plan.md`）は今回の doc batch に含めて staged 済み。
- 外部公開・push・commit は未実施。

## 次の具体的な一手

1. staged 11 ファイルは **1 本の doc batch として維持**する。
2. バッチの意味は「#43 派生草稿 / #44 / #45 の本文整備」と「その再開導線を handoff / KB / ideas に同期」の 2 層で、内容は同一テーマ内に収まっている。
3. #43 en/zh/ko は「ローカル草稿整合」ではなく、**発行済み限定共有 draft の同期凍結**として扱う。live URL は残ったままなので、translation drift 解消を publish gate に明記する。
4. publish 前 gate（URL/著者帰属/translation drift/raw asset 200、`qiita44` 一次文献補強、`kamikudaki` の短縮版要素確認）は **別バッチに分離**し、この commit には混ぜない。

## このターンの判断

- `git diff --cached --stat` は **11 ファイル / 1909 insertions / 76 deletions**。index には handoff 3 文書、`FULLSENSE_KB_INDEX.md`、`IDEAS_2026_06_15_harness_loop_raptor.md`、Qiita 草稿 6 ファイルが載っている。
- `docs/NEXT_SESSION.md` が草稿の状態・安全柵・残タスクを説明し、`FULLSENSE_KB_INDEX.md` と `IDEAS_2026_06_15_harness_loop_raptor.md` が同じ状態へ追従しているため、文書側だけ切り出すと handoff が嘘になる。
- en/zh/ko の変更は本文改稿ではなく `ignorePublish: true` への切替だが、`id:` を持つ発行済み限定共有 draft の **同期凍結**であって、公開面の drift が消えるわけではない。
- `.llterm/loop_ledger.jsonl` は `git add .` 系で巻き込みうるため、restore するか commit 対象外として明示したまま扱う必要がある。

## publish gate 送り

- `qiita44` は参考文献節が系統名整理の水準なので、GA / ES / GP / MAP-Elites など各流派の一次文献を最低 1 本ずつ補う。
- `qiita43_harness_loop_stack_kamikudaki.md` は短縮版草稿として ☕ 休憩ポイントと参考文献節をまだ省略している。公開線へ回す前に、意図的省略のまま行くか追補するかを決める。
- #43 en/zh/ko は発行済み限定共有 draft の translation drift を解消してから `ignorePublish: false` に戻す。

## commit メッセージ案

- `docs: sync qiita draft handoff for articles 43-45`
- `docs: add qiita 43 companion drafts and handoff updates`
- `docs: align handoff with qiita 43-45 draft batch`

## 注意

- `ignorePublish: true` / `private: true` は `qiita-cli-poc` ローカル運用の安全柵。既発行の限定共有 URL を撤回するものではない。
- `docs/SESSION_SUMMARY.md` は通常 Stop hook に上書きされるため、必要な恒久メモは `NEXT_SESSION.md` と本ファイルを優先する。
