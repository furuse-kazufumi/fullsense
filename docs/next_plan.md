# Next Plan

最終更新: 2026-06-19

## 現在地

- Qiita 草稿と handoff 文書の commit 記録ルール: `c37d084` までは連続列挙、それ以降は肥大化回避のため **範囲表記 + マイルストーン**で記録する。
- handoff 台帳は構造上、**最新 1 件の handoff commit を未反映のまま残すのが正常状態**である。自己増殖を避けるため、backfill は **実質的な handoff 更新を伴う commit に便乗してのみ**行い、台帳追記だけの単独 commit は原則作らない。例外標本は `a0b793a` / `6d9854d` / `c16a69b` / `e150ee4` / `ed1e841` で、いずれも standalone backfill debt の過去標本として扱う。以後は同型の commit を増やさず、cleanup が必要なら 1 行 note を積み増すのではなく、次の実質的 handoff 更新か別 human-gate 判断の中で 1 回で畳む。
- deindex は commit `7745f84`、記事シードのスクリーニングは commit `b4d1241` で確定済み。2026-06-19 の handoff / 草稿更新も commit `2a8b942` で確定し、次セッションはこの commit 境界を再開点として読めばよい。
- `.llterm/loop_ledger.jsonl` は deindex 実行済みで、以後は local-only telemetry として `.gitignore` 管理へ移行する。
- handoff 3 文書（`docs/NEXT_SESSION.md` / `docs/SESSION_SUMMARY.md` / `docs/next_plan.md`）は同じ handoff 群として追うが、**commit range 台帳の正本は `SESSION_SUMMARY.md` / `next_plan.md` の 2 枚だけ**である。`NEXT_SESSION.md` は後続の実質更新で別タイミングに進むため、直近更新 hash を range 注記へ固定しない。`NEXT_SESSION.md` の現在地は、このファイル群の commit range ではなく `NEXT_SESSION.md` 本文側の現況メモを正本として読む。
- git push は local-first 運用のため未実施のまま据え置いており、human-gate を要する外部アクション集合には数えない。一般 Qiita への新規 publish は未実施だが、Qiita Team stock 3 本の POST は 2026-06-18 に完了している。既存 public Qiita item `2622da17495d61480fa2` のタイトル修正 PATCH と `bf1cfe3b4f40b87f068d` の redirect 本文 PATCH だけ実施済み。
- Team 向けの難所 stock として、`team_stock_semantic_governance.md` / `team_stock_llm_wiki_anti_circulation.md` / `team_stock_ctx2549_postmortem.md` を local draft として追加し、2026-06-18 に Qiita Team `fullsense` へ POST 済み。item id は `6f67e54e538c10b8f1c3` / `b35b429dc6dc1fde207a` / `6fe79ab04443f7654eca` で、追跡先は `docs/articles/2026-06-18/team_stock_queue.md`。
- Team stock の公開順・human-gate 条件・rollback 注意の正本は `docs/articles/2026-06-18/team_stock_publish_plan.md`。投稿待ち一覧の正本は `docs/articles/2026-06-18/team_stock_queue.md`。
- Team stock 正本 2 枚には preflight runbook / 実行コマンド / rollback notes / POST 後の記録欄まで追加済み。通常 POST はその 2 枚で回せるが、rollback 実施時のみ handoff にも 1 行転記する。
- 2026-06-18 の human-gate 回答では「3 本すべて POSTする」を採用した。実行順は publish plan の推奨どおり `team_stock_semantic_governance.md` → `team_stock_llm_wiki_anti_circulation.md` → `team_stock_ctx2549_postmortem.md` とし、POST 前に `verify` と 3 本の `dry-run` を再実行する。POST 後は `team_stock_queue.md` の `status / item id / Team URL / visible range memo / rollback needed / note` を即時更新し、可視範囲が想定より広い場合は rollback runbook に従って差し替え判断へ移る。
- 実行結果として、3 本とも 201 Created で item 作成に成功した。POST 後の API GET では 3 本とも `private:false` で返っており、frontmatter `private:true` は Team create 後の可視範囲を保証しなかった。さらに 2026-06-19 12:41:22 +09:00 の未認証 HTML GET では 3 本とも Team URL に対して `302` / `Location: /login?redirect_to=...` が返った。
- ただしこの Login redirect は「匿名ブラウザで即読めない」ことしか示さず、**team-only と positively 確認できるまでは過剰露出の疑いを優先**する。`private:false` の意味づけ自体も一次情報待ちで、ここで言う `visibility semantics` は **プロジェクト内用語**に留まる。なお `https://qiita.com/furuse-kazufumi/items/<id>` の direct probe は 3 本とも `404` だったが、これは Team scope item なら team-only / 過剰露出のどちらでも起こりうるため、over-exposure 判定の弁別力は無い。今回 probe した 3 本について、同時点で public 側の対応記事を直URLでは確認できなかった、という記録に留める。
- 追加で、同じ API GET は 3 本とも `group.url_name: general` / `group.private:false` / `organization_url_name:null` を返した。2026-06-18 の Team poster payload では `group_url_name` を明示していなかったため、現在の仮説は **implicit General sharing** である。ただしこれは root-cause 仮説であって、team-only の証明でも否定でもない。local source にはこの観測値を resend default として固定せず、将来 create は explicit target を再判断する。2026-06-19 の hardening では、既存 item の PATCH でも `group_url_name` を既定送信しないことを `tests/test_qiita_frontmatter.py` で固定し、観測された `general` を通常更新で再宣言しない状態へ揃えた（2026-06-19 再実行で `91 passed`）。その反面、**current blocker の 3 本を狭い共有先へ寄せ直す remediation は、このツールの既定 PATCH 経路だけでは実施できない**。是正が必要なら Team UI か、`id` あり更新でも `group_url_name` を明示送信できる別改修が要る。
- 2026-06-19 の続きで、上記の「別改修」をローカルで実装した。`tools/qiita_team_post.py` は **既定 PATCH を維持したまま** `--patch-group-url-name` を付けたときだけ `group_url_name` を再送できる。これは **共有先 (`group_url_name`) を寄せ直すための opt-in 経路**であり、`private` 範囲の tightening そのものではない。dry-run でも `private` は frontmatter 値を再送する旨を明示する。現在の 3 本は source が `private:false` のため、この経路だけでは露出疑いを縮めず、`private:true` へ直す別アクションが要る
- Qiita API docs の `PATCH /api/v2/items/:item_id` に `group_url_name` 記載がある**可能性**はあるが、この点自体は現時点で一次未確認である。したがって現状ここで確定しているのは、ローカル実装として resend 経路を持たせたことだけであり、**既共有 item に対し、この PATCH が実際に共有先や可視範囲を締め直す効果を持つかは一次未確認**のまま扱う
- 従って current blocker の次の候補は `Team UI` か `human-gate 後の opt-in PATCH` の二択まで狭まったが、後者を「visibility 是正が実証済み」とは扱わない。frontmatter に concrete target が無い PATCH は fail-closed で停止する
- 2026-06-19 のローカル再確認では、Team stock 3 本の source frontmatter にはまだ `group_url_name` が無く、`py -3.11 tools/qiita_team_post.py dry-run <file> --patch-group-url-name` は 3 本とも `PATCH_GROUP_URL_NAME_BLOCK` で停止した。したがって opt-in PATCH 経路は実装済みだが、**human が concrete target を決めて source に入れるまでは実行不能**である
- 実行順の判断としては、**外部 remediation の first choice は Team UI** に置く。理由は、opt-in PATCH は `group_url_name` 再送のローカル経路までは実装済みでも、既共有 item に対する締め直し効果が一次未確認だからである。したがって次の human-gate は、(1) Team UI で intended share target / private state を確認・是正できるかを先に見る、(2) UI で表現できない、または再現性ある API 経路を残す必要がある場合だけ、concrete group_url_name を source に入れた opt-in PATCH を検討する、の順で扱う
- この段階で `general` を local source へ焼き戻すことはしない。理由は、観測値を resend default に固定しないという current rule を保つためである
- 2026-06-19 の最終到達点として、`#37` short companion の public PATCH は完了済みで、`tests/test_qiita_frontmatter.py` は再実行で `91 passed` だった。本差分の docs / tests / tools 更新が残っているため worktree は clean ではない。従って次セッションの主対象は `#37` ではなく、**Qiita Team 3 本の visibility blocker** のみで読む。
- handoff 系 docs のテスト件数は、今回の更新で **`76 passed` → `91 passed`** へ同期した。`docs/articles/2026-05-23/INTEGRATION_AUDIT.md` にある `88 passed` は別文脈の過去監査記録であり、今回の同期対象には含めていない
- 2026-06-19 に `tests/test_qiita_frontmatter.py` へ `qiita_team_post.py` の回帰も追加し、`real_id` の nullish fallback、frontmatter `private: false` の文字列パース経路、そして **空 `private:` は default=True へ倒す**修正まで固定した。したがって Team stock 3 本の `private:false` incident は、少なくとも現在の Team poster 実装では再現しない層のバグとして切り分けられるが、だからといって可視範囲の疑いが解消したとは扱わない。
- さらに Team poster の `ignorePublish` gate も 2026-06-19 に fail-closed 化し、`dry-run` でも不正値や key typo を exit 非 0 で返すようにした。したがって `ignorePublish:true` / `--force-ignore-publish` の扱いは public poster と同じく **明示 override 前提**へ揃っている。
- Team stock 3 本は source article と大筋整合していることを spot-check 済み。対応は `team_stock_semantic_governance.md` / `team_stock_llm_wiki_anti_circulation.md` = #43、`team_stock_ctx2549_postmortem.md` = #46。公開前の読みやすさだけ先に上げるため、3 本とも冒頭へ `前提 / 流れ / ゴール` の 3 点ボックスを追加した。
- Team stock 3 本には `この記事で話さないこと` も追加し、難所の切り出し範囲を local draft の段階で固定した。
- Team stock 3 本の source anchor も明記し、#43 `2-2. loop engineering にもセキュリティの顔がある` / #43 `3-2. LLM Wiki — 「育つ知識」のパターン` / #46 `2. ターン境界と緊急割り込みは、最初から別物として設計する / 3. ctx 2549% は「AI が太った」のではなく、計測が壊れていた / 6. テストも「たまたま緑」を疑う` のどこから切り出したかを queue で追えるようにした。
- local draft 側の `この草稿の位置づけ` / `source` でも、#43 `3-2. LLM Wiki — 「育つ知識」のパターン` と #46 `2 / 3 / 6` の実見出し粒度まで揃え、queue 正本と同じ anchor で辿れる状態にした。
- さらに後続の整合確認で、`team_stock_queue.md` / `team_stock_publish_plan.md` / local source 3 本の title・source anchor・現在の frontmatter mirror（`private:false` / `public_private:false` / `ignorePublish:true` / `id:`）は相互に矛盾していないことを再確認した。`semantic_governance` は #43 `2-2`、`llm_wiki_anti_circulation` は #43 `3-2`、`ctx2549_postmortem` は #46 `2 / 3 / 6` の切り出しとして queue 記述と draft 本文が揃っている。
- `team_stock_ctx2549_postmortem.md` の `source` 行に残っていた `ctx 2549%` のネスト backtick も外し、queue 正本と同じ inner-backtick 無し表記へ揃えた。
- さらに source article 本文との一次突合も回し、`Semantic Governance` は #43 `2-2` の Verloy / Semantic Governance / fail-closed 橋渡し束、`LLM Wiki` は #43 `3-2` の 3 層 / thought circulation / safeguards 束、`ctx2549` postmortem は #46 `2 / 3 / 6` の incident 束を基準に local draft が切り出し範囲から外れていないことを spot-check 済み。
- Team stock 3 本の local draft `source` 節にも、その「切り出しの核」（Verloy / Semantic Governance / fail-closed、3 層 / thought circulation / safeguards、turn boundary / ctx2549 / block point）を明記し、anchor だけでなく論点束でも原典追跡できるようにした。
- `team_stock_semantic_governance.md` の `切り出しの核` では、原典追跡精度を優先して `意味管理` ではなく `意味論的ガバナンス（Semantic Governance）` の語へ寄せた。
- #43 companion の `qiita43_harness_loop_stack_kamikudaki.md` も full article と一次突合し、`RAPTOR / llterm / RAD` の 3 点構造、`手綱 / 輪 / 知識基盤` の圧縮軸、`AI 本体より器と回し方を設計する時代` という結論が current naming / current hedge に追従していることを確認した。
- そのうえで `qiita43_harness_loop_stack_kamikudaki.md` の `llterm` 初出には、完全版の温度感に合わせて「まだ試作段階のスケルトン」という短い alpha 留保も補った。
- `qiita45_human_ai_dev_incident_patterns.md` は publish gate 前の local polish として、本文と図の `human gate` / `Human Gate` 表記を `human-gate` へ統一し、`外部書き込み` も現行 handoff と同じ `外部アクション` の語へ置き換えた。主張や gate 条件は変えず、運用語だけ現行版へ揃えた。
- さらに `qiita45_human_ai_dev_incident_patterns.md` の appendix / 参考節には、`VLAA-GUI` / `Resilient Write` / `Crab` / `Measuring the Permission Gate` の 4 本を近い実名ソースとして追加した。`unsupported success` / `human-gate` / `verifier` / `durable write` / `checkpoint` 自体は内製ラベルのまま維持し、実名ソースは「外部系統メモ」として対応づける形に留めた。
- 上記 4 本の arXiv 引用は実在確認済みで、`2604.21375` / `2604.10842` / `2604.28138` / `2604.04978` を一次情報アンカーとして handoff に明示した。
- 続く local polish では、`qiita45_human_ai_dev_incident_patterns.md` の `## 2` にある honest disclosure 前置きを 1 パス圧縮し、main path には「ローカル再集計値」「内製ラベル」「appendix の 4 本実名ソース対応」だけを残した。appendix 参照の重複説明は削り、接地メモとしての機能を先頭で言い切る形へ寄せた。
- 別パスで `qiita47_harness_engineering_thoughts.md` の 0〜4 章も軽く圧縮し、列挙で分散していた「人間側の揺れ」説明と、`AI のための discipline` / `人間のための discipline` の二重言い換えを畳んだ。主張は変えず、前半の spine を「ハーネスは人間側の雑さを通さない器」へ寄せている。
- さらに `qiita47_harness_engineering_thoughts.md` の forward bridge 3 箇所も `次は...` の定型から少し崩し、接続を保ったまま機械的な反復を弱めた。
- 追加の軽微修正では、`qiita47_harness_engineering_thoughts.md` の §0 だけは bullet の走査性を優先して 4 項目列挙を復元し、§5→6 ブリッジも見出しの `PoC` 反復と近接しすぎない言い回しへ戻した。`qiita45_human_ai_dev_incident_patterns.md` の対応表では `human-gate / permission boundary` 行を `(補助線)` と明示し、本文の主従と揃えた。
- 続く micro-polish では、`qiita45_human_ai_dev_incident_patterns.md` の `研究側で特に近い型` / `要するに` 周辺も 1 パスだけ削り、main path が「4 類型を持ち帰る段」だと読み取りやすい粒度へ揃えた。
- その後、`qiita45_human_ai_dev_incident_patterns.md` の前半にも `handoff / human-gate / diff / checkpoint` は**運用上の持ち帰りカテゴリ**、後段の `4+1` は RAD 接地の**分析レイヤ**だと 1 文だけ足し、taxonomy の切替点を本文前半で先に見えるようにした。
- `qiita45 + handoff sync` と前ターンからの `qiita43 en/zh/ko` / `qiita44` / `qiita47` 差分は、commit `2a8b942` として一体で確定した。handoff は `qiita45` micro-polish 単体ではなく、この bundled commit 全体を前提に読む。
- さらに `qiita45_human_ai_dev_incident_patterns.md` の `## 2` では、`ローカルコーパス要約の上でも` を `ローカルコーパス要約でも` に縮め、`要するに本稿の main path で持ち帰りたいのは` も `要するに持ち帰りたいのは` へ詰めて、説明口調だけを少し落とした。
- 最後の micro-polish では、`qiita45_human_ai_dev_incident_patterns.md` の `## 2` 冒頭にあった 2 文切りの導入も 1 段へ畳み、main path の論点に入るまでの助走をさらに短くした。
- 追加確認として、`VLAA-GUI` / `Resilient Write` / `Crab` / `Measuring the Permission Gate` の arXiv 4 件は 2026-06-19 に一次情報で URL / title / author を照合済みだと本文へ固定した。あわせて `5 点` は運用カテゴリ、`4+1` は RAD 接地の分析レイヤだと 1 行で明示し、taxonomy の切替が誤読されにくい形へ揃えた。
- `qiita47_harness_engineering_thoughts.md` は `#43` から派生した **independent short draft** として維持する方針に決めた。`006.jpg` を「賢そうに見える瞬間」、`157.jpg` を「しつけが必要なのは人類側」という反転オチへ役割分担させたうえで、冒頭には `前提 / 流れ / ゴール` の 3 点契約と「この短稿で話さないこと」も置いた。（本プロジェクトでの）RAPTOR / `llterm` / Claude Code 公式 `/goal` まで引いて「何を harness に入れるのか」「何を PoC したのか」の具体節と最小の参考導線を追加済み。ここでの RAPTOR は 判断層と実行層を分けた二層 runtime、`llterm` は terminal 起点の名残を名前に残した PySide6 GUI 実装だと最小グロスも補った。参照ブロックの二重化も解消し、`desired / actual / drift / repair` の 4 点で読む最小アルゴリズム節、`green-keeper` 的な **いちばん小さい具体例**、その比喩が clean / dirty の観測までしか言い切れずズレの意味づけや優先順位づけは自動化しないという破綻点、harness を強くしすぎると `desired` の狭めすぎ / proxy の本体視 / drift の過剰検知 / repair の硬直化を招く failure mode、「明日 1 個だけ変えるなら何を loop に載せるか」、さらに「何を runtime に入れず人間へ残すか」、runtime を **観測 → 停止 → 修復 → 意味づけ** の順で育てる実務ルール、最後の `意味づけ` だけは runtime に載せず人間へ残すという境界、`しつけ` 比喩が効くのはせいぜい `観測 / 停止 / 修復` の前半までだという seam、そして runtime に入れる前に先に捨てるべき人間側の癖（後付け説明 / proxy の本体視 / 例外の雑な一般化）まで含めて、短稿段階でも「何を loop として固定したいのか」と「何をまだ runtime に入れず人間へ残すのか」が分かる形まで進めた。さらに 2026-06-19 の local polish では、§4→5 / §5→6 / §8→9 / §11→12 に短い forward bridge を足し、§13 には「比喩で写すのは反復で振る舞いを固定する関係だけで、感情や忠誠の表面属性ではない」という break-point 明示を追加した。続く圧縮 pass では、RAD の controlling idea / clutter-cut 基準に寄せて、導入の言い換え、PoC 節の冗長説明、runtime 境界まわりの重複を少し削り、spine を「AI を賢くする技術より、人間側の曖昧さを通さない discipline」へさらに寄せた。補助導線の外部 2 本も Distill `Research Debt` と Mitchell Hashimoto `My AI Adoption Journey` の実 URL へ揃えた。**現時点の具体状態**は、runtime の射程と人間残置の境界、比喩の破綻点、短稿で扱わない範囲まで明示した local-only draft で、最新 commit `44ed5af` は ledger 未反映の最新 1 件として残っているのが正常状態である。
- 同じ変更範囲で、`qiita43_harness_loop_stack_en.md` / `_zh.md` / `_ko.md` の `### prompt → context → harness → loop の流れ` に `paradigm_staircase.svg` と caption を同期し、#43 local source residual translation drift 監査を一旦クローズしてよいとした根拠差分を translations 3 本へ固定した。
- さらに `qiita44_evolutionary_programs_block_diagram.md` の MIT Press gate staging comment も `soft-gate` と `別 UI / 別ブラウザ経由の補助観測` へ揃え、到達性 hedge の実差分を本文側へ残した。
- `qiita37_gpu_triple_run_gate_price_kamikudaki.md` は、短すぎてアルゴリズム / PoC の層が見えないという指摘を受けて増補した。`1 分version` と比喩パートの間に、**「実験 3 本の中身」**（HD-1 full / HD-1 null / Stage-B）と **「AI が裏で何を自走したか」**（pre-registration / attacker AI 3 体 / major 5 件修正 / Kaggle T4 / 152 runs / `$0`）の 2 節を戻し、完全版の骨格を壊さず plain-language で厚みを出した。
- 2026-06-19 の方針追加として、「**公開済みの短い companion 記事は、十分に長い本編へ統合できるなら統合を優先し、空いた item は新記事の器として再利用する**」を採用する。ただし `#37` は、核説明 (`4 文指示 / 実験 3 本 / PoC 裏方 / 17〜19 倍 / 0 円 / safety tax 本文接続`) は完全版へ吸収済みでも、**EN/ZH/KO 多言語スイッチャーと curated 関連ニュース節は未吸収**なので、即 redirect せず本文保全を優先する。
- あわせて、`qiita43/46/47` に対する現在の変更は **local source の内部 polish のみ**で、外部 publish / PATCH / 統合実行は #37 の判断とは別件・未着手のまま切り分けて扱う。
- 前提確認として、`qiita37_gpu_triple_run_gate_price_kamikudaki.md` は front matter 上 `private:false` / `id:f06ca92ea208c7646fcd` で、Qiita live HTML / API も 2026-06-19 に `200` を返した。`qiita43_harness_loop_stack_kamikudaki.md` / `qiita46_llterm_supervision_first_kamikudaki.md` / `qiita47_harness_engineering_thoughts.md` は front matter 上 `private:true` / `ignorePublish:true` の local draft である。
- ただし `#37` には local representation が 2 本ある。public short companion の更新対象は `tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md` (`id:f06ca92ea208c7646fcd`) で、`docs/articles/QIITA_#37_gpu_triple_run_gate_price_kamikudaki.md` は `id:df687d0ecddb56d5a373` / `qiita_public_id:f06ca92ea208c7646fcd` を持つ **多言語アーカイブ / Team mirror** として分けて扱う。
- `#37` の本文比較まで進めると、短稿側の核だった `指示 4 文 / 実験 3 本の役割分担 / PoC 裏方 / 17〜19 倍 / 0 円 / safety tax 接続` は完全版へ吸収済みだが、**完全版側の full-article-pending switcher（EN/ZH/KO 導線）と curated 関連ニュース節は未吸収**だった。したがって現時点の推奨実行案は redirect ではなく、**短稿本文を残したまま冒頭に canonical 告知だけを足す**形になる。
- local source 側では、この保全案に沿って `qiita37_gpu_triple_run_gate_price_kamikudaki.md` を本文保全版へ戻し、冒頭に canonical 告知を追加した。front matter `ignorePublish` は **qiita-cli 系の一括 publish を止めるため** `true` のまま維持し、2026-06-19 に live item `f06ca92ea208c7646fcd` へ `post --yes --force-ignore-publish` を実行して PATCH まで完了した。
- `.remote/f06ca92ea208c7646fcd.md` と現行 local source の再 diff も 2026-06-19 に取り直し、**companion-preserved switcher（EN/ZH/KO 導線）** とマスコット画像 + 📗導入の live-only 2 ブロックはすでに local source 側へ保全済みだと再確認した。現時点の主要差分は canonical 告知ブロックと `実験 3 本` / `AI は裏で何を自走したのか` の補足節である。
- ここで使う `ignorePublish` は Qiita 標準属性ではなく、`qiita-cli-poc` ローカル運用の publish 安全柵である。`tools/qiita_public_post.py` もこれを読み、`ignorePublish:true` の source は **`--force-ignore-publish` が無い限り fail-closed で BLOCK** する。したがってこのポスター経路の実ゲートは **`ignorePublish` override gate（`--force-ignore-publish` 必須）+ `post <file> --yes` + human-gate 承認** である。ただし live PATCH 経路で `--force-ignore-publish` を付ける時点で、この柵そのものは override 済みなので、**実保護は human-gate と step3 の本文 word-diff 目視と preflight** にある。この override は今回の `#37` companion PATCH 限定で、他ファイルへコピペ流用しない。また「redirect」は HTTP 転送ではなく、Qiita 本文を統合告知 + canonical 誘導へ差し替える運用語として使う。
- `tools/qiita_public_post.py` は filename ではなく frontmatter `public_id` を冪等キーにして public PATCH/POST を分ける。したがって PATCH 直前に確認すべきは custom 名そのものではなく、`tools/.../qiita37_gpu_triple_run_gate_price_kamikudaki.md` が正しい `public_id` を持つ更新対象 source だという点である。
- その確認も先回りで済ませ、`tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price_kamikudaki.md` に `public_id:f06ca92ea208c7646fcd` を追記した。これで public poster の dry-run でも `PATCH update public_id=f06ca92ea208c7646fcd` と読める。
- 完全版 source `tools/qiita-cli-poc/public/qiita37_gpu_triple_run_gate_price.md` にも `public_id: 6f44575d440a9ebf5228` を追記し、完全版側を触る場合も accidental create ではなく PATCH update へ入る前提を揃えた。
- `qiita_public_post.py` の frontmatter `private:` はこの public poster では payload に使われない。可視性の既定値は frontmatter **`public_private:`** で与え、**CLI の `--private` はそれを強制 override** する。`#37` companion の live 更新は一般公開 PATCH を前提に読み、ここでは `public_private` 既定 false / `--private` なしを使う。
- 2026-06-19 の hardening で、`qiita_public_post.py` は `private:` だけがあり `public_private:` が無い source、または両者が矛盾する source を **fail-closed で拒否**するようにした。`#37` source には `public_private: false` を明示済みである。
- さらに `public_private` の値も strict parse に切り替え、未認識値は一般公開へ黙落ちさせず BLOCK する。bulk 移行として `tools/qiita-cli-poc/public/*.md` の `private:` 単独 69 件へ `public_private:` を機械追加し、`public_id` を持つ PATCH 対象は 2026-06-19 時点で欠落 0 件まで戻した。
- 2026-06-19 の追加 hardening で、tag drift 比較は case-insensitive のまま維持しつつ、**送信 payload のタグ表記は frontmatter 原文の大小文字を保持**するよう修正した。これで `AI` / `FullSense` が live PATCH 時に `ai` / `fullsense` へ壊れる回帰を防ぎ、`TODO_TAG` プレースホルダも payload から除外する。
- human-gate 後に実行へ進むときは、`https://qiita.com/furuse-kazufumi/items/f06ca92ea208c7646fcd` をブラウザで開き、表示されている live item が **完全版 `6f44575d440a9ebf5228` ではなく short companion 本文**だと目視確認してから `post ... --yes --force-ignore-publish` を打つ。dry-run は network なしなので、この確認を `public_id` 取り違え防止の最終ゲートとする。
- さらに `tests/test_qiita_frontmatter.py` に最小回帰テストを追加し、`qiita_public_post.py` が **`public_id` を PATCH キーとして使い、`id` だけでは POST create 扱い**になることと、frontmatter `private:` ではなく `public_private` / CLI `--private` だけが公開可視性を切り替えることを固定した。
- safety polish として、`qiita_public_post.py` は **`id` はあるが `public_id` が無い** source を dry-run したとき warning を出し、実 `post --yes` では **`--allow-create` が無い限り fail-closed で停止**する。これは初回 public 化でも起こりうる正常 warning / gate で、`public_id` は Qiita API の公式 frontmatter 名ではなく **このラッパーの PATCH 識別子**である。`#37` companion は `public_id` 付きなのでこの gate に掛からない。
- `#37` live PATCH の human-gate 後 runbook も固定済みで、`preflight --refresh-baseline` → `baseline 退避` → `prepatch baseline との本文 diff` → `f06ca92...` live item 目視 → `post ... --yes --force-ignore-publish` → `preflight --require-marker` + 目視、の 6 段で実行する。ここで言う `preflight` は CORS の OPTIONS ではなく、**このラッパー独自の pre-patch health check** である。今回の `#37` companion source は 2026-06-19 時点で **既存行の順序保存・非削除・非改変**を前提に hardening しているため、step1 の `preflight --refresh-baseline` で live API 本文を `.remote/f06ca92ea208c7646fcd.md` に再取得し、step2 でその refresh 後 baseline を `f06ca92ea208c7646fcd.prepatch.md` へ退避する。承認者は step3 の `git diff --no-index --word-diff=color ...prepatch.md ...kamikudaki.md` を監査証跡として見る。baseline refresh は **live title / visibility / tags / URL / HTML 到達性が payload と整合したときだけ** `.remote` を atomic に更新し、不一致なら fail-closed で baseline を書き換えない。さらに `--refresh-baseline` は `public_id:` と `preflight_remote_baseline:` の両方が無いと no-op ではなく fail-closed で止まり、baseline write の OSError も `BLOCKED` 扱いで返す。step1 の preflight 出力では `asset_count: 3` だけでなく、`kamikudaki_shishi.svg` / `191.jpg` / `192.jpg` の 3 件すべてが `content-type=image/...` で返っていること、`baseline_refresh_tags` / `baseline_tags` / `api_tags` が `['ai', 'fullsense', 'llcore', 'かみくだき', '機械学習']` で一致していることも確認する。step3 では companion-preserved switcher とマスコット画像 + 📗導入を含む本文が保全されていること、frontmatter `tags:` 行が drift していないこと、かつ既存行に削除・改変が無いことを確認する。新規行は中間挿入でも機械ゲートを通りうるので、承認者がこの word-diff 出力を目視し、挿入位置まで精査することを human-gate の必須条件とする。step5 の `post ... --yes --force-ignore-publish` も送信前に preflight 相当（auth / live title / live visibility / live tags / asset / marker 非要求）を再評価し、未通過なら fail-closed で止まる。現行設計では **live tags ≠ payload tags の既存 public 記事 PATCH も BLOCK** するため、将来タグ編集を伴う PATCH を通すには別の explicit override 方針が要る。step1〜step5 の間に時間が空く、または live を別 UI で触った疑いがある場合は step1 からやり直す。step6 では `marker_present: True` と canonical 告知反映 / item id 不変に加えて `kamikudaki_shishi.svg` を含む live SVG / 画像描画と多言語導線 `bdfad6db3f2e70c40511` / `fa0890f136636d495ea6` / `e5093e4816b25c1bd4d0` の到達性も目視確認し、Qiita / imgix 側キャッシュで古い描画が残る場合は `?v=20260619N` cache-bust を足して source を更新し、step1 から runbook をやり直して再 publish する。publish 直後に `marker_present: False` が一過性で出る場合は即失敗扱いせず、少し待って再確認する。もし `marker_present: False` が継続する場合は、Qiita API の live body でも marker 文字列が見えるかを確認し、HTML 側の整形差か本文未反映かを切り分けてから失敗判定する。`#37` source は `public_id` 付きなので `--allow-create` は不要。
- 2026-06-19 現在、`#37` short companion の live 更新に関する local blocker は解消済みで、append-only runbook hardening の節目は commit `1b98fc0`（`tighten qiita append-only patch runbook`）で確定している。`#37` companion の public PATCH は **:70 のとおり完了済み**で、以後の残件は別系統のみである。`#46` / dev.to / CTA-149 / Team 可視範囲是正は `#37` PATCH 完了扱いではなく別管理の残件とする。
- 2026-06-19 の human-gate 選択では、`#37` short companion は **本文保全版で PATCH する**方針を採用した。実行時は runbook の step1〜6 を順番どおりに回し、step3 の word-diff 目視と step4 の live 本文目視を人間が通した後にだけ step5 `post --yes --force-ignore-publish` へ進む。
- 実行結果として、2026-06-19 に `py -3.11 tools/qiita_public_post.py preflight ... --refresh-baseline` は `baseline_body_preserved: True` / `baseline_tags_match: True` / `preflight: OK`、`py -3.11 -m pytest tests/test_qiita_frontmatter.py` は `64 passed`、`py -3.11 tools/qiita_public_post.py post ... --yes --force-ignore-publish` は `OK (200) [PUBLIC(一般公開)]` で通過した。直後の `preflight --require-marker` も `marker_present: True` / `preflight: OK`、live HTML でも canonical id `6f44575d440a9ebf5228` と多言語導線 3 本を確認済みである。したがって `#37` short companion の public PATCH は完了し、残件は **Qiita Team 3 本の `private:false` 着地問題**を主とする別系統のみへ戻った。
- なお `.remote/f06ca92ea208c7646fcd.md` と `f06ca92ea208c7646fcd.prepatch.md` は `.gitignore` 対象の監査補助物で、repo 単独では再検証できず、将来の `--refresh-baseline` で上書きされうる ephemeral 証跡である。必要なら同じ runbook を step1 から再実行して再採取する。
- step4 は short companion 本文の同一性確認だけでなく、**PATCH が source からの title / tags / body 全置換**である以上、live-only 編集を失ってよいかを確認する gate として扱う。
- pre-patch baseline も 2026-06-19 に読み取り専用で取り直し、`preflight` は `PATCH update public_id=f06ca92...` / `ignorePublish` warning（expected） / `private: False` / `auth_status: 200` / `api_status: 200` / `api_private: False` / `api_tags:['ai','fullsense','llcore','かみくだき','機械学習']` / `html_status: 200` / `marker_present: False` / `asset_count: 3` / `preflight: OK` を返した。`baseline_refresh_tags` / `baseline_tags` も同一集合で一致している。
- baseline の asset 対象も `kamikudaki_shishi.svg` だけでなく `191.jpg` / `192.jpg` へ広げ、3 件とも raw `200` を確認済みである。raw asset URL は `origin/main` を解決するが、local `main` が `origin/main` より 263 commits ahead でも今回参照する 3 asset は remote `main` 側で `200` を返すため runbook に影響しない。
- 未吸収 2 ブロック（多言語スイッチャー / curated 関連ニュース節）は完全版 `6f44575d440a9ebf5228` 側の将来課題であり、short companion 側の欠落ではない。したがって live PATCH option 1 は companion 本文保全のまま canonical 告知を反映する線として扱う。
- このターンで言う RAD grounding は、主に `D:/docs/loop_engineering_corpus_v2/` の `fail-closed`, `human_in_the_loop_approval_gate`, `progressive_delivery_canary_metric_gate` と `D:/docs/article_craft_corpus_v2/136_ablations_baselines_as_honesty_*.md` を指す。
- `ac398349ec42e40913f1.md` と `docs/articles/QIITA_SERIES_INDEX.md` の #37 導線も `canonical / companion` 表記へ更新済みで、local index 上では完全版を正本、かみくだき版を companion として扱う。
- #43 の `2-6. 起動と実証タスク green-keeper` / `2-7. 「検証可能なゴール」を持つループ — /goal という公式実装` も 4 言語で spot-check し、`desired / actual / drift / repair` の対応、PySide6 GUI / `term` 名残の補足、Haiku 既定と turn cap を含む `/goal` 説明、直後の「捨てた数字」節への橋渡しまで日本語正本に追従していることを確認した。
- 追加 spot-check で、`2-5` honest disclosure 末尾の `2qlJjBwdpYGOVjBkyhhL` 引用が en/zh/ko では第3章直前へ誤配置されていたことを確認した。translations 側は誤配置ブロックを除去し、`2-5` 末尾の本来位置へ戻した。末尾参考の URL 自体は維持している。
- さらに `1-4` 後半の `AI成長マネジメント` / 4理由 / `First, Break All the Rules` ヘッジ / `アンチパターン` / 第2章への橋渡しも 4 言語で spot-check し、日本語正本に対する新たな factual / translation drift は見当たらないことを確認した。
- さらに終盤の `なぜ「手綱を握るのは人間」だと言えるのか — 観察ベースの3点` から、H4Pix 引用を挟んだ結語導入まで 4 言語で spot-check し、`常時並列 / 長射程の伏線回収 / 常時稼働の危険予知` の 3 点、`観察された傾向` というヘッジ、`ルール（構造）で縛る` への橋渡しまで日本語正本に追従していることを確認した。
- さらに参考文献節と末尾 hedge note も 4 言語で spot-check し、`alu.jp` crop URL 数は日本語正本 16 / en 16 / zh 16 / ko 16 に維持され、OpenAI 403 / RAD `47,097 docs` / `人間優位3点` 観察ベースなどの留保も日本語正本に追従していることを確認した。`GPT-5.5` についてはこのターンで OpenAI 公式一次情報によりモデル名の実在を確認し、留保を「モデル名未確認」から「比較値の一次計測元・計測条件未確認」へ締め直した。
- 残ブリッジ棚卸しとして、`第1章末 → 第2章頭`（`なぜ` → `どう` への橋渡し）、`3-1. RAD コーパス → 3-2. LLM Wiki`、`3-4. corpus-first advantage → 統合章` の 3 接続も 4 言語で再確認した。第1章の補助線から第2章の制御論へ移る温度感、`集めた知識は放っておくとただの山` から LLM Wiki へ入る導入、`A/B/C が1本に繋がる` から統合章へ畳む着地まで、日本語正本に対する新たな factual / translation drift は見つかっていない。
- さらに最終棚卸しとして、導入 → 第0章、第0章末 → 第1章頭、`/goal` 節 → 独立 honest disclosure、独立 honest disclosure → 第3章頭、`3-2. LLM Wiki` → `3-3. RAPTOR` の局所接続も 4 言語で spot-check した。一次情報に錨を下ろす作法から用語地図へ入る導入、`実務ブログも査読論文も鵜呑みにしない` から harness engineering の命名確認へ移る接続、`mystery graph` から `捨てた数字` 検証へ降りる橋、`無知の知` から knowledge stack へ移る着地、thought circulation 警告から RAPTOR の evidence ladder へ渡す流れまで、日本語正本に対する新たな factual / translation drift は見つかっていない。
- さらに、まだ handoff に明示していなかった seam として、`2-7. /goal` → ★ honest disclosure 節、`3-3. RAPTOR` → `3-4. corpus-first advantage`、統合章 → まとめ、まとめ → 次回予告 / 参考 も 4 言語で spot-check した。`検証可能なゴール` から `捨てた数字` 実演へ落とす open loop、evidence ladder から corpus-first の条件付き優位へ渡す橋、A/B/C 統合から `手綱 / 輪 / 知` の3点要約へ畳む順序、次回予告と参考節で閉じる終盤構造まで、日本語正本に対する新たな factual / translation drift は見つかっていない。
- 上記までで、handoff がこれまで再開候補として列挙してきた #43 の seam 範囲は一巡した。少なくとも `導入 → 第0章`、`第0章末 → 第1章頭`、`第1章末 → 第2章頭`、`2-7 → ★ honest disclosure`、`/goal` 節 → 独立 honest disclosure、独立 honest disclosure → 第3章頭、`3-1 → 3-2`、`3-2 → 3-3`、`3-3 → 3-4`、`3-4 → 統合章`、統合章 → まとめ、まとめ → 次回予告 / 参考 は 4 言語で spot-check 済みである。ただし、新規 seam 候補の網羅までは保証しない。
- この seam spot-check の最小根跡として、確認観点は `ja/en/zh/ko` 4 言語の見出し語順、★/独立 honest disclosure の節境界、引用 / コードブロックの有無、直前直後の橋渡し文の追従に置いた。
- 追加の機械点検として、4 言語の見出し数 / 引用ブロック数 / コードフェンス数 / table 行数も比較した。`headings=47`、`quotes=54`、`codefence=4`、`table_lines=26`（`|` 含有行ベース）は 4 言語で一致し、section 単位の bullet / quote 分布も本文側は揃っている。front matter タグの既知差は 2 種で、①本数差 = ja のみ `個人開発` が 1 本多い（`ja bullets=81`、en/zh/ko=`80`）、②ローカライズ差 = `AIエージェント`（ja）↔ `Agent`（en/zh/ko）である。いずれも translation drift というより想定内の metadata / ローカライズ差として扱う。
- さらに 2026-06-19 に section fingerprint ベースの line 単位 re-diff を再実行し、見出し index ごとの `heading / quote / bullet / numbered / table / codefence / image / caption` 分布を比較した。新しく actionable だったのは `### prompt → context → harness → loop の流れ` にある `paradigm_staircase.svg` と caption が en/zh/ko で欠落していた 1 件だけで、translations 3 本へ同期済み。再実行後に残った mismatch 8 件は、3 言語が同型の `para-1 / blank-1` 差を示すだけで、raw URL を blockquote 内 inline link へ畳んだ既存スタイル差・段落結合差として説明でき、新しい structural omission は見つからなかった。残差 index は `7 / 18 / 28 / 31 / 32 / 35 / 40 / 44` で固定しておく。
- `個人開発` タグは、現時点では ja 固有タグとして現状維持する。4 言語タグの完全一致は要件にせず、将来 line 単位 re-diff を回す際は `個人開発` と `AIエージェント` ↔ `Agent` の両方を既知差として除外する。
- 2026-06-18 終了時点の到達メモとしては、#43 は companion / `green-keeper` / `/goal` 帯まで、#46 は JA/en/zh/ko/kamikudaki の本文と endmatter まで、Team stock 3 本は Team POST と item id 記録まで完了していた。その後 2026-06-19 の handoff / 草稿更新は commit `2a8b942` で確定した。現行 blocker として最優先で残すのは、Qiita Team 3 本で **API GET は `private:false` を返し、未認証 HTML は `/login` へリダイレクトするが、それでも team-only と positively 確認できていない**点である。可視範囲是正（rollback / visibility tightening）が必要かどうかの判断待ち案件として、残件一覧から落とさない。
- 同時に API 側では `group.url_name: general` / `group.private:false` / `organization_url_name:null` も確認済みで、poster が当時 `group_url_name` を送っていなかったことから implicit General sharing 仮説を追う。ただし blocker の主語は引き続き **過剰露出疑いを否定できないこと**であり、local source に `general` を resend default として固定しない。
- 未解決の human-gate 外部アクションは、#46 の publish 判断、dev.to 英語版 update / publish 判断、CTA-149 local batch の live 再 publish / PATCH 要否判断の 3 件である。Qiita Team 3 本の rollback / visibility tightening は、必要だと人間が判断した時点でこの集合へ追加する。
- dev.to 英語版の残件定義も実ファイルと一致している。`tools/qiita-cli-poc/public/qiita43_harness_loop_stack_en.devto.json` は `id: 3915834` / `published: false` / dev.to URL 付きの sidecar として残っており、公開前に human-gate を要する draft 状態である。
- `NEXT_SESSION.md` の旧 operator queue 見出しは `old context / current scope outside (2026-06-12 stale)` へ更新済みで、asciinema 録画 / production 起動 / credential 復旧は **ローカル operator 作業の旧メモ**として現行スコープ外に退避した。現行の未解決 human-gate 外部アクション 3 件とは別カテゴリで読む。

