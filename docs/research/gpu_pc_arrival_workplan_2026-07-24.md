# GPU PC 着荷 作業計画（2026-07-24 / Fable5・ultracode）

> **これは何**: RTX 5090 機（Ark arkhive、〜2026-07-25/26 着荷予定）の**着荷前後にやらねばならない作業を全プロジェクト横断で洗い出した実行計画**。
> ユーザー指示 2 点 =（1）GPU PC でやる作業を列挙して計画化 （2）**特に環境設定を徹底深掘り**。
> **前提の確定**（ユーザー 2026-07-24）: **「D ドライブはそのまま物理移動」** = パス温存は物理で解決、robocopy backup/restore は不要、移行対象は **C: 常駐物だけ**。
> **正本の関係**: 移行 runbook の原型 = `gpu_pc_migration_plan_2026-06-28.md`（ハード確定・OOBE・D: レター固定の詳細）。本 doc はそれを **「D: そのまま移動」前提へ更新 + 現行機の実測監査 + 環境深掘り（torch/JAX-MJX-WSL2/依存/MCP/secrets）+ GPU 研究バックログ** で上書き・拡張したもの。memory = `project_gpu_pc_arrival_prep_2026_07_24`。
> 生成根拠 = 環境 5 領域を web 検証つきで深掘り + 研究 5 ドメインを横断抽出した Workflow（10 agents / 955k tokens、`wf_aa632297-bc8`）+ 現行機の実測監査。**外部 web は 2025〜2026 初頭のキャッシュ混在ゆえ、torch/jax の版タグは着荷時に必ず live 確認**（§A3-2）。

---

## 0. 現行機 実測サマリ（2026-07-24 監査・これが移行元の真実）

| 項目 | 実測値 | 含意 |
|---|---|---|
| Windows アカウント | 名前 `puruyan` / **profile フォルダ `C:\Users\puruy`**（OOBE 5 文字切詰め） | ハードコードは **フォルダ `C:\Users\puruy`** 参照 → 新機は **ローカルアカウント `puruy`** で作れば確実（§A1） |
| Python | `py -3.11` 既定（他 3.14 / 3.9 / uv 3.12） | FullSense 規律どおり py -3.11 |
| torch | **2.12.0+cpu**（CUDA なし） | **cu128/cu130 CUDA build へ入替必須**（§A3） |
| jax | **未導入** | MJX の前提。WSL2 で導入（§A4） |
| mujoco / mujoco.mjx | mujoco 3.10.0 有 / **mjx 不在** | mjx は WSL2 の別 venv で（§A4） |
| numpy/scipy/cma | 2.4.4 / 1.17.1 / 4.4.4 | 進化系は揃っている |
| node/npm | v24.14.0 / 11.9.0 | **Node は v24 厳守**（node-pty ABI、§A6） |
| rust/uv/git/gh | 1.94.1 / 0.10.12 / 2.42.0 / 2.88.1 | gh は **keyring 認証=ファイルでない=再 auth**（§A6） |
| WSL2 | **Ubuntu-24.04 (v2, Stopped)** + docker-desktop 存在（**旧機 C: 常駐**） | 新機では **来ない**（C: 常駐）→ 再構築 or `wsl --export/--import`（§A4） |
| MCP（top-level） | github, osv-mcp, semgrep, sqlite, fetch, calil, arxiv, filesystem, scholar-search, firecrawl（10） | `.claude.json` コピーで配線再現 + 個別再導入（§A6） |
| MCP（project-scoped） | alpaca, duckduckgo, fetch, perplexity, playwright, sqlite, wikipedia | browser-use-project cwd 時のみ。trading 廃止済 = alpaca 要否確認 |
| User env 秘密 | **3 本**: `ANTHROPIC_API_KEY`(len108) / `SOCIALDATA_API_KEY` / `TELEGRAM_BOT_TOKEN` | ファイルでない=travels で拾えない=再設定（§A2） |
| 秘密ファイル | D:/api-keys.json（travels）/ C: 側: .codex/auth.json・.ssh/id_ed25519・.claude/.credentials.json・qiita-cli/credentials.json・.claude.json(70KB)・.gitconfig・**.pypirc** | C: 側は暗号化バンドルで移送（§A2） |
| 大容量 | ollama models **27G** / HF cache **9G** | 再 DL 可（帯域と相談） |
| Scheduled Tasks（要移行） | ClaudeCodeUpdate / DisplayTimeout_Morning / DisplayTimeout_Night / FullSense-StatusTelegram / RAPTOR-Backup / RAPTOR-CorpusUpdate | HP/OneDrive/Zoom 系はノート bloat=不要 |
| ドライブ | D: exFAT 1863GB **HealthStatus=Warning（dirty bit）** / C: NTFS 952GB Healthy | 移送前に read-only スキャン + off-disk 保険（§A0） |

**新機**: Ark arkhive GL-I7G59M FE ／ RTX 5090 FE **32GB GDDR7（Blackwell, sm_120）** ／ Core Ultra 7 270K Plus（Arrow Lake）／ **128GB DDR5-5600** ／ ASRock B860M Steel Legend WiFi ／ **単一 2TB NVMe（既定 C: のみ・D: 無し）** ／ 1000W ／ **Win11 Pro DSP プリインストール**。

