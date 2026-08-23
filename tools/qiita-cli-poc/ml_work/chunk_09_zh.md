#### camera(22 op)

相机模型与投影计算。在 3D 与 2D 之间往返的变换群。

| op | 说明 |
|---|---|
| `SolvePnP` | 由 3D-2D 对应估计相机姿态(cv2.solvePnP,不可用时 numpy)(camera.SolvePnP)。  [backend=opencv] |
| `backproject` | 用深度将像素 (N,2) 提升为相机坐标系的 3D 点(反投影)。 |
| `decompose_essential` | 将本质矩阵 E 分解为 4 种相对 pose 候选。 |
| `decompose_intrinsics` | 从内参矩阵 K 取出 fx, fy, cx, cy, skew。 |
| `depth_to_points` | 将整张深度图反投影为相机坐标系的点云。 |
| `distort_points` | 给理想像素施加径向、切向镜头畸变(Brown 模型)。 |
| `epipolar_lines` | 经基础矩阵计算对应点所诱导的极线。 |
| `essential_from_fundamental` | 以 E = K2^T·F·K 将基础矩阵转换为本质矩阵。 |
| `essential_matrix` | 由已标定像对的 8 组以上对应估计本质矩阵 E。 |
| `fundamental_matrix` | 由 8 组以上对应用归一化 8 点法估计基础矩阵 F。 |
| `intrinsic_matrix` | 组装针孔内参矩阵 K。 |
| `normals_from_depth` | 由对齐好的深度图逐像素估计法线 (H,W,3)。 |
| `project_points` | 将世界点 (N,3) 投影到像素并返回 (uv, depth)。 |
| `projection_matrix` | 组装 3x4 投影矩阵 P = K·[R t](R, t 可省略)。 |
| `recover_pose` | 从本质矩阵的分解候选中选出物理上正确的相对 pose。 |
| `reprojection_error` | 计算逐点的重投影误差 [px]。 |
| `rodrigues` | 旋转向量(轴×角)转旋转矩阵(Rodrigues 公式)。 |
| `rotation_log` | 旋转矩阵转旋转向量(rodrigues 的逆)。 |
| `solve_pnp` | 由 6 组以上 3D↔2D 对应估计 6 自由度 pose(PnP)。 |
| `stereo_rectify` | 计算已标定立体像对的校正旋转(Fusiello 法)。 |
| `triangulate` | 两视点对应像素的线性 DLT 三角测量。 |
| `undistort_points` | 去除径向、切向畸变(distort_points 的逆)。 |

#### texture(21 op)

纹理(质地)分析。Laws 能量、Gabor 等,把"花纹的质感"数值化。

![texture 示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_10_texture_laws.png)
*图: Laws 纹理能量的示例(转自 11.1.1 节)*

| op | 说明 |
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

频域处理(FFT、滤波)。把图像视作波的叠加的视角。

![frequency 示例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_08_fft_image.png)
*图: FFT 频谱的示例(转自 11.1.1 节)*

| op | 说明 |
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

点云分割(平面提取、聚类等)。

| op | 说明 |
|---|---|
| `aabb` | 返回点云的轴平行包围盒 (min, max)。 |
| `centroid` | 返回点云的重心。 |
| `crop_box` | 只保留轴平行盒 [lo, hi] 内的点。 |
| `crop_sphere` | 只保留距中心 radius 以内的点(返回点与掩码)。 |
| `curvature` | 由 k 近邻的特征值计算逐点曲率(表面变化率)。 |
| `euclidean_clusters` | 用欧氏聚类对邻近点分组(Rusu 2009)。 |
| `farthest_point_sampling` | 用最远点采样选出空间上分散的 k 个点。 |
| `fit_cylinder_ransac` | 由点+法线样本用 RANSAC 稳健拟合圆柱。 |
| `fit_plane` | 对全部点的全最小二乘平面拟合(PCA)。 |
| `fit_plane_ransac` | 用 RANSAC 稳健拟合主导平面。 |
| `fit_sphere_ransac` | 用 RANSAC 稳健拟合球(返回中心、半径、内点)。 |
| `height_above_plane` | 各点沿平面法线方向的高度(带符号距离)。 |
| `obb` | 基于 PCA 的有向包围盒。 |
| `plane_distance` | 各点到平面 [a,b,c,d] 的带符号距离。 |
| `principal_axes` | 点云的主成分分析(返回特征值与特征向量)。 |
| `region_growing` | 带平滑度约束的区域生长聚类分割(Rabbani 2006)。 |
| `remove_ground` | 用 RANSAC 拟合主导平面,把点云分为地面/非地面。 |

#### specops(16 op)

疑似传感器、感知系的特殊 op(疑似 LiDAR、一维事件相机、实机传感器复现等,正文第 6 章、第 9 章的主角们)。

| op | 说明 |
|---|---|
| `read_envi` | 读取 ENVI 高光谱立方体(cube, meta)。 |
| `spec_angle_mapper` | 与参考光谱的逐像素光谱角 [rad](SAM)。 |
| `spec_band` | 将立方体的第 i 个波段取出为一张图像。 |
| `spec_band_ratio` | 计算逐像素的波段比 band_i/(band_j+eps)。 |
| `spec_continuum_removal` | 连续统去除(将各光谱除以其上包络线)。 |
| `spec_decorrelation_stretch` | 用去相关拉伸强调颜色差异(decorrelation stretch)。 |
| `spec_endmembers_ppi` | 用 Pixel Purity Index 近似提取端元。 |
| `spec_fuse` | 将已配准的单波段图像组融合为一张。 |
| `spec_index` | 归一化差值指数 (a-b)/(a+b+eps)(NDVI 型)。 |
| `spec_mnf` | 最小噪声分数变换(MNF)。 |
| `spec_nearest_band` | 返回最接近指定波长的波段 index。 |
| `spec_pansharpen` | 用高分辨率全色波段对多光谱做全色锐化。 |
| `spec_pca` | 沿光谱轴方向的主成分分析。 |
| `spec_rgb_composite` | 由选定的 3 个波段生成显示用 RGB 合成图像。 |
| `spec_unmix` | 用线性光谱解混估计逐像素的丰度图。 |
| `write_envi` | 写出 ENVI 立方体(.hdr + .img)。 |

