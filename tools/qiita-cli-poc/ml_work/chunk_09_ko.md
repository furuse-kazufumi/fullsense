#### camera(22 op)

카메라 모델과 투영 계산. 3D와 2D를 오가는 변환 군이다.

| op | 설명 |
|---|---|
| `SolvePnP` | 3D-2D 대응으로부터 카메라 자세를 추정(cv2.solvePnP, 부재 시 numpy)(camera.SolvePnP).  [backend=opencv] |
| `backproject` | 픽셀 (N,2)를 깊이로 카메라 좌표계의 3D 점으로 들어 올린다(역투영). |
| `decompose_essential` | 본질 행렬 E를 4가지 상대 pose 후보로 분해한다. |
| `decompose_intrinsics` | 내부 행렬 K로부터 fx, fy, cx, cy, skew를 꺼낸다. |
| `depth_to_points` | 깊이 맵 전체를 카메라 좌표계의 점군으로 역투영한다. |
| `distort_points` | 이상 픽셀에 반경·접선 방향의 렌즈 왜곡을 부여한다(Brown 모델). |
| `epipolar_lines` | 기초 행렬을 통해 대응점이 유도하는 에피폴라 선을 계산한다. |
| `essential_from_fundamental` | E = K2^T·F·K 로 기초 행렬을 본질 행렬로 변환한다. |
| `essential_matrix` | 캘리브레이션 완료 페어의 8쌍 이상 대응으로부터 본질 행렬 E를 추정한다. |
| `fundamental_matrix` | 8쌍 이상의 대응으로부터 정규화 8점법으로 기초 행렬 F를 추정한다. |
| `intrinsic_matrix` | 핀홀 내부 행렬 K를 조립한다. |
| `normals_from_depth` | 정렬 완료 깊이 맵으로부터 픽셀별 법선 (H,W,3)을 추정한다. |
| `project_points` | 월드 점 (N,3)을 픽셀로 투영해 (uv, depth)를 반환한다. |
| `projection_matrix` | 3x4 투영 행렬 P = K·[R t] 를 조립한다(R, t는 생략 가능). |
| `recover_pose` | 본질 행렬의 분해 후보에서 물리적으로 올바른 상대 pose를 고른다. |
| `reprojection_error` | 점별 재투영 오차 [px]를 계산한다. |
| `rodrigues` | 회전 벡터(축×각)를 회전 행렬로(Rodrigues 공식). |
| `rotation_log` | 회전 행렬을 회전 벡터로(rodrigues의 역). |
| `solve_pnp` | 6쌍 이상의 3D↔2D 대응으로부터 6자유도 pose를 추정한다(PnP). |
| `stereo_rectify` | 캘리브레이션 완료 스테레오 페어의 평행화 회전을 계산한다(Fusiello 법). |
| `triangulate` | 2시점 대응 픽셀의 선형 DLT 삼각측량. |
| `undistort_points` | 반경·접선 방향의 왜곡을 제거한다(distort_points의 역). |

#### texture(21 op)

텍스처(결) 해석. Laws 에너지나 Gabor 등, "무늬의 질감"을 수치화한다.

![texture 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_10_texture_laws.png)
*그림: Laws 텍스처 에너지 예(11.1.1절에서 재수록)*

| op | 설명 |
|---|---|
| `deviation_image` | texture op(HALCON: deviation_image) |
| `entropy_image` | texture op(HALCON: entropy_image) |
| `f2_symmetry` | texture op(HALCON: symmetry) |
| `gabor` | texture op(HALCON: gen_gabor) |
| `gen_gabor` | texture op(HALCON: gen_gabor) |
| `sk_entropy` | texture op(HALCON: entropy_image) |
| `sk_frangi` | texture op(HALCON: lines_gauss) |
| `sk_gabor` | texture op(HALCON: gen_gabor) |
| `sk_hessian` | texture op(HALCON: lines_gauss) |
| `sk_lbp` | texture op(HALCON: -) |
| `sk_meijering` | texture op(HALCON: lines_gauss) |
| `sk_shape_index` | texture op(HALCON: -) |
| `std_filter` | texture op(HALCON: deviation_image) |
| `texture_laws` | texture op(HALCON: texture_laws) |
| `tf_census_transform` | texture op(HALCON: -) |
| `tf_rank_transform` | texture op(HALCON: -) |
| `xsk2_hog` | texture op(HALCON: -) |
| `xsk_meijering` | texture op(HALCON: -) |
| `xsk_sato` | texture op(HALCON: -) |
| `xsk_struct_coherence` | texture op(HALCON: -) |
| `xsp_hilbert_env` | texture op(HALCON: -) |

#### frequency(19 op)

주파수 영역 처리(FFT·필터링). 이미지를 파동의 중첩으로 다루는 관점이다.

![frequency 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_08_fft_image.png)
*그림: FFT 스펙트럼 예(11.1.1절에서 재수록)*

| op | 설명 |
|---|---|
| `bandpass_image` | frequency op(HALCON: bandpass_image) |
| `fft_generic` | frequency op(HALCON: fft_generic) |
| `fft_image` | frequency op(HALCON: fft_image) |
| `fft_image_inv` | frequency op(HALCON: fft_image_inv) |
| `highpass` | frequency op(HALCON: highpass_image) |
| `highpass_image` | frequency op(HALCON: highpass_image) |
| `lowpass` | frequency op(HALCON: -) |
| `phase_deg` | frequency op(HALCON: phase_deg) |
| `phase_rad` | frequency op(HALCON: phase_rad) |
| `power_byte` | frequency op(HALCON: power_byte) |
| `power_ln` | frequency op(HALCON: power_ln) |
| `power_real` | frequency op(HALCON: power_real) |
| `rft_generic` | frequency op(HALCON: rft_generic) |
| `sk_butterworth` | frequency op(HALCON: -) |
| `xsk2_radon` | frequency op(HALCON: -) |
| `xsp_dct` | frequency op(HALCON: -) |
| `xsp_dct_lowpass` | frequency op(HALCON: -) |
| `xwt_mra_component` | frequency op(HALCON: -) |
| `xwt_subband_tile` | frequency op(HALCON: -) |

#### pcseg(17 op)

점군 세그멘테이션(평면 추출·클러스터링 등).

| op | 설명 |
|---|---|
| `aabb` | 점군의 축 평행 바운딩 박스 (min, max)를 반환한다. |
| `centroid` | 점군의 무게중심을 반환한다. |
| `crop_box` | 축 평행 박스 [lo, hi] 안의 점만 남긴다. |
| `crop_sphere` | 중심에서 radius 이내의 점만 남긴다(점과 마스크를 반환). |
| `curvature` | k 근방의 고유값으로부터 점별 곡률(표면 변화율)을 계산한다. |
| `euclidean_clusters` | 유클리드 클러스터링으로 근접 점을 그룹화한다(Rusu 2009). |
| `farthest_point_sampling` | 최원점 샘플링으로 공간적으로 흩어진 k점을 고른다. |
| `fit_cylinder_ransac` | 점+법선 샘플로부터 RANSAC으로 원기둥을 강건하게 피팅한다. |
| `fit_plane` | 전체 점에 대한 전최소제곱 평면 피팅(PCA). |
| `fit_plane_ransac` | RANSAC으로 지배 평면을 강건하게 피팅한다. |
| `fit_sphere_ransac` | RANSAC으로 구를 강건하게 피팅한다(중심·반지름·인라이어를 반환). |
| `height_above_plane` | 평면의 법선 방향을 따른 각 점의 높이(부호 있는 거리). |
| `obb` | PCA에 의한 유향 바운딩 박스. |
| `plane_distance` | 평면 [a,b,c,d]에 대한 각 점의 부호 있는 거리. |
| `principal_axes` | 점군의 주성분 분석(고유값과 고유벡터를 반환). |
| `region_growing` | 매끄러움 제약 포함 영역 성장으로 클러스터 분할한다(Rabbani 2006). |
| `remove_ground` | 지배 평면을 RANSAC으로 맞춰 점군을 지면/비지면으로 나눈다. |

