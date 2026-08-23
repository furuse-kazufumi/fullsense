#### Matrix(46 op)

矩阵运算、线性方程组、矩阵分解(SVD 等)。相机标定与姿态估计背后的数学幕后功臣。

| op | 说明 |
|---|---|
| `abs_matrix` | 计算矩阵各元素的绝对值。 |
| `abs_matrix_mod` | 逐元素绝对值(结果覆写到输入矩阵)。 |
| `add_matrix` | 两个矩阵相加。 |
| `add_matrix_mod` | 矩阵加法(结果覆写到输入矩阵)。 |
| `create_matrix` | 生成新矩阵。 |
| `decompose_matrix` | 返回 LU 分解(P,L,U)(decompose_matrix)。 |
| `determinant_matrix` | 计算行列式。 |
| `div_element_matrix` | 矩阵之间逐元素相除。 |
| `div_element_matrix_mod` | 逐元素除法(结果覆写到输入矩阵)。 |
| `eigenvalues_general_matrix` | 计算一般矩阵的特征值(需要时也计算特征向量)。 |
| `eigenvalues_symmetric_matrix` | 计算对称矩阵的特征值(需要时也计算特征向量)。 |
| `generalized_eigenvalues_general_matrix` | 计算一般矩阵对的广义特征值(需要时也计算特征向量)。 |
| `generalized_eigenvalues_symmetric_matrix` | 计算对称矩阵对的广义特征值(需要时也计算特征向量)。 |
| `get_diagonal_matrix` | 取出矩阵的对角元素。 |
| `get_sub_matrix` | 取出子矩阵。 |
| `invert_matrix` | 计算逆矩阵。 |
| `invert_matrix_mod` | 逆矩阵(结果覆写到输入矩阵)。 |
| `max_matrix` | 返回矩阵元素的最大值。 |
| `mean_matrix` | 返回矩阵元素的平均值。 |
| `min_matrix` | 返回矩阵元素的最小值。 |
| `mult_element_matrix` | 矩阵之间逐元素相乘。 |
| `mult_element_matrix_mod` | 逐元素乘法(结果覆写到输入矩阵)。 |
| `mult_matrix` | 计算两个矩阵的乘积。 |
| `mult_matrix_mod` | 矩阵乘法(结果覆写到输入矩阵)。 |
| `norm_matrix` | 计算矩阵的范数。 |
| `orthogonal_decompose_matrix` | 返回 QR 正交分解(orthogonal_decompose_matrix)。 |
| `pow_element_matrix` | 对矩阵各元素求幂。 |
| `pow_element_matrix_mod` | 逐元素求幂(结果覆写到输入矩阵)。 |
| `pow_matrix` | 计算矩阵本身的幂。 |
| `pow_matrix_mod` | 矩阵幂(结果覆写到输入矩阵)。 |
| `pow_scalar_element_matrix` | 以标量为底、各元素为指数,逐元素计算幂。 |
| `pow_scalar_element_matrix_mod` | 标量为底的逐元素幂(结果覆写到输入矩阵)。 |
| `repeat_matrix` | 将矩阵平铺重复排列。 |
| `scale_matrix` | 矩阵乘以标量。 |
| `scale_matrix_mod` | 标量倍乘(结果覆写到输入矩阵)。 |
| `set_diagonal_matrix` | 设置矩阵的对角元素。 |
| `set_sub_matrix` | 写入子矩阵。 |
| `solve_matrix` | 求解线性方程组。 |
| `sqrt_matrix` | 计算矩阵各元素的平方根。 |
| `sqrt_matrix_mod` | 逐元素平方根(结果覆写到输入矩阵)。 |
| `sub_matrix` | 两个矩阵相减。 |
| `sub_matrix_mod` | 矩阵减法(结果覆写到输入矩阵)。 |
| `sum_matrix` | 返回矩阵元素的总和。 |
| `svd_matrix` | 计算奇异值分解(SVD)。 |
| `transpose_matrix` | 矩阵转置。 |
| `transpose_matrix_mod` | 转置(结果覆写到输入矩阵)。 |

#### 3D Reconstruction(43 op)

基于深度、视差、多视点的 3D 重建。是从 2.5D(深度图)迈向点云与网格世界的桥梁。

![3D Reconstruction 示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_16_depth_to_points.png)
*图: 深度 → 点云的示例(转自 11.1.1 节)*

