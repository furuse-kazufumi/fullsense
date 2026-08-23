#### domain(2 op)

| op | 설명 |
|---|---|
| `it_crop_domain` | domain op(HALCON: crop_domain) |
| `it_full_domain` | domain op(HALCON: -) |

#### matching(2 op)

| op | 설명 |
|---|---|
| `ncc_locate` | matching op(HALCON: find_ncc_model) |
| `shape_locate` | matching op(HALCON: find_shape_model) |

#### noise(2 op)

| op | 설명 |
|---|---|
| `add_noise_distribution` | noise op(HALCON: add_noise_distribution) |
| `add_noise_white` | noise op(HALCON: add_noise_white) |

#### Legacy(1 op)

| op | 설명 |
|---|---|
| `distance_funct_1d` | 두 함수 간의 거리(max=상한, mean=평균, distance_funct_1d). |

#### barcode(1 op)

| op | 설명 |
|---|---|
| `decode_barcode` | barcode op(HALCON: find_bar_code) |

#### classification(1 op)

| op | 설명 |
|---|---|
| `classify_shape` | classification op(HALCON: -) |

#### filter(1 op)

| op | 설명 |
|---|---|
| `Bilateral` | 엣지 보존 평활화(cv2.bilateralFilter, 부재 시 numpy 구현)(filter.Bilateral).  [backend=opencv] |

#### filtering(1 op)

| op | 설명 |
|---|---|
| `tf_gradient_domain_reintegrate` | filtering op(HALCON: -) |

#### intensity-transform(1 op)

| op | 설명 |
|---|---|
| `xmh_soft` | intensity-transform op(HALCON: -) |

#### misc(1 op)

| op | 설명 |
|---|---|
| `identity` | misc op(HALCON: copy_image) |

#### morphology/markers(1 op)

| op | 설명 |
|---|---|
| `xmh_regmin` | morphology/markers op(HALCON: -) |

#### region-morphology(1 op)

| op | 설명 |
|---|---|
| `xmh_majority` | region-morphology op(HALCON: -) |

#### region-transform(1 op)

| op | 설명 |
|---|---|
| `xmh_bwperim` | region-transform op(HALCON: -) |

#### self-similarity(1 op)

| op | 설명 |
|---|---|
| `xmh_selfmatch` | self-similarity op(HALCON: -) |

#### texture-feature(1 op)

| op | 설명 |
|---|---|
| `xmh_pftas` | texture-feature op(HALCON: -) |

#### texture/shape-feature(1 op)

| op | 설명 |
|---|---|
| `xmh_zernike` | texture/shape-feature op(HALCON: -) |

## 부록 G: 미래 자료집 — 센싱·우주·학회·경진대회(URL 실재 확인 완료)

제 13 장의 자료편이다. URL은 모두 집필 시점에 접속을 확인한 것만 실었다(확인하지 못한 것은 싣지 않았다). 링크가 끊겼을 때는 사이트 이름으로 검색하기 바란다.

### A. 센싱의 최전선

#### A-1. 이벤트 카메라 / 뉴로모픽 시각

