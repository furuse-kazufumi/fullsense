#### camera (22 ops)

Camera models and projection math. The transforms that shuttle back and forth between 3D and 2D.

| op | Description |
|---|---|
| `SolvePnP` | Estimate the camera pose from 3D-2D correspondences (cv2.solvePnP; numpy if absent) (camera.SolvePnP).  [backend=opencv] |
| `backproject` | Lift pixels (N,2) with depth into 3D points in the camera frame (back-projection). |
| `decompose_essential` | Decompose the essential matrix E into the 4 relative-pose candidates. |
| `decompose_intrinsics` | Extract fx, fy, cx, cy, skew from the intrinsic matrix K. |
| `depth_to_points` | Back-project an entire depth map into a point cloud in the camera frame. |
| `distort_points` | Apply radial and tangential lens distortion to ideal pixels (Brown model). |
| `epipolar_lines` | Compute the epipolar lines induced by corresponding points via the fundamental matrix. |
| `essential_from_fundamental` | Convert the fundamental matrix to the essential matrix with E = K2^T·F·K. |
| `essential_matrix` | Estimate the essential matrix E from 8+ correspondences of a calibrated pair. |
| `fundamental_matrix` | Estimate the fundamental matrix F from 8+ correspondences with the normalized 8-point method. |
| `intrinsic_matrix` | Assemble the pinhole intrinsic matrix K. |
| `normals_from_depth` | Estimate per-pixel normals (H,W,3) from an aligned depth map. |
| `project_points` | Project world points (N,3) to pixels and return (uv, depth). |
| `projection_matrix` | Assemble the 3x4 projection matrix P = K·[R t] (R, t optional). |
| `recover_pose` | Pick the physically correct relative pose from the essential-matrix decomposition candidates. |
| `reprojection_error` | Compute the per-point reprojection error [px]. |
| `rodrigues` | Rotation vector (axis × angle) to rotation matrix (Rodrigues' formula). |
| `rotation_log` | Rotation matrix to rotation vector (inverse of rodrigues). |
| `solve_pnp` | Estimate a 6-DoF pose from 6+ 3D↔2D correspondences (PnP). |
| `stereo_rectify` | Compute the rectification rotations of a calibrated stereo pair (Fusiello's method). |
| `triangulate` | Linear DLT triangulation of corresponding pixels from two views. |
| `undistort_points` | Remove radial and tangential distortion (inverse of distort_points). |

#### texture (21 ops)

Texture analysis. Laws energy, Gabor, and friends — putting numbers on "the feel of a pattern."

![Example of texture](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_10_texture_laws.png)
*Figure: Laws texture energy example (reprised from Section 11.1.1)*

| op | Description |
|---|---|
| `deviation_image` | texture op (HALCON: deviation_image) |
| `entropy_image` | texture op (HALCON: entropy_image) |
| `f2_symmetry` | texture op (HALCON: symmetry) |
| `gabor` | texture op (HALCON: gen_gabor) |
| `gen_gabor` | texture op (HALCON: gen_gabor) |
| `sk_entropy` | texture op (HALCON: entropy_image) |
| `sk_frangi` | texture op (HALCON: lines_gauss) |
| `sk_gabor` | texture op (HALCON: gen_gabor) |
| `sk_hessian` | texture op (HALCON: lines_gauss) |
| `sk_lbp` | texture op (HALCON: -) |
| `sk_meijering` | texture op (HALCON: lines_gauss) |
| `sk_shape_index` | texture op (HALCON: -) |
| `std_filter` | texture op (HALCON: deviation_image) |
| `texture_laws` | texture op (HALCON: texture_laws) |
| `tf_census_transform` | texture op (HALCON: -) |
| `tf_rank_transform` | texture op (HALCON: -) |
| `xsk2_hog` | texture op (HALCON: -) |
| `xsk_meijering` | texture op (HALCON: -) |
| `xsk_sato` | texture op (HALCON: -) |
| `xsk_struct_coherence` | texture op (HALCON: -) |
| `xsp_hilbert_env` | texture op (HALCON: -) |

#### frequency (19 ops)

Frequency-domain processing (FFT, filtering). The viewpoint that treats an image as a superposition of waves.

![Example of frequency](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_08_fft_image.png)
*Figure: FFT spectrum example (reprised from Section 11.1.1)*

| op | Description |
|---|---|
| `bandpass_image` | frequency op (HALCON: bandpass_image) |
| `fft_generic` | frequency op (HALCON: fft_generic) |
| `fft_image` | frequency op (HALCON: fft_image) |
| `fft_image_inv` | frequency op (HALCON: fft_image_inv) |
| `highpass` | frequency op (HALCON: highpass_image) |
| `highpass_image` | frequency op (HALCON: highpass_image) |
| `lowpass` | frequency op (HALCON: -) |
| `phase_deg` | frequency op (HALCON: phase_deg) |
| `phase_rad` | frequency op (HALCON: phase_rad) |
| `power_byte` | frequency op (HALCON: power_byte) |
| `power_ln` | frequency op (HALCON: power_ln) |
| `power_real` | frequency op (HALCON: power_real) |
| `rft_generic` | frequency op (HALCON: rft_generic) |
| `sk_butterworth` | frequency op (HALCON: -) |
| `xsk2_radon` | frequency op (HALCON: -) |
| `xsp_dct` | frequency op (HALCON: -) |
| `xsp_dct_lowpass` | frequency op (HALCON: -) |
| `xwt_mra_component` | frequency op (HALCON: -) |
| `xwt_subband_tile` | frequency op (HALCON: -) |

#### pcseg (17 ops)

Point-cloud segmentation (plane extraction, clustering, and more).

| op | Description |
|---|---|
| `aabb` | Return the axis-aligned bounding box (min, max) of a point cloud. |
| `centroid` | Return the centroid of a point cloud. |
| `crop_box` | Keep only points inside the axis-aligned box [lo, hi]. |
| `crop_sphere` | Keep only points within radius of the center (returns points and mask). |
| `curvature` | Compute per-point curvature (surface variation) from the eigenvalues of the k nearest neighbors. |
| `euclidean_clusters` | Group nearby points via Euclidean clustering (Rusu 2009). |
| `farthest_point_sampling` | Pick k spatially spread-out points by farthest point sampling. |
| `fit_cylinder_ransac` | Robustly fit a cylinder with RANSAC from point + normal samples. |
| `fit_plane` | Total-least-squares plane fit to all points (PCA). |
| `fit_plane_ransac` | Robustly fit the dominant plane with RANSAC. |
| `fit_sphere_ransac` | Robustly fit a sphere with RANSAC (returns center, radius, inliers). |
| `height_above_plane` | Height of each point along the plane normal (signed distance). |
| `obb` | Oriented bounding box via PCA. |
| `plane_distance` | Signed distance of each point to the plane [a,b,c,d]. |
| `principal_axes` | Principal component analysis of a point cloud (returns eigenvalues and eigenvectors). |
| `region_growing` | Cluster with smoothness-constrained region growing (Rabbani 2006). |
| `remove_ground` | Fit the dominant plane with RANSAC and split the cloud into ground/non-ground. |

#### specops (16 ops)

Special ops for pseudo-sensors and perception (pseudo-LiDAR, a 1D event camera, real-sensor reproduction, and more — the stars of Chapters 6 and 9).

| op | Description |
|---|---|
| `read_envi` | Read an ENVI hyperspectral cube (cube, meta). |
| `spec_angle_mapper` | Per-pixel spectral angle [rad] to a reference spectrum (SAM). |
| `spec_band` | Extract the i-th band of a cube as a single image. |
| `spec_band_ratio` | Compute the per-pixel band ratio band_i/(band_j+eps). |
| `spec_continuum_removal` | Continuum removal (divide each spectrum by its upper envelope). |
| `spec_decorrelation_stretch` | Emphasize color differences with a decorrelation stretch. |
| `spec_endmembers_ppi` | Approximate endmember extraction via the Pixel Purity Index. |
| `spec_fuse` | Fuse aligned single-band images into one. |
| `spec_index` | Normalized difference index (a-b)/(a+b+eps) (NDVI-style). |
| `spec_mnf` | Minimum Noise Fraction transform (MNF). |
| `spec_nearest_band` | Return the index of the band closest to a given wavelength. |
| `spec_pansharpen` | Pansharpen multispectral data with a high-resolution panchromatic band. |
| `spec_pca` | Principal component analysis along the spectral axis. |
| `spec_rgb_composite` | Build a display RGB composite from 3 chosen bands. |
| `spec_unmix` | Estimate per-pixel abundance maps by linear spectral unmixing. |
| `write_envi` | Write out an ENVI cube (.hdr + .img). |

#### 3D Matching (15 ops)

| op | Description |
|---|---|
| `create_cam_pose_look_at_point` | Build a look-at pose (4x4) from a camera position and a target point (create_cam_pose_look_at_point). |
| `create_deformable_surface_model` | Create a deformable surface model (PPF-based) (create_deformable_surface_model). |
| `create_shape_model_3d` | Build a multi-view silhouette shape model from a 3D point cloud (create_shape_model_3d). |
| `create_surface_model` | Build the Point Pair Feature descriptors (hash table) of a model point cloud. |
| `find_box_3d` | Detect an axis-aligned bounding box (OBB approximation = PCA box) in a point cloud (find_box_3d). |
| `find_deformable_surface_model` | Detect a deformable surface model in a scene point cloud (PPF + ICP refine) (find_deformable_surface_model). |
| `find_shape_model_3d` | Detect a 3D shape model in an image (correlation with projected silhouettes) (find_shape_model_3d). |
| `find_surface_model` | Find the model's 6-DoF pose in a scene with PPF voting + ICP refinement. |
| `find_surface_model_image` | Convert a depth image into a point cloud and detect a surface model (find_surface_model_image). |
| `project_shape_model_3d` | Project a 3D model into the camera and generate an edge image (project_shape_model_3d). |
| `reduce_domain` | Reduce the domain to a region (reduce_domain). A facade synonymous with change_domain. |
| `refine_deformable_surface_model` | Detect a deformable surface model → refine with ICP (refine_deformable_surface_model). |
| `refine_surface_model_pose` | Refine a surface model pose from an initial pose with ICP (refine_surface_model_pose). |
| `refine_surface_model_pose_image` | Convert a depth image into a point cloud and refine the pose with ICP (refine_surface_model_pose_image). |
| `trans_pose_shape_model_3d` | Apply a pose (4x4) to a 3D model (trans_pose_shape_model_3d). |

#### videops (15 ops)

Video and time-series processing (frame differencing, tracking, and more).

| op | Description |
|---|---|
| `background_subtraction` | Get per-frame foreground masks with a temporal-median background model. |
| `flicker_reduce` | Remove global brightness flicker between frames. |
| `frame_difference` | Get a motion-magnitude volume from absolute differences of adjacent frames. |
| `motion_energy` | Motion energy map (H,W) accumulating the amount of change along time. |
| `moving_average` | Temporal moving-average (box) smoothing. |
| `optical_flow_sequence` | Flow-magnitude volume between adjacent frames (T-1,H,W). |
| `per_frame` | Apply a 2D op independently to each frame. |
| `spatiotemporal_gaussian` | Separable 3D Gaussian smoothing in (t,y,x). |
| `spatiotemporal_sobel` | 3D Sobel gradient magnitude in (t,y,x). |
| `temporal_gradient` | Time derivative d(video)/dt by central differences. |
| `temporal_max` | Maximum projection along time (H,W). |
| `temporal_mean` | Per-pixel temporal mean (H,W). |
| `temporal_median` | Per-pixel temporal median (H,W). |
| `temporal_min` | Minimum projection along time (H,W). |
| `temporal_std` | Per-pixel temporal standard deviation = activity map (H,W). |

#### Segmentation (14 ops)


![fops_segmentation_facade](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_segmentation_facade.png)
*Figure: Segmentation ops in action — an insect in amber: against a strong orange color cast + translucent scattering + interference from bubbles and cracks, a fixed pipeline of darkest-region binarization → opening → excluding components touching the image border (border shadows, cracks) → largest component pulls out the insect body (actual Fullseye output). Honest record of the trial process: B-channel + clahe preprocessing amplified the amber's internal texture and backfired (clahe is not always the answer). All inputs are AI-generated images (Gemini).*

| op | Description |
|---|---|
| `check_difference` | Return pixels whose difference from a reference image exceeds tol as a region (check_difference). |
| `class_2dim_sup` | Classify pixels falling within ref_region's distribution in a 2-channel feature space (supervised) (class_2dim_sup). |
| `class_2dim_unsup` | Unsupervised k-means classification of a 2-channel feature space (class_2dim_unsup). Returns a label image. |
| `class_ndim_norm` | Classify an ND feature image with trained normal-distribution classes (Mahalanobis distance < thresh) (class_ndim_norm). |
| `classify_image_class_gmm` | Pixel-classify a multi-channel feature image with a Gaussian mixture model (classify_image_class_gmm). |
| `classify_image_class_knn` | Pixel-classify a multi-channel feature image with k-NN (classify_image_class_knn). |
| `classify_image_class_lut` | Pixel classification via a gray LUT (threshold/label LUT) (classify_image_class_lut). |
| `classify_image_class_mlp` | Pixel-classify a multi-channel feature image with a trained MLP (classify_image_class_mlp). |
| `classify_image_class_svm` | Pixel-classify a multi-channel feature image with a trained linear SVM (classify_image_class_svm). |
| `expand_gray` | Grow a region from seeds by gray similarity (/Δ/<tol) (expand_gray). |
| `expand_gray_ref` | Grow seeds by gray similarity to a reference image (expand_gray_ref). |
| `learn_ndim_norm` | Learn normal-distribution classes (mean, covariance) from feature vectors (learn_ndim_norm). |
| `regiongrowing_n` | Segment the whole image by similarity of multi-channel features (regiongrowing_n). Returns a label image. |
| `watersheds_marker` | Marker-controlled watershed segmentation (watersheds_marker). markers: int label image (0 = unassigned). |

#### extra (14 ops)

| op | Description |
|---|---|
| `xsitk_closing_by_recon` | extra op (HALCON: -) |
| `xsitk_confidence_connected` | extra op (HALCON: -) |
| `xsitk_connected_threshold` | extra op (HALCON: -) |
| `xsitk_curv_aniso_diff` | extra op (HALCON: -) |
| `xsitk_curvature_flow` | extra op (HALCON: -) |
| `xsitk_grayscale_fillhole` | extra op (HALCON: -) |
| `xsitk_grayscale_grindpeak` | extra op (HALCON: -) |
| `xsitk_huang_thresh` | extra op (HALCON: -) |
| `xsitk_laplacian_sharpen` | extra op (HALCON: -) |
| `xsitk_maxentropy_thresh` | extra op (HALCON: -) |
| `xsitk_minmax_curv_flow` | extra op (HALCON: -) |
| `xsitk_moments_thresh` | extra op (HALCON: -) |
| `xsitk_opening_by_recon` | extra op (HALCON: -) |
| `xsitk_signed_maurer_dist` | extra op (HALCON: -) |

#### stereo (13 ops)

Distance estimation from stereo disparity. Two-eyed triangulation (see Section 14.4).

| op | Description |
|---|---|
| `BlockMatching` | Block-matching disparity (cv2.StereoBM; fullseye numpy if absent) (stereo.BlockMatching).  [backend=opencv] |
| `SGBM` | Semi-Global BM disparity (cv2.StereoSGBM; fullseye SGM numpy if absent) (stereo.SGBM).  [backend=opencv] |
| `census_transform` | Census transform: encode each pixel by its ordering relations with its neighbors. |
| `depth_from_disparity` | Compute metric depth Z = f·B/d from disparity. |
| `disparity_census` | Estimate dense disparity by Census + Hamming-distance winner-take-all. |
| `disparity_confidence` | Estimate per-pixel matching confidence [0,1] from the cost curve (PKRN-style). |
| `disparity_map` | Dense disparity estimation via winner-take-all block matching. |
| `disparity_sgm` | Semi-Global Matching disparity (Hirschmüller's method). |
| `disparity_subpixel` | Refine disparity to subpixel with a parabola fit. |
| `fill_disparity` | Fill invalid disparities by row-wise interpolation (biased toward the background). |
| `lr_consistency` | Left-right consistency check mask (True = trustworthy disparity). |
| `reproject_to_points` | Back-project a depth map into a point cloud (N,3) in the camera frame. |
| `speckle_filter` | Remove small speckle regions from a disparity map. |

#### terrain (13 ops)

| op | Description |
|---|---|
| `detect_obstacles` | Segment cells rising more than clearance above the walkable ground as obstacles. |
| `elevation_map` | Bin a point cloud into a 2.5D elevation grid. |
| `fill_gaps` | Fill nan cells with the nearest valid height. |
| `foothold_candidates` | Pick discrete safe foothold candidates from the terrain. |
| `foothold_score` | Per-cell flatness score [0,1] (1 = flat and level = a good foothold). |
| `fuse_elevation` | Fuse aligned elevation grids into a single robot-centric one. |
| `ground_plane` | Estimate the ground plane z = ax+by+c by cell-wise robust least squares. |
| `ground_surface` | Get a smooth walkable-ground envelope surface via gray opening. |
| `roughness_map` | Per-cell roughness = standard deviation of local heights. |
| `slope_map` | Per-cell slope = surface angle from horizontal. |
| `step_edges` | Detect step edges (curbs, stair drop-off lines) from a height map. |
| `surface_normals` | Per-cell upward unit normals (H,W,3). |
| `traversability` | Build a traversable mask from step and slope limits. |

#### artificial-life (12 ops)

| op | Description |
|---|---|
| `alife_curvature_flow` | artificial-life op (HALCON: -) |
| `alife_cyclic_ca` | artificial-life op (HALCON: -) |
| `alife_dla` | artificial-life op (HALCON: -) |
| `alife_gray_scott` | artificial-life op (HALCON: -) |
| `alife_langton_ant` | artificial-life op (HALCON: -) |
| `alife_lenia` | artificial-life op (HALCON: -) |
| `alife_life_step` | artificial-life op (HALCON: -) |
| `alife_perona_malik` | artificial-life op (HALCON: -) |
| `alife_reaction_bz` | artificial-life op (HALCON: -) |
| `alife_sandpile` | artificial-life op (HALCON: -) |
| `alife_turing` | artificial-life op (HALCON: -) |
| `alife_wolfram1d` | artificial-life op (HALCON: -) |

#### complexops (12 ops)

| op | Description |
|---|---|
| `cx_apply_transfer_function` | Multiply a centered spectrum by a filter H (apply a transfer function). |
| `cx_bandpass` | Ideal annular band-pass filter in the frequency domain. |
| `cx_fft` | Centered 2D FFT of a real image (complex spectrum). |
| `cx_from_mag_phase` | Reconstruct a complex field from magnitude and phase in radians. |
| `cx_ifft` | Inverse of cx_fft (ifft2 + ifftshift). |
| `cx_imag` | Return the imaginary part of a complex field as a real image. |
| `cx_log_magnitude` | Log-magnitude spectrum [0,1] for display. |
| `cx_magnitude` | Return the per-pixel complex magnitude (absolute value). |
| `cx_phase` | Return the wrapped phase of a complex field. |
| `cx_real` | Return the real part of a complex field as a real image. |
| `cx_wiener_deconvolve` | Restore an image by frequency-domain Wiener deconvolution. |
| `phase_unwrap` | 2D phase unwrapping (wrapped phase → continuous phase). |

#### restoration (12 ops)


![fops_restoration](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_restoration.png)
*Figure: restoration ops in action — motion blur is a convolution, so edge sharpening (unsharp) cannot restore it; only iv_motion_deblur (Wiener deconvolution) assuming the blur PSF brings the text back to legibility (actual Fullseye output). The blur was applied by convolving a linear motion PSF (L=9px, 0°) (convol_fft). Inputs: skimage page/camera + AI-generated images (Gemini).*

| op | Description |
|---|---|
| `iv_backproject_superres` | restoration op (HALCON: -) |
| `iv_gradient_inpaint` | restoration op (HALCON: -) |
| `iv_motion_deblur` | restoration op (HALCON: -) |
| `iv_richardson_lucy` | restoration op (HALCON: -) |
| `iv_unsharp_deblur` | restoration op (HALCON: -) |
| `iv_wiener_deconv_spatial` | restoration op (HALCON: -) |
| `xcv3_inpaint_ns` | restoration op (HALCON: -) |
| `xcv_inpaint` | restoration op (HALCON: -) |
| `xsk2_wiener` | restoration op (HALCON: -) |
| `xsk_inpaint` | restoration op (HALCON: -) |
| `xsk_richardson_lucy` | restoration op (HALCON: -) |
| `xsk_unwrap_phase` | restoration op (HALCON: -) |

#### meshrepair (11 ops)

| op | Description |
|---|---|
| `boundary_edges` | Return the list (M,2) of edges on the mesh's open boundary. |
| `components` | Split a mesh into connected components. |
| `convex_hull` | Build the convex-hull mesh (outward-facing triangles) of a point set. |
| `decimate_qem` | Simplify (decimate) to a target face count by QEM edge collapse. |
| `inertia_tensor` | Exact mass properties (inertia tensor) of the solid enclosed by a watertight mesh. |
| `is_edge_manifold` | True if no edge is shared by 3 or more faces (edge-manifold test). |
| `is_watertight` | True if edge-manifold and closed (watertightness test). |
| `orient_consistent` | Make all face windings consistent (also returns the number of flipped faces). |
| `remove_degenerate_faces` | Discard zero-area degenerate faces (vertices unchanged). |
| `smooth_taubin` | Taubin λ/μ smoothing (topology-preserving). |
| `weld_vertices` | Weld vertices that coincide within a tolerance. |

#### arithmetic (10 ops)


![fops_arithmetic](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_arithmetic.png)
*Figure: arithmetic ops in action — for an image with crushed shadows, linear gain blows out the highlights first, but log_image (log transform) lifts the shadows while compressing the highlights, so you get both (actual Fullseye output). Inputs: 3 kinds — AI-generated (Gemini), our own synthetic, and a darkened skimage camera.*

| op | Description |
|---|---|
| `abs_image` | arithmetic op (HALCON: abs_image) |
| `acos_image` | arithmetic op (HALCON: acos_image) |
| `asin_image` | arithmetic op (HALCON: asin_image) |
| `atan_image` | arithmetic op (HALCON: atan_image) |
| `cos_image` | arithmetic op (HALCON: cos_image) |
| `exp_image` | arithmetic op (HALCON: exp_image) |
| `log_image` | arithmetic op (HALCON: log_image) |
| `sin_image` | arithmetic op (HALCON: sin_image) |
| `sqrt_image` | arithmetic op (HALCON: sqrt_image) |
| `tan_image` | arithmetic op (HALCON: tan_image) |

#### augmentation (10 ops)


![fops_augmentation](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_augmentation.png)
*Figure: augmentation ops in action — ops that regenerate adverse imaging conditions (shot noise, motion blur, vignetting) from a single image with physical models to multiply training data (actual Fullseye output). Inputs: skimage camera + 2 AI-generated images (Gemini).*

| op | Description |
|---|---|
| `aug_barrel` | augmentation op (HALCON: -) |
| `aug_chromatic` | augmentation op (HALCON: -) |
| `aug_cutout` | augmentation op (HALCON: -) |
| `aug_fixed_pattern` | augmentation op (HALCON: -) |
| `aug_jpeg_blocks` | augmentation op (HALCON: -) |
| `aug_motion_blur` | augmentation op (HALCON: -) |
| `aug_read_noise` | augmentation op (HALCON: -) |
| `aug_rolling_shutter` | augmentation op (HALCON: -) |
| `aug_shot_noise` | augmentation op (HALCON: -) |
| `aug_vignette` | augmentation op (HALCON: -) |

#### mesh (10 ops)

| op | Description |
|---|---|
| `bounds` | Return the axis-aligned bounding box (min, max). |
| `mesh_to_points` | Alias of sample_surface — put in a mesh, get out a point cloud. |
| `normalize_scale` | Scale about the origin so the largest bounding-box edge equals size. |
| `read_mesh` | Read a triangle mesh and return (V, F). |
| `read_points` | Read a point cloud (returns (P, C) if colored). |
| `recenter` | Translate so the vertex centroid lands at the origin (returns new arrays). |
| `sample_surface` | Sample n points uniformly from the mesh surface. |
| `voxelize` | Voxelize a mesh onto a regular grid (occ, origin). |
| `write_mesh` | Write out a triangle mesh in a format read_mesh can read (.obj etc.). |
| `write_points` | Write out a point cloud to .ply / .xyz etc. |

#### xldgeom (10 ops)

| op | Description |
|---|---|
| `xg_area_center` | Polygon area of contours by the shoelace formula (sum of absolute values). |
| `xg_clip_contours` | Discard contours whose polyline length is less than a times the maximum length. |
| `xg_crop_contours` | Keep only contour points inside the central a-fraction window of the image. |
| `xg_eccentricity` | Compute eccentricity sqrt(1-λmin/λmax) from the point covariance. |
| `xg_elliptic_axis` | Major/minor axis ratio sqrt(λmax/λmin) of a point set. |
| `xg_gen_polygons` | Douglas-Peucker polyline simplification (eps is a times the bounding-box diagonal). |
| `xg_height_width_ratio` | Aspect ratio of the axis-aligned bounding rectangle of a point set. |
| `xg_moments` | Normalized 2nd central moments mu20+mu02 of a point set. |
| `xg_orientation` | Principal-axis direction [deg] folded into [0,180) and normalized by dividing by 180. |
| `xg_regress_contours` | Residual RMS of a total-least-squares line fit (square root of the covariance's minor-axis eigenvalue). |

#### volops (9 ops)

| op | Description |
|---|---|
| `vol_distance_transform` | Exact Euclidean distance transform of a binary volume. |
| `vol_frangi` | 3D Frangi vessel-like (tubular structure) enhancement — multi-scale. |
| `vol_gradient_magnitude` | 3D Sobel gradient magnitude sqrt(gz^2+gy^2+gx^2). |
| `vol_hessian_blobness` | Spherical blob response from Hessian eigenvalues (single scale). |
| `vol_label` | 3D connected-component labeling (selectable neighborhood). |
| `vol_local_maxima` | 3D local maxima (peak) detection. |
| `vol_region_props` | Compute quantitative per-component features from a label volume. |
| `vol_sato` | 3D Sato tubular-structure filter (simplified 2-eigenvalue version). |
| `vol_watershed` | Marker-controlled 3D watershed segmentation (only when scikit-image is installed). |

#### 2D Metrology (8 ops)


![fops_metrology](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_metrology.png)
*Figure: 2D Metrology ops in action — least-squares circle fit (fit_circle) on subpixel contours (threshold_sub_pix) to measure radii. Radius error measured on 6 synthetic circles with ground truth (actual Fullseye output). Inputs: synthetic + 2 AI-generated (Gemini).*

| op | Description |
|---|---|
| `add_metrology_object_circle_measure` | Add a circle measurement object (add_metrology_object_circle_measure). |
| `add_metrology_object_ellipse_measure` | Add an ellipse measurement object (add_metrology_object_ellipse_measure). |
| `add_metrology_object_generic` | Add a generic measurement object (add_metrology_object_generic). |
| `add_metrology_object_line_measure` | Add a line measurement object (add_metrology_object_line_measure). Returns the index. |
| `add_metrology_object_rectangle2_measure` | Add a rectangle measurement object (add_metrology_object_rectangle2_measure). |
| `align_metrology_model` | Translate all objects of a metrology model into alignment (align_metrology_model). |
| `apply_metrology_model` | Measure edges near each measurement object, refit the shape, and return the results (apply_metrology_model). |
| `create_metrology_model` | Create an empty metrology model (create_metrology_model). |

#### Inspection (8 ops)


![fops_inspection](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_inspection.png)
*Figure: Inspection ops in action — blister packs (synthetic, with injected defects for ground-truth control) inspected pocket by pocket along the grid spec: binarization → area (missing/wrong item) → circularity (chips) → dark pixels (stains), pass/fail by fixed thresholds. Across 3 packs, 11 of 11 injected defects detected with 0 false positives (actual Fullseye output).*

| op | Description |
|---|---|
| `apply_bead_inspection_model` | Inspect the bead in an image and detect gaps/overflow along the path (apply_bead_inspection_model). |
| `apply_texture_inspection_model` | Detect anomalous regions (large Mahalanobis distance) with a texture inspection model (apply_texture_inspection_model). |
| `compare_ext_variation_model` | Extended comparison: pixels satisfying both the relative (k*std) and absolute (abs_thresh) thresholds become defects (compare_ext_variation_model). |
| `compare_variation_model` | Compare an image against the variation model and return defect regions where /image-mean/ > k*std (compare_variation_model). |
| `create_bead_inspection_model` | Adhesive bead inspection model (reference path + width tolerance) (create_bead_inspection_model). |
| `create_ocv_proj` | Mean-template model for OCV (optical character verification) (create_ocv_proj). |
| `create_texture_inspection_model` | Texture inspection model (local statistical distribution of good samples) (create_texture_inspection_model). |
| `create_variation_model` | Build a variation model of per-pixel mean and standard deviation from good-part images (create_variation_model). |

#### Morphology (8 ops)

| op | Description |
|---|---|
| `bottom_hat` | closing(region) - region: extract small dark structures (gaps) (bottom_hat). |
| `erosion2` | Erosion with a structuring element with reference point (row,col) (erosion2). |
| `hit_or_miss` | Hit-or-miss transform: erode foreground with disc ∧ erode background with disc (hit_or_miss). Corner/isolated-point detection. |
| `minkowski_add1` | Minkowski addition (dilation by a structuring element) (minkowski_add1). |
| `minkowski_add2` | Iterated Minkowski addition (minkowski_add2). |
| `minkowski_sub1` | Minkowski subtraction (erosion by a structuring element) (minkowski_sub1). |
| `minkowski_sub2` | Iterated Minkowski subtraction (minkowski_sub2). |
| `top_hat` | region - opening(region): extract small bright structures (top_hat). |

#### color (8 ops)


![fops_color](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_color.png)
*Figure: color ops in action — "pick only the red things" is fundamentally impossible on a luminance image (equal-luminance objects can't be told apart by thresholding), but converting to HSV with trans_from_rgb and thresholding the H (hue) channel selects by color regardless of illumination brightness (actual Fullseye output). Inputs: 2 AI-generated images (Gemini) + 1 equal-luminance synthetic of our own.*

| op | Description |
|---|---|
| `access_channel` | color op (HALCON: access_channel) |
| `cfa_to_rgb` | color op (HALCON: cfa_to_rgb) |
| `linear_trans_color` | color op (HALCON: linear_trans_color) |
| `principal_comp` | color op (HALCON: principal_comp) |
| `rgb1_to_gray` | color op (HALCON: rgb1_to_gray) |
| `rgb3_to_gray` | color op (HALCON: rgb3_to_gray) |
| `trans_from_rgb` | color op (HALCON: trans_from_rgb) |
| `trans_to_rgb` | color op (HALCON: trans_to_rgb) |

#### events (8 ops)

| op | Description |
|---|---|
| `contrast_maximization` | Estimate global optical flow by contrast maximization (Gallego et al. 2018). |
| `event_count` | Per-pixel signed contrast-crossing count sign(d)*floor(abs(d)/thr). |
| `event_image` | Build an image of accumulated events (IWE). |
| `event_rate` | Overall event activity = fraction of pixels that fired at least once. |
| `event_rate_map` | Local event-density map [0,1] from a smoothed firing mask. |
| `simulate_events` | Generate a signed event-polarity map between two frames. |
| `time_surface` | Compute the Surface of Active Events (SAE) from a (T,H,W) stack. |
| `warp_frame` | Shift a frame by (dy,dx) (for motion compensation, bilinear). |

#### grasp (8 ops)

| op | Description |
|---|---|
| `approach_vector_from_normals` | Find the gripper approach direction (unit vector) orthogonal to the grasp axis. |
| `collision_free` | Coarse interference check of the finger sweep (approximate). |
| `ferrari_canny_quality` | Approximate computation of the Ferrari-Canny ε grasp quality. |
| `force_closure` | Two-finger antipodal force-closure test (Nguyen 1988). |
| `grasp_pose` | Assemble the 4x4 gripper frame (rigid pose) of a grasp. |
| `grasps_from_mesh` | One-shot version that samples the mesh surface into a point cloud and then proposes grasp candidates. |
| `rank_grasps` | Sort grasp candidates in descending order of quality (best first). |
| `sample_antipodal_grasps` | Propose scored two-finger antipodal grasp candidates from a point cloud. |

#### measure (8 ops)


![fops_measure](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_measure.png)
*Figure: measure ops in action — X-ray transmission inspection of BGA solder balls (attenuation projection + void injection; 2 of our own synthetics + 1 AI-generated): for each ball, bright interior pixels are measured as voids and the area ratio is checked against ground truth (actual Fullseye output). A subject close to real practice in the inspection-equipment industry.*

| op | Description |
|---|---|
| `angle` | Angle [deg] of segment p0→p1 (image y downward, (-180,180]). |
| `distance` | Euclidean distance between two (row,col) points. |
| `fit_circle` | Algebraic least-squares circle fit to (row,col) points (Kåsa/Coope). |
| `fit_ellipse` | Direct least-squares ellipse fit (Halir & Flusser 1998). |
| `fit_line` | Total-least-squares line fit (orthogonal regression). |
| `fit_rectangle2` | Minimum-area oriented bounding rectangle fit. |
| `line_profile` | Intensity profile along segment p0→p1 (bilinear sampling). |
| `profile_stats` | Profile min/max/mean and the position of the strongest edge (gradient peak). |

#### segment (8 ops)

| op | Description |
|---|---|
| `Watershed` | Marker-controlled watershed segmentation (cv2.watershed; skimage if absent, numpy otherwise)  [backend=opencv] |
| `sg_felzenszwalb` | segment op (HALCON: -) |
| `sg_gmm_segment` | segment op (HALCON: -) |
| `sg_kmeans_intensity` | segment op (HALCON: -) |
| `sg_normalized_cut_2` | segment op (HALCON: -) |
| `sg_region_growing_seeded` | segment op (HALCON: -) |
| `sg_slic_superpixels` | segment op (HALCON: -) |
| `sg_watershed_gradient` | segment op (HALCON: -) |

#### 1D Measuring (7 ops)


![fops_measuring1d](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_measuring1d.png)
*Figure: 1D Measuring ops in action — tree rings and the growth rings of fish otoliths can be counted with the same tools: unroll with polar_trans_image → angle-averaged 1D profile → peak counting with smooth_funct_1d_gauss + local_min_max_funct_1d. Counting accuracy confirmed on synthetics with ground truth (actual Fullseye output). Inputs: synthetic + 2 AI-generated (Gemini).*

| op | Description |
|---|---|
| `create_funct_1d_pairs` | Resample (x,y) pairs into an evenly spaced 1D function (create_funct_1d_pairs). |
| `fuzzy_measure_pairing` | Pick the edge pairs that best satisfy a fuzzy criterion (expected width pair_size) (fuzzy_measure_pairing). |
| `gen_measure_arc` | Define a measurement arc (profile taken along the circumference) (gen_measure_arc). |
| `gen_measure_rectangle2` | Define a rotated measurement rectangle (profile taken along the major axis) (gen_measure_rectangle2). |
| `measure_pairs` | Extract pairs of rising/falling edges (structure widths) (measure_pairs). |
| `measure_pos` | Extract edge positions (subpixel) and amplitudes along the measurement line (measure_pos). |
| `translate_measure` | Translate a measurement object (translate_measure). |

#### 3d (7 ops)

| op | Description |
|---|---|
| `vol_dilate` | 3d op (HALCON: -) |
| `vol_erode` | 3d op (HALCON: -) |
| `vol_gaussian` | 3d op (HALCON: -) |
| `vol_median` | 3d op (HALCON: -) |
| `vol_mip` | 3d op (HALCON: -) |
| `vol_slice` | 3d op (HALCON: -) |
| `vol_threshold` | 3d op (HALCON: -) |

#### decomposition (7 ops)

| op | Description |
|---|---|
| `dc_homomorphic` | decomposition op (HALCON: -) |
| `dc_local_contrast_norm` | decomposition op (HALCON: -) |
| `dc_retinex` | decomposition op (HALCON: -) |
| `dc_rpca_lowrank` | decomposition op (HALCON: -) |
| `dc_rpca_sparse` | decomposition op (HALCON: -) |
| `dc_structure_texture` | decomposition op (HALCON: -) |
| `dc_texture_residual` | decomposition op (HALCON: -) |

#### flow (7 ops)


![fops_flow](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_flow.png)
*Figure: flow ops in action — from an "ideal high-speed camera" = our own ballistic-simulation frame sequence (dt=1/240s known; real-camera rolling shutter / motion blur not included), frame_difference detects the moving object → centroid tracking → parabola fit estimates the gravitational acceleration g, checked against the true 9.81 m/s² (actual Fullseye output). The real-world craft of high-speed analysis: measuring physical constants from video.*

| op | Description |
|---|---|
| `Farneback` | Dense optical flow (cv2.calcOpticalFlowFarneback; Horn-Schunck numpy if absent)  [backend=opencv] |
| `flow_angle` | Per-pixel motion direction atan2(v,u) [rad]. |
| `flow_magnitude` | Per-pixel speed sqrt(u^2+v^2). |
| `optical_flow_hs` | Dense Horn-Schunck optical flow (global smoothness). |
| `optical_flow_lk` | Dense pyramidal Lucas-Kanade flow. |
| `track_points` | Track sparse points from prev→nxt (Lucas-Kanade point tracker). |
| `warp_by_flow` | Forward-warp an image according to the flow. |

#### motion (7 ops)

| op | Description |
|---|---|
| `detect_events` | Detect spike positions (events) in a motion-energy signal. |
| `dominant_motion` | Least-squares fit of a global affine motion model. |
| `flow_from_model` | Generate a (u,v) flow field from an affine motion model M. |
| `frame_motion_energy` | RMS speed of a flow field = one scalar per frame pair. |
| `motion_energy_series` | Motion-energy series for each adjacent frame pair. |
| `motion_segments` | Segment independently moving regions from a flow field. |
| `residual_motion` | Residual flow after removing global (camera) motion = independent object motion. |

#### registration (7 ops)

| op | Description |
|---|---|
| `apply_transform` | Apply the rigid transform R·p + t to all points. |
| `feature_register` | Correspondence-based registration via FPFH features + RANSAC (+ ICP refinement). |
| `icp` | ICP (iterative closest point): align src to dst without known correspondences. |
| `kabsch` | Optimal rigid transform for matched point pairs (Kabsch method). |
| `pca_align` | Coarse rigid alignment from principal axes (one-shot ICP initialization). |
| `point_to_plane_icp` | Point-to-plane ICP: registration minimizing distances along the normals. |
| `register` | Robust all-in-one registration from pca_align large-rotation initialization through ICP. |

#### render3d (7 ops)

| op | Description |
|---|---|
| `auto_view` | Auto-frame (pose, K) so the mesh's bounding sphere fits in view. |
| `intrinsics_from_fov` | Build a pinhole intrinsic matrix K from a vertical field of view. |
| `look_at` | Build the 4x4 world→camera pose of a camera looking at target from eye. |
| `marching_cubes` | Extract an isosurface triangle mesh from a scalar volume (marching cubes). |
| `mesh_to_sdf` | Compute the signed distance field (sdf, origin) of a watertight mesh. |
| `render_mesh` | Rasterize a triangle mesh into depth, silhouette, and normal maps. |
| `voxelize_solid` | Compute voxel occupancy (occ, origin) with the interior of a watertight mesh filled in. |

#### sceneflow (7 ops)

| op | Description |
|---|---|
| `ego_translation_from_flow` | Estimate the camera translation direction (heading) from a translational flow field. |
| `flow_curl` | Rotation (vorticity) of the flow field dv/dx - du/dy (per pixel). |
| `flow_divergence` | Divergence of the flow field du/dx + dv/dy (per pixel). |
| `focus_of_expansion` | Focus of expansion (FOE): the image point flow radiates out from under translation. |
| `looming` | Summarize a whole-image approach (imminent-collision) indicator from the flow field. |
| `scene_flow` | Per-pixel 3D scene flow from stereo + optical flow pairs (Vedula 1999). |
| `time_to_contact` | Per-pixel time to contact τ [frames] (Lee 1976). |

#### physics (6 ops)

| op | Description |
|---|---|
| `ph_coherence_enhancing_diffusion` | physics op (HALCON: -) |
| `ph_heat_flow` | physics op (HALCON: -) |
| `ph_mean_curvature_motion` | physics op (HALCON: -) |
| `ph_perona_malik` | physics op (HALCON: -) |
| `ph_reaction_diffusion` | physics op (HALCON: -) |
| `ph_total_variation_flow` | physics op (HALCON: -) |

#### raster (6 ops)

| op | Description |
|---|---|
| `read_depth` | Read a metric depth map (depth, valid). |
| `read_pfm` | Read a PFM (Portable Float Map) (arr, scale). |
| `read_raster` | Read a raster preserving its native bit depth (arr, meta). |
| `save16` | Write out at high precision in a format chosen by extension. |
| `to01` | Return a [0,1] float64 view without touching the raw values. |
| `write_pfm` | Write out a PFM ((H,W) is gray, (H,W,3) is color). |

#### subpix (6 ops)

| op | Description |
|---|---|
| `sp_critical_points_sub_pix` | subpix op (HALCON: critical_points_sub_pix) |
| `sp_local_max_sub_pix` | subpix op (HALCON: -) |
| `sp_local_min_sub_pix` | subpix op (HALCON: local_min_sub_pix) |
| `sp_lowlands_center` | subpix op (HALCON: lowlands_center) |
| `sp_plateaus` | subpix op (HALCON: plateaus) |
| `sp_saddle_points_sub_pix` | subpix op (HALCON: saddle_points_sub_pix) |

#### detect (5 ops)


![fops_detect](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_detect.png)
*Figure: detect ops in action — the 3-step combo of "separate (segment_objects) → measure (per-object features) → sort (cluster color-coding)" (actual Fullseye output + numpy k-means). Clusters are unsupervised groupings, not species identification. The Hubble deep field is NASA/STScI (bundled with scikit-image, public domain).*

| op | Description |
|---|---|
| `draw_objects` | Return an RGB visualization with per-object mask coloring + bbox drawing. |
| `feature_table` | Build a per-object feature list (area, circularity, eccentricity, centroid). |
| `nearest_prototype` | Classify descriptors by nearest prototype {label: descriptor}. |
| `object_descriptor` | Compact scale- and rotation-robust descriptor for identification (Hu's 7 moments etc.). |
| `segment_objects` | Segment foreground objects and return a record per connected component. |

#### locomotion (5 ops)

| op | Description |
|---|---|
| `com_from_silhouette` | Return the centroid (row,col) of a binary silhouette. |
| `com_support_margin` | Static stability margin: signed distance from the COM's ground projection to the support-polygon boundary. |
| `contact_points` | Extract points within tol of the ground plane = contact points. |
| `gait_phase` | Classify stance/swing for each frame from foot heights. |
| `support_polygon` | Compute the convex support polygon of the contact points (ground x,y plane). |

#### measure1d (5 ops)

| op | Description |
|---|---|
| `m1_fuzzy_measure_pos` | measure1d op (HALCON: fuzzy_measure_pos) |
| `m1_measure_pairs` | measure1d op (HALCON: measure_pairs) |
| `m1_measure_pos` | measure1d op (HALCON: measure_pos) |
| `m1_measure_projection` | measure1d op (HALCON: measure_projection) |
| `m1_measure_thresh` | measure1d op (HALCON: measure_thresh) |

#### occupancy (5 ops)

| op | Description |
|---|---|
| `clearance_map` | Distance map from each cell to the nearest obstacle (world units). |
| `frontier_cells` | Frontier cells for exploration: free cells adjacent to unknown space. |
| `inflate_obstacles` | Dilate occupied cells by radius_cells (configuration-space obstacles). |
| `line_of_sight` | True if the straight line between two cells crosses no obstacle. |
| `occupancy_grid_2d` | Aggregate a 3D point cloud into a top-down 2D occupancy grid. |

#### odometry (5 ops)

| op | Description |
|---|---|
| `integrate_trajectory` | Compose a sequence of relative motions into a sequence of absolute 4x4 poses. |
| `pnp_odometry` | Estimate camera motion by PnP from previous-frame 3D points seen in the current frame. |
| `rgbd_odometry` | Estimate frame-to-frame camera motion from an RGB-D pair + optical flow. |
| `trajectory_error` | Absolute trajectory error (ATE) between the estimated and ground-truth trajectories. |
| `umeyama_align` | Align src points to dst with Umeyama's least-squares similarity transform. |

#### pointcloud (5 ops)

| op | Description |
|---|---|
| `estimate_normals` | Estimate per-point normals via local PCA of the k nearest neighbors. |
| `fpfh` | Per-point FPFH (Fast Point Feature Histogram) descriptors (Rusu 2009). |
| `remove_radius_outliers` | Remove points with fewer than min_neighbors neighbors within radius. |
| `remove_statistical_outliers` | Remove points whose mean k-NN distance is an outlier of the overall distribution (statistical outlier removal). |
| `voxel_downsample` | Thin to one point (cell centroid) per occupied voxel. |

#### tactile (5 ops)

| op | Description |
|---|---|
| `tac_contact_mask` | tactile op (HALCON: -) |
| `tac_height_from_shading` | tactile op (HALCON: -) |
| `tac_pressure_proxy` | tactile op (HALCON: -) |
| `tac_shear_field` | tactile op (HALCON: -) |
| `tac_surface_normal` | tactile op (HALCON: -) |

#### tomography (5 ops)

| op | Description |
|---|---|
| `tm_backproject_unfiltered` | tomography op (HALCON: -) |
| `tm_fbp_reconstruct` | tomography op (HALCON: -) |
| `tm_radon_forward` | tomography op (HALCON: -) |
| `tm_sart_reconstruct` | tomography op (HALCON: -) |
| `tm_sinogram_denoise` | tomography op (HALCON: -) |

#### deformreg (4 ops)

| op | Description |
|---|---|
| `demons_register` | Non-rigidly register moving to fixed with Thirion's demons method. |
| `field_magnitude` | Per-pixel displacement length sqrt(fx^2+fy^2). |
| `residual_ssd` | Sum of squared intensity differences of two images (0 = identical). |
| `warp_by_field` | Warp an image with a displacement field (fx,fy) (bilinear, clamped at the borders). |

#### macro (4 ops)

| op | Description |
|---|---|
| `macro_binarize` | macro op (HALCON: -) |
| `macro_denoise` | macro op (HALCON: -) |
| `macro_edge` | macro op (HALCON: -) |
| `macro_vol_denoise` | macro op (HALCON: -) |

#### pose (4 ops)

| op | Description |
|---|---|
| `pose_descriptor` | Compact posture descriptor combining the skeleton graph and the principal axis. |
| `principal_axis` | Principal axis of a figure by PCA of the foreground pixels. |
| `skeleton_nodes` | Count the skeleton's endpoints and branch points. |
| `skeletonize_mask` | 1-pixel-wide morphological skeletonization of a binary figure. |

#### artistic (3 ops)

| op | Description |
|---|---|
| `xcv_pencil_sketch` | artistic op (HALCON: -) |
| `xcv_stylization` | artistic op (HALCON: -) |
| `xpil_emboss` | artistic op (HALCON: -) |

#### deformation (3 ops)

| op | Description |
|---|---|
| `deform_ffd` | deformation op (HALCON: -) |
| `deform_mls` | deformation op (HALCON: -) |
| `deform_tps` | deformation op (HALCON: -) |

#### ppf (3 ops)

| op | Description |
|---|---|
| `find_surface_pose` | One-shot version doing model descriptor construction and scene matching at once. |
| `ppf_model` | Build the Point Pair Feature descriptors (hash table) of a model point cloud. |
| `surface_match` | Search for the model's 6-DoF pose in a scene with PPF voting + ICP refinement. |

#### sim-source (3 ops)

| op | Description |
|---|---|
| `Gazebo` | Gazebo sim-source (unconnected scaffold). RGB/depth/ground truth to be supplied via a gz-transport bridge.  [sim=gazebo, scaffold] |
| `IsaacSim` | Isaac Sim sim-source (unconnected scaffold). To be supplied via an omni.replicator bridge.  [sim=isaacsim, scaffold] |
| `MuJoCo` | MuJoCo sim-source: renders RGB/depth, computes K, outputs ground-truth poses, back-projects the depth and  [sim=mujoco, available] |

#### transform (3 ops)

| op | Description |
|---|---|
| `tf_radon_sinogram` | transform op (HALCON: -) |
| `xmh_daubechies` | transform op (HALCON: -) |
| `xmh_haar` | transform op (HALCON: -) |

#### domain (2 ops)

| op | Description |
|---|---|
| `it_crop_domain` | domain op (HALCON: crop_domain) |
| `it_full_domain` | domain op (HALCON: -) |
