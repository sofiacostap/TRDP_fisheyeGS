# TRDP FisheyeGS

Reproducible experimental workspace for the DirectFisheye-GS sparse-view study on the FisheyeNeRF **Globe** and **Chairs** scenes.

## Current milestone

The strict full-view baselines and the first sparse-view count study are complete for Globe and Chairs. All runs use native fisheye images, CVO with the `recip` preset, 30,000 iterations, batch size 2, and the repository's default image handling. The sparse study holds the test set, camera conversion, resolution behaviour, CVO preset, and training budget fixed while varying the number of uniformly distributed training views: 12, 24, 48, and 96.

The experiment protocol is retained in `docs/DirectFisheyeGS_Experimental_Protocol.docx`.

## Project principles

- Keep the original fisheye images; do not undistort them for training.
- Convert each full scene once, then freeze its cameras, image ordering, point cloud, and image-name mapping.
- Use a permanent test split generated from the frozen converted ordering.
- Define every sparse subset through manifests. Never delete images or regenerate COLMAP for a subset.
- Record the repository commit, environment, command, seed, manifest, runtime, GPU memory, metrics, and output location for every run.

## Repository layout

```text
TRDP_fisheyeGS/
├── docs/                 # Protocol and project decisions
├── environments/         # Exported environment specifications and setup notes
├── manifests/            # Frozen test sets and explicit training subsets
├── scripts/              # Preparation, validation, launch, and evaluation helpers
├── configs/              # Committed experiment configurations
├── results/              # Small versioned summaries, tables, and figures
├── logs/                 # Small run logs only; large logs stay on CREMI storage
└── .gitignore            # Excludes datasets, models, renders, and local secrets
```

The following large or machine-local material is deliberately not committed: raw FisheyeNeRF data, converted image directories, checkpoints, dense renders, CUDA build artifacts, virtual environments, and credentials.

## CREMI storage plan

The canonical project storage is the shared, automatically backed-up CREMI workspace:

```text
/net/travail/sacosta/trdp-fisheyeGS/
```

Keep source data, converted reconstructions, environments, checkpoints, final renders, and metrics there. Use a host's `/local/sacosta/trdp-fisheyeGS/` only as temporary fast workspace for active preprocessing or training input. Local workspaces can disappear after reboot or cleanup.

## CREMI shared environment

The tested environment is stored in your shared, automatically backed-up CREMI work space, so it is not limited to Jessica:

```text
/net/travail/sacosta/trdp-fisheyeGS/
├── env/dfgs/       # Python 3.12.11, CUDA 12.6, PyTorch 2.8.0+cu126
├── repo/           # DirectFisheye-GS source, commit recorded in metadata
└── metadata/setup/ # activation helper, environment export, package list, compatibility patch
```

It works on any CREMI host with an NVIDIA GPU and a driver compatible with CUDA 12.6. On login, use:

```bash
source /net/travail/sacosta/trdp-fisheyeGS/metadata/setup/jessica_activate.sh
nvidia-smi
python -c 'import torch; print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))'
```

The two custom CUDA extensions are compiled for NVIDIA compute capabilities 7.5, 8.0, 8.6, and 8.9, with forward-compatible PTX. CPU-only machines cannot train the project.


## Baseline checklist

- [x] Freeze the DirectFisheye-GS source commit.
- [x] Build and export the Python/CUDA environment on Jessica.
- [x] Confirm a CUDA tensor test and repository import.
- [x] Prepare and validate the full Globe and Chairs conversions.
- [x] Train both 30,000-iteration full-view CVO baselines.
- [x] Render test views and save official PSNR, SSIM, and LPIPS-VGG metrics.

See `results/baseline-summary.md` for the completed-run settings, metrics, and shared-storage locations.

## Sparse-view count study

- [x] Freeze one permanent held-out test set for each scene.
- [x] Freeze exact, uniformly distributed 12/24/48/96-view training manifests.
- [x] Train and evaluate all eight scene-by-view-count conditions.
- [x] Export aggregate metrics and matched-view qualitative/error-map comparisons.
- [ ] Run the planned fixed-24-view angular-coverage comparison (360° uniform versus 180° and 90° contiguous coverage).

See `results/sparse-view-count-summary.md` for the completed results and `docs/sparse-view-meeting-guide.md` for discussion notes. The exact selected images are versioned in `manifests/sparse/`.

## Git workflow

Commit small, meaningful changes: source scripts, manifests, configurations, setup records, metrics, and documentation. Use a unique `run_id` for every training result and store the run’s Git commit in its metadata.

Typical working cycle:

```bash
git pull --rebase
git status
git add README.md manifests scripts configs environments docs results
git commit -m "Describe the change"
git push
```

Do not add raw data, runs, models, or rendered image directories to Git.

## Source

- DirectFisheye-GS: <https://github.com/Metaverse-AI-Lab-THU/DirectFisheye-GS>
- FisheyeNeRF / SCNeRF: <https://github.com/POSTECH-CVLab/SCNeRF>
