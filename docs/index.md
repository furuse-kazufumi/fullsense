---
layout: default
title: "FullSense ™"
description: "Umbrella brand & spec for llmesh / llive / llove"
nav_order: 1
---

# FullSense ™

> **Umbrella brand & specification** for an open-source family of products
> targeting **self-evolving, on-prem, audit-friendly LLM systems**.

---

## Family Tree

```mermaid
flowchart TD
    F["FullSense umbrella v1.1 — 9 axes: KAR DTKR APO ICP TLB Math PM RPAR SIL"]
    LM["llmesh — secure LLM hub (on-prem MCP)"]
    LI["llive — self-evolving memory (4-layer + biological model)"]
    LO["llove — TUI dashboard (HITL workbench)"]
    LD["lldesign — UI/Web/diagram design (alpha)"]
    LT["lltrade — paper trading research (alpha)"]
    LMS["llmesh-suite (installer)"]
    LCAD["llcad — machine CAD (planned)"]
    LEDA["lleda — EDA / circuit / PCB (planned)"]
    LCHIP["llchip — semiconductor IC layout (planned)"]
    LMED["llmed — medical literature (parked)"]
    LPAPER["llpaper — academic drafting (parked)"]
    F --> LM
    F --> LI
    F --> LO
    F --> LD
    F --> LT
    F -.-> LMS
    F -.-> LCAD
    F -.-> LEDA
    F -.-> LCHIP
    F -.-> LMED
    F -.-> LPAPER
    LM <-. MCP .-> LI
    LI <-. bridge .-> LO
    LM <-. hub .-> LO
    LD <-. brief .-> LI
    LT <-. signal+gate .-> LI
    style F fill:#fef3c7,stroke:#f59e0b,stroke-width:3px
    style LI fill:#d1fae5,stroke:#10b981
    style LM fill:#dbeafe,stroke:#3b82f6
    style LO fill:#fce7f3,stroke:#ec4899
    style LD fill:#ede9fe,stroke:#8b5cf6
    style LT fill:#fee2e2,stroke:#ef4444
    style LCAD fill:#f3f4f6,stroke:#9ca3af,stroke-dasharray:5 5
    style LEDA fill:#f3f4f6,stroke:#9ca3af,stroke-dasharray:5 5
    style LCHIP fill:#f3f4f6,stroke:#9ca3af,stroke-dasharray:5 5
    style LMED fill:#f3f4f6,stroke:#9ca3af,stroke-dasharray:5 5
    style LPAPER fill:#f3f4f6,stroke:#9ca3af,stroke-dasharray:5 5
```

## Product Sites

