---
title: '実 Brief 6 件で MATH grounding を観察したら、1 セッションで 6 周のバグ修正サイクルが回った'
tags:
  - FullSense
  - llive
  - MATH
  - デバッグ
  - 解説
private: false
id: 29b26774667b3af3a04e
---

言語 / Language / 语言 / 언어: [日本語](#日本語) | [English](#english) | [中文](#中文) | [한국어](#한국어)

---

# 日本語

# 実 Brief 6 件で MATH grounding を観察したら、1 セッションで 6 周のバグ修正サイクルが回った

**1 行 hook**:
`(1.38e-23 * 300)` をボルツマン定数 × 300 K として grounded 化したいだけだったのに、観察スクリプトが「23 * 300 = 6,900」と出してきた。指数表記の regex バグが 1 件目。そこから 6 周のサイクルで 1,270 → 1,314 PASS、UNKNOWN unit 0 件、TRIZ 偽陽性 0 件まで辿り着いた話。

---

## 背景 — なぜ「観察」を入れるのか

llive は「**LLM の周りに被せる認知 OS**」を志向するフレームワークで、Brief (構造化された依頼) を受け取って FullSenseLoop に流し込む前に、`BriefGrounder` という grounding 層を通します。grounding 層には 5 channel が乗っています:

| Channel | 担当 | 出典 |
|---|---|---|
| **TRIZ** | trade-off 系の trigger を検出 | TRIZ 40 原理 |
| **RAD** | 関連分野コーパスから引用 | Raptor RAD 49 分野 ~5 万件 |
| **calc (MATH-08)** | 算術式を deterministic に評価 | `SafeCalculator` |
| **units (MATH-01)** | 「数値+単位」を SI 次元に焼き付け | `parse_unit` |
| **constants (MATH-05)** | CODATA/NIST 定数を grounded 化 | `get_constant` |

これら 5 channel は単体テストで PASS していました。**それでも実 Brief を回したら、想定外の挙動が次々出てきた**のが本記事の主題です。

---

## ステップ 0 — 観察スクリプトの設計

`scripts/observe_grounding.py` という小さなスクリプトを書きました (~250 行)。役割は 3 つだけ:

1. 6 件の realistic Brief を `BriefRunner` 経由で実行
2. ledger の `grounding_applied` event payload から citation を抽出
3. Markdown サマリーで「**どの channel が何を surface したか**」を可視化

```python
SAMPLE_BRIEFS = [
    Brief("phys-drone", "Design a delivery drone that maintains 5 m/s during a 30 s window at 100 kg payload..."),
    Brief("energy-photon", "Compute the photon energy at 500 nm using the planck constant and the speed of light..."),
    Brief("trade-off", "Resolve the trade-off between high precision and speed..."),
    Brief("bookkeep", "Ship the report in 5 days, then revisit in 2 weeks. Each chapter should be under 30 pages..."),
    Brief("mixed", "Use the boltzmann constant to estimate kT at 300 K and compare with (1.38e-23 * 300)..."),
    Brief("prose-only", "Write the executive summary of the architecture rationale..."),
]
```

**assertion ではなく観察**を目的にしているので、テストは書かず Markdown を吐くだけにしました。`pytest` は通っているのに記事を書く根拠が無い場面で、「ベンチや観察」だけ別途記録する習慣を入れたかった、という設計判断です。

### ☕ ちなみに

`observe_grounding.py` は最初「単にレポートを出すだけ」と思って書きました。実際に動かして reports/observation.md を開いた瞬間、`23 * 300 = 6,900` という出力に「うわっ」となったのが 1 周目の始まり。**観察スクリプトは PASS している test では絶対見えないものを surface する**ことを身を持って確認した瞬間です。

---

## 1 周目 — `(1.38e-23 * 300)` が `(23 * 300)` と誤抽出

最初に出てきたのが Brief `mixed` の出力:

```
- (23 * 300) = 6,900 (ops=1)   ← 誤
```

期待は `(1.38e-23 * 300) = 4.14e-21`。ボルツマン定数 × 300 K = kT (300 K で約 4.14×10⁻²¹ J) という物理結果。

**原因**: `extract_expressions` の正規表現が `1.38` の小数までしか拾わず、`e-23` を切り捨てていた。

```python
# Before
_NUM = r"\d+(?:\.\d+)?"

# After
_NUM = r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
```

回帰テストを 3 件足して 1,288 → 1,291 PASS。最初の 1 周は **regex 1 行 + テスト 3 件で完了**。

---

## 2 周目 — `500 nm` `5 days` が UNKNOWN

次に来たのが Brief `energy-photon` と `bookkeep` の UNKNOWN 大量発生:

```
- 500 nm → UNKNOWN: unknown unit symbol 'nm'
- 5 days → UNKNOWN: unknown unit symbol 'days'
- 2 weeks → UNKNOWN: unknown unit symbol 'weeks'
- 30 pages → UNKNOWN: unknown unit symbol 'pages'
- 1 email → UNKNOWN: unknown unit symbol 'email'
```

このうち `nm` は SI 接頭辞 + 単位記号、`days` `weeks` は時間慣用語。**これらは parser 拡張で救うべき**。一方 `pages` `email` は単位ではなくドメイン語。後で処理する。

**対応**:
- `_SI_PREFIXES` frozenset (`Y/Z/E/P/T/G/M/k/h/da/d/c/m/μ/u/n/p/f/a/z/y`)
- `_term_dimensions` で prefix 試行 (2 文字優先で `da` を正しく解決)
- 時間慣用単位を `_DERIVED` に追加: `min`/`h`/`hour`/`day`/`days`/`week`/`weeks`/`year`/`years`

1,291 → 1,298 PASS。

### ☕ ここで一息

SI 接頭辞対応で気づいたのが「**m と m の衝突問題**」。`m` は meter (基本単位) でも milli (10⁻³ prefix) でもある。`mm` (millimetre) を解釈するとき、どちらでマッチさせるか? 解決は単純で「完全一致辞書を優先、接頭辞剥がしは fallback」。`m` 単独なら meter、`mm` なら meter が辞書にあるので prefix `m` + symbol `m`。これは「**辞書順序の優先度設計**」だけで衝突回避できた典型例でした。

---

## 3 周目 — `the speed of light` の `speed` が #35 を誤発火

Brief `energy-photon` で TRIZ citation を見ると、想定外の発火がありました:

```
- #24 Mediator (trigger: via)        ← OK ('Cross-check via the elementary charge')
- #35 Parameter Changes (trigger: speed)   ← 誤発火
```

`_TRIZ_TRIGGERS` 辞書で `"speed": 35` と登録していたため、`the speed of light` の `speed` がそのまま match。

**対応**: 2 段階の精度向上策を入れました。

1. **Word boundary**: 短い English trigger は `\b{trigger}\b` で囲む

   ```python
   _WORD_BOUNDARY_TRIGGERS = frozenset({"vs", "via", "speed", "quality", ...})
   ```

   これで `speedy delivery` の `speedy` から `speed` が誤発火しなくなる。

2. **否定文脈**: 特定フレーズが Brief に存在する場合は trigger を抑制

   ```python
   _TRIZ_NEGATIVE_CONTEXTS = {
       "speed": ("speed of light", "lightspeed"),
       "via": ("via point", "via the api"),
   }
   ```

これで `speed of light` を含む Brief では `#35` が発火しなくなる。1,298 → 1,301 PASS。

---

## 4 周目 — MATH-07 (`MATHEMATICAL` EpistemicType) 未着手

ここまで「Brief grounding 層の精度問題」を直してきましたが、観察スクリプトの集約欄を見て気づいたのが **「FACTUAL track はあるのに MATHEMATICAL track が無い」** 点。

llive は `EpistemicType` (FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC + 予備 5) で track を分けています。FACTUAL は「結論不変、confidence < 0.7 で SILENT 降格」する strict mode。**数学命題はもっと厳格にできるはず**。

**対応**:
- `EpistemicType.MATHEMATICAL = "mathematical"` 追加
- `mathematical_track`: confidence < 0.8 で SILENT 降格 (FACTUAL の 0.7 より厳格)
- rationale に `MathVerifier 検算可能性を確認` の hint を添付

```python
def mathematical_track(stim, plan):
    if plan.thought is not None and plan.thought.confidence < 0.8:
        plan = ActionPlan(
            decision=ActionDecision.SILENT,
            rationale="MATHEMATICAL strict: confidence < 0.8, withholding until MathVerifier 検算可能性を確認",
            ...
        )
    return _tag(plan, "mathematical")
```

1,301 → 1,305 PASS。

### ☕ ちょっと脱線

「数学命題は他のドメインより厳格にしていい」というのは、岡潔先生 (※) が遺された「数学は情緒である」という思想とは方向が違うように見えますが、こちらは「**LLM がうっかり数式を間違えないための gate**」のためのもの。先生の思想に学ぶ層 (`OKA-FX`) は別レイヤで設計しています。**Defensive (MATH 系) と offensive (OKA 系) を分離する**のが設計判断。

(※ 岡潔先生の思想を実装したと主張するものではありません。先生が遺された豊かな思索のうち、エンジニアリング言語として参照させていただける観点に着目し、設計の触発源として活かしている、というスタンスです。)

---

## 5 周目 — `pages` `email` のドメイン語ノイズ

2 周目で「ドメイン語は後で」と言って先送りした件です。実 Brief `bookkeep` で `30 pages`, `1 email`, `1 milestone` のような表現が citation に大量に残っていました。

これらは parser が「unknown unit」として error citation に残しますが、**error citation の本来の目的は「拡張すべき単位を発見すること」**なので、ドメイン語が大量に混ざると信号価値が下がります。

**対応**: `_NON_UNIT_WORDS` frozenset でフィルタ (28 語)

```python
_NON_UNIT_WORDS = frozenset({
    "email", "users", "page", "pages", "item", "items",
    "request", "point", "slide", "chapter", "widget",
    "ticket", "comment", "issue", "row", "column",
    "people", "customer", "step", "task", "milestone", ...
})
```

`_lookup_units` で unit_text がここに含まれていたら **silently skip** (citation 化しない)。これにより error citation には「parser が知らない真の単位」(`furlong` 等) だけが残るようになりました。1,305 → 1,306 PASS。

### ☕ ちなみに

このとき既存テスト 1 件が壊れました (`test_grounder_surfaces_unknown_units_as_errors`)。元々「`5 days` `2 pages` が error citation に残る」を期待していましたが、本セッションの修正で `5 days` は正規 unit に、`2 pages` はドメイン語フィルタで skip に。**仕様変更で既存テストが壊れたら、新仕様に合わせて書き直す**のが正解。テストを「Brief 中の `3 furlong`」に変更して回帰維持しました。

---

## 6 周目 — `5 days` を `5 秒` と混同させないために (MATH-06 minimal)

ここまでで `5 days` は time 次元として認識できるようになりましたが、**値はまだ 5 のまま**。LLM が後段で「days を seconds に変換」する責任を負う設計だと、変換忘れによる致命的なバグ (5 秒の実験になってしまう) が起きる。

**対応**: `Quantity` API は触らず、citation 層に `si_factor` / `si_value` を追加。

```python
@dataclass(frozen=True)
class UnitCitation:
    raw_text: str
    value: float          # 元の数値 (5)
    unit_text: str        # "days"
    dimensions: str       # "s"
    si_factor: float = 1.0   # 86400
    si_value: float = 0.0    # 432000
    error: str | None = None
```

grounded prompt 出力:
```
- 5 days → value=5.0, dimensions=s, SI=432000.0 (×86400.0)
- 500 nm → value=500.0, dimensions=m, SI=5.0e-7 (×1e-9)
```

これで LLM は「**実は SI base で 432,000 秒**」と即座に知ることができ、変換ミスのリスクが減ります。

1,306 → 1,314 PASS。

---

## まとめ — 観察スクリプトが効いた理由

| 周 | 発見 | 修正 | PASS |
|---|---|---|---|
| 1 | 指数表記 regex バグ | `_NUM` atom 拡張 | 1,291 |
| 2 | SI prefix + 時間慣用語 未対応 | parser 拡張 | 1,298 |
| 3 | TRIZ trigger 偽陽性 | word-boundary + 否定文脈 | 1,301 |
| 4 | MATH-07 未着手 | `MATHEMATICAL` track | 1,305 |
| 5 | ドメイン語ノイズ | 28 語フィルタ | 1,306 |
| 6 | scale 未表示 | minimal `si_factor`/`si_value` | **1,314** |

合計 44 PASS 増、回帰ゼロ、UNKNOWN unit ゼロ、TRIZ 偽陽性ゼロ。

**得られた教訓**:

1. **観察スクリプトは PASS テストでは見えない場所を surface する** — 単体テストは「想定通りの入力で想定通りの出力」を保証するが、実 Brief は単体テスト作者が思いつかない組合せを入れてくる
2. **error citation を silently drop しない設計が機能した** — 「unknown unit を残す」設計を入れたので、観察から「拡張すべき辞書」が自動収集できた
3. **小さい修正を 6 周回す方が、一気に大幅改修するより成果が出る** — 各周は regex 1 行 / 辞書 28 語 / 否定文脈 dict 等、20 行以下。これを 6 周することで生地が成熟した
4. **Quantity API の破壊変更は避けて citation 層で完結** (MATH-06 minimal) — 後段で本格 scale-aware Quantity 算術が必要になる時に、過去の判断に縛られない自由度を残せた

---

## 残課題と運用

| 候補 | スコープ | 着手判断 |
|---|---|---|
| MATH-03 LaTeX/MathML 構文解析 | 中 | 実 Brief で LaTeX 数式が surface してから |
| MATH-04 IEEE 754 精度トラッキング | 大 | 同上 |
| Cross-quantity 次元演算チェック (`5 m/s + 3 s`) | 中 | 観察で具体 mismatch が出てから |
| Quantity scale-aware 算術 (MATH-06 後段) | 破壊変更含む | 必要性確認後 |

すべて「実 Brief 観察ベースで必要性 surface 後」という保留方針。**今すぐ着手する根拠が無い**のは、観察スクリプトの結果が「unit/calc/constants/TRIZ の minimal grounding が現状 6 Brief で十分機能する」と教えてくれているから。

llive のリポジトリ:
- <https://github.com/furuse-kazufumi/llive>
- 本記事の数値根拠: `docs/benchmarks/2026-05-17-grounding-observation/observation.md`
- 観察スクリプト: `scripts/observe_grounding.py`

「実装 → 観察 → 課題発見 → 即修正」のサイクルに興味がある方は、Issue / Discussion でぜひ。

---

## 参考文献 / 参考リソース

### CODATA / NIST (MATH-05 関連)
- CODATA 2022 Recommended Values — <https://physics.nist.gov/cuu/Constants/>
- NIST SP 330: The International System of Units (SI)

### TRIZ (第 3 周修正の関連)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996

### llive 関連
- llive リポジトリ — <https://github.com/furuse-kazufumi/llive>
- 「第二の脳」シリーズ全 4 部 (構築論/運用論/ビジョン論+不可視 Annotation)

<!-- llive:meta.article_id="QIITA_OBSERVATION_GROUNDING_jp" target=llove -->
<!-- llive:meta.published_date="2026-05-18" -->
<!-- llive:meta.tags=["llive","grounding","observation","math","triz","testing","honest-disclosure"] target=any -->
<!-- llive:meta.series="implementation_observations" -->

---

# English

# Observing MATH grounding on 6 real Briefs spun up 6 rounds of bug-fixing in a single session

**One-line hook**:
All I wanted was to ground `(1.38e-23 * 300)` as the Boltzmann constant × 300 K, but the observation script spat out "23 * 300 = 6,900." A scientific-notation regex bug was round one. From there, six rounds of the cycle took us from 1,270 → 1,314 PASS, with zero UNKNOWN units and zero TRIZ false positives. This is that story.

---

## Background — why add "observation"

llive is a framework aiming to be "**a cognitive OS you wrap around an LLM**." Before a Brief (a structured request) is fed into the FullSenseLoop, it passes through a grounding layer called `BriefGrounder`. The grounding layer carries 5 channels:

| Channel | Responsibility | Source |
|---|---|---|
| **TRIZ** | Detects trade-off triggers | TRIZ 40 principles |
| **RAD** | Cites from related-field corpora | Raptor RAD, 49 fields, ~50k items |
| **calc (MATH-08)** | Evaluates arithmetic expressions deterministically | `SafeCalculator` |
| **units (MATH-01)** | Bakes "number + unit" into SI dimensions | `parse_unit` |
| **constants (MATH-05)** | Grounds CODATA/NIST constants | `get_constant` |

These 5 channels were all passing in unit tests. **And yet, the moment we ran real Briefs, unexpected behaviors kept popping up** — that is the subject of this article.

---

## Step 0 — designing the observation script

I wrote a small script called `scripts/observe_grounding.py` (~250 lines). It has just 3 jobs:

1. Run 6 realistic Briefs through `BriefRunner`
2. Extract citations from the `grounding_applied` event payload in the ledger
3. Visualize "**which channel surfaced what**" in a Markdown summary

```python
SAMPLE_BRIEFS = [
    Brief("phys-drone", "Design a delivery drone that maintains 5 m/s during a 30 s window at 100 kg payload..."),
    Brief("energy-photon", "Compute the photon energy at 500 nm using the planck constant and the speed of light..."),
    Brief("trade-off", "Resolve the trade-off between high precision and speed..."),
    Brief("bookkeep", "Ship the report in 5 days, then revisit in 2 weeks. Each chapter should be under 30 pages..."),
    Brief("mixed", "Use the boltzmann constant to estimate kT at 300 K and compare with (1.38e-23 * 300)..."),
    Brief("prose-only", "Write the executive summary of the architecture rationale..."),
]
```

Because the goal is **observation, not assertion**, I wrote no tests — the script just emits Markdown. The design call was: I wanted to build the habit of separately recording "benchmarks and observations" for those cases where `pytest` passes but there is no basis to write an article.

### ☕ By the way

I first wrote `observe_grounding.py` thinking it would "just print a report." The instant I actually ran it and opened reports/observation.md, the output `23 * 300 = 6,900` made me go "ugh" — and that was the start of round one. It was the moment I learned firsthand that **an observation script surfaces things passing tests can never reveal**.

---

## Round 1 — `(1.38e-23 * 300)` mis-extracted as `(23 * 300)`

The first thing to surface was the output for Brief `mixed`:

```
- (23 * 300) = 6,900 (ops=1)   ← wrong
```

The expectation was `(1.38e-23 * 300) = 4.14e-21`: the physical result of the Boltzmann constant × 300 K = kT (about 4.14×10⁻²¹ J at 300 K).

**Cause**: the regex in `extract_expressions` only picked up the `1.38` decimal and discarded the `e-23`.

```python
# Before
_NUM = r"\d+(?:\.\d+)?"

# After
_NUM = r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
```

Added 3 regression tests, taking 1,288 → 1,291 PASS. The first round was **done with 1 line of regex + 3 tests**.

---

## Round 2 — `500 nm` and `5 days` come back UNKNOWN

Next up was a flood of UNKNOWNs from Briefs `energy-photon` and `bookkeep`:

```
- 500 nm → UNKNOWN: unknown unit symbol 'nm'
- 5 days → UNKNOWN: unknown unit symbol 'days'
- 2 weeks → UNKNOWN: unknown unit symbol 'weeks'
- 30 pages → UNKNOWN: unknown unit symbol 'pages'
- 1 email → UNKNOWN: unknown unit symbol 'email'
```

Of these, `nm` is an SI prefix + unit symbol, and `days`/`weeks` are colloquial time terms. **These should be rescued by extending the parser.** On the other hand, `pages` and `email` are not units but domain words. I'll handle those later.

**Fix**:
- `_SI_PREFIXES` frozenset (`Y/Z/E/P/T/G/M/k/h/da/d/c/m/μ/u/n/p/f/a/z/y`)
- Try prefixes in `_term_dimensions` (prefer 2-character matches so `da` resolves correctly)
- Add colloquial time units to `_DERIVED`: `min`/`h`/`hour`/`day`/`days`/`week`/`weeks`/`year`/`years`

1,291 → 1,298 PASS.

### ☕ A breather here

While handling SI prefixes, I ran into the "**m versus m collision problem**." `m` is both meter (a base unit) and milli (the 10⁻³ prefix). When interpreting `mm` (millimetre), which one do you match? The solution was simple: "prefer the exact-match dictionary, fall back to prefix stripping." `m` alone is meter; `mm` is meter (in the dictionary) so it's prefix `m` + symbol `m`. This was a textbook case where the collision was avoided **purely by designing the priority order of the dictionary**.

---

## Round 3 — `speed` in `the speed of light` falsely fires #35

Looking at the TRIZ citations for Brief `energy-photon`, there was an unexpected firing:

```
- #24 Mediator (trigger: via)        ← OK ('Cross-check via the elementary charge')
- #35 Parameter Changes (trigger: speed)   ← false fire
```

Because the `_TRIZ_TRIGGERS` dictionary registered `"speed": 35`, the `speed` in `the speed of light` matched directly.

**Fix**: I introduced a two-stage precision improvement.

1. **Word boundary**: wrap short English triggers in `\b{trigger}\b`

   ```python
   _WORD_BOUNDARY_TRIGGERS = frozenset({"vs", "via", "speed", "quality", ...})
   ```

   This stops `speed` from falsely firing on the `speedy` in `speedy delivery`.

2. **Negative context**: suppress the trigger when a specific phrase is present in the Brief

   ```python
   _TRIZ_NEGATIVE_CONTEXTS = {
       "speed": ("speed of light", "lightspeed"),
       "via": ("via point", "via the api"),
   }
   ```

   Now `#35` no longer fires for Briefs containing `speed of light`. 1,298 → 1,301 PASS.

---

## Round 4 — MATH-07 (the `MATHEMATICAL` EpistemicType) not yet started

So far I had been fixing "precision problems in the Brief grounding layer," but looking at the aggregation column of the observation script I noticed: **"there is a FACTUAL track but no MATHEMATICAL track."**

llive separates tracks by `EpistemicType` (FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC + 5 reserved). FACTUAL is a strict mode that "keeps the conclusion fixed and demotes to SILENT when confidence < 0.7." **Mathematical propositions should be able to be stricter still.**

**Fix**:
- Add `EpistemicType.MATHEMATICAL = "mathematical"`
- `mathematical_track`: demote to SILENT when confidence < 0.8 (stricter than FACTUAL's 0.7)
- Attach a hint to the rationale: `Confirm MathVerifier recomputability`

```python
def mathematical_track(stim, plan):
    if plan.thought is not None and plan.thought.confidence < 0.8:
        plan = ActionPlan(
            decision=ActionDecision.SILENT,
            rationale="MATHEMATICAL strict: confidence < 0.8, withholding until MathVerifier 検算可能性を確認",
            ...
        )
    return _tag(plan, "mathematical")
```

1,301 → 1,305 PASS.

### ☕ A small digression

The idea that "mathematical propositions may be stricter than other domains" looks like it points the opposite way from the philosophy Kiyoshi Oka (※) left us — "mathematics is emotion (jōcho)" — but this is a **gate to keep the LLM from carelessly getting a formula wrong**. The layer that learns from Oka's thought (`OKA-FX`) is designed separately. **Separating defensive (the MATH family) from offensive (the OKA family)** was the design call.

(※ This is not a claim to have implemented Kiyoshi Oka's thought. The stance is that, among the rich reflections he left behind, we focus on the viewpoints we may reference as an engineering language and draw on them as a source of design inspiration.)

---

## Round 5 — domain-word noise from `pages` and `email`

This is the matter I deferred in round 2 with "domain words later." In real Brief `bookkeep`, expressions like `30 pages`, `1 email`, and `1 milestone` were left in large numbers among the citations.

The parser leaves these as "unknown unit" error citations, but **the real purpose of an error citation is "to discover units that should be extended,"** so when domain words flood in, the signal value drops.

**Fix**: filter via the `_NON_UNIT_WORDS` frozenset (28 words)

```python
_NON_UNIT_WORDS = frozenset({
    "email", "users", "page", "pages", "item", "items",
    "request", "point", "slide", "chapter", "widget",
    "ticket", "comment", "issue", "row", "column",
    "people", "customer", "step", "task", "milestone", ...
})
```

In `_lookup_units`, if unit_text is contained here, **silently skip** (do not turn it into a citation). As a result, error citations now retain only "true units the parser doesn't know" (e.g. `furlong`). 1,305 → 1,306 PASS.

### ☕ By the way

At this point one existing test broke (`test_grounder_surfaces_unknown_units_as_errors`). It originally expected that "`5 days` and `2 pages` remain as error citations," but with this session's fixes `5 days` became a proper unit and `2 pages` got skipped by the domain-word filter. **When a spec change breaks an existing test, the right answer is to rewrite it to match the new spec.** I changed the test to use "`3 furlong` in the Brief" to maintain the regression.

---

## Round 6 — so as not to confuse `5 days` with `5 seconds` (MATH-06 minimal)

By this point `5 days` could be recognized as a time dimension, but **the value was still just 5**. With a design where the LLM is responsible for "converting days to seconds" downstream, a fatal bug from a forgotten conversion (it becomes a 5-second experiment) can happen.

**Fix**: don't touch the `Quantity` API; add `si_factor` / `si_value` to the citation layer.

```python
@dataclass(frozen=True)
class UnitCitation:
    raw_text: str
    value: float          # original number (5)
    unit_text: str        # "days"
    dimensions: str       # "s"
    si_factor: float = 1.0   # 86400
    si_value: float = 0.0    # 432000
    error: str | None = None
```

Grounded prompt output:
```
- 5 days → value=5.0, dimensions=s, SI=432000.0 (×86400.0)
- 500 nm → value=500.0, dimensions=m, SI=5.0e-7 (×1e-9)
```

Now the LLM can instantly know "**this is actually 432,000 seconds in SI base**," reducing the risk of conversion mistakes.

1,306 → 1,314 PASS.

---

## Summary — why the observation script worked

| Round | Discovery | Fix | PASS |
|---|---|---|---|
| 1 | Scientific-notation regex bug | Extend the `_NUM` atom | 1,291 |
| 2 | SI prefix + colloquial time unsupported | Extend the parser | 1,298 |
| 3 | TRIZ trigger false positive | Word boundary + negative context | 1,301 |
| 4 | MATH-07 not started | `MATHEMATICAL` track | 1,305 |
| 5 | Domain-word noise | 28-word filter | 1,306 |
| 6 | Scale not displayed | Minimal `si_factor`/`si_value` | **1,314** |

A total of +44 PASS, zero regressions, zero UNKNOWN units, zero TRIZ false positives.

**Lessons learned**:

1. **An observation script surfaces places passing tests cannot see** — unit tests guarantee "expected output for expected input," but real Briefs throw in combinations the unit-test author never imagined
2. **The design of not silently dropping error citations paid off** — because we built in a design that "keeps unknown units," observation could automatically gather "dictionaries that should be extended"
3. **Spinning small fixes 6 times produces more than one sweeping overhaul** — each round was under 20 lines (1 line of regex / a 28-word dictionary / a negative-context dict, etc.); doing this 6 times let the dough mature
4. **Avoid breaking changes to the Quantity API and keep it within the citation layer** (MATH-06 minimal) — this preserves the freedom to not be bound by past decisions when full scale-aware Quantity arithmetic becomes necessary downstream

---

## Remaining work and operations

| Candidate | Scope | Decision to start |
|---|---|---|
| MATH-03 LaTeX/MathML syntax parsing | Medium | After LaTeX formulas surface in real Briefs |
| MATH-04 IEEE 754 precision tracking | Large | Same as above |
| Cross-quantity dimensional checks (`5 m/s + 3 s`) | Medium | After a concrete mismatch surfaces in observation |
| Quantity scale-aware arithmetic (MATH-06 downstream) | Includes breaking changes | After need is confirmed |

The hold-off policy for all of these is "after the need surfaces from real-Brief observation." **The reason there is no basis to start right now** is that the observation script's results tell us "the minimal grounding of unit/calc/constants/TRIZ functions sufficiently for the current 6 Briefs."

llive repository:
- <https://github.com/furuse-kazufumi/llive>
- Numeric basis for this article: `docs/benchmarks/2026-05-17-grounding-observation/observation.md`
- Observation script: `scripts/observe_grounding.py`

If you're interested in the "implement → observe → discover issues → fix immediately" cycle, please come by an Issue / Discussion.

---

## References / resources

### CODATA / NIST (related to MATH-05)
- CODATA 2022 Recommended Values — <https://physics.nist.gov/cuu/Constants/>
- NIST SP 330: The International System of Units (SI)

### TRIZ (related to the round-3 fix)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996

### llive related
- llive repository — <https://github.com/furuse-kazufumi/llive>
- "The Second Brain" series, all 4 parts (construction / operation / vision + invisible Annotation)

---

# 中文

# 用 6 个真实 Brief 观察 MATH grounding 后，在一次会话里转了 6 轮修 bug 循环

**一句话钩子**：
我本来只想把 `(1.38e-23 * 300)` 作为玻尔兹曼常数 × 300 K 做 grounding，可观察脚本却给出了「23 * 300 = 6,900」。科学计数法的 regex bug 是第 1 轮。从那里开始，6 轮循环让我们从 1,270 → 1,314 PASS，UNKNOWN 单位 0 件、TRIZ 假阳性 0 件。这就是那段经历。

---

## 背景 —— 为什么要加入「观察」

llive 是一个志在成为「**套在 LLM 周围的认知 OS**」的框架，在把 Brief（结构化的请求）送入 FullSenseLoop 之前，会先通过一个叫 `BriefGrounder` 的 grounding 层。grounding 层上搭载了 5 个 channel：

| Channel | 职责 | 来源 |
|---|---|---|
| **TRIZ** | 检测 trade-off 类的 trigger | TRIZ 40 原理 |
| **RAD** | 从相关领域语料库中引用 | Raptor RAD 49 领域 约 5 万件 |
| **calc (MATH-08)** | 确定性地求值算术表达式 | `SafeCalculator` |
| **units (MATH-01)** | 把「数值+单位」烧录为 SI 量纲 | `parse_unit` |
| **constants (MATH-05)** | 把 CODATA/NIST 常数 grounding 化 | `get_constant` |

这 5 个 channel 在单元测试里都 PASS 了。**然而一旦跑起真实 Brief，意料之外的行为接连冒了出来**——这正是本文的主题。

---

## 步骤 0 —— 观察脚本的设计

我写了一个叫 `scripts/observe_grounding.py` 的小脚本（约 250 行）。它只承担 3 件事：

1. 通过 `BriefRunner` 运行 6 个 realistic Brief
2. 从 ledger 的 `grounding_applied` event payload 中提取 citation
3. 用 Markdown 摘要可视化「**哪个 channel surface 了什么**」

```python
SAMPLE_BRIEFS = [
    Brief("phys-drone", "Design a delivery drone that maintains 5 m/s during a 30 s window at 100 kg payload..."),
    Brief("energy-photon", "Compute the photon energy at 500 nm using the planck constant and the speed of light..."),
    Brief("trade-off", "Resolve the trade-off between high precision and speed..."),
    Brief("bookkeep", "Ship the report in 5 days, then revisit in 2 weeks. Each chapter should be under 30 pages..."),
    Brief("mixed", "Use the boltzmann constant to estimate kT at 300 K and compare with (1.38e-23 * 300)..."),
    Brief("prose-only", "Write the executive summary of the architecture rationale..."),
]
```

由于目标是**观察而非断言**，所以没有写测试，脚本只输出 Markdown。设计上的判断是：在 `pytest` 通过却没有依据去写文章的场合，我想养成单独记录「基准测试或观察」的习惯。

### ☕ 顺带一提

我最初写 `observe_grounding.py` 时以为它「只是输出一份报告」。当我真正运行它并打开 reports/observation.md 的那一瞬间，看到 `23 * 300 = 6,900` 这个输出「哎呀」了一声，这就是第 1 轮的开始。这正是我亲身确认「**观察脚本会 surface 出 PASS 测试里绝对看不到的东西**」的时刻。

---

## 第 1 轮 —— `(1.38e-23 * 300)` 被误抽取成 `(23 * 300)`

最先冒出来的是 Brief `mixed` 的输出：

```
- (23 * 300) = 6,900 (ops=1)   ← 错
```

期望是 `(1.38e-23 * 300) = 4.14e-21`：玻尔兹曼常数 × 300 K = kT（300 K 时约 4.14×10⁻²¹ J）这个物理结果。

**原因**：`extract_expressions` 的正则只取到 `1.38` 的小数为止，把 `e-23` 截掉了。

```python
# Before
_NUM = r"\d+(?:\.\d+)?"

# After
_NUM = r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
```

补了 3 个回归测试，从 1,288 → 1,291 PASS。第一轮**用 1 行 regex + 3 个测试就完成了**。

---

## 第 2 轮 —— `500 nm` `5 days` 变成 UNKNOWN

接下来是 Brief `energy-photon` 和 `bookkeep` 大量出现的 UNKNOWN：

```
- 500 nm → UNKNOWN: unknown unit symbol 'nm'
- 5 days → UNKNOWN: unknown unit symbol 'days'
- 2 weeks → UNKNOWN: unknown unit symbol 'weeks'
- 30 pages → UNKNOWN: unknown unit symbol 'pages'
- 1 email → UNKNOWN: unknown unit symbol 'email'
```

其中 `nm` 是 SI 前缀 + 单位符号，`days` `weeks` 是时间的习惯用语。**这些应该用 parser 扩展来挽救**。另一方面 `pages` `email` 不是单位而是领域词。稍后处理。

**对应**：
- `_SI_PREFIXES` frozenset（`Y/Z/E/P/T/G/M/k/h/da/d/c/m/μ/u/n/p/f/a/z/y`）
- 在 `_term_dimensions` 中尝试前缀（优先 2 字符以正确解析 `da`）
- 把时间习惯单位加入 `_DERIVED`：`min`/`h`/`hour`/`day`/`days`/`week`/`weeks`/`year`/`years`

1,291 → 1,298 PASS。

### ☕ 在这里歇口气

在做 SI 前缀对应时注意到的是「**m 与 m 的冲突问题**」。`m` 既是 meter（基本单位）也是 milli（10⁻³ 前缀）。解释 `mm`（millimetre）时，要用哪一个去匹配？解决很简单：「优先精确匹配字典，剥离前缀作为 fallback」。`m` 单独是 meter；`mm` 因为字典里有 meter，所以是前缀 `m` + 符号 `m`。这是一个仅凭「**字典顺序的优先级设计**」就规避冲突的典型例子。

---

## 第 3 轮 —— `the speed of light` 中的 `speed` 误触发 #35

在看 Brief `energy-photon` 的 TRIZ citation 时，出现了意料之外的触发：

```
- #24 Mediator (trigger: via)        ← OK ('Cross-check via the elementary charge')
- #35 Parameter Changes (trigger: speed)   ← 误触发
```

因为在 `_TRIZ_TRIGGERS` 字典里登记了 `"speed": 35`，`the speed of light` 中的 `speed` 就这样直接 match 了。

**对应**：引入了两阶段的精度提升策略。

1. **Word boundary**：把短的英文 trigger 用 `\b{trigger}\b` 包起来

   ```python
   _WORD_BOUNDARY_TRIGGERS = frozenset({"vs", "via", "speed", "quality", ...})
   ```

   这样 `speedy delivery` 里的 `speedy` 就不会再误触发出 `speed`。

2. **否定语境**：当 Brief 中存在特定短语时抑制 trigger

   ```python
   _TRIZ_NEGATIVE_CONTEXTS = {
       "speed": ("speed of light", "lightspeed"),
       "via": ("via point", "via the api"),
   }
   ```

   这样在包含 `speed of light` 的 Brief 中 `#35` 就不再触发了。1,298 → 1,301 PASS。

---

## 第 4 轮 —— MATH-07（`MATHEMATICAL` EpistemicType）尚未着手

到这里为止一直在修「Brief grounding 层的精度问题」，但看着观察脚本的汇总栏注意到一点：**「有 FACTUAL track 却没有 MATHEMATICAL track」**。

llive 用 `EpistemicType`（FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC + 预备 5 个）来分 track。FACTUAL 是「结论不变，confidence < 0.7 时降级为 SILENT」的 strict mode。**数学命题应该能更严格才对**。

**对应**：
- 添加 `EpistemicType.MATHEMATICAL = "mathematical"`
- `mathematical_track`：confidence < 0.8 时降级为 SILENT（比 FACTUAL 的 0.7 更严格）
- 在 rationale 上附加 hint：`确认 MathVerifier 验算可能性`

```python
def mathematical_track(stim, plan):
    if plan.thought is not None and plan.thought.confidence < 0.8:
        plan = ActionPlan(
            decision=ActionDecision.SILENT,
            rationale="MATHEMATICAL strict: confidence < 0.8, withholding until MathVerifier 検算可能性を確認",
            ...
        )
    return _tag(plan, "mathematical")
```

1,301 → 1,305 PASS。

### ☕ 稍微岔开一下

「数学命题可以比其他领域更严格」这一点，看起来与冈洁先生（※）留下的「数学是情绪（情绪）」这一思想方向不同，但这边是为了「**让 LLM 不会一不小心把数式弄错的 gate**」。向先生思想学习的层（`OKA-FX`）在另一层另行设计。**把 Defensive（MATH 系）与 offensive（OKA 系）分离**，是设计上的判断。

（※ 并非主张已实现冈洁先生的思想。立场是：在先生留下的丰富思索之中，着眼于可作为工程语言来参照的观点，并将其作为设计的触发源加以运用。）

---

## 第 5 轮 —— `pages` `email` 的领域词噪声

这是第 2 轮时说「领域词稍后处理」而推迟下来的事。在真实 Brief `bookkeep` 中，像 `30 pages`、`1 email`、`1 milestone` 这样的表达在 citation 中大量残留。

这些被 parser 当作「unknown unit」留在 error citation 里，但**error citation 本来的目的是「发现应该扩展的单位」**，所以当领域词大量混入时，信号价值就下降了。

**对应**：用 `_NON_UNIT_WORDS` frozenset 过滤（28 个词）

```python
_NON_UNIT_WORDS = frozenset({
    "email", "users", "page", "pages", "item", "items",
    "request", "point", "slide", "chapter", "widget",
    "ticket", "comment", "issue", "row", "column",
    "people", "customer", "step", "task", "milestone", ...
})
```

在 `_lookup_units` 中，如果 unit_text 包含在这里就**silently skip**（不做成 citation）。由此 error citation 里就只留下「parser 不认识的真正单位」（如 `furlong`）了。1,305 → 1,306 PASS。

### ☕ 顺带一提

这时有一个既有测试坏了（`test_grounder_surfaces_unknown_units_as_errors`）。它原本期望「`5 days` `2 pages` 残留在 error citation 中」，但经本次会话的修改，`5 days` 成了正规 unit，`2 pages` 被领域词过滤 skip 掉了。**当规格变更导致既有测试坏掉时，按新规格重写才是正解**。我把测试改成「Brief 中的 `3 furlong`」以维持回归。

---

## 第 6 轮 —— 为了不把 `5 days` 与 `5 秒` 混淆（MATH-06 minimal）

到此为止 `5 days` 已经能被识别为 time 量纲了，但**值还停在 5**。如果采用「由 LLM 在后段负责把 days 转换成 seconds」的设计，那么因忘记转换而引发的致命 bug（变成了 5 秒的实验）就会发生。

**对应**：不碰 `Quantity` API，在 citation 层添加 `si_factor` / `si_value`。

```python
@dataclass(frozen=True)
class UnitCitation:
    raw_text: str
    value: float          # 原始数值 (5)
    unit_text: str        # "days"
    dimensions: str       # "s"
    si_factor: float = 1.0   # 86400
    si_value: float = 0.0    # 432000
    error: str | None = None
```

grounded prompt 输出：
```
- 5 days → value=5.0, dimensions=s, SI=432000.0 (×86400.0)
- 500 nm → value=500.0, dimensions=m, SI=5.0e-7 (×1e-9)
```

这样 LLM 就能立刻知道「**其实是 SI base 下的 432,000 秒**」，降低转换出错的风险。

1,306 → 1,314 PASS。

---

## 总结 —— 观察脚本为什么有效

| 轮 | 发现 | 修正 | PASS |
|---|---|---|---|
| 1 | 科学计数法 regex bug | 扩展 `_NUM` atom | 1,291 |
| 2 | SI prefix + 时间习惯语 未支持 | 扩展 parser | 1,298 |
| 3 | TRIZ trigger 假阳性 | word-boundary + 否定语境 | 1,301 |
| 4 | MATH-07 未着手 | `MATHEMATICAL` track | 1,305 |
| 5 | 领域词噪声 | 28 词过滤 | 1,306 |
| 6 | scale 未显示 | minimal `si_factor`/`si_value` | **1,314** |

合计 +44 PASS、回归为零、UNKNOWN 单位为零、TRIZ 假阳性为零。

**得到的教训**：

1. **观察脚本会 surface 出 PASS 测试看不到的地方** —— 单元测试保证「在预想的输入下给出预想的输出」，但真实 Brief 会塞进单元测试作者想不到的组合
2. **不 silently drop error citation 的设计起了作用** —— 因为加入了「保留 unknown unit」的设计，所以可以从观察中自动收集「应该扩展的字典」
3. **把小修正转 6 轮，比一口气大改更出成果** —— 每一轮都在 20 行以下（1 行 regex / 28 词字典 / 否定语境 dict 等），转 6 轮让面团成熟了起来
4. **避免对 Quantity API 的破坏性变更，在 citation 层内完结**（MATH-06 minimal）—— 这样在后段需要正式的 scale-aware Quantity 算术时，就能保留不被过去判断束缚的自由度

---

## 遗留课题与运营

| 候选 | 范围 | 着手判断 |
|---|---|---|
| MATH-03 LaTeX/MathML 语法解析 | 中 | 在真实 Brief 中 surface 出 LaTeX 数式之后 |
| MATH-04 IEEE 754 精度跟踪 | 大 | 同上 |
| Cross-quantity 量纲运算检查（`5 m/s + 3 s`） | 中 | 在观察中出现具体 mismatch 之后 |
| Quantity scale-aware 算术（MATH-06 后段） | 含破坏性变更 | 确认必要性之后 |

所有这些都采取「在真实 Brief 观察的基础上 surface 出必要性之后」的保留方针。**之所以没有立刻着手的依据**，是因为观察脚本的结果告诉我们「unit/calc/constants/TRIZ 的 minimal grounding 在当前 6 个 Brief 下已充分发挥作用」。

llive 的仓库：
- <https://github.com/furuse-kazufumi/llive>
- 本文的数值依据：`docs/benchmarks/2026-05-17-grounding-observation/observation.md`
- 观察脚本：`scripts/observe_grounding.py`

对「实现 → 观察 → 发现课题 → 立即修正」这一循环感兴趣的朋友，欢迎来 Issue / Discussion。

---

## 参考文献 / 参考资源

### CODATA / NIST（MATH-05 相关）
- CODATA 2022 Recommended Values — <https://physics.nist.gov/cuu/Constants/>
- NIST SP 330: The International System of Units (SI)

### TRIZ（与第 3 轮修正相关）
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996

### llive 相关
- llive 仓库 — <https://github.com/furuse-kazufumi/llive>
- 「第二大脑」系列全 4 部（构建论/运营论/愿景论+不可见 Annotation）

---

# 한국어

# 실제 Brief 6건으로 MATH grounding을 관찰했더니, 한 세션에서 6바퀴의 버그 수정 사이클이 돌았다

**한 줄 후크**:
`(1.38e-23 * 300)`를 볼츠만 상수 × 300 K로 grounding하고 싶었을 뿐인데, 관찰 스크립트가 「23 * 300 = 6,900」이라고 내놓았다. 지수 표기 regex 버그가 1건째. 거기서부터 6바퀴의 사이클로 1,270 → 1,314 PASS, UNKNOWN 단위 0건, TRIZ 거짓 양성 0건까지 도달한 이야기다.

---

## 배경 — 왜 「관찰」을 넣는가

llive는 「**LLM 주위에 씌우는 인지 OS**」를 지향하는 프레임워크로, Brief(구조화된 의뢰)를 받아 FullSenseLoop에 흘려보내기 전에 `BriefGrounder`라는 grounding 층을 통과시킵니다. grounding 층에는 5개 channel이 실려 있습니다:

| Channel | 담당 | 출처 |
|---|---|---|
| **TRIZ** | trade-off 계열 trigger를 검출 | TRIZ 40 원리 |
| **RAD** | 관련 분야 코퍼스에서 인용 | Raptor RAD 49 분야 약 5만 건 |
| **calc (MATH-08)** | 산술식을 deterministic하게 평가 | `SafeCalculator` |
| **units (MATH-01)** | 「수치+단위」를 SI 차원으로 굽기 | `parse_unit` |
| **constants (MATH-05)** | CODATA/NIST 상수를 grounding화 | `get_constant` |

이 5개 channel은 단위 테스트에서 PASS하고 있었습니다. **그런데도 실제 Brief를 돌렸더니, 예상 밖의 동작이 잇따라 나온** 것이 본 글의 주제입니다.

---

## 스텝 0 — 관찰 스크립트의 설계

`scripts/observe_grounding.py`라는 작은 스크립트를 썼습니다(~250줄). 역할은 3가지뿐:

1. 6건의 realistic Brief를 `BriefRunner`를 경유해 실행
2. ledger의 `grounding_applied` event payload에서 citation을 추출
3. Markdown 요약으로 「**어느 channel이 무엇을 surface했는가**」를 가시화

```python
SAMPLE_BRIEFS = [
    Brief("phys-drone", "Design a delivery drone that maintains 5 m/s during a 30 s window at 100 kg payload..."),
    Brief("energy-photon", "Compute the photon energy at 500 nm using the planck constant and the speed of light..."),
    Brief("trade-off", "Resolve the trade-off between high precision and speed..."),
    Brief("bookkeep", "Ship the report in 5 days, then revisit in 2 weeks. Each chapter should be under 30 pages..."),
    Brief("mixed", "Use the boltzmann constant to estimate kT at 300 K and compare with (1.38e-23 * 300)..."),
    Brief("prose-only", "Write the executive summary of the architecture rationale..."),
]
```

**assertion이 아니라 관찰**을 목적으로 하기에 테스트는 쓰지 않고 Markdown만 뱉도록 했습니다. `pytest`는 통과하는데 글을 쓸 근거가 없는 장면에서, 「벤치마크나 관찰」만 별도로 기록하는 습관을 들이고 싶었다는 설계 판단입니다.

### ☕ 그나저나

`observe_grounding.py`는 처음에 「그냥 리포트를 내놓을 뿐」이라고 생각하고 썼습니다. 실제로 돌려보고 reports/observation.md를 연 순간, `23 * 300 = 6,900`이라는 출력에 「으악」 하게 된 것이 1바퀴째의 시작. **관찰 스크립트는 PASS하는 test에서는 절대 보이지 않는 것을 surface한다**는 것을 몸소 확인한 순간입니다.

---

## 1바퀴째 — `(1.38e-23 * 300)`이 `(23 * 300)`으로 오추출

가장 먼저 나온 것이 Brief `mixed`의 출력:

```
- (23 * 300) = 6,900 (ops=1)   ← 오류
```

기대는 `(1.38e-23 * 300) = 4.14e-21`. 볼츠만 상수 × 300 K = kT(300 K에서 약 4.14×10⁻²¹ J)라는 물리 결과.

**원인**: `extract_expressions`의 정규식이 `1.38`의 소수까지만 잡고 `e-23`을 잘라냈다.

```python
# Before
_NUM = r"\d+(?:\.\d+)?"

# After
_NUM = r"\d+(?:\.\d+)?(?:[eE][-+]?\d+)?"
```

회귀 테스트를 3건 추가해 1,288 → 1,291 PASS. 첫 1바퀴는 **regex 1줄 + 테스트 3건으로 완료**.

---

## 2바퀴째 — `500 nm` `5 days`가 UNKNOWN

다음에 온 것이 Brief `energy-photon`과 `bookkeep`의 UNKNOWN 대량 발생:

```
- 500 nm → UNKNOWN: unknown unit symbol 'nm'
- 5 days → UNKNOWN: unknown unit symbol 'days'
- 2 weeks → UNKNOWN: unknown unit symbol 'weeks'
- 30 pages → UNKNOWN: unknown unit symbol 'pages'
- 1 email → UNKNOWN: unknown unit symbol 'email'
```

이 중 `nm`은 SI 접두사 + 단위 기호, `days` `weeks`는 시간 관용어. **이것들은 parser 확장으로 구제해야 한다**. 한편 `pages` `email`은 단위가 아니라 도메인 단어. 나중에 처리한다.

**대응**:
- `_SI_PREFIXES` frozenset(`Y/Z/E/P/T/G/M/k/h/da/d/c/m/μ/u/n/p/f/a/z/y`)
- `_term_dimensions`에서 prefix 시도(2글자 우선으로 `da`를 올바르게 해석)
- 시간 관용 단위를 `_DERIVED`에 추가: `min`/`h`/`hour`/`day`/`days`/`week`/`weeks`/`year`/`years`

1,291 → 1,298 PASS.

### ☕ 여기서 한숨 돌리기

SI 접두사 대응에서 깨달은 것이 「**m과 m의 충돌 문제**」. `m`은 meter(기본 단위)이기도 milli(10⁻³ prefix)이기도 하다. `mm`(millimetre)를 해석할 때 어느 쪽으로 매치시킬 것인가? 해결은 단순해서 「완전 일치 사전을 우선, 접두사 떼기는 fallback」. `m` 단독이면 meter, `mm`이면 meter가 사전에 있으므로 prefix `m` + symbol `m`. 이것은 「**사전 순서의 우선도 설계**」만으로 충돌을 회피할 수 있었던 전형적인 예였습니다.

---

## 3바퀴째 — `the speed of light`의 `speed`가 #35를 오발화

Brief `energy-photon`에서 TRIZ citation을 보면, 예상 밖의 발화가 있었습니다:

```
- #24 Mediator (trigger: via)        ← OK ('Cross-check via the elementary charge')
- #35 Parameter Changes (trigger: speed)   ← 오발화
```

`_TRIZ_TRIGGERS` 사전에서 `"speed": 35`로 등록했기 때문에, `the speed of light`의 `speed`가 그대로 match.

**대응**: 2단계의 정밀도 향상책을 넣었습니다.

1. **Word boundary**: 짧은 English trigger는 `\b{trigger}\b`로 감싼다

   ```python
   _WORD_BOUNDARY_TRIGGERS = frozenset({"vs", "via", "speed", "quality", ...})
   ```

   이로써 `speedy delivery`의 `speedy`에서 `speed`가 오발화하지 않게 된다.

2. **부정 문맥**: 특정 구절이 Brief에 존재할 경우 trigger를 억제

   ```python
   _TRIZ_NEGATIVE_CONTEXTS = {
       "speed": ("speed of light", "lightspeed"),
       "via": ("via point", "via the api"),
   }
   ```

   이로써 `speed of light`를 포함하는 Brief에서는 `#35`가 발화하지 않게 된다. 1,298 → 1,301 PASS.

---

## 4바퀴째 — MATH-07(`MATHEMATICAL` EpistemicType) 미착수

여기까지 「Brief grounding 층의 정밀도 문제」를 고쳐 왔지만, 관찰 스크립트의 집계 칸을 보고 깨달은 것이 **「FACTUAL track은 있는데 MATHEMATICAL track이 없다」**는 점.

llive는 `EpistemicType`(FACTUAL / EMPIRICAL / NORMATIVE / INTERPRETIVE / PRAGMATIC + 예비 5개)로 track을 나눕니다. FACTUAL은 「결론 불변, confidence < 0.7에서 SILENT로 강등」하는 strict mode. **수학 명제는 더 엄격하게 할 수 있을 것**.

**대응**:
- `EpistemicType.MATHEMATICAL = "mathematical"` 추가
- `mathematical_track`: confidence < 0.8에서 SILENT로 강등(FACTUAL의 0.7보다 엄격)
- rationale에 `MathVerifier 검산 가능성을 확인` hint를 첨부

```python
def mathematical_track(stim, plan):
    if plan.thought is not None and plan.thought.confidence < 0.8:
        plan = ActionPlan(
            decision=ActionDecision.SILENT,
            rationale="MATHEMATICAL strict: confidence < 0.8, withholding until MathVerifier 検算可能性を確認",
            ...
        )
    return _tag(plan, "mathematical")
```

1,301 → 1,305 PASS.

### ☕ 잠깐 옆길로

「수학 명제는 다른 도메인보다 엄격하게 해도 된다」라는 것은, 오카 기요시 선생(※)이 남기신 「수학은 정서다」라는 사상과는 방향이 다르게 보이지만, 이쪽은 「**LLM이 무심코 수식을 틀리지 않도록 하는 gate**」를 위한 것. 선생의 사상에서 배우는 층(`OKA-FX`)은 별도 레이어로 설계하고 있습니다. **Defensive(MATH 계열)와 offensive(OKA 계열)를 분리하는** 것이 설계 판단.

(※ 오카 기요시 선생의 사상을 구현했다고 주장하는 것은 아닙니다. 선생이 남기신 풍부한 사색 중, 엔지니어링 언어로서 참조할 수 있는 관점에 착목하여, 설계의 촉발원으로 살리고 있다는 스탠스입니다.)

---

## 5바퀴째 — `pages` `email`의 도메인 단어 노이즈

2바퀴째에 「도메인 단어는 나중에」라고 하며 미뤘던 건입니다. 실제 Brief `bookkeep`에서 `30 pages`, `1 email`, `1 milestone` 같은 표현이 citation에 대량으로 남아 있었습니다.

이것들은 parser가 「unknown unit」으로 error citation에 남기지만, **error citation의 본래 목적은 「확장해야 할 단위를 발견하는 것」**이므로, 도메인 단어가 대량으로 섞이면 신호 가치가 떨어집니다.

**대응**: `_NON_UNIT_WORDS` frozenset으로 필터(28개 단어)

```python
_NON_UNIT_WORDS = frozenset({
    "email", "users", "page", "pages", "item", "items",
    "request", "point", "slide", "chapter", "widget",
    "ticket", "comment", "issue", "row", "column",
    "people", "customer", "step", "task", "milestone", ...
})
```

`_lookup_units`에서 unit_text가 여기에 포함되어 있으면 **silently skip**(citation으로 만들지 않음). 이로써 error citation에는 「parser가 모르는 진짜 단위」(`furlong` 등)만 남게 되었습니다. 1,305 → 1,306 PASS.

### ☕ 그나저나

이때 기존 테스트 1건이 깨졌습니다(`test_grounder_surfaces_unknown_units_as_errors`). 원래 「`5 days` `2 pages`가 error citation에 남는다」를 기대했지만, 이번 세션의 수정으로 `5 days`는 정규 unit으로, `2 pages`는 도메인 단어 필터로 skip으로. **사양 변경으로 기존 테스트가 깨지면, 새 사양에 맞춰 다시 쓰는** 것이 정답. 테스트를 「Brief 안의 `3 furlong`」으로 변경해 회귀를 유지했습니다.

---

## 6바퀴째 — `5 days`를 `5초`와 혼동하지 않기 위해(MATH-06 minimal)

여기까지로 `5 days`는 time 차원으로 인식할 수 있게 되었지만, **값은 아직 5인 채**. LLM이 후단에서 「days를 seconds로 변환」하는 책임을 지는 설계라면, 변환 누락으로 인한 치명적인 버그(5초의 실험이 되어 버린다)가 일어난다.

**대응**: `Quantity` API는 건드리지 않고, citation 층에 `si_factor` / `si_value`를 추가.

```python
@dataclass(frozen=True)
class UnitCitation:
    raw_text: str
    value: float          # 원래 수치 (5)
    unit_text: str        # "days"
    dimensions: str       # "s"
    si_factor: float = 1.0   # 86400
    si_value: float = 0.0    # 432000
    error: str | None = None
```

grounded prompt 출력:
```
- 5 days → value=5.0, dimensions=s, SI=432000.0 (×86400.0)
- 500 nm → value=500.0, dimensions=m, SI=5.0e-7 (×1e-9)
```

이로써 LLM은 「**실은 SI base로 432,000초**」라고 즉시 알 수 있어, 변환 실수의 리스크가 줄어듭니다.

1,306 → 1,314 PASS.

---

## 정리 — 관찰 스크립트가 효과를 본 이유

| 바퀴 | 발견 | 수정 | PASS |
|---|---|---|---|
| 1 | 지수 표기 regex 버그 | `_NUM` atom 확장 | 1,291 |
| 2 | SI prefix + 시간 관용어 미대응 | parser 확장 | 1,298 |
| 3 | TRIZ trigger 거짓 양성 | word-boundary + 부정 문맥 | 1,301 |
| 4 | MATH-07 미착수 | `MATHEMATICAL` track | 1,305 |
| 5 | 도메인 단어 노이즈 | 28개 단어 필터 | 1,306 |
| 6 | scale 미표시 | minimal `si_factor`/`si_value` | **1,314** |

합계 +44 PASS, 회귀 제로, UNKNOWN 단위 제로, TRIZ 거짓 양성 제로.

**얻은 교훈**:

1. **관찰 스크립트는 PASS 테스트에서는 보이지 않는 곳을 surface한다** — 단위 테스트는 「예상대로의 입력에 예상대로의 출력」을 보증하지만, 실제 Brief는 단위 테스트 작성자가 떠올리지 못한 조합을 넣어 온다
2. **error citation을 silently drop하지 않는 설계가 기능했다** — 「unknown unit을 남긴다」는 설계를 넣었기에, 관찰에서 「확장해야 할 사전」을 자동 수집할 수 있었다
3. **작은 수정을 6바퀴 돌리는 편이, 한 번에 대폭 개수하는 것보다 성과가 난다** — 각 바퀴는 regex 1줄 / 사전 28개 단어 / 부정 문맥 dict 등 20줄 이하. 이것을 6바퀴 돌림으로써 반죽이 성숙해졌다
4. **Quantity API의 파괴적 변경은 피하고 citation 층에서 완결**(MATH-06 minimal) — 후단에서 본격적인 scale-aware Quantity 산술이 필요해질 때, 과거의 판단에 얽매이지 않는 자유도를 남길 수 있었다

---

## 남은 과제와 운용

| 후보 | 스코프 | 착수 판단 |
|---|---|---|
| MATH-03 LaTeX/MathML 구문 해석 | 중 | 실제 Brief에서 LaTeX 수식이 surface한 후 |
| MATH-04 IEEE 754 정밀도 트래킹 | 대 | 위와 동일 |
| Cross-quantity 차원 연산 체크(`5 m/s + 3 s`) | 중 | 관찰에서 구체적인 mismatch가 나온 후 |
| Quantity scale-aware 산술(MATH-06 후단) | 파괴적 변경 포함 | 필요성 확인 후 |

모두 「실제 Brief 관찰 기반으로 필요성 surface 후」라는 보류 방침. **지금 당장 착수할 근거가 없는** 것은, 관찰 스크립트의 결과가 「unit/calc/constants/TRIZ의 minimal grounding이 현 상태 6 Brief에서 충분히 기능한다」고 알려 주고 있기 때문.

llive의 리포지토리:
- <https://github.com/furuse-kazufumi/llive>
- 본 글의 수치 근거: `docs/benchmarks/2026-05-17-grounding-observation/observation.md`
- 관찰 스크립트: `scripts/observe_grounding.py`

「구현 → 관찰 → 과제 발견 → 즉시 수정」 사이클에 관심 있는 분은 Issue / Discussion으로 꼭 와 주세요.

---

## 참고문헌 / 참고 리소스

### CODATA / NIST (MATH-05 관련)
- CODATA 2022 Recommended Values — <https://physics.nist.gov/cuu/Constants/>
- NIST SP 330: The International System of Units (SI)

### TRIZ (제3바퀴 수정의 관련)
- Genrich Altshuller, *And Suddenly the Inventor Appeared: TRIZ, the Theory of Inventive Problem Solving*, Technical Innovation Center, 1996

### llive 관련
- llive 리포지토리 — <https://github.com/furuse-kazufumi/llive>
- 「제2의 뇌」 시리즈 전 4부 (구축론/운용론/비전론+비가시 Annotation)
