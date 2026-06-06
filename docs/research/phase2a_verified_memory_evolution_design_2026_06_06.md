# llcore Phase 2a — Verified Memory Evolution 設計doc

作成日: 2026-06-06
対象: llcore Phase 2a (param→memory-update ギャップを埋める最小 PoC)
規律: honest disclosure 厳守 (誇張禁止)。本 doc の主張部はソース行を一次確認した内容のみ採用。
ステータス: 設計確定 (実装未着手)。

---

## 1. 目的と SSGM 時間窓

### 1.1 達成したいこと (honest crux)

llcore の証明ゲートは現状、**単一の更新カーネル遺伝子 (RWKV decay/mix/gate_str) のパラメータの性質**として
L<1 contraction を証明する (`verify_lipschitz_contraction`)。これは「カーネル param の性質」であって
「メモリ更新そのもの (a memory update event)」ではない。Phase 2a の唯一の目的は、この
**param → memory-update ギャップを最小コードで、かつ over-claim せずに埋める**ことである。

honest crux の正確な定式: 証明命題そのものは既に更新写像 `s' = f(s, x)` の不変量として書かれている
(Research 2 棚卸し済)。したがってギャップは「証明対象」ではなく「**ゲートをどの粒度の memory 概念に
掛けるか、そしてそれを過剰主張せずどう名付けるか**」にある。

### 1.2 差別化の生存核 (4 点交差)

差別化監査の結論 = 生存核は次の四点の交差点であり、5 件の隣接研究のいずれも全 4 点を**同時には**満たさない:

1. sound contraction 証明 (SMT-exact / 閉形式)
2. Transformer 記憶コアの内部 recurrent dynamics
3. 進化 / 更新ループ内の prove-then-reject ゲート (失敗 = resample / fallback)
4. 動く実装

ただし各点は**単独では既に占拠済**: contraction 証明 = InterContiNet[1] / VLA[4]、memory write gate = SSGM[2]、
prove-then-reject in loop = SafeAdapt[3]、verified + 継続更新 = Socrates-CCL[5]。
よって新規性は「応用先」ではなく「**SMT-exact × 離散 ChangeOp / 進化候補ごとの再証明 × 動く実装**」の
交差で主張する。

### 1.3 SSGM 時間窓 (なぜ今やるか)

SSGM (arXiv 2603.11768, 2026-03-12 投稿, Jinan University) は LLM agent の memory bank への
**write gate (NLI 矛盾検出)** を理論アーキとして提案した。一次確認した事実:

- **概念フラグの先取り**: SSGM は「memory write gate for verified memory evolution」の応用枠そのものを
  公的に先取りした。**したがって応用アイデアの新規性は主張できない**。
- **証明は非形式**: 唯一の定理 (Theorem 1 "Bounded Semantic Drift", O(N·ε_step)) は明示的に
  "Proof Sketch"。contraction / Lipschitz / 固定点の議論なし。gate (⊧⊥) の soundness 証明なし。
  gate が定理証明器か neural NLI 分類器か symbolic かも未規定。
- **実装ゼロ**: 著者自身が "Rather than a specific software implementation, SSGM provides a rigorous
  theoretical architecture and a set of design principles" と明言。コード・実験・ベンチマークなし。
  実装を "the community" に呼びかけている。

**含意 = 実装先取りの時間窓が有限**。SSGM は実装をコミュニティに公募しており、後追い実装論文が
いつ出てもおかしくない。Phase 2a は tightly time-box すべき。我々の防衛的公開ポジションは:

> SSGM は NLI ベースの理論 write gate を proof sketch + 実装ゼロで提案した。我々は、進化する更新
> カーネルに対する **sound (SMT/閉形式で機械検証された) contraction-class ゲートと動く実装**を提供し、
> Banach 自己修復を実証する。

---

## 2. 2 案の比較

