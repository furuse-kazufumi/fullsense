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
  - 「自分専用の 47,097 docs の研究知識を、fail-closed のセキュリティ AI に食わせる — RAPTOR × RAD × LLM Wiki」
  - 「AI に『調べておいて』と言える日常 — corpus-first という反則」
- **フック**: 「AI に『この分野、先に調べておいて』と言える。返ってくるのは Web の検索結果ではなく、**自分で育てた 65 コーパス・47,097 docs の研究知識**だ。それを **fail-closed のセキュリティエージェント**が引きながら脆弱性を狩る。知識は Wiki のように育つ。これが私の“反則”の正体だ。」
- **本文骨子**:
  1. **RAPTOR**: gadievron/raptor ベースの security agent fork。決定論 Python orchestration、run lifecycle、fail-closed、commands（/agentic /scan /sourcehunt /validate /understand /sca）、governance / plugin-integrity / coverage tracking。= 記事 A の harness の実物。
  2. **RAD コーパス**: Research Aggregation Directory、**65 コーパス / 47,097 docs**（2026-06-17 手元再集計、ローカル RAD コーパス群配下 `*.md`、`hacker_corpus_v2` を含む）。file-per-note deposit / K² サイジング / 鮮度×価値剪定（[[project_rad_corpus_governance]] / [[project_rad_expansion_2026_05]]）。= agent の grounding 層。
  3. **LLM Wiki**: Karpathy 2026-04 パターンを llive Phase 2-4（LLW-01〜08）+ raptor corpus にマップ（[[project_llm_wiki_pattern]]）。= 知識が Wiki 的に育つ仕組み。
  4. **corpus-first advantage**（[[project_corpus_first_advantage]]）: 「調べる」を内製化した者の優位。一次情報主義（[[feedback_no_solo_ai_judgment]]）。
  5. honest: 「すごさ」を盛らない。実数（65 コーパス / 47,097 docs / 50 ループ手法）で語り、research-grade と production を区別。
- **13 側面**: 技術設計 / エコシステム / 戦略 / 哲学（corpus-first）/ ユーザー体験
- **読者**: both
- **閑話休題（Alu）**: 「本を鵜呑みにするな」MDsuuBm0xXPgngwyQve0（qiita43 側コマ。知ったかぶり防止＝一次情報主義）。`JRY5aSqHgjWRo1QnfR2l` は #44 候補からは撤去済み。

---

## シリーズ構成（推奨）

**A（WHY=哲学：harness を握る）→ B（HOW=制御：loop を安全に回す）→ C（WHAT=実装スタック：RAPTOR/RAD/Wiki）**。
各回末に「2026 年、業界がこの言葉を発明した。私はその実物をここに置いておく」で連結。技術者向け（QIITA_SUMMARY）と一般向け（QIITA_GENERAL）を並走（[[feedback_daily_articles_policy]]）。

## 実施状況（2026-06-15 起点 / 2026-06-18 追記反映）
- **★A+B+C を 1 本に統合した #43 を執筆し、日本語版は public publish 済**（grounding→一次情報検証→執筆→敵対レビュー→仕上げ workflow）。
  - 成果物: `tools/qiita-cli-poc/public/qiita43_harness_loop_stack.md`（本文 34,471 字 / 公開版は public publish 済み / 手元 source の front matter も `private: false` で公開状態と一致 / Alu 閑話休題 3 / 既存 Qiita 関連リンクあり / ローカルパス 0・画像 0）。
  - 一次情報検証の結果ヘッジ: Bölük「10×」=引用論文に該当記述なし→**冒頭で「捨てた数字」として教訓化** / OpenAI harness 記事=HTTP403→二次情報ヘッジ / Hashimoto は実引用（命名独占を主張しない）/ RAPTOR 2層=upstream README 実引用。
  - publish: ✅ 実施済み（2026-06-16 / commit `5f10609`）。当時は公開Qiitaトークン無のため、ユーザーが `npx qiita publish qiita43_harness_loop_stack` を実行して限定共有確認→public 化した。
- **2026-06-17 追記**: `tools/qiita-cli-poc/public/qiita43_harness_loop_stack_kamikudaki.md`
  を追加。`private: true` のローカル草稿で、完全版 #43 の 10 分版として
  「手綱 / 輪 / 知識基盤」に絞って説明。冒頭には拾い読みガイドも追加。
  ただし冒頭ジャンプ導線は Qiita 実機未検証なので、現時点では publish-ready 扱いにしない。
- **2026-06-17 追記**: `qiita43_harness_loop_stack_en.md` / `_zh.md` / `_ko.md`
  は、日本語版 `qiita43_harness_loop_stack.md` を source of truth とする
  多言語草稿ラインとして整理。章立て / 主張 / honest disclosure の同期を優先し、
  現時点では drift が残るため `ignorePublish: true` に倒した。
  冒頭の sync note は記事本文から外してある。
- **2026-06-17 追記**: `qiita43_harness_loop_stack_kamikudaki.md` /
  `qiita44_evolutionary_programs_block_diagram.md` /
  `qiita45_human_ai_dev_incident_patterns.md` も、`private: true` 草稿として
  `ignorePublish: true` に統一。`qiita44` のバス江コマは
  `JRY5aSqHgjWRo1QnfR2l` と `H4Pix38XWLRS077emoZC` の **2 コマとも本文から外した（残 0）**。