**뭐가 대단한가(3줄)**
- 인간의 망막처럼 "변화한 픽셀만"을 비동기로 보내는 카메라. 시간 분해능은 마이크로초 오더, 다이내믹 레인지는 약 140 dB(일반 카메라는 약 60 dB)로, 모션 블러가 거의 없다([Gallego et al. survey](https://arxiv.org/abs/1904.08405) 참고).
- 드론 레이스에서 세계 챔피언을 이긴 자율 드론(UZH/ETH의 Scaramuzza 연구실)이나 NASA 화성 헬리콥터의 비전 계열 알고리즘에도 연구 성과가 파급됐다.
- Sony와 스타트업 Prophesee의 협업으로 4.86 µm 픽셀의 적층형 이벤트 센서(IMX636/637)가 양산화되어, "연구실의 별종"에서 "살 수 있는 부품"이 됐다.

| 항목 | 내용 | URL |
|---|---|---|
| 대표 논문 | Gallego et al., "Event-based Vision: A Survey", IEEE TPAMI 44(1), 2022(arXiv 2019) | https://arxiv.org/abs/1904.08405 |
| 대표 특허 | US10498977B2 "Event-based vision sensor"(Samsung, 2019 발행) | https://patents.google.com/patent/US10498977B2/en |
| 제품 1차 정보 | Sony 적층형 이벤트 센서 IMX636/IMX637 보도자료(2021) | https://www.sony-semicon.com/en/news/2021/2021090901.html |
| 제품 1차 정보 | Prophesee × Sony IMX636 / 평가 키트 EVK4 | https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/ / https://www.prophesee.ai/event-camera-evk4/ |
| 연구실 | Robotics and Perception Group(UZH & ETH Zurich, Davide Scaramuzza 교수) | https://rpg.ifi.uzh.ch/ (본인 페이지: https://rpg.ifi.uzh.ch/people_scaramuzza.html ) |
| 연구실 GitHub | uzh-rpg(ESIM 외 다수 공개) | https://github.com/uzh-rpg |
| 공개 데이터셋 | UZH-FPV 드론 레이스 데이터셋(이벤트+IMU+레이저 참값) | https://fpv.ifi.uzh.ch/ |
| 시뮬레이터 | ESIM: an Open Event Camera Simulator(CoRL 2018) | https://github.com/uzh-rpg/rpg_esim |
| 시뮬레이터 | v2e: 일반 동영상→리얼한 DVS 이벤트 변환(CVPRW 2021 Best Paper) | https://github.com/SensorsINI/v2e (해설: https://sites.google.com/view/video2events/home ) |
| 동영상 | UZH RPG 공식 YouTube(자율 드론·이벤트 카메라 데모 다수) | https://www.youtube.com/user/ailabRPG |

#### A-2. 양자 센싱(NV 센터 자기 계측·양자 관성 항법)

**뭐가 대단한가(3줄)**
- 다이아몬드 속 원자 결함(NV 센터) 1개가 "양자 나침반"이 되어, 상온에서 세포 스케일의 자기장까지 잴 수 있다. 양자 센싱의 표준 교과서급 리뷰가 [Degen–Reinhard–Cappellaro (Rev. Mod. Phys. 2017)](https://dspace.mit.edu/bitstream/handle/1721.1/124553/RevModPhys.89.035002.pdf).
- 냉각 원자를 "파동"으로 간섭시키는 원자 간섭계는, GPS를 쓸 수 없는 곳에서도 위치를 잃지 않는 관성 항법의 본명. 미군 스페이스플레인 X-37B의 제 8 비행에서 양자 관성 센서의 궤도상 시험이 계획됐다([The Conversation, 2025](https://theconversation.com/quantum-alternative-to-gps-navigation-will-be-tested-on-us-military-spaceplane-262967)).
- MIT는 NV 센터와 CMOS 칩의 통합(온칩 양자 센서)을 실증했고, "양자 센서를 평범한 반도체 부품으로 만드는" 흐름이 진행 중이다([MIT News, 2019](https://news.mit.edu/2019/quantum-sensing-chip-0925)).

| 항목 | 내용 | URL |
|---|---|---|
| 대표 논문 | Degen, Reinhard, Cappellaro, "Quantum sensing", Rev. Mod. Phys. 89, 035002 (2017) | https://dspace.mit.edu/bitstream/handle/1721.1/124553/RevModPhys.89.035002.pdf (DOI: 10.1103/RevModPhys.89.035002) |
| 대표 리뷰 | BEC를 쓰는 양자 관성 항법의 전망(Applied Physics Reviews, 2025) | https://pubs.aip.org/aip/apr/article/12/3/031306/3351228/Developments-for-quantum-inertial-navigation |
| 대표 특허 | US12424810B1 "Compact atom interferometry inertial navigation sensors with tailored diffractive optics"(Sandia, 2025) | https://patents.google.com/patent/US12424810B1/en |
| 대표 특허 | US7317184B2 "Kinematic sensors employing atom interferometer phases"(2008) | https://patents.google.com/patent/US7317184B2/en |
| 연구기관 | Sandia National Laboratories – Atom Interferometry | https://www.sandia.gov/quantum/atom-interferometry/ |
| 연구기관 | QuTech(TU Delft + TNO. NV 센터로 양자 네트워크 세계 최초 실증군) | https://qutech.nl/ |
| 연구실(일본) | 도쿄과학대(구 도쿄공업대) 이와사키 연구실 – 고체 양자 센서 | http://dia.pe.titech.ac.jp/en/solid-quantum-sensors/ |
| 해설 기사 | MIT Technology Review "양자 항법은 GPS 재밍 문제를 풀 수 있을까"(2025-12) | https://www.technologyreview.com/2025/12/16/1129887/quantum-navigation-militarys-gps-jamming-problem/ |
| 자택 입구 | QuTiP: 열린 양자계 다이내믹스의 OSS 시뮬레이터(Python) | https://qutip.org/ |

#### A-3. 하이퍼스펙트럴·편광 이미징

**뭐가 대단한가(3줄)**
- 모든 픽셀에 "분광 스펙트럼"이 붙은 이미지(하이퍼큐브)를 찍는 기술. 인간의 눈에는 같은 색이라도, 재질·수분·신선도·병변이 "스펙트럼의 지문"으로 구별된다.
- 농업(작물 스트레스·잡초 판별), 식품 검사, 암 검출·수술 중 이미징, 광물 탐사, 재활용 선별까지 응용이 확대 중이다([Heliyon 2024 리뷰](https://www.sciencedirect.com/science/article/pii/S2405844024092399)).
- 의료 분야에서는 편광×하이퍼스펙트럴 융합(PHSI), 하이퍼스펙트럴 내시경, AR 통합 등이 최전선이다([2025 의료 HSI 리뷰](https://pmc.ncbi.nlm.nih.gov/articles/PMC13003176/)).

| 항목 | 내용 | URL |
|---|---|---|
| 대표 리뷰 | "Hyperspectral imaging and its applications: A review", Heliyon (2024) | https://www.sciencedirect.com/science/article/pii/S2405844024092399 |
| 대표 리뷰 | "Modern Trends and Recent Applications of Hyperspectral Imaging: A Review", Technologies (2025) | https://www.mdpi.com/2227-7080/13/5/170 |
| 의료 리뷰 | Medical hyperspectral imaging: updated review(편광 HSI·내시경·AR 통합) | https://pmc.ncbi.nlm.nih.gov/articles/PMC13003176/ |

#### A-4. 촉각 스킨·전자 피부

**뭐가 대단한가(3줄)**
- MIT의 GelSight는 "카메라로 젤의 변형을 본다"만으로 인간 손끝을 넘는 공간 분해능의 촉각을 실현. 지금은 GelSight 사로 제품화되어, 로봇의 손끝이 되기도 했다([MIT News](https://news.mit.edu/2017/gelsight-robots-sense-touch-0605)).
- 스탠퍼드 Bao 연구실의 전자 피부는, 늘어나고·자가 수복하고·압력과 전단력을 구별하는 것을 재료화학부터 만들어 넣는다. 의수에 "촉각"을 되돌려주는 것이 골.
- 촉각은 시각의 "마지막 원 마일". 잡는 순간의 미끄러짐·단단함·마찰은 카메라로는 보이지 않아, Physical AI의 다음 주전장이 되고 있다.

| 항목 | 내용 | URL |
|---|---|---|
| 대표 논문 | Yuan, Dong, Adelson, "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force", Sensors 17(12):2762 (2017) | https://www.mdpi.com/1424-8220/17/12/2762 |
| 대표 특허 | WO2023081342A1 "Four-dimensional tactile sensing system, device, and method"(2023) | https://patents.google.com/patent/WO2023081342A1/en |
| 연구실 | MIT CSAIL(Adelson 연구실 계열) GelSight Wedge 프로젝트 | https://gelsight.csail.mit.edu/wedge/ |
| 연구실 | Stanford Bao Group(전자 피부·신축 일렉트로닉스) | https://baogroup.stanford.edu/ |
| 기업 | GelSight, Inc.(GelSight Mini 등) | https://www.gelsight.com/gelsightmini/ |
| 해설 | MIT News "Giving robots a sense of touch" (2017) | https://news.mit.edu/2017/gelsight-robots-sense-touch-0605 |

#### A-5. 신경 인터페이스적 센싱(근전 / EIT) — 가볍게

**뭐가 대단한가(3줄)**
- Meta(구 CTRL-labs)의 손목밴드는 손목의 표면 근전(sEMG)만으로, 개인별 보정 없이 손가락의 미세한 움직임을 디코딩. 허공의 손글씨를 분당 약 20.9 단어로 입력할 수 있다(Nature 2025 게재).
- "뇌에 전극을 꽂지 않는" 비침습 뉴로모터 인터페이스가, 키보드·마우스의 다음 표준 입력을 노리는 위치까지 왔다.
- 전기 임피던스 단층촬영(EIT)을 팔찌화하는 연구도 있어, 저비용·저전력(약 50 mW)으로 제스처 인식 정확도 93%의 보고가 있다([Biosensors 2026](https://www.mdpi.com/2079-6374/16/4/200)).

| 항목 | 내용 | URL |
|---|---|---|
| 대표 논문 | "A generic non-invasive neuromotor interface for human-computer interaction", Nature 645 (2025) | https://www.nature.com/articles/s41586-025-09255-w |
| 1차 정보 | Meta EMG Wristband 공식 페이지 | https://www.meta.com/emerging-tech/emg-wearable-technology/ |
| 관련 논문 | EIT 기반의 강건한 제스처 인식(Biosensors, 2026) | https://www.mdpi.com/2079-6374/16/4/200 |

---

### B. 우주 개발

#### B-1. 궤도상 서비싱·데브리 포획

**뭐가 대단한가(3줄)**
- Astroscale의 ADRAS-J(JAXA CRD2 페이즈 I)는, 2024년에 "협력 기능을 일절 갖지 않은" 약 3톤의 로켓 상단으로 15 m까지 자율 접근해, 주회 관측에 성공. 세계 최초급의 실적이다([Astroscale 공식](https://www.astroscale.com/en/news/astroscales-adras-j-achieves-historic-15-meter-approach-to-space-debris)).
- 이어지는 ADRAS-J2(CRD2 페이즈 II)는 로봇 팔로 같은 데브리를 실제로 포획·궤도 강하시킬 계획. ESA × ClearSpace의 ClearSpace-1도 4개 팔로 하는 포획 실증을 준비 중이다.
- "텀블링하는 비협력 물체에 안전하게 다가가 잡는다" = 자유 부유 물체의 랑데부&캡처는, GNC(유도·항법·제어)·시각·접촉역학의 종합 격투기. 그야말로 시뮬레이션이 주전장이다.

| 항목 | 내용 | URL |
|---|---|---|
| 공식 미션 | Astroscale ADRAS-J 미션 페이지 | https://www.astroscale.com/en/missions/adras-j |
| 공식 프로그램 | JAXA CRD2(상업 데브리 제거 실증) | https://www.kenkai.jaxa.jp/eng/crd2/index.html |
| 1차 정보 | JAXA 보도: ADRAS-J의 데브리 주회 관측 이미지(2024-07) | https://global.jaxa.jp/press/2024/07/20240730-1_e.html |
| 특허(해설) | Astroscale 특허 US12,479,603 B2 "텀블링 물체의 포획 방법" 공식 해설 | https://www.astroscale.com/en/news/astroscale-patent-advances-docking-and-servicing-of-tumbling-satellites |
| 제품 | Astroscale 도킹 플레이트(자기 포획용 "위성의 견인 고리") | https://www.astroscale.com/en/docking-plate |
| 해설 기사 | MIT Technology Review: 세계 최초의 데브리 제거 미션 개시(2024) | https://www.technologyreview.com/2024/02/27/1089065/first-mission-dead-rocket/ |
| 동영상 첨부 기사 | ADRAS-J의 플라이어라운드 영상(Space.com) | https://www.space.com/astroscale-debris-removal-adras-j-video |

※ ClearSpace 사 공식 사이트는 URL 미확인이라 싣지 않았다(ClearSpace-1의 개황은 위 Space.com / MIT Tech Review 기사 안에서 언급).

#### B-2. 달 표면 로보틱스

**뭐가 대단한가(3줄)**
- JAXA × 도요타의 유인 여압 로버 "LUNAR CRUISER"는 수소 연료전지로 달리는 "달 표면의 캠핑카". 미니버스 2대분 크기로 우주복 없이 탈 수 있다([도요타 공식](https://global.toyota/en/mobility/technology/lunarcruiser/)).
- NASA JPL의 CADRE는, 여행가방 크기의 로버 3대가 스스로 "리더"를 뽑고, 역할을 분담해 달 표면을 3D 매핑하는 자율 협조 실증. 지구에서는 "이 영역을 탐사하라"라는 목표만 준다([JPL 공식](https://www.jpl.nasa.gov/missions/cadre/)).
- 한편 NASA의 물 얼음 탐사 로버 VIPER는 2024년에 계획 중지(투입된 금액 약 4.5억 달러). 최전선은 "전부 성공하는 이야기"가 아니라는 것도 정직하게 전하고 싶다.

| 항목 | 내용 | URL |
|---|---|---|
| 공식 | 도요타 LUNAR CRUISER 공식 페이지 | https://global.toyota/en/mobility/technology/lunarcruiser/ |
| 공식 | NASA JPL CADRE 미션 페이지 | https://www.jpl.nasa.gov/missions/cadre/ |
| 1차 정보 | NASA: CADRE 로버, 달 여행 채비 완료(IM-3으로 2026년 도착 예정) | https://www.nasa.gov/missions/tech-demonstration/cadre/nasas-mini-rover-team-is-packed-for-lunar-journey/ |
| 기업 | ispace(HAKUTO-R 프로그램) | https://www.ispace-inc.com/aboutus |
| 보도 | VIPER 계획 중지의 경위(Spaceflight Now, 2024) | https://spaceflightnow.com/2024/07/18/nasa-cancels-half-billion-dollar-water-ice-seeking-moon-rover/ |
| 일본 | 도호쿠대가 달 표면 인프라 대형 프로젝트를 주도(2026) | https://www.tohoku.ac.jp/en/news/university_news/selected_to_lead_landmark_lunar_infrastructure_project.html |

#### B-3. 궤도상 제조·우주 건축

**뭐가 대단한가(3줄)**
- Varda Space는 무중력에서만 만들 수 있는 "더 완전한 결정"을 노려, 항바이러스제 Ritonavir의 결정을 궤도상에서 제조해 캡슐로 가지고 돌아오는 데 성공(2024년 W-1 미션). 이미 캡슐 비행 6회차까지 진행.
- 미소중력은 대류도 침강도 없기 때문에, 단백질 결정·의약품·특수 광섬유의 제조 환경으로 본명시되며, Redwire는 우주 제약 전문 자회사 SpaceMD를 설립했다([CNBC, 2026](https://www.cnbc.com/2026/06/09/space-race-pharma-spacex-varda-redwire-drug-development-orbit.html)).
- "공장을 쏘아 올리고 제품만 마하 25로 가지고 돌아온다"라는 산업 구조 자체가 새롭다. 재진입 캡슐의 공력·열 방어도 시뮬레이션 덩어리다.

| 항목 | 내용 | URL |
|---|---|---|
| 공식 | Varda W-Series 플랫폼(궤도상 제조+재진입) | https://www.varda.com/platform |
| 공식 | Redwire(우주 인프라+우주 제약 SpaceMD) | https://rdw.com/ |
| 보도 | Varda 캡슐, 우주 제조약을 싣고 귀환(Space.com, 2024) | https://www.space.com/varda-in-space-manufacturing-capsule-landing-success |
| 보도 | 제약이 LEO로 향하는 이유(CNBC, 2026-06) | https://www.cnbc.com/2026/06/09/space-race-pharma-spacex-varda-redwire-drug-development-orbit.html |

#### B-4. 우주용 시뮬레이터 OSS(전부 무료로 자택 PC에 들어간다)

| 도구 | 무엇을 할 수 있나 | URL |
|---|---|---|
| NASA GMAT | 미션 설계·궤도 설계의 본격파(NASA 실무에서도 사용). GUI+스크립트 | https://sourceforge.net/projects/gmat/ |
| Basilisk | 우주기의 자세·궤도·비행 소프트웨어까지 모듈식으로 통합 시뮬레이션(콜로라도대 AVS Lab) | https://avslab.github.io/basilisk/ |
| 42 (NASA GSFC) | 복수 우주기의 자세·궤도역학. 랑데부·편대 비행 연구에도 | https://github.com/ericstoneking/42 |
| poliastro | Python으로 궤도역학. 교육·프로토타이핑의 입구로 최적 | https://github.com/poliastro/poliastro |
| Kerbal Space Program | 게임이지만 궤도역학의 직감을 만드는 교육 정번(교육판 KerbalEdu도 존재) | https://www.kerbalspaceprogram.com/ |

#### B-5. 회전날개로 행성을 난다 — Ingenuity의 유산과 Dragonfly

**뭐가 대단한가(3줄)**
- 화성 헬리콥터 Ingenuity는 "대기 밀도가 지구의 1%인 하늘에서 날 수 있는가"라는 실험기였는데도, 상정 5회였던 것을 72회 비행하고 2024년에 퇴역([JPL 공식](https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/)). 비용 8,500만 달러의 기술 실증이 행성 탐사의 형태를 바꿨다.
- 후계기 Dragonfly는 토성의 달 타이탄으로 보내는 원자력 구동 8로터기(자동차 크기). 2028년 7월 발사 예정으로, 생명의 화학적 기원을 하늘에서 찾는다([JHUAPL 공식](https://dragonfly.jhuapl.edu/)).
- "나는 곳의 공기·중력이 지구와 다르기" 때문에, 설계의 주역은 철저한 시뮬레이션과 지상 시험. 회전날개 공력은 자택의 CFD(흐름을 계산기로 푸는 수치유체역학)/물리 엔진으로도 입구에 설 수 있다.

| 항목 | 내용 | URL |
|---|---|---|
| 공식 | Dragonfly 미션(JHU APL) | https://dragonfly.jhuapl.edu/ (별관: https://www.jhuapl.edu/destinations/missions/dragonfly ) |
| 공식 갤러리 | Dragonfly Gallery(상상도·시험 영상) | https://dragonfly.jhuapl.edu/Gallery/ |
| 공식 | NASA Ingenuity 미션 페이지 | https://science.nasa.gov/mission/mars-2020-perseverance/ingenuity-mars-helicopter/ |
| 1차 정보 | JPL: Ingenuity 미션 종료 발표(72 비행) | https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ |

---

### C. 시뮬레이션으로 최전선을 "자택 재현"할 수 있는 예

"억 엔급 실험 장치가 없어도, 물리 법칙은 다운로드할 수 있다"가 이 장의 메시지다. 전부 무료 OSS.

| 최전선 테마 | 자택 PC + OSS에서의 입구 | URL |
|---|---|---|
| 이벤트 카메라 | 갖고 있는 동영상을 **v2e**로 이벤트 스트림으로 변환해 "망막이 보는 세계"를 체험. 본격파는 **ESIM**으로 3D 씬에서 이벤트 생성 | https://github.com/SensorsINI/v2e / https://github.com/uzh-rpg/rpg_esim |
| 데브리 포획·자유 부유 물체 | **MuJoCo**로 중력 제로+팔 달린 위성의 MJCF를 쓰고, 텀블링하는 물체의 포획을 물리 시뮬레이션(공식 로봇 모델집 Menagerie가 출발점) | https://github.com/google-deepmind/mujoco / https://github.com/google-deepmind/mujoco_menagerie |
| 궤도 계획·미션 설계 | **GMAT**로 지구-달 천이 궤도를 짜고, **poliastro**(Python)로 호만 천이를 수십 줄로 계산 | https://sourceforge.net/projects/gmat/ / https://github.com/poliastro/poliastro |
| 우주기의 자세 제어 | **Basilisk** 또는 **42**로 리액션 휠 제어·편대 비행을 시뮬레이션 | https://avslab.github.io/basilisk/ / https://github.com/ericstoneking/42 |
| 달 표면 로버·보행 로봇의 RL | **Gymnasium** + **MuJoCo Playground**(GPU 가속)로 강화학습. 저중력은 XML의 gravity 1줄로 달이 된다 | https://github.com/Farama-Foundation/Gymnasium / https://github.com/google-deepmind/mujoco_playground |
| 양자 센싱 | **QuTiP**으로 스핀의 Rabi 진동·Ramsey 간섭(NV 센터 계측의 원리 그 자체)을 수치 실험 | https://qutip.org/ |
| 궤도역학의 직감 | **Kerbal Space Program**으로 "중력 턴" "천이 궤도"를 몸으로 익힌다(교육 카테고리) | https://www.kerbalspaceprogram.com/ |

---

### D. 보고 자극을 받기 위한 자료

#### D-1. 보면 자극이 되는 공식 갤러리·동영상

| 소스 | 내용 | URL |
|---|---|---|
| NASA Image and Video Library | 14만 점 넘는 이미지·동영상·음성을 횡단 검색 | https://images.nasa.gov/ |
| NASA Galleries | 미션별 갤러리 입구 | https://www.nasa.gov/gallery/ |
| JAXA 디지털 아카이브 | JAXA의 사진·영상 아카이브(이용 조건 페이지 포함) | https://jda.jaxa.jp/en/service.php |
| ESA Images | ESA 공식 이미지 갤러리 | https://www.esa.int/ESA_Multimedia/Images |
| UZH Robotics and Perception Group | 이벤트 카메라·자율 드론 레이스 데모 동영상 | https://www.youtube.com/user/ailabRPG |
| Boston Dynamics | Atlas / Spot 공식 채널 | https://www.youtube.com/@BostonDynamics |
| Unitree Robotics | G1 / Go2 등 공식 데모 | https://www.youtube.com/@unitreerobotics/videos |
| Dragonfly Gallery | 타이탄 탐사기의 상상도·시험 영상 | https://dragonfly.jhuapl.edu/Gallery/ |

#### D-2. 이 분야에 강한 대학·연구기관(실재 확인 완료 연구실 URL)

| 대학·기관 | 연구실 / 부문 | 분야 | URL |
|---|---|---|---|
| Univ. of Zurich & ETH Zurich | Robotics and Perception Group(Scaramuzza) | 이벤트 카메라·자율 드론 | https://rpg.ifi.uzh.ch/ |
| MIT | CSAIL GelSight 프로젝트(Adelson 계열) | 시각 기반 촉각 | https://gelsight.csail.mit.edu/wedge/ |
| Stanford | Bao Group | 전자 피부·신축 일렉트로닉스 | https://baogroup.stanford.edu/ |
| Stanford | Interactive Perception and Robot Learning Lab | 로봇 조작·지각 | https://iprl.stanford.edu/ |
| CMU | Robotics Institute(1979년 설립, 세계 최대급) | 로보틱스 전반 | https://www.ri.cmu.edu/ |
| TUM | MIRMI(Munich Institute of Robotics and Machine Intelligence) | 로보틱스·기계지능(70+ 교수) | https://www.mirmi.tum.de/en/mirmi/home/ |
| TU Delft | QuTech(+ TNO) | 양자 컴퓨터·양자 인터넷·NV 센터 | https://qutech.nl/ |
| Sandia National Labs | Atom Interferometry 그룹 | 양자 관성 항법 | https://www.sandia.gov/quantum/atom-interferometry/ |
| 도호쿠대학 | Space Robotics Lab(요시다 연구실. ETS-VII, HAKUTO 기술 리더) | 우주 로봇·달 표면 탐사 | https://astro2.mech.tohoku.ac.jp/en/ |
| 도쿄대학 | Intelligent Space Systems Laboratory(항공우주) | 우주기 GNC·자율화 | https://www.space.t.u-tokyo.ac.jp/ |
| 도쿄대학 | JSK Robotics Laboratory | 휴머노이드·지능 로봇 | http://www.jsk.t.u-tokyo.ac.jp/information.html |
| 도쿄과학대(구 도쿄공업대) | 이와사키 연구실(고체 양자 센서) | NV 센터 양자 센싱 | http://dia.pe.titech.ac.jp/en/solid-quantum-sensors/ |
| JHU APL | Dragonfly 미션 팀(PI: Elizabeth Turtle) | 행성 회전날개 탐사 | https://dragonfly.jhuapl.edu/ |
| NASA JPL | CADRE(자율 협조 로버) | 달 표면 멀티 로봇 | https://www.jpl.nasa.gov/missions/cadre/ |

---

### E. 관련 학회·전시회·경진대회 — "보러 갈 수 있다 / 나갈 수 있다" 동선

#### E-1. 학회(연구의 최전선을 "읽고·듣는다")

| 학회 | 소개(1〜2줄) | 개최 시기의 기준 | URL |
|---|---|---|---|
| ICRA | IEEE RAS 기함의 로보틱스 최대급 회의. 2026년은 빈(6/1–5), 2027년은 5월 하순 | 매년 5〜6월 | https://www.ieee-ras.org/conferences-workshops/fully-sponsored/icra/ (2026: https://2026.ieee-icra.org/ ) |
| IROS | IEEE/RSJ 공동 주최의 또 하나의 최대급 회의(1988년〜). 2026년은 피츠버그 | 매년 10월 전후 | https://www.ieee-ras.org/conferences-workshops/financially-co-sponsored/iros/ (2026: https://2026.ieee-iros.org/ ) |
| RSS | 소수 정예·구두 발표 중심의 "품질 중시" 회의. 2026년은 시드니(7/13–17) | 매년 7월 전후 | https://roboticsconference.org/ |
| CoRL | 로봇 학습(RL·모방·기반 모델) 전문의 젊은 회의(2017년〜). 2026년은 11/9–12 | 매년 11월 전후 | https://www.corl.org/ |
| Humanoids | IEEE-RAS 휴머노이드 전문 회의(2000년〜). 제 25회는 2026-12 실리콘밸리 | 매년 11〜12월 | https://2026.ieee-humanoids.org/ |
| NeurIPS(관련 WS) | ML 최고봉 회의. Robot Learning 계열 워크숍이 매년 병설(예: World Models × 로봇 학습 WS @ NeurIPS 2026) | 매년 12월 | https://neurips.cc/ (WS 예: https://robowm-ws.github.io/ ) |
| ICLR(관련 WS) | 표현 학습의 최고봉 회의. 로보틱스×기반 모델 계열 WS의 수용처 | 매년 4〜5월 | https://iclr.cc/ |

#### E-2. 전시회(실기를 "보러 간다" — 학생도 입장하기 쉽다)

| 전시회 | 소개(1〜2줄) | 개최 시기의 기준 | URL |
|---|---|---|---|
| 국제 로봇전 iREX(도쿄) | 1974년부터 이어지는 세계 최대급 로봇전. 2025년은 도쿄 빅사이트에서 12/3–6 개최, 다음 회는 2027년 12월 | 격년 12월(홀수 해) | https://irex.nikkan.co.jp/ |
| World Robot Conference(베이징) | 중국 최대급의 로봇 회의+전시+경기의 복합 이벤트. 휴머노이드 신제품의 첫 공개 무대로 | 매년 8월경 | https://www.worldrobotconference.com/ |
| CES(라스베이거스) | 세계 최대급 테크 박람회. 최근에는 휴머노이드·Physical AI의 주요 발표 무대 | 매년 1월 | https://www.ces.tech/ |
| automatica(뮌헨) | 스마트 자동화·산업용 로봇의 세계적 박람회. 다음 회 2027년 6/22–25 | 격년 6월 | https://automatica-munich.com/en/ |
| CEATEC(마쿠하리) | 일본 최대급의 IT·일렉트로닉스전. 2026년은 10/13–16 마쿠하리 멧세. 학생 입장 문턱이 낮다 | 매년 10월 | https://www.ceatec.com/en/ |

#### E-3. 경진대회("나갈 수 있다" — 개인·학생 팀의 입구)

| 경진대회 | 소개(1〜2줄) | 개최 시기의 기준 | URL |
|---|---|---|---|
| **ROBO-ONE(일본)** ★중점 | 2002년부터 이어지는 이족보행 로봇 격투 경기. **개인이 자작 휴머노이드로 출전할 수 있는** 일본발 문화로, 시판기로 나갈 수 있는 초심자용 "ROBO-ONE Light"도 있다. 본 기사의 "개인이 하는 로봇 운동회"의 실세계판으로 가장 궁합이 좋다 | 연 2회 정도(봄·가을) | https://www.robo-one.com/ (해설: https://www.robo-one.com/abouts/view/aboutroboone/ ) |
| RoboCup | "2050년에 월드컵 우승팀에 로봇으로 이긴다"를 내건 국제 경진대회. 축구 외에 레스큐·가정·산업 리그, 중고생용 RoboCupJunior도 있다 | 매년 7월 전후(세계 대회) | https://www.robocup.org/ |
| World Humanoid Robot Games(베이징) | 2025년 8월에 냐오차오(鳥の巣)에서 첫 개최. 16개국 280팀·500대 넘는 휴머노이드가 26종목에서 경기(100 m 달리기 우승 기록은 21.50초). 제 2회는 2026년 8월 | 매년 8월 | https://english.beijing.gov.cn/whatson/events/sports/202505/t20250509_4085816.html (개요: https://en.wikipedia.org/wiki/World_Humanoid_Robot_Games ) |
| DARPA Robotics Challenge(역사) | 2012–2015년의 휴머노이드 재해 대응 경기. 당시 로봇은 전도가 속출했지만, 현재 휴머노이드 붐의 원점. "10년 만에 여기까지 왔다"를 말하는 소재 | 종료(아카이브) | https://www.darpa.mil/research/programs/darpa-robotics-challenge |
| DARPA Triage Challenge(현행) | DARPA 현행 챌린지의 예. 대량 부상자 트리아지를 센싱+자율 시스템으로 혁신하는 경기(2025년에 결승) | 프로그램 진행 중 | https://triagechallenge.darpa.mil/ |

> 동선 메모: "관람"이라면 CEATEC·iREX(일본 내·저비용)→ "출전"이라면 ROBO-ONE Light(시판기 가능)→ RoboCupJunior(중고생)→ 대학에서 RoboCup/학회, 라는 계단을 그릴 수 있다.

---

### 기사에 쓸 수 있는 "사실+출처" 메모(과장 방지용)

| 사실 | 출처 |
|---|---|
| 이벤트 카메라의 시간 분해능은 마이크로초대, 다이내믹 레인지 약 140 dB(프레임 카메라 약 60 dB) | https://arxiv.org/abs/1904.08405 |
| Sony IMX636/637은 업계 최소(발표 당시)의 4.86 µm 이벤트 픽셀·1280×720 | https://www.sony-semicon.com/en/news/2021/2021090901.html |
| Meta의 sEMG 밴드는 보정 없는 범용 디코딩, 허공 손글씨 20.9 단어/분(Nature 645, 2025) | https://www.nature.com/articles/s41586-025-09255-w |
| ADRAS-J는 비협력 데브리(전장 약 11 m·약 3톤)로 15 m까지 자율 접근(2024) | https://www.astroscale.com/en/news/astroscales-adras-j-achieves-historic-15-meter-approach-to-space-debris |
| Ingenuity는 3년간 72회 비행, 2024-01에 미션 종료. 기술 실증으로서의 비용은 약 8,500만 달러 | https://www.jpl.nasa.gov/news/after-three-years-on-mars-nasas-ingenuity-helicopter-mission-ends/ / https://www.space.com/space-exploration/missions/nasa-begins-building-nuclear-powered-dragonfly-drone-for-2028-launch-to-saturn-moon-titan |
| Dragonfly는 미션 총액 약 33.5억 달러, 2028-07 발사 예정(Falcon Heavy), CDR 통과 완료 | https://www.space.com/space-exploration/missions/nasa-begins-building-nuclear-powered-dragonfly-drone-for-2028-launch-to-saturn-moon-titan |
| Varda W-1은 Ritonavir 결정을 궤도상 제조해 2024-02에 지상 회수(민간 최초급) | https://www.space.com/varda-in-space-manufacturing-capsule-landing-success |
| NASA VIPER는 2024-07에 중지 결정(투입된 금액 약 4.5억 달러, 중지로 인한 절약은 약 8,400만 달러) | https://spaceflightnow.com/2024/07/18/nasa-cancels-half-billion-dollar-water-ice-seeking-moon-rover/ |
| CADRE는 3대의 자율 로버가 IM-3 랜더로 Reiner Gamma로(2026 예정) | https://www.jpl.nasa.gov/missions/cadre/ / https://www.nasa.gov/missions/tech-demonstration/cadre/nasas-mini-rover-team-is-packed-for-lunar-journey/ |
| X-37B 제 8 비행에서 양자 관성 센서(원자 간섭계)의 궤도상 시험을 계획(2025) | https://theconversation.com/quantum-alternative-to-gps-navigation-will-be-tested-on-us-military-spaceplane-262967 |

---

## 부록 H: 학습 로그 실측 발췌 — 13세대의 성장 곡선을 숫자 그대로

각 세대의 학습 로그에서, eval 행(약 5.2M 스텝마다)의 주요 값을 발췌한 생 데이터 표다(모두 MuJoCo 시뮬레이션 내의 실측값). 그래프보다 거칠지만, "어느 세대가, 언제, 어떻게 늘었나/막혔나"를 원전으로 확인할 수 있다(reward는 세대 간에 보상 설계가 다르므로 **세로 비교는 할 수 없다**. 같은 세대 안의 추이만 봐 주기 바란다). ep_len은 생존 스텝(×0.02초), fwd_v는 전진 속도 m/s, crash는 충돌률이다.

### walk10(26M까지·eval 6회)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 194 | 31 | 1.09 | — |
| 5M | 258 | 42 | 0.93 | — |
| 10M | 338 | 57 | 0.83 | — |
| 16M | 469 | 81 | 0.80 | — |
| 21M | 691 | 126 | 0.72 | — |
| 26M | 1861 | 371 | 0.71 | — |

### walk11(31M까지·eval 7회)

| steps | reward | ep_len | fwd_v | crash |
|---|---|---|---|---|
| 0M | 195 | 31 | 1.09 | — |
| 5M | 265 | 43 | 0.95 | — |
| 10M | 354 | 58 | 0.85 | — |
| 16M | 471 | 78 | 0.78 | — |
| 21M | 685 | 118 | 0.67 | — |
| 26M | 1673 | 316 | 0.67 | — |
| 31M | 3331 | 667 | 0.83 | — |

### walk12(52M까지·eval 11회)

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

### walk12b(58M까지·eval 12회)

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

### walk12c(68M까지·eval 14회)

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

### walk13(131M까지·eval 26회)

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

### walk13b(126M까지·eval 25회)

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

### walk13c(68M까지·eval 14회)

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

### walk13d(147M까지·eval 29회)

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

### walk13e(147M까지·eval 29회)

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

### walk4(42M까지·eval 9회)

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

### walk5(42M까지·eval 9회)

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

### walk6(37M까지·eval 8회)

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

### walk8(37M까지·eval 8회)

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

### walk9(37M까지·eval 8회)

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

## 부록 I: 있을 법한 질문(FAQ)

독자에게서 올 법한 질문에, 미리 정직하게 답해 둔다.

**Q. 총액 얼마 들었나요?**
A. 추가 투자는 GPU를 포함한 PC 한 세트뿐이다(수십만 엔급). 소프트웨어는 물리 엔진부터 로봇 모델, 모션 데이터, 학습 프레임워크까지 전부 무료(OSS)였다. 러닝 비용은 전기요금으로, 학습 1종목당 백 엔이 안 된다(12.1절의 실측 추산). 취미로서는 카메라나 골프보다 싸다는 게 실감이다.

**Q. 기간은 어느 정도?**
A. 이 기사의 실험군은 대략 몇 주다. 다만 하루 종일 붙어 있는 건 아니고, "저녁에 걸어 두고 밤에 본다"의 반복. 인간의 작업 시간보다 GPU의 연습 시간이 훨씬 길다.

**Q. 프로그래밍은 어느 정도 할 수 있어야 하나요?**
A. 나 자신은 영상처리 엔지니어지만, 이 기사의 구현 작업 대부분은 AI 코딩 에이전트에게 맡기고 있다(서두의 귀속 표기대로). 필요했던 것은 코드를 쓰는 힘보다 "무엇을 재면 거짓을 간파할 수 있는가"를 정하는 힘이었다. 프로그래밍 초심자라도, AI와 짝을 이루면 입구에는 설 수 있는 시대라고 생각한다. 다만 **결과 검증을 AI에게 맡기지 말 것** — 거기만큼은 인간의 일이다.

**Q. 실기가 없는데 의미 있나요?**
A. 나는 있다고 생각하고 계속하고 있다. 이유는 3가지. ①관측을 실기 센서 구성에 맞춰 두면, 정책은 원리적으로 실기로 가져갈 수 있다(sim-to-real의 입구에는 서 있다). ②실기에서는 위험하고 비싼 실패(수천 번의 전도)는 시뮬레이션으로만 쌓을 수 있다. ③애초에 실기 개발 현장에서도, 지금은 시뮬레이션으로 먼저 돌리는 것이 표준 절차다. 다만, 시뮬레이션에서 완벽해도 실기에서 무너지는 요소(모델화되지 않은 마찰, 지연, 휨)는 확실히 있고, 거기는 미검증이라고 정직하게 말할 수밖에 없다.

**Q. AI에게 어디까지 맡기고, 당신은 뭘 했나요?**
A. 방향을 정한다·가설을 낸다·결과를 의심한다·그만둘 때를 정한다, 가 나. 코드를 쓴다·실험을 돌린다·수치를 집계한다, 가 AI다. 예컨대 "이벤트 카메라적인 시간 차분을 더한다"는 이쪽의 발안이고, "그 구현에서 원기둥 교차를 해석적으로 푼다"는 AI의 일. 반대로 "48mm 들어 올렸다"라는 보고를 곧이곧대로 믿지 않고 "반드시 영상으로 검증하고 나서 합격시킨다"라는 규칙을 깔아 두는 것이 이쪽의 일이며, 그 규칙에 따라 실제로 영상을 정밀 조사해 환상(초기화 버그에 의한 사출)임을 밝혀낸 것은 AI 자신이다. 역할 분담이 작동한 예로 마음에 든다.

**Q. 실패투성이라 싫어지지 않나요?**
A. 싫어지는 날도 있다. 다만, 이 분야의 실패는 "원인을 반드시 특정할 수 있는" 타입의 실패다(물리 엔진은 재현 가능하므로). 원인을 알 수 있는 실패는 자산이 된다 — 부록 A의 연대기가 실제로 그렇게 됐듯이. 참고로 가장 풀이 죽었던 것은, 3주 연속으로 각기 다른 꼼수를 발명당했을 때다.

**Q. 어디서부터 시작하면 되나요?**
A. 추천 경로: ① MuJoCo를 설치하고 Menagerie의 로봇을 화면에 띄운다(1일)→ ② 좋아하는 모델을 keyframe 자세로 세우고 물리를 돌린다(1일)→ ③ mujoco_playground의 사족보행 튜토리얼을 돌린다(며칠)→ ④ 자신의 "종목"을 하나 정하고 보상을 쓴다(여기서부터 늪). ④ 전에 본 기사의 부록 D(교훈집)를 읽으면, 늪의 깊이가 3할은 얕아질 것이다.

**Q. 아이나 학생도 할 수 있나요?**
A. 시뮬레이션 자체는 무료이므로, GPU가 없어도 CPU로 작은 실험은 할 수 있다(학습은 느려지지만, 사족보행 정도라면 현실적). 제 13 장의 자료집에, 보면 즐거운 입구(공식 동영상)부터 경진대회(ROBO-ONE은 개인 참가 가능)까지의 동선을 정리해 두었다.

**Q. 왜 운동회인가요?**
A. 경기에는 계측과 규율이 들어가기 때문이다(제 1 장). 그리고, 단순히 즐겁기 때문이다. 즐겁지 않으면 몇 주씩 계속되지 않는다.

**Q. 이 기사, 너무 길지 않나요?**
A. 맞다. 다만, 목차와 3코스 안내(서두)를 붙였으므로, 필요한 곳만 골라 읽을 수 있게는 해 두었다. 길이는 "하나의 놀이를 어디까지 팔 수 있는가"의 실험이라고 생각하고 봐 주기 바란다. 이것도 일종의 경기다.
