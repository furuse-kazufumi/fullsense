---
title: LinkedIn post — 2026-05-22 FullSense Rust 高速化マラソン + Gemini 共創ブレスト
created_at: 2026-05-22
languages: ja, en, zh, ko
audience: LinkedIn (技術 + 経営層 + AI 研究)
links:
  github_llive: https://github.com/furuse-kazufumi/llive
  github_llove: https://github.com/furuse-kazufumi/llove
  github_llmesh: https://github.com/furuse-kazufumi/llmesh
  qiita_series_index: # 投稿後に埋める
---

# LinkedIn 投稿文 — 2026-05-22 FullSense 進捗 (4 言語版)

> 全体の要約 + Qiita 連載 + GitHub repo へのリンク. 4 言語 (ja / en / zh / ko)
> で発信. memory `feedback_linkedin_translation_jp_only` (LinkedIn は組込翻訳
> ありで日本語のみ OK) があるが, ユーザー指示 (2026-05-22) で 4 言語明示版に
> 上書き. 多言語化方針は将来 [[feedback_multilingual_release_2026_05_22]] に
> 統合予定.

---

## 🇯🇵 日本語版

**FullSense マラソン (2026-05-22) — llive Rust 高速化と「Rust 化 = 速い」の嘘**

今日 1 日で llive (自己進化型モジュラー記憶 LLM フレームワーク) の派生集団進化
hot path を Rust 化しました。 結果, 興味深い honest disclosure:

- **RUST-15** `persona_dissimilarity`: 単発で **x0.80 (Python に負ける!)** → batch
  化で **x12.71 (N=64 で x17.07)**
- **RUST-16** `collusion_score`: numpy 小 N の API 多用 hot path で **x66.70
  (N=8 で x115.04)** 圧勝
- **RUST-17b** `novelty_score_batch`: rayon 並列 + quickselect で **全 archive
  サイズ 5x clear** (avg x9.32, A=1000 で x6.41)

**「Rust 化 = 速い」も「numpy = 速い」も嘘** — 実装方法 (FFI 境界 / batch /
zero-copy / 並列度 / partial sort) で結果が桁違いに変わります。 5 パターン
判定表を `docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md`
に時系列で残しています。

加えて Gemini からの一歩先のアーキ提案を 4 つ受け取り (Predictive Verification /
KV cache Memory Translator / Antifragile Mutation / Speculative Mesh Execution),
うち KV cache Stage 1 (prefix_embeddings) を skeleton で本日着地。 multi-AI 共創
(Gemini = アーキ飛距離 / Claude+llive = 即時実装 + honest disclosure) の実例
としても面白い 1 日でした。

連載解説 9 本 (Qiita): https://qiita.com/furuse-kazufumi
コード (GitHub): https://github.com/furuse-kazufumi/llive

#FullSense #llive #Rust #pyo3 #ローカルLLM #自己進化 #honest_disclosure

---

## 🇬🇧 English

**FullSense marathon (2026-05-22) — llive Rust acceleration and the lie that "Rust = fast"**

Spent today on Rust-accelerating the hot paths of llive (a self-evolving modular
memory LLM framework). The results came with honest disclosures worth sharing:

- **RUST-15** `persona_dissimilarity`: single-pair call was **0.80x (slower than
  Python!)** due to FFI overhead → batched (N×N in one call) hit **12.71x avg
  (17.07x at N=64)**
- **RUST-16** `collusion_score`: a hot path heavy in numpy small-N API calls
  reached **66.70x avg (115.04x at N=8)** — a clean win because Python overhead
  dominates there
- **RUST-17b** `novelty_score_batch`: with rayon parallelism + quickselect,
  cleared 5x gate **at every archive size** (avg 9.32x, A=1000 still 6.41x)

**Both "Rust is fast" and "numpy is fast" are lies** — the answer depends
entirely on how you draw the FFI boundary, on batch size, zero-copy, parallelism,
and partial-sort choices. I keep the 5-pattern decision table in
`docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md` as a
time-series log.

Also received four forward-looking architectural ideas from Gemini today
(Predictive Verification / KV cache Memory Translator / Antifragile Mutation /
Speculative Mesh Execution); the KV cache Stage 1 (prefix_embeddings) skeleton
landed the same day. A nice multi-AI co-creation example: Gemini covers the
"architectural distance", Claude+llive handle "immediate implementation +
honest disclosure".

Series (Qiita, JP): https://qiita.com/furuse-kazufumi
Code (GitHub): https://github.com/furuse-kazufumi/llive

#FullSense #llive #Rust #pyo3 #LocalLLM #SelfEvolving #HonestDisclosure

---

## 🇨🇳 中文 (简体)

**FullSense 马拉松 (2026-05-22) — llive 的 Rust 加速,以及"Rust = 快"的谎言**

