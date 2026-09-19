"""Every example a contract document gives is what its own schema declares.

A consumer's double is built from these examples (`modules/loans/src/loans/catalogue_double.py`):
an example that breaks its schema is a double that lies to every consumer tested against it.
The module's `check` validates the document's structure, never its examples; this suite reads
them. A pull request that changes only a contract document runs this module's verbs alone, so
nothing else would catch it.
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest
import yaml
from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

CONTRACTS = Path(__file__).resolve().parents[1]
DOCUMENTS = sorted(CONTRACTS.glob("*/v*/openapi.yaml"))
BY_REFERENCE = object()


def escaped(key: object) -> str:
    return str(key).replace("~", "~0").replace("/", "~1")


def examples(node: Any, pointer: str = "") -> Iterator[tuple[str, str, Any]]:
    """(where the example is, where its schema is, the example): every media type, parameter
    and header that gives both a schema and an example."""
    if isinstance(node, dict):
        if "schema" in node:
            if "example" in node:
                yield f"{pointer}/example", f"{pointer}/schema", node["example"]
            for name, given in (node.get("examples") or {}).items():
                value = given.get("value", BY_REFERENCE) if isinstance(given, dict) else given
                yield f"{pointer}/examples/{escaped(name)}", f"{pointer}/schema", value
        for key, value in node.items():
            yield from examples(value, f"{pointer}/{escaped(key)}")
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from examples(value, f"{pointer}/{index}")


def read(document: Path) -> Any:
    return yaml.safe_load(document.read_text(encoding="utf-8"))


CASES = [
    pytest.param(document, schema, example, id=f"{document.relative_to(CONTRACTS)}#{where}")
    for document in DOCUMENTS
    for where, schema, example in examples(read(document))
]


def test_the_documents_and_their_examples_are_found() -> None:
    """No quiet pass: a suite that finds nothing to read says so."""
    assert DOCUMENTS, "no contract document found under contracts/<name>/v<n>/openapi.yaml"
    assert CASES, "no example found in the contract documents"


@pytest.mark.parametrize(("document", "schema", "example"), CASES)
def test_the_example_is_what_its_schema_declares(document: Path, schema: str, example: Any) -> None:
    assert example is not BY_REFERENCE, (
        "an example given by reference or as an external value: read it here before a "
        "double relies on it"
    )
    uri = document.as_uri()
    registry = Registry().with_resource(
        uri, Resource(contents=read(document), specification=DRAFT202012)
    )
    validator = Draft202012Validator({"$ref": f"{uri}#{schema}"}, registry=registry)

    broken = [f"{error.json_path}: {error.message}" for error in validator.iter_errors(example)]

    assert not broken, broken
