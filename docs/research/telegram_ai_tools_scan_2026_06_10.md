# Telegram 共有 AI ツール 4 件 網羅調査 (2026-06-10)

> 出典: ユーザーが 2026-06-09 に Telegram 共有した 4 メッセージ (claude-loop queue, id 42e478/4b088b/6bc4f8/d2fe6e)。
> 調査手法 = raptor Workflow `telegram-ai-tools-scan` (8 agent / 一次情報 WebFetch 検証 / 約7.4分)。
> 制約: `no-push` / `needs-human-judgment` → 調査(安全)は自律実行・導入/外部送信(危険)はユーザー判断保留。
> 全 raw 結果 = `<session tmp>/tasks/wr3uv0dof.output` (本 doc は要約と判断材料)。

## TL;DR

- **ui-skills.com** (ibelick/Julien Thibeaut, MIT, 2.4k★, Web frontend 焦点) = AI に綺麗な UI を作らせる skill 集。FullSense コアとは別レイヤ=**競合せず「取り込む MIT 素材」**。効くのは portal/記事メタ/llove VS Code 拡張(Web view)の周辺面のみ。Textual TUI 本体には効かない。
- **notebooklm-mcp-cli** (jacob-bd, MIT, 4.8k★) = NotebookLM 非公式ブリッジ。internal API + ブラウザ cookie 抽出 + クラウド送信で、FullSense の on-prem/責任所在哲学とは逆方向 → **反面教師の記事素材** として high 価値。llive 記憶層への接続は設計違反。
- **GitHub 急上昇コア競合 5 件** = ★最重要。FullSense の個別機能の新規性は深刻に先行されている(下表)。
- **マルチモーダル/デモ 5 件** = VoxCPM2(古瀬あい音声) と PaddleOCR(llive VLM 前処理) が on-prem 整合で high。Open-LLM-VTuber はマスコット差別化の脅威。

## ★コア競合 (honest disclosure — 個別機能は先行されている)

| repo | ★ | License | FullSense の何を脅かすか |
|---|---|---|---|
| hermes-agent (NousResearch) | 189k | MIT | **llive のコア**「自己進化記憶+スキル自作+セッション跨ぎ記憶」をほぼ完全先行。command approval+container isolation=Approval Bus/HITL 相当。Telegram/Slack/Discord push も標準。2026-02 公開 |
| ECC / Everything Claude Code (affaan-m) | 211.8k | MIT | **raptor** のスキル+コーパス+セキュリティ+継続学習 1パックを 64 agent/261 skill+マルチハーネス(Claude Code/Codex/Cursor/Gemini/Copilot/Zed)で先行。AgentShield 脆弱性スキャン同梱 |
| codegraph (colbymchenry) | 45.9k | MIT | rtk/トークン削減を専業先行(公称 47%減/tool-call 58%減, 100%ローカル, ナレッジグラフ型) |
| headroom (chopratejas) | 20.4k | Apache-2.0 | rtk/トークン削減を専業先行(公称 60-95%減, 6 圧縮技法, ローカル, CacheAligner/可逆圧縮) |
| last30days-skill (mvanhorn) | 37.1k | MIT | raptor RAD 横断調査+根拠付き要約と重複(対象は SNS/トレンド寄り) |

### FullSense が誇張なしで優位な 4 点 (5 件全てに皆無を一次確認)

- **(a) 産業ドメイン接続** — MQTT/OPC-UA 産業 IoT 直結 + SPC 統計的工程管理 + llcore verifier を AI スタックに統合した例は競合に無い
- **(b) 責任所在を architecture level に貫く一貫思想** — Approval Bus + SPC + HITL を全製品で(hermes の command approval は機能的に近いが思想として未体系化)
- **(c) verified-plasticity** — 学習/進化が本当に効いたかを **sound certificate で判別するメタ層**(llcore)。competitor の自己改善主張(hermes「20+スキルで40%高速」/ECC Continuous Learning/headroom learn)は **全て第三者未検証ベンチ**であり、verified-plasticity framework はまさにこの種の false-positive を排除する道具
- **(d) 二重設計** — 3 製品独立 OSS + 統合で 1 世界観(ECC の「1パック」とは逆方向)

### 補正 (実コード検証済 — 鵜呑み禁止)

