#### Transformations(79 op)

画像の幾何変換(回転・スケール・射影・極座標など)。検査では「ワークの向きを揃えてから測る」の前段として毎回登場します。


![fops_transformations](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_transformations.png)
*図: Transformations の実処理例 — 斜め視点の平面はアフィン変換(6 自由度)では台形歪みが直らず、4 点対応から DLT で推定した射影変換(vector_to_proj_hom_mat2d → gen_image_warp_map)で初めて真上視点に整流できる(Fullseye 実出力)。1 段目は既知ホモグラフィの合成(真値あり)、2-3 段目は AI 生成画像(Gemini)。*

| op | 説明 |
|---|---|
| `affine_trans_pixel` | 画素 (row,col) にアフィン変換を適用(HALCON は (row,col) 順)。 |
| `affine_trans_point_2d` | 点列に任意の 2D アフィン変換を適用する。 |
| `axis_angle_to_quat` | 回転軸と角度から回転クォータニオンを作る。 |
| `convert_point_3d_cart_to_spher` | 3D 点の直交座標を球面座標へ変換する。 |
| `convert_point_3d_spher_to_cart` | 3D 点の球面座標を直交座標へ変換する。 |
| `convert_pose_type` | pose の並びを返す(genuine な型変換の簡易版=恒等で type タグを付す)。 |
| `dual_quat_compose` | 二重四元数の合成(剛体変換の合成、dual_quat_compose)。 |
| `dual_quat_conjugate` | 双対クォータニオンの共役を返す。 |
| `dual_quat_interpolate` | 二重四元数の補間(pose 経由で並進 lerp + 回転 slerp、dual_quat_interpolate)。 |
| `dual_quat_normalize` | 双対クォータニオンを正規化する。 |
| `dual_quat_to_hom_mat3d` | 単位二重四元数 [qr(4), qd(4)] を 4x4 剛体変換に(dual_quat_to_hom_mat3d)。 |
| `dual_quat_to_pose` | 双対クォータニオンを 3D pose 表現へ変換する。 |
| `dual_quat_to_screw` | 二重四元数からスクリュー成分(角度・並進・軸)を返す(dual_quat_to_screw)。 |
| `dual_quat_trans_line_3d` | 双四元数で 3D 直線を変換(点と方向を剛体変換)(dual_quat_trans_line_3d)。 |
| `dual_quat_trans_point_3d` | 単位双対クォータニオンで 3D 点を剛体変換する。 |
| `gen_image_warp_map` | 2D ホモグラフィから画素ワープマップ(逆写像)を生成(gen_image_warp_map)。 |
| `get_pose_type` | 3D pose の表現形式(回転の持ち方)を返す。 |
| `get_rectangle_pose` | 画像上の矩形から平面姿勢を推定(4 角対応 → homography → pose)(get_rectangle_pose)。 |
| `hom_mat2d_compose` | 2 つの 2D 同次変換行列を合成(積)する。 |
| `hom_mat2d_determinant` | 2D 同次変換行列の行列式を計算する。 |
| `hom_mat2d_identity` | 恒等 2D 変換の同次行列を作る。 |
| `hom_mat2d_invert` | 2D 同次変換行列の逆行列を求める。 |
| `hom_mat2d_reflect` | 2D 同次変換行列に鏡映を追加する。 |
| `hom_mat2d_reflect_local` | 2D 同次変換行列にローカル座標系での鏡映を追加する。 |
| `hom_mat2d_rotate` | 2D 同次変換行列に回転を追加する。 |
| `hom_mat2d_rotate_local` | 2D 同次変換行列にローカル座標系での回転を追加する。 |
| `hom_mat2d_scale` | 2D 同次変換行列に拡大縮小を追加する。 |
| `hom_mat2d_scale_local` | 2D 同次変換行列にローカル座標系での拡大縮小を追加する。 |
| `hom_mat2d_slant` | 2D 同次変換行列にせん断(スラント)を追加する。 |
| `hom_mat2d_slant_local` | 2D 同次変換行列にローカル座標系でのせん断を追加する。 |
| `hom_mat2d_to_affine_par` | 2D アフィン行列を (sx, sy, phi, theta, tx, ty) に分解。 |
| `hom_mat2d_translate` | 2D 同次変換行列に平行移動を追加する。 |
| `hom_mat2d_translate_local` | 2D 同次変換行列にローカル座標系での平行移動を追加する。 |
| `hom_mat2d_transpose` | 2D 同次変換行列を転置する。 |
| `hom_mat3d_compose` | 2 つの 3D 同次変換行列を合成(積)する。 |
| `hom_mat3d_determinant` | 3D 同次変換行列の行列式を計算する。 |
| `hom_mat3d_identity` | 恒等 3D 変換の同次行列を作る。 |
| `hom_mat3d_invert` | 3D 同次変換行列の逆行列を求める。 |
| `hom_mat3d_project` | 4x4 の透視投影行列で 3D 点を 2D 画像点へ(hom_mat3d_project)。 |
| `hom_mat3d_rotate` | 軸周りの右手系回転を左乗算(axis 0=x,1=y,2=z、標準の符号規約)。 |
| `hom_mat3d_rotate_local` | 3D 同次変換行列にローカル座標系での回転を追加する。 |
| `hom_mat3d_scale` | 3D 同次変換行列に拡大縮小を追加する。 |
| `hom_mat3d_scale_local` | 3D 同次変換行列にローカル座標系での拡大縮小を追加する。 |
| `hom_mat3d_to_pose` | 4x4 変換行列を pose [rx,ry,rz(ZYX euler), tx,ty,tz] に分解。 |
| `hom_mat3d_translate` | 3D 同次変換行列に平行移動を追加する。 |
| `hom_mat3d_translate_local` | 3D 同次変換行列にローカル座標系での平行移動を追加する。 |
| `hom_mat3d_transpose` | 3D 同次変換行列を転置する。 |
| `hom_vector_to_proj_hom_mat2d` | 4 点以上の対応から射影変換(homography, DLT)3x3 を求める(hom_vector_to_proj_hom_mat2d)。 |
| `point_line_to_hom_mat2d` | 点+方向の対応から 2D 剛体変換を推定(point_line_to_hom_mat2d)。 |
| `point_pluecker_line_to_hom_mat3d` | 点+Plücker 直線の対応から 3D 剛体変換を推定(point_pluecker_line_to_hom_mat3d)。 |
| `pose_average` | 複数の pose の平均 pose を求める。 |
| `pose_compose` | 2 つの 3D pose を合成する。 |
| `pose_invert` | 3D pose 列の各要素を逆変換にする。 |
| `pose_to_dual_quat` | 3D pose を単位双対クォータニオンへ変換する。 |
| `pose_to_hom_mat3d` | pose [rx,ry,rz(rad), tx,ty,tz] を 4x4 変換行列に(hom_mat3d_to_pose の逆)。 |
| `pose_to_quat` | 3D pose の回転成分をクォータニオンへ変換する。 |
| `proj_hom_mat2d_to_pose` | ホモグラフィと内部行列から平面の姿勢(R,t)を分解(proj_hom_mat2d_to_pose)。 |
| `projective_trans_hom_point_3d` | 同次 3D 点に 4x4 射影変換を適用(projective_trans_hom_point_3d)。 |
| `projective_trans_pixel` | 画素 (row,col) に射影変換を適用(HALCON (row,col) 順)。 |
| `projective_trans_point_3d` | 射影変換行列で 3D 点を射影する。 |
| `quat_compose` | 2 つのクォータニオンの積を計算する。 |
| `quat_conjugate` | クォータニオンの共役を返す。 |
| `quat_interpolate` | slerp 球面線形補間。 |
| `quat_normalize` | クォータニオンを正規化する。 |
| `quat_rotate_point_3d` | 単位クォータニオンで 3D 点を回転する。 |
| `quat_to_hom_mat3d` | クォータニオンを対応する回転行列へ変換する。 |
| `quat_to_pose` | クォータニオンを対応する 3D pose へ変換する。 |
| `screw_to_dual_quat` | スクリュー(軸方向 l, モーメント m, 回転角 theta, 並進 d)を二重四元数へ(screw_to_dual_quat)。 |
| `set_origin_pose` | 姿勢の原点を局所オフセットだけ移動(set_origin_pose)。 |
| `vector_angle_to_rigid` | 1 組の (点, 角度) から 2D 剛体変換を求める(vector_angle_to_rigid)。 |
| `vector_field_to_hom_mat2d` | ベクトル場全体に最も合うアフィン変換(2x3)を最小二乗推定(vector_field_to_hom_mat2d)。 |
| `vector_to_aniso` | 2D 点対応から異方性(非等方スケール)アフィン変換を推定(vector_to_aniso)。 |
| `vector_to_hom_mat2d` | 点対応から 2D ホモグラフィを推定(vector_to_hom_mat2d)。 |
| `vector_to_hom_mat3d` | 3D 点対応から剛体/相似変換(4x4)を Umeyama 推定(vector_to_hom_mat3d)。 |
| `vector_to_pose` | 6 組以上の 3D↔2D 対応から物体/カメラの 6 自由度 pose (R, t) を推定する(PnP)。 |
| `vector_to_proj_hom_mat2d` | 2D 点対応から射影変換(ホモグラフィ 3x3)を DLT 推定(vector_to_proj_hom_mat2d)。 |
| `vector_to_proj_hom_mat2d_distortion` | 歪み込みで射影変換を推定(歪みは小と仮定し DLT)(vector_to_proj_hom_mat2d_distortion)。 |
| `vector_to_rigid` | 対応点から 2D 剛体変換(回転+並進、Kabsch)を求める(vector_to_rigid)。 |
| `vector_to_similarity` | 対応点から 2D 相似変換(回転+スケール+並進、Umeyama)を求める(vector_to_similarity)。 |

