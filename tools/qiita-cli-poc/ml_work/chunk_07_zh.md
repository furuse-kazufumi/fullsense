#### Transformations(79 op)

图像的几何变换(旋转、缩放、射影、极坐标等)。在检测中作为"先把工件的朝向摆正再测量"的前置步骤每次都会登场。


![fops_transformations](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_transformations.png)
*图: Transformations 的实处理示例 — 斜视角下的平面用仿射变换(6 自由度)无法矫正梯形畸变,只有用从 4 点对应经 DLT 估计的射影变换(vector_to_proj_hom_mat2d → gen_image_warp_map)才能整流为正上方视角(Fullseye 实输出)。第 1 行是已知单应矩阵的合成(有真值),第 2-3 行是 AI 生成图像(Gemini)。*

| op | 说明 |
|---|---|
| `affine_trans_pixel` | 对像素 (row,col) 施加仿射变换(HALCON 采用 (row,col) 顺序)。 |
| `affine_trans_point_2d` | 对点列施加任意 2D 仿射变换。 |
| `axis_angle_to_quat` | 由旋转轴和角度构建旋转四元数。 |
| `convert_point_3d_cart_to_spher` | 把 3D 点的直角坐标转换为球面坐标。 |
| `convert_point_3d_spher_to_cart` | 把 3D 点的球面坐标转换为直角坐标。 |
| `convert_pose_type` | 返回 pose 的排列(真正类型转换的简化版=恒等并附加 type 标签)。 |
| `dual_quat_compose` | 对偶四元数的复合(刚体变换的复合、dual_quat_compose)。 |
| `dual_quat_conjugate` | 返回对偶四元数的共轭。 |
| `dual_quat_interpolate` | 对偶四元数的插值(经由 pose 做平移 lerp + 旋转 slerp、dual_quat_interpolate)。 |
| `dual_quat_normalize` | 归一化对偶四元数。 |
| `dual_quat_to_hom_mat3d` | 把单位对偶四元数 [qr(4), qd(4)] 转为 4x4 刚体变换(dual_quat_to_hom_mat3d)。 |
| `dual_quat_to_pose` | 把对偶四元数转换为 3D pose 表示。 |
| `dual_quat_to_screw` | 由对偶四元数返回螺旋分量(角度、平移、轴)(dual_quat_to_screw)。 |
| `dual_quat_trans_line_3d` | 用对偶四元数变换 3D 直线(对点和方向做刚体变换)(dual_quat_trans_line_3d)。 |
| `dual_quat_trans_point_3d` | 用单位对偶四元数对 3D 点做刚体变换。 |
| `gen_image_warp_map` | 由 2D 单应矩阵生成像素扭曲映射(逆映射)(gen_image_warp_map)。 |
| `get_pose_type` | 返回 3D pose 的表示形式(旋转的持有方式)。 |
| `get_rectangle_pose` | 由图像上的矩形估计平面姿态(4 角对应 → homography → pose)(get_rectangle_pose)。 |
| `hom_mat2d_compose` | 复合(相乘)2 个 2D 齐次变换矩阵。 |
| `hom_mat2d_determinant` | 计算 2D 齐次变换矩阵的行列式。 |
| `hom_mat2d_identity` | 创建恒等 2D 变换的齐次矩阵。 |
| `hom_mat2d_invert` | 求 2D 齐次变换矩阵的逆矩阵。 |
| `hom_mat2d_reflect` | 向 2D 齐次变换矩阵追加镜像。 |
| `hom_mat2d_reflect_local` | 向 2D 齐次变换矩阵追加局部坐标系下的镜像。 |
| `hom_mat2d_rotate` | 向 2D 齐次变换矩阵追加旋转。 |
| `hom_mat2d_rotate_local` | 向 2D 齐次变换矩阵追加局部坐标系下的旋转。 |
| `hom_mat2d_scale` | 向 2D 齐次变换矩阵追加缩放。 |
| `hom_mat2d_scale_local` | 向 2D 齐次变换矩阵追加局部坐标系下的缩放。 |
| `hom_mat2d_slant` | 向 2D 齐次变换矩阵追加剪切(slant)。 |
| `hom_mat2d_slant_local` | 向 2D 齐次变换矩阵追加局部坐标系下的剪切。 |
| `hom_mat2d_to_affine_par` | 把 2D 仿射矩阵分解为 (sx, sy, phi, theta, tx, ty)。 |
| `hom_mat2d_translate` | 向 2D 齐次变换矩阵追加平移。 |
| `hom_mat2d_translate_local` | 向 2D 齐次变换矩阵追加局部坐标系下的平移。 |
| `hom_mat2d_transpose` | 转置 2D 齐次变换矩阵。 |
| `hom_mat3d_compose` | 复合(相乘)2 个 3D 齐次变换矩阵。 |
| `hom_mat3d_determinant` | 计算 3D 齐次变换矩阵的行列式。 |
| `hom_mat3d_identity` | 创建恒等 3D 变换的齐次矩阵。 |
| `hom_mat3d_invert` | 求 3D 齐次变换矩阵的逆矩阵。 |
| `hom_mat3d_project` | 用 4x4 透视投影矩阵把 3D 点投到 2D 图像点(hom_mat3d_project)。 |
| `hom_mat3d_rotate` | 绕轴的右手系旋转做左乘(axis 0=x,1=y,2=z、标准符号约定)。 |
| `hom_mat3d_rotate_local` | 向 3D 齐次变换矩阵追加局部坐标系下的旋转。 |
| `hom_mat3d_scale` | 向 3D 齐次变换矩阵追加缩放。 |
| `hom_mat3d_scale_local` | 向 3D 齐次变换矩阵追加局部坐标系下的缩放。 |
| `hom_mat3d_to_pose` | 把 4x4 变换矩阵分解为 pose [rx,ry,rz(ZYX euler), tx,ty,tz]。 |
| `hom_mat3d_translate` | 向 3D 齐次变换矩阵追加平移。 |
| `hom_mat3d_translate_local` | 向 3D 齐次变换矩阵追加局部坐标系下的平移。 |
| `hom_mat3d_transpose` | 转置 3D 齐次变换矩阵。 |
| `hom_vector_to_proj_hom_mat2d` | 由 4 点以上的对应求射影变换(homography, DLT)3x3(hom_vector_to_proj_hom_mat2d)。 |
| `point_line_to_hom_mat2d` | 由点+方向的对应估计 2D 刚体变换(point_line_to_hom_mat2d)。 |
| `point_pluecker_line_to_hom_mat3d` | 由点+Plücker 直线的对应估计 3D 刚体变换(point_pluecker_line_to_hom_mat3d)。 |
| `pose_average` | 求多个 pose 的平均 pose。 |
| `pose_compose` | 复合 2 个 3D pose。 |
| `pose_invert` | 把 3D pose 列的各元素变为逆变换。 |
| `pose_to_dual_quat` | 把 3D pose 转换为单位对偶四元数。 |
| `pose_to_hom_mat3d` | 把 pose [rx,ry,rz(rad), tx,ty,tz] 转为 4x4 变换矩阵(hom_mat3d_to_pose 的逆)。 |
| `pose_to_quat` | 把 3D pose 的旋转分量转换为四元数。 |
| `proj_hom_mat2d_to_pose` | 由单应矩阵和内参矩阵分解出平面的姿态(R,t)(proj_hom_mat2d_to_pose)。 |
| `projective_trans_hom_point_3d` | 对齐次 3D 点施加 4x4 射影变换(projective_trans_hom_point_3d)。 |
| `projective_trans_pixel` | 对像素 (row,col) 施加射影变换(HALCON (row,col) 顺序)。 |
| `projective_trans_point_3d` | 用射影变换矩阵投影 3D 点。 |
| `quat_compose` | 计算 2 个四元数的乘积。 |
| `quat_conjugate` | 返回四元数的共轭。 |
| `quat_interpolate` | slerp 球面线性插值。 |
| `quat_normalize` | 归一化四元数。 |
| `quat_rotate_point_3d` | 用单位四元数旋转 3D 点。 |
| `quat_to_hom_mat3d` | 把四元数转换为对应的旋转矩阵。 |
| `quat_to_pose` | 把四元数转换为对应的 3D pose。 |
| `screw_to_dual_quat` | 把螺旋(轴方向 l, 矩 m, 旋转角 theta, 平移 d)转为对偶四元数(screw_to_dual_quat)。 |
| `set_origin_pose` | 把姿态的原点按局部偏移移动(set_origin_pose)。 |
| `vector_angle_to_rigid` | 由 1 组 (点, 角度) 求 2D 刚体变换(vector_angle_to_rigid)。 |
| `vector_field_to_hom_mat2d` | 最小二乘估计与整个向量场最吻合的仿射变换(2x3)(vector_field_to_hom_mat2d)。 |
| `vector_to_aniso` | 由 2D 点对应估计各向异性(非等向缩放)仿射变换(vector_to_aniso)。 |
| `vector_to_hom_mat2d` | 由点对应估计 2D 单应矩阵(vector_to_hom_mat2d)。 |
| `vector_to_hom_mat3d` | 由 3D 点对应用 Umeyama 估计刚体/相似变换(4x4)(vector_to_hom_mat3d)。 |
| `vector_to_pose` | 由 6 组以上的 3D↔2D 对应估计物体/相机的 6 自由度 pose (R, t)(PnP)。 |
| `vector_to_proj_hom_mat2d` | 由 2D 点对应用 DLT 估计射影变换(单应矩阵 3x3)(vector_to_proj_hom_mat2d)。 |
| `vector_to_proj_hom_mat2d_distortion` | 在含畸变的条件下估计射影变换(假设畸变较小、采用 DLT)(vector_to_proj_hom_mat2d_distortion)。 |
| `vector_to_rigid` | 由对应点求 2D 刚体变换(旋转+平移、Kabsch)(vector_to_rigid)。 |
| `vector_to_similarity` | 由对应点求 2D 相似变换(旋转+缩放+平移、Umeyama)(vector_to_similarity)。 |

