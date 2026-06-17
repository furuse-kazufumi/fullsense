# Next Plan

最終更新: 2026-06-18

## 現在地

- Qiita 草稿と handoff 文書の整合調整は commit `bab1557` / `e4e3968` / `7e7931c` / `0478fa1` / `426be90` / `e942370` / `496ca41` / `fded95b` / `e0b0ee5` / `7ce6ee1` / `31e974e` まで反映済み。
- 現在の worktree 差分は `.llterm/loop_ledger.jsonl` の tracked ノイズだけ。
- `.llterm/loop_ledger.jsonl` は **未 restore** で、tracked ノイズ差分が worktree に残っている。
- handoff 3 文書（`docs/NEXT_SESSION.md` / `docs/SESSION_SUMMARY.md` / `docs/next_plan.md`）は上記 commit 群に含めた。
- 外部公開・push は未実施。

## 次の具体的な一手

1. publish gate 用の別バッチとして、#43 en/zh/ko のうち「約49k件」節と直後の橋渡し段、`50手法 vs 96ノート` 節、`LLM Wiki / thought circulation` 節の訳文追従確認済み部分を除く未確認箇所の factual / translation drift を優先して詰める。
2. #43 en/zh/ko は「ローカル草稿整合」ではなく、**発行済み限定共有 draft の同期凍結**として扱う。live URL は残ったままなので、translation drift 解消を優先する。
3. `loop_ledger` 恒久対策: `git rm --cached .llterm/loop_ledger.jsonl` + `.gitignore` 追記。human gate 解除待ちだが、次の安全な区切りで早めに上程する。
4. handoff commit では `git add .` を使わず、対象 docs の名指し add に固定する。
5. push / publish / 外部書き込みは引き続き human gate のまま維持する。
6. レビュー依頼時は `.llterm/loop_ledger.jsonl` の未 commit ノイズ diff ではなく、対象 commit の `git show` を提示して docs 差分を分離する。
7. 外部公開フェーズで audit 系語を使う場合は、records-retention 監査との誤読を避けるため定義を添える。

## このターンの実施結果

- `docs: sync qiita draft handoff for articles 43-45` を commit `bab1557` として作成した。
- `docs: tighten publish-gate notes for qiita drafts` を commit `e4e3968` として作成した。
- `docs: refresh handoff after publish-gate cleanup` を commit `7e7931c` として作成した。
- `docs: sync handoff with article 43 drift fixes` を commit `0478fa1` として作成した。
- `docs: refresh handoff after latest drift sync` を commit `426be90` として作成した。
- `docs: fix handoff evidence for article 43 drift` を commit `e942370` として作成した。
- `docs: refresh handoff after article 43 audit` を commit `496ca41` として作成した。
- `docs: clarify handoff risk and next scope` を commit `fded95b` として作成した。
- `docs: narrow article 43 drift scope` を commit `e0b0ee5` として作成した。
- `docs: tighten handoff scope wording` を commit `7ce6ee1` として作成した。
- `docs: record article 43 llm wiki audit` を commit `31e974e` として作成した。
- `e4e3968` では #43 多言語 draft の RAD 件数 drift、`kamikudaki` の最小補強、`qiita44` の参考文献訂正、handoff の stale 記述を整えた。
- `0478fa1` では #43 JA 正本の hedge note と `NEXT_SESSION.md` の stale 記述を、ローカル source / live URL の差も含めて整えた。
- `426be90` では handoff 2 ファイルを最新の commit 列まで追従させたが、その後の factual 反転確認ぶんで handoff 2 文書に再度更新が入っている。
- `e942370` では #43 en/zh/ko の honest-disclosure 節の実在根拠を handoff に明記し、`git add .` で `loop_ledger` を再ステージしない個別 add 方針を足した。
- `496ca41` は `git show` で spot-check し、handoff 2 文書だけの更新であることを確認済み。
- en/zh/ko の変更は `ignorePublish: true` への切替だけでなく、終盤 hedge note / 要約表 / 結論部の `47,097 docs` 反映まで含む本文改稿である。
- `.llterm/loop_ledger.jsonl` はどちらの commit にも含めていない。
  - 当面は `git add docs/SESSION_SUMMARY.md docs/next_plan.md` のような個別 add を使い、`git add .` で ledger を再ステージしない。