#### specops(16 op)

의사 센서·지각계의 특수 op(의사 LiDAR, 1차원 이벤트 카메라, 실기 센서 재현 등, 본편 6장·9장의 주역들).

| op | 설명 |
|---|---|
| `read_envi` | ENVI 하이퍼스펙트럴 큐브를 읽어 들인다(cube, meta). |
| `spec_angle_mapper` | 참조 스펙트럼과의 픽셀별 스펙트럼 각 [rad](SAM). |
| `spec_band` | 큐브의 제 i 밴드를 1장의 이미지로 꺼낸다. |
| `spec_band_ratio` | 픽셀별 밴드 비 band_i/(band_j+eps) 를 계산한다. |
| `spec_continuum_removal` | 컨티뉴엄 제거(각 스펙트럼을 상포락선으로 나눈다). |
| `spec_decorrelation_stretch` | 상관 제거 스트레치로 색 차이를 강조한다(decorrelation stretch). |
| `spec_endmembers_ppi` | Pixel Purity Index에 의한 엔드멤버의 근사 추출. |
| `spec_fuse` | 정렬 완료된 단일 밴드 이미지 군을 1장으로 융합한다. |
| `spec_index` | 정규화 차분 지수 (a-b)/(a+b+eps)(NDVI 형). |
| `spec_mnf` | 최소 노이즈 비율 변환(MNF). |
| `spec_nearest_band` | 지정 파장에 가장 가까운 밴드의 index를 반환한다. |
| `spec_pansharpen` | 고해상도 팬크로 밴드로 멀티스펙트럴을 팬샤픈화한다. |
| `spec_pca` | 스펙트럼 축 방향의 주성분 분석. |
| `spec_rgb_composite` | 고른 3밴드로 표시용 RGB 합성 이미지를 만든다. |
| `spec_unmix` | 선형 스펙트럼 분해로 픽셀별 존재비 맵을 추정한다. |
| `write_envi` | ENVI 큐브를 써낸다(.hdr + .img). |

#### 3D Matching(15 op)

| op | 설명 |
|---|---|
| `create_cam_pose_look_at_point` | 카메라 위치와 주시점으로부터 look-at 자세(4x4)를 구축(create_cam_pose_look_at_point). |
| `create_deformable_surface_model` | 변형 surface 모델을 만든다(PPF 기반)(create_deformable_surface_model). |
| `create_shape_model_3d` | 3D 점군으로부터 복수 시점의 실루엣 shape 모델을 만든다(create_shape_model_3d). |
| `create_surface_model` | 모델 점군의 Point Pair Feature 기술자(해시 표)를 구축한다. |
| `find_box_3d` | 점군에서 축 평행 경계 상자(OBB 근사=PCA 상자)를 검출(find_box_3d). |
| `find_deformable_surface_model` | 변형 surface 모델을 장면 점군에서 검출(PPF + ICP refine)(find_deformable_surface_model). |
| `find_shape_model_3d` | 3D shape 모델을 이미지에서 검출(투영 실루엣과 상관)(find_shape_model_3d). |
| `find_surface_model` | PPF 투표 + ICP 정밀화로 장면 안 모델의 6자유도 pose를 찾는다. |
| `find_surface_model_image` | 깊이 이미지를 점군화해 surface 모델을 검출(find_surface_model_image). |
| `project_shape_model_3d` | 3D 모델을 카메라로 투영해 에지 이미지를 생성(project_shape_model_3d). |
| `reduce_domain` | domain을 region으로 축소(reduce_domain). change_domain과 동의의 facade. |
| `refine_deformable_surface_model` | 변형 surface 모델을 검출 → ICP로 정밀화(refine_deformable_surface_model). |
| `refine_surface_model_pose` | 초기 자세로부터 ICP로 surface 모델 자세를 정밀화(refine_surface_model_pose). |
| `refine_surface_model_pose_image` | 깊이 이미지로부터 점군화해 ICP로 자세 정밀화(refine_surface_model_pose_image). |
| `trans_pose_shape_model_3d` | 3D 모델에 자세(4x4)를 적용(trans_pose_shape_model_3d). |

#### videops(15 op)

동영상·시계열 처리(프레임 간 차분, 트래킹 등).

| op | 설명 |
|---|---|
| `background_subtraction` | 시간 중앙값의 배경 모델로 프레임별 전경 마스크를 얻는다. |
| `flicker_reduce` | 프레임 간 전체 휘도의 깜빡임(플리커)을 제거한다. |
| `frame_difference` | 인접 프레임의 절대 차분으로 움직임량 볼륨을 얻는다. |
| `motion_energy` | 시간 방향의 변화량을 누적한 움직임 에너지 맵 (H,W). |
| `moving_average` | 시간 방향의 이동 평균(박스) 평활화. |
| `optical_flow_sequence` | 인접 프레임 간의 플로 강도 볼륨 (T-1,H,W). |
| `per_frame` | 2D op를 각 프레임에 독립적으로 적용한다. |
| `spatiotemporal_gaussian` | (t,y,x)의 분리형 3D 가우시안 평활화. |
| `spatiotemporal_sobel` | (t,y,x)의 3D Sobel 그래디언트 강도. |
| `temporal_gradient` | 중심 차분에 의한 시간 미분 d(video)/dt. |
| `temporal_max` | 시간 방향의 최댓값 투영 (H,W). |
| `temporal_mean` | 픽셀별 시간 평균 (H,W). |
| `temporal_median` | 픽셀별 시간 중앙값 (H,W). |
| `temporal_min` | 시간 방향의 최솟값 투영 (H,W). |
| `temporal_std` | 픽셀별 시간 표준편차 = 활동 맵 (H,W). |

#### Segmentation(14 op)


![fops_segmentation_facade](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_segmentation_facade.png)
*그림: Segmentation의 실제 처리 예 — 호박(앰버) 속의 벌레: 강한 주황 색기+반투명 산란+기포·균열의 방해 속에서, 최암부 이진화 → opening → 이미지 가장자리에 닿는 성분(가장자리 그림자·균열) 제외 → 최대 성분이라는 고정 파이프라인으로 벌레 본체를 뽑아낸다(Fullseye 실제 출력). 시행 과정의 honest 기록: B 채널+clahe 전처리는 호박 내부 텍스처를 증폭해 역효과였다(clahe가 항상 정답은 아니다). 입력은 모두 AI 생성 이미지(Gemini).*

