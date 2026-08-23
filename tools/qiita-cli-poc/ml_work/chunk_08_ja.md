#### Matrix(46 op)

行列演算・連立方程式・分解(SVD 等)。カメラ較正や姿勢推定の数学的裏方です。

| op | 説明 |
|---|---|
| `abs_matrix` | 行列の各要素の絶対値を計算する。 |
| `abs_matrix_mod` | 要素ごとの絶対値(結果を入力行列へ上書き)。 |
| `add_matrix` | 2 つの行列を加算する。 |
| `add_matrix_mod` | 行列加算(結果を入力行列へ上書き)。 |
| `create_matrix` | 新しい行列を生成する。 |
| `decompose_matrix` | LU 分解(P,L,U)を返す(decompose_matrix)。 |
| `determinant_matrix` | 行列式を計算する。 |
| `div_element_matrix` | 行列同士を要素ごとに除算する。 |
| `div_element_matrix_mod` | 要素ごとの除算(結果を入力行列へ上書き)。 |
| `eigenvalues_general_matrix` | 一般行列の固有値(必要なら固有ベクトルも)を計算する。 |
| `eigenvalues_symmetric_matrix` | 対称行列の固有値(必要なら固有ベクトルも)を計算する。 |
| `generalized_eigenvalues_general_matrix` | 一般行列対の一般化固有値(必要なら固有ベクトルも)を計算する。 |
| `generalized_eigenvalues_symmetric_matrix` | 対称行列対の一般化固有値(必要なら固有ベクトルも)を計算する。 |
| `get_diagonal_matrix` | 行列の対角要素を取り出す。 |
| `get_sub_matrix` | 部分行列を取り出す。 |
| `invert_matrix` | 逆行列を計算する。 |
| `invert_matrix_mod` | 逆行列(結果を入力行列へ上書き)。 |
| `max_matrix` | 行列要素の最大値を返す。 |
| `mean_matrix` | 行列要素の平均を返す。 |
| `min_matrix` | 行列要素の最小値を返す。 |
| `mult_element_matrix` | 行列同士を要素ごとに乗算する。 |
| `mult_element_matrix_mod` | 要素ごとの乗算(結果を入力行列へ上書き)。 |
| `mult_matrix` | 2 つの行列の積を計算する。 |
| `mult_matrix_mod` | 行列積(結果を入力行列へ上書き)。 |
| `norm_matrix` | 行列のノルムを計算する。 |
| `orthogonal_decompose_matrix` | QR 直交分解を返す(orthogonal_decompose_matrix)。 |
| `pow_element_matrix` | 行列の各要素をべき乗する。 |
| `pow_element_matrix_mod` | 要素ごとのべき乗(結果を入力行列へ上書き)。 |
| `pow_matrix` | 行列そのもののべき乗を計算する。 |
| `pow_matrix_mod` | 行列べき乗(結果を入力行列へ上書き)。 |
| `pow_scalar_element_matrix` | スカラーを底、各要素を指数とするべき乗を要素ごとに計算する。 |
| `pow_scalar_element_matrix_mod` | スカラー底の要素べき乗(結果を入力行列へ上書き)。 |
| `repeat_matrix` | 行列をタイル状に繰り返して並べる。 |
| `scale_matrix` | 行列をスカラー倍する。 |
| `scale_matrix_mod` | スカラー倍(結果を入力行列へ上書き)。 |
| `set_diagonal_matrix` | 行列の対角要素を設定する。 |
| `set_sub_matrix` | 部分行列を書き込む。 |
| `solve_matrix` | 連立一次方程式の解を計算する。 |
| `sqrt_matrix` | 行列の各要素の平方根を計算する。 |
| `sqrt_matrix_mod` | 要素ごとの平方根(結果を入力行列へ上書き)。 |
| `sub_matrix` | 2 つの行列を減算する。 |
| `sub_matrix_mod` | 行列減算(結果を入力行列へ上書き)。 |
| `sum_matrix` | 行列要素の総和を返す。 |
| `svd_matrix` | 特異値分解(SVD)を計算する。 |
| `transpose_matrix` | 行列を転置する。 |
| `transpose_matrix_mod` | 転置(結果を入力行列へ上書き)。 |

#### 3D Reconstruction(43 op)

深度・視差・多視点からの 3D 復元。2.5D(深度画像)から点群・メッシュの世界へ渡る橋です。

![3D Reconstruction の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_16_depth_to_points.png)
*図: 深度 → 点群の例(11.1.1 節より再掲)*

