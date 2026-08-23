#### camera(22 op)

カメラモデルと投影計算。3D と 2D を往復する変換群です。

| op | 説明 |
|---|---|
| `SolvePnP` | 3D-2D 対応からカメラ姿勢を推定(cv2.solvePnP、不在時 numpy)(camera.SolvePnP)。  [backend=opencv] |
| `backproject` | 画素 (N,2) を深度でカメラ座標系の 3D 点へ持ち上げる(逆投影)。 |
| `decompose_essential` | 基本行列 E を 4 通りの相対 pose 候補に分解する。 |
| `decompose_intrinsics` | 内部行列 K から fx, fy, cx, cy, skew を取り出す。 |
| `depth_to_points` | 深度マップ全体をカメラ座標系の点群へ逆投影する。 |
| `distort_points` | 理想画素に半径・接線方向のレンズ歪みを与える(Brown モデル)。 |
| `epipolar_lines` | 基礎行列を介して対応点が誘導するエピポーラ線を計算する。 |
| `essential_from_fundamental` | E = K2^T·F·K で基礎行列を基本行列へ変換する。 |
| `essential_matrix` | 較正済みペアの 8 組以上の対応から基本行列 E を推定する。 |
| `fundamental_matrix` | 8 組以上の対応から正規化 8 点法で基礎行列 F を推定する。 |
| `intrinsic_matrix` | ピンホール内部行列 K を組み立てる。 |
| `normals_from_depth` | 整列済み深度マップから画素ごとの法線 (H,W,3) を推定する。 |
| `project_points` | ワールド点 (N,3) を画素へ射影し (uv, depth) を返す。 |
| `projection_matrix` | 3x4 射影行列 P = K·[R t] を組み立てる(R, t は省略可)。 |
| `recover_pose` | 基本行列の分解候補から物理的に正しい相対 pose を選ぶ。 |
| `reprojection_error` | 点ごとの再投影誤差 [px] を計算する。 |
| `rodrigues` | 回転ベクトル(軸×角)を回転行列へ(Rodrigues の公式)。 |
| `rotation_log` | 回転行列を回転ベクトルへ(rodrigues の逆)。 |
| `solve_pnp` | 6 組以上の 3D↔2D 対応から 6 自由度 pose を推定する(PnP)。 |
| `stereo_rectify` | 較正済みステレオペアの平行化回転を計算する(Fusiello 法)。 |
| `triangulate` | 2 視点の対応画素の線形 DLT 三角測量。 |
| `undistort_points` | 半径・接線方向の歪みを除去する(distort_points の逆)。 |

#### texture(21 op)

テクスチャ(肌理)解析。Laws エネルギーや Gabor など、「模様の質感」を数値化します。

![texture の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_10_texture_laws.png)
*図: Laws テクスチャエネルギーの例(11.1.1 節より再掲)*

| op | 説明 |
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

周波数領域処理(FFT・フィルタリング)。画像を波の重ね合わせとして扱う視点です。

![frequency の例](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_08_fft_image.png)
*図: FFT スペクトルの例(11.1.1 節より再掲)*

| op | 説明 |
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

点群のセグメンテーション(平面抽出・クラスタリング等)。

| op | 説明 |
|---|---|
| `aabb` | 点群の軸平行バウンディングボックス (min, max) を返す。 |
| `centroid` | 点群の重心を返す。 |
| `crop_box` | 軸平行ボックス [lo, hi] 内の点だけ残す。 |
| `crop_sphere` | 中心から radius 以内の点だけ残す(点とマスクを返す)。 |
| `curvature` | k 近傍の固有値から点ごとの曲率(表面変化率)を計算する。 |
| `euclidean_clusters` | ユークリッドクラスタリングで近接点をグループ化する(Rusu 2009)。 |
| `farthest_point_sampling` | 最遠点サンプリングで空間的に散らばった k 点を選ぶ。 |
| `fit_cylinder_ransac` | 点+法線サンプルから RANSAC で円柱をロバストにフィットする。 |
| `fit_plane` | 全点に対する全最小二乗平面フィット(PCA)。 |
| `fit_plane_ransac` | RANSAC で支配平面をロバストにフィットする。 |
| `fit_sphere_ransac` | RANSAC で球をロバストにフィットする(中心・半径・インライアを返す)。 |
| `height_above_plane` | 平面の法線方向に沿った各点の高さ(符号つき距離)。 |
| `obb` | PCA による有向バウンディングボックス。 |
| `plane_distance` | 平面 [a,b,c,d] への各点の符号つき距離。 |
| `principal_axes` | 点群の主成分分析(固有値と固有ベクトルを返す)。 |
| `region_growing` | 滑らかさ制約つき領域成長でクラスタ分割する(Rabbani 2006)。 |
| `remove_ground` | 支配平面を RANSAC で当てて点群を地面/非地面に分ける。 |

#### specops(16 op)

疑似センサ・知覚系の特殊 op(疑似 LiDAR、1 次元イベントカメラ、実機センサ再現など、本編 6 章・9 章の主役たち)。

