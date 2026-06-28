# GPU PC 移行ツール (working set 一括移送)

現機(HP ノート i7-1065G7)から新機(arkhive GL-I7G59M / **RTX 5090 32GB / 128GB RAM /
Win11 Pro**)へ、working set を外付け SSD 経由で一括移送し、新機で **同一絶対パス**へ
push-button 復元するための PowerShell スクリプト群。

> **正本(必読)**
> - `D:\projects\fullsense\docs\research\gpu_pc_migration_plan_2026-06-28.md`
>   (§2 パス戦略 / §3 データ移行 / §5 検証 / §7 タイムライン)
> - `D:\projects\fullsense\docs\research\migration_manifest_2026-06-28.md`
>   (§1 working-set サイズ / §2 移行ディレクトリ / §5 secrets / §6 GPU 配線 / §7 bootstrap)

移行設計の核心は **「ドライブレター・絶対パスを温存する」**(plan §2)。tool-guard グローバル
hook・ccr・raptor・llcore が `C:\Users\puruy\...` と `D:\...` を絶対パスでハードコードしている
ため、新機でも同一パスを再現できればハードコード破損ゼロで動く。

---

## スクリプト一覧

| ファイル | 役割 | 実行マシン |
|---|---|---|
| `backup_working_set.ps1` | working set を外付けへ robocopy `/MIR` でミラー | **現機**(着荷前) |
| `restore_working_set.ps1` | 外付け → 新機の **同一絶対パス**へ復元 | **新機**(着荷後) |
| `migrate_secrets.ps1` | 秘密(API キー)を暗号化 zip で別経路移送 / 復元 | 現機(Bundle)→ 新機(Restore) |
| `verify_new_machine.ps1` | 移行後チェック(plan §5 の 7 項目を PASS/Fail/Skip 集計) | **新機**(復元後) |
| `gpu_smoke.py` | RTX 5090 / Blackwell sm_120 の最小 GPU smoke(verify から呼ばれる / 単体可) | 新機 |

すべて PowerShell 7(pwsh)/ UTF-8(BOM なし)/ 冪等。robocopy `/MIR` は差分のみ転送するので
再実行で増分同期になる。`.git` は除外しない(repo 履歴温存)。

### 外付け上のレイアウト(ドライブレター展開)

`backup` は絶対パスをドライブレター = フォルダ名に展開して保存し、`restore` が逆変換する:

```
<Dest>\C\Users\puruy\.claude
<Dest>\C\Users\puruy\.cache\huggingface
<Dest>\D\projects
<Dest>\D\tools\raptor
<Dest>\D\tools              (raptor サブツリーは除外 = 二重コピー回避)
<Dest>\D\docs
<Dest>\D\api-manager
<Dest>\_migration_logs\*.log   (backup のログ)
```

---

## ★秘密の扱い(最重要 / plan §5・manifest §5)

秘密は **外付けミラーに絶対に混ぜない**。別経路(暗号化 USB / パスワード zip)で運ぶ。