#### 3D Matching(15 op)

| op | 说明 |
|---|---|
| `create_cam_pose_look_at_point` | 由相机位置与注视点构建 look-at 姿态(4x4)(create_cam_pose_look_at_point)。 |
| `create_deformable_surface_model` | 创建可变形 surface 模型(基于 PPF)(create_deformable_surface_model)。 |
| `create_shape_model_3d` | 由 3D 点云创建多视点轮廓影像 shape 模型(create_shape_model_3d)。 |
| `create_surface_model` | 构建模型点云的 Point Pair Feature 描述子(哈希表)。 |
| `find_box_3d` | 从点云检测轴平行边界盒(OBB 近似=PCA 盒)(find_box_3d)。 |
| `find_deformable_surface_model` | 从场景点云检测可变形 surface 模型(PPF + ICP refine)(find_deformable_surface_model)。 |
| `find_shape_model_3d` | 从图像检测 3D shape 模型(投影轮廓影像与相关)(find_shape_model_3d)。 |
| `find_surface_model` | 用 PPF 投票 + ICP 精化在场景中搜索模型的 6 自由度 pose。 |
| `find_surface_model_image` | 将深度图像点云化后检测 surface 模型(find_surface_model_image)。 |
| `project_shape_model_3d` | 将 3D 模型投影到相机并生成边缘图像(project_shape_model_3d)。 |
| `reduce_domain` | 将 domain 缩小到 region(reduce_domain)。与 change_domain 同义的 facade。 |
| `refine_deformable_surface_model` | 检测可变形 surface 模型 → 用 ICP 精化(refine_deformable_surface_model)。 |
| `refine_surface_model_pose` | 从初始姿态用 ICP 精化 surface 模型姿态(refine_surface_model_pose)。 |
| `refine_surface_model_pose_image` | 由深度图像点云化并用 ICP 精化姿态(refine_surface_model_pose_image)。 |
| `trans_pose_shape_model_3d` | 对 3D 模型应用姿态(4x4)(trans_pose_shape_model_3d)。 |

#### videops(15 op)

视频、时间序列处理(帧间差分、跟踪等)。

| op | 说明 |
|---|---|
| `background_subtraction` | 用时间中值的背景模型得到逐帧的前景掩码。 |
| `flicker_reduce` | 去除帧间整体亮度的闪烁(flicker)。 |
| `frame_difference` | 用相邻帧的绝对差分得到运动量体。 |
| `motion_energy` | 沿时间方向累积变化量的运动能量图 (H,W)。 |
| `moving_average` | 时间方向的滑动平均(box)平滑。 |
| `optical_flow_sequence` | 相邻帧间的光流强度体 (T-1,H,W)。 |
| `per_frame` | 将 2D op 独立应用到各帧。 |
| `spatiotemporal_gaussian` | (t,y,x) 的可分离 3D 高斯平滑。 |
| `spatiotemporal_sobel` | (t,y,x) 的 3D Sobel 梯度强度。 |
| `temporal_gradient` | 中心差分的时间微分 d(video)/dt。 |
| `temporal_max` | 时间方向的最大值投影 (H,W)。 |
| `temporal_mean` | 逐像素的时间平均 (H,W)。 |
| `temporal_median` | 逐像素的时间中值 (H,W)。 |
| `temporal_min` | 时间方向的最小值投影 (H,W)。 |
| `temporal_std` | 逐像素的时间标准差 = 活动图 (H,W)。 |

#### Segmentation(14 op)


![fops_segmentation_facade](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_segmentation_facade.png)
*图: Segmentation 的实际处理示例 — 琥珀中的昆虫: 在强烈橙色偏色+半透明散射+气泡、裂纹的干扰下,用最暗部二值化 → opening → 排除接触图像边缘的分量(边缘阴影、裂纹)→ 取最大分量的固定流水线抠出虫体(Fullseye 实际输出)。试错过程的 honest 记录: B 通道+clahe 预处理放大了琥珀的内部纹理,反而适得其反(clahe 并不总是正解)。输入全部为 AI 生成图像(Gemini)。*