今天一整天专注于把 llive (一个自进化模块化记忆 LLM 框架) 的热路径迁移到 Rust。
结果有几个值得分享的"诚实披露 (honest disclosure)":

- **RUST-15** `persona_dissimilarity`:单次调用 **0.80x (比 Python 还慢!)**,因为
  FFI 开销吃掉了所有优势 → 批量化 (N×N 一次 FFI) 后达到 **平均 12.71x (N=64 时
  17.07x)**
- **RUST-16** `collusion_score`:numpy 小 N (N<100) 的 API 多用热路径达到 **平均
  66.70x (N=8 时 115.04x)**,完胜 — 因为这里 Python 开销才是瓶颈
- **RUST-17b** `novelty_score_batch`:rayon 并行 + quickselect 让 **所有 archive
  尺寸都通过 5x 关卡** (平均 9.32x, A=1000 时仍有 6.41x)

**"Rust 快"是谎言,"numpy 快"也是谎言** — 真正决定速度的是 FFI 边界画法、
批量大小、zero-copy、并行度、partial sort 等"实现方式"。 5 模式判定表保存在
`docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md`,按时序累积。

同时今天收到 Gemini 的 4 个面向未来的架构提议 (Predictive Verification / KV cache
Memory Translator / Antifragile Mutation / Speculative Mesh Execution), 其中 KV
cache Stage 1 (prefix_embeddings) skeleton 当天落地。 multi-AI 共创的好例子:
Gemini 提供"架构飞距", Claude+llive 负责"即时实现 + 诚实披露"。

技术连载 (Qiita, 日语): https://qiita.com/furuse-kazufumi
代码 (GitHub): https://github.com/furuse-kazufumi/llive

#FullSense #llive #Rust #pyo3 #本地LLM #自进化 #诚实披露

---

## 🇰🇷 한국어

**FullSense 마라톤 (2026-05-22) — llive Rust 가속화, 그리고 "Rust = 빠르다"의 거짓말**

오늘 하루 동안 llive (자기 진화형 모듈형 메모리 LLM 프레임워크) 의 hot path 를
Rust 로 가속화했습니다. 흥미로운 honest disclosure (정직한 공개) 결과:

- **RUST-15** `persona_dissimilarity`: 단발 호출은 **0.80x (Python 보다 느림!)** —
  FFI 오버헤드 때문 → 배치 (N×N 을 1 FFI) 로 **평균 12.71x (N=64 에서 17.07x)** 달성
- **RUST-16** `collusion_score`: numpy 작은 N (N<100) 의 API 다용 hot path 에서
  **평균 66.70x (N=8 에서 115.04x)** 압승 — Python 오버헤드가 지배적인 영역
- **RUST-17b** `novelty_score_batch`: rayon 병렬 + quickselect 로 **모든 archive
  크기에서 5x gate 통과** (평균 9.32x, A=1000 에서도 6.41x)

**"Rust = 빠르다"도 "numpy = 빠르다"도 거짓말** — 실제 결정 요인은 FFI 경계 설계,
배치 크기, zero-copy, 병렬도, partial sort 등 "구현 방법"입니다. 5 패턴 판정표를
`docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md` 에 시계열
로 누적하고 있습니다.

또한 오늘 Gemini 에서 한 발 앞선 아키텍처 제안 4 가지를 받았고 (Predictive
Verification / KV cache Memory Translator / Antifragile Mutation / Speculative
Mesh Execution), 그 중 KV cache Stage 1 (prefix_embeddings) skeleton 을 당일
착륙. multi-AI 공동 창작의 좋은 사례입니다 — Gemini 는 "아키텍처의 비거리",
Claude+llive 는 "즉시 구현 + 정직한 공개".

기술 연재 (Qiita, 일본어): https://qiita.com/furuse-kazufumi
코드 (GitHub): https://github.com/furuse-kazufumi/llive

#FullSense #llive #Rust #pyo3 #로컬LLM #자기진화 #정직한공개

---

## 投稿運用メモ

- LinkedIn は組込翻訳ありなので日本語版だけでも届くが, 本日 (2026-05-22) のユーザー
  指示で 4 言語版を整備. 各 platform / 各読者層に応じて切替.
- tags はスペース区切り (Qiita / Twitter / LinkedIn の hashtag 形式と互換).
- 全 4 言語版で **同じ数値・同じ honest disclosure** を提示.
- GitHub URL は public repo. Qiita URL は **投稿後に確定** するため series index
  URL を後で埋める ([[QIITA_#24_LINK_MAP]] と同じ運用).

## 関連

- Qiita 連載 #24-00 〜 #24-08 (9 本 draft 着地済, 2026-05-21〜22)
- `D:/projects/llive/docs/perf_comparison/2026-05-22_kernel_implementation_comparison.md`
  (repo 内部, 投稿時は GitHub URL に展開)
- memory: project_user_brainstorm_2026_05_22 (Gemini 4 アイデア集約)
