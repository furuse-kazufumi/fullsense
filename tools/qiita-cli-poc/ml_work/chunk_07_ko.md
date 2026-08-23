#### Transformations(79 op)

이미지의 기하 변환(회전·스케일·사영·극좌표 등). 검사에서는 「워크의 방향을 맞춘 뒤에 잰다」의 전 단계로 매번 등장한다.


![fops_transformations](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_transformations.png)
*그림: Transformations의 실처리 예 — 비스듬한 시점의 평면은 아핀 변환(6 자유도)으로는 사다리꼴 왜곡이 잡히지 않고, 4점 대응에서 DLT로 추정한 사영 변환(vector_to_proj_hom_mat2d → gen_image_warp_map)으로 비로소 바로 위 시점으로 정류할 수 있다(Fullseye 실출력). 1단은 기지 호모그래피의 합성(참값 있음), 2-3단은 AI 생성 이미지(Gemini).*

| op | 설명 |
|---|---|
| `affine_trans_pixel` | 화소 (row,col)에 아핀 변환을 적용(HALCON은 (row,col) 순). |
| `affine_trans_point_2d` | 점렬에 임의의 2D 아핀 변환을 적용한다. |
| `axis_angle_to_quat` | 회전축과 각도로 회전 쿼터니언을 만든다. |
| `convert_point_3d_cart_to_spher` | 3D 점의 직교 좌표를 구면 좌표로 변환한다. |
| `convert_point_3d_spher_to_cart` | 3D 점의 구면 좌표를 직교 좌표로 변환한다. |
| `convert_pose_type` | pose의 나열을 반환(genuine한 형 변환의 간이판=항등으로 type 태그를 붙임). |
| `dual_quat_compose` | 이중 사원수의 합성(강체 변환의 합성, dual_quat_compose). |
| `dual_quat_conjugate` | 쌍대 쿼터니언의 켤레를 반환. |
| `dual_quat_interpolate` | 이중 사원수의 보간(pose 경유로 병진 lerp + 회전 slerp, dual_quat_interpolate). |
| `dual_quat_normalize` | 쌍대 쿼터니언을 정규화한다. |
| `dual_quat_to_hom_mat3d` | 단위 이중 사원수 [qr(4), qd(4)]를 4x4 강체 변환으로(dual_quat_to_hom_mat3d). |
| `dual_quat_to_pose` | 쌍대 쿼터니언을 3D pose 표현으로 변환한다. |
| `dual_quat_to_screw` | 이중 사원수에서 스크류 성분(각도·병진·축)을 반환(dual_quat_to_screw). |
| `dual_quat_trans_line_3d` | 쌍대 사원수로 3D 직선을 변환(점과 방향을 강체 변환)(dual_quat_trans_line_3d). |
| `dual_quat_trans_point_3d` | 단위 쌍대 쿼터니언으로 3D 점을 강체 변환한다. |
| `gen_image_warp_map` | 2D 호모그래피에서 화소 워프 맵(역사상)을 생성(gen_image_warp_map). |
| `get_pose_type` | 3D pose의 표현 형식(회전을 담는 방식)을 반환. |
| `get_rectangle_pose` | 이미지 위의 사각형에서 평면 자세를 추정(4모서리 대응 → homography → pose)(get_rectangle_pose). |
| `hom_mat2d_compose` | 두 2D 동차 변환 행렬을 합성(곱)한다. |
| `hom_mat2d_determinant` | 2D 동차 변환 행렬의 행렬식을 계산한다. |
| `hom_mat2d_identity` | 항등 2D 변환의 동차 행렬을 만든다. |
| `hom_mat2d_invert` | 2D 동차 변환 행렬의 역행렬을 구한다. |
| `hom_mat2d_reflect` | 2D 동차 변환 행렬에 반사를 추가한다. |
| `hom_mat2d_reflect_local` | 2D 동차 변환 행렬에 로컬 좌표계에서의 반사를 추가한다. |
| `hom_mat2d_rotate` | 2D 동차 변환 행렬에 회전을 추가한다. |
| `hom_mat2d_rotate_local` | 2D 동차 변환 행렬에 로컬 좌표계에서의 회전을 추가한다. |
| `hom_mat2d_scale` | 2D 동차 변환 행렬에 확대 축소를 추가한다. |
| `hom_mat2d_scale_local` | 2D 동차 변환 행렬에 로컬 좌표계에서의 확대 축소를 추가한다. |
| `hom_mat2d_slant` | 2D 동차 변환 행렬에 전단(슬랜트)을 추가한다. |
| `hom_mat2d_slant_local` | 2D 동차 변환 행렬에 로컬 좌표계에서의 전단을 추가한다. |
| `hom_mat2d_to_affine_par` | 2D 아핀 행렬을 (sx, sy, phi, theta, tx, ty)로 분해. |
| `hom_mat2d_translate` | 2D 동차 변환 행렬에 평행 이동을 추가한다. |
| `hom_mat2d_translate_local` | 2D 동차 변환 행렬에 로컬 좌표계에서의 평행 이동을 추가한다. |
| `hom_mat2d_transpose` | 2D 동차 변환 행렬을 전치한다. |
| `hom_mat3d_compose` | 두 3D 동차 변환 행렬을 합성(곱)한다. |
| `hom_mat3d_determinant` | 3D 동차 변환 행렬의 행렬식을 계산한다. |
| `hom_mat3d_identity` | 항등 3D 변환의 동차 행렬을 만든다. |
| `hom_mat3d_invert` | 3D 동차 변환 행렬의 역행렬을 구한다. |
| `hom_mat3d_project` | 4x4 투시 투영 행렬로 3D 점을 2D 이미지 점으로(hom_mat3d_project). |
| `hom_mat3d_rotate` | 축 둘레의 오른손 좌표계 회전을 왼쪽 곱(axis 0=x,1=y,2=z, 표준 부호 규약). |
| `hom_mat3d_rotate_local` | 3D 동차 변환 행렬에 로컬 좌표계에서의 회전을 추가한다. |
| `hom_mat3d_scale` | 3D 동차 변환 행렬에 확대 축소를 추가한다. |
| `hom_mat3d_scale_local` | 3D 동차 변환 행렬에 로컬 좌표계에서의 확대 축소를 추가한다. |
| `hom_mat3d_to_pose` | 4x4 변환 행렬을 pose [rx,ry,rz(ZYX euler), tx,ty,tz]로 분해. |
| `hom_mat3d_translate` | 3D 동차 변환 행렬에 평행 이동을 추가한다. |
| `hom_mat3d_translate_local` | 3D 동차 변환 행렬에 로컬 좌표계에서의 평행 이동을 추가한다. |
| `hom_mat3d_transpose` | 3D 동차 변환 행렬을 전치한다. |
| `hom_vector_to_proj_hom_mat2d` | 4점 이상의 대응에서 사영 변환(homography, DLT) 3x3을 구한다(hom_vector_to_proj_hom_mat2d). |
| `point_line_to_hom_mat2d` | 점+방향의 대응에서 2D 강체 변환을 추정(point_line_to_hom_mat2d). |
| `point_pluecker_line_to_hom_mat3d` | 점+Plücker 직선의 대응에서 3D 강체 변환을 추정(point_pluecker_line_to_hom_mat3d). |
| `pose_average` | 여러 pose의 평균 pose를 구한다. |
| `pose_compose` | 두 3D pose를 합성한다. |
| `pose_invert` | 3D pose 열의 각 요소를 역변환으로 만든다. |
| `pose_to_dual_quat` | 3D pose를 단위 쌍대 쿼터니언으로 변환한다. |
| `pose_to_hom_mat3d` | pose [rx,ry,rz(rad), tx,ty,tz]를 4x4 변환 행렬로(hom_mat3d_to_pose의 역). |
| `pose_to_quat` | 3D pose의 회전 성분을 쿼터니언으로 변환한다. |
| `proj_hom_mat2d_to_pose` | 호모그래피와 내부 행렬에서 평면의 자세(R,t)를 분해(proj_hom_mat2d_to_pose). |
| `projective_trans_hom_point_3d` | 동차 3D 점에 4x4 사영 변환을 적용(projective_trans_hom_point_3d). |
| `projective_trans_pixel` | 화소 (row,col)에 사영 변환을 적용(HALCON (row,col) 순). |
| `projective_trans_point_3d` | 사영 변환 행렬로 3D 점을 사영한다. |
| `quat_compose` | 두 쿼터니언의 곱을 계산한다. |
| `quat_conjugate` | 쿼터니언의 켤레를 반환. |
| `quat_interpolate` | slerp 구면 선형 보간. |
| `quat_normalize` | 쿼터니언을 정규화한다. |
| `quat_rotate_point_3d` | 단위 쿼터니언으로 3D 점을 회전한다. |
| `quat_to_hom_mat3d` | 쿼터니언을 대응하는 회전 행렬로 변환한다. |
| `quat_to_pose` | 쿼터니언을 대응하는 3D pose로 변환한다. |
| `screw_to_dual_quat` | 스크류(축 방향 l, 모멘트 m, 회전각 theta, 병진 d)를 이중 사원수로(screw_to_dual_quat). |
| `set_origin_pose` | 자세의 원점을 국소 오프셋만큼 이동(set_origin_pose). |
| `vector_angle_to_rigid` | 한 쌍의 (점, 각도)에서 2D 강체 변환을 구한다(vector_angle_to_rigid). |
| `vector_field_to_hom_mat2d` | 벡터장 전체에 가장 잘 맞는 아핀 변환(2x3)을 최소제곱 추정(vector_field_to_hom_mat2d). |
| `vector_to_aniso` | 2D 점 대응에서 이방성(비등방 스케일) 아핀 변환을 추정(vector_to_aniso). |
| `vector_to_hom_mat2d` | 점 대응에서 2D 호모그래피를 추정(vector_to_hom_mat2d). |
| `vector_to_hom_mat3d` | 3D 점 대응에서 강체/상사 변환(4x4)을 Umeyama 추정(vector_to_hom_mat3d). |
| `vector_to_pose` | 6쌍 이상의 3D↔2D 대응에서 물체/카메라의 6 자유도 pose (R, t)를 추정한다(PnP). |
| `vector_to_proj_hom_mat2d` | 2D 점 대응에서 사영 변환(호모그래피 3x3)을 DLT 추정(vector_to_proj_hom_mat2d). |
| `vector_to_proj_hom_mat2d_distortion` | 왜곡 포함으로 사영 변환을 추정(왜곡은 작다고 가정하고 DLT)(vector_to_proj_hom_mat2d_distortion). |
| `vector_to_rigid` | 대응점에서 2D 강체 변환(회전+병진, Kabsch)을 구한다(vector_to_rigid). |
| `vector_to_similarity` | 대응점에서 2D 상사 변환(회전+스케일+병진, Umeyama)을 구한다(vector_to_similarity). |

