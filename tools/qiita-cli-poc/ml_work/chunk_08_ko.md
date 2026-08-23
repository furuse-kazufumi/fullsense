#### Matrix(46 op)

행렬 연산·연립방정식·분해(SVD 등). 카메라 캘리브레이션과 자세 추정의 수학적 뒷받침이다.

| op | 설명 |
|---|---|
| `abs_matrix` | 행렬 각 요소의 절댓값을 계산한다. |
| `abs_matrix_mod` | 요소별 절댓값(결과를 입력 행렬에 덮어쓴다). |
| `add_matrix` | 두 행렬을 더한다. |
| `add_matrix_mod` | 행렬 덧셈(결과를 입력 행렬에 덮어쓴다). |
| `create_matrix` | 새 행렬을 생성한다. |
| `decompose_matrix` | LU 분해(P,L,U)를 반환한다(decompose_matrix). |
| `determinant_matrix` | 행렬식을 계산한다. |
| `div_element_matrix` | 행렬끼리 요소별로 나눈다. |
| `div_element_matrix_mod` | 요소별 나눗셈(결과를 입력 행렬에 덮어쓴다). |
| `eigenvalues_general_matrix` | 일반 행렬의 고유값(필요하면 고유벡터도)을 계산한다. |
| `eigenvalues_symmetric_matrix` | 대칭 행렬의 고유값(필요하면 고유벡터도)을 계산한다. |
| `generalized_eigenvalues_general_matrix` | 일반 행렬 쌍의 일반화 고유값(필요하면 고유벡터도)을 계산한다. |
| `generalized_eigenvalues_symmetric_matrix` | 대칭 행렬 쌍의 일반화 고유값(필요하면 고유벡터도)을 계산한다. |
| `get_diagonal_matrix` | 행렬의 대각 요소를 꺼낸다. |
| `get_sub_matrix` | 부분 행렬을 꺼낸다. |
| `invert_matrix` | 역행렬을 계산한다. |
| `invert_matrix_mod` | 역행렬(결과를 입력 행렬에 덮어쓴다). |
| `max_matrix` | 행렬 요소의 최댓값을 반환한다. |
| `mean_matrix` | 행렬 요소의 평균을 반환한다. |
| `min_matrix` | 행렬 요소의 최솟값을 반환한다. |
| `mult_element_matrix` | 행렬끼리 요소별로 곱한다. |
| `mult_element_matrix_mod` | 요소별 곱셈(결과를 입력 행렬에 덮어쓴다). |
| `mult_matrix` | 두 행렬의 곱을 계산한다. |
| `mult_matrix_mod` | 행렬 곱(결과를 입력 행렬에 덮어쓴다). |
| `norm_matrix` | 행렬의 노름을 계산한다. |
| `orthogonal_decompose_matrix` | QR 직교 분해를 반환한다(orthogonal_decompose_matrix). |
| `pow_element_matrix` | 행렬의 각 요소를 거듭제곱한다. |
| `pow_element_matrix_mod` | 요소별 거듭제곱(결과를 입력 행렬에 덮어쓴다). |
| `pow_matrix` | 행렬 자체의 거듭제곱을 계산한다. |
| `pow_matrix_mod` | 행렬 거듭제곱(결과를 입력 행렬에 덮어쓴다). |
| `pow_scalar_element_matrix` | 스칼라를 밑으로, 각 요소를 지수로 하는 거듭제곱을 요소별로 계산한다. |
| `pow_scalar_element_matrix_mod` | 스칼라 밑의 요소 거듭제곱(결과를 입력 행렬에 덮어쓴다). |
| `repeat_matrix` | 행렬을 타일 형태로 반복해 배열한다. |
| `scale_matrix` | 행렬을 스칼라배한다. |
| `scale_matrix_mod` | 스칼라배(결과를 입력 행렬에 덮어쓴다). |
| `set_diagonal_matrix` | 행렬의 대각 요소를 설정한다. |
| `set_sub_matrix` | 부분 행렬을 써넣는다. |
| `solve_matrix` | 연립 일차방정식의 해를 계산한다. |
| `sqrt_matrix` | 행렬 각 요소의 제곱근을 계산한다. |
| `sqrt_matrix_mod` | 요소별 제곱근(결과를 입력 행렬에 덮어쓴다). |
| `sub_matrix` | 두 행렬을 뺀다. |
| `sub_matrix_mod` | 행렬 뺄셈(결과를 입력 행렬에 덮어쓴다). |
| `sum_matrix` | 행렬 요소의 총합을 반환한다. |
| `svd_matrix` | 특이값 분해(SVD)를 계산한다. |
| `transpose_matrix` | 행렬을 전치한다. |
| `transpose_matrix_mod` | 전치(결과를 입력 행렬에 덮어쓴다). |

#### 3D Reconstruction(43 op)

깊이·시차·다시점으로부터의 3D 복원. 2.5D(깊이 이미지)에서 점군·메시의 세계로 건너가는 다리다.

![3D Reconstruction 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_16_depth_to_points.png)
*그림: 깊이 → 점군 예(11.1.1절에서 재수록)*

