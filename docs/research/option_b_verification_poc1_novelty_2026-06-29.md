# option-b 一次検証 — PoC-1 未踏性 / 引用本文 / base 乗換 / VLM (2026-06-29)

> **provenance**: 検証ワークフロー `llcore-primary-source-verify` (wp7ugxvch, **25 agents / 244 tool uses / ~17 min**)。
> 12 task(論文本文 7 + 未踏性 3 + Qwen base + VLM)を arXiv 本文/HTML で一次精読 → 各 finding を敵対的 refute → 統合。
> 規律: triz §5「未踏は absence-of-evidence / abstract のみ → 本文検証必須」の実行。全 verdict は adversarial review 生存(flip は N3 の 1 件のみ)。
> **接続(矛盾を是正する対象)**: `triz_constant_state_recall_2026-06-29.md`(TOP-1/2/3)/ `efficient_arch_landscape_refresh_2026-06-28.md`(§4.2 prereg)/ `distill_protocol_and_differentiation_2026-06-28.md` / memory `project_llcore_efficient_arch_landscape_2026_06_26`。
> **honest 注**: 本統合は findings JSON の合成。各 finding の一次 fetch は検証セッションで実施済(本統合での再 fetch なし)。novelty(N1/N2/N3)の confidence は absence-of-evidence 規律で medium 据え置き、writeup 前の citing-graph 深掘りは未実施=未検証点。

---

## 1. 検証結果サマリ表

