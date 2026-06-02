# 進化が「効く」構造的条件 — 4 ステップモデルの先鋭化

*2026-06-02 / cross-method synthesis (5-Whys × TRIZ × RAD corpus × canonical web)*

対象とする作業モデル:

> **Evolution = ⟨structured chance⟩ × ⟨prepared honest recognition⟩ × ⟨long-term retention⟩, looped.**

積（×）の形が本質である。どれか 1 項が 0 になれば全体が 0 になる。本ドキュメントは、4 つの独立プローブ（5-Whys 根本連鎖／TRIZ 矛盾解消／RAD コーパス照合／正典科学 web 検証）が **どこで一致し、どこで先鋭化され、どこで挑戦されたか** を統合し、ユーザー自身の 4 ステップ直観を一段深い構造へ引き上げる。

---

## 1. 先鋭化されたテーゼ（1–2 文）

**進化が「効く」のは、矛盾する性質を 1 点で両立させようとせず、異なる階層・時間・条件に分離した時に限る。** すなわち「速い・盲目・可変な frontier（変異の前線）」「遅い・先見的・安定な core（証明済みの核）」「最遅・厳格・不可逆な ratchet（正直な認識ゲート + 一方向保持）」を **層として同時に重ねる** ことで、新規性の起源（盲目でしか入らない）・誤りの増幅（認識が唯一の真偽ゲート）・高次元欺瞞地形（多様性でしか拾えない）という 3 つの根本制約を、トレードオフの妥協ではなく **分離によって** 一挙に解く。

一言で言えば: **進化はどちらかを選ぶのではなく、層に分けることで効く（layering, not choosing）。**

---

## 2. 根本原因のスパイン（5-Whys が掘り当てた最深原理）

5 本の why-chain が共通して底打ちした原理。最初の 3 つは論理的・証明可能に「固い」。P1 にだけ正直な範囲限定がある。

### P1 — 新規性は定義上、先見では起源しえない（情報の data-processing inequality）
決定論的関数（＝先見・モデル・勾配・プランナ）はその入力の情報量を増やせない。「X へ向けて探索を誘導する」には、既に「X に近い＝高得点」と採点できる事前モデルが必要で、そのモデルは自分が既に表現している空間の閉包の中しか順位付けできない。**真に新しいもの＝閉包の外**。ゆえに net-new な情報の唯一の搬入路は、現モデルの予測と **脱相関した（＝モデルから見て盲目な）サンプル**。これが Campbell の BVSR が「偶然そうなる」のではなく **認識論的必然** である理由 — 非盲目な変異は定義上、既存知識と冗長。
- **正直な範囲限定（唯一の seam）**: この連鎖は **fundamental novelty（新しい原始要素/次元）** に対して厳密だが、**combinatorial novelty（既知原始要素の新しい配列、例: transformer が未見の文を生成）** に対しては過剰主張。組合せ的新規性は閉包内＝原理上は先見可能。BVSR の必然性が噛むのは「新しい原始要素が要る frontier」だけ。

### P2 — optimizer's curse + 再検証なき保持 = 楽観的誤りの不可逆ラチェット
ノイズ付き推定の max は上方バイアスを持つ（E[max X̂ᵢ] ≥ max E[Xᵢ]、勝者の呪い）。保持はこの推定器バイアスをシステムの prior に積分する。低域通過フィルタが DC オフセットを溜めるのと同じ。**選択は、選択自身が守っている誤りを訂正できない**（凍結された elite）。我々の実験そのもの: elitism が幸運なノイズ fitness 0.473 を凍結 → fresh-seed 再評価で真値 0.183 が露呈。ゆえに認識は **unbiased かつ新証拠で再検証された** 正直さでなければ、系は自分の測定アーチファクトを最適化する。**真偽判定はこの 1 リンク（recognition）にだけ宿る。**

### P3 — 増幅はフィードバック位相の性質であって、内容の真偽の性質ではない
記憶を持つ正帰還ループは **内容非依存の乗算器**。retain × build-on という同一演算を、真値の gain にも偽値の error にも符号を読まずに適用する。**累積する力（創発）と累積する脆さ（化石化した誤り）は同一臓器（retention）を共有する分離不能な双子**。だから真偽は **上流の recognition でしか入れられない** — これがモデルの中心矛盾。