#### features(77 op)

从区域和轮廓中提取数值特征(面积、周长、圆形度、矩等)的 op 群。"把图像变成数字"这一测量任务的主阵地。

![features 的示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_13_area_center.png)
*图: 面积、重心测量的示例(11.1.1 节再次引用)*

| op | 说明 |
|---|---|
| `ORB` | ORB 关键点(cv2.ORB,不可用时用 numpy 的 Harris 角点)(features.ORB)。  [backend=opencv] |
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
| `describe_patches` | 把各关键点周边的亮度 patch 归一化为均值 0、范数 1 的描述子。 |
| `diameter_region` | features op(HALCON: diameter_region) |
| `diameter_xld` | features op(HALCON: diameter_xld) |
| `eccentricity` | features op(HALCON: eccentricity) |
| `eccentricity_xld` | features op(HALCON: eccentricity_xld) |
| `elliptic_axis` | features op(HALCON: elliptic_axis) |
| `elliptic_axis_xld` | features op(HALCON: elliptic_axis_xld) |
| `entropy_gray` | features op(HALCON: entropy_gray) |
| `estimate_noise` | features op(HALCON: estimate_noise) |
| `euler_number` | features op(HALCON: euler_number) |
| `fast_corners` | FAST 型角点关键点检测(按响应强度排序)。 |
| `get_region_thickness` | features op(HALCON: get_region_thickness) |
| `gray_histo_abs` | features op(HALCON: gray_histo_abs) |
| `harris_corners` | Harris 角点关键点检测(按响应强度排序)。 |
| `height_width_ratio` | features op(HALCON: height_width_ratio) |
| `hough_circle_trans` | features op(HALCON: hough_circle_trans) |
| `hough_line_trans` | features op(HALCON: hough_line_trans) |
| `intensity` | features op(HALCON: intensity) |
| `length_xld` | features op(HALCON: length_xld) |
| `match_descriptors` | 用最近邻 + Lowe 比率检验对 2 组描述子做匹配。 |
| `match_keypoints` | 一次性执行 2 幅图像间的关键点检测、描述与匹配。 |
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

