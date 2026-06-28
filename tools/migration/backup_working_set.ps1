#Requires -Version 7.0
<#
.SYNOPSIS
    現機の C: 常駐 working set を C: 常駐 staging ルート(既定 D:\_c_migration)へ
    robocopy で staging する(GPU PC 移行・物理移送前提の step 1)。

.DESCRIPTION
    正本: D:\projects\fullsense\docs\research\gpu_pc_migration_plan_2026-06-28.md (§2/§3/§7)
          D:\projects\fullsense\docs\research\migration_manifest_2026-06-28.md   (§1/§2/§5)

    ★新前提(2026-06-28 実機一次検証で確定):
      - D: は外付け SSD 本体(SanDisk Extreme 55AE / exFAT / 平文 / BusType=USB)。
        新機へ **物理接続してレター D: を温存** する = D:\ 配下(projects/raptor/tools/
        docs/api-manager 等)は「ドライブごと travels」= robocopy 不要。
      - したがって本スクリプトは **D: をミラーしない**。新機セットアップで取りこぼす
        のは「C: 常駐分」だけなので、それを C: 常駐 staging ルート(既定 D:\_c_migration、
        = 外付け D: 上に間借りして一緒に travels)へ集約する。
      - 新機では restore_working_set.ps1 が逆方向に展開して **同一絶対パス**を復元する
        (ハードコード破損ゼロ = plan §2 の最重要要件)。$Targets は restore 側と完全一致。

    staging 上のレイアウト(ドライブレターをフォルダ名に展開):
        <Dest>\C\Users\puruy\.claude                       (hooks/memory/settings/skills)
        <Dest>\C\Users\puruy\.claude.json                  (単一ファイル: MCP 配線本体)
        <Dest>\C\Users\puruy\.codex                        (config.toml/memories/state)
        <Dest>\C\Users\puruy\browser-use-project           (alpaca_state.json 等 live state)
        <Dest>\C\Users\puruy\.gitconfig                    (単一ファイル)
        <Dest>\C\Users\puruy\AppData\Roaming\GitHub CLI    (gh hosts.yml)
        <Dest>\C\Users\puruy\Documents\PowerShell          (PS profile)
        <Dest>\C\Users\puruy\.config
        <Dest>\C\Users\puruy\.cache\huggingface            (任意)
        <Dest>\C\Users\puruy\.ollama\models                (任意)
        <Dest>\reference\user_path.txt                     (User PATH 退避)
        <Dest>\reference\user_env_nonsecret.txt            (User env: secret 3キー除外)
        <Dest>\reference\scheduled_tasks\*.xml             (Export-ScheduledTask)

    ★秘密の扱い(plan §5 / manifest §5 — 物理移送前提で再スコープ):
      - secret は staging に **平文で置かない**。具体的には次を staging から除外し、
        migrate_secrets.ps1 -Mode Bundle の暗号化バンドル(7z AES-256)へ回す:
          * C:\Users\puruy\.claude\.credentials.json   (claude-home ジョブから /XF 除外)
          * C:\Users\puruy\.codex\auth.json            (codex ジョブから /XF 除外)
          * C:\Users\puruy\.ssh\id_ed25519(.pub)       (そもそも $Targets に含めない)
          * User env 平文 3 キー(ANTHROPIC_API_KEY / TELEGRAM_BOT_TOKEN /
            SOCIALDATA_API_KEY)= ファイルでないため reference export からも除外
      - D:\api-keys.json と raptor の settings.local.json は **D: 上 = travels** のため
        本スクリプトの対象外(別送不要)。off-disk 損失保険も migrate_secrets.ps1 が担う。

    冪等: robocopy /MIR(ディレクトリ)は差分のみ転送。再実行で増分同期。単一ファイルは
          /MIR を使わず(共有親ディレクトリを purge しないため)対象ファイルのみ上書きコピー。
    本スクリプトは ★外付け D: が無い現状では実行しないこと(作成・構文検証のみ)。

.PARAMETER Dest
    C: 常駐 staging ルート(既定 D:\_c_migration = 外付け D: 上に間借り)。

.PARAMETER DryRun
    robocopy /L でリスト表示のみ(実コピーしない)。-WhatIf と同義。
    DryRun 時は reference export(PATH/env/tasks)も実書き込みをスキップする。

.PARAMETER IncludeRunOutputs
    out\ / .out\ などの大きな run 出力ディレクトリも含める(既定は除外)。

.EXAMPLE
    pwsh -File .\backup_working_set.ps1 -DryRun
    # 既定 Dest=D:\_c_migration へ。まず DryRun で対象とサイズを確認

