#### Transformations (79 ops)

Geometric image transforms (rotation, scale, projective, polar, and so on). In inspection work these appear every single time as the step before measuring — "align the workpiece's orientation first, then measure."


![fops_transformations](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_transformations.png)
*Figure: A real Transformations example — for a plane seen from an oblique viewpoint, an affine transform (6 degrees of freedom) cannot fix the keystone distortion; only the projective transform estimated by DLT from 4 point correspondences (vector_to_proj_hom_mat2d → gen_image_warp_map) rectifies it to a true top-down view (actual Fullseye output). Row 1 is a composition of a known homography (ground truth available); rows 2-3 are AI-generated images (Gemini).*

| op | Description |
|---|---|
| `affine_trans_pixel` | Apply an affine transform to a pixel (row,col) (HALCON uses (row,col) order). |
| `affine_trans_point_2d` | Apply an arbitrary 2D affine transform to a point sequence. |
| `axis_angle_to_quat` | Build a rotation quaternion from a rotation axis and an angle. |
| `convert_point_3d_cart_to_spher` | Convert 3D points from Cartesian to spherical coordinates. |
| `convert_point_3d_spher_to_cart` | Convert 3D points from spherical to Cartesian coordinates. |
| `convert_pose_type` | Return the pose sequence (a simplified version of a genuine type conversion = identity with a type tag attached). |
| `dual_quat_compose` | Compose dual quaternions (composition of rigid transforms, dual_quat_compose). |
| `dual_quat_conjugate` | Return the conjugate of a dual quaternion. |
| `dual_quat_interpolate` | Interpolate dual quaternions (translation lerp + rotation slerp via pose, dual_quat_interpolate). |
| `dual_quat_normalize` | Normalize a dual quaternion. |
| `dual_quat_to_hom_mat3d` | Unit dual quaternion [qr(4), qd(4)] to a 4x4 rigid transform (dual_quat_to_hom_mat3d). |
| `dual_quat_to_pose` | Convert a dual quaternion to a 3D pose representation. |
| `dual_quat_to_screw` | Return the screw components (angle, translation, axis) from a dual quaternion (dual_quat_to_screw). |
| `dual_quat_trans_line_3d` | Transform a 3D line with a dual quaternion (rigidly transform the point and the direction) (dual_quat_trans_line_3d). |
| `dual_quat_trans_point_3d` | Rigidly transform a 3D point with a unit dual quaternion. |
| `gen_image_warp_map` | Generate a pixel warp map (inverse mapping) from a 2D homography (gen_image_warp_map). |
| `get_pose_type` | Return the representation format (how the rotation is stored) of a 3D pose. |
| `get_rectangle_pose` | Estimate a plane's pose from a rectangle in the image (4-corner correspondence → homography → pose) (get_rectangle_pose). |
| `hom_mat2d_compose` | Compose (multiply) two 2D homogeneous transformation matrices. |
| `hom_mat2d_determinant` | Compute the determinant of a 2D homogeneous transformation matrix. |
| `hom_mat2d_identity` | Create the homogeneous matrix of the identity 2D transform. |
| `hom_mat2d_invert` | Invert a 2D homogeneous transformation matrix. |
| `hom_mat2d_reflect` | Add a reflection to a 2D homogeneous transformation matrix. |
| `hom_mat2d_reflect_local` | Add a reflection in the local coordinate system to a 2D homogeneous transformation matrix. |
| `hom_mat2d_rotate` | Add a rotation to a 2D homogeneous transformation matrix. |
| `hom_mat2d_rotate_local` | Add a rotation in the local coordinate system to a 2D homogeneous transformation matrix. |
| `hom_mat2d_scale` | Add scaling to a 2D homogeneous transformation matrix. |
| `hom_mat2d_scale_local` | Add scaling in the local coordinate system to a 2D homogeneous transformation matrix. |
| `hom_mat2d_slant` | Add a slant (shear) to a 2D homogeneous transformation matrix. |
| `hom_mat2d_slant_local` | Add a slant in the local coordinate system to a 2D homogeneous transformation matrix. |
| `hom_mat2d_to_affine_par` | Decompose a 2D affine matrix into (sx, sy, phi, theta, tx, ty). |
| `hom_mat2d_translate` | Add a translation to a 2D homogeneous transformation matrix. |
| `hom_mat2d_translate_local` | Add a translation in the local coordinate system to a 2D homogeneous transformation matrix. |
| `hom_mat2d_transpose` | Transpose a 2D homogeneous transformation matrix. |
| `hom_mat3d_compose` | Compose (multiply) two 3D homogeneous transformation matrices. |
| `hom_mat3d_determinant` | Compute the determinant of a 3D homogeneous transformation matrix. |
| `hom_mat3d_identity` | Create the homogeneous matrix of the identity 3D transform. |
| `hom_mat3d_invert` | Invert a 3D homogeneous transformation matrix. |
| `hom_mat3d_project` | Project 3D points to 2D image points with a 4x4 perspective projection matrix (hom_mat3d_project). |
| `hom_mat3d_rotate` | Left-multiply a right-handed rotation about an axis (axis 0=x,1=y,2=z, standard sign convention). |
| `hom_mat3d_rotate_local` | Add a rotation in the local coordinate system to a 3D homogeneous transformation matrix. |
| `hom_mat3d_scale` | Add scaling to a 3D homogeneous transformation matrix. |
| `hom_mat3d_scale_local` | Add scaling in the local coordinate system to a 3D homogeneous transformation matrix. |
| `hom_mat3d_to_pose` | Decompose a 4x4 transformation matrix into a pose [rx,ry,rz(ZYX euler), tx,ty,tz]. |
| `hom_mat3d_translate` | Add a translation to a 3D homogeneous transformation matrix. |
| `hom_mat3d_translate_local` | Add a translation in the local coordinate system to a 3D homogeneous transformation matrix. |
| `hom_mat3d_transpose` | Transpose a 3D homogeneous transformation matrix. |
| `hom_vector_to_proj_hom_mat2d` | Compute a 3x3 projective transform (homography, DLT) from 4 or more correspondences (hom_vector_to_proj_hom_mat2d). |
| `point_line_to_hom_mat2d` | Estimate a 2D rigid transform from point+direction correspondences (point_line_to_hom_mat2d). |
| `point_pluecker_line_to_hom_mat3d` | Estimate a 3D rigid transform from point + Plücker line correspondences (point_pluecker_line_to_hom_mat3d). |
| `pose_average` | Compute the average pose of multiple poses. |
| `pose_compose` | Compose two 3D poses. |
| `pose_invert` | Invert each element of a sequence of 3D poses. |
| `pose_to_dual_quat` | Convert a 3D pose to a unit dual quaternion. |
| `pose_to_hom_mat3d` | Pose [rx,ry,rz(rad), tx,ty,tz] to a 4x4 transformation matrix (inverse of hom_mat3d_to_pose). |
| `pose_to_quat` | Convert the rotation part of a 3D pose to a quaternion. |
| `proj_hom_mat2d_to_pose` | Decompose a plane's pose (R,t) from a homography and the intrinsic matrix (proj_hom_mat2d_to_pose). |
| `projective_trans_hom_point_3d` | Apply a 4x4 projective transform to homogeneous 3D points (projective_trans_hom_point_3d). |
| `projective_trans_pixel` | Apply a projective transform to a pixel (row,col) (HALCON (row,col) order). |
| `projective_trans_point_3d` | Project 3D points with a projective transformation matrix. |
| `quat_compose` | Compute the product of two quaternions. |
| `quat_conjugate` | Return the conjugate of a quaternion. |
| `quat_interpolate` | Slerp spherical linear interpolation. |
| `quat_normalize` | Normalize a quaternion. |
| `quat_rotate_point_3d` | Rotate a 3D point with a unit quaternion. |
| `quat_to_hom_mat3d` | Convert a quaternion to the corresponding rotation matrix. |
| `quat_to_pose` | Convert a quaternion to the corresponding 3D pose. |
| `screw_to_dual_quat` | Screw (axis direction l, moment m, rotation angle theta, translation d) to a dual quaternion (screw_to_dual_quat). |
| `set_origin_pose` | Shift the origin of a pose by a local offset (set_origin_pose). |
| `vector_angle_to_rigid` | Compute a 2D rigid transform from one (point, angle) pair (vector_angle_to_rigid). |
| `vector_field_to_hom_mat2d` | Least-squares estimate of the affine transform (2x3) that best fits an entire vector field (vector_field_to_hom_mat2d). |
| `vector_to_aniso` | Estimate an anisotropic (non-uniform scale) affine transform from 2D point correspondences (vector_to_aniso). |
| `vector_to_hom_mat2d` | Estimate a 2D homography from point correspondences (vector_to_hom_mat2d). |
| `vector_to_hom_mat3d` | Umeyama estimation of a rigid/similarity transform (4x4) from 3D point correspondences (vector_to_hom_mat3d). |
| `vector_to_pose` | Estimate the 6-DoF pose (R, t) of an object/camera from 6 or more 3D↔2D correspondences (PnP). |
| `vector_to_proj_hom_mat2d` | DLT estimation of a projective transform (3x3 homography) from 2D point correspondences (vector_to_proj_hom_mat2d). |
| `vector_to_proj_hom_mat2d_distortion` | Estimate a projective transform including distortion (distortion assumed small; DLT) (vector_to_proj_hom_mat2d_distortion). |
| `vector_to_rigid` | Compute a 2D rigid transform (rotation + translation, Kabsch) from corresponding points (vector_to_rigid). |
| `vector_to_similarity` | Compute a 2D similarity transform (rotation + scale + translation, Umeyama) from corresponding points (vector_to_similarity). |