| op | 説明 |
|---|---|
| `apply_sheet_of_light_calibration` | プロファイル(画素行)を高さ(メトリック)へ換算(apply_sheet_of_light_calibration)。 |
| `binocular_disparity` | Semi-Global Matching によるステレオ視差推定(Hirschmüller 法)。 |
| `binocular_disparity_mg` | 勝者総取りブロックマッチングによる密な視差推定。 |
| `binocular_disparity_ms` | SGM 視差推定の別入口(実装は Hirschmüller 法)。 |
| `binocular_distance` | 視差から計量深度 Z = f·B/d を計算する。 |
| `binocular_distance_mg` | 視差→計量深度 Z = f·B/d(mg 入口)。 |
| `binocular_distance_ms` | 視差→計量深度 Z = f·B/d(ms 入口)。 |
| `calibrate_sheet_of_light` | 既知段差からシート光の画素→高さスケールを校正(calibrate_sheet_of_light)。 |
| `create_sheet_of_light_calib_object` | シート光校正オブジェクト(既知段差)(create_sheet_of_light_calib_object)。 |
| `create_sheet_of_light_model` | シート光(レーザライン)プロファイル計測モデル(create_sheet_of_light_model)。 |
| `create_stereo_model` | ステレオ計測モデル(左右内部 + 相対姿勢)(create_stereo_model)。 |
| `create_structured_light_model` | 構造化光計測モデル(位相シフトパターン設定)(create_structured_light_model)。 |
| `decode_structured_light_pattern` | 位相シフト構造化光の画像列から絶対位相(=対応)を復号(decode_structured_light_pattern)。 |
| `depth_from_focus` | フォーカススタックから画素ごと最良合焦位置=深度を推定(depth_from_focus)。 |
| `disparity_to_distance` | 視差 d を距離 Z = f*baseline/d に変換(disparity_to_distance)。 |
| `disparity_to_point_3d` | 画像点 (row,col) と視差 disparity から 3D 点 (X,Y,Z) を計算(disparity_to_point_3d)。 |
| `distance_to_disparity` | 距離 Z を視差 d = f*baseline/Z に変換(distance_to_disparity)。 |
| `essential_to_fundamental_matrix` | 基本行列 F = K2^-T E K1^-1 を本質行列 E から計算(essential_to_fundamental_matrix)。 |
| `gen_binocular_proj_rectification` | 基礎行列からステレオ平行化のためのエピポール整列変換を推定 |
| `gen_binocular_rectification_map` | 較正済みステレオペアの平行化回転を計算する(Fusiello 法)。 |
| `gen_structured_light_pattern` | 正弦波の構造化光パターン画像を生成(gen_structured_light_pattern)。 |
| `intersect_lines_of_sight` | 2 視点の対応画素を線形 DLT 三角測量で 3D 復元する。 |
| `match_essential_matrix_ransac` | 点対応と内部行列 K から RANSAC で本質行列 E を推定(match_essential_matrix_ransac)。 |
| `match_fundamental_matrix_distortion_ransac` | 歪み込み基礎行列の RANSAC 推定(match_fundamental_matrix_distortion_ransac)。 |
| `match_fundamental_matrix_ransac` | 点対応から RANSAC で基礎行列 F とインライアを推定(match_fundamental_matrix_ransac)。 |
| `match_rel_pose_ransac` | 点対応から相対姿勢を RANSAC 推定(match_rel_pose_ransac)。 |
| `measure_profile_sheet_of_light` | 各列でレーザライン(最大輝度)の行位置=高さプロファイルを抽出 |
| `photometric_stereo` | 複数照明画像(Lambertian)から法線と反射率を復元(photometric_stereo)。 |
| `reconst3d_from_fundamental_matrix` | 基礎行列経由で相対姿勢を分解し対応点を三角測量(reconst3d_from_fundamental_matrix)。 |
| `reconstruct_height_field_from_gradient` | 勾配場 (dz/dr, dz/dc) を Frankot-Chellappa で積分し高さ場 z を復元 |
| `reconstruct_points_stereo` | 左右対応点(行一致)から視差経由で 3D 点群を復元(reconstruct_points_stereo)。 |
| `reconstruct_surface_stereo` | 視差マップ全体から 3D 点群(サーフェス)を復元(reconstruct_surface_stereo)。 |
| `reconstruct_surface_structured_light` | 構造化光の位相復号 → 視差 → 3D サーフェス復元(reconstruct_surface_structured_light)。 |
| `rel_pose_to_fundamental_matrix` | 相対姿勢 (R,t) と内部行列から基礎行列 F を計算(rel_pose_to_fundamental_matrix)。 |
| `select_grayvalues_from_channels` | index 画像に従い多チャネルスタックから画素ごとにグレー値を選ぶ |
| `sfs_mod_lr` | Shape-from-Shading(改良 linear、sfs_mod_lr)。Pentland 実装を共用。 |
| `sfs_orig_lr` | Shape-from-Shading(原法 linear、sfs_orig_lr)。Pentland 実装を共用。 |
| `sfs_pentland` | Pentland の線形化 Shape-from-Shading で高さ場を復元(sfs_pentland)。 |
| `uncalibrated_photometric_stereo` | 光源方向未知の photometric stereo(SVD で 3 階数近似、uncalibrated_photometric_stereo)。 |
| `vector_to_essential_matrix` | 較正済みペアの 8 組以上の対応から基本行列 E を推定する。 |
| `vector_to_fundamental_matrix` | 8 組以上の対応から正規化 8 点法で基礎行列 F を推定する。 |
| `vector_to_fundamental_matrix_distortion` | 歪み込みで基礎行列を RANSAC 推定(歪みは小と仮定し正規化 8-point) |
| `vector_to_rel_pose` | 点対応と内部行列から相対姿勢 (R,t) を推定(本質行列分解)(vector_to_rel_pose)。 |

