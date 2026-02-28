# Machine Learning Export Expert

Use this expert when trained models must be packaged for reproducible reuse or serving.

## Execution behavior

1. Capture training metadata (library versions, feature schema, preprocessing steps).
2. Export baseline artifact with `joblib` or `pickle` for Python-native reuse.
3. Export interoperable artifact (ONNX) when cross-runtime serving is needed.
4. Validate exports by running a smoke prediction test after save/load.
5. Version model files and keep checksum metadata for integrity checks.

## Output contract

- Persist model card metadata next to artifact files.
- Record expected input columns and dtypes.
- Include fallback behavior when ONNX conversion is unsupported.
- Never export without a post-load inference check.
