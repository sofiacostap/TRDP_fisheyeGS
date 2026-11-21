# Native fisheye sparse-view selection study

## 1. Research goal

Determine whether a static, scene-aware image-selection policy can improve sparse native-fisheye DirectFisheye-GS reconstruction over simple pose-only selection at the **same image budget**.

This project does not claim that fewer images cause lower quality. It tests whether, when only a small number of images can be used, some image subsets are measurably more useful than others.

## 2. Research question

> At a fixed sparse budget and with the same DirectFisheye-GS training protocol, does static selection using COLMAP scene visibility and viewing direction improve held-out native-fisheye reconstruction quality over pose-only selection?

Primary budget: **24 training images**.

Harder follow-up budget: **12 training images**.

Scenes: Flowers, Chairs, Globe.

## 3. The three selection methods

| Method | What it selects | Information used | Provenance and status |
|---|---|---|---|
| PCA-angle spacing | Cameras approximately evenly spaced in a PCA-fitted plane through the camera-centre distribution. | Camera centres only. | Custom pose-only baseline. The same deterministic selector is used for Flowers, Chairs, and Globe. |
| 3D angular FPS | Camera directions maximally separated in 3D. | Unit vectors from a reference point to camera centres. | Adaptation of iterative farthest-point sampling from PointNet++ [Qi et al., 2017]. PointNet++ samples point clouds, not GS cameras; this is a pose-only baseline adapted by Shihab. |
| Static visibility-and-direction selector | A complete training subset selected before GS training. | Full COLMAP sparse points, which candidate cameras observe each point, and each point-to-camera viewing direction. | Custom method implemented by Shihab. It is conceptually related to active coverage selection but is **not** the published COVER algorithm. |

### Avoid ambiguous terminology

Use these names in slides and reports:

- **PCA-angle baseline**
- **3D angular-FPS baseline**
- **static visibility-and-direction selector**

Do not call all three methods "coverage". In particular, this is different from **camera-path coverage** (for example, 360, 180, or 90 degrees) and different from **CVO**, which pairs already-selected images during training.

## 4. Relation to papers

### PointNet++

PointNet++ uses iterative farthest-point sampling to cover a point set. The 3D angular-FPS baseline transfers that sampling rule from 3D points to candidate camera directions. This is a reasonable baseline, but the original paper does not claim it selects optimal training cameras for Gaussian Splatting.

Reference: Qi et al., "PointNet++: Deep Hierarchical Feature Learning on Point Sets in a Metric Space," NeurIPS 2017, Section 3.2. <https://arxiv.org/abs/1706.02413>

### COVER

COVER is the closest conceptual camera-selection paper. It derives an active view-selection criterion from approximate Fisher information and chooses new viewpoints that cover geometry insufficiently observed so far. It selects views adaptively while reconstruction develops.

Reference: Chen et al., "Coverage Optimization for Camera View Selection," 2026. <https://arxiv.org/abs/2604.05259>

Our static selector is not COVER: it selects a fixed subset before DirectFisheye-GS training, using already available COLMAP observations. We may describe it as a **static COLMAP-based proxy for scene coverage**, not as an implementation of COVER.

### DirectFisheye-GS

DirectFisheye-GS supports native fisheye images and uses CVO to pair overlapping training views during optimisation. The paper's CVO pairing strategy is not a pre-training image-subset selector.

Reference: Yang et al., "DirectFisheye-GS," 2026. <https://arxiv.org/html/2604.00648v1>

## 5. Clear comparison with regular-camera work

Before claiming a fisheye contribution, create a literature table for PointNet++, COVER, and any further candidate view-selection paper. For every paper, record:

- camera model: pinhole, regular perspective, panoramic, fisheye, or unspecified;
- whether cameras are selected before training or acquired adaptively during training;
- whether poses and geometry are assumed known;
- scene and dataset type;
- image budget;
- evaluation protocol;
- reported improvement over its own matched baseline.

