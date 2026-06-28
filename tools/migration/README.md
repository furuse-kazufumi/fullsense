# GPU PC 移行ツール (C: 常駐分 staging + D: 外付け物理移送)

現機(HP ノート i7-1065G7)から新機(arkhive GL-I7G59M / **RTX 5090 32GB / 128GB RAM /
Win11 Pro**)へ移行する。**新前提 = D: は外付け SSD 本体(SanDisk Extreme 55AE, exFAT, 平文,
USB)を新機へ物理接続しレター D: を温存する。D: は robocopy しない**(D: ごと travels)。
backup/restore が運ぶのは **C: 常駐分のみ**で、中継ステージング `D:\_c_migration\` を経由する。
新機では **同一絶対パス**へ push-button 復元する。

> **正本(必読)**
> - `D:\projects\fullsense\docs\research\gpu_pc_migration_plan_2026-06-28.md`
>   (§2 パス戦略 / §2-2 Day-of レター固定 / §2-3 Phase 2 内蔵化 / §3 データ移行 / §5 検証 / §7 タイムライン)
> - `D:\projects\fullsense\docs\research\migration_manifest_2026-06-28.md`
>   (§1 D: ボリュームの事実 / §2 C: 常駐 inventory / §5 secrets / §6 GPU 配線 / §7 bootstrap)

移行設計の核心は **「ドライブレター・絶対パスを温存する」**(plan §2)。tool-guard グローバル
hook・ccr・raptor・llcore が `C:\Users\puruy\...` と `D:\...` を絶対パスでハードコードしている
ため、新機でも同一パスを再現できればハードコード破損ゼロで動く。D: は外付け本体をそのまま
持ち込みレター D: に固定するので `D:\...` 側は無移送で温存され、C: 常駐分だけ運べばよい。

> **D: ボリュームの事実(一次検証済)**: SanDisk Extreme 55AE / **exFAT**(非ジャーナル)/
> HealthStatus=Warning / "Full Repair Needed" / **ダーティビット SET** / BitLocker None(**平文**)/
> BusType=USB。物理移送=コピー不要だが、**唯一コピー + 非ジャーナル携帯ディスク**のため、
> 移送前に read-only スキャン(`Repair-Volume -Scan`)と off-disk 保険(secret bundle・未push
> git bundle・RAD 一部を別媒体)を必ず取る。落下/不正取り外し/exFAT 修復失敗 = 全データ単一障害。

---

## スクリプト一覧

| ファイル | 役割 | 実行マシン |
|---|---|---|
| `backup_working_set.ps1` | **C: 常駐分**を `D:\_c_migration\` へ robocopy `/MIR` で staging + reference export | **現機**(着荷前) |
| `restore_working_set.ps1` | `D:\_c_migration\` → 新機 C: の **同一絶対パス**へ復元 | **新機**(着荷後) |
| `migrate_secrets.ps1` | (A)off-disk 損失保険 + (B)C: 常駐 secret の暗号化バンドル / 復元 | 現機(Bundle)→ 新機(Restore) |
| `verify_new_machine.ps1` | 移行後チェック(Check 0 = D: レター/健全性 → 緑、以降 plan §5 項目 + C: 常駐検証を集計) | **新機**(復元後) |
| `gpu_smoke.py` | RTX 5090 / Blackwell sm_120 の最小 GPU smoke(verify から呼ばれる / 単体可) | 新機 |

すべて PowerShell 7(pwsh)/ UTF-8(BOM なし)/ 冪等。robocopy `/MIR` は差分のみ転送するので
再実行で増分同期になる。`.git` は除外しない(repo 履歴温存)。**D: ターゲットは backup/restore の
両方から完全に除去済**(外付け = D: なので、旧設計の `Test-Path 'D:\'` 通過で本物の D: を
`/MIR` purge する事故を構造的に防ぐ)。

### ステージング上のレイアウト(`D:\_c_migration\` に C: をドライブレター展開)

