---
layout: default
title: "検問体系監査 (A-Evolve 三重検問棚卸し)"
parent: "Research"
nav_order: 95
---

# 自己進化フレームワークの「検問 (gate)」体系監査 — A-Evolve 三重検問の棚卸しと拡張

> **作成 2026-06-06** / 対象: llcore・llive・raptor・lleval・llmesh(FullSense)
> **目的**: 自己進化 LLM フレームワーク A-Evolve (arXiv 2602.00359 v2) の「三重検問 +
> 統治機構」に相当するものを我々が持っているかを **実コードで** 棚卸しし、それ以外に
> あり得る検問を体系化する。推測でなく Read/Grep で実体確認した事実のみを記す。
> **honest disclosure**: 「未実装/部分実装/未配線」は曖昧にせず明記する
> ([[feedback_implementation_status_record]])。

---

## 0. A-Evolve の検問とは何か (検証済み事実)

A-Evolve は改造案 (ツール / スキル / 知識の更新) を **本番採用する前に** 3 段の検問を通す:

| # | A-Evolve の検問 | 何を保証するか | 性質 |
|---|---|---|---|
| 1 | **AST 文法チェック** (Python AST parsing for tools) | ツールコードが構文的に壊れていない | 形式 (構文) |
| 2 | **スキーマ形式チェック** (YAML frontmatter schema for skills) | スキル定義がスキーマに準拠する | 形式 (スキーマ) |
| 3 | **隔離 sandbox 試運転** (isolated execution in ToolWorkspace) | 実行して即時にクラッシュ・劣化しない | 動的 (実行) |

加えて全変更に **来歴 (provenance) logging + rollback + risk-based human oversight** を付ける。

**核心の理解**: A-Evolve の検問は「**性能が落ちない・形式が壊れない**」ことを担保する
*工学的* ゲートであり、**数学的証明ゲートではない**。ここが我々 (特に llcore) との最大の差。

---

## 1. 我々の検問の棚卸し (実コードで確認)

### 1.1 llcore (`D:/projects/llcore`) — 形式証明ゲートを持つ唯一の repo

llcore は RWKV-gene の自己進化を「数学的に証明された不変量」で gate する。A-Evolve には
**無い軸**を持つ。

| 検問 | 実体 (ファイル) | 何を保証するか | 状態 |
|---|---|---|---|
| **Z3 state-norm 不変量** | `src/llcore/verifier/invariants.py::verify_gene_safe` | clip 済み gene が `\|s\|≤1` を time step を跨いで保つ(Z3 unsat = 反例なし)。tanh は sound 上界 `\|tanh(pre)\|≤min(\|pre\|,1)` で近似 | 実装済 |
| **Z3 Lipschitz contraction (L<1)** | 同 `::verify_lipschitz_contraction` | 状態方向ヤコビ `J(t)=decay+(1−decay)·gate_str·t` の `sup\|J\|<1` を free-t over-approx で証明 → Banach 一意固定点 | 実装済 |
| **SDP/Lyapunov LMI gate (coupled gene)** | `src/llcore/verifier/backends.py::SdpLyapunovBackend` | 非対角 gene の共通二次 Lyapunov 行列 `P−JᵀPJ≻0` を CLARABEL で求解 → 任意の固定誘導ノルムより広いクラスを certify | 実装済 |
| **fail-closed 規律** | `backends.py` (CLARABEL 必須)・`research/.../test_fail_closed.py` (10 test) | CLARABEL 不在環境で SCS(artifact-prone)に **暗黙フォールバックしない**。証明器が不在なら certify を拒否(`available=False`/`certified=None`) | 実装済 + 専用テスト |
| **null harness (反証ハーネス)** | `src/llcore/evolution/honest_eval.py::evolution_vs_random` | 「進化が同予算 random search を ≥15 seed で片側 Wilcoxon p<0.05 かつ効果量非無視で上回る」を合格条件にする。elitism 凍結持越し artifact を fresh-seed 再評価で構造的に排除 | 実装済 |
| **gate-into-loop 配線 (resample + fallback)** | `research/verified_evolution/gated_evolve.py` | 子個体生成時に gate を適用し、reject → resample (cap=50) → known-safe fallback gene。`gate_mode="none"` は src `evolve()` と byte-identical(制御として等価性を assert) | **research 層のみ** |
| **red-team lens 運用** | `research/**/redteam_*.py` (Grep で **22 ファイル**確認) | 各 PoC verdict を敵対的に反証(soundness / overclaim / trace-violator / seedshift / boundary 等) | 運用済 (research 規律) |
| **pytest** | `tests/unit/` (**15 test ファイル**: backends 7 / honest_eval 10 / lipschitz 14 等) | 各 PoC の回帰 | 実装済 |

