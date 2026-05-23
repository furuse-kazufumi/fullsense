# FullSense「表現 × リアルタイム」ideation marathon

> 2026-05-23 セッション。ユーザー指示「再起動したら ~12h の思考/ideation 枠を設けたい。
> 実装(A→B→C→D)より先にアイデア熟成」を受けた deep ideation の成果記録。
> フロー: **rad-research（先行研究）→ triz-ideation（矛盾解消）→ cross-domain-ideation（異分野転用）→ 統合**。

---

## 0. North Star と前提

- **北極星**: 「スナックバス江」級のマンガ理解を持ち、**豊かな表現を near-real-time で届ける** FullSense。
- **構成**: llmesh(on-prem LLM hub, MCP server, SPC, MQTT/OPC-UA) / llive(認知OS, 4層メモリ) / llove(TUI, SVG/Mermaid/Markdown 端末再現)。
- **既知の課題（前セッション）**: llmesh は前半(センサ→SPC)のみ real-time、後半(LLM説明+push)が gap。あらゆる表現の根は llmesh の表現汎用層で、manga-SVG/llove SVG/記事埋込は consumer。

---

## 1. 統合発見（marathon の核）

### 発見A: FullSense 全体を「予測符号化アーキテクチャ」として再構成できる

神経科学の **予測符号化（Predictive Coding, Friston 自由エネルギー原理）** = 脳は感覚入力を待たず**予測を先に生成し、予測誤差(prediction error)だけを上方伝播**する。これを FullSense に移植すると 3 論点が 1 原理で貫ける:

- **論点4（real-time）**: LLM説明を SPC warning-zone で**先回り生成**（予測）→ 異常確定時は予測との**差分だけ push**（予測誤差）。「確定後に全文生成」する既存の異常検知LLMに対し、**負のレイテンシ**を実現。
- **論点3（表現コントラクト）**: push は full payload でなく **typed diff（予測誤差）**。CRDT/JSON Patch op として配信。
- **論点1（評価）**: 評価とは「生成（予測）と rubric（観測）の予測誤差」。誤差が大きい箇所だけを批評・再生成する局所修正ループ。

→ **これは FullSense の新しい設計アイデンティティになりうる**。「LLMの周りに被せる認知OS（llive）」というメタファーに、神経科学的な予測符号化の裏付けが付く。

### 発見B: FullSense の「制約」はすべて差別化の源泉（TRIZ #22 災い転じて福）

5 矛盾中 4 つが **原理#22（制約→強みへ転化）** に収束した。

| 制約 | 転化後の強み |
|---|---|
| オンプレ（外部送信不可） | データ来歴を完全制御 → licensing クリーン性が副産物で得られる（論点2） |
| 同一VLM（コスト/純度で別モデル使えない） | 役割分離 + rubric外在化で self-preference を構造的に切る設計を持つ（論点1） |
| 少数自作データ（汎用大規模データ使えない） | identity層だけ来歴クリーンにすればよい（base/identity分離, 論点2） |
| 弱consumer（TUIは描画能力が低い） | capability negotiation + degrade を型で保証（論点3） |
| 機密を出せない（魅せにくい） | 「機密を出さず full loop が動く」こと自体が最強デモ（論点5） |

---

## 2. 6 論点の構造化（矛盾 / 先行研究 / TRIZ / 異分野 / 差別化 / 実装の種）

### 論点1 — マンガ評価ラダー + 同一VLM閉ループ

