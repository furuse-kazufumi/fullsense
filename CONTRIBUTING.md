# Contributing to FullSense (Portal)

Thanks for your interest in the **FullSense umbrella portal**.

## What lives here vs. in the product repos

| If your contribution is about… | Open a PR in… |
|--------------------------------|---------------|
| Bugs / features in `llmesh`, `llive`, or `llove` | the matching **product repo** |
| The FullSense Spec v1.1 (architecture, axes) | [`llive/docs/fullsense_spec_eternal.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md) — the spec source of truth lives in `llive` until v1.0 |
| Trademark drafts (JP/US/EU) | [`llive/docs/legal/trademark/`](https://github.com/furuse-kazufumi/llive/tree/main/docs/legal/trademark) |
| **Portal landing page text / family-tree diagram / aux links / styling** | **this repo (`fullsense`)** |
| Portal `_config.yml` / Jekyll theme overrides | this repo |
| New links to articles / demos / press | this repo (`docs/index.md`) |
| Typos in `README.md` here | this repo |

## License & DCO

All product code is **Apache-2.0** with an optional separate commercial
license (see `LICENSE-COMMERCIAL` in `llive`). Documentation in this portal
repo is **Apache-2.0** (see `LICENSE` here).

By submitting a PR you agree your contribution is licensed under
Apache-2.0. Please sign off each commit with the **Developer Certificate of
Origin 1.1**:

```bash
git commit -s -m "docs: fix typo in family tree"
```

`-s` appends `Signed-off-by: Your Name <your@email>` — that is your DCO
sign-off. Full DCO text: <https://developercertificate.org/>.

## Local preview

```bash
# requires Ruby 3.x + Bundler
gem install bundler jekyll
cd docs
bundle init
bundle add github-pages --group jekyll_plugins
bundle exec jekyll serve --baseurl ''
# open http://127.0.0.1:4000
```

GitHub Pages will rebuild automatically from `docs/` on push to `main`.

## Style

- Keep `docs/index.md` short — link out to product Pages sites for detail.
- Mermaid diagrams: use the existing family-tree colour scheme (yellow root,
  blue/green/pink leaves) for visual consistency.
- Don't import product-side article text — link out instead, to keep the
  portal lean and link-rot recoverable.

## Trademark

`FullSense ™`, `llmesh ™`, `llive ™`, and `llove ™` are trademarks of
Kazufumi Furuse. PRs that use these names in a confusing or commercial way
will be asked to revise. See the trademark drafts in
[`llive/docs/legal/trademark/`](https://github.com/furuse-kazufumi/llive/tree/main/docs/legal/trademark)
for the (in-progress) usage policy.
