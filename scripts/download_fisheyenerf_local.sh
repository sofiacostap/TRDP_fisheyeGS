#!/usr/bin/env bash
set -euo pipefail

LOCAL_ROOT="${TRDP_LOCAL_ROOT:-/local/sacosta/trdp-fisheyeGS}"
ENV_DIR="${DFGS_ENV:-/net/travail/sacosta/trdp-fisheyeGS/env/dfgs}"
ARCHIVE="$LOCAL_ROOT/incoming/FisheyeNeRF.zip"
META_DIR="/net/travail/sacosta/trdp-fisheyeGS/metadata/dataset"
DATASET_URL="https://drive.google.com/file/d/1VhnpMUIKEak4TBpKY4H8vMJJe--FM2k5/view"

mkdir -p "$LOCAL_ROOT/incoming" "$LOCAL_ROOT/scenes" "$META_DIR"
"$ENV_DIR/bin/python" -m pip install gdown
"$ENV_DIR/bin/gdown" --fuzzy "$DATASET_URL" -O "$ARCHIVE" 2>&1 | tee "$META_DIR/download-local.log"
sha256sum "$ARCHIVE" | tee "$META_DIR/FisheyeNeRF.zip.sha256"
unzip -t "$ARCHIVE" | tee "$META_DIR/FisheyeNeRF.zip.test.log"
unzip -Z1 "$ARCHIVE" > "$META_DIR/FisheyeNeRF.zip.contents.txt"
