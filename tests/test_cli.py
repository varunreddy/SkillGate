from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from contextlib import redirect_stdout

from skill_registry_rag.cli import main


def test_cli_retrieve_emits_enriched_fields():
    root = Path(__file__).resolve().parents[1]
    registry = root / "examples" / "registry" / "tools.enriched.json"

    buf = StringIO()
    with redirect_stdout(buf):
        code = main(
            [
                "retrieve",
                "--registry",
                str(registry),
                "--query",
                "opencv contour detection",
                "--top-k",
                "1",
            ]
        )

    assert code == 0
    payload = json.loads(buf.getvalue())
    hit = payload["hits"][0]
    assert hit["id"] == "cv.opencv-image-processing"
    assert "dependencies" in hit
    assert "risk_level" in hit
    assert "metadata" in hit
