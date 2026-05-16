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

### Open items

- [ ] Add GitHub remote (`gh repo create furuse-kazufumi/fullsense --public`),
      push `main`, enable Pages from `docs/`
- [ ] Verify `mermaid` renders correctly under `just-the-docs` remote theme
      (the theme needs `enable_copy_code_button` + custom JS for Mermaid;
      revisit after first deploy)
- [ ] Add `docs/spec/` mirror of the FullSense Spec v1.1 once it stabilises in
      `llive/docs/` (currently the portal links out to llive for the spec)
- [ ] Add Open Graph card image (1200×630 PNG) for social previews
- [ ] Replace bare LinkedIn/Qiita article links with a curated `docs/articles/`
      index once the article-pause (see `feedback_articles_pause.md`) is
      lifted

## References

- Brand introduction memo — `~/.claude/.../memory/project_fullsense_brand.md`
- Spec source of truth — `llive/docs/fullsense_spec_eternal.md`
- Trademark drafts — `llive/docs/legal/trademark/`