`backup` は C: 常駐の絶対パスをドライブレター = フォルダ名に展開して `D:\_c_migration\` 直下へ
保存し、`restore` が逆変換して C: の同一絶対パスへ戻す。D: 配下は外付け本体に既にあるため
ここには現れない:

```
D:\_c_migration\C\Users\puruy\.claude               (hooks/memory/settings.json/skills)
D:\_c_migration\C\Users\puruy\.claude.json          (57KB 単一ファイル・MCP 配線本体)
D:\_c_migration\C\Users\puruy\.codex                (config.toml/memories/state ※auth は除外)
D:\_c_migration\C\Users\puruy\browser-use-project   (alpaca_state.json 等の live state)
D:\_c_migration\C\Users\puruy\.gitconfig            (単一ファイル)
D:\_c_migration\C\Users\puruy\AppData\Roaming\GitHub CLI   (gh hosts.yml)
D:\_c_migration\C\Users\puruy\Documents\PowerShell  (PS profile)
D:\_c_migration\C\Users\puruy\.config
D:\_c_migration\C\Users\puruy\.cache\huggingface    (任意・9G)
D:\_c_migration\C\Users\puruy\.ollama\models        (任意)
D:\_c_migration\reference\user_path.txt             (User PATH)
D:\_c_migration\reference\user_env_nonsecret.txt    (secret 3 キーは除外)
D:\_c_migration\reference\scheduled_tasks\*.xml      (Export-ScheduledTask)
D:\_c_migration\_migration_logs\*.log               (backup のログ)
```

---

## ★秘密の扱い(最重要 / plan §5・manifest §5・再スコープ)

**物理移送では `D:\api-keys.json` と raptor `settings.local.json` は D: 上 = travels**(別送不要)。
旧設計の「working-set ミラーから除外して別経路で運ぶ」目的は消滅した。新前提での secret 課題は
2 つに再定義され、`migrate_secrets.ps1` が両方を扱う:

- **(A) off-disk 損失保険** … D: は平文 exFAT の携帯ディスク(ダーティビット SET / Full Repair
  Needed)で唯一コピー。落下/修復失敗で全消失し得るため、`D:\api-keys.json` と
  `D:\tools\raptor\.claude\settings.local.json`(平文 `ANTHROPIC_API_KEY`)+ 任意で未push git
  bundle を **別媒体へ保険コピー**する(D: travels だが落下時の保険)。
- **(B) C: 常駐 secret の暗号化バンドル** … staging に平文で置けない C: 上の秘密
  (`C:\Users\puruy\.codex\auth.json` / `C:\Users\puruy\.claude\.credentials.json` /
  `C:\Users\puruy\.ssh\id_ed25519`(+`.pub`))+ User env 平文 3 キー
  (`ANTHROPIC_API_KEY` / `TELEGRAM_BOT_TOKEN` / `SOCIALDATA_API_KEY`、`SECRET_user_env.txt` として
  同梱)を 7-Zip AES-256 + ヘッダ暗号化(`-mhe=on`)でバンドルする。

`backup_working_set.ps1` は `.credentials.json` / `.codex\auth.json` / `.ssh` / env 3 キーを
staging に **含めない**(`/XF` 除外)。これらは必ず `migrate_secrets.ps1 -Mode Bundle` の暗号化
バンドル経由で運ぶ。`.credentials.json` は端末紐づきのため **新機は claude 再ログイン前提**。
**鍵ローテーションは到着直後に手順化**(`api-keys.json` 再発行 + 旧キー失効 + env3キー再発行)。
バンドル zip は staging の D: とは **別の暗号化 USB** に置く。

7-Zip が無い場合は `Compress-Archive`(**暗号化されない**)にフォールバックし、暗号化 USB を
使うよう警告する。導入推奨: `winget install 7zip.7zip`。

---

## 手順(plan §7 タイムラインに沿って)

### A. 着荷前(現機・staging + 保険 + D: スキャン)

1. **D: read-only スキャン**(ダーティビット対処。先に保険を取ってから):
   ```powershell
   Repair-Volume -DriveLetter D -Scan          # read-only。dirty/修復必要を確認
   # 修復が必要なら off-disk 保険を取った後で:
   # Repair-Volume -DriveLetter D -OfflineScanAndFix
   ```
2. **C: 常駐分を `D:\_c_migration\` へ staging**(まず DryRun で対象とサイズを確認):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\backup_working_set.ps1 -Dest D:\_c_migration -DryRun
   ```
