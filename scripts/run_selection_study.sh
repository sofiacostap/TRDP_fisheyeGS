#!/usr/bin/env bash
# Run one frozen-manifest DirectFisheye-GS sparse-view experiment.
# Usage: bash run_selection_study.sh <scene> <selector> <12|24|48|96> <gpu-id> [seed]
# Example: bash run_selection_study.sh chairs pca_angle 24 0 0
set -euo pipefail

scene="$1"
selector="$2"
budget="$3"
gpu="$4"
seed="${5:-0}"
root="/net/travail/sacosta/trdp-fisheyeGS"
run_id="${scene}_${selector}_${budget}views_cvo_recip_seed${seed}_v1"
input="${root}/data/selected/${scene}"
manifest="${root}/manifests/selection-study/${scene}/${scene}_${selector}_${budget}_v1.json"
output="${root}/results/selection-study/${run_id}"
log="${root}/logs/selection-study/${run_id}.log"

case "$scene" in flowers|chairs|globe) ;; *) echo "Unknown scene: $scene" >&2; exit 2 ;; esac
case "$selector" in pca_angle|angular_fps|coverage) ;; *) echo "Unknown selector: $selector" >&2; exit 2 ;; esac
case "$budget" in 12|24|48|96) ;; *) echo "Budget must be 12, 24, 48, or 96" >&2; exit 2 ;; esac
case "$seed" in *[!0-9]*|'') echo "Seed must be a non-negative integer" >&2; exit 2 ;; esac

test -d "$input"
test -f "$manifest"
test ! -e "$output"
mkdir -p "$(dirname "$output")" "$(dirname "$log")"

CUDA_VISIBLE_DEVICES="$gpu" "${root}/env/dfgs/bin/python" \
  "${root}/repo/DirectFisheye-GS-selection-study/train_eval.py" \
  -s "$input" -m "$output" --eval --split_manifest "$manifest" \
  --bs 2 --cvo_preset recip --iterations 30000 --disable_viewer \
  --checkpoint_iterations 30000 --seed "$seed" > "$log" 2>&1
