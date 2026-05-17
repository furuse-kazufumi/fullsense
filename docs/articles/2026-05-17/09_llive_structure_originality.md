---
layout: default
title: "llive の構造は LLM として独自になっているか — 8 つの差別化要素の点検"
date: 2026-05-17
author: "古瀬 和文（ぷるやん）"
tags: [llm, architecture, originality, cognitive-os, llive]
---

# llive の構造は LLM として独自になっているか — 8 つの差別化要素の点検

著者: 古瀬 和文（ぷるやん）

## TL;DR

ユーザーからの問い：「llive の構造って、LLM として独自の構造になっていってますか？」

答え: **llive は LLM そのものではなく、LLM の周りに被せる「認知 OS」として独自**。Decoder-only LLM (Qwen / Llama / Mistral / 等) を frozen な計算コアとして使い、その上に 8 つの構造要素を積層することで、既存類似研究 (MemGPT / LongMem / AutoML-Zero / Self-Refine / Reflexion / MERA / AutoGPT 系) のいずれとも一致しない設計に到達している。

## 8 つの差別化要素

### 1. Decoder-only LLM コアは凍結 + 周辺で能力拡張

| 既存 | llive |
|---|---|
| 全量 fine-tune / LoRA / adapter | LLM 重みは **絶対に触らない** |
| 学習 = モデル更新 | 学習 = **外部記憶への書き込み** + **構造変更** |

これは LoRA / adapter の延長線にあるが、「重みを更新しないことで replay 可能 / monitorable な学習軌跡」を最優先にしている点が独自。CABT (S2 で計画中) では forward hook で attention に bias を加えるが、これも重み凍結のまま。

### 2. 4 層メモリの責務分離 (特に parameter memory が独自)

| 層 | 役割 | 既存研究の対応 |
|---|---|---|
| semantic | 知識 (事実) | RAG、ベクトル DB、kNN-LM |
| episodic | 経験 (時系列) | MemGPT / Memorizing Transformers |
| **structural** | **関係 (graph / dependency)** | **少例 (Knowledge Graph 系)** |
| **parameter** | **重みの差分** | **llive 独自寄り** |

特に **parameter memory** は「LoRA adapter / sub-block の集合を memory として扱い、surprise gate で write 制御する」発想。Adapter Store + Bayesian Surprise + 進化レポジトリ という組合せは類似がない。

### 3. 6 stage FullSense Loop の擬人化された認知段階

```
Salience Gate ──→ Curiosity Drive ──→ Inner Monologue ──→
Ego/Altruism Scorer ──→ Action Plan ──→ Output Bus (Sandbox / Production)
```

各段階に **数式 + 心理学的根拠** を持たせている設計:

- Salience: 入力の surprise score でフィルタ
- Curiosity: 既知 corpus との novelty で点数化
- Inner Monologue: 鏡映認知 (mirror-thought)、TRIZ 原理検出を内蔵
- Ego/Altruism: 動機の二軸でアクションを再採点
- Action Plan: PROPOSE / INTERVENE / NOTE / SILENT の 4 択
- Output Bus: Sandbox (副作用なし) と Production (Approval 経由) を物理分離

これは既存の "agent loop" (ReAct / ToT / Reflexion) より **心理的妥当性を重視した 6 段モデル**。

### 4. Multi-track Filter Architecture A-1.5 (EpistemicType による track 切替)

`EpistemicType` 列挙 (FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC / RESERVED_1〜5) に応じて filter chain を切り替える。

例:
- 数学質問 → MATHEMATICAL track (FACTUAL strict)
- 倫理的判断 → NORMATIVE track (§F5 ethical 優先)
- 歴史認識 → INTERPRETIVE track (perspective-dependent)

「結論不変な FACTUAL と perspective-dependent な INTERPRETIVE を crude に混ぜない」設計。これは LLM 単体には存在しない。

### 5. Approval Bus を Loop 内に組み込み (HITL を architecture level に)

PROPOSE / INTERVENE 決定は必ず Approval Bus を経由。policy で auto-approve/deny、残りは llove TUI で人手 review。すべて SQLite ledger に永続化。

既存類似:
- Codex CLI の `suggest / auto-edit / full-auto` モード
- Gemini CLI の approval prompt

しかし、**Bus 経由で全 PROPOSE/INTERVENE が SQLite に永続化 + replay 可** な実装は llive 独自。これは COG-FX 整合因子 (COG-02) の核心。

### 6. TRIZ 40 原理を mutation policy として内蔵

FR-23〜27 で実装:
- Contradiction Detector (メトリクスから矛盾自動検出)
- Principle Mapper (39×39 マトリクス内蔵)
- RAD-Backed Idea Generator (TRIZ × RAD コーパス → CandidateDiff 生成)
- 9-Window System Operator (時間軸 × 階層軸)
- ARIZ Pipeline (9 ステップを mutation 自動化)

これは Self-Refine / Reflexion の「自己批評」と異なり、**創造の代替案生成エンジン**として TRIZ を内蔵。Synectics (CREAT-05 計画) と組合せて cross-domain analogical reasoning も。

### 7. Cognitive Factor Framework (CFF) ― 認知設計を明示的に分解