**honest disclosure (重要・未配線)**: Z3/SDP gate と null harness は **`src/llcore/evolution/minimal_ga.py` の本体 GA ループには配線されていない**(Grep 確認: minimal_ga に `certif`/`verify_` 呼び出しなし)。gate を進化ループに挿す配線は `research/verified_evolution/gated_evolve.py` という **research 層の別実装**にあり、src の `evolve()` は無検問。つまり「証明ゲート付き進化」は **研究レベルで実証済だが、出荷 API には未統合**。

### 1.2 llive (`D:/projects/llive`) — HITL + 構造不変量 SMT を持つ

llive は「LLM の周りに被せる認知 OS」。自己進化(ChangeOp によるアーキ書換え)に対して
**構造的検問**と **人間承認 (HITL)** を持つ。

| 検問 | 実体 (ファイル) | 何を保証するか | 状態 |
|---|---|---|---|
| **Approval Bus (HITL)** | `src/llive/approval/bus.py::ApprovalBus` | §AB1 replayable(ledger 再構築で同一 verdict 列)/ §AB2 principal 識別 / §AB3 revoke→rollback / **§AB4 silence==denial(沈黙は不承認 = fail-closed)** | 実装済 |
| **Approval Policy 事前 gate** | `src/llive/approval/policy.py` (`AllowList`/`DenyList`/`Composite`) | action を allowlist/denylist で自動承認・拒否、不明は人手 review に流す | 実装済 |
| **SQLite ledger (来歴永続)** | `src/llive/approval/ledger.py` | approval/denial を再起動越しに replay 可能に永続化 | 実装済 |
| **Static Verifier (構造不変量)** | `src/llive/evolution/verifier.py::verify_diff` | ChangeOp 列が構造不変量(min/max blocks・essential types・attention 必須・memory_read↔write ペア・重複名)を保つかを **LLM 評価の前に** 検査 | 実装済 |
| **SMT 層 (Z3, opt-in)** | 同 `::_smt_verify` | 上記不変量を Z3 で(n_blocks/attention/memory_read/write を per-step エンコード)状態軌道全体で satisfiable か検証。Z3 不在時は構造検査のみに degrade (`smt_used=False`) | 実装済 |
| **ChangeOp action log (来歴)** | `src/llive/evolution/change_op_log.py` | 実際に materialise された ChangeOp 列を append-only JSONL に記録(`applied` で static gate 通過可否も記録) | 実装済(データ蓄積待ち) |
| **6-stage Loop の salience gate** | `src/llive/fullsense/loop.py::_salience_gate` | Stimulus.surprise が低い刺激を落とす **関連性ゲート**(安全/正当性ゲートではない) | 実装済 |
| **1000+ tests** | `tests/` (**248 test ファイル**) | 全機能の回帰 | 実装済 |

**honest disclosure**: llive の `evolution/verifier.py` は **A-Evolve の検問 1+2 を上回る**(構文/スキーマでなく**構造不変量を SMT で証明**する)。一方、A-Evolve の検問 3「隔離 sandbox 試運転」に直接対応するのは `src/llive/fullsense/sandbox.py` (SandboxOutputBus) だが、これは **出力隔離バス**であり、改造案を別プロセスで *実行して劣化を測る* canary 試運転とは別物 → **検問 3 は部分**。

### 1.3 raptor (`D:/tools/raptor`) — 供給網・統治の検問

raptor はセキュリティエージェント fork。改造案(plugin/skill/MCP)の **供給網整合性**と
**エージェント統治**を gate する。CLAUDE.md 記載と実体は一致(確認済)。

