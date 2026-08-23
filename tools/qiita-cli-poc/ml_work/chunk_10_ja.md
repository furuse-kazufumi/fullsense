#### domain(2 op)

| op | 説明 |
|---|---|
| `it_crop_domain` | domain op(HALCON: crop_domain) |
| `it_full_domain` | domain op(HALCON: -) |

#### matching(2 op)

| op | 説明 |
|---|---|
| `ncc_locate` | matching op(HALCON: find_ncc_model) |
| `shape_locate` | matching op(HALCON: find_shape_model) |

#### noise(2 op)

| op | 説明 |
|---|---|
| `add_noise_distribution` | noise op(HALCON: add_noise_distribution) |
| `add_noise_white` | noise op(HALCON: add_noise_white) |

#### Legacy(1 op)

| op | 説明 |
|---|---|
| `distance_funct_1d` | 2 関数間の距離(max=上限, mean=平均、distance_funct_1d)。 |

#### barcode(1 op)

| op | 説明 |
|---|---|
| `decode_barcode` | barcode op(HALCON: find_bar_code) |

#### classification(1 op)

| op | 説明 |
|---|---|
| `classify_shape` | classification op(HALCON: -) |

#### filter(1 op)

| op | 説明 |
|---|---|
| `Bilateral` | エッジ保存平滑化(cv2.bilateralFilter、不在時 numpy 実装)(filter.Bilateral)。  [backend=opencv] |

#### filtering(1 op)

| op | 説明 |
|---|---|
| `tf_gradient_domain_reintegrate` | filtering op(HALCON: -) |

#### intensity-transform(1 op)

| op | 説明 |
|---|---|
| `xmh_soft` | intensity-transform op(HALCON: -) |

#### misc(1 op)

| op | 説明 |
|---|---|
| `identity` | misc op(HALCON: copy_image) |

#### morphology/markers(1 op)

| op | 説明 |
|---|---|
| `xmh_regmin` | morphology/markers op(HALCON: -) |

#### region-morphology(1 op)

| op | 説明 |
|---|---|
| `xmh_majority` | region-morphology op(HALCON: -) |

#### region-transform(1 op)

| op | 説明 |
|---|---|
| `xmh_bwperim` | region-transform op(HALCON: -) |

#### self-similarity(1 op)

| op | 説明 |
|---|---|
| `xmh_selfmatch` | self-similarity op(HALCON: -) |

#### texture-feature(1 op)

| op | 説明 |
|---|---|
| `xmh_pftas` | texture-feature op(HALCON: -) |

#### texture/shape-feature(1 op)

| op | 説明 |
|---|---|
| `xmh_zernike` | texture/shape-feature op(HALCON: -) |

## 付録 G: 未来資料集 — センシング・宇宙・学会・競技会(URL 実在確認済み)

第 13 章の資料編です。URL はすべて執筆時点でアクセスを確認したものだけを載せています(確認できなかったものは載せていません)。リンク切れの際はサイト名で検索してください。

### A. センシングの最先端

#### A-1. イベントカメラ / ニューロモルフィック視覚

