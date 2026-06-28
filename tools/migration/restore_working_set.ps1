#Requires -Version 7.0
<#
.SYNOPSIS
    新機(RTX 5090 / 128GB / Win11 Pro)で外付けドライブから working set を
    **同一絶対パス**へ復元する(GPU PC 移行 step 2)。

.DESCRIPTION
    正本: gpu_pc_migration_plan_2026-06-28.md §2(パス戦略)/ §7(タイムライン)
          migration_manifest_2026-06-28.md §2 / §7

    backup_working_set.ps1 が外付けに作ったレイアウト
        <Source>\C\Users\puruy\.claude  等
    を逆方向に robocopy /MIR で復元し、現機と同じ絶対パスを再現する。
    plan §2 の前提どおり C: と D: が揃っていること(Win ユーザー名 = puruy、
    2TB を C:+D: 分割)を確認してから実行する。

    ★前提チェック(fail-closed):
      - 実行ユーザーが 'puruy' でない場合、または C:\Users\puruy が無い場合は警告。
        ユーザー名が違うと hook/memory パスが破損する(plan §2-1)。
      - D:\ ボリュームが無い場合は中止(D:\ ハードコード多数 = plan §2-2)。

    ★秘密は別経路: api-keys.json / raptor settings.local.json はこのミラーに
    含まれない。復元後に migrate_secrets.ps1 -Mode Restore で配置する。
    /MIR の purge から守るため、これらは復元ジョブでも除外する(順序非依存)。

    冪等: robocopy /MIR は差分のみ。再実行で増分同期。

.PARAMETER Source
    外付けドライブのミラー元ルート(必須)。backup の -Dest と同じ。例: E:\raptor-migration

.PARAMETER DryRun
    robocopy /L でリスト表示のみ(実コピーしない)。-WhatIf と同義。

.PARAMETER IncludeRunOutputs
    out\ / .out\ も復元する(既定は除外。backup 側で含めていなければ意味なし)。

.PARAMETER Force
    /MIR は復元先の余剰ファイルを削除(purge)する。新機が空でない場合の確認を省略する。

.EXAMPLE
    pwsh -File .\restore_working_set.ps1 -Source E:\raptor-migration -DryRun

.EXAMPLE
    pwsh -File .\restore_working_set.ps1 -Source E:\raptor-migration
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [switch]$DryRun,

    [switch]$IncludeRunOutputs,

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$ListOnly = $DryRun.IsPresent -or $WhatIfPreference

# ------------------------------------------------------------------ targets
# backup_working_set.ps1 と同一の対象表(Src = 復元先の絶対パス)。
$Targets = @(
    [pscustomobject]@{ Name = 'claude-home'; Dst = 'C:\Users\puruy\.claude';            ExtraXD = @(); ExtraXF = @() }
    [pscustomobject]@{ Name = 'hf-cache';    Dst = 'C:\Users\puruy\.cache\huggingface'; ExtraXD = @(); ExtraXF = @() }
    [pscustomobject]@{ Name = 'projects';    Dst = 'D:\projects';                       ExtraXD = @(); ExtraXF = @() }
    [pscustomobject]@{ Name = 'raptor';      Dst = 'D:\tools\raptor';                   ExtraXD = @(); ExtraXF = @('D:\tools\raptor\.claude\settings.local.json') }
    [pscustomobject]@{ Name = 'tools';       Dst = 'D:\tools';                          ExtraXD = @('D:\tools\raptor'); ExtraXF = @() }
    [pscustomobject]@{ Name = 'docs';        Dst = 'D:\docs';                           ExtraXD = @(); ExtraXF = @() }
    [pscustomobject]@{ Name = 'api-manager'; Dst = 'D:\api-manager';                    ExtraXD = @(); ExtraXF = @() }
)

