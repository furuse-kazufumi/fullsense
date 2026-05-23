---
title: llive 完全解説 (7) — 「審査つき AI」: runtime_metadata × Approval Bus × Ed25519 audit chain
tags:
  - FullSense
  - llive
  - 解説
private: false
updated_at: '2026-05-22'
id: null
organization_url_name: null
slide: false
ignorePublish: true
---
<!-- lead-trans-placed -->
<!-- h2-trans-placed -->

<!-- trilingual-subtitle-placed -->
<small><strong>EN:</strong> “AI with audit”: runtime_metadata × Approval Bus × Ed25519 audit chain<br>
<strong>中:</strong> "带审查的 AI": runtime_metadata × Approval Bus × Ed25519 审计链</small>
<!-- section-separators-placed -->

# llive 完全解説 (7) — 「審査つき AI」: runtime_metadata × Approval Bus × Ed25519 audit chain

![hero — Approval Bus verdict flow + Ed25519 audit chain](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_07_hero.svg)

<!-- progress-svg-placed -->
![連載進捗 (7/8) — 現在: audit](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_07_progress.svg)

> **コンセプト hook**: 多くの LLM agent は「結果のログ」しか残さない. しかし
> AI が **自分自身を進化** させはじめると, 「**いつ何を判断して何を変えたか**」
> の audit trail が無いと, **後でデバッグ不能** になる. llive はこれを
> architecture level で解いた:
> - **runtime_metadata** = 1 推論ごとの構造化 metadata
> - **Approval Bus** = 重大変更を ledger 経由で human / policy が approve
> - **Ed25519 + SHA-256 audit chain** = ledger 改ざん防止
> - **本日 (2026-05-21) 着地の E.4 governance** = 集団進化の共謀検出 → Approval Bus 連携
> 
> = **「自己進化する AI が, 自分の決定を全て署名つきで残す」** という珍しい形.

>
## 0. 連載中での位置づけ
<small><strong>EN:</strong> 0. Position within the series / <strong>中:</strong> 0. 在系列中的定位</small>

```
#24-00 series index
#24-01 4 層メモリ
#24-02 思考因子 × COG-MESH
#24-03 構造進化 × TRIZ × Z3
#24-04 B-series
#24-05 EvolutionLoop
#24-06 LLM backend non-transformer
#24-07 observability + governance (← 本記事)
#24-08 lleval
```

#24-03 の Z3 verifier が「**個体内**の構造変更を機械検証」だとすると, #24-07
は「**個体間**の挙動 + 個体集団の決定を audit trail で保存」. 検証と監査の
<small><strong>EN:</strong> This chapter persists 'inter-individual behaviour + population-level decisions' as an audit trail. Verification and audit substrate.<br>
<strong>中:</strong> 本章把 "个体间行为 + 群体级决策" 作为 audit trail 保存. 是验证与审计的基底.</small>
両輪.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

<!-- theme-svg-placed -->
![theme — Approval Bus + Ed25519 audit chain (animated)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_07_theme.svg)

## 1. なぜ Audit Chain が必須か
<small><strong>EN:</strong> 1. Why an audit chain is mandatory / <strong>中:</strong> 1. 为什么必须有审计链</small>

LLM agent が自分自身を書き換えはじめると, 「**さっきの推論は何 commit の
<small><strong>EN:</strong> Once an LLM agent rewrites itself, 'what commit produced this inference' becomes critical.<br>
<strong>中:</strong> 一旦 LLM agent 开始重写自身, "该次推断是哪个 commit 产生的" 就变得至关重要.</small>
構造で動いていたか**」が分からなくなる. これは debugging だけでなく:

- **責任追跡** — 集団進化で「**全派生が嘘の高得点を付け合った**」とき, 誰が
  最初に嘘をついたかを ledger で遡れる必要がある.
- **再現性** — 「あのとき出た結果」を後で再生するには構造 commit + memory
  zone + Brief input + Approval verdict の全て record が要る.
- **法的 compliance** — EU AI Act / 中国 AI 弁法 / 日本 G7 広島 process が
  示す方向は「**AI の決定は audit possible でなければならない**」.