| 観点 | Case A: Verified External Memory Bank (slot-set write/update gate) | Case B: Trajectory-Tube Memory Invariant Gate |
|---|---|---|
| memory の定義 | 外部 (key,value) スロット集合。値 state `S` が証明対象 | RWKV recurrent state 軌道 `s_0..s_T` (外部 bank なし) |
| memory update step | (1) 1 スロットへの 1 write = `eval_step`、(2) 更新規則の ChangeOp 変更 | 1 step `eval_step` / 進化候補 = 新カーネル |
| 証明する不変量 | I1 bank-norm 有界 + I2 write contraction L<1 + I3 rule-change refinement | tube 含包: limsup‖s_act−s_ref‖∞ ≤ r = G·w̄/(1−L) |
| 主証明エンジン | `verify_lipschitz_contraction` (scalar) / coupled backends (多スロット) | `tracking_tube()` (Banach 系の派生定理、新規 Z3 不要) |
| 既存実装の流用度 | スカラ路は高い。**coupled 路は実体が無い (下記)** | 高い。tube reporter は `admits` 付きで既に出荷済 |
| additive 性 | スカラ路 = additive。**coupled 路 = 新サブシステム (非 additive)** | gate_mode 1 分岐 (~40-60 行) + research/ PoC のみ |
| 推定規模 | スカラ ~530 LOC / 数日。coupled = 数日では不可能 | 小 (src ~40-60 行 + research ~150-200 行)、数日未満 |
| 敵対レビュー fatal | なし (全 fixable)。ただし**看板の coupled 部が虚構**という致命的 fixable | なし (全 fixable)。defect は L 証明の provenance 誤標と gate-nesting 誤主張 |
| 最大の落とし穴 | 「外部 memory bank」の看板が現実装と乖離 (bank/retrieval 不在)。スカラ bank は単一 state の N コピー = 単なる relabel | tube gate を「Z3-exact」と謳うと referee が tracking_tube.py を開いた瞬間に崩れる |

### 2.1 敵対レビューで確定した一次事実 (両案に共通の地雷)

実装着手前に必ず守るべき、ソース行で確認済の事実:

- **`refinement.py:209-218`**: `verify_refinement_single` は z3 不在時 `ok=True` を返す = **fail-OPEN**。
  両案の提案文が「refinement は fail-closed」と述べているのは**誤り**。新 glue は `used_z3=False` を
  reject として扱い直さねばならない。
- **`refinement.py:232-237`**: refinement の Z3 encoding は `tanh_after` を [-1,1] 自由にし、ChangeOp 後の
  mix/gate を**意図的に無視**する。よって refinement は contraction を判定**できない** =
  「boundedness フィルタ (slack ε 付き)」であって contraction 証明ではない。
- **`tracking_tube.py:189`**: `contraction_ok = bool(L < 1.0)` は achievable-t box 上の **numpy float 比較**で
  あり、Z3 unsat 証明ではない (tracking_tube.py:186-188 が自ら「Z3/InfNormBackend を経由しない」と注記)。
- **`minimal_ga.py:435-441`**: `evolve()` は `gate_mode != "none"` かつ `codec` 指定で **ValueError を raise**。
  coupled gene は既存コードでは in-loop でゲートできない。
- **`src/llcore/` に coupled forward map は存在しない** (grep 確認: `eval_step`/`run_sequence` のみ。
  `eval_coupled`/`run_coupled`/`coupled_step` なし)。coupled backends は **Jacobian を組む verifier 専用
  ヘルパ**であって state を前進させない。
- **`invariants.py:392-405`**: `verify_lipschitz_contraction` は z3 不在時 `contraction=None` +
  `L_upper_bound` を返す。`L_upper_bound` は「assumed・未検証」。caller が `None` を reject 扱いにする
  責任を負う (= 新 glue の live trap)。

---

## 3. 敵対レビューで生存した推奨案

### 3.1 結論: Case B を主軸、Case A のスカラ核を補強的に採用するハイブリッド

両案とも fatal は無く全 fixable。だが敵対レビューを通すと **Case B の方が「看板と現実装の乖離」が
本質的に小さく、additive 性が真**である。理由:

- **Case A の致命的 (fixable) 欠陥は看板そのもの**: 「外部 memory bank の write gate」は llcore に
  bank/retrieval が無い以上、現実装と乖離する (Research 2)。SSGM の owned 概念にも正面衝突する。
  唯一 truly-additive な Case A 路 = スカラ対角 bank = **単一 state の N 独立コピー** = 既存 single-gene
  PoC の block-diagonal relabel であり、「メモリ bank 構造」という VLA/SSGM が強い軸では**むしろ弱い**。
  「cross-slot interference (SSGM が hand-wave する部分)」を埋める coupled 路は、新 coupled gene +
  codec + forward map + gated 配線 + coupled ChangeOp/refinement を要し、**数日では不可能・非 additive**。
  つまり Case A の SSGM-beating セールスポイントは未スコープの coupled 路に全乗りしている。

