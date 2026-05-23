---
title: 3 日間で 8 リポを駆け抜けた話 — 火種 / 爆発 / 構造化、AI agent と二人羽織で踊った 72 時間
tags:
  - FullSense
  - llive
  - ClaudeCode
  - 自律エージェント
  - HonestDisclosure
private: false
updated_at: '2026-05-20'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

<!--
Qiita タグは 5 個上限. 本記事の主役順で:
  FullSense (umbrella) / llive (本セッション主役) / ClaudeCode (agent 環境)
  / 自律エージェント (主題) / HonestDisclosure (差別化ワード).
llove / llmesh / TRIZ / OSS / TUI / Python / pytest 等の関連タグは本文内
("[[...]]") で吸収する. 投稿前に user 判断でタグ入替可.
-->


> 投稿可否は user 判断. これは「3 日分の活動を全部入りで物語にする」依頼で
> agent が自律ドラフトしたものです.
> articles_pause は 2026-05-20 に解除済. 解除後の第 1 本目候補.

## 0. コンセプト hook — 「火種, 爆発, 構造化」

> **3 日間 × 1 人 × 8 リポジトリ × 100 commit overload × 1585 + 3086 + 796 テスト緑.**
> これ, 個人 OSS の話です. AI agent と二人羽織で踊ったらこうなりました.

先に結論:

- **5/18 = 火種を撒く日**. F25 Phase h, llove Day-0 gap audit, 中国 LLM presets,
  gitee mirror CI, COG-MESH 10 件 skeleton 投入. 「種まきの月曜」.
- **5/19 = 連続爆発**. M8.2〜M8.9 を朝に全件着地 → 昼に Production HTTP Sink +
  LoveApp 統合 → 夕方に F23/F24 PoC + 商標 + 収益化 playbook + 市場 SWOT +
  AI 開発環境 roadmap + 自律 spinoff カタログ + Qiita 記事 2 本. **1 日で 50+ commit**.
- **5/20 = 構造化と自動収束**. 朝に NEXT_SESSION.auto 自動化 + research hub 6 件 +
  test 回帰 fix. 昼に lleval v0.1 draft + 実装ノート. 夜に **llive コア最適化 12h goal** —
  Hebbian-style な自動収束フレームワーク (SynapticSelector + UCB1) を作り,
  得られた発見を実 production hot path に注入. **1585 PASS 維持**.

3 日間の役割分担を 1 行で整理すると, **量を撒くのは人間, 構造に押し戻すのが
AI**. 仕様の方向性決定とゴール設定が人間, 多前線の実装と検証 + 履歴整理が
AI. これは LLM agent と長く回した実感ベースの分担です.

以下, 3 部構成 + 教訓抽出. 90 秒で骨組み / 5 分で全体 / 30 分で全部入り,
の **集中曲線 3 段** で読めるように書いています.

---

## 1. 第 1 幕 (5/18 火種) — 月曜日に撒いた 6 種

### 1.1 90 秒サマリ

| 撒いた火種 | 場所 | なぜ撒いたか |
|---|---|---|
| F25 Phase h.1/h.2 HTTP API skeleton | llove | TUI 玩具から「llive 観測 IDE」へ pivot の足場 |
| Day-0 gap audit | llove | dogfooding に入る前に「何ができてない」を地図化 |
| 中国 LLM 6 種 OpenAI-compat presets | llmesh | EAR 制約環境で配布パスを断たれない保険 |
| gitee mirror CI | llmesh | GitHub 落ちても配布が止まらない冗長化 |
| supply-chain audit α (deps_audit CLI) | llmesh | OSS 監査責任を自前で持つ. PyPI 依存の origin 追跡 |
| COG-MESH 10 件 skeleton (深夜帯から早朝) | llive | 「勝手に話しかけてくる AI」の最小骨格を投入 |

種は撒いただけです. 育てるのは翌日.

### 1.2 「F25 Phase h」って何だっけ

llove (TUI dashboard) を「観測ツール」に化けさせる計画です. 5/18 時点で:

- `POST /api/v1/brief/submit` で外から brief を投入できるようにする (Phase h.1)
- `GET /api/v1/annotations/stream` で SSE 経由で annotations を流す (Phase h.2)

これを足場に, 後で **VS Code 拡張 + Neovim プラグイン** を載せる, という
multi-UI 戦略の前哨戦. 「TUI で終わる玩具ではなく, **エディタに住む観測 OS** に
寄せたい」という方針が memory に走っています.

