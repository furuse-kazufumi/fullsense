#Requires -Version 7.0
<#
.SYNOPSIS
    新機(RTX 5090 / 128GB / Win11 Pro)で staging(D:\_c_migration)から
    **C: 常駐の working set** を同一絶対パスへ復元する(GPU PC 移行 step 2)。

.DESCRIPTION
    正本: gpu_pc_migration_plan_2026-06-28.md §2(パス戦略)/ §7(タイムライン)
          migration_manifest_2026-06-28.md §2 / §7
          migration_change_spec.md §0(VERIFIED FACTS)/ §2-4

    ★新前提(物理移送):
      D: は外付け SSD 本体(SanDisk Extreme 55AE / exFAT / 平文 / USB)を新機へ
      物理接続しレター D: を温存する。よって D:\projects / D:\tools\raptor / D:\docs
      などは「travels(移送不要)」であり、本スクリプトは **復元しない**。
      本スクリプトが運ぶのは backup_working_set.ps1 が D:\_c_migration\ へ staging した
      **C: 常駐分のみ**(.claude / .claude.json / .codex / browser-use live state /
      .gitconfig / gh hosts / PowerShell profile / .config / hf-cache / ollama)。

    backup_working_set.ps1 が staging に作ったレイアウト
        <Source>\C\Users\puruy\.claude          (ディレクトリ)
        <Source>\C\Users\puruy\.claude.json      (単一ファイル)
        <Source>\reference\user_path.txt         (User PATH)
        <Source>\reference\user_env_nonsecret.txt(secret 3 キーを除く User env)
        <Source>\reference\scheduled_tasks\*.xml (Export-ScheduledTask)
    を逆方向に robocopy で復元し、新機 C: に同じ絶対パスを再現する。
    $Targets は backup_working_set.ps1 と **完全一致**(name → C: 宛先)。

    ★前提チェック(fail-closed):
      - 実行ユーザーが 'puruy' でない場合は **throw**(警告から格上げ)。
        ユーザー名が違うと hook/memory/.claude.json/gh パスが破損する(plan §2-1)。
      - D:\ ボリュームが無い場合は中止。さらに **sentinel(D:\tools\raptor 存在)**で
        「D: が本物の作業ディスクか」を確認する。別ボリュームが D: に化けている状態で
        走らせると誤った staging を掴む / 旧設計では /MIR purge 事故の温床になるため
        fail-closed で止める(spec §2-4 / §0)。

    ★秘密は別経路: .codex\auth.json / .claude\.credentials.json / .ssh / User env の
      3 secret はこのミラーに **含まれない**(平文 staging しない)。復元後に
      migrate_secrets.ps1 -Mode Restore で配置し、env3キーは setx か再発行する。
      .credentials.json は端末紐づきのため **新機は claude 再ログイン前提**。
      D:\api-keys.json と raptor settings.local.json は D: 上(travels)で別送不要。

    ★復元後ステップ(-SkipReferenceApply で省略可):
      - reference\user_path.txt / user_env_nonsecret.txt を setx で再適用(secret 除外)。
      - reference\scheduled_tasks\*.xml を Register-ScheduledTask -Xml で再登録。
        ただし action は旧機 C: 依存(C:\Python314\python.exe / C:\Users\puruy\raptor\...)
        のままなので、D:\tools\raptor\libexec + py -3.11 へ **手修正が必要**と注記する
        (VERIFIED FACTS / manifest §4)。

    冪等: robocopy /MIR は差分のみ。単一ファイルは差分コピー。再実行で増分同期。

.PARAMETER Source
    staging のルート。backup の -Dest と同じ。既定 D:\_c_migration。

.PARAMETER DryRun
    robocopy /L でリスト表示のみ(実コピーしない)。setx / タスク登録もシミュレートのみ。
    -WhatIf と同義。

.PARAMETER IncludeRunOutputs
    out\ / .out\ も復元する(既定は除外。backup 側で含めていなければ意味なし)。

.PARAMETER Force
    /MIR は復元先(C: ディレクトリ)の余剰ファイルを削除(purge)する。
    新機がクリーンでない場合の確認を省略する。

