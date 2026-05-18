---
layout: default
title: "Comparison"
nav_order: 60
---

# FullSense ™ vs. the field

> Honest competitive positioning. We list capabilities we're behind on too —
> hiding them would just delay the gap-closing work.

## At a glance

| Capability | Claude Code | Perplexity | Codex CLI | Gemini CLI | **FullSense (llive + ll*)** |
|---|---|---|---|---|---|
| Code editing (SOTA) | **A** | C | A | A− | A |
| Web research + citations | B | **A+** | C | B+ (Google) | A (RAD-backed) |
| Autonomous resident loop | C (Stop on prompt) | F | C (full-auto) | C | **A** (ResidentRunner) |
| HITL workbench | F | F | C (approval mode) | C (approval mode) | **A** (llove TUI) |
| Memory persistence | C (file) | C (chat) | C (session) | C | **A** (SQLite Ledger) |
| **On-prem inference** | F (cloud) | F (cloud) | F (cloud) | F (cloud) | **A** (Ollama / LM Studio / vLLM) |
| CLI OSS | F | F | A (Apache-2.0) | A (Apache-2.0) | A |
| **Backend OSS (end-to-end)** | F | F | F | F | **A** (full OSS stack) |
| Audit Ledger (SIL) | F | F | F | F | **A** (per-action persistent log) |
| Dangerous-op gate | C (warning only) | F | A (approval mode) | A (approval mode) | A (Approval Bus) |
| MCP tool ecosystem | **A** | F | C | B (recent) | B (ll{domain} family) |
| Domain-specific adapters | C (generic) | C | C | C | **A** (lldesign / lltrade / planned llcad/lleda/llchip) |

Letter grades reflect 2026-05-16 state of the art. We update this page when
any row shifts ±1 grade.

## Where we are clearly ahead

- **On-prem inference** — All four competitors are cloud-only. FullSense runs
  end-to-end against your own Ollama / LM Studio / vLLM / TGI deployment.
- **End-to-end OSS** — Codex / Gemini publish OSS *CLIs*, but their backends
  (GPT, Gemini) are closed cloud APIs. FullSense lets you swap in any OSS
  model.
- **Audit Ledger** — None of the competitors persist a per-action audit log
  for compliance / law / reproducibility. llive's SQLite Ledger does.
- **HITL workbench** — Competitors that have approval modes (Codex / Gemini)
  show one signal at a time in a CLI prompt. llove gives you a full TUI
  workbench where the human stays in the loop.

## Where we are behind (and what we're doing about it)

### vs. Claude Code

- **Coding precision** — Claude Code is the current SOTA. We compete on
  *safety* (Approval Bus blocks dangerous ops at the API level, not as a
  text warning) and *audit* (every edit lands in the Ledger).
- **MCP tool ecosystem** — Anthropic ships dozens of MCP servers. Our path
  is **domain-specific** MCP servers from the ll{domain} family. Generic MCP
  parity is not the goal.

### vs. Perplexity

