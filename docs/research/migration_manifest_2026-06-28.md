# 移行 manifest(現機キャプチャ 2026-06-28)

> `gpu_pc_migration_plan_2026-06-28.md` の付属=**実測した現機の事実**(決定論的再構築の正本)。
> 着荷後はこの manifest 通りに新機(RTX 5090 / 128GB / Win11 Pro)へ載せ替える。

## 1. working-set サイズ(実測 du)

| 対象 | サイズ | 備考 |
|---|---|---|
| `D:/tools/raptor` | **75G** | framework + tool-guard + libexec + corpus skills(最大)|
| `D:/projects/llcore` | 9.1G | |
| `C:/Users/puruy/.cache/huggingface` | 9.0G | Qwen 0.5B/1.5B 等(再DL可だが移送が速い)|
| `D:/projects/fullsense` | 8.4G | |
| `C:/Users/puruy/.claude` | 1.5G | memory + settings + skills(★ccr/tool-guard の核)|
| `D:/api-keys.json` | 1M | ★secret |
| `D:/docs`(RAD)| 別途(大)| 80+ `*_corpus_v2/` + hacker_corpus、~48,800 docs |

→ 合計 ~100GB+(+ D:/docs)。**外付け 2TB SSD で余裕**、2TB 新機 SSD にも余裕。

**D: ボリュームの事実(実機一次検証・確定)**: SanDisk Extreme 55AE / **exFAT** / HealthStatus=Warning / OperationalStatus="Full Repair Needed" / **★ダーティビット SET**(`fsutil dirty query D:` → "Volume - D: is Dirty")/ BitLocker None(**平文**・ProtectionStatus Off)/ BusType=**USB** / GPT 単一 basic-data 2.0TB(used ~847GB / 残 ~1.15TB)。**物理移送=robocopy 不要だが、唯一コピー+非ジャーナル(exFAT)の単一障害点**。移送前に **read-only スキャン**(`Repair-Volume -DriveLetter D -Scan`)+ **off-disk 保険**(secret bundle・未push git bundle・RAD 一部を別媒体)を取る。

## 2. 移行ディレクトリ(★絶対パス温存)

> **新前提**: D: は外付け SSD 本体を物理移送しレター D: を温存 → **D: 配下は robocopy 不要(D: ごと travels)**。移送対象は **C: 常駐分のみ**。

### 2-A. D: 配下(travels=移送対象外)

- `D:/projects/`(llcore, fullsense, llive, llove, llmesh, llloop, llterm, mcp-3d, **browser-use-project の code 本体**[Alpaca trading])
- `D:/tools/raptor/`(75G)/ `D:/tools/`(raptor-analytics.db, osv-mcp)— rtk 実体は C: 側=§3 参照
- `D:/docs/`(RAD)/ `D:/api-keys.json` / `D:/api-manager/`

### 2-B. C: 常駐 inventory(★要移送=staging 対象)

