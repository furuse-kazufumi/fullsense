# Security Policy — FullSense Portal

This repository is the **brand portal** for FullSense. It contains only
documentation and static-site config; no executable code is shipped from
this repo.

## Where to report

If you have found a vulnerability in **one of the FullSense products**, please
report it in **that product's repository**, not here:

| Product | Repository | Security tab |
|---------|------------|--------------|
| llmesh | [furuse-kazufumi/llmesh](https://github.com/furuse-kazufumi/llmesh) | Use the repo's "Security" → "Report a vulnerability" |
| llive  | [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)   | Same — preferred per `llive/SECURITY.md` |
| llove  | [furuse-kazufumi/llove](https://github.com/furuse-kazufumi/llove)   | Same |

For issues **specific to this portal** (e.g. cross-site scripting in a Mermaid
diagram, a malicious link, content tampering, trademark misuse), report
privately via:

- **GitHub Security Advisories** — preferred. "Security" tab → "Report a
  vulnerability" on this repo.
- **Email** — `kazufumi@furuse.work` with the subject prefix
  `[fullsense portal security]`.

## Out of scope for this repository

- Vulnerabilities in `just-the-docs`, Jekyll, or Mermaid — report upstream.
- Vulnerabilities in the products themselves — see the table above.
- Phishing / typo-squatted PyPI packages (`fullsens`, `fulisens`, etc.) — these
  are tracked in `llive/docs/v1.0_migration_plan.md`; please email if you
  spot one.

## Disclosure timeline

For in-scope portal issues:

- Acknowledgement: within 5 business days
- Fix: target 14 days from acknowledgement (most portal issues are content
  edits, so faster than the product-side SLA)
- Coordinated public disclosure with the reporter
