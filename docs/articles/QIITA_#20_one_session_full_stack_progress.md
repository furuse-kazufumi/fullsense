---
title: 1 セッションで 5409 テスト緑 + research hub 6 本開設 — FullSense の一日
tags:
  - FullSense
  - llive
  - ClaudeCode
  - 自律エージェント
  - HonestDisclosure
project_group: llive
private: false
updated_at: '2026-05-20'
id: 96dc8af5b361ee44877b
organization_url_name: null
slide: false
ignorePublish: true
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 1 セッションで 5409 テスト緑 + research hub 6 本開設 — FullSense の一日

> 📚 **連載ナビ**: ← #19 GPU 無し PC で動く AI ｜ **#20 本記事** ｜ #21 3 日間 8 リポ marathon → ｜ [連載 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 各記事は単独でも読めます（リンクは回遊用）。

> 朝に test が 7 件赤くなっていて, 環境変化が原因と判明し, 修正と同時に
> AI agent 6 体を並列で先行研究調査に走らせ, FullSense の spinoff 採用優先度を
> 確定させ, portal の進捗ダッシュボードを自動化し, 採用優先度 HIGH の lleval
> v0.1 要件 draft まで仕上げて全 push した — 個人 OSS 開発者 × 自律 AI 開発の
> 1 セッションの密度を, 事実と数字だけで残す.

---

## 0. このセッションの構成

1 セッションで以下を達成した:

- **3 プロジェクトの全テスト緑** — llive 1518 / llove 805 / llmesh 3086 = 計 **5409 件**
- **AI agent 6 体並列で先行研究調査** — FullSense の spinoff 7 件の採用優先度を確定 (lleval = HIGH)
- **portal `NEXT_SESSION.auto.md` の Stop hook 連動自動化**
- **採用優先度 HIGH の lleval v0.1 要件 draft**

以下, 起きた順に縦軸 (debug → test fix) と横軸 (research → 優先度判定) を
記録する.

---

## 1. test が朝起きたら 7 件赤かった件

セッション最初の確認で, llove の test 7 件が `FAILED` だった:

```text
FAILED tests/test_dot_render.py::test_render_dot_falls_back_to_ascii_without_image_tool
FAILED tests/test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg
FAILED tests/test_mermaid_render.py::test_render_mermaid_falls_back_to_ascii_without_image_tool
FAILED tests/test_plantuml_render.py::test_render_plantuml_falls_back_to_ascii_without_image_tool
FAILED tests/test_svg_render.py::test_render_svg_falls_back_to_ascii_without_image_tool
FAILED tests/test_svgbob_render.py::test_render_svgbob_falls_back_to_ascii_without_image_tool
```

コードは前回セッションから触っていない. それでも赤くなっている. 単独実行
すると 1 件目の assert は:

```text
AssertionError: assert 'image' == 'ascii'
```

期待: `result.kind == "ascii"` (画像ツールが無いので ASCII fallback)
現実: `result.kind == "image"` (画像 renderer が走った)

### 原因

llove の各 renderer (mermaid / svg / dot / plantuml / svgbob) は次の判定で
fallback を決める:

```python
resolved_tool = image_tool if image_tool is not None else find_image_tool()

if not resolved_svgbob or resolved_tool is None:
    return SvgbobRender(kind="ascii", ascii_text=ascii_fallback(source))
```

`find_image_tool()` は内部で `shutil.which("chafa")` 等を呼ぶ. test 側は
`image_tool=None` を渡しているが, **実装は `None` を「明示的に無し」では
なく「auto detect 指示」と解釈する設計**.

ここまでは普通の Python の書き方で問題は無い. 問題は環境側で起きていた:

- 前日 (環境上) **WinGet が `chafa.exe` を PATH 上に登録した**
  (`C:\Users\<user>\AppData\Local\Microsoft\WinGet\Links\Chafa.exe`)
- `find_image_tool()` がそれを拾ってしまう
- ASCII fallback 経路に降りない → test 失敗

### 修正

`monkeypatch.shutil.which` を全て None で抑止する.

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

5 件 (dot / mermaid / plantuml / svg / svgbob) は同じパターンで修正.
6 件目の `test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg`
は MarkdownView 内部で複数の renderer module を経由するため, for ループで
全 module に同じ抑止を適用:

```python
for mod in (dot_render, mermaid_render, plantuml_render, svg_render, svgbob_render):
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
```

実 binary 必須の `test_e2e_real_chafa.py` は別件で, `mmdc` が PATH 上に
あっても実行で失敗するケースが新たに発生していた. test 内で結果 None を
検知して `pytest.skip()` に降りる二段構えを追加.

### 教訓

`shutil.which` で optional binary を検出するコードを書いた場合, test 側で
`shutil.which` を必ず monkeypatch する. 環境は予告なく変わる.

この教訓は memory `feedback_env_dependent_tests` に運用則として記録した.

---

## 2. llmesh の Hypothesis test も DeadlineExceeded で flaky だった

llove の修正後, llmesh 側で property test が次々に DeadlineExceeded で
fail し始めた:

```text
hypothesis.errors.DeadlineExceeded: Test took 490.69ms, which exceeds the deadline of 200.00ms.
```

Hypothesis のデフォルト deadline は **200ms**. Windows 環境では初回ファイル
IO や import で簡単に超過する.

### 個別対処では負ける

最初は `@settings(deadline=None)` を個別 test に追加した. ところが,

- `test_audit_chain_verify_succeeds_after_clean_appends` を直すと
- 次の run で `test_audit_chain_verify_fails_after_tamper` が同じ理由で fail
- それも直すと `test_codec_json_roundtrip` が fail

llmesh の property test は数十件あり, 個別対処は終わらない.

### conftest.py で profile 一括化

`tests/conftest.py` に hypothesis profile を登録する.

```python
from hypothesis import settings

# Windows での初回 file IO / import / hypothesis warmup で 200ms deadline を
# 超えるケースが頻発するため, llmesh の全 property test で deadline を
# 無効化する. 個別 test で @settings(deadline=...) を上書きすれば優先.
settings.register_profile("local-flaky-safe", deadline=None)
settings.load_profile("local-flaky-safe")
```

これで全 hypothesis test が `deadline=None` を default として受け取る.
個別 `@settings(...)` を書いた test はそちらが優先されるので, 既存 test は
壊れない.

結果: llmesh **3086 件全部緑** (12 分 20 秒). 個別対処を続けていたら半日
失っていた.

教訓は memory `feedback_hypothesis_deadline` に記録した.

---

## 3. AI agent 6 体並列で先行研究調査 (横軸)

ここから縦軸 (debug) を一旦止め, 横軸 (research) に切り替える.

FullSense umbrella には spinoff 候補が 7 つある:

| 候補 | 一行 |
|---|---|
| **llgrow** | 個人開発者向け成長 / 収益化自動化 (HITL コンテンツ生成) |
| **lleval** | LLM ベンチ・評価専用 framework |
| **llcraft** | on-prem クリエイティブ素材生成 (TTS / 画像 / 動画 / 音楽) |
| **llbridge** | multi-AI orchestration (Claude / GPT / Gemini / Codex) |
| **llrisk** | 法務 / 技術 / ビジネス / 健康 / レピュ / セキュ の 6 軸リスク自動追跡 |
| **llforen** | raptor の forensic 機能を FullSense に取り込む |
| **llgov** | EU AI Act / 中国 AI 弁法 / GDPR / SOC2 を要件化する compliance layer |

