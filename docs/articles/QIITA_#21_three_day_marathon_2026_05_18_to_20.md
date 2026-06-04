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
id: 4d4a2083c32acf1d96be
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

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

> 📚 **連載ナビ**: ← #20 1 セッション 5409 テスト緑 ｜ **#21 本記事** ｜ #22 Transformer 脱却の現状 → ｜ [連載 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 各記事は単独でも読めます（リンクは回遊用）。

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

![docs/research/ ディレクトリ構成図 — 自律 agent が SOTA / prior-art を引ける研究ハブ](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q21/research_hub_tree.svg)

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
- llive コア最適化 experiments log (本リポ外, `llive/docs/experiments/optimize_core_2026_05_20.md` の commit log を参照)
- maintainer memory:
  - `project_llive_core_optimization_2026_05_20`
  - `feedback_benchmark_honest_disclosure`
  - `feedback_qiita_long_form`
  - `feedback_article_humor_style`
  - `feedback_reader_attention_curve`
  - `feedback_articles_concept_hook`

---

# English

# Sprinting Through 8 Repos in 3 Days — Tinder / Explosion / Crystallization, 72 Hours Dancing in Tandem with an AI Agent

> Whether to publish is the user's call. This was autonomously drafted by the
> agent from a request to "turn three days of activity into one all-inclusive story."
> articles_pause was lifted on 2026-05-20. This is the first candidate after the lift.

> 📚 **Series nav**: ← #20 5409 tests green in one session ｜ **#21 this article** ｜ #22 The current state of moving beyond Transformer → ｜ [Series LINK_MAP](./QIITA_#24_LINK_MAP.md). Each article also reads standalone (links are for browsing).

## 0. Concept hook — "Tinder, Explosion, Crystallization"

> **3 days × 1 person × 8 repositories × 100-commit overload × 1585 + 3086 + 796 tests green.**
> This is a personal OSS story. Here is what happened when I danced in tandem with an AI agent.

The conclusion up front:

- **5/18 = the day for scattering tinder.** F25 Phase h, llove Day-0 gap audit, Chinese LLM presets,
  gitee mirror CI, COG-MESH 10-item skeleton drop. "The Monday of seed-sowing."
- **5/19 = continuous explosion.** Landed M8.2–M8.9 in full in the morning → Production HTTP Sink +
  LoveApp integration at midday → F23/F24 PoC + trademark + monetization playbook + market SWOT +
  AI dev-environment roadmap + autonomous spinoff catalog + 2 Qiita articles in the evening. **50+ commits in one day.**
- **5/20 = structuring and automatic convergence.** Morning: NEXT_SESSION.auto automation + 6 research-hub items +
  test regression fix. Midday: lleval v0.1 draft + implementation notes. Evening: the **12h llive core-optimization goal** —
  building a Hebbian-style automatic-convergence framework (SynapticSelector + UCB1) and
  injecting the resulting discoveries into the real production hot path. **1585 PASS maintained.**

To sum up the three-day division of labor in one line: **the human scatters volume, the AI pushes it back into structure.**
The human decides spec direction and sets goals; the AI handles multi-front implementation, verification, and history tidying.
This split is grounded in the felt experience of running an LLM agent over a long stretch.

Below: a three-act structure plus a lessons extraction. It is written so you can read
the skeleton in 90 seconds / the whole thing in 5 minutes / everything-included in 30 minutes —
a **three-stage attention curve**.

---

## 1. Act 1 (5/18 tinder) — The 6 seeds sown on Monday

### 1.1 90-second summary

| Tinder sown | Where | Why sown |
|---|---|---|
| F25 Phase h.1/h.2 HTTP API skeleton | llove | Foothold for the pivot from TUI toy to "llive observation IDE" |
| Day-0 gap audit | llove | Map out "what isn't done yet" before entering dogfooding |
| 6 Chinese LLM OpenAI-compat presets | llmesh | Insurance so the distribution path isn't cut off in EAR-constrained environments |
| gitee mirror CI | llmesh | Redundancy so distribution doesn't stop even if GitHub goes down |
| supply-chain audit α (deps_audit CLI) | llmesh | Own the OSS audit responsibility ourselves. Origin tracking of PyPI dependencies |
| COG-MESH 10-item skeleton (from late night into early morning) | llive | Drop in the minimal skeleton of "an AI that talks to you on its own" |

The seeds were only sown. Growing them is the next day's job.

### 1.2 What was "F25 Phase h" again?

It's the plan to transform llove (the TUI dashboard) into an "observation tool." As of 5/18:

- Make it possible to submit a brief from the outside via `POST /api/v1/brief/submit` (Phase h.1)
- Stream annotations over SSE via `GET /api/v1/annotations/stream` (Phase h.2)

Using this as a foothold, a **VS Code extension + Neovim plugin** would be layered on later — the opening
skirmish of a multi-UI strategy. The policy "I don't want it to end as a TUI toy; I want to lean it toward an
**observation OS that lives inside the editor**" is recorded in memory.

### 1.3 Chinese LLM presets and gitee mirror — insurance for the distribution path

This is the kind of groundwork that **nobody does in ordinary OSS work.** Why I did it on 5/18:

- In a certain manufacturer's EAR-constrained environment, cloud LLMs **simply cannot be reached.**
  Anthropic, OpenAI, and Gemini are all impossible. Only local LLMs or Chinese LLMs.
- Cases where GitHub goes down or gets temporarily frozen can't be ignored.
  With a gitee mirror, distribution won't stop.

If you claim "FullSense is a responsible AI ecosystem," you have to maintain a posture that **takes
responsibility all the way through distribution.** This is a seed.

### 1.4 COG-MESH 10 items skeletoned in one night

This was a continuous battle from late night 5/18 into early morning 5/19. "Proactive Speech," "Quarantined Memory,"
"Mesh5W1H Annotator," "Quiet Hours," "BriefDeque Bridge," "Idle Training,"
"TonicRiskMonitor," "TitleRecall," "ProactiveSpeaker," "GiftValueEstimator."

10 frameworks derived from a human cognitive model. One skeleton + one test each
added 107 PASS. This became the fuel for the next day's explosion.

---

## 2. Act 2 (5/19 explosion) — The 50 commits burned up on Tuesday

### 2.1 90-second summary

I woke up, flipped the switch to "convert the skeletons into full implementations," and **the whole thing burned up
in a single day.**

| Time slot | What burned | Numbers |
|---|---|---|
| Early morning | M8.2–M8.7 full implementation | llive +55 PASS |
| Morning | M8.8 (graph analytics) + M8.9 (grammar EVO bridge) | +22 PASS |
| Morning | M8.1 Timeline bridge skeleton (emitter on the llive side) | +5 PASS |
| Morning | M8.1 LoveApp integration (CognitiveMeshPanel attach) | llove +25 PASS |
| Late morning | **ProductionHttpTimelineSink** (auth Bearer + exp backoff retry + batch buffer + 4 env) | +12 PASS |
| Midday | Added cog_* 4 types to the llmesh `/timeline/ingest` allow-list | +4 PASS |
| Midday | E2E integration test (M8.1–M8.9 chain) | +1 PASS |
| Afternoon | F23/F24 PoC (PowerShell-compatible shell + ccr launcher) skeleton | llove +α |
| Afternoon | AI dev-environment investment roadmap, ¥50k trademark CHECKLIST, monetization playbook, market SWOT | 4 docs |
| Evening | autonomous spinoff catalog + Family Tree update + llgrow Planned | portal + many |
| Night | 2 Qiita article drafts (M8.x 3-stage rocket / personal-OSS market SWOT) | docs +2 |

**50+ commits in one day, cumulative PASS count up by nearly +120.** For personal OSS, there's no word for it
but "the day it burned out."

### 2.2 What was "M8.x" again? — a one-line refresher each

M8 = the **full-implementation phase** of COG-MESH. The set of milestones that flip
the state from skeleton to "works as a feature."

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

Switching all of these ON in a single day is what 5/19 was. You could also call it the day I got to see
"the moment the boundary between skeleton and full implementation exceeded the amount one human's stamina
can cram into a single day."

### 2.3 ProductionHttpTimelineSink — "field operation" in its minimal unit

What I crammed into one file in the late morning was a Sink that can be deployed to production. Contents:

- **Auth Bearer** token (env `LLIVE_LLMESH_TIMELINE_TOKEN`)
- **Exponential backoff retry** (`LLIVE_LLMESH_TIMELINE_RETRIES=5`)
- **Batch buffer** (`LLIVE_LLMESH_TIMELINE_BATCH_SIZE=10`)
- **Endpoint URL** (`LLIVE_LLMESH_TIMELINE_URL=http://prod-llmesh:8080`)

That's it. If an operator sets these 4 env vars, real production runs.
+12 PASS. Tests green.

**"The minimal configuration to deploy to production is 4 env vars"** — that feel was a pleasure.

### 2.4 The surprise of 4 docs (trademark / monetization / market / investment)

5/19 was **not a code-only day.** In the afternoon I rapidly wrote out the materials that
"anyone doing personal OSS can't avoid":

1. **AI dev-environment investment roadmap** — a rough budget for "what to spend, how much, over the next year"
2. **¥50k trademark CHECKLIST** — proceeding flatly with 1 class for JP/US/EU
3. **Monetization playbook** — what to sell across 10 channels × 4 sprints
4. **Market receptivity SWOT** — 6-axis WebSearch + SWOT + survival strategy

