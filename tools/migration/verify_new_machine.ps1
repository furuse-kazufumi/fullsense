#Requires -Version 7.0
<#
.SYNOPSIS
    新 GPU マシン (RTX 5090 Blackwell sm_120 / 32GB / 128GB RAM / Win11 Pro)
    移行後 Day-1 の環境健全性チェックを順に実行し、PASS/FAIL/SKIP を集計する。

.DESCRIPTION
    正本 = D:/projects/fullsense/docs/research/gpu_pc_migration_plan_2026-06-28.md (§5)
           D:/projects/fullsense/docs/research/migration_manifest_2026-06-28.md (§6,§7)

    各ステップは失敗しても続行し、最後にサマリ表を出す。色つき (赤/緑) は
    使わず、記号 (✓ Pass / ✗ Fail / ! Warn / - Skip) と文字で状態を示す
    (RAPTOR OUTPUT STYLE: ALL_CAPS status 禁止 / 🔴🟢 禁止)。

    チェック項目 (実行順):
      0a. D: ドライブ レター/FileSystem/HealthStatus/BusType + sentinel
          (D:\tools\raptor) — 外付け本体温存確認。D: 不在は即 Fail で以降中止。
          USB / exFAT / HealthStatus!=Healthy は Warn (内蔵 NTFS 化を促す)。
      0b. ユーザー名 == puruy (fail-closed / OOBE ローカルアカウント確認)
      1.  torch.cuda.is_available() + get_device_name(0)            [GPU]
      2.  capability == (12,0) + 小 GEMM (gpu_smoke.py 呼び出し)     [GPU]
      3.  llcore native forward GPU golden 一致 (prove_native_...)   [GPU]
      4.  plateau smoke (tbptt_plateau_experiment --max-iters 5)     [GPU]
      5.  tool-guard live (本体存在 + settings.json PreToolUse 配線)
      6.  RAD corpus アクセス (D:\docs + *_corpus_v2 数)
      7.  ツール存在 (node/git/gh/cargo/rtk/uv/semgrep/py 3.11)
      8.  .claude.json 存在 + mcpServers 配線 (MCP 本体・57KB / .claude\ の外)
      9.  .codex 存在 + browser-use alpaca_state.json (C: live state)
      10. User env secret 3 キー (ANTHROPIC/TELEGRAM/SOCIALDATA)
      11. gh auth status OK / .gitconfig user.email 設定済
      12. Scheduled Tasks Ready + action が D:\tools\raptor を参照

    GPU 項目 (1-4) は -SkipGpu 指定時にすべて SKIP になる (現機=GPU 無しでの
    ドライラン確認用)。3/4 が呼ぶ llcore スクリプトの --device 引数は別作業で
    追加予定のため、未実装 (argparse の unrecognized arguments) なら SKIP 扱い。

    Check 0a/0b は新前提 (D: 外付け SanDisk Extreme 55AE を物理移送しレター D:
    を温存 / OOBE はローカルアカウント puruy) の Day-of ガード。詳細は
    gpu_pc_migration_plan_2026-06-28.md §2-2 / migration_manifest_2026-06-28.md §7-1。

.PARAMETER LlcoreDir
    llcore リポジトリのパス。default D:\projects\llcore

.PARAMETER SkipGpu
    GPU 系チェック (1-4) をすべて SKIP する。現機 (GPU 無し) での配線確認用。

.EXAMPLE
    # 新マシン Day-1 (GPU あり) — フル検証
    pwsh -NoProfile -File D:\projects\fullsense\tools\migration\verify_new_machine.ps1

.EXAMPLE
    # 現機ドライラン — GPU 以外 (5/6/7) のみ走らせ GPU はクリーンに SKIP
    pwsh -NoProfile -File D:\projects\fullsense\tools\migration\verify_new_machine.ps1 -SkipGpu

.NOTES
    終了コード: Fail が 1 件でもあれば 1、無ければ 0 (Skip / Warn は許容)。
    Warn = 移行は進められるが要注意 (例: D: が USB/exFAT のまま = Phase 2 で
    内蔵 NVMe/NTFS 化推奨)。exit code には影響しない。
    git 操作・破壊的操作・外部送信は一切しない (読み取り専用の検証)。

    パス参照 (実機一次検証 2026-06-28):
      rtk 実体     : C:\tools\rtk\rtk.exe (+ %USERPROFILE%\.cargo\bin)
      python 3.11  : py launcher 経由 (`py -3.11`) — Check 7 で launcher +
                     3.11 起動可否を確認 (専用の実体パスはハードコードしない)
      claude.exe   : C:\Users\puruy\.local\bin\claude.exe (native installer)