---

# Part A — 環境設定（徹底深掘り）★ユーザー重点

## A0. 着荷前（現行機でやる）

1. **未 git / 未 push の消失リスクを潰す**（★最優先）:
   - `D:/projects/evis_chopstick` は **非 git**（箸巧緻把持の主戦場: training_chopsticks.py / gates.py / graft.py / s1_thumb_servo.py）→ **必ず git init + commit、または別媒体バックアップ**。
   - `gaitlab` main は origin より **+266 commits 未 push**（human-gate）／ `onocollo-complete` は origin 同期済（push 済）。移送前に未 push repo の push 判断（human-gate）。
   - off-disk 保険（D: は唯一コピー・dirty bit）: `git bundle create ...--all` を Desktop→暗号化 USB へ。
2. **D: read-only スキャン**: `Repair-Volume -DriveLetter D -Scan`（dirty なら保険確保後に `-OfflineScanAndFix`）。
3. **★DATA を D: に載せる（新方針の要）**: 再インストールで復元できない DATA だけ D: へコピー（§A2 ①）:
   ```powershell
   robocopy "C:\Users\puruy\.claude" "D:\_c_migration\.claude" /MIR /XJ /R:1 /W:1   # ★memory 含む .claude 一式
   Copy-Item "C:\Users\puruy\.claude.json" "D:\_c_migration\.claude.json"           # 任意(MCP 配線省力化)
   robocopy "C:\Users\puruy\.codex" "D:\_c_migration\.codex" /MIR /XJ                # 任意(Codex 蓄積)
   ```
   新機ではこれを `C:\Users\puruy\` へ戻すだけ（暗号化バンドル/backup_working_set/restore は使わなくてよい。使うなら A0-fix 3 件を先に）。
4. **（任意）WSL export**: `wsl --shutdown; wsl --export Ubuntu-24.04 D:\_c_migration\wsl\ubuntu-24.04.vhdx --vhd`（中に資産が無ければ skip し新機で新規 install でよい）。
5. **秘密**: どうせ着荷後に鍵ローテするので原則「新機で再発行」（§A2 ③）。ローテしない qiita/.pypirc だけ①で D: に載せてもよい。

### ★A0-fix: 移行スクリプトの実測ギャップ 3 件（**推奨・要ユーザー go で適用**）
> RAPTOR 規律「apply patches = ASK FIRST」に従い**未適用**。着荷前に適用推奨（無音のデータ欠落を防ぐ）。
1. `migrate_secrets.ps1` の `$SecretFiles` に 2 行追加: `C:\Users\puruy\.pypirc`（PyPI トークン 492B・**現在どのバンドルにも入っていない**）と `C:\Users\puruy\.config\qiita-cli\credentials.json`（Qiita write 147B）。
2. `backup_working_set.ps1` の `config` ジョブ ExtraXF に `qiita-cli\credentials.json` を追加（**平文 exFAT D: に write トークンが乗るのを除外**）。
3. `backup_working_set.ps1` の task export regex を `'FullSense|RAPTOR|ClaudeCode'` → `'FullSense|RAPTOR|ClaudeCode|DisplayTimeout'` に拡張（**現状 DisplayTimeout 2 本が無音で export されない**）。

## A1. OS 初期化・アカウント `puruy`・D: レター固定

- **OOBE でローカルアカウント `puruy`**（MS アカウントだと `C:\Users\<5字切詰め>` になり全ハードコード即死）:
  - `Shift+F10` → `start ms-cxh:localonly`。**25H2 build 26220.6772+ でパッチ済報告あり**ゆえフォールバック用意: `reg add HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\OOBE /v BypassNRO /t REG_DWORD /d 1 /f` → 再起動 → 「インターネットに接続していません」→ ローカル `puruy`。
  - **検証**: `Test-Path C:\Users\puruy` が True（全ハードコードの生死判定）。
- **BitLocker**: `manage-bde -status C:` → ON なら回復キーを MS アカウント + PW マネージャ + 紙の 3 重 escrow（Day-1 初手）。
- **D: レター固定**（外付け SanDisk 単独接続）: `Get-Disk/Partition/Volume` → `Set-Partition -DiskNumber <n> -PartitionNumber 1 -NewDriveLetter D` → **sentinel `Test-Path D:\tools\raptor` が True**。他ボリュームが D: を先取りなら `Remove-PartitionAccessPath` で退かす。
- **（後日 Phase 2）** 単一 2TB は当面 C: のみ。安定後に内蔵 NVMe 増設 → `robocopy D:\ X:\ /MIR /XJ` → レタースワップ → 内蔵 D: を BitLocker（exFAT 平文脱却）。USB selective-suspend 無効化を新機でも再適用（D: 切断で tool-guard hook が fail-open すると保護が無音消失）。

## A2. C: 常駐物の扱い（★方針: D: 経由で引っ越す or 新規インストールで対応 — ユーザー確定 2026-07-24）

> **方針**: C: 常駐物は各項目ごとに 3 分類。**「再インストール/再認証で復元できない DATA」だけ D: に載せて運び、あとは全部新規導入**。旧計画の暗号化バンドル + backup/restore の仕掛けは**不要（optional に降格）**。
> **★かけがえのない DATA = `C:\Users\puruy\.claude\projects\...\memory\`（全プロジェクト記憶）**。これだけは必ず D: に載せて運ぶ（fresh install では消える）。

### ① D: に載せて運ぶ（DATA・再現不能 → `robocopy` で D: の staging 領域へコピーして travels）
| 対象 | 重要度 | 備考 |
|---|---|---|
| `.claude\projects\...\memory\`（+ MEMORY.md） | ★★必須 | **全プロジェクト記憶**。最優先で D: へ。単独でも小さい |
| `.claude\`（hooks/settings.json/skills/statusline 等） | ★推奨 | ccr/tool-guard の挙動。手で再構成も可だが load-bearing |
| `.claude.json`（70KB, MCP 配線/trust） | ○任意 | コピーで MCP 手再設定を省ける。手動再構成でも可。※中に perplexity/alpaca 平文キー=ローテ時 env 更新 |
| `.codex\`（memories/goals/state） | ○任意 | Codex の蓄積コンテキストを惜しむなら。auth.json は別途再ログイン |
| D:/api-keys.json / raptor settings.local.json | 既に D: | travels（何もしない） |

### ② 新規インストール（バイナリ/ランタイム・再現可能 → どのみち再導入）
Node v24 / uv / rust / git / gh(binary) / claude(binary) / codex(binary) / semgrep / scholar-search / rtk / 7zip / **WSL2 Ubuntu(新規)** / Docker Desktop / MCP ランタイム（uvx・npx 自動取得）/ playwright ブラウザ / **ollama models 27G(再 pull)** / **HF cache 9G(再 DL、`HF_HUB_DISABLE_XET=1`)**。→ 詳細は §A6。

### ③ 再認証・再発行（機械紐付き/秘密・コピー無効 or ローテ対象 → 新機で取り直す）
gh(`gh auth login`) / claude(`/login`) / codex(`codex login`) / **firecrawl API キー(再取得)** / User env 秘密 3 本(ANTHROPIC/SOCIALDATA/TELEGRAM=console 再発行 or 再設定) / PyPI(.pypirc) / Qiita write / GitHub PAT。→ **どうせ着荷後に鍵ローテする**ので「新機で取り直す」が最もクリーン。SSH 鍵も `ssh-keygen` 新規 + GitHub 再登録が clean（惜しむなら `.ssh\id_ed25519` を①で運ぶ）。
- **例外的に「運ぶ方が楽」**: qiita creds(147B) / `.pypirc`(492B) はローテしないなら①で D: に載せてコピーでも動く（exFAT 平文の at-rest 露出は許容できる範囲、気になるなら再発行）。

### その他（項目固有）
- **Scheduled Tasks 6 本**: XML export→`Register-ScheduledTask -Xml`（失敗時 `-User puruy`）+ **action パス是正**（RAPTOR-* は旧 `C:\Python314\python.exe` 参照=書換要）。import 成功≠動作。全 6 本を新規登録し直す方が確実な場合も。
- **二重起動注意**: FullSense-StatusTelegram / trading（trading は廃止済）は旧機を先に Disable → 新機で有効化。
- **鍵ローテは「新機が全緑になってから」**（先にやると旧機=最後のバックアップが死ぬ）。旧ノートは verify 緑 + ローテ完了までワイプ禁止。

> **単純化の含意**: ①の DATA コピー（実質 `.claude` を D: へ）と未 git repo バックアップ（§A0）さえ済ませれば、あとは新機で **fresh install + 再認証** で組み上がる。`migrate_secrets.ps1`/`backup_working_set.ps1`/`restore_working_set.ps1` は使っても使わなくてもよい（使うなら A0-fix 3 件を先に）。

## A3. GPU 基盤（driver / torch / sm_120 検証）★深掘り

1. **NVIDIA driver**: `nvidia-smi` で RTX 5090 表示 & **Driver >= 570（できれば 580+）/ CUDA Version >= 12.8** を確認。プリインストール済公算大、不足なら nvidia.com 最新 Game Ready/Studio。※`nvidia-smi` の "CUDA Version" は driver 上限であって wheel の版ではない（13.x 表示でも cu128 wheel は同梱 12.8 runtime で正常）。
2. **★torch wheel タグは着荷時に live 確認**（**agent 間で cu128 vs cu130 の食い違い=どちらも mid-2026 の matrix を web 確認できず**）:
   ```powershell
   py -3.11 -m pip index versions torch --index-url https://download.pytorch.org/whl/cu128
   py -3.11 -m pip index versions torch --index-url https://download.pytorch.org/whl/cu130
   ```
   **確実な下限 = cu128**（PyTorch 2.7/2025-04 で sm_120 stable 初出）。**torch 2.12 系は cu128 撤去で cu126/cu130/cu132 のみ、という未確認情報あり** → 現行機 torch が 2.12.0 なので **実在するタグの中で最新の cuXXX（≥128、cu126 は sm_120 非対応ゆえ不可 → 実質 cu130 が有力）** を採る。ダメなら nightly `.../nightly/cu128`。
3. **入替（base + D: 上の各 venv）**: `pip uninstall -y torch torchvision torchaudio` → `pip install torch torchvision torchaudio --index-url .../cu130`。**3 つ同じ index から同時に**（別々だと +cpu を掴み ABI 不整合）。**D: 上の各 venv には旧 +cpu が焼付いて travels するので venv ごとに `--force-reinstall`**。
4. **★sm_120 + 実 GEMM 検証（`no kernel image` オラクル）** = 既存 `fullsense/tools/migration/gpu_smoke.py`:
   ```powershell
   py -3.11 D:\projects\fullsense\tools\migration\gpu_smoke.py   # capability==(12,0) / gemm_ok / linear_ok / overall=pass
   ```
   **`torch.cuda.is_available()` は driver の有無しか見ない**（True でも wheel に sm_120 kernel が無ければ最初の GEMM で `RuntimeError: no kernel image`）→ **必ず実 GEMM まで走らせる**。新機で `gpu_smoke.py` が exit 2（SKIP）を返したら「環境差でスキップ」でなく「cu130 torch/driver が実際には入っていない」= 要修正（現機の SKIP 意味論に流されない）。
5. **CUDA Toolkit は不要**（wheel が runtime 同梱、driver のみで動く）。`nvcc` が要るのは flash-attn/bnb を source ビルドする時だけ。不要な Toolkit で PATH の nvcc と wheel 同梱 runtime を食い違わせない。
6. **int8 カーネル系（llcore 用）**: bitsandbytes は Blackwell で**機能はする**が **小モデル（<7B）で de-quant 律速により逆に遅い**（throughput -41%）→ 「量子化=高速」を仮定せず必ずベースライン計測。**32GB VRAM では 1.5B–4B は fp16 で余裕 → int8 GPU の意義は 7B+/edge 配布寄りに再定義**。flash-linear-attention は **Triton 依存 → native Windows は難所 → WSL2**（§A4）。

## A4. WSL2 + JAX + MuJoCo MJX（★箸 MJX 並列 RL の GPU 経路・最重要領域）

- **確定事実**: **JAX の native Windows CUDA wheel は無い（CPU のみ）→ MJX は WSL2 一択**。torch CUDA は native Windows で可（世界モデル/Dreamer は Windows のまま GPU 化、WSL 不要）。
- **旧機の Ubuntu-24.04 は C: 常駐=来ない** → 新機で `wsl --update; wsl --set-default-version 2; wsl --install -d Ubuntu-24.04`（or 旧機で `wsl --export`→新機で `--import`）。**WSL 内に Linux NVIDIA driver を入れない**（Windows driver が `/usr/lib/wsl/lib` でパススルー。入れると壊れる）。検証: `wsl -d Ubuntu-24.04 -- nvidia-smi` が 5090 表示。
- **WSL venv 構築**（Python 3.11 で Windows と揃える）:
  ```bash
  sudo add-apt-repository -y ppa:deadsnakes/ppa && sudo apt update
  sudo apt install -y python3.11 python3.11-venv python3.11-dev build-essential
  python3.11 -m venv ~/mjx && source ~/mjx/bin/activate   # ★必ず ext4(~/)。/mnt/d(exFAT)は symlink 不可で venv が壊れる
  unset LD_LIBRARY_PATH                                    # ★下記トラップ回避
  pip install -U "jax[cuda12]" mujoco mujoco-mjx           # cuda13 も候補、実機で device 検出の良い方を採用
  ```
- **★最大のトラップ = `LD_LIBRARY_PATH`**: pip-JAX は CUDA を同梱するため、`export LD_LIBRARY_PATH=/usr/local/cuda...`（PyTorch 用）を同じ shell に貼ると同梱 lib が shadow され **`No visible GPU devices`** で落ちる（JAX 公式明記／唯一の公開 RTX5090+MJX 事例 `mujoco_playground#299` の失敗はこれが主因）。
- **★sm_120 コンパイル関門**（device 列挙でなく**本物の matmul を JIT させる**）:
  ```bash
  python -c "import jax, jax.numpy as jnp; x=jnp.ones((4096,4096)); print(float((x@x).sum()))"  # [CudaDevice] + 数値、sm_90a/ptxas エラー無し=Blackwell 実働確定
  ```
  jax は GPU 未認識でも**黙って CpuDevice で fail-open**する → `jax.devices()` が `CudaDevice` を返すことを必ず確認（でないと「MJX が遅い」の偽結論）。