| op | 说明 |
|---|---|
| `apply_sheet_of_light_calibration` | 将轮廓(像素行)换算为高度(度量单位)(apply_sheet_of_light_calibration)。 |
| `binocular_disparity` | 基于 Semi-Global Matching 的立体视差估计(Hirschmüller 法)。 |
| `binocular_disparity_mg` | 基于赢者通吃块匹配的稠密视差估计。 |
| `binocular_disparity_ms` | SGM 视差估计的另一入口(实现为 Hirschmüller 法)。 |
| `binocular_distance` | 由视差计算度量深度 Z = f·B/d。 |
| `binocular_distance_mg` | 视差→度量深度 Z = f·B/d(mg 入口)。 |
| `binocular_distance_ms` | 视差→度量深度 Z = f·B/d(ms 入口)。 |
| `calibrate_sheet_of_light` | 用已知台阶标定片光的像素→高度比例(calibrate_sheet_of_light)。 |
| `create_sheet_of_light_calib_object` | 片光标定对象(已知台阶)(create_sheet_of_light_calib_object)。 |
| `create_sheet_of_light_model` | 片光(激光线)轮廓测量模型(create_sheet_of_light_model)。 |
| `create_stereo_model` | 立体测量模型(左右内参 + 相对姿态)(create_stereo_model)。 |
| `create_structured_light_model` | 结构光测量模型(相移图案设置)(create_structured_light_model)。 |
| `decode_structured_light_pattern` | 从相移结构光图像序列解码绝对相位(=对应关系)(decode_structured_light_pattern)。 |
| `depth_from_focus` | 从焦点堆栈按像素估计最佳合焦位置=深度(depth_from_focus)。 |
| `disparity_to_distance` | 将视差 d 转换为距离 Z = f*baseline/d(disparity_to_distance)。 |
| `disparity_to_point_3d` | 由图像点 (row,col) 与视差 disparity 计算 3D 点 (X,Y,Z)(disparity_to_point_3d)。 |
| `distance_to_disparity` | 将距离 Z 转换为视差 d = f*baseline/Z(distance_to_disparity)。 |
| `essential_to_fundamental_matrix` | 由本质矩阵 E 计算基础矩阵 F = K2^-T E K1^-1(essential_to_fundamental_matrix)。 |
| `gen_binocular_proj_rectification` | 由基础矩阵估计用于立体校正(极线对齐)的变换 |
| `gen_binocular_rectification_map` | 计算已标定立体像对的校正旋转(Fusiello 法)。 |
| `gen_structured_light_pattern` | 生成正弦结构光图案图像(gen_structured_light_pattern)。 |
| `intersect_lines_of_sight` | 用线性 DLT 三角测量对两视点对应像素做 3D 重建。 |
| `match_essential_matrix_ransac` | 由点对应与内参矩阵 K 用 RANSAC 估计本质矩阵 E(match_essential_matrix_ransac)。 |
| `match_fundamental_matrix_distortion_ransac` | 含畸变基础矩阵的 RANSAC 估计(match_fundamental_matrix_distortion_ransac)。 |
| `match_fundamental_matrix_ransac` | 由点对应用 RANSAC 估计基础矩阵 F 与内点(match_fundamental_matrix_ransac)。 |
| `match_rel_pose_ransac` | 由点对应做相对姿态的 RANSAC 估计(match_rel_pose_ransac)。 |
| `measure_profile_sheet_of_light` | 在每列提取激光线(最大亮度)的行位置=高度轮廓 |
| `photometric_stereo` | 从多光照图像(Lambertian)恢复法线与反射率(photometric_stereo)。 |
| `reconst3d_from_fundamental_matrix` | 经基础矩阵分解相对姿态并对对应点做三角测量(reconst3d_from_fundamental_matrix)。 |
| `reconstruct_height_field_from_gradient` | 用 Frankot-Chellappa 积分梯度场 (dz/dr, dz/dc) 恢复高度场 z |
| `reconstruct_points_stereo` | 由左右对应点(行对齐)经视差恢复 3D 点云(reconstruct_points_stereo)。 |
| `reconstruct_surface_stereo` | 由整张视差图恢复 3D 点云(表面)(reconstruct_surface_stereo)。 |
| `reconstruct_surface_structured_light` | 结构光相位解码 → 视差 → 3D 表面重建(reconstruct_surface_structured_light)。 |
| `rel_pose_to_fundamental_matrix` | 由相对姿态 (R,t) 与内参矩阵计算基础矩阵 F(rel_pose_to_fundamental_matrix)。 |
| `select_grayvalues_from_channels` | 按 index 图像从多通道堆栈中逐像素选取灰度值 |
| `sfs_mod_lr` | Shape-from-Shading(改良 linear,sfs_mod_lr)。共用 Pentland 实现。 |
| `sfs_orig_lr` | Shape-from-Shading(原始 linear,sfs_orig_lr)。共用 Pentland 实现。 |
| `sfs_pentland` | 用 Pentland 的线性化 Shape-from-Shading 恢复高度场(sfs_pentland)。 |
| `uncalibrated_photometric_stereo` | 光源方向未知的 photometric stereo(用 SVD 做秩 3 近似,uncalibrated_photometric_stereo)。 |
| `vector_to_essential_matrix` | 由已标定像对的 8 组以上对应估计本质矩阵 E。 |
| `vector_to_fundamental_matrix` | 由 8 组以上对应用归一化 8 点法估计基础矩阵 F。 |
| `vector_to_fundamental_matrix_distortion` | 含畸变的基础矩阵 RANSAC 估计(假定畸变较小,归一化 8-point) |
| `vector_to_rel_pose` | 由点对应与内参矩阵估计相对姿态 (R,t)(本质矩阵分解)(vector_to_rel_pose)。 |

