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

## 2. 移行ディレクトリ(★絶対パス温存)

- `C:/Users/puruy/.claude/`(memory `projects/<...>/memory/`, `settings.json`[グローバル hook + **tool-guard 配線**], skills)
- `D:/projects/`(llcore, fullsense, llive, llove, llmesh, llloop, llterm, mcp-3d, browser-use-project[Alpaca trading])
- `D:/tools/raptor/`(75G)/ `D:/tools/`(raptor-analytics.db, osv-mcp)
- `D:/docs/`(RAD)/ `D:/api-keys.json` / `D:/api-manager/`
- `C:/Users/puruy/.cache/huggingface`(モデル重み)

## 3. ツール(再導入先・現機実測)

| ツール | 現パス | 再導入 |
|---|---|---|
| node/npm | `C:/Program Files/nodejs` | Node v24 installer |
| git | `C:/Program Files/Git`(Git Bash 同梱)| installer |
| gh | `C:/Program Files/GitHub CLI` | installer |
| rustc/cargo/**rtk** | `C:/Users/puruy/.cargo/bin` | rustup + `cargo install`(rtk=token killer)|
| uv | `C:/Users/puruy/.local/bin` | uv installer |
| semgrep | `C:/Python314/Scripts`(pip)| `py -3.14 -m pip install semgrep` |
| codeql | **未導入**(startup ✗)| 必要時に導入 |
| py | 3.11(default)/3.14/3.9/uv3.12 | python.org + uv |
| ccr | (zx build + node-pty)| 再ビルド |

## 4. 環境変数 / scheduled tasks

- **env**(ccr/raptor 起動時に設定): `RAPTOR_CALLER_DIR`(ccr が user cwd を保存)、`RAPTOR_DIR`(ccr 起動時)、`CLAUDE_ENV_FILE=.claude/raptor.env`、`CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1`、`ANTHROPIC_API_KEY`。
- **再登録すべき task**(現機 Ready): **`FullSense-StatusTelegram`**(平日11:30)/ **`RAPTOR-Backup`** / **`RAPTOR-CorpusUpdate`**。
- 移さない: `FullSense-TelegramInbound`(Disabled・廃止)、`BatteryStatus*`(★ノート専用=デスクトップ不要)、ClaudeCode*(大半 Disabled)。
- **trading(Alpaca 20分サイクル)= MCP cron(Job1–5)で schtasks 外** → `browser-use-project` 側で再設定。移行中は二重起動回避(旧機/クラウド残置)。

## 5. secrets(★安全移送・暗号化/別経路)

- `D:/api-keys.json`、raptor `.claude/settings.local.json`(**ANTHROPIC_API_KEY 平文**)、env。外付け一括コピーに混ぜず別経路で移送。**移行を機に key ローテーションを検討**(平文露出の衛生)。

## 6. GPU コード準備度(llcore)— ★初手 GPU 本走の前提

- `research/*.py`(verifier_navigability_gpu / internalization_poc / third_axis_gpu / rllm_stage_b 等)= `DEVICE = "cuda" if torch.cuda.is_available() else "cpu"`(**自動 GPU**)。
- `lm/` models(ttt.py / rwkv.py / recurrent.py)= `init_state(batch, *, device=...)` 対応。
- **★未配線**: 学習 entry(`scripts/tbptt_plateau_experiment.py` / `ttt_plateau_experiment.py`)+ `Trainer` / `TBPTTTrainer` は **CPU-only**(model/batch を device に移していない)。**初手 = ここに device を通す**。
  - **必要変更(backward-compatible)**: ① experiment に `--device`(default `auto = "cuda" if torch.cuda.is_available() else "cpu"`)② trainer で `model.to(device)` + 各 batch を `.to(device)` + `init_state(device=device)` ③ eval/longctx も device 統一。CPU 機では auto→cpu で **byte-identical**(現プローブの方法論に影響なし)。
  - **実装タイミング**: 本日プローブ(`blj04yepr`)完了後に実装+CPU smoke(走行中は CPU 競合回避のため未実施)、または着荷後 Day 1 の最初のコードタスク。所要 ~30分+smoke。

## 7. 新機 bootstrap チェックリスト(着荷後・順に)

1. Win11 初期セットアップ: **ユーザー名 `puruy`**(C:/Users/puruy 温存)。
2. **2TB を C:+D: 分割**(ディスクの管理。例 C:800/D:1100GB)。
3. **NVIDIA driver R570+**(Blackwell)。
4. py(3.11 default)導入 → **`torch cu128`** → `torch.cuda.get_device_capability()==(12,0)` 確認。
5. 外付けから **C:/D: 同一絶対パス**へ展開、`api-keys.json` は別経路。
6. node/git/gh/cargo(rtk)/uv/semgrep 再導入、ccr 再ビルド。
7. MCP servers + scheduled tasks 再登録(FullSense-StatusTelegram / RAPTOR-Backup / CorpusUpdate)、trading は二重起動回避。
8. 検証(plan §5)→ **llcore device 配線**(§6)→ 初手 = 本日プローブの GPU フル版。