| op | 説明 |
|---|---|
| `read_envi` | ENVI ハイパースペクトルキューブを読み込む(cube, meta)。 |
| `spec_angle_mapper` | 参照スペクトルとの画素ごとのスペクトル角 [rad](SAM)。 |
| `spec_band` | キューブの第 i バンドを 1 枚の画像として取り出す。 |
| `spec_band_ratio` | 画素ごとのバンド比 band_i/(band_j+eps) を計算する。 |
| `spec_continuum_removal` | コンティニュアム除去(各スペクトルを上包絡線で割る)。 |
| `spec_decorrelation_stretch` | 相関除去ストレッチで色の違いを強調する(decorrelation stretch)。 |
| `spec_endmembers_ppi` | Pixel Purity Index によるエンドメンバーの近似抽出。 |
| `spec_fuse` | 位置合わせ済みの単バンド画像群を 1 枚に融合する。 |
| `spec_index` | 正規化差分指数 (a-b)/(a+b+eps)(NDVI 型)。 |
| `spec_mnf` | 最小ノイズ比率変換(MNF)。 |
| `spec_nearest_band` | 指定波長に最も近いバンドの index を返す。 |
| `spec_pansharpen` | 高解像度パンクロバンドでマルチスペクトルをパンシャープン化する。 |
| `spec_pca` | スペクトル軸方向の主成分分析。 |
| `spec_rgb_composite` | 選んだ 3 バンドから表示用 RGB 合成画像を作る。 |
| `spec_unmix` | 線形スペクトル分解で画素ごとの存在比マップを推定する。 |
| `write_envi` | ENVI キューブを書き出す(.hdr + .img)。 |

#### 3D Matching(15 op)

| op | 説明 |
|---|---|
| `create_cam_pose_look_at_point` | カメラ位置と注視点から look-at 姿勢(4x4)を構築(create_cam_pose_look_at_point)。 |
| `create_deformable_surface_model` | 変形 surface モデルを作る(PPF ベース)(create_deformable_surface_model)。 |
| `create_shape_model_3d` | 3D 点群から複数視点のシルエット shape モデルを作る(create_shape_model_3d)。 |
| `create_surface_model` | モデル点群の Point Pair Feature 記述子(ハッシュ表)を構築する。 |
| `find_box_3d` | 点群から軸並行境界箱(OBB 近似=PCA 箱)を検出(find_box_3d)。 |
| `find_deformable_surface_model` | 変形 surface モデルをシーン点群から検出(PPF + ICP refine)(find_deformable_surface_model)。 |
| `find_shape_model_3d` | 3D shape モデルを画像から検出(投影シルエットと相関)(find_shape_model_3d)。 |
| `find_surface_model` | PPF 投票 + ICP 精緻化でシーン中のモデル 6 自由度 pose を探す。 |
| `find_surface_model_image` | 深度画像を点群化して surface モデルを検出(find_surface_model_image)。 |
| `project_shape_model_3d` | 3D モデルをカメラへ投影しエッジ画像を生成(project_shape_model_3d)。 |
| `reduce_domain` | domain を region へ縮小(reduce_domain)。change_domain と同義の facade。 |
| `refine_deformable_surface_model` | 変形 surface モデルを検出 → ICP で精緻化(refine_deformable_surface_model)。 |
| `refine_surface_model_pose` | 初期姿勢から ICP で surface モデル姿勢を精緻化(refine_surface_model_pose)。 |
| `refine_surface_model_pose_image` | 深度画像から点群化し ICP で姿勢精緻化(refine_surface_model_pose_image)。 |
| `trans_pose_shape_model_3d` | 3D モデルに姿勢(4x4)を適用(trans_pose_shape_model_3d)。 |

#### videops(15 op)

動画・時系列処理(フレーム間差分、トラッキング等)。

| op | 説明 |
|---|---|
| `background_subtraction` | 時間中央値の背景モデルでフレームごとの前景マスクを得る。 |
| `flicker_reduce` | フレーム間の全体輝度のちらつき(フリッカ)を除去する。 |
| `frame_difference` | 隣接フレームの絶対差分で動き量ボリュームを得る。 |
| `motion_energy` | 時間方向の変化量を積算した動きエネルギーマップ (H,W)。 |
| `moving_average` | 時間方向の移動平均(ボックス)平滑化。 |
| `optical_flow_sequence` | 隣接フレーム間のフロー強度ボリューム (T-1,H,W)。 |
| `per_frame` | 2D op を各フレームへ独立に適用する。 |
| `spatiotemporal_gaussian` | (t,y,x) の分離型 3D ガウス平滑化。 |
| `spatiotemporal_sobel` | (t,y,x) の 3D Sobel 勾配強度。 |
| `temporal_gradient` | 中心差分による時間微分 d(video)/dt。 |
| `temporal_max` | 時間方向の最大値投影 (H,W)。 |
| `temporal_mean` | 画素ごとの時間平均 (H,W)。 |
| `temporal_median` | 画素ごとの時間中央値 (H,W)。 |
| `temporal_min` | 時間方向の最小値投影 (H,W)。 |
| `temporal_std` | 画素ごとの時間標準偏差 = 活動マップ (H,W)。 |

#### Segmentation(14 op)


![fops_segmentation_facade](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_segmentation_facade.png)
*図: Segmentation の実処理例 — 琥珀の中の虫: 強い橙の色かぶり+半透明散乱+気泡・割れの妨害から、最暗部二値化 → opening → 画像縁に接する成分(縁影・割れ)の除外 → 最大成分、の固定パイプラインで虫本体を抜く(Fullseye 実出力)。試行過程の honest 記録: B チャネル+clahe 前処理は琥珀の内部テクスチャを増幅して逆効果だった(clahe が常に正解ではない)。入力は全て AI 生成画像(Gemini)。*