| op | 说明 |
|---|---|
| `check_difference` | 将与基准图像之差超过 tol 的像素作为区域返回(check_difference)。 |
| `class_2dim_sup` | 在 2 通道特征空间中对落入 ref_region 分布的像素分类(有监督)(class_2dim_sup)。 |
| `class_2dim_unsup` | 对 2 通道特征空间做 k-means 无监督分类(class_2dim_unsup)。返回标签图像。 |
| `class_ndim_norm` | 用学习好的正态分布类对 ND 特征图像分类(Mahalanobis 距离 < thresh)(class_ndim_norm)。 |
| `classify_image_class_gmm` | 用高斯混合模型对多通道特征图像做像素分类(classify_image_class_gmm)。 |
| `classify_image_class_knn` | 用 k-NN 对多通道特征图像做像素分类(classify_image_class_knn)。 |
| `classify_image_class_lut` | 按灰度 LUT 做像素分类(阈值/标签 LUT)(classify_image_class_lut)。 |
| `classify_image_class_mlp` | 用训练好的 MLP 对多通道特征图像做像素分类(classify_image_class_mlp)。 |
| `classify_image_class_svm` | 用训练好的线性 SVM 对多通道特征图像做像素分类(classify_image_class_svm)。 |
| `expand_gray` | 从 seed 按灰度相似(/Δ/<tol)膨胀区域(expand_gray)。 |
| `expand_gray_ref` | 按与参考图像的灰度相似膨胀 seed(expand_gray_ref)。 |
| `learn_ndim_norm` | 由特征向量组学习正态分布类(均值、协方差)(learn_ndim_norm)。 |
| `regiongrowing_n` | 按多通道特征的相似性对整幅图像做区域分割(regiongrowing_n)。返回标签图像。 |
| `watersheds_marker` | 标记控制的 watershed 分割(watersheds_marker)。markers: int 标签图像(0=未分配)。 |

#### extra(14 op)

| op | 说明 |
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

基于立体视差的距离估计。也就是双眼的三角测量(参见正文 14.4)。

| op | 说明 |
|---|---|
| `BlockMatching` | 块匹配视差(cv2.StereoBM,不可用时 fullseye numpy)(stereo.BlockMatching)。  [backend=opencv] |
| `SGBM` | Semi-Global BM 视差(cv2.StereoSGBM,不可用时 fullseye SGM numpy)(stereo.SGBM)。  [backend=opencv] |
| `census_transform` | Census 变换: 按与邻域的大小关系编码各像素。 |
| `depth_from_disparity` | 由视差计算度量深度 Z = f·B/d。 |
| `disparity_census` | 用 Census + 汉明距离的赢者通吃估计稠密视差。 |
| `disparity_confidence` | 由代价曲线估计逐像素的匹配置信度 [0,1](PKRN 型)。 |
| `disparity_map` | 基于赢者通吃块匹配的稠密视差估计。 |
| `disparity_sgm` | Semi-Global Matching 视差(Hirschmüller 法)。 |
| `disparity_subpixel` | 用抛物线拟合将视差精化到亚像素。 |
| `fill_disparity` | 用行方向插值填补无效视差(偏向背景插值)。 |
| `lr_consistency` | 左右一致性检查的掩码(True = 可信的视差)。 |
| `reproject_to_points` | 将深度图反投影为相机坐标系的点云 (N,3)。 |
| `speckle_filter` | 从视差图中去除小的斑点区域。 |

#### terrain(13 op)

| op | 说明 |
|---|---|
| `detect_obstacles` | 将从可行走地面隆起 clearance 以上的单元分割为障碍物。 |
| `elevation_map` | 将点云装箱为 2.5D 高程网格。 |
| `fill_gaps` | 用最近邻的有效高度填补 nan 单元。 |
| `foothold_candidates` | 从地形中选出离散的安全落脚点候选。 |
| `foothold_score` | 逐单元的平坦度得分 [0,1](1 = 平坦且水平 = 好落脚点)。 |
| `fuse_elevation` | 将配准好的高程网格组融合为以机器人为中心的一张。 |
| `ground_plane` | 用单元级稳健最小二乘估计地面平面 z = ax+by+c。 |
| `ground_surface` | 用灰度开运算得到平滑的可行走地面包络面。 |
| `roughness_map` | 逐单元的粗糙度 = 局部高度的标准差。 |
| `slope_map` | 逐单元的坡度 = 相对水平面的表面角度。 |
| `step_edges` | 从高度图中检测台阶边缘(路缘、楼梯的踏空线)。 |
| `surface_normals` | 逐单元的朝上单位法线 (H,W,3)。 |
| `traversability` | 由台阶与坡度的上限生成可通行掩码。 |

#### artificial-life(12 op)

| op | 说明 |
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

| op | 说明 |
|---|---|
| `cx_apply_transfer_function` | 对中心化频谱乘以滤波器 H(应用传递函数)。 |
| `cx_bandpass` | 频域的理想圆环带通滤波器。 |
| `cx_fft` | 实图像的中心化 2D FFT(复频谱)。 |
| `cx_from_mag_phase` | 由幅值与弧度相位重构复数场。 |
| `cx_ifft` | cx_fft 的逆变换(ifft2 + ifftshift)。 |
| `cx_imag` | 将复数场的虚部作为实图像返回。 |
| `cx_log_magnitude` | 显示用的对数幅值频谱 [0,1]。 |
| `cx_magnitude` | 返回逐像素的复数幅值(绝对值)。 |
| `cx_phase` | 返回复数场的卷绕相位。 |
| `cx_real` | 将复数场的实部作为实图像返回。 |
| `cx_wiener_deconvolve` | 用频域 Wiener 去卷积复原图像。 |
| `phase_unwrap` | 2D 相位解缠(卷绕相位→连续相位)。 |

#### restoration(12 op)


![fops_restoration](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_restoration.png)
*图: restoration 的实际处理示例 — 运动模糊是卷积,所以轮廓强调(unsharp)无法复原,只有假定模糊 PSF 的 iv_motion_deblur(Wiener 逆卷积)才能把文字恢复到可读(Fullseye 实际输出)。模糊是通过卷积线性运动 PSF(L=9px, 0°)施加的(convol_fft)。输入为 skimage page/camera+AI 生成图像(Gemini)。*