.PARAMETER SkipReferenceApply
    復元後の reference 適用(PATH/env setx + scheduled task 登録)を行わない。

.EXAMPLE
    pwsh -File .\restore_working_set.ps1 -DryRun

.EXAMPLE
    pwsh -File .\restore_working_set.ps1 -Source D:\_c_migration
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $false)]
    [string]$Source = 'D:\_c_migration',

    [switch]$DryRun,

    [switch]$IncludeRunOutputs,

    [switch]$Force,

    [switch]$SkipReferenceApply
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ListOnly = $DryRun.IsPresent -or $WhatIfPreference

# ------------------------------------------------------------------ targets
# backup_working_set.ps1 と同一の対象表(Dst = 復元先の絶対パス)。
# すべて C: 常駐・非 secret。secret(.credentials.json / .codex\auth.json)は
# ExtraXF で除外し、migrate_secrets.ps1 -Mode Restore で別配置する。
# IsFile = $true は単一ファイル(/MIR を使わずファイル 1 個だけコピー)。
$Targets = @(
    [pscustomobject]@{ Name = 'claude-home'; Dst = 'C:\Users\puruy\.claude';                  IsFile = $false; ExtraXD = @();             ExtraXF = @('C:\Users\puruy\.claude\.credentials.json') }
    [pscustomobject]@{ Name = 'claude-json'; Dst = 'C:\Users\puruy\.claude.json';              IsFile = $true;  ExtraXD = @();             ExtraXF = @() }
    [pscustomobject]@{ Name = 'codex';       Dst = 'C:\Users\puruy\.codex';                    IsFile = $false; ExtraXD = @('tmp', 'logs'); ExtraXF = @('C:\Users\puruy\.codex\auth.json') }
    [pscustomobject]@{ Name = 'browser-use'; Dst = 'C:\Users\puruy\browser-use-project';       IsFile = $false; ExtraXD = @();             ExtraXF = @() }
    [pscustomobject]@{ Name = 'gitconfig';   Dst = 'C:\Users\puruy\.gitconfig';                IsFile = $true;  ExtraXD = @();             ExtraXF = @() }
    [pscustomobject]@{ Name = 'gh-hosts';    Dst = 'C:\Users\puruy\AppData\Roaming\GitHub CLI'; IsFile = $false; ExtraXD = @();            ExtraXF = @() }
    [pscustomobject]@{ Name = 'ps-profile';  Dst = 'C:\Users\puruy\Documents\PowerShell';      IsFile = $false; ExtraXD = @();             ExtraXF = @() }
    [pscustomobject]@{ Name = 'config';      Dst = 'C:\Users\puruy\.config';                   IsFile = $false; ExtraXD = @();             ExtraXF = @() }
    [pscustomobject]@{ Name = 'hf-cache';    Dst = 'C:\Users\puruy\.cache\huggingface';        IsFile = $false; ExtraXD = @();             ExtraXF = @() }
    [pscustomobject]@{ Name = 'ollama';      Dst = 'C:\Users\puruy\.ollama\models';            IsFile = $false; ExtraXD = @();             ExtraXF = @() }
)

$ExcludeDirs   = @('__pycache__', '.venv', 'venv', 'node_modules', '.mypy_cache', '.pytest_cache', '.ruff_cache')
# api-keys.json は C: には来ない(D: travels)が、防御的に常時除外(secret を C: へ書かない)。
$ExcludeFiles  = @('*.pyc', '*.tmp', 'api-keys.json')
$RunOutputDirs = @('out', '.out')

# 復元後に setx 再適用しない secret env 名(平文 staging されない / 別経路)。
$SecretEnvNames = @('ANTHROPIC_API_KEY', 'TELEGRAM_BOT_TOKEN', 'SOCIALDATA_API_KEY')

# ------------------------------------------------------------------ helpers