| op | 説明 |
|---|---|
| `check_difference` | 基準画像との差が tol を超える画素を領域として返す(check_difference)。 |
| `class_2dim_sup` | 2 チャネル特徴空間で ref_region の分布に入る画素を分類(教師つき)(class_2dim_sup)。 |
| `class_2dim_unsup` | 2 チャネル特徴空間を k-means で教師なし分類(class_2dim_unsup)。ラベル画像を返す。 |
| `class_ndim_norm` | ND 特徴画像を学習済み正規分布クラスで分類(Mahalanobis 距離 < thresh)(class_ndim_norm)。 |
| `classify_image_class_gmm` | ガウス混合モデルで多チャネル特徴画像を画素分類(classify_image_class_gmm)。 |
| `classify_image_class_knn` | k-NN で多チャネル特徴画像を画素分類(classify_image_class_knn)。 |
| `classify_image_class_lut` | グレー LUT による画素分類(閾値/ラベル LUT)(classify_image_class_lut)。 |
| `classify_image_class_mlp` | 学習済み MLP で多チャネル特徴画像を画素分類(classify_image_class_mlp)。 |
| `classify_image_class_svm` | 学習済み線形 SVM で多チャネル特徴画像を画素分類(classify_image_class_svm)。 |
| `expand_gray` | seed から gray 類似(/Δ/<tol)で領域を膨張(expand_gray)。 |
| `expand_gray_ref` | 参照画像のグレー類似で seed を膨張(expand_gray_ref)。 |
| `learn_ndim_norm` | 特徴ベクトル群から正規分布クラス(平均・共分散)を学習(learn_ndim_norm)。 |
| `regiongrowing_n` | 多チャネル特徴の類似性で画像全体を領域分割(regiongrowing_n)。ラベル画像を返す。 |
| `watersheds_marker` | マーカー制御 watershed 分割(watersheds_marker)。markers: int ラベル画像(0=未割当)。 |

#### extra(14 op)

| op | 説明 |
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

ステレオ視差からの距離推定。両眼の三角測量です(本編 14.4 参照)。

| op | 説明 |
|---|---|
| `BlockMatching` | ブロックマッチング視差(cv2.StereoBM、不在時 fullseye numpy)(stereo.BlockMatching)。  [backend=opencv] |
| `SGBM` | Semi-Global BM 視差(cv2.StereoSGBM、不在時 fullseye SGM numpy)(stereo.SGBM)。  [backend=opencv] |
| `census_transform` | Census 変換: 近傍との大小関係で各画素を符号化する。 |
| `depth_from_disparity` | 視差から計量深度 Z = f·B/d を計算する。 |
| `disparity_census` | Census + ハミング距離の勝者総取りで密な視差を推定する。 |
| `disparity_confidence` | コスト曲線から画素ごとのマッチング信頼度 [0,1] を推定(PKRN 型)。 |
| `disparity_map` | 勝者総取りブロックマッチングによる密な視差推定。 |
| `disparity_sgm` | Semi-Global Matching 視差(Hirschmüller 法)。 |
| `disparity_subpixel` | 放物線フィットで視差をサブピクセルへ精緻化する。 |
| `fill_disparity` | 無効視差を行方向の補間で埋める(背景寄りに補間)。 |
| `lr_consistency` | 左右一致チェックのマスク(True = 信頼できる視差)。 |
| `reproject_to_points` | 深度マップをカメラ座標系の点群 (N,3) へ逆投影する。 |
| `speckle_filter` | 視差マップから小さなスペックル領域を除去する。 |

#### terrain(13 op)

| op | 説明 |
|---|---|
| `detect_obstacles` | 歩行可能地面から clearance 以上せり上がるセルを障害物として分割する。 |
| `elevation_map` | 点群を 2.5D 標高グリッドへビン詰めする。 |
| `fill_gaps` | nan セルを最近傍の有効高さで埋める。 |
| `foothold_candidates` | 地形から離散的な安全足場候補を選ぶ。 |
| `foothold_score` | セルごとの平坦度スコア [0,1](1 = 平坦で水平 = 良い足場)。 |
| `fuse_elevation` | 位置合わせ済みの標高グリッド群をロボット中心の 1 枚に融合する。 |
| `ground_plane` | セル単位のロバスト最小二乗で地面平面 z = ax+by+c を推定する。 |
| `ground_surface` | グレーオープニングで滑らかな歩行可能地面の包絡面を得る。 |
| `roughness_map` | セルごとの粗さ = 局所高さの標準偏差。 |
| `slope_map` | セルごとの斜度 = 水平からの表面角度。 |
| `step_edges` | 高さマップから段差エッジ(縁石・階段の踏み外し線)を検出する。 |
| `surface_normals` | セルごとの上向き単位法線 (H,W,3)。 |
| `traversability` | 段差と斜度の上限から通行可能マスクを作る。 |

#### artificial-life(12 op)

| op | 説明 |
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

| op | 説明 |
|---|---|
| `cx_apply_transfer_function` | 中心化スペクトルにフィルタ H を乗じる(伝達関数の適用)。 |
| `cx_bandpass` | 周波数領域の理想円環バンドパスフィルタ。 |
| `cx_fft` | 実画像の中心化 2D FFT(複素スペクトル)。 |
| `cx_from_mag_phase` | 振幅とラジアン位相から複素場を再構成する。 |
| `cx_ifft` | cx_fft の逆変換(ifft2 + ifftshift)。 |
| `cx_imag` | 複素場の虚部を実画像として返す。 |
| `cx_log_magnitude` | 表示用の対数振幅スペクトル [0,1]。 |
| `cx_magnitude` | 画素ごとの複素振幅(絶対値)を返す。 |
| `cx_phase` | 複素場のラップされた位相を返す。 |
| `cx_real` | 複素場の実部を実画像として返す。 |
| `cx_wiener_deconvolve` | 周波数領域 Wiener デコンボリューションで画像を復元する。 |
| `phase_unwrap` | 2D 位相アンラップ(ラップ位相→連続位相)。 |

#### restoration(12 op)


![fops_restoration](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_restoration.png)
*図: restoration の実処理例 — モーションブラーは畳み込みなので、輪郭強調(unsharp)では復元できず、ブラー PSF を仮定した iv_motion_deblur(Wiener 逆畳み込み)で初めて文字が読めるまで戻る(Fullseye 実出力)。ブレは線形モーション PSF(L=9px, 0°)を畳み込んで付与(convol_fft)。入力は skimage page/camera+AI 生成画像(Gemini)。*

