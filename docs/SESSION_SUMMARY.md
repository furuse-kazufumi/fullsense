# Session Summary

> 手動更新: context limit 到達前の再開用スナップショット
> 注意: 通常は Stop hook により自動生成・上書きされうる

- 最終更新: 2026-06-19
- プロジェクト: `D:/projects/fullsense`
- ブランチ: `main`

## 現況

- 今回の作業は **Qiita 草稿 / poster スクリプト / handoff 文書の整合調整**に加え、**llterm 記事シードのスクリーニング**。本命長編は種 #6、単独中編候補は種 #1 と判断した。
- 文書バッチの commit 記録ルール: `c37d084` までは連続列挙、それ以降は肥大化回避のため **範囲表記 + マイルストーン**で記録する。
- handoff 台帳は構造上、**最新 1 件の handoff commit を未反映のまま残すのが正常状態**である。自己増殖を避けるため、backfill は **実質的な handoff 更新を伴う commit に便乗してのみ**行い、台帳追記だけの単独 commit は原則作らない。例外標本は `a0b793a` / `6d9854d` / `c16a69b` / `e150ee4` / `ed1e841` で、いずれも standalone backfill debt の過去標本として扱う。以後は同型の commit を増やさず、cleanup が必要なら 1 行 note を積み増すのではなく、次の実質的 handoff 更新か別 human-gate 判断の中で 1 回で畳む。
- 2026-06-19 のユーザー判断で、この 5 件の例外標本は cleanup 対象として掘り返さず、履歴上の標本として保持する方針に固定した。以後は再発防止だけを維持し、同型の standalone backfill commit を増やさない。
- 2026-06-18 の Team stock POST では、`private:true` を意図した 3 本が API GET ではすべて `private:false` で着地した。さらに 2026-06-19 12:41:22 +09:00 の未認証 HTML GET では 3 本とも Team URL が `/login?redirect_to=...` へ `302` したが、これは Team サブドメイン全体の auth gate でも説明できる。したがって **team-only と positively 確認できるまでは過剰露出の疑いを優先**し、`private:false` の意味づけは一次情報待ちとする。なお `https://qiita.com/furuse-kazufumi/items/<id>` の direct probe は 3 本とも `404` だったが、これは Team scope item なら team-only / 過剰露出のどちらでも起こりうるため、over-exposure 判定の弁別力は無い。今回 probe した 3 本について、同時点で public 側の対応記事を直URLでは確認できなかった、という記録に留める。
- 同じ API GET では `group.url_name: general` / `group.private:false` / `organization_url_name:null` も 3 本とも一致した。2026-06-18 の poster payload では `group_url_name` を送っていなかったため、implicit General sharing が起きた可能性を current 仮説として追う。ただしこれは root-cause 仮説であって、team-only の証明でも否定でもない。local source にはこの観測値を resend default として固定しない。2026-06-19 の hardening では、既存 item の PATCH でも `group_url_name` を既定送信しないことを `tests/test_qiita_frontmatter.py` で固定し、観測された `general` を通常更新で再宣言しない状態へ揃えた（2026-06-19 再実行で `93 passed`）。その反面、**current blocker の 3 本を狭い共有先へ寄せ直す remediation は、このツールの既定 PATCH 経路だけでは実施できない**。是正が必要なら Team UI か、`id` あり更新でも `group_url_name` を明示送信できる別改修が要る。
- 2026-06-19 の継続作業で、その「別改修」をローカル実装した。`tools/qiita_team_post.py` は **既定 PATCH を維持したまま** `--patch-group-url-name` を付けたときだけ `group_url_name` を再送できる。これは **共有先 (`group_url_name`) を寄せ直すための opt-in 経路**であり、`private` 範囲の tightening そのものではない。dry-run でも `private` は frontmatter 値を再送する旨を明示する。現在の 3 本は source が `private:false` のため、この経路だけでは露出疑いを縮めず、`private:true` へ直す別アクションが要る
- Qiita API docs の `PATCH /api/v2/items/:item_id` に `group_url_name` 記載がある**可能性**はあるが、この点自体は現時点で一次未確認である。したがって現状ここで確定しているのは、ローカル実装として resend 経路を持たせたことだけであり、**既共有 item に対し、この PATCH が実際に共有先や可視範囲を締め直す効果を持つかは一次未確認**のまま扱う
- したがって current blocker の次アクション候補は `Team UI` と `human-gate 後の opt-in PATCH` の二択まで狭まったが、後者を「visibility 是正が実証済み」とは扱わない。通常更新での非再送は壊さず、frontmatter に concrete target が無い remediation PATCH は fail-closed で止める
- 2026-06-19 のローカル再確認では、Team stock 3 本の source frontmatter にはまだ `group_url_name` が無く、`py -3.11 tools/qiita_team_post.py dry-run <file> --patch-group-url-name` は 3 本とも `PATCH_GROUP_URL_NAME_BLOCK` で停止した。従って opt-in PATCH 経路は実装済みだが、**human が concrete target を決めて source に入れるまでは実行不能**である
- 外部 remediation の優先順位は、現時点では **Team UI first / opt-in PATCH second** で置くのが妥当である。理由は、opt-in PATCH はローカル実装と fail-closed guard までは確認済みでも、既共有 item に対する締め直し効果が一次未確認だからである。次の human-gate では、まず Team UI で intended share target / private state を確認・是正できるかを見て、UI で表現できない場合に限って concrete `group_url_name` を source に入れた opt-in PATCH を検討する
- ここで言う `visibility blocker` / `intended share target` / `private state` は **project-local shorthand** であり、Qiita 公式 API の用語としては扱わない。API 仕様として未確認の箇所は、引き続き一次未確認のまま明示する
- 次の human-gate に向けたローカル準備として、`team_stock_publish_plan.md` に **Team UI remediation checklist** も追加した。目的は UI 操作そのものではなく、変更前後の Team API GET / Team UI / 未認証 HTML GET / direct probe / source frontmatter の evidence capture と、`team_stock_queue.md` の **POST 後の記録欄 `note`** を正本にした反映順を固定することである。containment は diagnosis より前に置く
- 同日の追加 hardening として、`tools/qiita_team_post.py` の `dry-run` / `post` は **位置引数を 1 件だけ許可**するようになった。複数 article path を渡した場合は `BLOCKED: exactly one file expected, got N` で fail-closed に止め、対象記事の取り違えを黙殺しない。`tests/test_qiita_frontmatter.py` のフル再実行は `93 passed`。
- この段階で `general` を local source へ焼き戻すことはしない。理由は、観測値を resend default に固定しないという current rule を保つためである
- 2026-06-19 の最新ローカル到達点として、`#37` short companion の public PATCH は完了済みで、`tests/test_qiita_frontmatter.py` は再実行で `93 passed` だった。当該 docs / tests / tools 更新は commit `a29f8e3` と `196af76` へ反映済みで、現在の worktree は clean である。新セッションの再開点は `#37` ではなく、**Qiita Team 3 本の visibility 問題を current blocker としてどう潰すか**に一本化される。
- handoff 系 docs のテスト件数は、今回の更新で **`76 passed` → `93 passed`** へ同期した。`docs/articles/2026-05-23/INTEGRATION_AUDIT.md` にある `88 passed` は別文脈の過去監査記録であり、今回の同期対象には含めていない
- 2026-06-19 に `tests/test_qiita_frontmatter.py` へ `qiita_team_post.py` の回帰も追加し、`real_id` の nullish fallback、frontmatter `private: false` の文字列パース経路、そして **空 `private:` は default=True へ倒す**修正まで固定した。したがって上記の `private:false` incident は、少なくとも現在の Team poster 実装では再現しない層のバグとして切り分けられるが、だからといって可視範囲の疑いが解消したとは扱わない。
- さらに同日、Team poster の `ignorePublish` gate も fail-closed 化し、`dry-run` でも不正値や key typo を exit 非 0 で返すようにした。`ignorePublish:true` の source は Team poster でも `--force-ignore-publish` 無しでは送れない。
- git push は local-first 運用のため未実施のまま据え置いており、human-gate を要する外部アクション集合には数えない。新規記事の新規 publish は **未実施**だが、Qiita Team stock 3 本の POST は 2026-06-18 に実施済みで、item id は `6f67e54e538c10b8f1c3` / `b35b429dc6dc1fde207a` / `6fe79ab04443f7654eca` である。test については**この差分では未実施**で、前バッチで追加した frontmatter 回帰テストとは切り分ける。既存 public Qiita item `2622da17495d61480fa2` のタイトル修正 PATCH と `bf1cfe3b4f40b87f068d` の redirect 本文 PATCH は実施済み。
- Team 向けの難所 stock として、`team_stock_semantic_governance.md` / `team_stock_llm_wiki_anti_circulation.md` / `team_stock_ctx2549_postmortem.md` を local draft として追加し、`tools/qiita_team_post.py dry-run` を経て 2026-06-18 に Team POST まで完了した。投稿待ち一覧と POST 後の記録欄の正本は `docs/articles/2026-06-18/team_stock_queue.md`、公開順・human-gate 条件・rollback 注意の正本は `docs/articles/2026-06-18/team_stock_publish_plan.md`。2026-06-19 時点の Team poster は `ignorePublish:true` も読み、`--force-ignore-publish` 無しでは fail-closed で停止する。
- Team stock 正本 2 枚には preflight runbook / 実行コマンド / rollback notes / POST 後の記録欄まで追加済み。通常 POST はその 2 枚で回せるが、rollback 実施時のみ handoff にも 1 行転記する。
- 2026-06-18 の human-gate 回答「3本すべて POSTする」に従い、推奨順どおり `team_stock_semantic_governance.md` → `team_stock_llm_wiki_anti_circulation.md` → `team_stock_ctx2549_postmortem.md` を Qiita Team `fullsense` へ POST した。返却 id / URL は queue 正本へ記録済みで、local draft 3 本の frontmatter にも `id:` を書き戻し、サーバ実体に合わせて `private:false` へ更新した。2026-06-19 12:41:22 +09:00 の未認証 HTML GET は 3 本とも Team Login redirect だったが、これだけで team-only と断定しない。
- Team stock 3 本は source article と大筋整合していることを spot-check 済み。対応は `team_stock_semantic_governance.md` / `team_stock_llm_wiki_anti_circulation.md` = #43、`team_stock_ctx2549_postmortem.md` = #46。公開前の読みやすさだけ先に上げるため、3 本とも冒頭へ `前提 / 流れ / ゴール` の 3 点ボックスを追加した。
- さらに 3 本とも `この記事で話さないこと` を足し、難所の切り出し範囲を local draft の段階で固定した。
- さらに source anchor も明記し、#43 `2-2. loop engineering にもセキュリティの顔がある` / #43 `3-2. LLM Wiki — 「育つ知識」のパターン` / #46 `2. ターン境界と緊急割り込みは、最初から別物として設計する / 3. ctx 2549% は「AI が太った」のではなく、計測が壊れていた / 6. テストも「たまたま緑」を疑う` のどこから切り出したかを queue で追えるようにした。
- local draft 側の `この草稿の位置づけ` / `source` でも、#43 `3-2. LLM Wiki — 「育つ知識」のパターン` と #46 `2 / 3 / 6` の実見出し粒度まで揃え、queue 正本と同じ anchor で辿れる状態にした。
- さらに後続の整合確認で、`team_stock_queue.md` / `team_stock_publish_plan.md` / local source 3 本の title・source anchor・現在の frontmatter mirror（`private:false` / `public_private:false` / `ignorePublish:true` / `id:`）は相互に矛盾していないことを再確認した。`semantic_governance` は #43 `2-2`、`llm_wiki_anti_circulation` は #43 `3-2`、`ctx2549_postmortem` は #46 `2 / 3 / 6` の切り出しとして queue 記述と draft 本文が揃っている。
- `team_stock_ctx2549_postmortem.md` の `source` 行に残っていた `ctx 2549%` のネスト backtick も外し、queue 正本と同じ inner-backtick 無し表記へ揃えた。
- さらに source article 本文との一次突合も回し、`Semantic Governance` は #43 `2-2` の Verloy / Semantic Governance / fail-closed 橋渡し束、`LLM Wiki` は #43 `3-2` の 3 層 / thought circulation / safeguards 束、`ctx2549` postmortem は #46 `2 / 3 / 6` の incident 束を基準に local draft が切り出し範囲から外れていないことを spot-check 済み。
- Team stock 3 本の local draft `source` 節にも、その「切り出しの核」（Verloy / Semantic Governance / fail-closed、3 層 / thought circulation / safeguards、turn boundary / ctx2549 / block point）を明記し、anchor だけでなく論点束でも原典追跡できるようにした。
- `team_stock_semantic_governance.md` の `切り出しの核` では、原典追跡精度を優先して `意味管理` ではなく `意味論的ガバナンス（Semantic Governance）` の語へ寄せた。
- #43 companion の `qiita43_harness_loop_stack_kamikudaki.md` も full article と一次突合し、`RAPTOR / llterm / RAD` の 3 点構造、`手綱 / 輪 / 知識基盤` の圧縮軸、`AI 本体より器と回し方を設計する時代` という結論が current naming / current hedge に追従していることを確認した。
- そのうえで `qiita43_harness_loop_stack_kamikudaki.md` の `llterm` 初出には、完全版の温度感に合わせて「まだ試作段階のスケルトン」という短い alpha 留保も補った。
- `qiita45_human_ai_dev_incident_patterns.md` は publish gate に入る前の local polish として、本文と図の `human gate` / `Human Gate` 表記を `human-gate` へ統一し、`外部書き込み` も現行 handoff と同じ `外部アクション` の語へ置き換えた。主張や gate 条件は変えず、運用語だけ現行版へ揃えた。
- 続く追補で `qiita45_human_ai_dev_incident_patterns.md` の appendix / 参考節には、`VLAA-GUI` / `Resilient Write` / `Crab` / `Measuring the Permission Gate` の 4 本を近い実名ソースとして追加した。`unsupported success` / `human-gate` / `verifier` / `durable write` / `checkpoint` は引き続き FullSense / RAD 側の整理語として残しつつ、外部系統との対応先だけを本文末で辿れるようにした。
- 上記 4 本の arXiv 引用は実在確認済みで、`2604.21375` / `2604.10842` / `2604.28138` / `2604.04978` を一次情報アンカーとして handoff に明示した。
- さらに `qiita45_human_ai_dev_incident_patterns.md` の `## 2` にある honest disclosure 前置きは 1 パス圧縮し、ローカル再集計値であること・内製ラベルであること・appendix に 4 本の実名ソース対応があることだけを main path に残した。重複気味だった「appendix と対にして読む」説明は本文から削り、接地メモとしての役割だけを先頭で言い切る形へ寄せた。
- `qiita47_harness_engineering_thoughts.md` は `#43` から派生した **independent short draft** として維持する方針に決めた。`006.jpg` が「ハーネスを通した途端に AI が賢そうに見える瞬間」を担うのに対し、`157.jpg` は「本当にしつけが必要なのは AI より人類側の運用では」という反転オチを担う。草稿内では invisible comment (`<!-- draft:... -->`) で整理用メタを残し、冒頭には `前提 / 流れ / ゴール` の 3 点契約と「この短稿で話さないこと」も置いた。`honest disclosure` と「ウラオモテナシ」的な表裏同時開示の関係に加え、（本プロジェクトでの）RAPTOR / 試作段階の `llterm` / Claude Code 公式 `/goal` を引いた具体節と最小の参考導線まで追加し、参照ブロックの二重化も解消した。ここでの RAPTOR は 判断層と実行層を分けた二層 runtime、`llterm` は terminal 起点の名残を名前に残した PySide6 GUI 実装だと最小グロスも補っている。さらに `desired / actual / drift / repair` の 4 点で読む最小アルゴリズム節、`green-keeper` 的な最小具体例、その比喩が clean / dirty の観測までしか言い切れずズレの意味づけや優先順位づけまでは自動化しないという破綻点、harness を強くしすぎたときの failure mode、「明日 1 個だけ変えるなら何か」、そして「何を runtime に入れず人間へ残すか」、runtime を **観測 → 停止 → 修復 → 意味づけ** の順で育てる実務ルール、さらに最後の `意味づけ` だけは runtime に載せず人間へ受け渡すという境界に加え、`しつけ` 比喩は growth order 全体を説明するものではなく、せいぜい `観測 / 停止 / 修復` の前半までに効き、最後に「何が本当に重要なズレか」を決める `意味づけ` は loop の外側に残る、という seam、そして runtime に入れる前に人間側で先に捨てるべき癖（後付け説明 / proxy の本体視 / 例外の雑な一般化）まで足し、短稿段階でも loop の読み筋と「どこで人間の雑な自己正当化を止めたいのか」が分かる状態にした。さらに 2026-06-19 の local polish では、§4→5 / §5→6 / §8→9 / §11→12 に短い forward bridge を足し、§13 には「比喩で写すのは反復で振る舞いを固定する関係だけで、感情や忠誠の表面属性ではない」という break-point 明示を追加した。続く圧縮 pass では、RAD の controlling idea / clutter-cut 基準に寄せて、導入の言い換え、PoC 節の冗長説明、runtime 境界まわりの重複を少し削り、spine を「AI を賢くする技術より、人間側の曖昧さを通さない discipline」へより寄せた。補助導線の外部 2 本も Distill `Research Debt` と Mitchell Hashimoto `My AI Adoption Journey` の実 URL へ揃えた。**現在地**は、runtime に入れるもの / 人間へ残すもの / この短稿で話さないものの境界まで固定した local-only draft であり、最新 `44ed5af` は ledger 未反映の最新 1 件として残るのが正常状態である。
- 続く軽い圧縮では `qiita47_harness_engineering_thoughts.md` の 0〜4 章だけを再度削り、列挙で 1 行ずつ使っていた「人間側の揺れ」を 1 文へ畳み、`AI のための discipline` と `人間のための discipline` の二重言い換えも 1 回へ寄せた。主張は変えず、前半の spine を「ハーネスは人間側の雑さを通さない器」という軸に揃えた。
- その後の micro-polish では、`qiita47_harness_engineering_thoughts.md` の forward bridge が `次は...` 型に寄りすぎていた 3 箇所だけを崩し、本文の接続は保ったまま機械的な反復を弱めた。
- 追加の軽微修正では、`qiita47_harness_engineering_thoughts.md` の §0 だけは bullet の走査性を優先して 4 項目列挙を復元し、§5→6 ブリッジも見出しの `PoC` 反復と近接しすぎない言い回しへ戻した。`qiita45_human_ai_dev_incident_patterns.md` の対応表では `human-gate / permission boundary` 行を `(補助線)` と明示し、本文の主従と揃えた。
- 続く micro-polish では、`qiita45_human_ai_dev_incident_patterns.md` の `## 2` にある `研究側で特に近い型` / `要するに` 周辺も 1 パスだけ削り、main path が「4 類型を持ち帰る段」だと読み取りやすい粒度へ揃えた。
- その後の補足では、「5 点」看板が **主線として持ち帰る 4 類型 + 補助線 1 つ（human-gate）** の 4+1 だと本文で一度言い切り、件数の見え方を揃えた。
- さらに `qiita45_human_ai_dev_incident_patterns.md` の前半にも、`handoff / human-gate / diff / checkpoint` は**運用上の持ち帰りカテゴリ**、後段の `4+1` は RAD 接地の**分析レイヤ**だと 1 文だけ足し、taxonomy の切替点を拾い読みでも誤読しにくくした。
- さらに `qiita45_human_ai_dev_incident_patterns.md` の `## 2` では、`ローカルコーパス要約の上でも` を `ローカルコーパス要約でも` に縮め、`要するに本稿の main path で持ち帰りたいのは` も `要するに持ち帰りたいのは` へ詰めて、説明口調だけを少し落とした。
- 最後の micro-polish では、`qiita45_human_ai_dev_incident_patterns.md` の `## 2` 冒頭にあった 2 文切りの導入も 1 段へ畳み、main path の論点に入るまでの助走をさらに短くした。
- 上記の `qiita45` / `qiita43` / `qiita44` / `qiita47` 更新は、commit `2a8b942` (`sync qiita handoff and draft polish`) として確定済みである。handoff はこの commit 境界を正本として読む。
- 追加確認として、`VLAA-GUI` / `Resilient Write` / `Crab` / `Measuring the Permission Gate` の arXiv 4 件は 2026-06-19 に一次情報で URL / title / author を照合済みだと本文へ固定した。あわせて `5 点` は運用カテゴリ、`4+1` は RAD 接地の分析レイヤだと 1 行で明示し、taxonomy の切替が誤読されにくい形へ揃えた。
- 同じ変更範囲では、`qiita43_harness_loop_stack_en.md` / `_zh.md` / `_ko.md` の `### prompt → context → harness → loop の流れ` に `paradigm_staircase.svg` と caption を同期し、#43 local source residual translation drift 監査を一旦クローズしてよいとした根拠差分を 3 本の実ファイルへ固定した。
- また `qiita44_evolutionary_programs_block_diagram.md` では MIT Press gate の staging comment を `soft-gate` と `別 UI / 別ブラウザ経由の補助観測` に揃え、到達性 hedge の実差分を本文側へ残した。
- `qiita37_gpu_triple_run_gate_price_kamikudaki.md` は「短すぎてアルゴリズムや PoC の量が見えない」という指摘を受けて増補した。`1 分version` と比喩パートのあいだに、**「実験 3 本の中身」**（HD-1 full / HD-1 null / Stage-B）と **「AI は裏で何を自走したのか」**（pre-registration / attacker AI 3 体 / major 5 件修正 / Kaggle T4 / 152 runs / `$0`）の 2 節を追加し、完全版の骨格を壊さず plain-language の厚みを戻した。
- 2026-06-19 の editorial 方針追加として、「公開済みの短い companion 記事は、十分に長い本編へ統合できるなら統合を優先し、空いた item は新記事の器として再利用する」を採用した。ただし `#37` は、`4 文指示 / 実験 3 本 / PoC 裏方 / 17〜19 倍 / 0 円 / safety tax 本文接続` は完全版へ吸収済みでも、**EN/ZH/KO 多言語スイッチャーと curated 関連ニュース節は未吸収**なので、いったん本文保全を優先する。
- なお `qiita43/46/47` に対する現行差分は **local source の内部 polish のみ**で、外部 publish / PATCH / 統合作業はまだ始めていない。#37 の外部アクション判断とは切り分けて読む。
- この前提は 2026-06-19 に一次情報で確認済みで、`qiita37_gpu_triple_run_gate_price_kamikudaki.md` は front matter 上 `private:false` / `id:f06ca92ea208c7646fcd`、Qiita live HTML / API も `200` を返した。一方 `qiita43_harness_loop_stack_kamikudaki.md` / `qiita46_llterm_supervision_first_kamikudaki.md` / `qiita47_harness_engineering_thoughts.md` は front matter 上 `private:true` / `ignorePublish:true` の local draft である。
- ただし `#37` には local representation が 2 本ある。public short companion の更新対象は `tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md` (`id:f06ca92ea208c7646fcd`) で、`docs/articles/QIITA_#37_gpu_triple_run_gate_price_kamikudaki.md` は `id:df687d0ecddb56d5a373` / `qiita_public_id:f06ca92ea208c7646fcd` を持つ **多言語アーカイブ / Team mirror** である。
- `#37` の短稿と完全版を本文比較した結果、**核説明は概ね吸収済みだが、EN/ZH/KO 多言語スイッチャーと curated 関連ニュース節は未吸収 = 要保全**だと分かった。したがって次の外部アクション案は redirect ではなく、短稿本文を残したまま canonical 告知だけ足す形へいったん切り替える。
- local source `qiita37_gpu_triple_run_gate_price_kamikudaki.md` はこの保全案へ戻し済みで、冒頭に「完全版 #37 が正本」告知を追加し、本文本体は維持した。front matter `ignorePublish` は **qiita-cli 系の一括 publish を止めるため** `true` のまま維持し、2026-06-19 に live item `f06ca92ea208c7646fcd` へ PATCH まで完了した。
- `.remote/f06ca92ea208c7646fcd.md` と現行 local source の再 diff も 2026-06-19 に取り直し、**companion-preserved switcher（EN/ZH/KO 導線）** とマスコット画像 + 📗導入の live-only 2 ブロックはすでに local source 側へ保全済みだと再確認した。現時点の主要差分は canonical 告知ブロックと `実験 3 本` / `AI は裏で何を自走したのか` の補足節である。
- ここで使う `ignorePublish` は Qiita 標準属性ではなく、`qiita-cli-poc` ローカル運用の publish 安全柵である。`tools/qiita_public_post.py` もこれを読み、`ignorePublish:true` の source は **`--force-ignore-publish` が無い限り fail-closed で BLOCK** する。したがってこのポスター経路の実ゲートは **`ignorePublish` override gate（`--force-ignore-publish` 必須）+ `post <file> --yes` + human-gate 承認** である。ただし live PATCH 経路で `--force-ignore-publish` を付ける時点で、この柵自体は override 済みなので、**実保護は human-gate と step3 の本文 word-diff 目視と preflight** にある。この override は今回の `#37` companion PATCH 限定で、他ファイルへコピペ流用しない。また「redirect」は HTTP 転送ではなく、Qiita 本文を統合告知 + canonical 誘導へ差し替える運用語として使っている。
- `tools/qiita_public_post.py` は filename ではなく frontmatter `public_id` を冪等キーとして public PATCH/POST を分ける実装なので、PATCH 直前は `tools/.../qiita37_gpu_triple_run_gate_price_kamikudaki.md` の `public_id` / `id` のどちらを使う source かだけ再確認すればよい。custom 名そのものは直ちに重複条件ではない。
- 追加で、`tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md` に `public_id:f06ca92ea208c7646fcd` を明示し、public poster の dry-run 上も `PATCH update public_id=f06ca92ea208c7646fcd` と解釈される source へ揃えた。`id:` は既存 metadata 互換のため残し、poster 実装の冪等キーとしては `public_id` を正とする。
- 完全版 source `tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price.md` にも `public_id: 6f44575d440a9ebf5228` を追記し、完全版側を触る場合も accidental create ではなく PATCH update へ入る前提を揃えた。
- `qiita_public_post.py` の frontmatter `private:` も、この public poster では payload に使われない。可視性の既定値は frontmatter **`public_private:`** で与え、**CLI の `--private` はそれを強制 override** する。`#37` companion の live 更新は一般公開 PATCH 前提なので、ここでは `public_private` 既定 false / `--private` なしで読む。
- 2026-06-19 の hardening で、`qiita_public_post.py` は `private:` だけがあり `public_private:` が無い source、または両者が矛盾する source を **fail-closed で拒否**するようにした。`#37` source には `public_private: false` を明示済みである。
- さらに `public_private` の値も strict parse に切り替え、未認識値は一般公開へ黙落ちさせず BLOCK するようにした。あわせて `tools/qiita-cli-poc/public/*.md` の `private:` 単独 69 件へ `public_private:` を機械追加し、`public_id` を持つ PATCH 対象は 2026-06-19 時点で欠落 0 件まで移行済みである。
- 2026-06-19 の追加 hardening で、tag drift 比較は case-insensitive のまま維持しつつ、**送信 payload のタグ表記は frontmatter 原文の大小文字を保持**するよう修正した。これで `AI` / `FullSense` が live PATCH 時に `ai` / `fullsense` へ壊れる回帰を防ぎ、`TODO_TAG` プレースホルダも payload から除外する。
- さらに human-gate 後に実行する最終前提として、`https://qiita.com/furuse-kazufumi/items/f06ca92ea208c7646fcd` をブラウザで開き、表示される live item が **完全版 `6f44575d440a9ebf5228` ではなく short companion 本文**だと目視確認してから `post ... --yes --force-ignore-publish` を打つ。dry-run は network なしなので、この目視確認が `public_id` 取り違え防止の最後のゲートである。
- この実装前提は docs だけに留めず、2026-06-19 に `tests/test_qiita_frontmatter.py` へ最小回帰テストを追加した。内容は、`qiita_public_post.py` で **`public_id` 有りなら PATCH / `id` だけでは POST create 扱い**になることと、frontmatter `private:` ではなく `public_private` / CLI `--private` だけが公開可視性を切り替えることの 2 点である。
- さらに `qiita_public_post.py` は、**`id` はあるが `public_id` が無い** source を dry-run したとき warning を出し、実 `post --yes` では **`--allow-create` が無い限り fail-closed で停止**するようにした。これは初回 public 化でも起こりうる正常 warning / gate で、`public_id` は Qiita API の公式 frontmatter 名ではなく **このラッパーの PATCH 識別子**である。`#37` companion は `public_id` 付きなのでこの warning / gate に掛からず、PATCH source として読める。
- そのうえで `#37` live PATCH runbook も 6 段へ固定した。ここで言う `preflight` は CORS の OPTIONS ではなく、**このラッパー独自の pre-patch health check** である。まず `python tools/qiita_public_post.py preflight ... --refresh-baseline` で live API 本文を `.remote/f06ca92ea208c7646fcd.md` に再取得し、その場で `PATCH update public_id=f06ca92...` / `ignorePublish` warning（expected） / `private: False` / `auth_status: 200` / `api_status: 200` / `api_private: False` / `html_status: 200` / `baseline_body_preserved: True` / `asset_count: 3` / `preflight: OK` を確認する。baseline refresh は **live title / visibility / tags / URL / HTML 到達性が payload と整合したときだけ** `.remote` を更新し、不一致なら fail-closed で baseline を汚さない。さらに `--refresh-baseline` は `public_id:` と `preflight_remote_baseline:` の両方が無いと no-op ではなく fail-closed で止まり、baseline write の OSError も `BLOCKED` 扱いで返す。step1 では 3 asset とも `content-type=image/...` で返っていることに加え、`baseline_refresh_tags` / `baseline_tags` / `api_tags` が `['ai', 'fullsense', 'llcore', 'かみくだき', '機械学習']` で一致していることも合わせて見る。続いて `.remote/f06ca92ea208c7646fcd.md` を `f06ca92ea208c7646fcd.prepatch.md` へ退避し、human-gate の監査証跡を残す。今回の `#37` companion source は 2026-06-19 時点で **既存行の順序保存・非削除・非改変**を前提に hardening している。step3 では `git diff --no-index --word-diff=color tools/qiita-cli-poc/public/.remote/f06ca92ea208c7646fcd.prepatch.md tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md` を明示取得し、companion-preserved switcher とマスコット画像 + 📗導入を含む companion 本文が保全されていること、frontmatter `tags:` 行が drift していないこと、かつ既存行に削除・改変が無いことを確認する。新規行は中間挿入でも機械ゲートを通りうるため、承認者がこの word-diff 出力を目視し、挿入位置まで精査することを human-gate の必須条件とする。step4 でブラウザ上の `f06ca92...` live item が short companion 本文であることを目視確認してから、step5 の `post ... --yes --force-ignore-publish` を打つ。`post` 自体も送信前に preflight 相当（auth / live title / live visibility / live tags / asset / marker 非要求）を再評価し、未通過なら fail-closed で止まる。現行設計では **live tags ≠ payload tags の既存 public 記事 PATCH も BLOCK** するため、将来タグ編集を伴う PATCH を通すには別の explicit override 方針が要る。step1〜step5 の間に時間が空く、または live を別 UI で触った疑いがある場合は step1 からやり直す。step6 では `python tools/qiita_public_post.py preflight ... --require-marker` で `marker_present: True` と `preflight: OK` を確認し、あわせて `kamikudaki_shishi.svg` を含む live SVG / 画像描画と多言語導線 `bdfad6db3f2e70c40511` / `fa0890f136636d495ea6` / `e5093e4816b25c1bd4d0` の到達性を目視確認する。Qiita / imgix 側キャッシュで古い描画が残る場合は `?v=20260619N` cache-bust を足して source を更新し、step1 から runbook をやり直して再 publish する。publish 直後に `marker_present: False` が一過性で出る場合は即失敗扱いせず、少し待って再確認する。もし `marker_present: False` が継続する場合は、Qiita API の live body でも marker 文字列が見えるかを確認し、HTML 側の整形差か本文未反映かを切り分けてから失敗判定する。`#37` source は `public_id` 付きなので `--allow-create` は不要である。
- 実行結果として、2026-06-19 の `preflight --refresh-baseline` は `baseline_body_preserved: True` / `baseline_tags_match: True` / `preflight: OK` を返し、`pytest tests/test_qiita_frontmatter.py` も `64 passed` だった。続く `post ... --yes --force-ignore-publish` は `OK (200) [PUBLIC(一般公開)]` で通過し、直後の `preflight --require-marker` も `marker_present: True` / `preflight: OK` を返した。live HTML 側でも canonical id `6f44575d440a9ebf5228` と多言語導線 3 本の存在を再確認済みである。
- `.remote/f06ca92ea208c7646fcd.md` と `f06ca92ea208c7646fcd.prepatch.md` は `.gitignore` 対象の監査補助物で、repo 単独では再検証できず、将来の `--refresh-baseline` で上書きされうる。必要なら同じ runbook を step1 からやり直して再採取する。
- step4 は、live item が short companion であることを見るだけでなく、**PATCH が source からの title / tags / body 全置換**である以上、live-only 編集を失ってよいかを確認する gate として読む。
- さらに 2026-06-19 の pre-patch baseline として、`preflight` は `PATCH update public_id=f06ca92...` / `ignorePublish` warning（expected） / `private: False` / `auth_status: 200` / `api_status: 200` / `api_private: False` / `api_tags:['ai','fullsense','llcore','かみくだき','機械学習']` / `html_status: 200` / `marker_present: False` / `asset_count: 3` / `preflight: OK` を返すことまで読み取り専用で確認した。`baseline_refresh_tags` / `baseline_tags` も同一集合で一致している。
- baseline の asset 対象も `kamikudaki_shishi.svg` だけでなく `191.jpg` / `192.jpg` へ広げ、3 件とも raw `200` を確認した。raw asset URL は `origin/main` を解決するが、local `main` が `origin/main` より 263 commits ahead でも今回参照する 3 asset は remote `main` 側で確認済みなので runbook に影響しない。
- なお、未吸収 2 ブロック（**full-article-pending switcher** / curated 関連ニュース節）は完全版 `6f44575d440a9ebf5228` 側の将来課題であり、short companion 側の欠落ではない。live PATCH option 1 は companion 本文保全のまま canonical 告知を反映する選択として扱う。
- このターンで言う RAD grounding は、主に `D:/docs/loop_engineering_corpus_v2/` の `fail-closed`, `human_in_the_loop_approval_gate`, `progressive_delivery_canary_metric_gate` と `D:/docs/article_craft_corpus_v2/136_ablations_baselines_as_honesty_*.md` を指す。
- あわせて、読む順ガイド `ac398349ec42e40913f1.md` と `docs/articles/QIITA_SERIES_INDEX.md` の #37 導線も `canonical / companion` 表記へ揃えた。live URL 自体は変えず、local index 上の役割だけ明示している。
- `qiita44_evolutionary_programs_block_diagram.md` の参考文献節には、2026-06-18 時点で GA / ES / GP / NEAT / novelty search / MAP-Elites / CMA-ME / lexicase の一次導線 URL を補った。本文の主張強度と参考導線の最終突合は完了済みで、MIT Press 2 件の到達性 gate は 2026-06-19 時点で **soft-gate** 状態へ整理した。
- `qiita44_evolutionary_programs_block_diagram.md` は本文と参考導線の spot-check も 1 パス通した。GA = 固定長遺伝子列、ES / CMA-ES = 変異分布更新、GP = 式 / プログラム木進化、NEAT = 構造進化、novelty / MAP-Elites / lexicase = 「何を残すか」の分岐、という説明は参考節の入口と整合している。
- `qiita44` の claim-strength pass では、論旨を変えずに過強な断定を 3 箇所だけ弱めた。具体的には `淘汰器が壊れていたら進化はだいたい壊れる` → `探索は鈍りやすい`、`長期でだいたい飽和か monoculture に寄る` → `寄りやすい`、`descriptor が高次元になると cell の大半が空になる` → `空になりがち` へ調整した。
- 続く最終微調整では、事実主張よりトーンが先行していた 4 箇所も弱めた。`これはかなり重要です` → `ここは見落としやすい点です`、`これは本当に重要です` → `ここは切り分けを誤りやすい点です`、`かなりクリア` → `だいぶクリア`、結語の `壊れやすい` → `詰まりやすい` とし、論旨を保ったまま断定トーンだけ落としている。
- Holland / Koza の MIT Press permalink を本文と handoff で揃えた後も、`何を残すか` を中心にした本文の主張強度は参考節の入口と矛盾していないことを再確認した。`qiita44` の未解決論点からは「canonical permalink を主参照として維持する」点は外してよいが、gate 自体は一度きりの補助観測に依存する **soft-gate** として残す。
<!-- QIITA44_GATE_POINTER_BEGIN -->
- `qiita44` の publish 前残タスクであった到達性 gate については、2026-06-18 時点で記事側の Holland 導線 `Adaptation in Natural and Artificial Systems`（canonical permalink `https://mitpress.mit.edu/9780262581110/adaptation-in-natural-and-artificial-systems/`、DOI `10.7551/mitpress/1090.001.0001`、resolver `https://doi.org/10.7551/mitpress/1090.001.0001`）と、Koza 導線 `Genetic Programming: On the Programming of Computers by Means of Natural Selection`（canonical permalink `https://mitpress.mit.edu/9780262527910/genetic-programming/`）を対象に、PowerShell `Invoke-WebRequest` + browser UA + Cookie なし、および Microsoft Edge headless で canonical permalink 2 本と Holland DOI resolver の Akamai 403 までは証跡化済みである。ここで確定している事実は **このローカル egress からは Akamai 403 を受けた** ことだけであり、reader にとってリンクが無効だとまでは言えない。Holland の DOI `10.7551/mitpress/1090.001.0001` は 2026-06-18 に Crossref API で `The MIT Press` / `Adaptation in Natural and Artificial Systems` / `John H. Holland` / `1992-04-29` の一致を確認済みで、citation 上の主参照から外さない。Koza 側は Crossref の title/author 検索と `9780262527910` クエリでは MIT Press 書籍 DOI を特定できていない一方、MIT Press title page では paperback `9780262527910` / hardcover `9780262111706` の同一書誌として確認でき、WorldCat でも OCLC `26263956` の 1992 MIT Press print book として確認できた。したがって現時点では DOI 未固定のまま canonical permalink を主参照として維持し、必要なら補助導線として publisher catalog / WorldCat を併記する。
- `qiita44` の gate は **自 egress の 403** と **citation integrity** を分けて扱う。主参照は DOI / canonical permalink を維持し、archive.org / WorldCat / Google Books などの非 Akamai 系は差し替えではなく補助導線としてのみ併記する。archive.org も全文スキャン直リンクではなく書誌ページ扱いに留める。再現条件固定での再試行は調査補助手段であり、gate 合否根拠には使わない。
- 2026-06-18 の追加再観測では、このマシンの同一 egress 上で canonical permalink 2 本に対し PowerShell `Invoke-WebRequest`（browser UA / Cookie なし）を再実行し、どちらも `STATUS=403` を再確認した。これは **ローカル観測の再実行**だった。
- 2026-06-19 に **別 UI / 別ブラウザ経由の補助観測**として canonical permalink 2 本を 1 回ずつ開き、どちらもログイン不要の MIT Press 書誌ページとして表示できることを確認した。これは一度きりの観測に留まり、別 egress の恒常的 reachability は未実証である。したがって publish gate は `このローカル egress では 403` と `reader reachability/citation integrity は維持` を分けて整理した **soft-gate** として扱い、非 Akamai 系の補助導線は本文に常時露出させず staging comment に留める。観測時の成功条件は、Holland / Koza の canonical URL がログイン要求や即時 block page ではなく MIT Press の title/bibliographic page と読める画面を返すことだった。Koza 側の DOI は引き続き Crossref で未特定・MIT Press title page / WorldCat までは確認済み、という粒度で維持する。
<!-- QIITA44_GATE_POINTER_END -->
- #43 の `2-6. 起動と実証タスク green-keeper` / `2-7. 「検証可能なゴール」を持つループ — /goal という公式実装` も 4 言語で spot-check し、`desired / actual / drift / repair` の対応、PySide6 GUI / `term` 名残の補足、Haiku 既定と turn cap を含む `/goal` 説明、直後の「捨てた数字」節への橋渡しまで日本語正本に追従していることを確認した。
- 追加 spot-check で、`2-5` honest disclosure 末尾の `2qlJjBwdpYGOVjBkyhhL` 引用が en/zh/ko では本来位置から落ち、第3章直前へ誤配置されていたことを確認した。translations 側は誤配置ブロックを除去し、`2-5` 末尾の本来位置へ戻した。末尾参考の URL 自体は維持している。
- さらに `1-4` 後半の `AI成長マネジメント` / 4理由 / `First, Break All the Rules` ヘッジ / `アンチパターン` / 第2章への橋渡しも 4 言語で spot-check し、日本語正本に対する新たな factual / translation drift は見当たらないことを確認した。
- さらに終盤の `なぜ「手綱を握るのは人間」だと言えるのか — 観察ベースの3点` から、H4Pix 引用を挟んだ結語導入まで 4 言語で spot-check し、`常時並列 / 長射程の伏線回収 / 常時稼働の危険予知` の 3 点、`観察された傾向` というヘッジ、`ルール（構造）で縛る` への橋渡しまで日本語正本に追従していることを確認した。
- さらに参考文献節と末尾 hedge note も 4 言語で spot-check し、`alu.jp` crop URL 数は日本語正本 16 / en 16 / zh 16 / ko 16 に維持され、OpenAI 403 / RAD `47,097 docs` / `人間優位3点` 観察ベースなどの留保も日本語正本に追従していることを確認した。`GPT-5.5` についてはこのターンで OpenAI 公式一次情報によりモデル名の実在を確認し、留保を「モデル名未確認」から「比較値の一次計測元・計測条件未確認」へ締め直した。
- 残ブリッジ棚卸しとして、`第1章末 → 第2章頭`（`なぜ` → `どう` への橋渡し）、`3-1. RAD コーパス → 3-2. LLM Wiki`、`3-4. corpus-first advantage → 統合章` の 3 接続を 4 言語で再確認した。第1章の補助線から第2章の制御論へ移る温度感、`集めた知識は放っておくとただの山` から LLM Wiki へ入る導入、`A/B/C が1本に繋がる` から統合章へ畳む着地まで、日本語正本に対する新たな factual / translation drift は見つかっていない。
- さらに最終棚卸しとして、導入 → 第0章、第0章末 → 第1章頭、`/goal` 節 → 独立 honest disclosure、独立 honest disclosure → 第3章頭、`3-2. LLM Wiki` → `3-3. RAPTOR` の局所接続も 4 言語で spot-check した。一次情報に錨を下ろす作法から用語地図へ入る導入、`実務ブログも査読論文も鵜呑みにしない` から harness engineering の命名確認へ移る接続、`mystery graph` から `捨てた数字` 検証へ降りる橋、`無知の知` から knowledge stack へ移る着地、thought circulation 警告から RAPTOR の evidence ladder へ渡す流れまで、日本語正本に対する新たな factual / translation drift は見つかっていない。
- さらに、まだ handoff に明示していなかった seam として、`2-7. /goal` → ★ honest disclosure 節、`3-3. RAPTOR` → `3-4. corpus-first advantage`、統合章 → まとめ、まとめ → 次回予告 / 参考 も 4 言語で spot-check した。`検証可能なゴール` から `捨てた数字` 実演へ落とす open loop、evidence ladder から corpus-first の条件付き優位へ渡す橋、A/B/C 統合から `手綱 / 輪 / 知` の3点要約へ畳む順序、次回予告と参考節で閉じる終盤構造まで、日本語正本に対する新たな factual / translation drift は見つかっていない。
- 上記までで、handoff がこれまで再開候補として列挙してきた #43 の seam 範囲は一巡した。少なくとも `導入 → 第0章`、`第0章末 → 第1章頭`、`第1章末 → 第2章頭`、`2-7 → ★ honest disclosure`、`/goal` 節 → 独立 honest disclosure、独立 honest disclosure → 第3章頭、`3-1 → 3-2`、`3-2 → 3-3`、`3-3 → 3-4`、`3-4 → 統合章`、統合章 → まとめ、まとめ → 次回予告 / 参考 は 4 言語で spot-check 済みである。ただし、新規 seam 候補の網羅までは保証しない。
- この seam spot-check の最小根跡として、確認観点は `ja/en/zh/ko` 4 言語の見出し語順、★/独立 honest disclosure の節境界、引用 / コードブロックの有無、直前直後の橋渡し文の追従に置いた。
- 追加の機械点検として、4 言語の見出し数 / 引用ブロック数 / コードフェンス数 / table 行数も比較した。`headings=47`、`quotes=54`、`codefence=4`、`table_lines=26`（`|` 含有行ベース）は 4 言語で一致し、section 単位の bullet / quote 分布も本文側は揃っている。front matter タグの既知差は 2 種で、①本数差 = ja のみ `個人開発` が 1 本多い（`ja bullets=81`、en/zh/ko=`80`）、②ローカライズ差 = `AIエージェント`（ja）↔ `Agent`（en/zh/ko）である。いずれも translation drift というより想定内の metadata / ローカライズ差として扱う。
- さらに 2026-06-19 に line 単位 re-diff を section fingerprint で再実行し、見出し index ごとの `heading / quote / bullet / numbered / table / codefence / image / caption` 分布を 4 言語で比較した。新しく actionable だったのは `### prompt → context → harness → loop の流れ` にある `paradigm_staircase.svg` とその caption が en/zh/ko で欠落していた 1 件だけで、これは translations 3 本へ同期済み。再実行後に残った mismatch 8 件は、いずれも en/zh/ko が同じ形で `para-1 / blank-1` を示すだけで、`この章の honest disclosure` 節のように raw URL を blockquote 内 inline link へ畳んだ既存スタイル差・段落結合差として説明でき、新たな structural omission は見つからなかった。残差 index は `7 / 18 / 28 / 31 / 32 / 35 / 40 / 44` で固定しておく。
- `個人開発` タグは、現時点では ja 固有タグとして現状維持する。4 言語タグの完全一致は要件にせず、将来 line 単位 re-diff を回す際は `個人開発` と `AIエージェント` ↔ `Agent` の両方を既知差として除外する。
- 2026-06-18 終了時点の到達メモとしては、#43 は companion / `green-keeper` / `/goal` 帯まで監査済み、#46 は JA/en/zh/ko/kamikudaki の本文と endmatter まで監査済み、Team stock 3 本は Team POST と item id 記録まで完了していた。その後 2026-06-19 の handoff / 草稿更新は commit `2a8b942` で確定した。現行 blocker として最優先で残すのは、Qiita Team 3 本で **API GET は `private:false` を返し、未認証 HTML は `/login` へ落ち、public `qiita.com` direct probe は `404` だったが、それでも team-only と positively 確認できていない**点である。事実として未認証一般ユーザーへの実露出までは確認できていないが、可視範囲是正（rollback / visibility tightening）が必要かどうかの判断待ち案件として、残件一覧から落とさない。
- 追加の観測として `group.url_name: general` / `group.private:false` / `organization_url_name:null` も確認済みで、poster が当時 `group_url_name` を送っていなかったことから implicit General sharing 仮説を追っている。ただし blocker の主語は引き続き **過剰露出疑いを否定できないこと**であり、local source に `general` を resend default として固定しない。
- 未解決の human-gate 外部アクションは、#46 の publish 判断、dev.to 英語版 update / publish 判断、CTA-149 local batch の live 再 publish / PATCH 要否判断の 3 件である。Qiita Team 3 本の rollback / visibility tightening は、必要だと人間が判断した時点でこの集合へ追加する。
- dev.to 英語版の残件定義も実ファイルと一致している。`tools/qiita-cli-poc/public/qiita43_harness_loop_stack_en.devto.json` は `id: 3915834` / `published: false` / dev.to URL 付きの sidecar として残っており、公開前に human-gate を要する draft 状態である。
- `NEXT_SESSION.md` の旧 operator queue 見出しは `old context / current scope outside (2026-06-12 stale)` へ更新し、asciinema 録画 / production 起動 / credential 復旧は **ローカル operator 作業の旧メモ**であって、現行の未解決 human-gate 外部アクション 3 件とは別カテゴリ・現行優先ではないことを明記した。
- public Qiita 記事 `bf1cfe3b4f40b87f068d` への本文更新は実施済み。
- `.llterm/loop_ledger.jsonl` は deindex 実行済み。`.gitignore` にファイル単位で追記し、local-only telemetry として on-disk では保持しつつ Git 追跡から外す運用へ切り替えた。
- `tools/qiita-cli-poc/public/bf1cfe3b4f40b87f068d.md` は canonical 誘導案の local source として整備済み。
- バス江挿絵の CTA 整理では、既定の referral 用コマは引き続き `012.jpg`（「ひくわ」）を採用し、`044.jpg` は「押し売り感をわざと過剰化する強め variant」として台帳に別定義した。全記事一括差し替えはせず、個別草稿で opt-in 採用する。
<!-- CTA149_BATCH_STATE_BEGIN -->
- いま手元で整えていた CTA-149 batch は、live の `22d5460384c2cb54a9e6` を直す作業ではなく、`qiita43/44/45/46/47` の local source 末尾 CTA を整える差分であった。`149.jpg` は opt-in の強め variant に戻し、`1-week free trial` / `1 週間の無料トライアル` などの時限断定は「無料で試せる（提供条件は公式参照）」へヘッジした。en/ko CTA キャプションの `\"` エスケープも local source 側では除去済みで、live 再 publish / PATCH はまだ実行していない。
- この CTA-149 local batch は commit `430fcdc` で確定済みで、review 対象の local-only 差分は worktree から消えている。残件は live 再 publish / PATCH が必要かどうかの human-gate 判断であり、未解決の外部アクション一覧から落とさない。
<!-- CTA149_BATCH_STATE_END -->
- handoff 3 文書（`docs/NEXT_SESSION.md` / `docs/SESSION_SUMMARY.md` / `docs/next_plan.md`）は同じ handoff 群として追うが、**commit range 台帳の正本は `SESSION_SUMMARY.md` / `next_plan.md` の 2 枚だけ**である。`NEXT_SESSION.md` は後続の実質更新で別タイミングに進むため、直近更新 hash を range 注記へ固定しない。`NEXT_SESSION.md` の現在地は、このファイル群の commit range ではなく `NEXT_SESSION.md` 本文側の現況メモを正本として読む。
- 公開 safety 柵は維持:
  - `qiita43_harness_loop_stack_kamikudaki.md` = `private: true` + `ignorePublish: true`
  - `qiita44_evolutionary_programs_block_diagram.md` = `private: true` + `ignorePublish: true`
  - `qiita45_human_ai_dev_incident_patterns.md` = `private: true` + `ignorePublish: true`
  - `qiita46_llterm_supervision_first.md` = `private: true` + `ignorePublish: true`
  - `qiita46_llterm_supervision_first_kamikudaki.md` = `private: true` + `ignorePublish: true`
  - #43 en/zh/ko draft も `ignorePublish: true`

