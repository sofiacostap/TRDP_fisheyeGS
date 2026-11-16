# Partner handoff: coordinated sparse-view selection study

## Purpose

This repository is the source of truth for the next experiment phase.  The
question is: **with a fixed number of native-fisheye training images, can a
static scene-aware selector improve held-out DirectFisheye-GS quality over
pose-only image selection?**

Do not rerun the completed full-view or preliminary uniform-count study.  They
are retained as pilot evidence.  The following is a new, coordinated study.

## Read first

1. [`selection-study-plan.md`](selection-study-plan.md): research question and
   interpretation boundaries.
2. This file: exact common protocol and handoff tasks.
3. `scripts/create_xy_angle_manifest.py`: executable canonical XY baseline.
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
Compare methods *within a scene*, as a change from that scene's XY baseline;
do not compare raw PSNR between scenes.

## Methods

| Selector | Status | Required deliverable |
|---|---|---|
| `xy_angle` | Canonical implementation supplied here. | Generate manifests for every scene at 24, then 12. |
| `angular_fps` | Partner implementation required. | Commit one deterministic generator plus manifests. |
| `visibility_direction` | Partner implementation required. | Commit one deterministic generator plus manifests and scoring description. |

The supplied `xy_angle` rule is: take the coordinate-wise median of all
points in the frozen full-COLMAP `points3D.bin`; compute each eligible camera's
XY azimuth around it; choose the unused camera nearest each equally spaced
azimuth-bin centre.  Image-name order resolves exact ties.

If the historical Flowers selector used a different search rule, preserve it
as `flowers_legacy_xy_10_20` in documentation only.  Do not mix it with this
coordinated study unless the same rule is applied to all three scenes.

## Partner tasks

1. Clone this repository and read the four files above.
2. Commit the exact deterministic `angular_fps` generator.  State the
   reference-point rule, initial camera(s), distance formula, and ties.
3. Commit the exact deterministic `visibility_direction` generator.  State
   point eligibility, observation filtering, score equation, weights, initial
   selection, and ties.
4. Do **not** launch GPU jobs until each manifest has been reviewed.
5. Generate 24-view manifests for Flowers, Chairs, Globe using the frozen base
   test lists.  Commit manifests before training.
6. Run the shared launcher once per selector/scene at 24 views.  Keep the
   output and log paths that the launcher creates on CREMI; commit only small
   metrics summaries, manifests, and code.
7. Repeat all selectors at 12 views after validating the 24-view results.
8. Repeat only the strongest resulting comparison with `--seed 1`.

## Shared training command

On a CREMI GPU host:

```bash
source /net/travail/sacosta/trdp-fisheyeGS/metadata/setup/jessica_activate.sh
bash /net/travail/sacosta/trdp-fisheyeGS/scripts/run_selection_study.sh chairs xy_angle 24 0
```

The launcher refuses to overwrite an existing output directory.  Copy or
prepare a scene input directory at
`/net/travail/sacosta/trdp-fisheyeGS/selection_inputs/<scene>` only after the
manifest is frozen.  It must expose the original images and the unchanged
full-scene COLMAP sparse model expected by `train_eval.py`.

## Results to record

For each run, record: Git commit, hostname/GPU, manifest path and hash,
full-COLMAP hashes, command, seed, runtime, global metrics, per-test-view
metrics, and output directory.  Save matched renders and error maps outside
Git.  Never add raw datasets, checkpoints, or dense render folders to Git.