- `D:\api-keys.json` … backup の robocopy `/XF` で **全ジョブから除外**(そもそも `D:\` 直下で
  対象サブツリー外だが belt-and-suspenders で確実に除外)。
- `D:\tools\raptor\.claude\settings.local.json` … **平文 `ANTHROPIC_API_KEY` を含む**ため
  raptor ジョブの `/XF` で除外。`restore` でも除外し `/MIR` の purge から守る(順序非依存)。
- `C:\Users\puruy\.claude\settings.local.json` … 秘密を含まない(permissions + Stop hook のみ)
  ためミラーに **残す**。

上記 2 つの秘密は `migrate_secrets.ps1` が暗号化 zip にまとめて運ぶ。**移行を機に API キーの
ローテーション**(再発行 + `api-keys.json` 更新 + 旧キー失効)を推奨(平文露出の衛生)。

---

## 手順(plan §7 タイムラインに沿って)

### A. 着荷前(現機・ダウンタイム短縮のリハーサル)

1. 外付け 2TB NVMe SSD を接続(例 `E:`)。working set 合計 ~100GB+(+ `D:\docs`)。
2. **まず DryRun** で対象とサイズを確認(実コピーしない):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\backup_working_set.ps1 -Dest E:\raptor-migration -DryRun
   ```
3. 問題なければ実ミラー(初回はフル、以後は差分):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\backup_working_set.ps1 -Dest E:\raptor-migration
   ```
   - run 出力(`out\` / `.out\`)も含めたい場合のみ `-IncludeRunOutputs`。
   - 着荷直前に **もう一度** 同じコマンドを実行 → 差分だけ追いつき最新化。
4. 秘密を別経路でまとめる(7-Zip があれば AES-256 + ヘッダ暗号化):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\migrate_secrets.ps1 -Mode Bundle
   # 既定で Desktop\fullsense-secrets\fullsense-secrets-<時刻>.7z を作成(パスワード対話入力)
   ```
   - 出力 zip は **working set の外付けとは別の暗号化 USB** に置く(同ドライブに `_migration_logs`
     を検出すると安全のため中止 / 意図的なら `-Force`)。

### B. 着荷後 Day 1–2(新機セットアップ)

1. Win11 初期セットアップで **ユーザー名 `puruy`**(plan §2-1。違うと hook/memory パス破損)。
2. **2TB を C:+D: 分割**(ディスクの管理。例 C:800GB / D:1.1TB。plan §2-2A)。
3. NVIDIA driver **R570+**(Blackwell)→ `py -3.11` → `torch` **cu128** を導入。

### C. 着荷後 Day 3–5(復元 → 秘密 → 検証)

1. 外付けを新機に接続し、**同一絶対パス**へ復元(まず DryRun 推奨):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\restore_working_set.ps1 -Source E:\raptor-migration -DryRun
   pwsh -File D:\projects\fullsense\tools\migration\restore_working_set.ps1 -Source E:\raptor-migration
   ```
   - 実行前に **ユーザー名 puruy / C:・D: の存在**を fail-closed チェックする。
   - `/MIR` は復元先の余剰を削除する。新機がクリーンなら安全。確認を省くなら `-Force`。
2. 秘密を元パスへ配置(**verify の前に**):
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\migrate_secrets.ps1 -Mode Restore -Source <暗号化USB>\fullsense-secrets-<時刻>.7z
   # D:\api-keys.json と raptor settings.local.json を元の絶対パスへ復元(既存は -Force で上書き)
   ```
3. 移行後チェック:
   ```powershell
   pwsh -File D:\projects\fullsense\tools\migration\verify_new_machine.ps1
   # 現機(GPU 無し)でドライラン確認するなら GPU 項目を抜く: -SkipGpu
   ```

### D. Day 6–7

- trading 系(Alpaca paper)の二重起動回避を確認(plan §7 / manifest §4)。
- llcore の **device 配線**(`Trainer`/`TBPTTTrainer`/plateau experiment に `--device`、manifest §6)。
- 初手 GPU ワークロード = 本日プローブの GPU フル版。

---

## 各スクリプトの引数

### backup_working_set.ps1(現機)
| 引数 | 説明 |
|---|---|
| `-Dest <root>` | **必須**。外付けのミラー先ルート(例 `E:\raptor-migration`)。ドライブルートや対象内側は拒否。 |
| `-DryRun` / `-WhatIf` | robocopy `/L`(リスト表示のみ・コピーしない)。 |
| `-IncludeRunOutputs` | `out\` / `.out\` も含める(既定は除外し明示ログ)。 |

除外: `__pycache__ *.pyc .venv venv node_modules .mypy_cache .pytest_cache .ruff_cache *.tmp`
+ `api-keys.json`(全ジョブ)+ raptor `settings.local.json`。各ジョブのログは
`<Dest>\_migration_logs\<name>.log`。最後に対象ごとのコピー済バイト/失敗をサマリ表示。

### restore_working_set.ps1(新機)
| 引数 | 説明 |
|---|---|
| `-Source <root>` | **必須**。外付けのミラー元ルート(backup の `-Dest` と同じ)。 |
| `-DryRun` / `-WhatIf` | robocopy `/L`(リスト表示のみ)。 |
| `-IncludeRunOutputs` | `out\` / `.out\` も復元。 |
| `-Force` | `/MIR` purge の確認プロンプトを省略。 |

### migrate_secrets.ps1(現機 → 新機)
| 引数 | 説明 |
|---|---|
| `-Mode Bundle` | 既定。秘密を暗号化 zip にまとめる。 |
| `-Mode Restore` | zip を展開し元の絶対パスへ配置。 |
| `-Out <dir>` | Bundle の出力先(既定 `Desktop\fullsense-secrets`)。外付けミラーには置かない。 |
| `-Source <zip>` | Restore する `.7z` / `.zip`。 |
| `-Force` | Restore で既存上書き / Bundle で外付け警告を無視。 |

7-Zip が無い場合は `Compress-Archive`(**暗号化されない**)にフォールバックし、暗号化 USB を
使うよう警告する。導入推奨: `winget install 7zip.7zip`。

### verify_new_machine.ps1(新機 / read-only)
| 引数 | 説明 |
|---|---|
| `-LlcoreDir <path>` | llcore リポジトリ(既定 `D:\projects\llcore`)。 |
| `-SkipGpu` | GPU 系チェック(torch.cuda / gpu_smoke / llcore forward / plateau)を SKIP。 |

plan §5 の 7 項目(torch.cuda、capability (12,0)+小 GEMM、llcore golden 一致、plateau smoke、
tool-guard live、RAD corpus、ツール存在)を `✓ Pass / ✗ Fail / - Skip` で集計。Fail があれば
exit 1。破壊的操作・git・外部送信は一切しない。

### gpu_smoke.py(新機 / verify から呼ばれる・単体可)
`py -3.11 gpu_smoke.py`(`PYTHONUTF8=1` 前置推奨)。torch import → cuda → capability (12,0)
→ 小 GEMM → `nn.Linear.to('cuda')` を順に確認し 1 行 JSON を出力。終了コード契約:
**0**=全 PASS / **2**=cuda 不可(環境差 → verify は SKIP)/ **1**=実不具合。

---

## 安全注意(まとめ)

- robocopy `/MIR` は **ミラー**(復元先の余剰を削除)。`restore` を既存環境へ向けるときは注意。
- クロスマシン移行のため ACL は持ち込まない(`/COPY:DAT`)。junction はループ防止で除外(`/XJ`)。
- **秘密を外付けミラーに混ぜない**。`migrate_secrets.ps1` の暗号化 zip + 別 USB を使う。
- 日本語 Windows でも robocopy サマリを正しく集計できるようロケール非依存パーサを使用。
- これらは作成・構文検証済み。**外付け接続後**に DryRun → 実行の順で使うこと。