## いま worktree に残っている差分

- なし。`loop_ledger` deindex は commit `7745f84` で確定済み。

## 今回 commit した差分の要点

- #43:
  - 第3章導入〜`3-2. LLM Wiki` 本体の主要段落を日本語正本→en→zh→ko の順で spot-check し、3層スタック説明、`RAD_INDEX.md` / `65 RAD corpora` 導入、`47,097 docs` と `32,503 files` の内訳、`hacker_corpus` の raw 集約ファイルという留保、Karpathy 帰属のヘッジ付き `LLM Wiki` 3層導入、thought circulation / Anti-Circulation Safeguards、製品対応づけまで多言語 draft が日本語正本に追従していることを確認した
  - en/zh/ko に欠落していた「半信×半疑」の引用ブロックと URL を既存の inline 引用形式へ揃えて日本語正本へ同期し、末尾参考リストにも `Ud7lZLbei1F5xaFuAq3i` を追加した。`3-2. LLM Wiki` 本体は quote block と参考導線を含む主要論点まで局所確認済みとして扱える状態になった
  - 公開済み英語版 Qiita item `2622da17495d61480fa2` のタイトル崩れ（`# >-` 表示）を再現し、原因を front matter `title: >-` と poster 側の最小パーサ不一致と特定した。英語版 / 韓国語版 source は single-quoted title へ修正し、英語版には `public_id` も明示した。`tools/_frontmatter.py` を新設して poster / converter 4 経路へ共有化し、`tests/test_qiita_frontmatter.py` で folded scalar / single-quote escaping / block list の回帰テストを追加した。human-gate 後の public PATCH と API / HTML 確認まで完了した
  - #43 本文の旧名称 `llloop` / 起動コマンド `lll` を、最終名称 `llterm` へ 4 言語草稿で一括置換した。あわせて handoff 内の現行進捗説明も `llterm` 表記へ揃え、archive 扱いの旧メモは温存した
  - さらに #43 の `llloop` / `llterm` 関係を補足し、`llloop` は terminal 内で回していた TUI 試作、`llterm` は TUI の入力・表示・観測で行き詰まりを感じて作り直した GUI 版だと 4 言語本文へ明記した
  - あわせて llterm 実 repo (`D:/projects/llterm`) を一次確認し、`pyproject.toml` の `gui-scripts` と `src/llterm/gui/app.py` の実装に合わせて、#43 の `2-6` 起動説明を「console script の対話メニュー」から「PySide6 GUI エントリポイント」へ修正した。`term` が残るのは terminal 起点の名残、という補足も追加した
  - #43 の「キン肉星＋R.O.D＋リィンカーネーション＋ROS PBT」の 4 連想について、引用や画像の誤用に見えないよう補足説明を追加した。4 つの連想がそれぞれ「種の並立 / 知識の外部化 / 同じ魂の再搭載 / 世代交代つき個体群評価」という別々の設計部品を指していたことを、ja/en/zh/ko で明示した