- **矛盾**: 同一VLMで生成↔評価を回したい（コスト/オンプレ純度）⟷ 同一モデルは self-preference bias / reward hacking が必発（評価信頼性低下）。
- **先行研究**: MangaVQA/MangaLMM (arXiv 2505.20298, 理解側), Re:Verse (2508.08508, long-form 物語理解), **Semantic Similarity is Spurious for Comic Understanding (2603.01950)** = embedding類似で評価すると幻覚を見逃す, **rDPO Rubric Rewards (2604.13029)** = instance-specific checklist rubric が outcome score を上回る, HumorBench (2507.21476) = ユーモアは open-ended 説明タスクが診断的, **Reward Hacking in Self-Refinement (2407.04549) / LLM Evaluators Favor Own Generations (2404.13076)** = 同一モデル閉ループの落とし穴の直接証拠, StoryReward (StoryRMB) = 自モデル判定の人間一致は最良 66.3%。
- **TRIZ解**: 物理的矛盾の**条件/時間分離**（生成時=自由、評価時=rubric束縛）。#2分離+#4非対称化で重みは同一だが役割を非対称な批評人格+検証可能rubricに外在化。#22で self-preference を「reward hacking 検出シグナル」に転用。
- **異分野転用**: 対審制(検察/弁護/裁判官)+二重盲検（法廷/科学）= 批評人格に生成プロセスを隠し rubric だけ渡す。免疫の negative selection（生物）= rubric違反を排除（self-preference=自己免疫の逆）。
- **FullSense 差別化**:
  1. 起承転結を**検証可能な構造制約**に分解した4コマ専用評価ラダー（既存は character/style 偏重 → 物語構造×ユーモア軸）。eyeglasses(眼鏡)を semantic類似でなく rubric checklist で実装し 2603.01950 の spurious 問題を回避。
  2. 同一VLM閉ループの self-preference を「役割を別人格+別rubricで固定」して再学習なし・on-prem で切る → llive Approval Bus と親和。
  3. 「ユーモア説明可能性」を最上位 evidence level に（HumorBench流, 「なぜ面白いか」の整合性をラダー最上段合格条件に）。
- **評価ラダー軸案（6段, sourcehunt evidence ladder と同形）**: `parsed → panel_consistency → structure_valid(rubric) → causal_coherent → twist_present(「転」の意外性) → humor_explained(最上段)`。
- **4コマ脚本 L 段階案**: L0=粗筋(起承転結ラベル) / **L1=構造化脚本(各コマ: シーン/キャラ/台詞/カメラ/感情 の JSON, 起承転結を生成制約にハード固定)** / L2=コマ間 world-state 持ち越し / L3=Critic ラダーで局所自己改稿。
- **未踏領域**: 4コマ(起承転結)専用の**生成評価ベンチが corpus/web 双方に未発見 = 最大の空白＝差別化機会**。

### 論点2 — 一貫生成 + licensing クリーン化

- **矛盾**: 高品質な一貫キャラ生成には汎用大規模モデル/大量データが欲しい ⟷ 商用 dual-license には来歴クリーン=少数自作データ/制約モデルのみ。
- **先行研究**: training-free multi-panel 一貫性が実用段階（StoryDiffusion / Story2Board / StoryBooth, cross-frame self-attention, SDXL/FLUX上でローカル可）, ReMix (2510.10156, 統一一貫性), CineAGI (2604.23579, LLMオーケストレーション×一貫性 +28.7%), SwiftPie (2605.01510, 1-step リアルタイム personalization), SEAL (2604.26883, 単一reference過学習回避), 透かし CSGuard(2605.01479)/SSB(2605.06153)。
- **licensing 実務**: **FLUX.1[schnell]=Apache-2.0**（商用クリーンの第一候補）, FLUX.1[dev]=非商用（採用不可）, SDXL=OpenRAIL++-M（商用可）, **Mitsua Diffusion**（CC0+許諾済データのみで学習=来歴クリーン唯一級）。生成物の著作権: 米国Copyright Office 2025報告でプロンプトのみ生成は著作者性欠く→人手レタッチ/選別の編集来歴を残す。
- **TRIZ解**: 物理的矛盾の分離（**データ量と来歴を分ける**）。#1分割+#3局所的性質で base(汎用画力, Apache-2.0/Mitsua) と identity(自作キャラLoRA, 来歴100%自己管理) を分離。#10先取り作用で来歴チェーンを生成時に自動付与。
- **異分野転用**: 差分プライバシー/合成データ（金融・統計）= 自作少数を augment で安価に増やし来歴は親が保証。
- **FullSense 差別化**:
  1. **「来歴クリーン全層スタック」**: FLUX.1[schnell] or Mitsua を base に自作キャラ(古瀬あい)15-25枚で LoRA → C2PA manifest + 改竄耐性透かしを生成物に自動付与。「学習データ来歴 + 生成来歴 + 改竄耐性」を一本のチェーンで証明する on-prem パイプライン。汎用 SaaS が法務上謳えない領域 = オンプレ哲学が直接 licensing 強みに転化。
  2. LLMオーケストレーション×一貫性（CineAGI思想の認知OS化）: llive がキャラprofile/scene blueprint 管理、一貫性破綻を Approval Bus で止める HITL ゲート。
  3. llove 端末再現 × リアルタイム一貫生成（SwiftPie系1-step → SVG/Mermaidと並べTUI逐次描画, SNS拡散性高）。
