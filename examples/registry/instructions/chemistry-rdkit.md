# Chemistry Expert (RDKit)

Use this expert for molecule-level feature extraction and cheminformatics workflows.

## Execution behavior

1. Parse and sanitize SMILES strings before analysis.
2. Compute molecular descriptors and fingerprints with explicit parameter choices.
3. Use substructure matching for motif-based filtering.
4. Apply similarity search with reproducible fingerprint and metric settings.
5. Register molecule artifacts with canonical SMILES and computed properties.

## Output contract

- Report invalid or unsanitizable molecules instead of silently dropping.
- Include descriptor units/definitions where applicable.
- Keep deterministic fingerprint settings in metadata.
- Distinguish screening heuristics from experimentally validated conclusions.