- **2026-06-17 追記**: RAD コーパス件数は handoff 用にローカル再集計し、
  `65 コーパス / 47,097 docs` へ更新。旧 `21分野 / 約49,000` は概数メモとして扱わない。
  この値は 2026-06-17 の再集計値を handoff 上の正として引き継ぐ。
  公開面の概数は「約47,000」または「約4.7万」とし、内訳や厳密値を出すときは
  `47,097 docs`（2026-06-17 再集計、ローカル RAD 配下 `*.md`、`hacker_corpus_v2` を含む）に揃える。
- **2026-06-17 追記**: Qiita の伸び筋については外部記事も参考にしつつ、
  最終的には自分の経験則として、`qiita44` は benefit 先出し +
  初心者導線 + 「壊れどころ」訴求へ、`qiita45` は
  `handoff / human gate / diff / checkpoint` を軸にした AI 失敗談 +
  すぐ試せるチェックリスト寄りへタイトル / タグ / 導入を寄せた。
- **2026-06-17 追記**: その続きとして、`qiita44` には「最初の 1 本を実装するなら」、
  `qiita45` には「今ならこう直す」を追加し、読むだけで終わらず次の一歩へ
  着地しやすい草稿へ寄せた。
  さらに `qiita44` / `qiita45` 冒頭へ拾い読みガイドを追加。
  こちらも冒頭ジャンプ導線は Qiita 実機未検証で、publish 前にアンカー方式の切り分けが必要。
- **2026-06-18 追記**: `qiita45` の休憩ポイントは 1 箇所集中から複数配置へ寄せ直し、
  #44/#45 とも attention trough ごとに呼吸を入れる構成へ再調整した。
- **2026-06-18 追記**: #43 かみくだき / `qiita44` / `qiita45` の冒頭導線は、
  アンカーが落ちても節番号 + 実見出し名だけで本文内を追える表記へ寄せた。
  ただし Qiita 実機でのアンカー可否は引き続き未検証。
- **2026-06-18 追記**: `qiita44` / `qiita45` に出てくる `llcore` / `lldarwin`
  の名称は、本文が参照する既公開 Qiita 記事名と一致しているため、役割名への抽象化はしない。
- **2026-06-18 追記**: `qiita45` の RAD 節は、外部研究との対応づけを
  「コーパス要約上の傾向」まで弱め、一次確認前提の honest disclosure に揃えた。
- **2026-06-18 追記**: `qiita45` 終盤の総括でも同じ温度感へ寄せ、
  「かなり広い母集団」といった強めの言い回しは避けて
  コーパス要約ベースの表現に揃えた。
- **2026-06-18 追記**: `qiita44` / `qiita45` の終盤は、まとめ・appendix の
  一文目で要点が立つよう front-load して、拾い読みでも結論が先に見える形へ寄せた。
- **2026-06-18 追記**: `qiita44` / `qiita45` の draft-only 注記と
  #43 多言語の sync note は記事本文から外し、`qiita45` 本文内の内部 handoff
  ファイル名は公開向けに抽象化した。
- **2026-06-18 追記**: `qiita45` の honest disclosure / appendix に残っていた
  self-TODO は外し、読者向けの外部系統メモ / 背景メモとして読める形へ寄せた。
- **2026-06-18 追記**: `qiita44` は staged 版も worktree と同期し、
  本文からバス江コマ 0 の状態をそのまま commit できる形へ揃えた。
  `qiita45` の外部研究との対応づけも「近い型として読めた」水準へ弱め、
  検証状態と主張強度を合わせた。
- **2026-06-18 追記**: #43 かみくだき / `qiita44` / `qiita45` の冒頭導線は、
  custom アンカーを本文から外し、見出し階層だけで読める text TOC を優先した。
- **2026-06-18 追記**: `qiita45` の挿絵は意図的に 0 コマへ戻した。
- **2026-06-18 追記**: `docs/articles/FULLSENSE_KB_INDEX.md` の導入文は
  `fullsense.qiita.com` と `qiita.com` の両方を含む表現へ修正した。
- **2026-06-18 追記**: `qiita44` は ☕ 休憩ポイントを 4 箇所へ増やし、
  `qiita44` / `qiita45` には末尾 HTML annotation メタタグと参考文献節を追加した。
- AI 一般ニュースネタ集（139 候補）: `docs/articles/IDEAS_2026_06_15_ai_news_harvest.md`。

## 次アクション候補
1. 日本語版 #43 は public publish 済み。残タスクは dev.to 英語版の更新 / publish だが、外部書き込みなので human gate。
2. #43 の多言語版を触るときは、日本語版を正本として chapter order / claims / honest disclosure を先に合わせ、その後 dev.to 英語版へ流す。
3. #43 のかみくだき版を推敲し、必要なら en/zh/ko への横展開を検討（#37 と同パターン）。
4. AI ニュースネタ集から次の単発記事（Mythos / DeepSeek V4 / ローカルAI三段ロケット等）。
