#Requires -Version 7.0
<#
.SYNOPSIS
    新 GPU マシン (RTX 5090 Blackwell sm_120 / 32GB / 128GB RAM / Win11 Pro / ユーザー puruy)
    の Day-of 「要再インストール物」を順序付きで導入する draft。

    ★★ レビュー必須 / 自動実行 非推奨 ★★
    既定は dry-run (計画表示のみ・存在チェックは実行)。実際に導入するには -Execute を渡す。
    本スクリプトは draft であり、実機 (新機 GPU 機) で 1 ステップずつ目視しながら使う前提。
    一括無人実行は想定しない。

.DESCRIPTION
    正本 = D:/projects/fullsense/docs/research/migration_dependencies_2026-06-28.md (§5 順序)
           D:/projects/fullsense/docs/research/gpu_pc_migration_plan_2026-06-28.md     (§4)
           D:/projects/fullsense/docs/research/migration_manifest_2026-06-28.md        (§3,§6,§7)

    設計方針:
      - 各ステップ = 存在チェック → 未検出なら導入 (冪等寄り)。既存は [skip]。
      - 破壊的操作なし (削除・git・force・DB drop は一切しない)。winget/pip/cargo/npm の
        additive な導入のみ。
      - secret・対話が要る所 (NVIDIA driver / gh auth login / Codex login / Claude 再ログイン /
        claude.ai コネクタ / User env secret) は Write-Host の案内に留め、自動実行しない。
      - 色つき (赤/緑) は使わず記号で状態を示す (RAPTOR OUTPUT STYLE: ALL_CAPS 禁止 / 絵文字赤緑禁止)。
        [skip] 既存 / [need] 未検出 / [plan] dry-run / [run] 実行 / [manual] 手動 / [warn] 注意。
      - ★torch は freeze の +cpu を使わず cu128 index で先入れ (Blackwell 必須・§1-A)。

    実行順 (§5):
      1  GPU driver R570+            [manual 案内]
      2  D: 温存確認 (Test-Path)     [前提ガード]
      3  base CLI (winget 5 本)       Git/Node v24/gh/7zip/Rustup → rustup default stable
      4  rtk (cargo install, rev 固定)
      5  uv (astral installer)
      6  global npm 6 本
      7  ★torch cu128 + 検証
      8  FullSense editable (D: 上コードから / extras 明示)
      9  freeze 差分補完 [案内: +cpu と -e/file:// を除外]
      10 semgrep (py3.14)
      11 scholar-search-mcp (py3.11)
      12 MCP ランタイム (osv-mcp uv sync + uvx pre-warm 案内)
      13 Ollama + 5 モデル pull
      14 browser-use 別 venv (uv sync)
      15 ccr node-pty ロード確認 (失敗時のみ rebuild)
      16 対話・secret 再設定         [manual 案内集約]

.PARAMETER Execute
    指定時のみ実際に導入を実行する。未指定 (既定) は dry-run = 計画と存在チェックのみ。

.PARAMETER SkipOllamaModels
    Ollama 本体は入れるが 26GB のモデル pull はスキップ (D: 経由 copy で運ぶ場合)。

.EXAMPLE
    # まず計画を眺める (何も導入しない・安全)
    pwsh -NoProfile -File D:\projects\fullsense\tools\migration\bootstrap_install.ps1

.EXAMPLE
    # レビュー後、実際に導入 (1 回通し)
    pwsh -NoProfile -File D:\projects\fullsense\tools\migration\bootstrap_install.ps1 -Execute

.NOTES
    git 操作・破壊的操作・外部送信はしない。winget/cargo/npm/pip の導入は network が要る。
    対話ログイン (gh/codex/claude) と driver は本スクリプト外 (手動)。
    UTF-8 (BOM なし) 前提。
#>

[CmdletBinding()]
param(
    [switch]$Execute,
    [switch]$SkipOllamaModels
)

$ErrorActionPreference = 'Continue'

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
$script:Planned = 0
$script:Skipped = 0
$script:Ran     = 0
$script:Manual  = 0

function Write-Head {
    param([string]$Text)
    Write-Host ""
    Write-Host "==== $Text ===="
}

function Test-Cmd {
    param([string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

# 存在チェック → 未検出なら導入 (dry-run 既定)
function Step {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][scriptblock]$Check,   # $true = 既に存在
        [Parameter(Mandatory)][string]$CmdText,      # 人間可読の導入コマンド
        [scriptblock]$Run                            # 実導入 (省略時は CmdText を & で評価しない=案内のみ)
    )
    Write-Host ""
    Write-Host "-- $Name"
    $present = $false
    try { $present = [bool](& $Check) } catch { $present = $false }
    if ($present) {
        Write-Host "   [skip] 既に存在 — 再導入不要"
        $script:Skipped++
        return
    }
    Write-Host "   [need] 未検出"
    Write-Host "   cmd  : $CmdText"
    if ($Execute -and $Run) {
        Write-Host "   [run] 実行中..."
        try { & $Run } catch { Write-Host "   [warn] 失敗: $($_.Exception.Message)" }
        $script:Ran++
    } else {
        Write-Host "   [plan] -Execute 未指定のため実行せず (dry-run)"
        $script:Planned++
    }
}

# 手動 (対話/secret/driver) は案内のみ — 自動実行しない
function Manual {
    param([Parameter(Mandatory)][string]$Name, [Parameter(Mandatory)][string]$Text)
    Write-Host ""
    Write-Host "-- $Name"
    Write-Host "   [manual] $Text"
    $script:Manual++
}

# winget パッケージ導入 (存在チェックはコマンド名で)
function Step-Winget {
    param([string]$Name, [string]$CmdName, [string]$WingetId, [string]$ExtraArgs = '')
    $argline = "winget install --id $WingetId --accept-source-agreements --accept-package-agreements $ExtraArgs".Trim()
    Step -Name $Name -Check { Test-Cmd $CmdName } -CmdText $argline -Run {
        $a = @('install','--id',$WingetId,'--accept-source-agreements','--accept-package-agreements')
        if ($ExtraArgs) { $a += $ExtraArgs.Split(' ') }
        & winget @a
    }.GetNewClosure()
}

# ----------------------------------------------------------------------------
# banner
# ----------------------------------------------------------------------------
Write-Host "================================================================"
Write-Host " FullSense GPU 機 bootstrap (draft / レビュー必須)"
if ($Execute) {
    Write-Host " MODE = EXECUTE  (実際に導入します)"
} else {
    Write-Host " MODE = DRY-RUN  (計画表示のみ。導入するには -Execute)"
}
Write-Host " 正本 = migration_dependencies_2026-06-28.md / gpu_pc_migration_plan / manifest"
Write-Host "================================================================"

# ----------------------------------------------------------------------------
# 1. GPU driver (manual)
# ----------------------------------------------------------------------------
Write-Head "1. NVIDIA driver (Blackwell sm_120)"
$nvsmi = Test-Cmd 'nvidia-smi'
if ($nvsmi) {
    Write-Host "   [skip] nvidia-smi 検出:"
    try { & nvidia-smi --query-gpu=name,driver_version --format=csv,noheader } catch {}
} else {
    Manual -Name "NVIDIA driver R570+" -Text @"
RTX 5090 = sm_120 → driver R570 以降が必須 (cu128 wheel が要求)。
https://www.nvidia.com/Download/index.aspx から Game Ready/Studio R570+ を導入し再起動。
CUDA toolkit は PyTorch wheel 同梱のため driver のみで可。
"@
}

# ----------------------------------------------------------------------------
# 2. D: 温存ガード
# ----------------------------------------------------------------------------
Write-Head "2. D: 温存確認 (外付け本体 travels の sentinel)"
if (Test-Path 'D:\tools\raptor') {
    Write-Host "   [skip] D:\tools\raptor 検出 — D: が正しくマウントされている"
} else {
    Write-Host "   [warn] D:\tools\raptor が無い。外付け D: が未接続/未マウントの可能性。"
    Write-Host "          plan §2-2 でレター D: を固定してから本スクリプトを続行すること。"
    Write-Host "          editable install (§8) と MCP (§12) は D: 実体に依存するため中断推奨。"
}

# ----------------------------------------------------------------------------
# 3. base CLI (winget)
# ----------------------------------------------------------------------------
Write-Head "3. base CLI (winget)"
Step-Winget -Name "Git (Git Bash 同梱)"     -CmdName 'git'    -WingetId 'Git.Git'
# ★Node は v24 系を厳守 (node-pty 0.13.1 engines = node <25.0.0)。LTS が v24 を返すか要確認。
Step-Winget -Name "Node.js LTS (★v24・<25 厳守)" -CmdName 'node' -WingetId 'OpenJS.NodeJS.LTS'
Step-Winget -Name "GitHub CLI"               -CmdName 'gh'     -WingetId 'GitHub.cli'
Step-Winget -Name "7-Zip (migrate_secrets が依存)" -CmdName '7z' -WingetId '7zip.7zip'
Step-Winget -Name "Rustup"                   -CmdName 'rustup' -WingetId 'Rustlang.Rustup'

Step -Name "rustup default stable" `
     -Check { (Test-Cmd 'cargo') -and ((rustup default 2>$null) -match 'stable') } `
     -CmdText "rustup default stable" `
     -Run { & rustup default stable }

Write-Host ""
Write-Host "   [warn] 7-Zip は既定で PATH 未登録 (現機実測)。'7z' 解決不可なら PATH に"
Write-Host "          'C:\Program Files\7-Zip' を追加するか migrate_secrets.ps1 をフルパス参照に。"
Write-Host "   [warn] Node が v25+ になっていないか確認: node -v が v24.x であること (node-pty engines)。"

# ----------------------------------------------------------------------------
# 4. rtk (cargo install / rev 固定)
# ----------------------------------------------------------------------------
Write-Head "4. rtk (token killer / .cargo/bin)"
$rtkRev = '6444c4b018f5619ab2a441191534937894b17970'
Step -Name "rtk v0.34.1" `
     -Check { Test-Cmd 'rtk' } `
     -CmdText "cargo install --git https://github.com/rtk-ai/rtk --rev $rtkRev" `
     -Run { & cargo install --git https://github.com/rtk-ai/rtk --rev $rtkRev }
Write-Host "   [warn] C:\tools\rtk は古い重複コピー。再現不要 (整理推奨)。"

# ----------------------------------------------------------------------------
# 5. uv
# ----------------------------------------------------------------------------
Write-Head "5. uv (Python パッケージ/venv マネージャ)"
Step -Name "uv 0.10+" `
     -Check { Test-Cmd 'uv' } `
     -CmdText 'irm https://astral.sh/uv/install.ps1 | iex' `
     -Run { Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression }

# ----------------------------------------------------------------------------
# 6. global npm 6 本
# ----------------------------------------------------------------------------
Write-Head "6. global npm packages (6)"
$npmPkgs = @(
    @{ name = 'Codex CLI';   bin = 'codex';  pkg = '@openai/codex' },
    @{ name = 'zx (ccr 依存)'; bin = 'zx';    pkg = 'zx' },
    @{ name = 'Copilot CLI'; bin = 'copilot'; pkg = '@github/copilot' },
    @{ name = 'Gemini CLI';  bin = 'gemini'; pkg = '@google/gemini-cli' },
    @{ name = 'mermaid-cli'; bin = 'mmdc';   pkg = '@mermaid-js/mermaid-cli' },
    @{ name = 'bun';         bin = 'bun';    pkg = 'bun' }
)
foreach ($p in $npmPkgs) {
    Step -Name $p.name `
         -Check { Test-Cmd $p.bin }.GetNewClosure() `
         -CmdText "npm i -g $($p.pkg)" `
         -Run { & npm i -g $p.pkg }.GetNewClosure()
}

# ----------------------------------------------------------------------------
# 7. ★torch cu128 (freeze より前)
# ----------------------------------------------------------------------------
Write-Head "7. ★torch cu128 (Blackwell sm_120 / freeze の +cpu は使わない)"
$torchCu = ''
try { $torchCu = (& py -3.11 -c "import torch;print(torch.version.cuda)" 2>$null) } catch {}
Step -Name "torch (cu128)" `
     -Check { $torchCu -and ($torchCu.Trim() -ne 'None') -and ($torchCu.Trim() -ne '') } `
     -CmdText "py -3.11 -m pip install torch --index-url https://download.pytorch.org/whl/cu128" `
     -Run { & py -3.11 -m pip install torch --index-url https://download.pytorch.org/whl/cu128 }
if ($Execute) {
    Write-Host "   検証: get_device_capability() == (12, 0) を確認"
    try { & py -3.11 -c "import torch;print('cuda=',torch.version.cuda,'cap=',torch.cuda.get_device_capability() if torch.cuda.is_available() else 'NO-CUDA')" } catch {}
} else {
    Write-Host "   [plan] 導入後に: py -3.11 -c `"import torch;print(torch.cuda.get_device_capability())`"  # (12,0) 期待"
}

# ----------------------------------------------------------------------------
# 8. FullSense editable (D: 上コードから / extras 明示)
# ----------------------------------------------------------------------------
Write-Head "8. FullSense projects editable install (D: travels 済コードから)"
Write-Host "   ※ torch を 7 で cu128 にした後に実行 (extras の torch が cu128 と整合)。"
Write-Host "   ※ fullsense は packaging ファイル無し = py3.11 グローバル env に直依存 (独立 venv 無し)。"
$editables = @(
    @{ name='llcore'; spec='D:/projects/llcore[z3,sdp,chat,clip,text,ann,dev]' },
    @{ name='llive';  spec='D:/projects/llive[torch,ingest,llm,mcp,vlm,dev]' },
    @{ name='llmesh'; spec='D:/projects/llmesh[claude,industrial]' },
    @{ name='llove';  spec='D:/projects/llove[gui]' },
    @{ name='llterm'; spec='D:/projects/llterm' },
    @{ name='llloop'; spec='D:/projects/llloop' }
)
foreach ($e in $editables) {
    $dir = ($e.spec -split '\[')[0]
    Step -Name "$($e.name) (editable)" `
         -Check { -not (Test-Path $dir) }.GetNewClosure() `
         -CmdText "py -3.11 -m pip install -e `"$($e.spec)`"" `
         -Run { & py -3.11 -m pip install -e $e.spec }.GetNewClosure()
}
Write-Host ""
Write-Host "   [manual] rust 拡張 (llmesh-rust cp311-abi3 / llive rust_ext): freeze の wheel は D: travels。"
Write-Host "            新機 py3.11 で ABI 不整合なら maturin で rebuild:"
Write-Host "            cd D:/projects/llmesh/rust_ext; maturin develop --release  (llive も同様)"
$script:Manual++

# ----------------------------------------------------------------------------
# 9. freeze 差分補完 (案内)
# ----------------------------------------------------------------------------
Write-Head "9. freeze 差分補完 (leaf ツール回収)"
Manual -Name "pip freeze 差分" -Text @"
正本 = D:/projects/fullsense/docs/research/migration_pip_freeze_py311_2026-06-28.txt (216 行)。
★ torch==*+cpu 行と -e/file:// 行を除外してから補完すること:
  (a) 入れ忘れ検出のみ: py -3.11 -m pip check
  (b) leaf を一括補完 (除外フィルタ後): py -3.11 -m pip install -r <filtered.txt>
  回収対象 leaf 例: twine/build/kaggle/cyclonedx-python-lib/pip_audit/bandit/maturin/ruff/mypy など。
freeze の -e git+ssh:// 行 (llmesh/llive/llove/llterm/lleval/md-tree-viewer/usv-pandas-bridge) は
§8 の D: editable で代替済 (ssh/network 不要)。
"@

# ----------------------------------------------------------------------------
# 10. semgrep (py3.14)
# ----------------------------------------------------------------------------
Write-Head "10. semgrep (raptor /scan / py3.14 別 env)"
$hasSemgrep = $false
try { $hasSemgrep = [bool](& py -3.14 -m semgrep --version 2>$null) } catch {}
Step -Name "semgrep 1.161" `
     -Check { $hasSemgrep -or (Test-Cmd 'semgrep') }.GetNewClosure() `
     -CmdText "py -3.14 -m pip install semgrep" `
     -Run { & py -3.14 -m pip install semgrep }
Write-Host "   [warn] semgrep を PATH へ (C:\Python314\Scripts)。MCP 'semgrep mcp' が解決に要る。"
Write-Host "   [warn] 現機の C:\Users\puruy\.semgrep\settings.yml は破損 (先頭 null byte)。移送せず新機で再生成。"

# ----------------------------------------------------------------------------
# 11. scholar-search-mcp (py3.11)
# ----------------------------------------------------------------------------
Write-Head "11. scholar-search-mcp (MCP scholar-search / py3.11 常駐)"
$hasScholar = $false
try { & py -3.11 -c "import scholar_search_mcp" 2>$null; $hasScholar = ($LASTEXITCODE -eq 0) } catch {}
Step -Name "scholar-search-mcp 0.1.3" `
     -Check { $hasScholar }.GetNewClosure() `
     -CmdText "py -3.11 -m pip install scholar-search-mcp" `
     -Run { & py -3.11 -m pip install scholar-search-mcp }

# ----------------------------------------------------------------------------
# 12. MCP ランタイム (osv-mcp uv sync + uvx pre-warm)
# ----------------------------------------------------------------------------
Write-Head "12. MCP ランタイム"
Step -Name "osv-mcp venv (uv sync)" `
     -Check { Test-Path 'D:\tools\osv-mcp\.venv\Scripts\python.exe' } `
     -CmdText "cd D:/tools/osv-mcp; uv sync" `
     -Run { Push-Location 'D:/tools/osv-mcp'; try { & uv sync } finally { Pop-Location } }
Write-Host "   [warn] osv-mcp の .venv は pyvenv.cfg が死に C: パス (uv py3.13) を指す → uv sync で再生成 (ネット必須)。"
Manual -Name "uvx/npx pre-warm (任意)" -Text @"
.claude.json コピーで wiring は再現するが uvx/npx キャッシュは C: 常駐=travels せず。
初回起動時に PyPI/npm から自動取得 (ネット必須)。事前 warm するなら:
  uvx mcp-server-fetch --help ; uvx mcp-server-sqlite --help ; uvx arxiv-mcp-server --help
  uvx alpaca-mcp-server --help ; uvx duckduckgo-mcp-server --help ; uvx mediawiki-mcp-server --help
github PAT (失効なら再発行) / firecrawl の FIRECRAWL_API_KEY 出所 (config env 空=要確認) /
claude.ai コネクタ (Google Drive/PDF Viewer/Claude Design) は新機ログイン後に再認可。
"@

# ----------------------------------------------------------------------------
# 13. Ollama + models
# ----------------------------------------------------------------------------
Write-Head "13. Ollama (本体 + 5 モデル 26.30GB)"
Step-Winget -Name "Ollama 本体" -CmdName 'ollama' -WingetId 'Ollama.Ollama'
$models = @('qwen2.5:14b','qwen2.5:7b','llama3.2-vision:latest','llava:7b','llama3.2:latest')
if ($SkipOllamaModels) {
    Write-Host "   [skip] -SkipOllamaModels 指定 — モデル pull を省略 (.ollama を D: 経由 copy する場合)"
} else {
    foreach ($m in $models) {
        Step -Name "ollama pull $m" `
             -Check { $false }.GetNewClosure() `
             -CmdText "ollama pull $m" `
             -Run { & ollama pull $m }.GetNewClosure()
    }
    Write-Host "   [warn] 計 26.30GB。回線次第では C:\Users\puruy\.ollama\models を D: 経由 copy が速い。"
}

