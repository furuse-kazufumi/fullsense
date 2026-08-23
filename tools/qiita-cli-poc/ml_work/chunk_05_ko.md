### B.1 종별 내역(실측 67 모델)

| 종별 | 수 | 대표 |
|---|---|---|
| 휴머노이드(이족) | 12 | Unitree G1/H1, Booster T1, Fourier N1, Apptronik Apollo, PAL Talos, Agility Cassie, Berkeley Humanoid, Robotis OP3, PND Adam Lite, ToddlerBot ×2 |
| 사족 | 8 | ANYmal B/C, Boston Dynamics Spot, Google Barkour v0/vB, Unitree A1/Go1/Go2 |
| 암(단완) | 22 | Franka Panda/FR3, KUKA iiwa14, UR5e/UR10e, Kinova Gen3, xArm7, ViperX 외 |
| 양팔 | 2 | ALOHA, Trossen WXAI |
| 이동 매니퓰레이터 | 7 | Hello Robot Stretch ×2, PAL TIAGo ×2, Google Robot, TidyBot, Rainbow RBY1 |
| 다지 핸드 | 6 | Shadow Hand, LEAP Hand, Allegro, Shadow DEX-EE 외 |
| 그리퍼 | 3 | Robotiq 2F-85 ×2, UMI Gripper |
| 드론 | 2 | Crazyflie 2, Skydio X2 |
| 근골격/생물 | 2 | MS-Human-700(700근), flybody(파리) |
| 기타 | 3 | 축구 키트, RealSense D435i(센서 자재), IIT SoftFoot(발 부품) |

![명감 통계](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig_roster_stats.png)
*그림: 67기의 종별·액추에이터 형·keyframe 유무의 실측 집계(재고 조사 JSON으로 작도)*

### B.2 재고 조사에서 보인 "움직이기 위한 지도"

![Go2 포트레이트](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_go2.png)
*그림: Unitree Go2(시뮬레이션 렌더)*

![Spot 포트레이트](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/portrait_spot.png)
*그림: Boston Dynamics Spot(시뮬레이션 렌더)*

- **사족 8기종은 모두 동형(자유도 18·구동 12).** 즉 학습 파이프라인 1개를 쓰면 8기종을 나란히 스위프할 수 있다. 사족 종목은 운동회의 단체 종목에 최적.
- **암 22개는 "넘어지지 않으므로", 역운동학(IK. 손끝의 목표 위치에서 관절각을 역산하는 계산)을 맞히기만 해도 즉시 데모를 만들 수 있다.** 미분 IK 라이브러리(mink, Apache-2.0)의 샘플이 사실상의 Menagerie 데모집이 되어 있다.
- **home 자세(keyframe)가 없는 모델이 19체.** 전 기체 선보이기의 첫 "소재 만들기"는, 선 자세의 자작이라는 다소 수수한 작업이다.
- **요주의 개체**: Cassie는 폐링크 기구로 GPU 병렬(MJX)에 제약. 다지 핸드는 건 구동이나 부족 구동(underactuated)으로 "관절 수와 지령 수가 일치하지 않는" 전제의 설계가 필요.
- **휴머노이드 12체에는, 토크 직결형(H1, Talos 등)과 위치 서보형(G1, T1 등)이 있다.** 본편의 H1 대응에서는, 토크형을 위치 서보화하는 어댑터를 써서 이 차이를 흡수했다(G1의 보상 11개조를 그대로 이식하기 위해).

### B.3 학습 자원의 2대 기둥과, 라이선스의 지뢰밭

OSS의 학습 환경은, (1) **MuJoCo Playground**(Apache-2.0. 사족·이족의 이동 9기종+매니퓰레이션 4기종의 학습 환경과 설정)와 (2) **LocoMuJoCo**(MIT. 22,000편 넘는 리타깃 완료 모션 배포, 휴머노이드 10+사족 4)가 2대 기둥으로, 상호 보완의 관계에 있다.

그리고 재고 조사 최대의 수확이 **모션 데이터의 라이선스 지도**였다.

| 데이터원 | 내용 | 라이선스 |
|---|---|---|
| AMASS | SMPL 통일의 대규모 모캡 집성 | **비상용 한정(상용 신경망 학습도 금지)** |
| LAFAN1(본 기사의 교사) | 4.6시간의 고품질 모캡 | **CC BY-NC-ND(비상용·개변 금지)** |
| CMU Mocap | 2,600+ 시퀀스 | **무료·상용 가능**(전매만 금지) |
| GMR(범용 리타기터) | SMPL-X/BVH/영상 → 로봇 18기종 | **MIT** |

취미의 운동회라면 LAFAN1으로 문제없지만, 이 기술을 제품에 가까이 가져간다면, **"CMU mocap(상용 가능) + GMR(MIT)"의 조합이 가장 깨끗한 계보**가 된다. 데이터의 라이선스는 코드의 라이선스보다 간과되기 쉽고, 게다가 나중에 갈아 끼우기 어렵다 — 이것도 산업 쪽의 감각이 도움이 된 지점이었다.

### B.4 전 67 모델 실측표

67기분의 "체격 측정 결과"다. nq=일반화 좌표의 수(자유도+쿼터니언분), nv=속도 자유도, nu=구동 지령의 수. 액추에이터 형의 의미는 본편과 B.2대로이고, 자유 관절이 "있음"인 기체는 전도가 있는(=밸런스가 종목이 되는) 기체다. keyframe은 동봉된 기준 자세. 전 행, 실제로 로드해 물리 스텝을 돌려서 얻은 값이다.