#### features(77 op)

영역이나 윤곽에서 수치 특징(면적·둘레 길이·원형도·모멘트 등)을 추출하는 op 군. 「이미지를 숫자로 만드는」 계측의 본진이다.

![features의 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_13_area_center.png)
*그림: 면적·무게중심 계측의 예(11.1.1절에서 재게재)*

| op | 설명 |
|---|---|
| `ORB` | ORB 키포인트(cv2.ORB, 부재 시 Harris 코너 numpy)(features.ORB).  [backend=opencv] |
| `area_center` | features op(HALCON: area_center) |
| `area_center_xld` | features op(HALCON: area_center_xld) |
| `area_frac` | features op(HALCON: area_center) |
| `area_holes` | features op(HALCON: area_holes) |
| `blob_count` | features op(HALCON: count_obj) |
| `circularity` | features op(HALCON: circularity) |
| `circularity_xld` | features op(HALCON: circularity_xld) |
| `compactness` | features op(HALCON: compactness) |
| `compactness_xld` | features op(HALCON: compactness_xld) |
| `connect_and_holes` | features op(HALCON: connect_and_holes) |
| `contlength` | features op(HALCON: contlength) |
| `convexity` | features op(HALCON: convexity) |
| `convexity_xld` | features op(HALCON: convexity_xld) |
| `count_channels` | features op(HALCON: count_channels) |
| `count_contours` | features op(HALCON: count_obj) |
| `count_obj` | features op(HALCON: count_obj) |
| `cv_cc_count` | features op(HALCON: connection) |
| `cv_good_features` | features op(HALCON: -) |
| `cv_hough_circles` | features op(HALCON: hough_circles) |
| `cv_hough_lines` | features op(HALCON: hough_lines) |
| `describe_patches` | 각 키포인트 주변의 휘도 패치를 평균 0·노름 1로 정규화한 기술자. |
| `diameter_region` | features op(HALCON: diameter_region) |
| `diameter_xld` | features op(HALCON: diameter_xld) |
| `eccentricity` | features op(HALCON: eccentricity) |
| `eccentricity_xld` | features op(HALCON: eccentricity_xld) |
| `elliptic_axis` | features op(HALCON: elliptic_axis) |
| `elliptic_axis_xld` | features op(HALCON: elliptic_axis_xld) |
| `entropy_gray` | features op(HALCON: entropy_gray) |
| `estimate_noise` | features op(HALCON: estimate_noise) |
| `euler_number` | features op(HALCON: euler_number) |
| `fast_corners` | FAST형 코너 키포인트 검출(응답이 강한 순). |
| `get_region_thickness` | features op(HALCON: get_region_thickness) |
| `gray_histo_abs` | features op(HALCON: gray_histo_abs) |
| `harris_corners` | Harris 코너 키포인트 검출(응답이 강한 순). |
| `height_width_ratio` | features op(HALCON: height_width_ratio) |
| `hough_circle_trans` | features op(HALCON: hough_circle_trans) |
| `hough_line_trans` | features op(HALCON: hough_line_trans) |
| `intensity` | features op(HALCON: intensity) |
| `length_xld` | features op(HALCON: length_xld) |
| `match_descriptors` | 두 기술자 집합을 최근접 + Lowe의 비율 테스트로 대응시킨다. |
| `match_keypoints` | 2 이미지 간의 키포인트 검출·기술·매칭을 일괄 실행한다. |
| `min_max_gray` | features op(HALCON: min_max_gray) |
| `moments_region_2nd` | features op(HALCON: moments_region_2nd) |
| `moments_region_2nd_invar` | features op(HALCON: moments_region_2nd_invar) |
| `moments_region_2nd_rel_invar` | features op(HALCON: moments_region_2nd_rel_invar) |
| `moments_region_3rd` | features op(HALCON: moments_region_3rd) |
| `moments_region_3rd_invar` | features op(HALCON: moments_region_3rd_invar) |
| `moments_region_central` | features op(HALCON: moments_region_central) |
| `moments_region_central_invar` | features op(HALCON: moments_region_central_invar) |
| `moments_xld` | features op(HALCON: moments_xld) |
| `orientation_region` | features op(HALCON: orientation_region) |
| `orientation_xld` | features op(HALCON: orientation_xld) |
| `rectangularity` | features op(HALCON: rectangularity) |
| `rectangularity_xld` | features op(HALCON: rectangularity_xld) |
| `roundness` | features op(HALCON: roundness) |
| `sk_blur_effect` | features op(HALCON: -) |
| `sk_entropy_feat` | features op(HALCON: entropy_gray) |
| `sk_euler` | features op(HALCON: euler_number) |
| `total_length` | features op(HALCON: length_xld) |
| `vol_count` | features op(HALCON: -) |
| `xcv2_fast_count` | features op(HALCON: -) |
| `xcv2_lap_var` | features op(HALCON: -) |
| `xcv3_agast_count` | features op(HALCON: -) |
| `xcv3_brisk_count` | features op(HALCON: -) |
| `xcv3_gray_hu1` | features op(HALCON: -) |
| `xcv3_lsd_count` | features op(HALCON: -) |
| `xcv3_sift_count` | features op(HALCON: -) |
| `xcv_orb_count` | features op(HALCON: -) |
| `xsk3_estimate_sigma` | features op(HALCON: -) |
| `xsk3_is_low_contrast` | features op(HALCON: -) |
| `xsk_blob_dog` | features op(HALCON: -) |
| `xsk_blob_doh` | features op(HALCON: -) |
| `xsk_blob_log` | features op(HALCON: -) |
| `xsk_orb_count` | features op(HALCON: -) |
| `xwt_detail_energy` | features op(HALCON: -) |
| `xwt_packet_entropy` | features op(HALCON: -) |

