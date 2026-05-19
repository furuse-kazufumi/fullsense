---
layout: default
title: "Articles — 2026-05-20"
nav_order: 68
---

# FullSense — 2026-05-20 articles index

> 2026-05-14 から保留していた投稿用記事 pause を **2026-05-20 解除**.
> 用途は「投稿候補 + ユーザーの進捗把握源」. 投稿判断はユーザー.
>
> セッション内容: 15 時間自律ループ goal を受けた前半サイクル. portal
> NEXT_SESSION 自動化 + research hub 6 件 + 3 prj test 回帰 fix + lleval
> HIGH 採用優先度確定 + lleval v0.1 draft 要件.

## 当日の柱 3 本

| # | タイトル | テーマ | 主要対象 |
|---|---|---|---|
| 20 | [1 セッションで 5409 テスト緑緑緑にして research hub 6 本開いた話](./QIITA_20_one_session_full_stack_progress.md) | 進捗ダイジェスト / 全 stack 整備 | FullSense フォロワー / 個人 OSS 開発者 |
| 21 | [テストが朝起きたら 7 件死んでいた件 — WinGet で chafa が来た](./QIITA_21_env_dependent_tests_chafa_lesson.md) | TIL / 環境依存 test の脆さ / monkeypatch パターン | テスト書く全プログラマ |
| 22 | [AI agent 6 体並列に走らせて spinoff 採用優先度を 30 分で決めた話](./QIITA_22_ai_parallel_research_priority_decision.md) | AI workflow / 採用優先度判定 / agent dispatch | 設計判断に AI を使う人 |

## 一文サマリ (RT 用)

- **#20**: 朝起きたら test 7 件死んでた → 直す → AI 6 体で先行研究調査 →
  spinoff 採用優先度を決定 → portal NEXT_SESSION 自動化 → 全 push.
  1 セッションで縦 (test) も横 (research) も両方詰めた話.
- **#21**: WinGet が `chafa.exe` を勝手に PATH に乗せただけで, llove の
  ASCII fallback test が 7 件死亡. 環境依存 test の正しい monkeypatch
  パターン.
- **#22**: 採用優先度を「会議室で議論」じゃなくて「AI 6 体に並列で先行研究
  調査させて 30 分で報告書 6 件」で決めた話. lleval=HIGH を 800 字 × 6 件で
  根拠化.

## 関連 docs

- [research hub]({{ '/research/' | relative_url }}) — 今日生成した 6 件の SOTA / prior-art メモ
- [spinoff_ideas_2026_05]({{ '/spinoff_ideas_2026_05' | relative_url }}) — C-2 採用優先度表 (lleval=HIGH 等)
- [requirements_lleval_v0.1_draft]({{ '/spec/requirements_lleval_v0.1_draft' | relative_url }}) — agent 自律ドラフト
- [NEXT_SESSION 手書き版]({{ '/NEXT_SESSION' | relative_url }})
- [NEXT_SESSION 自動生成版]({{ '/NEXT_SESSION.auto' | relative_url }}) (新規, Stop hook 連動)
