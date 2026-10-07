# Jessica environment

This folder records the tested DirectFisheye-GS environment created on the CREMI host `jessica`. It is stored in the shared `/net/travail/sacosta` workspace and is intended for any CUDA-capable CREMI host whose NVIDIA driver supports CUDA 12.6.

It is a recipe and audit record, not a copy of the installed environment. The installed files remain in `/net/travail/sacosta/trdp-fisheyeGS/env/dfgs` on Jessica.

## Verified stack

- Python 3.12.11
- PyTorch 2.8.0+cu126 and torchvision 0.23.0+cu126
- CUDA Toolkit 12.6
- GCC/G++ 12.4
- NVIDIA RTX 4000 Ada Generation
- DirectFisheye-GS source commit recorded in `directfisheyegs-commit.txt`

`environment-jessica.yml` and `pip-freeze.txt` are the exact exported records. `simple-knn-cfloat-compat.patch` is the one-line compatibility patch applied before building the `simple-knn` CUDA extension.

## Activate an existing environment

From an SSH session on a CUDA-capable CREMI machine:

```bash
source /net/travail/sacosta/trdp-fisheyeGS/metadata/setup/jessica_activate.sh
nvidia-smi
python -c 'import torch; print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))'
```

The `.sh` file activates the environment that is already installed in the shared CREMI work space; it does not reinstall packages.

## Limitations

- The host must have an NVIDIA GPU. CPU-only CREMI machines cannot train DirectFisheye-GS.
- The NVIDIA driver must support CUDA 12.6. If PyTorch reports a driver/CUDA error, use another GPU host or ask CREMI; do not modify the shared environment.
- The environment and custom extensions are shared through `/net/travail/sacosta` and support common NVIDIA compute capabilities 7.5, 8.0, 8.6, and 8.9.
