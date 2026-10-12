#!/usr/bin/env bash
# Install COLMAP without altering the existing DirectFisheye-GS Conda install.
set -euo pipefail

ROOT=/net/travail/sacosta/trdp-fisheyeGS
RUNTIME_ROOT=/local/sacosta/trdp-fisheyeGS/colmap-runtime
BOOT="$RUNTIME_ROOT/miniforge"
CACHE="$RUNTIME_ROOT/pkgs"
INSTALLER="$RUNTIME_ROOT/Miniforge3-Linux-x86_64.sh"
COLMAP_ENV="$ROOT/env/colmap"

mkdir -p "$RUNTIME_ROOT" "$CACHE" "$ROOT/metadata/conversion"

if [ ! -x "$BOOT/bin/conda" ]; then
  curl -fL --retry 3 \
    https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh \
    -o "$INSTALLER"
  bash "$INSTALLER" -b -p "$BOOT"
fi

# A previous incomplete attempt may have created this project-owned environment.
if [ -d "$COLMAP_ENV" ] && [ ! -x "$COLMAP_ENV/bin/colmap" ]; then
  rm -rf -- "$COLMAP_ENV"
fi

if [ ! -x "$COLMAP_ENV/bin/colmap" ]; then
  CONDA_PKGS_DIRS="$CACHE" "$BOOT/bin/conda" create -y -p "$COLMAP_ENV" \
    -c conda-forge --override-channels colmap
fi

"$COLMAP_ENV/bin/colmap" -h | head -3
