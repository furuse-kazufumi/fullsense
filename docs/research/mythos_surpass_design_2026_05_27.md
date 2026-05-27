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

## 8. PoC-CTF-0 進捗 (2026-05-27)
- **ハーネス着地**: llive `scripts/poc_ctf_coverage.py`。決定論オラクル付き CTF マイクロバッテリ(base64/hex/rot13/reverse/url/caesar/atbash/binary, 難易度幅あり)+ persona system prompt 3 種(terse/analyst/pattern)+ `OllamaBackend` 再利用(on-prem)。`single`(1 モデル反復) vs `diverse`(複数モデル×温度×persona) の coverage@k を比較。`--mock` で inference ゼロ検証可。
- **mock 検証 OK**: coverage 曲線(単調非減少)・pass@1・集計・JSON 出力すべて正常(96 calls=8×6×2)。
- **🔴最重要 honest 教訓 (mock で判明)**: **naive な均等多様化は単一強モデルに負けうる** (mock: diverse cov@k 0.875 < single 1.000)。強モデルが 1 つあると、サンプル予算を弱モデルに**均等分散**させると coverage が薄まる。→ **多様性は「単一モデルが外す盲点」に集中投下しないと勝てない** = competence-aware routing / ε-lexicase specialist / 進化が難問に予算集中する根拠。指標が両方向に動く=測定器として妥当。
- **設計含意 (PoC-1 へ)**: (1) **第一レバー = 単一(最強 on-prem=qwen2.5:14b)の coverage@k を k で押し上げる**(test-time scaling 本体)。(2) **第二レバー = 単一が saturate < 1.0 のタスク(真の盲点/entanglement)でのみクロスファミリ多様性を効かせる**。均等でなく**盲点ターゲット配分**。これを進化(lldarwin の ε-lexicase = 軸別 specialist 共存)で自動化するのが本筋。
- **実機 smoke 結果 (qwen2.5:14b, 4 易タスク, k=4)**: アダプタ end-to-end 動作確認(32 calls, exit 0, JSON 出力)。coverage single=diverse=0.75 (4 易タスクのみで diverse 優位は出ない=想定内)。**🔴重要実態**: (1) **qwen2.5:14b の cold ロードが OllamaBackend 既定 timeout(120s) を超え 2 回 TimeoutError** → `RealResponder` に **timeout=300s + warmup()** を追加して対策済。(2) **932s / 32 calls ≈ 29s/call** = 極めて遅い → 「計算リソース限定」が**結合制約**。**大規模 pass@k sweep は非現実的** → 戦略を「**mock でロジック開発 + 極小実機確認 + temp=0 キャッシュ + warmup**」に確定。**含意**: ブルートフォース pass@k(巨大 k=巨大 compute) より **sample-efficient な進化 specialist 配分**(少サンプルで盲点被覆)の価値が相対的に上がる。
- **on-prem 在庫**: qwen2.5:14b(最強) / 7b / llama3.2:3b。OLLAMA_HOST 未設定=localhost。
- **RAD corpus 拡張(継続)**: `D:/docs/ctf_exploit_corpus/` 新設、arXiv 12 クエリで fetch background 稼働(64+ 本着地, "Demystifying the Mythos" 含む)。v2 化コマンドは保留記録。

## 9. PoC-CTF-1 設計 (進化連結 = 真の差別化)
**命題 (falsifiable)**: ε-lexicase 進化で得た個体群(= evolved diverse ensemble)の集団 coverage は、(a) 単一最強個体、(b) 非進化の均等多様ミックス(PoC-0 diverse)、を**上回る**。上回らねば「進化」の付加価値は無い → honest に報告。

**鍵となる対応関係**: **進化集団そのものが奏者アンサンブル**。
- 各個体 = (persona/c_prompt で決まる) 1 つの解法戦略。temp=0 で決定論化し `(system_prompt, task)` をキャッシュ(poc_orchestra 流, compute 節約)。
- **ε-lexicase が「異なるタスクを解く specialist」を集団に共存させる**(集約しない多目的選択 = 各タスク=1 case)→ 集団が自動的にタスク空間を**被覆**(盲点ターゲット配分を進化が達成。PoC-0 の「均等多様化は負ける」教訓への解)。
- **答え時 (answer-on-demand)**: 決定論オラクルが集団メンバーの flag を verify → **集団 coverage = best-of-population がそのままデプロイ可能**(poc_orchestra の「best_of は oracle 上限で deploy 不可」を決定論オラクルが解消)。
- novelty + 中立貯蔵庫 = specialist 系統の絶滅回避(coverage 天井を守る)。

