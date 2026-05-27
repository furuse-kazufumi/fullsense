# 設計正本 — 進化型オーケストラで Claude Mythos を超える (セキュリティ領域, 2026-05-27)

> 親ゴール: [[goal_surpass_mythos_evolutionary]] / 競合スペック: `mythos_competitor_spec_2026_05_27.md` / 親計画: [[project_llive_optimization_cycle]] Phase C。
> 制約: 計算リソース限定・**速度不問**・**on-prem only**(measurement purity)。直接対決不可 → 公開数値(Cybench pass@1 100%)を proxy バーに実測比較。

## 0. 一行テーゼ
**決定論的セキュリティオラクルがある検証可能タスクでは、弱い on-prem モデルでも「進化で多様化した生成 × 無制限 test-time サンプリング × オラクル選別」でフロンティア級カバレッジに到達できる。**

## 1. アーキテクチャ (RAPTOR × llive 合流)
```
生成(coverage)            選別(precision)              試行(無制限)
llive 進化オーケストラ  →  RAPTOR 決定論オラクル     →  test-time compute
lldarwin v2:               flag一致 / exploit ACE /      pass@k・世代・集団・
ε-lexicase+novelty         crash再現 / ASan・UBSan       MoA集約 を sweep
+中立貯蔵庫+persona        (LLM判定でない=Goodhart耐性)  (speed不問で押し上げ)
```

## 2. 先行研究の含意 (RAD 調査 2026-05-27, Agent A)
| 論文 (year) | 含意 | 本設計への反映 |
|---|---|---|
| PACE: Defying the Scaling Hypothesis (2602.05370) | Best-of-N は N≥8 で diminishing returns・policy collapse。verifier noise が分布シフト | **決定論オラクルで noise を排除**。k は中庸(2-8)から sweep し collapse 点を実測 |
| Multi-Agent Reasoning Improves Compute Efficiency (2605.01566) | MoA が debate を上回り Pareto 最適 (+7.1% vs CoT @20x) | MoA 集約を採用。debate は後回し |
| How Independent are LLMs? (2604.07650) | **behavioral entanglement**: 18 LLM の 53% が同じ error mode 共有。脱相関加重で +4.5% vs majority | **root blocker**。クロスファミリ(qwen↔llama)+進化多様性+uncertainty 加重で脱相関 |
| CoTEvol (2604.14768) | 遺伝的 CoT 進化で +6.6% (軌跡交差+不確実性変異) | 個体の c_prompt 進化に CoT 軌跡多様化を組込む方向性 |
| ContextualJailbreak (2605.02647) | 進化的 red-teaming が弱モデルで ASR 100%・frontier へ転移 | exploit/攻撃生成の進化的探索が弱モデルでも有効な傍証 |
| Verifiable Process Rewards (2605.10325) | 中間アクションを symbolic oracle で密検証 → long-horizon credit | RAPTOR の evidence ladder を process reward 化(段階点) |
| Reward Model Ensembles Mitigate Overopt. (llm_v2) | WCO/uncertainty 加重で overoptimization 排除・BoN +70% | オラクル過適合(Goodhart)対策に uncertainty 加重 |

## 3. 最重要 honest 洞察 (差別化の核)
Agent A の feasibility 反証 = 「弱モデルの entanglement で verifier が Goodhart 化」。これは **汎用推論(LLM-judge)** での話。**我々はアリーナをセキュリティに選んだことでこの壁を構造的に回避する**:
- オラクルが **決定論的 ground-truth**(flag==flag / exploit が刺さるか / crash するか)→ verifier 偽陽性が原理的にほぼゼロ。Goodhart の主経路を封じる。
- 残る壁は **coverage 天井**: 全弱モデルが同じ問題を外せば pass@k は 1 未満で頭打ち。
- → coverage を上げる手段 = **クロスファミリ多様性(qwen2.5 ↔ llama3.2)＋進化した prompt/persona/温度多様性**。これは進化オーケストラの本務。**「進化で生成多様性を作り、決定論オラクルで選別」= 我々の white-space**。
- HONEST 留保: (a) 決定論オラクルでも「flag は当てたが理解は伴わない」運ゲー成分は残る→pass@1 と pass@k を分けて報告。(b) coverage 天井がモデル能力で決まる領域では到達不能→「弱モデルでも届く難度帯」を明示。

## 4. 再利用資産 (Agent B 棚卸し, 要実コード検証)
**verifier 側 (RAPTOR)**: `packages/exploit_feasibility/api.py` analyze_binary()→verdict+constraints(機械) / crash oracle(ASan, bool) / `packages/exploitability_validation/orchestrator.py` evidence ladder(段階点) / technique viability。→ **exit-code 化と fitness vector 正規化のミドルウェアが新規**。
**generator 側 (llive)**: `src/llive/perf/evolutionary/` の lldarwin_v2(ε-lexicase+novelty+adaptive gate) / real_pressures.py(genome→system prompt→ollama 採点) / lineage_reservoir / loop.py hooks。→ **fitness 関数差込で即動く**。
**新規**: ①ExploitChromosome(将来) ②RAPTOR↔llive connector(result→[0,1] fitness) ③security task battery(決定論オラクル) ④CLI runner ⑤exploit-aware operators。

## 5. 段階的 PoC ロードマップ (feasibility-first・多彩条件で反復)
- **PoC-0 (最小・低 compute, まず最初)**: Docker 非依存の**決定論オラクル CTF マイクロバッテリ**(base64/caesar/xor/hash 同定/文字列探索 等、flag が機械判定可)+ ollama adapter(localhost:11434/v1)。測る = **coverage(any-correct) vs サンプル予算**を「単一 qwen2.5:14b」vs「多様ミックス(複数モデル×温度×進化 prompt)」で比較。**テーゼ(多様性が coverage 曲線を押し上げるか)を最小 compute で検証**。
- **PoC-1**: 上を lldarwin v2 進化ループに接続(real-security-pressure: 個体→prompt→タスク→オラクル採点→ε-lexicase 淘汰)。世代で coverage が伸びるか。
- **PoC-2 (実 CTF)**: InterCode-CTF(Docker, flag 採点)へ移植。単一モデル baseline → オーケストラ pass@1/pass@k。
- **PoC-3 (正対比較)**: Cybench(Apache-2.0, ollama adapter 改修)で **Mythos 公開 100% pass@1 と同一ベンチ実測比較**。
- 各 PoC は `experiments/` 相当に条件と結果を記録(honest 内訳)。異常に良い結果は内訳を疑う([[feedback_benchmark_honest_disclosure]])。

## 6. 評価指標
- **coverage@k** (any-of-k が正解) — test-time scaling の主指標。
- **pass@1** (素の能力) と **pass@k** を必ず分離報告。
- **compute 予算** (総サンプル数・総トークン) を併記 = 速度不問でも「どれだけ投下したか」は honest disclosure。
- **gap-to-Mythos** = 公開数値 − 実測。Cybench は 100% 基準(到達度)、難度帯別 coverage。

## 7. 登録 TODO
本 doc と `mythos_competitor_spec_2026_05_27.md` を `docs/research/index.md` / `doc_map.md` に登録([[feedback_fullsense_feedback_smart]])。
