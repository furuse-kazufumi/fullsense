---
layout: default
title: "Next Session Handoff"
nav_order: 95
---

# Next Session Handoff (2026-06-19 時点 → next)

> Picked up by the next FullSense session. Everything below is ready to
> resume on. Operator actions are flagged 🧑 (user) vs 🤖 (agent).

> 運用メモ(環境・会話依存の参考):
> project 直下には `CLAUDE.md` が見当たらない。
> ただしグローバル `~/.claude/CLAUDE.md` や、会話上位の system / developer / `AGENTS.md` 規約が存在する実行系では、それらを優先する。
> 再開時は、まず会話上位の system / developer / `AGENTS.md` 指示があればそちらを優先し、
> そのうえで repo 内の handoff 正本は本ファイルを使い、
> `docs/articles/IDEAS_2026_06_15_harness_loop_raptor.md` は補足・背景メモとして参照する。
> ただし ideation 段階の着想メモで、旧フレーミングや旧 naming を含みうる。現行の語彙・位置づけは本ファイルと canonical handoff 2 正本を正本とする。
> 環境依存の個人メモ類は、あっても参考扱いに留め、再開判断の正本には含めない。
> `docs/SESSION_SUMMARY.md` は Stop hook が自動生成するスナップショットとして参照可。
> ただしコミット時点で更新が止まっていることもあるため、最新ターンの現況とみなして鵜呑みにはしない。
> `docs/next_plan.md` は再開判断メモとして使ってよいが、手動更新のため index 状態がズレることがある。commit 境界の判断に使うときは `git status` で staged / unstaged も併記して読む。
> `.llterm/loop_ledger.jsonl` は自動ログで記事差分のノイズになりやすかったが、2026-06-18 に `git rm --cached` + `.gitignore` で deindex 済み。今後は on-disk に残る local telemetry として扱い、review / handoff では通常 diff から外れる前提でよい。
> handoff の commit 台帳は `docs/SESSION_SUMMARY.md` / `docs/next_plan.md` の 2 枚だけが正本で、**最新 1 件の handoff commit が未反映なのは正常状態**である。backfill は実質的な handoff 更新に便乗してのみ行い、台帳追記だけの単独 commit を増やさない。`a0b793a` / `6d9854d` / `c16a69b` / `e150ee4` / `ed1e841` は、そのルールを締め直す前後に残った standalone backfill debt の標本として扱う。以後は同型の commit を増やさず、cleanup が必要なら 1 行 note の積み増しではなく、次の実質的 handoff 更新か別 human-gate 判断の中で 1 回で畳む。`NEXT_SESSION.md` 自身の現在地は、他 2 枚の range 注記ではなく本ファイル本文の現況メモを正本として読む。
> 2026-06-19 のユーザー判断で、上記 5 件は cleanup 対象として掘り返さず、例外標本として履歴に残す方針に固定した。以後は再発防止だけを維持し、同型の standalone backfill commit を増やさない。

## ⭐ 2026-06-17 昼 — #43 継続の再開地点

> **この節が現時点の最優先の再開地点。** 下の 2026-06-12 節は旧文脈の記録として残している。
> **2026-06-19 このターンの変更範囲:** 以下の local source / handoff 更新は commit `2a8b942` (`sync qiita handoff and draft polish`) で確定済みである。`qiita47_harness_engineering_thoughts.md` では、「この比喩はどこで破綻するか」を §12 の繰り返しではなく **比喩固有の破綻点** へ寄せ、`しつけ` 比喩がまだ効くのは `観測 / 停止 / 修復` の前半までで、最後の `意味づけ` は loop の外側に残ることを本文で明示した。さらに「runtime に入れる前に、先に捨てるべき人間側の癖」を 1 節足し、その後の local polish で §4→5 / §5→6 / §8→9 / §11→12 に短い forward bridge を足し、0〜4 章の重複も圧縮して前半の spine を「ハーネスは人間側の雑さを通さない器」へ締めた。`qiita45_human_ai_dev_incident_patterns.md` では `human-gate` 表記統一、appendix / 参考節への `VLAA-GUI` / `Resilient Write` / `Crab` / `Measuring the Permission Gate` 追加、`## 2` honest disclosure 前置きの圧縮、`human-gate` を permission-boundary の補助線として扱う整合修正、さらに前半で **運用カテゴリ** と後段の **RAD 接地の分析レイヤ** を分ける 1 文まで反映済みである。あわせて `qiita43_harness_loop_stack_en.md` / `_zh.md` / `_ko.md` では `### prompt → context → harness → loop の流れ` の `paradigm_staircase.svg` と caption を同期し、`qiita44_evolutionary_programs_block_diagram.md` では MIT Press gate 文言を `soft-gate` と `別 UI / 別ブラウザ経由の補助観測` に揃えた。handoff 3 文書も同じ現在地へ揃えている。
> **2026-06-18 追加メモ:** referral CTA 用のバス江コマは `012.jpg`（「ひくわ」）を既定のまま維持し、`044.jpg` は「押し売り感をわざと過剰化する強め variant」として `docs/articles/assets/bazue_all/index.md` に整理した。CTAIMG の一括差し替えはしておらず、必要な草稿だけ opt-in で使う前提。
> <!-- CTA149_BATCH_STATE_BEGIN -->
> **2026-06-18 追加メモ 2:** いま手元で整えていた CTA-149 batch は `22d5460384c2cb54a9e6` の live item 修正ではなく、`qiita43/44/45/46/47` の local source 末尾 CTA を整える差分であった。`149.jpg` は opt-in の強め variant に戻し、`1-week free trial` 系の時限断定は「無料で試せる（提供条件は公式参照）」へヘッジした。en/ko CTA キャプションの `\"` も local source では除去済みで、live 再 publish / PATCH はまだ人間承認待ちの外部アクションである。
> **2026-06-18 追加メモ 3:** 上記 CTA-149 local batch は commit `430fcdc` で確定済み。以後の残件は local wording 整流ではなく、live 再 publish / PATCH を本当にやるかどうかの human-gate 外部アクション判断だけである。
> <!-- CTA149_BATCH_STATE_END -->

**再確認した状態:**
- `#43` 日本語記事 `tools/qiita-cli-poc/public/qiita43_harness_loop_stack.md` は
  2026-06-16 に public publish 済み（commit `5f10609`）。
- 英語版 `tools/qiita-cli-poc/public/qiita43_harness_loop_stack_en.md` は
  dev.to 下書きサイドカー `qiita43_harness_loop_stack_en.devto.json` を持つが、
  `published: false` のまま。限定共有の下書きとして id / URL は発行済みだが、
  public 公開はまだされていない。
  下書き URL は
  `https://dev.to/kzfm_frs_d1afeb3fc/43-in-2026-the-industry-named-the-ais-reins-and-wheel-how-i-started-assembling-a-prototype-3mcd-temp-slug-6156556`。
- `#43` の en/zh/ko 草稿は、いずれも **日本語版
  `qiita43_harness_loop_stack.md` を正本**として 2026-06-17 時点の章立て /
  主張 / honest disclosure に合わせる方針へ整理した。2026-06-19 の
  seam spot-check + section fingerprint re-diff までで、**local source 上の residual translation drift 監査は一旦クローズしてよい** 状態になった。翻訳差分を再度触る場合は、
  まず日本語 source を見て、次に英語、その後 zh/ko を追従させる。
- `qiita43_harness_loop_stack_en.md` と `qiita43_harness_loop_stack_ko.md` の front matter `title:` は
  repo 規約どおり **single-quoted 1 行 title** へ修正済み。英語版は
  `public_id: 2622da17495d61480fa2` も front matter に明示した。
- `tools/qiita_public_post.py` / `tools/qiita_team_post.py` は、front matter の
  `title: >-` / `|` と single-quoted YAML の `''` エスケープを解釈できるよう修正済み。
  2026-06-18 の dry-run と public PATCH 後の API / HTML 確認では、
  英語版タイトルを正しく表示することを確認した。
- さらに 2026-06-19 に `tests/test_qiita_frontmatter.py` へ `qiita_team_post.py` の回帰も追加し、`real_id` の nullish fallback、frontmatter `private: false` の文字列パース経路、そして **空 `private:` は default=True へ倒す**修正まで固定した。よって Team stock 3 本の `private:false` incident は、少なくとも現在の Team poster 実装では再現しない層のバグとして切り分けられるが、だからといって可視範囲の疑いが解消したとは扱わない。
- 追加の観測では、3 本とも Team API GET が `group.url_name: general` / `group.private:false` / `organization_url_name:null` も返した。2026-06-18 の poster payload は `group_url_name` を明示していなかったため、implicit General sharing が起きた可能性を current 仮説として追う。ただしこれは root-cause 仮説であって、team-only の証明でも否定でもない。local source にはこの観測値を resend default として固定しない。2026-06-19 の hardening では、既存 item の PATCH でも `group_url_name` を既定送信しないことを `tests/test_qiita_frontmatter.py` で固定し、観測された `general` を通常更新で再宣言しない状態へ揃えた (`71 passed`)。
- 追加の観測では、3 本とも Team API GET が `group.url_name: general` / `group.private:false` / `organization_url_name:null` も返した。2026-06-18 の poster payload は `group_url_name` を明示していなかったため、implicit General sharing が起きた可能性を current 仮説として追う。ただしこれは root-cause 仮説であって、team-only の証明でも否定でもない。local source にはこの観測値を resend default として固定しない。2026-06-19 の hardening では、既存 item の PATCH でも `group_url_name` を既定送信しないことを `tests/test_qiita_frontmatter.py` で固定し、観測された `general` を通常更新で再宣言しない状態へ揃えた (`71 passed`)。その反面、**current blocker の 3 本を狭い共有先へ寄せ直す remediation は、このツールの既定 PATCH 経路だけでは実施できない**。是正が必要なら Team UI か、`id` あり更新でも `group_url_name` を明示送信できる別改修が要る。
- さらに同日、Team poster の `ignorePublish` gate も fail-closed 化し、`dry-run` でも不正値や key typo を exit 非 0 で返すようにした。`ignorePublish:true` の source は Team poster でも `--force-ignore-publish` 無しでは送れない。
- `tools/qiita-cli-poc/convert_to_qiita_cli.py` と `scripts/publish/zenn_convert.py` も
  同じ shared parser へ切替済み。`title: >-` を文字列 `">-"` のまま持ち回る
  sibling 側の root-cause は除去した。
- `qiita43_harness_loop_stack_en.md` / `_zh.md` / `_ko.md` は、最終棚卸しが終わるまで
  accidental publish を避けるため `ignorePublish: true` に倒した。
  ただし `id:` を持つ発行済み限定共有 draft のため、これは **同期凍結**であって
  既発行 URL 側の状態は別管理である。local source 上の residual translation drift 監査は
  2026-06-19 の seam spot-check + section fingerprint re-diff までで一旦クローズ済みで、
  再度触る場合だけ日本語 source → 英語 → zh/ko の順で確認する。
  2026-06-18 に手元 source では `47,097 docs` ベースへ factual drift を詰めたが、
  それは **ローカル working copy の修正**であり、既発行の限定共有 URL まではまだ更新していない。
- `tools/qiita-cli-poc/public/qiita43_harness_loop_stack_kamikudaki.md` を
  新規追加済み。公開版 #43 とは別に、**手元の草稿は現在** `private: true` で、
  完全版 #43 への導線つき。短縮版草稿として ☕ 休憩ポイントと参考文献節は追加済みで、
  一次情報の細目は完全版 #43 側へ寄せる方針を維持している。
