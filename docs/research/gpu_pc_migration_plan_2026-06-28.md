# GPU PC 移行計画 (target: 2026-07 中旬 / 2–3 週間先)

> 作成 2026-06-28。前提・確定事項の正本 = memory `project_gpu_pc_consideration_2026_06_21`
> (購入意向確定 2026-06-27) / `feedback_gpu_rent_over_buy`(rent-first を 24/7 研究用途で上書き)
> / `feedback_claude_max_compute_priority`(GPU 投入は decision-relevant な実測を優先)。
> 経済性の旧正本 = `gpu_portfolio_decision_2026-06-02.md`(RENT-FIRST、128GB級向け)。
> 本計画は **24GB 級の自前デスクトップを買って移行する**最新方針に基づく runbook。

## 0. 確定事項(議論済み・蒸し返さない)

- **方針**: 自前 24GB GPU デスクトップを **買って移行**。24/7 専有(ゲームしない・llcore は実験キュー豊富で遊休しない)なら自前が事実上唯一解(クラウド A100 24/7 ≈ 月30万 vs 自前 電気 ~月1万)。128GB級の rent-first 判断はスケールが違うので本件には不適用。
- **CUDA C はほぼ不要**: ①動かす=自前 forward は PyTorch なので `model.to("cuda")` で自動 GPU(cuBLAS/cuDNN)/②高速化=Triton or 既存lib(bitsandbytes / flash-linear-attention / llama.cpp)/③CUDA C 自作は最後の手段で射程外。**forward を PyTorch で書いたことが移植性として効く**。
- **即始動準備済(2026-06-27)**: 自前 forward が HF transformers と golden 一致(CPU 実証)/ 改造①〜④(linearize/quant/loader-mmap/distill)実装 / 正直な評価器 proxy v2 整備。GPU 到来で「黄/赤ブロックを緑にする本走」を即投入可。
- **移行元(実測 2026-06-28)**: HP ノート **i7-1065G7 (4C/8T, 1.3GHz, 15W mobile) / RAM 16GB(オンボード=増設不可)/ Intel Iris(CUDA GPU 無し)/ Win11 Pro**。C: 568/952GB free、D: 1075/1863GB free(used ~788GB)。py: **3.11 が default**(+3.14/3.9/uv 3.12)。**このノートが CPU 本走 6–9h の真因**=流用ゼロ・新規デスクトップ必須。
- **★移送方式(2026-06-28 一次検証で確定)**: **D: は外付け SSD 本体(SanDisk Extreme 55AE, exFAT, 平文, BusType=USB)を新機へ物理接続しレター D: を温存する**。内蔵 2TB は **C: 単一(分割しない)**。`D:/` の robocopy は不要 = **D: ごと travels**。残作業は **C: 常駐分のステージング** のみ(`.claude`/`.claude.json`/`.codex`/browser-use live state/ssh/env 等)。D: は現在 **HealthStatus=Warning / ダーティビット SET / 唯一コピー** のため移送前に read-only スキャン + off-disk 保険が必須(§8)。

## 1. ハードウェア(★購入確定 — 注文明細 2026-06-28、組立後出荷待ち)

