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

### Round 1 → 次手（dispatch 予定）
- 自己 PoC #2: 「適応難易度 **+** novelty 選抜」で能力と多様性を**両立**できるかを直接検証（相補仮説の検証, Agent A の選択 sweep と非重複の組合せ）。
- A(開放端 sweep)/C(オーケストラ) 完了待ち → 結果を本台帳へ。
- B 成果（応答ログ）を活かし、次 real-pressure ランは `--response-log @out` 付き＋難化バッテリで起動する方針。

<!-- 以降、各ワーカー完了ごとに結果と次手を追記 -->

---

## 4. 現時点の方策（朝までに確定させる本体・随時更新）

> 暫定。証拠が積まれるたびに更新。最終的にここが「決めた方策」になる。

- **方策仮説**: 固定 quiz fitness を捨て、**QD アーカイブ（MAP-Elites）+ novelty/ε-lexicase + minimal-criterion** を選択核に据える。成果物は単一 best でなく**多様な elite の archive**。その archive を**連続進化させつつ MoA でオーケストラ**して 1 答を出す。個体は段階的に**サンドボックス調査機能**を獲得。**観測（応答+スコア時系列+lineage+step/resume）を最初に整備**。
- **検証ゲート（この仮説を採用してよい条件）**:
  1. 開放端構成が baseline の飽和・全滅を**実データで回避**（A: monoculture<0.8 / archive 末尾成長 / 多様性高止まり）。
  2. MoA アンサンブルが単一 best を**上回る**（C: ORCH-4）。上回らなければ ORCH は棄却。
  3. 観測基盤で「個体別応答＋選択スコア＋系統」が**実際に見える**（B）。
- **却下条件（honest）**: 上記が示せない構成は正直に棄却し台帳に残す。
