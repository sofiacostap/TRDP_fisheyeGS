#!/usr/bin/env bash
# Launch one reproducible uniform-pose sparse-view run on Xeonphi.
# Usage: bash launch_sparse_uniform_xeonphi.sh <chairs|globe> <view-count> <gpu-id>
set -euo pipefail

scene="$1"
count="$2"
gpu="$3"
root="/net/travail/sacosta/trdp-fisheyeGS"
run_id="${scene}_uniform_pose${count}_cvo_recip_seed0_v1"
input="/local/sacosta/trdp-fisheyeGS/sparse_inputs/${scene}_uniform${count}_v1"
manifest="${root}/manifests/sparse/${scene}_uniform_pose_${count}_v1.json"
output="${root}/results/sparse/${run_id}"
log="${root}/logs/sparse/${run_id}.log"

test -d "$input"
test -f "$manifest"
test ! -e "$output"
mkdir -p "$(dirname "$output")" "$(dirname "$log")"

CUDA_VISIBLE_DEVICES="$gpu" "${root}/env/dfgs/bin/python" \
  "${root}/repo/DirectFisheye-GS-sparse/train_eval.py" \
  -s "$input" \
  -m "$output" \
  --eval \
  --split_manifest "$manifest" \
  --bs 2 \
  --cvo_preset recip \
  --iterations 30000 \
  --disable_viewer \
  --checkpoint_iterations 30000 \
  > "$log" 2>&1