#### 3D Object Model(40 op)

点群・メッシュ(3D オブジェクトモデル)の操作。変換・法線・簡略化・特徴量など。

| op | 説明 |
|---|---|
| `affine_trans_object_model_3d` | 全点に剛体変換 R·p + t を適用する。 |
| `area_object_model_3d` | 3D 点群の凸包表面積を返す(area_object_model_3d)。 |
| `connection_object_model_3d` | ユークリッドクラスタリングで近接点をグループ化する(Rusu 2009)。 |
| `convex_hull_object_model_3d` | 3D 凸包の頂点を返す(convex_hull_object_model_3d)。 |
| `distance_object_model_3d` | 2 つの 3D モデル間の最小点間距離(distance_object_model_3d)。 |
| `edges_object_model_3d` | 局所曲率が高い点=3D エッジを抽出(edges_object_model_3d)。近傍 PCA の平面性で判定。 |
| `fit_primitives_object_model_3d` | RANSAC で支配平面をロバストにフィットする。 |
| `fuse_object_model_3d` | 複数 3D モデルを 1 つに統合(fuse_object_model_3d)。 |
| `gen_box_object_model_3d` | 箱の 6 面の点群(gen_box_object_model_3d)。 |
| `gen_cylinder_object_model_3d` | 円柱側面の点群(gen_cylinder_object_model_3d)。 |
| `gen_empty_object_model_3d` | 空の 3D モデル(gen_empty_object_model_3d)。 |
| `gen_object_model_3d_from_points` | x,y,z 配列から 3D 点群モデルを作る(gen_object_model_3d_from_points)。 |
| `gen_plane_object_model_3d` | z=0 平面上の格子点群(gen_plane_object_model_3d)。 |
| `gen_sphere_object_model_3d` | 球面上の準一様点群(黄金螺旋、gen_sphere_object_model_3d)。 |
| `gen_sphere_object_model_3d_center` | 中心指定の球面点群(gen_sphere_object_model_3d_center)。 |
| `intersect_plane_object_model_3d` | 平面(a,b,c,d)の近傍(距離<tol)の点=断面を返す(intersect_plane_object_model_3d)。 |
| `max_diameter_object_model_3d` | 点群の最大差し渡し径(convex 包上で最遠 2 点、max_diameter_object_model_3d)。 |
| `moments_object_model_3d` | 3D 点群の重心と共分散(2 次中心モーメント)を返す(moments_object_model_3d)。 |
| `object_model_3d_to_xyz` | 3D 点群を X/Y/Z 画像へ(格子順、object_model_3d_to_xyz)。 |
| `prepare_object_model_3d` | 法線推定つきモデル前処理(近傍 PCA、prepare_object_model_3d)。 |
| `project_object_model_3d` | ワールド点群 (N,3) を画素へ射影し (uv, depth) を返す。 |
| `projective_trans_object_model_3d` | 4x4 射影変換を適用(projective_trans_object_model_3d)。既定は恒等。 |
| `reduce_object_model_3d_by_view` | 指定軸で手前 keep 割合の点のみ残す(視点による簡易間引き、reduce_object_model_3d_by_view)。 |
| `register_object_model_3d_global` | point-to-plane ICP: 法線方向の距離を最小化して src を dst へ位置合わせ。 |
| `register_object_model_3d_pair` | ICP(反復最近点法): 対応未知のまま src を dst へ位置合わせ。 |
| `render_object_model_3d` | 3D モデルを画像へレンダリング(深度で明暗、render_object_model_3d)。 |
| `rigid_trans_object_model_3d` | 4x4 剛体/相似変換を点群へ適用(rigid_trans_object_model_3d)。 |
| `sample_object_model_3d` | 占有ボクセルごとに 1 点(セル重心)へ間引くダウンサンプリング。 |
| `segment_object_model_3d` | 近傍距離で点群を連結成分に分割(segment_object_model_3d)。ラベル配列を返す。 |
| `select_object_model_3d` | 属性値域で点を選択(select_object_model_3d)。 |
| `select_points_object_model_3d` | 指定軸の値域で点を選ぶ(select_points_object_model_3d)。 |
| `simplify_object_model_3d` | ボクセルグリッド平均で点群を簡約(simplify_object_model_3d)。 |
| `smallest_bounding_box_object_model_3d` | PCA による有向バウンディングボックスを求める。 |
| `smallest_sphere_object_model_3d` | 最小包含球の近似(中心=重心、半径=最遠点、smallest_sphere_object_model_3d)。 |
| `smooth_object_model_3d` | 各点を k 近傍の重心へ移動して平滑化(smooth_object_model_3d)。 |
| `surface_normals_object_model_3d` | k 近傍の局所 PCA で点ごとの法線を推定する。 |
| `triangulate_object_model_3d` | 主平面へ投影して Delaunay 三角形分割(triangulate_object_model_3d)。三角形頂点 index を返す。 |
| `union_object_model_3d` | 2 つの 3D モデルを結合(union_object_model_3d)。 |
| `volume_object_model_3d_relative_to_plane` | 平面 (a,b,c,d) より上の点群体積を凸包で近似(volume_object_model_3d_relative_to_plane)。 |
| `xyz_to_object_model_3d` | X/Y/Z 画像(各 2D)から 3D 点群モデルへ(xyz_to_object_model_3d)。 |