function Get-MirrorChildPath {
    param([string]$Root, [string]$AbsPath)
    $full     = [System.IO.Path]::GetFullPath($AbsPath)
    $pathRoot = [System.IO.Path]::GetPathRoot($full)
    $driveLtr = $pathRoot.Substring(0, 1)
    $relative = $full.Substring($pathRoot.Length)
    return (Join-Path (Join-Path $Root $driveLtr) $relative)
}

function Get-RoboStatus {
    param([int]$Code)
    if ($Code -ge 8)     { return 'Failed' }
    elseif ($Code -eq 0) { return 'No change' }
    else                 { return 'OK' }
}

function Get-RoboSummary {
    param([string]$LogPath)
    $result = [pscustomobject]@{ FilesCopied = [int64]0; FilesFailed = [int64]0; BytesCopied = [int64]0; BytesFailed = [int64]0 }
    if (-not (Test-Path -LiteralPath $LogPath)) { return $result }
    $rows = @()
    foreach ($ln in (Get-Content -LiteralPath $LogPath)) {
        if ($ln -match ':\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s*$') {
            $rows += , @($Matches[1..6] | ForEach-Object { [int64]($_ -replace ',', '') })
        }
    }
    if ($rows.Count -ge 2) { $result.FilesCopied = $rows[1][1]; $result.FilesFailed = $rows[1][4] }
    if ($rows.Count -ge 3) { $result.BytesCopied = $rows[2][1]; $result.BytesFailed = $rows[2][4] }
    return $result
}

function Format-Bytes {
    param([int64]$Bytes)
    if ($Bytes -lt 1KB) { return "$Bytes B" }
    $units = 'KB', 'MB', 'GB', 'TB'
    $val = [double]$Bytes
    foreach ($u in $units) {
        $val /= 1024.0
        if ($val -lt 1024.0) { return ('{0:N2} {1}' -f $val, $u) }
    }
    return ('{0:N2} PB' -f ($val / 1024.0))
}

