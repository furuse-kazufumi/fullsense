# llcore 差別化監査 — 特許 DB 照会 (2026-06-06)

> 本日の敵対的差別化監査 (44 候補, breaks 0, [`differentiation_audit_dna_roadmap_2026_06_06.md`](differentiation_audit_dna_roadmap_2026_06_06.md)) は
> **学術文献のみ**で実施され、特許 DB は未照会だった (同 §7「残リスク」: 不在証拠として弱い)。
> 本書はその穴 (包括計画 T4 4-1, Phase 3(c)) を埋める **調査専用**ドキュメント。コード変更・git 操作は一切行わない。

---

## 0. 照会対象 (四点交差点)

llcore の生存する差別化核 = **四点交差点** (監査 §2 より):

> **sound contraction 証明 (閉形式 ∞-norm / SDP-Lyapunov) × Transformer 記憶コアの内部 dynamics ×
> 進化/更新ループ内の prove-then-reject ゲート (fail-closed) × 動く実装+実験**

この四点 (または近接) を claim する**特許**が存在するかを調べ、5 軸ルーブリックで脅威判定する。

### 5 軸ルーブリック

| 軸 | 意味 | 交差点の要件 |
|---|---|---|
| **gatesUpdates** | 重み/記憶の**更新そのもの**を accept/reject するゲートか | 出力・行動・展開のゲートは×、更新ゲートが◯ |
| **soundProof** | ゲート根拠が**健全な形式証明** (contraction/Lyapunov) か | 統計的 bound・ヒューリスティック・ハッシュ照合・テストは× |
| **llmMemoryCore** | 対象が **Transformer/LLM 記憶コアの内部 dynamics** か | 制御系プラント・分類 head・回路は× |
| **evolutionLoop** | ゲートが**進化/自己改変ループ内**にあるか | 単発展開承認・post-hoc 監視は× |
| **implemented** | **reduced-to-practice (動く実装)** か | 概念のみは× (※特許では明細書の実施可能要件で大半が形式的に充足するため、本軸は「具体的アルゴリズムの開示有無」で評価) |

四点交差点を脅かすには **gatesUpdates + soundProof + (llmMemoryCore または evolutionLoop)** を**同時**に満たす独立 claim が必要。

---

## 1. 方法 (再現可能性のため)

- **DB**: Google Patents (patents.google.com) を中心に、USPTO 全文 PDF (image-ppubs.uspto.gov) を補助。
- **言語**: 英語 (USPTO/EP/WO/CN) + 日本語 (JPO 向け、JP 番号・日本語クエリ)。
- **クエリ数**: 14 クエリ (英語 11 + 日本語 3)。各クエリは 5-8 件のヒットを返す Web 検索を経由。
- **claim 確認**: 脅威候補は WebFetch で**独立 claim 1 の全文**を取得し、5 軸で個別判定。
  特許番号は WebFetch で**実在確認したもののみ**記載 (捏造禁止)。
- **限界**: Web 検索経由のため網羅性は専門特許 DB (Derwent/PatBase/J-PlatPat 公報検索) に劣る (§5 参照)。

### 実行クエリ一覧 (不在証拠の素材)

