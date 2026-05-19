---
layout: default
title: "Cognitive Mesh vs SOTA LLM Agent Memory"
parent: "Research"
nav_order: 3
---

# llive Cognitive Mesh v0.8 vs SOTA LLM Agent Memory (2026-05-20)

> AI agent (Claude Opus 4.7) が WebSearch + 既知の論文知識から
> 800 字以内で生成した比較メモ. llive v0.8 Cognitive Mesh の差別化軸を
> 論文/OSS 群と対応づけ、未解決な研究問いを残す.

## Mesh sub-system ↔ Prior art 対応表

| Mesh | 役割 | 対応する既存研究 | 差分 |
|---|---|---|---|
| M8.1 Mesh Bridge | timeline 双方向同期 + HTTP push | LangGraph state channels, AutoGen GroupChat | UI (llove TUI) を first-class peer に昇格, 純 LLM ↔ LLM ではない |
| M8.2 Quiet Hours | 就寝帯抑止 | 先行研究ほぼ無し / Constitutional AI 抑止の時間軸版 | 時刻ベース proactive 抑止は新規 |
| M8.3 Proactive Speech (4 trigger) | LLM 自発発話 | Generative Agents reflection trigger, Voyager curiosity | timer + integrity-violation trigger を加えた 4-axis 統合 |
| M8.4 Idle Training | アイドル時 reasoning → 学習データ | STaR / self-distillation, Reflexion | 「アイドル検出」をシステムが自律判断 |
| M8.5 TonicRisk Monitor | 持続的リスクスコア | Constitutional AI, ShieldGemma | 短期 phasic + 長期 tonic の二軸監視は非定型 |
| M8.6 TitleRecall | 過去会話タイトル連想 | MemGPT recall memory, MemoryBank | タイトル限定の軽量連想 (full embedding 不要) |
| M8.7 Mesh5W1H | 5W1H メタデータ | Generative Agents memory stream schema | journalistic schema を明示固定化 |
| M8.8 Graph + Quarantined Memory | BFS/DFS/centrality + Ed25519 署名分離 | A-MEM graph memory, HiAgent | 署名による信頼境界はメモリ研究側にほぼ存在しない |
| M8.9 Multilingual Grammar Sink | 多言語規則違反 + EVO saga | Constitutional AI / linguistic guardrails | 文法レベルの drift を memory event 化は新規 |

## Differentiation summary

1. **On-prem first** — MemGPT / Generative Agents は cloud LLM 前提.
   Mesh は llmesh 経由で local LLM 動作 (EAR / 輸出規制対応).
2. **Trust boundary in memory** — Ed25519 署名による Quarantined Memory は
   SOTA memory 研究には希薄, agent supply-chain 研究側に近い.
3. **Tonic + phasic dual-timescale risk** — 既存 guardrail は phasic 単発検査が中心.
4. **Time-aware autonomy (Quiet Hours)** — proactive 抑止の時間条件化は前例少.
5. **UI を memory peer 化** — TUI を観測 sink でなく対等な mesh node にする設計.

## Open research questions

- Quarantined Memory の署名コストは大規模 graph で sub-linear に収まるか
- Tonic risk score の長期窓は LLM hallucination 検出感度とどう trade-off するか
- Idle Training の self-distillation が mode collapse を起こす境界条件
- Proactive Speech の 4 trigger に第 5 軸 (社会的 cue) が必要か
- 多言語 grammar sink の言語間 transfer は単言語 fine-tune を上回るか

## References

1. MemGPT — <https://arxiv.org/abs/2310.08560>
2. Generative Agents (Smallville) — <https://arxiv.org/abs/2304.03442>
3. MemoryBank — <https://arxiv.org/abs/2305.10250> / Voyager — <https://arxiv.org/abs/2305.16291>
4. LangGraph — <https://langchain-ai.github.io/langgraph/>
5. AutoGen — <https://arxiv.org/abs/2308.08155> / CrewAI — <https://docs.crewai.com/>
6. A-MEM (agentic memory graph) — <https://arxiv.org/abs/2502.12110>
7. STaR — <https://arxiv.org/abs/2203.14465>
8. Reflexion — <https://arxiv.org/abs/2303.11366>
9. Constitutional AI — <https://arxiv.org/abs/2212.08073>
10. OWASP Top 10 for LLM Applications — <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
