---
title: "llcore — 「進化で AI を設計するとき、選り分けて育てる工夫は本当に要るのか?」を 3 実験で詰めた話 (第三軸 ③ 決着 Step D)"
tags: ["Python", "進化計算", "MAP-Elites", "honest disclosure", "統計検定"]
private: true
updated_at: "2026-06-02"
id: 21d6c4dcfde204062a89
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# (連載 #33) 整いすぎた結果は、勝ちではなく警報 — 第三軸 ③ を proper power で決着させた一日

## TL;DR

- 問いは **「AI のコア計算を進化で探すとき、"選り分けて分けて育てる工夫" (= 進化の③ 適者生存/分離) は本当に要るのか」**。
- **合成した "谷つき (欺瞞) 地形" では③は圧勝** (過去実験で Cliff δ=+1.0)。③ は機構として本物。
- **だが実物に近い CPU proxy 地形を、評価ノイズを物理的にゼロまで落として測り直したら "本当に滑らか (単峰)" で、③ は不要と確定**。「過去の negative は検出力不足 (underpower) ではなく、地形が本当に滑らかだった」が初めて裏付いた。
- 実 multitask 近傍 (C-gen4b) だけ「③ NOT null」の弱い気配が出たが、データを増やすとフラついて **候補止まり** (走行内ドリフト + 多重比較で脆い)。
- 「ある後処理が③を隠している」疑い (K4 ridge clip) は、外したら逆に悪化 → **隠していない、診断的所見に降格**。
- 外部レビュー (Codex) は **ブロッカーなし**で結論を追認。
- 結論を一行で: **「③ が活きるのは地形が欺瞞的なときだけ。今 CPU で測れた実物もどきは、たまたま滑らかだった」**。本丸の決着は GPU (実 LLM 地形) が要るが、それは投資判断。
- **追記 (2026-06-02, §11.5)**: 最後の CPU 抜け道 **kernel 多様化 (BG9) は構造的に閉じた**。kernel 選択は低次元ゆえ強 baseline (RR) が直接サンプルし、③ の niching 優位が原理的に出ない。**③ が効くには "高次元の" 欺瞞地形が要る**と分かり、残る路は GPU full-LLM のみ (それも bet)。
- メタ教訓: **正直さ (honest disclosure) は飾りではなく、研究を前に進める道具だった**。BG9 では「negative を正しく negative と確定する」方向でも同じ規律が効いた。

> ⚠ この記事の数値は、すべて手元 (ローカル) の研究 commit `THIRD_AXIS_SETTLE_VERDICT.md` に紐づく実測です。llcore はまだ公開リポジトリを作っていないので、外部リンクは貼れません。代わりに「どう測ったか」を本文に全部書きます。

---

## 0. この記事は何の話か (コンセプト)

