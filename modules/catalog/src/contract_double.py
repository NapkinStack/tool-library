"""A double built from an OpenAPI document, and from nothing else.

It carries no domain behaviour and knows nothing about tools: point it at another OpenAPI
document and it serves that one. This is what lets a consumer work against
`contracts/catalog-api/v1/openapi.yaml` before any implementation of `catalog` exists —
and there is none behind this.

Every answer comes from the document:

- a path it does not declare → 404, a method it does not declare on that path → 405, and
  the body says the double is answering rather than the contract;
- a parameter the declared schema rejects → the operation's declared 400;
- a parameter the schemas accept, whose value is not the example the document carries →
  the operation's declared 404, when it declares one: the contract describes one tool, so
  every other identifier is one it does not describe;
- otherwise → the lowest 2xx the operation declares, with the example that response
  carries, under the media type it declares.

A response declared without an example gets a 501: a contract with no example leaves its
consumer guessing (`docs/os/03-contracts.md` §7).

    python -m contract_double ../../contracts/catalog-api/v1/openapi.yaml 8000
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any

import uvicorn
import yaml
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from jsonschema import Draft202012Validator

METHODS = ["GET", "PUT", "POST", "DELETE", "PATCH"]
PROBLEM = "application/problem+json"
FROM_THE_DOUBLE = "Answered by the double built from the document, not by the contract."


def load(document: Path) -> dict[str, Any]:
    return yaml.safe_load(document.read_text(encoding="utf-8"))


def resolve(document: dict[str, Any], node: Any) -> Any:
    """Follow a local `$ref`. Nothing outside the document is ever fetched."""
    while isinstance(node, dict) and "$ref" in node:
        target: Any = document
        for step in node["$ref"].removeprefix("#/").split("/"):
            target = target[step]
        node = target
    return node


def match(declared: str, asked: str) -> dict[str, str] | None:
    """The path parameters of `asked` when it matches the declared template, else None."""
    names: list[str] = []
    pattern = ""
    for index, part in enumerate(re.split(r"{([^}]*)}", declared)):
        if index % 2:
            names.append(part)
            pattern += "([^/]+)"
        else:
            pattern += re.escape(part)
    found = re.fullmatch(pattern, asked)
    return dict(zip(names, found.groups(), strict=True)) if found else None


def said(title: str, status: int) -> JSONResponse:
    """The double speaking for itself, where the document declares nothing."""
    body = {"type": "about:blank", "title": title, "status": status, "detail": FROM_THE_DOUBLE}
    return JSONResponse(body, status_code=status, media_type=PROBLEM)


def declared(document: dict[str, Any], operation: dict[str, Any], code: int) -> JSONResponse | None:
    """The response the operation declares for that status, with the example it carries."""
    response = resolve(document, (operation.get("responses") or {}).get(str(code)))
    if not response:
        return None
    content = response.get("content") or {}
    media = next(iter(content), "application/json")
    example = resolve(document, content.get(media) or {}).get("example")
    if example is None:
        return said(f"The contract declares no example for its {code}", 501)
    return JSONResponse(example, status_code=code, media_type=media)


def serve(
    document: dict[str, Any], operation: dict[str, Any], given: dict[str, str]
) -> JSONResponse:
    """What the document says to answer, for the values this request carries."""
    for parameter in (resolve(document, p) for p in operation.get("parameters") or []):
        value = given.get(parameter["name"])
        if value is None:
            continue
        schema = resolve(document, parameter.get("schema") or {})
        if list(Draft202012Validator(schema).iter_errors(value)):
            return declared(document, operation, 400) or said(
                "Not a request the contract declares", 400
            )
        if value != str(parameter.get("example")) and (
            unknown := declared(document, operation, 404)
        ):
            return unknown
    codes = sorted(int(code) for code in operation.get("responses") or {} if code.startswith("2"))
    if not codes:
        return said("The contract declares no success for this operation", 501)
    return declared(document, operation, codes[0]) or said("Unserveable operation", 501)


def create_app(document: dict[str, Any]) -> FastAPI:
    """The double for that document. `openapi_url=None`: the document is the schema, and
    this double never publishes one of its own."""
    app = FastAPI(openapi_url=None)

    @app.api_route("/{asked:path}", methods=METHODS)
    async def from_the_document(request: Request, asked: str) -> JSONResponse:
        for path, item in (document.get("paths") or {}).items():
            values = match(path, f"/{asked}")
            if values is None:
                continue
            operation = resolve(document, item).get(request.method.lower())
            if not operation:
                return said("The contract declares no such method on that path", 405)
            return serve(document, operation, {**values, **request.query_params})
        return said("The contract declares no such path", 404)

    return app


def main(arguments: list[str]) -> int:
    """`python -m contract_double <openapi document> [port]` — it serves what it is given."""
    if not arguments:
        print(main.__doc__, file=sys.stderr)
        return 2
    port = int(arguments[1]) if len(arguments) > 1 else 8000
    app = create_app(load(Path(arguments[0])))
    uvicorn.run(app, host="127.0.0.1", port=port, log_level="warning")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