## 次の具体的な一手

1. #43 en/zh/ko は「ローカル草稿整合」ではなく、**発行済み限定共有 draft の同期凍結**として扱う。2026-06-19 の re-diff と spot-check までで、**local source 上の residual translation drift 監査は一旦クローズしてよい**状態になった。以後の論点は live URL 側の未反映 factual 値と publish gate 管理であり、local source 監査そのものを再開候補の先頭へ戻さない。
2. #43 en/zh/ko の次の再開点は、**既に handoff に列挙済みの帯を機械的に再監査しない**こと。2026-06-19 の 4 言語 line 単位 re-diff では `paradigm_staircase.svg` 同期漏れ 1 件だけを修正し、残差は既存スタイル差へ縮退した。次にやるなら、「新しい seam 候補の発見」よりも、live draft 再開前の publish gate 管理と live 側未反映分の扱いを判断する。
   - `2-7 → ★ honest disclosure`、`/goal` 節 → 独立 honest disclosure、`3-3 → 3-4`、統合章 → まとめ、まとめ → 次回予告 / 参考 は、少なくとも seam spot-check 一巡の確認済み候補として扱う。
   - 機械比較では本文構造の異常は見つかっておらず、直近の既知差は日本語正本先頭タグの `個人開発` と、`AIエージェント` ↔ `Agent` のローカライズ差である。line 単位 re-diff を切るなら、この metadata 差を除いた本文比較として扱う。