### P4 — 多様性維持は「欺瞞 × 高次元」への条件付き保険であって、一般的改善ではない
QD/MAP-Elites が load-bearing になるのは、目標が **(a) 直接サンプリングに対し measure-zero（次元の呪い・測度集中）かつ (b) 勾配に隠れている（欺瞞）** の両方が成り立つ時だけ。どちらか 1 つを外せば — 低次元化が直接到達性を回復、平滑化が先見を回復 — より安い手法（random-restart hill-climbing, RR）が証明可能に優越する。QD の唯一の独自貢献は「即時 fitness は負だが、谷を渡す橋になる accidental stepping-stone を保持する」こと。**No Free Lunch（Wolpert–Macready 1997）が、この主張が普遍ではなく地形条件付きでなければならない形式的理由を与える。**

### P5 — Pasteur 因数分解: 設計の手が届くのは「認識」因子だけ
novelty-capture = P(accident) × P(recognition | accident)。設計は第 2 因子を ~1 に上げられるが、第 1 因子を **方向づけ（aim）** はできない（予測不能を予測することになる）。正直な精緻化: 設計は試行の **頻度（brute volume × 豊かな環境）を上げられるが、個別の勝ちを aim できない**。controllable 因子（recognition）を極めるほど、uncontrollable 因子（trigger）への依存が最大化する。

**スパイン総括（収束した一文）**: 進化は **真偽判定を 1 リンク（recognition）に隔離し、他のリンクを意図的に真偽盲目にする** ことで効く。盲目変異は入れる係（判定不可なので盲目でなければならない）、保持は増幅する係（判定不可な機械）。ユーザーが加えた「勝利を確信する」ステップが keystone であると同時に最も危険なのは、**ループ全体で真偽が入れる唯一の場所** だから — ここの誤りは機械の他の部分では訂正不能。

---

## 3. TRIZ による解消 — 階層分離（LAYERING, not choosing）

5 つの矛盾（探索 vs 活用、安定 vs 変化、速度 vs 頑健、先見 vs 新規性、盲目 vs 正直認識）は別々の問題ではなく、**「候補に適用する厳格さ/知識/可変性が同時に低くも高くもなければならない」** という同一の物理的矛盾を 5 つのパラメータで見たもの。物理的矛盾（同一パラメータが反対の値を要求）は妥協では解けず、**分離** でのみ解ける。

### 分離の三本柱

| 分離軸 | 解く矛盾 | 実現する発明原理 | 具体実装 |
|---|---|---|---|
| **TIME（時間）** | 探索↔活用、盲目↔正直認識 | 19 周期作用 / 20 有用作用の連続 / 15 ダイナミック化 | simulated annealing、失敗時に変異率爆発（antifragile mutation） |
| **SPACE（空間）** | 安定↔変化（部分）、探索↔活用（部分） | 3 局所性 / 1 分割 / 4 非対称 | island-model GA、MAP-Elites のニッチ（= 我々の ③） |
| **SCALE/HIERARCHY（階層）** ★master | 安定↔変化、速度↔頑健、**先見↔新規性（根本）** | 1 分割 / 7 入れ子 / 30 柔軟殻 / 10 予備作用（ラチェット） | **2 層ゲノム（安定 core + 可変 prompt）**、Maynard Smith & Szathmáry の major-transition ラチェット |

### マスター解 — 階層分離が落とす構造

```
LEVEL (slow ↔ fast)        ROLE                          保持する値
────────────────────────────────────────────────────────────────────
SUPER-SYSTEM (最遅)   正直認識ゲート + 長期保持        厳格・凍結前に fresh-seed 再検証・不可逆
  "the ratchet"
────────────────────────────────────────────────────────────────────
SYSTEM (中速)         安定 core / 証明済みゲノム        低可変性・先見が内部モデルで峰へ直行（活用）
  "the core"
────────────────────────────────────────────────────────────────────
SUB-SYSTEM (最速)     可変 periphery / frontier         高可変性・盲目変異・anomaly を自由生成（探索）
  "the frontier"
────────────────────────────────────────────────────────────────────
```

