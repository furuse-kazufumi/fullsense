# GPU PC 移行計画 (target: 2026-07 中旬 / 2–3 週間先)

> 作成 2026-06-28。前提・確定事項の正本 = memory `project_gpu_pc_consideration_2026_06_21`
> (購入意向確定 2026-06-27) / `feedback_gpu_rent_over_buy`(rent-first を 24/7 研究用途で上書き)
> / `feedback_claude_max_compute_priority`(GPU 投入は decision-relevant な実測を優先)。
> 経済性の旧正本 = `gpu_portfolio_decision_2026-06-02.md`(RENT-FIRST、128GB級向け)。
> 本計画は **24GB 級の自前デスクトップを買って移行する**最新方針に基づく runbook。

## 0. 確定事項(議論済み・蒸し返さない)

- **方針**: 自前 24GB GPU デスクトップを **買って移行**。24/7 専有(ゲームしない・llcore は実験キュー豊富で遊休しない)なら自前が事実上唯一解(クラウド A100 24/7 ≈ 月30万 vs 自前 電気 ~月1万)。128GB級の rent-first 判断はスケールが違うので本件には不適用。
- **CUDA C はほぼ不要**: ①動かす=自前 forward は PyTorch なので `model.to("cuda")` で自動 GPU(cuBLAS/cuDNN)/②高速化=Triton or 既存lib(bitsandbytes / flash-linear-attention / llama.cpp)/③CUDA C 自作は最後の手段で射程外。**forward を PyTorch で書いたことが移植性として効く**。
- **即始動準備済(2026-06-27)**: 自前 forward が HF transformers と golden 一致(CPU 実証)/ 改造①〜④(linearize/quant/loader-mmap/distill)実装 / 正直な評価器 proxy v2 整備。GPU 到来で「黄/赤ブロックを緑にする本走」を即投入可。
- **移行元(実測 2026-06-28)**: HP ノート **i7-1065G7 (4C/8T, 1.3GHz, 15W mobile) / RAM 16GB(オンボード=増設不可)/ Intel Iris(CUDA GPU 無し)/ Win11 Pro**。C: 568/952GB free、D: 1075/1863GB free(used ~788GB)。py: **3.11 が default**(+3.14/3.9/uv 3.12)。**このノートが CPU 本走 6–9h の真因**=流用ゼロ・新規デスクトップ必須。

## 1. ハードウェア(★購入確定 — 注文明細 2026-06-28、組立後出荷待ち)