| 모델 | nq | nv | nu | 액추에이터 | 자유 관절 | keyframe | 메시 수 | 라이선스 |
|---|---|---|---|---|---|---|---|---|
| `agilex_piper` | 8 | 8 | 7 | position+kv×7 | 없음 | home | 82 | MIT |
| `agility_cassie` | 35 | 32 | 10 | motor×10 | 있음 | home | 25 | custom/see LICENSE |
| `aloha` | 16 | 16 | 14 | position×12, position+kv×2 | 없음 | neutral_pose | 24 | custom/see LICENSE |
| `anybotics_anymal_b` | 19 | 18 | 12 | position×12 | 있음 | 없음 | 46 | custom/see LICENSE |
| `anybotics_anymal_c` | 19 | 18 | 12 | position×12 | 있음 | 없음 | 24 | custom/see LICENSE |
| `apptronik_apollo` | 39 | 38 | 32 | position×32 | 있음 | stand | 44 | Apache-2.0 |
| `arx_l5` | 8 | 8 | 7 | position+kv×7 | 없음 | home | 10 | BSD |
| `berkeley_humanoid` | 19 | 18 | 12 | position+kv×12 | 있음 | home | 13 | custom/see LICENSE |
| `bitcraze_crazyflie_2` | 7 | 6 | 4 | motor×4 | 있음 | hover | 39 | MIT |
| `booster_t1` | 30 | 29 | 23 | position+kv×23 | 있음 | home | 24 | Apache-2.0 |
| `boston_dynamics_spot` | 19 | 18 | 12 | position+kv×12 | 있음 | home | 23 | BSD |
| `dynamixel_2r` | 2 | 2 | 2 | position+kv×2 | 없음 | 없음 | 15 | custom/see LICENSE |
| `flexiv_rizon4` | 7 | 7 | 7 | position+kv×7 | 없음 | home | 14 | Apache-2.0 |
| `flexiv_rizon4s` | 7 | 7 | 7 | position+kv×7 | 없음 | home | 14 | Apache-2.0 |
| `flybody` | 109 | 108 | 78 | position×64, motor×6, adhesion×8 | 있음 | key0 | 85 | Apache-2.0 |
| `fourier_n1` | 30 | 29 | 23 | motor×23 | 있음 | home | 29 | Apache-2.0 |
| `franka_emika_panda` | 9 | 9 | 8 | position+kv×8 | 없음 | home | 67 | Apache-2.0 |
| `franka_fr3` | 7 | 7 | 7 | position+kv×7 | 없음 | home | 36 | Apache-2.0 |
| `franka_fr3_v2` | 7 | 7 | 7 | position+kv×7 | 없음 | home | 37 | Apache-2.0 |
| `google_barkour_v0` | 19 | 18 | 12 | position+kv×12 | 있음 | standing | 14 | Apache-2.0 |
| `google_barkour_vb` | 19 | 18 | 12 | position+kv×12 | 있음 | home | 11 | Apache-2.0 |
| `google_robot` | 9 | 9 | 9 | position×9 | 없음 | 없음 | 47 | Apache-2.0 |
| `hello_robot_stretch` | 31 | 29 | 8 | motor×2, position+kv×3, position×3 | 있음 | 없음 | 67 | BSD |
| `hello_robot_stretch_3` | 41 | 38 | 10 | velocity×2, position+kv×3, position×5 | 있음 | home, stow | 85 | Apache-2.0 |
| `i2rt_yam` | 8 | 8 | 7 | position+kv×7 | 없음 | home | 17 | MIT |
| `iit_softfoot` | 93 | 93 | 1 | position×1 | 없음 | 없음 | 10 | custom/see LICENSE |
| `kinova_gen3` | 7 | 7 | 7 | position+kv×7 | 없음 | home, retract | 8 | custom/see LICENSE |
| `kuka_iiwa_14` | 7 | 7 | 7 | position+kv×7 | 없음 | home | 13 | BSD |
| `leap_hand` | 16 | 16 | 16 | position+kv×16 | 없음 | 없음 | 11 | custom/see LICENSE |
| `low_cost_robot_arm` | 6 | 6 | 6 | position+kv×6 | 없음 | home | 22 | Apache-2.0 |
| `ms_human_700` | 85 | 85 | 700 | muscle×700 | 없음 | init | 189 | Apache-2.0 |
| `pal_talos` | 51 | 50 | 32 | motor×32 | 있음 | key0 | 74 | Apache-2.0 |
| `pal_tiago` | 29 | 28 | 14 | motor×7, position×5, velocity×2 | 있음 | 없음 | 21 | Apache-2.0 |
| `pal_tiago_dual` | 32 | 31 | 25 | velocity×4, position×7, motor×14 | 있음 | 없음 | 25 | Apache-2.0 |
| `pndbotics_adam_lite` | 32 | 31 | 25 | motor×25 | 있음 | 없음 | 73 | MIT |
| `rainbow_robotics_rby1` | 35 | 34 | 26 | velocity×2, position+kv×24 | 있음 | 없음 | 47 | Apache-2.0 |
| `realsense_d435i` | 0 | 0 | 0 | — | 없음 | 없음 | 9 | Apache-2.0 |
| `rethink_robotics_sawyer` | 7 | 7 | 7 | position+kv×7 | 없음 | home | 49 | Apache-2.0 |
| `robot_soccer_kit` | 71 | 70 | 4 | velocity×3, position+kv×1 | 있음 | 없음 | 29 | custom/see LICENSE |
| `robotiq_2f85` | 15 | 14 | 1 | position+kv×1 | 있음 | 없음 | 8 | custom/see LICENSE |
| `robotiq_2f85_v4` | 13 | 12 | 1 | position+kv×1 | 있음 | 없음 | 8 | custom/see LICENSE |
| `robotis_op3` | 27 | 26 | 20 | position×20 | 있음 | 없음 | 48 | Apache-2.0 |
| `robotstudio_so101` | 6 | 6 | 6 | position+kv×6 | 없음 | 없음 | 18 | Apache-2.0 |
| `shadow_dexee` | 12 | 12 | 12 | motor×12 | 없음 | 없음 | 26 | Apache-2.0 |
| `shadow_hand` | 31 | 30 | 20 | position×20 | 있음 | 없음 | 13 | Apache-2.0 |
| `sharpa_wave` | 22 | 22 | 22 | position+kv×22 | 없음 | 없음 | 54 | Apache-2.0 |
| `skydio_x2` | 7 | 6 | 4 | motor×4 | 있음 | hover | 1 | Apache-2.0 |
| `stanford_tidybot` | 18 | 18 | 11 | position+kv×11 | 없음 | home, retract | 20 | MIT |
| `tetheria_aero_hand_open` | 16 | 16 | 7 | position×7 | 없음 | home | 27 | Apache-2.0 |
| `toddlerbot_2xc` | 51 | 50 | 30 | motor×30 | 있음 | home | 47 | MIT |
| `toddlerbot_2xm` | 51 | 50 | 30 | motor×30 | 있음 | home | 47 | MIT |
| `trossen_vx300s` | 8 | 8 | 7 | position×7 | 없음 | home | 10 | custom/see LICENSE |
| `trossen_wx250s` | 8 | 8 | 7 | position+kv×7 | 없음 | home | 10 | custom/see LICENSE |
| `trossen_wxai` | 16 | 16 | 14 | position×14 | 없음 | left/, right/ | 84 | BSD |
| `trs_so_arm100` | 6 | 6 | 6 | position+kv×6 | 없음 | home, rest | 18 | Apache-2.0 |
| `ufactory_lite6` | 6 | 6 | 6 | position+kv×6 | 없음 | home | 14 | custom/see LICENSE |
| `ufactory_xarm7` | 13 | 13 | 8 | position+kv×8 | 없음 | home | 16 | custom/see LICENSE |
| `umi_gripper` | 8 | 8 | 7 | position×1, position+kv×6 | 없음 | 없음 | 6 | MIT |
| `unitree_a1` | 19 | 18 | 12 | position×12 | 있음 | home | 5 | BSD |
| `unitree_g1` | 36 | 35 | 29 | position+kv×29 | 있음 | stand | 35 | custom/see LICENSE |
| `unitree_go1` | 19 | 18 | 12 | position×12 | 있음 | home | 5 | BSD |
| `unitree_go2` | 19 | 18 | 12 | motor×12 | 있음 | home | 16 | custom/see LICENSE |
| `unitree_h1` | 26 | 25 | 19 | motor×19 | 있음 | home | 21 | custom/see LICENSE |
| `unitree_z1` | 6 | 6 | 6 | position+kv×6 | 없음 | home | 7 | BSD |
| `universal_robots_ur10e` | 6 | 6 | 6 | position+kv×6 | 없음 | home | 20 | custom/see LICENSE |
| `universal_robots_ur5e` | 6 | 6 | 6 | position+kv×6 | 없음 | home | 20 | custom/see LICENSE |
| `wonik_allegro` | 23 | 22 | 16 | position×16 | 있음 | 없음 | 11 | custom/see LICENSE |


## 부록 C: 센서 도감 — 스펙·장단점·퓨전·시장 동향

관측 설계는 센서 선정이다, 라는 본편의 주장을 지탱하는 자료편이다.

![센서 비교 레이더](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/fig2_sensor_compare.png)
*그림: 주요 5센서의 특성 비교(부록 C의 실제 스펙 표에서의 정성적 요약). 만능인 센서는 없다 — 그래서 섞게(퓨전) 된다*