3. 問題なければ実 staging(初回はフル、以後は差分)+ reference export:
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\backup_working_set.ps1 -Dest D:\_c_migration
   ```
   - run 出力(`out\` / `.out\`)も含めたい場合のみ `-IncludeRunOutputs`。
   - 着荷直前に **もう一度** 同じコマンドを実行 → 差分だけ追いつき最新化。
   - reference(User PATH / env 非 secret / Scheduled Tasks XML)も同時に export される。
4. **secret は別経路で**(off-disk 保険 + C: 常駐バンドル。7-Zip があれば AES-256 + ヘッダ暗号化):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\migrate_secrets.ps1 -Mode Bundle
   # 既定で Desktop\fullsense-secrets\fullsense-secrets-<時刻>.7z を作成(パスワード対話入力)
   ```
   - 出力バンドルは staging の D: とは **別の暗号化 USB** に置く(`_migration_logs` を検出すると
     安全のため中止 / 意図的なら `-Force`)。
5. 旧機 trading 停止(`alpaca_state.json` 凍結)。**旧ノートは新機が緑になるまでワイプ禁止**
   (実質バックアップ)。

### B. 着荷後 Day 1(新機セットアップ → D: 接続 → C: 復元)

1. OOBE は **ローカルアカウント `puruy`**(plan §2-1)。MS アカウントで作ると
   `C:\Users\<先頭5字>` 等になり全 hook/memory/.claude.json/gh/gitconfig が破損する。
2. **新機 C: BitLocker 回復キー escrow**(Day-1 初手):
   ```powershell
   manage-bde -status C:        # Win11 Pro は Device Encryption 既定 ON の可能性
   # 回復キーを MS アカウント + パスワードマネージャ + 紙 の 3 重で控える
   ```
3. **D: 接続・レター固定**: 他の removable を全部外し外付けを単独接続 →
   `Get-Disk` / `Get-Partition` / `Get-Volume` で確認 → SanDisk が E: 等なら:
   ```powershell
   Set-Partition -DiskNumber <n> -PartitionNumber 1 -NewDriveLetter D   # GptId 束縛で永続
   Test-Path D:\tools\raptor                                            # 温存確認(True 必須)
   ```
   - D: が別物に取られていたら先に `Remove-PartitionAccessPath` してから付与(plan §2-2)。
4. **C: 常駐分を復元**(まず DryRun 推奨):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\restore_working_set.ps1 -Source D:\_c_migration -DryRun
   pwsh -File D:\projects\fullsense\tools\migration\restore_working_set.ps1 -Source D:\_c_migration
   ```
   - 実行前に **ユーザー名 puruy**(`-ne 'puruy'` で throw)+ **D: が本物の作業ディスクか**
     (sentinel `D:\tools\raptor` 存在)を fail-closed チェックする。
   - `/MIR` は復元先の余剰を削除する。新機がクリーンなら安全。確認を省くなら `-Force`。
5. **secret を元パスへ配置**(**verify の前に**):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\migrate_secrets.ps1 -Mode Restore -Source <暗号化USB>\fullsense-secrets-<時刻>.7z
   # C: 常駐 secret(.codex\auth.json/.credentials.json/.ssh)+ 保険分を元の絶対パスへ復元
   ```
   - User env 3 キーは `setx` で再適用(または **再発行を推奨**)。
   - Scheduled Tasks は reference XML を `Register-ScheduledTask -Xml` で再登録し、
     **action の C: 依存を是正**(`RAPTOR-Backup`/`CorpusUpdate` の `C:\Python314\python.exe` +
     不在の `C:\Users\puruy\raptor\...` を `py -3.11` + `D:\tools\raptor\libexec` へ書換)。
   - `.credentials.json` は端末紐づき = 新機で **claude 再ログイン**前提。
