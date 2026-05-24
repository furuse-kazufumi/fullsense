---
layout: default
title: "Gemini ブレスト #3/#4 実装着地 (Antifragile / Speculative Mesh)"
parent: "Research"
nav_order: 96
---

# Gemini ブレスト #3/#4 実装着地メモ (2026-05-24)

> Gemini 発ブレスト 4 案 ([`project_user_brainstorm_2026_05_22`]) のうち **#3 Antifragile
> Mutation (llive)** と **#4 Speculative Mesh Execution (llmesh)** を本日 PoC 着地。
> いずれも統合発見 **予測符号化アーキテクチャ**
> ([Ideation Marathon]({{ '/research/ideation_marathon_expression_realtime_2026_05_23' | relative_url }})
> 発見A) と親和する。本メモは各 repo 実装の **FullSense 側フィードバック** (技術資料取り込み用)。

---

## 0. 位置づけ — ブレスト 4 案の進捗

| # | アイデア | 着地状況 |
|---|---|---|
| #1 | 予測検証メタゲート (Z3/TLA+ で verifier コスト削減) | 未実装 (memory `project_idea_predictive_verification`) |
| #2 | KV-cache memory translator (4層メモリを mesh 間 KV 差分共有) | 未実装 (memory `project_idea_kv_cache_memory_translator`) |
| **#3** | **Antifragile Mutation** (高 surprise→panic で探索爆発) | **着地 (llive `f2c2d1e`)** ← 本メモ |
| **#4** | **Speculative Mesh Execution** (思考リレー) | **着地 (llmesh `2a05f64`)** ← 本メモ |

予測符号化との関係: #4 は「予測 (分岐) を先に立て、mesh で先回り実行」= **予測符号化の
分散版**。#3 は「予測誤差 (高 surprise) を学習トリガに変える」= **予測誤差を捨てずに活かす**。

---

## 1. #3 Antifragile Mutation — llive `src/llive/evolution/antifragile.py`

commit `f2c2d1e` / **28 tests passed** / ruff + mypy strict green / Python 3.11 / stdlib + numpy。

**何**: Nassim Taleb の反脆弱性を進化計算へ。llive は通常、高 surprise / エラーで
**fail-closed** (守りに入る) が default。本機構は **opt-in** で逆の選択肢を与える —
高 surprise を「学習機会」と捉え **panic mode** へ遷移し探索を一時増幅する。