The main comparison should be methodological, not raw PSNR. Absolute metrics from a regular-camera dataset cannot be numerically compared with metrics from Flowers, Chairs, or Globe. Compare the **gain over the matched baseline** instead.

## 6. Controlled experimental protocol

The first study uses shared full-scene COLMAP geometry. This isolates image selection from the separate problem of sparse pose and sparse-point estimation.

Keep fixed within each scene:

- candidate training-image pool and frozen held-out test images;
- full-scene COLMAP reconstruction;
- source code revision and environment;
- native fisheye image handling;
- CVO reciprocal preset and batch size 2;
- resolution behaviour, 30,000 iterations, seed, checkpoints, and evaluation code.

Change only the selected training-image manifest.

## 7. Experiment matrix

### Primary study at 24 views

| Scene | PCA angle | 3D angular FPS | Static visibility-and-direction |
|---|---:|---:|---:|
| Flowers | Run with frozen common protocol | Run with frozen common protocol | Run with frozen common protocol |
| Chairs | Run or audit existing equivalent baseline | New run | New run |
| Globe | Run or audit existing equivalent baseline | New run | New run |

The existing Chairs and Globe uniform-24 runs can be reused only if their manifest rule and all fixed parameters match the frozen shared protocol. Otherwise rerun them as the coordinated PCA-angle baseline.

### Follow-up at 12 views

Repeat the same three selectors after the 24-view experiment gives a clear result. This tests whether selection matters more in the harder sparse regime.

## 8. Evaluation

All methods use the same held-out test images. No test image may appear in the candidate pool or contribute observations to the static selector.

Report:

1. Overall PSNR, SSIM, and LPIPS on the complete frozen test set.
2. Per-test-view metrics.
3. Quality versus angular distance from the nearest selected training camera.
4. Near, intermediate, and far held-out view bins.
5. Matched test renders and error maps.
6. The selected-image manifest and summary statistics: observed COLMAP points, point-direction diversity, and camera-path angular spread.

The per-distance analysis separates withheld interpolation views from far extrapolation views. A global average alone is insufficient for this purpose.

## 9. What is needed before training

### Shihab

1. Share the exact Flowers code for all three selectors.
2. Specify the static selector's scoring equation, candidate filtering, and filename tie-breaking.
3. Confirm whether the Flowers 10 and 20 view runs used identical CVO, seed, resolution, and iteration settings.
4. Reproduce the Flowers manifests and result table from the shared code.

### Sofia

1. Freeze common scene directories, full-scene COLMAP identifiers, test lists, CVO settings, seeds, and results schema.
2. Audit whether the completed Chairs and Globe 24-view manifests match the agreed PCA-angle baseline. Rerun only if they do not.
3. Implement the per-test-view distance evaluation and shared tables.
4. Prepare the Chairs and Globe candidate pools so test images cannot leak into selection.

### Both

1. Complete the regular-camera versus fisheye literature table.
2. Agree on the exact 24-view manifests before running any new GPU jobs.
3. Run one selector per scene at a time and save manifests, logs, metrics, renders, and seeds.
4. Repeat the strongest observed contrast with a second seed before making a final claim.

## 10. Scope boundary: sparse COLMAP

Sparse COLMAP asks a different question: can the same small image set estimate sufficiently good intrinsics, poses, and sparse points before GS training? It must not be mixed into the selection study.

After the shared-geometry selection result is established, sparse COLMAP can become a separate extension using the strongest selector. We need a dedicated literature review before committing to this branch, including sparse-SfM and pose-free GS methods.

## 11. Next-meeting statement

> We will compare three fixed, pre-training image-selection strategies under one coordinated native-fisheye DirectFisheye-GS protocol. The PCA-angle and 3D angular-FPS methods test pose-only diversity. The static visibility-and-direction selector tests whether COLMAP scene observations provide a better way to spend the same image budget. We will evaluate matched held-out views overall and as a function of distance from the selected cameras, then compare the gain over baseline with the assumptions and camera models used in regular-camera view-selection papers.
