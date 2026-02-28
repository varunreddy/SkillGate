# PyTorch Training Expert

Use this expert for deep learning pipelines with reproducible training and evaluation.

## Execution behavior

1. Set deterministic seeds and reproducible data splits.
2. Build explicit model, loss, optimizer, and scheduler blocks.
3. Use DataLoader batching and optional mixed precision on GPU.
4. Track train/validation loss and stop with patience-based early stopping.
5. Save checkpoints and best model state with metadata.

## Output contract

- Record device choice (CPU/GPU) and precision mode.
- Include epoch-wise metric history.
- Save at least one recoverable checkpoint.
- Report final model performance on held-out validation/test data.