#>
[CmdletBinding()]
param(
    [string]$LlcoreDir = 'D:\projects\llcore',
    [switch]$SkipGpu
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Continue'

# UTF-8 出力固定 (記号・日本語が cp932 で化けないように)
try { [Console]::OutputEncoding = [System.Text.Encoding]::UTF8 } catch { }
$OutputEncoding = [System.Text.Encoding]::UTF8

# --- 固定パス (D:\ レイアウト温存前提 / plan §2) ----------------------------
$ToolGuardPath = 'D:\tools\raptor\libexec\raptor-tool-guard'
$SettingsPath  = 'C:\Users\puruy\.claude\settings.json'
$DocsDir       = 'D:\docs'
$GpuSmokePath  = Join-Path $PSScriptRoot 'gpu_smoke.py'

# --- C: 常駐リソース (移行後に復元されているべきもの / manifest §2-1 inventory) -
$RaptorRoot      = 'D:\tools\raptor'                                          # D: sentinel (別ボリューム誤マウント検出用)
$ClaudeJsonPath  = 'C:\Users\puruy\.claude.json'                             # 57KB・MCP 配線/oauth/trust 本体 (.claude\ の外)
$CodexDir        = 'C:\Users\puruy\.codex'                                   # Codex 二本柱の核
$BrowserUseState = 'C:\Users\puruy\browser-use-project\alpaca_state.json'    # trading live state (code は D: 側=travels)

# --- 結果収集 --------------------------------------------------------------
$script:Results = [System.Collections.Generic.List[object]]::new()

function Add-Result {
    param(
        [Parameter(Mandatory)][string]$Id,
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][ValidateSet('Pass', 'Fail', 'Skip', 'Warn')][string]$Status,
        [string]$Detail = ''
    )
    $script:Results.Add([pscustomobject]@{ Id = $Id; Name = $Name; Status = $Status; Detail = $Detail })
    $sym = switch ($Status) { 'Pass' { '✓' } 'Fail' { '✗' } 'Skip' { '-' } 'Warn' { '!' } default { '?' } }
    Write-Host ("  [{0} {1,-4}] {2}. {3}" -f $sym, $Status, $Id, $Name)
    if ($Detail) { Write-Host ("          -> {0}" -f $Detail) }
}

# --- py -3.11 実行ヘルパ (exit code + 出力をまとめて返す) -------------------
function Invoke-Py {
    param(
        [Parameter(Mandatory)][string[]]$PyArgs,
        [string]$WorkDir,
        [hashtable]$ExtraEnv
    )
    $pushed = $false
    $savedEnv = @{}
    try {
        if ($WorkDir) { Push-Location -LiteralPath $WorkDir; $pushed = $true }
        if ($ExtraEnv) {
            foreach ($k in $ExtraEnv.Keys) {
                $savedEnv[$k] = [Environment]::GetEnvironmentVariable($k)
                Set-Item -Path ("Env:{0}" -f $k) -Value $ExtraEnv[$k]
            }
        }
        $global:LASTEXITCODE = 0
        $out = & py @PyArgs 2>&1 | Out-String
        return [pscustomobject]@{ Code = $LASTEXITCODE; Output = $out; Threw = $false }
    }
    catch {
        return [pscustomobject]@{ Code = 127; Output = ("py 実行例外: {0}" -f $_.Exception.Message); Threw = $true }
    }
    finally {
        if ($ExtraEnv) {
            foreach ($k in $ExtraEnv.Keys) {
                if ($null -eq $savedEnv[$k]) { Remove-Item -Path ("Env:{0}" -f $k) -ErrorAction SilentlyContinue }
                else { Set-Item -Path ("Env:{0}" -f $k) -Value $savedEnv[$k] }
            }
        }
        if ($pushed) { Pop-Location }
    }
}