#### gray(40 op)

グレースケール形態学など、濃淡画像のまま行う形態学的処理。


![fops_gray](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_gray.png)
*図: gray の実処理例 — 照明ムラ・低コントラストの入力では大域ヒストグラム均等化が破綻(明部の白飛び・ノイズ増幅)しやすいのに対し、clahe(コントラスト制限付き局所適応均等化)は局所ごとに階調を回復する(Fullseye 実出力)。入力は AI 生成(Gemini)2 種+skimage 同梱 moon。*

| op | 説明 |
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

テンプレートマッチング・形状マッチング。「教えた形をどこでも見つける」係で、産業画像処理の華です。

| op | 説明 |
|---|---|
| `adapt_shape_model_high_noise` | 高ノイズ向けに平滑化を強めた形状モデルを作る(adapt_shape_model_high_noise)。 |
| `create_aniso_shape_model` | 異方性スケール形状モデル(create_aniso_shape_model、モデル自体は同一、find で異方 scale 探索)。 |
| `create_aniso_shape_model_xld` | XLD 輪郭から異方性スケール形状モデル(create_aniso_shape_model_xld)。 |
| `create_calib_descriptor_model` | 校正済 descriptor モデル(create_calib_descriptor_model)。 |
| `create_generic_shape_model` | 汎用形状モデル(create_generic_shape_model、create_shape_model と同核)。 |
| `create_local_deformable_model` | 局所変形マッチング用モデル(テンプレート保持)(create_local_deformable_model)。 |
| `create_local_deformable_model_xld` | XLD 由来の局所変形モデル(create_local_deformable_model_xld)。 |
| `create_ncc_model` | NCC モデル(=正規化テンプレート)を準備(create_ncc_model)。 |
| `create_planar_calib_deformable_model` | 平面(校正済)変形モデル(create_planar_calib_deformable_model)。 |
| `create_planar_calib_deformable_model_xld` | XLD 由来の平面校正済変形モデル(create_planar_calib_deformable_model_xld)。 |
| `create_planar_uncalib_deformable_model` | 平面(未校正)変形モデル(create_planar_uncalib_deformable_model)。 |
| `create_planar_uncalib_deformable_model_xld` | XLD 由来の平面未校正変形モデル(create_planar_uncalib_deformable_model_xld)。 |
| `create_scaled_shape_model` | 等方スケール形状モデル(create_scaled_shape_model)。 |
| `create_scaled_shape_model_xld` | XLD 輪郭からスケール対応形状モデル(create_scaled_shape_model_xld)。 |
| `create_shape_model` | テンプレートのエッジ点(/grad/>min_grad)の正規化勾配ベクトルをモデル化(create_shape_model)。 |
| `create_shape_model_xld` | XLD 輪郭から形状モデルを作る(create_shape_model_xld)。 |
| `create_uncalib_descriptor_model` | 未校正 descriptor モデル(Harris keypoint + 正規化パッチ)(create_uncalib_descriptor_model)。 |
| `determine_deformable_model_params` | 変形モデルの推奨パラメータを決定(determine_deformable_model_params)。 |
| `determine_ncc_model_params` | NCC モデルの推奨パラメータ(コントラスト/レベル数)を決定(determine_ncc_model_params)。 |
| `determine_shape_model_params` | テンプレートから推奨 min_grad/コントラストを自動決定(determine_shape_model_params)。 |
| `find_aniso_shape_model` | 行/列独立スケール(異方性)での形状モデル検出(find_aniso_shape_model)。 |
| `find_aniso_shape_models` | 異方性スケールでの複数インスタンス検出(find_aniso_shape_models)。 |
| `find_calib_descriptor_model` | 校正済 descriptor モデルの検出 → 平面姿勢(find_calib_descriptor_model)。 |
| `find_generic_shape_model` | 汎用形状モデル検出(find_generic_shape_model)。find_shape_model の別名。 |
| `find_local_deformable_model` | 剛体位置を粗く合わせた後、オプティカルフローで局所変形を推定 |
| `find_ncc_model` | NCC モデルを画像中で探索し最良一致(行/列/スコア)を返す(find_ncc_model)。 |
| `find_ncc_models` | NCC モデルの複数インスタンス検出(find_ncc_models)。 |
| `find_planar_calib_deformable_model` | 平面校正済変形モデルの検出(find_planar_calib_deformable_model)。 |
| `find_planar_uncalib_deformable_model` | 平面未校正変形モデルの検出(find_planar_uncalib_deformable_model)。 |
| `find_scaled_shape_model` | スケールを変えながら最良一致を探索(find_scaled_shape_model)。 |
| `find_scaled_shape_models` | スケール探索つき複数インスタンス検出(find_scaled_shape_models)。 |
| `find_shape_models` | 複数インスタンスを非最大抑制つきで検出(find_shape_models)。 |
| `find_uncalib_descriptor_model` | descriptor モデルを画像から検出(比率テスト + RANSAC ホモグラフィ) |
| `get_shape_model_contours` | 形状モデルのエッジ点を輪郭として返す(get_shape_model_contours)。 |
| `get_shape_model_origin` | 形状モデルの原点(重心)を返す(get_shape_model_origin)。 |
| `inspect_shape_model` | 形状モデルのエッジ点数・広がり・原点を点検用に返す(inspect_shape_model)。 |
| `set_shape_model_origin` | 形状モデルの参照原点を設定(set_shape_model_origin)。 |

