#!/usr/bin/env bash
# Usage: convert_fisheye_scene.sh globe|chairs
# Run on a CREMI CUDA host. Keeps native images and DirectFisheye-GS defaults.
set -euo pipefail

scene="${1:?Usage: $0 globe|chairs}"
case "$scene" in globe|chairs) ;; *) echo "Unknown scene: $scene" >&2; exit 2;; esac

ROOT=/net/travail/sacosta/trdp-fisheyeGS
WORK=/local/sacosta/trdp-fisheyeGS/preparation/"$scene"
PYTHON="$ROOT/env/dfgs/bin/python"
CONVERT="$ROOT/repo/DirectFisheye-GS/convert.py"
COLMAP="$ROOT/env/colmap/bin/colmap"

test -x "$PYTHON"
test -f "$CONVERT"
test -x "$COLMAP"
test -d "$WORK/input"

# Never overwrite a reconstruction without an explicit inspection/reset step.
if [ -e "$WORK/sparse" ] || [ -e "$WORK/distorted/database.db" ]; then
  echo "Refusing to overwrite existing conversion output in $WORK" >&2
  exit 3
fi

"$PYTHON" "$CONVERT" -s "$WORK" --fisheye --colmap_executable "$COLMAP"
