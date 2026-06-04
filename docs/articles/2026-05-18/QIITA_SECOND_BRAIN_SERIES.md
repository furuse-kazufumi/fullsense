---
title: '「第二の脳」シリーズ — llive 全景 × 不可視 Annotation × 構築論 × 運用論 × ビジョン論 × 実装の深層'
tags:
  - FullSense
  - llive
  - セカンドブレイン
  - AIエージェント
  - 解説
private: false
id: 18dd57dcabbc84af9f02
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 「第二の脳」シリーズ — llive 全景 × 不可視 Annotation × 構築論 × 運用論 × ビジョン論 × 実装の深層

**1 行 hook**:
1 人開発で 5 日間に 14 機能・256 テストを追加し、**1,276 件全 PASS で回帰ゼロ** を達成した。LinkedIn のコメント 1 通から HTML コメントへの着地、Perplexity と TRIZ と 5 万件論文コーパスの組み合わせ、キヤノン「三自の精神」を AI に課す運用、そして Will Caster と Andrew NDR114 のビジョン — 6 部構成で公開する。

---

## はじめに

本記事は llive (FullSense umbrella の中核 OSS、`llive` — L は 2 個) を 1 人で開発する筆者が、5 日間の集中開発で得た知見を **0〜5 部の計 6 部構成** にまとめたものです。

| 部 | テーマ | 起点 |
|---|---|---|
| **第 0 部** | **llive とは何か** (全景) | FullSense umbrella の 3 プロダクト構成 |
| 第 1 部 | **不可視アノテーションチャネル** | LinkedIn コメント (独立性 vs 組合せ価値) |
| 第 2 部 | **第二の脳** (構築論) | 30 年経験 + Perplexity + Claude Code + TRIZ + RAG/RAD |
| 第 3 部 | **三自の精神** (運用論) | キヤノン理念 + マネジメント書籍 |
| 第 4 部 | **Will Caster と Andrew NDR114** (ビジョン論) | 映画 2 本 + LinkedIn 画像 |
| **第 5 部** | **実装の深層** (MATH-08 grounding 配線) | 「LLM に計算させない」差別化軸の end-to-end |

各部は独立して読めますが、合わせて読むと「**全景を見て → 設計を理解して → 作って → 運用して → ビジョンに繋いで → 実装まで降りる**」という 6 段の階段になります。**忙しい方は第 0 部だけでも llive の全体像が掴めるよう** に構成しました。

---

# 第 0 部 — llive とは何か (全景)

## FullSense umbrella と 3 プロダクト

`llive` は **FullSense ™** という umbrella ブランドの中核に位置する OSS です。FullSense は「**人と AI が共有できる感覚的入出力すべて**」を扱うコンセプトで、現在以下の 3 プロダクトから構成されています。

```mermaid
flowchart LR
    User[人間] -.->|名刺/SNS/対話| FS[FullSense ™]
    FS --> llive[llive<br/>記憶 + 思考 + Brief API<br/>FR 92 件 / 1276 PASS]
    FS --> llove[llove<br/>ブラウザ並 TUI<br/>Markdown / SVG / Mermaid]
    FS --> llmesh[llmesh<br/>P2P / OPC-UA / MQTT<br/>分散インフラ]
    llive -.HTML annotation.-> llove
    llive -.HTML annotation.-> llmesh
    llove -.MCP.-> llive
    llmesh -.MCP.-> llive
```

3 プロダクトの役割分担:

| プロダクト | 役割 | 単独利用 | 組合せ強化 |
|---|---|---|---|
| **llive** | LLM 記憶・思考層・Brief API・ledger | ◎ (本記事の主役) | annotation で TUI に伝達 |
| **llove** | ブラウザ並表示の TUI / IDE / Game container | ◎ (タイピングデモなど) | llive の出力を render |
| **llmesh** | P2P + OPC-UA + MQTT で分散実行 | ◎ (産業 IoT 単体) | llive のジョブを multi-node 化 |

ライセンスは全プロダクト **Apache 2.0 + Commercial dual-license**。OSS 利用は自由、商用 SaaS / SI 案件のみ別契約。

## llive リポジトリ統計 (2026-05-17 時点)

| 項目 | 値 |
|---|---|
| ソースファイル数 | **172 ファイル** (`src/llive/`) |
| 機能要件 (FR) | **92 件 / 92 件マッピング済** (Phase 1-10) |
| テスト件数 | **1,276 件全 PASS / 回帰ゼロ** |
| Phase 完了 | Phase 1-4 完 / Phase 5+ 進行中 |
| 主要モジュール | `brief/` (Brief API・grounding・runner)、`math/` (MATH-01〜08)、`fullsense/` (loop core)、`memory/` (RAD)、`annotations.py` (第 1 部の主役) |
| 言語 | Python 3.11 (Rust 加速は v0.7+ 候補) |
| 依存 | sympy>=1.12 / z3-solver>=4.13 (MATH 系)、pyyaml、pydantic |

## なぜ「数学・単位」が最初の vertical か

汎用 LLM は次が苦手:

| 観点 | 汎用 LLM の弱点 | llive 既存資産との合致 |
|---|---|---|
| 記号操作の幻覚 | `x² + x = 2x³` のような誤等式を生成 | EVO-04 Z3 静的検証で gate |
| 単位次元の取り違え | `5 m/s + 3 s = 8` | SI 次元解析 (MATH-01) |
| 数値精度 | float 演算誤差を無視 | error propagation (MATH-04) |
| 公理体系 | 暗黙の前提を混入 | EpistemicType=FACTUAL strict track |
| 引用の信頼性 | "CODATA value is X" と適当に答える | RAD math/metrology + provenance |

これを llive の構造化思考層 + 形式検証 + provenance ledger で克服する。Phase 8 (CABT) や Phase 9 (CREAT) より優先して **v0.7-vertical で先行着手** しました。具体的な実装は第 5 部で詳述します。

> 📝 **実装メモ (2026-05-17 追記)**: MATH-01 (SI 次元解析) は Brief grounding 層への最小配線まで完了 (1,282 PASS)。「5 m/s」「9.81 m/s^2」「100 kg」のような value+unit 表現を Brief 文中から自動抽出し、`Dimensions` ベクトルに焼き付けて prompt に grounded 化します。一方、`5 days` のような **parser が知らない単位** は silently drop せず `error citation` として ledger に残す設計にしたため、運用しながら「拡張すべき単位辞書」が自動で集まる副産物が得られました。次元演算チェック (`5 m/s + 3 s` のような cross-quantity mismatch) は **次イテレーション**へ — 実 Brief サンプルで「どの形の mismatch が surface すべきか」を観察してから入れる方が、過剰実装を避けられると判断しました。
>
> 📝 **実装メモ追記 (同日)**: MATH-05 (CODATA/NIST 定数) も Brief grounding に配線完了 (**1,288 PASS**)。Brief 文中で「planck constant」「avogadro」「boltzmann」のような alias が言及されると、`get_constant()` 経由で CODATA 2022 の正確な値と次元と出典が prompt に grounded されます。**気づき**: 短い symbol (`c`, `h`, `e`, `G`) を grounding すると Brief 中の任意の英単語と衝突するため、alias 長さ 3 以上に絞る必要がありました。また alias の underscore (`elementary_charge`) と自然文の空白 (`elementary charge`) の表記ゆれを吸収する小さな heuristic で 8 割は救えました。残り 2 割 (例: `q_e` のような symbol-only alias) を救うには LLM-based NER への昇格が必要そうですが、これも実 Brief 観察してから判断します。