#### 3D Object Model(40 op)

点云、网格(3D 对象模型)的操作。变换、法线、简化、特征量等。

| op | 说明 |
|---|---|
| `affine_trans_object_model_3d` | 对全部点应用刚体变换 R·p + t。 |
| `area_object_model_3d` | 返回 3D 点云的凸包表面积(area_object_model_3d)。 |
| `connection_object_model_3d` | 用欧氏聚类对邻近点分组(Rusu 2009)。 |
| `convex_hull_object_model_3d` | 返回 3D 凸包的顶点(convex_hull_object_model_3d)。 |
| `distance_object_model_3d` | 两个 3D 模型之间的最小点间距离(distance_object_model_3d)。 |
| `edges_object_model_3d` | 提取局部曲率高的点=3D 边缘(edges_object_model_3d)。以近邻 PCA 的平面性判定。 |
| `fit_primitives_object_model_3d` | 用 RANSAC 稳健拟合主导平面。 |
| `fuse_object_model_3d` | 将多个 3D 模型融合为一个(fuse_object_model_3d)。 |
| `gen_box_object_model_3d` | 长方体 6 个面的点云(gen_box_object_model_3d)。 |
| `gen_cylinder_object_model_3d` | 圆柱侧面的点云(gen_cylinder_object_model_3d)。 |
| `gen_empty_object_model_3d` | 空的 3D 模型(gen_empty_object_model_3d)。 |
| `gen_object_model_3d_from_points` | 由 x,y,z 数组创建 3D 点云模型(gen_object_model_3d_from_points)。 |
| `gen_plane_object_model_3d` | z=0 平面上的网格点云(gen_plane_object_model_3d)。 |
| `gen_sphere_object_model_3d` | 球面上的准均匀点云(黄金螺旋,gen_sphere_object_model_3d)。 |
| `gen_sphere_object_model_3d_center` | 指定中心的球面点云(gen_sphere_object_model_3d_center)。 |
| `intersect_plane_object_model_3d` | 返回平面(a,b,c,d)附近(距离<tol)的点=截面(intersect_plane_object_model_3d)。 |
| `max_diameter_object_model_3d` | 点云的最大跨距直径(凸包上最远 2 点,max_diameter_object_model_3d)。 |
| `moments_object_model_3d` | 返回 3D 点云的重心与协方差(2 阶中心矩)(moments_object_model_3d)。 |
| `object_model_3d_to_xyz` | 将 3D 点云转为 X/Y/Z 图像(网格序,object_model_3d_to_xyz)。 |
| `prepare_object_model_3d` | 带法线估计的模型预处理(近邻 PCA,prepare_object_model_3d)。 |
| `project_object_model_3d` | 将世界点云 (N,3) 投影到像素并返回 (uv, depth)。 |
| `projective_trans_object_model_3d` | 应用 4x4 射影变换(projective_trans_object_model_3d)。默认为恒等。 |
| `reduce_object_model_3d_by_view` | 沿指定轴只保留靠前 keep 比例的点(按视点的简易抽稀,reduce_object_model_3d_by_view)。 |
| `register_object_model_3d_global` | point-to-plane ICP: 最小化法线方向距离,将 src 配准到 dst。 |
| `register_object_model_3d_pair` | ICP(迭代最近点法): 在对应关系未知的情况下将 src 配准到 dst。 |
| `render_object_model_3d` | 将 3D 模型渲染为图像(按深度明暗,render_object_model_3d)。 |
| `rigid_trans_object_model_3d` | 对点云应用 4x4 刚体/相似变换(rigid_trans_object_model_3d)。 |
| `sample_object_model_3d` | 按占用体素抽稀为每体素 1 点(单元重心)的降采样。 |
| `segment_object_model_3d` | 按近邻距离将点云分割为连通分量(segment_object_model_3d)。返回标签数组。 |
| `select_object_model_3d` | 按属性值域选择点(select_object_model_3d)。 |
| `select_points_object_model_3d` | 按指定轴的值域选点(select_points_object_model_3d)。 |
| `simplify_object_model_3d` | 用体素网格平均简化点云(simplify_object_model_3d)。 |
| `smallest_bounding_box_object_model_3d` | 用 PCA 求有向包围盒。 |
| `smallest_sphere_object_model_3d` | 最小包围球的近似(中心=重心,半径=最远点,smallest_sphere_object_model_3d)。 |
| `smooth_object_model_3d` | 将各点移向 k 近邻重心以平滑(smooth_object_model_3d)。 |
| `surface_normals_object_model_3d` | 用 k 近邻的局部 PCA 逐点估计法线。 |
| `triangulate_object_model_3d` | 投影到主平面后做 Delaunay 三角剖分(triangulate_object_model_3d)。返回三角形顶点 index。 |
| `union_object_model_3d` | 合并两个 3D 模型(union_object_model_3d)。 |
| `volume_object_model_3d_relative_to_plane` | 用凸包近似平面 (a,b,c,d) 之上的点云体积(volume_object_model_3d_relative_to_plane)。 |
| `xyz_to_object_model_3d` | 由 X/Y/Z 图像(各为 2D)生成 3D 点云模型(xyz_to_object_model_3d)。 |

