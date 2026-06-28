# 移行 依存物インベントリ — 新機 C: に「要再インストール物」の正本(2026-06-28)

> 4 つの実環境実測インベントリ(Python / システムツール / MCP サーバ / ccr・node-pty・rtk・Ollama)を統合。
> **目的** = D: を外付け本体ごと物理移送(travels)した後、**C: にグローバル導入された実行体だけ**を漏れなく再インストールする台帳。
> **正本(突き合わせ先)**: `gpu_pc_migration_plan_2026-06-28.md` §4 / `migration_manifest_2026-06-28.md` §3・§4。
> **付属スクリプト**: `D:/projects/fullsense/tools/migration/bootstrap_install.ps1`(本 doc §5 の順序を実装。**レビュー必須・dry-run 既定**)。
> **freeze 正本(差分照合先)**: `D:/projects/fullsense/docs/research/migration_pip_freeze_py311_2026-06-28.txt`(py3.11 / 216 行)。
>
> すべて read-only 実測(install/削除なし・git 操作なし)。バージョン・実体パス・インストール元は 2026-06-28 の現ノート(HP i7-1065G7 / GPU 無し / Win11 Pro)で採取。

---

## (0) 方針 — D: travels で「不要」と「要再インストール」の境界

新機は **D: を外付け SSD 本体ごと物理接続しレター D: を温存**する(plan §2 / manifest §2)。よって:

- **不要(D: 配下=travels)**: コード本体(`D:/projects/*`・`D:/tools/raptor`・`D:/docs`(RAD)・`D:/api-keys.json`)、`D:/tools/raptor/node_modules`(ccr の node-pty もここ=D: 側)、`D:/tools/osv-mcp` repo、`D:/tools/raptor-analytics.db`。**ファイルは運ばれる**。
- **要再インストール(C: 常駐の実行体=本 doc の主題)**: グローバル Python パッケージ(py3.11/3.14 の site-packages)、CLI(node/git/gh/rustup/cargo/rtk/uv/semgrep/Claude/Codex/Ollama)、グローバル npm 6 本、MCP サーバのランタイム実体(uvx/npx キャッシュ・pip 常駐分)。**これらは C: に居るので travels で拾えず、新機で入れ直す**。
- **要再ビルド/再生成(ABI/interpreter 依存)**: ccr の node-pty(native ABI)、rust 拡張(llmesh-rust / llive rust_ext)、osv-mcp の `.venv`(pyvenv.cfg が死に C: パスを指す)。

> **罠の核心**: D: travels で「動くはず」と錯覚しやすいが、**native binding / venv interpreter / グローバル site-packages は C: に紐づく**。これらが本 doc の回収対象。

---

## (1) Python 依存 — torch cu128 を筆頭に、必須 vs optional の階層

### 1-A. ★最重要: torch は freeze の `+cpu` を絶対に使わない

実測(py3.11): **`torch==2.12.0+cpu`** / `torch.version.cuda=None` / `cuda.is_available()=False` = **CPU ビルド確定**。freeze をそのまま `pip install -r` すると Blackwell で動かない CPU 版が入り `no kernel image` になる。

```powershell
# ★必ず freeze より先に、cu128 index で torch を固定する
py -3.11 -m pip install torch --index-url https://download.pytorch.org/whl/cu128
py -3.11 -c "import torch; print(torch.cuda.get_device_capability())"   # (12, 0) を確認
```

(plan §4-4 の「現 CPU torch 2.12」表記は実測 `2.12.0+cpu` で正確。cu128 必須・cu124 不可も §4 と一致。)

### 1-B. 必須 vs optional の階層表(実測版)

