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

## 1. 旗艦 `llmesh` × HPE 衝突（→ §1.1 で解決済）

bare `llmesh` (PyPI / GitHub) は **Hewlett Packard (HPE)** が保有:

- PyPI `llmesh` v0.1.4 = **"HPE LLM Agentic Tool Mesh Platform"** / author: Antonio Fin
  (antonio.fin@**hpe.com**) / repo: **`HewlettPackard/llmesh` (90★)**。
- **同名・同ドメイン**（LLM オーケストレーション mesh / Intelligent Plugins）。repir/repir
  (情報検索) より深刻 — 大企業・同領域の真っ向衝突。

FullSense の旗艦は PyPI を **`llmesh-mcp`** で公開しているため完全一致は回避済だが、**ブランド名
「llmesh」自体は HPE と競合**。当初は戦略課題として保留したが、**2026-05-24 にユーザー方針決定で
クローズ**（下記 §1.1）。

### 1.1 解決方針 (2026-05-24, ユーザー決定)

**llmesh はリネームしない。** 根拠:

- **llmesh の位置づけ = 規格/標準 (spec) の枠**（売り物ではない）。表現コントラクト / ハブ・
  プロトコル層で、products（llive / llove / 公開フェイス）がその上に乗る
  ([[project_llmesh_representation_layer]]、mcp-spatial-asset-profile と同系)。
- よって **独立 OSS 原則は矛盾せず精緻化**: 独立販売層 = products / llmesh = 共有 spec。
- HPE 衝突は **low-stakes**（llmesh は marketed product でなく内部 spec 名）。PyPI 完全一致も
  `llmesh-mcp` で回避済。
- **公開ブランド = FullSense**（衝突確認済 2026-05-24）: PyPI `fullsense` / `fullsense-mcp` 空き、
  GitHub 同名は無関係の極小のみ（`MiguelEstevesMF/FullSense` 1★ 別ドメイン、
  `fullsense/fullsense` = profile config）。

→ **名前問題はクローズ**。llmesh は内部 spec/engine 名として維持、FullSense が公開フェイス。
統合（products への要素統合）の具体実装は後日・結合判断はユーザー領域（Claude は勝手に統合しない）。

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
| **lldarwin** | bare 空き(404) / `llmesh-lldarwin` 空き(404) | **ZERO（完全クリーン）** | ✓ **採用確定**=選択圧PJ (2026-05-25, ユーザー決定「記憶しやすい」)。注: "darwin"単語は混雑(V7 darwin-py / sgould drwn / llvm-libtool-darwin / Apple Darwin OS / SparkCognition Darwin AutoML)だが連結形 lldarwin の完全一致は皆無。予約は実装着手後 (doc §3 ルール: placeholder 乱立回避) |

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