二值区域(region)的生成、合成、筛选。阈值处理 → 连通域 → 条件筛选,是这里的经典三连招。

![region 的示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_05_threshold_label.png)
*图: 二值化 → 连通域标记的示例(11.1.1 节再次引用)*

| op | 说明 |
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
| `r2_inner_circle` | 把最大内切圆画成掩膜(a 用于缩放绘制半径,a=0.5 时严格)。 |
| `r2_inner_rectangle1` | 最大的轴平行内接矩形(a 用于缩小绘制矩形,a=0 时严格)。 |
| `r2_partition_rectangle` | 把区域的外接矩形划分为 N×N 网格,只保留与区域重叠的单元。 |
| `r2_runlength_features` | 区域→特征量: 水平方向前景游程长度的平均。 |
| `r2_smallest_circle` | 把最小包含圆画成掩膜(Welzl 法,a 用于放大半径)。 |
| `r2_smallest_rectangle1` | 轴平行的外接矩形(边界框)。 |
| `r2_smallest_rectangle2` | 把面积最小的有向外接矩形掩膜化(旋转卡壳法)。 |
| `r2_sort_region` | 只保留第 k 大的连通域(k = round(a*(n-1)))。 |
| `r2_split_skeleton_lines` | 把区域细线化为骨架,在分叉点(邻域数 3 以上)处切分。 |
| `r2_union1` | 把全部连通域合并为 1 个掩膜(标签的 OR)。 |
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

