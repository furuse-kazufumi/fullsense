# HeyGen Hyperframes 調査 — HTML→決定論的 MP4 の agent-first OSS (2026-06-12)

> 出所: Telegram 経由ユーザー送付 (claude-loop task `20260612T120540-061c8c`)。
> 対象 = <https://x.com/heygen/status/2064385558496100502> (2026-06-09 投稿) → <https://github.com/heygen-com/hyperframes>。
> 制約 = needs-human-judgment: 本メモは調査のみ。採用判断・PoC 着手はユーザー判断待ち。

## 1. 事実 (一次情報: repo metadata + README, 2026-06-12 取得)

- **何か**: HTML + CSS + media + seekable animation を **決定論的 MP4** にレンダリングする OSS フレームワーク。
  キャッチコピー「Write HTML. Render video. Built for agents.」
- **メタデータ**: heygen-com/hyperframes、TypeScript、**Apache-2.0** (per-render 課金なし・商用閾値なし)、
  created 2026-03-10、**26,866 stars / 2,518 forks** (公開 3 ヶ月、X 告知は 2026-06-09)。
  topics: ai, animation, ffmpeg, gsap, html, **mcp**, puppeteer, rendering, video。
- **仕組み**: composition = `data-start`/`data-duration`/`data-track-index` 等の data 属性付き HTML。
  アニメは GSAP/CSS/Lottie/Three.js/Anime.js/WAAPI を **adapter 経由で seekable 化** →
  headless Chrome で 1 frame ずつ seek → FFmpeg encode。**same input → same frames → same output** (CI/回帰テスト前提)。
- **agent-first**: `npx skills add heygen-com/hyperframes` で Claude Code / Cursor / Gemini CLI / Codex に
  「動画制作ループ (plan → HTML → animation 配線 → lint → preview → render)」を skill として教える設計。
- **frame.md**: design.md (web 向けデザインシステム) を「カメラ向けに反転」した DESIGN.md superset。
  同じ token・同じ規則を frame 用に書き直し、agent が scale を推測せずにブランド準拠動画を組めるようにする翻訳層。
- **スタック**: CLI / core / engine (Puppeteer+FFmpeg) / producer / studio / player / shader-transitions / AWS Lambda 分散レンダ。
  要件 = Node 22+ + FFmpeg。
- **vs Remotion**: 同じ headless Chrome + FFmpeg 系。差 = React 不要・ビルドステップなし・plain HTML
  (agent が書きやすい)・Apache-2.0 (Remotion は source-available)。

## 2. FullSense との関係分析

| 観点 | 判定 | 根拠 |
|---|---|---|
| animemd / mangamd / llove animated SVG との競合 | **競合せず・隣接** | 出力メディアが違う: 我々 = SVG/SMIL (README/Qiita 埋込・軽量ベクタ・ブラウザネイティブ)、Hyperframes = MP4 (X/YouTube/SNS 動画)。配布チャネルが排他でなく相補 |
| llrepr (RepIR, LLVM-for-expression) との思想 | **同方向の大手実例 = 妥当性の裏付け** | 「宣言的マークアップ = 表現の中間表現」「決定論的レンダリング」「agent に制作ループを教える」が一致。HeyGen 規模の参入は typed-representation 路線の市場検証になる |
| frame.md パターン | **llrepr writer 設計への直接示唆** | 「メディア毎の翻訳層を md 契約で書く」= FullSense「表現コントラクト 1 本に各 consumer が乗る」(project_llmesh_representation_layer) と同型。llrepr の writer 別 DESIGN 契約に転用可能 |
| デモ生成の道具として | **採用候補 (consumer)** | f25_demo_polish「動きで魅せる・採用ファネル先頭」に合致。llcore gate 判別デモ / llove TUI デモを MP4 化して X/YouTube 発信できる。Apache-2.0 で商用障壁なし (feedback_qwen_commercial_barrier の懸念非該当) |
| Qiita 戦略への影響 | **不変** | Qiita は動画/アニメ埋込制約 (imgix ラスタライズ) → 既存の静的 SVG フォールバック戦略 (feedback_qiita_svg_path_and_cache) はそのまま。Hyperframes は発信チャネル拡張であって SVG 戦略の代替ではない |

## 3. 取り込める知見 (実装せずとも学べるもの)

1. **seekable adapter 抽象**: wall-clock アニメを「seek できる timeline」に正規化してから frame capture する設計。
   animemd の SMIL 出力でも「決定論的に任意時刻の静止フレームを切り出せる」性質は静的フォールバック生成に同じ価値。
2. **agent skill として制作ループを配布**する形 (`npx skills add`) — FullSense デモ/記事生成ループの配布形態の参考。
3. **lint → preview → render の非対話 CLI** = agent 駆動の前提。llrepr CLI 設計の規範になる。

## 4. 提案 (human-go 待ち)

- **小 PoC 案**: llcore gate 判別デモ (既存 SVG) を Hyperframes composition に移植し 10-20 秒 MP4 を 1 本レンダ →
  X 発信テスト。規模 = 小 (Node 22+ / FFmpeg導入込み 1 セッション以内)。
- 判断点: (a) FullSense 発信に動画チャネル (X/YouTube) を加えるか (b) その最初の題材
  (llcore gate デモ / llove TUI / 進化アニメ) (c) PoC 優先度 (master_plan T3 発信トラックの位置づけ)。

## 5. 来歴

- X post: 2026-06-09 16:34 UTC, @HeyGen 公式 (engagement は告知時点で小: 15 likes / 2.6k views — repo stars 26.9k との乖離は repo 既知層が主)
- 取得手段: api.fxtwitter.com (post 本文) + gh api (metadata/README)
- 関連既存 doc: telegram_ai_tools_scan_2026_06_10.md (同種の Telegram 発ツール調査)