#### gray(40 op)

灰度形态学等,在保持灰度图像的前提下进行的形态学处理。


![fops_gray](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_gray.png)
*图: gray 的实际处理示例 — 对光照不均、低对比度的输入,全局直方图均衡化容易失效(亮部过曝、噪声放大),而 clahe(对比度受限的局部自适应均衡化)能逐局部恢复灰度层次(Fullseye 实际输出)。输入为 AI 生成(Gemini)2 种+skimage 自带 moon。*

| op | 说明 |
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

模板匹配、形状匹配。负责"把教过的形状在任何地方找出来",堪称工业图像处理的招牌。

| op | 说明 |
|---|---|
| `adapt_shape_model_high_noise` | 生成面向高噪声、加强平滑的形状模型(adapt_shape_model_high_noise)。 |
| `create_aniso_shape_model` | 各向异性缩放形状模型(create_aniso_shape_model,模型本身相同,find 时做各向异性 scale 搜索)。 |
| `create_aniso_shape_model_xld` | 由 XLD 轮廓创建各向异性缩放形状模型(create_aniso_shape_model_xld)。 |
| `create_calib_descriptor_model` | 已标定 descriptor 模型(create_calib_descriptor_model)。 |
| `create_generic_shape_model` | 通用形状模型(create_generic_shape_model,与 create_shape_model 同核)。 |
| `create_local_deformable_model` | 局部变形匹配用模型(保留模板)(create_local_deformable_model)。 |
| `create_local_deformable_model_xld` | 源自 XLD 的局部变形模型(create_local_deformable_model_xld)。 |
| `create_ncc_model` | 准备 NCC 模型(=归一化模板)(create_ncc_model)。 |
| `create_planar_calib_deformable_model` | 平面(已标定)变形模型(create_planar_calib_deformable_model)。 |
| `create_planar_calib_deformable_model_xld` | 源自 XLD 的平面已标定变形模型(create_planar_calib_deformable_model_xld)。 |
| `create_planar_uncalib_deformable_model` | 平面(未标定)变形模型(create_planar_uncalib_deformable_model)。 |
| `create_planar_uncalib_deformable_model_xld` | 源自 XLD 的平面未标定变形模型(create_planar_uncalib_deformable_model_xld)。 |
| `create_scaled_shape_model` | 各向同性缩放形状模型(create_scaled_shape_model)。 |
| `create_scaled_shape_model_xld` | 由 XLD 轮廓创建支持缩放的形状模型(create_scaled_shape_model_xld)。 |
| `create_shape_model` | 将模板边缘点(/grad/>min_grad)的归一化梯度向量建为模型(create_shape_model)。 |
| `create_shape_model_xld` | 由 XLD 轮廓创建形状模型(create_shape_model_xld)。 |
| `create_uncalib_descriptor_model` | 未标定 descriptor 模型(Harris keypoint + 归一化 patch)(create_uncalib_descriptor_model)。 |
| `determine_deformable_model_params` | 决定变形模型的推荐参数(determine_deformable_model_params)。 |
| `determine_ncc_model_params` | 决定 NCC 模型的推荐参数(对比度/层级数)(determine_ncc_model_params)。 |
| `determine_shape_model_params` | 由模板自动决定推荐 min_grad/对比度(determine_shape_model_params)。 |
| `find_aniso_shape_model` | 行/列独立缩放(各向异性)的形状模型检测(find_aniso_shape_model)。 |
| `find_aniso_shape_models` | 各向异性缩放下的多实例检测(find_aniso_shape_models)。 |
| `find_calib_descriptor_model` | 已标定 descriptor 模型的检测 → 平面姿态(find_calib_descriptor_model)。 |
| `find_generic_shape_model` | 通用形状模型检测(find_generic_shape_model)。find_shape_model 的别名。 |
| `find_local_deformable_model` | 先粗配刚体位置,再用光流估计局部变形 |
| `find_ncc_model` | 在图像中搜索 NCC 模型并返回最佳匹配(行/列/得分)(find_ncc_model)。 |
| `find_ncc_models` | NCC 模型的多实例检测(find_ncc_models)。 |
| `find_planar_calib_deformable_model` | 平面已标定变形模型的检测(find_planar_calib_deformable_model)。 |
| `find_planar_uncalib_deformable_model` | 平面未标定变形模型的检测(find_planar_uncalib_deformable_model)。 |
| `find_scaled_shape_model` | 在改变缩放的同时搜索最佳匹配(find_scaled_shape_model)。 |
| `find_scaled_shape_models` | 带缩放搜索的多实例检测(find_scaled_shape_models)。 |
| `find_shape_models` | 带非极大值抑制的多实例检测(find_shape_models)。 |
| `find_uncalib_descriptor_model` | 从图像中检测 descriptor 模型(比率检验 + RANSAC 单应) |
| `get_shape_model_contours` | 将形状模型的边缘点作为轮廓返回(get_shape_model_contours)。 |
| `get_shape_model_origin` | 返回形状模型的原点(重心)(get_shape_model_origin)。 |
| `inspect_shape_model` | 返回形状模型的边缘点数、展布、原点以供检视(inspect_shape_model)。 |
| `set_shape_model_origin` | 设置形状模型的参考原点(set_shape_model_origin)。 |