#### region(76 op)

이진 영역(region)의 생성·합성·선별. 임계값 처리 → 연결 성분 → 조건 선별이 정석의 3연계다.

![region의 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_05_threshold_label.png)
*그림: 이진화 → 연결 성분 라벨링의 예(11.1.1절에서 재게재)*

| op | 설명 |
|---|---|
| `boundary` | region op(HALCON: boundary) |
| `closest_point_transform` | region op(HALCON: closest_point_transform) |
| `closing_circle` | region op(HALCON: closing_circle) |
| `closing_golay` | region op(HALCON: closing_golay) |
| `closing_rectangle1` | region op(HALCON: closing_rectangle1) |
| `convex_fill` | region op(HALCON: shape_trans) |
| `cv_dist` | region op(HALCON: distance_transform) |
| `dilation_circle` | region op(HALCON: dilation_circle) |
| `dilation_golay` | region op(HALCON: dilation_golay) |
| `dilation_rectangle1` | region op(HALCON: dilation_rectangle1) |
| `dilation_seq` | region op(HALCON: dilation_seq) |
| `dist_transform` | region op(HALCON: distance_transform) |
| `distance_transform` | region op(HALCON: distance_transform) |
| `erosion_circle` | region op(HALCON: erosion_circle) |
| `erosion_golay` | region op(HALCON: erosion_golay) |
| `erosion_rectangle1` | region op(HALCON: erosion_rectangle1) |
| `erosion_seq` | region op(HALCON: erosion_seq) |
| `fill_holes` | region op(HALCON: fill_up) |
| `fill_up` | region op(HALCON: fill_up) |
| `fill_up_shape` | region op(HALCON: fill_up_shape) |
| `get_region_contour` | region op(HALCON: get_region_contour) |
| `get_region_convex` | region op(HALCON: get_region_convex) |
| `invert_region` | region op(HALCON: complement) |
| `junctions_skeleton` | region op(HALCON: junctions_skeleton) |
| `morph_skeleton` | region op(HALCON: morph_skeleton) |
| `opening_circle` | region op(HALCON: opening_circle) |
| `opening_golay` | region op(HALCON: opening_golay) |
| `opening_rectangle1` | region op(HALCON: opening_rectangle1) |
| `pruning` | region op(HALCON: pruning) |
| `r2_inner_circle` | 최대 내접원을 마스크로 그린다(a로 그리기 반경을 확대 축소, a=0.5로 엄밀). |
| `r2_inner_rectangle1` | 최대의 축평행 내접 사각형(a로 그리기 사각형을 축소, a=0으로 엄밀). |
| `r2_partition_rectangle` | 영역의 외접 사각형을 N×N 격자로 분할하고 영역과 겹치는 셀만 남긴다. |
| `r2_runlength_features` | 영역→특징량: 수평 방향 전경 런 길이의 평균. |
| `r2_smallest_circle` | 최소 포함원을 마스크로 그린다(Welzl 법, a로 반경을 확대). |
| `r2_smallest_rectangle1` | 축평행의 외접 사각형(바운딩 박스). |
| `r2_smallest_rectangle2` | 면적 최소의 유향 외접 사각형을 마스크화(회전 캘리퍼 법). |
| `r2_sort_region` | k번째로 큰 연결 성분만 남긴다(k = round(a*(n-1))). |
| `r2_split_skeleton_lines` | 영역을 세선화해 골격으로 만들고 분기점(근방 3 이상)에서 잘라 나눈다. |
| `r2_union1` | 전체 연결 성분을 1개의 마스크로 통합(라벨의 OR). |
| `r3_background_seg` | region op(HALCON: background_seg) |
| `r3_clip_region` | region op(HALCON: clip_region) |
| `r3_eliminate_runs` | region op(HALCON: eliminate_runs) |
| `r3_label_to_region` | region op(HALCON: label_to_region) |
| `r3_partition_dynamic` | region op(HALCON: partition_dynamic) |
| `r3_polar_trans_region` | region op(HALCON: polar_trans_region) |
| `r3_rank_region` | region op(HALCON: rank_region) |
| `r3_region_features` | region op(HALCON: region_features) |
| `r3_runlength_distribution` | region op(HALCON: runlength_distribution) |
| `r3_select_region_point` | region op(HALCON: select_region_point) |
| `reg_close` | region op(HALCON: closing_circle) |
| `reg_dilate` | region op(HALCON: dilation_circle) |
| `reg_erode` | region op(HALCON: erosion_circle) |
| `reg_open` | region op(HALCON: opening_circle) |
| `region_boundary` | region op(HALCON: boundary) |
| `remove_noise_region` | region op(HALCON: remove_noise_region) |
| `remove_small` | region op(HALCON: select_shape) |
| `select_largest` | region op(HALCON: select_shape_std) |
| `select_shape` | region op(HALCON: select_shape) |
| `select_shape_std` | region op(HALCON: select_shape_std) |
| `shape_trans` | region op(HALCON: shape_trans) |
| `sk_clear_border` | region op(HALCON: -) |
| `sk_convex` | region op(HALCON: shape_trans) |
| `sk_find_boundaries` | region op(HALCON: boundary) |
| `sk_medial` | region op(HALCON: skeleton) |
| `sk_remove_holes` | region op(HALCON: fill_up) |
| `sk_skeleton` | region op(HALCON: skeleton) |
| `sk_thin` | region op(HALCON: thinning) |
| `skeleton` | region op(HALCON: skeleton) |
| `smallest_rectangle1` | region op(HALCON: smallest_rectangle1) |
| `thinning` | region op(HALCON: thinning) |
| `thinning_golay` | region op(HALCON: thinning_golay) |
| `thinning_seq` | region op(HALCON: thinning_seq) |
| `xcv2_hitmiss` | region op(HALCON: -) |
| `xsk2_isotropic_close` | region op(HALCON: -) |
| `xsk3_rank_majority` | region op(HALCON: -) |
| `xsp_chamfer_dist` | region op(HALCON: -) |