#### features(77 op)

領域や輪郭から数値特徴(面積・周長・円形度・モーメントなど)を取り出す op 群。「画像を数字にする」計測の本丸です。

![features の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_13_area_center.png)
*図: 面積・重心計測の例(11.1.1 節より再掲)*

| op | 説明 |
|---|---|
| `ORB` | ORB キーポイント(cv2.ORB、不在時 Harris コーナー numpy)(features.ORB)。  [backend=opencv] |
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
| `describe_patches` | 各キーポイント周辺の輝度パッチを平均 0・ノルム 1 に正規化した記述子。 |
| `diameter_region` | features op(HALCON: diameter_region) |
| `diameter_xld` | features op(HALCON: diameter_xld) |
| `eccentricity` | features op(HALCON: eccentricity) |
| `eccentricity_xld` | features op(HALCON: eccentricity_xld) |
| `elliptic_axis` | features op(HALCON: elliptic_axis) |
| `elliptic_axis_xld` | features op(HALCON: elliptic_axis_xld) |
| `entropy_gray` | features op(HALCON: entropy_gray) |
| `estimate_noise` | features op(HALCON: estimate_noise) |
| `euler_number` | features op(HALCON: euler_number) |
| `fast_corners` | FAST 型のコーナーキーポイント検出(応答の強い順)。 |
| `get_region_thickness` | features op(HALCON: get_region_thickness) |
| `gray_histo_abs` | features op(HALCON: gray_histo_abs) |
| `harris_corners` | Harris コーナーキーポイント検出(応答の強い順)。 |
| `height_width_ratio` | features op(HALCON: height_width_ratio) |
| `hough_circle_trans` | features op(HALCON: hough_circle_trans) |
| `hough_line_trans` | features op(HALCON: hough_line_trans) |
| `intensity` | features op(HALCON: intensity) |
| `length_xld` | features op(HALCON: length_xld) |
| `match_descriptors` | 2 つの記述子集合を最近傍 + Lowe の比率テストで対応づける。 |
| `match_keypoints` | 2 画像間のキーポイント検出・記述・マッチングを一括で実行する。 |
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

