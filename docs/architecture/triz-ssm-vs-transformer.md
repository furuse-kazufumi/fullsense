# TRIZ 検討: SSM (Mamba) vs Transformer — FullSense (llive on-prem) 文脈 (draft v0.1)

> 2026-05-18 作成. FullSense の Local LLM 制約下で、Transformer 一強の対抗軸
> として SSM (Mamba) ファミリーを TRIZ で構造化する設計検討メモ.
>
> 出典は Qiita / Zenn / Reddit / 論文サイト等のレビュー記事群 (参照は §8).

## 0. なぜ TRIZ で扱うか

「Transformer は強い、でも長コンテキスト × on-prem には重い」という現象は
**典型的な技術矛盾**. 強くしたい特性を上げると別特性が悪化する状況なので、
40 原理から「両立する解」を探すのが本来の TRIZ の用途. SSM はこの矛盾を
原理レベルで切り崩しているので、原理に分解すると採用判断がはっきりする.

---

## 1. 矛盾の定式化

### 1.1 物理矛盾 (1 つの主体に対する正反対の要求)

「**系列モデルの内部表現は、長系列に対して完全 (Transformer の全 attention)
であり、かつ、計算は短系列並みに軽くあれ**」 — 同じ物体 (系列モデル) に
対して「完全性」と「軽量性」の正反対要求が同時に課される.

### 1.2 技術矛盾 (TRIZ 39 特性で表現)

| 改善したい特性 | 悪化する特性 |
|---|---|
| #9 Speed (推論速度) | #36 Complexity of device (実装の難しさ) |
| #19 Use of energy by moving object (推論時エネルギー) | #13 Stability of object (品質安定性) |
| #25 Loss of time (応答遅延) | #33 Convenience of use (既存エコシステム整合性) |
| #39 Productivity (スループット) | #28 Accuracy of measurement (生成品質) |

→ TRIZ 矛盾マトリクスで上位に出る原理 (経験則): **1, 5, 15, 17, 35, 37**.

詳細解説は §3 で各 SSM/Mamba の設計選択にマッピング.

---

## 2. SSM/Mamba ファミリー概観 (FullSense 候補目線)

| モデル | 系統 | 推論 | 訓練 | 系列線形性 | OSS / ライセンス | FullSense 取込 fit |
|---|---|---|---|---|---|---|
| **S4** (Gu+ 2022) | 構造化 SSM | O(L) | O(L log L) | ✓ | OSS (MIT) | 古典、ベンチ基準 |
| **S5** / DSS | S4 派生 | 同上 | 同上 | ✓ | OSS | 派生として参照 |
| **Mamba** (Gu+Dao 2023) | Selective SSM | O(L) | O(L) | ✓ | OSS (Apache-2.0) | **第一候補**. Codestral-Mamba (7B) が実用品質 |
| **Mamba-2** (2024) | SSM = Attention 等価 | O(L) | O(L) | ✓ | OSS | Transformer との数学的橋渡し |
| **Jamba** (AI21, 2024) | Mamba + Attention hybrid | mixed | mixed | △ | OSS (一部) | **EAR 制約下で実運用候補** |
| **Codestral-Mamba** (Mistral, 7B) | Pure Mamba LLM | O(L) | O(L) | ✓ | Apache-2.0 | 軽量 + 256k context |
| **Sigma** (vision) | Mamba 派生 | O(L) | O(L) | ✓ | OSS | mcp-3d 連携候補 |
| **Falcon-Mamba** (TII, 7B) | Pure SSM LLM | O(L) | O(L) | ✓ | TII Falcon LLM 1.0 | 中東 origin、検閲リスク要確認 |

**EAR + on-prem 制約での絞り込み**:
- Apache-2.0 系 (Mamba, Codestral-Mamba, Mamba-2) が安全
- TII Falcon は地政学的に要確認
- 中国製 SSM (まだ少ないが) は別途検討

---

## 3. 40 原理 → SSM/Mamba の設計選択マッピング

矛盾マトリクスから推奨される原理を、Mamba の具体的な設計判断と対応付ける.

### 3.1 原理 1 — Segmentation (分割)

**応用**: Mamba は系列長 L に対し、**隠れ状態 h_t を時間方向に分割保持**.
Transformer は全 token を一度に attention するが、Mamba は時刻ごとに
状態を更新する RNN 形 → メモリ占有が O(state_dim) で L に依存しない.

**FullSense 適用**: llive の memory layer (4 階層) と相性が良い.
`Working / Episodic / Semantic / Procedural` を SSM 隠れ状態の **subspace**
として保持できる. memory layer は既に「分割」されているので、その上に
Mamba を被せると階層全体の状態更新が線形コスト.

