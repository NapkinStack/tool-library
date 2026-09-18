"""The catalogue as the contract declares it, built from the contract document.

A consumer-side double (`docs/os/03-contracts.md` §5). It exists so that `loans` can be
written, run and verified with `catalog` neither running nor installed — D3's fourth
criterion and ADR-0001's success criterion.

Nothing here is invented: the tools it serves, the statuses and the problem payloads all
come out of `contracts/catalog-api/v1/openapi.yaml`'s own examples, so the double cannot
drift away from the contract without the contract itself changing. It answers what the
contract declares, and nothing else.
"""

from __future__ import annotations

import re
from typing import Any

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from loans import contract

PROBLEM = "application/problem+json"
TOOLS = "/tools"
ONE_TOOL = "/tools/{toolId}"


def build() -> FastAPI:
    document = contract.document()
    tools: list[dict[str, Any]] = contract.example(TOOLS, "200")["tools"]
    listed = {tool["id"]: tool for tool in tools}
    identifier = re.compile(document["components"]["schemas"]["ToolId"]["pattern"])

    app = FastAPI(title=document["info"]["title"], version=document["info"]["version"])

    @app.get(TOOLS)
    def list_tools() -> dict[str, Any]:
        return {"tools": tools}

    @app.get("/tools/{tool_id}")
    def get_tool(tool_id: str) -> Any:
        if not identifier.fullmatch(tool_id):
            return _problem(ONE_TOOL, "400")
        if tool_id not in listed:
            return _problem(ONE_TOOL, "404")
        return listed[tool_id]

    return app


def _problem(path: str, status: str) -> JSONResponse:
    payload = contract.example(path, status, PROBLEM)
    return JSONResponse(payload, status_code=int(status), media_type=PROBLEM)
