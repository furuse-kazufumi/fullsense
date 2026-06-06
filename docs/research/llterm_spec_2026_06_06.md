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
| R8 | **Unicode 幅の正確な等幅表示**: ①② 等で桁ずれしない。原因 = East Asian Width Ambiguous 文字の幅計算 (1幅) とCJK フォント描画 (2幅) の不一致 → 幅テーブルを日本語ロケール準拠で自前統一して根治 | ユーザー要望 |
| R9 | **ANSI カラー対応** (PowerShell 同様の色付き表示) | ユーザー要望 |
| R10 | **IME 入力欄の安定**: 描画処理中に IME の文字入力欄が飛び回らない。原因 = IME composition window がコンソールカーソルに追従し、TUI 再描画のカーソル移動に引きずられる。根治 = 入力欄を出力描画から分離した固定領域にし、出力描画はカーソルを動かさない | ユーザー要望 (llterm を作りたい理由の 1 つ) |
| R11 | **複数行貼り付け対応**: 入力欄は複数行ペーストを 1 つの入力として保持し、ペースト内改行で誤送信しない (bracketed paste の正しい実装)。送信前に編集可能。現 TUI/ccr が CR/LF 正規化で格闘してきた連結バグ問題の根治 | ユーザー要望 |
| R12 | **送信モデル**: Enter は常に改行挿入のみ。送信は **Ctrl+Enter / Shift+Enter** の明示操作 (現 TUI の Enter=送信と逆)。誤送信を構造的に防止。従来端末では Enter と Shift+Enter が同一バイト (\r) で区別不能だが、自前入力欄はキーイベント直取りで実装可能 | ユーザー要望 |
| R13 | **矢印キーのモデル**: 矢印キーは常にカーソル移動 (複数行入力内の上下左右)。**Ctrl+矢印 / Shift+矢印**で補完候補の選択・入力履歴の切り替え。現 TUI の「複数行編集中に ↑ で履歴に飛ばされる」衝突を排除 | ユーザー要望 |

## 2.5 v1 スコープ (2026-06-06 ユーザー確定)

> **「表示は今の表示方法と互換でよく、入力欄だけが別扱い」** — v1 はこの絞り込みで作る。

- **表示 (v1)**: リッチ TUI の完全再現は目標にしない。claude を stream-json headless で動かすと
  TUI の入力欄は存在しなくなるため、出力イベントを「今の見た目と互換」に素朴にレンダリング
  (テキスト + ANSI 色) すれば足りる。
- **入力欄 (v1 の核)**: 出力から分離した固定領域のミニエディタ (R10-R13)。
- R3 (長テキスト) / R4 (ちらつき) / R8 (桁ずれ) の**完全根治は v2 進化先**。ただし v1 でも
  入力欄分離により IME 飛び (R10) は解消し、追記型描画によりちらつきの主因は自然に減る。

## 3. アーキテクチャ (3 層)

```
┌─ L3: 表示 + シェル層 (馬2; 基盤選定は §11 未決)
│   ・PowerShell 同等シェル (R2)。llove term 部品は再利用候補だが Textual 固定ではない (R3)
│   ・表示は TUI 素通しではなく stream-json イベントの自前レンダリング (本命案):
│     - ちらつき根治 (R4): 全画面再描画でなくイベント追記描画
│     - 長テキスト耐性 (R3): リングバッファ + 仮想スクロールを自分で設計できる
│     - 等幅根治 (R8): East Asian Width を日本語準拠 (Ambiguous=wide) で統一した幅計算 + ANSI カラー (R9)
│     - IME 安定 (R10): 入力欄を固定領域に分離、出力描画はカーソル非移動 → composition window が飛ばない
│     - 複数行ペースト (R11): bracketed paste を入力欄が一級サポート
│     - 送信モデル (R12): Enter=改行挿入のみ、送信は Ctrl+Enter / Shift+Enter (誤送信の構造的防止)
│     - 矢印モデル (R13): 矢印=カーソル移動のみ、Ctrl/Shift+矢印=補完選択・履歴切替 (編集と履歴の分離)
│   ・代替案: 既存高性能端末 (Windows Terminal / WezTerm) + 制御層のみ自作
│
├─ L2: セッションホスト (馬1.5; 公式部品に乗る, R7)
│   ・claude を `-p --session-id <uuid> --input-format stream-json --output-format stream-json`
│     でホスト。1 ターンごとに自然に制御が外側へ戻る (defer hook 不要の閉ループ)
│   ・状態 = (session_id, cwd) ペア + effort + 履歴 (§7 知見: session は cwd ごとに保存される)
│   ・--fork-session でセッション分岐、--resume で再開
│
└─ L1: 制御プレーン llterm-ctl (馬1; 最初に射た馬 = PoC 済)
    ・Claude が Bash/Write ツールで構造化コマンドを投函 (帯域外; 確実な副作用)
    ・ディレクトリ: .llterm/queue/ (コマンド) / .llterm/results/ (書き戻し) / .llterm/ledger.jsonl (監査)
    ・現 .rotate-signal / [ROTATE:CRITICAL] は action:rotate の特殊ケースとして包摂 (後方互換)
```

