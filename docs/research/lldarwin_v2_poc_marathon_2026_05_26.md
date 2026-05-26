# lldarwin v2 — overnight PoC マラソン台帳 (2026-05-26 → 翌朝)

> **Goal (ユーザー 2026-05-26)**: 「徹底的に要件を整理して、もっと進化型として独自性を出す。
> PoC も何度も繰り返す。明日の朝までずっと小さい単位で PoC をしまくって**方策を決める**。」
> Codex / Perplexity 使用可。push 不可（ローカルコミットのみ）。honest disclosure 厳守。
> 本書は朝までの**意思決定ログ**＝最終成果は §「現時点の方策」に集約する。

---

## 0. 出発点（実データで確定した事実）

12h 実 LLM 進化ラン `out/lldarwin_12h_realpressure_2026_05_26` の分析:

| 事実 | 値 | 含意 |
|---|---|---|
| 完走 | 71 世代 / 12h（≈10.3 分/世代, real-LLM 逐次） | スループットが律速 |
| best_score | **gen5 で 1.0 → gen70 まで固定** | **目的飽和。65 世代が無進歩** |
| mean | 0.85 で頭打ち、1.0 戦略が席巻しない | **適応が蓄積しない** |
| 軸別 | 10 問中 6-7 問が飽和、勾配は multistep(2問, 0.5固定) のみ | 実効解像度が小さすぎ |
| fitness 依存 | **c_prompt のみ**。c_factors(40d)/c_impl/c_meta は中立浮動 | 43 次元が選択圧ゼロ |
| 集団健全性 | pop=24 維持・min≥0.70・**全滅せず** | 機構(GA)は壊れていない |

**判定**: 全滅はしていないが**累積進化になっていない**（≒ filtered random search）。
**真因 = 人手の固定ものさしの飽和**（ユーザー洞察「眼鏡が飽和すると選択圧は無力」の実証）。

---

## 1. ユーザーが対話で示した独自性 3 軸（要件 doc §1.11-1.13 に統合済）

1. **連続進化集団 = ライブ・オーケストラ**（ORCH）— 進化し続ける集団がその場で MoA 集約して 1 答。**最大の差別化候補**。
2. **調査機能を持つ個体**（AGENT）— Voyager 系。SR-1（個体=データのみ）と衝突 → 二空間分離で解決。
3. **観測・対話制御**（OBS）— 個体別応答＋選択スコアの時系列ビュー、step/停止/再開/保存。**no-regret＝第一歩**。

---

## 2. 並列ワーカー（overnight）

| # | ワーカー | タスク | 状態 |
|---|---|---|---|
| A | Claude agent | 開放端 sweep PoC（baseline は飽和・全滅 / 開放端は回避 を実証, ≥10K gen, §3 sweep） | 起動 |
| B | Claude agent | 観測基盤（応答ログ additive / 個体別スコア時系列ビューワー / lineage 復元） | 起動 |
| C | Claude agent | オーケストラ PoC（MoA が単一 best を上回るか, 多様性選抜 vs 冗長選抜） | 起動 |
| P | Perplexity | QD/novelty/MoA/agentic 進化 SOTA サーベイ（文献ギャップ補完） | 起動 |
| X | Codex | 設計の独立批評＋最小 PoC 3 案＋見落とし指摘（鵜呑みせず要検証） | 起動 |

---

## 3. ラウンド別ログ

### Round 0 (kickoff, 2026-05-26 夜)
- 要件 doc に独自性 3 軸（§1.11 ORCH / §1.12 AGENT / §1.13 OBS）を統合。SR-1↔AGENT 矛盾を二空間分離で解消。
- 並列ワーカー A-C + P + X 起動。
- 次: 各ワーカー完了 → 集計 → round 1 の小 PoC を dispatch。

### Round 1 (ワーカー第1陣完了)

**B 観測基盤 — 完了・着地（OBS 3要件すべてに動く実装）**
- 応答ログ: `real_pressures.py` に `response_log` kwarg（既定 off・後方互換）。回帰4件＋進化系886テスト緑。
- 個体別スコア時系列ビューワー `scripts/evolution_response_viewer.py`（HTML+SVG）。12h データで「gen0 founder 0.700→gen5 で 1.000、multistep が弱点軸」を可視化確認。
- lineage 復元 `scripts/evolution_lineage_rebuild.py`。「全部 ?」を解消、champion 系統 gen70→59 を12 hops 解決、欠落は捏造せず `lost@genN` 明示。根因=parent_ids が snapshot(5世代毎全24)+winners(全世代top3) のどちらか単独では辿れない。
- 注記: llive repo の **auto-commit hook** が編集を自動コミット（agent は git 未実行）。

