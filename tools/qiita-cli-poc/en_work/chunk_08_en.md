#### Matrix (46 ops)

Matrix operations, linear systems, and decompositions (SVD and friends). The mathematical backstage crew behind camera calibration and pose estimation.

| op | Description |
|---|---|
| `abs_matrix` | Compute the element-wise absolute value of a matrix. |
| `abs_matrix_mod` | Element-wise absolute value (result overwrites the input matrix). |
| `add_matrix` | Add two matrices. |
| `add_matrix_mod` | Matrix addition (result overwrites the input matrix). |
| `create_matrix` | Create a new matrix. |
| `decompose_matrix` | Return the LU decomposition (P, L, U) (decompose_matrix). |
| `determinant_matrix` | Compute the determinant of a matrix. |
| `div_element_matrix` | Element-wise division of two matrices. |
| `div_element_matrix_mod` | Element-wise division (result overwrites the input matrix). |
| `eigenvalues_general_matrix` | Compute the eigenvalues (and eigenvectors if needed) of a general matrix. |
| `eigenvalues_symmetric_matrix` | Compute the eigenvalues (and eigenvectors if needed) of a symmetric matrix. |
| `generalized_eigenvalues_general_matrix` | Compute the generalized eigenvalues (and eigenvectors if needed) of a general matrix pair. |
| `generalized_eigenvalues_symmetric_matrix` | Compute the generalized eigenvalues (and eigenvectors if needed) of a symmetric matrix pair. |
| `get_diagonal_matrix` | Extract the diagonal elements of a matrix. |
| `get_sub_matrix` | Extract a submatrix. |
| `invert_matrix` | Compute the matrix inverse. |
| `invert_matrix_mod` | Matrix inverse (result overwrites the input matrix). |
| `max_matrix` | Return the maximum of the matrix elements. |
| `mean_matrix` | Return the mean of the matrix elements. |
| `min_matrix` | Return the minimum of the matrix elements. |
| `mult_element_matrix` | Element-wise multiplication of two matrices. |
| `mult_element_matrix_mod` | Element-wise multiplication (result overwrites the input matrix). |
| `mult_matrix` | Compute the product of two matrices. |
| `mult_matrix_mod` | Matrix product (result overwrites the input matrix). |
| `norm_matrix` | Compute the norm of a matrix. |
| `orthogonal_decompose_matrix` | Return the QR orthogonal decomposition (orthogonal_decompose_matrix). |
| `pow_element_matrix` | Raise each element of a matrix to a power. |
| `pow_element_matrix_mod` | Element-wise power (result overwrites the input matrix). |
| `pow_matrix` | Compute the power of the matrix itself. |
| `pow_matrix_mod` | Matrix power (result overwrites the input matrix). |
| `pow_scalar_element_matrix` | Element-wise power with a scalar base and each element as the exponent. |
| `pow_scalar_element_matrix_mod` | Scalar-base element-wise power (result overwrites the input matrix). |
| `repeat_matrix` | Tile a matrix repeatedly. |
| `scale_matrix` | Multiply a matrix by a scalar. |
| `scale_matrix_mod` | Scalar multiplication (result overwrites the input matrix). |
| `set_diagonal_matrix` | Set the diagonal elements of a matrix. |
| `set_sub_matrix` | Write a submatrix. |
| `solve_matrix` | Solve a system of linear equations. |
| `sqrt_matrix` | Compute the element-wise square root of a matrix. |
| `sqrt_matrix_mod` | Element-wise square root (result overwrites the input matrix). |
| `sub_matrix` | Subtract two matrices. |
| `sub_matrix_mod` | Matrix subtraction (result overwrites the input matrix). |
| `sum_matrix` | Return the sum of the matrix elements. |
| `svd_matrix` | Compute the singular value decomposition (SVD). |
| `transpose_matrix` | Transpose a matrix. |
| `transpose_matrix_mod` | Transpose (result overwrites the input matrix). |

#### 3D Reconstruction (43 ops)

3D reconstruction from depth, disparity, and multiple views. The bridge that carries you from 2.5D (depth images) into the world of point clouds and meshes.

![Example of 3D Reconstruction](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_16_depth_to_points.png)
*Figure: depth → point cloud example (reprised from Section 11.1.1)*