- **Case B の defect は局所的かつ標識訂正で済む**: tube 不等式 eq(4)-(5) は **本物の定理** (Banach +
  Lipschitz 合成、明示的定義 e_t/L/G/w̄ + 幾何級数収束 + 参照が系自身の解なので ρ_feas=0)。
  SSGM の Proof Sketch とは「定理の厳密さ」軸で真に差がつく。tube reporter (`admits` 付き) は
  既に read-only で出荷済で、Case B は**それを gate として配線するだけ**。additive 性が真。

- **アンチ re-skin 証拠が数値的に確認済**: contracting (L<1) gene の中で tube 半径 r=G·w̄/(1−L) は
  大きく散らばる (レビューで 20000 gene sweep: contracting 14190 件中 tube 半径 0.0–65.2、p50≈0.031)。
  よって非退化な r_max は contraction gate が admit する gene の**真部分集合**を reject する =
  trajectory_tube gate は contraction gate より**識別力で強い**ことが demonstrable (vacuous re-skin ではない)。

### 3.2 ハイブリッドの正確な切り分け

- **主軸 = Case B**: gate 対象 = 進化生成された (非固定の) スカラ更新カーネルの **trajectory-tube 含包**。
  これが VLA[4] (固定 1 設計の一回解析証明) が踏んでいない「param → 実現された state 軌道の有界性」軸を
  最小コードで取りに行く。
- **補強 = Case A のスカラ核 (bank ではなく "named-slot" 解釈)**: `eval_step` を「named memory slot の
  1 write」として **numerical-identity test で literal に同一**であることを証明する (= bridge の唯一正当な
  anchor)。これにより「proven object = 実際の memory write step」を honest に言える。**ただし「bank」
  「external」「cross-slot」「retrieval」の語は使わない**。

### 3.3 採用しない (敵対レビューで落ちた看板)

- Case A の coupled "memory bank" 全体 (非 additive・実体不在)。
- 「first sound contraction-class write gate for an evolving **memory bank** with Banach self-healing」という
  headline (bank が虚構)。代わりに「**sound contraction-tube gate over the internal recurrent memory
  trajectory of an evolving update kernel**」を看板にする。

---

## 4. 推奨案 (Case B 主軸ハイブリッド) の最小 PoC 実装手順

### 4.1 Falsifiable 命題 (反証可能・誇張なし)

> `gate_mode="trajectory_tube"` (admits = L<1 ∧ tube 有限 ∧ r = G·w̄/(1−L) ≤ r_max) を
> `minimal_ga.evolve` に配線し、fitness = `CopyTask(delay=k>0)` を bounded input disturbance w̄ 下で評価する。
> 対 control (`gate_mode="none"`) で:
> (P1) trajectory_tube が admit した**全カーネル**で、外乱下軌道の実測 limsup‖e_t‖∞ ≤ certified tube r
>      (N≥64 seed で 0 件違反)、かつ
> (P2) `verify_lipschitz_contraction.contraction=True` だが r>r_max のカーネルを reject する
>      (`gate_stats.n_rejections > 0`) = trajectory gate は contraction gate の真部分集合に絞る、かつ
> (P3) named-slot write (= `eval_step`) は数値的に既存 `eval_step` と恒等 (bridge が虚構でない)。

**反証条件**:
- (a) admit したカーネルの実測軌道誤差 > certified tube r → 定理 / 実装の破綻。
- (b) trajectory_tube と contraction gate が同一集合を admit → r_max が緩すぎ degenerate (re-skin)。
- (c) delay>0 memory タスクで gated 集団の best fitness が single-step L<1 gate と統計的に区別不能 →
      trajectory lift が memory 保持に何も買っていない (honest disclosure red flag)。

### 4.2 証明する不変量

- **主不変量 (trajectory tube)**: 任意の admit カーネルについて、bounded disturbance ‖d_t‖∞ ≤ w̄ 下で
  limsup_t ‖s_act,t − s_ref,t‖∞ ≤ r = G·w̄/(1−L) < ∞ (s_ref = 同カーネル + 参照入力の系自身の解)。
- **補助不変量 (bridge anchor)**: named-slot write 写像 = `eval_step` (genes.py:98) と literal 同一
  (relabel: slot value = s, write delta = x)。

### 4.3 Soundness 論拠 (継承であり再導出ではない)

