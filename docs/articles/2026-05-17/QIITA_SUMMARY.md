---
title: "1 日で要件 32 件追加 + Brief API + COG-FX + MATH 実装 + ベンチ 4 種 — 自己進化型 LLM フレームワーク llive 開発記 2026-05-17"
tags: LLM,Agent,OnPrem,Ollama,Python,認知科学,TRIZ
id: bfa83d01e79028132438
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 1 日で要件 32 件追加 + Brief API + COG-FX + MATH 実装 + ベンチ 4 種 — 自己進化型 LLM フレームワーク llive 開発記 2026-05-17

著者: **古瀬 和文（ぷるやん）**

## はじめに — 1 セッションで何を達成したか

2026-05-17 の 1 セッション (Claude Opus 4.7 1M context, ccr 経由) で **自己進化型 LLM フレームワーク [llive](https://github.com/furuse-kazufumi/llive)** に対し以下を達成しました:

| 種別 | 件数 | 内容 |
|---|---|---|
| 要件 (FR) 追加 | **32 件** | v0.7-MATH 8 / v0.8-CABT 7 / v0.9-CREAT 5 / v1.0-COG-FX 4 / v2.0-ORG-FX 8 |
| 実装 (LoC) | ~2 200 行 | Brief API end-to-end / Grounder / Governance / Trace Graph / MATH 単位 & 計算 |
| テスト追加 | **+78 件** | 936 → **1014 PASS / 0 fail / 0 regression** |
| ベンチ 4 種 | 15 + 12 + 10 + 10 セル | progressive matrix / fair bench / quiz Debug / quiz Release |
| 公開記事 | **11 本 + 本記事** | [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17) |
| GitHub push | 2 リポジトリ | llive `349a234` / fullsense `cb346aa` |

llive は **OSS LLM (Qwen / Llama / Mistral) を内蔵する「認知 OS」** という positioning。Decoder-only LLM コアは frozen のまま、4 層メモリ + 6 stage Loop + Approval Bus + TRIZ 40 原理 + 10 思考因子 を統合した研究開発フレームワークです。

本記事は 11 本の個別記事を **本文込み**で統合したもので、Qiita 単独でも通読可能なように書きました。各章末に詳細リンクも置いています。

---

## 1. Brief API end-to-end (LLIVE-001/002 全 7 step)

### 動機

これまで llive の `FullSenseLoop.process(Stimulus)` は **thinking-evaluator** であって **doing-agent** ではありませんでした。外部クライアント (lldesign / lltrade / 計画中の llcad/lleda/llchip) が「構造化された work unit」を渡す API がなかったためです。

設計ドラフト `docs/proposals/brief_api_design.md` (5 日見積) を 1 セッションで完走させました。

### Brief dataclass

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str                           # ascii word/dash/dot のみ、path-safe
    goal: str                               # 必須
    constraints: tuple[str, ...] = ()
    source: str = "manual"
    priority: float = 0.5                   # [0.0, 1.0]
    epistemic_type: EpistemicType = EpistemicType.PRAGMATIC
    backend: str = ""                       # "ollama:qwen2.5:14b" 等
    tools: tuple[str, ...] = ()             # whitelist
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    ledger_path: Path | None = None
```

**frozen + tuple** で hashable / replay-friendly。同じ Brief を ledger・loop・result が共有する invariant を frozen で守ります。

### BriefRunner — submit 1 トランザクションで以下を実行

```
1. brief_submitted          → ledger
2. (optional) grounding_applied (TRIZ × RAD citation)
3. stimulus_built           → ledger
4. FullSenseLoop.process(stim)
   └─ 6 stage loop (既存)
5. loop_completed           → ledger
6. decision                 → ledger
7. (optional) governance_scored (COG-02, 4 軸)
8. Approval Bus gate (PROPOSE/INTERVENE 時のみ)
9. tool_invoked × N         → ledger
10. outcome                 → ledger
```

すべて **append-only JSONL ledger** に記録。`meta` envelope に timestamp/pid を分離し、replay 時に ignore できる構造。

### CLI

```bash
# YAML から
llive brief submit path/to/brief.yaml

# インライン
llive brief submit --goal "Refactor docs/index.md..." \
                   --brief-id portal-refresh \
                   --priority 0.8 --no-approval

# ledger 検索
llive brief ledger portal-refresh-2026-05-16 --json --limit 5
```

### MCP

`submit_brief` tool が追加され、Claude Desktop / Cursor 等から llive にタスクを渡せます:

```jsonc
{
  "name": "submit_brief",
  "input_schema": {
    "type": "object",
    "required": ["goal"],
    "properties": {
      "goal": {"type": "string"},
      "constraints": {"type": "array", "items": {"type": "string"}},
      "priority": {"type": "number", "minimum": 0.0, "maximum": 1.0},
      "approval_required": {"type": "boolean", "default": true}
    }
  }
}
```

### Progressive validation matrix (5×3 = 15 セル)

xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b} を on-prem only で実走 (cloud は混在禁止、`feedback_llive_measurement_purity` ルール):

#### Wall-time matrix (ms)

| model | xs (cold) | s | m | l | xl (timeout) |
|---|---|---|---|---|---|
| llama3.2:3b | 8 908 | 43 978 | 89 484 | 458 400 | 1 202 282 ⌛ |
| qwen2.5:7b | 59 447 | 94 158 | 122 134 | 722 867 | 1 202 104 ⌛ |
| qwen2.5:14b | 121 560 | 122 160 | 122 160 | 1 202 263⌛ | 1 202 199 ⌛ |

#### LLM-only / Wall

全 15 セルで **> 99.8 %** — Brief API + loop の追加コストは ~1 % 未満。

#### Loop decision

| model \ size | xs | s | m | l | xl |
|---|---|---|---|---|---|
| llama3.2:3b | note | note | note | note | note |
| qwen2.5:7b | note | note | note | note | note |
| qwen2.5:14b | note | note | note | note | note |

**全 15 セル `note`** — loop の決定木が token 圧力に対し完全 stable。

### 思考層との接続

- `Brief.epistemic_type` で Multi-track Filter の chain を選択
- `Brief.priority` が Stimulus.surprise になり Salience Gate に影響
- `Brief.constraints` は augmented goal として thought に注入
- `Brief.tools` whitelist で BriefRunner の tool 実行を制限
- `Brief.approval_required` で C-1 Approval Bus を経由

詳細: [01_brief_api_progressive.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md)

---

## 2. 心理の深層 10 思考因子で整理する llive 思考層 — 9/10 実装済

### 出典

YouTube チャンネル「心理の深層」から抽出された人間の思考因子セット。ユーザーが目的を「深層心理の説明」ではなく **「再利用可能な思考因子の抽出 → LLM の推論・計画・自己改善・エージェント設計への組み込み」** に明示転換し、要件化しました。

### 10 因子 × llive マッピング

| # | 因子 | LLM 役割 | llive 既存 (実装済) | 追加 (2026-05-17 実装) |
|---|---|---|---|---|
| 1 | **構造化** | 課題を分解 | Brief constraints, Salience+Curiosity gate | — |
| 2 | 再構成 | 代替案生成 | TRIZ 40 原理 + ARIZ + 9 画法 (FR-23〜27) | (CREAT-01 計画) |
| 3 | **閉ループ** | 検証計画を伴う | BriefRunner (submit→plan→approval→tool→outcome) | — |
| 4 | 自己拡張 | 外部資源を使う | 4 層メモリ + RAD 49 分野 + tools whitelist | MATH-08 計算エンジン |
| 5 | **不確実性** | 仮説と事実を分離 | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | 探索 | 未踏案を試す | EVO-* (Z3 + Failed Reservoir + Reverse-Evo) | — |
| 7 | **整合** | 全体制約で再評価 | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | **来歴** | 判断履歴を残す | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | 多視点 | 評価関数を分離 | Multi-track Filter A-1.5 (5 EpistemicType) | (COG-04 + CREAT-04 計画) |
| 10 | 現実接続 | 実環境制約を扱う | (Phase 4 INT-01〜04 計画中) | — |

### v1.0 必須 5 因子 (太字) はすべて実装済

ユーザー観察: **「探索 / 再構成を強化する前に、構造化 / 不確実性 / 閉ループ / 整合 / 来歴の土台が必要」**。これがない状態で探索因子や再構成因子を強くすると、面白い案は増えるが誤差・暴走・非再現性も増えます。

| 因子 | 実装場所 |
|---|---|
| 構造化 | `src/llive/brief/types.py::Brief` + loop._salience_gate/curiosity_drive |
| 閉ループ | `src/llive/brief/runner.py::BriefRunner.submit` |
| 不確実性 | `src/llive/learning/bayesian_surprise.py` (FR-21) + COG-01 |
| 整合 | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py` (EVO-04) + COG-02 |
| 来歴 | `src/llive/memory/provenance.py` + ledger × 3 + COG-03 |

### COG-01〜03 の実装

#### COG-01 Triple Output

`BriefResult` に **confidence / assumptions / missing_evidence** の 3 列を追加:

```python
@dataclass
class BriefResult:
    # 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` が決定論的に算出:

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`: grounder 不在 / success_criteria 不在を明文化
- `missing_evidence`: TRIZ 原理が surface しなかった / tool 失敗を保存

#### COG-02 Governance Scoring Layer

Approval Bus の **前段** に 4 軸スコアラを挿入:

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block
```

責務分離:
- **Governance** = scoring (なぜ良い/悪いか)
- **Approval Bus** = gating (実行可否の判断)

dangerous_token 検出 (`rm -rf` / `DROP TABLE` / `format c:` 等)、INTERVENE-without-approval ペナルティ、`block_threshold` / `safety_floor` をサポート。

#### COG-03 Trace Graph

`BriefLedger.trace_graph()` が 3 層 view を返す:

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

これによりデバッグ・自己改善・失敗分析・evolution への学習データ抽出が機械的に可能になります。

詳細: [02_cognitive_factors.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md)

---

## 3. 数学・単位に強い AI への第一歩 — MATH-01/08

llive の最初の vertical specialisation は「数学・単位特化 AI」。汎用 LLM が苦手な以下を、**「LLM に計算させない」決定論的サイドカー**で克服します。

### LLM の数学的弱点

| 観点 | 汎用 LLM の弱点 | llive 既存資産との合致 |
|---|---|---|
| 記号操作の幻覚 | `x² + x = 2x³` のような誤等式 | EVO-04 Z3 静的検証で gate |
| 単位次元 | `5 m/s + 3 s = 8` | SI 次元解析エンジン (MATH-01) |
| 数値精度 | float 演算誤差を無視 | error propagation tracking (MATH-04) |
| 公理体系 | 暗黙の前提を混入 | EpistemicType=MATHEMATICAL の strict track |
| 引用の信頼性 | "CODATA value is X" と適当に答える | RAD math/metrology + provenance |

### MATH-01 — SI 7 基本単位 + 派生単位の次元代数

```python
from llive.math import Quantity, parse_unit, UnitMismatchError

# 速度 + 時間 = 不可能 (典型的 LLM 幻覚を必ず止める)
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t
assert d.dimensions.matches(parse_unit("m"))

# 力 × 距離 = エネルギー (J)
F = Quantity(10.0, parse_unit("N"))
d = Quantity(5.0, parse_unit("m"))
E = F * d
assert E.dimensions.matches(parse_unit("J"))  # ✓
```

実装の核は `Dimensions(m, kg, s, A, K, mol, cd)` の 7 次元ベクトル。`Quantity.__add__` で次元検算 → 不一致は **必ず raise**。

派生単位: `N` (kg·m/s²) / `J` (kg·m²/s²) / `W` (kg·m²/s³) / `Pa` (kg/m/s²) / `Hz` (1/s) / `C` (s·A) / `V` (kg·m²/s³/A) / `ohm` を頻出範囲のみ実装。

### MATH-08 — 内蔵計算エンジン (差別化軸最大)

**設計の核**: LLM に **数値計算をさせない**。

```python
from llive.math import SafeCalculator, extract_expressions

calc = SafeCalculator()
brief_text = "Compute (2.5 * 7.8) / 0.3 then verify sqrt(16) is exact."

for expr in extract_expressions(brief_text):
    r = calc.evaluate(expr)
    print(f"{r.expression} = {r.value}  (ops={r.operation_count}, fns={r.used_functions})")
# (2.5 * 7.8) / 0.3 = 65.0   (ops=2, fns=())
# sqrt(16)          = 4.0    (ops=1, fns=('sqrt',))
```

#### Safety の意味

- `eval()` は使わない (任意コード実行回避)
- AST visitor で許可ノード (`BinOp` / `UnaryOp` / `Constant` / `Call` to whitelist) のみ通す
- 関数 whitelist: `sqrt` / `sin` / `cos` / `log` / `abs` / `mean` 等 28 関数 (math + statistics モジュール)
- 定数 whitelist: `pi` / `e` / `tau` / `inf` / `nan`
- 0 除算は `CalculationError` で安全に reject
- `__import__('os').system('rm')` のような攻撃を **attribute access 段階で reject**

### なぜ Wolfram Alpha より良いか

- Wolfram Alpha: 強力だが closed cloud、商用、有料
- MATH: 完全 on-prem (Z3 + Sympy はオープンソース)、監査ログ付き、BriefLedger に固定記録
- 数学・物理・工学・金融・薬学 のすべてが「数式の正しさ」を要求 → llive の vertical 戦略の中核

### v0.7-vertical MATH 全 8 件

| FR | 名前 | 優先 |
|---|---|---|
| MATH-01 | SI 単位次元解析エンジン | ✅ 実装済 |
| MATH-02 | Z3 / Sympy 統合検証層 | 2nd |
| MATH-05 | 物理定数辞書 (CODATA 2022 + NIST) | 3rd |
| **MATH-08** | **内蔵計算エンジン (差別化軸)** | ✅ 実装済 |
| MATH-03 | 数式構文解析 (LaTeX/MathML/Sympy AST) | MED |
| MATH-04 | 数値計算精度トラッキング (IEEE 754) | MED |
| MATH-06 | 単位変換 + Buckingham π 無次元化 | MED |
| MATH-07 | MATHEMATICAL EpistemicType | MED |

詳細: [03_math_vertical.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md)

---

## 4. CABT 設計予告 — Transformer ブロックを高度化する 7 アプローチ

ユーザー指示「Transformer 構造はシンプルだが各ブロックでもっと高度なことができる」+「マトリクスを参照ベース並べ替えに置換し付加情報を持たせる」+「llive 独自の思考の層と親和性が高いものに」を技術設計に落としたものです。

### 設計動機

![CABT: attention の置換案](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/summary/cabt_attention.svg)

### Hook 設計 (重み凍結のまま)

```python
# src/llive/cabt/hooks.py (S2 で実装予定)
class ReferenceAttentionHook:
    def _on_attention(self, module, inputs, outputs):
        attn_output = outputs[0]  # [batch, seq, hidden]
        bias = self._metadata_provider(attn_output)  # provenance/trust/...
        return (attn_output + self._strength * bias, *outputs[1:])
```

### 6 列 metadata

| 列 | 由来 |
|---|---|
| provenance_id | `memory/provenance.py` のレコード ID |
| trust_score | Quarantined Memory の trust 値 [0,1] |
| epistemic_type | FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC + RESERVED |
| timestamp_norm | 時系列正規化 [0,1] |
| source_domain_id | RAD 49 分野の ID |
| surprise_score | BayesianSurpriseGate (FR-21) の出力 |

### 7 つの CABT FR

| FR | 役割 | llive 思考層との接続 |
|---|---|---|
| CABT-01 | Reference-based Attention with Metadata | ユーザー直接案 |
| CABT-02 | Stage-aware Block Routing | FullSense 6 stage 連動 |
| CABT-03 | Epistemic-typed Token Pool | Multi-track Filter A-1.5 の token 化 |
| CABT-04 | Salience-gated Attention | FR-21 surprise gate 同期 |
| CABT-05 | TRIZ-conditioned Head Selection | BriefGrounder citation 連携 |
| CABT-06 | Approval-gated Decoding | C-1 Approval Bus を decoder 内拡張 |
| CABT-07 | Memory-augmented Residual | 4 層メモリを residual に注入 |

詳細: [04_next_cabt_block_design.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md)

---

## 5. CREAT 設計予告 — LLM × KJ法 × MindMap で要件定義を自動化

ユーザー観察「人間の思考の流れは KJ法 / MindMap / TRIZ 等を経て要件定義に入る」を技術設計に落としたもの。

### 人間の思考フロー vs llive

![人間の思考フロー ↔ llive のマッピング](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/summary/creat_thinking_flow.svg)

### 5 つの CREAT FR

| FR | 名前 | 効果 |
|---|---|---|
| CREAT-01 | KJ法ノード (LLM mixture sampling + clustering) | 視野狭窄を防ぐ (≥20 候補を強制) |
| CREAT-02 | MindMap ノード (DFS depth=3) | 思考の浅さを防ぐ (深さを強制) |
| CREAT-03 | 構造化変換 (4 出力を要件 spec に統合) | Brief → 自動 REQUIREMENTS.md 生成 |
| CREAT-04 | Six Hats Multi-track | 偏った楽観を防ぐ (cautious 観点を強制) |
| CREAT-05 | Synectics 類比エンジン (cross-domain RAD bridge) | 既存パターン依存を防ぐ (異分野類比を強制) |

詳細: [05_next_creat_kj_mindmap.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md)

---

## 6. MATH-02 設計予告 — 形式検証ゲートで LLM 数式幻覚を止める

### SafeCalculator (MATH-08, 実装済) では防げない幻覚

| 幻覚タイプ | SafeCalculator で防げる? |
|---|---|
| `(2.5 * 7.8) / 0.3 = 12.4` (実際は 65.0) | ✅ |
| `5 m/s + 3 s = 8` | ✅ (MATH-01 で) |
| `(x+1)² = x² + 2x` (2x ではなく 2x+1) | ❌ — **MATH-02 の対象** |
| `lim x→0 sin(x)/x = 0` (実際は 1) | ❌ — Sympy 必要 |
| `det([[1,2],[3,4]]) = 0` (実際は -2) | ❌ — Sympy 必要 |
| `e^(iπ) + 1 = 2` (実際は 0) | ❌ — Sympy 必要 |

### 設計

```
LLM 出力テキスト
    │
    ▼
[式抽出器] (MATH-03 multi-syntax parser)
    │
    ▼
[Sympy AST]
    │
    ├─→ simplify(lhs - rhs) == 0 ? → ✅ 通過
    │   ❌ → 失敗 flag
    │
    └─→ Z3 で satisfiability check (∀ x. lhs(x) == rhs(x) ?)
        ❌ → 反例を ledger に記録
```

```python
checker = FormalChecker()
verdict = checker.check_equation("(x+1)**2", "x**2 + 2*x")
# verdict.satisfied: False
# verdict.counterexample: {"x": 0}
# verdict.rationale: "differs at x=0: 1 vs 0"
```

### EVO-04 (既存 Z3) の延長線

- EVO-04: 「mutation 後の sub-block が ABI 制約を満たすか」を Z3 で検証
- MATH-02: 「LLM が出した等式が満たすべき推論ステップを Z3 で検証」

同じ Z3 layer の数式版。Phase 3 資産で拡張する経済設計。

詳細: [06_next_math02_formal_gate.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md)

---

## 7. Fair benchmark の罠 — honest disclosure の重要さ

### 最初のベンチで「異常に速い」結果

`bench_run.py` で `--all` (4 brief × 6 model) を実行したところ:

```
brief model       status      ms   chars
b1    llive       OK         152     884
b1    ollama      OK       18812     148
b1    perplexity  OK        4555     192
```

llive 134-184ms で 4/4 OK、cloud LLM や ollama より圧倒的に速い数字が出ました。

ユーザー指摘:

> 変に高速ですね、何か応答におかしな部分はないですか？

### 確認された異常 3 件

#### 異常 1: LLMBackend 未 attach

`run_brief.py` が `FullSenseLoop(sandbox=True)` を LLM backend なしで構築 → loop の `_inner_monologue` が **template 経路** (rule-based) に落ち、出力は:

```
Observation about 'manual': <brief content[:120]> — novel territory, worth exploring.
```

全 brief で同じテンプレート構造、brief の **先頭 120 文字**だけ thought に挿入。

#### 異常 2: chars が JSON 全長

`bench_run.py::chars = len(p.stdout)`:
- llive: JSON 構造 (stim metadata + stages + plan + raw) が dominant → 884 chars
- ollama / perplexity: LLM 応答テキストそのもの → 148〜1733 chars

つまり llive 4/4 で `884 chars` 同一なのは「同じ JSON 構造を吐いたから」。

#### 異常 3: 134-184ms は subprocess RTT

- py launcher 起動 + Python interpreter import (~80-120ms)
- `FullSenseLoop.process()` の 6 stage を template 経路で抜ける (~10-30ms)
- JSON 出力 (~1ms)
- subprocess wait + stdout 読込 (~10-30ms)

合計 134-184ms = LLM 推論レイテンシではない。

### 修正 — Fair contract

`run_brief.py` に `--backend ollama:qwen2.5:14b` 等を渡せる引数を追加し、`bench_run.py::run_llive` が `BENCH_LLIVE_BACKEND` env (default `ollama:qwen2.5:14b`) を必ず指定するように。

```python
def run_llive(brief: str, _keys: dict) -> tuple[bool, str, float]:
    backend = os.environ.get("BENCH_LLIVE_BACKEND", "ollama:qwen2.5:14b")
    debug_flag = os.environ.get("BENCH_LLIVE_DEBUG", "0") == "1"
    cmd = ["py", "-3.11", "llive/scripts/run_brief.py",
           "--json", "--backend", backend]
    if debug_flag:
        cmd.append("--debug")
    cmd.append(brief)
    # ...
    # chars は stages.thought.text から取得 (JSON 全長ではなく LLM 出力本体)
```

### Fair 再走結果

| brief | llive (+llama3.2:3b) | ollama 直叩き | perplexity |
|---|---|---|---|
| b1 | **32 750 ms** | 12 423 ms | 2 411 ms |
| b2 | **50 936 ms** | 13 024 ms | 3 591 ms |
| b3 | **43 787 ms** | 19 610 ms | 2 104 ms |
| b4 | **43 163 ms** | 21 936 ms | 6 162 ms |

llive (LLM attached) は ollama 直叩きの **2-4 倍遅い**。差分は `build_llm_prompt` がブリーフを `_inner_monologue` 用にラップして長文化させること。

### 教訓 (TRIZ 矛盾としての記録)

> ベンチで自社が異常に速い結果が出たら、勝った気になる前に必ず以下を確認:
> 1. LLM 推論レイヤーが実際に呼ばれているか
> 2. 計測時間に subprocess 起動 / JSON serialize 等の RTT が混ざっていないか
> 3. 応答長 (chars) の指標は同じ単位で測られているか
> 4. 応答内容が brief 内容を実質的に反映しているか

memory: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

### llive の付加価値の再定義

**llive の付加価値は速度ではなく構造** (ledger / approval / governance / grounding / 6 stage trace) にある。速度だけで判断するなら ollama 直叩きの方が良い。

詳細: [07_bench_results.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md)

---

## 8. Quiz bench — Debug vs Release × mean/stdev

ユーザー指示「DebugMode と Release 版でベンチマークテスト」+「クイズ形式 + 平均値・分散値」を反映。

### Quiz set v1 (10 問 × 5 カテゴリ × 2 難易度)

| id | category | difficulty |
|---|---|---|
| arith-01/02 | arithmetic | easy / medium |
| logic-01/02 | logic | easy / medium |
| knowledge-01/02 | knowledge | easy / medium |
| reason-01/02 | reasoning | easy / medium |
| creative-01/02 | creativity | easy / medium |

採点: keyword 一致 (`keyword_match` / `keyword_all` / `keyword_any` / `keyword_*_soft`)。

### bench_quiz.py に統計列を追加

```python
import statistics as _stat

partials = [c.get("partial_score", 0.0) for c in ok_cells]
mss = [c.get("ms", 0.0) for c in ok_cells]
p_mean = sum(partials) / len(partials) if partials else 0.0
p_std = _stat.stdev(partials) if len(partials) > 1 else 0.0
m_mean = sum(mss) / len(mss) if mss else 0.0
m_std = _stat.stdev(mss) if len(mss) > 1 else 0.0
```

### 結果 (llama3.2:3b × 10 quiz × {debug, release})

| mode | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum |
|---|---|---|---|---|---|---|
| Debug | 6/10 | 0.550 | 0.497 | **22 343** | 5 790 | 223.4 s |
| Release | 7/10 | 0.650 | 0.474 | **22 750** | 8 356 | 227.5 s |

### 観察

1. **Debug overhead は +1.8 % で実質ゼロ** → 開発時 debug=True 常時 ON でも性能ペナルティなし
2. 正答率の差 (6/10 vs 7/10) は **確率変動の範囲** (N=10 では二項検定で p > 0.5)
3. ms stdev が release で大きい (LLM 推論時間が問題依存で変動)

### 個別 quiz 結果のサンプル

| quiz | debug | release |
|---|---|---|
| arith-01 (easy) | ❌ 0.0 18.6s | ✅ 1.0 39.7s |
| arith-02 (medium) | ❌ 0.0 33.1s | ❌ 0.0 17.8s |
| logic-01 (easy) | ✅ 1.0 18.3s | ✅ 1.0 17.4s |
| logic-02 (medium) | ✅ 0.5 21.6s | ✅ 0.5 33.1s |
| knowledge-01 (easy) | ❌ 0.0 28.9s | ❌ 0.0 19.7s |
| knowledge-02 (medium) | ✅ 1.0 20.2s | ✅ 1.0 19.4s |
| reason-01 (easy) | ✅ 1.0 17.9s | ✅ 1.0 17.7s |
| reason-02 (medium) | ❌ 0.0 19.3s | ❌ 0.0 19.5s |
| creative-01 (easy) | ✅ 1.0 29.1s | ✅ 1.0 29.4s |
| creative-02 (medium) | ✅ 1.0 16.6s | ✅ 1.0 13.8s |

### 次回改善

- **N ≥ 30** で各 model 評価 (現在 N=10)
- 複数 model 並列 (llama3.2:3b / qwen2.5:7b / qwen2.5:14b)
- seed 固定 (`OLLAMA_SEED`) で再現性確保
- LLM-as-judge での 2 次採点
- 同一問題を 3 回サンプリングして per-quiz mean/stdev

詳細: [08_quiz_bench_debug_vs_release.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md)

---

## 9. llive の構造は LLM として独自か？ — 8 要素の点検

ユーザーの問い: 「llive の構造って、LLM として独自の構造になっていってますか？」

### 8 つの差別化要素

1. **Decoder-only LLM コアは凍結 + 周辺で能力拡張** — 重みを更新しないことで replay 可能 / monitorable な学習軌跡
2. **4 層メモリの責務分離** (semantic / episodic / **structural** / **parameter**) — 特に parameter memory (重みの差分を memory として扱う) が独自
3. **6 stage FullSense Loop** (Salience → Curiosity → Inner Monologue → Ego/Altruism → Action Plan → Output Bus) — 心理学的根拠付き 6 段モデル
4. **Multi-track Filter Architecture A-1.5** (EpistemicType による track 切替) — FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC で filter chain を切替
5. **Approval Bus を Loop 内に組み込み** — HITL を architecture level に、SQLite ledger で replay 可
6. **TRIZ 40 原理を mutation policy として内蔵** (FR-23〜27) — Contradiction Detector + Principle Mapper + RAD-Backed Idea Generator + 9-Window + ARIZ
7. **Cognitive Factor Framework (CFF) ― 10 因子を policy 分解** — planner / memory / critic / evolution / trace の 5 policy
8. **Brief API ― 構造化 work unit という primitives** — frozen + ledger + Approval Bus + Governance Scorer built-in

### 既存類似研究との位置づけ

| 既存系 | 重なる範囲 | llive の差別化 |
|---|---|---|
| MemGPT / LongMem | 階層メモリ | 4 層分離 + phase transition + 署名 zone |
| AutoML-Zero / NAS-LLM | 構造探索 | 形式検証 gate + multi-precision shadow + 失敗データ化 |
| Self-Refine / Reflexion | 自己批評 | online/offline 分離 + llove TUI HITL staging |
| MERA / ModularLLM | モジュラー化 | 可変長 BlockContainer YAML + plugin registry |
| AutoGPT 系 | エージェント | llmesh 産業 IoT 直結 + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | 10 因子明示分解 + 認知 OS positioning |

### 結論

> **llive は LLM ではなく、LLM を内蔵する「認知 OS」**

8 要素の組合せ × 役割分離 × 心理因子マッピングは類似研究のいずれにも一致しない。

### 「LLM 自体は何か変えているか」への答え

Phase 1〜v0.6 では LLM 重みは触らない (frozen)。これは設計判断:
- replay 可能性を最優先
- 学習軌跡を monitorable に保つ
- LLM 提供元 (Qwen, Meta, Mistral) の更新を直接取り込める

Phase 8 (CABT) で forward hook による attention bias 注入を計画。完全な独自 LLM 構築 (LoRA training / distillation) は Phase 11+ で。

詳細: [09_llive_structure_originality.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md)

---

## 10. Qwen 依存から離脱する 5 段階 (ORG-FX 戦略 A)

ユーザー観察:

> 差別化されていないと研究の価値がない。普及している AI を使った方がマシってなりそう。

### 現状の差別化の層別分析

| 層 | llive 独自性 | Qwen 依存度 |
|---|---|---|
| 入力 (Brief API) | ★★★★★ | 0% |
| Grounder (TRIZ × RAD) | ★★★★★ | 0% |
| 6 stage Loop | ★★★★☆ | 10% |
| 4 層メモリ | ★★★★☆ | 0% |
| Multi-track Filter | ★★★★☆ | 0% |
| Approval Bus | ★★★★★ | 0% |
| Governance Scoring | ★★★★★ | 0% |
| Trace Graph (Ledger) | ★★★★☆ | 0% |
| **LLM コア (Decoder-only Transformer)** | ☆ | **100%** ← 問題 |

### 5 段階ロードマップ

```
Stage A (短期, 〜3 ヶ月)
  ├ LLM コアは凍結
  ├ 周辺差別化を最大化
  └ CABT forward hook / MATH-08 / CREAT-01 で「LLM を使わない層」を厚く

Stage B (中期 1, 3〜6 ヶ月)
  ├ LoRA で llive 用 specialised adapter
  ├ RTX 3090 級で訓練可
  └ Attention に memory bias 注入

Stage C (中期 2, 6〜12 ヶ月)
  ├ Distillation: qwen2.5:14b → llive-7b
  ├ 学習データ: RAD 49 分野 + ledger 成功例 + TRIZ 出力
  └ Multi-track sub-network (EpistemicType 別)

Stage D (長期 1, 1〜2 年)
  ├ Transformer block を memory-coupled に置換
  ├ Cognitive Block Replacement (CABT-01〜07 本実装)
  └ Approval-native decoding

Stage E (長期 2, 2〜3 年)
  ├ Transformer 以外の LLM コア (Mamba / RWKV / Hyena / RetNet)
  ├ Surprise-native pretraining (Bayesian Surprise を loss に)
  └ TRIZ-guided architecture search (AutoML-Zero + TRIZ)
```

### 8 つの ORG-* FR

| FR | 名前 | Stage |
|---|---|---|
| ORG-06 | Provenance-aware tokens | B+D |
| ORG-02 | Memory-coupled inference | C/D |
| ORG-03 | Multi-track sub-network | C |
| ORG-08 | llive-specialized small model | C |
| ORG-07 | Approval-native decoding | C/D |
| ORG-01 | Cognitive Block Replacement | D |
| ORG-04 | TRIZ-guided architecture search | D |
| ORG-05 | Surprise-native pretraining | E |

### 3 つの評価指標

- **Architectural Originality Score (AOS)** = 差別化 FR 実装数 / 全 FR 数 (現状 ~60%, 目標 ≥85%)
- **LLM Core Independence Ratio (LCIR)** = llive 専用 inference path / 全 inference path (現状 0%, 目標 Stage C で ≥50%)
- **Replaceability Test** = Qwen を抜いて動作するか (Stage E で ✅)

### 長期で論文化候補

- "**Cognitive Block Replacement**: Memory-coupled Transformer for Verifiable Agent Loops"
- "**Provenance-aware Attention**: Trust Score as Inductive Bias"
- "**Surprise-native Pretraining**: Bayesian Surprise as Loss Function"
- "**TRIZ-guided Neural Architecture Search**: 40 Principles for Network Mutation"

ICML / NeurIPS / ICLR / AAAI で通る研究品質を目指す。

詳細: [10_qwen_divergence_strategy.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md)

---

## 11. Qwen と相互補完する llive — Local 環境で 5 隙間を埋める (戦略 B)

ユーザー観察:

> 相互補完の関係を目指すのもあり。もともと llive は Local 環境で動かす想定のもの。隙間をうまく補間できるといい。

### 二層構造

```
路線 1: 常設の補完戦略 (Local 環境特化)
       └ Qwen / Llama が進化しても不変の価値
路線 2: 研究としての独自化 (ORG-FX 5 段階)
       └ 中長期で研究価値を持続

両者は同時並走可能
```

### 5 つの隙間

#### 隙間 1: 数値計算・記号操作・形式検証

| Qwen の弱点 | llive の補完 |
|---|---|
| `(2.5 * 7.8) / 0.3` を間違える | **MATH-08 SafeCalculator** |
| `5 m/s + 3 s = 8` (次元誤り) | **MATH-01 SI 次元解析** |
| `(x+1)² = x² + 2x` (記号幻覚) | **MATH-02 Sympy 検算 + EVO-04 Z3** |
| CODATA 値の捏造 | **MATH-05 物理定数辞書** |

#### 隙間 2: 長期記憶・経験再生

| Qwen の弱点 | llive の補完 |
|---|---|
| context window (32K-128K) の限界 | **4 層メモリ** |
| session を跨ぐ記憶不能 | **persistent memory** + provenance |
| 同じ間違いを繰り返す | **Failed Reservoir** (EVO-06) + Reverse-Evo Monitor (EVO-07) |
| 「自分が以前何を言ったか」忘れる | **append-only ledger** |

#### 隙間 3: 行動監査・責任所在

| Qwen の弱点 | llive の補完 |
|---|---|
| 危険な動作の architectural gate なし | **Approval Bus** + Policy + SQLite Ledger |
| 出力責任の追跡困難 | **Provenance chain** + SHA-256 audit chain |
| dangerous tokens のフィルタなし | **GovernanceScorer** (4 軸 scoring) |
| 監査ログがエフェメラル | **persistent JSONL + replay** 可 |

#### 隙間 4: 認知構造・多視点・矛盾解決

| Qwen の弱点 | llive の補完 |
|---|---|
| 視野狭窄 (最初の候補に引きずられる) | **CREAT-01 KJ法ノード** (拡散 ≥20 件強制) |
| 思考の浅さ (1 階層展開) | **CREAT-02 MindMap** (DFS depth=3) |
| 偏った楽観 | **CREAT-04 Six Hats** (cautious 観点強制) |
| 既存パターン依存 | **CREAT-05 Synectics** (異分野類比) |
| 矛盾を扱えない | **TRIZ 40 原理** (FR-23〜27) |

#### 隙間 5: Local 環境特有の制約

| Local 環境の特性 | llive の対応 |
|---|---|
| ネットワーク不在 | **完全 on-prem 動作** (Ollama / LM Studio / vLLM) |
| 個人データを外に出せない | **provenance + Quarantined Zone** (SEC-01) |
| 計測機器との直接接続 | **llmesh sensor bridge** (FR-19, MQTT/OPC-UA) |
| エッジ推論 (低スペック) | **MATH-08 等の決定論的層** (LLM を呼ばない) |
| プライバシー (家族の会話、医療情報) | **Local-only ledger** + クラウド送信ゼロ |
| 起動時間・通信遅延の制約 | **Brief API の overhead < 1 %** (実測済) |

cloud LLM (GPT / Claude / Gemini / Perplexity) では **絶対に再現できない領域**。これが llive の **不変の差別化軸**。

### 再フレーミング

> 「単独で使うなら Qwen で十分」 → **「Qwen を Local 環境で安全に責任を持って使うなら llive が最短経路」**

### 評価ベンチへの示唆 (今後の改善)

「llive vs Qwen」の対立構図ではなく **協調 axis**:

- **Hybrid task score**: Qwen のみ vs llive (= Qwen + 決定論的補完層) の総合スコア
- **Niche task score**: Qwen が苦手なタスクで llive がどれだけ補えるか
- **Local capability**: ネットワークなしで完結する task の網羅率
- **Audit completeness**: 出力に対する trace coverage

詳細: [11_complementary_with_qwen.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md)

---

## 全体まとめ — 1 セッションでの到達点

### 実装

- **Brief API** (LLIVE-001/002) end-to-end / S1 BriefGrounder / MATH-01/08 / COG-01/02/03
- llive テスト: **1014 PASS / 0 fail / 0 regression**

### 要件追加 (REQUIREMENTS.md)

- v0.7-vertical MATH 8 件 (内 MATH-08 が差別化軸最大)
- v0.8 CABT 7 件 (Transformer ブロック高度化)
- v0.9 CREAT 5 件 (KJ法 / MindMap / Six Hats / Synectics)
- v1.0-frame COG-FX 4 件 (10 思考因子マッピング)
- v2.0-core ORG-FX 8 件 (Qwen 依存からの離脱 5 段階)
- **合計 100 件、Phase マッピング完備**

### ベンチマーク

| 種類 | セル数 | 主要観察 |
|---|---|---|
| progressive matrix | 5×3=15 | overhead < 1 %, decision 全 note |
| fair re-bench | 4×6=24 (実 OK 12) | llive (LLM attached) は ollama 直叩きの 2-4 倍遅い |
| quiz Debug | 10 | passed 6/10, ms mean 22.3s |
| quiz Release | 10 | passed 7/10, ms mean 22.8s, Debug overhead +1.8% |

### 戦略の二層構造

1. **常設の補完戦略** (Local 環境で 5 隙間補完) — cloud LLM が進化しても不変
2. **研究としての独自化** (ORG-FX 5 段階) — Stage A → B → C → D → E

### 教訓 — TRIZ 矛盾としての honest disclosure

> ベンチを取った瞬間に勝った気になる前に、ベンチの設計欠陥を疑う。

新規 memory: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

### GitHub

- llive: <https://github.com/furuse-kazufumi/llive>
- fullsense (umbrella ポータル): <https://github.com/furuse-kazufumi/fullsense>
- llove (TUI HITL): <https://github.com/furuse-kazufumi/llove>
- llmesh (LLM hub): <https://github.com/furuse-kazufumi/llmesh>

すべて **Apache-2.0 + Commercial dual-license**。

### 個別記事リンク (詳細はこちらから)

| # | タイトル | テーマ |
|---|---|---|
| 1 | [Brief API + progressive matrix (overhead < 1 %)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md) | Brief API + 5×3 ベンチ |
| 2 | [心理の深層 10 思考因子で整理する llive 思考層](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md) | COG-FX フレームワーク |
| 3 | [数学・単位に強い AI — MATH-01/08](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md) | MATH 系 |
| 4 | [Transformer ブロック高度化 7 アプローチ (CABT 設計予告)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md) | CABT |
| 5 | [LLM × KJ法 × MindMap で要件定義自動化 (CREAT 設計予告)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md) | CREAT |
| 6 | [形式検証ゲートで LLM 数式幻覚を止める (MATH-02 設計予告)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md) | MATH-02 |
| 7 | [fair bench (honest disclosure 全面改訂版)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md) | bench 方法論 |
| 8 | [quiz bench Debug vs Release × mean/stdev](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md) | quiz + 統計 |
| 9 | [llive 構造独自性 8 要素](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md) | 認知 OS positioning |
| 10 | [Qwen 離脱 5 段階 ORG-FX](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md) | 独自化路線 |
| 11 | [Qwen 相互補完 5 隙間](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md) | 補完路線 |

## おわりに

llive は「LLM そのもの」ではなく「LLM を内蔵する認知 OS」として、Local 環境で 5 つの隙間を補完しつつ、中長期では LLM コア自体の独自化を計画的に進める設計です。

1 日で要件 32 件 + 実装 1014 PASS + 公開記事 11 本 + 本サマリ という「ベンチで自社を疑う honest disclosure」も含む等身大の開発記録として残しました。

質問・指摘・改善提案は GitHub Issues または Twitter / X (@puruyan) までお願いします。

---

> 本記事は Claude Opus 4.7 (1M context) と対話しながら執筆。実装と検証も同セッション内で完走。1 日でこの規模を進められるのは、認知 OS が思考の足場をしっかり作っているから。

---

# English

# 32 Requirements Added in One Day + Brief API + COG-FX + MATH Implementation + 4 Benchmarks — A Development Log of the Self-Evolving LLM Framework llive, 2026-05-17

Author: **Kazufumi Furuse (puruyan)**

## Introduction — What Was Achieved in a Single Session

In one session on 2026-05-17 (Claude Opus 4.7, 1M context, via ccr), the following was achieved for the **self-evolving LLM framework [llive](https://github.com/furuse-kazufumi/llive)**:

| Category | Count | Content |
|---|---|---|
| Requirements (FR) added | **32** | v0.7-MATH 8 / v0.8-CABT 7 / v0.9-CREAT 5 / v1.0-COG-FX 4 / v2.0-ORG-FX 8 |
| Implementation (LoC) | ~2,200 lines | Brief API end-to-end / Grounder / Governance / Trace Graph / MATH units & calculation |
| Tests added | **+78** | 936 → **1014 PASS / 0 fail / 0 regression** |
| 4 benchmarks | 15 + 12 + 10 + 10 cells | progressive matrix / fair bench / quiz Debug / quiz Release |
| Published articles | **11 + this article** | [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17) |
| GitHub push | 2 repositories | llive `349a234` / fullsense `cb346aa` |

llive is positioned as a **"cognitive OS" with embedded OSS LLMs (Qwen / Llama / Mistral)**. The decoder-only LLM core stays frozen, while a 4-layer memory + 6-stage Loop + Approval Bus + TRIZ 40 principles + 10 thinking factors are integrated into a research-and-development framework.

This article consolidates 11 individual articles **with their full text** so it can be read end-to-end on Qiita alone. Detailed links are also placed at the end of each chapter.

---

## 1. Brief API end-to-end (LLIVE-001/002, all 7 steps)

### Motivation

Until now, llive's `FullSenseLoop.process(Stimulus)` was a **thinking-evaluator**, not a **doing-agent**. That is because there was no API for external clients (lldesign / lltrade / the planned llcad/lleda/llchip) to hand over a "structured work unit."

The design draft `docs/proposals/brief_api_design.md` (estimated at 5 days) was completed in a single session.

### Brief dataclass

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str                           # ascii word/dash/dot のみ、path-safe
    goal: str                               # 必須
    constraints: tuple[str, ...] = ()
    source: str = "manual"
    priority: float = 0.5                   # [0.0, 1.0]
    epistemic_type: EpistemicType = EpistemicType.PRAGMATIC
    backend: str = ""                       # "ollama:qwen2.5:14b" 等
    tools: tuple[str, ...] = ()             # whitelist
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    ledger_path: Path | None = None
```

**frozen + tuple** makes it hashable / replay-friendly. The invariant that the same Brief is shared across ledger, loop, and result is protected by `frozen`.

### BriefRunner — a single submit transaction executes the following

```
1. brief_submitted          → ledger
2. (optional) grounding_applied (TRIZ × RAD citation)
3. stimulus_built           → ledger
4. FullSenseLoop.process(stim)
   └─ 6 stage loop (既存)
5. loop_completed           → ledger
6. decision                 → ledger
7. (optional) governance_scored (COG-02, 4 軸)
8. Approval Bus gate (PROPOSE/INTERVENE 時のみ)
9. tool_invoked × N         → ledger
10. outcome                 → ledger
```

Everything is recorded in an **append-only JSONL ledger**. The `meta` envelope separates timestamp/pid so they can be ignored during replay.

### CLI

```bash
# YAML から
llive brief submit path/to/brief.yaml

# インライン
llive brief submit --goal "Refactor docs/index.md..." \
                   --brief-id portal-refresh \
                   --priority 0.8 --no-approval

# ledger 検索
llive brief ledger portal-refresh-2026-05-16 --json --limit 5
```

### MCP

A `submit_brief` tool was added, allowing tasks to be handed to llive from Claude Desktop / Cursor and similar:

```jsonc
{
  "name": "submit_brief",
  "input_schema": {
    "type": "object",
    "required": ["goal"],
    "properties": {
      "goal": {"type": "string"},
      "constraints": {"type": "array", "items": {"type": "string"}},
      "priority": {"type": "number", "minimum": 0.0, "maximum": 1.0},
      "approval_required": {"type": "boolean", "default": true}
    }
  }
}
```

### Progressive validation matrix (5×3 = 15 cells)

xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b} were run on-prem only (mixing in cloud is forbidden, per the `feedback_llive_measurement_purity` rule):

#### Wall-time matrix (ms)

| model | xs (cold) | s | m | l | xl (timeout) |
|---|---|---|---|---|---|
| llama3.2:3b | 8,908 | 43,978 | 89,484 | 458,400 | 1,202,282 ⌛ |
| qwen2.5:7b | 59,447 | 94,158 | 122,134 | 722,867 | 1,202,104 ⌛ |
| qwen2.5:14b | 121,560 | 122,160 | 122,160 | 1,202,263⌛ | 1,202,199 ⌛ |

#### LLM-only / Wall

Over **> 99.8 %** across all 15 cells — the added cost of the Brief API + loop is under ~1 %.

#### Loop decision

| model \ size | xs | s | m | l | xl |
|---|---|---|---|---|---|
| llama3.2:3b | note | note | note | note | note |
| qwen2.5:7b | note | note | note | note | note |
| qwen2.5:14b | note | note | note | note | note |

**All 15 cells `note`** — the loop's decision tree is completely stable under token pressure.

### Connection to the thinking layer

- `Brief.epistemic_type` selects the Multi-track Filter chain
- `Brief.priority` becomes Stimulus.surprise and influences the Salience Gate
- `Brief.constraints` are injected into the thought as an augmented goal
- `Brief.tools` whitelist restricts BriefRunner's tool execution
- `Brief.approval_required` routes through the C-1 Approval Bus

Details: [01_brief_api_progressive.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md)

---

## 2. Organizing llive's Thinking Layer with the "Depths of Psychology" 10 Thinking Factors — 9/10 Implemented

### Source

A set of human thinking factors extracted from the YouTube channel "Shinri no Shinso" (Depths of Psychology). The user explicitly shifted the goal away from "explaining depth psychology" toward **"extracting reusable thinking factors → embedding them into LLM reasoning, planning, self-improvement, and agent design,"** and turned it into requirements.

### 10 factors × llive mapping

| # | Factor | LLM role | llive existing (implemented) | Added (implemented 2026-05-17) |
|---|---|---|---|---|
| 1 | **Structuring** | Decompose the problem | Brief constraints, Salience+Curiosity gate | — |
| 2 | Reconstruction | Generate alternatives | TRIZ 40 principles + ARIZ + 9-window (FR-23–27) | (CREAT-01 planned) |
| 3 | **Closed loop** | Comes with a verification plan | BriefRunner (submit→plan→approval→tool→outcome) | — |
| 4 | Self-extension | Use external resources | 4-layer memory + RAD 49 domains + tools whitelist | MATH-08 calculation engine |
| 5 | **Uncertainty** | Separate hypothesis from fact | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | Exploration | Try untrodden ideas | EVO-* (Z3 + Failed Reservoir + Reverse-Evo) | — |
| 7 | **Consistency** | Re-evaluate under global constraints | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | **Provenance** | Keep a history of decisions | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | Multiple perspectives | Separate evaluation functions | Multi-track Filter A-1.5 (5 EpistemicTypes) | (COG-04 + CREAT-04 planned) |
| 10 | Reality grounding | Handle real-environment constraints | (Phase 4 INT-01–04 in planning) | — |

### The 5 v1.0-mandatory factors (in bold) are all implemented

User observation: **"Before strengthening exploration / reconstruction, you need the foundation of structuring / uncertainty / closed loop / consistency / provenance."** Without this, strengthening the exploration and reconstruction factors increases interesting ideas but also increases error, runaway behavior, and non-reproducibility.

| Factor | Implementation location |
|---|---|
| Structuring | `src/llive/brief/types.py::Brief` + loop._salience_gate/curiosity_drive |
| Closed loop | `src/llive/brief/runner.py::BriefRunner.submit` |
| Uncertainty | `src/llive/learning/bayesian_surprise.py` (FR-21) + COG-01 |
| Consistency | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py` (EVO-04) + COG-02 |
| Provenance | `src/llive/memory/provenance.py` + ledger × 3 + COG-03 |

### Implementation of COG-01–03

#### COG-01 Triple Output

Three columns — **confidence / assumptions / missing_evidence** — were added to `BriefResult`:

```python
@dataclass
class BriefResult:
    # 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` computes them deterministically:

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`: makes explicit the absence of a grounder / absence of success_criteria
- `missing_evidence`: records that no TRIZ principle surfaced / tool failures

#### COG-02 Governance Scoring Layer

A 4-axis scorer is inserted **upstream** of the Approval Bus:

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block
```

Separation of responsibilities:
- **Governance** = scoring (why it is good/bad)
- **Approval Bus** = gating (the decision of whether to execute)

Supports dangerous_token detection (`rm -rf` / `DROP TABLE` / `format c:` etc.), an INTERVENE-without-approval penalty, and `block_threshold` / `safety_floor`.

#### COG-03 Trace Graph

`BriefLedger.trace_graph()` returns a 3-layer view:

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

This makes debugging, self-improvement, failure analysis, and extraction of learning data for evolution mechanically possible.

Details: [02_cognitive_factors.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md)

---

## 3. A First Step Toward AI Strong in Math and Units — MATH-01/08

llive's first vertical specialization is "math- and unit-specialized AI." It overcomes the following weaknesses of general-purpose LLMs with a **deterministic side-car that "does not let the LLM compute."**

### Mathematical weaknesses of LLMs

| Aspect | Weakness of general-purpose LLM | Match with llive's existing assets |
|---|---|---|
| Hallucinated symbol manipulation | Wrong identities like `x² + x = 2x³` | Gated by EVO-04 Z3 static verification |
| Unit dimensions | `5 m/s + 3 s = 8` | SI dimensional analysis engine (MATH-01) |
| Numerical precision | Ignores float arithmetic error | error propagation tracking (MATH-04) |
| Axiom systems | Mixes in implicit premises | strict track of EpistemicType=MATHEMATICAL |
| Citation reliability | Answers "CODATA value is X" at random | RAD math/metrology + provenance |

### MATH-01 — Dimensional algebra of SI 7 base units + derived units

```python
from llive.math import Quantity, parse_unit, UnitMismatchError

# 速度 + 時間 = 不可能 (典型的 LLM 幻覚を必ず止める)
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t
assert d.dimensions.matches(parse_unit("m"))

# 力 × 距離 = エネルギー (J)
F = Quantity(10.0, parse_unit("N"))
d = Quantity(5.0, parse_unit("m"))
E = F * d
assert E.dimensions.matches(parse_unit("J"))  # ✓
```

The core of the implementation is the 7-dimensional vector `Dimensions(m, kg, s, A, K, mol, cd)`. `Quantity.__add__` verifies dimensions → a mismatch **always raises**.

Derived units: `N` (kg·m/s²) / `J` (kg·m²/s²) / `W` (kg·m²/s³) / `Pa` (kg/m/s²) / `Hz` (1/s) / `C` (s·A) / `V` (kg·m²/s³/A) / `ohm` are implemented only for the frequently used range.

### MATH-08 — Built-in calculation engine (greatest differentiation axis)

**Design core**: do **not** let the LLM perform numerical computation.

```python
from llive.math import SafeCalculator, extract_expressions

calc = SafeCalculator()
brief_text = "Compute (2.5 * 7.8) / 0.3 then verify sqrt(16) is exact."

for expr in extract_expressions(brief_text):
    r = calc.evaluate(expr)
    print(f"{r.expression} = {r.value}  (ops={r.operation_count}, fns={r.used_functions})")
# (2.5 * 7.8) / 0.3 = 65.0   (ops=2, fns=())
# sqrt(16)          = 4.0    (ops=1, fns=('sqrt',))
```

#### What "safety" means

- Does not use `eval()` (avoids arbitrary code execution)
- An AST visitor passes only allowed nodes (`BinOp` / `UnaryOp` / `Constant` / `Call` to whitelist)
- Function whitelist: 28 functions such as `sqrt` / `sin` / `cos` / `log` / `abs` / `mean` (math + statistics modules)
- Constant whitelist: `pi` / `e` / `tau` / `inf` / `nan`
- Division by zero is safely rejected with `CalculationError`
- Attacks like `__import__('os').system('rm')` are **rejected at the attribute-access stage**

### Why it is better than Wolfram Alpha

- Wolfram Alpha: powerful but closed cloud, commercial, paid
- MATH: fully on-prem (Z3 + Sympy are open source), with an audit log, fixed-recorded in the BriefLedger
- Math, physics, engineering, finance, and pharmacology all require "the correctness of formulas" → the core of llive's vertical strategy

### All 8 v0.7-vertical MATH items

| FR | Name | Priority |
|---|---|---|
| MATH-01 | SI unit dimensional analysis engine | ✅ Implemented |
| MATH-02 | Z3 / Sympy integrated verification layer | 2nd |
| MATH-05 | Physical constants dictionary (CODATA 2022 + NIST) | 3rd |
| **MATH-08** | **Built-in calculation engine (differentiation axis)** | ✅ Implemented |
| MATH-03 | Formula parsing (LaTeX/MathML/Sympy AST) | MED |
| MATH-04 | Numerical precision tracking (IEEE 754) | MED |
| MATH-06 | Unit conversion + Buckingham π non-dimensionalization | MED |
| MATH-07 | MATHEMATICAL EpistemicType | MED |

Details: [03_math_vertical.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md)

---

## 4. CABT Design Preview — 7 Approaches to Advancing the Transformer Block

This translates into a technical design the user's instructions: "The Transformer structure is simple, but each block could do something far more advanced," "Replace the matrix with a reference-based reordering and give it side information," and "Make it highly compatible with llive's own thinking layers."

### Design motivation

![CABT: attention replacement](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/summary/cabt_attention_en.svg)

### Hook design (weights stay frozen)

```python
# src/llive/cabt/hooks.py (S2 で実装予定)
class ReferenceAttentionHook:
    def _on_attention(self, module, inputs, outputs):
        attn_output = outputs[0]  # [batch, seq, hidden]
        bias = self._metadata_provider(attn_output)  # provenance/trust/...
        return (attn_output + self._strength * bias, *outputs[1:])
```

### 6-column metadata

| Column | Origin |
|---|---|
| provenance_id | Record ID from `memory/provenance.py` |
| trust_score | trust value [0,1] of Quarantined Memory |
| epistemic_type | FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC + RESERVED |
| timestamp_norm | time-series normalization [0,1] |
| source_domain_id | ID of one of the RAD 49 domains |
| surprise_score | output of the BayesianSurpriseGate (FR-21) |

### The 7 CABT FRs

| FR | Role | Connection to llive's thinking layer |
|---|---|---|
| CABT-01 | Reference-based Attention with Metadata | User's direct proposal |
| CABT-02 | Stage-aware Block Routing | Linked to FullSense 6 stages |
| CABT-03 | Epistemic-typed Token Pool | Tokenization of Multi-track Filter A-1.5 |
| CABT-04 | Salience-gated Attention | Synced with FR-21 surprise gate |
| CABT-05 | TRIZ-conditioned Head Selection | Linked with BriefGrounder citation |
| CABT-06 | Approval-gated Decoding | Extends the C-1 Approval Bus inside the decoder |
| CABT-07 | Memory-augmented Residual | Injects the 4-layer memory into the residual |

Details: [04_next_cabt_block_design.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md)

---

## 5. CREAT Design Preview — Automating Requirements Definition with LLM × KJ Method × MindMap

This translates into a technical design the user's observation: "The human flow of thought passes through the KJ method / MindMap / TRIZ and so on before entering requirements definition."

### Human thinking flow vs llive

![Human thinking flow ↔ llive mapping](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/summary/creat_thinking_flow_en.svg)

### The 5 CREAT FRs

| FR | Name | Effect |
|---|---|---|
| CREAT-01 | KJ-method node (LLM mixture sampling + clustering) | Prevents tunnel vision (forces ≥20 candidates) |
| CREAT-02 | MindMap node (DFS depth=3) | Prevents shallow thinking (forces depth) |
| CREAT-03 | Structuring transform (integrates 4 outputs into a requirements spec) | Brief → automatic REQUIREMENTS.md generation |
| CREAT-04 | Six Hats Multi-track | Prevents biased optimism (forces a cautious perspective) |
| CREAT-05 | Synectics analogy engine (cross-domain RAD bridge) | Prevents dependence on existing patterns (forces cross-domain analogy) |

Details: [05_next_creat_kj_mindmap.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md)

---

## 6. MATH-02 Design Preview — Stopping LLM Formula Hallucination with a Formal Verification Gate

### Hallucinations that SafeCalculator (MATH-08, implemented) cannot prevent

| Hallucination type | Can SafeCalculator prevent it? |
|---|---|
| `(2.5 * 7.8) / 0.3 = 12.4` (actually 65.0) | ✅ |
| `5 m/s + 3 s = 8` | ✅ (via MATH-01) |
| `(x+1)² = x² + 2x` (it is 2x+1, not 2x) | ❌ — **target of MATH-02** |
| `lim x→0 sin(x)/x = 0` (actually 1) | ❌ — needs Sympy |
| `det([[1,2],[3,4]]) = 0` (actually -2) | ❌ — needs Sympy |
| `e^(iπ) + 1 = 2` (actually 0) | ❌ — needs Sympy |

### Design

```
LLM 出力テキスト
    │
    ▼
[式抽出器] (MATH-03 multi-syntax parser)
    │
    ▼
[Sympy AST]
    │
    ├─→ simplify(lhs - rhs) == 0 ? → ✅ 通過
    │   ❌ → 失敗 flag
    │
    └─→ Z3 で satisfiability check (∀ x. lhs(x) == rhs(x) ?)
        ❌ → 反例を ledger に記録
```

```python
checker = FormalChecker()
verdict = checker.check_equation("(x+1)**2", "x**2 + 2*x")
# verdict.satisfied: False
# verdict.counterexample: {"x": 0}
# verdict.rationale: "differs at x=0: 1 vs 0"
```

### An extension of EVO-04 (existing Z3)

- EVO-04: verifies with Z3 whether "the sub-block after mutation satisfies the ABI constraints"
- MATH-02: verifies with Z3 "the inference steps that the equation produced by the LLM should satisfy"

A formula-oriented version of the same Z3 layer. An economical design that extends Phase 3 assets.

Details: [06_next_math02_formal_gate.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md)

---

## 7. The Trap of Fair Benchmarks — The Importance of Honest Disclosure

### The first benchmark produced "abnormally fast" results

Running `bench_run.py` with `--all` (4 briefs × 6 models) gave:

```
brief model       status      ms   chars
b1    llive       OK         152     884
b1    ollama      OK       18812     148
b1    perplexity  OK        4555     192
```

llive at 134–184ms passed 4/4, with numbers overwhelmingly faster than cloud LLMs or ollama.

User's remark:

> Suspiciously fast. Isn't there something odd in the responses?

### 3 confirmed anomalies

#### Anomaly 1: LLMBackend not attached

`run_brief.py` constructed `FullSenseLoop(sandbox=True)` without an LLM backend → the loop's `_inner_monologue` fell into the **template path** (rule-based), and the output was:

```
Observation about 'manual': <brief content[:120]> — novel territory, worth exploring.
```

Every brief had the same template structure, with only the **first 120 characters** of the brief inserted into the thought.

#### Anomaly 2: chars was the full JSON length

`bench_run.py::chars = len(p.stdout)`:
- llive: the JSON structure (stim metadata + stages + plan + raw) dominates → 884 chars
- ollama / perplexity: the LLM response text itself → 148–1733 chars

So llive being identically `884 chars` for 4/4 was because "it emitted the same JSON structure."

#### Anomaly 3: 134–184ms is subprocess RTT

- py launcher startup + Python interpreter import (~80-120ms)
- passing through the 6 stages of `FullSenseLoop.process()` via the template path (~10-30ms)
- JSON output (~1ms)
- subprocess wait + reading stdout (~10-30ms)

Total 134–184ms = not LLM inference latency.

### Fix — Fair contract

An argument was added to `run_brief.py` to pass `--backend ollama:qwen2.5:14b` and the like, and `bench_run.py::run_llive` was changed to always specify the `BENCH_LLIVE_BACKEND` env (default `ollama:qwen2.5:14b`).

```python
def run_llive(brief: str, _keys: dict) -> tuple[bool, str, float]:
    backend = os.environ.get("BENCH_LLIVE_BACKEND", "ollama:qwen2.5:14b")
    debug_flag = os.environ.get("BENCH_LLIVE_DEBUG", "0") == "1"
    cmd = ["py", "-3.11", "llive/scripts/run_brief.py",
           "--json", "--backend", backend]
    if debug_flag:
        cmd.append("--debug")
    cmd.append(brief)
    # ...
    # chars は stages.thought.text から取得 (JSON 全長ではなく LLM 出力本体)
```

### Fair re-run results

| brief | llive (+llama3.2:3b) | ollama direct | perplexity |
|---|---|---|---|
| b1 | **32,750 ms** | 12,423 ms | 2,411 ms |
| b2 | **50,936 ms** | 13,024 ms | 3,591 ms |
| b3 | **43,787 ms** | 19,610 ms | 2,104 ms |
| b4 | **43,163 ms** | 21,936 ms | 6,162 ms |

llive (with LLM attached) is **2–4× slower** than calling ollama directly. The difference is that `build_llm_prompt` wraps the brief for `_inner_monologue`, making it longer.

### Lesson (recorded as a TRIZ contradiction)

> When a benchmark shows your own product to be abnormally fast, before feeling like you won, always check the following:
> 1. Is the LLM inference layer actually being called?
> 2. Is the measured time mixing in RTT such as subprocess startup / JSON serialization?
> 3. Is the response-length (chars) metric measured in the same unit?
> 4. Does the response content substantively reflect the brief content?

memory: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

### Redefining llive's added value

**llive's added value is not speed but structure** (ledger / approval / governance / grounding / 6-stage trace). If you judge by speed alone, calling ollama directly is better.

Details: [07_bench_results.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md)

---

## 8. Quiz bench — Debug vs Release × mean/stdev

This reflects the user's instructions: "Benchmark-test the DebugMode and Release versions" + "quiz format + mean/variance."

### Quiz set v1 (10 questions × 5 categories × 2 difficulties)

| id | category | difficulty |
|---|---|---|
| arith-01/02 | arithmetic | easy / medium |
| logic-01/02 | logic | easy / medium |
| knowledge-01/02 | knowledge | easy / medium |
| reason-01/02 | reasoning | easy / medium |
| creative-01/02 | creativity | easy / medium |

Scoring: keyword match (`keyword_match` / `keyword_all` / `keyword_any` / `keyword_*_soft`).

### Statistics columns added to bench_quiz.py

```python
import statistics as _stat

partials = [c.get("partial_score", 0.0) for c in ok_cells]
mss = [c.get("ms", 0.0) for c in ok_cells]
p_mean = sum(partials) / len(partials) if partials else 0.0
p_std = _stat.stdev(partials) if len(partials) > 1 else 0.0
m_mean = sum(mss) / len(mss) if mss else 0.0
m_std = _stat.stdev(mss) if len(mss) > 1 else 0.0
```

### Results (llama3.2:3b × 10 quizzes × {debug, release})

| mode | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum |
|---|---|---|---|---|---|---|
| Debug | 6/10 | 0.550 | 0.497 | **22,343** | 5,790 | 223.4 s |
| Release | 7/10 | 0.650 | 0.474 | **22,750** | 8,356 | 227.5 s |

### Observations

1. **Debug overhead is +1.8 %, essentially zero** → no performance penalty even with debug=True always ON during development
2. The difference in accuracy (6/10 vs 7/10) is **within the range of random variation** (at N=10, a binomial test gives p > 0.5)
3. ms stdev is larger for release (LLM inference time varies with the problem)

### Sample of individual quiz results

| quiz | debug | release |
|---|---|---|
| arith-01 (easy) | ❌ 0.0 18.6s | ✅ 1.0 39.7s |
| arith-02 (medium) | ❌ 0.0 33.1s | ❌ 0.0 17.8s |
| logic-01 (easy) | ✅ 1.0 18.3s | ✅ 1.0 17.4s |
| logic-02 (medium) | ✅ 0.5 21.6s | ✅ 0.5 33.1s |
| knowledge-01 (easy) | ❌ 0.0 28.9s | ❌ 0.0 19.7s |
| knowledge-02 (medium) | ✅ 1.0 20.2s | ✅ 1.0 19.4s |
| reason-01 (easy) | ✅ 1.0 17.9s | ✅ 1.0 17.7s |
| reason-02 (medium) | ❌ 0.0 19.3s | ❌ 0.0 19.5s |
| creative-01 (easy) | ✅ 1.0 29.1s | ✅ 1.0 29.4s |
| creative-02 (medium) | ✅ 1.0 16.6s | ✅ 1.0 13.8s |

### Next improvements

- Evaluate each model with **N ≥ 30** (currently N=10)
- Multiple models in parallel (llama3.2:3b / qwen2.5:7b / qwen2.5:14b)
- Fix the seed (`OLLAMA_SEED`) to ensure reproducibility
- A second round of scoring with LLM-as-judge
- Sample the same question 3 times for per-quiz mean/stdev

Details: [08_quiz_bench_debug_vs_release.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md)

---

## 9. Is llive's Structure Original as an LLM? — An Inspection of 8 Elements

User's question: "Is llive's structure becoming an original structure as an LLM?"

### The 8 differentiation elements

1. **The decoder-only LLM core is frozen, with capability extended at the periphery** — by not updating the weights, the learning trajectory is replayable / monitorable
2. **Separation of responsibilities in the 4-layer memory** (semantic / episodic / **structural** / **parameter**) — in particular, the parameter memory (treating weight deltas as memory) is original
3. **The 6-stage FullSense Loop** (Salience → Curiosity → Inner Monologue → Ego/Altruism → Action Plan → Output Bus) — a psychologically grounded 6-stage model
4. **Multi-track Filter Architecture A-1.5** (track switching by EpistemicType) — switches the filter chain among FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC
5. **The Approval Bus is built into the Loop** — bringing HITL to the architecture level, replayable via the SQLite ledger
6. **TRIZ 40 principles built in as a mutation policy** (FR-23–27) — Contradiction Detector + Principle Mapper + RAD-Backed Idea Generator + 9-Window + ARIZ
7. **Cognitive Factor Framework (CFF) — decomposing 10 factors into policies** — the 5 policies of planner / memory / critic / evolution / trace
8. **Brief API — a primitive that is a structured work unit** — frozen + ledger + Approval Bus + Governance Scorer built in

### Positioning against existing related research

| Existing line | Overlapping range | llive's differentiation |
|---|---|---|
| MemGPT / LongMem | Hierarchical memory | 4-layer separation + phase transition + signed zone |
| AutoML-Zero / NAS-LLM | Structure search | formal verification gate + multi-precision shadow + turning failures into data |
| Self-Refine / Reflexion | Self-criticism | online/offline separation + llove TUI HITL staging |
| MERA / ModularLLM | Modularization | variable-length BlockContainer YAML + plugin registry |
| AutoGPT line | Agents | llmesh industrial IoT direct connection + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | explicit decomposition of 10 factors + cognitive OS positioning |

### Conclusion

> **llive is not an LLM but a "cognitive OS" with an embedded LLM**

The combination of the 8 elements × role separation × psychological-factor mapping matches none of the related research.

### The answer to "Is the LLM itself being changed in any way?"

In Phase 1 through v0.6, the LLM weights are not touched (frozen). This is a design decision:
- Prioritize replayability above all
- Keep the learning trajectory monitorable
- Be able to directly incorporate updates from the LLM providers (Qwen, Meta, Mistral)

Phase 8 (CABT) plans attention-bias injection via a forward hook. Building a fully original LLM (LoRA training / distillation) is for Phase 11+.

Details: [09_llive_structure_originality.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md)

---

## 10. The 5 Stages of Breaking Away from Qwen Dependence (ORG-FX Strategy A)

User observation:

> Without differentiation, there is no research value. It would feel like "you might as well use a widely adopted AI."

### Layered analysis of the current differentiation

| Layer | llive originality | Qwen dependence |
|---|---|---|
| Input (Brief API) | ★★★★★ | 0% |
| Grounder (TRIZ × RAD) | ★★★★★ | 0% |
| 6-stage Loop | ★★★★☆ | 10% |
| 4-layer memory | ★★★★☆ | 0% |
| Multi-track Filter | ★★★★☆ | 0% |
| Approval Bus | ★★★★★ | 0% |
| Governance Scoring | ★★★★★ | 0% |
| Trace Graph (Ledger) | ★★★★☆ | 0% |
| **LLM core (Decoder-only Transformer)** | ☆ | **100%** ← the problem |

### 5-stage roadmap

```
Stage A (短期, 〜3 ヶ月)
  ├ LLM コアは凍結
  ├ 周辺差別化を最大化
  └ CABT forward hook / MATH-08 / CREAT-01 で「LLM を使わない層」を厚く

Stage B (中期 1, 3〜6 ヶ月)
  ├ LoRA で llive 用 specialised adapter
  ├ RTX 3090 級で訓練可
  └ Attention に memory bias 注入

Stage C (中期 2, 6〜12 ヶ月)
  ├ Distillation: qwen2.5:14b → llive-7b
  ├ 学習データ: RAD 49 分野 + ledger 成功例 + TRIZ 出力
  └ Multi-track sub-network (EpistemicType 別)

Stage D (長期 1, 1〜2 年)
  ├ Transformer block を memory-coupled に置換
  ├ Cognitive Block Replacement (CABT-01〜07 本実装)
  └ Approval-native decoding

Stage E (長期 2, 2〜3 年)
  ├ Transformer 以外の LLM コア (Mamba / RWKV / Hyena / RetNet)
  ├ Surprise-native pretraining (Bayesian Surprise を loss に)
  └ TRIZ-guided architecture search (AutoML-Zero + TRIZ)
```

### The 8 ORG-* FRs

| FR | Name | Stage |
|---|---|---|
| ORG-06 | Provenance-aware tokens | B+D |
| ORG-02 | Memory-coupled inference | C/D |
| ORG-03 | Multi-track sub-network | C |
| ORG-08 | llive-specialized small model | C |
| ORG-07 | Approval-native decoding | C/D |
| ORG-01 | Cognitive Block Replacement | D |
| ORG-04 | TRIZ-guided architecture search | D |
| ORG-05 | Surprise-native pretraining | E |

### The 3 evaluation metrics

- **Architectural Originality Score (AOS)** = number of differentiation FRs implemented / total FRs (currently ~60%, target ≥85%)
- **LLM Core Independence Ratio (LCIR)** = llive-specific inference paths / all inference paths (currently 0%, target ≥50% at Stage C)
- **Replaceability Test** = does it work with Qwen removed (✅ at Stage E)

### Long-term candidates for academic papers

- "**Cognitive Block Replacement**: Memory-coupled Transformer for Verifiable Agent Loops"
- "**Provenance-aware Attention**: Trust Score as Inductive Bias"
- "**Surprise-native Pretraining**: Bayesian Surprise as Loss Function"
- "**TRIZ-guided Neural Architecture Search**: 40 Principles for Network Mutation"

Aiming for research quality that passes at ICML / NeurIPS / ICLR / AAAI.

Details: [10_qwen_divergence_strategy.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md)

---

## 11. llive Mutually Complementing Qwen — Filling 5 Gaps in the Local Environment (Strategy B)

User observation:

> Aiming for a mutually complementary relationship is also an option. llive was originally intended to run in the Local environment. It would be good to interpolate the gaps well.

### Two-layer structure

```
路線 1: 常設の補完戦略 (Local 環境特化)
       └ Qwen / Llama が進化しても不変の価値
路線 2: 研究としての独自化 (ORG-FX 5 段階)
       └ 中長期で研究価値を持続

両者は同時並走可能
```

### The 5 gaps

#### Gap 1: Numerical computation, symbol manipulation, formal verification

| Qwen's weakness | llive's complement |
|---|---|
| Gets `(2.5 * 7.8) / 0.3` wrong | **MATH-08 SafeCalculator** |
| `5 m/s + 3 s = 8` (dimension error) | **MATH-01 SI dimensional analysis** |
| `(x+1)² = x² + 2x` (symbol hallucination) | **MATH-02 Sympy check + EVO-04 Z3** |
| Fabricating CODATA values | **MATH-05 physical constants dictionary** |

#### Gap 2: Long-term memory, experience replay

| Qwen's weakness | llive's complement |
|---|---|
| Limits of the context window (32K-128K) | **4-layer memory** |
| Inability to remember across sessions | **persistent memory** + provenance |
| Repeating the same mistakes | **Failed Reservoir** (EVO-06) + Reverse-Evo Monitor (EVO-07) |
| Forgetting "what it said before" | **append-only ledger** |

#### Gap 3: Action auditing, accountability

| Qwen's weakness | llive's complement |
|---|---|
| No architectural gate for dangerous actions | **Approval Bus** + Policy + SQLite Ledger |
| Difficulty tracing output accountability | **Provenance chain** + SHA-256 audit chain |
| No filter for dangerous tokens | **GovernanceScorer** (4-axis scoring) |
| Ephemeral audit logs | **persistent JSONL + replay** capable |

#### Gap 4: Cognitive structure, multiple perspectives, contradiction resolution

| Qwen's weakness | llive's complement |
|---|---|
| Tunnel vision (dragged along by the first candidate) | **CREAT-01 KJ-method node** (forces ≥20 in divergence) |
| Shallow thinking (1-level expansion) | **CREAT-02 MindMap** (DFS depth=3) |
| Biased optimism | **CREAT-04 Six Hats** (forces a cautious perspective) |
| Dependence on existing patterns | **CREAT-05 Synectics** (cross-domain analogy) |
| Cannot handle contradictions | **TRIZ 40 principles** (FR-23–27) |

#### Gap 5: Constraints specific to the Local environment

| Characteristic of the Local environment | llive's response |
|---|---|
| No network | **fully on-prem operation** (Ollama / LM Studio / vLLM) |
| Cannot send personal data outside | **provenance + Quarantined Zone** (SEC-01) |
| Direct connection to measurement instruments | **llmesh sensor bridge** (FR-19, MQTT/OPC-UA) |
| Edge inference (low-spec) | **deterministic layers such as MATH-08** (does not call the LLM) |
| Privacy (family conversations, medical information) | **Local-only ledger** + zero cloud transmission |
| Constraints of startup time / communication latency | **Brief API overhead < 1 %** (measured) |

A domain that cloud LLMs (GPT / Claude / Gemini / Perplexity) can **never reproduce**. This is llive's **invariant differentiation axis**.

### Reframing

> "If you use it alone, Qwen is enough" → **"If you want to use Qwen safely and responsibly in the Local environment, llive is the shortest path"**

### Implications for evaluation benchmarks (future improvements)

Not a "llive vs Qwen" confrontation but a **cooperation axis**:

- **Hybrid task score**: the overall score of Qwen alone vs llive (= Qwen + deterministic complement layer)
- **Niche task score**: how much llive can compensate on tasks Qwen is weak at
- **Local capability**: the coverage of tasks that complete without a network
- **Audit completeness**: trace coverage of the output

Details: [11_complementary_with_qwen.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md)

---

## Overall Summary — What Was Reached in One Session

### Implementation

- **Brief API** (LLIVE-001/002) end-to-end / S1 BriefGrounder / MATH-01/08 / COG-01/02/03
- llive tests: **1014 PASS / 0 fail / 0 regression**

### Requirements added (REQUIREMENTS.md)

- v0.7-vertical MATH 8 items (of which MATH-08 is the greatest differentiation axis)
- v0.8 CABT 7 items (advancing the Transformer block)
- v0.9 CREAT 5 items (KJ method / MindMap / Six Hats / Synectics)
- v1.0-frame COG-FX 4 items (10 thinking factors mapping)
- v2.0-core ORG-FX 8 items (5 stages of breaking away from Qwen dependence)
- **100 items in total, with complete Phase mapping**

### Benchmarks

| Type | Cells | Key observation |
|---|---|---|
| progressive matrix | 5×3=15 | overhead < 1 %, all decisions note |
| fair re-bench | 4×6=24 (12 actually OK) | llive (with LLM attached) is 2–4× slower than calling ollama directly |
| quiz Debug | 10 | passed 6/10, ms mean 22.3s |
| quiz Release | 10 | passed 7/10, ms mean 22.8s, Debug overhead +1.8% |

### The two-layer structure of the strategy

1. **Permanent complement strategy** (filling 5 gaps in the Local environment) — invariant even as cloud LLMs evolve
2. **Originalization as research** (ORG-FX 5 stages) — Stage A → B → C → D → E

### Lesson — Honest disclosure as a TRIZ contradiction

> Before feeling like you won the moment you take a benchmark, suspect a design flaw in the benchmark.

New memory: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

### GitHub

- llive: <https://github.com/furuse-kazufumi/llive>
- fullsense (umbrella portal): <https://github.com/furuse-kazufumi/fullsense>
- llove (TUI HITL): <https://github.com/furuse-kazufumi/llove>
- llmesh (LLM hub): <https://github.com/furuse-kazufumi/llmesh>

All are **Apache-2.0 + Commercial dual-license**.

### Links to individual articles (for details)

| # | Title | Theme |
|---|---|---|
| 1 | [Brief API + progressive matrix (overhead < 1 %)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md) | Brief API + 5×3 bench |
| 2 | [Organizing llive's thinking layer with the Depths-of-Psychology 10 thinking factors](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md) | COG-FX framework |
| 3 | [AI strong in math and units — MATH-01/08](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md) | MATH line |
| 4 | [7 approaches to advancing the Transformer block (CABT design preview)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md) | CABT |
| 5 | [Automating requirements definition with LLM × KJ method × MindMap (CREAT design preview)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md) | CREAT |
| 6 | [Stopping LLM formula hallucination with a formal verification gate (MATH-02 design preview)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md) | MATH-02 |
| 7 | [fair bench (fully revised honest-disclosure edition)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md) | bench methodology |
| 8 | [quiz bench Debug vs Release × mean/stdev](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md) | quiz + statistics |
| 9 | [8 elements of llive's structural originality](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md) | cognitive OS positioning |
| 10 | [5 stages of breaking away from Qwen, ORG-FX](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md) | originalization line |
| 11 | [5 gaps of mutual complement with Qwen](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md) | complement line |

## Closing

llive, as not "the LLM itself" but "a cognitive OS with an embedded LLM," is designed to fill 5 gaps in the Local environment while methodically advancing the originalization of the LLM core itself over the medium to long term.

I have left this as a life-sized development record — including the "honest disclosure of suspecting your own product on a benchmark" — of 32 requirements + 1014 PASS implementation + 11 published articles + this summary in one day.

Questions, criticisms, and improvement suggestions are welcome via GitHub Issues or Twitter / X (@puruyan).

---

> This article was written while conversing with Claude Opus 4.7 (1M context). Implementation and verification were also completed within the same session. The reason this scale can be advanced in a single day is that the cognitive OS firmly builds the scaffolding for thinking.

---

# 中文

# 一天内新增 32 项需求 + Brief API + COG-FX + MATH 实现 + 4 种基准测试 —— 自进化型 LLM 框架 llive 开发记 2026-05-17

作者: **古濑和文（puruyan）**

## 引言 —— 在一次会话中达成了什么

在 2026-05-17 的一次会话（Claude Opus 4.7，1M context，经由 ccr）中，针对**自进化型 LLM 框架 [llive](https://github.com/furuse-kazufumi/llive)** 达成了以下成果：

| 类别 | 数量 | 内容 |
|---|---|---|
| 新增需求 (FR) | **32 项** | v0.7-MATH 8 / v0.8-CABT 7 / v0.9-CREAT 5 / v1.0-COG-FX 4 / v2.0-ORG-FX 8 |
| 实现 (LoC) | ~2,200 行 | Brief API end-to-end / Grounder / Governance / Trace Graph / MATH 单位与计算 |
| 新增测试 | **+78 项** | 936 → **1014 PASS / 0 fail / 0 regression** |
| 4 种基准测试 | 15 + 12 + 10 + 10 单元格 | progressive matrix / fair bench / quiz Debug / quiz Release |
| 公开文章 | **11 篇 + 本文** | [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17) |
| GitHub push | 2 个仓库 | llive `349a234` / fullsense `cb346aa` |

llive 的定位是**内置开源 LLM（Qwen / Llama / Mistral）的"认知 OS"**。decoder-only LLM 核心保持 frozen，而将 4 层记忆 + 6 阶段 Loop + Approval Bus + TRIZ 40 原理 + 10 思考因子整合为一个研究开发框架。

本文将 11 篇独立文章**连同正文**整合在一起，使其仅在 Qiita 上也能通读。各章末尾也放置了详细链接。

---

## 1. Brief API end-to-end (LLIVE-001/002 全 7 步)

### 动机

迄今为止，llive 的 `FullSenseLoop.process(Stimulus)` 一直是 **thinking-evaluator**，而非 **doing-agent**。原因在于没有让外部客户端（lldesign / lltrade / 计划中的 llcad/lleda/llchip）递交"结构化 work unit"的 API。

设计草案 `docs/proposals/brief_api_design.md`（预估 5 天）在一次会话中全部完成。

### Brief dataclass

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str                           # ascii word/dash/dot のみ、path-safe
    goal: str                               # 必須
    constraints: tuple[str, ...] = ()
    source: str = "manual"
    priority: float = 0.5                   # [0.0, 1.0]
    epistemic_type: EpistemicType = EpistemicType.PRAGMATIC
    backend: str = ""                       # "ollama:qwen2.5:14b" 等
    tools: tuple[str, ...] = ()             # whitelist
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    ledger_path: Path | None = None
```

**frozen + tuple** 使其可哈希 / 利于 replay。同一个 Brief 由 ledger、loop、result 共享这一不变式由 frozen 保护。

### BriefRunner —— 单次 submit 事务执行以下流程

```
1. brief_submitted          → ledger
2. (optional) grounding_applied (TRIZ × RAD citation)
3. stimulus_built           → ledger
4. FullSenseLoop.process(stim)
   └─ 6 stage loop (既存)
5. loop_completed           → ledger
6. decision                 → ledger
7. (optional) governance_scored (COG-02, 4 軸)
8. Approval Bus gate (PROPOSE/INTERVENE 時のみ)
9. tool_invoked × N         → ledger
10. outcome                 → ledger
```

全部记录在 **append-only JSONL ledger** 中。`meta` envelope 将 timestamp/pid 分离出来，使其在 replay 时可被忽略。

### CLI

```bash
# YAML から
llive brief submit path/to/brief.yaml

# インライン
llive brief submit --goal "Refactor docs/index.md..." \
                   --brief-id portal-refresh \
                   --priority 0.8 --no-approval

# ledger 検索
llive brief ledger portal-refresh-2026-05-16 --json --limit 5
```

### MCP

新增了 `submit_brief` tool，可从 Claude Desktop / Cursor 等向 llive 递交任务：

```jsonc
{
  "name": "submit_brief",
  "input_schema": {
    "type": "object",
    "required": ["goal"],
    "properties": {
      "goal": {"type": "string"},
      "constraints": {"type": "array", "items": {"type": "string"}},
      "priority": {"type": "number", "minimum": 0.0, "maximum": 1.0},
      "approval_required": {"type": "boolean", "default": true}
    }
  }
}
```

### Progressive validation matrix (5×3 = 15 单元格)

xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b} 仅在 on-prem 下实跑（禁止混入 cloud，遵循 `feedback_llive_measurement_purity` 规则）：

#### Wall-time matrix (ms)

| model | xs (cold) | s | m | l | xl (timeout) |
|---|---|---|---|---|---|
| llama3.2:3b | 8,908 | 43,978 | 89,484 | 458,400 | 1,202,282 ⌛ |
| qwen2.5:7b | 59,447 | 94,158 | 122,134 | 722,867 | 1,202,104 ⌛ |
| qwen2.5:14b | 121,560 | 122,160 | 122,160 | 1,202,263⌛ | 1,202,199 ⌛ |

#### LLM-only / Wall

全部 15 个单元格均 **> 99.8 %** —— Brief API + loop 的额外开销不到 ~1 %。

#### Loop decision

| model \ size | xs | s | m | l | xl |
|---|---|---|---|---|---|
| llama3.2:3b | note | note | note | note | note |
| qwen2.5:7b | note | note | note | note | note |
| qwen2.5:14b | note | note | note | note | note |

**全部 15 个单元格 `note`** —— loop 的决策树在 token 压力下完全 stable。

### 与思考层的连接

- `Brief.epistemic_type` 选择 Multi-track Filter 的 chain
- `Brief.priority` 成为 Stimulus.surprise 并影响 Salience Gate
- `Brief.constraints` 作为 augmented goal 注入到 thought 中
- `Brief.tools` whitelist 限制 BriefRunner 的 tool 执行
- `Brief.approval_required` 经由 C-1 Approval Bus

详情: [01_brief_api_progressive.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md)

---

## 2. 用"心理的深层"10 思考因子整理 llive 思考层 —— 9/10 已实现

### 出处

从 YouTube 频道"心理的深层"中提取的人类思考因子集合。用户明确将目标从"深层心理的说明"转向 **"提取可复用的思考因子 → 嵌入到 LLM 的推理、计划、自我改善、agent 设计"**，并将其需求化。

### 10 因子 × llive 映射

| # | 因子 | LLM 角色 | llive 既有（已实现） | 新增（2026-05-17 实现） |
|---|---|---|---|---|
| 1 | **结构化** | 分解课题 | Brief constraints, Salience+Curiosity gate | — |
| 2 | 重构 | 生成替代方案 | TRIZ 40 原理 + ARIZ + 9 画法 (FR-23〜27) | (CREAT-01 计划) |
| 3 | **闭环** | 伴随验证计划 | BriefRunner (submit→plan→approval→tool→outcome) | — |
| 4 | 自我扩展 | 使用外部资源 | 4 层记忆 + RAD 49 分野 + tools whitelist | MATH-08 计算引擎 |
| 5 | **不确定性** | 分离假设与事实 | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | 探索 | 尝试未踏方案 | EVO-* (Z3 + Failed Reservoir + Reverse-Evo) | — |
| 7 | **一致性** | 以整体约束重新评估 | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | **来历** | 保留判断历史 | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | 多视角 | 分离评价函数 | Multi-track Filter A-1.5 (5 EpistemicType) | (COG-04 + CREAT-04 计划) |
| 10 | 现实连接 | 处理实环境约束 | (Phase 4 INT-01〜04 计划中) | — |

### v1.0 必需的 5 因子（粗体）全部已实现

用户观察：**"在强化探索 / 重构之前，需要结构化 / 不确定性 / 闭环 / 一致性 / 来历的地基。"** 没有这些就强化探索因子和重构因子，有趣的方案会增多，但误差、失控、不可复现性也会增多。

| 因子 | 实现位置 |
|---|---|
| 结构化 | `src/llive/brief/types.py::Brief` + loop._salience_gate/curiosity_drive |
| 闭环 | `src/llive/brief/runner.py::BriefRunner.submit` |
| 不确定性 | `src/llive/learning/bayesian_surprise.py` (FR-21) + COG-01 |
| 一致性 | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py` (EVO-04) + COG-02 |
| 来历 | `src/llive/memory/provenance.py` + ledger × 3 + COG-03 |

### COG-01〜03 的实现

#### COG-01 Triple Output

向 `BriefResult` 增加了 **confidence / assumptions / missing_evidence** 三列：

```python
@dataclass
class BriefResult:
    # 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` 确定性地计算：

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`：明示 grounder 不在 / success_criteria 不在
- `missing_evidence`：记录 TRIZ 原理未 surface / tool 失败

#### COG-02 Governance Scoring Layer

在 Approval Bus 的**前段**插入 4 轴评分器：

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block
```

职责分离：
- **Governance** = scoring（为何好/坏）
- **Approval Bus** = gating（是否执行的判断）

支持 dangerous_token 检测（`rm -rf` / `DROP TABLE` / `format c:` 等）、INTERVENE-without-approval 惩罚、`block_threshold` / `safety_floor`。

#### COG-03 Trace Graph

`BriefLedger.trace_graph()` 返回 3 层 view：

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

由此，调试、自我改善、失败分析、向 evolution 提取学习数据均可机械化进行。

详情: [02_cognitive_factors.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md)

---

## 3. 迈向擅长数学与单位的 AI 的第一步 —— MATH-01/08

llive 的第一个 vertical specialisation 是"数学与单位特化 AI"。它用**"不让 LLM 计算"的确定性 side-car** 克服通用 LLM 不擅长的以下问题。

### LLM 的数学弱点

| 观点 | 通用 LLM 的弱点 | 与 llive 既有资产的契合 |
|---|---|---|
| 符号操作的幻觉 | 像 `x² + x = 2x³` 这样的错误等式 | 由 EVO-04 Z3 静态验证 gate |
| 单位量纲 | `5 m/s + 3 s = 8` | SI 量纲分析引擎 (MATH-01) |
| 数值精度 | 忽略 float 运算误差 | error propagation tracking (MATH-04) |
| 公理体系 | 混入隐含前提 | EpistemicType=MATHEMATICAL 的 strict track |
| 引用可靠性 | 随口回答 "CODATA value is X" | RAD math/metrology + provenance |

### MATH-01 —— SI 7 基本单位 + 派生单位的量纲代数

```python
from llive.math import Quantity, parse_unit, UnitMismatchError

# 速度 + 時間 = 不可能 (典型的 LLM 幻覚を必ず止める)
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t
assert d.dimensions.matches(parse_unit("m"))

# 力 × 距離 = エネルギー (J)
F = Quantity(10.0, parse_unit("N"))
d = Quantity(5.0, parse_unit("m"))
E = F * d
assert E.dimensions.matches(parse_unit("J"))  # ✓
```

实现的核心是 `Dimensions(m, kg, s, A, K, mol, cd)` 这一 7 维向量。`Quantity.__add__` 进行量纲验算 → 不一致**必定 raise**。

派生单位：`N` (kg·m/s²) / `J` (kg·m²/s²) / `W` (kg·m²/s³) / `Pa` (kg/m/s²) / `Hz` (1/s) / `C` (s·A) / `V` (kg·m²/s³/A) / `ohm` 仅在高频范围实现。

### MATH-08 —— 内置计算引擎（差别化轴最大）

**设计核心**：**不让 LLM 进行数值计算**。

```python
from llive.math import SafeCalculator, extract_expressions

calc = SafeCalculator()
brief_text = "Compute (2.5 * 7.8) / 0.3 then verify sqrt(16) is exact."

for expr in extract_expressions(brief_text):
    r = calc.evaluate(expr)
    print(f"{r.expression} = {r.value}  (ops={r.operation_count}, fns={r.used_functions})")
# (2.5 * 7.8) / 0.3 = 65.0   (ops=2, fns=())
# sqrt(16)          = 4.0    (ops=1, fns=('sqrt',))
```

#### Safety 的含义

- 不使用 `eval()`（避免任意代码执行）
- 由 AST visitor 只放行允许的节点（`BinOp` / `UnaryOp` / `Constant` / `Call` to whitelist）
- 函数 whitelist：`sqrt` / `sin` / `cos` / `log` / `abs` / `mean` 等 28 个函数（math + statistics 模块）
- 常量 whitelist：`pi` / `e` / `tau` / `inf` / `nan`
- 除零以 `CalculationError` 安全 reject
- 像 `__import__('os').system('rm')` 这样的攻击在 **attribute access 阶段被 reject**

### 为何优于 Wolfram Alpha

- Wolfram Alpha：强大但 closed cloud、商用、收费
- MATH：完全 on-prem（Z3 + Sympy 为开源）、带审计日志、固定记录到 BriefLedger
- 数学、物理、工学、金融、药学 全部要求"数式的正确性" → llive 的 vertical 战略的核心

### v0.7-vertical MATH 全 8 项

| FR | 名称 | 优先 |
|---|---|---|
| MATH-01 | SI 单位量纲分析引擎 | ✅ 已实现 |
| MATH-02 | Z3 / Sympy 集成验证层 | 2nd |
| MATH-05 | 物理常数辞典 (CODATA 2022 + NIST) | 3rd |
| **MATH-08** | **内置计算引擎（差别化轴）** | ✅ 已实现 |
| MATH-03 | 数式语法解析 (LaTeX/MathML/Sympy AST) | MED |
| MATH-04 | 数值计算精度跟踪 (IEEE 754) | MED |
| MATH-06 | 单位转换 + Buckingham π 无量纲化 | MED |
| MATH-07 | MATHEMATICAL EpistemicType | MED |

详情: [03_math_vertical.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md)

---

## 4. CABT 设计预告 —— 让 Transformer 块更高级的 7 种方法

将用户指示"Transformer 结构虽简单，但每个块都能做更高级的事"+"将矩阵置换为基于引用的重排并赋予附加信息"+"与 llive 独有的思考层亲和性高"落实为技术设计。

### 设计动机

![CABT：attention 的替换方案](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/summary/cabt_attention_zh.svg)

### Hook 设计（权重保持 frozen）

```python
# src/llive/cabt/hooks.py (S2 で実装予定)
class ReferenceAttentionHook:
    def _on_attention(self, module, inputs, outputs):
        attn_output = outputs[0]  # [batch, seq, hidden]
        bias = self._metadata_provider(attn_output)  # provenance/trust/...
        return (attn_output + self._strength * bias, *outputs[1:])
```

### 6 列 metadata

| 列 | 来源 |
|---|---|
| provenance_id | `memory/provenance.py` 的记录 ID |
| trust_score | Quarantined Memory 的 trust 值 [0,1] |
| epistemic_type | FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC + RESERVED |
| timestamp_norm | 时序正规化 [0,1] |
| source_domain_id | RAD 49 分野的 ID |
| surprise_score | BayesianSurpriseGate (FR-21) 的输出 |

### 7 个 CABT FR

| FR | 角色 | 与 llive 思考层的连接 |
|---|---|---|
| CABT-01 | Reference-based Attention with Metadata | 用户直接提案 |
| CABT-02 | Stage-aware Block Routing | 与 FullSense 6 stage 联动 |
| CABT-03 | Epistemic-typed Token Pool | Multi-track Filter A-1.5 的 token 化 |
| CABT-04 | Salience-gated Attention | 与 FR-21 surprise gate 同步 |
| CABT-05 | TRIZ-conditioned Head Selection | 与 BriefGrounder citation 联动 |
| CABT-06 | Approval-gated Decoding | 在 decoder 内扩展 C-1 Approval Bus |
| CABT-07 | Memory-augmented Residual | 将 4 层记忆注入 residual |

详情: [04_next_cabt_block_design.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md)

---

## 5. CREAT 设计预告 —— 用 LLM × KJ法 × MindMap 自动化需求定义

将用户观察"人类的思考流程经过 KJ法 / MindMap / TRIZ 等后才进入需求定义"落实为技术设计。

### 人类思考流程 vs llive

![人类思考流程 ↔ llive 映射](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/summary/creat_thinking_flow_zh.svg)

### 5 个 CREAT FR

| FR | 名称 | 效果 |
|---|---|---|
| CREAT-01 | KJ法节点 (LLM mixture sampling + clustering) | 防止视野狭窄（强制 ≥20 候选） |
| CREAT-02 | MindMap 节点 (DFS depth=3) | 防止思考浅薄（强制深度） |
| CREAT-03 | 结构化变换（将 4 输出整合为需求 spec） | Brief → 自动生成 REQUIREMENTS.md |
| CREAT-04 | Six Hats Multi-track | 防止偏向乐观（强制 cautious 观点） |
| CREAT-05 | Synectics 类比引擎 (cross-domain RAD bridge) | 防止依赖既有模式（强制异分野类比） |

详情: [05_next_creat_kj_mindmap.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md)

---

## 6. MATH-02 设计预告 —— 用形式验证 gate 阻止 LLM 数式幻觉

### SafeCalculator (MATH-08, 已实现) 无法防止的幻觉

| 幻觉类型 | SafeCalculator 能防止吗？ |
|---|---|
| `(2.5 * 7.8) / 0.3 = 12.4`（实际为 65.0） | ✅ |
| `5 m/s + 3 s = 8` | ✅（由 MATH-01） |
| `(x+1)² = x² + 2x`（是 2x+1，不是 2x） | ❌ —— **MATH-02 的对象** |
| `lim x→0 sin(x)/x = 0`（实际为 1） | ❌ —— 需要 Sympy |
| `det([[1,2],[3,4]]) = 0`（实际为 -2） | ❌ —— 需要 Sympy |
| `e^(iπ) + 1 = 2`（实际为 0） | ❌ —— 需要 Sympy |

### 设计

```
LLM 出力テキスト
    │
    ▼
[式抽出器] (MATH-03 multi-syntax parser)
    │
    ▼
[Sympy AST]
    │
    ├─→ simplify(lhs - rhs) == 0 ? → ✅ 通過
    │   ❌ → 失敗 flag
    │
    └─→ Z3 で satisfiability check (∀ x. lhs(x) == rhs(x) ?)
        ❌ → 反例を ledger に記録
```

```python
checker = FormalChecker()
verdict = checker.check_equation("(x+1)**2", "x**2 + 2*x")
# verdict.satisfied: False
# verdict.counterexample: {"x": 0}
# verdict.rationale: "differs at x=0: 1 vs 0"
```

### EVO-04（既有 Z3）的延长线

- EVO-04：用 Z3 验证"mutation 后的 sub-block 是否满足 ABI 约束"
- MATH-02：用 Z3 验证"LLM 给出的等式应满足的推理步骤"

同一 Z3 layer 的数式版。以 Phase 3 资产扩展的经济设计。

详情: [06_next_math02_formal_gate.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md)

---

## 7. Fair benchmark 的陷阱 —— honest disclosure 的重要性

### 最初的基准测试出现"异常快"的结果

用 `bench_run.py` 执行 `--all`（4 brief × 6 model）时：

```
brief model       status      ms   chars
b1    llive       OK         152     884
b1    ollama      OK       18812     148
b1    perplexity  OK        4555     192
```

llive 在 134-184ms 内 4/4 OK，出现了比 cloud LLM 或 ollama 压倒性更快的数字。

用户指出：

> 快得有点奇怪，回应里没有什么异常之处吗？

### 确认的 3 项异常

#### 异常 1：LLMBackend 未 attach

`run_brief.py` 在没有 LLM backend 的情况下构建 `FullSenseLoop(sandbox=True)` → loop 的 `_inner_monologue` 落入 **template 路径**（rule-based），输出为：

```
Observation about 'manual': <brief content[:120]> — novel territory, worth exploring.
```

所有 brief 都是相同的 template 结构，只将 brief 的**前 120 个字符**插入到 thought 中。

#### 异常 2：chars 是 JSON 全长

`bench_run.py::chars = len(p.stdout)`：
- llive：JSON 结构（stim metadata + stages + plan + raw）占主导 → 884 chars
- ollama / perplexity：LLM 回应文本本身 → 148〜1733 chars

也就是说，llive 4/4 都是 `884 chars` 相同，是因为"吐出了相同的 JSON 结构"。

#### 异常 3：134-184ms 是 subprocess RTT

- py launcher 启动 + Python interpreter import (~80-120ms)
- 以 template 路径穿过 `FullSenseLoop.process()` 的 6 stage (~10-30ms)
- JSON 输出 (~1ms)
- subprocess wait + 读取 stdout (~10-30ms)

合计 134-184ms = 并非 LLM 推理延迟。

### 修正 —— Fair contract

向 `run_brief.py` 增加可传入 `--backend ollama:qwen2.5:14b` 等的参数，并将 `bench_run.py::run_llive` 改为必定指定 `BENCH_LLIVE_BACKEND` env（default `ollama:qwen2.5:14b`）。

```python
def run_llive(brief: str, _keys: dict) -> tuple[bool, str, float]:
    backend = os.environ.get("BENCH_LLIVE_BACKEND", "ollama:qwen2.5:14b")
    debug_flag = os.environ.get("BENCH_LLIVE_DEBUG", "0") == "1"
    cmd = ["py", "-3.11", "llive/scripts/run_brief.py",
           "--json", "--backend", backend]
    if debug_flag:
        cmd.append("--debug")
    cmd.append(brief)
    # ...
    # chars は stages.thought.text から取得 (JSON 全長ではなく LLM 出力本体)
```

### Fair 重跑结果

| brief | llive (+llama3.2:3b) | ollama 直接调用 | perplexity |
|---|---|---|---|
| b1 | **32,750 ms** | 12,423 ms | 2,411 ms |
| b2 | **50,936 ms** | 13,024 ms | 3,591 ms |
| b3 | **43,787 ms** | 19,610 ms | 2,104 ms |
| b4 | **43,163 ms** | 21,936 ms | 6,162 ms |

llive（LLM attached）比直接调用 ollama **慢 2-4 倍**。差异在于 `build_llm_prompt` 将 brief 为 `_inner_monologue` 包装而使其变长。

### 教训（作为 TRIZ 矛盾的记录）

> 当基准测试显示自家产品异常之快时，在自以为获胜之前，请务必确认以下几点：
> 1. LLM 推理层是否真的被调用
> 2. 计测时间中是否混入了 subprocess 启动 / JSON serialize 等 RTT
> 3. 回应长度 (chars) 的指标是否以相同单位测量
> 4. 回应内容是否实质性地反映了 brief 内容

memory: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

### 重新定义 llive 的附加价值

**llive 的附加价值不在速度而在结构**（ledger / approval / governance / grounding / 6 stage trace）。若仅以速度判断，直接调用 ollama 更好。

详情: [07_bench_results.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md)

---

## 8. Quiz bench —— Debug vs Release × mean/stdev

反映用户指示"用 DebugMode 和 Release 版做基准测试"+"测验形式 + 平均值・方差值"。

### Quiz set v1 (10 题 × 5 类别 × 2 难度)

| id | category | difficulty |
|---|---|---|
| arith-01/02 | arithmetic | easy / medium |
| logic-01/02 | logic | easy / medium |
| knowledge-01/02 | knowledge | easy / medium |
| reason-01/02 | reasoning | easy / medium |
| creative-01/02 | creativity | easy / medium |

评分：keyword 一致（`keyword_match` / `keyword_all` / `keyword_any` / `keyword_*_soft`）。

### 向 bench_quiz.py 增加统计列

```python
import statistics as _stat

partials = [c.get("partial_score", 0.0) for c in ok_cells]
mss = [c.get("ms", 0.0) for c in ok_cells]
p_mean = sum(partials) / len(partials) if partials else 0.0
p_std = _stat.stdev(partials) if len(partials) > 1 else 0.0
m_mean = sum(mss) / len(mss) if mss else 0.0
m_std = _stat.stdev(mss) if len(mss) > 1 else 0.0
```

### 结果 (llama3.2:3b × 10 quiz × {debug, release})

| mode | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum |
|---|---|---|---|---|---|---|
| Debug | 6/10 | 0.550 | 0.497 | **22,343** | 5,790 | 223.4 s |
| Release | 7/10 | 0.650 | 0.474 | **22,750** | 8,356 | 227.5 s |

### 观察

1. **Debug overhead 为 +1.8 %，实质为零** → 开发时即使 debug=True 常时 ON 也无性能惩罚
2. 正答率的差异（6/10 vs 7/10）在**概率波动范围内**（N=10 时二项检验 p > 0.5）
3. ms stdev 在 release 更大（LLM 推理时间随问题而变动）

### 个别 quiz 结果的样本

| quiz | debug | release |
|---|---|---|
| arith-01 (easy) | ❌ 0.0 18.6s | ✅ 1.0 39.7s |
| arith-02 (medium) | ❌ 0.0 33.1s | ❌ 0.0 17.8s |
| logic-01 (easy) | ✅ 1.0 18.3s | ✅ 1.0 17.4s |
| logic-02 (medium) | ✅ 0.5 21.6s | ✅ 0.5 33.1s |
| knowledge-01 (easy) | ❌ 0.0 28.9s | ❌ 0.0 19.7s |
| knowledge-02 (medium) | ✅ 1.0 20.2s | ✅ 1.0 19.4s |
| reason-01 (easy) | ✅ 1.0 17.9s | ✅ 1.0 17.7s |
| reason-02 (medium) | ❌ 0.0 19.3s | ❌ 0.0 19.5s |
| creative-01 (easy) | ✅ 1.0 29.1s | ✅ 1.0 29.4s |
| creative-02 (medium) | ✅ 1.0 16.6s | ✅ 1.0 13.8s |

### 下次改善

- 以 **N ≥ 30** 评估各 model（当前 N=10）
- 多个 model 并行（llama3.2:3b / qwen2.5:7b / qwen2.5:14b）
- 固定 seed（`OLLAMA_SEED`）以确保可复现性
- 以 LLM-as-judge 进行二次评分
- 对同一问题采样 3 次以得到 per-quiz mean/stdev

详情: [08_quiz_bench_debug_vs_release.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md)

---

## 9. llive 的结构作为 LLM 是否独特？ —— 8 要素的点检

用户的提问：「llive 的结构，是否正在成为作为 LLM 的独特结构？」

### 8 个差别化要素

1. **Decoder-only LLM 核心被冻结 + 在外围扩展能力** —— 通过不更新权重，使学习轨迹可 replay / monitorable
2. **4 层记忆的职责分离**（semantic / episodic / **structural** / **parameter**）—— 尤其是 parameter memory（将权重差分作为 memory 处理）是独特的
3. **6 stage FullSense Loop**（Salience → Curiosity → Inner Monologue → Ego/Altruism → Action Plan → Output Bus）—— 带有心理学根据的 6 段模型
4. **Multi-track Filter Architecture A-1.5**（按 EpistemicType 切换 track）—— 在 FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC 间切换 filter chain
5. **Approval Bus 内嵌于 Loop** —— 将 HITL 带到 architecture level，可经 SQLite ledger replay
6. **TRIZ 40 原理作为 mutation policy 内置**（FR-23〜27）—— Contradiction Detector + Principle Mapper + RAD-Backed Idea Generator + 9-Window + ARIZ
7. **Cognitive Factor Framework (CFF) —— 将 10 因子分解为 policy** —— planner / memory / critic / evolution / trace 的 5 policy
8. **Brief API —— 作为结构化 work unit 的 primitives** —— frozen + ledger + Approval Bus + Governance Scorer built-in

### 与既有相关研究的定位

| 既有系 | 重叠范围 | llive 的差别化 |
|---|---|---|
| MemGPT / LongMem | 层级记忆 | 4 层分离 + phase transition + 签名 zone |
| AutoML-Zero / NAS-LLM | 结构搜索 | 形式验证 gate + multi-precision shadow + 失败数据化 |
| Self-Refine / Reflexion | 自我批评 | online/offline 分离 + llove TUI HITL staging |
| MERA / ModularLLM | 模块化 | 可变长 BlockContainer YAML + plugin registry |
| AutoGPT 系 | agent | llmesh 工业 IoT 直连 + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | 10 因子明示分解 + 认知 OS positioning |

### 结论

> **llive 不是 LLM，而是内置 LLM 的"认知 OS"**

8 要素的组合 × 职责分离 × 心理因子映射，与任何相关研究都不一致。

### 对"LLM 本身是否有所改变"的回答

在 Phase 1〜v0.6 中不触碰 LLM 权重（frozen）。这是设计判断：
- 最优先 replay 可能性
- 使学习轨迹保持 monitorable
- 能直接吸收 LLM 提供方（Qwen, Meta, Mistral）的更新

Phase 8 (CABT) 计划经由 forward hook 注入 attention bias。完全独立的 LLM 构建（LoRA training / distillation）放在 Phase 11+。

详情: [09_llive_structure_originality.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md)

---

## 10. 脱离 Qwen 依赖的 5 个阶段 (ORG-FX 战略 A)

用户观察：

> 没有差别化就没有研究价值。会变成"还不如用普及的 AI"。

### 当前差别化的分层分析

| 层 | llive 独特性 | Qwen 依赖度 |
|---|---|---|
| 输入 (Brief API) | ★★★★★ | 0% |
| Grounder (TRIZ × RAD) | ★★★★★ | 0% |
| 6 stage Loop | ★★★★☆ | 10% |
| 4 层记忆 | ★★★★☆ | 0% |
| Multi-track Filter | ★★★★☆ | 0% |
| Approval Bus | ★★★★★ | 0% |
| Governance Scoring | ★★★★★ | 0% |
| Trace Graph (Ledger) | ★★★★☆ | 0% |
| **LLM 核心 (Decoder-only Transformer)** | ☆ | **100%** ← 问题 |

### 5 阶段路线图

```
Stage A (短期, 〜3 ヶ月)
  ├ LLM コアは凍結
  ├ 周辺差別化を最大化
  └ CABT forward hook / MATH-08 / CREAT-01 で「LLM を使わない層」を厚く

Stage B (中期 1, 3〜6 ヶ月)
  ├ LoRA で llive 用 specialised adapter
  ├ RTX 3090 級で訓練可
  └ Attention に memory bias 注入

Stage C (中期 2, 6〜12 ヶ月)
  ├ Distillation: qwen2.5:14b → llive-7b
  ├ 学習データ: RAD 49 分野 + ledger 成功例 + TRIZ 出力
  └ Multi-track sub-network (EpistemicType 別)

Stage D (長期 1, 1〜2 年)
  ├ Transformer block を memory-coupled に置換
  ├ Cognitive Block Replacement (CABT-01〜07 本実装)
  └ Approval-native decoding

Stage E (長期 2, 2〜3 年)
  ├ Transformer 以外の LLM コア (Mamba / RWKV / Hyena / RetNet)
  ├ Surprise-native pretraining (Bayesian Surprise を loss に)
  └ TRIZ-guided architecture search (AutoML-Zero + TRIZ)
```

### 8 个 ORG-* FR

| FR | 名称 | Stage |
|---|---|---|
| ORG-06 | Provenance-aware tokens | B+D |
| ORG-02 | Memory-coupled inference | C/D |
| ORG-03 | Multi-track sub-network | C |
| ORG-08 | llive-specialized small model | C |
| ORG-07 | Approval-native decoding | C/D |
| ORG-01 | Cognitive Block Replacement | D |
| ORG-04 | TRIZ-guided architecture search | D |
| ORG-05 | Surprise-native pretraining | E |

### 3 个评价指标

- **Architectural Originality Score (AOS)** = 差别化 FR 实现数 / 全 FR 数（当前 ~60%, 目标 ≥85%）
- **LLM Core Independence Ratio (LCIR)** = llive 专用 inference path / 全 inference path（当前 0%, 目标 Stage C 达到 ≥50%）
- **Replaceability Test** = 抽掉 Qwen 是否仍能运行（Stage E 达到 ✅）

### 长期可论文化的候选

- "**Cognitive Block Replacement**: Memory-coupled Transformer for Verifiable Agent Loops"
- "**Provenance-aware Attention**: Trust Score as Inductive Bias"
- "**Surprise-native Pretraining**: Bayesian Surprise as Loss Function"
- "**TRIZ-guided Neural Architecture Search**: 40 Principles for Network Mutation"

以能通过 ICML / NeurIPS / ICLR / AAAI 的研究品质为目标。

详情: [10_qwen_divergence_strategy.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md)

---

## 11. 与 Qwen 相互补充的 llive —— 在 Local 环境填补 5 个隙间 (战略 B)

用户观察：

> 以相互补充的关系为目标也行。llive 原本就是设想在 Local 环境运行的。能把隙间巧妙地插补上就好了。

### 二层结构

```
路線 1: 常設の補完戦略 (Local 環境特化)
       └ Qwen / Llama が進化しても不変の価値
路線 2: 研究としての独自化 (ORG-FX 5 段階)
       └ 中長期で研究価値を持続

両者は同時並走可能
```

### 5 个隙间

#### 隙间 1：数值计算・符号操作・形式验证

| Qwen 的弱点 | llive 的补充 |
|---|---|
| 算错 `(2.5 * 7.8) / 0.3` | **MATH-08 SafeCalculator** |
| `5 m/s + 3 s = 8`（量纲错误） | **MATH-01 SI 量纲分析** |
| `(x+1)² = x² + 2x`（符号幻觉） | **MATH-02 Sympy 验算 + EVO-04 Z3** |
| 捏造 CODATA 值 | **MATH-05 物理常数辞典** |

#### 隙间 2：长期记忆・经验再生

| Qwen 的弱点 | llive 的补充 |
|---|---|
| context window (32K-128K) 的极限 | **4 层记忆** |
| 无法跨 session 记忆 | **persistent memory** + provenance |
| 重复相同的错误 | **Failed Reservoir** (EVO-06) + Reverse-Evo Monitor (EVO-07) |
| 忘记"自己以前说过什么" | **append-only ledger** |

#### 隙间 3：行动审计・责任所在

| Qwen 的弱点 | llive 的补充 |
|---|---|
| 危险动作无 architectural gate | **Approval Bus** + Policy + SQLite Ledger |
| 输出责任难以追踪 | **Provenance chain** + SHA-256 audit chain |
| 无 dangerous tokens 过滤 | **GovernanceScorer**（4 轴 scoring） |
| 审计日志为临时性 | **persistent JSONL + replay** 可 |

#### 隙间 4：认知结构・多视角・矛盾解决

| Qwen 的弱点 | llive 的补充 |
|---|---|
| 视野狭窄（被最初的候选拖着走） | **CREAT-01 KJ法节点**（扩散 强制 ≥20 件） |
| 思考浅薄（1 层展开） | **CREAT-02 MindMap**（DFS depth=3） |
| 偏向乐观 | **CREAT-04 Six Hats**（强制 cautious 观点） |
| 依赖既有模式 | **CREAT-05 Synectics**（异分野类比） |
| 无法处理矛盾 | **TRIZ 40 原理**（FR-23〜27） |

#### 隙间 5：Local 环境特有的约束

| Local 环境的特性 | llive 的应对 |
|---|---|
| 无网络 | **完全 on-prem 运行**（Ollama / LM Studio / vLLM） |
| 个人数据不能外发 | **provenance + Quarantined Zone**（SEC-01） |
| 与计测设备直接连接 | **llmesh sensor bridge**（FR-19, MQTT/OPC-UA） |
| 边缘推理（低规格） | **MATH-08 等确定性层**（不调用 LLM） |
| 隐私（家人对话、医疗信息） | **Local-only ledger** + 零 cloud 发送 |
| 启动时间・通信延迟的约束 | **Brief API 的 overhead < 1 %**（已实测） |

这是 cloud LLM（GPT / Claude / Gemini / Perplexity）**绝对无法重现**的领域。这是 llive 的**不变的差别化轴**。

### 重新框定

> "若单独使用，Qwen 足矣" → **"若要在 Local 环境安全且负责任地使用 Qwen，llive 是最短路径"**

### 对评价基准的启示（今后的改善）

不是"llive vs Qwen"的对立构图，而是**协调 axis**：

- **Hybrid task score**：仅 Qwen vs llive（= Qwen + 确定性补充层）的综合分数
- **Niche task score**：在 Qwen 不擅长的任务上 llive 能补充多少
- **Local capability**：无网络即可完结的 task 的覆盖率
- **Audit completeness**：对输出的 trace coverage

详情: [11_complementary_with_qwen.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md)

---

## 整体总结 —— 一次会话的到达点

### 实现

- **Brief API** (LLIVE-001/002) end-to-end / S1 BriefGrounder / MATH-01/08 / COG-01/02/03
- llive 测试：**1014 PASS / 0 fail / 0 regression**

### 新增需求 (REQUIREMENTS.md)

- v0.7-vertical MATH 8 项（其中 MATH-08 是差别化轴最大）
- v0.8 CABT 7 项（Transformer 块高度化）
- v0.9 CREAT 5 项（KJ法 / MindMap / Six Hats / Synectics）
- v1.0-frame COG-FX 4 项（10 思考因子映射）
- v2.0-core ORG-FX 8 项（脱离 Qwen 依赖的 5 阶段）
- **合计 100 项，Phase 映射完备**

### 基准测试

| 种类 | 单元格数 | 主要观察 |
|---|---|---|
| progressive matrix | 5×3=15 | overhead < 1 %, decision 全 note |
| fair re-bench | 4×6=24（实 OK 12） | llive（LLM attached）比直接调用 ollama 慢 2-4 倍 |
| quiz Debug | 10 | passed 6/10, ms mean 22.3s |
| quiz Release | 10 | passed 7/10, ms mean 22.8s, Debug overhead +1.8% |

### 战略的二层结构

1. **常设的补充战略**（在 Local 环境补充 5 隙间）—— cloud LLM 进化也不变
2. **作为研究的独自化**（ORG-FX 5 阶段）—— Stage A → B → C → D → E

### 教训 —— 作为 TRIZ 矛盾的 honest disclosure

> 在取得基准测试的那一刻就自以为获胜之前，先怀疑基准测试的设计缺陷。

新 memory: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

### GitHub

- llive: <https://github.com/furuse-kazufumi/llive>
- fullsense (umbrella 门户): <https://github.com/furuse-kazufumi/fullsense>
- llove (TUI HITL): <https://github.com/furuse-kazufumi/llove>
- llmesh (LLM hub): <https://github.com/furuse-kazufumi/llmesh>

全部为 **Apache-2.0 + Commercial dual-license**。

### 个别文章链接（详情请见此处）

| # | 标题 | 主题 |
|---|---|---|
| 1 | [Brief API + progressive matrix (overhead < 1 %)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md) | Brief API + 5×3 bench |
| 2 | [用"心理的深层"10 思考因子整理 llive 思考层](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md) | COG-FX 框架 |
| 3 | [擅长数学与单位的 AI —— MATH-01/08](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md) | MATH 系 |
| 4 | [Transformer 块高度化 7 种方法 (CABT 设计预告)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md) | CABT |
| 5 | [用 LLM × KJ法 × MindMap 自动化需求定义 (CREAT 设计预告)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md) | CREAT |
| 6 | [用形式验证 gate 阻止 LLM 数式幻觉 (MATH-02 设计预告)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md) | MATH-02 |
| 7 | [fair bench (honest disclosure 全面改订版)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md) | bench 方法论 |
| 8 | [quiz bench Debug vs Release × mean/stdev](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md) | quiz + 统计 |
| 9 | [llive 结构独特性 8 要素](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md) | 认知 OS positioning |
| 10 | [脱离 Qwen 5 阶段 ORG-FX](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md) | 独自化路线 |
| 11 | [与 Qwen 相互补充 5 隙间](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md) | 补充路线 |

## 结语

llive 并非"LLM 本身"，而是"内置 LLM 的认知 OS"，其设计是在 Local 环境填补 5 个隙间的同时，于中长期有计划地推进 LLM 核心本身的独自化。

我把这作为一份等身大的开发记录留存下来——一天内 32 项需求 + 1014 PASS 实现 + 11 篇公开文章 + 本摘要，其中也包括"在基准测试中怀疑自家产品的 honest disclosure"。

问题、指摘、改善建议请通过 GitHub Issues 或 Twitter / X (@puruyan) 提出。

---

> 本文是与 Claude Opus 4.7 (1M context) 对话的同时执笔的。实现与验证也在同一会话内全部完成。一天内能推进如此规模，是因为认知 OS 牢牢搭建了思考的脚手架。

---

# 한국어

# 하루 만에 요건 32 건 추가 + Brief API + COG-FX + MATH 구현 + 벤치 4 종 — 자기진화형 LLM 프레임워크 llive 개발기 2026-05-17

저자: **후루세 카즈후미（puruyan）**

## 들어가며 — 한 세션에서 무엇을 달성했는가

2026-05-17 의 한 세션 (Claude Opus 4.7 1M context, ccr 경유) 에서 **자기진화형 LLM 프레임워크 [llive](https://github.com/furuse-kazufumi/llive)** 에 대해 다음을 달성했습니다:

| 종류 | 건수 | 내용 |
|---|---|---|
| 요건 (FR) 추가 | **32 건** | v0.7-MATH 8 / v0.8-CABT 7 / v0.9-CREAT 5 / v1.0-COG-FX 4 / v2.0-ORG-FX 8 |
| 구현 (LoC) | ~2,200 줄 | Brief API end-to-end / Grounder / Governance / Trace Graph / MATH 단위 & 계산 |
| 테스트 추가 | **+78 건** | 936 → **1014 PASS / 0 fail / 0 regression** |
| 벤치 4 종 | 15 + 12 + 10 + 10 셀 | progressive matrix / fair bench / quiz Debug / quiz Release |
| 공개 기사 | **11 편 + 본 기사** | [docs/articles/2026-05-17/](https://github.com/furuse-kazufumi/fullsense/tree/main/docs/articles/2026-05-17) |
| GitHub push | 2 리포지토리 | llive `349a234` / fullsense `cb346aa` |

llive 는 **OSS LLM (Qwen / Llama / Mistral) 을 내장하는 "인지 OS"** 라는 포지셔닝입니다. Decoder-only LLM 코어는 frozen 인 채로, 4 층 메모리 + 6 stage Loop + Approval Bus + TRIZ 40 원리 + 10 사고 인자를 통합한 연구개발 프레임워크입니다.

본 기사는 11 편의 개별 기사를 **본문 포함**으로 통합한 것으로, Qiita 단독으로도 통독 가능하도록 작성했습니다. 각 장 말미에 상세 링크도 두었습니다.

---

## 1. Brief API end-to-end (LLIVE-001/002 전 7 step)

### 동기

지금까지 llive 의 `FullSenseLoop.process(Stimulus)` 는 **thinking-evaluator** 였지 **doing-agent** 는 아니었습니다. 외부 클라이언트 (lldesign / lltrade / 계획 중인 llcad/lleda/llchip) 가 "구조화된 work unit" 을 건네는 API 가 없었기 때문입니다.

설계 초안 `docs/proposals/brief_api_design.md` (5 일 견적) 를 한 세션에 완주시켰습니다.

### Brief dataclass

```python
@dataclass(frozen=True)
class Brief:
    brief_id: str                           # ascii word/dash/dot のみ、path-safe
    goal: str                               # 必須
    constraints: tuple[str, ...] = ()
    source: str = "manual"
    priority: float = 0.5                   # [0.0, 1.0]
    epistemic_type: EpistemicType = EpistemicType.PRAGMATIC
    backend: str = ""                       # "ollama:qwen2.5:14b" 等
    tools: tuple[str, ...] = ()             # whitelist
    success_criteria: tuple[str, ...] = ()
    approval_required: bool = True
    ledger_path: Path | None = None
```

**frozen + tuple** 로 hashable / replay-friendly. 같은 Brief 를 ledger・loop・result 가 공유하는 invariant 를 frozen 으로 지킵니다.

### BriefRunner — submit 한 트랜잭션으로 다음을 실행

```
1. brief_submitted          → ledger
2. (optional) grounding_applied (TRIZ × RAD citation)
3. stimulus_built           → ledger
4. FullSenseLoop.process(stim)
   └─ 6 stage loop (既存)
5. loop_completed           → ledger
6. decision                 → ledger
7. (optional) governance_scored (COG-02, 4 軸)
8. Approval Bus gate (PROPOSE/INTERVENE 時のみ)
9. tool_invoked × N         → ledger
10. outcome                 → ledger
```

모두 **append-only JSONL ledger** 에 기록. `meta` envelope 에 timestamp/pid 를 분리하여 replay 시 ignore 할 수 있는 구조.

### CLI

```bash
# YAML から
llive brief submit path/to/brief.yaml

# インライン
llive brief submit --goal "Refactor docs/index.md..." \
                   --brief-id portal-refresh \
                   --priority 0.8 --no-approval

# ledger 検索
llive brief ledger portal-refresh-2026-05-16 --json --limit 5
```

### MCP

`submit_brief` tool 이 추가되어 Claude Desktop / Cursor 등에서 llive 에 작업을 건넬 수 있습니다:

```jsonc
{
  "name": "submit_brief",
  "input_schema": {
    "type": "object",
    "required": ["goal"],
    "properties": {
      "goal": {"type": "string"},
      "constraints": {"type": "array", "items": {"type": "string"}},
      "priority": {"type": "number", "minimum": 0.0, "maximum": 1.0},
      "approval_required": {"type": "boolean", "default": true}
    }
  }
}
```

### Progressive validation matrix (5×3 = 15 셀)

xs/s/m/l/xl × {llama3.2:3b, qwen2.5:7b, qwen2.5:14b} 을 on-prem only 로 실주행 (cloud 혼재 금지, `feedback_llive_measurement_purity` 규칙):

#### Wall-time matrix (ms)

| model | xs (cold) | s | m | l | xl (timeout) |
|---|---|---|---|---|---|
| llama3.2:3b | 8,908 | 43,978 | 89,484 | 458,400 | 1,202,282 ⌛ |
| qwen2.5:7b | 59,447 | 94,158 | 122,134 | 722,867 | 1,202,104 ⌛ |
| qwen2.5:14b | 121,560 | 122,160 | 122,160 | 1,202,263⌛ | 1,202,199 ⌛ |

#### LLM-only / Wall

전 15 셀에서 **> 99.8 %** — Brief API + loop 의 추가 비용은 ~1 % 미만.

#### Loop decision

| model \ size | xs | s | m | l | xl |
|---|---|---|---|---|---|
| llama3.2:3b | note | note | note | note | note |
| qwen2.5:7b | note | note | note | note | note |
| qwen2.5:14b | note | note | note | note | note |

**전 15 셀 `note`** — loop 의 결정 트리가 token 압력에 대해 완전 stable.

### 사고층과의 접속

- `Brief.epistemic_type` 로 Multi-track Filter 의 chain 을 선택
- `Brief.priority` 가 Stimulus.surprise 가 되어 Salience Gate 에 영향
- `Brief.constraints` 는 augmented goal 로서 thought 에 주입
- `Brief.tools` whitelist 로 BriefRunner 의 tool 실행을 제한
- `Brief.approval_required` 로 C-1 Approval Bus 를 경유

상세: [01_brief_api_progressive.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md)

---

## 2. 심리의 심층 10 사고 인자로 정리하는 llive 사고층 — 9/10 구현됨

### 출처

YouTube 채널 "심리의 심층" 에서 추출된 인간의 사고 인자 세트. 사용자가 목적을 "심층 심리의 설명" 이 아니라 **"재사용 가능한 사고 인자의 추출 → LLM 의 추론・계획・자기개선・에이전트 설계에의 통합"** 으로 명시 전환하여 요건화했습니다.

### 10 인자 × llive 매핑

| # | 인자 | LLM 역할 | llive 기존 (구현됨) | 추가 (2026-05-17 구현) |
|---|---|---|---|---|
| 1 | **구조화** | 과제를 분해 | Brief constraints, Salience+Curiosity gate | — |
| 2 | 재구성 | 대안 생성 | TRIZ 40 원리 + ARIZ + 9 화법 (FR-23〜27) | (CREAT-01 계획) |
| 3 | **폐루프** | 검증 계획을 동반 | BriefRunner (submit→plan→approval→tool→outcome) | — |
| 4 | 자기확장 | 외부 자원을 사용 | 4 층 메모리 + RAD 49 분야 + tools whitelist | MATH-08 계산 엔진 |
| 5 | **불확실성** | 가설과 사실을 분리 | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | 탐색 | 미답 안을 시도 | EVO-* (Z3 + Failed Reservoir + Reverse-Evo) | — |
| 7 | **정합** | 전체 제약으로 재평가 | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | **내력** | 판단 이력을 남김 | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | 다시점 | 평가 함수를 분리 | Multi-track Filter A-1.5 (5 EpistemicType) | (COG-04 + CREAT-04 계획) |
| 10 | 현실 접속 | 실환경 제약을 다룸 | (Phase 4 INT-01〜04 계획 중) | — |

### v1.0 필수 5 인자 (굵은 글씨) 는 모두 구현됨

사용자 관찰: **"탐색 / 재구성을 강화하기 전에, 구조화 / 불확실성 / 폐루프 / 정합 / 내력의 토대가 필요하다"**. 이것이 없는 상태에서 탐색 인자나 재구성 인자를 강하게 하면, 흥미로운 안은 늘지만 오차・폭주・비재현성도 늡니다.

| 인자 | 구현 위치 |
|---|---|
| 구조화 | `src/llive/brief/types.py::Brief` + loop._salience_gate/curiosity_drive |
| 폐루프 | `src/llive/brief/runner.py::BriefRunner.submit` |
| 불확실성 | `src/llive/learning/bayesian_surprise.py` (FR-21) + COG-01 |
| 정합 | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py` (EVO-04) + COG-02 |
| 내력 | `src/llive/memory/provenance.py` + ledger × 3 + COG-03 |

### COG-01〜03 의 구현

#### COG-01 Triple Output

`BriefResult` 에 **confidence / assumptions / missing_evidence** 의 3 열을 추가:

```python
@dataclass
class BriefResult:
    # 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` 가 결정론적으로 산출:

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`: grounder 부재 / success_criteria 부재를 명문화
- `missing_evidence`: TRIZ 원리가 surface 되지 않음 / tool 실패를 저장

#### COG-02 Governance Scoring Layer

Approval Bus 의 **전단** 에 4 축 스코어러를 삽입:

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block
```

책무 분리:
- **Governance** = scoring (왜 좋은가/나쁜가)
- **Approval Bus** = gating (실행 가부의 판단)

dangerous_token 검출 (`rm -rf` / `DROP TABLE` / `format c:` 등), INTERVENE-without-approval 페널티, `block_threshold` / `safety_floor` 를 지원.

#### COG-03 Trace Graph

`BriefLedger.trace_graph()` 가 3 층 view 를 반환:

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

이로써 디버그・자기개선・실패 분석・evolution 으로의 학습 데이터 추출이 기계적으로 가능해집니다.

상세: [02_cognitive_factors.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md)

---

## 3. 수학・단위에 강한 AI 로의 첫걸음 — MATH-01/08

llive 의 최초 vertical specialisation 은 "수학・단위 특화 AI". 범용 LLM 이 약한 다음을 **"LLM 에게 계산시키지 않는" 결정론적 사이드카** 로 극복합니다.

### LLM 의 수학적 약점

| 관점 | 범용 LLM 의 약점 | llive 기존 자산과의 합치 |
|---|---|---|
| 기호 조작의 환각 | `x² + x = 2x³` 같은 오등식 | EVO-04 Z3 정적 검증으로 gate |
| 단위 차원 | `5 m/s + 3 s = 8` | SI 차원 해석 엔진 (MATH-01) |
| 수치 정밀도 | float 연산 오차를 무시 | error propagation tracking (MATH-04) |
| 공리 체계 | 암묵적 전제를 혼입 | EpistemicType=MATHEMATICAL 의 strict track |
| 인용의 신뢰성 | "CODATA value is X" 라고 적당히 답함 | RAD math/metrology + provenance |

### MATH-01 — SI 7 기본 단위 + 파생 단위의 차원 대수

```python
from llive.math import Quantity, parse_unit, UnitMismatchError

# 速度 + 時間 = 不可能 (典型的 LLM 幻覚を必ず止める)
v = Quantity(5.0, parse_unit("m/s"))
t = Quantity(3.0, parse_unit("s"))
try:
    bad = v + t
except UnitMismatchError as e:
    print(f"refused: {e}")

# 速度 × 時間 = 距離 (m)
d = v * t
assert d.dimensions.matches(parse_unit("m"))

# 力 × 距離 = エネルギー (J)
F = Quantity(10.0, parse_unit("N"))
d = Quantity(5.0, parse_unit("m"))
E = F * d
assert E.dimensions.matches(parse_unit("J"))  # ✓
```

구현의 핵심은 `Dimensions(m, kg, s, A, K, mol, cd)` 의 7 차원 벡터. `Quantity.__add__` 에서 차원 검산 → 불일치는 **반드시 raise**.

파생 단위: `N` (kg·m/s²) / `J` (kg·m²/s²) / `W` (kg·m²/s³) / `Pa` (kg/m/s²) / `Hz` (1/s) / `C` (s·A) / `V` (kg·m²/s³/A) / `ohm` 을 빈출 범위만 구현.

### MATH-08 — 내장 계산 엔진 (차별화 축 최대)

**설계의 핵심**: LLM 에게 **수치 계산을 시키지 않는다**.

```python
from llive.math import SafeCalculator, extract_expressions

calc = SafeCalculator()
brief_text = "Compute (2.5 * 7.8) / 0.3 then verify sqrt(16) is exact."

for expr in extract_expressions(brief_text):
    r = calc.evaluate(expr)
    print(f"{r.expression} = {r.value}  (ops={r.operation_count}, fns={r.used_functions})")
# (2.5 * 7.8) / 0.3 = 65.0   (ops=2, fns=())
# sqrt(16)          = 4.0    (ops=1, fns=('sqrt',))
```

#### Safety 의 의미

- `eval()` 은 사용하지 않음 (임의 코드 실행 회피)
- AST visitor 로 허가 노드 (`BinOp` / `UnaryOp` / `Constant` / `Call` to whitelist) 만 통과
- 함수 whitelist: `sqrt` / `sin` / `cos` / `log` / `abs` / `mean` 등 28 함수 (math + statistics 모듈)
- 상수 whitelist: `pi` / `e` / `tau` / `inf` / `nan`
- 0 나눗셈은 `CalculationError` 로 안전하게 reject
- `__import__('os').system('rm')` 같은 공격을 **attribute access 단계에서 reject**

### 왜 Wolfram Alpha 보다 좋은가

- Wolfram Alpha: 강력하지만 closed cloud, 상용, 유료
- MATH: 완전 on-prem (Z3 + Sympy 는 오픈소스), 감사 로그 부착, BriefLedger 에 고정 기록
- 수학・물리・공학・금융・약학 의 모두가 "수식의 정확성" 을 요구 → llive 의 vertical 전략의 핵심

### v0.7-vertical MATH 전 8 건

| FR | 이름 | 우선 |
|---|---|---|
| MATH-01 | SI 단위 차원 해석 엔진 | ✅ 구현됨 |
| MATH-02 | Z3 / Sympy 통합 검증층 | 2nd |
| MATH-05 | 물리 상수 사전 (CODATA 2022 + NIST) | 3rd |
| **MATH-08** | **내장 계산 엔진 (차별화 축)** | ✅ 구현됨 |
| MATH-03 | 수식 구문 해석 (LaTeX/MathML/Sympy AST) | MED |
| MATH-04 | 수치 계산 정밀도 트래킹 (IEEE 754) | MED |
| MATH-06 | 단위 변환 + Buckingham π 무차원화 | MED |
| MATH-07 | MATHEMATICAL EpistemicType | MED |

상세: [03_math_vertical.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md)

---

## 4. CABT 설계 예고 — Transformer 블록을 고도화하는 7 접근

사용자 지시 "Transformer 구조는 심플하지만 각 블록에서 더 고도한 것을 할 수 있다" + "매트릭스를 참조 기반 재배열로 치환하고 부가 정보를 갖게 한다" + "llive 독자의 사고층과 친화성이 높은 것으로" 를 기술 설계로 옮긴 것입니다.

### 설계 동기

![CABT: attention 치환 안](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/summary/cabt_attention_ko.svg)

### Hook 설계 (가중치 동결인 채로)

```python
# src/llive/cabt/hooks.py (S2 で実装予定)
class ReferenceAttentionHook:
    def _on_attention(self, module, inputs, outputs):
        attn_output = outputs[0]  # [batch, seq, hidden]
        bias = self._metadata_provider(attn_output)  # provenance/trust/...
        return (attn_output + self._strength * bias, *outputs[1:])
```

### 6 열 metadata

| 열 | 유래 |
|---|---|
| provenance_id | `memory/provenance.py` 의 레코드 ID |
| trust_score | Quarantined Memory 의 trust 값 [0,1] |
| epistemic_type | FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC + RESERVED |
| timestamp_norm | 시계열 정규화 [0,1] |
| source_domain_id | RAD 49 분야의 ID |
| surprise_score | BayesianSurpriseGate (FR-21) 의 출력 |

### 7 개의 CABT FR

| FR | 역할 | llive 사고층과의 접속 |
|---|---|---|
| CABT-01 | Reference-based Attention with Metadata | 사용자 직접 제안 |
| CABT-02 | Stage-aware Block Routing | FullSense 6 stage 연동 |
| CABT-03 | Epistemic-typed Token Pool | Multi-track Filter A-1.5 의 token 화 |
| CABT-04 | Salience-gated Attention | FR-21 surprise gate 동기 |
| CABT-05 | TRIZ-conditioned Head Selection | BriefGrounder citation 연계 |
| CABT-06 | Approval-gated Decoding | C-1 Approval Bus 를 decoder 내 확장 |
| CABT-07 | Memory-augmented Residual | 4 층 메모리를 residual 에 주입 |

상세: [04_next_cabt_block_design.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md)

---

## 5. CREAT 설계 예고 — LLM × KJ법 × MindMap 으로 요건 정의를 자동화

사용자 관찰 "인간의 사고 흐름은 KJ법 / MindMap / TRIZ 등을 거쳐 요건 정의에 들어간다" 를 기술 설계로 옮긴 것.

### 인간의 사고 플로우 vs llive

![인간의 사고 흐름 ↔ llive 매핑](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/summary/creat_thinking_flow_ko.svg)

### 5 개의 CREAT FR

| FR | 이름 | 효과 |
|---|---|---|
| CREAT-01 | KJ법 노드 (LLM mixture sampling + clustering) | 시야 협착을 방지 (≥20 후보를 강제) |
| CREAT-02 | MindMap 노드 (DFS depth=3) | 사고의 얕음을 방지 (깊이를 강제) |
| CREAT-03 | 구조화 변환 (4 출력을 요건 spec 으로 통합) | Brief → 자동 REQUIREMENTS.md 생성 |
| CREAT-04 | Six Hats Multi-track | 편향된 낙관을 방지 (cautious 관점을 강제) |
| CREAT-05 | Synectics 유추 엔진 (cross-domain RAD bridge) | 기존 패턴 의존을 방지 (이분야 유추를 강제) |

상세: [05_next_creat_kj_mindmap.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md)

---

## 6. MATH-02 설계 예고 — 형식 검증 게이트로 LLM 수식 환각을 멈춘다

### SafeCalculator (MATH-08, 구현됨) 로는 막을 수 없는 환각

| 환각 타입 | SafeCalculator 로 막을 수 있는가? |
|---|---|
| `(2.5 * 7.8) / 0.3 = 12.4` (실제는 65.0) | ✅ |
| `5 m/s + 3 s = 8` | ✅ (MATH-01 로) |
| `(x+1)² = x² + 2x` (2x 가 아니라 2x+1) | ❌ — **MATH-02 의 대상** |
| `lim x→0 sin(x)/x = 0` (실제는 1) | ❌ — Sympy 필요 |
| `det([[1,2],[3,4]]) = 0` (실제는 -2) | ❌ — Sympy 필요 |
| `e^(iπ) + 1 = 2` (실제는 0) | ❌ — Sympy 필요 |

### 설계

```
LLM 出力テキスト
    │
    ▼
[式抽出器] (MATH-03 multi-syntax parser)
    │
    ▼
[Sympy AST]
    │
    ├─→ simplify(lhs - rhs) == 0 ? → ✅ 通過
    │   ❌ → 失敗 flag
    │
    └─→ Z3 で satisfiability check (∀ x. lhs(x) == rhs(x) ?)
        ❌ → 反例を ledger に記録
```

```python
checker = FormalChecker()
verdict = checker.check_equation("(x+1)**2", "x**2 + 2*x")
# verdict.satisfied: False
# verdict.counterexample: {"x": 0}
# verdict.rationale: "differs at x=0: 1 vs 0"
```

### EVO-04 (기존 Z3) 의 연장선

- EVO-04: "mutation 후의 sub-block 이 ABI 제약을 충족하는가" 를 Z3 로 검증
- MATH-02: "LLM 이 내놓은 등식이 충족해야 할 추론 스텝을 Z3 로 검증"

같은 Z3 layer 의 수식판. Phase 3 자산으로 확장하는 경제적 설계.

상세: [06_next_math02_formal_gate.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md)

---

## 7. Fair benchmark 의 함정 — honest disclosure 의 중요성

### 최초의 벤치에서 "비정상적으로 빠른" 결과

`bench_run.py` 로 `--all` (4 brief × 6 model) 을 실행했더니:

```
brief model       status      ms   chars
b1    llive       OK         152     884
b1    ollama      OK       18812     148
b1    perplexity  OK        4555     192
```

llive 134-184ms 로 4/4 OK, cloud LLM 이나 ollama 보다 압도적으로 빠른 숫자가 나왔습니다.

사용자 지적:

> 이상하게 빠르네요, 응답에 뭔가 이상한 부분은 없나요?

### 확인된 이상 3 건

#### 이상 1: LLMBackend 미 attach

`run_brief.py` 가 `FullSenseLoop(sandbox=True)` 를 LLM backend 없이 구축 → loop 의 `_inner_monologue` 가 **template 경로** (rule-based) 로 떨어지고, 출력은:

```
Observation about 'manual': <brief content[:120]> — novel territory, worth exploring.
```

전 brief 에서 같은 템플릿 구조, brief 의 **선두 120 문자** 만 thought 에 삽입.

#### 이상 2: chars 가 JSON 전체 길이

`bench_run.py::chars = len(p.stdout)`:
- llive: JSON 구조 (stim metadata + stages + plan + raw) 가 dominant → 884 chars
- ollama / perplexity: LLM 응답 텍스트 그 자체 → 148〜1733 chars

즉 llive 4/4 에서 `884 chars` 동일한 것은 "같은 JSON 구조를 뱉었기 때문".

#### 이상 3: 134-184ms 는 subprocess RTT

- py launcher 기동 + Python interpreter import (~80-120ms)
- `FullSenseLoop.process()` 의 6 stage 를 template 경로로 빠져나감 (~10-30ms)
- JSON 출력 (~1ms)
- subprocess wait + stdout 읽기 (~10-30ms)

합계 134-184ms = LLM 추론 레이턴시가 아님.

### 수정 — Fair contract

`run_brief.py` 에 `--backend ollama:qwen2.5:14b` 등을 건넬 수 있는 인자를 추가하고, `bench_run.py::run_llive` 가 `BENCH_LLIVE_BACKEND` env (default `ollama:qwen2.5:14b`) 를 반드시 지정하도록.

```python
def run_llive(brief: str, _keys: dict) -> tuple[bool, str, float]:
    backend = os.environ.get("BENCH_LLIVE_BACKEND", "ollama:qwen2.5:14b")
    debug_flag = os.environ.get("BENCH_LLIVE_DEBUG", "0") == "1"
    cmd = ["py", "-3.11", "llive/scripts/run_brief.py",
           "--json", "--backend", backend]
    if debug_flag:
        cmd.append("--debug")
    cmd.append(brief)
    # ...
    # chars は stages.thought.text から取得 (JSON 全長ではなく LLM 出力本体)
```

### Fair 재주행 결과

| brief | llive (+llama3.2:3b) | ollama 직접 호출 | perplexity |
|---|---|---|---|
| b1 | **32,750 ms** | 12,423 ms | 2,411 ms |
| b2 | **50,936 ms** | 13,024 ms | 3,591 ms |
| b3 | **43,787 ms** | 19,610 ms | 2,104 ms |
| b4 | **43,163 ms** | 21,936 ms | 6,162 ms |

llive (LLM attached) 는 ollama 직접 호출의 **2-4 배 느림**. 차이는 `build_llm_prompt` 가 브리프를 `_inner_monologue` 용으로 래핑하여 장문화시키는 것.

### 교훈 (TRIZ 모순으로서의 기록)

> 벤치에서 자사가 비정상적으로 빠른 결과가 나오면, 이긴 기분이 되기 전에 반드시 다음을 확인:
> 1. LLM 추론 레이어가 실제로 호출되고 있는가
> 2. 계측 시간에 subprocess 기동 / JSON serialize 등의 RTT 가 섞여 있지 않은가
> 3. 응답 길이 (chars) 의 지표는 같은 단위로 측정되었는가
> 4. 응답 내용이 brief 내용을 실질적으로 반영하고 있는가

memory: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

### llive 의 부가가치 재정의

**llive 의 부가가치는 속도가 아니라 구조** (ledger / approval / governance / grounding / 6 stage trace) 에 있다. 속도만으로 판단한다면 ollama 직접 호출 쪽이 낫다.

상세: [07_bench_results.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md)

---

## 8. Quiz bench — Debug vs Release × mean/stdev

사용자 지시 "DebugMode 와 Release 판으로 벤치마크 테스트" + "퀴즈 형식 + 평균값・분산값" 을 반영.

### Quiz set v1 (10 문제 × 5 카테고리 × 2 난이도)

| id | category | difficulty |
|---|---|---|
| arith-01/02 | arithmetic | easy / medium |
| logic-01/02 | logic | easy / medium |
| knowledge-01/02 | knowledge | easy / medium |
| reason-01/02 | reasoning | easy / medium |
| creative-01/02 | creativity | easy / medium |

채점: keyword 일치 (`keyword_match` / `keyword_all` / `keyword_any` / `keyword_*_soft`).

### bench_quiz.py 에 통계 열을 추가

```python
import statistics as _stat

partials = [c.get("partial_score", 0.0) for c in ok_cells]
mss = [c.get("ms", 0.0) for c in ok_cells]
p_mean = sum(partials) / len(partials) if partials else 0.0
p_std = _stat.stdev(partials) if len(partials) > 1 else 0.0
m_mean = sum(mss) / len(mss) if mss else 0.0
m_std = _stat.stdev(mss) if len(mss) > 1 else 0.0
```

### 결과 (llama3.2:3b × 10 quiz × {debug, release})

| mode | passed | partial mean | partial stdev | ms mean | ms stdev | wall sum |
|---|---|---|---|---|---|---|
| Debug | 6/10 | 0.550 | 0.497 | **22,343** | 5,790 | 223.4 s |
| Release | 7/10 | 0.650 | 0.474 | **22,750** | 8,356 | 227.5 s |

### 관찰

1. **Debug overhead 는 +1.8 % 로 실질 제로** → 개발 시 debug=True 상시 ON 이어도 성능 페널티 없음
2. 정답률의 차이 (6/10 vs 7/10) 는 **확률 변동의 범위** (N=10 에서는 이항검정으로 p > 0.5)
3. ms stdev 가 release 에서 큼 (LLM 추론 시간이 문제 의존으로 변동)

### 개별 quiz 결과의 샘플

| quiz | debug | release |
|---|---|---|
| arith-01 (easy) | ❌ 0.0 18.6s | ✅ 1.0 39.7s |
| arith-02 (medium) | ❌ 0.0 33.1s | ❌ 0.0 17.8s |
| logic-01 (easy) | ✅ 1.0 18.3s | ✅ 1.0 17.4s |
| logic-02 (medium) | ✅ 0.5 21.6s | ✅ 0.5 33.1s |
| knowledge-01 (easy) | ❌ 0.0 28.9s | ❌ 0.0 19.7s |
| knowledge-02 (medium) | ✅ 1.0 20.2s | ✅ 1.0 19.4s |
| reason-01 (easy) | ✅ 1.0 17.9s | ✅ 1.0 17.7s |
| reason-02 (medium) | ❌ 0.0 19.3s | ❌ 0.0 19.5s |
| creative-01 (easy) | ✅ 1.0 29.1s | ✅ 1.0 29.4s |
| creative-02 (medium) | ✅ 1.0 16.6s | ✅ 1.0 13.8s |

### 다음 개선

- **N ≥ 30** 으로 각 model 평가 (현재 N=10)
- 복수 model 병렬 (llama3.2:3b / qwen2.5:7b / qwen2.5:14b)
- seed 고정 (`OLLAMA_SEED`) 으로 재현성 확보
- LLM-as-judge 에서의 2 차 채점
- 동일 문제를 3 회 샘플링하여 per-quiz mean/stdev

상세: [08_quiz_bench_debug_vs_release.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md)

---

## 9. llive 의 구조는 LLM 으로서 독자적인가? — 8 요소의 점검

사용자의 물음: "llive 의 구조란, LLM 으로서 독자적인 구조가 되어가고 있나요?"

### 8 개의 차별화 요소

1. **Decoder-only LLM 코어는 동결 + 주변에서 능력 확장** — 가중치를 갱신하지 않음으로써 replay 가능 / monitorable 한 학습 궤적
2. **4 층 메모리의 책무 분리** (semantic / episodic / **structural** / **parameter**) — 특히 parameter memory (가중치의 차분을 memory 로서 다루는 것) 가 독자적
3. **6 stage FullSense Loop** (Salience → Curiosity → Inner Monologue → Ego/Altruism → Action Plan → Output Bus) — 심리학적 근거가 있는 6 단 모델
4. **Multi-track Filter Architecture A-1.5** (EpistemicType 에 의한 track 전환) — FACTUAL/EMPIRICAL/NORMATIVE/INTERPRETIVE/PRAGMATIC 로 filter chain 을 전환
5. **Approval Bus 를 Loop 내에 내장** — HITL 을 architecture level 로, SQLite ledger 로 replay 가능
6. **TRIZ 40 원리를 mutation policy 로서 내장** (FR-23〜27) — Contradiction Detector + Principle Mapper + RAD-Backed Idea Generator + 9-Window + ARIZ
7. **Cognitive Factor Framework (CFF) — 10 인자를 policy 분해** — planner / memory / critic / evolution / trace 의 5 policy
8. **Brief API — 구조화 work unit 이라는 primitives** — frozen + ledger + Approval Bus + Governance Scorer built-in

### 기존 유사 연구와의 위치 설정

| 기존계 | 겹치는 범위 | llive 의 차별화 |
|---|---|---|
| MemGPT / LongMem | 계층 메모리 | 4 층 분리 + phase transition + 서명 zone |
| AutoML-Zero / NAS-LLM | 구조 탐색 | 형식 검증 gate + multi-precision shadow + 실패 데이터화 |
| Self-Refine / Reflexion | 자기비평 | online/offline 분리 + llove TUI HITL staging |
| MERA / ModularLLM | 모듈화 | 가변장 BlockContainer YAML + plugin registry |
| AutoGPT 계 | 에이전트 | llmesh 산업 IoT 직결 + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | 10 인자 명시 분해 + 인지 OS positioning |

### 결론

> **llive 는 LLM 이 아니라, LLM 을 내장하는 "인지 OS"**

8 요소의 조합 × 역할 분리 × 심리 인자 매핑은 유사 연구의 어느 것과도 일치하지 않는다.

### "LLM 자체는 무언가 바꾸고 있는가" 에 대한 답

Phase 1〜v0.6 에서는 LLM 가중치는 건드리지 않는다 (frozen). 이것은 설계 판단:
- replay 가능성을 최우선
- 학습 궤적을 monitorable 로 유지
- LLM 제공처 (Qwen, Meta, Mistral) 의 갱신을 직접 받아들일 수 있음

Phase 8 (CABT) 에서 forward hook 에 의한 attention bias 주입을 계획. 완전한 독자 LLM 구축 (LoRA training / distillation) 은 Phase 11+ 에서.

상세: [09_llive_structure_originality.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md)

---

## 10. Qwen 의존에서 이탈하는 5 단계 (ORG-FX 전략 A)

사용자 관찰:

> 차별화되어 있지 않으면 연구의 가치가 없다. 보급되어 있는 AI 를 쓰는 편이 낫다는 식이 될 것 같다.

### 현상의 차별화의 층별 분석

| 층 | llive 독자성 | Qwen 의존도 |
|---|---|---|
| 입력 (Brief API) | ★★★★★ | 0% |
| Grounder (TRIZ × RAD) | ★★★★★ | 0% |
| 6 stage Loop | ★★★★☆ | 10% |
| 4 층 메모리 | ★★★★☆ | 0% |
| Multi-track Filter | ★★★★☆ | 0% |
| Approval Bus | ★★★★★ | 0% |
| Governance Scoring | ★★★★★ | 0% |
| Trace Graph (Ledger) | ★★★★☆ | 0% |
| **LLM 코어 (Decoder-only Transformer)** | ☆ | **100%** ← 문제 |

### 5 단계 로드맵

```
Stage A (短期, 〜3 ヶ月)
  ├ LLM コアは凍結
  ├ 周辺差別化を最大化
  └ CABT forward hook / MATH-08 / CREAT-01 で「LLM を使わない層」を厚く

Stage B (中期 1, 3〜6 ヶ月)
  ├ LoRA で llive 用 specialised adapter
  ├ RTX 3090 級で訓練可
  └ Attention に memory bias 注入

Stage C (中期 2, 6〜12 ヶ月)
  ├ Distillation: qwen2.5:14b → llive-7b
  ├ 学習データ: RAD 49 分野 + ledger 成功例 + TRIZ 出力
  └ Multi-track sub-network (EpistemicType 別)

Stage D (長期 1, 1〜2 年)
  ├ Transformer block を memory-coupled に置換
  ├ Cognitive Block Replacement (CABT-01〜07 本実装)
  └ Approval-native decoding

Stage E (長期 2, 2〜3 年)
  ├ Transformer 以外の LLM コア (Mamba / RWKV / Hyena / RetNet)
  ├ Surprise-native pretraining (Bayesian Surprise を loss に)
  └ TRIZ-guided architecture search (AutoML-Zero + TRIZ)
```

### 8 개의 ORG-* FR

| FR | 이름 | Stage |
|---|---|---|
| ORG-06 | Provenance-aware tokens | B+D |
| ORG-02 | Memory-coupled inference | C/D |
| ORG-03 | Multi-track sub-network | C |
| ORG-08 | llive-specialized small model | C |
| ORG-07 | Approval-native decoding | C/D |
| ORG-01 | Cognitive Block Replacement | D |
| ORG-04 | TRIZ-guided architecture search | D |
| ORG-05 | Surprise-native pretraining | E |

### 3 개의 평가 지표

- **Architectural Originality Score (AOS)** = 차별화 FR 구현 수 / 전 FR 수 (현상 ~60%, 목표 ≥85%)
- **LLM Core Independence Ratio (LCIR)** = llive 전용 inference path / 전 inference path (현상 0%, 목표 Stage C 에서 ≥50%)
- **Replaceability Test** = Qwen 을 빼고 동작하는가 (Stage E 에서 ✅)

### 장기로 논문화 후보

- "**Cognitive Block Replacement**: Memory-coupled Transformer for Verifiable Agent Loops"
- "**Provenance-aware Attention**: Trust Score as Inductive Bias"
- "**Surprise-native Pretraining**: Bayesian Surprise as Loss Function"
- "**TRIZ-guided Neural Architecture Search**: 40 Principles for Network Mutation"

ICML / NeurIPS / ICLR / AAAI 에서 통하는 연구 품질을 목표로 한다.

상세: [10_qwen_divergence_strategy.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md)

---

## 11. Qwen 과 상호 보완하는 llive — Local 환경에서 5 틈새를 메운다 (전략 B)

사용자 관찰:

> 상호 보완의 관계를 목표로 하는 것도 있다. 원래 llive 는 Local 환경에서 돌리는 상정의 것. 틈새를 잘 보간할 수 있으면 좋다.

### 이층 구조

```
路線 1: 常設の補完戦略 (Local 環境特化)
       └ Qwen / Llama が進化しても不変の価値
路線 2: 研究としての独自化 (ORG-FX 5 段階)
       └ 中長期で研究価値を持続

両者は同時並走可能
```

### 5 개의 틈새

#### 틈새 1: 수치 계산・기호 조작・형식 검증

| Qwen 의 약점 | llive 의 보완 |
|---|---|
| `(2.5 * 7.8) / 0.3` 를 틀린다 | **MATH-08 SafeCalculator** |
| `5 m/s + 3 s = 8` (차원 오류) | **MATH-01 SI 차원 해석** |
| `(x+1)² = x² + 2x` (기호 환각) | **MATH-02 Sympy 검산 + EVO-04 Z3** |
| CODATA 값의 날조 | **MATH-05 물리 상수 사전** |

#### 틈새 2: 장기 기억・경험 재생

| Qwen 의 약점 | llive 의 보완 |
|---|---|
| context window (32K-128K) 의 한계 | **4 층 메모리** |
| session 을 넘는 기억 불가 | **persistent memory** + provenance |
| 같은 실수를 반복 | **Failed Reservoir** (EVO-06) + Reverse-Evo Monitor (EVO-07) |
| "자신이 이전에 무엇을 말했는지" 잊음 | **append-only ledger** |

#### 틈새 3: 행동 감사・책임 소재

| Qwen 의 약점 | llive 의 보완 |
|---|---|
| 위험한 동작의 architectural gate 없음 | **Approval Bus** + Policy + SQLite Ledger |
| 출력 책임의 추적 곤란 | **Provenance chain** + SHA-256 audit chain |
| dangerous tokens 의 필터 없음 | **GovernanceScorer** (4 축 scoring) |
| 감사 로그가 에페메럴 | **persistent JSONL + replay** 가능 |

#### 틈새 4: 인지 구조・다시점・모순 해결

| Qwen 의 약점 | llive 의 보완 |
|---|---|
| 시야 협착 (최초의 후보에 끌려감) | **CREAT-01 KJ법 노드** (확산 ≥20 건 강제) |
| 사고의 얕음 (1 계층 전개) | **CREAT-02 MindMap** (DFS depth=3) |
| 편향된 낙관 | **CREAT-04 Six Hats** (cautious 관점 강제) |
| 기존 패턴 의존 | **CREAT-05 Synectics** (이분야 유추) |
| 모순을 다룰 수 없음 | **TRIZ 40 원리** (FR-23〜27) |

#### 틈새 5: Local 환경 특유의 제약

| Local 환경의 특성 | llive 의 대응 |
|---|---|
| 네트워크 부재 | **완전 on-prem 동작** (Ollama / LM Studio / vLLM) |
| 개인 데이터를 밖에 내보낼 수 없음 | **provenance + Quarantined Zone** (SEC-01) |
| 계측 기기와의 직접 접속 | **llmesh sensor bridge** (FR-19, MQTT/OPC-UA) |
| 엣지 추론 (저스펙) | **MATH-08 등의 결정론적 층** (LLM 을 호출하지 않음) |
| 프라이버시 (가족의 대화, 의료 정보) | **Local-only ledger** + 클라우드 송신 제로 |
| 기동 시간・통신 지연의 제약 | **Brief API 의 overhead < 1 %** (실측됨) |

cloud LLM (GPT / Claude / Gemini / Perplexity) 으로는 **절대로 재현할 수 없는 영역**. 이것이 llive 의 **불변의 차별화 축**.

### 재프레이밍

> "단독으로 쓴다면 Qwen 으로 충분" → **"Qwen 을 Local 환경에서 안전하게 책임을 지고 쓴다면 llive 가 최단 경로"**

### 평가 벤치에의 시사 (향후 개선)

"llive vs Qwen" 의 대립 구도가 아니라 **협조 axis**:

- **Hybrid task score**: Qwen 만 vs llive (= Qwen + 결정론적 보완층) 의 종합 스코어
- **Niche task score**: Qwen 이 약한 태스크에서 llive 가 얼마나 보완할 수 있는가
- **Local capability**: 네트워크 없이 완결되는 task 의 망라율
- **Audit completeness**: 출력에 대한 trace coverage

상세: [11_complementary_with_qwen.md](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md)

---

## 전체 정리 — 한 세션에서의 도달점

### 구현

- **Brief API** (LLIVE-001/002) end-to-end / S1 BriefGrounder / MATH-01/08 / COG-01/02/03
- llive 테스트: **1014 PASS / 0 fail / 0 regression**

### 요건 추가 (REQUIREMENTS.md)

- v0.7-vertical MATH 8 건 (그 중 MATH-08 이 차별화 축 최대)
- v0.8 CABT 7 건 (Transformer 블록 고도화)
- v0.9 CREAT 5 건 (KJ법 / MindMap / Six Hats / Synectics)
- v1.0-frame COG-FX 4 건 (10 사고 인자 매핑)
- v2.0-core ORG-FX 8 건 (Qwen 의존에서의 이탈 5 단계)
- **합계 100 건, Phase 매핑 완비**

### 벤치마크

| 종류 | 셀 수 | 주요 관찰 |
|---|---|---|
| progressive matrix | 5×3=15 | overhead < 1 %, decision 전 note |
| fair re-bench | 4×6=24 (실 OK 12) | llive (LLM attached) 는 ollama 직접 호출의 2-4 배 느림 |
| quiz Debug | 10 | passed 6/10, ms mean 22.3s |
| quiz Release | 10 | passed 7/10, ms mean 22.8s, Debug overhead +1.8% |

### 전략의 이층 구조

1. **상설의 보완 전략** (Local 환경에서 5 틈새 보완) — cloud LLM 이 진화해도 불변
2. **연구로서의 독자화** (ORG-FX 5 단계) — Stage A → B → C → D → E

### 교훈 — TRIZ 모순으로서의 honest disclosure

> 벤치를 취한 순간에 이긴 기분이 되기 전에, 벤치의 설계 결함을 의심한다.

신규 memory: [`feedback_benchmark_honest_disclosure`](https://github.com/furuse-kazufumi/raptor/blob/main/.claude/projects/C--Users-puruy-raptor/memory/feedback_benchmark_honest_disclosure.md)

### GitHub

- llive: <https://github.com/furuse-kazufumi/llive>
- fullsense (umbrella 포털): <https://github.com/furuse-kazufumi/fullsense>
- llove (TUI HITL): <https://github.com/furuse-kazufumi/llove>
- llmesh (LLM hub): <https://github.com/furuse-kazufumi/llmesh>

모두 **Apache-2.0 + Commercial dual-license**.

### 개별 기사 링크 (상세는 여기서)

| # | 제목 | 테마 |
|---|---|---|
| 1 | [Brief API + progressive matrix (overhead < 1 %)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/01_brief_api_progressive.md) | Brief API + 5×3 bench |
| 2 | [심리의 심층 10 사고 인자로 정리하는 llive 사고층](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/02_cognitive_factors.md) | COG-FX 프레임워크 |
| 3 | [수학・단위에 강한 AI — MATH-01/08](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/03_math_vertical.md) | MATH 계 |
| 4 | [Transformer 블록 고도화 7 접근 (CABT 설계 예고)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/04_next_cabt_block_design.md) | CABT |
| 5 | [LLM × KJ법 × MindMap 으로 요건 정의 자동화 (CREAT 설계 예고)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/05_next_creat_kj_mindmap.md) | CREAT |
| 6 | [형식 검증 게이트로 LLM 수식 환각을 멈춘다 (MATH-02 설계 예고)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/06_next_math02_formal_gate.md) | MATH-02 |
| 7 | [fair bench (honest disclosure 전면 개정판)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/07_bench_results.md) | bench 방법론 |
| 8 | [quiz bench Debug vs Release × mean/stdev](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/08_quiz_bench_debug_vs_release.md) | quiz + 통계 |
| 9 | [llive 구조 독자성 8 요소](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/09_llive_structure_originality.md) | 인지 OS positioning |
| 10 | [Qwen 이탈 5 단계 ORG-FX](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/10_qwen_divergence_strategy.md) | 독자화 노선 |
| 11 | [Qwen 상호 보완 5 틈새](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/articles/2026-05-17/11_complementary_with_qwen.md) | 보완 노선 |

## 맺으며

llive 는 "LLM 그 자체" 가 아니라 "LLM 을 내장하는 인지 OS" 로서, Local 환경에서 5 개의 틈새를 보완하면서, 중장기로는 LLM 코어 자체의 독자화를 계획적으로 진행하는 설계입니다.

하루에 요건 32 건 + 구현 1014 PASS + 공개 기사 11 편 + 본 서머리 라는 "벤치에서 자사를 의심하는 honest disclosure" 도 포함한 등신대의 개발 기록으로 남겼습니다.

질문・지적・개선 제안은 GitHub Issues 또는 Twitter / X (@puruyan) 로 부탁드립니다.

---

> 본 기사는 Claude Opus 4.7 (1M context) 와 대화하면서 집필. 구현과 검증도 같은 세션 내에서 완주. 하루에 이 규모를 진행할 수 있는 것은, 인지 OS 가 사고의 발판을 단단히 만들고 있기 때문.