| task_id | load-bearing claim (要約) | verdict (post-refute) | confidence | refute で変化したか | key evidence |
|---|---|---|---|---|---|
| P1-CCQ | CCQ の read は single-shot / 解析的 / 非学習 / 非反復、read 側を最初に開いた | partially_confirmed | high | 不変(\"non-learned\" のみ不正確: 学習スカラゲート λ_t=σ(W_λq+b_λ) あり) | [2606.01294](https://arxiv.org/abs/2606.01294) |
| P2-GDN2 | channel-wise erase/write 分離、linear pure-recurrent で最強 RULER/NIAH | confirmed | high | 不変(NIAH 数値は桁一致で finding より保守的) | [2605.22791](https://arxiv.org/abs/2605.22791) |
| P3-FDM | 最近接 cross-domain 競合だが single-shot + 272-slot cache、数値信用不可 | confirmed | high | 不変(O(1) 表現の精緻化のみ) | [2604.07716](https://arxiv.org/abs/2604.07716) |
| P4-JetNemotron | 凍結事前学習モデルから PostNAS で hybrid 改修、softmax 層残す | confirmed | high | **要修正**: base は Qwen2.5-1.5B(Qwen3-1.7B は比較ベースライン) | [2508.15884](https://arxiv.org/abs/2508.15884) |
| P5-STAR | gradient-free 進化 × LIV 整数ゲノム × NSGA-2 多目的、constant-state ブロック含む | confirmed | high | 不変(ICLR 2025 **Oral** と判明=より強い) | [2411.17800](https://arxiv.org/abs/2411.17800) |
| P6-1stepRead | 「read=1勾配ステップが最適」が理論的 kill-risk | partially_confirmed | high | 不変(kill-risk 推論**非成立**、softmax-only 反論も無効) | [2502.05164](https://arxiv.org/abs/2502.05164) |
| P7-Ceiling | state resolution > 蒸留予算、additive は ~0% NIAH で不可逆飽和 | confirmed | high | 不変(引用語/日付の軽微修正のみ) | [2504.14366](https://arxiv.org/abs/2504.14366) |
| N1-TTT-readside | read 側 test-time 最適化の先行なし、PoC-1 niche 未占有 | partially_confirmed | medium | claim 文言**過大**(CCQ・Top-K Completion が read 側に存在) | [2506.05233](https://arxiv.org/abs/2506.05233) |
| N2-LISTA-read | 凍結 native linear-attn state 上の unrolled-ISTA read は未踏 | partially_confirmed | medium | 不変(最近接 CS-VLM は softmax+追加射影+学習層) | [2507.02957](https://arxiv.org/html/2507.02957v1) |
| N3-DEQ-Hopfield-read | 非softmax + sparsity-prior 反復 read over linear-attn は未占有 | **contradicted(flip)** | medium | **★flip**: Resonator Network/VSA が占有 | [1906.11684](https://arxiv.org/abs/1906.11684) |
| F1-Qwen35-swap | Qwen3.5-0.8B/2B への base 乗換は low-friction | partially_confirmed | high | **前提矛盾**: 実体は multimodal + 18/24 層 Gated DeltaNet | [HF API](https://huggingface.co/api/models/Qwen/Qwen3.5-0.8B) |
| S1-VLM-scope | quad→linear 蒸留は VLM に転移可、constant-state は vision-KV 爆発で最有用 | confirmed | high | 不変(recall 下限の反論は非 load-bearing) | [2502.13145](https://arxiv.org/abs/2502.13145) |

verdict flip は **N3 の 1 件のみ**。他は全 finding が adversarial review を生存。

---

## 2. PoC-1(test-time iterative read)未踏性の最終判定

**結論: PoC-1 の read 機構そのものは「未踏」ではない。生き残る新規性は狭い application/domain-transfer に縮小。ただし a-priori-dead ではない。** 判定 = **go-with-caveats(正直フレーミングへ再定義必須)**、機構レベル新規性を要求されるなら **pivot-to-TOP2 / NAS-allele(P5系)**。

- **P6(理論的 kill-risk)= 非成立。a-priori death なし。** 「1勾配ステップ最適/反復有害」は実在だが射程が狭い(Bayes 事後平均の in-context denoising、明示・非圧縮 context token、L→∞ 漸近)。PoC-1 の「圧縮 S=Σkvᵀ からの sparse 復元」とは task も memory model も逆。**副作用**: この最適性は softmax 非依存(線形も同 1-step 最適, Prop 3.2)→ prior doc の「softmax 専用だから線形に効かない」防御は**無効**。非転移の真因は energy form でなく task+memory-model mismatch。
- **P1(CCQ)/P3(FDM)は pre-empt しない。** CCQ = 単発閉形式 contraction (I−λΣ)q(学習ゲート1個)、FDM = 単発乗算ゲート + 272-slot token cache(純 scan の MQAR=0.011)。どちらも反復でも compressed-sensing inversion でもなく、CCQ はむしろ「read 側未開拓」枠組みを補強。
- **N1/N2: 厳密な合成(凍結 native linear-attn state + 反復 ISTA/sparse-prior + no softmax + post-hoc distilled)を 1 本で占有する論文は未発見。** ただし read 側は急速密集中: MesaNet(2506.05233, 反復 CG ridge readout だが state 更新・dense・学習)、CS-VLM(2507.02957, ISTA/LISTA だが softmax+追加射影+学習)、CCQ、Top-K Completion(2604.05438, post-hoc だが one-pass)。N1 の「先行なし」は**過大**。
- **★N3 が決定打(flip)**: PoC-1 が「survive する新規性」と見た核(**codebook/dictionary-prior sparse-recovery を圧縮 sum-of-outer-products 定数状態上の反復・非softmax READ として使う**)は、**Resonator Network / VSA cleanup memory(1906.11684, 2208.12880, 2211.05052, 2303.13957)が既に占有**。Schlag(2102.11174)で「linear attention = 加法 outer-product fast-weight memory」のため「linear-attention state」限定詞は対象を足さない。

**総合**: 反復 read 機構は VSA/resonator により占有済み。未占有は **application wrapper(凍結・蒸留済み LLM の linear-attention KV 状態へ decode 時適用)のみ = novel mechanism でなく domain-transfer + engineering**。

**追加リスク(逆風)**: P7「不可逆 state saturation」。書込み時に情報破壊される vanilla-additive S では、いかなる query 時 cleanup でも復元不能(vanilla LA は 0% NIAH)。**read-only on frozen vanilla-additive state は最弱変種** → gated/delta 状態(精度保持を P7 が実証)に適用するか書込み則を変える方が遥かに防御可能。

**推奨(go-with-caveats)**:
1. 「first iterative read」と主張**しない**(N3 で偽)。正直に「既知の resonator/VSA codebook sparse-recovery read を蒸留 LLM の凍結 linear-attention 状態へ decode 時転用する engineering 貢献」と位置付け。
2. MesaNet / CS-VLM / CCQ / FDM / Resonator に対し差別化軸を明示(反復 × sparse-prior × 真の凍結蒸留状態 × post-hoc)。
3. P7 を受け vanilla-additive でなく **gated/delta 状態**へ適用、または書込み則変更を検討。
4. writeup 前に CCQ/MesaNet/CS-VLM/Resonator の citing-paper 深掘りクロール(read 側急速密集中、medium confidence のまま)。
5. 査読で機構レベル新規性が必須なら **TOP-2 / NAS-allele へ pivot**: P5(STAR) 裏付けの NAS-allele/Pareto 路線は一次資料の地盤が最も固く機構新規性の主張余地大。

---

## 3. Write 側飽和(P2 Gated DeltaNet-2)

**「write 側飽和」= 否定(confirmed, contradicts_prior_doc=true, high)。** GDN-2(2605.22791, Hatamizadeh/Choi/Kautz, NVlabs)は channel-wise erase gate b_t∈[0,1]^{d_k} と write gate w_t∈[0,1]^{d_v} でスカラ結合を分離(Eq.10)。**状態も softmax も増やさぬ純 write/erase 変更だけで MK-NIAH で KDA 比 +約9-10pt**(NIAH は HTML 表と桁一致)。並走 Qwen/Alibaba \"Erase-then-Delta\"(2606.26560)も erase/write 分離フロンティアを押す=活発で生産的な headroom。

**caveat**: (a)「linear pure-recurrent で最強」は recurrent-only 比較では成立だが、論文最良 overall は 2K SWA hybrid(53.97% > recurrent 53.11%)で pure-recurrent が full softmax を超えるとは非主張。(b) GDN-2(ゲート振幅分離)と EDA(erase/write アドレス分離)は異なる分離軸。PoC-1 とは orthogonal-to-complementary(pre-empt せず)。

---

## 4. 天井制約(P7)— 「relaxation not breakthrough」は honest か

**Honest。confirmed/high。** 一次(2504.14366, Haller/Golde/Akbik, HU Berlin)が verbatim 支持: 「state resolution is a more fundamental bottleneck than the distillation budget」「cannot be overcome by simply scaling training compute」「additive models suffer from irreversible state saturation」。vanilla LA は S-NIAH 全 ctx 0.0%、RetNet 2k+ で 0.0%、Gated DeltaNet 81.8%@2k(Table 3 桁一致)。蒸留予算 80M+160M→10B token でも gap が漸近残=アーキ的下限。→ read 側 PoC は「固定解像度状態からの読み出し改善=ceiling-relaxation/mapping」で「plateau-breakthrough」ではない、は正確。

**正直修正(verdict 不変)**: 「destructive interference」「capacity ~ d」は論文語でなく解釈 gloss(論文語=state resolution/saturation/irreversible)。\"distillation budget\"(token なし)。v3 日付=2026-01-28。**scope**: 論文 Limitations が「hybrid(intra/inter-layer)は扱わない」=天井は純 linearized mixer のみを拘束 → sparse softmax 層追加/write 則変更 PoC はこの資料の射程外。

---

## 5. Qwen base 乗り換え(F1)— go/no-go + porting cost + license

**License = OK(Apache-2.0、gated:false、生 LICENSE/HF API 確認)。商用障壁なし。**

**Go/No-Go = literal swap(Qwen3.5-0.8B/2B を like-for-like 蒸留 base に)は NO-GO(partially_confirmed, contradicts_prior_doc=true, high)。** 生 config.json が「comparable small dense softmax text model」前提を反証: Qwen3.5 は `Qwen3_5ForConditionalGeneration`(**multimodal**, vision_config 付)で 24 層中 **18 層が Gated DeltaNet 系 linear_attention**(softmax QKᵀ なし)、softmax GQA は **6 層のみ**(full_attention_interval:4)。llcore PoC の「Qwen2 softmax 注意を O(1) 線形状態へ蒸留」対象が 75% 層で消失。加えて mrope partial-rotary(0.25)、attn_output_gate=true、head_dim=256 decoupled、vocab 248320、transformers≥4.57 等差分多数。

**Porting cost(`_capture_layer_io` Q/K/V フック)**: 忠実移植は **HIGH**(multimodal text subtree への path 再ターゲット、18 GatedDeltaNet 層の分岐、qkv-bias 廃止、head_dim config 読み、GQA 8:2、mrope 対応)。6 full-attention 層のみ hook なら MEDIUM-HIGH だが 25% しか蒸留できず前提崩壊。

**推奨**: softmax→linear 蒸留前提を保ち base を近代化するなら **Qwen3-0.6B / Qwen3-1.7B**(`Qwen3ForCausalLM` 平文、全層 full softmax GQA、Apache-2.0)。フック移植 **LOW-MEDIUM**(qkv-bias 除去、head_dim=128 config 読み、GQA 16:8、Qwen3 内在 QK-RMSNorm 留意)。Qwen3.5 の native Gated DeltaNet は「constant O(1) state」設計の **Apache-2.0 reference/teacher・baseline comparator** として活用(蒸留ソースにしない)。

**caveat**: cutoff(2026-01)後の Feb-Mar 2026 リリースで公式 blog 404。存在根拠は生 config.json + LICENSE + HF API + 傍証報道(一次性高いが公式 blog でない)。

---

## 6. T6 VLM(S1)— scope verdict + posture

**Scope verdict = confirmed(high)。ただし「landscape + 蒸留転移 feasibility」に限定** — llcore 固有の iterative-read add-on が VLM で動く確証ではない(そこが実 research risk)。

一次(fetch 済 abstract 5本): **mmMamba(2502.13145)** が「既存 MLLM(HoVLE)を段階蒸留で linear-complexity 化」を実証(103K token で 20.6x speedup / 75.8% VRAM 削減)。**OmniMamba(2503.08686)** は linear multimodal が 2M pairs(Show-o の 1/1000)で学習可。**FastV(2403.06764)**: vision token は layer 2 以降で高冗長(45% FLOPs 削減)。**InternVL1.5(2404.16821)**: 動的高解像度 1-40 タイル→単一画像 ~10k vision token。→ vision-KV 爆発が支配コスト=constant-state recall の差別化が最も効く領域。

**Posture = PARK → shallow-prototype(2 条件 gate)**: (a) GPU 到着、(b) text PoC が signal を示す。iterative-read 仮説は text(Qwen 0.5/1.5B)で最安に falsify でき、VLM はコスト増のみ。mmMamba/OmniMamba が蒸留路転移を既証 → 遅延の科学リスク小。unpark 時は既 linearized 小型 VLM backbone 再利用で「植え込んだ vision token 値を constant state S から iterative-read で復元できるか」だけ検証する 1-2 週 spike。

**caveat**: **recall-memory tradeoff の理論的緊張** — Zoology(2312.04927)/Based(2402.18668) は「厳密 associative recall には recurrent-state サイズが recall 項目数に比例」の下限。vision は ~10k token/画像 → 固定 O(1) 状態の recall は text より**難しい**。prior doc の「O(1)+recall は VLM に text より自然にマップ」楽観は**逆**(非 load-bearing だが要訂正)。mmMamba は native VLM 蒸留 / linear のみだと teacher 近接に hybrid 必要=「no softmax KV」志向と緊張。

---

## 7. ★矛盾・修正(honest disclosure)— full-text 検証が prior doc を矛盾・弱化させた箇所

重要度順:

1. **【最重要・verdict FLIP】N3**: 「非softmax + sparsity-prior 反復 read over linear-attention は unoccupied」を**反証**。機構は Resonator Network/VSA(1906.11684 ほか)が占有、Schlag(2102.11174)で「linear-attention state」限定詞は無意味。**未占有は application wrapper のみ = domain-transfer であって novel mechanism でない**。原因=原 finding が VSA/hyperdimensional/resonator line を未検索。
2. **【contradicts_prior_doc】P6**: 二重矛盾。(i) 「1-step 最適性が PoC-1 kill-risk」推論を一次資料は支持せず(task+memory mismatch で非転移)。(ii) prior の防御「softmax 専用だから線形に効かない」も**無効**(線形も同 1-step 最適 Prop 3.2)。kill-risk フレーミング自体が一次未裏付け。
3. **【contradicts_prior_doc】P2**: 「write 側飽和」を反証(+約9-10pt MK-NIAH、Qwen EDA 2606.26560 も裏付け)。write/erase は活発フロンティア。
4. **【contradicts_prior_doc】F1**: Qwen3.5-0.8B/2B は「comparable small dense softmax text」でなく multimodal + 18/24 層 Gated DeltaNet → like-for-like swap NO-GO。
5. **【claim 過大】N1**: 「read 側 test-time 最適化の先行なし」は過大(CCQ・Top-K Completion 2604.05438 が存在)。niche は「反復 × sparse-recovery × 真の凍結蒸留状態 × post-hoc」の union に縮小。
6. **【factual 修正】P4**: 蒸留 base 誤同定。Jet-Nemotron-2B は **Qwen2.5-1.5B** 上に構築(Qwen3-1.7B は比較ベースラインのみ)。訂正後の方が「llcore の Qwen2 0.5/1.5B と同 family/scale」記述が正確。
7. **【inaccuracy】P1**: CCQ「non-learned」は不正確(学習スカラゲート λ_t あり)。core operator は解析的だが「100% parameter-free」と誇張しない(ただし PoC-1 新規性は崩さない)。
8. **【quote 精度・gloss・メタ】P7**: 「destructive interference / capacity~d」は解釈 gloss。\"distillation budget\"(token なし)。v3=2026-01-28。
9. **【表現精緻化】P3**: FDM は big-O で O(1)(272 は N 非依存)。正確には「O(1) でない」でなく「**cache-free でない**」(272 実 token slot を線形状態の外に保持、recall はその cache 担当; 純 scan の MQAR=0.011 vs 0.966)。
10. **【非 load-bearing】S1**: bullet「O(1)+recall は VLM に text より自然」は recall 下限理論と逆向き(token 多い vision の方が固定状態 recall は難)。

---

## 8. 更新 next_plan 案(claude-projects.json 用)

> option-b deep-dive 検証完了(12 task, primary-source+adversarial)。**PoC-1 read 機構は非新規**(N3 flip: Resonator/VSA が codebook sparse-recovery 反復read を既占有; CCQ/MesaNet/CS-VLM も read 側に密集)→「first iterative read」主張禁止、honest framing=蒸留LLM凍結 linear-attn 状態への domain-transfer + P7 不可逆飽和を避け gated/delta 状態へ適用。P6 kill-risk は非転移(a-priori-dead 否定, ただし softmax-only 防御も無効)。**Write側は飽和せず**(P2 GDN-2/+Qwen EDA, contradicts prior)。**Base 乗換は Qwen3.5=multimodal+75%GatedDeltaNet で NO-GO → Qwen3-0.6B/1.7B**(Apache-2.0, 全層softmax)に変更。VLM(T6)は PARK→GPU+text PoC signal で shallow-prototype。**次: P5(STAR) 基盤の NAS-allele(evolve_linearization/nas_pareto)を機構新規性の本命候補として再評価 + read側 citing-graph 深掘り**。

---

## 9. ★N3 再検証 — re-flip(深掘り WF wdhj0hmdp, 6 probe + 2 一次 spot-check, 2026-06-29)

§7-1 の N3 flip(「PoC-1 read 機構は占有済み」)を、setting 軸で深掘り再検証した結果 **over-reach と判明 → down-grade(re-flip)**。

**★HINGE 結論**: VSA/Resonator/cleanup-memory ライン全体が **KNOWN・hand-designed・near-orthogonal な codebook 前提**で、recovery 保証は near-orthogonality に依存(VSA survey 2111.06077 一次確認)。**PoC-1 の「学習・非直交・designed-codebook 無しの蒸留状態」はこの前提外=VSA 理論がカバーしない regime**。学習・非直交辞書上の反復 sparse recovery は古典 dictionary-learning/LISTA 系(1808.10038/2106.00058)にしか無く、**蒸留 linear-attention LLM 状態への適用前例ゼロ**。flip が誤った理由 = 文献跨ぎ(Schlag=WRITE/構造の事実 → VSA cleanup=KNOWN codebook 上の READ、鎖は codebook で切れる)。

**補強**: fast-weight/linear-attn/TTT の READ は常に single inner-product(Schlag Eq.25「No iterative loops」/ 2501.12352 verbatim 確認)、iteration は全て WRITE 側。Borobia 2605.01192 が「学習非直交 superposition の nonlinear/iterative recovery は OPEN」と独立支持。

**一次 spot-check(`feedback_external_ai_verify` 履行)**:
- **CCQ 2606.01294 forward-citation = 0**(scholar-search 空配列確認)→ niche は文字通り未占有(~4 週・fast-moving ゆえ 2-3 ヶ月後再 crawl 推奨)。
- **Lexico 2412.08890**(Papailiopoulos ら)= **標準 softmax KV cache の OMP sparse 圧縮**で read も softmax →「linear-attn Σkvᵀ・no softmax」を外す = 非占有(partial)。最近接 killer 候補だが kill せず。

**最終 novelty 判定 = (b) mechanism_occupied_wrapper_open(narrow だが real, confidence MEDIUM)**。6 probe 独立収束。生き残る差別化軸 = ① 凍結(非更新)蒸留 linear-attn Σkvᵀ ② post-hoc decode-time ③ 学習・非直交・codebook 無し key を辞書 ④ 反復 K=3-5 ⑤ no softmax ⑥ 追加重学習 read-network 無し。

**フォーク含意(firm)**: **A(PoC-1 go-with-caveats)を支持・強化**(read 側 post-hoc wrapper が唯一残る open niche)/ **B(anticipatory write gate)は弱化**(write 側は delta-rule/MesaNet/OVQ/KalmaNet/FwPKM で過密)/ **C(NAS-allele)は直交・独立**。→ **推奨 = A**(§0 framing 規律 + CCQ 差別化を必須条件として付帯)。PoC-1 pre-registration = `llcore docs/research/preregistration/prereg_poc1_testtime_read_2026-06-29.md`(作成済)。

**honest 留保**: verdict は absence-in-targeted-search + 構造論証で、決定的 foreclosing 論文は無い。深掘り probe は abstract ベース(本パスで Lexico/CCQ-cite の 2 点のみ一次 spot-check)。多数の 2026 preprint ID はカットオフ後で probe 報告依存。
