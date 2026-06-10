---
layout: default
title: "画像認識25年パラダイムシフト (藤吉 2026) + FullSense接続"
parent: "Research"
---

# 画像認識25年のパラダイムシフト (藤吉弘亘 2026) — FullSense 戦略接続メモ

> 元資料: 藤吉弘亘(中部大学 理工学部 AIロボティクス学科 / MPRG 主宰)
> 「画像認識25年のパラダイムシフト: 深層学習からマルチモーダル、そして世界モデルへ」全52p, 2026-06。
> ユーザーが 2026-06-10 出張直前に共有。本メモは FullSense (特に llcore / llive / 予測符号化テーマ) への接続を抽出。

## 講演の核 (p.52) — ★llcore/llive の進化テーゼと同型

> **進化の本質 = 「何を人が与え、何を機械が自ら獲得するか」の境界が広がり続けたこと**

| 世代 | 時期 | 人が与える | 機械が獲得する |
|---|---|---|---|
| ① ハンドクラフト特徴 | 〜2011 | 特徴設計+正解ラベル | 識別境界のみ |
| ② CNN(深層学習) | 2012〜 | 正解ラベル | 特徴表現を自動獲得 |
| ③ ViT+自己教師あり | 2021〜 | 大量の未ラベル画像 | 関係性・大域形状(ラベル不要に) |
| ④ MLLM 基盤モデル | 2021〜 | Webスケール画像-言語ペア | 言語・世界知識・オープン語彙 |
| ⑤ 世界モデル × VLA | 2025〜 | 観測と行動の系列 | 時間・因果・行動(予測して動く) |

3転換点: ① Deep Learning(表現自動獲得) ② Foundation Model(World Knowledge) ③ World Model×VLA(認識→予測・行動)。
結論: **Perception → Prediction → Action が一基盤上で閉ループ**。

## ★FullSense への接続 (本メモの主眼)

### 1. llcore verified-plasticity への最強フック (p.51)
世界モデルの「未来予測でできること」5項目の第5: **「安全設計に寄与する(ただし保証ではない)」**
— 不確実性定量化・因果制御・行動検証と組合せて効く、と藤吉氏は honest に限定している。
→ **llcore の核は『保証(GUARANTEE)』**: sound certificate で「進化/学習が ρ<1 で発散しない」を判別する。
世界モデル/VLA 系の「安全に寄与するが保証なし」と、llcore verified-plasticity の「sound cert で保証」は
**記事の決定的対比軸**。普及メタ記事「ラングトンの蟻の幻」に『世界モデルですら保証は出せない。
verified-plasticity は出す』の1節を足せる。

### 2. 予測符号化テーマの裏付け (World Model = 予測→反省→行動)
p.47-50 の3統合アーキ(Uni-World VLA インターリーブ / DriveWorld-VLA 潜在統合 / VLA-World 生成→反省)+
LeWM(JEPA型・潜在予測で軽量) は、FullSense の「表現×リアルタイム」ideation 統合発見
=**予測符号化アーキテクチャ**([[project_fullsense_expression_realtime_marathon]])の学術的裏付け。
特に **「潜在空間で予測するからリアルタイム実行可能(ピクセル生成を回避)」(DriveWorld-VLA/LeWM)** は
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