二値領域(region)の生成・合成・選別。しきい値処理 → 連結成分 → 条件選別、が定番の 3 連携です。

![region の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_05_threshold_label.png)
*図: 二値化 → 連結成分ラベリングの例(11.1.1 節より再掲)*

| op | 説明 |
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
| `r2_inner_circle` | 最大内接円をマスクとして描く(a で描画半径を拡縮、a=0.5 で厳密)。 |
| `r2_inner_rectangle1` | 最大の軸平行内接矩形(a で描画矩形を縮小、a=0 で厳密)。 |
| `r2_partition_rectangle` | 領域の外接矩形を N×N 格子に分割し、領域と重なるセルだけ残す。 |
| `r2_runlength_features` | 領域→特徴量: 水平方向の前景ラン長の平均。 |
| `r2_smallest_circle` | 最小包含円をマスクとして描く(Welzl 法、a で半径を拡大)。 |
| `r2_smallest_rectangle1` | 軸平行の外接矩形(バウンディングボックス)。 |
| `r2_smallest_rectangle2` | 面積最小の有向外接矩形をマスク化(回転キャリパー法)。 |
| `r2_sort_region` | k 番目に大きい連結成分だけ残す(k = round(a*(n-1)))。 |
| `r2_split_skeleton_lines` | 領域を細線化して骨格にし、分岐点(近傍 3 以上)で切り分ける。 |
| `r2_union1` | 全連結成分を 1 つのマスクへ統合(ラベルの OR)。 |
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