- **MJX go/no-go spike**（コードは ext4 にコピーして実行、`/mnt/d` は 9P 越しで壊滅的に遅い）:
  ```bash
  cp -r /mnt/d/projects/onocollo-complete ~/onocollo-complete && cd ~/onocollo-complete
  pip install -e ".[dev,mujoco]" cma imageio imageio-ffmpeg
  PYTHONPATH=src python scripts/mjx_spike.py --batch 2048 --steps 200   # → GO(speedup>=5x) / MARGINAL は --batch 4096/8192
  ```
  ※`setup_gpu_env.py` の既定は **jax[cuda12] 固定 & torch cu124 固定**（cu124 は sm_120 非対応）→ WSL の jax はスクリプトに任せず手動導入、torch は `--cuda cu130` を明示。
- **EGL ヘッドレス描画**（RDP 耐性・`reference_mujoco_gl_remote_desktop` の WGL クラッシュ回避）: `sudo apt install -y libegl1 libgles2 libglvnd0; export MUJOCO_GL=egl` → `verify_gpu_env.py` の render 行が `frame (64,64,3)`。
- **フォールバック梯子**（MJX が Blackwell で NO-GO の時）: (a) **onocollo `parallel_map --workers N`**（jax 不要・移植ゼロ・serial byte-identical=最も確実な携行 win、Core Ultra 多コア + 128GB で即効）→ (b) **MuJoCo Warp**（Blackwell で MJX 比 252–475x の実測だが warp-lang で書き直し=別 API、drop-in でない）→ (c) torch ベース GPU 並列 → (d) brax / Isaac Lab（重い・最後の手段）。**まず (a) で確実な win を取り、MJX の go/no-go で Warp 検討**。

