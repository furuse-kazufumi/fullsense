---
layout: default
title: "10 思考因子で整理する llive 思考層"
date: 2026-05-17
tags: [llm, agent, cognitive-architecture, design]
id: 4de8dcff1cf4c2ab9bdc
---

# 「心理の深層」10 因子で整理する llive 思考層 — 既に 9/10 実装済

## TL;DR

- 「心理の深層」YouTube から抽出された **10 思考因子** (構造化・再構成・閉ループ・自己拡張・不確実性・探索・整合・来歴・多視点・現実接続) を llive 既存 FR にマッピング
- v1.0 リリース必須の **土台 5 因子 (構造化 / 閉ループ / 不確実性 / 整合 / 来歴) は全て実装済**
- 不足分を COG-01〜04 として要件化し、2026-05-17 同セッション内で COG-01/02/03 を実装完了
- 残るは「現実接続」(Phase 4 IoT) と「多視点」の強化 (CREAT-04 と統合する COG-04)

## なぜ 10 因子フレームワークか

汎用 LLM の能力評価は「知識量」「言語流暢性」「推論精度」で語られがちですが、エージェント設計では **「どの認知フレームで状況を切るか」** の方が決定的に効きます。

ユーザー観察:

> 探索 / 再構成を強化する前に、構造化 / 不確実性 / 閉ループ / 整合 / 来歴の土台が必要

これがない状態で探索因子や再構成因子を強くすると、面白い案は増えるが、誤差・暴走・非再現性も増える。

## 10 因子 × llive マッピング

| # | 因子 | LLM 役割 | llive 既存 (実装済) | 追加 (2026-05-17 実装) |
|---|---|---|---|---|
| 1 | 構造化 | 課題を分解 | Brief constraints, Salience+Curiosity gate | — |
| 2 | 再構成 | 代替案生成 | TRIZ 40 原理 + ARIZ + 9 画法 (FR-23〜27) | (CREAT-01 計画) |
| 3 | 閉ループ | 検証計画を伴う | BriefRunner (submit→plan→approval→tool→outcome) | — |
| 4 | 自己拡張 | 外部資源を使う | 4 層メモリ + RAD 49 分野 + tools whitelist | MATH-08 計算エンジン |
| 5 | 不確実性 | 仮説と事実を分離 | FR-21 BayesianSurpriseGate + Quarantined Zone | **COG-01 Triple Output** |
| 6 | 探索 | 未踏案を試す | EVO-* (Z3 + Failed Reservoir + Reverse-Evo) | — |
| 7 | 整合 | 全体制約で再評価 | C-1 Approval Bus + EVO-04 Z3 + SEC-03 chain | **COG-02 Scoring Layer** |
| 8 | 来歴 | 判断履歴を残す | Provenance + SqliteLedger + BriefLedger + SHA-256 chain | **COG-03 Trace Graph** |
| 9 | 多視点 | 評価関数を分離 | Multi-track Filter A-1.5 (5 EpistemicType) | (COG-04 + CREAT-04 計画) |
| 10 | 現実接続 | 実環境制約を扱う | (Phase 4 INT-01〜04 計画中) | — |

## v1.0 必須 5 因子は全て実装済

| 因子 | 実装場所 | 役割 |
|---|---|---|
| 構造化 | `src/llive/brief/types.py::Brief` + loop._salience_gate / _curiosity_drive | 課題を decompose |
| 閉ループ | `src/llive/brief/runner.py::BriefRunner.submit` | plan-act-check loop |
| 不確実性 | `src/llive/learning/bayesian_surprise.py` (FR-21) + COG-01 | 仮説と事実の三層分離 |
| 整合 | `src/llive/approval/bus.py` + `src/llive/evolution/z3_checker.py` (EVO-04) + COG-02 | 全体制約 + governance |
| 来歴 | `src/llive/memory/provenance.py` + `src/llive/approval/ledger.py` + `src/llive/brief/ledger.py` + COG-03 | evidence/tool/decision chain |

これは llive が「v1.0 リリース水準で誤差・暴走・非再現性を防ぐ土台を備えている」という強い根拠です。

## 新規 COG-01〜03 の実装

### COG-01 Triple Output (不確実性因子の強化)

`BriefResult` に 3 列追加:

```python
@dataclass
class BriefResult:
    # ... 既存 ...
    confidence: float = 0.5
    assumptions: tuple[str, ...] = ()
    missing_evidence: tuple[str, ...] = ()
```

`BriefRunner` が決定論的に算出:

- `confidence = 0.5 · thought_conf + 0.5 · tool_success_ratio`
- `assumptions`: grounding 不在 / success_criteria 不在を明文化
- `missing_evidence`: TRIZ 原理が surface しなかった / tool 失敗 を保存

すべて ledger の `outcome` event に固定記録 → auditor が後から検証可能。

### COG-02 Governance Scoring Layer (整合因子の強化)

Approval Bus の **前段** に 4 軸スコアラを挿入:

```python
class GovernanceScorer:
    def score(self, brief, decision) -> GovernanceVerdict:
        # usefulness / feasibility / safety / traceability を独立算出
        # 重み付け平均 + recommend_block を返す
```

責務分離:
- **Governance** = scoring (なぜ良い/悪いか)
- **Approval Bus** = gating (実行可否の判断)

dangerous_token 検出 (`rm -rf` / `DROP TABLE` / `format c:` 等)、INTERVENE-without-approval ペナルティ、`block_threshold` / `safety_floor` をサポート。

### COG-03 Trace Graph (来歴因子の強化)

`BriefLedger.trace_graph()` メソッドが 3 層 view を返す:

```python
@dataclass(frozen=True)
class TraceGraph:
    evidence_chain: tuple[dict[str, Any], ...]   # TRIZ + RAD + calc citation
    tool_chain: tuple[dict[str, Any], ...]        # invoked / rejected / failed
    decision_chain: tuple[dict[str, Any], ...]    # decision / approval / outcome / governance
```

これにより、デバッグ・自己改善・失敗分析・evolution への学習データ抽出が機械的に可能になります。

## 横断 metadata schema

各メモリ・各 ledger entry に統一 attribute を付与する設計:

```python
{
    "factor": "uncertainty",       # 10 因子のどれか
    "uncertainty": 0.23,
    "dependency": ["evidence:doc#42", "tool:sympy.simplify"],
    "evidence_source": "doc#42",
    "applicable_scope": "math:dimensional",
    "promotion_status": "candidate",
}
```

LLM の自然言語ルールに依存せず、llove TUI / audit agent / evolution scheduler が機械的に消費できる形式。

## 結論

「面白い AI を作る」前に「壊れない AI を作る」ためのフレームワークとして、10 因子は強い指針になります。llive はその土台 5 因子をすべて実装済で、これからは **再構成・探索** (CREAT / EVO / TRIZ) を安心して積める段階に入りました。

## ソース

- 要件: `llive/.planning/REQUIREMENTS.md` v1.0-frame COG-FX セクション
- 実装: `src/llive/brief/governance.py` (新規) + `src/llive/brief/ledger.py::trace_graph()` (拡張) + `src/llive/brief/types.py::BriefResult` (拡張)
- テスト: `tests/unit/test_brief_cog.py` (16 件) — 1014 PASS / 回帰ゼロ
- memory: `project_llive_cog_fx_factors.md`

---

> 出典: 「心理の深層」 YouTube チャンネルから抽出された人間の思考因子セットを、ユーザーが「LLM に組み込める形」に変換した結果を要件化したものです。