.EXAMPLE
    pwsh -File .\backup_working_set.ps1 -Dest D:\_c_migration
    # 実 staging(再実行で差分のみ)
#>
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$Dest = 'D:\_c_migration',

    [switch]$DryRun,

    [switch]$IncludeRunOutputs
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# -WhatIf もしくは -DryRun のとき robocopy を /L (list only) で走らせる
$ListOnly = $DryRun.IsPresent -or $WhatIfPreference

# ------------------------------------------------------------------ targets
# Src     = 現機の絶対パス(C: 常駐・非 secret のみ。D: 配下は travels = 対象外)。
# IsFile  = 単一ファイル($true なら /MIR せず共有親を purge しないファイルコピー分岐)。
# ExtraXD = このジョブ固有の追加除外ディレクトリ名(robocopy /XD)。
# ExtraXF = このジョブ固有の追加除外ファイル(full-path 可。secret を別バンドルへ回す)。
# Optional= 任意(不在でも問題ない大容量キャッシュ等。不在時は通常どおり SKIP)。
# ★この $Targets は restore_working_set.ps1 の $Targets と完全一致させること。
$Targets = @(
    # claude-home: .credentials.json(端末紐づき secret)は別バンドルへ回すため /XF 除外
    [pscustomobject]@{ Name = 'claude-home'; Src = 'C:\Users\puruy\.claude';                    IsFile = $false; ExtraXD = @();              ExtraXF = @('C:\Users\puruy\.claude\.credentials.json'); Optional = $false }
    # claude-json: MCP 配線・oauth・trust の本体。.claude\ の外にある単一ファイル
    [pscustomobject]@{ Name = 'claude-json'; Src = 'C:\Users\puruy\.claude.json';               IsFile = $true;  ExtraXD = @();              ExtraXF = @();                                          Optional = $false }
    # codex: Codex 二本柱の核。auth.json(secret)は別バンドルへ。tmp/logs は嵩むので除外
    [pscustomobject]@{ Name = 'codex';       Src = 'C:\Users\puruy\.codex';                     IsFile = $false; ExtraXD = @('tmp','logs'); ExtraXF = @('C:\Users\puruy\.codex\auth.json');         Optional = $false }
    # browser-use: trading の live state(alpaca_state.json / telegram_offset.json)。code は D: 側
    [pscustomobject]@{ Name = 'browser-use'; Src = 'C:\Users\puruy\browser-use-project';        IsFile = $false; ExtraXD = @();              ExtraXF = @();                                          Optional = $false }
    [pscustomobject]@{ Name = 'gitconfig';   Src = 'C:\Users\puruy\.gitconfig';                 IsFile = $true;  ExtraXD = @();              ExtraXF = @();                                          Optional = $false }
    [pscustomobject]@{ Name = 'gh-hosts';    Src = 'C:\Users\puruy\AppData\Roaming\GitHub CLI'; IsFile = $false; ExtraXD = @();              ExtraXF = @();                                          Optional = $false }
    [pscustomobject]@{ Name = 'ps-profile';  Src = 'C:\Users\puruy\Documents\PowerShell';       IsFile = $false; ExtraXD = @();              ExtraXF = @();                                          Optional = $false }
    [pscustomobject]@{ Name = 'config';      Src = 'C:\Users\puruy\.config';                    IsFile = $false; ExtraXD = @();              ExtraXF = @();                                          Optional = $false }
    # hf-cache / ollama: 再ダウンロード可能。任意(不在でも問題なし)
    [pscustomobject]@{ Name = 'hf-cache';    Src = 'C:\Users\puruy\.cache\huggingface';         IsFile = $false; ExtraXD = @();              ExtraXF = @();                                          Optional = $true  }
    [pscustomobject]@{ Name = 'ollama';      Src = 'C:\Users\puruy\.ollama\models';             IsFile = $false; ExtraXD = @();              ExtraXF = @();                                          Optional = $true  }
)

# 共通除外(plan の要件どおり)。.git は残す(repo 履歴温存) = 除外しない。
$ExcludeDirs   = @('__pycache__', '.venv', 'venv', 'node_modules', '.mypy_cache', '.pytest_cache', '.ruff_cache')
$ExcludeFiles  = @('*.pyc', '*.tmp')                    # secret は各ジョブの ExtraXF で full-path 除外
$RunOutputDirs = @('out', '.out')                       # -IncludeRunOutputs が無ければ除外

# reference export から必ず除外する平文 secret env(ファイルでない = travels で拾えない)。
# これらは migrate_secrets.ps1 の暗号化バンドルへ同梱し、新機では再発行/再設定する。
$SecretEnvNames = @('ANTHROPIC_API_KEY', 'TELEGRAM_BOT_TOKEN', 'SOCIALDATA_API_KEY')