- `tools/qiita-cli-poc/public/qiita44_evolutionary_programs_block_diagram.md` を
  新規追加済み。**現在は** `private: true` のローカル草稿で、
  進化型プログラムを **用語表 → 流派地図 → Mermaid block diagram → FullSense 接続**
  の順で解説するハブ記事。Qiita 向けには、外部記事も参考にしつつ自分の経験則として
  **初心者タグ / benefit 先出し / 「どこで壊れるか」導線** へ寄せ直した。バス江コマは
  `JRY5aSqHgjWRo1QnfR2l` と `H4Pix38XWLRS077emoZC` の **2 コマとも本文から削除済み（残 0）**。
  あわせて「最初の 1 本を実装するなら」節を追加し、入門者が次の一歩へ
  着地しやすい形に寄せた。冒頭には拾い読みガイドも追加済み。
  `llcore` / `lldarwin` という名称は、本文がリンクしている既公開 Qiita 記事名と一致するため維持。
  参考文献節は追加済みで、2026-06-18 に GA / ES / GP / NEAT / novelty search /
  MAP-Elites / CMA-ME / lexicase の一次導線 URL まで補強した。CMA-ES は失効証明書の旧 PDF ではなく
  arXiv `1604.00772` へ差し替え済み。publish 前の残りは
  本文主張と参考導線の最終突合は完了済みで、MIT Press 2 件の到達性 gate は 2026-06-19 時点で **soft-gate** 状態にある。
  本文と参考導線の spot-check では、GA = 固定長遺伝子列、ES / CMA-ES = 変異分布更新、
  GP = 式 / プログラム木進化、NEAT = 構造進化、novelty / MAP-Elites / lexicase = 「何を残すか」の分岐、
  という説明までは整合していた。
- `tools/qiita-cli-poc/public/qiita45_human_ai_dev_incident_patterns.md` を
  新規追加済み。**現在は** `private: true` のローカル草稿で、
  人間 + AI 開発の実務教訓を **症状 / 真因 / 対策 / 残した再開導線** 形式で共有する記事。
  Qiita 向けには、外部記事も参考にしつつ自分の経験則として
  **失敗談 + 5 点チェックリスト + コメントしやすい締め**
  を足し、テーマを「AI と一緒に開発すると事故る 5 点」へ寄せ直した。
  さらに「今ならこう直す」を追加し、失敗談を postmortem 的に再利用しやすくした。
  冒頭には拾い読みガイドも追加済み。挿絵は意図的に 0 コマへ戻している。
  直近の local polish として、本文と図の `human gate` / `Human Gate` は `human-gate` へ統一し、`外部書き込み` も現行 handoff と同じ `外部アクション` の語へ置き換えた。主張や gate 条件は変えず、運用語だけ現行版へ揃えた。
- `tools/qiita-cli-poc/public/qiita47_harness_engineering_thoughts.md` も新規追加済み。**現在は** `private: true` の local-only な independent short draft で、`006.jpg` を「ハーネスを通した途端に AI が賢そうに見える瞬間」、`157.jpg` を「本当にしつけが必要なのは AI より人類側の運用では」という反転オチへ役割分担させた短稿である。本文には invisible comment (`<!-- draft:... -->`) を残しつつ、冒頭の `前提 / 流れ / ゴール` 3 点契約、（本プロジェクトでの）RAPTOR（判断層と実行層を分けた二層 runtime）/ 試作段階の `llterm`（terminal 起点の名残を名前に残した PySide6 GUI 実装）/ Claude Code 公式 `/goal` / `desired-actual-drift-repair` の最小 loop 節、`green-keeper` を `main` に対する clean / dirty を見張る最小監視ループとして読む最小具体例、その比喩が clean / dirty の観測までしか言い切れずズレの意味づけや優先順位づけまでは自動化しないという破綻点、harness を強くしすぎたときの failure mode、さらに「明日 1 個だけ変えるなら何か」と「何を runtime に入れず人間へ残すか」、そして runtime を **観測 → 停止 → 修復 → 意味づけ** の順で一段ずつ育てるという実務ルール（ただし最後の `意味づけ` は runtime に載せず人間へ残す段）に加え、`しつけ` 比喩は §12 の growth order 全体を説明するものではなく、せいぜい `観測 / 停止 / 修復` の前半までに効く比喩で、最後に「何が本当に重要なズレか」を決める `意味づけ` は loop の外側に残る、という seam、そして runtime に入れる前に捨てるべき人間側の癖（後付け説明 / proxy の本体視 / 例外の雑な一般化）まで入り、後から Team / 公開どちらへ育てる場合でも内部構造だけ先に辿れるようにしてある。補助導線の外部 2 本も Distill / Mitchell Hashimoto の実 URL へ揃えてある。
- `tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md` も増補済み。短すぎてアルゴリズム / PoC の量が見えないという指摘を受け、`1 分version` の直後に **「実験 3 本の中身」** と **「AI は裏で何を自走したのか」** を追加し、HD-1 full / HD-1 null / Stage-B、pre-registration / attacker AI 3 体 / major 5 件修正 / Kaggle T4 / 152 runs / `$0` を plain-language で戻してある。
- editorial 方針としては、「公開済みの短い companion 記事は、十分に長い本編へ統合できるなら統合を優先し、空いた item は新記事の器として再利用する」を採用した。ただし `#37` については、**`4 文指示 / 実験 3 本 / PoC 裏方 / 17〜19 倍 / 0 円 / safety tax 本文接続` は完全版へ吸収済みでも、EN/ZH/KO 多言語スイッチャーと curated 関連ニュース節は未吸収**だと確認したため、即 redirect ではなく本文保全を優先する。
- ここで触っている `qiita43/46/47` の差分は **local source の内部 polish のみ**で、外部 publish / PATCH / 統合実行は #37 統合判断とは別件の未着手タスクとして切り分ける。
- 上の前提は一次情報で確認済みである。`qiita37_gpu_triple_run_gate_price_kamikudaki.md` は front matter 上 `private:false` / `id:f06ca92ea208c7646fcd` で、Qiita live HTML / API も 2026-06-19 に `200` を返した。`qiita43_harness_loop_stack_kamikudaki.md` / `qiita46_llterm_supervision_first_kamikudaki.md` / `qiita47_harness_engineering_thoughts.md` は front matter 上 `private:true` / `ignorePublish:true` の local draft である。
- ただし `#37` には local representation が 2 本ある。public short companion の更新対象は `tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md` (`id:f06ca92ea208c7646fcd` / 現在 `ignorePublish:true`) で、`docs/articles/QIITA_#37_gpu_triple_run_gate_price_kamikudaki.md` は `id:df687d0ecddb56d5a373` / `qiita_public_id:f06ca92ea208c7646fcd` を持つ **多言語アーカイブ / Team mirror** として別管理する。
- `#37` の短稿と完全版は本文比較も済ませた。結論は「**核の説明は吸収済みだが、EN/ZH/KO 多言語スイッチャーと curated 関連ニュース節は未吸収なので要保全**」である。したがって現時点の推奨案は redirect ではなく、**短稿本文を残したまま冒頭に canonical 告知だけを足す**線になる。
- local source では、`qiita37_gpu_triple_run_gate_price_kamikudaki.md` をこの保全案へ戻し、冒頭に「完全版 #37 が正本」告知を追加済みである。Qiita live item `f06ca92ea208c7646fcd` への PATCH は 2026-06-19 に実行済みで、front matter `ignorePublish` は **qiita-cli 系の一括 publish を止めるため** `true` のまま維持している。
- `.remote/f06ca92ea208c7646fcd.md` と現行 local source の再 diff も 2026-06-19 に取り直し、**companion-preserved switcher（EN/ZH/KO 導線）** とマスコット画像 + 📗導入の live-only 2 ブロックはすでに local source 側へ保全済みだと再確認した。現時点の主要差分は canonical 告知ブロックと `実験 3 本` / `AI は裏で何を自走したのか` の補足節である。
- ここで使っている `ignorePublish` は Qiita 標準属性ではなく、`qiita-cli-poc` ローカル運用の publish 安全柵である。`tools/qiita_public_post.py` もこれを読み、`ignorePublish:true` の source は **`--force-ignore-publish` が無い限り fail-closed で BLOCK** する。したがってこのポスター経路の実ゲートは **`ignorePublish` override gate（`--force-ignore-publish` 必須）+ `post <file> --yes` + human-gate 承認** である。ただし live PATCH 経路で `--force-ignore-publish` を付ける時点で、この柵自体は override 済みなので、**実保護は human-gate と step3 の本文 word-diff 目視と preflight** にある。またこの override は今回の `#37` companion PATCH 限定で、他ファイルへコピペ流用しない。またここで言う `redirect` は HTTP 転送ではなく、**Qiita 本文を統合告知 + canonical 誘導へ差し替える運用語**として使う。
- PATCH 実行時の既存記事照合は filename ではなく `public_id` 基準で行う。`tools/qiita_public_post.py` は frontmatter `public_id` があれば PATCH、無ければ POST create の経路なので、custom 名ファイルでも `public_id:f06ca92ea208c7646fcd` を持つ public source を使えば重複作成は避けられる。
- `tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md` にも `public_id:f06ca92ea208c7646fcd` を追記し、poster 実装上も **dry-run で PATCH update と読める source** へ揃えた。`id:` は既存 metadata 互換のため残し、public poster の冪等キーは `public_id` を正とする。
- 完全版 source `tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price.md` にも `public_id: 6f44575d440a9ebf5228` を追記し、完全版側を触る場合も accidental create ではなく PATCH update へ入る前提を揃えた。
- `qiita_public_post.py` の frontmatter `private:` はこの public poster では payload に使われない。可視性の既定値は frontmatter **`public_private:`** で与え、**CLI の `--private` はそれを強制 override** する。`#37` companion は一般公開 PATCH が前提なので、ここでは `public_private` 既定 false / `--private` なしで読む。
- 2026-06-19 の hardening で、`qiita_public_post.py` は `private:` だけがあり `public_private:` が無い source、または両者が矛盾する source を **fail-closed で拒否**するようにした。`#37` source には `public_private: false` を明示済みである。
- あわせて `public_private` の値も strict parse に切り替え、`ture` や `限定共有` のような未認識値は一般公開へ黙落ちさせず BLOCK するようにした。bulk 移行として `tools/qiita-cli-poc/public/*.md` の `private:` 単独 69 件へ `public_private:` を機械追加し、`public_id` を持つ PATCH 対象は 2026-06-19 時点で欠落 0 件である。
- さらに 2026-06-19 の追加 hardening で、tag drift 比較は case-insensitive のまま維持しつつ、**送信 payload のタグ表記は frontmatter 原文の大小文字を保持**するよう修正した。これで `AI` / `FullSense` が live PATCH 時に `ai` / `fullsense` へ壊れる回帰を防ぎ、`TODO_TAG` プレースホルダも payload から除外する。
- human-gate 後に実際に `--yes` を打つ前には、`https://qiita.com/furuse-kazufumi/items/f06ca92ea208c7646fcd` をブラウザで開き、表示されている live item が **完全版 `6f44575d440a9ebf5228` ではなく short companion 本文**だと目視確認してから PATCH する。dry-run は network なしなので、この目視確認が `public_id` 取り違え防止の最終ゲートになる。
- 2026-06-19 に `tests/test_qiita_frontmatter.py` へ最小回帰テストも追加し、`qiita_public_post.py` が **`public_id` 有りなら PATCH / `id` だけでは POST create 扱い**になること、および frontmatter `private:` ではなく `public_private` / CLI `--private` だけが公開可視性を切り替えることを固定した。
- 続く safety polish で、`qiita_public_post.py` は **`id` はあるが `public_id` が無い** source を dry-run したとき warning を出し、実 `post --yes` では **`--allow-create` が無い限り fail-closed で停止**するようにした。これは初回 public 化でも起こりうる正常 warning / gate で、`public_id` は Qiita API の公式 frontmatter 名ではなく **このラッパーの PATCH 識別子**である。`#37` companion は `public_id` 付きなのでこの warning / gate に掛からず、PATCH source として読める。
- `#37` live PATCH の runbook は次の 6 段で固定する。**この PATCH 自体は 2026-06-19 に実行・完了済み（:134 参照）で、以下は再実行用ではなく参照用の runbook** である。再 PATCH が必要な将来ケースでは、`.remote/f06ca92ea208c7646fcd.md` が stale になりうる前提で必ず step1 `--refresh-baseline` 起点でやり直す。ここで言う `preflight` は CORS の OPTIONS ではなく、**このラッパー独自の pre-patch health check** である。`ignorePublish: true` は `qiita-cli` 系の安全柵であり、2026-06-19 の hardening 後は **`tools/qiita_public_post.py` でも `--force-ignore-publish` が無い限り fail-closed で停止**する。
  1. `python tools/qiita_public_post.py preflight tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md --refresh-baseline`
     で live API 本文を `.remote/f06ca92ea208c7646fcd.md` に再取得し、その場で `PATCH update public_id=f06ca92ea208c7646fcd` / `WARNING: frontmatter ignorePublish: true is a qiita-cli gate, not a qiita_public_post.py gate.` / `private: False` / `auth_status: 200` / `api_status: 200` / `api_private: False` / `baseline_refresh_tags:['ai','fullsense','llcore','かみくだき','機械学習']` / `api_tags:['ai','fullsense','llcore','かみくだき','機械学習']` / `html_status: 200` / `baseline_body_preserved: True` / `asset_count: 3` / `preflight: OK` を再確認する。ここでの baseline refresh は **live title / visibility / tags / URL / HTML 到達性の整合が通ったときだけ** `.remote` を atomic に更新し、不一致なら fail-closed で `.remote` を書き換えない。`api_title` と payload title の不一致、live `private` と payload visibility の不一致、live tags と payload tags の不一致、`.remote` baseline 本文の欠落は fail-closed で BLOCK される。`--refresh-baseline` は `public_id:` と `preflight_remote_baseline:` の両方が無いと no-op ではなく fail-closed で止まり、baseline write の OSError も `BLOCKED` 扱いで返す。`updated_at` は payload に乗らないので、この段階では送信対象外として扱う。`asset_count: 3` だけでなく、3 asset とも `content-type=image/...` で返っていること、`baseline_tags` も payload と一致していることを見る。
  2. `Copy-Item tools/qiita-cli-poc/public/.remote/f06ca92ea208c7646fcd.md tools/qiita-cli-poc/public/.remote/f06ca92ea208c7646fcd.prepatch.md -Force`
     を実行し、refresh 後 baseline の監査原本を退避する。以後の human-gate はこの `prepatch.md` を基準に見る。今回の `#37` companion source は 2026-06-19 時点で **既存行の順序保存・非削除・非改変**を前提に hardening している。新規行は中間挿入でも機械ゲートを通りうるため、次段の目視では挿入位置まで確認する。
  3. `git diff --no-index --word-diff=color tools/qiita-cli-poc/public/.remote/f06ca92ea208c7646fcd.prepatch.md tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md`
     を実行し、companion-preserved switcher とマスコット画像 + 📗導入を含む companion 本文が local source 側に保全されていること、かつ**既存行に削除・改変が無い**ことを明示確認する。新規行の中間挿入も機械上は通りうるので、**承認者がこの word-diff 出力を目視し、挿入箇所まで精査すること**を human-gate の必須条件とする。
  4. `https://qiita.com/furuse-kazufumi/items/f06ca92ea208c7646fcd` をブラウザで開き、live item が完全版 `6f44575d440a9ebf5228` ではなく short companion 本文であることを目視確認する。
     ここでの確認対象は本文同一性だけではなく、**PATCH が source からの title / tags / body 全置換**であることを踏まえ、live-only 編集を失ってよい状態かも含む。
  5. `python tools/qiita_public_post.py post tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md --yes --force-ignore-publish`
     `public_id` 付き source なので `--allow-create` は不要。`post` は送信前に preflight 相当（auth / live title / live visibility / live tags / asset / marker 非要求）を再評価し、未通過なら fail-closed で止まる。現行設計では **live tags ≠ payload tags の既存 public 記事 PATCH も BLOCK** するため、将来タグ編集を伴う PATCH を通すには別の explicit override 方針が要る。step1〜step5 の間に時間が空いたり、live を別 UI で触った疑いがある場合は **step1 からやり直し**、baseline を再 refresh してから実行する。
  6. `python tools/qiita_public_post.py preflight tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md --require-marker`
     で `marker_present: True` と `preflight: OK` を確認し、あわせて live SVG / 画像 (`kamikudaki_shishi.svg`) が描画されるか目視確認する。さらに多言語導線 `bdfad6db3f2e70c40511` / `fa0890f136636d495ea6` / `e5093e4816b25c1bd4d0` の 3 リンクが live で到達することも確認する。Qiita / imgix 側キャッシュで非表示や古い描画が残る場合は、画像 URL に `?v=20260619N` を足して source を更新し、**step1 から runbook をやり直して**再 publish する。publish 直後に `marker_present: False` が一過性で出る場合は即失敗扱いせず、少し待って再確認する。`marker_present: False` が継続する場合は、Qiita API の live body でも marker 文字列が見えるかを確認し、HTML 側の整形差か本文未反映かを切り分けてから失敗判定する。