llive は Phase 4 (Production Security MVR, v0.3.0) でこの 3 つを **同時に**
解いた.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 2. runtime_metadata — 1 推論あたりの構造化 trace
<small><strong>EN:</strong> 2. runtime_metadata - structured trace per inference / <strong>中:</strong> 2. runtime_metadata - 每次推断的结构化 trace</small>

llive の `FitnessReport.runtime_metadata` は free-form dict[str, str] だが
<small><strong>EN:</strong> llive's FitnessReport.runtime_metadata is a free-form dict[str, str], but with conventions.<br>
<strong>中:</strong> llive 的 FitnessReport.runtime_metadata 是 free-form dict[str, str], 但有约定.</small>
慣習的に以下を入れる:

- `signed_by`: peer evaluation の署名者 id
- `gen`: 世代番号
- `agg`: aggregator strategy
- `commit_sha`: ソース commit (CI 経由で注入)
- `model_id`: 使用 LLM backend id

これにより 1 推論結果から **完全に再現** できる. 再現性は **OSS LLM
inference の標準ではない** — 多くの agent は seed すら記録しない.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 3. Approval Bus — 構造的に変更を止める
<small><strong>EN:</strong> 3. Approval Bus - structurally halting changes / <strong>中:</strong> 3. Approval Bus - 结构性地阻止变更</small>

`src/llive/approval/bus.py` の `ApprovalBus`:
<small><strong>EN:</strong> src/llive/approval/bus.py — ApprovalBus.<br>
<strong>中:</strong> src/llive/approval/bus.py — ApprovalBus.</small>

- `request(action, payload, ...)` → pending リストに入る.
- `policy` が事前評価して `Verdict.APPROVED / DENIED / None` を返す.
  None なら人手待ち.
- 人手 / policy の verdict は `_ledger: list[ApprovalResponse]` に append.
- `ledger=SqliteLedger` を渡せば永続化 + 復元.

これは **架空の「Trust Score」** ではなく **明示的な APPROVED/DENIED 状態
マシン**. 沈黙 = denial (§AB4). 「曖昧な許可」が存在しない.

### 3.1 本日着地の E.4 governance 連携

`CoevolutionGovernance.evaluate_generation` (本日着地) が 1 世代の peer
matrix を見て **共謀疑い** → `ApprovalBus.request("coevolution.suspected_collusion",
payload)` を発火. payload には generation / collusion_score / n_agents.
人手が deny したら **その世代の派生集団は採用されない** という architecture
level の制御.

これは Constitutional AI / RLHF の **human-in-the-loop** を, **architecture
level** で代替する設計. 「prompt 最後に <human_review> を加える」のような
弱い制御ではない.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 4. Ed25519 + SHA-256 audit chain
<small><strong>EN:</strong> 4. Ed25519 + SHA-256 audit chain / <strong>中:</strong> 4. Ed25519 + SHA-256 审计链</small>

`src/llive/security/` 系. Phase 4 着地.
<small><strong>EN:</strong> src/llive/security/ family. Landed in Phase 4.<br>
<strong>中:</strong> src/llive/security/ 系列. 在 Phase 4 落地.</small>

- 各 PeerEvaluationMatrix / ChangeOp / consolidation event は Ed25519 で
  **署名**.
- ledger に書き込むときに **直前の hash** を含めて SHA-256 を計算 → next
  block の prev_hash として使う. つまり **blockchain-light**.
- これにより「過去の任意の record を改ざんすると, それ以降の hash が全て
  ずれる」 → 改ざん即検出.

### 4.1 なぜ on-chain ではなく on-disk か

`project_fullsense_ear_origin` — llive は EAR + セキュリティ制約で
**外部送信不可** の環境を想定. on-chain (Ethereum / Solana) は外部送信に
なるため不適. on-disk audit chain は外部依存ゼロで完結する.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 5. honest disclosure
<small><strong>EN:</strong> 5. Honest disclosure / <strong>中:</strong> 5. 诚实披露</small>