### 3.2 原理 5 — Merging (統合)

**応用**: **Jamba** は Mamba ブロックと Attention ブロックを層ごとに統合.
全 Attention にすると重く、全 Mamba にすると in-context learning が弱い
ので、**層単位で交互**にする.

**FullSense 適用**: llive 6 stage の **stage ごとに backend を選ぶ**設計が
TRIZ 的に整合.
- Salience Gate / Curiosity Drive → 軽量 Mamba
- Inner Monologue → 表現力重視で Transformer (cloud 不可なら Jamba)
- Ego/Altruism Scorer → 軽量 Mamba
- Action Plan → ハイブリッド
- Finalise → Transformer

`LLIVE_LLM_BACKEND` を **stage 単位で切替可能**にする env 拡張は要件として
立てる価値あり (現状は global 1 backend).

### 3.3 原理 15 — Dynamics (動的化)

**応用**: **Selective SSM (= Mamba 本体)**. 状態遷移パラメータ Δ, A, B, C
を **入力 token に依存して動的に変える**. 古典 SSM (S4) は時不変だったが、
Mamba は時変化 = 入力に追従.

**FullSense 適用**: llive `10 思考因子` (uncertainty / structurize / reconstruct
等) を、**Δ パラメータの動的調整器**として組込可能.
不確実性が高い token では Δ を小さく (短期記憶に依存)、整合的な情報なら
Δ を大きく (長期に統合). llive 思考層から SSM 状態への直接介入が
architectural-level に成立する.

### 3.4 原理 17 — Another dimension (次元移行)

**応用**: Transformer は **系列方向 (L) × 表現方向 (D)** の 2 次元 attention.
SSM は **系列方向を時間 (state machine 1 次元)** に押し込み、表現方向 (D)
のみ並列化. つまり「もう 1 次元 (時間軸) を別概念に変換」.

**FullSense 適用**: llive Annotation Channel は時間的 emit イベント列なので、
**Annotation を SSM の入力 token と等価視**できる. Annotation を直接
Mamba に流す bridge を作ると、思考因子の発火履歴がそのまま LLM の文脈に
入る (現状は string 化して prompt に詰める).

### 3.5 原理 35 — Parameter changes (パラメータ変更)

**応用**: SSM の**離散化ステップサイズ Δ**を可変にして連続/離散の切替を
パラメータレベルで制御. これが Mamba の core idea.

**FullSense 適用**: llive `MathVerifier` で連続値検証する経路 (MATH-08)
を、SSM の Δ パラメータ計算に流用可能. **思考因子から Δ への可微分
パイプライン**を作れば、思考の確実さが LLM 推論の解像度を直接制御する
(他にない設計).

### 3.6 原理 37 — Thermal expansion (温度展開 → 文脈展開と読み替え)

**応用**: SSM は **HIPPO 行列**で過去全体を圧縮表現する (= 「展開」した
過去を低次元で保持). Transformer は全 KV cache を持つ ↔ SSM は HIPPO で
情報損失最小化しつつ圧縮.

**FullSense 適用**: llive の `feedback_benchmark_progressive_tokens` で
xs/s/m/l/xl 5 段階の stress curve を取る要件があるが、SSM ベース backend
なら **xl (>100k token) でも latency が線形**で測れる. 競合 (Transformer
cloud API) との crossover 可視化が綺麗に出る (memory `feedback_llive_measurement_purity`
の 2 系統分離ベンチに有利).

---

## 4. FullSense (llive) への適用設計案

### 4.1 短期 (Phase h+1 / Month 2, 実装可能)

- **`LLIVE_LLM_BACKEND=mamba:<model>`** 新規 backend 追加
  - `MambaBackend` クラス (`OpenAIBackend` と同じ interface)
  - llama.cpp が Mamba を一部サポート開始 (b3000 系〜) → `llama-server` 経由
    で `LLIVE_LLM_BACKEND=openai` + `OPENAI_BASE_URL=...` + Codestral-Mamba の
    .gguf を指せば **既存 OpenAI 互換経路で動く** (改修ゼロ)
  - または mamba-ssm 公式 PyPI 経由で in-process backend
- **bench: progressive matrix xl/xxl (256k token) 計測**
  - memory `feedback_benchmark_progressive_tokens` の自然な拡張
  - SSM vs Transformer の crossover 点を on-prem で実測 → honest disclosure
    (memory `feedback_benchmark_honest_disclosure` 厳守)

### 4.2 中期 (Phase 5 / Month 3-4)

- **stage 単位 backend 切替** (`LLIVE_LLM_BACKEND_BY_STAGE` JSON env)
  - Salience / Curiosity / Ego → Mamba
  - Inner Monologue / Action Plan → Transformer or Jamba
  - 6 stage の重みづけ計測で実効性確認