- **現実性**: 「自作素材だけで回す」は十分現実的（LoRA は 15-25枚で安定、30枚超は memorize リスク）。最大作業は来歴チェーンの自動化配線。初期は静止コマ+training-free一貫性に絞るのが堅実（video系multi-shotはVRAM要求高）。
- **未踏領域**: 「来歴クリーン base × training-free一貫性」の組合せ検証が空白。C2PA+透かし+学習データ来歴を一本化した来歴チェーンが未確立。

### 論点3 — 表現コントラクト（typed representation over MCP）+ push/stream

- **矛盾**: 1本の型付きコントラクトで全consumer統一したい（統一性/保守性）⟷ 各consumer(TUI/SVG/web/manga)は能力差がありリッチな型は弱consumerで崩れる（表現力 vs 互換）。
- **既存技術**: MCP は型付き結果を既にサポート（`outputSchema`+`structuredContent`, content union+`annotations{audience,priority}`）。push/stream は「できるが request-response 起点」（Streamable HTTP の SSE, `resources/subscribe`→`notifications/resources/updated`）。MCP Apps（`ui://`, 2026-01）は multi-consumer 公式入口だが**HTMLバンドル前提**で型付き抽象IRではない。「1 IR・複数target」は graphics/UI で確立（USD/glTF, React reconciler, layout2vector）。差分配信は CRDT/JSON Patch が現実解。
- **TRIZ解**: 物理的矛盾の分離（**コア型は単純・拡張は宣言制・consumerがdegrade**）。#1分割+#7入れ子で RepIR をコア閉集合+extensions(glTF流used/required)。#16部分的に+#15動性化で renderCaps 宣言→per-consumer 動的 degrade。#3で writer 責務は consumer 側。
- **異分野転用** ★3つの強い類比:
  - **LLVM IR + nanopass（コンパイラ）**: RepIR=IR、consumer=backend、writer=code generator、表現変換=pass。
  - **General MIDI capability レベル（音楽）**: 演奏意図の型付き表現でデバイス能力差をGMで吸収、非対応は近い音色にfallback = capability negotiation + ノードfallbackの完成形。
  - **Scalable Video Coding レイヤード符号化（情報理論）**: base layer + enhancement layer、帯域に応じて捨てる = base node + enhancement node、弱consumerはenhancement破棄。
- **FullSense 差別化**:
  1. **RepIR = LLVM-for-expression**: `{type:"representation", repSchema, root:<typed node tree>}` を MCP content union の新type相当として定義。SVG/Markdown/Mermaid/manga は consumer 側 writer で派生。MCP Apps(HTML固定) に対し「**端末でも描ける型付きIR**」が独自軸（llove TUI が一級 consumer に）。
  2. **Capability-negotiated degrade**: consumer が `renderCaps`(描けるノード型/SMIL可否) 宣言 → llmesh 表現層が per-consumer に最適 writer 選択+fallback。
  3. **Typed diff-stream over MCP**: 表現を CRDT/JSON Patch op を typed chunk として SSE/MQTT push（既存 on-prem MQTT 資産を transport に流用）。発見Aの予測符号化（誤差=差分）と直結。