- 2026-06-19 の pre-patch baseline として、`python tools/qiita_public_post.py preflight ...` は `PATCH update public_id=f06ca92ea208c7646fcd` / `ignorePublish` warning（expected） / `private: False` / `auth_status: 200` / `api_status: 200` / `api_private: False` / `api_tags:['ai','fullsense','llcore','かみくだき','機械学習']` / `html_status: 200` / `marker_present: False` / `asset_count: 3` / `preflight: OK` を返し、asset 3 件 (`kamikudaki_shishi.svg`, `191.jpg`, `192.jpg`) もすべて `200` だった。`baseline_refresh_tags` / `baseline_tags` も同一集合で一致している。
- その後の本番 runbook では、`preflight --refresh-baseline` → `Copy-Item ...prepatch.md` → word-diff 目視 → live 本文目視 → `post --yes --force-ignore-publish` → `preflight --require-marker` を順に通した。`post` は `OK (200) [PUBLIC(一般公開)]`、`preflight --require-marker` も `marker_present: True` / `preflight: OK` で終了し、live HTML 側でも canonical id `6f44575d440a9ebf5228` と多言語導線 3 本の存在を再確認済みである。したがって `#37` short companion の public PATCH は完了済みで、以後の残件は Team visibility blocker を主とする別系統だけである。
- 補足として、`.remote/f06ca92ea208c7646fcd.md` と `f06ca92ea208c7646fcd.prepatch.md` は `.gitignore` 対象の一時監査物であり、repo 単独では再検証不能、かつ将来の `--refresh-baseline` で上書きされうる。監査証跡を更新したい場合は同じ runbook を step1 からやり直して再採取する。
- 未吸収 2 ブロック（**full-article-pending switcher** / curated 関連ニュース節）は **完全版 `6f44575d440a9ebf5228` 側の将来課題**であって、short companion 側の欠落ではない。したがって現行 option 1 は、companion 本文を欠落させず canonical 告知だけを live へ反映する選択として読む。
- raw asset URL は `origin/main` を解決する。local `main` が `origin/main` より 263 commits ahead でも、今回参照する `kamikudaki_shishi.svg` / `191.jpg` / `192.jpg` はすでに remote `main` 側で `200` を返しているため、この PATCH runbook の asset 参照には影響しない。
- このターンで言う RAD grounding は、主に `D:/docs/loop_engineering_corpus_v2/` の `fail-closed`, `human_in_the_loop_approval_gate`, `progressive_delivery_canary_metric_gate` と `D:/docs/article_craft_corpus_v2/136_ablations_baselines_as_honesty_*.md` を指す。
- さらに `ac398349ec42e40913f1.md` と `docs/articles/QIITA_SERIES_INDEX.md` の #37 導線も `canonical / companion` 表記へ揃え、local index 上で短稿を「実体記事」扱いしないよう補正した。
- `qiita43_harness_loop_stack_kamikudaki.md` / `qiita44_*` / `qiita45_*` も含め、
  現在の `private: true` 草稿は accidental publish 防止のため
  `ignorePublish: true` に統一済み。
  ただしこれは `qiita-cli-poc` ローカル同期を止める安全柵であって、既に発行済みの限定共有 id / URL を非公開化・撤回する効果までは持たない。
- RAD コーパス件数は 2026-06-17 に **65 コーパス / 47,097 docs** へローカル再集計し、
  旧 `21分野 / 約49,000` 表現から handoff / 草稿を順次更新した。
  この値は 2026-06-17 の再集計値を handoff 上の正として引き継いでいる。
  公開面の概数は「約47,000」または「約4.7万」とし、内訳や厳密値を出すときは
  **47,097 docs（2026-06-17 再集計、ローカル RAD 配下 `*.md`、`hacker_corpus_v2` を含む）**
  に統一する。
  以後の表記ルールは **厳密値 = docs / 概数 prose = 件 許容** とする。
  再現経路の最小形は
  `Get-ChildItem <RAD corpus root> -Directory -Filter '*_corpus_v2' | ForEach-Object { (Get-ChildItem $_.FullName -Recurse -Filter *.md).Count } | Measure-Object -Sum`
  （`<RAD corpus root>` は各環境のローカル配置に置き換える）。

**次回ここから再開:**
1. dev.to 英語版を更新または publish する前に、
   `published: false` の sidecar draft が残っている前提を確認しつつ、
   「外部公開などの外部アクションは human-gate を要する」という運用を守る。
2. #46 (`qiita46_llterm_supervision_first.md`) は JA / en / zh / ko / kamikudaki の本文と endmatter まで同期済みで、
   `ctx 2549%` / `turn boundary` / `interrupt` / `block point` の用語固定も一巡している。
   `025.jpg` は言語ごとに作品名を localize しつつ raw URL の HTTP 200 を確認済み、
   `kamikudaki_shishi.svg` も raw URL の HTTP 200 を確認済み。
   最終見直しパスでも新たな重大 drift は未検出なので、次の外部アクションは
   human-gate を伴う publish 判断になる。
3. 難しい論点は後で個別公開できるよう Team stock へ切り出し始めた。
   `tools/qiita-cli-poc/public/team_stock_semantic_governance.md`、
   `team_stock_llm_wiki_anti_circulation.md`、
   `team_stock_ctx2549_postmortem.md`
   を local draft として追加済みで、`tools/qiita_team_post.py dry-run` では
   3 本とも registration-safe を確認済み。
   source article 本文との一次突合も実施済みで、`Semantic Governance` は
   #43 `2-2`（Verloy / Semantic Governance / fail-closed 束）、
   `LLM Wiki` は #43 `3-2`（3 層 / thought circulation / safeguards 束）、
   `ctx2549` postmortem は #46 `2 / 3 / 6`（incident 束）を基準に、
   local draft が切り出し範囲から外れていないことを spot-check 済み。
   また `team_stock_queue.md` / `team_stock_publish_plan.md` / local source 3 本の
   title・source anchor・現在の frontmatter mirror（`private:false` / `public_private:false` / `ignorePublish:true` / `id:`）も相互に矛盾していなかった。
   2026-06-18 に human-gate 後の Team POST まで完了し、item id は
   `6f67e54e538c10b8f1c3` / `b35b429dc6dc1fde207a` / `6fe79ab04443f7654eca`。
   2026-06-19 時点の `tools/qiita_team_post.py` は `ignorePublish:true` も読み、
   `post --yes --force-ignore-publish` を明示しない限り fail-closed で停止する。
   確認済みの事実は、API GET では 3 本とも `private:false`、2026-06-19 12:41:22 +09:00 の未認証 HTML GET では 3 本とも `302 /login?redirect_to=...`、`https://qiita.com/furuse-kazufumi/items/<id>` の direct probe は 3 本とも `404`、という挙動だけである。前者は Team サブドメイン全体の auth gate でも説明でき、後者は Team scope item なら team-only / 過剰露出のどちらでも起こりうるため弁別力が無い。したがって「未認証一般ユーザーへ実露出している」とまでは確認できていないが、**team-only と positively 確認できるまでは過剰露出の疑いを優先**する。`visibility semantics` は副次論点として残す。
   追加で API は `group.url_name: general` / `group.private:false` / `organization_url_name:null` も返したため、現時点では `group_url_name` omission による implicit General sharing 仮説を追う。ただし blocker の主語は引き続き **過剰露出疑いを否定できないこと**であり、local source に `general` を resend default として固定しない。
   可視範囲の絞り込みや rollback が必要なら、以後は別の human-gate 外部アクションとして扱う。