| op | 설명 |
|---|---|
| `apply_sheet_of_light_calibration` | 프로파일(픽셀 행)을 높이(메트릭)로 환산(apply_sheet_of_light_calibration). |
| `binocular_disparity` | Semi-Global Matching에 의한 스테레오 시차 추정(Hirschmüller 법). |
| `binocular_disparity_mg` | 승자 독식 블록 매칭에 의한 조밀한 시차 추정. |
| `binocular_disparity_ms` | SGM 시차 추정의 다른 입구(구현은 Hirschmüller 법). |
| `binocular_distance` | 시차로부터 계량 깊이 Z = f·B/d 를 계산한다. |
| `binocular_distance_mg` | 시차→계량 깊이 Z = f·B/d(mg 입구). |
| `binocular_distance_ms` | 시차→계량 깊이 Z = f·B/d(ms 입구). |
| `calibrate_sheet_of_light` | 기지의 단차로부터 시트광의 픽셀→높이 스케일을 캘리브레이션(calibrate_sheet_of_light). |
| `create_sheet_of_light_calib_object` | 시트광 캘리브레이션 오브젝트(기지의 단차)(create_sheet_of_light_calib_object). |
| `create_sheet_of_light_model` | 시트광(레이저 라인) 프로파일 계측 모델(create_sheet_of_light_model). |
| `create_stereo_model` | 스테레오 계측 모델(좌우 내부 + 상대 자세)(create_stereo_model). |
| `create_structured_light_model` | 구조광 계측 모델(위상 시프트 패턴 설정)(create_structured_light_model). |
| `decode_structured_light_pattern` | 위상 시프트 구조광의 이미지 열에서 절대 위상(=대응)을 복호(decode_structured_light_pattern). |
| `depth_from_focus` | 포커스 스택에서 픽셀별 최적 초점 위치=깊이를 추정(depth_from_focus). |
| `disparity_to_distance` | 시차 d를 거리 Z = f*baseline/d 로 변환(disparity_to_distance). |
| `disparity_to_point_3d` | 이미지 점 (row,col)과 시차 disparity로부터 3D 점 (X,Y,Z)를 계산(disparity_to_point_3d). |
| `distance_to_disparity` | 거리 Z를 시차 d = f*baseline/Z 로 변환(distance_to_disparity). |
| `essential_to_fundamental_matrix` | 기초 행렬 F = K2^-T E K1^-1 를 본질 행렬 E로부터 계산(essential_to_fundamental_matrix). |
| `gen_binocular_proj_rectification` | 기초 행렬로부터 스테레오 평행화를 위한 에피폴 정렬 변환을 추정 |
| `gen_binocular_rectification_map` | 캘리브레이션 완료 스테레오 페어의 평행화 회전을 계산한다(Fusiello 법). |
| `gen_structured_light_pattern` | 정현파 구조광 패턴 이미지를 생성(gen_structured_light_pattern). |
| `intersect_lines_of_sight` | 2시점의 대응 픽셀을 선형 DLT 삼각측량으로 3D 복원한다. |
| `match_essential_matrix_ransac` | 점 대응과 내부 행렬 K로부터 RANSAC으로 본질 행렬 E를 추정(match_essential_matrix_ransac). |
| `match_fundamental_matrix_distortion_ransac` | 왜곡 포함 기초 행렬의 RANSAC 추정(match_fundamental_matrix_distortion_ransac). |
| `match_fundamental_matrix_ransac` | 점 대응으로부터 RANSAC으로 기초 행렬 F와 인라이어를 추정(match_fundamental_matrix_ransac). |
| `match_rel_pose_ransac` | 점 대응으로부터 상대 자세를 RANSAC 추정(match_rel_pose_ransac). |
| `measure_profile_sheet_of_light` | 각 열에서 레이저 라인(최대 휘도)의 행 위치=높이 프로파일을 추출 |
| `photometric_stereo` | 복수 조명 이미지(Lambertian)로부터 법선과 반사율을 복원(photometric_stereo). |
| `reconst3d_from_fundamental_matrix` | 기초 행렬을 거쳐 상대 자세를 분해하고 대응점을 삼각측량(reconst3d_from_fundamental_matrix). |
| `reconstruct_height_field_from_gradient` | 그래디언트 장 (dz/dr, dz/dc)을 Frankot-Chellappa로 적분해 높이 장 z를 복원 |
| `reconstruct_points_stereo` | 좌우 대응점(행 일치)으로부터 시차를 거쳐 3D 점군을 복원(reconstruct_points_stereo). |
| `reconstruct_surface_stereo` | 시차 맵 전체로부터 3D 점군(서피스)을 복원(reconstruct_surface_stereo). |
| `reconstruct_surface_structured_light` | 구조광의 위상 복호 → 시차 → 3D 서피스 복원(reconstruct_surface_structured_light). |
| `rel_pose_to_fundamental_matrix` | 상대 자세 (R,t)와 내부 행렬로부터 기초 행렬 F를 계산(rel_pose_to_fundamental_matrix). |
| `select_grayvalues_from_channels` | index 이미지에 따라 다채널 스택에서 픽셀별로 그레이 값을 고른다 |
| `sfs_mod_lr` | Shape-from-Shading(개량 linear, sfs_mod_lr). Pentland 구현을 공용. |
| `sfs_orig_lr` | Shape-from-Shading(원법 linear, sfs_orig_lr). Pentland 구현을 공용. |
| `sfs_pentland` | Pentland의 선형화 Shape-from-Shading으로 높이 장을 복원(sfs_pentland). |
| `uncalibrated_photometric_stereo` | 광원 방향 미지의 photometric stereo(SVD로 3계수 근사, uncalibrated_photometric_stereo). |
| `vector_to_essential_matrix` | 캘리브레이션 완료 페어의 8쌍 이상 대응으로부터 본질 행렬 E를 추정한다. |
| `vector_to_fundamental_matrix` | 8쌍 이상의 대응으로부터 정규화 8점법으로 기초 행렬 F를 추정한다. |
| `vector_to_fundamental_matrix_distortion` | 왜곡 포함으로 기초 행렬을 RANSAC 추정(왜곡은 작다고 가정하고 정규화 8-point) |
| `vector_to_rel_pose` | 점 대응과 내부 행렬로부터 상대 자세 (R,t)를 추정(본질 행렬 분해)(vector_to_rel_pose). |

#### 3D Object Model(40 op)

점군·메시(3D 오브젝트 모델) 조작. 변환·법선·간략화·특징량 등.

