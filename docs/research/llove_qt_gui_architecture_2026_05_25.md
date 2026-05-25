# llove Qt GUI / OS-like Front — アーキテクチャ設計 (Research Stream H)

> **由来**: 2026-05-25 ユーザー指示 — 「開放端進化システムの**可視化を llove ベース**で行い、
> llove を現状の CLI/TUI (Textual) から **Qt による本格 GUI / OS 風フロント**へ成長させる。
> 他の ll 系プロジェクトも取り込み得る」。
> **可視化対象**: [[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] / [[OPEN_ENDED_CULTURAL_EVOLUTION]] が定義する
> 進化ラン (proxy / 将来は実 LLM)。fitness/diversity 軌跡・lineage tree・persona dominance・
> Genome3D heatmap・QD archive map・live run monitor (pause/resume)・belief-space viewer。
> **honest disclosure**: Qt GUI は**大規模ビルド**。本書は段階移行 (最小 PoC = 1 live panel から) を前提に
> 効果と工数を正直に見積もる。
>
> **位置づけ**: 設計 (要件確定 → 実装) の前段。本書は「推奨スタック + アーキ + 移行計画」を確定させ、
> 実装着手の判断材料にする。Stream H 単独で価値が成立する (llove 単体の GUI 化計画) が、
> Stream A-F (進化エンジン要件) の可視化 consumer として機能する。

---

## 0. 前提となる現状把握 (調査結果)

### 0.1 llove の現状 (D:/projects/llove)

- **Textual TUI**。`llove/app.py` の `LoveApp(App)` が複数ペインをホストし、`DataSource.stream()`
  (async generator) が `Event` を流し、各 `View.feed(Event)` が描画更新する pub/sub。
- **View 抽象** (`llove/views/base.py`): `class View` は `feed(event: Event) -> None` 1 メソッドのみ。
  Textual widget とは多重継承で混ぜる (metaclass 衝突回避で `abc.ABC` を使わない plain base)。
- **Event モデル** (`llove/events.py`): pydantic `Event(kind, ts, source_id, payload: dict)`。
  `EventKind` = sensor/spc_alarm/audit/rag_hit/llm_call/trace_span/narration/info。
  `payload` は free-form dict (rigid schema を持たない)。JSONL 直列化可。
- **DataSource 抽象** (`llove/sources/base.py`): `async def stream() -> AsyncIterator[Event]`。
  `JSONLSource` は `follow=True` で `tail -F` 相当 (進化ランの `generations.jsonl` をそのまま追える)。
- **Window 管理基盤 (F17) が既に存在** — ここが最重要:
  - `llove/window/types.py`: `WindowType` ABC + Registry。`builder(config) -> View` で
    **「Textual / Qt / その他 View インスタンスを生成」** と docstring に明記。`default_size` は
    **「TUI では文字単位、Qt では px 換算」** と既に Qt を想定。12 カテゴリ (data/viewer/game/editor/
    dialogue/input/visualization/meta/llmesh/typing/learning/debug)。サードパーティ `register_window_type` 可。
  - `llove/window/manager.py`: `WindowManager` が `FreeContainer`/`LockedContainer` を保持、
    `WindowMode` = **SDI/MDI/Tabbed/Tile**、`layout.toml` 保存/復元 (位置記憶 F17(c))、
    `WindowLayout` でシナリオ駆動レイアウト宣言 (F17(r))。
  - **設計原則 2.1.2「ウィンドウ哲学」: 既存ウィンドウを膨らませず新ウィンドウ種を追加するのが正しい**。
- **llive view パネル** (`llove/views/llive/`): bwt_dashboard / route_trace_viewer / memory_link_panel /
  cognitive_mesh_panel。`dispatch.py` に **view-model 分離の手本** がある:
  `dispatch_events()` = pure function (event_type で振り分け feed)、`TimelinePollDriver` =
  時間軸非依存の周回器 (`poll_once()` を Textual `Timer` から呼ぶ)。**ループと dispatcher が別レイヤ**。
- **SVG export** (`llove/export/svg.py`): SMIL animated SVG (`thought_factor_ring_svg` 等)。
  `<script>` 不使用 (GitHub Camo 互換)。将来候補に `lineage_animated_svg` / `map_elites_grid_svg` が
  既にコメントで予約済み。pure data → SVG 文字列 (Textual 非依存・テスト容易)。

### 0.2 ライセンス現状 — **要注意の不整合**

- **llove の `LICENSE` と `pyproject.toml` は現在 `MIT`** (`license = "MIT"` / `License :: OSI Approved :: MIT`)。
  ブリーフィングと一部メモリは「Apache-2.0 + Commercial dual-license」と記述するが、**コードは MIT のまま**。
  → **どちらにせよ permissive 系** (MIT も Apache-2.0 も)。LGPL 依存 (PySide6) と**両立**する。
  ただし dual-license に移行するなら **GUI 着手前にライセンス方針を確定** すべき (後述 §1.3 のピットフォール)。
- `shogi` extra は GPL-3.0 (`python-shogi`) を**意図的に optional extras に隔離**して core wheel を汚さない
  設計が既にある。**この「GPL は extras に隔離」パターンが Qt 依存選定の指針**になる。

### 0.3 可視化対象データの実形状 (llive 進化ラン出力 / D:/projects/llive/out/evo_run_2026_05_25*)

実ランの run dir は既に以下を吐く (= GUI が読む source of truth):

| ファイル | 形状 | GUI 用途 |
|---|---|---|
| `generations.jsonl` / `metrics.jsonl` | 1 行/世代: `{generation, n_individuals, best_score, mean_score, std_score, median_score, diversity_l2, seed}` | fitness/diversity 軌跡 (live plot) |
| `winners.jsonl` | `{generation, individual_id, parent_ids, score, rank}` | lineage tree のエッジ |
| `founder_lineage.jsonl` | `{generation, n_individuals, founder_counts: {name: count}}` | persona/founder dominance stream |
| `snapshot_gen_NNNN.json` | `{individuals: [...], bounds, generation, seed, generation_seeds}` (全状態) | resume 復元・Genome3D heatmap・個体詳細 |
| `lineage.mmd` / `champion_lineage.mmd` | Mermaid `graph TD` (gen×個体ノード) | lineage Mermaid (QWebEngineView 描画) |
| `evolution.svg` / `persona_dominance.svg` | SMIL animated SVG | 既存 SVG をそのまま貼る viewer |
| `run_manifest.json` / `run_summary.json` | ラン設定/結果 | run monitor ヘッダ |
| QD archive | `MAPElitesGrid.to_dict()` = `{n_bins_per_axis, feature_ranges, cells: {"i,j": cell_dict}}` (`src/llive/perf/evolutionary/quality_diversity.py`) | QD archive map (2D heatmap) |

**含意**: 進化エンジンは既に**ファイル境界で疎結合**な出力を持つ。GUI は「`out/<run>/` を読む / tail する」
だけで成立する。**進化エンジンと GUI を同一プロセスに同居させる必要はない** (これが long-run の鍵, §4)。

### 0.4 llmesh `llrepr` = 型付き表現コントラクト (D:/projects/llmesh/llmesh/llrepr/)

- `model.py`: `Document` + Node 型 (Text/Heading/CodeBlock/Figure/List/Table/Panel/Container)、`Style`。
- `writer_base.py`: `Writer(ABC)` = `render(doc: Document) -> str`。**glTF / General-MIDI 流の capability
  negotiation** — `supported_extensions` を宣言、`extensions_required` を満たせなければ **fail-closed で拒否**
  (`LlreprCapabilityError`)、非必須拡張は graceful degrade。
- 既存 writer: `MarkdownWriter` (能力の床) / `SvgWriter` / `TuiWriter` + `mcp_result.py` (MCP 配信)。
- `diff.py`: `diff_documents` / `apply_patch` / **`prediction_error`** ← 予測符号化 viz テーマと地続き
  ([[project_fullsense_animemd_branch_token_viz]] / [[project_fullsense_expression_realtime_marathon]])。
- **memory [[project_llmesh_representation_layer]] の原則**: 「あらゆる表現の根は llmesh の表現汎用層。
  llove / 記事 / web は consumer。表現コントラクトを 1 本決めて各 consumer が乗る」。
  → **Qt GUI のパネルは新たな consumer**。理想は **`QtWriter(Writer)`** を 1 本足し、llrepr Document を
  Qt widget へ落とす (writer は文字列を返す契約なので、後述 §5.3 でアダプタ層を挟む)。

---

## 1. (1) 推奨 Qt スタック + ライセンス根拠

### 1.1 結論 (推奨スタック)

| 層 | 採用 | ライセンス | 根拠 |
|---|---|---|---|
| **Qt バインディング** | **PySide6** | **LGPLv3** (公式 Qt for Python) | MIT/Apache と両立。動的リンクで自前コードを open-source 化する必要なし。Qt Company 公式・2026 のデファクト |
| **ドッキング/OS 風** | **PySide6-QtAds** (Qt Advanced Docking System) | **LGPL v2.1** | VS Code 級ドッキング。central widget 不要・どこにでもドック・floating window 間ドック。permissive と両立 |
| **live plot (高速)** | **pyqtgraph** | **MIT** | matplotlib 比 **75–150x 高速** (ImageItem)。QGraphicsScene ネイティブ・OpenGL 加速。real-time/大データ向け |
| **静的/論文品質 plot** | **matplotlib** (Qt5Agg backend) | **PSF/BSD** (permissive) | エクスポート品質図・補助。live でなく snapshot 図に限定 |
| **HTML/Mermaid/SVG** | **QWebEngineView** (PySide6-Addons) | **LGPLv3** (Qt parts) + Chromium (最も厳しくて LGPL 2.1) | 既存 `lineage.mmd` を mermaid.js (offline 同梱) で描画。`evolution.svg` も描画可。setHtml() でローカル完結 |
| **カスタム対話 viz** | **QGraphicsView / QGraphicsScene** | (PySide6 同梱・LGPL) | lineage tree / QD archive map / Genome3D の自前描画。BSP 木索引で**数百万 item でも ms オーダー** |
| **パッケージング** | **PyInstaller** (primary) → **Nuitka** (最適化時) | (出力 exe にライセンス影響なし) | §7 |

### 1.2 PySide6 vs PyQt6 — ライセンス根拠 (これが選定の核心)

- **PyQt6 = GPL or 商用 (Riverbank)**。GPL ライブラリを配布物に含めると **アプリ全体が GPL 化**を強制される。
  llove (MIT/将来 Apache+Commercial) で配布したいなら、**PyQt6 は GPL 強制 or 有償ライセンス**になり、
  **FullSense の dual-license (商用クローズド配布を許す) と根本的に衝突**する。
- **PySide6 = LGPLv3**。**LGPL は「PySide6 自体への改変のみ開示」で足り、自前アプリコードは
  open-source 化不要**。MIT/BSD/Apache と一般に両立 (LGPL 依存を permissive プロジェクトで使える)。
  → **PySide6 一択**。「商用クローズド配布を残す」FullSense 方針 ([[feedback_qwen_commercial_barrier]]
  と同じ思想 = 商用障壁を作らない) と完全整合。

### 1.3 ライセンスのピットフォール (honest disclosure)

1. **QtCharts は LGPL ではない (GPL or 商用)**。誘惑に駆られて QtCharts を使うと **GPL 汚染 or 有償**。
   → **QtCharts は使わない。pyqtgraph (MIT) を使う**。本書はこれを明示的に禁止する。
2. **`python-shogi` (既存 shogi extra) は GPL-3.0**。既に extras 隔離済だが、**Qt GUI が shogi panel を
   標準同梱すると GPL が core に漏れる**。GUI でも shogi 等 GPL 機能は **optional extra のまま**にする。
3. **LGPL の動的リンク要件**: PyInstaller で 1 バイナリに固めると「静的リンク」とみなされ得る議論がある。
   実務上は **(a) PySide6 を別 DLL/共有ライブラリとして同梱し置換可能にする、(b) LGPL ソース入手先を
   明記、(c) ライセンス全文同梱** で満たす。pyside6-deploy / PyInstaller とも LGPL 同梱手順あり。
4. **llove の LICENSE 不整合 (§0.2)**: コードは MIT、ブリーフィング/一部メモリは Apache+Commercial。
   **GUI 着手前に llove のライセンスを正本化** (MIT 継続 or Apache-2.0+Commercial 移行) すること。
   どちらでも PySide6 と両立するが、**dual-license に移行するなら CONTRIBUTOR からの過去コードの
   再ライセンス可否確認が必要** (これは GUI とは独立の宿題)。

---

## 2. (2) 「OS 風」フロント・アーキテクチャ

### 2.1 2 行サマリ

> **QtAds (Advanced Docking System) を「デスクトップシェル/WM」メタファの土台に据え、各パネルを
> "アプリ" として WindowType Registry から起動 → ドック/フロート/タブ/ワークスペース保存できる
> 単一 QMainWindow シェル。** llove 既存の `WindowManager`/`WindowType`/`layout.toml` をそのまま
> Qt 側の WM 実体にマップ (SDI/MDI/Tabbed/Tile の `WindowMode` は QtAds の perspective に対応)。

### 2.2 なぜ QtAds か (MDI/QDockWidget との比較)

| 方式 | 長所 | 短所 | 採否 |
|---|---|---|---|
| **QMdiArea** | 標準・MDI 子ウィンドウ | central widget 必須・子は MainWindow 外に出せない・古い UX | △ "MDI モード" の互換実装用にのみ |
| **QDockWidget** | 標準・基本ドック | central widget 領域にドック不可・モニタ跨ぎ弱い | △ 最小 PoC の最初の一歩には可 |
| **QtAds** | central widget 不要・全縁/全エリアにドック・floating window 間ドック・VS Code 級グループ移動・perspective 保存 | 3rd-party 依存 (LGPL v2.1) | **◎ 本命** |

QtAds は **「メインウィンドウとフローティングウィンドウに差がない」** = まさに OS 風 (どのパネルも
独立ウィンドウにも、ドックタブにもなれる) を素直に実現する。

### 2.3 シェル構成 (デスクトップシェル/WM メタファ)

```
QMainWindow ("llove Shell")
├─ MenuBar / ToolBar          … "View → New Window <type>" = WindowType Registry を列挙
├─ CDockManager (QtAds)        … = WindowManager の Qt 実体 (FreeContainer/LockedContainer をマップ)
│   ├─ Dock Area (left)        … ナビ/run 一覧 ("ファイラ" 相当)
│   ├─ Dock Area (center)      … 主可視化 (lineage tree / QD map) — 大画面パネル
│   ├─ Dock Area (right)       … メトリクス plot 群 (fitness/diversity)
│   └─ Dock Area (bottom)      … audit log / belief-space / status
├─ "Command Palette" (`:`)     … 既存 Textual CommandPalette の Qt 版 (QLineEdit + 補完)
├─ Workspace (perspective)     … QtAds perspective = "デスクトップのワークスペース切替"
│                                  layout.toml の上位概念。`:layout <preset>` を perspective に橋渡し
└─ StatusBar                   … run 接続状態 / poll 結果 (TimelinePollDriver.status_line() を流用)
```

- **パネル = "アプリ"**: 各 `WindowType` (id=`viz.lineage_tree` 等) が「デスクトップのアプリアイコン」。
  メニュー/パレットから起動 → 新規 dock widget として生える。`register_window_type` でサードパーティ拡張。
- **WindowMode マッピング**: `SDI` → 全パネルを独立フローティング / `MDI` → QMdiArea 互換ビュー /
  `Tabbed` → 1 dock area にタブ集約 / `Tile` → 自動タイル配置。QtAds perspective + 簡易レイアウタで実装。
- **layout 永続化**: 既存 `WindowManager.to_toml()/from_toml()` を**メタ記述**として残しつつ、
  QtAds 固有の幾何は `CDockManager.saveState()` (QByteArray→base64) を `layout.toml` に併記
  (TUI と Qt で **共通の論理レイアウト + UI 固有の物理レイアウト** の 2 層に分ける)。

---

## 3. (3) EVOLUTION-VIZ パネルセット → ウィジェット対応表

進化ランの可視化を **パネル (= WindowType) のカタログ**に落とす。各パネルは独立に起動/ドック可能
(OS 風 = 必要なものだけ開く)。**全パネルに `proxy`/`real` ラベル** ([[feedback_benchmark_honest_disclosure]])。

| # | パネル (WindowType id) | 可視化内容 (要件) | ウィジェット | データ源 |
|---|---|---|---|---|
| P1 | `viz.fitness_trajectory` | best/mean/median/std スコア時系列・**multi-best 化で単調収束が消えるか** | **pyqtgraph** PlotWidget (複数曲線・live append) | `metrics.jsonl` tail |
| P2 | `viz.diversity_trajectory` | `diversity_l2` / behavioral diversity (記述子分散) の高止まり・**末尾世代で非ゼロ** (受入メトリクス) | pyqtgraph PlotWidget (帯/分位) | `metrics.jsonl` tail (+ snapshot 由来記述子分散) |
| P3 | `viz.lineage_tree` | gen×個体の系譜 DAG・**champion lineage 強調**・founder 絶滅の可視化 | **QGraphicsView** (自前ノード/エッジ・zoom/pan・BSP 索引) ⊕ 簡易版は **QWebEngineView** で `lineage.mmd` を mermaid.js 描画 | `winners.jsonl` (parent_ids) + `*.mmd` |
| P4 | `viz.persona_dominance` | founder/persona の世代別占有 stream・**monoculture < 0.8 ガード** (max_lineage_share) | **pyqtgraph** stacked/stream plot ⊕ 既存 `persona_dominance.svg` viewer | `founder_lineage.jsonl` (founder_counts) |
| P5 | `viz.genome3d_heatmap` | Genome3D (c_factors 40 ⊕ c_cultural ⊕ c_latent) の個体×遺伝子 heatmap・疎変異の可視化 | **pyqtgraph** `ImageItem` (高速 heatmap・colormap) | `snapshot_gen_NNNN.json`(individuals) |
| P6 | `viz.qd_archive_map` | MAP-Elites archive: 記述子 2 軸 grid・cell 別 elite fitness・**単調成長 (QD-2) / 占有率 / 末尾で新 cell 増加 (open-endedness 判定)** | **QGraphicsView** grid (cell クリックで個体詳細) ⊕ 簡易版 pyqtgraph `ImageItem` | `MAPElitesGrid.to_dict()` (cells) |
| P7 | `viz.run_monitor` | live run の世代/壁時計/eta・**pause/resume**・checkpoint 状態・seed/config | QWidget (ラベル + QPushButton pause/resume) + **進捗 plot 縮約** | run プロセス IPC (§4) + `run_manifest.json` |
| P8 | `viz.belief_space` | Cultural Algorithm belief space: normative(値域)/situational(best exemplar)/temporal(軌跡) の 3 知識源・**critical social learning (Rogers ガード) fallback 率** | **QGraphicsView** or pyqtgraph (3 知識源を別タブ) | belief space checkpoint (CKPT-1) |
| P9 | `viz.metrics_table` | 受入メトリクス表 (§2 of requirements) の合格/反証症状を live 判定 | **QTableView** (合格列を強調・🔴/🟢 不使用 §OUTPUT STYLE 準拠) | metrics 集計 |
| P10 | `viz.individual_inspector` | P3/P6 から選んだ 1 個体の thought-factor ring・cultural vector・persona | 既存 `thought_factor_ring_svg` → QWebEngineView/QSvgWidget | snapshot individuals |
| P11 | `viz.predictive_diff` (将来) | llrepr `prediction_error` の diff-stream (予測符号化 viz)・annotated token flow | QGraphicsView annotated stream | llrepr `diff.py` |

**OS 風の効き所**: P1–P11 は「進化観測 OS のアプリ群」。ユーザーは run を開く → 必要なパネルを起動 →
ワークスペース (perspective) として保存。複数 run を別ワークスペースで並べて比較も可。

---

## 4. (4) live データ + 長期ラン + チェックポイント統合

### 4.1 大原則 — **進化エンジンと GUI を別プロセスに**

§0.3 の通り進化ランは**ファイル境界で疎結合**な出力を持つ。**5h+ 連続運転 (RUN-2) の進化プロセスを
GUI と同居させると、GUI のクラッシュ/再起動がランを巻き込む**。よって:

- **進化ラン = 独立プロセス** (既存の CLI ランナーをそのまま使う)。`out/<run>/` に逐次出力 + CKPT-1 で全状態。
- **GUI = 観測 + 制御クライアント**。2 経路でデータを取る:
  1. **ファイル tail (主・疎結合)**: `metrics.jsonl`/`winners.jsonl`/`founder_lineage.jsonl` を
     `JSONLSource(follow=True)` 相当で追う。**GUI が落ちても run は無傷**。
  2. **制御 IPC (副・pause/resume 用)**: run プロセスへ pause/resume/checkpoint シグナルを送る軽い経路
     (ファイルフラグ `control.json` ポーリング or ローカルソケット or llmesh MCP)。**fail-closed**:
     IPC 不通でも tail は生き、観測は継続。

### 4.2 GUI 内のスレッドモデル (PySide6)

- **GUI スレッドをブロックしない**のが鉄則。tail/poll/heavy 集計は **QThread worker** か
  **QThreadPool + QRunnable**。worker は `Signal()` でデータを emit、GUI スレッドの `@Slot` が受けて描画更新。
  クロススレッドは **queued connection** で安全 (PySide6 公式パターン)。
- **マルチプロセス (run プロセス) → GUI**: Python `multiprocessing.Queue` を 1 本の QThread が監視し、
  新着で Signal emit (公式推奨)。ただし §4.1 で run を別プロセス CLI にするなら、**tail で十分**で、
  Queue は「GUI が run を spawn する」モードのときだけ使う。
- **更新レート制御**: 進化は秒オーダーで多数世代を吐く (proxy 71 gen/s)。**全世代を即描画せず**、
  QTimer (例 10–30 Hz) で worker が貯めた最新バッチをまとめて描画 (pyqtgraph は append 高速だが
  描画は coalesce する)。

### 4.3 pause/resume × CKPT-1 のひも付け

- **P7 run_monitor の Pause ボタン** → 制御 IPC で run プロセスに「次の `checkpoint_every` 境界で
  チェックポイント後 停止」を要求。要件 CKPT-1 の全状態 (population+generation+RNG+QD archive+
  novelty archive+belief space+metrics+founder_lineage) を永続化してから停止。
- **Resume ボタン** → run プロセスを `--resume <latest_checkpoint>` で再起動 (決定論的継続)。
  GUI は新 run dir or 同 run dir を tail し直す。
- **GUI 単独の "巻き戻し閲覧"**: `snapshot_gen_NNNN.json` が 25 世代毎にあるので、**GUI は run を
  止めずに過去スナップショットへスクラブ (time-slider) して P3/P5/P6 を再描画**できる (read-only)。
  これは「録画再生」UX = ccr 連続運転 ([[project_ccr_auto_resume]]) と相性が良い。
- **5h+ 連続 (RUN-2)**: GUI は**任意のタイミングで起動/終了してよい** (run は別プロセスで走り続ける)。
  夜間ランを翌朝 GUI で開いて tail から最新まで追従 → そのまま live 観測、が自然。

---

## 5. (5) Core-engine + Multi-UI (TUI + Qt) リファクタ + ll 系統合

### 5.1 現状の view-model 分離はほぼ出来ている

llove は既に **Core engine + Multi-UI** 方向 ([[project_llove_editor_extensions]])。
`dispatch.py` の `dispatch_events()` (pure) + `TimelinePollDriver` (時間軸非依存) が手本。
**Textual に依存しているのは「描画」だけ**で、データ取り込み・振り分け・ポーリングは UI 非依存。

### 5.2 リファクタ方針 — 3 層に正本化

```
[Core / view-model 層]  ← UI フレームワーク非依存 (Textual も Qt も import しない)
  llove/core/
    event.py          … 既存 events.py を移設 (pydantic Event は既に UI 非依存)
    sources/          … DataSource / JSONLSource (既に async, UI 非依存)
    viewmodels/       … 各パネルの "状態" を持つ純粋クラス
                        例) FitnessTrajectoryVM(feed(metrics_row) -> 内部系列更新)
                            LineageVM(feed(winner_row) -> DAG 構築)
                            QDArchiveVM(load(grid_dict) -> cells)
                        → feed/load は pure。描画は持たない。テスト容易。
    drivers/          … TimelinePollDriver / FileTailDriver (時間軸抽象, UI 非依存)

[UI 層 A: Textual]                       [UI 層 B: Qt (新規)]
  llove/views/ (既存 Textual widget)       llove/qt/ (新規 PySide6 widget)
    各 View が VM を購読し render            各 QWidget が同じ VM を購読し paint
  llove/app.py LoveApp(App)                 llove/qt/shell.py LoveShell(QMainWindow)

[共通] WindowType Registry (llove/window/types.py)
   builder(config) -> View(Textual) | QWidget(Qt) を返す。
   → 同じ type_id "viz.lineage_tree" が TUI builder と Qt builder の 2 実装を持つ
     (起動側が UI に応じて適切な builder を選ぶ。Registry を UI 別に分けるか、
      builder を {"tui": fn, "qt": fn} の dict にする)。
```

- **最小破壊で進める**: `events.py`/`sources/` は既に UI 非依存なので**移設のみ** (import path 互換 shim)。
  新規は `core/viewmodels/` と `qt/`。Textual 側 View は VM 購読に薄く付け替える (一気にやらない, §6)。
- **View 抽象の一般化**: 現 `View.feed(Event)` は TUI/Qt 共通に保てる。Qt widget も `feed(event)` を
  実装すれば dispatcher (`dispatch_events`) をそのまま再利用できる (Qt 側は feed 内で `self.update()` 呼ぶ)。

### 5.3 ll 系統合

- **llive (進化エンジン + ラン出力)**:
  - GUI は llive を **import しない** (疎結合)。`out/<run>/` のファイル契約だけに依存 (§0.3)。
    これで llive のバージョン進化に GUI が追従しすぎない (measurement purity も保てる)。
  - 例外: P5/P6/P10 で個体の thought-factor/cultural vector を解釈する際、**ラベル順序**
    (`THOUGHT_FACTOR_LABELS` 等) は llove 側に**コピー保持**する既存方針 (`export/svg.py` が既にそう)
    を踏襲 (動的 import 回避・llove 単体動作維持)。snapshot に解釈に足る情報を持たせるのが理想
    (= llive 側に「GUI が読む安定スキーマ」を 1 つ約束させる, 小さな契約)。
- **llmesh `llrepr` (型付き表現コントラクト = レンダリングの source of truth)**:
  - **理想形**: パネルの中身を llrepr `Document` で記述し、**`QtWriter(Writer)`** が Document → Qt widget へ。
    ただし `Writer.render(doc) -> str` は**文字列契約**。Qt は live widget なので、2 段で扱う:
    1. **静的内容** (テーブル/見出し/図) は llrepr Document → (a) `SvgWriter`/`MarkdownWriter` の出力を
       QWebEngineView/QSvgWidget に流す (今すぐ可)、(b) 将来 `QtWidgetBuilder` (Writer の兄弟・
       `build(doc) -> QWidget` を返す非文字列 writer) を新設。
    2. **live 内容** (時系列 plot) は llrepr の対象外 (Document は静的表現)。pyqtgraph を直接使い、
       **スナップショット時のみ** llrepr Document (Figure ノード) に焼いて MCP 配信/記事埋込/SVG export。
  - これで [[project_llmesh_representation_layer]] の「表現コントラクト 1 本・consumer が乗る」を守る:
    **Qt GUI は llrepr の新 consumer**。記事 (Qiita)・GitHub SVG・TUI と**同じ Document から派生**。
  - **予測符号化 viz (P11)**: `llrepr/diff.py` の `prediction_error`/`diff_documents` を使い、
    世代間の表現 diff を annotated stream に (animemd / token flow viz と接続)。

---

## 6. (6) 段階移行計画 (Textual → Qt, 最小 PoC から)

honest: **一気に全パネルを Qt 化しない**。Textual TUI は**残す** (軽量・SSH 越し・CI snapshot 資産)。
Qt は「重い対話可視化が要る用途」の第 2 フロント。最小から積む。

### Stage 0 — Core 層の抽出 (UI 非依存化, ~小)
- `events.py`/`sources/` を `llove/core/` へ移設 (import shim で後方互換)。
- `core/viewmodels/FitnessTrajectoryVM` を 1 個だけ作り、**Textual 側を VM 購読に付け替え** (回帰テストで担保)。
- ゲート: 既存 pytest 全 PASS + Textual snapshot 回帰なし。

### Stage 1 — **最小第 1 PoC = 1 live パネル (★ここが "smallest first")**
- **`viz.fitness_trajectory` (P1) だけ** を PySide6 + pyqtgraph で実装。
- 単一 `QMainWindow` (QtAds はまだ入れず QVBoxLayout で可) に PlotWidget 1 枚。
- `metrics.jsonl` を QThread worker で tail → Signal → `@Slot` で pyqtgraph に append。
- **依存は `gui` extra に隔離** (`pip install llmesh-llove[gui]` = PySide6 + pyqtgraph)。core wheel は不変。
- 完成判定: 既存 `out/evo_run_2026_05_25_rich/metrics.jsonl` を食わせて best/mean/std 曲線が live 描画される。
- **これが最小・最も価値が高い** (進化ランの「動いてる感」を最短で出す・採用ファネル先頭 [[project_f25_demo_polish]])。

### Stage 2 — シェル化 (QtAds 導入)
- `LoveShell(QMainWindow)` + `CDockManager`。P1 を dock widget 化。`WindowType` Registry に Qt builder 追加。
- `viz.run_monitor` (P7) を追加し pause/resume IPC (まず `control.json` フラグ + run 側ポーリングで最小実装)。
- perspective 保存 = `layout.toml` 連携。

### Stage 3 — 対話可視化 (QGraphicsView/QWebEngine)
- `viz.lineage_tree` (P3): まず **QWebEngineView で `lineage.mmd` を mermaid.js 描画** (実装最短)、
  次に QGraphicsView 自前ノードへ (zoom/pan/個体選択)。
- `viz.qd_archive_map` (P6): pyqtgraph ImageItem → QGraphicsView grid (cell クリック)。
- `viz.persona_dominance` (P4) / `viz.genome3d_heatmap` (P5)。

### Stage 4 — Multi-UI 正本化 + llrepr 統合
- 残りパネル (P8 belief / P9 table / P10 inspector)。`QtWidgetBuilder` (llrepr) PoC。
- time-slider (snapshot スクラブ)。複数 run ワークスペース比較。

### Stage 5 — 仕上げ
- P11 予測符号化 viz。パッケージング (§7)。多言語 UI (i18n は既存 `llove/i18n` 流用)。

**各 Stage を独立コミット / 失敗実験も残す** ([[研究的探索の振る舞い]])。Stage 1 だけで「llove で進化を
live 可視化」は成立する。

---

## 7. (7) パッケージング / 配布

- **primary: PyInstaller** — 最も普及・PySide6 サポート枯れている・CI 再現性。Windows 単一フォルダ/単一 exe。
- **最適化/IP 保護時: Nuitka** — Python→C で **バイナリ最小・起動高速・bytecode 露出減**。
  ただし C ツールチェイン (MSVC) 必須・ビルド重い。**release ビルドの最終段でのみ** 検討。
- **briefcase**: PySide6 サポートは要個別確認 (検索で確証なし)。クロスプラットフォーム配布や
  Windows MSI/store 配布が要件化したら再評価 (現状は非推奨・調査保留)。
- **Windows 第一** (ユーザー環境)。QWebEngine 同梱で配布物は重い (Chromium ~150MB+) →
  **QWebEngine を使うパネルを optional に**し、軽量配布版 (pyqtgraph のみ) と
  full 版 (QWebEngine 込み) を分ける案も。
- **LGPL 同梱要件** (§1.3): PySide6/QtAds の LGPL 全文 + ソース入手先を配布物に同梱。
  PySide6 を置換可能な共有ライブラリとして同梱 (PyInstaller の onedir 形態が LGPL 的に安全)。
- **依存隔離**: `[gui]` extra = `PySide6 + pyqtgraph (+ PySide6-QtAds)`。`[gui-web]` extra = `+ PySide6-Addons (QWebEngine)`。
  core wheel (textual ベース) は**従来通り軽量**を維持 (Optional extras 設計の維持 = グローバル品質基準)。

---

## 8. リスクと honest disclosure

1. **Qt GUI は大規模ビルド (最大リスク)**。TUI 全機能の Qt 移植は数ヶ月級。→ **本書は Textual を捨てず、
   Qt を「重い可視化用の第 2 フロント」と位置づけ、Stage 1 (1 パネル) から積む**ことで初期投資を最小化。
   「OS 風フル WM」は到達目標であって初手ではない。
2. **ライセンス汚染** (QtCharts=GPL / python-shogi=GPL / LGPL 静的リンク議論)。§1.3 で回避策明示。
   **llove の LICENSE 不整合 (MIT vs Apache+Commercial) を GUI 着手前に正本化**する宿題。
3. **QWebEngine の配布肥大化** (Chromium ~150MB+) + プラットフォーム差。→ optional extra 化・
   lineage は QGraphicsView 自前描画を本命にして QWebEngine 依存を「mermaid 簡易表示」に限定。
4. **(副) 二重メンテ**: TUI と Qt の 2 フロント。→ Core/viewmodel 層を厚くし描画層を薄く保つ (§5.2) ことで
   ロジック重複を防ぐ。view-model は既に `dispatch.py` に手本あり。
5. **(副) 進化エンジンとの結合度**: llive スキーマ変更で GUI が壊れる。→ **ファイル契約 (§0.3) だけに依存**し
   llive を import しない疎結合で緩和。snapshot の安定スキーマを llive 側に小さく 1 本約束させる。

## 9. 参考 (調査出典)

- PySide6 vs PyQt6 ライセンス: pythonguis.com (LGPL vs GPL/commercial), doc.qt.io commercial
- QtAds: github.com/githubuser0xFFFF/Qt-Advanced-Docking-System, pypi PySide6-QtAds (LGPL v2.1)
- pyqtgraph (MIT, 75-150x matplotlib) / QtChart (GPL/商用) / matplotlib (PSF/BSD): pythonguis.com, pyqtgraph.com
- QWebEngine ライセンス (LGPLv3 + Chromium LGPL2.1): doc.qt.io qtwebengine-licensing
- QThread worker/signal-slot: doc.qt.io QThread, pythonguis.com multithreading
- QGraphicsView (BSP 索引・数百万 item): doc.qt.io QGraphicsScene
- パッケージング (PyInstaller/Nuitka): ahmedsyntax.com 2026, krrt7.dev
- 内部: D:/projects/llove (app.py / views/base.py / events.py / window/{manager,types}.py / sources / export/svg.py / views/llive/dispatch.py)、
  D:/projects/llive/out/evo_run_2026_05_25*、D:/projects/llmesh/llmesh/llrepr/、
  [[OPEN_ENDED_EVOLUTION_REQUIREMENTS]] / [[OPEN_ENDED_CULTURAL_EVOLUTION]] / [[project_llmesh_representation_layer]] /
  [[project_llove_editor_extensions]] / [[feedback_qwen_commercial_barrier]] / [[project_f25_demo_polish]]
