#!/usr/bin/env python3
"""Export an immutable DirectFisheye-GS full-view split and COLMAP identity."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--scene", required=True, choices=("chairs", "globe"))
    parser.add_argument("--reconstruction", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--method-commit", required=True)
    args = parser.parse_args()

    reconstruction = args.reconstruction.resolve()
    sys.path.insert(0, "/net/travail/sacosta/trdp-fisheyeGS/repo/DirectFisheye-GS")
    from scene.colmap_loader import read_extrinsics_binary  # noqa: PLC0415

    model_files = ["cameras.bin", "images.bin", "points3D.bin", "project.ini"]
    file_hashes = {}
    for name in model_files:
        path = reconstruction / name
        if not path.is_file():
            raise FileNotFoundError(path)
        file_hashes[name] = sha256(path)

    identity = "".join(f"{name}  {file_hashes[name]}\n" for name in model_files)
    reconstruction_sha256 = hashlib.sha256(identity.encode("utf-8")).hexdigest()

    extrinsics = read_extrinsics_binary(str(reconstruction / "images.bin"))
    ordered_images = sorted(extrinsic.name for extrinsic in extrinsics.values())
    test_images = [name for index, name in enumerate(ordered_images) if index % 8 == 0]
    train_images = [name for index, name in enumerate(ordered_images) if index % 8 != 0]

    payload = {
        "manifest_version": 1,
        "scene": args.scene,
        "purpose": "immutable full-view DirectFisheye-GS baseline split",
        "method_commit": args.method_commit,
        "reconstruction": {
            "path": str(reconstruction),
            "model_files_sha256": file_hashes,
            "canonical_model_sha256": reconstruction_sha256,
            "image_ordering": "lexicographic COLMAP image_name ordering",
        },
        "split": {
            "evaluation_enabled": True,
            "repository_rule": "sorted COLMAP image list; every eighth image with zero-based index is held out",
            "holdout_interval": 8,
            "total_images": len(ordered_images),
            "train_count": len(train_images),
            "test_count": len(test_images),
        },
        "ordered_images": ordered_images,
        "train_images": train_images,
        "test_images": test_images,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    print(f"{args.scene}: {len(ordered_images)} total, {len(train_images)} train, {len(test_images)} test")
    print(f"canonical_model_sha256={reconstruction_sha256}")


if __name__ == "__main__":
    main()