수치는 2026-08 시점의 조사이고, 각 항목에 출처를 달았다(공식 데이터시트 우선. 확인하지 못한 값은 "미확인"인 채로 남겨 두었다 — 추측으로 메우기보다, 안 메워져 있음을 알 수 있는 쪽이 자료로서 성실하기 때문이다).

### 1. 주요 센서의 스펙과 장단점

**기사용 요약(5행)**

1. 휴머노이드의 "눈"은 1종류로는 성립하지 않는다 — LiDAR(정확한 거리), 깊이 카메라(밀한 근거리 3D), IMU(자세), 관절 인코더(자기 몸)를 겹쳐야 비로소 세계가 보인다.
2. Livox Mid-360은 360°×(-7°〜+52°) FOV·20만 점/초·265 g·실세 $750〜900으로, 연구용 로봇 LiDAR의 사실상 표준이 됐다(한 자릿수 위의 산업급 Hesai XT16은 $6,650).
3. Intel RealSense D435i는 87°×58° FOV의 액티브 IR 스테레오+IMU 내장 $334로, 2025년에 Intel에서 스핀오프한 RealSense Inc.가 D500 계열로 갱신 중.
4. 이벤트 카메라(Sony IMX636)는 μs급의 시간 분해능과 120 dB(저조도 조건)의 다이내믹 레인지를 갖지만, 평가 키트는 여전히 수십만 엔급으로 "다음 주역 후보" 단계.
5. IMU는 등급에 따라 가격이 3자릿수 차이 나는(민생 몇 달러 → 전술급 $8,000 초과) 한편, GPS 없는 60초의 위치 오차는 400 m → 5 m로 2자릿수 줄어든다 — 다리 로봇은 민생〜산업급 IMU+타 센서 융합으로 싸우는 것이 정석이다.

#### 1.0 횡단 비교표(휴머노이드 탑재 관점)

| 센서 | 원리(1행) | 장점 | 약점 | 대표 기종과 가격대 | 전형 용도 |
|---|---|---|---|---|---|
| 회전식/반구 LiDAR | 레이저 비행 시간(ToF)으로 거리를 직접 잰다 | 거리 정밀도(cm급)·어둠·넓은 FOV | 비/안개/눈, 검은 저반사면, 유리 | Livox Mid-360 $749〜/ Unitree L2 $419 / Hesai XT16 $6,650 | SLAM·장애물 회피·전 주위 지각 |
| 깊이 카메라(액티브 IR 스테레오) | IR 패턴 투광+좌우 카메라 시차로 깊이 | 근거리의 밀한 3D, 저렴, RGB 동시 취득 | 직사광(IR이 진다), 원거리, 투명/거울면 | RealSense D435i $334 / Orbbec Gemini 335 $264 | 발밑의 지형·매니퓰레이션 |
| 스테레오 카메라(패시브) | 좌우 카메라의 시차만으로 깊이(+근년은 뉴럴 깊이) | 실외·긴 기선으로 중거리, 투광 불요 | 무텍스처 면(흰 벽), 어두운 곳 | ZED 2i $499〜 / ZED X $549〜(검색 결과값) | 실외 내비·차량형 지각 |
| ToF 카메라 | 변조광의 위상차로 전 화소 동시에 거리 | 실내의 밀한 깊이, 넓은 FOV | 직사광, 검은 저반사, 멀티패스 | Orbbec Femto Bolt $418 | 실내 매핑·제스처 |
| 이벤트 카메라(DVS) | 화소마다 휘도 변화의 순간만 비동기 출력 | 고속 운동·HDR(역광/터널)·저지연 | 정지 장면(아무것도 안 나옴), 기존 CV 자산을 쓸 수 없음 | Prophesee EVK4 ≈$5,400(대리점)/ iniVation DVXplorer €3,900 | 고속 회피·드론 검지·진동 감시 |
| IMU(MEMS) | 각속도와 가속도의 관성 계측 | 고레이트(kHz급)·자기 완결 | 드리프트(단독으로는 위치가 발산) | BMI088 몇 달러급 / ADIS16470 $482 / HG4930 $8,300〜 | 자세 추정·LIO/VIO의 척추 |
| 6축 F/T 센서 | 스트레인 게이지 등으로 3힘+3모멘트 | ZMP 직접 산출·힘 제어 | 고가·충격/EMI에 약함 | ATI Axia80(견적제)/ Robotiq FT 300-S 키트 $5,720 | 발목의 바닥 반력·파지력 제어 |
| 촉각 스킨 | 겔 변형의 촬상(시촉각)이나 자기식 3축 분포 | 미끄럼 검지·미세 형상·재질 | 면적당 비용·배선·내구 | GelSight Mini $499 / Meta Digit 360(가격 미공표) | 손끝의 파지·접촉 조작 |
| 초음파 | 음파의 왕복 시간 | 투명물·유리도 보임, 몇 달러 | 분해능이 거칠고, 지향성이 넓음 | HC-SR04 몇 달러 | 근접 범퍼적 용도 |
| GNSS/RTK | 위성 측위+기준국 보정 | 실외에서 절대 위치 cm급 | 실내·도시 협곡은 불가 | u-blox ZED-F9P 보드 $259.95 | 실외 내비·그라운드 트루스 |
| 관절 인코더 | 자기/광학으로 관절각을 직독 | 고분해능(17〜23 bit)·저지연 | 외계는 전혀 안 보임 | (기체 내장) | 고유수용 감각=제어의 토대 |

---

#### 1.1 LiDAR

##### Livox Mid-360(최중요·상세)

방식: 비반복 스캔(non-repetitive scanning)+회전 기구에 의한 수평 360° 커버. 시간 경과와 함께 FOV 내의 점 충전율이 올라가는 Livox 독자 방식.

| 항목 | 값 | 출처 |
|---|---|---|
| FOV | 수평 360° / 수직 **-7°〜+52°**(공식 확인 완료) | https://www.livoxtech.com/mid-360/specs |
| 점수/초 | 200,000 pts/s(first return) | 상동 |
| 측거 범위 | 40 m @ 반사율 10% / 70 m @ 반사율 80%(모두 환경광 100 klx) | 상동 |
| 측거 편차(1σ) | ≤2 cm @ 10 m(지근 0.2 m에서는 ≤3 cm) | 상동 |
| 각도 정밀도 | < 0.15°(1σ) | 상동 |
| 질량 | 265 g | 상동 |
| 소비 전력 | 평균 6.5 W(자기 가열 모드 시 피크 14 W) | 상동 |
| 프레임 레이트 | 10 Hz(typical) | 상동 |
| 파장 | 905 nm | 상동 |
| IMU | 내장(ICM40609) | 상동 |
| 접속 | 100BASE-TX Ethernet, PTPv2/GPS 시각 동기 대응 | 상동 |
| 가격 | 공식 샘플 가격 $749(2023-01 발매 시. DJI 스토어 검색 결과에서도 $749) | https://www.livoxtech.com/news/mid360_launch / https://store.dji.com/product/livox-mid-360 |
| 실세 가격 | 미국 대리점 $899(backorder), AliExpress 실세 $480〜550(2025년의 구매 보고, 비공식) | https://www.roboticscenter.ai/store/product/livox-dji-livox-mid-360 / https://www.aliexpress.com/s/wiki-ssr/article/livox-mid-360-price-usd-2025 |