图像的生成、输入输出、通道操作、算术合成等,处理图像本身的基础 op 群。


![fops_image_chapter](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_image_chapter.png)
*图: Image 的实处理示例 — 用 decompose3 把彩色图像分解为 R/G/B 通道。每个通道承载的信息不同(在眼底图像中,血管与背景的对比度分配随通道差异巨大)(Fullseye 实输出)。输入为 scikit-image 自带 retina + AI 生成图像(Gemini)2 种。非诊断用途,仅为图像处理演示。*

| op | 说明 |
|---|---|
| `add_channels` | 把 gray 图像作为通道追加到 base 图像(add_channels)。 |
| `append_channel` | 向多通道图像追加 1 个通道(append_channel)。 |
| `area_center_gray` | 以灰度值为权重的面积(质量)与重心 (row,col)(area_center_gray)。 |
| `change_domain` | 把图像的 domain(ROI)改为 region(区域外做 0 掩膜)(change_domain)。 |
| `channels_to_image` | 把 2D 通道的列表/序列变为多通道图像(channels_to_image)。 |
| `complex_to_real` | 把复数图像分解为实部/虚部(complex_to_real)。 |
| `compose2` | 把 2 幅图像合并为 2 通道图像。 |
| `compose3` | 把 3 幅图像合并为 3 通道图像。 |
| `compose4` | 把 4 幅图像合并为 4 通道图像。 |
| `compose5` | 把 5 幅图像合并为 5 通道图像。 |
| `compose6` | 把 6 幅图像合并为 6 通道图像。 |
| `compose7` | 把 7 幅图像合并为 7 通道图像。 |
| `cooc_feature_matrix` | 由 GLCM 计算 Haralick 特征(energy/contrast/correlation/homogeneity)(cooc_feature_matrix)。 |
| `crop_domain_rel` | 按带相对边距的 domain 外接矩形裁剪(crop_domain_rel)。 |
| `crop_rectangle2` | 裁剪旋转矩形 (row,col,phi,l1,l2) 并转为轴平行(crop_rectangle2)。 |
| `decompose2` | 把 2 通道图像分解为 2 幅图像。 |
| `decompose3` | 把 3 通道图像分解为 3 幅图像。 |
| `decompose4` | 把 4 通道图像分解为 4 幅图像。 |
| `decompose5` | 把 5 通道图像分解为 5 幅图像。 |
| `decompose6` | 把 6 通道图像分解为 6 幅图像。 |
| `decompose7` | 把 7 通道图像分解为 7 幅图像。 |
| `elliptic_axis_gray` | 灰度值加权 2 阶矩的等效椭圆 (ra, rb, phi)(elliptic_axis_gray)。 |
| `fuzzy_entropy` | 区域灰度分布的 Shannon 熵(fuzzy_entropy)。 |
| `fuzzy_perimeter` | 由灰度梯度总和得到的 fuzzy 周长(fuzzy_perimeter)。 |
| `gen_cooc_matrix` | 灰度共生矩阵 (GLCM)(gen_cooc_matrix)。direction=0/45/90/135 度。 |
| `gen_image1` | 由 1 通道数组创建图像(gen_image1)。 |
| `gen_image1_extern` | 由外部内存(1D/2D)构建 1 通道图像(gen_image1_extern)。 |
| `gen_image1_rect` | 从图像中裁出矩形区域(gen_image1_rect)。 |
| `gen_image3` | 由 3 通道数组创建 (H,W,3) 图像(gen_image3)。 |
| `gen_image3_extern` | 由外部内存(interleaved)构建 3 通道图像(gen_image3_extern)。 |
| `gen_image_const` | 用常数值填充的图像(gen_image_const)。 |
| `gen_image_gray_ramp` | 线性斜坡图像 g = alpha*(c-cx)+beta*(r-cy)+mean(gen_image_gray_ramp)。 |
| `gen_image_interleaved` | 把像素交织的 1D 数组还原为 (H,W,C) 图像(gen_image_interleaved)。 |
| `gen_image_surface_first_order` | 1 次曲面图像 g = alpha*(c-col0)+beta*(r-row0)+gamma(gen_image_surface_first_order)。 |
| `gen_image_surface_second_order` | 2 次曲面图像 g = a*x^2+b*x*y+c*y^2+d*x+e*y+f(gen_image_surface_second_order)。 |
| `get_grayval` | 返回 (row,col) 处的灰度值(最近邻)(get_grayval)。 |
| `get_grayval_interpolated` | (row,col) 处的双线性插值灰度值(get_grayval_interpolated)。 |
| `gray_features` | 区域的灰度特征(mean/deviation/min/max/median/area)(gray_features)。 |
| `gray_histo` | 灰度直方图(绝对频数与相对频数)(gray_histo)。 |
| `gray_histo_range` | 指定范围的灰度直方图(gray_histo_range)。 |
| `gray_projections` | 行方向/列方向的灰度投影(gray_projections)。 |
| `histo_2dim` | 2 通道的二维直方图(histo_2dim)。 |
| `image_to_channels` | 把多通道图像拆分为各个通道(image_to_channels)。 |
| `interleave_channels` | 把通道排布成像素交织的一条数组(interleave_channels)。 |
| `moments_gray_plane` | 1 次灰度矩(平面近似系数 alpha,beta,mean)(moments_gray_plane)。 |
| `overpaint_gray` | 与 paint_gray 同义,叠绘 source(overpaint_gray)。 |
| `overpaint_region` | 与 paint_region 同义,叠涂区域(overpaint_region)。 |
| `paint_gray` | 把 source 图像的灰度值(在区域内)转写到 image(paint_gray)。 |
| `paint_region` | 用常数灰度值涂抹区域(paint_region)。 |
| `paint_xld` | 把 XLD 轮廓绘制到图像(paint_xld)。 |
| `real_to_complex` | 把实部/虚部图像合成为复数图像(real_to_complex)。 |
| `real_to_vector_field` | 把 2 幅实图像合成为 (H,W,2) 向量场(real_to_vector_field)。 |
| `select_gray` | 只选取灰度特征落在 [minv,maxv] 内的区域(select_gray)。regions=bool mask 的列表。 |
| `shape_histo_all` | 扫掠阈值、收集各级区域面积的形状直方图(shape_histo_all)。 |
| `shape_histo_point` | 按阈值逐级收集包含指定点的连通区域面积(shape_histo_point)。 |
| `tile_channels` | 把多通道平铺为 1 幅灰度图像(tile_channels)。 |
| `tile_images` | 把同尺寸图像组平铺成网格(tile_images)。 |
| `tile_images_offset` | 把各图像粘贴到 offset (row,col) 处合成(tile_images_offset)。 |
| `vector_field_to_real` | 把向量场 (H,W,2) 分解为 row/col 分量图像(vector_field_to_real)。 |

