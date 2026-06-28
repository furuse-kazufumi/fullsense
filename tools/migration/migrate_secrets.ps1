#Requires -Version 7.0
<#
.SYNOPSIS
    秘密(API キー等)を working-set ミラーとは別経路で安全に移送する(GPU PC 移行 secrets)。

.DESCRIPTION
    正本: gpu_pc_migration_plan_2026-06-28.md §5(秘密の移送)
          migration_manifest_2026-06-28.md §5

    対象の秘密ファイル(現機実測):
      - D:\api-keys.json                                  (★API キー一元管理 = secret)
      - D:\tools\raptor\.claude\settings.local.json       (★ANTHROPIC_API_KEY 平文)

    これらは backup_working_set.ps1 の外付けミラーから **意図的に除外** してある。
    本スクリプトはそれらを **パスワード付き zip** にまとめ(7-Zip があれば AES-256 +
    ヘッダ暗号化、無ければ Compress-Archive + 警告)、暗号化 USB 等の別経路で運ぶ。

    ★設計(誤って平文を外付けミラーに混ぜない):
      - 既定の出力先は Desktop\fullsense-secrets(ローカル)。working-set ミラー用の
        外付けドライブ(_migration_logs を持つルート)に出力しようとすると警告/中止。
      - 平文の中間ファイルは作らず、対象ファイルを直接アーカイブへ投入する。
      - 終了時に出力 zip のパスのみ表示し、内容(キー値)はログに出さない。

    ★key ローテーション推奨(plan §5 / manifest §5):
      平文露出の衛生として、移行を機に ANTHROPIC_API_KEY / 各 API キーの
      ローテーション(再発行 + D:\api-keys.json 更新 + 旧キー失効)を検討すること。
      移送 zip はあくまで「移行をブロックしないための保険」であり、理想は
      新機で鍵を新規発行して古い zip は安全に破棄する運用。

.PARAMETER Mode
    Bundle  : 秘密ファイルを暗号化 zip にまとめる(既定)。
    Restore : 暗号化 zip を展開し、元の絶対パスへ各秘密を配置する(新機)。

.PARAMETER Out
    Bundle 時の出力ディレクトリ(既定: Desktop\fullsense-secrets)。
    ★working-set ミラーの外付けドライブには置かないこと(別 USB 推奨)。

.PARAMETER Source
    Restore 時に展開する zip ファイルパス(.7z または .zip)。

.PARAMETER Force
    Restore 時に既存の秘密ファイルを上書きする。Bundle 時に外付けドライブ警告を無視する。

.EXAMPLE
    pwsh -File .\migrate_secrets.ps1 -Mode Bundle
    # Desktop\fullsense-secrets に暗号化 zip を作成(7-Zip ならパスワードを対話入力)

.EXAMPLE
    pwsh -File .\migrate_secrets.ps1 -Mode Restore -Source 'D:\fullsense-secrets-20260715-101010.7z'
    # 新機で zip を展開し D:\api-keys.json 等を元パスへ配置(復元は restore_working_set の後)