- 장점: 저가격·경량·IMU 내장·전 주위 FOV. FAST-LIO2 / Point-LIO에 공식 설정 파일이 있어(후술), 상자에서 꺼내면 바로 LIO가 돈다.
- 약점: 수직 -7°까지밖에 아래를 못 본다(발밑 바로 아래는 깊이 카메라로 보완하는 것이 G1 방식). 905 nm 광학식이므로 비·안개·검은 저반사면은 원리적으로 불리.
- 전형 용도: 사족/휴머노이드의 360° 근접 지각·실내외 SLAM. 연구용 로봇의 사실상 표준.
- 보충: Livox는 그 밖에 Avia(70.4°×77.2°, 240k pts/s, 450 m @ 80%, 498 g — 드론 측량용 https://www.livoxtech.com/avia/specs)、HAP(차량 탑재, 120°×25°, 452k pts/s, 150 m @ 10% — https://www.livoxtech.com/hap/specs)을 전개.

##### 경쟁 LiDAR 비교

| 제품 | 방식 | 레인지 @10% 반사율 | 점수/초 | 질량 | 실세 가격 | 출처 |
|---|---|---|---|---|---|---|
| Unitree L1 | 반구 "4D LiDAR" 360°×90° | 미확인(최대 30 m) | 21,600 | 230 g | **$249**(공식) | https://shop.unitree.com/products/unitree-4d-lidar-l1 |
| Unitree L2 | 반구 360°×96° | 미확인(최대 30 m) | 64,000(공식. 판매점에 128,000 표기도 있어 불일치→공식값 채용) | 미확인 | **$419**(공식) | https://shop.unitree.com/products/unitree-4d-lidar-l2 |
| Livox Mid-360 | 비반복 360°×59° | 40 m | 200,000 | 265 g | $749〜899 | 상기 |
| Hesai JT16 | 16ch 미니 돔 360°×40° | 30 m | 48,000 | 199.7 g / 4.3 W | €599(세일, 통상 €739) | https://www.hesaitech.com/product/jt16/ / https://openelab.io/products/hesai-jt16-mini-3d-lidar |
| Hesai XT16 | 16ch 기계식 회전 360°×30° | 미확인(0.05〜120 m. 형제기 XT32M은 80 m @10%) | 320,000 | 800 g | **$6,650**(미국 대리점) | https://www.hesaitech.com/product/xt16-32-32m/ / https://robostore.com/products/hesai-xt16-3d-lidar |
| Ouster OS0 | digital LiDAR(SPAD+ASIC) 최대 128ch, 수직 90° | 35 m | 10,400,000 | 미확인 | 문의 필요(참고: OS1-32 발표 시 $8,000) | https://ouster.com/products/hardware/os0-lidar-sensor |
| Ouster OS1 | 동 128ch, 수직 45° | 90 m | 10,400,000 | 미확인 | 문의 필요 | https://ouster.com/products/hardware/os1-lidar-sensor / https://www.geoweeknews.com/articles/32-channel-lidar-for-8k-ousters-newest-lidar-finds-a-sweet-spot/ |

각론:

- **Hesai XT16**: 정밀도 ±1 cm(accuracy)/ 0.5 cm(1σ precision), 제로 블라인드 스폿이 세일즈 포인트인 산업 그레이드. AGV/AMR·cm급 실내외 내비용(https://www.hesaitech.com/product/xt16-32-32m/)。
- **Hesai JT16**: CES 발표의 로봇용 미니 돔. 200 g·IP6K6로 Mid-360의 직접 경쟁. 청소 로봇·배송 로봇 겨냥.
- **Ouster OS 시리즈**: 수광 쪽을 SPAD+커스텀 ASIC에 집적한 "digital LiDAR". 점밀도 10.4 M pts/s는 Mid-360의 50배지만, 가격·질량은 다른 클래스. OS0의 수직 90° FOV는 창고 내 로봇의 바닥〜천장 지각에 강하다. 현행 Rev7/8의 정밀도·질량·전력·실판매가는 공식 페이지 비게재(미확인, 데이터시트는 https://ouster.com/downloads )。
- **Velodyne의 현황(사실 확인 완료)**: Velodyne은 2023-02-10에 Ouster와 대등 합병을 완료했고, 존속 회사는 Ouster(NYSE: OUST). 구 Velodyne 주식은 상장 폐지(1주 = Ouster 0.8204주). 출처: https://investors.ouster.com/news-releases/news-release-details/ouster-and-velodyne-complete-merger-equals-accelerate-lidar / https://www.therobotreport.com/lidar-makers-ouster-velodyne-complete-merger/

#### 1.2 깊이 카메라

##### Intel RealSense D435i(최중요·상세)

방식: 액티브 IR 스테레오(IR 패턴 투광+좌우 IR 카메라의 시차).

| 항목 | 값 | 출처 |
|---|---|---|
| 깊이 FOV | **87°×58°(공식 확인 완료)**. 데이터시트 정밀값 87°±3° × 58°±1°(대각 95°±3°) | https://www.intel.com/content/www/us/en/products/sku/190004/intel-realsense-depth-camera-d435i/specifications.html / https://cdrdv2-public.intel.com/841984/Intel-RealSense-D400-Series-Datasheet.pdf |
| 깊이 범위 | 이상 0.3〜3 m(Min-Z 약 28 cm, 848×480 시 0.105 m). 3 m 초과도 가능하나 정밀도 저하 | https://www.realsenseai.com/products/depth-camera-d435i/ |
| 깊이 해상도/fps | 최대 1280×720 / 최대 90 fps | 상동 |
| 깊이 정밀도 | <2% @ 2 m | 상동 |
| RGB | 1920×1080 @30 fps(롤링 셔터) | 상동 |
| IMU | **Bosch BMI055(6축) 내장 — 확인 완료** | https://github.com/realsenseai/librealsense/blob/master/doc/d435i.md |
| 질량 | 약 72 g(대리점값. 공식 현행 페이지 비게재) | https://framos.com/products/3d/3d-cameras/depth-camera-d435i-bulk-22610/ |
| 치수/접속 | 90×25×25 mm, USB-C 3.1 Gen 1 | https://www.realsenseai.com/products/depth-camera-d435i/ |
| 가격 | **$334.00(공식 스토어)** | https://store.realsenseai.com/buy-intel-realsense-depth-camera-d435i.html |

RealSense 사업의 현황:

- 2021년에 Intel이 사업 축소를 발표했지만 D400 계열은 계속. **2025-07-11에 RealSense Inc.로서 Intel에서 스핀오프 완료**, Series A로 $50M 조달(Intel Capital, MediaTek Innovation Fund 참여). 출처: https://www.realsenseai.com/news-insights/news/realsense-completes-spin-out-from-intel-raises-50-million-to-accelerate-ai-powered-vision-for-robotics-and-biometrics/ / https://www.tomshardware.com/tech-industry/realsense-completes-spin-out-from-intel-gets-usd50-million-in-funding-from-intel-capital-and-mediatek
- 독립 후 제1탄 = **D555**(D500 계열): Vision SoC V5(5 TOPS) 탑재, PoE 급전+글로벌 셔터. 출처: https://www.vision-systems.com/embedded/article/55303384/intel-completes-realsense-spinoff
- 동사는 "세계의 AMR/휴머노이드의 60%에 채용"이라고 주장(자사 발표값).

##### 경쟁 깊이 카메라

| 제품 | 방식 | 깊이 스펙 | 가격 | 출처 |
|---|---|---|---|---|
| Orbbec Gemini 335 | 액티브 스테레오(MX6800 ASIC) | 0.1〜20 m+, 1280×800@30fps, FOV 90°×65° | **$264**(공식 스토어) | https://store.orbbec.com/products/gemini-335 |
| Orbbec Gemini 335L | 동·기선 95 mm·IP65 | 정밀도 ≤0.8% @ 2 m | $359 | https://www.hackster.io/news/orbbec-unveils-the-robust-fakra-connectable-gemini-335lg-depth-camera-for-autonomous-robots-and-more-e23d922b5158 |
| Orbbec Femto Bolt | Microsoft iToF(Azure Kinect와 동일 깊이 기술) | 0.25〜5.46 m, WFOV 120°×120°, RGB 4K, IMU 내장 | **$418**(공식 스토어) | https://store.orbbec.com/products/femto-bolt |
| Stereolabs ZED 2i | 패시브 스테레오+Neural Depth | 0.2〜20 m, 110° 광각, IMU+기압+자기 | $499〜(검색 결과값, 재확인 필요) | https://store.stereolabs.com/products/zed-2i/ |
| Stereolabs ZED X | 동(Gen2)+글로벌 셔터 | 0.3〜20 m(2.2mm)/1〜35 m(4mm), GMSL2 접속(Jetson 전제) | $549〜599(검색 결과값) | https://static.generation-robots.com/media/zed-x-datasheet-v1.2.pdf |

- **Azure Kinect DK의 EOL(사실 확인 완료)**: Microsoft는 2023-08에 생산 종료를 발표, 2023년 10월 판매 종료. SDK 리포지토리는 2024-08-22 아카이브. 후계로서 Microsoft 공식 제휴 하에 Orbbec Femto Bolt/Mega가 iToF 기술을 라이선스 구현(Azure Kinect와 동일 깊이 모드, K4A API 호환 래퍼 있음). 출처: https://hackaday.com/2023/08/26/microsoft-discontinues-kinect-again/ / https://github.com/microsoft/Azure-Kinect-Sensor-SDK/issues/1971 / https://www.orbbec.com/microsoft-collaboration/ / https://www.orbbec.com/documentation/comparison-with-azure-kinect-dk/
- Orbbec SDK는 ROS1/ROS2 네이티브 대응(https://store.orbbec.com/products/gemini-335le)。

#### 1.3 이벤트 카메라(DVS)

원리(1행): 각 화소가 독립·비동기로 "휘도의 로그 변화가 임곗값을 넘은 순간"만을 (x, y, 타임스탬프, 극성)의 이벤트로 출력한다 — 프레임을 찍지 않는다. 출처: https://www.prophesee.ai/event-based-sensor-imx636-sony-prophesee/

##### Prophesee / Sony IMX636

| 항목 | 값 | 출처 |
|---|---|---|
| 개발 | Sony(적층 BSI 프로세스) × Prophesee(이벤트 화소) 공동 개발 | https://www.prophesee.ai/2022/04/13/new-sony-imx636es-hd-sensor-realized-in-collaboration-between-sony-and-prophesee/ |
| 해상도 / 화소 피치 | **1280×720 / 4.86 μm(확인 완료)** | https://www.prophesee.ai/wp-content/uploads/2024/05/IMX636-Product-Brief-2024-v3.0.pdf |
| 시간 분해능 | 타임스탬프 정밀도 1 μs, 화소 지연 <100 μs @1000 lux(등가 >10k fps) | 상동 / https://www.prophesee.ai/event-camera-evk4/ |
| 다이내믹 레인지 | **공식 표기는 >86 dB(typ)/ >120 dB(저조도 조건 0.08〜100,000 lux)** — "120 dB"는 측정 조건부의 값 | https://support.prophesee.ai/portal/en/kb/articles/evk4-hd-product-brief |
| 최대 이벤트 레이트 | 1.06 Geps급(Sony 공표) | https://www.sony-semicon.com/en/products/is/industry/evs.html |
| SDK | Metavision SDK(OSS판 OpenEB) | https://github.com/prophesee-ai/openeb |
| 평가 키트 EVK4 | IMX636, USB 3.0, 30×30×36 mm, 40 g. 공식 직판은 견적제(미확인), 대만 대리점 실판매 NT$175,000 ≈ **$5,400** | https://www.prophesee.ai/event-camera-evk4/ / https://store.edomtech.com/products/evk4 |

##### iniVation DVXplorer

| 항목 | 값 | 출처 |
|---|---|---|
| 해상도 | VGA 640×480 | https://docs.inivation.com/hardware/current-products/dvxplorer.html |
| 다이내믹 레인지 | 최대 110 dB | 상동 |
| 시간 분해능 | 200 μs, 지연 <1 ms, 최대 165 Meps | 상동 |
| 가격 | **€3,900(상용)/ €3,400(아카데믹)** | https://shop.inivation.com/collections/dvxplorer |

- 장점: 고속 운동(모션 블러 없음)·HDR 환경(터널 출입구·역광)·저소비·μs급 저지연.
- 약점: 정지 장면은 원리적으로 아무것도 안 보인다(자기 운동이나 액티브 조명이 필요)/프레임 전제의 CV·딥러닝 자산을 직접 쓸 수 없어 표현 변환(voxel grid, time surface 등)이 필요/이벤트 레이트가 장면 의존으로 버스트적(대역·처리계는 워스트 케이스 설계).
- 데이터 레이트의 성질: 출력은 장면 의존·희소. 정지에서 거의 제로, 격렬한 움직임+고텍스처에서 Geps급까지 스파이크할 수 있다.
- 전형 용도: 고속 장애물 회피, 드론 검지·추적, 고속 VO/SLAM, 진동 감시, 저지연 파지.

#### 1.4 IMU(MEMS) — 등급과 드리프트

업계 관용의 4등급. 위치 오차는 시간의 약 3제곱으로 성장하고, 자이로의 in-run bias instability가 지배항(https://www.vectornav.com/resources/detail/what-is-an-inertial-navigation-system)。

| 등급 | Gyro bias instability 기준 | GPS 없는 관성 항법 60초의 위치 오차 | 대표 용도 |
|---|---|---|---|
| 민생급 | ~100 °/h | **400 m** | 스마트폰·드론 FC·호비 |
| 산업급 | ~10 °/h | **40 m** | 로봇·농기계·AGV |
| 전술급 | ~1 °/h | **5 m** | UAV·군용·측량 |
| 항법급 | ~0.01 °/h | **50 cm** | 항공기·함선·잠수함 |

(출처: VectorNav 상기. 등급 정의는 메이커 간에 엄밀한 표준이 없는 점에 주의 — https://ez.analog.com/mems/w/documents/4111/what-does-tactical-grade-mean-for-a-mems-imu )

대표 디바이스 실스펙:

| 디바이스 | 등급 | Gyro bias instability | 노이즈 | 가격 | 출처 |
|---|---|---|---|---|---|
| Bosch BMI088 | 민생(드론용) | 데이터시트 비기재(포럼 답변으로 <2 °/h로 안내 ※flyer 값) | gyro 0.014 °/s/√Hz | 몇 달러급(단가 미확인) | https://www.bosch-sensortec.com/media/boschsensortec/downloads/datasheets/bst-bmi088-ds001.pdf |
| TDK ICM-42688-P | 민생(FPV 정번) | 데이터시트 비기재 | gyro 2.8 mdps/√Hz | 몇 달러급(미확인) | https://product.tdk.com/system/files/dam/doc/product/sensor/mortion-inertial/imu/data_sheet/ds-000347-icm-42688-p-v1.6.pdf |
| ADI ADIS16470 | 산업급 | **8 °/h** | 0.008 °/s/√Hz | **$481.53**(DigiKey) | https://www.analog.com/media/en/technical-documentation/data-sheets/adis16470.pdf / https://www.digikey.com/en/products/detail/analog-devices-inc/ADIS16470AMLZ/7932982 |
| ADI ADIS16490 | 전술급 | **1.8 °/h** | ARW 0.09 °/√h | 수천 달러급(미확인) | https://www.analog.com/media/en/technical-documentation/data-sheets/adis16490.pdf |
| Honeywell HG4930 | 전술급 | **0.25 °/h** | ARW 0.04 °/√h | **$8,300〜$13,500**(DigiKey 형번별) | https://media.digikey.com/pdf/data%20sheets/honeywell%20pdfs/hg4930_perfandenvriomanual_jul2017.pdf / https://www.digikey.com/en/products/detail/honeywell-aerospace/HG4930CA51/6562993 |

- 정리: 민생→전술로 가격 3자릿수, bias instability 2자릿수 이상 개선. GPS 없는 60초에 400 m vs 5 m.
- 채용례: Pixhawk 6X(Rev 8)는 ICM-45686 ×3의 3중 리던던시 — 민생급 IMU의 리던던시 구성+퓨전으로 운용(https://www.getfpv.com/electronics/flight-controllers/holybro-pixhawk-6x-fc-v2a-standard-set-icm-45686.html)。Unitree G1은 "6축 IMU"라고만 공표, 형번·등급은 미확인(https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications)。
- 전형 용도: 자세 추정, LIO/VIO의 predict 스텝. 다리 로봇은 착지 충격(고대역·포화) 대책이 열쇠(후술 Point-LIO).

#### 1.5 힘/토크·발바닥·촉각

##### 6축 F/T 센서

| 제품 | 원리 | 스펙 | 가격 | 출처 |
|---|---|---|---|---|
| ATI(현 Novanta)Axia80 | 실리콘 스트레인 게이지(박 게이지 대비 75배의 신호 강도) | 힘 ~500 N / 토크 ~20 Nm, 과부하 내성 5〜12.5배, EtherCAT/Ethernet | 견적제(미확인. 시장에서는 수천 달러급으로 알려짐) | https://ati.novanta.com/product/axia80-force-torque-sensor-kit/ |
| Robotiq FT 300-S | "wear-free sensing technology"(정전용량식인지는 공식 명기 없음=미확인) | ±300 N / ±30 Nm, 100 Hz, IP65, 과부하 500% | 키트 **$5,720**(대리점) | https://robotiq.com/products/ft-300-force-torque-sensor / https://www.kingbarcode.com/FTS-300-S-KIT-001 |

##### 휴머노이드 발바닥의 접지 검지 — 3방식 비교

| 방식 | 얻어지는 정보 | 장점 | 단점 | 채용례 |
|---|---|---|---|---|
| 발목 6축 F/T | 바닥 반력 3힘+3모멘트 → ZMP 직접 산출 | ZMP 제어에 최적·고정밀 | 고가·무겁고·착지 충격/EMI에 약함 | ASIMO, HRP-4 등(연구 문헌 기반: https://www.researchgate.net/publication/257672554_Signal_Processing_and_Application_of_Six-axis_ForceTorque_Sensor_Integrated_in_Humanoid_Robot_Foot ) |
| 발바닥 분포압(FSR/압력 매트) | 법선 방향의 압력 분포 | 저렴·얇음·접지면 형상을 알 수 있음 | 전단력/모멘트 불가, 히스테리시스 | 호비/연구기에서 널리 사용(개별 1차 소스 미확인) |
| 관절 전류(토크) 추정 | 관절 토크에서 외력 추정 | 추가 센서 불요·비용 0 | 감속기 마찰로 정밀도 한계 | 근년의 양산 휴머노이드의 주류 경향 |

- **Unitree G1**: 공표 사양에 발바닥 힘 센서의 기재 없음(센서 표는 Depth 카메라/3D LiDAR/마이크/관절 인코더/IMU뿐) → 접지 판정은 관절 쪽 추정으로 보임(단정은 미확인). 출처: https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications

##### 촉각 스킨

| 제품 | 원리 | 상황·가격 | 출처 |
|---|---|---|---|
| GelSight Mini | 시촉각(겔 변형을 카메라 촬상) | **$499**(교환 겔 $49)로 일반 판매 중. 연구에서 최보급 | https://www.gelsight.com/gelsightmini/ |
| Meta Digit 360 | 손끝 전 주위의 시촉각+멀티모달(1 mN의 힘 검출) | GelSight 제조. 2024-10 발표, 가격 미공표(미확인) | https://www.businesswire.com/news/home/20241031980322/en/GelSight-and-Meta-AI-Introduce-Digit-360-Tactile-Sensor |
| uSkin(XELA Robotics) | 자기식 3축(법선+전단) 고밀도 분포 | 상용 전개 중(2025-12 Tesollo DG-5F 통합, CES 2026 데모). 가격 미공표 | https://roboticsandautomationnews.com/2025/12/04/xela-robotics-adds-high-precision-tactile-sensing-to-tesollo-robot-hand/97352/ |

#### 1.6 기타(간결)

- **ToF 카메라**: 변조광의 위상차로 전 화소 동시 측거. Orbbec Femto Bolt는 계통 오차 <11 mm + 거리의 0.1%, σ≤17 mm(https://www.orbbec.com/products/tof-camera/femto-bolt/)。실내의 밀한 깊이에 강하고, 직사광·검은 저반사·멀티패스가 약점.
- **초음파**: HC-SR04로 레인지 2 cm〜4 m, 분해능 0.3 cm, 몇 달러(https://www.dfrobot.com/blog-13482.html)。광학식이 어려워하는 투명물·유리에 반응하는 것이 차별화 포인트.
- **GNSS/RTK**: u-blox ZED-F9P는 RTK 시 수평 1 cm(단독 2.5 m). SparkFun 보드로 $259.95(https://www.sparkfun.com/sparkfun-gps-rtk2-board-zed-f9p-qwiic-gps-15136.html)。cm급에는 기준국이나 NTRIP 보정이 필수. 실외 실험의 그라운드 트루스 취득에 최적.
- **관절 인코더**: 절댓값식 17 bit = 131,072 분할/회전, 23 bit = 약 839만 분할(https://www.dynapar.com/knowledge/encoder-basics/encoder-resolution/single-turn-vs-multi-turn-encoders/)。휴머노이드 관절은 절댓값식이 주류. Unitree G1은 각 관절에 듀얼 인코더(모터 쪽+출력 쪽)(https://robostore.com/blogs/news/unitree-g1-edu-ultimate-technical-specifications)。

---

### 2. 멀티센서 퓨전 기법의 정리

**기사용 요약(5행)**

1. 퓨전의 고전은 "각 센서의 오차 특성(공분산)으로 가중한 축차 베이즈 추정" = 칼만 필터(EKF/UKF)이며, ROS의 robot_localization이 사실상의 표준 구현.
2. LiDAR-관성 오도메트리(LIO. 이동량을 적산해 자기 위치를 내는 기법)는 팩터 그래프의 LIO-SAM(2020) → 반복 EKF+ikd-Tree의 FAST-LIO2(2021, 100 Hz) → 점 단위 갱신의 Point-LIO(2023, 4〜8 kHz)로 진화했고, 모두 Mid-360 대응 설정이 공식 제공되고 있다.
3. 학습 기반에서는, 카메라+LiDAR를 조감(BEV) 특징 공간에서 섞는 BEVFusion(2022)과, 훈련 중에 센서 1계통을 통째로 떨어뜨리는 modality dropout에 의한 강건화가 주요 조류.
4. 다리 로봇의 금자탑은 teacher-student 증류: 시뮬레이션 안의 특권 정보(접촉력·지형)를 보는 교사를, 실기에서 쓸 수 있는 고유수용 감각만의 학생에게 증류한다(Lee et al. 2020 / Miki et al. 2022, Science Robotics).
5. 실기 휴머노이드는 "LiDAR+깊이 카메라파"(Unitree, Agility)와 "카메라 순화파"(Tesla, Figure)로 양분되며, 양산판 Atlas의 LiDAR 철거 보도는 카메라파로의 합류를 시사한다.

#### 2.1 고전: 칼만 필터와 팩터 그래프

##### EKF / UKF

| 항목 | EKF | UKF |
|---|---|---|
| 비선형의 취급 | 야코비안으로 1차 선형화 | 시그마 점을 비선형 함수에 그대로 통과(Unscented 변환) |
| 장점 | 가볍다·실적 방대 | 2차 정밀도·야코비안 도출 불요 |
| 단점 | 강한 비선형·큰 자세 오차에서 발산하기 쉬움 | 약간 무겁다 |

- 전형 구성: IMU(고레이트·드리프트)를 예측으로, 인코더·GNSS(절대·저레이트)를 관측으로 통합. ROS 표준 구현 = robot_localization(EKF/UKF 양대응): https://github.com/cra-ros-pkg/robot_localization
- 본질: 상보적인 센서를 오차 공분산으로 가중해 섞는 축차 베이즈 추정.
- 서지: Kalman 1960이 원전, UKF는 Julier & Uhlmann 1997(1차 URL 미확인).

##### 팩터 그래프 / LIO 계보

| 기법 | 연도/저자 | 요점 | 성능 주장 | URL |
|---|---|---|---|---|
| GTSAM | Georgia Tech Borg Lab(iSAM2는 Kaess et al., IJRR 2012) | 팩터 그래프+베이즈 트리의 C++ 기반. IMU 사전 적분 factor 제공 | iSAM2로 인크리멘털 갱신 | https://github.com/borglab/gtsam |
| LIO-SAM | 2020 IROS / Tixiao Shan 등(MIT/Stevens) | LiDAR-관성을 팩터 그래프로 정식화(GTSAM 사용). 루프 클로저·GPS를 factor로 추가 가능 | 실시간 고정밀 궤적+지도 | https://github.com/TixiaoShan/LIO-SAM / https://arxiv.org/abs/2007.00258 |
| FAST-LIO2 | 2021 arXiv / 2022 T-RO / Wei Xu, Fu Zhang 등(HKU MARS) | 특징 추출 없이 생점군을 직접 레지스트레이션. tightly-coupled 반복 EKF+증분 kd 트리 ikd-Tree | "SOTA 대비 고정밀이면서 대폭 낮은 계산 부하" "최대 100 Hz" | https://github.com/hku-mars/FAST_LIO / https://arxiv.org/abs/2107.06829 |
| Point-LIO | 2023 Advanced Intelligent Systems / He, Xu, Zhang 등(HKU MARS) | 점 단위로 상태를 갱신해 프레임 내 왜곡을 원리적으로 배제. IMU를 "출력"으로 취급해 포화 하에서도 추정 계속 | 4〜8 kHz 오도메트리, 각속도 75 rad/s의 격한 운동에서도 동작 | https://github.com/hku-mars/Point-LIO / https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202200459 |

- **Mid-360 대응**: FAST-LIO 리포지토리에 공식 `config/mid360.yaml`이 있고(https://github.com/hku-mars/FAST_LIO/blob/main/config/mid360.yaml)、Point-LIO도 같은 계열로 Mid-360 설정을 제공 — G1 표준 탑재의 Mid-360으로 그대로 LIO가 도는 에코시스템이 갖춰져 있다.
- 구분 사용의 상식: 루프 클로저·GPS 통합까지 원한다 → LIO-SAM / 계산 자원이 빠듯하다·고속 기동 → FAST-LIO2 / 다리 로봇의 발 접지 충격 같은 진동·격한 운동 → Point-LIO.

#### 2.2 학습 기반

##### BEV 융합

| 논문 | 출처 | 요점 | URL |
|---|---|---|---|
| BEVFusion(MIT판) | MIT Han Lab, 2022(ICRA 2023) | 카메라·LiDAR 양 특징을 공유 BEV 공간에 가져와 융합. BEV pooling 최적화로 view 변환 40배 이상 고속화. 멀티태스크 대응 | https://arxiv.org/abs/2205.13542 / https://github.com/mit-han-lab/bevfusion |
| BEVFusion(PKU판·동명의 별논문) | 베이징대+Alibaba, NeurIPS 2022 | 카메라 흐름과 LiDAR 흐름을 독립적으로 BEV화해 융합. LiDAR 고장 시뮬레이션 포함 훈련으로 SOTA +15.7〜28.9% mAP를 주장 | https://arxiv.org/abs/2205.13790 / https://github.com/ADLab-AutoDrive/BEVFusion |

##### 모달리티 드롭아웃(센서 결손에 대한 강건화)

- 개념: 통상의 dropout이 뉴런을 지우는 데 비해, 훈련 중에 센서 1계통을 통째로 떨어뜨린다(제로 채움/마스크) → "남은 센서로 메우는" 내부 표현을 학습해, 실운용의 센서 고장·차폐에 견딘다. 개설: https://www.emergentmind.com/topics/modality-dropout
- 대표례: PKU판 BEVFusion의 고장 포함 훈련(상기)/ MoME(2025, 카메라 전손에서 NDS 87.9% 유지로 보고 — https://arxiv.org/abs/2503.19776)/ 선행례 Sensor Dropout(Liu et al., CoRL 2017 — https://arxiv.org/abs/1705.10422 、세부 미확인).

##### Privileged learning / Teacher-Student 증류(다리 로봇의 금자탑)

| 논문 | 서지 | 요점 | URL |
|---|---|---|---|
| Lee et al. "Learning quadrupedal locomotion over challenging terrain" | Science Robotics Vol.5, Issue 47, eabc5986, 2020-10-21 | 교사는 시뮬레이션 안에서만 얻을 수 있는 특권 정보(접지 상태·접촉력·지형 형상·마찰)로 RL 학습 → 학생은 실기에서 쓸 수 있는 고유수용 감각(관절각·IMU)의 이력만으로 교사를 모방. 맹목의 ANYmal이 진흙·눈·초목·잔해를 답파 | https://doi.org/10.1126/scirobotics.abc5986 / https://arxiv.org/abs/2010.11251 |
| Miki et al. "Learning robust perceptive locomotion for quadrupedal robots in the wild" | Science Robotics Vol.7, Issue 62, eabk2822, 2022 | 외수용(높이 맵)+고유수용을 attention 기반의 재귀적 belief state encoder로 통합. 외계 센서를 믿을 수 없는 장면에서는 고유수용 쪽으로 자동으로 가중을 옮긴다 = "학습된 퓨전 게이트". ANYmal이 알프스 등산로 1시간 코스를 완주 | https://www.science.org/doi/10.1126/scirobotics.abk2822 |

- 휴머노이드로의 수입례: Humanoid Parkour Learning(Zhuang et al., CoRL 2024)은 증류 정책을 Unitree H1에 zero-shot 이식(https://arxiv.org/abs/2406.10759)。ExBody2는 teacher-student 증류로 H1/G1의 전신 트래킹(arXiv:2412.13196으로 알려지나 1차 확인 미완). 사족에서 확립된 구도가 2024〜2026의 휴머노이드 RL 보행으로 그대로 유입되고 있다.

#### 2.3 실기 휴머노이드의 센서 구성(공표 정보)

| 기체 | 센서 구성(공표분) | 출처 | 비고 |
|---|---|---|---|
| Unitree G1 | 공식 사양표는 "Depth Camera + 3D LiDAR"+4ch 마이크 어레이+스피커 | https://www.unitree.com/g1 | **공식은 모델명을 명기하지 않음**. Livox Mid-360 + RealSense D435(i)라는 형번은 대리점/기술 문서 쪽의 기재(https://docs.quadruped.de/projects/g1/html/g1_overview.html) |
| Unitree H1 | 공식: "3D LIDAR + Depth Camera에 의한 360° 깊이 지각" | https://www.unitree.com/h1 | 형번은 공식 비기재(유통 정보로는 Mid-360 + D435i) |
| Tesla Optimus | 카메라 중심(Autopilot 유래 비전)+손끝 촉각+발바닥 힘/토크. "8 카메라"는 제3자 리뷰값으로 공식 1차 소스 미확인 | https://briandcolwell.com/a-complete-review-of-teslas-optimus-robot/ | LiDAR 비탑재의 카메라 순화 노선 |
| Figure 02 / 03 | 02: RGB 카메라 6대+VLM(6대의 1차 페이지 명기는 미확인). 03: 손바닥 카메라+촉각 센서를 공식 발표 | https://www.figure.ai/news/introducing-figure-03 | LiDAR 없음·시각+촉각 노선 |
| Boston Dynamics 신 Atlas(전동) | 2024 연구기: ToF+RGB-D/스테레오+LiDAR, IMU 1 kHz·관절 인코더 4 kHz(제3자 정리). 2026 양산판은 LiDAR를 빼고 360° 카메라+촉각 구성으로 변경했다는 보도 | https://www.aparobot.com/robots/atlas | 공식의 1차 센서 사양서는 존재하지 않음(미확인 취급) |
| Agility Digit | Velodyne VLP-16(몸통 꼭대기) + RealSense 깊이 카메라×4(골반 앞뒤의 D430 ×2 포함). LiDAR=원방 지도/장애물, 깊이 카메라=발밑의 면 추정 | https://robotsguide.com/robots/digit / https://agilityrobotics.com/content/check-out-these-big-advancements-in-digits-development | LiDAR+깊이의 고전적 퓨전 구성의 대표 |

관찰: 업계는 두 파 — ① LiDAR+깊이 카메라파(Unitree, Agility, 연구판 Atlas): §2.1의 LIO 자산을 그대로 쓸 수 있다. ② 카메라 순화파(Tesla, Figure): 학습 기반(§2.2)으로 기하를 추정. 양산 Atlas의 LiDAR 철거는 ②로의 합류를 시사.

#### 2.4 "어느 층에서 섞는가" — early / mid / late fusion(3단 쉽게 풀기)

##### ① 비유(요리)

- **Early fusion(생데이터로 섞기)** = 재료를 전부 같은 냄비에 처음부터 넣는다. 재료끼리 잘 어우러지지만, 하나가 썩어 있으면 냄비째 망친다.
- **Mid fusion(특징으로 섞기)** = 각 재료를 따로따로 손질한 후에 합친다. 합치기 쉽고, 이상한 재료는 손질 단계에서 알아챌 수 있다.
- **Late fusion(결론으로 섞기)** = 3명의 요리사가 각각 완성품을 만들고, 심사원이 다수결. 한 명이 실패해도 만회할 수 있지만, 재료끼리의 화학 반응은 일어나지 않는다.

##### ② 공학적 설명

| 층 | 섞는 것 | 장점 | 단점 |
|---|---|---|---|
| Early(raw) | 생점군·생화소·생 IMU 값 | 정보 손실 제로. 상관을 최대한 이용(예: Point-LIO는 LiDAR 점 1개마다 IMU와 상태 갱신) | 시각 동기·외부 캘리브레이션에 극히 민감. 레이트 차(IMU 수백 Hz vs 카메라 30 Hz)의 흡수가 어렵다. 1센서의 고장이 전체를 오염 |
| Mid(특징) | 특징 맵·BEV 특징·임베딩 | 모달리티마다 최적의 인코더를 쓰면서 밀하게 융합. BEVFusion도 Miki 2022의 belief encoder도 이 층 | 공통 표현 공간의 설계가 필요. 훈련 분포 밖의 결손에 약함 → modality dropout으로 보강 |
| Late(판단) | 각 계통의 추정 결과(위치·검출·판정) | 모듈 독립으로 개발·검증·교환이 용이. 고장 격리가 자연스러움(EKF로 LIO 출력+GNSS+오도메트리를 통합하는 것은 이 층) | 각 계통이 버린 정보는 돌아오지 않는다. 판단이 갈렸을 때의 조정이 어렵다 |

##### ③ 구현상의 고려

- **시각 동기가 모든 것의 토대**: early로 갈수록 PTP/하드웨어 트리거급의 동기가 필수. Mid-360은 IMU 내장·동기 완료이므로 early fusion(LIO)이 하기 쉽다.
- **캘리브레이션 오차의 전파**: early/mid는 센서 간 외부 파라미터의 오차가 특징 공간의 "번짐"으로 학습을 오염시킨다. late는 각 계통 안에서 닫힌다.
- **고장 모드 설계**: late는 축퇴 운전(LiDAR 사망→카메라만으로 감속 계속)을 설계하기 쉽다. mid에서 동등한 강건성을 원하면 modality dropout을 훈련 시 반드시 넣는다(PKU판 BEVFusion의 교훈).
- **계산 예산과 레이트**: early는 최속 센서의 레이트로 돈다(Point-LIO 4〜8 kHz). 제어 루프 직결의 상태 추정은 early/고전, 의미 이해는 mid/학습, 행동 판단·이중화는 late — 로 층마다 구분해 쓰는 하이브리드가 실기의 정석(예: G1 = Mid-360+IMU를 FAST-LIO2로 early 융합 → 깊이 카메라의 검출을 mid/late로 중첩).

---

### 3. 시장 동향(2024〜2026)

**기사용 요약(5행)**

1. 휴머노이드 시장 예측은 Goldman Sachs "2035년 380억 달러"(2024년에 종래 대비 6배로 상향 수정)부터 Morgan Stanley "2050년 5조 달러 TAM", Citi "2050년 7조 달러"까지, 투자은행 간에 2자릿수 가까운 폭이 있다.
2. 중국은 공업정보화부가 2023-11에 "2025년 양산·2027년 세계 선진 수준"의 산업 정책을 공표했고, 중상산업연구원은 2025년의 중국 출하 1.44만 대=세계의 84.7%로 추계한다(2026년 시점).
3. LiDAR는 가격 파괴가 진행 중 — Mid-360 $749, Unitree L1 $249, Hesai는 "약 $200의 ATX"를 양산하며 2025년 출하 가이던스 120〜150만 대. Yole은 "출하 감소가 아니라 단가 급락"을 이유로 금액 예측을 하향 수정했다.
4. 이벤트 카메라의 기수 Prophesee는 2024-10에 사법 재건 절차 진입 → CEO 교체 → 2026-06에 €20M 조달+드론 검지 시스템 Mantara 발표로 자력 재건(인수가 아님).
5. 베이징은 2025-04에 세계 최초의 휴머노이드 하프 마라톤(우승: 톈궁 Ultra, 2:40:42), 2025-08에 제1회 세계 휴머노이드 로봇 운동회(16개국·500대 초과)를 개최했고, 2026-04의 제2회 마라톤에서는 로봇이 인간의 세계 기록을 웃도는 50분 26초를 기록, 제2회 운동회는 2026-08-22 개막(2,056대).