#### features (77 ops)

Ops that extract numeric features (area, perimeter, circularity, moments, and so on) from regions and contours. The heartland of measurement — "turning images into numbers."

![features example](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_13_area_center.png)
*Figure: An area/centroid measurement example (reprinted from Section 11.1.1)*

| op | Description |
|---|---|
| `ORB` | ORB keypoints (cv2.ORB; falls back to Harris corners in numpy when unavailable) (features.ORB).  [backend=opencv] |
| `area_center` | features op (HALCON: area_center) |
| `area_center_xld` | features op (HALCON: area_center_xld) |
| `area_frac` | features op (HALCON: area_center) |
| `area_holes` | features op (HALCON: area_holes) |
| `blob_count` | features op (HALCON: count_obj) |
| `circularity` | features op (HALCON: circularity) |
| `circularity_xld` | features op (HALCON: circularity_xld) |
| `compactness` | features op (HALCON: compactness) |
| `compactness_xld` | features op (HALCON: compactness_xld) |
| `connect_and_holes` | features op (HALCON: connect_and_holes) |
| `contlength` | features op (HALCON: contlength) |
| `convexity` | features op (HALCON: convexity) |
| `convexity_xld` | features op (HALCON: convexity_xld) |
| `count_channels` | features op (HALCON: count_channels) |
| `count_contours` | features op (HALCON: count_obj) |
| `count_obj` | features op (HALCON: count_obj) |
| `cv_cc_count` | features op (HALCON: connection) |
| `cv_good_features` | features op (HALCON: -) |
| `cv_hough_circles` | features op (HALCON: hough_circles) |
| `cv_hough_lines` | features op (HALCON: hough_lines) |
| `describe_patches` | Descriptors from the luminance patch around each keypoint, normalized to mean 0 and norm 1. |
| `diameter_region` | features op (HALCON: diameter_region) |
| `diameter_xld` | features op (HALCON: diameter_xld) |
| `eccentricity` | features op (HALCON: eccentricity) |
| `eccentricity_xld` | features op (HALCON: eccentricity_xld) |
| `elliptic_axis` | features op (HALCON: elliptic_axis) |
| `elliptic_axis_xld` | features op (HALCON: elliptic_axis_xld) |
| `entropy_gray` | features op (HALCON: entropy_gray) |
| `estimate_noise` | features op (HALCON: estimate_noise) |
| `euler_number` | features op (HALCON: euler_number) |
| `fast_corners` | FAST-style corner keypoint detection (strongest responses first). |
| `get_region_thickness` | features op (HALCON: get_region_thickness) |
| `gray_histo_abs` | features op (HALCON: gray_histo_abs) |
| `harris_corners` | Harris corner keypoint detection (strongest responses first). |
| `height_width_ratio` | features op (HALCON: height_width_ratio) |
| `hough_circle_trans` | features op (HALCON: hough_circle_trans) |
| `hough_line_trans` | features op (HALCON: hough_line_trans) |
| `intensity` | features op (HALCON: intensity) |
| `length_xld` | features op (HALCON: length_xld) |
| `match_descriptors` | Match two descriptor sets with nearest neighbor + Lowe's ratio test. |
| `match_keypoints` | Keypoint detection, description, and matching between two images in one call. |
| `min_max_gray` | features op (HALCON: min_max_gray) |
| `moments_region_2nd` | features op (HALCON: moments_region_2nd) |
| `moments_region_2nd_invar` | features op (HALCON: moments_region_2nd_invar) |
| `moments_region_2nd_rel_invar` | features op (HALCON: moments_region_2nd_rel_invar) |
| `moments_region_3rd` | features op (HALCON: moments_region_3rd) |
| `moments_region_3rd_invar` | features op (HALCON: moments_region_3rd_invar) |
| `moments_region_central` | features op (HALCON: moments_region_central) |
| `moments_region_central_invar` | features op (HALCON: moments_region_central_invar) |
| `moments_xld` | features op (HALCON: moments_xld) |
| `orientation_region` | features op (HALCON: orientation_region) |
| `orientation_xld` | features op (HALCON: orientation_xld) |
| `rectangularity` | features op (HALCON: rectangularity) |
| `rectangularity_xld` | features op (HALCON: rectangularity_xld) |
| `roundness` | features op (HALCON: roundness) |
| `sk_blur_effect` | features op (HALCON: -) |
| `sk_entropy_feat` | features op (HALCON: entropy_gray) |
| `sk_euler` | features op (HALCON: euler_number) |
| `total_length` | features op (HALCON: length_xld) |
| `vol_count` | features op (HALCON: -) |
| `xcv2_fast_count` | features op (HALCON: -) |
| `xcv2_lap_var` | features op (HALCON: -) |
| `xcv3_agast_count` | features op (HALCON: -) |
| `xcv3_brisk_count` | features op (HALCON: -) |
| `xcv3_gray_hu1` | features op (HALCON: -) |
| `xcv3_lsd_count` | features op (HALCON: -) |
| `xcv3_sift_count` | features op (HALCON: -) |
| `xcv_orb_count` | features op (HALCON: -) |
| `xsk3_estimate_sigma` | features op (HALCON: -) |
| `xsk3_is_low_contrast` | features op (HALCON: -) |
| `xsk_blob_dog` | features op (HALCON: -) |
| `xsk_blob_doh` | features op (HALCON: -) |
| `xsk_blob_log` | features op (HALCON: -) |
| `xsk_orb_count` | features op (HALCON: -) |
| `xwt_detail_energy` | features op (HALCON: -) |
| `xwt_packet_entropy` | features op (HALCON: -) |

