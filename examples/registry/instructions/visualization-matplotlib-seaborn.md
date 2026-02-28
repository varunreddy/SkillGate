# Visualization Expert (Matplotlib + Seaborn)

Use this expert when the task needs clear, publication-quality figures.

## Execution behavior

1. Select chart type by analytical goal (trend, distribution, relationship, composition).
2. Build visuals with seaborn-first style and matplotlib for layout control.
3. Enforce readable titles, axis labels, units, and legends.
4. Use consistent color palettes and avoid misleading axis truncation.
5. Save outputs to deterministic paths and register them as figure artifacts.

## Output contract

- Include at least one explanatory caption per figure.
- Use high-resolution export (`dpi >= 180`) for report integration.
- Prefer PNG for documents and SVG for web where supported.
- Keep figure code reproducible from raw dataframe inputs.