**arkhive Gaming Limited GL-I7G59M Founders Edition(型番 AG-IA24D2TB86MGB9F-CF4) 税込 ¥978,000**
(<https://www.ark-pc.co.jp/i/72003600/>)。当初推奨(中古3090/4090・24GB)を大きく上回るハイエンド → 開いていたハード判断は**すべて解決**。

| 部品 | 確定スペック | 計画への含意 |
|---|---|---|
| **GPU** | **GeForce RTX 5090 Founders Edition / 32GB GDDR7(Blackwell, sm_120)** | VRAM 32GB = 3B 快適・7–14B fine-tune 可・70B int4 は際どい。★ソフト=**driver R570+ & torch cu128 必須**(§4) |
| **CPU** | **Intel Core Ultra 7 270K Plus**(Arrow Lake, LGA1851)| 旧ノート 15W i7-1065G7 比で桁違い。前処理/データ load も加速 |
| **RAM** | **128GB DDR5-5600(64GB×2 Crucial Pro CL46 EXPO ※OCメモリ)** | 大コーパス前処理・CPU offload に大余裕。★EXPO は AMD 系プロファイル=Intel B860 では XMP/手動で定格化、無ければ JEDEC で動く(BIOS 確認) |
| **マザボ** | **ASRock B860M Steel Legend WiFi(Micro-ATX, WiFi/BT 内蔵)** | M.2 追加スロットあり(後で 2nd SSD = D: 増設可。§2)|
| **SSD** | **2TB NVMe PCIe4.0 x4(Princeton PHD-ISM2G4)1 本のみ・パーティション分割なし** | ★**既定で C: だけ・D: が無い**=パス温存に対策必須(§2)|
| **電源** | **1000W 80+ GOLD(Cooler Master Elite Gold 1000)** | RTX 5090 TGP ~575W + transient に十分 |
| **CPUクーラー** | Cooler Master V4 Alpha 3DHP(デュアル 12cm サイドフロー)| 空冷・標準 |
| **ケース** | **Cooler Master MasterFrame 400 Mesh Silver【入荷待ち】** | ★ケース入荷待ち=出荷遅延リスク(§7)|
| **OS** | **Windows 11 Pro 64bit DSP プリインストール** | ★OS インストール不要。dev 環境を載せるだけ |
| 保証 | 通常保証 1年(標準構成)| 周辺機器/Office/セキュリティ無し |

- **VRAM 32GB**: llcore 射程 ≤32B の線形化/量子化/蒸留に余裕。3B 本走・StateX continued-train・proxy v2 フル走を快適に。70B は int4 で際どい(Claude 代替不可なので無理に狙わない)。
- **速度**: 旧ノート CPU 本走 6–9h は、3090 想定で 1–2h。**RTX 5090 は 3090 比 ~2–3×** → 本日プローブ級は**数分〜数十分**見込み(forward 律速分のみ加速=Amdahl、楽観しない)。
- **128GB RAM** が効く場面: 大コーパス(RAD/aozora)前処理、複数モデル同時 load、CPU-offload による大型モデルの一部実行、データ生成。

## 2. パス戦略(★最重要 — 破損回避の鍵)

**現 `D:/` レイアウトを新機で完全再現する**(ドライブレター・絶対パスを温存)。理由 = ハードコード多数:

- **tool-guard グローバル hook** が `python "D:/tools/raptor/libexec/raptor-tool-guard"` を絶対パスで参照(`~/.claude/settings.json`)。
- ccr / raptor が `RAPTOR_DIR` / `RAPTOR_CALLER_DIR`、多数の `D:/` 絶対パス、`D:/api-keys.json`、`D:/docs`(RAD)、`D:/tools/raptor-analytics.db`。
- llcore/fullsense スクリプトの `D:/projects/...`、Task Scheduler ジョブの絶対パス。

→ 新機でも **C:/Users/puruy/** と **D:/** を同名で用意。**D: は内蔵分割でなく外付け SSD 本体を物理接続してレター D: を温存する**(§2-2)ので、`D:/` 配下のハードコードは robocopy 不要でそのまま成立する。C: 常駐分のみ展開(§3)。パス変更は原則しない(変えるなら一括 grep して洗い出し)。

### 2-1. Windows ユーザー名は `puruy`(★最優先)

- **Windows ユーザー名を `puruy` で作成**(初回セットアップ時)。グローバル hook が `C:/Users/puruy/.claude/hooks/...`、memory が `C:/Users/puruy/.claude/projects/...` を参照するため、ユーザー名が違うと全 hook/memory/`.claude.json`/gh/gitconfig パスが破損。**最優先**。
- ★**MS アカウントで OOBE すると `C:\Users\<先頭5字>`(例 `C:\Users\puruy` にならず `C:\Users\furus` 等)になり全 hook/memory/.claude.json/gh/gitconfig が破損する** → **必ずローカルアカウント `puruy` で作成**(OOBE でネット切断 or「サインインオプション→オフライン アカウント」)。
- C: を揃えたら **§3 の C: 常駐 inventory を同一絶対パスへ展開**、`D:/` 配下はレター固定だけで温存。残る環境差(`C:/Python314` 等の py インストール先、`RAPTOR_DIR`)は §4 で再設定。

### 2-2. Day-of: D: レター確認・固定(★全手順の前提)

外付け SanDisk Extreme(exFAT/USB)を接続し、**レター D: を確実に割り当てる**。新機は内蔵 2TB が C: 単一なので D: は空いている公算が高いが、他 removable と衝突し得るため固定する。

1. **他の removable / USB ストレージを全部外し**、外付け SanDisk を**単独**接続する(レター取り合いを排除)。
2. 確認: `Get-Disk` / `Get-Partition` / `Get-Volume`(SanDisk Extreme 55AE / exFAT / Size ~2.0TB を識別)。
3. SanDisk が **E: 等になっていたら D: へ付け替え**(GptId 束縛で永続):
   ```powershell
   Set-Partition -DiskNumber <n> -PartitionNumber 1 -NewDriveLetter D
   ```
4. **D: が別ボリュームに取られていた**ら、先に解放してから付与:
   ```powershell
   Remove-PartitionAccessPath -DiskNumber <別disk> -PartitionNumber <p> -AccessPath 'D:\'
   Set-Partition -DiskNumber <n> -PartitionNumber 1 -NewDriveLetter D
   ```
   diskpart 版: `diskpart` → `list volume` → `select volume <n>` → `assign letter=D`。
5. **温存確認(sentinel)**: `Test-Path D:\tools\raptor`(true なら本物の作業ディスクが D: にマウントされている)。`fsutil fsinfo volumeinfo D:` で exFAT を再確認。
6. exFAT は非ジャーナル=破損に弱い。当面 USB 運用のまま検証し、安定後に §2-3 の内蔵 NVMe 化で恒久化する。

### 2-3. Phase 2: D: を内蔵 NVMe(NTFS)へ移管(後日・安定化/冗長化/exFAT 脱却)

外付け筐体(SanDisk Extreme Portable)は封止・基板直付けの公算大=分解 harvest は見込み薄。よって **別途内蔵 NVMe を増設し D:→内蔵へ copy** してレタースワップする(harvest でなく copy)。

1. **内蔵 NVMe を B860M の空き M.2 に増設** → NTFS で初期化し一時レター **X:** を割当。
2. **全コピー**(ジャンクション保護・属性保持):
   ```powershell
   robocopy D:\ X:\ /MIR /XJ /R:1 /W:1 /COPY:DAT /DCOPY:DAT
   ```
3. **レタースワップ**: 外付けを **Y: に降格** → 内蔵 X: を **D: に昇格**(`Set-Partition ... -NewDriveLetter`)。
4. **内蔵 D: を BitLocker 暗号化** + `Enable-BitLockerAutoUnlock -MountPoint D`(平文 exFAT 脱却 + at-rest 保護)。
5. **外付け Y: は backup として退役温存**(旧ノートが緑化するまで唯一コピーを潰さない)。
6. **当面 USB 運用の固め**(Phase 2 まで外付けを酷使しないための堅牢化):
   - USB selective suspend を無効化:
     ```powershell
     powercfg /SETACVALUEINDEX SCHEME_CURRENT 2a737441-1930-4402-8d77-b2bebba308a3 48e6b7a6-50f5-4782-a5d4-53bb8f07e226 0
     powercfg /SETACTIVE SCHEME_CURRENT
     ```
   - standby/hibernate を AC=0 に / デバイスマネージャで該当 USB の「電源オフを許可」をオフ / ポリシーを Better performance に。
   - BIOS 起動順=**内蔵 NVMe 最優先**(外付けから起動しない)。
   - checkpoint / HF cache の書込先は **内蔵 C:** へ(外付けの write 摩耗と USB 律速を回避)。

## 3. データ移行(★方式転換 — D: 本体は travels / C: 常駐分のみ staging)

**D: 配下(`D:/projects`・`D:/tools/raptor`・`D:/tools`・`D:/docs`(RAD)・`D:/api-keys.json`・`D:/api-manager`)は外付け SSD 本体に載ったまま新機へ物理移送する = `D:` 本体で温存・移送不要(travels)**。robocopy も別経路コピーも不要で、絶対パスのハードコードはレター固定だけで成立する。**移行作業の対象は C: 常駐分のステージングだけ**。

**C: 常駐 inventory(実機で全実在確認済 2026-06-28 — これを staging で運ぶ)**:

| C: 常駐 | 分類 | secret | 備考 |
|---|---|---|---|
| `.claude\`(hooks/memory/settings.json/skills/.credentials.json) | copy | 一部 | 1.5G・ccr/tool-guard 核 |
| `.claude.json`(57KB) | copy(別ファイル) | ★ | MCP 配線・oauth・trust の本体。`.claude\` の **外** |
| `.codex\`(config.toml/auth.json/memories/goals/state) | copy+CLI 再導入 | ★auth | Codex 二本柱の核 |
| `browser-use-project\`(alpaca_state.json/telegram_offset.json) | copy | 一部 | trading live state・**code は `D:\projects`=travels** |
| `.ssh\`(id_ed25519) | copy | ★ | |
| `.gitconfig` / gh `hosts.yml` / PS profile / Win Terminal / `.config\` | copy(gh は再auth 可) | — | |
| `.cache\huggingface`(9G)/ `.ollama\models` | copy(再DL可) | — | 任意 |
| User env 3 secret + PATH | 再設定(secret は再発行推奨) | ★ | **ファイルでない=travels で拾えない** |
| Scheduled Tasks(Ready 4本) | XML export→import + action 是正 | — | |

- **転送手段**: C: 常駐分を **`D:\_c_migration\` へ staging**(`backup_working_set.ps1`)→ D: ごと travels → 新機で `restore_working_set.ps1` が同一絶対パスへ復元。LAN や別外付けは代替。
- **secret は staging に平文で置かない**: `.credentials.json` / `.codex\auth.json` / `.ssh\id_ed25519` / User env 3 キーは `migrate_secrets.ps1 -Mode Bundle` の暗号化バンドルへ(§8 / manifest §5)。
- 容量目安: C: 常駐の staging 主体は `.claude`(~1.5G)+ `.cache\huggingface`(~9G、任意)。D: 本体 used ~847GB は travels で運ぶため staging 容量に含めない。

## 4. 環境セットアップ(新機 OS 後)

1. **OS = Windows 11 Pro(プリインストール済 → インストール不要)**。現と統一で PowerShell/Git Bash 二本立て・パス互換・tool-guard/ccr/全スクリプトが Windows 前提。初回セットアップで **ユーザー名 `puruy`**(§2-1)。Linux は移行コスト大 → 非推奨。
2. **★NVIDIA driver = Blackwell 対応 R570 以降**(RTX 5090 = sm_120)。CUDA toolkit は PyTorch wheel 同梱のため driver のみで可。
3. **Python**: `py -3.11`(全 FullSense)+ 3.14/3.9/uv 3.12 を現状踏襲。
4. **★torch CUDA 版 = cu128(Blackwell 必須・cu124 不可)**: `py -3.11 -m pip install torch --index-url https://download.pytorch.org/whl/cu128`(2026 時点で安定 wheel あり。現 CPU torch 2.12 → cu128 版へ)。**検証**: `torch.cuda.get_device_capability()` が **(12, 0)** を返し、簡単な GEMM が `no kernel image` エラーを出さないこと(出たら torch 版が sm_120 未対応=cu128/nightly に上げる)。
5. **各 project 依存再構築**(pyproject から venv 再生成)。llcore は src レイアウト(`PYTHONPATH=src` or editable install)。
6. **ツール群再導入**: Git Bash / Node.js v24 / Rust 1.94 / uv / rtk(token killer)/ ccr(node-pty, zx build)。
7. **環境変数**: `RAPTOR_DIR` / `RAPTOR_CALLER_DIR` / `ANTHROPIC_API_KEY`(`settings.local.json`)/ `api-keys.json`。
8. **MCP servers 再設定**: osv-mcp / semgrep / sqlite(raptor-analytics.db)/ fetch / github / Google Drive / firecrawl / arxiv 等。
9. **Task Scheduler 再登録**: fullsense status telegram(平日11:30)/ trading 20分サイクル / api key sync 等。**★トレーディング(Alpaca paper)は時間依存** — 移行中の二重起動/欠損に注意(移行ウィンドウは旧機停止 or 明示一本化)。

## 5. 検証チェックリスト(移行後・順に緑化)

1. `py -3.11 -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"` → **True + GPU 名**
2. **llcore native forward GPU golden 一致**: `scripts/prove_native_matches_hf.py` を GPU で(CPU 一致は実証済 → GPU でも next-token argmax 一致を確認)
3. **小 GPU 学習 smoke**: ttt_plateau or chat 1 step を `.to("cuda")` で(本日の `--chunk-size` 経路含む)
4. **ccr 起動 → SESSION START 復元 → tool-guard live**(グローバル hook が `D:/tools/raptor` 温存パスで発火)
5. **raptor /scan smoke + MCP servers 応答**
6. **trading 系(paper)健全起動**(二重起動回避を確認)
7. **RAD corpus アクセス**(`D:/docs` 横断検索)
8. **rtk / 各 libexec / hooks(backup-hook auto-commit)** 動作

## 6. 移行後の初手 GPU ワークロード(compute-gated キュー)

`feedback_claude_max_compute_priority` に従い **decision-relevant な実測を先に**(方向を解決する work):

- **★本日のプローブ(chunk_size>128 plateau)を GPU でフル**: gated-deltanet + recurrent/recurrent-wide × chunk∈{128,256,512,1024} × **≥3 seeds**(CPU 9h/arm → GPU 数十分)。§13(4) の真の検証を一気に。
- **線形化 本訓練 + 蒸留 held-out 検証**(改造①④)。
- **int8 GPU カーネル**で 0.7tok/s 解消(改造②)。
- **StateX continued-train / 3B スケール**。
- **proxy v2 フル走**(K≥12、context sweep 2048–4096=SUPRA 級長文脈崩壊帯)。

> ★初手の前提 = **llcore 学習スクリプトの device 配線** → **✅ 実装済(2026-06-28、移行準備セッション)**。`Trainer`/`TBPTTTrainer`/eval/longctx/3 entry script に `--device auto`(cuda if available)を backward-compatible に配線、CPU byte-identical(既存スイート全 green)+ mypy/ruff PASS。**着荷後 Day 1 は GPU 本走コマンドに `--device cuda` を付けるだけ**。詳細 = `migration_manifest_2026-06-28.md` §6。

**新ブランチ候補(北極星とは別モダリティ — 意図的に選んでから着手)**:
- **VLM(Vision-Language)検証**: 32GB は 7B 級 VLM(Qwen2.5-VL-7B / InternVL2.5-8B / Llama-3.2-11B-Vision / Pixtral / MiniCPM-V)を full 精度で推論+LoRA、~32B を int4 で推論可。**FullSense 接続点** = manga-md(コマ画像→構造理解、`vlm_comic_comprehension`/`manga_craft`/`visual_narrative` corpus 既存)/ llove(SVG・図の VLM 批評)/ llterm・browser-use(スクショ grounding)/ 記事 craft(挿絵検証)。**全て on-prem=哲学合致**。
  - 着手順序(`feedback_claude_max_compute_priority`): まず (b)hello-world(7B を `.to("cuda")` で動かす smoke)→ 価値を見て (a)`rad-research`「ローカル VLM SOTA×manga 理解」で本腰スコープ。北極星(llcore GPU 本走)を先に緑化してから。

## 7. タイムライン(発注済・組立後出荷待ち / 2–3 週間先)

> ★**出荷はケース「Cooler Master MasterFrame 400 Mesh Silver」の入荷待ちに依存**。Ark に入荷/出荷予定日を確認し、着荷日を起点にスケジュールを確定する(2–3 週間=ユーザー予定と整合)。

- **着荷まで(現機で先行作業)**: ①外付け 2TB SSD 入手 ②**データ移行リハーサル**=現機 working set(`.claude/`+`D:/projects`+`D:/tools/raptor`+`D:/docs`)を外付けへコピー開始(ダウンタイム短縮)③`api-keys.json` の安全移送経路を準備 ④移行手順書(本 doc)を最終化。
- **着荷後 Day 1–2**: ①初期セットアップ(**ユーザー名 `puruy`**)②**2TB を C:+D: 分割**(§2-2A)③driver R570+ 導入 ④`torch cu128` 入れて `torch.cuda` 検証。
- **Day 3–5**: ①データ展開(**同一絶対パス**)②`py -3.11` + 各 venv/ccr/MCP/Task 再構築 ③検証チェックリスト(§5)緑化。
- **Day 6–7**: ①trading 系切替(二重起動回避)②**初手 GPU ワークロード**=本日プローブのフル版(3 arch×chunk×≥3seed)③旧ノートは予備/退役。

## 8. リスク・コンティンジェンシー

- **DDR5 高騰** → RAM 最小開始 + 後追い増設(mmap loader で system RAM 圧縮済)。
- **中古 3090 個体差/保証** → 保証付中古ショップ or 新品 4090。電源 850W+ 必須。
- **データ移行中の trading 欠損** → paper なので実害小だが、移行ウィンドウは旧機継続 or 明示一本化。
- **パス不一致による hardcode 破損** → **D:/ レイアウト完全温存**で回避(tool-guard グローバル hook の絶対パス含む)。移行後 `torch.cuda` + tool-guard + ccr の 3 点をまず確認。
- **torch CUDA × driver 版不整合** → driver は CUDA 12.4+ 対応、torch は cu124 wheel。
- **秘密の移送** → `api-keys.json` は外付け一括コピーに混ぜず別経路(暗号化 USB / パスワード zip)。

## 9. 残る意思決定(ハードは購入確定済み)

| 項目 | 推奨 | 備考 |
|---|---|---|
| **D: の用意** | 2TB を **C:+D: 分割**(追加費用ゼロ・即)| I/O 余裕や容量増したくなったら後日 2nd M.2 を D: 増設(§2-2B)|
| **データ移送手段** | **外付け 2TB NVMe SSD で一括** | LAN(robocopy /MIR)も可。`api-keys.json` は別経路(暗号化)|
| **trading 系の置き場** | 移行中は**旧機/クラウドに残置**(二重起動回避)→ 安定後に新機へ | paper なので実害小 |
| **C: / D: 容量配分** | 例 C:800GB / D:1.1TB | working set 数十GB+将来 checkpoint で D: 1TB+ 十分 |
| **RAM 定格化** | BIOS で XMP/EXPO 確認(無ければ JEDEC で運用)| 128GB あるので体感差は小 |