## publish gate 送り

- `qiita44` は参考文献節へ canonical 入口を追加済み。
  - GA / ES / GP / NEAT / novelty search / MAP-Elites / CMA-ME の代表文献を最低 1 本ずつ置いた。
  - 残りは URL 明記をどこまで入れるか、lexicase まで補うかの粒度調整。
- `qiita43_harness_loop_stack_kamikudaki.md` は ☕ 休憩ポイントと参考文献節を追加済み。
  - ただし完全版 #43 への導線を優先した短縮版のため、一次情報の細目は引き続き完全版側へ寄せる。
- #43 en/zh/ko は発行済み限定共有 draft の translation drift を解消してから `ignorePublish: false` に戻す。
  - `47,097 docs` ベースの factual drift 修正は **ローカル source 側のみ** で、live URL はまだ旧表現を残している。
  - en/zh/ko とも対応する honest-disclosure 節は実在している。
    - 根拠: en `qiita43_harness_loop_stack_en.md` の `#### honest disclosure (Handling the "About 49k Items" Number)`、zh `qiita43_harness_loop_stack_zh.md` の `#### honest disclosure（关于「约49k件」这个数字的处理）`、ko `qiita43_harness_loop_stack_ko.md` の `#### honest disclosure("약 49k건"이라는 숫자의 취급)`。
  - 「約49k件」節と直後の橋渡し段は局所確認済みで、日本語正本に大筋追従している。
  - `50手法 vs 96ノート` 節も局所確認済みで、96ノート / 39 documents / 12 clusters の注意書きまで日本語正本に追従している。
    - ここで確認したのは数値そのものの正当性ではなく、日本語正本に対する訳文追従である。
  - `LLM Wiki / thought circulation` 節も局所確認済みで、Anti-Circulation Safeguards の箇条書きと `llmesh / llive / llove` の製品対応づけまで日本語正本に追従している。
    - ここで確認したのは日本語正本に対する訳文追従であり、`Anti-Circulation Safeguards` / `thought circulation` / `RAD` の外部一次情報ベースの factual 検証ではない。
  - 追加 spot-check で、Karpathy 帰属のヘッジ語、`llive` 設計段階の限定句、製品対応づけの「私のマッピング」表現が en/zh/ko で保持されていることも確認済み。
  - 残っているのは、それ以外の未確認箇所にある細い factual / translation drift。

## 次回の開始メモ

- 新規の設計・実装・調査へ進む前に、必要な論点があれば RAD コーパスを grep して先行手法を確認する。
- publish gate は着手済みで、`qiita44` の参考文献補強は RAD 接地後に着手した。
- `kamikudaki` の ☕ / 参考文献は最小補強まで完了した。
- #43 en/zh/ko では、終盤 hedged note の RAD 件数を `47,097 docs` へ更新済み。
- #43 JA 正本の hedge note も `47,097 docs` ベースへ更新済み。
- 次は #43 en/zh/ko のうち、「約49k件」節と直後の橋渡し段、`50手法 vs 96ノート` 節、`LLM Wiki / thought circulation` 節の訳文追従確認済み部分を除く未確認箇所の factual / translation drift を詰める。

## 注意

- `ignorePublish: true` / `private: true` は `qiita-cli-poc` ローカル運用の安全柵。既発行の限定共有 URL を撤回するものではない。
- `docs/SESSION_SUMMARY.md` は通常 Stop hook に上書きされるため、必要な恒久メモは `NEXT_SESSION.md` と本ファイルを優先する。