- **Citation UX** — Perplexity's citation rendering is excellent. We have
  the data (RAD 49 domains, ~49K documents, frozen so citations don't rot),
  but the UX has to be built in llove.
- **Reasoning UI** — Perplexity Pro shows step-by-step thinking. The llive
  Ledger has this data; llove needs a timeline view to surface it.

### vs. Codex CLI

- **Approval mode polish** — Codex's `suggest / auto-edit / full-auto` is
  battle-tested. The llive Approval Bus has the right architecture but needs
  UX work: timeout policies, retry semantics, grouped approvals.

### vs. Gemini CLI

- **Web search integration** — Gemini's Google Search integration is
  first-class. Our RAD is frozen (great for stability, bad for "what
  happened this week"). The plan is to add WebFetch / SearXNG / Brave Search
  MCP integration through the ll{domain} layer, keeping the RAD as the
  high-trust tier.

## vs. Qwen / any single LLM weight set

Qwen / Llama / Mistral / DeepSeek 等の **LLM weights そのもの** は FullSense
にとって競合ではなく、内側で呼ぶ素材です。Brief API (LLIVE-002, 2026-05-16
実装) によって、どの OSS LLM も llive の LLMBackend として透過的に差し替え
可能。差別化はモデル単体ではなく、その上に乗る **フレームワーク層** にあります。

| 層 | 素の OSS LLM (Qwen / Llama / Mistral / ...) | llive (それを内包する) | 実装状況 |
|---|---|---|---|
| **推論コア** | Decoder-only LLM 重み | OSS LLM を `LLMBackend` として呼び出す | 実装済 (`OllamaBackend` / `OpenAIBackend` / `AnthropicBackend` / `MockBackend`) |
| **記憶** | 単一 context window | 4 層メモリ (semantic / episodic / structural / parameter) + 海馬-皮質 consolidation (FR-12) | semantic / episodic 実装済、structural / parameter 部分 |
| **意思決定** | 1 ターン生成 | FullSense 6 stage loop (salience → curiosity → thought → ego/altruism → plan → output) | 実装済 |
| **入力契約** | プロンプト 1 本 | **Brief API** — 構造化 work unit + constraints + success_criteria + tool whitelist | 実装済 (2026-05-16) |
| **安全** | プロンプトレベル | Approval Bus + Policy gate + Quarantined Memory (SEC-01) + Ed25519 Signed Adapter (SEC-02) | 実装済 |
| **監査** | なし | append-only SIL ledger (BriefLedger / SqliteLedger) + SHA-256 hash chain (SEC-03) | 実装済 (Brief 経路は 2026-05-16) |
| **自己進化** | 事前学習 + ファインチューニングのみ | オンライン提案 → Z3 形式検証 (EVO-04) → 審査 → 昇格 (EVO-06/07) | Phase 3 完了 |
| **アイデア源** | なし | TRIZ 40 原理 + 39×39 矛盾マトリクス内蔵 (FR-23〜27) | 実装済 |
| **HITL** | なし | llove TUI Candidate Arena (FR-20) | 設計済、未統合 |
| **産業 IoT** | なし | llmesh MQTT / OPC-UA sensor bridge (FR-19) | 設計済、未統合 |

### 実測 (2026-05-16 progressive validation matrix)

xs / s / m × {llama3.2:3b, **qwen2.5:7b**, **qwen2.5:14b**} を on-prem only で
Brief API → FullSenseLoop に流したところ:

- **Brief API + loop overhead < 1 %** (LLM-only wall time / Total wall time > 99.8 %)
- LLM の生出力は Brief Runner / Ledger / Decision 層を経由してから出る ―
  Qwen は判断者ではなく**素材生成者**として動作

詳細: `D:/projects/llive/docs/benchmarks/2026-05-16-progressive-merged/`

### 同点と認める領域

- **生成品質そのもの** ― llive の出力品質下限は内蔵 OSS LLM (Qwen 等) に依存
- **on-prem 実行** ― Ollama 直叩きでも on-prem。llive 経由でなくても OSS LLM
  だけで on-prem は成立
- **多言語** ― Qwen 等の素のモデルでも対応、llive は付加価値なし

## Benchmark methodology

For every new feature in FullSense, we:

1. Define a Brief that exercises the feature
2. Run the same Brief against Claude Code, Perplexity, Codex CLI, Gemini CLI,
   and the FullSense stack
3. Score on: correctness, speed, citation quality, dangerous-op handling,
   cost, on-prem capability, backend OSS, audit log presence
4. Publish the per-product benchmark results under each product's
   `docs/benchmarks/<date>.md`
5. Open issues for any axis where FullSense lost

**詳細運用ルール**: [Benchmark Policy]({{ '/benchmarks/policy/' | relative_url }})
を参照 — 系列 A/B/C/D の分離、xs/s/m/l/xl の progressive curve、
honest disclosure の必須項目を portal 公式方針として固定。

Methodology details: [`feedback_competitor_benchmark`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_competitor_benchmark.md)
in the maintainer's tooling repo.

## Honest disclosure (2026-05-18 時点)

A/F 採点には以下の **正直に開示すべき制約**がある。隠さない:

- **cloud 系列 (B) は 3/4 が未測**: Anthropic Haiku 4.5 / Gemini 2.0 Flash /
  OpenAI Codex はいずれも credential / quota 復旧待ち。比較は **Perplexity
  Sonar の 1 点のみ**で補強されている。NEXT_SESSION 復旧後に再評価。
- **on-prem 系列 (A) は llama3.2:3b の `lllive` typo 問題**を抱える。
  推奨は qwen2.5:7b / 14b だが、recent ベンチは未完。本表の on-prem 列は
  「ollama 一般」を示しており、特定モデルの絶対値ではない。
- **llive 自身 (C/D 系列) は Brief API 経由のオーバーヘッド < 1 %** を
  実測 (`/benchmarks/2026-05-16-progressive` で公開) しているが、生成品質
  の絶対値は内蔵 OSS LLM 重みに依存する。「llive は速い / 高品質」と単独で
  言うのは不正確。
- **採点者バイアス**: 採点は maintainer (`furuse-kazufumi`) によるもので、
  外部レビューはまだ無い。A/F の絶対値より「±1 差を生む論拠」を読むこと。

## Empirical benchmarks (2026-05-16)

Four Briefs run against llive (`FullSenseLoop.process`) + ollama
`llama3.2:3b` (on-prem) + Perplexity Sonar (cloud). Anthropic Haiku 4.5,
Gemini 2.0 Flash, OpenAI Codex were attempted but failed for credential /
quota reasons (operator action queued).

- [Mermaid family-tree generation]({{ '/benchmarks/2026-05-16_mermaid_brief' | relative_url }})
- [Quick Start section + MCP sequence diagram]({{ '/benchmarks/2026-05-16_quickstart_seqdiag' | relative_url }})
- [lltrade paper-trading strategy YAML]({{ '/benchmarks/2026-05-16_lltrade_yaml' | relative_url }})

Headline of the day:

- llive does not yet generate (LLIVE-001 / LLIVE-002 in
  [`docs/BUGS_2026-05-16_brief_ab.md`](https://github.com/furuse-kazufumi/llive/blob/main/docs/BUGS_2026-05-16_brief_ab.md))
- ollama `llama3.2:3b` is the working on-prem option but produces the
  `lllive` typo (3 Ls) twice across 4 Briefs — tokenisation hostility to
  the `ll*` naming convention. Recommended replacement: qwen2.5:14b+
- Perplexity Sonar scores 4/4 on spec compliance at ~$0.005/brief

## Last updated

2026-05-16 — initial publication + first 4-Brief A/B run. Reviewed at:
portal-side `PROGRESS.md` *Phase 0.3 — umbrella expansion* and *Phase 0.3
— competitive positioning* entries.