#### Filters(58 op)

空间滤波器全家桶。平滑、锐化、微分系等,用像素邻域的卷积整理图像的一群。

![Filters 的示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_01_gauss_image.png)
*图: 高斯平滑的示例(11.1.1 节再次引用)*

| op | 说明 |
|---|---|
| `abs_diff_image` | /image1-image2/*mult(abs_diff_image)。 |
| `add_image` | (image1+image2)*mult+add(add_image)。 |
| `apply_color_trans_lut` | 把 RGB (H,W,3) 转换到 LUT 的色彩空间(apply_color_trans_lut)。rgb_to_hsv / rgb_to_yuv 等。 |
| `atan2_image` | atan2(image1, image2)(vector field 的角度、atan2_image)。 |
| `bit_and` | 整数化像素的按位 AND(bit_and)。 |
| `bit_not` | 按位取反(bit_not)。 |
| `bit_or` | 按位 OR(bit_or)。 |
| `bit_xor` | 按位 XOR(bit_xor)。 |
| `clear_color_trans_lut` | 销毁颜色变换 LUT(clear_color_trans_lut)。 |
| `convert_map_type` | 映射/图像的类型转换(convert_map_type)。 |
| `convol_channels` | 对多通道图像逐通道卷积(convol_channels)。image=(H,W,C) 或 2D。 |
| `convol_fft` | 基于 FFT 的线性卷积(convol_fft/convol_image)。 |
| `convol_image` | 空间卷积(convol_image)。 |
| `correlation_fft` | 基于 FFT 的互相关(correlation_fft)。 |
| `create_color_trans_lut` | 创建颜色变换 LUT(变换类型)(create_color_trans_lut)。 |
| `crop_domain` | 用 domain 的外接矩形裁剪图像(crop_domain)。 |
| `derivate_vector_field` | 计算向量场的散度/旋度/雅可比(derivate_vector_field)。 |
| `deviation_n` | 图像堆栈的逐像素标准差(deviation_n)。 |
| `div_image` | image1/image2*mult+add(div_image)。0 除法有保护。 |
| `energy_gabor` | 由 Gabor 实/虚响应计算能量(幅值平方)(energy_gabor)。 |
| `exhaustive_match` | 全搜索 NCC 的最佳匹配(与 find_ncc_model 同核,也返回 error=1-score)。 |
| `exhaustive_match_mg` | 多重网格全搜索模板匹配(粗到细加速)(exhaustive_match_mg)。 |
| `gauss_distribution` | 正态分布的概率密度表(gauss_distribution)。用于噪声模型。 |
| `gen_canonical_variates_trans` | 由带类别的多通道图像求正准变量(LDA)变换(gen_canonical_variates_trans)。 |
| `gen_filter_mask` | 生成任意系数的滤波掩膜(gen_filter_mask)。 |
| `gen_gauss_filter` | 归一化 2D 高斯滤波掩膜(gen_gauss_filter)。 |
| `gen_mean_filter` | 均值(box)滤波掩膜(gen_mean_filter)。 |
| `gen_principal_comp_trans` | 由多通道图像组求主成分变换(特征向量/特征值)(gen_principal_comp_trans)。 |
| `gen_psf_defocus` | 圆形模糊(散焦)PSF(gen_psf_defocus)。 |
| `gen_psf_motion` | 直线模糊(运动)PSF(gen_psf_motion)。 |
| `gen_savitzky_golay_filter` | Savitzky-Golay 平滑/微分 1D 滤波系数(gen_savitzky_golay_filter)。 |
| `gen_sin_bandpass` | 正弦窗的频率带通掩膜(gen_sin_bandpass)。 |
| `gen_std_bandpass` | Butterworth 型带通掩膜(gen_std_bandpass)。 |
| `harmonic_interpolation` | 用 Laplace 方程(调和函数)填补孔洞(region=True)(harmonic_interpolation)。 |
| `inpainting_aniso` | 用各向异性扩散(Perona-Malik)修复缺损区域(inpainting_aniso)。 |
| `inpainting_ced` | 相干增强扩散(沿结构张量方向扩散)修补(inpainting_ced)。 |
| `inpainting_ct` | 接近相干输运的各向同性扩散修补(inpainting_ct)。 |
| `inpainting_mcf` | 平均曲率流(Mean Curvature Flow)修补(inpainting_mcf)。 |
| `inpainting_texture` | 纹理合成修补(复制邻域已知 patch)(inpainting_texture)。 |
| `map_image` | 把 LUT (map) 应用到像素(map_image)。map 为长度 N 的 1D 数组。 |
| `max_image` | 逐像素最大值(max_image)。 |
| `mean_n` | 图像堆栈的逐像素平均(mean_n)。 |
| `midrange_image` | 局部 (min+max)/2 的 midrange 滤波(midrange_image)。 |
| `min_image` | 逐像素最小值(min_image)。 |
| `mult_image` | image1*image2*mult+add(mult_image)。 |
| `noise_distribution_mean` | 由多次观测估计逐像素噪声标准差的平均(noise_distribution_mean)。 |
| `optical_flow_mg` | 多重网格(粗到细金字塔 + warping)Horn-Schunck 稠密光流 |
| `phase_correlation_fft` | 用相位相关估计平移 (drow, dcol)(phase_correlation_fft)。 |
| `points_sojka` | 基于 Sojka 梯度协方差的角点响应提取亚像素角点 |
| `rank_n` | 图像堆栈的逐像素 rank 值(顺序统计、rank_n)。默认取中位数。 |
| `scene_flow_calib` | 已标定的场景流(用内参矩阵把 3D 位移度量化)(scene_flow_calib)。 |
| `scene_flow_uncalib` | 由左右 2 个时刻的图像估计 3D 场景流(未标定近似)(scene_flow_uncalib)。 |
| `sp_distribution` | salt-and-pepper 噪声分布(两端有质量、中央均匀)(sp_distribution)。 |
| `sub_image` | (image1-image2)*mult+add(sub_image)。 |
| `unwarp_image_vector_field` | 沿向量场扭曲图像(逆映射)(unwarp_image_vector_field)。 |
| `vector_field_length` | 向量场各点的幅值(vector_field_length)。 |
| `wiener_filter` | Wiener 反卷积(wiener_filter)。 |
| `wiener_filter_ni` | 非迭代 Wiener 复原(wiener_filter_ni)。 |

#### edges(56 op)

边缘(轮廓)检测。从 Sobel 系的梯度到 Canny 的细线化。测量的基准线大多诞生于此。

![edges 的示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_04_canny.png)
*图: Canny 边缘检测的示例(11.1.1 节再次引用)*

| op | 说明 |
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

把图像切分成有意义区域的分割。从阈值系到分水岭(watershed)。

![segmentation 的示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_14_watersheds.png)
*图: 分水岭法的示例(11.1.1 节再次引用)*

| op | 说明 |
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

平滑专门户的一群。高斯、双边、各向异性扩散等,"消噪声但守边缘"这一系的用法取舍是关键。


![fops_smoothing](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_smoothing.png)
*图: smoothing 的实处理示例 — 对同一噪声输入,高斯平滑会连轮廓一起糊掉,而 anisotropic_diffusion(各向异性扩散)不跨越边缘扩散,因此在保住轮廓的同时只抹平噪声(Fullseye 实输出)。输入为 skimage camera + AI 生成图像(Gemini)2 种。*

| op | 说明 |
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
