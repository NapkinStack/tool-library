"""D2's fourth acceptance criterion: the producer answers its own contract (cycle 1).

The producer side of `docs/os/03-contracts.md` §5 — *I honour what I promised*. The document
is the one `catalog` provides, read as it is written: it is never regenerated from this
module's models (charter, C2), and this test is what stops the two drifting apart.

Schemathesis is the producer-side tool the charter's C2 fixes. It calls every operation the
document declares — with the examples the document carries, with values its schemas accept,
and with values they reject — and judges each answer against the document alone.
"""

from __future__ import annotations

import hashlib
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

import pytest
import schemathesis
from jsonschema import Draft202012Validator
from schemathesis import Case, Config

# Fixed: a scenario that answers differently from one run to the next is evidence of nothing.
SEED = 1
RECORDS: dict[str, dict[str, Any]] = {}


def resolve(document: dict[str, Any], node: Any) -> Any:
    """Follow a local `$ref`. Nothing outside the document is ever fetched.

    Duplicated from D1's scenarios on purpose: two oracles sharing a reader go green
    together on a bug they hold in common (`AGENTS.md`).
    """
    while isinstance(node, dict) and "$ref" in node:
        target: Any = document
        for step in node["$ref"].removeprefix("#/").split("/"):
            target = target[step]
        node = target
    return node


def declared_refusal(document: dict[str, Any], case: Case) -> int | None:
    """The status the contract declares for a request its own schemas reject, when this case
    carries one — None when the case is readable or the document declares no such answer.

    Schemathesis judges a status against the list the operation declares, so a `404` for an
    identifier that is not an identifier would pass: `catalog` would be saying *no tool is
    listed under that identifier* about a request it cannot even read. Found by mutation.
    """
    item = resolve(document, document["paths"].get(case.path) or {})
    operation = resolve(document, item.get(case.method.lower()) or {})
    for declared in (resolve(document, p) for p in operation.get("parameters") or []):
        value = (case.path_parameters or {}).get(declared["name"])
        schema = resolve(document, declared.get("schema") or {})
        if value is not None and list(Draft202012Validator(schema).iter_errors(value)):
            return 400 if "400" in (operation.get("responses") or {}) else None
    return None


@pytest.fixture(scope="session")
def catalog_schema(contract: Path, listed_neighbourhood: str) -> schemathesis.BaseSchema:
    """The contract document, pointed at `catalog` itself rather than at the double."""
    schema = schemathesis.openapi.from_path(contract, config=Config(seed=SEED))
    schema.config.update(base_url=listed_neighbourhood)
    return schema


@pytest.fixture(scope="session", autouse=True)
def report(contract: Path, evidence: Callable[[str, Any], Path]) -> Iterator[None]:
    """Written at teardown, whatever the outcome: a failure is documented rather than silent."""
    yield
    evidence(
        "producer-contract-report.json",
        {
            "document": "contracts/catalog-api/v1/openapi.yaml",
            "sha256": hashlib.sha256(contract.read_bytes()).hexdigest(),
            "producer": "catalog, started by the command README.md documents",
            "checked_by": f"schemathesis {schemathesis.SCHEMATHESIS_VERSION}, seed {SEED}",
            "operations": RECORDS,
        },
    )


schema = schemathesis.pytest.from_fixture("catalog_schema")


@schema.parametrize()
def test_catalog_answers_the_contract_it_provides(case: Case, document: dict[str, Any]) -> None:
    """S4 — every operation the contract declares, called against the running module."""
    record = RECORDS.setdefault(case.operation.label, {"calls": 0, "statuses": {}, "gaps": []})
    response = case.call()
    record["calls"] += 1
    seen = str(response.status_code)
    record["statuses"][seen] = record["statuses"].get(seen, 0) + 1
    refusal = declared_refusal(document, case)
    try:
        if refusal is not None and response.status_code != refusal:
            raise AssertionError(
                f"status {response.status_code}, the contract declares {refusal} for a request "
                "its own schemas reject"
            )
        case.validate_response(response)
    except Exception as gap:
        record["gaps"].append(f"{case.method} {case.formatted_path}: {str(gap)[:400]}")
        raise
