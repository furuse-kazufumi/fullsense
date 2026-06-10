---
layout: default
title: "画像認識25年パラダイムシフト + FullSense接続 (内部メモ)"
parent: "Research"
published: false
---

# 画像認識25年のパラダイムシフト — FullSense 戦略接続メモ (内部研究メモ)

> **内部研究メモ。** 本メモは外部講演を視聴した上での自分の接続分析であり、原講演の著作権は藤吉弘亘氏に帰属する。外部発信時は事実関係のみとし、講演スライドの文言・図表・系譜構成は再現しない。
>
> 背景: CV パラダイムに関する 2026 年の講演(藤吉弘亘氏)を視聴し、FullSense (特に llcore / llive / 予測符号化テーマ) への接続を抽出した。以下の本文は自分の言葉による要約・分析。

## CV パラダイム進化の一般的事実 — ★llcore/llive の進化テーゼと同型

コンピュータビジョンは、技術的事実として、人手で設計・付与する部分を減らし、機械が自らデータから構造を獲得する方向へ進んできた。ハンドクラフト特徴(SIFT/HOG 等)から始まり、深層学習(CNN)による特徴表現の自動獲得、ViT と自己教師あり学習によるラベル依存の低減、Web スケールの画像-言語ペアで学習する基盤モデル(MLLM)による世界知識・オープン語彙の獲得、そして世界モデル × VLA による予測・行動の統合へと段階的に発展してきた、というのが広く共有された理解である。

大きな転換点として、(1) 深層学習による表現の自動獲得、(2) 基盤モデルによる世界知識の取り込み、(3) 世界モデル × VLA による認識から予測・行動への拡張、が挙げられる。方向性として **Perception → Prediction → Action が一つの基盤上で閉ループ化していく** 流れがある。2026 年の講演でも同趣旨が示された(藤吉弘亘氏)。

## ★FullSense への接続 (本メモの主眼)

### 1. llcore verified-plasticity への最強フック
技術的事実として、世界モデル系の手法は不確実性定量化・因果制御・行動検証と組合せることで安全設計に寄与しうるが、それ自体は形式的な保証(guarantee)を与えるものではない。これは技術コミュニティで広く共有された観察である。
→ **llcore の核は『保証(GUARANTEE)』**: sound certificate で「進化/学習が ρ<1 で発散しない」を判別する。
すなわち「世界モデル系の手法は一般に安全性に寄与するが形式的保証は与えない」のに対し、「llcore verified-plasticity は sound certificate で(small-n per-component 域で)保証を出す」という、
**記事の決定的対比軸**になる。普及メタ記事「ラングトンの蟻の幻」に『世界モデル系の手法でも形式的保証は出せない。
verified-plasticity は出す』の1節を足せる。

### 2. 予測符号化テーマの裏付け (World Model = 予測→反省→行動)
世界モデルと VLA を統合する近年の研究(Uni-World VLA / DriveWorld-VLA / VLA-World / LeWM 等)は、FullSense の「表現×リアルタイム」ideation 統合発見
=**予測符号化アーキテクチャ**([[project_fullsense_expression_realtime_marathon]])の学術的裏付けになる。
特に **「潜在空間で予測するからリアルタイム実行可能(ピクセル生成を回避)」(DriveWorld-VLA / LeWM)** は
llmesh の near-real-time push / llrepr typed diff-stream の設計原理(重い完全生成でなく差分/潜在)と同型。

### 3. Supervision Deficit → 密な自己教師 (llive 自己進化への示唆)
VLA の弱点 = 行動ラベルが疎(Supervision Deficit)。世界モデルの未来予測を**密な自己教師信号**にして
スケーリングを増幅。第3世代(MAE/DINO)の「ラベル不要化」の行動版再演。
→ llive 自己進化メモリの fitness 設計(合成 proxy 脱却)に、「予測誤差=密な自己信号」という発想を移植可能。

### 4. 産業センシング含意 (llmesh の差別化補強)
「固定クラス分類器 → 予測して行動する基盤」= 検査/計測へ直結。オープン語彙検出(YOLO-World)・
VLM 世界知識 = 「学習していない欠陥」対応、世界モデル = 「異常予兆検知(surprise検出)」。
→ llmesh 産業 IoT (MQTT/OPC-UA) + SPC の差別化(competitor scan で確認した FullSense 独自軸 a)を
学術トレンド側から補強する。SPC の管理限界外れ = surprise 検出と接続できる。

## 世代別 SOTA 早見 (原著付き)
- ① SIFT/HOG+SVM/BoVW(Viola-Jones, Dalal-Triggs, Csurka)
- ② AlexNet→VGG→GoogLeNet→ResNet→EfficientNet→ABN(藤吉研) / Faster R-CNN→YOLO→Mask R-CNN
- ③ Transformer(Vaswani 2017)→ViT(Dosovitskiy ICLR2021)→DINO/DINOv3/MAE。ViTは「形状」を見る(Tuli CogSci2021)=ノイズ頑健(SegFormer)
- ④ CLIP(Radford ICML2021, 4億ペア対照学習)→LLaVA(connector+2段学習)→Gemini / EMMA(Waymo, 世界知識で未学習物体対応)
- ④.5 VLA: RT-2(CoT推論+action token離散化) / Open X-Embodiment(22ロボ100万episode) / GR00T N1
- ⑤ World Models(Ha-Schmidhuber 2018)→Dreamer→Uni-World VLA / DriveWorld-VLA / VLA-World / **LeWM**(LeCunら, JEPA, ~15M param, 最大48倍高速plan)

## アクション候補 (llcore 記事執筆時に反映)
- [ ] 普及メタ記事に「世界モデルの安全=保証でない vs verified-plasticity=保証」対比節を追加
- [ ] 予測符号化テーマ doc に LeWM/DriveWorld-VLA の「潜在予測でリアルタイム」を裏付け引用として追記
- [ ] llmesh 差別化(産業センシング)に「SPC管理限界=surprise検出」の世界モデル接続を1行