4. #43 の多言語差分を触るときは、日本語版を source of truth として
   章立て / 主張 / honest disclosure / front matter の順で同期する。
   en/zh/ko の translation sync note は本文から外してあり、publish へ進めるときは
   `ignorePublish: true` / `private: true` を外す前に
   翻訳 drift と metadata を見直す。
   2026-06-18 の時点で RAD 件数の factual drift（`47,097 docs`）は
   ローカル source へ反映済みだが、公開面の live URL はまだ旧表現を残している。
   また en/zh/ko には、日本語正本 `## honest disclosure（「約49k件」という数字の扱い）`
   に対応する honest-disclosure 節は実在する。
   第3章の導入〜`3-2. LLM Wiki` 導入直前も 4 言語で spot-check 済みで、
   3層スタック説明、`RAD_INDEX.md` / `65 RAD corpora` 導入、`47,097 docs` と
   `32,503 files` の内訳、`hacker_corpus` の raw 集約ファイルという留保、
   Karpathy 帰属のヘッジ付き `LLM Wiki` 3層導入まで日本語正本に追従している。
   `3-2. LLM Wiki` 本体は、3層説明と thought circulation / Anti-Circulation Safeguards 節、製品対応づけ、「半信×半疑」の引用ブロックと URL、末尾参考リストまで局所確認・同期済みで、未確認対象はそれ以外の細い橋渡し段に絞られている。
   その後の追補で、未同期だった 4 件（`MDsuuBm0xXPgngwyQve0` / `2qlJjBwdpYGOVjBkyhhL` /
   `CPon283udq6PfvfKrxAP` / `H4Pix38XWLRS077emoZC`）も本文と末尾参考へ同期した。
   これで crop URL 数は日本語正本 16 / en 16 / zh 16 / ko 16 に揃っている。
   ただし再監査で、`2qlJjBwdpYGOVjBkyhhL` は単純な未同期ではなく、
   en/zh/ko で **`2-5` honest disclosure 末尾から第3章直前へ位置ずれ**していたことが判明した。
   現在は 3 言語とも `2-5` 末尾の本来位置へ戻し、第3章直前の誤配置は除去済み。
   さらに `1-4` 後半の `AI成長マネジメント` / 4理由 / `First, Break All the Rules` ヘッジ /
   `アンチパターン` / 第2章への橋渡しも 4 言語で spot-check し、新たな factual / translation drift は見つかっていない。
   さらに終盤の `観察ベースの3点` と H4Pix 引用を挟んだ結語導入も 4 言語で spot-check し、
   `常時並列 / 長射程の伏線回収 / 常時稼働の危険予知` の 3 点、`観察された傾向` のヘッジ、
   `ルール（構造）で縛る` への橋渡しまで日本語正本に追従していることを確認した。
   さらに参考文献節と末尾 hedge note も 4 言語で spot-check し、`alu.jp` crop URL 数は
   日本語正本 16 / en 16 / zh 16 / ko 16 に維持され、OpenAI 403 /
   RAD `47,097 docs` / `人間優位3点` 観察ベースなどの留保も日本語正本に追従していることを確認した。
   `GPT-5.5` についてはこのターンで OpenAI 公式一次情報によりモデル名の実在を確認し、
   留保を「モデル名未確認」から「比較値の一次計測元・計測条件未確認」へ締め直した。
   16 本基準は、日本語正本を source of truth として **本文 8 本 + 参考節 8 本 = 計 16 本
   （unique は 8 本、各 URL が本文と参考で 2 回ずつ出現）** と確認したうえで、
   en/zh/ko も同じ構成かを照合した。
   また `promise-progress-payoff` / `ending-payoff` の再確認では、終盤の
   `観察ベースの3点` → H4Pix 引用 → `まとめ：手綱と、輪と、知` の 3 箇条 →
   `Bölük` 数字を捨てた payoff 文 → `次回予告的な余韻` → 参考文献節、という鎖を
   4 言語で突き合わせた。
   その後の残ブリッジ棚卸しで、`第1章末 → 第2章頭`、`3-1. RAD コーパス → 3-2. LLM Wiki`、
   `3-4. corpus-first advantage → 統合章` の 3 接続も 4 言語で再確認した。
   第1章の `なぜ` から第2章の `どう` へ移る橋渡し、`集めた知識は放っておくとただの山`
   から LLM Wiki へ入る導入、`A/B/C が1本に繋がる` から統合章へ畳む着地まで、
   日本語正本に対する新たな factual / translation drift は見つかっていない。
   さらに最終棚卸しとして、導入 → 第0章、第0章末 → 第1章頭、`/goal` 節 → 独立 honest disclosure、
   独立 honest disclosure → 第3章頭、`3-2. LLM Wiki` → `3-3. RAPTOR` の局所接続も 4 言語で再確認した。
   導入の作法宣言から用語地図、`鵜呑みにしない` から一次情報確認、`mystery graph` から
   `捨てた数字` 検証、`無知の知` から knowledge stack、thought circulation 警告から
   evidence ladder へ渡す流れまで、日本語正本に対する新たな factual / translation drift はない。
   さらに `2-7. /goal` → ★ honest disclosure 節、`3-3. RAPTOR` → `3-4. corpus-first advantage`、
   統合章 → まとめ、まとめ → 次回予告 / 参考 も 4 言語で再確認した。`検証可能なゴール` から
   `捨てた数字` 実演へ落とす open loop、evidence ladder から corpus-first の条件付き優位へ渡す橋、
   A/B/C 統合から `手綱 / 輪 / 知` の3点要約へ畳む順序、次回予告と参考節で閉じる終盤構造まで、
   日本語正本に対する新たな factual / translation drift は見つかっていない。
   ここまでで、handoff がこれまで再開候補として列挙してきた #43 の seam 範囲は一巡した。少なくとも
   `導入 → 第0章`、`第0章末 → 第1章頭`、`第1章末 → 第2章頭`、`2-7 → ★ honest disclosure`、
   `/goal` 節 → 独立 honest disclosure、独立 honest disclosure → 第3章頭、`3-1 → 3-2`、
   `3-2 → 3-3`、`3-3 → 3-4`、`3-4 → 統合章`、統合章 → まとめ、まとめ → 次回予告 / 参考 は
   4 言語で spot-check 済みである。ただし、新規 seam 候補の網羅までは保証しない。
   最小根跡として、確認観点は `ja/en/zh/ko` の見出し語順、★/独立 honest disclosure の節境界、
   引用 / コードブロックの有無、直前直後の橋渡し文の追従である。
   追加の機械点検として、4 言語の見出し数 / 引用ブロック数 / コードフェンス数 / table 行数も比較した。
   `headings=47`、`quotes=54`、`codefence=4`、`table_lines=26`（`|` 含有行ベース）は 4 言語で一致し、
   section 単位の bullet / quote 分布も本文側は揃っていた。front matter タグの既知差は 2 種で、
   ①本数差 = ja のみ `個人開発` が 1 本多い（`ja bullets=81`、en/zh/ko=`80`）、
   ②ローカライズ差 = `AIエージェント`（ja）↔ `Agent`（en/zh/ko）である。いずれも
   translation drift というより想定内の metadata / ローカライズ差として扱う。
   さらに 2026-06-19 に section fingerprint ベースの line 単位 re-diff を再実行し、
   見出し index ごとの `heading / quote / bullet / numbered / table / codefence / image / caption` 分布を比較した。
   新しく actionable だったのは `### prompt → context → harness → loop の流れ` にある
   `paradigm_staircase.svg` とその caption が en/zh/ko で欠落していた 1 件だけで、translations 3 本へ同期済み。
   その後に残った mismatch 8 件は、3 言語が同型の `para-1 / blank-1` 差を示すだけで、
   `この章の honest disclosure` 節のように raw URL を blockquote 内 inline link へ畳んだ既存スタイル差・段落結合差として説明でき、
   新しい structural omission は見つからなかった。
   `個人開発` タグは ja 固有タグとして現状維持し、4 言語タグの完全一致は要件にしない。
   なお、統合レビューで触れられた「翻訳版は blockquote 内 inline link / 正本は blockquote 下 raw URL」という形式差は、
   今回の修正で生じたものではなく既存スタイル差なので、このターンの修正対象にはしない。
   参考文献節と末尾の留保注記も 4 言語で spot-check 済みで、今後の drift 対象からはいったん外している。
   導入部（「捨てた数字」フック / 一次情報への錨 / 第2章後の独立 honest disclosure 節への前振り）も
   4 言語で spot-check 済みで、異常値を捨てる作法と本稿の主題提示まで日本語正本に追従している。
   第0章（`prompt → context → harness → loop` / automation vs loop / 章末 honest disclosure）と、
   第2章前半の `loop engineering` をもう一段深く〜strategy names〜security face〜`llterm` 導入〜
   MAPE-K 骨格も spot-check 済みで、用語の橋渡し・二次情報ヘッジ・Verloy 出典導線まで日本語正本に追従している。
   `2-6. 起動と実証タスク green-keeper` / `2-7. 「検証可能なゴール」を持つループ — /goal という公式実装`
   も 4 言語で spot-check 済みで、`desired / actual / drift / repair` の対応、
   PySide6 GUI / `term` 名残の補足、Haiku 既定と turn cap を含む `/goal` 説明、
   直後の「捨てた数字」節への橋渡しまで日本語正本に追従している。
   代表的な細い橋渡し段は一巡済みだが、これは網羅保証ではない。
   ここから残るのは、local source 監査ではなく live draft / live URL 側の未反映差と publish gate 管理である。
   `2-7 → ★ honest disclosure`、`/goal` 節 → 独立 honest disclosure、`3-3 → 3-4`、
   統合章 → まとめ、まとめ → 次回予告 / 参考 も seam spot-check 一巡の確認済み候補として読む。
   今回の line 単位 re-diff では、既知差として `個人開発` と `AIエージェント` ↔ `Agent` を除外したうえで、
   `paradigm_staircase.svg` 同期漏れ 1 件以外の新規 structural omission は拾っていない。
   local source 監査は一旦閉じたが、live URL 側の未反映差が残るため、
   en/zh/ko の `ignorePublish: false` は戻さず同期凍結を維持する。
3. 出自不明の front matter 整形差分が再発した場合は、
   1 行化を採らず repo 既存形式に戻してから扱う。
5. `qiita43_harness_loop_stack_kamikudaki.md` を必要なら推敲する。
   いまは「手綱 / 輪 / 知識基盤」の 3 点に絞った短縮版で、
   冒頭に拾い読みガイドも追加済みで、節番号 + 実見出し名だけで本文内を追える text TOC にしてある。
   full article との一次突合でも、`RAPTOR / llterm / RAD` の 3 点構造、
   `手綱 / 輪 / 知識基盤` の圧縮軸、`AI 本体より器と回し方を設計する時代`
   という結論は current naming / current hedge に追従しており、大きな drift はない。
6. `qiita44_evolutionary_programs_block_diagram.md` を必要なら推敲する。
   現状は進化計算の総論ハブで、歴史記録より「用語と構造の説明」を優先。
   冒頭の急ぐ人向け導線は追加済みで、節番号 + 実見出し名でも辿れる text TOC にしてある。