$ExcludeDirs   = @('__pycache__', '.venv', 'venv', 'node_modules', '.mypy_cache', '.pytest_cache', '.ruff_cache')
$ExcludeFiles  = @('*.pyc', '*.tmp', 'api-keys.json')
$RunOutputDirs = @('out', '.out')

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

# ------------------------------------------------------------------ pre-flight

if (-not (Get-Command robocopy.exe -ErrorAction SilentlyContinue)) {
    throw 'robocopy.exe が見つかりません(Windows 標準ツール)。'
}

$srcRoot = [System.IO.Path]::GetFullPath($Source).TrimEnd('\')
if (-not (Test-Path -LiteralPath $srcRoot)) {
    throw "Source '$srcRoot' が存在しません。外付けドライブを接続し、正しいルートを指定してください。"
}

# plan §2-1: Windows ユーザー名 puruy の確認(違うと hook/memory パス破損)
if ($env:USERNAME -ne 'puruy') {
    Write-Host ("警告: 現在のユーザー名は '{0}' です。plan §2-1 はユーザー名 'puruy' を要求します。" -f $env:USERNAME) -ForegroundColor Red
    Write-Host '      C:\Users\puruy\.claude 配下の hook/memory パスが破損する可能性があります。' -ForegroundColor Red
}
if (-not (Test-Path -LiteralPath 'C:\Users\puruy')) {
    Write-Host '警告: C:\Users\puruy が存在しません。グローバル hook/memory パスが破損します(plan §2-1)。' -ForegroundColor Red
}
# plan §2-2: D:\ ボリュームの確認(D:\ ハードコード多数 → 無いと破損)
if (-not (Test-Path -LiteralPath 'D:\')) {
    throw 'D:\ ボリュームが存在しません。plan §2-2 に従い 2TB を C:+D: 分割してから再実行してください。'
}

$LogDir = Join-Path $Source '_restore_logs'
[System.IO.Directory]::CreateDirectory($LogDir) | Out-Null

Write-Host ''
Write-Host '=== restore_working_set.ps1 (GPU PC 移行 step 2) ===' -ForegroundColor Cyan
Write-Host ("Source           : {0}" -f $srcRoot)
Write-Host ("User             : {0}" -f $env:USERNAME)
Write-Host ("Mode             : {0}" -f ($(if ($ListOnly) { 'DryRun (/L list only — 復元しません)' } else { '実復元 (/MIR)' })))
Write-Host ("IncludeRunOutputs: {0}" -f $IncludeRunOutputs.IsPresent)
Write-Host ''

# /MIR は復元先の余剰を削除する。新機が空でない場合は確認(-Force でスキップ)。
if (-not $ListOnly -and -not $Force) {
    Write-Host '注意: robocopy /MIR は復元先の「ミラー元に無いファイル」を削除します。' -ForegroundColor Yellow
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
        Write-Host ("[{0,-12}] SKIP — 外付けにデータがありません: {1}" -f $t.Name, $srcFull) -ForegroundColor DarkYellow
        $report += [pscustomobject]@{ Target = $t.Name; Status = 'Skipped (no source)'; ExitCode = ''; FilesCopied = ''; BytesCopied = ''; Failed = '' }
        continue
    }

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

$anyFail = $report | Where-Object { $_.ExitCode -is [int] -and $_.ExitCode -ge 8 }
if ($anyFail) {
    Write-Host '一部ジョブが失敗しました(exit >= 8)。上記のログを確認してください。' -ForegroundColor Red
    exit 1
}

if ($ListOnly) {
    Write-Host 'DryRun 完了(実復元なし)。' -ForegroundColor Yellow
} else {
    Write-Host ''
    Write-Host '同一絶対パスへ展開完了。次は verify_new_machine.ps1 で移行後チェックを実行してください。' -ForegroundColor Green
    Write-Host '(秘密の配置は migrate_secrets.ps1 -Mode Restore を verify の前に実行)' -ForegroundColor Yellow
}
exit 0