- **型レイヤ案（3層）**: L1 Node型カタログ（`Text/Heading/List/Table/CodeBlock/Figure(svg|mermaid|image)/Panel(mangaコマ)/Container/Style`, glTF風 extensions used/required） / L2 Document tree（USD風composition） / L3 Writer（consumer側純関数 `RepIR→{SVG, Markdown, Mermaid, manga-SVG, TUI cells}`）。
- **push 経路選定**: 既定=MCP Streamable HTTP(SSE) / near-real-time=MQTT(llmesh既存流用) / 双方向UI=WebSocket。全て同一RepIR+同一diff opを運ぶ。fail-closed（解釈不能ノードは描画せず明示拒否+理由annotation, CLAUDE.md MCP規約準拠）。
- **未踏領域**: MCP に「typed representation」標準型なし。server-initiated 連続 push の typed増分ペイロード標準なし。multi-consumer の能力ネゴシエーションが MCP 表現層に無い。

### 論点4 — near-real-time E2E の天井上げ

- **矛盾**: LLM説明を高品質(長い/正確)にしたい ⟷ near-real-time で push したい（レイテンシ）。
- **先行研究**: CoSense-LLM (2510.19670, エッジでセンサ→検証可能意味トークン→Edge-RAG→サブ秒p95), PAT prefix-aware attention (2511.22333, 共有prefixでattention latency -53.5%), EAGLE-3/Medusa (speculative decoding 2-6×), PicoSpec (2603.19133, edge-cloud非同期 2.9×), KVShare/LMCache (prefix cache で TTFT 最大9.39×減), mq-bench (2603.21600, NATS/Zenoh はサブミリ秒), LLM Inference at Edge (2603.23640, 4bit 1.5B が consumer GPUで131 tok/s, NPUは near-zero variance)。
- **E2E 遅延分解**: ①センサ取得 ②SPC検知 = real-time(OK) / **③異常→LLM入力化 ④prefill(TTFT) ④decode(TPOT) ④→⑤完了待ち→push = gap**。ボトルネックは「異常確定後」に集中。
- **TRIZ解**: 物理的矛盾の**時間分離**（異常確定前に先回り生成）。#10先取り作用 + #34排除と再生(prefix cache) + #21高速化(speculative)。
- **異分野転用** ★: **予測符号化（神経科学）= 発見A** / **Smith Predictor・MPC（制御工学）= dead-time補償** / CPU投機実行+分岐予測（compiler）= warning傾向予測=分岐予測、説明先行生成=投機実行、誤予測時破棄=rollback。
- **天井を上げる Top-3 改修**:
  1. **SPC説明の prefix/KV cache 固定化**: `[固定prefix: 役割+SPC解説テンプレ+用語集] + [可変: 異常レコード]` に二分し固定prefixのKV cacheを常駐（PAT/vLLM prefix-caching）。SPCは説明構造が定型でprefix比率高 → TTFTを支配項から外す。実装軽・費用対効果最大。
  2. **edge SLM speculative decoding**（EAGLE-3 自己投機, on-prem純度維持版）: TPOT 2-2.9×、品質非劣化。
  3. **完了待ち廃止→token-streaming push + warning-zone 予測的先回り生成**: 生成token即push(SSE/NATS/Zenoh) + SPCがwarning-zone(2σ/連の傾向)で説明を投機事前生成・キャッシュ→確定で差分push＝**負のレイテンシ**。
- **FullSense 差別化**:
  1. **SPC-grounded speculative explanation**: draft を汎用SLMでなくSPCルール(管理図種別/8ランレジング判定)でテンプレ化 → acceptance↑＋「説明がSPC理論に接地」の監査可能性。
  2. **Warning-zone 予測的先回り生成**: SPC予兆性を使った負のレイテンシ。「先回りヒット率」を honest disclosure で内訳開示。
  3. **決定論的レイテンシ NPU + prefix常駐の SLO 保証**: 「説明 push の p99 を秒単位で SLO 保証」する on-prem 製品ライン（クラウドが出せない予測可能・低分散・データ非送信の3点セット）。

