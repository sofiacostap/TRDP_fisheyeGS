# Flowers Reference Integration

## Purpose

The November 19 Flowers study is the reference implementation for the shared
native-fisheye selection experiment. Its code is pinned as the public Git
submodule `external/flowers-reference`. The submodule is source code,
manifests, lightweight metrics, and provenance only. It deliberately excludes
raw photographs, trained checkpoints, dense renders, and the private frozen
COLMAP archive.

## Pinned components

| Component | Location | Status |
|---|---|---|
| Flowers reference package | `external/flowers-reference` | Public source package pinned by Git submodule |
| Reference code on CREMI | `/net/cremi/sacosta/SPARSE_VIEW_FISHEYE_GS-control/November_19th_Flower_Scene_Experiment` | Shallow clone of the same package |
| Pinned selection engine | `/net/travail/sacosta/trdp-fisheyeGS/repo/DirectFisheye-GS-selection-study` | Separate checkout; 33 training-file hashes verified |
| Prepared Flowers scene | `/net/travail/sacosta/trdp-fisheyeGS/data/selected/flowers` | 149 original images plus frozen COLMAP model |
| Private geometry archive | `/net/travail/sacosta/trdp-fisheyeGS/private_inputs/flowers/flowers_frozen_colmap_v1.tar.gz` | SHA-256 verified; never commit |

The original baseline is **PCA-angle selection**: candidate camera centres are
projected into the first two PCA axes around their mean, then the nearest
unused image is selected for each equally spaced angular target. It is the
common pose-only baseline for Flowers, Chairs, and Globe.

## Verified Flowers preflight

The prepared scene passes the reference package's CPU-only preflight:

- 149 original Flowers images;
- 130 frozen training candidates and 19 frozen held-out tests;
- exact frozen cameras, image poses, sparse points, point-cloud cache, and
  camera-association file;
- all 12 PCA-angle, 3D-angular-FPS, and visibility-direction manifests;
- test images excluded from both training and scene-aware selection tracks.

No GPU optimisation was started by this validation.

## Clone and update

For a new local checkout:

```bash
git clone --recurse-submodules https://github.com/sofiacostap/TRDP_fisheyeGS.git
```

For an existing checkout:

```bash
git pull --ff-only
git submodule update --init --recursive
```

The reference package remains Shihab's repository. Changes to its code should
be committed there first; this repository then updates the submodule pin only
after the change has been reviewed. Project-wide protocol changes belong here.

## Next experiment gate

Before any new GPU job, install the exact CUDA extensions for the separate
selection-study engine and run the reference GPU loader preflight. The full
Flowers result table already exists; do not rerun Flowers merely to reproduce
it. New GPU work starts with the same selector implementation on Chairs and
Globe, after their manifests pass the same checks.
