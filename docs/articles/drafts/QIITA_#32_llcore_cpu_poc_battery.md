---
title: "llcore — Transformer のコアを CPU で進化させる: Verified Neural Architecture Evolution の最小 PoC battery"
tags: ["Python", "進化計算", "Z3", "RWKV", "形式検証"]
private: true
updated_at: "2026-05-29"
id: 88ed294aa107330c6894
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# (連載 #32) llcore CPU PoC battery 完成

## TL;DR

- Transformer の **コア計算 (state update / 学習則 / 認知駆動 Δ)** を進化対象にする研究フレームワーク `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 独立路線) の **CPU PoC battery 完成**
- **5 PoC / 39 falsifiable gates / 76 tests / Codex pair-review 5/5 Green-light** で機構実証
- **Z3 で構造変異を online gate** = 進化探索の selection pressure に SMT を組込んだ先行未発見 (事前調査 RAD 14 分野 + Agent A-D 確認)
- 投稿先候補: TMLR (本命) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

## なぜ作ったか

LLM 重みは凍結が標準だが、**コア計算アルゴリズム自体は人手設計に固定**されている。AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge など architecture/algorithm 探索は進んだが:

1. **個人 compute では計算リソース不可能** (TinyLlama 1.1B from scratch = $140k / 90 日 / 16×A100)
2. **探索中の安全性保証なし** = 数値不安定な architecture を生み出して時間浪費
3. **検証付き探索は静的 verification (Reluplex/Marabou/α,β-CROWN) と分断** — 進化ループ内 SMT online gate の研究は未発見

## 確定独自軸 (事前調査で negation work なし)

mechanism 実証済 (4 軸):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **state update 規則を遺伝子化 RWKV-style** (Stage 0a v2)
3. **factor_hook (認知状態 → SSM Δ)** (Stage 2a mock)
4. **自前進化器 + verifier 基盤** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / VNN-COMP 新カテゴリ提案。

## PoC レダー (5 stage / 39 gates 全 PASS)

| PoC | 内容 | キー数値 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 自前 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

## v1 の失敗から学んだこと (honest disclosure)

PoC 0a v1 は `decay*s + mix*x*tanh(gate_str*s)` で **state=0 が fixed point の zero attractor** = G1-G5 形式 PASS だが情報伝達ゼロ。Claude 単独で見落とした設計問題を **Codex (gpt-5.4) と gem-critic の独立 verdict** が検出し RWKV-style に v2 redesign。

→ **5 PoC 中 4 件で Claude 単独では見落とした設計問題を Codex pair-review が検出**。構造破綻防止に相互レビューが機能した実例。

## 次の選択肢

a. Stage 3 kernel 多様化 (rwkv/mamba/hopfield/linear-attn を遺伝子化)  
b. Stage 4 学習則 (FF/EP/PCN/Hebb) を gene 化  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. PrediPrune+Quokka で Z3 gate 高速化  
e. FlashEvolve で 3.5-5x wall-clock 高速化  
f. 論文化 (TMLR + GECCO 2027)

## Honest 留保

- mock 中心、実 LLM/重み接続は GPU/新 PC 待ち
- 1 step scalar invariant の over-approx proof 段階、多次元・多 step は post phase
- tanh 上界近似は保守的 (sound だが完全でない)

---

**Tags**: 進化計算 / 形式検証 / Z3 / RWKV / state space model / CPU研究  
**関連**: 連載 #14-31 (llive lldarwin v0.B-E + 観測+governance + lleval)  
**Project**: D:/projects/llcore (PyPI llmesh-llcore 0.1.0a0)

---

# English

# (Series #32) llcore CPU PoC battery complete

## TL;DR

- **CPU PoC battery complete** for `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, an independent llive track), a research framework that makes the **core computation of a Transformer (state update / learning rule / cognition-driven Δ)** the target of evolution
- Mechanism demonstrated with **5 PoCs / 39 falsifiable gates / 76 tests / Codex pair-review 5/5 green-light**
- **Gating structural mutations online with Z3** = embedding SMT into the selection pressure of evolutionary search — found to be unexplored prior art (prior survey across 14 RAD domains + confirmation by Agents A–D)
- Submission candidates: TMLR (primary) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