採用優先度を決めたい. 1 人で順に調査すると 1 件 1 時間で 7 時間. 並列化
するために Claude Code の Agent ツールで 6 体並列に投げた (llforen は
raptor 依存が強いため除外).

### 投入した指示の骨子

各 agent に以下を渡す:

- 担当 vertical の概要 (FullSense 哲学・既存実装との関係)
- 800 字以内で報告書
- Sources 5-10 件 (URL 必須)
- 構成は 3 章: "Stack matrix / Gap / Recommended approach"

### 結果

30 分以内に 6 件揃った. `docs/research/<topic>.md` として保存:

| File | 中身 |
|---|---|
| `lleval_sota.md` | OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse / TruLens / Ragas を整理. **4 つの空白** (on-prem 統一 / progressive size / honest disclosure / self-pref bias) を特定 |
| `llgrow_prior_art.md` | Jasper / Mautic / Langfuse + academic 2025. on-prem + audit + HITL + 個人 OSS 配信の 4 条件は空白 |
| `cognitive_mesh_vs_sota.md` | MemGPT / Generative Agents / A-MEM / Reflexion / Constitutional AI と sub-system 毎に対応づけ |
| `llcraft_sota.md` | TTS / 画像 / 動画 / 音楽 × Tier 1/2/3 license matrix. C2PA + IPTC 2025.1 に license_tier 拡張 |
| `llrisk_prior_art.md` | AI-driven GRC / DevOps risk / LLM × risk register / reputation / developer burnout を 5 縦割りで整理 |
| `llgov_sota.md` | NeMo Guardrails / OPA / Cedar / MS Agent Governance Toolkit / Credo AI の matrix |

### 採用優先度の確定

研究結果を `spinoff_ideas_2026_05.md` の C-2 表に反映:

| vertical | 優先度 | 根拠 |
|---|---|---|
| **lleval** | **HIGH** | promptfoo (Apache-2.0) を fork base にすれば 4 つの空白を埋められる. base に乗るので 0 から作らない |
| **llgrow** | MID | Langfuse + Mautic を再利用すれば基盤新規不要 |
| **llbridge** | MID | LangGraph / AutoGen に対し UI を first-class peer 化する差別化 |
| **llcraft** | LOW | license tier 自動化が差別化候補. GPU 要件高 |
| **llrisk** | LOW | scope が大きい (6 軸). MVP は個人開発者向け 6 軸ダッシュボード |
| **llgov** | LOW | EU AI Act Art.9-15 自動検証 OSS は空白. 規制改定頻度が高い |
| **llforen** | DEFER | raptor 依存が強い. raptor 側安定化待ち |

「人 1 人で 7 時間かかる調査」を「AI agent 並列で 30 分」に短縮した. 並列で
6 体動かしても自分は test 修正を続けていられるので, 縦軸と横軸が干渉しない.

---

## 4. portal の `NEXT_SESSION.auto.md` 自動化 (縦軸 2)

`docs/NEXT_SESSION.md` (人手, 次セッションへの方向性メモ) は drift する.
完全自動化すると「人間が考えた次の方針」が消える. なので 2 ファイル運用に
分離:

![NEXT_SESSION の 2 ファイル運用 (人手の方向性メモ + 自動 snapshot の分離)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q20/next_session_two_file.svg)

`scripts/gen_next_session_auto.py` を新規作成. Stop hook (raptor 側の
`libexec/raptor-next-session-update` ラッパ経由) で毎ターン以下を上書き:

1. **portal git snapshot** — 直近 commit 10 件 + status + upstream との ahead/behind
2. **関連プロジェクト最新状態** — llive / llove / llmesh / lldesign / lltrade の
   最新 commit + `tests/` ディレクトリの直近 mtime
3. **operator action 再抽出** — `NEXT_SESSION.md` の 🧑 セクションを parsing
   して `[ ]` チェックボックス化
4. **`verify_publication` 最新結果** — `out/verify_publication.last` キャッシュの tail 30 行
5. **直近 4 時間に変更された portal ファイル**

raptor 側ラッパは `RAPTOR_CALLER_DIR=<your-path>/fullsense` のときだけ
動く分岐. 他プロジェクトに切替えても無害.

---

## 5. 採用優先度 HIGH の lleval v0.1 要件 draft

採用優先度 HIGH に確定した lleval の v0.1 要件 draft を
`docs/spec/requirements_lleval_v0.1_draft.md` に書いた.

要点:

- **promptfoo を fork base** (Apache-2.0 / CI 親和 / on-prem provider 拡張余地大)
- 観測層は **Phoenix (OpenInference / OTel)**
- RAG metric は **Ragas / TruLens** を adapter で吸収
- 差別化 4 軸:
  1. on-prem + cloud 統一 A/B (`LLMeshProvider` plugin)
  2. Progressive size curve (xs/s/m/l/xl の 5 段階 token sweep)
  3. Honest disclosure analyzer (異常 latency を 5 因子に自動分解)
  4. Judge rotation + position swap (self-preference bias 自動検出)

要件 `LE-01〜08` + 非要件 + 着手 trigger 4 段.

実装着手は user 判断. これは agent 自律 draft であり, ベンチ復旧
(Anthropic / Gemini / OpenAI credential / quota 復旧) と並行で promptfoo
fork PoC を走らせる, という trigger 案を明記している.

---

## 6. このセッションの定量メトリクス

| 指標 | 値 |
|---|---|
| 全テスト緑件数 | **5409** (llive 1518 + llove 805 + llmesh 3086) |
| 1 セッション内 commit 数 | 約 14 (backup-hook auto: commits 含む) |
| 意図 commit (feat / docs / fix / test) | 7 件 |
| 意図 push 数 | 6 件 (portal × 4 + llove × 1 + llmesh × 1) |
| 新規 research メモ | 6 件 |
| 新規 memory (運用則) | 5 件 |
| TaskCreate / 全 complete | 16 件 |
| AI agent dispatch (research) | 6 件 (並列, 全 30 分以内に完了) |
| 環境依存 test 修正 | 8 件 (llove 7 + llmesh は conftest 一括) |

---

## 7. 教訓 (ここまでで学んだこと)

1. **環境依存 test には `monkeypatch.shutil.which` を必ず入れる**. WinGet 等
   パッケージマネージャが背後で PATH を書き換える前提で書く.
2. **Hypothesis flaky は conftest 一括対処**. `register_profile` で
   default を上書きする. 個別 `@settings` で逐次対処すると終わらない.
3. **採用優先度判断には AI agent 並列調査**. 30 分で 6 件の SOTA 報告書が
   揃う. 人間の調査時間に比して桁が違う.
4. **NEXT_SESSION は 2 ファイル運用** (人手の方向性 + 自動 snapshot). drift
   と情報損失を両立しない.
5. **lleval = promptfoo fork** が確定路線. 着手 trigger 待ち.

---

## 8. 次の一日へ

- 環境がさらに変わっていないか, 朝に test 全件 run
- `test_aoi_adapter_processes_synthetic` の順序依存 flaky 根本調査
- raptor リポ origin/main との diverge 解消 (manual merge 必要)
- lleval PoC 着手判断 (ベンチ復旧と並行)

---

## 関連

- [research/lleval_sota](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/lleval_sota.md)
- [research/llgrow_prior_art](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/llgrow_prior_art.md)
- [research/cognitive_mesh_vs_sota](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/cognitive_mesh_vs_sota.md)
- [spinoff_ideas_2026_05](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spinoff_ideas_2026_05.md)
- [requirements_lleval_v0.1_draft](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/requirements_lleval_v0.1_draft)
- [NEXT_SESSION (人手)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.md)
- [NEXT_SESSION (自動)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.auto)