3. llterm 記事シードは、まず **種 #6「自走 AI ループの作り方と落とし穴」** を先に育てる。種 #1「注入タスク飢餓」は #6 の導入 incident としていったん吸収し、単独先出しは当面しない。
4. 種 #6 の ja draft は `tools/qiita-cli-poc/public/qiita46_llterm_supervision_first.md` として第8章まで通し、`2549%` 記述も「rotate 因果は確認済み / 膨張機序は有力推定 / 算定内訳は未確定」の境界へ締め直した。JA 正本側の `☕ 休憩ポイント` / 参考文献 / HTML annotation / 挿絵 `025.jpg` は投入済みで、`025.jpg` は多言語ごとに作品名表記を分けつつ raw URL の HTTP 200 も確認済み。URL は既存運用どおり `raw.githubusercontent.com/.../main/...` を維持する。`qiita46_llterm_supervision_first_kamikudaki.md` も冒頭ナビ・「完全版で掘る 3 点」・内部語の 1 行グロスまで磨き込み済み、`kamikudaki_shishi.svg` raw URL の HTTP 200 も確認済み。さらに en/zh/ko draft も第8章と翻訳版 endmatter 一式まで同期し、最終見直しパスでも新たな重大 drift は未検出だった。次の外部アクションは human-gate を伴う publish 判断になる。
5. handoff commit では `git add .` を使わず、対象 docs の名指し add に固定する。
6. push / publish などの外部アクションは引き続き human-gate を要するものとして維持する。
7. レビュー依頼時は `.llterm/loop_ledger.jsonl` の未 commit ノイズ diff ではなく、対象 commit の `git show` を提示して docs 差分を分離する。
8. 外部公開フェーズで audit 系語を使う場合は、records-retention 監査との誤読を避けるため定義を添える。
9. バス江コマを比喩に使う場合は、一次確認できたセリフと筆者解釈を混ぜない。たとえば `alu.jp` crop `1DLuaYTNfWIQz3tqCv1h` は「聖書の引用みたいになってる…!」までは出典化できるが、`honest disclosure` を毎回持ち出す感じ等は筆者比喩として明示する。
10. #46 の publish gate 状態は項目 `4` を正本として追う。JA 正本の HTML annotation は完了済み。翻訳版の最終見直しと用語 drift 監査は一巡し、新たな重大差分は未検出。残る外部アクションは human-gate を伴う publish 判断。
11. 難しい論点は Team 向けに個別 stock する。現時点での 3 本 (`Semantic Governance` / `LLM Wiki と thought circulation` / ``ctx 2549%`` postmortem) は Team POST 済みで、投稿待ち一覧 / POST 後の記録欄の正本は `docs/articles/2026-06-18/team_stock_queue.md`、公開順・human-gate 条件・rollback 注意は `docs/articles/2026-06-18/team_stock_publish_plan.md` を正本とする。`private:false` 着地に対する可視範囲是正（rollback / visibility tightening）の判断待ちは current blocker として別建てで追うが、現時点では「可視範囲意味論の不一致」より **team-only を positively 確認できるまで過剰露出の疑いを優先**する。
12. `NEXT_SESSION.md` の 2026-06-12 旧 operator セクションは stale 扱いを明示済みなので、asciinema 録画 / production 起動 / credential 復旧は現行優先の残件に数えない。現行の未解決 human-gate 外部アクションは #46 publish 判断 / dev.to 英語版 update・publish 判断 / CTA-149 live 再 publish・PATCH 要否判断の 3 件で読み、Qiita Team 3 本の `private:false` 着地はこれとは別の current blocker として追う。
13. **次の具体的一手**は Team blocker の remediation を、すでに固定した優先順で再開すること。`docs/articles/2026-06-18/team_stock_queue.md` と `team_stock_publish_plan.md` を正本として開き、(1) Team UI で intended share target / private state を確認・是正できるかを先に見る。(2) UI で表現できない、または再現性ある API 経路を残す必要がある場合だけ、concrete group_url_name を source に入れた opt-in PATCH (`--patch-group-url-name`) を検討する。既定 PATCH は維持されており、opt-in 再送経路はローカル実装済みだが、既共有 item に対する締め直し効果は一次未確認という前提で再開する。
13. 翻訳 QA は、JA 原文と各節を逐次照合し、専門用語 (`ctx 2549%` / `turn boundary` / `interrupt` / `sign-off` / `block point`) を固定しながら反映する。
   - ko 版では、第5章の `운영 환경` / `본 처리` も最終見直しで固定済み。
   - zh 版では、`算定内情` / `饥饿` も第3章〜第7章で統一済み。
   - zh 版では、第8章末尾の `故障处理记录` まで含めて日本語混在を解消済み。