| op | 설명 |
|---|---|
| `affine_trans_object_model_3d` | 모든 점에 강체 변환 R·p + t 를 적용한다. |
| `area_object_model_3d` | 3D 점군의 볼록 껍질 표면적을 반환한다(area_object_model_3d). |
| `connection_object_model_3d` | 유클리드 클러스터링으로 근접 점을 그룹화한다(Rusu 2009). |
| `convex_hull_object_model_3d` | 3D 볼록 껍질의 꼭짓점을 반환한다(convex_hull_object_model_3d). |
| `distance_object_model_3d` | 두 3D 모델 간의 최소 점 간 거리(distance_object_model_3d). |
| `edges_object_model_3d` | 국소 곡률이 높은 점=3D 에지를 추출(edges_object_model_3d). 근방 PCA의 평면성으로 판정. |
| `fit_primitives_object_model_3d` | RANSAC으로 지배 평면을 강건하게 피팅한다. |
| `fuse_object_model_3d` | 복수 3D 모델을 하나로 통합(fuse_object_model_3d). |
| `gen_box_object_model_3d` | 상자 6면의 점군(gen_box_object_model_3d). |
| `gen_cylinder_object_model_3d` | 원기둥 측면의 점군(gen_cylinder_object_model_3d). |
| `gen_empty_object_model_3d` | 빈 3D 모델(gen_empty_object_model_3d). |
| `gen_object_model_3d_from_points` | x,y,z 배열로부터 3D 점군 모델을 만든다(gen_object_model_3d_from_points). |
| `gen_plane_object_model_3d` | z=0 평면 위의 격자 점군(gen_plane_object_model_3d). |
| `gen_sphere_object_model_3d` | 구면 위의 준균일 점군(황금 나선, gen_sphere_object_model_3d). |
| `gen_sphere_object_model_3d_center` | 중심 지정 구면 점군(gen_sphere_object_model_3d_center). |
| `intersect_plane_object_model_3d` | 평면(a,b,c,d) 근방(거리<tol)의 점=단면을 반환(intersect_plane_object_model_3d). |
| `max_diameter_object_model_3d` | 점군의 최대 지름(볼록 껍질 위에서 가장 먼 2점, max_diameter_object_model_3d). |
| `moments_object_model_3d` | 3D 점군의 무게중심과 공분산(2차 중심 모멘트)을 반환(moments_object_model_3d). |
| `object_model_3d_to_xyz` | 3D 점군을 X/Y/Z 이미지로(격자 순서, object_model_3d_to_xyz). |
| `prepare_object_model_3d` | 법선 추정 포함 모델 전처리(근방 PCA, prepare_object_model_3d). |
| `project_object_model_3d` | 월드 점군 (N,3)을 픽셀로 투영해 (uv, depth)를 반환한다. |
| `projective_trans_object_model_3d` | 4x4 사영 변환을 적용(projective_trans_object_model_3d). 기본은 항등. |
| `reduce_object_model_3d_by_view` | 지정 축에서 앞쪽 keep 비율의 점만 남긴다(시점에 의한 간이 솎아내기, reduce_object_model_3d_by_view). |
| `register_object_model_3d_global` | point-to-plane ICP: 법선 방향 거리를 최소화해 src를 dst로 정합. |
| `register_object_model_3d_pair` | ICP(반복 최근접점법): 대응 미지 상태로 src를 dst로 정합. |
| `render_object_model_3d` | 3D 모델을 이미지로 렌더링(깊이로 명암, render_object_model_3d). |
| `rigid_trans_object_model_3d` | 4x4 강체/상사 변환을 점군에 적용(rigid_trans_object_model_3d). |
| `sample_object_model_3d` | 점유 복셀마다 1점(셀 무게중심)으로 솎아내는 다운샘플링. |
| `segment_object_model_3d` | 근방 거리로 점군을 연결 성분으로 분할(segment_object_model_3d). 라벨 배열을 반환. |
| `select_object_model_3d` | 속성 값 범위로 점을 선택(select_object_model_3d). |
| `select_points_object_model_3d` | 지정 축의 값 범위로 점을 고른다(select_points_object_model_3d). |
| `simplify_object_model_3d` | 복셀 그리드 평균으로 점군을 간략화(simplify_object_model_3d). |
| `smallest_bounding_box_object_model_3d` | PCA에 의한 유향 바운딩 박스를 구한다. |
| `smallest_sphere_object_model_3d` | 최소 포함구의 근사(중심=무게중심, 반지름=최원점, smallest_sphere_object_model_3d). |
| `smooth_object_model_3d` | 각 점을 k 근방의 무게중심으로 이동해 평활화(smooth_object_model_3d). |
| `surface_normals_object_model_3d` | k 근방의 국소 PCA로 점별 법선을 추정한다. |
| `triangulate_object_model_3d` | 주평면에 투영해 Delaunay 삼각분할(triangulate_object_model_3d). 삼각형 꼭짓점 index를 반환. |
| `union_object_model_3d` | 두 3D 모델을 결합(union_object_model_3d). |
| `volume_object_model_3d_relative_to_plane` | 평면 (a,b,c,d)보다 위의 점군 부피를 볼록 껍질로 근사(volume_object_model_3d_relative_to_plane). |
| `xyz_to_object_model_3d` | X/Y/Z 이미지(각 2D)에서 3D 점군 모델로(xyz_to_object_model_3d). |

#### gray(40 op)

그레이스케일 형태학 등, 농담 이미지 그대로 수행하는 형태학적 처리.


![fops_gray](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_gray.png)
*그림: gray의 실제 처리 예 — 조명 얼룩·저대비 입력에서는 전역 히스토그램 균등화가 무너지기(밝은 부분의 화이트 클리핑·노이즈 증폭) 쉬운 반면, clahe(대비 제한 국소 적응 균등화)는 국소별로 계조를 회복한다(Fullseye 실제 출력). 입력은 AI 생성(Gemini) 2종+skimage 동봉 moon.*

| op | 설명 |
|---|---|
| `clahe` | gray op(HALCON: -) |
| `cv_clahe` | gray op(HALCON: -) |
| `cv_trunc` | gray op(HALCON: scale_image) |
| `equ_histo_image` | gray op(HALCON: equ_histo_image) |
| `equ_histo_image_rect` | gray op(HALCON: equ_histo_image_rect) |
| `equalize` | gray op(HALCON: equ_histo_image) |
| `f2_bit_slice` | gray op(HALCON: bit_slice) |
| `f2_expand_domain` | gray op(HALCON: expand_domain_gray) |
| `f2_lut_trans` | gray op(HALCON: lut_trans) |
| `gamma` | gray op(HALCON: pow_image) |
| `gamma_image` | gray op(HALCON: gamma_image) |
| `illuminate` | gray op(HALCON: illuminate) |
| `invert` | gray op(HALCON: invert_image) |
| `invert_image` | gray op(HALCON: invert_image) |
| `it_bit_lshift` | gray op(HALCON: bit_lshift) |
| `it_bit_mask` | gray op(HALCON: bit_mask) |
| `it_bit_rshift` | gray op(HALCON: bit_rshift) |
| `it_convert_image_type` | gray op(HALCON: convert_image_type) |
| `monotony` | gray op(HALCON: monotony) |
| `pow_image` | gray op(HALCON: pow_image) |
| `scale_clip` | gray op(HALCON: scale_image) |
| `scale_image` | gray op(HALCON: scale_image) |
| `scale_image_max` | gray op(HALCON: scale_image_max) |
| `sigmoid` | gray op(HALCON: scale_image_max) |
| `sk_adapthist` | gray op(HALCON: -) |
| `sk_adjust_log` | gray op(HALCON: log_image) |
| `sk_autolevel` | gray op(HALCON: scale_image_max) |
| `sk_enhance_contrast` | gray op(HALCON: -) |
| `xcv_detail_enhance` | gray op(HALCON: -) |
| `xkor_clahe` | gray op(HALCON: -) |
| `xpil_autocontrast` | gray op(HALCON: -) |
| `xpil_contrast` | gray op(HALCON: -) |
| `xpil_detail` | gray op(HALCON: -) |
| `xpil_edge_enhance` | gray op(HALCON: -) |
| `xpil_posterize` | gray op(HALCON: -) |
| `xpil_solarize` | gray op(HALCON: -) |
| `xsk3_integral_image` | gray op(HALCON: -) |
| `xsk3_rank_equalize` | gray op(HALCON: -) |
| `xsk3_rank_subtract_mean` | gray op(HALCON: -) |
| `xsp_detrend_flatten` | gray op(HALCON: -) |

#### Matching(37 op)

템플릿 매칭·형상 매칭. "가르쳐 준 모양을 어디서든 찾아내는" 담당으로, 산업 영상 처리의 꽃이다.

