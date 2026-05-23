---
layout: default
title: "ll- ファミリー名 衝突監査 + PyPI 予約"
parent: "Research"
nav_order: 94
---

# ll- ファミリー名 衝突監査 + PyPI 予約 (2026-05-24)

> RepIR → llrepr 改名 ([[llrepr_poc_2026_05_24]]) を機に「他の ll- 名は大丈夫か / PyPI 未登録が
> ないか」をユーザーが懸念 → FullSense ファミリー名を GitHub + PyPI で一括監査した記録。
> **重要発見: 旗艦 `llmesh` が HPE のプロダクトと衝突。**

---

## 1. ⚠ 旗艦 `llmesh` × HPE 衝突（要戦略判断）

bare `llmesh` (PyPI / GitHub) は **Hewlett Packard (HPE)** が保有:

- PyPI `llmesh` v0.1.4 = **"HPE LLM Agentic Tool Mesh Platform"** / author: Antonio Fin
  (antonio.fin@**hpe.com**) / repo: **`HewlettPackard/llmesh` (90★)**。
- **同名・同ドメイン**（LLM オーケストレーション mesh / Intelligent Plugins）。repir/repir
  (情報検索) より深刻 — 大企業・同領域の真っ向衝突。

FullSense の旗艦は PyPI を **`llmesh-mcp`** で公開しているため完全一致は回避済だが、**ブランド名
「llmesh」自体は HPE と競合**。旗艦リネームは FullSense 全体（llive/llove/記事/portal）へ波及する
重い判断のため、**戦略課題として保留・ユーザー判断待ち**（本監査では事実提示のみ）。

> 選択肢の方向性（未決）: (a) `llmesh-mcp` で差別化し共存、(b) 旗艦サブブランド名を別途用意、
> (c) 静観。いずれも結合・ブランド判断はユーザー ([[feedback_fullsense_project_priority]])。

---

## 2. ll- ファミリー 監査結果

| 名前 | PyPI (bare / `llmesh-<n>`) | GitHub 同名衝突 | 状況 |
|---|---|---|---|
| **llmesh** | bare=**HPE 取得済** / `llmesh-mcp` 公開済 | **HewlettPackard/llmesh 90★** | ⚠ ブランド衝突（要判断） |
| llive | bare 空き / `llmesh-llive` 公開済 | なし（無関係 ≤4★） | ✓ 公開済 |
| llove | bare 空き / `llmesh-llove` 公開済 | なし（別語 8★） | ✓ 公開済 |
| llrepr | bare 空き / `llmesh-llrepr` **予約** | クリーン | ✓ 本日予約 |
| lleval | bare 空き / `llmesh-lleval` **予約** | mattn/lleval-vim 3★（別用途, コード実行サービス） | ✓ 本日予約 |
| lltrade | bare 空き / `llmesh-lltrade` **予約** | クリーン (0★) | ✓ 本日予約 |
| lldesign | bare 空き / `llmesh-lldesign` **予約** | クリーン (0★) | ✓ 本日予約 |
| llcraft | bare 空き / `llmesh-llcraft` 空き | ほぼクリーン (1件 0★) | 研究段階・未予約 |
| llgov | bare 空き / `llmesh-llgov` 空き | 完全クリーン | 研究段階・未予約 |
| llrisk | bare 空き / `llmesh-llrisk` 空き | 完全クリーン | 研究段階・未予約 |
| llgrow | bare 空き / `llmesh-llgrow` 空き | 完全クリーン | 研究段階・未予約 |

---

## 3. 本日の予約 (squat 防止)

PyPI に **placeholder 0.0.1**（Apache-2.0, GitHub repo を指す）を publish して名前確保:

- <https://pypi.org/project/llmesh-llrepr/>
- <https://pypi.org/project/llmesh-lleval/>
- <https://pypi.org/project/llmesh-lltrade/>
- <https://pypi.org/project/llmesh-lldesign/>

GitHub: `furuse-kazufumi/llrepr` 予約 repo 作成済（Comet 経由, Apache-2.0）。
lleval/lltrade/lldesign は既存 repo あり。

**未予約（意図的）**: llcraft / llgov / llrisk / llgrow は研究 prior-art 段階で実体未確定 →
使わない名の placeholder 乱立は PyPI hygiene に反するため見送り。実体が固まった段階で予約する。

---

## 4. 確立した運用ルール

公開ブランド名（OSS / パッケージ / プロジェクト）は **提案・採用前に GitHub org + 同名 repo の
star + PyPI 名（bare と `llmesh-<n>` 両形）の衝突を必ず実測確認**する。記憶・直感で判断しない。
採用後は GitHub 予約 repo（README+LICENSE）+ PyPI placeholder で確保。
(memory: `feedback_name_collision_check`)

---

## Sources / 関連

- [[llrepr_poc_2026_05_24]] — RepIR→llrepr 改名の起点
- PyPI bare `llmesh` info: HPE "LLM Agentic Tool Mesh", `HewlettPackard/llmesh`
- 確認コマンド: `pypi.org/pypi/<name>/json` (200=取得済) / `api.github.com/search/repositories?q=<name>+in:name&sort=stars`
