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
```

Then confirm it is ready:

```bash
python -c 'import torch; print(torch.__version__, torch.cuda.get_device_name(0))'
```

Do not re-run the installer on every login. Activation simply selects the already-installed environment.

Before a training run on a different host, check that the GPU is present and PyTorch can use it:

```bash
nvidia-smi
python -c 'import torch; print(torch.cuda.get_device_name(0), torch.cuda.get_device_capability(0))'
```

CPU-only hosts cannot train DirectFisheye-GS. If a host reports a driver error, use a newer CUDA-capable workstation or contact CREMI rather than modifying the shared environment.