| op | 설명 |
|---|---|
| `adapt_shape_model_high_noise` | 고노이즈용으로 평활화를 강화한 형상 모델을 만든다(adapt_shape_model_high_noise). |
| `create_aniso_shape_model` | 이방성 스케일 형상 모델(create_aniso_shape_model, 모델 자체는 동일, find에서 이방 scale 탐색). |
| `create_aniso_shape_model_xld` | XLD 윤곽으로부터 이방성 스케일 형상 모델(create_aniso_shape_model_xld). |
| `create_calib_descriptor_model` | 캘리브레이션 완료 descriptor 모델(create_calib_descriptor_model). |
| `create_generic_shape_model` | 범용 형상 모델(create_generic_shape_model, create_shape_model과 동일 코어). |
| `create_local_deformable_model` | 국소 변형 매칭용 모델(템플릿 보유)(create_local_deformable_model). |
| `create_local_deformable_model_xld` | XLD 유래의 국소 변형 모델(create_local_deformable_model_xld). |
| `create_ncc_model` | NCC 모델(=정규화 템플릿)을 준비(create_ncc_model). |
| `create_planar_calib_deformable_model` | 평면(캘리브레이션 완료) 변형 모델(create_planar_calib_deformable_model). |
| `create_planar_calib_deformable_model_xld` | XLD 유래의 평면 캘리브레이션 완료 변형 모델(create_planar_calib_deformable_model_xld). |
| `create_planar_uncalib_deformable_model` | 평면(미캘리브레이션) 변형 모델(create_planar_uncalib_deformable_model). |
| `create_planar_uncalib_deformable_model_xld` | XLD 유래의 평면 미캘리브레이션 변형 모델(create_planar_uncalib_deformable_model_xld). |
| `create_scaled_shape_model` | 등방 스케일 형상 모델(create_scaled_shape_model). |
| `create_scaled_shape_model_xld` | XLD 윤곽으로부터 스케일 대응 형상 모델(create_scaled_shape_model_xld). |
| `create_shape_model` | 템플릿의 에지 점(/grad/>min_grad)의 정규화 그래디언트 벡터를 모델화(create_shape_model). |
| `create_shape_model_xld` | XLD 윤곽으로부터 형상 모델을 만든다(create_shape_model_xld). |
| `create_uncalib_descriptor_model` | 미캘리브레이션 descriptor 모델(Harris keypoint + 정규화 패치)(create_uncalib_descriptor_model). |
| `determine_deformable_model_params` | 변형 모델의 권장 파라미터를 결정(determine_deformable_model_params). |
| `determine_ncc_model_params` | NCC 모델의 권장 파라미터(대비/레벨 수)를 결정(determine_ncc_model_params). |
| `determine_shape_model_params` | 템플릿으로부터 권장 min_grad/대비를 자동 결정(determine_shape_model_params). |
| `find_aniso_shape_model` | 행/열 독립 스케일(이방성)로 형상 모델 검출(find_aniso_shape_model). |
| `find_aniso_shape_models` | 이방성 스케일에서의 복수 인스턴스 검출(find_aniso_shape_models). |
| `find_calib_descriptor_model` | 캘리브레이션 완료 descriptor 모델 검출 → 평면 자세(find_calib_descriptor_model). |
| `find_generic_shape_model` | 범용 형상 모델 검출(find_generic_shape_model). find_shape_model의 별칭. |
| `find_local_deformable_model` | 강체 위치를 대략 맞춘 뒤 옵티컬 플로로 국소 변형을 추정 |
| `find_ncc_model` | NCC 모델을 이미지에서 탐색해 최적 일치(행/열/스코어)를 반환(find_ncc_model). |
| `find_ncc_models` | NCC 모델의 복수 인스턴스 검출(find_ncc_models). |
| `find_planar_calib_deformable_model` | 평면 캘리브레이션 완료 변형 모델 검출(find_planar_calib_deformable_model). |
| `find_planar_uncalib_deformable_model` | 평면 미캘리브레이션 변형 모델 검출(find_planar_uncalib_deformable_model). |
| `find_scaled_shape_model` | 스케일을 바꿔 가며 최적 일치를 탐색(find_scaled_shape_model). |
| `find_scaled_shape_models` | 스케일 탐색 포함 복수 인스턴스 검출(find_scaled_shape_models). |
| `find_shape_models` | 복수 인스턴스를 비최대 억제 포함으로 검출(find_shape_models). |
| `find_uncalib_descriptor_model` | descriptor 모델을 이미지에서 검출(비율 테스트 + RANSAC 호모그래피) |
| `get_shape_model_contours` | 형상 모델의 에지 점을 윤곽으로 반환(get_shape_model_contours). |
| `get_shape_model_origin` | 형상 모델의 원점(무게중심)을 반환(get_shape_model_origin). |
| `inspect_shape_model` | 형상 모델의 에지 점 수·퍼짐·원점을 점검용으로 반환(inspect_shape_model). |
| `set_shape_model_origin` | 형상 모델의 참조 원점을 설정(set_shape_model_origin). |

#### XLD(35 op)

XLD = 서브픽셀 정밀도의 윤곽 표현. 픽셀보다 세밀한 정밀도로 윤곽을 다루는, 정밀 계측의 핵심이다.


![fops_xld](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_xld.png)
*그림: XLD의 실제 처리 예 — 이진화한 경계는 픽셀 격자의 계단밖에 되지 않지만, threshold_sub_pix는 레벨 교차 위치를 픽셀보다 세밀하게(서브픽셀) 추정한 윤곽(XLD)을 반환한다. 참값이 있는 합성 원으로 평균 오차 0.001px를 실측. 8배 확대로 계단과 매끄러운 윤곽선의 차이가 보인다(Fullseye 실제 출력). 입력은 자체 합성·AI 생성(Gemini)·skimage coins.*