6. **GPU 基盤**: NVIDIA driver **R570+**(Blackwell)→ `py -3.11` → `torch` **cu128** →
   `get_device_capability()==(12,0)`。
7. **ツール再導入**: Node v24(+`npm rebuild` node-pty=native ABI)/ git / gh(再auth)/
   rustup + rtk(`C:\tools\rtk\rtk.exe`)/ uv / semgrep / Claude Code native installer
   (`C:\Users\puruy\.local\bin\claude.exe`)/ Codex CLI。**MCP は `.claude.json` コピーで再現**
   (手再設定不要)。User PATH を reference から再構築。

### C. 着荷後 Day 1(検証)

```powershell
pwsh -File D:\projects\fullsense\tools\migration\verify_new_machine.ps1
# 現機(GPU 無し)でドライラン確認するなら GPU 項目を抜く: -SkipGpu
```
Check 0(D: レター/健全性 → 緑、ユーザー名 puruy)を先頭に、plan §5 の 7 項目 + C: 常駐検証
(`.claude.json`/`mcpServers`、`.codex`、`alpaca_state.json`、env3キー、`gh auth`/`.gitconfig`、
Scheduled Tasks の action パス)を集計する。

### D. 安定化と後日 Phase 2

- trading 系(Alpaca paper)の二重起動回避を確認(plan §7 / manifest §4)。
- llcore の **device 配線**(`Trainer`/`TBPTTTrainer`/plateau experiment に `--device`、manifest §6)。
- 初手 GPU ワークロード = 本日プローブの GPU フル版(`--device cuda`)。
- **当面は USB 外付け D: 運用を固める**: USB selective suspend 無効 + standby/hibernate AC=0 +
  デバイス「電源オフを許可」オフ + Better performance + BIOS 起動順 = 内蔵 NVMe 最優先。
- **(後日)Phase 2 = D: を内蔵 NVMe(NTFS)へ移管**(安定化・冗長化・exFAT 脱却。plan §2-3):
  別途内蔵 NVMe を増設し NTFS で X: 初期化 → `robocopy D:\ X:\ /MIR /XJ /R:1 /W:1 /COPY:DAT /DCOPY:DAT`
  → 外付けを Y: に降格・内蔵 X: を D: に昇格 → 内蔵 D: を BitLocker 暗号化 +
  `Enable-BitLockerAutoUnlock -MountPoint D`。外付けは backup 退役。**旧ノートはこの緑化まで温存**。

---

## Day-of マスターチェックリスト(順序付き / plan §7)

1. **旧機(出発前)**: ① `Repair-Volume -DriveLetter D -Scan`(read-only)→ ダーティ/修復必要なら
   先に off-disk 保険(secret bundle・未push git bundle・RAD 一部を別媒体)→ 必要時 `-OfflineScanAndFix`。
   ② `backup_working_set.ps1 -Dest D:\_c_migration`(C: 常駐分 staging + reference export)。
   ③ 旧機 trading 停止(`alpaca_state.json` 凍結)。④ 新機 C: BitLocker 回復キー控え方針。
2. **シャットダウン → 「ハードウェアの安全な取り外し」で D: 取り外し**(exFAT は怠ると破損)。
   chain-of-custody で移送(預け荷物にしない)。
3. **新機セットアップ**: OOBE で **ローカルアカウント `puruy`**。`manage-bde -status C:` →
   回復キー escrow(MS アカウント + PW マネージャ + 紙)。
