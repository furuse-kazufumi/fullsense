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