| op | Description |
|---|---|
| `apply_sheet_of_light_calibration` | Convert profiles (pixel rows) to metric heights (apply_sheet_of_light_calibration). |
| `binocular_disparity` | Stereo disparity estimation via Semi-Global Matching (Hirschmüller's method). |
| `binocular_disparity_mg` | Dense disparity estimation via winner-take-all block matching. |
| `binocular_disparity_ms` | Alternate entry point for SGM disparity estimation (implementation is Hirschmüller's method). |
| `binocular_distance` | Compute metric depth Z = f·B/d from disparity. |
| `binocular_distance_mg` | Disparity → metric depth Z = f·B/d (mg entry point). |
| `binocular_distance_ms` | Disparity → metric depth Z = f·B/d (ms entry point). |
| `calibrate_sheet_of_light` | Calibrate the sheet-of-light pixel→height scale from a known step (calibrate_sheet_of_light). |
| `create_sheet_of_light_calib_object` | Sheet-of-light calibration object (known step) (create_sheet_of_light_calib_object). |
| `create_sheet_of_light_model` | Sheet-of-light (laser line) profile measurement model (create_sheet_of_light_model). |
| `create_stereo_model` | Stereo measurement model (left/right intrinsics + relative pose) (create_stereo_model). |
| `create_structured_light_model` | Structured-light measurement model (phase-shift pattern settings) (create_structured_light_model). |
| `decode_structured_light_pattern` | Decode the absolute phase (= correspondence) from a phase-shift structured-light image sequence (decode_structured_light_pattern). |
| `depth_from_focus` | Estimate the per-pixel best-focus position = depth from a focus stack (depth_from_focus). |
| `disparity_to_distance` | Convert disparity d to distance Z = f*baseline/d (disparity_to_distance). |
| `disparity_to_point_3d` | Compute the 3D point (X,Y,Z) from an image point (row,col) and disparity (disparity_to_point_3d). |
| `distance_to_disparity` | Convert distance Z to disparity d = f*baseline/Z (distance_to_disparity). |
| `essential_to_fundamental_matrix` | Compute the fundamental matrix F = K2^-T E K1^-1 from the essential matrix E (essential_to_fundamental_matrix). |
| `gen_binocular_proj_rectification` | Estimate the epipole-aligning transforms for stereo rectification from the fundamental matrix |
| `gen_binocular_rectification_map` | Compute the rectification rotations of a calibrated stereo pair (Fusiello's method). |
| `gen_structured_light_pattern` | Generate sinusoidal structured-light pattern images (gen_structured_light_pattern). |
| `intersect_lines_of_sight` | Reconstruct corresponding pixels from two views in 3D via linear DLT triangulation. |
| `match_essential_matrix_ransac` | Estimate the essential matrix E via RANSAC from point correspondences and the intrinsic matrix K (match_essential_matrix_ransac). |
| `match_fundamental_matrix_distortion_ransac` | RANSAC estimation of the fundamental matrix including distortion (match_fundamental_matrix_distortion_ransac). |
| `match_fundamental_matrix_ransac` | Estimate the fundamental matrix F and inliers via RANSAC from point correspondences (match_fundamental_matrix_ransac). |
| `match_rel_pose_ransac` | RANSAC estimation of the relative pose from point correspondences (match_rel_pose_ransac). |
| `measure_profile_sheet_of_light` | Extract the laser-line (maximum brightness) row position = height profile in each column |
| `photometric_stereo` | Recover normals and albedo from multiple illumination images (Lambertian) (photometric_stereo). |
| `reconst3d_from_fundamental_matrix` | Decompose the relative pose via the fundamental matrix and triangulate the correspondences (reconst3d_from_fundamental_matrix). |
| `reconstruct_height_field_from_gradient` | Integrate a gradient field (dz/dr, dz/dc) with Frankot-Chellappa to recover the height field z |
| `reconstruct_points_stereo` | Reconstruct 3D points from left/right correspondences (matching rows) via disparity (reconstruct_points_stereo). |
| `reconstruct_surface_stereo` | Reconstruct a 3D point cloud (surface) from an entire disparity map (reconstruct_surface_stereo). |
| `reconstruct_surface_structured_light` | Structured-light phase decoding → disparity → 3D surface reconstruction (reconstruct_surface_structured_light). |
| `rel_pose_to_fundamental_matrix` | Compute the fundamental matrix F from the relative pose (R,t) and intrinsics (rel_pose_to_fundamental_matrix). |
| `select_grayvalues_from_channels` | Pick a gray value per pixel from a multi-channel stack according to an index image |
| `sfs_mod_lr` | Shape-from-Shading (modified linear, sfs_mod_lr). Shares the Pentland implementation. |
| `sfs_orig_lr` | Shape-from-Shading (original linear, sfs_orig_lr). Shares the Pentland implementation. |
| `sfs_pentland` | Recover a height field with Pentland's linearized Shape-from-Shading (sfs_pentland). |
| `uncalibrated_photometric_stereo` | Photometric stereo with unknown light directions (rank-3 approximation via SVD, uncalibrated_photometric_stereo). |
| `vector_to_essential_matrix` | Estimate the essential matrix E from 8+ correspondences of a calibrated pair. |
| `vector_to_fundamental_matrix` | Estimate the fundamental matrix F from 8+ correspondences with the normalized 8-point method. |
| `vector_to_fundamental_matrix_distortion` | RANSAC estimation of the fundamental matrix including distortion (assumes small distortion, normalized 8-point) |
| `vector_to_rel_pose` | Estimate the relative pose (R,t) from point correspondences and intrinsics (essential-matrix decomposition) (vector_to_rel_pose). |

#### 3D Object Model (40 ops)

Operations on point clouds and meshes (3D object models): transforms, normals, simplification, features, and more.

| op | Description |
|---|---|
| `affine_trans_object_model_3d` | Apply the rigid transform R·p + t to all points. |
| `area_object_model_3d` | Return the convex-hull surface area of a 3D point cloud (area_object_model_3d). |
| `connection_object_model_3d` | Group nearby points via Euclidean clustering (Rusu 2009). |
| `convex_hull_object_model_3d` | Return the vertices of the 3D convex hull (convex_hull_object_model_3d). |
| `distance_object_model_3d` | Minimum point-to-point distance between two 3D models (distance_object_model_3d). |
| `edges_object_model_3d` | Extract points with high local curvature = 3D edges (edges_object_model_3d). Judged by the planarity of a neighborhood PCA. |
| `fit_primitives_object_model_3d` | Robustly fit the dominant plane with RANSAC. |
| `fuse_object_model_3d` | Fuse multiple 3D models into one (fuse_object_model_3d). |
| `gen_box_object_model_3d` | Point cloud of the 6 faces of a box (gen_box_object_model_3d). |
| `gen_cylinder_object_model_3d` | Point cloud of a cylinder's side surface (gen_cylinder_object_model_3d). |
| `gen_empty_object_model_3d` | Empty 3D model (gen_empty_object_model_3d). |
| `gen_object_model_3d_from_points` | Build a 3D point-cloud model from x,y,z arrays (gen_object_model_3d_from_points). |
| `gen_plane_object_model_3d` | Grid of points on the z=0 plane (gen_plane_object_model_3d). |
| `gen_sphere_object_model_3d` | Quasi-uniform points on a sphere (golden spiral, gen_sphere_object_model_3d). |
| `gen_sphere_object_model_3d_center` | Sphere point cloud with a specified center (gen_sphere_object_model_3d_center). |
| `intersect_plane_object_model_3d` | Return points near the plane (a,b,c,d) (distance < tol) = the cross-section (intersect_plane_object_model_3d). |
| `max_diameter_object_model_3d` | Maximum diameter of a point cloud (farthest two points on the convex hull, max_diameter_object_model_3d). |
| `moments_object_model_3d` | Return the centroid and covariance (2nd central moments) of a 3D point cloud (moments_object_model_3d). |
| `object_model_3d_to_xyz` | 3D point cloud to X/Y/Z images (grid order, object_model_3d_to_xyz). |
| `prepare_object_model_3d` | Model preprocessing with normal estimation (neighborhood PCA, prepare_object_model_3d). |
| `project_object_model_3d` | Project a world point cloud (N,3) to pixels and return (uv, depth). |
| `projective_trans_object_model_3d` | Apply a 4x4 projective transform (projective_trans_object_model_3d). Default is the identity. |
| `reduce_object_model_3d_by_view` | Keep only the front keep-fraction of points along a given axis (simple view-based thinning, reduce_object_model_3d_by_view). |
| `register_object_model_3d_global` | Point-to-plane ICP: align src to dst by minimizing distances along the normals. |
| `register_object_model_3d_pair` | ICP (iterative closest point): align src to dst without known correspondences. |
| `render_object_model_3d` | Render a 3D model to an image (shaded by depth, render_object_model_3d). |
| `rigid_trans_object_model_3d` | Apply a 4x4 rigid/similarity transform to a point cloud (rigid_trans_object_model_3d). |
| `sample_object_model_3d` | Downsampling that thins to one point per occupied voxel (cell centroid). |
| `segment_object_model_3d` | Split a point cloud into connected components by neighbor distance (segment_object_model_3d). Returns a label array. |
| `select_object_model_3d` | Select points by attribute value range (select_object_model_3d). |
| `select_points_object_model_3d` | Select points by value range along a given axis (select_points_object_model_3d). |
| `simplify_object_model_3d` | Simplify a point cloud by voxel-grid averaging (simplify_object_model_3d). |
| `smallest_bounding_box_object_model_3d` | Compute the oriented bounding box via PCA. |
| `smallest_sphere_object_model_3d` | Approximate smallest enclosing sphere (center = centroid, radius = farthest point, smallest_sphere_object_model_3d). |
| `smooth_object_model_3d` | Smooth by moving each point to the centroid of its k nearest neighbors (smooth_object_model_3d). |
| `surface_normals_object_model_3d` | Estimate per-point normals via local PCA of the k nearest neighbors. |
| `triangulate_object_model_3d` | Delaunay triangulation after projecting onto the principal plane (triangulate_object_model_3d). Returns triangle vertex indices. |
| `union_object_model_3d` | Merge two 3D models (union_object_model_3d). |
| `volume_object_model_3d_relative_to_plane` | Approximate the volume of the point cloud above the plane (a,b,c,d) by its convex hull (volume_object_model_3d_relative_to_plane). |
| `xyz_to_object_model_3d` | From X/Y/Z images (each 2D) to a 3D point-cloud model (xyz_to_object_model_3d). |

#### gray (40 ops)

Grayscale morphology and other morphological processing performed directly on gray-value images.


![fops_gray](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_gray.png)
*Figure: gray ops in action — on unevenly lit, low-contrast input, global histogram equalization tends to break down (blown-out highlights, amplified noise), while clahe (contrast-limited adaptive histogram equalization) recovers tonal range locally (actual Fullseye output). Inputs: 2 AI-generated images (Gemini) + the moon image bundled with skimage.*

| op | Description |
|---|---|
| `clahe` | gray op (HALCON: -) |
| `cv_clahe` | gray op (HALCON: -) |
| `cv_trunc` | gray op (HALCON: scale_image) |
| `equ_histo_image` | gray op (HALCON: equ_histo_image) |
| `equ_histo_image_rect` | gray op (HALCON: equ_histo_image_rect) |
| `equalize` | gray op (HALCON: equ_histo_image) |
| `f2_bit_slice` | gray op (HALCON: bit_slice) |
| `f2_expand_domain` | gray op (HALCON: expand_domain_gray) |
| `f2_lut_trans` | gray op (HALCON: lut_trans) |
| `gamma` | gray op (HALCON: pow_image) |
| `gamma_image` | gray op (HALCON: gamma_image) |
| `illuminate` | gray op (HALCON: illuminate) |
| `invert` | gray op (HALCON: invert_image) |
| `invert_image` | gray op (HALCON: invert_image) |
| `it_bit_lshift` | gray op (HALCON: bit_lshift) |
| `it_bit_mask` | gray op (HALCON: bit_mask) |
| `it_bit_rshift` | gray op (HALCON: bit_rshift) |
| `it_convert_image_type` | gray op (HALCON: convert_image_type) |
| `monotony` | gray op (HALCON: monotony) |
| `pow_image` | gray op (HALCON: pow_image) |
| `scale_clip` | gray op (HALCON: scale_image) |
| `scale_image` | gray op (HALCON: scale_image) |
| `scale_image_max` | gray op (HALCON: scale_image_max) |
| `sigmoid` | gray op (HALCON: scale_image_max) |
| `sk_adapthist` | gray op (HALCON: -) |
| `sk_adjust_log` | gray op (HALCON: log_image) |
| `sk_autolevel` | gray op (HALCON: scale_image_max) |
| `sk_enhance_contrast` | gray op (HALCON: -) |
| `xcv_detail_enhance` | gray op (HALCON: -) |
| `xkor_clahe` | gray op (HALCON: -) |
| `xpil_autocontrast` | gray op (HALCON: -) |
| `xpil_contrast` | gray op (HALCON: -) |
| `xpil_detail` | gray op (HALCON: -) |
| `xpil_edge_enhance` | gray op (HALCON: -) |
| `xpil_posterize` | gray op (HALCON: -) |
| `xpil_solarize` | gray op (HALCON: -) |
| `xsk3_integral_image` | gray op (HALCON: -) |
| `xsk3_rank_equalize` | gray op (HALCON: -) |
| `xsk3_rank_subtract_mean` | gray op (HALCON: -) |
| `xsp_detrend_flatten` | gray op (HALCON: -) |

#### Matching (37 ops)

Template matching and shape matching. The "find the shape I taught you, anywhere" department — the crown jewel of industrial image processing.

| op | Description |
|---|---|
| `adapt_shape_model_high_noise` | Build a shape model with stronger smoothing for high-noise images (adapt_shape_model_high_noise). |
| `create_aniso_shape_model` | Anisotropic-scale shape model (create_aniso_shape_model; the model itself is identical, find searches anisotropic scales). |
| `create_aniso_shape_model_xld` | Anisotropic-scale shape model from XLD contours (create_aniso_shape_model_xld). |
| `create_calib_descriptor_model` | Calibrated descriptor model (create_calib_descriptor_model). |
| `create_generic_shape_model` | Generic shape model (create_generic_shape_model, same core as create_shape_model). |
| `create_local_deformable_model` | Model for local deformable matching (keeps the template) (create_local_deformable_model). |
| `create_local_deformable_model_xld` | Local deformable model derived from XLD (create_local_deformable_model_xld). |
| `create_ncc_model` | Prepare an NCC model (= normalized template) (create_ncc_model). |
| `create_planar_calib_deformable_model` | Planar (calibrated) deformable model (create_planar_calib_deformable_model). |
| `create_planar_calib_deformable_model_xld` | Planar calibrated deformable model derived from XLD (create_planar_calib_deformable_model_xld). |
| `create_planar_uncalib_deformable_model` | Planar (uncalibrated) deformable model (create_planar_uncalib_deformable_model). |
| `create_planar_uncalib_deformable_model_xld` | Planar uncalibrated deformable model derived from XLD (create_planar_uncalib_deformable_model_xld). |
| `create_scaled_shape_model` | Isotropic-scale shape model (create_scaled_shape_model). |
| `create_scaled_shape_model_xld` | Scale-capable shape model from XLD contours (create_scaled_shape_model_xld). |
| `create_shape_model` | Model the normalized gradient vectors of the template's edge points (/grad/>min_grad) (create_shape_model). |
| `create_shape_model_xld` | Build a shape model from XLD contours (create_shape_model_xld). |
| `create_uncalib_descriptor_model` | Uncalibrated descriptor model (Harris keypoints + normalized patches) (create_uncalib_descriptor_model). |
| `determine_deformable_model_params` | Determine recommended parameters for a deformable model (determine_deformable_model_params). |
| `determine_ncc_model_params` | Determine recommended NCC model parameters (contrast / number of levels) (determine_ncc_model_params). |
| `determine_shape_model_params` | Auto-determine the recommended min_grad / contrast from the template (determine_shape_model_params). |
| `find_aniso_shape_model` | Shape model detection with independent row/column scales (anisotropic) (find_aniso_shape_model). |
| `find_aniso_shape_models` | Multi-instance detection at anisotropic scales (find_aniso_shape_models). |
| `find_calib_descriptor_model` | Detect a calibrated descriptor model → planar pose (find_calib_descriptor_model). |
| `find_generic_shape_model` | Generic shape model detection (find_generic_shape_model). Alias of find_shape_model. |
| `find_local_deformable_model` | Coarsely align the rigid position, then estimate local deformation with optical flow |
| `find_ncc_model` | Search the image for an NCC model and return the best match (row/col/score) (find_ncc_model). |
| `find_ncc_models` | Multi-instance NCC model detection (find_ncc_models). |
| `find_planar_calib_deformable_model` | Detect a planar calibrated deformable model (find_planar_calib_deformable_model). |
| `find_planar_uncalib_deformable_model` | Detect a planar uncalibrated deformable model (find_planar_uncalib_deformable_model). |
| `find_scaled_shape_model` | Search for the best match while varying scale (find_scaled_shape_model). |
| `find_scaled_shape_models` | Multi-instance detection with scale search (find_scaled_shape_models). |
| `find_shape_models` | Detect multiple instances with non-maximum suppression (find_shape_models). |
| `find_uncalib_descriptor_model` | Detect a descriptor model in an image (ratio test + RANSAC homography) |
| `get_shape_model_contours` | Return the shape model's edge points as contours (get_shape_model_contours). |
| `get_shape_model_origin` | Return the shape model's origin (centroid) (get_shape_model_origin). |
| `inspect_shape_model` | Return the shape model's edge point count, extent, and origin for inspection (inspect_shape_model). |
| `set_shape_model_origin` | Set the shape model's reference origin (set_shape_model_origin). |

#### XLD (35 ops)

XLD = a subpixel-accurate contour representation. Handling contours at finer-than-pixel precision — the backbone of precision measurement.


![fops_xld](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_xld.png)
*Figure: XLD ops in action — a binarized boundary can only ever be a staircase on the pixel grid, but threshold_sub_pix returns a contour (XLD) whose level-crossing positions are estimated at finer-than-pixel (subpixel) precision. Mean error of 0.001 px measured on synthetic circles with ground truth. At 8x magnification the difference between the staircase and the smooth contour is visible (actual Fullseye output). Inputs: our own synthetics, AI-generated (Gemini), and skimage coins.*

| op | Description |
|---|---|
| `difference_closed_contours_xld` | Difference of two closed contours (difference_closed_contours_xld). |
| `difference_closed_polygons_xld` | Difference of two closed polygons (difference_closed_polygons_xld). |
| `gen_circle_contour_xld` | Generate a circular-arc contour (gen_circle_contour_xld). |
| `gen_contour_nurbs_xld` | Generate a NURBS (B-spline) contour from control points (gen_contour_nurbs_xld). |
| `gen_contour_polygon_rounded_xld` | Generate a polygon contour with rounded corners (gen_contour_polygon_rounded_xld). |
| `gen_contour_polygon_xld` | Generate a polygon contour from a point sequence (gen_contour_polygon_xld). |
| `gen_contours_skeleton_xld` | Extract the skeleton of a region and convert it into contours (one per branch) (gen_contours_skeleton_xld). |
| `gen_cross_contour_xld` | Generate a cross-marker contour (gen_cross_contour_xld). |
| `gen_ellipse_contour_xld` | Generate an elliptical-arc contour (gen_ellipse_contour_xld). |
| `gen_nurbs_interp` | NURBS interpolating contour through given points (gen_nurbs_interp). |
| `gen_parallels_xld` | Generate offset contours parallel to each contour (gen_parallels_xld). |
| `gen_rectangle2_contour_xld` | Generate the contour of a rotated rectangle (gen_rectangle2_contour_xld). |
| `get_contour_angle_xld` | Return the tangent angle (radians) at each point along a contour (get_contour_angle_xld). |
| `get_polygon_xld` | Approximate a contour by a polygon with Douglas-Peucker (get_polygon_xld). Returns the vertex sequence. |
| `get_regress_params_xld` | Regression-line parameters for contour points (normal angles nr,nc and origin distance dist) (get_regress_params_xld). |
| `intersection_closed_contours_xld` | Intersection of two closed contours (intersection_closed_contours_xld). |
| `intersection_closed_polygons_xld` | Intersection of two closed polygons (intersection_closed_polygons_xld). |
| `intersection_region_contour_xld` | Intersection region of a region and a closed contour (intersection_region_contour_xld). |
| `local_max_contours_xld` | Extract points on a contour where the gray value is a local maximum (local_max_contours_xld). |
| `max_parallels_xld` | Parallel contours up to a maximum distance (max_parallels_xld). |
| `merge_cont_line_scan_xld` | Connect contour endpoints across adjacent frames of a line-scan (strip) acquisition (merge_cont_line_scan_xld). |
| `mod_parallels_xld` | Generate parallel contours (parameter-modified version) (mod_parallels_xld). |
| `moments_any_points_xld` | Area, centroid, and 2nd moments of a contour point set (moments_any_points_xld). |
| `segment_contour_attrib_xld` | Split a contour at points where an attribute of the underlying gray values changes abruptly (segment_contour_attrib_xld). |
| `segment_contours_xld` | Split contours into line segments (segment_contours_xld). |
| `symm_difference_closed_contours_xld` | Symmetric difference of two closed contours (symm_difference_closed_contours_xld). |
| `symm_difference_closed_polygons_xld` | Symmetric difference of two closed polygons (symm_difference_closed_polygons_xld). |
| `test_xld_point` | Whether a point lies inside a closed contour (crossing-number method) (test_xld_point). |
| `union2_closed_contours_xld` | Union of two closed contours (union2_closed_contours_xld). |
| `union2_closed_polygons_xld` | Union of two closed polygons (union2_closed_polygons_xld). |
| `union_cocircular_contours_xld` | Merge cocircular (same-circle) contours (union_cocircular_contours_xld). |
| `union_collinear_contours_ext_xld` | Collinear merging (extended-parameter version) (union_collinear_contours_ext_xld). |
| `union_collinear_contours_xld` | Merge collinear contour fragments (union_collinear_contours_xld). |
| `union_cotangential_contours_xld` | Merge tangent-continuous contours (union_cotangential_contours_xld). |
| `union_straight_contours_xld` | Merge straight contours (union_straight_contours_xld). |

#### Calibration (34 ops)

Camera calibration (intrinsic and extrinsic parameters, lens distortion). The foundation for "translating pixels into millimeters" (the Brown distortion model from Section 14.4 lives here too).

![Example of Calibration](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_12_radial_distortion.png)
*Figure: lens distortion model examples (barrel / pincushion) (reprised from Section 11.1.1)*

| op | Description |
|---|---|
| `affine_trans_point_3d` | Apply a 4x4 homogeneous affine transform to a 3D point (affine_trans_point_3d). |
| `binocular_calibration` | Calibrate the left and right cameras individually with Zhang's method and estimate the stereo relative pose (binocular_calibration). |
| `calibrate_cameras` | Zhang camera calibration (calibrate_cameras). Alias of camera_calibration. |
| `calibrate_hand_eye` | Hand-eye calibration (calibrate_hand_eye). Alias of hand_eye_calibration. |
| `caltab_points` | Return the ideal mark coordinates of the calibration plate (world, mm) (caltab_points). |
| `cam_mat_to_cam_par` | Extract fx, fy, cx, cy, skew from the intrinsic matrix K. |
| `cam_par_pose_to_hom_mat3d` | Convert a camera pose [rx,ry,rz(rad), tx,ty,tz] to a 4x4 homogeneous transform matrix (cam_par_pose_to_hom_mat3d). |
| `cam_par_to_cam_mat` | Assemble the pinhole intrinsic matrix K from fx, fy, cx, cy, skew. |
| `camera_calibration` | Estimate the intrinsic matrix K from multiple views of a planar target with Zhang's method (camera_calibration). |
| `change_radial_distortion_cam_par` | Replace the radial distortion coefficient in the camera parameters with kappa_new (change_radial_distortion_cam_par). |
| `change_radial_distortion_image` | Apply radial distortion r' = r(1 + kappa r^2) to an image and resample (change_radial_distortion_image). |
| `change_radial_distortion_points` | Apply radial and tangential lens distortion to ideal pixels (Brown model). |
| `contour_to_world_plane_xld` | Map an XLD contour (dict {cs:[Nx2]}) to the world plane (contour_to_world_plane_xld). |
| `create_caltab` | Create the calibration plate description (ideal points) (create_caltab). |
| `create_pose` | Create a 3D pose. |
| `disp_caltab` | Return a calibration plate image (for display) (disp_caltab). |
| `find_calib_object` | Detect the calibration object (marks) (find_calib_object). Alias of find_caltab. |
| `find_caltab` | Detect the circular mark centers of the calibration plate in an image (centroids of connected components) (find_caltab). |
| `find_marks_and_pose` | Mark detection + calibration plate pose estimation (PnP approximation = planar homography) (find_marks_and_pose). |
| `gen_caltab` | Generate a calibration plate image with a grid of circular marks (gen_caltab). |
| `gen_image_to_world_plane_map` | Generate the mapping table from the image to the world plane (z=0) (gen_image_to_world_plane_map). |
| `gen_radial_distortion_map` | Generate the inverse map (row_map, col_map) of radial distortion (gen_radial_distortion_map). |
| `get_line_of_sight` | Return the line-of-sight direction (normalized 3D vector) of pixel (row,col) (get_line_of_sight). |
| `hand_eye_calibration` | Solve AX=XB from a series of motion pairs and estimate X (4x4) (hand_eye_calibration). |
| `image_points_to_world_plane` | Back-project pixels to the world plane z=0 from camera intrinsics/extrinsics (image_points_to_world_plane). |
| `image_to_world_plane` | Map image points to the world plane (z=0) via a planar homography (image_to_world_plane). |
| `project_3d_point` | Perspective-project a 3D point into the camera and return the pixel (row, col) (project_3d_point). |
| `project_hom_point_hom_mat3d` | Project a homogeneous 3D point (4,) with a 3x4/4x4 matrix (project_hom_point_hom_mat3d). |
| `project_point_hom_mat3d` | Transform and project a 3D point with a 4x4 or 3x4 homogeneous transform (project_point_hom_mat3d). |
| `projective_trans_point_2d` | Project a homogeneous 2D point with a projective transform matrix. |
| `radial_distortion_self_calibration` | Estimate the radial distortion kappa by minimizing residuals of point sequences that should be straight lines (plumb-line method) |
| `radiometric_self_calibration` | Estimate the camera response function (inverse-response LUT) from images at different exposures |
| `sim_caltab` | Simulate an image of the calibration plate projected at a given camera pose (sim_caltab). |
| `stationary_camera_self_calibration` | Estimate the intrinsic matrix K from rotation-only infinite homographies H = K R K^-1 |

#### morphology (33 ops)

Binary morphology (dilation, erosion, opening, closing). The classics of noise removal and shape cleanup — still on active duty.

![Example of morphology](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_06_opening_circle.png)
*Figure: opening example (reprised from Section 11.1.1)*

| op | Description |
|---|---|
| `bothat` | morphology op (HALCON: gray_bothat) |
| `cv_blackhat` | morphology op (HALCON: gray_bothat) |
| `cv_close` | morphology op (HALCON: gray_closing) |
| `cv_dilate` | morphology op (HALCON: gray_dilation) |
| `cv_erode` | morphology op (HALCON: gray_erosion) |
| `cv_gradient` | morphology op (HALCON: gray_range_rect) |
| `cv_open` | morphology op (HALCON: gray_opening) |
| `cv_tophat` | morphology op (HALCON: gray_tophat) |
| `f2_gray_inside` | morphology op (HALCON: gray_inside) |
| `f2_gray_skeleton` | morphology op (HALCON: gray_skeleton) |
| `gclose` | morphology op (HALCON: gray_closing) |
| `gdilate` | morphology op (HALCON: gray_dilation) |
| `gerode` | morphology op (HALCON: gray_erosion) |
| `gopen` | morphology op (HALCON: gray_opening) |
| `gray_bothat` | morphology op (HALCON: gray_bothat) |
| `gray_closing` | morphology op (HALCON: gray_closing) |
| `gray_closing_rect` | morphology op (HALCON: gray_closing_rect) |
| `gray_closing_shape` | morphology op (HALCON: gray_closing_shape) |
| `gray_dilation` | morphology op (HALCON: gray_dilation) |
| `gray_dilation_shape` | morphology op (HALCON: gray_dilation_shape) |
| `gray_erosion` | morphology op (HALCON: gray_erosion) |
| `gray_erosion_shape` | morphology op (HALCON: gray_erosion_shape) |
| `gray_opening` | morphology op (HALCON: gray_opening) |
| `gray_opening_rect` | morphology op (HALCON: gray_opening_rect) |
| `gray_opening_shape` | morphology op (HALCON: gray_opening_shape) |
| `gray_tophat` | morphology op (HALCON: gray_tophat) |
| `morph_grad` | morphology op (HALCON: gray_range_rect) |
| `sk_area_opening` | morphology op (HALCON: -) |
| `tophat` | morphology op (HALCON: gray_tophat) |
| `xsk2_diameter_opening` | morphology op (HALCON: -) |
| `xsk2_reconstruction` | morphology op (HALCON: -) |
| `xsk3_area_closing` | morphology op (HALCON: -) |
| `xsk3_diameter_closing` | morphology op (HALCON: -) |

#### geometry (28 ops)

Fitting and computing geometric primitives — points, lines, circles. The ops that turn measurement results into "the language of shapes."


![fops_geometry](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_geometry.png)
*Figure: geometry ops in action — structures along a circle (the ring brightness of a black hole, gear teeth, tree rings) can't be measured with straight-line tools, but unrolling into polar coordinates with polar_trans_image lays them out in a single row, so 1D profiles and straight-line inspection work as-is (actual Fullseye output). Inputs: the EHT Collaboration's M87* (CC BY 4.0) + 2 AI-generated images (Gemini).*

| op | Description |
|---|---|
| `affine_trans_image` | geometry op (HALCON: affine_trans_image) |
| `affine_trans_image_size` | geometry op (HALCON: affine_trans_image_size) |
| `affine_trans_region` | geometry op (HALCON: affine_trans_region) |
| `affine_warp` | geometry op (HALCON: affine_trans_image) |
| `it_add_image_border` | geometry op (HALCON: add_image_border) |
| `it_change_format` | geometry op (HALCON: change_format) |
| `it_crop_part` | geometry op (HALCON: crop_part) |
| `it_crop_rectangle1` | geometry op (HALCON: crop_rectangle1) |
| `mirror_image` | geometry op (HALCON: mirror_image) |
| `mirror_region` | geometry op (HALCON: mirror_region) |
| `polar_trans_image` | geometry op (HALCON: polar_trans_image) |
| `polar_trans_image_ext` | geometry op (HALCON: polar_trans_image_ext) |
| `polar_trans_image_inv` | geometry op (HALCON: polar_trans_image_inv) |
| `polar_trans_region_inv` | geometry op (HALCON: polar_trans_region_inv) |
| `projective_trans_image` | geometry op (HALCON: projective_trans_image) |
| `projective_trans_image_size` | geometry op (HALCON: projective_trans_image_size) |
| `projective_trans_region` | geometry op (HALCON: projective_trans_region) |
| `rescale_img` | geometry op (HALCON: zoom_image_size) |
| `rotate_image` | geometry op (HALCON: rotate_image) |
| `rotate_img` | geometry op (HALCON: rotate_image) |
| `sk_swirl` | geometry op (HALCON: polar_trans_image) |
| `tf_log_polar` | geometry op (HALCON: -) |
| `transpose_region` | geometry op (HALCON: transpose_region) |
| `xcv2_warp_logpolar` | geometry op (HALCON: -) |
| `xpil_offset` | geometry op (HALCON: -) |
| `zoom_image_factor` | geometry op (HALCON: zoom_image_factor) |
| `zoom_image_size` | geometry op (HALCON: zoom_image_size) |
| `zoom_region` | geometry op (HALCON: zoom_region) |

#### 3dgs (26 ops)

3D Gaussian Splatting and friends. 3D reconstruction, rendering, and meshing from multi-view images — the cutting edge of this toolbox.

| op | Description |
|---|---|
| `animate_mesh` | Animate a ground-truth mesh along a qpos trajectory (can also composite a static terrain mesh) |
| `bin_pick_gif` | Bin picking rendered headless to a GIF: pick a part from a jumbled bin by candidate scoring, grasp it from above with 6DoF IK, and lift it out of the bin (no GPU needed; success count measured by whether the part actually left the bin) |
| `capture_orbit` | Capture an orbit of a sim scene and turn it into a 3DGS dataset (transforms.json) |
| `event_camera` | Mimic an event camera (DVS) with a log-brightness-change model and generate ON/OFF event streams. Verified by measurement that it fires on moving edges (no GPU needed) |
| `evis_perceive` | Perceive a GPU-trained evis rollout (qpos npy) with Fullseye: 3-pane GIF of RGB/depth/DVS (with ego_body= for the robot's viewpoint = 4-pane head-mounted RGB/depth/DVS) |
| `figure8` | Turning-control practice/calibration: draw figure-8-style curves at various sizes with differential steering (bird's-eye track, no GPU needed) |
| `focus_stack` | Generate a focus stack with depth-of-field blur from ground-truth depth and composite an all-in-focus image by local sharpness maximum (also recovers focus-derived depth, no GPU needed) |
| `g1_perceive_real` | Perceive with the G1's real sensor specs: Livox Mid-360 (top of head, 360°/-7..+52°) BEV point cloud + RealSense D435i (87°×58°, 0.3-6 m band) RGB/depth in a 4-pane GIF. obstacles=True places static verification obstacles off the walking path (giving the sensors something to see) |
| `g1_training_curves` | Parse the progress lines of G1 training logs (step/reward/ep_len/perr/crash…) into a dict of arrays — plot training curves in Studio without touching the GPU machine |
| `g1_walk_policy` | Run a GPU-trained G1 walking policy (brax ckpt) on Windows alone: numpy inference (verified numerically identical to brax) + native MuJoCo rollout → measured distance/survival/lateral RMS + follow-camera video. vision=True for the pseudo-LiDAR + obstacles visual walking version |
| `hurdle_physics` | A real-physics long jump as GIF + trajectory telemetry: go2 runs up, leaps explosively over an obstacle (barrier), and lands on the far side (cleared / upright measured, no GPU needed) |
| `jump_physics` | A real-physics jump as GIF + height telemetry: go2 crouches → explosive extension → ballistic flight (all feet off the ground = zero contacts, measured) → landing (jump height / airtime measured, friction and gravity included, no GPU needed) |
| `lidar_scan` | Simulate a spinning LIDAR with real mj_ray raycasts, generating and visualizing point clouds (no GPU needed; hit rate etc. measured) |
| `long_route` | go2 walks a long undulating terrain of varying roughness all the way (default 100 m) under real physics (distance/upright measured, no GPU needed) |
| `pick_gif` | Pick-and-place rendered headless to a GIF: a robot arm (Panda) grasps a cube with real contact and friction and places it elsewhere (no GPU needed; grasp success judged by the measured height of the box) |
| `polarization` | Mimic a polarization camera with a forward Fresnel model (normals → DoLP/AoLP → 4 polarization images → Stokes). Polarization encodes surface orientation even on textureless surfaces (for transparent/specular grasping, no GPU needed) |
| `pseudo_lidar` | Planar pseudo-LiDAR scan (K normalized distances over a forward arc). Numpy parity with the exact observation geometry of the G1VisionWalk walking policy — compute the input the policy eats as a standalone tool |
| `render_walk_gif` | Kinematic preview of a walker placed on terrain, rendered headless to a GIF (no contacts; visualizes motion/gait. For physical walking use walk_physics) |
| `route_planning` | Real-physics navigation: go2 looks ahead at obstacles with raycasts, picks candidate headings by pyramid search (coarse → fine), avoids them with differential steering, and reaches the goal (with a bird's-eye plan, no GPU needed) |
| `sensor_fusion` | Fuse a position sensor (camera/GPS) and a velocity sensor (IMU) with a Kalman filter to track a projectile. Generates a figure that honestly compares the fused RMSE against each sensor alone (no GPU needed) |
| `stereo_depth` | Render a stereo pair from two parallel cameras, estimate depth by block matching, and compare errors against ground-truth depth (uses the existing stereo.py, no GPU needed) |
| `sugar_mesh` | Surface-align 3DGS SuGaR-style → extract a mesh with Poisson (with ground-truth bbox verification) |
| `train_3dgs` | Train 3DGS on a sim scene with native gsplat (fast) |
| `train_3dgs_densify` | 3DGS training with densify + SH + antialiased (high quality) |
| `tsdf_mesh` | TSDF-fuse perfect sim depth into a clean watertight mesh (no GPU needed, no spikes) |
| `walk_physics` | Walk go2 over a rough height field with torque PD control + closed-loop balance + mj_step under real physics (gravity, friction, contact, inertia), capturing the body tilting as GIF + telemetry (upright/forward-progress/tilt measured, no GPU needed) |

#### Regions (26 ops)

A HALCON-compatible superset for region processing (extended version of the region category).


![fops_regions](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_regions.png)
*Figure: Regions ops in action — real-world binary images are riddled with grain noise and holes, and labeling them as-is miscounts. The standard recipe of region processing: erase the grains with opening_circle (opening), fill the holes with fill_up, then split into connected components (actual Fullseye output). Inputs: 2 AI-generated (Gemini) + 1 bundled sample, binarized with artificial dirt added.*

| op | Description |
|---|---|
| `difference` | Region difference region \ sub (difference). |
| `find_neighbors` | Return the indices of adjacent pairs in a region list (dilate and test for intersection) (find_neighbors). |
| `gen_random_region` | Generate a random connected region (boundary accretion = exact area + connectivity guaranteed) (gen_random_region). |
| `gen_random_regions` | Generate multiple random regions (gen_random_regions). |
| `gen_rectangle1` | Generate an axis-parallel rectangular region (gen_rectangle1). |
| `gen_region_histo` | Draw a 1D histogram as a bar-chart region (gen_region_histo). |
| `gen_region_hline` | Generate horizontal line-segment regions (gen_region_hline). rows: sequence of row indices. |
| `gen_region_line` | Turn a line segment into a region (gen_region_line, DDA). |
| `gen_region_points` | Turn individual pixels into a region (gen_region_points). |
| `gen_region_polygon` | Turn a polygon outline into a region (gen_region_polygon). |
| `gen_region_polygon_filled` | Fill a polygon into a region (gen_region_polygon_filled). |
| `gen_region_runs` | Generate a region from run-length codes [(row, col_start, col_end), ...] (gen_region_runs). |
| `get_region_points` | The (row, col) coordinate arrays of the region's pixels (get_region_points). |
| `get_region_polygon` | Return the polygon-approximation vertices of the region outline (get_region_polygon). |
| `get_region_runs` | Run-length representation of the region [(row, col_start, col_end), ...] (get_region_runs). |
| `hamming_distance` | Hamming distance between two regions (number of differing pixels) (hamming_distance). |
| `hamming_distance_norm` | Normalized Hamming distance (differing pixels / union pixels) (hamming_distance_norm). |
| `intersection` | Region intersection (intersection). |
| `merge_regions_line_scan` | Connect the run sets from a line scan and merge them into regions (merge_regions_line_scan). |
| `select_region_spatial` | Select regions satisfying a given spatial relation to a reference region (select_region_spatial). |
| `select_shape_proto` | Select regions whose shape features are close to a prototype region (select_shape_proto). |
| `spatial_relation` | Spatial relation of two regions (above/below/left/right) based on their centroid directions (spatial_relation). |
| `symm_difference` | Symmetric difference (symm_difference). |
| `test_equal_region` | Whether two regions are equal (test_equal_region). |
| `test_subset_region` | Whether region1 ⊆ region2 (test_subset_region). |
| `union2` | Region union (union2). |

#### contour (26 ops)

Contour extraction, smoothing, splitting, and attribute computation.


![fops_contour](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/ops/fops_contour.png)
*Figure: contour ops in action — thin linear structures (blood vessels, wing veins, leaf veins, cracks) come out doubled under edge detection (edges on both sides of the line), but lines_gauss (Frangi ridge response) grabs the band of the linear structure and skeleton thins it to a 1-pixel-wide centerline. Blood vessels, wing veins, leaf veins, and cracks are all measured with the same math (actual Fullseye output). All inputs are AI-generated images (Gemini). The medical-looking input is not for diagnostic use.*

| op | Description |
|---|---|
| `FindContours` | Contour extraction from binary/level images (cv2.findContours; skimage if absent, numpy otherwise)  [backend=opencv] |
| `affine_trans_contour_xld` | contour op (HALCON: affine_trans_contour_xld) |
| `affine_trans_polygon_xld` | contour op (HALCON: affine_trans_polygon_xld) |
| `close_contours_xld` | contour op (HALCON: close_contours_xld) |
| `contour_point_num_xld` | contour op (HALCON: contour_point_num_xld) |
| `contours_to_region` | contour op (HALCON: gen_region_contour_xld) |
| `edges_color_sub_pix` | contour op (HALCON: edges_color_sub_pix) |
| `edges_sub_pix` | contour op (HALCON: edges_sub_pix) |
| `fit_line_contours` | contour op (HALCON: fit_line_contour_xld) |
| `gen_contour_region_xld` | contour op (HALCON: gen_contour_region_xld) |
| `gen_region_contour_xld` | contour op (HALCON: gen_region_contour_xld) |
| `gen_region_polygon_xld` | contour op (HALCON: gen_region_polygon_xld) |
| `lines_color` | contour op (HALCON: lines_color) |
| `lines_facet` | contour op (HALCON: lines_facet) |
| `lines_gauss` | contour op (HALCON: lines_gauss) |
| `polar_trans_contour_xld` | contour op (HALCON: polar_trans_contour_xld) |
| `projective_trans_contour_xld` | contour op (HALCON: projective_trans_contour_xld) |
| `select_contours` | contour op (HALCON: select_contours_xld) |
| `select_contours_xld` | contour op (HALCON: select_contours_xld) |
| `select_shape_xld` | contour op (HALCON: select_shape_xld) |
| `shape_trans_xld` | contour op (HALCON: shape_trans_xld) |
| `sk_find_contours` | contour op (HALCON: -) |
| `smooth_contours` | contour op (HALCON: smooth_contours_xld) |
| `smooth_contours_xld` | contour op (HALCON: smooth_contours_xld) |
| `threshold_sub_pix` | contour op (HALCON: threshold_sub_pix) |
| `zero_crossing_sub_pix` | contour op (HALCON: zero_crossing_sub_pix) |

#### rank (23 ops)

Rank filters (median and friends). Noise removal based on order statistics — the go-to remedy for salt-and-pepper noise.

![Example of rank](https://raw.githubusercontent.com/furuse-kazufumi/fullsense/main/docs/articles/assets/qiita_games_2026_08/opdemo_02_median_image.png)
*Figure: median filter example (reprised from Section 11.1.1)*

| op | Description |
|---|---|
| `cv_median` | rank op (HALCON: median_image) |
| `dual_rank` | rank op (HALCON: dual_rank) |
| `eliminate_min_max` | rank op (HALCON: eliminate_min_max) |
| `eliminate_sp` | rank op (HALCON: eliminate_sp) |
| `gray_dilation_rect` | rank op (HALCON: gray_dilation_rect) |
| `gray_erosion_rect` | rank op (HALCON: gray_erosion_rect) |
| `gray_range_rect` | rank op (HALCON: gray_range_rect) |
| `max_filter` | rank op (HALCON: gray_dilation_rect) |
| `mean_sp` | rank op (HALCON: mean_sp) |
| `median` | rank op (HALCON: median_image) |
| `median_image` | rank op (HALCON: median_image) |
| `median_rect` | rank op (HALCON: median_rect) |
| `median_separate` | rank op (HALCON: median_separate) |
| `median_weighted` | rank op (HALCON: median_weighted) |
| `min_filter` | rank op (HALCON: gray_erosion_rect) |
| `percentile` | rank op (HALCON: rank_image) |
| `rank_image` | rank op (HALCON: rank_image) |
| `rank_rect` | rank op (HALCON: rank_rect) |
| `sk_median_disk` | rank op (HALCON: median_image) |
| `trimmed_mean` | rank op (HALCON: trimmed_mean) |
| `xkor_median` | rank op (HALCON: -) |
| `xpil_mode_filter` | rank op (HALCON: -) |
| `xsk2_rank_geomean` | rank op (HALCON: -) |
