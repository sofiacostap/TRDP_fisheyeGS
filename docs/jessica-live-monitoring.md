# Jessica live monitoring

Connect in one terminal:

```bash
ssh jessica
```

Before a run, check who is using the GPU:

```bash
nvidia-smi
```

Watch GPU memory, utilisation, and running processes in real time:

```bash
watch -n 2 nvidia-smi
```

Run training inside a named tmux session so it survives an SSH disconnect:

```bash
tmux new -s trdp-baseline
```

Launch the command with a timestamped log, for example:

```bash
python train_eval.py ... 2>&1 | tee /net/travail/sacosta/trdp-fisheyeGS/metadata/logs/<run-id>.log
```

Detach without stopping the run with `Ctrl-b`, then `d`. Later, reconnect with:

```bash
tmux attach -t trdp-baseline
```

Or follow a saved log without attaching:

```bash
tail -f /net/travail/sacosta/trdp-fisheyeGS/metadata/logs/<run-id>.log
```

Use `Ctrl-c` to stop `watch` or `tail`; this does not stop training.
