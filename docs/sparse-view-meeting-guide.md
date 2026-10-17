# Meeting guide: completed sparse-view count study

## Start with this summary

> I completed the controlled view-count study for DirectFisheye-GS on the FisheyeNeRF Chairs and Globe scenes. I kept the reconstructed cameras, test images, CVO configuration, resolution behaviour, and training budget fixed, then trained from 12, 24, 48, and 96 uniformly distributed views. The next question is not only how many views we have, but whether their angular coverage changes reconstruction quality at the same count.

## What was run

- **Scenes:** Chairs and Globe.
- **Conditions:** 12, 24, 48, and 96 selected training views per scene; eight sparse runs total.
- **Reference:** existing full-view baselines using all non-test images.
- **Method:** DirectFisheye-GS native-fisheye mode, `--eval --bs 2 --cvo_preset recip --iterations 30000 --disable_viewer`.
- **Training subsets:** static, uniformly distributed camera-centre azimuth selections; see `manifests/sparse/`.
- **Evaluation:** the same frozen held-out test images for every condition within a scene — 28 for Chairs and 27 for Globe.

## What to show

1. The aggregate results table in `results/sparse-view-count-summary.md`.
2. One matched held-out render comparison per scene: ground truth, 12, 24, 48, 96, and full reference.
3. The error-map slide as a spatial diagnostic: blue means low pixel difference; yellow/red means higher difference.

Explain that the heatmaps show one test view, whereas PSNR/SSIM/LPIPS are averages over the full test split. An individual image can depart from the aggregate ranking.

## Main observations to say aloud

- More uniformly distributed training views improve the aggregate held-out metrics in both scenes.
- Twelve views still gives a coherent, recognisable reconstruction. The loss is concentrated in fine structure, sharp edges, texture, highlights, and background detail rather than a collapse of the whole scene.
- Ninety-six views comes substantially closer to, but does not equal, the full-view baseline.
- A view-count curve by itself is expected. Its purpose is calibration: it identifies a meaningful intermediate count for the more informative coverage experiment.

## Why use 24 views for the coverage study?

At 12 views the setup is extremely sparse; at 96 views it is already fairly close to the full-view reference. Twenty-four views is a practical middle regime: reconstructions remain recognisable, but there is still a clear quantitative gap and therefore room to observe whether view placement/coverage matters. It is a design choice, not a universal optimum; supervisors may prefer 48 after reviewing the results.

## Decisions to request from supervisors

1. **Count:** Is 24 the accepted fixed budget for the angular-coverage arm, or should it be 48?
2. **Coverage conditions:** Is 360° uniform versus 180° and 90° contiguous coverage an appropriate minimal comparison?
3. **Sector convention:** Should a contiguous sector be defined from the PCA-azimuth convention already used for the uniform manifests, and should we test more than one sector location/seed?
4. **CVO ablation:** Should we add CVO-on versus CVO-off at one fixed 24-view coverage condition to isolate the method's main contribution?
5. **Reporting:** Should we report per-view distributions and within/outside-sector test performance in addition to PSNR, SSIM, LPIPS, renders, and error maps?

## Do not overclaim

- Do not say that the selected heatmap view proves a condition is globally best or worst.
- Do not call a 19 dB PSNR universally good or bad; it is meaningful relative to this scene and protocol.
- Do not say that 96 views matches the full baseline.
- Do not change the frozen test split, rerun COLMAP, or regenerate earlier manifests while running coverage conditions.
