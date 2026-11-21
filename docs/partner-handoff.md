# Partner handoff: coordinated sparse-view selection study

## Purpose

This repository is the source of truth for the next experiment phase.  The
question is: **with a fixed number of native-fisheye training images, can a
static scene-aware selector improve held-out DirectFisheye-GS quality over
pose-only image selection?**

On CREMI, keep the small Git control checkout separate from the large shared
data-and-results workspace:

```text
/net/cremi/sacosta/TRDP_fisheyeGS-control/  # Git checkout: scripts, manifests, docs
/net/travail/sacosta/trdp-fisheyeGS/        # data, environment, logs, results
```

The coordinated launch and validation scripts are **Linux-only**: they use
Linux process locking and are intended to run on CREMI GPU hosts. This does not
limit the study, because all training is performed on CREMI; Windows is only a
local editing and SSH client.

Do not rerun the completed full-view or preliminary uniform-count study.  They
are retained as pilot evidence.  The following is a new, coordinated study.

## Read first

1. [`selection-study-plan.md`](selection-study-plan.md): research question and
   interpretation boundaries.
2. This file: exact common protocol and handoff tasks.
3. `scripts/create_uniform_pose_manifest.py`: executable canonical PCA-angle baseline.
4. `scripts/run_selection_study.sh`: the only shared training launcher.

## Frozen common protocol

| Item | Required setting |
|---|---|
| Scenes | `flowers`, `chairs`, `globe` |
| Budgets | 24 views first; 12 views after validating 24 |
| Geometry | Frozen full-scene COLMAP model per scene |
| Candidate pool | All permanent-training images in the base manifest |
| Test data | Frozen base-manifest test list; excluded from selection and training |
| Input model | Native fisheye DirectFisheye-GS; no undistortion |
| CVO | `--bs 2 --cvo_preset recip` |
| Optimisation | `--iterations 30000 --seed 0` |
| Resolution | Repository automatic image handling; do not pass a resize option |
| Evaluation | Same frozen test list; global and per-test-view PSNR, SSIM, LPIPS |

Different scenes have different frozen test-image counts.  This is acceptable.
Compare methods *within a scene*, as a change from that scene's PCA-angle baseline;
do not compare raw PSNR between scenes.

## Methods

| Selector | Status | Required deliverable |
|---|---|---|
| `pca_angle` | Canonical pose-only reference implementation. | Frozen manifests generated for Flowers, Chairs, and Globe. |
| `angular_fps` | Deterministic 3D angular farthest-point sampler. | Frozen manifests generated for Flowers, Chairs, and Globe. |
| `coverage` | Static COLMAP visibility-and-direction selector. | Frozen manifests generated for Flowers, Chairs, and Globe. |

The supplied `pca_angle` rule is: calculate each eligible camera centre, fit
the first two PCA axes to the camera centres around their mean, and select the
unused image nearest each equally spaced azimuth-bin centre in that fitted
plane. Image-name order resolves exact ties. This is the same pose-only
baseline used by the November Flowers package and by the earlier Globe/Chairs
uniform-view study.

`scripts/create_xy_angle_manifest.py` is retained only as an archived,
superseded fixed-world-XY prototype. Do not use it for coordinated runs.

## Study state and next GPU step

All three selectors are now defined in the pinned Flowers reference package.
Flowers already has its completed reference table; it should not be rerun.
The shared Chairs and Globe manifests have passed the no-training audit:
their frozen geometry hashes match the original baseline, every test image is
excluded, and all budget prefixes are nested.

1. Do **not** regenerate a manifest or rerun COLMAP.
2. Run the shared launcher for each selector/scene at 24 views. Keep the
   output and log paths that the launcher creates on CREMI; commit only small
   metrics summaries, manifests, and code.
3. Repeat all selectors at 12 views after validating the 24-view results.
4. Repeat only the strongest resulting comparison with `--seed 1`.

## Shared training command

On a CREMI GPU host:

```bash
source /net/travail/sacosta/trdp-fisheyeGS/metadata/setup/jessica_activate.sh
bash /net/cremi/sacosta/TRDP_fisheyeGS-control/scripts/run_selection_study.sh chairs pca_angle 24 0 0
```

The final optional argument is the training seed and defaults to `0`. The
launcher refuses to overwrite an existing output directory. It reads the
original images and a non-duplicating link to the unchanged full-scene COLMAP
sparse model from `/net/travail/sacosta/trdp-fisheyeGS/data/selected/<scene>`.

## Results to record

For each run, record: Git commit, hostname/GPU, manifest path and hash,
full-COLMAP hashes, command, seed, runtime, global metrics, per-test-view
metrics, and output directory.  Save matched renders and error maps outside
Git.  Never add raw datasets, checkpoints, or dense render folders to Git.
