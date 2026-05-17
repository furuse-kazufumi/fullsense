# LinkedIn 投稿 — 2026-05-17 開発履歴版 (日本語版)

📜 **llmesh → llove → llive — FullSense 3 製品の開発履歴と設計コンセプト**

私 (古瀬 和文 / ぷるやん) が研究開発している **FullSense ™** umbrella の 3 製品の歩みです。

🧩 **llmesh** (最古参) — secure LLM hub
- v1.5.0 完了 (MTEngine + XbarRChart + CUSUMChart + CLI)
- 設計: 複数 LLM (OpenAI / Anthropic / Ollama 等) を統合し MCP プロトコルで配信。SPC を埋め込み産業 IoT に直結

🎮 **llove** (TUI HITL workbench)
- v0.2.2 PyPI 公開 (2026-05-09)
- F15 ブラウザ並み表示 (Markdown / SVG / Mermaid)
- F16 マルチゲーム LLM 対局アリーナ (chess / go / mahjong / poker)
- F22 テトリスデモ / F23 PowerShell 互換シェル / F24 Claude Code 統合
- F25 連携基盤 (llove ↔ llmesh ↔ llive を MCP で繋ぐ shim)
- 設計: Textual ベース、デモを多数用意して「動きで魅せる」

🧠 **llive** (本日 5 日目) — self-evolving modular memory LLM framework
- 2026-05-13 発足、v0.1.0 (Phase 1 MVR)
- 2026-05-14: v0.3 → v0.4 → v0.5 (Phase 3/4/5 同日完走)
- 2026-05-16: v0.6.0 (9 axes skeleton + Apache 2.0 + FullSense umbrella)
- 本日: Brief API + 32 件要件 + 1014 PASS

🎯 **設計コンセプト 6 柱**:
1. Local 環境こそ AI の本来の居場所
2. 責任所在を architecture level に持ち込む
3. 多側面の思考を構造化 (10 思考因子)
4. TRIZ で創造を構造に持ち込む
5. Honest disclosure を研究の核に
6. ファミリーで作る (3 製品で 1 つの世界観)

⭐ **差別化要素**:
- cloud LLM (GPT/Claude/Gemini): on-prem / 監査ログ / 災害時動作で勝つ
- Agent framework (LangChain/CrewAI): HITL TUI / 形式検証 / TRIZ 内蔵で勝つ
- Wolfram Alpha: 完全 OSS + LLM 統合 + 監査ログで勝つ

🔗 詳細統合記事: <https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/QIITA_HISTORY.md>

#OSS #LLM #ローカル環境 #開発履歴 #認知科学

著者: 古瀬 和文（ぷるやん）
