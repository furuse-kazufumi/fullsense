# Next Plan

最終更新: 2026-06-18

## 現在地

- Qiita 草稿と handoff 文書の整合調整は commit `bab1557` / `e4e3968` / `7e7931c` / `0478fa1` / `426be90` / `e942370` / `496ca41` / `fded95b` / `e0b0ee5` / `7ce6ee1` / `31e974e` / `e871b12` / `23998cd` / `ed0159a` / `ed1caab` / `cdcc389` / `2f92ee2` / `7f82f6e` / `85eb5e3` / `521d318` まで反映済み。
- 現在の worktree 差分は `.llterm/loop_ledger.jsonl` の tracked ノイズだけ。
- `.llterm/loop_ledger.jsonl` は **未 restore** で、tracked ノイズ差分が worktree に残っている。
- handoff 3 文書（`docs/NEXT_SESSION.md` / `docs/SESSION_SUMMARY.md` / `docs/next_plan.md`）は上記 commit 群に含めた。
- 外部公開・push は未実施。

## 次の具体的な一手

1. publish gate 用の別バッチとして、#43 en/zh/ko のうち既に spot-check 済みの 冒頭〜第1章前寄り / 第1章前半 / 第1章後半〜第2章冒頭 / 第2章前半の `llloop` 導入〜 MAPE-K 骨格 / 第2章中盤（安全層〜`/goal`）/ 「捨てた数字」の独立 honest disclosure 節 / `47,097 docs` honest-disclosure 節 / `50手法 vs 96ノート` / 第3章後半（RAD 運用ルール〜統合章）/ `LLM Wiki / thought circulation` / 統合章〜結語 を除く未確認箇所の factual / translation drift を優先して詰める。
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
- `docs: clarify article 43 factual audit scope` を commit `e871b12` として作成した。
- `docs: record article 43 hedge retention audit` を commit `23998cd` として作成した。
- `docs: note review handoff process follow-ups` を commit `ed0159a` として作成した。
- `docs: narrow article 43 remaining audit scope` を commit `ed1caab` として作成した。
- `docs: sync next session handoff for article 43 drift` を commit `cdcc389` として作成した。
- `docs: record article 43 harness audit` を commit `2f92ee2` として作成した。
- `docs: narrow article 43 early-section audit scope` を commit `7f82f6e` として作成した。
- `docs: record article 43 control-loop audit` を commit `85eb5e3` として作成した。
- `docs: record article 43 terminology audit` を commit `521d318` として作成した。
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
  - `47,097 docs` honest-disclosure 節と直後の橋渡し段は局所確認済みで、日本語正本に大筋追従している。
  - `50手法 vs 96ノート` 節も局所確認済みで、96ノート / 39 documents / 12 clusters の注意書きまで日本語正本に追従している。
    - ここで確認したのは数値そのものの正当性ではなく、日本語正本に対する訳文追従である。
  - `LLM Wiki / thought circulation` 節も局所確認済みで、Anti-Circulation Safeguards の箇条書きと `llmesh / llive / llove` の製品対応づけまで日本語正本に追従している。
    - ここで確認したのは日本語正本に対する訳文追従であり、`Anti-Circulation Safeguards` / `thought circulation` / `RAD` の外部一次情報ベースの factual 検証ではない。
  - 追加 spot-check で、Karpathy 帰属のヘッジ語、`llive` 設計段階の限定句、製品対応づけの「私のマッピング」表現が en/zh/ko で保持されていることも確認済み。
  - 統合章〜結語も局所確認済みで、A/B/C 統合表、`手綱 / 輪 / 知` の3点整理、`Bölük 10×` を捨てた設計思想、次回予告の `設計段階` ヘッジまで日本語正本に追従している。
  - 第1章前半（`harness engineering` 命名経緯 / `vibe coding` 区別 / RAPTOR 2層 / `ハーネス型バイブコーディング` 説明）も局所確認済みで、Hashimoto/OpenAI まわりのヘッジ、Karpathy との差異、fail-closed の説明、ユーザー側3能力の導入まで日本語正本に追従している。
  - 第1章後半〜第2章冒頭（ユーザー側3能力 / AI成長マネジメント / anti-pattern / `loop engineering` 定義 / `Semantic Governance` 導入 / `llloop` honest disclosure）も局所確認済みで、比喩・留保・戦略説明まで日本語正本に追従している。
  - 第2章前半の `llloop` 導入〜 MAPE-K 骨格も局所確認済みで、alpha 段階の honest disclosure、`MapeKRunner` の閉ループ、plan-execute-verify / Reflexion、体温調節の比喩まで日本語正本に追従している。
  - 第2章中盤（`fail-closed` 安全層 / `現状の実装では` の条件付き留保 / `green-keeper` / `/goal`）も局所確認済みで、SafetyPolicy の 3 段判定、CircuitBreaker / Budget / 認証要求検知、`Executor` 条件付きの honest disclosure、GitOps reconciliation 比喩、`Haiku` 既定の `/goal` 説明まで日本語正本に追従している。
    - ここで確認したのは主に日本語正本に対する訳文追従であり、Claude Code `/goal` docs の外部一次情報ベース再検証をこのターンで追加実施したわけではない。
  - 冒頭〜第1章前寄り（捨てた数字の導入 / `prompt → context → harness → loop` の階段 / automation と loop の差分 / Hashimoto 起点の `harness engineering` / OpenAI 403 に伴う二次情報ヘッジ / RAPTOR 二層構造の導入）も局所確認済みで、一次情報アンカー・二次情報ヘッジ・`Agent = Model + Harness` の注意書きまで日本語正本に追従している。
    - ここでも確認したのは主に日本語正本に対する訳文追従であり、Hashimoto/OpenAI/Karpathy/RAPTOR の一次情報を各翻訳ターンで再取得したわけではない。
  - 「捨てた数字」の独立 honest disclosure 節も局所確認済みで、arXiv `2605.18747` / `2605.27922` / `2605.26112`、`Bölük 10x` 否定、`GPT-5.5` 要検証、一次と二次の線引きまで日本語正本に追従している。
    - ここでも確認したのは主に日本語正本に対する訳文追従であり、各論文やベンチの一次ページをこの翻訳監査ターンで再取得したわけではない。
  - 第3章後半（RAD の運用ルール / `LLM Wiki` の 3 層 / thought circulation と Anti-Circulation Safeguards / RAPTOR の evidence ladder / `corpus-first advantage` / 統合章の A-B-C 表）も局所確認済みで、K² サイジング、`rad_prune.py` の dry-run、`39 documents / 12 clusters` 注記、llive の主観マッピング、`suspicion → patch_validated` の証拠段階、`47,097 docs` を含む統合表まで日本語正本に追従している。
    - ここでも確認したのは主に日本語正本に対する訳文追従であり、Karpathy Gist / llive 要件 / RAPTOR 実装の一次情報をこの翻訳監査ターンで再取得したわけではない。
  - 残っているのは、それ以外の未確認箇所にある細い factual / translation drift。