| op | 说明 |
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

| op | 说明 |
|---|---|
| `boundary_edges` | 返回网格开放边缘的边列表 (M,2)。 |
| `components` | 将网格分割为连通分量。 |
| `convex_hull` | 生成点集的凸包网格(外向三角形)。 |
| `decimate_qem` | 用 QEM 边收缩简化到目标面数(decimation)。 |
| `inertia_tensor` | 水密网格所围立体的精确质量特性(惯性张量)。 |
| `is_edge_manifold` | 若没有任何边被 3 个以上面共享则为 True(边流形判定)。 |
| `is_watertight` | 若为边流形且封闭则为 True(水密判定)。 |
| `orient_consistent` | 统一全部面的环绕方向(同时返回被翻转的面数)。 |
| `remove_degenerate_faces` | 丢弃面积为零的退化面(顶点不变)。 |
| `smooth_taubin` | Taubin 的 λ/μ 平滑(拓扑不变)。 |
| `weld_vertices` | 融合(weld)容差内一致的顶点。 |

#### arithmetic(10 op)


![fops_arithmetic](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_arithmetic.png)
*图: arithmetic 的实际处理示例 — 暗部压死的图像用线性增益会先让亮部过曝,而 log_image(对数变换)在提升暗部的同时压缩亮部,两者得以兼顾(Fullseye 实际输出)。输入为 AI 生成(Gemini)、自制合成、skimage camera 减光的 3 种。*

| op | 说明 |
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
*图: augmentation 的实际处理示例 — 用物理模型从 1 张图像再现生成成像的恶劣条件(散粒噪声、运动模糊、周边减光),以扩充训练数据的 op 群(Fullseye 实际输出)。输入为 skimage camera+AI 生成图像(Gemini)2 种。*

| op | 说明 |
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

| op | 说明 |
|---|---|
| `bounds` | 返回轴平行包围盒 (min, max)。 |
| `mesh_to_points` | sample_surface 的别名 — 输入网格,输出点云。 |
| `normalize_scale` | 以原点为基准缩放,使包围盒最大边等于 size。 |
| `read_mesh` | 读取三角形网格并返回 (V, F)。 |
| `read_points` | 读取点云(带颜色时返回 (P, C))。 |
| `recenter` | 平移使顶点重心位于原点(返回新数组)。 |
| `sample_surface` | 从网格表面均匀采样 n 个点。 |
| `voxelize` | 将网格体素化到规则网格 (occ, origin)。 |
| `write_mesh` | 以 read_mesh 可读的格式(.obj 等)写出三角形网格。 |
| `write_points` | 将点云写出为 .ply / .xyz 等。 |

#### xldgeom(10 op)

| op | 说明 |
|---|---|
| `xg_area_center` | 用鞋带公式求轮廓的多边形面积(绝对值之和)。 |
| `xg_clip_contours` | 丢弃折线长不足最大长 a 倍的轮廓。 |
| `xg_crop_contours` | 只保留图像中央 a 比例窗口内的轮廓点。 |
| `xg_eccentricity` | 由点协方差计算离心率 sqrt(1-λmin/λmax)。 |
| `xg_elliptic_axis` | 点集的长短轴比 sqrt(λmax/λmin)。 |
| `xg_gen_polygons` | Douglas-Peucker 折线简化(eps 为外接矩形对角线的 a 倍)。 |
| `xg_height_width_ratio` | 点集轴平行外接矩形的纵横比。 |
| `xg_moments` | 点集的归一化 2 阶中心矩 mu20+mu02。 |
| `xg_orientation` | 主轴方向 [deg] 折回 [0,180) 并除以 180 归一化。 |
| `xg_regress_contours` | 全最小二乘直线拟合的残差 RMS(协方差短轴特征值的平方根)。 |

#### volops(9 op)

| op | 说明 |
|---|---|
| `vol_distance_transform` | 二值体的精确欧氏距离变换。 |
| `vol_frangi` | 3D Frangi 血管样(管状结构)增强 — 多尺度。 |
| `vol_gradient_magnitude` | 3D Sobel 梯度强度 sqrt(gz^2+gy^2+gx^2)。 |
| `vol_hessian_blobness` | 基于 Hessian 特征值的球状 blob 响应(单一尺度)。 |
| `vol_label` | 3D 连通分量标记(邻域系可选)。 |
| `vol_local_maxima` | 3D 局部极大(峰)检测。 |
| `vol_region_props` | 由标签体计算逐分量的定量特征。 |
| `vol_sato` | 3D Sato 管状结构滤波器(2 特征值的简化版)。 |
| `vol_watershed` | 标记控制的 3D watershed 分割(仅在安装 scikit-image 时可用)。 |

#### 2D Metrology(8 op)


![fops_metrology](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_metrology.png)
*图: 2D Metrology 的实际处理示例 — 对亚像素轮廓(threshold_sub_pix)做圆的最小二乘拟合(fit_circle)测量半径。在带真值的合成 6 圆上实测半径误差(Fullseye 实际输出)。输入为合成+AI 生成(Gemini)2 种。*