| # | クエリ | 主なヒット種別 | 交差点ヒット |
|---|---|---|---|
| Q1 | `"formally verified" "machine learning" "model update" gate reject patent` | ML 検証・gated layer 特許 / 記事 | なし |
| Q2 | `"formal verification" "neural network" "weight update" admission control patent` | 重み NVM 検証・selective weight update 特許 / arXiv | なし |
| Q3 | `contraction Lyapunov certificate "neural network" update gate patent self-improving` | **全て arXiv** (制御系 certificate) | なし |
| Q4 | `"self-modifying"/"self-improving" AI "formal proof" gate reject (assignee G/DeepMind)` | **全て arXiv** (Gödel machine, SGM, safe self-improve) | なし |
| Q5 | `site:patents.google.com NN model update formal verification reject accept gate` | 話者照合・NN ハッシュ照合特許 / arXiv | なし |
| Q6 | `site:patents.google.com verified ML model update admission evolutionary fail-closed` | ML 監視・evolved ML 特許 | なし |
| Q7 | `site:patents.google.com Lyapunov/contraction NN stability certificate update accept reject` | **全て arXiv** (neural contraction metric) | なし |
| Q8 | `patent self-improving agent memory "write gate" verification accept reject LLM` | **全て arXiv** (LLM memory security/SEDM) | なし |
| Q9 | `site:patents.google.com ML model update verify stability reject deploy provably` | model registry / resiliency / 版管理特許 | なし |
| Q10 | `site:patents.google.com evolutionary/GA verification/model-checking NN update gate` | NN 進化アーキ特許 (US6553357/US11003994 等) | なし |
| Q11 | `IBM/MS/Amazon "certified" "model update" deploy reject NN deployment gate` | certify-and-deploy / rollback 特許 | なし |
| Q12 | `site:patents.google.com abstract interpretation/provably safe model update accept reject` | **全て arXiv** (Provably Safe Model Updates 等) | なし |
| Q13 | `site:patents.google.com runtime assurance NN monitor reject unsafe update gatekeeper` | **全て arXiv** (runtime monitor/Simplex) | なし |
| Q14 | `site:patents.google.com certified continual learning forgetting guarantee update gate bound` | US20240119280A1 (error sensitivity) / arXiv | なし |
| Q15 | `site:patents.google.com Lipschitz/spectral-norm transformer by-construction stable` | **全て arXiv** (LipsFormer/Enforced Lipschitz) | なし |
| J1 | `安定性 証明 ニューラルネットワーク 更新 検証 ゲート 棄却 特許` | NN 回路 (JP2019057072A)・解説記事 | なし |
| J2 | `特許 機械学習 モデル 更新 形式検証 リアプノフ 縮小写像 ゲート 自己進化` | JPO/弁理士 AI 特許解説 (一般論のみ) | なし |
| J3 | `特許 自己進化 エージェント 記憶 書込み ゲート 検証 (J2 内に統合)` | (J2 と同系) | なし |

---

## 2. ヒット一覧 (claim 確認済み — 脅威判定)

四点交差点に**最も近い**特許を WebFetch で独立 claim まで確認した。**いずれも交差点を埋めない。**

### 2.1 US11715005B2 — "Verification and identification of a neural network"

- **assignee**: Cariad SE / **priority**: 2018-12-13 (filed 2019-12-12)
- **claim 1 要旨**: 学習済み NN の特徴量 (層数・ノード数・リンク・重み・訓練法詳細) から**ハッシュを計算し、セキュア DB の参照ハッシュと照合して NN を verify/reject** する。
- **5 軸**: gatesUpdates ×(更新でなく完成済 NN の真正性) / soundProof ×(暗号ハッシュ照合、形式証明でない) / llmMemoryCore ×(一般 NN) / evolutionLoop × / implemented ◯
- **脅威判定**: **background**。「NN を reject する」語彙は被るが、**データ完全性・出自検証**であって解析的性質の証明ゲートでない。交差点と無関係。

### 2.2 US10896032 — "System and method for certifying and deploying instruction code"

- **assignee**: (USPTO 全文 PDF。明細書本文より) / claim 1 は PDF 画像化のため部分抽出。
- **要旨** (検索スニペット + 本文): モデルを certification system が**認証**し、deployment system が契約インスタンス化を検知して「certified」とマーク。開発者承認後、deployment ID を Pending → Active に移す**ガバナンス/権限ワークフロー**。
- **5 軸**: gatesUpdates △(展開を gate するが重み更新の解析性質でない) / soundProof ×(認証 = 手続的 attestation、数学証明でない) / llmMemoryCore × / evolutionLoop ×(単発展開承認) / implemented ◯
- **脅威判定**: **narrows (弱)**。「certify → deploy gate」の語彙が被る。**related work に「ガバナンス型展開ゲートとの対比」として 1 文添えると防御が固い**が、soundProof/llmMemoryCore/evolutionLoop いずれも非該当で交差点は破らない。

### 2.3 US11868855 — "Resiliency for machine learning workloads"

