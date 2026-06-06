# llcore 差別化監査 + 特別 DNA ロードマップ (2026-06-06)

> 敵対的差別化監査 (Workflow 56 agents) の確定結果と、TRIZ に基づく差別化強化の優先度付き実行計画。
> 戦略前提 = memory `project_special_dna_strategy`: 計算リソース制約下で差別化 trait を積層し
> 「特別な DNA を持つニッチ種」を狙う。順番の原則 = 計画 → 小 PoC → 大 PoC → 組込み、進化の行き止まり回避。

## 1. 監査の方法 (再現可能性のため)

- 敵対的 Workflow: 7 角度の反証探索 (証明ゲート系譜 / certified training / Transformer 安定性 / 進化×検証 /
  verified memory / runtime assurance / 産業・特許) + critic が指摘した盲点 3 角度の追加探索
  (形式手法会議側逆引き / certified continual learning 語彙系 / 内部状態・SSM 解釈)。
- 44 候補を 5 軸ルーブリック (gatesUpdates / soundProof / llmMemoryCore / evolutionLoop / implemented) で
  個別判定。判定 agent は一次情報 (arXiv abstract/html) を WebFetch で必ず確認。
- 並行して internal agent が PAPER_DRAFT.md と research/ から自己申告の脆弱点を抽出 (honest disclosure)。

## 2. 確定結論

**breaks 0 / narrows 36 / background 8 (44 件)。**

生存する差別化核 = **四点交差点**:

> **sound contraction 証明 (閉形式 ∞-norm / SDP-Lyapunov) × Transformer 記憶コアの内部 dynamics ×
> 進化/更新ループ内の prove-then-reject ゲート (fail-closed) × 動く実装+実験**

この 4 条件を同時に満たす先行は、盲点角度の追加探索後もゼロ。
ただし**現行クレーム D1-D4 の文言は広すぎて、そのままでは複数の先行に反証される** (§4 で再定義)。

## 3. 防御壁リスト (related work に編入すべき主要 narrows)

| 先行 | 何をやっている | なぜ交差点を埋めないか (差別化線) |
|---|---|---|
| SSGM (arXiv 2603.11768, 2026) | LLM agent memory bank の write gate (NLI 矛盾検出) を理論アーキとして提案 | **理論のみ・実装ゼロ**、証明は非形式 (Proof Sketch)。D2 の看板 (governing evolving memory) を先取り |
| SEVerA (2603.25111, 2026) | 自己進化エージェント合成に Dafny 演繹検証、実装あり | 検証対象は**合成プログラムの仕様準拠**。重み更新は un-gated、contraction なし |
| PSV / AlphaVerus (2025) | 形式検証を self-play / bootstrap のループ内ゲートに、実装あり | ゲート対象は**生成解 (code/math) の正しさ**であって重み/記憶の数学的性質でない |
| Provably Safe Model Updates / LID (2512.01899) | 更新の δ-safe を抽象解釈で保証、実装あり | **射影 (project-then-accept)** で prove-then-reject でない、対象は frozen embedding 上の分類 head |
| GP × Model Checking (1402.6785, 2014) | 進化ループ内に時相論理モデル検査ゲート | **設計パターンの先例** (引用必須)。対象は古典並行プログラムで記憶コアでない |
| Gödel Machine 実装 (Steunebrink 2011/12) | 記号的 proof-gated 自己改変の走る VM | 古典記号 proof search × 記号コード。connectionist でない |
| Enforced Lipschitz Transformers (2507.13338) / R2DN (2504.01250) | **by-construction** で contraction/Lipschitz を強制、Transformer 適用あり | 構造強制であり「任意更新を証明して棄却する」ゲートでない。表現力を構造で縛る対抗解として明示対比 |
| Safeguarded AI (ARIA) | proof-gated gatekeeper の最有力概念 (£59M programme) | **行動/出力**のゲート。重み/記憶更新でなく、shipped 実装なし |
| Emergent Formal Verification (substrate-guard) | Z3 で AI **出力**を検証する実装 | post-hoc 監視であり per-update ゲートでない |
| STABLE / certified continual learning 系 | forgetting/stability bound で更新をゲート | 統計的/数値的 bound であり sound 形式証明でない (語彙違いの最近接系統) |

## 4. クレーム再定義 (D1'-D4') — Phase 0 の実体

- **D1'**: 「SMT × 自己改変」一般の不在主張は**撤回** (SS-GM/Emergent FV が反例)。新文言 =
  「*sound な contraction 証明を、Transformer 記憶コアの重み更新そのものに対する進化ループ内
  prove-then-reject ゲートとして用い、実装+実験で実証した例は (我々の探索範囲で) ない*」。
  by-construction (R2DN/Lipschitz Transformers) との対比 1 文を必ず添える。