## 4. 制御コマンド schema (L1)

```json
{
  "id": "ctl-<timestamp>-<rand>",
  "action": "rotate | set-effort | inject-task | fork-session | query-state | shutdown",
  "args": {},
  "reason": "監査用: なぜ Claude がこれを発火したか",
  "constraints": ["no-push"],
  "requires_human": false,
  "created_at": "ISO8601"
}
```

- `rotate` — summary 書き出し → 同 (session_id, cwd) で新ターン/新セッション再開
- `set-effort` — 次ターン/次セッションの effort 変更 (実行中変更の可否は未調査; §11)
- `inject-task` — claude-loop の既存 queue/ にタスク投函 (既存自走骨格と統合)
- `fork-session` — --fork-session で分岐セッションを起こす
- `query-state` — ランチャ状態 (session#, effort, uptime, cost 累計) を results に
- `shutdown` — 自走ループ安全停止。認証切れ検知時は自動でこれ + 人間待ち

## 5. 安全設計 (FullSense 哲学: fail-closed / Approval Bus / 監査)

1. **発火は Claude の明示ツール経由のみ** (帯域外)。発話テキスト sentinel は当面不採用 →
   untrusted repo スキャン中の prompt injection で制御を乗っ取られる経路を構造的に断つ。
   学術警鐘: 制御プレーン injection (arXiv 2503.24191 "Space-Time Decoupling Control-Plane
   Jailbreaks") を設計時点の脅威モデルに含める。
2. **allowlist された action のみ実行** (未知 action は fail-closed 拒否 + ledger 記録)。
3. **危険 action は requires_human:true** (shutdown 恒久化・破壊的操作)。Approval Bus 連携の差し込み口。
4. **全制御を ledger.jsonl に append-only 監査** (id / action / reason / 結果 / コスト)。
5. **構造的上限 (honest)**: 再ログイン/認証切れは llterm でも解けない。検知 → shutdown → 人間待ち。

## 6. 既存資産との関係

| 資産 | 扱い |
|---|---|
| ccr / claude-auto.mjs | **prototype として継続稼働**。llterm L1 が安定したら .rotate-signal を順次包摂 |
| claude-loop (inbox/queue) | inject-task の実体としてそのまま統合 (再発明しない) |
| llove term (builtins 等) | L3 シェルの部品候補。ただし Textual 固定にしない (R3) |
| llove F23/F24 要件 | 姉妹要件。llterm の L3 確定後に統合可否をユーザーが判断 (勝手に結合しない) |
| Claude Agent SDK | L2 の代替実装候補 (CLI 直叩きより型安全)。§11 で比較 |

## 7. PoC 実証結果 (2026-06-06, 本セッション)

| 検証 | 結果 |
|---|---|
| R1: 外側が UUID 事前生成 → `claude -p --session-id <uuid>` でセッション作成・合言葉記憶 | ✅ ACK / session_id 一致 |
| R2: 外側が `claude -p --resume <uuid>` → 文脈保持 | ✅ 合言葉 GINKO-7741 を正答 |
| 知見1 | session は **cwd ごと**に保存 → resume は同 cwd 必須 → 状態は (session_id, cwd) ペア |
| 知見2 | コスト 1 呼び出し ~$0.24 (PoC 計 ~$0.72)。自走ループのコスト計測は ledger に組込む |
| 結論 | **外側プロセスによる閉ループは公式部品で成立** (将の心臓は動く) |

## 8. 先行例と差別化 (honest: 7 割は既存、3 割が新規)

- 既存 (再発明しない): 自走ループ (Ralph)、TUI orchestration (Warp/OpenHarness)、
  session resume (公式 headless)、端末制御プレーン (tmux control mode `-CC`)、
  file/sentinel 制御 (**ccr 自身が実装済**)。
- 新規 (差別化核): ①公式 stream-json を土台にした Claude 専用の双方向制御 protocol
  ②PowerShell 同等シェル同居 ③csv-pandas-bridge 思想の明示的中間層 ④HITL gate + 監査を
  制御プレーン自体に組込み + 制御プレーン injection への設計時対策。
  **公式 defer/resume × tmux 制御モード級 protocol の結合実装は調査時点で空白**。
- Anthropic 製の器 (デスクトップアプリ / claude.ai/code / Agent SDK) と被る部分は protocol 側に
  寄せて吸収する (R7)。差別化は自走オーケストレーション + 安全制御プレーン + FullSense 統合に置く。

## 9. 段階実装 (馬の階層; 各段が独立に価値を持つ)

| 段 | 内容 | 状態 |
|---|---|---|
| 馬0 | 公式閉ループの PoC (--session-id / --resume) | ✅ 済 (§7) |
| 馬1 | L1 制御プレーン llterm-ctl 最小実装 (queue/results/ledger + rotate/inject-task の 2 action) | 次 |
| 馬1.5 | L2 セッションホスト (stream-json 双方向 + (session_id,cwd) 状態管理 + コスト ledger) | 馬1 の後 |
| 馬2 | L3 シェル + 表示層 (基盤選定 §11 を先に決める) | 設計後 |
| 馬3 | 統合: L3 が L2 をホストし L1 で自己制御 = 将 | 最後 |

## 10. テスト方針

- L1: コマンド投函 → 消費 → results 書き戻し → ledger 整合の unit + E2E (モック claude)。
  fail-closed (未知 action / 壊れた JSON / 重複 id) の回帰テスト必須。
- L2: モック stream-json サーバで resume / fork / cwd 不一致エラーの再現テスト
  (実 API 呼び出しはコスト発生のため opt-in スモークに隔離)。
- L3: 長テキスト性能の負荷テスト (R3; 例: 100MB 連続出力でフリーズ・メモリ線形爆発なし) を
  受け入れ基準に明記。Warp の轍を踏まないことを数値で確認。
  加えて ①②③・絵文字・罫線・全角半角混在行の**桁ずれゼロ** (R8) と ANSI 256色/truecolor 表示 (R9)、
  **日本語 IME 変換中に大量出力が流れても composition window が固定位置に留まる** (R10)、
  **複数行テキスト (改行・コードブロック含む) のペーストが 1 入力として保持され誤送信ゼロ** (R11)、
  **Enter 連打で送信されない / Ctrl+Enter・Shift+Enter でのみ送信される** (R12)、
  **複数行編集中の矢印キーで履歴に飛ばされない / Ctrl・Shift+矢印でのみ履歴・補完が動く** (R13) を
  受け入れ基準に含める。

## 11. 未決事項 (実装 plan の前に決める)

1. **L3 の基盤**: stream-json 自前レンダリング (本命) の実装言語/フレームワーク —
   Rust (性能) vs Python+prompt_toolkit/Textual+リングバッファ (開発速度・llove 部品再利用) vs
   既存端末 + 制御層のみ。R3/R4 の数値基準で選定。
2. **L2 の実装**: CLI 直叩き (`claude -p`) vs Claude Agent SDK。SDK の hooks (defer 等) の実機検証。
3. **set-effort の実行中変更可否**: /effort はセッション内コマンド。外側からの注入手段
   (stream-json の user message として送れるか) を要検証。
4. **置き場所**: 新規 D:/projects/llterm として独立 repo (推奨; FullSense 編入はユーザー判断) か
   raptor 配下か。
5. **ちらつきの定量定義**: 現 TUI のフリッカー再現条件を記録し、解消の判定基準を作る。
6. **R2「PowerShell 同等」の範囲定義**: フル互換 (オブジェクトパイプライン / cmdlet / .NET 統合) は
   非現実的。候補 (a) 日常シェル操作 (コマンド実行・パイプ・補完・履歴・環境変数・スクリプト起動) を
   「同等」と定義して自前実装 (b) pwsh を内部委譲で呼び表示だけ llterm が持つ。ユーザーと確定する。

## 12. 次アクション

- ユーザー spec レビュー → 承認後 writing-plans で馬1 (llterm-ctl 最小実装) の実装計画を作成。
- 本 doc を fullsense research index に登録。memory (project_llterm) を作成。