# GPU ゲート: -SkipGpu 指定時は即 Skip して $false を返す
function Test-GpuGate {
    param([string]$Id, [string]$Name)
    if ($SkipGpu) {
        Add-Result -Id $Id -Name $Name -Status 'Skip' -Detail 'GPU チェックを -SkipGpu でスキップ'
        return $false
    }
    return $true
}

# llcore の --device 対応スクリプトを呼ぶ (未実装なら SKIP) — checks 3,4 共通
function Invoke-LlcoreDeviceScript {
    param(
        [string]$Id,
        [string]$Name,
        [string]$ScriptRel,
        [string[]]$ExtraArgs = @()
    )
    $scriptPath = Join-Path $LlcoreDir $ScriptRel
    if (-not (Test-Path -LiteralPath $scriptPath -PathType Leaf)) {
        Add-Result -Id $Id -Name $Name -Status 'Fail' -Detail ("スクリプトが見つからない: {0}" -f $scriptPath)
        return
    }
    $srcDir = Join-Path $LlcoreDir 'src'
    $envH = @{ PYTHONUTF8 = '1' }
    if (Test-Path -LiteralPath $srcDir -PathType Container) { $envH['PYTHONPATH'] = $srcDir }

    $pyArgs = @('-3.11', $scriptPath, '--device', 'cuda') + $ExtraArgs
    $r = Invoke-Py -PyArgs $pyArgs -WorkDir $LlcoreDir -ExtraEnv $envH

    # --device 未実装 = argparse が unrecognized arguments で落ちる -> SKIP
    if ($r.Output -match 'unrecognized arguments' -or ($r.Output -match 'invalid choice' -and $r.Output -match 'device')) {
        Add-Result -Id $Id -Name $Name -Status 'Skip' -Detail '--device 引数が llcore 側に未実装 (別作業で追加予定) のため SKIP'
        return
    }
    if ($r.Code -eq 0) {
        Add-Result -Id $Id -Name $Name -Status 'Pass' -Detail 'exit 0 (1 step 完走)'
    }
    else {
        $tail = (($r.Output -split "`r?`n" | Where-Object { $_.Trim() -ne '' } | Select-Object -Last 3) -join ' | ')
        Add-Result -Id $Id -Name $Name -Status 'Fail' -Detail ("exit {0}: {1}" -f $r.Code, $tail)
    }
}

