---
title: '一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27（開放端進化 / ライブ・オーケストラ / honest cross-validation）'
tags:
  - FullSense
  - llive
  - 進化計算
  - honest_disclosure
  - 解説
private: true
updated_at: '2026-05-27'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 一晩で AI 進化を作り直した — 実 LLM 12h ランがまた満点で飽和し、6 本の PoC と 4 体の Agent と Perplexity が「独立に同じ結論」へ収束した夜 #27

> 📚 **連載ナビ（lldarwin アーク）**: #24-05 集団進化 → #25 monoculture の失敗 → #26 設計編 → **#27 本記事（climax）** → 実装編（予定）。※ 各記事は単独でも読めます（リンクは回遊用）。

> **コンセプト hook**: 前作 #25 で、私は「AI を 500 世代進化させたら、世界に**私とフリストンだけ**が
> 残った」という大失敗を晒しました。原因は、評価関数（眼鏡 = lleval）が満点を出し続けて、
> **選択圧がゼロになった**こと。
>
> 「では今度こそ、本物の LLM で確かめよう」——そう思って、on-prem の llama3.2 を相手に
> **12 時間ぶっ通しで進化**させました。proxy（合成のものさし）ではなく、実 LLM です。
>
> 結果。**gen5 で満点に張り付き、そこから 65 世代、ピクリとも進歩しませんでした。**
> 全滅はしない。でも累積もしない。これは進化ではなく、**ただの「ふるい付きランダムサーチ」**
> だった——proxy だけでなく、**実 LLM でも、まだ進化になっていなかった**のです。
>
> そこから一晩。私は「方策を決める」ために、自分で 6 本の PoC を回し、4 体の Claude Agent を
> 並列で走らせ、Perplexity に文献を漁らせました。そして朝、**全員が独立に、同じ結論へ収束**
> していた。これは、その「徹夜の意思決定ログ」の honest disclosure です。

---

## 0. 三行であらすじ（落語でいう「枕」）

落語には本題の前に「枕」があります。まずは三行で。

- **また飽和した** — 実 LLM(llama3.2) で 12h 回したら、gen5 で best=1.0 に張り付き、65 世代無進歩。全滅はしないが累積もしない＝**filtered random search**。真因は #25 と同じ「固定の人手ものさしの飽和」。
- **一晩で方策を決めた** — 自己 PoC 6 本 + 並列 Agent 4 体 + Perplexity が、**独立に同じ結論**へ収束。「ものさしを固定したまま淘汰器を磨いても無駄。**評価そのものを開放端化せよ**」。
- **独自性が見えた** — 連続進化する集団を、止めずに任意の瞬間に合奏（MoA）させて 1 答する「**ライブ・オーケストラ**」が、先行研究の white-space（空白地帯）だと判明した。

要するに **「眼鏡（評価）が飽和したら、淘汰器（lldarwin）をどれだけ磨いても無力」**。
だから磨く対象を変える——**評価そのものを開放端にする**、が今回の結論です。

---

## 1. なぜ「また」やったのか — #25 / #26(設計) の続き

ここまでの連載を 3 行で振り返ります。

- **#24-05**「集団が学ぶ AI」— 1 個の LLM を賢くするのではなく、**N 個の llive 個体（genome）を世代交代させて互いに評価し合う**派生集団進化、という枠組みを立てた。
- **#25**「私とフリストンだけが残った」— その集団に 8 人の知性をペルソナ種として蒔き、proxy 500 世代で回したら、**満点飽和 → 選択圧ゼロ → 運（遺伝的浮動）だけで 2 系統に偏る**大失敗。眼鏡が曇っていた。
- **#26(設計編)**「眼鏡で測るだけでは進化しない」— 淘汰器 **lldarwin** を設計し、「集約しない多目的淘汰（ε-lexicase / QD / 中立貯蔵庫）」を実装。proxy では系統絶滅を防げた。

ここまでは全部 **proxy（決定論 heuristic、LLM 非依存）**での話でした。proxy は「機構が回ること」は示せても、「進化が**意味あるもの**を見つけた」ことは示せません（[[feedback_benchmark_honest_disclosure]]）。

だから、当然の次の一手。**本物の LLM で確かめる。**

localhost の ollama（llama3.2:latest）が到達可能だったので、個体の `c_prompt`（prompt 戦略の遺伝子）を system prompt に変換し、固定の llama3.2 に被せて実タスクを解かせる——**Promptbreeder 系の写像**で、12 時間の連続進化ランを起動しました。これが本記事の出発点です。

> 🍵 **休憩ポイント**: ここまでで「proxy では機構が回った。じゃあ本物の LLM では?」という
> 問いが立てば OK。研究のいいところは、この「じゃあ本物では?」を実際に回せること。
> そして今回、本物は——容赦なかった。

---

## 2. 出発点 — 実 LLM 12h ランの「正直な不合格」

12 時間の実 LLM 進化ラン（on-prem llama3.2、measurement purity 厳守＝cloud LLM と混在させない、[[feedback_llive_measurement_purity]]）の結果が、これです。

| 事実 | 値 | 含意 |
|---|---|---|
| 完走 | 71 世代 / 12h（≒10.3 分/世代、実 LLM 逐次） | スループットが律速 |
| best_score | **gen5 で 1.0 → gen70 まで固定** | **目的飽和。65 世代が無進歩** |
| mean | 0.85 で頭打ち、1.0 戦略が席巻しない | **適応が蓄積しない** |
| 軸別 | 10 問中 6-7 問が飽和、勾配は multistep（2 問）のみ | 実効解像度が小さすぎ |
| fitness 依存 | **c_prompt のみ**。c_factors(40 次元)/c_impl/c_meta は中立浮動 | **43 次元が選択圧ゼロ** |
| 集団健全性 | pop=24 維持・min ≥ 0.70・**全滅せず** | 機構（GA）は壊れていない |

ここで踏みとどまるのが、FullSense の honest disclosure ルールです（[[feedback_benchmark_honest_disclosure]]）。「全滅しなかった！ best=1.0 に到達した！」と書けば、いかにも成功っぽい。でも内訳を見れば一目瞭然です。

**判定: 全滅はしていないが、累積進化になっていない（≒ filtered random search）。**

10 問のテストのうち、勾配（差）が残っているのは multistep の 2 問だけ。残り 8 問は早々に全員満点。つまり 10 問中 8 問は、もはや誰を選んでも同じ。選択圧の実効解像度が、ほぼ 2 問分しか残っていない。しかも fitness に関与するのは 4 つの染色体のうち `c_prompt` ただ 1 つで、残り 43 次元（思考因子 40 次元 + 実装 + メタ）は**選択圧ゼロの中立浮動**。

![実 on-prem LLM（llama3.2）進化ランの適応度と多様性（12h 連続ラン）。best は早々に天井に張り付き、以降は平坦](./assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status.svg)