14. `qiita47_harness_engineering_thoughts.md` は `#43` から派生した local-only の **independent short draft** として維持する。現時点では publish / Team stock へは載せず、`157.jpg` の使いどころ定義に加えて、冒頭の `前提 / 流れ / ゴール` 3 点契約と「この短稿で話さないこと」、（本プロジェクトでの）RAPTOR（判断層と実行層を分けた二層 runtime）/ 試作段階の `llterm`（terminal 起点の名残を名前に残した PySide6 GUI 実装）/ Claude Code 公式 `/goal` / `desired-actual-drift-repair` の最小 loop 節、`green-keeper` 的な最小具体例、その比喩が clean / dirty の観測までしか言い切れないという破綻点、harness を強くしすぎたときの failure mode、「明日 1 個だけ変えるなら何か」、さらに「何を runtime に入れず人間へ残すか」、runtime を **観測 → 停止 → 修復 → 意味づけ** の順で育てる実務ルール、最後の `意味づけ` だけは runtime に載せず人間へ残すという境界、`しつけ` 比喩は growth order 全体を説明するものではなく、せいぜい `観測 / 停止 / 修復` の前半までに効き、最後に「何が本当に重要なズレか」を決める `意味づけ` は loop の外側に残る、という seam、そして runtime に入れる前に人間側で先に捨てるべき癖（後付け説明 / proxy の本体視 / 例外の雑な一般化）まで入れた。補助導線の外部 2 本も Distill / Mitchell Hashimoto の実 URL へ揃えた。**次の具体的一手**は、`#43` へ戻すか publish へ送るかではなく、`qiita47` をあと 1 回だけ読み直して「これ以上削ると spine が壊れる最短版」まで圧縮するのか、逆に公開候補として参考導線と用語注記を最終整形するのかを最初に二択で決めること。その際、canonical ledger は `44ed5af` が未反映の最新 1 件として残るのが正常状態である。
15. `qiita37_gpu_triple_run_gate_price_kamikudaki.md` は増補済みだが、Kaggle 運用 PoC をこのまま本文に残すか、`<details>` の深掘り層へ逃がすかはまだ決め切っていない。次に触るならそこを 1 回だけ判断する。