| op | 설명 |
|---|---|
| `difference_closed_contours_xld` | 2개 폐윤곽의 차(difference_closed_contours_xld). |
| `difference_closed_polygons_xld` | 2개 폐다각형의 차(difference_closed_polygons_xld). |
| `gen_circle_contour_xld` | 원호 윤곽을 생성(gen_circle_contour_xld). |
| `gen_contour_nurbs_xld` | 제어점으로부터 NURBS(B 스플라인) 윤곽을 생성(gen_contour_nurbs_xld). |
| `gen_contour_polygon_rounded_xld` | 모서리를 둥글린 다각형 윤곽을 생성(gen_contour_polygon_rounded_xld). |
| `gen_contour_polygon_xld` | 점열로부터 다각형 윤곽을 생성(gen_contour_polygon_xld). |
| `gen_contours_skeleton_xld` | 영역의 스켈레톤을 추출해 윤곽(가지별)으로 변환(gen_contours_skeleton_xld). |
| `gen_cross_contour_xld` | 십자 마커 윤곽을 생성(gen_cross_contour_xld). |
| `gen_ellipse_contour_xld` | 타원호 윤곽을 생성(gen_ellipse_contour_xld). |
| `gen_nurbs_interp` | 점을 지나는 NURBS 보간 윤곽(gen_nurbs_interp). |
| `gen_parallels_xld` | 각 윤곽에 평행한 오프셋 윤곽을 생성(gen_parallels_xld). |
| `gen_rectangle2_contour_xld` | 회전 직사각형의 윤곽을 생성(gen_rectangle2_contour_xld). |
| `get_contour_angle_xld` | 윤곽을 따라 접선각(라디안)을 각 점에서 반환(get_contour_angle_xld). |
| `get_polygon_xld` | Douglas-Peucker로 윤곽을 다각형 근사(get_polygon_xld). 꼭짓점 열을 반환. |
| `get_regress_params_xld` | 윤곽점에 대한 회귀 직선 파라미터(법선각 nr,nc와 원점 거리 dist)(get_regress_params_xld). |
| `intersection_closed_contours_xld` | 2개 폐윤곽의 곱(intersection_closed_contours_xld). |
| `intersection_closed_polygons_xld` | 2개 폐다각형의 곱(intersection_closed_polygons_xld). |
| `intersection_region_contour_xld` | 영역과 폐윤곽의 교차 영역(intersection_region_contour_xld). |
| `local_max_contours_xld` | 윤곽 위에서 그레이 값이 국소 최대가 되는 점을 추출(local_max_contours_xld). |
| `max_parallels_xld` | 최대 거리까지의 평행 윤곽 군(max_parallels_xld). |
| `merge_cont_line_scan_xld` | 라인 스캔(띠 형태 취득)의 인접 프레임 윤곽 끝점을 연결(merge_cont_line_scan_xld). |
| `mod_parallels_xld` | 평행 윤곽의 생성(파라미터 변경판)(mod_parallels_xld). |
| `moments_any_points_xld` | 윤곽점 집합의 면적·무게중심·2차 모멘트(moments_any_points_xld). |
| `segment_contour_attrib_xld` | 윤곽을, 바탕 그레이 값의 속성이 급변하는 점에서 분할(segment_contour_attrib_xld). |
| `segment_contours_xld` | 윤곽을 직선 선분으로 분할(segment_contours_xld). |
| `symm_difference_closed_contours_xld` | 2개 폐윤곽의 대칭차(symm_difference_closed_contours_xld). |
| `symm_difference_closed_polygons_xld` | 2개 폐다각형의 대칭차(symm_difference_closed_polygons_xld). |
| `test_xld_point` | 점이 폐윤곽 내부에 있는지(교차수 법)(test_xld_point). |
| `union2_closed_contours_xld` | 2개 폐윤곽의 합(union2_closed_contours_xld). |
| `union2_closed_polygons_xld` | 2개 폐다각형의 합(union2_closed_polygons_xld). |
| `union_cocircular_contours_xld` | 공원(같은 원 위)인 윤곽을 통합(union_cocircular_contours_xld). |
| `union_collinear_contours_ext_xld` | 공선 통합(확장 파라미터판)(union_collinear_contours_ext_xld). |
| `union_collinear_contours_xld` | 공선인 윤곽 조각을 통합(union_collinear_contours_xld). |
| `union_cotangential_contours_xld` | 접선 연속인 윤곽을 통합(union_cotangential_contours_xld). |
| `union_straight_contours_xld` | 직선적인 윤곽을 통합(union_straight_contours_xld). |

#### Calibration(34 op)

카메라 캘리브레이션(내부·외부 파라미터, 렌즈 왜곡). "픽셀을 mm로 번역하기" 위한 토대다(본편 14.4의 Brown 왜곡 모델도 여기).

![Calibration 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_12_radial_distortion.png)
*그림: 렌즈 왜곡 모델 예(배럴형/핀쿠션형)(11.1.1절에서 재수록)*

| op | 설명 |
|---|---|
| `affine_trans_point_3d` | 3D 점에 4x4 동차 아핀 변환을 적용(affine_trans_point_3d). |
| `binocular_calibration` | 좌우 카메라를 Zhang 법으로 개별 캘리브레이션하고 스테레오 상대 자세를 추정(binocular_calibration). |
| `calibrate_cameras` | Zhang 법 카메라 캘리브레이션(calibrate_cameras). camera_calibration의 별칭. |
| `calibrate_hand_eye` | 핸드아이 캘리브레이션(calibrate_hand_eye). hand_eye_calibration의 별칭. |
| `caltab_points` | 캘리브레이션 보드의 이상 마크 좌표(월드, mm)를 반환(caltab_points). |
| `cam_mat_to_cam_par` | 내부 행렬 K로부터 fx, fy, cx, cy, skew를 꺼낸다. |
| `cam_par_pose_to_hom_mat3d` | 카메라 포즈 [rx,ry,rz(rad), tx,ty,tz]를 4x4 동차 변환 행렬로 변환(cam_par_pose_to_hom_mat3d). |
| `cam_par_to_cam_mat` | fx, fy, cx, cy, skew로부터 핀홀 내부 행렬 K를 조립한다. |
| `camera_calibration` | Zhang 법으로 평면 타깃 다시점으로부터 내부 행렬 K를 추정(camera_calibration). |
| `change_radial_distortion_cam_par` | 카메라 파라미터의 방사 왜곡 계수를 kappa_new로 치환(change_radial_distortion_cam_par). |
| `change_radial_distortion_image` | 이미지에 방사 왜곡 r' = r(1 + kappa r^2) 를 적용해 리샘플(change_radial_distortion_image). |
| `change_radial_distortion_points` | 이상 픽셀에 반경·접선 방향의 렌즈 왜곡을 부여한다(Brown 모델). |
| `contour_to_world_plane_xld` | XLD 윤곽(dict {cs:[Nx2]})을 world 평면으로 사상(contour_to_world_plane_xld). |
| `create_caltab` | 캘리브레이션 보드의 기술(이상점)을 만든다(create_caltab). |
| `create_pose` | 3D pose를 생성한다. |
| `disp_caltab` | 캘리브레이션 보드 이미지를 반환(표시용)(disp_caltab). |
| `find_calib_object` | 캘리브레이션 오브젝트(마크)를 검출(find_calib_object). find_caltab의 별칭. |
| `find_caltab` | 이미지에서 캘리브레이션 보드의 원 마크 중심을 검출(연결 성분의 무게중심)(find_caltab). |
| `find_marks_and_pose` | 마크 검출 + 캘리브레이션 보드의 자세 추정(PnP 근사=평면 호모그래피)(find_marks_and_pose). |
| `gen_caltab` | 원 마크 격자의 캘리브레이션 보드 이미지를 생성(gen_caltab). |
| `gen_image_to_world_plane_map` | 이미지→월드 평면(z=0)의 사상 테이블을 생성(gen_image_to_world_plane_map). |
| `gen_radial_distortion_map` | 반경 왜곡의 역맵(row_map, col_map)을 생성(gen_radial_distortion_map). |
| `get_line_of_sight` | 픽셀 (row,col)의 시선 방향(정규화 3D 벡터)을 반환(get_line_of_sight). |
| `hand_eye_calibration` | 일련의 운동 쌍으로부터 AX=XB 를 풀어 X(4x4)를 추정(hand_eye_calibration). |
| `image_points_to_world_plane` | 카메라 내부/외부로부터 픽셀을 world 평면 z=0 으로 역투영(image_points_to_world_plane). |
| `image_to_world_plane` | 이미지 점을 평면 호모그래피로 world 평면(z=0)으로 사상(image_to_world_plane). |
| `project_3d_point` | 3D 점을 카메라로 투시 투영해 픽셀 (row, col)을 반환(project_3d_point). |
| `project_hom_point_hom_mat3d` | 동차 3D 점 (4,)를 3x4/4x4 행렬로 투영(project_hom_point_hom_mat3d). |
| `project_point_hom_mat3d` | 4x4 or 3x4 동차 변환으로 3D 점을 변환하고 투영(project_point_hom_mat3d). |
| `projective_trans_point_2d` | 사영 변환 행렬로 동차 2D 점을 사영한다. |
| `radial_distortion_self_calibration` | 본래 직선이어야 할 점열의 잔차를 최소화해 반경 왜곡 kappa를 추정(plumb-line 법) |
| `radiometric_self_calibration` | 노출이 다른 이미지 군으로부터 카메라 응답 함수(역응답 LUT)를 추정 |
| `sim_caltab` | 캘리브레이션 보드를 지정 카메라 자세로 투영한 이미지를 시뮬레이트(sim_caltab). |
| `stationary_camera_self_calibration` | 회전만의 무한원 호모그래피 H = K R K^-1 로부터 내부 행렬 K를 추정 |