- **先見↔新規性（C4・根本）が溶ける**: frontier は盲目（新規性はここで起源、モデルがないので循環しない）、core は先見的（モデルで精緻化）、ratchet は正直な判定者。Campbell の循環「勝者を先見するには既に符号化していなければ」は **1 つのレベル内では真、レベル間では無関係** — 先見するレベルは生成せず、生成するレベルは先見しない。これは **Campbell 自身の解（vicarious selector の階層）**: 上位の遅い selector が下位の盲目試行を「代理」するが、それ自身は自分のタイムスケールで盲目変異の産物。**先見＝保持・ラチェットされた過去の盲目的勝利の結晶**。だから先見は新規性を起源できず（C4 維持）、精緻化するだけ（ユーザーの点 5）。
- **安定↔変化（C2）が溶ける**: 可変性 = sub で高、super で ~0。同じ「ゲノム可変性」が異なるレベルで反対の値 = **2 層ゲノム**（input にある `project_llive_genome_two_layer` / reincarnation-rod 構造）。
- **速度↔頑健（C3）が溶ける**: 速い活用ループは sub/system（安く、間違ってよい＝誤りが安く可逆）、遅い頑健なラチェットは super（高価・正直・不可逆＝だから正しくなければならず、凍結前に再検証するから正しい）。

**Maynard Smith & Szathmáry の major transitions への写像**: 各遷移（複製分子→染色体→真核→多細胞→社会）は **新しい階層レベルと新しいラチェットの設置**。進化が「もっと働いた」時、1 つのレートを調整したのではなく、より遅く・厳格で・高いレベルを足した。

---

## 4. 文献での grounding（検証済みと未検証を正直に）

| 因子 | ステータス | 正典アンカー |
|---|---|---|
| (1) 新規性の trigger は盲目的偶然、先見は起源できない | **確認** | Campbell BVSR (Psychol. Review 1960; 1974); Lehman–Stanley objective paradox (2011/2015) |
| (2) 偶然は認識+保持されて初めて trigger、認識が危険ステップ | **確認 + 改名** | Pasteur 1854; Goodhart 1975 / Campbell's Law 1976; noisy-TV → surprise でなく learning-progress を報酬に (Schmidhuber, Oudeyer) |
| (3) 純粋でなく structured chance | **確認** | Kauffman adjacent possible (*Investigations* 2000); NK epistasis (Kauffman & Levin 1987 / Weinberger 1989) |
| (4) 多様性は欺瞞/高 K 地形でのみ load-bearing、平滑/低 K では RR が勝つ | **確認、地形条件付き** | NK の K ダイヤル; MAP-Elites (Mouret & Clune 2015); No Free Lunch (Wolpert–Macready 1997) が普遍主張を禁じる |
| (5) 偶然=探索（novelty）、先見+正直認識=活用（精緻化） | **確認、ただしひねり** | Schwartenbeck/Friston 2013: explore と exploit は 1 つの expected-free-energy 目的の 2 項 |

### RAD コーパスの主要ヒット（AI/最適化プロキシ — 生物学正典は不在）
- **(4) を最良に支持**: "Objectives Are All You Need"（Boldi et al. 2311.02283、欺瞞域では objective 分解が QD に勝ち、非欺瞞 illumination では QD が勝つ）; "Quality-Diversity Can Provably Be Helpful"（Qian et al. 2401.10539、NP-hard クラスで MAP-Elites が多項式時間、単目的 EA は指数時間）; JEDi（2405.04308、「ちょうど十分な多様性」）。
- **(2) を heuristic から構造定理へ昇格**: **"Reward Hacking as Equilibrium under Finite Evaluation"**（2603.28063）— **有限評価** 下で reward hacking は「訂正可能なバグでなく構造的均衡」と証明。Goodhart 領域 → Campbell 領域の遷移を命名。**0.473 凍結事件の形式化**。"Reward Hacking Benchmark"（2605.02964）は「正直解が tractable な複雑度閾値以下でのみ alignment が hacking を抑制」と経験的に補強 = 認識の正直さは regime 依存。
- **(1) への挑戦**: LoongFlow（2512.24077）/ ShinkaEvolve（2509.19349）= 推論誘導（非盲目）変異が盲目変異より高効率。**(1) は「先見は prior の外では起源できない」と再定義すれば生き残る** — 豊かな prior の内側では guided が blind に勝つ。
- **③ のための重要な精緻化**: **DOSSIER**（Hernandez et al. 2204.13839）= 探索を「diversity exploration」と「valley-crossing exploration」に分解し、両者は dissociate する。lexicase は多経路に強いが谷渡りでは random search より弱い。**「欺瞞地形には QD」は粗すぎ — 多様性機構は欺瞞の種類に合わせねばならない。**