| op | 설명 |
|---|---|
| `check_difference` | 기준 이미지와의 차가 tol을 넘는 픽셀을 영역으로 반환(check_difference). |
| `class_2dim_sup` | 2채널 특징 공간에서 ref_region의 분포에 들어가는 픽셀을 분류(지도)(class_2dim_sup). |
| `class_2dim_unsup` | 2채널 특징 공간을 k-means로 비지도 분류(class_2dim_unsup). 라벨 이미지를 반환. |
| `class_ndim_norm` | ND 특징 이미지를 학습 완료 정규분포 클래스로 분류(Mahalanobis 거리 < thresh)(class_ndim_norm). |
| `classify_image_class_gmm` | 가우시안 혼합 모델로 다채널 특징 이미지를 픽셀 분류(classify_image_class_gmm). |
| `classify_image_class_knn` | k-NN으로 다채널 특징 이미지를 픽셀 분류(classify_image_class_knn). |
| `classify_image_class_lut` | 그레이 LUT에 의한 픽셀 분류(임계값/라벨 LUT)(classify_image_class_lut). |
| `classify_image_class_mlp` | 학습 완료 MLP로 다채널 특징 이미지를 픽셀 분류(classify_image_class_mlp). |
| `classify_image_class_svm` | 학습 완료 선형 SVM으로 다채널 특징 이미지를 픽셀 분류(classify_image_class_svm). |
| `expand_gray` | seed로부터 gray 유사(/Δ/<tol)로 영역을 팽창(expand_gray). |
| `expand_gray_ref` | 참조 이미지의 그레이 유사도로 seed를 팽창(expand_gray_ref). |
| `learn_ndim_norm` | 특징 벡터 군으로부터 정규분포 클래스(평균·공분산)를 학습(learn_ndim_norm). |
| `regiongrowing_n` | 다채널 특징의 유사성으로 이미지 전체를 영역 분할(regiongrowing_n). 라벨 이미지를 반환. |
| `watersheds_marker` | 마커 제어 watershed 분할(watersheds_marker). markers: int 라벨 이미지(0=미할당). |

#### extra(14 op)

| op | 설명 |
|---|---|
| `xsitk_closing_by_recon` | extra op(HALCON: -) |
| `xsitk_confidence_connected` | extra op(HALCON: -) |
| `xsitk_connected_threshold` | extra op(HALCON: -) |
| `xsitk_curv_aniso_diff` | extra op(HALCON: -) |
| `xsitk_curvature_flow` | extra op(HALCON: -) |
| `xsitk_grayscale_fillhole` | extra op(HALCON: -) |
| `xsitk_grayscale_grindpeak` | extra op(HALCON: -) |
| `xsitk_huang_thresh` | extra op(HALCON: -) |
| `xsitk_laplacian_sharpen` | extra op(HALCON: -) |
| `xsitk_maxentropy_thresh` | extra op(HALCON: -) |
| `xsitk_minmax_curv_flow` | extra op(HALCON: -) |
| `xsitk_moments_thresh` | extra op(HALCON: -) |
| `xsitk_opening_by_recon` | extra op(HALCON: -) |
| `xsitk_signed_maurer_dist` | extra op(HALCON: -) |

#### stereo(13 op)

스테레오 시차로부터의 거리 추정. 양안의 삼각측량이다(본편 14.4 참조).

| op | 설명 |
|---|---|
| `BlockMatching` | 블록 매칭 시차(cv2.StereoBM, 부재 시 fullseye numpy)(stereo.BlockMatching).  [backend=opencv] |
| `SGBM` | Semi-Global BM 시차(cv2.StereoSGBM, 부재 시 fullseye SGM numpy)(stereo.SGBM).  [backend=opencv] |
| `census_transform` | Census 변환: 근방과의 대소 관계로 각 픽셀을 부호화한다. |
| `depth_from_disparity` | 시차로부터 계량 깊이 Z = f·B/d 를 계산한다. |
| `disparity_census` | Census + 해밍 거리의 승자 독식으로 조밀한 시차를 추정한다. |
| `disparity_confidence` | 비용 곡선으로부터 픽셀별 매칭 신뢰도 [0,1]을 추정(PKRN 형). |
| `disparity_map` | 승자 독식 블록 매칭에 의한 조밀한 시차 추정. |
| `disparity_sgm` | Semi-Global Matching 시차(Hirschmüller 법). |
| `disparity_subpixel` | 포물선 피팅으로 시차를 서브픽셀로 정밀화한다. |
| `fill_disparity` | 무효 시차를 행 방향 보간으로 메운다(배경 쪽으로 보간). |
| `lr_consistency` | 좌우 일치 체크의 마스크(True = 신뢰할 수 있는 시차). |
| `reproject_to_points` | 깊이 맵을 카메라 좌표계의 점군 (N,3)으로 역투영한다. |
| `speckle_filter` | 시차 맵에서 작은 스펙클 영역을 제거한다. |

#### terrain(13 op)

| op | 설명 |
|---|---|
| `detect_obstacles` | 보행 가능 지면에서 clearance 이상 솟아오르는 셀을 장애물로 분할한다. |
| `elevation_map` | 점군을 2.5D 표고 그리드로 빈 담기 한다. |
| `fill_gaps` | nan 셀을 최근접 유효 높이로 메운다. |
| `foothold_candidates` | 지형에서 이산적인 안전 발판 후보를 고른다. |
| `foothold_score` | 셀별 평탄도 스코어 [0,1](1 = 평탄하고 수평 = 좋은 발판). |
| `fuse_elevation` | 정렬 완료된 표고 그리드 군을 로봇 중심의 1장으로 융합한다. |
| `ground_plane` | 셀 단위의 강건 최소제곱으로 지면 평면 z = ax+by+c 를 추정한다. |
| `ground_surface` | 그레이 오프닝으로 매끄러운 보행 가능 지면의 포락면을 얻는다. |
| `roughness_map` | 셀별 거칠기 = 국소 높이의 표준편차. |
| `slope_map` | 셀별 경사도 = 수평으로부터의 표면 각도. |
| `step_edges` | 높이 맵에서 단차 에지(연석·계단의 헛디딤 선)를 검출한다. |
| `surface_normals` | 셀별 위쪽 방향 단위 법선 (H,W,3). |
| `traversability` | 단차와 경사도의 상한으로 통행 가능 마스크를 만든다. |

#### artificial-life(12 op)

| op | 설명 |
|---|---|
| `alife_curvature_flow` | artificial-life op(HALCON: -) |
| `alife_cyclic_ca` | artificial-life op(HALCON: -) |
| `alife_dla` | artificial-life op(HALCON: -) |
| `alife_gray_scott` | artificial-life op(HALCON: -) |
| `alife_langton_ant` | artificial-life op(HALCON: -) |
| `alife_lenia` | artificial-life op(HALCON: -) |
| `alife_life_step` | artificial-life op(HALCON: -) |
| `alife_perona_malik` | artificial-life op(HALCON: -) |
| `alife_reaction_bz` | artificial-life op(HALCON: -) |
| `alife_sandpile` | artificial-life op(HALCON: -) |
| `alife_turing` | artificial-life op(HALCON: -) |
| `alife_wolfram1d` | artificial-life op(HALCON: -) |

