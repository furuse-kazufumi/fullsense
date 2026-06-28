# Zhipu AI / GLM ブリーフィング (2026-06-29 時点)

> **provenance**: 検証ワークフロー `zhipu-ai-glm-landscape` (wwcbiu2si, 11 agents / 157 tool uses / 9.5 min)。
> 5 角度(lineup / architecture / license / benchmarks / VLM)を web 一次情報で調査 → 各 angle を敵対的 fact-check で反証 → 統合。
> 規律: 全 concrete claim に fetch 済 URL。confidence を angle ごとに正直併記。カットオフ 2026-01 以降の GLM は全て web 一次検証(記憶不使用)。
> **接続**: `interim_research_agenda_2026-06-28.md`(T2 線形化レシピ / T6 VLM)/ memory `feedback_qwen_commercial_barrier` / `project_llcore_efficient_arch_landscape_2026_06_26`。

対象: llcore 効率 LLM プロジェクト + FullSense「Qwen commercial barrier」検討。

---

## 1. 最新ラインナップ (TL;DR)

**最新フラッグシップ = GLM-5.2**(本日の13日前、有料コーディング顧客向け ~2026-06-13 → open weights / 公式リリースノート 2026-06-16)。これが「最近出た新しい Zhipu モデル」でほぼ確定。GLM-5.3 / GLM-6 は存在しない(HF org "Updated 6 days ago" が最新)。

