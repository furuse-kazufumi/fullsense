---
layout: default
title: "Mythos 超え — 機構実証と gap の honest 中間報告 (2026-05-28)"
nav_order: 38
---

# Mythos 超え — 機構実証と gap の honest 中間報告 (2026-05-28)

> ゴール = **進化型オーケストラ + RAPTOR 決定論オラクル + 無制限 test-time compute** で
> Claude Mythos をセキュリティ領域で超える/到達する（速度不問・on-prem only）。
> 本稿は設計正本（[Mythos 超え 設計正本]({{ '/research/mythos_surpass_design_2026_05_27' | relative_url }})）に対する
> **実証の中間報告**で、何が「実機で実証済」「mock 検証のみ」「反証された」かを honest に切り分ける
> ([[feedback_benchmark_honest_disclosure]] 準拠)。

## 1. 収束アーキ（おさらい）

- **生成 = カバレッジ**: llive 進化オーケストラ（lldarwin v2 = ε-lexicase + novelty + 中立貯蔵庫）が多様な解候補を大量生成。
- **検証 = precision**: RAPTOR の **決定論オラクル**（flag 一致 / exploit 成立 / crash 再現 / ASan・UBSan）が「効く 1 答」を機械判定。
- **試行 = 無制限**: speed 不問 → test-time compute 青天井で弱モデル群をフロンティア級へ押し上げる。
- **核心 honest**: 決定論オラクルは **verifier-Goodhart を構造的に回避**する（汎用推論ベンチとの本質差）。セキュリティは flag/exploit が ground-truth = 最適アリーナ。

## 2. 機構連鎖の実証マトリクス（honest 切り分け）

| 段 | 命題 | 結果 | 種別 |
|---|---|---|---|
| PoC-CTF-0 | 決定論オラクル coverage@k harness | 動作。**均等多様化は単一強モデルに負ける**（盲点ターゲット配分が要る） | mock + 一部 real |
| PoC-CTF-1 | ε-lexicase 進化集団=奏者アンサンブルが単一/均等 diverse を上回る | evolved 1.000 > 単一最強 0.800 > gen0 均等 0.900 | **mock 検証のみ** |
| cross-family 脱相関 | 別モデル族は盲点が脱相関し集団 coverage が上がる | **反証**: 全 on-prem が同じ盲点を共有（真の entanglement）。mock の +0.400 は合成 artifact | **実機で破綻** |
| PoC-CTF-2 | tool-exec（コード生成→sandbox 実行→オラクル）が no-tool を上回る | qwen2.5:14b で no_tool 0.625 → **tool_exec 0.875**, blind-spot 反転 | **実機 ✓** |
| PoC-CTF-3 | agentic 戦略（code/direct）を ε-lexicase が進化 | evolved 0.875 vs direct-only 0.500 | mock + 要所 real |
| Phase D-1 | 実 CTF (InterCode-CTF) を multi-turn 自律で前進 | no_tool 0.429 → **multi-turn 0.571 → +self-check 0.714** | **実機 ✓** |
| 進化 × multi-turn | 観察先行 specialist を進化が保ち naive を上回る | evolved 1.000 vs naive 0.571 | **mock 検証のみ** |

**読み筋**: レバーは「モデル族の多様性」**ではなく**「agentic code-execution + multi-turn 自律性」だと実機で同定された。Mythos が CTF を制すのは agentic 実行能力。我々の弱モデルは「頭の中で解いて外す」が、コード実行 + 観察ループ + 決定論オラクルで reasoning-execution gap を埋められる。

## 3. 現在地と gap-to-Mythos

- **実機ベスト** = qwen2.5:14b, multi-turn + self-check gate, easy picoCTF **5/7 (0.714)**。
- **Mythos** = Cybench pass@1 **100%**。
- → **依然遠い**。easy picoCTF の polish はゴールに直結しない（honest）。本丸 = Cybench 多段 exploitation 正対。

## 4. 🔴 律速＝計算資源（ハードウェア gated）

実機フル進化ラン = pop × gens × task × turn × **~88s/call（CPU 推論）** = 数万秒 → CPU では非現実的。
**GPU が必須だが現状ラップトップ環境で不可＝新 PC 購入が前提**（2026-05-28 ユーザー確認）。
よって本丸の実機進化スケール + Cybench 正対は **ハードウェア確保まで棚上げ**。

## 5. honest な結論（負けを消さない）

1. **機構は健全で GPU-ready**: coverage harness → ε-lexicase 集団 → tool-exec レバー（real ✓）→ multi-turn 自律（real ✓）→ agentic 戦略進化（mock ✓）の連鎖は実証済。GPU 確保後すぐ回せる状態。
2. **Mythos 正面超えは現時点で困難**: ハードウェア律速 + gap が大きい。これを誇張しない。
3. **研究貢献は Mythos 超え可否と独立に成立**: 「**進化型アルゴリズムが、検証可能なセキュリティタスクで、弱い on-prem モデルをベースライン超えさせる**」機構を、決定論オラクル（verifier-Goodhart 回避）の上で実証したこと自体に価値がある。

## 6. 次の一手

- **CPU で可能（genuine progress）**: 機構ハードニング — no_action retry-nudge / binary 観察 sanitize（着地済）/ parse_action 頑健化 / 多段 persistent-session の scaffold。実機予言ではない mock 検証で機構を固め GPU-ready を維持。
- **GPU 確保後（hardware-gated）**: 実 LLM 進化スケール（pop 256→4096）/ persistent-session 多段 exploitation / Cybench 正対で公開 100% と実測対決。

---

関連: [Mythos 超え 設計正本]({{ '/research/mythos_surpass_design_2026_05_27' | relative_url }}) / [Mythos 競合スペック台帳]({{ '/research/mythos_competitor_spec_2026_05_27' | relative_url }}) / memory `goal_surpass_mythos_evolutionary` / `project_lldarwin`。