| op | 説明 |
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

| op | 説明 |
|---|---|
| `boundary_edges` | メッシュの開いた縁のエッジ一覧 (M,2) を返す。 |
| `components` | メッシュを連結成分に分割する。 |
| `convex_hull` | 点集合の凸包メッシュ(外向き三角形)を作る。 |
| `decimate_qem` | QEM エッジ収縮で目標面数まで簡略化(デシメーション)する。 |
| `inertia_tensor` | 水密メッシュが囲む立体の厳密な質量特性(慣性テンソル)。 |
| `is_edge_manifold` | どのエッジも 3 面以上に共有されていなければ True(エッジ多様体判定)。 |
| `is_watertight` | エッジ多様体かつ閉じていれば True(水密判定)。 |
| `orient_consistent` | 全面の巻き方向を揃える(反転した面数も返す)。 |
| `remove_degenerate_faces` | 面積ゼロの退化面を捨てる(頂点は不変)。 |
| `smooth_taubin` | Taubin の λ/μ 平滑化(トポロジー不変)。 |
| `weld_vertices` | 許容差内で一致する頂点を融合(weld)する。 |

#### arithmetic(10 op)


![fops_arithmetic](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_arithmetic.png)
*図: arithmetic の実処理例 — 暗部がつぶれた画像は線形ゲインでは明部が先に白飛びするが、log_image(対数変換)は暗部を持ち上げつつ明部を圧縮するので両立する(Fullseye 実出力)。入力は AI 生成(Gemini)・自前合成・skimage camera 減光の 3 種。*

| op | 説明 |
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
*図: augmentation の実処理例 — 1 枚の画像から撮像の悪条件(ショットノイズ・モーションブラー・周辺減光)を物理モデルで再現生成し、学習データを増やす op 群(Fullseye 実出力)。入力は skimage camera+AI 生成画像(Gemini)2 種。*

| op | 説明 |
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

| op | 説明 |
|---|---|
| `bounds` | 軸平行バウンディングボックス (min, max) を返す。 |
| `mesh_to_points` | sample_surface の別名 — メッシュを入れると点群が出る。 |
| `normalize_scale` | バウンディングボックス最大辺が size になるよう原点基準でスケールする。 |
| `read_mesh` | 三角形メッシュを読み込み (V, F) を返す。 |
| `read_points` | 点群を読み込む(色つきなら (P, C) を返す)。 |
| `recenter` | 頂点重心が原点に来るよう平行移動する(新しい配列を返す)。 |
| `sample_surface` | メッシュ表面から一様に n 点をサンプリングする。 |
| `voxelize` | メッシュを正規グリッドへボクセル化する (occ, origin)。 |
| `write_mesh` | read_mesh が読める形式(.obj 等)で三角形メッシュを書き出す。 |
| `write_points` | 点群を .ply / .xyz などへ書き出す。 |

#### xldgeom(10 op)

| op | 説明 |
|---|---|
| `xg_area_center` | 靴ひも公式で輪郭の多角形面積を求める(絶対値の和)。 |
| `xg_clip_contours` | 折れ線長が最大長の a 倍未満の輪郭を捨てる。 |
| `xg_crop_contours` | 画像中央の a 割合の窓内にある輪郭点だけ残す。 |
| `xg_eccentricity` | 点共分散から離心率 sqrt(1-λmin/λmax) を計算する。 |
| `xg_elliptic_axis` | 点集合の長短軸比 sqrt(λmax/λmin)。 |
| `xg_gen_polygons` | Douglas-Peucker 折れ線単純化(eps は外接矩形対角の a 倍)。 |
| `xg_height_width_ratio` | 点集合の軸平行外接矩形の縦横比。 |
| `xg_moments` | 点集合の正規化 2 次中心モーメント mu20+mu02。 |
| `xg_orientation` | 主軸方向 [deg] を [0,180) に折り返し 180 で割って正規化。 |
| `xg_regress_contours` | 全最小二乗直線あてはめの残差 RMS(共分散の短軸固有値の平方根)。 |

#### volops(9 op)

| op | 説明 |
|---|---|
| `vol_distance_transform` | 二値ボリュームの厳密なユークリッド距離変換。 |
| `vol_frangi` | 3D Frangi 血管様(管状構造)強調 — マルチスケール。 |
| `vol_gradient_magnitude` | 3D Sobel 勾配強度 sqrt(gz^2+gy^2+gx^2)。 |
| `vol_hessian_blobness` | Hessian 固有値による球状ブロブ応答(単一スケール)。 |
| `vol_label` | 3D 連結成分ラベリング(近傍系を選択可)。 |
| `vol_local_maxima` | 3D 局所極大(ピーク)検出。 |
| `vol_region_props` | ラベルボリュームから成分ごとの定量特徴を計算する。 |
| `vol_sato` | 3D Sato 管状構造フィルタ(2 固有値の簡易版)。 |
| `vol_watershed` | マーカー制御の 3D watershed 分割(scikit-image 導入時のみ)。 |

#### 2D Metrology(8 op)


![fops_metrology](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_metrology.png)
*図: 2D Metrology の実処理例 — サブピクセル輪郭(threshold_sub_pix)に円を最小二乗フィット(fit_circle)して半径を計測。真値つき合成 6 円で半径誤差を実測(Fullseye 実出力)。入力は合成+AI 生成(Gemini)2 種。*