---

# English

# One Session: 5409 Tests Green + 6 Research Hubs Opened — A Day in FullSense

> 📚 **Series nav**: ← #19 AI that runs on a GPU-less PC ｜ **#20 this article** ｜ #21 A 3-day, 8-repo marathon → ｜ [Series LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ Each article also stands on its own (links are for browsing).

> In the morning, 7 tests had turned red. The cause was an environmental change. While fixing it, I set 6 AI agents running in parallel on prior-art research, locked in the adoption priorities for the FullSense spinoffs, automated the portal's progress dashboard, and even finished the v0.1 requirements draft for lleval (adoption priority HIGH) — then pushed everything. This records the density of a single session of "solo OSS developer × autonomous AI development," using only facts and numbers.

---

## 0. How this session was structured

In one session I achieved the following:

- **All tests green across 3 projects** — llive 1518 / llove 805 / llmesh 3086 = **5409 total**
- **Prior-art research with 6 AI agents in parallel** — locked in adoption priorities for 7 FullSense spinoffs (lleval = HIGH)
- **Stop-hook-driven automation of the portal `NEXT_SESSION.auto.md`**
- **v0.1 requirements draft for lleval (adoption priority HIGH)**

Below, in the order things happened, I record the vertical axis (debug → test fix) and the horizontal axis (research → priority judgment).

---

## 1. 7 tests were already red when I woke up

In the first check of the session, 7 of llove's tests were `FAILED`:

```text
FAILED tests/test_dot_render.py::test_render_dot_falls_back_to_ascii_without_image_tool
FAILED tests/test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg
FAILED tests/test_mermaid_render.py::test_render_mermaid_falls_back_to_ascii_without_image_tool
FAILED tests/test_plantuml_render.py::test_render_plantuml_falls_back_to_ascii_without_image_tool
FAILED tests/test_svg_render.py::test_render_svg_falls_back_to_ascii_without_image_tool
FAILED tests/test_svgbob_render.py::test_render_svgbob_falls_back_to_ascii_without_image_tool
```

The code had not been touched since the previous session. Yet it was red. Running just the first one, the assert was:

```text
AssertionError: assert 'image' == 'ascii'
```

Expected: `result.kind == "ascii"` (no image tool, so ASCII fallback)
Actual: `result.kind == "image"` (the image renderer ran)

### Root cause

Each of llove's renderers (mermaid / svg / dot / plantuml / svgbob) decides on a fallback with this check:

```python
resolved_tool = image_tool if image_tool is not None else find_image_tool()

if not resolved_svgbob or resolved_tool is None:
    return SvgbobRender(kind="ascii", ascii_text=ascii_fallback(source))
```

`find_image_tool()` internally calls things like `shutil.which("chafa")`. The test passes `image_tool=None`, but **the implementation interprets `None` not as "explicitly none" but as "instruction to auto-detect."**

Up to here, this is ordinary Python and there is no problem. The problem was happening on the environment side:

- The day before (on the environment), **WinGet registered `chafa.exe` onto the PATH**
  (`C:\Users\<user>\AppData\Local\Microsoft\WinGet\Links\Chafa.exe`)
- `find_image_tool()` picks it up
- The ASCII fallback branch is never taken → the test fails

### The fix

Suppress all of `monkeypatch.shutil.which` by returning None.

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

The 5 tests (dot / mermaid / plantuml / svg / svgbob) were fixed with the same pattern. The 6th, `test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg`, goes through multiple renderer modules inside MarkdownView, so I applied the same suppression to all modules in a for loop:

```python
for mod in (dot_render, mermaid_render, plantuml_render, svg_render, svgbob_render):
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
```

`test_e2e_real_chafa.py`, which requires the real binary, is a separate matter: a new case had appeared where even with `mmdc` on the PATH, execution failed. I added a two-stage guard that detects a None result inside the test and drops into `pytest.skip()`.

### Lesson

If you write code that detects an optional binary via `shutil.which`, always monkeypatch `shutil.which` on the test side. The environment changes without warning.

I recorded this lesson as an operating rule in the memory `feedback_env_dependent_tests`.

---

## 2. llmesh's Hypothesis tests were also flaky with DeadlineExceeded

After fixing llove, the property tests on the llmesh side started failing one after another with DeadlineExceeded:

```text
hypothesis.errors.DeadlineExceeded: Test took 490.69ms, which exceeds the deadline of 200.00ms.
```

Hypothesis's default deadline is **200ms**. On Windows, first-time file IO or import can easily exceed it.

### Fixing them individually is a losing game

At first I added `@settings(deadline=None)` to individual tests. But:

- I fixed `test_audit_chain_verify_succeeds_after_clean_appends`
- and on the next run `test_audit_chain_verify_fails_after_tamper` failed for the same reason
- I fixed that too, and `test_codec_json_roundtrip` failed

llmesh has dozens of property tests; fixing them individually never ends.

### Consolidate the profile in conftest.py

Register a hypothesis profile in `tests/conftest.py`.

```python
from hypothesis import settings

# Windows での初回 file IO / import / hypothesis warmup で 200ms deadline を
# 超えるケースが頻発するため, llmesh の全 property test で deadline を
# 無効化する. 個別 test で @settings(deadline=...) を上書きすれば優先.
settings.register_profile("local-flaky-safe", deadline=None)
settings.load_profile("local-flaky-safe")
```

Now every hypothesis test receives `deadline=None` as the default. Tests that wrote their own `@settings(...)` take precedence, so existing tests don't break.

Result: llmesh **all 3086 green** (12 min 20 s). Had I kept fixing them one by one, I would have lost half a day.

I recorded the lesson in the memory `feedback_hypothesis_deadline`.

---

## 3. Prior-art research with 6 AI agents in parallel (horizontal axis)

Here I paused the vertical axis (debug) and switched to the horizontal axis (research).

The FullSense umbrella has 7 spinoff candidates:

| Candidate | One-liner |
|---|---|
| **llgrow** | Growth / monetization automation for individual developers (HITL content generation) |
| **lleval** | A framework dedicated to LLM benchmarking and evaluation |
| **llcraft** | On-prem creative-asset generation (TTS / image / video / music) |
| **llbridge** | Multi-AI orchestration (Claude / GPT / Gemini / Codex) |
| **llrisk** | Automatic tracking of 6-axis risk: legal / technical / business / health / reputation / security |
| **llforen** | Bringing raptor's forensic features into FullSense |
| **llgov** | A compliance layer that turns EU AI Act / China's AI measures / GDPR / SOC2 into requirements |

I wanted to set adoption priorities. Researching them one by one alone would take 1 hour each, 7 hours total. To parallelize, I dispatched 6 agents in parallel with Claude Code's Agent tool (llforen was excluded because its raptor dependency is too strong).

### The gist of the instructions given

Each agent was given the following:

- An overview of its assigned vertical (FullSense philosophy and relationship to the existing implementation)
- A report within 800 characters
- 5–10 sources (URLs required)
- A 3-chapter structure: "Stack matrix / Gap / Recommended approach"

### Results

Within 30 minutes, 6 came back. Saved as `docs/research/<topic>.md`:

