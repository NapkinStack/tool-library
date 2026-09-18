"""The consumer side of catalog-api v1: I only use what was promised.

`docs/os/03-contracts.md` §5. Every answer below is checked against the schemas of
`contracts/catalog-api/v1/openapi.yaml`, and the double under test is built from that same
document — not from `catalog`, which this module never imports, installs or starts.
"""

from __future__ import annotations

import asyncio
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
from jsonschema import Draft202012Validator

from loans import catalogue_double, contract
from loans.catalogue import DOUBLE, Catalogue

LISTED = "9f1c6f6a-5f1e-4e2a-9a1e-6a1b0c2d3e4f"  # the contract's own example
NOT_LISTED = "00000000-0000-4000-8000-000000000000"
NOT_AN_IDENTIFIER = "a-hammer-drill"


def through_the_contract(exchange: Callable[[httpx.AsyncClient], Awaitable[Any]]) -> Any:
    """One exchange with the double, carried exactly as the page carries it."""

    async def carried() -> Any:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=catalogue_double.build()), base_url=DOUBLE
        ) as client:
            return await exchange(client)

    return asyncio.run(carried())


def declares(name: str, payload: object) -> None:
    Draft202012Validator(contract.schema(name)).validate(payload)


def test_the_list_of_tools_answers_what_the_contract_declares() -> None:
    answer = through_the_contract(lambda client: client.get("/tools"))

    assert answer.status_code == 200
    declares("ToolList", answer.json())


def test_one_listed_tool_answers_what_the_contract_declares() -> None:
    answer = through_the_contract(lambda client: client.get(f"/tools/{LISTED}"))

    assert answer.status_code == 200
    declares("Tool", answer.json())


def test_an_identifier_that_is_not_one_is_refused_as_the_contract_declares() -> None:
    answer = through_the_contract(lambda client: client.get(f"/tools/{NOT_AN_IDENTIFIER}"))

    assert answer.status_code == 400
    assert answer.headers["content-type"].startswith("application/problem+json")
    declares("Problem", answer.json())


def test_a_tool_nobody_listed_answers_as_the_contract_declares() -> None:
    answer = through_the_contract(lambda client: client.get(f"/tools/{NOT_LISTED}"))

    assert answer.status_code == 404
    assert answer.headers["content-type"].startswith("application/problem+json")
    declares("Problem", answer.json())


def test_the_consumer_reads_only_the_fields_the_contract_declares() -> None:
    declared = set(contract.document()["components"]["schemas"]["Tool"]["properties"])

    tools = through_the_contract(lambda client: Catalogue(client).tools())
    served = through_the_contract(lambda client: client.get("/tools"))

    assert [tool.name for tool in tools] == ["Hammer drill", "Extension ladder"]
    assert [tool.lender for tool in tools] == ["Amina", "Bruno"]
    assert all(set(listed) <= declared for listed in served.json()["tools"])


def test_a_tool_that_is_not_listed_is_no_tool_at_all() -> None:
    assert through_the_contract(lambda client: Catalogue(client).tool(LISTED)) is not None
    assert through_the_contract(lambda client: Catalogue(client).tool(NOT_LISTED)) is None
    assert through_the_contract(lambda client: Catalogue(client).tool(NOT_AN_IDENTIFIER)) is None