**P Perplexity SOTA サーベイ — 完了**（`docs/research/openended_evo_sota_perplexity_2026_05_26.md`, 1143行）
- **独自性裏付け（最重要）**: 「online evolution + online answering を統合した連続稼働システム」は**明確な先行研究なし＝research white-space**（ORCH §1.11 の差別化が確定）。近接は MoA / Self-MoA / sequential aggregation / routing だが同一物なし。
- **ORCH への反証警告**: 2025 Self-MoA 研究で**多様性は自動的に優位でない** — 単一トップモデル反復が異種混合 MoA を AlpacaEval で 6.6% 上回る（quality-diversity トレードオフ）。→ ORCH-3/4 は実測必須・pass-bar 正直に（Agent C が検証中）。
- **飽和回避レシピ（実装指向）**: ①**パーセンタイル動的 minimal-criterion**（閾値=集団30%点→集団改善で自動上昇→飽和しない, pseudocode 有） ②**タスクでなく条件のカリキュラム**（難易度 d∈[0,1] を集団に追従） ③behavior descriptor は structural/dynamical/semantic を 20-100d→5-10d 縮約、fitness のクローン記述子は避ける ④parent 50% high-quality / 50% novelty。

**X Codex 批評 — ブロック（環境問題, honest）**
- gpt-5.2-codex / gpt-5.1-codex / gpt-5-codex / gpt-5.1 すべて "not supported when using Codex with a ChatGPT account" で 400。ChatGPT アカウントの許可モデル不一致（10x promo は ~2026-05-31 のはずだが API 側で拒否）。→ **Codex は一旦見送り**、PoC群＋Perplexity を主軸に。要・モデル設定見直し（ユーザー領域）。

**自己 PoC #1（固定ものさし飽和 vs 適応難易度, `D:\tmp\poc_saturation_fixes.py`）— 完了**
- 交絡除去後（elite=score 基準）: baseline(固定難易度) は能力 **0.627 で低位停滞**（best 0.757, 12h病理を再現）/ adaptive(難易度=集団60分位) は **0.952 へ上昇**（best 1.0）。
- ただし adaptive は**多様性を犠牲**（div 0.310→0.134）。→ **適応難易度（勾配維持）と QD/novelty（多様性維持）は相補**（どちらか一方では不十分）。Self-MoA 反証と整合。

**自己 PoC #2（相補仮説: 適応難易度 + novelty 選抜, 同 `poc_saturation_fixes.py`）— 完了・確定**

| 構成 | 最終能力 | best | 多様性 | plateau |
|---|---|---|---|---|
| baseline（固定難易度） | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive（難易度追従） | 0.952 | 1.000 | 0.134（崩壊） | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316**（維持） | gen99（最長探索） |

- **adaptive+novelty が能力（baseline比 +40%）と多様性（adaptive比 2.4倍, baseline 同等）を両立**。能力を 7% 譲って多様性を完全維持＝Self-MoA が警告する quality-diversity トレードオフを**好ましい側**で着地。
- **方策の核が自前データで確定**: 「適応難易度＝勾配維持」と「QD/novelty＝多様性維持」は**相補で両方必須**。固定ものさし単独(baseline)も適応難易度単独も不十分。
- honest 留保: 抽象 proxy（competence ベクトル）であり実 LLM 写像ではない＝mechanism feasibility の検証。plateau@gen は「停滞した世代」で、停滞の**水準**（baseline=低位0.627 / adaptive系=天井近傍）が本質。

### Round 1 → 次手
- ✅ 自己 PoC #1/#2 完了（上記）。
- ⏳ A(開放端 sweep)/C(オーケストラ) 完了待ち → 結果を本台帳へ統合。
- 次 real-pressure ランは Agent B の `--response-log @out` 付き＋**難化/適応難易度バッテリ**で起動する方針（自己 PoC #1/#2 の知見を実 LLM 段へ）。