| File | Contents |
|---|---|
| `lleval_sota.md` | Organizes OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse / TruLens / Ragas. Identifies **4 gaps** (on-prem unification / progressive size / honest disclosure / self-pref bias) |
| `llgrow_prior_art.md` | Jasper / Mautic / Langfuse + academic 2025. The 4 conditions of on-prem + audit + HITL + individual-OSS distribution are a gap |
| `cognitive_mesh_vs_sota.md` | Maps MemGPT / Generative Agents / A-MEM / Reflexion / Constitutional AI per sub-system |
| `llcraft_sota.md` | TTS / image / video / music × Tier 1/2/3 license matrix. Extend C2PA + IPTC 2025.1 with license_tier |
| `llrisk_prior_art.md` | Organizes AI-driven GRC / DevOps risk / LLM × risk register / reputation / developer burnout across 5 verticals |
| `llgov_sota.md` | A matrix of NeMo Guardrails / OPA / Cedar / MS Agent Governance Toolkit / Credo AI |

### Locking in adoption priorities

The research results were reflected in the C-2 table of `spinoff_ideas_2026_05.md`:

| vertical | Priority | Rationale |
|---|---|---|
| **lleval** | **HIGH** | Forking promptfoo (Apache-2.0) as the base lets us fill the 4 gaps. Riding on the base means not building from zero |
| **llgrow** | MID | Reusing Langfuse + Mautic means no new foundation needed |
| **llbridge** | MID | Differentiation by making the UI a first-class peer versus LangGraph / AutoGen |
| **llcraft** | LOW | License-tier automation is a differentiation candidate. High GPU requirements |
| **llrisk** | LOW | Large scope (6 axes). The MVP is a 6-axis dashboard for individual developers |
| **llgov** | LOW | EU AI Act Art.9-15 auto-verification OSS is a gap. High frequency of regulatory revisions |
| **llforen** | DEFER | Strong raptor dependency. Waiting for the raptor side to stabilize |

I shrank "research that takes one person 7 hours" into "30 minutes with AI agents in parallel." Even with 6 running in parallel, I could keep fixing tests myself, so the vertical and horizontal axes don't interfere.

---

## 4. Automating the portal's `NEXT_SESSION.auto.md` (vertical axis 2)

`docs/NEXT_SESSION.md` (manual, a direction memo for the next session) drifts. Fully automating it would erase "the next direction a human thought up." So I split it into a two-file scheme:

![NEXT_SESSION two-file scheme (manual direction memo + automatic snapshot)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q20/next_session_two_file_en.svg)

I newly created `scripts/gen_next_session_auto.py`. With a Stop hook (via the raptor-side wrapper `libexec/raptor-next-session-update`), it overwrites the following every turn:

1. **portal git snapshot** — last 10 commits + status + ahead/behind versus upstream
2. **Latest state of related projects** — latest commits of llive / llove / llmesh / lldesign / lltrade + the most recent mtime of the `tests/` directory
3. **Re-extraction of operator actions** — parses the 🧑 section of `NEXT_SESSION.md` and turns it into `[ ]` checkboxes
4. **Latest `verify_publication` result** — tail 30 lines of the `out/verify_publication.last` cache
5. **portal files changed in the last 4 hours**

The raptor-side wrapper has a branch that runs only when `RAPTOR_CALLER_DIR=<your-path>/fullsense`. It's harmless even after switching to another project.

---

## 5. v0.1 requirements draft for lleval (adoption priority HIGH)

I wrote the v0.1 requirements draft for lleval, which was locked in at adoption priority HIGH, in `docs/spec/requirements_lleval_v0.1_draft.md`.

Key points:

- **Fork promptfoo as the base** (Apache-2.0 / CI-friendly / large room for on-prem provider extension)
- The observation layer is **Phoenix (OpenInference / OTel)**
- RAG metrics are absorbed via adapters from **Ragas / TruLens**
- 4 axes of differentiation:
  1. Unified on-prem + cloud A/B (`LLMeshProvider` plugin)
  2. Progressive size curve (a 5-stage token sweep of xs/s/m/l/xl)
  3. Honest disclosure analyzer (auto-decomposes anomalous latency into 5 factors)
  4. Judge rotation + position swap (auto-detection of self-preference bias)

Requirements `LE-01–08` + non-requirements + 4 stages of kick-off triggers.

The decision to start implementation is the user's. This is an agent-autonomous draft; it explicitly notes a trigger proposal to run the promptfoo fork PoC in parallel with benchmark recovery (recovery of Anthropic / Gemini / OpenAI credentials / quotas).

---

## 6. Quantitative metrics for this session

| Metric | Value |
|---|---|
| Number of tests green | **5409** (llive 1518 + llove 805 + llmesh 3086) |
| Commits within one session | ~14 (including backup-hook auto: commits) |
| Intentional commits (feat / docs / fix / test) | 7 |
| Intentional pushes | 6 (portal × 4 + llove × 1 + llmesh × 1) |
| New research memos | 6 |
| New memories (operating rules) | 5 |
| TaskCreate / all complete | 16 |
| AI agent dispatches (research) | 6 (parallel, all done within 30 min) |
| Environment-dependent test fixes | 8 (llove 7 + llmesh consolidated in conftest) |

---

## 7. Lessons (what I learned so far)

1. **Always put `monkeypatch.shutil.which` into environment-dependent tests.** Write on the assumption that a package manager like WinGet rewrites the PATH behind your back.
2. **Handle Hypothesis flakiness all at once in conftest.** Override the default with `register_profile`. Handling it sequentially with individual `@settings` never ends.
3. **Use parallel AI-agent research for adoption-priority judgments.** In 30 minutes you get 6 SOTA reports. It's an order of magnitude different from human research time.
4. **Run NEXT_SESSION as two files** (manual direction + automatic snapshot). Don't trade off between drift and information loss.
5. **lleval = promptfoo fork** is the confirmed route. Waiting for the kick-off trigger.

---

## 8. Toward the next day

- Run all tests in the morning to check whether the environment has changed further
- Root-cause investigation of the order-dependent flaky `test_aoi_adapter_processes_synthetic`
- Resolve the divergence of the raptor repo with origin/main (manual merge needed)
- Decision on starting the lleval PoC (in parallel with benchmark recovery)

---

## Related

- [research/lleval_sota](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/lleval_sota.md)
- [research/llgrow_prior_art](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/llgrow_prior_art.md)
- [research/cognitive_mesh_vs_sota](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/cognitive_mesh_vs_sota.md)
- [spinoff_ideas_2026_05](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spinoff_ideas_2026_05.md)
- [requirements_lleval_v0.1_draft](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/requirements_lleval_v0.1_draft)
- [NEXT_SESSION (manual)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.md)
- [NEXT_SESSION (auto)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.auto)

---

# 中文

# 一次会话：5409 个测试全绿 + 开设 6 个 research hub —— FullSense 的一天

> 📚 **连载导航**：← #19 在无 GPU 的 PC 上运行的 AI ｜ **#20 本文** ｜ #21 三天 8 个仓库的 marathon → ｜ [连载 LINK_MAP](./QIITA_#24_LINK_MAP.md)。※ 每篇文章都可单独阅读（链接用于串读）。

> 早上起来发现有 7 个测试变红了，查明原因是环境变化。在修复的同时，我让 6 个 AI agent 并行去做先行研究调查，确定了 FullSense 各 spinoff 的采用优先级，自动化了 portal 的进度仪表盘，甚至把采用优先级 HIGH 的 lleval v0.1 需求 draft 也写完，然后全部 push 了——本文只用事实和数字，记录「个人 OSS 开发者 × 自律 AI 开发」一次会话的密度。

---

## 0. 本次会话的构成

在一次会话中我完成了以下事项：

- **3 个项目的全部测试转绿** —— llive 1518 / llove 805 / llmesh 3086 = 共 **5409 件**
- **6 个 AI agent 并行做先行研究调查** —— 确定了 FullSense 7 个 spinoff 的采用优先级（lleval = HIGH）
- **portal `NEXT_SESSION.auto.md` 的 Stop hook 联动自动化**
- **采用优先级 HIGH 的 lleval v0.1 需求 draft**