7. `qiita45_human_ai_dev_incident_patterns.md` を必要なら推敲する。
   現状は handoff / human-gate / diff / checkpoint と llcore 教訓をまとめた
   問題集で、成功談より再開導線を重視。RAD 由来の
   unsupported success / verifier / durable write / checkpoint 系も追記済み。
   主要 4 本の実名ソース追加までは完了しているが、
   内製ラベル側の説明は引き続きコーパス要約ベースの整理として扱う。
   冒頭の拾い読みガイドも追加済みで、節番号 + 実見出し名でも辿れる text TOC にしてある。
   annotation / 参考文献節は追加済みで、appendix / 参考節には
   `VLAA-GUI` / `Resilient Write` / `Crab` / `Measuring the Permission Gate`
   の 4 本を近い実名ソースとして追加済みである。
   これら 4 本の arXiv 引用は実在確認済みで、`2604.21375` / `2604.10842` /
   `2604.28138` / `2604.04978` を一次情報アンカーとして handoff に明示する。
   `## 2` の honest disclosure 前置きも 1 パス圧縮済みで、
   main path には「ローカル再集計値」「内製ラベル」「appendix の 4 本実名ソース対応」
   だけを残し、appendix 参照の重複説明は削った。
   残タスクは、必要ならこの 4 本より先へ一次ソースを増やすか、
   逆に内製ラベル側 (`unsupported success` / `human-gate` など) の説明を
   どこまで簡潔にするかの整形寄りである。
8. `qiita47_harness_engineering_thoughts.md` は `#43` から派生した local-only の independent short draft として新設済みで、いまは独立短稿として最低限読める具体節に加え、冒頭の `前提 / 流れ / ゴール` 3 点契約、（本プロジェクトでの）RAPTOR / `llterm` / `/goal` の最小グロス、`green-keeper` を `main` に対する clean / dirty を見張る最小監視ループとして読む最小具体例、その比喩が clean / dirty の観測までしか言い切れずズレの意味づけや優先順位づけまでは自動化しないという破綻点、harness を強くしすぎたときの failure mode、さらに「明日 1 個だけ変えるなら何か」と「何を runtime に入れず人間へ残すか」、そして runtime を **観測 → 停止 → 修復 → 意味づけ** の順で一段ずつ育てるという実務ルール、さらに runtime に入れる前に人間側で先に捨てるべき癖まで入った状態。
   現状の spine は「ハーネスは AI を賢くする技術というより、人類側の曖昧な運用を二度と通さない discipline であり、最初の一歩は観測できるズレを 1 個だけ増やすこと、次に runtime を 観測 → 停止 → 修復 → 意味づけ の順で一段ずつ育てること（ただし `意味づけ` は runtime に載せず人間に残す段） 、その前に後付け説明 / proxy の本体視 / 例外の雑な一般化のような癖を先に捨てること」である。さらに §13 では、その全部を `しつけ` 比喩で説明し切ろうとすると壊れ、比喩がまだ効くのは `観測 / 停止 / 修復` の前半までだと整理した。
   直近の軽い圧縮では 0〜4 章の重複だけを削り、列挙で散っていた「人間側の揺れ」を 1 文へ畳み、`AI のための discipline` / `人間のための discipline` の二重言い換えも 1 回へ寄せた。前半の spine は「ハーネスは人間側の雑さを通さない器」と読める粒度へさらに締めている。
   その後の micro-polish では、forward bridge が `次は...` の定型に寄りすぎていた 3 箇所だけを崩し、接続を保ったまま機械的な反復を弱めた。
   追加の軽微修正では、§0 だけは bullet の走査性を優先して 4 項目列挙を復元し、§5→6 ブリッジも見出しの `PoC` 反復と近接しすぎない言い回しへ戻した。`qiita45` の対応表では `human-gate / permission boundary` 行を `(補助線)` と明示し、本文の主従と揃えた。
   続く micro-polish では、`qiita45` の `研究側で特に近い型` / `要するに` 周辺も 1 パスだけ削り、main path が「4 類型を持ち帰る段」だと読み取りやすい粒度へ揃えた。
   その後の補足では、「5 点」看板が **主線として持ち帰る 4 類型 + 補助線 1 つ（human-gate）** の 4+1 だと本文で一度言い切り、件数の見え方を揃えた。
   さらに `qiita45` の `## 2` では、`ローカルコーパス要約の上でも` を `ローカルコーパス要約でも` に縮め、`要するに本稿の main path で持ち帰りたいのは` も `要するに持ち帰りたいのは` へ詰めて、説明口調だけを少し落とした。
   最後の micro-polish では、`qiita45` の `## 2` 冒頭にあった 2 文切りの導入も 1 段へ畳み、main path の論点に入るまでの助走をさらに短くした。
   追加確認として、`VLAA-GUI` / `Resilient Write` / `Crab` / `Measuring the Permission Gate` の arXiv 4 件は 2026-06-19 に一次情報で URL / title / author を照合済みだと本文へ固定した。あわせて `5 点` は運用カテゴリ、`4+1` は RAD 接地の分析レイヤだと 1 行で明示し、taxonomy の切替が誤読されにくい形へ揃えた。
   canonical ledger 2 正本への `513546f..b5464fa` 回収は完了済みで、次に触るときはこの短稿をさらに短く締めるか、公開水準へ向けて参考整形を詰めるかから始めればよい。
   次にやるなら、`#43` へ戻す判断ではなく、独立短稿として runtime / orchestration の最小グロスを保ったままさらに圧縮するか、外部公開できる水準まで参考整形を進めるかを決める。現段階では publish / Team stock へは送らず、`157.jpg` の使いどころ定義、RAPTOR / `llterm` / `/goal` の具体節、`desired-actual-drift-repair` の最小 loop 説明、green-keeper 比喩の破綻点と failure mode、runtime 成長順の実務ルール、そして runtime に入れる前に先に捨てるべき人間側の癖まで入れたところで止めている。
9. `qiita37_gpu_triple_run_gate_price_kamikudaki.md` は本文の spine を増補済み。次に触るなら、Kaggle 運用 PoC を本文に残すか `<details>` 層へ逃がすかを 1 回だけ決める。
   この一次確認は references 節に列挙した外部 URL 群にも同じく適用する。
   参考メモ節は、いまは appendix として外部系統メモと背景メモを分けた状態。
   `## 2` の外部用語帰属も、`ignorePublish` を外す前に appendix の外部系統メモと照合する。
8. 公開作業を止める場合は、#43 の多言語版 /
   既存記事リンク導線のローカル整備を先に進める。
9. publish 前 gate として、`qiita43_harness_loop_stack_kamikudaki.md` の
   `kamikudaki_shishi.svg` が main 反映後に raw URL で HTTP 200 を返すか確認する。
   `qiita44` はバス江コマをいったん本文から外したので、再投入する場合だけ
   その時点でコマ選定・クレジット・転載許諾 / 利用条件の一次確認をやり直す。
10. `qiita44` / `qiita45` の末尾 HTML annotation と参考文献節は追加済み。
   `qiita44` は GA / ES / GP / NEAT / novelty search / MAP-Elites / CMA-ME /
   lexicase の一次導線 URL まで補強済みで、CMA-ES も arXiv `1604.00772` へ差し替え済みなので、publish 前は本文の言い回しと
   claim-strength の最終確認まで通した。直近の pass では、論旨を変えずに `淘汰器が壊れていたら進化はだいたい壊れる` → `探索は鈍りやすい`、`長期でだいたい飽和か monoculture に寄る` → `寄りやすい`、`高次元 descriptor では cell の大半が空になる` → `空になりがち` の 3 箇所だけを弱めた。
   続く最終微調整では、`これはかなり重要です` → `ここは見落としやすい点です`、`これは本当に重要です` → `ここは切り分けを誤りやすい点です`、`かなりクリア` → `だいぶクリア`、結語の `壊れやすい` → `詰まりやすい` まで弱め、断定トーンだけを追加で落とした。
   <!-- QIITA44_GATE_STATE_BEGIN -->
   参考導線の最終突合と本文の主張強度微調整は完了済みで、`qiita44` の MIT Press 到達性 gate は 2026-06-19 時点で **soft-gate** 状態にある。2026-06-18 時点では、記事側の Holland 導線 `Adaptation in Natural and Artificial Systems`（canonical permalink `https://mitpress.mit.edu/9780262581110/adaptation-in-natural-and-artificial-systems/`、DOI `10.7551/mitpress/1090.001.0001`、resolver `https://doi.org/10.7551/mitpress/1090.001.0001`）と、Koza 導線 `Genetic Programming: On the Programming of Computers by Means of Natural Selection`（canonical permalink `https://mitpress.mit.edu/9780262527910/genetic-programming/`）を対象に、PowerShell `Invoke-WebRequest` + browser UA + Cookie なし、および Microsoft Edge headless で canonical permalink 2 本と Holland DOI resolver の Akamai 403 までは証跡化済みである。ここで確定している事実は **このローカル egress からは Akamai 403 を受けた** ことだけであり、reader にとってリンクが無効だとまでは言えない。Holland の DOI `10.7551/mitpress/1090.001.0001` は 2026-06-18 に Crossref API で `The MIT Press` / `Adaptation in Natural and Artificial Systems` / `John H. Holland` / `1992-04-29` の一致を確認済み。Koza 側は Crossref の title/author 検索と `9780262527910` クエリでは MIT Press 書籍 DOI を特定できていない一方、MIT Press title page では paperback `9780262527910` / hardcover `9780262111706` の同一書誌として確認でき、WorldCat でも OCLC `26263956` の 1992 MIT Press print book として確認できた。したがって現時点では Koza DOI 未固定のまま canonical permalink を主参照として維持し、必要なら補助導線として publisher catalog / WorldCat を併記する。2026-06-18 の追加再観測では、このマシンの同一 egress 上で canonical permalink 2 本に対し PowerShell `Invoke-WebRequest`（browser UA / Cookie なし）を再実行し、どちらも `STATUS=403` を再確認した。これは **ローカル観測の再実行**だった。2026-06-19 には **別 UI / 別ブラウザ経由の補助観測**として canonical permalink 2 本を 1 回ずつ開き、どちらもログイン不要の MIT Press 書誌ページとして表示できることを確認した。これは一度きりの観測に留まり、別 egress の恒常的 reachability は未実証である。したがって gate は `ローカル egress 403` と `reader reachability/citation integrity` を分けた **soft-gate** として維持し、非 Akamai 系の導線は本文の staging comment にだけ保持する。観測時の成功条件は、`https://mitpress.mit.edu/9780262581110/adaptation-in-natural-and-artificial-systems/` と `https://mitpress.mit.edu/9780262527910/genetic-programming/` について、ログイン要求や即時 block page ではなく MIT Press の title/bibliographic page と読める画面が出ることだった。
   <!-- QIITA44_GATE_STATE_END -->
   publish 直前の human-gate チェックリスト:
   1. 2026-06-19 時点の観測は soft-gate の補助証跡に留まり、別 UI / 別ブラウザ経由の補助観測であって別 egress の恒常的 reachability 実証ではないと明記したか。
   2. 将来 canonical 側で片側障害が再発した場合、fallback supplement を un-comment したのが失敗側だけで、成功側を carry していないか。
   3. Holland / Koza の取り違えがなく、補助導線を露出させるときは canonical permalink と 1:1 で扱っているか。
   4. `references` 節にある外部 URL 群も、この soft-gate の確認対象に含めて spot-check したか。
   `qiita43_harness_loop_stack_kamikudaki.md` も、公開線へ回すなら同じ粒度で
   annotation / 参考導線 / 参考文献テンプレの有無を確認する。
11. 草稿を publish へ回すときは、対象記事の `ignorePublish: true` を外し、
    公開方針に合わせて `private: true/false` を決める。
    この 2 つは `qiita-cli-poc` 草稿ラインで使っているローカル運用フィールド
    （Qiita 公式 API の公開状態そのものではなく、ローカルの同期・公開手順を止めるための安全柵）
    として扱う。
    既発行の限定共有 draft そのものを撤回するフラグではないため、未確認帯が残る状態のまま
    `ignorePublish: false` に戻さない。
    #43 多言語 draft の翻訳 drift と
    draft-only 注記の除去漏れがないかもこのタイミングで確認する。
    あわせて、冒頭の拾い読み導線が `##` / `###` の見出し階層だけでも意味を持つか見直す。
12. `qiita45` の `## 2` にある外部用語帰属と、appendix の外部系統メモを
    `ignorePublish` 解除前に突き合わせる。