2026-06-18 decision log: ユーザー選択 `1) 実行する` を受領。公開中の Qiita 英語版記事 `2622da17495d61480fa2` に対して、local で復旧済みの正しいタイトルを public PATCH で反映する。対象は Qiita API の記事更新 1 件のみで、push / publish 範囲拡大 / deindex はこの決定に含めない。
2026-06-18 execution log: `tools/qiita_public_post.py post ... --yes` で public Qiita item `2622da17495d61480fa2` を PATCH 更新し、Qiita API `GET /api/v2/items/2622da17495d61480fa2` と HTML の `<title>` / `og:title` / `<h1>` で正しい英語タイトルへの反映を確認した。
2026-06-18 decision log: ユーザー選択 `1) 実行する` を受領。public Qiita 記事 `bf1cfe3b4f40b87f068d` は、既公開 canonical `6e107c7dfa0c261ee4d7` へ誘導する short redirect 本文へ置き換える。対象は Qiita API の記事更新 1 件のみで、push / deindex / 他記事の publish はこの決定に含めない。
2026-06-18 execution log: `py -3.11 tools/qiita_public_post.py post tools/qiita-cli-poc/public/bf1cfe3b4f40b87f068d.md --yes` で public Qiita item `bf1cfe3b4f40b87f068d` を PATCH 更新した。反映確認は、このセッションで実行した Qiita API / HTML の自己確認ログに基づく。API `GET /api/v2/items/bf1cfe3b4f40b87f068d` の `body` 先頭と、公開 HTML の canonical ID / 「統合・再編しました」文言で redirect 本文への反映を確認した。
2026-06-18 decision log: ユーザー選択 `1) 実行する` を受領。`.llterm/loop_ledger.jsonl` の tracked ノイズを恒久対策として deindex する。実行内容は `git rm --cached .llterm/loop_ledger.jsonl` と `.gitignore` へのファイル単位追記で、push / publish / 追加の削除はこの決定に含めない。
2026-06-18 execution log: `git rm --cached .llterm/loop_ledger.jsonl` を実行し、`.gitignore` に `.llterm/loop_ledger.jsonl` を追記した。実ファイル末尾は JSONL として読める状態を確認済みで、破損切り分けは不要だった。以後この台帳は on-disk で保持しつつ untracked 運用へ切り替える。
2026-06-19 decision log: ユーザー選択 `1) 例外標本として履歴に残し、以後は再発防止のみを維持する` を受領。`a0b793a` / `6d9854d` / `c16a69b` / `e150ee4` / `ed1e841` の standalone backfill debt 標本は cleanup 対象として掘り返さず、履歴上の例外標本として保持する。以後は新たな同型 commit を増やさず、backfill は実質的 handoff 更新に便乗させる方針だけを維持する。
2026-06-18 decision log: ユーザー選択 `1) 別 egress を含む対話ブラウザで Holland / Koza の canonical permalink を確認し、開けない側にだけ WorldCat / Google Books / archive.org 書誌ページなどの補助導線を併記する` を受領。まず handoff 上はこの方針を固定し、その後に non-local egress からの reader reachability を補助確認して、結果と根拠を handoff へ戻す。
2026-06-18 note: referral CTA 用のバス江コマは `012.jpg`（「ひくわ」）を既定のまま維持し、`044.jpg` は「押し売り感を意図的に過剰化する強め variant」として台帳に追加定義した。既存 CTAIMG の一括差し替えは行わず、必要な草稿だけ opt-in で差し込む。
<!-- CTA149_BATCH_STATE_BEGIN -->
2026-06-18 note: review 対象だった CTA-149 batch は `22d5460384c2cb54a9e6` の live item を直す作業ではなく、`qiita43/44/45/46/47` の local source 末尾 CTA を整える差分だった。`149.jpg` は opt-in の強め variant に戻し、`1-week free trial` / `1 週間の無料トライアル` などの時限断定は「無料で試せる（提供条件は公式参照）」へヘッジ済み。live 再 publish / PATCH は未実施のまま据え置く。
2026-06-18 note: 上記 CTA-149 local batch は commit `430fcdc` で確定済み。したがって次に触るなら local wording ではなく、live 再 publish / PATCH を本当にやるかどうかの human-gate 外部アクション判断から始める。この判断待ちは未解決の外部アクション一覧にも残す。
<!-- CTA149_BATCH_STATE_END -->

