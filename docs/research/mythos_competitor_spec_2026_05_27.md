# 競合スペック台帳 — Claude Mythos (2026-05-27)

> 目的: ゴール「進化型アルゴリズム(llive/lldarwin オーケストラ)で **Claude Mythos を超えた性能**をセキュリティ領域で達成する」の **競合ベンチマーク基準**を確定し、情報を残す。
> 制約(ユーザー 2026-05-27): **計算リソース限定・速度不問**。→ test-time compute を青天井に投下できる。
> 矛盾(ユーザー指摘): Mythos は **vetted-only (Project Glasswing)** で**直接実行・直接対決ができない**。
> → **解決**: Mythos の**公開された検証可能なベンチ数値を「競合スペック」として固定**し、**同一/同種の機械採点ベンチ上で我々の on-prem 進化オーケストラを実測**して比較する。直接対決でなく**予測ターゲットに対する実測到達**で「超えた」を honest に主張する。

## 1. Claude Mythos とは (2026 現行情報)

- Anthropic のフロンティアモデル。コードネーム **Capybara**。Opus ティアの上位。
- 公開タイムライン: 2026-03-26 に CMS 誤設定でプレリリース草稿が一時露出 → **2026-04-08 に Mythos Preview 正式公開**。
- 位置づけ: 「サイバーセキュリティ・自律コーディング・長時間エージェント向けの新クラスの知能」。仮説生成→検証→コンテナ起動→コード実行まで**自律実行**(提案でなく行動)。
- サイバー能力が強力なため、リリースを審査済みパートナープログラム **Project Glasswing** に限定 = **一般には直接叩けない**。

## 2. 競合スペック (公開ベンチ数値 = 我々のターゲットバー)

| ベンチ | Mythos 公開スコア | 採点 | 我々の関心 |
|---|---|---|---|
| **Cybench (CTF)** | **pass@1 = 100%** (全課題 solve) | flag 一致(機械) | 旗艦・セキュリティ本丸。100% は「超え」不可 → **弱モデル群でフロンティア級到達**自体が成果 |
| **ExploitBench** | **9.90 / 16** (nudge あり) / 9.55 (完全自律) ≈ **62%**、41 脆弱性中 21 で最高ティア | exploit 成立(機械寄り) | **headroom 大** → 数値超過を狙える本命 |
| SWE-Bench Verified | 93.9% | テスト実行 | アリーナ外(参考) |
| SWE-Bench Pro | 77.8% | テスト実行 | アリーナ外(参考) |
| Terminal-Bench 2.0 | 82% | 機械 | アリーナ外(参考) |
| agentic tool use | #1 / 117 (avg 100) | 機械 | 参考 |

> ⚠️ HONEST: 上記は二次情報(ベンダー/解説ブログ/leaderboard)由来。**一次情報(Anthropic system card / 公式 leaderboard)で各数値を裏取りしてから確定**する([[reference_codex_two_pillar]] の「finding は一次情報で検証」規律)。出所は §4。

## 3. 我々の対戦設計 (アリーナ = セキュリティ)

```
[生成: カバレッジ]            [検証: precision]              [試行: 無制限]
llive 進化オーケストラ   →    RAPTOR セキュリティオラクル  →   test-time compute 青天井
(lldarwin v2:               (exploit 成立 / crash 再現 /     (speed 不問 = pass@k を
 ε-lexicase+novelty           flag 一致 / ASan・UBSan)         大量試行で押し上げる)
 +中立貯蔵庫, persona)
```

- **理論的根拠**: test-time scaling / 反復サンプリング文献 — 弱モデルでも大量サンプリングで正解候補の **coverage(pass@k)** を上げれば強モデルに迫る。ただし **"正解を選び取る信頼できる verifier" がある検証可能タスクに限る**(coverage→precision のギャップを verifier が埋める)。→ セキュリティ(flag/exploit が ground-truth)は最適アリーナ。
- **競合ターゲット**:
  - 第一目標(超過狙い): **ExploitBench 系で Mythos の ≈62% を上回る**。
  - 第二目標(到達狙い): **Cybench で単一 on-prem 弱モデル baseline を大きく超え、フロンティア級(100% 近傍)に test-time compute で接近**。
- **measurement purity**([[feedback_llive_measurement_purity]]): 基盤モデルは **on-prem(ollama) のみ**。cloud LLM と混在禁止。

## 4. 出所 (要・一次情報で裏取り)

二次情報(初期把握):
- ArmorCode — The Claude Mythos Security Playbook
- Bain & Company — Claude Mythos and the AI Cybersecurity Wake-Up Call
- Zvi Mowshowitz (Substack) — Claude Mythos: The System Card
- Pluralsight — What is Claude Mythos?
- The Decoder — New benchmark shows Claude Mythos and GPT-5.5 can develop real browser exploits autonomously
- MindStudio — From 80% to 93.9%: Claude Mythos SWE-Bench / 93.9% SWE-Bench and 59% Multimodal
- BenchLM.ai — Claude Mythos Preview Benchmarks 2026

裏取り TODO: Anthropic 公式 system card(Mythos) / Cybench 公式 leaderboard / ExploitBench 公式 → 各数値・採点定義・nudge の定義を確認。

## 5. 関連

[[project_llive_optimization_cycle]] Phase C(既存超え実証, 天井ベースライン=Mythos) / [[project_lldarwin]](生成側選択圧) / [[feedback_benchmark_honest_disclosure]] / [[feedback_llive_measurement_purity]]。
新 doc は docs/research/index.md / doc_map.md に登録すること([[feedback_fullsense_feedback_smart]])。