`C:` 配下は D: travels で拾えない → `D:\_c_migration\` へ staging(`backup_working_set.ps1`)。`settings.json` の **グローバル hook + tool-guard 配線**、memory `projects/<...>/memory/`、skills は `.claude\` に内包。

| C: 常駐 | 分類 | secret | 備考 |
|---|---|---|---|
| `.claude\`(hooks/memory/settings.json/skills/.credentials.json) | copy | 一部 | 1.5G・ccr/tool-guard 核 |
| `.claude.json`(57KB) | copy(別ファイル) | ★ | MCP 配線・oauth・trust の本体。`.claude\` の外 |
| `.codex\`(config.toml/auth.json/memories/goals/state) | copy+CLI 再導入 | ★auth | Codex 二本柱の核 |
| `browser-use-project\`(alpaca_state.json/telegram_offset.json) | copy | 一部 | **trading live state**・code は `D:\projects`(travels) |
| `.ssh\`(id_ed25519) | copy | ★ | |
| `.gitconfig` / gh `hosts.yml` / PS profile / Win Terminal / `.config\` | copy(gh は再auth 可) | — | |
| `.cache\huggingface`(9G)/ `.ollama\models` | copy(再DL可) | — | 任意 |
| User env 3 secret + PATH | 再設定(secret は再発行推奨) | ★ | ファイルでない=travels で拾えない |
| Scheduled Tasks(Ready 4本) | XML export→import + action 是正 | — | |

> **★browser-use の二分**: code=`D:\projects\...\browser-use-project`(travels)/ **live state**=`C:\Users\puruy\browser-use-project\`(`alpaca_state.json` 等=C: 常駐=要移送)。両者を混同すると trading 状態を失う。

## 3. ツール(再導入先・現機実測)

> ★**要インストール物の正本 = `migration_dependencies_2026-06-28.md`**(2026-06-28 実環境 grounding: Python 全依存=torch cu128 / システムツール / MCP / ccr・rtk・Ollama、+ draft `tools/migration/bootstrap_install.ps1`)。本表は要点のみ。

| ツール | 現パス | 再導入 |
|---|---|---|
| node/npm | `C:/Program Files/nodejs` | Node v24 installer |
| git | `C:/Program Files/Git`(Git Bash 同梱)| installer |
| gh | `C:/Program Files/GitHub CLI` | installer(再 auth)|
| rustc/cargo | `C:/Users/puruy/.cargo/bin` | rustup |
| **rtk**(token killer) | 実体 `C:/Users/puruy/.cargo/bin/rtk.exe`(cargo install v0.34.1, rev 6444c4b0)。`C:/tools/rtk/rtk.exe` は古い重複=再現不要 | `cargo install`(rtk-ai/rtk)→ `.cargo/bin`(PATH 済)|
| **7-Zip** | `C:/Program Files/7-Zip`(PATH 未登録)| installer。★`migrate_secrets.ps1` の AES-256 バンドルが依存 |
| **global npm**(6本)| nodejs `-g` | `npm i -g`: `@openai/codex` / `zx` / `@github/copilot` / `@google/gemini-cli` / `@mermaid-js/mermaid-cli` / `bun` |
| uv | `C:/Users/puruy/.local/bin` | uv installer |
| **Claude Code 本体** | `C:/Users/puruy/.local/bin/claude.exe` | **native installer**(npm 版でない)|
| **Codex CLI**(二本柱の部下)| (CLI) | **再導入**(`.codex\` config/auth は §2-B で copy)|
| semgrep | `C:/Python314/Scripts`(pip)| `py -3.14 -m pip install semgrep` |
| codeql | **未導入**(startup ✗)| 必要時に導入 |
| py | 3.11(default)/3.14/3.9/uv3.12 | python.org + uv |
| ccr | (zx build + node-pty)| 再ビルド。**node-pty は native ABI = 新機 Node v24 で `npm rebuild`**(古い prebuilt は ABI 不一致で落ちる)|

## 4. 環境変数 / scheduled tasks

- **env(プロセス用・ccr/raptor 起動時に設定)**: `RAPTOR_CALLER_DIR`(ccr が user cwd を保存)、`RAPTOR_DIR`(ccr 起動時)、`CLAUDE_ENV_FILE=.claude/raptor.env`、`CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1`。
- **★User env 平文 secret 3キー**(ファイルでない=travels で拾えない→新機で再設定、**移行を機に再発行推奨**): `ANTHROPIC_API_KEY`(len108)/ `TELEGRAM_BOT_TOKEN`(len46)/ `SOCIALDATA_API_KEY`(len53)。User PATH も reference から再構築。
- **再登録すべき task**(現機 Ready 4本): **`FullSense-StatusTelegram`**(平日11:30)/ **`RAPTOR-Backup`** / **`RAPTOR-CorpusUpdate`** / **`ClaudeCodeUpdate`**(Ready=**要判断**)。
  - ★**action の C: 依存を是正**: `RAPTOR-Backup` / `RAPTOR-CorpusUpdate` は `C:\Python314\python.exe` + **不在の** `C:\Users\puruy\raptor\...`(`raptor-backup` 等)を指し壊れている → 新機では `py -3.11` + `D:\tools\raptor\libexec\...` へ書換。
- 移さない: `FullSense-TelegramInbound`(Disabled・廃止)、`BatteryStatus*`(★ノート専用=デスクトップ不要)、その他 ClaudeCode*(大半 Disabled)。
- **MCP servers**: `.claude.json`(57KB・MCP 配線本体)を **コピーすれば再現(手再設定不要)** → `claude mcp list` で主要サーバ Connected を確認。
- **trading(Alpaca 20分サイクル)= MCP cron(Job1–5)で schtasks 外** → `browser-use-project` 側で再設定。移行中は二重起動回避(旧機/クラウド残置)。

## 5. secrets(★物理移送前提に全面改訂)

**D: 上の secret は travels(別送不要)**:
- `D:\api-keys.json` / raptor `.claude\settings.local.json`(**ANTHROPIC_API_KEY 平文**)は **どちらも D: 上=travels**。旧設計の「ミラー除外して別送」目的は消滅。

新前提の secret 課題は 2 つ:
- **(a) D: 平文携帯ディスクの at-rest 露出**: D: は BitLocker None(平文)exFAT の **唯一コピー** → **chain-of-custody**(預け荷物にしない・手持ち移送)+ **着荷直後の鍵ローテ**。
- **(b) C: 常駐 secret の暗号化バンドル**(`migrate_secrets.ps1` を再スコープ): `.codex\auth.json` / `.ssh\id_ed25519` / `.claude\.credentials.json` / User env 3キー を **7z AES-256(`-mhe=on`・ヘッダ暗号化)** でバンドル。`.credentials.json` は **端末紐づき=新機は claude 再ログイン前提**(復元しても無効になり得る)。
- **off-disk 損失保険**: `api-keys.json` / raptor `settings.local.json` + 未push git bundle(任意)を別媒体に退避(落下/exFAT 修復失敗での単一障害に備える)。
- **鍵ローテ**: 旧 manifest の『検討』→『**到着直後に手順化**』へ格上げ。

## 6. GPU コード準備度(llcore)— ★初手 GPU 本走の前提

- `research/*.py`(verifier_navigability_gpu / internalization_poc / third_axis_gpu / rllm_stage_b 等)= `DEVICE = "cuda" if torch.cuda.is_available() else "cpu"`(**自動 GPU**)。
- `lm/` models(ttt.py / rwkv.py / recurrent.py)= `init_state(batch, *, device=...)` 対応。
- **✅ 配線済(2026-06-28、移行準備セッション)**: 学習 entry + `Trainer` / `TBPTTTrainer` / eval / longctx に device を backward-compatible に通した。**着荷後 Day 1 は `--device auto`(or `cuda`)を付けるだけで GPU 本走可能**。
  - **実装内容**: 新規 `src/llcore/lm/device.py`(`resolve_device("auto"|"cpu"|"cuda"|"cuda:N")` + `model_device(model)`)。`Trainer`/`TBPTTTrainer`/`estimate_loss`/`held_out_nll`/`held_out_report_any`/`held_out_top1_report`/`longctx_eval`(`nll_at_positions_with_context`/`context_length_curve`/`block_reset_nll`/`streaming_metrics_by_band`/`gpt_sliding_window_nll`)が **model の device を推論し各 batch を `.to(device)`**。RNG/index sampling は CPU 据え置きで乱数ストリーム不変。3 entry script(`tbptt_plateau_experiment.py`/`ttt_plateau_experiment.py`/`prove_native_matches_hf.py`)に `--device`(default `auto = cuda if available else cpu`)。
  - **検証(CPU)**: 既存 LM スイート全 green(resume 系 `atol=0` 含む)= **CPU byte-identical**(現プローブの方法論に影響なし)/ mypy strict・ruff PASS / `--device cpu` で experiment end-to-end smoke 成功。**GPU 上の cross-device 一致は着荷後 Day 1 に `verify_new_machine.ps1`(§7-8 / plan §5-2,3)で確認**。
  - 設計根拠: 全モデルの `init_state(batch, *, device=...)` が既に device 対応のため、穴は「学習/評価グルーが batch を CPU に置いたまま」だけだった。

## 7. 新機 bootstrap チェックリスト(着荷後・順に)

1. Win11 初期セットアップ: **ローカルアカウント `puruy`**(C:/Users/puruy 温存)。★**MS アカウントで OOBE すると `C:\Users\<先頭5字>` 等になり全 hook/memory/.claude.json/gh/gitconfig が破損** → 必ずローカルアカウント `puruy` で作成。
2. **新機 C: BitLocker 回復キー escrow**(Day-1 初手): Win11 Pro は Device Encryption 既定 ON の可能性 → `manage-bde -status C:` 確認 → 回復キーを MS アカウント+PW マネージャ+紙に控える。
3. **外付け D: 接続 → レター D: 固定**: 他 removable を全外し外付け単独接続 → `Set-Partition ... -NewDriveLetter D` → `Test-Path D:\tools\raptor` で温存確認(2TB の C:+D: 分割は **行わない**=D: ごと travels)。
4. **NVIDIA driver R570+**(Blackwell)。
5. py(3.11 default)導入 → **`torch cu128`** → `torch.cuda.get_device_capability()==(12,0)` 確認。
6. **C: 常駐分復元**(§2-B): `restore_working_set.ps1 -Source D:\_c_migration` → `migrate_secrets.ps1 -Mode Restore` → env 3キー再設定/再発行 → tasks XML import + action 是正。`.credentials.json` は claude 再ログイン前提。
7. node/git/gh/cargo/**rtk**/uv/semgrep/**Claude Code(native)**/**Codex CLI** 再導入、ccr 再ビルド(node-pty `npm rebuild`)。MCP は `.claude.json` コピーで再現。
8. scheduled tasks 再登録(FullSense-StatusTelegram / RAPTOR-Backup / CorpusUpdate / ClaudeCodeUpdate)、trading は二重起動回避。
9. 検証(`verify_new_machine.ps1` / plan §5)→ **llcore device 配線**(§6)→ 初手 = 本日プローブの GPU フル版。
10. **(後日)Phase 2**: 内蔵 NVMe 増設 → robocopy → レタースワップ → 内蔵 D: を BitLocker。外付けは backup 退役。旧ノートはこの緑化まで温存。