#### complexops(12 op)

| op | 설명 |
|---|---|
| `cx_apply_transfer_function` | 중심화 스펙트럼에 필터 H를 곱한다(전달 함수 적용). |
| `cx_bandpass` | 주파수 영역의 이상 원환 밴드패스 필터. |
| `cx_fft` | 실이미지의 중심화 2D FFT(복소 스펙트럼). |
| `cx_from_mag_phase` | 진폭과 라디안 위상으로부터 복소장을 재구성한다. |
| `cx_ifft` | cx_fft의 역변환(ifft2 + ifftshift). |
| `cx_imag` | 복소장의 허수부를 실이미지로 반환한다. |
| `cx_log_magnitude` | 표시용 로그 진폭 스펙트럼 [0,1]. |
| `cx_magnitude` | 픽셀별 복소 진폭(절댓값)을 반환한다. |
| `cx_phase` | 복소장의 랩된 위상을 반환한다. |
| `cx_real` | 복소장의 실수부를 실이미지로 반환한다. |
| `cx_wiener_deconvolve` | 주파수 영역 Wiener 디컨볼루션으로 이미지를 복원한다. |
| `phase_unwrap` | 2D 위상 언랩(랩 위상→연속 위상). |

#### restoration(12 op)


![fops_restoration](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_restoration.png)
*그림: restoration의 실제 처리 예 — 모션 블러는 컨볼루션이므로 윤곽 강조(unsharp)로는 복원할 수 없고, 블러 PSF를 가정한 iv_motion_deblur(Wiener 역컨볼루션)로 비로소 글자를 읽을 수 있는 수준까지 돌아온다(Fullseye 실제 출력). 블러는 선형 모션 PSF(L=9px, 0°)를 컨볼루션해 부여(convol_fft). 입력은 skimage page/camera+AI 생성 이미지(Gemini).*

| op | 설명 |
|---|---|
| `iv_backproject_superres` | restoration op(HALCON: -) |
| `iv_gradient_inpaint` | restoration op(HALCON: -) |
| `iv_motion_deblur` | restoration op(HALCON: -) |
| `iv_richardson_lucy` | restoration op(HALCON: -) |
| `iv_unsharp_deblur` | restoration op(HALCON: -) |
| `iv_wiener_deconv_spatial` | restoration op(HALCON: -) |
| `xcv3_inpaint_ns` | restoration op(HALCON: -) |
| `xcv_inpaint` | restoration op(HALCON: -) |
| `xsk2_wiener` | restoration op(HALCON: -) |
| `xsk_inpaint` | restoration op(HALCON: -) |
| `xsk_richardson_lucy` | restoration op(HALCON: -) |
| `xsk_unwrap_phase` | restoration op(HALCON: -) |

#### meshrepair(11 op)

| op | 설명 |
|---|---|
| `boundary_edges` | 메시의 열린 가장자리의 에지 목록 (M,2)을 반환한다. |
| `components` | 메시를 연결 성분으로 분할한다. |
| `convex_hull` | 점 집합의 볼록 껍질 메시(바깥 방향 삼각형)를 만든다. |
| `decimate_qem` | QEM 에지 수축으로 목표 면 수까지 간략화(데시메이션)한다. |
| `inertia_tensor` | 수밀 메시가 둘러싼 입체의 엄밀한 질량 특성(관성 텐서). |
| `is_edge_manifold` | 어느 에지도 3면 이상에 공유되지 않으면 True(에지 다양체 판정). |
| `is_watertight` | 에지 다양체이며 닫혀 있으면 True(수밀 판정). |
| `orient_consistent` | 모든 면의 감김 방향을 맞춘다(뒤집힌 면 수도 반환). |
| `remove_degenerate_faces` | 면적 0의 퇴화 면을 버린다(꼭짓점은 불변). |
| `smooth_taubin` | Taubin의 λ/μ 평활화(토폴로지 불변). |
| `weld_vertices` | 허용 오차 내에서 일치하는 꼭짓점을 융합(weld)한다. |

#### arithmetic(10 op)


![fops_arithmetic](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_arithmetic.png)
*그림: arithmetic의 실제 처리 예 — 암부가 뭉개진 이미지는 선형 게인으로는 명부가 먼저 화이트 클리핑되지만, log_image(로그 변환)는 암부를 끌어올리면서 명부를 압축하므로 양립한다(Fullseye 실제 출력). 입력은 AI 생성(Gemini)·자체 합성·skimage camera 감광의 3종.*

| op | 설명 |
|---|---|
| `abs_image` | arithmetic op(HALCON: abs_image) |
| `acos_image` | arithmetic op(HALCON: acos_image) |
| `asin_image` | arithmetic op(HALCON: asin_image) |
| `atan_image` | arithmetic op(HALCON: atan_image) |
| `cos_image` | arithmetic op(HALCON: cos_image) |
| `exp_image` | arithmetic op(HALCON: exp_image) |
| `log_image` | arithmetic op(HALCON: log_image) |
| `sin_image` | arithmetic op(HALCON: sin_image) |
| `sqrt_image` | arithmetic op(HALCON: sqrt_image) |
| `tan_image` | arithmetic op(HALCON: tan_image) |

#### augmentation(10 op)


![fops_augmentation](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_augmentation.png)
*그림: augmentation의 실제 처리 예 — 1장의 이미지에서 촬상의 악조건(샷 노이즈·모션 블러·주변 감광)을 물리 모델로 재현 생성해 학습 데이터를 늘리는 op 군(Fullseye 실제 출력). 입력은 skimage camera+AI 생성 이미지(Gemini) 2종.*

| op | 설명 |
|---|---|
| `aug_barrel` | augmentation op(HALCON: -) |
| `aug_chromatic` | augmentation op(HALCON: -) |
| `aug_cutout` | augmentation op(HALCON: -) |
| `aug_fixed_pattern` | augmentation op(HALCON: -) |
| `aug_jpeg_blocks` | augmentation op(HALCON: -) |
| `aug_motion_blur` | augmentation op(HALCON: -) |
| `aug_read_noise` | augmentation op(HALCON: -) |
| `aug_rolling_shutter` | augmentation op(HALCON: -) |
| `aug_shot_noise` | augmentation op(HALCON: -) |
| `aug_vignette` | augmentation op(HALCON: -) |

#### mesh(10 op)

| op | 설명 |
|---|---|
| `bounds` | 축 평행 바운딩 박스 (min, max)를 반환한다. |
| `mesh_to_points` | sample_surface의 별칭 — 메시를 넣으면 점군이 나온다. |
| `normalize_scale` | 바운딩 박스의 최대 변이 size가 되도록 원점 기준으로 스케일한다. |
| `read_mesh` | 삼각형 메시를 읽어 (V, F)를 반환한다. |
| `read_points` | 점군을 읽는다(색 포함이면 (P, C)를 반환). |
| `recenter` | 꼭짓점 무게중심이 원점에 오도록 평행 이동한다(새 배열을 반환). |
| `sample_surface` | 메시 표면에서 균일하게 n점을 샘플링한다. |
| `voxelize` | 메시를 정규 그리드로 복셀화한다 (occ, origin). |
| `write_mesh` | read_mesh가 읽을 수 있는 형식(.obj 등)으로 삼각형 메시를 써낸다. |
| `write_points` | 점군을 .ply / .xyz 등으로 써낸다. |