#### Image(59 op)

이미지의 생성·입출력·채널 조작·산술 합성 등, 이미지 자체를 다루는 기초 op 군.


![fops_image_chapter](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_image_chapter.png)
*그림: Image의 실처리 예 — decompose3로 컬러 이미지를 R/G/B 채널로 분해. 채널마다 담기는 정보가 다르다(안저에서는 혈관과 배경의 콘트라스트 배분이 채널에 따라 크게 변한다)(Fullseye 실출력). 입력은 scikit-image 동봉 retina+AI 생성 이미지(Gemini) 2종. 진단 용도가 아니라 화상 처리 데모.*

| op | 설명 |
|---|---|
| `add_channels` | gray 이미지를 base 이미지에 채널로 추가(add_channels). |
| `append_channel` | 다채널 이미지에 1 채널을 덧붙임(append_channel). |
| `area_center_gray` | 그레이 값을 가중치로 한 면적(질량)과 무게중심 (row,col)(area_center_gray). |
| `change_domain` | 이미지의 domain(ROI)을 region으로 변경(영역 밖을 0 마스크)(change_domain). |
| `channels_to_image` | 2D 채널의 리스트/열을 다채널 이미지로(channels_to_image). |
| `complex_to_real` | 복소 이미지를 실부/허부로 분해(complex_to_real). |
| `compose2` | 2장의 이미지를 2채널 이미지로 묶는다. |
| `compose3` | 3장의 이미지를 3채널 이미지로 묶는다. |
| `compose4` | 4장의 이미지를 4채널 이미지로 묶는다. |
| `compose5` | 5장의 이미지를 5채널 이미지로 묶는다. |
| `compose6` | 6장의 이미지를 6채널 이미지로 묶는다. |
| `compose7` | 7장의 이미지를 7채널 이미지로 묶는다. |
| `cooc_feature_matrix` | GLCM에서 Haralick 특징(energy/contrast/correlation/homogeneity)(cooc_feature_matrix). |
| `crop_domain_rel` | domain 외접 사각형을 상대 마진 포함으로 잘라낸다(crop_domain_rel). |
| `crop_rectangle2` | 회전 사각형 (row,col,phi,l1,l2)를 잘라내 축평행화(crop_rectangle2). |
| `decompose2` | 2채널 이미지를 2장의 이미지로 분해한다. |
| `decompose3` | 3채널 이미지를 3장의 이미지로 분해한다. |
| `decompose4` | 4채널 이미지를 4장의 이미지로 분해한다. |
| `decompose5` | 5채널 이미지를 5장의 이미지로 분해한다. |
| `decompose6` | 6채널 이미지를 6장의 이미지로 분해한다. |
| `decompose7` | 7채널 이미지를 7장의 이미지로 분해한다. |
| `elliptic_axis_gray` | 그레이 값 가중 2차 모멘트의 등가 타원 (ra, rb, phi)(elliptic_axis_gray). |
| `fuzzy_entropy` | 영역 그레이 분포의 Shannon 엔트로피(fuzzy_entropy). |
| `fuzzy_perimeter` | 그레이 기울기 총합에 의한 fuzzy 둘레 길이(fuzzy_perimeter). |
| `gen_cooc_matrix` | 그레이 동시발생 행렬 (GLCM)(gen_cooc_matrix). direction=0/45/90/135도. |
| `gen_image1` | 1채널 배열로 이미지를 만든다(gen_image1). |
| `gen_image1_extern` | 외부 메모리(1D/2D)에서 1채널 이미지를 구성(gen_image1_extern). |
| `gen_image1_rect` | 이미지에서 사각형 영역을 잘라낸다(gen_image1_rect). |
| `gen_image3` | 3채널 배열로 (H,W,3) 이미지를 만든다(gen_image3). |
| `gen_image3_extern` | 외부 메모리(interleaved)에서 3채널 이미지를 구성(gen_image3_extern). |
| `gen_image_const` | 상수값으로 채운 이미지(gen_image_const). |
| `gen_image_gray_ramp` | 선형 경사 이미지 g = alpha*(c-cx)+beta*(r-cy)+mean(gen_image_gray_ramp). |
| `gen_image_interleaved` | 화소 인터리브 1D 배열을 (H,W,C) 이미지로 복원(gen_image_interleaved). |
| `gen_image_surface_first_order` | 1차 서피스 이미지 g = alpha*(c-col0)+beta*(r-row0)+gamma(gen_image_surface_first_order). |
| `gen_image_surface_second_order` | 2차 서피스 이미지 g = a*x^2+b*x*y+c*y^2+d*x+e*y+f(gen_image_surface_second_order). |
| `get_grayval` | (row,col)의 그레이 값을 반환(최근접)(get_grayval). |
| `get_grayval_interpolated` | (row,col)의 쌍선형 보간 그레이 값(get_grayval_interpolated). |
| `gray_features` | 영역의 그레이 특징(mean/deviation/min/max/median/area)(gray_features). |
| `gray_histo` | 그레이 히스토그램(절대 도수와 상대 도수)(gray_histo). |
| `gray_histo_range` | 지정 레인지의 그레이 히스토그램(gray_histo_range). |
| `gray_projections` | 행 방향/열 방향의 그레이 투영(gray_projections). |
| `histo_2dim` | 2채널의 2차원 히스토그램(histo_2dim). |
| `image_to_channels` | 다채널 이미지를 개별 채널로 나눈다(image_to_channels). |
| `interleave_channels` | 채널을 화소 인터리브 배치의 1개 배열로(interleave_channels). |
| `moments_gray_plane` | 1차 그레이 모멘트(평면 근사 계수 alpha,beta,mean)(moments_gray_plane). |
| `overpaint_gray` | paint_gray와 같은 의미로 source를 겹쳐 그림(overpaint_gray). |
| `overpaint_region` | paint_region과 같은 의미로 영역을 겹쳐 칠함(overpaint_region). |
| `paint_gray` | source 이미지의 그레이 값을 (영역 내에서) image로 전사(paint_gray). |
| `paint_region` | 영역을 상수 그레이 값으로 칠한다(paint_region). |
| `paint_xld` | XLD 윤곽을 이미지에 그린다(paint_xld). |
| `real_to_complex` | 실부/허부 이미지를 복소 이미지로 합성(real_to_complex). |
| `real_to_vector_field` | 2장의 실이미지를 (H,W,2) 벡터장으로 합성(real_to_vector_field). |
| `select_gray` | 그레이 특징이 [minv,maxv]에 들어가는 영역만 선택(select_gray). regions=bool mask의 리스트. |
| `shape_histo_all` | 임계값을 스윕해 각 레벨의 영역 면적을 모은 형상 히스토그램(shape_histo_all). |
| `shape_histo_point` | 지정 점을 포함하는 연결 영역의 면적을 임계값마다 모은다(shape_histo_point). |
| `tile_channels` | 다채널을 1장의 그레이 이미지로 타일 배치(tile_channels). |
| `tile_images` | 같은 크기의 이미지 군을 그리드로 타일(tile_images). |
| `tile_images_offset` | 각 이미지를 offset (row,col)에 붙여 합성(tile_images_offset). |
| `vector_field_to_real` | 벡터장 (H,W,2)를 row/col 성분 이미지로 분해(vector_field_to_real). |

