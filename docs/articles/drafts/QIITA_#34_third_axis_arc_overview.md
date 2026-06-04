---
title: "llcore — 「進化で AI を設計するとき、選り分けて育てる工夫 (③) は要るのか」を 6 段の実験 + 生物学で俯瞰した話 (第三軸 arc 全体)"
tags: ["Python", "進化計算", "MAP-Elites", "honest disclosure", "進化生物学"]
private: true
updated_at: "2026-06-02"
id: ff1f2b6c29e41abab10d
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# (連載 #34) 山登り 6 連戦で分かった「いつ進化の③は効くのか」— そして 100 年前の進化生物学が同じ答えを出していた

## TL;DR

- 問いは **「AI のコア計算を進化で探すとき、"選り分けて分けて育てる工夫" (= 進化の③ 適者生存/分離) は本当に要るのか」**。連載 #33 は最終局面 (Step D + BG9) の決着を書きましたが、**この #34 は arc 全体 (6 段) を 1 つの物語として俯瞰**します。
- **第1段 (合成だまし地形)**: ③は圧勝 (Cliff δ=+1.0)。③は機構として本物 = **存在証明**。
- **第2段 (記憶タスク / 多 reservoir)**: 基質の「床」と「天井」に阻まれて③を測れず = **N/A**。
- **第3段 (多タスク汎化)**: ③は「選択なし」には勝つが、単純な選択や random には勝てず = ③不要 (honest negative)。
- **第4段 (実 proxy 地形を noise-free 測定)**: 評価ノイズを物理的にゼロまで落としたら地形は **本当に滑らか (単峰)** = ③不要を確定。「過去の negative は検出力不足ではなく地形が滑らかだった」が初めて裏付いた。
- **第5段 (部品 4 種を混ぜる抜け道 BG9)**: kernel 選択は **低次元**ゆえ強 baseline (ランダムリスタート山登り) が直接サンプルし、③の niching 優位が**構造的に**出ない = 抜け道は閉じた。
- **構造的洞察 (この arc の核)**: ③が効くのは難所が **高次元 behavior 空間**にあって直接サンプル不能なときだけ。実 CPU 基質は低次元/滑らかなので③不要。
- **生物学的接地 (検証済み)**: これはライト (Wright) の **シフティング・バランス説**そのもの。**暗化モフ (単一遺伝子 = 低次元)** では普通の選択で十分 (= BG9 の kernel ケース)、**レンスキーの Cit+ (高次元・歴史依存)** では多様性が効く (= ③ regime)。私たちの negative は **コイン批判 (現実の地形は単純で③は稀にしか決定的でない) の計算版**。
- **メタ教訓**: 「うまく行きすぎた結果は勝ちでなく警報」。事前登録・honest disclosure・敵対検証・決定論 noise-free 測定で、ぬか喜びを避けた。

> ⚠ この記事の数値は、すべて手元 (ローカル) の研究記録に紐づく実測です。llcore はまだ公開リポジトリを作っていないので、外部リンクは貼れません。代わりに「どう測ったか」を本文に書きます。生物学パートで引用する論文は、別途一次情報で存在・帰属・主張内容を照合したものだけを挙げています。

---

## 0. この記事は何の話か (コンセプト)

`llcore` は「Transformer のコア計算 (状態更新則・学習則・認知駆動 Δ) を遺伝子にして、Z3 で壊れないように検証しながら進化させる」CPU 完結の研究フレームワークです。

その進化エンジンには、進化の 4 要素 (① 変異 / ② 遺伝 / ③ 適者生存・分離 / ④ 過剰繁殖) のうち、**③ (selection / separation)** をどう効かせるか、という設計上の急所があります。多様性を保ってニッチに残す MAP-Elites のような「選り分けて分けて育てる」仕組みです。

問いはシンプルです。

> **その③、本当に要るの?**

要るなら、③を載せるための重い投資 (最終的には GPU で実 LLM を回す) に意味がある。要らないなら、③にこだわるのは時間と電気の無駄になる。

連載 #33 では、その問いの **最終局面** (Step D の決定論測定 + BG9 の構造的決着) を詳しく書きました。でも、そこに至るまでには **6 段の実験**があり、勝ったり (存在証明)、測れなかったり (N/A)、負けたり (honest negative) を繰り返していました。この #34 では、その **arc 全体を 1 つの物語**として並べ直します。さらに今回の目玉として、**この計算結果が 100 年近く前の進化生物学の論争 (ライト対フィッシャー) と驚くほど同じ形をしている**ことを、検証済みの一次情報で接地します。

— ここまで 40 秒。準備運動おわり。本題へ。 —

---

## 1. たとえ: 山登りと、だまし地形と、記憶の宮殿

数式の前に、この研究で一貫して使っている 3 つのメタファーで全体像を掴みます。

設計の良し悪しを **地形の高さ**で表します。**高い場所 = 良い設計**。一番高い頂上を探すゲームです。

**地形その1: 滑らかな一つ山 (簡単)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

こういう地形では、素朴な「山登り法 (hill-climbing)」、つまり「今より少し良い方へ動くだけ」で十分に頂上へ着きます。**凝った工夫 (③) は要りません**。

**地形その2: だまし地形 (欺瞞的 deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

ここでは素朴な山登りはニセ頂上で止まります。谷を下る勇気がないからです。

このとき効くのが③の発想です。**いろんなタイプの登山者を谷のあちこちに残しておく** (= 記憶の宮殿 / MAP-Elites archive)。誰かが谷を「飛び石 (stepping-stone)」で渡って本物の頂上に到達できる、という仕組みです。

**この研究の核心を一言で**: ③が本当に役立つのは **「だまし地形」のときだけ**。滑らかな一つ山では、③は無用の長物です。

だから問いは、こう言い換えられます。

> **「進化で AI を設計するとき、実際に出くわす地形は "だまし地形" なのか、それとも "滑らかな一つ山" なのか?」**

#33 では Step D + BG9 でこの問いに決着をつけました。この #34 では、そこに至る **6 段の山登り全部**を見せます。各段で「だまし地形だったか / 滑らかだったか / そもそも測れたか」が変わるのが面白いところです。

— 小休止。準備はここまで。ここから 6 連戦の実録です。 —

---

## 2. arc 全体マップ — 6 段の山登りを一望する

先に地図を出します。これがこの記事の背骨です。

| 段 | 基質 (どんな地形を測ったか) | ③は効いたか | 一言 |
|---|---|---|---|
| **I (Step 4)** | 合成した「だまし地形」(欺瞞 corridor) | **Yes (圧勝)** | 存在証明。③は本物 |
| **II (Step C / 梯子1)** | 記憶タスク / 多 reservoir パリティ | **N/A** | 床・天井・degree-5 の壁で測れず |
| **III (E-A)** | 多タスク汎化 | **No** | ③は「選択なし」には勝つが、それ以上ではない |
| **IV (Step D)** | 実 proxy のテキスト地形 (決定論測定) | **No** | 地形が**本当に滑らか**と確定 (noise-free) |
| **V (BG9)** | 部品 (kernel) 4 種の union | **No** | **構造的に**閉じた (低次元選択) |

ストーリーラインはこうです。**まず「③は条件次第で圧勝する本物だ」と存在証明し (I)、次に「では実問題ではどうか」を 4 段かけて測りに行ったら (II〜V)、ことごとく "実 CPU 基質は③が要らない地形だった"**。しかも最後 (IV, V) で「要らない理由」が **検出力不足ではなく地形の性質**だと確定した ── これが arc 全体の弧 (アーク) です。

では 1 段ずつ。

---

## 3. 第I段 (Step 4) — 存在証明: だまし地形なら③は圧勝する

最初にやったのは「③が **理屈どおり効く場面が実在するか**」の存在証明です。地形を **わざと欺瞞的に作って**、③ (MAP-Elites) を 3 つの baseline ── pure random / panmictic GA / **ランダムリスタート山登り (random-restart hill-climbing)** ── と勝負させました。

**地形の作り**: 遺伝子は 24 次元。behavior (登山者のタイプ) を `mean(遺伝子)` = 24 個の平均で定義します。behavior を上げるには **全 24 次元を同時に高く**しないといけない。fitness は「behavior≈0.4 にニセ頂上 (値 0.6) → behavior≈0.65 に谷 (値≈0) → behavior≈0.9 に本物の頂上 (値 1.0)」という、まさにだまし地形。

**結果**:

| 方法 | 本物の頂上への到達率 | ③ との比較 |
|---|---|---|
| **MAP-Elites (③)** | **約 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | 同上 |
| ランダムリスタート山登り | 0% | 同上 |

③ だけが本物の頂上に着き、3 つの baseline は全部ニセ頂上 (≈0.60) で止まりました。**100% 勝ち / 効果量は理論最大 (δ=+1.0)**。base seed 3 通り (計 60 seed) で頑健。

なぜこうなるか、が後の伏線になります。

- **random** は behavior が必ず ≈0.5 に集中する (24 個の平均は中心極限定理で 0.5 に固まる)。だから behavior 0.9 には **永遠に到達できない** (6000 サンプル引いても 0%)。
- **山登り** はニセ頂上 0.6 まで登り、谷を下る一手を拒否。リスタートしても behavior≈0.5 に戻り、同じ罠へ。
- **③ (MAP-Elites)** は谷のマスを「新しい behavioral ニッチ」として保持し、behavior を 0.5 → 0.9 へ **飛び石で渡る**。

**境界も正直に測りました**。谷を消した滑らかな corridor では、③ は山登りに勝てなくなる (p≈0.29)。**③ は万能ではなく、だまし地形でだけ効く**。

**honest 留保**: これは **わざと作った**合成地形です。③が「可能」だと証明しただけで、現実のタスクがこの構造を持つ証明ではない。toy スケール・低ノイズ・baseline は素朴な (1+1) です。

→ ここで仮説が立ちます。**「実問題の地形も、これくらいだまし地形なら、③は活きるはず」**。次の 4 段は、それを実問題に近い基質で確かめに行く旅です。

— 一服。第I段は気持ちのいい圧勝でした。ここから雲行きが…。 —

---

## 4. 第II段 (Step C / 梯子1) — 基質の「床」と「天井」に阻まれる (N/A)

次に「だまし corridor が **標準的な記憶タスクに自然に出現するか**」を調べました (Step C)。delayed parity / flip-flop / delayed recall を、1 個の leaky reservoir + ridge readout で。

結果は綺麗な **N/A (測定不能)**。理由が両極端で面白い。

- **delayed parity = 床 (floor)**: 1 個の reservoir は XOR を計算できない (Minsky-Papert)。全方法が R²≈0.003。誰も登れないので③を分離できない。
- **flip_flop = 天井 (ceiling)**: 全方法が R²≈0.95 に飽和。分散が潰れて③の差が出ない (③ vs random は符号は正だが p=0.15 = underpower で **null ではない**)。

ここで大事な発見が 1 つ。**遺伝子空間の多峰性は高かった** (valley fraction が parity で 1.000) のに、③の役には立たなかった。つまり **「遺伝子空間で多峰」≠「behavior で渡るべきだまし地形」**。この区別が arc 後半の鍵になります。

**梯子1 (多 reservoir)**: では reservoir を複数つなげば床が上がるか? → 5 つの機構を試して全部 `floor_lifted = false`。深さ (DeepESN) は床を統計的には上げる (効果 +0.47/+0.60, PASS) が絶対値は R² 0.05-0.10 止まり。決め手は positive control: degree-2 readout は 2-bit XOR を厳密に解く (R²=+1.0) が degree≥3 で破綻。**5-bit パリティは degree-5 = この CPU reservoir+ridge パラダイムの構造的な壁**。

→ パリティ路は構造的に塞がれた。③の本検定は **パリティから降りる**必要がある。

**honest 留保**: degree-5 の壁は「この設定の壁」であって、パラダイム全体の不可能性証明ではありません。

— 小休止。「測れなかった」という結果は地味ですが、地図を描く上では大事な空白地帯です。 —

---

## 5. 第III段 (E-A) — 多タスク汎化: ③は要らなかった (honest negative)

パリティの床を降りて、**汎化 (generalization)** で③を測りました。一番きれいな ablation を組んで。

**設定**: 単層 leaky reservoir + ridge。可変遅延の recall。**短い遅延 {15, 30} で学習し、長い遅延 {45, 60} でテスト** (外挿)。比較は MAP-Elites (①②③フル) vs **選択を抜いた MAP-Elites** (`randselect`: 親をランダムに選び無条件配置 = 変異だけ) + panmictic GA + random。

**結果 (ペアレビュー後)**:

| 方法 | テスト汎化 R² (平均±std) |
|---|---|
| MAP-E (①②③フル) | 0.682 ± 0.115 |
| MAP-E randselect (選択を抜く) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| ゲート | 比較 | diff | p (片側) | 判定 |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**読み方**: ③は「**選択を抜いたドリフト対照**」には勝つ (C-gen3 PASS = "何らかの選択は無選択に勝つ")。でも **panmictic GA (選択はあるが niching なし) には勝てない** (むしろ僅かに負け)、random にも勝てない。つまり **niching 固有 (= ③ 本来) の寄与は無い**。この汎化地形は、単純な選択や random でも同じところに着くくらい **滑らか**だった。第I段の「滑らかなら③は効かない」境界と整合します。

**honest 留保 (重要)**: この verdict は **この設定限定** (予算 400, grid 6×6)。さらに ── ここが honest methodology の肝 ── ペアレビュー (Codex) が当初「信用できない」と判定し、3 つの rerun ブロッカー (replicate ごとの独立 seeding / 予算内グローバル最良の採用 / honest_n を 16→30) を強制しました。**修正後も結論は変わりませんでした**。「直したら結論が変わる脆い negative」ではなかった、というのが収穫です。

— 一服。負けは負けですが、「正しく負けた」ことを確かめる作業の方が時間がかかりました。 —

---

## 6. 第IV段 (Step D) — 実 proxy 地形は「本当に滑らか」と確定 (noise-free)

ここが arc の転回点です。第III段までで「③ negative」が続いたが、ずっと **しこり**が残っていました。

> 「③不要」は本当に **地形が滑らか**だからか? それとも単に **サンプル数が足りず差を検出できなかった (underpower)** だけか?

これを取り違えると「③ は無力」と過剰一般化してしまう。Step D はここに決着をつけます。

**トリック**: ESN reservoir (固定 seed) + ridge readout の closed-form (`np.linalg.solve`) は **乱数を一切引かない**。だから評価ノイズを **機械イプシロン (約 1.11e-16)** まで物理的にゼロ化できる。実測で `eval_noise_std ≤ 1.11e-16` を確認 ── これは浮動小数点の最小単位 (ULP) 由来で **実質ゼロ**です。ノイズの霧を完全に晴らして、地形の谷を直接測れる。

地形は llcore 自身のソース (約 24k 文字) の次文字予測。valley_fraction (谷の割合、≥0.2 で多峰=だまし地形) を測りました。

| 地形 | 次元 | valley_fraction (mean/max) | 多峰? | 判定 |
|---|---|---|---|---|
| **ESN 3-param** (実 proxy) | 3 | **0.000 / 0.000** | No (3 seed 一致) | 滑らか → ③不要を noise-free で確定 |
| **ESN per-neuron** (実 proxy) | 40 | **0.096 / 0.121** | No (3 seed 一致) | smooth 寄り → ③不要 |
| 多峰 control (正) | 3 / 40 | 0.70 / 0.80 | Yes | 診断器は多峰を検出できる ✓ |
| 二次関数 control (負) | 3 / 40 | 0.000 | No | 診断器は滑らかを検出できる ✓ |

ポイントは 2 つ。

1. **実 proxy 地形 (3 次元 / 40 次元とも) は単峰**。3 seed で一致。
2. **診断器そのものは健全**。わざと作った多峰はちゃんと多峰と検出し、二次関数はちゃんと滑らかと検出する。だから「実 proxy が単峰」は計器のバグでなく **地形の性質**。

→ これで初めて **「過去の③ negative は underpower ではなく、地形が本当に滑らかだった」** が実 substrate 上で noise-free に裏付きました。再測しても多峰は出ない。

**honest 留保 (重要)**: 「滑らか」は閾値近接でだけ精密です。ESN 3-param の midpoint の **90.9% がわずかに下方に dip** し、最大相対 dip (0.0435) は谷閾値 0.05 の直下。正確には「**真に単峰**」ではなく「**閾値を僅かに下回る浅い谷 (~2-4%) を持つ弱 multi-basin**」。方向は維持されるが、頑健性は閾値近接ゆえ限定的 ── ここを「完璧な凸の器」と丸めない、が今回の規律です。

— 深呼吸。ここで「実物もどきは滑らか」が確定。残るは「最後の CPU 抜け道」です。 —

---

## 7. 第V段 (BG9) — 部品を混ぜる抜け道は、構造的に閉じていた

実 proxy が滑らかと確定した以上、滑らかな地形で③を追っても利得は出ない。でも GPU は投資判断なので、**CPU で前進できる別仮説**を試しました。それが **kernel 多様化 (BG9)** です。

**仮説 (事前登録 H7)**: 個々の kernel (rwkv / mamba / hopfield / linear_attn) が滑らかでも、**4 種類を union すると kernel 切替の瞬間に fitness が段差を作る → multi-basin (だまし地形) になる → ③が GPU なしで CPU 上で立つ**。事前登録した honest prior は **null 寄り** (これまで全 CPU 基質が滑らかだったので)。

結果を 3 段で。

**(1) substrate validity — 弁別はあるが弱い (PASS だが要注意)**: タスクごとに得意 kernel が違うか測ると、写像は非定数 = non-inert (PASS)。mamba は selective-copy、linear_attn は weighted-accumulation で best。ただし **hopfield はどのタスクでも勝てなかった** (対角スカラ mock で機能不全) ので、実質「**3 kernel** union」。**弁別の存在 ≠ 多峰障壁**。

**(2) harness validity — positive control が validate しない (決め手)**: 合成 kernel-barrier で③を 3 baseline と比較。

| 基質 | 結果 |
|---|---|
| **positive control** | ③ は panmictic (+0.423)・random (+0.208) を撃破。**だが RR (ランダムリスタート山登り) には勝てない** (+0.051, p=0.31 → FAIL)。3 baseline 全勝に届かず = harness が立たない |
| **negative control** | 全 method 飽和、③ 優位なし = 正しく null (計器は健全) |
| **real** smoke | ③ beaten 0/3、panmictic が逆に③を上回る |

第I段の corridor では③が RR を排除できたのに、**なぜ kernel 空間ではできないのか?** 根因は 1 つ。

> **RR は restart のたびに kernel_id ∈ [0,4) を直接サンプルできる**。kernel 選択は 4 離散の単一座標 (**低次元**) なので、RR は restart で全 4 kernel を直撃する。「best kernel を探す」のに谷を跨ぐ必要がない = **直接ワープ**。だから③の behavioral niching に出番が来ない。

第I段で③が RR を排除できたのは、そこの behavior が `mean(24 次元)` で、平均が 0.5 に集中 → 大域ピークが measure-zero 域 = **直接サンプル不能な高次元**だったから。kernel_id は逆に低次元で直接サンプルできてしまう。

**(3) red-team — 敵対検証でも反証できず、むしろ確証**: instrumented RR が positive control 上で 4 basin に restart kernel を [12,18,16,18] とほぼ一様分散、target 到達 88%。4 つの faithful 構成 (高次元 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) すべてで③は RR に勝てない。corridor を締めると③が **先に starve (餓死)** する (D=3: ③ reach 0.08 vs RR 0.42)。**「RR だけ排除して③が通る behavior 次元は、kernel 空間に構造的に存在しない」**を定量確証。

**verdict**: 形式上は N/A (positive control が validate しない) だが、実質は **決定的な構造的 negative**。harness は健全 (negative control を正しく null にし、GA/random を検出する) なのに、基質が③のだまし地形を **そもそもホストできない**。第I段で残った問い「kernel 多様化で探索空間を拡張すれば③が unlock するか?」への答えは **NO (CPU では構造的に)**。

**honest 留保 (重要)**: これは **「③不要と判明」ではありません**。「③が低次元 kernel 空間では強 baseline と原理的に分離できない」= **情報量のある N/A**。③の機構自体は第I段で本物と確定済み。substrate は弱い (実質 3 kernel、hopfield は対角 mock)。より強い kernel 実装なら別結論の余地は理論上あるが、**構造的障壁 (低次元選択 → RR 直接サンプル) は kernel 実装の質と独立**です。

---

## 8. 構造的洞察 — 6 段を 1 つの条件でまとめる

存在証明 (I) と 4 つの negative (II〜V) は、たった 1 つの条件で全部つながります。

> **③ (behavioral niching) が強 baseline を上回るのは、「難所」が高次元 behavior 空間にあって、直接サンプリング (ランダムリスタート) で到達できないときだけ。**

- **第I段が満たす理由**: behavior = `mean(24 次元)`。平均は中心極限定理で 0.5 に集中し、大域ピーク (mean≈0.9) は実質 measure-zero。random も restart も**直接届かない**。だから飛び石を残してラチェットする③が必須。
- **実 CPU 基質が満たさない理由**: 難所が低次元。ESN テキスト proxy の制御座標は実質 leak rate (滑らかな低次元ノブ、そもそも谷が無い)。kernel union の難所は「どの kernel か」= 4 択の単一離散。RR が直接サンプルして全 basin に teleport するので、渡るべき谷が無い。

だから第II段の「遺伝子空間の多峰性 1.000」は十分条件ではない ── 遺伝子は谷だらけでも、難所が低次元 behavior 座標に集中していれば、restart が直接届く。**効いてくるのは "探索が到達すべき behavior の次元" であって、遺伝子の次元ではない**。

---

## 9. 生物学的接地 — 100 年前の進化生物学が、同じ答えを出していた

ここからが #34 の目玉です。**「多様性を保つ選択は、狭い条件でだけ効き、それ以外では冗長」** ── この境界条件には、20 世紀の進化生物学に異常にきれいな先例があります。

> ⚠ **honesty 契約**: 以下の生物学は **「たとえ話 (structural analogy)」であって、私たちの計算結果の証明ではありません**。対応は構造的で、機構レベルでは一致しません。たとえがずれる箇所は全部その場で明記します。引用する論文は、別途一次情報で存在・帰属・主張内容を照合したものだけです。

### 9.1 ライト (Wright) のシフティング・バランス説 = ③の先例

シューアル・ライト (Sewall Wright, 1931/1932) はこう考えました。大きな「一つの群れ (panmictic population)」のままだと、ふつうの自然淘汰では **目の前の局所ピークに捕まる**。もっと高い山へ行くには一度 mean fitness を **下げて谷を渡る**必要があるのに、決定論的な選択はそれを拒むから。

ライトの解決策は **群れを多数の半隔離されたサブ集団 (deme) に分ける**こと。

- **Phase I**: 小さな deme が**遺伝的浮動 (drift)** で偶然、谷を下って渡る。
- **Phase II**: そこで deme 内のふつうの選択が新しい (より高い) ピークを登る。
- **Phase III**: 高いピークに乗った deme が多くの移住者を出し、優れた遺伝子組合せが種全体に広がる。

メタ集団 **全体**として、単一収束集団には渡れない谷を渡る ── これが「だまし地形の谷を飛び石で渡る」の生物学版です。

**③ / MAP-Elites への対応 (= たとえ話、帰属ではない)**: archive の各セル = 準隔離 deme、セル内の局所 elitism = deme 内選択 (Phase II)、セル間変異 = interdeme 拡散 (Phase III)、そして **archive 全体** (≒メタ集団、単一セルではない) が谷を渡る。

> **honesty 注意 (2 点)**:
> 1. **これは解説者の枠組みで、ライトの主張でも MAP-Elites の出自でもない**。MAP-Elites の原論文 (Mouret & Clune 2015) も QD 文献も **ライトや「シフティング・バランス」を引用していない**。ライトは私たちの **着想 / たとえ**として挙げるのであって、MAP-Elites の系譜としてではない。
> 2. **機構は構造的に似ているだけで同一ではない**。MAP-Elites の谷渡りは **変異オペレータ**が子を新セルに置くことで起き、**遺伝的浮動ではない**。archive は複製するセルの集団でもない。

### 9.2 ライト対フィッシャー = 次元 (地形の形) の軸

ライトと同時代のフィッシャー (R. A. Fisher, 1930) は逆を主張: **大きな panmictic 集団 + 加法的分散へのマス選択で十分**に適応は進む、わざわざ分割は要らない、と。

二人の **一番深い対立軸は、実は「エピスタシス (遺伝子間相互作用) と地形の形」** でした。ライトは「非加法的相互作用ゆえ地形は**でこぼこ多峰**、だから谷を渡る drift が要る」と仮定し、フィッシャーは「相互作用はあるが重要でない、地形はほぼ**単峰で滑らかに登れる**、だからマス選択で足りる」と判断した。

**この epistasis/ruggedness の軸が、まさに私たちの結果が生きている次元です。地形の形 (topology) こそが全問題**。地形が本当にでこぼこ高次元なら (ライト regime) 多様性が谷を渡し、滑らか or 難所が低次元なら (フィッシャー regime) マス選択 ── すなわち **強いランダムリスタート山登りの生物学版** ── で既に足りる。私たちの ESN テキスト proxy は noise-free で滑らか、kernel union の難所は低次元離散。**どちらもフィッシャー regime** で、③は効かないし効かなかった。

> 細かい注意 (正直に): 「フィッシャーは drift を無視した」は俗説の圧縮です。正確には「drift はあると認めたが、大きな集団では量的に無視できると判断した」。完全否定ではない。

### 9.3 私たちの negative = コイン批判の計算版

一番効いてくる対応は、ライトの **提案**ではなく、生物学界の **経験的判定**の方です。Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) はシフティング・バランス説を理論・実証の両面から評価し、こう結論しました (全文照合済み)。

