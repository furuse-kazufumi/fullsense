# Pre-registration — Proxy v2 フル走: memory↔quality NAS の統計的に正直な評価

- **日付**: 2026-06-28
- **status**: `pre-registered`(実行は GPU 着荷後 / RTX 5090 32GB)
- **interim agenda 対応**: T1 実験 3/3(`docs/research/interim_research_agenda_2026-06-28.md` §T1)
- **対象コード(実在確認済)**:
  - `D:/projects/llcore/src/llcore/runtime/eval_proxy.py`(proxy-v2 全関数)
  - `D:/projects/llcore/scripts/nas_pareto.py`(driver、`--proxy-v2` 配線・`_proxy_v2_rigorous`)
- **正本知見**: eval_proxy.py module docstring(v1 の欠陥分析)/ `MODEL_LANDSCAPE_2026_06.md`(NAS 新規性)/ SUPRA 長文脈崩壊(`next_plan.md` L2)
- **honest 規律**: `feedback_benchmark_honest_disclosure`(内訳を疑う)/ eval_proxy.py 自体が honest-disclosure を中核設計

> **凍結宣言**: holdout 数・context sweep・cross-corpus・主要指標・成功 verdict を実行前に固定。eval_proxy.py は **設計段階で解析自由度を凍結する装置**(`build_proxy_v2_report` が scope を pin)。本 prereg はその凍結を実験計画として明文化する。

---

## 1. 背景

`nas_pareto.py` の **v1 proxy** は各 genome を **256-token 1 窓・1 コーパス・誤差棒なし**の単一 Δnll でスコアした。eval_proxy.py module docstring が明記する 3 つの致命傷:

1. **短文脈の盲点**: constant-state 線形 attention の品質コストは長文脈(2k–8k+、SUPRA 級)で顕在化。256 tok は **劣化を系統的に過小検出**。
2. **メモリ crossover 未満**: 線形 vs softmax のメモリ交差は ~227 tok。256 tok は「節約がほぼ無い所」で品質を測っている。
3. **誤差棒なし**: 「進化した frontier が greedy に勝つ」「config X が all-softmax に勝つ」を **1 点 Δnll では支えられない**(winner's curse / 窓ノイズ)。

proxy-v2(eval_proxy.py、実装済 + テスト済)は 3 層でこれを解く:

- **fast inner-loop**(全 genome): paired multi-window Δnll @ 中程度 context(default L=1024)→ GA が選ぶスカラ平均 + bootstrap CI が随伴(`fast_proxy`/`bootstrap_paired_ci`)。
- **rigorous frontier-only**(非劣解のみ): **fresh disjoint holdout** で再評価(winner's curse 除去、`reeval_frontier` + `optimism_gap`)、context sweep(`context_sweep`)、needle/passkey(`needle_horizon`)。
- **diagnostics**(選択に絶対 feed しない): HV gain CI、蒸留右シフト CI、attention-KL(256 cap)、proxy-vs-judge 順位相関。
- **honest chokepoint**: `honest_verdict`(全 guard → 1 verdict)+ `build_proxy_v2_report`(scope='next_token_nll_proxy' を pin、`conversational_claim=None`)。

### 実装状態

proxy-v2 は **実装+単体検証済**(`fast_proxy` が v1 平均と一致、`suffix_losses` が golden test で `window_losses` と一致、CI/sign/wilcoxon が pure-numpy)。**実走(フル GPU、K≥12、長 sweep、cross-corpus)は未実施** = 本 prereg が登録する本走。

---

## 2. 仮説(falsifiable)

- **H1(memetic vs greedy / 主仮説)**: memetic NAS frontier は greedy(budget スキャン)frontier を **holdout hypervolume** で上回る。
  - **真なら成功**: `honest_verdict` の `memetic_vs_greedy` が「memetic beats greedy」(HV gain 95% CI 下限 > 0)かつ confidence ∈ {significant, suggestive}。
  - **棄却**: verdict が「no significant difference」(CI 0 跨ぎ)/「greedy not beaten」/「suppressed」(optimism_gap が noise floor 超)。
- **H2(regime 依存)**: 線形化の品質コストは context 長で単調増(短いと隠れる)。
  - **真なら**: `context_sweep` の Δnll が L=256→2048(→4096)で単調増、長 L で CI 下限>0(有意な劣化)。
  - **棄却**: L 依存なし → v1 の短窓でも十分だった(proxy-v2 の前提が崩れる、これも重要な発見)。
- **H3(cross-corpus 汎化)**: search コーパス(aozora)で選んだ frontier が **disjoint コーパス**でも greedy を上回る。
  - **真なら**: cross-corpus holdout の Δnll で memetic ≤ greedy(同符号・CI 整合)。
  - **棄却**: 別コーパスで逆転 → frontier はコーパス過適合(汎化しない)。
- **H4(蒸留右シフト)**: `--distill` 併用で frontier が右シフト(`right_shift_ci` 下限>0)。※`prereg_linearization_distill.md` H1 と同一機構を NAS 文脈で再確認。
- **H5(needle 崩壊帯)**: 最 aggressive な線形 genome は長文脈 needle retrieval で all-softmax より早く失敗する(`needle_horizon` が有限値)。
  - **真なら**: horizon ∈ {2048, 4096}(softmax は acc=1 維持下で線形が acc<1)。
  - **棄却**: horizon=None → 選ばれた hybrid は長文脈 retrieval を保持(良い知らせ)。

> 事前予想(honest 記録): proxy-v2 の動機自体が「v1 は短窓で過小検出」なので、**H2 は支持(長 L で劣化顕在化)寄り**。H1(memetic 勝利)は **optimism_gap に殺されやすい**と予想 — `honest_verdict` が selection optimism > noise floor で verdict suppress する設計なので、勝利宣言には holdout が要る。

---

## 3. 実験デザイン

### 3.1 要因 / arm

| 要因 | 水準 |
|---|---|
| **base モデル**| Qwen2.5-0.5B-Instruct(主、24層)/ 1.5B(28層、規模頑健性)|
| **frontier**| greedy(`--budgets` スキャン)vs memetic(`evolve_multiobjective`、`--pop`/`--generations`)|
| **蒸留**| なし / `--distill`(出力 MSE)|
| **context(inner)**| `--inner-context 1024`(227-tok crossover と劣化 onset の右)|
| **context sweep(frontier)**| `--context-sweep 256,512,1024,2048,4096`(SUPRA 級長文脈崩壊帯まで)|
| **holdout windows(K)**| **`--holdout-windows 12` 以上**(docstring: <12 は CI を unreliable に降格)|
| **cross-corpus**| `--cross-corpus <disjoint file>`(aozora と非重複)|
| **needle**| `--needle --needle-lengths 2048,4096`(depths 0.0/0.25/0.5/0.75/0.9 は関数 default)|
| **seed**| **0, 1, 2(≥3)**(`--seed`、GA 確率性 + bootstrap seed)|

### 3.2 K≥12 holdout と窓独立性(★統計の核)

- **fast pool**: `--fast-windows 8`(K_fast)で inner-loop(GA 選択用)。
- **holdout pool**: `--holdout-windows 12`(以上)。`make_windows` は **default stride=L で非重複**(窓 bootstrap が anti-conservative にならない独立性ガード)。`--holdout-offset` で fast pool の先(disjoint prefix)から取る(`_proxy_v2_rigorous` が `used` トークン後に自動設定)。
- **K の意味**: bootstrap CI は K 個の paired per-window Δnll を resample(`bootstrap_paired_ci`、2000 resample)。K<12 で CI が広く unreliable になるため **12 を下限**に固定。長 L(2048/4096)ではコーパス長が窓数を律速 → コーパスを十分長く(`--text-file` を大きく)。

### 3.3 context sweep 2048–4096(SUPRA 級崩壊帯)

- `context_sweep(model,…, lengths=(256,512,1024,2048), K=holdout_windows)` が各 L で fresh holdout 窓を切り、paired Δnll + CI + sign_test。
- **本走では 4096 を追加**(`--context-sweep 256,512,1024,2048,4096`)。`context_sweep` は **full forward**(O(L²)、線形含む任意 mixer で正しい)を使う = 4096 は VRAM/計算が重いが RTX 5090 32GB なら 0.5B で可。1.5B は 4096 で要監視(OOM 時は 2048 まで)。
- **honest**: 長 L の full forward は softmax 側も O(L²) → 4096 は frontier の最 aggressive genome 1 個に限定(`_proxy_v2_rigorous` の設計どおり frontier-only)。

### 3.4 cross-corpus

- `nas_pareto.py` は `--cross-corpus <file>` を読み(`ctext[50000:]` でオフセット)、`make_windows` で窓を切り、memetic/greedy 両 frontier を `reeval_frontier`(disjoint コーパス holdout)。
- **disjoint コーパス要用意**(要追加データ): aozora と語彙/ドメインが重ならない別テキスト(例: 技術文書 / 別作家 / Wikipedia 抜粋)。tokenizer は base モデルの BPE(Qwen2)なので char-vocab 制約はなし。

### 3.5 指標確定(事前固定)

- **fast inner**: `mean_dnll`(GA 選択)+ `ci_lo/ci_hi/p_worse/n_windows`(随伴 CI)。
- **frontier holdout**: `delta_nll_heldout`(headline)/ `optimism_gap`(= selection − heldout)/ `ci_lo/ci_hi/p_worse`/ `pos_frac`/`p_sign`。
- **HV gain**: `bootstrap_hv_gain`(paired window resample、`gain_pct_mean` + CI + `p_memetic_wins`)。
- **右シフト**: `right_shift_ci`(`shift_pct_mean` + CI + verdict)。
- **needle**: `horizon` + `by_depth`(argmax_acc / mean_logprob / control_acc)。
- **attention-KL**(診断のみ、256 cap): `genome_attn_kl`(mean/max/sum/per_layer)。**NAS fitness に絶対 wire しない**。
- **proxy-vs-judge**: `kendall_tau`/`spearman_rho`(τ<0.7 で verdict を「suggestive」に降格)。
- **最終 verdict**: `honest_verdict`(precedence: optimism 超過→suppress / CI 0 跨ぎ→null / CI<0→null / else memetic 勝利、τ<0.7 で suggestive)。`build_proxy_v2_report` が `scope='next_token_nll_proxy'`・`conversational_claim=None` を pin。

### 3.6 device

`nas_pareto.py` は `load_qwen2` でモデルロード。明示 `--device` 無し(grep 確認)→ **`load_qwen2` の to(device) 配線が要追加**(backward-compatible auto、`migration_manifest §6` 方針)。CPU では byte-identical。

---

## 4. 測定指標と解析手順

- **主要指標(事前指定・1 つ)**: **memetic-vs-greedy の holdout hypervolume gain %**(`bootstrap_hv_gain.gain_pct_mean` + 95% CI、`honest_verdict` 経由)。これが NAS の中心主張「層別 hybrid 探索が固定ヒューリスティックに勝つ」の直接尺度。
- **副次**: context_sweep の L 別 Δnll 曲線(H2)/ cross-corpus holdout Δnll(H3)/ right_shift %(H4)/ needle horizon(H5)/ optimism_gap(楽観バイアス監査)。
- **解析手順(事前固定)**:
  1. seed 0/1/2 で `--proxy-v2` フル(K=12、sweep …4096、cross-corpus、needle、distill)。
  2. 各 seed で `honest_verdict` を取得 → **3 seed で verdict が一致するか**(頑健性)。多数決でなく、全 seed で CI 下限>0 のときのみ「勝利」。
  3. **optimism_gap の監査**: 各 frontier 点の `optimism_gap` を列挙。最大値が CI half-width floor を超えたら(`honest_verdict` が suppress)→「選択楽観が支配」と正直に報告し、勝利を主張しない。
  4. **H2**: context_sweep の (L, mean, ci_lo, ci_hi) を曲線化。CI 下限>0 になる最小 L = 「劣化が有意化する文脈長」。
  5. **proxy-vs-judge**: 可能なら小規模 LLM-judge(別途)で frontier を採点し τ を計算(τ<0.7 なら全 verdict を suggestive 止め)。judge 未整備なら τ=None で「significant/suggestive 判定は proxy 内に閉じる」と明記。
- **有意性**: paired bootstrap(2000、window resample)+ sign_test + wilcoxon_perm(n≤12 で exact)。全て eval_proxy.py に実在・pure numpy。

---

## 5. 成功基準(事前固定)と honest 内訳プラン

### 成功基準

- **PASS(H1)**: 全 3 seed で `honest_verdict` = 「memetic beats greedy」、HV gain 95% CI 下限 > 0、confidence=significant(τ≥0.7 or judge 未使用明記)、**かつ** cross-corpus でも符号一致(H3)。
- **NULL**: verdict が seed 間で割れる / suppress / CI 0 跨ぎ。→「層別 NAS は固定ヒューリスティックに対し holdout で有意差なし」を確定(誇張しない。eval_proxy.py の設計思想そのもの)。

### honest 内訳プラン(`feedback_benchmark_honest_disclosure`、eval_proxy.py の設計と二重化)

1. **winner's curse(最重要)**: GA は数百 genome から非劣解を拾う = max-of-N 楽観。**headline は必ず `delta_nll_heldout` / HV gain on holdout**。`optimism_gap` を毎回開示し、noise floor 超なら `honest_verdict` の suppress に従う。
2. **短文脈 artifact**: 256 tok の見かけ勝利を信じない。`context_sweep` 長 L で消えるなら「劣化を隠していた」と記録。
3. **窓非独立**: 重複窓で CI を狭める anti-conservative を回避(`make_windows` non-overlap 既定を維持)。K≥12 を死守。
4. **cross-corpus 過適合**: 単一コーパス勝利を一般化しない。disjoint コーパスで逆転したら「aozora 過適合」と書く。
5. **attention-KL の誤用禁止**: 診断専用・256 cap・fitness 非連結(コード強制)。KL が低い=会話が良い、と読み替えない。
6. **scope の厳守**: `build_proxy_v2_report` が pin する `scope='next_token_nll_proxy'` / `conversational_claim=None` を尊重。**perplexity proxy から会話品質を主張しない**(別の disclosed 生成 eval が要る)。
7. **needle の非自明性**: `build_passkey_prompt` は gap 内に答えが再出現したら ValueError(局所コピー不能を保証)。control_acc(softmax 基準)で gate し、線形のみの失敗を分離。
8. **規模限定**: 0.5B/1.5B・aozora 中心の結論を 7B+ へ外挿しない。1.5B 再走で規模頑健性のみ確認。

---

## 6. 実行コマンド(具体・既存引数のみ)

> 全フラグ(`--proxy-v2`/`--inner-context`/`--fast-windows`/`--holdout-windows`/`--holdout-offset`/`--context-sweep`/`--cross-corpus`/`--needle`/`--needle-lengths`/`--distill`/`--budgets`/`--pop`/`--generations`/`--seed`/`--checkpoint-every`/`--out`)は nas_pareto.py の argparse で **実在確認済**。`--device auto`(load_qwen2 配線)は **要追加**。

```powershell
# --- proxy-v2 フル走 (0.5B, 3 seeds) ---
foreach ($s in 0,1,2) {
  py -3.11 D:/projects/llcore/scripts/nas_pareto.py `
    --model-dir D:/models/Qwen2.5-0.5B-Instruct `
    --text-file out/corpus_aozora_multi.txt `
    --proxy-v2 `
    --inner-context 1024 --fast-windows 8 `
    --holdout-windows 12 `                              # K>=12 (CI 信頼下限)
    --context-sweep 256,512,1024,2048,4096 `            # SUPRA 級崩壊帯まで
    --cross-corpus out/corpus_holdout_disjoint.txt `    # DISJOINT (要用意)
    --budgets 0.02,0.05,0.10,0.15,0.25,0.50 `
    --pop 24 --generations 20 `
    --distill --distill-steps 400 --distill-lr 5e-2 --distill-tokens 512 `
    --needle --needle-lengths 2048,4096 `
    --checkpoint-every 20 `                             # ccr 再ログイン/OOM 耐性
    --seed $s `
    --out out/proxy_v2_full/qwen0p5b_seed${s}
}

# --- 規模頑健性 (1.5B, seed 0; 4096 は OOM 監視, 必要なら sweep を 2048 まで) ---
py -3.11 D:/projects/llcore/scripts/nas_pareto.py `
  --model-dir D:/models/Qwen2.5-1.5B-Instruct `
  --text-file out/corpus_aozora_multi.txt `
  --proxy-v2 --inner-context 1024 --fast-windows 8 --holdout-windows 12 `
  --context-sweep 256,512,1024,2048 `
  --cross-corpus out/corpus_holdout_disjoint.txt `
  --pop 24 --generations 20 --distill --needle --needle-lengths 2048,4096 `
  --checkpoint-every 20 --seed 0 `
  --out out/proxy_v2_full/qwen1p5b_seed0
```

> 注: `--cross-corpus` の disjoint ファイルは別途用意(要追加データ。aozora と非重複ドメイン)。長 L=4096 × 1.5B は VRAM 律速 → OOM 時は `--context-sweep` を 2048 まで下げる(honest に「4096 は 0.5B のみ」と記録)。`--checkpoint-every 20` で eval cache を snapshot(kill/restart でも時間を失わない)。

---

## 7. 想定アウトプット先

- `D:/projects/llcore/out/proxy_v2_full/qwen0p5b_seed{0,1,2}/`(nas_pareto report、`proxy_v2` ブロック: context_sweep / frontier_holdout / hv_gain_ci / right_shift_ci / needle / attention_kl / cross_corpus + `honest_verdict`)
- `D:/projects/llcore/out/proxy_v2_full/qwen1p5b_seed0/`
- `D:/projects/llcore/out/proxy_v2_full/eval_cache.json`(resumability snapshot)
- `D:/projects/llcore/out/proxy_v2_full/ANALYSIS.md`(3 seed の honest_verdict 一致表 + HV gain CI + context_sweep 曲線 + optimism_gap 監査 + cross-corpus 符号)
- 結論は MODEL_LANDSCAPE の NAS 節へ反映。会話品質クレームは **本走から出さない**(scope pin)。
