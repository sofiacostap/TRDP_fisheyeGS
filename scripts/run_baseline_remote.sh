#!/usr/bin/env bash
# Usage: run_baseline_remote.sh <scene> <run_name>
#
# The scene input is read from the host-local fast workspace.  Results, logs,
# and resumable checkpoints are written to the shared project workspace so a
# host reboot or a later move to another CREMI machine does not lose progress.
set -euo pipefail

scene="${1:?scene required}"
run_name="${2:?run name required}"
ROOT=/net/travail/sacosta/trdp-fisheyeGS
WORK=/local/sacosta/trdp-fisheyeGS/baseline_inputs/"$scene"
RUN="$ROOT/results/baselines/$run_name"
LOG_ROOT="$ROOT/metadata/training_logs"

mkdir -p "$LOG_ROOT" "$ROOT/results/baselines"
test -d "$WORK"
test ! -e "$RUN"

cd "$ROOT/repo/DirectFisheye-GS"
exec "$ROOT/env/dfgs/bin/python" train_eval.py \
  -s "$WORK" -m "$RUN" --eval --bs 2 --cvo_preset recip \
  --iterations 30000 --disable_viewer \
  --checkpoint_iterations 7000 14000 21000 28000 30000 \
  >"$LOG_ROOT/$run_name.log" 2>&1