## A5. 各プロジェクト venv 再構築

- **方針: 既存 .venv は torch 入替でなく全再生成**（pyvenv.cfg/Scripts に旧 C: パス焼付き + CPU torch 焼付き）。`uv venv --python 3.11 .venv` → **torch を cu130 で先に入れてから** `uv pip install -e ".[extras]"`（逆順だと extras 解決で PyPI torch に上書きされる）。
- **wm_carracing(canonical) と onocollo-complete(worktree) は同一パッケージ名** → global に editable を 2 つ入れると壊れる → **必ず project ごと venv 分離**。
- **プロジェクト別**:
  - `onocollo-complete`（.venv 無/pyproject+req）: venv 新設 → cu130 → `-e ".[dev,mujoco]"` → `verify_gpu_env.py`（jax probe は Windows で fail が正常=WSL 側で担保）→ pytest（**641 pass / 5 fail は test_import_hygiene.py の既知内部矛盾テスト**=移行成功の基準）。
  - `llive`（.venv 有=旧）: `.venv.old-cpu` へ退避 → 新設 → cu130 → `-e ".[dev,torch,ingest]"`（faiss は cpu 版のまま可）。ベンチは on-prem 純度規約（`feedback_llive_measurement_purity`）に従い環境変更を記録。
  - `llcore`（src レイアウト・PYTHONPATH=src → editable へ昇格）: cu130 → `-e ".[dev,z3,sdp,chat,clip,text]"`。cvxpy は `CLARABEL` 固定確認（`feedback_cvxpy_pin_accurate_solver`）。
  - global py -3.11（xct/evis_chopstick/myohand_chopstick/fullsense）: `torch --index-url .../cu130` + numpy/scipy/cma/mujoco/imageio。
  - WSL MJX 用 venv は §A4（ext4 に別途）。