- rtk(ls/git/grep/test 出力を圧縮する CLI proxy)は headroom/codegraph と真正面で競合するが、**llrepr(markdown/svg/tui writer + diff + schema over MCP の typed representation 層)は別カテゴリ**。脅威を llrepr に巻き込むのは誤り。
- 競合の自社ベンチ(hermes 40%高速 / codegraph 47% / headroom 60-95%)は全て第三者未検証。**star 数は人気の証で性能優位の証ではない**(feedback_benchmark_honest_disclosure)。FullSense 側も自前ベンチで対照すべき。
- ui-skills 周辺の主張(UI/UX Pro Max 88.7k★ / Vercel skill 98k+ installs)は WebSearch 二次情報で未検証 → 市場判断の根拠に使わない。

## トピック別 適用ハイライト

### ui-skills.com
- portal(a11y/metadata: コントラスト比/focus/OGP/canonical)= **high**、記事 animated SVG(motion 最適化)= medium、llove VS Code 拡張 Web view = medium。TUI 本体・raptor 本体には不適。

### notebooklm-mcp-cli
- **記事 = high**: 「便利なクラウド MCP ブリッジ vs 責任ある on-prem AI」対比表(機密扱える/on-prem/責任所在/data residency 明示 の4軸)の格好の題材。先方は README に送信先の明示記載すら無い。
- llive = medium(逆向きの教訓: Approval Bus が外部送信を architecture level でゲートする境界事例)。**実接続は設計違反**。

### マルチモーダル/デモ
- **VoxCPM2** (Apache-2.0, on-prem, 30言語, 48kHz, Voice Design) = 古瀬あい音声合成の最有力 = **high**(Voice Cloning は声の権利問題回避で不使用方針)。
- **PaddleOCR** (Apache-2.0, PaddleOCR-VL 0.9B, 109言語, 軽量) = llive VLM 拡張のドキュメント→構造化前処理 = medium(optional extras 隔離で組込検討)。
- Open-LLM-VTuber = マスコット可視化+proactive 発話の差別化を脅かす先行例(完全オフライン/割込発話/デスクトップペット)。**VTuber化・音声化は新規性にならない前提**で、差別化は中身(自己進化・責任所在)に置く。
- Agent-Reach(MIT, APIキー不要 SNS 横断)= raptor/rad-research の閲覧バックエンドとして **consumer に回る**のが妥当。
- MoneyPrinterTurbo = 動画パイプライン構造のみ参考、外部 API 依存で Local 第一非整合。

## ★ユーザー判断が要る項目 (needs-human-judgment, 全件保留中)

1. **戦略(最重要)**: FullSense ブランド主張を「個別機能の新規性」から「**産業接続+責任設計+検証可能性(verified-plasticity)+表現レイヤ+統合世界観**」へ重心移動する方針を正式採用するか(全製品の README/記事/portal に波及)。
2. llive/llmesh/raptor の README・新規性主張の文言修正(「自己進化記憶 LLM が新規」→「進化を構造化・検証可能にした」等)を commit/push するか。
3. 競合 repo(hermes/ECC/codegraph/headroom 等)をローカル clone/install して直接ベンチ比較するか(サードパーティコード実行=供給網リスク、plugin-integrity/SWD 前提でも承認要)。
4. ui-skills の skill を FullSense リポジトリに install するか / NotebookLM へ非機密ダミー文書で挙動確認するか。
5. VoxCPM2(2B 重み DL)/PaddleOCR(PaddlePaddle 依存追加)をローカル導入するか。
6. raptor を ECC のようにマルチハーネス横展開するか、Claude Code fork 特化を維持するか。
7. 記事「正直な競合解剖」を実際に publish するか drafts 留めか。

## llcore 普及記事へのシナジー (メインゴール直結)

verified-plasticity framework は competitor の未検証「自己改善」主張(hermes 40%/ECC Continuous Learning/headroom learn)を **sound certificate で判別する道具**。Phase 2 の発見「経験 gate は発散 gene の 84% を false-admit、sound cert は 0%(=ラングトンの蟻の幻)」を、対競合の文脈で「人気の自己改善エージェントの『賢くなった』は本当に賢くなったのか、それとも有限ホライズンで騙されているだけか」という普及フックに直結できる。