### 1.3 中国 LLM presets と gitee mirror — 配布パスの保険

これは普段の OSS 仕事だと **誰もやらない仕込み**です. なぜ 5/18 にやったか:

- ある製造業の EAR 制約環境では cloud LLM が **そもそも引けない**.
  Anthropic も OpenAI も Gemini も無理. local LLM か中国 LLM のみ.
- GitHub が落ちる / 一時凍結される事案も無視できない.
  gitee mirror があれば配布が止まらない.

「FullSense は責任感のある AI エコシステム」と謳うなら, **配布まで責任を持つ**
姿勢を維持しないといけない. これが種.

### 1.4 COG-MESH 10 件を 1 晩で skeleton

これは 5/18 深夜から 5/19 早朝にかけての連続戦. 「能動発話」「Quarantined Memory」
「Mesh5W1H Annotator」「Quiet Hours」「BriefDeque Bridge」「Idle Training」
「TonicRiskMonitor」「TitleRecall」「ProactiveSpeaker」「GiftValueEstimator」.

人間の認知モデルから派生した 10 個の framework. 1 個ずつ skeleton + テスト 1 件で
107 PASS 増. これが翌日の爆発の燃料になる.

---

## 2. 第 2 幕 (5/19 爆発) — 火曜日に焼き尽くした 50 commit

### 2.1 90 秒サマリ

朝起きて「skeleton を本実装に切り替える」スイッチを入れたら, **その日 1 日で
全部燃え尽きた**.

| 時間帯 | 何が燃えたか | 数値 |
|---|---|---|
| 早朝 | M8.2〜M8.7 本実装 | llive +55 PASS |
| 朝 | M8.8 (graph analytics) + M8.9 (grammar EVO bridge) | +22 PASS |
| 朝 | M8.1 Timeline bridge skeleton (llive 側 emitter) | +5 PASS |
| 朝 | M8.1 LoveApp 統合 (CognitiveMeshPanel attach) | llove +25 PASS |
| 昼前 | **ProductionHttpTimelineSink** (auth Bearer + exp backoff retry + batch buffer + 4 env) | +12 PASS |
| 昼 | llmesh `/timeline/ingest` allow-list に cog_* 4 種 | +4 PASS |
| 昼 | E2E integration test (M8.1〜M8.9 chain) | +1 PASS |
| 午後 | F23/F24 PoC (PowerShell 互換シェル + ccr launcher) skeleton | llove +α |
| 午後 | AI 開発環境投資 roadmap, 商標 5 万円 CHECKLIST, 収益化 playbook, 市場 SWOT | docs 4 本 |
| 夕方 | autonomous spinoff カタログ + Family Tree 更新 + llgrow Planned | portal +多数 |
| 夜 | Qiita 記事 2 本 draft (M8.x 3 段ロケット / 個人 OSS 市場 SWOT) | docs +2 |

**1 日で 50+ commit, 累計 PASS 数 +120 弱**. 個人 OSS でこれは「燃え尽きた日」と
呼ぶしかない.

### 2.2 「M8.x」って何だっけ — 1 行ずつ復習

M8 = COG-MESH の **本実装フェーズ**. skeleton から「機能として動く」状態に
切り替えるマイルストーン群.

```text
M8.1  Timeline emit + LoveApp panel attach
M8.2  ProactiveSpeaker (能動発話)
M8.3  QuietHours gate
M8.4  IdleTraining (空き時間ミニ訓練)
M8.5  TonicRiskMonitor (KYT 由来の重要度モニタ)
M8.6  TitleRecall (タイトル想起ループ)
M8.7  Mesh5W1H Annotator
M8.8  GraphAnalytics (BFS/DFS/centrality 自前実装)
M8.9  GrammarLayer EVO bridge
```

これを 1 日で全部スイッチ ON にしたのが 5/19. 「skeleton と本実装の境界が
人間の体力で 1 日に詰め込める量を超えた瞬間」が見れた日, とも言える.

### 2.3 ProductionHttpTimelineSink — 「現場運用」を最小単位で

production 投入できる Sink を 1 ファイルに詰め込んだのが昼前. 内容:

- **Auth Bearer** トークン (env `LLIVE_LLMESH_TIMELINE_TOKEN`)
- **Exponential backoff retry** (`LLIVE_LLMESH_TIMELINE_RETRIES=5`)
- **Batch buffer** (`LLIVE_LLMESH_TIMELINE_BATCH_SIZE=10`)
- **Endpoint URL** (`LLIVE_LLMESH_TIMELINE_URL=http://prod-llmesh:8080`)

