# LinkedIn 投稿 — 2026-05-17 技術者向け統合 (日本語版)

🚀 **1 日で要件 32 件 + 実装 2200 行 + テスト 78 件 + ベンチ 4 種 — 自己進化型 LLM フレームワーク llive 開発記**

本日 (2026-05-17)、自己進化型モジュラー記憶 LLM フレームワーク **llive** に対し以下を達成しました。

✅ **Brief API end-to-end 完成** — 外部クライアント (lldesign / lltrade / MCP) から構造化 work unit を渡せる API。schema / loader / ledger / runner / CLI / MCP を 1 セッションで実装 (5 日見積を 1 日で完走)
✅ **要件 32 件追加** — v0.7-MATH 8 件 / v0.8-CABT 7 件 / v0.9-CREAT 5 件 / v1.0-COG-FX 4 件 / v2.0-ORG-FX 8 件
✅ **テスト 936 → 1014 PASS / 0 fail / 0 regression**
✅ **ベンチマーク 4 種実施** — progressive matrix 15 セル / fair re-bench / quiz Debug + Release (mean/stdev 統計付き)
✅ **honest disclosure** — 最初のベンチで「llive 4/4 OK 134-184ms」という異常に速い結果が出たが、調査の結果 LLMBackend 未 attach の template fallback だったと判明。教訓を memory に保存し、fair 再走 (32-51s) で公開

💡 **重要な発見**: 「llive の付加価値は速度ではなく構造 (ledger / approval / governance / grounding / 6 stage trace)」「Local 環境で AI を安全に責任を持って使う」というポジショニングを確立。

📊 **progressive matrix 主要結果** (xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b}, on-prem only):
- Brief API オーバーヘッド < 1 %
- 全 15 セル decision=note (loop は token 圧力に対し完全 stable)

🔗 詳細記事 (11 本 + 統合 2 本) と raw データ:
<https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17>

#LLM #Agent #OnPrem #Ollama #Python

著者: 古瀬 和文（ぷるやん）/ 古瀬 和文 (puruyan)