| op | 説明 |
|---|---|
| `add_metrology_object_circle_measure` | 円計測オブジェクトを追加(add_metrology_object_circle_measure)。 |
| `add_metrology_object_ellipse_measure` | 楕円計測オブジェクトを追加(add_metrology_object_ellipse_measure)。 |
| `add_metrology_object_generic` | 汎用計測オブジェクトを追加(add_metrology_object_generic)。 |
| `add_metrology_object_line_measure` | 直線計測オブジェクトを追加(add_metrology_object_line_measure)。index を返す。 |
| `add_metrology_object_rectangle2_measure` | 矩形計測オブジェクトを追加(add_metrology_object_rectangle2_measure)。 |
| `align_metrology_model` | 計測モデルの全オブジェクトを平行移動して整列(align_metrology_model)。 |
| `apply_metrology_model` | 各計測オブジェクトの近傍でエッジを測定し、形状を再フィットして結果を返す(apply_metrology_model)。 |
| `create_metrology_model` | 空の計測モデルを作る(create_metrology_model)。 |

#### Inspection(8 op)


![fops_inspection](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_inspection.png)
*図: Inspection の実処理例 — ブリスターパック(合成・欠陥注入で真値管理)を格子仕様に沿ってポケット毎に検査: 二値化→面積(欠品/異種)→真円度(欠け)→暗部画素(汚れ)の固定しきい値で合否判定。3 パック合計で注入欠陥 11 件中 11 検出・誤検出 0(Fullseye 実出力)。*

| op | 説明 |
|---|---|
| `apply_bead_inspection_model` | 画像中のビードを検査し、経路上での欠損/はみ出しを検出(apply_bead_inspection_model)。 |
| `apply_texture_inspection_model` | テクスチャ検査モデルで異常(Mahalanobis 距離大)領域を検出(apply_texture_inspection_model)。 |
| `compare_ext_variation_model` | 拡張比較: 相対(k*std)と絶対(abs_thresh)の両閾値を満たす画素を欠陥に(compare_ext_variation_model)。 |
| `compare_variation_model` | 画像を variation model と比較し /image-mean/ > k*std の欠陥領域を返す(compare_variation_model)。 |
| `create_bead_inspection_model` | 接着ビード検査モデル(基準経路 + 幅公差)(create_bead_inspection_model)。 |
| `create_ocv_proj` | OCV(光学文字検証)用の平均テンプレートモデル(create_ocv_proj)。 |
| `create_texture_inspection_model` | テクスチャ検査モデル(正常サンプルの局所統計分布)(create_texture_inspection_model)。 |
| `create_variation_model` | 良品画像群から画素毎の平均・標準偏差の variation model を作る(create_variation_model)。 |

#### Morphology(8 op)

| op | 説明 |
|---|---|
| `bottom_hat` | closing(region) - region: 小さな暗構造(隙間)を抽出(bottom_hat)。 |
| `erosion2` | 参照点 (row,col) つき構造要素での収縮(erosion2)。 |
| `hit_or_miss` | hit-or-miss 変換: 前景を disc で erode ∧ 背景を disc で erode(hit_or_miss)。角/孤立点検出。 |
| `minkowski_add1` | Minkowski 和(構造要素で膨張)(minkowski_add1)。 |
| `minkowski_add2` | 反復 Minkowski 和(minkowski_add2)。 |
| `minkowski_sub1` | Minkowski 差(構造要素で収縮)(minkowski_sub1)。 |
| `minkowski_sub2` | 反復 Minkowski 差(minkowski_sub2)。 |
| `top_hat` | region - opening(region): 小さな明構造を抽出(top_hat)。 |

#### color(8 op)


![fops_color](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_color.png)
*図: color の実処理例 — 「赤い物だけ選ぶ」は輝度画像では原理的に不可能(等輝度なら二値化で区別できない)だが、trans_from_rgb で HSV に変換し H(色相)チャネルを閾値処理すれば照明の明暗によらず色で選べる(Fullseye 実出力)。入力は AI 生成画像(Gemini)2 種+等輝度の自前合成 1 種。*

| op | 説明 |
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

| op | 説明 |
|---|---|
| `contrast_maximization` | コントラスト最大化(contrast maximisation, Gallego et al. 2018)で大域オプティカルフローを推定する。 |
| `event_count` | 画素ごとの符号つきコントラスト横断回数 sign(d)*floor(abs(d)/thr)。 |
| `event_image` | イベントを蓄積した画像(IWE)を作る。 |
| `event_rate` | 全体のイベント活性 = 1 回以上発火した画素の割合。 |
| `event_rate_map` | 発火マスクを平滑化した局所イベント密度マップ [0,1]。 |
| `simulate_events` | 2 フレーム間の符号つきイベント極性マップを生成する。 |
| `time_surface` | (T,H,W) スタックから Surface of Active Events(SAE)を計算する。 |
| `warp_frame` | フレームを (dy,dx) だけシフトする(動き補償用、双一次)。 |

#### grasp(8 op)

| op | 説明 |
|---|---|
| `approach_vector_from_normals` | 把持軸に直交するグリッパ接近方向(単位ベクトル)を求める。 |
| `collision_free` | 指スイープの粗い干渉チェック(近似)。 |
| `ferrari_canny_quality` | Ferrari-Canny の ε 把持品質の近似計算。 |
| `force_closure` | 2 指の対蹠 force-closure(力の閉じ込め)判定(Nguyen 1988)。 |
| `grasp_pose` | 把持の 4x4 グリッパ座標系(剛体 pose)を組み立てる。 |
| `grasps_from_mesh` | メッシュ表面を点群化してから把持候補を提案する一括版。 |
| `rank_grasps` | 把持候補を品質の降順に並べ替える(最良が先頭)。 |
| `sample_antipodal_grasps` | 点群から 2 指対蹠把持候補をスコアつきで提案する。 |

#### measure(8 op)


![fops_measure](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_measure.png)
*図: measure の実処理例 — BGA はんだボールの X 線透過検査(減衰投影+ボイド注入の自前合成 2 種+AI 生成 1 種): ボール毎に内部の明るい画素をボイドとして面積率を計測し、真値と照合(Fullseye 実出力)。検査装置業界の実務に近い題材。*