## このターンの実施結果

- `docs: sync qiita draft handoff for articles 43-45` を commit `bab1557` として作成した。
- `docs: tighten publish-gate notes for qiita drafts` を commit `e4e3968` として作成した。
- `docs: refresh handoff after publish-gate cleanup` を commit `7e7931c` として作成した。
- `docs: sync handoff with article 43 drift fixes` を commit `0478fa1` として作成した。
- `docs: refresh handoff after latest drift sync` を commit `426be90` として作成した。
- `docs: fix handoff evidence for article 43 drift` を commit `e942370` として作成した。
- `docs: refresh handoff after article 43 audit` を commit `496ca41` として作成した。
- `docs: clarify handoff risk and next scope` を commit `fded95b` として作成した。
- `docs: narrow article 43 drift scope` を commit `e0b0ee5` として作成した。
- `docs: tighten handoff scope wording` を commit `7ce6ee1` として作成した。
- `docs: record article 43 llm wiki audit` を commit `31e974e` として作成した。
- `docs: clarify article 43 factual audit scope` を commit `e871b12` として作成した。
- `docs: record article 43 hedge retention audit` を commit `23998cd` として作成した。
- `docs: note review handoff process follow-ups` を commit `ed0159a` として作成した。
- `docs: narrow article 43 remaining audit scope` を commit `ed1caab` として作成した。
- `docs: sync next session handoff for article 43 drift` を commit `cdcc389` として作成した。
- `docs: record article 43 harness audit` を commit `2f92ee2` として作成した。
- `docs: narrow article 43 early-section audit scope` を commit `7f82f6e` として作成した。
- `docs: record article 43 control-loop audit` を commit `85eb5e3` として作成した。
- `docs: record article 43 terminology audit` を commit `521d318` として作成した。
- `docs: record article 43 benchmark section audit` を commit `9af1bbd` として作成した。
- `docs: record article 43 knowledge-stack audit` を commit `7d281c3` として作成した。
- `docs: sync handoff after article 43 audits` を commit `d2cec49` として作成した。
- `docs: record article 43 reference audit` を commit `e7dfdef` として作成した。
- `docs: align next-session handoff state` を commit `d92192f` として作成した。
- `docs: record article 43 chapter 3 intro audit` を commit `20afd3e` として作成した。
- `docs: refresh handoff narrative after audit` を commit `dc70dc0` として作成した。
- `docs: sync article 43 llm wiki quote blocks` を commit `83f510b` として作成した。
- `docs: align article 43 quote formatting` を commit `16f2b52` として作成した。
- `docs: sync remaining article 43 interludes` を commit `5a4aedf` として作成した。
- `e4e3968` では #43 多言語 draft の RAD 件数 drift、`kamikudaki` の最小補強、`qiita44` の参考文献訂正、handoff の stale 記述を整えた。
- `0478fa1` では #43 JA 正本の hedge note と `NEXT_SESSION.md` の stale 記述を、ローカル source / live URL の差も含めて整えた。
- `426be90` では handoff 2 ファイルを最新の commit 列まで追従させたが、その後の factual 反転確認ぶんで handoff 2 文書に再度更新が入っている。
- `e942370` では #43 en/zh/ko の honest-disclosure 節の実在根拠を handoff に明記し、`git add .` で `loop_ledger` を再ステージしない個別 add 方針を足した。
- `496ca41` は `git show` で spot-check し、handoff 2 文書だけの更新であることを確認済み。
- `d92192f` では handoff 3 文書の commit 列と drift 範囲メモを更新し、当時最新だった `e7dfdef` までの現在地を揃えた。
- en/zh/ko の変更は `ignorePublish: true` への切替だけでなく、終盤 hedge note / 要約表 / 結論部の `47,097 docs` 反映まで含む本文改稿である。
- `20afd3e` では #43 第3章導入〜`3-2. LLM Wiki` 導入直前の監査結果を handoff へ反映した。
- `dc70dc0` では stale だった handoff ナラティブを今回監査内容へ更新した。
- `83f510b` では en/zh/ko の `3-2. LLM Wiki` 本体に日本語正本の「半信×半疑」引用ブロックと `alu.jp` URL を同期した。
- `16f2b52` では新規 `Ud7l...` ブロックを各翻訳ファイルの既存引用スタイルへ揃え、末尾参考リストにも `Ud7lZLbei1F5xaFuAq3i` を追記した。
- `5a4aedf` では残っていた inline 引用 4 件（`MDsuu...` / `2qlJjB...` / `CPon283...` / `H4Pix38...`）を本文と末尾参考へ同期し、crop URL 数を日本語正本 16 / en 16 / zh 16 / ko 16 へ揃えた。
- 公開済み英語版 Qiita item `2622da17495d61480fa2` のタイトル崩れ（`# >-` 表示）を再現し、front matter の `title: >-` と poster 側の最小パーサ不一致が原因と切り分けた。
- `qiita43_harness_loop_stack_en.md` / `_ko.md` の front matter `title:` を repo 規約どおり single-quoted 1 行へ修正した。
- `tools/qiita_public_post.py` / `tools/qiita_team_post.py` に YAML block scalar title (`>-` / `|`) と single-quoted YAML escaping (`''`) の解釈を追加し、dry-run で英語版タイトルが正しく復旧することを確認した。
- `tools: fix qiita title frontmatter parsing` を commit `409b628` として作成し、ローカル修正を ledger ノイズから分離して確定した。
- public Qiita item `2622da17495d61480fa2` に対してタイトル修正 PATCH を実行し、API / HTML の両方で `#43 In 2026, the Industry Named the AI's "Reins" and "Wheel" — How I Started Assembling a Prototype harness/loop engineering Stack Locally` へ復旧したことを確認した。
- `tools/_frontmatter.py` を新設し、`qiita_public_post.py` / `qiita_team_post.py` / `convert_to_qiita_cli.py` / `zenn_convert.py` の frontmatter パーサを共有化した。
- `tests/test_qiita_frontmatter.py` を追加し、folded scalar / single-quote escaping / block list の回帰テストを導入した。`pytest tests/test_qiita_frontmatter.py tests/test_zenn_convert.py tests/test_qiita_url_sync.py` は 34 passed。
- live 反映確認は、このセッションで実行した Qiita API / HTML の自己確認ログに基づく。
- `docs/articles/assets/bazue_all/index.md` にユーザー確認済みの挿絵対応を追記し、`081.jpg` = バイブコーディング、`006.jpg` = ハーネスエンジニアリング、`163.jpg` = AIオーケストラ、`025.jpg` = ループエンジニアリング実践中、という運用メモを固定した。
- `tools: share frontmatter parser across qiita flows` を commit `a07f0c7` として作成し、shared parser・sibling root-cause 修正・回帰テスト追加を ledger ノイズから分離して確定した。
- #43 の 4 言語草稿で、旧名称 `llloop` と起動コマンド `lll` を最終名称 `llterm` へ更新した。`SESSION_SUMMARY.md` / `next_plan.md` の現行進捗説明も同じ表記へ揃えた。
- #43 の `llloop` / `llterm` の関係も 4 言語本文へ補足し、`llloop` は TUI 試作名、`llterm` は TUI の限界感から GUI に切り替えて作り直した後継だと明記した。
- `D:/projects/llterm` の一次確認で、`llterm` は実際に `gui-scripts` / `src/llterm/gui/app.py` を持つ PySide6 GUI 実装だと確認したため、#43 の `2-6` 起動説明も GUI 前提へ揃えた。`term` は terminal 起点の名残である旨を 4 言語本文へ補足した。
- #43 の「キン肉星＋R.O.D＋リィンカーネーション＋ROS PBT」の 4 連想は、人によっては飛躍や `bazue_all/015.jpg` 的な誤用に見えうるため、4 つの連想が別々の設計部品を受け持ったことを ja/en/zh/ko の本文へ追記した。
- public Qiita 記事 `bf1cfe3b4f40b87f068d` を canonical `6e107c7dfa0c261ee4d7` への short redirect 本文へ更新した。ローカル source `tools/qiita-cli-poc/public/bf1cfe3b4f40b87f068d.md` は public PATCH 済みの実体として維持する。
- public Qiita の redirect / タイトル修正の反映確認は、このセッションで実行した API / HTML の自己確認ログに基づく。
- `D:/projects/llterm/docs/ARTICLE_SEEDS.md` を記事化観点で読み直し、`docs/articles/2026-06-18/llterm_article_seeds_screening.md` にスクリーニングを追加した。本命は 種 #6「自走 AI ループの作り方と落とし穴」、先行して切り出せる中編は 種 #1「注入タスク飢餓」、種 #2〜#5 は #6 の章素材として回収する方針が最有力。
- 2026-06-19 時点の handoff / 草稿差分は commit `2a8b942` で確定済みで、対象は `docs/*` に加え、`qiita43_harness_loop_stack_{en,zh,ko}.md`、`qiita44_evolutionary_programs_block_diagram.md`、`qiita45_human_ai_dev_incident_patterns.md`、`qiita47_harness_engineering_thoughts.md` である。`loop_ledger` の deindex は commit `7745f84` で完了済み。
- public Qiita 記事 `bf1cfe3b4f40b87f068d` を確認したところ、内容は `個人開発AIのlliveが"メガ進化"！ — 進化の大失敗から甦り、実LLMの"苦手"まで淘汰した全記録` で、既公開の canonical 総集編 `6e107c7dfa0c261ee4d7`（`lldarwin / 進化 arc 総集編`）と実質重複している。#26 public 短報 `0a35e1...` が既に canonical へ誘導する short redirect 化を採っているため、`bf1...` も同じ方針で整理するのが最小。
- 上記の重複・前例確認は、Qiita API の `bf1...` / `6e107...` / `0a35...` と、ローカル原稿 `tools/qiita-cli-poc/public/0a35e1bfb814adab8565.md` / `6e107c7dfa0c261ee4d7.md` の一次確認に基づく。
- canonical `6e107c7dfa0c261ee4d7` と raw 原稿 `docs/articles/drafts/QIITA_evo_ja.md` の HEAD 200 は確認済み。`bf1...` の redirect 文面は、前例 `0a35e1bfb814adab8565.md` の「統合・再編しました」+ canonical 直リンク形式に合わせた。
- `.llterm/loop_ledger.jsonl` はどちらの commit にも含めていない。
  - 当面は `git add docs/SESSION_SUMMARY.md docs/next_plan.md` のような個別 add を使い、`git add .` で ledger を再ステージしない。
  - 旧 tracked ノイズ問題は `7745f84` で解消済み。以後は `loop_ledger` を通常の review diff へ混ぜない運用を維持する。