#### XLD(35 op)

XLD = サブピクセル精度の輪郭表現。画素より細かい精度で輪郭を扱う、精密計測の要です。


![fops_xld](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_xld.png)
*図: XLD の実処理例 — 二値化した境界は画素格子の階段にしかならないが、threshold_sub_pix はレベル交差位置を画素より細かく(サブピクセル)推定した輪郭(XLD)を返す。真値つき合成円で平均誤差 0.001px を実測。8 倍拡大で階段と滑らかな輪郭線の差が見える(Fullseye 実出力)。入力は自前合成・AI 生成(Gemini)・skimage coins。*

| op | 説明 |
|---|---|
| `difference_closed_contours_xld` | 2 閉輪郭の差(difference_closed_contours_xld)。 |
| `difference_closed_polygons_xld` | 2 閉多角形の差(difference_closed_polygons_xld)。 |
| `gen_circle_contour_xld` | 円弧輪郭を生成(gen_circle_contour_xld)。 |
| `gen_contour_nurbs_xld` | 制御点から NURBS(B スプライン)輪郭を生成(gen_contour_nurbs_xld)。 |
| `gen_contour_polygon_rounded_xld` | 角を丸めた多角形輪郭を生成(gen_contour_polygon_rounded_xld)。 |
| `gen_contour_polygon_xld` | 点列から多角形輪郭を生成(gen_contour_polygon_xld)。 |
| `gen_contours_skeleton_xld` | 領域のスケルトンを抽出し輪郭(枝ごと)へ変換(gen_contours_skeleton_xld)。 |
| `gen_cross_contour_xld` | 十字マーカー輪郭を生成(gen_cross_contour_xld)。 |
| `gen_ellipse_contour_xld` | 楕円弧輪郭を生成(gen_ellipse_contour_xld)。 |
| `gen_nurbs_interp` | 点を通る NURBS 補間輪郭(gen_nurbs_interp)。 |
| `gen_parallels_xld` | 各輪郭に平行なオフセット輪郭を生成(gen_parallels_xld)。 |
| `gen_rectangle2_contour_xld` | 回転矩形の輪郭を生成(gen_rectangle2_contour_xld)。 |
| `get_contour_angle_xld` | 輪郭に沿った接線角(ラジアン)を各点で返す(get_contour_angle_xld)。 |
| `get_polygon_xld` | Douglas-Peucker で輪郭を多角形近似(get_polygon_xld)。頂点列を返す。 |
| `get_regress_params_xld` | 輪郭点への回帰直線パラメータ(法線角 nr,nc と原点距離 dist)(get_regress_params_xld)。 |
| `intersection_closed_contours_xld` | 2 閉輪郭の積(intersection_closed_contours_xld)。 |
| `intersection_closed_polygons_xld` | 2 閉多角形の積(intersection_closed_polygons_xld)。 |
| `intersection_region_contour_xld` | 領域と閉輪郭の交差領域(intersection_region_contour_xld)。 |
| `local_max_contours_xld` | 輪郭上でグレー値が局所最大となる点を抽出(local_max_contours_xld)。 |
| `max_parallels_xld` | 最大距離までの平行輪郭群(max_parallels_xld)。 |
| `merge_cont_line_scan_xld` | ラインスキャン(帯状取得)の隣接フレーム輪郭端点を連結(merge_cont_line_scan_xld)。 |
| `mod_parallels_xld` | 平行輪郭の生成(パラメータ変更版)(mod_parallels_xld)。 |
| `moments_any_points_xld` | 輪郭点集合の面積・重心・2 次モーメント(moments_any_points_xld)。 |
| `segment_contour_attrib_xld` | 輪郭を、下地グレー値の属性が急変する点で分割(segment_contour_attrib_xld)。 |
| `segment_contours_xld` | 輪郭を直線分に分割(segment_contours_xld)。 |
| `symm_difference_closed_contours_xld` | 2 閉輪郭の対称差(symm_difference_closed_contours_xld)。 |
| `symm_difference_closed_polygons_xld` | 2 閉多角形の対称差(symm_difference_closed_polygons_xld)。 |
| `test_xld_point` | 点が閉輪郭の内部にあるか(交差数法)(test_xld_point)。 |
| `union2_closed_contours_xld` | 2 閉輪郭の和(union2_closed_contours_xld)。 |
| `union2_closed_polygons_xld` | 2 閉多角形の和(union2_closed_polygons_xld)。 |
| `union_cocircular_contours_xld` | 共円(同一円上)な輪郭を統合(union_cocircular_contours_xld)。 |
| `union_collinear_contours_ext_xld` | 共線統合(拡張パラメータ版)(union_collinear_contours_ext_xld)。 |
| `union_collinear_contours_xld` | 共線な輪郭断片を統合(union_collinear_contours_xld)。 |
| `union_cotangential_contours_xld` | 接線連続な輪郭を統合(union_cotangential_contours_xld)。 |
| `union_straight_contours_xld` | 直線的な輪郭を統合(union_straight_contours_xld)。 |