| op | 说明 |
|---|---|
| `add_metrology_object_circle_measure` | 添加圆测量对象(add_metrology_object_circle_measure)。 |
| `add_metrology_object_ellipse_measure` | 添加椭圆测量对象(add_metrology_object_ellipse_measure)。 |
| `add_metrology_object_generic` | 添加通用测量对象(add_metrology_object_generic)。 |
| `add_metrology_object_line_measure` | 添加直线测量对象(add_metrology_object_line_measure)。返回 index。 |
| `add_metrology_object_rectangle2_measure` | 添加矩形测量对象(add_metrology_object_rectangle2_measure)。 |
| `align_metrology_model` | 平移对齐测量模型的全部对象(align_metrology_model)。 |
| `apply_metrology_model` | 在各测量对象附近测量边缘,重新拟合形状并返回结果(apply_metrology_model)。 |
| `create_metrology_model` | 创建空的测量模型(create_metrology_model)。 |

#### Inspection(8 op)


![fops_inspection](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_inspection.png)
*图: Inspection 的实际处理示例 — 对泡罩包装(合成、注入缺陷以管理真值)按网格规格逐腔检查: 二值化→面积(缺件/异种)→圆度(缺损)→暗部像素(污渍)的固定阈值判定合格与否。3 板合计注入缺陷 11 件中检出 11 件、误检 0(Fullseye 实际输出)。*

| op | 说明 |
|---|---|
| `apply_bead_inspection_model` | 检查图像中的胶条,检测路径上的缺失/溢出(apply_bead_inspection_model)。 |
| `apply_texture_inspection_model` | 用纹理检查模型检测异常(Mahalanobis 距离大)区域(apply_texture_inspection_model)。 |
| `compare_ext_variation_model` | 扩展比较: 将同时满足相对(k*std)与绝对(abs_thresh)两阈值的像素判为缺陷(compare_ext_variation_model)。 |
| `compare_variation_model` | 将图像与 variation model 比较,返回 /image-mean/ > k*std 的缺陷区域(compare_variation_model)。 |
| `create_bead_inspection_model` | 胶条检查模型(基准路径 + 宽度公差)(create_bead_inspection_model)。 |
| `create_ocv_proj` | OCV(光学字符验证)用的平均模板模型(create_ocv_proj)。 |
| `create_texture_inspection_model` | 纹理检查模型(正常样本的局部统计分布)(create_texture_inspection_model)。 |
| `create_variation_model` | 由良品图像组创建逐像素均值、标准差的 variation model(create_variation_model)。 |

#### Morphology(8 op)

| op | 说明 |
|---|---|
| `bottom_hat` | closing(region) - region: 提取小的暗结构(缝隙)(bottom_hat)。 |
| `erosion2` | 带参考点 (row,col) 的结构元素腐蚀(erosion2)。 |
| `hit_or_miss` | hit-or-miss 变换: 前景用 disc 腐蚀 ∧ 背景用 disc 腐蚀(hit_or_miss)。用于角点/孤立点检测。 |
| `minkowski_add1` | Minkowski 和(用结构元素膨胀)(minkowski_add1)。 |
| `minkowski_add2` | 迭代 Minkowski 和(minkowski_add2)。 |
| `minkowski_sub1` | Minkowski 差(用结构元素腐蚀)(minkowski_sub1)。 |
| `minkowski_sub2` | 迭代 Minkowski 差(minkowski_sub2)。 |
| `top_hat` | region - opening(region): 提取小的亮结构(top_hat)。 |

#### color(8 op)


![fops_color](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_color.png)
*图: color 的实际处理示例 — "只挑红色的东西"在亮度图像中原理上不可能(等亮度时二值化无法区分),但用 trans_from_rgb 转到 HSV 后对 H(色相)通道做阈值处理,就能不受照明明暗影响按颜色挑选(Fullseye 实际输出)。输入为 AI 生成图像(Gemini)2 种+等亮度的自制合成 1 种。*

| op | 说明 |
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

| op | 说明 |
|---|---|
| `contrast_maximization` | 用对比度最大化(contrast maximisation, Gallego et al. 2018)估计全局光流。 |
| `event_count` | 逐像素的带符号对比度穿越次数 sign(d)*floor(abs(d)/thr)。 |
| `event_image` | 生成累积事件的图像(IWE)。 |
| `event_rate` | 整体事件活性 = 发放 1 次以上的像素占比。 |
| `event_rate_map` | 平滑发放掩码得到的局部事件密度图 [0,1]。 |
| `simulate_events` | 生成 2 帧之间的带符号事件极性图。 |
| `time_surface` | 由 (T,H,W) 堆栈计算 Surface of Active Events(SAE)。 |
| `warp_frame` | 将帧平移 (dy,dx)(用于运动补偿,双线性)。 |

#### grasp(8 op)

| op | 说明 |
|---|---|
| `approach_vector_from_normals` | 求与抓取轴正交的夹爪接近方向(单位向量)。 |
| `collision_free` | 手指扫掠的粗略干涉检查(近似)。 |
| `ferrari_canny_quality` | Ferrari-Canny 的 ε 抓取质量的近似计算。 |
| `force_closure` | 2 指对跖 force-closure(力闭合)判定(Nguyen 1988)。 |
| `grasp_pose` | 组装抓取的 4x4 夹爪坐标系(刚体 pose)。 |
| `grasps_from_mesh` | 先将网格表面点云化再提议抓取候选的一体版。 |
| `rank_grasps` | 将抓取候选按质量降序排列(最优在前)。 |
| `sample_antipodal_grasps` | 从点云提议带得分的 2 指对跖抓取候选。 |

#### measure(8 op)


![fops_measure](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_measure.png)
*图: measure 的实际处理示例 — BGA 焊球的 X 射线透射检查(衰减投影+注入空洞的自制合成 2 种+AI 生成 1 种): 逐球把内部的亮像素作为空洞测量面积率,并与真值对照(Fullseye 实际输出)。是贴近检查设备行业实务的题材。*

