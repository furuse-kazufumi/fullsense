---
layout: default
title: "QIITA #20 — 1 セッションで 5409 テスト緑緑緑 + research hub 6 本開設"
parent: "Articles — 2026-05-20"
nav_order: 1
---

# 1 セッションで 5409 テスト緑緑緑 + research hub 6 本開設 — FullSense の一日

> 個人 OSS 開発者 × 自律 AI 開発の "1 セッション" は, 朝に test が
> 7 件死んでいて昼に lleval の採用優先度を決めて夕方に portal の自動更新
> パイプラインまで全部 push してる. そういう密度の日の話.

---

## 0. はじめに — 朝起きたら test が死んでいた

朝, コーヒー入れる前に CI を眺める. 緑だった test がいつの間にか 7 件赤い.
コードは触ってない. 触ってないのに赤い. これは「**家を出る前にラジオが
壊れてた事件**」と同じで, 自分の行動と無関係に世界が変わっている.

犯人は **WinGet**. 昨日勝手に `chafa.exe` を PATH に乗せていた.

このセッションでは, この事件を皮切りに,

- **3 プロジェクトの全テスト緑** (llive 1518 / llove 805 / llmesh 3086 =
  **計 5409 件**) を 1 セッション内で叩き出し,
- **AI agent 6 体並列で先行研究調査**を回し, FullSense の spinoff 7 件の
  採用優先度を決め (`lleval=HIGH`),
- **portal の `NEXT_SESSION.auto.md`** を Stop hook 連動で自動更新するように
  パイプライン化し,
- **採用優先度 HIGH の lleval の v0.1 要件 draft** を仕上げて全 push する,

という所までやった. 縦 (debug) も横 (research) も両方詰めた一日.

「個人 OSS 開発に Claude Opus 4.7 を秘書にしたら, セッション 1 つで
これだけ動く」というサンプルとして残す.

---

## 1. 事件 1 — WinGet が chafa を撃ち落とした

llove は TUI で Markdown / Mermaid / SVG / svgbob / dot / plantuml を
ターミナル画像に変換する. 画像変換ツールが **PATH に無ければ ASCII fallback
に降りる**設計で, fallback test が 5 件 (各 renderer 1 件) + MarkdownView
default test 1 件 = 計 6 件ある.

これが朝起きたら全部赤い:

```text
FAILED tests/test_dot_render.py::test_render_dot_falls_back_to_ascii_without_image_tool
FAILED tests/test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg
FAILED tests/test_mermaid_render.py::test_render_mermaid_falls_back_to_ascii_without_image_tool
FAILED tests/test_plantuml_render.py::test_render_plantuml_falls_back_to_ascii_without_image_tool
FAILED tests/test_svg_render.py::test_render_svg_falls_back_to_ascii_without_image_tool
FAILED tests/test_svgbob_render.py::test_render_svgbob_falls_back_to_ascii_without_image_tool
```

落語の枕みたいに考える. 「**落語家が小道具の扇子を忘れて来たんじゃない.
扇子は持ってきた. 持ってきたんだけど, 楽屋に勝手に箸が置いてあった.
箸があるから扇子じゃなくて箸で蕎麦すすってる. そりゃ客はキレる.**」

これと同じ. test は `image_tool=None` を渡して「画像ツール無いと仮定して
fallback してね」と言ったのに, 実装側は `image_tool is None` だったら
`find_image_tool()` で **PATH 上を勝手に探しに行く**. そして chafa を
見つけて image renderer 経路に行く. ASCII fallback に降りてくれない.

これは Python 設計としては別に間違ってない. `None` を「明示的に無し」と
解釈するか「未指定なので auto detect」と解釈するか, は実装者の自由. でも
test 側は前者で書いていた. **環境が変わるまでは合致していた**.

### 修正パターン: `monkeypatch.shutil.which` を抑止する

5 ファイルすべて同じパターンなので, 各 test 関数に `pytest.MonkeyPatch` を
引数追加し, 本体先頭で:

```python
def test_render_svgbob_falls_back_to_ascii_without_image_tool(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from llove.views import svgbob_render

    # image_tool=None でも find_image_tool() が環境上の chafa 等を拾うため,
    # PATH 検索を抑止して「画像ツール一切なし」を再現する.
    monkeypatch.setattr(svgbob_render.shutil, "which", lambda name: None)

    # ...以下従来通り
```