下面按发生顺序，记录纵轴（debug → test fix）与横轴（research → 优先级判定）。

---

## 1. 早上起床时有 7 个测试已经是红的

会话最初的检查中，llove 有 7 个测试是 `FAILED`：

```text
FAILED tests/test_dot_render.py::test_render_dot_falls_back_to_ascii_without_image_tool
FAILED tests/test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg
FAILED tests/test_mermaid_render.py::test_render_mermaid_falls_back_to_ascii_without_image_tool
FAILED tests/test_plantuml_render.py::test_render_plantuml_falls_back_to_ascii_without_image_tool
FAILED tests/test_svg_render.py::test_render_svg_falls_back_to_ascii_without_image_tool
FAILED tests/test_svgbob_render.py::test_render_svgbob_falls_back_to_ascii_without_image_tool
```

代码自上次会话以来并未改动，却变红了。单独执行第 1 个时，assert 是：

```text
AssertionError: assert 'image' == 'ascii'
```

期望：`result.kind == "ascii"`（没有图像工具，所以走 ASCII fallback）
现实：`result.kind == "image"`（图像 renderer 跑起来了）

### 原因

llove 的各个 renderer（mermaid / svg / dot / plantuml / svgbob）用如下判断来决定 fallback：

```python
resolved_tool = image_tool if image_tool is not None else find_image_tool()

if not resolved_svgbob or resolved_tool is None:
    return SvgbobRender(kind="ascii", ascii_text=ascii_fallback(source))
```

`find_image_tool()` 内部会调用 `shutil.which("chafa")` 之类。测试侧传入的是 `image_tool=None`，但**实现把 `None` 解释为「自动探测指示」，而非「明确指定为无」**。

到这里都还是普通的 Python 写法，没有问题。问题出在环境侧：

- 前一天（在环境上）**WinGet 把 `chafa.exe` 注册到了 PATH 上**
  （`C:\Users\<user>\AppData\Local\Microsoft\WinGet\Links\Chafa.exe`）
- `find_image_tool()` 把它捡了起来
- 于是没有走 ASCII fallback 分支 → 测试失败

### 修复

把 `monkeypatch.shutil.which` 全部抑制为返回 None。

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

这 5 个测试（dot / mermaid / plantuml / svg / svgbob）用同样的模式修复。第 6 个 `test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg` 在 MarkdownView 内部会经过多个 renderer module，所以用 for 循环对所有 module 应用同样的抑制：

```python
for mod in (dot_render, mermaid_render, plantuml_render, svg_render, svgbob_render):
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
```

必须依赖真实 binary 的 `test_e2e_real_chafa.py` 是另一回事：新出现了一种情况，即使 PATH 上有 `mmdc`，执行也会失败。我在测试内增加了一个两段式守卫，检测到 None 结果就降级到 `pytest.skip()`。

### 教训

如果你写了用 `shutil.which` 探测 optional binary 的代码，那么测试侧务必 monkeypatch `shutil.which`。环境会毫无预兆地变化。

这条教训作为运用规则记录在了 memory `feedback_env_dependent_tests` 里。

---

## 2. llmesh 的 Hypothesis test 也因 DeadlineExceeded 而 flaky

修完 llove 后，llmesh 侧的 property test 开始接连因 DeadlineExceeded 而 fail：

```text
hypothesis.errors.DeadlineExceeded: Test took 490.69ms, which exceeds the deadline of 200.00ms.
```

Hypothesis 的默认 deadline 是 **200ms**。在 Windows 环境下，首次文件 IO 或 import 很容易就超出了。

### 逐个对付会输

最初我对个别 test 加了 `@settings(deadline=None)`。但是：

- 我修好了 `test_audit_chain_verify_succeeds_after_clean_appends`
- 下一次 run 时 `test_audit_chain_verify_fails_after_tamper` 又因同样的原因 fail
- 那个也修好后，`test_codec_json_roundtrip` 又 fail 了

llmesh 有数十个 property test，逐个对付永远修不完。

### 在 conftest.py 里统一 profile

在 `tests/conftest.py` 里注册一个 hypothesis profile。

```python
from hypothesis import settings

# Windows での初回 file IO / import / hypothesis warmup で 200ms deadline を
# 超えるケースが頻発するため, llmesh の全 property test で deadline を
# 無効化する. 個別 test で @settings(deadline=...) を上書きすれば優先.
settings.register_profile("local-flaky-safe", deadline=None)
settings.load_profile("local-flaky-safe")
```

这样所有 hypothesis test 都把 `deadline=None` 当作默认接收。写了自己 `@settings(...)` 的 test 以那个为优先，所以既有 test 不会被破坏。

结果：llmesh **3086 件全部转绿**（12 分 20 秒）。要是继续逐个对付，我会损失半天。

教训记录在了 memory `feedback_hypothesis_deadline` 里。

---

## 3. 6 个 AI agent 并行做先行研究调查（横轴）

到这里我暂停纵轴（debug），切换到横轴（research）。

FullSense umbrella 有 7 个 spinoff 候选：

| 候选 | 一句话 |
|---|---|
| **llgrow** | 面向个人开发者的成长 / 变现自动化（HITL 内容生成） |
| **lleval** | 专用于 LLM 基准测试 / 评估的 framework |
| **llcraft** | on-prem 创意素材生成（TTS / 图像 / 视频 / 音乐） |
| **llbridge** | multi-AI orchestration（Claude / GPT / Gemini / Codex） |
| **llrisk** | 法务 / 技术 / 商业 / 健康 / 声誉 / 安全 6 轴风险自动追踪 |
| **llforen** | 把 raptor 的 forensic 功能纳入 FullSense |
| **llgov** | 把 EU AI Act / 中国 AI 办法 / GDPR / SOC2 需求化的 compliance layer |

我想确定采用优先级。一个人挨个调查的话，每件 1 小时，共 7 小时。为了并行化，我用 Claude Code 的 Agent 工具同时投了 6 个（llforen 因为对 raptor 依赖太强而排除）。

### 投入指示的骨架

给每个 agent 的内容如下：

- 所负责 vertical 的概要（FullSense 哲学 · 与既有实现的关系）
- 800 字以内的报告书
- 5–10 个 Sources（必须有 URL）
- 结构为 3 章："Stack matrix / Gap / Recommended approach"

### 结果

30 分钟内 6 件全部齐了。作为 `docs/research/<topic>.md` 保存：

| File | 内容 |
|---|---|
| `lleval_sota.md` | 整理 OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse / TruLens / Ragas。识别出 **4 个空白**（on-prem 统一 / progressive size / honest disclosure / self-pref bias） |
| `llgrow_prior_art.md` | Jasper / Mautic / Langfuse + academic 2025。on-prem + audit + HITL + 个人 OSS 分发这 4 个条件是空白 |
| `cognitive_mesh_vs_sota.md` | 把 MemGPT / Generative Agents / A-MEM / Reflexion / Constitutional AI 按 sub-system 逐一对应 |
| `llcraft_sota.md` | TTS / 图像 / 视频 / 音乐 × Tier 1/2/3 license matrix。给 C2PA + IPTC 2025.1 扩展 license_tier |
| `llrisk_prior_art.md` | 把 AI-driven GRC / DevOps risk / LLM × risk register / reputation / developer burnout 按 5 个纵向整理 |
| `llgov_sota.md` | NeMo Guardrails / OPA / Cedar / MS Agent Governance Toolkit / Credo AI 的 matrix |