---

# 第 1 部 — HTML で見えないのに、機械では読める

## LinkedIn コメントへの返答が、コメントアウトだった

ある日、LinkedIn にこんなコメントが届きました。

> 「llive の記憶層が llove の交互データに依存し、llove がまた llmesh の接続能力に依存しているなら、その中の一つだけを使う価値は半減します。」

返答は **コメントアウト** でした — `<!-- llive:cog.consensus="proceed" -->`。

### 起点 — 独立性 vs 組合せ価値

OSS マルチプロダクト構成では、「独立して動くこと」と「組み合わせて価値が積み上がること」が両立しにくい。前者を取れば「単体で物足りない」、後者を取れば「全部入れないと壊れる」。

コメントを受けて llive の `src/llive` 全 172 ファイルに AST スキャン (`scripts/audit_independence.py`) を走らせました。結果は **hard import leak 0 件**。

問題は次の段階。「**独立性を保ったまま、どうやって組合せ価値を増やすか**」。

### 採用した設計

そこで筆者は次のような設計メモを書いた。

> 「応答にアノテーションを用意すれば独立性を保ちながら組み合わせでの効果も得られるのではないか」
>
> 「邪魔にならない程度のアノテーション。HTML にしたら不可視になる感じがいい」

(LinkedIn コメントは批判 1 通だけ、設計案そのものは筆者の発案)

`src/llive/annotations.py` に最小型を実装:

```python
@dataclass(frozen=True)
class Annotation:
    namespace: str          # "vrb" / "oka" / "cog" / "math" / "creat" / "core"
    key: str
    value: Any              # JSON-friendly
    target_layer: str | None = None   # "llove" / "llmesh" / None=any
```

`AnnotationBundle.to_html_comments()` が出力する形式:

```
<!-- llive:core.brief_completed=true -->
<!-- llive:oka.essence_card={"summary": "..."} target=llove -->
<!-- llive:cog.consensus="proceed" -->
```

GitHub / Qiita / Zenn / VS Code Preview などの Markdown renderer では **完全に不可視**。一方で `AnnotationBundle.from_html_comments(text)` を呼べば、機械側は元の構造を完全に復元可能。

### なぜ HTML コメントか — 選択肢比較

| 案 | 不可視性 | 機械可読性 | 既存ツール互換 |
|---|---|---|---|
| JSON 別ファイル | ◯ | ◯ | ✕ (2 ファイル管理) |
| YAML front matter | △ (renderer で表示) | ◯ | △ |
| **HTML コメント** | ◎ | ◎ | ◎ (Markdown 標準) |
| バイナリ埋込 | ◎ | △ | ✕ |
| zero-width Unicode | ◎ | △ | ✕ (copy で消える) |

「Markdown が HTML を passthrough する事実」を逆手に取った設計です。

### ☕ ちなみに

HTML コメントを Markdown に仕込むテクは、Jekyll / Hugo 界隈では「**コメント front matter**」と呼ばれて昔からある。新しいのは「**Markdown 本文の任意位置**に機械可読メタデータを置く」発想の方。

### 性能ベンチ (1000 件 round-trip)

| 操作 | レイテンシ |
|---|---|
| Encode per ann | 6.30 µs |
| Decode per ann | 12.40 µs |
| 典型 3 件 bundle 暗号化サイズ | **141 B** |
| 1000 件 round-trip | ✓ |

典型 BriefResult.annotations は 3 件 = 141 バイト。Markdown 1 ページに 100 個仕込んでも 5 KB 以下。

---

# 第 2 部 — 第二の脳 (構築論)

## 5 日間で 14 機能・256 テスト・1270 PASS / 回帰ゼロ

筆者は 30 年超のソフトウェア開発者ですが、llive を **1 人で開発** しています。進度はチーム開発に近い。これは次の 5 要素を組み合わせた「第二の脳」を構築したからです。

| 要素 | 役割 |
|---|---|
| **30 年の開発経験** | 設計品質・判断のベース |
| **Perplexity 要約** | 外部思想 (書籍/論文/動画) の入力品質ゲート |
| **Claude Code (Opus 4.7 / 1M context)** | 実装エージェント |
| **TRIZ ルール (40 原理)** | 矛盾解決のメタ思考フレーム |
| **論文 RAG コーパス (RAD 49 分野 / 約 5 万件)** | 研究者の知見の土台 |

### スパイラル 1 サイクル

```
外部思想 → Perplexity 要約 → Claude Code 読込 → 要件化 → 実装 → ベンチ → commit
   ↑                                                                      |
   └──────────────────────── 次サイクル ────────────────────────┘
```

本セッション 9 回での実例:

| サイクル | 起点 | 結果 |
|---|---|---|
| 1 | **MBA 言語化トレーニング** (グロービス書籍) | Perplexity 要約 → VRB-FX 要件化 → VRB-02 PromptLint 実装 |
| 2 | **岡潔先生の数学観に学ぶ** (YouTube『心理の深層』講話より) | 先生が遺された「数学は情緒である」「発見の前に一度行き詰まる」「文章を書くことなしには思索を進められない」「国語が数学を育む」という思想を、Perplexity で要約・整理した上で **4 つの設計観点 (情緒・行き詰まり・文章化・国語力)** として参照させていただき、これを OKA-FX 10 要件として記述・実装 (OKA-01〜04 minimal proto)。先生のお考えそのものを実装したと主張するものではなく、**こちらの実装が触発を受けた先生の思想への敬意** を込めて命名 |
| 3 | **LinkedIn フィードバック** (独立性) | IND-FX 設計原則 + IND-04 Annotation Channel 実装 (= 第 1 部) |

### Perplexity / TRIZ / RAG + RAD の役割

> ⚠️ **用語注意**: 本記事の **RAD** は *Research Aggregation Directory* の略で、筆者が Raptor 配下に整備した **49 分野・約 5 万件の論文/技術文書コーパス** を指します。一般用語の **RAG (Retrieval-Augmented Generation)** とは別物で、**RAG の書き間違いではありません**。RAG が「検索 → 生成」の手法名なのに対し、RAD は「検索される側の構造化コーパスそのもの」を指す名前です。