- **D2'**: 「verified memory evolution は未踏」→「*SSGM が同応用枠を NLI ベース理論アーキとして
  先取りしたが、sound 形式証明によるゲート + 動く実装は未踏*」。SSGM を明示引用。**時間窓が閉じつつある**。
- **D3'**: 「既存自己進化のゲートは性能/governance のみ」→「*証明ベースゲートを持つ自己進化系
  (SEVerA/PSV/AlphaVerus) は登場したが、検証対象は生成物の仕様準拠であり、進化する重み/記憶の
  解析的性質 (contraction) を毎更新ゲートする例はない*」。
- **D4'**: 「検証派は制御系 dynamics 限定」は維持しつつ、(a) Safeguarded AI (行動ゲート) との対比、
  (b) 内部状態解釈 (Hopfield/SSM/linear attention の安定性解析) を related work に先回り編入。

## 5. honest 内部脆弱点 (internal agent 抽出、要対処)

1. **Z3 看板と実装の乖離**: 論文本体のゲートは Z3 不使用 (閉形式 ∞-norm / 頂点 SVD / SDP-CLARABEL)。
   C_VERDICT.md 自身が「Z3 は decorative」と結論済み。→ 看板を「sound contraction certifier ladder」へ修正。
2. **出荷 API 未配線**: 証明ゲートは research/verified_evolution/gated_evolve.py のみ。
   src の evolve() (evolution/minimal_ga.py) は無検問 (grep で確認済)。
3. **規模留保**: 本体 n=8 (gene 72 実数)・16KB corpus・byte vocab。「LLM 記憶コア」は機構実証の意味に限定。
4. **L3 縮小済**: verifier 強度の payoff は navigability (進化の探索可能性) であって learning でない。
   EA 固有で gradient では消える。

## 6. 特別 DNA ロードマップ (優先度順)

> 各 Phase は前 Phase の踏み石。行き止まり回避欄 = 「これが死んでも何が残るか」。

| Phase | 内容 | 規模 | 行き止まり回避 |
|---|---|---|---|
| **0. 文言・防御壁 (即時, コスト≈0)** | D1'-D4' 再定義 + §3 防御壁を PAPER_DRAFT related work に編入 + Z3 看板修正 | 編集のみ | 全後続の前提。誇張のまま進むと査読一撃 = 最大の行き止まり要因を先に除去 |
| **1. 組込み (実証済→製品面)** | (a) G1: gated_evolve を src evolve() に additive flag で本配線 (b) G3: tracking tube レポータ組込み (本日 PoC 済: 契約 PASS 3/3 が tube 内、非契約は 9.3 倍増幅) | 小 | どちらも既に研究実証済 = リスク最小。配線が Phase 2 のゲート差し込み口になる |
| **2. 小 PoC (時間窓あり, 最優先研究)** | (a) **G2: verified memory evolution 小 PoC** — SSGM が理論で看板先取り、実装先取りの窓が閉じる前に着地 (b) SPC 管理図を進化メトリクスの runtime ゲートに転用 (llmesh エンジン配線のみ) | 小→中 | G2 は競合空白の本丸。失敗しても D2' の「我々は試して◯◯が壁」という honest 一次情報が残る |
| **3. 中 PoC (防御の深掘り)** | (a) metamorphic gate (llive 構造不変量→振る舞い不変量) (b) 内部状態解釈の related work 防御 (Hopfield/SSM/RWKV 安定性) (c) 特許 DB 照会 (既知の穴) | 中 | (b)(c) は調査であり実装リスクなし |
| **4. 大 PoC / 統合** | 検証器殻地形 (地形改造 E 案) × G2 の合流 = 「証明ゲート下の記憶進化」を多峰地形で立たせる / ファミリー統合デモ (llive Approval Bus × llcore gate × llmesh SPC) | 大 | Phase 1-3 の trait が全て踏み石として再利用される設計 |
| **継続 (並行)** | G5 ペルソナ (済: 進化派 3 名 + 古典 2 名進行中) / G8 Sakana 統合 corpus (進行中) / G14+ 古典 DNA (進行中) / G13 safety tax 測定値の発信 | — | 失敗概念なし (資産蓄積) |

## 7. 残リスク (honest)

- 特許 DB (USPTO/JPO/Google Patents) は専用照会未実施 — 不在証拠として弱い。
- 形式手法会議 (CAV/TACAS) tool paper の逆引きは 1 ラウンドのみ。
- D2 の実装先取り窓は**時間依存** — SSGM 系の後続実装が出れば閉じる。Phase 2(a) の優先度はそのため。
- 「探索範囲で未踏」の留保は常に維持する (網羅証明は不可能)。