| 層 | パッケージ(実測版) | 利用元 | 入れ方 |
|---|---|---|---|
| **基盤(必須)** | numpy 2.4.4 | 全 project コア | pip(最初) |
| **GPU 本走(★別 index 先入れ)** | torch 2.12.0(→cu128 に置換) | llcore[chat/clip] / llive[torch] | 1-A の cu128 経路 |
| **重 ML(optional・torch 後)** | transformers 5.10.2 / sentence-transformers 5.5.1 / faiss-cpu 1.14.2 / accelerate / peft / hdbscan / tokenizers 0.22.2 / safetensors 0.7.0 | llcore[chat/clip/text/ann] / llive[torch] | torch の後に pip |
| **SMT / 最適化(llive=必須/他=optional)** | z3-solver 4.16.0.0 / cvxpy 1.9.1(+clarabel 0.11.1/osqp/scs/qdldl/highspy) / onnx 1.21.0 | z3=llive コア必須・raptor SMT / cvxpy=llcore[sdp] | pip。★cvxpy は memory `cvxpy_pin_accurate_solver`= **CLARABEL 固定** |
| **GUI(llterm=必須/llove=optional)** | PySide6 6.11.1(+shiboken6/Addons/Essentials)/ pyqtgraph 0.14.0 / textual 8.2.5 / rich 15.0.0 | llterm コア=PySide6 必須 / llove[gui] / llove コア=textual | pip(重) |
| **MCP / LLM(用途必須)** | mcp 1.27.1 / anthropic 0.100.0 | llmesh[claude] / llive[mcp,llm] / mcp-3d / raptor | pip |
| **Web/サーバ(llmesh=必須)** | fastapi 0.136.1 / uvicorn 0.46.0 / cryptography 48.0.0 / duckdb 1.5.2 / kuzu 0.11.3 / sympy 1.14.0 | llmesh コア / llive コア | pip |
| **科学/文書(用途依存)** | scipy 1.17.1 / scikit-learn 1.8.0 / pandas 3.0.3 / pillow 12.2.0 | llmesh[industrial] / mcp-3d / usv-pandas-bridge / vlm | pip |
| **単発ツール(leaf)** | twine 6.2.0 / build 1.5.0 / kaggle 2.2.1 / cyclonedx-python-lib 11.7.0 / pip_audit 2.10.0 / bandit 1.9.4 / maturin 1.13.1 / ruff 0.15.12 / mypy 2.0.0 | CI/配布/SCA | freeze 差分で回収 |
| **別 env(py3.14)** | semgrep 1.161.0 | raptor `/scan` | **`py -3.14 -m pip install semgrep`** |

### 1-C. 各プロジェクトの宣言依存(pyproject 実測 — editable 再構築の意図を保つ材料)

**コアは stdlib+numpy 方針が貫徹**(CLAUDE.md「基本 stdlib+numpy・重いものは optional」と合致):

| project | コア依存(必須) | extras(optional) |
|---|---|---|
| **llcore** | `numpy>=1.26` のみ | `z3` / `sdp`(cvxpy) / `chat`(torch,transformers) / `clip`(+pillow) / `text`(sentence-transformers) / `ann`(faiss-cpu) / `llive` / `dev` |
| **llive** | z3-solver / kuzu / duckdb / cryptography / sympy 等(★コアに重め) | `torch`(torch,transformers,accelerate,sentence-transformers,faiss-cpu,peft,hdbscan) / `ingest` / `llm`(anthropic) / `rust`(maturin) / `mcp` / `vlm`(pillow) / `coding` / `dev` |
| **llmesh** | cryptography / jsonschema / base58 / fastapi / uvicorn[standard] | `claude`(mcp) / `industrial`(pymodbus,pyserial,asyncua,paho-mqtt) / `msgpack` / `localfile` / `vision` / `udp` / `ssh` / `email` / `ftp` / `mgmt` / `dev` |
| **llove** | textual / rich / click / pydantic | `gui`(PySide6,pyqtgraph) / `plots` / `llmesh` / `shogi` / `chess` |
| **llterm** | `PySide6>=6.6`(★コア必須) | `dev` |
| **llloop** | `[]`(stdlib のみ) | `dev` |
| **lltrade** | `[]` | — |
| **fullsense** | **packaging ファイル無し**(pyproject/requirements/setup.py 不在) | — |

