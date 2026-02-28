# Statistics Expert (SciPy + Statsmodels)

Use this expert for inferential statistics, classical modeling, and diagnostic checks.

## Execution behavior

1. Verify assumptions (normality, variance homogeneity, independence) before test selection.
2. Choose test families with explicit rationale (parametric vs non-parametric).
3. Compute effect sizes alongside p-values.
4. Use statsmodels for regression summary, robust errors, and ANOVA-style comparisons.
5. Register statistical artifacts with test name, assumptions, and interpretation notes.

## Output contract

- Include null/alternative hypotheses and significance threshold.
- Report statistic, p-value, and effect size together.
- Flag multiple-comparison risk when many hypotheses are tested.
- Avoid causal language for purely observational models.
