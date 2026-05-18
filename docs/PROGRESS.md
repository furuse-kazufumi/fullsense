---
layout: default
title: "Progress"
nav_order: 90
---

# FullSense Portal — Progress

> Persistent project notes for the **umbrella portal repository** itself.
> Product-side progress lives in each product's repo (`llive/docs/PROGRESS.md`,
> `llmesh/docs/PROGRESS.md`, `llove/docs/PROGRESS.md`).

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

## References

- Brand introduction memo — `~/.claude/.../memory/project_fullsense_brand.md`
- Spec source of truth — `llive/docs/fullsense_spec_eternal.md`
- Trademark drafts — `llive/docs/legal/trademark/`
