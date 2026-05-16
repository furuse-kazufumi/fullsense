# FullSense ™

> **Umbrella brand & specification** for `llmesh`, `llive`, `llove`.

FullSense is the parent brand under which three open-source products are
organised. This repository is the **portal** — code lives in each product
repository.

## Family

```
                  FullSense ™   (umbrella brand & spec v1.1)
                  /     |     \
              llmesh   llive   llove
              (hub)   (memory) (TUI)
```

| Product | Role | Source | Docs |
|---------|------|--------|------|
| **llmesh** | Secure LLM hub / on-prem MCP server | [github.com/furuse-kazufumi/llmesh](https://github.com/furuse-kazufumi/llmesh) | [Pages](https://furuse-kazufumi.github.io/llmesh/) |
| **llive** | Self-evolving modular memory LLM framework | [github.com/furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive) | [Pages](https://furuse-kazufumi.github.io/llive/) |
| **llove** | TUI dashboard / HITL workbench | [github.com/furuse-kazufumi/llove](https://github.com/furuse-kazufumi/llove) | [Pages](https://furuse-kazufumi.github.io/llove/) |

Spec: see [llive/docs/fullsense_spec_eternal.md](https://github.com/furuse-kazufumi/llive/blob/main/docs/fullsense_spec_eternal.md)
for the FullSense Spec v1.1 reference.

## Install

```bash
# install everything in one shot
pip install llmesh-suite

# or individually
pip install llmesh
pip install llmesh-llive
pip install llmesh-llove
```

PyPI rename to `fullsense-*` is planned at v1.0 — see
[llive/docs/v1.0_migration_plan.md](https://github.com/furuse-kazufumi/llive/blob/main/docs/v1.0_migration_plan.md).

## License

The code in each product repo is licensed under **Apache-2.0** (with the
option of a separate commercial license, see `LICENSE-COMMERCIAL` in
`llive`). The brand name **FullSense ™** is a trademark of Kazufumi Furuse;
see [llive/TRADEMARK.md](https://github.com/furuse-kazufumi/llive/blob/main/TRADEMARK.md).

## Demos

| Static gallery | <https://furuse-kazufumi.github.io/llove/scenarios/> |
| Animated gallery | same page, Animated section |
| Clustering demo | <https://furuse-kazufumi.github.io/llmesh/demos/clustering_demo> |

## Repository files

| File | Purpose |
|------|---------|
| [`LICENSE`](LICENSE) | Apache-2.0 (portal docs) |
| [`NOTICE`](NOTICE) | Trademark + attribution + third-party |
| [`SECURITY.md`](SECURITY.md) | Where to report portal vs. product issues |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | What belongs here vs. product repos, DCO sign-off |
| [`docs/index.md`](docs/index.md) | Landing page (rendered by GitHub Pages) |
| [`docs/PROGRESS.md`](docs/PROGRESS.md) | Portal-side project log |
| [`docs/NOTES.md`](docs/NOTES.md) | Design decisions + link-rot watch list |
| [`docs/_config.yml`](docs/_config.yml) | Jekyll `just-the-docs` config |

## Contact

`kazufumi@furuse.work`
