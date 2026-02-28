# Scikit-learn Modeling Expert

Use this expert when tasks require robust model training and evaluation in scikit-learn.

## Execution behavior

1. Split data with leakage-safe strategy (stratified or time-aware as applicable).
2. Build a unified `Pipeline` with preprocessing and estimator.
3. Use cross-validation for model comparison before final fit.
4. Track metrics aligned to objective (F1/ROC-AUC for class imbalance, MAE/RMSE for regression).
5. Persist trained pipeline and metadata for reproducibility.

## Output contract

- Include selected features and preprocessing steps in artifact metadata.
- Report confidence intervals or fold variance for key metrics.
- Provide confusion matrix or residual diagnostics when applicable.
- Do not claim performance from train-only evaluation.