## publish gate 送り

- `qiita44` は参考文献節へ canonical 入口を追加済み。このターンでは #43 residual drift 棚卸しに加えて、MIT Press 到達性 gate の証拠強度表現を `closed` から **soft-gate** へ降格し、Koza DOI 未固定のまま canonical permalink 主参照を維持する方針を handoff に明記した。
  - GA / ES / GP / NEAT / novelty search / MAP-Elites / CMA-ME / lexicase の代表文献を最低 1 本ずつ置き、一次導線 URL まで補った。CMA-ES は失効証明書の旧 PDF ではなく arXiv `1604.00772` を使う。
  <!-- QIITA44_GATE_STATE_BEGIN -->
  - 本文の言い回しと参考導線の最終突合は完了済みで、MIT Press 2 件の到達性 gate は 2026-06-19 時点で **soft-gate** 状態へ整理した。
  - 本文と参考導線の spot-check では、GA = 固定長遺伝子列、ES / CMA-ES = 変異分布更新、GP = 式 / プログラム木進化、NEAT = 構造進化、novelty / MAP-Elites / lexicase = 「何を残すか」の分岐、という説明までは整合していた。
  - claim-strength pass では、論旨を変えずに過強な断定を 3 箇所だけ弱めた。`淘汰器が壊れていたら進化はだいたい壊れる` は `探索は鈍りやすい` へ、`長期でだいたい飽和か monoculture に寄る` は `寄りやすい` へ、`高次元 descriptor では cell の大半が空になる` は `空になりがち` へ調整済み。
  - 追加の最終微調整では、断定トーンが先行していた 4 箇所も弱めた。`これはかなり重要です` は `ここは見落としやすい点です`、`これは本当に重要です` は `ここは切り分けを誤りやすい点です`、`かなりクリア` は `だいぶクリア`、結語の `壊れやすい` は `詰まりやすい` へ調整済み。
  - Holland / Koza の MIT Press permalink は本文と handoff で一致済み。`qiita44` の未解決論点からは「canonical permalink を主参照として維持する」点は外してよいが、gate 自体は一度きりの補助観測に依存する **soft-gate** として残す。
  - 到達性 gate については、2026-06-18 時点で記事側の Holland 導線 `Adaptation in Natural and Artificial Systems`（canonical permalink `https://mitpress.mit.edu/9780262581110/adaptation-in-natural-and-artificial-systems/`、DOI `10.7551/mitpress/1090.001.0001`、resolver `https://doi.org/10.7551/mitpress/1090.001.0001`）と、Koza 導線 `Genetic Programming: On the Programming of Computers by Means of Natural Selection`（canonical permalink `https://mitpress.mit.edu/9780262527910/genetic-programming/`）を対象に、PowerShell `Invoke-WebRequest` + browser UA + Cookie なし、および Microsoft Edge headless で canonical permalink 2 本と Holland DOI resolver の Akamai 403 までは証跡化済みである。ここで確定している事実は **このローカル egress からは Akamai 403 を受けた** ことだけであり、reader にとってリンクが無効だとまでは言えない。Holland の DOI `10.7551/mitpress/1090.001.0001` は 2026-06-18 に Crossref API で `The MIT Press` / `Adaptation in Natural and Artificial Systems` / `John H. Holland` / `1992-04-29` の一致を確認済み。Koza 側は Crossref の title/author 検索と `9780262527910` クエリでは MIT Press 書籍 DOI を特定できていない一方、MIT Press title page では paperback `9780262527910` / hardcover `9780262111706` の同一書誌として確認でき、WorldCat でも OCLC `26263956` の 1992 MIT Press print book として確認できた。したがって現時点では DOI 未固定のまま canonical permalink を主参照として維持し、必要なら補助導線として publisher catalog / WorldCat を併記する。
- この gate の基線は **canonical permalink / DOI を引用上の主参照として維持する** ことであり、我々の 1 網からの自動 403 だけでは citation integrity を崩さない。非 Akamai 系の導線は差し替えではなく補助導線としてだけ併記し、archive.org も全文スキャン直リンクではなく書誌ページ扱いに留める。IP / VPN / Cookie など再現条件固定での再試行は調査補助手段であって gate 合否根拠には使わない。現時点の補助証跡は **別 UI / 別ブラウザ経由の補助観測** 1 回に留まり、reader reachability の恒常的実証まではしていない。
- 2026-06-18 の追加再観測では、このマシンの同一 egress 上で canonical permalink 2 本に対し PowerShell `Invoke-WebRequest`（browser UA / Cookie なし）を再実行し、どちらも `STATUS=403` を再確認した。これは **ローカル観測の再実行**だった。
- 2026-06-19 に Web 側対話ブラウザで canonical permalink 2 本を 1 回ずつ開き、どちらもログイン不要の MIT Press 書誌ページとして表示できることを確認した。これは **別 UI / 別ブラウザ経由の補助観測**という一度きりの観測であって、別 egress の恒常的 reachability 実証ではない。したがって gate は `ローカル egress 403` と `reader reachability/citation integrity` を切り分けた **soft-gate** として維持し、補助候補（Holland = WorldCat `https://search.worldcat.org/oclc/42854623` / Google Books `https://books.google.com/books/about/Adaptation_in_Natural_and_Artificial_Sys.html?id=5EgGaBkwvWcC` / Internet Archive `https://archive.org/details/adaptationinnatu00holl`、Koza = WorldCat `https://search.worldcat.org/oclc/26263956` / Google Books `https://books.google.com/books/about/Genetic_Programming.html?id=Bhtxo60BV0EC` / Internet Archive `https://archive.org/details/geneticprogrammi0000koza`）は本文常設ではなく staging comment に留める。観測時の成功条件は、Holland / Koza の canonical URL がログイン要求や即時 block page ではなく MIT Press の title/bibliographic page と読める画面を返すことだった。Koza 側の DOI は引き続き Crossref で未特定・MIT Press title page / WorldCat までは確認済み、という粒度を維持する。
  <!-- QIITA44_GATE_STATE_END -->
- `qiita43_harness_loop_stack_kamikudaki.md` は ☕ 休憩ポイントと参考文献節を追加済み。
  - ただし完全版 #43 への導線を優先した短縮版のため、一次情報の細目は引き続き完全版側へ寄せる。