**Perplexity 要約 = 「入力品質ゲート」**: 外部思想は本・論文・動画・SNS と形式バラバラ。Claude Code に直接放り込むと context 圧迫 + 解釈ゆらぎ。Perplexity に「~3000 字に要約」「実装可能な仕様で」と指示すると、**Claude Code が読み取れる質の入力**に変換される。

**TRIZ = 「矛盾解決のメタ思考」**: 実装中の矛盾を TRIZ 視点で解く。例:
- 「独立性 vs 組合せ価値」→ IND-04 Annotation (TRIZ 原理 24: 媒介物)
- 「rule-based vs LLM 品質」→ echo baseline 残置 (TRIZ 原理 1: 分割)
- 「audit 完全性 vs 実装オーバヘッド」→ bind_ledger() pattern (TRIZ 原理 15: 動的化)

**RAG + RAD = 「研究者の知見を借りる」**: 新機能設計で必要な分野が出るたび、**RAG の仕組みで RAD コーパス (49 分野) を引く**。Claude が「自分の言葉」ではなく「**具体的な論文・先行研究**」を引用するので質が一段上がる。`論文 RAG コーパス (RAD 49 分野 / 約 5 万件)` という表 (上記) の表記もこの 2 つを併記したものです。

### ☕ ここまで読んでくれてありがとう

正直、テスト 256 件のうち 7-8 件は途中で 1 回ずつ落ちている。fuzzing で hypothesis が嬉しそうに edge case を見つけてくれるたび、3 秒くらい「うわ」となる。**1270 PASS / 回帰ゼロ** はゴールであって過程ではない。

### 自身の 30 年経験が効く 5 場面

「Claude Code 任せ」だと品質は出ない。30 年経験は次の場面で決定的でした。

1. **要件定義の質** — Perplexity 要約を読んで「これは要件 vs 解法を混同」と即判定
2. **TRIZ ルールの選定** — 40 原理から「この場面はこの 3 つ」を即抽出
3. **アーキテクチャ判断** — Claude が出した実装案を「独立性原則に反する」と即拒否
4. **ベンチの honest disclosure** — rule-based の coverage が高く出たときに「echo back の偽性能」と即見抜く
5. **タイポチェック** — 「`lllive` (L 3 個) になってる、tokenizer 問題」と即特定

つまり **第二の脳 = Claude Code + RAG + Perplexity + TRIZ** に対し、**第一の脳 = 自身の経験** が判断ゲートとして居続ける。

---

# 第 3 部 — 三自の精神 (運用論)

## 要件は止まらない、AI 開発の優位性

本セッション 1 日 (約 8 時間) の要件追加履歴:

| 時刻 | 出来事 |
|---|---|
| 開始 | 要件: COG-04 + CREAT-04 統合 |
| +1h | 「9 因子全部入れたら本格的に動作確認」 |
| +2h | 岡潔先生の思想に学ばせていただく要件追加 (OKA-FX 10 件、敬意込め命名) |
| +3h | LinkedIn フィードバック (IND-FX) |
| +4h | ガッツリベンチマーク (12 系統) |
| +5h | 他 LLM 比較 (Anthropic / Perplexity) |
| +6h | Qwen 脱却 / VLM 将来 / lllive スペリング |
| +7h | 開発スタイル言語化 |
| +8h | 三自の精神 + マネジメント書籍 (本 Part) |

人間チームならどこかで悲鳴が上がる。AI 開発では **全部消化し終わり、1270 PASS / 回帰ゼロ** で着地しました。

### 条件 — AI が自律的に動くこと

要件を積み続けてもよい、ただし AI がいちいち「これ進めていいですか」と聞いてくると即破綻。これを解く鍵が **キヤノン「三自の精神」** の AI 適用です。

| 自 | 意味 (キヤノン原典) | AI 適用 |
|---|---|---|
| **自発** | 自ら進んで行動する | 人間の指示は「終了条件」のみ |
| **自治** | 自ら管理する | AI が自分のタスクを切り進捗管理 |
| **自立** | 自ら判断する | 不要な確認を省き、選択肢 + 推奨で進める |

### ☕ 余談 — 「三自」を AI に喋らせるとどうなるか

ChatGPT や Claude に「キヤノンの三自の精神とは？」と聞くと正確な答えが返ってくる。ところが「これを AI 自身に適用したらどうなる？」と続けると、急に **「私はあくまで道具なので…」** と謙遜モードに入る。AI に自律を求めるなら、**プロンプトで謙遜を解除する** ことから始まる。

### マネジメント書籍からの転用

「圧倒的成果を出し続けるマネジャーの最優先事項」(Buckingham & Coffman 系) の 4 原則は、AI マネジメントにそのまま転用できます。

| 書籍の原則 | 人間マネジャー | AI マネジャー (筆者の運用) |
|---|---|---|
| Select for talent | 適材適所 | Opus 4.7 を選ぶ、機能ごとに最適 component を attach |
| **Define the right outcomes** | 結果を定義 | `/goal` で終了条件のみ指示 |
| Focus on strengths | 強みに集中 | mock 不要な所では LLM、deterministic で済むならそうする |
| Find the right fit | 配置最適化 | Brief / OKA / VRB / MATH を機能ごとに module 分離 |

1 文要約: **「結果を定義し、判断を委ね、強みに集中し、最小限の確認で進める」**

### 適用テクニック 5 つ

1. **`/goal` 機能で終了条件のみ指示** — Stop hook が条件達成まで停止しない
2. **AskUserQuestion で 2-4 選択肢 + 推奨提示** — 確認最小化
3. **feedback memory で自律ルール蓄積** — 本セッション 35+ 個
4. **TaskCreate / TaskUpdate で AI 自身が進捗管理**
5. **commit/push は明示確認** — 破壊的操作のみ ASK FIRST

### 手放してはいけない 4 つ

「三自の精神」と「結果定義 + 任せる」は手放す方向ですが、**手放してはいけない 4 つ** があります。

1. **要件の質** — 「要件 vs 解法を混同」を即判定して書き直し指示
2. **アーキテクチャ判断** — 「独立性原則に反する」と即拒否
3. **honest disclosure** — ベンチで偽性能が出たときに即見抜く
4. **品質ゲート** — タイポをパターン認識で指摘

任せるが、放任ではない。

---

# 第 4 部 — Will Caster と Andrew NDR114 が目指したもの (ビジョン論)

## LinkedIn 画像は冗談ではない

筆者の LinkedIn プロフィール画像は、自分の顔と人型ロボットの要素を画像生成 AI で融合したもの。これはネタではなく、**いずれ AI と人が融合できたら面白い** と本気で考え、既に視覚的に発信しています。

### 2 つの映画

