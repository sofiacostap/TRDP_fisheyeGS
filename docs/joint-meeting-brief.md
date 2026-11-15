# DirectFisheye-GS joint meeting brief

## The shared project question

> Given a fixed sparse training budget and a shared full-scene COLMAP reconstruction, can geometry-aware photo selection based on COLMAP visibility and viewing direction improve DirectFisheye-GS reconstruction compared with simple pose-based or uniform sampling?

This is a sparse-training-image study. It does not yet claim that the complete reconstruction can be created from a sparse capture alone. Every current condition uses a shared full-scene COLMAP model so that the selected image subset is the variable under test.

## Why the Chairs and Globe runs matter

The completed Chairs and Globe experiments establish the evaluation envelope for a selector:

- Full-view references verify the DirectFisheye-GS environment and held-out evaluation.
- Uniform 12, 24, 48, and 96-view runs calibrate the sparse regime.
- Fixed-count 24-view 360, 180, and 90 degree runs show that count alone is insufficient: image distribution affects held-out quality.
- Every completed run holds the native fisheye data, frozen COLMAP conversion, test split, CVO reciprocal preset, batch size 2, 30,000 iterations, and metrics fixed.

The completed runs therefore provide the matched reference conditions required to decide whether a new image-selection policy helps.

## What the Flowers work contributes

The Flowers work evaluates static image selection before DirectFisheye-GS training:

- Scene: Flowers from FisheyeNeRF, 149 images total.
- Reference protocol: 130 training candidates and 19 fixed test images.
- Budgets: 10 and 20 selected training images.
- Pose-only baselines: XY angle spacing and 3D angular farthest-point sampling (FPS).
- Proposed static selector: use full COLMAP point observations and point-to-camera viewing directions to choose images that contribute unseen scene points or useful additional views of known points.

This selector is separate from CVO. The static selector chooses the entire training subset once. CVO operates during training and pairs related images within the already-selected subset.

The Flowers report finds that its visibility-and-direction selector modestly outperforms angle-only selection at the same count. This is encouraging but preliminary because the current results have one run per condition and one scene.

## The combined story

Sofia's work defines suitable budgets and reveals that coverage matters. The Flowers work proposes a geometry-aware way of selecting better images at a fixed budget. Together, the next question is whether the Flowers selector generalises to Chairs and Globe.

This is not a duplication of work:

| Workstream | Role |
|---|---|
| Flowers | Develop and test the visibility-and-direction selector on one scene. |
| Chairs and Globe | Validate the reconstruction pipeline, quantify the sparse regime, and test the selector on two additional scenes with matched existing references. |

## Terminology

| Term | Meaning |
|---|---|
| XY angle spacing | Select camera centres approximately evenly spaced by azimuth around a reference point, using X and Y only. |
| 3D angular FPS | Greedily select camera-centre directions that are maximally separated in 3D. |
| Static visibility-and-direction selector | Select the whole subset before training using COLMAP scene-point observations and viewing directions. This was called `coverage selection` in the Flowers report. |
| Camera-path coverage | The extent of selected camera positions around the path, such as 360, 180, or 90 degrees. This is different from the static selector. |
| CVO | DirectFisheye-GS's in-training selection of related image pairs from the selected training set. |

## Recommended next experiments

1. Freeze and share the exact Flowers selector code, tie-breaking rule, and manifest format.
2. Verify the implementation reproduces the Flowers image lists and reported result table.
3. Generate a 24-view static visibility-and-direction manifest for Chairs and Globe, excluding all test images from candidate and observation lists.
4. Train the two 24-view selector conditions with the same configuration as the completed uniform 24-view references.
5. If the 24-view result is consistent, repeat at 12 views for Chairs and Globe.
6. Repeat the strongest comparison with a second seed. Report mean and variation, not only one result.
7. Optionally reproduce the 3D angular FPS baseline at 24 views on Chairs and Globe for a direct cross-scene comparison with Flowers.
8. Treat sparse-only COLMAP as a later, separate end-to-end realism extension.

## What to say in the meeting

> We first validated DirectFisheye-GS and mapped the sparse-view regime on Chairs and Globe. Those runs show that image count and camera-path distribution both affect held-out quality, so image count alone is not enough to define a sparse capture. In parallel, the Flowers work provides a static selection rule based on COLMAP visibility and viewing directions. Our next joint experiment tests whether that selector improves over uniform sampling at the same 12- and 24-view budgets on Chairs and Globe.

## Questions for supervisors

1. Is the shared-geometry image-selection question the right main scope for the project?
2. Should 24 views be the primary cross-scene comparison and 12 views the harder follow-up?
3. Is a 3D angular-FPS baseline needed on Chairs and Globe, or is uniform sampling sufficient as the main comparator?
4. Should the group add sparse-only COLMAP only after validating selection across scenes?