- #43 en/zh/ko は発行済み限定共有 draft のまま凍結する。2026-06-19 の seam spot-check と line 単位 re-diff までで **local source 上の residual translation drift 監査は一旦クローズしてよい** 状態になったため、`ignorePublish: false` の判断は live URL 側未反映分と publish gate 管理を見てから行う。
  - `47,097 docs` ベースの factual drift 修正は **ローカル source 側のみ** で、live URL には旧 factual 値が**確実に残っている**（別管理）。local source 側の residual translation drift 監査は一旦クローズ済みなので、以後ここで追うのは live URL 側の未反映差である。
  - en/zh/ko とも対応する honest-disclosure 節は実在している。
    - 根拠: en `qiita43_harness_loop_stack_en.md` の `#### honest disclosure (Handling the "About 49k Items" Number)`、zh `qiita43_harness_loop_stack_zh.md` の `#### honest disclosure（关于「约49k件」这个数字的处理）`、ko `qiita43_harness_loop_stack_ko.md` の `#### honest disclosure("약 49k건"이라는 숫자의 취급)`。
  - `47,097 docs` honest-disclosure 節と直後の橋渡し段は局所確認済みで、日本語正本に大筋追従している。
  - `50手法 vs 96ノート` 節も局所確認済みで、96ノート / 39 documents / 12 clusters の注意書きまで日本語正本に追従している。
    - ここで確認したのは数値そのものの正当性ではなく、日本語正本に対する訳文追従である。
  - `LLM Wiki / thought circulation` 節も局所確認済みで、Anti-Circulation Safeguards の箇条書きと `llmesh / llive / llove` の製品対応づけまで日本語正本に追従している。
    - ここで確認したのは日本語正本に対する訳文追従であり、`Anti-Circulation Safeguards` / `thought circulation` / `RAD` の外部一次情報ベースの factual 検証ではない。
  - 追加 spot-check で、Karpathy 帰属のヘッジ語、`llive` 設計段階の限定句、製品対応づけの「私のマッピング」表現が en/zh/ko で保持されていることも確認済み。
  - 統合章〜結語も局所確認済みで、A/B/C 統合表、`手綱 / 輪 / 知` の3点整理、`Bölük 10×` を捨てた設計思想、次回予告の `設計段階` ヘッジまで日本語正本に追従している。
  - 第0章（`prompt → context → harness → loop` の階段 / `Agent = Model + Harness` の二次情報ヘッジ / automation vs loop / 章末 honest disclosure）も局所確認済みで、階段図の説明、二次情報の留保、`verifiable goal` の橋渡し、実務ブログと学術定義を分ける温度感まで日本語正本に追従している。
  - 導入部（「使うのをやめた数字」 / 一次情報に錨を下ろす / 第2章後の独立 honest disclosure 節で全開示する予告）も局所確認済みで、異常値を捨てる作法と本稿の主題提示まで日本語正本に追従している。
  - 第1章前半（`harness engineering` 命名経緯 / `vibe coding` 区別 / RAPTOR 2層 / `ハーネス型バイブコーディング` 説明）も局所確認済みで、Hashimoto/OpenAI まわりのヘッジ、Karpathy との差異、fail-closed の説明、ユーザー側3能力の導入まで日本語正本に追従している。
  - 第1章後半〜第2章冒頭（ユーザー側3能力 / AI成長マネジメント / anti-pattern / `loop engineering` 定義 / `Semantic Governance` 導入 / `llterm` honest disclosure）も局所確認済みで、比喩・留保・戦略説明まで日本語正本に追従している。
  - 第2章前半の `loop engineering` をもう一段深く（`react` / `reflexion` / `plan_execute_verify` の差し替え比較 / strategy names のかみくだき）も局所確認済みで、「固定レシピ」対比、速さと安全性の二軸、各戦略の平易化まで日本語正本に追従している。
  - 第2章前半の `loop engineering` security face（Filip Verloy 引用 / `scaling risk at machine speed` / `Semantic Governance`）も局所確認済みで、警句・出典導線・自作ハーネスの設計動機への橋渡しまで日本語正本に追従している。
    - この確認は JA `qiita43_harness_loop_stack.md:313-323, 687-695` と en/zh/ko の対応段落・参考文献行を横並びで突き合わせ、本文リンクと末尾出典の両方に Verloy Medium URL があることまで含めて行った。
  - 第2章前半の `llterm` 導入〜 MAPE-K 骨格も局所確認済みで、alpha 段階の honest disclosure、`MapeKRunner` の閉ループ、plan-execute-verify / Reflexion、体温調節の比喩まで日本語正本に追従している。
  - 第2章中盤（`fail-closed` 安全層 / `現状の実装では` の条件付き留保 / `green-keeper` / `/goal`）も局所確認済みで、SafetyPolicy の 3 段判定、CircuitBreaker / Budget / 認証要求検知、`Executor` 条件付きの honest disclosure、GitOps reconciliation 比喩、`Haiku` 既定の `/goal` 説明まで日本語正本に追従している。
    - ここで確認したのは主に日本語正本に対する訳文追従であり、Claude Code `/goal` docs の外部一次情報ベース再検証をこのターンで追加実施したわけではない。
  - さらに `2-6. 起動と実証タスク green-keeper` / `2-7. 「検証可能なゴール」を持つループ — /goal という公式実装` も spot-check し、`desired / actual / drift / repair` の4項対応、PySide6 GUI / `term` 名残の補足、`/goal` の Haiku 既定・turn cap・直後の honest disclosure 節への橋渡しまで en/zh/ko が日本語正本に追従していることを確認した。
  - 冒頭〜第1章前寄り（捨てた数字の導入 / `prompt → context → harness → loop` の階段 / automation と loop の差分 / Hashimoto 起点の `harness engineering` / OpenAI 403 に伴う二次情報ヘッジ / RAPTOR 二層構造の導入）も局所確認済みで、一次情報アンカー・二次情報ヘッジ・`Agent = Model + Harness` の注意書きまで日本語正本に追従している。
    - ここでも確認したのは主に日本語正本に対する訳文追従であり、Hashimoto/OpenAI/Karpathy/RAPTOR の一次情報を各翻訳ターンで再取得したわけではない。
  - 「捨てた数字」の独立 honest disclosure 節も局所確認済みで、arXiv `2605.18747` / `2605.27922` / `2605.26112`、`Bölük 10x` 否定、`GPT-5.5` 実在確認済み / 比較値の一次計測元・条件は未確認、一次と二次の線引きまで日本語正本に追従している。
    - ここでも確認したのは主に日本語正本に対する訳文追従であり、各論文やベンチの一次ページをこの翻訳監査ターンで再取得したわけではない。
  - 第3章後半（RAD の運用ルール / `LLM Wiki` の 3 層 / thought circulation と Anti-Circulation Safeguards / RAPTOR の evidence ladder / `corpus-first advantage` / 統合章の A-B-C 表）も局所確認済みで、K² サイジング、`rad_prune.py` の dry-run、`39 documents / 12 clusters` 注記、llive の主観マッピング、`suspicion → patch_validated` の証拠段階、`47,097 docs` を含む統合表まで日本語正本に追従している。
    - ここでも確認したのは主に日本語正本に対する訳文追従であり、Karpathy Gist / llive 要件 / RAPTOR 実装の一次情報をこの翻訳監査ターンで再取得したわけではない。
  - 第3章の導入〜`3-2. LLM Wiki` 導入直前も局所確認済みで、3層スタックの説明、`RAD_INDEX.md` / `65 RAD corpora` の導入、`47,097 docs` と `32,503 files` の内訳、`hacker_corpus` の raw 集約ファイルという留保、Karpathy 帰属のヘッジ付き `LLM Wiki` 3層導入まで日本語正本に追従している。
    - ここで確認したのは主に日本語正本に対する訳文追従であり、`RAD_INDEX.md` や Karpathy Gist の一次情報をこの翻訳監査ターンで再取得したわけではない。
  - `3-2. LLM Wiki` 本体は、3層説明と thought circulation / Anti-Circulation Safeguards 節、製品対応づけ、「半信×半疑」の引用ブロックと URL、末尾参考リストまで局所確認・同期済みで、未確認対象はそれ以外の細い橋渡し段に絞られている。
  - 追加 spot-check で、en/zh/ko に欠落していた「半信×半疑」の引用ブロックと `alu.jp` URL を日本語正本に合わせて補い、新規ブロックを各翻訳ファイルの既存引用スタイルへ揃えた。
  - 続く追補で、未同期だった 4 件（`MDsuuBm0xXPgngwyQve0` / `2qlJjBwdpYGOVjBkyhhL` / `CPon283udq6PfvfKrxAP` / `H4Pix38XWLRS077emoZC`）も本文と末尾参考へ同期した。crop URL 数も日本語正本 16 / en 16 / zh 16 / ko 16 に揃った。
  - その後の再監査で、`2qlJjBwdpYGOVjBkyhhL` は「未同期」ではなく、en/zh/ko で **`2-5` から第3章直前へ位置ずれした状態** だったことが分かった。現在は 3 言語とも `2-5` honest disclosure 末尾の本来位置へ戻し、第3章直前の誤配置は除去済み。
  - 統合レビューで挙がった「翻訳版は blockquote 内 inline link / 正本は blockquote 下 raw URL」という形式差は、今回の修正に起因するものではなく、同ファイル内の既存スタイル差でもあるため、このターンの actionable な修正対象には含めない。
  - さらに終盤の `観察ベースの3点` と H4Pix 引用を挟んだ結語導入も局所確認済みで、3 点の内容、`観察された傾向` のヘッジ、`ルール（構造）で縛る` への橋渡しまで日本語正本に追従している。
  - さらに参考文献節と末尾 hedge note も局所確認済みで、`alu.jp` crop URL 数は日本語正本 16 / en 16 / zh 16 / ko 16 に維持され、OpenAI 403 / RAD `47,097 docs` / `人間優位3点` 観察ベースなどの留保も日本語正本に追従している。`GPT-5.5` は OpenAI 公式で実在確認済みで、未確認として残るのは比較値の一次計測元・計測条件だけ。
  - 残ブリッジ棚卸しとして、`第1章末 → 第2章頭`、`3-1. RAD コーパス → 3-2. LLM Wiki`、`3-4. corpus-first advantage → 統合章` も確認済みで、第1章の `なぜ` から第2章の `どう` への橋渡し、`ただの山` から LLM Wiki へ入る導入、`A/B/C が1本に繋がる` から統合章へ畳む着地まで日本語正本に追従している。
  - さらに、導入 → 第0章、第0章末 → 第1章頭、`/goal` → 独立 honest disclosure、独立 honest disclosure → 第3章頭、`3-2` → `3-3` の局所接続も確認済みで、導入の作法宣言から用語地図、`鵜呑みにしない` から一次情報確認、`mystery graph` から `捨てた数字`、`無知の知` から knowledge stack、thought circulation から evidence ladder への流れまで日本語正本に追従している。
  - `alu.jp` crop URL 数の 16 本基準は、日本語正本を source of truth として **本文 8 本 + 参考節 8 本 = 計 16 本（unique は 8 本、各 URL が本文と参考で 2 回ずつ出現）** と確認したうえで、en/zh/ko も同じ構成かを照合した。
  - `promise-progress-payoff` / `ending-payoff` の再確認では、終盤の `観察ベースの3点` → H4Pix 引用 → `まとめ：手綱と、輪と、知` の 3 箇条 → `Bölük` 数字を捨てた payoff 文 → `次回予告的な余韻` → 参考文献節、という鎖を 4 言語で突き合わせた。
  - 参考文献節と末尾注記も局所確認済みで、`/goal` docs、arXiv `2605.*` 群、RAPTOR upstream、自著関連記事、バス江引用、`secondary-only / primary unconfirmed` の列挙まで日本語正本に追従している。
  - 2026-06-19 の seam spot-check + section fingerprint re-diff までで、代表的な細い橋渡し段と再開候補になりやすい章境界の局所接続は一巡し、**local source 上の residual translation drift 監査は一旦クローズ済み**である。ただし網羅保証ではないため、以後の論点は新しい seam 候補探索ではなく、live draft / live URL 側の未反映差と publish gate 管理へ寄せる。

## 次回の開始メモ

- 新規の設計・実装・調査へ進む前に、必要な論点があれば RAD コーパスを grep して先行手法を確認する。
- publish gate は着手済みで、`qiita44` の参考文献補強は RAD 接地後に反映済み。
- `kamikudaki` の ☕ / 参考文献は最小補強まで完了した。
- #43 en/zh/ko では、終盤 hedged note の RAD 件数を `47,097 docs` へ更新済み。
- #43 JA 正本の hedge note も `47,097 docs` ベースへ更新済み。
- 次は #43 en/zh/ko について、handoff が列挙してきた代表 seam は一巡済みだが網羅保証はしない、という前提で、**local source 監査をクローズした後に残る論点だけを扱う**。既に spot-check 済みの導入 / 第0章 / 第1章前半〜第2章冒頭 / 第2章前半〜中盤 / 独立 honest disclosure 節 / `47,097 docs` 節 / `50手法 vs 96ノート` / 第3章前半主要論点 / 第3章後半（RAD 運用ルール〜統合章）/ 参考文献節と末尾注記 / 主要 seam 群に加え、2026-06-19 の line 単位 re-diff でも `paradigm_staircase.svg` 同期漏れ 1 件以外の新規 structural omission は見つかっていない。したがって #43 の残件は、live draft / live URL 側の未反映差と publish gate 管理へ限定してよい。
- 直近の機械比較で actionable だったのは上記の図版同期漏れ 1 件だけで、front matter タグ差（`個人開発` と `AIエージェント` ↔ `Agent`）および 8 節の `para-1 / blank-1` 差は既知の metadata / 既存スタイル差として扱う。
- `.llterm/loop_ledger.jsonl` の恒久対策は commit `7745f84` で実施済み。今後は `.gitignore` 管理の local telemetry として扱う。

## 注意

- `ignorePublish: true` / `private: true` は `qiita-cli-poc` ローカル運用の安全柵。既発行の限定共有 URL を撤回するものではない。
- `docs/SESSION_SUMMARY.md` は通常 Stop hook に上書きされるため、必要な恒久メモは `NEXT_SESSION.md` と本ファイルを優先する。