### 确定采用优先级

研究结果反映到了 `spinoff_ideas_2026_05.md` 的 C-2 表里：

| vertical | 优先级 | 依据 |
|---|---|---|
| **lleval** | **HIGH** | 把 promptfoo（Apache-2.0）作为 fork base，就能填上那 4 个空白。乘在 base 上，不必从 0 开始做 |
| **llgrow** | MID | 复用 Langfuse + Mautic，就不需要新建基盘 |
| **llbridge** | MID | 相对 LangGraph / AutoGen，把 UI 提升为 first-class peer 的差异化 |
| **llcraft** | LOW | license tier 自动化是差异化候选。GPU 要求高 |
| **llrisk** | LOW | scope 大（6 轴）。MVP 是面向个人开发者的 6 轴仪表盘 |
| **llgov** | LOW | EU AI Act Art.9-15 自动验证 OSS 是空白。法规修订频率高 |
| **llforen** | DEFER | 对 raptor 依赖强。等 raptor 侧稳定 |

我把「一个人要 7 小时的调查」缩短成了「AI agent 并行 30 分钟」。即便同时跑 6 个，我自己也能继续修测试，所以纵轴和横轴互不干扰。

---

## 4. portal 的 `NEXT_SESSION.auto.md` 自动化（纵轴 2）

`docs/NEXT_SESSION.md`（人手，给下次会话的方向性备忘）会 drift。完全自动化的话，「人类想出来的下一步方针」就会消失。所以分成 2 文件运用：

![NEXT_SESSION 的 2 文件运用（人手方向性备忘 + 自动 snapshot 的分离）](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q20/next_session_two_file_zh.svg)

新建了 `scripts/gen_next_session_auto.py`。通过 Stop hook（经由 raptor 侧的 `libexec/raptor-next-session-update` 包装器），每个 turn 覆写以下内容：

1. **portal git snapshot** —— 最近 10 个 commit + status + 与 upstream 的 ahead/behind
2. **相关项目的最新状态** —— llive / llove / llmesh / lldesign / lltrade 的最新 commit + `tests/` 目录的最近 mtime
3. **operator action 再抽取** —— parse `NEXT_SESSION.md` 的 🧑 章节，转成 `[ ]` 复选框
4. **`verify_publication` 最新结果** —— `out/verify_publication.last` 缓存的 tail 30 行
5. **最近 4 小时内变更的 portal 文件**

raptor 侧包装器有一个仅在 `RAPTOR_CALLER_DIR=<your-path>/fullsense` 时才运行的分支。即使切换到其他项目也无害。

---

## 5. 采用优先级 HIGH 的 lleval v0.1 需求 draft

我把确定为采用优先级 HIGH 的 lleval 的 v0.1 需求 draft 写在了 `docs/spec/requirements_lleval_v0.1_draft.md`。

要点：

- **以 promptfoo 为 fork base**（Apache-2.0 / 与 CI 亲和 / on-prem provider 扩展余地大）
- 观测层为 **Phoenix（OpenInference / OTel）**
- RAG metric 通过 adapter 从 **Ragas / TruLens** 吸收
- 差异化 4 轴：
  1. on-prem + cloud 统一 A/B（`LLMeshProvider` plugin）
  2. Progressive size curve（xs/s/m/l/xl 的 5 段 token sweep）
  3. Honest disclosure analyzer（把异常 latency 自动分解为 5 因子）
  4. Judge rotation + position swap（self-preference bias 自动检测）

需求 `LE-01~08` + 非需求 + 着手 trigger 4 段。

是否着手实现由 user 判断。这是 agent 自律 draft，其中明确写了一个 trigger 方案：在 benchmark 复原（Anthropic / Gemini / OpenAI credential / quota 复原）的同时，并行跑 promptfoo fork PoC。

---

## 6. 本次会话的定量指标

| 指标 | 值 |
|---|---|
| 全测试转绿件数 | **5409**（llive 1518 + llove 805 + llmesh 3086） |
| 一次会话内 commit 数 | 约 14（含 backup-hook auto: commits） |
| 意图 commit（feat / docs / fix / test） | 7 件 |
| 意图 push 数 | 6 件（portal × 4 + llove × 1 + llmesh × 1） |
| 新增 research 备忘 | 6 件 |
| 新增 memory（运用规则） | 5 件 |
| TaskCreate / 全部 complete | 16 件 |
| AI agent dispatch（research） | 6 件（并行，全部 30 分钟内完成） |
| 环境依赖 test 修复 | 8 件（llove 7 + llmesh 在 conftest 一括处理） |

---

## 7. 教训（到目前为止学到的）

1. **环境依赖的 test 一定要放入 `monkeypatch.shutil.which`**。要按「WinGet 等包管理器会在背后改写 PATH」的前提来写。
2. **Hypothesis flaky 要在 conftest 一括处理**。用 `register_profile` 覆写默认值。用个别 `@settings` 逐个对付永远修不完。
3. **采用优先级判断要用 AI agent 并行调查**。30 分钟就能凑齐 6 份 SOTA 报告书。相比人类的调查时间，差了一个数量级。
4. **NEXT_SESSION 用 2 文件运用**（人手的方向性 + 自动 snapshot）。不在 drift 与信息损失之间二选一。
5. **lleval = promptfoo fork** 是确定的路线。等着手 trigger。

---

## 8. 走向下一天

- 早上 run 全部测试，确认环境有没有进一步变化
- 对顺序依赖的 flaky `test_aoi_adapter_processes_synthetic` 做根本调查
- 解决 raptor 仓库与 origin/main 的 diverge（需要 manual merge）
- lleval PoC 着手判断（与 benchmark 复原并行）

---

## 相关

- [research/lleval_sota](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/lleval_sota.md)
- [research/llgrow_prior_art](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/llgrow_prior_art.md)
- [research/cognitive_mesh_vs_sota](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/cognitive_mesh_vs_sota.md)
- [spinoff_ideas_2026_05](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spinoff_ideas_2026_05.md)
- [requirements_lleval_v0.1_draft](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/requirements_lleval_v0.1_draft)
- [NEXT_SESSION（人手）](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.md)
- [NEXT_SESSION（自动）](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.auto)

---

# 한국어

# 한 세션으로 5409 테스트 그린 + research hub 6개 개설 — FullSense의 하루

> 📚 **연재 내비**: ← #19 GPU 없는 PC에서 도는 AI ｜ **#20 본 글** ｜ #21 3일간 8개 리포 marathon → ｜ [연재 LINK_MAP](./QIITA_#24_LINK_MAP.md). ※ 각 글은 단독으로도 읽을 수 있습니다(링크는 회유용).

> 아침에 테스트 7건이 빨갛게 되어 있었고, 원인이 환경 변화로 판명되었다. 수정과 동시에 AI agent 6대를 병렬로 선행 연구 조사에 투입하고, FullSense spinoff들의 채택 우선순위를 확정하고, portal의 진척 대시보드를 자동화하고, 채택 우선순위 HIGH인 lleval v0.1 요구사항 draft까지 마무리한 뒤 전부 push했다 — 개인 OSS 개발자 × 자율 AI 개발의 한 세션의 밀도를, 사실과 숫자만으로 남긴다.

---

## 0. 이 세션의 구성

한 세션으로 다음을 달성했다:

- **3개 프로젝트의 전 테스트 그린** — llive 1518 / llove 805 / llmesh 3086 = 총 **5409건**
- **AI agent 6대 병렬로 선행 연구 조사** — FullSense의 spinoff 7건의 채택 우선순위를 확정(lleval = HIGH)
- **portal `NEXT_SESSION.auto.md`의 Stop hook 연동 자동화**
- **채택 우선순위 HIGH인 lleval v0.1 요구사항 draft**