これで「画像ツール一切なし」を再現できる. test は environment-independent に
なる. 6 件全部この対処で緑.

7 件目の `test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg`
は MarkdownView 内部で複数 renderer module を呼ぶので, **for ループで一括
monkeypatch**:

```python
for mod in (dot_render, mermaid_render, plantuml_render, svg_render, svgbob_render):
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
```

### 教訓

「**`shutil.which` で optional binary を検出するコードを書いたら, test も
必ず `shutil.which` を monkeypatch しろ**」.

これを忘れると, 朝起きた時に WinGet が勝手に何か入れたせいで CI が落ちる.

memory に残した. キーワード: `feedback_env_dependent_tests`.

---

## 2. 事件 2 — Hypothesis が「Windows 遅いから知らん」と言ってきた

llmesh は HMAC chain ベースの audit log 系の test を Hypothesis で書いている.
ところが Hypothesis には **デフォルト deadline 200ms** という掟がある.
1 ケース 200ms 以内に終わらないと `DeadlineExceeded` で fail.

これも朝の状態に追加情報:

```text
hypothesis.errors.DeadlineExceeded: Test took 490.69ms, which exceeds the deadline of 200.00ms.
```

Windows + 初回ファイル IO で 490ms かかった (2 回目は 149ms). 完全に
**ウォームアップ問題**で, 本質的な実装バグではない.

最初は個別 test に `@settings(deadline=None)` を足した. でも 1 個直すと
次の test が同じ理由で fail. **「もぐら叩き」状態**.

漫才で言うと:

> ボケ「次に出てきたモグラは『self.entry_count』っていうやつや」
> ツッコミ「直す端から別のモグラが出てくるやないか」
> ボケ「Hypothesis ファミリーがそういう仕様や」
> ツッコミ「ファミリーって言うな」

これは個別対処では負ける. `conftest.py` で **profile 単位の一括設定**に
切り替える:

```python
# tests/conftest.py
from hypothesis import settings

# Windows での初回 file IO / import / hypothesis warmup で 200ms deadline を
# 超えるケースが頻発するため, llmesh の全 property test で deadline を
# 無効化する. 個別 test で @settings(deadline=...) を上書きすれば優先.
settings.register_profile("local-flaky-safe", deadline=None)
settings.load_profile("local-flaky-safe")
```

これで全 hypothesis test が `deadline=None` を default として受け取る.
個別 `@settings(...)` がある test はそちらが優先されるので, 後方互換も保たれる.

結果: llmesh **3086 件全部緑**. 走り終わって `12 分 20 秒`. property test
だけで数百件あるので, deadline 個別対処をしていたら半日溶けていた.

memory キーワード: `feedback_hypothesis_deadline`.

---

## 3. 横軸 — AI agent 6 体並列で先行研究調査

ここから縦 (debug) を一旦置いて, 横 (research) に切り替える.

FullSense umbrella には「spinoff 候補カタログ」 ([`spinoff_ideas_2026_05.md`](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spinoff_ideas_2026_05.md))
というのがあって, 現状 **7 つの vertical 候補** が並んでいる:

| 候補 | 一行 |
|---|---|
| **llgrow** | 個人開発者向け成長/収益化自動化 (HITL コンテンツ生成) |
| **lleval** | LLM ベンチ・評価専用 framework |
| **llcraft** | on-prem クリエイティブ素材生成 (TTS / 画像 / 動画 / 音楽) |
| **llbridge** | multi-AI orchestration (Claude / GPT / Gemini / Codex) |
| **llrisk** | 法務 / 技術 / ビジネス / 健康 / レピュ / セキュ の 6 軸リスク自動追跡 |
| **llforen** | raptor の forensic 機能を FullSense に取り込む |
| **llgov** | EU AI Act / 中国 AI 弁法 / GDPR / SOC2 を要件化する compliance layer |

これらの **採用優先度を決めたい**. でも一人で「うーん」と唸っていると
日が暮れる. なので Claude の Agent ツールで **6 体並列**に投げた:

```
Agent("llgrow prior art research", prompt="...")    # Jasper / Mautic / Langfuse 等を調査
Agent("lleval framework SOTA",      prompt="...")    # promptfoo / DeepEval / Phoenix 等を調査
Agent("Cognitive Mesh vs SOTA",     prompt="...")    # MemGPT / Generative Agents 等
Agent("llcraft creative SOTA",      prompt="...")    # SDXL / Flux.1 / VOICEVOX 等
Agent("llrisk continuous risk",     prompt="...")    # ServiceNow / Snyk / burnout 研究
Agent("llgov AI governance SOTA",   prompt="...")    # OPA / Cedar / Credo AI 等
```

それぞれに「800 字以内で報告書」「Sources 5-10 件」「Stack matrix / Gap /
Recommended approach の 3 章構成」と指示. **30 分以内に 6 件揃った**.

これを `docs/research/<topic>.md` として保存. 結果, 採用優先度が次のように
データで裏付けられた:

| vertical | 優先度 | 根拠 |
|---|---|---|
| **lleval** | **HIGH** | promptfoo を fork base にすれば 4 つの明確な空白 (on-prem 統一 / progressive size / honest disclosure / self-pref bias) を全部埋められる. base に乗るので 0 から作らない |
| **llgrow** | MID | Langfuse + Mautic を再利用すれば基盤新規不要. 新規実装は 3 件のみ |
| **llbridge** | MID | LangGraph/AutoGen は UI を memory peer 化していない → 差別化軸 |
| **llcraft** | LOW | C2PA Content Credentials + 独自 license_tier assertion で差別化候補, GPU 要件高 |
| **llrisk** | LOW | scope が大きい (6 軸), MVP は「個人開発者向け 6 軸ダッシュボード」 |
| **llgov** | LOW | EU AI Act Art.9-15 を自動検証する OSS は空白だが規制改定頻度が高い |
| **llforen** | DEFER | raptor 依存が強い, raptor 側の安定化を待つ |

「6 体並列の AI 調査」と「会議室で 6 人が会議」のコスト比は感覚的に
**100 倍以上の生産性差**. しかも 6 体は同時に動くので絶対サボらない.

memory キーワード: `project_fullsense_2026_05_20`.

---

## 4. 縦軸 — Portal の `NEXT_SESSION.auto.md` を自動化

ここで portal 側の **積み残し Priority 2** (Operator / Agent action queue 自動化)
を片付ける.

これまで `docs/NEXT_SESSION.md` は **手で書いていた**. でも

- 手で書くと **drift する** (実装が進むと中身が嘘になる).
- かといって **完全自動化すると意図が消える** (人間が「次にこれをやろう」と
  考えた方針メモが消える).

なので **2 ファイル運用** にする:

```text
docs/
├── NEXT_SESSION.md       # 人手. 方向性メモ. drift してもいい
└── NEXT_SESSION.auto.md  # 自動. Stop hook で毎ターン上書き
```

`gen_next_session_auto.py` を新規作成. Stop hook で呼ばれて以下を毎ターン
上書き:

1. **portal git snapshot** — 直近 commit 10 件 + status + upstream との
   ahead/behind
2. **関連プロジェクト最新状態** — llive / llove / llmesh / lldesign / lltrade の
   最新 commit + `tests/` ディレクトリ直近 mtime
3. **operator action 再抽出** — `NEXT_SESSION.md` の 🧑 セクションを
   parsing して `[ ]` チェックボックス化
4. **`verify_publication` 最新結果** — `out/verify_publication.last` キャッシュ
   の tail 30 行
5. **直近 4 時間に変更された portal ファイル**

raptor リポ側に薄いラッパ (`libexec/raptor-next-session-update`) を作って
`RAPTOR_CALLER_DIR=D:/projects/fullsense` のときだけ動くようにし,
`.claude/settings.json` の Stop hook 配列に登録. これで毎ターン終了時に
裏で勝手に portal が更新される.

> 「**書くのが面倒な日報を, 部下が勝手に書いて机に置いてくれる**」
> という上司の夢みたいな状態.

---

## 5. 仕上げ — lleval v0.1 要件 draft

採用優先度 HIGH に確定した **lleval** について, v0.1 要件 draft を
`docs/spec/requirements_lleval_v0.1_draft.md` に書いた.