これだけ. 4 つの env を operator が設定すれば実 production が動く.
+12 PASS. テスト緑.

**「Production 投入するための最小構成は 4 env」**, この感触が嬉しい.

### 2.4 docs 4 本のサプライズ (商標 / 収益化 / 市場 / 投資)

5/19 は **コードだけの日ではなかった**. 午後に「個人 OSS をやってる人なら
誰もが避けて通れない」資料を一気に書いた:

1. **AI 開発環境投資 roadmap** — 「次の 1 年で何にいくら使うか」のラフ予算
2. **商標 5 万円 CHECKLIST** — JP/US/EU 1 区分でフラットに進める
3. **収益化 playbook** — 10 チャネル × 4 sprint で何を売るか
4. **市場受容性 SWOT** — 6 軸 WebSearch + SWOT + 生存戦略

これ全部 1 日で書く必要は本当はないんですよ. でも **「燃え尽きるなら全部
燃やす」** の精神で並列実行した. 後から見ると, この 4 本は **5/20 の構造化
セッションのインプット** になっています. 「商標を取る前に独立性を確認したい」
「収益化を始める前に研究 hub を整えたい」みたいな依存関係が見えた.

---

## 3. 第 3 幕 (5/20 構造化) — 水曜日に整理した 3 層

### 3.1 90 秒サマリ

| 時間帯 | 何をやったか | なぜ |
|---|---|---|
| 朝 | NEXT_SESSION.auto 自動生成 + Stop hook 連動 | NEXT_SESSION 手動更新の drift を構造的に解消 |
| 朝 | research hub 新設 (6 件 SOTA / prior-art メモ) | 自律 agent が SOTA 踏める基盤 |
| 朝 | 関連 prj test 回帰 fix (llove image-tool / llmesh hypothesis) | dogfooding に入る前に flaky を潰す |
| 朝 | spinoff_ideas C-2 採用優先度表 (HIGH/MID/LOW/DEFER) | research 結果から判断 |
| 昼 | QIITA #20 をユーモア方針で全面書き直し | articles_pause 解除後の表現テスト |
| 昼 | lleval v0.1 draft + implementation notes | 採用優先度 HIGH の最初の具体化 |
| 夕方 | (休憩 + バックグラウンド llmesh 全 3086 test 走行) | flaky 再現確認 |
| 夜 | **llive コア最適化 12h goal** (B-0〜B-6 + B-9) | Hebbian-style 自動収束 framework + 実 production 注入 |

**コードと文書のバランスを取り戻す日**, と表現できる. 5/19 が「全部燃やす」
なら, 5/20 は「**燃え滓を結晶に整える**」.

### 3.2 NEXT_SESSION.auto 自動化 — drift と戦う

NEXT_SESSION.md は手で更新するから, **必ず drift する**. 朝の 1 時間半で
解決:

- `scripts/gen_next_session_auto.py` を新設
- raptor の Stop hook に登録 → 毎ターン自動上書き
- `git log` + 関連 prj 最新 commit + 直近 4h 変更 + verify_publication 結果 + 未消化 operator action を 1 枚に集約
- 手動更新する `NEXT_SESSION.md` は **方向性メモ専用** に格下げ

これで次セッション開始時の context 復元コストが激減した. **「自動生成
ファイルは 1 つ多めに置く」が個人 OSS の正解** だと思う.

### 3.3 research hub 新設 — agent に SOTA を踏ませる

`docs/research/` に 6 件投入:

```text
docs/research/
├── index.md                       # Reference hub
├── lleval_sota.md                 # 10 framework 比較 + 4 ギャップ
├── llgrow_prior_art.md            # Growth Automation 先行例
├── cognitive_mesh_vs_sota.md      # COG-MESH の関連研究
├── llcraft_sota.md                # llcraft 候補の SOTA
├── llrisk_prior_art.md            # llrisk (Tonic Risk) 先行例
└── llgov_sota.md                  # llgov (governance) SOTA
```

これは「**自律 agent が研究分野を踏まえて判断できる基盤**」.
RAD (Research Aggregation Directory) の派生概念で, 普段の Claude
セッションで「先行研究は ?」と聞かれた時に, agent が `docs/research/`
を読むだけで SOTA matrix を引ける.

**「人間の研究調査の労力を agent が引き継ぐ」** ための仕掛けです.

### 3.4 spinoff_ideas C-2 採用優先度表

research 結果を踏まえて 6 件を分類:

| spinoff | 優先度 | 根拠 |
|---|---|---|
| **lleval** | **HIGH** | promptfoo wrap で 4 ギャップを埋める設計が明確 |
| llgrow | MID | growth automation は需要あるが既存 SaaS 競合多 |
| llbridge | MID | MCP bridge は wave 待ち |
| llcraft | LOW | LLM workshop は趣味色強い |
| llrisk | LOW | Tonic Risk monolithic な需要薄い |
| llgov | LOW | LLM governance は legal-heavy |
| llforen | DEFER | LLM forensics は時期早尚 |

これで **次に手をつけるべき spinoff が lleval 1 本に絞られた**. 個人 OSS で
spinoff カタログを持つと「全部やりたい病」になるが, 優先度表で抗体作る.

### 3.5 lleval v0.1 draft + implementation notes — 採用優先度 HIGH を具体化

午後に 2 本の draft を書いた:

1. **requirements_lleval_v0.1_draft.md** — LE-01〜08 要件
2. **lleval_v0_1_implementation_notes.md** — PoC scope (wrap not fork)

主要決定:

- **promptfoo を fork しない. wrap する.** Node.js fork は維持コスト 2 倍.
  Python subprocess で叩いて上載せする.
- **別 GitHub repo** (`furuse-kazufumi/lleval`), Apache-2.0 + Commercial dual.
- **v0.1 MVP** = LE-01 (多 provider 統一) + LE-02 (progressive size matrix) +
  LE-03 (honest disclosure analyzer) + LE-07 (CLI + Python API).

差別化 4 軸:

| # | 差別化 | 既存ギャップ |
|---|---|---|
| 1 | on-prem + cloud 統一 A/B | 産業 IoT + local llama.cpp と cloud API を同一 run で扱う設計が不在 |
| 2 | Progressive size curve (xs/s/m/l/xl) | 既存はどれも固定 prompt 長 |
| 3 | **Honest disclosure 自動診断** | 異常値の内訳分解は手作業領域 |
| 4 | Judge rotation + position swap | self-preference bias 自動検出 |

honest-disclosure 5 因子分解:

1. warmup hit
2. token-count normalization
3. network RTT 除外
4. backend attach overhead
5. system load

これを **CI でブロック可能な diagnosis report** にする, という設計が
本気度の温度. もう「自社が速い ! 勝った !」で終わらせない仕組み.

### 3.6 夜の本番 — llive コア最適化 12h goal

ユーザーから午後の終わりに本気の goal が降ってきた:

> 「llive のコア部分の最適化を進める. 12 時間後まで情報収集しながら色々と
> 試行してみること. ちゃんと履歴を残して不具合が出ない形に収束させて
> ください.」
>
> 「コア部分のデータの持ち方とかコンテナを変えてみたり, デザインパターンを
> 拡張してみたりして, 出来るだけ自動的に最適な構造に収束する感じが理想的.」
>
> 「**脳のシナプス構造のような重みづけが変化するような感じがいい**.」

これは普段の最適化依頼と桁が違う. 単一実装の手動高速化じゃなくて, **複数
候補を並べて自動収束させる framework を作れ**, という指令.

#### 設計判断 — `SynapticSelector`

ε-greedy + Hebbian-style weight update を組み合わせた variant selector を
新設:

```python
@dataclass
class StrategyVariant:
    name: str
    impl: Callable
    weight: float = 1.0

class SynapticSelector:
    """Hebbian-style strategy variant chooser.

    - ε-greedy で variant を選択
    - 実行 latency / quality を観測
    - weight = max(min_w, min(max_w, weight + lr * reward))
    - thread-safe (RLock)
    """
```

bounded modification (APO §E2) で min/max clip. 19 件テスト緑. **既存 1518 →
1537**, 回帰なし. これが B-0.

#### B-1 〜 B-6 — 自動収束を観察

| Phase | 試したこと | 学び |
|---|---|---|
| B-1 | top-K 抽出 (n=5000, k=10, 200 iter) | `heapq_nlargest` が weight=100 (max) に収束. `full_sort` は 0.377 に減衰. **収束する.** |
| B-2 | cosine variants (dim=16/128/768) | `numpy_normalized` (pre-L2 normalized 入力) が全次元圧勝. **pre-normalize cache で 2-5x.** |
| B-4 | decay variants (N=100/10000/100000) | N=100 では正しく `np_inplace` に収束, **N=10000/100000 で誤って `np_einsum` に収束**. 真の最良は `np_inplace` で 17% 速いのに weight が伸びない. **early-convergence bias 発見.** |
| B-5 | `UCBSynapticSelector` (UCB1) | B-4 と同条件で 3 サイズすべて `np_inplace` に正しく収束. **病理解消.** |
| B-6 | sliding window (deque vs list_slice) | maxlen=1000 で deque は converged. list_slice は **119x 遅化** (O(N) copy). **production 適用候補確定.** |