| モデル | 公開 | 規模 | ctx | license | source |
|---|---|---|---|---|---|
| **GLM-5.2** ★最新 | 2026-06-16 | ~744B total / ~40B active MoE(HF widget 753B), `glm_moe_dsa`, 78層 | 1M (config: 1,048,576) | **MIT** | [HF](https://huggingface.co/zai-org/GLM-5.2) / [release notes](https://docs.z.ai/release-notes/new-released) / [config.json](https://huggingface.co/zai-org/GLM-5.2/raw/main/config.json) |
| GLM-5.1 | 2026-04-07 | ~754B MoE, ~8h 自律run | — | **MIT** | [release notes](https://docs.z.ai/release-notes/new-released) / [HF](https://huggingface.co/zai-org/GLM-5.1) |
| GLM-5 (base) | 2026-02-12 | 744B total / 40B active, 256 experts, 28.5T tokens | 200K | **MIT** | [HF](https://huggingface.co/zai-org/GLM-5) / [arXiv 2602.15763](https://arxiv.org/html/2602.15763v2) |
| GLM-5-Turbo / GLM-5V-Turbo | 2026-03-15 / 04-01 | turbo / native 多modal(GUI agent) | — | 5V-Turbo は **closed/API** 専用 | [release notes](https://docs.z.ai/release-notes/new-released) / [5V-Turbo](https://docs.z.ai/guides/vlm/glm-5v-turbo) |
| GLM-4.7 / 4.7-Flash | 2025-12-22 / 2026-01-19 | 358B MoE / **31B** | — | **MIT** | [HF GLM-4.7](https://huggingface.co/zai-org/GLM-4.7) |
| GLM-4.6 (前世代 coding flagship) | 2025-09-30 | 357B MoE, ~32B active | 200K | **MIT** | [HF](https://huggingface.co/zai-org/GLM-4.6) |
| GLM-4.5-Air | 2025-07-28 | 106B / 12B active MoE | — | **MIT** | [HF](https://huggingface.co/zai-org/GLM-4.5-Air) |
| GLM-4-9B-0414 | 2025-04-14 | **9B dense**(最小 MIT dense base) | — | **MIT** | [HF](https://huggingface.co/zai-org/GLM-4-9B-0414) |
| GLM-Edge 1.5B / 4B | 2024-11 | ~2B / 4B dense | — | ⚠️ **custom "glm-4"**(MIT でない) | [HF](https://huggingface.co/zai-org/GLM-Edge-1.5B-Chat) |
| 特化系: GLM-OCR ~1B / GLM-Image / GLM-ASR-Nano ~2B | 2026 各種 | small | — | 要確認 | [HF org](https://huggingface.co/zai-org) |

**要点**: フラッグシップは全部 700B+ MoE。小型 dense は GLM-4-9B(MIT)止まり、その下(GLM-Edge 1.5B/4B)は MIT でない。confidence = **high**。

---

## 2. アーキ / 効率 — constant-state / linear-attention への転用性

GLM は **sparse attention + low-rank KV + MTP** に賭ける系譜で、**Mamba/RWKV/GLA 系の linear/recurrent/constant-state とは別の学派**。GLM-4.5→5.2 全系譜に linear/SSM 要素は無い([arXiv 2602.15763](https://arxiv.org/html/2602.15763v2))。それでも llcore に**転用可能な3点**:

1. **DSA dense→sparse 変換レシピ(最も直接的)**: GLM-5 は dense checkpoint から `~1000-step warm-up + 20B-token sparse-adaptation` で DeepSeek Sparse Attention(lightning indexer が top-k KV を動的選択、long-seq で attention ~1.5-2x 削減)に変換([arXiv 2602.15763](https://arxiv.org/html/2602.15763v2))。これは **LoLCATs 型の linear-attention 蒸留(安価な継続事前学習で attention を差し替える)と構造的に同型** — llcore の retrofit 戦略の直接の先行例。
2. **MLA 低ランク KV 圧縮**: GLM-5 の production base attention は MLA(576次元 latent KV)。report は正直に「MLA-576 は GQA-8(2048次元 KV)に及ばない」と認めつつ `Muon Split` で詰めて出荷([arXiv 2602.15763](https://arxiv.org/html/2602.15763v2))。constant-state と**相補的**(状態圧縮の一手法)。
3. **IndexShare(top-k 選択コストの償却)**: GLM-5.2 が「4 sparse-attention 層ごとに同じ indexer を再利用し 1M ctx で per-token FLOPs を **2.9x 削減**」([README](https://huggingface.co/zai-org/GLM-5.2/raw/main/README.md))。「どの過去トークンが重要か」という、constant-state モデルが暗黙に解く問題を**明示的に**扱う設計 — 比較対象として有用。MTP speculative decoding は acceptance length +20%。

confidence = **high**(全 quote を一次 fetch + arXiv で確認)。

---

## 3. ★ライセンス判定 — GLM は Qwen より良い商用ベースか?

**結論: 大型 MoE teacher/base クラスでは YES、sub-2B 蒸留ターゲットでは NO。** `feedback_qwen_commercial_barrier` を「部分的に」しか解消しない。

**MIT が確認できたもの(LICENSE 実テキスト or card metadata + 独立報道で裏取り)**:
- GLM-4.5 / 4.5-Air: GitHub README が逐語で「released under the MIT open-source license and can be used commercially and for secondary development」([raw README](https://raw.githubusercontent.com/zai-org/GLM-4.5/main/README.md))。
- GLM-4.6(357B): HF API `license:mit`([HF](https://huggingface.co/zai-org/GLM-4.6))。
- GLM-5 / 5.1 / 5.2: card YAML `license: mit`、VentureBeat 等が独立に「MIT open-weights」確認。MAU 閾値・帰属名要求・用途 carve-out・PRC 管轄条項なし([GLM-5](https://huggingface.co/zai-org/GLM-5) / [GLM-5.2](https://huggingface.co/zai-org/GLM-5.2))。
- GLM-4-9B-0414(9B、最小 MIT dense): HF API `license:mit`([HF API](https://huggingface.co/api/models/zai-org/GLM-4-9B-0414))。

**⚠️ flag(LICENSE blob を開けなかった点・正直に)**: GLM-5 / GLM-5.2 / GLM-4.5 の `/raw/main/LICENSE` は **HTTP 404**(standalone LICENSE ファイルなし)。MIT 判定は card metadata + 報道由来であり、MIT 全文 blob は未読。商用採用前に live HF card で再確認推奨。

**restrictive な custom "glm-4" license(LICENSE 実読で確認)**:
- 旧 THUDM/glm-4-9b-chat(2024-06): 商用登録要求、「Built with glm-4」掲示 + 派生モデル名に `glm-4` prefix、軍事/違法用途禁止、北京海淀区裁判所管轄([raw LICENSE](https://huggingface.co/THUDM/glm-4-9b-chat/resolve/main/LICENSE))。
- **GLM-Edge 1.5B/4B(唯一の小型 dense GLM): HF API `license:other` / license_name "glm-4"** — **MIT ではない**([HF](https://huggingface.co/zai-org/GLM-Edge-1.5B-Chat))。lineup angle の「sub-2B dense は存在しない」は誤りだが、**存在する小型 dense は MIT でない**ので戦略結論は変わらない。

**Qwen 比較(HF API / LICENSE 実読)**:
- Qwen2-1.5B / Qwen3-0.6B = **apache-2.0**(clean)([Qwen2-1.5B](https://huggingface.co/Qwen/Qwen2-1.5B) / [Qwen3-0.6B](https://huggingface.co/Qwen/Qwen3-0.6B))。
- Qwen2.5-3B = `license:other`(非商用 "qwen-research")、Qwen2.5-72B = "qwen" license で**逐語**「product or service has more than 100 million monthly active users, you shall request a license from us」([Qwen2.5-72B LICENSE](https://huggingface.co/Qwen/Qwen2.5-72B/resolve/main/LICENSE))。

**判定表**:

| 用途 | GLM | Qwen | 勝者 |
|---|---|---|---|
| 大型 teacher / base(>9B) | MIT(MAU 閾値なし) | mixed(72B は qwen license + 100M MAU) | **GLM** |
| 小型蒸留ターゲット(0.5–1.5B) | MIT 級は**無い**(GLM-4-9B が最小 MIT; Edge は glm-4) | **Qwen2/3 0.5–1.5B = Apache-2.0** | **Qwen** |

confidence = **high**(MIT-blob 未読の caveat 付き)。

---

## 4. ベンチ / ポジショニング(vendor vs independent を明示)

**独立(信頼度高)**: Artificial Analysis Intelligence Index v4.1 で **GLM-5.2 = 51、open-weight #1**(MiniMax-M3 44 / DeepSeek V4 Pro 44 / Kimi K2.6 43 / Gemini 3.1 Pro Preview 46 を上回る、AA 自身が公表)([trendingtopics](https://www.trendingtopics.eu/glm-5-2-chinas-zhipu-ai-beats-even-googles-top-models-with-its-new-open-llm/))。価格 ~1/6(GLM-5.2 ~$1.40/$4.40 per M vs GPT-5.5 ~$5/$30、Opus ~$5/$25)は VentureBeat 見出しでも裏取り([VentureBeat](https://venturebeat.com/technology/z-ais-open-weights-glm-5-2-beats-gpt-5-5-on-multiple-long-horizon-coding-benchmarks-for-1-6th-the-cost))。

**vendor(Z.ai docs、独立検証なし)**: SWE-bench Pro 62.1、Terminal-Bench 2.1 (Terminus-2) 81.0、FrontierSWE で Opus 4.8 と「~1% 差」([docs.z.ai](https://docs.z.ai/guides/llm/glm-5.2))。

**正直な flag**: GLM-5.2 は**全勝ではない**。CNBC は「closing in … not yet overtaking」([CNBC](https://www.cnbc.com/2026/06/26/china-zhipu-z-ai-open-source-anthropic-openai.html))。「Claude Opus 4.8 が SWE-bench Pro ~69 で GLM-5.2 62.1 を上回る」の **~69 は一次ソース未確認**(aggregator 由来、approximate 扱い)。

**採用シグナル**: 中国 open モデルが OpenRouter token の ~60-61% に到達(2025初 <2% から)、GLM は top-5 常連([dataconomy](https://dataconomy.com/2026/02/25/chinese-ai-models-hit-61-market-share-on-openrouter/))。

**企業/地政学リスク(load-bearing)**: Zhipu は HKEX 上場(2026-01-08、code 2513.HK、~US$7B、初の LLM 企業上場)([CNBC IPO](https://www.cnbc.com/2026/01/08/china-ai-tiger-goes-ipo-zhipu-hong-kong-debut-openai-knowledge-atlas-hsi-hang-seng-listing.html))。一方 **Beijing Zhipu Huazhang は米 Entity List(2025-01 追加)** — 米国向け商用プロダクトのベースにする場合の供給網/輸出規制リスク([theairankings](https://theairankings.com/zhipu/))。

confidence = **medium-high**(独立指標 high、cross-model の細かい delta は directional)。

---

## 5. VLM (GLM-V) — llcore T6 VLM scope への関連

**最新 open-weights VLM = GLM-4.6V(2025-12-08)**、~108B `glm4v_moe` MoE + **9B Flash**、128K ctx、MIT、**native multimodal tool-calling**(画像/スクショ/ドキュメントを tool パラメータとして直接渡す)([HF](https://huggingface.co/zai-org/GLM-4.6V) / [MarkTechPost](https://www.marktechpost.com/2025/12/09/zhipu-ai-releases-glm-4-6v-a-128k-context-vision-language-model-with-native-tool-calling/))。

**戦略スプリットが明確**: text base は open(MIT)だが、**最新 vision head は monetization-gated**。GLM-5V-Turbo(2026-04-01、Design2Code 94.8)は **closed/API 専用**、GLM-5.2(June flagship)は **text-only**(3つの独立 aggregator が image 入力非対応を確認 — marketing blog の "multimodal" 表現は text 推論を指す)([5V-Turbo docs](https://docs.z.ai/guides/vlm/glm-5v-turbo))。

**llcore に直接関連する小型 MIT VLM base**:
- **GLM-4.6V-Flash 9B**(MIT、128K、tool-calling)
- **GLM-4.1V-9B-Thinking**(2025-07、MIT、AIMv2-Huge ViT + MLP + GLM-4-9B-0414、10B 級で 23/28 bench 首位、Qwen2.5-VL-72B を 18 task で上回ると主張・vendor)([GLM-V GitHub](https://github.com/zai-org/GLM-V))

→ **Qwen-VL の cleaner-license 代替**として T6 で有力(ただし MIT は card metadata 由来、weight LICENSE blob は 404 で未読)。

**効率-VLM の転用ネタ**: ① 3D-conv temporal 2x downsampling で video token 削減、2D/3D-RoPE で任意解像度([arXiv 2507.01006](https://arxiv.org/abs/2507.01006))。② **Glyph framework(arXiv 2510.17800)= 長文を画像レンダリングして VLM に食わせ 3-4x token 圧縮**、128K-ctx VLM で ~1M-token text task を処理。constant-state 文脈圧縮の異分野アイデアとして注目([arXiv 2510.17800](https://arxiv.org/abs/2510.17800))。

confidence = **high**(GLM-5.2 text-only という crux を独立 3 ソースで裏取り済)。

---

## 6. llcore / FullSense への含意と推奨

GPU 到着待ちの interim-research 期間(律速 = ノート CPU)を前提に:

**(a) 効率アイデアの研究対象として: YES(中優先)。**
GLM は constant-state とは別学派だが、**DSA の dense→sparse retrofit レシピ(~1000-step warmup + 20B tokens)は llcore の LoLCATs 型 linear-attention 蒸留と同型の先行事例**で、retrofit の安価さ・収束の実証データとして読む価値がある([arXiv 2602.15763](https://arxiv.org/html/2602.15763v2))。IndexShare の「indexer 共有で選択コスト償却」と Glyph の視覚 token 圧縮は cross-domain ネタ。**CPU で重い実験は不要、arXiv 精読のみで取り込める** → interim 期間に適合。

**(b) 代替蒸留 base として: NO(現状)。**
llcore が要る 0.5–1.5B dense ターゲットに **MIT GLM は存在しない**(最小 MIT dense = GLM-4-9B、その下 GLM-Edge は glm-4 license)。一方 **Qwen2/Qwen3 0.5–1.5B は既に Apache-2.0** でクリーン。蒸留 base を GLM に乗り換える licensing 上の動機は**この size では無い**。GLM は **teacher(large MoE, MIT)**としてなら Qwen より優位だが、CPU 完結の llcore では 700B teacher を回せない。

**(c) FullSense「Qwen commercial barrier」への回答: 部分的。**
Qwen barrier が問題になるのは主に**大型 base の商用配布**。そこは GLM-MIT が綺麗に解消する。**小型蒸留ターゲットの barrier は Qwen Apache-2.0 で既に無い**ため、GLM 採用の追加便益は限定的。barrier 文脈で GLM を「答え」と framing するなら **size 限定の注釈必須**。

**推奨(1行)**: GLM は **(a) 効率レシピの研究素材として interim 期間に arXiv 精読で取り込む**(特に DSA retrofit と Glyph)。**蒸留 base は Qwen2/3 small(Apache-2.0)を維持**。large-teacher が必要になった/GPU 到着後に GLM-MIT を teacher 候補として再評価。VLM(T6)では **GLM-4.1V-9B-Thinking / GLM-4.6V-Flash 9B(MIT)を Qwen-VL 代替候補としてバックログ登録**。

---

## 7. 未確認・要追跡

- **MIT LICENSE blob 未読**: GLM-5 / 5.2 / 4.5 / 4.6V の `/raw/main/LICENSE` が全て **HTTP 404**。MIT は card metadata + 報道由来。**商用採用の意思決定前に live HF card で license フィールドを直接確認**(load-bearing)。
- **GLM-5 / 5.2 active-expert top-k**: GLM-5.2 config は 256 routed + 1 shared、8 experts/token を確認([config.json](https://huggingface.co/zai-org/GLM-5.2/raw/main/config.json))。GLM-5 の router top-k は逐語未確認(40B active は確定)。
- **GLM-5 param 744 vs 754B**: card「744B total / 40B active」が正、HF widget 754B は MTP/embedding 込みの rounding(解決済)。
- **Opus 4.8 の SWE-bench Pro ~69**: 一次ソース無し、aggregator 由来。head-to-head delta は directional 扱い。
- **Ascend/MindSpore 訓練説**(GLM-5 を NVIDIA なしで訓練): SCMP/blog 由来、HF card / arXiv 未確認 → **未検証扱い**([SCMP](https://www.scmp.com/tech/article/3343239))。
- **GLM-5.2 専用 technical report**: 未発見(IndexShare/1M は HF README のみ、arXiv は GLM-5 base の 2602.15763)。
- **GLM-4.6V active params / Flash 9B が dense か small-MoE か**: 未文書化。
- **GLM-5.2 deployment ctx**: spec は 1M だが Together AI は実効 256K と表示 — 1M は model-spec であり全 provider 保証ではない([Together](https://www.together.ai/models/glm-52))。
- **SEO-spam 注意**: glm5.ai / glm-5.org / glm5.net 等のベンチ数値・「aligns with Claude Opus 4.6」は一次確認なしに信用しない(本ブリーフィングでは未使用)。
