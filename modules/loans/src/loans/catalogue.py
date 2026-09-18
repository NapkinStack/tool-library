"""What `loans` is allowed to know about a tool: what catalog-api v1 declares.

The consumer side of the contract. It reads the four fields the contract declares and
nothing beside them, so that `catalog` can rework its inside without breaking this module
(`docs/os/03-contracts.md` §5).
"""

from __future__ import annotations

import os
from dataclasses import dataclass

import httpx

from loans import catalogue_double

DOUBLE = "http://double.invalid"  # never resolved: the double answers in-process
TIMEOUT_SECONDS = 5.0


@dataclass(frozen=True)
class Tool:
    """A listed tool, in the contract's terms. Never an exact address (charter, no-go)."""

    id: str
    name: str
    lender: str
    approximate_location: str

    @classmethod
    def declared(cls, payload: dict) -> Tool:
        return cls(
            payload["id"], payload["name"], payload["lender"], payload["approximateLocation"]
        )


class Catalogue:
    """catalog-api v1, and the only door to it in this module."""

    def __init__(self, client: httpx.AsyncClient) -> None:
        self._client = client

    async def tools(self) -> list[Tool]:
        answer = await self._client.get("/tools")
        answer.raise_for_status()
        return [Tool.declared(listed) for listed in answer.json()["tools"]]

    async def tool(self, tool_id: str) -> Tool | None:
        """The tool listed under that identifier, or None — the contract declares both
        refusals, 400 for what is not an identifier and 404 for what nobody listed."""
        answer = await self._client.get(f"/tools/{tool_id}")
        if answer.status_code in (400, 404):
            return None
        answer.raise_for_status()
        return Tool.declared(answer.json())


def client() -> httpx.AsyncClient:
    """What answers the catalogue: a deployed `catalog` where one is configured, the double
    built from the contract otherwise. Nothing is deployed in this project, so the double
    is what answers — and `catalog` is neither imported nor started.

    The call is a real HTTP exchange either way: against the double it is carried in-process
    by an ASGI transport, so no port is opened and no second server has to be running.
    """
    configured = os.environ.get("CATALOG_BASE_URL")
    if configured:
        return httpx.AsyncClient(base_url=configured, timeout=TIMEOUT_SECONDS)
    return httpx.AsyncClient(
        transport=httpx.ASGITransport(app=catalogue_double.build()), base_url=DOUBLE
    )
