#!/usr/bin/env bash
set -euo pipefail

TRDP_ROOT="${TRDP_ROOT:-/net/travail/sacosta/trdp-fisheyeGS}"
CONDA="$TRDP_ROOT/env/miniforge3/bin/conda"
COLMAP_ENV="$TRDP_ROOT/env/colmap"

# Keep solver/download cache off the backed-up project space and avoid relying
# on a previously interrupted cache entry. This cache is disposable.
export CONDA_PKGS_DIRS="${TRDP_COLMAP_PKGS:-/local/sacosta/trdp-fisheyeGS/conda-pkgs}"
mkdir -p "$CONDA_PKGS_DIRS"

if [ ! -x "$COLMAP_ENV/bin/colmap" ]; then
  "$CONDA" create -y -p "$COLMAP_ENV" -c conda-forge colmap
fi

"$COLMAP_ENV/bin/colmap" -h | head -3