| 検問 | 実体 (ファイル) | 何を保証するか | 状態 |
|---|---|---|---|
| **Plugin integrity (SHA-256 manifest)** | `libexec/raptor-plugin-integrity` | plugin/skill/MCP 配下全ファイルの SHA-256 + 連鎖 hash で `INTEGRITY.json` を生成・検証。MODIFIED/MISSING/UNTRACKED を検出、exit 2 | 実装済 |
| **Promotion gate** | 同 `cmd_promotion_check` | 昇格(dev→prod)前に integrity + 必須ファイル(README/plugin.json)+ `.mcp.json` の `@latest` 非ピン依存を検査 | 実装済 |
| **SWD (Strict Write Discipline)** | `libexec/raptor-swd` | 出力成果物の SHA-256 snapshot → drift 検出(snapshot/verify/diff/clean、exit 2 on drift) | 実装済 |
| **GovernancePolicy (`@govern`)** | `packages/governance/policy.py` | tool allowlist/blocklist・content blocked_patterns(正規表現)・rate limit・REVIEW(人手承認)を decorator で強制。`compose_policies` は most-restrictive-wins | 実装済 |
| **IntentClassifier** | `packages/governance/intent.py` | prompt を正規表現で危険分類(data_exfiltration / privilege_escalation / system_destruction / prompt_injection / credential_exposure)、confidence 付き | 実装済(ヒューリスティック) |
| **TrustScore (時間減衰)** | `packages/governance/trust.py` | エージェントの成功/失敗で trust を更新、無活動で指数減衰。reliability = successes/total | 実装済 |
| **AuditTrail / Traceability** | `packages/governance/audit.py`・`traceability.py` | 重要状態変化を log。`ActionRecord` で Claude/GPT/Gemini 横断の causal chain(parent_id)を追跡 | 実装済 |
| **semgrep / CodeQL SAST** | `raptor.py` (semgrep MCP も `~/.claude.json` に登録) | 改造対象コードの静的脆弱性スキャン | 実装済 |

**honest disclosure**: IntentClassifier は **正規表現ヒューリスティック**であり、CLAUDE.md の
「semantic intent classification」という語感より実体は浅い(意味埋め込みではなくパターン照合)。
誤検知/見逃しは構造的にあり得る。

### 1.4 lleval (`D:/projects/lleval`) — eval 基盤(pre-PoC)

| 検問 | 実体 | 何を保証するか | 状態 |
|---|---|---|---|
| **Honest disclosure 5+1 軸** | README / `src/lleval/` | latency/quality/stability/safety/honesty + runtime metadata 6 SHA の内訳分解 | **0.1.0a0 skeleton(設計のみ)** |
| **Judge rotation + position swap** | 設計(README §4) | LLM-as-judge の self-preference bias を自動検出(Panickssery 2024) | **未実装(設計記載のみ)** |
| **Progressive size matrix** | `src/lleval/runner.py` | xs/s/m/l/xl × providers の A/B run(promptfoo を wrap) | skeleton |

**honest disclosure**: lleval は **pre-PoC skeleton (0.1.0a0, 2026-05-21)**。eval を「採用検問」
として使う基盤は **設計だけ存在し、自己進化ループの gate としては未稼働**。

### 1.5 llmesh (`D:/projects/llmesh`) — SPC 管理図ゲート(我々だけの強み)

| 検問 | 実体 (ファイル) | 何を保証するか | 状態 |
|---|---|---|---|
| **SPC 管理図エンジン** | `llmesh/industrial/spc_engine.py` | Xbar-R / CUSUM 等の統計的工程管理。プロセスが「管理限界内」かを判定 | 実装済 |
| **多変量 SPC** | `industrial/hotelling_t2.py`・`multimodal_spc.py` | Hotelling T² で多変量の異常を検出 | 実装済 |
| **explained CUSUM / video CUSUM** | `industrial/explained_cusum.py`・`video_cusum.py` | 逐次変化点検出 + 説明 | 実装済 |

**SPC を「採用検問」に転用する着想は本 doc のギャップ分析(§4)で扱う** — 現状 SPC は
産業 IoT センサ向けで、**自己進化メトリクスの管理図ゲートとしては未配線**。

---

## 2. 対応表 — A-Evolve の各検問 ↔ 我々の対応物

| A-Evolve の検問 / 統治 | 我々の対応物 (repo / 実体) | 有/無/部分 | 我々の方が強い点 |
|---|---|---|---|
| ① AST 文法チェック (tools) | pytest 構文・import 検査 (全 repo) / Python 自体の parse | **部分** | — (A-Evolve 同等。専用 AST gate は無い) |
| ② スキーマ形式チェック (skills) | llive `evolution/verifier.py` 構造不変量 + Z3 SMT / raptor `_meta` skill-lint / plugin.json 必須検査 | **有 (上回る)** | スキーマ準拠でなく **構造不変量を SMT で証明** |
| ③ 隔離 sandbox 試運転 | llive `fullsense/sandbox.py` (出力隔離) / llcore `gated_evolve` の fresh-seed 再評価 | **部分** | canary 実行による劣化計測は弱い(§4(a)で補強候補) |
| 来歴 (provenance) logging | llive `approval/ledger.py`(SQLite)・`change_op_log.py` / raptor `traceability.py`・`audit.py` / raptor SWD・plugin-integrity manifest | **有 (上回る)** | SHA-256 連鎖 + drift 検出 + 多 AI causal chain |
| rollback | llive Approval Bus §AB3 revoke→rollback | **有** | replayable ledger で決定的に再構築 |
| risk-based human oversight | llive Approval Bus(§AB4 silence==denial = fail-closed)+ Policy / raptor `@govern` の REVIEW | **有 (上回る)** | **沈黙=拒否**の fail-closed 既定 |
| (A-Evolve に無い) **数学的証明ゲート** | llcore Z3 state-norm / Z3 Lipschitz L<1 / SDP-Lyapunov LMI(全 fail-closed) | **我々だけ** | A-Evolve は性能ゲートのみ。我々は **不変量を証明**して admit |
| (A-Evolve に無い) **null/反証ハーネス** | llcore `honest_eval.py`(進化 vs 同予算 random、Wilcoxon + 効果量) | **我々だけ** | 「本当に進化したか」を統計的に反証 |
| (A-Evolve に無い) **SPC 管理図** | llmesh `industrial/`(Xbar-R / CUSUM / Hotelling T²) | **我々だけ (未配線)** | 逐次プロセス監視の成熟実装(転用候補) |
| (A-Evolve に無い) **供給網整合性 gate** | raptor plugin-integrity / SWD / promotion-check | **我々だけ** | SHA-256 manifest + 昇格ゲート |