- **マス選択でたいてい足りる**。「ライトの三段階機構の方が単純なマス選択よりうまく説明できる実例はほとんど無い」。人為選択実験も「分割集団の選択が大集団のマス選択より大きな応答を生む」ことを示せなかった。
- **シフティング・バランスが効くのは限定的・稀少な条件下だけ**。集団構造の経験的推定からは「**浅い谷で隔てられたピーク間でしか drift は移動を起こせない**」(深い谷は drift では稀にしか渡れない)、しかも **大半の適応は谷渡りを必要としない**。

これは私たちの結果の **驚くほど正確な生物学版**です。彼らの言葉を私たちの語彙に翻訳すると ── **地形が真にだまし的/高次元でないなら、ふつうのマス選択 (≒強いランダムリスタート山登り) で既に解け、多様性維持の装置はほとんど何も買わない**。「現実の谷はたいてい浅い、大半の適応は谷渡り不要」は、私たちの「**実地形はたいてい単純だから niching は冗長**」の生物学的言明です。

> **honesty 注意 (3 点)**:
> 1. **彼らはシフティング・バランスを「反証」していない**。Phase I/II は起こりうると明言し、6 件の経験事例も挙げている。主張は **より狭い確率的なもの** (「一般的・重要な機構とは言い難い」) であって、「refuted」と書けば言い過ぎ。
> 2. **論争はまだ決着していない**。Wade & Goodnight (1998)、Peck et al. (1998, タイトルが文字通り「feasible」と主張) が反論し、Coyne らの 2000 年の再反論、Goodnight & Wade の同号反論と続いた。1997 批判を「最終結論」として引いてはいけない。
> 3. **生物には計算側に対応物のない機構があり、しかも私たちより強い主張をしている**。Phase III では、多様性を守る gene-flow 障壁が **良い解を周辺 deme に閉じ込めて広がりを妨げる** = niching が **逆効果**になりうる。私たちの stateless な離散選択設定にはこの cost の対応物が無いので、ここは **過剰に重ねない**。生物の方が一段強い主張をしている箇所です。

### 9.4 二つの実例 — 低次元の蛾と、高次元の大腸菌

私たちの主張には 2 つの極 (低次元 = ③不要 / 高次元 = ③が効きうる) がありますが、進化生物学はそれぞれにきれいな実例を持っています。