#### XLD(35 op)

XLD = 亚像素精度的轮廓表示。以比像素更细的精度处理轮廓,是精密测量的关键。


![fops_xld](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_xld.png)
*图: XLD 的实际处理示例 — 二值化得到的边界只能是像素网格的阶梯状,而 threshold_sub_pix 以比像素更细的(亚像素)精度估计电平交叉位置,返回轮廓(XLD)。在带真值的合成圆上实测平均误差 0.001px。放大 8 倍可以看出阶梯与平滑轮廓线的差别(Fullseye 实际输出)。输入为自制合成、AI 生成(Gemini)、skimage coins。*

| op | 说明 |
|---|---|
| `difference_closed_contours_xld` | 两个闭轮廓的差(difference_closed_contours_xld)。 |
| `difference_closed_polygons_xld` | 两个闭多边形的差(difference_closed_polygons_xld)。 |
| `gen_circle_contour_xld` | 生成圆弧轮廓(gen_circle_contour_xld)。 |
| `gen_contour_nurbs_xld` | 由控制点生成 NURBS(B 样条)轮廓(gen_contour_nurbs_xld)。 |
| `gen_contour_polygon_rounded_xld` | 生成圆角多边形轮廓(gen_contour_polygon_rounded_xld)。 |
| `gen_contour_polygon_xld` | 由点列生成多边形轮廓(gen_contour_polygon_xld)。 |
| `gen_contours_skeleton_xld` | 提取区域骨架并转换为轮廓(按分支)(gen_contours_skeleton_xld)。 |
| `gen_cross_contour_xld` | 生成十字标记轮廓(gen_cross_contour_xld)。 |
| `gen_ellipse_contour_xld` | 生成椭圆弧轮廓(gen_ellipse_contour_xld)。 |
| `gen_nurbs_interp` | 过点的 NURBS 插值轮廓(gen_nurbs_interp)。 |
| `gen_parallels_xld` | 为每条轮廓生成平行的偏移轮廓(gen_parallels_xld)。 |
| `gen_rectangle2_contour_xld` | 生成旋转矩形的轮廓(gen_rectangle2_contour_xld)。 |
| `get_contour_angle_xld` | 逐点返回沿轮廓的切线角(弧度)(get_contour_angle_xld)。 |
| `get_polygon_xld` | 用 Douglas-Peucker 对轮廓做多边形近似(get_polygon_xld)。返回顶点列。 |
| `get_regress_params_xld` | 对轮廓点的回归直线参数(法线角 nr,nc 与原点距离 dist)(get_regress_params_xld)。 |
| `intersection_closed_contours_xld` | 两个闭轮廓的交(intersection_closed_contours_xld)。 |
| `intersection_closed_polygons_xld` | 两个闭多边形的交(intersection_closed_polygons_xld)。 |
| `intersection_region_contour_xld` | 区域与闭轮廓的相交区域(intersection_region_contour_xld)。 |
| `local_max_contours_xld` | 提取轮廓上灰度值局部最大的点(local_max_contours_xld)。 |
| `max_parallels_xld` | 至最大距离为止的平行轮廓组(max_parallels_xld)。 |
| `merge_cont_line_scan_xld` | 连接线扫描(条带采集)相邻帧的轮廓端点(merge_cont_line_scan_xld)。 |
| `mod_parallels_xld` | 生成平行轮廓(参数修改版)(mod_parallels_xld)。 |
| `moments_any_points_xld` | 轮廓点集的面积、重心、2 阶矩(moments_any_points_xld)。 |
| `segment_contour_attrib_xld` | 在下方灰度属性突变的点处分割轮廓(segment_contour_attrib_xld)。 |
| `segment_contours_xld` | 将轮廓分割为直线段(segment_contours_xld)。 |
| `symm_difference_closed_contours_xld` | 两个闭轮廓的对称差(symm_difference_closed_contours_xld)。 |
| `symm_difference_closed_polygons_xld` | 两个闭多边形的对称差(symm_difference_closed_polygons_xld)。 |
| `test_xld_point` | 判断点是否在闭轮廓内部(交叉数法)(test_xld_point)。 |
| `union2_closed_contours_xld` | 两个闭轮廓的并(union2_closed_contours_xld)。 |
| `union2_closed_polygons_xld` | 两个闭多边形的并(union2_closed_polygons_xld)。 |
| `union_cocircular_contours_xld` | 合并共圆(同一圆上)的轮廓(union_cocircular_contours_xld)。 |
| `union_collinear_contours_ext_xld` | 共线合并(扩展参数版)(union_collinear_contours_ext_xld)。 |
| `union_collinear_contours_xld` | 合并共线的轮廓片段(union_collinear_contours_xld)。 |
| `union_cotangential_contours_xld` | 合并切线连续的轮廓(union_cotangential_contours_xld)。 |
| `union_straight_contours_xld` | 合并近似直线的轮廓(union_straight_contours_xld)。 |