---

## 3. 「それ以外の検問」体系化

自己進化ループのどの段階に置くべきかは 4 段で分類する:
**変異時 (mutation)** = 改造案を生成した直後 / **採用時 (admission)** = 集団・本番に入れる前 /
**実行時 (runtime)** = 採用後に動かしている最中 / **事後 (post-hoc)** = 走り終えた後の監査。

| 検問 | 何を保証するか | コスト | 置くべき段階 | 我々の保有 |
|---|---|---|---|---|
| **AST / 構文 gate** | 改造コードが parse できる | 極小 | 変異時 | 部分(汎用 parse のみ) |
| **スキーマ / 構造不変量 gate** | 定義がスキーマ・構造制約に従う | 小 | 変異時 → 採用時 | 有 (llive SMT で上回る) |
| **形式証明ゲート (Z3 / SMT / SDP)** | 不変量(有界性・contraction・安全制約)が **数学的に**成立 | 中〜大(求解) | 採用時 | **有 (llcore 独占)** |
| **property-based testing** | 入力空間を網羅的にサンプルして契約違反を探す | 小〜中 | 変異時 → 採用時 | 部分(pytest 内で hypothesis 散発) |
| **metamorphic testing** | 入力変換に対し出力が期待関係(不変・単調等)を保つ | 中 | 採用時 | **無**(候補 §4) |
| **differential testing** | 旧版/参照実装と新版の出力差を比較 | 中 | 採用時 | 部分(lleval A/B 設計、未稼働) |
| **隔離 sandbox / canary 試運転** | 別プロセスで動かし即時クラッシュ・劣化を検出 | 中 | 採用時 → 実行時 | 部分(出力隔離はあるが劣化計測弱い) |
| **statistical safety (Safe Policy Improvement)** | 新方策が旧方策を高確率で下回らない(下側信頼限界) | 中 | 採用時 | 部分(llcore null harness が近いが SPI そのものは無) |
| **null / 反証ハーネス** | 「効果は偶然でない」を同予算対照で統計的に反証 | 中 | 採用時 → 事後 | **有 (llcore 独占)** |
| **runtime shield (出力ゲート)** | 採用後も毎出力を policy/制約で検閲し fail-closed | 小(毎回) | 実行時 | 有(raptor `@govern` content filter / llive Approval) |
| **canary deployment + 自動 rollback** | 一部トラフィックに段階投入、劣化検知で自動巻戻し | 中 | 実行時 | 部分(rollback は有、段階投入は無) |
| **SPC 管理図ゲート** | プロセス指標が管理限界内(逐次変化点検出) | 小(逐次) | 実行時 → 事後 | **有 (llmesh、未配線)** |
| **integrity manifest** | 採用物のバイト同一性(改竄検出) | 極小 | 採用時 → 事後 | **有 (raptor)** |
| **provenance chain** | 誰が・いつ・何を変えたかの追跡可能性 | 小 | 全段階 | **有 (llive ledger / raptor traceability)** |
| **adversarial red-team eval** | 敵対入力・反証視点で堅牢性を破ろうとする | 中〜大(人手/LLM) | 採用時 → 事後 | **有 (llcore redteam 規律)** |
| **semantic diff 検査** | 改造前後の **意味的**変化(挙動差)を抽出・要約 | 中 | 採用時 | **無**(候補 §4) |

---

## 4. ギャップ分析 (honest 仕分け)

### (a) すぐ足せて差別化に効くもの [採用推奨]