- public Qiita:
  - public Qiita 記事 `bf1cfe3b4f40b87f068d` を、既公開 canonical `6e107c7dfa0c261ee4d7` へ誘導する short redirect 本文へ PATCH 更新した。ローカル source は `tools/qiita-cli-poc/public/bf1cfe3b4f40b87f068d.md` として保持し、前例 `0a35e1bfb814adab8565` と同じ「統合・再編しました」+ canonical 直リンクの文面へ揃えた
  - Qiita 側の反映確認は、このセッションで実行した API / HTML の自己確認ログに基づく。Qiita API `GET /api/v2/items/bf1cfe3b4f40b87f068d` の `body` 先頭と、公開 HTML の canonical ID `6e107c7dfa0c261ee4d7` / 「統合・再編しました」の文言が一致していた
- 記事ネタ評価:
  - llterm 側 commit `ff066bdf99db74263f1c6208fa8a671a080bc7fc` 時点の `D:/projects/llterm/docs/ARTICLE_SEEDS.md` を読み、`docs/articles/2026-06-18/llterm_article_seeds_screening.md` に記事化スクリーニングを追加した。結論は、**本命長編は 種 #6「自走 AI ループの作り方と落とし穴」**、単独中編候補は 種 #1「注入タスク飢餓」だったが、handoff 方針としては #1 を先出しせず #6 の導入 incident に吸収する、というもの
  - さらに `docs/articles/2026-06-18/llterm_seed6_article_plan.md` を追加し、種 #6 の controlling idea、hook + nut graf、6-beat through-line、種 #1〜#5 の章マッピング、章構成案、9 原則の骨子まで固定した。Qiita 草稿の spine は確定済みだが、各原則の 1 段落肉付けはまだ残っている
  - `docs/articles/2026-06-18/llterm_seed6_evidence.md` を追加し、`13 分` / `ctx 2549%` / `billing 累積値の occupancy 誤用` / `race 依存の緑` など公開直結の具体主張を、llterm 側 `ARTICLE_SEEDS.md` から fullsense repo 内へ根拠スナップショットとして固定した
  - `tools/qiita-cli-poc/public/qiita46_llterm_supervision_first.md` を新規作成し、種 #6 の Qiita 草稿を起こし始めた。現時点では front matter つき draft として、冒頭 3 点ボックス、hook + nut graf、`0. まず結論`、`1. 「進捗を要約して」が永久に返らなかった` までを書き、through-line が実際の prose でも立つところまで確認した
  - 同 draft に続けて `2. ターン境界と緊急割り込みは、最初から別物として設計する` と `3. ctx 2549% は「AI が太った」のではなく、計測が壊れていた` を追記した。通常注入と interrupt の分離、sticky cancel の罠、累積 billing 値と瞬間 occupancy の混同、codex 自己圧縮と llterm rotate の二重管理まで prose 化し、中核 3 章がつながった
  - さらに同 draft に `4. 多AIレビューは質だが、無条件に重ねるとただ遅い`、`5. 追えないなら監督ではない`、`6. テストも「たまたま緑」を疑う` を追記した。記録ターンへのフルレビュー二度漬け、全行タイムスタンプ / ローテログの architecture-level 意味、並行テストの block point と suspiciously green の疑い方まで prose 化し、第6章まで一本の流れになった
  - さらに同 draft に `7. 障害対応から抽出した、loop engineering 9原則` と `8. honest disclosure は「敗北宣言」ではなく、監督の一部` を追記し、9 原則の本文化、未解決境界、適用条件、短い締めまで含めて日本語草稿を最後まで通した。残りは publish gate 向けのかみくだき / 多言語 / 挿絵 / 参考文献 / HTML annotation などの派生整備が中心になった
  - その後の wording 調整で、`2549%` まわりの確信度をさらに締めた。rotate 因果は確認済み、`cache 再読込の重複加算` は有力な膨張機序だが `2549%` への算定内訳までは未確定、という二段の境界へ統一し、原則7にも「全章横断のメタ原則」という 1 行を補った
  - さらに publish gate の軽い体裁要素として、#46 本文に `☕ 休憩ポイント` を 3 箇所追加し、末尾へ `関連記事の入口`、`参考文献 / 参考リソース`、HTML annotation メタタグを追加した。その後 `025.jpg` も本文導入に実投入し、クレジットを `Snack Basue` に統一、raw URL の HTTP 200 も確認した。画像 URL は既存運用どおり `raw.githubusercontent.com/.../main/...` を維持し、残る gate 項目は、かみくだき版 / en-zh-ko の仕上げが中心になった
  - 続けて `tools/qiita-cli-poc/public/qiita46_llterm_supervision_first_kamikudaki.md` を新規追加し、#46 の 10 分短縮版 draft を起こした。結論を「AI を賢くするより、人間が見失わない境界を作る」に絞り、通常注入 / 異常値 / 審査強度 / telemetry の 4 点だけを先に掴める構成にした
  - その後の publish gate 補正で、#46 本文の「実装レベルの低層根拠」は内部ログにつき非公開だと明示し、第7章末尾に `☕ 休憩ポイント` を追加した。`kamikudaki` 側では重複していた関連記事 URL を整理し、完全版 #46 の公開 URL は未発行のため publish 時追記と明記した。あわせて `kamikudaki_shishi.svg` の raw URL は 2026-06-18 時点で HTTP 200 を確認済み
  - さらに `kamikudaki` 版を磨き、冒頭ナビを `1 分 version / 境界設計 / 4原則 / 完全版で掘る 3 点 / 覚えて帰るポイント` に整理した。途中で「境界を作る」とは何かを 3 行で砕き、完全版側へ送る論点も 3 点に固定した
  - 続けて #46 の en/zh/ko draft を新規作成し、タイトル、冒頭 3 点ボックス、`honest disclosure`、第0章、`025.jpg` キャプション、第1章前半（注入飢餓の導入と `2549%` 露出）まで同期した。その後さらに 3 言語とも第1章末尾〜第2章（turn 境界 / queue / `cancel` vs `interrupt` / `☕ 休憩ポイント`）まで同期し、対応する節を 3 言語で訳了した。続く第3章でも、`2549%` を「確認済みの rotate 因果」と「未解決の算定内訳」に分ける二段の確信度を維持したまま 3 言語へ同期した。さらに第4章も 3 言語で追記し、over-review / record-turn / sign-off の適用範囲を同じ構造で読める状態にした。第5章では traceability / 全行タイムスタンプ / rotate log / fail-safe telemetry を 3 言語で揃え、監督可能性を「後から追えること」として説明する節まで同期した。第6章では `green by accident` / `block point` / `suspiciously green` を軸に、並行テストの race 依存と honest disclosure の適用先を 3 言語で揃えた。続く第7章では 9 原則の一般化を 3 言語へ同期し、`production 観測から芋づるで掘る` というメタ原則と `人間が割り込める境界を実装する` という 1 行要約まで揃えた。さらに第8章と endmatter も 3 言語へ同期し、`honest disclosure` を bookkeeping / supervisability の側へ引き戻す締め、関連記事、参考文献、HTML annotation メタタグまで揃えた
  - その後の zh 最終見直しで、`算定内情` 系の訳語を第3章と第7章で統一し、繁体字混入していた `飢饿` も `饥饿` へ揃えた
  - さらに zh 第8章末尾に残っていた日本語混在 `障害处理记录` を `故障处理记录` へ直し、締めの 1 文を中国語として自然な状態へ揃えた
  - その後の最終見直しで、ko 第5章に残っていた `본번` / `본처리` を `운영 환경` / `본 처리` へ直し、第6章で固定した用語系と整合させた
  - さらに `kamikudaki` 側の内部語へ 1 行グロスを足し、`注入飢餓` / `ctx 2549%` / `flaky test 露出` が何を指すかを短縮版単体でも判断できるようにした。TL;DR でも「9 原則のうち 4 本を抜粋した短縮版」だと先に明示した
