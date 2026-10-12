#!/usr/bin/env bash
set -euo pipefail

ROOT=/net/travail/sacosta/trdp-fisheyeGS
mkdir -p "$ROOT/metadata/conversion"
exec "$ROOT/metadata/setup/setup_colmap_isolated.sh" \
  >"$ROOT/metadata/conversion/colmap-install.log" 2>&1