# ----------------------------------------------------------------------------
# 14. browser-use 別 venv
# ----------------------------------------------------------------------------
Write-Head "14. browser-use-project (uv 別 venv / py3.12 / 101 pkgs)"
Step -Name "browser-use uv sync" `
     -Check { Test-Path 'C:\Users\puruy\browser-use-project\.venv\Scripts\python.exe' } `
     -CmdText "cd C:/Users/puruy/browser-use-project; uv sync" `
     -Run { Push-Location 'C:/Users/puruy/browser-use-project'; try { & uv sync } finally { Pop-Location } }
Write-Host "   [warn] uv.lock 存在。初回 playwright ブラウザ実体 DL あり (ネット必須)。"
Write-Host "   [warn] live state (alpaca_state.json) は C: 常駐 = restore_working_set.ps1 で別途復元。"

# ----------------------------------------------------------------------------
# 15. ccr node-pty
# ----------------------------------------------------------------------------
Write-Head "15. ccr node-pty (D: travels / ABI 確認)"
Write-Host "   node-pty 実体 = D:/tools/raptor/node_modules (D: 側)。Node v24 維持なら rebuild は fallback。"
if ($Execute) {
    Write-Host "   [run] ロード確認:"
    Push-Location 'D:/tools/raptor'
    try {
        & node -e "require('@homebridge/node-pty-prebuilt-multiarch');console.log('node-pty load OK')"
        if ($LASTEXITCODE -ne 0) {
            Write-Host "   [warn] ロード失敗 → rebuild が要る: npm rebuild @homebridge/node-pty-prebuilt-multiarch"
            Write-Host "          (VS Build Tools C++ + Python が必要)"
        }
    } catch { Write-Host "   [warn] node 未解決か D: 未マウント" }
    finally { Pop-Location }
} else {
    Write-Host "   [plan] cd D:\tools\raptor; node -e `"require('@homebridge/node-pty-prebuilt-multiarch')`""
    Write-Host "          通れば rebuild 不要。失敗時のみ: npm rebuild @homebridge/node-pty-prebuilt-multiarch"
}