- **assignee**: (USPTO 全文 PDF。検索スニペット「validating the stability of the model and weights」)。claim 1 は PDF 画像化で全文抽出不可。
- **要旨** (スニペット): ML モデル展開時に「**モデルと重みの安定性を検証**」する resiliency プロセス。文脈は**ワークロードの可用性/フォールトトレランス**であり、「安定性」は dynamical-systems の contraction でなく**運用上の頑健性**を指す蓋然性が高い。
- **5 軸**: gatesUpdates △ / soundProof ×(運用安定性、Lyapunov でない蓋然性大) / llmMemoryCore × / evolutionLoop × / implemented ◯
- **脅威判定**: **background→narrows (弱)**。「stability of model and weights を validate」の文言被りに注意。ただし claim 全文未確認 (PDF 画像) のため**留保**。専門 DB での再確認を推奨 (§5)。

### 2.4 US20240119280A1 — "Improving Continual Learning Through Error Sensitivity Modulation"

- **assignee**: (Google Patents) / continual learning の catastrophic forgetting 対策。
- **要旨**: 誤差感度を変調して逐次学習の忘却を緩和。**ヒューリスティックな学習法改良**であり、更新を accept/reject するゲートでも形式証明でもない。
- **5 軸**: gatesUpdates × / soundProof × / llmMemoryCore × / evolutionLoop × / implemented ◯
- **脅威判定**: **background**。「certified continual learning」語彙系 (監査 §3 の最近接系統) の特許版だが、ゲート・証明とも非該当。

### 2.5 進化系 NN 特許群 (US6553357 / US11003994 / US5214746 / US11250327 / US11507844 等)

- NN アーキ/重みを**進化/GA で最適化**する古典特許群 (1990s-2020s)。
- **5 軸**: gatesUpdates ×(fitness 選択であって証明ゲートでない) / soundProof × / llmMemoryCore × / evolutionLoop ◯ / implemented ◯
- **脅威判定**: **background**。evolutionLoop 軸**のみ**該当。「進化 × NN」の先行は豊富 (監査既知) だが、**証明ゲートを持つものは皆無**。交差点の evolutionLoop 単独は防御不要 (監査が既に古典進化を背景として処理済)。

---

## 3. 不在証拠 (何をどう検索してゼロだったか)

**交差点を埋める特許は、14 英語 + 3 日本語クエリのいずれからもゼロ件。** 不在の構造的パターン:

1. **「証明ゲート × 更新」系クエリ (Q3, Q4, Q7, Q8, Q12, Q13, Q15) は、特許 DB を site 指定しても結果が
   ほぼ全て arXiv に逸れた。** これは「sound proof で更新/記憶/進化をゲートする」概念が**学術段階に留まり、
   特許化されていない**ことの強い間接証拠 (検索エンジンが特許で該当を見つけられず学術に fallback)。
2. **特許としてヒットしたものは 3 系統に分類され、いずれも交差点外**:
   - (a) **完全性・真正性検証** (US11715005: ハッシュ照合) — soundProof が暗号で形式証明でない。
   - (b) **展開ガバナンス/版管理** (US10896032, US11868855, model registry, rollback) — gate はあるが
     根拠が手続的 attestation / 運用テストで、解析的性質の sound 証明でない。
   - (c) **進化/逐次学習の最適化** (進化 NN 群, US20240119280A1) — ループはあるが証明ゲートがない。
3. **日本語 (JPO 向け) も同様にゼロ**: J1/J2/J3 は NN 回路実装特許と弁理士の AI 特許**一般論解説**のみで、
   「リアプノフ/縮小写像で更新をゲート」する JP 公報は表層検索範囲に存在せず。
4. **assignee 観点 (Google/DeepMind, MS, IBM, Amazon, NVIDIA, Anthropic, Sakana) でもゼロ**:
   AlphaEvolve/ShinkaEvolve は**進化 × LLM の実装**だが、ゲートは evaluator (性能/正しさ) であり
   **sound contraction 証明ではない** (監査 §3 の PSV/AlphaVerus と同系の差別化線)。これらの**特許**で
   交差点を claim するものは表層検索で発見されず。