**実装計画 (real_pressures.py パターン踏襲, additive)**:
1. `security_pressures.py` (新規): CTF バッテリ(poc_ctf_coverage の BATTERY を昇格/拡張)を ProxyPressure 群に写像。各タスク=1 lexicase case。個体 c_prompt→system prompt→ollama(temp=0)→flag オラクル採点。`make_ctf_fitness()` + `--fitness ctf-security`。
2. `run_persona_evolution(--fitness ctf-security --selection lldarwin-v2)` で進化 → 各世代 snapshot。
3. 計測スクリプト(poc_orchestra を拡張 or 新規): 世代ごとに「集団 coverage(best-of-pop) / 単一最強 / PoC-0 均等 diverse」を比較プロット。pass@1 と coverage 分離。
4. compute 節約: 小バッテリ + temp=0 キャッシュ + 小集団(16-32) + 少世代でまず兆候を見る。

**PoC-2/3 への接続**: ここで coverage が伸びれば、InterCode-CTF(実 CTF, Docker flag 採点) → Cybench(Mythos 100% 正対) へ同じループを移植。バッテリを実 CTF タスクに差し替えるだけ(オラクルは flag 一致で不変)。

### PoC-CTF-1 実装＋mock 検証結果 (2026-05-27, 独立再現済)
- **着地**: llive `scripts/poc_ctf_evolution.py`(additive)。既存を再利用 = `genome_to_system_prompt` / `build_lldarwin_v2_selector`(ε-lexicase 確定 S1) / `run_persona_evolution`(Genome3D + diverse founder + selection 注入 + 世代 snapshot)。**MultiPressureSelector が個体 `fitness.breakdown` から数値 case を自動抽出**するため、fitness が `ctf::<tid>` を 0/1 で入れるだけで各タスク=1 lexicase case になり specialist 共存が成立(自前 ε-lexicase 不要)。既存進化系 **78 tests pass・回帰なし**。
- **mock verdict (pop12/gens16/10タスク, 独立再現)**: **evolved pop coverage 1.000 vs 単一最強 0.800 (+0.200) vs gen0 均等 diverse 0.900 (+0.100)** = **命題支持**(非飽和 regime)。ε-lexicase が gen5 で gen0 に欠けた `atbash` specialist を集団に確立 → 被覆完成。persona founders=furuse/friston/millidge/isomura(persona_genome_integration 実機)。
- **honest 留保**: (1) **飽和 regime(易タスクのみ)では単一個体が 1.0 飽和→進化の価値ゼロ**(PoC-0 教訓の再現)。(2) 大きい独立 random ミックスは小タスク空間を shotgun で 1.0(進化の価値は raw coverage 競争でなく「同じ種から選択圧で被覆を伸ばす」点)。(3) **mock は合成 responder で specialty を埋込済=ロジック/配線検証専用。実機予言でない**。実 on-prem モデルが実 CTF で decorrelated specialty を本当に持つかは**未実証**(次の実機の crux)。
- **次の核心増分**: (a) **クロスファミリ多様性の進化的配線**=個体 genome `backend_id` 次元→responder のモデル選択(qwen↔llama)に写像し、「どのモデルを使う specialist か」を進化させる=Agent A 指摘の **entanglement root blocker への直撃**(設計 §3)。mock 検証可。(b) その後 **1 本の overnight 実機ラン**(弱/クロスファミリ, temp=0+cache, 有界)で「単一が飽和せず進化が伸びる難度帯」を実 CTF で同定。

## 7. 登録 TODO
本 doc と `mythos_competitor_spec_2026_05_27.md` を `docs/research/index.md` / `doc_map.md` に登録([[feedback_fullsense_feedback_smart]])。