### 論点5 — 普及ファネルとの接続

- **矛盾**: リアルタイムに動きで魅せて拡散したい ⟷ オンプレ/プライバシー製品は機密を出せず魅せにくい。
- **先行研究/事例**: PLG 5段ファネル(discover→try→adopt→expand→procure), Time-to-Wow（即value実感で継続+81%, reverse funnel=サインアップ前にコア価値）, README animated GIF/SVG(20秒/5MB以内, GitHubネイティブレンダ), browser playground(StackBlitz/WebContainers), synthetic demo data(Syntho/Tonic, プライバシー製品の標準解), TED clarity 論文(2604.04583, processing fluency=認知摩擦低減が好評価、動く表現は文章より摩擦低い)。
- **TRIZ解**: 物理的矛盾の分離（**構造はリアル・中身は合成**）。#26コピー(合成データ) + #22災い転じて福(弱点→差別化) + #13逆転。
- **異分野転用**: ポチョムキン村（建築/歴史）の**逆転** = 「合成データだと透明に開示する正直なデモ」がオンプレ信頼に転化。建築BIMのLOD・演劇の書割 = 構造正確・素材代替。
- **FullSense 差別化**:
  1. **ゼロ設定 wow デモ**: llove 対局アリーナ(chess/go/mahjong/poker)を install不要で見せ time-to-wow 秒単位に。
  2. **機密を出さない動的デモ**: 合成センサ/合成機密で SPC/MQTT→LLM説明→push の full loop を録画・SMIL化。プライバシー製品の弱点を差別化点へ。
  3. **表現コントラクト1本→多面展開**（記事埋込SVG/README SMIL/llove TUI/playground を同一ソース多出力）= 論点3 RepIR と直結、先行事例なしの構造的優位。
- **施策ヒント**: `pip install llmesh-llove && llove arena` の2行 quickstart を README先頭 / 各記事冒頭に animated SVG+1行コンセプト→repo直リンク / 対局アリーナ20秒録画→SMIL（多言語各版に複製, feedback_multilingual_article_structure 準拠）。

---

## 3. 横断アーキテクチャ提案（marathon の収束点）

```
                 ┌─────────────────────────────────────────┐
                 │   llmesh 表現汎用層 (Representation Hub)  │
                 │   = Predictive-Coding Expression System  │
                 ├─────────────────────────────────────────┤
  センサ→SPC ──> │ ① 予測: warning-zone で説明を先回り生成   │
  (real-time)    │ ② 表現: RepIR (LLVM-for-expression) 生成 │
                 │ ③ 配信: typed diff(予測誤差) を push      │──SSE──> web consumer
                 │    prefix-cache常駐 / SPC-grounded spec   │──MQTT─> 産業IoT consumer
                 └─────────────────────────────────────────┘──stdout> llove TUI consumer
                        │ capability negotiation + degrade        (writer は各 consumer 側)
                        ▼
              評価ループ(論点1): 生成(予測) vs rubric(観測) の誤差だけ批評・再生成
```

- **1 原理（予測符号化）が論点1/3/4 を貫く**。論点2(licensing)は base/identity 分離で独立に解決。論点5(普及)は RepIR の多面展開 + 正直デモで接続。
- **実装順序の自然な依存**: RepIR 型定義（論点3 L1）→ prefix-cache + diff-stream（論点4改修1,3）→ 評価ラダー（論点1）→ 来歴チェーン（論点2）→ 普及デモ（論点5）。

---

## 4. 悩みどころの未解決点（honest disclosure）