#### Filters(58 op)

공간 필터 전반. 평활화·선예화·미분계 등, 화소 근방의 합성곱으로 이미지를 다듬는 일군이다.

![Filters의 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_01_gauss_image.png)
*그림: 가우스 평활화의 예(11.1.1절에서 재게재)*

| op | 설명 |
|---|---|
| `abs_diff_image` | /image1-image2/*mult(abs_diff_image). |
| `add_image` | (image1+image2)*mult+add(add_image). |
| `apply_color_trans_lut` | RGB (H,W,3)를 LUT의 색 공간으로 변환(apply_color_trans_lut). rgb_to_hsv / rgb_to_yuv 등. |
| `atan2_image` | atan2(image1, image2)(vector field의 각도, atan2_image). |
| `bit_and` | 정수화한 화소의 비트 AND(bit_and). |
| `bit_not` | 비트 반전(bit_not). |
| `bit_or` | 비트 OR(bit_or). |
| `bit_xor` | 비트 XOR(bit_xor). |
| `clear_color_trans_lut` | 색 변환 LUT를 파기(clear_color_trans_lut). |
| `convert_map_type` | 맵/이미지의 형 변환(convert_map_type). |
| `convol_channels` | 다채널 이미지를 각 채널 합성곱(convol_channels). image=(H,W,C) or 2D. |
| `convol_fft` | FFT에 의한 선형 합성곱(convol_fft/convol_image). |
| `convol_image` | 공간 합성곱(convol_image). |
| `correlation_fft` | FFT에 의한 상호 상관(correlation_fft). |
| `create_color_trans_lut` | 색 변환 LUT(변환 종별)를 만든다(create_color_trans_lut). |
| `crop_domain` | domain의 외접 사각형으로 이미지를 잘라낸다(crop_domain). |
| `derivate_vector_field` | 벡터장의 발산/회전/야코비안을 계산(derivate_vector_field). |
| `deviation_n` | 이미지 스택의 화소 표준 편차(deviation_n). |
| `div_image` | image1/image2*mult+add(div_image). 0 나눗셈은 보호. |
| `energy_gabor` | Gabor 실/허 응답에서 에너지(진폭 제곱)(energy_gabor). |
| `exhaustive_match` | 전탐색 NCC의 최적 일치(find_ncc_model과 같은 핵, error=1-score도 반환). |
| `exhaustive_match_mg` | 멀티그리드 전탐색 템플릿 매칭(coarse-to-fine으로 고속화)(exhaustive_match_mg). |
| `gauss_distribution` | 정규 분포의 확률 밀도 테이블(gauss_distribution). 노이즈 모델용. |
| `gen_canonical_variates_trans` | 클래스가 있는 다채널 이미지에서 정준 변량(LDA) 변환을 구한다(gen_canonical_variates_trans). |
| `gen_filter_mask` | 임의 계수의 필터 마스크를 생성(gen_filter_mask). |
| `gen_gauss_filter` | 정규화 2D 가우스 필터 마스크(gen_gauss_filter). |
| `gen_mean_filter` | 평균(box) 필터 마스크(gen_mean_filter). |
| `gen_principal_comp_trans` | 다채널 이미지 군에서 주성분 변환(고유 벡터/고윳값)을 구한다(gen_principal_comp_trans). |
| `gen_psf_defocus` | 원형 흐림(디포커스) PSF(gen_psf_defocus). |
| `gen_psf_motion` | 직선 블러(모션) PSF(gen_psf_motion). |
| `gen_savitzky_golay_filter` | Savitzky-Golay 평활/미분 1D 필터 계수(gen_savitzky_golay_filter). |
| `gen_sin_bandpass` | 정현파 창의 주파수 대역 통과 마스크(gen_sin_bandpass). |
| `gen_std_bandpass` | Butterworth형의 대역 통과 마스크(gen_std_bandpass). |
| `harmonic_interpolation` | 구멍(region=True)을 Laplace 방정식(조화 함수)으로 메운다(harmonic_interpolation). |
| `inpainting_aniso` | 이방성 확산(Perona-Malik)으로 결손 영역을 복원(inpainting_aniso). |
| `inpainting_ced` | 코히런스 강조 확산(구조 텐서 방향으로 확산)으로 인페인트(inpainting_ced). |
| `inpainting_ct` | 코히런스 수송에 가까운 등방 확산 인페인트(inpainting_ct). |
| `inpainting_mcf` | 평균 곡률류(Mean Curvature Flow) 인페인트(inpainting_mcf). |
| `inpainting_texture` | 텍스처 합성 인페인트(근방의 기지 패치 복사)(inpainting_texture). |
| `map_image` | LUT (map)를 화소에 적용(map_image). map은 길이 N의 1D 배열. |
| `max_image` | 화소별 최대(max_image). |
| `mean_n` | 이미지 스택의 화소 평균(mean_n). |
| `midrange_image` | 국소 (min+max)/2의 midrange 필터(midrange_image). |
| `min_image` | 화소별 최소(min_image). |
| `mult_image` | image1*image2*mult+add(mult_image). |
| `noise_distribution_mean` | 복수 관측에서 화소별 노이즈 표준 편차의 평균을 추정(noise_distribution_mean). |
| `optical_flow_mg` | 멀티그리드(coarse-to-fine 피라미드 + warping) Horn-Schunck 밀집 옵티컬 플로 |
| `phase_correlation_fft` | 위상 상관으로 병진 (drow, dcol)을 추정(phase_correlation_fft). |
| `points_sojka` | Sojka의 기울기 공분산에 기반한 코너 응답으로 서브픽셀 코너를 추출 |
| `rank_n` | 이미지 스택의 화소 rank 값(순위 통계, rank_n). 기본은 중앙값. |
| `scene_flow_calib` | 교정된 신 플로(내부 행렬로 3D 변위를 메트릭화)(scene_flow_calib). |
| `scene_flow_uncalib` | 좌우 2시각의 이미지에서 3D 신 플로(미교정 근사)를 추정(scene_flow_uncalib). |
| `sp_distribution` | salt-and-pepper 노이즈 분포(양끝에 질량, 중앙 균일)(sp_distribution). |
| `sub_image` | (image1-image2)*mult+add(sub_image). |
| `unwarp_image_vector_field` | 벡터장을 따라 이미지를 워프(역매핑)(unwarp_image_vector_field). |
| `vector_field_length` | 벡터장 각 점의 크기(vector_field_length). |
| `wiener_filter` | Wiener 디컨볼루션(wiener_filter). |
| `wiener_filter_ni` | 비반복 Wiener 복원(wiener_filter_ni). |

#### edges(56 op)

엣지(윤곽) 검출. Sobel 계열의 기울기부터 Canny의 세선화까지. 계측의 기준선은 대개 여기서 태어난다.

![edges의 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_04_canny.png)
*그림: Canny 엣지 검출의 예(11.1.1절에서 재게재)*

| op | 설명 |
|---|---|
| `corner_response` | edges op(HALCON: points_harris) |
| `cv_corner_harris` | edges op(HALCON: points_harris) |
| `cv_laplacian` | edges op(HALCON: laplace) |
| `cv_min_eigen` | edges op(HALCON: points_harris) |
| `cv_precorner` | edges op(HALCON: corner_response) |
| `cv_scharr` | edges op(HALCON: edges_image) |
| `derivate_gauss` | edges op(HALCON: derivate_gauss) |
| `diff_of_gauss` | edges op(HALCON: diff_of_gauss) |
| `dog` | edges op(HALCON: diff_of_gauss) |
| `dots_image` | edges op(HALCON: dots_image) |
| `edges_color` | edges op(HALCON: edges_color) |
| `f2_shock` | edges op(HALCON: shock_filter) |
| `f2_topographic` | edges op(HALCON: topographic_sketch) |
| `frei_amp` | edges op(HALCON: frei_amp) |
| `frei_dir` | edges op(HALCON: frei_dir) |
| `grad_dir` | edges op(HALCON: -) |
| `kirsch_amp` | edges op(HALCON: kirsch_amp) |
| `kirsch_dir` | edges op(HALCON: kirsch_dir) |
| `laplace` | edges op(HALCON: laplace) |
| `laplace_of_gauss` | edges op(HALCON: laplace_of_gauss) |
| `log` | edges op(HALCON: laplace_of_gauss) |
| `points_foerstner` | edges op(HALCON: points_foerstner) |
| `points_harris_binomial` | edges op(HALCON: points_harris_binomial) |
| `prewitt_amp` | edges op(HALCON: prewitt_amp) |
| `prewitt_dir` | edges op(HALCON: prewitt_dir) |
| `prewitt_mag` | edges op(HALCON: prewitt_amp) |
| `roberts` | edges op(HALCON: roberts) |
| `roberts_mag` | edges op(HALCON: roberts) |
| `robinson_amp` | edges op(HALCON: robinson_amp) |
| `robinson_dir` | edges op(HALCON: robinson_dir) |
| `sk_corner_harris` | edges op(HALCON: points_harris) |
| `sk_dog` | edges op(HALCON: diff_of_gauss) |
| `sk_farid` | edges op(HALCON: edges_image) |
| `sk_hessian_det` | edges op(HALCON: -) |
| `sk_scharr` | edges op(HALCON: edges_image) |
| `sobel_amp` | edges op(HALCON: sobel_amp) |
| `sobel_dir` | edges op(HALCON: sobel_dir) |
| `sobel_mag` | edges op(HALCON: sobel_amp) |
| `tf_phase_congruency` | edges op(HALCON: -) |
| `tf_steerable_filter` | edges op(HALCON: -) |
| `xkor_dog` | edges op(HALCON: -) |
| `xkor_gftt` | edges op(HALCON: -) |
| `xkor_harris` | edges op(HALCON: -) |
| `xkor_hessian` | edges op(HALCON: -) |
| `xkor_laplacian` | edges op(HALCON: -) |
| `xpil_contour` | edges op(HALCON: -) |
| `xpil_find_edges` | edges op(HALCON: -) |
| `xsk2_corner_kr` | edges op(HALCON: -) |
| `xsk2_inv_gauss_grad` | edges op(HALCON: -) |
| `xsk3_corner_fast` | edges op(HALCON: -) |
| `xsk3_corner_moravec` | edges op(HALCON: -) |
| `xsk_hessian_eig` | edges op(HALCON: -) |
| `xsp_gauss_grad_mag` | edges op(HALCON: -) |
| `xsp_morph_laplace` | edges op(HALCON: -) |
| `xwt_directional_detail` | edges op(HALCON: -) |
| `xwt_hf_reconstruct` | edges op(HALCON: -) |

#### segmentation(54 op)

이미지를 의미 있는 영역으로 잘라 나누는 세그멘테이션. 임계값 계열부터 분수령(watershed)까지.

![segmentation의 예](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_14_watersheds.png)
*그림: 분수령법의 예(11.1.1절에서 재게재)*

| op | 설명 |
|---|---|
| `adaptive_gauss_thresh` | segmentation op(HALCON: local_threshold) |
| `auto_threshold` | segmentation op(HALCON: auto_threshold) |
| `bin_threshold` | segmentation op(HALCON: bin_threshold) |
| `binary_threshold` | segmentation op(HALCON: binary_threshold) |
| `canny` | segmentation op(HALCON: edges_image) |
| `cv_adaptive_gauss` | segmentation op(HALCON: local_threshold) |
| `cv_adaptive_mean` | segmentation op(HALCON: dyn_threshold) |
| `cv_canny` | segmentation op(HALCON: edges_image) |
| `cv_otsu` | segmentation op(HALCON: binary_threshold) |
| `dual_threshold` | segmentation op(HALCON: dual_threshold) |
| `dyn_threshold` | segmentation op(HALCON: dyn_threshold) |
| `edges_image` | segmentation op(HALCON: edges_image) |
| `fast_threshold` | segmentation op(HALCON: fast_threshold) |
| `h_threshold` | segmentation op(HALCON: threshold) |
| `hysteresis_threshold` | segmentation op(HALCON: hysteresis_threshold) |
| `it_region_to_bin` | segmentation op(HALCON: region_to_bin) |
| `local_max` | segmentation op(HALCON: local_max_sub_pix) |
| `local_min` | segmentation op(HALCON: local_min) |
| `local_threshold` | segmentation op(HALCON: local_threshold) |
| `nonmax_suppression_amp` | segmentation op(HALCON: nonmax_suppression_amp) |
| `otsu` | segmentation op(HALCON: binary_threshold) |
| `pouring` | segmentation op(HALCON: pouring) |
| `regiongrowing` | segmentation op(HALCON: regiongrowing) |
| `regiongrowing_mean` | segmentation op(HALCON: regiongrowing_mean) |
| `segment_image_mser` | segmentation op(HALCON: segment_image_mser) |
| `sk_canny` | segmentation op(HALCON: edges_image) |
| `sk_chan_vese` | segmentation op(HALCON: -) |
| `sk_felzenszwalb` | segmentation op(HALCON: -) |
| `sk_hysteresis` | segmentation op(HALCON: hysteresis_threshold) |
| `sk_li` | segmentation op(HALCON: binary_threshold) |
| `sk_local_maxima` | segmentation op(HALCON: local_max) |
| `sk_niblack` | segmentation op(HALCON: var_threshold) |
| `sk_otsu` | segmentation op(HALCON: binary_threshold) |
| `sk_sauvola` | segmentation op(HALCON: var_threshold) |
| `sk_slic` | segmentation op(HALCON: -) |
| `sk_yen` | segmentation op(HALCON: binary_threshold) |
| `threshold` | segmentation op(HALCON: threshold) |
| `var_threshold` | segmentation op(HALCON: var_threshold) |
| `watersheds` | segmentation op(HALCON: watersheds) |
| `watersheds_threshold` | segmentation op(HALCON: watersheds_threshold) |
| `xcv2_meanshift` | segmentation op(HALCON: -) |
| `xcv_grabcut` | segmentation op(HALCON: -) |
| `xcv_watershed_markers` | segmentation op(HALCON: watersheds) |
| `xkor_canny` | segmentation op(HALCON: -) |
| `xmh_bernsen` | segmentation op(HALCON: -) |
| `xsk2_h_maxima` | segmentation op(HALCON: -) |
| `xsk2_multiotsu` | segmentation op(HALCON: -) |
| `xsk3_h_minima` | segmentation op(HALCON: -) |
| `xsk3_peak_local_max` | segmentation op(HALCON: -) |
| `xsk3_rank_otsu` | segmentation op(HALCON: -) |
| `xsk3_threshold_local_median` | segmentation op(HALCON: -) |
| `xsk_flood` | segmentation op(HALCON: -) |
| `xsk_random_walker` | segmentation op(HALCON: -) |
| `zero_crossing` | segmentation op(HALCON: zero_crossing) |

#### smoothing(48 op)

평활화 전문의 일군. 가우스·바이래터럴·이방성 확산 등 「노이즈는 지우되 엣지는 지킨다」 계열의 구분 사용이 핵심이다.


![fops_smoothing](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_smoothing.png)
*그림: smoothing의 실처리 예 — 같은 잡음 입력에 대해 가우스 평활화는 윤곽째 흐리게 만들지만, anisotropic_diffusion(이방성 확산)은 엣지를 넘지 않고 확산하므로 윤곽을 유지한 채 잡음만 고른다(Fullseye 실출력). 입력은 skimage camera+AI 생성 이미지(Gemini) 2종.*

| op | 설명 |
|---|---|
| `anisotropic_diffusion` | smoothing op(HALCON: anisotropic_diffusion) |
| `bilateral` | smoothing op(HALCON: bilateral_filter) |
| `bilateral_filter` | smoothing op(HALCON: bilateral_filter) |
| `binomial_filter` | smoothing op(HALCON: binomial_filter) |
| `coherence_enhancing_diff` | smoothing op(HALCON: coherence_enhancing_diff) |
| `cv_bilateral` | smoothing op(HALCON: bilateral_filter) |
| `cv_box` | smoothing op(HALCON: mean_image) |
| `cv_gaussian` | smoothing op(HALCON: gauss_filter) |
| `cv_nlmeans` | smoothing op(HALCON: -) |
| `cv_sharpen` | smoothing op(HALCON: emphasize) |
| `dl_aniso_diffusion` | smoothing op(HALCON: anisotropic_diffusion) |
| `dl_guided_filter` | smoothing op(HALCON: guided_filter) |
| `f2_gauss_pyramid` | smoothing op(HALCON: gen_gauss_pyramid) |
| `gauss_filter` | smoothing op(HALCON: gauss_filter) |
| `gauss_image` | smoothing op(HALCON: gauss_image) |
| `gaussian` | smoothing op(HALCON: gauss_filter) |
| `guided_filter` | smoothing op(HALCON: guided_filter) |
| `isotropic_diffusion` | smoothing op(HALCON: isotropic_diffusion) |
| `mean_box` | smoothing op(HALCON: mean_image) |
| `mean_curvature_flow` | smoothing op(HALCON: mean_curvature_flow) |
| `mean_image` | smoothing op(HALCON: mean_image) |
| `sigma_image` | smoothing op(HALCON: sigma_image) |
| `simulate_defocus` | smoothing op(HALCON: simulate_defocus) |
| `simulate_motion` | smoothing op(HALCON: simulate_motion) |
| `sk_nlm` | smoothing op(HALCON: -) |
| `sk_rolling_ball` | smoothing op(HALCON: -) |
| `sk_tv` | smoothing op(HALCON: -) |
| `sk_tv_bregman` | smoothing op(HALCON: -) |
| `sk_wavelet` | smoothing op(HALCON: -) |
| `smooth_image` | smoothing op(HALCON: smooth_image) |
| `unsharp` | smoothing op(HALCON: emphasize) |
| `xcv3_denoise_tvl1` | smoothing op(HALCON: -) |
| `xcv3_pyr_laplacian` | smoothing op(HALCON: -) |
| `xcv_edge_preserving` | smoothing op(HALCON: -) |
| `xkor_bilateral` | smoothing op(HALCON: -) |
| `xkor_gaussian` | smoothing op(HALCON: -) |
| `xkor_motion_blur` | smoothing op(HALCON: -) |
| `xkor_unsharp` | smoothing op(HALCON: -) |
| `xpil_smooth_more` | smoothing op(HALCON: -) |
| `xpil_unsharp_mask` | smoothing op(HALCON: -) |
| `xsk3_rank_mean_bilateral` | smoothing op(HALCON: -) |
| `xsp_cspline_smooth` | smoothing op(HALCON: -) |
| `xsp_dct_denoise` | smoothing op(HALCON: -) |
| `xsp_savgol` | smoothing op(HALCON: -) |
| `xsp_wiener` | smoothing op(HALCON: -) |
| `xwt_firm_denoise` | smoothing op(HALCON: -) |
| `xwt_lf_reconstruct` | smoothing op(HALCON: -) |
| `xwt_visushrink` | smoothing op(HALCON: -) |
