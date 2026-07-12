# Motion Pack

Reusable animated SVG article assets.

Design rules:

- Static-safe: the authored frame already communicates the point.
- Qiita/imgix-safe: no `animateMotion` or `mpath`; only `animate` and `animateTransform`.
- Small enough to embed as raw GitHub URLs in Qiita articles.
- Language-light: labels are generic and reusable across articles.

Recommended use:

- `loop_observe_gate_repair.svg`
  - Approval loop, harness, fail-closed, drift-repair articles
- `worldmodel_rollout_strip.svg`
  - World model, planning, latent rollout, safe commit articles
- `qd_archive_pulse.svg`
  - QD, archive, novelty, coverage, evolution articles
- `human_gate_funnel.svg`
  - Human-in-the-loop, supervision-first, permission boundary articles
- `backend_swap_compare.svg`
  - Backend abstraction, non-transformer swap, interface stability articles
- `rocket_launch_land_cycle.svg`
  - onocollo rocket landing toy, launch-to-landing timeline, control-regime articles

Build / refresh:

```powershell
py -3.11 tools/build_article_motion_pack.py
```

Raw URL pattern:

```text
https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/motion_pack/<file>.svg
```

Notes:

- The raw URL becomes usable only after the file is committed on `main` and pushed.
- For Qiita / imgix embeds, prefer a cache-busted URL such as
  `.../<file>.svg?v=1` and increment `v` after visible updates.