- **tube 定理は本物 (SSGM の sketch と差がつく軸)**: e_t = s_act−s_ref, F が state 方向 L-Lipschitz /
  入力方向 G-Lipschitz のとき ‖e_{t+1}‖∞ ≤ L‖e_t‖∞ + G·w̄。L<1 で幾何級数が収束し
  limsup ≤ G·w̄/(1−L) (Banach + Lipschitz 合成)。参照が系自身の解なので feasibility 残差 ρ_feas=0
  (eq(5) が完全に sound になる唯一のケース)。
- **G は閉形式上界**: G = max_i (1−decay_i)·Σ_j|V_ij| は t=1 端点での sup (上界)。
- **fail-closed 規律 (新 glue の責任)**: z3 不在 / sat / timeout / tube=∞ / r>r_max は全て **reject**。
  `_gate_admits` の "hard True only" 規律を継承する。

#### 重要 — honest 訂正 (敵対レビューが暴いた over-claim を本 doc で先に潰す)

1. **tube gate の L は Z3-exact ではない**。`tracking_tube.py:189` の `contraction_ok` は achievable-t box
   `[t_min,1]` 上の **閉形式 numpy 比較**であり、`verify_lipschitz_contraction` の free-t∈[0,1] box 上の
   **Z3 unsat 証明とは別物**。論文 / README では「**閉形式 (Banach 系) で導かれた tube 境界**」と書き、
   「Z3-exact contraction + tube」と書いてはならない (referee が tracking_tube.py を開いた瞬間に崩れる)。
   Z3-exact なのは別系統の `verify_lipschitz_contraction` であり、これを使う場合は**明示的に二系統**として
   報告する。
2. **2 つの gate は nested でなく non-comparable**。free-t L (Z3 gate) ≥ achievable-t L (tube gate)。
   よって「trajectory_tube は contraction gate より strictly stronger」は無条件には成り立たない。
   free-t L≥1 (Z3 reject) かつ achievable-t L<1 (tube admit) の gene が両立しうる。(P2) の「真部分集合」
   主張は **同一の L 定義 (同一 box) で揃えて測った上で** r_max が binding していることを示して初めて
   成立する。box mismatch が混入しないよう、アンチ re-skin 比較は**両 gate を同一 L 定義で揃える**こと。
3. **cross-check ツールの誤帰属を避ける**: tube 半径 r=G·w̄/(1−L) の検証は **64-seed 外乱ドライバ**
   (実測 e_t) で行う。`empirical_lipschitz` (invariants.py:455) は state 方向 L の有限差分推定のみで
   G も e_t も測らないため、tube 半径の cross-check には使えない (L 単体の sanity にのみ使う)。

### 4.4 既存部品の再利用 (additive 性)

src/ への変更は `_gate_admits` の 1 分岐 + `evolve()` の数 kwarg に限定。それ以外は research/ に置く。

| 部品 | 用途 | 変更 |
|---|---|---|
| `src/llcore/verifier/tracking_tube.py:138` `tracking_tube()` | r=G·w̄/(1−L) + `admits` 既出荷 | 変更なし (gate として呼ぶだけ) |
| `tracking_tube.py:87/115` `input_gain_inf`/`state_lipschitz_inf` | 閉形式 G, L | 変更なし |
| `tracking_tube.py:219` `_coupled_arrays_any` | scalar gene を n=1 coupled に持ち上げ | 変更なし |
| `src/llcore/evolution/minimal_ga.py:232` `_gate_admits` | gate dispatch | **1 分岐追加 (trajectory_tube)** |
| `minimal_ga.py:353` `evolve(gate_mode=...)` | fail-closed resample + fallback + GateStats | **w_bar/r_max kwarg 追加** (default は gate-off 等価) |
| `_FALLBACK_GENE` (decay=0.5,mix=0,gate_str=0) | G=0 → tube=0 → 新 gate も通過 | 変更なし (fallback 妥当性維持) |
| `src/llcore/state_update/genes.py:98/135` `eval_step`/`run_sequence` | s_ref / s_act 生成 + bridge anchor | 変更なし |
| `src/llcore/fitness/tasks.py:113/222/245` `CopyTask(delay)`/`evaluate_gene`/`calibrate_baseline` | memory-horizon fitness | 変更なし |
| `src/llcore/verifier/invariants.py:351/455` `verify_lipschitz_contraction`/`empirical_lipschitz` | L<1 二系統参照 + L sanity | 変更なし |
| `research/verified_evolution/exp_b_runner.py:39-124` | gated_evolve + CopyTask + control の既配線 A/B | 雛形として流用 |
| `research/target_trajectory_poc/poc_target_trajectory.py:109` `rollout_with_disturbance` | 外乱注入パターン | **port (CoupledNDGene → scalar run_sequence 再ポイント, ~20-30 行)** |