#### Calibration(34 op)

カメラ較正(内部・外部パラメータ、レンズ歪み)。「画素を mm に翻訳する」ための土台です(本編 14.4 の Brown 歪みモデルもここ)。

![Calibration の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_12_radial_distortion.png)
*図: レンズ歪みモデルの例(樽型/糸巻き型)(11.1.1 節より再掲)*

| op | 説明 |
|---|---|
| `affine_trans_point_3d` | 3D 点に 4x4 同次アフィン変換を適用(affine_trans_point_3d)。 |
| `binocular_calibration` | 左右カメラを Zhang で個別校正しステレオ相対姿勢を推定(binocular_calibration)。 |
| `calibrate_cameras` | Zhang 法カメラ校正(calibrate_cameras)。camera_calibration の別名。 |
| `calibrate_hand_eye` | ハンドアイ校正(calibrate_hand_eye)。hand_eye_calibration の別名。 |
| `caltab_points` | 校正板の理想マーク座標(ワールド, mm)を返す(caltab_points)。 |
| `cam_mat_to_cam_par` | 内部行列 K から fx, fy, cx, cy, skew を取り出す。 |
| `cam_par_pose_to_hom_mat3d` | カメラポーズ [rx,ry,rz(rad), tx,ty,tz] を 4x4 同次変換行列に変換(cam_par_pose_to_hom_mat3d)。 |
| `cam_par_to_cam_mat` | fx, fy, cx, cy, skew からピンホール内部行列 K を組み立てる。 |
| `camera_calibration` | Zhang 法で平面ターゲット多視点から内部行列 K を推定(camera_calibration)。 |
| `change_radial_distortion_cam_par` | カメラパラメータの放射歪み係数を kappa_new に置換(change_radial_distortion_cam_par)。 |
| `change_radial_distortion_image` | 画像に放射歪み r' = r(1 + kappa r^2) を適用して再サンプル(change_radial_distortion_image)。 |
| `change_radial_distortion_points` | 理想画素に半径・接線方向のレンズ歪みを与える(Brown モデル)。 |
| `contour_to_world_plane_xld` | XLD 輪郭(dict {cs:[Nx2]})を world 平面へ写す(contour_to_world_plane_xld)。 |
| `create_caltab` | 校正板の記述(理想点)を作る(create_caltab)。 |
| `create_pose` | 3D pose を生成する。 |
| `disp_caltab` | 校正板画像を返す(表示用)(disp_caltab)。 |
| `find_calib_object` | 校正オブジェクト(マーク)を検出(find_calib_object)。find_caltab の別名。 |
| `find_caltab` | 画像から校正板の円マーク中心を検出(連結成分の重心)(find_caltab)。 |
| `find_marks_and_pose` | マーク検出 + 校正板の姿勢推定(PnP 近似=平面ホモグラフィ)(find_marks_and_pose)。 |
| `gen_caltab` | 円マーク格子の校正板画像を生成(gen_caltab)。 |
| `gen_image_to_world_plane_map` | 画像→ワールド平面(z=0)の写像テーブルを生成(gen_image_to_world_plane_map)。 |
| `gen_radial_distortion_map` | 半径歪みの逆マップ(row_map, col_map)を生成(gen_radial_distortion_map)。 |
| `get_line_of_sight` | 画素 (row,col) の視線方向(正規化 3D ベクトル)を返す(get_line_of_sight)。 |
| `hand_eye_calibration` | 一連の運動対から AX=XB を解き X(4x4)を推定(hand_eye_calibration)。 |
| `image_points_to_world_plane` | カメラ内部/外部から画素を world 平面 z=0 へ逆投影(image_points_to_world_plane)。 |
| `image_to_world_plane` | 画像点を平面ホモグラフィで world 平面(z=0)へ写す(image_to_world_plane)。 |
| `project_3d_point` | 3D 点をカメラへ透視投影し画素 (row, col) を返す(project_3d_point)。 |
| `project_hom_point_hom_mat3d` | 同次 3D 点 (4,) を 3x4/4x4 行列で投影(project_hom_point_hom_mat3d)。 |
| `project_point_hom_mat3d` | 4x4 or 3x4 同次変換で 3D 点を変換し投影(project_point_hom_mat3d)。 |
| `projective_trans_point_2d` | 射影変換行列で同次 2D 点を射影する。 |
| `radial_distortion_self_calibration` | 本来直線であるべき点列の残差を最小化して半径歪み kappa を推定(plumb-line 法) |
| `radiometric_self_calibration` | 異なる露光の画像群からカメラ応答関数(逆応答 LUT)を推定 |
| `sim_caltab` | 校正板を指定カメラ姿勢で投影した画像をシミュレート(sim_caltab)。 |
| `stationary_camera_self_calibration` | 回転のみの無限遠ホモグラフィ H = K R K^-1 から内部行列 K を推定 |

#### morphology(33 op)