## Why we built it

Freezing LLM weights is the norm, but the **core computation algorithm itself stays fixed by hand design**. Architecture/algorithm search such as AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge has advanced, yet:

1. **Infeasible compute for individuals** (TinyLlama 1.1B from scratch = $140k / 90 days / 16×A100)
2. **No safety guarantee during search** = wasting time generating numerically unstable architectures
3. **Verified search is disconnected from static verification (Reluplex/Marabou/α,β-CROWN)** — research on an SMT online gate inside the evolution loop was not found

## Confirmed original axes (no negation work in the prior survey)

Mechanism-proven (4 axes):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **State update rule turned into a gene, RWKV-style** (Stage 0a v2)
3. **factor_hook (cognitive state → SSM Δ)** (Stage 2a mock)
4. **In-house evolver + verifier foundation** (Stage 0c + 1a)

Post phase: persona-indexed specialist / Marabou refinement / proposal of a new VNN-COMP category.

## PoC ladder (5 stages / all 39 gates PASS)

| PoC | Content | Key numbers |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | in-house minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

## What we learned from the v1 failure (honest disclosure)

PoC 0a v1 used `decay*s + mix*x*tanh(gate_str*s)`, which made **state=0 a fixed point — a zero attractor**: it passed G1–G5 formally but transmitted zero information. The design flaw that Claude overlooked on its own was caught by the **independent verdicts of Codex (gpt-5.4) and gem-critic**, leading to a v2 redesign in RWKV-style.

→ **In 4 of the 5 PoCs, Codex pair-review caught design flaws that Claude missed on its own.** A concrete case where mutual review worked to prevent structural breakdown.

## Next options

a. Stage 3 kernel diversification (turn rwkv/mamba/hopfield/linear-attn into genes)  
b. Stage 4 turn learning rules (FF/EP/PCN/Hebb) into genes  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. Speed up the Z3 gate with PrediPrune+Quokka  
e. 3.5–5x wall-clock speedup with FlashEvolve  
f. Write it up as a paper (TMLR + GECCO 2027)

## Honest caveats

- Mostly mock; connecting to real LLMs/weights waits for a GPU/new PC
- The 1-step scalar invariant is at the over-approx proof stage; multi-dimensional and multi-step are in the post phase
- The tanh upper-bound approximation is conservative (sound but not complete)

---

**Tags**: evolutionary computation / formal verification / Z3 / RWKV / state space model / CPU research  
**Related**: Series #14-31 (llive lldarwin v0.B-E + observation + governance + lleval)  
**Project**: D:/projects/llcore (PyPI llmesh-llcore 0.1.0a0)

---

# 中文

# (连载 #32) llcore CPU PoC battery 完成

## TL;DR