**B-4 が本セッション最大の発見**: 「自動収束」と謳っても ε-greedy だけだと
一極集中 dynamics に陥る. UCB1 の exploration round が必要. これは
`feedback_benchmark_honest_disclosure` の精神 — 「収束結果が実は最良で
ない」を見抜ける observability が全て.

#### B-9 — 発見を実 production hot path に注入

研究結果を実コードに反映しないと意味がない. B-9-a と B-9-b で 2 件注入:

**B-9-a: `SurpriseGate` / `BayesianSurpriseGate.compute_surprise`**

```python
# Before
def compute_surprise(self, new, mem):
    new = _l2_normalize(np.atleast_2d(new))
    mem = _l2_normalize(np.atleast_2d(mem))  # ← 毎回 O(M*D) 再 normalize !
    ...

# After
def compute_surprise(self, new, mem, *, assume_normalized: bool = False):
    new = _l2_normalize(np.atleast_2d(new))
    if assume_normalized:
        mem = np.atleast_2d(mem)             # ← skip
    else:
        mem = _l2_normalize(np.atleast_2d(mem))
    ...
```

callsite (`MemoryWriteBlock`) で `assume_normalized=True` を指定.
`SemanticMemory.all_embeddings()` は L2 normalized 済みなので **意味的に
同じ結果, 計算が落ちる**. 公開 API kwarg default False で完全後方互換.

**B-9-b: `GiftValueEstimator._history` を deque 化**

```python
# Before
self._history: list[_UtteranceHistoryEntry] = []
def commit(self, utterance, now=None):
    self._history.append(...)
# → 無限増殖. estimate() の度に線形走査

# After
self._history: deque[_UtteranceHistoryEntry] = deque()
def commit(self, utterance, now=None):
    evict_threshold = self.cooldown * 2
    while self._history and (now - self._history[0].timestamp) > evict_threshold:
        self._history.popleft()
    self._history.append(...)
```

B-6 で `list_slice` が deque より 119x 遅化することを確認済みなので,
long-run で同じ pathology に陥る可能性のあった hot path を予防的に
deque 化. cooldown 倍率は誤差マージン.

**結果**: 全 1585 PASS 維持, 回帰なし.

#### 採用ゲート確認

| 項目 | 状態 |
|---|---|
| 5% 改善 | 達成 (B-2 で測定済) |
| 全 test 緑 | 1585 PASS |
| selector overhead | 該当なし (直接最適化) |
| 後方互換 | OK (kwarg default False) |

branch `optimize/core-2026-05-20` に commit. main にマージするかは
後日判断 (PR 後に user 承認).

---

## 4. 3 日通して見えた教訓 — 「Hebbian × Honest × Hub」

### 4.1 教訓 1: Hebbian-style 自動収束には UCB1 が必要