#### morphology(33 op)

이진 형태학(팽창·침식·오프닝·클로징). 노이즈 제거와 형태 다듬기의 고전이자 현역.

![morphology 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_06_opening_circle.png)
*그림: 오프닝 예(11.1.1절에서 재수록)*

| op | 설명 |
|---|---|
| `bothat` | morphology op(HALCON: gray_bothat) |
| `cv_blackhat` | morphology op(HALCON: gray_bothat) |
| `cv_close` | morphology op(HALCON: gray_closing) |
| `cv_dilate` | morphology op(HALCON: gray_dilation) |
| `cv_erode` | morphology op(HALCON: gray_erosion) |
| `cv_gradient` | morphology op(HALCON: gray_range_rect) |
| `cv_open` | morphology op(HALCON: gray_opening) |
| `cv_tophat` | morphology op(HALCON: gray_tophat) |
| `f2_gray_inside` | morphology op(HALCON: gray_inside) |
| `f2_gray_skeleton` | morphology op(HALCON: gray_skeleton) |
| `gclose` | morphology op(HALCON: gray_closing) |
| `gdilate` | morphology op(HALCON: gray_dilation) |
| `gerode` | morphology op(HALCON: gray_erosion) |
| `gopen` | morphology op(HALCON: gray_opening) |
| `gray_bothat` | morphology op(HALCON: gray_bothat) |
| `gray_closing` | morphology op(HALCON: gray_closing) |
| `gray_closing_rect` | morphology op(HALCON: gray_closing_rect) |
| `gray_closing_shape` | morphology op(HALCON: gray_closing_shape) |
| `gray_dilation` | morphology op(HALCON: gray_dilation) |
| `gray_dilation_shape` | morphology op(HALCON: gray_dilation_shape) |
| `gray_erosion` | morphology op(HALCON: gray_erosion) |
| `gray_erosion_shape` | morphology op(HALCON: gray_erosion_shape) |
| `gray_opening` | morphology op(HALCON: gray_opening) |
| `gray_opening_rect` | morphology op(HALCON: gray_opening_rect) |
| `gray_opening_shape` | morphology op(HALCON: gray_opening_shape) |
| `gray_tophat` | morphology op(HALCON: gray_tophat) |
| `morph_grad` | morphology op(HALCON: gray_range_rect) |
| `sk_area_opening` | morphology op(HALCON: -) |
| `tophat` | morphology op(HALCON: gray_tophat) |
| `xsk2_diameter_opening` | morphology op(HALCON: -) |
| `xsk2_reconstruction` | morphology op(HALCON: -) |
| `xsk3_area_closing` | morphology op(HALCON: -) |
| `xsk3_diameter_closing` | morphology op(HALCON: -) |

#### geometry(28 op)

점·선·원 등 기하 프리미티브의 피팅과 계산. 계측 결과를 "도형의 언어"로 옮기는 op 군.


![fops_geometry](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_geometry.png)
*그림: geometry의 실제 처리 예 — 원주 위의 구조(블랙홀 링의 휘도, 톱니바퀴의 이, 나이테)는 직선용 도구로는 잴 수 없지만, polar_trans_image로 극좌표로 펼치면 가로 한 줄이 되어 1D 프로파일이나 직선 검사를 그대로 쓸 수 있다(Fullseye 실제 출력). 입력은 EHT Collaboration의 M87*(CC BY 4.0)+AI 생성 이미지(Gemini) 2종.*

| op | 설명 |
|---|---|
| `affine_trans_image` | geometry op(HALCON: affine_trans_image) |
| `affine_trans_image_size` | geometry op(HALCON: affine_trans_image_size) |
| `affine_trans_region` | geometry op(HALCON: affine_trans_region) |
| `affine_warp` | geometry op(HALCON: affine_trans_image) |
| `it_add_image_border` | geometry op(HALCON: add_image_border) |
| `it_change_format` | geometry op(HALCON: change_format) |
| `it_crop_part` | geometry op(HALCON: crop_part) |
| `it_crop_rectangle1` | geometry op(HALCON: crop_rectangle1) |
| `mirror_image` | geometry op(HALCON: mirror_image) |
| `mirror_region` | geometry op(HALCON: mirror_region) |
| `polar_trans_image` | geometry op(HALCON: polar_trans_image) |
| `polar_trans_image_ext` | geometry op(HALCON: polar_trans_image_ext) |
| `polar_trans_image_inv` | geometry op(HALCON: polar_trans_image_inv) |
| `polar_trans_region_inv` | geometry op(HALCON: polar_trans_region_inv) |
| `projective_trans_image` | geometry op(HALCON: projective_trans_image) |
| `projective_trans_image_size` | geometry op(HALCON: projective_trans_image_size) |
| `projective_trans_region` | geometry op(HALCON: projective_trans_region) |
| `rescale_img` | geometry op(HALCON: zoom_image_size) |
| `rotate_image` | geometry op(HALCON: rotate_image) |
| `rotate_img` | geometry op(HALCON: rotate_image) |
| `sk_swirl` | geometry op(HALCON: polar_trans_image) |
| `tf_log_polar` | geometry op(HALCON: -) |
| `transpose_region` | geometry op(HALCON: transpose_region) |
| `xcv2_warp_logpolar` | geometry op(HALCON: -) |
| `xpil_offset` | geometry op(HALCON: -) |
| `zoom_image_factor` | geometry op(HALCON: zoom_image_factor) |
| `zoom_image_size` | geometry op(HALCON: zoom_image_size) |
| `zoom_region` | geometry op(HALCON: zoom_region) |

#### 3dgs(26 op)

3D Gaussian Splatting 관련. 다시점 이미지로부터의 3D 복원·렌더링·메시화라는, 이 도구 상자의 최전선이다.