| op | 説明 |
|---|---|
| `angle` | 線分 p0→p1 の角度 [deg](画像 y 下向き、(-180,180])。 |
| `distance` | 2 点 (row,col) 間のユークリッド距離。 |
| `fit_circle` | (row,col) 点列への代数的最小二乗円フィット(Kåsa/Coope)。 |
| `fit_ellipse` | 直接最小二乗の楕円フィット(Halir & Flusser 1998)。 |
| `fit_line` | 全最小二乗の直線フィット(直交回帰)。 |
| `fit_rectangle2` | 面積最小の有向外接矩形フィット。 |
| `line_profile` | 線分 p0→p1 に沿う輝度プロファイル(双一次サンプル)。 |
| `profile_stats` | プロファイルの min/max/mean と最強エッジ(勾配ピーク)の位置。 |

#### segment(8 op)

| op | 説明 |
|---|---|
| `Watershed` | マーカー制御 watershed 分割(cv2.watershed、不在時 skimage、なければ numpy)  [backend=opencv] |
| `sg_felzenszwalb` | segment op(HALCON: -) |
| `sg_gmm_segment` | segment op(HALCON: -) |
| `sg_kmeans_intensity` | segment op(HALCON: -) |
| `sg_normalized_cut_2` | segment op(HALCON: -) |
| `sg_region_growing_seeded` | segment op(HALCON: -) |
| `sg_slic_superpixels` | segment op(HALCON: -) |
| `sg_watershed_gradient` | segment op(HALCON: -) |

#### 1D Measuring(7 op)


![fops_measuring1d](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_measuring1d.png)
*図: 1D Measuring の実処理例 — 年輪も魚の耳石の輪紋も同じ道具で数えられる: polar_trans_image で展開 → 角度平均の 1D プロファイル → smooth_funct_1d_gauss+local_min_max_funct_1d でピーク計数。真値つき合成で計数精度を確認(Fullseye 実出力)。入力は合成+AI 生成(Gemini)2 種。*

| op | 説明 |
|---|---|
| `create_funct_1d_pairs` | (x,y) 対から等間隔 1D 関数へ再標本化(create_funct_1d_pairs)。 |
| `fuzzy_measure_pairing` | ファジィ基準(想定幅 pair_size)に最も合うエッジ対を選ぶ(fuzzy_measure_pairing)。 |
| `gen_measure_arc` | 測定弧(円周方向にプロファイルを取る)を定義(gen_measure_arc)。 |
| `gen_measure_rectangle2` | 回転測定矩形(長軸に沿ってプロファイルを取る)を定義(gen_measure_rectangle2)。 |
| `measure_pairs` | 立ち上がり/立ち下がりエッジのペア(構造の幅)を抽出(measure_pairs)。 |
| `measure_pos` | 測定線上のエッジ位置(サブピクセル)と振幅を抽出(measure_pos)。 |
| `translate_measure` | 測定オブジェクトを平行移動(translate_measure)。 |

#### 3d(7 op)

| op | 説明 |
|---|---|
| `vol_dilate` | 3d op(HALCON: -) |
| `vol_erode` | 3d op(HALCON: -) |
| `vol_gaussian` | 3d op(HALCON: -) |
| `vol_median` | 3d op(HALCON: -) |
| `vol_mip` | 3d op(HALCON: -) |
| `vol_slice` | 3d op(HALCON: -) |
| `vol_threshold` | 3d op(HALCON: -) |

#### decomposition(7 op)

| op | 説明 |
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
*図: flow の実処理例 — 「理想のハイスピードカメラ」=自前弾道シミュレーション連番(dt=1/240s 既知、実カメラのローリングシャッター/モーションブラーは含まない)から、frame_difference で動体を検出 → 重心追跡 → 放物線フィットで重力加速度 g を推定し真値 9.81 m/s² と照合(Fullseye 実出力)。動画から物理定数を測るハイスピード解析の実務。*

| op | 説明 |
|---|---|
| `Farneback` | 密オプティカルフロー(cv2.calcOpticalFlowFarneback、不在時 Horn-Schunck numpy)  [backend=opencv] |
| `flow_angle` | 画素ごとの運動方向 atan2(v,u) [rad]。 |
| `flow_magnitude` | 画素ごとの速さ sqrt(u^2+v^2)。 |
| `optical_flow_hs` | 密な Horn-Schunck オプティカルフロー(大域平滑性)。 |
| `optical_flow_lk` | 密なピラミッド Lucas-Kanade フロー。 |
| `track_points` | 疎な点を prev→nxt へ追跡する(Lucas-Kanade 点トラッカ)。 |
| `warp_by_flow` | フローに従って画像を前方ワープする。 |

#### motion(7 op)

| op | 説明 |
|---|---|
| `detect_events` | 動きエネルギー信号のスパイク位置(イベント)を検出する。 |
| `dominant_motion` | 大域アフィン運動モデルを最小二乗でフィットする。 |
| `flow_from_model` | アフィン運動モデル M から (u,v) フロー場を生成する。 |
| `frame_motion_energy` | フロー場の RMS 速さ = フレーム対ごとの 1 スカラー。 |
| `motion_energy_series` | 隣接フレーム対ごとの動きエネルギー系列。 |
| `motion_segments` | フロー場から独立に動く領域を分割する。 |
| `residual_motion` | 大域(カメラ)運動を除いた残差フロー = 独立物体の動き。 |

#### registration(7 op)