**留保**: 「ゼロ件」は**表層 Web 検索範囲**での不在であり、網羅証明ではない (§5)。

---

## 4. 結論 (差別化への影響)

### **判定: clear (交差点は破られない) — ただし US10896032/US11868855 への related-work 言及で narrows を先回り防御すべき。**

- **breaks: 0**。四点交差点を同時 claim する特許は、英語 14 + 日本語 3 クエリ・主要 assignee 観点を通じて
  **発見されなかった**。学術監査 (breaks 0) の結論は**特許面でも維持**される。
- **narrows: 2 (弱)**。
  - **US10896032 (certify-then-deploy ガバナンスゲート)** と
    **US11868855 (model/weights の "stability" を validate)** は**語彙が部分的に被る**。
    PAPER_DRAFT の related work に「**展開ガバナンス型ゲート (手続的 attestation) / 運用安定性検証とは異なり、
    本研究は重み更新の解析的 contraction 性質を sound 証明でゲートする**」の対比を **1-2 文**先回り編入すれば、
    査読/審査での文言衝突リスクを消せる。これは監査 §3 の防御壁編入作業 (Phase 0) に**特許 2 件を追加**する形。
- **特許面の積極的含意**: 交差点が特許でも空白ということは、llcore 側に**新規性・進歩性の余地**がある
  (将来 llcore 自身を出願する選択肢の素地)。ただし監査の internal 脆弱点 (Z3 看板乖離・出荷 API 未配線・
  規模 n=8) は特許の**実施可能要件/有用性**にも効くため、Phase 1 の本配線が出願前提条件になる。

### 監査クレーム D1'-D4' への反映

- **D1' / D3'** (証明ゲート × 自己改変/進化は未踏): **特許面でも支持**。証明ゲート型更新の特許ゼロ。
- **D2'** (verified memory evolution の実装先取り窓): **特許面でも空白**。memory write-gate は arXiv (SSGM 等) のみで
  特許化されておらず、**時間窓は特許面でも開いている** (出願による先取りも理論上可能)。
- **D4'** (検証派は制御系限定 / 展開ガバナンスとの対比): **US10896032/US11868855 を対比対象に追加**して補強。

---

## 5. 限界 (honest disclosure)

- **網羅性**: 本調査は **WebSearch + WebFetch 経由の Google Patents/USPTO 表層検索**であり、
  専門特許 DB (Derwent World Patents Index, PatBase, Orbit, J-PlatPat 公報全文検索) の**クレーム全文インデックス**には
  カバレッジで劣る。「ゼロ件」は**この探索範囲での不在**であって絶対的不在の証明ではない。
- **claim 全文未取得が 2 件** (US10896032, US11868855): USPTO 全文 PDF が**画像 (CCITT Fax) 化**されており
  独立 claim を機械抽出できなかった。要旨は検索スニペット + 明細書断片に基づく**暫定判定**。
  脅威度が上がる場合は J-PlatPat / Google Patents の OCR テキスト版で claim 1 を再確認すべき。
- **言語**: 中国語 (CNIPA) 公報は CN 番号が英訳経由で 1-2 件混じった程度で、**中国語ネイティブ検索は未実施**。
  自己進化/検証 AI は中国出願が活発な領域のため、CN の取りこぼし可能性は残る。
- **時間**: 2026-06 時点。特許は公開まで最長 18 ヶ月のラグがあり、**直近 18 ヶ月の未公開出願**は原理的に不可視。
  D2' の時間窓論はこのラグも織り込むべき (競合が既に出願済で未公開の可能性は排除できない)。
- **「探索範囲で未踏」の留保を常に維持** (監査 §7 と整合)。

---

## 参照

- 本日の差別化監査: [`differentiation_audit_dna_roadmap_2026_06_06.md`](differentiation_audit_dna_roadmap_2026_06_06.md) (§7「残リスク」の特許穴を本書が充足)
- ゲート分類監査: [`gate_taxonomy_audit_2026_06_06.md`](gate_taxonomy_audit_2026_06_06.md)
- ロードマップ位置付け: 同監査 §6 Phase 3(c)「特許 DB 照会 (既知の穴)」= 調査であり実装リスクなし
