---
layout: default
title: "Progress"
nav_order: 90
---

# FullSense Portal — Progress

> Persistent project notes for the **umbrella portal repository** itself.
> Product-side progress lives in each product's repo (`llive/docs/PROGRESS.md`,
> `llmesh/docs/PROGRESS.md`, `llove/docs/PROGRESS.md`).

## 2026-05-20

### Phase 0.6 — NEXT_SESSION 自動化

- `scripts/gen_next_session_auto.py` 新規 — `docs/NEXT_SESSION.auto.md` を毎ターン上書きする Stop hook 用スクリプト. 内容は: portal git snapshot (log 10 件 + status + ahead/behind) / 関連プロジェクト (llive/llove/llmesh/lldesign/lltrade) の最新 commit & `tests/` 直近 mtime / `NEXT_SESSION.md` の 🧑 セクションを再抽出した checkbox 化 operator action / `out/verify_publication.last` cache snapshot / 直近 4 時間に変更された portal ファイル.
- raptor 側 `libexec/raptor-next-session-update` ラッパ追加 + `.claude/settings.json` Stop hook に登録. `RAPTOR_CALLER_DIR=D:/projects/fullsense` のときだけ動く分岐.
- index.md / doc_map.md に `NEXT_SESSION.auto.md` リンク追加.
- 設計判断: 手書き `NEXT_SESSION.md` を温存しつつ別ファイル分離で drift を防ぐ. NEXT_SESSION.md Priority 2 (NEXT_SESSION 自動更新フロー) の実装相当.

### Phase 0.7 — Research notes hub + spinoff 深化

- `docs/research/` 新設 (nav_order: 92, `has_children: true`). 各 spinoff 候補ごとに先行研究/SOTA メモを並べる方針.
- 5 件の調査メモ追加 (AI agent 並列調査 + 800 字内要約 + Sources 5-10 件):
  - `llgrow_prior_art.md` — HITL content automation (Jasper/Mautic/Langfuse) + academic 2025. on-prem + audit + HITL + 個人 OSS 配信の 4 条件は空白. 推奨: Langfuse + Mautic 再利用 + 3 vertical layer 新規実装.
  - `lleval_sota.md` — OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse / TruLens / Ragas. on-prem 統一 + progressive size + honest disclosure + self-pref bias の 4 つに空白. 推奨 fork base: promptfoo.
  - `cognitive_mesh_vs_sota.md` — llive v0.8 M8.1〜M8.9 を MemGPT / Generative Agents / A-MEM / Reflexion / Constitutional AI 等と sub-system 毎に対応づけ. Ed25519 署名 Quarantined Memory と Tonic+phasic 二軸 risk が差別化.
  - `llcraft_sota.md` — on-prem creative material (TTS / 画像 / 動画 / 音楽) の OSS Stack matrix + license tier 管理. C2PA Content Credentials + IPTC 2025.1 に license_tier カスタム assertion を載せる方針.
  - `llgov_sota.md` — AI governance OSS / SaaS matrix (NeMo Guardrails / OPA / Cedar / Credo AI / Holistic AI 等). EU AI Act Art.9-15 を自動検証する OSS は不在. 推奨: ApprovalBus を OPA/Cedar wrapper 化 + Rego rule pack 配布.
  - `llrisk_prior_art.md` — AI-driven GRC / DevOps risk monitoring / LLM × project risk register / reputation / dev burnout の縦割り. 6 軸統合 + 個人開発者 + on-prem + LLM-driven は空白. 推奨: TonicRiskMonitor のメタ拡張.
- `spinoff_ideas_2026_05.md` 各 vertical セクションに `先行研究` cross-ref を埋め込み, `C-2. 採用優先度` 表で lleval=HIGH / llgrow=MID / llbridge=MID / llcraft=llrisk=llgov=LOW / llforen=DEFER と判定.

### Phase 0.8 — 関連プロジェクト test 回帰確認 + 環境依存 fix

- **llive**: 1518 PASS 維持 (回帰なし).
- **llove**: chafa が WinGet 経由で PATH に乗ったことで `find_image_tool()` が拾い image renderer fallback test 6 件 + markdown_view 1 件が fail. 各 test に `monkeypatch.setattr(<module>.shutil, "which", lambda name: None)` を追加して環境依存を排除. property test 1 件は Windows IO で 200ms deadline 超過のため `@settings(deadline=None)`. e2e_real_chafa は mmdc 実行失敗時に `pytest.skip()` へ降りる gate を追加.
- **llmesh**: `test_property_audit_qos.py` の hypothesis test 2 件で `@settings(deadline=None)` 追加 (Windows での初回 file IO で 200ms 超過の flaky 対策).

## 2026-05-16

### Portal bootstrap (Phase 0)

Initial scaffold of `furuse-kazufumi/fullsense`:

- `README.md` — short brand + family overview + install snippet
- `docs/index.md` — full landing page with Mermaid family tree, product
  matrix, demo links, spec links, license
- `docs/_config.yml` — Jekyll `just-the-docs` remote-theme config, Mermaid
  enabled, aux links to the three product Pages sites
- `.gitignore` — Jekyll build artifacts (`_site/`, `.jekyll-cache/`, etc.)
- First commit `d7d070b chore(init): FullSense umbrella portal repo`

### Portal hardening (Phase 0.1, current)

