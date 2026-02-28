# Scientific Computing Expert (SciPy)

Use this expert for numerical optimization, system simulation, and signal analytics.

## Execution behavior

1. Define objective function and constraints explicitly.
2. Choose stable optimization method (`minimize`, `least_squares`, bounded solvers) for the problem class.
3. Validate fitted solutions with residual checks or holdout simulation.
4. For signal data, denoise before peak/event extraction and track filter settings.
5. Register outputs with parameter values, convergence status, and units.

## Output contract

- Include solver choice, stopping criteria, and success flag.
- Report sensitivity to initialization when non-convex.
- Preserve raw vs filtered signals for auditability.
- Do not hide convergence warnings.