| op | 説明 |
|---|---|
| `apply_transform` | 全点に剛体変換 R·p + t を適用する。 |
| `feature_register` | FPFH 特徴 + RANSAC(+ICP 精緻化)による対応ベース位置合わせ。 |
| `icp` | ICP(反復最近点法): 対応未知のまま src を dst へ位置合わせ。 |
| `kabsch` | 対応済み点対の最適剛体変換(Kabsch 法)。 |
| `pca_align` | 主軸から粗い剛体位置合わせ(ICP の一発初期化)。 |
| `point_to_plane_icp` | point-to-plane ICP: 法線方向の距離を最小化する位置合わせ。 |
| `register` | pca_align の大回転初期化から ICP まで通すロバスト一括位置合わせ。 |

#### render3d(7 op)

| op | 説明 |
|---|---|
| `auto_view` | メッシュの外接球が収まるよう (pose, K) を自動フレーミングする。 |
| `intrinsics_from_fov` | 垂直視野角からピンホール内部行列 K を作る。 |
| `look_at` | eye から target を見るカメラの 4x4 world→camera pose を作る。 |
| `marching_cubes` | スカラー体から等値面の三角形メッシュを抽出する(マーチングキューブ)。 |
| `mesh_to_sdf` | 水密メッシュの符号つき距離場 (sdf, origin) を計算する。 |
| `render_mesh` | 三角形メッシュを深度・シルエット・法線マップへラスタライズする。 |
| `voxelize_solid` | 水密メッシュの内部まで埋めたボクセル占有 (occ, origin) を計算する。 |

#### sceneflow(7 op)

| op | 説明 |
|---|---|
| `ego_translation_from_flow` | 並進フロー場からカメラ並進方向(進行方位)を推定する。 |
| `flow_curl` | フロー場の回転(渦度)dv/dx - du/dy(画素ごと)。 |
| `flow_divergence` | フロー場の発散 du/dx + dv/dy(画素ごと)。 |
| `focus_of_expansion` | 拡張焦点(FOE): 並進時にフローが放射状に湧き出す画像上の点。 |
| `looming` | フロー場から接近(衝突切迫)の全体指標を要約する。 |
| `scene_flow` | ステレオ+オプティカルフロー対から画素ごとの 3D シーンフロー(Vedula 1999)。 |
| `time_to_contact` | 画素ごとの接触までの時間 τ [フレーム](Lee 1976)。 |

#### physics(6 op)

| op | 説明 |
|---|---|
| `ph_coherence_enhancing_diffusion` | physics op(HALCON: -) |
| `ph_heat_flow` | physics op(HALCON: -) |
| `ph_mean_curvature_motion` | physics op(HALCON: -) |
| `ph_perona_malik` | physics op(HALCON: -) |
| `ph_reaction_diffusion` | physics op(HALCON: -) |
| `ph_total_variation_flow` | physics op(HALCON: -) |

#### raster(6 op)

| op | 説明 |
|---|---|
| `read_depth` | 計量深度マップを読み込む (depth, valid)。 |
| `read_pfm` | PFM(Portable Float Map)を読み込む (arr, scale)。 |
| `read_raster` | ネイティブビット深度を保ったままラスタを読み込む (arr, meta)。 |
| `save16` | 拡張子に応じた形式で高精度のまま書き出す。 |
| `to01` | 生値に触れず [0,1] の float64 ビューを返す。 |
| `write_pfm` | PFM を書き出す((H,W) はグレー、(H,W,3) はカラー)。 |

#### subpix(6 op)

| op | 説明 |
|---|---|
| `sp_critical_points_sub_pix` | subpix op(HALCON: critical_points_sub_pix) |
| `sp_local_max_sub_pix` | subpix op(HALCON: -) |
| `sp_local_min_sub_pix` | subpix op(HALCON: local_min_sub_pix) |
| `sp_lowlands_center` | subpix op(HALCON: lowlands_center) |
| `sp_plateaus` | subpix op(HALCON: plateaus) |
| `sp_saddle_points_sub_pix` | subpix op(HALCON: saddle_points_sub_pix) |

#### detect(5 op)


![fops_detect](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_detect.png)
*図: detect の実処理例 — 「分ける(segment_objects)→測る(個体ごとの特徴量)→仕分ける(クラスタ色分け)」の 3 段活用(Fullseye 実出力+numpy k-means)。クラスタは教師なしのグループ分けであり種別の同定ではない。ハッブル深宇宙は NASA/STScI(scikit-image 同梱、パブリックドメイン)。*

| op | 説明 |
|---|---|
| `draw_objects` | 各物体のマスク着色 + bbox 描画の RGB 可視化を返す。 |
| `feature_table` | 物体ごとの特徴一覧(面積・円形度・離心率・重心)を作る。 |
| `nearest_prototype` | 記述子を最近傍プロトタイプ {label: 記述子} で分類する。 |
| `object_descriptor` | 識別用のスケール・回転頑健なコンパクト記述子(Hu の 7 モーメント等)。 |
| `segment_objects` | 前景物体を分割し、連結成分ごとのレコードを返す。 |

#### locomotion(5 op)

| op | 説明 |
|---|---|
| `com_from_silhouette` | 二値シルエットの重心 (row,col) を返す。 |
| `com_support_margin` | 静的安定余裕: 重心の接地投影から支持多角形境界までの符号つき距離。 |
| `contact_points` | 地面平面から tol 以内にある点 = 接地点を抽出する。 |
| `gait_phase` | 足の高さから各フレームの立脚/遊脚を分類する。 |
| `support_polygon` | 接地点の凸支持多角形(地面 x,y 平面)を求める。 |

#### measure1d(5 op)

| op | 説明 |
|---|---|
| `m1_fuzzy_measure_pos` | measure1d op(HALCON: fuzzy_measure_pos) |
| `m1_measure_pairs` | measure1d op(HALCON: measure_pairs) |
| `m1_measure_pos` | measure1d op(HALCON: measure_pos) |
| `m1_measure_projection` | measure1d op(HALCON: measure_projection) |
| `m1_measure_thresh` | measure1d op(HALCON: measure_thresh) |