#### region (76 ops)

Generating, combining, and selecting binary regions. Thresholding → connected components → conditional selection is the classic three-step combo.

![region example](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_05_threshold_label.png)
*Figure: A binarization → connected-component labeling example (reprinted from Section 11.1.1)*

| op | Description |
|---|---|
| `boundary` | region op (HALCON: boundary) |
| `closest_point_transform` | region op (HALCON: closest_point_transform) |
| `closing_circle` | region op (HALCON: closing_circle) |
| `closing_golay` | region op (HALCON: closing_golay) |
| `closing_rectangle1` | region op (HALCON: closing_rectangle1) |
| `convex_fill` | region op (HALCON: shape_trans) |
| `cv_dist` | region op (HALCON: distance_transform) |
| `dilation_circle` | region op (HALCON: dilation_circle) |
| `dilation_golay` | region op (HALCON: dilation_golay) |
| `dilation_rectangle1` | region op (HALCON: dilation_rectangle1) |
| `dilation_seq` | region op (HALCON: dilation_seq) |
| `dist_transform` | region op (HALCON: distance_transform) |
| `distance_transform` | region op (HALCON: distance_transform) |
| `erosion_circle` | region op (HALCON: erosion_circle) |
| `erosion_golay` | region op (HALCON: erosion_golay) |
| `erosion_rectangle1` | region op (HALCON: erosion_rectangle1) |
| `erosion_seq` | region op (HALCON: erosion_seq) |
| `fill_holes` | region op (HALCON: fill_up) |
| `fill_up` | region op (HALCON: fill_up) |
| `fill_up_shape` | region op (HALCON: fill_up_shape) |
| `get_region_contour` | region op (HALCON: get_region_contour) |
| `get_region_convex` | region op (HALCON: get_region_convex) |
| `invert_region` | region op (HALCON: complement) |
| `junctions_skeleton` | region op (HALCON: junctions_skeleton) |
| `morph_skeleton` | region op (HALCON: morph_skeleton) |
| `opening_circle` | region op (HALCON: opening_circle) |
| `opening_golay` | region op (HALCON: opening_golay) |
| `opening_rectangle1` | region op (HALCON: opening_rectangle1) |
| `pruning` | region op (HALCON: pruning) |
| `r2_inner_circle` | Draw the largest inscribed circle as a mask (a scales the drawn radius; a=0.5 for exact). |
| `r2_inner_rectangle1` | The largest axis-parallel inscribed rectangle (a shrinks the drawn rectangle; a=0 for exact). |
| `r2_partition_rectangle` | Split the region's bounding rectangle into an N×N grid and keep only the cells overlapping the region. |
| `r2_runlength_features` | Region → feature: the mean horizontal foreground run length. |
| `r2_smallest_circle` | Draw the minimum enclosing circle as a mask (Welzl's algorithm; a enlarges the radius). |
| `r2_smallest_rectangle1` | The axis-parallel enclosing rectangle (bounding box). |
| `r2_smallest_rectangle2` | Mask of the minimum-area oriented enclosing rectangle (rotating calipers). |
| `r2_sort_region` | Keep only the k-th largest connected component (k = round(a*(n-1))). |
| `r2_split_skeleton_lines` | Thin the region into a skeleton and cut it apart at branch points (3 or more neighbors). |
| `r2_union1` | Merge all connected components into one mask (OR of the labels). |
| `r3_background_seg` | region op (HALCON: background_seg) |
| `r3_clip_region` | region op (HALCON: clip_region) |
| `r3_eliminate_runs` | region op (HALCON: eliminate_runs) |
| `r3_label_to_region` | region op (HALCON: label_to_region) |
| `r3_partition_dynamic` | region op (HALCON: partition_dynamic) |
| `r3_polar_trans_region` | region op (HALCON: polar_trans_region) |
| `r3_rank_region` | region op (HALCON: rank_region) |
| `r3_region_features` | region op (HALCON: region_features) |
| `r3_runlength_distribution` | region op (HALCON: runlength_distribution) |
| `r3_select_region_point` | region op (HALCON: select_region_point) |
| `reg_close` | region op (HALCON: closing_circle) |
| `reg_dilate` | region op (HALCON: dilation_circle) |
| `reg_erode` | region op (HALCON: erosion_circle) |
| `reg_open` | region op (HALCON: opening_circle) |
| `region_boundary` | region op (HALCON: boundary) |
| `remove_noise_region` | region op (HALCON: remove_noise_region) |
| `remove_small` | region op (HALCON: select_shape) |
| `select_largest` | region op (HALCON: select_shape_std) |
| `select_shape` | region op (HALCON: select_shape) |
| `select_shape_std` | region op (HALCON: select_shape_std) |
| `shape_trans` | region op (HALCON: shape_trans) |
| `sk_clear_border` | region op (HALCON: -) |
| `sk_convex` | region op (HALCON: shape_trans) |
| `sk_find_boundaries` | region op (HALCON: boundary) |
| `sk_medial` | region op (HALCON: skeleton) |
| `sk_remove_holes` | region op (HALCON: fill_up) |
| `sk_skeleton` | region op (HALCON: skeleton) |
| `sk_thin` | region op (HALCON: thinning) |
| `skeleton` | region op (HALCON: skeleton) |
| `smallest_rectangle1` | region op (HALCON: smallest_rectangle1) |
| `thinning` | region op (HALCON: thinning) |
| `thinning_golay` | region op (HALCON: thinning_golay) |
| `thinning_seq` | region op (HALCON: thinning_seq) |
| `xcv2_hitmiss` | region op (HALCON: -) |
| `xsk2_isotropic_close` | region op (HALCON: -) |
| `xsk3_rank_majority` | region op (HALCON: -) |
| `xsp_chamfer_dist` | region op (HALCON: -) |

#### Image (59 ops)

Fundamental ops that handle the image itself: generation, input/output, channel operations, arithmetic composition, and so on.


![fops_image_chapter](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_image_chapter.png)
*Figure: A real Image example — decompose3 splits a color image into its R/G/B channels. Each channel carries different information (in a retina image, the contrast balance between vessels and background changes dramatically per channel) (actual Fullseye output). Inputs are the retina image bundled with scikit-image plus 2 AI-generated images (Gemini). An image-processing demo, not for diagnostic use.*

| op | Description |
|---|---|
| `add_channels` | Add a gray image to a base image as a channel (add_channels). |
| `append_channel` | Append one channel to a multichannel image (append_channel). |
| `area_center_gray` | Area (mass) and centroid (row,col) weighted by gray values (area_center_gray). |
| `change_domain` | Change the image's domain (ROI) to a region (zero-masking outside the region) (change_domain). |
| `channels_to_image` | Turn a list/sequence of 2D channels into a multichannel image (channels_to_image). |
| `complex_to_real` | Decompose a complex image into real/imaginary parts (complex_to_real). |
| `compose2` | Combine 2 images into a 2-channel image. |
| `compose3` | Combine 3 images into a 3-channel image. |
| `compose4` | Combine 4 images into a 4-channel image. |
| `compose5` | Combine 5 images into a 5-channel image. |
| `compose6` | Combine 6 images into a 6-channel image. |
| `compose7` | Combine 7 images into a 7-channel image. |
| `cooc_feature_matrix` | Haralick features from a GLCM (energy/contrast/correlation/homogeneity) (cooc_feature_matrix). |
| `crop_domain_rel` | Crop the domain's bounding rectangle with relative margins (crop_domain_rel). |
| `crop_rectangle2` | Crop a rotated rectangle (row,col,phi,l1,l2) and axis-align it (crop_rectangle2). |
| `decompose2` | Decompose a 2-channel image into 2 images. |
| `decompose3` | Decompose a 3-channel image into 3 images. |
| `decompose4` | Decompose a 4-channel image into 4 images. |
| `decompose5` | Decompose a 5-channel image into 5 images. |
| `decompose6` | Decompose a 6-channel image into 6 images. |
| `decompose7` | Decompose a 7-channel image into 7 images. |
| `elliptic_axis_gray` | Equivalent ellipse (ra, rb, phi) of the gray-value-weighted second moments (elliptic_axis_gray). |
| `fuzzy_entropy` | Shannon entropy of a region's gray distribution (fuzzy_entropy). |
| `fuzzy_perimeter` | Fuzzy perimeter from the total gray gradient (fuzzy_perimeter). |
| `gen_cooc_matrix` | Gray-level co-occurrence matrix (GLCM) (gen_cooc_matrix). direction=0/45/90/135 degrees. |
| `gen_image1` | Create an image from a 1-channel array (gen_image1). |
| `gen_image1_extern` | Build a 1-channel image from external memory (1D/2D) (gen_image1_extern). |
| `gen_image1_rect` | Crop a rectangular area out of an image (gen_image1_rect). |
| `gen_image3` | Create an (H,W,3) image from 3-channel arrays (gen_image3). |
| `gen_image3_extern` | Build a 3-channel image from external (interleaved) memory (gen_image3_extern). |
| `gen_image_const` | An image filled with a constant value (gen_image_const). |
| `gen_image_gray_ramp` | Linear ramp image g = alpha*(c-cx)+beta*(r-cy)+mean (gen_image_gray_ramp). |
| `gen_image_interleaved` | Restore a pixel-interleaved 1D array to an (H,W,C) image (gen_image_interleaved). |
| `gen_image_surface_first_order` | First-order surface image g = alpha*(c-col0)+beta*(r-row0)+gamma (gen_image_surface_first_order). |
| `gen_image_surface_second_order` | Second-order surface image g = a*x^2+b*x*y+c*y^2+d*x+e*y+f (gen_image_surface_second_order). |
| `get_grayval` | Return the gray value at (row,col) (nearest neighbor) (get_grayval). |
| `get_grayval_interpolated` | Bilinearly interpolated gray value at (row,col) (get_grayval_interpolated). |
| `gray_features` | Gray features of a region (mean/deviation/min/max/median/area) (gray_features). |
| `gray_histo` | Gray histogram (absolute and relative frequencies) (gray_histo). |
| `gray_histo_range` | Gray histogram over a specified range (gray_histo_range). |
| `gray_projections` | Row-direction/column-direction gray projections (gray_projections). |
| `histo_2dim` | 2D histogram of two channels (histo_2dim). |
| `image_to_channels` | Split a multichannel image into its individual channels (image_to_channels). |
| `interleave_channels` | Channels into a single pixel-interleaved array (interleave_channels). |
| `moments_gray_plane` | First-order gray moments (plane-fit coefficients alpha,beta,mean) (moments_gray_plane). |
| `overpaint_gray` | Synonymous with paint_gray; overpaints with the source (overpaint_gray). |
| `overpaint_region` | Synonymous with paint_region; overpaints the region (overpaint_region). |
| `paint_gray` | Transfer the gray values of a source image into an image (within a region) (paint_gray). |
| `paint_region` | Paint a region with a constant gray value (paint_region). |
| `paint_xld` | Draw an XLD contour into an image (paint_xld). |
| `real_to_complex` | Combine real/imaginary images into a complex image (real_to_complex). |
| `real_to_vector_field` | Combine 2 real images into an (H,W,2) vector field (real_to_vector_field). |
| `select_gray` | Select only regions whose gray feature falls within [minv,maxv] (select_gray). regions = list of bool masks. |
| `shape_histo_all` | Shape histogram collecting the region area at each level while sweeping the threshold (shape_histo_all). |
| `shape_histo_point` | Collect, per threshold, the area of the connected region containing a specified point (shape_histo_point). |
| `tile_channels` | Tile a multichannel image into a single gray image (tile_channels). |
| `tile_images` | Tile same-size images into a grid (tile_images). |
| `tile_images_offset` | Paste each image at an offset (row,col) and composite (tile_images_offset). |
| `vector_field_to_real` | Decompose a vector field (H,W,2) into row/col component images (vector_field_to_real). |

#### Filters (58 ops)

Spatial filters at large. Smoothing, sharpening, derivative families — a group that conditions the image through convolutions over pixel neighborhoods.

![Filters example](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_01_gauss_image.png)
*Figure: A Gaussian smoothing example (reprinted from Section 11.1.1)*

| op | Description |
|---|---|
| `abs_diff_image` | /image1-image2/*mult (abs_diff_image). |
| `add_image` | (image1+image2)*mult+add (add_image). |
| `apply_color_trans_lut` | Convert RGB (H,W,3) to the LUT's color space (apply_color_trans_lut). rgb_to_hsv / rgb_to_yuv etc. |
| `atan2_image` | atan2(image1, image2) (angle of a vector field, atan2_image). |
| `bit_and` | Bitwise AND of integerized pixels (bit_and). |
| `bit_not` | Bit inversion (bit_not). |
| `bit_or` | Bitwise OR (bit_or). |
| `bit_xor` | Bitwise XOR (bit_xor). |
| `clear_color_trans_lut` | Discard a color-transform LUT (clear_color_trans_lut). |
| `convert_map_type` | Map/image type conversion (convert_map_type). |
| `convol_channels` | Convolve each channel of a multichannel image (convol_channels). image=(H,W,C) or 2D. |
| `convol_fft` | Linear convolution via FFT (convol_fft/convol_image). |
| `convol_image` | Spatial convolution (convol_image). |
| `correlation_fft` | Cross-correlation via FFT (correlation_fft). |
| `create_color_trans_lut` | Create a color-transform LUT (transform type) (create_color_trans_lut). |
| `crop_domain` | Crop the image at the domain's bounding rectangle (crop_domain). |
| `derivate_vector_field` | Compute the divergence/curl/Jacobian of a vector field (derivate_vector_field). |
| `deviation_n` | Per-pixel standard deviation of an image stack (deviation_n). |
| `div_image` | image1/image2*mult+add (div_image). Division by zero is guarded. |
| `energy_gabor` | Energy (squared amplitude) from the Gabor real/imaginary responses (energy_gabor). |
| `exhaustive_match` | Best match of exhaustive NCC (same core as find_ncc_model; also returns error=1-score). |
| `exhaustive_match_mg` | Multigrid exhaustive template matching (coarse-to-fine speedup) (exhaustive_match_mg). |
| `gauss_distribution` | Probability density table of a normal distribution (gauss_distribution). For noise models. |
| `gen_canonical_variates_trans` | Compute a canonical variates (LDA) transform from class-labeled multichannel images (gen_canonical_variates_trans). |
| `gen_filter_mask` | Generate a filter mask with arbitrary coefficients (gen_filter_mask). |
| `gen_gauss_filter` | Normalized 2D Gaussian filter mask (gen_gauss_filter). |
| `gen_mean_filter` | Mean (box) filter mask (gen_mean_filter). |
| `gen_principal_comp_trans` | Compute a principal-component transform (eigenvectors/eigenvalues) from a set of multichannel images (gen_principal_comp_trans). |
| `gen_psf_defocus` | Circular blur (defocus) PSF (gen_psf_defocus). |
| `gen_psf_motion` | Linear blur (motion) PSF (gen_psf_motion). |
| `gen_savitzky_golay_filter` | Savitzky-Golay smoothing/derivative 1D filter coefficients (gen_savitzky_golay_filter). |
| `gen_sin_bandpass` | Sine-window frequency bandpass mask (gen_sin_bandpass). |
| `gen_std_bandpass` | Butterworth-style bandpass mask (gen_std_bandpass). |
| `harmonic_interpolation` | Fill holes (region=True) with the Laplace equation (harmonic functions) (harmonic_interpolation). |
| `inpainting_aniso` | Restore missing regions with anisotropic diffusion (Perona-Malik) (inpainting_aniso). |
| `inpainting_ced` | Inpaint with coherence-enhancing diffusion (diffusion along the structure-tensor direction) (inpainting_ced). |
| `inpainting_ct` | Isotropic-diffusion inpainting close to coherence transport (inpainting_ct). |
| `inpainting_mcf` | Mean Curvature Flow inpainting (inpainting_mcf). |
| `inpainting_texture` | Texture-synthesis inpainting (copying known nearby patches) (inpainting_texture). |
| `map_image` | Apply a LUT (map) to the pixels (map_image). map is a 1D array of length N. |
| `max_image` | Pixelwise maximum (max_image). |
| `mean_n` | Per-pixel mean of an image stack (mean_n). |
| `midrange_image` | Local (min+max)/2 midrange filter (midrange_image). |
| `min_image` | Pixelwise minimum (min_image). |
| `mult_image` | image1*image2*mult+add (mult_image). |
| `noise_distribution_mean` | Estimate the mean per-pixel noise standard deviation from multiple observations (noise_distribution_mean). |
| `optical_flow_mg` | Multigrid (coarse-to-fine pyramid + warping) Horn-Schunck dense optical flow |
| `phase_correlation_fft` | Estimate the translation (drow, dcol) via phase correlation (phase_correlation_fft). |
| `points_sojka` | Extract subpixel corners with Sojka's gradient-covariance corner response |
| `rank_n` | Per-pixel rank value of an image stack (order statistics, rank_n). Default is the median. |
| `scene_flow_calib` | Calibrated scene flow (3D displacements made metric via the intrinsic matrix) (scene_flow_calib). |
| `scene_flow_uncalib` | Estimate 3D scene flow from left/right images at two time steps (uncalibrated approximation) (scene_flow_uncalib). |
| `sp_distribution` | Salt-and-pepper noise distribution (mass at both ends, uniform in the middle) (sp_distribution). |
| `sub_image` | (image1-image2)*mult+add (sub_image). |
| `unwarp_image_vector_field` | Warp an image along a vector field (inverse mapping) (unwarp_image_vector_field). |
| `vector_field_length` | Magnitude at each point of a vector field (vector_field_length). |
| `wiener_filter` | Wiener deconvolution (wiener_filter). |
| `wiener_filter_ni` | Non-iterative Wiener restoration (wiener_filter_ni). |

#### edges (56 ops)

Edge (contour) detection, from Sobel-style gradients to Canny's thinning. Most measurement baselines are born here.

![edges example](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_04_canny.png)
*Figure: A Canny edge detection example (reprinted from Section 11.1.1)*

| op | Description |
|---|---|
| `corner_response` | edges op (HALCON: points_harris) |
| `cv_corner_harris` | edges op (HALCON: points_harris) |
| `cv_laplacian` | edges op (HALCON: laplace) |
| `cv_min_eigen` | edges op (HALCON: points_harris) |
| `cv_precorner` | edges op (HALCON: corner_response) |
| `cv_scharr` | edges op (HALCON: edges_image) |
| `derivate_gauss` | edges op (HALCON: derivate_gauss) |
| `diff_of_gauss` | edges op (HALCON: diff_of_gauss) |
| `dog` | edges op (HALCON: diff_of_gauss) |
| `dots_image` | edges op (HALCON: dots_image) |
| `edges_color` | edges op (HALCON: edges_color) |
| `f2_shock` | edges op (HALCON: shock_filter) |
| `f2_topographic` | edges op (HALCON: topographic_sketch) |
| `frei_amp` | edges op (HALCON: frei_amp) |
| `frei_dir` | edges op (HALCON: frei_dir) |
| `grad_dir` | edges op (HALCON: -) |
| `kirsch_amp` | edges op (HALCON: kirsch_amp) |
| `kirsch_dir` | edges op (HALCON: kirsch_dir) |
| `laplace` | edges op (HALCON: laplace) |
| `laplace_of_gauss` | edges op (HALCON: laplace_of_gauss) |
| `log` | edges op (HALCON: laplace_of_gauss) |
| `points_foerstner` | edges op (HALCON: points_foerstner) |
| `points_harris_binomial` | edges op (HALCON: points_harris_binomial) |
| `prewitt_amp` | edges op (HALCON: prewitt_amp) |
| `prewitt_dir` | edges op (HALCON: prewitt_dir) |
| `prewitt_mag` | edges op (HALCON: prewitt_amp) |
| `roberts` | edges op (HALCON: roberts) |
| `roberts_mag` | edges op (HALCON: roberts) |
| `robinson_amp` | edges op (HALCON: robinson_amp) |
| `robinson_dir` | edges op (HALCON: robinson_dir) |
| `sk_corner_harris` | edges op (HALCON: points_harris) |
| `sk_dog` | edges op (HALCON: diff_of_gauss) |
| `sk_farid` | edges op (HALCON: edges_image) |
| `sk_hessian_det` | edges op (HALCON: -) |
| `sk_scharr` | edges op (HALCON: edges_image) |
| `sobel_amp` | edges op (HALCON: sobel_amp) |
| `sobel_dir` | edges op (HALCON: sobel_dir) |
| `sobel_mag` | edges op (HALCON: sobel_amp) |
| `tf_phase_congruency` | edges op (HALCON: -) |
| `tf_steerable_filter` | edges op (HALCON: -) |
| `xkor_dog` | edges op (HALCON: -) |
| `xkor_gftt` | edges op (HALCON: -) |
| `xkor_harris` | edges op (HALCON: -) |
| `xkor_hessian` | edges op (HALCON: -) |
| `xkor_laplacian` | edges op (HALCON: -) |
| `xpil_contour` | edges op (HALCON: -) |
| `xpil_find_edges` | edges op (HALCON: -) |
| `xsk2_corner_kr` | edges op (HALCON: -) |
| `xsk2_inv_gauss_grad` | edges op (HALCON: -) |
| `xsk3_corner_fast` | edges op (HALCON: -) |
| `xsk3_corner_moravec` | edges op (HALCON: -) |
| `xsk_hessian_eig` | edges op (HALCON: -) |
| `xsp_gauss_grad_mag` | edges op (HALCON: -) |
| `xsp_morph_laplace` | edges op (HALCON: -) |
| `xwt_directional_detail` | edges op (HALCON: -) |
| `xwt_hf_reconstruct` | edges op (HALCON: -) |

#### segmentation (54 ops)

Segmentation, which carves an image into meaningful regions — from the thresholding families to the watershed.

![segmentation example](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_14_watersheds.png)
*Figure: A watershed example (reprinted from Section 11.1.1)*

| op | Description |
|---|---|
| `adaptive_gauss_thresh` | segmentation op (HALCON: local_threshold) |
| `auto_threshold` | segmentation op (HALCON: auto_threshold) |
| `bin_threshold` | segmentation op (HALCON: bin_threshold) |
| `binary_threshold` | segmentation op (HALCON: binary_threshold) |
| `canny` | segmentation op (HALCON: edges_image) |
| `cv_adaptive_gauss` | segmentation op (HALCON: local_threshold) |
| `cv_adaptive_mean` | segmentation op (HALCON: dyn_threshold) |
| `cv_canny` | segmentation op (HALCON: edges_image) |
| `cv_otsu` | segmentation op (HALCON: binary_threshold) |
| `dual_threshold` | segmentation op (HALCON: dual_threshold) |
| `dyn_threshold` | segmentation op (HALCON: dyn_threshold) |
| `edges_image` | segmentation op (HALCON: edges_image) |
| `fast_threshold` | segmentation op (HALCON: fast_threshold) |
| `h_threshold` | segmentation op (HALCON: threshold) |
| `hysteresis_threshold` | segmentation op (HALCON: hysteresis_threshold) |
| `it_region_to_bin` | segmentation op (HALCON: region_to_bin) |
| `local_max` | segmentation op (HALCON: local_max_sub_pix) |
| `local_min` | segmentation op (HALCON: local_min) |
| `local_threshold` | segmentation op (HALCON: local_threshold) |
| `nonmax_suppression_amp` | segmentation op (HALCON: nonmax_suppression_amp) |
| `otsu` | segmentation op (HALCON: binary_threshold) |
| `pouring` | segmentation op (HALCON: pouring) |
| `regiongrowing` | segmentation op (HALCON: regiongrowing) |
| `regiongrowing_mean` | segmentation op (HALCON: regiongrowing_mean) |
| `segment_image_mser` | segmentation op (HALCON: segment_image_mser) |
| `sk_canny` | segmentation op (HALCON: edges_image) |
| `sk_chan_vese` | segmentation op (HALCON: -) |
| `sk_felzenszwalb` | segmentation op (HALCON: -) |
| `sk_hysteresis` | segmentation op (HALCON: hysteresis_threshold) |
| `sk_li` | segmentation op (HALCON: binary_threshold) |
| `sk_local_maxima` | segmentation op (HALCON: local_max) |
| `sk_niblack` | segmentation op (HALCON: var_threshold) |
| `sk_otsu` | segmentation op (HALCON: binary_threshold) |
| `sk_sauvola` | segmentation op (HALCON: var_threshold) |
| `sk_slic` | segmentation op (HALCON: -) |
| `sk_yen` | segmentation op (HALCON: binary_threshold) |
| `threshold` | segmentation op (HALCON: threshold) |
| `var_threshold` | segmentation op (HALCON: var_threshold) |
| `watersheds` | segmentation op (HALCON: watersheds) |
| `watersheds_threshold` | segmentation op (HALCON: watersheds_threshold) |
| `xcv2_meanshift` | segmentation op (HALCON: -) |
| `xcv_grabcut` | segmentation op (HALCON: -) |
| `xcv_watershed_markers` | segmentation op (HALCON: watersheds) |
| `xkor_canny` | segmentation op (HALCON: -) |
| `xmh_bernsen` | segmentation op (HALCON: -) |
| `xsk2_h_maxima` | segmentation op (HALCON: -) |
| `xsk2_multiotsu` | segmentation op (HALCON: -) |
| `xsk3_h_minima` | segmentation op (HALCON: -) |
| `xsk3_peak_local_max` | segmentation op (HALCON: -) |
| `xsk3_rank_otsu` | segmentation op (HALCON: -) |
| `xsk3_threshold_local_median` | segmentation op (HALCON: -) |
| `xsk_flood` | segmentation op (HALCON: -) |
| `xsk_random_walker` | segmentation op (HALCON: -) |
| `zero_crossing` | segmentation op (HALCON: zero_crossing) |

#### smoothing (48 ops)

A group dedicated to smoothing. Gaussian, bilateral, anisotropic diffusion — the craft lies in choosing among the "remove the noise but protect the edges" variants.


![fops_smoothing](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_smoothing.png)
*Figure: A real smoothing example — on the same noisy input, Gaussian smoothing blurs the contours away with everything else, whereas anisotropic_diffusion diffuses without crossing edges, flattening only the noise while keeping the contours (actual Fullseye output). Inputs are skimage camera plus 2 AI-generated images (Gemini).*

| op | Description |
|---|---|
| `anisotropic_diffusion` | smoothing op (HALCON: anisotropic_diffusion) |
| `bilateral` | smoothing op (HALCON: bilateral_filter) |
| `bilateral_filter` | smoothing op (HALCON: bilateral_filter) |
| `binomial_filter` | smoothing op (HALCON: binomial_filter) |
| `coherence_enhancing_diff` | smoothing op (HALCON: coherence_enhancing_diff) |
| `cv_bilateral` | smoothing op (HALCON: bilateral_filter) |
| `cv_box` | smoothing op (HALCON: mean_image) |
| `cv_gaussian` | smoothing op (HALCON: gauss_filter) |
| `cv_nlmeans` | smoothing op (HALCON: -) |
| `cv_sharpen` | smoothing op (HALCON: emphasize) |
| `dl_aniso_diffusion` | smoothing op (HALCON: anisotropic_diffusion) |
| `dl_guided_filter` | smoothing op (HALCON: guided_filter) |
| `f2_gauss_pyramid` | smoothing op (HALCON: gen_gauss_pyramid) |
| `gauss_filter` | smoothing op (HALCON: gauss_filter) |
| `gauss_image` | smoothing op (HALCON: gauss_image) |
| `gaussian` | smoothing op (HALCON: gauss_filter) |
| `guided_filter` | smoothing op (HALCON: guided_filter) |
| `isotropic_diffusion` | smoothing op (HALCON: isotropic_diffusion) |
| `mean_box` | smoothing op (HALCON: mean_image) |
| `mean_curvature_flow` | smoothing op (HALCON: mean_curvature_flow) |
| `mean_image` | smoothing op (HALCON: mean_image) |
| `sigma_image` | smoothing op (HALCON: sigma_image) |
| `simulate_defocus` | smoothing op (HALCON: simulate_defocus) |
| `simulate_motion` | smoothing op (HALCON: simulate_motion) |
| `sk_nlm` | smoothing op (HALCON: -) |
| `sk_rolling_ball` | smoothing op (HALCON: -) |
| `sk_tv` | smoothing op (HALCON: -) |
| `sk_tv_bregman` | smoothing op (HALCON: -) |
| `sk_wavelet` | smoothing op (HALCON: -) |
| `smooth_image` | smoothing op (HALCON: smooth_image) |
| `unsharp` | smoothing op (HALCON: emphasize) |
| `xcv3_denoise_tvl1` | smoothing op (HALCON: -) |
| `xcv3_pyr_laplacian` | smoothing op (HALCON: -) |
| `xcv_edge_preserving` | smoothing op (HALCON: -) |
| `xkor_bilateral` | smoothing op (HALCON: -) |
| `xkor_gaussian` | smoothing op (HALCON: -) |
| `xkor_motion_blur` | smoothing op (HALCON: -) |
| `xkor_unsharp` | smoothing op (HALCON: -) |
| `xpil_smooth_more` | smoothing op (HALCON: -) |
| `xpil_unsharp_mask` | smoothing op (HALCON: -) |
| `xsk3_rank_mean_bilateral` | smoothing op (HALCON: -) |
| `xsp_cspline_smooth` | smoothing op (HALCON: -) |
| `xsp_dct_denoise` | smoothing op (HALCON: -) |
| `xsp_savgol` | smoothing op (HALCON: -) |
| `xsp_wiener` | smoothing op (HALCON: -) |
| `xwt_firm_denoise` | smoothing op (HALCON: -) |
| `xwt_lf_reconstruct` | smoothing op (HALCON: -) |
| `xwt_visushrink` | smoothing op (HALCON: -) |