- 挿絵索引:
  - `docs/articles/assets/bazue_all/index.md` にユーザー指定の 4 対応を追記した。`081.jpg` をバイブコーディング、`006.jpg` をハーネスエンジニアリング、`163.jpg` を AI オーケストラ、`025.jpg` をループエンジニアリング実践中のイメージとして再利用する方針を、各コマの `使いどころ` に固定した
  - `alu.jp` crop `1DLuaYTNfWIQz3tqCv1h` は一次確認し、セリフ `『そういうお前も好きやで…』激オチ『頑ななあの娘へ』2章12節から.. 聖書の引用みたいになってる…!` の存在を確認した。今後このコマを記事に使う場合、出典として支えられるのはこのセリフまでで、`honest disclosure` を毎回持ち出す感じ / chapter-verse のように引用する感じ、等の上乗せ解釈は筆者側の比喩として分離して書く
- Team stock:
  - #43 から `Semantic Governance` 単独記事と `LLM Wiki / thought circulation` 単独記事、#46 から ``ctx 2549%`` postmortem 単独記事の 3 本を source-only draft として `tools/qiita-cli-poc/public/` に追加した
  - 3 本とも `private: true` / `ignorePublish: true` のまま `tools/qiita_team_post.py dry-run` を通し、title / tags / body の登録安全性だけ確認した。実際の Team 投稿は human-gate 待ち
