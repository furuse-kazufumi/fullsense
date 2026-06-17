# Next Plan

最終更新: 2026-06-18

## 現在地

- Qiita 草稿と handoff 文書の整合調整は commit `bab1557` で一段落した。
- 現在の worktree 差分は 9 ファイル。
  - `.llterm/loop_ledger.jsonl` の tracked ノイズ
  - commit `bab1557` 後に加えた `docs/SESSION_SUMMARY.md` / `docs/next_plan.md` / `qiita43_harness_loop_stack.md` / `qiita43_harness_loop_stack_en.md` / `qiita43_harness_loop_stack_kamikudaki.md` / `qiita43_harness_loop_stack_ko.md` / `qiita43_harness_loop_stack_zh.md` / `qiita44_evolutionary_programs_block_diagram.md`
- `.llterm/loop_ledger.jsonl` は **未 restore** で、tracked ノイズ差分が worktree に残っている。
- handoff 3 文書（`docs/NEXT_SESSION.md` / `docs/SESSION_SUMMARY.md` / `docs/next_plan.md`）は上記 commit に含めた。
- 外部公開・push は未実施。

## 次の具体的な一手

1. publish gate 用の別バッチとして、#43 en/zh/ko の translation drift を優先して詰める。
2. #43 en/zh/ko は「ローカル草稿整合」ではなく、**発行済み限定共有 draft の同期凍結**として扱う。live URL は残ったままなので、translation drift 解消を優先する。
3. `.llterm/loop_ledger.jsonl` は次の commit に混ぜない。必要なら restore するか、恒久対策を別判断する。
4. push / publish / 外部書き込みは引き続き human gate のまま維持する。

## このターンの実施結果

- `docs: sync qiita draft handoff for articles 43-45` を commit `bab1557` として作成した。
- commit 対象は handoff 3 文書、`FULLSENSE_KB_INDEX.md`、`IDEAS_2026_06_15_harness_loop_raptor.md`、Qiita 草稿 6 ファイルの計 11 ファイル。
- en/zh/ko の変更は本文改稿ではなく `ignorePublish: true` への切替だが、`id:` を持つ発行済み限定共有 draft の **同期凍結**であって、公開面の drift が消えるわけではない。
- `.llterm/loop_ledger.jsonl` は commit に含めていない。

## publish gate 送り

- `qiita44` は参考文献節へ canonical 入口を追加済み。
  - GA / ES / GP / NEAT / novelty search / MAP-Elites / CMA-ME の代表文献を最低 1 本ずつ置いた。
  - 残りは URL 明記をどこまで入れるか、lexicase まで補うかの粒度調整。
- `qiita43_harness_loop_stack_kamikudaki.md` は ☕ 休憩ポイントと参考文献節を追加済み。
  - ただし完全版 #43 への導線を優先した短縮版のため、一次情報の細目は引き続き完全版側へ寄せる。
- #43 en/zh/ko は発行済み限定共有 draft の translation drift を解消してから `ignorePublish: false` に戻す。

## 次回の開始メモ

- 新規の設計・実装・調査へ進む前に、必要な論点があれば RAD コーパスを grep して先行手法を確認する。
- publish gate は着手済みで、`qiita44` の参考文献補強は RAD 接地後に着手した。
- `kamikudaki` の ☕ / 参考文献は最小補強まで完了した。
- #43 en/zh/ko では、終盤 hedged note の RAD 件数を `47,097 docs` へ更新済み。
- 次は #43 en/zh/ko の残りの translation drift を詰める。

## 注意

- `ignorePublish: true` / `private: true` は `qiita-cli-poc` ローカル運用の安全柵。既発行の限定共有 URL を撤回するものではない。
- `docs/SESSION_SUMMARY.md` は通常 Stop hook に上書きされるため、必要な恒久メモは `NEXT_SESSION.md` と本ファイルを優先する。