画像の生成・入出力・チャンネル操作・算術合成など、画像そのものを扱う基礎 op 群。


![fops_image_chapter](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_image_chapter.png)
*図: Image の実処理例 — decompose3 でカラー画像を R/G/B チャネルに分解。チャネルごとに写る情報が違う(眼底では血管と背景のコントラスト配分がチャネルで大きく変わる)(Fullseye 実出力)。入力は scikit-image 同梱 retina+AI 生成画像(Gemini)2 種。診断用途ではなく画像処理デモ。*

| op | 説明 |
|---|---|
| `add_channels` | gray 画像を base 画像へチャネルとして追加(add_channels)。 |
| `append_channel` | 多チャネル画像に 1 チャネルを追記(append_channel)。 |
| `area_center_gray` | グレー値を重みとした面積(質量)と重心 (row,col)(area_center_gray)。 |
| `change_domain` | 画像の domain(ROI)を region に変更(領域外を 0 マスク)(change_domain)。 |
| `channels_to_image` | 2D チャネルのリスト/列を多チャネル画像へ(channels_to_image)。 |
| `complex_to_real` | 複素画像を実部/虚部へ分解(complex_to_real)。 |
| `compose2` | 2 枚の画像を 2 チャネル画像にまとめる。 |
| `compose3` | 3 枚の画像を 3 チャネル画像にまとめる。 |
| `compose4` | 4 枚の画像を 4 チャネル画像にまとめる。 |
| `compose5` | 5 枚の画像を 5 チャネル画像にまとめる。 |
| `compose6` | 6 枚の画像を 6 チャネル画像にまとめる。 |
| `compose7` | 7 枚の画像を 7 チャネル画像にまとめる。 |
| `cooc_feature_matrix` | GLCM から Haralick 特徴(energy/contrast/correlation/homogeneity)(cooc_feature_matrix)。 |
| `crop_domain_rel` | domain 外接矩形を相対マージン付きで切り出す(crop_domain_rel)。 |
| `crop_rectangle2` | 回転矩形 (row,col,phi,l1,l2) を切り出し軸並行化(crop_rectangle2)。 |
| `decompose2` | 2 チャネル画像を 2 枚の画像に分解する。 |
| `decompose3` | 3 チャネル画像を 3 枚の画像に分解する。 |
| `decompose4` | 4 チャネル画像を 4 枚の画像に分解する。 |
| `decompose5` | 5 チャネル画像を 5 枚の画像に分解する。 |
| `decompose6` | 6 チャネル画像を 6 枚の画像に分解する。 |
| `decompose7` | 7 チャネル画像を 7 枚の画像に分解する。 |
| `elliptic_axis_gray` | グレー値重み 2 次モーメントの等価楕円 (ra, rb, phi)(elliptic_axis_gray)。 |
| `fuzzy_entropy` | 領域グレー分布の Shannon エントロピー(fuzzy_entropy)。 |
| `fuzzy_perimeter` | グレー勾配総和による fuzzy 周長(fuzzy_perimeter)。 |
| `gen_cooc_matrix` | グレー共起行列 (GLCM)(gen_cooc_matrix)。direction=0/45/90/135 度。 |
| `gen_image1` | 1 チャネル配列から画像を作る(gen_image1)。 |
| `gen_image1_extern` | 外部メモリ(1D/2D)から 1 チャネル画像を構成(gen_image1_extern)。 |
| `gen_image1_rect` | 画像から矩形領域を切り出す(gen_image1_rect)。 |
| `gen_image3` | 3 チャネル配列から (H,W,3) 画像を作る(gen_image3)。 |
| `gen_image3_extern` | 外部メモリ(interleaved)から 3 チャネル画像を構成(gen_image3_extern)。 |
| `gen_image_const` | 定数値で満たした画像(gen_image_const)。 |
| `gen_image_gray_ramp` | 線形傾斜画像 g = alpha*(c-cx)+beta*(r-cy)+mean(gen_image_gray_ramp)。 |
| `gen_image_interleaved` | 画素インタリーブ 1D 配列を (H,W,C) 画像へ復元(gen_image_interleaved)。 |
| `gen_image_surface_first_order` | 1 次サーフェス画像 g = alpha*(c-col0)+beta*(r-row0)+gamma(gen_image_surface_first_order)。 |
| `gen_image_surface_second_order` | 2 次サーフェス画像 g = a*x^2+b*x*y+c*y^2+d*x+e*y+f(gen_image_surface_second_order)。 |
| `get_grayval` | (row,col) のグレー値を返す(最近傍)(get_grayval)。 |
| `get_grayval_interpolated` | (row,col) の双一次補間グレー値(get_grayval_interpolated)。 |
| `gray_features` | 領域のグレー特徴(mean/deviation/min/max/median/area)(gray_features)。 |
| `gray_histo` | グレーヒストグラム(絶対度数と相対度数)(gray_histo)。 |
| `gray_histo_range` | 指定レンジのグレーヒストグラム(gray_histo_range)。 |
| `gray_projections` | 行方向/列方向のグレー投影(gray_projections)。 |
| `histo_2dim` | 2 チャネルの 2 次元ヒストグラム(histo_2dim)。 |
| `image_to_channels` | 多チャネル画像を個々のチャネルへ分ける(image_to_channels)。 |
| `interleave_channels` | チャネルを画素インタリーブ配置の 1 本の配列へ(interleave_channels)。 |
| `moments_gray_plane` | 1 次グレーモーメント(平面近似係数 alpha,beta,mean)(moments_gray_plane)。 |
| `overpaint_gray` | paint_gray と同義で source を重ね描き(overpaint_gray)。 |
| `overpaint_region` | paint_region と同義で領域を重ね塗り(overpaint_region)。 |
| `paint_gray` | source 画像のグレー値を(領域内で)image へ転写(paint_gray)。 |
| `paint_region` | 領域を定数グレー値で塗る(paint_region)。 |
| `paint_xld` | XLD 輪郭を画像へ描画(paint_xld)。 |
| `real_to_complex` | 実部/虚部画像を複素画像へ合成(real_to_complex)。 |
| `real_to_vector_field` | 2 枚の実画像を (H,W,2) ベクトル場へ合成(real_to_vector_field)。 |
| `select_gray` | グレー特徴が [minv,maxv] に入る領域だけ選ぶ(select_gray)。regions=bool mask のリスト。 |
| `shape_histo_all` | しきい値を掃引して各レベルの領域面積を集めた形状ヒストグラム(shape_histo_all)。 |
| `shape_histo_point` | 指定点を含む連結領域の面積をしきい値ごとに集める(shape_histo_point)。 |
| `tile_channels` | 多チャネルを 1 枚のグレー画像へタイル配置(tile_channels)。 |
| `tile_images` | 同サイズ画像群をグリッドにタイル(tile_images)。 |
| `tile_images_offset` | 各画像を offset (row,col) に貼り付けて合成(tile_images_offset)。 |
| `vector_field_to_real` | ベクトル場 (H,W,2) を row/col 成分画像へ分解(vector_field_to_real)。 |