二値形態学(膨張・収縮・オープニング・クロージング)。ノイズ除去と形の整形の古典にして現役。

![morphology の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_06_opening_circle.png)
*図: オープニングの例(11.1.1 節より再掲)*

| op | 説明 |
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

点・線・円などの幾何プリミティブの当てはめと計算。計測結果を「図形の言葉」にする op 群。


![fops_geometry](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_geometry.png)
*図: geometry の実処理例 — 円周上の構造(ブラックホールのリング輝度、歯車の歯、年輪)は直線用のツールでは測れないが、polar_trans_image で極座標に展開すると横一列になり、1D プロファイルや直線検査がそのまま使える(Fullseye 実出力)。入力は EHT Collaboration の M87*(CC BY 4.0)+AI 生成画像(Gemini)2 種。*

| op | 説明 |
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

3D Gaussian Splatting 関連。多視点画像からの 3D 復元・レンダリング・メッシュ化という、この道具箱の最前線です。

| op | 説明 |
|---|---|
| `animate_mesh` | qpos 軌道で真値メッシュをアニメ再生(静的地形メッシュの合成も可) |
| `bin_pick_gif` | バラ積みされた部品を候補スコアリングで選び 6DoF IK で上面把持し bin から取り出す bin-picking を headless で GIF 化(GPU不要・成功数は部品が bin を出たかで実測) |
| `capture_orbit` | sim シーンをオービット撮影し 3DGS データセット(transforms.json)化 |
| `event_camera` | イベントカメラ(DVS)を対数輝度変化モデルで模倣し ON/OFF イベント列を生成。動くエッジに発火することを実測(GPU不要) |
| `evis_perceive` | GPU学習evisのロールアウト(qpos npy)をFullseyeで知覚: RGB/深度/DVSの3面GIF(ego_body=でロボット視点=頭部搭載RGB/深度/DVSの4面) |
| `figure8` | 差動旋回で 8 の字系の曲線を各サイズで描く旋回制御の練習/較正(俯瞰トラック、GPU不要) |
| `focus_stack` | 真値深度から被写界深度ボケの焦点スタックを生成し局所シャープネス最大で全焦点合成(焦点由来深度も復元、GPU不要) |
| `g1_perceive_real` | G1実機センサ仕様で知覚: Livox Mid-360(頭頂360°/-7..+52°)BEV点群 + RealSense D435i(87°×58°, 0.3-6m帯)RGB/深度の4面GIF。obstacles=True で歩行経路外に検証用の静的障害物を配置(センサに映る対象を用意) |
| `g1_training_curves` | G1学習ログの進捗行(step/reward/ep_len/perr/crash…)を配列辞書へパース — GPU機に触れず学習曲線をStudioでプロット |
| `g1_walk_policy` | GPU学習済みG1歩行方策(brax ckpt)をWindowsのみで実行: numpy推論(brax数値一致検証済)+ネイティブMuJoCoロールアウト→距離/生存/横ずれRMS実測+追従カメラ動画。vision=True で疑似LiDAR+障害物つき視覚歩行版 |
| `hurdle_physics` | go2 が助走→爆発跳躍で障害物(バリア)を越え向こう側へ着地する本物の物理の走幅跳をGIF＋軌道テレメトリ化(越えたか/自立かを実測、GPU不要) |
| `jump_physics` | go2 をしゃがみ→爆発伸展→弾道飛行(全足離地=接触0を実測)→着地させる本物の物理ジャンプをGIF＋高さテレメトリ化(跳躍高/滞空を実測、摩擦・重力込み、GPU不要) |
| `lidar_scan` | スピニング LIDAR を mj_ray の実レイキャストでシミュレートし点群を生成・可視化(GPU不要・命中率など実測) |
| `long_route` | go2 が粗さの変化する長い起伏地形を本物の物理で長距離(既定100m)歩き切る(距離/自立を実測、GPU不要) |
| `pick_gif` | ロボットアーム(Panda)が実接触・摩擦でキューブを把持し別位置へ設置する pick-and-place を headless で GIF 化(GPU不要・把持成否は箱の実測高さで判定) |
| `polarization` | 偏光カメラを Fresnel 順モデル(法線→DoLP/AoLP→4偏光画像→Stokes)で模倣。無テクスチャ面でも表面方位を偏光が符号化(透過/鏡面把持向け、GPU不要) |
| `pseudo_lidar` | 平面疑似LiDARスキャン(前方弧K本の正規化距離)。歩行方策G1VisionWalkの観測と同一ジオメトリのnumpy parity — 方策が食べる入力をツールとして単体計算 |
| `render_walk_gif` | walker を terrain 上に配置した運動学プレビューを headless で GIF 化(接触なし・motion/gait を可視化。物理歩行は walk_physics を使う) |
| `route_planning` | go2 が障害物をレイキャストで先読みし候補方位をピラミッド探索(粗→細)で選び差動旋回で回避してゴール到達する本物の物理ナビ(俯瞰プラン付き、GPU不要) |
| `sensor_fusion` | 位置センサ(カメラ/GPS)と速度センサ(IMU)を Kalman フィルタで融合し投射体を追跡。融合 RMSE を各センサ単体と正直に比較した図を生成(GPU不要) |
| `stereo_depth` | 平行2カメラのステレオペアを描画しブロックマッチングで深度推定、真値深度と誤差比較(既存 stereo.py 使用、GPU不要) |
| `sugar_mesh` | 3DGS を SuGaR 風に表面整列→Poisson でメッシュ抽出(真値 bbox 検証つき) |
| `train_3dgs` | sim シーンを native gsplat で 3DGS 学習(高速) |
| `train_3dgs_densify` | densify + SH + antialiased つき 3DGS 学習(高品質) |
| `tsdf_mesh` | sim 完全深度を TSDF 融合し清潔な watertight メッシュ化(GPU 不要・針無し) |
| `walk_physics` | go2 をトルク PD 制御＋閉ループバランス＋mj_step の本物の物理(重力・摩擦・接触・慣性)でラフな height field 上を歩かせ、胴体が傾く様子を GIF＋テレメトリ化(自立/前進/傾きを実測、GPU不要) |