#### xldgeom(10 op)

| op | 설명 |
|---|---|
| `xg_area_center` | 신발끈 공식으로 윤곽의 다각형 면적을 구한다(절댓값의 합). |
| `xg_clip_contours` | 폴리라인 길이가 최대 길이의 a배 미만인 윤곽을 버린다. |
| `xg_crop_contours` | 이미지 중앙의 a 비율 창 안에 있는 윤곽점만 남긴다. |
| `xg_eccentricity` | 점 공분산으로부터 이심률 sqrt(1-λmin/λmax) 를 계산한다. |
| `xg_elliptic_axis` | 점 집합의 장단축 비 sqrt(λmax/λmin). |
| `xg_gen_polygons` | Douglas-Peucker 폴리라인 단순화(eps는 외접 직사각형 대각선의 a배). |
| `xg_height_width_ratio` | 점 집합의 축 평행 외접 직사각형의 세로가로 비. |
| `xg_moments` | 점 집합의 정규화 2차 중심 모멘트 mu20+mu02. |
| `xg_orientation` | 주축 방향 [deg]을 [0,180)으로 접어 180으로 나눠 정규화. |
| `xg_regress_contours` | 전최소제곱 직선 피팅의 잔차 RMS(공분산의 단축 고유값의 제곱근). |

#### volops(9 op)

| op | 설명 |
|---|---|
| `vol_distance_transform` | 이진 볼륨의 엄밀한 유클리드 거리 변환. |
| `vol_frangi` | 3D Frangi 혈관형(관상 구조) 강조 — 멀티스케일. |
| `vol_gradient_magnitude` | 3D Sobel 그래디언트 강도 sqrt(gz^2+gy^2+gx^2). |
| `vol_hessian_blobness` | Hessian 고유값에 의한 구형 블롭 응답(단일 스케일). |
| `vol_label` | 3D 연결 성분 라벨링(근방계 선택 가능). |
| `vol_local_maxima` | 3D 국소 극대(피크) 검출. |
| `vol_region_props` | 라벨 볼륨으로부터 성분별 정량 특징을 계산한다. |
| `vol_sato` | 3D Sato 관상 구조 필터(2 고유값의 간이판). |
| `vol_watershed` | 마커 제어의 3D watershed 분할(scikit-image 도입 시에만). |

#### 2D Metrology(8 op)


![fops_metrology](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_metrology.png)
*그림: 2D Metrology의 실제 처리 예 — 서브픽셀 윤곽(threshold_sub_pix)에 원을 최소제곱 피팅(fit_circle)해 반지름을 계측. 참값이 있는 합성 6원으로 반지름 오차를 실측(Fullseye 실제 출력). 입력은 합성+AI 생성(Gemini) 2종.*

| op | 설명 |
|---|---|
| `add_metrology_object_circle_measure` | 원 계측 오브젝트를 추가(add_metrology_object_circle_measure). |
| `add_metrology_object_ellipse_measure` | 타원 계측 오브젝트를 추가(add_metrology_object_ellipse_measure). |
| `add_metrology_object_generic` | 범용 계측 오브젝트를 추가(add_metrology_object_generic). |
| `add_metrology_object_line_measure` | 직선 계측 오브젝트를 추가(add_metrology_object_line_measure). index를 반환. |
| `add_metrology_object_rectangle2_measure` | 직사각형 계측 오브젝트를 추가(add_metrology_object_rectangle2_measure). |
| `align_metrology_model` | 계측 모델의 전체 오브젝트를 평행 이동해 정렬(align_metrology_model). |
| `apply_metrology_model` | 각 계측 오브젝트의 근방에서 에지를 측정하고, 형상을 다시 피팅해 결과를 반환(apply_metrology_model). |
| `create_metrology_model` | 빈 계측 모델을 만든다(create_metrology_model). |

#### Inspection(8 op)


![fops_inspection](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_inspection.png)
*그림: Inspection의 실제 처리 예 — 블리스터 팩(합성·결함 주입으로 참값 관리)을 격자 사양에 따라 포켓별로 검사: 이진화→면적(결품/이종)→진원도(깨짐)→암부 픽셀(오염)의 고정 임계값으로 합격/불합격 판정. 3팩 합계로 주입 결함 11건 중 11건 검출·오검출 0(Fullseye 실제 출력).*

| op | 설명 |
|---|---|
| `apply_bead_inspection_model` | 이미지 안의 비드를 검사해, 경로 위에서의 결손/삐져나옴을 검출(apply_bead_inspection_model). |
| `apply_texture_inspection_model` | 텍스처 검사 모델로 이상(Mahalanobis 거리 큼) 영역을 검출(apply_texture_inspection_model). |
| `compare_ext_variation_model` | 확장 비교: 상대(k*std)와 절대(abs_thresh)의 두 임계값을 모두 만족하는 픽셀을 결함으로(compare_ext_variation_model). |
| `compare_variation_model` | 이미지를 variation model과 비교해 /image-mean/ > k*std 인 결함 영역을 반환(compare_variation_model). |
| `create_bead_inspection_model` | 접착 비드 검사 모델(기준 경로 + 폭 공차)(create_bead_inspection_model). |
| `create_ocv_proj` | OCV(광학 문자 검증)용 평균 템플릿 모델(create_ocv_proj). |
| `create_texture_inspection_model` | 텍스처 검사 모델(정상 샘플의 국소 통계 분포)(create_texture_inspection_model). |
| `create_variation_model` | 양품 이미지 군으로부터 픽셀별 평균·표준편차의 variation model을 만든다(create_variation_model). |

#### Morphology(8 op)

| op | 설명 |
|---|---|
| `bottom_hat` | closing(region) - region: 작은 어두운 구조(틈)를 추출(bottom_hat). |
| `erosion2` | 참조점 (row,col) 포함 구조 요소에 의한 침식(erosion2). |
| `hit_or_miss` | hit-or-miss 변환: 전경을 disc로 erode ∧ 배경을 disc로 erode(hit_or_miss). 모서리/고립점 검출. |
| `minkowski_add1` | Minkowski 합(구조 요소로 팽창)(minkowski_add1). |
| `minkowski_add2` | 반복 Minkowski 합(minkowski_add2). |
| `minkowski_sub1` | Minkowski 차(구조 요소로 침식)(minkowski_sub1). |
| `minkowski_sub2` | 반복 Minkowski 차(minkowski_sub2). |
| `top_hat` | region - opening(region): 작은 밝은 구조를 추출(top_hat). |

#### color(8 op)


![fops_color](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_color.png)
*그림: color의 실제 처리 예 — "빨간 물체만 고르기"는 휘도 이미지로는 원리적으로 불가능(등휘도라면 이진화로 구별 불가)하지만, trans_from_rgb로 HSV로 변환해 H(색상) 채널을 임계값 처리하면 조명의 명암과 무관하게 색으로 고를 수 있다(Fullseye 실제 출력). 입력은 AI 생성 이미지(Gemini) 2종+등휘도 자체 합성 1종.*