- **依存固定**: 各環境 activate 状態で `uv pip freeze` を `requirements-lock-*.txt` に採取しコミット（`+cu130` local tag は index-url をコメント併記）。

## A6. MCP サーバ + CLI ツールの再導入・再認証

1. **前提ランタイム**（winget）: **Node LTS = v24 厳守**（`node -v` 目視。v25+ だと D: の node-pty prebuilt が ABI 不一致で ccr 起動不能）/ Git / GitHub CLI / 7zip / Rustup(`rustup default stable`) / uv(`irm https://astral.sh/uv/install.ps1｜iex`) / rtk(`cargo install --git https://github.com/rtk-ai/rtk --rev 6444c4b...`)。
2. **再認証群（ファイルで運べない/運んでも死ぬ）**:
   - **gh**: `gh auth login`（トークンは Windows Credential Manager=keyring）。
   - **Claude Code**: native installer（`irm https://claude.ai/install.ps1｜iex`）→ `claude` → `/login`（.credentials.json コピーは保険どまり）。★再ログインは人間介在点=CLAUDE.md の「再ログイン時ループ継続禁止」どおり止まるのが正常。
   - **Codex**: `npm i -g @openai/codex` → auth.json 復元 → `codex login status`、ダメなら `codex login`。非対話は `Get-Content p.txt -Raw | codex exec -s read-only -`（stdin）。