## 次回の開始メモ

- 新規の設計・実装・調査へ進む前に、必要な論点があれば RAD コーパスを grep して先行手法を確認する。
- publish gate は着手済みで、`qiita44` の参考文献補強は RAD 接地後に着手した。
- `kamikudaki` の ☕ / 参考文献は最小補強まで完了した。
- #43 en/zh/ko では、終盤 hedged note の RAD 件数を `47,097 docs` へ更新済み。
- #43 JA 正本の hedge note も `47,097 docs` ベースへ更新済み。
- 次は #43 en/zh/ko のうち、既に spot-check 済みの 冒頭〜第1章前寄り / 第1章前半 / 第1章後半〜第2章冒頭 / 第2章前半の `llloop` 導入〜 MAPE-K 骨格 / 第2章中盤（安全層〜`/goal`）/ 「捨てた数字」の独立 honest disclosure 節 / `47,097 docs` honest-disclosure 節 / `50手法 vs 96ノート` / 第3章後半（RAD 運用ルール〜統合章）/ `LLM Wiki / thought circulation` / 統合章〜結語 を除く未確認箇所の factual / translation drift を詰める。

## 注意

- `ignorePublish: true` / `private: true` は `qiita-cli-poc` ローカル運用の安全柵。既発行の限定共有 URL を撤回するものではない。
- `docs/SESSION_SUMMARY.md` は通常 Stop hook に上書きされるため、必要な恒久メモは `NEXT_SESSION.md` と本ファイルを優先する。
