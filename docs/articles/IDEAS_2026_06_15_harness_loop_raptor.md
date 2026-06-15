# 記事ネタ台帳 — ハーネス/ループエンジニアリング × RAPTOR/RAD/LLM Wiki（2026-06-15）

> 古瀬さん発の 3 シード（harness eng / loop eng / RAPTOR+RAD+LLM Wiki のすごさ）を、Web ポジショニング調査 + 手元の実材料で grounding した記事コンセプト台帳。
> ★ honest disclosure: 下の「業界用語の出自・日付・人物」は WebSearch 要約ベース。**公開前に一次情報で要確認**（[[feedback_no_solo_ai_judgment]] / 外部 finding は一次検証）。
> Alu コマは各記事に**閑話休題（箸休め）程度**で 1〜2 個（[[reference_alu_manga_crops]]、Qiita は出典付きリンク）。

---

## 🎁 大発見：3 本は「2026 年パラダイム転換」シリーズになる

WebSearch で判明（要一次確認）:

- **Harness Engineering** = 2026 の確立用語。LLM を包む**決定論的ランタイム層**。提唱は Mitchell Hashimoto（2026-02 blog）、OpenAI Ryan Lopopolo（2026-02-11、手書き 0 行で本番アプリ出荷）。「**LLM にツールを直接叩かせない。harness が schema 検証・権限・実行・結果注入を担う**」。Bölük 2026 は**ツールハーネスだけ**変えて 15 モデルで最大 **10×**。
  → 出典: [Augment Code](https://www.augmentcode.com/guides/harness-engineering-ai-coding-agents) / [Agent Harness Survey (preprints)](https://www.preprints.org/manuscript/202604.0428) / [Code as Agent Harness (arXiv 2605.18747)](https://arxiv.org/abs/2605.18747) / [The Agent Harness (Medium)](https://medium.com/@nraman.n6/the-agent-harness-why-the-infrastructure-around-your-llm-is-more-important-than-the-llm-itself-3a6e5cbb2e97)
- **Loop Engineering** = 2026 の確立用語。Prompt Engineering → Loop Engineering。「**automation はレシピ通り・判断しない／loop は中で『目標に着いたか』を判断して評価・反復・調整する**」。Perceive→Reason→Plan→Act→Observe。Claude Code `/goal`（v2.1.139, 2026-05-12）が実装例。
  → 出典: [Agentic Loops: From ReAct to Loop Engineering (Data Science Dojo)](https://datasciencedojo.com/blog/agentic-loops-explained-from-react-to-loop-engineering-2026-guide/) / [From Prompt Engineering to Loop Engineering (Filip Verloy, Medium)](https://medium.com/@filipv_74515/from-prompt-engineering-to-loop-engineering-why-the-agent-era-demands-a-new-security-paradigm-816385040e3d)

**含意（古瀬さんの強み）**: llloop は文字通り "loop engineering environment"、RAPTOR は "Python orchestrates everything / never circumvent" = harness engineering の核を**先に実装済み**。業界が名前を付けた瞬間に「実物」を出せる立場。
ただし honest: **harness engineering（業界, 2026-02）は「ハーネス型バイブコーディング」（古瀬さん造語, 2026-05-22）より先**。"先に言った" ではなく "**並行して同じ洞察に到達 + 人間中心の独自ひねり**" が正直な立て付け（区別する相手は Karpathy "vibe coding" 2025-02）。

---

## 記事 A — ハーネスエンジニアリング（哲学・業界比較）

- **タイトル案**:
  - 「ハーネスエンジニアリング、ただし主役は人間 — 業界が見落とす harness の握り手」
  - 「AI に手綱(harness)をつける技術。私の定義には“育てる人”がいる」
- **フック**: 「2026 年、AI 業界が『ハーネスエンジニアリング』と呼び始めた。LLM を決定論の檻で囲い、ツールを直接叩かせない設計思想だ。私もほぼ同時期に同じ結論に至っていた——ただし私の檻には、業界が描かない人物が中心にいる。**手綱を握り、AI を部下のように育てる人間**だ。」
- **本文骨子**:
  1. 業界定義（決定論的 outer harness / schema 検証 / Bölük 10× / 手書き 0 行）。
  2. RAPTOR が実物：`Python orchestrates everything. Never circumvent Python execution flow` / run lifecycle / fail-closed gates / schema 検証ツール呼び = harness engineering そのもの。
  3. 古瀬さんの独自ひねり = **ハーネス型バイブコーディング**：人間側 3 能力（発想力 / 経験則 / アルゴリズム理解）+ **AI 成長マネジメント（部下育成＝キヤノン三自の精神）**（[[feedback_harness_vibe_coding]]）。Karpathy "vibe coding"（AI 全任せ）と明確に区別。
  4. llive Approval Bus / Novelty Lane = 「育成と監査を architecture に持ち込む」harness の動機側。
- **13 側面**: 哲学 / 業界比較 / 戦略 / 教訓 / エコシステム
- **読者**: both（エンジニア寄り）
- **閑話休題（Alu）**: 「見た目で判断するな→中身で」V0Y8JK1Xfv4S1vVecdC0（AI を UI でなく実力で評価）or 部下育成ネタ。
- **honest 注意**: 「先に言った」と書かない。日付・人物は一次確認。

---

## 記事 B — ループエンジニアリング（技術設計・実装報告・安全）

- **タイトル案**:
  - 「自動化とループは違う — 安全装置つき『ループエンジニアリング環境』を一から作った（llloop）」
  - 「ループの中に“判断”を入れる。fail-closed で。」
- **フック**: 「自動化はレシピ通りに動く。ループは違う。中で『まだ目標に着いてないな』と**判断する**。2026 年、これは『ループエンジニアリング』という名前を得た。私はそれを**実験できる環境**を一から作った——暴走を止める安全装置を最初に。」
- **本文骨子**:
  1. loop eng 定義（automation vs loop、Perceive→…→Observe、`/goal` 例）。
  2. RAD `loop_engineering` 50 手法の地図（ReAct/Reflexion/Self-Refine/MAPE-K/OODA/PID/MPC/Lyapunov-safe-RL/circuit-breaker…）（[[project_loop_lang_corpus_and_env_2026_06_11]]）。
  3. llloop 設計：MAPE-K backbone + plan-execute-verify + Reflexion、**fail-closed 安全層が主役**（circuit breaker / 発散検知 / 危険操作ゲート / 予算上限 / 再ログインで継続しない）。LLM は提案のみ・最終ゲートは SafetyPolicy 迂回不可。
  4. **セキュリティ角度**（Filip Verloy: loop 時代は新しいセキュリティ paradigm を要求）= 古瀬さんの fail-closed 哲学と完全一致。
  5. **外部駆動の技術メモ**（Telegram 受領）: 常駐 PowerShell を Named Pipes IPC / PSSession / RPA で外部制御 → 「永続ループを外から駆動」。honest: ccr 自動継続は構造上不可と結論済（[[project_ccr_automation_limits]]）→ これは候補解（要検証）。
- **13 側面**: 技術設計 / 実装報告 / 戦略 / honest disclosure / 教訓（+ 安全）
- **読者**: engineer
- **閑話休題（Alu）**: 「振り上げた拳→疲れたら自然に下がる」PoGMZ2J43qQeqeZahh6T（引き際＝circuit breaker / 撤退）or 避実撃虚 U2rv0KRioTg0Kbfx7mAs。
- **連載の核**: この回が「2026 トレンド × 自作実装」のハイライト。

---

## 記事 C — RAPTOR + RAD コーパス + LLM Wiki のすごさ（技術設計・エコシステム）

- **タイトル案**:
  - 「自分専用の 49,000 件の研究知識を、fail-closed のセキュリティ AI に食わせる — RAPTOR × RAD × LLM Wiki」
  - 「AI に『調べておいて』と言える日常 — corpus-first という反則」
- **フック**: 「AI に『この分野、先に調べておいて』と言える。返ってくるのは Web の検索結果ではなく、**自分で育てた 21 分野・約 49,000 件の研究知識**だ。それを **fail-closed のセキュリティエージェント**が引きながら脆弱性を狩る。知識は Wiki のように育つ。これが私の“反則”の正体だ。」
- **本文骨子**:
  1. **RAPTOR**: gadievron/raptor ベースの security agent fork。決定論 Python orchestration、run lifecycle、fail-closed、commands（/agentic /scan /sourcehunt /validate /understand /sca）、governance / plugin-integrity / coverage tracking。= 記事 A の harness の実物。
  2. **RAD コーパス**: Research Aggregation Directory、21 分野 + hacker_corpus ≈ 49k docs。file-per-note deposit / K² サイジング / 鮮度×価値剪定（[[project_rad_corpus_governance]] / [[project_rad_expansion_2026_05]]）。= agent の grounding 層。
  3. **LLM Wiki**: Karpathy 2026-04 パターンを llive Phase 2-4（LLW-01〜08）+ raptor corpus にマップ（[[project_llm_wiki_pattern]]）。= 知識が Wiki 的に育つ仕組み。
  4. **corpus-first advantage**（[[project_corpus_first_advantage]]）: 「調べる」を内製化した者の優位。一次情報主義（[[feedback_no_solo_ai_judgment]]）。
  5. honest: 「すごさ」を盛らない。実数（21 分野 / ≈49k / 50 ループ手法）で語り、research-grade と production を区別。
- **13 側面**: 技術設計 / エコシステム / 戦略 / 哲学（corpus-first）/ ユーザー体験
- **読者**: both
- **閑話休題（Alu）**: 「無知の知／ガチの無知じゃないですか」JRY5aSqHgjWRo1QnfR2l or 「本を鵜呑みにするな」MDsuuBm0xXPgngwyQve0（知ったかぶり防止＝一次情報主義）。

---

## シリーズ構成（推奨）

**A（WHY=哲学：harness を握る）→ B（HOW=制御：loop を安全に回す）→ C（WHAT=実装スタック：RAPTOR/RAD/Wiki）**。
各回末に「2026 年、業界がこの言葉を発明した。私はその実物をここに置いておく」で連結。技術者向け（QIITA_SUMMARY）と一般向け（QIITA_GENERAL）を並走（[[feedback_daily_articles_policy]]）。

## 次アクション候補
1. A/B/C のどれか 1 本を full draft 化（grounding workflow で実コード/実コーパス照合 → 執筆 → 敵対レビュー）。
2. まず業界用語の出自（Hashimoto/Lopopolo/Bölük/`/goal` 日付）を一次情報で確定（要 honest）。
3. AI ネタ workflow（一般ニュース 12 領域）完了を待って統合台帳に合流。
