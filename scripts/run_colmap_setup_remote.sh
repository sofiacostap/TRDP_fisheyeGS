#!/usr/bin/env bash
# Launch this script in tmux on a CREMI compute host.
set -euo pipefail

ROOT=/net/travail/sacosta/trdp-fisheyeGS
mkdir -p "$ROOT/metadata/conversion"
exec "$ROOT/metadata/setup/setup_colmap.sh" \
  >"$ROOT/metadata/conversion/colmap-install.log" 2>&1