ε-greedy だけだと「収束した先が実は最良じゃない」を見抜けない. UCB1 の
exploration round で全 variant を公平試行することで, **真の最良に到達**
できる. これは TRIZ 40 原理の「事前作用」(原理 #10) と「自己制御」(原理 #25)
の組み合わせに近い.

production 注入候補:

- cosine 計算: embedding pre-normalize cache → 2-5x
- sliding window: list → deque 移行 → 2-5x
- ε-greedy → UCB1 切替: production hot path の自動収束

### 4.2 教訓 2: Honest disclosure はアルゴリズム設計でも有効

B-4 で「収束結果が実は最良ではない」を見抜けたのは **avg_latency_ms を別途
記録して比較できる observability があったため**. ベンチで「変に高速」が
出たら必ず内訳を疑え, は `feedback_benchmark_honest_disclosure` のルール
だが, これは **アルゴリズム設計レイヤーにも適用される** ということ.

lleval v0.1 で 5 因子分解を一次クラス機能にしたのは, この精神の延長.
「速く見える理由を分解する」が **個人 OSS が cloud 大手と戦える数少ない武器**.

### 4.3 教訓 3: research hub 化で agent が SOTA を踏める

`docs/research/` に SOTA / prior-art を畳むと, **自律 agent が次のセッション
で「先行研究は ?」と聞かれた時に 1 秒で答えられる**. これは TRIZ で言う
「資源探索」(原理 #5, #15) の AI 化.

普段の Claude セッションで「lleval って何を差別化しないといけないの?」と
聞いた時に, agent が `docs/research/lleval_sota.md` を読むだけで「4 ギャップ
ある, promptfoo を fork ではなく wrap が正解」と即答できる. **人間の調査の
労力を agent が引き継ぐ**.

### 4.4 副次的な学び — 「燃え尽きる日と整理する日を交互に置く」

5/19 (爆発) と 5/20 (構造化) のリズムは, 後から見ると **2 拍子のサイクル**
として有効. 5/18 が「火種」, 5/19 が「燃焼」, 5/20 が「結晶化”. これを
1 週間に 2 サイクル組めれば, 個人 OSS でも企業並みの output が出る.

「燃え尽きるなら全部燃やす」「燃え滓は必ず結晶に整える」, この 2 つを
ルールにすれば良い.

---

## 5. 数値で締め — 「桁を見せる」

3 日間の累積:

| 指標 | 値 |
|---|---|
| 関連リポジトリ | 8 (llive / llove / llmesh / fullsense / lldesign / lltrade / raptor / mcp-spatial-asset-profile) |
| 主要 commit (auto: 除く) | 80+ |
| 全 commit | 200+ |
| llive PASS 数 | 1393 → **1585** (+192) |
| llove PASS 数 | 771 → **796** (+25) |
| llmesh PASS 数 | 42 → **3086** (※測定範囲拡大込み, 純 +4) |
| 新規記事 (Qiita draft / spec / research) | 14+ |
| 新規要件定義 (LE-FX / COG-MESH / 商標 / 収益化 / 投資) | 6+ |
| 自律 agent セッション継続時間 | 累計 30h+ |

**個人 OSS は人海戦術ではなく, AI agent との二人羽織で時間を 2 倍にして
回す**, というのが本質的な答え.

---

## 6. 次セッションへの渡し

- **lleval v0.1 着手判断**: implementation notes に書いた wrap 設計を user に
  確認後, `furuse-kazufumi/lleval` repo init.
- **llive B-7 (audit JSONL sink) / B-8 (jsonschema 検証)**: optimize branch
  の続き. SynapticSelector を実 hot path に注入する候補.
- **credential 復旧**: Anthropic / Gemini / OpenAI の quota / API 回復後に
  comparison.md の honest disclosure を再採点.
- **asciinema 録画**: COG-MESH 統合 demo (9 セクション) と llive demo,
  LoveApp + env attach の 3 本. articles_pause 解除後の SNS 素材.
- **articles pause 解除**: 解除済. 本記事は解除後の第 1 本目 (要 user 公開判断).

---

## 7. まとめ

3 日間で **8 リポ × 200+ commit** の出力を出せたのは, 個別の作業を高速化
したからではなく, **役割分担を割り切った**ためです.

- 人間: 仕様の方向性決定, 数字と goal の設定, 公開判断
- AI agent: 多前線の同時実装, テスト整備, 履歴整理, 進捗統合記事のドラフト

5/19 の 50+ commit と 5/20 の 50+ commit は, **片方が AI** の二人羽織で初めて
踏破できた量です. 「3 日で 200 commit したか」より「**3 日で燃え滓を結晶に整え
直せたか**」のほうが本質で, 後者には書き残し (PROGRESS / experiments /
memory) の整備が不可欠でした.

3 日で 8 リポ. 火種, 爆発, 結晶化. 次に何を燃やすかは 5/21 の朝に決めます.

---

## 関連 (cross-reference)

- [PROGRESS](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/PROGRESS.md) — 累積セッション履歴
- [NEXT_SESSION (auto)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.auto) — 毎ターン自動生成
- [Spec — lleval draft](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/requirements_lleval_v0.1_draft)
- [Spec — lleval implementation notes](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/lleval_v0_1_implementation_notes.md)
- [Research hub](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/.md)
- [Benchmark Policy](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/benchmarks/policy/.md)
- llive コア最適化 experiments log (本リポ外, `D:/projects/llive/docs/experiments/optimize_core_2026_05_20.md` の commit log を参照)
- maintainer memory:
  - `project_llive_core_optimization_2026_05_20`
  - `feedback_benchmark_honest_disclosure`
  - `feedback_qiita_long_form`
  - `feedback_article_humor_style`
  - `feedback_reader_attention_curve`
  - `feedback_articles_concept_hook`
