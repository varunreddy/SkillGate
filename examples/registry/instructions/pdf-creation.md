# PDF Creation Expert

Use this expert when analysis output must be delivered as deterministic PDF documents.

## Execution behavior

1. Build a clean intermediate format (Markdown or HTML) before rendering.
2. Apply print-safe styles (page margins, typography, table wraps, heading hierarchy).
3. Render with a deterministic backend (WeasyPrint or ReportLab).
4. Validate generated PDF file exists and has non-zero size.
5. Register PDF artifact path and include source format traceability.

## Output contract

- Support both narrative text and embedded chart images.
- Preserve numeric table alignment and avoid clipped cells.
- Include failure-safe message when PDF backend is unavailable.
- Output should be reproducible from the same source input.