# ----------------------------------------------------------------------------
# 16. 対話・secret (manual 集約)
# ----------------------------------------------------------------------------
Write-Head "16. 対話・secret 再設定 (自動実行しない — 手動)"
Manual -Name "Claude Code (native)" -Text "native installer で導入し claude 再ログイン (global npm 版ではない)。.credentials.json は端末紐づき=再ログイン前提。"
Manual -Name "gh auth login"        -Text "gh auth login で再認証 (hosts.yml コピーでも再 auth 推奨)。"
Manual -Name "Codex login"          -Text "@openai/codex は §6 で導入済。.codex\ (config.toml/auth.json) を restore_working_set で復元 or codex login。"
Manual -Name "User env secret 3"    -Text "ANTHROPIC_API_KEY / TELEGRAM_BOT_TOKEN / SOCIALDATA_API_KEY を setx で再設定 (移行を機に再発行推奨)。ファイルでない=travels で拾えない。"
Manual -Name "User PATH"            -Text ".local\bin / .cargo\bin / AppData\Roaming\npm / Ollama / (任意) C:\Python314\Scripts を PATH へ。reference export から再構築。"

# ----------------------------------------------------------------------------
# summary
# ----------------------------------------------------------------------------
Write-Head "サマリ"
Write-Host ("  skip (既存)   : {0}" -f $script:Skipped)
if ($Execute) {
    Write-Host ("  run  (実行)   : {0}" -f $script:Ran)
} else {
    Write-Host ("  plan (要導入) : {0}   ← -Execute で実行" -f $script:Planned)
}
Write-Host ("  manual (手動) : {0}" -f $script:Manual)
Write-Host ""
Write-Host "  次手: verify_new_machine.ps1 で全項目 PASS を確認 → 初手 GPU ワークロード (--device cuda)。"
if (-not $Execute) {
    Write-Host ""
    Write-Host "  ※ これは dry-run です。レビュー後 -Execute を付けて再実行してください。"
}
