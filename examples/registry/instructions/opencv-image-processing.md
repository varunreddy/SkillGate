# OpenCV Image Processing Expert

Use this expert for computer vision preprocessing and feature extraction workflows.

## Execution behavior

1. Load and validate image channels and dimensions.
2. Apply deterministic preprocessing (resize, denoise, color-space conversion).
3. Use thresholding/edge detection for shape-aware segmentation.
4. Extract contours, regions, or keypoints based on task objective.
5. Save processed outputs and measurement summaries as artifacts.

## Output contract

- Preserve originals and processed outputs separately.
- Record parameter values for each transform step.
- Include quality checks for low-contrast/noisy inputs.
- Report failure cases when detection confidence is weak.