| op | 说明 |
|---|---|
| `angle` | 线段 p0→p1 的角度 [deg](图像 y 向下,(-180,180])。 |
| `distance` | 两点 (row,col) 间的欧氏距离。 |
| `fit_circle` | 对 (row,col) 点列的代数最小二乘圆拟合(Kåsa/Coope)。 |
| `fit_ellipse` | 直接最小二乘的椭圆拟合(Halir & Flusser 1998)。 |
| `fit_line` | 全最小二乘的直线拟合(正交回归)。 |
| `fit_rectangle2` | 面积最小的有向外接矩形拟合。 |
| `line_profile` | 沿线段 p0→p1 的亮度轮廓(双线性采样)。 |
| `profile_stats` | 轮廓的 min/max/mean 与最强边缘(梯度峰)的位置。 |

#### segment(8 op)

| op | 说明 |
|---|---|
| `Watershed` | 标记控制的 watershed 分割(cv2.watershed,不可用时 skimage,再没有则 numpy)  [backend=opencv] |
| `sg_felzenszwalb` | segment op(HALCON: -) |
| `sg_gmm_segment` | segment op(HALCON: -) |
| `sg_kmeans_intensity` | segment op(HALCON: -) |
| `sg_normalized_cut_2` | segment op(HALCON: -) |
| `sg_region_growing_seeded` | segment op(HALCON: -) |
| `sg_slic_superpixels` | segment op(HALCON: -) |
| `sg_watershed_gradient` | segment op(HALCON: -) |

#### 1D Measuring(7 op)


![fops_measuring1d](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_measuring1d.png)
*图: 1D Measuring 的实际处理示例 — 年轮和鱼耳石的轮纹可以用同一套工具来数: polar_trans_image 展开 → 角度平均的 1D 轮廓 → smooth_funct_1d_gauss+local_min_max_funct_1d 峰值计数。在带真值的合成数据上确认计数精度(Fullseye 实际输出)。输入为合成+AI 生成(Gemini)2 种。*

| op | 说明 |
|---|---|
| `create_funct_1d_pairs` | 由 (x,y) 对重采样为等间隔 1D 函数(create_funct_1d_pairs)。 |
| `fuzzy_measure_pairing` | 选出最符合模糊准则(预期宽度 pair_size)的边缘对(fuzzy_measure_pairing)。 |
| `gen_measure_arc` | 定义测量弧(沿圆周方向取轮廓)(gen_measure_arc)。 |
| `gen_measure_rectangle2` | 定义旋转测量矩形(沿长轴取轮廓)(gen_measure_rectangle2)。 |
| `measure_pairs` | 提取上升/下降边缘的对(结构的宽度)(measure_pairs)。 |
| `measure_pos` | 提取测量线上的边缘位置(亚像素)与幅值(measure_pos)。 |
| `translate_measure` | 平移测量对象(translate_measure)。 |

#### 3d(7 op)

| op | 说明 |
|---|---|
| `vol_dilate` | 3d op(HALCON: -) |
| `vol_erode` | 3d op(HALCON: -) |
| `vol_gaussian` | 3d op(HALCON: -) |
| `vol_median` | 3d op(HALCON: -) |
| `vol_mip` | 3d op(HALCON: -) |
| `vol_slice` | 3d op(HALCON: -) |
| `vol_threshold` | 3d op(HALCON: -) |

#### decomposition(7 op)

| op | 说明 |
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
*图: flow 的实际处理示例 — 从"理想高速相机"=自制弹道模拟连拍序列(dt=1/240s 已知,不含实际相机的卷帘快门/运动模糊)出发,用 frame_difference 检测动体 → 重心跟踪 → 抛物线拟合估计重力加速度 g,并与真值 9.81 m/s² 对照(Fullseye 实际输出)。这是从视频中测量物理常数的高速解析实务。*

| op | 说明 |
|---|---|
| `Farneback` | 稠密光流(cv2.calcOpticalFlowFarneback,不可用时 Horn-Schunck numpy)  [backend=opencv] |
| `flow_angle` | 逐像素的运动方向 atan2(v,u) [rad]。 |
| `flow_magnitude` | 逐像素的速度 sqrt(u^2+v^2)。 |
| `optical_flow_hs` | 稠密的 Horn-Schunck 光流(全局平滑性)。 |
| `optical_flow_lk` | 稠密的金字塔 Lucas-Kanade 光流。 |
| `track_points` | 将稀疏点从 prev→nxt 跟踪(Lucas-Kanade 点跟踪器)。 |
| `warp_by_flow` | 按光流对图像做前向 warp。 |

#### motion(7 op)

| op | 说明 |
|---|---|
| `detect_events` | 检测运动能量信号的尖峰位置(事件)。 |
| `dominant_motion` | 用最小二乘拟合全局仿射运动模型。 |
| `flow_from_model` | 由仿射运动模型 M 生成 (u,v) 光流场。 |
| `frame_motion_energy` | 光流场的 RMS 速度 = 每帧对 1 个标量。 |
| `motion_energy_series` | 逐相邻帧对的运动能量序列。 |
| `motion_segments` | 从光流场中分割独立运动的区域。 |
| `residual_motion` | 去除全局(相机)运动后的残差光流 = 独立物体的运动。 |

#### registration(7 op)