#### Calibration(34 op)

相机标定(内参、外参、镜头畸变)。是"把像素翻译成 mm"的地基(正文 14.4 的 Brown 畸变模型也在这里)。

![Calibration 示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_12_radial_distortion.png)
*图: 镜头畸变模型的示例(桶形/枕形)(转自 11.1.1 节)*

| op | 说明 |
|---|---|
| `affine_trans_point_3d` | 对 3D 点应用 4x4 齐次仿射变换(affine_trans_point_3d)。 |
| `binocular_calibration` | 用 Zhang 法分别标定左右相机并估计立体相对姿态(binocular_calibration)。 |
| `calibrate_cameras` | Zhang 法相机标定(calibrate_cameras)。camera_calibration 的别名。 |
| `calibrate_hand_eye` | 手眼标定(calibrate_hand_eye)。hand_eye_calibration 的别名。 |
| `caltab_points` | 返回标定板的理想标记坐标(世界坐标, mm)(caltab_points)。 |
| `cam_mat_to_cam_par` | 从内参矩阵 K 取出 fx, fy, cx, cy, skew。 |
| `cam_par_pose_to_hom_mat3d` | 将相机位姿 [rx,ry,rz(rad), tx,ty,tz] 转换为 4x4 齐次变换矩阵(cam_par_pose_to_hom_mat3d)。 |
| `cam_par_to_cam_mat` | 由 fx, fy, cx, cy, skew 组装针孔内参矩阵 K。 |
| `camera_calibration` | 用 Zhang 法从平面靶标多视点估计内参矩阵 K(camera_calibration)。 |
| `change_radial_distortion_cam_par` | 将相机参数的径向畸变系数替换为 kappa_new(change_radial_distortion_cam_par)。 |
| `change_radial_distortion_image` | 对图像施加径向畸变 r' = r(1 + kappa r^2) 并重采样(change_radial_distortion_image)。 |
| `change_radial_distortion_points` | 给理想像素施加径向、切向镜头畸变(Brown 模型)。 |
| `contour_to_world_plane_xld` | 将 XLD 轮廓(dict {cs:[Nx2]})映射到 world 平面(contour_to_world_plane_xld)。 |
| `create_caltab` | 创建标定板的描述(理想点)(create_caltab)。 |
| `create_pose` | 生成 3D pose。 |
| `disp_caltab` | 返回标定板图像(用于显示)(disp_caltab)。 |
| `find_calib_object` | 检测标定对象(标记)(find_calib_object)。find_caltab 的别名。 |
| `find_caltab` | 从图像中检测标定板圆形标记中心(连通分量的重心)(find_caltab)。 |
| `find_marks_and_pose` | 标记检测 + 标定板姿态估计(PnP 近似=平面单应)(find_marks_and_pose)。 |
| `gen_caltab` | 生成圆形标记网格的标定板图像(gen_caltab)。 |
| `gen_image_to_world_plane_map` | 生成图像→世界平面(z=0)的映射表(gen_image_to_world_plane_map)。 |
| `gen_radial_distortion_map` | 生成径向畸变的逆映射(row_map, col_map)(gen_radial_distortion_map)。 |
| `get_line_of_sight` | 返回像素 (row,col) 的视线方向(归一化 3D 向量)(get_line_of_sight)。 |
| `hand_eye_calibration` | 由一系列运动对求解 AX=XB 估计 X(4x4)(hand_eye_calibration)。 |
| `image_points_to_world_plane` | 由相机内/外参将像素反投影到 world 平面 z=0(image_points_to_world_plane)。 |
| `image_to_world_plane` | 用平面单应将图像点映射到 world 平面(z=0)(image_to_world_plane)。 |
| `project_3d_point` | 将 3D 点透视投影到相机并返回像素 (row, col)(project_3d_point)。 |
| `project_hom_point_hom_mat3d` | 用 3x4/4x4 矩阵投影齐次 3D 点 (4,)(project_hom_point_hom_mat3d)。 |
| `project_point_hom_mat3d` | 用 4x4 或 3x4 齐次变换对 3D 点变换并投影(project_point_hom_mat3d)。 |
| `projective_trans_point_2d` | 用射影变换矩阵对齐次 2D 点做射影。 |
| `radial_distortion_self_calibration` | 最小化本应为直线的点列的残差以估计径向畸变 kappa(plumb-line 法) |
| `radiometric_self_calibration` | 由不同曝光的图像组估计相机响应函数(逆响应 LUT) |
| `sim_caltab` | 模拟以指定相机姿态投影标定板得到的图像(sim_caltab)。 |
| `stationary_camera_self_calibration` | 由纯旋转的无穷远单应 H = K R K^-1 估计内参矩阵 K |

#### morphology(33 op)

二值形态学(膨胀、腐蚀、开运算、闭运算)。去噪与形状整形的经典,至今仍是现役。

![morphology 示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_06_opening_circle.png)
*图: 开运算的示例(转自 11.1.1 节)*