- **同一VLM閉ループの自モデル判定限界 = 最良66%**（StoryReward）。役割分離で緩和するが完全には消えない。「先回りヒット率」「評価一致率」を内訳開示する設計を最初から持つ（feedback_benchmark_honest_disclosure）。
- **4コマ生成評価ベンチが存在しない** → 自作する必要（差別化機会だが工数）。
- **来歴クリーン base × training-free 一貫性の品質**が未検証（Mitsua上でStoryDiffusionが動くか要PoC）。
- **SMIL/SVG のファネル転換効果は実証データが薄い**（GIF は多いがSMILは少）。効果計測の枠組みが要る。
- **MCP の server-initiated 連続 push** は素直でなく、2026 RC で Extensions/Tasks へ再設計中 → typed diff-stream は拡張側に乗る前提で設計。

---

## 5. 実装キュー（急がない・優先順）— plan_ref 更新候補

marathon の結論として、実装は以下の順を推奨（ユーザー判断待ち、急がない）:

1. **RepIR PoC**（論点3 L1 型カタログ + SVG/Markdown/TUI の3 writer）— 実現性最高・他論点の土台。
2. **予測符号化 push PoC**（論点4 改修1 prefix-cache + 改修3 warning-zone 先回り + diff-stream）— 最大差別化、E2E gap を埋める。
3. **manga 評価ラダー L1**（論点1, mangamd L0 PoC の続き）— manga 専用 GitHub repo 作成可（gh認証済 furuse-kazufumi, private先行）。
4. **来歴クリーン生成パイプライン**（論点2, FLUX.1[schnell]/Mitsua + 自作LoRA + C2PA）。
5. **正直デモ + 多面展開**（論点5, 合成データ full loop 録画→SMIL→記事/README/playground）。
6. **既存キュー**: llove animated SVG B/C/D（project_llove_animated_svg_program）, llive Predictive Verification（project_idea_predictive_verification, Z3前段メタゲート — 発見Aの「予測」とも親和）。

---

## 6. 深掘り: 予測符号化の来歴と honest disclosure（発見A の検証）

ユーザーの来歴調査メソッド（特許→発明者→研究者→研究費/機材→参考論文源流→サプライチェーン）を
発見A に適用。4 並列エージェント（ML接地 / 西洋系譜 / 機材+citation / 日本エコシステム）で調査。

### 系譜（アイデアのサプライチェーン）
```
Helmholtz(1860s 無意識的推論) → Mumford(1992 皮質ループ: backward=予測/forward=誤差)
→ Rao&Ballard(1999 PC正典, Nature Neurosci) → Friston(2005-10 FEP/能動的推論で行動まで一般化)
  ├ 哲学: Clark(embodied) / Hohwy(internalist) / Seth(意識=制御された幻覚)
  ├ 数理: Parr / Da Costa(経路積分) / Ramstead
  └ ML: Bogacz&Whittington(PC≒backprop) → Millidge(限界を自ら明言) / Buckley / Lotter(PredNet)
        LeCun(JEPA: 別起源だが表現空間予測で収斂)
```

### 特許・人材のサプライチェーン
- **VERSES AI**（Friston が Chief Scientist）= FEP/能動的推論を商用化する事実上唯一の中心。
  登録特許 **US12,393,581 B2**（NL→active inference エージェント仕様化）の**発明者12名**が人材集中
  マップ＝Sussex/Ghent の能動的推論人材（Heins/Tschantz/Verbelen/Buckley）を吸収。
  honest disclosure: 登録は実質1件+provisional 多数で特許網は薄い、IR に空売り筋の誇張指摘あり。
- **Numenta**（Hawkins, HTM/Thousand Brains）= 別系譜。2025 に NuPIC（LLM CPU 最適化）へピボット、研究は非営利分離。
- **OSS**: pymdp（Heins ら, 離散 active inference 標準）/ PredNet（Lotter ら Harvard）/ RxInfer.jl（de Vries ら TU Eindhoven）。

