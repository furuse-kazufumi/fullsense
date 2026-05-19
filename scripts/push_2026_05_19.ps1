# SPDX-License-Identifier: Apache-2.0
# ============================================================================
# 2026-05-19 セッション push スクリプト
#
# 本日の COG-MESH M8.x + M8.1 production wire + llove 統合 + portal 反映
# 累計 commit を 4 リポへ push する.
#
# 実行:
#   pwsh D:\projects\fullsense\scripts\push_2026_05_19.ps1
#
# または PowerShell から直接:
#   D:\projects\fullsense\scripts\push_2026_05_19.ps1
#
# 各リポで以下を順に行う:
#   1. fetch (origin/main 同期)
#   2. 未 push commit 数を表示
#   3. (llive のみ) 軽い pytest 確認 (任意、SKIP_TESTS=$true でスキップ可)
#   4. git push origin main
#   5. 成功なら次のリポへ、失敗なら停止して理由を表示
#
# 安全機能:
#   - 各リポは独立処理 (1 つ失敗しても他は試行する設計)
#   - --force は使わない (fast-forward 失敗時は人手で resolve)
#   - 各 step の出力を保持
# ============================================================================

[CmdletBinding()]
param(
    # テスト実行をスキップ (デフォルトはテスト実行する)
    [switch]$SkipTests,

    # dry-run: git push の代わりに何を push するか表示するだけ
    [switch]$DryRun,

    # 1 リポ失敗で全体停止 (デフォルトは continue)
    [switch]$StopOnFail
)

$ErrorActionPreference = "Continue"

# 対象リポと推奨 push 順 (依存方向: server → emitter → UI → docs)
$Repos = @(
    @{
        Name       = "llmesh"
        Path       = "D:\projects\llmesh"
        TestCmd    = { py -3.11 -m pytest tests/test_timeline.py --tb=no -q }
        TestNote   = "timeline tests (46 PASS 期待)"
    },
    @{
        Name       = "llive"
        Path       = "D:\projects\llive"
        TestCmd    = { py -3.11 -m pytest tests/unit tests/integration -q --tb=no }
        TestNote   = "unit + integration (1518 PASS 期待, ~60s)"
    },
    @{
        Name       = "llove"
        Path       = "D:\projects\llove"
        TestCmd    = { py -3.11 -m pytest tests --tb=no -q }
        TestNote   = "全 tests (796 passed / 6 failed image_tool baseline 期待)"
    },
    @{
        Name       = "fullsense"
        Path       = "D:\projects\fullsense"
        TestCmd    = { bash scripts/verify_publication.sh }
        TestNote   = "verify_publication.sh (ALL CHECKS PASSED 期待)"
    }
)

# ----------------------------------------------------------------------------
# ヘルパ
# ----------------------------------------------------------------------------

function Write-Section {
    param([string]$Title)
    Write-Host ""
    Write-Host "============================================================" -ForegroundColor Cyan
    Write-Host " $Title" -ForegroundColor Cyan
    Write-Host "============================================================" -ForegroundColor Cyan
}

function Test-RepoUnpushed {
    param([string]$Path)
    Push-Location $Path
    try {
        # fetch して origin/main を最新化
        & git fetch origin main 2>&1 | Out-Null
        $unpushed = & git log origin/main..HEAD --oneline 2>&1
        if ($LASTEXITCODE -ne 0) {
            Write-Host "  [warn] git log 失敗 (リモート未設定?)" -ForegroundColor Yellow
            return $null
        }
        return $unpushed
    } finally {
        Pop-Location
    }
}

# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

Write-Section "2026-05-19 セッション push スクリプト"
Write-Host "対象リポ: $($Repos.Count) 件"
Write-Host "SkipTests: $SkipTests / DryRun: $DryRun / StopOnFail: $StopOnFail"
Write-Host ""

$Results = @()

