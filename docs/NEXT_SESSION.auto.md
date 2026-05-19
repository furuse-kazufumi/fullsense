---
layout: default
title: "Next Session (auto-generated)"
nav_order: 94
---

# Next Session — auto-generated snapshot

> このファイルは Stop hook (`scripts/gen_next_session_auto.py`) が
> 毎ターン自動上書きします. **手動編集は失われます**.
> 永続化したい内容は [`NEXT_SESSION.md`]({{ '/NEXT_SESSION' | relative_url }}) 側に書いてください.

- **生成時刻**: 2026-05-20 07:43:28
- **生成元**: `scripts/gen_next_session_auto.py` (RAPTOR Stop hook)


## 1. portal git snapshot

- ブランチ: `main`
- HEAD vs upstream (左=ahead 右=behind): `0	0`

```
b3e4841 docs(spec): lleval v0.1 draft 要件 (採用優先度 HIGH, agent ドラフト)
14df788 docs(next-session): 2026-05-20 朝セッション追記 (NEXT_SESSION 自動化 + research hub + test 回帰 fix)
167d1b6 docs(research): index.md に llcraft / llrisk / llgov を追加 (6 件揃い)
502a8fb auto: index.md 編集前 (2026-05-20 07:22)
d39ea84 auto: spinoff_ideas_2026_05.md 編集前 (2026-05-20 07:21)
c156012 auto: spinoff_ideas_2026_05.md 編集前 (2026-05-20 07:21)
12cc15f docs(research): research hub 新設 + 5 件 SOTA メモ + spinoff 優先度反映 + 関連 prj test 回帰 fix を反映
3105c87 auto: PROGRESS.md 編集前 (2026-05-20 07:14)
76d83d9 auto: spinoff_ideas_2026_05.md 編集前 (2026-05-20 07:04)
d1ebeef auto: spinoff_ideas_2026_05.md 編集前 (2026-05-20 06:46)
```

### git status (porcelain)

```
M docs/NEXT_SESSION.auto.md
 M docs/SESSION_SUMMARY.md
```


## 2. 関連プロジェクト最新状態

| project | 最新 commit | 直近 commit msg | tests/ 直近 mtime |
|---|---|---|---|
| llive | `17e63bb 2026-05-20` | docs(qiita): 2026-05-19 記事 2 draft — 個人 OSS の市場受容性 SWOT + 生存戦略 | 2026-05-19 12:45 |
| llove | `4396f64 2026-05-20` | fix(tests): environment-dependent image-tool detection を抑止 | 2026-05-20 07:07 |
| llmesh | `21edb8d 2026-05-20` | test(conftest): hypothesis profile 'local-flaky-safe' で deadline=None を default に | 2026-05-20 07:23 |
| lldesign | `1014ce3 2026-05-19` | docs(pages): FullSense portal hub への参照を docs/index.md にも追加 | 2026-05-16 17:52 |
| lltrade | `d20876c 2026-05-19` | docs(pages): FullSense portal hub への参照を docs/index.md にも追加 | 2026-05-16 17:56 |


## 3. 未消化 operator action (NEXT_SESSION.md 由来)

- [ ] 1. Credential restoration — 3 cloud LLMs (継続)
- [ ] 2. asciinema 録画 — Cognitive Mesh 統合 demo (9 セクション拡張版)
- [ ] 3. PAT rotation (継続)

_本セクションは `NEXT_SESSION.md` の 🧑 見出し配下を毎ターン再抽出したものです.
 消化判定は手動で `NEXT_SESSION.md` 側を編集してください._


## 4. verify_publication 直近結果 (cache)

- まだ `out/verify_publication.last` がありません.
  `bash scripts/verify_publication.sh | tee out/verify_publication.last`
  で snapshot を残すと次回以降ここに tail 30 行が貼られます.


## 5. 直近 4 時間に変更されたファイル (portal)

- `07:43` `docs/SESSION_SUMMARY.md`
- `07:41` `docs/NEXT_SESSION.auto.md`
- `07:40` `docs/spec/requirements_lleval_v0.1_draft.md`
- `07:32` `docs/NEXT_SESSION.md`
- `07:22` `docs/research/index.md`
- `07:21` `docs/spinoff_ideas_2026_05.md`
- `07:14` `docs/PROGRESS.md`
- `07:06` `docs/research/llrisk_prior_art.md`
- `07:05` `docs/research/llgov_sota.md`
- `07:05` `docs/research/llcraft_sota.md`
- `06:39` `docs/research/cognitive_mesh_vs_sota.md`
- `06:39` `docs/research/llgrow_prior_art.md`
- `06:39` `docs/research/lleval_sota.md`
- `06:32` `docs/doc_map.md`
- `06:32` `docs/index.md`
- `06:30` `scripts/gen_next_session_auto.py`


## Cross-references

- [NEXT_SESSION (manual)]({{ '/NEXT_SESSION' | relative_url }}) — 人手で書く方向性メモ
- [PROGRESS]({{ '/PROGRESS' | relative_url }}) — 累積セッション履歴
- [Roadmap]({{ '/roadmap' | relative_url }}) — Phase + dependency
- [Spec hub]({{ '/spec/' | relative_url }}) — FullSense Spec v1.1