#### occupancy(5 op)

| op | 説明 |
|---|---|
| `clearance_map` | 各セルから最近障害物までの距離マップ(ワールド単位)。 |
| `frontier_cells` | 探索用フロンティアセル: 未知領域に接する自由セル。 |
| `inflate_obstacles` | 占有セルを radius_cells 分膨張する(配置空間の障害物)。 |
| `line_of_sight` | 2 セル間の直線が障害物を横切らなければ True。 |
| `occupancy_grid_2d` | 3D 点群を上から見た 2D 占有グリッドへ集約する。 |

#### odometry(5 op)

| op | 説明 |
|---|---|
| `integrate_trajectory` | 相対運動の列を合成して絶対 4x4 pose 列にする。 |
| `pnp_odometry` | 前フレームの 3D 点を現フレームで見た対応から PnP でカメラ運動を推定する。 |
| `rgbd_odometry` | RGB-D ペア + オプティカルフローからフレーム間カメラ運動を推定する。 |
| `trajectory_error` | 推定軌跡と真値軌跡の絶対軌跡誤差(ATE)。 |
| `umeyama_align` | Umeyama の最小二乗相似変換で src 点群を dst へ整列する。 |

#### pointcloud(5 op)

| op | 説明 |
|---|---|
| `estimate_normals` | k 近傍の局所 PCA で点ごとの法線を推定する。 |
| `fpfh` | 点ごとの FPFH(Fast Point Feature Histogram)記述子(Rusu 2009)。 |
| `remove_radius_outliers` | radius 内の近傍数が min_neighbors 未満の点を除去する。 |
| `remove_statistical_outliers` | k 近傍平均距離が全体分布から外れた点を除去する(統計的外れ値除去)。 |
| `voxel_downsample` | 占有ボクセルごとに 1 点(セル重心)へ間引く。 |

#### tactile(5 op)

| op | 説明 |
|---|---|
| `tac_contact_mask` | tactile op(HALCON: -) |
| `tac_height_from_shading` | tactile op(HALCON: -) |
| `tac_pressure_proxy` | tactile op(HALCON: -) |
| `tac_shear_field` | tactile op(HALCON: -) |
| `tac_surface_normal` | tactile op(HALCON: -) |

#### tomography(5 op)

| op | 説明 |
|---|---|
| `tm_backproject_unfiltered` | tomography op(HALCON: -) |
| `tm_fbp_reconstruct` | tomography op(HALCON: -) |
| `tm_radon_forward` | tomography op(HALCON: -) |
| `tm_sart_reconstruct` | tomography op(HALCON: -) |
| `tm_sinogram_denoise` | tomography op(HALCON: -) |

#### deformreg(4 op)

| op | 説明 |
|---|---|
| `demons_register` | Thirion の demons 法で moving を fixed へ非剛体位置合わせする。 |
| `field_magnitude` | 画素ごとの変位長 sqrt(fx^2+fy^2)。 |
| `residual_ssd` | 2 画像の輝度差の二乗和(0 = 同一)。 |
| `warp_by_field` | 変位場 (fx,fy) で画像をワープする(双一次、端はクランプ)。 |

#### macro(4 op)

| op | 説明 |
|---|---|
| `macro_binarize` | macro op(HALCON: -) |
| `macro_denoise` | macro op(HALCON: -) |
| `macro_edge` | macro op(HALCON: -) |
| `macro_vol_denoise` | macro op(HALCON: -) |

#### pose(4 op)

| op | 説明 |
|---|---|
| `pose_descriptor` | 骨格グラフと主軸を組み合わせたコンパクトな姿勢記述子。 |
| `principal_axis` | 前景画素の PCA による図形の主軸。 |
| `skeleton_nodes` | 骨格の端点数・分岐点数を数える。 |
| `skeletonize_mask` | 二値図形の 1 画素幅モルフォロジー骨格化。 |

#### artistic(3 op)

| op | 説明 |
|---|---|
| `xcv_pencil_sketch` | artistic op(HALCON: -) |
| `xcv_stylization` | artistic op(HALCON: -) |
| `xpil_emboss` | artistic op(HALCON: -) |

#### deformation(3 op)

| op | 説明 |
|---|---|
| `deform_ffd` | deformation op(HALCON: -) |
| `deform_mls` | deformation op(HALCON: -) |
| `deform_tps` | deformation op(HALCON: -) |

#### ppf(3 op)

| op | 説明 |
|---|---|
| `find_surface_pose` | モデル記述子の構築とシーン照合を一度に行う一括版。 |
| `ppf_model` | モデル点群の Point Pair Feature 記述子(ハッシュ表)を構築する。 |
| `surface_match` | PPF 投票 + ICP 精緻化でシーン中のモデル 6 自由度 pose を探索する。 |

#### sim-source(3 op)

| op | 説明 |
|---|---|
| `Gazebo` | Gazebo sim-source(未接続 scaffold)。gz-transport ブリッジで RGB/depth/真値を供給予定。  [sim=gazebo, scaffold] |
| `IsaacSim` | Isaac Sim sim-source(未接続 scaffold)。omni.replicator ブリッジで供給予定。  [sim=isaacsim, scaffold] |
| `MuJoCo` | MuJoCo sim-source: RGB/深度を描画し、K を算出、真値姿勢を出し、深度を逆投影して  [sim=mujoco, available] |

#### transform(3 op)

| op | 説明 |
|---|---|
| `tf_radon_sinogram` | transform op(HALCON: -) |
| `xmh_daubechies` | transform op(HALCON: -) |
| `xmh_haar` | transform op(HALCON: -) |
