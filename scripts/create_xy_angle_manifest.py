#!/usr/bin/env python3
"""Create a deterministic XY-azimuth sparse-view manifest.

This is the coordinated *canonical* XY-angle baseline for the selection study.
It uses the coordinate-wise median of the frozen full-COLMAP 3D points as its
reference point, then selects the unused eligible camera nearest each equally
spaced XY azimuth-bin centre.  It intentionally does not depend on a GPU or
on the DirectFisheye-GS source tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import struct
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


def read_next(stream, size: int, pattern: str):
    return struct.unpack("<" + pattern, stream.read(size))


def qvec_to_rotation(qvec: np.ndarray) -> np.ndarray:
    q0, q1, q2, q3 = qvec
    return np.array([
        [1 - 2 * (q2 * q2 + q3 * q3), 2 * (q1 * q2 - q0 * q3), 2 * (q1 * q3 + q0 * q2)],
        [2 * (q1 * q2 + q0 * q3), 1 - 2 * (q1 * q1 + q3 * q3), 2 * (q2 * q3 - q0 * q1)],
        [2 * (q1 * q3 - q0 * q2), 2 * (q2 * q3 + q0 * q1), 1 - 2 * (q1 * q1 + q2 * q2)],
    ])


def read_camera_centres(images_bin: Path) -> dict[str, np.ndarray]:
    centres: dict[str, np.ndarray] = {}
    with images_bin.open("rb") as stream:
        for _ in range(read_next(stream, 8, "Q")[0]):
            data = read_next(stream, 64, "idddddddi")
            qvec = np.asarray(data[1:5], dtype=np.float64)
            tvec = np.asarray(data[5:8], dtype=np.float64)
            name = bytearray()
            while (char := stream.read(1)) != b"\x00":
                name.extend(char)
            track_len = read_next(stream, 8, "Q")[0]
            stream.seek(24 * track_len, 1)
            centres[name.decode("utf-8")] = -qvec_to_rotation(qvec).T @ tvec
    return centres


def read_point_xyz(points3d_bin: Path) -> np.ndarray:
    points: list[tuple[float, float, float]] = []
    with points3d_bin.open("rb") as stream:
        for _ in range(read_next(stream, 8, "Q")[0]):
            record = read_next(stream, 43, "QdddBBBd")
            points.append(record[1:4])
            track_len = read_next(stream, 8, "Q")[0]
            stream.seek(8 * track_len, 1)  # image_id (int32), point2D_idx (int32)
    if not points:
        raise ValueError(f"No 3D points in {points3d_bin}")
    return np.asarray(points, dtype=np.float64)


def circular_distance(left: float, right: float) -> float:
    return abs((left - right + math.pi) % (2 * math.pi) - math.pi)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline-manifest", required=True, type=Path)
    parser.add_argument("--images-bin", required=True, type=Path)
    parser.add_argument("--points3d-bin", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--count", required=True, type=int)
    args = parser.parse_args()

    base = json.loads(args.baseline_manifest.read_text(encoding="utf-8"))
    eligible = sorted(base["train_images"])
    if not 1 < args.count <= len(eligible):
        raise ValueError("count must be between 2 and the number of eligible training images")

    centres = read_camera_centres(args.images_bin)
    missing = sorted(set(eligible) - set(centres))
    if missing:
        raise ValueError(f"Eligible images missing from COLMAP poses: {missing[:5]}")

    all_points = read_point_xyz(args.points3d_bin)
    reference = np.median(all_points, axis=0)
    angles = np.asarray([
        math.atan2(centres[name][1] - reference[1], centres[name][0] - reference[0])
        for name in eligible
    ])
    targets = [-math.pi + (index + 0.5) * 2 * math.pi / args.count for index in range(args.count)]
    selected_indices: list[int] = []
    for target in targets:
        choices = sorted(
            (circular_distance(angle, target), eligible[index], index)
            for index, angle in enumerate(angles)
            if index not in selected_indices
        )
        selected_indices.append(choices[0][2])

    selected = [eligible[index] for index in selected_indices]
    payload = {
        "manifest_version": 1,
        "scene": base["scene"],
        "purpose": "coordinated sparse-view selection study: canonical XY-angle baseline",
        "base_manifest": str(args.baseline_manifest),
        "base_manifest_sha256": sha256(args.baseline_manifest),
        "reconstruction": base["reconstruction"],
        "selection": {
            "strategy": "xy_azimuth_bin_v1",
            "training_view_count": args.count,
            "eligible_training_view_count": len(eligible),
            "reference_point_rule": "coordinate-wise median of every XYZ point in frozen full-COLMAP points3D.bin",
            "reference_point_xyz": reference.tolist(),
            "full_colmap_point_count": int(len(all_points)),
            "angle_rule": "atan2(camera_center_y-reference_y, camera_center_x-reference_x), in [-pi, pi)",
            "selection_rule": "one unused eligible image nearest each equally spaced azimuth-bin centre",
            "tie_breaking": "ascending image filename",
            "target_azimuth_degrees": [round(math.degrees(target), 6) for target in targets],
            "images_bin_sha256": sha256(args.images_bin),
            "points3d_bin_sha256": sha256(args.points3d_bin),
        },
        "eligible_train_images": eligible,
        "train_images": selected,
        "test_images": base["test_images"],
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.output}: {len(selected)} train / {len(payload['test_images'])} frozen test")
    for target, index in zip(targets, selected_indices):
        print(f"{math.degrees(target):8.3f}  {eligible[index]}")


if __name__ == "__main__":
    main()