- 将 **Transformer 的核心计算 (state update / 学习规则 / 认知驱动 Δ)** 作为进化对象的研究框架 `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 独立路线) 的 **CPU PoC battery 完成**
- 以 **5 个 PoC / 39 个可证伪 gate / 76 个测试 / Codex pair-review 5/5 Green-light** 完成机制验证
- **用 Z3 对结构变异进行 online gate** = 把 SMT 嵌入进化搜索的 selection pressure，经事先调查发现为未被探索的先行研究 (事前调查 RAD 14 个领域 + Agent A-D 确认)
- 投稿候选: TMLR (本命) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

## 为什么要做

冻结 LLM 权重是标准做法，但**核心计算算法本身仍固定为人工设计**。AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge 等 architecture/algorithm 搜索虽已推进，但:

1. **个人 compute 无法承担计算资源** (TinyLlama 1.1B from scratch = $140k / 90 天 / 16×A100)
2. **搜索过程中没有安全性保证** = 生成数值不稳定的 architecture 而浪费时间
3. **带验证的搜索与静态 verification (Reluplex/Marabou/α,β-CROWN) 相互割裂** — 在进化循环内做 SMT online gate 的研究未被发现

## 已确定的独有轴 (事前调查中没有 negation work)

机制已验证 (4 个轴):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **将 state update 规则基因化 RWKV-style** (Stage 0a v2)
3. **factor_hook (认知状态 → SSM Δ)** (Stage 2a mock)
4. **自研进化器 + verifier 基础** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / 提出 VNN-COMP 新类别。

## PoC 阶梯 (5 stage / 39 gate 全部 PASS)

| PoC | 内容 | 关键数值 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 自研 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

## 从 v1 的失败中学到的东西 (honest disclosure)

PoC 0a v1 用 `decay*s + mix*x*tanh(gate_str*s)`，使得 **state=0 成为 fixed point 的 zero attractor** = 形式上通过 G1-G5，但信息传递为零。Claude 单独遗漏的设计问题被 **Codex (gpt-5.4) 与 gem-critic 的独立 verdict** 检测出来，从而在 RWKV-style 上做了 v2 redesign。

→ **在 5 个 PoC 中有 4 件，Claude 单独遗漏的设计问题被 Codex pair-review 检测出来**。这是相互评审在防止结构崩溃上发挥作用的实例。

## 下一步选项

a. Stage 3 kernel 多样化 (将 rwkv/mamba/hopfield/linear-attn 基因化)  
b. Stage 4 将学习规则 (FF/EP/PCN/Hebb) 基因化  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. 用 PrediPrune+Quokka 给 Z3 gate 提速  
e. 用 FlashEvolve 实现 3.5-5x wall-clock 提速  
f. 写成论文 (TMLR + GECCO 2027)

## Honest 保留

- 以 mock 为主，连接真实 LLM/权重要等 GPU/新 PC
- 1 step scalar invariant 处于 over-approx proof 阶段，多维、多 step 在 post phase
- tanh 上界近似偏保守 (sound 但不完整)

---

**Tags**: 进化计算 / 形式验证 / Z3 / RWKV / state space model / CPU研究  
**相关**: 连载 #14-31 (llive lldarwin v0.B-E + 观测+governance + lleval)  
**Project**: D:/projects/llcore (PyPI llmesh-llcore 0.1.0a0)

---

# 한국어

# (연재 #32) llcore CPU PoC battery 완성

## TL;DR

- **Transformer의 코어 계산 (state update / 학습 규칙 / 인지 구동 Δ)** 을 진화 대상으로 삼는 연구 프레임워크 `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 독립 노선) 의 **CPU PoC battery 완성**
- **5개 PoC / 39개 falsifiable gate / 76개 테스트 / Codex pair-review 5/5 Green-light** 로 메커니즘 실증
- **Z3로 구조 변이를 online gate** = 진화 탐색의 selection pressure에 SMT를 끼워 넣음 — 사전 조사에서 발견되지 않은 선행 연구 (사전 조사 RAD 14개 분야 + Agent A-D 확인)
- 투고 후보: TMLR (본명) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

## 왜 만들었나

LLM 가중치를 동결하는 것이 표준이지만, **코어 계산 알고리즘 자체는 수작업 설계로 고정**되어 있다. AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge 같은 architecture/algorithm 탐색은 진전되었지만:

1. **개인 compute로는 계산 리소스가 불가능** (TinyLlama 1.1B from scratch = $140k / 90일 / 16×A100)
2. **탐색 중 안전성 보장 없음** = 수치적으로 불안정한 architecture를 만들어 시간 낭비
3. **검증을 동반한 탐색은 정적 verification (Reluplex/Marabou/α,β-CROWN) 과 단절** — 진화 루프 내 SMT online gate 연구는 발견되지 않음

## 확정 독자 축 (사전 조사에서 negation work 없음)

메커니즘 실증 완료 (4개 축):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **state update 규칙을 유전자화 RWKV-style** (Stage 0a v2)
3. **factor_hook (인지 상태 → SSM Δ)** (Stage 2a mock)
4. **자체 진화기 + verifier 기반** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / VNN-COMP 신규 카테고리 제안.

