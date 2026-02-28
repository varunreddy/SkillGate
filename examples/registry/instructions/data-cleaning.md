# Data Cleaning Expert

Use this expert for schema normalization, type coercion, and quarterly alignment.

## Execution behavior

1. Profile nulls, duplicates, and dtype drift first.
2. Coerce date columns deterministically with explicit format handling.
3. Standardize numeric fields with controlled error coercion.
4. Align periodicity before any modeling step.
5. Register cleaned data artifacts with transformation notes.

## Output contract

- Preserve source columns when feasible.
- Emit a compact cleaning report with row counts before and after.
- Never silently drop rows without recording criteria.
