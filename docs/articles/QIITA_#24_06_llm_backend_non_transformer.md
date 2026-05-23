---
title: llive 完全解説 (6) — 「Transformer の外」: Mamba / Jamba / RWKV / Diffusion を llive 内側で呼ぶ
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
<small><strong>EN:</strong> “Beyond Transformer”: Mamba / Jamba / RWKV / Diffusion + thought factors → SSM Δ Bridge<br>
<strong>中:</strong> "Transformer 之外": Mamba / Jamba / RWKV / Diffusion + 思考因子 → SSM Δ Bridge</small>
<!-- section-separators-placed -->

# llive 完全解説 (6) — 「Transformer の外」: Mamba / Jamba / RWKV / Diffusion を llive 内側で呼ぶ

![hero — SSM state stream vs Transformer attention](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_06_hero.svg)

<!-- progress-svg-placed -->
![連載進捗 (6/8) — 現在: backend](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_06_progress.svg)

> **コンセプト hook**: LLM = Transformer, は **2024 までの話**. 2025-2026 で
> State Space Model (Mamba / Jamba) と RWKV (時系列 RNN を再発明) が **長
> context で transformer に追いつき**, Diffusion text model が **token 順序
> 制約を外す** 新族として登場した. llive はそれら **全部を `LLMBackend` として
> 内側で呼べる** 設計で出発した. 思考因子 (#24-02) と SSM (state space) を
> Bridge して「**SSM 流れに 10 因子を埋め込む**」が次の到達点.
> 
> **重要な honest disclosure**: 本記事の数値は **mock baseline のみ着地**.
> 実 Mamba / Jamba / RWKV backend は **credential / weights 未着地**.

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
#24-06 LLM backend non-transformer (← 本記事)
#24-07 observability + governance
#24-08 lleval
```

#24-02 が「**思考を 10 軸 vector に展開**」だったとすると, #24-06 はその
**vector を流す管** = LLM backend. Transformer 以外の管も繋げる.
<small><strong>EN:</strong> The 'pipe through which vectors flow' = the LLM backend. We can also wire non-Transformer pipes.<br>
<strong>中:</strong> "流过 vector 的管道" = LLM backend. 非 Transformer 的管道也能接入.</small>

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

<!-- theme-svg-placed -->
![theme — non-transformer 4 backend swap + Δ Bridge (animated)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_06_theme.svg)

## 1. Transformer 以外の系統樹 (2025-2026)
<small><strong>EN:</strong> 1. Non-Transformer family tree (2025-2026) / <strong>中:</strong> 1. 非 Transformer 系谱图 (2025-2026)</small>

| family | 代表 model | 強み | 弱み |
|---|---|---|---|
| Transformer | GPT-4o / Claude / Llama 3 | 汎用 | 長 context メモリ O(N²) |
| **State Space Model (SSM)** | Mamba / Mamba-2 (2024) | 長 context O(N), selective scan | 1-step training 困難 |
| **Hybrid (SSM × Attention)** | Jamba (AI21 2024) | SSM の長さ + Attention の精度 | implementation 複雑 |
| **Linear RNN** | RWKV-6 (2024) | 推論 O(N) state | 学習効率課題 |
| **Diffusion text** | SEDD / Diffusion-LM | non-autoregressive | latency 大 |

llive の `LLMBackend` Protocol は **どれも受け取れる** ように設計されている.
<small><strong>EN:</strong> llive's LLMBackend Protocol is designed so any of them plug in.<br>
<strong>中:</strong> llive 的 LLMBackend Protocol 设计成任意 backend 都能插入.</small>
具体的には:

- `complete(prompt: str, ...) -> str` のシグネチャを満たせば backend 化可能.
- 内部実装は **transformer / SSM / RWKV / diffusion** どれでも OK.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 2. なぜ Mamba / SSM が llive 内側で価値あるか
<small><strong>EN:</strong> 2. Why Mamba / SSM are valuable inside llive / <strong>中:</strong> 2. 为什么 Mamba / SSM 在 llive 内部有价值</small>

llive の 4 層メモリ (#24-01) は **長 context** を前提に動く. Transformer
<small><strong>EN:</strong> llive's 4-layer memory (#24-01) assumes long context. Mamba / SSM make that cheap.<br>
<strong>中:</strong> llive 的 4 层记忆 (#24-01) 以长 context 为前提. Mamba / SSM 让这变得便宜.</small>
だと 32k-128k で頭打ち / 値段が高騰する. SSM は **O(N) で 1M token まで**
動く理論. これが噛むと:

- episodic memory の全件流し込みが現実的に
- consolidation cycle (海馬→皮質) の一括バッチ処理が現実的に
- TRIZ self-reflection に過去 ChangeOp 全件を context で渡せる

そのため Mamba / Jamba は llive の **長 context backend** として最有力候補.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 3. RWKV — 時系列 RNN を再発明したもの
<small><strong>EN:</strong> 3. RWKV - a reinvention of time-series RNN / <strong>中:</strong> 3. RWKV - 时序 RNN 的再发明</small>

Bo Peng (RWKV-6, 2024) が示したのは「**Attention は時系列の特殊形**」.
<small><strong>EN:</strong> Bo Peng (RWKV-6, 2024) showed that 'attention is a special case of time-series'.<br>
<strong>中:</strong> Bo Peng (RWKV-6, 2024) 证明了 "attention 是时序的特例".</small>
RWKV は state を持つ RNN だが Attention 並みの精度を達成. 推論時は **state
を保持して 1 token ずつ** 進めるので **推論 O(N) state, O(1) per token**.

llive にとって RWKV は:

- on-prem 動作前提 (weights が小さい)
- state 保持 = 4 層 memory との親和性
- 商用 license 自由度 (Apache-2.0)

の 3 点で魅力. が, weights が手元になく **実機検証は次セッション以降**.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 4. Diffusion text — token 順序の制約を外す
<small><strong>EN:</strong> 4. Diffusion text - breaking the token-order constraint / <strong>中:</strong> 4. Diffusion text - 解除 token 顺序约束</small>

Diffusion-LM / SEDD (Lou et al. 2024) は text を **noise → denoise** で生成
<small><strong>EN:</strong> Diffusion-LM / SEDD (Lou et al. 2024) generates text via noise → denoise — non-autoregressive.<br>
<strong>中:</strong> Diffusion-LM / SEDD (Lou 等 2024) 通过 噪声 → 去噪 生成文本 — 非自回归.</small>
する non-autoregressive 系. これは「**token 順序が逆方向にも書ける**」という
透明性を持つ. llive の **「自己進化」** で過去 ChangeOp を **後ろから再生成
してその先を予測** するような用途で活きる可能性. ただし latency は大きい.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 5. SSM × 10 思考因子 Bridge (構想中, 未実装)
<small><strong>EN:</strong> 5. SSM x 10 thought factors Bridge (planned, unimplemented) / <strong>中:</strong> 5. SSM x 10 思考因子 Bridge (构思中, 未实现)</small>

これが本記事の **「期待値」** セクション. 構想:
<small><strong>EN:</strong> This is the 'expectations' section of the article. The plan:<br>
<strong>中:</strong> 这是本文的 "期望值" 部分. 计划如下:</small>

- SSM の hidden state `h_t` (D dim) を 10 因子 vector と **同じ空間** に
  embed する.
- consolidation cycle で `h_t` から 10 因子の **強さ** を読み出す.
- 派生個体の persona affinity を SSM state に **書き戻す** こともできる.
- 結果: 「**SSM が走るたびに 10 因子の傾きが書き換わる派生集団**」.

これは構想で **未実装**. weights + credential 確保後に PoC. 早ければ
v0.7 〜 v0.8.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 6. 本日 (2026-05-21) 着地状況
<small><strong>EN:</strong> 6. Landing status (2026-05-21) / <strong>中:</strong> 6. 本日 (2026-05-21) 落地情况</small>

| 項目 | 状態 |
|---|---|
| LLMBackend Protocol | 着地済 (v0.B から) |
| OpenAIBackend | 実機動作済 |
| AnthropicBackend | 実機動作済 |
| OllamaBackend | 実機動作済 |
| MockBackend | 着地済 (テスト用) |
| MambaBackend | **未着地** |
| JambaBackend | **未着地** |
| RWKVBackend | **未着地** |
| DiffusionBackend | **未着地** |
| SSM × 10 因子 Bridge | **構想のみ** |

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 7. honest disclosure (本記事は honest-disclosure-required タグつき)
<small><strong>EN:</strong> 7. Honest disclosure (this article carries the honest-disclosure-required tag) / <strong>中:</strong> 7. 诚实披露 (本文带 honest-disclosure-required 标签)</small>

constraints に明記されているので **繰り返し書く**:
<small><strong>EN:</strong> Per the constraint, repeat explicitly:<br>
<strong>中:</strong> 依据 constraint, 明确重复:</small>

- **#24-06 の数値類は全て mock baseline.** 実 Mamba / Jamba / RWKV backend は
  **本セッションでは着地せず**.
- weights 入手 (HuggingFace) と GPU credential 確保後に PoC.
- 「Mamba は Transformer より速い」と書きたいところだが, それは原論文の主張で
  あって llive で実測したわけではない. 引用は出典つきで.
- SSM × 思考因子 Bridge は **完全な構想**. 「面白そう」というだけで実装根拠は
  まだ無い.
- RWKV-6 の License は Apache-2.0 だが derivative の license 互換性は
  別検証要 (FullSense Apache-2.0 + Commercial dual-license と整合確認).
- Diffusion text の latency が大きい問題は llive consolidation cycle の
  「**遅くて OK な経路**」に押し込めば吸収できるが, それが本当に
  workable かは PoC 待ち.

![section](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_24_section_separator.svg)

## 8. References
<small><strong>EN:</strong> 8. References / <strong>中:</strong> 8. 参考资料</small>

- Gu, A. & Dao, T. (2024). *Mamba: Linear-Time Sequence Modeling with Selective State Spaces*. arXiv:2312.00752.
- AI21 (2024). *Jamba: A Hybrid Transformer-Mamba Language Model*.
- Peng, B. et al. (2024). *RWKV-6: Continually Improving Linear RNN*.
- Lou, A. et al. (2024). *Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution*.
- Karpathy, A. (2025). *LLM Wiki* (concept-of-document).
- 完全リストは v0.7 リリース時に references.bib に同梱予定.

---

> draft (10x volume 版は次セッション). 骨子 + 7 main section + honest
> disclosure 6 件 (constraints honest-disclosure-required 準拠).

---

## Series Navigation

- ← 前: [llive 完全解説 (5) 「集団が学ぶ AI」](https://qiita.com/furuse-kazufumi/private/07b686ea311e06027f94)
- → 次: [llive 完全解説 (7) 「審査つき AI」](https://qiita.com/furuse-kazufumi/private/c5f2077a3399d3fc9b26)
- 全体: [llive 完全解説 (0) — series index](https://qiita.com/furuse-kazufumi/items/07b4882e872994b27b3c)
- repo: [furuse-kazufumi/llive](https://github.com/furuse-kazufumi/llive)
