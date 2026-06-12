---
title: 'llcore 検証 arc (#36) — 2ⁿ の壁を破る: vertex-free 健全証明と「コストを進化の選択圧に」'
tags: [FullSense, llcore, 解説, 形式手法, 進化計算]
private: true
updated_at: '2026-06-06'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

> 📝 **ドラフト注記**: 本稿は #35 (検証器の梯子) の続編。図アセットは `docs/articles/assets/qiita_36/` に同梱済 (公開時に push して raw URL を解決)。

> ⚠️ **追記 / Addendum (2026-06-06, PoC-2.6)**
> - **JA**: 本文の coverage 値 (B2 77.6% / inf∪B2 87%) は **n=8 限定**。後続測定で coverage は次元上昇に伴い劣化 (inf∪B2 87→77→**60%** @ n=8/12/16、n=16 で inf に合流) と判明。**コスト勝ち・健全性は全 n で維持**されるが、高次元では cheap 境界が保守化する (詳細は論文 PAPER_DRAFT.md §7.5)。
> - **EN**: The coverage figures (B2 77.6% / inf∪B2 87%) are **n=8 only**; a follow-up found coverage degrades with dimension (inf∪B2 87→77→**60%** at n=8/12/16, meeting cert_inf by n=16). The cost win and soundness hold at all n, but the cheap bound becomes conservative at scale.
> - **中文**: 本文的覆盖率 (B2 77.6% / inf∪B2 87%) **仅限 n=8**；后续测量发现覆盖率随维度上升而下降 (inf∪B2 87→77→**60%**，n=16 时与 inf 持平)。成本优势与健全性在所有 n 下保持，但廉价上界在高维下趋于保守。
> - **한국어**: 본문의 커버리지 수치 (B2 77.6% / inf∪B2 87%) 는 **n=8 한정**이며, 후속 측정에서 차원이 커질수록 저하됨 (inf∪B2 87→77→**60%**, n=16 에서 inf 와 합류). 비용 이점과 건전성은 모든 n 에서 유지되지만 고차원에서는 저렴한 상계가 보수적으로 변한다.

---

# 日本語

# llcore 検証 arc (#36) — 2ⁿ の壁を破る: vertex-free 健全証明と「コストを進化の選択圧に」

![検証器コスト: vertex-free vs 2ⁿ 列挙](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_cost.svg)

> **Concept hook**
> 進化する AI の「壊れてないか検査器」は、安全の番人であると同時に **計算コストの怪物**でもある。厳密な健全証明 (2-norm / SDP) は状態次元 n に対し **2ⁿ 個の頂点**を列挙する。n=8 で 256、n=16 で 65,536、n=32 で 43 億 — 虫の DNA 規模の次元どころか、その手前で検査器が先に音を上げる。本稿は (1) この 2ⁿ の壁を **頂点を列挙しない健全な近似**で破った実測 (SVD 1 回・最大 12,520 倍速・健全性違反ゼロ)、(2) PoC を一段ずつ回して「最安の素朴な境界は緩すぎ → 絶対値支配境界なら 78% 回収」と訂正した過程、(3) 生物の還元進化に倣い「**コストそのものを進化の選択圧に**する」構想、そして (4) 正直開示 — 検証器が perplexity を解放するという L3 の結果は **evolvability であって language learning ではない**(対照実験が tie しない) — を扱う。

## 0. 用語説明 / Glossary