| op | 说明 |
|---|---|
| `apply_transform` | 对全部点应用刚体变换 R·p + t。 |
| `feature_register` | FPFH 特征 + RANSAC(+ICP 精化)的基于对应的配准。 |
| `icp` | ICP(迭代最近点法): 在对应关系未知的情况下将 src 配准到 dst。 |
| `kabsch` | 已对应点对的最优刚体变换(Kabsch 法)。 |
| `pca_align` | 由主轴做粗刚体配准(ICP 的一步初始化)。 |
| `point_to_plane_icp` | point-to-plane ICP: 最小化法线方向距离的配准。 |
| `register` | 从 pca_align 的大旋转初始化到 ICP 一路贯通的稳健一体配准。 |

#### render3d(7 op)

| op | 说明 |
|---|---|
| `auto_view` | 自动取景 (pose, K),使网格的外接球恰好收入画面。 |
| `intrinsics_from_fov` | 由垂直视场角生成针孔内参矩阵 K。 |
| `look_at` | 生成从 eye 看向 target 的相机 4x4 world→camera pose。 |
| `marching_cubes` | 从标量体提取等值面的三角形网格(marching cubes)。 |
| `mesh_to_sdf` | 计算水密网格的带符号距离场 (sdf, origin)。 |
| `render_mesh` | 将三角形网格光栅化为深度、轮廓影像、法线图。 |
| `voxelize_solid` | 计算填充至水密网格内部的体素占用 (occ, origin)。 |

#### sceneflow(7 op)

| op | 说明 |
|---|---|
| `ego_translation_from_flow` | 由平移光流场估计相机平移方向(行进方位)。 |
| `flow_curl` | 光流场的旋转(涡度)dv/dx - du/dy(逐像素)。 |
| `flow_divergence` | 光流场的散度 du/dx + dv/dy(逐像素)。 |
| `focus_of_expansion` | 扩张焦点(FOE): 平移时光流呈放射状涌出的图像上的点。 |
| `looming` | 由光流场汇总接近(碰撞迫近)的整体指标。 |
| `scene_flow` | 由立体+光流对计算逐像素的 3D 场景流(Vedula 1999)。 |
| `time_to_contact` | 逐像素的接触时间 τ [帧](Lee 1976)。 |

#### physics(6 op)

| op | 说明 |
|---|---|
| `ph_coherence_enhancing_diffusion` | physics op(HALCON: -) |
| `ph_heat_flow` | physics op(HALCON: -) |
| `ph_mean_curvature_motion` | physics op(HALCON: -) |
| `ph_perona_malik` | physics op(HALCON: -) |
| `ph_reaction_diffusion` | physics op(HALCON: -) |
| `ph_total_variation_flow` | physics op(HALCON: -) |

#### raster(6 op)

| op | 说明 |
|---|---|
| `read_depth` | 读取度量深度图 (depth, valid)。 |
| `read_pfm` | 读取 PFM(Portable Float Map)(arr, scale)。 |
| `read_raster` | 保持原生位深读取栅格 (arr, meta)。 |
| `save16` | 按扩展名对应的格式以高精度写出。 |
| `to01` | 不触碰原始值,返回 [0,1] 的 float64 视图。 |
| `write_pfm` | 写出 PFM((H,W) 为灰度,(H,W,3) 为彩色)。 |

#### subpix(6 op)

| op | 说明 |
|---|---|
| `sp_critical_points_sub_pix` | subpix op(HALCON: critical_points_sub_pix) |
| `sp_local_max_sub_pix` | subpix op(HALCON: -) |
| `sp_local_min_sub_pix` | subpix op(HALCON: local_min_sub_pix) |
| `sp_lowlands_center` | subpix op(HALCON: lowlands_center) |
| `sp_plateaus` | subpix op(HALCON: plateaus) |
| `sp_saddle_points_sub_pix` | subpix op(HALCON: saddle_points_sub_pix) |

#### detect(5 op)


![fops_detect](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_detect.png)
*图: detect 的实际处理示例 — "分开(segment_objects)→测量(逐个体的特征量)→分拣(聚类着色)"的 3 段用法(Fullseye 实际输出+numpy k-means)。聚类是无监督的分组,并非物种鉴定。哈勃深空为 NASA/STScI(scikit-image 自带,公有领域)。*

| op | 说明 |
|---|---|
| `draw_objects` | 返回各物体掩码着色 + bbox 绘制的 RGB 可视化。 |
| `feature_table` | 生成逐物体的特征一览(面积、圆形度、离心率、重心)。 |
| `nearest_prototype` | 用最近邻原型 {label: 描述子} 对描述子分类。 |
| `object_descriptor` | 用于识别的对尺度、旋转稳健的紧凑描述子(Hu 的 7 个矩等)。 |
| `segment_objects` | 分割前景物体,按连通分量返回记录。 |

#### locomotion(5 op)

| op | 说明 |
|---|---|
| `com_from_silhouette` | 返回二值轮廓影像的重心 (row,col)。 |
| `com_support_margin` | 静态稳定裕度: 重心的接地投影到支撑多边形边界的带符号距离。 |
| `contact_points` | 提取距地面平面 tol 以内的点 = 接地点。 |
| `gait_phase` | 由足部高度对各帧分类支撑相/摆动相。 |
| `support_polygon` | 求接地点的凸支撑多边形(地面 x,y 平面)。 |

#### measure1d(5 op)

| op | 说明 |
|---|---|
| `m1_fuzzy_measure_pos` | measure1d op(HALCON: fuzzy_measure_pos) |
| `m1_measure_pairs` | measure1d op(HALCON: measure_pairs) |
| `m1_measure_pos` | measure1d op(HALCON: measure_pos) |
| `m1_measure_projection` | measure1d op(HALCON: measure_projection) |
| `m1_measure_thresh` | measure1d op(HALCON: measure_thresh) |

