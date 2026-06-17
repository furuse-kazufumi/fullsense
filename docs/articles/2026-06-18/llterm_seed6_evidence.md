# llterm 種 #6 根拠スナップショット (2026-06-18)

対象記事: `docs/articles/2026-06-18/llterm_seed6_article_plan.md`  
元ソース: llterm commit `ff066bdf99db74263f1c6208fa8a671a080bc7fc` の `docs/ARTICLE_SEEDS.md`

## 目的

- 公開直結の具体主張を、`D:/projects/llterm/...` の外部絶対パスに依存せず `fullsense` 側に固定する
- 記事 plan の `13 分` / `ctx 2549%` / `billing 累積値の誤用` / `race 依存の緑` を追跡可能にする

## 固定した根拠

### A. 「13 分待っても返らない」

元メモ要旨:

- orchestra 1 ターンは実時間で **約 13〜18 分**
- そのターン実行中に注入した「進捗を要約できますか？」が、ターン完了境界まで待たされた

出所:

- llterm `ARTICLE_SEEDS.md` の 種 #1「何が起きたか」

記事 plan で使う場所:

- [llterm_seed6_article_plan.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_article_plan.md) の hook / `6-beat through-line` の anomaly / 第1章

### B. 「ctx 2549%」

元メモ要旨:

- ターン完了時の **ctx 使用率が 2549%**
- cache 再読込の重複加算による過大計上
- 毎ターン rotate の直接原因

出所:

- llterm `ARTICLE_SEEDS.md` の 種 #1「何が起きたか」
- 種 #6 原則 2「占有率には物理上限がある」

記事 plan で使う場所:

- [llterm_seed6_article_plan.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_article_plan.md) の hook / complication / 第3章 / 第7章 原則 2 / 第8章

### C. 「billing 累積値を occupancy 制御へ流用」

元メモ要旨:

- billing 用の**累積**トークンを、そのまま文脈占有率へ流用した
- ツール往復で文脈を再送するたび N 倍化し、瞬間 occupancy の意味を失う
- `min(1.0, ...)` のクランプは「物理上限を超えない」のコード化

出所:

- llterm `ARTICLE_SEEDS.md` の 種 #6 原則 2

記事 plan で使う場所:

- [llterm_seed6_article_plan.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_article_plan.md) の 第3章 / 第7章 原則 2

### D. 「自己圧縮する codex に llterm rotate を重ねると二重管理」

元メモ要旨:

- codex は exec resume で自前で文脈圧縮する
- その上から llterm が占有率で rotate を強制すると競合し、1 セッション=1 ターンに縮退する

出所:

- llterm `ARTICLE_SEEDS.md` の 種 #6 原則 3

記事 plan で使う場所:

- [llterm_seed6_article_plan.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_article_plan.md) の complication / 第3章 / 第7章 原則 3

### E. 「race 依存の緑」

元メモ要旨:

- choice→inject テストは実ループをスレッド駆動し、注入キューを直接 assert
- `VirtualClaudeRunner(delay=0.0)` で worker がキューを race 消費
- 出力ログ I/O 追加でレースが顕在化
- `delay>0` で turn 1 に block point を作り決定論化

出所:

- llterm `ARTICLE_SEEDS.md` の 種 #5「事実」

記事 plan で使う場所:

- [llterm_seed6_article_plan.md](/D:/projects/fullsense/docs/articles/2026-06-18/llterm_seed6_article_plan.md) の investigation / 第6章 / 第7章 原則 8

## 運用メモ

- 以後、`llterm_seed6_article_plan.md` で具体数値や失敗モードを書くときは、まずこのスナップショットへリンクする
- 公開本文では、このスナップショットを根拠メモとしつつ、必要なら log / test / code の一次ソースを別付録へ切り出す