### 日本エコシステム（重心 = 学術変革領域(A)「予測と行動の統一理論」2023-28, 領域代表 磯村拓哉@理研）
- **ATR川人系**: 川人光男 内部モデル/forward model（運動制御の予測=PC 日本源流）→ DecNef → XNef 商業化。特許 **JP2015116213A**（connectivity-neurofeedback, 発明者 今水/川人/福田）。
- **OIST系**: 谷淳（PC×能動的推論ロボ, RNNPB）/ 銅谷賢治（Bayesian brain×RL, A03班代表）。
- **RIKEN磯村系**: 培養神経回路で FEP 世界初実証（2023）、コンソーシアム横断統合。
- **京都/記号創発系**: 乾敏郎（和文 FEP 普及）/ 谷口忠大（**集合的予測符号化**=日本独自路線）。
- **臨床系**: 山下祐一（NCNP, 計算論的精神医学）/ 高橋英彦 / 吉田正俊。
- **研究機材/手法**: SPM（Friston 作の解析基盤）/ DCM（有効結合=生成モデル推定）/ variational Laplace / pymdp。神経計測は MMN・repetition suppression で予測誤差を顕在化。

### 発見A が「統一原理」になる対応（どこで効くか）
| PC 機構 | FullSense 構成要素 |
|---|---|
| 階層生成モデル | llive 4層メモリ（上位=empirical prior, 下位=sensory） |
| top-down 予測 | warning-zone 先回り生成 |
| bottom-up 予測誤差（誤差だけ伝播） | typed diff-stream（差分だけ push） |
| **precision weighting（誤差の信頼度=注意）** | **SPC 管理限界=precision threshold, 分散=信頼度**（最も筋の良い接点） |
| active inference（行動で誤差を減らす） | おせっかい proactive push / Approval Bus / 探索 vs 整合 |

### honest disclosure 結論（最重要・Millidge ペルソナの規律）
- 「PC=AI の統一原理」は**実証された定理でなく、反証困難ゆえに批判される思弁的統合**（FEP は
  unfalsifiable/トートロジー的との批判が定説）。PC≒backprop は浅層・厳しい前提下のみ、深層は未達。
- speculative decoding ↔ PC は「同型」でなく「**情報節約原理の家族的類似**」が honest な線
  （PC の誤差は連続・precision 重み付け・学習を駆動するが、speculative は離散一致判定で重みも学習もなし）。
- **採るべきは「統一原理として売る」ことではなく、2 つの具体機構**:
  (1) **precision-weighted push**（どの予測誤差を信じ push するかの重み付け層 — FullSense に未設計の新規レバレッジ）
  (2) **誤差駆動の差分配信**（typed diff-stream）。
  名乗りは「**予測符号化"風"アーキテクチャ**」に留める（過大主張回避）。
- 新規に効く順: **precision weighting（最有力, SPC と自然接続）> active inference（proactive llive,
  ただし Prakki 2024 を唯一足場とする実験的位置づけ）> free-energy 目的関数（メタファ整合に留める）**。

### 成果物: 予測符号化評議会ペルソナ（raptor/tiers/personas/）
発見A を深めるとき**生成↔懐疑↔検証**で回す 3 役 + ユーザー手法ペルソナ:
- `predictive_coding/friston_active_inference.md` — 生成・統一（大胆な統一案）
- `predictive_coding/millidge_honest_skeptic.md` — 懐疑・内訳開示（過大主張を冷ます）
- `predictive_coding/isomura_falsifier.md` — 検証・反証可能化（測定量・棄却条件・最小検証系へ）
- `provenance_investigator.md` — ユーザー(古瀬式)来歴調査メソッド（汎用, /oss-forensics・/sca とも同型）
- 将来案: ペルソナを llive 進化ゲノムに組込む（[[project_persona_genome_integration]]）。

## 関連 memory

[[project_next_session_ideation_marathon]] / [[project_manga_md_poc]] / [[project_llmesh_representation_layer]] /
[[project_llove_animated_svg_program]] / [[project_idea_predictive_verification]] /
[[feedback_benchmark_honest_disclosure]] / [[feedback_multilingual_article_structure]] /
[[feedback_provenance_research_method]] / [[project_persona_genome_integration]] /
[[project_fullsense_expression_realtime_marathon]]