| Product | Status | Description | Docs (Pages) | Source |
|---------|--------|-------------|--------------|--------|
| **llmesh** | stable | Secure LLM hub / on-prem MCP server | [llmesh docs](https://furuse-kazufumi.github.io/llmesh/) | [GitHub](https://github.com/furuse-kazufumi/llmesh) |
| **llive** | beta | Self-evolving modular memory LLM framework | [llive docs](https://furuse-kazufumi.github.io/llive/) | [GitHub](https://github.com/furuse-kazufumi/llive) |
| **llove** | beta | TUI dashboard / HITL workbench | [llove docs](https://furuse-kazufumi.github.io/llove/) | [GitHub](https://github.com/furuse-kazufumi/llove) |
| **lldesign** | alpha | UI / Web / diagram design via LLM-friendly DSLs | [lldesign docs](https://furuse-kazufumi.github.io/lldesign/) | [GitHub](https://github.com/furuse-kazufumi/lldesign) |
| **lltrade** | alpha | Trading research — **paper-trading only** (v0.x) | [lltrade docs](https://furuse-kazufumi.github.io/lltrade/) | [GitHub](https://github.com/furuse-kazufumi/lltrade) |
| llmesh-suite | stable | One-shot installer | — | [GitHub](https://github.com/furuse-kazufumi/llmesh-suite) |

Planned (parked, see [roadmap]({{ '/roadmap' | relative_url }})): **llcad** (machine CAD) · **lleda** (EDA / PCB) · **llchip** (IC layout) · **llmed** (medical literature) · **llpaper** (academic drafting)

## Quick Demos

Visual demos live in each product. The portal links them here:

- **TUI scenarios (17 ×  ja/en, vector SVG)** — <https://furuse-kazufumi.github.io/llove/scenarios/>
- **Animated SVG (5 × ja/en, CSS keyframes)** — same page, Animated section
- **Shogi animation (動きで魅せる代表例)** — <https://furuse-kazufumi.github.io/llove/scenarios/anim/shogi/ja.svg>
- **Clustering demo (Phase 2a P2P discovery)** — <https://furuse-kazufumi.github.io/llmesh/demos/clustering_demo>

## Install

```bash
# Suite (all-in-one)
pip install llmesh-suite

# Individual
pip install llmesh           # hub
pip install llmesh-llive     # memory
pip install llmesh-llove     # TUI
```

PyPI rename to `fullsense-*` is planned at v1.0 — see
[llive v1.0 migration plan](https://github.com/furuse-kazufumi/llive/blob/main/docs/v1.0_migration_plan.md).

## Spec & RFC

- **FullSense Spec v1.1** — [llive/docs/fullsense_spec_eternal.md](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md)
- **P2P mesh RFC (Winny 思想を技術導入)** — [llive/docs/llmesh_p2p_mesh_rfc.md](https://github.com/furuse-kazufumi/llive/blob/main/docs/llmesh_p2p_mesh_rfc.md)
- **EDLA 歴史的参照 (金子勇 1999)** — [llive/docs/references/historical/edla_kaneko_1999.md](https://github.com/furuse-kazufumi/llive/blob/main/docs/references/historical/edla_kaneko_1999.md)
- **v1.0 PyPI rename plan** — [llive/docs/v1.0_migration_plan.md](https://github.com/furuse-kazufumi/llive/blob/main/docs/v1.0_migration_plan.md)
- **Trademark drafts (FullSense × JP/US/EU)** — [llive/docs/legal/trademark/](https://github.com/furuse-kazufumi/llive/tree/main/docs/legal/trademark)

## License

All product code: **Apache-2.0** with optional separate **Commercial License**.
- License text: <https://github.com/furuse-kazufumi/llive/blob/main/LICENSE>
- Commercial: <https://github.com/furuse-kazufumi/llive/blob/main/LICENSE-COMMERCIAL>
- Trademark policy: <https://github.com/furuse-kazufumi/llive/blob/main/TRADEMARK.md>

## Articles

**最新公開資料の集約場所 (2026-05-17〜)**: [`docs/articles/`]({{ '/articles/' | relative_url }}) に日付別ディレクトリで配置。最新は [`docs/articles/2026-05-17/`]({{ '/articles/2026-05-17/' | relative_url }}):

- [01 — Brief API + progressive matrix (overhead < 1%)]({{ '/articles/2026-05-17/01_brief_api_progressive' | relative_url }})
- [02 — 10 思考因子で整理する llive 思考層 (9/10 実装済)]({{ '/articles/2026-05-17/02_cognitive_factors' | relative_url }})
- [03 — 数学・単位に強い AI: MATH-01/08 内蔵計算エンジン]({{ '/articles/2026-05-17/03_math_vertical' | relative_url }})

過去の posts は `llive/docs/linkedin/` および `llive/docs/qiita/`:

- LinkedIn ja/en/zh: [overview](https://github.com/furuse-kazufumi/llive/blob/main/docs/linkedin/post_2026-05-14_overview.ja.md)
  + [v0.6.0 update](https://github.com/furuse-kazufumi/llive/blob/main/docs/linkedin/post_2026-05-16_update.ja.md)
- Qiita: [overview](https://github.com/furuse-kazufumi/llive/blob/main/docs/qiita/qiita-overview.md)
- Authoring guide (画像 / Mermaid / アニメ): [llove](https://github.com/furuse-kazufumi/llove/blob/main/docs/qiita/AUTHORING.md) / [llive](https://github.com/furuse-kazufumi/llive/blob/main/docs/qiita/AUTHORING.md)

## Reference hubs (2026-05-18 追加)

> 個別 product README で drift しがちなトピックを **portal 公式 hub** に集約:

- [Spec hub]({{ '/spec/' | relative_url }}) — FullSense Eternal Spec v1.1 章直リンク + 要件定義 8 本一覧 (v0.1〜v0.8 cognitive mesh)
- [Benchmark Policy]({{ '/benchmarks/policy/' | relative_url }}) — 系列 A/B/C/D + xs/s/m/l/xl progressive curve + honest disclosure 運用ルール
- [Recommended models]({{ '/recommended-models/' | relative_url }}) — 用途別推奨 on-prem モデル (`llama3.2:3b` 非推奨の根拠含む) + Mermaid 判断軸 + 共通 install スニペット

## Portal meta

- [Doc map]({{ '/doc_map' | relative_url }}) — one-page index of every doc across the portal + 4 product repos + maintainer memory
- [Roadmap]({{ '/roadmap' | relative_url }}) — live + planned + parked products with trigger conditions + ステータス遷移 / 依存グラフ / タイムライン
- [Comparison]({{ '/comparison' | relative_url }}) — honest vs Claude Code / Perplexity / Codex / Gemini + Honest disclosure
- [Progress log]({{ '/PROGRESS' | relative_url }}) — portal-side changelog
- [Design notes]({{ '/NOTES' | relative_url }}) — decisions, link-rot watch
- [Next session handoff]({{ '/NEXT_SESSION' | relative_url }}) — queued operator + agent work
- [Security policy](https://github.com/furuse-kazufumi/fullsense/blob/main/SECURITY.md)
- [Contributing](https://github.com/furuse-kazufumi/fullsense/blob/main/CONTRIBUTING.md)
- [License (Apache-2.0)](https://github.com/furuse-kazufumi/fullsense/blob/main/LICENSE)
- [Notice](https://github.com/furuse-kazufumi/fullsense/blob/main/NOTICE)

## Contact

- Email: `kazufumi@furuse.work`
- GitHub: [@furuse-kazufumi](https://github.com/furuse-kazufumi)

---

*FullSense ™ / llmesh ™ / llive ™ / llove ™ are trademarks of Kazufumi Furuse.*
*Code distributed under Apache-2.0; commercial license available on request.*