- 注意: 2026-06-19 時点の `qiita_team_post.py` は `ignorePublish:true` を読み、`post --yes --force-ignore-publish` を明示しない限り fail-closed で停止する。ただし Team 上の可視範囲は、API `private:false` と未認証 HTML `302 /login` が併存しても十分に確定できていない。`visibility semantics` はここでは **プロジェクト内用語**であり、詳細条件は `team_stock_publish_plan.md` を正本とする
- deindex:
  - ユーザー承認後、`.llterm/loop_ledger.jsonl` に対して `git rm --cached` を実行し、`.gitignore` にファイル単位の ignore を追加した。ログファイル本体は残したまま Git 追跡だけを外す形で、毎セッションの tracked ノイズ差分を止める恒久対策へ切り替えた
- handoff:
  - `NEXT_SESSION.md` / `SESSION_SUMMARY.md` / `next_plan.md` のナラティブを今回監査内容へ更新し、前バッチの #44 / #45 説明が再開導線に残らないよう整理した
  - handoff の commit 列と実施結果列に `d92192f` を backfill し、`20afd3e` 自身は 1-commit ラグ規律どおり次回 backfill 対象に維持した

## 未解決ではないが次に確認すべき点

- commit `bab1557` は **11 ファイル / 1909 insertions / 76 deletions** の doc batch。
- `NEXT_SESSION.md` には publish gate（外部 URL / 著者帰属 / raw 200 / dev.to draft 状態、および translation drift は **local source 側クローズ済み・live URL 側未反映分の管理**として残る）が残っている。
- #43 en/zh/ko は発行済み限定共有 draft のまま凍結している。2026-06-19 の seam spot-check と line 単位 re-diff までで **local source 上の residual translation drift 監査は一旦クローズしてよい** 状態になったため、残件は公開線へ戻す前の live URL 側未反映分と publish gate 管理である。
- `qiita44` の参考文献節には canonical 入口を追加済みで、2026-06-18 に GA / ES / GP / NEAT / novelty search / MAP-Elites / CMA-ME / lexicase の一次導線 URL まで補強した。
  - CMA-ES は失効証明書の旧 PDF をやめ、arXiv `1604.00772` の安定導線へ差し替えた。
  - 本文の言い回しと参考導線の最終突合は完了済みで、MIT Press 2 件の到達性 gate は 2026-06-19 時点で **soft-gate** 状態へ整理した。
