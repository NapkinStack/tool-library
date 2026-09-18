"""catalog-api v1, the one thing this module knows about the catalogue.

The document is read here and nowhere else, so that everything downstream depends on the
contract rather than on a copy of it (ADR-0001). It is never edited from here: `v1` is
frozen once merged, and a change to it is a decision, not a fix (charter, C2).
"""

from __future__ import annotations

import hashlib
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

PATH = Path(__file__).resolve().parents[4] / "contracts" / "catalog-api" / "v1" / "openapi.yaml"


@lru_cache(maxsize=1)
def document() -> dict[str, Any]:
    return yaml.safe_load(PATH.read_text(encoding="utf-8"))


def digest() -> str:
    """Which contract answered, byte for byte — the evidence names it."""
    return hashlib.sha256(PATH.read_bytes()).hexdigest()


def schema(name: str) -> dict[str, Any]:
    """One declared schema, usable on its own: its `$ref`s resolve inside the document."""
    return {"$ref": f"#/components/schemas/{name}", "components": document()["components"]}


def example(path: str, status: str, media: str = "application/json") -> Any:
    """What the contract itself answers for that operation — never something invented."""
    return document()["paths"][path]["get"]["responses"][status]["content"][media]["example"]