- **Ed25519 鍵管理は未解決** — 鍵を OS の secure store / HSM に保存する
  module は未着地. 現状は環境変数 / file 経由でロード. これは v1.0 前に
<small><strong>EN:</strong> The module is not yet landed. Currently loaded via env var / file. Must be fixed before v1.0.<br>
<strong>中:</strong> 该 module 尚未落地. 当前通过 env var / 文件加载. 必须在 v1.0 之前修复.</small>
  解決必須.
- **Approval Bus の人手介在は scale しない** — 派生集団 N=64 で 1 世代毎に
  approval が出ると人手の負荷が 24 時間で破綻する. policy 自動評価で 80% を
  通すのが現実解だが, policy が完璧に書ける保証はない.
- **runtime_metadata の sign は optional** — `signed_by` フィールドは
  慣習だが mandatory ではない. これを mandatory にすると `Brief API` の
  互換が壊れる. 移行は v0.7 以降.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 6. 本日 (2026-05-21) 着地サマリ
<small><strong>EN:</strong> 6. Today (2026-05-21) landing summary / <strong>中:</strong> 6. 本日 (2026-05-21) 落地总结</small>

| 項目 | 状態 |
|---|---|
| `CoevolutionGovernance` skeleton | **本日着地** |
| `CollusionDetector` (CE-06) | **本日着地** |
| `collusion_risk_score` (TonicRisk 連携, CE-08) | **本日着地** |
| `GovernanceReport` (frozen) | **本日着地** |
| 28 ケース test PASS | **本日着地** |
| Ed25519 audit chain | Phase 4 着地済 (v0.3.0) |
| Approval Bus | C-1 着地済 (2026-05-16) |
| runtime_metadata 慣習 | v0.B から運用中 |

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 7. Mermaid — governance 全体像
<small><strong>EN:</strong> 7. Mermaid - governance overview / <strong>中:</strong> 7. Mermaid - governance 全貌</small>

```mermaid
flowchart TD
    peer[PeerEvaluationMatrix]
    cd[CollusionDetector]
    cg[CoevolutionGovernance]
    ab[ApprovalBus]
    tr[TonicRiskMonitor]
    qm[QuarantinedMemory]
    led[Audit Ledger]
    human[Human / Policy]

    peer -->|3 指標| cd
    cd -->|suspected?| cg
    cg -->|request| ab
    cg -->|tick| tr
    ab -->|verdict| human
    human -->|approve/deny| ab
    ab -->|signed entry| led
    tr -->|alert| qm
    qm -->|isolate| led
```

### 7.1 governance maturity を「文明レベル」で見る — 4D Kardashev radar (v0.I-C 先取り)

§3 の Approval Bus pass率 / §4 の audit chain 完全性 / §6 の peer eval cohesion
<small><strong>EN:</strong> Approval Bus pass rate (§3) / audit chain integrity (§4) / peer eval cohesion (§6) are the three measurable axes.<br>
<strong>中:</strong> Approval Bus 通过率 (§3) / 审计链完整性 (§4) / peer eval 内聚度 (§6) 是三个可度量的轴.</small>
は, 単独で見ると「数字が良くなった」で終わる. **v0.I-C (4D Kardashev Radar)**
ではこれらを Energy / Knowledge / Coordination / **Ethics** の 4 軸 × 5 段階
(Type 0 → I → II → III → IV) の「文明レベル」スケールに束ねて, 個体 / 集団 /
メタ集団の 3 階層で同時計測する構想.

![4D Kardashev Scale](./assets/qiita_24_v0i_kardashev_4d_hero.svg)

Ethics 軸はまさに本記事の Approval Bus pass率 + frozen gene 違反検出 + 規制
適合度のスコアで, governance maturity を「個体の躾」から「文明の成熟」まで
連続スケールで語れるようになる. 詳細要件は llive `docs/requirements_v0.I_meta_evolution_and_cross_substrate.md` §5 参照.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 8. 期待値 — 次に来るもの
<small><strong>EN:</strong> 8. Expectations - what comes next / <strong>中:</strong> 8. 期望值 - 接下来要做的</small>