![5 苦手軸（typo / polysemy / multistep / calibration / context）の母集団平均推移（実 on-prem LLM 評価）。multistep 以外は早期に飽和し、勾配が残らない](./assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

**真因 = 人手の固定ものさしの飽和。** #25 でユーザーが言語化した洞察「**眼鏡が飽和すると、選択圧は無力**」を、今度は proxy ではなく**実 LLM で実証**してしまった、という構図です。眼鏡を proxy から実 LLM に替えても、**ものさしが「固定の 10 問」である限り、すぐ満点で飽和する**。レンズのメーカーを替えても、目盛りが粗ければ同じ。

> 🤔 **たとえ話**: 採点者を「本物の先生（実 LLM）」に替えても、出す問題が毎回同じなら、
> 数回で全員が満点を取り、以降は何回テストしても差がつきません。問題が悪いのではなく、
> **問題用紙が固定で簡単すぎる**のです。採点者（眼鏡）を proxy から実 LLM に交換しても、
> ものさし（問題）が固定なら飽和する。これが「正直な不合格」の正体です。

> 🍵 **休憩ポイント**: ここで多くの人は「実 LLM でも飽和なら、もう詰みでは?」と思います。
> 私もそう思いました。でも、ここからが本題。**「ものさしを固定したのが間違い」**だとしたら、
> 直すべきは淘汰器でも LLM でもなく、**ものさしの作り方そのもの**です。それを一晩かけて、
> 6 本の PoC と 4 体の Agent と Perplexity で確かめました。

---

## 3. 一晩の作戦 — 「方策を決める」ための分散調査

ユーザーから来た指示は、こうでした。

> 「徹底的に要件を整理して、もっと進化型として独自性を出す。PoC も何度も繰り返す。
> 明日の朝までずっと小さい単位で PoC をしまくって**方策を決める**。」

ここで重要なのは、**「実装を完成させる」ではなく「方策を決める」**が目的だったこと。だから、大きな本番ランを 1 本回すのではなく、**小さい PoC を大量に**回して、設計判断を 1 つずつ実データで潰していく、という作戦を取りました（[[feedback_poc_feasibility_first]] = 要件 → PoC → フィジビリティ → 詳細設計）。

並列で動かしたワーカーは、これです（[[feedback_parallel_first_execution]] = 独立タスクは並列 Agent 起動が default）。

| # | ワーカー | タスク |
|---|---|---|
| A | Claude Agent | 開放端 sweep PoC（baseline は飽和・全滅 / 開放端は回避 を実証、≥1 万世代） |
| B | Claude Agent | 観測基盤（応答ログ / 個体別スコア時系列ビューワー / lineage 復元） |
| C | Claude Agent | オーケストラ PoC（MoA が単一 best を上回るか、多様性選抜 vs 冗長選抜） |
| P | Perplexity | QD/novelty/MoA/agentic 進化の SOTA サーベイ（文献ギャップ補完） |
| X | Codex | 設計の独立批評 + 最小 PoC 3 案 + 見落とし指摘 |
| 自己 | 私（main） | 自己 PoC #1〜#6 を直接実装・実行（orchestrator 兼最重要タスク担当） |

> 🍵 **休憩ポイント**: この「6 人がかり」の体制、実は本記事の隠れた主役です。
> なぜ 1 人（1 つの context）で全部やらないのか? 答えは honest disclosure の核心にあります。
> **同じ頭で考えた結論は、同じバイアスに引きずられる。** 別々の手法（合成 PoC / 実 LLM /
> 文献調査）で**独立に**確かめて、それが一致したときだけ、結論を信用する。これを
> **honest cross-validation** と呼びます。後半でその威力が出てきます。

ここで 1 つ、正直な不発も書いておきます。**Codex（X）は使えませんでした。** ChatGPT アカウントの許可モデル不一致（API 側が codex 系モデルを軒並み拒否）でブロック。10x promo 期間中のはずが、API が "not supported when using Codex with a ChatGPT account" を返す。これは環境問題なので、当面は自己 PoC + 並列 Agent + Perplexity を主軸に切り替えました。**「使えるはずの道具が使えなかった」も、隠さず記録する。**

---

## 4. 最初の決定打 — 「固定ものさし」を捨てるか（自己 PoC #1 / #2）

最初に潰すべき仮説は、いちばん根っこの問いでした。**「ものさしを固定難易度から適応難易度に変えれば、飽和は直るのか?」**

### 4.1 自己 PoC #1 — 適応難易度は飽和を直す。が、多様性を殺す

合成の competence ベクトルを使った proxy で、交絡を除去して（elite を score 基準で選ぶ）比較しました。

- **baseline（固定難易度）**: 能力 **0.627 で低位停滞**（best 0.757）。12h の病理を proxy で再現。
- **adaptive（難易度 = 集団 60 分位に追従）**: 能力 **0.952 へ上昇**（best 1.0）。

難易度を集団に追従させる（できる問題が増えたら問題を難しくする）と、飽和が解けて能力が伸びた。**だが**——adaptive は**多様性を犠牲**にしました（diversity 0.310 → 0.134 に崩壊）。難しい問題に最適化する過程で、集団が 1 つの正解戦略に凝集してしまう。

### 4.2 自己 PoC #2 — 適応難易度 × novelty は両立する

そこで「適応難易度（勾配を維持）」に「novelty 選抜（多様性を維持）」を足したらどうなるか。

| 構成 | 最終能力 | best | 多様性 | plateau |
|---|---|---|---|---|
| baseline（固定難易度） | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive（難易度追従） | 0.952 | 1.000 | 0.134（崩壊） | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316（維持）** | gen99（最長探索） |

**adaptive + novelty が、能力（baseline 比 +40%）と多様性（adaptive 比 2.4 倍、baseline 同等）を両立**しました。能力を 7% 譲るかわりに、多様性を完全維持。

ここで**方策の核が、自前データで確定**しました。

> **「適応難易度＝勾配維持」と「QD/novelty＝多様性維持」は相補で、両方必須。**
> 固定ものさし単独（baseline）も、適応難易度単独（adaptive）も、どちらも不十分。

honest 留保: これは抽象 proxy（competence ベクトル）であって、実 LLM 写像ではありません。**mechanism feasibility（機構が回るか）の検証**に限定されます。plateau@gen の数字は「停滞した世代」を指しますが、本質は停滞の**水準**——baseline は低位（0.627）で停滞、adaptive 系は天井近傍で停滞、という違いです。

> 🤔 **たとえ話**: 全員が満点を取ったら問題を難しくする（適応難易度）。すると点は割れますが、
> 今度は全員が同じ解き方に収束してしまう（金太郎飴）。そこで「変わった解き方にもご褒美をやる」
> （novelty）を足すと、能力と多様性が両立する。**「難しくする」と「変わり者を褒める」の二刀流**——
> これが PoC #2 の要点です。

---

## 5. 本丸の証拠 — 開放端進化の 1 万世代 sweep（Agent A）

自己 PoC で「方向」は見えました。次は、それを**大規模に・厳密に**叩く番です。並列 Agent A に、**各 1 万世代 × pop256 × 19 構成 × 2 巡**の開放端 sweep を回させました。

判定基準は「open-ended（開放端）かどうか」——**飽和せず、monoculture（単一文化への収束）を避け、archive（多様性の貯蔵）が成長し続けるか**。

### 5.1 決定的な判定表

**verdict（gen9999 時点）: 全 scalar 構成 = False / 全 novelty・lexicase 構成 = True**

| label | 選択 | std | MC | reservoir | archive | open-ended | occupied | monoculture | uniq_lineages |
|---|---|---|---|---|---|---|---|---|---|
| baseline_scalar | scalar | - | - | 0 | none | **False** | 9 | 0.74 | 1.0 |
| baseline_scalar_mc | scalar | - | ✓ | 0 | none | **False** | 9 | 0.90 | 1.0 |
| **scalar_qd** | scalar | - | - | 0 | map-elites | **False** | — | — | — |
| novelty_std | novelty | ✓ | - | 0 | none | True | 100 | 0.13 | 1.0 |
| novelty_std_qd | novelty | ✓ | - | 0 | map-elites | True | — | — | — |
| **novelty_std_res256** | novelty | ✓ | - | 256 | map-elites | True | 95 | 0.05 | **31.9** |
| novelty_std_res1024 | novelty | ✓ | - | 1024 | map-elites | True | 98 | 0.04 | 15.2 |
| **full_oe** | novelty | ✓ | ✓ | 1024 | map-elites | True | 90 | 0.05 | 15.3 |
| lexicase_std(_mc) | lexicase | ✓ | -/✓ | 0 | none | True | 111–122 | 0.03 | 1.0 |

ここから、4 つの決定的な発見が出ました。

1. **選択圧が決定打。** scalar（単一スカラー fitness）は、MAP-Elites の archive を足しても（`scalar_qd`）**全滅（False）**。つまり「貯蔵庫を足せば多様性が守れる」というのは**誤り**で、**novelty / lexicase という開放端な選択でないと、そもそも開放端は成立しない**。archive 単独では救えない。**選択圧そのものを開放端化する**のが本質だった。
2. **標準化（z-score）が QD 被覆を桁で広げる。** novelty に per-dim z-score 標準化を足すと、occupied cells が 9 → 100+ に。各軸の「逸脱」を選択圧に変えると、行動空間の被覆が一桁広がる。
3. **中立貯蔵庫が系統多様性を回復。** novelty_std だけだと uniq_lineages は 1.0（系統は 1 つに固定）。reservoir256 を足すと **31.9** に。**行動多様性と系統多様性は別の軸**で、後者には貯蔵庫が要る（これは #26 設計編で実装済の知見の再確認）。
4. **スケールが効く。** latent 次元を 256 → 1024 にすると niche が 101 → 166、archive が 1021（飽和）→ 2234（成長継続）。多様性は「容量」で買える。

![Stage1 baseline（novelty なし）の適応度と多様性。終盤に多様性が崩壊する（scalar の典型的な失敗）](./assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg)

![Stage1 novelty pressure あり。行動多様性が終盤まで維持される](./assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status.svg)

![baseline vs +novelty の diversity を重ね描き。崩壊（scalar）と維持（novelty）を 1 枚で対比](./assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay.svg)

### 5.2 Agent A が出してくれた「正直な限界」

良い結果（open-ended 成立）が出たときこそ、限界を書く。Agent A 自身が、こう指摘してきました。

> novelty/lexicase は記述子**全体**の多様性は保つが、**特定の意味次元（factor）の多様性は保証しない**。
> 大きな latent では factor drift が起き、fspread（factor の広がり）が要監視。

つまり「全体としては多様」でも「思考因子という特定の意味次元では収束している」ことがありうる。これは新しい要件 **factor-subspace QD（意味次元を個別に保護する QD）** を生みました（後述の PoC #6 で対処）。

> 🍵 **休憩ポイント**: ここが本記事のいちばん硬い節です。持ち帰ってほしいのは 1 行——
> **「archive（貯蔵庫）を足すだけでは救えない。選択圧そのものを開放端にしないと駄目」**。
> #25/#26 設計編で「集約しない」と言ってきましたが、その本丸が「**選択の仕方を開放端化する**」
> ことだった、と 1 万世代の実データが言い切ってくれた。ここを越えたら、あとは独自性の話です。

---

## 6. 独自性の核 — 「連続進化する集団を、止めずに合奏させる」

ここまでで「飽和を構造的に避ける選択核（S1）」が固まりました。次は、ユーザーが対話で示した**独自性 3 軸**を、PoC と文献で裏付ける番です。

ユーザーが言語化した 3 軸は、これでした。

1. **連続進化集団 = ライブ・オーケストラ（ORCH）** — 進化し続ける集団が、その場で MoA（Mixture-of-Agents）集約して 1 答する。進化を止めない。**最大の差別化候補。**
2. **調査機能を持つ個体（AGENT）** — 個体が自分で調べに行く。Voyager 系。
3. **観測・対話制御（OBS）** — 個体別の応答 + 選択スコアの時系列を見て、止めて、再開できる。

### 6.1 Perplexity が裏付けた white-space

並列で走らせた Perplexity の SOTA サーベイ（1143 行）が、最重要の裏付けを返してきました。

> 「**online evolution + online answering を統合した連続稼働システム**」は、明確な先行研究なし
> ＝ **research white-space（空白地帯）**。近接は MoA / Self-MoA / sequential aggregation / routing
> だが、同一物はない。

つまり「進化を止めて、できあがった最強個体で答える」のは普通。「進化を**止めずに**、進化中の集団をそのまま合奏させて答える」のは、誰もまだやっていない。**ORCH §1.11 の差別化が確定**しました。

### 6.2 ただし Perplexity は反証警告もくれた

honest disclosure として、Perplexity がくれた**反証警告**も同じ重みで書きます。

> 2025 年の **Self-MoA 研究**では、**多様性は自動的に優位ではない**。単一トップモデルの反復が、
> 異種混合 MoA を AlpacaEval で 6.6% 上回った（quality-diversity トレードオフ）。

「集団を合奏させれば単一個体より強い」は、**自明ではない**。むしろ多様性が逆効果になる場合がある、と先行研究が警告している。だから ORCH は「実測で証明せよ、pass-bar を正直に」。これを Agent C と自己 PoC #3/#4 で検証しました。

> 🍵 **休憩ポイント**: ここ、研究の誠実さが試される分岐点です。「online 進化 + online 回答は
> white-space！独自性！」で舞い上がりたいところに、Perplexity が「でも多様性は自動的に良くない
> という反証があるよ」と冷や水をかけてくる。**舞い上がる材料と冷や水を、同じ調査の中で両方
> 受け取る。** これができると、結論がぐっと強くなります。次節で、その冷や水の正体を解明します。

---

## 7. Self-MoA 反証の「正体」を解明する（自己 PoC #3 → Agent C 実 LLM）

「多様性は自動的に優位でない」——この反証を、proxy ではなく**メカニズムのレベル**で解明したのが、ここの山場です。

### 7.1 自己 PoC #3 — 投票か、ルーティングか

まず、proxy では検証不能でした（飽和した fitness では single best が既に満点 = headroom ゼロで差が出ない）。そこで**「単一個体が満点を取れない難タスク」**（専門家が分散し、single_best=0.5）を合成して測りました。

| 構成 | best_of（routing） | majority（vote） | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant（top-k） | 0.750 | 0.500 | 3/4 |
| MoA diverse（max-cover） | **1.000** | **0.000** | 4/4 |

ここで**決定的な発見**が出ました。

- 多様 MoA は **best-of / routing なら 1.000**（単一 best の倍）。**ORCH は成立する。**
- **ところが naive majority（多数決）では、多様性が逆効果**（diverse = 0.000）。各 sub-task で competent な専門家 1 人が、無知な多数派に negate（打ち消し）される。冗長 MoA の majority（0.500）のほうが上。

つまり **Self-MoA 反証（多様性 ≠ 自動優位）の正体は、「集約器が投票か、ルーティングか」だった**。投票・平均は多様性を殺し、competence-aware な routing/gating は多様性を活かす。「指揮者がいるオーケストラ」と「全員が好き勝手に音を出す雑踏」の違いです。

### 7.2 Agent C の実 LLM が、独立に同じ結論を出した

そして——並列 Agent C が、**実 LLM（llama3.2、105 回の LLM 呼び出し、15 タスク）**で、自己 PoC #3 と**独立に同じ結論**を出してきました。

- 単一 best = **0.933**。MoA `best_of` + k≥5 で **1.000**（+0.067）。**majority / weighted は一度も 0.933 を超えず。**
- diverse > redundant（多様選抜が異 QD cell の補完 specialist を少ない k で先に拾う）。
- 改善は**丸ごと multistep の 1 問**（「5 を 2 倍して 3 引く」）由来。CoT 個体群が揃って落とす 1 問を、多様選抜の異種個体が解いた。

> 🔑 **独立クロス検証（本記事の核）**: 自己 PoC #3（合成・専門家分散）と Agent C（実 LLM・llama3.2）が、
> **別の手法で同一の結論**——「MoA は competence-aware routing（best_of）でのみ単一 best を上回る /
> 投票では届かない / 多様性は routing 下でのみ価値を持つ」——に達しました。
> 2 手法が一致することは、honest disclosure 上きわめて強い証拠です。

### 7.3 最大の穴 — 「実ルーター」は oracle に届くのか（自己 PoC #4）

ここで Agent C が、最大の穴を指摘してきました。「best_of は **oracle routing**（どの個体が正解かを神様が知っている上限）であって、実際は『どの個体が competent か』を**予測する gate** の精度が律速。実投票（majority）は oracle に届かない」。

これを自己 PoC #4（実ルーター vs oracle、20 seed 平均）で埋めました。

| κ（較正） | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **descriptor / specialty-router は較正不要で robust に 0.90**（単一 best 0.675 を安定超え、oracle 近傍）。しかも **routing キーは QD 用に既に計算する behavior descriptor を流用できる**——**QD と ORCH が同じ記述子基盤を共有**する相乗効果。
- **confidence-router は較正 κ≥0.6 で oracle 到達**。ただし小型 LLM は較正が弱い恐れ → **descriptor-router を第一選択**（較正非依存）。
- **majority = 0.338 は確定的に不適**（PoC #3、Agent C と**三たび一致**）。

**結論**: Agent C が指摘した「oracle に実投票が届かない」穴は、**descriptor-routing（QD 記述子を流用）で実用的に埋まる**。ORCH が proxy + （部分）実 LLM で end-to-end に成立しました。

> 🤔 **たとえ話**: 専門家を 10 人集めて多数決させると、無知な多数派が正しい専門家を打ち消してしまう。
> 数学の問題は数学者に振る——**振り分ける係（指揮者 = routing）**が要るのです。しかもその指揮者の楽譜
> （behavior descriptor）は、多様性を管理するために**すでに計算してある**ものを流用できる。投票
> （majority）は専門家を殺し、指揮者（routing）が活かす。これが PoC #4 の要点です。

---

## 8. 個体に「調べる力」を持たせる（自己 PoC #5）

独自性 3 軸の 2 つ目、**調査機能を持つ個体（AGENT）**。個体が探索空間でサンドボックス読取専用の調査をできるようにする構想です。ただし「調査はタダではない」——コストを計上したとき、進化は調査を使いこなすのか?

自己 PoC #5（コスト λ を変えて、調査閾値 θ がどう進化するか、20 seed 平均）。

| λ | θ*（=λc, 最適閾値） | θ_evolved（進化が獲得した閾値） | evolved | always | never |
|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.049 | 21.46 | 21.47 | **11.70** |
| 0.3 | 0.30 | 0.476 | 21.34 | 21.26 | 21.20 |
| 0.6 | 0.60 | 0.659 | **21.24** | 21.06 | 21.21 |
| 0.9 | 0.90 | 0.888 | 21.21 | 20.85 | 21.21 |

- **進化が、選択閾値 θ → λc を自力で獲得**した（= 状況に応じて「調べるべきときだけ調べる」選択的調査が**創発**）。
- **調査機能の価値は明白**: λ=0（調査無料）のとき、never（一切調べない）は 11.70 = **45% の損**。
- **コスト λ が「always 調査」を劣化させ、選択を強制**する。AGENT-3（コスト原理）成立。

honest 留保: 中間 λ での margin は小さく（浅い報酬地形）、これも抽象 proxy（実 LLM × 知識ベースは別段）。それでも「コストがあると、選択的調査が創発する」というメカニズムは proxy で確かめられました。

---

## 9. スケールが「多様性を質的に増やす」（Round 3）

最後に、Agent A が指摘した「容量で多様性を買える」を、母数（集団サイズ）でも確かめました。`full_oe` 構成（novelty + std + MC + reservoir1024 + map-elites）で、pop を 256 → 4096 まで振りました。

| pop | gens | occupied niches | monoculture | uniq_lineages | distinct_genomes | bspread_tail |
|---|---|---|---|---|---|---|
| 256 | 5000 | 171 | 0.047 | 14 | 256 | 0.939 |
| 1024 | 3500 | 467 | 0.019 | 74 | 1022 | 1.003 |
| 2048 | 2500 | 754 | 0.009 | 188 | 2041 | 1.071 |
| 4096 | 1200 | **1219** | **0.006** | **372** | 4054 | 1.253 |

母数スケールで、open-endedness が**単調に向上**しました（niches 171 → 1219 / monoculture 0.047 → 0.006 / uniq_lineages 14 → 372 / 行動の広がり bspread も単調増）。POP-1 仮説（母数が多様性を増やす）が proxy で支持されました。

**honest（交絡を明示）**: ここに正直な落とし穴があります。pop を上げるぶん、gens を短縮しました（5000 → 1200）。これは **niche 蓄積には不利な方向の交絡**です。それでも単調増だった——つまり **POP 効果は robust な下限**（本来はもっと効くはず）。逆に言えば「もっと効く可能性」は、この実験では証明できていない。proxy mechanism feasibility に限定された主張です。

![勝者個体の思考因子 × メモリ層ヒートマップ（Genome3D）。real-pressure では c_factors が中立浮動のため、これは認知プロファイルの可視化として参考扱い](./assets/lldarwin_2026_05_26/lldarwin_genome_heatmap.svg)

> 🍵 **休憩ポイント**: 「スケールすれば多様性が増える」は直感的ですが、ここで大事なのは
> **「不利な交絡を入れてもなお単調増だった」**という正直さです。gens を削るのは普通なら
> 多様性に不利。それでも増えた。だから「下限」と言える。良い結果を「上限」と誇張せず
> 「下限」と書く——これも honest disclosure の作法です。

---

## 10. 朝、全員が同じ結論に着いていた — 確定した方策

一晩で、**自己 PoC 6 本 + Agent A/B/C + Perplexity が、独立に同じ結論へ収束**しました。これが honest cross-validation の威力です。固定ものさし路線を捨て、以下を lldarwin v2 の核に確定採用しました。

### S1. 選択核（飽和を構造的に回避）

- **固定スカラー quiz fitness を廃止**（baseline は 1 万世代で飽和 + monoculture 0.9 + 多様性崩壊 = 12h 病理を大規模再現、open-ended 0/6）。
- **選択 = novelty / ε-lexicase（z-score 標準化必須）+ minimal-criterion**。**MAP-Elites archive 単独では不可**（scalar_qd も全滅）= 選択圧そのものを開放端化する。
- **品質も要るので QD（品質 × 多様性 per cell）**: 純 novelty は scalar 品質を犠牲（0.77-0.83）→ 適応難易度（条件カリキュラム）と組んで品質勾配を供給（PoC #2）。
- **系統多様性は中立貯蔵庫で別途確保**（行動多様性 ≠ 系統多様性、res256 で uniq_lineages 1 → 32）。
- **factor-subspace QD を追加**（意味次元の多様性を個別保護、Agent A の factor-drift 限界への対処、PoC #6）。

### S2. 成果の出し方 = 連続進化 × ライブ・オーケストラ（独自性の核）

- 成果物は単一 best でなく、**QD archive を連続進化させ、任意時点で MoA オーケストラして 1 答**（ORCH; online 進化 + online 回答の統合は white-space = 独自性、Perplexity 確認）。
- **集約は投票でなく competence-aware routing/gating（指揮者）必須**（自己 PoC #3/#4 + 実 LLM Agent C が三重一致）。
- **routing キーは QD の behavior descriptor を流用**（descriptor-router が較正非依存で oracle 近傍 0.90）= QD と ORCH が同一記述子基盤を共有（設計の節約）。

### S3. 個体 = 調査機能を持つ agentic 個体（段階導入、proxy 検証済）

- 探索空間ではサンドボックス読取専用調査のみ（実 I/O は Approval Bus 片方向昇格後）。調査はコスト計上。
- **proxy 検証済（PoC #5）**: コスト λ が「選択的調査」を創発。AGENT-3（コスト原理）成立。実 LLM × 知識ベースは次段。

### S4. 観測・対話制御（実装済 = 全ランで標準装備、Agent B 完了）

- 応答ログ / 個体別スコア時系列ビューワー / lineage 復元（進化系 886 テスト緑）。step/pause/resume は次段で配線予定。
- Agent B の lineage 復元は、12h データで「**全部 ?**」だった系統表示を解消し、champion 系統を gen70 → gen59 まで 12 hops 解決。欠落は捏造せず `lost@genN` と明示する（根因 = 親 ID が snapshot と winners のどちらか単独では辿れなかったこと）。観測基盤こそが honest disclosure の土台です。

### 自己 PoC #6 — factor-subspace QD で Agent A の限界に対処

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

意味次元（factor）用の novelty を別途課すと、意味次元の多様性損失をほぼ半減（50% 損 → 32% 損）。Agent A の factor-drift 限界への有効策を proxy で実証。honest: 完全固定ではなく 68% 残存 = 残 drift は中立貯蔵庫併用 or factor 重み強化が要。

---

## 11. 教訓（honest disclosure として残す）

- **実 LLM でも飽和した。** 眼鏡を proxy から実 LLM に替えても、ものさしが固定なら gen5 で満点。
  「本物の LLM を使えば進化する」は**嘘**でした。問題はものさしの作り方だった。
- **archive を足すだけでは救えない。** 「多様性の貯蔵庫を持てば多様性が守れる」は誤り。
  scalar 選択は QD archive を足しても全滅した。**救うのは選択圧の開放端化そのもの。**
- **多様性は自動的には良くない。** Self-MoA 反証の正体は「投票か routing か」。
  指揮者（competence-aware routing）がいて初めて、多様性は価値になる。投票は専門家を殺す。
- **独立クロス検証が、結論を強くする。** 自己 PoC（合成）と Agent C（実 LLM）と Perplexity（文献）が
  別々に同じ結論へ収束したからこそ、信用してよい。同じ頭の結論は、同じバイアスを共有する。
- **proxy は mechanism feasibility のみ。** 本記事の PoC 群は「機構が回るか」の検証であって、
  「実 LLM 一般の能力向上」の主張ではありません。この線引きを越えた瞬間、研究は嘘になります。
- **使えなかった道具（Codex）も記録する。** 成功だけでなく不発も honest に。

要するに——**「眼鏡（評価）が飽和したら、淘汰器をどれだけ磨いても無力」**。
だから磨く対象を、淘汰器でも LLM でもなく、**評価そのものの開放端化**に移す。これが一晩の結論です。

> 🍵 **休憩ポイント**: #25 で「失敗を晒す」と決めた。#26 設計編で「集約しない淘汰器」を作った。
> そして今回、本物の LLM が「それでもまだ足りない、ものさしが固定だから」と教えてくれた。
> **失敗が次の設計を生み、その設計の限界がまた次を生む。** これが連載の背骨です。
> 派手な「進化で AI が賢くなった！」は、まだ一度も書いていません。書けるだけの根拠が
> 揃っていないからです。揃ったときに、初めて書きます。

---

## 12. 結論

- 実 LLM 12h ランは「正直な不合格」だった——全滅しないが累積しない filtered random search。真因は固定ものさしの飽和（#25 の洞察を実 LLM で実証）。
- 一晩の分散調査（自己 PoC 6 本 + Agent A/B/C + Perplexity）が、独立に同じ結論へ収束 = **honest cross-validation**。
- 確定方策: **S1 開放端な選択核**（novelty/lexicase + std + MC + QD + 適応難易度 + 中立貯蔵庫 + factor-subspace QD）/ **S2 連続進化 × routing-MoA**（white-space 独自性、投票でなく指揮者）/ **S3 agentic 個体 + コスト**（選択的調査の創発）/ **S4 観測**（実装済）。
- すべての要素を proxy / （部分）実 LLM で裏付け済。残課題は「実 LLM 段への配線」「factor-subspace QD 実装」「scale-up」。コア戦略は確定した。

良い部品を作り、集約せずに束ね、実 LLM で飽和を確かめ、開放端な選択へ作り直す。そして 6 通りの独立検証が同じ結論に着いたとき、ようやく「方策が決まった」と言える。本記事こそ、#25 で予告した「**眼鏡が曇ると淘汰も無力**」の回です——実 LLM で眼鏡が曇った瞬間（飽和）を正直に晒し、Goodhart's law と proxy の限界を引き受けたうえで、開放端へ作り直しました。次は、この確定方策をコードへ落とす**実装フェーズ**へ。

---

## 13. 関連

- 連載 #24-05「集団が学ぶ AI」— 派生集団進化の枠組み（本記事の前提）
- 連載 #24-08「眼鏡を作る」— lleval（測る側）
- 連載 #25「私とフリストンだけが残った」— monoculture の honest disclosure（本記事の動機）
- 連載 #26（設計編）「眼鏡で測るだけでは進化しない」— 淘汰器 lldarwin の設計と Stage1/1.5/2 実測（本記事の姉妹編）
- 先駆者論文（2026-05-27, date of record）「Continuously-Evolving Populations as Live Orchestrated Ensembles」— 本記事の方策を学術形式で定式化した防御的公開（FullSense 公開リポジトリ `docs/papers/`）
- 関連 memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

# English

# Rebuilding AI Evolution Overnight — The Night a Real-LLM 12h Run Saturated at a Perfect Score Again, and 6 PoCs, 4 Agents, and Perplexity Independently Converged on the Same Conclusion #27

> 📚 **Series navigation (lldarwin arc)**: #24-05 population evolution → #25 the monoculture failure → #26 design → **#27 this article (climax)** → implementation (planned). Each article stands alone (links are for browsing).

> **Concept hook**: In the previous installment (#25), I confessed a major failure: after evolving an AI for 500 generations, the only survivors left in the world were **Friston and me**. The cause was that the evaluation function (the "lens" = lleval) kept handing out perfect scores, so **selection pressure dropped to zero**.
>
> "Then this time, let's verify it with a real LLM." With that, I ran a **continuous 12-hour evolution** against on-prem llama3.2. Not a proxy (a synthetic ruler) — a real LLM.
>
> The result: **it pinned to a perfect score at gen5 and didn't budge for the next 65 generations.** No extinction, but no accumulation either. This wasn't evolution — it was **just "filtered random search"**: not only with the proxy, but **even with a real LLM, it still wasn't evolving.**
>
> From there, one all-nighter. To "decide a strategy," I ran 6 PoCs myself, dispatched 4 Claude Agents in parallel, and had Perplexity comb the literature. By morning, **everyone had independently converged on the same conclusion.** This is the honest disclosure of that "overnight decision log."

---

## 0. The story in three lines (the "preamble" in rakugo terms)

In rakugo (Japanese comic storytelling) there's a "preamble" before the main story. First, three lines.

- **It saturated again** — Running the real LLM (llama3.2) for 12h, best=1.0 pinned at gen5, no progress for 65 generations. No extinction but no accumulation either = **filtered random search**. The root cause is the same as #25: "saturation of a fixed, hand-crafted ruler."
- **A strategy was decided overnight** — 6 self-run PoCs + 4 parallel Agents + Perplexity **independently converged on the same conclusion**: "Polishing the selector while keeping the ruler fixed is useless. **Make the evaluation itself open-ended.**"
- **The originality came into view** — Letting a continuously-evolving population perform an ensemble (MoA) at any instant — without stopping — to produce one answer, "**the live orchestra**," turned out to be a white-space in prior research.

In short: **"Once the lens (evaluation) saturates, no amount of polishing the selector (lldarwin) helps."** So we change what we polish — **we make the evaluation itself open-ended.** That's this round's conclusion.

---

## 1. Why I did it "again" — continuing from #25 / #26 (design)

Recapping the series so far in three lines:

- **#24-05** "AI that learns as a population" — Rather than making one LLM smarter, we framed **derivative-population evolution**: N llive individuals (genomes) cycle through generations, evaluating each other.
- **#25** "Only Friston and I were left" — We seeded that population with 8 intellects as persona seeds and ran 500 proxy generations, producing a major failure: **perfect-score saturation → zero selection pressure → genetic drift (luck) alone biasing toward 2 lineages.** The lens was clouded.
- **#26 (design)** "Measuring with a lens alone doesn't make it evolve" — We designed the selector **lldarwin** and implemented "non-aggregating multi-objective selection (ε-lexicase / QD / neutral reservoir)." In proxy, it prevented lineage extinction.

Up to here, everything was about **proxy (deterministic heuristic, LLM-independent)**. A proxy can show "the mechanism turns," but it can't show "evolution found something **meaningful**" ([[feedback_benchmark_honest_disclosure]]).

So, the natural next move: **verify with a real LLM.**

Since localhost's ollama (llama3.2:latest) was reachable, I converted each individual's `c_prompt` (the prompt-strategy gene) into a system prompt, layered it over a fixed llama3.2, and had it solve real tasks — a **Promptbreeder-style mapping** — launching a 12-hour continuous evolution run. That's the starting point of this article.

> 🍵 **Break point**: If you've reached "the mechanism turned in proxy — so what about a real LLM?" you're good. The nice thing about research is you can actually run that "so what about the real thing?" And this time, the real thing was — merciless.

---

## 2. The starting point — the "honest fail" of the real-LLM 12h run

Here's the result of the 12-hour real-LLM evolution run (on-prem llama3.2, strictly honoring measurement purity = never mixing in cloud LLMs, [[feedback_llive_measurement_purity]]).

| Fact | Value | Implication |
|---|---|---|
| Completed | 71 generations / 12h (≈10.3 min/gen, real LLM sequential) | Throughput is the bottleneck |
| best_score | **1.0 at gen5 → fixed through gen70** | **Objective saturation. 65 generations of no progress** |
| mean | Capped at 0.85; the 1.0 strategy doesn't take over | **Adaptation doesn't accumulate** |
| Per-axis | 6-7 of 10 questions saturated; gradient only in multistep (2 questions) | Effective resolution too small |
| fitness dependence | **c_prompt only**. c_factors (40-dim) / c_impl / c_meta drift neutrally | **43 dimensions have zero selection pressure** |
| Population health | pop=24 maintained, min ≥ 0.70, **no extinction** | The mechanism (GA) isn't broken |

This is where FullSense's honest disclosure rule makes you stop ([[feedback_benchmark_honest_disclosure]]). Write "No extinction! Reached best=1.0!" and it sounds like a success. But look at the breakdown and it's obvious.

**Verdict: not extinct, but not cumulative evolution either (≈ filtered random search).**

Of the 10-question test, only the 2 multistep questions retain a gradient (a difference). The other 8 were all maxed out early. In other words, for 8 of 10 questions it no longer matters who you pick. The effective resolution of selection pressure is down to roughly 2 questions' worth. And only 1 of the 4 chromosomes — `c_prompt` — participates in fitness; the remaining 43 dimensions (40-dim thought factors + impl + meta) are **neutral drift with zero selection pressure.**

![Fitness and diversity of the real on-prem LLM (llama3.2) evolution run (12h continuous). best pins to the ceiling early and stays flat thereafter](./assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_status.svg)

![Population-mean trajectories of the 5 weak axes (typo / polysemy / multistep / calibration / context) under real on-prem LLM evaluation. Everything except multistep saturates early, leaving no gradient](./assets/lldarwin_2026_05_26/lldarwin_stage2_real_llm_axes.svg)

**Root cause = saturation of the hand-crafted fixed ruler.** The insight the user articulated in #25 — "**once the lens saturates, selection pressure is powerless**" — we've now **demonstrated with a real LLM**, not a proxy. Swapping the lens from proxy to real LLM doesn't help: **as long as the ruler is "the fixed 10 questions," it saturates at a perfect score quickly.** Change the lens manufacturer and, if the gradations are coarse, you get the same thing.

> 🤔 **Analogy**: Even if you swap the grader for a "real teacher" (real LLM), if the questions are the same every time, everyone scores full marks within a few rounds, and no difference shows afterward no matter how many tests you run. The questions aren't bad — **the question sheet is fixed and too easy.** Swapping the grader (lens) from proxy to real LLM still saturates if the ruler (questions) is fixed. This is the essence of the "honest fail."

> 🍵 **Break point**: Many people now think, "If even a real LLM saturates, isn't it game over?" I thought so too. But this is where the main story begins. If **"fixing the ruler was the mistake,"** then what we should fix is neither the selector nor the LLM, but **the very way we build the ruler.** I verified that over one all-nighter, with 6 PoCs, 4 Agents, and Perplexity.

---

## 3. The overnight plan — distributed investigation to "decide a strategy"

The instruction from the user was this:

> "Organize the requirements thoroughly, and bring out more originality as an evolutionary system. Repeat PoCs many times. Keep running small-unit PoCs nonstop until morning to **decide a strategy.**"

The key here was that the goal was **not "complete the implementation" but "decide a strategy."** So rather than running one big production run, I took the approach of running **many small PoCs** to knock down design decisions one by one with real data ([[feedback_poc_feasibility_first]] = requirements → PoC → feasibility → detailed design).

The workers I ran in parallel were these ([[feedback_parallel_first_execution]] = independent tasks default to launching parallel Agents).

| # | Worker | Task |
|---|---|---|
| A | Claude Agent | Open-ended sweep PoC (demonstrate baseline = saturation/extinction vs. open-ended = avoidance, ≥10k generations) |
| B | Claude Agent | Observability (response logs / per-individual score time-series viewer / lineage reconstruction) |
| C | Claude Agent | Orchestra PoC (does MoA beat a single best? diversity vs. redundant selection) |
| P | Perplexity | SOTA survey of QD/novelty/MoA/agentic evolution (filling literature gaps) |
| X | Codex | Independent design critique + 3 minimal-PoC proposals + blind-spot flags |
| self | Me (main) | Directly implement and run self-PoCs #1–#6 (orchestrator + owner of the most important task) |

> 🍵 **Break point**: This "six-handed" setup is actually the hidden protagonist of this article. Why not do everything with one person (one context)? The answer is at the heart of honest disclosure. **A conclusion reached by the same mind is dragged by the same bias.** Verify **independently** with different methods (synthetic PoC / real LLM / literature survey), and only trust the conclusion when they agree. This is what I call **honest cross-validation.** Its power shows up in the second half.

Here, one honest dud to record. **Codex (X) was unusable.** A permitted-model mismatch on the ChatGPT account (the API rejected the entire codex model family) blocked it. It should have been within the 10x promo period, yet the API returned "not supported when using Codex with a ChatGPT account." Since this is an environment problem, for now I switched the main axis to self-PoCs + parallel Agents + Perplexity. **"A tool that should have worked but didn't" gets recorded too, not hidden.**

---

## 4. The first decisive blow — should we discard the "fixed ruler"? (self-PoC #1 / #2)

The first hypothesis to knock down was the most fundamental question: **"If we change the ruler from fixed difficulty to adaptive difficulty, does saturation get fixed?"**

### 4.1 Self-PoC #1 — adaptive difficulty fixes saturation. But it kills diversity

Using a proxy with synthetic competence vectors, I compared while removing confounds (selecting elites by score).

- **baseline (fixed difficulty)**: competence **stagnates low at 0.627** (best 0.757). The 12h pathology reproduced in proxy.
- **adaptive (difficulty follows the population's 60th percentile)**: competence **rises to 0.952** (best 1.0).

Letting difficulty track the population (raise difficulty as more problems become solvable) breaks the saturation and grows competence. **But** — adaptive **sacrifices diversity** (diversity collapses 0.310 → 0.134). In the process of optimizing for hard problems, the population coalesces onto one correct strategy.

### 4.2 Self-PoC #2 — adaptive difficulty × novelty are compatible

So what happens if we add "novelty selection (maintain diversity)" on top of "adaptive difficulty (maintain gradient)"?

| Configuration | Final competence | best | Diversity | plateau |
|---|---|---|---|---|
| baseline (fixed difficulty) | 0.627 | 0.757 | 0.310 | gen82 |
| adaptive (difficulty-tracking) | 0.952 | 1.000 | 0.134 (collapse) | gen63 |
| **adaptive + novelty** | **0.881** | 1.000 | **0.316 (maintained)** | gen99 (longest exploration) |

**Adaptive + novelty achieved both** competence (+40% vs. baseline) and diversity (2.4× adaptive, on par with baseline). It cedes 7% of competence in exchange for fully maintaining diversity.

Here, **the core of the strategy was confirmed with our own data.**

> **"Adaptive difficulty = gradient maintenance" and "QD/novelty = diversity maintenance" are complementary, and both are mandatory.**
> Neither the fixed ruler alone (baseline) nor adaptive difficulty alone (adaptive) is sufficient.

Honest caveat: this is an abstract proxy (competence vectors), not a real-LLM mapping. It is limited to **verifying mechanism feasibility (whether the mechanism turns).** The plateau@gen numbers indicate "the generation at which it stagnated," but the essence is the **level** of stagnation — baseline stagnates low (0.627), the adaptive family stagnates near the ceiling.

> 🤔 **Analogy**: When everyone scores full marks, you raise the difficulty (adaptive difficulty). Then scores spread out — but now everyone converges on the same way of solving (cookie-cutter). So you also add "reward unusual solutions too" (novelty), and competence and diversity coexist. **The two-sword style of "make it harder" and "reward the oddballs"** — that's the point of PoC #2.

---

## 5. The core evidence — the 10k-generation open-ended sweep (Agent A)

The self-PoCs showed the "direction." Next, it was time to hit it **at scale, rigorously.** I had parallel Agent A run an open-ended sweep of **10k generations each × pop256 × 19 configurations × 2 rounds.**

The criterion was whether it was "open-ended" — **does it avoid saturation, avoid monoculture (convergence to a single culture), and keep its archive (diversity reservoir) growing?**

### 5.1 The decisive verdict table

**verdict (at gen9999): all scalar configs = False / all novelty & lexicase configs = True**

| label | selection | std | MC | reservoir | archive | open-ended | occupied | monoculture | uniq_lineages |
|---|---|---|---|---|---|---|---|---|---|
| baseline_scalar | scalar | - | - | 0 | none | **False** | 9 | 0.74 | 1.0 |
| baseline_scalar_mc | scalar | - | ✓ | 0 | none | **False** | 9 | 0.90 | 1.0 |
| **scalar_qd** | scalar | - | - | 0 | map-elites | **False** | — | — | — |
| novelty_std | novelty | ✓ | - | 0 | none | True | 100 | 0.13 | 1.0 |
| novelty_std_qd | novelty | ✓ | - | 0 | map-elites | True | — | — | — |
| **novelty_std_res256** | novelty | ✓ | - | 256 | map-elites | True | 95 | 0.05 | **31.9** |
| novelty_std_res1024 | novelty | ✓ | - | 1024 | map-elites | True | 98 | 0.04 | 15.2 |
| **full_oe** | novelty | ✓ | ✓ | 1024 | map-elites | True | 90 | 0.05 | 15.3 |
| lexicase_std(_mc) | lexicase | ✓ | -/✓ | 0 | none | True | 111–122 | 0.03 | 1.0 |

Four decisive findings came out of this.

1. **Selection pressure is decisive.** scalar (single scalar fitness) is **extinct (False)** even with a MAP-Elites archive added (`scalar_qd`). So "add a reservoir and you protect diversity" is **wrong** — **unless the selection itself is open-ended (novelty / lexicase), open-endedness doesn't even hold.** An archive alone can't save it. **Making the selection pressure itself open-ended** was the essence.
2. **Standardization (z-score) widens QD coverage by an order of magnitude.** Adding per-dim z-score standardization to novelty takes occupied cells from 9 → 100+. Turning each axis's "deviation" into selection pressure widens behavior-space coverage by an order of magnitude.
3. **The neutral reservoir recovers lineage diversity.** With novelty_std alone, uniq_lineages is 1.0 (lineage fixed to one). Add reservoir256 and it goes to **31.9**. **Behavior diversity and lineage diversity are different axes**; the latter needs a reservoir (a re-confirmation of the knowledge already implemented in #26 design).
4. **Scale matters.** Raising the latent dimension 256 → 1024 takes niches 101 → 166 and archive 1021 (saturated) → 2234 (continued growth). Diversity can be bought with "capacity."

![Fitness and diversity of Stage1 baseline (no novelty). Diversity collapses near the end (the typical scalar failure)](./assets/lldarwin_2026_05_26/lldarwin_stage1_baseline_status.svg)

![Stage1 with novelty pressure. Behavior diversity is maintained until the end](./assets/lldarwin_2026_05_26/lldarwin_stage1_novelty_status.svg)

![Overlay of baseline vs. +novelty diversity. Collapse (scalar) and maintenance (novelty) contrasted in one figure](./assets/lldarwin_2026_05_26/lldarwin_stage1_diversity_overlay.svg)

### 5.2 The "honest limits" Agent A surfaced

It's exactly when you get a good result (open-endedness holds) that you write the limits. Agent A itself pointed this out:

> novelty/lexicase preserves the diversity of the descriptor **as a whole**, but **does not guarantee the diversity of a specific semantic dimension (factor).**
> At large latents, factor drift occurs, and fspread (the spread of factors) needs monitoring.

In other words, even when "diverse as a whole," it may be "converged on the specific semantic dimension of thought factors." This gave rise to a new requirement, **factor-subspace QD (a QD that protects each semantic dimension individually)** (addressed in PoC #6 below).

> 🍵 **Break point**: This is the densest section of the article. The one line to take home: **"Adding an archive (reservoir) alone can't save it. Unless the selection pressure itself is open-ended, it fails."** Since #25/#26 design we've said "don't aggregate," but its core was that **"open-ending the way you select"** — and 10k generations of real data declared it. Past this point, it's all about originality.

---

## 6. The core of originality — "let a continuously-evolving population perform an ensemble without stopping"

By now, the "selection core that structurally avoids saturation (S1)" was solidified. Next, it was time to back up — with PoCs and literature — the **three originality axes** the user laid out in dialogue.

The three axes the user articulated were these.

1. **Continuously-evolving population = live orchestra (ORCH)** — a continuously-evolving population performs MoA (Mixture-of-Agents) aggregation on the spot to produce one answer. Evolution never stops. **The biggest differentiation candidate.**
2. **Individuals with investigation capability (AGENT)** — individuals go investigate by themselves. Voyager-style.
3. **Observation / interactive control (OBS)** — view per-individual responses + selection-score time series, pause, and resume.

### 6.1 The white-space Perplexity backed up

The Perplexity SOTA survey (1143 lines) running in parallel returned the most important backing.

> A "**continuously-operating system integrating online evolution + online answering**" has no clear prior research = a **research white-space.** The closest are MoA / Self-MoA / sequential aggregation / routing, but none is identical.

In other words, "stop evolution and answer with the strongest individual produced" is ordinary. "Without stopping evolution, have the evolving population itself perform an ensemble and answer" — nobody has done it yet. **The differentiation of ORCH §1.11 was confirmed.**

### 6.2 But Perplexity also gave a counter-warning

As honest disclosure, I write the **counter-warning** Perplexity gave with equal weight.

> In 2025's **Self-MoA research**, **diversity is not automatically superior.** Iterating a single top model beat a heterogeneous-mix MoA by 6.6% on AlpacaEval (a quality-diversity trade-off).

"An ensemble of a population is stronger than a single individual" is **not self-evident.** Prior research warns that diversity can even be counterproductive. So ORCH is "prove it empirically, with an honest pass-bar." I verified this with Agent C and self-PoCs #3/#4.

> 🍵 **Break point**: This is the branch point where research integrity is tested. Right where you want to get carried away with "online evolution + online answering is white-space! originality!", Perplexity pours cold water with "but there's a counter-result that diversity isn't automatically good." **Receive both the elation material and the cold water within the same investigation.** Do this, and the conclusion gets much stronger. In the next section, I unravel the true nature of that cold water.

---

## 7. Unraveling the "true nature" of the Self-MoA counter-result (self-PoC #3 → Agent C real LLM)

"Diversity is not automatically superior" — unraveling this counter-result at the **mechanism level**, not in proxy, is the climax here.

### 7.1 Self-PoC #3 — voting, or routing?

First, it couldn't be verified in proxy (with saturated fitness the single best is already at full marks = zero headroom, so no difference shows). So I synthesized **"hard tasks a single individual can't ace"** (experts dispersed, single_best=0.5) and measured.

| Configuration | best_of (routing) | majority (vote) | domain coverage |
|---|---|---|---|
| single_best | 0.500 | — | 2/4 |
| MoA redundant (top-k) | 0.750 | 0.500 | 3/4 |
| MoA diverse (max-cover) | **1.000** | **0.000** | 4/4 |

Here a **decisive finding** emerged.

- Diverse MoA is **1.000 with best-of / routing** (double the single best). **ORCH holds.**
- **But with naive majority (a vote), diversity is counterproductive** (diverse = 0.000). On each sub-task, the one competent expert gets negated (canceled out) by the ignorant majority. Redundant MoA's majority (0.500) is higher.

In other words, **the true nature of the Self-MoA counter-result (diversity ≠ automatic superiority) was "whether the aggregator is voting or routing."** Voting/averaging kills diversity; competence-aware routing/gating leverages it. It's the difference between "an orchestra with a conductor" and "a crowd where everyone plays whatever they want."

### 7.2 Agent C's real LLM independently produced the same conclusion

And then — parallel Agent C, with a **real LLM (llama3.2, 105 LLM calls, 15 tasks)**, produced the **same conclusion independently** of self-PoC #3.

- single best = **0.933**. MoA `best_of` + k≥5 reaches **1.000** (+0.067). **majority / weighted never exceeded 0.933.**
- diverse > redundant (diverse selection picks up complementary specialists in different QD cells earlier, with fewer k).
- The improvement is **entirely from one multistep question** ("double 5 and subtract 3"). The CoT-individual group all drops one question, and the heterogeneous individuals from diverse selection solved it.

> 🔑 **Independent cross-validation (the core of this article)**: Self-PoC #3 (synthetic, dispersed experts) and Agent C (real LLM, llama3.2) reached the **same conclusion via different methods** — "MoA beats the single best only with competence-aware routing (best_of) / voting doesn't get there / diversity has value only under routing." Two methods agreeing is extremely strong evidence in honest disclosure terms.

### 7.3 The biggest hole — does a "real router" reach the oracle? (self-PoC #4)

Here Agent C pointed out the biggest hole. "best_of is **oracle routing** (the upper bound where God knows which individual is correct); in reality, the accuracy of the **gate that predicts** 'which individual is competent' is the bottleneck. Real voting (majority) doesn't reach the oracle."

I filled this with self-PoC #4 (real router vs. oracle, averaged over 20 seeds).

| κ (calibration) | single | majority | conf_router | specialty_router | oracle |
|---|---|---|---|---|---|
| 0.0 | 0.675 | 0.338 | 0.525 | **0.902** | 1.000 |
| 0.3 | 0.675 | 0.338 | 0.883 | 0.910 | 1.000 |
| 0.6 | 0.675 | 0.338 | **1.000** | 0.912 | 1.000 |
| 0.9 | 0.675 | 0.338 | 1.000 | 0.912 | 1.000 |

- **The descriptor / specialty-router is robust at 0.90 with no calibration needed** (stably beating the single best 0.675, near the oracle). Moreover, **the routing key can reuse the behavior descriptor already computed for QD** — a synergy where **QD and ORCH share the same descriptor foundation.**
- **The confidence-router reaches the oracle at calibration κ≥0.6.** But small LLMs may be weakly calibrated → **make the descriptor-router the first choice** (calibration-independent).
- **majority = 0.338 is decisively unfit** (agreeing with PoC #3 and Agent C — a **third agreement**).

**Conclusion**: The hole Agent C pointed out — "real voting doesn't reach the oracle" — is **practically filled by descriptor-routing (reusing the QD descriptor).** ORCH holds end-to-end in proxy + (partial) real LLM.

> 🤔 **Analogy**: Gather 10 experts and have them vote, and the ignorant majority cancels out the correct experts. Route the math question to the mathematician — you need a **dispatcher (a conductor = routing).** And that conductor's score (behavior descriptor) can reuse what's **already been computed** to manage diversity. Voting (majority) kills the expert; the conductor (routing) leverages them. This is the point of PoC #4.

---

## 8. Giving individuals the "power to investigate" (self-PoC #5)

The second of the three originality axes: **individuals with investigation capability (AGENT).** The idea is to let individuals do sandboxed read-only investigation in the search space. But "investigation isn't free" — when you charge a cost, does evolution learn to use investigation well?

Self-PoC #5 (vary cost λ and see how the investigation threshold θ evolves, averaged over 20 seeds).

| λ | θ* (=λc, optimal threshold) | θ_evolved (threshold evolution acquired) | evolved | always | never |
|---|---|---|---|---|---|
| 0.0 | 0.00 | 0.049 | 21.46 | 21.47 | **11.70** |
| 0.3 | 0.30 | 0.476 | 21.34 | 21.26 | 21.20 |
| 0.6 | 0.60 | 0.659 | **21.24** | 21.06 | 21.21 |
| 0.9 | 0.90 | 0.888 | 21.21 | 20.85 | 21.21 |

- **Evolution acquired the selection threshold θ → λc on its own** (= selective investigation, "investigate only when you should," **emerged**).
- **The value of investigation capability is clear**: when λ=0 (investigation free), never (never investigate) = 11.70 = **a 45% loss.**
- **Cost λ degrades "always investigate" and forces selection.** AGENT-3 (the cost principle) holds.

Honest caveat: the margin at intermediate λ is small (a shallow reward landscape), and this too is an abstract proxy (real LLM × knowledge base is a separate matter). Still, the mechanism "with a cost, selective investigation emerges" was confirmed in proxy.

---

## 9. Scale "qualitatively increases diversity" (Round 3)

Finally, I verified Agent A's "you can buy diversity with capacity" also via population size. With the `full_oe` configuration (novelty + std + MC + reservoir1024 + map-elites), I swept pop from 256 → 4096.

| pop | gens | occupied niches | monoculture | uniq_lineages | distinct_genomes | bspread_tail |
|---|---|---|---|---|---|---|
| 256 | 5000 | 171 | 0.047 | 14 | 256 | 0.939 |
| 1024 | 3500 | 467 | 0.019 | 74 | 1022 | 1.003 |
| 2048 | 2500 | 754 | 0.009 | 188 | 2041 | 1.071 |
| 4096 | 1200 | **1219** | **0.006** | **372** | 4054 | 1.253 |

With population-size scaling, open-endedness improved **monotonically** (niches 171 → 1219 / monoculture 0.047 → 0.006 / uniq_lineages 14 → 372 / behavior spread bspread also monotonically up). The POP-1 hypothesis (population size increases diversity) was supported in proxy.

**Honest (confound made explicit)**: there's an honest pitfall here. To raise pop, I shortened gens (5000 → 1200). This is **a confound in the direction unfavorable to niche accumulation.** Yet it still increased monotonically — i.e., **the POP effect is a robust lower bound** (it should actually be stronger). Conversely, "the possibility that it's stronger" couldn't be proven in this experiment. The claim is limited to proxy mechanism feasibility.

![Winner-individual thought-factor × memory-layer heatmap (Genome3D). Under real-pressure, c_factors drift neutrally, so treat this as a reference visualization of a cognitive profile](./assets/lldarwin_2026_05_26/lldarwin_genome_heatmap.svg)

> 🍵 **Break point**: "Scale up and diversity increases" is intuitive, but the important thing here is the honesty that **"even when we added an unfavorable confound, it still increased monotonically."** Cutting gens is normally unfavorable to diversity. It increased anyway. So we can call it a "lower bound." Writing a good result as a "lower bound" rather than exaggerating it as an "upper bound" — this too is the manner of honest disclosure.

---

## 10. By morning, everyone had arrived at the same conclusion — the finalized strategy

In one all-nighter, **6 self-PoCs + Agent A/B/C + Perplexity independently converged on the same conclusion.** This is the power of honest cross-validation. We discarded the fixed-ruler line and finalized the following as the core of lldarwin v2.

### S1. The selection core (structurally avoid saturation)

- **Abolish fixed scalar quiz fitness** (baseline saturates at 10k generations + monoculture 0.9 + diversity collapse = large-scale reproduction of the 12h pathology, open-ended 0/6).
- **Selection = novelty / ε-lexicase (z-score standardization mandatory) + minimal-criterion.** **A MAP-Elites archive alone won't do** (scalar_qd also goes extinct) = make the selection pressure itself open-ended.
- **Quality is also needed, so QD (quality × diversity per cell)**: pure novelty sacrifices scalar quality (0.77-0.83) → pair with adaptive difficulty (conditional curriculum) to supply a quality gradient (PoC #2).
- **Lineage diversity is secured separately with a neutral reservoir** (behavior diversity ≠ lineage diversity; res256 takes uniq_lineages 1 → 32).
- **Add factor-subspace QD** (protect semantic-dimension diversity individually; addressing Agent A's factor-drift limit; PoC #6).

### S2. How to produce results = continuous evolution × live orchestra (the core of originality)

- The deliverable is not a single best but **continuously evolving the QD archive and performing a MoA orchestra at any point in time to produce one answer** (ORCH; integrating online evolution + online answering is white-space = originality, confirmed by Perplexity).
- **Aggregation must be competence-aware routing/gating (a conductor), not voting** (self-PoCs #3/#4 + real-LLM Agent C agree threefold).
- **The routing key reuses QD's behavior descriptor** (the descriptor-router is calibration-independent and near-oracle at 0.90) = QD and ORCH share the same descriptor foundation (design economy).

### S3. Individuals = agentic individuals with investigation capability (staged introduction, proxy-verified)

- In the search space, only sandboxed read-only investigation (real I/O after one-way promotion via the Approval Bus). Investigation incurs a cost.
- **Proxy-verified (PoC #5)**: cost λ makes "selective investigation" emerge. AGENT-3 (the cost principle) holds. Real LLM × knowledge base is the next stage.

### S4. Observation / interactive control (implemented = standard in all runs, Agent B done)

- Response logs / per-individual score time-series viewer / lineage reconstruction (evolution-system 886 tests green). step/pause/resume to be wired in the next stage.
- Agent B's lineage reconstruction resolved the lineage display that was "**all ?**" in the 12h data, resolving the champion lineage gen70 → gen59 over 12 hops. Gaps are not fabricated but explicitly marked `lost@genN` (root cause = parent IDs couldn't be traced from either the snapshot or the winners alone). The observability foundation is the very bedrock of honest disclosure.

### Self-PoC #6 — factor-subspace QD addresses Agent A's limit

| mode | factor_spread | retention | latent_spread |
|---|---|---|---|
| full_only | 1.017 → 0.500 | **49.5%** | 0.545 |
| full_plus_factor | 1.092 → 0.737 | **68.1%** | 0.588 |

Imposing a separate novelty for the semantic dimension (factor) roughly halves the loss of semantic-dimension diversity (50% loss → 32% loss). An effective measure for Agent A's factor-drift limit, demonstrated in proxy. Honest: not fully fixed but 68% retained = the remaining drift needs combining with the neutral reservoir or strengthening factor weights.

---

## 11. Lessons (kept as honest disclosure)

- **Even a real LLM saturated.** Even swapping the lens from proxy to real LLM, with a fixed ruler it's full marks at gen5.
  "Use a real LLM and it'll evolve" was a **lie.** The problem was the way the ruler was built.
- **Adding an archive alone can't save it.** "Hold a diversity reservoir and diversity is protected" is wrong.
  scalar selection went extinct even with a QD archive added. **What saves it is open-ending the selection pressure itself.**
- **Diversity isn't automatically good.** The true nature of the Self-MoA counter-result is "voting or routing."
  Only with a conductor (competence-aware routing) does diversity become a value. Voting kills experts.
- **Independent cross-validation strengthens the conclusion.** Self-PoCs (synthetic), Agent C (real LLM), and Perplexity (literature)
  separately converged on the same conclusion — that's why you can trust it. A conclusion from the same mind shares the same bias.
- **Proxy is only mechanism feasibility.** This article's PoCs verify "whether the mechanism turns," not a claim of "general capability improvement of real LLMs." The moment you cross this line, the research becomes a lie.
- **Record the tool that didn't work (Codex), too.** Not just successes but duds, honestly.

In short — **"once the lens (evaluation) saturates, no amount of polishing the selector helps."** So we shift what we polish — not the selector, not the LLM, but **open-ending the evaluation itself.** That's the conclusion of the all-nighter.

> 🍵 **Break point**: In #25 I decided to "expose failure." In #26 design I built a "non-aggregating selector." And this time, a real LLM taught me "that's still not enough, because the ruler is fixed." **Failure breeds the next design, and the limits of that design breed the next.** This is the backbone of the series. The flashy "AI got smarter through evolution!" — I haven't written it even once. Because the evidence to write it isn't in place. When it is, that's when I'll write it.

---

## 12. Conclusion

- The real-LLM 12h run was an "honest fail" — filtered random search that doesn't go extinct but doesn't accumulate. The root cause is saturation of the fixed ruler (demonstrating #25's insight with a real LLM).
- The overnight distributed investigation (6 self-PoCs + Agent A/B/C + Perplexity) independently converged on the same conclusion = **honest cross-validation.**
- Finalized strategy: **S1 an open-ended selection core** (novelty/lexicase + std + MC + QD + adaptive difficulty + neutral reservoir + factor-subspace QD) / **S2 continuous evolution × routing-MoA** (white-space originality, a conductor not voting) / **S3 agentic individuals + cost** (emergence of selective investigation) / **S4 observation** (implemented).
- All elements backed in proxy / (partial) real LLM. Remaining work: "wiring to the real-LLM stage," "factor-subspace QD implementation," "scale-up." The core strategy is finalized.

Build good parts, bundle them without aggregating, verify saturation with a real LLM, and rebuild toward open-ended selection. And only when 6 independent verifications arrive at the same conclusion can we finally say "the strategy is decided." This article is precisely the "**when the lens clouds, the selector is powerless too**" installment foretold in #25 — honestly exposing the moment the lens clouded with a real LLM (saturation), taking on Goodhart's law and the limits of proxy, then rebuilding toward open-endedness. Next is the **implementation phase** that turns this finalized strategy into code.

---

## 13. Related

- Series #24-05 "AI that learns as a population" — the framework of derivative-population evolution (the premise of this article)
- Series #24-08 "Building the lens" — lleval (the measuring side)
- Series #25 "Only Friston and I were left" — the honest disclosure of monoculture (the motivation of this article)
- Series #26 (design) "Measuring with a lens alone doesn't make it evolve" — the design of the selector lldarwin and the Stage1/1.5/2 measurements (the sister article)
- Pioneer paper (2026-05-27, date of record) "Continuously-Evolving Populations as Live Orchestrated Ensembles" — a defensive publication formalizing this article's strategy in academic form (FullSense public repository `docs/papers/`)
- Related memory: [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]] / [[feedback_poc_feasibility_first]] / [[feedback_parallel_first_execution]] / [[feedback_originality_over_imitation]]

---

<!-- TODO(投稿前): hero SVG / theme SVG / 進捗 badge / #24-05・#24-08・#25・#26設計編・#27 の Qiita URL cross-link -->
<!-- KEY MESSAGE: 実 LLM でも固定ものさしは飽和する。archive を足すだけでは救えない、選択圧そのものを開放端化せよ。多様性は投票でなく competence-aware routing でのみ価値。独自性=連続進化×ライブオーケストラ(white-space)。自己PoC6本+Agent4体+Perplexityの独立収束=honest cross-validation。 -->
<!-- NUMBERING NOTE (2026-05-27 解消済): 本記事=#27(マラソン climax)。#25 で予告した「眼鏡が曇ると淘汰も無力」枠を、実 LLM で食らった+開放端転回として実現。設計編 #26(drafts/QIITA_#26_lldarwin_multi_pressure_selection.md) は #26 のまま温存=番号衝突なし。 -->