- `qiita43_harness_loop_stack_kamikudaki.md` には ☕ 休憩ポイントと参考文献節を追加済み。
  - ただし短縮版のため、一次情報の細目は完全版 #43 側へ寄せる方針を維持。
- `qiita43` en/zh/ko の終盤 hedged note に残っていた RAD 総件数の古い表現は、`47,097 docs` ベースへ更新済み。
- `e4e3968` では #43 多言語 draft の要約表・結論部の RAD 件数も `47,097 docs` ベースへ揃えた。
- `0478fa1` では #43 JA 正本の hedge note と `NEXT_SESSION.md` の stale 記述も `47,097 docs` / live URL 未反映の前提へ揃えた。
- ただしこの `47,097 docs` 修正は **ローカル source 側のみ** で、発行済み限定共有 URL まではまだ更新していない。
- en/zh/ko とも、日本語正本の「約49k件」という数字の扱いに対応する honest-disclosure 節は実在する。
  - 根拠: en は `qiita43_harness_loop_stack_en.md` の `#### honest disclosure (Handling the "About 49k Items" Number)`、zh は `qiita43_harness_loop_stack_zh.md` の `#### honest disclosure（关于「约49k件」这个数字的处理）`、ko は `qiita43_harness_loop_stack_ko.md` の `#### honest disclosure("약 49k건"이라는 숫자의 취급)`。