3. **`.claude.json` を同一パスへ配置**（MCP 配線 top 10 + browser-use scoped 7 を再現）。※perplexity/alpaca キーが平文 env=ローテ時は env 値も更新。
4. **uvx/npx MCP を pre-warm**（キャッシュは C: 常駐=来ない・オフライン初回は無音 connect 失敗）: `uvx mcp-server-fetch --help` / `uvx mcp-server-sqlite --help` / `uvx arxiv-mcp-server --help` / `uvx alpaca-mcp-server --help`（trading 廃止済=要否確認）/ `uvx duckduckgo-mcp-server --help` / `uvx mediawiki-mcp-server --help` / `npx -y @modelcontextprotocol/server-filesystem --help` / `npx -y firecrawl-mcp --help` / `npx -y @perplexity-ai/mcp-server --help` / `npx -y @playwright/mcp@latest --help`。
5. **個別対応**:
   - **osv-mcp**: `Push-Location D:\tools\osv-mcp; uv sync; Pop-Location`（.venv/pyvenv.cfg が旧 C: interpreter を指す=再生成必須）。
   - **semgrep**: `py -3.14 -m pip install semgrep` + `C:\Python314\Scripts` を User PATH へ（MCP は global バイナリ依存）。破損 `.semgrep/settings.yml`（先頭 null byte）は移送せず新機で自動再生成。
   - **scholar-search-mcp**: `py -3.11 -m pip install scholar-search-mcp`。
   - **playwright**: `npx -y playwright install chromium`（ブラウザ実体は別 DL）。
   - **★firecrawl（最大の未解決）**: `FIRECRAWL_API_KEY` が config/User/Machine env / api-keys.json の**どこにも無い**のに in-session では動く（キー出所不明）→ 新機では **firecrawl.dev ダッシュボードでキー再取得** → User env or config env へ、`api-keys.json` に `firecrawl_api_key` を追記して真ソース化。
   - **github MCP**: remote HTTP OAuth の既知不具合（claude-code#3433）→ `/mcp` 再認可、駄目なら `claude mcp add --transport http github https://api.githubcopilot.com/mcp/ --header "Authorization: Bearer <PAT>"`。
   - **ccr node-pty**: `node -e "require('D:/tools/raptor/node_modules/@homebridge/node-pty-prebuilt-multiarch');console.log('OK')"`（Node v24 維持なら rebuild 不要。v25+ になった時のみ `npm rebuild`=要 VS Build Tools）。
6. **最終判定**: `claude mcp list` で top 10 が connected。

## A7. Day-1 検証チェックリスト + 鍵ローテ

- `verify_new_machine.ps1`（Check0=D: レター/健全性/sentinel → 全項目）。
- `gpu_smoke.py` PASS（capability (12,0) + 実 GEMM）。
- torch CUDA True + `torch.cuda.get_device_name(0)`=RTX 5090。
- WSL: `jax.devices()`=CudaDevice + matmul 関門通過（§A4）。
- ccr 起動 → SESSION START 復元 → **tool-guard live**（D:/ 温存パスで発火）→ raptor /scan smoke。
- RAD corpus（D:/docs 横断）/ rtk / auto-commit hook。
- **鍵ローテ（全緑後）**: ANTHROPIC / TELEGRAM(BotFather /revoke) / SOCIALDATA / PyPI(.pypirc) / Qiita write / GitHub(gh 旧 token revoke) を各コンソールで再発行 → env + api-keys.json + raptor settings.local.json 更新 → 旧失効を 401 で実確認。

---

# Part B — GPU 待ち研究作業バックログ（優先度順）

## B0. 横断の前提（全 GPU 作業に効く）

- **GPU 初手の最有力（ユーザー既知）= 箸の巧緻把持を MJX 並列 RL で解く**（手動調整 約27試行で自由物体 pinch-lift 安定化不可と確定 → 数千環境並列 RL が正道）。ただし前提 = 環境立ち上げ（§A3/A4）と **箸 MJX rollout + throughput go/no-go gate**。
- **最大の honest 分岐点 = MJX の Hill 筋/tendon サポート**: evis/myohand は 39/700 の Hill 筋実手。MJX が GPU で正しく積分できるか未検証 → **不可なら (a) 剛体レバー簡略 rig（`src/onocollo/chopstick`、MJX 前提設計済）で先行 (b) CPU process 並列に退避**。
- **RL(PPO)スタックは onocollo に未配線**（現状 CMA-ES/scripted seam のみ）= MJX+RL は新規構築が要る（全 RL 項目共通のブロッカー）。
- **honest 規律**: 評価は常に 4 ゲート（ablation + 長時間 + force-closure ε + 摂動）で false success を摘発。異常に良い結果は内訳を疑う（`feedback_benchmark_honest_disclosure`）。CPU で既に positive 達成済（把持/飲む/pour/snake/交互歩行 1.66m/freefloat whole-body 100% 回復）は GPU 不要。
- **GPU 占有競合**: MJX RL と llcore 学習は同一 32GB を食い合う → llcore は短時間 prereg 実験（plateau/proxy v2 overnight）を隙間に、重量級（joint 蒸留/StateX）は順番待ち。

## B1. 優先度テーブル（necessity: must=GPU 無しでは事実上不可 / strong=桁違い高速 / nice=あれば便利）