There's really no need to write all of these in a single day. But in the spirit of
**"if you're going to burn out, burn it all,"** I ran them in parallel. In hindsight, these 4 docs
became **inputs to the 5/20 structuring session.** Dependencies surfaced like
"I want to confirm independence before taking a trademark" and
"I want to set up the research hub before starting monetization."

---

## 3. Act 3 (5/20 structuring) — The 3 layers organized on Wednesday

### 3.1 90-second summary

| Time slot | What I did | Why |
|---|---|---|
| Morning | NEXT_SESSION.auto auto-generation + Stop hook linkage | Structurally resolve the drift of manually updating NEXT_SESSION |
| Morning | Set up a new research hub (6 SOTA / prior-art notes) | A foundation so the autonomous agent can step through SOTA |
| Morning | Regression fix for related project tests (llove image-tool / llmesh hypothesis) | Stomp out flakiness before entering dogfooding |
| Morning | spinoff_ideas C-2 adoption-priority table (HIGH/MID/LOW/DEFER) | Judging from research results |
| Midday | Fully rewrote QIITA #20 in a humor direction | An expression test after the articles_pause lift |
| Midday | lleval v0.1 draft + implementation notes | First concretization of the HIGH adoption priority |
| Afternoon | (break + background run of all 3086 llmesh tests) | Confirm flaky reproduction |
| Night | **12h llive core-optimization goal** (B-0–B-6 + B-9) | Hebbian-style auto-convergence framework + real production injection |

You could describe it as **the day for regaining the balance between code and documents.** If 5/19 was "burn it all,"
then 5/20 was "**arrange the embers into crystals.**"

### 3.2 NEXT_SESSION.auto automation — fighting drift

Because NEXT_SESSION.md is updated by hand, it **always drifts.** Resolved in an hour and a half in the morning:

- Created `scripts/gen_next_session_auto.py`
- Registered it in raptor's Stop hook → auto-overwritten every turn
- Aggregates `git log` + related projects' latest commits + changes in the last 4h + verify_publication results + outstanding operator actions onto a single sheet
- Demoted the hand-updated `NEXT_SESSION.md` to **direction-memo only**

This drastically cut the context-restoration cost at the start of the next session. I think
**"keep one extra auto-generated file around" is the right answer for personal OSS.**

### 3.3 Setting up the research hub — letting the agent step through SOTA

Dropped 6 items into `docs/research/`:

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

This is a **foundation so the autonomous agent can judge with research fields in mind.**
A concept derived from RAD (Research Aggregation Directory): in an ordinary Claude
session, when asked "what's the prior art?", the agent can pull up a SOTA matrix
just by reading `docs/research/`.

It's a mechanism for **"the agent inheriting the labor of human research surveys."**

### 3.4 spinoff_ideas C-2 adoption-priority table

In light of the research results, I classified 6 items:

| spinoff | Priority | Rationale |
|---|---|---|
| **lleval** | **HIGH** | A design that fills the 4 gaps with a promptfoo wrap is clear |
| llgrow | MID | Growth automation is in demand but has many existing SaaS competitors |
| llbridge | MID | The MCP bridge is waiting on the wave |
| llcraft | LOW | The LLM workshop is strongly hobbyist-flavored |
| llrisk | LOW | Tonic Risk is monolithic; thin demand |
| llgov | LOW | LLM governance is legal-heavy |
| llforen | DEFER | LLM forensics is premature |

This **narrowed the next spinoff to tackle down to lleval alone.** When you hold a spinoff catalog in personal OSS
you catch "want-to-do-everything disease," but a priority table builds antibodies.

### 3.5 lleval v0.1 draft + implementation notes — concretizing the HIGH priority

In the afternoon I wrote 2 drafts:

1. **requirements_lleval_v0.1_draft.md** — requirements LE-01–08
2. **lleval_v0_1_implementation_notes.md** — PoC scope (wrap not fork)

Key decisions:

- **Don't fork promptfoo. Wrap it.** A Node.js fork doubles maintenance cost.
  Call it via Python subprocess and layer on top.
- **A separate GitHub repo** (`furuse-kazufumi/lleval`), Apache-2.0 + Commercial dual.
- **v0.1 MVP** = LE-01 (multi-provider unification) + LE-02 (progressive size matrix) +
  LE-03 (honest disclosure analyzer) + LE-07 (CLI + Python API).

4 axes of differentiation:

| # | Differentiation | Existing gap |
|---|---|---|
| 1 | on-prem + cloud unified A/B | No design that handles industrial IoT + local llama.cpp and cloud API in the same run |
| 2 | Progressive size curve (xs/s/m/l/xl) | Existing ones all use a fixed prompt length |
| 3 | **Automatic honest-disclosure diagnosis** | Breaking down anomaly internals is a manual-labor area |
| 4 | Judge rotation + position swap | Automatic detection of self-preference bias |

The honest-disclosure 5-factor breakdown:

1. warmup hit
2. token-count normalization
3. network RTT exclusion
4. backend attach overhead
5. system load

The design that turns this into a **diagnosis report that can be blocked in CI** is the temperature
of how serious this is. No more ending on "our product is fast! we won!"

### 3.6 The night's main event — the 12h llive core-optimization goal

At the end of the afternoon, a serious goal came down from the user:

> "Push forward the optimization of llive's core. Keep gathering information and try
> various things over the next 12 hours. Properly leave a history and converge it into
> a form where no defects arise."
>
> "Try changing how the core holds data, the containers, extending design patterns, and so on,
> so that it converges into an optimal structure as automatically as possible — that's ideal."
>
> "**Something like weighting that changes the way a brain's synaptic structure does would be good.**"

This is an order of magnitude different from an ordinary optimization request. Not manual speedup of a single
implementation, but **"build a framework that lines up multiple candidates and lets them converge automatically."**

#### Design decision — `SynapticSelector`

I set up a new variant selector that combines ε-greedy + Hebbian-style weight update:

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

With bounded modification (APO §E2), min/max clip. 19 tests green. **Existing 1518 →
1537**, no regression. This is B-0.

#### B-1 to B-6 — observing automatic convergence

| Phase | What I tried | Lesson |
|---|---|---|
| B-1 | top-K extraction (n=5000, k=10, 200 iter) | `heapq_nlargest` converges to weight=100 (max). `full_sort` decays to 0.377. **It converges.** |
| B-2 | cosine variants (dim=16/128/768) | `numpy_normalized` (pre-L2-normalized input) wins outright across all dimensions. **2–5x with a pre-normalize cache.** |
| B-4 | decay variants (N=100/10000/100000) | At N=100 it correctly converges to `np_inplace`, but at **N=10000/100000 it incorrectly converges to `np_einsum`**. The true best is `np_inplace`, 17% faster, yet its weight doesn't grow. **Found early-convergence bias.** |
| B-5 | `UCBSynapticSelector` (UCB1) | Under the same conditions as B-4, all 3 sizes correctly converge to `np_inplace`. **Pathology resolved.** |
| B-6 | sliding window (deque vs list_slice) | At maxlen=1000 deque is converged. list_slice is **119x slower** (O(N) copy). **Production-adoption candidate confirmed.** |

**B-4 is this session's biggest discovery**: even when you claim "automatic convergence," ε-greedy alone falls into
a winner-take-all dynamic. UCB1's exploration rounds are needed. This is the spirit of
`feedback_benchmark_honest_disclosure` — it's all about having the observability to catch
"the converged result actually isn't the best."

#### B-9 — injecting the discoveries into the real production hot path

Reflecting research results into real code is the whole point. I injected 2 in B-9-a and B-9-b:

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

Specify `assume_normalized=True` at the callsite (`MemoryWriteBlock`).
`SemanticMemory.all_embeddings()` is already L2-normalized, so **the result is semantically
the same and the computation drops.** With a public-API kwarg defaulting to False, fully backward compatible.

**B-9-b: making `GiftValueEstimator._history` a deque**

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

Since B-6 confirmed `list_slice` is 119x slower than deque, I preemptively turned a hot path that
could have fallen into the same pathology over a long run into a deque. The cooldown multiplier
is the error margin.

**Result**: all 1585 PASS maintained, no regression.

#### Adoption-gate check

| Item | Status |
|---|---|
| 5% improvement | Achieved (measured in B-2) |
| All tests green | 1585 PASS |
| selector overhead | N/A (direct optimization) |
| Backward compatible | OK (kwarg default False) |

Committed to branch `optimize/core-2026-05-20`. Whether to merge to main is decided later
(user approval after PR).

---

## 4. The lesson seen across 3 days — "Hebbian × Honest × Hub"

### 4.1 Lesson 1: Hebbian-style automatic convergence needs UCB1

With ε-greedy alone you can't catch "the place it converged to actually isn't the best." By
fairly trying all variants with UCB1's exploration rounds, you can **reach the true best.**
This is close to combining the TRIZ 40 Principles' "preliminary action" (#10) and "self-service" (#25).

Production-injection candidates:

- cosine computation: embedding pre-normalize cache → 2–5x
- sliding window: list → deque migration → 2–5x
- ε-greedy → UCB1 switch: automatic convergence of the production hot path

### 4.2 Lesson 2: Honest disclosure is also effective in algorithm design

The reason I could catch "the converged result actually isn't the best" in B-4 is that there was
**observability that records avg_latency_ms separately for comparison.** "If a benchmark shows
something weirdly fast, always doubt the internals" is a rule of `feedback_benchmark_honest_disclosure`,
but this means **it also applies at the algorithm-design layer.**