function Invoke-ReferenceApply {
    <#
        reference\ 退避物を新機へ再適用する。
          - user_path.txt           : User PATH を setx(1024 文字超は SetEnvironmentVariable)。
          - user_env_nonsecret.txt  : NAME=VALUE 行を setx(secret / PATH は skip)。
          - scheduled_tasks\*.xml   : Register-ScheduledTask -Xml(action の C: 依存は要手修正)。
        ListOnly のときは実行せず内容のみ表示する。
    #>
    param(
        [Parameter(Mandatory = $true)][string]$ReferenceRoot,
        [string[]]$SecretEnvNames = @(),
        [switch]$ListOnly
    )

    Write-Host ''
    Write-Host '=== reference 再適用 (PATH / env / scheduled tasks) ===' -ForegroundColor Cyan

    if (-not (Test-Path -LiteralPath $ReferenceRoot)) {
        Write-Host ("reference ディレクトリがありません: {0}(backup 側で export 済みか確認)" -f $ReferenceRoot) -ForegroundColor DarkYellow
        return
    }

    # --- User PATH ---
    $pathFile = Join-Path $ReferenceRoot 'user_path.txt'
    if (Test-Path -LiteralPath $pathFile) {
        $pathVal = (Get-Content -LiteralPath $pathFile -Raw).Trim()
        if ($pathVal) {
            if ($ListOnly) {
                Write-Host ("[reference] (DryRun) User PATH を再適用予定 ({0} 文字)" -f $pathVal.Length)
            }
            elseif ($pathVal.Length -gt 1024) {
                # setx は 1024 文字で切り詰める → SetEnvironmentVariable で適用。
                [Environment]::SetEnvironmentVariable('Path', $pathVal, 'User')
                Write-Host ("[reference] User PATH を SetEnvironmentVariable で再適用 ({0} 文字 / setx 1024 制限回避)" -f $pathVal.Length) -ForegroundColor Green
            }
            else {
                & setx PATH $pathVal | Out-Null
                Write-Host '[reference] User PATH を setx で再適用' -ForegroundColor Green
            }
        }
    }
    else {
        Write-Host '[reference] user_path.txt なし — PATH 再適用 skip' -ForegroundColor DarkYellow
    }

    # --- User env (non-secret) ---
    $envFile = Join-Path $ReferenceRoot 'user_env_nonsecret.txt'
    if (Test-Path -LiteralPath $envFile) {
        foreach ($ln in (Get-Content -LiteralPath $envFile)) {
            $line = $ln.Trim()
            if (-not $line -or $line.StartsWith('#')) { continue }
            $idx = $line.IndexOf('=')
            if ($idx -lt 1) { continue }
            $name  = $line.Substring(0, $idx).Trim()
            $value = $line.Substring($idx + 1)
            if (($name -in $SecretEnvNames) -or ($name -ieq 'Path')) {
                Write-Host ("[reference] env '{0}' は secret/PATH のため skip" -f $name) -ForegroundColor DarkYellow
                continue
            }
            if ($ListOnly) {
                Write-Host ("[reference] (DryRun) setx {0} ..." -f $name)
            }
            else {
                & setx $name $value | Out-Null
                Write-Host ("[reference] setx {0} 適用" -f $name) -ForegroundColor Green
            }
        }
    }
    else {
        Write-Host '[reference] user_env_nonsecret.txt なし — env 再適用 skip' -ForegroundColor DarkYellow
    }

    # --- Scheduled tasks ---
    $taskDir = Join-Path $ReferenceRoot 'scheduled_tasks'
    if (Test-Path -LiteralPath $taskDir) {
        $xmls = @(Get-ChildItem -LiteralPath $taskDir -Filter '*.xml' -File -ErrorAction SilentlyContinue)
        foreach ($x in $xmls) {
            $taskName = [System.IO.Path]::GetFileNameWithoutExtension($x.Name)
            if ($ListOnly) {
                Write-Host ("[reference] (DryRun) Register-ScheduledTask {0}" -f $taskName)
                continue
            }
            try {
                $xmlText = Get-Content -LiteralPath $x.FullName -Raw
                Register-ScheduledTask -Xml $xmlText -TaskName $taskName -Force -ErrorAction Stop | Out-Null
                Write-Host ("[reference] ScheduledTask 登録: {0}" -f $taskName) -ForegroundColor Green
            }
            catch {
                # 管理者権限不足 / action パス不正などで失敗し得る。致命にせず警告に留める。
                Write-Host ("[reference] ScheduledTask 登録失敗: {0} — {1}" -f $taskName, $_.Exception.Message) -ForegroundColor Yellow
            }
        }
        if ($xmls.Count -gt 0) {
            Write-Host '  注記: 登録した task の action は旧機 C: 依存のまま(C:\Python314\python.exe /' -ForegroundColor Yellow
            Write-Host '        C:\Users\puruy\raptor\... は新機に存在しない)。D:\tools\raptor\libexec +' -ForegroundColor Yellow
            Write-Host '        py -3.11 へ手修正が必要(VERIFIED FACTS / manifest §4)。' -ForegroundColor Yellow
            Write-Host '        ClaudeCodeUpdate は Ready のまま要判断。' -ForegroundColor Yellow
        }
    }
    else {
        Write-Host '[reference] scheduled_tasks\ なし — タスク登録 skip' -ForegroundColor DarkYellow
    }
}

# ------------------------------------------------------------------ pre-flight

if (-not (Get-Command robocopy.exe -ErrorAction SilentlyContinue)) {
    throw 'robocopy.exe が見つかりません(Windows 標準ツール)。'
}