| op | 설명 |
|---|---|
| `access_channel` | color op(HALCON: access_channel) |
| `cfa_to_rgb` | color op(HALCON: cfa_to_rgb) |
| `linear_trans_color` | color op(HALCON: linear_trans_color) |
| `principal_comp` | color op(HALCON: principal_comp) |
| `rgb1_to_gray` | color op(HALCON: rgb1_to_gray) |
| `rgb3_to_gray` | color op(HALCON: rgb3_to_gray) |
| `trans_from_rgb` | color op(HALCON: trans_from_rgb) |
| `trans_to_rgb` | color op(HALCON: trans_to_rgb) |

#### events(8 op)

| op | 설명 |
|---|---|
| `contrast_maximization` | 콘트라스트 최대화(contrast maximisation, Gallego et al. 2018)로 전역 옵티컬 플로를 추정한다. |
| `event_count` | 픽셀별 부호 있는 콘트라스트 횡단 횟수 sign(d)*floor(abs(d)/thr). |
| `event_image` | 이벤트를 누적한 이미지(IWE)를 만든다. |
| `event_rate` | 전체의 이벤트 활성 = 1회 이상 발화한 픽셀의 비율. |
| `event_rate_map` | 발화 마스크를 평활화한 국소 이벤트 밀도 맵 [0,1]. |
| `simulate_events` | 2프레임 간의 부호 있는 이벤트 극성 맵을 생성한다. |
| `time_surface` | (T,H,W) 스택으로부터 Surface of Active Events(SAE)를 계산한다. |
| `warp_frame` | 프레임을 (dy,dx)만큼 시프트한다(움직임 보상용, 쌍선형). |

#### grasp(8 op)

| op | 설명 |
|---|---|
| `approach_vector_from_normals` | 파지 축에 직교하는 그리퍼 접근 방향(단위 벡터)을 구한다. |
| `collision_free` | 손가락 스위프의 대략적인 간섭 체크(근사). |
| `ferrari_canny_quality` | Ferrari-Canny의 ε 파지 품질의 근사 계산. |
| `force_closure` | 2지 대척 force-closure(힘 가둠) 판정(Nguyen 1988). |
| `grasp_pose` | 파지의 4x4 그리퍼 좌표계(강체 pose)를 조립한다. |
| `grasps_from_mesh` | 메시 표면을 점군화한 뒤 파지 후보를 제안하는 일괄판. |
| `rank_grasps` | 파지 후보를 품질 내림차순으로 정렬한다(최선이 선두). |
| `sample_antipodal_grasps` | 점군으로부터 2지 대척 파지 후보를 스코어 포함으로 제안한다. |

#### measure(8 op)


![fops_measure](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_measure.png)
*그림: measure의 실제 처리 예 — BGA 솔더 볼의 X선 투과 검사(감쇠 투영+보이드 주입의 자체 합성 2종+AI 생성 1종): 볼마다 내부의 밝은 픽셀을 보이드로 보고 면적률을 계측해 참값과 대조(Fullseye 실제 출력). 검사 장비 업계의 실무에 가까운 소재.*

| op | 설명 |
|---|---|
| `angle` | 선분 p0→p1의 각도 [deg](이미지 y 아래 방향, (-180,180]). |
| `distance` | 2점 (row,col) 간의 유클리드 거리. |
| `fit_circle` | (row,col) 점열에 대한 대수적 최소제곱 원 피팅(Kåsa/Coope). |
| `fit_ellipse` | 직접 최소제곱의 타원 피팅(Halir & Flusser 1998). |
| `fit_line` | 전최소제곱의 직선 피팅(직교 회귀). |
| `fit_rectangle2` | 면적 최소의 유향 외접 직사각형 피팅. |
| `line_profile` | 선분 p0→p1을 따르는 휘도 프로파일(쌍선형 샘플). |
| `profile_stats` | 프로파일의 min/max/mean과 최강 에지(그래디언트 피크)의 위치. |

#### segment(8 op)

| op | 설명 |
|---|---|
| `Watershed` | 마커 제어 watershed 분할(cv2.watershed, 부재 시 skimage, 없으면 numpy)  [backend=opencv] |
| `sg_felzenszwalb` | segment op(HALCON: -) |
| `sg_gmm_segment` | segment op(HALCON: -) |
| `sg_kmeans_intensity` | segment op(HALCON: -) |
| `sg_normalized_cut_2` | segment op(HALCON: -) |
| `sg_region_growing_seeded` | segment op(HALCON: -) |
| `sg_slic_superpixels` | segment op(HALCON: -) |
| `sg_watershed_gradient` | segment op(HALCON: -) |

#### 1D Measuring(7 op)


![fops_measuring1d](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_measuring1d.png)
*그림: 1D Measuring의 실제 처리 예 — 나이테도 물고기 이석의 윤문도 같은 도구로 셀 수 있다: polar_trans_image로 펼치기 → 각도 평균의 1D 프로파일 → smooth_funct_1d_gauss+local_min_max_funct_1d로 피크 계수. 참값이 있는 합성으로 계수 정밀도를 확인(Fullseye 실제 출력). 입력은 합성+AI 생성(Gemini) 2종.*

| op | 설명 |
|---|---|
| `create_funct_1d_pairs` | (x,y) 쌍으로부터 등간격 1D 함수로 재표본화(create_funct_1d_pairs). |
| `fuzzy_measure_pairing` | 퍼지 기준(상정 폭 pair_size)에 가장 맞는 에지 쌍을 고른다(fuzzy_measure_pairing). |
| `gen_measure_arc` | 측정 호(원주 방향으로 프로파일을 얻는다)를 정의(gen_measure_arc). |
| `gen_measure_rectangle2` | 회전 측정 직사각형(장축을 따라 프로파일을 얻는다)을 정의(gen_measure_rectangle2). |
| `measure_pairs` | 상승/하강 에지의 쌍(구조의 폭)을 추출(measure_pairs). |
| `measure_pos` | 측정선 위의 에지 위치(서브픽셀)와 진폭을 추출(measure_pos). |
| `translate_measure` | 측정 오브젝트를 평행 이동(translate_measure). |

#### 3d(7 op)

| op | 설명 |
|---|---|
| `vol_dilate` | 3d op(HALCON: -) |
| `vol_erode` | 3d op(HALCON: -) |
| `vol_gaussian` | 3d op(HALCON: -) |
| `vol_median` | 3d op(HALCON: -) |
| `vol_mip` | 3d op(HALCON: -) |
| `vol_slice` | 3d op(HALCON: -) |
| `vol_threshold` | 3d op(HALCON: -) |

#### decomposition(7 op)

| op | 설명 |
|---|---|
| `dc_homomorphic` | decomposition op(HALCON: -) |
| `dc_local_contrast_norm` | decomposition op(HALCON: -) |
| `dc_retinex` | decomposition op(HALCON: -) |
| `dc_rpca_lowrank` | decomposition op(HALCON: -) |
| `dc_rpca_sparse` | decomposition op(HALCON: -) |
| `dc_structure_texture` | decomposition op(HALCON: -) |
| `dc_texture_residual` | decomposition op(HALCON: -) |

#### flow(7 op)