#### Regions(26 op)

領域処理の HALCON 互換上位セット(region カテゴリの拡張版)。


![fops_regions](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_regions.png)
*図: Regions の実処理例 — 現場の二値画像は粒ノイズと穴だらけで、そのままラベリングすると誤計数する。opening_circle(オープニング)で粒を消し fill_up で穴を埋めてから連結成分に分けるのが領域処理の定石(Fullseye 実出力)。入力は AI 生成(Gemini)2 種+同梱サンプル 1 種の二値化+人工汚し。*

| op | 説明 |
|---|---|
| `difference` | 領域差 region \ sub(difference)。 |
| `find_neighbors` | 領域リストの隣接ペア index を返す(膨張して交差判定)(find_neighbors)。 |
| `gen_random_region` | ランダムな連結領域を生成(境界集積=正確な面積 + 連結性保証)(gen_random_region)。 |
| `gen_random_regions` | 複数のランダム領域を生成(gen_random_regions)。 |
| `gen_rectangle1` | 軸並行矩形領域を生成(gen_rectangle1)。 |
| `gen_region_histo` | 1D ヒストグラムを棒グラフ領域として描く(gen_region_histo)。 |
| `gen_region_hline` | 水平線分の領域を生成(gen_region_hline)。rows: 行 index の列。 |
| `gen_region_line` | 線分を region 化(gen_region_line、DDA)。 |
| `gen_region_points` | 個々の画素を region 化(gen_region_points)。 |
| `gen_region_polygon` | 多角形の輪郭を region 化(gen_region_polygon)。 |
| `gen_region_polygon_filled` | 多角形を塗りつぶして region 化(gen_region_polygon_filled)。 |
| `gen_region_runs` | 実行長符号 [(row, col_start, col_end), ...] から region を生成(gen_region_runs)。 |
| `get_region_points` | 領域画素の (row, col) 座標配列(get_region_points)。 |
| `get_region_polygon` | 領域外形の多角形近似頂点を返す(get_region_polygon)。 |
| `get_region_runs` | 領域のランレングス表現 [(row, col_start, col_end), ...](get_region_runs)。 |
| `hamming_distance` | 2 領域の Hamming 距離(異なる画素数)(hamming_distance)。 |
| `hamming_distance_norm` | 正規化 Hamming 距離(差分画素 / 和集合画素)(hamming_distance_norm)。 |
| `intersection` | 領域積(intersection)。 |
| `merge_regions_line_scan` | ラインスキャンのラン集合を連結して領域へ統合(merge_regions_line_scan)。 |
| `select_region_spatial` | 基準領域に対し指定空間関係を満たす領域を選ぶ(select_region_spatial)。 |
| `select_shape_proto` | プロトタイプ領域に形状特徴が近い領域を選ぶ(select_shape_proto)。 |
| `spatial_relation` | 2 領域の重心方向に基づく空間関係(above/below/left/right)(spatial_relation)。 |
| `symm_difference` | 対称差(symm_difference)。 |
| `test_equal_region` | 2 領域が等しいか(test_equal_region)。 |
| `test_subset_region` | region1 ⊆ region2 か(test_subset_region)。 |
| `union2` | 領域和(union2)。 |

#### contour(26 op)

輪郭(contour)の抽出・平滑化・分割・属性計算。


![fops_contour](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_contour.png)
*図: contour の実処理例 — 細い線状構造(血管・翅脈・葉脈・ひび割れ)はエッジ検出だと線の両側の縁が二重に出るが、lines_gauss(Frangi 稜線応答)で線状構造の帯を取り、skeleton で 1 画素幅の中心線に細線化する。血管も翅脈も葉脈もひびも同じ数学で測れる(Fullseye 実出力)。入力は全て AI 生成画像(Gemini)。医療風入力は診断用途ではない。*

| op | 説明 |
|---|---|
| `FindContours` | 2 値/レベルからの輪郭抽出(cv2.findContours、不在時 skimage、なければ numpy)  [backend=opencv] |
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

ランクフィルタ(メディアン等)。順序統計に基づくノイズ除去で、ごま塩ノイズの特効薬。

![rank の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_02_median_image.png)
*図: メディアンフィルタの例(11.1.1 節より再掲)*

| op | 説明 |
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