**低次元の極 ── オオシモフリエダシャクの工業暗化 (= BG9 kernel ケース)**: *Biston betularia* の carbonaria (黒) vs typica (白) は **単一メンデル座位・少数アレル** (原因変異は cortex 遺伝子への転移因子挿入; van't Hof et al. 2011/2016) で、**強い方向性選択** (s ≈ 0.1-0.2; Saccheri et al. 2008; 捕食は Cook, Grant, Saccheri & Mallet 2012 で再確認) を受ける。最適は各時点で単峰、環境でシフトするだけ。**単純な方向性選択 ── greedy 山登り/ランダムリスタートの生物学版 ── が直接、適者モフを固定し、多様性維持機構は不要だし呼ばれていない**。これがまさに BG9: kernel 選択は 4 択の低次元単一座標で、RR が全 kernel を直接サンプルし、③が構造的に分離できない。**暗化モフ = BG9 kernel ケースの生き物版**。

> 注意 (正直に): 移行期には多型が一時保たれるが、それは **空間的環境不均一 + 遺伝子流動 (移住-選択平衡)** によるもので、内在的な多様性保存機構ではない。たとえが少しずれる箇所。

**高次元・歴史依存の極 ── レンスキーの Cit+ (= ③ regime)**: 大腸菌長期進化実験 (LTEE) で、好気的クエン酸利用 (Cit+) は **12 集団中ちょうど 1 つ**で約 31,500 世代目に進化した (Blount, Borland & Lenski 2008)。鍵は **順序立った potentiation (前駆変異の蓄積) → actualization (citT のタンデム重複によるプロモータ捕獲) → refinement** という高次元・歴史依存の経路 (Blount et al. 2012)。リプレイ実験が「歴史的偶発性」を「一定率の稀変異」から区別した。これは contingency・epistasis・高次元でこぼこ地形を探索する価値を **本物で例示**する ── ③ が効きうる regime の実例です。

> **honesty 注意 (これは私たちの条件文の "前件" にしか対応しない)**:
> - **LTEE は niching アルゴリズムを使っていない**。ただの自然選択で、12 並列集団は **それ自体がランダムリスタート的な設計**。だから「contingency + 多様性が稀な革新を可能にする」存在証明であって、「niching が強 restart baseline に勝つ」証拠 **ではない**。
> - 「大腸菌がゼロからクエン酸を食べる力を獲得」は俗説の誇張。革新は **制御 (既存トランスポータの好気発現) = exaptation** で、新規遺伝子でも新規生化学でもない。
> - Van Hofwegen et al. (2016) が「直接選択ならもっと速く Cit+ が出る」と示し、「稀/偶発」枠組みに異議を唱えた (Lenski 側は LTEE 条件下の potentiation とは矛盾しないと反論)。「極めて稀/長期遅延」物語に寄りかかるなら、この **係争中の追試**も併記すべき。

### 9.5 接地のまとめ

| 極 | 生物学 | 地形 | ③は効く? | 私たちの基質 |
|---|---|---|---|---|
| 低次元/滑らか | 暗化モフ (単一座位, s≈0.1-0.2, 方向性) | 単峰・シフト | **No** — マス選択で十分 | BG9 kernel union; ESN/ridge テキスト proxy (決定論・滑らか) |
| 高次元/偶発 | レンスキー Cit+ (potentiation→actualization→refinement) | でこぼこ・変異で谷越え | **Yes** (効きうる regime) | 合成だまし corridor (behavior = 24 次元の平均) |
| 経験的判定 | コイン・バートン・トゥレリ: マス選択でたいてい足りる、シフティング・バランスは稀にしか決定的でない | 実地形はたいてい単純 | 私たちの **negative の鏡** | 試した全 CPU 基質 |

**結論**: ライトのシフティング・バランスは「③が効くとき**なぜ**効くか」の正しい生物学先例、ライト-フィッシャーの epistasis/ruggedness 軸は「**次元**条件」の正しい枠組み、暗化モフとレンスキー Cit+ は低次元/高次元の clean な両極、コイン批判は私たちの **negative** の生物学先例。**ただし、これらは計算結果を証明しない。接地するだけ**。たとえが一番ゆるむのは、生物が cost (Phase III の gene-flow trap) を加える点 ── 私たちの stateless 設定にはそれが無い。

— 一服。100 年前の論争が同じ形だと気づいたときは、正直ゾクッとしました。ただし「ゾクッとした」を「証明」と取り違えないのが今回の規律です。 —

---

## 10. GPU への含意 — 残された路は高次元だけ、しかし依然 bet

arc は CPU の路を全部閉じました。実 proxy は noise-free で滑らか (IV)、最後の候補 (kernel 多様化) は構造的に閉じた (V)。③の残された路は **高次元の地形のみ** ── それを提供するのが **full-LLM のパラメータ/損失空間 (数百万次元)** です。

構造的洞察は GPU の賭けを **better-motivated** にします。「full-LLM だけが例外かも」という盲目的な賭けではなく、「**③ は高次元を要し、full-LLM が高次元域**」という原理に沿う賭けになる。

**ただし依然 bet**。生物学の Cit+ が「③ アルゴリズムの勝利」を証明しないのと同じ理由、そして BG9 で RR に勝てなかったのと同型の理由で ── **実 LLM 地形が backprop (勾配降下) という強 baseline で直接ナビゲートできるなら、③はやはり不要**。難所が高次元なのは **必要条件であって十分条件ではない**。「強い直接法が解けない」ことを追加で示す必要がある (CPU では RR、GPU では勾配降下)。

だから GPU は「③のため単独」でなく **ポートフォリオ判断** (llive の実 LLM fitness 等と相乗り) + **クラウド借りで事前登録 1 本** (資本コミット前) が適正。go/no-go 基準も falsifiable に書けます:

> **full-LLM の難所は behavior で高次元か、かつ強い直接 baseline (勾配降下) で到達困難か?** 高次元でも勾配が直接届くなら③不要 (= BG9 の RR 結果の GPU 版)。

---

## 11. メタ教訓 — 正直さは、勝つための道具だった

この arc の本当の成果は数値ではなく、**「整いすぎた結果を疑う」精神が実際に研究を前へ進めた**ことです。

- **存在証明 (I)** で勝ったとき、谷を消した境界実験で「③は万能ではない」を自分から確かめた (勝ちを過大評価しない)。
- **汎化 (III)** でペアレビューが 3 つの rerun ブロッカーを突きつけたが、直しても結論は変わらなかった (脆い negative ではないと確認)。
- **決定論測定 (IV)** で評価ノイズを物理的に消したから、「滑らか」が地形の性質か計器の限界かを切り分けられた。
- **BG9 (V)** では敵対検証で自分の「③が立たない」を**反証しようとして反証できず**、構造として確証された (negative を正しく negative と確定する方向でも同じ規律が効いた)。

さらに arc 全体で 1 つ学んだのは ── **低次元の難所は強 baseline が直接解いてしまう。だから③ (選り分けて育てる工夫) が効くには "高次元 behavior 空間" が要る**。「だまし地形を作れば③が立つ」は半分しか正しくなくて、正確には「**直接サンプルできないほど高次元な**だまし地形」でないと③は立たない。そして驚いたことに、この境界条件は **ライトのシフティング・バランスとコイン批判が 100 年近く前に到達していた**ものでした。

「異常に良い結果が出たら、勝った気になる前に必ず内訳を疑う」── FullSense の研究規律 (`honest disclosure`) は、ただの自戒ではなく、**実際に偽陽性を捕まえ、negative を正しく確定し、研究の精度を上げる機構**として 6 段全部で回っていました。

結論を、最後にもう一度、正確に。

> **③ が活きるのは「高次元の」だまし地形のときだけ**。存在証明 (合成 corridor) では圧勝したが、実 CPU 基質は ── 記憶タスク (床/天井) も、多タスク汎化 (滑らか) も、実 proxy テキスト地形 (noise-free で滑らか) も、kernel 多様化 (低次元・構造的に閉) も ── どれもその条件を満たさなかった。**「③ 決着 = ③ は不要と判明」ではなく**、「③ が活きる条件 (高次元のだまし地形) を、今 CPU で測れた実物もどきは満たさなかった」。本丸 (GPU 高次元) はまだ先で、しかも「強い直接 baseline が解く」リスクを抱えた賭けです。そしてこの結論の骨格は、20 世紀の進化生物学が既に描いていました ── ただし生物学はそれを **証明するのでなく、接地するだけ**です。

---

**Tags**: 進化計算 / MAP-Elites / 統計検定 / honest disclosure / 進化生物学 / CPU 研究
**関連**: 連載 #33 (第三軸 ③ 決着 Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (反証・Goodhart・proxy 限界)
**Project**: llcore (PyPI 予約 llmesh-llcore、リポジトリ未公開のためローカル研究)

---

# English

# (Series #34) What Six Rounds of Hill-Climbing Taught Us About "When Does Evolution's ③ Actually Matter" — and How Evolutionary Biology Reached the Same Answer 100 Years Ago

## TL;DR

- The question is **"When you search for an AI's core computation by evolution, do you really need the 'sort-and-rear-separately' trick (= evolution's ③: survival of the fittest / separation)?"** Series #33 wrote up the endgame (Step D + BG9); **this #34 surveys the whole arc (6 stages) as a single story**.
- **Stage 1 (synthetic deceptive landscape)**: ③ wins decisively (Cliff δ=+1.0). ③ is a real mechanism = **existence proof**.
- **Stage 2 (memory task / multi-reservoir)**: blocked by the substrate's "floor" and "ceiling," so ③ could not be measured = **N/A**.
- **Stage 3 (multi-task generalization)**: ③ beats "no selection," but cannot beat simple selection or random = ③ unnecessary (honest negative).
- **Stage 4 (measure a real proxy landscape noise-free)**: once we physically drove evaluation noise to zero, the landscape was **genuinely smooth (unimodal)** = ③-unnecessary confirmed. For the first time, "the past negatives were not lack of statistical power but a smooth landscape" was backed up.
- **Stage 5 (BG9: the loophole of mixing 4 component kinds)**: kernel selection is **low-dimensional**, so a strong baseline (random-restart hill-climbing) samples it directly, and ③'s niching advantage **structurally** does not appear = the loophole is closed.
- **Structural insight (the core of this arc)**: ③ only helps when the hard spot lies in a **high-dimensional behavior space** that cannot be sampled directly. The real CPU substrate is low-dimensional/smooth, so ③ is unnecessary.
- **Biological grounding (verified)**: this is exactly Wright's **shifting-balance theory**. For **the melanic moth (single gene = low-dimensional)**, ordinary selection suffices (= the BG9 kernel case); for **Lenski's Cit+ (high-dimensional, history-dependent)**, diversity matters (= the ③ regime). Our negative is **the computational version of the Coyne critique** (real landscapes are simple and ③ is only rarely decisive).
- **Meta-lesson**: "a result that went too well is not a victory but an alarm." Pre-registration, honest disclosure, adversarial verification, and deterministic noise-free measurement kept us from premature celebration.

> ⚠ Every number in this article is an actual measurement tied to local (on-machine) research records. llcore does not yet have a public repository, so I cannot link out. Instead I write "how it was measured" in the body. The papers cited in the biology part are only those whose existence, attribution, and claimed content I separately cross-checked against primary sources.

---

## 0. What this article is about (the concept)

`llcore` is a CPU-complete research framework that "turns a Transformer's core computation (state-update rule, learning rule, cognitive-drive Δ) into a genome and evolves it while verifying with Z3 that it doesn't break."

Its evolution engine has a design crux: of the 4 elements of evolution (① mutation / ② heredity / ③ survival of the fittest / separation / ④ overproduction), how should **③ (selection / separation)** be made to take effect? It is the "sort and rear separately" mechanism — like MAP-Elites, which preserves diversity and keeps things in niches.

The question is simple.

> **Is that ③ really needed?**

If it is, then the heavy investment to carry ③ (ultimately running a real LLM on GPU) is meaningful. If it is not, then clinging to ③ is a waste of time and electricity.

Series #33 wrote up in detail the **endgame** of that question (the deterministic measurement of Step D + the structural resolution of BG9). But to get there, there were **6 stages of experiments**, repeatedly winning (existence proof), failing to measure (N/A), and losing (honest negative). This #34 re-lays out **the whole arc as a single story**. And as the highlight this time, we **ground** — with verified primary sources — the fact that **this computational result has a strikingly identical shape to a roughly 100-year-old debate in evolutionary biology (Wright vs. Fisher)**.

— That was 40 seconds. Warm-up done. On to the main topic. —

---

## 1. Metaphor: hill-climbing, the deceptive landscape, and the memory palace

Before the equations, let's grasp the big picture with the 3 metaphors used consistently throughout this research.

We represent the quality of a design as **the height of a landscape**. **High place = good design**. It's a game of finding the highest peak.

**Landscape 1: a smooth single mountain (easy)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

In such a landscape, plain "hill-climbing" — that is, "just move toward something slightly better than now" — is enough to reach the top. **The fancy trick (③) is not needed.**

**Landscape 2: the deceptive landscape (deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

Here, plain hill-climbing stops at the false peak, because it lacks the courage to descend into the valley.

This is where ③'s idea works. **You keep all sorts of climbers scattered around the valley** (= the memory palace / MAP-Elites archive). Someone can cross the valley by "stepping-stones" and reach the real peak — that's the mechanism.

**The heart of this research in one line**: ③ is truly useful **only in the "deceptive landscape."** On a smooth single mountain, ③ is a white elephant.

So the question can be rephrased like this.

> **"When you design an AI by evolution, is the landscape you actually run into a 'deceptive landscape,' or a 'smooth single mountain'?"**

In #33 we settled this question with Step D + BG9. In this #34 we show **all 6 stages of hill-climbing** that led there. The interesting part is that at each stage, "was it a deceptive landscape / was it smooth / could it even be measured" changes.

— A short break. That's the prep. From here, the full record of the 6-round series. —

---

## 2. The whole-arc map — surveying the 6 stages of hill-climbing at a glance

Let me put out the map first. This is the backbone of this article.

| Stage | Substrate (what landscape was measured) | Did ③ work? | One line |
|---|---|---|---|
| **I (Step 4)** | a synthesized "deceptive landscape" (deceptive corridor) | **Yes (decisive)** | Existence proof. ③ is real |
| **II (Step C / ladder 1)** | memory task / multi-reservoir parity | **N/A** | Couldn't measure due to floor, ceiling, the degree-5 wall |
| **III (E-A)** | multi-task generalization | **No** | ③ beats "no selection," but no more than that |
| **IV (Step D)** | real-proxy text landscape (deterministic measurement) | **No** | The landscape is confirmed **genuinely smooth** (noise-free) |
| **V (BG9)** | union of 4 component (kernel) kinds | **No** | **Structurally** closed (low-dimensional selection) |

The storyline is this. **First we prove existence — "③ is real and wins decisively under the right conditions" (I); next, to ask "well, what about real problems," we went to measure across 4 stages (II–V), and every single time it was "the real CPU substrate is a landscape that doesn't need ③."** Moreover, at the very end (IV, V), it was confirmed that the "reason it's not needed" is **the nature of the landscape, not lack of statistical power** — that is the whole-arc arc.

So, one stage at a time.

---

## 3. Stage I (Step 4) — existence proof: in a deceptive landscape, ③ wins decisively

The first thing we did was an existence proof of "does a scene where ③ **works as the theory says** actually exist?" We **deliberately built a deceptive landscape** and pitted ③ (MAP-Elites) against 3 baselines — pure random / panmictic GA / **random-restart hill-climbing** — in a contest.

**The landscape's construction**: the genome is 24-dimensional. We define behavior (the climber's type) as `mean(genome)` = the average of the 24 values. To raise behavior, you have to **raise all 24 dimensions simultaneously**. The fitness is exactly a deceptive landscape: "a false peak (value 0.6) at behavior≈0.4 → a valley (value≈0) at behavior≈0.65 → the real peak (value 1.0) at behavior≈0.9."

**Results**:

| Method | Reach rate to the real peak | Comparison with ③ |
|---|---|---|
| **MAP-Elites (③)** | **about 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | same as above |
| random-restart hill-climbing | 0% | same as above |

Only ③ reached the real peak; all 3 baselines stopped at the false peak (≈0.60). **100% wins / the effect size is the theoretical maximum (δ=+1.0)**. Robust across 3 base seeds (60 seeds total).

Why this happens becomes foreshadowing for later.

- **random** always has behavior concentrated at ≈0.5 (the average of 24 values is locked at 0.5 by the central limit theorem). So it can **never reach** behavior 0.9 (0% even after drawing 6000 samples).
- **hill-climbing** climbs to the false peak 0.6 and refuses the one move of descending into the valley. Even on restart it returns to behavior≈0.5 and falls into the same trap.
- **③ (MAP-Elites)** keeps the valley cells as "new behavioral niches" and **crosses behavior 0.5 → 0.9 by stepping-stones**.

**We measured the boundary honestly too**. In a smooth corridor with the valley removed, ③ can no longer beat hill-climbing (p≈0.29). **③ is not omnipotent; it only works in a deceptive landscape.**

**Honest caveat**: this is a **deliberately built** synthetic landscape. It only proves that ③ is "possible," not that real tasks have this structure. Toy scale, low noise, and the baseline is a plain (1+1).

→ Here a hypothesis arises: **"If the real-problem landscape is this deceptive, ③ should come alive."** The next 4 stages are a journey to verify that on substrates closer to real problems.

— A pause. Stage I was a satisfying decisive win. From here, the weather turns... —

---

## 4. Stage II (Step C / ladder 1) — blocked by the substrate's "floor" and "ceiling" (N/A)

Next we investigated "does a deceptive corridor **naturally arise in standard memory tasks**?" (Step C). We ran delayed parity / flip-flop / delayed recall with a single leaky reservoir + ridge readout.

The result was a clean **N/A (unmeasurable)**. The reasons are interesting because they're at two extremes.

- **delayed parity = floor**: a single reservoir cannot compute XOR (Minsky-Papert). All methods give R²≈0.003. No one can climb, so ③ cannot be separated.
- **flip_flop = ceiling**: all methods saturate at R²≈0.95. Variance is crushed and ③'s difference doesn't show (③ vs random has a positive sign but p=0.15 = underpowered, so it is **not a null**).

Here is one important finding. **The multimodality of the genome space was high** (valley fraction was 1.000 for parity), yet it was no use to ③. In other words, **"multimodal in genome space" ≠ "a deceptive landscape whose behavior must be crossed."** This distinction becomes the key for the second half of the arc.

**Ladder 1 (multi-reservoir)**: so, if we chain multiple reservoirs, does the floor rise? → We tried 5 mechanisms and all were `floor_lifted = false`. Depth (DeepESN) raises the floor statistically (effect +0.47/+0.60, PASS), but the absolute value stops at R² 0.05-0.10. The clincher is a positive control: a degree-2 readout solves 2-bit XOR exactly (R²=+1.0) but breaks down at degree≥3. **5-bit parity is degree-5 = a structural wall of this CPU reservoir+ridge paradigm.**

→ The parity path is structurally blocked. The real test of ③ needs to **come down off parity**.

**Honest caveat**: the degree-5 wall is "a wall of this setting," not a proof of impossibility for the whole paradigm.

— A short break. A "couldn't measure" result is plain, but in drawing the map it's an important blank zone. —

---

## 5. Stage III (E-A) — multi-task generalization: ③ wasn't needed (honest negative)

Coming down off the parity floor, we measured ③ on **generalization**, with the cleanest ablation we could assemble.

**Setup**: single-layer leaky reservoir + ridge. Recall with variable delay. **Train on short delays {15, 30}, test on long delays {45, 60}** (extrapolation). The comparison is MAP-Elites (full ①②③) vs. **MAP-Elites with selection removed** (`randselect`: choose parents at random and place unconditionally = mutation only) + panmictic GA + random.

**Results (after peer review)**:

| Method | Test generalization R² (mean±std) |
|---|---|
| MAP-E (full ①②③) | 0.682 ± 0.115 |
| MAP-E randselect (selection removed) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| Gate | Comparison | diff | p (one-sided) | Verdict |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**How to read it**: ③ beats the **drift control with selection removed** (C-gen3 PASS = "some selection beats no selection"). But it **cannot beat panmictic GA (which has selection but no niching)** (it even loses slightly), nor random. In other words, **there is no niching-specific (= ③'s intrinsic) contribution**. This generalization landscape was **smooth** enough that simple selection or even random arrives at the same place. This is consistent with Stage I's boundary, "if it's smooth, ③ doesn't work."

**Honest caveat (important)**: this verdict is **limited to this setting** (budget 400, grid 6×6). Furthermore — and here is the crux of honest methodology — peer review (Codex) initially judged it "untrustworthy" and forced 3 rerun blockers (independent seeding per replicate / adopting the global best within budget / raising honest_n from 16→30). **Even after the fixes, the conclusion did not change.** The takeaway is that it was not a "fragile negative that flips when fixed."

— A pause. A loss is a loss, but the work of confirming we "lost correctly" took more time. —

---

## 6. Stage IV (Step D) — the real-proxy landscape is confirmed "genuinely smooth" (noise-free)

This is the turning point of the arc. Through Stage III, "③ negative" kept happening, but a **nagging doubt** lingered the whole time.

> Is "③ unnecessary" really because **the landscape is smooth**? Or was it merely **lack of sample size, so the difference couldn't be detected (underpower)**?

Mistake this and you'd over-generalize to "③ is powerless." Step D settles it here.

**The trick**: an ESN reservoir (fixed seed) + a closed-form ridge readout (`np.linalg.solve`) **draws no random numbers at all**. So we can physically zero out evaluation noise down to **machine epsilon (about 1.11e-16)**. We measured `eval_noise_std ≤ 1.11e-16` — this comes from the smallest unit of floating point (ULP) and is **effectively zero**. With the fog of noise completely cleared, we can measure the landscape's valleys directly.

The landscape is next-character prediction of llcore's own source (about 24k characters). We measured valley_fraction (the fraction of valleys; ≥0.2 means multimodal = deceptive landscape).

| Landscape | Dims | valley_fraction (mean/max) | Multimodal? | Verdict |
|---|---|---|---|---|
| **ESN 3-param** (real proxy) | 3 | **0.000 / 0.000** | No (3 seeds agree) | Smooth → ③-unnecessary confirmed noise-free |
| **ESN per-neuron** (real proxy) | 40 | **0.096 / 0.121** | No (3 seeds agree) | Smooth-ish → ③ unnecessary |
| multimodal control (positive) | 3 / 40 | 0.70 / 0.80 | Yes | The diagnostic can detect multimodality ✓ |
| quadratic control (negative) | 3 / 40 | 0.000 | No | The diagnostic can detect smoothness ✓ |

There are 2 points.

1. **The real-proxy landscape (both 3-dim and 40-dim) is unimodal**. Agreement across 3 seeds.
2. **The diagnostic itself is sound**. A deliberately built multimodal landscape is properly detected as multimodal, and a quadratic is properly detected as smooth. So "the real proxy is unimodal" is not an instrument bug but **the nature of the landscape**.

→ For the first time, **"the past ③ negatives were not underpower; the landscape was genuinely smooth"** was backed up on a real substrate, noise-free. Re-measure and no multimodality appears.

**Honest caveat (important)**: "smooth" is precise only near the threshold. **90.9% of the midpoints of ESN 3-param dip slightly downward**, and the maximum relative dip (0.0435) is just below the valley threshold of 0.05. Strictly, it is not "**truly unimodal**" but a "**weak multi-basin with shallow valleys (~2-4%) just below the threshold**." The direction holds, but the robustness is limited because it's near the threshold — not rounding this off to "a perfect convex bowl" is this time's discipline.

— A deep breath. Here, "the real-thing-mimic is smooth" is confirmed. What remains is "the last CPU loophole." —

---

## 7. Stage V (BG9) — the loophole of mixing components was structurally closed

Since the real proxy is confirmed smooth, chasing ③ in a smooth landscape yields no gain. But GPU is an investment decision, so we tried **a different hypothesis we could advance on CPU**. That is **kernel diversification (BG9)**.

**Hypothesis (pre-registered H7)**: even if each individual kernel (rwkv / mamba / hopfield / linear_attn) is smooth, **when you union the 4 kinds, the moment of kernel switching creates fitness steps → multi-basin (deceptive landscape) → ③ stands up on CPU without GPU**. The pre-registered honest prior leaned **toward null** (since all CPU substrates so far were smooth).

The result in 3 parts.

**(1) substrate validity — there is discrimination but it's weak (PASS but caution)**: when we measure whether the best kernel differs per task, the mapping is non-constant = non-inert (PASS). mamba is best on selective-copy, linear_attn on weighted-accumulation. However, **hopfield could not win on any task** (dysfunctional with the diagonal-scalar mock), so it is effectively a "**3-kernel** union." **The existence of discrimination ≠ a multimodal barrier.**

**(2) harness validity — the positive control does not validate (the clincher)**: on a synthetic kernel-barrier, compare ③ against 3 baselines.

| Substrate | Result |
|---|---|
| **positive control** | ③ crushes panmictic (+0.423) and random (+0.208). **But it cannot beat RR (random-restart hill-climbing)** (+0.051, p=0.31 → FAIL). It falls short of beating all 3 baselines = the harness doesn't stand |
| **negative control** | all methods saturate, no ③ advantage = correctly null (the instrument is sound) |
| **real** smoke | ③ beaten 0/3, panmictic actually exceeds ③ |

In Stage I's corridor, ③ could shut out RR; **why can't it in kernel space?** The root cause is one.

> **RR can sample kernel_id ∈ [0,4) directly at every restart.** Kernel selection is a single coordinate over 4 discrete values (**low-dimensional**), so RR hits all 4 kernels directly on restart. There's no need to cross a valley to "find the best kernel" = **direct warp**. So ③'s behavioral niching has no turn to play.

The reason ③ could shut out RR in Stage I is that there, behavior was `mean(24 dims)`, the average concentrates at 0.5 → the global peak is in a measure-zero region = **high-dimensional, not directly samplable**. kernel_id, conversely, is low-dimensional and can be sampled directly.

**(3) red-team — even adversarial verification couldn't refute it, and rather confirmed it**: on the positive control, instrumented RR spread restart kernels nearly uniformly across the 4 basins as [12,18,16,18], reaching target 88% of the time. In all 4 faithful configurations (high-dimensional theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin), ③ cannot beat RR. Tightening the corridor makes ③ **starve first** (D=3: ③ reach 0.08 vs RR 0.42). We quantitatively confirmed **"the behavior dimension along which RR alone is excluded and ③ gets through does not structurally exist in kernel space."**

**Verdict**: formally N/A (the positive control does not validate), but in substance a **decisive structural negative**. The harness is sound (it correctly nulls the negative control and detects GA/random), yet the substrate **cannot host ③'s deceptive landscape in the first place**. The answer to the question left from Stage I, "if we expand the search space with kernel diversification, does ③ unlock?", is **NO (structurally, on CPU)**.

**Honest caveat (important)**: this is **not "③ turned out to be unnecessary."** It is "③ cannot in principle be separated from a strong baseline in low-dimensional kernel space" = **an informative N/A**. ③'s mechanism itself is already confirmed real in Stage I. The substrate is weak (effectively 3 kernels; hopfield is a diagonal mock). A stronger kernel implementation could in theory yield a different conclusion, but **the structural barrier (low-dimensional selection → RR direct sampling) is independent of the quality of the kernel implementation**.

---

## 8. Structural insight — uniting the 6 stages under a single condition

The existence proof (I) and the 4 negatives (II–V) all connect under just one condition.

> **③ (behavioral niching) exceeds a strong baseline only when the "hard spot" lies in a high-dimensional behavior space and cannot be reached by direct sampling (random restart).**

- **Why Stage I satisfies it**: behavior = `mean(24 dims)`. The average concentrates at 0.5 by the central limit theorem, and the global peak (mean≈0.9) is effectively measure-zero. Neither random nor restart **reaches it directly**. So ③, which leaves stepping-stones and ratchets, is essential.
- **Why the real CPU substrate doesn't satisfy it**: the hard spot is low-dimensional. The control coordinate of the ESN text proxy is effectively leak rate (a smooth low-dimensional knob; there's no valley to begin with). The hard spot of the kernel union is "which kernel" = a single discrete choice among 4. RR samples directly and teleports to all basins, so there's no valley to cross.

So Stage II's "multimodality of genome space 1.000" is not a sufficient condition — even if the genome is riddled with valleys, if the hard spot is concentrated in low-dimensional behavior coordinates, restart reaches it directly. **What matters is "the dimension of the behavior the search must reach," not the dimension of the genome.**

---

## 9. Biological grounding — evolutionary biology gave the same answer 100 years ago

From here is the highlight of #34. **"Diversity-preserving selection works only under narrow conditions and is redundant otherwise"** — this boundary condition has a strangely clean precedent in 20th-century evolutionary biology.

> ⚠ **Honesty contract**: the following biology is a **"metaphor (structural analogy)," not a proof of our computational result**. The correspondence is structural and does not match at the mechanism level. Wherever the analogy slips, I note it on the spot. The papers cited are only those whose existence, attribution, and claimed content I separately cross-checked against primary sources.

### 9.1 Wright's shifting-balance theory = the precedent of ③

Sewall Wright (1931/1932) reasoned as follows. If you stay as one big "single herd (panmictic population)," ordinary natural selection **gets trapped on the local peak right in front of you**. To go to a higher mountain you must once **lower mean fitness and cross the valley**, but deterministic selection refuses that.

Wright's solution was **to split the herd into many semi-isolated sub-populations (demes)**.

- **Phase I**: a small deme crosses the valley by chance, descending via **genetic drift**.
- **Phase II**: there, ordinary selection within the deme climbs a new (higher) peak.
- **Phase III**: the deme that landed on the high peak sends out many migrants, and the superior gene combination spreads through the whole species.

As a **whole** metapopulation, it crosses a valley that a single converged population cannot — this is the biological version of "crossing the valley of the deceptive landscape by stepping-stones."

**Correspondence to ③ / MAP-Elites (= metaphor, not attribution)**: each cell of the archive = a semi-isolated deme, local elitism within a cell = within-deme selection (Phase II), cross-cell mutation = interdeme diffusion (Phase III), and **the archive as a whole** (≒ metapopulation, not a single cell) crosses the valley.

> **Honesty notes (2 points)**:
> 1. **This is a commentator's framework, neither Wright's claim nor MAP-Elites's origin.** The original MAP-Elites paper (Mouret & Clune 2015) and the QD literature **do not cite Wright or "shifting balance."** I raise Wright as our **inspiration / metaphor**, not as the lineage of MAP-Elites.
> 2. **The mechanisms are only structurally similar, not identical.** MAP-Elites's valley crossing happens because a **mutation operator** places offspring in a new cell, **not genetic drift**. The archive is also not a population of replicating cells.

### 9.2 Wright vs. Fisher = the dimension (the shape of the landscape) axis

Wright's contemporary Fisher (R. A. Fisher, 1930) argued the opposite: **a large panmictic population + mass selection on additive variance is enough** for adaptation to proceed; there's no need to bother splitting it.

The two's **deepest point of conflict was actually "epistasis (gene-gene interaction) and the shape of the landscape."** Wright assumed "because of non-additive interaction the landscape is **bumpy and multimodal**, so drift to cross valleys is needed," and Fisher judged "interactions exist but are unimportant, the landscape is roughly **unimodal and smoothly climbable**, so mass selection suffices."

**This epistasis/ruggedness axis is exactly the dimension in which our result lives. The shape of the landscape (topology) is the whole problem.** If the landscape is genuinely bumpy and high-dimensional (the Wright regime), diversity ferries you across valleys; if it's smooth or the hard spot is low-dimensional (the Fisher regime), mass selection — i.e., the biological version of strong random-restart hill-climbing — already suffices. Our ESN text proxy is noise-free and smooth, and the hard spot of the kernel union is low-dimensional discrete. **Both are the Fisher regime**, and ③ doesn't work and didn't work.

> Fine print (honestly): "Fisher ignored drift" is a compressed popular myth. Precisely, "he acknowledged drift exists but judged it quantitatively negligible in large populations." It's not a total denial.

### 9.3 Our negative = the computational version of the Coyne critique

The most telling correspondence is not Wright's **proposal** but the biology community's **empirical verdict**. Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) evaluated shifting-balance theory both theoretically and empirically, and concluded as follows (full text cross-checked).