| P | 作業 | ドメイン | necessity | dir / entry | honest 現状 |
|---|---|---|---|---|---|
| **P0** | 環境立ち上げ + MJX 疎通 smoke（torch cu130 / WSL2 jax / MJX probe） | 横断 | must | onocollo `scripts/setup_gpu_env.py`→`verify_gpu_env.py`→`mjx_spike.py` | 土台 CPU 検証済・GPU 未実行。sm_120 wheel 互換が day-1 最大リスク |
| **P0** | 箸 MJX rollout + throughput go/no-go gate | dexterity | must | `src/onocollo/chopstick/{model,rollout}.py` + `mjx_batch.py` | rig は CPU 緑・push 済。MJX 未配線・接触リッチで C engine と発散し得る |
| **P0** | **箸 自由物体 pinch-lift 閉ループ把持を大規模並列 RL（本丸）** | dexterity | must | **`D:/projects/evis_chopstick`**（training_chopsticks.py/gates.py） | 正しい把持+可動腕+静的挟み+単箸 genuine pinch まで。**完全 pick-and-lift 未達=閉ループ力制御が次**。RL 未着手。**dir 非 git=要バックアップ** |
| **P0** | llcore plateau プローブ フル走（3 arch×chunk sweep×≥3 seed） | llcore | strong | `scripts/tbptt_plateau_experiment.py --device cuda` + prereg | device 配線済=`--device cuda` 足すだけ。CPU 9h/arm→GPU 数十分 |
| **P1** | rocket MJX バッチ rollout throughput 実証 | worldmodel | strong | `mjx_spike.py`/`mjx_batch.py` | scaffold CPU 済・GPU 未検証。eval-signal は robust NULL 済=throughput 実証が主目的 |
| **P1** | LoLCATs-path 線形化 本訓練 + 蒸留 held-out 検証（O1→O5） | llcore | must | `runtime/distill.py`(O2/O4/O5 未実装)/`linearize.py` | per-layer 蒸留 91-98% まで。**joint 蒸留=回復本体が GPU 待ち** |
| **P1** | llcore proxy v2 フル走（K≥12・context sweep 2048-4096） | llcore | strong | `nas_pareto.py --proxy-v2 --distill --context-sweep ... --device cuda` | 道具は完成・「線形化は長文脈で単調劣化」検出済。publishable 強度が計算量待ち |
| **P1** | gaitlab MJX 移植（factorial/hybrid を大予算再測定） | gaitlab | strong | `scripts/mjx_smoke.py`/`rollout.py` MjxEvaluator seam | seam CPU 済・MjxEvaluator 未実装。**main +266 未 push** |
| **P1** | llive 実 LLM fitness 実走 → 1000 世代 persona/Genome3D 進化 | llive | strong | `scripts/run_persona_evolution_long.py --fitness llm --backend ollama` | 基盤完成・mock 完走済。実走だけ未。ollama on-prem=純度規約適合 |
| **P1** | 世界モデル大 RSSM 再挑戦（momentum 系・前回 h*=0） | worldmodel | strong | `scripts/wm_reacher_drift.py`（env 差替） | device=auto 済=torch のみで着手可（WSL 不要）。突破は不確実 |
| **P2** | 筋 RL + SAR 次元圧縮（39→~10 シナジー） | dexterity | strong | `dexterity/myohand/gate2b_grip.py` | プリミティブ確立・RL/SAR 未。**MJX の Hill 筋対応が分岐点** |
| **P2** | evis/graft 巧緻操作の MJX 化（両箸 robust 化）/ Gate D 摂動ドメインランダム化 | dexterity | strong | `graft.py`/`s1_thumb_servo.py`/`gates.py` | graft は artifact 自己摘発済・genuine は単箸のみ。摂動学習未 |
| **P2** | freefloat 汎化拡張（OOD debris/tumbling/faults）/ 宇宙ゴミ捕捉スケールアップ | worldmodel/space | strong | `scripts/adr_freefloat_wholebody.py`/`adr_evolve.py` | whole-body 100% 回復済。汎化・高速タンブリングは env 拡張が先。運動量保存オラクル維持必須 |
| **P2** | 筋シナジー musculo 歩行/立位の予算突破試行 / ape 二足歩行 RL | locomotion | strong | `musculo_walk_par.py`/`robot_walk_altphase.py`/`ape_balance.py` | robust null・~3.7s 天井・1.66m 交互歩行まで。null が予算由来か構造由来か未分離=突破不確実 |
| **P2** | V→M→C 画素本走 / DreamerV3 忠実化 + gaitlab タスク適用 | worldmodel | strong | `oc.train`/`rssm.py`/`dreamer.py` | 配線済・fidelity 訓練は未。実タスクで random 未満の negative=V3 化とセットで |
| **P2** | xct Phase 1（LoDoPaB/Walnut 再現・R²-Gaussian/NAF） | xct | must | **コード未着手**（docs のみ）/ Phase0 survey 正本 | 発足 3 日。**R²-Gaussian の CUDA kernel が sm_120 でビルドできるか要検証** |
| **P2** | VLM 新ブランチ（7B ローカル推論 + LoRA、manga-md/llove 接続） | VLM | must | 新規（mangamd 実体位置要特定） | 完全新規。Qwen 商用障壁に注意=代替 VLM ライセンス比較先行 |
| **P2** | llcore int8 GPU カーネル / CSC-NAS / 3B スケール / 数学蒸留 SFT | llcore | strong〜must | `loader.py`/`evolve_linearize.py`/`qwen2.py` | 32GB では 1.5-4B は fp16 で余裕=int8 は目的再定義。3B は商用可ライセンス base 確立 |
| **P3** | PERSONA-FX 実部品接続 / gaitlab K×ε sweep・QDax 化 / Isaac Lab / xct 拡散 / nanoGPT S0 / 動画環境 GPU 化 / heterogeneous QD 多コア並列 / StateX continued-train | 各種 | nice〜must | 各 memory 参照 | Isaac/xct 拡散/nanoGPT は「GPU 無しでは不可」だが後段。多くが前段の結果待ち |

## B2. ドメイン別の要点（詳細は各 memory・GPU_PLAYBOOK）

