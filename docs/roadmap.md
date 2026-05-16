---
layout: default
title: "Roadmap"
nav_order: 50
---

# FullSense ™ — Roadmap

> What is shipping, what is planned, and what is parked with trigger conditions.

## Live products (5)

| Product | Status | Next milestone |
|---|---|---|
| [llmesh](https://github.com/furuse-kazufumi/llmesh) | stable v1.5 | v1.6 (OPC-UA + MQTT) |
| [llive](https://github.com/furuse-kazufumi/llive) | beta v0.6 | C-2 (`@govern` → ProductionOutputBus) |
| [llove](https://github.com/furuse-kazufumi/llove) | beta v0.6 | F23/F24 (PowerShell shell + Claude Code integration) |
| [lldesign](https://github.com/furuse-kazufumi/lldesign) | alpha v0.0.1 | v0.1 (Mermaid generator + llove HITL) |
| [lltrade](https://github.com/furuse-kazufumi/lltrade) | alpha v0.0.1 (paper only) | v0.1 (Backtrader adapter) |

## Planned — design / engineering family

| Product | Scope | **Trigger condition for skeleton bootstrap** |
|---|---|---|
| **llcad** | Machine CAD operator emulation via code-CAD (OpenSCAD / CadQuery / Build123d) | OpenSCAD / CadQuery / Build123d become stable RAD references + user requests a machine-design task |
| **lleda** | Electronic design automation: schematic + PCB (KiCad CLI + JITX-style DSL) | KiCad Python API or JITX DSL becomes stable LLM target with reproducible sample |
| **llchip** | Semiconductor IC layout (OpenLane / Magic VLSI orchestration, RL-assisted floorplan) | OpenLane / Magic VLSI installable on Windows/WSL + test chip GDSII generated |

## Planned — domain research family

| Product | Scope | **Trigger condition** |
|---|---|---|
| **llmed** | Medical literature curation, evidence synthesis | A medical-domain user adopts FullSense + RAD `medicine` corpus reaches > 5K documents |
| **llpaper** | Academic drafting (LaTeX / Pandoc + citation graph) | Stable Zotero / arXiv MCP server + user submits a real paper through the loop |
| **llmaterial** | Materials science — phase diagrams, simulation orchestration | RAD `materials` corpus + user with materials-domain pain |
| **llops** | DevOps / SRE — incident response, runbook execution | RAD `devops` / `sre` corpus + Approval Bus matured enough for production change |
| **llhft** | High-frequency / market-making — **out of lltrade scope** | Audited release process + dedicated infra. Never on `lltrade` main. |

## Parking rules

A "parked" product is a name + 1-line scope + trigger condition. It is **not**:

- A skeleton repository (none created yet)
- A PyPI reservation (no `llmesh-llcad` etc. registered)
- A promise of delivery

The point of parking is **architectural foresight without commitment**. The
moment a trigger condition fires, the corresponding product gets the same
13-file skeleton treatment as lldesign / lltrade.

## Naming convention

All FullSense products use the prefix `ll` followed by a 4–8 character domain
hint. Trademarks are registered umbrella-wide (`FullSense ™` covers all
`ll*` derivatives) — see [trademark drafts](https://github.com/furuse-kazufumi/llive/tree/main/docs/legal/trademark).

## Versioning gates

| Version line | Hard rules |
|---|---|
| **v0.x** | API may break between minors. Public alpha. |
| **v1.0** | PyPI rename to `fullsense-*` namespace. API stabilises. lltrade enters live-trading audit branch (separate). |
| **v2.0+** | P2P mesh (LLMesh v2.x, Winny-inspired) + cross-product knowledge fusion |
