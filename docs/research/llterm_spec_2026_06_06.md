# llterm — Claude Code 自走端末 設計 spec (2026-06-06)

> ユーザー発案 (2026-06-06): 「claude code 専用ターミナル。表示の互換性は維持しつつ、ccr によるリブートとか
> ultracode の実行とか、claude code 自身から制御構文を渡すとその通りに動作するターミナル。
> csv-pandas-bridge の思想を入れてもいい」。同日のブレスト対話で要件・方式・命名を確定した記録。
> 関連: [[project_ccr_automation_limits]] / claude-auto.mjs (既存 prototype) / llove F23/F24 (姉妹要件)

## 0. 一行定義

**llterm = Claude Code を公式 protocol (stream-json / --session-id / --resume) でホストし、
Claude 自身が発火する構造化制御 (再起動 / effort 変更 / タスク注入 / セッション分岐) を
HITL gate + 監査つき制御プレーンで実行する、自走特化の端末/ランチャ。**

## 1. 背景と動機 (将と馬)

- **将 (大目標)**: Claude Code が自走・自律動作できる形。「Claude は自力で exit/再起動/再ログインできない」
  (memory: project_ccr_automation_limits) という構造的制約を、**Claude のライフサイクル外の別プロセス
  (llterm) が制御構文を傍受して代行する**ことで、認証切れを除き突破する。
- **馬 (足場)**: ①公式 CLI の閉ループ部品 (PoC 実証済、§7) ②既存 ccr/claude-auto.mjs
  (= 事実上の prototype: .rotate-signal / [ROTATE:CRITICAL] / PTY 注入) ③llove term の
  シェル部品 (builtins/command/completion/palette)。
- ユーザーの指針: 「将を射んとする者はまず馬を射よ」— 完成形を一足飛びに作らず、足場から段階実装する。

## 2. 確定要件 (ユーザー対話 2026-06-06)

| # | 要件 | 出所 |
|---|---|---|
| R1 | Claude Code の**自走・自律動作**が主目的 (自己制御の拡張) | ユーザー回答 |
| R2 | **PowerShell が持つ機能と同等のシェル機能**を端末自身が持つ (素通しではない) | ユーザー訂正 |
| R3 | **長テキスト蓄積でも固まらない**。Warp は実際に固まりアンインストールした (生の反例) | ユーザー実体験 |
| R4 | **ちらつき問題の根本解消** (現 TUI は外部プロセス出力と再描画が衝突しフリッカー) | ユーザー要望 |
| R5 | 制御構文は **csv-pandas-bridge 思想** (生ストリーム ↔ 構造化制御の明示的中間層) | ユーザー発案 |
| R6 | 個人利用前提。名称衝突チェックは不要 (llterm で確定) | ユーザー回答 |
| R7 | protocol を再発明しない — Anthropic 自身が器 (デスクトップアプリ/web/Agent SDK) を進化させ続けるため | 対話合意 |

## 3. アーキテクチャ (3 層)

```
┌─ L3: 表示 + シェル層 (馬2; 基盤選定は§11未決)
│   ・PowerShell 同等シェル (R2)。llove term 部品は再利用候補だが Textual 固定ではない (R3)
│   ・表示は TUI 素通しではなく stream-json イ