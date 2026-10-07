#!/usr/bin/env bash
# Load the tested DirectFisheye-GS environment on CREMI host Jessica.

export TRDP_ROOT=/net/travail/sacosta/trdp-fisheyeGS
export DFGS_ENV="$TRDP_ROOT/env/dfgs"
export CUDA_HOME="$DFGS_ENV"
export PATH="$DFGS_ENV/bin:$PATH"
export CC="$DFGS_ENV/bin/x86_64-conda-linux-gnu-gcc"
export CXX="$DFGS_ENV/bin/x86_64-conda-linux-gnu-g++"
export TORCH_CUDA_ARCH_LIST=8.9
export PYTHONNOUSERSITE=1

if [ ! -x "$DFGS_ENV/bin/python" ]; then
  echo "DirectFisheye-GS environment not found at $DFGS_ENV" >&2
  return 1 2>/dev/null || exit 1
fi

echo "DirectFisheye-GS environment active: $DFGS_ENV"