### 4.5 実装ステップ (順序)

1. **src 配線 (additive)**: `minimal_ga._gate_admits` に `gate_mode="trajectory_tube"` 分岐を追加。
   scalar `StateUpdateGene` を `_coupled_arrays_any` で n=1 に持ち上げ → `tracking_tube(gene, w_bar=W_BAR,
   r_max=R_MAX).admits` を返す。`evolve()` に `w_bar`/`r_max` kwarg を通す (default は gate-off 等価で
   `gate_mode="none"` を **byte-identical** に保つ)。fail-closed: `tracking_tube` が admit=False / 例外なら reject。
2. **外乱チェッカ (research/, port)**: `run_sequence` (genes.py:135) を 2 回 (s_ref = x_ref、s_act = x_ref +
   uniform d∈[−w̄,w̄]) ×64 seed で回し、steady-state 後半の実測 limsup‖e_t‖∞ を返す。
   `poc_target_trajectory.py` の `rollout_with_disturbance` を **scalar 基板に再ポイント** (substrate が
   CoupledNDGene のため copy でなく port)。これは tube **定理の cross-check** であって gate の soundness の
   一部ではない (4.3 訂正 3)。
3. **bridge anchor test (research/ または tests/)**: named-slot write == `eval_step` の数値恒等を assert
   (P3 = bridge が fork でない証拠)。
4. **fitness**: `evaluate_gene` + `CopyTask(delay=k)`, k∈{0,4,8} (delay>0 が真の memory horizon)。
   先に `calibrate_baseline` (tasks.py:245)。
5. **3-arm A/B (research/)**: 同一 seed で `evolve()` を `none` (control) / `contraction` (現 single-step gate) /
   `trajectory_tube` (新) の 3 系統。pop=20, gen=20, 複数 seed。`assert_none_matches_src` 相当で control 一致を担保。
6. **falsifiable 検証**: (P1) admit 全 gene で実測誤差 ≤ certified r (0 違反)。(P2) `contraction=True` だが
   r>r_max の gene を reject = `gate_stats.n_rejections>0` を **同一 L 定義で揃えて**確認。(P3) 恒等 test pass。
7. **VERDICT.md (research/, 一次成果物)**: arm 別 tube-vs-実測 表 + contraction gate に対する delta +
   honest 留保 (参照妥当性は未証明 / ρ_feas=0 は参照が系自身の解だから / w̄ は離散入力では弱い)。
   `feedback_benchmark_honest_disclosure` 規律: gated arm が「綺麗すぎる」なら r_max が never-bind に
   退化していないか per-gene verdict を dump して確認。

### 4.6 行き止まり回避 (一次確認に基づく)

1. **「verified external memory bank write gate」と謳わない** — bank/retrieval が無く (Research 2)、SSGM の
   owned 概念に正面衝突する。看板は「進化する更新カーネルの内部 recurrent memory 軌道に対する
   sound contraction-tube ゲート」。
2. **trajectory_tube を contraction gate に退化させない** — r_max が緩すぎると admit 集合が一致し lift が
   vacuous (re-skin trap)。PoC は**「contracting (L<1) だが trajectory_tube が reject する gene を ≥1 件
   提示」**して strict 追加力を実証する。提示できなければ (c) で falsified。
3. **参照軌道を「理想 memory」と過剰主張しない** — 定理は GIVEN 参照周りの追従誤差を bound するだけ。
   参照が「良い」memory かは task fitness の責任で verifier の責任ではない。
4. **「contraction」「continual」を headline 語にしない** — InterContiNet (2206.07996) と語彙衝突。
   方法論を明示して「**SMT-exact prove-then-reject over discrete change-ops in an evolutionary loop**」と
   軸を切る。
5. **z3 不在を黙って PASS にしない** — refinement.py / invariants.py は z3 不在で fail-OPEN または None を
   返す (4.3 / §2.1)。新 glue は `used_z3=False` / `contraction is not True` を **reject** として扱う。
6. **coupled "bank" を数日でやろうとしない** — forward map / codec / gated 配線が全て未実装 (非 additive)。
   Phase 2a のスコープ外。

---

## 5. Honest 留保とリスク

### 5.1 主張してよいこと / よくないこと