![fops_flow](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_flow.png)
*그림: flow의 실제 처리 예 — "이상적인 하이스피드 카메라"=자체 탄도 시뮬레이션 연속 프레임(dt=1/240s 기지, 실제 카메라의 롤링 셔터/모션 블러는 포함하지 않음)에서 frame_difference로 움직이는 물체를 검출 → 무게중심 추적 → 포물선 피팅으로 중력가속도 g를 추정해 참값 9.81 m/s²와 대조(Fullseye 실제 출력). 동영상에서 물리 상수를 재는 하이스피드 해석의 실무.*

| op | 설명 |
|---|---|
| `Farneback` | 조밀 옵티컬 플로(cv2.calcOpticalFlowFarneback, 부재 시 Horn-Schunck numpy)  [backend=opencv] |
| `flow_angle` | 픽셀별 운동 방향 atan2(v,u) [rad]. |
| `flow_magnitude` | 픽셀별 속력 sqrt(u^2+v^2). |
| `optical_flow_hs` | 조밀한 Horn-Schunck 옵티컬 플로(전역 평활성). |
| `optical_flow_lk` | 조밀한 피라미드 Lucas-Kanade 플로. |
| `track_points` | 성긴 점을 prev→nxt로 추적한다(Lucas-Kanade 점 트래커). |
| `warp_by_flow` | 플로에 따라 이미지를 전방 워프한다. |

#### motion(7 op)

| op | 설명 |
|---|---|
| `detect_events` | 움직임 에너지 신호의 스파이크 위치(이벤트)를 검출한다. |
| `dominant_motion` | 전역 아핀 운동 모델을 최소제곱으로 피팅한다. |
| `flow_from_model` | 아핀 운동 모델 M으로부터 (u,v) 플로 장을 생성한다. |
| `frame_motion_energy` | 플로 장의 RMS 속력 = 프레임 쌍마다 1 스칼라. |
| `motion_energy_series` | 인접 프레임 쌍마다의 움직임 에너지 계열. |
| `motion_segments` | 플로 장으로부터 독립적으로 움직이는 영역을 분할한다. |
| `residual_motion` | 전역(카메라) 운동을 제거한 잔차 플로 = 독립 물체의 움직임. |

#### registration(7 op)

| op | 설명 |
|---|---|
| `apply_transform` | 모든 점에 강체 변환 R·p + t 를 적용한다. |
| `feature_register` | FPFH 특징 + RANSAC(+ICP 정밀화)에 의한 대응 기반 정합. |
| `icp` | ICP(반복 최근접점법): 대응 미지 상태로 src를 dst로 정합. |
| `kabsch` | 대응 완료 점 쌍의 최적 강체 변환(Kabsch 법). |
| `pca_align` | 주축으로부터 대략적인 강체 정합(ICP의 한 방 초기화). |
| `point_to_plane_icp` | point-to-plane ICP: 법선 방향의 거리를 최소화하는 정합. |
| `register` | pca_align의 대회전 초기화부터 ICP까지 통과시키는 강건 일괄 정합. |

#### render3d(7 op)

| op | 설명 |
|---|---|
| `auto_view` | 메시의 외접구가 들어가도록 (pose, K)를 자동 프레이밍한다. |
| `intrinsics_from_fov` | 수직 시야각으로부터 핀홀 내부 행렬 K를 만든다. |
| `look_at` | eye에서 target을 보는 카메라의 4x4 world→camera pose를 만든다. |
| `marching_cubes` | 스칼라 체로부터 등치면의 삼각형 메시를 추출한다(마칭 큐브). |
| `mesh_to_sdf` | 수밀 메시의 부호 있는 거리장 (sdf, origin)을 계산한다. |
| `render_mesh` | 삼각형 메시를 깊이·실루엣·법선 맵으로 래스터라이즈한다. |
| `voxelize_solid` | 수밀 메시의 내부까지 채운 복셀 점유 (occ, origin)를 계산한다. |

#### sceneflow(7 op)

| op | 설명 |
|---|---|
| `ego_translation_from_flow` | 병진 플로 장으로부터 카메라 병진 방향(진행 방위)을 추정한다. |
| `flow_curl` | 플로 장의 회전(와도) dv/dx - du/dy(픽셀별). |
| `flow_divergence` | 플로 장의 발산 du/dx + dv/dy(픽셀별). |
| `focus_of_expansion` | 확장 초점(FOE): 병진 시 플로가 방사상으로 솟아나는 이미지 위의 점. |
| `looming` | 플로 장으로부터 접근(충돌 임박)의 전체 지표를 요약한다. |
| `scene_flow` | 스테레오+옵티컬 플로 쌍으로부터 픽셀별 3D 신 플로(Vedula 1999). |
| `time_to_contact` | 픽셀별 접촉까지의 시간 τ [프레임](Lee 1976). |

#### physics(6 op)

| op | 설명 |
|---|---|
| `ph_coherence_enhancing_diffusion` | physics op(HALCON: -) |
| `ph_heat_flow` | physics op(HALCON: -) |
| `ph_mean_curvature_motion` | physics op(HALCON: -) |
| `ph_perona_malik` | physics op(HALCON: -) |
| `ph_reaction_diffusion` | physics op(HALCON: -) |
| `ph_total_variation_flow` | physics op(HALCON: -) |

#### raster(6 op)

| op | 설명 |
|---|---|
| `read_depth` | 계량 깊이 맵을 읽어 들인다 (depth, valid). |
| `read_pfm` | PFM(Portable Float Map)을 읽어 들인다 (arr, scale). |
| `read_raster` | 네이티브 비트 깊이를 유지한 채 래스터를 읽어 들인다 (arr, meta). |
| `save16` | 확장자에 따른 형식으로 고정밀도 그대로 써낸다. |
| `to01` | 원시 값을 건드리지 않고 [0,1]의 float64 뷰를 반환한다. |
| `write_pfm` | PFM을 써낸다((H,W)는 그레이, (H,W,3)은 컬러). |

#### subpix(6 op)

| op | 설명 |
|---|---|
| `sp_critical_points_sub_pix` | subpix op(HALCON: critical_points_sub_pix) |
| `sp_local_max_sub_pix` | subpix op(HALCON: -) |
| `sp_local_min_sub_pix` | subpix op(HALCON: local_min_sub_pix) |
| `sp_lowlands_center` | subpix op(HALCON: lowlands_center) |
| `sp_plateaus` | subpix op(HALCON: plateaus) |
| `sp_saddle_points_sub_pix` | subpix op(HALCON: saddle_points_sub_pix) |

#### detect(5 op)


![fops_detect](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_detect.png)
*그림: detect의 실제 처리 예 — "나누고(segment_objects)→재고(개체별 특징량)→분류하는(클러스터 색 구분)" 3단 활용(Fullseye 실제 출력+numpy k-means). 클러스터는 비지도 그룹 나누기이며 종별 동정이 아니다. 허블 딥 필드는 NASA/STScI(scikit-image 동봉, 퍼블릭 도메인).*

| op | 설명 |
|---|---|
| `draw_objects` | 각 물체의 마스크 채색 + bbox 그리기의 RGB 시각화를 반환한다. |
| `feature_table` | 물체별 특징 목록(면적·원형도·이심률·무게중심)을 만든다. |
| `nearest_prototype` | 기술자를 최근접 프로토타입 {label: 기술자}로 분류한다. |
| `object_descriptor` | 식별용의 스케일·회전 강건 콤팩트 기술자(Hu의 7 모멘트 등). |
| `segment_objects` | 전경 물체를 분할하고, 연결 성분별 레코드를 반환한다. |