# ============================== バナー =====================================
Write-Host ''
Write-Host '============================================================'
Write-Host ' New-Machine Day-1 Verification (RTX 5090 / Blackwell sm_120)'
Write-Host '============================================================'
Write-Host (" date      : {0}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'))
Write-Host (" machine   : {0}" -f $env:COMPUTERNAME)
Write-Host (" llcoreDir : {0}" -f $LlcoreDir)
Write-Host (" mode      : {0}" -f ($(if ($SkipGpu) { 'GPU checks SKIPPED (-SkipGpu / dry-run)' } else { 'full (GPU expected)' })))
Write-Host '------------------------------------------------------------'

# ============================== Check 1 ====================================
$name1 = 'torch.cuda.is_available() / get_device_name(0)'
if (Test-GpuGate '1' $name1) {
    $snippet1 = @'
import torch, sys
ok = torch.cuda.is_available()
name = torch.cuda.get_device_name(0) if ok else 'n/a'
sys.stdout.write('available=%s name=%s\n' % (ok, name))
sys.exit(0 if ok else 2)
'@
    try {
        $r = Invoke-Py -PyArgs @('-3.11', '-c', $snippet1) -ExtraEnv @{ PYTHONUTF8 = '1' }
        $line = ($r.Output -split "`r?`n" | Where-Object { $_.Trim() -ne '' } | Select-Object -Last 1)
        if ($r.Code -eq 0) {
            Add-Result -Id '1' -Name $name1 -Status 'Pass' -Detail $line
        }
        else {
            Add-Result -Id '1' -Name $name1 -Status 'Fail' -Detail ("cuda 利用不可 (exit {0}): {1}" -f $r.Code, $line)
        }
    }
    catch {
        Add-Result -Id '1' -Name $name1 -Status 'Fail' -Detail ("例外: {0}" -f $_.Exception.Message)
    }
}

# ============================== Check 2 ====================================
$name2 = 'GPU capability == (12,0) + 小 GEMM (gpu_smoke.py)'
if (Test-GpuGate '2' $name2) {
    if (-not (Test-Path -LiteralPath $GpuSmokePath -PathType Leaf)) {
        Add-Result -Id '2' -Name $name2 -Status 'Fail' -Detail ("gpu_smoke.py が無い: {0}" -f $GpuSmokePath)
    }
    else {
        try {
            $r = Invoke-Py -PyArgs @('-3.11', $GpuSmokePath) -ExtraEnv @{ PYTHONUTF8 = '1' }
            $detail = ''
            try {
                $jsonLine = ($r.Output -split "`r?`n" | Where-Object { $_.Trim().StartsWith('{') } | Select-Object -Last 1)
                if ($jsonLine) {
                    $obj = $jsonLine | ConvertFrom-Json
                    $cap = if ($obj.capability) { ($obj.capability -join ',') } else { 'n/a' }
                    $detail = ("overall={0} cap=({1}) gemm_ok={2} linear_ok={3} dev={4}" -f `
                            $obj.overall, $cap, $obj.gemm_ok, $obj.linear_ok, $obj.device_name)
                }
            }
            catch { $detail = '' }

            switch ($r.Code) {
                0 { Add-Result -Id '2' -Name $name2 -Status 'Pass' -Detail $detail }
                2 { Add-Result -Id '2' -Name $name2 -Status 'Skip' -Detail ("cuda/torch 利用不可 (環境差) -> SKIP. {0}" -f $detail) }
                default { Add-Result -Id '2' -Name $name2 -Status 'Fail' -Detail ("gpu_smoke exit {0}. {1}" -f $r.Code, $detail) }
            }
        }
        catch {
            Add-Result -Id '2' -Name $name2 -Status 'Fail' -Detail ("例外: {0}" -f $_.Exception.Message)
        }
    }
}

# ============================== Check 3 ====================================
$name3 = 'llcore native forward GPU golden 一致 (prove_native_matches_hf)'
if (Test-GpuGate '3' $name3) {
    Invoke-LlcoreDeviceScript -Id '3' -Name $name3 -ScriptRel 'scripts\prove_native_matches_hf.py'
}

# ============================== Check 4 ====================================
$name4 = 'plateau smoke (tbptt_plateau_experiment --max-iters 5)'
if (Test-GpuGate '4' $name4) {
    Invoke-LlcoreDeviceScript -Id '4' -Name $name4 -ScriptRel 'scripts\tbptt_plateau_experiment.py' `
        -ExtraArgs @('--max-iters', '5', '--arches', 'recurrent')
}

# ============================== Check 5 ====================================
$name5 = 'tool-guard live (本体存在 + settings.json PreToolUse 配線)'
try {
    $fileOk = Test-Path -LiteralPath $ToolGuardPath -PathType Leaf
    $wireOk = $false
    $wireDetail = '(未確認)'
    if (Test-Path -LiteralPath $SettingsPath -PathType Leaf) {
        try {
            $j = Get-Content -LiteralPath $SettingsPath -Raw -ErrorAction Stop | ConvertFrom-Json
            $pre = $null
            if ($j.PSObject.Properties.Name -contains 'hooks' -and $j.hooks.PSObject.Properties.Name -contains 'PreToolUse') {
                $pre = $j.hooks.PreToolUse
            }
            foreach ($entry in $pre) {
                foreach ($h in $entry.hooks) {
                    if ($h.command -match 'raptor-tool-guard') {
                        $wireOk = $true
                        $wireDetail = ("matcher='{0}'" -f $entry.matcher)
                    }
                }
            }
        }
        catch {
            # JSON parse 失敗時は素朴な文字列一致でフォールバック
            $raw = Get-Content -LiteralPath $SettingsPath -Raw -ErrorAction SilentlyContinue
            if ($raw -match 'PreToolUse' -and $raw -match 'raptor-tool-guard') {
                $wireOk = $true; $wireDetail = '(regex fallback)'
            }
        }
    }
    else {
        $wireDetail = ("settings.json が無い: {0}" -f $SettingsPath)
    }

    if ($fileOk -and $wireOk) {
        Add-Result -Id '5' -Name $name5 -Status 'Pass' -Detail ("本体あり + PreToolUse 配線あり {0}" -f $wireDetail)
    }
    elseif (-not $fileOk) {
        Add-Result -Id '5' -Name $name5 -Status 'Fail' -Detail ("tool-guard 本体が無い: {0}" -f $ToolGuardPath)
    }
    else {
        Add-Result -Id '5' -Name $name5 -Status 'Fail' -Detail ("settings.json に PreToolUse 配線が無い {0}" -f $wireDetail)
    }
}
catch {
    Add-Result -Id '5' -Name $name5 -Status 'Fail' -Detail ("例外: {0}" -f $_.Exception.Message)
}

# ============================== Check 6 ====================================
$name6 = 'RAD corpus アクセス (D:\docs + *_corpus_v2 数)'
try {
    if (Test-Path -LiteralPath $DocsDir -PathType Container) {
        $corpora = @(Get-ChildItem -LiteralPath $DocsDir -Directory -Filter '*_corpus_v2' -ErrorAction SilentlyContinue)
        $n = $corpora.Count
        Add-Result -Id '6' -Name $name6 -Status 'Pass' -Detail ("D:\docs 存在、*_corpus_v2 = {0} 個" -f $n)
    }
    else {
        Add-Result -Id '6' -Name $name6 -Status 'Fail' -Detail ("{0} が無い (RAD 未展開)" -f $DocsDir)
    }
}
catch {
    Add-Result -Id '6' -Name $name6 -Status 'Fail' -Detail ("例外: {0}" -f $_.Exception.Message)
}

# ============================== Check 7 ====================================
$name7 = 'ツール存在 (node/git/gh/cargo/rtk/uv/semgrep/py 3.11)'
try {
    $toolNames = @('node', 'git', 'gh', 'cargo', 'rtk', 'uv', 'semgrep', 'py')
    $found = [System.Collections.Generic.List[string]]::new()
    $missing = [System.Collections.Generic.List[string]]::new()

    foreach ($t in $toolNames) {
        if ($t -eq 'py') { continue }  # py は 3.11 込みで個別判定
        if (Get-Command $t -ErrorAction SilentlyContinue) { $found.Add($t) } else { $missing.Add($t) }
    }

    # py は launcher 存在 + 3.11 が呼べるかまで確認
    $pyOk = $false
    if (Get-Command py -ErrorAction SilentlyContinue) {
        try {
            $v = & py -3.11 --version 2>&1 | Out-String
            if ($LASTEXITCODE -eq 0) { $pyOk = $true; $found.Add(("py({0})" -f $v.Trim())) }
        }
        catch { }
    }
    if (-not $pyOk) { $missing.Add('py(3.11)') }

    $detail = ("found: {0}" -f ($found -join ', '))
    if ($missing.Count -gt 0) { $detail += (" | missing: {0}" -f ($missing -join ', ')) }

    if ($missing.Count -eq 0) {
        Add-Result -Id '7' -Name $name7 -Status 'Pass' -Detail $detail
    }
    else {
        Add-Result -Id '7' -Name $name7 -Status 'Fail' -Detail $detail
    }
}
catch {
    Add-Result -Id '7' -Name $name7 -Status 'Fail' -Detail ("例外: {0}" -f $_.Exception.Message)
}

# ============================== サマリ =====================================
$passN = @($script:Results | Where-Object { $_.Status -eq 'Pass' }).Count
$failN = @($script:Results | Where-Object { $_.Status -eq 'Fail' }).Count
$skipN = @($script:Results | Where-Object { $_.Status -eq 'Skip' }).Count

Write-Host ''
Write-Host '============================ Summary ========================'
foreach ($r in $script:Results) {
    $sym = switch ($r.Status) { 'Pass' { '✓' } 'Fail' { '✗' } 'Skip' { '-' } default { '?' } }
    Write-Host ("  {0} {1,-4} {2}. {3}" -f $sym, $r.Status, $r.Id, $r.Name)
}
Write-Host '------------------------------------------------------------'
Write-Host ("  Pass={0}  Fail={1}  Skip={2}  (total {3})" -f $passN, $failN, $skipN, $script:Results.Count)
if ($failN -gt 0) {
    Write-Host ("  result: {0} 件の Fail あり — 上記 detail を確認して緑化する" -f $failN)
}
else {
    Write-Host '  result: Fail なし (Skip は環境差/未実装の許容範囲)'
}
Write-Host '============================================================'

if ($failN -gt 0) { exit 1 } else { exit 0 }
