---
title: "推論する AI から「予測する認知 OS」へ — FullSense 開発 1 週間ダイジェスト (2026-05-17 → 05-24)"
tags: LLM,Agent,OnPrem,認知科学,Python
ignorePublish: true
---

> **言語 / Language / 语言 / 언어**: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)
>
> この記事は 2026-05-17 に公開した 11 本の開発記事を出発点に、そこから 1 週間
> (〜2026-05-24) で FullSense が **どこまで進んだか**を統合したダイジェストです。
> 各言語版は完全自己完結 (そのままコピーして共有できます)。

---

# 日本語

## はじめに — 7 日間で「推論する AI」が「予測する認知 OS」に脱皮した

著者: **古瀬 和文（ぷるやん）**

2026-05-17、私は 1 セッションで自己進化型 LLM フレームワーク
[llive](https://github.com/furuse-kazufumi/llive) に要件 32 件・実装 2,200 行・
テスト +78 件 (計 1,014 PASS) を足し、Brief API・10 思考因子・数学エンジン・
ベンチ 4 種を一気に着地させました。

それから **7 日**。FullSense (llmesh / llive / llove の傘ブランド) は、単に機能が
増えただけではなく、**設計アイデンティティが 1 段変わりました**。本稿はその
「変化の中身」を、出発点の 3 本柱と接続しながら振り返ります。

## 出発点 — 2026-05-17 のスナップショット

| 柱 | 中身 | 当時の状態 |
|---|---|---|
| Brief API | 外部クライアントが「構造化 work unit」を 6 stage loop に流す薄い接着剤 | overhead < 1 % を 15 セルベンチで実測 |
| COG-FX 10 思考因子 | 「心理の深層」由来の 10 因子を llive 思考層へマッピング | 土台 5 因子を既に実装済 (9/10) |
| MATH エンジン | LLM に計算させず決定論サイドカーで止める (AST + SI 次元解析) | `5 m/s + 3 s` を必ず弾く |
| bench honesty | 当初版が不公平 → 異常 3 件を明示して fair 再走 | honest disclosure の型を確立 |

この時点の llive は「**frozen な LLM コアの周りに被せる認知 OS**」という positioning でした。

## この 1 週間の前進

| 領域 | 進展 (2026-05-17 → 05-24) |
|---|---|
| 進化スタック | v0.B〜v0.F (派生集団進化 / genome 2 階層 / メタ認知進化) を大規模前倒し |
| 高速化 | Rust 拡張 (RUST-15/16/17b) でホットパスを加速 (用途次第で効く所のみ、と honest に) |
| マルチモーダル | C-1.3 で audio + sensor の skeleton を追加 |
| 表現層 | RepIR を **llrepr** に改名 (頭字語衝突回避)、"LLVM-for-expression" として typed IR を MCP 上に |
| 予測 push | llmesh `predictive_push` — SPC warning-zone で説明を投機生成、確定時は typed diff (予測誤差) だけ push |
| 非 Transformer | RWKV backend skeleton (SSM 系第一弾) |

## 統合発見 — FullSense 全体を「予測符号化アーキテクチャ」として再構成できる

この 1 週間で最も大きかったのは個別機能ではなく、**それらを貫く 1 本の原理**に
気づいたことです。神経科学の予測符号化 (Friston) — 脳は予測を先に立て、
**予測誤差だけを伝播**する — が FullSense の複数レイヤーに同型で現れていました:

- **リアルタイム**: SPC が warning-zone に入った時点で説明を先回り生成し、確定時は
  差分だけ push → 体感「負のレイテンシ」
- **表現**: push は full document でなく typed diff (= 予測誤差)
- **評価**: 評価 = 生成 (予測) と rubric (観測) の誤差。誤差箇所だけ批評・再生成

「LLM の周りに被せる認知 OS」という positioning に、神経科学的な裏付けが付いた、
というのがこの週の中核です。

## 今日 (05-24) 着地した 2 つ — Gemini 発ブレストの実装

予測符号化と親和する 2 アイデアをこの日コードに落としました。

### 1. Antifragile Mutation (llive, commit `f2c2d1e`)

Nassim Taleb の反脆弱性を進化計算へ。高 surprise を「守り (fail-closed)」でなく
「学習機会」と捉え、**panic mode** で探索を一時増幅します:

- BayesianSurpriseGate の動的閾値超過 → panic 遷移
- panic 中のみ UCB1 exploration constant を **10x**、相反する TRIZ 原理 pair を unlock、
  全 ChangeOp を SHA-256 hash chain (AuditTrail) に署名記録
- **fail-closed default は崩さない** — opt-in / `LLIVE_ANTIFRAGILE_AUTO=true` でのみ有効
- cooldown (既定 5 分) と surprise 回復 hysteresis で panic 滞在に上限
- 28 テスト PASS / ruff + mypy strict green

### 2. Speculative Mesh Execution (llmesh, commit `2a05f64`)

CPU の分岐予測を **agent level** へ。メイン推論中に予測した分岐を idle peer へ
**Ed25519 署名付き**で投機投入し、到達時に mesh から回収します:

- LAN-first の idle node 選択 (負荷スコア + VRAM hard filter)
- 受信結果は **Ed25519 検証を fail-closed** で実施 (改ざん / 誤配を拒否)
- pull で hit / miss、未使用投機は waste として計上
- 23 テスト PASS / ruff + mypy strict green

## honest disclosure — まだ証明していないこと

- **Antifragile**: 「自己破壊で次の安定へ」が本当に効くかは未検証。panic の成功率 /
  損失率を時系列で追う計測基盤を入れただけ。勝った気になる前に内訳を疑う。
- **Speculative Mesh**: 得をするのは「hit rate が高く、かつ mesh 往復 < ローカル swap」
  のときだけ。WAN は負ける前提で別カウント。実 transport / executor は未配線の PoC。
- **進化スタック**: 駆動側 (driver) の genome 整合に既知の課題が残る。

## まとめ

7 日間で FullSense は「機能が増えた」だけでなく、**予測符号化という 1 本の背骨**を
得ました。出発点の 3 本柱 (Brief API / 10 因子 / 数学) は、いまや「予測を先に立て、
誤差だけを流す」という統一原理の上に並びます。次は配線 (実 transport / explainer) と、
効果の正直な定量化です。

- llive: <https://github.com/furuse-kazufumi/llive>
- llmesh: <https://github.com/furuse-kazufumi/llmesh>

---

# English

## Intro — In 7 days, an "AI that reasons" molted into a "cognitive OS that predicts"

Author: **Kazufumi Furuse (puruyan)**

On 2026-05-17 I spent a single session adding 32 requirements, ~2,200 lines, and
+78 tests (1,014 PASS total) to the self-evolving LLM framework
[llive](https://github.com/furuse-kazufumi/llive), landing the Brief API, the
10 cognitive factors, a math engine, and four benchmarks at once.

**Seven days later**, FullSense (the umbrella brand over llmesh / llive / llove)
didn't just grow features — its **design identity shifted a level**. This digest
revisits that shift, connecting it back to the three original pillars.

## Starting point — the 2026-05-17 snapshot

| Pillar | What it is | State then |
|---|---|---|
| Brief API | Thin glue that feeds a structured work unit into the 6-stage loop | < 1 % overhead measured on a 15-cell bench |
| COG-FX 10 factors | Ten cognitive factors mapped onto llive's thinking layer | 5 foundational factors already implemented (9/10) |
| MATH engine | Don't let the LLM compute; stop it with a deterministic sidecar (AST + SI dimensional analysis) | Always rejects `5 m/s + 3 s` |
| Bench honesty | First version unfair → 3 anomalies disclosed, fair rerun | Established an honest-disclosure pattern |

Back then llive was positioned as "**a cognitive OS wrapped around a frozen LLM core**".

## What moved this week

| Area | Progress (2026-05-17 → 05-24) |
|---|---|
| Evolutionary stack | v0.B–v0.F (derivative-population evolution / two-layer genome / meta-cognition) brought forward at scale |
| Acceleration | Rust extensions (RUST-15/16/17b) speeding up hot paths (honestly: only where it actually helps) |
| Multimodal | C-1.3 adds an audio + sensor skeleton |
| Expression layer | RepIR renamed to **llrepr** (acronym-collision avoidance); a typed "LLVM-for-expression" IR over MCP |
| Predictive push | llmesh `predictive_push` — speculatively generate an explanation in the SPC warning zone, then push only the typed diff (prediction error) on confirmation |
| Non-Transformer | RWKV backend skeleton (first SSM-family backend) |

## The unifying discovery — FullSense as a "predictive-coding architecture"

The biggest thing this week wasn't any single feature; it was noticing **one
principle that runs through all of them**. Neuroscience's predictive coding
(Friston) — the brain forms a prediction first and propagates only the
**prediction error** — appears isomorphically across FullSense layers:

- **Real time**: generate the explanation ahead of time when SPC enters the
  warning zone, then push only the diff on confirmation → felt "negative latency".
- **Expression**: push a typed diff (= prediction error), not the full document.
- **Evaluation**: evaluation = the error between generation (prediction) and
  rubric (observation); only critique/regenerate where the error is.

The core of the week: the "cognitive OS around the LLM" positioning gained a
neuroscientific backing.

## Two things landed today (05-24) — implementing Gemini-sparked ideas

Both ideas resonate with predictive coding and were turned into code today.

### 1. Antifragile Mutation (llive, commit `f2c2d1e`)

Taleb's antifragility, brought to evolutionary computation. High surprise becomes
a **learning opportunity** rather than a defensive fail-closed, via a **panic mode**:

- Exceeding the BayesianSurpriseGate dynamic threshold → transition to panic.
- Only in panic: amplify the UCB1 exploration constant **10×**, unlock opposing
  TRIZ-principle pairs, and sign every ChangeOp into a SHA-256 hash chain (AuditTrail).
- **The fail-closed default is preserved** — opt-in / enabled only via
  `LLIVE_ANTIFRAGILE_AUTO=true`.
- A cooldown (default 5 min) and surprise-recovery hysteresis cap the panic dwell time.
- 28 tests PASS / ruff + mypy strict green.

### 2. Speculative Mesh Execution (llmesh, commit `2a05f64`)

CPU branch prediction lifted to the **agent level**. While the main inference runs,
predicted branches are dispatched to idle peers **Ed25519-signed** for speculative
execution, then pulled from the mesh on arrival:

- LAN-first idle-node selection (load score + VRAM hard filter).
- Incoming results are **Ed25519-verified, fail-closed** (tamper / misroute rejected).
- pull yields hit / miss; unused speculation is counted as waste.
- 23 tests PASS / ruff + mypy strict green.

## Honest disclosure — what is not yet proven

- **Antifragile**: whether "self-destruct toward the next stability" actually works
  is unverified. I only added the instrumentation to track panic success/loss rates
  over time. Suspect the breakdown before declaring a win.
- **Speculative Mesh**: it only pays off when the hit rate is high *and* a mesh
  round-trip beats local swap. WAN is expected to lose and is counted separately.
  Real transport / executor are unwired (PoC).
- **Evolutionary stack**: a known genome-consistency issue remains on the driver side.

## Wrap-up

In seven days FullSense didn't just "gain features" — it gained a **single spine:
predictive coding**. The three original pillars (Brief API / 10 factors / math) now
sit on one unifying principle: form a prediction first, propagate only the error.
Next: wiring (real transport / explainer) and an honest quantification of the effect.

- llive: <https://github.com/furuse-kazufumi/llive>
- llmesh: <https://github.com/furuse-kazufumi/llmesh>

---

# 中文

## 引言 — 7 天里，“会推理的 AI”蜕变为“会预测的认知 OS”

作者：**古濑和文（puruyan）**

2026-05-17，我用一个会话给自进化 LLM 框架
[llive](https://github.com/furuse-kazufumi/llive) 添加了 32 条需求、约 2,200 行实现、
+78 个测试（共 1,014 通过），一次性落地了 Brief API、10 个思维因子、数学引擎与四种基准。

**七天之后**，FullSense（llmesh / llive / llove 的总品牌）不只是功能变多了——它的
**设计身份提升了一个层级**。本文回顾这一转变，并把它与最初的三大支柱相连接。

## 起点 — 2026-05-17 的快照

| 支柱 | 内容 | 当时状态 |
|---|---|---|
| Brief API | 把结构化工作单元送入 6 阶段循环的薄胶水层 | 15 单元基准实测开销 < 1 % |
| COG-FX 10 因子 | 将 10 个思维因子映射到 llive 思考层 | 5 个基础因子已实现（9/10） |
| 数学引擎 | 不让 LLM 计算，用确定性旁路拦截（AST + SI 量纲分析） | 必然拦下 `5 m/s + 3 s` |
| 基准诚实性 | 初版不公平 → 明示 3 处异常并公平重跑 | 确立了诚实披露的范式 |

那时 llive 的定位是“**包裹在冻结 LLM 内核之外的认知 OS**”。

## 本周的进展

| 领域 | 进展（2026-05-17 → 05-24） |
|---|---|
| 进化栈 | v0.B–v0.F（派生种群进化 / 双层基因组 / 元认知进化）大规模提前 |
| 加速 | Rust 扩展（RUST-15/16/17b）加速热点路径（诚实地说：只在真正有效处） |
| 多模态 | C-1.3 增加 audio + sensor 骨架 |
| 表达层 | RepIR 改名为 **llrepr**（规避缩写冲突）；MCP 之上的类型化“表达式 LLVM” IR |
| 预测推送 | llmesh `predictive_push`——在 SPC 警戒区投机生成解释，确认时只推送类型化 diff（预测误差） |
| 非 Transformer | RWKV 后端骨架（SSM 系第一个） |

## 统合发现 — 可将整个 FullSense 重构为“预测编码架构”

本周最大的收获不是某个功能，而是注意到**贯穿它们的同一条原理**。神经科学的预测编码
（Friston）——大脑先形成预测，只传播**预测误差**——在 FullSense 各层同构出现：

- **实时**：SPC 进入警戒区时提前生成解释，确认时只推送差分 → 体感“负延迟”。
- **表达**：推送类型化 diff（= 预测误差），而非完整文档。
- **评估**：评估 = 生成（预测）与 rubric（观测）之间的误差；只在误差处批评 / 重生成。

本周的核心：“包裹 LLM 的认知 OS”这一定位获得了神经科学依据。

## 今天（05-24）落地的两件事 — 实现来自 Gemini 的头脑风暴

两个与预测编码契合的想法今天都落成了代码。

### 1. 反脆弱变异（llive，commit `f2c2d1e`）

把 Taleb 的反脆弱性带入进化计算。高 surprise 不再触发防御性的 fail-closed，而是
作为**学习机会**进入 **panic 模式**：

- 超过 BayesianSurpriseGate 的动态阈值 → 进入 panic。
- 仅在 panic 期间：将 UCB1 探索常数放大 **10 倍**，解锁对立的 TRIZ 原理对，并把每个
  ChangeOp 签名写入 SHA-256 哈希链（AuditTrail）。
- **保持 fail-closed 默认** —— 仅通过 opt-in / `LLIVE_ANTIFRAGILE_AUTO=true` 启用。
- 冷却（默认 5 分钟）与 surprise 恢复滞回为 panic 停留设上限。
- 28 个测试通过 / ruff + mypy strict 通过。

### 2. 思维网格投机执行（llmesh，commit `2a05f64`）

把 CPU 分支预测提升到 **agent 层级**。主推理进行时，把预测分支以 **Ed25519 签名**
派发给空闲节点投机执行，到达时从网格回收：

- LAN 优先的空闲节点选择（负载分数 + VRAM 硬过滤）。
- 收到的结果以 **Ed25519 验证、fail-closed** 处理（拒绝篡改 / 误投）。
- pull 产生 hit / miss；未使用的投机计为浪费。
- 23 个测试通过 / ruff + mypy strict 通过。

## 诚实披露 — 尚未证明的部分

- **反脆弱**：“自毁以跳向下一个稳定”是否真有效尚未验证。我只是加入了追踪 panic
  成功 / 损失率的度量基础。宣称胜利前先怀疑内部明细。
- **思维网格**：只有当命中率高 *且* 网格往返快于本地 swap 时才划算。WAN 预期会输，
  单独计数。实际 transport / executor 尚未接线（PoC）。
- **进化栈**：驱动侧的基因组一致性仍有已知问题。

## 小结

七天里 FullSense 不只是“功能变多”，而是获得了**一条脊梁：预测编码**。最初的三大支柱
（Brief API / 10 因子 / 数学）如今都立于同一原理之上：先做预测，只传播误差。下一步是
接线（实际 transport / explainer）与对效果的诚实量化。

- llive: <https://github.com/furuse-kazufumi/llive>
- llmesh: <https://github.com/furuse-kazufumi/llmesh>

---

# 한국어

## 들어가며 — 7일 만에 "추론하는 AI"가 "예측하는 인지 OS"로 탈피했다

저자: **후루세 가즈후미 (puruyan)**

2026-05-17, 나는 한 세션 동안 자기진화형 LLM 프레임워크
[llive](https://github.com/furuse-kazufumi/llive)에 요건 32건·구현 약 2,200줄·
테스트 +78건(총 1,014 통과)을 더하며 Brief API·10가지 사고 인자·수학 엔진·
4종 벤치마크를 한 번에 안착시켰다.

**7일 후**, FullSense(llmesh / llive / llove의 우산 브랜드)는 단지 기능이 늘어난 것이
아니라 **설계 정체성이 한 단계 바뀌었다**. 이 글은 그 변화를, 출발점의 세 기둥과
연결하며 돌아본다.

## 출발점 — 2026-05-17 스냅샷

| 기둥 | 내용 | 당시 상태 |
|---|---|---|
| Brief API | 구조화된 작업 단위를 6단계 루프에 흘리는 얇은 접착제 | 15셀 벤치에서 오버헤드 < 1 % 실측 |
| COG-FX 10 인자 | 10가지 사고 인자를 llive 사고층에 매핑 | 토대 5인자 이미 구현(9/10) |
| 수학 엔진 | LLM에 계산시키지 않고 결정론적 사이드카로 차단(AST + SI 차원해석) | `5 m/s + 3 s`를 반드시 차단 |
| 벤치 정직성 | 초기판 불공정 → 이상 3건 명시 후 공정 재실행 | 정직한 공개(honest disclosure) 패턴 확립 |

그때 llive의 포지셔닝은 "**얼어붙은 LLM 코어를 감싸는 인지 OS**"였다.

## 이번 주의 전진

| 영역 | 진전(2026-05-17 → 05-24) |
|---|---|
| 진화 스택 | v0.B–v0.F(파생 집단 진화 / 2계층 게놈 / 메타인지 진화)를 대규모로 앞당김 |
| 가속 | Rust 확장(RUST-15/16/17b)으로 핫패스 가속(정직히: 실제로 효과 있는 곳만) |
| 멀티모달 | C-1.3에서 audio + sensor 스켈레톤 추가 |
| 표현층 | RepIR을 **llrepr**로 개명(약어 충돌 회피); MCP 위의 타입드 "표현식용 LLVM" IR |
| 예측 push | llmesh `predictive_push` — SPC 경고 구간에서 설명을 투기 생성, 확정 시 타입드 diff(예측 오차)만 push |
| 비-Transformer | RWKV 백엔드 스켈레톤(SSM 계열 첫 번째) |

## 통합 발견 — FullSense 전체를 "예측 부호화 아키텍처"로 재구성할 수 있다

이번 주 가장 큰 수확은 개별 기능이 아니라 **그것들을 관통하는 하나의 원리**를
알아챈 것이다. 신경과학의 예측 부호화(Friston) — 뇌는 먼저 예측을 세우고 **예측
오차만 전파**한다 — 가 FullSense 여러 층에 동형으로 나타났다:

- **실시간**: SPC가 경고 구간에 들어서면 설명을 미리 생성하고, 확정 시 차분만 push
  → 체감 "음의 지연".
- **표현**: 완전한 문서가 아니라 타입드 diff(= 예측 오차)를 push.
- **평가**: 평가 = 생성(예측)과 rubric(관측) 사이의 오차; 오차가 있는 곳만 비평/재생성.

이번 주의 핵심: "LLM을 감싸는 인지 OS"라는 포지셔닝이 신경과학적 근거를 얻었다.

## 오늘(05-24) 안착시킨 두 가지 — Gemini 발 브레인스토밍 구현

예측 부호화와 잘 맞는 두 아이디어를 이날 코드로 옮겼다.

### 1. Antifragile Mutation (llive, commit `f2c2d1e`)

Taleb의 반취약성을 진화 계산에. 높은 surprise를 방어적 fail-closed가 아니라
**학습 기회**로 보고 **panic 모드**로 진입한다:

- BayesianSurpriseGate의 동적 임계 초과 → panic 전이.
- panic 동안만: UCB1 탐색 상수를 **10배**, 상반되는 TRIZ 원리 쌍을 unlock, 모든
  ChangeOp를 SHA-256 해시 체인(AuditTrail)에 서명 기록.
- **fail-closed 기본값은 유지** — opt-in / `LLIVE_ANTIFRAGILE_AUTO=true`로만 활성화.
- 쿨다운(기본 5분)과 surprise 회복 히스테리시스로 panic 체류에 상한.
- 28개 테스트 통과 / ruff + mypy strict 통과.

### 2. Speculative Mesh Execution (llmesh, commit `2a05f64`)

CPU 분기 예측을 **agent 레벨**로. 메인 추론 중에 예측 분기를 유휴 피어에게
**Ed25519 서명**과 함께 투기 투입하고, 도달 시 메시에서 회수한다:

- LAN 우선 유휴 노드 선택(부하 점수 + VRAM 하드 필터).
- 수신 결과는 **Ed25519 검증, fail-closed**로 처리(변조 / 오배송 거부).
- pull은 hit / miss를 내고, 사용되지 않은 투기는 낭비로 집계.
- 23개 테스트 통과 / ruff + mypy strict 통과.

## 정직한 공개 — 아직 증명하지 못한 것

- **Antifragile**: "자기 파괴로 다음 안정으로"가 정말 효과적인지는 미검증. panic의
  성공/손실률을 시계열로 추적하는 계측 기반만 넣었다. 승리를 선언하기 전에 내역을 의심하라.
- **Speculative Mesh**: 적중률이 높고 *또한* 메시 왕복이 로컬 swap보다 빠를 때만 이득.
  WAN은 질 것으로 보고 따로 집계. 실제 transport / executor는 미배선(PoC).
- **진화 스택**: 드라이버 측 게놈 일관성에 알려진 과제가 남아 있다.

## 마무리

7일 동안 FullSense는 단지 "기능이 늘어난" 것이 아니라 **하나의 척추 — 예측 부호화**를
얻었다. 출발점의 세 기둥(Brief API / 10 인자 / 수학)은 이제 하나의 원리 위에 선다:
먼저 예측하고, 오차만 전파한다. 다음은 배선(실제 transport / explainer)과 효과의
정직한 정량화다.

- llive: <https://github.com/furuse-kazufumi/llive>
- llmesh: <https://github.com/furuse-kazufumi/llmesh>