| 要素 | 内容 |
|---|---|
| トリガ | `BayesianSurpriseGate` の動的閾値 (`mu + k·sigma`) 超過で panic 遷移 |
| 探索増幅 | panic 中のみ UCB1 exploration constant を **10x** (`ucb_clip` で UCB bound へ clamp 可) |
| 対立 unlock | 通常 filter する相反 TRIZ 原理 pair (#1分割×#40複合材料 等) を panic 中だけ同時適用許可 |
| 監査 | panic 中の全 ChangeOp を `AuditTrail` の SHA-256 hash chain に署名記録 |
| 復帰 | cooldown (既定 5 分) 経過 / surprise 回復 (hysteresis) / Approval Bus user 停止 |
| honest disclosure | `disclosure()` が episode 別 hit/success/loss/滞在時間を時系列集計 |

**設計判断 (FullSense 哲学整合)**:

- **fail-closed default は崩さない** — `AntifragileConfig.enabled=False` が既定。
  opt-in / `LLIVE_ANTIFRAGILE_AUTO=true` でのみ有効化。
- **Approval Bus を迂回しない** — controller は探索パラメータ増幅と監査記録のみ。
  panic 中の重大変更も通常どおり approval が必要。
- **既存進化 driver には未配線** (疎結合) — gem-critic 指摘の driver genome 不整合
  ([`project_llive_evolution_next_session`]) は本機構の対象外。

---

## 2. #4 Speculative Mesh Execution — llmesh `llmesh/speculative/`

commit `2a05f64` / **23 tests passed** / ruff + mypy strict green / Python 3.11。

**何**: CPU の分岐予測を **agent level** へ。メイン推論中に予測した分岐を、llmesh の
**暇な peer** へ Ed25519 署名付きで投機投入し、到達時に mesh から回収 (cache hit) する。
[`project_llmesh_p2p_winny`] の P2P mesh と整合。本 PoC は **Phase 2 (投入) + Phase 3 (回収)**
を担い、Phase 1 (分岐予測) は推論エンジン側 (llive MetaMutation 拡張) に委ねる。

| モジュール | 役割 |
|---|---|
| `manifest.py` | `SpeculativeManifest` (deterministic canonical_bytes / sha256 `manifest_hash` = mesh cache key) + `SignedManifest` + `sign_manifest(NodeIdentity)`。自ノード以外の origin 署名は拒否 (fail-closed) |
| `coordinator.py` | `SpeculativeMeshCoordinator`: LAN-first idle node 選択 (負荷スコア + VRAM hard filter) / 署名投機投入 / `submit_result` の Ed25519 検証 (fail-closed) / `pull` で hit-miss / `discard_unpulled` で空振り計上 |
| metrics | `SpeculativeMetrics` + `disclosure()`: hit_rate / wasted_compute_ms / wan_dispatches / signature_rejections |

**設計判断 (constraints `ed25519-sign-required` / `honest-disclosure-required` 準拠)**:

- **Ed25519 署名必須** — `llmesh.auth.signer` と同じ canonical bytes 上の署名。mesh で
  受信した manifest が本当に自分発かを検証、改ざん / 誤配は **fail-closed** で拒否。
- **LAN-first** — `require_lan=True` 既定。WAN は往復が swap より遅い前提で別カウント
  (`wan_dispatches`)。損益分岐は `docs/perf_comparison/speculative_mesh.md` に方法論。
- 実 mesh transport / 実 executor は **未配線** (PoC は ready-made manifest を消費し
  lifecycle を検証)。

---

## 3. 公開フィードバック — 1 週間ダイジェスト記事

両着地を含む 1 週間 (2026-05-17 → 05-24) の進捗を 4 言語ダイジェストに統合:
`docs/articles/QIITA_WEEKLY_DIGEST_2026-05-17_to_24.md` (JA/EN/ZH/KO, `ignorePublish: true`)。
2026-05-17 の 3 本柱 (Brief API / COG-FX 10 因子 / MATH) を**予測符号化という背骨**に接続。

---

## 4. honest disclosure / 次

- **#3 Antifragile**: 「自己破壊で次の安定へ」が本当に効くかは**未検証**。panic の
  success/loss 率を追う計測基盤を入れただけ。実 loop への配線 + 効果定量化が次。
- **#4 Speculative Mesh**: 得をするのは hit_rate が高く **かつ** mesh 往復 < ローカル swap
  のときだけ。WAN は負ける前提。実 transport / executor 配線 + ベースライン測定が次。
- **#1/#2 は未着手** — #1 (予測検証メタゲート) は #3/#4 双方の verifier コスト削減と
  親和、#2 (KV-cache translator) は #4 と署名スキーム共通で結合余地あり。
- プロジェクト間の結合 (要素統合) 判断は**ユーザー** (勝手に結合しない / FullSense 規約)。

---

## Sources / 関連

- 上流: [Ideation Marathon (表現×リアルタイム)]({{ '/research/ideation_marathon_expression_realtime_2026_05_23' | relative_url }}) 発見A=予測符号化アーキテクチャ
- 姉妹実装: [予測符号化 push PoC]({{ '/research/predictive_push_poc_2026_05_24' | relative_url }}) (発見A の別具現)
- 実装 #3: llive `src/llive/evolution/antifragile.py` (commit `f2c2d1e`)
- 実装 #4: llmesh `llmesh/speculative/` (commit `2a05f64`) + `docs/perf_comparison/speculative_mesh.md`
- ブレスト集約: memory `project_user_brainstorm_2026_05_22` / `project_idea_antifragile_mutation` / `project_idea_speculative_mesh_execution`