| op | 说明 |
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

点、线、圆等几何基元的拟合与计算。把测量结果转换为"图形的语言"的 op 群。


![fops_geometry](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_geometry.png)
*图: geometry 的实际处理示例 — 圆周上的结构(黑洞的环状亮度、齿轮的齿、年轮)用直线类工具测不了,但用 polar_trans_image 展开到极坐标后就变成横向一排,1D 轮廓或直线检查可以直接套用(Fullseye 实际输出)。输入为 EHT Collaboration 的 M87*(CC BY 4.0)+AI 生成图像(Gemini)2 种。*

| op | 说明 |
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

3D Gaussian Splatting 相关。基于多视点图像的 3D 重建、渲染、网格化,是这套工具箱的最前沿。

| op | 说明 |
|---|---|
| `animate_mesh` | 按 qpos 轨迹动画播放真值网格(也可合成静态地形网格) |
| `bin_pick_gif` | 对散乱堆放的零件做候选打分、6DoF IK 从上方抓取并取出 bin 的 bin-picking,headless 生成 GIF(无需 GPU,成功数按零件是否离开 bin 实测) |
| `capture_orbit` | 对 sim 场景做环绕拍摄并生成 3DGS 数据集(transforms.json) |
| `event_camera` | 用对数亮度变化模型模拟事件相机(DVS),生成 ON/OFF 事件流。实测确认对运动边缘发放(无需 GPU) |
| `evis_perceive` | 用 Fullseye 感知 GPU 训练 evis 的 rollout(qpos npy): RGB/深度/DVS 的 3 面 GIF(ego_body= 时为机器人视角=头部搭载 RGB/深度/DVS 的 4 面) |
| `figure8` | 用差速转向按各尺寸画 8 字形曲线的转向控制练习/校准(俯瞰轨迹,无需 GPU) |
| `focus_stack` | 由真值深度生成景深虚化的焦点堆栈,并以局部锐度最大做全焦点合成(同时恢复来自焦点的深度,无需 GPU) |
| `g1_perceive_real` | 按 G1 实机传感器规格感知: Livox Mid-360(头顶 360°/-7..+52°)BEV 点云 + RealSense D435i(87°×58°, 0.3-6m 范围)RGB/深度的 4 面 GIF。obstacles=True 时在步行路径外放置验证用静态障碍物(为传感器准备可拍摄对象) |
| `g1_training_curves` | 将 G1 训练日志的进度行(step/reward/ep_len/perr/crash…)解析为数组字典 — 不接触 GPU 机器即可在 Studio 中绘制训练曲线 |
| `g1_walk_policy` | 仅在 Windows 上执行 GPU 训练好的 G1 步行策略(brax ckpt): numpy 推理(已验证与 brax 数值一致)+原生 MuJoCo rollout→实测距离/存活/横向偏移 RMS+跟随相机视频。vision=True 时为带疑似 LiDAR+障碍物的视觉步行版 |
| `hurdle_physics` | go2 助跑→爆发跳跃越过障碍物(栏架)并落到另一侧的真实物理跳远,生成 GIF+轨迹遥测(实测是否越过/是否自立,无需 GPU) |
| `jump_physics` | 让 go2 下蹲→爆发伸展→弹道飞行(实测全脚离地=接触为 0)→落地的真实物理跳跃,生成 GIF+高度遥测(实测跳跃高度/滞空,含摩擦、重力,无需 GPU) |
| `lidar_scan` | 用 mj_ray 的真实光线投射模拟旋转 LIDAR,生成并可视化点云(无需 GPU,命中率等为实测) |
| `long_route` | go2 在粗糙度变化的漫长起伏地形上以真实物理走完长距离(默认 100m)(实测距离/自立,无需 GPU) |
| `pick_gif` | 机械臂(Panda)以真实接触、摩擦抓取立方体并放置到另一位置的 pick-and-place,headless 生成 GIF(无需 GPU,抓取成败按箱体实测高度判定) |
| `polarization` | 用 Fresnel 正向模型(法线→DoLP/AoLP→4 偏振图像→Stokes)模拟偏振相机。即便是无纹理表面,偏振也能编码表面朝向(面向透明/镜面抓取,无需 GPU) |
| `pseudo_lidar` | 平面疑似 LiDAR 扫描(前方弧 K 条的归一化距离)。与步行策略 G1VisionWalk 观测同一几何的 numpy parity — 把策略要吃的输入作为工具单独计算 |
| `render_walk_gif` | 将 walker 放置在 terrain 上的运动学预览 headless 生成 GIF(无接触,可视化 motion/gait。物理步行请用 walk_physics) |
| `route_planning` | go2 用光线投射预判障碍物、以金字塔搜索(粗→细)选择候选方位、差速转向绕行并到达目标的真实物理导航(附俯瞰规划,无需 GPU) |
| `sensor_fusion` | 用 Kalman 滤波融合位置传感器(相机/GPS)与速度传感器(IMU)以跟踪抛射体。生成与各传感器单独使用做诚实比较的融合 RMSE 图(无需 GPU) |
| `stereo_depth` | 渲染平行双相机的立体像对并用块匹配估计深度,与真值深度做误差比较(使用既有 stereo.py,无需 GPU) |
| `sugar_mesh` | 将 3DGS 按 SuGaR 风格做表面对齐→Poisson 网格提取(带真值 bbox 验证) |
| `train_3dgs` | 用 native gsplat 训练 sim 场景的 3DGS(高速) |
| `train_3dgs_densify` | 带 densify + SH + antialiased 的 3DGS 训练(高质量) |
| `tsdf_mesh` | 将 sim 完整深度做 TSDF 融合,生成干净的水密网格(无需 GPU,无针刺) |
| `walk_physics` | 让 go2 以扭矩 PD 控制+闭环平衡+mj_step 的真实物理(重力、摩擦、接触、惯性)行走在粗糙 height field 上,把躯干倾斜的样子生成 GIF+遥测(实测自立/前进/倾斜,无需 GPU) |

