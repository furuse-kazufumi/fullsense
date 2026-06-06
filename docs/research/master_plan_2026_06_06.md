# 包括計画 — 特別 DNA 戦略 × 全やり残し統合 (2026-06-06)

> ユーザー Goal「包括的な計画を立てる」への回答。本日の差別化監査 + DNA 積層 5 タスクの成果と、
> 全プロジェクトのやり残しを単一の優先度順計画に統合する。
> 原則 = [[project_special_dna_strategy]]: 計画 → 小 PoC → 大 PoC → 組込み、進化の行き止まり回避、
> trait 積層 (polygenic)、計算リソース制約下のニッチ生存 (G16 避実撃虚)。
> 姉妹 doc: differentiation_audit_dna_roadmap_2026_06_06.md (監査確定) / classics_dna_mapping_2026_06_06.md (G14-G18) /
> gate_taxonomy_audit_2026_06_06.md (検問棚卸し)。

## 0. 本日の確定事実 (計画の前提)

- 差別化監査: **breaks 0 / narrows 36** — 四点交差点 (sound contraction 証明 × Transformer 記憶コア ×
  ループ内 prove-then-reject × 動く実装) は生存。ただし D1-D4 文言の限定再定義が急務。
- **時間窓リスク**: SSGM (2603.11768) が verified memory evolution の看板を理論先取り — 実装先取りの窓は有限。
- honest 急所 2 件: Z3 看板と実装の乖離 / 証明ゲートが出荷 `evolve()` 未配線。
- DNA 積層の本日進捗: ペルソナ +5 (進化派 3 + 古典 2、llive ontology 19 名) / Sakana 統合 corpus 10 docs /
  目標軌道 tube ゲート設計+PoC 済 / 検問タクソノミ / G14-G18 提案 / 兵法書 corpus (構築中)。
- llive 実 LLM 進化本走行 (persona_evo_main_realpressure_s1) は **06-02 21:13 から停止中** (--resume 可)。

## 1. トラック構成 (依存と並列性)

```
T1 llcore 本線 (Phase 0→1→2→4)   ← 最優先・直列
T2 llive 進化基盤 (再開+Sakana 取込) ← T1 と並列可
T3 発信 (論文/Qiita/Team)          ← T1-Phase0 と連動
T4 防御調査 (Phase 3)              ← いつでも・低リスク
T5 台帳・環境の大掃除              ← 随時 (セッション端数時間)
```

## 2. T1: llcore 本線 — 監査ロードマップの実行 (最優先)

| # | 項目 | 規模 | gate | 備考 (行き止まり回避) |
|---|---|---|---|---|
| 1-1 | **Phase 0: クレーム再定義** — D1'-D4' + 防御壁 15 件を PAPER_DRAFT related work に編入、Z3 看板を「sound contraction certifier ladder」へ修正 | 編集 0.5-1 セッション | なし | 全後続の前提。誇張のまま=査読一撃の行き止まり |
| 1-2 | **Phase 1a: 証明ゲート本配線** — `gated_evolve` を src `evolve()` に additive flag で正式配線 + 回帰テスト | 小 | なし | 研究実証済の配線のみ。1-3/2 系の差し込み口になる |
| 1-3 | **Phase 1b: tracking tube レポータ組込み** — 本日 PoC 済 (cert_inf 限定、r=G·w̄/(1−L)) | 小 | なし | additive read-only、certifies() 非破壊 |
| 1-4 | ✅ **完了 (06-06/07)**: Phase 2a trajectory_tube gate — P1/P2/P3 PASS + (c) n=20 事前登録決着 (d8 Δ=+0.0152, p=0.0056, dose-response) + 論文新 §9 編入 (SSGM 引用済)。正本 = llcore verified_memory_poc/VERDICT.md | — | — | 防衛的公開 (push + 記事) が次の user-gate |
| 1-5 | **Phase 2b: SPC 進化ゲート転用** — llmesh Xbar-R/CUSUM を進化メトリクス runtime ゲートに配線 | 小 | なし | 新規実装ほぼ不要、SPC×進化は我々だけの軸 |
| 1-6 | **Phase 4: 地形改造 E (検証器殻) × 1-4 合流** — ③を立たせる人工地形で「証明ゲート下の記憶進化」 | 大 | ユーザー選択 | Phase 1-2 の trait を全部踏み石に使う。地形ブレスト Workflow は resume 可 |
| 1-7 | (park 継続) 人狼 PoC / ECC instinct-loop / IP 保護・Cython 化 | — | ユーザー | social corpus は資産として保持 |