| op | 설명 |
|---|---|
| `animate_mesh` | qpos 궤적으로 참값 메시를 애니메이션 재생(정적 지형 메시의 합성도 가능) |
| `bin_pick_gif` | 어지럽게 쌓인 부품을 후보 스코어링으로 골라 6DoF IK로 윗면 파지해 bin에서 꺼내는 bin-picking을 headless로 GIF화(GPU 불필요·성공 수는 부품이 bin을 벗어났는지로 실측) |
| `capture_orbit` | sim 장면을 오빗 촬영해 3DGS 데이터셋(transforms.json)화 |
| `event_camera` | 이벤트 카메라(DVS)를 로그 휘도 변화 모델로 모사해 ON/OFF 이벤트 열을 생성. 움직이는 에지에 발화함을 실측(GPU 불필요) |
| `evis_perceive` | GPU 학습 evis의 롤아웃(qpos npy)을 Fullseye로 지각: RGB/깊이/DVS의 3면 GIF(ego_body=로 로봇 시점=머리 탑재 RGB/깊이/DVS의 4면) |
| `figure8` | 차동 선회로 8자 계열 곡선을 각 크기로 그리는 선회 제어 연습/캘리브레이션(부감 트랙, GPU 불필요) |
| `focus_stack` | 참값 깊이로부터 피사계 심도 보케의 초점 스택을 생성하고 국소 선명도 최대로 전초점 합성(초점 유래 깊이도 복원, GPU 불필요) |
| `g1_perceive_real` | G1 실기 센서 사양으로 지각: Livox Mid-360(정수리 360°/-7..+52°) BEV 점군 + RealSense D435i(87°×58°, 0.3-6m 대역) RGB/깊이의 4면 GIF. obstacles=True 로 보행 경로 밖에 검증용 정적 장애물을 배치(센서에 잡히는 대상을 마련) |
| `g1_training_curves` | G1 학습 로그의 진행 행(step/reward/ep_len/perr/crash…)을 배열 사전으로 파싱 — GPU 머신을 건드리지 않고 학습 곡선을 Studio에서 플롯 |
| `g1_walk_policy` | GPU 학습 완료 G1 보행 정책(brax ckpt)을 Windows만으로 실행: numpy 추론(brax 수치 일치 검증 완료)+네이티브 MuJoCo 롤아웃→거리/생존/횡편차 RMS 실측+추적 카메라 동영상. vision=True 로 의사 LiDAR+장애물 포함 시각 보행판 |
| `hurdle_physics` | go2가 도움닫기→폭발 도약으로 장애물(배리어)을 넘어 반대편에 착지하는 진짜 물리의 멀리뛰기를 GIF＋궤적 텔레메트리화(넘었는지/자립했는지를 실측, GPU 불필요) |
| `jump_physics` | go2를 웅크리기→폭발 신전→탄도 비행(모든 발 이지=접촉 0을 실측)→착지시키는 진짜 물리 점프를 GIF＋높이 텔레메트리화(도약 높이/체공을 실측, 마찰·중력 포함, GPU 불필요) |
| `lidar_scan` | 스피닝 LIDAR를 mj_ray의 실제 레이캐스트로 시뮬레이트해 점군을 생성·시각화(GPU 불필요·명중률 등 실측) |
| `long_route` | go2가 거칠기가 변하는 긴 기복 지형을 진짜 물리로 장거리(기본 100m) 완주한다(거리/자립을 실측, GPU 불필요) |
| `pick_gif` | 로봇 팔(Panda)이 실제 접촉·마찰로 큐브를 파지해 다른 위치에 놓는 pick-and-place를 headless로 GIF화(GPU 불필요·파지 성패는 상자의 실측 높이로 판정) |
| `polarization` | 편광 카메라를 Fresnel 순방향 모델(법선→DoLP/AoLP→4편광 이미지→Stokes)로 모사. 무텍스처 면에서도 표면 방위를 편광이 부호화(투과/경면 파지용, GPU 불필요) |
| `pseudo_lidar` | 평면 의사 LiDAR 스캔(전방 호 K개의 정규화 거리). 보행 정책 G1VisionWalk의 관측과 동일 지오메트리의 numpy parity — 정책이 먹는 입력을 도구로 단독 계산 |
| `render_walk_gif` | walker를 terrain 위에 배치한 운동학 프리뷰를 headless로 GIF화(접촉 없음·motion/gait을 시각화. 물리 보행은 walk_physics를 사용) |
| `route_planning` | go2가 장애물을 레이캐스트로 미리 읽고 후보 방위를 피라미드 탐색(거침→세밀)으로 골라 차동 선회로 회피해 골에 도달하는 진짜 물리 내비게이션(부감 플랜 포함, GPU 불필요) |
| `sensor_fusion` | 위치 센서(카메라/GPS)와 속도 센서(IMU)를 Kalman 필터로 융합해 투사체를 추적. 융합 RMSE를 각 센서 단독과 정직하게 비교한 그림을 생성(GPU 불필요) |
| `stereo_depth` | 평행 2카메라의 스테레오 페어를 렌더링해 블록 매칭으로 깊이 추정, 참값 깊이와 오차 비교(기존 stereo.py 사용, GPU 불필요) |
| `sugar_mesh` | 3DGS를 SuGaR풍으로 표면 정렬→Poisson으로 메시 추출(참값 bbox 검증 포함) |
| `train_3dgs` | sim 장면을 native gsplat으로 3DGS 학습(고속) |
| `train_3dgs_densify` | densify + SH + antialiased 포함 3DGS 학습(고품질) |
| `tsdf_mesh` | sim 완전 깊이를 TSDF 융합해 깨끗한 watertight 메시화(GPU 불필요·바늘 없음) |
| `walk_physics` | go2를 토크 PD 제어＋폐루프 밸런스＋mj_step의 진짜 물리(중력·마찰·접촉·관성)로 거친 height field 위를 걷게 하고, 몸통이 기우는 모습을 GIF＋텔레메트리화(자립/전진/기울기를 실측, GPU 불필요) |

#### Regions(26 op)

영역 처리의 HALCON 호환 상위 세트(region 카테고리의 확장판).


![fops_regions](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_regions.png)
*그림: Regions의 실제 처리 예 — 현장의 이진 이미지는 낟알 노이즈와 구멍투성이라, 그대로 라벨링하면 잘못 계수한다. opening_circle(오프닝)로 낟알을 지우고 fill_up으로 구멍을 메운 뒤 연결 성분으로 나누는 것이 영역 처리의 정석(Fullseye 실제 출력). 입력은 AI 생성(Gemini) 2종+동봉 샘플 1종의 이진화+인공 오염.*