$srcRoot = [System.IO.Path]::GetFullPath($Source).TrimEnd('\')
if (-not (Test-Path -LiteralPath $srcRoot)) {
    throw "Source '$srcRoot' が存在しません。staging(D:\_c_migration)を作成済みか、正しいルートを指定してください。"
}

# plan §2-1: Windows ユーザー名 puruy の確認 → fail-closed(throw)。
# 違うと .claude / .claude.json / gh / memory のハードコードパスが破損する。
if ($env:USERNAME -ne 'puruy') {
    throw ("実行ユーザーが '{0}' です。本スクリプトはユーザー名 'puruy' を要求します(違うと hook/memory/.claude.json/gh パスが破損 — plan §2-1)。ローカルアカウント 'puruy' で OOBE してから再実行してください。" -f $env:USERNAME)
}
if (-not (Test-Path -LiteralPath 'C:\Users\puruy')) {
    Write-Host '警告: C:\Users\puruy が存在しません。復元先プロファイルが無いとパスが破損します(plan §2-1)。' -ForegroundColor Red
}

# plan §2-2 / spec §2-4: D:\ ボリュームの確認(外付け本体 = travels が接続済みか)。
if (-not (Test-Path -LiteralPath 'D:\')) {
    throw 'D:\ ボリュームが存在しません。外付け SSD(本体 = travels)を接続しレター D: を固定してから再実行してください(plan §2-2)。'
}
# sentinel: D: が「本物の作業ディスク」かを確認する。別ボリュームが D: に割り当てられた
# 状態では誤った staging を掴んだり /MIR purge 事故の温床になるため fail-closed で止める。
if (-not (Test-Path -LiteralPath 'D:\tools\raptor')) {
    throw 'D:\ は存在しますが sentinel(D:\tools\raptor)が見つかりません。別ボリュームが D: に化けている可能性があります。正しい外付け SSD をレター D: に固定(§2-2)してから再実行してください(spec §2-4 / §0)。'
}

$LogDir = Join-Path $srcRoot '_restore_logs'
[System.IO.Directory]::CreateDirectory($LogDir) | Out-Null

Write-Host ''
Write-Host '=== restore_working_set.ps1 (GPU PC 移行 step 2 / C: 常駐分の復元) ===' -ForegroundColor Cyan
Write-Host ("Source           : {0}" -f $srcRoot)
Write-Host ("User             : {0}" -f $env:USERNAME)
Write-Host ("Mode             : {0}" -f ($(if ($ListOnly) { 'DryRun (/L list only — 復元しません)' } else { '実復元 (/MIR)' })))
Write-Host ("IncludeRunOutputs: {0}" -f $IncludeRunOutputs.IsPresent)
Write-Host ("ReferenceApply   : {0}" -f ($(if ($SkipReferenceApply) { 'skip' } else { '有効 (PATH/env/tasks)' })))
Write-Host ''

# /MIR は復元先(C: ディレクトリ)の余剰を削除する。新機がクリーンでなければ確認(-Force でスキップ)。
if (-not $ListOnly -and -not $Force) {
    Write-Host '注意: robocopy /MIR は復元先(C: の各ディレクトリ)の「staging に無いファイル」を削除します。' -ForegroundColor Yellow
    Write-Host '      新機がクリーンな前提なら安全です。続行しますか? (-Force で本確認を省略)' -ForegroundColor Yellow
    $ans = Read-Host '続行する場合は y を入力'
    if ($ans -ne 'y') { Write-Host '中止しました。'; exit 0 }
}

# ------------------------------------------------------------------ run

$report = @()

foreach ($t in $Targets) {
    $dstFull = [System.IO.Path]::GetFullPath($t.Dst)
    $srcFull = Get-MirrorChildPath -Root $srcRoot -AbsPath $dstFull
    $log     = Join-Path $LogDir ("{0}.log" -f $t.Name)

    if (-not (Test-Path -LiteralPath $srcFull)) {
        Write-Host ("[{0,-12}] SKIP — staging にデータがありません: {1}" -f $t.Name, $srcFull) -ForegroundColor DarkYellow
        $report += [pscustomobject]@{ Target = $t.Name; Status = 'Skipped (no source)'; ExitCode = ''; FilesCopied = ''; BytesCopied = ''; Failed = '' }
        continue
    }

    if ($t.IsFile) {
        # 単一ファイル: /MIR を使わない(親ディレクトリを purge してしまうため)。
        # robocopy <srcDir> <dstDir> <fileName> でファイル 1 個だけコピーする。
        $srcDir   = [System.IO.Path]::GetDirectoryName($srcFull)
        $dstDir   = [System.IO.Path]::GetDirectoryName($dstFull)
        $fileName = [System.IO.Path]::GetFileName($srcFull)

        $opts = @('/R:2', '/W:5', '/BYTES', '/NP', '/NFL', '/NDL', '/COPY:DAT', '/TEE')
        if ($ListOnly) { $opts += '/L' }

        $argList = @($srcDir, $dstDir, $fileName) + $opts
        $argList += "/LOG:$log"

        Write-Host ("[{0,-12}] {1}  (単一ファイル)" -f $t.Name, $srcFull) -ForegroundColor Green
        Write-Host ("            -> {0}" -f $dstFull) -ForegroundColor DarkGray
    }
    else {
        $xd = @() + $ExcludeDirs + $t.ExtraXD
        if (-not $IncludeRunOutputs) { $xd += $RunOutputDirs }
        $xf = @() + $ExcludeFiles + $t.ExtraXF

        $opts = @('/MIR', '/MT:16', '/R:2', '/W:5', '/XJ', '/BYTES', '/NP', '/NFL', '/NDL', '/COPY:DAT', '/DCOPY:DAT', '/TEE')
        if ($ListOnly) { $opts += '/L' }

        $argList = @($srcFull, $dstFull) + $opts
        $argList += '/XD'; $argList += $xd
        $argList += '/XF'; $argList += $xf
        $argList += "/LOG:$log"

        Write-Host ("[{0,-12}] {1}" -f $t.Name, $srcFull) -ForegroundColor Green
        Write-Host ("            -> {0}" -f $dstFull) -ForegroundColor DarkGray
    }

    & robocopy.exe @argList
    $code = $LASTEXITCODE
    $stat = Get-RoboStatus -Code $code
    $sum  = Get-RoboSummary -LogPath $log

    if ($code -ge 8) {
        Write-Host ("            !! robocopy 失敗 (exit {0}) — ログ確認: {1}" -f $code, $log) -ForegroundColor Red
    }

    $report += [pscustomobject]@{
        Target      = $t.Name
        Status      = $stat
        ExitCode    = $code
        FilesCopied = $sum.FilesCopied
        BytesCopied = (Format-Bytes -Bytes $sum.BytesCopied)
        Failed      = ('{0} files / {1}' -f $sum.FilesFailed, (Format-Bytes -Bytes $sum.BytesFailed))
    }
}

# ------------------------------------------------------------------ summary

Write-Host ''
Write-Host '=== 復元サマリ ===' -ForegroundColor Cyan
$report | Format-Table -AutoSize

# ------------------------------------------------------------------ reference apply

if (-not $SkipReferenceApply) {
    $referenceRoot = Join-Path $srcRoot 'reference'
    Invoke-ReferenceApply -ReferenceRoot $referenceRoot -SecretEnvNames $SecretEnvNames -ListOnly:$ListOnly
}

# ------------------------------------------------------------------ exit

$anyFail = $report | Where-Object { $_.ExitCode -is [int] -and $_.ExitCode -ge 8 }
if ($anyFail) {
    Write-Host ''
    Write-Host '一部ジョブが失敗しました(exit >= 8)。上記のログを確認してください。' -ForegroundColor Red
    exit 1
}

if ($ListOnly) {
    Write-Host ''
    Write-Host 'DryRun 完了(実復元なし)。' -ForegroundColor Yellow
} else {
    Write-Host ''
    Write-Host 'C: 常駐分を同一絶対パスへ展開完了。次の手順:' -ForegroundColor Green
    Write-Host '  1) migrate_secrets.ps1 -Mode Restore で secret 配置 + env3キー setx/再発行' -ForegroundColor Yellow
    Write-Host '  2) .credentials.json は端末紐づき → 新機で claude 再ログイン' -ForegroundColor Yellow
    Write-Host '  3) 登録 scheduled task の action(C: 依存)を D:\tools\raptor + py -3.11 へ手修正' -ForegroundColor Yellow
    Write-Host '  4) verify_new_machine.ps1 で移行後チェック(Check0 = D: レター/健全性)' -ForegroundColor Yellow
}
exit 0