## 3. T2: llive 進化基盤 — 走行再開 + Sakana 取込

| # | 項目 | 規模 | 備考 |
|---|---|---|---|
| 2-1 | **本走行の再開判断** — persona_evo_main_realpressure_s1 (06-02 停止) を --resume するか、Sakana 取込後に再走するか | 判断のみ | 推奨: 2-2 の novelty 棄却を入れてから再走 (評価コスト削減が直接効く) |
| 2-2 | **ShinkaEvolve novelty 棄却の移植** (Sakana 所見 #1) — 評価前に embedding 類似で重複変異を捨てる 1 段を評価ループ前段に | 小 | 15h marathon の「評価がボトルネック」教訓と整合。参照実装 = SakanaAI/ShinkaEvolve |
| 2-3 | **TIES/DARE 交配演算子化** (所見 #2) — 派生集団進化の crossover に符号多数決/間引きを導入 → 将来「memory-merge」(4 層メモリ混合比 × CMA-ES) へ | 中 | memory-merge は Sakana 未踏の空白 = 新遺伝子座候補 |
| 2-4 | bandit バックエンド選択 (所見 #3) — UCB で変異依頼先バックエンドを動的選択 | 中 | 既存マルチバックエンド資産と整合。reward hacking 警戒 (DGM 反面教師) |
| 2-5 | G14-G18 の実装接続 — G15 二層倫理 (探索=詭道自由 / 採用=仁=Approval Bus) を進化ループの明示構造に | 小 | 古典 DNA を「文書」から「コード」へ |
| 2-6 | PERSONA-FX stretch-E (文化的獲得ペルソナの非自明性検証) — 既存 TOP PRIORITY | 中 | ペルソナ 19 名に増えた ontology が素材 |
| 2-7 | llive unpushed commits 整理 (0d: auto: 系 333+) — push 承認済みブランチの push 実行 | 判断+小 | user-gated (push) |

## 4. T3: 発信 — 論文 + 記事

| # | 項目 | 規模 | 備考 |
|---|---|---|---|
| 3-1 | **論文 submission 準備** — Phase 0 (1-1) 完了後に repro code / 図 / bib 整備 | 中 | §7 まで結晶化済み。監査の防御壁がそのまま related work になる |
| 3-2 | **QIITA #38: 差別化監査 + 特別 DNA 物語** — 本日のセッション (敵対監査 56 agents → breaks 0 → 古典 DNA) は記事 13 側面の「戦略」「教訓」枠に最適 | 小 | 本編 + かみくだき、4 言語、Team 併載 |
| 3-3 | Qiita 残務: 0h 限定共有 10 件の公開昇格スケジュール / 0i タイトル手動修正 / 0j LinkedIn link 差替 | 小 | 0h/0i は operator 作業含む |
| 3-4 | Qiita Team registration-safety 準備 (画像 public URL / 文字数 / frontmatter) | 小 | reference_qiita_team_fullsense |

## 5. T4: 防御調査 (Phase 3) — 低リスク・随時

| # | 項目 | 備考 |
|---|---|---|
| 4-1 | 特許 DB 照会 (USPTO/JPO/Google Patents) — 監査の既知の穴 | 調査のみ |
| 4-2 | ✅ **完了 (06-07)**: CAV/TACAS/FM 逆引き 2 巡目 — breaks 0 / narrows 17 / SSGM 後続なし。論文編入済。正本 = research/cav_tacas_reverse_lookup_round2_2026_06_07.md | 監査 critic 指摘の最優先盲点 → 解消 |
| 4-3 | ✅ **完了 (06-07)**: 内部状態安定性 4 系統 sweep — breaks 0 / must_cite 27 → 系統代表 ~14 件を論文編入。「解析は成熟・ゲートは不在」の二段防御確立。正本 = research/internal_state_stability_defense_2026_06_07.md | D4 の最脆部 → 解消 |
| 4-4 | metamorphic gate (llive 構造不変量→振る舞い不変量) | 検問タクソノミ TOP-3 の残り |

## 6. T5: 台帳・環境の大掃除 (端数時間で消化)

| # | 項目 | 備考 |
|---|---|---|
| 5-1 | **cross-corpus INDEX 一括再生成** — 兵法書 corpus 完了後すぐ (self_evolving_agents 31 docs 反映含む) | 本セッション内 |
| 5-2 | **NEXT_SESSION.md の stale 掃除** — 🔴 PyPI fullsense は 2026-05-25 完了済 → ✅ 化、0a/0b 等クローズ済みセクション整理 | 台帳 drift 解消 |
| 5-3 | 進化 RAD corpus 重複統合判断 (evolution_corpus_v2 698 vs evolutionary_computation_corpus_v2 161) | 両方に我々 findings — 統合 or 役割分離を決める |
| 5-4 | Codex file-read review 再試行 (前回 systemic timeout) | 二本柱の復旧確認 |
| 5-5 | fullsense deep-dive + GPU doc の push 判断 (local commit のみ、local-path レビュー後) | user-gated |
| 5-6 | lleval honest disclosure 5+1 軸の実装 (現状 design 記載のみ) | 検問 4-4 と併走可 |
| 5-7 | GPU portfolio 判断 (rent-first 推奨 doc 済、BG10 pre-reg 未作成) | user 判断待ち。Phase 2/4 が GPU を要する時に再浮上 |
| 5-8 | 0c (llove offline-check Phase 2) / 0f (browser-use path 2 件) / 0g (C: 配下処遇) | 旧キュー、優先度低のまま保持 |

## 7. 推奨実行順 (次の 3 セッション)

1. **次セッション = T1 Phase 0 (1-1)** + T5 5-1/5-2 (端数)。コスト最小・全後続の前提・dead-end 除去。
2. **その次 = T1 Phase 1 (1-2, 1-3)** + T2 2-2 (novelty 棄却) → llive 本走行再開 (2-1)。
3. **3 セッション目 = T1 Phase 2a (1-4 verified memory PoC ★時間窓)** + T3 3-2 (QIITA #38)。

> 並列運用: T4/T5 は各セッションの背景 Agent 枠で随時消化。T3 3-1 (論文) は Phase 0 完了が前提。
> user-gate が必要なもの: 1-6 着手判断 / 2-7 push / 5-5 push / 5-7 GPU / 1-7 park 解除。
> **特許出願は見送り (2026-06-06 ユーザー判断)**: 出願コスト (JP+US で 100 万円級+公開代償+行使コスト) は
> リソース制約と非整合。代替 = **防衛的公開** (論文/QIITA/git commit = date of record 方式、先駆者論文
> 2026-05-27 で確立済) — Phase 2a PoC → 即日付付き公開、が SSGM への最速・最安の先取り。

## T6: 記事作法の全面見直し (2026-06-06 追加 — ユーザー連続指摘)

発信物の品質規律を体系化し全記事に適用するトラック。正本 = `article_craft_audit_2026_06_06.md` (監査) + `ethics_audit_published_2026_06_06.md` (倫理) + memory 7 規律 (ethics_before_product / anthropomorphize_concrete / borrowed_craft_needs_kb / article_as_gift / cliffhanger / humility_tone / project_rakugo_as_llm_knowledge)。

| # | 内容 | 状態 |
|---|---|---|
| 6-1 | 倫理遡及監査 (暴力語) → A 群穏当化 (#25/#27) | ✅ 済 |
| 6-2 | #38 全面改修 (暴力語/来歴脚色/図/リンク/漫画看板除去/llcore 具体物) | ✅ 済 (Team 反映) |
| 6-3 | 落語 corpus 構築 (話芸→LLM 写像 KB) | ✅ 済 |
| 6-4 | 文章作法監査 (引き/謙虚さ/落語/つなぎ, 43 記事) | ✅ 済 — 引き弱 10/自慢 2/落語 0 |
| 6-5 | 段階改善: 第1波 (#16/#03/#35_02) → 第2波 (#01-03) → 第3波 (残り) | 🔄 #16 着手 |
| 6-6 | 改善記事の 4 言語同期 → push → Qiita 公開+Team 再投稿 | 各波で |
| 6-7 | **連載用語ハブ** (全用語を概念図+定義表に、各記事からリンク) — ユーザー提案。読者が用語で迷わない親切。4 言語・静的 SVG | 次回候補 |
| 6-8 | **アニメ SVG 拡充** — ユーザー提案。二段運用 (GitHub/Pages=SMIL 動く + Qiita=静的フォールバック, imgix 制約)。tracking tube/prove-then-reject/進化ループ/四点交差点 を動かす | 次回候補 (6-7 連動) |

**統合発見**: 今日の全指摘は「記事=読者へのプレゼント、良い贈り物の作法」に収束。倫理ゲート/具体物擬人化/KB 保持/引き/謙虚さ が全部その細目。

## 8. 進行中 (本計画確定時点)

- 兵法書 corpus 構築 Agent (武経七書+西洋+OODA) — 完了後 5-1 を実行して本日分クローズ。
