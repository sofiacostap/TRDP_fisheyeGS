# TRDP FisheyeGS

Reproducible experimental workspace for the DirectFisheye-GS sparse-view study on the FisheyeNeRF **Globe** and **Chairs** scenes.

## Current milestone

The immediate objective is to reproduce the full-view DirectFisheye-GS baseline for Globe and Chairs with native fisheye images and cross-view optimization (CVO). Sparse-view experiments begin only after the baseline, camera conversion, permanent test split, and common image resolution are frozen.

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

Jessica currently reports about 1.4 TB free on its local NVMe filesystem and about 6.6 GB free in the user account. Large materials must therefore live outside the account home directory, in a CREMI-approved persistent location.

Before downloading data or training, confirm with CREMI:

1. the approved directory for project data and its persistence across reboot/cleanup;
2. whether it is permitted to store environments, raw data, checkpoints, and renders there;
3. GPU-use, unattended-run, and `tmux` policies.

After approval, record the chosen absolute path in `docs/storage-and-hosts.md` (not yet created because the policy is unresolved).

## Baseline checklist

- [ ] Freeze the DirectFisheye-GS source commit.
- [ ] Build and export the Python/CUDA environment on Jessica.
- [ ] Confirm a CUDA tensor test and repository import.
- [ ] Run 100 iterations at batch sizes 1 and 2; record peak VRAM.
- [ ] Freeze one common image resolution.
- [ ] Prepare and validate the full Globe and Chairs conversions.
- [ ] Save permanent train/test manifests.
- [ ] Train both 30,000-iteration full-view CVO baselines.
- [ ] Render test views and save official PSNR, SSIM, and LPIPS-VGG metrics.

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