- 残っているのは「節が無い」ことではなく、節**内部**とその周辺の factual / translation drift。
- `e942370` では上記の factual 反転確認を handoff へ反映し、`loop_ledger` を巻き込まない個別 `git add` 方針も明記した。
- `496ca41` では `e942370` 後の handoff 現在地を更新し、「約49k件」節まわりの局所監査結果を handoff に追記した。
- その後の局所確認では、「約49k件」節と直後の橋渡し段については en/zh/ko とも日本語正本に大筋追従しており、残差は細い訳しぶれの範囲だった。
- さらに RAD 再接地後に `50手法 vs 96ノート` 節も spot-check し、96ノート / 39 documents / 12 clusters の注意書きまで en/zh/ko が日本語正本に追従していることを確認した。
  - ここで確認したのは数値そのものの正当性ではなく、日本語正本に対する訳文追従である。
- さらに `LLM Wiki / thought circulation` 節も spot-check し、Anti-Circulation Safeguards の箇条書きと `llmesh / llive / llove` の製品対応づけまで en/zh/ko が日本語正本に追従していることを確認した。
  - ここで確認したのは日本語正本に対する訳文追従であり、`Anti-Circulation Safeguards` / `thought circulation` / `RAD` の外部一次情報ベースの factual 検証ではない。
  - 追加 spot-check で、Karpathy 帰属のヘッジ、`設計段階` の限定、製品対応づけの「私のマッピング / 主観」表現も en/zh/ko で保持されていることを確認した。
- さらに統合章〜結語も spot-check し、A/B/C の統合表、`手綱 / 輪 / 知` の3点整理、`Bölük 10×` を捨てた設計思想、次回予告の `設計段階` ヘッジまで en/zh/ko が日本語正本に追従していることを確認した。
- さらに導入部（「使うのをやめた数字」 / 一次情報に錨を下ろす / 第2章後の独立 honest disclosure 節で全開示する予告）も spot-check し、異常値を捨てる作法と本稿の主題提示まで en/zh/ko が日本語正本に追従していることを確認した。
- さらに第0章（`prompt → context → harness → loop` の階段 / `Agent = Model + Harness` の二次情報ヘッジ / automation vs loop / 章末 honest disclosure）も spot-check し、階段図の説明、二次情報の留保、`verifiable goal` の橋渡し、実務ブログと学術定義を分ける温度感まで en/zh/ko が日本語正本に追従していることを確認した。
- さらに第1章前半（`harness engineering` 命名経緯 / `vibe coding` 区別 / RAPTOR 2層 / `ハーネス型バイブコーディング` の説明）も spot-check し、Hashimoto/OpenAI まわりのヘッジ、Karpathy との差異、fail-closed の説明、ユーザー側3能力の導入まで en/zh/ko が日本語正本に追従していることを確認した。
- さらに第1章後半〜第2章冒頭（ユーザー側3能力 / AI成長マネジメント / anti-pattern / `loop engineering` の定義 / `Semantic Governance` 導入 / `llterm` honest disclosure）も spot-check し、比喩・留保・戦略説明まで en/zh/ko が日本語正本に追従していることを確認した。
- さらに第2章前半の `loop engineering` をもう一段深く（`react` / `reflexion` / `plan_execute_verify` の差し替え比較 / strategy names のかみくだき）も spot-check し、「固定レシピ」との対比、速さと安全性の二軸、各戦略の平易化まで en/zh/ko が日本語正本に追従していることを確認した。
- さらに第2章前半の `loop engineering` security face（Filip Verloy 引用 / `scaling risk at machine speed` / `Semantic Governance`）も spot-check し、警句・出典導線・自作ハーネスの設計動機への橋渡しまで en/zh/ko が日本語正本に追従していることを確認した。
  - 確認方法: JA `qiita43_harness_loop_stack.md:313-323, 687-695` と en/zh/ko の対応段落・参考文献行を横並びで突き合わせ、本文リンクと末尾出典の両方に Verloy Medium URL があることまで確認した。
- さらに第2章中盤（`fail-closed` 安全層 / `現状の実装では` の条件付き留保 / `green-keeper` / `/goal`）も spot-check し、SafetyPolicy の 3 段判定、CircuitBreaker / Budget / 認証要求検知、`Executor` 条件付きの honest disclosure、GitOps reconciliation 比喩、`Haiku` 既定の `/goal` 説明まで en/zh/ko が日本語正本に追従していることを確認した。
  - ここで確認したのは主に日本語正本に対する訳文追従であり、Claude Code `/goal` docs の外部一次情報ベース再検証をこのターンで追加実施したわけではない。
- さらに `2-6. 起動と実証タスク green-keeper` / `2-7. 「検証可能なゴール」を持つループ — /goal という公式実装` も spot-check し、`desired / actual / drift / repair` の4項対応、PySide6 GUI / `term` 名残の補足、`/goal` の Haiku 既定・turn cap・直後の honest disclosure 節への橋渡しまで en/zh/ko が日本語正本に追従していることを確認した。
- さらに冒頭〜第1章前寄り（捨てた数字の導入 / `prompt → context → harness → loop` の階段 / automation と loop の差分 / Hashimoto 起点の `harness engineering` / OpenAI 403 に伴う二次情報ヘッジ / RAPTOR 二層構造の導入）も spot-check し、一次情報アンカー・二次情報ヘッジ・`Agent = Model + Harness` の注意書きまで en/zh/ko が日本語正本に追従していることを確認した。
  - ここでも確認したのは主に日本語正本に対する訳文追従であり、Hashimoto/OpenAI/Karpathy/RAPTOR の一次情報を各翻訳ターンで再取得したわけではない。