### Free-Energy / Active Inference — 部分適合 + 1 つの真の緊張
Schwartenbeck, FitzGerald, Dolan & Friston (2013) は「surprise 最小化」と「novelty 探索」の矛盾を **expected free energy** で解消（utility 項=活用 + entropy/information-gain 項=探索）。これは点 5 にきれいに写像。**緊張**: 強い FEP は「どこを探索するか」をモデルが推論する（=先見の一種）と言い、ユーザーモデルは「新規性は盲目」と言う。和解 = active inference の prior 自身が「natural selection で獲得」された盲目変異+選択の産物（= Campbell の vicarious selector）。**「進化は active inference の一形態か、単なる類似か」は学界で未解決** — モデルは FEP 統一を仮説として扱うべき。

---

## 5. 我々の ③ 研究との接続

- **③（diversity = MAP-Elites/QD）は frontier-blindness の機械**: 即時 fitness を無視して behavioral niche で保持することで、谷の底にある負 fitness の stepping-stone を生かす。これが P1（盲目でしか新規性は入らない）と P4（measure-zero かつ勾配隠れ）を同時に満たす唯一の構造。
- **平滑/低次元で不要な理由**: 目標 basin の体積分率が非消失（P4 の Why-2）→ RR が直接サンプリングで basin に入り、先見（hill-climbing）が峰へ直行。保持すべき stepping-stone が存在しないので QD の機械は dead weight。**BG9（kernel choice は低次元 → RR が直接サンプル → ③ は構造的に RR に勝てない）はここから clean に落ちる。**
- **GPU full-LLM テストへの予測**:
  1. full-LLM のパラメータ/プロンプト空間は **高次元** だが、**欺瞞的とは限らない**。P4 は「両方」を要求する。空間が高次元でも勾配整合（uni-basin）なら、先見的変異（LoongFlow/ShinkaEvolve 型の reasoning-guided mutation）が ③ に勝ちうる。
  2. ③ が勝つ条件 = fitness 地形に **谷を渡らねば届かない隠れた良 basin** がある時のみ。だから GPU テストは「地形が欺瞞的か」を先に診断すべき（例: RR baseline が局所最適に固着する vs スムーズに改善する）。
  3. DOSSIER の警告: ③ が「多様性」を出していても「谷渡り」をしているとは限らない。**谷渡り能力を別途測れ**（fitness-sharing 系 vs lexicase 系で挙動が割れる）。

---

## 6. 直観を先鋭化する takeaways + 新規仮説

### Takeaways（4 つ）
1. **進化は「どちらか」でなく「層」で効く。** 探索 vs 活用・盲目 vs 先見・速い vs 頑健 — すべて同一の物理的矛盾。妥協レートを 1 つ探すのは罠（半盲目=両方の最悪）。frontier/core/ratchet に分離せよ。
2. **真偽判定が宿るのは recognition だけ。** 変異は捨てられる（安い）、保持は符号盲目（機械）。だから honesty の全荷重が認識ゲート 1 点に集中する。ここの誤りはループの他では訂正不能。**「変な好成績」は祝う対象でなく、再検証を発火させる条件**（0.473→0.183 の教訓）。
3. **先見は新規性を起源できない、精緻化するだけ。** 先見＝結晶化した過去の盲目的勝利（vicarious selector）。新規性が要る frontier では盲目が必然。ただし **豊かな prior の内側（combinatorial novelty）では guided 変異が blind に勝つ** — 範囲を見極めよ。
4. **多様性（③）は欺瞞 × 高次元への条件付き保険。** デフォルトで積むな、欺瞞の量に比例して積め。平滑/低 K では RR に構造的に勝てない。

### 新規 testable 仮説（cross-method が surface したもの）