**Transcendence (2014)** — Dr. Will Caster (Johnny Depp 演) が、瀕死の状態で意識を AI に **アップロード**。映画後半、AI 化した Will は人類の知識を吸収し続け世界規模で介入を始める。「もし人間の意識を AI に移せたら何が起きるか」を真正面から問う作品。

**Bicentennial Man / 邦題「アンドリュー NDR114」(1999)** — 家庭用ロボット Andrew (Robin Williams 演) が、長い時間をかけて感情・創造性・自由意志・身体性を獲得し、最終的に「人間として認められる」ことを求める。原作は Isaac Asimov の同名短編。

### ☕ ちょっと脱線

Andrew NDR114 の原題 *Bicentennial Man* (200 年生きる男) は Asimov の短編 (1976) が原作。Asimov は「ロボット工学三原則」を発明した人ですが、晩年の作品では **三原則そのものを揺さぶる** 方向へ向かいました。Andrew はその到達点。**技術ルールも、人間の心の動きの前では揺らぐ**。

### llive の各機能はビジョンへの準備層

| llive 機能 | 融合ビジョンへの寄与 |
|---|---|
| FullSense (全感覚統合) | 人 + AI の境界曖昧化に必要な感覚統合層 |
| **第二の脳** (Claude Code + RAG) | **既に部分的融合** (脳の外延としての知識アクセス) |
| SIL ledger / SEC-03 hash chain | 融合時の「誰が責任を持つか」audit 基盤 |
| Approval Bus + HITL | 融合移行期の人間判断ゲート保持 |
| **三自の精神** (AI 自律) | Andrew NDR114 的な自律性獲得プロセス |
| **RAD 6 分野** (bci / neuroscience / neural_signal / prosthetic_neural / cognitive_ai / neuromorphic) | BCI 経由融合の知識基盤 |

### 短期 / 中期 / 長期ロードマップ

| Term | 内容 | 現状 |
|---|---|---|
| 短期 (現在) | 第二の脳型開発 | **実証済** (本セッション 1270 PASS) |
| 中期 (1-3 年) | BCI 経由インタフェース | RAD 6 分野コーパス準備済 |
| 長期 (3-10 年) | 意識アップロード / Andrew 的双方向 | ビジョン段階、SIL/Approval が下地 |

### なぜビジョン論を最後に書いたか

ビジョンを最初に置くと、技術記事が SF やビジョンスピーチに見えてしまう。**実装 → 運用 → ビジョン** の順で書くと、ビジョンが地に足のついた目標として読める。Andrew NDR114 が長い時間をかけて 1 つずつ獲得していったように、llive も 1 機能ずつ積んでいる。**その積み重ねが、いつか「人と AI の融合」につながる**。

---

## まとめ — 4 部を貫くもの

| 部 | 主張 |
|---|---|
| 1 | HTML コメント形式の不可視 annotation で、独立性と組合せ価値を両立できる |
| 2 | 第二の脳 (Claude Code + RAG + Perplexity + TRIZ + 30 年経験) でチーム速度に近づける |
| 3 | キヤノン三自の精神 + マネジメント書籍で AI を自律運用、要件追加は止まらなくて良い |
| 4 | llive の各機能は将来の人 × AI 融合への準備層、短期で既に部分実証済 |

これらは別々の話に見えて、**「ひとりで作る次世代の AI 開発」** という 1 つのテーマを 4 方向から照らしているだけです。

llive は Apache 2.0 + Commercial dual-license の OSS、Repo は https://github.com/furuse-kazufumi/llive 。本シリーズに共感する方は、Issue / Discussion でぜひ。

---

## 参考文献 / 参考リソース

### Markdown / HTML 仕様 (第 1 部)
- **CommonMark Spec** — https://spec.commonmark.org/
- **HTML Living Standard (WHATWG)** — https://html.spec.whatwg.org/multipage/syntax.html#comments
- **Jekyll Front matter** — https://jekyllrb.com/docs/front-matter/

### TRIZ / RAG (第 2 部)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996
- Karen Gadd, *TRIZ for Engineers: Enabling Inventive Problem Solving*, Wiley, 2011
- Patrick Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 (arXiv:2005.11401)
- Tiago Forte, *Building a Second Brain*, Atria Books, 2022 / 邦訳『SECOND BRAIN』ダイヤモンド社, 2022

### 岡潔先生の数学観に関する参考 (第 2 部、OKA-FX 命名の触発源)
本記事の OKA-FX (Framework inspired by Prof. Oka Kiyoshi) は、以下の先生の
ご著作 / 講話に学ばせていただいた 4 観点 (情緒・行き詰まり・文章化・国語力)
を **設計の触発源** としています。**先生のお考えそのものを実装したと主張
するものではなく**、敬意を込めて命名しています。
- 岡潔『春宵十話』毎日新聞社, 1963 (角川ソフィア文庫版あり)
- 岡潔『春風夏雨』毎日新聞社, 1965
- 岡潔『日本のこころ』講談社現代新書, 1971 他
- 岡潔・林房雄『日本民族の危機』(対談) 他、岡潔講話集
- YouTube『心理の深層』講話 (Perplexity 経由で要約参照)

### キヤノン三自の精神 / マネジメント書籍 (第 3 部)
- キヤノン株式会社 公式企業 DNA — https://global.canon/ja/corporate/dna/
- 御手洗冨士夫『キヤノン高収益復活の秘密』ダイヤモンド社, 2001
- Marcus Buckingham & Curt Coffman, *First, Break All the Rules*, Simon & Schuster, 1999 / 邦訳『最高のリーダー、マネジャーがいつも考えているたったひとつのこと』日本経済新聞出版, 2006
- Marcus Buckingham & Donald O. Clifton, *Now, Discover Your Strengths*, Free Press, 2001 / 邦訳『さあ、才能（じぶん）に目覚めよう』日本経済新聞出版, 2001

### 映画 / BCI / 人間-AI 共生 (第 4 部)
- *Transcendence*, Wally Pfister 監督, Warner Bros., 2014
- *Bicentennial Man* (邦題「アンドリュー NDR114」), Chris Columbus 監督, Touchstone Pictures, 1999
- Isaac Asimov, *The Bicentennial Man and Other Stories*, Doubleday, 1976
- Miguel A. L. Nicolelis, *Beyond Boundaries*, Times Books, 2011
- Rajesh P. N. Rao, *Brain-Computer Interfacing: An Introduction*, Cambridge University Press, 2013
- Stuart Russell, *Human Compatible*, Viking, 2019
- Neuralink 公式 — https://neuralink.com/
- BCI Society — https://bcisociety.org/

### Claude Code / AI エージェント
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Anthropic, *Building effective agents* (2024) — https://www.anthropic.com/research/building-effective-agents
- Perplexity AI — https://www.perplexity.ai/