| 用語 | やさしい意味 |
|---|---|
| llcore | FullSense の研究基盤。小さなニューラル系の「動き方 (dynamics)」を進化させる。CPU のみ・オンプレ・$0。 |
| 収縮 (contraction) | 時間が進むと状態差が縮む性質。あると暴走せず安定する=系の恒常性。 |
| 検査器 (verifier) | 「この個体は本当に収縮するか」を判定する関門。弱い順に梯子状 (∞ノルム→2-norm→SDP→…)。 |
| ヤコビアン J | 各時刻の「微小なズレがどう増幅されるか」を表す行列。σ_max(J)<1 なら 2-norm 的に収縮。 |
| t-box | tanh の傾き t がとりうる範囲 (各座標 [t_min,1])。J はこの箱の上を動く区間行列。 |
| 頂点列挙 (2ⁿ) | t-box の角 (2ⁿ 個) すべてで σ_max を調べる厳密法。n が増えると指数爆発。 |
| vertex-free | 頂点を列挙せず、箱全体の上界を 1〜2 回の行列演算で出す近似。安く済む。 |
| 健全 (sound) | 「収縮すると判定したら本当に収縮している」。偽陽性 (発散個体の見逃し) を出さない。 |
| 保守的 (conservative) | 本当は収縮するのに「ダメ」と弾きすぎること。健全だが取りこぼす。 |
| B2 = σ(\|M\|+R) | 区間行列の中点 M と半径 R から作る健全な上界。SVD 1 回。本稿の主役。 |
| SDP / LMI (robust-LMI) | 半正定値計画 / 線形行列不等式。Lyapunov の証明書 P を凸最適化で探す厳密枠組み (#35 の主役)。本稿では 2ⁿ 列挙の先にある「さらに重い」厳密検査器として登場。 |
| Lyapunov 関数 / 証明書 | 「この系は収縮する」ことを示すエネルギー関数 P。時間とともに必ず減る量を見つける発想。本稿では検査器の「次数 (どこまで強い証明か)」の文脈で言及。 |
| 2-norm (σ_max, 最大特異値) | 行列が入力を最も引き伸ばす倍率。σ_max(J)<1 ならどの方向のズレも縮む=2-norm 的に収縮。cert_two はこれを 2ⁿ 角で厳密確認する。 |
| ∞ノルム (cert_inf) | 各行の絶対値の和の最大。O(n²) で最も軽い健全検査器だが過保守 (#35 で進化を罠に)。本稿の安い基準線。 |
| SVD (特異値分解) | 行列を「回転×引き伸ばし×回転」に分解し σ_max を得る標準計算。B2 は箱全体の上界をこの SVD 1 回で得る (安さの源)。 |
| 区間行列 (中点 M / 半径 R) | 各成分が幅を持つ行列。t-box 上の J 全体を「真ん中 M ± ぶれ幅 R」で表す。B2 はこの M と R だけから上界を作る。 |
| fitness (適応度) | 進化が個体を選ぶときの「良さ」のスコア。本稿では言語予測性能 (perplexity) を主に指す。 |
| perplexity (PPL) | 言語モデルが次の文字をどれだけ「迷う」かの指標。低いほど良い予測。L3 で fitness 尺度に使う。 |
| unigram (無文脈モデル) | 文脈を一切見ず各文字の頻度だけで予測する最も単純な言語モデル。進化が陥る「退化の底」。 |
| evolvability (進化のしやすさ) | ある領域内で良い個体へ変異で到達できるか。到達可能な最良値 (天井の高さ) とは別物。本稿の正直開示の核。 |
| navigability | 探索空間を変異で「歩いて登れる」か。良い遺伝子が在っても辿り着けなければ低い。evolvability とほぼ同義で使う。 |
| パレート (Pareto) | 「片方を良くすると他方が悪くなる」複数目的のつり合い。本稿は性能 vs 構造コストをスカラー和でなくパレートで扱うべきと述べる。 |
| CE / nats | CE = 交差エントロピー (予測のずれ、低いほど良い)。nats は自然対数を底とする情報量の単位 (1 nat ≈ 1.44 bit)。L3 の対照実験の尺度。 |
| 還元進化 (reductive evolution) | 生物が不要な遺伝子・器官を捨てて単純化する進化。コスト削減そのものが選択圧。 |
| canalization | 進化が進むほど発生経路が固定され、変化しにくくなる現象 (Waddington 博士)。 |

## 1. かみくだき結論 / Plain-language conclusion

進化する AI には「壊れてないか検査器」が要る。これは #35 で梯子として実測した。今回の主題は、その検査器の **値段**だ。

一番強い健全検査器 (2-norm / SDP) は、状態の次元 n に対して **箱の角を 2ⁿ 個ぜんぶ調べる**。n=8 なら 256 個で済むが、n=16 で 65,536 個、n=32 で 43 億個 — 現実的な言語モデルの次元に届く前に検査器が破綻する。つまり「進化の天井」を決めていたのは、Lyapunov の次数でも遺伝子の数でもなく、**検査器が状態次元に対して指数的に重い**ことだった。

そこで「角を全部見るのをやめて、箱全体をまとめて 1 回で見積もる」近似を試した。最初の素朴な版 (三角不等式で分割した B1) は **緩すぎて**、収縮個体の 29.5% しか拾えず、しかも最安の ∞ノルムより保守的だった — いったんは「安い vertex-free はダメ、本物の SDP が要る」と悲観した。

ところが境界の作り方を変えた版 (絶対値で支配する B2) は一変。**厳密な 2ⁿ 列挙が拾う個体の 77.6% を、SVD たった 1 回で回収**した。健全性違反はゼロ (偽陽性なし)。∞ノルムと組み合わせると 87% に届く。速度は n=16 で **12,520 倍**。2ⁿ の壁は、少なくとも実用域では破れた。

そして発想がもう一段。生物は不要なものを捨てて単純化する (洞窟魚は眼を、寄生体は遺伝子を捨てる)。**コストの低さ自体を進化の選択圧にすれば、AI も「安く検証できる単純な構造」へ自分から向かう**のではないか。ただし罠がある — 「安い」には良い安さ (構造的に単純) と悪い安さ (検査器が保守的すぎて何も学ばない退化) があり、llcore の L3 で実際に後者 (unigram への退化) が観測された。だから単純なスカラー化ではなく、性能とコストのパレートで扱う必要がある。

最後に正直開示。「より強い検査器が perplexity を解放する」という L3 の見出しは、内訳を疑うと **evolvability (進化のしやすさ) であって language learning ではない**。文字列をシャッフルした対照実験でも検査器間の差が消えない (むしろ CE 尺度では ~107%) ので、効果は言語構造にほぼ依存しない最適化現象だった。本稿はこの内訳まで開示する。

## 2. なぜ 2ⁿ なのか — 検査器が指数的に重い理由

llcore の進化対象は遺伝子 `(decay, W)` で、次元は `n + n²`(n=8 なら 72)。だが**実行時間の律速はこの遺伝子サイズではない**。健全検査器が、ヤコビアン `J(t) = diag(decay) + diag((1−decay)⊙t)·W` の最大特異値を、**t-box の 2ⁿ 個の角すべて**で 1 未満か確かめるところにある。

| n | 遺伝子次元 n+n² | 2ⁿ 頂点 | cert_two 実測 (秒/個体) |
|---|---|---|---|
| 8 | 72 | 256 | 0.0064 |
| 12 | 156 | 4,096 | 0.082 |
| 16 | 272 | 65,536 | 2.76 |
| 32 | 1,056 | 43 億 | 実行不能 |

ここで誤解しやすいのは、**2ⁿ は状態次元 n に効くもので、重み行列の要素数 n² ではない**こと。だから「W を低ランク化して n² を減らす」だけでは検査器は速くならない。閉じた式の ∞ノルム (cert_inf) は O(n²) で軽いが、#35 で見たとおり過保守で進化を罠にかける。「**スケールする検査器は弱く、強い検査器はスケールしない**」というトレードオフが本丸だった。

## 3. PoC を一段ずつ — 「最安は緩すぎ」を「絶対値支配なら 78%」に訂正

検査器のコストを下げる方針として、t-box の角を列挙せず**箱全体の上界**を 1〜2 回の行列演算で出す「vertex-free」を試した。J は t についてアフィンなので、t-box は区間行列 = 中点 M と半径 R で表せる。

**PoC-1 (素朴な三角分割 B1 = σ(M) + σ(R))**: 健全 (構成上、上界) で、n=16 で 1 万倍以上速い。が、収縮個体の **29.5%** しか拾えず、最安の ∞ノルムより保守的だった。三角不等式が M と摂動を別々に最悪化するため緩い。→ いったん「安い vertex-free はダメ」と報告。

**PoC-2 (絶対値支配 B2 = σ(\|M\|+R))**: `|J| ≤ |M|+R` かつ「非負成分支配なら σ_max も単調」という性質から健全。これが効いた。

![証明器ごとの admit カバレッジ](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_coverage.svg)

| 検査器 | コスト | admit (3000 個中) | 厳密 2ⁿ (1310) の % | 健全性違反 |
|---|---|---|---|---|
| cert_two (厳密 2ⁿ) | O(2ⁿ·n³) | 1310 | 100% (基準) | — |
| cert_inf (∞ノルム) | O(n²) | 1072 | 81.8%※ | 0 |
| B1 = σ(M)+σ(R) | SVD 2 回 | 387 | 29.5% | 0 |
| **B2 = σ(\|M\|+R)** | **SVD 1 回** | **1017** | **77.6%** | **0** |
| cert_inf ∪ B2 | O(n²)+SVD 1 回 | **1142** | **87.2%** | 0 |

※ ∞ノルムは別ノルムの証明書で、1072 のうち 75 個は 2-norm では非収縮 (inf ⊄ two)。

つまり **B2 は厳密 2ⁿ の reach の 77.6% を SVD 1 回で回収**し、∞ノルムと組み合わせると 87% に届く。PoC-1 の悲観は「素朴な境界 B1 が悪かった」だけで、vertex-free 健全証明そのものが筋悪なのではなかった。これは「仕様を膨らませる前に PoC で安く確かめる」規律が効いた好例で、重い SDP 実装に進む前に**最安の境界が緩すぎることを数秒で確定**できた。

残った ~22% (B2 が取り逃し、厳密 2ⁿ か SDP のみが拾う個体) が、本当に「良い動き」を担っているか — これは現在測定中で、担っていなければ B2 で十分、本物の robust-LMI (SDP) は不要、という go/no-go になる。**測ってから決める**(担っている前提で SDP を作り始めない) のが honest disclosure の規律だ。

## 4. コストを「進化の選択圧」に — 生物の還元進化に倣う

ここから先は構想 (実装は user-gate)。現在の fitness は性能 (perplexity) だけだ。ここに**構造コスト** (ランク・疎性・実効次元) の項を足して多目的化すれば、進化は自分から「安く検証できる単純な構造」へ向かうのではないか。

生物はまさにこれをやっている。Prochlorococcus や SAR11 は自由生活細菌で最小ゲノム (複製速度・栄養経済で「削った方」が勝つ)、寄生体 (Buchnera, Mycoplasma) は遺伝子を捨て、洞窟魚は眼を失う。**複雑な機能の便益 < 維持コスト なら、単純な方が生き残る**。TRIZ も「理想性 (= 機能/コスト) の増大」を技術システム進化の中心法則とする。

ただし **llcore 自身の結果が警告する — 安さには 2 種類ある**:

- ✅ **良い安さ = 構造的単純さ** (低ランク/疎): 本当に検証が安く、かつ進化が動きやすい (navigable)。
- ❌ **悪い安さ① = 検査器の保守性**: ∞ノルムは最安だが、進化を unigram (無文脈) に罠落ちさせた。「検証が安い=善」と素朴に報酬化すると、進化を ∞ の罠へ押し込む。
- ❌ **悪い安さ② = 退化した振る舞い**: L3 で観測した unigram への collapse 自体が「安全・安価だが無能な、単純すぎる構造が生き残った」例 — 削りすぎて自由生活できなくなった絶対寄生体そのものだ。

だから正しい設計は「安い=善」のスカラー化ではなく、**性能 vs 構造コストのパレート**で、コスト項は構造的単純さを狙い、検査器の保守性を狙わない。そして llcore には**健全性 oracle** があるので、「良い単純 (低ランクでも unigram を超える)」と「退化した単純 (unigram に潰れた)」を**判別できる** — 普通の進化系にはできない芸当だ。これは FullSense の世界観そのもの:「適応的なだけでなく、**安く安全だと証明できる**方向へ進化する」。

そして「仕様が膨らむ前に PoC を」というのも、同じ原理の meta 版だ。**進化が進みすぎた系は変化しにくくなる** (canalization)。研究の物語・仕様が固まりすぎる前に、小さな実験で骨を確かめておく — それが系自身の navigability 教訓を、開発プロセスに適用するということだ。

## 5. 正直開示 / Honest disclosure — L3 は evolvability であって learning ではない

最後に、今日いちばん削った主張を開示する。L3 (検証 arc を実 byte-LM に載せた実験) の見出しは当初「より強い健全検査器が実 LM の perplexity を解放する」だった。10 seed で sound relaxation が ∞ゲートを上回る (p=0.000977) のは本物だ。だが内訳を疑うと:

![L3 正直開示: gate-gap は対照でも消えない](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_l3gap.svg)

- **同コーパス landscape**: ∞領域は unigram より 0.118 nats 良い遺伝子を**含む**のに、∞ゲート進化はそこへ到達できず unigram に張り付く。→ 罠は領域天井でなく **navigability (進化のしやすさ)** の問題。しかも 8192B では 3 領域の天井がほぼ等しく、12288B の「∞が最悪天井」梯子は corpus-robust でない。
- **対照実験 (文字列シャッフル)**: 「文脈が無意味なら検査器差は消える」と事前予測したのに、**順序が消えない**。fitness 尺度で ~84%、自然な CE (nats) 尺度ではむしろ **~107%** 残る。real−null の残差は非有意。→ gate-gap は言語構造にほぼ依存しない最適化現象。
- **唯一の構造依存 signal** = unigram-crossing (sound gate が real で無文脈を超え、null では超えない)。
- **gradient は罠を回避** (別実験 BG10): 勾配学習は全ゲートで同じ CE に到達し、検査器ペナルティ ~ゼロ。→ gradient-trained LM では検査器は soundness/coverage で選べばよく、navigability は不問。

結論: 検証された進化コアは実 byte-LM として**動く** (L0/L1/L2 成立) が、L3 の「payoff」は **evolvability であって language learning ではない**。これは負けではなく、内訳を疑った結果の正しい記述だ ([feedback_benchmark_honest_disclosure] の規律)。

> **Honest-disclosure box**
> | 主張 | 強さ | 限界 |
> |---|---|---|
> | B2 が厳密 2ⁿ の 77.6% を SVD 1 回で回収・健全性違反 0 | 実測 (n=8, 3000 個体) | 残 22% tail が navigable な動力学を担うかは測定中 |
> | inf∪B2 で 87.2%・最大 12,520 倍速 | 実測 (n=8/12/16) | n=8 reservoir LM、真 Transformer ではない |
> | sound relaxation が ∞ゲートを上回る (10/10, p=0.000977) | 実測 | evolvability であって learning ではない |
> | 検査器差は対照でも消えない (~107% on CE) | 実測 (10 seed null) | だから構造非依存=言語学習の証拠ではない |
> | コストを選択圧に | 構想・user-gate | 安さは 2 種、パレートで扱う必要 |

## 6. まとめ

- 進化する AI の検査器は、状態次元 n に対し **2ⁿ で爆発**する。これが「進化の天井」の正体だった。
- **vertex-free な健全境界 B2 = σ(\|M\|+R)** が、厳密 2ⁿ の reach の 77.6% を SVD 1 回・最大 12,520 倍速・偽陽性ゼロで回収。∞ノルムと併せ 87%。壁は実用域で破れた。
- 「**コストを進化の選択圧に**」=生物の還元進化に倣う構想。ただし良い安さ (構造的単純) と悪い安さ (保守性/退化) を健全性 oracle で判別するのが要。
- 正直開示: L3 の検証器 payoff は **evolvability であって language learning ではない** (対照が tie しない)。

(本稿は llcore 研究 arc の一部です。前段 = #35 検証器の梯子・SDP not SMT・solver-swap 正直開示。)

---

# English

# llcore Verification Arc (#36) — Breaking the 2ⁿ Wall: Vertex-Free Soundness Proofs and "Turning Cost into Evolutionary Selection Pressure"

![Verifier cost: vertex-free vs 2ⁿ enumeration](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_cost.svg)

> **Concept hook**
> The "is-it-broken inspector" for an evolving AI is both a guardian of safety and a **monster of computational cost**. A rigorous soundness proof (2-norm / SDP) enumerates **2ⁿ vertices** with respect to the state dimension n. That is 256 at n=8, 65,536 at n=16, and 4.3 billion at n=32 — long before reaching dimensions on the scale of an insect's DNA, the inspector itself collapses first. This article covers (1) the measured result of breaking this 2ⁿ wall with a **sound approximation that does not enumerate vertices** (a single SVD, up to 12,520× faster, zero soundness violations), (2) the process of running the PoC one stage at a time and correcting "the cheapest naive bound is too loose → an absolute-value-dominated bound recovers 78%," (3) a vision of "**turning cost itself into evolutionary selection pressure**," modeled on the reductive evolution of living things, and (4) an honest disclosure — the L3 result that a verifier "unlocks" perplexity is **evolvability, not language learning** (the control experiment does not tie).

## 0. Glossary

| Term | Plain meaning |
|---|---|
| llcore | FullSense's research substrate. It evolves the "dynamics" (the way it moves) of small neural systems. CPU-only, on-prem, $0. |
| contraction | The property that state differences shrink as time advances. With it, the system stays stable and does not run away = homeostasis of the system. |
| verifier (inspector) | The gate that judges "does this individual really contract." From weakest to strongest, arranged like a ladder (∞-norm → 2-norm → SDP → …). |
| Jacobian J | A matrix expressing "how a tiny deviation gets amplified" at each time step. If σ_max(J)<1, it contracts in the 2-norm sense. |
| t-box | The range that the tanh slope t can take (each coordinate in [t_min, 1]). J is an interval matrix moving over this box. |
| vertex enumeration (2ⁿ) | The exact method that checks σ_max at all 2ⁿ corners of the t-box. As n grows it explodes exponentially. |
| vertex-free | An approximation that produces an upper bound over the whole box with 1–2 matrix operations, without enumerating vertices. Cheap. |
| sound | "If it is judged to contract, it really does contract." It produces no false positives (no missed diverging individuals). |
| conservative | Rejecting too much — saying "no" even when something actually contracts. Sound, but it leaves real cases behind. |
| B2 = σ(\|M\|+R) | A sound upper bound built from the midpoint M and radius R of an interval matrix. A single SVD. The protagonist of this article. |
| SDP / LMI (robust-LMI) | Semidefinite program / linear matrix inequality — a rigorous framework that finds the Lyapunov certificate P by convex optimization (the protagonist of #35). Here it is the even heavier exact verifier that lies beyond 2ⁿ enumeration. |
| Lyapunov function / certificate | An energy function P proving the system contracts — the idea of finding a quantity that must keep decreasing over time. Referenced here in the context of the inspector's "order (how strong a proof)." |
| 2-norm (σ_max, largest singular value) | The maximum factor by which a matrix stretches an input. If σ_max(J)<1, deviations in every direction shrink = contraction in the 2-norm sense. cert_two checks this exactly at the 2ⁿ corners. |
| ∞-norm (cert_inf) | The max over rows of the absolute-value row sum. At O(n²) it is the cheapest sound inspector, but over-conservative (it trapped evolution in #35). The cheap baseline of this article. |
| SVD (singular value decomposition) | The standard computation that factors a matrix into "rotation × stretch × rotation" and yields σ_max. B2 obtains an upper bound over the whole box with a single SVD (the source of its cheapness). |
| interval matrix (midpoint M / radius R) | A matrix whose entries each have a width. The whole J over the t-box is written as "center M ± spread R." B2 builds its bound from only this M and R. |
| fitness | The "goodness" score by which evolution selects individuals. Here it mainly means language-prediction performance (perplexity). |
| perplexity (PPL) | A measure of how much a language model "hesitates" over the next character. Lower is a better prediction. Used as the fitness metric in L3. |
| unigram (context-free model) | The simplest language model, predicting from each character's frequency alone with no context. The "floor of degeneration" evolution falls into. |
| evolvability | Whether mutation can reach good individuals within a region — distinct from the best reachable value (the height of the ceiling). The core of this article's honest disclosure. |
| navigability | Whether the search space can be "walked up" by mutation. Low if good genes exist but cannot be reached. Used almost synonymously with evolvability. |
| Pareto | The balance among multiple objectives where "improving one worsens the other." This article argues performance vs structural cost must be handled as a Pareto trade-off, not a scalar sum. |
| CE / nats | CE = cross-entropy (the prediction gap; lower is better). nats is the unit of information in natural-log base (1 nat ≈ 1.44 bit). The metric of the L3 control experiment. |
| reductive evolution | The evolution by which organisms discard unnecessary genes and organs and become simpler. Cost reduction itself is the selection pressure. |
| canalization | The phenomenon that the more evolution advances, the more developmental pathways become fixed and resistant to change (Waddington). |

## 1. Plain-language conclusion

An evolving AI needs an "is-it-broken inspector." We measured this as a ladder in #35. The theme this time is the **price tag** of that inspector.

The strongest sound inspector (2-norm / SDP) checks **all 2ⁿ corners of the box** with respect to the state dimension n. At n=8 that is just 256 corners, but at n=16 it is 65,536, and at n=32 it is 4.3 billion — the inspector breaks down before reaching the dimensions of a realistic language model. In other words, what was setting the "ceiling on evolution" was not the order of the Lyapunov function nor the number of genes, but the fact that **the inspector is exponentially heavy with respect to the state dimension**.

So we tried an approximation that "stops looking at every corner and instead estimates the whole box at once." The first naive version (B1, split by the triangle inequality) was **too loose**: it picked up only 29.5% of the contracting individuals, and was even more conservative than the cheapest ∞-norm — for a moment we concluded pessimistically that "cheap vertex-free is no good; we need the real SDP."

But the version that changed how the bound is constructed (B2, dominated by absolute values) flipped everything around. **With a single SVD, it recovered 77.6% of the individuals that exact 2ⁿ enumeration admits.** Soundness violations were zero (no false positives). Combined with the ∞-norm it reaches 87%. The speed at n=16 was **12,520×**. The 2ⁿ wall was broken, at least in the practical range.

And then one more step in the idea. Living things discard the unnecessary and become simpler (cave fish discard their eyes, parasites discard their genes). **If we make cheapness of cost itself an evolutionary selection pressure, perhaps the AI too will steer on its own toward "simple structures that are cheap to verify."** But there is a trap — "cheap" comes in good cheapness (structurally simple) and bad cheapness (the inspector is so conservative that nothing is learned: degeneration), and in llcore's L3 the latter (degeneration into a unigram) was actually observed. So instead of simple scalarization, it must be handled as a Pareto trade-off between performance and cost.

Finally, an honest disclosure. The L3 headline "a stronger inspector unlocks perplexity" turns out, when you doubt the breakdown, to be **evolvability (ease of evolving), not language learning**. Even in a control experiment that shuffled the strings, the difference between inspectors does not vanish (it actually remains at ~107% on the CE metric), so the effect was an optimization phenomenon that barely depends on linguistic structure. This article discloses even that breakdown.

## 2. Why 2ⁿ — the reason the inspector is exponentially heavy

The target of evolution in llcore is the gene `(decay, W)`, whose dimension is `n + n²` (72 at n=8). But **the rate-limiting factor of runtime is not this gene size**. It lies where the sound inspector verifies that the largest singular value of the Jacobian `J(t) = diag(decay) + diag((1−decay)⊙t)·W` is below 1 at **all 2ⁿ corners of the t-box**.

| n | gene dim n+n² | 2ⁿ vertices | cert_two measured (sec/individual) |
|---|---|---|---|
| 8 | 72 | 256 | 0.0064 |
| 12 | 156 | 4,096 | 0.082 |
| 16 | 272 | 65,536 | 2.76 |
| 32 | 1,056 | 4.3 billion | infeasible |

The easy-to-misunderstand point here is that **2ⁿ scales with the state dimension n, not with the element count n² of the weight matrix**. So "lowering n² by making W low-rank" alone does not make the inspector faster. The closed-form ∞-norm (cert_inf) is light at O(n²), but as we saw in #35 it is over-conservative and lures evolution into a trap. The crux was the trade-off that "**the inspector that scales is weak, and the strong inspector does not scale**."

## 3. The PoC one stage at a time — correcting "the cheapest is too loose" into "absolute-value dominance gives 78%"

As a strategy to lower the inspector's cost, we tried "vertex-free": producing an upper bound over the **whole box** with 1–2 matrix operations, without enumerating the corners of the t-box. Since J is affine in t, the t-box can be represented as an interval matrix = midpoint M and radius R.

**PoC-1 (naive triangle split B1 = σ(M) + σ(R))**: Sound (by construction, an upper bound) and over 10,000× faster at n=16. But it picked up only **29.5%** of the contracting individuals and was more conservative than the cheapest ∞-norm. The triangle inequality is loose because it worst-cases M and the perturbation separately. → For the moment we reported "cheap vertex-free is no good."

**PoC-2 (absolute-value dominance B2 = σ(\|M\|+R))**: Sound by virtue of the property that `|J| ≤ |M|+R` and "if it is dominated by nonnegative components, σ_max is also monotone." This is what worked.

![Admit coverage by prover](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_coverage.svg)

| Inspector | Cost | admit (out of 3000) | % of exact 2ⁿ (1310) | Soundness violations |
|---|---|---|---|---|
| cert_two (exact 2ⁿ) | O(2ⁿ·n³) | 1310 | 100% (baseline) | — |
| cert_inf (∞-norm) | O(n²) | 1072 | 81.8%※ | 0 |
| B1 = σ(M)+σ(R) | 2 SVDs | 387 | 29.5% | 0 |
| **B2 = σ(\|M\|+R)** | **1 SVD** | **1017** | **77.6%** | **0** |
| cert_inf ∪ B2 | O(n²)+1 SVD | **1142** | **87.2%** | 0 |

※ The ∞-norm is a certificate in a different norm; 75 of the 1072 are non-contracting under the 2-norm (inf ⊄ two).

In other words, **B2 recovers 77.6% of the reach of exact 2ⁿ with a single SVD**, and combined with the ∞-norm it reaches 87%. The pessimism of PoC-1 was just "the naive bound B1 was bad" — vertex-free soundness proofs themselves were not a dead end. This is a good example of the discipline "check cheaply with a PoC before inflating the spec," letting us **confirm in seconds that the cheapest bound was too loose** before proceeding to a heavy SDP implementation.

The remaining ~22% (the individuals B2 misses, which only exact 2ⁿ or SDP picks up) — whether they really carry the "good dynamics" — is currently being measured, and this becomes a go/no-go: if they do not carry it, B2 is enough and a real robust-LMI (SDP) is unnecessary. **Decide after measuring** (do not start building the SDP on the assumption that they carry it) is the discipline of honest disclosure.

## 4. Turning cost into "evolutionary selection pressure" — modeled on the reductive evolution of living things

From here on it is a vision (implementation is user-gated). The current fitness is performance (perplexity) alone. If we add a **structural cost** term (rank, sparsity, effective dimension) here and make it multi-objective, perhaps evolution will steer on its own toward "simple structures that are cheap to verify."

Living things do exactly this. Prochlorococcus and SAR11 are free-living bacteria with minimal genomes ("the ones that trimmed" win on replication speed and nutrient economy), parasites (Buchnera, Mycoplasma) discard genes, and cave fish lose their eyes. **If the benefit of a complex function < the cost of maintaining it, the simpler one survives.** TRIZ too holds the "increase of ideality (= function / cost)" as the central law of technical-system evolution.

But **llcore's own results give a warning — there are two kinds of cheapness**:

- ✅ **Good cheapness = structural simplicity** (low-rank / sparse): truly cheap to verify, and also easy for evolution to move through (navigable).
- ❌ **Bad cheapness ① = the inspector's conservatism**: the ∞-norm is the cheapest, but it dropped evolution into a unigram (context-free) trap. If you naively reward "cheap to verify = good," you push evolution into the ∞ trap.
- ❌ **Bad cheapness ② = degenerate behavior**: the collapse into a unigram observed in L3 is itself an example of "a structure too simple — safe and cheap but incompetent — surviving." It is exactly an obligate parasite that trimmed away so much it can no longer live freely.

So the correct design is not the "cheap = good" scalarization, but a **Pareto trade-off between performance and structural cost**, where the cost term aims at structural simplicity, not at the inspector's conservatism. And because llcore has a **soundness oracle**, it can **discriminate** between "good simplicity (low-rank yet exceeding the unigram)" and "degenerate simplicity (collapsed into a unigram)" — a feat ordinary evolutionary systems cannot pull off. This is the FullSense worldview itself: "evolve not merely to be adaptive, but in a direction where one can **prove it is cheap and safe**."

And "do the PoC before the spec inflates" is the meta-version of the same principle. **A system that has evolved too far becomes resistant to change** (canalization). Before the research narrative and spec harden too much, confirm the skeleton with a small experiment — that is applying the system's own navigability lesson to the development process.

## 5. Honest disclosure — L3 is evolvability, not learning

Finally, let me disclose the claim I cut the most today. The L3 headline (the experiment putting the verification arc on a real byte-LM) was originally "a stronger sound inspector unlocks the perplexity of a real LM." That the sound relaxation beats the ∞ gate over 10 seeds (p=0.000977) is real. But when you doubt the breakdown:

![L3 honest disclosure: the gate-gap does not vanish even in the control](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_l3gap.svg)

- **Same-corpus landscape**: the ∞ region **contains** genes that are 0.118 nats better than the unigram, yet ∞-gate evolution cannot reach there and stays stuck at the unigram. → The trap is not a regional ceiling but a problem of **navigability (ease of evolving)**. Moreover, at 8192B the ceilings of the three regions are nearly equal, and the "∞ has the worst ceiling" ladder at 12288B is not corpus-robust.
- **Control experiment (string shuffle)**: we predicted in advance that "if context is meaningless, the inspector difference vanishes," yet **the ordering does not vanish**. On the fitness metric ~84% remains, and on the natural CE (nats) metric it actually remains at **~107%**. The real−null residual is non-significant. → The gate-gap is an optimization phenomenon that barely depends on linguistic structure.
- **The only structure-dependent signal** = unigram-crossing (the sound gate exceeds context-free on real, but does not exceed it on null).
- **Gradient avoids the trap** (separate experiment BG10): gradient learning reaches the same CE for all gates, with the inspector penalty ~zero. → For gradient-trained LMs, the inspector can be chosen by soundness/coverage, and navigability is moot.

Conclusion: the verified evolution core **works** as a real byte-LM (L0/L1/L2 hold), but the L3 "payoff" is **evolvability, not language learning**. This is not a defeat but the correct description that results from doubting the breakdown (the discipline of [feedback_benchmark_honest_disclosure]).

> **Honest-disclosure box**
> | Claim | Strength | Limitation |
> |---|---|---|
> | B2 recovers 77.6% of exact 2ⁿ with 1 SVD, 0 soundness violations | measured (n=8, 3000 individuals) | whether the remaining 22% tail carries navigable dynamics is being measured |
> | inf∪B2 gives 87.2%, up to 12,520× faster | measured (n=8/12/16) | n=8 reservoir LM, not a true Transformer |
> | sound relaxation beats the ∞ gate (10/10, p=0.000977) | measured | evolvability, not learning |
> | the inspector difference does not vanish even in the control (~107% on CE) | measured (10 seed null) | hence structure-independent = not evidence of language learning |
> | turning cost into selection pressure | vision, user-gated | cheapness comes in two kinds, must be handled as a Pareto trade-off |

## 6. Summary

- An evolving AI's inspector **explodes as 2ⁿ** with respect to the state dimension n. This was the true identity of the "ceiling on evolution."
- The **vertex-free sound bound B2 = σ(\|M\|+R)** recovers 77.6% of the reach of exact 2ⁿ with a single SVD, up to 12,520× faster, with zero false positives. Combined with the ∞-norm, 87%. The wall is broken in the practical range.
- "**Turning cost into evolutionary selection pressure**" = a vision modeled on the reductive evolution of living things. The key, however, is to discriminate good cheapness (structural simplicity) from bad cheapness (conservatism / degeneration) with the soundness oracle.
- Honest disclosure: the L3 verifier payoff is **evolvability, not language learning** (the control does not tie).

(This article is part of the llcore research arc. The preceding installment = #35: the ladder of verifiers, SDP not SMT, the solver-swap honest disclosure.)

---

# 中文

# llcore 验证 arc (#36) —— 突破 2ⁿ 之墙：vertex-free 健全证明与「把成本变成进化的选择压」

![验证器成本: vertex-free vs 2ⁿ 枚举](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_cost.svg)

> **Concept hook（概念钩子）**
> 进化中的 AI 的「检查它有没有坏掉的检查器」，既是安全的守门人，同时也是 **计算成本的怪兽**。严格的健全证明（2-norm / SDP）会针对状态维数 n 枚举 **2ⁿ 个顶点**。n=8 是 256，n=16 是 65,536，n=32 是 43 亿 —— 别说昆虫 DNA 规模的维数，连那之前检查器就先吃不消叫苦了。本文讨论：(1) 用 **不枚举顶点的健全近似** 突破这道 2ⁿ 之墙的实测（仅 1 次 SVD、最高提速 12,520 倍、健全性违规为零）；(2) 把 PoC 一段一段跑起来，从而把「最便宜的朴素界限太松 → 改用绝对值支配界限就能回收 78%」这一过程更正的经过；(3) 仿照生物的还原进化，「**把成本本身变成进化的选择压**」的构想；以及 (4) 诚实披露 —— 「验证器解放 perplexity」这一 L3 结果，其实是 **evolvability（易进化性）而非 language learning（语言学习）**（对照实验并不打平）。

## 0. 术语说明 / Glossary

| 术语 | 通俗含义 |
|---|---|
| llcore | FullSense 的研究基座。让小型神经系统的「运动方式（dynamics）」进化。仅用 CPU、本地（on-prem）、成本 $0。 |
| 收缩（contraction） | 随着时间推进，状态差会缩小的性质。具备它就不会失控、保持稳定＝系统的恒常性。 |
| 检查器（verifier） | 判定「这个个体是否真的会收缩」的关卡。按由弱到强呈梯子状（∞ 范数 → 2-norm → SDP → …）。 |
| 雅可比矩阵 J | 表示各时刻「微小偏差如何被放大」的矩阵。若 σ_max(J)<1 则在 2-norm 意义上收缩。 |
| t-box | tanh 的斜率 t 所能取的范围（各坐标 [t_min,1]）。J 是在这个盒子之上运动的区间矩阵。 |
| 顶点枚举（2ⁿ） | 在 t-box 的角（共 2ⁿ 个）上全部检查 σ_max 的严格方法。n 一增大就指数爆炸。 |
| vertex-free | 不枚举顶点，用 1～2 次矩阵运算给出整个盒子的上界的近似。代价便宜。 |
| 健全（sound） | 「一旦判定为收缩，就真的在收缩」。不产生假阳性（漏掉发散个体）。 |
| 保守（conservative） | 明明真的会收缩却被判「不行」而过度拒绝。虽健全但有漏判。 |
| B2 = σ(\|M\|+R) | 由区间矩阵的中点 M 与半径 R 构造的健全上界。仅 1 次 SVD。本文的主角。 |
| SDP / LMI（robust-LMI） | 半正定规划 / 线性矩阵不等式 —— 用凸优化寻找 Lyapunov 证书 P 的严格框架（#35 的主角）。本文中是位于 2ⁿ 枚举之后、「更重」的严格检查器。 |
| Lyapunov 函数 / 证书 | 证明系统收缩的能量函数 P —— 寻找一个随时间必然减少的量的思路。本文在检查器的「阶数（证明强到何种程度）」语境下提及。 |
| 2-norm（σ_max，最大奇异值） | 矩阵对输入的最大拉伸倍率。若 σ_max(J)<1，则各方向的偏差都缩小＝在 2-norm 意义上收缩。cert_two 在 2ⁿ 个角上严格确认这一点。 |
| ∞ 范数（cert_inf） | 各行绝对值之和的最大值。O(n²)、最便宜的健全检查器，但过度保守（在 #35 中把进化带进陷阱）。本文的廉价基准线。 |
| SVD（奇异值分解） | 把矩阵分解为「旋转×拉伸×旋转」并求出 σ_max 的标准计算。B2 仅用 1 次 SVD 就得到整个盒子的上界（廉价的来源）。 |
| 区间矩阵（中点 M / 半径 R） | 各元素都带有宽度的矩阵。把 t-box 上的整个 J 表示为「中心 M ± 摆幅 R」。B2 仅由这个 M 与 R 构造上界。 |
| fitness（适应度） | 进化挑选个体时的「好坏」分数。本文主要指语言预测性能（perplexity）。 |
| perplexity（PPL） | 衡量语言模型对下一个字符有多「犹豫」的指标。越低预测越好。L3 中用作 fitness 尺度。 |
| unigram（无上下文模型） | 完全不看上下文、仅凭各字符频率预测的最简单语言模型。进化陷入的「退化之底」。 |
| evolvability（易进化性） | 在某区域内能否通过变异到达好的个体 —— 与可达的最优值（天花板高度）是两回事。本文诚实披露的核心。 |
| navigability | 搜索空间能否靠变异「一步步爬上去」。即便存在好基因却到不了，则该性低。与 evolvability 几乎同义。 |
| 帕累托（Pareto） | 「改善一方就恶化另一方」的多目标平衡。本文主张性能 vs 结构成本应以帕累托权衡处理，而非标量求和。 |
| CE / nats | CE = 交叉熵（预测偏差，越低越好）。nats 是以自然对数为底的信息量单位（1 nat ≈ 1.44 bit）。L3 对照实验的尺度。 |
| 还原进化（reductive evolution） | 生物舍弃不需要的基因、器官而趋于简化的进化。成本削减本身就是选择压。 |
| canalization（运河化） | 进化越深入，发育路径越被固定、越难以改变的现象（Waddington 博士）。 |

## 1. 通俗结论 / Plain-language conclusion

进化中的 AI 需要一个「检查它有没有坏掉的检查器」。这一点在 #35 中已作为梯子实测过。这次的主题是这个检查器的 **价钱**。

最强的健全检查器（2-norm / SDP）会针对状态维数 n **把盒子的角 2ⁿ 个全部检查一遍**。n=8 时 256 个就够，但 n=16 是 65,536 个，n=32 是 43 亿个 —— 还没够到现实语言模型的维数，检查器就先崩了。也就是说，决定「进化天花板」的，既不是 Lyapunov 的阶数，也不是基因的数量，而是 **检查器相对状态维数呈指数级沉重**这一点。

于是我们尝试了「不再看遍所有角，而是把整个盒子合在一起一次性估算」的近似。最初的朴素版本（用三角不等式分拆的 B1）**太松**，只能捞起收缩个体的 29.5%，而且比最便宜的 ∞ 范数还保守 —— 一度悲观地认为「便宜的 vertex-free 不行，必须上货真价实的 SDP」。

然而改了界限构造方式的版本（用绝对值支配的 B2）一举翻盘。**仅用 1 次 SVD，就回收了严格 2ⁿ 枚举所捞到个体的 77.6%**。健全性违规为零（无假阳性）。与 ∞ 范数组合则达到 87%。速度在 n=16 时为 **12,520 倍**。这道 2ⁿ 之墙，至少在实用区间被突破了。

接着发想再进一步。生物会舍弃不需要的东西而趋于简化（穴居鱼舍弃眼睛，寄生体舍弃基因）。**如果把成本之低本身变成进化的选择压，AI 是否也会自己朝着「能廉价验证的简单结构」前进**呢？不过有陷阱 —— 「便宜」分为好的便宜（结构上简单）和坏的便宜（检查器太保守以致什么都学不到的退化），而在 llcore 的 L3 中实际观测到了后者（向 unigram 的退化）。因此不能用简单的标量化，而必须以性能与成本的帕累托（Pareto）来处理。

最后是诚实披露。「更强的检查器解放 perplexity」这一 L3 标题，一旦怀疑其内幕，其实是 **evolvability（易进化性）而非 language learning（语言学习）**。即便在打乱字符串顺序的对照实验中，检查器之间的差异也不消失（在 CE 尺度下反而约 107%），因此该效应是几乎不依赖语言结构的最优化现象。本文连同这份内幕一并披露。

## 2. 为什么是 2ⁿ —— 检查器呈指数级沉重的原因

llcore 的进化对象是基因 `(decay, W)`，维数为 `n + n²`（n=8 时为 72）。但 **执行时间的瓶颈并不是这个基因尺寸**。瓶颈在于健全检查器要把雅可比矩阵 `J(t) = diag(decay) + diag((1−decay)⊙t)·W` 的最大奇异值，在 **t-box 的 2ⁿ 个角上全部** 确认是否小于 1。

| n | 基因维数 n+n² | 2ⁿ 顶点 | cert_two 实测（秒/个体） |
|---|---|---|---|
| 8 | 72 | 256 | 0.0064 |
| 12 | 156 | 4,096 | 0.082 |
| 16 | 272 | 65,536 | 2.76 |
| 32 | 1,056 | 43 亿 | 无法执行 |

这里容易误解的是，**2ⁿ 作用于状态维数 n，而非权重矩阵的元素数 n²**。所以仅仅「把 W 低秩化以减少 n²」并不能让检查器变快。闭式的 ∞ 范数（cert_inf）是 O(n²)、很轻，但正如 #35 所见，它过度保守，会把进化带进陷阱。「**可扩展的检查器弱，强的检查器不可扩展**」这一权衡才是真正的核心。

## 3. 把 PoC 一段一段跑 —— 把「最便宜的太松」更正为「绝对值支配则 78%」

作为降低检查器成本的方针，我们尝试了「vertex-free」：不枚举 t-box 的角，而用 1～2 次矩阵运算给出 **整个盒子的上界**。由于 J 关于 t 是仿射（affine）的，t-box 可表示为区间矩阵＝中点 M 与半径 R。

**PoC-1（朴素三角分拆 B1 = σ(M) + σ(R)）**：健全（由构造上即为上界），在 n=16 时快 1 万倍以上。但只能捞到收缩个体的 **29.5%**，比最便宜的 ∞ 范数还保守。原因是三角不等式把 M 与扰动分别最坏化，所以太松。→ 一度报告「便宜的 vertex-free 不行」。

**PoC-2（绝对值支配 B2 = σ(\|M\|+R)）**：由 `|J| ≤ |M|+R` 以及「若由非负成分支配则 σ_max 也单调」这一性质而健全。这一招奏效了。

![各证明器的 admit 覆盖率](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_coverage.svg)

| 检查器 | 成本 | admit（3000 个中） | 占严格 2ⁿ（1310）的 % | 健全性违规 |
|---|---|---|---|---|
| cert_two（严格 2ⁿ） | O(2ⁿ·n³) | 1310 | 100%（基准） | — |
| cert_inf（∞ 范数） | O(n²) | 1072 | 81.8%※ | 0 |
| B1 = σ(M)+σ(R) | SVD 2 次 | 387 | 29.5% | 0 |
| **B2 = σ(\|M\|+R)** | **SVD 1 次** | **1017** | **77.6%** | **0** |
| cert_inf ∪ B2 | O(n²)+SVD 1 次 | **1142** | **87.2%** | 0 |

※ ∞ 范数是另一种范数的证书，1072 个中有 75 个在 2-norm 下其实非收缩（inf ⊄ two）。

也就是说，**B2 用 1 次 SVD 就回收了严格 2ⁿ 的可达（reach）的 77.6%**，与 ∞ 范数组合可达 87%。PoC-1 的悲观仅仅是「朴素界限 B1 不好」而已，并不是 vertex-free 健全证明本身路子差。这是「在膨胀规格之前先用 PoC 廉价地确认」这一纪律奏效的好例子 —— 在进入沉重的 SDP 实现之前，**几秒钟就能确定最便宜的界限太松**。

剩下的约 22%（B2 漏掉、只有严格 2ⁿ 或 SDP 才捞到的个体），是否真的承担了「好的运动」—— 这一点目前正在测量中，如果没有承担，那么 B2 就足够、不需要货真价实的 robust-LMI（SDP），这就是 go/no-go 判断。**先测了再决定**（不在「假设它承担」的前提下就开始做 SDP），这才是 honest disclosure 的纪律。

## 4. 把成本变成「进化的选择压」—— 仿照生物的还原进化

从这里往后是构想（实现需 user-gate）。当前的 fitness 只有性能（perplexity）。若在此加上 **结构成本** 项（秩、稀疏性、有效维数）实现多目标化，进化是否会自己朝着「能廉价验证的简单结构」前进呢？

生物正是在这么做。Prochlorococcus 与 SAR11 是自由生活细菌，拥有最小基因组（在复制速度、营养经济上「削减的一方」胜出）；寄生体（Buchnera、Mycoplasma）舍弃基因；穴居鱼失去眼睛。**若复杂功能的收益 < 维持成本，则简单的一方存活**。TRIZ 也把「理想度（= 功能/成本）的增大」当作技术系统进化的中心法则。

不过 **llcore 自身的结果在警告我们 —— 便宜分为两种**：

- ✅ **好的便宜 = 结构上的简单**（低秩/稀疏）：真的验证便宜，且进化也容易推进（navigable）。
- ❌ **坏的便宜①  = 检查器的保守性**：∞ 范数最便宜，但它把进化推入了 unigram（无上下文）陷阱。若朴素地把「验证便宜＝善」奖励化，就会把进化挤进 ∞ 的陷阱。
- ❌ **坏的便宜② = 退化的行为**：L3 中观测到的向 unigram 的 collapse 本身，就是「安全、廉价却无能、过于简单的结构存活下来」的例子 —— 正是削减过头、再也无法自由生活的专性寄生体。

因此正确的设计不是「便宜＝善」的标量化，而是 **性能 vs 结构成本的帕累托**，成本项瞄准结构上的简单，而不瞄准检查器的保守性。并且 llcore 有 **健全性 oracle**，所以能 **区分**「好的简单（即便低秩也超越 unigram）」与「退化的简单（被压扁成 unigram）」—— 这是普通进化系统做不到的绝活。这正是 FullSense 的世界观：「不只是会适应，而是朝着 **能证明自己廉价且安全** 的方向进化」。

而「在规格膨胀之前先做 PoC」也是同一原理的 meta 版。**进化得太深的系统会变得难以改变**（canalization）。在研究的叙事、规格固化得太死之前，用小实验确认骨架 —— 这就是把系统自身的 navigability 教训，应用到开发流程上。

## 5. 诚实披露 / Honest disclosure —— L3 是 evolvability 而非 learning

最后，披露今天削减得最多的主张。L3（把验证 arc 搭载到真实 byte-LM 上的实验）的标题，最初是「更强的健全检查器解放真实 LM 的 perplexity」。在 10 个 seed 上 sound relaxation 胜过 ∞ 门（p=0.000977）是真的。但一旦怀疑其内幕：

![L3 诚实披露: gate-gap 在对照中也不消失](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_l3gap.svg)

- **同语料 landscape**：∞ 区域 **包含** 比 unigram 好 0.118 nats 的基因，但 ∞ 门进化却到不了那里，而黏在 unigram 上。→ 陷阱不是区域天花板，而是 **navigability（易进化性）** 的问题。而且在 8192B 时三个区域的天花板几乎相等，12288B 那个「∞ 是最差天花板」的梯子并不是 corpus-robust（语料稳健）的。
- **对照实验（字符串打乱）**：事前预测「若上下文无意义则检查器差异会消失」，但 **顺序并不消失**。在 fitness 尺度下约 84%，在自然的 CE（nats）尺度下反而残留 **约 107%**。real−null 的残差非显著。→ gate-gap 是几乎不依赖语言结构的最优化现象。
- **唯一的结构依赖 signal** = unigram-crossing（sound gate 在 real 下超越无上下文，而在 null 下不超越）。
- **gradient 会规避陷阱**（另一实验 BG10）：梯度学习在所有门下都到达相同的 CE，检查器惩罚约为零。→ 在 gradient-trained LM 中，检查器只需按 soundness/coverage 选择即可，navigability 不成问题。

结论：被验证过的进化核作为真实 byte-LM **能跑**（L0/L1/L2 成立），但 L3 的「payoff」是 **evolvability 而非 language learning**。这不是失败，而是怀疑内幕后得到的正确描述（[feedback_benchmark_honest_disclosure] 的纪律）。

> **Honest-disclosure box（诚实披露盒）**
> | 主张 | 强度 | 局限 |
> |---|---|---|
> | B2 用 1 次 SVD 回收严格 2ⁿ 的 77.6%、健全性违规 0 | 实测（n=8, 3000 个体） | 剩余 22% tail 是否承担 navigable 的动力学，仍在测量中 |
> | inf∪B2 达 87.2%、最高提速 12,520 倍 | 实测（n=8/12/16） | n=8 reservoir LM，并非真正的 Transformer |
> | sound relaxation 胜过 ∞ 门（10/10, p=0.000977） | 实测 | 是 evolvability 而非 learning |
> | 检查器差异在对照中也不消失（CE 上约 107%） | 实测（10 seed null） | 因此结构无关＝不是语言学习的证据 |
> | 把成本变成选择压 | 构想・user-gate | 便宜有 2 种，需以帕累托处理 |

## 6. 总结

- 进化中的 AI 的检查器，相对状态维数 n **以 2ⁿ 爆炸**。这就是「进化天花板」的真面目。
- **vertex-free 的健全界限 B2 = σ(\|M\|+R)**，用 1 次 SVD、最高提速 12,520 倍、假阳性为零，回收了严格 2ⁿ 可达的 77.6%。与 ∞ 范数合用则 87%。这道墙在实用区间被突破了。
- 「**把成本变成进化的选择压**」＝仿照生物还原进化的构想。但关键在于用健全性 oracle 区分好的便宜（结构上简单）与坏的便宜（保守性/退化）。
- 诚实披露：L3 的验证器 payoff 是 **evolvability 而非 language learning**（对照不打平）。

（本文是 llcore 研究 arc 的一部分。前篇 = #35 检查器的梯子、SDP not SMT、solver-swap 诚实披露。）

---

# 한국어

# llcore 검증 arc (#36) — 2ⁿ의 벽을 깨다: vertex-free 건전성 증명과 "비용을 진화의 선택압으로"

![검증기 비용: vertex-free vs 2ⁿ 열거](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_cost.svg)

> **Concept hook**
> 진화하는 AI의 "고장 나지 않았는지 검사하는 검사기"는 안전의 파수꾼인 동시에 **계산 비용의 괴물**이기도 하다. 엄밀한 건전성 증명(2-norm / SDP)은 상태 차원 n에 대해 **2ⁿ 개의 꼭짓점(vertex)**을 열거한다. n=8이면 256, n=16이면 65,536, n=32면 43억 — 곤충의 DNA 규모의 차원은커녕, 그 한참 앞에서 검사기가 먼저 비명을 지른다. 본고는 (1) 이 2ⁿ의 벽을 **꼭짓점을 열거하지 않는 건전한 근사**로 깬 실측(SVD 1회·최대 12,520배 가속·건전성 위반 제로), (2) PoC를 한 단계씩 돌려 "가장 싼 소박한 경계는 너무 느슨함 → 절댓값 지배 경계라면 78% 회수"로 정정한 과정, (3) 생물의 환원적 진화(reductive evolution)를 본떠 "**비용 그 자체를 진화의 선택압으로**" 만드는 구상, 그리고 (4) 정직한 개시(honest disclosure) — 검사기가 perplexity를 해방한다는 L3의 결과는 **evolvability(진화 용이성)이지 language learning이 아니다**(대조 실험이 tie하지 않는다) — 를 다룬다.

## 0. 용어 설명 / Glossary

| 용어 | 쉬운 의미 |
|---|---|
| llcore | FullSense의 연구 기반. 작은 신경계의 "움직이는 방식(dynamics)"을 진화시킨다. CPU만 사용·온프레미스·$0. |
| 수축 (contraction) | 시간이 흐르면 상태 차이가 줄어드는 성질. 이게 있으면 폭주하지 않고 안정된다 = 계의 항상성. |
| 검사기 (verifier) | "이 개체가 정말로 수축하는가"를 판정하는 관문. 약한 순으로 사다리 형태(∞노름→2-norm→SDP→…). |
| 야코비안 J | 각 시각의 "미세한 어긋남이 어떻게 증폭되는가"를 나타내는 행렬. σ_max(J)<1이면 2-norm적으로 수축. |
| t-box | tanh의 기울기 t가 취할 수 있는 범위(각 좌표 [t_min,1]). J는 이 상자 위를 움직이는 구간 행렬(interval matrix). |
| 꼭짓점 열거 (2ⁿ) | t-box의 모서리(2ⁿ 개) 전부에서 σ_max를 조사하는 엄밀법. n이 커지면 지수 폭발. |
| vertex-free | 꼭짓점을 열거하지 않고, 상자 전체의 상계(upper bound)를 1~2회 행렬 연산으로 산출하는 근사. 비용이 싸게 든다. |
| 건전 (sound) | "수축한다고 판정했다면 정말로 수축하고 있다." 위양성(발산 개체의 누락)을 내지 않는다. |
| 보수적 (conservative) | 실제로는 수축하는데 "안 된다"고 지나치게 튕겨내는 것. 건전하지만 놓친다. |
| B2 = σ(\|M\|+R) | 구간 행렬의 중점(midpoint) M과 반경(radius) R로부터 만드는 건전한 상계. SVD 1회. 본고의 주인공. |
| SDP / LMI (robust-LMI) | 반정정계획 / 선형행렬부등식 — Lyapunov 증명서 P를 볼록 최적화로 찾는 엄밀한 틀 (#35의 주역). 본고에서는 2ⁿ 열거 너머에 있는 「더 무거운」 엄밀 검사기로 등장. |
| Lyapunov 함수 / 증명서 | 시스템이 수축함을 증명하는 에너지 함수 P — 시간에 따라 반드시 줄어드는 양을 찾는 발상. 본고에서는 검사기의 「차수(얼마나 강한 증명인가)」 맥락에서 언급. |
| 2-norm (σ_max, 최대 특이값) | 행렬이 입력을 가장 크게 늘리는 배율. σ_max(J)<1이면 모든 방향의 어긋남이 줄어듦＝2-norm적으로 수축. cert_two는 이를 2ⁿ 모서리에서 엄밀 확인. |
| ∞노름 (cert_inf) | 각 행의 절댓값 합의 최댓값. O(n²)으로 가장 싼 건전 검사기지만 과보수 (#35에서 진화를 함정에). 본고의 싼 기준선. |
| SVD (특이값 분해) | 행렬을 「회전×늘림×회전」으로 분해해 σ_max를 얻는 표준 계산. B2는 상자 전체의 상계를 이 SVD 1회로 얻는다 (저렴함의 원천). |
| 구간 행렬 (중점 M / 반경 R) | 각 성분이 폭을 가진 행렬. t-box 위의 J 전체를 「중심 M ± 흔들림 폭 R」로 표현. B2는 이 M과 R만으로 상계를 만든다. |
| fitness (적합도) | 진화가 개체를 고를 때의 「좋음」 점수. 본고에서는 주로 언어 예측 성능(perplexity)을 가리킨다. |
| perplexity (PPL) | 언어 모델이 다음 문자를 얼마나 「망설이는가」의 지표. 낮을수록 좋은 예측. L3에서 fitness 척도로 사용. |
| unigram (무문맥 모델) | 문맥을 전혀 보지 않고 각 문자의 빈도만으로 예측하는 가장 단순한 언어 모델. 진화가 빠지는 「퇴화의 바닥」. |
| evolvability (진화 용이성) | 어떤 영역 안에서 변이로 좋은 개체에 도달할 수 있는가 — 도달 가능한 최선값(천장 높이)과는 별개. 본고 정직 공개의 핵심. |
| navigability | 탐색 공간을 변이로 「걸어 올라갈」 수 있는가. 좋은 유전자가 있어도 도달 못 하면 낮다. evolvability와 거의 동의어로 사용. |
| 파레토 (Pareto) | 「한쪽을 좋게 하면 다른 쪽이 나빠지는」 다목적 균형. 본고는 성능 vs 구조 비용을 스칼라 합이 아니라 파레토로 다뤄야 한다고 말한다. |
| CE / nats | CE = 교차 엔트로피(예측 오차, 낮을수록 좋음). nats는 자연로그를 밑으로 하는 정보량 단위(1 nat ≈ 1.44 bit). L3 대조 실험의 척도. |
| 환원적 진화 (reductive evolution) | 생물이 불필요한 유전자·기관을 버리고 단순화하는 진화. 비용 절감 그 자체가 선택압. |
| canalization | 진화가 진행될수록 발생 경로가 고정되어 변하기 어려워지는 현상(Waddington 박사). |

## 1. 쉽게 풀어쓴 결론 / Plain-language conclusion

진화하는 AI에는 "고장 나지 않았는지 검사하는 검사기"가 필요하다. 이것은 #35에서 사다리로서 실측했다. 이번의 주제는, 그 검사기의 **값**이다.

가장 강한 건전 검사기(2-norm / SDP)는, 상태 차원 n에 대해 **상자의 모서리를 2ⁿ 개 전부 조사한다**. n=8이면 256개로 끝나지만, n=16이면 65,536개, n=32면 43억 개 — 현실적인 언어 모델의 차원에 닿기 전에 검사기가 붕괴한다. 즉 "진화의 천장"을 정하고 있던 것은, Lyapunov의 차수도 유전자의 수도 아니라, **검사기가 상태 차원에 대해 지수적으로 무겁다**는 점이었다.

그래서 "모서리를 전부 보는 것을 그만두고, 상자 전체를 한꺼번에 1회로 어림한다"는 근사를 시도했다. 처음의 소박한 버전(삼각부등식으로 분할한 B1)은 **너무 느슨해서**, 수축 개체의 29.5%밖에 건지지 못했고, 게다가 가장 싼 ∞노름보다 보수적이었다 — 일단은 "싼 vertex-free는 안 된다, 진짜 SDP가 필요하다"고 비관했다.

그런데 경계를 만드는 방식을 바꾼 버전(절댓값으로 지배하는 B2)은 완전히 달랐다. **엄밀한 2ⁿ 열거가 건지는 개체의 77.6%를, SVD 단 1회로 회수**했다. 건전성 위반은 제로(위양성 없음). ∞노름과 조합하면 87%에 도달한다. 속도는 n=16에서 **12,520배**. 2ⁿ의 벽은, 적어도 실용 영역에서는 깨졌다.

그리고 발상이 한 단계 더. 생물은 불필요한 것을 버리고 단순화한다(동굴 물고기는 눈을, 기생체는 유전자를 버린다). **비용의 낮음 자체를 진화의 선택압으로 삼으면, AI도 "싸게 검증할 수 있는 단순한 구조"로 스스로 향하지** 않을까. 다만 함정이 있다 — "싸다"에는 좋은 싸움(구조적으로 단순)과 나쁜 싸움(검사기가 너무 보수적이어서 아무것도 학습하지 않는 퇴화)이 있고, llcore의 L3에서 실제로 후자(unigram으로의 퇴화)가 관측되었다. 그래서 단순한 스칼라화가 아니라, 성능과 비용의 파레토(Pareto)로 다룰 필요가 있다.

마지막으로 정직한 개시. "더 강한 검사기가 perplexity를 해방한다"는 L3의 표제는, 내역을 의심해 보면 **evolvability(진화 용이성)이지 language learning이 아니다**. 문자열을 셔플한 대조 실험에서도 검사기 간의 차이가 사라지지 않는다(오히려 CE 척도로는 ~107%)므로, 효과는 언어 구조에 거의 의존하지 않는 최적화 현상이었다. 본고는 이 내역까지 개시한다.

## 2. 왜 2ⁿ인가 — 검사기가 지수적으로 무거운 이유

llcore의 진화 대상은 유전자 `(decay, W)`이고, 차원은 `n + n²`(n=8이면 72). 하지만 **실행 시간의 율속(律速, bottleneck)은 이 유전자 크기가 아니다**. 건전 검사기가, 야코비안 `J(t) = diag(decay) + diag((1−decay)⊙t)·W`의 최대 특이값을, **t-box의 2ⁿ 개의 모서리 전부**에서 1 미만인지 확인하는 데에 있다.

| n | 유전자 차원 n+n² | 2ⁿ 꼭짓점 | cert_two 실측 (초/개체) |
|---|---|---|---|
| 8 | 72 | 256 | 0.0064 |
| 12 | 156 | 4,096 | 0.082 |
| 16 | 272 | 65,536 | 2.76 |
| 32 | 1,056 | 43억 | 실행 불가능 |

여기서 오해하기 쉬운 것은, **2ⁿ은 상태 차원 n에 작용하는 것이지, 가중치 행렬의 원소 수 n²가 아니라는** 점이다. 그래서 "W를 저랭크(low-rank)화해서 n²를 줄인다"는 것만으로는 검사기가 빨라지지 않는다. 닫힌 식의 ∞노름(cert_inf)은 O(n²)으로 가볍지만, #35에서 본 대로 과도하게 보수적이어서 진화를 함정에 빠뜨린다. "**스케일하는 검사기는 약하고, 강한 검사기는 스케일하지 않는다**"는 트레이드오프가 본질이었다.

## 3. PoC를 한 단계씩 — "가장 싼 것은 너무 느슨함"을 "절댓값 지배라면 78%"로 정정

검사기의 비용을 낮추는 방침으로, t-box의 모서리를 열거하지 않고 **상자 전체의 상계**를 1~2회 행렬 연산으로 산출하는 "vertex-free"를 시도했다. J는 t에 대해 아핀(affine)이므로, t-box는 구간 행렬 = 중점 M과 반경 R로 표현할 수 있다.

**PoC-1 (소박한 삼각 분할 B1 = σ(M) + σ(R))**: 건전(구성상 상계)하고, n=16에서 1만 배 이상 빠르다. 하지만 수축 개체의 **29.5%**밖에 건지지 못했고, 가장 싼 ∞노름보다 보수적이었다. 삼각부등식이 M과 섭동(perturbation)을 별개로 최악화하기 때문에 느슨하다. → 일단 "싼 vertex-free는 안 된다"고 보고.

**PoC-2 (절댓값 지배 B2 = σ(\|M\|+R))**: `|J| ≤ |M|+R`이고 "비음수 성분 지배라면 σ_max도 단조"라는 성질로부터 건전. 이것이 효과를 냈다.

![증명기별 admit 커버리지](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_coverage.svg)

| 검사기 | 비용 | admit (3000개 중) | 엄밀 2ⁿ (1310)의 % | 건전성 위반 |
|---|---|---|---|---|
| cert_two (엄밀 2ⁿ) | O(2ⁿ·n³) | 1310 | 100% (기준) | — |
| cert_inf (∞노름) | O(n²) | 1072 | 81.8%※ | 0 |
| B1 = σ(M)+σ(R) | SVD 2회 | 387 | 29.5% | 0 |
| **B2 = σ(\|M\|+R)** | **SVD 1회** | **1017** | **77.6%** | **0** |
| cert_inf ∪ B2 | O(n²)+SVD 1회 | **1142** | **87.2%** | 0 |

※ ∞노름은 다른 노름의 증명서로, 1072개 중 75개는 2-norm에서는 비수축(inf ⊄ two).

즉 **B2는 엄밀 2ⁿ의 reach의 77.6%를 SVD 1회로 회수**하고, ∞노름과 조합하면 87%에 도달한다. PoC-1의 비관은 "소박한 경계 B1이 나빴을" 뿐, vertex-free 건전성 증명 그 자체가 길이 나쁜 것은 아니었다. 이것은 "사양을 부풀리기 전에 PoC로 싸게 확인한다"는 규율이 효과를 낸 좋은 예로, 무거운 SDP 구현으로 진행하기 전에 **가장 싼 경계가 너무 느슨하다는 것을 수 초 만에 확정**할 수 있었다.

남은 ~22%(B2가 놓치고, 엄밀 2ⁿ 또는 SDP만이 건지는 개체)가, 정말로 "좋은 움직임"을 담당하고 있는가 — 이것은 현재 측정 중이며, 담당하고 있지 않다면 B2로 충분하고, 진짜 robust-LMI(SDP)는 불필요하다는 go/no-go가 된다. **측정하고 나서 정한다**(담당하고 있다는 전제로 SDP를 만들기 시작하지 않는다)는 것이 honest disclosure의 규율이다.

## 4. 비용을 "진화의 선택압"으로 — 생물의 환원적 진화를 본뜨다

여기서부터는 구상(구현은 user-gate). 현재의 fitness는 성능(perplexity)뿐이다. 여기에 **구조 비용**(랭크·희소성·실효 차원)의 항을 더해 다목적화하면, 진화는 스스로 "싸게 검증할 수 있는 단순한 구조"로 향하지 않을까.

생물은 바로 이것을 하고 있다. Prochlorococcus나 SAR11은 자유 생활 세균으로 최소 게놈(복제 속도·영양 경제로 "깎은 쪽"이 이긴다), 기생체(Buchnera, Mycoplasma)는 유전자를 버리고, 동굴 물고기는 눈을 잃는다. **복잡한 기능의 편익 < 유지 비용이라면, 단순한 쪽이 살아남는다**. TRIZ도 "이상성(理想性, = 기능/비용)의 증대"를 기술 시스템 진화의 중심 법칙으로 삼는다.

다만 **llcore 자신의 결과가 경고한다 — 싸움에는 2종류가 있다**:

- ✅ **좋은 싸움 = 구조적 단순함** (저랭크/희소): 정말로 검증이 싸고, 게다가 진화가 움직이기 쉽다(navigable).
- ❌ **나쁜 싸움① = 검사기의 보수성**: ∞노름은 가장 싸지만, 진화를 unigram(무문맥)에 함정에 빠뜨렸다. "검증이 싸다=선(善)"이라고 소박하게 보상화하면, 진화를 ∞의 함정으로 밀어 넣는다.
- ❌ **나쁜 싸움② = 퇴화한 행동**: L3에서 관측한 unigram으로의 collapse 자체가 "안전·저렴하지만 무능한, 너무 단순한 구조가 살아남았다"는 예 — 너무 깎아서 자유 생활을 할 수 없게 된 절대 기생체 그 자체다.

그래서 올바른 설계는 "싸다=선"의 스칼라화가 아니라, **성능 vs 구조 비용의 파레토**로, 비용 항은 구조적 단순함을 노리고, 검사기의 보수성을 노리지 않는다. 그리고 llcore에는 **건전성 oracle**이 있으므로, "좋은 단순(저랭크라도 unigram을 넘는다)"과 "퇴화한 단순(unigram에 짓눌렸다)"을 **판별할 수 있다** — 보통의 진화계에는 할 수 없는 재주다. 이것은 FullSense의 세계관 그 자체:"적응적일 뿐만 아니라, **싸고 안전하다고 증명할 수 있는** 방향으로 진화한다."

그리고 "사양이 부풀기 전에 PoC를"이라는 것도, 같은 원리의 메타 버전이다. **진화가 너무 진행된 계는 변하기 어려워진다**(canalization). 연구의 이야기·사양이 너무 굳어지기 전에, 작은 실험으로 뼈대를 확인해 둔다 — 그것이 계 자신의 navigability 교훈을, 개발 프로세스에 적용한다는 것이다.

## 5. 정직한 개시 / Honest disclosure — L3는 evolvability이지 learning이 아니다

마지막으로, 오늘 가장 많이 깎은 주장을 개시한다. L3(검증 arc를 실제 byte-LM에 얹은 실험)의 표제는 당초 "더 강한 건전 검사기가 실제 LM의 perplexity를 해방한다"였다. 10 seed에서 sound relaxation이 ∞게이트를 능가하는 것(p=0.000977)은 진짜다. 하지만 내역을 의심해 보면:

![L3 정직한 개시: gate-gap은 대조에서도 사라지지 않는다](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_36/qiita_36_l3gap.svg)

- **동일 코퍼스 landscape**: ∞영역은 unigram보다 0.118 nats 좋은 유전자를 **포함**하는데도, ∞게이트 진화는 거기에 도달하지 못하고 unigram에 달라붙는다. → 함정은 영역 천장이 아니라 **navigability(진화 용이성)**의 문제. 게다가 8192B에서는 3개 영역의 천장이 거의 같고, 12288B의 "∞가 최악 천장" 사다리는 corpus-robust가 아니다.
- **대조 실험 (문자열 셔플)**: "문맥이 무의미하면 검사기 차이는 사라진다"고 사전 예측했는데, **순서가 사라지지 않는다**. fitness 척도로 ~84%, 자연스러운 CE(nats) 척도로는 오히려 **~107%** 남는다. real−null의 잔차는 비유의(non-significant). → gate-gap은 언어 구조에 거의 의존하지 않는 최적화 현상.
- **유일한 구조 의존 signal** = unigram-crossing (sound gate가 real에서 무문맥을 넘고, null에서는 넘지 않는다).
- **gradient는 함정을 회피** (별도 실험 BG10): 경사 학습은 모든 게이트에서 같은 CE에 도달하고, 검사기 페널티 ~제로. → gradient-trained LM에서는 검사기를 soundness/coverage로 고르면 되고, navigability는 불문(不問).

결론: 검증된 진화 코어는 실제 byte-LM으로서 **작동한다**(L0/L1/L2 성립)지만, L3의 "payoff"는 **evolvability이지 language learning이 아니다**. 이것은 패배가 아니라, 내역을 의심한 결과의 올바른 기술이다([feedback_benchmark_honest_disclosure]의 규율).

> **Honest-disclosure box**
> | 주장 | 강도 | 한계 |
> |---|---|---|
> | B2가 엄밀 2ⁿ의 77.6%를 SVD 1회로 회수·건전성 위반 0 | 실측 (n=8, 3000 개체) | 남은 22% tail이 navigable한 동역학을 담당하는지는 측정 중 |
> | inf∪B2로 87.2%·최대 12,520배 가속 | 실측 (n=8/12/16) | n=8 reservoir LM, 진짜 Transformer가 아니다 |
> | sound relaxation이 ∞게이트를 능가 (10/10, p=0.000977) | 실측 | evolvability이지 learning이 아니다 |
> | 검사기 차이는 대조에서도 사라지지 않는다 (~107% on CE) | 실측 (10 seed null) | 그래서 구조 비의존 = 언어 학습의 증거가 아니다 |
> | 비용을 선택압으로 | 구상·user-gate | 싸움은 2종, 파레토로 다룰 필요 |

## 6. 정리

- 진화하는 AI의 검사기는, 상태 차원 n에 대해 **2ⁿ으로 폭발**한다. 이것이 "진화의 천장"의 정체였다.
- **vertex-free한 건전 경계 B2 = σ(\|M\|+R)**가, 엄밀 2ⁿ의 reach의 77.6%를 SVD 1회·최대 12,520배 가속·위양성 제로로 회수. ∞노름과 합쳐 87%. 벽은 실용 영역에서 깨졌다.
- "**비용을 진화의 선택압으로**" = 생물의 환원적 진화를 본뜬 구상. 다만 좋은 싸움(구조적 단순)과 나쁜 싸움(보수성/퇴화)을 건전성 oracle로 판별하는 것이 핵심.
- 정직한 개시: L3의 검증기 payoff는 **evolvability이지 language learning이 아니다**(대조가 tie하지 않는다).

(본고는 llcore 연구 arc의 일부입니다. 전편 = #35 검증기의 사다리·SDP not SMT·solver-swap 정직한 개시.)