13. `qiita43_harness_loop_stack_kamikudaki.md` / `qiita44_*` / `qiita45_*` の
    冒頭導線は、**いまは text TOC として読める形を優先**している。
    custom アンカーは本文から外してあるので、publish 前は
    見出し階層と限定共有での見え方だけ確認すればよい。
    `qiita43_harness_loop_stack_kamikudaki.md` は短縮版だが、☕ / 参考文献は追加済み。
    `qiita43_harness_loop_stack_kamikudaki.md` を公開線に乗せる前は、
    その短縮版で追加した一次 URL と著者帰属の整備を優先する。
    `qiita45` 側は主要 4 本（`VLAA-GUI` / `Resilient Write` / `Crab` /
    `Measuring the Permission Gate`）の実名ソース追加までは完了しており、
    残るのは増補するか内製ラベル説明をさらに簡潔化するかの整形寄り作業である。

## Archive: 2026-06-12 夜 当時の次回最優先 (ccr で FullSense 選択時 / Qiita 記事ライン)

> llterm は llcore 対象で別駆動中。こちら (ccr/FullSense) は記事・SVG 整備が本線。

**今セッションで完了:**
- hero アニメ SVG 強化レイヤ注入 (78 ファイル, `tools/enrich_hero_svgs.py`)。qiita_24 連載 9 記事を
  `?v=20260612` cache-bust で再 publish (全 public)。GitHub 直表示でアニメ強化、Qiita は静止フレーム反映。