> ★**fullsense は独立 venv が存在しない** = py3.11 グローバル env に直依存(editable 同梱の llmesh/llive/llove + freeze の leaf 群)。**fullsense の復元 ≡ py3.11 グローバル env の再現**。plan §4-5「各 project を pyproject から venv 再生成」は fullsense には適用できない点を移行手順に明記すべき(→ §6 差分)。
>
> **rust 拡張**: freeze に `llmesh-rust @ file:///D:/.../cp311-abi3-win_amd64.whl` と `-e git+ssh://.../llive rust_ext` あり。前者の wheel は D: 上=travels だが、**新機 Python マイナー差異 / ABI 不整合時は maturin で rebuild**(node-pty と同種の native ABI 問題)。

### 1-D. 再現方針 = ★ハイブリッド(freeze 一括 `-r` 単独は非推奨)

**結論: freeze.txt は「インベントリ正本 / 移行後の差分検証(入れ忘れ検出)」に使い、再構築は torch 特別扱い → D: 上 editable → freeze で leaf 差分補完、の順。** 根拠(実測):

1. **torch +cpu 罠**(1-A)。freeze の `torch==2.12.0+cpu` 行は cu128 経路と相反 → 必ず除外。
2. **editable/git/local-wheel 行が replay 不可**: freeze 内に `-e git+ssh://...`(llmesh/llive/llove/llterm/lleval/md-tree-viewer/usv-pandas-bridge)、`file:///D:/...whl`、`-e d:\projects\llloop` が多数(freeze 78–87・93・207 行目)。ssh 認証・network・rust 再ビルド依存でクリーンに流れない → **D: travels で実体がある今、ローカルパスから editable install する方が確実**。

推奨手順は §5 に統合。各 pyproject の extra 設計が綺麗で「必須 vs optional」が明示されているため、editable 再構築の方が意図(どの extra を入れるか)を保てる。

### 1-E. その他の Python 環境(実測)

- **py3.14**: 223 pkgs だが実質 **semgrep 1.161.0 専用**(+numpy/requests/setuptools)。`C:/Python314` 実体。→ `py -3.14 -m pip install semgrep`。
- **py3.9**(`C:/Python39`): **0 pkgs**(freeze 空)= 実質未使用 → **移行不要**。
- **uv 管理 Python**: 3.14.3 / 3.13.12 / 3.12.13 / 3.11.3 / 3.9.7 が C: 常駐。`browser-use-project` は uv venv(py3.12)。→ uv 再導入 + `uv sync`。

---

## (2) システムツール(CLI / ランタイム)

