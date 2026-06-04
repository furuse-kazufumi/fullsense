---
title: "llcore — Transformer のコアを CPU で進化させる: Verified Neural Architecture Evolution の最小 PoC battery"
tags: ["Python", "進化計算", "Z3", "RWKV", "形式検証"]
private: true
updated_at: "2026-05-29"
id: 88ed294aa107330c6894
---

# (連載 #32) llcore CPU PoC battery 完成

## TL;DR

- Transformer の **コア計算 (state update / 学習則 / 認知駆動 Δ)** を進化対象にする研究フレームワーク `llcore` (PyPI: `llmesh-llcore` 0.1.0a0, llive 独立路線) の **CPU PoC battery 完成**
- **5 PoC / 39 falsifiable gates / 76 tests / Codex pair-review 5/5 Green-light** で機構実証
- **Z3 で構造変異を online gate** = 進化探索の selection pressure に SMT を組込んだ先行未発見 (事前調査 RAD 14 分野 + Agent A-D 確認)
- 投稿先候補: TMLR (本命) / GECCO 2027 short / NeurIPS 2026 workshop (verification × ML)

## なぜ作ったか

LLM 重みは凍結が標準だが、**コア計算アルゴリズム自体は人手設計に固定**されている。AutoML-Zero / NAS / AlphaEvolve / Sakana Evolutionary Model Merge など architecture/algorithm 探索は進んだが:

1. **個人 compute では計算リソース不可能** (TinyLlama 1.1B from scratch = $140k / 90 日 / 16×A100)
2. **探索中の安全性保証なし** = 数値不安定な architecture を生み出して時間浪費
3. **検証付き探索は静的 verification (Reluplex/Marabou/α,β-CROWN) と分断** — 進化ループ内 SMT online gate の研究は未発見

## 確定独自軸 (事前調査で negation work なし)

mechanism 実証済 (4 軸):
1. **ChangeOp → Z3 online gate** (Stage 1a, 5.8ms)
2. **state update 規則を遺伝子化 RWKV-style** (Stage 0a v2)
3. **factor_hook (認知状態 → SSM Δ)** (Stage 2a mock)
4. **自前進化器 + verifier 基盤** (Stage 0c + 1a)

post phase: persona-indexed specialist / Marabou refinement / VNN-COMP 新カテゴリ提案。

## PoC レダー (5 stage / 39 gates 全 PASS)

| PoC | 内容 | キー数値 |
|---|---|---|
| 0a v2 | RWKV-style state update gene | G6 var=7.4e-3, G9 escape@step1 |
| 0b v2 | synthetic fitness (copy/add) | G4 rank_corr=-0.20, G7 best 0.518/0.525/0.703 |
| 0c v2 | 自前 minimal GA | G3 monotonic 0.249→0.552, G7 dist=2.15 |
| 1a v2 | Z3 state_norm invariant | G2 unsat **5.8ms**, G3 sound CE |
| 2a | factor_hook × state update mock | G7 evolution smoke monotonic |

## v1 の失敗から学んだこと (honest disclosure)

PoC 0a v1 は `decay*s + mix*x*tanh(gate_str*s)` で **state=0 が fixed point の zero attractor** = G1-G5 形式 PASS だが情報伝達ゼロ。Claude 単独で見落とした設計問題を **Codex (gpt-5.4) と gem-critic の独立 verdict** が検出し RWKV-style に v2 redesign。

→ **5 PoC 中 4 件で Claude 単独では見落とした設計問題を Codex pair-review が検出**。構造破綻防止に相互レビューが機能した実例。

## 次の選択肢

a. Stage 3 kernel 多様化 (rwkv/mamba/hopfield/linear-attn を遺伝子化)  
b. Stage 4 学習則 (FF/EP/PCN/Hebb) を gene 化  
c. Stage 5 Marabou Incremental NN Verification bridge  
d. PrediPrune+Quokka で Z3 gate 高速化  
e. FlashEvolve で 3.5-5x wall-clock 高速化  
f. 論文化 (TMLR + GECCO 2027)

## Honest 留保

- mock 中心、実 LLM/重み接続は GPU/新 PC 待ち
- 1 step scalar invariant の over-approx proof 段階、多次元・多 step は post phase
- tanh 上界近似は保守的 (sound だが完全でない)

---

**Tags**: 進化計算 / 形式検証 / Z3 / RWKV / state space model / CPU研究  
**関連**: 連載 #14-31 (llive lldarwin v0.B-E + 観測+governance + lleval)  
**Project**: D:/projects/llcore (PyPI llmesh-llcore 0.1.0a0)