#### Filters(58 op)

空間フィルタ全般。平滑化・鮮鋭化・微分系など、画素近傍の畳み込みで画像を整える一群です。

![Filters の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_01_gauss_image.png)
*図: ガウス平滑化の例(11.1.1 節より再掲)*

| op | 説明 |
|---|---|
| `abs_diff_image` | /image1-image2/*mult(abs_diff_image)。 |
| `add_image` | (image1+image2)*mult+add(add_image)。 |
| `apply_color_trans_lut` | RGB (H,W,3) を LUT の色空間へ変換(apply_color_trans_lut)。rgb_to_hsv / rgb_to_yuv 等。 |
| `atan2_image` | atan2(image1, image2)(vector field の角度、atan2_image)。 |
| `bit_and` | 整数化した画素のビット AND(bit_and)。 |
| `bit_not` | ビット反転(bit_not)。 |
| `bit_or` | ビット OR(bit_or)。 |
| `bit_xor` | ビット XOR(bit_xor)。 |
| `clear_color_trans_lut` | 色変換 LUT を破棄(clear_color_trans_lut)。 |
| `convert_map_type` | マップ/画像の型変換(convert_map_type)。 |
| `convol_channels` | 多チャネル画像を各チャネル畳み込み(convol_channels)。image=(H,W,C) or 2D。 |
| `convol_fft` | FFT による線形畳み込み(convol_fft/convol_image)。 |
| `convol_image` | 空間畳み込み(convol_image)。 |
| `correlation_fft` | FFT による相互相関(correlation_fft)。 |
| `create_color_trans_lut` | 色変換 LUT(変換種別)を作る(create_color_trans_lut)。 |
| `crop_domain` | domain の外接矩形で画像を切り出す(crop_domain)。 |
| `derivate_vector_field` | ベクトル場の発散/回転/ヤコビアンを計算(derivate_vector_field)。 |
| `deviation_n` | 画像スタックの画素標準偏差(deviation_n)。 |
| `div_image` | image1/image2*mult+add(div_image)。0 除算は保護。 |
| `energy_gabor` | Gabor 実/虚応答からエネルギー(振幅二乗)(energy_gabor)。 |
| `exhaustive_match` | 全探索 NCC の最良一致(find_ncc_model と同核、error=1-score も返す)。 |
| `exhaustive_match_mg` | マルチグリッド全探索テンプレートマッチ(粗密で高速化)(exhaustive_match_mg)。 |
| `gauss_distribution` | 正規分布の確率密度テーブル(gauss_distribution)。ノイズモデル用。 |
| `gen_canonical_variates_trans` | クラス付き多チャネル画像から正準変量(LDA)変換を求める(gen_canonical_variates_trans)。 |
| `gen_filter_mask` | 任意係数のフィルタマスクを生成(gen_filter_mask)。 |
| `gen_gauss_filter` | 正規化 2D ガウスフィルタマスク(gen_gauss_filter)。 |
| `gen_mean_filter` | 平均(box)フィルタマスク(gen_mean_filter)。 |
| `gen_principal_comp_trans` | 多チャネル画像群から主成分変換(固有ベクトル/固有値)を求める(gen_principal_comp_trans)。 |
| `gen_psf_defocus` | 円形ボケ(デフォーカス)PSF(gen_psf_defocus)。 |
| `gen_psf_motion` | 直線ブラー(モーション)PSF(gen_psf_motion)。 |
| `gen_savitzky_golay_filter` | Savitzky-Golay 平滑/微分 1D フィルタ係数(gen_savitzky_golay_filter)。 |
| `gen_sin_bandpass` | 正弦窓の周波数帯域通過マスク(gen_sin_bandpass)。 |
| `gen_std_bandpass` | Butterworth 型の帯域通過マスク(gen_std_bandpass)。 |
| `harmonic_interpolation` | 穴(region=True)を Laplace 方程式(調和関数)で埋める(harmonic_interpolation)。 |
| `inpainting_aniso` | 異方性拡散(Perona-Malik)で欠損領域を修復(inpainting_aniso)。 |
| `inpainting_ced` | コヒーレンス強調拡散(構造テンソル方向へ拡散)でインペイント(inpainting_ced)。 |
| `inpainting_ct` | コヒーレンス輸送に近い等方拡散インペイント(inpainting_ct)。 |
| `inpainting_mcf` | 平均曲率流(Mean Curvature Flow)インペイント(inpainting_mcf)。 |
| `inpainting_texture` | テクスチャ合成インペイント(近傍既知パッチのコピー)(inpainting_texture)。 |
| `map_image` | LUT (map) を画素に適用(map_image)。map は長さ N の 1D 配列。 |
| `max_image` | 画素ごとの最大(max_image)。 |
| `mean_n` | 画像スタックの画素平均(mean_n)。 |
| `midrange_image` | 局所 (min+max)/2 の midrange フィルタ(midrange_image)。 |
| `min_image` | 画素ごとの最小(min_image)。 |
| `mult_image` | image1*image2*mult+add(mult_image)。 |
| `noise_distribution_mean` | 複数観測から画素ごとノイズ標準偏差の平均を推定(noise_distribution_mean)。 |
| `optical_flow_mg` | マルチグリッド(粗密ピラミッド + warping)Horn-Schunck 密オプティカルフロー |
| `phase_correlation_fft` | 位相相関で並進 (drow, dcol) を推定(phase_correlation_fft)。 |
| `points_sojka` | Sojka の勾配共分散に基づくコーナー応答でサブピクセルコーナーを抽出 |
| `rank_n` | 画像スタックの画素 rank 値(順位統計、rank_n)。既定は中央値。 |
| `scene_flow_calib` | 校正済シーンフロー(内部行列で 3D 変位をメトリック化)(scene_flow_calib)。 |
| `scene_flow_uncalib` | 左右 2 時刻の画像から 3D シーンフロー(未校正近似)を推定(scene_flow_uncalib)。 |
| `sp_distribution` | salt-and-pepper ノイズ分布(両端に質量、中央一様)(sp_distribution)。 |
| `sub_image` | (image1-image2)*mult+add(sub_image)。 |
| `unwarp_image_vector_field` | ベクトル場に沿って画像をワープ(逆マッピング)(unwarp_image_vector_field)。 |
| `vector_field_length` | ベクトル場の各点の大きさ(vector_field_length)。 |
| `wiener_filter` | Wiener デコンボリューション(wiener_filter)。 |
| `wiener_filter_ni` | 非反復 Wiener 復元(wiener_filter_ni)。 |

#### edges(56 op)

エッジ(輪郭)検出。Sobel 系の勾配から Canny の細線化まで。計測の基準線は大抵ここから生まれます。

![edges の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_04_canny.png)
*図: Canny エッジ検出の例(11.1.1 節より再掲)*

| op | 説明 |
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

画像を意味のある領域に切り分けるセグメンテーション。しきい値系から分水嶺(watershed)まで。

![segmentation の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_14_watersheds.png)
*図: 分水嶺法の例(11.1.1 節より再掲)*

| op | 説明 |
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

平滑化専門の一群。ガウス・バイラテラル・異方性拡散など「ノイズは消すがエッジは守る」系の使い分けが肝です。


![fops_smoothing](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_smoothing.png)
*図: smoothing の実処理例 — 同じ雑音入力に対し、ガウス平滑化は輪郭ごとぼかすが、anisotropic_diffusion(異方性拡散)はエッジをまたがずに拡散するため輪郭を保ったまま雑音だけをならす(Fullseye 実出力)。入力は skimage camera+AI 生成画像(Gemini)2 種。*

| op | 説明 |
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
