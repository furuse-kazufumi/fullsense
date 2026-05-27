# llive 北極星アーキテクチャ — ブロック図と「矛盾→単純化」設計 (2026-05-27)

> 目的: 拡張示唆 (統計ペルソナ / meta dispatch / router / ablation) を積みすぎて複雑化したため、**全体をブロック図で俯瞰し、矛盾を単純化方向で解消**する (ユーザー指示)。設計原則: **矛盾を含む箇所は単純化を優先**。

## 北極星
**連続進化 × ライブ MoA オーケストラ** — 進化し続ける多様な個体集団を、答えが要る瞬間に competence-aware routing (指揮者) で合奏させ 1 答する。

## ブロック図

```mermaid
flowchart TB
  F["入力: persona founders + c_factors"]

  subgraph CORE["① 進化エンジン = コア (確定・最小)"]
    direction TB
    P["Population"] --> EV["評価 (pressures / fitness)"]
    EV --> SEL["選択 = lldarwin<br/>ε-lexicase + novelty + 中立貯蔵庫"]
    SEL --> BR["交配・変異"]
    BR --> P
  end

  subgraph ARCH["② QD archive = 奏者カタログ (成果物)"]
    ME["MAP-Elites<br/>behavior descriptor"]
  end

  subgraph META["③ meta 層 = 奏者の多様性源 (拡張対象・ablation で検証)"]
    MC["c_meta: algorithm_id<br/>ペルソナ駆動アルゴリズム選択 (META-1)"]
  end

  subgraph ORCH["④ router = 指揮者 = 北極星本体 (未実装・Phase B)"]
    R["competence-aware routing<br/>(QD descriptor を流用)"]
  end

  F --> P
  P --> ME
  MC -. "persona → algorithm 切替" .-> SEL
  MC -. "persona → algorithm 切替" .-> BR
  ME --> R
  R --> OUT["1 答 = 合奏出力"]
```

## 層の役割と確度

| 層 | 役割 | 確度 | 構成 |
|---|---|---|---|
| ① 進化エンジン (コア) | 多様な奏者を絶やさず進化 | **確定** (proxy ablation 裏付け) | ε-lexicase + novelty + 中立貯蔵庫 + コア24本 |
| ② QD archive | 奏者カタログ (descriptor で索引) | コア候補だが proxy では選択圧に再帰せず | MAP-Elites |
| ③ meta 層 | 奏者ごとにアルゴリズムを変える多様性源 | **拡張対象** (要 ablation) | c_meta / MetaChromosome / dispatch (要配線) |
| ④ router (指揮者) | 奏者を選び合奏 = 北極星本体 | **未実装** (Phase B) | competence-aware routing |

## 矛盾 → 単純化 (設計判断)

進化研究では「矛盾を統合で解く」のが理想だが、本フェーズは**キャパ制約下の収束**なので **TRIZ #1 分離 / 単純化を優先**する。

1. **矛盾: 収束 (frozen で機能削減) ↔ 拡張 (meta/統計ペルソナ追加)**
   → **単純化**: 「コアは①の最小固定。②③④の拡張は **1 つずつ** ablation で寄与率を測って足す/淘汰」。同時に複数を積まない (今回複雑化した反省)。拡張↔縮小は**逐次**回す。

2. **矛盾: proxy で削減候補 (adaptive_difficulty / factor_subspace_qd / map_elites) ↔ 実 LLM では効く設計**
   → **単純化**: **デフォルトを単純側に倒す**。proxy で効かない要素は **既定 off** にし (lldarwin v2 既定の見直し候補)、実 LLM ablation で有意な効果が出た要素だけ既定 on に昇格。「効果が証明されるまでは付けない」。

3. **矛盾: 多様性 (novelty/QD) ↔ 品質 (適応難易度の選択圧)**
   → **単純化**: **ε-lexicase が構造的に両立**を担う (集約しない多目的選択 = 各軸の specialist が共存)。追加の調整器 (adaptive 等) は「lexicase で足りない分だけ」最小投入。調整器を増やす前に lexicase の軸設計を見直す。

4. **矛盾: meta (個体ごとに algorithm 違う) ↔ 単純なループ (全個体同じ algorithm)**
   → **単純化**: meta は **c_meta の algorithm_id を 2-3 個の離散選択に限定**して始める (連続パラメータ空間でなく)。persona → algorithm の写像も最初は単純な表引き。効けば拡張。

## 当面の単純化アクション (Phase A 締め → B)

- **コア確定**: ①(ε-lexicase + novelty + reservoir + コア24本) を「変えない土台」とする。
- **既定の単純化**: lldarwin v2 の proxy 無効要素 (adaptive/factor-subspace) を**既定 off に倒す**ことを検討 (実 LLM で昇格)。← 矛盾2 の解消。
- **拡張は逐次**: ④ router を**最小の 1 機能**として次に実装 (meta③ はその後、1 つずつ)。
- frozen (experimental/) で①外を隔離しコアを小さく保つ。

## HONEST
本図は設計の現時点スナップショット。proxy 限界 (①の ablation 裏付けは proxy mechanism feasibility) と未実装 (④) を明示。実 LLM 段で②③④の確度が変わる。新 doc は `docs/research/index.md` / `doc_map.md` に登録すること ([[feedback_fullsense_feedback_smart]])。
