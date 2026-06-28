#Requires -Version 7.0
<#
.SYNOPSIS
    現機の working set を外付けドライブへ robocopy /MIR でミラーする(GPU PC 移行 step 1)。

.DESCRIPTION
    正本: D:\projects\fullsense\docs\research\gpu_pc_migration_plan_2026-06-28.md (§2/§3/§7)
          D:\projects\fullsense\docs\research\migration_manifest_2026-06-28.md   (§1/§2/§5)

    現機(HP ノート)の working set を外付け NVMe SSD へ「ドライブレターを温存した
    レイアウト」でミラーする。新機では restore_working_set.ps1 が逆方向に展開して
    **同一絶対パス**を復元する(ハードコード破損ゼロ = plan §2 の最重要要件)。

    外付け上のレイアウト(ドライブレターをフォルダ名に展開):
        <Dest>\C\Users\puruy\.claude
        <Dest>\C\Users\puruy\.cache\huggingface
        <Dest>\D\projects
        <Dest>\D\tools\raptor
        <Dest>\D\tools            (raptor サブツリーは除外 = 二重コピー回避)
        <Dest>\D\docs
        <Dest>\D\api-manager

    ★秘密の扱い(plan §5 / manifest §5):
      - D:\api-keys.json は **絶対にミラーに含めない**(robocopy /XF で全ジョブから除外)。
        そもそも D:\ 直下にあり対象サブツリー外だが、念のため belt-and-suspenders で除外。
      - raptor の .claude\settings.local.json は **平文 ANTHROPIC_API_KEY を含む**ため
        ミラーから除外(full-path /XF)。秘密は migrate_secrets.ps1 の別経路で移送する。
      - global の C:\Users\puruy\.claude\settings.local.json は秘密を含まない
        (permissions + Stop hook のみ)ためミラーに残す。

    冪等: robocopy /MIR は差分のみ転送。再実行で増分同期。
    本スクリプトは ★外付けが無い現状では実行しないこと(作成・構文検証のみ)。

.PARAMETER Dest
    外付けドライブのミラー先ルート(必須)。例: E:\raptor-migration

.PARAMETER DryRun
    robocopy /L でリスト表示のみ(実コピーしない)。-WhatIf と同義。

.PARAMETER IncludeRunOutputs
    out\ / .out\ などの大きな run 出力ディレクトリも含める(既定は除外)。

.EXAMPLE
    pwsh -File .\backup_working_set.ps1 -Dest E:\raptor-migration -DryRun
    # まず DryRun で対象とサイズを確認

.EXAMPLE
    pwsh -File .\backup_working_set.ps1 -Dest E:\raptor-migration
    # 実ミラー(再実行で差分のみ)
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [Parameter(Mandatory = $true)]
    [string]$Dest,

    [switch]$DryRun,

    [switch]$IncludeRunOutputs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# -WhatIf もしくは -DryRun のとき robocopy を /L (list only) で走らせる
$ListOnly = $DryRun.IsPresent -or $WhatIfPreference

# ------------------------------------------------------------------ targets
# Src = 現機の絶対パス。ExtraXD/ExtraXF = このジョブ固有の追加除外(full-path 可)。
$Targets = @(
    [pscustomobject]@{ Name = 'claude-home'; Src = 'C:\Users\puruy\.claude';            ExtraXD = @(); ExtraXF = @() }
    [pscustomobject]@{ Name = 'hf-cache';    Src = 'C:\Users\puruy\.cache\huggingface'; ExtraXD = @(); ExtraXF = @() }
    [pscustomobject]@{ Name = 'projects';    Src = 'D:\projects';                       ExtraXD = @(); ExtraXF = @() }
    # raptor: 平文 API キーを含む settings.local.json をミラーから除外(別経路 = migrate_secrets)
    [pscustomobject]@{ Name = 'raptor';      Src = 'D:\tools\raptor';                   ExtraXD = @(); ExtraXF = @('D:\tools\raptor\.claude\settings.local.json') }
    # tools: raptor サブツリーは別ジョブで扱うため除外し二重コピー/MIR purge 事故を防ぐ
    [pscustomobject]@{ Name = 'tools';       Src = 'D:\tools';                          ExtraXD = @('D:\tools\raptor'); ExtraXF = @() }
    [pscustomobject]@{ Name = 'docs';        Src = 'D:\docs';                           ExtraXD = @(); ExtraXF = @() }
    [pscustomobject]@{ Name = 'api-manager'; Src = 'D:\api-manager';                    ExtraXD = @(); ExtraXF = @() }
)