- **dexterity（箸/手）**: P0 本丸は evis_chopstick の閉ループ力制御 RL。カリキュラム S1 単箸 pinch→S2 両箸→S3 食片摘み→lift→口へ。報酬は gates.py 4 ゲートを写像（先端開度+非交差で測る、関節角でない=piano curl 教訓）。budget-matched baseline を held-out で。**MJX 筋対応が不可なら剛体 rig 先行 or parallel_map 退避**。
- **locomotion/musculo/freefloat**: null が多い（筋シナジー歩行=robust null、rocket=robust null、wm h*=0、ape 単脚支持=frontier）。GPU は「予算/表現由来 null」を突破できるか試すレバー。構造由来なら GPU でも破れない可能性を併記。
- **worldmodel/space**: 世界モデルは device=auto 配線済で torch のみ着手可（WSL 不要）。momentum 系 + 大 RSSM で h* 再挑戦。宇宙ゴミは終端捕捉のみ（軌道力学 out-of-scope）。
- **llcore**: 内の初手は plateau プローブ（prereg 済）。本命回復は joint 蒸留（O4/O5）で GPU 待ち。PoC-1(read) は NOT GO 確定=除外。32GB VRAM で 3B fp16 が本命 base 候補（Qwen3-4B/Ministral-3-3B=Apache、Qwen3.5 は NO-GO）。
- **gaitlab/llive/xct/VLM**: gaitlab は MjxEvaluator 実装が入口。llive は実 LLM fitness 実走が keystone。xct/VLM は「GPU 無しでは事実上不可」の新規ライン（3DGS/INR/拡散/LoRA）だが Phase 順守。

---

# Part C — 実機で確認すべき未解決事項（open questions）

1. **torch の実 wheel タグ**（cu128/cu130/cu132 のどれが torch 2.12 系で存在するか）— `pip index versions` で live 確認。
2. **DSP プリインストールの Win11 ビルド番号**（24H2/25H2/26220.6772+）→ どの OOBE バイパスが効くか。
3. **WSL2 GPU パススルー**が driver 導入直後に成立するか（`wsl -- nvidia-smi`）+ **matmul 関門**（sm_120 の PTX JIT）が通るか= Blackwell 実働の最終裁定。
4. **jax[cuda12] vs [cuda13]** のどちらが 5090+WSL2 で clean に CudaDevice を出すか（両方試して決める）+ mujoco-mjx との pairwise 互換。
5. **MJX の Hill 筋/tendon サポート**（evis/myohand 実手が MJX で回るか=筋 RL 項目の分岐点）。
6. **firecrawl API キーの出所**（現機で ccr プロセス env への一時注入か）→ 新機は firecrawl.dev 再取得。
7. **github remote MCP の OAuth トークン**が .claude.json コピーで生き残るか（`claude mcp list` で実測）。
8. **BitLocker/Device Encryption が出荷時 ON か**（`manage-bde -status C:`）。
9. **ollama 27G / HF 9G** を staging に含めるか（新機回線速度で判断）。
10. **trading（alpaca）廃止後の要否**（不要なら alpaca MCP/playwright ブラウザ DL をスキップ）。

**honest caveats**: 消費者 RTX 5090 上で MJX 学習が「動いた」とバージョン付きで明言する公開事例は web 確定できず（正の傍証は間接的、唯一の直接事例 #299 は失敗報告）→ **実機の matmul 関門が唯一の裁定者**。torch/jax の版タグ・bitsandbytes の Blackwell ペナルティ改善・codex auth.json 可搬性・github MCP OAuth 生存は全て着荷後の実測待ち。

---

# Part D — 着手順序（Day-by-day）

- **着荷前（現機）**: §A0（★未 git repo バックアップ / D: スキャン / **`.claude`=memory を D: へコピー** / 任意 WSL export）。暗号化バンドル・A0-fix は使うなら（新方針では optional）。
- **Day 1**: ローカル `puruy` OOBE / BitLocker escrow → D: レター固定 + sentinel → driver 確認 → **torch cu130 入替 + gpu_smoke.py PASS**（§A3）→ **`.claude`(memory) を C: へ戻す** + env 秘密 3 本を再設定（or 再発行）。
- **Day 2**: WSL2 Ubuntu 構築 + jax[cuda12] + **matmul 関門** + **MJX spike go/no-go**（§A4）→ 各 project venv 再生成（§A5）→ MCP/CLI 再導入・再認証（§A6）→ `verify_new_machine.ps1` 緑。
- **Day 3+**: **GPU 初手 = 箸 MJX rollout throughput gate → 通れば閉ループ RL 本丸（P0）**。並走で llcore plateau プローブ overnight（P0）。以降 Part B の優先度順。
- **全緑後**: 鍵ローテ（§A7）→ 旧ノート退役判断。**旧ノートは全緑 + ローテ完了までワイプ禁止**（実質バックアップ）。

> 更新履歴: 2026-07-24 初版（Fable5/ultracode、Workflow `wf_aa632297-bc8` + 現機実測監査）。前提「D: そのまま移動」確定・環境深掘り（torch/JAX-MJX-WSL2/依存/MCP/secrets）を新規反映。