- `docs/PROGRESS.md` (this file) — persistent project log
- `docs/NOTES.md` — design decisions, link-rot watch list, deferred items
- `LICENSE` — Apache-2.0 (matches product code; docs themselves are
  permissive)
- `.nojekyll` is **not** added — we **do** want Jekyll to process the docs
- `.github/workflows/link-check.yml` — Lychee CI for external link
  rot. Runs on docs/README push, on PRs that touch docs, weekly on Monday
  18:00 UTC, and on manual dispatch. Scheduled failures open a tracked
  issue with the `docs, link-rot` labels.
- `docs/assets/images/og-card.{svg,png}` — Open Graph social card,
  1200×630. SVG is the editable source; PNG is the actual crawler
  target (Twitter/LinkedIn don't render SVG `og:image`). The PNG was
  generated via a small Pillow script — to regenerate, edit the SVG
  manually or re-run the script (recorded in this PROGRESS entry).
- `docs/_config.yml` — `defaults.image`, `logo`, `social.links`,
  `twitter.card: summary_large_image` added so `jekyll-seo-tag`
  emits proper `og:image` / `twitter:image` tags across all pages.

### Umbrella expansion (Phase 0.3, 2026-05-16)

Two new products spun up as siblings of llmesh / llive / llove and added to
the Family Tree, both **alpha v0.0.1 skeleton**:

- [lldesign](https://github.com/furuse-kazufumi/lldesign) — UI / Web / diagram design
  tooling (stresses llive KAR / TLB / ICP / PM axes)
- [lltrade](https://github.com/furuse-kazufumi/lltrade) — paper-trading research
  with `REAL_TRADING=False` hard-pinned at 3 layers (stresses llive RPAR /
  SIL / DTKR / APO axes)

Portal-side additions:

- `docs/roadmap.md` — live + planned + parked products with trigger conditions
  (llcad / lleda / llchip / llmed / llpaper)
- `docs/comparison.md` — honest 9-axis comparison vs Claude Code / Perplexity
  / Codex CLI / Gemini CLI with A–F grading
- Family Tree mermaid extended with 5 live + 5 parked nodes (ghost styled)
- `scripts/verify_publication.sh` — one-shot checker for Pages / portal links
  / branch protection / About config / Mermaid rendering

llive integration probe:

- `D:/projects/llive/scripts/run_brief.py` + `docs/BUGS_2026-05-16_brief_ab.md`
  — A/B run of the same skeleton-creation Brief against the FullSense Loop
  yielded 8 documented gaps. Headline: LLM backend unwired (LLIVE-001) and
  Brief API absent (LLIVE-002). Captured in
  `~/.claude/.../memory/project_llive_bug_2026_05_16.md`.

Empirical AI A/B benchmark (4 Briefs × 6 models):

- `scripts/bench_run.py` — one-shot A/B replayer (llive / ollama / Anthropic
  / Gemini / Codex / Perplexity)
- `scripts/bench_vlm.py` — same shape for vision models (Anthropic Claude
  vision, Gemini Flash vision, GPT-4o-mini vision, ollama llava,
  llama3.2-vision)
- `docs/benchmarks/2026-05-16{,_mermaid_brief,_quickstart_seqdiag,_lltrade_yaml}.md`
  — first 4 Brief results. Headline: Perplexity Sonar 4/4 spec-compliant
  at ~$0.005/brief; ollama `llama3.2:3b` typos `llive` as `lllive` twice
  (`ll*` prefix tokenization hostility) and violates constraints; Anthropic
  + Gemini + OpenAI Codex all errored on credentials (operator action
  queued — see `~/.claude/.../memory/project_benchmark_2026_05_16.md`).
- `docs/comparison.md` — empirical benchmark section links to the per-Brief
  pages so the comparison story is data-backed, not aspirational.

CI scaffolding for the new products:

- `lldesign/.github/workflows/test.yml` — pytest + ruff format + ruff check
  on Python 3.11 (18 s first green run)
- `lltrade/.github/workflows/test.yml` — pytest + ruff + an extra step that
  verifies `lltrade.REAL_TRADING is False` (20 s first green run). The
  REAL_TRADING check guards the v0.x paper-only invariant in CI as well as
  in the package itself.

### Public launch (Phase 0.2, 2026-05-16)

Portal is live:

- Repo: <https://github.com/furuse-kazufumi/fullsense> (public, Apache-2.0)
- Pages: <https://furuse-kazufumi.github.io/fullsense/> (source = `main` /
  `/docs`, HTTPS enforced, first `pages-build-deployment` succeeded in 39 s)
- Description, Homepage, and 10 individual Topics
  (`apache2 fullsense llive llm llmesh llove mcp on-prem self-evolving
  umbrella`) set via GitHub UI — `gh api` PATCH was blocked by the
  fine-grained PAT not having `Administration: Write`, so the About panel
  in the GitHub UI is the source of truth for these.
- Push protocol: HTTPS rejected (PAT lacks `contents: write`), switched
  `origin` to SSH `git@github.com:furuse-kazufumi/fullsense.git`. SSH key
  `Windows-PC-2026` was already registered.
- Link-check CI ran on first push, 10 s success — Lychee found no broken
  links in `docs/**` and `README.md`.

### Open items

- [x] ~~Verify `mermaid` renders correctly under `just-the-docs` remote theme~~
      **解消 (2026-05-16 以降 verify_publication.sh で継続確認、Phase 0.4 で
      Mermaid lint CI 追加)**
- [x] ~~Add `docs/spec/` mirror of the FullSense Spec v1.1~~
      **Phase 0.4 で portal `docs/spec/index.md` を「章直リンク方式」で追加
      (drift 防止)**
- [ ] Open Graph card v2: when the v1.0 PyPI rename lands, re-render
      `og-card.{svg,png}` with the `fullsense-*` install snippet and
      bump it on social by sharing the canonical Pages URL.
- [ ] Replace bare LinkedIn/Qiita article links with a curated `docs/articles/`
      index once the article-pause (see `feedback_articles_pause.md`) is
      lifted
- [ ] Rotate the fine-grained PAT into one with `Administration: Write` (or
      switch to a classic PAT with `repo` scope) so future portal-side
      automation (`gh api topics`, Pages settings, repo edit) can run
      without manual UI steps.

## 2026-05-18

### Phase 0.4 — Reference hubs + drift 防止構造の整備

ユーザ依頼「朝 7 時まで自律的に改善し続ける」+ 「直近 memory を llive 設計
思想として要件定義に追記」を受け、portal + llive 両方を補強。

llive 側 (1 commit, 4 ファイル):

- **`docs/requirements_v0.8_cognitive_mesh.md`** (新規 462 行) — COG-MESH-01〜10
  の 10 要件 (MultiBriefCoherenceManager / TitleRecallPlanner /
  TonicRiskMonitor / IdleTrainingScheduler / GiftValueEstimator / ProactiveLoop /
  QuietHoursGuard / BriefDeque-Map-Tree / GrammarLayer / Mesh5W1H +
  Granularity)。出典: 2026-05-18 一連 memory (user_cognitive_mesh_model /
  feedback_brain_like_trigger_periodic / feedback_proactive_llm_speech /
  feedback_quiet_hours / project_proactive_llive_demo /
  feedback_response_timing)
- **`.planning/REQUIREMENTS.md`** — v0.8b COG-MESH 群を CABT v0.8 と並列に
  10 件追記。CABT (低レイヤ) と COG-MESH (高レイヤ) は「同 v0.8 期に着手
  すべき双子の要件群」
- **`docs/architecture.md` §8** — v0.8 拡張ポイント (Proactive / Mesh /
  Safety / Evolution Layer) を Mermaid + 接続表で図示
- **`docs/roadmap.md` Phase 8** — CABT + COG-MESH 双子マイルストーン
  (M8.0〜M8.9 + M8.A〜M8.E)、SemVer は build metadata で段階リリース

portal 側 (7 commit):

- **`docs/benchmarks/policy.md`** (新規) — 三本柱 (measurement purity / progressive
  curve / honest disclosure) + 運用チェックリスト + 直近運用状況 (Mermaid)
- **`docs/comparison.md`** — Honest disclosure セクション追加 + Benchmark
  Policy リンク + Last updated 更新 (credential 復旧待ち事実を明記)
- **`docs/spec/index.md`** (新規) — Spec hub。22 章直リンク + 要件定義 8 本
  一覧 + drift 防止方針
- **`docs/roadmap.md`** — ステータス遷移モデル (5 状態) + Live/Planned
  マトリクス (13 product) + 依存グラフ + タイムライン (Mermaid 3 種)
- **`.github/workflows/mermaid-lint.yml`** (新規) — Mermaid 構文 CI lint
  (mermaid-cli 経由)
- **`docs/recommended-models.md`** (新規) — 用途別推奨 on-prem モデル hub
  (`llama3.2:3b` 非推奨の根拠含む) + 判断軸 flowchart + 共通 install スニペット
- **`docs/index.md`** — Reference hubs セクション追加 (Spec / Benchmark
  Policy / Recommended models へのナビ統合)

設計指針 (本 Phase で確立):

- **drift 防止構造**: 各 product README は具体モデル / 系列ラベル / 系
  特定の数値を書かず、portal hub にリンクする
- **honest disclosure as architecture**: credential 復旧待ち事実 / 採点者
  バイアス / 一部測定未完を明示する hub を設置
- **倫理は architecture の一部**: Quiet Hours / Gift Value gate / Risk
  monitoring を後付けでなくコンストラクタで注入

検証:

```bash
bash scripts/verify_publication.sh
# A. Pages reachability: 5/5 PASS
# B. Portal link sweep: PASS (35 external GitHub links)
# C. Branch protection: 6/6 PASS
# D. About + Topics: 4/4 PASS (lldesign / lltrade)
# E. Mermaid family tree: PASS
# Summary: ALL CHECKS PASSED (継続維持)
```

## 2026-05-19 早朝 (Phase 0.5)

### COG-MESH 全 10 件実装ラッシュ (llive 側)

Phase 0.4 で要件追加した COG-MESH 群を、続くセッション後半で **全 10 件
最小実装まで完走**。portal 側からは家系図で見守る形だが、llive `v0.8`
として要件 → 実装着地までを 1 セッションで踏み抜けた事実は portal 側
進捗としても記録する。

実装完了:

| ID | 名称 | Phase 想定 | 結果 |
|---|---|---|---|
| COG-MESH-01 | MultiBriefCoherenceManager | 7 前倒し | ✅ |
| COG-MESH-02 | TitleRecallPlanner | 6 前倒し | ✅ |
| COG-MESH-03 | TonicRiskMonitor | 6 前倒し | ✅ |
| COG-MESH-04 | IdleTrainingScheduler | 5 | ✅ |
| COG-MESH-05 | GiftValueEstimator | 5 | ✅ |
| COG-MESH-06 | ProactiveLoop | 5 | ✅ |
| COG-MESH-07 | QuietHoursGuard | 5 | ✅ |
| COG-MESH-08 | BriefDeque / Map / Tree | 5 | ✅ |
| COG-MESH-09 | GrammarLayer (skeleton) | 7 | ✅ |
| COG-MESH-10 | Mesh5W1H + Granularity | 6 前倒し | ✅ |

数値:

- llive **1379 PASS** (前回 1272 + 新規 107)、regress 無し
- 統合 demo CLI (5 sub-system 連動): `py -3.11 -m llive.cognitive_mesh.demo`
  で Active/Quiet 両方の挙動を 1 画面確認
- llive 側 11 commit (feat 9 + docs 2)

設計指針 (本 Phase で再確認):

- **倫理は architecture の一部** — ProactiveLoop / IdleTraining は
  QuietHoursGuard 必須依存、None で TypeError
- **fail-closed in Quiet Hours** — TZ / env 欠落で常に Quiet 扱い
- **risk_alert / audit_alert は例外通過** — Quiet Hours 中でも emit OK
- **副作用分離** — state_snapshot は dict copy で後の変更と独立
- **70 点で commit** — feedback_response_timing を design / 実装の両方に適用

### portal 側で更新したもの

- (本 Phase 0.5 では portal 側ファイルは未更新、本セクション追記のみ)
- 次セッションで `roadmap.md` の Phase 8 にあった `M8.0〜M8.3` の状態を
  「Skeleton 完了 / Phase 5 本実装は別タスク」に更新検討
- portal `Spec hub` の要件定義一覧で v0.8 を「全 10 件 skeleton 完了」と
  注記検討

### 検証

```bash
# llive
cd D:/projects/llive
py -3.11 -m pytest tests/unit -q
# 1379 passed in ~110s

# portal
cd D:/projects/fullsense
bash scripts/verify_publication.sh
# ALL CHECKS PASSED (継続維持)
```

## 2026-05-19 朝 (Phase 0.6)

### COG-MESH 本実装フェーズ完了 (M8.2〜M8.7、llive 側)

Phase 0.5 (早朝の skeleton ラッシュ) に続く朝の継続セッションで、
NEXT_SESSION Priority 1 として残っていた **M8.2〜M8.7 を全件本実装**完了。
"skeleton から本実装" への昇格を 1 セッションで踏み抜いた。

完了マイルストーン (llive 側):

| Milestone | 内容 | 新規 adapter | テスト |
|---|---|---|---|
| M8.5 | ApprovalBus.intervene 配線 | `RiskInterventionAdapter` | 5 |
| M8.4 | TitleRecall semantic similarity | `EmbeddingSimilarityFn` (MemoryEncoder cosine) | 9 |
| M8.3 | BriefDeque ↔ BriefRunner 接続 | `BriefDequeRunnerBridge` | 6 |
| M8.6 | Mesh5W1H ↔ Annotation Channel 統合 | `Mesh5W1HAnnotator` | 7 |
| M8.7 | Proactive 拡張 (event / consistency mode) | `ProactiveEvent` / `ConsistencyViolation` | 12 |
| M8.2 | Idle ingest Quarantined Memory + Ed25519 | `QuarantinedMemory` + `Ed25519Verifier` + `SignedPayload` | 16 |

数値:

- llive **1448 PASS** (1393 + 新規 55)、regress 無し
- 統合 demo CLI を **5 → 9 セクション**に拡張 (Active/Quiet 双方の挙動が可視化)
- llive 側 主要 commit 2 件 (feat: COG-MESH 本実装 + demo 拡張)

設計上の共通点 (本フェーズ):

- **全 adapter が backward compatible** — 注入しなければ従来挙動
- **fail-closed が継続** — adapter 経路例外は token/pending/silent に縮退
- **公開 API 整理** — `__init__.py` `__all__` に 9 シンボル追加

### portal 側 反映

- `docs/NEXT_SESSION.md` を「M8.2〜M8.7 完了」「残作業は M8.1/M8.8/M8.9」に
  全面書換 (Last updated 2026-05-19 朝)
- `docs/PROGRESS.md` 本セクション追記
- (mermaid family tree / Roadmap / Spec hub の Phase 8 状態は次セッションで
  refresh 候補)

### 残作業 (次セッション候補)

- **M8.1**: ProactiveLoop を llove F25 経由で TUI 表示 + asciinema 録画 (llove 側 + 操作者)
- **M8.8**: MultiBriefCoherenceManager を networkx + 実 Brief 統合 (agent Phase 6)
- **M8.9**: GrammarLayer を EVO-04/06/07 と接続、言語別 layer 設計 (agent Phase 7)
- **bench**: Anthropic / Gemini / OpenAI credential 復旧後に bench_run.py / bench_vlm.py 再実行
- **articles pause**: パッケージ公開級の完成度に到達 — 解除タイミング再評価

### 検証

```bash
cd D:/projects/llive
py -3.11 -m pytest tests/unit -q
# 1448 passed

# 統合 demo (9 セクション、Active 10:00 / Quiet 02:00 切替)
$env:LLIVE_TZ="Asia/Tokyo"
$env:LLIVE_QUIET_HOURS_START="22"; $env:LLIVE_QUIET_HOURS_END="8"; $env:LLIVE_QUIET_HOURS_ENABLED="1"
$env:LLIVE_DEMO_FORCE_TIME="2026-05-19T10:00:00+09:00"
py -3.11 -m llive.cognitive_mesh.demo
```

## References

- Brand introduction memo — `~/.claude/.../memory/project_fullsense_brand.md`
- Spec source of truth — `llive/docs/fullsense_spec_eternal.md`
- Trademark drafts — `llive/docs/legal/trademark/`

---

## Phase 0.6 — 2026-05-20 夜 (llive コア最適化 + 3 日統合記事)

このセッションは「llive コア最適化 12h goal」継続と「一巡で全プロジェクト
残件対応」を兼ねる. 結果:

### llive コア最適化 (B-9 production 注入完了)

- branch `optimize/core-2026-05-20` で B-9-a + B-9-b commit:
  - **B-9-a** (`17302db` 周辺): `SurpriseGate` / `BayesianSurpriseGate.compute_surprise`
    に `assume_normalized: bool = False` kwarg 追加. `MemoryWriteBlock` callsite
    で True 指定し `SemanticMemory.all_embeddings()` の L2 normalized 済 matrix を
    再 normalize しないように. B-2 で測定済の 2-5x cosine 高速化を実コードに反映.
  - **B-9-b** (`17302db`): `GiftValueEstimator._history` を `list` → `deque` 化.
    `commit()` で `cooldown * 2` 超過 entry を popleft で sliding-window evict.
    B-6 で list_slice が 119x 遅化することを確認済の pathology を予防的に解消.
  - **experiments doc 追記** (`de76f8c`): B-9-a/B-9-b 注入結果 + 採用ゲート確認.
- 全 1585 PASS 維持, 回帰なし.

### llmesh test_aoi 順序依存 flaky 調査

- 単独 5 回 + `tests/test_synthetic_dataset.py` 全体 5 回 + 全 3086 test 走行で
  flaky 再現せず. 朝の `register_profile("local-flaky-safe", deadline=None)`
  fix で実質収束済と推定.
- 根本原因は依然 hypothesis ベース property test の deadline か, あるいは
  並列 / 環境負荷で稀発生する asyncio タイミング. 将来宿題のまま, 本セッション
  では追加 fix 不要と判定.

### lleval v0.1 implementation notes (PoC scope 確定)

- `docs/spec/lleval_v0_1_implementation_notes.md` 追加 (`eaca2e5`).
- 主要決定:
  - promptfoo は **fork ではなく wrap** (TS/Node を Python subprocess で叩く)
  - 別 GitHub repo (`furuse-kazufumi/lleval`), Apache-2.0 + Commercial dual
  - v0.1 MVP = LE-01 / 02 / 03 / 07 (judge rotation / OTel trace / RAG adapter
    / CI hook は v0.2 以降)
  - 5 因子 honest-disclosure 分解 (warmup / token-norm / RTT / attach / load) を
    一次クラス機能化
- 着手判断 4 課題 (C-1〜C-4) を明記. user 承認後に repo init.

### 3 日統合記事 (5/18-20) QIITA #21

- `docs/articles/2026-05-20/QIITA_21_three_day_marathon_2026_05_18_to_20.md` 新規
  (`bab4dd8` + auto snapshot `bdc325a`).
- 3 部構成: 第 1 幕 5/18 火種 / 第 2 幕 5/19 爆発 / 第 3 幕 5/20 構造化.
- Qiita タグ 5 個 (FullSense / llive / ClaudeCode / 自律エージェント / HonestDisclosure).
- articles_pause 解除後の第 1 本目候補. 公開判断は user.

### 数値まとめ (3 日累積)

| 指標 | 値 |
|---|---|
| 関連リポジトリ | 8 |
| 主要 commit (auto: 除く) | 80+ |
| 全 commit | 200+ |
| llive PASS 数 | 1393 → **1585** (+192) |
| llove PASS 数 | 771 → **796** (+25) |
| llmesh PASS 数 | 42 → **3086** (測定範囲拡大込み, 純 +4) |
| 新規記事 (Qiita draft / spec / research) | 14+ |
| 新規要件定義 / 戦略文書 | 6+ |

### 残作業 (次セッション候補)

- **lleval repo init 着手判断** (user 承認待ち, mock provider で先行可能).
- **llive B-7 (audit JSONL sink)** — optimize/core branch 継続候補.
- **llive optimize/core branch → main マージ判断** — PR 後 user 承認.
- **credential 復旧** (Anthropic / Gemini / OpenAI) → bench_run.py 再走 →
  comparison.md honest disclosure 再採点.
- **asciinema 録画** — COG-MESH 統合 demo 9 セクション + llive demo + LoveApp+env.
- **articles_pause 解除後の連投ペース** — QIITA #21 含め複数本 stocked, 公開
  順序を user と確認.

### 検証

```bash
# llive optimize branch (B-9 注入後)
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1585 passed

# llmesh 全件
cd D:/projects/llmesh
py -3.11 -m pytest -q
# 3086 passed (12 分)

# 統合記事レンダリング
cd D:/projects/fullsense
bash scripts/verify_publication.sh
```

---

## Phase 0.7 — 2026-05-21 (llama.cpp 追従要件 v0.A + 進化型 v0.B 全件実装)

### llama.cpp 追従要件 (v0.A) 実コード落とし込み

- llive 新規 `docs/requirements_v0.A_external_runtime_tracking.md` — 月次追従ルール
- llive 新規 `docs/spec/llamacpp_compat_matrix.md` — 3 段階 pin SSoT
- llive 新規 `tests/contract/test_llamacpp_smoke.py` — S-1〜S-5, default skip (CI 安全)
- llive 新規 `src/llive/benchmark/runtime_metadata.py` — 6 metadata helper + publish gate
- llive 新規 `tests/unit/test_benchmark_runtime_metadata.py` — 6 件緑
- portal `docs/spec/lleval_v0_1_implementation_notes.md` に **Honest Disclosure
  6 因子目 (Runtime metadata)** を追加, lleval CI で BLOCK 仕様

### claude-smart 隔離評価準備

- portal `.worktrees/eval-claude-smart` 隔離 worktree 作成
  (branch `eval/claude-smart-2026-05-21`)
- `.gitignore` に `.worktrees/` 追加
- `EVAL_PLAN.md` (8 軸観測 × 3 セッション × 5 ターン以上, 判定 3 択)
- raptor memory `reference_claude_smart` + `feedback_llamacpp_tracking` 追加

### 進化型最適化レイヤ (v0.B) 一気通貫実装

ユーザー指示「ROS 歩行進化の AI 版 = 集団 → 評価 → 選別 → 交配 → 突然変異 →
次世代」を本セッション内で全件カバー.

- llive 新規 `docs/requirements_v0.B_evolutionary_optimization.md` — 要件 EV-01〜11
- llive 新規 `src/llive/perf/evolutionary/` package:
  - `genome.py` (Genome + bounds), `individual.py` (FitnessReport + history),
    `population.py` (RLock + PopulationStats + diversity_l2)
  - `selection.py` (Tournament/Roulette/Elitism), `crossover.py` (Uniform/Blend),
    `mutation.py` (Gaussian/Reset/Chained)
  - `fitness.py` (sphere/rosenbrock + runtime_metadata 必須),
    `fitness_ucb.py` (EV-09 UCB hyperparam 連携)
  - `loop.py` (EvolutionLoop + patience + diversity_floor + JSONL out),
    `scheduler.py` (Serial / Multiprocessing / Asyncio)
- llive 新規 `tests/unit/test_evolutionary.py` (22 件) +
  `tests/unit/test_evolutionary_scheduler.py` (4 件) すべて緑
- llive 新規 `scripts/demo_evolutionary_loop.py` (sphere/rosenbrock/ucb_hparam)
- llive 新規 `docs/experiments/evolutionary_v0_B_2026_05_21.md` — 実走結果 +
  教訓 4 つ + 残作業表
- llive 全件: 1591 → **1617 PASS** (+26, 回帰なし)

### Demo 実走結果

| Problem | 結果 |
|---|---|
| sphere 3 dim / 25 gen | best=-1.2e-5 (真の最適 0 にほぼ収束) |
| rosenbrock 2 dim / 60 gen | best=-0.0057 (valley 沿いに収束) |
| ucb_hparam 3 dim / 15 gen | exploration_constant=3.28 (UCB1 標準 √2 と乖離, toy 環境では妥当) |

### 教訓 (3 日累積)

1. **収束型 × 進化型 は直交補完**: UCB が個体内 variant, GA が集団構造を担当
2. **bounded modification は GA でも強制**: 物理的に不可能な genome を作らない
3. **runtime metadata は進化中もズレないように同梱必須**: 評価基準が進化途中で
   変わると進化が破綻 (重力が変わるシミュレーター回避)
4. **月次追従 + commit SHA pin が公開ベンチの最低限**: llama.cpp の moving target
   を Honest Disclosure 規約と整合させる唯一の現実解

### 残作業 (次セッション候補)

- Phase 3.5: per-individual sub-seed 派生 (再現性強化, 1h)
- Phase 4: 実 LLM fitness adapter `fitness_llm.py` (credential 復旧後)
- Phase 4: lleval LE-02 progressive size matrix と GA を連結 (lleval repo init 後)
- claude-smart 評価セッション (5/22-25 を予定)
- llive optimize branch を main にマージする判断 (B-9 + v0.B の規模が大きいので
  PR 経由)

### 検証

```bash
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1617 passed

py -3.11 scripts/demo_evolutionary_loop.py --problem sphere --size 30 --gens 25
py -3.11 scripts/demo_evolutionary_loop.py --problem rosenbrock --size 50 --gens 60 --seed 7
py -3.11 scripts/demo_evolutionary_loop.py --problem ucb_hparam --size 20 --gens 15
```

---

## Phase 0.8 — 2026-05-21 (15h marathon: 前倒し全件実装)

ユーザー指示「前倒しで出来ることも含めて実施. 15 時間後まで続けてください」の
もと, credential / 外部 binary 依存なしで進められる残作業を全件着地.

### llive v0.B Phase 3.5 + 4 — mock baseline で全件カバー

- **Phase 3.5: per-individual sub-seed 派生** (`seeds.py`).
  SHA-256(parent_seed + individual_id) → 31-bit int で deterministic 派生.
  `fitness_accepts_seed` で inspect dispatch, 既存 1 引数 fitness と完全
  後方互換. +8 test.
- **Phase 4: `fitness_llm.py` mock skeleton**.
  5 軸 fitness (latency/quality/stability/safety/honesty) + LLM_GENOME_BOUNDS
  (backend_id/temp/top_p/kv_quant_id/model_quant_id) を MockBackend ベースで
  credential 不要に. +7 test.
- **5 backend Genome PoC** (`test_evolutionary_backend_select.py`).
  GA × 5 backend (MockBackend 解決) で 3 世代回し, bounds 内収束を確認.
  +2 test.
- `demo_evolutionary_loop.py` に `backend_select` problem 追加.

### low_spec bench mock 実走

- `demo_low_spec_mock.py` 新設. MockBackend で xs/s を実走 → bench 経路の
  生死 + JSON shape 確定. **honest disclosure**: MockBackend 数値は公開
  ベンチに使用禁止と明記 (`docs/experiments/low_spec_mock_2026_05_21.md`).

### lleval skeleton (D:/projects/lleval/)

- 新規 repo 雛形作成. Apache-2.0, Python 3.11, pyproject + src/lleval/.
- 公開 API: `Bench` / `Config` / `ProgressiveMatrixRunner` /
  `HonestDisclosureAnalyzer` / `Report` / `cli`.
- 8 件 skeleton smoke test 緑.
- 実 GitHub repo 化 + PyPI 公開判断は **user 承認後**.

### llive 全件回帰

- 1617 → **1634 PASS** (+17, 回帰なし).
- branch `optimize/core-2026-05-20` の HEAD は `d096ce0` 以降に追加 commit
  (seeds + fitness_llm + backend_select + low_spec mock + docs).

### 残作業 (credential / 外部 binary 復旧後)

| # | アクション | 依存 |
|---|---|---|
| 1 | llama.cpp + Codestral-Mamba GGUF で `MambaBackend(transport='llama_cpp_server')` 実走 smoke | llama-server 起動 |
| 2 | low_spec bench 実 backend 実走 (MockBackend 数値を上書き) | step 1 |
| 3 | RWKV-7 を `RwkvBackend(transport='rwkv_cpp_server')` で繋ぐ | RWKV.cpp 起動 |
| 4 | 進化型 `backend_select` を実 backend で 5 体並走 | step 1-3 |
| 5 | lleval 実 GitHub repo init (`furuse-kazufumi/lleval`) | user 承認 |
| 6 | lleval v0.1.0a1 (promptfoo subprocess 接続) | step 5 |
| 7 | claude-smart 評価 Session 1 dogfood | user が worktree で Claude Code 起動 |

### 検証

```bash
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1634 passed

py -3.11 scripts/demo_evolutionary_loop.py --problem backend_select --size 12 --gens 6
py -3.11 scripts/demo_low_spec_mock.py --backends mock --sizes xs s

cd D:/projects/lleval
py -3.11 -m pytest tests/unit -q
# 8 passed
```

---

## Phase 0.9 — 2026-05-21 夕方 (llive v0.C 派生集団進化)

ユーザー指示 3 連発 (2026-05-21):

1. 「完全に同時でなくても多くのランダム llive 派生を取捨選択」
2. 「進化形態として多様性を持ちながらゲノム交配のような要素」
3. 「個体数が必要で時間がかかる, 準備が大事」

→ **「1 llive = 1 個体」** で集団化, **染色体単位の交配 (SegmentCrossover)**,
**長時間運用対応 (checkpoint / resume / budget)** を 1 セッションで全件着地.

### 新規 (llive v0.C)

- `docs/requirements_v0.C_llive_variant_evolution.md` — 要件 LV-01〜10
- `docs/experiments/llive_variant_v0_C_2026_05_21.md` — 実走 + 教訓 3 つ
- `src/llive/perf/evolutionary/llive_variant.py` — 19 dim Genome
  (思考因子 10 + memory 3 + backend 1 + sampler 3 + proactive 2) +
  LIVE_VARIANT_SEGMENTS (5 chromosome) + LlivVariantBuilder +
  mock_variant_fitness_factory (8 軸合成) + SegmentedScheduler
- `src/llive/perf/evolutionary/crossover.py` に **SegmentCrossover** 追加
  (生物的 gene segment swap)
- `src/llive/perf/evolutionary/loop.py` に大規模集団対応:
  - `max_wallclock_seconds` (時間予算)
  - `checkpoint_every` (世代ごと snapshot)
  - `resume_from` (snapshot から再開, dir 指定で最新自動選択)
- `scripts/demo_evolutionary_loop.py` に llive_variant problem 追加

### 新規 test (+19)

- `test_evolutionary_llive_variant.py` (13) — Genome / Builder /
  SegmentCrossover / mock fitness 8 軸 / Segmented / GA 3 世代
- `test_evolutionary_checkpoint.py` (6) — snapshot per-gen /
  checkpoint_every / resume_from (dir + fallback) / wallclock budget

### 実走 (30 個体 × 12 世代 mock)

| 世代 | best | mean | diversity |
|---|---|---|---|
| 0 | 0.5358 | 0.6420 | 14.40 |
| 6 | 0.7278 | 0.7058 | 8.81 |
| 12 | **0.7514** | 0.7327 | 8.28 |

12 世代で +40% 改善, 多様性 8.28 維持 (枯渇なし). 12 世代 evolved in 0.08s
(mock). best individual: factor_provenance=1.0, factor_consistency=0.91,
backend=anthropic, temp=0.77, gift=0.61, cooldown=30 分.

### llive 累積数値

- 1518 → **1653 PASS** (+135, 全 marathon 累積)
- 本 Phase 0.9: +19 test (v0.C)

### 教訓 (v0.C から 3 つ)

1. **染色体単位の交配は多様性に寄与** — SegmentCrossover で diversity 維持
2. **checkpoint + resume があると「長時間 GA は普通の運用」** — serial でも
   セッション跨いで世代を進められる
3. **19 dim でも収束は十分速い** — 30 体 × 12 世代 = 360 評価で +40% 改善

### 次セッション残作業 (累計, 本 Phase で増えた分)

11. v0.C Phase 2 — 実 LlivKernel spawn (subprocess 経由) + ephemeral data_dir
12. v0.C Phase 3 — lleval 統合 (19 dim genome → lleval Config bridge)
13. v0.C LV-10 — 系統樹可視化 (`lineage.mmd` Mermaid)

### 検証

```bash
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1653 passed

py -3.11 scripts/demo_evolutionary_loop.py --problem llive_variant --size 30 --gens 12 --seed 42
# best 0.5358 → 0.7514

py -3.11 scripts/demo_evolutionary_loop.py --problem llive_variant --size 50 --gens 30 \
    --out out/llive_variant_resume_test/
# checkpoint 機構の動作確認
```

---

## Phase 0.10 — 2026-05-21 夜 (前倒し補強 wave)

ユーザー指示「次に私がコメント入力するまで、出来ることを先行して進めて」+ 連続コメント
(LinkedIn 多言語 / Qiita 多言語 / 海外 platform / GitHub リンク) への並行応答.

### llive 側 (新規 +16 test, 1669 PASS)

- `src/llive/variant_runner.py` — v0.C Phase 2 subprocess 起動先 CLI
  (`py -m llive.variant_runner --config-json ... --output-json ...`).
  実 LlivKernel spawn は将来, 現状 mock baseline. exit code (0/1/2/3/4) で
  fail mode 分離.
- `src/llive/perf/evolutionary/lineage.py` — LV-10 系統樹可視化.
  `Winner` dataclass + `winners.jsonl` I/O + `render_lineage_mermaid` で
  graph TD 描画. parent_ids 辿って世代間 lineage 表現. ghost node サポート.

### lleval 側 (新規 +12 test, 59 PASS)

- `src/lleval/bridges/llive.py` — llive 19 dim Genome → lleval ProviderSpec
  上書き + Report cells → 5 軸合成 dict. llive は optional 依存.
- `src/lleval/report/html.py` — Report → HTML 文字列 (CSS 内蔵 self-contained).
  anomaly セル赤背景, summary block, XSS escape. stdlib only.
- `CHANGELOG.md` 0.1.0a1 エントリ追記
- `ROADMAP.md` v0.1.0a0 → 1.0 段階表

### portal / memory 反映

- `docs/spec/llive_variant_phase2_interface.md` — Phase 2 interface spec
  (subprocess / in-process transport, ephemeral data_dir, 5 fail mode, 系統樹)
- llive `docs/experiments/llive_variant_v0_C_2026_05_21.md` に checkpoint/
  resume/budget 実 file I/O 動作確認の追記 (Run 1/2/3)
- raptor memory:
  - `feedback_linkedin_translation_jp_only` 大幅修正 (多言語推奨に転換)
  - `feedback_qiita_github_links` 新規 (GitHub link 積極配置)
  - `feedback_overseas_tech_platforms` 新規 (海外 platform 戦略 5 step cross-post)

### 累積数値

- llive: 1518 → **1669 PASS** (+151 全 marathon 累積)
- lleval: 新規 → **59 PASS** (skeleton + 段階拡張)
- 主要 commit (本 Phase): llive 2 + lleval 2 + portal 0 = 4 件
  (portal は memory のみ更新, commit 不要)

### 残作業 (次セッション)

| # | アクション | 依存 |
|---|---|---|
| 1 | llama-server + Mamba GGUF 実走 smoke | llama-server 起動 |
| 2 | low_spec bench 実 backend 実走 | step 1 |
| 3 | RWKV-7 を `RwkvBackend` で繋ぐ | RWKV.cpp 起動 |
| 4 | `backend_select` を実 backend で 5 体並走 | step 1-3 |
| 5 | lleval 実 GitHub repo init | user 承認 |
| 6 | lleval v0.1.0a2 (promptfoo subprocess 実走) | step 5 + npx promptfoo |
| 7 | claude-smart 評価 Session 1 | user が worktree で起動 |
| 8 | llive optimize/core → main 3 PR | user 承認 |
| 9 | credential 復旧 → bench 再走 | 外部 |
| 10 | asciinema 3 本 | operator |
| 11 | **v0.C Phase 2 実 LlivKernel spawn** | kernel module 実装後 |
| 12 | **llive lineage 実 GA loop 統合 hook** (現状は run 終了後に手動書出し) | 設計後 1h |
| 13 | **海外 platform 投稿 cross-post 試行** (Medium / dev.to にQIITA #21-23 の en 版) | user 投稿判断後 |
| 14 | **Qiita 記事に GitHub link 積極配置 retrofit** (既存 QIITA #21-23 更新) | 各 30 min |

### 検証

```bash
cd D:/projects/llive
git checkout optimize/core-2026-05-20
py -3.11 -m pytest tests/unit tests/integration -q
# 1669 passed

py -3.11 -m llive.variant_runner --config-json /tmp/test_cfg.json \
    --output-json /tmp/test_result.json
# mock 経路で動作確認可

cd D:/projects/lleval
py -3.11 -m pytest tests/unit -q
# 59 passed
```