# 共通除外(plan の要件どおり)。.git は残す(repo 履歴温存) = 除外しない。
$ExcludeDirs   = @('__pycache__', '.venv', 'venv', 'node_modules', '.mypy_cache', '.pytest_cache', '.ruff_cache')
$ExcludeFiles  = @('*.pyc', '*.tmp', 'api-keys.json')   # ★api-keys.json は全ジョブから除外
$RunOutputDirs = @('out', '.out')                       # -IncludeRunOutputs が無ければ除外

# ------------------------------------------------------------------ helpers

function Get-MirrorChildPath {
    # 絶対パス C:\Users\puruy\.claude -> <Root>\C\Users\puruy\.claude
    param([string]$Root, [string]$AbsPath)
    $full      = [System.IO.Path]::GetFullPath($AbsPath)
    $pathRoot  = [System.IO.Path]::GetPathRoot($full)        # "C:\"
    $driveLtr  = $pathRoot.Substring(0, 1)                   # "C"
    $relative  = $full.Substring($pathRoot.Length)           # "Users\puruy\.claude"
    return (Join-Path (Join-Path $Root $driveLtr) $relative)
}

function Get-RoboStatus {
    # robocopy 終了コード: 0-7=成功(ビットフラグ), 8+=失敗
    param([int]$Code)
    if ($Code -ge 8)      { return 'Failed' }
    elseif ($Code -eq 0)  { return 'No change' }
    else                  { return 'OK' }
}

function Get-RoboSummary {
    <#
        ロケール非依存パーサ。robocopy フッターの集計表は言語に依らず
        Dirs / Files / Bytes / Times の順に並ぶ。先頭 3 行(コロンの後に
        6 個の整数列)が Dirs, Files, Bytes に対応する(/BYTES 指定で整数)。
        Times 行は時刻書式(コロン入り)なので 6 整数パターンに一致しない。
    #>
    param([string]$LogPath)
    $result = [pscustomobject]@{ FilesCopied = [int64]0; FilesFailed = [int64]0; BytesCopied = [int64]0; BytesFailed = [int64]0 }
    if (-not (Test-Path -LiteralPath $LogPath)) { return $result }

    $rows = @()
    foreach ($ln in (Get-Content -LiteralPath $LogPath)) {
        if ($ln -match ':\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s+([\d,]+)\s*$') {
            $rows += , @($Matches[1..6] | ForEach-Object { [int64]($_ -replace ',', '') })
        }
    }
    # 期待順: rows[0]=Dirs, rows[1]=Files, rows[2]=Bytes。列順 = Total,Copied,Skipped,Mismatch,FAILED,Extras
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
    throw 'robocopy.exe が見つかりません(Windows 標準ツール)。Windows 環境で実行してください。'
}

# Dest のドライブが存在するか(fail-closed)
$destRoot = [System.IO.Path]::GetPathRoot([System.IO.Path]::GetFullPath($Dest))
if (-not (Test-Path -LiteralPath $destRoot)) {
    throw "Dest のドライブ '$destRoot' が存在しません。外付けドライブを接続し、正しいレターを指定してください。"
}