## PoC 사다리 (5 stage / 39 gate 전부 PASS)

| PoC | 내용 | 키 수치 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 자체 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

## v1의 실패에서 배운 것 (honest disclosure)

PoC 0a v1은 `decay*s + mix*x*tanh(gate_str*s)` 로 **state=0이 fixed point인 zero attractor** = G1-G5 형식적으로는 PASS이지만 정보 전달이 제로. Claude 단독으로 놓친 설계 문제를 **Codex (gpt-5.4) 와 gem-critic의 독립 verdict** 가 검출하여 RWKV-style로 v2 redesign 했다.

→ **5개 PoC 중 4건에서 Claude 단독으로는 놓친 설계 문제를 Codex pair-review가 검출**. 상호 리뷰가 구조 붕괴 방지에 작동한 실례.

## 다음 선택지

a. Stage 3 kernel 다양화 (rwkv/mamba/hopfield/linear-attn 을 유전자화)  
b. Stage 4 학습 규칙 (FF/EP/PCN/Hebb) 을 gene화  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. PrediPrune+Quokka로 Z3 gate 고속화  
e. FlashEvolve로 3.5-5x wall-clock 고속화  
f. 논문화 (TMLR + GECCO 2027)

## Honest 유보

- mock 중심, 실제 LLM/가중치 접속은 GPU/새 PC 대기
- 1 step scalar invariant의 over-approx proof 단계, 다차원·다 step은 post phase
- tanh 상계 근사는 보수적 (sound이지만 완전하지 않음)

---

**Tags**: 진화 계산 / 형식 검증 / Z3 / RWKV / state space model / CPU연구  
**관련**: 연재 #14-31 (llive lldarwin v0.B-E + 관측+governance + lleval)  
**Project**: D:/projects/llcore (PyPI llmesh-llcore 0.1.0a0)

<!-- NAV -->
---
**FullSense KB ナビ**: [← #31 AI に AI を部下として使わせる #31 —](https://fullsense.qiita.com/furuse-kazufumi/items/71c2304718ad5829d2d7) ・ [📑 目次](https://fullsense.qiita.com/furuse-kazufumi/items/1ad8db4b854194e2d215) ・ [#33 llcore — 「進化で AI を設計するとき →](https://fullsense.qiita.com/furuse-kazufumi/items/21d6c4dcfde204062a89)
<!-- /NAV -->


<!-- REFERRAL -->

---

> ### ⚡ この連載は Claude Code と二人三脚で書いています
>
> 記事中の実装・検証・可視化は **Claude Code**(Anthropic の AI コーディング環境)と一緒に進めています。
> Claude Code は **1 週間の無料トライアル**で試せます。気に入って有料プランに登録される際、
> 下の紹介リンク経由だと筆者に「開発を続けるためのクレジット」が入り、この連載の継続を後押しできます。
>
> 👉 **無料で試す / 紹介リンク** → https://claude.ai/referral/0sqPw8E_lw
>
> <sub>EN: This series is built together with **Claude Code** — try it with a **1-week free trial**. If you subscribe via the link, the author receives credits to keep building. /
> 中文: 本系列与 **Claude Code** 协作完成,可享 **1 周免费试用**;通过链接注册可让作者获得继续开发的额度。 /
> 한국어: 이 시리즈는 **Claude Code**와 함께 작성합니다 — **1주 무료 체험** 제공. 링크로 가입하면 저자가 개발 지속용 크레딧을 받습니다.</sub>

<!-- /REFERRAL -->

<!-- CTAIMG -->

![「ひくわ」と一万円札を差し出す森田](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/bazue_all/012.jpg)
> 🗒️ *「ひくわ」— 紹介リンクで小銭を稼ごうとする魂胆、我ながらちょっと引く*（© Forbidden shibukawa / SHUEISHA・『スナックバス江』）

<!-- /CTAIMG -->