「心理の深層」由来の 10 因子 (構造化・再構成・閉ループ・自己拡張・不確実性・探索・整合・来歴・多視点・現実接続) を **役割別 policy に分解**:

- planner policy / memory policy / critic policy / evolution policy / trace policy

これにより個別 A/B 比較・改善・evolve が可能。COG-01/02/03 (本日実装) で確認: BriefResult に (confidence, assumptions, missing_evidence) の Triple Output + Governance Scoring (4 軸) + Trace Graph (3 chain)。

既存 LLM ライブラリ (LangChain / LlamaIndex / AutoGen / CrewAI) には policy 分解の発想はあるが、**認知因子を明示的にマップした architecture** は llive のみ。

### 8. Brief API ― 構造化 work unit という primitives

外部クライアント (lldesign / lltrade / 計画中の llcad / lleda / llchip) が work unit を渡せる API:

```python
Brief(
    brief_id="webpage-portal-refresh",
    goal="...",
    constraints=("no inline HTML inside fenced ```mermaid``` blocks",),
    success_criteria=("rendered HTML contains SVG",),
    tools=("read_file", "write_file"),
    approval_required=True,
    epistemic_type=EpistemicType.PRAGMATIC,
)
```

これは LangChain の `Chain` や CrewAI の `Task` と類似だが:

- **frozen dataclass** (immutable, replay-friendly)
- **append-only JSONL ledger** に全段階を固定記録
- **Approval Bus + Governance Scorer** を built-in
- **Grounder (TRIZ × RAD × SafeCalculator)** を前段に持つ

これらの組合せは類似がない。

## 構造として「独自」と言える理由

8 要素の各々は既存研究のどこかに対応物がある。しかし **8 要素の組合せ + 役割分離 + 心理因子マッピング** は llive 固有。

```
LLM (Qwen/Llama/...) を凍結コアとして使い
  + 4 層メモリで知識/経験/関係/重みを分離保持
  + 6 stage Loop で擬人化された認知段階
  + Multi-track Filter で epistemic_type 別 chain
  + Approval Bus で HITL を architecture level に
  + TRIZ 40 原理 + RAD 49 分野で代替案生成
  + 10 思考因子で policy を分解
  + Brief API で外部入力を構造化
```

この **積層構造** は、LangChain (chain) / AutoGen (multi-agent) / MemGPT (memory) / Self-Refine (critique) / AutoML-Zero (search) のいずれかに偏ることなく、**認知 OS** として横断する。

## 「LLM 自体は何か変えているか」への答え

**Phase 1〜v0.6 では LLM 重みは触らない** (frozen)。これは設計判断:
- replay 可能性を最優先
- 学習軌跡を monitorable に保つ
- LLM 提供元 (Qwen, Meta, Mistral) の更新を直接取り込める

ただし **Phase 8 (CABT) で forward hook による attention bias 注入** を計画。これも **重み更新ではない** が、推論時に metadata bias を加えるという「LLM の挙動を変える」レイヤー。完全な独自 LLM 構築 (LoRA training / distillation) は Phase 10+ の話で、現状の "独自性" は **LLM の周りに被せる cognitive OS** にある。

## 既存類似研究との位置づけ (再掲)

| 既存系 | 重なる範囲 | llive の差別化 |
|---|---|---|
| MemGPT / LongMem | 階層メモリ | 4 層分離 + phase transition + 署名 zone |
| AutoML-Zero / NAS-LLM | 構造探索 | 形式検証 gate + multi-precision shadow + 失敗データ化 |
| Self-Refine / Reflexion | 自己批評 | online/offline 分離 + llove TUI HITL staging |
| MERA / ModularLLM | モジュラー化 | 可変長 BlockContainer YAML + plugin registry |
| AutoGPT 系 | エージェント | llmesh 産業 IoT 直結 + llove TUI + Approval Bus |
| LangChain / CrewAI | Agent OS | 10 因子明示分解 + 認知 OS positioning |

## まとめ

「llive は LLM か」 → No、**llive は LLM を内蔵する認知 OS**。

「llive の構造は独自か」 → Yes、**8 要素の組合せ × 役割分離 × 心理因子マッピング** が独自。

「ベンチで速度比較すべきか」 → No、**速度ではなく構造を比較**すべき。llive の付加価値は ledger / approval / governance / grounding / 6 stage trace にあり、これは ollama 直叩きや LangChain chain では再現できない。

## ソース

- 設計: `D:/projects/llive/.planning/REQUIREMENTS.md` (要件 92 件、内 v1.0-frame COG-FX 4 件で因子マッピング)
- 実装: `D:/projects/llive/src/llive/` (brief / fullsense / approval / triz / memory / evolution / cabt 計画)
- 比較ベンチ: 同日記事 [01]({{ '/articles/2026-05-17/01_brief_api_progressive' | relative_url }}) / [07]({{ '/articles/2026-05-17/07_bench_results' | relative_url }}) / [08]({{ '/articles/2026-05-17/08_quiz_bench_debug_vs_release' | relative_url }})

---

> llive は LLM ではなく、LLM の周りに被せる認知 OS。8 要素の組合せが独自性を構成する。