#### locomotion(5 op)

| op | 설명 |
|---|---|
| `com_from_silhouette` | 이진 실루엣의 무게중심 (row,col)을 반환한다. |
| `com_support_margin` | 정적 안정 여유: 무게중심의 접지 투영으로부터 지지 다각형 경계까지의 부호 있는 거리. |
| `contact_points` | 지면 평면에서 tol 이내에 있는 점 = 접지점을 추출한다. |
| `gait_phase` | 발 높이로부터 각 프레임의 입각/유각을 분류한다. |
| `support_polygon` | 접지점의 볼록 지지 다각형(지면 x,y 평면)을 구한다. |

#### measure1d(5 op)

| op | 설명 |
|---|---|
| `m1_fuzzy_measure_pos` | measure1d op(HALCON: fuzzy_measure_pos) |
| `m1_measure_pairs` | measure1d op(HALCON: measure_pairs) |
| `m1_measure_pos` | measure1d op(HALCON: measure_pos) |
| `m1_measure_projection` | measure1d op(HALCON: measure_projection) |
| `m1_measure_thresh` | measure1d op(HALCON: measure_thresh) |

#### occupancy(5 op)

| op | 설명 |
|---|---|
| `clearance_map` | 각 셀에서 최근접 장애물까지의 거리 맵(월드 단위). |
| `frontier_cells` | 탐사용 프런티어 셀: 미지 영역에 접하는 자유 셀. |
| `inflate_obstacles` | 점유 셀을 radius_cells 만큼 팽창한다(배치 공간의 장애물). |
| `line_of_sight` | 2셀 간의 직선이 장애물을 가로지르지 않으면 True. |
| `occupancy_grid_2d` | 3D 점군을 위에서 본 2D 점유 그리드로 집약한다. |

#### odometry(5 op)

| op | 설명 |
|---|---|
| `integrate_trajectory` | 상대 운동의 열을 합성해 절대 4x4 pose 열로 만든다. |
| `pnp_odometry` | 이전 프레임의 3D 점을 현재 프레임에서 본 대응으로부터 PnP로 카메라 운동을 추정한다. |
| `rgbd_odometry` | RGB-D 쌍 + 옵티컬 플로로부터 프레임 간 카메라 운동을 추정한다. |
| `trajectory_error` | 추정 궤적과 참값 궤적의 절대 궤적 오차(ATE). |
| `umeyama_align` | Umeyama의 최소제곱 상사 변환으로 src 점군을 dst에 정렬한다. |

#### pointcloud(5 op)

| op | 설명 |
|---|---|
| `estimate_normals` | k 근방의 국소 PCA로 점별 법선을 추정한다. |
| `fpfh` | 점별 FPFH(Fast Point Feature Histogram) 기술자(Rusu 2009). |
| `remove_radius_outliers` | radius 내의 근방 수가 min_neighbors 미만인 점을 제거한다. |
| `remove_statistical_outliers` | k 근방 평균 거리가 전체 분포에서 벗어난 점을 제거한다(통계적 이상치 제거). |
| `voxel_downsample` | 점유 복셀마다 1점(셀 무게중심)으로 솎아낸다. |

#### tactile(5 op)

| op | 설명 |
|---|---|
| `tac_contact_mask` | tactile op(HALCON: -) |
| `tac_height_from_shading` | tactile op(HALCON: -) |
| `tac_pressure_proxy` | tactile op(HALCON: -) |
| `tac_shear_field` | tactile op(HALCON: -) |
| `tac_surface_normal` | tactile op(HALCON: -) |

#### tomography(5 op)

| op | 설명 |
|---|---|
| `tm_backproject_unfiltered` | tomography op(HALCON: -) |
| `tm_fbp_reconstruct` | tomography op(HALCON: -) |
| `tm_radon_forward` | tomography op(HALCON: -) |
| `tm_sart_reconstruct` | tomography op(HALCON: -) |
| `tm_sinogram_denoise` | tomography op(HALCON: -) |

#### deformreg(4 op)

| op | 설명 |
|---|---|
| `demons_register` | Thirion의 demons 법으로 moving을 fixed로 비강체 정합한다. |
| `field_magnitude` | 픽셀별 변위 길이 sqrt(fx^2+fy^2). |
| `residual_ssd` | 2 이미지의 휘도 차의 제곱합(0 = 동일). |
| `warp_by_field` | 변위장 (fx,fy)로 이미지를 워프한다(쌍선형, 끝은 클램프). |

#### macro(4 op)

| op | 설명 |
|---|---|
| `macro_binarize` | macro op(HALCON: -) |
| `macro_denoise` | macro op(HALCON: -) |
| `macro_edge` | macro op(HALCON: -) |
| `macro_vol_denoise` | macro op(HALCON: -) |

#### pose(4 op)

| op | 설명 |
|---|---|
| `pose_descriptor` | 골격 그래프와 주축을 조합한 콤팩트한 자세 기술자. |
| `principal_axis` | 전경 픽셀의 PCA에 의한 도형의 주축. |
| `skeleton_nodes` | 골격의 끝점 수·분기점 수를 센다. |
| `skeletonize_mask` | 이진 도형의 1픽셀 폭 모폴로지 골격화. |

#### artistic(3 op)

| op | 설명 |
|---|---|
| `xcv_pencil_sketch` | artistic op(HALCON: -) |
| `xcv_stylization` | artistic op(HALCON: -) |
| `xpil_emboss` | artistic op(HALCON: -) |

#### deformation(3 op)

| op | 설명 |
|---|---|
| `deform_ffd` | deformation op(HALCON: -) |
| `deform_mls` | deformation op(HALCON: -) |
| `deform_tps` | deformation op(HALCON: -) |

#### ppf(3 op)

| op | 설명 |
|---|---|
| `find_surface_pose` | 모델 기술자의 구축과 장면 대조를 한 번에 수행하는 일괄판. |
| `ppf_model` | 모델 점군의 Point Pair Feature 기술자(해시 표)를 구축한다. |
| `surface_match` | PPF 투표 + ICP 정밀화로 장면 안 모델의 6자유도 pose를 탐색한다. |

#### sim-source(3 op)

| op | 설명 |
|---|---|
| `Gazebo` | Gazebo sim-source(미연결 scaffold). gz-transport 브리지로 RGB/depth/참값을 공급 예정.  [sim=gazebo, scaffold] |
| `IsaacSim` | Isaac Sim sim-source(미연결 scaffold). omni.replicator 브리지로 공급 예정.  [sim=isaacsim, scaffold] |
| `MuJoCo` | MuJoCo sim-source: RGB/깊이를 렌더링하고, K를 산출, 참값 자세를 내고, 깊이를 역투영해  [sim=mujoco, available] |

#### transform(3 op)

| op | 설명 |
|---|---|
| `tf_radon_sinogram` | transform op(HALCON: -) |
| `xmh_daubechies` | transform op(HALCON: -) |
| `xmh_haar` | transform op(HALCON: -) |