要点:

- **promptfoo を fork base** (Apache-2.0 / CI 親和 / on-prem provider 拡張余地大)
- 観測層は **Phoenix (OpenInference/OTel)**
- RAG metric は **Ragas / TruLens** を adapter で吸収
- 差別化 4 軸:
  1. on-prem + cloud 統一 A/B (LLMeshProvider plugin)
  2. Progressive size curve (xs/s/m/l/xl の 5 段階 token sweep)
  3. Honest disclosure analyzer (異常 latency を 5 因子に自動分解)
  4. Judge rotation + position swap (self-preference bias 自動検出)

`LE-01〜08` の 8 要件 + 非要件 + 着手 trigger 4 段.

**実装着手は user 判断**. これは agent 自律 draft なので, ベンチ復旧
(Anthropic / Gemini / OpenAI credential / quota 復旧) と合わせて user が
GO サイン出してから, promptfoo fork PoC を走らせる.

---

## 6. 数字で締める

このセッションの定量メトリクス:

| 指標 | 値 |
|---|---|
| 全テスト緑件数 | **5409** (llive 1518 + llove 805 + llmesh 3086) |
| 1 セッション内 commit 数 | 約 10 (auto: backup 含む) |
| 意図 commit (feat/docs/fix/test) | 6 件 |
| 意図 push 数 | 5 件 (portal × 3 + llove × 1 + llmesh × 2) |
| 新規 research メモ | 6 件 |
| 新規 memory (運用則) | 4 件 |
| 新規 task (TaskCreate) | 16 件 (全 complete) |
| AI agent dispatch | 6 件 (research) |
| 環境依存 test fix | 8 件 (llove 7 + llmesh は profile 一括) |

---

## 7. 教訓まとめ

漫才のサゲ風に:

> 「結局なぁ, 自分一人でやろうとせんと AI 6 体並列で投げた方がええ」
> 「ええって言うてもお前, 1 体が 800 字書く間にこっちは寝るんか」
> 「**いや並列なんやから 6 体同時に走らせて自分は test 直しとるんや**」
> 「あー, ほな time-slicing じゃなくてマルチプロセスやな」
> 「**お前の脳みそをマルチプロセスにせえへんと FullSense は完成せえへん**」
> 「最後は俺の脳が悪いて結論かい」

技術的には:

1. **環境依存 test には `monkeypatch.shutil.which` を必ず入れろ**.
   WinGet が勝手に何か入れる時代.
2. **Hypothesis flaky は conftest 一括対処**. もぐら叩き禁止.
3. **採用優先度判断には AI agent 並列調査を使え**. 30 分で 6 件の SOTA
   報告書が揃う.
4. **NEXT_SESSION は 2 ファイル運用** (人手の方向性 + 自動 snapshot).
5. **lleval = promptfoo fork** が確定路線. 着手 trigger 待ち.

---

## 8. 次の一日へ

- 明朝起きて緑が緑のままか確認 (環境がまた変わってないか)
- `test_aoi_adapter_processes_synthetic` の順序依存 flaky を根本調査
- raptor リポ origin/main との diverge 解消 (manual merge 必要)
- lleval PoC 着手判断 (ベンチ復旧と並行)

---

> 「個人開発者は 1 セッションで縦と横を両方詰める. AI 秘書が並列なら
> 1 日が 6 日分動く. ただし上司の脳みそはマルチプロセスにならない.
> そこだけが律速.」
>
> — FullSense 2026-05-20 セッション総括

---

## 関連

- [research/lleval_sota]({{ '/research/lleval_sota' | relative_url }})
- [research/llgrow_prior_art]({{ '/research/llgrow_prior_art' | relative_url }})
- [research/cognitive_mesh_vs_sota]({{ '/research/cognitive_mesh_vs_sota' | relative_url }})
- [spinoff_ideas_2026_05]({{ '/spinoff_ideas_2026_05' | relative_url }})
- [requirements_lleval_v0.1_draft]({{ '/spec/requirements_lleval_v0.1_draft' | relative_url }})
- [NEXT_SESSION (人手)]({{ '/NEXT_SESSION' | relative_url }})
- [NEXT_SESSION (自動)]({{ '/NEXT_SESSION.auto' | relative_url }})