# ------------------------------------------------------------------ helpers

function Get-MirrorChildPath {
    # 絶対パス C:\Users\puruy\.claude -> <Root>\C\Users\puruy\.claude
    # 単一ファイル C:\Users\puruy\.claude.json -> <Root>\C\Users\puruy\.claude.json
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
        単一ファイルコピー(/MIR なし)でも同じフッター表が出るため流用可。
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

# Dest のドライブが存在するか(fail-closed)。既定 D:\_c_migration なら外付け D: が要接続。
$destRoot = [System.IO.Path]::GetPathRoot([System.IO.Path]::GetFullPath($Dest))
if (-not (Test-Path -LiteralPath $destRoot)) {
    throw "Dest のドライブ '$destRoot' が存在しません。外付け D: を接続(またはレター固定)し、正しい staging ルートを指定してください。"
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
    throw "Dest はドライブのルート '$destFull' にできません(例: D:\_c_migration のようにサブフォルダを指定)。"
}

$LogDir = Join-Path $Dest '_migration_logs'
[System.IO.Directory]::CreateDirectory($LogDir) | Out-Null   # -WhatIf に影響されず常に作成

Write-Host ''
Write-Host '=== backup_working_set.ps1 (GPU PC 移行 step 1 — C: 常駐 staging) ===' -ForegroundColor Cyan
Write-Host ("Dest (staging)   : {0}" -f $destFull)
Write-Host ("Mode             : {0}" -f ($(if ($ListOnly) { 'DryRun (/L list only — コピーしません)' } else { '実 staging' })))
Write-Host ("IncludeRunOutputs: {0}" -f $IncludeRunOutputs.IsPresent)
if (-not $IncludeRunOutputs) {
    Write-Host ("除外(run 出力) : {0}  ← -IncludeRunOutputs で含められます" -f ($RunOutputDirs -join ', ')) -ForegroundColor Yellow
}
Write-Host ("除外(secret)   : .credentials.json / .codex auth.json / .ssh / env3キー は staging 外 = migrate_secrets.ps1") -ForegroundColor Yellow
Write-Host ("前提            : D:\ 配下(projects/raptor/tools/docs/api-manager)は外付け本体ごと travels = 対象外") -ForegroundColor Yellow
Write-Host ("ログ             : {0}" -f $LogDir)
Write-Host ''

# ------------------------------------------------------------------ run

$report = @()

foreach ($t in $Targets) {
    $srcFull = [System.IO.Path]::GetFullPath($t.Src)

    if (-not (Test-Path -LiteralPath $srcFull)) {
        $tag = if ($t.Optional) { 'SKIP (任意・不在)' } else { 'SKIP — ソースが存在しません' }
        Write-Host ("[{0,-12}] {1}: {2}" -f $t.Name, $tag, $srcFull) -ForegroundColor DarkYellow
        $report += [pscustomobject]@{ Target = $t.Name; Status = 'Skipped (no source)'; ExitCode = ''; FilesCopied = ''; BytesCopied = ''; Failed = '' }
        continue
    }

    $dstFull = Get-MirrorChildPath -Root $destFull -AbsPath $srcFull
    $log     = Join-Path $LogDir ("{0}.log" -f $t.Name)

    if ($t.IsFile) {
        # --- 単一ファイル分岐 ---
        # 共有親ディレクトリ(<Dest>\C\Users\puruy)を /MIR で purge しないよう、対象ファイル
        # のみをコピーする(robocopy <srcParent> <dstParent> <fileName>。/MIR は使わない)。
        $srcParent = [System.IO.Path]::GetDirectoryName($srcFull)
        $fileName  = [System.IO.Path]::GetFileName($srcFull)
        $dstParent = [System.IO.Path]::GetDirectoryName($dstFull)

        $fileOpts = @('/R:2', '/W:5', '/BYTES', '/NP', '/NFL', '/NDL', '/COPY:DAT', '/TEE')
        if ($ListOnly) { $fileOpts += '/L' }

        $argList = @($srcParent, $dstParent, $fileName) + $fileOpts + @("/LOG:$log")

        Write-Host ("[{0,-12}] {1}  (単一ファイル)" -f $t.Name, $srcFull) -ForegroundColor Green
        Write-Host ("            -> {0}" -f $dstFull) -ForegroundColor DarkGray
    }
    else {
        # --- ディレクトリ分岐(従来の /MIR ミラー) ---
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

# ------------------------------------------------------------------ reference export
# 新機再構築に要るが「ファイルでない」状態を退避: User PATH / 非 secret User env /
# Scheduled Tasks 定義(XML)。secret env 3 キーは必ず除外(migrate_secrets が担当)。
# 失敗しても staging 本体の成否は左右しない(fail-soft、warning のみ)。

$refDir = Join-Path $Dest 'reference'
if ($ListOnly) {
    Write-Host ''
    Write-Host ("[reference  ] DryRun のため export はスキップ(実行時に {0} へ生成)" -f $refDir) -ForegroundColor DarkYellow
}
else {
    Write-Host ''
    Write-Host ("[reference  ] export -> {0}" -f $refDir) -ForegroundColor Green
    try {
        [System.IO.Directory]::CreateDirectory($refDir) | Out-Null

        # (1) User PATH
        try {
            $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
            if ($null -eq $userPath) { $userPath = '' }
            Set-Content -LiteralPath (Join-Path $refDir 'user_path.txt') -Value $userPath -Encoding UTF8
            Write-Host '            user_path.txt 退避' -ForegroundColor DarkGray
        }
        catch {
            Write-Host ("            !! user_path.txt 退避失敗: {0}" -f $_.Exception.Message) -ForegroundColor Yellow
        }

        # (2) 非 secret User env(secret 3 キーと PATH は除外)
        try {
            $userEnv = [Environment]::GetEnvironmentVariables('User')
            $envLines = foreach ($k in ($userEnv.Keys | Sort-Object)) {
                if ($SecretEnvNames -contains $k) { continue }   # 平文 secret は除外
                if ($k -ieq 'Path') { continue }                 # PATH は別ファイル
                ('{0}={1}' -f $k, $userEnv[$k])
            }
            Set-Content -LiteralPath (Join-Path $refDir 'user_env_nonsecret.txt') -Value $envLines -Encoding UTF8
            Write-Host ("            user_env_nonsecret.txt 退避(secret 3キー除外: {0})" -f ($SecretEnvNames -join ', ')) -ForegroundColor DarkGray
        }
        catch {
            Write-Host ("            !! user_env_nonsecret.txt 退避失敗: {0}" -f $_.Exception.Message) -ForegroundColor Yellow
        }

        # (3) Scheduled Tasks 定義(FullSense / RAPTOR / ClaudeCode* を XML エクスポート)
        try {
            $taskDir = Join-Path $refDir 'scheduled_tasks'
            [System.IO.Directory]::CreateDirectory($taskDir) | Out-Null
            $tasks = Get-ScheduledTask -ErrorAction SilentlyContinue |
                Where-Object { $_.TaskName -match 'FullSense|RAPTOR|ClaudeCode' }
            $taskCount = 0
            foreach ($task in $tasks) {
                try {
                    $xml  = Export-ScheduledTask -TaskName $task.TaskName -TaskPath $task.TaskPath
                    $safe = ($task.TaskName -replace '[\\/:*?"<>|]', '_')
                    Set-Content -LiteralPath (Join-Path $taskDir ("{0}.xml" -f $safe)) -Value $xml -Encoding UTF8
                    $taskCount++
                }
                catch {
                    Write-Host ("            !! task '{0}' export 失敗: {1}" -f $task.TaskName, $_.Exception.Message) -ForegroundColor Yellow
                }
            }
            Write-Host ("            scheduled_tasks\*.xml 退避({0} 件)" -f $taskCount) -ForegroundColor DarkGray
            Write-Host '            ※ 復元時 action の C: 依存(python.exe / raptor libexec)は新機パスへ要是正' -ForegroundColor DarkYellow
        }
        catch {
            Write-Host ("            !! scheduled task export 失敗: {0}" -f $_.Exception.Message) -ForegroundColor Yellow
        }
    }
    catch {
        Write-Host ("            !! reference export 全体失敗(staging 本体には影響なし): {0}" -f $_.Exception.Message) -ForegroundColor Yellow
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
    Write-Host 'DryRun 完了(実コピーなし)。問題なければ -DryRun を外して実 staging してください。' -ForegroundColor Yellow
} else {
    Write-Host '★秘密(.credentials.json / .codex auth.json / .ssh / env3キー)はこの staging に含まれていません。' -ForegroundColor Yellow
    Write-Host '  別途 migrate_secrets.ps1 -Mode Bundle で暗号化バンドル(7z AES-256)を作成してください。' -ForegroundColor Yellow
    Write-Host '★D:\ 配下(projects/raptor/tools/docs/api-manager)は外付け本体ごと travels = この staging には含めません。' -ForegroundColor Yellow
    Write-Host 'staging 完了。新機では restore_working_set.ps1 で同一絶対パスへ展開します。' -ForegroundColor Green
}
exit 0