4. **D: 接続・レター固定**: 他 removable を全外し外付け単独接続 →
   `Set-Partition ... -NewDriveLetter D` → `Test-Path D:\tools\raptor` 温存確認。
5. **C: 常駐分復元**: `restore_working_set.ps1 -Source D:\_c_migration` →
   `migrate_secrets.ps1 -Mode Restore` → env3キー `setx`(または再発行)→ tasks XML import +
   action 是正。`.credentials.json` は新機で **claude 再ログイン**前提。
6. **GPU 基盤**: NVIDIA driver R570+ → `torch cu128` → `get_device_capability()==(12,0)`。
7. **ツール再導入**: Node v24(+`npm rebuild` node-pty)/ git / gh(再auth)/ rustup + rtk / uv /
   semgrep / Claude Code native installer / Codex CLI。MCP は `.claude.json` コピーで再現。
   User PATH を reference から再構築。
8. **検証**: `verify_new_machine.ps1`(Check0 = D: レター/健全性 → 緑、以降全項目)。
9. **初手 GPU**: plateau プローブを `--device cuda` でフル(配線済)。
10. **(後日)Phase 2**: 内蔵 NVMe 増設 → robocopy → レタースワップ → 内蔵 D: を BitLocker。
    外付けは backup 退役。旧ノートはこの緑化まで温存。

---

## 各スクリプトの引数

