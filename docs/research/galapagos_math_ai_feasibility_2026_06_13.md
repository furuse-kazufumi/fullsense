# ガラパゴ数学を AI/VLM に取り込めるか — 徹底フィジビリティ調査

- 日付: 2026-06-13
- 対象: FullSense (llcore / llive / lldarwin) への取り込み可否
- 規律: honest disclosure (異常に良い話は内訳を疑う / relabel を見抜く / over-claim 禁止)
- 検証根拠: 一次資料 (wiki.mathlava.com)、ローカル RAD コーパス grep、arxiv/WebSearch、**実コード一件ずつ検証** (D:/projects/llive, D:/projects/llcore)

---

## 1. エグゼクティブサマリ

**結論: 「新数学として取り込める」要素はゼロ。「検証可能な教材/データ生成器として additive に効く」要素が 1〜2 件 genuine に残る。**

6 角度 × 各 map→敵対検証 の総当りで、**verdict=genuine は 1 件も出なかった**。最良でも `weak`(動くが新規性が薄く、機構の本質はガラパゴ性でなく主流技術が担う)、多くは `illusory`(主流技術への日本語ラベル貼り、または既存資産の冗長な再実装)。全 16 mapping の `galapagos_doing_work` は **全件 false** ── すなわち「ガラパゴの斜交基底・視覚統一性」は、どの AI 機構においても計算の本質を担っていない。価値は一貫して「表現/視点/教材」側にある。

ただし honest disclosure を保ったまま **2 件**だけ、地に足の着いた additive な着地点がある:

1. **MathVerifier の三角正規化バグの回帰修正**(実測で発見した実バグ。最も確実な deliverable)
2. **ユーザー最重要洞察(言語化↔ビジュアル→VLM)の検証可能 paired データ生成器**(genuine に近いが受け皿が未実装で feasibility は要前段整備)

### スコープ補正注記

本タスクは当初『学術的に隔離進化した数学(和算・岡潔の数学等)を AI に取り込めるか』という枠で起票されたが、調査の結果、対象は **Mathlava(数学を愛する会)のコミュニティ独自体系 "Galapagothmetic"**(創始=みゆ、Discord・Twitter @Galapagothmetic、査読論文ではなくコミュニティ Wiki)であると判明した。岡潔(OKA-FX)は llive 側の既存実装であって調査対象そのものではない。以降「ガラパゴ数学」は一貫して Mathlava の Galapagothmetic を指す。

---

## 2. ガラパゴ数学とは(一次資料要約)

一次資料(wiki.mathlava.com の「ガラパゴ累乗定理」「ガラパゴ数列」記事)で確認できる中核は次の通り。

### 中核思想

- **数 = 多様体型オブジェクト上のラベル**。「大きさ(量; 1階以上のベクトル/テンソル的)」または「位置(座標; 0階, 無次元)」。
- **座標系 = 基準量 P(基底)+ 基準座標 0(原点)**。標準座標系は |P|=1, 終点=+1。
- **四則 = 同一オブジェクト上の異なる座標系間の値の翻訳**:
  - 加減(+,−): P 同一・0 を動かす = **並進(原点移動)**。座標 a→a+b。
  - 乗除(×,÷): 0 同一・P を変える = **スケーリング(基底変更)**。量 a→a×b。
  - → 加法と乗法を「同じ"座標翻訳"の別側面(動かす対象が原点か基底か)」として視覚統一。

### 中核機構(確定)

- **斜交座標系**: 複素数を直交基底 {1,i} でなく斜交基底 {1,z}(z=a+bi)で表す。
- **ガラパゴ累乗定理**: l=z·z̄=|z|², r=z+z̄=2Re(z) として
  **z^n = −l·S_{n−1} + S_n·z**。
  S_n は三項間漸化式 S_n=r·S_{n−1}−l·S_{n−2}, S_0=0, S_1=1。
  companion 行列 M=[[0,1],[−l,r]] の固有値が z,z̄。閉形式 S_n=(z^n−z̄^n)/(z−z̄)=Σ_k C(n−k−1,k) r^{n−2k−1} l^k。