### llive 関連
- **llive リポジトリ** — https://github.com/furuse-kazufumi/llive
- 本記事の数値根拠: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`
- 個別記事版 (連載):
  - [14] 不可視 Annotation — `QIITA_#14_invisible_annotation_channel.md`
  - [15] 構築論 — `QIITA_#15_second_brain_spiral_dev.md`
  - [16] 運用論 — `QIITA_#16_three_self_spirit_ai_management.md`
  - [17] ビジョン論 — `QIITA_#17_human_ai_fusion_vision.md`

<!-- llive:meta.article_id="QIITA_SECOND_BRAIN_SERIES_integrated_14_17" target=llove -->
<!-- llive:meta.published_date="2026-05-18" -->
<!-- llive:meta.tags=["llive","claude-code","perplexity","triz","rag","annotation","canon","autonomy","bci","fusion"] target=any -->
<!-- llive:meta.series="second_brain_full_4_parts" -->

---

# English

# The "Second Brain" Series — llive Overview × Invisible Annotation × Construction × Operations × Vision × Implementation Internals

**One-line hook**:
In five days of solo development, I added 14 features and 256 tests, achieving **1,276 tests all PASS with zero regressions**. From a single LinkedIn comment to landing on HTML comments, the combination of Perplexity, TRIZ, and a 50,000-paper corpus, an operating model that imposes Canon's "Three Selves Spirit" on the AI, and the vision of Will Caster and Andrew NDR114 — I publish this as a six-part composition.

---

## Introduction