- さらに第2章前半の `llterm` 導入〜 MAPE-K 骨格（alpha 段階の honest disclosure / `MapeKRunner` の閉ループ / plan-execute-verify と Reflexion / 体温調節の比喩）も spot-check し、`llterm` の位置づけと MAPE-K の説明まで en/zh/ko が日本語正本に追従していることを確認した。
- さらに「捨てた数字」の独立 honest disclosure 節（arXiv `2605.18747` / `2605.27922` / `2605.26112`、`Bölük 10x` の否定、`GPT-5.5` 実在確認済み / 比較値の一次計測元・条件は未確認、一次と二次の線引き）も spot-check し、一次情報アンカーと二次情報ヘッジの書き分けまで en/zh/ko が日本語正本に追従していることを確認した。
  - ここでも確認したのは主に日本語正本に対する訳文追従であり、各論文やベンチの一次ページをこの翻訳監査ターンで再取得したわけではない。
- さらに第3章後半（RAD の運用ルール / `LLM Wiki` の 3 層 / thought circulation と Anti-Circulation Safeguards / RAPTOR の evidence ladder / `corpus-first advantage` / 統合章の A-B-C 表）も spot-check し、K² サイジング、`rad_prune.py` の dry-run、`39 documents / 12 clusters` 注記、llive の主観マッピング、`suspicion → patch_validated` の証拠段階、`47,097 docs` を含む統合表まで en/zh/ko が日本語正本に追従していることを確認した。
  - ここでも確認したのは主に日本語正本に対する訳文追従であり、Karpathy Gist / llive 要件 / RAPTOR 実装の一次情報をこの翻訳監査ターンで再取得したわけではない。
- さらに第3章の導入〜`3-2. LLM Wiki` 導入直前も spot-check し、3層スタックの説明、`RAD_INDEX.md` / `65 RAD corpora` の導入、`47,097 docs` と `32,503 files` の内訳、`hacker_corpus` の raw 集約ファイルという留保、Karpathy 帰属のヘッジ付き `LLM Wiki` 3層導入まで en/zh/ko が日本語正本に追従していることを確認した。
  - ここで確認したのは主に日本語正本に対する訳文追従であり、`RAD_INDEX.md` や Karpathy Gist の一次情報をこの翻訳監査ターンで再取得したわけではない。
- 追加 spot-check で、`3-2. LLM Wiki` 本体にある「半信×半疑」の引用ブロックと `alu.jp` URL が en/zh/ko で欠落していたことを確認し、日本語正本に合わせて補った。
  - この修正は factual 反転ではなく、引用ブロックと参照 URL の同期漏れを埋めるための translation drift 修正である。
- さらに末尾参考リストにも `Ud7lZLbei1F5xaFuAq3i` を同期し、新規ブロックの `Snack Bus-e / Forbidden Shibukawa (Alu)` 表記と埋込リンク形式を各翻訳ファイル内の既存引用スタイルへ揃えた。
- 続く追補で、未同期だった 4 件（`MDsuuBm0xXPgngwyQve0` / `2qlJjBwdpYGOVjBkyhhL` / `CPon283udq6PfvfKrxAP` / `H4Pix38XWLRS077emoZC`）も本文と末尾参考へ同期した。
  - crop URL 数は日本語正本 16 / en 16 / zh 16 / ko 16 に揃い、引用導線の非対称は解消した。
- その後の再監査で、`2qlJjBwdpYGOVjBkyhhL` は「未同期」ではなく、en/zh/ko で **`2-5` から第3章直前へ位置ずれした状態** だったことが分かった。現在は 3 言語とも `2-5` honest disclosure 末尾の本来位置へ戻し、第3章直前の誤配置は除去済み。
- 統合レビューで挙がった「翻訳版は blockquote 内 inline link / 正本は blockquote 下 raw URL」という形式差は、今回の修正で生じたものではなく同ファイル内の既存スタイル差でもあるため、actionable な修正指摘としては採らなかった。
- RAD 研究接地としては、`article_craft_corpus_v2` の narrative architecture / but-therefore rule / seeds of curiosity を再確認し、今回の監査対象も「and then」で列挙せず、章間の因果と橋渡し段の整合を優先して確認した。
- `alu.jp` crop URL 数の 16 本基準は、日本語正本を source of truth として **本文 8 本 + 参考節 8 本 = 計 16 本（unique は 8 本、各 URL が本文と参考で 2 回ずつ出現）** と確認したうえで、en/zh/ko も同じ構成かを照合した。
- `promise-progress-payoff` / `ending-payoff` の再確認では、終盤の `観察ベースの3点` → H4Pix 引用 → `まとめ：手綱と、輪と、知` の 3 箇条 → `Bölük` 数字を捨てた payoff 文 → `次回予告的な余韻` → 参考文献節、という鎖を 4 言語で突き合わせた。
- 2026-06-18 時点では、#43 en/zh/ko は handoff に列挙した主要帯に加え endmatter まで一巡し、「未確認の細い橋渡し段」や局所接続が本当に残っているかの最終棚卸しが残る、と整理していた。
- その後 2026-06-19 の seam spot-check と section fingerprint re-diff まで含めると、手元 handoff で再開候補になりやすい章境界の局所接続はほぼ一巡し、**local source 上の residual translation drift 監査は一旦クローズしてよい** 状態になった。現時点の #43 残件は、drift 修正そのものではなく、live draft / live URL 側未反映分と publish gate 管理である。
- さらに参考文献節と末尾注記（`/goal` docs、arXiv `2605.*` 群、RAPTOR upstream、自著関連記事、バス江引用、`secondary-only / primary unconfirmed` の列挙）も spot-check し、4 言語とも出典束と留保注記が日本語正本に追従していることを確認した。
- `loop_ledger` の恒久対策は commit `7745f84` で実施済み。`git rm --cached .llterm/loop_ledger.jsonl` と `.gitignore` 追記により、以後は tracked ノイズを発生させず local-only telemetry として保持する。
  - 運用ルール: `git add .` は引き続き避け、handoff は `git add docs/SESSION_SUMMARY.md docs/next_plan.md` のような名指し add に固定する。
- レビュー依頼時は、未 commit の `.llterm/loop_ledger.jsonl` ノイズ diff と commit 本体の docs diff を混ぜず、対象 commit の `git show` を優先提示する。
- `hedge retention audit` のような audit 系語は内部 handoff では問題ないが、外部公開文脈へ出す場合は records-retention 監査と誤読されないよう定義を添える。
- 公開済み英語版 Qiita item `2622da17495d61480fa2` のタイトル修正は完了した。なお live 反映確認は、このセッションで実行した API / HTML 自己確認ログに基づく。

## 次の具体的な一手

1. #43 en/zh/ko の次の再開点は、既に handoff に列挙済みの帯を機械的に再監査せず、handoff 上の seam 一巡で取りこぼしがないかを改めて疑うこと。2026-06-19 の section fingerprint ベース line 単位 re-diff では `paradigm_staircase.svg` 同期漏れ 1 件だけを拾って修正済みで、残差は段落結合差へ縮退した。したがって **local source 上の residual translation drift 監査は一旦クローズしてよく**、次にやるなら live draft を再開する直前の publish gate 管理と live 側未反映分の扱いである。
   - `2-7 → ★ honest disclosure`、`/goal` 節 → 独立 honest disclosure、`3-3 → 3-4`、統合章 → まとめ、まとめ → 次回予告 / 参考 は、少なくとも seam spot-check 一巡の確認済み候補として扱う。
   - 機械比較では本文構造の異常は見つかっておらず、直近の既知差は日本語正本先頭タグの `個人開発` と、`AIエージェント` ↔ `Agent` のローカライズ差である。line 単位 re-diff を切るなら、この metadata 差を除いた本文比較として扱う。
2. 新規の設計・実装・調査へ進む前に、必要な論点があれば RAD コーパスを grep して先行手法を確認する。
3. deindex 後の運用を維持し、review / handoff では `loop_ledger` を通常 diff に混ぜない。
4. `qiita46_llterm_supervision_first.md` は日本語草稿を第8章まで通し、休憩ポイント / 参考文献 / HTML annotation / `025.jpg` まで入った。`025.jpg` は言語ごとに作品名を localize しつつ raw URL の HTTP 200 も確認済み。`qiita46_llterm_supervision_first_kamikudaki.md` は磨き込み済み、さらに en/zh/ko draft も第8章と翻訳版 endmatter 一式まで同期した。最終見直しパスでも新たな重大 drift は未検出で、残る外部アクションは human-gate を伴う publish 判断が中心になった。
5. 難しい論点の Team stock 3 本は 2026-06-18 に Qiita Team へ POST 済みで、queue 正本へ item id / URL を記録した。API GET では 3 本とも `private:false`、未認証 HTML では Team Login redirect だったが、team-only と positively 確認できるまでは過剰露出の疑いを優先する。可視範囲是正（rollback / visibility tightening）が必要かどうかの判断待ち案件として current blocker に残す。
6. `NEXT_SESSION.md` の 2026-06-12 旧 operator セクションは stale 扱いを明示済みなので、asciinema 録画 / production 起動 / credential 復旧は現行の human-gate 外部アクションと混同しない。現行の未解決 human-gate 外部アクションは #46 publish 判断 / dev.to 英語版 update・publish 判断 / CTA-149 live 再 publish・PATCH 要否判断で読み、Team stock の可視範囲是正判断はこれとは別の current blocker として追う。
7. 新セッションの最初の具体的一手は、`docs/articles/2026-06-18/team_stock_queue.md` と `team_stock_publish_plan.md` を正本として開き、Team blocker の containment-first gate を再開すること。まず 3 本それぞれの intended state baseline を固定する。未認証 HTML GET / public direct probe で positive が出た記事は Team UI 完了を待たずその記事だけ fail-closed 候補へ送る。それ以外の記事について Team UI で intended share target / private state を read-only で確認し、既採取の Team API GET / 未認証 HTML GET / direct probe / source frontmatter と同ターンで 3 本ぶん突き合わせて、share target 起因 / private state 起因 / 未確定 を 1 行判定する。no-op retain は 1 回まで、時間上限は次回 human-gate までに留め、2 回目に入る前には暫定 private 化を含む fail-closed 分岐を human-gate に出す。opt-in PATCH (`--patch-group-url-name`) は UI で表現できない、または再現性ある API 経路を残す必要がある場合の診断後従属候補としてのみ扱い、既共有 item に対する締め直し効果は一次未確認という前提を崩さない。

- 翻訳 QA:
  - #46 多言語同期は、JA 原文を基準に各節を逐次照合し、`ctx 2549%` / `turn boundary` / `interrupt` / `block point` などの用語を訳語固定しながら反映している。