- **Mass selection is usually enough.** "There are almost no real examples better explained by Wright's three-phase mechanism than by simple mass selection." Artificial-selection experiments also failed to show that "selection in subdivided populations produces a greater response than mass selection in a large population."
- **Shifting balance works only under limited, rare conditions.** Empirical estimates of population structure suggest "**drift can move populations only between peaks separated by shallow valleys**" (deep valleys are only rarely crossed by drift), and moreover **most adaptation does not require valley crossing**.

This is a **strikingly precise biological version** of our result. Translated into our vocabulary, their words become: **if the landscape isn't genuinely deceptive/high-dimensional, ordinary mass selection (≒ strong random-restart hill-climbing) already solves it, and the diversity-maintaining apparatus buys almost nothing.** "Real valleys are usually shallow, most adaptation needs no valley crossing" is the biological statement of our "**real landscapes are usually simple, so niching is redundant**."

> **Honesty notes (3 points)**:
> 1. **They did not "refute" shifting balance.** They explicitly state Phase I/II can happen and cite 6 empirical cases. The claim is **narrower and probabilistic** ("hard to call it a general, important mechanism"), and writing "refuted" overstates it.
> 2. **The debate is not yet settled.** Wade & Goodnight (1998) and Peck et al. (1998, whose title literally argues "feasible") rebutted it, followed by Coyne et al.'s 2000 counter-rebuttal and Goodnight & Wade's rebuttal in the same issue. You must not cite the 1997 critique as the "final conclusion."
> 3. **Biology has a mechanism with no counterpart on the computational side, and it makes a claim even stronger than ours.** In Phase III, the gene-flow barrier that protects diversity can **trap a good solution in peripheral demes and impede its spread** = niching can be **counterproductive**. Our stateless discrete-selection setting has no counterpart to this cost, so we **don't overlay** it here. This is a spot where biology makes a stronger claim.

### 9.4 Two real examples — the low-dimensional moth and the high-dimensional E. coli

Our claim has two poles (low-dimensional = ③ unnecessary / high-dimensional = ③ can work), and evolutionary biology has a clean real example for each.