- **ガラパゴ数列**: 第1種 G_n(虚部倍率)/第2種 G'_n(実部倍率)、同一漸化式・初期値違い。
- **ガラパゴ三角関数**: e^{xz}=cos_z(x)+z·sin_z(x)({1,z=e^{iθ}} 斜交基底)。z=i で標準 sin/cos 復元。
- **ガラパゴ三辺比定理**: 余弦定理の根号を「角の偶数倍化(=z^n)」で整式化 → 有理 cosθ で整数三辺比。θ=π/3 で x²−y² : 2xy−y² : x²+y²−xy。

---

## ガラパゴ数学の標準数学への翻訳と古典対応

ガラパゴ全体は「ℂ(あるいは実二次拡大)上の companion 行列冪 = Lucas/Chebyshev 数列」を、座標翻訳という単一の視覚言語で束ねた **再定式化(reformulation)** である。定理単位ではどれも 19 世紀までに確立済み。

| ガラパゴ概念 | 古典構造 | 新数学? |
|---|---|---|
| S_n(三項間漸化式) | **Lucas 数列 U_n(P=r, Q=l)**(完全一致, Lucas 1878) | × |
| z^n = C_n + S_n·z | 商環 ℝ[x]/(x²−rx+l) の剰余簡約 / **Cayley–Hamilton** | × |
| 第2種 G'_n | Lucas 数列 V_n = aⁿ+bⁿ(同一漸化式・別初期値) | × |
| |z|=1 特殊化 → S_n=sin nθ/sinθ | **第2種 Chebyshev 多項式 U_{n−1}**、V_n=2cos nθ=2·T_n | × |
| 黄金数生成元(l=−1,r=1) | **Fibonacci F_n / Lucas 数 L_n** | × |
| e^{xz}=cos_z+z·sin_z | 複素指数 / **de Moivre** / SO(2)=e^{iθ} の 1 パラメータ群 | × |
| 四則の視覚統一(原点 vs 基底) | 加法群(R,+) vs 乗法群(R*,×)/**アフィン群=並進⋉線形 / Klein・Lie** | × |
| ガラパゴ三辺比定理 | **Gaussian/Eisenstein 整数ノルム**形式によるピタゴラス数の角度一般化 | × |
| 斜交基底 {1,z} | 線形代数の**基底取り替え** / 実二次拡大体 ℝ[z]≅ℂ の生成元 | × |

### 新規性の正直な評価

**新定理は皆無**(is_new_math は全項目 false)。genuine な価値は次の 4 点に集約され、いずれも「新数学」でなく「表現/視点」である:

- **(A) 統一的視覚表現**: sin/cos・Fibonacci・Lucas・Chebyshev・de Moivre・Pythagoras 数を「単一生成元 z(2 パラメータ l,r)+ companion 行列」の 1 枚の座標翻訳図に圧縮(既知の同型を貼り合わせただけ)。
- **(B) 言語化↔視覚化の明示的ペア**: 記号記述(z^n=C_n+S_n z, companion 行列)と図像(斜交座標上の回転+伸縮)を 1:1 対応。VLM の modality-consistency 素材になりうる(後述・ユーザー最重要洞察)。
- **(C) OKA-FX への worked example**: l=|z|²(スケール不変量), r=2Re z(角度不変量)+ 加法群/乗法群の双対は、岡潔の invariants/symmetries 抽出の教科書的実例。
- **(D) 教育/普及**: 加法と乗法を「動かす対象が原点か基底か」で統一する視覚図は、honest disclosure を保ったまま記事・animated SVG・隔離進化(ガラパゴス化)ブランドの素材として強い。

---

## 3. AI/VLM 取り込み候補ランキング

verdict=genuine は 0 件のため、`weak`(動くが薄い)を上位に、`illusory`(焼き直し/冗長)を下位に置く。全件 `galapagos_doing_work=false`。

| 順位 | 候補 | 接続先 | verdict | feasibility | galapagos が機構を担うか | 先行研究重複 |
|---|---|---|---|---|---|---|
| 1 | **言語↔図像 paired 生成器(VLM consistency/grounding)** | llive(未実装 OKA-05)+ lldarwin visual_qa(未実装)+ VLM-FX | weak | low(受け皿未整備) | × | SynthRL / GF-Reasoner / PRiSM / VisTIRA / MathVerse |
| 2 | **6 表現 reformulation 同値クラス + MathVerifier 検証** | llive MathVerifier(実装済) | weak | medium | × | Putnam-AXIOM / RE-IMAGINE / S4Eq / RLVR |
| 3 | **number-direction probe(斜交基底=clock/pizza を l,r で読む)** | llcore(外部学習済 LLM 解釈) | weak | medium | × | Nanda 2023 / Kantamneni 2025 / Engels 2024 |
| 4 | **companion 行列 = 数埋め込み生成系** | llcore research(PoC) | weak | medium | × | Neural Isomorphic Fields 2601.12095 / FoNE |
| 5 | **OKA-03 戦略=斜交基底変換 stall→switch** | llive OKA-03(実装済) | weak | low | × | Polya 1945 / SATzilla portfolio |
| 6 | **斜交双対フレーム probe** | llcore(新規 lens) | illusory | low | × | Moisescu-Pareja 2025 / Hu-Niu-Varma 2026 |
| 7 | **companion 2×2 安定ゲート → Verified-Plasticity** | llcore verifier | illusory | low | × | S4D / 自社 backends.py(既存・上位互換) |
| 8 | **加法/乗法 2 ヘッド分離(同変)帰納バイアス** | llcore/lldarwin | weak/illusory | low | × | NALU 2018 / scale-equivariant CNN |
| 9 | **scale-equivariant 数演算層(log で乗→加)** | lldarwin/llcore | illusory | low | × | Sosnovik 2019 / Fourier-Mellin |
| 10 | **(l,r) 安定領域ダッシュボード可視化** | llcore(可視化層) | weak | high(図として) | × | Jury 判定 / trace-det plane(60 年前) |

### 各候補の要旨

**候補 1(VLM paired 生成器)** — ユーザー最重要洞察の直接実装で、本調査で「面白い案の域を超える」唯一の方向。だが (a) 受け皿の OKA-05 Reformulation Corpus は実コード上 Pending(後述・実測確認)、(b) lldarwin の visual_qa 軸も VLM-FX も requirements doc のみで未実装、(c) 機構(検証付き合成 paired データ + modality gap 定量化)は SynthRL/GF-Reasoner/PRiSM/VisTIRA に厚く先行されている。残る差分は「代数的に等価が機械検証された複数記号表現 × equivariant 図像」の組合せニッチのみ。

**候補 2(6 表現同値クラス)** — 数学は健全(n=2..9 で sympy 確認)で MathVerifier(実装済)は多項式表現を deterministic に検証できる。だが三角形式 sin nθ/sinθ は実 verifier で **FALSE NEGATIVE**(後述バグ)。受け皿 OKA-05 は未実装。価値は「Lucas 恒等式という良質な検証済み教材 1 件 + verifier の実バグ露出」に縮む。

**候補 3(number-direction probe)** — number-direction は円上(|z|=1)で表現されるため l=1,r=2cosθ となり、companion 固有基底 {z,z̄} が張る平面は helix fit の平面と**同一**。on-circle では両 fit が同じ R² → 増分なし。Kantamneni 2025 の helix+causal intervention の範囲内。

**候補 4(companion 数埋め込み)** — 有界性に |z|=√l=1 が必要 → l=1 に固定 → FoNE の単一周波数版に数値一致。「2 パラメータ族」は実質 Fourier か不安定基底の二択。Neural Isomorphic Fields(2601.12095)が中核を 5 か月先行。

---

## 4. 角度別詳細(6 角度)

### 角度 A: LLM/NN の数表現と解釈可能性

- **斜交基底 number probe(weak)**: companion 固有基底を残差ストリームに fit して clock/pizza を (l,r) で読む。機構は 50 行で動くが、on-circle では helix と同一平面 → 増分ゼロが理論的に確定。causal intervention(Engels/Nanda 流)を足さないと相関 fit に留まる。
- **斜交双対フレーム probe(illusory)**: Moisescu-Pareja 2025 が「Clock/Pizza=同一多様体の別パラメータ化」を証明済 → 斜交基底で両者を「別物として」補間する前提が崩れる。双対の非一意性で overparametrized、偽の説明力を生む。`backends.py` に lens/Gram 双対構成は存在せず greenfield。**ユーザー最重要の VLM 角度に一切触れない**(1D token 活性化 probe)。

### 角度 B: 帰納バイアス・数埋め込み・算術 curriculum

- **companion 数埋め込み(weak)**: 前述。FoNE の特殊例に縮退。
- **加法/乗法 2 ヘッド分離(illusory)**: NALU(2018)の add-gate/mul-gate と scale-equivariant CNN の再ラベル。log-polar は 0/負/複素で破綻。
- **6 表現 reformulation curriculum(weak)**: RLVR/Putnam-AXIOM に被覆。受け皿 OKA-05 未実装。

### 角度 C: SSM/線形再帰(llcore Mamba)と安定性・検証付き可塑性

最も「FullSense の主軸に効きそう」に見えて、最も徹底的に潰れた角度。

- **companion 2×2 安定ゲート(illusory)**: 実コード検証(`D:/projects/llcore/src/llcore/verifier/backends.py`, `tracking_tube.py`)で機構の前提が崩壊。
  - llcore の状態モデルは実数値 leaky-integrator RWKV。状態ヤコビは実スカラ/一般実行列で、**companion 行列 [[0,1],[−l,r]] も複素共役固有対も l=|z|² も llcore のどこにも存在しない**(grep `companion|complex|conjugate|imag` で hit ゼロ)。
  - ガラパゴ累乗定理は判別式 r²−4l<0 の複素共役根を要求するが、llcore の収縮ゲートは**実スペクトル半径を box 上で測る**問題。提案ゲートは適用対象の gene が存在しない = additive dead code。
  - **致命的に unsound**: spectral radius ρ<1 は時変(switched/LTV)系の収縮を保証しない(joint spectral radius の問題)。実測で ρ=0.72 の 2 行列を交互適用すると 40 step でノルムが 67000 倍以上に発散。既存 two_norm(σ_max<1)は正しく reject、提案ゲートは誤って admit する。fail-closed 規律と真っ向から矛盾。
  - 既存 `SdpLyapunovBackend` は line 219 で `np.max(np.abs(np.linalg.eigvals(J)))` を必要条件 pre-screen に既に使用。提案の閉形式は既存実装に内包済み。
- **VERDICT.md(実測確認)**: 検証器 frontier は `inf(0.38)→two_norm(0.89)→sdp(0.90)→[JSR/non-quadratic?]→empirical(0.99)` と pre-registration 付きで確定し、**次の backend を companion 固有値ゲートでなく JSR/non-quadratic Lyapunov と名指し済**。本案は frontier を後退させる。
- **(l,r) 安定領域可視化(weak)**: 三角形 {|r|<1+l ∧ l<1} は Schur-Cohn/Jury 判定の正確な特例(200k サンプルで 0 mismatch)。だが「stability region over the trace-determinant plane」は ~60 年前の制御理論教科書図。Mamba の A は対角・実(Re<0)で複素内部に入らないため、回転を見せる 2D 三角形は 1D 放物線に退化する。**図としては正しく有用だが新機構ゼロ**。

### 角度 D: 幾何深層学習・同変性・Erlangen

- **scale-equivariant 数演算層(illusory)**: Fourier-Mellin/log-polar(1970s)+ Sosnovik 2019 + ScaleGMN 2024 に完全被覆。RAD note 自身(galapago_math_corpus_v2/SKILL.md)が +/−=並進群・×/÷=乗法群を Bronstein/Cohen-Welling に既に紐付けており、relabel であることを内部資料が先に認めている。
- **不変量 l,r を OKA golden case に(weak)**: essence.py の InvariantLens は純粋なキーワード部分文字列マッチで、z^n から l=|z|² を抽出する記号能力はゼロ。提案 golden の一つ「arg(z^n)=n·arg(z)」は分岐切断で**数学的に偽**(z=−1−i で反例)。MathVerifier が reject する。

### 角度 E: llive OKA-FX 再定式化 + neuro-symbolic 検証算術

- **6 表現同値クラス(weak)**: 多項式表現(漸化式/companion/閉形式/Fibonacci)は実 MathVerifier で確実に equivalent、わざと符号誤植(二項和は (−l)^k が正、Wiki/note は誤記)を混ぜれば not_equivalent 検出の回帰テストになる。だが OKA-05 が Pending、三角は要 verifier 改修。
- **OKA-03 戦略=斜交基底変換(weak)**: StrategyOrchestrator の register/should_switch/switch_to/ledger は実在し additive。だが golden ケースの核「整式化で √ が消える」は、既に required dep の **sympy.factor が galapago 機構なしで出す結果**(x⁴−2x³y+3x²y²−2xy³+y⁴ → (x²−xy+y²)²)。ガラパゴ斜交基底は解法 capability を一切供給せず戦略名の label。stall→switch 自体は Polya 1945 + SATzilla portfolio の標準。

### 角度 F: VLM(言語化↔ビジュアルイメージの結合)— ユーザー最重要

- **座標翻訳 curriculum(weak)**: 機構(検証付き合成 symbol⇄diagram paired + code-prediction/consistency 損失)は SynthRL/GF-Reasoner/Choudhury 2509.09013/MathVerse に 2025-2026 で飽和。`svg_translate.py` は文字列翻訳ユーティリティで図を描かない(道具の誤用)。lldarwin の `_AXIS_TASKS` は text-only で visual_qa 軸は未実装。Chimera/Hou が示す通り、合成図の単純さで VLM はショートカットで当てる(高一致率≠見て解いた)。
- **7 表現(6 記号 + 図像)同値クラス(weak)**: パラメトリック(全 n)同値が実 MathVerifier で discharge 不能(symbolic-n は hyper/gamma を含む Piecewise を返す)。fixed-n の 6 表現は rep1=rep2=rep4 が全 n で一致 = 独立情報量 1。「7 表現=7 倍知識」は over-claim。

---

## 5. 最有望: 次の最小 PoC(1 件を具体化)

**= MathVerifier の三角正規化バグの回帰修正 + 検証済み多項式同値クラスの seed 投入。**

これが最も確実に着地する理由: (1) 調査中に**実測で見つけた実バグ**であり仮説でない、(2) CPU 完結・既存 verifier に additive・新依存なし、(3) ガラパゴ由来を正直に「Lucas 恒等式の良質な seed」とラベルしつつ、副産物として llive の実欠陥を露出・修正できる。

### 実バグの内容(実コード検証済)

`D:/projects/llive/src/llive/math/verifier.py` の `check_equivalence` は `sympy.simplify(lhs−rhs)==0` 一本(line 244)。`expand_trig`/`rewrite(exp)` 前処理がない。このため三角形式 sin(nθ)/sinθ ⇄ Chebyshev U_{n−1}(cosθ) を n=5,7,11 で simplify しきれず **FALSE NEGATIVE**(残差 16sin⁴t−20sin²t+5−sin(5t)/sin(t) ≠ 0 を返す)。n=3 のみ偶然通る。

### PoC の中身(additive, src 非破壊で research スクリプト + テスト)

1. **回帰テスト追加**: `tests/unit/test_galapago_reformulation.py`
   - z=1+i など固定生成元で companion 行列冪 M^n[0,1] = 漸化式 S_n = 閉形式 (zⁿ−z̄ⁿ)/(z−z̄) = 多項式剰余 を n=2..7 で `check_equivalence` が equivalent を返すことを assert(多項式パスは確実に通る)。
   - 符号誤植版(Σ二項を (+l)^k にした誤記)を 1 件混ぜ not_equivalent 検出を assert(=verifier の健全性回帰)。
   - 三角形式 sin(nθ)/sinθ ⇄ chebyshevu(n−1, cos θ) を n=5 で投入し、**現状 verifier が FALSE NEGATIVE を返すことを xfail で固定**(バグの可視化)。
2. **verifier への trig 正規化フォールバック**(`check_equivalence` に薄い前処理):
   - `simplify(lhs−rhs)` が 0 でないとき、`expand_trig(...).rewrite(exp)` を適用して再 simplify するフォールバック path を additive 追加。n=5,7,11 で成功することを実測(緩和策は検証済)。
   - これで xfail を pass に昇格。**ガラパゴでなく任意の三角恒等式に効く一般改善**として位置づける。
3. **OKA-05 起動 seed(任意・小)**: 上記の検証済み多項式同値クラス JSON を、OKA-05 Reformulation Corpus の最初の 1 エントリとして投入できる形で出力。ただし「ガラパゴ取り込み」でなく「古典同値クラスで OKA-05 を着工」と正直にラベル。

### honest red-flag

- これは「新数学の獲得」でも「ガラパゴが機構を駆動」でもない。価値は **MathVerifier の実欠陥の発見・修正 + 良質な検証済み教材 1 件**。
- 効果(汎化/抽象化向上)を主張するなら baseline 比較を取り、改善幅ゼロも正直に出す。

---

## 6. ユーザー洞察の評価: 言語化↔ビジュアルイメージ→VLM(専節)

> 「言語化とビジュアルイメージのつながりが得られれば、VLM にも適用できる要素があるかもしれない」

**この洞察は正しい方向を突いている**が、現状の到達点は honest に言って「paired-representation 素材として有望」までで、「VLM grounding を実際に改善する」は未検証仮説である。

### なぜ筋が良いか

ガラパゴの本質『演算を視覚イメージで捉える』は、記号記述(z^n=C_n+S_n·z, companion 行列)と図像(斜交座標上の回転 arg z + 伸縮 |z|=√l)を **1:1 で対応づける**。これは「同一意味内容の textual-symbolic 表現と visual-spatial 表現のペア」そのもので、VLM の modality-consistency 評価・grounding 学習の paired-representation 素材になりうる。しかも記号側の正解が MathVerifier で deterministic に取れるため、**VLM 採点に人手不要(audit 可能)**で、FullSense の責任所在哲学に fit する。

### なぜ現状 weak に留まるか(内訳)

1. **機構は飽和**: 「検証付き合成 symbol⇄diagram paired + consistency/grounding 評価」は SynthRL(2506.02096, OOD 汎化を実証済)・GF-Reasoner(2508.09099)・PRiSM(2512.05930)・VisTIRA(2601.14440)・MathVerse(ECCV2024)に 2025-2026 で厚く先行。MathVerse は各問題を 6 版に変換して「MLLM が図を真に見ているか」を測り、**MLLM の図軽視を実証して VLM 効果主張を反証**している。
2. **反証側の証拠が優勢**: ViLP/Probing Visual Language Priors、MathSight、『VLM Visual Invariance の脆さ』(2604.01848)が一致して「現行 VLM は数学推論で画像を実質無視し言語 prior に依存」(Qwen3-VL は画像なしで multimodal variant を上回る)を示す。`非標準な斜交座標 z^n 図はむしろ grounding を阻害しうる`。
3. **受け皿が未実装**(実コード確認): OKA-05 Reformulation Corpus は Pending(Phase 11, MED)。lldarwin の visual_qa 軸・VLM-FX は requirements doc のみでコード不在。`svg_translate.py` は図を描かない。
4. **galapagos が機構を担わない**: 同じ生成器は標準 {1,i} 基底でも完全に同一に動く。斜交基底/視覚統一は「どの恒等式を描くか」という curriculum 内容に過ぎず、機構ではない。

### 残る genuine に近い差分

「**代数的に等価が機械検証された複数記号表現 × 明示的に rotation+scale equivariant な図像**」という構造化された冗長性は、surveyed 論文のいずれとも完全一致しない応用ニッチ。ただしこのニッチも equivariance 評価では 2604.01848 が隣接で食っており、優位は「verified algebraic equivalence class を equivariant 図に紐付ける」点に縮小する。

### VLM 方向の正直な推奨

VLM-evolution / lldarwin pressure 追加 / modality-consistency 数値化は real-VLM 評価経路が未実装(`scenario_6_vlm` は MockBackend = 画素を読まず image 数のみ報告、pressures.py は proxy 明記)のため **over-claim として切り離す**。救出できるのは CPU 完結・additive・audit クリーンな **検証可能図像↔記号ペア生成器**(matplotlib で {1,i} と {1,z} の両表現で同一 z^n 軌跡 + sympy で GT + MathVerifier で生成器自身を self-test)を、OKA-05 が立ち上がった後の最初の教材コーパスとして投入する用途まで。「ガラパゴ図が VLM grounding を改善するか」は reformulation 有/無の consistency 変化を baseline 比較してからのみ主張可。

---

## 7. 既存 FullSense 資産との接続

| 資産 | 接続の正直な評価 |
|---|---|
| **llive OKA-FX(実装済 OKA-01〜04/06/07)** | invariants/symmetries lens は**キーワード部分文字列マッチ**で記号抽出できない。ガラパゴ golden を入れるには lens を「sympy 式から保存量を解析抽出する symbolic lens」に Strategy 差し替えが必要(別作業)。 |
| **llive OKA-05 Reformulation Corpus** | **Pending(未実装)**。「既存資産に additive」前提は誤りで、片側は新規構築。古典同値クラスで着工する seed としてなら価値あり。 |
| **llive MathVerifier(実装済 MATH-02)** | 多項式同値は deterministic に検証可。三角は前処理(expand_trig/rewrite)欠落で false-negative(本調査で発見・修正対象)。complex z は a+bI 明示展開が前提。 |
| **llcore SSM-Lyapunov / Verified-Plasticity** | 既存 backends(inf/two_norm/sdp の sound certificate ladder)が companion より上位互換。frontier の次は JSR/non-quadratic と確定済。companion ゲートは**回帰**。実モデルは実数 RWKV/対角 Mamba で複素 companion ブロック不在。 |
| **lldarwin visual_qa / VLM-FX** | **コード不在**(requirements doc のみ)。pressures.py は proxy 明記で「進化で VLM 改善」は over-claim。 |
| **OKA-05 reformulation corpus(統一視点)との同型** | ガラパゴの「四則=座標翻訳の統一視点」と岡潔「同一概念の異表現で抽象化を育てる」は偶然同型で、教材としての物語整合は本物。ただし機構新規性ではない。 |

---

## 8. 完全性チェック(取りこぼし)

- **未取得の下位定理**: ガラパゴ数列の第1種/第2種の詳細初期値、三辺比定理の一般 θ 拡張、生成元族の相互変換則の細部は Wiki の該当記事を逐条取得していない。ただし全て Lucas U/V・Eisenstein ノルムの既知構造に還元されるため、結論(新数学ゼロ)は揺るがないと判断。
- **Discord 限定資料**: Mathlava の Discord 内に Wiki 未収録の定理/議論がある可能性。査読なしコミュニティ資料のため、採用する場合も標準数学(Lucas 数列)で正規化してから扱う方針は不変。
- **記法の揺れ**: Wiki の S_n=r·S_{n−1}(明らかな r·S_{n−1}−l·S_{n−2} の誤記)、二項和の符号((−l)^k が正)等を一次資料そのまま採用しない。
- **arxiv ID の誤り**: 統合データ中 DynaMath の ID は 2411.00836 が正(2510.22340 は誤記)。調査精度の注意点として記録。

---

## 9. needs-human-judgment(no-push 制約下でユーザー判断が要る分岐)

1. **MathVerifier の trig 正規化フォールバックを src に入れるか**(候補 1 の PoC ステップ 2)。これは `src/llive/math/verifier.py` への変更で、研究スクリプト additive を超える。push 制約下では PR 提案までに留めるべきか、本人レビュー待ちか。
2. **OKA-05 Reformulation Corpus をガラパゴ seed で着工するか**。OKA-05 は Phase 11(MED)で、ロードマップ前倒しの是非はユーザーの優先度判断。
3. **VLM paired データ生成器を独立プロジェクトとして立てるか**。lldarwin visual_qa / VLM-FX が未実装のため、受け皿を先に作る投資判断。
4. **みゆ氏 / Mathlava コミュニティへの関与の是非**。ガラパゴ数学を FullSense の記事・デモ素材に使う場合、創始者クレジット・コミュニティとの関係構築をどう扱うか(査読なし体系の引用作法、@Galapagothmetic への連絡可否)。
5. **斜交座標図を Qiita/記事で使うか**(feedback_qiita_svg_path_and_cache の制約下)。教育素材としての採用は genuine に価値があるが、honest disclosure(「Lucas 数列の再発見であり新数学ではない」)の明記が前提。

---

## 10. honest disclosure 留保(ロマンと実体の境界)

- **over-claim していない確認**: 本報告は verdict=genuine を 1 件も立てていない。全 16 mapping の `galapagos_doing_work=false` を尊重し、ガラパゴ性が機構の本質を担う主張は一切していない。
- **「取り込める」の定義を守った**: 機構(どの部品のどこに)・先行研究・最小 PoC(CPU 可・additive)・red-flag の 4 点で具体化できたのは候補 1(VLM 生成器)と最有望 PoC(MathVerifier 修正)のみ。残りは「relabel」または「既存資産の冗長再実装」と明示した。
- **ロマンの所在**: ガラパゴ数学の魅力(加法と乗法を 1 枚の図で統一する視覚的快感、隔離進化というブランド物語)は本物で、FullSense の普及ファネル(記事・animated SVG・隔離進化思想)と物語的に強く整合する。だがそれは **表現/教育の価値**であって、**AI capability の前進ではない**。この境界を曖昧にしないことが本調査の核。
- **異常に良い話の内訳監査**: 「companion 行列が SSM を安定化」「斜交基底で VLM が改善」「6 表現=6 倍の知識」はいずれも内訳を割ると、それぞれ「既存 SDP gate の冗長 relabel(かつ unsound)」「未検証仮説 + 反証側優勢」「独立情報量 1 の同型コピー」に帰着した。feedback_benchmark_honest_disclosure の規律どおり、勝った気になる前に内訳を疑った結果である。

---

*報告書ここまで。次アクションは §5 の MathVerifier 三角正規化バグ修正(最も確実)、または §6/§9-3 の VLM 生成器(受け皿整備が前提)。いずれもユーザー判断点を §9 に明示。*