| op | 설명 |
|---|---|
| `difference` | 영역 차 region \ sub(difference). |
| `find_neighbors` | 영역 리스트의 인접 쌍 index를 반환(팽창해 교차 판정)(find_neighbors). |
| `gen_random_region` | 랜덤한 연결 영역을 생성(경계 집적=정확한 면적 + 연결성 보장)(gen_random_region). |
| `gen_random_regions` | 복수의 랜덤 영역을 생성(gen_random_regions). |
| `gen_rectangle1` | 축 평행 직사각형 영역을 생성(gen_rectangle1). |
| `gen_region_histo` | 1D 히스토그램을 막대그래프 영역으로 그린다(gen_region_histo). |
| `gen_region_hline` | 수평 선분의 영역을 생성(gen_region_hline). rows: 행 index의 열. |
| `gen_region_line` | 선분을 region화(gen_region_line, DDA). |
| `gen_region_points` | 개별 픽셀을 region화(gen_region_points). |
| `gen_region_polygon` | 다각형의 윤곽을 region화(gen_region_polygon). |
| `gen_region_polygon_filled` | 다각형을 채워서 region화(gen_region_polygon_filled). |
| `gen_region_runs` | 런렝스 부호 [(row, col_start, col_end), ...] 로부터 region을 생성(gen_region_runs). |
| `get_region_points` | 영역 픽셀의 (row, col) 좌표 배열(get_region_points). |
| `get_region_polygon` | 영역 외형의 다각형 근사 꼭짓점을 반환(get_region_polygon). |
| `get_region_runs` | 영역의 런렝스 표현 [(row, col_start, col_end), ...](get_region_runs). |
| `hamming_distance` | 2개 영역의 Hamming 거리(다른 픽셀 수)(hamming_distance). |
| `hamming_distance_norm` | 정규화 Hamming 거리(차분 픽셀 / 합집합 픽셀)(hamming_distance_norm). |
| `intersection` | 영역 곱(intersection). |
| `merge_regions_line_scan` | 라인 스캔의 런 집합을 연결해 영역으로 통합(merge_regions_line_scan). |
| `select_region_spatial` | 기준 영역에 대해 지정 공간 관계를 만족하는 영역을 고른다(select_region_spatial). |
| `select_shape_proto` | 프로토타입 영역에 형상 특징이 가까운 영역을 고른다(select_shape_proto). |
| `spatial_relation` | 2개 영역의 무게중심 방향에 기반한 공간 관계(above/below/left/right)(spatial_relation). |
| `symm_difference` | 대칭차(symm_difference). |
| `test_equal_region` | 2개 영역이 같은지(test_equal_region). |
| `test_subset_region` | region1 ⊆ region2 인지(test_subset_region). |
| `union2` | 영역 합(union2). |

#### contour(26 op)

윤곽(contour)의 추출·평활화·분할·속성 계산.


![fops_contour](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_contour.png)
*그림: contour의 실제 처리 예 — 가는 선 모양 구조(혈관·시맥·잎맥·균열)는 에지 검출로는 선 양쪽의 가장자리가 이중으로 나오지만, lines_gauss(Frangi 능선 응답)로 선 구조의 띠를 얻고 skeleton으로 1픽셀 폭의 중심선으로 세선화한다. 혈관도 시맥도 잎맥도 균열도 같은 수학으로 잴 수 있다(Fullseye 실제 출력). 입력은 모두 AI 생성 이미지(Gemini). 의료풍 입력은 진단 용도가 아니다.*

| op | 설명 |
|---|---|
| `FindContours` | 이진/레벨로부터의 윤곽 추출(cv2.findContours, 부재 시 skimage, 없으면 numpy)  [backend=opencv] |
| `affine_trans_contour_xld` | contour op(HALCON: affine_trans_contour_xld) |
| `affine_trans_polygon_xld` | contour op(HALCON: affine_trans_polygon_xld) |
| `close_contours_xld` | contour op(HALCON: close_contours_xld) |
| `contour_point_num_xld` | contour op(HALCON: contour_point_num_xld) |
| `contours_to_region` | contour op(HALCON: gen_region_contour_xld) |
| `edges_color_sub_pix` | contour op(HALCON: edges_color_sub_pix) |
| `edges_sub_pix` | contour op(HALCON: edges_sub_pix) |
| `fit_line_contours` | contour op(HALCON: fit_line_contour_xld) |
| `gen_contour_region_xld` | contour op(HALCON: gen_contour_region_xld) |
| `gen_region_contour_xld` | contour op(HALCON: gen_region_contour_xld) |
| `gen_region_polygon_xld` | contour op(HALCON: gen_region_polygon_xld) |
| `lines_color` | contour op(HALCON: lines_color) |
| `lines_facet` | contour op(HALCON: lines_facet) |
| `lines_gauss` | contour op(HALCON: lines_gauss) |
| `polar_trans_contour_xld` | contour op(HALCON: polar_trans_contour_xld) |
| `projective_trans_contour_xld` | contour op(HALCON: projective_trans_contour_xld) |
| `select_contours` | contour op(HALCON: select_contours_xld) |
| `select_contours_xld` | contour op(HALCON: select_contours_xld) |
| `select_shape_xld` | contour op(HALCON: select_shape_xld) |
| `shape_trans_xld` | contour op(HALCON: shape_trans_xld) |
| `sk_find_contours` | contour op(HALCON: -) |
| `smooth_contours` | contour op(HALCON: smooth_contours_xld) |
| `smooth_contours_xld` | contour op(HALCON: smooth_contours_xld) |
| `threshold_sub_pix` | contour op(HALCON: threshold_sub_pix) |
| `zero_crossing_sub_pix` | contour op(HALCON: zero_crossing_sub_pix) |

#### rank(23 op)

랭크 필터(메디안 등). 순서 통계에 기반한 노이즈 제거로, 소금후추 노이즈의 특효약.

![rank 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_02_median_image.png)
*그림: 메디안 필터 예(11.1.1절에서 재수록)*

| op | 설명 |
|---|---|
| `cv_median` | rank op(HALCON: median_image) |
| `dual_rank` | rank op(HALCON: dual_rank) |
| `eliminate_min_max` | rank op(HALCON: eliminate_min_max) |
| `eliminate_sp` | rank op(HALCON: eliminate_sp) |
| `gray_dilation_rect` | rank op(HALCON: gray_dilation_rect) |
| `gray_erosion_rect` | rank op(HALCON: gray_erosion_rect) |
| `gray_range_rect` | rank op(HALCON: gray_range_rect) |
| `max_filter` | rank op(HALCON: gray_dilation_rect) |
| `mean_sp` | rank op(HALCON: mean_sp) |
| `median` | rank op(HALCON: median_image) |
| `median_image` | rank op(HALCON: median_image) |
| `median_rect` | rank op(HALCON: median_rect) |
| `median_separate` | rank op(HALCON: median_separate) |
| `median_weighted` | rank op(HALCON: median_weighted) |
| `min_filter` | rank op(HALCON: gray_erosion_rect) |
| `percentile` | rank op(HALCON: rank_image) |
| `rank_image` | rank op(HALCON: rank_image) |
| `rank_rect` | rank op(HALCON: rank_rect) |
| `sk_median_disk` | rank op(HALCON: median_image) |
| `trimmed_mean` | rank op(HALCON: trimmed_mean) |
| `xkor_median` | rank op(HALCON: -) |
| `xpil_mode_filter` | rank op(HALCON: -) |
| `xsk2_rank_geomean` | rank op(HALCON: -) |