- **思考因子 → SSM Δ パラメータ橋渡し**
  - llive 思考層が SSM 内部状態を制御する PoC
  - mcp-3d の VQ 量子化 ([[project_precision_metrology_llm]]) との結合可能性

### 4.3 長期 (Phase 6+ / Month 5-12)

- **Mamba ベース llive 専用 LLM の事前学習**
  - 軽量 7B / 13B Codestral-Mamba 派生で llive Annotation を pre-training 入力に
  - 中国 LLM (Qwen-Mamba 派生があれば) の動向次第で組合せ
- **mcp-3d v4 候補**: 3DGS SH 係数 VQ → Mamba 256k context で空間データを
  LLM トークン化 ([[project_precision_metrology_llm]] と直結)

---

## 5. 論文化 / 差別化軸

memory `feedback_benchmark_honest_disclosure` と
`project_llive_dev_style` (第二の脳型スパイラル開発) を踏まえると、論文化
ネタとして以下が成立:

1. **「思考因子 → SSM Δ パラメータ」橋渡し** — llive 独自で、Transformer ベース
   既存 LLM では実装不能 (動的 Δ がない). 認知科学 × アーキテクチャの新規軸.
2. **stage-wise backend 切替の効率/品質トレードオフ** — 6 stage × 2 backend
   行列を on-prem only で計測. cloud LLM と差別化.
3. **mcp-3d × Mamba 256k context** — 精密計測 + LLM の長コンテキストで、
   空間アセットを LLM が直接「読む」 ([[project_precision_metrology_llm]]).
4. **Local LLM コスト面 honest disclosure** — Transformer 70B vs Mamba 7B の
   実 latency / energy 比較. 「Mamba 7B で Transformer 70B 並の品質に
   到達するか?」を progressive matrix で測る.

---

## 6. リスク / 反論への備え

| リスク | 対応 |
|---|---|
| Mamba は in-context learning が Transformer より弱い (実測ベース) | Jamba (hybrid) を主軸. Pure Mamba は backend 候補に留める |
| llama.cpp Mamba 対応がまだ若い | OpenAI 互換 (vLLM の Mamba 対応) も並行 |
| Codestral-Mamba は Mistral ライセンス (商用 一部制限) | Apache-2.0 の Mamba ベースモデルに切替可能性 |
| 知名度低い → 普及障壁 | FullSense は EAR + on-prem 起源で、知名度より制約解消が優先 |
| SSM は文脈長を伸ばすほど性能劣化が報告されている | xs/s/m/l/xl progressive matrix で実測、honest disclosure |

---

## 7. 撤退条件

- progressive matrix xl で Mamba が Transformer 70B より品質 5pt 以上劣る
  → Mamba は補助 backend 扱い、主軸は Transformer に戻す
- stage-wise backend 切替の効率改善が < 20% → 設計凍結
- ライセンス問題で商用配布できないモデルしか無いと判明 → 中国 LLM 経路に
  寄せる (memory `feedback_qwen_commercial_barrier` に注意)

---

## 8. 参考文献 / 出典

- Gu, Dao et al. *Mamba: Linear-Time Sequence Modeling with Selective State Spaces* (2023)
- Mamba-2 paper (2024): SSM ↔ Attention 数学的等価性
- AI21 Labs *Jamba* technical report (2024)
- Mistral *Codestral Mamba* model card (2024)
- Reddit /r/LocalLLaMA *Alternative to Transformer architecture LLMs* (2025-09)
- Zenn / Qiita / GIGAZINE / 各種日本語レビュー記事 (本セッション貼付分)
- 本検討の TRIZ 文献: Altshuller *Innovation Algorithm* + Mann *Hands-On Systematic Innovation*

---

## 9. 次の TRIZ 軸候補 (本検討の続き)

本軸 (SSM vs Transformer) は **on-prem 文脈 × 長コンテキスト** に絞った.
直交する軸として:

- **stage-wise backend mix** TRIZ — 6 stage × 4 backend (Transformer / Mamba /
  Jamba / Diffusion) の組合せ最適化. これは別 docs で扱う.
- **on-prem inference vs cloud API** TRIZ — コスト × 品質 × 越境.
  `data-sovereignty.md` と密結合.
- **llive 思考因子 vs LLM 内部表現** TRIZ — 認知科学側の TRIZ.
  [[project_llive_cog_fx_factors]] / [[project_llive_oka]] と接続.

---

## 改訂履歴

- 2026-05-18 — draft v0.1 (Qiita / Zenn / Reddit ベース + TRIZ 40 原理マッピング +
  Mamba ファミリー整理 + FullSense 短期/中期/長期適用案 + 論文ネタ 4 件)