**何が凄いか(3 行)**
- 人間の網膜のように「変化した画素だけ」を非同期に送るカメラ。時間分解能はマイクロ秒オーダー、ダイナミックレンジは約 140 dB(通常カメラは約 60 dB)で、モーションブラーがほぼ無い([Gallego et al. survey](https://arxiv.org/abs/1904.08405) より)。
- ドローンレースで世界チャンピオンに勝った自律ドローン(UZH/ETH の Scaramuzza 研)や、NASA 火星ヘリのビジョン系アルゴリズムにも研究成果が波及。
- Sony とスタートアップ Prophesee の協業で 4.86 µm 画素の積層型イベントセンサ(IMX636/637)が量産化され、「研究室の変わり種」から「買える部品」になった。

| 項目 | 内容 | URL |
|---|---|---|
| 代表論文 | Gallego et al., "Event-based Vision: A Survey", IEEE TPAMI 44(1), 2022(arXiv 2019) | https://arxiv.org/abs/1904.08405 |
| 代表特許 | US10498977B2 "Event-based vision sensor"(Samsung, 2019 発行) | https://patents.google.com/patent/US10498977B2/en |
| 製品一次情報 | Sony 積層型イベントセンサ IMX636/IMX637 プレスリリース(2021) | https://www.sony-semicon.com/en/news/2021/2021090901.html |
| 製品一次情報 | Prophesee × Sony IMX636 / 評価キット EVK4 | https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/ / https://www.prophesee.ai/event-camera-evk4/ |
| 研究室 | Robotics and Perception Group(UZH & ETH Zurich、Davide Scaramuzza 教授) | https://rpg.ifi.uzh.ch/ (本人ページ: https://rpg.ifi.uzh.ch/people_scaramuzza.html ) |
| 研究室 GitHub | uzh-rpg(ESIM ほか多数公開) | https://github.com/uzh-rpg |
| 公開データセット | UZH-FPV ドローンレース データセット(イベント+IMU+レーザ真値) | https://fpv.ifi.uzh.ch/ |
| シミュレータ | ESIM: an Open Event Camera Simulator(CoRL 2018) | https://github.com/uzh-rpg/rpg_esim |
| シミュレータ | v2e: 通常動画→リアルな DVS イベント変換(CVPRW 2021 Best Paper) | https://github.com/SensorsINI/v2e (解説: https://sites.google.com/view/video2events/home ) |
| 動画 | UZH RPG 公式 YouTube(自律ドローン・イベントカメラのデモ多数) | https://www.youtube.com/user/ailabRPG |

#### A-2. 量子センシング(NV センター磁気計測・量子慣性航法)

**何が凄いか(3 行)**
- ダイヤモンド中の原子欠陥(NV センター)1 個が「量子コンパス」になり、常温で細胞スケールの磁場まで測れる。量子センシングの標準教科書級レビューが [Degen–Reinhard–Cappellaro (Rev. Mod. Phys. 2017)](https://dspace.mit.edu/bitstream/handle/1721.1/124553/RevModPhys.89.035002.pdf)。
- 冷却原子を「波」として干渉させる原子干渉計は、GPS が使えない場所でも位置を失わない慣性航法の本命。米軍のスペースプレーン X-37B の第 8 飛行で量子慣性センサの軌道上試験が計画された([The Conversation, 2025](https://theconversation.com/quantum-alternative-to-gps-navigation-will-be-tested-on-us-military-spaceplane-262967))。
- MIT は NV センターと CMOS チップの統合(オンチップ量子センサ)を実証し、「量子センサを普通の半導体部品にする」流れが進行中([MIT News, 2019](https://news.mit.edu/2019/quantum-sensing-chip-0925))。

| 項目 | 内容 | URL |
|---|---|---|
| 代表論文 | Degen, Reinhard, Cappellaro, "Quantum sensing", Rev. Mod. Phys. 89, 035002 (2017) | https://dspace.mit.edu/bitstream/handle/1721.1/124553/RevModPhys.89.035002.pdf (DOI: 10.1103/RevModPhys.89.035002) |
| 代表レビュー | BEC を使う量子慣性航法の展望(Applied Physics Reviews, 2025) | https://pubs.aip.org/aip/apr/article/12/3/031306/3351228/Developments-for-quantum-inertial-navigation |
| 代表特許 | US12424810B1 "Compact atom interferometry inertial navigation sensors with tailored diffractive optics"(Sandia, 2025) | https://patents.google.com/patent/US12424810B1/en |
| 代表特許 | US7317184B2 "Kinematic sensors employing atom interferometer phases"(2008) | https://patents.google.com/patent/US7317184B2/en |
| 研究機関 | Sandia National Laboratories – Atom Interferometry | https://www.sandia.gov/quantum/atom-interferometry/ |
| 研究機関 | QuTech(TU Delft + TNO。NV センターで量子ネットワークの世界初実証群) | https://qutech.nl/ |
| 研究室(国内) | 東京科学大(旧東工大)岩崎研 – 固体量子センサ | http://dia.pe.titech.ac.jp/en/solid-quantum-sensors/ |
| 解説記事 | MIT Technology Review「量子航法は GPS 妨害問題を解けるか」(2025-12) | https://www.technologyreview.com/2025/12/16/1129887/quantum-navigation-militarys-gps-jamming-problem/ |
| 自宅入口 | QuTiP: 開量子系ダイナミクスの OSS シミュレータ(Python) | https://qutip.org/ |

#### A-3. ハイパースペクトル・偏光イメージング

**何が凄いか(3 行)**
- 全画素に「分光スペクトル」が付いた画像(ハイパーキューブ)を撮る技術。人間の目には同じ色でも、材質・水分・鮮度・病変が「スペクトルの指紋」で見分けられる。
- 農業(作物ストレス・雑草判別)、食品検査、がん検出・術中イメージング、鉱物探査、リサイクル選別まで応用が拡大中([Heliyon 2024 レビュー](https://www.sciencedirect.com/science/article/pii/S2405844024092399))。
- 医療分野では偏光×ハイパースペクトルの融合(PHSI)、ハイパースペクトル内視鏡、AR 統合などが最前線([2025 医療 HSI レビュー](https://pmc.ncbi.nlm.nih.gov/articles/PMC13003176/))。

| 項目 | 内容 | URL |
|---|---|---|
| 代表レビュー | "Hyperspectral imaging and its applications: A review", Heliyon (2024) | https://www.sciencedirect.com/science/article/pii/S2405844024092399 |
| 代表レビュー | "Modern Trends and Recent Applications of Hyperspectral Imaging: A Review", Technologies (2025) | https://www.mdpi.com/2227-7080/13/5/170 |
| 医療レビュー | Medical hyperspectral imaging: updated review(偏光 HSI・内視鏡・AR 統合) | https://pmc.ncbi.nlm.nih.gov/articles/PMC13003176/ |

#### A-4. 触覚スキン・電子皮膚

**何が凄いか(3 行)**
- MIT の GelSight は「カメラでゲルの変形を見る」だけで人間の指先を超える空間分解能の触覚を実現。今は GelSight 社として製品化され、ロボットの指先にもなっている([MIT News](https://news.mit.edu/2017/gelsight-robots-sense-touch-0605))。
- スタンフォード Bao 研の電子皮膚は、伸びる・自己修復する・圧力と剪断力を区別する、を材料化学から作り込む。義手に「触覚」を返すことがゴール。
- 触覚は視覚の「最後のワンマイル」。掴む瞬間の滑り・硬さ・摩擦はカメラでは見えず、Physical AI の次の主戦場になっている。

| 項目 | 内容 | URL |
|---|---|---|
| 代表論文 | Yuan, Dong, Adelson, "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force", Sensors 17(12):2762 (2017) | https://www.mdpi.com/1424-8220/17/12/2762 |
| 代表特許 | WO2023081342A1 "Four-dimensional tactile sensing system, device, and method"(2023) | https://patents.google.com/patent/WO2023081342A1/en |
| 研究室 | MIT CSAIL(Adelson 研系)GelSight Wedge プロジェクト | https://gelsight.csail.mit.edu/wedge/ |
| 研究室 | Stanford Bao Group(電子皮膚・伸縮エレクトロニクス) | https://baogroup.stanford.edu/ |
| 企業 | GelSight, Inc.(GelSight Mini 等) | https://www.gelsight.com/gelsightmini/ |
| 解説 | MIT News "Giving robots a sense of touch" (2017) | https://news.mit.edu/2017/gelsight-robots-sense-touch-0605 |

#### A-5. 神経インターフェース的センシング(筋電 / EIT)— 軽く

**何が凄いか(3 行)**
- Meta(旧 CTRL-labs)のリストバンドは手首の表面筋電(sEMG)だけで、個人ごとの較正なしに指の微細な動きをデコード。空中の手書き文字を毎分約 20.9 語で入力できる(Nature 2025 掲載)。
- 「脳に電極を刺さない」非侵襲ニューロモータ・インターフェースが、キーボード・マウスの次の標準入力を狙う位置まで来た。
- 電気インピーダンス断層撮影(EIT)を腕輪化する研究もあり、低コスト・低消費電力(約 50 mW)でジェスチャ認識精度 93% の報告がある([Biosensors 2026](https://www.mdpi.com/2079-6374/16/4/200))。

| 項目 | 内容 | URL |
|---|---|---|
| 代表論文 | "A generic non-invasive neuromotor interface for human-computer interaction", Nature 645 (2025) | https://www.nature.com/articles/s41586-025-09255-w |
| 一次情報 | Meta EMG Wristband 公式ページ | https://www.meta.com/emerging-tech/emg-wearable-technology/ |
| 関連論文 | EIT ベースのロバストなジェスチャ認識(Biosensors, 2026) | https://www.mdpi.com/2079-6374/16/4/200 |

---

### B. 宇宙開発

#### B-1. 軌道上サービシング・デブリ捕獲

**何が凄いか(3 行)**
- Astroscale の ADRAS-J(JAXA CRD2 フェーズ I)は、2024 年に「協力機能を一切持たない」約 3 トンのロケット上段へ 15 m まで自律接近し、周回観測に成功。世界初級の実績([Astroscale 公式](https://www.astroscale.com/en/news/astroscales-adras-j-achieves-historic-15-meter-approach-to-space-debris))。
- 続く ADRAS-J2(CRD2 フェーズ II)はロボットアームで同デブリを実際に捕獲・軌道降下させる計画。ESA × ClearSpace の ClearSpace-1 も 4 本アームでの捕獲実証を準備中。
- 「タンブリングする非協力物体に安全に近づいて掴む」= 自由浮遊物体のランデブー&キャプチャは、GNC(誘導・航法・制御)・視覚・接触力学の総合格闘技。まさにシミュレーションが主戦場。

| 項目 | 内容 | URL |
|---|---|---|
| 公式ミッション | Astroscale ADRAS-J ミッションページ | https://www.astroscale.com/en/missions/adras-j |
| 公式プログラム | JAXA CRD2(商業デブリ除去実証) | https://www.kenkai.jaxa.jp/eng/crd2/index.html |
| 一次情報 | JAXA プレス: ADRAS-J のデブリ周回観測画像(2024-07) | https://global.jaxa.jp/press/2024/07/20240730-1_e.html |
| 特許(解説) | Astroscale 特許 US12,479,603 B2「タンブリング物体の捕獲方法」公式解説 | https://www.astroscale.com/en/news/astroscale-patent-advances-docking-and-servicing-of-tumbling-satellites |
| 製品 | Astroscale ドッキングプレート(磁気捕獲用「衛星の牽引フック」) | https://www.astroscale.com/en/docking-plate |
| 解説記事 | MIT Technology Review: 世界初のデブリ除去ミッション開始(2024) | https://www.technologyreview.com/2024/02/27/1089065/first-mission-dead-rocket/ |
| 動画付き記事 | ADRAS-J のフライアラウンド映像(Space.com) | https://www.space.com/astroscale-debris-removal-adras-j-video |

※ ClearSpace 社公式サイトは URL 未確認のため掲載せず(ClearSpace-1 の概況は上記 Space.com / MIT Tech Review 記事内で言及)。

#### B-2. 月面ロボティクス

**何が凄いか(3 行)**
- JAXA × トヨタの有人与圧ローバ「LUNAR CRUISER」は水素燃料電池で走る「月面のキャンピングカー」。ミニバス 2 台分のサイズで宇宙服なしで乗れる([トヨタ公式](https://global.toyota/en/mobility/technology/lunarcruiser/))。
- NASA JPL の CADRE は、スーツケース大のローバ 3 台が自分たちで「リーダー」を選び、役割分担して月面を 3D マッピングする自律協調実証。地球からは「この領域を探査せよ」と目標だけ与える([JPL 公式](https://www.jpl.nasa.gov/missions/cadre/))。
- 一方で NASA の水氷探査ローバ VIPER は 2024 年に計画中止(投入済み約 4.5 億ドル)。最先端は「全部成功する物語」ではないことも正直に伝えたい。

| 項目 | 内容 | URL |
|---|---|---|
| 公式 | トヨタ LUNAR CRUISER 公式ページ | https://global.toyota/en/mobility/technology/lunarcruiser/ |
| 公式 | NASA JPL CADRE ミッションページ | https://www.jpl.nasa.gov/missions/cadre/ |
| 一次情報 | NASA: CADRE ローバ、月への旅支度完了(IM-3 で 2026 年到着予定) | https://www.nasa.gov/missions/tech-demonstration/cadre/nasas-mini-rover-team-is-packed-for-lunar-journey/ |
| 企業 | ispace(HAKUTO-R プログラム) | https://www.ispace-inc.com/aboutus |
| 報道 | VIPER 計画中止の経緯(Spaceflight Now, 2024) | https://spaceflightnow.com/2024/07/18/nasa-cancels-half-billion-dollar-water-ice-seeking-moon-rover/ |
| 国内 | 東北大が月面インフラ大型プロジェクトを主導(2026) | https://www.tohoku.ac.jp/en/news/university_news/selected_to_lead_landmark_lunar_infrastructure_project.html |

#### B-3. 軌道上製造・宇宙建築

**何が凄いか(3 行)**
- Varda Space は無重力でしか作れない「より完全な結晶」を狙い、抗ウイルス薬 Ritonavir の結晶を軌道上で製造してカプセルで持ち帰ることに成功(2024 年 W-1 ミッション)。既にカプセル飛行 6 回目まで進行。
- 微小重力は対流も沈降もないため、タンパク質結晶・医薬品・特殊光ファイバの製造環境として本命視され、Redwire は宇宙製薬の専門子会社 SpaceMD を設立([CNBC, 2026](https://www.cnbc.com/2026/06/09/space-race-pharma-spacex-varda-redwire-drug-development-orbit.html))。
- 「工場を打ち上げて製品だけマッハ 25 で持ち帰る」という産業構造そのものが新しい。再突入カプセルの空力・熱防御もシミュレーションの塊。

| 項目 | 内容 | URL |
|---|---|---|
| 公式 | Varda W-Series プラットフォーム(軌道上製造+再突入) | https://www.varda.com/platform |
| 公式 | Redwire(宇宙インフラ+宇宙製薬 SpaceMD) | https://rdw.com/ |
| 報道 | Varda カプセル、宇宙製造薬を積んで帰還(Space.com, 2024) | https://www.space.com/varda-in-space-manufacturing-capsule-landing-success |
| 報道 | 製薬が LEO に向かう理由(CNBC, 2026-06) | https://www.cnbc.com/2026/06/09/space-race-pharma-spacex-varda-redwire-drug-development-orbit.html |

#### B-4. 宇宙用シミュレータ OSS(全部無料で自宅 PC に入る)

| ツール | 何ができるか | URL |
|---|---|---|
| NASA GMAT | ミッション設計・軌道設計の本格派(NASA 実務でも使用)。GUI+スクリプト | https://sourceforge.net/projects/gmat/ |
| Basilisk | 宇宙機の姿勢・軌道・フライトソフトまでモジュール式に統合シミュレーション(コロラド大 AVS Lab) | https://avslab.github.io/basilisk/ |
| 42 (NASA GSFC) | 複数宇宙機の姿勢・軌道力学。ランデブー・編隊飛行の研究にも | https://github.com/ericstoneking/42 |
| poliastro | Python で軌道力学。教育・プロトタイピングの入口に最適 | https://github.com/poliastro/poliastro |
| Kerbal Space Program | ゲームだが軌道力学の直感を作る教育定番(教育版 KerbalEdu も存在) | https://www.kerbalspaceprogram.com/ |

#### B-5. 回転翼で惑星を飛ぶ — Ingenuity の遺産と Dragonfly

**何が凄いか(3 行)**
- 火星ヘリ Ingenuity は「大気密度が地球の 1% の空で飛べるか」という実験機だったのに、想定 5 回のところ 72 回飛行して 2024 年に退役([JPL 公式](https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/))。費用 8,500 万ドルの技術実証が惑星探査の形を変えた。
- 後継の Dragonfly は土星の月タイタンへ送る原子力駆動の 8 ローター機(車サイズ)。2028 年 7 月打上げ予定で、生命の化学的起源を空から探す([JHUAPL 公式](https://dragonfly.jhuapl.edu/))。
- 「飛ぶ場所の空気・重力が地球と違う」ため、設計の主役は徹底したシミュレーションと地上試験。回転翼空力は自宅の CFD(流れを計算機で解く数値流体力学)/物理エンジンでも入口に立てる。

| 項目 | 内容 | URL |
|---|---|---|
| 公式 | Dragonfly ミッション(JHU APL) | https://dragonfly.jhuapl.edu/ (別館: https://www.jhuapl.edu/destinations/missions/dragonfly ) |
| 公式ギャラリー | Dragonfly Gallery(想像図・試験映像) | https://dragonfly.jhuapl.edu/Gallery/ |
| 公式 | NASA Ingenuity ミッションページ | https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/ |
| 一次情報 | JPL: Ingenuity ミッション終了発表(72 飛行) | https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ |

---

### C. シミュレーションで最先端を「自宅再現」できる例

「億円級の実験装置がなくても、物理法則はダウンロードできる」がこの章のメッセージ。全て無料 OSS。

| 最先端テーマ | 自宅 PC + OSS での入口 | URL |
|---|---|---|
| イベントカメラ | 手持ちの動画を **v2e** でイベントストリームに変換して「網膜の見る世界」を体験。本格派は **ESIM** で 3D シーンからイベント生成 | https://github.com/SensorsINI/v2e / https://github.com/uzh-rpg/rpg_esim |
| デブリ捕獲・自由浮遊物体 | **MuJoCo** で重力ゼロ+アーム付き衛星の MJCF を書き、タンブリングする物体の捕獲を物理シミュレーション(公式ロボットモデル集 Menagerie が出発点) | https://github.com/google-deepmind/mujoco / https://github.com/google-deepmind/mujoco_menagerie |
| 軌道計画・ミッション設計 | **GMAT** で地球-月遷移軌道を組む、**poliastro**(Python)でホーマン遷移を数十行で計算 | https://sourceforge.net/projects/gmat/ / https://github.com/poliastro/poliastro |
| 宇宙機の姿勢制御 | **Basilisk** または **42** でリアクションホイール制御・編隊飛行をシミュレーション | https://avslab.github.io/basilisk/ / https://github.com/ericstoneking/42 |
| 月面ローバ・歩行ロボットの RL | **Gymnasium** + **MuJoCo Playground**(GPU 加速)で強化学習。低重力は XML の gravity 1 行で月になる | https://github.com/Farama-Foundation/Gymnasium / https://github.com/google-deepmind/mujoco_playground |
| 量子センシング | **QuTiP** でスピンの Rabi 振動・Ramsey 干渉(NV センター計測の原理そのもの)を数値実験 | https://qutip.org/ |
| 軌道力学の直感 | **Kerbal Space Program** で「重力ターン」「遷移軌道」を体で覚える(教育枠) | https://www.kerbalspaceprogram.com/ |

---

### D. 見て刺激をもらうための資料

#### D-1. 見て刺激になる公式ギャラリー・動画

| ソース | 内容 | URL |
|---|---|---|
| NASA Image and Video Library | 14 万点超の画像・動画・音声を横断検索 | https://images.nasa.gov/ |
| NASA Galleries | ミッション別ギャラリー入口 | https://www.nasa.gov/gallery/ |
| JAXA デジタルアーカイブス | JAXA の写真・映像アーカイブ(利用条件ページ含む) | https://jda.jaxa.jp/en/service.php |
| ESA Images | ESA 公式画像ギャラリー | https://www.esa.int/ESA_Multimedia/Images |
| UZH Robotics and Perception Group | イベントカメラ・自律ドローンレースのデモ動画 | https://www.youtube.com/user/ailabRPG |
| Boston Dynamics | Atlas / Spot 公式チャンネル | https://www.youtube.com/@BostonDynamics |
| Unitree Robotics | G1 / Go2 等の公式デモ | https://www.youtube.com/@unitreerobotics/videos |
| Dragonfly Gallery | タイタン探査機の想像図・試験映像 | https://dragonfly.jhuapl.edu/Gallery/ |

#### D-2. この分野に強い大学・研究機関(実在確認済みの研究室 URL)

| 大学・機関 | 研究室 / 部門 | 分野 | URL |
|---|---|---|---|
| Univ. of Zurich & ETH Zurich | Robotics and Perception Group(Scaramuzza) | イベントカメラ・自律ドローン | https://rpg.ifi.uzh.ch/ |
| MIT | CSAIL GelSight プロジェクト(Adelson 系) | 視覚ベース触覚 | https://gelsight.csail.mit.edu/wedge/ |
| Stanford | Bao Group | 電子皮膚・伸縮エレクトロニクス | https://baogroup.stanford.edu/ |
| Stanford | Interactive Perception and Robot Learning Lab | ロボット操作・知覚 | https://iprl.stanford.edu/ |
| CMU | Robotics Institute(1979 年設立、世界最大級) | ロボティクス全般 | https://www.ri.cmu.edu/ |
| TUM | MIRMI(Munich Institute of Robotics and Machine Intelligence) | ロボティクス・機械知能(70+ 教授) | https://www.mirmi.tum.de/en/mirmi/home/ |
| TU Delft | QuTech(+ TNO) | 量子コンピュータ・量子インターネット・NV センター | https://qutech.nl/ |
| Sandia National Labs | Atom Interferometry グループ | 量子慣性航法 | https://www.sandia.gov/quantum/atom-interferometry/ |
| 東北大学 | Space Robotics Lab(吉田研。ETS-VII、HAKUTO 技術リーダー) | 宇宙ロボット・月面探査 | https://astro2.mech.tohoku.ac.jp/en/ |
| 東京大学 | Intelligent Space Systems Laboratory(航空宇宙) | 宇宙機 GNC・自律化 | https://www.space.t.u-tokyo.ac.jp/ |
| 東京大学 | JSK Robotics Laboratory | ヒューマノイド・知能ロボット | http://www.jsk.t.u-tokyo.ac.jp/information.html |
| 東京科学大(旧東工大) | 岩崎研(固体量子センサ) | NV センター量子センシング | http://dia.pe.titech.ac.jp/en/solid-quantum-sensors/ |
| JHU APL | Dragonfly ミッションチーム(PI: Elizabeth Turtle) | 惑星回転翼探査 | https://dragonfly.jhuapl.edu/ |
| NASA JPL | CADRE(自律協調ローバ) | 月面マルチロボット | https://www.jpl.nasa.gov/missions/cadre/ |

---

### E. 関連学会・展示会・競技会 — 「見に行ける / 出られる」導線

#### E-1. 学会(研究の最前線を「読む・聴く」)

| 学会 | 紹介(1〜2 行) | 開催時期の目安 | URL |
|---|---|---|---|
| ICRA | IEEE RAS 旗艦のロボティクス最大級会議。2026 年はウィーン(6/1–5)、2027 年は 5 月下旬 | 毎年 5〜6 月 | https://www.ieee-ras.org/conferences-workshops/fully-sponsored/icra/ (2026: https://2026.ieee-icra.org/ ) |
| IROS | IEEE/RSJ 共催のもう一つの最大級会議(1988 年〜)。2026 年はピッツバーグ | 毎年 10 月前後 | https://www.ieee-ras.org/conferences-workshops/financially-co-sponsored/iros/ (2026: https://2026.ieee-iros.org/ ) |
| RSS | 少数精鋭・口頭発表中心の「品質重視」会議。2026 年はシドニー(7/13–17) | 毎年 7 月前後 | https://roboticsconference.org/ |
| CoRL | ロボット学習(RL・模倣・基盤モデル)専門の若い会議(2017 年〜)。2026 年は 11/9–12 | 毎年 11 月前後 | https://www.corl.org/ |
| Humanoids | IEEE-RAS ヒューマノイド専門会議(2000 年〜)。第 25 回は 2026-12 シリコンバレー | 毎年 11〜12 月 | https://2026.ieee-humanoids.org/ |
| NeurIPS(関連 WS) | ML 最高峰会議。Robot Learning 系ワークショップが毎年併設(例: World Models × ロボット学習 WS @ NeurIPS 2026) | 毎年 12 月 | https://neurips.cc/ (WS 例: https://robowm-ws.github.io/ ) |
| ICLR(関連 WS) | 表現学習の最高峰会議。ロボティクス×基盤モデル系 WS の受け皿 | 毎年 4〜5 月 | https://iclr.cc/ |

#### E-2. 展示会(実機を「見に行く」— 学生でも入場しやすい)

| 展示会 | 紹介(1〜2 行) | 開催時期の目安 | URL |
|---|---|---|---|
| 国際ロボット展 iREX(東京) | 1974 年から続く世界最大級のロボット展。2025 年は東京ビッグサイトで 12/3–6 開催、次回は 2027 年 12 月 | 隔年 12 月(奇数年) | https://irex.nikkan.co.jp/ |
| World Robot Conference(北京) | 中国最大級のロボット会議+展示+競技の複合イベント。ヒューマノイド新製品の初出し場に | 毎年 8 月頃 | https://www.worldrobotconference.com/ |
| CES(ラスベガス) | 世界最大級のテック見本市。近年はヒューマノイド・Physical AI の主要な発表舞台 | 毎年 1 月 | https://www.ces.tech/ |
| automatica(ミュンヘン) | スマート自動化・産業用ロボットの世界的見本市。次回 2027 年 6/22–25 | 隔年 6 月 | https://automatica-munich.com/en/ |
| CEATEC(幕張) | 日本最大級の IT・エレクトロニクス展。2026 年は 10/13–16 幕張メッセ。学生入場の敷居が低い | 毎年 10 月 | https://www.ceatec.com/en/ |

#### E-3. 競技会(「出られる」— 個人・学生チームの入口)

| 競技会 | 紹介(1〜2 行) | 開催時期の目安 | URL |
|---|---|---|---|
| **ROBO-ONE(日本)** ★重点 | 2002 年から続く二足歩行ロボットの格闘競技。**個人が自作ヒューマノイドで出場できる**日本発の文化で、市販機で出られる初心者向け「ROBO-ONE Light」もある。本記事の「個人でやるロボット運動会」の実世界版として最も相性が良い | 年 2 回程度(春・秋) | https://www.robo-one.com/ (解説: https://www.robo-one.com/abouts/view/aboutroboone/ ) |
| RoboCup | 「2050 年にワールドカップ優勝チームにロボットで勝つ」を掲げる国際競技会。サッカーの他にレスキュー・家庭・産業リーグ、中高生向けの RoboCupJunior もある | 毎年 7 月前後(世界大会) | https://www.robocup.org/ |
| World Humanoid Robot Games(北京) | 2025 年 8 月に鳥の巣で初開催。16 か国 280 チーム・500 体超のヒューマノイドが 26 種目で競技(100 m 走優勝タイムは 21.50 秒)。第 2 回は 2026 年 8 月 | 毎年 8 月 | https://english.beijing.gov.cn/whatson/events/sports/202505/t20250509_4085816.html (概要: https://en.wikipedia.org/wiki/World_Humanoid_Robot_Games ) |
| DARPA Robotics Challenge(歴史) | 2012–2015 年のヒューマノイド災害対応競技。当時のロボットは転倒続出だったが、現在のヒューマノイドブームの原点。「10 年でここまで来た」を語る素材 | 終了(アーカイブ) | https://www.darpa.mil/research/programs/darpa-robotics-challenge |
| DARPA Triage Challenge(現行) | DARPA 現行チャレンジの例。大量負傷者トリアージをセンシング+自律システムで革新する競技(2025 年に決勝) | プログラム進行中 | https://triagechallenge.darpa.mil/ |

> 導線メモ: 「観る」なら CEATEC・iREX(国内・低コスト)→「出る」なら ROBO-ONE Light(市販機可)→ RoboCupJunior(中高生)→ 大学で RoboCup/学会、の階段が描ける。

---

### 記事に使える「事実+出典」メモ(誇張防止用)

| 事実 | 出典 |
|---|---|
| イベントカメラの時間分解能はマイクロ秒台、ダイナミックレンジ約 140 dB(フレームカメラ約 60 dB) | https://arxiv.org/abs/1904.08405 |
| Sony IMX636/637 は業界最小(発表当時)の 4.86 µm イベント画素・1280×720 | https://www.sony-semicon.com/en/news/2021/2021090901.html |
| Meta の sEMG バンドは較正なしの汎用デコード、空中手書き 20.9 語/分(Nature 645, 2025) | https://www.nature.com/articles/s41586-025-09255-w |
| ADRAS-J は非協力デブリ(全長約 11 m・約 3 トン)へ 15 m まで自律接近(2024) | https://www.astroscale.com/en/news/astroscales-adras-j-achieves-historic-15-meter-approach-to-space-debris |
| Ingenuity は 3 年で 72 回飛行、2024-01 にミッション終了。技術実証としての費用は約 8,500 万ドル | https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ / https://www.space.com/space-exploration/missions/nasa-begins-building-nuclear-powered-dragonfly-drone-for-2028-launch-to-saturn-moon-titan |
| Dragonfly はミッション総額約 33.5 億ドル、2028-07 打上げ予定(Falcon Heavy)、CDR 通過済み | https://www.space.com/space-exploration/missions/nasa-begins-building-nuclear-powered-dragonfly-drone-for-2028-launch-to-saturn-moon-titan |
| Varda W-1 は Ritonavir 結晶を軌道上製造し 2024-02 に地上回収(民間初級) | https://www.space.com/varda-in-space-manufacturing-capsule-landing-success |
| NASA VIPER は 2024-07 に中止決定(投入済み約 4.5 億ドル、中止による節約は約 8,400 万ドル) | https://spaceflightnow.com/2024/07/18/nasa-cancels-half-billion-dollar-water-ice-seeking-moon-rover/ |
| CADRE は 3 台の自律ローバが IM-3 ランダーで Reiner Gamma へ(2026 予定) | https://www.jpl.nasa.gov/missions/cadre/ / https://www.nasa.gov/missions/tech-demonstration/cadre/nasas-mini-rover-team-is-packed-for-lunar-journey/ |
| X-37B 第 8 飛行で量子慣性センサ(原子干渉計)の軌道上試験を計画(2025) | https://theconversation.com/quantum-alternative-to-gps-navigation-will-be-tested-on-us-military-spaceplane-262967 |

---

## 付録 H: 学習ログ実測抄 — 13 世代の成長曲線を数字のまま

各世代の学習ログから、eval 行(約 5.2M ステップごと)の主要値を抜粋した生データ表です(いずれも MuJoCo シミュレーション内の実測値)。グラフより粗いですが、「どの世代が、いつ、どう伸びた/詰まったか」を原典で確認できます(reward は世代間で報酬設計が違うため**縦の比較はできません**。同一世代内の推移だけを見てください)。ep_len は生存ステップ(×0.02 秒)、fwd_v は前進速度 m/s、crash は衝突率です。

### walk10(26M まで・eval 6 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 194 | 31 | 1.09 | — |
| 5M | 258 | 42 | 0.93 | — |
| 10M | 338 | 57 | 0.83 | — |
| 16M | 469 | 81 | 0.80 | — |
| 21M | 691 | 126 | 0.72 | — |
| 26M | 1861 | 371 | 0.71 | — |

### walk11(31M まで・eval 7 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.09 | — |
| 5M | 265 | 43 | 0.95 | — |
| 10M | 354 | 58 | 0.85 | — |
| 16M | 471 | 78 | 0.78 | — |
| 21M | 685 | 118 | 0.67 | — |
| 26M | 1673 | 316 | 0.67 | — |
| 31M | 3331 | 667 | 0.83 | — |

### walk12(52M まで・eval 11 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.09 | — |
| 5M | 260 | 42 | 0.95 | — |
| 10M | 327 | 54 | 0.84 | — |
| 16M | 479 | 80 | 0.77 | — |
| 21M | 687 | 118 | 0.70 | — |
| 26M | 1256 | 223 | 0.73 | — |
| 31M | 1536 | 277 | 0.72 | — |
| 37M | 1791 | 320 | 0.76 | — |
| 42M | 1701 | 305 | 0.80 | — |
| 47M | 1945 | 344 | 0.81 | — |
| 52M | 1996 | 355 | 0.80 | — |

### walk12b(58M まで・eval 12 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.09 | 0.00 |
| 5M | 255 | 41 | 0.93 | 0.00 |
| 10M | 332 | 54 | 0.84 | 0.00 |
| 16M | 463 | 77 | 0.76 | 0.00 |
| 21M | 700 | 119 | 0.67 | 0.00 |
| 26M | 1525 | 274 | 0.76 | 0.00 |
| 31M | 1909 | 350 | 0.83 | 0.00 |
| 37M | 2124 | 391 | 0.88 | 0.00 |
| 42M | 2322 | 426 | 0.85 | 0.00 |
| 47M | 2181 | 400 | 0.84 | 0.00 |
| 52M | 2489 | 458 | 0.79 | 0.00 |
| 58M | 2328 | 428 | 0.79 | 0.00 |

### walk12c(68M まで・eval 14 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.08 | 0.00 |
| 5M | 258 | 42 | 0.95 | 0.00 |
| 10M | 359 | 59 | 0.89 | 0.00 |
| 16M | 552 | 92 | 0.74 | 0.00 |
| 21M | 957 | 161 | 0.76 | 0.00 |
| 26M | 2057 | 343 | 0.85 | 0.00 |
| 31M | 4520 | 725 | 0.91 | 0.00 |
| 37M | 5725 | 882 | 1.09 | 0.00 |
| 42M | 6522 | 975 | 1.19 | 0.00 |
| 47M | 6828 | 989 | 1.29 | 0.00 |
| 52M | 7043 | 999 | 1.35 | 0.00 |
| 58M | 7148 | 992 | 1.40 | 0.00 |
| 63M | 7313 | 1000 | 1.41 | 0.00 |
| 68M | 7410 | 1000 | 1.43 | 0.00 |

### walk13(131M まで・eval 26 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 197 | 31 | 1.07 | 0.01 |
| 10M | 286 | 46 | 0.93 | 0.01 |
| 21M | 504 | 84 | 0.78 | 0.14 |
| 31M | 834 | 142 | 0.67 | 0.27 |
| 42M | 1095 | 192 | 0.67 | 0.27 |
| 52M | 1256 | 223 | 0.61 | 0.23 |
| 63M | 1335 | 240 | 0.53 | 0.20 |
| 73M | 1297 | 230 | 0.62 | 0.20 |
| 84M | 1496 | 266 | 0.54 | 0.20 |
| 94M | 1932 | 351 | 0.38 | 0.19 |
| 105M | 2282 | 418 | 0.33 | 0.13 |
| 115M | 2706 | 495 | 0.22 | 0.16 |
| 126M | 3007 | 553 | 0.22 | 0.14 |
| 131M | 3300 | 601 | 0.20 | 0.12 |

### walk13b(126M まで・eval 25 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.08 | 0.01 |
| 10M | 297 | 48 | 0.89 | 0.03 |
| 21M | 535 | 89 | 0.73 | 0.08 |
| 31M | 919 | 162 | 0.72 | 0.23 |
| 42M | 1329 | 247 | 0.61 | 0.22 |
| 52M | 1816 | 355 | 0.57 | 0.12 |
| 63M | 2058 | 398 | 0.47 | 0.10 |
| 73M | 2357 | 459 | 0.39 | 0.12 |
| 84M | 2774 | 540 | 0.38 | 0.09 |
| 94M | 3009 | 591 | 0.25 | 0.09 |
| 105M | 3072 | 606 | 0.24 | 0.10 |
| 115M | 3266 | 627 | 0.30 | 0.10 |
| 126M | 3338 | 642 | 0.28 | 0.15 |

### walk13c(68M まで・eval 14 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 193 | 31 | 1.06 | 0.01 |
| 5M | 243 | 39 | 0.96 | 0.03 |
| 10M | 303 | 49 | 0.93 | 0.02 |
| 16M | 402 | 66 | 0.78 | 0.06 |
| 21M | 602 | 100 | 0.71 | 0.12 |
| 26M | 831 | 140 | 0.64 | 0.18 |
| 31M | 976 | 162 | 0.61 | 0.30 |
| 37M | 1152 | 195 | 0.53 | 0.23 |
| 42M | 1634 | 284 | 0.43 | 0.20 |
| 47M | 1783 | 311 | 0.35 | 0.20 |
| 52M | 2293 | 406 | 0.32 | 0.29 |
| 58M | 2851 | 500 | 0.29 | 0.27 |
| 63M | 3668 | 637 | 0.23 | 0.26 |
| 68M | 3994 | 686 | 0.20 | 0.20 |

### walk13d(147M まで・eval 29 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 193 | 31 | 1.06 | 0.01 |
| 10M | 259 | 42 | 0.98 | 0.02 |
| 21M | 340 | 56 | 0.87 | 0.07 |
| 31M | 503 | 82 | 0.83 | 0.15 |
| 42M | 683 | 112 | 0.77 | 0.24 |
| 52M | 846 | 143 | 0.69 | 0.21 |
| 63M | 989 | 166 | 0.71 | 0.27 |
| 73M | 1112 | 188 | 0.67 | 0.27 |
| 84M | 1372 | 229 | 0.77 | 0.34 |
| 94M | 1431 | 246 | 0.70 | 0.28 |
| 105M | 1552 | 268 | 0.77 | 0.30 |
| 115M | 1960 | 342 | 0.76 | 0.28 |
| 126M | 1930 | 335 | 0.83 | 0.31 |
| 136M | 2515 | 436 | 0.90 | 0.30 |
| 147M | 2575 | 448 | 0.91 | 0.37 |

### walk13e(147M まで・eval 29 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 222 | 31 | 1.06 | 0.01 |
| 10M | 294 | 42 | 0.99 | 0.00 |
| 21M | 401 | 59 | 0.93 | 0.08 |
| 31M | 542 | 80 | 0.88 | 0.15 |
| 42M | 731 | 106 | 0.95 | 0.26 |
| 52M | 829 | 118 | 0.96 | 0.41 |
| 63M | 996 | 144 | 0.96 | 0.47 |
| 73M | 1054 | 152 | 0.99 | 0.52 |
| 84M | 1335 | 195 | 0.95 | 0.49 |
| 94M | 1481 | 216 | 0.98 | 0.53 |
| 105M | 1516 | 225 | 0.95 | 0.52 |
| 115M | 1890 | 290 | 0.90 | 0.41 |
| 126M | 1936 | 296 | 0.93 | 0.52 |
| 136M | 2450 | 374 | 0.96 | 0.42 |
| 147M | 2889 | 439 | 0.96 | 0.47 |

### walk4(42M まで・eval 9 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 147 | 44 | -0.18 | — |
| 5M | 221 | 59 | 0.05 | — |
| 10M | 496 | 126 | 0.06 | — |
| 16M | 2505 | 635 | 0.19 | — |
| 21M | 4158 | 924 | 0.45 | — |
| 26M | 4777 | 976 | 0.57 | — |
| 31M | 5132 | 993 | 0.62 | — |
| 37M | 5476 | 1000 | 0.57 | — |
| 42M | 5591 | 1000 | 0.62 | — |

### walk5(42M まで・eval 9 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 193 | 40 | -0.12 | — |
| 5M | 258 | 53 | -0.10 | — |
| 10M | 427 | 84 | -0.03 | — |
| 16M | 1864 | 382 | 0.09 | — |
| 21M | 4572 | 919 | 0.27 | — |
| 26M | 5193 | 965 | 0.45 | — |
| 31M | 5486 | 969 | 0.56 | — |
| 37M | 5922 | 997 | 0.57 | — |
| 42M | 6080 | 1000 | 0.61 | — |

### walk6(37M まで・eval 8 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 245 | 40 | -0.12 | — |
| 5M | 322 | 49 | -0.10 | — |
| 10M | 416 | 57 | -0.05 | — |
| 16M | 635 | 84 | 0.05 | — |
| 21M | 1607 | 217 | 0.03 | — |
| 26M | 5380 | 715 | 0.20 | — |
| 31M | 7299 | 928 | 0.33 | — |
| 37M | 7957 | 979 | 0.47 | — |

### walk8(37M まで・eval 8 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 174 | 34 | 0.98 | — |
| 5M | 214 | 42 | 0.82 | — |
| 10M | 273 | 54 | 0.74 | — |
| 16M | 369 | 74 | 0.66 | — |
| 21M | 583 | 119 | 0.67 | — |
| 26M | 1470 | 315 | 0.63 | — |
| 31M | 2821 | 612 | 0.71 | — |
| 37M | 3678 | 801 | 0.80 | — |

### walk9(37M まで・eval 8 回)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 164 | 31 | 1.09 | — |
| 5M | 219 | 42 | 0.95 | — |
| 10M | 288 | 56 | 0.86 | — |
| 16M | 386 | 75 | 0.84 | — |
| 21M | 629 | 125 | 0.77 | — |
| 26M | 1364 | 283 | 0.73 | — |
| 31M | 2800 | 589 | 0.85 | — |
| 37M | 4085 | 856 | 1.02 | — |

## 付録 I: よくありそうな質問(FAQ)

読者の方から来そうな質問を、先回りして正直に答えておきます。

**Q. 総額いくらかかりましたか?**
A. 追加投資は GPU を含む PC 一式だけです(数十万円級)。ソフトウェアは物理エンジンからロボットモデル、モーションデータ、学習フレームワークまで全部無料(OSS)でした。ランニングは電気代で、学習 1 種目あたり百円弱(12.1 節の実測試算)。趣味としてはカメラやゴルフより安い、というのが実感です。

**Q. 期間はどれくらい?**
A. この記事の実験群はおよそ数週間です。ただし 1 日中張り付いているわけではなく、「夕方仕込んで夜見る」の繰り返し。人間の作業時間より GPU の練習時間のほうがずっと長い。

**Q. プログラミングはどれくらいできる必要がありますか?**
A. 私自身は画像処理のエンジニアですが、この記事の実装作業の大半は AI コーディングエージェントに任せています(冒頭の帰属どおり)。必要だったのは、コードを書く力よりも「何を測れば嘘を見抜けるか」を決める力でした。プログラミング初心者でも、AI と組めば入口には立てる時代だと思います。ただし**結果の検証を AI 任せにしないこと** — そこだけは人間の仕事です。

**Q. 実機がないのに意味ありますか?**
A. 私はあると思って続けています。理由は 3 つ。①観測を実機センサ構成に合わせておけば、方策は原理的に実機へ持っていける(sim-to-real の入口には立っている)。②実機で危険・高価な失敗(数千回の転倒)はシミュレーションでしか積めない。③そもそも実機の開発現場でも、いまはシミュレーションで先に回すのが標準手順です。ただし、シミュレーションで完璧でも実機で崩れる要素(モデル化されていない摩擦、遅延、たわみ)は確実にあり、そこは未検証だと正直に言うほかありません。

**Q. AI にどこまで任せて、あなたは何をしたんですか?**
A. 方向を決める・仮説を出す・結果を疑う・やめ時を決める、が私。コードを書く・実験を回す・数値を集計する、が AI です。たとえば「イベントカメラ的な時間差分を足す」はこちらの発案で、「その実装で円柱交差を解析的に解く」は AI の仕事。逆に「48mm 持ち上げた」という報告を鵜呑みにせず「必ず映像で検証してから合格にする」というルールを敷いておくのがこちら側の仕事で、そのルールに従って実際に映像を精査し幻(初期化バグによる射出)だと突き止めたのは AI 自身です。役割分担が機能した例として気に入っています。

**Q. 失敗ばかりで嫌になりませんか?**
A. 嫌になる日もあります。ただ、この分野の失敗は「原因が必ず特定できる」タイプの失敗です(物理エンジンは再現可能なので)。原因が分かる失敗は資産になる — 付録 A の年代記が実際そうなったように。ちなみに一番へこんだのは、3 週連続で別々のズルを発明されたときです。

**Q. どこから始めればいいですか?**
A. おすすめの順路: ① MuJoCo を入れて Menagerie のロボットを画面に出す(1 日)→ ② 好きなモデルを keyframe 姿勢で立たせて物理を回す(1 日)→ ③ mujoco_playground の四足歩行チュートリアルを回す(数日)→ ④ 自分の「種目」を 1 つ決めて報酬を書く(ここから沼)。④ の前に本記事の付録 D(教訓集)を読むと、沼の深さが 3 割浅くなるはずです。

**Q. 子どもや学生でもできますか?**
A. シミュレーション自体は無料なので、GPU がなくても CPU で小さい実験はできます(学習は遅くなりますが、四足の歩行くらいなら現実的)。第 13 章の資料集に、見て楽しい入口(公式動画)から競技会(ROBO-ONE は個人参加可)までの導線をまとめてあります。

**Q. なんで運動会なんですか?**
A. 競技には計測と規律が入るからです(第 1 章)。あと、単純に楽しいからです。楽しくないと数週間も続きません。

**Q. この記事、長すぎませんか?**
A. はい。ただ、目次と 3 コース案内(冒頭)を付けたので、必要なところだけ拾えるようにはしてあります。長さは「一つの遊びをどこまで掘れるか」の実験だと思って眺めてください。これも一種の競技です。