#>
[CmdletBinding()]
param(
    [ValidateSet('Bundle', 'Restore')]
    [string]$Mode = 'Bundle',

    [string]$Out,

    [string]$Source,

    [switch]$Force
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

# ------------------------------------------------------------------ 秘密対象
# 各エントリ: 元の絶対パス。アーカイブ内は <drive>\<rel> の相対構造で保持し、
# Restore 時に元の絶対パスへ戻す(restore_working_set と同じドライブレター展開規則)。
$SecretFiles = @(
    'D:\api-keys.json',
    'D:\tools\raptor\.claude\settings.local.json'
)

# ------------------------------------------------------------------ helpers

function Find-SevenZip {
    $cmd = Get-Command 7z.exe -ErrorAction SilentlyContinue
    if ($cmd) { return $cmd.Source }
    foreach ($p in @("$env:ProgramFiles\7-Zip\7z.exe", "${env:ProgramFiles(x86)}\7-Zip\7z.exe")) {
        if (Test-Path -LiteralPath $p) { return $p }
    }
    return $null
}

function Get-ArchiveRelPath {
    # D:\api-keys.json -> D\api-keys.json
    param([string]$AbsPath)
    $full     = [System.IO.Path]::GetFullPath($AbsPath)
    $pathRoot = [System.IO.Path]::GetPathRoot($full)
    $driveLtr = $pathRoot.Substring(0, 1)
    $relative = $full.Substring($pathRoot.Length)
    return (Join-Path $driveLtr $relative)
}

function Restore-AbsPathFromRel {
    # D\api-keys.json -> D:\api-keys.json
    param([string]$RelPath)
    $parts = $RelPath -split '[\\/]', 2
    if ($parts.Count -lt 2) { throw "想定外の相対パス: $RelPath" }
    return ('{0}:\{1}' -f $parts[0], $parts[1])
}

# ================================================================== BUNDLE
function Invoke-Bundle {
    if (-not $Out) {
        $desktop = [Environment]::GetFolderPath('Desktop')
        $Out = Join-Path $desktop 'fullsense-secrets'
    }
    $OutFull = [System.IO.Path]::GetFullPath($Out)

    # ★ガード: 出力先が working-set ミラーの外付けドライブ(_migration_logs を持つ)でないか
    $outDriveRoot = [System.IO.Path]::GetPathRoot($OutFull)
    if ((Test-Path -LiteralPath (Join-Path $outDriveRoot '_migration_logs')) -and -not $Force) {
        throw ("出力先 '{0}' は working-set ミラーの外付けドライブのようです(_migration_logs 検出)。" -f $outDriveRoot +
               "平文を混ぜないため別の暗号化 USB を指定してください(意図的なら -Force)。")
    }

    [System.IO.Directory]::CreateDirectory($OutFull) | Out-Null

    # 実在する秘密のみ収集
    $present = @()
    foreach ($f in $SecretFiles) {
        if (Test-Path -LiteralPath $f) {
            $present += $f
            Write-Host ("  含める: {0}" -f $f) -ForegroundColor Green
        } else {
            Write-Host ("  無し  : {0}(スキップ)" -f $f) -ForegroundColor DarkYellow
        }
    }
    if ($present.Count -eq 0) { throw '対象の秘密ファイルが 1 つも見つかりません。' }

    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $sevenZip = Find-SevenZip

    if ($sevenZip) {
        $archive = Join-Path $OutFull ("fullsense-secrets-{0}.7z" -f $stamp)
        Write-Host ''
        Write-Host '7-Zip を使用して AES-256(ヘッダ暗号化込み)でまとめます。' -ForegroundColor Cyan
        Write-Host 'パスワードを対話入力してください(-p)。空パスワードは禁止です。' -ForegroundColor Yellow

        # ステージング: <drive>\<rel> 構造で一時コピー → アーカイブ → ステージング消去
        $stage = Join-Path ([System.IO.Path]::GetTempPath()) ("fs-secrets-stage-{0}" -f $stamp)
        [System.IO.Directory]::CreateDirectory($stage) | Out-Null
        try {
            foreach ($f in $present) {
                $rel = Get-ArchiveRelPath -AbsPath $f
                $dst = Join-Path $stage $rel
                [System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($dst)) | Out-Null
                Copy-Item -LiteralPath $f -Destination $dst -Force
            }
            # manifest(キー値は書かない。元パスとローテーション注意のみ)
            $manifest = @(
                '# fullsense secrets bundle',
                ("# created : {0}" -f (Get-Date -Format 'o')),
                '# files (restored to these absolute paths by migrate_secrets.ps1 -Mode Restore):'
            ) + ($present | ForEach-Object { "#   $_" }) + @(
                '#',
                '# ★移行を機に API キーのローテーションを検討すること(plan/manifest §5)。'
            )
            Set-Content -LiteralPath (Join-Path $stage 'MANIFEST.txt') -Value $manifest -Encoding utf8

            # -mhe=on: ファイル名(ヘッダ)も暗号化 / -p: パスワード対話入力
            & $sevenZip a -t7z -mhe=on -p "$archive" (Join-Path $stage '*')
            if ($LASTEXITCODE -ne 0) { throw "7z アーカイブ作成に失敗しました (exit $LASTEXITCODE)。" }
        }
        finally {
            if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
        }

        Write-Host ''
        Write-Host ("暗号化バンドル作成: {0}" -f $archive) -ForegroundColor Green
        Write-Host 'これを暗号化 USB 等の別経路で新機へ運び、migrate_secrets.ps1 -Mode Restore で配置してください。' -ForegroundColor Yellow
    }
    else {
        # フォールバック: Compress-Archive は暗号化非対応
        $archive = Join-Path $OutFull ("fullsense-secrets-{0}.zip" -f $stamp)
        Write-Host ''
        Write-Host '!! 7-Zip が見つかりません。Compress-Archive でまとめますが、これは暗号化されません。' -ForegroundColor Red
        Write-Host '!! 平文 zip です。必ず暗号化 USB(BitLocker To Go 等)に置き、転送後すぐ消去してください。' -ForegroundColor Red
        Write-Host '!! 7-Zip 導入(winget install 7zip.7zip)後に再実行することを強く推奨します。' -ForegroundColor Red

        $stage = Join-Path ([System.IO.Path]::GetTempPath()) ("fs-secrets-stage-{0}" -f $stamp)
        [System.IO.Directory]::CreateDirectory($stage) | Out-Null
        try {
            foreach ($f in $present) {
                $rel = Get-ArchiveRelPath -AbsPath $f
                $dst = Join-Path $stage $rel
                [System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($dst)) | Out-Null
                Copy-Item -LiteralPath $f -Destination $dst -Force
            }
            Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $archive -Force
        }
        finally {
            if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
        }
        Write-Host ''
        Write-Host ("平文バンドル作成(★暗号化されていません): {0}" -f $archive) -ForegroundColor Red
    }
}

# ================================================================== RESTORE
function Invoke-Restore {
    if (-not $Source) { throw 'Restore には -Source <zipパス> が必要です。' }
    $SrcFull = [System.IO.Path]::GetFullPath($Source)
    if (-not (Test-Path -LiteralPath $SrcFull)) { throw "アーカイブが見つかりません: $SrcFull" }

    $stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
    $stage = Join-Path ([System.IO.Path]::GetTempPath()) ("fs-secrets-restore-{0}" -f $stamp)
    [System.IO.Directory]::CreateDirectory($stage) | Out-Null

    try {
        $ext = [System.IO.Path]::GetExtension($SrcFull).ToLowerInvariant()
        if ($ext -eq '.7z') {
            $sevenZip = Find-SevenZip
            if (-not $sevenZip) { throw '.7z の展開に 7-Zip が必要ですが見つかりません(winget install 7zip.7zip)。' }
            Write-Host 'パスワードを対話入力してください(-p)。' -ForegroundColor Yellow
            & $sevenZip x "$SrcFull" "-o$stage" -y -p
            if ($LASTEXITCODE -ne 0) { throw "7z 展開に失敗しました(パスワード誤り? exit $LASTEXITCODE)。" }
        }
        elseif ($ext -eq '.zip') {
            Expand-Archive -LiteralPath $SrcFull -DestinationPath $stage -Force
        }
        else {
            throw "未対応の拡張子: $ext(.7z か .zip)"
        }

        # ステージ配下の <drive>\<rel> を元の絶対パスへ配置(MANIFEST.txt は除く)
        $restored = @()
        Get-ChildItem -LiteralPath $stage -Recurse -File | ForEach-Object {
            $rel = $_.FullName.Substring($stage.Length).TrimStart('\', '/')
            if ($rel -ieq 'MANIFEST.txt') { return }
            $abs = Restore-AbsPathFromRel -RelPath $rel
            $absDir = [System.IO.Path]::GetDirectoryName($abs)

            if ((Test-Path -LiteralPath $abs) -and -not $Force) {
                Write-Host ("  既存のためスキップ(上書きは -Force): {0}" -f $abs) -ForegroundColor DarkYellow
                return
            }
            [System.IO.Directory]::CreateDirectory($absDir) | Out-Null
            Copy-Item -LiteralPath $_.FullName -Destination $abs -Force
            Write-Host ("  配置: {0}" -f $abs) -ForegroundColor Green
            $restored += $abs
        }

        Write-Host ''
        if ($restored.Count -gt 0) {
            Write-Host ("秘密を {0} 件配置しました。" -f $restored.Count) -ForegroundColor Green
        } else {
            Write-Host '配置対象がありません(既存スキップ or 空アーカイブ)。' -ForegroundColor Yellow
        }
        Write-Host '★移行を機に API キーのローテーションを検討してください(plan/manifest §5)。' -ForegroundColor Yellow
        Write-Host '★展開した平文 zip は転送後すぐ安全に破棄してください。' -ForegroundColor Yellow
    }
    finally {
        if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
    }
}

# ------------------------------------------------------------------ main
Write-Host ''
Write-Host ('=== migrate_secrets.ps1 (Mode={0}) ===' -f $Mode) -ForegroundColor Cyan
switch ($Mode) {
    'Bundle'  { Invoke-Bundle }
    'Restore' { Invoke-Restore }
}
exit 0