1. **SPC 管理図を自己進化メトリクスの runtime ゲートに転用 (llmesh→llcore/llive)**
   — `llmesh/industrial/` の CUSUM / Xbar-R は成熟実装。fitness 曲線・多様性・gate
   reject 率を「プロセス変数」として管理図に流せば、**逐次変化点検出**で「進化が崩壊し
   始めた世代」を自動検知できる。**新規実装ほぼ不要(既存エンジンへの配線のみ)**。
   FullSense の独自性(SPC × LLM)を検問軸でも主張できる。

2. **metamorphic testing gate (llive 採用時)**
   — ChangeOp 適用後のモデルに対し「等価変換した入力で出力関係が保たれるか」を検査。
   llive は既に構造不変量 gate を持つので、**振る舞い不変量**へ拡張する自然な次の一手。
   sandbox 試運転の弱さ(§2 ③)を実行コスト小で補える。

3. **llcore の証明ゲートを src の `evolve()` に正式配線 (llcore)**
   — 現状 gate は `research/gated_evolve.py` の別実装。`gate_mode` 引数を src `evolve()`
   に semver 互換で追加すれば、「証明ゲート付き進化」が **research 実証から出荷 API へ**昇格。
   差別化核(A-Evolve に無い数学的 admission gate)を製品面に持ち込める。

### (b) 足す価値が薄いもの [見送り]

- **専用 AST gate の新設** — Python の import/parse + pytest で実質カバー済。A-Evolve 同等
  止まりで差別化に寄与しない。
- **Safe Policy Improvement の本格実装** — llcore null harness が「同予算対照で有意差」を
  既に検証しており、SPI の下側信頼限界は理論的により厳密だが、現行 proxy fitness が平坦で
  `passes=False` が想定される段階では **過剰**。実 LLM fitness 配線後に再評価。
- **canary 段階投入の自動化** — 自宅単一環境では段階投入のトラフィック分割が不自然。
  rollback(既存)+ SPC 管理図(候補 a-1)で実用上十分。
- **lleval を急いで gate 基盤化** — pre-PoC skeleton であり、judge rotation 等の差別化軸は
  魅力的だが、検問としての成熟は時期尚早。先に上記 (a) を固めるべき。

---

## 5. TOP-3 追加すべき検問 (理由つき)

1. **SPC 管理図 runtime ゲート (既存 llmesh エンジンの配線)** — コスト最小・既存資産活用・
   FullSense 独自性(SPC×LLM)を検問軸に拡張。進化崩壊の早期検知。
2. **llcore 証明ゲートの src `evolve()` 正式配線** — A-Evolve に対する最大の差別化核
   (数学的 admission gate)を research 層から出荷 API へ昇格させ、製品価値に直結。
3. **metamorphic testing gate (llive)** — 既存の構造不変量 gate を「振る舞い不変量」へ
   低コストで拡張し、sandbox 試運転の弱点を補う。

---

## 6. 結論

A-Evolve の三重検問(AST / スキーマ / sandbox)+ 来歴・rollback・HITL は、我々では
**llive(Approval Bus + 構造不変量 SMT)+ raptor(integrity / governance)が同等以上**に
カバーしている。さらに我々は A-Evolve に **無い 4 軸**(① 形式証明ゲート=llcore、② null/
反証ハーネス=llcore、③ SPC 管理図=llmesh、④ 供給網整合性 gate=raptor)を持つ。

最大の **honest な弱点**は「llcore の証明ゲートと null harness が research 層の別実装に留まり、
出荷 GA ループ(`minimal_ga.py`)に未配線」である点。差別化核が製品面に出ていないので、
§5 の TOP-2(src 配線)を優先すべき。

---

### 参照した実コード (一次情報)

- llcore: `src/llcore/verifier/{invariants,backends,changeop}.py`・`src/llcore/evolution/honest_eval.py`・`research/verified_evolution/gated_evolve.py`・`research/verified_evolution_sdp_gate/test_fail_closed.py`・`research/**/redteam_*.py` (22)・`tests/unit/` (15)
- llive: `src/llive/approval/{bus,policy,ledger}.py`・`src/llive/evolution/{verifier,change_op_log}.py`・`src/llive/fullsense/loop.py`・`tests/` (248)
- raptor: `libexec/raptor-plugin-integrity`・`libexec/raptor-swd`・`packages/governance/{policy,intent,trust,audit,traceability}.py`
- lleval: `README.md`・`src/lleval/runner.py`(0.1.0a0 skeleton)
- llmesh: `llmesh/industrial/{spc_engine,hotelling_t2,multimodal_spc,explained_cusum}.py`