- **HSM / secure store 連携** — Ed25519 鍵管理を v1.0 で. Windows Credential
  Store / macOS Keychain / Linux Keyring 経路.
<small><strong>EN:</strong> Windows Store / macOS Keychain / Linux Keyring integration.<br>
<strong>中:</strong> Windows Store / macOS Keychain / Linux Keyring 集成.</small>
- **policy 自動 evaluate の拡充** — Approval Bus の `policy` 引数で 80% を
  自動通過させる規則を v0.7 で.
- **Audit Ledger UI** — llove TUI で `governance verdict ledger` を時系列
  可視化. F25 連携.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 9. 2026-05-22 追記 — RUST-16 governance hot path 高速化
<small><strong>EN:</strong> 9. 2026-05-22 addendum - RUST-16 governance hot path acceleration / <strong>中:</strong> 9. 2026-05-22 追记 - RUST-16 governance 热路径加速</small>

CoevolutionGovernance.evaluate_generation の中で最も計算量を食うのが
<small><strong>EN:</strong> The most compute-heavy part of CoevolutionGovernance.evaluate_generation is the bottleneck.<br>
<strong>中:</strong> CoevolutionGovernance.evaluate_generation 中计算量最大的部分是瓶颈.</small>
PeerEvaluationMatrix.collusion_score (NxN matrix の variance / symmetry /
concentration 3 指標) で, ここに 200-300 μs/call かかっていた.

本日 (2026-05-22) RUST-16 として **numpy zero-copy で Rust kernel 化**:

| N | Python (numpy 既存) | Rust pyo3 zero-copy | speedup |
|---:|---:|---:|---:|
| 8 | 217.82 us | 1.89 us | **x115.04** |
| 16 | 203.33 us | 2.30 us | x88.54 |
| 32 | 237.68 us | 5.28 us | x45.00 |
| 64 | 306.13 us | 16.80 us | x18.22 |
| **avg** | — | — | **x66.70** |

実装は `crates/llive_rust_ext/src/lib.rs:collusion_score_kernel` + 5 parity
test (1e-6 tolerance). callers (`CollusionDetector.check`) は次 commit で
切替予定.

### 9.1 honest disclosure — 「numpy = 速い」も嘘

このゲインが大きいのは **「Rust が速い」だけでなく「numpy が小 NxN で遅い」**
が主因. `np.nanvar` / `np.corrcoef` / `np.nanmean` の 3 つ重ねがけは
N<100 で Python overhead 支配で 200μs+/call. Rust の単純 C ループは 2μs/call.

governance 側で重要なのは:

- **Approval Bus 発火判定の latency が 100x 短くなる** = N=64 派生集団でも
  governance.evaluate_generation を 64Hz で回せる
- **TonicRiskMonitor の tick** (collusion_risk_score を含む state を渡す)
  も同等に速くなる
- 結果として **「governance を常時動かしても許容コスト」**になる

これがあれば「**governance は重いから sampling だけ**」の妥協が要らなくなる.
全派生 / 全世代の評価行列を audit chain に署名つきで残しても latency budget
内に収まる.

### 9.2 関連

- `docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md` —
  全 3 kernel (RUST-15/16/17) の比較マトリクス
- `scripts/bench_collusion_score_5x_gate.py` — N=8/16/32/64 5x gate bench
- `feedback_rust_usage_matters` — Rust 化判断のチェックリスト

---

> draft (10x volume 版は次セッション). 骨子 + 9 main section + Mermaid +
> honest disclosure 4 件 (新規: numpy 小 N でも遅い + governance latency
> 100x 短縮).

---

## Series Navigation

- ← 前: [llive 完全解説 (6) 「Transformer の外」](https://qiita.com/furuse-kazufumi/private/6da5a883fb2ed651edd8)
- → 次: [llive 完全解説 (8) 「眼鏡を作る」](https://qiita.com/furuse-kazufumi/private/e49b7ab9027d93594402)
- 全体: [llive 完全解説 (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
