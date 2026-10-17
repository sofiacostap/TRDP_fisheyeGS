# Full-view baseline summary

Both runs are strict DirectFisheye-GS full-view baselines on the FisheyeNeRF scenes. They use native fisheye images, `--eval`, `--bs 2`, `--cvo_preset recip`, `--iterations 30000`, and `--disable_viewer`. The repository automatically rescales the 4240x2384 inputs to its default 1.6K working resolution.

The raw data, model checkpoints, point clouds, and renders are intentionally not stored in Git. They are in the backed-up shared CREMI workspace under `/net/travail/sacosta/trdp-fisheyeGS/results/baselines/`.

| Scene | Run ID | Test images | PSNR | SSIM | LPIPS | Shared output |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| Chairs | `chairs_cvo_recip_30000_v1` | 28 | 25.6680902 | 0.8833746 | 0.2048995 | `/net/travail/sacosta/trdp-fisheyeGS/results/baselines/chairs_cvo_recip_30000_v1` |
| Globe | `globe_cvo_recip_30000_v3` | 27 | 24.3213761 | 0.8012230 | 0.2483028 | `/net/travail/sacosta/trdp-fisheyeGS/results/baselines/globe_cvo_recip_30000_v3` |

Each completed output contains:

- `results_test.json` and `results_train.json` for aggregate metrics;
- `per_view_test.json` and `per_view_train.json` for per-image metrics;
- `point_cloud/iteration_30000/point_cloud.ply` for the final reconstruction;
- `test/ours_30000/renders/` and `test/ours_30000/gt/` for held-out render/ground-truth pairs;
- aggregate and per-view metric JSON files.

To stay within CREMI storage quotas, restart checkpoints and intermediate point clouds are pruned after a run has completed and its final point cloud, renders, and metrics have been verified. This does not remove the reproducible run configuration, the frozen data split, or the final evaluation outputs.

The immutable full-view train/test filename lists and the SHA256 identities of the corresponding COLMAP reconstructions are versioned in `manifests/chairs_fullview_split_v1.json` and `manifests/globe_fullview_split_v1.json`.

## Interruption and resumption

Globe was interrupted by host power cycles. It resumed from the self-created 7k checkpoint and completed with unchanged experiment parameters. PyTorch 2.8 requires an explicit trusted-checkpoint compatibility setting when loading this project's checkpoint format: `torch.load(checkpoint, weights_only=False)`. This is a serialization compatibility change only; it does not alter the data, training configuration, or model method.