### Round 1.5 (Agent C オーケストラ proxy 完了 / 実LLMラン継続中)

**C オーケストラ PoC — proxy 結果は天井飽和で判定不能（重要な方法論的発見）**
- `scripts/poc_orchestra.py` + `out/poc_orchestra_2026_05_26/orchestra_proxy.json` 着地。proposition=ORCH-4。
- proxy（12h snapshot gen70 の breakdown を流用）では **single_best も全 MoA 戦略（redundant/diverse × majority/best_of/weighted）も total=1.0** で差が出ない。**飽和した fitness は orchestration の価値を測れない**（single best が既に満点＝headroom ゼロ）。
- 多様性選抜は distinct_signatures が冗長選抜より多い（k=7: diverse 7 vs redundant 5）が、スコアに反映されない。
- **結論（方法論）**: **ORCH-4 の検証には「単一個体が満点を取れない難タスク」が前提**。= Round 1 の「飽和を直す」が ORCH 検証の**前提条件**でもある（二重の理由で saturation-fix が先）。
- 実LLMラン（monitor `be06f6741`, PID 26464）継続中。C は終了・ポーリング停止。親が実データ着地後に確認。

**自己 PoC #3（ORCH-4 を headroom 有り難タスクで, `D:\tmp\poc_orchestra_headroom.py`）— 完了・Self-MoA 反証の正体を解明**

| 構成 | best_of(routing) | majority(vote) | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant(top-k) | 0.750 | 0.500 | 3/4 |
| MoA diverse(max-cover) | **1.000** | **0.000** | 4/4 |

- 専門家が分散し single_best=0.5（headroom 有り）の難タスクで、**多様 MoA は best-of/routing で 1.000**（単一bestを倍）。**ORCH-4 成立、ただし条件付き**。
- **決定的発見**: **naive majority では多様性が逆効果**（diverse=0.000 — 各 sub-task で competent な専門家1人が無知な多数派に negate される）。redundant majority=0.500 が上回る。
- **= Self-MoA 反証（多様性≠自動優位）の正体**: 集約器が **competent メンバへ routing できるかが決定的**。投票/平均は diversity を殺し、competence-aware routing/gating は diversity を活かす。
- **方策への含意（ORCH 設計要件）**: オーケストラは**投票でなく「指揮者（router/gating）」が必須**。expert_council.py の gating or 学習 router を配線。honest 留保: best_of は oracle routing の上限＝実際は「どの個体が competent か」を予測する gate の精度が律速（ここが失敗点になり得る）。

### Round 1.6 (Agent C 実LLMラン 完了 — 自己PoC#3 と独立に一致＝強い証拠)

**C オーケストラ 実LLM結果**（`out/poc_orchestra_2026_05_26/orchestra_real.json` + `SUMMARY.md`, 105 LLM calls/2073s, llama3.2, 15タスク）:
- 単一best=**0.933**。MoA `best_of`+k≥5 で **1.000**（+0.067）。**majority/weighted は一度も 0.933 を超えず**。
- diverse > redundant（k=5: diverse/best_of=1.000 vs redundant/best_of=0.933）。多様選抜は異 QD cell の補完 specialist（base/terse 個体）を少ない k で先に拾う。冗長選抜は支配署名（chain_of_thought）に密集し同じ盲点を共有。
- 改善は**丸ごと multistep::t2（「5を2倍して3引く」）由来**＝CoT 個体群が揃って落とす1問を多様選抜の異種個体が解いた。他4軸は単一bestが既に満点。
- proxy は飽和で検証不能、実LLMで難問追加し de-saturation してようやく ORCH-4 を検証できた（Round1.5 / 自己PoC#3 の設計判断を実データが裏付け）。
- always-on（answer-on-demand）は構造的に成立（進化=background / 回答=最新snapshot read）。

**🔑 独立クロス検証**: 自己PoC#3（合成・専門家分散）と Agent C（実LLM・llama3.2）が**別手法で同一結論**＝「MoA は competence-aware routing(best_of) でのみ単一bestを上回る／投票では届かない／多様性は routing 下でのみ価値」。2手法一致は honest disclosure 上きわめて強い。
- **最大の穴（次の決定点）**: oracle best_of に実投票（majority/weighted）が届かない。**実ルーター/検証ゲートが best_of に近づけるか**が ORCH 実用性の核。→ 自己PoC#4 で検証。