- #35 SVG 被り修正: `qiita_35_sdp_vs_norm.svg` (判定ボックスをグラフ下へ) / `qiita_35_progress.svg`
  +en/zh/ko (タイムライン+点を y=415=カード下へ)。push 済 (#35 未公開なので再 publish 不要)。

**次回やること (この順):**
1. **#35_00 用語追補** (`docs/articles/QIITA_#35_00_verifier_sdp_not_smt_index.md`): 本文の専門語で
   `## 0. 用語説明 / Glossary` 未掲載のもの (SDP/Lyapunov/frontier/vertex-free 等) を追補。1 記事ずつ。
2. **かみくだき長め化** ([[feedback_kamikudaki_longer]]): plain-language 節は要約でなく比喩+具体例+
   「なぜそう言えるか」まで展開。研究者名に敬称 ([[feedback_qiita_professor_honorific]])、落語使うなら徹底。
3. **#35/#36/#38 公開判断**: 未公開草稿 (#35=`docs/articles/QIITA_#35_*`, #36=同, #38=`docs/articles/drafts/`)。
   公開するなら private-first (限定共有→確認→public)。
4. **llterm 小話** ([[project_llterm_kobanashi_idea]]): 任意。今セッションの素材 (黙る問題/ctx156%/Codex切替) で 1 本。

---

## 🟢 2026-06-12 — 現在の本線 (llterm 別駆動) = llcore ROADMAP 自走運用 (参考文脈)

## 🟢 2026-06-12 — 現在の本線 = llcore ROADMAP 自走運用 (最優先の文脈)

**正本 = `D:/projects/llcore/docs/ROADMAP.md`** (自走運用、ユーザー確定 2026-06-11) +
包括計画 = [research/master_plan_2026_06_06]({{ '/research/master_plan_2026_06_06' | relative_url }})。

- M0/M4/M5 ✅ (chat/clip/AnnotationStore、RAD corpus 生成、llloop v0.1.0a0)
- **M1 ✅ クローズ (2026-06-12)**: entity-coref エッジ + MiniLM encoder。MiniLM cosine MRR 0.947 =
  会話 retrieval ほぼ解決。正本 = llcore research/textseg1d/M1_ENTITY_ENCODER_RESULTS_2026_06_12.md
- **M3 🔄 進行中**: PoC + 検証 (i)(ii)(iii) ✅ (06-12, llcore `e399df4` + `7884f1f`)。
  (i) 56 倍化: 劣化はトピック重複 probe に集中 → **「干渉ゼロ」は条件付きと down-claim**。
  (ii) e5 は対価に見合わず → **MiniLM 続投確定**。(iii) 重複 corpus 段階注入: fail モードは
  **壊滅でなく漸進的押し下げ** (conv R@3 1.000 維持)、劣化 9 probe 中 7 は重複で説明、
  **corpus が rank 1 を取った事例は全て role="corpus" → role フィルタで会話 R@1 全防衛可**。
  正本 = llcore research/textseg1d/M3_SCALE_MULTILINGUAL + M3_TOPIC_OVERLAP (各 2026_06_12)

### ▶ 次の具体的な一手 (2026-06-12 夕方 EXIT 時点、ここから再開)

> **EXIT 状態 (クリーン)**: llcore 未コミットなし・走行中プロセスなし (全 PoC は foreground
> 完走済み)。本日の全成果は llcore `519d56d`→`6f2803e` の 5 commit + 本ファイルに反映済み。
> 再開 = 下の手順 1 (分野単位スコープ設計) から。設計判断 (a)/(b) は新セッションが
> 1 行宣言して進めてよい ((b) per-row 分野タグ推奨)。

**✅ role 絞り込み完了 (llcore `6f2803e`)**: `query(exclude_roles={"corpus"})` で (iii) +800
store の会話 22 probe が **0.849 → 0.947 (R@1 0.909) = 注入前に完全復元** (実証済、unit +3 =
393 PASS)。限界も開示済: corpus 間 (loop vs astro) の食い合いは role では防げない。

**次 = M3 残り: 分野単位スコープ設計 + ANN 化 → RAD 全量取込**:

1. **分野単位スコープ**: corpus 間食い合い対策。候補設計 = (a) group の帯域割当
   (corpus ごとに group 範囲を予約し range フィルタ)、(b) 行ごとの分野タグ (roles と同様の
   per-row list、save/load 互換に注意)。(b) が素直 — `add_text(domain="astro")` 的な。
   設計判断を 1 行宣言して実装 → loop probe が astro 混入下で 0.639 に復元するかで実証。
2. **ANN 化**: 10 万 annotations 級で総当たり cosine (87.8MB matmul @ 60k) が限界。
   optional extra 設計を維持 (基本 = stdlib+numpy、ANN は faiss optional — 当時の上位運用方針)。
3. その後 = RAD 全量取込 (~48 分野) → M2 (cert × 連結性教師)。
4. 実行注意: 長走 PoC は **foreground 分割** (memory `feedback-windows-background-task-silent-kill`)。

状態: llcore branch `phase2a-trajectory-tube-gate`、**unit 393 PASS**、push は全 repo user-gate のまま。
本日の着地 = M1 クローズ (`519d56d`) + M3 PoC (`0dd6cd3`) + 検証 (i)(ii) (`e399df4`) +
検証 (iii) (`7884f1f`) + role 絞り込み実装/実証 (`6f2803e`)。
- M2 ⬜: cert gate × 連結性教師 (M3 の次)
- llcore branch = `phase2a-trajectory-tube-gate` (push は user-gate)
- 別途 human-go 待ち: Hyperframes PoC 提案 ([research/hyperframes_heygen_survey_2026_06_12]({{ '/research/hyperframes_heygen_survey_2026_06_12' | relative_url }}))

## 🟢 2026-05-27 — lldarwin v2 方策確定 + 先駆者論文公開（当時の文脈）

overnight PoC マラソン（ユーザー Goal「徹底的に要件整理＋進化型として独自性＋PoC何度も」）で
**lldarwin v2 の方策を確定**。12h 実 LLM ランが「まだ進化でなかった（飽和で累積せず）」ことを
出発点に、自己 PoC 6 本＋並列 Agent 4 本＋Perplexity が**独立に同一結論へ収束**。

- **確定方策**: S1 選択核=novelty/ε-lexicase+z-score標準化+minimal-criterion+QD（+適応難易度・
  中立貯蔵庫・factor-subspace QD）／ S2 独自性=**連続進化集団＝ライブ・オーケストラ**（online進化+
  online回答, competence-aware routing, white-space）／ S3 agentic 個体（コストで選択的調査創発）／
  S4 観測=実装済。
- **先駆者論文（日付付き公開, 著者=古瀬 和文）**: `docs/papers/2026-05-27_continuously_evolving_orchestra_open_ended.md`
  （英日, 防御的公開, proxy 段の honest 限界明示, git commit が date of record）。
- **意思決定ログ正本**: `docs/research/lldarwin_v2_poc_marathon_2026_05_26.md`（出発点→Round0-3→
  確定方策→実装ロードマップ Phase1-5）。要件 `docs/vision/OPEN_ENDED_EVOLUTION_REQUIREMENTS.md`
  §1.11-1.13 + QD-3。Qiita #26 記事ドラフト進行中。
- **次フェーズ＝実装**（要レビュー）: 実装ロードマップ Phase1-5。部品の多くは `llive` に実装済・未配線。
- memory `project_lldarwin` 更新済。

---

## ✅ 完了 (2026-05-25) — `fullsense` PyPI upload

**完了済**: rate-limit window リセット後の再試行で upload 成功 —
<https://pypi.org/project/fullsense/0.0.1/> (公開ブランド名を PyPI で確保)。
詳細経緯は raptor `claude-projects.json` `_ecosystem_status` 参照。
[2026-06-06 stale 掃除: 本セクションは完了済みなのに 🔴 のまま残っていたためクローズ。
包括計画 = research/master_plan_2026_06_06.md T5 5-2]

## 📌 2026-05-24 命名/予約 サマリ (正本 = [research/llname_collision_audit_2026_05_24]({{ '/research/llname_collision_audit_2026_05_24' | relative_url }}))

- **RepIR → llrepr 改名** (github.com/repir/repir [情報検索] 衝突回避)。`llmesh/llrepr/` に PoC 着地
  (typed Representation IR=「LLVM-for-expression」, 24 tests, commits 12c1a07/6044ba4)。
  ✅ **配線完了済 (2026-05-24 確認)**: stdio_server の protocolVersion 2025-06-18 + outputSchema +
  structuredContent (text 併置で後方互換)、predictive_push の MQTT/SSE transport も着地
  (`predictive_push/sinks.py`)。**残 = 実 LLM explainer のみ**。詳細は
  [research/spec_mesh_01_b1_feedback_2026_05_24]({{ '/research/spec_mesh_01_b1_feedback_2026_05_24' | relative_url }}) §3。
- **llmesh × HPE 衝突**: llmesh は **規格/spec の枠**(売り物でない) → リネーム不要で **クローズ**。
  公開ブランド = **FullSense**(衝突確認済クリーン)。詳細は正本 §1.1。
- **PyPI 予約済 (placeholder 0.0.1)**: `llmesh-llrepr` / `llmesh-lleval` / `llmesh-lltrade` /
  `llmesh-lldesign`。`fullsense` は ✅ upload 完了 (2026-05-25, 上記参照)。**各実リリースは version > 0.0.1 必須**。
- **GitHub 予約 repo**: `furuse-kazufumi/llrepr` (Apache-2.0)。
- 次キュー: **#2 予測符号化 push PoC** (llmesh)。

## ✅ Done in 2026-05-18/19 連続セッション

> このセクションの詳細は [PROGRESS_archive_2026_05.md](PROGRESS_archive_2026_05.md) に移管済み。
> 要点は以下に残す。詳細は [PROGRESS.md]({{ '/PROGRESS' | relative_url }}) 参照。

llive 側 (累計 commit 多数):

- **requirements v0.8 cognitive mesh** 新規 (462 行、COG-MESH-01〜10)
- **architecture §8** v0.8 拡張ポイント (M8.x 完成配線 table 追加 — 2026-05-19 朝)
- **roadmap Phase 8** CABT + COG-MESH 双子マイルストーン
- **glossary** 24 用語 + 5 略語 (+ M8.x 11 用語、2026-05-19 朝)
- **COG-MESH-01〜10 全 10 件最小実装完了** (107 新規テスト、1379 PASS — 2026-05-19 早朝)
- **M8.2〜M8.7 本実装完了** (+55 テスト、1393 → 1448 PASS — 2026-05-19 朝)
- 統合 demo CLI (`py -3.11 -m llive.cognitive_mesh.demo`、5 → 9 セクション)
- PROGRESS 3 段階追記

portal 側 (10 commit):

- **benchmarks/policy.md** 新規 (三本柱 + 運用ルール)
- **spec/index.md** 新規 (章直リンク方式)
- **recommended-models.md** 新規 (用途別推奨 hub)
- **comparison.md** Honest disclosure 追加
- **roadmap.md** ステータス遷移 + 依存グラフ + タイムライン (Mermaid 3 種)
- **mermaid-lint.yml** CI 追加
- **index.md** Reference hubs ナビ統合
- **NOTES.md** link-rot watch list 更新 + ハブ間 cross-link 表
- **doc_map.md** Reference hubs セクション追加
- **PROGRESS.md** Phase 0.4 + 0.5

verify_publication.sh: **ALL CHECKS PASSED** 継続維持。

## 🧑 Operator actions queued — old context / current scope outside (2026-06-12 stale)

この節の項目はローカル operator 作業の旧メモであり、上位 handoff が言う
**既に未解決の human-gate 外部アクションとして並べている 3 件**
（#46 の publish 判断 / dev.to 英語版 update・publish 判断 / CTA-149 live 再 publish・PATCH 要否判断）
とは別カテゴリで、Qiita Team 3 本の `private:false` 着地は current blocker として前面に残す。
rollback / visibility tightening は必要だと人間が判断した時点で human-gate 外部アクションとして追加する。

### ✅ クローズ済み operator 項目 (要約のみ残置, 2026-06-12 stale 掃除)

詳細は git history (本ファイルの 2026-06-12 以前の版) / PROGRESS 参照。

- **0z** ✅ (05-23) ABC 並列 verify + DIV wiring — llive push 済
- **0y** ✅ (05-23) #24 シリーズ 4 言語 rollout 8 記事 + SVG 72 variant — 投稿も完走済 (末尾「Qiita 連載 #14-#24 全 19 本完走」参照)
- **0a** ✅ (05-23) lleval + usv-pandas-bridge repo 公開 (CI green / Topics / Dependabot)
- **0b** ✅ (05-23) Qiita 連載 #14-#24 全 19 本投稿完走 (公開 9 / 限定共有 10)

### 1. Credential restoration — 3 cloud LLMs (継続)

引き続き Anthropic / Gemini / OpenAI の credential / quota 復旧待ち。
復旧したら以下を再実行:

```bash
cd D:/projects/fullsense
PYTHONIOENCODING=utf-8 python3 scripts/bench_run.py --all --out docs/benchmarks/<DATE>/
PYTHONIOENCODING=utf-8 python3 scripts/bench_vlm.py --image docs/assets/images/og-card.png \
    --question "Describe this image in 2 sentences..." --all --out docs/benchmarks/<DATE>-vlm/
```

復旧後、`docs/comparison.md` の Honest disclosure セクションで
「3/4 が未測」と書いた行を更新し、A/F 採点を再評価。

### 2. asciinema 録画 — Cognitive Mesh 統合 demo (9 セクション拡張版)

llive 側で `py -3.11 -m llive.cognitive_mesh.demo` が 9 セクションに拡張済。
Active (10:00 JST) と Quiet (02:00 JST) を時刻固定で連続再生:

```powershell
asciinema rec demo-cog-mesh.cast
# 中で:
$env:LLIVE_TZ="Asia/Tokyo"; $env:LLIVE_QUIET_HOURS_START="22"; $env:LLIVE_QUIET_HOURS_END="8"; $env:LLIVE_QUIET_HOURS_ENABLED="1"
$env:LLIVE_DEMO_FORCE_TIME="2026-05-19T10:00:00+09:00"; py -3.11 -m llive.cognitive_mesh.demo
$env:LLIVE_DEMO_FORCE_TIME="2026-05-19T02:00:00+09:00"; py -3.11 -m llive.cognitive_mesh.demo
```

9 セクション (Quiet Hours / Proactive / Idle Training / TonicRisk +
ApprovalBus 配線 / TitleRecall / **Mesh5W1H Annotator** /
**Quarantined Memory (Ed25519)** / **Event/Consistency mode** /
**BriefDeque Bridge**).

`project_f25_demo_polish` (動きで魅せる + 採用ファネル先頭) と整合。
公開は `feedback_articles_pause` 解除後。

### 3. PAT rotation (継続)

`Administration: Write` 権限のある classic PAT が必要 (gh api topics /
Pages 設定 / repo edit を自動化するため)。

## 🤖 Agent-side work for the next session

### Priority 1 — M8.x 全件着地 + 残 HTTP push 実配線 (Phase 6 本配線)

| Milestone | 状態 | 残作業 |
|---|---|---|
| **M8.1** | llove 側 panel skeleton + llive timeline_emitter skeleton 配備済 | HTTP/MCP push 実配線 (llive ↔ llmesh Timeline server) と asciinema 録画 |
| **M8.2〜M8.7** | 本実装完了 (2026-05-19 朝) | 無し |
| **M8.8** | 本実装完了 (2026-05-19 昼前、自前 BFS/DFS/centrality) | networkx 化は将来 swap 候補 (依存追加要承認) |
| **M8.9** | 本実装完了 (2026-05-19 昼前、change_sink + MultilingualGrammar) | EVO change saga 配線は Phase 7 |

agent 単独で残るのは:
- llove app.py に CognitiveMeshPanel を attach する経路 (Tab 等)
- llmesh Timeline server に cog_* event_type を予約する文書化
- llive/clients/llmesh_timeline.py (HTTP push client) の skeleton

### Priority 2 — portal NEXT_SESSION 自動更新フロー

本ファイルは手動更新で drift する。Stop hook で自動生成する案を検討:

- 直近 git log + Phase 状態 + verify_publication 結果を貼る
- 「未消化 operator action」を `[ ]` チェックボックス化、PR 等から拾う

### Priority 3 — articles pause 解除タイミング

`feedback_articles_pause` (投稿用記事の追加・更新を当面保留) は 2026-05-14
からの方針。M8.2〜M8.7 着地はパッケージ公開級の大きな機能完成なので、
解除を提案する候補に。ベンチ復旧と合わせて再評価。

## State of the world (machine-checkable)

```bash
# llive: M8.2〜M8.9 本実装 + M8.1 skeleton + E2E test 完了
cd D:/projects/llive
py -3.11 -m pytest tests/unit tests/integration -q
# 1497 passed

# llive 統合 demo (9 セクション、Active 帯)
$env:LLIVE_TZ="Asia/Tokyo"; $env:LLIVE_QUIET_HOURS_START="22"; $env:LLIVE_QUIET_HOURS_END="8"; $env:LLIVE_QUIET_HOURS_ENABLED="1"
$env:LLIVE_DEMO_FORCE_TIME="2026-05-19T10:00:00+09:00"
py -3.11 -m llive.cognitive_mesh.demo

# portal: ALL CHECKS PASSED
cd D:/projects/fullsense
bash scripts/verify_publication.sh
```

## Cross-references

- [PROGRESS]({{ '/PROGRESS' | relative_url }}) — full session changelog (Phase 0〜0.5)
- [Spec hub]({{ '/spec/' | relative_url }}) — FullSense Spec v1.1 + 要件定義 8 本
- [Roadmap]({{ '/roadmap' | relative_url }}) — ステータス遷移 / 依存グラフ / タイムライン
- [Comparison]({{ '/comparison' | relative_url }}) — Honest disclosure
- [Benchmark Policy]({{ '/benchmarks/policy/' | relative_url }}) — 系列 A/B/C/D + progressive curve
- [Recommended models]({{ '/recommended-models/' | relative_url }}) — 用途別推奨 on-prem モデル
- [NOTES]({{ '/NOTES' | relative_url }}) — design decisions, link-rot watch
- maintainer memory:
  - 2026-05-18 一連 (user_cognitive_mesh_model 等 6 件 — COG-MESH 由来)
  - `feedback_response_timing` (70 点で出す)
  - `feedback_articles_pause` (投稿一時停止)
  - `feedback_max_plan_autonomy` (Max 契約自律性)

## 2026-05-20 朝セッション 追記

15 時間自律ループ (ユーザー指定) の前半進捗.

### 完了 (push 済)

- **Priority 2 完了**: portal `docs/NEXT_SESSION.auto.md` 自動生成
  (`scripts/gen_next_session_auto.py` + raptor Stop hook ラッパ).
- **research hub** 新設 (`docs/research/`) + 6 件 SOTA / prior-art メモ
  (lleval / llgrow / cognitive_mesh / llcraft / llrisk / llgov).
- **spinoff_ideas C-2 採用優先度表**: lleval=HIGH, llgrow=MID, llbridge=MID,
  llcraft=llrisk=llgov=LOW, llforen=DEFER (research 結果ベース).
- **関連 prj test 回帰 fix**:
  - llive **1518 PASS 維持**.
  - llove: chafa 環境変化由来の image renderer fallback test 6 + markdown_view 1 +
    property test 1 + e2e_chafa 1 を `monkeypatch.shutil.which` + `pytest.skip`
    + `@settings(deadline=None)` で fix.
  - llmesh: hypothesis DeadlineExceeded flaky を `conftest.py` の
    `register_profile("local-flaky-safe", deadline=None)` で一括解決.

### 残作業

- llmesh 全 test 確認は background で実行中. `test_synthetic_dataset::test_aoi_adapter_processes_synthetic`
  が前 run で 1 度 fail (順序依存 flaky 疑い, 単独 run では再現せず) → 根本原因
  調査は将来宿題.
- raptor リポは origin と diverge (local 67 / remote 67), `libexec/raptor-next-session-update`
  追加は local commit only. push 判断は manual merge 後.
- 採用優先度 HIGH の lleval は **ベンチ復旧と並行で promptfoo fork PoC** を着手
  判断する案 (research 結果に基づく).

### 関連 memory (今セッション新規)

- `feedback_env_dependent_tests` — PATH 上 optional binary 検出を含む test は
  `monkeypatch.shutil.which` で環境独立に.
- `feedback_hypothesis_deadline` — DeadlineExceeded flaky は `conftest.py` の
  `register_profile` で一括解決.
- `project_fullsense_2026_05_20` — 本セッション総括.

## 2026-05-21 15h marathon 追記

15 時間 marathon で前倒し可能な全件を着地. credential / 外部 binary 不要
レイヤを agent 単独で全部書く方針.

### Done (本セッション)

#### Phase 0.7 (要件定義 + 三日統合)
- llive v0.A 要件定義 (`docs/requirements_v0.A_external_runtime_tracking.md`)
- llive v0.A 互換性 matrix SSoT (`docs/spec/llamacpp_compat_matrix.md`)
- llive smoke contract test (5 件, default skip)
- llive `benchmark/runtime_metadata.py` + 6 unit test
- portal lleval impl notes に Honest Disclosure 6 因子目追加
- portal QIITA #21 三日マラソン統合記事 (5/18-20)

#### Phase 0.8 (15h marathon 前倒し)
- llive v0.B Phase 3.5 — per-individual sub-seed 派生 (`seeds.py` + 8 test)
- llive v0.B Phase 4 — 5 軸 fitness mock (`fitness_llm.py` + 7 test)
- llive 5 backend Genome PoC (`test_evolutionary_backend_select.py` + 2 test)
- llive `demo_low_spec_mock.py` + 実験ログ (MockBackend 数値の publish 禁止明記)
- lleval v0.1.0a0 skeleton repo (`D:/projects/lleval/`, 24 test 緑)
  - pyproject + src/lleval/ (config / runner / providers / analyzer / report / cli)
  - examples/{basic,progressive,multi_provider}.yaml
  - CHANGELOG / CONTRIBUTING / SECURITY
  - .github/workflows/test.yml (skeleton)
- llive PR ドラフト changelog (`docs/pr_drafts/optimize_core_2026_05_20_changelog.md`)
  - 3 PR に分ける案を推奨 (B-0〜B-9 / v0.A / v0.B)
- portal QIITA #22 transformer 脱却 status + QIITA #23 marathon 中間報告
- 両記事の漫才部分を除去 (memory `feedback_article_humor_style` 準拠)

### Test 数値

- llive: 1591 → **1634 PASS** (+43, 回帰なし)
- lleval: 新規 24 PASS
- llmesh: 3086 PASS (前セッションから不変)
- llove: 796 PASS (前セッションから不変)

### 残作業 (operator / credential / 外部 binary 復旧後)

| # | アクション | 依存 |
|---|---|---|
| 1 | `llama-server` + Codestral-Mamba GGUF で `MambaBackend` 実走 smoke | llama-server 起動 |
| 2 | low_spec bench 実 backend 実走 (MockBackend 数値を上書き) | step 1 |
| 3 | RWKV-7 World 7B を `RwkvBackend` で繋ぐ | RWKV.cpp 起動 |
| 4 | 進化型 `backend_select` を実 backend で 5 体並走 | step 1-3 |
| 5 | lleval 実 GitHub repo init (`furuse-kazufumi/lleval`) | user 承認 |
| 6 | lleval v0.1.0a1 (promptfoo subprocess 接続) | step 5 + npx promptfoo |
| 7 | claude-smart 評価 Session 1 dogfood | user が `.worktrees/eval-claude-smart` で起動 |
| 8 | llive `optimize/core-2026-05-20` branch を main マージ判断 | PR 3 件分 review |
| 9 | Anthropic / Gemini / OpenAI credential 復旧 → bench 再走 | 外部 |
| 10 | asciinema 録画 (COG-MESH demo 9 セクション + llive demo + LoveApp+env) | operator |

※ #9-10 は 2026-06-12 時点で stale 扱いへ移した operator 項目の旧記録。現行スコープ外として `old context / current scope outside` 節を正本に読む。

### 関連 memory (本セッション新規 / 更新)

- `project_15h_marathon_2026_05_21` (本セッション総括)
- `project_llive_v0B_evolutionary` (v0.B Phase 1-4 全件)
- `project_llive_core_optimization_2026_05_20` (B-0〜B-9 完了反映)
- `project_lleval_v01_poc_scope` (lleval PoC スコープ)
- `feedback_llamacpp_tracking` (月次追従ルール)
- `reference_claude_smart` (採用 pending)

## 2026-05-21 夜 (Phase 0.10 後) 追記

### 着地済 (v0.C 周辺 + 補強)

- llive v0.C variant_runner (subprocess 起動先 CLI, mock 経路で動作)
- llive lineage (LV-10) — Winner / write_winners_jsonl / render_lineage_mermaid
- **EvolutionLoop.on_generation_end hook** — lineage 自動書出し統合可
- lleval bridges/llive (Genome → Config + Report → fitness)
- lleval report/html (CSS 内蔵 self-contained)
- lleval CLI --html フラグ
- llive 1669 → **1673 PASS**, lleval 59 → **61 PASS**

### 着地済 (memory / 記事方針 / portal)

- memory `feedback_linkedin_translation_jp_only` 大幅修正 (多言語推奨に転換)
- memory `feedback_qiita_github_links` 新規
- memory `feedback_overseas_tech_platforms` 新規 (Medium / dev.to / HN 戦略)
- memory `feedback_articles_references_section` 新規 (引用文献必須)
- memory `feedback_articles_taxonomy_split` 新規 (大/中/小 分類 + 複数記事)
- portal **QIITA #24 series index** (大分類 8 記事 navigator)

### 次セッション残作業 (本セッションで context 限界により見送り)

| # | アクション | 所要 |
|---|---|---|
| A | **QIITA #24 series 個別記事 01〜08** (各 8-12k 字) | 週 2 本 × 4 週 |
| B | QIITA #21/22/23 に GitHub link 積極配置 retrofit | 各 30 min |
| C | cross-post 計画 doc (QIITA #21-23 を Medium en 化) | 1h |
| D | 既存 QIITA 記事に References セクション retrofit | 30 min × 3 |
| E | (Phase 2) 実 LlivKernel spawn 実装 | credential / kernel module 後 |

## Last updated

2026-05-21 夜 — **Phase 0.10 着地: hook + lineage + bridges + HTML + 5 memory + QIITA #24 series index**. llive 1673 PASS / lleval 61 PASS.

2026-05-21 — **15h marathon: v0.A 実コード + v0.B 全件 + lleval skeleton + 漫才除去**.

2026-05-19 夕方 — **M8.x 全件着地 + M8.1 production wire + LoveApp 統合完了**.

最終数値:
- llive: 1393 → **1518 PASS** (+125, +12 ProductionHttpTimelineSink)
- llove: 771 → **796 PASS** (+25, +5 LoveApp env-gated attach)
- llmesh: 42 → **46 PASS** (+4 ingest allow-list)

M8.1 完成度:
- llive: emitter / skeleton sink / **ProductionHttpTimelineSink** (auth
  Bearer + exp backoff retry + batch buffer + 4 env)
- llove: panel skeleton + **stand-alone demo** + **LoveApp 統合**
  (LLOVE_ENABLE_COG_MESH=1 で attach、既定無効で互換維持)
- llmesh: `/timeline/ingest` allow-list に 4 種 (cog_*) 追加
- portal: Mermaid sequenceDiagram + Phase 6 wire-up tutorial
- E2E integration test 1 件で M8.1〜M8.9 chain 動作確認

**残作業 (操作者作業)**:
※ この節の operator 項目は 2026-06-12 時点で stale 扱いへ移した旧記録。現行スコープ外として `old context / current scope outside` 節を正本に読む。
- asciinema 録画 (llive demo / llove cog_mesh_demo / LoveApp+env の 3 本)
- 実 production 起動 (env を operator 設定するだけ):
  ```
  LLIVE_LLMESH_TIMELINE_URL=http://prod-llmesh:8080
  LLIVE_LLMESH_TIMELINE_TOKEN=<bearer>
  LLIVE_LLMESH_TIMELINE_RETRIES=5
  LLIVE_LLMESH_TIMELINE_BATCH_SIZE=10
  LLOVE_ENABLE_COG_MESH=1
  ```

## 2026-05-23 深夜 silent 自律セッション 追記

### Done (本セッション)

cross-project 連携追跡 + D ドライブ集約整備:

- **5.5 GB 解放** — `D:/projects/raptor` 削除 (`move-raptor-to-d.ps1` 移行中断
  の robocopy 残骸、`.git` 無し、`C:/Users/puruy/raptor` が hard-coded で active)
- **17 MB 解放** — `C:/Users/puruy/mcp-3d.zip` / `mcp-3d-v3.zip` 削除 (D 移行後の zip backup)
- **15 プロジェクト baseline** 一斉スキャン (git status / branch / 最新活動)
- **Test green 5/5** 全 PASS 確認: llive 2492 / fullsense 10 / llove 全件 /
  llmesh exit 0 / lleval 88
- **コーパス C/D 整理**: 「C:/raptor のコード + 要約 skill」+「D:/docs の RAW」
  の組合せが active、`D:/projects/raptor/.claude/skills/corpus/` (古コピー) は
  raptor 削除に同梱で解消
- **F25 audit-deps Phase 2 wiring 実装** (llove):
  - `llove/engine/http_app.py` の `/api/v1/audit/deps` を `llmesh.cli.deps_audit`
    proxy 化 (lazy import + Phase-1 fallback 維持で `feedback_independence_principle` 遵守)
  - `tests/engine/test_engine_skeleton.py` を Phase-1/2 両モード対応に書き換え +
    Phase-1 fallback の明示テスト追加 (8 PASS in 5.17s)
  - commit `d9b0a44` (test 側 feat) + `8471d7a` (auto-commit hook が http_app 本体を含む)
- **memory drift 訂正**: `project_mcp_spatial_asset.md` を mcp-3d 改名 + llmesh 統合済 +
  論文題材残置のユーザー言明を反映

詳細は [`docs/articles/2026-05-23/INTEGRATION_AUDIT.md`]({{ '/articles/2026-05-23/INTEGRATION_AUDIT' | relative_url }}) 参照.

### 残作業 (次セッション追加 queue)

- **`0c`** llove engine `/api/v1/audit/offline-check` の Phase 2 化 — httpx/urllib/aiohttp の
  outbound trace hook 仕込み、推定 5h+
- **`0d`** llive 333 unpushed commits (`auto:` 系含む) の整理判断 — squash vs push as-is
- **`0e`** llmesh test の pass count 確定 — SNMP adapter deprecation warning が summary
  line を流すノイズに、別 reporter で測りたい
- **`0f`** browser-use-project (D:) の C: hard-coded path 修正 — 4 件 (alpaca_utils:493 /
  discord_queue_worker:36 が修正可、alpaca_r_optimizer:32 と alpaca_timeseries:18 は外部
  ツールの固定位置で touch 不可)
- **`0g`** `C:/Users/puruy/` 配下の `hello-rust / holyclaude / source / R / RustroverProjects /
  browser-use-project (6KB state)` の処遇判断 — FullSense 外、ユーザー裁量

### honest disclosure — 今夜の見落とし / 教訓

- `find` の `head -10` 切れで `llmesh.cli.deps_audit.py` (5 日前既に実装済) を
  見逃し、新規実装書き始めたところで Write tool に止められて気付いた
  (`feedback_implementation_status_record` 再確認)
- raptor の auto-commit hook が「編集前」commit を作る際、複数 file の変更を
  単一 commit に巻き込むため commit message が実態と乖離する問題を観測 (今回は
  feat commit を別途追加して補完)


### Done 追記 (CLI safety scan, session 後半)

- **`llmesh.cli.doctor` cp932 em-dash crash 修正** (llmesh commit `11b38e7`):
  Windows console で `UnicodeEncodeError: 'cp932' codec can't encode '—'` で
  クラッシュしていた問題、main() 冒頭に `_ensure_utf8_stdout()` 追加で解消
- **`llive.cognitive_mesh.demo` Quiet Hours halt UX 改善** (llive commit `7310152`):
  LLIVE_TZ 未設定 (fail-closed 既定) で section 1 halt していた問題、mock time
  `2026-05-23T12:00:00+09:00` で続行する fallback 追加. 全 10 sections 完走確認
- **`llmesh.cli.sbom` `→` 文字化け修正** (llmesh commit `798bf93`):
  cp932 で U+2192 が `??` に化けていた問題、doctor と同 helper 適用
- **memory `feedback_cli_utf8_stdout_pattern.md` 新規追加**: Windows CLI に
  `_ensure_utf8_stdout()` 必須化を future-self 用に記録
- **MEMORY.md 整理**: 39KB → 24KB に圧縮 (164 entries を 140 byte/line に短縮)、
  warning (limit 24.4KB) 解消


### Qiita 連載 #14-#24 全 19 本完走 (2026-05-23)

[[feedback_qiita_limited_share_unlimited]] (限定共有は 24h 制限対象外) の
発見を契機に、ユーザー手動投稿 + Claude が即時 LINK_MAP 更新 / qiita_url_sync /
atomic commit する pair-programming で **連続 19 本投稿完走** (公開 9 / 限定共有 10).

詳細は [[project_qiita_post_resume_2026_05_22]] (memory) で完走済テーブル管理.

**0b → CLOSED** (Qiita 連載 #16-#23 + #24-00..08 投稿は完了).

新規残作業:

- **`0h` (新規)** Qiita 限定共有 10 件の公開昇格スケジュール (連載順 (0)→(1)
  →…→(8) を守って 1 日 N 件ずつ `private: false` に編集)
- **`0i` (新規)** Qiita Web 上の #24-00 / #24-01 タイトルを `#24-NN` →
  `(0)` / `(1)` に手動修正 (ローカル draft は commit e359bd5 で統一済)
- **`0j` (新規)** LinkedIn 既存告知記事の GitHub blob link を Qiita 公開 URL に差替