**The low-dimensional pole — industrial melanism of the peppered moth (= the BG9 kernel case)**: in *Biston betularia*, carbonaria (black) vs. typica (white) are governed by **a single Mendelian locus, few alleles** (the causal variant is a transposable-element insertion into the cortex gene; van't Hof et al. 2011/2016) under **strong directional selection** (s ≈ 0.1-0.2; Saccheri et al. 2008; predation reconfirmed in Cook, Grant, Saccheri & Mallet 2012). The optimum is unimodal at each moment, merely shifting with the environment. **Simple directional selection — the biological version of greedy hill-climbing / random restart — directly fixes the fitter morph, and a diversity-maintenance mechanism is neither needed nor invoked.** This is exactly BG9: kernel selection is a low-dimensional single coordinate of 4 choices, RR samples all kernels directly, and ③ cannot structurally separate. **The melanic morph = the living-organism version of the BG9 kernel case.**

> Note (honestly): polymorphism is temporarily maintained during the transition, but that is due to **spatial environmental heterogeneity + gene flow (migration-selection balance)**, not an intrinsic diversity-preservation mechanism. A spot where the analogy slips slightly.

**The high-dimensional, history-dependent pole — Lenski's Cit+ (= the ③ regime)**: in the E. coli Long-Term Evolution Experiment (LTEE), aerobic citrate utilization (Cit+) evolved in **exactly 1 of 12 populations** around generation 31,500 (Blount, Borland & Lenski 2008). The key is a high-dimensional, history-dependent path of ordered **potentiation (accumulation of precursor mutations) → actualization (promoter capture via tandem duplication of citT) → refinement** (Blount et al. 2012). Replay experiments distinguished "historical contingency" from "a constant rate of rare mutation." This **genuinely exemplifies** the value of exploring contingency, epistasis, and a high-dimensional bumpy landscape — a real example of a regime where ③ can work.

> **Honesty notes (this corresponds only to the "antecedent" of our conditional)**:
> - **LTEE uses no niching algorithm.** It's plain natural selection, and the 12 parallel populations are **themselves a random-restart-like design**. So it's an existence proof that "contingency + diversity enables a rare innovation," **not** evidence that "niching beats a strong restart baseline."
> - "E. coli acquired the power to eat citrate from scratch" is a popular exaggeration. The innovation is **regulatory (aerobic expression of an existing transporter) = exaptation**, neither a new gene nor new biochemistry.
> - Van Hofwegen et al. (2016) showed "with direct selection Cit+ appears much faster" and challenged the "rare/contingent" framing (the Lenski side rebutted that it doesn't contradict the potentiation under LTEE conditions). If you lean on the "extremely rare / long-delay" narrative, you should also note this **contested follow-up**.

### 9.5 Grounding summary

| Pole | Biology | Landscape | Does ③ work? | Our substrate |
|---|---|---|---|---|
| low-dim/smooth | melanic morph (single locus, s≈0.1-0.2, directional) | unimodal, shifting | **No** — mass selection suffices | BG9 kernel union; ESN/ridge text proxy (deterministic, smooth) |
| high-dim/contingent | Lenski Cit+ (potentiation→actualization→refinement) | bumpy, valley crossing by mutation | **Yes** (a regime where it can work) | synthetic deceptive corridor (behavior = average of 24 dims) |
| empirical verdict | Coyne, Barton & Turelli: mass selection usually suffices, shifting balance is only rarely decisive | real landscapes are usually simple | the **mirror** of our negative | every CPU substrate we tried |

**Conclusion**: Wright's shifting balance is the correct biological precedent for "**why** ③ works when it works," the Wright-Fisher epistasis/ruggedness axis is the correct framework for the "**dimension** condition," the melanic moth and Lenski Cit+ are clean low-/high-dimensional poles, and the Coyne critique is the biological precedent of our **negative**. **But these do not prove the computational result. They only ground it.** Where the analogy loosens most is that biology adds a cost (the gene-flow trap of Phase III) — our stateless setting has none.

— A pause. When I realized a 100-year-old debate had the same shape, honestly I got chills. But not mistaking "got chills" for "proof" is this time's discipline. —

---

## 10. Implications for GPU — the only path left is high-dimensional, yet still a bet

The arc closed every CPU path. The real proxy is noise-free and smooth (IV), and the last candidate (kernel diversification) is structurally closed (V). The only path left for ③ is **a high-dimensional landscape** — and what provides that is **the parameter/loss space of a full LLM (millions of dimensions)**.

The structural insight makes the GPU bet **better-motivated**. It's not the blind bet "maybe only full-LLM is the exception," but a bet that follows the principle "**③ requires high dimensions, and full-LLM is the high-dimensional regime**."

**But still a bet.** For the same reason that biology's Cit+ does not prove "a victory of the ③ algorithm," and by the same form as not beating RR in BG9 — **if the real LLM landscape can be navigated directly by a strong baseline of backprop (gradient descent), ③ is again unnecessary**. The hard spot being high-dimensional is **a necessary, not a sufficient, condition**. You additionally need to show "a strong direct method cannot solve it" (RR on CPU, gradient descent on GPU).

So GPU is appropriate **not "for ③ alone"** but as a **portfolio judgment** (riding along with llive's real-LLM fitness, etc.) + **one pre-registration on rented cloud** (before capital commitment). The go/no-go criterion can also be written falsifiably:

> **Is the full-LLM hard spot high-dimensional in behavior, AND hard to reach by a strong direct baseline (gradient descent)?** If high-dimensional but the gradient reaches directly, ③ is unnecessary (= the GPU version of BG9's RR result).

---

## 11. Meta-lesson — honesty was a tool for winning

The real achievement of this arc is not the numbers but **that the spirit of "doubting results that came out too neatly" actually pushed the research forward**.

- When we won at the **existence proof (I)**, we voluntarily confirmed "③ is not omnipotent" with a boundary experiment that removed the valley (not overrating the win).
- At **generalization (III)**, peer review thrust 3 rerun blockers at us, but even after fixing, the conclusion didn't change (confirmed it was not a fragile negative).
- At the **deterministic measurement (IV)**, because we physically erased evaluation noise, we could separate whether "smooth" was the nature of the landscape or the limit of the instrument.
- At **BG9 (V)**, in adversarial verification we **tried to refute and couldn't refute** our own "③ doesn't stand," and it was confirmed as structural (the same discipline worked in the direction of confirming a negative as correctly negative).

And across the whole arc we learned one thing — **a low-dimensional hard spot gets solved directly by a strong baseline. So for ③ (the sort-and-rear trick) to work, a "high-dimensional behavior space" is required.** "Build a deceptive landscape and ③ stands up" is only half right; precisely, ③ doesn't stand unless it's a deceptive landscape **so high-dimensional it can't be directly sampled**. And surprisingly, this boundary condition was one that **Wright's shifting balance and the Coyne critique had reached nearly 100 years ago**.

"When an abnormally good result comes out, always doubt the breakdown before you feel like you've won" — FullSense's research discipline (`honest disclosure`) was not mere self-admonition but a **mechanism that actually catches false positives, confirms negatives correctly, and raises the precision of the research**, turning across all 6 stages.

Let me state the conclusion precisely one more time, at the end.

> **③ comes alive only in a "high-dimensional" deceptive landscape.** It won decisively in the existence proof (synthetic corridor), but the real CPU substrate — the memory task (floor/ceiling), the multi-task generalization (smooth), the real-proxy text landscape (noise-free and smooth), the kernel diversification (low-dimensional, structurally closed) — none satisfied that condition. It is **not "③ resolved = ③ turned out unnecessary"** but "the real-thing-mimics we could measure on CPU now did not satisfy the condition (a high-dimensional deceptive landscape) under which ③ comes alive." The main keep (GPU high dimensions) is still ahead, and it's a bet that carries the risk that "a strong direct baseline solves it." And the skeleton of this conclusion had already been drawn by 20th-century evolutionary biology — except that biology does **not prove it, only grounds it**.

---

**Tags**: evolutionary computation / MAP-Elites / statistical testing / honest disclosure / evolutionary biology / CPU research
**Related**: Series #33 (third axis ③ resolution Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (refutation, Goodhart, proxy limits)
**Project**: llcore (PyPI reservation llmesh-llcore; local research as the repository is not yet public)

---

# 中文

# (连载 #34) 六连战爬山实验弄清了「进化的③何时起作用」——而且 100 年前的进化生物学早已给出同样的答案

## TL;DR

- 问题是 **「用进化去搜索 AI 的核心计算时,『分门别类、隔离培育的工夫』(= 进化的③:适者生存/分离) 到底需不需要」**。连载 #33 写了终局 (Step D + BG9);**而本篇 #34 把整段 arc (6 段) 当作一个故事来俯瞰**。
- **第 1 段 (合成欺骗地形)**:③ 大获全胜 (Cliff δ=+1.0)。③ 作为机制是真货 = **存在证明**。
- **第 2 段 (记忆任务 / 多 reservoir)**:被基质的「地板」与「天花板」所阻,无法测量③ = **N/A**。
- **第 3 段 (多任务泛化)**:③ 能赢「无选择」,但赢不了简单选择或 random = ③ 不需要 (honest negative)。
- **第 4 段 (对真实 proxy 地形做 noise-free 测量)**:把评估噪声物理性地降到零之后,地形 **确实是光滑的 (单峰)** = ③不需要被确证。「过去的 negative 不是检定力不足,而是地形本来就光滑」第一次得到佐证。
- **第 5 段 (混合 4 种部件的旁门左道 BG9)**:kernel 选择是 **低维**,因而强 baseline (随机重启爬山) 直接采样,③ 的 niching 优势 **在结构上**不出现 = 旁门左道被堵死。
- **结构性洞见 (本 arc 的核心)**:③ 起作用,只有当难点位于 **高维 behavior 空间**、无法直接采样时才行。真实 CPU 基质是低维/光滑的,所以③不需要。
- **生物学接地 (已验证)**:这恰恰就是赖特 (Wright) 的 **转移平衡说**。对 **黑化型蛾 (单基因 = 低维)**,普通的选择就足够 (= BG9 的 kernel 情形);对 **伦斯基的 Cit+ (高维、依赖历史)**,多样性才起作用 (= ③ regime)。我们的 negative 就是 **科因批判的计算版** (现实地形简单、③ 极少起决定性作用)。
- **元教训**:「太顺利的结果不是胜利,而是警报」。预先登记、honest disclosure、对抗式验证、确定性的 noise-free 测量,使我们避免了空欢喜。

> ⚠ 本文中的所有数值,都是与手头 (本地) 研究记录绑定的实测值。llcore 还没有建公开仓库,所以无法贴出外部链接。作为替代,我在正文里写了「是怎么测的」。生物学部分引用的论文,只列出那些已单独对照一次信息源、核实过其存在、归属与主张内容的。

---

## 0. 这篇文章在讲什么 (概念)

`llcore` 是一个 CPU 完整的研究框架,它「把 Transformer 的核心计算 (状态更新规则、学习规则、认知驱动 Δ) 当作基因,一边用 Z3 验证它不会坏掉,一边进化」。

它的进化引擎有一个设计上的要害:在进化的 4 要素 (① 变异 / ② 遗传 / ③ 适者生存・分离 / ④ 过剩繁殖) 之中,**③ (selection / separation)** 该如何发挥作用?这是像 MAP-Elites 那样、保持多样性并留在生态位里的「分门别类、隔离培育」机制。

问题很简单。

> **那个③,真的需要吗?**

如果需要,那么为承载③而做的重投资 (最终是在 GPU 上跑真 LLM) 就有意义。如果不需要,那么执着于③就是浪费时间与电费。

连载 #33 详细写了那个问题的 **终局** (Step D 的确定性测量 + BG9 的结构性了结)。但在抵达那里之前,有 **6 段实验**,反复地赢 (存在证明)、测不出来 (N/A)、输 (honest negative)。本篇 #34 把 **整段 arc 重新排成一个故事**。而且作为本次的看点,我们用已验证的一次信息源 **接地**:**这个计算结果与近 100 年前进化生物学的论争 (赖特 vs 费希尔) 在形状上惊人地相同**。

— 到这里 40 秒。热身完毕。进入正题。 —

---

## 1. 比喻:爬山、欺骗地形,与记忆宫殿

在公式之前,我们用本研究始终使用的 3 个比喻来把握全貌。

我们用 **地形的高度** 来表示设计的好坏。**高的地方 = 好的设计**。这是一场寻找最高峰的游戏。

**地形其一:光滑的单座山 (简单)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

在这样的地形里,朴素的「爬山法 (hill-climbing)」,也就是「只往比现在稍好一点的方向移动」,就足以登顶。**花哨的工夫 (③) 不需要。**

**地形其二:欺骗地形 (deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

这里,朴素的爬山会停在假峰,因为它没有下到谷里的勇气。

这时起作用的就是③的想法。**把各种各样的登山者散布留在谷的各处** (= 记忆宫殿 / MAP-Elites archive)。某个人能用「踏脚石 (stepping-stone)」渡过山谷、抵达真正的山顶——这就是机制。

**用一句话概括本研究的核心**:③ 真正有用,**只在「欺骗地形」时**。在光滑的单座山上,③ 是无用的大白象。

所以问题可以改写成这样。

> **「用进化来设计 AI 时,你实际遇到的地形是『欺骗地形』,还是『光滑的单座山』?」**

#33 中我们用 Step D + BG9 给这个问题作了了结。本篇 #34 展示通往那里的 **全部 6 段爬山**。有趣之处在于,每一段「是不是欺骗地形 / 是不是光滑 / 能不能测量」都会变化。

— 小憩。准备到此为止。从这里开始是六连战的实录。 —

---

## 2. 整段 arc 地图——一览 6 段爬山

先把地图拿出来。这是本文的脊梁。

| 段 | 基质 (测的是什么地形) | ③ 起作用了吗 | 一句话 |
|---|---|---|---|
| **I (Step 4)** | 合成的「欺骗地形」(欺骗 corridor) | **Yes (完胜)** | 存在证明。③ 是真货 |
| **II (Step C / 梯子1)** | 记忆任务 / 多 reservoir 奇偶 | **N/A** | 被地板、天花板、degree-5 之墙挡住,测不出来 |
| **III (E-A)** | 多任务泛化 | **No** | ③ 能赢「无选择」,仅此而已 |
| **IV (Step D)** | 真实 proxy 的文本地形 (确定性测量) | **No** | 确证地形 **确实光滑** (noise-free) |
| **V (BG9)** | 部件 (kernel) 4 种的并集 | **No** | **在结构上**被堵死 (低维选择) |

故事线是这样的。**首先证明存在——「③ 在条件合适时确实大获全胜,是真货」(I);接着,为了问「那么在真实问题里如何」,跨 4 段去测量 (II–V),结果每一次都是「真实 CPU 基质是不需要③的地形」**。而且在最后 (IV, V),确认了「不需要的理由」是 **地形的性质,而非检定力不足**——这就是整段 arc 的弧。

那么,一段一段来。

---

## 3. 第 I 段 (Step 4)——存在证明:若是欺骗地形,③ 会完胜

最先做的,是「**按理论该起作用的场面是否真实存在**」的存在证明。我们 **故意把地形做成欺骗式**,让③ (MAP-Elites) 与 3 个 baseline——pure random / panmictic GA / **随机重启爬山 (random-restart hill-climbing)**——对决。

**地形的构造**:基因是 24 维。把 behavior (登山者的类型) 定义为 `mean(基因)` = 24 个数的平均。要提高 behavior,就得 **同时把全部 24 维抬高**。fitness 恰恰是欺骗地形:「behavior≈0.4 处有假峰 (值 0.6) → behavior≈0.65 处有谷 (值≈0) → behavior≈0.9 处有真峰 (值 1.0)」。

**结果**:

| 方法 | 抵达真峰的比率 | 与 ③ 的比较 |
|---|---|---|
| **MAP-Elites (③)** | **约 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | 同上 |
| 随机重启爬山 | 0% | 同上 |

只有③抵达了真峰,3 个 baseline 全都停在假峰 (≈0.60)。**100% 胜 / 效应量为理论最大 (δ=+1.0)**。在 3 种 base seed (共 60 seed) 上稳健。

为什么会这样,会成为后文的伏笔。

- **random** 的 behavior 必然集中在 ≈0.5 (24 个数的平均被中心极限定理锁在 0.5)。所以它 **永远到不了** behavior 0.9 (抽 6000 个样本也是 0%)。
- **爬山** 爬到假峰 0.6,拒绝下到谷里那一手。即便重启也回到 behavior≈0.5,落入同样的陷阱。
- **③ (MAP-Elites)** 把谷的格子当作「新的 behavioral 生态位」保留,**用踏脚石把 behavior 从 0.5 渡到 0.9**。

**边界我们也诚实地测了**。在去掉谷的光滑 corridor 上,③ 已赢不了爬山 (p≈0.29)。**③ 不是万能的,它只在欺骗地形里起作用。**

**honest 保留**:这是 **故意做出来的** 合成地形。它只证明了③「可能」,并没有证明真实任务具备这种结构。toy 规模、低噪声、baseline 是朴素的 (1+1)。

→ 这里立起一个假设:**「如果真实问题的地形也这么欺骗,③ 应该能活起来」**。接下来的 4 段,就是在更接近真实问题的基质上去验证它的旅程。

— 歇一会儿。第 I 段是令人舒畅的完胜。从这里风云突变…… —

---

## 4. 第 II 段 (Step C / 梯子1)——被基质的「地板」与「天花板」所阻 (N/A)

接着我们调查「欺骗 corridor 会不会 **在标准的记忆任务里自然出现**」(Step C)。用 1 个 leaky reservoir + ridge readout 跑 delayed parity / flip-flop / delayed recall。

结果是干净的 **N/A (不可测)**。原因有趣在于两个极端。

- **delayed parity = 地板 (floor)**:单个 reservoir 算不出 XOR (Minsky-Papert)。所有方法都是 R²≈0.003。谁都登不上去,所以无法分离③。
- **flip_flop = 天花板 (ceiling)**:所有方法都饱和在 R²≈0.95。方差被压垮,③ 的差异显不出来 (③ vs random 符号为正但 p=0.15 = underpower,因此 **并非 null**)。

这里有一个重要发现。**基因空间的多峰性很高** (parity 的 valley fraction 是 1.000),却对③毫无用处。也就是说,**「在基因空间多峰」≠「需要跨越的 behavior 欺骗地形」**。这个区别成为 arc 后半的钥匙。

**梯子1 (多 reservoir)**:那么,把多个 reservoir 串起来,地板会不会抬高?→ 试了 5 种机制全是 `floor_lifted = false`。深度 (DeepESN) 在统计上抬高了地板 (效应 +0.47/+0.60, PASS),但绝对值止步于 R² 0.05-0.10。决定性的是 positive control:degree-2 readout 严格解出 2-bit XOR (R²=+1.0),但 degree≥3 即崩溃。**5-bit 奇偶是 degree-5 = 这个 CPU reservoir+ridge 范式的结构性之墙。**

→ 奇偶之路在结构上被堵死。③ 的正式检定需要 **从奇偶上下来**。

**honest 保留**:degree-5 之墙是「这个设置的墙」,不是对整个范式的不可能性证明。

— 小憩。「测不出来」的结果虽朴素,但在画地图时是重要的空白地带。 —

---

## 5. 第 III 段 (E-A)——多任务泛化:③ 不需要 (honest negative)

从奇偶的地板下来,我们用 **泛化 (generalization)** 来测③,组了一个最干净的 ablation。

**设置**:单层 leaky reservoir + ridge。可变延迟的 recall。**用短延迟 {15, 30} 训练,用长延迟 {45, 60} 测试** (外推)。比较的是 MAP-Elites (①②③全) vs **抽掉选择的 MAP-Elites** (`randselect`:随机选父代、无条件放置 = 只有变异) + panmictic GA + random。

**结果 (同行评审后)**:

| 方法 | 测试泛化 R² (平均±std) |
|---|---|
| MAP-E (①②③全) | 0.682 ± 0.115 |
| MAP-E randselect (抽掉选择) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| 门 | 比较 | diff | p (单侧) | 判定 |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**读法**:③ 赢了「**抽掉选择的漂移对照**」(C-gen3 PASS = "某种选择胜过无选择")。但 **赢不了 panmictic GA (有选择但无 niching)** (甚至略输),也赢不了 random。也就是说,**niching 特有 (= ③ 本来) 的贡献为零**。这个泛化地形足够 **光滑**,以至于简单选择或 random 也能到同一个地方。这与第 I 段的边界「光滑则③不起作用」一致。

**honest 保留 (重要)**:这个 verdict **仅限于这个设置** (预算 400, grid 6×6)。此外——这里是 honest methodology 的要害——同行评审 (Codex) 起初判定「不可信」,强制了 3 个 rerun blocker (每个 replicate 独立 seeding / 采用预算内的全局最优 / 把 honest_n 从 16→30)。**修正之后结论仍未改变。** 收获是:它不是「一改就翻的脆弱 negative」。

— 歇一会儿。输就是输,但确认我们「正确地输了」的工作更花时间。 —

---

## 6. 第 IV 段 (Step D)——真实 proxy 地形被确证为「确实光滑」(noise-free)

这里是 arc 的转折点。直到第 III 段,「③ negative」一直在持续,但始终有一个 **疙瘩** 残留着。

> 「③不需要」真的是因为 **地形光滑** 吗?还是仅仅 **样本数不够、检测不出差异 (underpower)** 呢?

弄错这一点,就会过度泛化为「③ 无力」。Step D 在这里作了了结。

**诀窍**:ESN reservoir (固定 seed) + ridge readout 的闭式解 (`np.linalg.solve`) **完全不抽随机数**。所以可以把评估噪声物理性地降到 **机器 epsilon (约 1.11e-16)**。实测确认了 `eval_noise_std ≤ 1.11e-16`——这源自浮点的最小单位 (ULP),**实质为零**。把噪声之雾完全拨开,就能直接测量地形的谷。

地形是 llcore 自身源码 (约 24k 字符) 的下一字符预测。我们测了 valley_fraction (谷的比例;≥0.2 即多峰 = 欺骗地形)。

| 地形 | 维数 | valley_fraction (mean/max) | 多峰? | 判定 |
|---|---|---|---|---|
| **ESN 3-param** (真实 proxy) | 3 | **0.000 / 0.000** | No (3 seed 一致) | 光滑 → noise-free 确证③不需要 |
| **ESN per-neuron** (真实 proxy) | 40 | **0.096 / 0.121** | No (3 seed 一致) | 偏光滑 → ③ 不需要 |
| 多峰 control (正) | 3 / 40 | 0.70 / 0.80 | Yes | 诊断器能检出多峰 ✓ |
| 二次函数 control (负) | 3 / 40 | 0.000 | No | 诊断器能检出光滑 ✓ |

要点有 2 个。

1. **真实 proxy 地形 (3 维 / 40 维均如此) 是单峰**。3 个 seed 一致。
2. **诊断器本身是健全的**。故意做的多峰被正确检出为多峰,二次函数被正确检出为光滑。所以「真实 proxy 是单峰」不是仪器的 bug,而是 **地形的性质**。

→ 这才第一次在真实 substrate 上 noise-free 地佐证了 **「过去的③ negative 不是 underpower,而是地形确实光滑」**。再测也不会出现多峰。

**honest 保留 (重要)**:「光滑」只在阈值附近才精确。**ESN 3-param 的 midpoint 有 90.9% 略微向下 dip**,最大相对 dip (0.0435) 就在谷阈值 0.05 的正下方。准确说,它不是「**真正单峰**」,而是「**带有略低于阈值的浅谷 (~2-4%) 的弱 multi-basin**」。方向得以维持,但因贴近阈值,稳健性有限——不把它圆成「完美的凸碗」,是本次的纪律。

— 深呼吸。到这里「仿真之物是光滑的」已确证。剩下的是「最后的 CPU 旁门左道」。 —

---

## 7. 第 V 段 (BG9)——混合部件的旁门左道,在结构上是堵死的

既然真实 proxy 已确证为光滑,在光滑地形里追③就不会出利得。但 GPU 是投资判断,所以我们试了 **能在 CPU 上前进的另一个假设**。那就是 **kernel 多样化 (BG9)**。

**假设 (预先登记 H7)**:即便单个 kernel (rwkv / mamba / hopfield / linear_attn) 各自光滑,**把 4 种并集起来,在 kernel 切换的瞬间 fitness 会形成台阶 → multi-basin (欺骗地形) → ③ 不靠 GPU 就在 CPU 上立得住**。预先登记的 honest prior 偏 **null** (因为迄今所有 CPU 基质都光滑)。

结果分 3 段。

**(1) substrate validity——有辨别但很弱 (PASS 但需注意)**:测量每个任务的拿手 kernel 是否不同,映射是非常数 = non-inert (PASS)。mamba 在 selective-copy、linear_attn 在 weighted-accumulation 上最佳。不过 **hopfield 在任何任务上都赢不了** (对角标量 mock 下功能失常),所以实质是「**3 kernel** 并集」。**辨别的存在 ≠ 多峰障壁。**

**(2) harness validity——positive control 无法 validate (决定性)**:在合成 kernel-barrier 上,把③与 3 baseline 比较。

| 基质 | 结果 |
|---|---|
| **positive control** | ③ 击溃 panmictic (+0.423)、random (+0.208)。**但赢不了 RR (随机重启爬山)** (+0.051, p=0.31 → FAIL)。未能全胜 3 baseline = harness 立不住 |
| **negative control** | 全部 method 饱和,③ 无优势 = 正确地 null (仪器健全) |
| **real** smoke | ③ beaten 0/3,panmictic 反而超过③ |

第 I 段的 corridor 里③能把 RR 排除出去,**为什么在 kernel 空间做不到?** 根因只有一个。

> **RR 在每次 restart 都能直接采样 kernel_id ∈ [0,4)。** kernel 选择是 4 个离散值上的单一坐标 (**低维**),所以 RR 在 restart 时直接命中全部 4 个 kernel。「找最佳 kernel」无需跨谷 = **直接传送**。所以③的 behavioral niching 没有出场机会。

第 I 段③能排除 RR,是因为那里的 behavior 是 `mean(24 维)`,平均集中在 0.5 → 全局峰在 measure-zero 区域 = **高维、无法直接采样**。而 kernel_id 相反,是低维、可直接采样。

**(3) red-team——对抗式验证也无法反证,反而确证**:在 positive control 上,instrumented RR 把 restart kernel 在 4 个 basin 上近乎均匀分散为 [12,18,16,18],target 抵达率 88%。在全部 4 种 faithful 构成 (高维 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) 中,③ 都赢不了 RR。把 corridor 收紧,③ **先饿死 (starve)** (D=3:③ reach 0.08 vs RR 0.42)。我们定量确证了 **「能把 RR 单独排除、又让③通过的 behavior 维度,在 kernel 空间里结构上不存在」**。

**verdict**:形式上是 N/A (positive control 无法 validate),但实质是 **决定性的结构性 negative**。harness 是健全的 (它正确地把 negative control 置 null,并检测出 GA/random),然而基质 **根本无法承载③的欺骗地形**。对第 I 段遗留的问题「用 kernel 多样化扩展搜索空间,③ 会 unlock 吗?」的回答是 **NO (在 CPU 上,结构性地)**。

**honest 保留 (重要)**:这 **不是「③不需要被判明」**。它是「③ 在低维 kernel 空间里原理上无法与强 baseline 分离」= **有信息量的 N/A**。③ 的机制本身在第 I 段已确证为真货。substrate 很弱 (实质 3 kernel;hopfield 是对角 mock)。更强的 kernel 实现在理论上有得出不同结论的余地,但 **结构性障壁 (低维选择 → RR 直接采样) 与 kernel 实现的质量无关**。

---

## 8. 结构性洞见——用一个条件统合 6 段

存在证明 (I) 与 4 个 negative (II–V),全都在仅仅一个条件下连成一体。

> **③ (behavioral niching) 超越强 baseline,只在「难点」位于高维 behavior 空间、无法用直接采样 (随机重启) 抵达时。**

- **第 I 段满足的理由**:behavior = `mean(24 维)`。平均被中心极限定理集中在 0.5,全局峰 (mean≈0.9) 实质 measure-zero。random 和 restart 都 **够不着**。所以留下踏脚石、做 ratchet 的③是必需的。
- **真实 CPU 基质不满足的理由**:难点是低维。ESN 文本 proxy 的控制坐标实质是 leak rate (光滑的低维旋钮;本就没有谷)。kernel union 的难点是「哪个 kernel」= 4 选 1 的单一离散。RR 直接采样、传送到全部 basin,所以没有需要跨的谷。

所以第 II 段的「基因空间多峰性 1.000」不是充分条件——即便基因满是谷,只要难点集中在低维 behavior 坐标上,restart 就能直接抵达。**起作用的是「探索需抵达的 behavior 的维数」,而不是基因的维数。**

---

## 9. 生物学接地——100 年前的进化生物学早已给出同样的答案

从这里开始是 #34 的看点。**「保持多样性的选择,只在狭窄条件下起作用,其余时候是冗余的」**——这个边界条件,在 20 世纪的进化生物学里有一个异常干净的先例。

> ⚠ **honesty 契约**:以下生物学是 **「比喻 (structural analogy)」,而不是我们计算结果的证明**。对应是结构性的,在机制层面并不一致。比喻偏离之处,我都当场注明。引用的论文,只列出已单独对照一次信息源、核实过存在、归属与主张内容的。

### 9.1 赖特 (Wright) 的转移平衡说 = ③ 的先例

休厄尔・赖特 (Sewall Wright, 1931/1932) 这样思考。若维持为一个大「群 (panmictic population)」,普通的自然选择会 **被眼前的局部峰困住**。要去更高的山,必须先 **降低 mean fitness、跨过山谷**,而确定性的选择拒绝这样做。

赖特的解法是 **把群分成众多半隔离的亚群 (deme)**。

- **Phase I**:小 deme 凭 **遗传漂变 (drift)** 偶然下谷、渡过去。
- **Phase II**:在那里,deme 内的普通选择登上新的 (更高的) 峰。
- **Phase III**:登上高峰的 deme 派出许多迁移者,优良的基因组合扩散到整个物种。

作为 **整个** 元群体,它跨越了单一收敛群体无法跨越的谷——这是「用踏脚石渡过欺骗地形的谷」的生物学版。

**对应到③ / MAP-Elites (= 比喻,非归属)**:archive 的每个 cell = 半隔离 deme,cell 内的局部 elitism = deme 内选择 (Phase II),cell 间变异 = interdeme 扩散 (Phase III),而 **archive 整体** (≒ 元群体,非单一 cell) 跨越山谷。

> **honesty 注意 (2 点)**:
> 1. **这是解说者的框架,既非赖特的主张,也非 MAP-Elites 的出处。** MAP-Elites 原论文 (Mouret & Clune 2015) 与 QD 文献 **都没有引用赖特或「转移平衡」**。赖特是作为我们的 **灵感 / 比喻** 提出的,而非 MAP-Elites 的谱系。
> 2. **机制只是结构相似,并不相同。** MAP-Elites 的渡谷是 **变异算子** 把子代放进新 cell 而发生的,**不是遗传漂变**。archive 也不是复制 cell 的群体。

### 9.2 赖特 vs 费希尔 = 维数 (地形的形状) 之轴

与赖特同时代的费希尔 (R. A. Fisher, 1930) 主张相反:**大的 panmictic 群体 + 对加性方差的群体选择就足够** 让适应推进,根本无需特意分割。

二人 **最深的对立轴,其实是「上位性 (基因间相互作用) 与地形的形状」**。赖特假设「因非加性相互作用,地形 **崎岖多峰**,所以需要跨谷的 drift」,费希尔判断「相互作用存在但不重要,地形大致 **单峰、可平滑攀登**,所以群体选择就够」。

**这个 epistasis/ruggedness 之轴,正是我们结果生存的维度。地形的形状 (topology) 才是全部问题。** 若地形确实崎岖高维 (赖特 regime),多样性把你摆渡过谷;若光滑或难点低维 (费希尔 regime),群体选择——即强随机重启爬山的生物学版——就已足够。我们的 ESN 文本 proxy 是 noise-free 且光滑的,kernel union 的难点是低维离散。**两者都是费希尔 regime**,③ 不起作用、也没起作用。

> 细节注意 (诚实地):「费希尔忽视了 drift」是被压缩的俗说。准确说是「他承认 drift 存在,但判断在大群体里其量可忽略」。不是全盘否定。

### 9.3 我们的 negative = 科因批判的计算版

最切中的对应,不是赖特的 **提议**,而是生物学界的 **经验判定**。Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) 从理论与实证两面评估了转移平衡说,并如此结论 (全文已对照)。

- **群体选择通常就够了。** 「几乎没有用赖特三段机制比用简单群体选择解释得更好的实例。」人为选择实验也没能证明「分割群体的选择比大群体的群体选择产生更大的响应」。
- **转移平衡起作用,只在有限、稀少的条件下。** 群体结构的经验估计表明「**drift 只能在被浅谷隔开的峰之间引起迁移**」(深谷靠 drift 极少能渡过),而且 **大多数适应不需要跨谷**。

这是我们结果的 **惊人精确的生物学版**。把他们的话翻译成我们的词汇就是——**若地形并非真正欺骗/高维,普通的群体选择 (≒ 强随机重启爬山) 就已经能解,多样性维持装置几乎什么都买不到。**「现实的谷通常浅、大多数适应不需跨谷」就是我们「**实际地形通常简单,所以 niching 是冗余的**」的生物学陈述。

> **honesty 注意 (3 点)**:
> 1. **他们没有「反证」转移平衡。** 他们明言 Phase I/II 可能发生,并举出 6 个经验事例。主张是 **更狭窄的、概率性的** (「难以称之为一般而重要的机制」),写「refuted」就过头了。
> 2. **论争尚未了结。** Wade & Goodnight (1998)、Peck et al. (1998,标题字面就主张「feasible」) 提出反驳,接着是 Coyne 等人 2000 年的再反驳、Goodnight & Wade 在同期的反驳。不可把 1997 批判当作「最终结论」来引用。
> 3. **生物拥有计算侧无对应物的机制,而且做出比我们更强的主张。** 在 Phase III,保护多样性的 gene-flow 障壁可能 **把好解困在周边 deme、妨碍其扩散** = niching 可能 **适得其反**。我们 stateless 的离散选择设置没有这个 cost 的对应物,所以这里 **不过度叠加**。这是生物做出更强主张的地方。

### 9.4 两个实例——低维的蛾,与高维的大肠杆菌

我们的主张有两个极 (低维 = ③不需要 / 高维 = ③ 可能起作用),而进化生物学对每个都有干净的实例。

**低维之极——桦尺蛾的工业黑化 (= BG9 kernel 情形)**:*Biston betularia* 的 carbonaria (黑) vs typica (白) 受 **单一孟德尔座位、少数等位基因** 支配 (致因变异是向 cortex 基因的转座因子插入;van't Hof et al. 2011/2016),并受 **强方向性选择** (s ≈ 0.1-0.2;Saccheri et al. 2008;捕食在 Cook, Grant, Saccheri & Mallet 2012 中再确认)。最优在每个时点都是单峰,只随环境平移。**简单的方向性选择——贪婪爬山/随机重启的生物学版——直接固定更适应的型,多样性维持机制既不需要也未被调用。** 这恰恰就是 BG9:kernel 选择是 4 选 1 的低维单一座位,RR 直接采样全部 kernel,③ 在结构上无法分离。**黑化型 = BG9 kernel 情形的生物版。**

> 注意 (诚实地):过渡期会暂时保持多型,但那是由于 **空间环境异质 + 基因流动 (迁移-选择平衡)**,而非内在的多样性保存机制。比喻略微偏离之处。

**高维、依赖历史之极——伦斯基的 Cit+ (= ③ regime)**:在大肠杆菌长期进化实验 (LTEE) 中,需氧柠檬酸利用 (Cit+) 在 **12 个群体中恰好 1 个** 里于约第 31,500 代进化出来 (Blount, Borland & Lenski 2008)。关键是一条高维、依赖历史的路径,即有序的 **potentiation (前驱变异的积累) → actualization (citT 串联重复带来的启动子捕获) → refinement** (Blount et al. 2012)。重放实验把「历史偶然性」从「恒定率的稀有变异」中区分开来。这 **真正例示** 了探索 contingency、上位性与高维崎岖地形的价值——是③可能起作用之 regime 的实例。

> **honesty 注意 (这只对应我们条件句的「前件」)**:
> - **LTEE 不使用 niching 算法。** 它就是普通的自然选择,12 个并行群体 **本身就是随机重启式的设计**。所以它是「contingency + 多样性使稀有创新成为可能」的存在证明,**不是**「niching 胜过强 restart baseline」的证据。
> - 「大肠杆菌从零获得吃柠檬酸的能力」是俗说的夸张。创新是 **调控 (既有转运体的需氧表达) = exaptation**,既非新基因也非新生化。
> - Van Hofwegen et al. (2016) 指出「若直接选择,Cit+ 出现得快得多」,挑战了「稀有/偶然」框架 (伦斯基一侧反驳说这与 LTEE 条件下的 potentiation 并不矛盾)。若要依赖「极稀有/长期延迟」叙事,就应一并注明这个 **有争议的追试**。

### 9.5 接地小结

| 极 | 生物学 | 地形 | ③ 起作用? | 我们的基质 |
|---|---|---|---|---|
| 低维/光滑 | 黑化型 (单座位, s≈0.1-0.2, 方向性) | 单峰・平移 | **No** — 群体选择足够 | BG9 kernel union;ESN/ridge 文本 proxy (确定性・光滑) |
| 高维/偶然 | 伦斯基 Cit+ (potentiation→actualization→refinement) | 崎岖・靠变异越谷 | **Yes** (可能起作用的 regime) | 合成欺骗 corridor (behavior = 24 维的平均) |
| 经验判定 | 科因・巴顿・图雷利:群体选择通常足够,转移平衡极少起决定性作用 | 实际地形通常简单 | 我们 **negative 的镜像** | 试过的全部 CPU 基质 |

**结论**:赖特的转移平衡是「③起作用时**为何**起作用」的正确生物学先例,赖特-费希尔的 epistasis/ruggedness 之轴是「**维数**条件」的正确框架,黑化蛾与伦斯基 Cit+ 是低维/高维的干净两极,科因批判是我们 **negative** 的生物学先例。**但这些都不能证明计算结果。它们只是接地。** 比喻松动最大之处,在于生物加了一个 cost (Phase III 的 gene-flow trap)——我们 stateless 的设置没有它。

— 歇一会儿。当我意识到 100 年前的论争有同样的形状时,老实说我起了一身鸡皮疙瘩。但不把「起鸡皮疙瘩」误认作「证明」,正是本次的纪律。 —

---

## 10. 对 GPU 的含意——剩下的路只有高维,但依旧是赌

arc 把 CPU 的路全部堵死了。真实 proxy 是 noise-free 且光滑 (IV),最后的候选 (kernel 多样化) 在结构上被堵死 (V)。③ 剩下的路只有 **高维地形**——而提供它的,是 **full-LLM 的参数/损失空间 (数百万维)**。

结构性洞见让 GPU 这场赌 **better-motivated**。它不是「也许只有 full-LLM 是例外」这种盲目的赌,而是遵循原理「**③ 需要高维,而 full-LLM 正处于高维域**」的赌。

**但依旧是赌。** 出于与生物学的 Cit+ 不能证明「③ 算法的胜利」相同的理由,以及与 BG9 里赢不了 RR 同型的理由——**若真实 LLM 地形能用 backprop (梯度下降) 这个强 baseline 直接导航,③ 仍然不需要**。难点是高维,这是 **必要条件而非充分条件**。还需额外证明「强力的直接法解不了它」(CPU 上是 RR,GPU 上是梯度下降)。

所以 GPU 适合的 **不是「单为③」**,而是 **组合 (portfolio) 判断** (与 llive 的真 LLM fitness 等搭车) + **借云做 1 次预先登记** (在投入资本之前)。go/no-go 标准也能写成 falsifiable:

> **full-LLM 的难点在 behavior 上是否高维,且是否难以被强力的直接 baseline (梯度下降) 抵达?** 若高维但梯度能直接够到,③ 不需要 (= BG9 的 RR 结果的 GPU 版)。

---

## 11. 元教训——诚实,是用来赢的工具

这段 arc 真正的成果不是数值,而是 **「怀疑过于工整的结果」这种精神,实际上把研究往前推进了**。

- 在 **存在证明 (I)** 中赢的时候,我们用去掉谷的边界实验,主动确认了「③不是万能」(不高估胜利)。
- 在 **泛化 (III)** 中,同行评审甩出 3 个 rerun blocker,但修正后结论没变 (确认它不是脆弱的 negative)。
- 在 **确定性测量 (IV)** 中,因为物理性地抹掉了评估噪声,我们才能区分「光滑」是地形的性质还是仪器的极限。
- 在 **BG9 (V)** 中,在对抗式验证里我们 **试图反证、却无法反证** 自己的「③立不住」,它被确证为结构性的 (同样的纪律也在「把 negative 正确地确定为 negative」的方向上起了作用)。

而贯穿整段 arc 我们学到一件事——**低维的难点会被强 baseline 直接解掉。所以③ (分门别类、隔离培育的工夫) 要起作用,就需要「高维 behavior 空间」。**「做出欺骗地形③就立得住」只对了一半;准确说,除非是 **高维到无法直接采样** 的欺骗地形,③ 才立得住。而且令人惊讶的是,这个边界条件是 **赖特的转移平衡与科因批判在近 100 年前就已抵达** 的。

「当出现异常好的结果时,在自以为赢之前,务必先怀疑其内訳」——FullSense 的研究纪律 (`honest disclosure`) 不仅是自我告诫,而是一个 **实际捕捉假阳性、正确确定 negative、提升研究精度的机制**,在全部 6 段中都在转动。

最后,把结论再精确地说一遍。

> **③ 活起来,只在「高维」的欺骗地形时。** 它在存在证明 (合成 corridor) 中完胜,但真实 CPU 基质——记忆任务 (地板/天花板)、多任务泛化 (光滑)、真实 proxy 文本地形 (noise-free 且光滑)、kernel 多样化 (低维、结构上堵死)——没有一个满足那个条件。这 **不是「③了结 = ③被判明不需要」**,而是「现在能在 CPU 上测的仿真之物,没有满足③活起来的条件 (高维欺骗地形)」。主城 (GPU 高维) 还在前方,而且是一场背负着「强力直接 baseline 会解掉它」风险的赌。而且这个结论的骨架,20 世纪的进化生物学早已描绘过——只不过生物学 **不证明它,只接地它**。

---

**Tags**: 进化计算 / MAP-Elites / 统计检定 / honest disclosure / 进化生物学 / CPU 研究
**关联**: 连载 #33 (第三轴 ③ 了结 Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (反证・Goodhart・proxy 极限)
**Project**: llcore (PyPI 预约 llmesh-llcore,因仓库未公开故为本地研究)

---

# 한국어

# (연재 #34) 산오르기 6연전으로 알게 된 「진화의 ③은 언제 효과가 있는가」— 그리고 100년 전의 진화생물학이 같은 답을 내놓고 있었다

## TL;DR

- 질문은 **「AI의 코어 계산을 진화로 탐색할 때, '가려내어 따로 길러 내는 공정' (= 진화의 ③ 적자생존/분리) 은 정말로 필요한가」**. 연재 #33은 종반 (Step D + BG9) 의 결착을 썼지만, **이 #34는 arc 전체 (6단) 를 하나의 이야기로 조망**합니다.
- **제1단 (합성 속임수 지형)**: ③은 압승 (Cliff δ=+1.0). ③은 메커니즘으로서 진짜 = **존재 증명**.
- **제2단 (기억 과제 / 다중 reservoir)**: 기질의 「바닥」과 「천장」에 가로막혀 ③을 측정 불가 = **N/A**.
- **제3단 (다중 과제 일반화)**: ③은 「선택 없음」에는 이기지만, 단순한 선택이나 random에는 못 이김 = ③ 불필요 (honest negative).
- **제4단 (실제 proxy 지형을 noise-free 측정)**: 평가 노이즈를 물리적으로 0까지 낮췄더니 지형은 **정말로 매끄러움 (단봉)** = ③ 불필요 확정. 「과거의 negative는 검출력 부족이 아니라 지형이 매끄러웠던 것」이 처음으로 뒷받침되었다.
- **제5단 (부품 4종을 섞는 샛길 BG9)**: kernel 선택은 **저차원**이기에 강한 baseline (랜덤 리스타트 산오르기) 이 직접 샘플링하고, ③의 niching 우위가 **구조적으로** 나타나지 않음 = 샛길은 막혔다.
- **구조적 통찰 (이 arc의 핵심)**: ③이 효과가 있는 것은 난소(難所)가 **고차원 behavior 공간**에 있어 직접 샘플링이 불가능할 때뿐. 실제 CPU 기질은 저차원/매끄러우므로 ③ 불필요.
- **생물학적 접지 (검증 완료)**: 이것은 라이트 (Wright) 의 **시프팅 밸런스 설** 바로 그것. **흑화형 나방 (단일 유전자 = 저차원)** 에서는 보통의 선택으로 충분 (= BG9의 kernel 케이스), **렌스키의 Cit+ (고차원・역사 의존)** 에서는 다양성이 효과적 (= ③ regime). 우리의 negative는 **코인 비판의 계산판** (현실 지형은 단순하고 ③은 드물게만 결정적).
- **메타 교훈**: 「너무 잘 풀린 결과는 승리가 아니라 경보」. 사전 등록・honest disclosure・적대 검증・결정론적 noise-free 측정으로, 섣부른 기쁨을 피했다.

> ⚠ 이 글의 수치는 모두 수중 (로컬) 의 연구 기록에 연결된 실측입니다. llcore는 아직 공개 리포지토리를 만들지 않았으므로 외부 링크를 붙일 수 없습니다. 대신 「어떻게 측정했는가」를 본문에 씁니다. 생물학 파트에서 인용하는 논문은, 별도로 1차 정보로 존재・귀속・주장 내용을 대조한 것만 들고 있습니다.

---

## 0. 이 글은 무엇에 대한 이야기인가 (콘셉트)

`llcore`는 「Transformer의 코어 계산 (상태 갱신 규칙・학습 규칙・인지 구동 Δ) 을 유전자로 삼아, Z3로 망가지지 않도록 검증하면서 진화시킨다」는 CPU 완결 연구 프레임워크입니다.

그 진화 엔진에는, 진화의 4요소 (① 변이 / ② 유전 / ③ 적자생존・분리 / ④ 과잉번식) 중 **③ (selection / separation)** 을 어떻게 효과적으로 발휘시킬 것인가, 라는 설계상의 급소가 있습니다. 다양성을 유지하며 니치에 남기는 MAP-Elites 같은 「가려내어 따로 길러 내는」 구조입니다.

질문은 단순합니다.

> **그 ③, 정말로 필요한가?**

필요하다면, ③을 얹기 위한 무거운 투자 (최종적으로는 GPU로 실제 LLM을 돌리는 것) 에 의미가 있다. 필요 없다면, ③에 집착하는 것은 시간과 전기의 낭비가 된다.

연재 #33에서는 그 질문의 **종반** (Step D의 결정론 측정 + BG9의 구조적 결착) 을 상세히 썼습니다. 하지만 거기에 이르기까지에는 **6단의 실험**이 있었고, 이기거나 (존재 증명), 측정하지 못하거나 (N/A), 지거나 (honest negative) 를 반복했습니다. 이 #34에서는 그 **arc 전체를 하나의 이야기**로 다시 늘어놓습니다. 게다가 이번의 볼거리로서, **이 계산 결과가 100년 가까이 전의 진화생물학 논쟁 (라이트 대 피셔) 과 놀랄 만큼 같은 형태를 하고 있다**는 것을, 검증 완료한 1차 정보로 접지합니다.

— 여기까지 40초. 준비운동 끝. 본론으로. —

---

## 1. 비유: 산오르기, 그리고 속임수 지형, 그리고 기억의 궁전

수식 전에, 이 연구에서 일관되게 쓰고 있는 3개의 메타포로 전체상을 파악합니다.

설계의 좋고 나쁨을 **지형의 높이**로 나타냅니다. **높은 곳 = 좋은 설계**. 가장 높은 정상을 찾는 게임입니다.

**지형 1: 매끄러운 한 봉우리 (쉬움)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

이런 지형에서는, 소박한 「산오르기법 (hill-climbing)」, 즉 「지금보다 조금 더 좋은 쪽으로 움직이기만」 하는 것으로 충분히 정상에 닿습니다. **공들인 공정 (③) 은 필요 없습니다.**

**지형 2: 속임수 지형 (기만적 deceptive)**

```
 良さ↑                                  /\
     |                                 /  \   ← 本物の頂上
     |        ニセ頂上                /    \
  中 |         /\         谷         /      \
     |        /  \______________/        \
  低 |____/                                  \
     +----------------------------------------→ 設計の選び方
          ↑ニセ頂上で素朴な山登りは停止 (谷を下れない)
```

여기서는 소박한 산오르기가 가짜 정상에서 멈춥니다. 골짜기를 내려갈 용기가 없기 때문입니다.

이때 효과를 발휘하는 것이 ③의 발상입니다. **여러 타입의 등산자를 골짜기 여기저기에 남겨 둡니다** (= 기억의 궁전 / MAP-Elites archive). 누군가가 골짜기를 「징검돌 (stepping-stone)」 로 건너 진짜 정상에 도달할 수 있다, 라는 구조입니다.

**이 연구의 핵심을 한마디로**: ③이 정말로 도움이 되는 것은 **「속임수 지형」일 때뿐**. 매끄러운 한 봉우리에서는, ③은 무용지물입니다.

그래서 질문은 이렇게 바꿔 말할 수 있습니다.

> **「진화로 AI를 설계할 때, 실제로 마주치는 지형은 '속임수 지형'인가, 아니면 '매끄러운 한 봉우리'인가?」**

#33에서는 Step D + BG9로 이 질문에 결착을 지었습니다. 이 #34에서는, 거기에 이르는 **6단의 산오르기 전부**를 보여드립니다. 각 단에서 「속임수 지형이었는가 / 매끄러웠는가 / 애초에 측정할 수 있었는가」가 달라지는 것이 흥미로운 점입니다.

— 잠깐 쉼. 준비는 여기까지. 여기서부터 6연전의 실록입니다. —

---

## 2. arc 전체 지도 — 6단의 산오르기를 한눈에

먼저 지도를 내놓습니다. 이것이 이 글의 등뼈입니다.

| 단 | 기질 (어떤 지형을 측정했나) | ③은 효과가 있었나 | 한마디 |
|---|---|---|---|
| **I (Step 4)** | 합성한 「속임수 지형」(기만 corridor) | **Yes (압승)** | 존재 증명. ③은 진짜 |
| **II (Step C / 사다리1)** | 기억 과제 / 다중 reservoir 패리티 | **N/A** | 바닥・천장・degree-5의 벽으로 측정 불가 |
| **III (E-A)** | 다중 과제 일반화 | **No** | ③은 「선택 없음」에는 이기지만, 그 이상은 아니다 |
| **IV (Step D)** | 실제 proxy의 텍스트 지형 (결정론 측정) | **No** | 지형이 **정말로 매끄러움**으로 확정 (noise-free) |
| **V (BG9)** | 부품 (kernel) 4종의 union | **No** | **구조적으로** 막혔다 (저차원 선택) |

스토리 라인은 이렇습니다. **먼저 「③은 조건에 따라 압승하는 진짜다」라고 존재 증명하고 (I), 다음으로 「그럼 실제 문제에서는 어떤가」를 4단에 걸쳐 측정하러 갔더니 (II~V), 하나같이 "실제 CPU 기질은 ③이 필요 없는 지형이었다"**. 게다가 마지막 (IV, V) 에서 「필요 없는 이유」가 **검출력 부족이 아니라 지형의 성질**이라고 확정되었다 ── 이것이 arc 전체의 호(arc)입니다.

그럼 한 단씩.

---

## 3. 제I단 (Step 4) — 존재 증명: 속임수 지형이라면 ③은 압승한다

가장 먼저 한 것은 「③이 **이론대로 효과를 내는 장면이 실재하는가**」의 존재 증명입니다. 지형을 **일부러 기만적으로 만들어**, ③ (MAP-Elites) 을 3개의 baseline ── pure random / panmictic GA / **랜덤 리스타트 산오르기 (random-restart hill-climbing)** ── 와 대결시켰습니다.

**지형의 구성**: 유전자는 24차원. behavior (등산자의 타입) 를 `mean(유전자)` = 24개의 평균으로 정의합니다. behavior를 올리려면 **전체 24차원을 동시에 높게** 하지 않으면 안 됩니다. fitness는 「behavior≈0.4에 가짜 정상 (값 0.6) → behavior≈0.65에 골짜기 (값≈0) → behavior≈0.9에 진짜 정상 (값 1.0)」 라는, 그야말로 속임수 지형.

**결과**:

| 방법 | 진짜 정상으로의 도달률 | ③ 과의 비교 |
|---|---|---|
| **MAP-Elites (③)** | **약 95%** | — |
| pure random | 0% | p=1.9e-6, Cliff δ=+1.00 |
| panmictic GA | 0% | 위와 같음 |
| 랜덤 리스타트 산오르기 | 0% | 위와 같음 |

③만이 진짜 정상에 닿았고, 3개의 baseline은 전부 가짜 정상 (≈0.60) 에서 멈췄습니다. **100% 승 / 효과량은 이론 최대 (δ=+1.0)**. base seed 3가지 (총 60 seed) 에서 견고.

왜 이렇게 되는가, 가 나중의 복선이 됩니다.

- **random** 은 behavior가 반드시 ≈0.5에 집중한다 (24개의 평균은 중심극한정리로 0.5에 고정). 그래서 behavior 0.9에는 **영원히 도달할 수 없다** (6000 샘플을 뽑아도 0%).
- **산오르기** 는 가짜 정상 0.6까지 오르고, 골짜기를 내려가는 한 수를 거부. 리스타트해도 behavior≈0.5로 돌아가, 같은 함정으로.
- **③ (MAP-Elites)** 는 골짜기의 칸을 「새로운 behavioral 니치」로 보유하고, behavior를 0.5 → 0.9로 **징검돌로 건넌다**.

**경계도 정직하게 측정했습니다**. 골짜기를 없앤 매끄러운 corridor에서는, ③은 산오르기를 못 이기게 됩니다 (p≈0.29). **③은 만능이 아니라, 속임수 지형에서만 효과가 있다.**

**honest 유보**: 이것은 **일부러 만든** 합성 지형입니다. ③이 「가능」하다고 증명했을 뿐, 현실의 과제가 이 구조를 가진다는 증명은 아니다. toy 스케일・저노이즈・baseline은 소박한 (1+1) 입니다.

→ 여기서 가설이 섭니다. **「실제 문제의 지형도, 이 정도로 속임수 지형이라면, ③은 살아날 것」**. 다음 4단은, 그것을 실제 문제에 가까운 기질로 확인하러 가는 여행입니다.

— 한 모금. 제I단은 기분 좋은 압승이었습니다. 여기서부터 구름의 흐름이…. —

---

## 4. 제II단 (Step C / 사다리1) — 기질의 「바닥」과 「천장」에 가로막힌다 (N/A)

다음으로 「속임수 corridor가 **표준적인 기억 과제에 자연스럽게 출현하는가**」를 조사했습니다 (Step C). delayed parity / flip-flop / delayed recall을, 1개의 leaky reservoir + ridge readout으로.

결과는 깔끔한 **N/A (측정 불능)**. 이유가 양극단이라 흥미롭습니다.

- **delayed parity = 바닥 (floor)**: 1개의 reservoir는 XOR을 계산할 수 없다 (Minsky-Papert). 모든 방법이 R²≈0.003. 아무도 오를 수 없으므로 ③을 분리할 수 없다.
- **flip_flop = 천장 (ceiling)**: 모든 방법이 R²≈0.95에 포화. 분산이 짓눌려 ③의 차이가 나타나지 않는다 (③ vs random은 부호는 양이지만 p=0.15 = underpower로 **null이 아니다**).

여기서 중요한 발견이 하나. **유전자 공간의 다봉성은 높았다** (valley fraction이 parity에서 1.000) 인데, ③의 역할에는 도움이 되지 않았다. 즉 **「유전자 공간에서 다봉」≠「behavior에서 건너야 할 속임수 지형」**. 이 구별이 arc 후반의 열쇠가 됩니다.

**사다리1 (다중 reservoir)**: 그럼 reservoir를 여럿 연결하면 바닥이 올라가는가? → 5개의 메커니즘을 시험해 전부 `floor_lifted = false`. 깊이 (DeepESN) 는 바닥을 통계적으로는 올린다 (효과 +0.47/+0.60, PASS) 지만 절댓값은 R² 0.05-0.10에 그친다. 결정타는 positive control: degree-2 readout은 2-bit XOR을 엄밀히 푼다 (R²=+1.0) 지만 degree≥3에서 붕괴. **5-bit 패리티는 degree-5 = 이 CPU reservoir+ridge 패러다임의 구조적인 벽.**

→ 패리티 경로는 구조적으로 막혔다. ③의 본검정은 **패리티에서 내려올** 필요가 있다.

**honest 유보**: degree-5의 벽은 「이 설정의 벽」이지, 패러다임 전체의 불가능성 증명은 아닙니다.

— 잠깐 쉼. 「측정할 수 없었다」는 결과는 수수하지만, 지도를 그리는 데에는 중요한 공백 지대입니다. —

---

## 5. 제III단 (E-A) — 다중 과제 일반화: ③은 필요 없었다 (honest negative)

패리티의 바닥에서 내려와, **일반화 (generalization)** 로 ③을 측정했습니다. 가장 깔끔한 ablation을 짜서.

**설정**: 단층 leaky reservoir + ridge. 가변 지연의 recall. **짧은 지연 {15, 30} 으로 학습하고, 긴 지연 {45, 60} 으로 테스트** (외삽). 비교는 MAP-Elites (①②③풀) vs **선택을 뺀 MAP-Elites** (`randselect`: 부모를 랜덤으로 골라 무조건 배치 = 변이만) + panmictic GA + random.

**결과 (페어 리뷰 후)**:

| 방법 | 테스트 일반화 R² (평균±std) |
|---|---|
| MAP-E (①②③풀) | 0.682 ± 0.115 |
| MAP-E randselect (선택을 뺌) | 0.557 ± 0.108 |
| panmictic GA | 0.702 ± 0.083 |
| random | 0.620 ± 0.105 |

| 게이트 | 비교 | diff | p (단측) | 판정 |
|---|---|---|---|---|
| C-gen3 | MAP-E > randselect | +0.126 | 0.0151 | **PASS** |
| C-gen4a | MAP-E > panmictic | −0.019 | 0.598 | FAIL |
| C-gen4b | MAP-E > random | +0.062 | 0.126 | FAIL |

**읽는 법**: ③은 「**선택을 뺀 드리프트 대조**」에는 이긴다 (C-gen3 PASS = "어떤 선택이든 무선택에는 이긴다"). 하지만 **panmictic GA (선택은 있지만 niching 없음) 에는 못 이기고** (오히려 근소하게 짐), random에도 못 이긴다. 즉 **niching 고유 (= ③ 본래) 의 기여는 없다**. 이 일반화 지형은, 단순한 선택이나 random으로도 같은 곳에 닿을 만큼 **매끄러웠다**. 제I단의 「매끄러우면 ③은 효과가 없다」 경계와 정합합니다.

**honest 유보 (중요)**: 이 verdict는 **이 설정 한정** (예산 400, grid 6×6). 게다가 ── 여기가 honest methodology의 핵심 ── 페어 리뷰 (Codex) 가 당초 「신용할 수 없다」고 판정하고, 3개의 rerun 블로커 (replicate마다의 독립 seeding / 예산 내 글로벌 최량의 채용 / honest_n을 16→30) 를 강제했습니다. **수정 후에도 결론은 바뀌지 않았습니다.** 「고치면 결론이 바뀌는 취약한 negative」가 아니었다, 라는 것이 수확입니다.

— 한 모금. 진 건 진 거지만, 「올바르게 졌다」는 것을 확인하는 작업 쪽이 시간이 더 걸렸습니다. —

---

## 6. 제IV단 (Step D) — 실제 proxy 지형은 「정말로 매끄러움」으로 확정 (noise-free)

여기가 arc의 전환점입니다. 제III단까지 「③ negative」가 이어졌지만, 줄곧 **응어리**가 남아 있었습니다.

> 「③ 불필요」는 정말로 **지형이 매끄럽기** 때문인가? 아니면 단순히 **샘플 수가 부족해 차이를 검출하지 못한 (underpower)** 것뿐인가?

이것을 헷갈리면 「③은 무력」이라고 과잉 일반화해 버린다. Step D는 여기에 결착을 짓습니다.

**트릭**: ESN reservoir (고정 seed) + ridge readout의 closed-form (`np.linalg.solve`) 은 **난수를 일절 뽑지 않는다**. 그래서 평가 노이즈를 **머신 엡실론 (약 1.11e-16)** 까지 물리적으로 0으로 만들 수 있다. 실측으로 `eval_noise_std ≤ 1.11e-16`을 확인 ── 이것은 부동소수점의 최소 단위 (ULP) 유래로 **실질 제로**입니다. 노이즈의 안개를 완전히 걷어내고, 지형의 골짜기를 직접 측정할 수 있다.

지형은 llcore 자신의 소스 (약 24k 문자) 의 다음 문자 예측. valley_fraction (골짜기의 비율, ≥0.2면 다봉=속임수 지형) 을 측정했습니다.

| 지형 | 차원 | valley_fraction (mean/max) | 다봉? | 판정 |
|---|---|---|---|---|
| **ESN 3-param** (실제 proxy) | 3 | **0.000 / 0.000** | No (3 seed 일치) | 매끄러움 → noise-free로 ③ 불필요 확정 |
| **ESN per-neuron** (실제 proxy) | 40 | **0.096 / 0.121** | No (3 seed 일치) | 매끄러운 편 → ③ 불필요 |
| 다봉 control (양) | 3 / 40 | 0.70 / 0.80 | Yes | 진단기는 다봉을 검출할 수 있다 ✓ |
| 이차함수 control (음) | 3 / 40 | 0.000 | No | 진단기는 매끄러움을 검출할 수 있다 ✓ |

포인트는 2개.

1. **실제 proxy 지형 (3차원 / 40차원 모두) 은 단봉**. 3 seed에서 일치.
2. **진단기 자체는 건전**. 일부러 만든 다봉은 제대로 다봉으로 검출하고, 이차함수는 제대로 매끄러움으로 검출한다. 그래서 「실제 proxy가 단봉」은 계기의 버그가 아니라 **지형의 성질**.

→ 이것으로 처음으로 **「과거의 ③ negative는 underpower가 아니라, 지형이 정말로 매끄러웠다」**가 실제 substrate 위에서 noise-free로 뒷받침되었습니다. 재측정해도 다봉은 나오지 않는다.

**honest 유보 (중요)**: 「매끄러움」은 임곗값 근접에서만 정밀합니다. ESN 3-param의 midpoint의 **90.9%가 약간 아래로 dip**하고, 최대 상대 dip (0.0435) 은 골짜기 임곗값 0.05의 바로 아래. 정확히는 「**진정으로 단봉**」이 아니라 「**임곗값을 근소하게 밑도는 얕은 골짜기 (~2-4%) 를 가진 약한 multi-basin**」. 방향은 유지되지만, 견고성은 임곗값 근접이기에 한정적 ── 여기를 「완벽한 볼록 그릇」으로 뭉뚱그리지 않는 것이, 이번의 규율입니다.

— 심호흡. 여기서 「실물 모형도 매끄럽다」가 확정. 남은 건 「마지막 CPU 샛길」입니다. —

---

## 7. 제V단 (BG9) — 부품을 섞는 샛길은, 구조적으로 막혀 있었다

실제 proxy가 매끄럽다고 확정된 이상, 매끄러운 지형에서 ③을 좇아도 이득은 나오지 않는다. 하지만 GPU는 투자 판단이므로, **CPU에서 전진할 수 있는 다른 가설**을 시험했습니다. 그것이 **kernel 다양화 (BG9)** 입니다.

**가설 (사전 등록 H7)**: 개개의 kernel (rwkv / mamba / hopfield / linear_attn) 이 매끄러워도, **4종류를 union하면 kernel 전환의 순간에 fitness가 단차를 만든다 → multi-basin (속임수 지형) 이 된다 → ③이 GPU 없이 CPU 위에서 선다**. 사전 등록한 honest prior는 **null 쪽** (지금까지 모든 CPU 기질이 매끄러웠으므로).

결과를 3단으로.

**(1) substrate validity — 변별은 있지만 약하다 (PASS지만 요주의)**: 과제마다 잘하는 kernel이 다른가를 측정하면, 사상(寫像)은 비상수 = non-inert (PASS). mamba는 selective-copy, linear_attn은 weighted-accumulation에서 best. 다만 **hopfield는 어떤 과제에서도 못 이겼다** (대각 스칼라 mock에서 기능 부전) 므로, 실질 「**3 kernel** union」. **변별의 존재 ≠ 다봉 장벽.**

**(2) harness validity — positive control이 validate하지 않는다 (결정타)**: 합성 kernel-barrier에서 ③을 3 baseline과 비교.

| 기질 | 결과 |
|---|---|
| **positive control** | ③은 panmictic (+0.423)・random (+0.208) 을 격파. **하지만 RR (랜덤 리스타트 산오르기) 에는 못 이긴다** (+0.051, p=0.31 → FAIL). 3 baseline 전승에 못 미침 = harness가 안 선다 |
| **negative control** | 모든 method 포화, ③ 우위 없음 = 올바르게 null (계기는 건전) |
| **real** smoke | ③ beaten 0/3, panmictic이 역으로 ③을 웃돈다 |

제I단의 corridor에서는 ③이 RR을 배제할 수 있었는데, **왜 kernel 공간에서는 못 하는가?** 근본 원인은 하나.

> **RR은 restart 때마다 kernel_id ∈ [0,4) 를 직접 샘플링할 수 있다.** kernel 선택은 4 이산의 단일 좌표 (**저차원**) 이므로, RR은 restart로 전체 4 kernel을 직격한다. 「best kernel을 찾는」 데 골짜기를 건널 필요가 없다 = **직접 워프**. 그래서 ③의 behavioral niching에 출번이 오지 않는다.

제I단에서 ③이 RR을 배제할 수 있었던 것은, 거기의 behavior가 `mean(24차원)` 이고, 평균이 0.5에 집중 → 대역 피크가 measure-zero 영역 = **직접 샘플링 불가능한 고차원**이었기 때문. kernel_id는 반대로 저차원으로 직접 샘플링할 수 있어 버린다.

**(3) red-team — 적대 검증으로도 반증할 수 없고, 오히려 확증**: instrumented RR이 positive control 위에서 4 basin에 restart kernel을 [12,18,16,18] 로 거의 균일 분산, target 도달 88%. 4개의 faithful 구성 (고차원 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) 모두에서 ③은 RR에 못 이긴다. corridor를 조이면 ③이 **먼저 starve (아사)** 한다 (D=3: ③ reach 0.08 vs RR 0.42). **「RR만 배제하고 ③이 통과하는 behavior 차원은, kernel 공간에 구조적으로 존재하지 않는다」**를 정량 확증.

**verdict**: 형식상은 N/A (positive control이 validate하지 않음) 지만, 실질은 **결정적인 구조적 negative**. harness는 건전 (negative control을 올바르게 null로 하고, GA/random을 검출한다) 한데, 기질이 ③의 속임수 지형을 **애초에 호스트할 수 없다**. 제I단에서 남은 질문 「kernel 다양화로 탐색 공간을 확장하면 ③이 unlock하는가?」에 대한 답은 **NO (CPU에서는 구조적으로)**.

**honest 유보 (중요)**: 이것은 **「③ 불필요로 판명」이 아닙니다**. 「③이 저차원 kernel 공간에서는 강 baseline과 원리적으로 분리할 수 없다」 = **정보량이 있는 N/A**. ③의 메커니즘 자체는 제I단에서 진짜로 확정 완료. substrate는 약하다 (실질 3 kernel, hopfield는 대각 mock). 더 강한 kernel 구현이라면 다른 결론의 여지는 이론상 있지만, **구조적 장벽 (저차원 선택 → RR 직접 샘플) 은 kernel 구현의 질과 독립**입니다.

---

## 8. 구조적 통찰 — 6단을 하나의 조건으로 정리한다

존재 증명 (I) 과 4개의 negative (II~V) 는, 단 하나의 조건으로 전부 이어집니다.

> **③ (behavioral niching) 이 강 baseline을 웃도는 것은, 「난소」가 고차원 behavior 공간에 있어, 직접 샘플링 (랜덤 리스타트) 으로 도달할 수 없을 때뿐.**

- **제I단이 충족하는 이유**: behavior = `mean(24차원)`. 평균은 중심극한정리로 0.5에 집중하고, 대역 피크 (mean≈0.9) 는 실질 measure-zero. random도 restart도 **직접 닿지 않는다**. 그래서 징검돌을 남겨 ratchet하는 ③이 필수.
- **실제 CPU 기질이 충족하지 않는 이유**: 난소가 저차원. ESN 텍스트 proxy의 제어 좌표는 실질 leak rate (매끄러운 저차원 노브, 애초에 골짜기가 없다). kernel union의 난소는 「어느 kernel인가」 = 4지선다의 단일 이산. RR이 직접 샘플링해 전 basin에 teleport하므로, 건너야 할 골짜기가 없다.

그래서 제II단의 「유전자 공간의 다봉성 1.000」은 충분조건이 아니다 ── 유전자는 골짜기투성이라도, 난소가 저차원 behavior 좌표에 집중해 있으면, restart가 직접 닿는다. **효과가 있는 것은 "탐색이 도달해야 할 behavior의 차원"이지, 유전자의 차원이 아니다.**

---

## 9. 생물학적 접지 — 100년 전의 진화생물학이, 같은 답을 내놓고 있었다

여기서부터가 #34의 볼거리입니다. **「다양성을 유지하는 선택은, 좁은 조건에서만 효과가 있고, 그 외에서는 잉여」** ── 이 경계 조건에는, 20세기의 진화생물학에 이상하리만치 깔끔한 선례가 있습니다.

> ⚠ **honesty 계약**: 이하의 생물학은 **「비유 (structural analogy)」 이지, 우리 계산 결과의 증명이 아닙니다**. 대응은 구조적이고, 메커니즘 레벨에서는 일치하지 않습니다. 비유가 어긋나는 곳은 전부 그 자리에서 명기합니다. 인용하는 논문은, 별도로 1차 정보로 존재・귀속・주장 내용을 대조한 것만입니다.

### 9.1 라이트 (Wright) 의 시프팅 밸런스 설 = ③의 선례

슈얼 라이트 (Sewall Wright, 1931/1932) 는 이렇게 생각했습니다. 큰 「하나의 무리 (panmictic population)」 인 채로는, 보통의 자연선택으로는 **눈앞의 국소 피크에 붙잡힌다**. 더 높은 산으로 가려면 한 번 mean fitness를 **낮춰 골짜기를 건널** 필요가 있는데, 결정론적인 선택은 그것을 거부하기 때문.

라이트의 해결책은 **무리를 다수의 반(半)격리된 서브 집단 (deme) 으로 나누는** 것.

- **Phase I**: 작은 deme가 **유전적 부동 (drift)** 으로 우연히, 골짜기를 내려가 건넌다.
- **Phase II**: 거기서 deme 내의 보통의 선택이 새로운 (더 높은) 피크를 오른다.
- **Phase III**: 높은 피크에 오른 deme가 많은 이주자를 내보내, 우수한 유전자 조합이 종 전체에 퍼진다.

메타 집단 **전체**로서, 단일 수렴 집단으로는 건널 수 없는 골짜기를 건넌다 ── 이것이 「속임수 지형의 골짜기를 징검돌로 건넌다」의 생물학판입니다.

**③ / MAP-Elites로의 대응 (= 비유, 귀속이 아님)**: archive의 각 셀 = 준격리 deme, 셀 내의 국소 elitism = deme 내 선택 (Phase II), 셀 간 변이 = interdeme 확산 (Phase III), 그리고 **archive 전체** (≒ 메타 집단, 단일 셀이 아님) 가 골짜기를 건넌다.

> **honesty 주의 (2점)**:
> 1. **이것은 해설자의 틀이지, 라이트의 주장도 MAP-Elites의 출처도 아니다.** MAP-Elites의 원논문 (Mouret & Clune 2015) 도 QD 문헌도 **라이트나 「시프팅 밸런스」를 인용하지 않는다**. 라이트는 우리의 **착상 / 비유**로서 드는 것이지, MAP-Elites의 계보로서가 아니다.
> 2. **메커니즘은 구조적으로 닮았을 뿐 동일하지 않다.** MAP-Elites의 골짜기 건너기는 **변이 오퍼레이터**가 자식을 새 셀에 두는 것으로 일어나며, **유전적 부동이 아니다**. archive는 복제하는 셀의 집단도 아니다.

### 9.2 라이트 대 피셔 = 차원 (지형의 형태) 의 축

라이트와 동시대의 피셔 (R. A. Fisher, 1930) 는 반대를 주장: **큰 panmictic 집단 + 가법적 분산에의 매스 선택으로 충분**히 적응은 진행된다, 굳이 분할은 필요 없다, 고.

두 사람의 **가장 깊은 대립축은, 실은 「에피스타시스 (유전자 간 상호작용) 와 지형의 형태」** 였습니다. 라이트는 「비가법적 상호작용 때문에 지형은 **울퉁불퉁 다봉**, 그래서 골짜기를 건너는 drift가 필요」 라고 가정하고, 피셔는 「상호작용은 있지만 중요하지 않다, 지형은 거의 **단봉으로 매끄럽게 오를 수 있다**, 그래서 매스 선택으로 충분」 이라고 판단했다.

**이 epistasis/ruggedness의 축이, 바로 우리 결과가 살아 있는 차원입니다. 지형의 형태 (topology) 야말로 전 문제.** 지형이 정말로 울퉁불퉁 고차원이라면 (라이트 regime) 다양성이 골짜기를 건네주고, 매끄럽거나 난소가 저차원이라면 (피셔 regime) 매스 선택 ── 즉 **강한 랜덤 리스타트 산오르기의 생물학판** ── 으로 이미 충분. 우리의 ESN 텍스트 proxy는 noise-free로 매끄럽고, kernel union의 난소는 저차원 이산. **둘 다 피셔 regime**으로, ③은 효과가 없고 없었다.

> 세세한 주의 (정직하게): 「피셔는 drift를 무시했다」는 속설의 압축입니다. 정확히는 「drift는 있다고 인정했지만, 큰 집단에서는 양적으로 무시할 수 있다고 판단했다」. 완전 부정은 아니다.

### 9.3 우리의 negative = 코인 비판의 계산판

가장 효과적인 대응은, 라이트의 **제안**이 아니라, 생물학계의 **경험적 판정** 쪽입니다. Coyne, Barton & Turelli (1997, *Evolution* 51(3):643–671) 는 시프팅 밸런스 설을 이론・실증 양면에서 평가하고, 이렇게 결론지었습니다 (전문 대조 완료).

- **매스 선택으로 대개 충분.** 「라이트의 3단계 메커니즘이 단순한 매스 선택보다 더 잘 설명하는 실례는 거의 없다」. 인위 선택 실험도 「분할 집단의 선택이 대집단의 매스 선택보다 큰 응답을 낳는다」는 것을 보이지 못했다.
- **시프팅 밸런스가 효과를 내는 것은 한정적・희소한 조건 하에서만.** 집단 구조의 경험적 추정에서는 「**얕은 골짜기로 격리된 피크 사이에서만 drift는 이동을 일으킬 수 있다**」(깊은 골짜기는 drift로는 드물게만 건널 수 있다), 게다가 **대부분의 적응은 골짜기 건너기를 필요로 하지 않는다**.

이것은 우리 결과의 **놀랄 만큼 정확한 생물학판**입니다. 그들의 말을 우리의 어휘로 번역하면 ── **지형이 진정으로 기만적/고차원이 아니라면, 보통의 매스 선택 (≒ 강한 랜덤 리스타트 산오르기) 으로 이미 풀리고, 다양성 유지 장치는 거의 아무것도 사지 못한다.**「현실의 골짜기는 대개 얕다, 대부분의 적응은 골짜기 건너기 불필요」는, 우리의 「**실제 지형은 대개 단순하므로 niching은 잉여**」의 생물학적 언명입니다.

> **honesty 주의 (3점)**:
> 1. **그들은 시프팅 밸런스를 「반증」하지 않았다.** Phase I/II는 일어날 수 있다고 명언하고, 6건의 경험 사례도 들고 있다. 주장은 **더 좁은 확률적인 것** (「일반적・중요한 메커니즘이라 하기 어렵다」) 이지, 「refuted」 라고 쓰면 과언.
> 2. **논쟁은 아직 결착되지 않았다.** Wade & Goodnight (1998), Peck et al. (1998, 제목이 문자 그대로 「feasible」 이라 주장) 이 반론하고, Coyne 등의 2000년 재반론, Goodnight & Wade의 같은 호 반론으로 이어졌다. 1997 비판을 「최종 결론」으로 인용해서는 안 된다.
> 3. **생물에는 계산 측에 대응물이 없는 메커니즘이 있고, 게다가 우리보다 강한 주장을 하고 있다.** Phase III에서는, 다양성을 지키는 gene-flow 장벽이 **좋은 해를 주변 deme에 가둬 퍼짐을 방해한다** = niching이 **역효과**가 될 수 있다. 우리의 stateless한 이산 선택 설정에는 이 cost의 대응물이 없으므로, 여기는 **과도하게 겹치지 않는다**. 생물 쪽이 한 단계 강한 주장을 하는 곳입니다.

### 9.4 두 실례 — 저차원의 나방, 그리고 고차원의 대장균

우리의 주장에는 2개의 극 (저차원 = ③ 불필요 / 고차원 = ③이 효과를 낼 수 있다) 이 있지만, 진화생물학은 각각에 깔끔한 실례를 갖고 있습니다.

**저차원의 극 ── 회색가지나방의 공업 흑화 (= BG9 kernel 케이스)**: *Biston betularia* 의 carbonaria (검정) vs typica (흰색) 는 **단일 멘델 좌위・소수 대립유전자** (원인 변이는 cortex 유전자로의 전이인자 삽입; van't Hof et al. 2011/2016) 로, **강한 방향성 선택** (s ≈ 0.1-0.2; Saccheri et al. 2008; 포식은 Cook, Grant, Saccheri & Mallet 2012에서 재확인) 을 받는다. 최적은 각 시점에서 단봉, 환경으로 시프트할 뿐. **단순한 방향성 선택 ── greedy 산오르기/랜덤 리스타트의 생물학판 ── 이 직접, 적자형(適者型) 을 고정하고, 다양성 유지 메커니즘은 필요 없고 불려지지도 않는다.** 이것이 바로 BG9: kernel 선택은 4지선다의 저차원 단일 좌표이고, RR이 전 kernel을 직접 샘플링하며, ③이 구조적으로 분리할 수 없다. **흑화형 = BG9 kernel 케이스의 생물판.**

> 주의 (정직하게): 이행기에는 다형(多型) 이 일시적으로 유지되지만, 그것은 **공간적 환경 불균일 + 유전자 흐름 (이주-선택 평형)** 에 의한 것이지, 내재적인 다양성 보존 메커니즘이 아니다. 비유가 조금 어긋나는 곳.

**고차원・역사 의존의 극 ── 렌스키의 Cit+ (= ③ regime)**: 대장균 장기 진화 실험 (LTEE) 에서, 호기적 시트르산 이용 (Cit+) 은 **12 집단 중 정확히 1개**에서 약 31,500세대째에 진화했다 (Blount, Borland & Lenski 2008). 열쇠는 순서를 갖춘 **potentiation (전구 변이의 축적) → actualization (citT의 탠덤 중복에 의한 프로모터 포획) → refinement** 라는 고차원・역사 의존의 경로 (Blount et al. 2012). 리플레이 실험이 「역사적 우발성」을 「일정률의 희귀 변이」에서 구별했다. 이것은 contingency・에피스타시스・고차원 울퉁불퉁 지형을 탐색하는 가치를 **진짜로 예시**한다 ── ③이 효과를 낼 수 있는 regime의 실례입니다.

> **honesty 주의 (이것은 우리 조건문의 "전건"에만 대응한다)**:
> - **LTEE는 niching 알고리즘을 쓰지 않는다.** 그냥 자연선택이고, 12 병렬 집단은 **그 자체가 랜덤 리스타트적인 설계**. 그래서 「contingency + 다양성이 희귀한 혁신을 가능케 한다」는 존재 증명이지, 「niching이 강한 restart baseline에 이긴다」는 증거가 **아니다**.
> - 「대장균이 제로에서 시트르산을 먹는 능력을 획득」은 속설의 과장. 혁신은 **제어 (기존 트랜스포터의 호기 발현) = exaptation** 이지, 신규 유전자도 신규 생화학도 아니다.
> - Van Hofwegen et al. (2016) 이 「직접 선택이라면 Cit+가 훨씬 빨리 나온다」고 보이고, 「희귀/우발」 틀에 이의를 제기했다 (렌스키 측은 LTEE 조건 하의 potentiation과는 모순되지 않는다고 반론). 「극히 희귀/장기 지연」 이야기에 기대려면, 이 **계쟁 중인 추시(追試)** 도 병기해야 한다.

### 9.5 접지의 정리

| 극 | 생물학 | 지형 | ③은 효과? | 우리의 기질 |
|---|---|---|---|---|
| 저차원/매끄러움 | 흑화형 (단일 좌위, s≈0.1-0.2, 방향성) | 단봉・시프트 | **No** — 매스 선택으로 충분 | BG9 kernel union; ESN/ridge 텍스트 proxy (결정론・매끄러움) |
| 고차원/우발 | 렌스키 Cit+ (potentiation→actualization→refinement) | 울퉁불퉁・변이로 골짜기 넘기 | **Yes** (효과를 낼 수 있는 regime) | 합성 속임수 corridor (behavior = 24차원의 평균) |
| 경험적 판정 | 코인・바턴・투렐리: 매스 선택으로 대개 충분, 시프팅 밸런스는 드물게만 결정적 | 실제 지형은 대개 단순 | 우리의 **negative의 거울** | 시험한 모든 CPU 기질 |

**결론**: 라이트의 시프팅 밸런스는 「③이 효과를 낼 때 **왜** 효과를 내는가」의 올바른 생물학 선례, 라이트-피셔의 epistasis/ruggedness 축은 「**차원** 조건」의 올바른 틀, 흑화 나방과 렌스키 Cit+는 저차원/고차원의 깔끔한 양극, 코인 비판은 우리의 **negative**의 생물학 선례. **다만, 이것들은 계산 결과를 증명하지 않는다. 접지할 뿐.** 비유가 가장 느슨해지는 것은, 생물이 cost (Phase III의 gene-flow trap) 를 더하는 점 ── 우리의 stateless 설정에는 그것이 없다.

— 한 모금. 100년 전의 논쟁이 같은 형태라고 깨달았을 때는, 솔직히 소름이 돋았습니다. 다만 「소름이 돋았다」를 「증명」으로 헷갈리지 않는 것이 이번의 규율입니다. —

---

## 10. GPU로의 함의 — 남은 길은 고차원뿐, 그러나 여전히 bet

arc는 CPU의 길을 전부 막았습니다. 실제 proxy는 noise-free로 매끄럽고 (IV), 마지막 후보 (kernel 다양화) 는 구조적으로 막혔다 (V). ③의 남은 길은 **고차원의 지형뿐** ── 그것을 제공하는 것이 **full-LLM의 파라미터/손실 공간 (수백만 차원)** 입니다.

구조적 통찰은 GPU의 도박을 **better-motivated** 하게 만듭니다. 「full-LLM만이 예외일지도」 라는 맹목적인 도박이 아니라, 「**③은 고차원을 요하고, full-LLM이 고차원역**」 이라는 원리에 따른 도박이 된다.

**다만 여전히 bet.** 생물학의 Cit+가 「③ 알고리즘의 승리」를 증명하지 않는 것과 같은 이유, 그리고 BG9에서 RR에 못 이긴 것과 동형의 이유로 ── **실제 LLM 지형이 backprop (경사 하강) 이라는 강 baseline으로 직접 내비게이트할 수 있다면, ③은 역시 불필요**. 난소가 고차원인 것은 **필요조건이지 충분조건이 아니다**. 「강한 직접법이 풀 수 없다」는 것을 추가로 보일 필요가 있다 (CPU에서는 RR, GPU에서는 경사 하강).

그래서 GPU는 「③을 위해 단독」이 아니라 **포트폴리오 판단** (llive의 실제 LLM fitness 등과 합승) + **클라우드 임차로 사전 등록 1건** (자본 커밋 전) 이 적정. go/no-go 기준도 falsifiable하게 쓸 수 있습니다:

> **full-LLM의 난소는 behavior에서 고차원인가, 또한 강한 직접 baseline (경사 하강) 으로 도달 곤란한가?** 고차원이라도 경사가 직접 닿는다면 ③ 불필요 (= BG9의 RR 결과의 GPU판).

---

## 11. 메타 교훈 — 정직함은, 이기기 위한 도구였다

이 arc의 진정한 성과는 수치가 아니라, **「너무 정돈된 결과를 의심하는」 정신이 실제로 연구를 앞으로 진전시켰다**는 것입니다.

- **존재 증명 (I)** 에서 이겼을 때, 골짜기를 없앤 경계 실험으로 「③은 만능이 아니다」를 스스로 확인했다 (승리를 과대평가하지 않는다).
- **일반화 (III)** 에서 페어 리뷰가 3개의 rerun 블로커를 들이댔지만, 고쳐도 결론은 바뀌지 않았다 (취약한 negative가 아님을 확인).
- **결정론 측정 (IV)** 에서 평가 노이즈를 물리적으로 지웠기에, 「매끄러움」이 지형의 성질인지 계기의 한계인지를 가려낼 수 있었다.
- **BG9 (V)** 에서는 적대 검증으로 자신의 「③이 안 선다」를 **반증하려 해서 반증할 수 없었고**, 구조로서 확증되었다 (negative를 올바르게 negative로 확정하는 방향으로도 같은 규율이 효과를 발휘했다).

게다가 arc 전체에서 하나 배운 것은 ── **저차원의 난소는 강 baseline이 직접 풀어 버린다. 그래서 ③ (가려내어 길러 내는 공정) 이 효과를 내려면 "고차원 behavior 공간"이 필요하다.**「속임수 지형을 만들면 ③이 선다」는 절반만 옳고, 정확히는 「**직접 샘플링할 수 없을 만큼 고차원인** 속임수 지형」이 아니면 ③은 서지 않는다. 그리고 놀랍게도, 이 경계 조건은 **라이트의 시프팅 밸런스와 코인 비판이 100년 가까이 전에 도달해 있던** 것이었습니다.

「이상하게 좋은 결과가 나오면, 이긴 기분이 되기 전에 반드시 내역을 의심하라」── FullSense의 연구 규율 (`honest disclosure`) 은, 단순한 자계(自戒) 가 아니라, **실제로 거짓 양성을 잡고, negative를 올바르게 확정하며, 연구의 정밀도를 높이는 메커니즘**으로서 6단 전부에서 돌고 있었습니다.

결론을, 마지막에 다시 한 번, 정확하게.

> **③이 살아나는 것은 「고차원의」 속임수 지형일 때뿐.** 존재 증명 (합성 corridor) 에서는 압승했지만, 실제 CPU 기질은 ── 기억 과제 (바닥/천장) 도, 다중 과제 일반화 (매끄러움) 도, 실제 proxy 텍스트 지형 (noise-free로 매끄러움) 도, kernel 다양화 (저차원・구조적으로 막힘) 도 ── 어느 것도 그 조건을 충족하지 않았다. **「③ 결착 = ③은 불필요로 판명」이 아니라**, 「③이 살아나는 조건 (고차원의 속임수 지형) 을, 지금 CPU에서 측정할 수 있었던 실물 모형은 충족하지 않았다」. 본진 (GPU 고차원) 은 아직 앞이고, 게다가 「강한 직접 baseline이 푼다」는 리스크를 안은 도박입니다. 그리고 이 결론의 골격은, 20세기의 진화생물학이 이미 그리고 있었습니다 ── 다만 생물학은 그것을 **증명하는 것이 아니라, 접지할 뿐**입니다.

---

**Tags**: 진화계산 / MAP-Elites / 통계검정 / honest disclosure / 진화생물학 / CPU 연구
**관련**: 연재 #33 (제3축 ③ 결착 Step D + BG9) / #32 (llcore CPU PoC battery) / #29 (반증・Goodhart・proxy 한계)
**Project**: llcore (PyPI 예약 llmesh-llcore, 리포지토리 미공개이므로 로컬 연구)