### Round 1.7 (自己PoC #4 — ORCH 最大の穴を埋めた)

**自己PoC #4（実ルーター vs oracle best_of, `D:\tmp\poc_router.py`, 20 seed 平均）**

| κ(較正) | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **descriptor/specialty-router は較正不要で robust に 0.90**（単一best 0.675 を安定超え, oracle 近傍）。**QD 用に既に計算する behavior descriptor が routing キーに流用できる相乗効果**（QD と ORCH が同じ記述子基盤を共有）。
- **confidence-router は較正 κ≥0.6 で oracle 到達**。ただし小型LLMは較正が弱い恐れ → **descriptor-router を第一選択**（calibration 非依存）。
- **majority=0.338 は確定的に不適**（#3, C と三たび一致）。
- **結論**: C 指摘の「oracle に実投票が届かない」穴は、**descriptor-routing（QD記述子流用）で実用的に埋まる**。ORCH が proxy＋(部分)実LLM で end-to-end 成立。

<!-- 以降、各ワーカー完了ごとに結果と次手を追記 -->

---

## 4. 現時点の方策（朝までに確定させる本体・随時更新）

> 暫定。証拠が積まれるたびに更新。最終的にここが「決めた方策」になる。

- **方策仮説（Round 1 で大幅に裏付け）**: 固定 quiz fitness を捨て、選択核を **(a) 適応難易度（条件カリキュラム＝難易度を集団に追従）× (b) QD/novelty（MAP-Elites + novelty + ε-lexicase + パーセンタイル動的 minimal-criterion）** の**二本立て**にする。**(a) と (b) は相補で両方必須**（自己 PoC #2 で確定: (a) 単独は多様性崩壊、(b) を足すと能力 0.881・多様性 0.316 を両立）。成果物は単一 best でなく**多様な elite の archive**。その archive を**連続進化させつつ MoA でオーケストラ**して 1 答（ORCH; **online-evolution+online-answering は white-space=独自性**、ただし Self-MoA 反証ゆえ「多様性選抜＞冗長選抜」は実測で要証明＝Agent C）。個体は段階的に**サンドボックス調査機能**（AGENT, SR-1 整合の二空間分離）。**観測は最初に整備済（B 完了）**。
- **検証ゲート（採用条件）と現状**:
  1. 開放端構成が baseline の飽和・全滅を**実データで回避**（A: monoculture<0.8 / archive 末尾成長 / 多様性高止まり）。**⏳ Agent A 実行中**。自己 PoC #1/#2 で proxy 段の予備裏付けは取得。
  2. MoA アンサンブルが単一 best を**上回る**（C: ORCH-4）。上回らなければ ORCH は棄却。**⏳ Agent C 実行中**（Self-MoA 反証あり＝厳格に判定）。
  3. 観測基盤で「個体別応答＋選択スコア＋系統」が**実際に見える**。**✅ 達成（Agent B 完了）**。
- **確定した設計判断（Round 1）**:
  - 固定スカラー quiz は**廃止**（baseline は能力 0.627 で停滞＝12h病理を proxy で再現）。
  - **適応難易度＋novelty の二本立て**を選択核に採用（相補・両方必須）。
  - 観測（応答ログ/時系列ビューワー/lineage 復元）は**実装済み**＝今後の全ランで標準装備。
  - **ORCH の集約は「投票/平均」でなく「competence-aware routing/gating（指揮者）」必須**（自己PoC #3 + Agent C 実LLM が独立一致: routing/best_of で diverse>redundant>single、majority では逆効果＝Self-MoA 反証の正体）。
  - **ORCH の routing は実用可能（穴は埋まった）**: **QD の behavior descriptor を routing キーに流用する descriptor-router** が較正非依存で oracle 近傍（自己PoC #4: 0.90, 単一best 0.675 を安定超え）。QD と ORCH が同一記述子基盤を共有＝設計の節約。confidence-router は較正 κ≥0.6 で oracle 到達だが小型LLM較正リスクあり→descriptor-router 第一選択。
  - Codex は環境ブロックで**当面不使用**（model 設定見直し後に再評価）。
- **却下条件（honest）**: 上記が示せない構成は正直に棄却し台帳に残す。
