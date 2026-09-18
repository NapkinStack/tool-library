"""What the `test` verb leaves behind.

D3's fourth criterion asks for the run itself, in `.evidence/`: the sheet's evidence is
machine-produced or it is an assertion (charter, C1.3). The record says whether `catalog`
was importable while the suite ran — it must never be.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

EVIDENCE = Path(__file__).resolve().parents[1] / ".evidence"


def pytest_sessionfinish(session, exitstatus) -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    record = {
        "verb": "test",
        "module": "loans",
        "collected": session.testscollected,
        "failed": session.testsfailed,
        "exit_status": int(exitstatus),
        "catalog_importable": importlib.util.find_spec("catalog") is not None,
        "catalog_imported": "catalog" in sys.modules,
    }
    (EVIDENCE / "test-run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