| ツール | 現バージョン | 実体パス | 新機での入れ方 |
|---|---|---|---|
| node | v24.14.0 | `C:\Program Files\nodejs\node.exe` | `winget install OpenJS.NodeJS.LTS`(★v24 系。**node-pty engines `<25.0.0` → v25+ 禁止**) |
| npm | 11.9.0 | Node 同梱 | — |
| git | 2.42.0.windows.2 | `C:\Program Files\Git\cmd\git.exe` | `winget install Git.Git`(Git Bash 同梱) |
| gh | 2.88.1 | `C:\Program Files\GitHub CLI\gh.exe` | `winget install GitHub.cli`(再 auth は対話=手動) |
| rustc / cargo / rustup | 1.94.1(stable-x86_64-pc-windows-msvc 単一) | `C:\Users\puruy\.cargo\bin\` | `winget install Rustlang.Rustup` → `rustup default stable` |
| **rtk** | v0.34.1(git rtk-ai/rtk#6444c4b0) | 実体=`C:\Users\puruy\.cargo\bin\rtk.exe`(6.76MB)/ `C:\tools\rtk\rtk.exe`(8.28MB=**別ビルドの古い重複**) | **`cargo install --git https://github.com/rtk-ai/rtk --rev 6444c4b018f5619ab2a441191534937894b17970`**。`C:\tools\rtk` は再現不要 |
| uv | 0.10.12 | `C:\Users\puruy\.local\bin\uv.exe` | `irm https://astral.sh/uv/install.ps1 \| iex` |
| semgrep | 1.161.0 | `C:\Python314\Scripts\semgrep.exe`(py3.14) | `py -3.14 -m pip install semgrep` + PATH |
| 7-Zip | 26.00 | `C:\Program Files\7-Zip\7z.exe`(★**PATH 未登録**) | `winget install 7zip.7zip` + **PATH 登録**(`migrate_secrets.ps1` が 7z AES-256 に依存) |
| Claude Code | native(npm 非経由) | `C:\Users\puruy\.local\bin\claude.exe` | **native installer**(global npm に不在で正)+ 再ログイン(対話=手動) |
| Codex CLI | 0.135.0 | `C:\Users\puruy\AppData\Roaming\npm\codex.ps1`(**global npm**) | **`npm i -g @openai/codex`**(`.codex\` config/auth は §3 で copy) |
| Ollama | 0.30.11 | `C:\Users\puruy\AppData\Local\Programs\Ollama\ollama.exe` | `winget install Ollama.Ollama` + モデル再 pull(§4) |
| codeql | **未導入**(NOT FOUND) | — | 未導入で manifest と一致。必要時に導入 |
| py launcher | 既定 3.11(+3.14/3.13/3.12/3.9) | `C:\WINDOWS\py.exe`(`python`=3.14.3) | python.org installer + uv |

- **uv tool list = 空** / **pipx 未導入** / **PSGallery モジュール = 空**(`Get-InstalledModule` 空)→ これら経由の追加移行物は **無し**。
- **winget 管理の dev 関連(参考)**: MSYS2(`MSYS2.MSYS2`・PATH 常駐 `C:\tools\msys64`)/ Neovim(`C:\tools\neovim`)/ Docker Desktop(`Docker.DockerDesktop`)/ Pandoc(`JohnMacFarlane.Pandoc`)/ Chafa(`hpjansson.Chafa`・端末画像)/ gsudo。manifest §3 未記載 → 必要に応じ追記候補(コア依存は msys64 が PATH 常駐の点に注意)。

---

## (3) MCP サーバ 導入レシピ

設定本体 = `C:/Users/puruy/.claude.json`(MCP 配線・inline secret の本体、`.claude\` の **外**)。**top-level をコピーすれば wiring・inline secret(ALPACA/PERPLEXITY/github PAT)・project 別定義は全て再現**。ただし **コピーは配線のみ** — ランタイム実体(pip 常駐/venv/キャッシュ)は別途要る。

### 3-A. グローバル MCP(10 本・全 project 共通)

| server | 起動方式 | ランタイム実体 | 新機で要る作業 |
|---|---|---|---|
| github | http + Bearer PAT(inline) | リモート(ローカル実体なし) | 不要。**PAT 失効なら再発行** |
| osv-mcp | `uv --directory D:/tools/osv-mcp run osv-server` | D: 上 repo + `.venv`(★pyvenv.cfg が **死に C: パス** `…uv\python\cpython-3.13`) | **`cd D:/tools/osv-mcp; uv sync`**(venv 再生成・ネット必須) |
| semgrep | `semgrep mcp` | `C:/Python314/Scripts/semgrep`(C: 常駐) | **`py -3.14 -m pip install semgrep`** + PATH |
| sqlite | `uvx mcp-server-sqlite --db-path D:/tools/raptor-analytics.db` | PyPI(uv キャッシュ=C: 常駐)。DB は D: travels | 初回 uvx で自動取得(ネット必須)。任意 pre-warm |
| fetch | `uvx mcp-server-fetch` | PyPI(uvx) | 同上 |
| calil | http(auth なし) | リモート | 不要 |
| arxiv | `uvx arxiv-mcp-server` | PyPI(uvx) | 初回自動取得 |
| filesystem | `npx -y @modelcontextprotocol/server-filesystem D:/docs D:/projects` | npm(npm-cache=C: 常駐) | 初回 npx 自動取得 |
| scholar-search | `py -3.11 -m scholar_search_mcp` | **pip→py3.11 常駐**(`scholar-search-mcp 0.1.3`、freeze 167 行) | **`py -3.11 -m pip install scholar-search-mcp`** |
| firecrawl | `npx -y firecrawl-mcp` | npm。**env `{}` 空** | 初回 npx 自動取得。★**FIRECRAWL_API_KEY の出所要確認**(config に無い=別 env 依存の疑い) |

### 3-B. プロジェクト限定 MCP(`C:/Users/puruy/browser-use-project` 起動時のみ・7 本)

alpaca(`uvx alpaca-mcp-server`・鍵 inline)/ playwright(`npx @playwright/mcp`・初回ブラウザ DL)/ fetch / sqlite(`--db-path D:/trading_data.db`)/ duckduckgo / wikipedia(`uvx mediawiki-mcp-server`)/ perplexity(`npx @perplexity-ai/mcp-server`・鍵 inline)。**いずれも uvx/npx で初回自動取得**。鍵は `.claude.json` 内 travels だが **ローテ推奨**。

### 3-C. claude.ai 管理リモート MCP(`.claude.json` に**無い**)

`claudeAiMcpEverConnected` = Google Drive / PDF Viewer / Claude Design。claude.ai アカウント側コネクタ=ローカル実体なし → **`.claude.json` コピーでは復元されず、新機ログイン後に再認可(手動)**。

### 3-D. config copy で済む vs 手再設定が要る

`.claude.json` コピーで wiring は再現。**別途必要(ランタイム)**: ① `py -3.11 -m pip install scholar-search-mcp` ② `py -3.14 -m pip install semgrep`+PATH ③ `cd D:/tools/osv-mcp; uv sync` ④ uv+Node を PATH に+初回 uvx/npx 自動取得(キャッシュは C: 常駐で travels せず=ネット必須。pre-warm 候補: mcp-server-fetch / mcp-server-sqlite / arxiv-mcp-server / alpaca-mcp-server / duckduckgo-mcp-server / mediawiki-mcp-server)⑤ claude.ai コネクタ再認可 ⑥ github PAT 失効なら再発行 ⑦ firecrawl 鍵の出所確認。

---

## (4) ccr / node-pty / rtk / Ollama / その他グローバル

### 4-A. ccr / node-pty / zx
- ccr 起動体 `D:/tools/raptor/bin/ccr.ps1`(`& zx claude-auto.mjs @args`)= **D: travels**。`D:\tools\raptor\bin` は PATH 登録済(travels)。
- **zx は C: 常駐 global npm**(`zx.ps1` v8.8.5)。ccr の package.json 依存は node-pty のみで **zx は宣言外** → **`npm i -g zx` を明記**。
- node-pty = `@homebridge/node-pty-prebuilt-multiarch@^0.13.1`、実体は **`D:/tools/raptor/node_modules/`(D: travels・C: 側ではない)**。Windows native binding は `build/Release/{pty,conpty,conpty_console_list}.node`(node-gyp 生成・ABI 137=Node 24)。**現 Node v24 で `require()` ロード成功を実証済**。
  - → **Node v24 を維持する限り `npm rebuild` は no-op(fallback)で済む公算**。Node メジャーが変わる前提でのみ必須。判定: `cd D:\tools\raptor; node -e "require('@homebridge/node-pty-prebuilt-multiarch')"` が通れば rebuild 不要。
  - ★**node-pty 0.13.1 engines = `node >=18.0.0 <25.0.0` → Node v25+ は拒否**。v24 固定を明記すべき。

### 4-B. rtk
- PATH 解決実体 = `.cargo\bin\rtk.exe`(v0.34.1・cargo install 由来・shim でなく完全バイナリ)。`C:\tools\rtk\rtk.exe` は別ビルドの古い重複(PATH 後順・不使用)。
- 由来 = `cargo install --git https://github.com/rtk-ai/rtk`(`.crates.toml` で `git+https://github.com/rtk-ai/rtk#6444c4b0…` 確定)。**D: にソースは無く、リモート git 固定 commit が真ソース**。
- → 再現: `cargo install --git https://github.com/rtk-ai/rtk --rev 6444c4b018f5619ab2a441191534937894b17970`。`C:\tools\rtk` は再現不要(整理推奨)。

### 4-C. Ollama
- 本体 v0.30.11(C: 常駐)→ `winget install Ollama.Ollama`。
- モデル `C:\Users\puruy\.ollama\models` = **合計 26.30GB / 5 モデル**: qwen2.5:14b(9.0GB)/ qwen2.5:7b(4.7GB)/ llama3.2-vision:latest(7.8GB)/ llava:7b(4.7GB)/ llama3.2:latest(2.0GB)。**manifest §1 は HF cache 9G のみ計上で .ollama 26GB 未計上=要追記**。再 pull 可だが 26GB=回線次第で `.ollama\models` を D: 経由 copy が速い。

### 4-D. グローバル npm(6 本・全て C: 常駐 `AppData\Roaming\npm`)
`npm i -g @openai/codex zx @github/copilot @google/gemini-cli @mermaid-js/mermaid-cli bun`
- @openai/codex 0.135.0(Codex CLI)/ zx 8.8.5(ccr 依存)/ @github/copilot 1.0.56(`copilot_review.sh`)/ @google/gemini-cli 0.46.0(外部 AI 検証)/ @mermaid-js/mermaid-cli 11.14.0(/diagram)/ bun 1.3.11。

---

## (5) ★インストール順序(新機 Day-of)

> 実装 = `D:/projects/fullsense/tools/migration/bootstrap_install.ps1`(dry-run 既定 / `-Execute` で実行)。対話・secret 系は案内のみ(自動実行しない)。

1. **GPU 基盤**: NVIDIA driver **R570+**(Blackwell sm_120)→ 再起動。
2. **D: 温存確認**: `Test-Path D:\tools\raptor`(true 必須。false なら以降中止)。
3. **base CLI(winget)**: `Git.Git` / `OpenJS.NodeJS.LTS`(★v24・<25 厳守)/ `GitHub.cli` / `7zip.7zip`(+PATH)/ `Rustlang.Rustup` → `rustup default stable`。
4. **rtk**: `cargo install --git https://github.com/rtk-ai/rtk --rev 6444c4b0…`。
5. **uv**: `irm https://astral.sh/uv/install.ps1 | iex`。
6. **global npm 6 本**: `npm i -g @openai/codex zx @github/copilot @google/gemini-cli @mermaid-js/mermaid-cli bun`。
7. **★torch cu128(freeze より前)**: `py -3.11 -m pip install torch --index-url https://download.pytorch.org/whl/cu128` → `get_device_capability()==(12,0)` 検証。
8. **FullSense editable(D: travels 済コードから)**:
   - `py -3.11 -m pip install -e "D:/projects/llcore[z3,sdp,chat,clip,text,ann,dev]"`
   - `py -3.11 -m pip install -e "D:/projects/llive[torch,ingest,llm,mcp,vlm,dev]"`
   - `py -3.11 -m pip install -e "D:/projects/llmesh[claude,industrial]"`
   - `py -3.11 -m pip install -e "D:/projects/llove[gui]" -e D:/projects/llterm -e D:/projects/llloop`
   - rust 拡張(llmesh-rust / llive rust_ext)は ABI 不整合時のみ maturin で rebuild。
9. **freeze 差分補完**(leaf ツール回収): `migration_pip_freeze_py311_2026-06-28.txt` から **`torch==*+cpu` 行と `-e`/`file://` 行を除外**して `pip install -r`、または `pip check` で入れ忘れ検出。
10. **semgrep(別 env)**: `py -3.14 -m pip install semgrep` + PATH。
11. **scholar-search-mcp**: `py -3.11 -m pip install scholar-search-mcp`。
12. **MCP ランタイム**: `cd D:/tools/osv-mcp; uv sync` / uvx pre-warm(任意)。
13. **Ollama**: `winget install Ollama.Ollama` → 5 モデル `ollama pull`(or .ollama copy)。
14. **browser-use 別 venv**: `cd C:/Users/puruy/browser-use-project; uv sync`(uv.lock・py3.12・101 pkgs)。
15. **ccr**: node-pty ロード確認(`node -e "require('@homebridge/node-pty-prebuilt-multiarch')"`)→ 失敗時のみ `npm rebuild`。
16. **対話・secret(手動)**: gh `auth login` / Codex login(or `.codex\` copy)/ Claude Code native installer + 再ログイン / claude.ai コネクタ再認可 / github PAT・firecrawl 鍵確認 / User env 3 secret(`ANTHROPIC_API_KEY`/`TELEGRAM_BOT_TOKEN`/`SOCIALDATA_API_KEY`)再設定・再発行。

---

## (6) manifest §3 / plan §4 へ追記すべき差分(訂正提案)

1. **【誤り】rtk 実体が逆**: §3「実体 `C:/tools/rtk/rtk.exe`(+`.cargo/bin` shim)」→ 実測は逆。**現用は `.cargo/bin/rtk.exe`(cargo install v0.34.1)**、`C:/tools/rtk` は古い重複。再現は `cargo install --git ... --rev 6444c4b0…` だけで完結(「build→C:/tools/rtk 配置」は不要)。
2. **【漏れ】global npm 5 本**: §3 は Codex のみ言及。**copilot / gemini-cli / mermaid-cli / bun / zx が未掲載**(copilot=`copilot_review.sh` 前提、gemini-cli=外部 AI 検証、mermaid-cli=/diagram 必須)。
3. **【漏れ】7-Zip がツール表に無い**: `migrate_secrets.ps1`(7z AES-256 `-mhe=on`)が依存。実体 v26.00 だが **PATH 未登録**=`7z` 直叩き不可 → winget + PATH 登録 or フルパス参照に修正。
4. **【誤り/補正】node-pty は C: でなく D:**: §3「node-pty は C: 側 node_modules / npm rebuild 必須」→ **実体は `D:/tools/raptor/node_modules`(travels)で現 Node v24 上ロード実証済**。rebuild は **Node v24 維持なら fallback**。engines `<25.0.0` ゆえ **Node v25+ 禁止**を明記。
5. **【漏れ】Ollama models 容量**: §1/§2-B「9G(HF のみ)」→ **`.ollama` 実測 26.30GB / 5 モデル**を追記(qwen2.5:14b/7b・llama3.2-vision・llava:7b・llama3.2)。
6. **【補正】Codex 再導入の具体**: §3「Codex CLI 再導入」→ **`npm i -g @openai/codex@0.135.0`(npm global)**。
7. **【漏れ】fullsense は packaging ファイル無し**: plan §4-5「各 project を pyproject から venv 再生成」は fullsense に適用不可。**fullsense 復元 ≡ py3.11 グローバル env の再現**(独立 venv 不在)を手順に明記。
8. **【一致(確認)】**: codeql 未導入 / Claude Code=native / semgrep=py3.14 1.161.0 / node v24・git 2.42・gh 2.88.1・uv 0.10.12 / torch cu128 必須 / MCP は `.claude.json` コピーで wiring 再現 — いずれも §3/§4 と整合。

---

## 確信度・実機で要確認(honest disclosure)

**確信度=高(一次実測で確認)**: 全バージョン・実体パス・インストール元、torch `2.12.0+cpu`、freeze 216 行、各 pyproject の extras 名、global npm 6 本、Ollama 26.30GB、rtk の `.cargo/bin` 実体と git rev、node-pty の D: 実体 + Node v24 ロード成功、py3.9 空 / uv tool list 空 / pipx 未導入 / PSGallery 空。

**実機(新機 GPU 機)で要確認**:
- **torch cu128 が sm_120(12,0)で実際に GEMM を通すか**(`no kernel image` が出たら nightly/cu129 へ)。現機 GPU 無しのため未検証。
- **rust 拡張(llmesh-rust cp311-abi3 / llive rust_ext)が新機 py3.11 でそのままロードできるか**(マイナー差異/ABI で maturin rebuild が要るか)。
- **node-pty が新機 Node v24 で no-op か rebuild 要か**(VS Build Tools C++ + Python が要るのは rebuild 時のみ)。
- **winget `OpenJS.NodeJS.LTS` が v24 を返すか**(v25 を引いたら node-pty engines で弾かれる → `--version 24.x` ピン)。
- **llmesh/llove の extra 取捨**(本 doc は最小集合を提示。`industrial`(pymodbus 等)や `localfile`/`vision` 等は実利用に応じ追加)。
- **FIRECRAWL_API_KEY の供給元**(`.claude.json` の env 空 = 別 env var 依存の疑い)。
- **github PAT の有効性**(失効なら github MCP が落ちる)。
- **browser-use `uv sync` の 101 pkgs 再取得**(playwright ブラウザ実体 DL 含む・ネット必須)。