**arkhive Gaming Limited GL-I7G59M Founders Edition(型番 AG-IA24D2TB86MGB9F-CF4) 税込 ¥978,000**
(<https://www.ark-pc.co.jp/i/72003600/>)。当初推奨(中古3090/4090・24GB)を大きく上回るハイエンド → 開いていたハード判断は**すべて解決**。

| 部品 | 確定スペック | 計画への含意 |
|---|---|---|
| **GPU** | **GeForce RTX 5090 Founders Edition / 32GB GDDR7(Blackwell, sm_120)** | VRAM 32GB = 3B 快適・7–14B fine-tune 可・70B int4 は際どい。★ソフト=**driver R570+ & torch cu128 必須**(§4) |
| **CPU** | **Intel Core Ultra 7 270K Plus**(Arrow Lake, LGA1851)| 旧ノート 15W i7-1065G7 比で桁違い。前処理/データ load も加速 |
| **RAM** | **128GB DDR5-5600(64GB×2 Crucial Pro CL46 EXPO ※OCメモリ)** | 大コーパス前処理・CPU offload に大余裕。★EXPO は AMD 系プロファイル=Intel B860 では XMP/手動で定格化、無ければ JEDEC で動く(BIOS 確認) |
| **マザボ** | **ASRock B860M Steel Legend WiFi(Micro-ATX, WiFi/BT 内蔵)** | M.2 追加スロットあり(後で 2nd SSD = D: 増設可。§2)|
| **SSD** | **2TB NVMe PCIe4.0 x4(Princeton PHD-ISM2G4)1 本のみ・パーティション分割なし** | ★**既定で C: だけ・D: が無い**=パス温存に対策必須(§2)|
| **電源** | **1000W 80+ GOLD(Cooler Master Elite Gold 1000)** | RTX 5090 TGP ~575W + transient に十分 |
| **CPUクーラー** | Cooler Master V4 Alpha 3DHP(デュアル 12cm サイドフロー)| 空冷・標準 |
| **ケース** | **Cooler Master MasterFrame 400 Mesh Silver【入荷待ち】** | ★ケース入荷待ち=出荷遅延リスク(§7)|
| **OS** | **Windows 11 Pro 64bit DSP プリインストール** | ★OS インストール不要。dev 環境を載せるだけ |
| 保証 | 通常保証 1年(標準構成)| 周辺機器/Office/セキュリティ無し |

- **VRAM 32GB**: llcore 射程 ≤32B の線形化/量子化/蒸留に余裕。3B 本走・StateX continued-train・proxy v2 フル走を快適に。70B は int4 で際どい(Claude 代替不可なので無理に狙わない)。
- **速度**: 旧ノート CPU 本走 6–9h は、3090 想定で 1–2h。**RTX 5090 は 3090 比 ~2–3×** → 本日プローブ級は**数分〜数十分**見込み(forward 律速分のみ加速=Amdahl、楽観しない)。
- **128GB RAM** が効く場面: 大コーパス(RAD/aozora)前処理、複数モデル同時 load、CPU-offload による大型モデルの一部実行、データ生成。

## 2. パス戦略(★最重要 — 破損回避の鍵)

**現 `D:/` レイアウトを新機で完全再現する**(ドライブレター・絶対パスを温存)。理由 = ハードコード多数:

- **tool-guard グローバル hook** が `python "D:/tools/raptor/libexec/raptor-tool-guard"` を絶対パスで参照(`~/.claude/settings.json`)。
- ccr / raptor が `RAPTOR_DIR` / `RAPTOR_CALLER_DIR`、多数の `D:/` 絶対パス、`D:/api-keys.json`、`D:/docs`(RAD)、`D:/tools/raptor-analytics.db`。
- llcore/fullsense スクリプトの `D:/projects/...`、Task Scheduler ジョブの絶対パス。

→ 新機でも **C:/Users/puruy/** と **D:/** を同名で用意。パス変更は最小限に(変えるなら一括 grep して洗い出し)。

**★新機の前提と対策(注文明細で判明 — 2TB 1 本・パーティション分割なし=既定で C: だけ・D: 無し)**:

1. **Windows ユーザー名を `puruy` で作成**(初回セットアップ時)。グローバル hook が `C:/Users/puruy/.claude/hooks/...`、memory が `C:/Users/puruy/.claude/projects/...` を参照するため、ユーザー名が違うと全 hook/memory パスが破損。**最優先**。
2. **D: ボリュームを用意**(`D:/` ハードコードが大量=tool-guard グローバル hook の絶対パス含む)。2 案:
   - **(A) 2TB を C:+D: に分割(推奨・追加費用ゼロ)**: Win11 の「ディスクの管理」で C: を縮小 → 未割当に **D: を作成**(例 C: 800GB / D: 1.1TB)。移行データ(projects+docs+.claude ~数十GB+将来 checkpoint)に D: 1TB+ は十分。
   - **(B) 2nd M.2 SSD を増設して D: に割当**: B860M は M.2 追加スロットあり(注文では「追加SSD 未選択」)。物理分離で I/O 余裕・後から可。急がば (A) で開始し後日 (B) も可。
3. C:/D: を揃えたら **§3 のデータを同一絶対パスへ展開** → ハードコード破損ゼロ。
4. 残る環境差(`C:/Python314` 等の py インストール先、`RAPTOR_DIR`)は §4 で再設定。

## 3. データ移行(現 C:/D: → 新機)

**移行対象**(working set):

| 対象 | 中身 | 備考 |
|---|---|---|
| `C:/Users/puruy/.claude/` | memory(`projects/<...>/memory/`)、`settings.json`(グローバル hook + **tool-guard 配線**)、skills(superpowers/gsd/find-skills/raptor)、keybindings | ★ccr 自律・tool-guard の核。最優先 |
| `D:/projects/` | llcore, fullsense, llive, llove, llmesh, llloop, llterm, mcp-3d, browser-use-project(Alpaca) | FullSense 一式 |
| `D:/tools/raptor/` | raptor framework + tool-guard + libexec + corpus skills | |
| `D:/docs/` | RAD ~48,800 docs / 80+ `*_corpus_v2/` + hacker_corpus | 大容量・ファイル数多 |
| `D:/api-keys.json` / `D:/api-manager/` | APIキー一元管理 + sync スクリプト | ★秘密。安全に移送(暗号化 USB 等) |
| `D:/tools/` | raptor-analytics.db / codeql / osv-mcp | |
| HF model cache | Qwen 0.5B/1.5B 等(`~/.cache/huggingface` か指定先)| 再DL 可だが移送が速い |
| ccr 本体 + node-pty | 自走端末 | 再ビルドでも可 |
| `D:/backup/` | バックアップ | 任意(再生成可なら skip) |

- **転送手段**: **外付け NVMe SSD で一括コピー → 新機で同パスに展開**(最速・数百GB)。LAN(robocopy /MIR)は代替。クラウドは大容量で非推奨。**api-keys.json は別経路で安全に**。
- 容量目安: 現 D: used ~788GB(全部は不要)。working set は projects + docs + .claude が主。→ **2TB SSD 推奨**。正確値は du 集計(別途)で確定。

## 4. 環境セットアップ(新機 OS 後)

1. **OS = Windows 11 を維持**(現と統一。PowerShell/Git Bash 二本立て・パス互換・tool-guard/ccr/全スクリプトが Windows 前提)。Linux dual-boot は GPU 僅差有利だが移行コスト大 → 非推奨。
2. **NVIDIA driver**(最新 Studio/Game Ready、**CUDA 12.4+ 対応版**)。CUDA toolkit は PyTorch wheel 同梱のため **driver のみで可**。
3. **Python**: `py -3.11`(全 FullSense)+ 3.14/3.9/uv 3.12 を現状踏襲。
4. **torch CUDA 版**: `py -3.11 -m pip install torch --index-url https://download.pytorch.org/whl/cu124`(現 CPU torch 2.12 → CUDA 版。版整合を確認)。
5. **各 project 依存再構築**(pyproject から venv 再生成)。llcore は src レイアウト(`PYTHONPATH=src` or editable install)。
6. **ツール群再導入**: Git Bash / Node.js v24 / Rust 1.94 / uv / rtk(token killer)/ ccr(node-pty, zx build)。
7. **環境変数**: `RAPTOR_DIR` / `RAPTOR_CALLER_DIR` / `ANTHROPIC_API_KEY`(`settings.local.json`)/ `api-keys.json`。
8. **MCP servers 再設定**: osv-mcp / semgrep / sqlite(raptor-analytics.db)/ fetch / github / Google Drive / firecrawl / arxiv 等。
9. **Task Scheduler 再登録**: fullsense status telegram(平日11:30)/ trading 20分サイクル / api key sync 等。**★トレーディング(Alpaca paper)は時間依存** — 移行中の二重起動/欠損に注意(移行ウィンドウは旧機停止 or 明示一本化)。

## 5. 検証チェックリスト(移行後・順に緑化)

1. `py -3.11 -c "import torch; print(torch.cuda.is_available(), torch.cuda.get_device_name(0))"` → **True + GPU 名**
2. **llcore native forward GPU golden 一致**: `scripts/prove_native_matches_hf.py` を GPU で(CPU 一致は実証済 → GPU でも next-token argmax 一致を確認)
3. **小 GPU 学習 smoke**: ttt_plateau or chat 1 step を `.to("cuda")` で(本日の `--chunk-size` 経路含む)
4. **ccr 起動 → SESSION START 復元 → tool-guard live**(グローバル hook が `D:/tools/raptor` 温存パスで発火)
5. **raptor /scan smoke + MCP servers 応答**
6. **trading 系(paper)健全起動**(二重起動回避を確認)
7. **RAD corpus アクセス**(`D:/docs` 横断検索)
8. **rtk / 各 libexec / hooks(backup-hook auto-commit)** 動作

## 6. 移行後の初手 GPU ワークロード(compute-gated キュー)

`feedback_claude_max_compute_priority` に従い **decision-relevant な実測を先に**(方向を解決する work):

- **★本日のプローブ(chunk_size>128 plateau)を GPU でフル**: gated-deltanet + recurrent/recurrent-wide × chunk∈{128,256,512,1024} × **≥3 seeds**(CPU 9h/arm → GPU 数十分)。§13(4) の真の検証を一気に。
- **線形化 本訓練 + 蒸留 held-out 検証**(改造①④)。
- **int8 GPU カーネル**で 0.7tok/s 解消(改造②)。
- **StateX continued-train / 3B スケール**。
- **proxy v2 フル走**(K≥12、context sweep 2048–4096=SUPRA 級長文脈崩壊帯)。

## 7. タイムライン(2–3 週間 / ~07/12–07/18 完了目標)

- **Week 1(06/28–07/04)**: ①ハード確定・発注(GPU 中古調達 + パーツ)②外付け 2TB SSD 入手 ③**データ移行リハーサル**(現機 working set を外付けへコピー開始=ダウンタイム短縮)。
- **Week 2(07/05–07/11)**: ①組み立て・OS・driver・torch CUDA・py 環境 ②データ展開(**同パス**)③各 venv/ccr/MCP/Task 再構築。
- **Week 3(07/12–07/18)**: ①検証チェックリスト緑化 ②trading 系切替(二重起動回避)③**初手 GPU ワークロード投入**(まず本日プローブのフル版)④旧ノートは予備/退役。

## 8. リスク・コンティンジェンシー

- **DDR5 高騰** → RAM 最小開始 + 後追い増設(mmap loader で system RAM 圧縮済)。
- **中古 3090 個体差/保証** → 保証付中古ショップ or 新品 4090。電源 850W+ 必須。
- **データ移行中の trading 欠損** → paper なので実害小だが、移行ウィンドウは旧機継続 or 明示一本化。
- **パス不一致による hardcode 破損** → **D:/ レイアウト完全温存**で回避(tool-guard グローバル hook の絶対パス含む)。移行後 `torch.cuda` + tool-guard + ccr の 3 点をまず確認。
- **torch CUDA × driver 版不整合** → driver は CUDA 12.4+ 対応、torch は cu124 wheel。
- **秘密の移送** → `api-keys.json` は外付け一括コピーに混ぜず別経路(暗号化 USB / パスワード zip)。

## 9. 開いた意思決定(ユーザー確定待ち — 推奨を併記)

| 項目 | 推奨 | 要確認理由 |
|---|---|---|
| GPU | 中古 RTX 3090 24GB(~¥15万)| 24/7 耐久/速度を最優先するなら 4090(~¥30万)|
| RAM | 64GB(安心)| 予算/高騰回避なら 32GB 開始 + 後追い |
| データ移送 | 外付け 2TB NVMe SSD | LAN(robocopy)も可 |
| OS | Windows 11 維持 | Linux は移行コスト大 |
| trading 系 | 旧機/クラウドに残す or 新機へ | 移行中の二重起動回避 |
| 購入タイミング | GPU 先行・RAM 後追い も可 | DDR5 正常化(2027)待ちか今買うか |