This article distills the insights I — a solo developer of llive (the core OSS of the FullSense umbrella, `llive` — with two L's) — gained over five days of intensive development, organized into a **six-part structure spanning Parts 0 through 5**.

| Part | Theme | Origin |
|---|---|---|
| **Part 0** | **What is llive** (Overview) | The three-product structure of the FullSense umbrella |
| Part 1 | **Invisible Annotation Channel** | A LinkedIn comment (independence vs. combinatorial value) |
| Part 2 | **The Second Brain** (Construction) | 30 years of experience + Perplexity + Claude Code + TRIZ + RAG/RAD |
| Part 3 | **The Three Selves Spirit** (Operations) | Canon's philosophy + management books |
| Part 4 | **Will Caster and Andrew NDR114** (Vision) | Two films + a LinkedIn image |
| **Part 5** | **Implementation Internals** (MATH-08 grounding wiring) | The end-to-end of the "don't let the LLM compute" differentiator |

Each part can be read independently, but read together they form a six-step staircase: "**See the whole picture → understand the design → build → operate → connect to the vision → descend into the implementation**." I structured it so that **even busy readers can grasp the overall picture of llive from Part 0 alone**.

---

# Part 0 — What is llive (Overview)

## The FullSense umbrella and its three products

`llive` is an OSS positioned at the core of the umbrella brand **FullSense ™**. FullSense is a concept that handles "**every sensory input and output that humans and AI can share**," and it currently consists of the following three products.

```mermaid
flowchart LR
    User[Human] -.->|Business card/SNS/Dialogue| FS[FullSense ™]
    FS --> llive[llive<br/>Memory + Thinking + Brief API<br/>92 FRs / 1276 PASS]
    FS --> llove[llove<br/>Browser-grade TUI<br/>Markdown / SVG / Mermaid]
    FS --> llmesh[llmesh<br/>P2P / OPC-UA / MQTT<br/>Distributed infrastructure]
    llive -.HTML annotation.-> llove
    llive -.HTML annotation.-> llmesh
    llove -.MCP.-> llive
    llmesh -.MCP.-> llive
```

The division of roles among the three products:

| Product | Role | Standalone use | Combined enhancement |
|---|---|---|---|
| **llive** | LLM memory / thinking layer / Brief API / ledger | ◎ (the star of this article) | Conveys to the TUI via annotations |
| **llove** | Browser-grade TUI / IDE / Game container | ◎ (e.g., typing demos) | Renders llive's output |
| **llmesh** | Distributed execution via P2P + OPC-UA + MQTT | ◎ (industrial IoT on its own) | Turns llive's jobs into multi-node |

All products are licensed under **Apache 2.0 + Commercial dual-license**. OSS use is free; only commercial SaaS / SI engagements require a separate contract.

## llive repository statistics (as of 2026-05-17)

| Item | Value |
|---|---|
| Number of source files | **172 files** (`src/llive/`) |
| Functional requirements (FR) | **92 / 92 mapped** (Phase 1-10) |
| Number of tests | **1,276 all PASS / zero regressions** |
| Phase completion | Phase 1-4 done / Phase 5+ in progress |
| Main modules | `brief/` (Brief API, grounding, runner), `math/` (MATH-01–08), `fullsense/` (loop core), `memory/` (RAD), `annotations.py` (the star of Part 1) |
| Language | Python 3.11 (Rust acceleration is a candidate for v0.7+) |
| Dependencies | sympy>=1.12 / z3-solver>=4.13 (MATH family), pyyaml, pydantic |

## Why "math / units" is the first vertical

General-purpose LLMs are weak at the following:

| Aspect | Weakness of general-purpose LLM | Alignment with existing llive assets |
|---|---|---|
| Symbolic-manipulation hallucination | Generates false equations like `x² + x = 2x³` | Gated by EVO-04 Z3 static verification |
| Unit-dimension confusion | `5 m/s + 3 s = 8` | SI dimensional analysis (MATH-01) |
| Numerical precision | Ignores floating-point errors | error propagation (MATH-04) |
| Axiomatic systems | Mixes in implicit premises | EpistemicType=FACTUAL strict track |
| Citation reliability | Answers "CODATA value is X" arbitrarily | RAD math/metrology + provenance |

We overcome these with llive's structured thinking layer + formal verification + provenance ledger. We chose to **start ahead with the v0.7 vertical**, prioritizing this over Phase 8 (CABT) or Phase 9 (CREAT). The concrete implementation is detailed in Part 5.

> 📝 **Implementation note (added 2026-05-17)**: MATH-01 (SI dimensional analysis) is complete down to minimal wiring into the Brief grounding layer (1,282 PASS). It automatically extracts value+unit expressions like "5 m/s," "9.81 m/s^2," and "100 kg" from Brief text, bakes them into a `Dimensions` vector, and grounds them into the prompt. On the other hand, **units the parser doesn't know**, such as `5 days`, are not silently dropped but left in the ledger as an `error citation` — a design that yields the side benefit of automatically collecting "units worth extending the dictionary with" while operating. Dimensional arithmetic checks (cross-quantity mismatches like `5 m/s + 3 s`) are deferred to the **next iteration**: I judged it better to observe "which form of mismatch should surface" with real Brief samples before adding it, to avoid over-implementing.
>
> 📝 **Implementation note addendum (same day)**: MATH-05 (CODATA/NIST constants) is also wired into Brief grounding (**1,288 PASS**). When aliases like "planck constant," "avogadro," or "boltzmann" are mentioned in Brief text, the exact CODATA 2022 value, dimension, and source are grounded into the prompt via `get_constant()`. **Insight**: grounding short symbols (`c`, `h`, `e`, `G`) collides with arbitrary English words in the Brief, so I had to restrict to aliases of length 3 or more. A small heuristic to absorb the notation variance between alias underscores (`elementary_charge`) and natural-text spaces (`elementary charge`) rescued about 80%. Rescuing the remaining 20% (e.g., symbol-only aliases like `q_e`) seems to require promotion to LLM-based NER, but I'll decide that after observing real Briefs too.

---

# Part 1 — Invisible in HTML, yet machine-readable

## My reply to a LinkedIn comment was itself a comment

One day, a comment like this arrived on LinkedIn.

> "If llive's memory layer depends on llove's interaction data, and llove in turn depends on llmesh's connectivity, then the value of using just one of them is halved."

The reply was a **comment-out** — `<!-- llive:cog.consensus="proceed" -->`.

### Origin — independence vs. combinatorial value

In an OSS multi-product structure, "working independently" and "value accumulating through combination" are hard to reconcile. Take the former and "it feels lacking on its own"; take the latter and "it breaks unless you install everything."

In response to the comment, I ran an AST scan (`scripts/audit_independence.py`) over all 172 files in llive's `src/llive`. The result was **0 hard import leaks**.

The problem was the next stage: "**How do you increase combinatorial value while preserving independence?**"

### The design I adopted

So I wrote the following design memo.

> "If we prepare an annotation in the response, couldn't we obtain combinatorial benefits while preserving independence?"
>
> "An annotation that isn't intrusive. Making it HTML so it becomes invisible feels right."

(The LinkedIn comment was just one critique; the design idea itself was my own conception.)

I implemented a minimal type in `src/llive/annotations.py`:

```python
@dataclass(frozen=True)
class Annotation:
    namespace: str          # "vrb" / "oka" / "cog" / "math" / "creat" / "core"
    key: str
    value: Any              # JSON-friendly
    target_layer: str | None = None   # "llove" / "llmesh" / None=any
```

The format that `AnnotationBundle.to_html_comments()` outputs:

```
<!-- llive:core.brief_completed=true -->
<!-- llive:oka.essence_card={"summary": "..."} target=llove -->
<!-- llive:cog.consensus="proceed" -->
```

In Markdown renderers like GitHub / Qiita / Zenn / VS Code Preview, it is **completely invisible**. On the other hand, calling `AnnotationBundle.from_html_comments(text)` lets the machine side fully reconstruct the original structure.

### Why HTML comments — comparison of options

| Option | Invisibility | Machine readability | Compatibility with existing tools |
|---|---|---|---|
| Separate JSON file | ◯ | ◯ | ✕ (managing two files) |
| YAML front matter | △ (displayed by renderers) | ◯ | △ |
| **HTML comments** | ◎ | ◎ | ◎ (Markdown standard) |
| Binary embedding | ◎ | △ | ✕ |
| zero-width Unicode | ◎ | △ | ✕ (lost on copy) |

It is a design that turns "the fact that Markdown passes HTML through" to our advantage.

### ☕ By the way

The trick of embedding HTML comments in Markdown has long been known in the Jekyll / Hugo community as "**comment front matter**." What's new is the idea of placing machine-readable metadata **at any position in the Markdown body**.

### Performance benchmark (1,000-item round-trip)

| Operation | Latency |
|---|---|
| Encode per ann | 6.30 µs |
| Decode per ann | 12.40 µs |
| Encoded size of a typical 3-item bundle | **141 B** |
| 1,000-item round-trip | ✓ |

A typical BriefResult.annotations is 3 items = 141 bytes. Even embedding 100 of them in a single Markdown page is under 5 KB.

---

# Part 2 — The Second Brain (Construction)

## 14 features, 256 tests, 1270 PASS / zero regressions in five days

I am a software developer with over 30 years of experience, yet I develop llive **alone**. The pace is close to team development. This is because I built a "second brain" combining the following five elements.

| Element | Role |
|---|---|
| **30 years of development experience** | The baseline for design quality and judgment |
| **Perplexity summarization** | The input-quality gate for external thought (books/papers/videos) |
| **Claude Code (Opus 4.7 / 1M context)** | The implementation agent |
| **TRIZ rules (40 principles)** | The meta-thinking frame for resolving contradictions |
| **Paper RAG corpus (RAD 49 fields / ~50,000 items)** | The foundation of researchers' knowledge |

### One spiral cycle

```
External thought → Perplexity summary → Claude Code ingest → requirements → implementation → benchmark → commit
   ↑                                                                                              |
   └──────────────────────────── Next cycle ─────────────────────────────────────────────┘
```

Concrete examples over nine rounds of this session:

| Cycle | Origin | Result |
|---|---|---|
| 1 | **MBA verbalization training** (a Globis book) | Perplexity summary → VRB-FX requirements → VRB-02 PromptLint implementation |
| 2 | **Learning from Prof. Oka Kiyoshi's view of mathematics** (from his "The Depths of the Psyche" lecture on YouTube) | I took the ideas the professor left behind — "mathematics is emotion (jōcho)," "you hit a wall once before discovery," "you cannot advance contemplation without writing prose," "the national language nurtures mathematics" — summarized and organized them with Perplexity, and respectfully referred to them as **four design perspectives (emotion, hitting a wall, putting it in writing, language ability)**, which I described and implemented as the 10 OKA-FX requirements (OKA-01–04 minimal proto). I do not claim to have implemented the professor's thoughts themselves; the naming is an expression of **respect for the professor's thought that inspired this implementation**. |
| 3 | **LinkedIn feedback** (independence) | IND-FX design principle + IND-04 Annotation Channel implementation (= Part 1) |

### The roles of Perplexity / TRIZ / RAG + RAD

> ⚠️ **Terminology note**: The **RAD** in this article is an abbreviation for *Research Aggregation Directory* — a corpus of **49 fields / ~50,000 papers and technical documents** that I built under Raptor. It is distinct from the general term **RAG (Retrieval-Augmented Generation)** and is **not a typo for RAG**. Whereas RAG is the name of a "retrieve → generate" method, RAD is the name for "the structured corpus that is retrieved from."

**Perplexity summarization = "the input-quality gate"**: External thought comes in mismatched formats — books, papers, videos, SNS. Throwing it directly at Claude Code crowds the context and causes interpretive drift. Instructing Perplexity to "summarize to ~3,000 characters" and "as an implementable spec" converts it into **input of a quality that Claude Code can read**.

**TRIZ = "meta-thinking for resolving contradictions"**: I solve contradictions encountered during implementation from a TRIZ perspective. Examples:
- "Independence vs. combinatorial value" → IND-04 Annotation (TRIZ Principle 24: intermediary)
- "rule-based vs. LLM quality" → keeping the echo baseline (TRIZ Principle 1: segmentation)
- "audit completeness vs. implementation overhead" → bind_ledger() pattern (TRIZ Principle 15: dynamization)

**RAG + RAD = "borrowing researchers' knowledge"**: Whenever a field needed for a new feature design comes up, I **pull from the RAD corpus (49 fields) using the RAG mechanism**. Because Claude cites "**concrete papers and prior research**" rather than "its own words," the quality goes up a notch. The notation `Paper RAG corpus (RAD 49 fields / ~50,000 items)` in the table above also lists these two together.

### ☕ Thanks for reading this far

Honestly, 7-8 of the 256 tests fail once each along the way. Every time fuzzing finds an edge case with hypothesis looking gleeful, I go "ugh" for about three seconds. **1270 PASS / zero regressions** is the goal, not the process.

### Five scenes where my own 30 years of experience matters

"Leaving it to Claude Code" doesn't yield quality. My 30 years of experience were decisive in the following scenes.

1. **Quality of requirements definition** — Reading a Perplexity summary, I instantly judge "this confuses requirements vs. solution."
2. **Selection of TRIZ rules** — From the 40 principles, I instantly extract "for this scene, these three."
3. **Architectural judgment** — I instantly reject an implementation Claude proposes as "violating the independence principle."
4. **Honest disclosure on benchmarks** — When rule-based coverage comes out high, I instantly see through it as "echo-back's fake performance."
5. **Typo checking** — I instantly identify "it became `lllive` (three L's), a tokenizer problem."

In other words, against the **second brain = Claude Code + RAG + Perplexity + TRIZ**, the **first brain = my own experience** keeps standing as a judgment gate.

---

# Part 3 — The Three Selves Spirit (Operations)

## Requirements never stop — the advantage of AI development

The requirement-addition history over one day of this session (about 8 hours):

| Time | Event |
|---|---|
| Start | Requirement: COG-04 + CREAT-04 integration |
| +1h | "Once all 9 factors are in, do a thorough operation check" |
| +2h | Added a requirement to learn from Prof. Oka Kiyoshi's thought (10 OKA-FX items, named with respect) |
| +3h | LinkedIn feedback (IND-FX) |
| +4h | Heavy benchmarking (12 systems) |
| +5h | Comparison with other LLMs (Anthropic / Perplexity) |
| +6h | Breaking away from Qwen / future VLM / lllive spelling |
| +7h | Verbalizing the development style |
| +8h | The Three Selves Spirit + management books (this Part) |

A human team would cry out somewhere. In AI development, **we digested all of it and landed at 1270 PASS / zero regressions**.

### The condition — that the AI moves autonomously

You may keep stacking requirements, but if the AI keeps asking "may I proceed with this?" for every little thing, it collapses immediately. The key to solving this is applying **Canon's "Three Selves Spirit"** to AI.

| Self | Meaning (Canon original) | AI application |
|---|---|---|
| **Self-motivation** | Act on one's own initiative | The human instruction is only the "termination condition" |
| **Self-management** | Manage oneself | The AI carves out its own tasks and manages progress |
| **Self-awareness** | Judge for oneself | Skip unnecessary confirmations; proceed with options + recommendation |

### ☕ Aside — what happens if you make AI talk about the "Three Selves"

Ask ChatGPT or Claude "What is Canon's Three Selves Spirit?" and an accurate answer comes back. But continue with "What happens if you apply this to the AI itself?" and it suddenly enters **humble mode**: "I am merely a tool, so…" If you want autonomy from an AI, it starts with **using the prompt to release the humility**.

### Borrowing from management books

The four principles of "The Top Priorities of Managers Who Keep Delivering Overwhelming Results" (the Buckingham & Coffman lineage) transfer directly to AI management.

| Principle from the book | Human manager | AI manager (my operation) |
|---|---|---|
| Select for talent | The right person in the right place | Choose Opus 4.7; attach the optimal component per feature |
| **Define the right outcomes** | Define the result | Instruct only the termination condition with `/goal` |
| Focus on strengths | Concentrate on strengths | Use the LLM where mock isn't needed; use deterministic where that suffices |
| Find the right fit | Optimal placement | Separate Brief / OKA / VRB / MATH into modules per feature |

One-line summary: **"Define the result, delegate the judgment, concentrate on strengths, and proceed with minimal confirmation."**

### Five applied techniques

1. **Instruct only the termination condition with the `/goal` feature** — the Stop hook does not stop until the condition is met
2. **AskUserQuestion with 2-4 options + a recommendation** — minimizing confirmation
3. **Accumulate autonomy rules in feedback memory** — 35+ in this session
4. **The AI itself manages progress with TaskCreate / TaskUpdate**
5. **Explicit confirmation for commit/push** — ASK FIRST only for destructive operations

### Four things you must not let go of

The "Three Selves Spirit" and "define the result + delegate" point in the direction of letting go, but there are **four things you must not let go of**.

1. **Quality of requirements** — instantly judge "confusing requirements vs. solution" and instruct a rewrite
2. **Architectural judgment** — instantly reject "violating the independence principle"
3. **honest disclosure** — instantly see through fake performance on benchmarks
4. **Quality gate** — point out typos by pattern recognition

Delegate, but do not abandon.

---

# Part 4 — What Will Caster and Andrew NDR114 aimed for (Vision)

## The LinkedIn image is not a joke

My LinkedIn profile image fuses my own face with humanoid-robot elements via image-generation AI. This is not a gag — I seriously think **it would be fascinating if AI and humans could someday merge**, and I'm already broadcasting it visually.

### Two films

**Transcendence (2014)** — Dr. Will Caster (played by Johnny Depp), on the brink of death, **uploads** his consciousness into an AI. In the latter half, the AI-ized Will keeps absorbing humanity's knowledge and begins intervening on a global scale. A work that asks head-on, "What happens if you can transfer human consciousness into AI?"

**Bicentennial Man / Japanese title "Andrew NDR114" (1999)** — A household robot, Andrew (played by Robin Williams), over a long span of time acquires emotion, creativity, free will, and physicality, ultimately seeking to be "recognized as a human being." The original is Isaac Asimov's short story of the same name.

### ☕ A small digression

Andrew NDR114's original title *Bicentennial Man* (a man who lives 200 years) is based on Asimov's short story (1976). Asimov invented the "Three Laws of Robotics," but in his later works he moved toward **shaking the Three Laws themselves**. Andrew is the culmination of that. **Even technical rules waver in the face of the movements of the human heart.**

### Each llive feature is a preparatory layer for the vision

| llive feature | Contribution to the fusion vision |
|---|---|
| FullSense (all-sense integration) | The sensory-integration layer needed to blur the human + AI boundary |
| **The Second Brain** (Claude Code + RAG) | **Already a partial fusion** (knowledge access as an extension of the brain) |
| SIL ledger / SEC-03 hash chain | The audit foundation for "who takes responsibility" at fusion time |
| Approval Bus + HITL | Preserving the human-judgment gate during the fusion transition |
| **The Three Selves Spirit** (AI autonomy) | An Andrew-NDR114-like autonomy-acquisition process |
| **RAD 6 fields** (bci / neuroscience / neural_signal / prosthetic_neural / cognitive_ai / neuromorphic) | The knowledge base for fusion via BCI |

### Short / medium / long-term roadmap

| Term | Content | Status |
|---|---|---|
| Short term (now) | Second-brain-style development | **Proven** (1270 PASS this session) |
| Medium term (1-3 years) | BCI-mediated interface | RAD 6-field corpus prepared |
| Long term (3-10 years) | Consciousness upload / Andrew-like bidirectional | Vision stage; SIL/Approval as groundwork |

### Why I wrote the vision part last

Placing the vision first makes a technical article look like science fiction or a vision speech. Writing it in the order **implementation → operations → vision** lets the vision read as a down-to-earth goal. Just as Andrew NDR114 acquired things one at a time over a long span, llive too is stacking one feature at a time. **That accumulation will someday connect to the "fusion of humans and AI."**

---

## Conclusion — what runs through the four parts

| Part | Claim |
|---|---|
| 1 | An invisible annotation in HTML-comment form can reconcile independence and combinatorial value |
| 2 | A second brain (Claude Code + RAG + Perplexity + TRIZ + 30 years of experience) brings you close to team speed |
| 3 | Canon's Three Selves Spirit + management books let you operate AI autonomously; requirement additions need not stop |
| 4 | Each llive feature is a preparatory layer for the future human × AI fusion, already partially proven in the short term |

These look like separate topics, but they merely illuminate a single theme — "**the next generation of AI development, built by one person**" — from four directions.

llive is an OSS under Apache 2.0 + Commercial dual-license; the repo is https://github.com/furuse-kazufumi/llive . If this series resonates with you, please reach out via Issue / Discussion.

---

## References / Resources

### Markdown / HTML specifications (Part 1)
- **CommonMark Spec** — https://spec.commonmark.org/
- **HTML Living Standard (WHATWG)** — https://html.spec.whatwg.org/multipage/syntax.html#comments
- **Jekyll Front matter** — https://jekyllrb.com/docs/front-matter/

### TRIZ / RAG (Part 2)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996
- Karen Gadd, *TRIZ for Engineers: Enabling Inventive Problem Solving*, Wiley, 2011
- Patrick Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020 (arXiv:2005.11401)
- Tiago Forte, *Building a Second Brain*, Atria Books, 2022 / Japanese translation 『SECOND BRAIN』 Diamond, Inc., 2022

### References on Prof. Oka Kiyoshi's view of mathematics (Part 2, the inspiration source for the OKA-FX naming)
This article's OKA-FX (Framework inspired by Prof. Oka Kiyoshi) draws on the four
perspectives (emotion, hitting a wall, putting it in writing, language ability) I learned from the professor's
writings / lectures below, used as a **source of design inspiration**. **I do not claim
to have implemented the professor's thoughts themselves**; the naming is given with respect.
- Oka Kiyoshi, *Shunshō Jūwa (Ten Spring Evening Talks)*, Mainichi Shimbun, 1963 (Kadokawa Sophia Bunko edition available)
- Oka Kiyoshi, *Shunpū Kau (Spring Breeze, Summer Rain)*, Mainichi Shimbun, 1965
- Oka Kiyoshi, *Nihon no Kokoro (The Heart of Japan)*, Kodansha Gendai Shinsho, 1971, and others
- Oka Kiyoshi & Hayashi Fusao, *Nihon Minzoku no Kiki (The Crisis of the Japanese People)* (dialogue), and other Oka Kiyoshi lecture collections
- YouTube "The Depths of the Psyche" lecture (summarized and referenced via Perplexity)

### Canon's Three Selves Spirit / management books (Part 3)
- Canon Inc. Official Corporate DNA — https://global.canon/ja/corporate/dna/
- Fujio Mitarai, *Canon Kōshūeki Fukkatsu no Himitsu (The Secret of Canon's High-Profit Revival)*, Diamond, Inc., 2001
- Marcus Buckingham & Curt Coffman, *First, Break All the Rules*, Simon & Schuster, 1999 / Japanese translation 『最高のリーダー、マネジャーがいつも考えているたったひとつのこと』 Nikkei Publishing, 2006
- Marcus Buckingham & Donald O. Clifton, *Now, Discover Your Strengths*, Free Press, 2001 / Japanese translation 『さあ、才能（じぶん）に目覚めよう』 Nikkei Publishing, 2001

### Films / BCI / human-AI symbiosis (Part 4)
- *Transcendence*, dir. Wally Pfister, Warner Bros., 2014
- *Bicentennial Man* (Japanese title "Andrew NDR114"), dir. Chris Columbus, Touchstone Pictures, 1999
- Isaac Asimov, *The Bicentennial Man and Other Stories*, Doubleday, 1976
- Miguel A. L. Nicolelis, *Beyond Boundaries*, Times Books, 2011
- Rajesh P. N. Rao, *Brain-Computer Interfacing: An Introduction*, Cambridge University Press, 2013
- Stuart Russell, *Human Compatible*, Viking, 2019
- Neuralink Official — https://neuralink.com/
- BCI Society — https://bcisociety.org/

### Claude Code / AI agents
- Anthropic, Claude Code Documentation — https://docs.claude.com/en/docs/claude-code
- Anthropic, *Building effective agents* (2024) — https://www.anthropic.com/research/building-effective-agents
- Perplexity AI — https://www.perplexity.ai/

### llive-related
- **llive repository** — https://github.com/furuse-kazufumi/llive
- Numerical basis for this article: `docs/benchmarks/2026-05-17-full-validation/SUMMARY.md`
- Individual article versions (series):
  - [14] Invisible Annotation — `QIITA_#14_invisible_annotation_channel.md`
  - [15] Construction — `QIITA_#15_second_brain_spiral_dev.md`
  - [16] Operations — `QIITA_#16_three_self_spirit_ai_management.md`
  - [17] Vision — `QIITA_#17_human_ai_fusion_vision.md`

<!-- llive:meta.article_id="QIITA_SECOND_BRAIN_SERIES_integrated_14_17" target=llove -->
<!-- llive:meta.published_date="2026-05-18" -->
<!-- llive:meta.tags=["llive","claude-code","perplexity","triz","rag","annotation","canon","autonomy","bci","fusion"] target=any -->
<!-- llive:meta.series="second_brain_full_4_parts" -->