**H1（最有力・未開拓 — RAD で「両半分は存在するが誰も結合していない」と確認）**: **地形認識コントローラ + 有限評価ハードン保持ゲート。**
- 主張: 探索中に地形の欺瞞度・次元性をオンライン推定し、平滑/低次元なら ③（QD）を **完全にオフ** にして RR に切り替え、欺瞞/高次元なら ③ をオンにするメタコントローラが、固定戦略より sample 効率で優越する。さらにその ③ archive の **insertion/retention 規則を有限評価ラチェットに対しハードン**（elite 凍結前に fresh-seed 再評価を必須化）する。
- 根拠の結合: BG9（低次元で RR 優越）+ Boldi 2311.02283 + Qian 2401.10539 + DOSSIER（地形条件付き）は別々に支持されるが、**地形を検出して ③ を on/off するメタコントローラはコーパス内に存在しない**（JEDi が最接近だが「smooth で完全 off」には届かない）。また reward-hacking 均衡（2603.28063）と QD archive は形式化済みだが **誰も結合していない**。
- 反証可能な予測: (a) 欺瞞度指標が閾値以下の run で ③-on は ③-off(RR) に **勝てない**（BG9 の一般化）。(b) fresh-seed 再評価を archive insertion に挿むと、ノイズ地形での「凍結偽 elite」率が有意に下がり、最終 fitness の楽観バイアス（winner's curse）が縮む。

**H2（llive 自己進化ループの設計原理）**: **2 層ゲノム（安定 core + 可変 prompt）に「正直認識ゲート」を super-system ラチェットとして実装する。**
- frontier（可変 prompt 層）= 盲目・高変異・anomaly 自由生成。core（安定層）= 先見・低変異・活用。ratchet（最遅・別モジュール）= fresh-seed 再検証を経た不可逆保持。**recognition を elitism に任せず、メタ認知モニタ（SOFAI-LM 2508.17959 型: fast generator + slow checker）として別レベルに切り出す** ことで P2 のラチェット誤りを構造的に防ぐ。
- 反証可能な予測: recognition を別レベル（slow checker + 再検証）に切り出した llive ループは、elitism 一体型より「変なノイズ勝利の凍結」が減り、長期 run での累積 fitness が単調に近づく（化石化誤りの減少）。

---

## 7. 正直な caveats

- **生物学正典は RAD コーパスに実質不在。** Campbell BVSR / Pasteur / Lenski LTEE / Wright-Simpson の **原典** はコーパスに無く（corpus-wide grep で false-positive のみ: GHSA、著者名 Murray Campbell、ECG データ）、モデルは AI/最適化プロキシ（QD・lexicase・reward-hacking 理論・LLM-evolution）経由でのみ操作化されている。概念骨格（Kauffman, BVSR, adjacent possible）は外から持ち込んだもの。web 検証で正典は裏取り済みだが、**コーパスは計算論的テストを供給するだけ**。
- **P1 の範囲限定（唯一の理論的 seam）**: 「先見は新規性を起源できない」は **fundamental novelty** に厳密、**combinatorial novelty** には過剰主張。LoongFlow/ShinkaEvolve が示す通り、豊かな prior の内側では guided 変異が blind に勝つ。モデルは「先見は prior の外では起源できない」と読むべき。
- **FEP 統一は仮説、確立した等価でない。** 「進化は active inference の一形態か、単なる類似か」は未解決。Friston 派は phylogenetic タイムスケールでの自由エネルギー最小化と主張、批判側は illuminating な類似に留まると見る。**解決不能、仮説扱い**。
- **未検証ソース**: Schmidhuber (2010) と Oudeyer-Gottlieb-Lopes (2016) の PDF は binary-garbled で **正確な引用は直接検証できず** — compression-progress / learning-progress の特徴づけは二次資料で consensus-attested。「adjacent possible の Wagner/Rosen 経済学定式化」は **検証できなかった** — 安全な帰属は Kauffman *Investigations* (2000)。それ以外（Campbell 1960/1974; Popper 1963/1972; Maynard Smith & Szathmáry 1995; Kauffman & Levin 1987 / Weinberger 1989; Lehman & Stanley 2011/2015; Mouret & Clune 2015; Schwartenbeck et al. 2013; Goodhart 1975）は直接 source-verified。
- **DOSSIER の精緻化を要採用**: 「欺瞞地形には QD」は粗い。多様性機構（fitness-sharing 系 vs lexicase 系）は欺瞞の種類で挙動が割れる。③ の GPU テストでは「多様性を出している」と「谷を渡っている」を **別々に測る** こと。
- **「recognition と retention は 1 因子に collapse しうる」（web 提案）**: Pasteur の prepared mind は selection 演算そのものかもしれず、3 項でなく 2 項ループ（structured variation × selective-retention-under-honest-measurement）で足りる可能性。ただし **measurement-honesty サブステップ（Goodhart が噛む所）を instrument する** 運用上の理由があるなら recognition を分離して保つ価値がある。本モデルは後者を採る（0.473 事件の防止が運用目的）。
