# DirectFisheye-GS baseline: meeting cheat sheet

## One-sentence summary

I reproduced the full-view DirectFisheye-GS baseline on the native-fisheye FisheyeNeRF **Chairs** and **Globe** scenes, producing held-out test renders and metrics before beginning any sparse-view experiments.

## Where the work ran

Everything was run from a command-line terminal over SSH on CREMI GPU hosts. There was no web service or graphical training interface.

- **Chairs training:** `jessica`, NVIDIA RTX 4000 Ada Generation, 20 GB VRAM.
- **Globe training:** `albans`, NVIDIA RTX 4000 Ada Generation, 20 GB VRAM.
- **Canonical storage:** `/net/travail/sacosta/trdp-fisheyeGS/`, the shared backed-up CREMI workspace.
- **Temporary high-speed workspace:** `/local/sacosta/trdp-fisheyeGS/` on the host. It was used for active inputs only; final outputs went to the shared workspace.

The jobs were submitted from the terminal through the host job queue, so an SSH-window disconnect did not end them. A host reboot can end a running process; this is why shared checkpoints were enabled.

## Environment prepared before the experiments

The DirectFisheye-GS source was frozen at commit `db9b3a25bff79a59f02ce90f5bd235cb59c03aaa` and installed once in the shared workspace.

- Python 3.12.11
- PyTorch 2.8.0 + CUDA 12.6
- CUDA Toolkit 12.6; GCC/G++ 12.4
- CUDA extensions compiled for compute capabilities 7.5, 8.0, 8.6, and 8.9 plus PTX
- GPU-compatible COLMAP 3.10-dev build in `/net/travail/sacosta/trdp-fisheyeGS/env/colmap/`

On any compatible CREMI GPU host, the environment is activated with:

```bash
source /net/travail/sacosta/trdp-fisheyeGS/metadata/setup/jessica_activate.sh
nvidia-smi
python -c 'import torch; print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))'
```

## Data and camera preparation

1. Download the FisheyeNeRF archive once and verify its checksum/archive contents.
2. Keep only the two selected scenes, `chairs` and `globe`; preserve their native fisheye RGB images, supplied intrinsics, and poses in shared storage.
3. Run the DirectFisheye-GS conversion utility with fisheye COLMAP:

```bash
python convert.py \
  -s /local/sacosta/trdp-fisheyeGS/preparation/<scene> \
  --fisheye \
  --colmap_executable /net/travail/sacosta/trdp-fisheyeGS/env/colmap/bin/colmap
```

COLMAP estimates fisheye camera intrinsics/poses and a sparse 3D point cloud. The selected training reconstruction contains every image: Globe registered 216/216 images; Chairs registered 219/219 images. For Chairs, COLMAP produced a tiny 3-image component and a valid 219-image component; the complete component was selected without changing COLMAP parameters.

## What the model receives and optimizes

- **Inputs:** calibrated fisheye cameras, fixed poses, native RGB training images, and the COLMAP sparse point cloud for initialization.
- **Optimization:** each iteration renders the current 3D Gaussians from sampled fixed cameras, compares that render with the corresponding real photograph, and updates Gaussian position, scale/orientation, opacity, and appearance.
- **Ground truth:** the real RGB photographs, not the COLMAP geometry.
- **Evaluation:** held-out RGB photographs. These test views are never used for optimization.

## Frozen baseline parameters

```text
--eval
--bs 2
--cvo_preset recip
--iterations 30000
--disable_viewer
--checkpoint_iterations 7000 14000 21000 28000 30000
```

Interpretation:

- `--eval`: makes a fixed train/test split and evaluates the held-out set.
- `--bs 2`: two training camera views per optimization iteration.
- `--cvo_preset recip`: repository cross-view-optimization reciprocal preset.
- `--iterations 30000`: the common training budget for both scenes.
- `--disable_viewer`: no interactive GUI; useful for robust remote jobs.
- `--checkpoint_iterations ...`: saves resume points to shared storage.

The original images are 4240x2384. No manual resizing setting was passed. DirectFisheye-GS therefore used its documented default working-resolution behaviour: automatic downscaling to approximately 1.6K image width. This default is shared by both runs.

## Exact training command pattern

```bash
cd /net/travail/sacosta/trdp-fisheyeGS/repo/DirectFisheye-GS
/net/travail/sacosta/trdp-fisheyeGS/env/dfgs/bin/python train_eval.py \
  -s /local/sacosta/trdp-fisheyeGS/baseline_inputs/<scene> \
  -m /net/travail/sacosta/trdp-fisheyeGS/results/baselines/<run_id> \
  --eval --bs 2 --cvo_preset recip --iterations 30000 --disable_viewer \
  --checkpoint_iterations 7000 14000 21000 28000 30000
```

The completed run IDs are `chairs_cvo_recip_30000_v1` and `globe_cvo_recip_30000_v3`.

Globe was interrupted by a CREMI host power cycle and resumed from its shared 7k checkpoint using `--start_checkpoint <path-to-chkpnt7000.pth>`. The data and training parameters did not change. PyTorch 2.8 needed the recorded trusted-checkpoint compatibility adjustment `torch.load(checkpoint, weights_only=False)` to read the self-created checkpoint.

## Final held-out test results

| Scene | Images | Train / test | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
| --- | ---: | ---: | ---: | ---: | ---: |
| Chairs | 219 | 191 / 28 | 25.6681 | 0.8834 | 0.2049 |
| Globe | 216 | 189 / 27 | 24.3214 | 0.8012 | 0.2483 |

Use the paired held-out images in `results/figures/`: left is the real ground-truth photo and right is the model render. These are more important to show than training-view renders because they demonstrate novel-view reconstruction.

## What to ask supervisors

1. Is this baseline configuration accepted as the frozen reference for sparse-view experiments?
2. Which training-view budgets should be tested (for example 5%, 10%, 25%, and 50%)?
3. Should sparse subsets be uniformly spread around the camera path, and should a deliberately clustered/limited-view condition be added?
4. Besides PSNR, SSIM, LPIPS, and paired test render comparisons, do they want another evaluation or ablation?

## Next experimental step

Create explicit sparse training subsets while keeping the converted camera geometry, the held-out test images, the test split, resolution behaviour, CVO preset, and training budget fixed. Do not delete images or rerun COLMAP per subset. The number and selection of training images should be the controlled experimental variable.