#### Regions(26 op)

区域处理的 HALCON 兼容超集(region 类别的扩展版)。


![fops_regions](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_regions.png)
*图: Regions 的实际处理示例 — 现场的二值图像满是颗粒噪声和孔洞,直接做标记会导致误计数。先用 opening_circle(开运算)消除颗粒、fill_up 填补孔洞,再分连通分量,是区域处理的定式(Fullseye 实际输出)。输入为 AI 生成(Gemini)2 种+自带样例 1 种的二值化+人工污损。*

| op | 说明 |
|---|---|
| `difference` | 区域差 region \ sub(difference)。 |
| `find_neighbors` | 返回区域列表的相邻对 index(膨胀后判交)(find_neighbors)。 |
| `gen_random_region` | 生成随机连通区域(边界累积=准确面积 + 连通性保证)(gen_random_region)。 |
| `gen_random_regions` | 生成多个随机区域(gen_random_regions)。 |
| `gen_rectangle1` | 生成轴平行矩形区域(gen_rectangle1)。 |
| `gen_region_histo` | 将 1D 直方图画成条形图区域(gen_region_histo)。 |
| `gen_region_hline` | 生成水平线段的区域(gen_region_hline)。rows: 行 index 的列。 |
| `gen_region_line` | 将线段 region 化(gen_region_line,DDA)。 |
| `gen_region_points` | 将单个像素 region 化(gen_region_points)。 |
| `gen_region_polygon` | 将多边形的轮廓 region 化(gen_region_polygon)。 |
| `gen_region_polygon_filled` | 将多边形填充后 region 化(gen_region_polygon_filled)。 |
| `gen_region_runs` | 由行程编码 [(row, col_start, col_end), ...] 生成 region(gen_region_runs)。 |
| `get_region_points` | 区域像素的 (row, col) 坐标数组(get_region_points)。 |
| `get_region_polygon` | 返回区域外形的多边形近似顶点(get_region_polygon)。 |
| `get_region_runs` | 区域的行程长度表示 [(row, col_start, col_end), ...](get_region_runs)。 |
| `hamming_distance` | 两区域的 Hamming 距离(不同像素数)(hamming_distance)。 |
| `hamming_distance_norm` | 归一化 Hamming 距离(差分像素 / 并集像素)(hamming_distance_norm)。 |
| `intersection` | 区域交(intersection)。 |
| `merge_regions_line_scan` | 连接线扫描的行程集合并合并为区域(merge_regions_line_scan)。 |
| `select_region_spatial` | 选择相对基准区域满足指定空间关系的区域(select_region_spatial)。 |
| `select_shape_proto` | 选择形状特征接近原型区域的区域(select_shape_proto)。 |
| `spatial_relation` | 基于两区域重心方向的空间关系(above/below/left/right)(spatial_relation)。 |
| `symm_difference` | 对称差(symm_difference)。 |
| `test_equal_region` | 判断两区域是否相等(test_equal_region)。 |
| `test_subset_region` | 判断 region1 ⊆ region2(test_subset_region)。 |
| `union2` | 区域并(union2)。 |

#### contour(26 op)

轮廓(contour)的提取、平滑、分割与属性计算。


![fops_contour](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_contour.png)
*图: contour 的实际处理示例 — 细线状结构(血管、翅脉、叶脉、裂纹)用边缘检测会在线的两侧出现双重边缘,而用 lines_gauss(Frangi 脊线响应)取出线状结构的条带,再用 skeleton 细化为 1 像素宽的中心线。血管、翅脉、叶脉、裂纹都能用同一套数学来测(Fullseye 实际输出)。输入全部为 AI 生成图像(Gemini)。医疗风格的输入并非用于诊断用途。*

| op | 说明 |
|---|---|
| `FindContours` | 从二值/电平提取轮廓(cv2.findContours,不可用时 skimage,再没有则 numpy)  [backend=opencv] |
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

秩滤波(中值等)。基于顺序统计的去噪,是椒盐噪声的特效药。

![rank 示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_02_median_image.png)
*图: 中值滤波的示例(转自 11.1.1 节)*

| op | 说明 |
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