### backup_working_set.ps1(現機)
| 引数 | 説明 |
|---|---|
| `-Dest <root>` | **必須**。C: 常駐分の staging 先ルート(既定 `D:\_c_migration`)。ドライブルートや対象内側は拒否。 |
| `-DryRun` / `-WhatIf` | robocopy `/L`(リスト表示のみ・コピーしない)。 |
| `-IncludeRunOutputs` | `out\` / `.out\` も含める(既定は除外し明示ログ)。 |

対象は **C: 常駐・非 secret のみ**(`.claude` / `.claude.json` / `.codex` / `browser-use-project` /
`.gitconfig` / gh hosts / PS profile / `.config` / hf-cache / ollama)。**D: 配下は対象外**(travels)。
除外: `__pycache__ *.pyc .venv venv node_modules .mypy_cache .pytest_cache .ruff_cache *.tmp`
+ secret(`.credentials.json` / `.codex\auth.json` / `.ssh` / env3キー = `migrate_secrets` へ)。
各ジョブのログは `<Dest>\_migration_logs\<name>.log`。末尾で reference(User PATH / env 非 secret /
Scheduled Tasks XML)を `<Dest>\reference\` へ export。最後に対象ごとのコピー済バイト/失敗を集計。

### restore_working_set.ps1(新機)
| 引数 | 説明 |
|---|---|
| `-Source <root>` | **必須**。staging 元ルート(backup の `-Dest` と同じ。既定 `D:\_c_migration`)。 |
| `-DryRun` / `-WhatIf` | robocopy `/L`(リスト表示のみ)。 |
| `-IncludeRunOutputs` | `out\` / `.out\` も復元。 |
| `-Force` | `/MIR` purge の確認プロンプトを省略。 |

fail-closed: `$env:USERNAME -ne 'puruy'` で **throw**、`D:\tools\raptor`(sentinel)で D: が本物の
作業ディスクか確認(別ボリュームが D: 化けの検出)。**D: ターゲットは無し**(C: のみ復元)。
復元後に reference(User PATH / env)を `setx` 再適用(secret 除く)、Scheduled Tasks XML を
`Register-ScheduledTask -Xml`(action の C: 依存は `D:\tools\raptor` + `py -3.11` へ要手修正と注記)。

### migrate_secrets.ps1(現機 → 新機)
| 引数 | 説明 |
|---|---|
| `-Mode Bundle` | 既定。(A)off-disk 損失保険 + (B)C: 常駐 secret を暗号化バンドルにまとめる。 |
| `-Mode Restore` | バンドルを展開し元の絶対パスへ配置(新機での再構築用)。 |
| `-Out <dir>` | Bundle の出力先(既定 `Desktop\fullsense-secrets`)。staging の D: には置かない。 |
| `-Source <zip>` | Restore する `.7z` / `.zip`。 |
| `-Force` | Restore で既存上書き / Bundle で外付け警告を無視。 |

対象 secret: 保険 = `D:\api-keys.json` / `D:\tools\raptor\.claude\settings.local.json`、
C: 常駐 = `.codex\auth.json` / `.claude\.credentials.json` / `.ssh\id_ed25519`(+`.pub`)+
User env 3 キー(`SECRET_user_env.txt` 同梱)。7-Zip が無い場合は `Compress-Archive`
(**暗号化されない**)にフォールバックし、暗号化 USB を使うよう警告する。

### verify_new_machine.ps1(新機 / read-only)
| 引数 | 説明 |
|---|---|
| `-LlcoreDir <path>` | llcore リポジトリ(既定 `D:\projects\llcore`)。 |
| `-SkipGpu` | GPU 系チェック(torch.cuda / gpu_smoke / llcore forward / plateau)を SKIP。 |

先頭に **Check 0**(0a = D: レター/FileSystem/HealthStatus/BusType・sentinel 誤マウント検出 /
0b = ユーザー名 `puruy` fail-closed)。続いて plan §5 の 7 項目(torch.cuda、capability (12,0)+
小 GEMM、llcore golden 一致、plateau smoke、tool-guard live、RAD corpus、ツール存在)、さらに
C: 常駐検証(`.claude.json`/`mcpServers`、`.codex`/`alpaca_state.json`、env3キー、`gh auth`/
`.gitconfig`、Scheduled Tasks の action パス)を `✓ Pass / ✗ Fail / - Skip` で集計。Fail があれば
exit 1。破壊的操作・git・外部送信は一切しない。

### gpu_smoke.py(新機 / verify から呼ばれる・単体可)
`py -3.11 gpu_smoke.py`(`PYTHONUTF8=1` 前置推奨)。torch import → cuda → capability (12,0)
→ 小 GEMM → `nn.Linear.to('cuda')` を順に確認し 1 行 JSON を出力。終了コード契約:
**0**=全 PASS / **2**=cuda 不可(環境差 → verify は SKIP)/ **1**=実不具合。

---

## 安全注意(まとめ)

- **D: は外付け本体(平文 exFAT・ダーティビット SET・Full Repair Needed)で唯一コピー**。
  落下/不正取り外し/exFAT 修復失敗 = 全データ単一障害。移送前 read-only スキャン + off-disk 保険 +
  安全な取り外し + chain-of-custody + 着荷直後の鍵ローテ + Phase 2 内蔵 NTFS 化で緩和。
- backup/restore は **C: 常駐分のみ**を `D:\_c_migration\` 経由で運ぶ。**D: は robocopy しない**。
  D: ターゲットは両スクリプトから除去済 = 本物の D: を `/MIR` purge する事故は構造的に起こらない。
- robocopy `/MIR` は **ミラー**(復元先の余剰を削除)。`restore` を既存環境へ向けるときは注意。
- クロスマシン移行のため ACL は持ち込まない(`/COPY:DAT`)。junction はループ防止で除外(`/XJ`)。
- **秘密を staging に混ぜない**。`migrate_secrets.ps1` の暗号化バンドル + 別 USB を使う。
  User env 3 キーはファイルでないため travels で拾えない = 必ずバンドル + 再発行で扱う。
- USB 外付け D: の常時運用は切断/selective-suspend に注意(tool-guard hook が fail-open すると
  保護が無音で消える)。selective suspend 無効 + standby/hibernate AC=0 で固める。
- 日本語 Windows でも robocopy サマリを正しく集計できるようロケール非依存パーサを使用。
- これらは作成・構文検証済み。**D: レター固定後**に DryRun → 実行の順で使うこと。