- **言ってよい**: soundness (Banach 系の本物定理 vs SSGM の sketch) + 動く実装 (gate in loop vs SSGM の
  実装ゼロ) + param → state 軌道の bridge (固定 1 設計の VLA に対し、進化候補ごとに再評価)。
- **言ってはいけない**: (a) 応用アイデア (memory write gate / verified memory evolution) の新規性
  (SSGM が 2026-03-12 に概念フラグ取得済)。(b) tube gate が「Z3-exact contraction」(実体は閉形式 numpy 比較)。
  (c) trajectory_tube が無条件に contraction gate より strictly stronger (box mismatch で non-comparable)。
  (d) 「external memory bank」(bank 不在)。

### 5.2 残る本質的弱点 (honest)

- **bridge は半分**: tube は L も G も**カーネル param の閉形式端点量**から計算され、実現された軌道に対する
  新規 Z3 query ではない。64-seed 外乱 run は**定理の cross-check** であって gate soundness の一部ではない。
  防衛的に正確な framing = 「param-contraction → param 由来の trajectory-tube 境界」であり、宣伝文句の
  「memory-update-event gate」より厳密には弱い。これを doc / 論文で先に明言する。
- **VLA に対する新規性は薄い**: VLA[4] は memory 更新写像の contraction を解析証明済 = Phase 2a が埋めると
  宣言した param→memory-update gap を既に踏破。我々の wedge は (a) 進化候補ごと再証明、(b) SMT-exact vs
  pen-and-paper、(c) tube/input-gain 次元の追加。(a)+(b) は**方法論差**、(c) は textbook 数学。よって
  substantive 新規性は単一アイデアでなく**交差 (SMT-exact × 進化候補ごと × tube-with-r_max × 動く実装)**。
- **CopyTask の正直注記**: `CopyTask` の fitness は code docstring 自身が「fixed-readout probe-based
  fitness ... not gene-pure fitness」と述べる。memory probe としては妥当だが「real memory horizon」を
  過剰主張しない。

### 5.3 最大リスク (1 つ)

**VLA (arXiv 2605.11196) の先行踏破による「焼き直し」リスクが最大。** VLA は既に「メモリ更新写像そのものの
contraction を解析証明」しており、これは Phase 2a が埋めると宣言した param→memory-update gap を**先に
踏んでいる**。Phase 2a が gate 対象を「kernel param の L<1」から「実際に実現された memory 軌道の含包」へ
真に昇格させ、かつ **VLA が扱わない非固定 (進化生成された) 更新カーネル**で per-candidate に再証明して
fail-closed ゲート化しない限り、VLA に対する差別化は「進化 × SMT」の**方法論差のみに痩せる**。
これは焼き直し回避の必須条件であり、(P2)/(P3)/反証条件(c) はまさにこのリスクの検出器として設計してある。

---

## 6. 次アクション

1. **time-box 宣言**: SSGM 実装窓が有限のため Phase 2a を数日以内に切る (実装 §4.5 ステップ 1-7)。
2. **src 1 分岐着手**: `minimal_ga._gate_admits` に `trajectory_tube` 分岐 + `evolve()` kwarg (additive、
   `gate_mode="none"` byte-identical 維持)。fail-closed を新 glue で明示実装。
3. **外乱チェッカ port**: `poc_target_trajectory.py:109` を scalar `run_sequence` 基板に再ポイント (~20-30 行)。
4. **3-arm A/B + VERDICT.md**: none / contraction / trajectory_tube を同一 seed で。アンチ re-skin は
   **同一 L 定義で揃えて** (P2) を確認。honest disclosure 規律で「綺麗すぎ」を per-gene dump で点検。
5. **VLA[4] / InterContiNet[1] 全文再確認**: 着手前に手法詳細 (契約条件・proof 対象) を全文精読
   (Research 3 が PDF 部分抽出に留まったため)。
6. **防衛的公開の文面確定**: §1.3 のポジショニング文 + §5.1 の「言ってはいけない 4 点」を README / 論文の
   差別化節に固定。

---

## 参照 (一次確認済)

- [1] InterContiNet / Weight Interval Constraints — arXiv 2206.07996 (ICML 2022)
- [2] SSGM — arXiv 2603.11768 (2026-03-12)
- [3] SafeAdapt — arXiv 2604.09452 (2026)
- [4] Variational Linear Attention (stable associative memory) — arXiv 2605.11196 (2026)
- [5] Certified Continual Learning (Socrates) — arXiv 2407.06697
- llcore ソース行参照は §4.4 / §2.1 に file:line で記載 (実装手順用)。
