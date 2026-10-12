#!/usr/bin/env bash
set -euo pipefail

TRDP_ROOT="${TRDP_ROOT:-/net/travail/sacosta/trdp-fisheyeGS}"
ENV_DIR="${DFGS_ENV:-$TRDP_ROOT/env/dfgs}"
DATA_DIR="$TRDP_ROOT/data/raw"
META_DIR="$TRDP_ROOT/metadata/dataset"
DATASET_URL="https://drive.google.com/file/d/1VhnpMUIKEak4TBpKY4H8vMJJe--FM2k5/view"
ARCHIVE="$DATA_DIR/FisheyeNeRF.zip"

mkdir -p "$DATA_DIR" "$META_DIR"
"$ENV_DIR/bin/python" -m pip install gdown
"$ENV_DIR/bin/gdown" --fuzzy "$DATASET_URL" -O "$ARCHIVE" 2>&1 | tee "$META_DIR/download.log"
sha256sum "$ARCHIVE" | tee "$META_DIR/FisheyeNeRF.zip.sha256"
unzip -t "$ARCHIVE" | tee "$META_DIR/FisheyeNeRF.zip.test.log"