아래에 일어난 순서대로 세로축(debug → test fix)과 가로축(research → 우선순위 판정)을 기록한다.

---

## 1. 아침에 일어나니 테스트 7건이 빨갰던 건

세션 최초의 확인에서, llove의 테스트 7건이 `FAILED`였다:

```text
FAILED tests/test_dot_render.py::test_render_dot_falls_back_to_ascii_without_image_tool
FAILED tests/test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg
FAILED tests/test_mermaid_render.py::test_render_mermaid_falls_back_to_ascii_without_image_tool
FAILED tests/test_plantuml_render.py::test_render_plantuml_falls_back_to_ascii_without_image_tool
FAILED tests/test_svg_render.py::test_render_svg_falls_back_to_ascii_without_image_tool
FAILED tests/test_svgbob_render.py::test_render_svgbob_falls_back_to_ascii_without_image_tool
```

코드는 지난 세션 이후 건드리지 않았다. 그런데도 빨갛게 되어 있다. 단독으로 실행하면 1번째의 assert는:

```text
AssertionError: assert 'image' == 'ascii'
```

기대: `result.kind == "ascii"`(이미지 툴이 없으니 ASCII fallback)
현실: `result.kind == "image"`(이미지 renderer가 돌았다)

### 원인

llove의 각 renderer(mermaid / svg / dot / plantuml / svgbob)는 다음 판정으로 fallback을 결정한다:

```python
resolved_tool = image_tool if image_tool is not None else find_image_tool()

if not resolved_svgbob or resolved_tool is None:
    return SvgbobRender(kind="ascii", ascii_text=ascii_fallback(source))
```

`find_image_tool()`는 내부에서 `shutil.which("chafa")` 등을 호출한다. 테스트 쪽은 `image_tool=None`을 넘기지만, **구현은 `None`을 「명시적으로 없음」이 아니라 「auto detect 지시」로 해석하는 설계**다.

여기까지는 평범한 Python의 작성 방식이라 문제는 없다. 문제는 환경 쪽에서 일어나고 있었다:

- 전날(환경상) **WinGet이 `chafa.exe`를 PATH에 등록했다**
  (`C:\Users\<user>\AppData\Local\Microsoft\WinGet\Links\Chafa.exe`)
- `find_image_tool()`가 그것을 주워 버린다
- ASCII fallback 경로로 내려가지 않는다 → 테스트 실패

### 수정

`monkeypatch.shutil.which`를 전부 None으로 억제한다.

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

5건(dot / mermaid / plantuml / svg / svgbob)은 같은 패턴으로 수정. 6번째 `test_markdown_view_svg.py::test_default_renderers_cover_mermaid_and_svg`는 MarkdownView 내부에서 여러 renderer module을 경유하므로, for 루프로 전 module에 같은 억제를 적용:

```python
for mod in (dot_render, mermaid_render, plantuml_render, svg_render, svgbob_render):
    monkeypatch.setattr(mod.shutil, "which", lambda name: None)
```

실 binary 필수인 `test_e2e_real_chafa.py`는 별건으로, `mmdc`가 PATH에 있어도 실행에서 실패하는 케이스가 새로 발생하고 있었다. 테스트 내에서 결과 None을 감지해 `pytest.skip()`으로 내려가는 2단 구성을 추가했다.

### 교훈

`shutil.which`로 optional binary를 탐지하는 코드를 작성한 경우, 테스트 쪽에서 `shutil.which`를 반드시 monkeypatch 한다. 환경은 예고 없이 바뀐다.

이 교훈은 memory `feedback_env_dependent_tests`에 운용 규칙으로 기록했다.

---

## 2. llmesh의 Hypothesis test도 DeadlineExceeded로 flaky였다

llove 수정 후, llmesh 쪽에서 property test가 잇따라 DeadlineExceeded로 fail하기 시작했다:

```text
hypothesis.errors.DeadlineExceeded: Test took 490.69ms, which exceeds the deadline of 200.00ms.
```

Hypothesis의 기본 deadline은 **200ms**. Windows 환경에서는 첫 파일 IO나 import로 쉽게 초과한다.

### 개별 대처로는 진다

처음에는 `@settings(deadline=None)`을 개별 test에 추가했다. 그런데,

- `test_audit_chain_verify_succeeds_after_clean_appends`를 고치면
- 다음 run에서 `test_audit_chain_verify_fails_after_tamper`가 같은 이유로 fail
- 그것도 고치면 `test_codec_json_roundtrip`가 fail

llmesh의 property test는 수십 건 있어서, 개별 대처는 끝나지 않는다.

### conftest.py에서 profile 일괄화

`tests/conftest.py`에 hypothesis profile을 등록한다.

```python
from hypothesis import settings

# Windows での初回 file IO / import / hypothesis warmup で 200ms deadline を
# 超えるケースが頻発するため, llmesh の全 property test で deadline を
# 無効化する. 個別 test で @settings(deadline=...) を上書きすれば優先.
settings.register_profile("local-flaky-safe", deadline=None)
settings.load_profile("local-flaky-safe")
```

이로써 모든 hypothesis test가 `deadline=None`을 default로 받는다. 개별 `@settings(...)`를 작성한 test는 그쪽이 우선이므로, 기존 test는 깨지지 않는다.

결과: llmesh **3086건 전부 그린**(12분 20초). 개별 대처를 계속했다면 반나절을 잃었을 것이다.

교훈은 memory `feedback_hypothesis_deadline`에 기록했다.

---

## 3. AI agent 6대 병렬로 선행 연구 조사 (가로축)

여기서 세로축(debug)을 일단 멈추고, 가로축(research)으로 전환한다.

FullSense umbrella에는 spinoff 후보가 7개 있다:

| 후보 | 한 줄 |
|---|---|
| **llgrow** | 개인 개발자용 성장 / 수익화 자동화 (HITL 콘텐츠 생성) |
| **lleval** | LLM 벤치 · 평가 전용 framework |
| **llcraft** | on-prem 크리에이티브 소재 생성 (TTS / 이미지 / 영상 / 음악) |
| **llbridge** | multi-AI orchestration (Claude / GPT / Gemini / Codex) |
| **llrisk** | 법무 / 기술 / 비즈니스 / 건강 / 평판 / 보안의 6축 리스크 자동 추적 |
| **llforen** | raptor의 forensic 기능을 FullSense에 도입 |
| **llgov** | EU AI Act / 중국 AI 판법 / GDPR / SOC2를 요구사항화하는 compliance layer |

채택 우선순위를 정하고 싶다. 혼자서 차례대로 조사하면 1건 1시간으로 7시간. 병렬화하기 위해 Claude Code의 Agent 툴로 6대 병렬로 던졌다(llforen은 raptor 의존이 강해서 제외).

### 투입한 지시의 골자

각 agent에 다음을 건넨다:

- 담당 vertical의 개요 (FullSense 철학 · 기존 구현과의 관계)
- 800자 이내의 보고서
- Sources 5–10건 (URL 필수)
- 구성은 3장: "Stack matrix / Gap / Recommended approach"

### 결과

30분 이내에 6건이 갖춰졌다. `docs/research/<topic>.md`로 저장:

| File | 내용 |
|---|---|
| `lleval_sota.md` | OpenAI Evals / lmsys / HELM / promptfoo / DeepEval / Phoenix / Langfuse / TruLens / Ragas를 정리. **4개의 공백**(on-prem 통일 / progressive size / honest disclosure / self-pref bias)을 특정 |
| `llgrow_prior_art.md` | Jasper / Mautic / Langfuse + academic 2025. on-prem + audit + HITL + 개인 OSS 배포의 4조건은 공백 |
| `cognitive_mesh_vs_sota.md` | MemGPT / Generative Agents / A-MEM / Reflexion / Constitutional AI와 sub-system별로 대응 |
| `llcraft_sota.md` | TTS / 이미지 / 영상 / 음악 × Tier 1/2/3 license matrix. C2PA + IPTC 2025.1에 license_tier 확장 |
| `llrisk_prior_art.md` | AI-driven GRC / DevOps risk / LLM × risk register / reputation / developer burnout을 5개 세로로 정리 |
| `llgov_sota.md` | NeMo Guardrails / OPA / Cedar / MS Agent Governance Toolkit / Credo AI의 matrix |

### 채택 우선순위의 확정

연구 결과를 `spinoff_ideas_2026_05.md`의 C-2 표에 반영:

| vertical | 우선순위 | 근거 |
|---|---|---|
| **lleval** | **HIGH** | promptfoo(Apache-2.0)를 fork base로 하면 4개의 공백을 메울 수 있다. base에 올라타니 0부터 만들지 않는다 |
| **llgrow** | MID | Langfuse + Mautic을 재이용하면 기반 신규 불필요 |
| **llbridge** | MID | LangGraph / AutoGen에 대해 UI를 first-class peer화하는 차별화 |
| **llcraft** | LOW | license tier 자동화가 차별화 후보. GPU 요구 높음 |
| **llrisk** | LOW | scope가 크다(6축). MVP는 개인 개발자용 6축 대시보드 |
| **llgov** | LOW | EU AI Act Art.9-15 자동 검증 OSS는 공백. 규제 개정 빈도가 높음 |
| **llforen** | DEFER | raptor 의존이 강하다. raptor 쪽 안정화 대기 |

「혼자서 7시간 걸리는 조사」를 「AI agent 병렬로 30분」으로 단축했다. 병렬로 6대 돌려도 나는 test 수정을 계속할 수 있으므로, 세로축과 가로축이 간섭하지 않는다.

---

## 4. portal의 `NEXT_SESSION.auto.md` 자동화 (세로축 2)

`docs/NEXT_SESSION.md`(사람 손, 다음 세션으로의 방향성 메모)는 drift한다. 완전 자동화하면 「사람이 생각한 다음 방침」이 사라진다. 그래서 2파일 운용으로 분리:

![NEXT_SESSION 2파일 운용 (수동 방향성 메모 + 자동 snapshot 분리)](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_misc/q20/next_session_two_file_ko.svg)

`scripts/gen_next_session_auto.py`를 신규 작성. Stop hook(raptor 쪽 `libexec/raptor-next-session-update` 래퍼 경유)으로 매 턴 다음을 덮어쓴다:

1. **portal git snapshot** — 최근 commit 10건 + status + upstream과의 ahead/behind
2. **관련 프로젝트 최신 상태** — llive / llove / llmesh / lldesign / lltrade의 최신 commit + `tests/` 디렉터리의 최근 mtime
3. **operator action 재추출** — `NEXT_SESSION.md`의 🧑 섹션을 parsing 해서 `[ ]` 체크박스화
4. **`verify_publication` 최신 결과** — `out/verify_publication.last` 캐시의 tail 30행
5. **최근 4시간에 변경된 portal 파일**

raptor 쪽 래퍼는 `RAPTOR_CALLER_DIR=<your-path>/fullsense`일 때만 도는 분기. 다른 프로젝트로 전환해도 무해.

---

## 5. 채택 우선순위 HIGH인 lleval v0.1 요구사항 draft

채택 우선순위 HIGH로 확정한 lleval의 v0.1 요구사항 draft를 `docs/spec/requirements_lleval_v0.1_draft.md`에 썼다.

요점:

- **promptfoo를 fork base로**(Apache-2.0 / CI 친화 / on-prem provider 확장 여지 큼)
- 관측층은 **Phoenix(OpenInference / OTel)**
- RAG metric은 **Ragas / TruLens**를 adapter로 흡수
- 차별화 4축:
  1. on-prem + cloud 통일 A/B(`LLMeshProvider` plugin)
  2. Progressive size curve(xs/s/m/l/xl의 5단계 token sweep)
  3. Honest disclosure analyzer(이상 latency를 5인자로 자동 분해)
  4. Judge rotation + position swap(self-preference bias 자동 검출)

요구사항 `LE-01~08` + 비요구사항 + 착수 trigger 4단.

구현 착수는 user 판단. 이것은 agent 자율 draft이며, 벤치 복구(Anthropic / Gemini / OpenAI credential / quota 복구)와 병행으로 promptfoo fork PoC를 돌린다는 trigger 안을 명기하고 있다.

---

## 6. 이 세션의 정량 메트릭

| 지표 | 값 |
|---|---|
| 전 테스트 그린 건수 | **5409** (llive 1518 + llove 805 + llmesh 3086) |
| 한 세션 내 commit 수 | 약 14 (backup-hook auto: commits 포함) |
| 의도 commit (feat / docs / fix / test) | 7건 |
| 의도 push 수 | 6건 (portal × 4 + llove × 1 + llmesh × 1) |
| 신규 research 메모 | 6건 |
| 신규 memory (운용 규칙) | 5건 |
| TaskCreate / 전 complete | 16건 |
| AI agent dispatch (research) | 6건 (병렬, 전부 30분 이내 완료) |
| 환경 의존 test 수정 | 8건 (llove 7 + llmesh는 conftest 일괄) |

---

## 7. 교훈 (여기까지 배운 것)

1. **환경 의존 test에는 `monkeypatch.shutil.which`를 반드시 넣는다**. WinGet 등 패키지 매니저가 뒤에서 PATH를 바꿔 쓴다는 전제로 작성한다.
2. **Hypothesis flaky는 conftest 일괄 대처**. `register_profile`로 default를 덮어쓴다. 개별 `@settings`로 순차 대처하면 끝나지 않는다.
3. **채택 우선순위 판단에는 AI agent 병렬 조사**. 30분에 6건의 SOTA 보고서가 갖춰진다. 인간의 조사 시간에 비해 자릿수가 다르다.
4. **NEXT_SESSION은 2파일 운용**(사람 손의 방향성 + 자동 snapshot). drift와 정보 손실을 양립하지 않는다.
5. **lleval = promptfoo fork**가 확정 노선. 착수 trigger 대기.

---

## 8. 다음 하루로

- 환경이 더 바뀌지 않았는지, 아침에 test 전건 run
- `test_aoi_adapter_processes_synthetic`의 순서 의존 flaky 근본 조사
- raptor 리포 origin/main과의 diverge 해소(manual merge 필요)
- lleval PoC 착수 판단(벤치 복구와 병행)

---

## 관련

- [research/lleval_sota](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/lleval_sota.md)
- [research/llgrow_prior_art](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/llgrow_prior_art.md)
- [research/cognitive_mesh_vs_sota](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/research/cognitive_mesh_vs_sota.md)
- [spinoff_ideas_2026_05](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spinoff_ideas_2026_05.md)
- [requirements_lleval_v0.1_draft](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/spec/requirements_lleval_v0.1_draft)
- [NEXT_SESSION (사람 손)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.md)
- [NEXT_SESSION (자동)](https://github.com/furuse-kazufumi/fullsense/blob/main/docs/NEXT_SESSION.auto)
