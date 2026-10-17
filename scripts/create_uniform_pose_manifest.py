#!/usr/bin/env python3
"""Create a reproducible uniformly distributed sparse-view split manifest.

The input baseline manifest supplies the frozen test set and eligible training
images. Camera centres are projected onto their first two PCA axes; one eligible
training image nearest each evenly spaced azimuth target is selected.
"""

import argparse
import hashlib
import json
import math
import struct
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def read_next(fid, size, pattern):
    return struct.unpack("<" + pattern, fid.read(size))


def read_colmap_poses(images_bin: Path):
    poses = {}
    with images_bin.open("rb") as fid:
        for _ in range(read_next(fid, 8, "Q")[0]):
            data = read_next(fid, 64, "idddddddi")
            qvec = np.asarray(data[1:5], dtype=np.float64)
            tvec = np.asarray(data[5:8], dtype=np.float64)
            name_bytes = bytearray()
            while (char := fid.read(1)) != b"\x00":
                name_bytes.extend(char)
            name = name_bytes.decode("utf-8")
            count = read_next(fid, 8, "Q")[0]
            fid.seek(24 * count, 1)
            poses[name] = (qvec, tvec)
    return poses


def qvec_to_rotation(qvec):
    q0, q1, q2, q3 = qvec
    return np.array([
        [1 - 2 * (q2 * q2 + q3 * q3), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)],
        [2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1 * q1 + q3 * q3), 2 * (q2 * q3 - q0 * q1)],
        [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1 * q1 + q2 * q2)],
    ])


def circular_distance(left, right):
    return abs((left - right + math.pi) % (2 * math.pi) - math.pi)


def sha256(path: Path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-manifest", type=Path, required=True)
    parser.add_argument("--images-bin", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--count", type=int, required=True)
    args = parser.parse_args()

    baseline = json.loads(args.baseline_manifest.read_text(encoding="utf-8"))
    eligible = list(baseline["train_images"])
    if not 1 < args.count <= len(eligible):
        raise ValueError("count must be between 2 and the number of eligible training images")

    poses = read_colmap_poses(args.images_bin)
    missing = sorted(set(eligible) - set(poses))
    if missing:
        raise ValueError(f"Eligible images absent from COLMAP model: {missing[:5]}")

    centres = np.asarray([
        -qvec_to_rotation(poses[name][0]).T @ poses[name][1]
        for name in eligible
    ])
    centre = centres.mean(axis=0)
    _, _, right_axes = np.linalg.svd(centres - centre, full_matrices=False)
    axis_u, axis_v = right_axes[:2]
    planar = centres - centre
    angles = np.arctan2(planar @ axis_v, planar @ axis_u)

    selected_indices = []
    targets = [-math.pi + (index + 0.5) * 2 * math.pi / args.count for index in range(args.count)]
    for target in targets:
        candidates = sorted(
            (circular_distance(angle, target), image_index)
            for image_index, angle in enumerate(angles)
            if image_index not in selected_indices
        )
        selected_indices.append(candidates[0][1])

    selected = [eligible[index] for index in selected_indices]
    manifest = {
        "manifest_version": 1,
        "scene": baseline["scene"],
        "purpose": "static sparse-view pilot with frozen baseline test split",
        "base_manifest": str(args.baseline_manifest),
        "base_manifest_sha256": sha256(args.baseline_manifest),
        "reconstruction": baseline["reconstruction"],
        "selection": {
            "strategy": "uniform_camera_center_azimuth",
            "training_view_count": args.count,
            "eligible_training_view_count": len(eligible),
            "angle_convention": "camera centres projected to the first two PCA axes about their mean; select the nearest unused eligible image to each equally spaced azimuth-bin centre",
            "pca_axis_u": axis_u.tolist(),
            "pca_axis_v": axis_v.tolist(),
            "camera_center_mean": centre.tolist(),
            "target_azimuth_degrees": [round(math.degrees(target), 6) for target in targets],
        },
        "train_images": selected,
        "test_images": baseline["test_images"],
        "excluded_eligible_train_images": sorted(set(eligible) - set(selected)),
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}: {len(selected)} train / {len(manifest['test_images'])} test images")
    for target, index in zip(targets, selected_indices):
        print(f"{math.degrees(target):8.3f}°  {eligible[index]}")


if __name__ == "__main__":
    main()
