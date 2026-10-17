# Sparse-view count study: completed results

## Question and controlled comparison

How does held-out novel-view quality change when the same DirectFisheye-GS method receives fewer, uniformly distributed training views?

The only intended variable is the number of training images. The following remain fixed within each scene: frozen COLMAP reconstruction, permanent held-out test split, native fisheye images, default working-resolution behaviour, `--eval`, CVO `recip`, batch size 2, 30,000 iterations, and evaluation procedure.

The selected images are explicit, versioned manifests in `manifests/sparse/`. They are chosen by uniform camera-centre azimuth after projection onto the first two PCA axes of the frozen COLMAP camera centres.

## Aggregate held-out test results

Higher PSNR and SSIM are better. Lower LPIPS is better. `Full baseline` uses all non-test images and is a reference, not a sparse condition.

| Scene | Training views | PSNR ↑ | SSIM ↑ | LPIPS ↓ |
| --- | ---: | ---: | ---: | ---: |
| Chairs | 12 | 19.5072 | 0.7298 | 0.3174 |
| Chairs | 24 | 20.0334 | 0.7649 | 0.2823 |
| Chairs | 48 | 22.4447 | 0.8276 | 0.2328 |
| Chairs | 96 | 24.6223 | 0.8688 | 0.2110 |
| Chairs | Full baseline | 25.6681 | 0.8834 | 0.2049 |
| Globe | 12 | 18.2582 | 0.5825 | 0.3982 |
| Globe | 24 | 20.1751 | 0.6672 | 0.3276 |
| Globe | 48 | 22.1003 | 0.7440 | 0.2768 |
| Globe | 96 | 23.3265 | 0.7774 | 0.2614 |
| Globe | Full baseline | 24.3214 | 0.8012 | 0.2483 |

## Interpretation

The aggregate results improve as more uniformly distributed training views are available. This is a calibration result, not the main claim of the project: it establishes a usable scale of view scarcity before testing where the available views are located.

Twelve views are not a failure case. The matched-view reconstructions remain coherent and recognisable, while fine texture, sharp boundaries, and some illumination/background detail are less accurate. PSNR near 19 dB should therefore be interpreted relative to this fixed scene and protocol, not as a universal quality threshold.

At 96 views, the PSNR gain from 12 views is about 83% of the 12-to-full-baseline gap for both scenes. The full-view reference remains better, so this is not equivalence.

## Qualitative and spatial-error inspection

For matched held-out views, compare each rendering with the corresponding real RGB test image. Pixelwise maps use mean absolute RGB difference and a common robust colour scale within a scene:

- dark blue: lower pixel difference;
- yellow/red: higher pixel difference.

They identify *where* error occurs, but one test view is not a replacement for aggregate evaluation. For example, one selected Globe test frame has more local error in the 48-view output than in the 24-view output even though the 48-view condition is better on average across the full 27-image test set. Per-view quality need not follow the aggregate ranking exactly.

The local presentation-only visual assets are intentionally not committed because they are generated image outputs. They can be regenerated from the saved test renders and ground truth in the shared CREMI results directories.

## Next experiment: angular coverage

Use the completed 24-view uniform-coverage condition as the reference. Hold the count at 24 and compare:

1. 360° uniform coverage — complete reference;
2. 180° contiguous coverage — to run for Chairs and Globe;
3. 90° contiguous coverage — to run for Chairs and Globe.

Before launching, freeze the exact sector convention and selection manifests. Report aggregate metrics on the same fixed test split, plus matched-view render/error maps. A useful extension is to separately report test views inside and outside the observed angular sector.
