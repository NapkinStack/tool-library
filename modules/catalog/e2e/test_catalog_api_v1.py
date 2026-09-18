"""D1's three acceptance criteria, end to end (cycle 1).

One test per criterion, in the order of the test sheet. Each writes its evidence to
`.evidence/` before it asserts, so a failure is documented rather than silent.
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml
from jsonschema import Draft202012Validator
from openapi_spec_validator import OpenAPIV31SpecValidator
from playwright.sync_api import APIRequestContext
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

METHODS = ("get", "put", "post", "delete", "patch")
BASE = "urn:contract"  # the document, as the base every declared $ref resolves against
ABSENT = "00000000-0000-4000-8000-000000000000"  # well formed, and not what the contract carries
MALFORMED = "not-a-tool-id"


def resolve(document: dict[str, Any], node: Any) -> Any:
    """Follow a local `$ref`. Nothing outside the document is ever fetched."""
    while isinstance(node, dict) and "$ref" in node:
        target: Any = document
        for step in node["$ref"].removeprefix("#/").split("/"):
            target = target[step]
        node = target
    return node


def operations(document: dict[str, Any]) -> Iterator[tuple[str, str, dict[str, Any]]]:
    """Every operation the document declares — never a list written by hand."""
    for path, item in (document.get("paths") or {}).items():
        for method in METHODS:
            if operation := resolve(document, item).get(method):
                yield path, method, resolve(document, operation)


def declared(
    document: dict[str, Any], operation: dict[str, Any], status: str
) -> tuple[str, Any, Any]:
    """The media type, the schema and the example the contract declares for that status."""
    content = resolve(document, operation["responses"][status])["content"]
    media = next(iter(content))
    return media, content[media]["schema"], resolve(document, content[media])["example"]


def address(document: dict[str, Any], path: str, operation: dict[str, Any], **given: str) -> str:
    """The path to call: every path parameter takes the value given, or the contract's example."""
    for parameter in (resolve(document, p) for p in operation.get("parameters") or []):
        if parameter["in"] == "path":
            value = given.get(parameter["name"], parameter["example"])
            path = path.replace("{" + parameter["name"] + "}", value)
    return path


def against(document: dict[str, Any], schema: Any, instance: Any) -> list[str]:
    """What the declared schema rejects in that payload — empty when it accepts it."""
    registry = Registry().with_resource(
        BASE, Resource(contents=document, specification=DRAFT202012)
    )
    if reference := schema.get("$ref"):
        schema = {"$ref": f"{BASE}{reference}"}
    validator = Draft202012Validator(schema, registry=registry)
    return [error.message for error in validator.iter_errors(instance)]


def call(api: APIRequestContext, method: str, path: str) -> dict[str, Any]:
    response = api.fetch(path, method=method.upper())
    return {
        "request": {"method": method.upper(), "path": path},
        "status": response.status,
        "media_type": response.headers.get("content-type", "").split(";")[0],
        "body": response.json(),
    }


def gaps(
    document: dict[str, Any], answer: dict[str, Any], expected: tuple[str, Any, Any]
) -> list[str]:
    """Everything by which the answer departs from what the contract declares."""
    media, schema, example = expected
    found = []
    if answer["media_type"] != media:
        found.append(f"media type {answer['media_type']}, the contract declares {media}")
    if rejected := against(document, schema, answer["body"]):
        found.append(f"payload rejected by the declared schema: {rejected}")
    if answer["body"] != example:
        found.append("payload differs from the example the contract carries")
    if rejected := against(document, schema, example):
        found.append(f"the contract's own example is rejected by its own schema: {rejected}")
    return found


def test_the_document_is_a_valid_openapi_31_document(contract: Path, evidence) -> None:
    """S1 — the contract is a valid OpenAPI 3.1 document, and the report says so."""
    raw = contract.read_bytes()
    document = yaml.safe_load(raw.decode("utf-8"))
    version = str(document.get("openapi"))
    errors = [error.message for error in OpenAPIV31SpecValidator(document).iter_errors()]
    evidence(
        "openapi-validation.json",
        {
            "document": "contracts/catalog-api/v1/openapi.yaml",
            "sha256": hashlib.sha256(raw).hexdigest(),
            "declared_openapi_version": version,
            "validator": "openapi_spec_validator.OpenAPIV31SpecValidator",
            "errors": errors,
            "valid_openapi_3_1_document": not errors and version.startswith("3.1"),
        },
    )
    assert version.startswith("3.1"), f"the document declares OpenAPI {version}, not 3.1"
    assert not errors, f"the document is not a valid OpenAPI 3.1 document: {errors}"


def test_every_declared_operation_answers_as_the_contract_declares(
    document: dict[str, Any], double: APIRequestContext, evidence
) -> None:
    """S2 — every declared operation, called with the contract's own examples."""
    transcript: list[dict[str, Any]] = []
    faults: list[str] = []
    for path, method, operation in operations(document):
        status = min(code for code in operation["responses"] if code.startswith("2"))
        expected = declared(document, operation, status)
        answer = call(double, method, address(document, path, operation))
        found = gaps(document, answer, expected)
        if answer["status"] != int(status):
            found.insert(0, f"status {answer['status']}, the contract declares {status}")
        transcript.append({"operation": operation["operationId"], **answer, "gaps": found})
        faults += [f"{operation['operationId']}: {gap}" for gap in found]
    evidence("operations-transcript.json", {"calls": transcript})
    assert transcript, "the contract declares no operation"
    assert not faults, f"the double did not answer as the contract declares: {faults}"


def test_the_declared_error_cases_answer_as_the_contract_declares(
    document: dict[str, Any], double: APIRequestContext, evidence
) -> None:
    """S3 — a tool that does not exist, and a malformed request."""
    path, method, operation = next(
        (p, m, o) for p, m, o in operations(document) if {"400", "404"} <= set(o["responses"])
    )
    parameter = resolve(document, operation["parameters"][0])
    accepts = resolve(document, parameter["schema"])
    cases = [
        ("404", "a tool that does not exist", ABSENT, True),
        ("400", "a malformed request", MALFORMED, False),
    ]
    transcript: list[dict[str, Any]] = []
    faults: list[str] = []
    for status, given, value, well_formed in cases:
        expected = declared(document, operation, status)
        answer = call(
            double, method, address(document, path, operation, **{parameter["name"]: value})
        )
        found = gaps(document, answer, expected)
        if bool(not against(document, accepts, value)) is not well_formed:
            found.insert(0, f"'{value}' is not the kind of value this case is about")
        if answer["status"] != int(status):
            found.insert(0, f"status {answer['status']}, the contract declares {status}")
        transcript.append({"case": given, **answer, "gaps": found})
        faults += [f"{given}: {gap}" for gap in found]
    evidence("errors-transcript.json", {"operation": operation["operationId"], "cases": transcript})
    assert not faults, (
        f"the double did not answer the error cases as the contract declares: {faults}"
    )