`llcore` は「Transformer のコア計算 (状態更新則・学習則・認知駆動 Δ) を遺伝子にして、Z3 で壊れないように検証しながら進化させる」CPU 完結の研究フレームワークです (連載 #32 で PoC battery の話を書きました)。

その進化エンジンには、進化の 4 要素のうち **③ (適者生存 selection / 分離 separation)** をどう効かせるか、という設計上の急所があります。多様性を保ってニッチに残す MAP-Elites のような「選り分けて分けて育てる」仕組みです。

問いはシンプルです。

> **その③、本当に要るの?**

要るなら、③ を載せるための重い投資 (最終的には GPU で実 LLM を回す) に意味がある。要らないなら、③ にこだわるのは時間と電気の無駄になる。

この一日 (2026-06-02) で、その問いに **3 つの実験で正面から決着をつけにいきました**。タイトルどおり、結論は「整いすぎた結果は警報」という FullSense の通奏低音に、もう一度引き戻される話です。

— ここまで 30 秒。準備運動おわり。本題へ。 —

---

## 1. たとえ: 山登りと、だまし地形

数式の前に、地形のたとえで全体像を掴みます (この研究で一貫して使っているメタファーです)。

設計の良し悪しを **地形の高さ** で表します。**高い場所 = 良い設計**。一番高い頂上を探すゲームです。

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

このとき効くのが③ の発想です。**いろんなタイプの登山者を谷のあちこちに残しておく** (= 記憶の宮殿 / MAP-Elites archive)。誰かが谷を「飛び石」で渡って本物の頂上に到達できる、という仕組みです。

**この研究の核心を一言で**: ③ が本当に役立つのは **「だまし地形」のときだけ**。滑らかな一つ山では、③ は無用の長物です。

だから問いは、こう言い換えられます:

> **「進化で AI を設計するとき、実際に出くわす地形は "だまし地形" なのか、それとも "滑らかな一つ山" なのか?」**

これが決まれば、③ が要るか要らないかが決まる。今日はこれを測りました。

---

## 2. 過去の積み残し — 「③不要」は本当に "不要" だったのか

これまでの実験 (Step C → 梯子段1 → E-A → 谷深さ実測) を通じて、像はだいたいこうでした。

- **合成した欺瞞 corridor では③が圧勝** (3 つの baseline 全てに勝ち、Cliff δ=+1.0)。③ は存在証明済み、機構として本物。
- **実問題に近い proxy 地形では③ negative** (MAP-Elites が random にしか勝てない = 滑らかな地形と同じ症状)。

ところが、ここに 2 つの未解決のしこりが残っていました。

1. **「③不要」は本当に "地形が滑らか" だからなのか、それとも単に "サンプル数が足りなくて差を検出できなかった (underpower)" だけなのか?** ── これを取り違えると、「③ は無力」という過剰一般化をやらかす。
2. 谷深さの直接測定は前回 **N/A (測定不能)** で終わっていた。評価ノイズが谷の深さより大きくて、谷があっても埋もれて見えない、という計器の限界。

つまり「滑らかに見えた」のが **地形の性質** なのか **計器の限界** なのか、決着がついていなかった。ここを詰めるのが Step D です。

— 小休止。ここまでが前提。ここから先が今日やった 3 実験。 —

---

## 3. 実験の設計 — 3 本立て

| 実験 | 何を測るか | 狙い |
|---|---|---|
| **EXP1** | proper-n 再検定 | サンプル数を本気で増やして、③ の効果が本物か検出力で詰める |
| **EXP2** | 決定論 C1 多峰性 | 評価ノイズを物理的にゼロにして、地形が「だまし地形」か「滑らかな一つ山」かを noise-free で判定 |
| **EXP3** | K4 ridge clip の verdict-flip | 「ある後処理が③を隠している」疑いを検証 |

規律: 全部 `research/step_d_settle/` に隔離、src は無改変、git はオーケストレータが一括。各実験は破綻ゲート (G1 CPU 完走 / G2 再現性 / G3 診断器妥当 / G4 src 不変) を通す。

---

## 4. EXP2 が決め手だった — 評価ノイズをゼロにすると地形が見える

順番は前後しますが、**一番効いたのは EXP2** なので先に書きます。

前回の谷深さ測定が N/A になった原因は単純で、**「谷の深さ (0.05·|fitness| くらい) ≪ 評価ノイズの揺らぎ」** だったからです。計器のノイズに谷が埋もれて、あるのかないのか分からない。

EXP2 のトリックはこうです。

> ESN reservoir (固定 seed) + ridge readout の closed-form (`np.linalg.solve`) は、**乱数を一切引かない**。だから評価ノイズを機械イプシロン (約 1.11e-16) まで物理的にゼロ化できる。

実測で `eval_noise_std ≤ 1.11e-16` を確認しました。これは「評価のたびに値がブレる」のではなく、浮動小数点の最小単位 (ULP) 由来の誤差で、**実質ゼロ**です。ノイズの霧が完全に晴れた状態で、地形の谷を直接測れる。

結果がこれです (valley_fraction = 谷の割合、大きいほど多峰=だまし地形):

| landscape | 種別 | 次元 | valley_fraction (mean/max) | 多峰? | 判定 |
|---|---|---|---|---|---|
| **ESN_3param** (実 proxy) | real | 3 | **0.000 / 0.000** | **False** (3 seed 一致) | 滑らか=単峰 → ③不要を noise-free で確定 |
| **ESN_perneuron40** (実 proxy) | real | 40 | **0.096 / 0.121** | **False** (3 seed 一致) | smooth 寄り (床 0.2 未満) → ③不要 |
| ctrl_multipeak_dim3 (正 control) | control | 3 | 0.701 / 0.727 | True | 診断器は多峰を検出できる ✓ |
| ctrl_multipeak_dim40 (正 control) | control | 40 | 0.795 / 0.818 | True | 診断器健全 ✓ |
| ctrl_quadratic_dim3 (負 control) | control | 3 | 0.000 | False | 診断器は滑らかを検出できる ✓ |
| ctrl_quadratic_dim40 (負 control) | control | 40 | 0.000 | False | 診断器健全 ✓ |

ポイントは 3 つ:

1. **実 proxy 地形 (3 次元 / 40 次元 とも) は valley≈0 = 単峰**。3 seed で完全一致。
2. **診断器そのものは健全**。わざと作った多峰の正 control はちゃんと多峰 (0.70/0.80) と検出し、二次関数の負 control はちゃんと滑らか (0.0) と検出する。だから「実 proxy が単峰」は計器のバグではなく地形の性質。
3. これで **「過去の③ negative は underpower ではなく、地形が本当に滑らかだったから」** が、実 substrate 上で初めて noise-free に裏付いた。

副次発見も正直に書いておきます。**正 control に使うつもりだった欺瞞 corridor (`make_corridor_eval(d=0.16)`) が、決定論化したら valley=0.0 (単峰判定)** になってしまった。corridor の欺瞞性は「単一 basin の中に閉じ込めて③の behavioral niching で脱出させる」型 (behavioral-reach 欺瞞) であって、**地形の谷 (C1 multi-basin) の欺瞞ではなかった**。corridor は C1 の正 control にならない、という scope の狭まりを実測で確定しました。これは過去の谷深さ校正が「corridor 由来の閾値」を地形多峰性に転送できないことを意味します。

— ここで一服。「正 control が control にならなかった」のは地味にショックでした。が、これも測ってみないと分からなかった。 —

---

## 5. EXP1 — 実 multitask 近傍だけ「③ NOT null」の弱い気配

次に、実問題に一番近い帯 (C-gen4b = MAP-Elites vs random、実 multitask 近傍) を、サンプル数を本気で増やして再検定しました。

| case | 元 n=15 (監査) | fresh 真再走 | 判定 |
|---|---|---|---|
| **C-gen4b** | diff +0.063 / psd +0.20 / p 0.126 | **n=64: diff +0.0472, 片側 p 0.038, psd +0.188, gate PASS** | **③ load-bearing 候補 (still_inconclusive)** |

fresh seed で n=64 まで回したら **strict gate を 4 条件すべて PASS** しました。つまり監査が「③不要 (inconclusive)」と読んだのは方向としては誤りで、**C-gen4b では③は NOT null の方向**。

…と、ここで勝った気にならないのが今回のキモです。3 つの理由で **候補止まり** にしました。

1. **更新後の検出力 power@n64 = 0.517 < 0.80**。gate は通ったが、確証の基準 (検出力 0.80) には足りていない。
2. **走行内ドリフト (これが効いた)**。累積 p 値の軌跡を追うと: n=40 で初 PASS (p=0.042) → n=60 で p=0.010 と深く有意化 → **n=64 で p=0.038 へ 0.05 境界近くへ戻った**。さらに seed を前半/後半で割ると、**前半 32 seed は diff=+0.0755 (frac_pos=0.625) だが、後半 32 seed は diff=+0.0189、最後の 9 seed は diff=−0.0376 (負)**。PASS は前半 seed に支えられていて、**新しいデータほど逆方向に走っている**。
3. **多重比較**。p=0.038 は α=0.05 では PASS だが、EXP1 の 3 case だけでも Bonferroni α=0.0167 を超過 (FAIL)。③ research family 全体で見ればもっと厳しい。

加えて、効果量の床 (psd) が **構造的天井** にぶつかっていました。C-gen4b の median psd は n=15→0.200, n=255→0.200 で動かない。`P(|psd|≥0.147)` (効果量条件の充足率) は n=255 でも 0.794 で頭打ち。中効果 (psd≈0.20) なので、サンプルをいくら増やしても full gate の検出力が 0.80 を超えない。**つまり「サンプルを増やせば (A) 確定する」という見込み自体が、この proxy 上では薄い**。

結論: **C-gen4b は「③ load-bearing 候補 / still_inconclusive」**。「③ NOT null」という headline は、単発の境界 p=0.038 に寄りかかりすぎ。走行内ドリフトは「候補が偽陽性かもしれない」真の証拠です。

---

## 6. EXP3 — 「後処理が③を隠している」疑いは、外したら逆に悪化した

最後の疑いはこうでした。「ridge readout の clip (K4) という後処理が、実は③の信号を握りつぶしているのでは?」 もしそうなら、clip を外せば③が浮かび上がるはず。

外してみました。

| task | clip | MAP-E mean | baseline 勝数 | verdict_flip |
|---|---|---|---|---|
| **addition** | True | +0.0100 | 1/3 | — |
| **addition** | False | **−1.212** | 0/3 (全悪化) | **False** |
| **flip_flop** | True | +0.426 | 0/3 | — |
| **flip_flop** | False | +0.438 | 0/3 | **False** |

clip を外したら、③が浮かび上がるどころか **addition で MAP-Elites が +0.010 → −1.212 に劣化**。clip=False は raw R²<0 のノイズ領域 (15/15 seed が負、R² が [−3.68, −0.20]) に MAP-Elites を落とし、構造を回復するどころか悪化させた。**= 「clip が信号を隠している」仮説を能動的に反証**。

null-ridge FPR (gene 非依存 target = 真の帰無仮説) も clip True/False で差ゼロ (両方 0.0)。

判定: **K4 は「唯一の能動的 suppression 機序」ではなく、「spread を潰すが verdict を変えない診断的所見」に降格**。これで過去の統計監査が断定していた「K4 = 唯一の能動的 suppression」は過大だったと判明しました。

正直な留保 (§6.3 相当): null-FPR=0/0 は null_seeds=4 のみの床値だし、この実験は予算を約 7 倍縮小しています。だから verdict のラベルは「null 確定」ではなく **「not_load_bearing_at_this_budget (この予算では非載荷)」** に統一しました。「null を確定した」より「この予算では K4 が load-bearing でない」が正確だからです。判定の実体 (診断的所見への降格) は不変で、語の精度だけ上げています。

— ここで深呼吸。3 実験おわり。次は「言い過ぎていないか」の自己点検。 —

---

## 7. Surviving refutation — 3 つのレンズで自分の結論を殴ってみた

honest disclosure の核は「自分の結論を一番きつく疑う」ことなので、3 つの独立な反証レンズを当てました。**3 つとも `refuted=true / medium` で生き残った**、つまり保守的な verdict は覆らないが、positive 寄りの強調は弱める方向で効いています。

1. **[power_adequacy] C-gen4b の gate PASS は optional-stopping + 多重比較で脆い**。上の §5 のドリフトと Bonferroni FAIL がこれ。「③ NOT null」を headline にするのは境界 p に寄りかかりすぎ。→ p の n 軌跡と後半 seed の符号反転を開示フィールドに記録済。
2. **[determinism_and_circularity] 単峰 verdict は閾値近接で脆い**。決定論化と非循環性そのものは clean (behavior と fitness の相関は ≈0、診断器は behavior 記述子を使わず地形幾何を直接見る)。ただし ESN_3param の midpoint の **90.9% が下方に dip** していて、最大相対 dip=0.0435 は C1 谷閾 0.05 の直下 (13% 以内)。だから精密に言うと「**真に単峰**」ではなく「**C1 閾値を僅かに下回る浅い谷 (~2–4%) を持つ弱 multi-basin**」。(B) null の方向は維持されるが、頑健性は閾値近接ゆえ限定的。
3. **[clip_flip_validity] K4 降格は低予算ゆえ "at this budget" 限定**。verdict_flip=False は確かだが、FPR 0/0 は床値、予算は 7 倍縮小。だから「firm refutation」より「not load-bearing at this budget」と述べるべき。

3 つとも「結論をひっくり返す」ほどではないが、「言い過ぎを削る」方向で全部効いた。この自己監査こそ今日の成果の半分です。

---

## 8. 自分が踏んだミスを 1 つ正直に書く

前回の谷深さ workflow で、2 段目のオーケストレータ briefing に **stale (古い) な値** を渡してしまいました。「全 below threshold / d*=0.1234」みたいな値です。ところが実際に commit されている結果 JSON は `all_below_threshold=false` でした。前回の workflow 結果を読んだとき、別のメトリックの値を取り違えていたのです。

これを **敵対検証が検出して、verdict を N/A に格下げ**しました。つまり「整いすぎた結論」を自分で疑うプロセスが、自分のコピペミスを捕まえた。気持ちのいい話ではないけれど、これが回ったから今日の Step D で正しい足場から測り直せた。

honest disclosure は「失敗を消さない」だけでなく、「**失敗を検出する仕組みを先に置いておく**」ことなんだな、と改めて思いました。

---

## 9. 過去 verdict をどう更新したか

| 過去 verdict | 過去の読み | Step D の更新 |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **方向更新: ③ は NOT null の方向 (fresh n=64 で gate PASS)**。ただし候補止まり |
| step6 exp7 (実 ESN proxy, ③ negative) | n≤10 盲点域, 「再測必須」 | **大幅更新: 地形が本当に滑らか (③不要) を noise-free で確定**。再測しても多峰は出ない |
| 谷深さ N/A (計測不能) | instrument 不能 | **解消: 決定論化で計測可能化** → vf≈0 (単峰)。ただし閾値近接の浅い谷が留保 |
| K4 clip = 唯一の能動的 suppression | 「clip が landscape 構造を隠蔽」 | **降格: 診断的所見** (not_load_bearing_at_this_budget) |

「③不要に見えた過去 negative の多くは underpower ではなく、地形が本当に滑らかだった」── この一点が、実 substrate 上で初めて確かめられたのが今日の核です。

---

## 10. 外部レビュー (Codex) はブロッカーなしで追認

llcore の規律として、各 capstone は Codex (gpt-5.4, read-only) のペアレビューを通します。今回の総評は **「ブロッカーなし ── ③ 結論を外部確認」**。

- C-gen4b を load_bearing でなく候補止まりにした判断は妥当 (更新検出力 0.5174 < 0.80 を JSON で確認)。
- EXP2 の決定論・非循環は clean。「真に単峰」より「閾値下の弱 multi-basin」が精密、という本文の自認も追認。
- EXP3 の K4 降格は現予算なら妥当 (FPR 0/0 + 7倍縮小ゆえ at-this-budget 限定)。

指摘された 4 件 (CF1〜CF4) は **すべて将来 rerun 時の harness 堅牢性と文言精度** であって、現結論を覆すものではありません。GPU で③を再検定するとき、これらを適用してから harness を再利用します。

---

## 11. CPU の抜け道 (kernel 多様化 / BG9) を試していた

「③ の本丸は GPU (実 LLM の損失地形) へ」が EXP2 の推奨です。実 proxy が滑らかと確定した以上、滑らかな地形で③を追っても (A) は出ない (地形が一つ山なら選り分けに利得がないのは当然)。

ただし GPU は投資判断なので、**CPU で前進できる別仮説**を並行して試していました。それが **kernel 多様化** です。

仮説はこうです。個々の kernel (rwkv / mamba / hopfield / linear_attn) が滑らかでも、**4 種類の kernel 族を union すると、kernel 切替の瞬間に fitness が不連続に段差を作る → 地形が multi-basin (だまし地形) になりうる → ③が GPU なしで CPU 上で load-bearing になりうる**。これを検証するのが BG9 でした。

この記事を最初に書いた時点では「いま BG6 (task → best-kernel 写像が非定数か、つまり「タスクごとに得意 kernel が違うか」) を smoke 測定しているところ」でした。その後 (同じ 2026-06-02 中に) BG9 の決着がつきました。次の追記節がその結末です。

---

## 11.5. 追記 (2026-06-02): BG9 決着 — 抜け道は構造的に閉じていた

> 結論を一行で: **BG9 = N/A (構造的)。つまり kernel 多様化という CPU 抜け道は「③ が立たないことが構造的に決まっている」ので閉じた。** 「③ が要らない」ではなく「この空間では③が強 baseline と原理的に分離できない」という、情報量のある negative です。

§11 で仕掛けた抜け道の結果が出ました。期待した「kernel union で multi-basin (だまし地形) が生まれて③が CPU で立つ」は **起きませんでした**。しかも「たまたま立たなかった」のではなく **構造的に立てない** ことが分かった。BG9 はこれを 3 段の証拠で確定しています。

### (1) substrate validity — 「弁別はあるが弱い」(PASS だが要注意)

まず「タスクごとに得意 kernel が違うか」(BG6) を、kernel-favoring task 群を第一原理で設計し直して測ったところ、写像は **非定数 = 非 inert (PASS)**。mamba / linear_attn / rwkv はそれぞれ別タスクで best になりました。BG6 で踏んだ「memory_tasks は kernel 中立」の轍は回避できた、という意味では前進です。

ただし正直に言うと **弱い**:

- **hopfield はどのタスクでも勝てなかった**。これは hopfield kernel が **対角スカラ mock** で、tanh アトラクタが機能不全だったため (per-seed の R² が 0/0.99/0 と二極化)。つまり実質「4 kernel union」ではなく **3 kernel** です。
- clean な専門化は 2 軸のみ (selective_copy↔mamba / weighted_accum↔linear_attn)。残りは margin が薄く fragile。

→ **弁別の存在 ≠ 多峰/障壁**。non-inert 化には成功したが、それが欺瞞地形 (だまし地形) を保証するわけではない、という所まで。なお対角 mock の限界は kernels.py のスコープ宣言どおりで、ここでは **機構の feasibility のみ主張** (full kernel 性能は非主張) です。

### (2) harness validity — positive control が validate しない (これが決め手)

次が本丸です。固定パラメータ (behavior=(kernel_id, theta L1)) で MAP-Elites (③) を、3 つの baseline ── **RR-hillclimb (random restart 山登り)** / panmictic-GA / random ── と honest に paired 比較しました。

| 基質 | 結果 |
|---|---|
| **positive control** (合成 kernel-barrier) | ③ は panmictic (+0.423) と random (+0.208) は撃破。**だが RR には勝てない** (+0.051, p=0.31 → FAIL)。3 baseline 全勝に届かず = **harness validity が立たない** |
| **negative control** (kernel 中立タスク) | 全 method R²≈1.0 飽和、③ 優位なし = **正しく null** (false-positive なし、計器は健全) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3、panmictic が逆に③を上回る = **③ 勝たず** |

ここが Step D (技術版 §4-7) と決定的に違う点です。Step D の欺瞞 corridor では③が RR を排除できました。**なぜ kernel 空間ではできないのか?** 根因は 1 つ:

> **RR は restart のたびに kernel_id ∈ [0,4) を直接サンプルできる。** kernel 選択は 4 離散の単一座標 (低次元) なので、RR は restart で全 4 kernel を直撃する。「best kernel を探す」のに谷を跨ぐ必要がない = **teleport (直接ワープ)**。だから③ の behavioral niching に出番が来ない。

Step4 の corridor で③が RR を排除できたのは、そこの behavior が `mean(24次元)` で、CLT により平均が 0.5 に集中 → 大域ピークが measure-zero 域 = **random/RR が直接サンプルできない高次元**だったからです。kernel_id は逆に低次元で直接サンプルできてしまう。

### (3) red-team — 敵対検証でも反証できず、むしろ確証

「harness が立たないのは本当に構造のせいか? たまたまの設定ミスでは?」を独立 red-team で叩きました。結果は構造主張を **反証できず、むしろ強化**:

- **機構確証**: instrumented RR が positive control 上で 4 basin に restart kid を [12,18,16,18] とほぼ一様分散、target 到達 88%、best は restart→in-basin climb が 6/8 seed。「RR は restart で kernel_id を直接サンプルして谷を回避する」を **数値で確証**。
- **4 つの faithful 構成 (高次元 theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin) すべてで③は RR に勝てない (beats_rr=False)**。corridor を緩めると RR も同等到達、締めると③が **先に starve** (餓死)。
- **境界 sweep**: theta corridor の次元を D=0→3 と締めるほど③が RR より速く starve (D=3: ③ reach 0.08 vs RR 0.42)。base_seed 3 通りで同一。

→ **「RR だけ排除して③が通る behavior 次元は、kernel 空間に構造的に存在しない」** を定量確証。

### 構造的洞察 (この決着の payoff)

> **③ (MAP-Elites の behavioral niching) が強 baseline を上回るのは、「難所」が高次元 behavior 空間にあって直接サンプリング (random restart) で到達できないときだけ。**

- **kernel 選択は低次元 (4 離散の単一座標)** → RR が直接サンプル → ③ の niching 優位が原理的に出ない。
- theta 空間に欺瞞を移しても、RR は restart 後に in-basin で greedy climb するので、corridor を RR が抜けられない程度に締めると③も同程度に starve する。**RR fail ∧ ③ succeed の窓が存在しない。**

これは Step4 §7 で残った問い「探索空間を kernel 多様化で拡張すれば③が unlock するか?」への答えです。答えは **NO (CPU では構造的に)**。拡張が③を unlock するには、追加した自由度が **高次元で直接サンプル困難**な behavior を生む必要がある。kernel 選択 (低次元・離散) はその条件を満たさない。

### GPU への含意

- **CPU 出し切りゲートが CLEAR**: BG9 が最後の CPU 路 (kernel-union) を構造的に閉じた。③ の残り路は **高次元の GPU full-LLM 損失地形のみ**。
- 構造的洞察は GPU の賭けを **better-motivated** にします。③ は高次元 behavior で初めて意味を持つ。full-LLM のパラメータ空間は数百万次元 = まさに高次元。だから GPU 検定は「full-LLM だけが例外かも」という弱い賭けでなく「③ は高次元を要し、full-LLM が高次元域」という原理に沿う。
- **ただし依然 bet**: 実 LLM 地形が backprop 系の強 baseline で直接ナビゲートできるなら③不要 ── これは **BG9 の RR と同型のリスク**です (「強 baseline が直接解く」可能性は GPU でも残る)。だから GPU は「③のため単独」でなく **ポートフォリオ判断** (llive 実 LLM fitness 等と相乗り) + **クラウド借りで事前登録 1 本** (資本コミット前) が適正。BG9 の構造的洞察そのものが GPU の falsifiable な go/no-go 基準になります:「③ が full-LLM で load-bearing なら、その難所は高次元 behavior 空間にあり直接サンプル/backprop で到達困難なはず」。

### honest 留保 (重要)

- これは **「③不要と判明」ではありません**。「③ がこの低次元 kernel 空間では強 baseline と原理的に分離できない」= N/A (構造的) であって、③ の機構自体は Step4 で本物と確定済みです。N/A だが「kernel 路は閉じている」という決定的情報を持つ **情報量のある N/A** です。
- harness/red-team は smoke 規模 (5-12 seed)。本検定 15 seed では数値は動くが、**構造 (締めると③が先に starve / RR が kernel_id を直接サンプル) は seed 非依存で頑健**。real の full ≥15-seed 本検定は実施しません ── positive control validity が構造的に立たない以上、real で③不要が出ても「③不要 vs 検出器盲」を分離できず、その「検出器盲 = kernel 空間の構造」を red-team が既に確定したので、CPU を 7.5h 投じても結論は変わらないからです。
- substrate は弱い (実質 3 kernel、**hopfield は対角 mock で機能不全**)。より強い kernel 弁別 (full 実装・非対角) なら別結論の余地は **理論上**あるが、③ の構造的障壁 (低次元選択 → RR 直接サンプル) は kernel 実装の質と独立です。
- 「整いすぎた③成立」を疑う規律は今回は **不要でした** ── ③成立は最初から出ていない (honest prior 通りの negative)。

---

## 12. メタ教訓 — 正直さは、勝つための道具だった

今日の本当の成果は数値ではなく、**「整いすぎた結果を疑う」精神が実際に研究を前へ進めた**ことです。

- 評価ノイズを物理的に消した (EXP2) から、「滑らか」が地形の性質か計器の限界かを切り分けられた。
- 敵対検証 3 レンズを当てたから、「③ NOT null」を headline にせず「候補」に留められた。
- 自分の stale 値の取り違えを自己検出したから、N/A という正しい格下げができ、今日測り直せた。
- **BG9 (追記) でもう 1 つ学んだ**: **低次元の難所は強 baseline が直接解いてしまう。だから③ (選り分けて育てる工夫) が効くには "高次元 behavior 空間" が要る。** 「だまし地形を作れば③が立つ」は半分しか正しくなくて、正確には「**直接サンプルできないほど高次元な**だまし地形」でないと③は立たない。kernel 4 択 (低次元) では、RR が restart で全部直撃するので③の出番が原理的に来なかった。これは抜け道を「諦め」でなく「**構造的に閉じた**」と言い切れる根拠です。

「異常に良い結果が出たら、勝った気になる前に必ず内訳を疑う」── FullSense の研究規律 (`feedback_benchmark_honest_disclosure`) は、ただの自戒ではなく、**実際に偽陽性を捕まえて研究の精度を上げる機構**として回っていました。BG9 はその逆方向 (**negative を正しく negative と確定する**) でも同じ規律が効いた例です ── red-team で自分の「③ が立たない」を反証しようとして、反証できずに構造として確証された。

結論を、最後にもう一度、正確に (BG9 決着を反映):

> **proxy substrate 上では「③ は地形が真に滑らかゆえ不要」が noise-free に確定**した (Step D)。実 multitask 近傍 (C-gen4b) でだけ「③ NOT null」の弱い兆候が出たが、小効果 + ドリフト + 多重比較で **候補止まり**。K4 clip は能動的 suppression でなく診断的所見に降格。そして CPU の最後の抜け道 **kernel 多様化 (BG9) は構造的に閉じた** ── kernel 選択は低次元ゆえ強 baseline (RR) が直接サンプルし、③ の niching 優位が原理的に出ない。**③ の本丸検証に残された路は、高次元の GPU full-LLM 損失地形のみ** (それも「強 baseline が直接解く」リスクを抱えた bet)。

「③ 決着 = ③ は不要と判明」ではありません。正しくは **「③ が活きるのは "高次元の" 欺瞞地形のときだけ。今 CPU で測れた実物もどき (滑らか) も kernel 多様化 (低次元) も、その条件を満たさなかった」**。本丸 (GPU 高次元) はまだ先で、しかも保証のない賭けです。

---

**Tags**: 進化計算 / MAP-Elites / 統計検定 / 検出力 / honest disclosure / CPU 研究
**関連**: 連載 #32 (llcore CPU PoC battery) / #29 (反証・Goodhart・proxy 限界) / #31 (Codex 二本柱)
**Project**: llcore (PyPI 予約 llmesh-llcore、リポジトリ未公開のためローカル研究)

---

# English

# (Series #33) An Over-Tidy Result Is Not a Win, It's an Alarm — The Day We Settled Third Axis ③ with Proper Power

## TL;DR

- The question is **"When you search for the core computation of an AI by evolution, is the 'sort-and-separate-and-raise' device (= the ③ survival-of-the-fittest / separation factor of evolution) really needed?"**
- **On synthetic "valley-laced (deceptive) terrain," ③ wins by a landslide** (Cliff δ=+1.0 in past experiments). ③ is genuine as a mechanism.
- **But when we re-measured the more-realistic CPU proxy terrain after physically driving the evaluation noise down to zero, it turned out to be "truly smooth (single-peaked)," and ③ was confirmed unnecessary.** For the first time we backed up the claim "the past negatives were not from underpower; the terrain really was smooth."
- Only the real-multitask neighborhood (C-gen4b) showed a faint hint of "③ NOT null," but when we added data it wobbled and stayed **a candidate at best** (within-run drift + fragile under multiple comparison).
- The suspicion that "some post-processing is hiding ③" (K4 ridge clip) — when removed, things got *worse* instead → **it isn't hiding anything; demoted to a diagnostic observation.**
- The external review (Codex) confirmed the conclusion **with no blockers.**
- The conclusion in one line: **"③ pays off only when the terrain is deceptive. The realistic-ish terrain we could measure on CPU just happened to be smooth."** Settling the main battle requires GPU (real-LLM terrain), but that is an investment decision.
- **Addendum (2026-06-02, §11.5): the last CPU escape route, kernel diversification (BG9), is structurally closed.** Kernel selection is low-dimensional, so a strong baseline (RR) samples it directly, and ③'s niching advantage cannot in principle appear. **For ③ to work, "high-dimensional" deceptive terrain is required**, and the only remaining route is GPU full-LLM (itself a bet).
- Meta-lesson: **honest disclosure is not decoration — it was a tool that pushed the research forward.** In BG9, the same discipline worked in the direction of "confirming a negative correctly as a negative."

> ⚠ Every number in this article is a real measurement tied to a local (on-disk) research commit `THIRD_AXIS_SETTLE_VERDICT.md`. llcore does not yet have a public repository, so I can't link out. Instead I write "how we measured" fully in the body.

---

## 0. What This Article Is About (Concept)

`llcore` is a CPU-complete research framework that "turns the core computations of a Transformer (state-update rule, learning rule, cognitive-drive Δ) into genes and evolves them while verifying with Z3 that they don't break" (I wrote about the PoC battery in Series #32).

Its evolution engine has a design crux: how to make **③ (survival-of-the-fittest selection / separation)** — one of the four elements of evolution — effective. It's a "sort, separate, and raise" mechanism, like MAP-Elites, which keeps diversity and leaves elites in their niches.

The question is simple.

> **Do you really need that ③?**

If you do, the heavy investment to carry ③ (ultimately running a real LLM on GPU) is meaningful. If you don't, clinging to ③ is a waste of time and electricity.

Over this single day (2026-06-02), I went head-on to **settle that question with three experiments.** As the title says, the conclusion drags us back, once more, to FullSense's recurring bassline: "an over-tidy result is an alarm."

— That's 30 seconds. Warm-up done. On to the main subject. —

---

## 1. An Analogy: Mountain Climbing and Deceptive Terrain

Before the equations, let's grasp the big picture with a terrain analogy (a metaphor I've used consistently in this research).

We represent the quality of a design by **the height of the terrain**. **A high place = a good design.** It's a game of finding the highest summit.

**Terrain 1: a smooth single mountain (easy)**

```
 良さ↑
  高 |            ___________
     |         __/           \__
     |      __/                 \__     ← どこから登っても
     |   __/                       \__     同じ頂上に着く
  低 |__/                             \__
     +----------------------------------→ 設計の選び方
```

On terrain like this, naive "hill-climbing" — "just move toward something slightly better than now" — is enough to reach the summit. **You don't need the fancy device (③).**

**Terrain 2: deceptive terrain**

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

Here, naive hill-climbing stops at the false peak. It hasn't the courage to descend into the valley.

This is where the ③ idea works. **You leave various types of climbers scattered around the valley** (= memory palace / MAP-Elites archive). Someone can cross the valley by "stepping stones" and reach the real summit — that's the mechanism.

**The heart of this research in one line**: ③ is truly useful **only on "deceptive terrain."** On a smooth single mountain, ③ is a white elephant.

So the question can be rephrased:

> **"When you design an AI by evolution, is the terrain you actually run into 'deceptive terrain,' or a 'smooth single mountain'?"**

Settle this, and whether ③ is needed is settled. Today, this is what we measured.

---

## 2. The Leftover from the Past — Was "③ Unnecessary" Really "Unnecessary"?

Across the past experiments (Step C → Ladder rung 1 → E-A → valley-depth measurement), the picture was roughly this.

- **On the synthetic deceptive corridor, ③ wins by a landslide** (beats all three baselines, Cliff δ=+1.0). ③ is proven to exist, genuine as a mechanism.
- **On the more-realistic proxy terrain, ③ is negative** (MAP-Elites only ties random = the same symptom as a smooth terrain).

But two unresolved snags remained here.

1. **Is "③ unnecessary" really because "the terrain is smooth," or simply because "there weren't enough samples to detect the difference (underpower)"?** ── Mistaking these means committing the over-generalization "③ is powerless."
2. The direct measurement of valley depth ended last time as **N/A (not measurable)**. The evaluation noise was larger than the depth of the valley, so even if a valley existed it was buried out of sight — an instrument limit.

In other words, whether what "looked smooth" was a **property of the terrain** or a **limit of the instrument** had not been settled. Pinning this down is Step D.

— A short break. That was the premise. From here on are the three experiments done today. —

---

## 3. Experiment Design — A Three-Part Set

| Experiment | What it measures | Aim |
|---|---|---|
| **EXP1** | proper-n re-test | Seriously increase sample size and pin down with statistical power whether ③'s effect is real |
| **EXP2** | deterministic C1 multimodality | Physically zero out the evaluation noise and judge noise-free whether the terrain is "deceptive" or a "smooth single mountain" |
| **EXP3** | verdict-flip of K4 ridge clip | Test the suspicion that "some post-processing is hiding ③" |

Discipline: everything isolated in `research/step_d_settle/`, src unmodified, git committed in one batch by the orchestrator. Each experiment passes the break gates (G1 CPU full-run / G2 reproducibility / G3 diagnostic validity / G4 src invariance).

---

## 4. EXP2 Was the Decider — Zero the Evaluation Noise and the Terrain Becomes Visible

The order is shuffled, but **the one that mattered most was EXP2**, so I write it first.

The reason last time's valley-depth measurement came out N/A was simple: **"valley depth (about 0.05·|fitness|) ≪ the jitter of the evaluation noise."** The valley was buried in the instrument's noise, so you couldn't tell whether it existed.

EXP2's trick is this.

> The closed form of an ESN reservoir (fixed seed) + ridge readout (`np.linalg.solve`) **draws no randomness at all.** So the evaluation noise can be physically zeroed down to machine epsilon (about 1.11e-16).

In measurement we confirmed `eval_noise_std ≤ 1.11e-16`. This is not "the value jitters on every evaluation"; it's an error originating from the smallest unit of floating point (ULP), and is **essentially zero.** With the noise fog completely cleared, we can directly measure the valleys of the terrain.

Here is the result (valley_fraction = the fraction of valleys; the larger, the more multimodal = deceptive terrain):

| landscape | type | dim | valley_fraction (mean/max) | multimodal? | verdict |
|---|---|---|---|---|---|
| **ESN_3param** (real proxy) | real | 3 | **0.000 / 0.000** | **False** (3 seeds agree) | smooth=single-peaked → ③ unnecessary, confirmed noise-free |
| **ESN_perneuron40** (real proxy) | real | 40 | **0.096 / 0.121** | **False** (3 seeds agree) | smooth-leaning (below floor 0.2) → ③ unnecessary |
| ctrl_multipeak_dim3 (positive control) | control | 3 | 0.701 / 0.727 | True | the diagnostic can detect multimodality ✓ |
| ctrl_multipeak_dim40 (positive control) | control | 40 | 0.795 / 0.818 | True | diagnostic sound ✓ |
| ctrl_quadratic_dim3 (negative control) | control | 3 | 0.000 | False | the diagnostic can detect smoothness ✓ |
| ctrl_quadratic_dim40 (negative control) | control | 40 | 0.000 | False | diagnostic sound ✓ |

Three points:

1. **The real proxy terrain (both 3-dim and 40-dim) is valley≈0 = single-peaked.** Exactly matched across 3 seeds.
2. **The diagnostic itself is sound.** The deliberately built multimodal positive control is properly detected as multimodal (0.70/0.80), and the quadratic negative control is properly detected as smooth (0.0). So "the real proxy is single-peaked" is not an instrument bug but a property of the terrain.
3. With this, **"the past ③ negatives were not from underpower but because the terrain really was smooth"** was, for the first time, backed up noise-free on a real substrate.

I'll also honestly note a side discovery. **The deceptive corridor (`make_corridor_eval(d=0.16)`) that we intended to use as a positive control turned out to be valley=0.0 (single-peaked verdict) once made deterministic.** The corridor's deceptiveness is the type "confine within a single basin and escape via ③'s behavioral niching" (behavioral-reach deception), and was **not** the deception of terrain valleys (C1 multi-basin). We confirmed in measurement the narrowing of scope: the corridor does not serve as a positive control for C1. This means the past valley-depth calibration cannot transfer the "corridor-derived threshold" to terrain multimodality.

— A breather here. "The positive control didn't act as a control" was quietly a shock. But this too couldn't be known without measuring. —

---

## 5. EXP1 — Only the Real-Multitask Neighborhood Shows a Faint Hint of "③ NOT null"

Next, we re-tested the band closest to the real problem (C-gen4b = MAP-Elites vs random, the real-multitask neighborhood), seriously increasing the sample size.

| case | original n=15 (audit) | fresh true re-run | verdict |
|---|---|---|---|
| **C-gen4b** | diff +0.063 / psd +0.20 / p 0.126 | **n=64: diff +0.0472, one-sided p 0.038, psd +0.188, gate PASS** | **③ load-bearing candidate (still_inconclusive)** |

Running with fresh seeds up to n=64, it **PASSED all four conditions of the strict gate.** That means the audit's reading of "③ unnecessary (inconclusive)" was, directionally, wrong, and **in C-gen4b ③ is in the NOT-null direction.**

…and not getting a winner's high here is the crux of this round. For three reasons, I kept it **a candidate at best.**

1. **Post-update power@n64 = 0.517 < 0.80.** The gate passed, but it doesn't reach the confirmation standard (power 0.80).
2. **Within-run drift (this is what mattered).** Following the trajectory of the cumulative p-value: first PASS at n=40 (p=0.042) → deeply significant at n=60 (p=0.010) → **back near the 0.05 boundary at n=64 (p=0.038).** Furthermore, splitting the seeds into first/second halves: **the first 32 seeds have diff=+0.0755 (frac_pos=0.625), but the second 32 seeds have diff=+0.0189, and the last 9 seeds have diff=−0.0376 (negative).** The PASS is propped up by the first-half seeds, and **the newer the data, the more it runs in the opposite direction.**
3. **Multiple comparison.** p=0.038 PASSES at α=0.05, but even with just EXP1's 3 cases it exceeds Bonferroni α=0.0167 (FAIL). Seen across the whole ③ research family it's harsher still.

In addition, the effect-size floor (psd) was bumping against a **structural ceiling.** C-gen4b's median psd doesn't budge from n=15→0.200 to n=255→0.200. `P(|psd|≥0.147)` (the fulfillment rate of the effect-size condition) plateaus at 0.794 even at n=255. Since it's a medium effect (psd≈0.20), no matter how much you increase the sample, the full gate's power won't exceed 0.80. **In other words, the very prospect that "increasing samples will confirm (A)" is thin on this proxy.**

Conclusion: **C-gen4b is "③ load-bearing candidate / still_inconclusive."** The headline "③ NOT null" leans too hard on a single boundary p=0.038. The within-run drift is real evidence that "the candidate may be a false positive."

---

## 6. EXP3 — The Suspicion That "Post-Processing Is Hiding ③" — Removing It Made Things *Worse*

The last suspicion was this. "Could the post-processing called the ridge-readout clip (K4) actually be crushing ③'s signal?" If so, removing the clip should make ③ surface.

I tried removing it.

| task | clip | MAP-E mean | baselines beaten | verdict_flip |
|---|---|---|---|---|
| **addition** | True | +0.0100 | 1/3 | — |
| **addition** | False | **−1.212** | 0/3 (all worse) | **False** |
| **flip_flop** | True | +0.426 | 0/3 | — |
| **flip_flop** | False | +0.438 | 0/3 | **False** |

When the clip was removed, far from ③ surfacing, **MAP-Elites degraded from +0.010 → −1.212 on addition.** clip=False drops MAP-Elites into the noise region of raw R²<0 (15/15 seeds negative, R² in [−3.68, −0.20]), and instead of recovering structure it made things worse. **= an active refutation of the hypothesis "the clip is hiding the signal."**

The null-ridge FPR (gene-independent target = the true null hypothesis) also has zero difference between clip True/False (both 0.0).

Verdict: **K4 is not "the sole active suppression mechanism" but is demoted to "a diagnostic observation that crushes spread but doesn't change the verdict."** With this, the past statistical audit's assertion "K4 = the sole active suppression" was shown to be overstated.

Honest reservation (equivalent to §6.3): null-FPR=0/0 is a floor value from only null_seeds=4, and this experiment shrank the budget by about 7×. So I unified the verdict label not as "null confirmed" but as **"not_load_bearing_at_this_budget."** "At this budget, K4 is not load-bearing" is more accurate than "the null was confirmed." The substance of the verdict (demotion to a diagnostic observation) is unchanged; I'm only raising word precision.

— A deep breath here. Three experiments done. Next is a self-check of "did I overstate." —

---

## 7. Surviving Refutation — Beating Up My Own Conclusion Through Three Lenses

The core of honest disclosure is "doubt your own conclusion most harshly," so I applied three independent refutation lenses. **All three survived as `refuted=true / medium`** — that is, the conservative verdict isn't overturned, but the positive-leaning emphasis works in the direction of being weakened.

1. **[power_adequacy] C-gen4b's gate PASS is fragile under optional-stopping + multiple comparison.** This is the §5 drift and Bonferroni FAIL above. Making "③ NOT null" a headline leans too hard on a boundary p. → recorded the p-vs-n trajectory and the sign reversal of the second-half seeds in the disclosure fields.
2. **[determinism_and_circularity] The single-peaked verdict is fragile near the threshold.** The determinism and non-circularity themselves are clean (the correlation between behavior and fitness is ≈0; the diagnostic doesn't use behavior descriptors but looks directly at terrain geometry). However, **90.9%** of ESN_3param's midpoints **dip downward**, and the maximum relative dip=0.0435 is just below the C1 valley threshold 0.05 (within 13%). So precisely speaking, it's not "**truly single-peaked**" but "a **weak multi-basin with shallow valleys (~2–4%) slightly below the C1 threshold.**" The direction of (B) null is maintained, but the robustness is limited because of threshold proximity.
3. **[clip_flip_validity] The K4 demotion is "at this budget" only because of the low budget.** verdict_flip=False is certain, but FPR 0/0 is a floor value and the budget is shrunk 7×. So rather than "firm refutation" we should state "not load-bearing at this budget."

None of the three is enough to "flip the conclusion," but all worked in the direction of "trimming overstatement." This self-audit is half of today's output.

---

## 8. One Mistake of My Own, Written Honestly

In the previous valley-depth workflow, I passed **stale (old) values** into the second-stage orchestrator briefing. Values like "all below threshold / d*=0.1234." But the result JSON actually committed had `all_below_threshold=false`. When I read the previous workflow's result, I had mixed up the value of a different metric.

**Adversarial verification detected this and downgraded the verdict to N/A.** That is, the process of doubting my own "over-tidy conclusion" caught my own copy-paste mistake. It's not a pleasant story, but because that ran, in today's Step D I could re-measure from correct footing.

I was reminded that honest disclosure is not just "don't erase failures" but "**place a mechanism that detects failures in advance.**"

---

## 9. How I Updated the Past Verdicts

| past verdict | past reading | Step D's update |
|---|---|---|
| E-A C-gen4b | underpowered, inconclusive | **direction updated: ③ is in the NOT-null direction (gate PASS at fresh n=64).** But a candidate at best |
| step6 exp7 (real ESN proxy, ③ negative) | n≤10 blind zone, "re-measurement required" | **major update: the terrain really is smooth (③ unnecessary), confirmed noise-free.** Re-measuring won't produce multimodality |
| valley depth N/A (not measurable) | instrument incapable | **resolved: made measurable via determinism** → vf≈0 (single-peaked). But a shallow valley near the threshold is a reservation |
| K4 clip = sole active suppression | "the clip conceals landscape structure" | **demoted: diagnostic observation** (not_load_bearing_at_this_budget) |

"Many of the past negatives that looked like '③ unnecessary' were not from underpower but because the terrain really was smooth" ── this one point being verified for the first time on a real substrate is the core of today.

---

## 10. The External Review (Codex) Confirmed with No Blockers

As a discipline of llcore, each capstone passes a pair review by Codex (gpt-5.4, read-only). This time's overall comment was **"No blockers ── ③ conclusion externally confirmed."**

- The judgment to keep C-gen4b a candidate rather than load_bearing is valid (confirmed updated power 0.5174 < 0.80 in the JSON).
- EXP2's determinism and non-circularity are clean. It also confirmed the body's self-admission that "weak multi-basin below the threshold" is more precise than "truly single-peaked."
- EXP3's K4 demotion is valid at the current budget (FPR 0/0 + 7× shrink, so at-this-budget only).

The 4 items pointed out (CF1–CF4) are **all about harness robustness and wording precision for future reruns,** and do not overturn the current conclusion. When we re-test ③ on GPU, we'll apply these and then reuse the harness.

---

## 11. We Were Trying a CPU Escape Route (Kernel Diversification / BG9)

"③'s main battle moves to GPU (the loss landscape of a real LLM)" is EXP2's recommendation. Since the real proxy is confirmed smooth, chasing ③ on smooth terrain won't yield (A) (if the terrain is a single mountain, there's naturally no gain from sorting and separating).

But since GPU is an investment decision, I was running in parallel **another hypothesis we can advance on CPU.** That is **kernel diversification.**

The hypothesis is this. Even if each individual kernel (rwkv / mamba / hopfield / linear_attn) is smooth, **uniting four kernel families could make fitness create a discontinuous step at the moment of kernel switching → the terrain could become multi-basin (deceptive terrain) → ③ could become load-bearing on CPU without GPU.** Verifying this was BG9.

At the time I first wrote this article, it was "right now measuring BG6 (whether the task → best-kernel mapping is non-constant, i.e., 'whether the favored kernel differs by task') in a smoke run." After that (within the same 2026-06-02), BG9 was settled. The next addendum section is its ending.

---

## 11.5. Addendum (2026-06-02): BG9 Settled — The Escape Route Was Structurally Closed

> The conclusion in one line: **BG9 = N/A (structural). That is, the CPU escape route of kernel diversification is closed because "③ failing to stand is structurally determined."** It's not "③ is unnecessary" but "in this space, ③ cannot in principle be separated from the strong baseline" — an informative negative.

The result of the escape route set up in §11 came out. The expected "kernel union creates multi-basin (deceptive terrain) and ③ stands on CPU" **did not happen.** And not "it happened to not stand," but it turned out **it structurally cannot stand.** BG9 confirms this with three tiers of evidence.

### (1) substrate validity — "discrimination exists but is weak" (PASS but caution)

First, when we re-designed the kernel-favoring task set from first principles and measured "whether the favored kernel differs by task" (BG6), the mapping was **non-constant = non-inert (PASS).** mamba / linear_attn / rwkv each became best on a different task. In the sense that we avoided the rut of "memory_tasks are kernel-neutral" stepped in at BG6, it's progress.

But honestly it is **weak**:

- **hopfield couldn't win on any task.** This is because the hopfield kernel is a **diagonal-scalar mock** and its tanh attractor was dysfunctional (per-seed R² was polarized at 0/0.99/0). So it's effectively not a "4-kernel union" but **3 kernels.**
- Clean specialization is only on 2 axes (selective_copy↔mamba / weighted_accum↔linear_attn). The rest have thin margins and are fragile.

→ **the existence of discrimination ≠ multimodality/barriers.** Non-inert-ification succeeded, but that doesn't guarantee deceptive terrain — only that far. Note that the limit of the diagonal mock is as declared in kernels.py's scope, and here we **claim only the feasibility of the mechanism** (full kernel performance is not claimed).

### (2) harness validity — the positive control doesn't validate (this is the decider)

Next is the main battle. With fixed parameters (behavior=(kernel_id, theta L1)), we honestly paired-compared MAP-Elites (③) against three baselines ── **RR-hillclimb (random-restart hill-climbing)** / panmictic-GA / random.

| substrate | result |
|---|---|
| **positive control** (synthetic kernel-barrier) | ③ defeats panmictic (+0.423) and random (+0.208). **But it can't beat RR** (+0.051, p=0.31 → FAIL). Falls short of beating all 3 baselines = **harness validity doesn't stand** |
| **negative control** (kernel-neutral tasks) | all methods saturate at R²≈1.0, no ③ advantage = **correctly null** (no false positive, the instrument is sound) |
| **real** (kernel-favoring multitask) smoke | ③ beaten 0/3, panmictic conversely exceeds ③ = **③ doesn't win** |

This is the decisive difference from Step D (technical version §4-7). On Step D's deceptive corridor, ③ could exclude RR. **Why can't it in kernel space?** There's one root cause:

> **RR can directly sample kernel_id ∈ [0,4) on each restart.** Kernel selection is a single coordinate of 4 discretes (low-dimensional), so RR directly hits all 4 kernels on restart. To "find the best kernel," you don't need to cross a valley = **teleport (direct warp).** So ③'s behavioral niching gets no chance to play.

The reason ③ could exclude RR on Step4's corridor was that there the behavior was `mean(24-dim)`, and by the CLT the mean concentrates at 0.5 → the global peak is a measure-zero region = **a high dimension that random/RR cannot sample directly.** kernel_id, conversely, is low-dimensional and can be sampled directly.

### (3) red-team — even adversarial verification couldn't refute it; rather, it confirmed

We hammered "is the harness's failure to stand really due to structure? could it be a chance setup mistake?" with an independent red-team. The result **failed to refute the structural claim and rather strengthened it**:

- **Mechanism confirmation**: instrumented RR scatters restart kid nearly uniformly across the 4 basins at [12,18,16,18] on the positive control, target reach 88%, best is restart→in-basin climb on 6/8 seeds. **Confirmed numerically** that "RR directly samples kernel_id on restart and bypasses the valley."
- **In all 4 faithful configurations (high-dim theta corridor / sequential-kernel / in-basin L1 corridor / deceptive multi-basin), ③ can't beat RR (beats_rr=False).** Loosen the corridor and RR reaches equally; tighten it and ③ **starves first.**
- **Boundary sweep**: the tighter you make the theta corridor dimension D=0→3, the faster ③ starves relative to RR (D=3: ③ reach 0.08 vs RR 0.42). Same across 3 base_seeds.

→ Quantitatively confirmed that **"a behavior dimension where ③ passes by excluding only RR does not structurally exist in kernel space."**

### Structural insight (the payoff of this settlement)

> **③ (MAP-Elites' behavioral niching) exceeds the strong baseline only when the "hard spot" is in a high-dimensional behavior space and unreachable by direct sampling (random restart).**

- **Kernel selection is low-dimensional (a single coordinate of 4 discretes)** → RR samples directly → ③'s niching advantage cannot in principle appear.
- Even if you move the deception into theta space, RR does greedy climb in-basin after restart, so if you tighten the corridor enough that RR can't pass, ③ also starves to the same degree. **The window of RR fail ∧ ③ succeed does not exist.**

This is the answer to the question left at Step4 §7, "if we expand the search space by kernel diversification, does ③ unlock?" The answer is **NO (structurally, on CPU).** For expansion to unlock ③, the added degree of freedom must produce a behavior that is **high-dimensional and hard to sample directly.** Kernel selection (low-dimensional, discrete) does not meet that condition.

### Implication for GPU

- **The CPU-exhaustion gate is CLEAR**: BG9 structurally closed the last CPU route (kernel-union). ③'s remaining route is **only the high-dimensional GPU full-LLM loss landscape.**
- The structural insight makes the GPU bet **better-motivated.** ③ only becomes meaningful in high-dimensional behavior. A full-LLM's parameter space is millions of dimensions = exactly high-dimensional. So the GPU test follows a principle — not the weak bet "maybe full-LLM is the only exception," but "③ requires high dimension, and full-LLM is the high-dimensional regime."
- **But it's still a bet**: if the real-LLM terrain can be directly navigated by a strong backprop-family baseline, ③ is unnecessary ── this is a **risk isomorphic to BG9's RR** (the possibility that "a strong baseline solves it directly" remains even on GPU). So GPU is appropriate not "solely for ③" but as a **portfolio judgment** (riding along with llive's real-LLM fitness etc.) + **one pre-registration via a cloud rental** (before capital commitment). BG9's structural insight itself becomes the GPU's falsifiable go/no-go criterion: "if ③ is load-bearing on full-LLM, its hard spot should be in a high-dimensional behavior space and hard to reach by direct sampling/backprop."

### Honest reservations (important)

- This is **not "③ turned out unnecessary."** "③ cannot in principle be separated from the strong baseline in this low-dimensional kernel space" = N/A (structural), and ③'s mechanism itself was already confirmed genuine at Step4. It's an **informative N/A** that, though N/A, carries the decisive information "the kernel route is closed."
- The harness/red-team are at smoke scale (5-12 seeds). At the proper test 15 seeds the numbers move, but **the structure (tighten and ③ starves first / RR directly samples kernel_id) is seed-independent and robust.** We will not run the full ≥15-seed proper test on real ── since the positive-control validity structurally doesn't stand, even if "③ unnecessary" came out on real, we couldn't separate "③ unnecessary vs detector-blind," and the red-team already confirmed that "detector-blind = the structure of kernel space," so even investing 7.5h of CPU wouldn't change the conclusion.
- The substrate is weak (effectively 3 kernels, **hopfield is a diagonal mock and dysfunctional**). With stronger kernel discrimination (full implementation, off-diagonal) there is **in theory** room for a different conclusion, but ③'s structural barrier (low-dimensional selection → RR direct sampling) is independent of the quality of the kernel implementation.
- The discipline of doubting "an over-tidy ③ success" was **not needed this time** ── ③ success never appeared in the first place (a negative just as the honest prior expected).

---

## 12. Meta-Lesson — Honesty Was a Tool for Winning

Today's real output is not the numbers but **that the spirit of "doubting an over-tidy result" actually pushed the research forward.**

- Because we physically erased the evaluation noise (EXP2), we could separate whether "smooth" was a property of the terrain or a limit of the instrument.
- Because we applied 3 adversarial-verification lenses, we kept "③ NOT null" off the headline and held it as a "candidate."
- Because I self-detected my mix-up of a stale value, I could make the correct downgrade to N/A, and re-measure today.
- **In BG9 (addendum) I learned one more thing**: **a low-dimensional hard spot gets solved directly by the strong baseline. So for ③ (the sort-and-raise device) to work, a "high-dimensional behavior space" is required.** "Make deceptive terrain and ③ stands" is only half right; precisely, ③ won't stand unless the terrain is **deceptive in a way too high-dimensional to sample directly.** With a kernel 4-choice (low-dimensional), RR hits all of them on restart, so ③'s turn never came in principle. This is the basis for declaring the escape route not "given up" but "**structurally closed.**"

"When you get an abnormally good result, always doubt the breakdown before feeling like a winner" ── FullSense's research discipline (`feedback_benchmark_honest_disclosure`) was turning not as mere self-admonition but as **a mechanism that actually catches false positives and raises the precision of the research.** BG9 is an example where the same discipline worked in the reverse direction (**confirming a negative correctly as a negative**) ── trying in the red-team to refute my own "③ doesn't stand," I failed to refute it and it was confirmed as structure.

The conclusion, once more, precisely (reflecting the BG9 settlement):

> **On the proxy substrate, "③ is unnecessary because the terrain is truly smooth" was confirmed noise-free** (Step D). Only in the real-multitask neighborhood (C-gen4b) did a faint sign of "③ NOT null" appear, but with small effect + drift + multiple comparison it stays **a candidate at best.** The K4 clip is demoted from active suppression to a diagnostic observation. And the last CPU escape route, **kernel diversification (BG9), is structurally closed** ── kernel selection is low-dimensional, so a strong baseline (RR) samples it directly, and ③'s niching advantage cannot in principle appear. **The only route left for verifying ③'s main battle is the high-dimensional GPU full-LLM loss landscape** (itself a bet carrying the "strong baseline solves it directly" risk).

"③ settled = ③ turned out unnecessary" is wrong. Correctly, **"③ pays off only on 'high-dimensional' deceptive terrain. Neither the realistic-ish thing we could measure on CPU (smooth) nor kernel diversification (low-dimensional) met that condition."** The main battle (high-dimensional GPU) is still ahead, and it's a bet with no guarantee.

---

**Tags**: evolutionary computation / MAP-Elites / statistical testing / statistical power / honest disclosure / CPU research
**Related**: Series #32 (llcore CPU PoC battery) / #29 (refutation, Goodhart, proxy limits) / #31 (Codex two-pillar)
**Project**: llcore (PyPI reservation llmesh-llcore, local research since the repository is not yet public)