foreach ($Repo in $Repos) {
    Write-Section "[$($Repo.Name)] $($Repo.Path)"

    if (-not (Test-Path $Repo.Path)) {
        Write-Host "  [skip] パスが存在しません: $($Repo.Path)" -ForegroundColor Yellow
        $Results += [PSCustomObject]@{ Name = $Repo.Name; Status = "SKIP_NOPATH" }
        continue
    }

    Push-Location $Repo.Path
    try {
        # ----- 1. 未 push commit 一覧 -----
        Write-Host "[1/4] git fetch + 未 push commit 確認..."
        $unpushed = Test-RepoUnpushed -Path $Repo.Path
        if ($null -eq $unpushed -or $unpushed.Count -eq 0) {
            Write-Host "  ✓ 未 push commit なし (skip)" -ForegroundColor Green
            $Results += [PSCustomObject]@{ Name = $Repo.Name; Status = "SKIP_NOUNPUSHED" }
            continue
        }
        Write-Host "  未 push commit:"
        $unpushed | ForEach-Object { Write-Host "    $_" }

        # ----- 2. テスト -----
        if ($SkipTests) {
            Write-Host "[2/4] テストスキップ (--SkipTests)"
        } else {
            Write-Host "[2/4] テスト実行 ($($Repo.TestNote))..."
            & $Repo.TestCmd
            if ($LASTEXITCODE -ne 0) {
                Write-Host "  [warn] テストに failure あり (続行可能)" -ForegroundColor Yellow
                if ($StopOnFail) {
                    Write-Host "  [stop] --StopOnFail のため停止" -ForegroundColor Red
                    $Results += [PSCustomObject]@{ Name = $Repo.Name; Status = "FAIL_TEST" }
                    break
                }
            } else {
                Write-Host "  ✓ テスト OK" -ForegroundColor Green
            }
        }

        # ----- 3. uncommitted 確認 -----
        Write-Host "[3/4] uncommitted changes チェック..."
        $dirty = & git status --porcelain 2>&1
        # SESSION_SUMMARY.md は Stop hook が毎回上書きするので無視
        $dirty = $dirty | Where-Object { $_ -notmatch "SESSION_SUMMARY\.md" }
        if ($dirty) {
            Write-Host "  [warn] uncommitted changes あり (push は HEAD のみ)" -ForegroundColor Yellow
            $dirty | ForEach-Object { Write-Host "    $_" }
        } else {
            Write-Host "  ✓ clean" -ForegroundColor Green
        }

        # ----- 4. push -----
        if ($DryRun) {
            Write-Host "[4/4] [DRY-RUN] git push origin main をスキップ"
            $Results += [PSCustomObject]@{ Name = $Repo.Name; Status = "DRYRUN" }
        } else {
            Write-Host "[4/4] git push origin main..."
            & git push origin main 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Host "  ✗ push 失敗" -ForegroundColor Red
                $Results += [PSCustomObject]@{ Name = $Repo.Name; Status = "FAIL_PUSH" }
                if ($StopOnFail) {
                    Write-Host "  [stop] --StopOnFail のため停止" -ForegroundColor Red
                    break
                }
            } else {
                Write-Host "  ✓ push 成功" -ForegroundColor Green
                $Results += [PSCustomObject]@{ Name = $Repo.Name; Status = "OK" }
            }
        }
    } finally {
        Pop-Location
    }
}

# ----------------------------------------------------------------------------
# サマリ
# ----------------------------------------------------------------------------

Write-Section "Summary"
$Results | Format-Table -AutoSize

$failed = @($Results | Where-Object { $_.Status -like "FAIL_*" })
if ($failed.Count -gt 0) {
    Write-Host "失敗: $($failed.Count) 件" -ForegroundColor Red
    exit 1
}
$ok = @($Results | Where-Object { $_.Status -eq "OK" })
Write-Host "成功 push: $($ok.Count) 件" -ForegroundColor Green
exit 0