# 安全ガード: Dest がソース対象の内側を指していないか(再帰ミラー防止)
$destFull = [System.IO.Path]::GetFullPath($Dest).TrimEnd('\')
foreach ($t in $Targets) {
    $srcFull = [System.IO.Path]::GetFullPath($t.Src).TrimEnd('\')
    if ($destFull.StartsWith($srcFull, [System.StringComparison]::OrdinalIgnoreCase)) {
        throw "Dest '$destFull' がソース '$srcFull' の内側にあります。別ドライブ/別ルートを指定してください。"
    }
}
# 安全ガード: ドライブのルート(C:\ や D:\)を Dest にしない
if ($destFull -match '^[A-Za-z]:\\?$') {
    throw "Dest はドライブのルート '$destFull' にできません(例: E:\raptor-migration のようにサブフォルダを指定)。"
}

$LogDir = Join-Path $Dest '_migration_logs'
[System.IO.Directory]::CreateDirectory($LogDir) | Out-Null   # -WhatIf に影響されず常に作成

Write-Host ''
Write-Host '=== backup_working_set.ps1 (GPU PC 移行 step 1) ===' -ForegroundColor Cyan
Write-Host ("Dest             : {0}" -f $destFull)
Write-Host ("Mode             : {0}" -f ($(if ($ListOnly) { 'DryRun (/L list only — コピーしません)' } else { '実ミラー (/MIR)' })))
Write-Host ("IncludeRunOutputs: {0}" -f $IncludeRunOutputs.IsPresent)
if (-not $IncludeRunOutputs) {
    Write-Host ("除外(run 出力) : {0}  ← -IncludeRunOutputs で含められます" -f ($RunOutputDirs -join ', ')) -ForegroundColor Yellow
}
Write-Host ("除外(secret)   : D:\api-keys.json / raptor settings.local.json は別経路 = migrate_secrets.ps1") -ForegroundColor Yellow
Write-Host ("ログ             : {0}" -f $LogDir)
Write-Host ''

# ------------------------------------------------------------------ run

$report = @()

foreach ($t in $Targets) {
    $srcFull = [System.IO.Path]::GetFullPath($t.Src)

    if (-not (Test-Path -LiteralPath $srcFull)) {
        Write-Host ("[{0,-12}] SKIP — ソースが存在しません: {1}" -f $t.Name, $srcFull) -ForegroundColor DarkYellow
        $report += [pscustomobject]@{ Target = $t.Name; Status = 'Skipped (no source)'; ExitCode = ''; FilesCopied = ''; BytesCopied = ''; Failed = '' }
        continue
    }

    $dstFull = Get-MirrorChildPath -Root $destFull -AbsPath $srcFull
    $log     = Join-Path $LogDir ("{0}.log" -f $t.Name)

    # 除外リスト構築
    $xd = @() + $ExcludeDirs + $t.ExtraXD
    if (-not $IncludeRunOutputs) { $xd += $RunOutputDirs }
    $xf = @() + $ExcludeFiles + $t.ExtraXF

    # robocopy オプション(クロスマシン移行なので /COPY:DAT = ACL は持ち込まない)
    $opts = @('/MIR', '/MT:16', '/R:2', '/W:5', '/XJ', '/BYTES', '/NP', '/NFL', '/NDL', '/COPY:DAT', '/DCOPY:DAT', '/TEE')
    if ($ListOnly) { $opts += '/L' }

    $argList = @($srcFull, $dstFull) + $opts
    $argList += '/XD'; $argList += $xd
    $argList += '/XF'; $argList += $xf
    $argList += "/LOG:$log"

    Write-Host ("[{0,-12}] {1}" -f $t.Name, $srcFull) -ForegroundColor Green
    Write-Host ("            -> {0}" -f $dstFull) -ForegroundColor DarkGray
    if ($t.ExtraXF.Count -gt 0) { Write-Host ("            (除外ファイル: {0})" -f ($t.ExtraXF -join '; ')) -ForegroundColor DarkYellow }
    if ($t.ExtraXD.Count -gt 0) { Write-Host ("            (除外ディレクトリ: {0})" -f ($t.ExtraXD -join '; ')) -ForegroundColor DarkYellow }

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
Write-Host '=== 実行サマリ ===' -ForegroundColor Cyan
$report | Format-Table -AutoSize

$anyFail = $report | Where-Object { $_.ExitCode -is [int] -and $_.ExitCode -ge 8 }
if ($anyFail) {
    Write-Host '一部ジョブが失敗しました(exit >= 8)。上記のログを確認してください。' -ForegroundColor Red
    exit 1
}

if ($ListOnly) {
    Write-Host 'DryRun 完了(実コピーなし)。問題なければ -DryRun を外して実ミラーしてください。' -ForegroundColor Yellow
} else {
    Write-Host '★秘密(api-keys.json / raptor settings.local.json)はこのミラーに含まれていません。' -ForegroundColor Yellow
    Write-Host '  別途 migrate_secrets.ps1 で暗号化 USB 等の別経路を使ってください。' -ForegroundColor Yellow
    Write-Host 'バックアップ完了。新機では restore_working_set.ps1 で同一絶対パスへ展開します。' -ForegroundColor Green
}
exit 0
