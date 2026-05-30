# Session Summary — 2026-05-29〜30 (llcore S1/S2 + 進化機構監査 + CPU手順1 + 14proj health)

> 次セッション(ccr)の SESSION START 復元用。next_plan の正は claude-projects.json (fullsense)。

## プロジェクト
fullsense (umbrella) — `D:\projects\fullsense` / 主作業 = llcore (`D:\projects\llcore`)

## このセッションの成果 (全て local commit、push 未)

### llcore 本流
- `2e45216` kernel plugin 設計 doc (Codex 5 Findings 反映)
- `9bb2228` **S1**: kernel plugin 3 Protocol (GeneCodec/Trajectory/Kernel/VerifierBackend) + RWKV 準拠例
- `cc0c3c0` **S2**: minimal_ga を GeneCodec で gene 型非依存化 (codec=None は旧 RWKV byte-identical, *_g 追加)
- `f9f1798` 進化機構健全性監査 doc
- `5ee1c13` **CPU 手順1**: 公正な評価+反証ハーネス honest_eval.py + 監査に診断結果追記
- 本流 145→**195 PASS** / research 137+2skip 不変

### 最重要結論 (進化機構監査 + [GA健全性 切り分け診断])
- **llcore は進化機構 PoC としては成立、但し「進化(累積改善)」は未成立。**
- 進化4要件: ①変異②遺伝=成立 / ③選択圧④過剰繁殖=機構あるが空転。
- confound 解明: ③失敗の主因は **landscape の平坦さ** (本番 CopyTask 上位20遺伝子 spread=0.0007)。
  GA 機構は健全 (clean 構造 landscape で δ=+0.97 圧勝)。**但し構造 landscape の勝因も tournament_k=1 で勝つ
  = ③でなく elitism+変異の hill-climbing**。③そのものは未分離。報告 best +0.29 は elitism 凍結 artifact。
- **GPU 判定 = conditional (今は保留、「24GB必要」を修正)**: ノイズ抑制(GPU)では③立たず、実 LLM fitness が
  SNR≥2 構造+spread を持つか未証明 (=GPU 必要十分条件)。RTX 4090 24GB は CPU 手順で「効くと分かる」まで保留。

### 14プロジェクト health review + 低リスク修正 (10 commit)
- llive: Rust target 1095 ファイル追跡解除 / fullsense: gc で .git 4.6GB→42MB / 他 (memory: project_ecosystem_health_review_2026_05_29 に全記録)。残課題は承認制。
- RAD: compiler_corpus_v2=formal_methods 完全複製 (シードミス) / hacker_corpus 正本は repo側 (.claude/skills/corpus/) で健全、D:/docs は部分ミラー(注記済)。

### memory 追加 (応答スタイル等)
- feedback_term_format_jp_en (日本語(English)形式 + 略語初出展開、記事も。**英単語"honest/clean"を生で混ぜない→正直な/きれいな**)
- feedback_workflow_readable_naming ([用途名]で呼ぶ、#はQiita専用、id は <!-- wf:xxx --> で囲む)
- feedback_rotate_proactive_timing / feedback_repoc_when_impl_wrong

## 次にすべきこと (CPU 手順、GPU 前)
1. ~~honest_eval~~ **完了 (5ee1c13)**。**残: honest_eval の codex pair-review** (additive+tested で commit 先行した)
2. **[次の主作業] CPU 手順2**: fixed readout → per-gene least-squares(ridge, held-out) 置換を本番 fitness に配線
   (landscape un-flatten、診断 #3 が選択を殺す最大要因と実証)。honest_eval.evolution_vs_random で効果測定。
3. CPU 手順3: ③を hill-climbing から分離測定 (本番 readout で tournament_k sweep + elitism=0)
4. 手順4: 探索空間拡張 + 分離(QD/niching: LineageReservoir/ModesMeter を load-bearing 化) 5: addition 追試 6: 小型LLMで実proxy構造 sanity
- ③確立=分離機構+構造ある空間のセット (集団内 niching、大量プロセス不要)。
- audit=`docs/poc/EVOLUTION_SOUNDNESS_AUDIT_2026-05-30.md`。push 状態: llcore ローカル多数 commit 保持。