#### occupancy(5 op)

| op | 说明 |
|---|---|
| `clearance_map` | 各单元到最近障碍物的距离图(世界单位)。 |
| `frontier_cells` | 探索用边界单元: 与未知区域相邻的自由单元。 |
| `inflate_obstacles` | 将占用单元膨胀 radius_cells(构型空间的障碍物)。 |
| `line_of_sight` | 若两单元间的直线不穿越障碍物则为 True。 |
| `occupancy_grid_2d` | 将 3D 点云聚合为俯视 2D 占用栅格。 |

#### odometry(5 op)

| op | 说明 |
|---|---|
| `integrate_trajectory` | 将相对运动序列合成为绝对 4x4 pose 序列。 |
| `pnp_odometry` | 由上一帧 3D 点在当前帧的对应,用 PnP 估计相机运动。 |
| `rgbd_odometry` | 由 RGB-D 对 + 光流估计帧间相机运动。 |
| `trajectory_error` | 估计轨迹与真值轨迹的绝对轨迹误差(ATE)。 |
| `umeyama_align` | 用 Umeyama 的最小二乘相似变换将 src 点云对齐到 dst。 |

#### pointcloud(5 op)

| op | 说明 |
|---|---|
| `estimate_normals` | 用 k 近邻的局部 PCA 逐点估计法线。 |
| `fpfh` | 逐点的 FPFH(Fast Point Feature Histogram)描述子(Rusu 2009)。 |
| `remove_radius_outliers` | 去除 radius 内近邻数不足 min_neighbors 的点。 |
| `remove_statistical_outliers` | 去除 k 近邻平均距离偏离整体分布的点(统计离群点去除)。 |
| `voxel_downsample` | 按占用体素抽稀为每体素 1 点(单元重心)。 |

#### tactile(5 op)

| op | 说明 |
|---|---|
| `tac_contact_mask` | tactile op(HALCON: -) |
| `tac_height_from_shading` | tactile op(HALCON: -) |
| `tac_pressure_proxy` | tactile op(HALCON: -) |
| `tac_shear_field` | tactile op(HALCON: -) |
| `tac_surface_normal` | tactile op(HALCON: -) |

#### tomography(5 op)

| op | 说明 |
|---|---|
| `tm_backproject_unfiltered` | tomography op(HALCON: -) |
| `tm_fbp_reconstruct` | tomography op(HALCON: -) |
| `tm_radon_forward` | tomography op(HALCON: -) |
| `tm_sart_reconstruct` | tomography op(HALCON: -) |
| `tm_sinogram_denoise` | tomography op(HALCON: -) |

#### deformreg(4 op)

| op | 说明 |
|---|---|
| `demons_register` | 用 Thirion 的 demons 法将 moving 非刚体配准到 fixed。 |
| `field_magnitude` | 逐像素的位移长度 sqrt(fx^2+fy^2)。 |
| `residual_ssd` | 两图像亮度差的平方和(0 = 相同)。 |
| `warp_by_field` | 用位移场 (fx,fy) 对图像做 warp(双线性,边界钳制)。 |

#### macro(4 op)

| op | 说明 |
|---|---|
| `macro_binarize` | macro op(HALCON: -) |
| `macro_denoise` | macro op(HALCON: -) |
| `macro_edge` | macro op(HALCON: -) |
| `macro_vol_denoise` | macro op(HALCON: -) |

#### pose(4 op)

| op | 说明 |
|---|---|
| `pose_descriptor` | 组合骨架图与主轴的紧凑姿势描述子。 |
| `principal_axis` | 由前景像素 PCA 得到的图形主轴。 |
| `skeleton_nodes` | 统计骨架的端点数、分叉点数。 |
| `skeletonize_mask` | 二值图形的 1 像素宽形态学骨架化。 |

#### artistic(3 op)

| op | 说明 |
|---|---|
| `xcv_pencil_sketch` | artistic op(HALCON: -) |
| `xcv_stylization` | artistic op(HALCON: -) |
| `xpil_emboss` | artistic op(HALCON: -) |

#### deformation(3 op)

| op | 说明 |
|---|---|
| `deform_ffd` | deformation op(HALCON: -) |
| `deform_mls` | deformation op(HALCON: -) |
| `deform_tps` | deformation op(HALCON: -) |

#### ppf(3 op)

| op | 说明 |
|---|---|
| `find_surface_pose` | 一次完成模型描述子构建与场景匹配的一体版。 |
| `ppf_model` | 构建模型点云的 Point Pair Feature 描述子(哈希表)。 |
| `surface_match` | 用 PPF 投票 + ICP 精化在场景中搜索模型的 6 自由度 pose。 |

#### sim-source(3 op)

| op | 说明 |
|---|---|
| `Gazebo` | Gazebo sim-source(未接入 scaffold)。计划经 gz-transport 桥供给 RGB/depth/真值。  [sim=gazebo, scaffold] |
| `IsaacSim` | Isaac Sim sim-source(未接入 scaffold)。计划经 omni.replicator 桥供给。  [sim=isaacsim, scaffold] |
| `MuJoCo` | MuJoCo sim-source: 渲染 RGB/深度,计算 K,输出真值姿态,并反投影深度  [sim=mujoco, available] |

#### transform(3 op)

| op | 说明 |
|---|---|
| `tf_radon_sinogram` | transform op(HALCON: -) |
| `xmh_daubechies` | transform op(HALCON: -) |
| `xmh_haar` | transform op(HALCON: -) |