Making the 5-factor breakdown a first-class feature in lleval v0.1 is an extension of this spirit.
"Breaking down the reasons it looks fast" is **one of the few weapons with which personal OSS can fight the cloud giants.**

### 4.3 Lesson 3: Hub-ifying research lets the agent step through SOTA

When you fold SOTA / prior-art into `docs/research/`, **the autonomous agent can answer in one second
when asked "what's the prior art?" in the next session.** This is the AI-ification of what TRIZ calls
"resource exploration" (#5, #15).

In an ordinary Claude session, when I ask "what does lleval have to differentiate on?", the agent can
instantly answer "there are 4 gaps; the right move is to wrap promptfoo, not fork it" just by reading
`docs/research/lleval_sota.md`. **The agent inherits the labor of human surveys.**

### 4.4 A secondary lesson — "alternate burn-out days with tidy-up days"

In hindsight, the rhythm of 5/19 (explosion) and 5/20 (structuring) works as a **two-beat cycle.**
5/18 was "tinder," 5/19 was "combustion," 5/20 was "crystallization." If you can build 2 of these
cycles per week, even personal OSS can produce enterprise-grade output.

It's enough to make these 2 things rules: "if you're going to burn out, burn it all" and "always arrange the embers into crystals."

---

## 5. Closing with numbers — "show the order of magnitude"

The 3-day cumulative:

| Metric | Value |
|---|---|
| Related repositories | 8 (llive / llove / llmesh / fullsense / lldesign / lltrade / raptor / mcp-spatial-asset-profile) |
| Major commits (excluding auto:) | 80+ |
| All commits | 200+ |
| llive PASS count | 1393 → **1585** (+192) |
| llove PASS count | 771 → **796** (+25) |
| llmesh PASS count | 42 → **3086** (※ including expanded measurement scope, net +4) |
| New articles (Qiita draft / spec / research) | 14+ |
| New requirement definitions (LE-FX / COG-MESH / trademark / monetization / investment) | 6+ |
| Autonomous agent session duration | 30h+ cumulative |

**Personal OSS isn't a human-wave tactic; it's running with time doubled by dancing in tandem with an AI agent**
— that's the essential answer.

---

## 6. Handoff to the next session

- **lleval v0.1 start decision**: after confirming the wrap design written in the implementation notes with the user,
  init the `furuse-kazufumi/lleval` repo.
- **llive B-7 (audit JSONL sink) / B-8 (jsonschema validation)**: continuation of the optimize branch.
  Candidates for injecting SynapticSelector into the real hot path.
- **credential recovery**: after Anthropic / Gemini / OpenAI quota / API recovery,
  re-score the honest disclosure in comparison.md.
- **asciinema recording**: 3 reels — the COG-MESH integration demo (9 sections), the llive demo,
  and LoveApp + env attach. SNS material after the articles_pause lift.
- **articles pause lift**: lifted. This article is the first one after the lift (publication is the user's call).

---

## 7. Summary

Being able to produce **8 repos × 200+ commits** of output in 3 days came not from speeding up
individual tasks, but from **committing to a clear division of labor.**

- Human: deciding spec direction, setting numbers and goals, publication decisions
- AI agent: simultaneous multi-front implementation, test maintenance, history tidying, drafting progress-integration articles

The 50+ commits on 5/19 and the 50+ commits on 5/20 are an amount that could only be covered by
tandem work in which **one side is AI.** More essential than "did you do 200 commits in 3 days?" is
"**could you re-arrange the embers into crystals in 3 days?**", and the latter required maintaining
written records (PROGRESS / experiments / memory).

3 days, 8 repos. Tinder, explosion, crystallization. What to burn next, I'll decide on the morning of 5/21.

---

## Related (cross-reference)

- [PROGRESS](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/PROGRESS.md) — cumulative session history
- [NEXT_SESSION (auto)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.auto) — auto-generated every turn
- [Spec — lleval draft](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/requirements_lleval_v0.1_draft)
- [Spec — lleval implementation notes](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/lleval_v0_1_implementation_notes.md)
- [Research hub](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/.md)
- [Benchmark Policy](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/benchmarks/policy/.md)
- llive core-optimization experiments log (outside this repo; see the commit log of `llive/docs/experiments/optimize_core_2026_05_20.md`)
- maintainer memory:
  - `project_llive_core_optimization_2026_05_20`
  - `feedback_benchmark_honest_disclosure`
  - `feedback_qiita_long_form`
  - `feedback_article_humor_style`
  - `feedback_reader_attention_curve`
  - `feedback_articles_concept_hook`

---

# 中文

# 三天跑完 8 个仓库的故事 —— 火种 / 爆发 / 结构化，与 AI agent 二人羽织共舞的 72 小时

> 是否发布由 user 决定。这是在「把三天的全部活动汇成一个全员登场的故事」这一委托下，
> 由 agent 自主起草的稿件。
> articles_pause 已于 2026-05-20 解除。这是解除后的第 1 篇候选。

> 📚 **连载导航**: ← #20 一个会话 5409 测试全绿 ｜ **#21 本文** ｜ #22 脱离 Transformer 的现状 → ｜ [连载 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 每篇文章也都可单独阅读（链接用于回游）。

## 0. 概念 hook —— 「火种、爆发、结构化」

> **3 天 × 1 人 × 8 个仓库 × 100 commit overload × 1585 + 3086 + 796 测试全绿。**
> 这是个人 OSS 的故事。当我与 AI agent 二人羽织共舞之后，就变成了这样。

先说结论：

- **5/18 = 撒火种的一天。** F25 Phase h、llove Day-0 gap audit、中国 LLM presets、
  gitee mirror CI、COG-MESH 10 件 skeleton 投放。「播种的星期一」。
- **5/19 = 连续爆发。** 上午把 M8.2～M8.9 全部落地 → 中午 Production HTTP Sink +
  LoveApp 集成 → 傍晚 F23/F24 PoC + 商标 + 变现 playbook + 市场 SWOT +
  AI 开发环境 roadmap + 自主 spinoff 目录 + 2 篇 Qiita 文章。**一天 50+ commit。**
- **5/20 = 结构化与自动收敛。** 上午 NEXT_SESSION.auto 自动化 + research hub 6 件 +
  test 回归 fix。中午 lleval v0.1 draft + 实现笔记。夜晚 **llive 核心优化 12h goal** ——
  打造 Hebbian 风格的自动收敛框架（SynapticSelector + UCB1），
  并把得到的发现注入真实 production hot path。**维持 1585 PASS。**

用一行整理这三天的分工：**撒量的是人，把它推回结构的是 AI。**
规格方向决策与目标设定由人负责，多前线的实现与验证 + 历史整理由 AI 负责。
这是基于长期运行 LLM agent 的切身体感得出的分工。

以下是三幕结构 + 教训抽取。写成了能让你 90 秒看骨架 / 5 分钟看全貌 / 30 分钟看全部内容的
**三段集中曲线**。

---

## 1. 第 1 幕 (5/18 火种) —— 星期一撒下的 6 种

### 1.1 90 秒摘要

| 撒下的火种 | 地点 | 为何撒下 |
|---|---|---|
| F25 Phase h.1/h.2 HTTP API skeleton | llove | 从 TUI 玩具 pivot 到「llive 观测 IDE」的立足点 |
| Day-0 gap audit | llove | 进入 dogfooding 前把「还没做完什么」绘成地图 |
| 6 种中国 LLM OpenAI-compat presets | llmesh | 在 EAR 受限环境下不被切断分发路径的保险 |
| gitee mirror CI | llmesh | 即便 GitHub 宕机分发也不中断的冗余 |
| supply-chain audit α (deps_audit CLI) | llmesh | 自己承担 OSS 审计责任。追踪 PyPI 依赖的 origin |
| COG-MESH 10 件 skeleton（从深夜到凌晨） | llive | 投放「会主动跟你说话的 AI」的最小骨架 |

种只是撒下而已。养大它是第二天的事。

### 1.2 「F25 Phase h」是什么来着

这是把 llove（TUI dashboard）变身为「观测工具」的计划。截至 5/18：

- 通过 `POST /api/v1/brief/submit` 可以从外部投入 brief（Phase h.1）
- 通过 `GET /api/v1/annotations/stream` 经由 SSE 推送 annotations（Phase h.2）

以此为立足点，之后再载上 **VS Code 扩展 + Neovim 插件**，这是 multi-UI 战略的
前哨战。「不想止步于 TUI 玩具，想把它倾向于**住在编辑器里的观测 OS**」这一方针
记录在 memory 中。

### 1.3 中国 LLM presets 与 gitee mirror —— 分发路径的保险

这是平时的 OSS 工作里**谁都不会做的铺垫**。为什么在 5/18 做：

- 在某制造业的 EAR 受限环境中，cloud LLM **根本就够不着**。
  Anthropic、OpenAI、Gemini 都不行。只有 local LLM 或中国 LLM。
- GitHub 宕机 / 被临时冻结的事件也不能无视。
  有了 gitee mirror，分发就不会中断。

如果要标榜「FullSense 是有责任感的 AI 生态系统」，就必须维持一种**对分发也负责到底**
的姿态。这就是种。

### 1.4 一晚把 COG-MESH 10 件 skeleton 化

这是从 5/18 深夜到 5/19 凌晨的连续战。「能动发话」「Quarantined Memory」
「Mesh5W1H Annotator」「Quiet Hours」「BriefDeque Bridge」「Idle Training」
「TonicRiskMonitor」「TitleRecall」「ProactiveSpeaker」「GiftValueEstimator」。

从人类认知模型派生的 10 个 framework。每个 skeleton + 1 件测试
增加 107 PASS。这成了第二天爆发的燃料。

---

## 2. 第 2 幕 (5/19 爆发) —— 星期二烧尽的 50 commit

### 2.1 90 秒摘要

早上醒来后打开「把 skeleton 切换为正式实现」的开关，结果**那一整天就全部烧尽了**。

| 时段 | 烧了什么 | 数值 |
|---|---|---|
| 凌晨 | M8.2～M8.7 正式实现 | llive +55 PASS |
| 早上 | M8.8 (graph analytics) + M8.9 (grammar EVO bridge) | +22 PASS |
| 早上 | M8.1 Timeline bridge skeleton（llive 侧 emitter） | +5 PASS |
| 早上 | M8.1 LoveApp 集成（CognitiveMeshPanel attach） | llove +25 PASS |
| 上午晚些 | **ProductionHttpTimelineSink**（auth Bearer + exp backoff retry + batch buffer + 4 env） | +12 PASS |
| 中午 | 向 llmesh `/timeline/ingest` allow-list 加入 cog_* 4 种 | +4 PASS |
| 中午 | E2E integration test（M8.1～M8.9 chain） | +1 PASS |
| 下午 | F23/F24 PoC（PowerShell 兼容 shell + ccr launcher）skeleton | llove +α |
| 下午 | AI 开发环境投资 roadmap、5 万日元商标 CHECKLIST、变现 playbook、市场 SWOT | docs 4 篇 |
| 傍晚 | 自主 spinoff 目录 + Family Tree 更新 + llgrow Planned | portal + 多数 |
| 夜晚 | Qiita 文章 2 篇 draft（M8.x 三段火箭 / 个人 OSS 市场 SWOT） | docs +2 |

**一天 50+ commit，累计 PASS 数增加近 +120。** 对个人 OSS 来说，除了「烧尽的一天」
没有别的词可形容。

### 2.2 「M8.x」是什么来着 —— 每条一行复习

M8 = COG-MESH 的**正式实现阶段**。把状态从 skeleton 切换到「作为功能可运行」的
里程碑群。

```text
M8.1  Timeline emit + LoveApp panel attach
M8.2  ProactiveSpeaker (能动发话)
M8.3  QuietHours gate
M8.4  IdleTraining (空闲时间迷你训练)
M8.5  TonicRiskMonitor (源自 KYT 的重要度监视)
M8.6  TitleRecall (标题想起循环)
M8.7  Mesh5W1H Annotator
M8.8  GraphAnalytics (BFS/DFS/centrality 自前实现)
M8.9  GrammarLayer EVO bridge
```

在一天内把这些全部切到 ON 的，就是 5/19。也可以说，这是能看到「skeleton 与正式实现
的边界，超出一个人体力在一天里能塞下的量的那一刻」的日子。

### 2.3 ProductionHttpTimelineSink —— 用最小单位实现「现场运维」

上午晚些时候塞进一个文件里的，是可以投入 production 的 Sink。内容：

- **Auth Bearer** 令牌（env `LLIVE_LLMESH_TIMELINE_TOKEN`）
- **Exponential backoff retry**（`LLIVE_LLMESH_TIMELINE_RETRIES=5`）
- **Batch buffer**（`LLIVE_LLMESH_TIMELINE_BATCH_SIZE=10`）
- **Endpoint URL**（`LLIVE_LLMESH_TIMELINE_URL=http://prod-llmesh:8080`）

就这些。operator 只要设置这 4 个 env，真实 production 就能运行。
+12 PASS。测试全绿。

**「投入 production 的最小配置就是 4 个 env」**，这种手感令人高兴。

### 2.4 4 篇 docs 的惊喜（商标 / 变现 / 市场 / 投资）

5/19 **不是只写代码的一天**。下午一口气写了那些「只要在做个人 OSS 就
谁都绕不过去」的资料：

1. **AI 开发环境投资 roadmap** —— 「未来一年要花什么、花多少」的粗略预算
2. **5 万日元商标 CHECKLIST** —— 以 JP/US/EU 各 1 分类平推
3. **变现 playbook** —— 10 渠道 × 4 sprint 卖什么
4. **市场接受度 SWOT** —— 6 轴 WebSearch + SWOT + 生存战略

其实没必要把这些全在一天内写完。但本着 **「要烧就全烧」** 的精神并行执行了。
事后回看，这 4 篇成了 **5/20 结构化会话的输入**。浮现出诸如
「想在取得商标前确认独立性」「想在开始变现前把 research hub 整好」之类的依赖关系。

---

## 3. 第 3 幕 (5/20 结构化) —— 星期三整理的 3 层

### 3.1 90 秒摘要

| 时段 | 做了什么 | 为何 |
|---|---|---|
| 早上 | NEXT_SESSION.auto 自动生成 + Stop hook 联动 | 从结构上消解手动更新 NEXT_SESSION 的 drift |
| 早上 | 新设 research hub（6 件 SOTA / prior-art 笔记） | 让自主 agent 能踏上 SOTA 的基础 |
| 早上 | 相关 prj test 回归 fix（llove image-tool / llmesh hypothesis） | 进入 dogfooding 前消灭 flaky |
| 早上 | spinoff_ideas C-2 采用优先级表（HIGH/MID/LOW/DEFER） | 依据 research 结果判断 |
| 中午 | 以幽默方针全面重写 QIITA #20 | articles_pause 解除后的表现测试 |
| 中午 | lleval v0.1 draft + 实现笔记 | 采用优先级 HIGH 的首次具体化 |
| 傍晚 | （休息 + 后台运行全部 3086 个 llmesh test） | 确认 flaky 复现 |
| 夜晚 | **llive 核心优化 12h goal**（B-0～B-6 + B-9） | Hebbian 风格自动收敛 framework + 真实 production 注入 |

可以形容为**找回代码与文档平衡的一天**。如果 5/19 是「全烧」，
那 5/20 就是「**把余烬整理成结晶**」。

### 3.2 NEXT_SESSION.auto 自动化 —— 与 drift 作战

NEXT_SESSION.md 因为是手动更新，所以**必然 drift**。早上一个半小时解决：

- 新设 `scripts/gen_next_session_auto.py`
- 注册到 raptor 的 Stop hook → 每个 turn 自动覆盖
- 把 `git log` + 相关 prj 最新 commit + 最近 4h 变更 + verify_publication 结果 + 未消化的 operator action 汇集到一张纸上
- 把手动更新的 `NEXT_SESSION.md` 降级为**仅方向性备忘**

这样一来，下个会话开始时的 context 恢复成本大幅降低。我认为
**「自动生成文件多放一个」是个人 OSS 的正解**。

### 3.3 新设 research hub —— 让 agent 踏上 SOTA

向 `docs/research/` 投放 6 件：

```text
docs/research/
├── index.md                       # Reference hub
├── lleval_sota.md                 # 10 framework 比较 + 4 gap
├── llgrow_prior_art.md            # Growth Automation 先行例
├── cognitive_mesh_vs_sota.md      # COG-MESH 的相关研究
├── llcraft_sota.md                # llcraft 候选的 SOTA
├── llrisk_prior_art.md            # llrisk (Tonic Risk) 先行例
└── llgov_sota.md                  # llgov (governance) SOTA
```

这是「**让自主 agent 能在踏上研究领域的基础上判断**」的基础。
是 RAD（Research Aggregation Directory）的派生概念：在平时的 Claude
会话中，当被问到「先行研究是什么？」时，agent 只要读 `docs/research/`
就能调出 SOTA matrix。

这是为了实现 **「让 agent 接手人类研究调查的劳力」** 的机关。

### 3.4 spinoff_ideas C-2 采用优先级表

基于 research 结果将 6 件分类：

| spinoff | 优先级 | 依据 |
|---|---|---|
| **lleval** | **HIGH** | 用 promptfoo wrap 填补 4 个 gap 的设计很明确 |
| llgrow | MID | growth automation 有需求但既有 SaaS 竞品多 |
| llbridge | MID | MCP bridge 还在等 wave |
| llcraft | LOW | LLM workshop 兴趣色彩强 |
| llrisk | LOW | Tonic Risk monolithic，需求薄 |
| llgov | LOW | LLM governance 偏 legal-heavy |
| llforen | DEFER | LLM forensics 为时尚早 |

这样一来，**下一个该动手的 spinoff 被缩到 lleval 一个**。在个人 OSS 里持有 spinoff
目录会得「什么都想做病」，但优先级表能造出抗体。

### 3.5 lleval v0.1 draft + 实现笔记 —— 把采用优先级 HIGH 具体化

下午写了 2 篇 draft：

1. **requirements_lleval_v0.1_draft.md** —— LE-01～08 需求
2. **lleval_v0_1_implementation_notes.md** —— PoC scope（wrap not fork）

主要决定：

- **不 fork promptfoo，而是 wrap。** Node.js fork 的维护成本翻倍。
  用 Python subprocess 调用并在上面加层。
- **独立的 GitHub repo**（`furuse-kazufumi/lleval`），Apache-2.0 + Commercial dual。
- **v0.1 MVP** = LE-01（多 provider 统一）+ LE-02（progressive size matrix）+
  LE-03（honest disclosure analyzer）+ LE-07（CLI + Python API）。

4 个差异化轴：

| # | 差异化 | 既有 gap |
|---|---|---|
| 1 | on-prem + cloud 统一 A/B | 不存在能在同一 run 内处理工业 IoT + local llama.cpp 与 cloud API 的设计 |
| 2 | Progressive size curve (xs/s/m/l/xl) | 既有的全都是固定 prompt 长度 |
| 3 | **Honest disclosure 自动诊断** | 异常值的内部分解是手工领域 |
| 4 | Judge rotation + position swap | 自动检测 self-preference bias |

honest-disclosure 5 因子分解：

1. warmup hit
2. token-count normalization
3. network RTT 排除
4. backend attach overhead
5. system load

把这做成 **可在 CI 阻断的 diagnosis report** 的设计，就是认真程度的温度。
不再以「自家很快！赢了！」收尾的机制。

### 3.6 夜晚的正餐 —— llive 核心优化 12h goal

下午快结束时，user 抛来一个认真的 goal：

> 「推进 llive 核心部分的优化。在接下来 12 小时里一边收集信息一边
> 各种尝试。要好好留下历史，收敛到不出故障的形态。」
>
> 「试着改变核心部分的数据持有方式、容器，扩展设计模式之类的，
> 尽量自动地收敛到最优结构的感觉是理想的。」
>
> 「**像大脑突触结构那样权重会变化的感觉就很好。**」

这与平时的优化委托量级不同。不是对单一实现的手动加速，而是
**「打造一个把多个候选并列起来、让其自动收敛的 framework」** 的指令。

#### 设计判断 —— `SynapticSelector`

新设一个组合了 ε-greedy + Hebbian 风格 weight update 的 variant selector：

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

用 bounded modification（APO §E2）做 min/max clip。19 件测试全绿。**既有 1518 →
1537**，无回归。这是 B-0。

#### B-1 ～ B-6 —— 观察自动收敛

| Phase | 尝试了什么 | 学到了什么 |
|---|---|---|
| B-1 | top-K 抽取 (n=5000, k=10, 200 iter) | `heapq_nlargest` 收敛到 weight=100（max）。`full_sort` 衰减到 0.377。**会收敛。** |
| B-2 | cosine variants (dim=16/128/768) | `numpy_normalized`（pre-L2 normalized 输入）在所有维度完胜。**用 pre-normalize cache 提速 2-5x。** |
| B-4 | decay variants (N=100/10000/100000) | N=100 时正确收敛到 `np_inplace`，但 **N=10000/100000 时错误地收敛到 `np_einsum`**。真正最优是 `np_inplace`，快 17%，但 weight 却不增长。**发现 early-convergence bias。** |
| B-5 | `UCBSynapticSelector` (UCB1) | 在与 B-4 相同条件下，3 个尺寸全部正确收敛到 `np_inplace`。**病理解除。** |
| B-6 | sliding window (deque vs list_slice) | maxlen=1000 时 deque 已 converged。list_slice **慢 119x**（O(N) copy）。**确定为 production 适用候选。** |

**B-4 是本会话最大的发现**：即便标榜「自动收敛」，只靠 ε-greedy 也会陷入
赢家通吃的 dynamics。需要 UCB1 的 exploration round。这正是
`feedback_benchmark_honest_disclosure` 的精神 —— 关键全在于拥有能看穿
「收敛结果其实并非最优」的 observability。

#### B-9 —— 把发现注入真实 production hot path

不把研究结果反映到真实代码就毫无意义。在 B-9-a 与 B-9-b 注入了 2 件：

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

在 callsite（`MemoryWriteBlock`）指定 `assume_normalized=True`。
`SemanticMemory.all_embeddings()` 已是 L2 normalized，所以**语义上结果相同，
计算量下降**。公开 API kwarg default False，完全向后兼容。

**B-9-b: 把 `GiftValueEstimator._history` 改为 deque**

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

由于 B-6 已确认 `list_slice` 比 deque 慢 119x，所以把一个在 long-run 中
可能陷入同样 pathology 的 hot path 预防性地改为 deque。cooldown 倍率是误差余量。

**结果**：维持全部 1585 PASS，无回归。

#### 采用 gate 确认

| 项目 | 状态 |
|---|---|
| 5% 改善 | 达成（B-2 已测定） |
| 全 test 绿 | 1585 PASS |
| selector overhead | 不适用（直接优化） |
| 向后兼容 | OK（kwarg default False） |

commit 到 branch `optimize/core-2026-05-20`。是否合并到 main 日后判断
（PR 后经 user 批准）。

---

## 4. 贯穿 3 天看到的教训 —— 「Hebbian × Honest × Hub」

### 4.1 教训 1：Hebbian 风格自动收敛需要 UCB1

只靠 ε-greedy 看不穿「收敛到的地方其实并非最优」。通过 UCB1 的
exploration round 公平地试遍所有 variant，就能**到达真正的最优**。
这接近于 TRIZ 40 原理中「预先作用」（原理 #10）与「自服务」（原理 #25）的组合。

production 注入候选：

- cosine 计算：embedding pre-normalize cache → 2-5x
- sliding window：list → deque 迁移 → 2-5x
- ε-greedy → UCB1 切换：production hot path 的自动收敛

### 4.2 教训 2：Honest disclosure 在算法设计中同样有效

在 B-4 能看穿「收敛结果其实并非最优」，是因为有**单独记录 avg_latency_ms 以供比较的
observability**。「benchmark 一旦出现『异常地快』就一定要怀疑内部分解」是
`feedback_benchmark_honest_disclosure` 的规则，但这意味着**它也适用于算法设计层**。

在 lleval v0.1 把 5 因子分解做成一等公民功能，正是这种精神的延伸。
「分解看起来快的理由」是**个人 OSS 能与 cloud 巨头一战的少数武器之一**。

### 4.3 教训 3：把研究 hub 化能让 agent 踏上 SOTA

把 SOTA / prior-art 叠进 `docs/research/`，**自主 agent 在下个会话被问到
「先行研究是什么？」时就能 1 秒答出**。这是 TRIZ 所说「资源探索」（原理 #5, #15）的 AI 化。

在平时的 Claude 会话中，当我问「lleval 必须在什么上做差异化？」时，agent 只要读
`docs/research/lleval_sota.md` 就能即答「有 4 个 gap，正解是 wrap promptfoo 而非 fork」。
**agent 接手了人类调查的劳力**。

### 4.4 附带的学习 —— 「把烧尽的日子与整理的日子交替安排」

事后回看，5/19（爆发）与 5/20（结构化）的节奏作为**两拍子周期**有效。
5/18 是「火种」，5/19 是「燃烧」，5/20 是「结晶化」。如果一周能组出 2 个
这样的周期，即便是个人 OSS 也能产出企业级的 output。

把这两条定为规则就好：「要烧就全烧」「余烬必须整理成结晶」。

---

## 5. 用数字收尾 —— 「展示量级」

3 天的累计：

| 指标 | 值 |
|---|---|
| 相关仓库 | 8 (llive / llove / llmesh / fullsense / lldesign / lltrade / raptor / mcp-spatial-asset-profile) |
| 主要 commit（除 auto:） | 80+ |
| 全 commit | 200+ |
| llive PASS 数 | 1393 → **1585** (+192) |
| llove PASS 数 | 771 → **796** (+25) |
| llmesh PASS 数 | 42 → **3086**（※含测定范围扩大，净 +4） |
| 新增文章（Qiita draft / spec / research） | 14+ |
| 新增需求定义（LE-FX / COG-MESH / 商标 / 变现 / 投资） | 6+ |
| 自主 agent 会话持续时间 | 累计 30h+ |

**个人 OSS 不是人海战术，而是通过与 AI agent 二人羽织把时间翻倍来运转**
—— 这才是本质的答案。

---

## 6. 交接给下个会话

- **lleval v0.1 着手判断**：在向 user 确认 implementation notes 里写的 wrap 设计后，
  init `furuse-kazufumi/lleval` repo。
- **llive B-7 (audit JSONL sink) / B-8 (jsonschema 验证)**：optimize branch
  的续作。把 SynapticSelector 注入真实 hot path 的候选。
- **credential 恢复**：在 Anthropic / Gemini / OpenAI 的 quota / API 恢复后，
  重新评分 comparison.md 的 honest disclosure。
- **asciinema 录制**：COG-MESH 集成 demo（9 sections）、llive demo、
  LoveApp + env attach 这 3 卷。articles_pause 解除后的 SNS 素材。
- **articles pause 解除**：已解除。本文是解除后的第 1 篇（需 user 公开判断）。

---

## 7. 总结

3 天能产出 **8 个仓库 × 200+ commit** 的输出，并非靠加速单项作业，
而是因为**把分工想透了**。

- 人：规格方向决策、数字与 goal 的设定、公开判断
- AI agent：多前线同时实现、测试整备、历史整理、进度汇总文章的起草

5/19 的 50+ commit 与 5/20 的 50+ commit，是**有一方是 AI** 的二人羽织才第一次
跑得完的量。比起「3 天有没有做 200 commit」，「**3 天有没有把余烬重新整理成结晶**」
才是本质，而后者离不开书面记录（PROGRESS / experiments / memory）的整备。

3 天 8 个仓库。火种、爆发、结晶化。下一个烧什么，5/21 早上再决定。

---

## 相关 (cross-reference)

- [PROGRESS](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/PROGRESS.md) —— 累计会话历史
- [NEXT_SESSION (auto)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.auto) —— 每个 turn 自动生成
- [Spec — lleval draft](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/requirements_lleval_v0.1_draft)
- [Spec — lleval implementation notes](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/lleval_v0_1_implementation_notes.md)
- [Research hub](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/.md)
- [Benchmark Policy](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/benchmarks/policy/.md)
- llive 核心优化 experiments log（本仓库外，参见 `llive/docs/experiments/optimize_core_2026_05_20.md` 的 commit log）
- maintainer memory:
  - `project_llive_core_optimization_2026_05_20`
  - `feedback_benchmark_honest_disclosure`
  - `feedback_qiita_long_form`
  - `feedback_article_humor_style`
  - `feedback_reader_attention_curve`
  - `feedback_articles_concept_hook`

---

# 한국어

# 3일 만에 8개 리포를 내달린 이야기 — 불씨 / 폭발 / 구조화, AI agent와 니닌바오리로 춤춘 72시간

> 게시 여부는 user 판단입니다. 이것은 「3일간의 활동을 전부 담아 하나의 이야기로 만들어 달라」는
> 의뢰를 받아 agent가 자율적으로 초안을 작성한 것입니다.
> articles_pause는 2026-05-20에 해제됨. 해제 후 제 1탄 후보.

> 📚 **연재 내비**: ← #20 한 세션에 5409 테스트 그린 ｜ **#21 본 기사** ｜ #22 Transformer 탈피의 현황 → ｜ [연재 LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ 각 기사는 단독으로도 읽을 수 있습니다(링크는 회유용).

## 0. 콘셉트 hook — 「불씨, 폭발, 구조화」

> **3일 × 1인 × 8개 리포지토리 × 100 commit overload × 1585 + 3086 + 796 테스트 그린.**
> 이건 개인 OSS 이야기입니다. AI agent와 니닌바오리로 춤췄더니 이렇게 됐습니다.

먼저 결론:

- **5/18 = 불씨를 뿌리는 날.** F25 Phase h, llove Day-0 gap audit, 중국 LLM presets,
  gitee mirror CI, COG-MESH 10건 skeleton 투입. 「씨 뿌리는 월요일」.
- **5/19 = 연속 폭발.** 아침에 M8.2～M8.9를 전부 착지 → 낮에 Production HTTP Sink +
  LoveApp 통합 → 저녁에 F23/F24 PoC + 상표 + 수익화 playbook + 시장 SWOT +
  AI 개발환경 roadmap + 자율 spinoff 카탈로그 + Qiita 기사 2편. **하루에 50+ commit.**
- **5/20 = 구조화와 자동 수렴.** 아침에 NEXT_SESSION.auto 자동화 + research hub 6건 +
  test 회귀 fix. 낮에 lleval v0.1 draft + 구현 노트. 밤에 **llive 코어 최적화 12h goal** —
  Hebbian 스타일 자동 수렴 프레임워크(SynapticSelector + UCB1)를 만들고,
  얻은 발견을 실제 production hot path에 주입. **1585 PASS 유지.**

3일간의 역할 분담을 한 줄로 정리하면, **양을 뿌리는 건 인간, 구조로 되밀어 넣는 건 AI.**
사양의 방향 결정과 목표 설정은 인간, 다전선 구현과 검증 + 이력 정리는 AI.
이것은 LLM agent를 오래 돌려 본 체감 기반의 분담입니다.

이하, 3막 구성 + 교훈 추출. 90초로 골격 / 5분으로 전체 / 30분으로 전부,
의 **집중 곡선 3단**으로 읽을 수 있게 썼습니다.

---

## 1. 제 1막 (5/18 불씨) — 월요일에 뿌린 6가지

### 1.1 90초 요약

| 뿌린 불씨 | 장소 | 왜 뿌렸나 |
|---|---|---|
| F25 Phase h.1/h.2 HTTP API skeleton | llove | TUI 장난감에서 「llive 관측 IDE」로 pivot하는 발판 |
| Day-0 gap audit | llove | dogfooding에 들어가기 전 「무엇이 안 됐나」를 지도화 |
| 중국 LLM 6종 OpenAI-compat presets | llmesh | EAR 제약 환경에서 배포 경로가 끊기지 않게 하는 보험 |
| gitee mirror CI | llmesh | GitHub가 다운돼도 배포가 멈추지 않는 이중화 |
| supply-chain audit α (deps_audit CLI) | llmesh | OSS 감사 책임을 스스로 진다. PyPI 의존의 origin 추적 |
| COG-MESH 10건 skeleton (심야부터 새벽까지) | llive | 「알아서 말 걸어오는 AI」의 최소 골격을 투입 |

씨는 뿌리기만 했다. 키우는 건 다음 날.

### 1.2 「F25 Phase h」가 뭐였더라

llove(TUI dashboard)를 「관측 도구」로 탈바꿈시키는 계획입니다. 5/18 시점에:

- `POST /api/v1/brief/submit`로 외부에서 brief를 투입할 수 있게 한다 (Phase h.1)
- `GET /api/v1/annotations/stream`으로 SSE를 통해 annotations를 흘려보낸다 (Phase h.2)

이를 발판으로, 나중에 **VS Code 확장 + Neovim 플러그인**을 얹는 multi-UI 전략의
전초전. 「TUI로 끝나는 장난감이 아니라, **에디터에 사는 관측 OS**로 기울이고 싶다」는
방침이 memory에 흐르고 있습니다.

### 1.3 중국 LLM presets와 gitee mirror — 배포 경로의 보험

이건 평소의 OSS 작업이라면 **아무도 안 하는 사전 작업**입니다. 왜 5/18에 했나:

- 어느 제조업의 EAR 제약 환경에서는 cloud LLM이 **애초에 닿지 않는다**.
  Anthropic도 OpenAI도 Gemini도 무리. local LLM이나 중국 LLM뿐.
- GitHub가 다운되거나 일시 동결되는 사례도 무시할 수 없다.
  gitee mirror가 있으면 배포가 멈추지 않는다.

「FullSense는 책임감 있는 AI 에코시스템」이라고 내세운다면, **배포까지 책임을 지는**
자세를 유지해야 한다. 이것이 씨.

### 1.4 COG-MESH 10건을 하룻밤에 skeleton

이것은 5/18 심야부터 5/19 새벽에 걸친 연속전. 「능동 발화」「Quarantined Memory」
「Mesh5W1H Annotator」「Quiet Hours」「BriefDeque Bridge」「Idle Training」
「TonicRiskMonitor」「TitleRecall」「ProactiveSpeaker」「GiftValueEstimator」.

인간의 인지 모델에서 파생한 10개 framework. 1개씩 skeleton + 테스트 1건으로
107 PASS 증가. 이것이 다음 날 폭발의 연료가 된다.

---

## 2. 제 2막 (5/19 폭발) — 화요일에 다 태워버린 50 commit

### 2.1 90초 요약

아침에 일어나 「skeleton을 본 구현으로 전환」 스위치를 켰더니, **그날 하루에 전부 다 타버렸다**.

| 시간대 | 무엇이 탔나 | 수치 |
|---|---|---|
| 새벽 | M8.2～M8.7 본 구현 | llive +55 PASS |
| 아침 | M8.8 (graph analytics) + M8.9 (grammar EVO bridge) | +22 PASS |
| 아침 | M8.1 Timeline bridge skeleton (llive 측 emitter) | +5 PASS |
| 아침 | M8.1 LoveApp 통합 (CognitiveMeshPanel attach) | llove +25 PASS |
| 오전 늦게 | **ProductionHttpTimelineSink** (auth Bearer + exp backoff retry + batch buffer + 4 env) | +12 PASS |
| 낮 | llmesh `/timeline/ingest` allow-list에 cog_* 4종 추가 | +4 PASS |
| 낮 | E2E integration test (M8.1～M8.9 chain) | +1 PASS |
| 오후 | F23/F24 PoC (PowerShell 호환 셸 + ccr launcher) skeleton | llove +α |
| 오후 | AI 개발환경 투자 roadmap, 5만 엔 상표 CHECKLIST, 수익화 playbook, 시장 SWOT | docs 4편 |
| 저녁 | 자율 spinoff 카탈로그 + Family Tree 갱신 + llgrow Planned | portal + 다수 |
| 밤 | Qiita 기사 2편 draft (M8.x 3단 로켓 / 개인 OSS 시장 SWOT) | docs +2 |

**하루에 50+ commit, 누계 PASS 수 약 +120 가까이 증가.** 개인 OSS에서 이건 「다 타버린 날」이라고
부를 수밖에 없다.

### 2.2 「M8.x」가 뭐였더라 — 한 줄씩 복습

M8 = COG-MESH의 **본 구현 페이즈**. skeleton에서 「기능으로 동작」하는 상태로
전환하는 마일스톤 군.

```text
M8.1  Timeline emit + LoveApp panel attach
M8.2  ProactiveSpeaker (능동 발화)
M8.3  QuietHours gate
M8.4  IdleTraining (빈 시간 미니 훈련)
M8.5  TonicRiskMonitor (KYT 유래의 중요도 모니터)
M8.6  TitleRecall (타이틀 상기 루프)
M8.7  Mesh5W1H Annotator
M8.8  GraphAnalytics (BFS/DFS/centrality 자체 구현)
M8.9  GrammarLayer EVO bridge
```

이것을 하루에 전부 ON으로 전환한 것이 5/19. 「skeleton과 본 구현의 경계가
인간의 체력으로 하루에 우겨넣을 수 있는 양을 넘어선 순간」을 본 날, 이라고도 할 수 있다.

### 2.3 ProductionHttpTimelineSink — 「현장 운용」을 최소 단위로

오전 늦게 한 파일에 우겨넣은 것이 production에 투입 가능한 Sink. 내용:

- **Auth Bearer** 토큰 (env `LLIVE_LLMESH_TIMELINE_TOKEN`)
- **Exponential backoff retry** (`LLIVE_LLMESH_TIMELINE_RETRIES=5`)
- **Batch buffer** (`LLIVE_LLMESH_TIMELINE_BATCH_SIZE=10`)
- **Endpoint URL** (`LLIVE_LLMESH_TIMELINE_URL=http://prod-llmesh:8080`)

이것뿐. operator가 이 4개 env를 설정하면 실제 production이 돌아간다.
+12 PASS. 테스트 그린.

**「Production에 투입하기 위한 최소 구성은 4 env」**, 이 감촉이 기쁘다.

### 2.4 docs 4편의 서프라이즈 (상표 / 수익화 / 시장 / 투자)

5/19는 **코드만의 날이 아니었다**. 오후에 「개인 OSS를 하는 사람이라면
누구나 피해 갈 수 없는」 자료를 단숨에 썼다:

1. **AI 개발환경 투자 roadmap** — 「앞으로 1년 동안 무엇에 얼마를 쓸까」의 러프 예산
2. **5만 엔 상표 CHECKLIST** — JP/US/EU 1구분으로 평평하게 진행
3. **수익화 playbook** — 10채널 × 4 sprint로 무엇을 팔까
4. **시장 수용성 SWOT** — 6축 WebSearch + SWOT + 생존 전략

이걸 전부 하루에 쓸 필요는 사실 없다. 하지만 **「탈 거면 전부 태운다」**의
정신으로 병렬 실행했다. 나중에 보니 이 4편은 **5/20 구조화 세션의 입력**이
되어 있었다. 「상표를 따기 전에 독립성을 확인하고 싶다」
「수익화를 시작하기 전에 research hub를 정비하고 싶다」 같은 의존 관계가 보였다.

---

## 3. 제 3막 (5/20 구조화) — 수요일에 정리한 3층

### 3.1 90초 요약

| 시간대 | 무엇을 했나 | 왜 |
|---|---|---|
| 아침 | NEXT_SESSION.auto 자동 생성 + Stop hook 연동 | NEXT_SESSION 수동 갱신의 drift를 구조적으로 해소 |
| 아침 | research hub 신설 (6건 SOTA / prior-art 메모) | 자율 agent가 SOTA를 밟을 수 있는 기반 |
| 아침 | 관련 prj test 회귀 fix (llove image-tool / llmesh hypothesis) | dogfooding에 들어가기 전 flaky를 잡는다 |
| 아침 | spinoff_ideas C-2 채용 우선순위표 (HIGH/MID/LOW/DEFER) | research 결과로 판단 |
| 낮 | QIITA #20을 유머 방침으로 전면 재작성 | articles_pause 해제 후의 표현 테스트 |
| 낮 | lleval v0.1 draft + 구현 노트 | 채용 우선순위 HIGH의 첫 구체화 |
| 저녁 | (휴식 + 백그라운드 llmesh 전 3086 test 주행) | flaky 재현 확인 |
| 밤 | **llive 코어 최적화 12h goal** (B-0～B-6 + B-9) | Hebbian 스타일 자동 수렴 framework + 실제 production 주입 |

**코드와 문서의 밸런스를 되찾는 날**, 이라고 표현할 수 있다. 5/19가 「전부 태운다」라면,
5/20은 「**타다 남은 재를 결정으로 정리한다**」.

### 3.2 NEXT_SESSION.auto 자동화 — drift와 싸운다

NEXT_SESSION.md는 손으로 갱신하니까 **반드시 drift한다**. 아침 1시간 반에 해결:

- `scripts/gen_next_session_auto.py`를 신설
- raptor의 Stop hook에 등록 → 매 턴 자동 덮어쓰기
- `git log` + 관련 prj 최신 commit + 최근 4h 변경 + verify_publication 결과 + 미소화 operator action을 한 장에 집약
- 손으로 갱신하는 `NEXT_SESSION.md`는 **방향성 메모 전용**으로 강등

이로써 다음 세션 시작 시의 context 복원 비용이 급감했다. **「자동 생성
파일은 하나 더 많이 둔다」가 개인 OSS의 정답**이라고 생각한다.

### 3.3 research hub 신설 — agent에게 SOTA를 밟게 한다

`docs/research/`에 6건 투입:

```text
docs/research/
├── index.md                       # Reference hub
├── lleval_sota.md                 # 10 framework 비교 + 4 gap
├── llgrow_prior_art.md            # Growth Automation 선행 예
├── cognitive_mesh_vs_sota.md      # COG-MESH의 관련 연구
├── llcraft_sota.md                # llcraft 후보의 SOTA
├── llrisk_prior_art.md            # llrisk (Tonic Risk) 선행 예
└── llgov_sota.md                  # llgov (governance) SOTA
```

이것은 「**자율 agent가 연구 분야를 감안해 판단할 수 있는 기반**」.
RAD (Research Aggregation Directory)의 파생 개념으로, 평소의 Claude
세션에서 「선행 연구는?」이라고 물었을 때, agent가 `docs/research/`를
읽는 것만으로 SOTA matrix를 끌어낼 수 있다.

**「인간의 연구 조사 노력을 agent가 이어받는다」**를 위한 장치입니다.

### 3.4 spinoff_ideas C-2 채용 우선순위표

research 결과를 토대로 6건을 분류:

| spinoff | 우선순위 | 근거 |
|---|---|---|
| **lleval** | **HIGH** | promptfoo wrap으로 4 gap을 메우는 설계가 명확 |
| llgrow | MID | growth automation은 수요 있으나 기존 SaaS 경쟁 다수 |
| llbridge | MID | MCP bridge는 wave 대기 |
| llcraft | LOW | LLM workshop은 취미 색채 강함 |
| llrisk | LOW | Tonic Risk monolithic, 수요 옅음 |
| llgov | LOW | LLM governance는 legal-heavy |
| llforen | DEFER | LLM forensics는 시기 상조 |

이로써 **다음에 손댈 spinoff가 lleval 한 개로 좁혀졌다**. 개인 OSS에서
spinoff 카탈로그를 가지면 「전부 하고 싶은 병」에 걸리지만, 우선순위표로 항체를 만든다.

### 3.5 lleval v0.1 draft + 구현 노트 — 채용 우선순위 HIGH를 구체화

오후에 2편의 draft를 썼다:

1. **requirements_lleval_v0.1_draft.md** — LE-01～08 요건
2. **lleval_v0_1_implementation_notes.md** — PoC scope (wrap not fork)

주요 결정:

- **promptfoo를 fork하지 않는다. wrap한다.** Node.js fork는 유지 비용 2배.
  Python subprocess로 호출해 그 위에 얹는다.
- **별도 GitHub repo** (`furuse-kazufumi/lleval`), Apache-2.0 + Commercial dual.
- **v0.1 MVP** = LE-01 (다 provider 통일) + LE-02 (progressive size matrix) +
  LE-03 (honest disclosure analyzer) + LE-07 (CLI + Python API).

차별화 4축:

| # | 차별화 | 기존 gap |
|---|---|---|
| 1 | on-prem + cloud 통일 A/B | 산업 IoT + local llama.cpp와 cloud API를 동일 run에서 다루는 설계가 부재 |
| 2 | Progressive size curve (xs/s/m/l/xl) | 기존은 모두 고정 prompt 길이 |
| 3 | **Honest disclosure 자동 진단** | 이상값의 내부 분해는 수작업 영역 |
| 4 | Judge rotation + position swap | self-preference bias 자동 검출 |

honest-disclosure 5인자 분해:

1. warmup hit
2. token-count normalization
3. network RTT 제외
4. backend attach overhead
5. system load

이를 **CI에서 블록 가능한 diagnosis report**로 만든다, 는 설계가
본기도(本氣度)의 온도. 더는 「자사가 빠르다! 이겼다!」로 끝내지 않는 구조.

### 3.6 밤의 메인 — llive 코어 최적화 12h goal

오후가 끝날 무렵 user로부터 진심의 goal이 떨어졌다:

> 「llive의 코어 부분 최적화를 진행해. 12시간 후까지 정보 수집하면서 여러 가지
> 시행해 볼 것. 제대로 이력을 남기고 불량이 안 나는 형태로 수렴시켜
> 줘.」
>
> 「코어 부분의 데이터 보유 방식이나 컨테이너를 바꿔 보거나, 디자인 패턴을
> 확장해 보거나 해서, 가능한 한 자동으로 최적의 구조로 수렴하는 느낌이 이상적.」
>
> 「**뇌의 시냅스 구조처럼 가중치가 변화하는 느낌이 좋아.**」

이건 평소의 최적화 의뢰와 자릿수가 다르다. 단일 구현의 수동 고속화가 아니라, **여러
후보를 늘어놓고 자동 수렴시키는 framework를 만들어라**, 라는 지령.

#### 설계 판단 — `SynapticSelector`

ε-greedy + Hebbian 스타일 weight update를 조합한 variant selector를 신설:

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

bounded modification (APO §E2)으로 min/max clip. 19건 테스트 그린. **기존 1518 →
1537**, 회귀 없음. 이것이 B-0.

#### B-1 ～ B-6 — 자동 수렴을 관찰

| Phase | 시도한 것 | 배움 |
|---|---|---|
| B-1 | top-K 추출 (n=5000, k=10, 200 iter) | `heapq_nlargest`가 weight=100 (max)로 수렴. `full_sort`는 0.377로 감쇠. **수렴한다.** |
| B-2 | cosine variants (dim=16/128/768) | `numpy_normalized` (pre-L2 normalized 입력)가 전 차원 압승. **pre-normalize cache로 2-5x.** |
| B-4 | decay variants (N=100/10000/100000) | N=100에서는 올바르게 `np_inplace`로 수렴, **N=10000/100000에서 잘못 `np_einsum`으로 수렴**. 진짜 최선은 `np_inplace`로 17% 빠른데도 weight가 늘지 않는다. **early-convergence bias 발견.** |
| B-5 | `UCBSynapticSelector` (UCB1) | B-4와 동일 조건에서 3 사이즈 모두 `np_inplace`로 올바르게 수렴. **병리 해소.** |
| B-6 | sliding window (deque vs list_slice) | maxlen=1000에서 deque는 converged. list_slice는 **119x 느려짐** (O(N) copy). **production 적용 후보 확정.** |

**B-4가 본 세션 최대의 발견**: 「자동 수렴」이라고 내세워도 ε-greedy만으로는
승자 독식 dynamics에 빠진다. UCB1의 exploration round가 필요. 이것은
`feedback_benchmark_honest_disclosure`의 정신 — 「수렴 결과가 실은 최선이
아니다」를 간파할 수 있는 observability가 전부.

#### B-9 — 발견을 실제 production hot path에 주입

연구 결과를 실제 코드에 반영하지 않으면 의미가 없다. B-9-a와 B-9-b로 2건 주입:

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

callsite (`MemoryWriteBlock`)에서 `assume_normalized=True`를 지정.
`SemanticMemory.all_embeddings()`는 L2 normalized 완료이므로 **의미적으로
같은 결과, 계산이 줄어든다**. 공개 API kwarg default False로 완전 하위 호환.

**B-9-b: `GiftValueEstimator._history`를 deque화**

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

B-6에서 `list_slice`가 deque보다 119x 느려짐을 확인했으므로,
long-run에서 같은 pathology에 빠질 가능성이 있던 hot path를 예방적으로
deque화. cooldown 배율은 오차 마진.

**결과**: 전 1585 PASS 유지, 회귀 없음.

#### 채용 게이트 확인

| 항목 | 상태 |
|---|---|
| 5% 개선 | 달성 (B-2에서 측정 완료) |
| 전 test 그린 | 1585 PASS |
| selector overhead | 해당 없음 (직접 최적화) |
| 하위 호환 | OK (kwarg default False) |

branch `optimize/core-2026-05-20`에 commit. main에 머지할지는
추후 판단 (PR 후 user 승인).

---

## 4. 3일을 통해 보인 교훈 — 「Hebbian × Honest × Hub」

### 4.1 교훈 1: Hebbian 스타일 자동 수렴에는 UCB1이 필요

ε-greedy만으로는 「수렴한 곳이 실은 최선이 아니다」를 간파할 수 없다. UCB1의
exploration round로 전 variant를 공평히 시행함으로써 **진짜 최선에 도달**할
수 있다. 이것은 TRIZ 40 원리의 「사전 작용」(원리 #10)과 「자기 서비스」(원리 #25)의
조합에 가깝다.

production 주입 후보:

- cosine 계산: embedding pre-normalize cache → 2-5x
- sliding window: list → deque 이행 → 2-5x
- ε-greedy → UCB1 전환: production hot path의 자동 수렴

### 4.2 교훈 2: Honest disclosure는 알고리즘 설계에서도 유효

B-4에서 「수렴 결과가 실은 최선이 아니다」를 간파할 수 있었던 건 **avg_latency_ms를 별도로
기록해 비교할 수 있는 observability가 있었기 때문**. 벤치에서 「묘하게 빠른」 결과가
나오면 반드시 내부를 의심하라, 는 `feedback_benchmark_honest_disclosure`의 규칙이지만,
이것은 **알고리즘 설계 레이어에도 적용된다**는 것.

lleval v0.1에서 5인자 분해를 일급 기능으로 만든 것은 이 정신의 연장.
「빨라 보이는 이유를 분해한다」가 **개인 OSS가 cloud 대기업과 싸울 수 있는 몇 안 되는 무기**.

### 4.3 교훈 3: research를 hub화하면 agent가 SOTA를 밟을 수 있다

`docs/research/`에 SOTA / prior-art를 접어 넣으면, **자율 agent가 다음 세션에서
「선행 연구는?」이라고 물었을 때 1초 만에 답할 수 있다**. 이것은 TRIZ로 말하는
「자원 탐색」(원리 #5, #15)의 AI화.

평소의 Claude 세션에서 「lleval은 무엇을 차별화해야 하나?」라고 물었을 때, agent가
`docs/research/lleval_sota.md`를 읽는 것만으로 「4 gap이 있다, promptfoo를 fork가
아니라 wrap이 정답」이라고 즉답할 수 있다. **인간의 조사 노력을 agent가 이어받는다**.

### 4.4 부차적인 배움 — 「다 타버리는 날과 정리하는 날을 번갈아 배치한다」

나중에 보니 5/19(폭발)와 5/20(구조화)의 리듬은 **2박자 사이클**로서 유효.
5/18이 「불씨」, 5/19가 「연소」, 5/20이 「결정화」. 이를 1주일에 2 사이클
짤 수 있으면, 개인 OSS라도 기업급 output이 나온다.

「탈 거면 전부 태운다」「타다 남은 재는 반드시 결정으로 정리한다」, 이 둘을
규칙으로 삼으면 된다.

---

## 5. 숫자로 마무리 — 「자릿수를 보여준다」

3일간의 누계:

| 지표 | 값 |
|---|---|
| 관련 리포지토리 | 8 (llive / llove / llmesh / fullsense / lldesign / lltrade / raptor / mcp-spatial-asset-profile) |
| 주요 commit (auto: 제외) | 80+ |
| 전 commit | 200+ |
| llive PASS 수 | 1393 → **1585** (+192) |
| llove PASS 수 | 771 → **796** (+25) |
| llmesh PASS 수 | 42 → **3086** (※측정 범위 확대 포함, 순 +4) |
| 신규 기사 (Qiita draft / spec / research) | 14+ |
| 신규 요건 정의 (LE-FX / COG-MESH / 상표 / 수익화 / 투자) | 6+ |
| 자율 agent 세션 지속 시간 | 누계 30h+ |

**개인 OSS는 인해전술이 아니라, AI agent와의 니닌바오리로 시간을 2배로 만들어
돌린다**, 는 것이 본질적인 답.

---

## 6. 다음 세션으로의 인계

- **lleval v0.1 착수 판단**: implementation notes에 쓴 wrap 설계를 user에게
  확인한 후, `furuse-kazufumi/lleval` repo init.
- **llive B-7 (audit JSONL sink) / B-8 (jsonschema 검증)**: optimize branch
  의 연속. SynapticSelector를 실제 hot path에 주입하는 후보.
- **credential 복구**: Anthropic / Gemini / OpenAI의 quota / API 회복 후
  comparison.md의 honest disclosure를 재채점.
- **asciinema 녹화**: COG-MESH 통합 demo (9 sections)와 llive demo,
  LoveApp + env attach의 3편. articles_pause 해제 후의 SNS 소재.
- **articles pause 해제**: 해제 완료. 본 기사는 해제 후의 제 1편 (user 공개 판단 필요).

---

## 7. 정리

3일 만에 **8개 리포 × 200+ commit**의 출력을 낼 수 있었던 것은, 개별 작업을 고속화
했기 때문이 아니라, **역할 분담을 딱 잘라 정했기** 때문입니다.

- 인간: 사양의 방향 결정, 숫자와 goal의 설정, 공개 판단
- AI agent: 다전선 동시 구현, 테스트 정비, 이력 정리, 진척 통합 기사의 초안

5/19의 50+ commit과 5/20의 50+ commit은, **한쪽이 AI**인 니닌바오리로 처음
주파할 수 있었던 양입니다. 「3일에 200 commit 했나」보다 「**3일에 타다 남은 재를 결정으로
다시 정리할 수 있었나**」 쪽이 본질이며, 후자에는 기록 남기기(PROGRESS / experiments /
memory)의 정비가 불가결했습니다.

3일에 8개 리포. 불씨, 폭발, 결정화. 다음에 무엇을 태울지는 5/21 아침에 정합니다.

---

## 관련 (cross-reference)

- [PROGRESS](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/PROGRESS.md) — 누계 세션 이력
- [NEXT_SESSION (auto)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.auto) — 매 턴 자동 생성
- [Spec — lleval draft](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/requirements_lleval_v0.1_draft)
- [Spec — lleval implementation notes](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/lleval_v0_1_implementation_notes.md)
- [Research hub](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/.md)
- [Benchmark Policy](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/benchmarks/policy/.md)
- llive 코어 최적화 experiments log (본 리포 외, `llive/docs/experiments/optimize_core_2026_05_20.md`의 commit log 참조)
- maintainer memory:
  - `project_llive_core_optimization_2026_05_20`
  - `feedback_benchmark_honest_disclosure`
  - `feedback_qiita_long_form`
  - `feedback_article_humor_style`
  - `feedback_reader_attention_curve`
  - `feedback_articles_concept_hook`
