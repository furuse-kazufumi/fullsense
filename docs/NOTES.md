---
layout: default
title: "Notes"
nav_order: 91
---

# FullSense Portal — Design Notes

> Free-form notes. Promote anything stable into `PROGRESS.md` or the spec.

## Decisions

### Why a separate portal repo (not a section in `llive`)?

- Brand neutrality — `FullSense ™` is the parent; pinning the portal inside
  one product (e.g. `llive`) would imply that product is the "real" one.
- Independent Pages URL — `furuse-kazufumi.github.io/fullsense/` reads cleanly
  alongside the three product Pages sites.
- License separation — the **code** Apache-2.0 license lives in each product;
  the **brand & spec** live here, so a `LICENSE` for documentation in this
  repo doesn't pollute the product-side license discussion.

### Why `just-the-docs` (not `chirpy` / `minima`)?

- Search out of the box, side-nav, anchor links — matches what the product
  Pages sites already use, so the visual style is consistent.
- Mermaid support via `mermaid:` config block (no plugin install).
- Remote theme — zero local Gemfile maintenance.

### Why `pip install llmesh-suite` (not `pip install fullsense`)?

- `fullsense-*` PyPI namespace is **reserved for v1.0 rename** (see
  `llive/docs/v1.0_migration_plan.md`). Until that migration, `llmesh-suite`
  remains the all-in-one installer to avoid a confusing partial rename.

## Link-rot watch list

The portal points to many files inside `llive`. If those move, update here:

| Portal target | Linked file |
|---------------|-------------|
| Spec | `llive/docs/fullsense_spec_eternal.md` |
| P2P RFC | `llive/docs/llmesh_p2p_mesh_rfc.md` |
| EDLA historical | `llive/docs/references/historical/edla_kaneko_1999.md` |
| v1.0 migration | `llive/docs/v1.0_migration_plan.md` |
| Trademark drafts | `llive/docs/legal/trademark/` |
| LinkedIn overview | `llive/docs/linkedin/post_2026-05-14_overview.ja.md` |
| LinkedIn update | `llive/docs/linkedin/post_2026-05-16_update.ja.md` |
| Qiita overview | `llive/docs/qiita/qiita-overview.md` |
| Authoring guide | `llove/docs/qiita/AUTHORING.md`, `llive/docs/qiita/AUTHORING.md` |

Implemented as `.github/workflows/link-check.yml` (Lychee). Runs on
docs/README push, on docs PRs, weekly (Mon 18:00 UTC), and on manual
dispatch. Scheduled failures open a `docs, link-rot` issue automatically.
The CI does **not** fail the build (`fail: false`) — link rot is reported
out-of-band so docs PRs stay mergeable when the rot is in an unrelated
section.

## Deferred

- **GitHub Discussions** — enable once the three product repos have steady
  inbound traffic. Until then, issues + email are sufficient.
- **Sponsors / funding link** — defer until v1.0 (post PyPI rename).
- **Translation infra** — articles are already authored in ja/en/zh in the
  product repos; centralising them in the portal would duplicate the source
  of truth. Re-evaluate after the v1.0 rename, when stable URLs make
  centralisation worthwhile.
