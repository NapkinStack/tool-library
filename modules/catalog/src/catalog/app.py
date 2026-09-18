"""The neighbourhood's page, and the contract `catalog` provides.

Two surfaces, and they are not the same thing:

- **the page**, server-rendered, one page wide enough for a phone and no wider (charter, C2).
  It is `catalog`'s own, and it is not in the contract: publishing is something a neighbour
  does, not something another module does;
- **`catalog-api` v1**, which is how another module knows this one (`docs/os/03-contracts.md`).
  The document is hand-written and is never regenerated from what is below — this app
  conforms to it, not the reverse, and `e2e/test_producer_contract.py` is what says so.

Start it from the module folder, exactly as `README.md` says — and as the scenarios do:

    PYTHONPATH=src uv run python -m catalog.app [database] [port]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException

from catalog import listing, store

MODULE = Path(__file__).resolve().parents[2]
PAGES = Jinja2Templates(directory=Path(__file__).parent / "templates")
PROBLEM = "application/problem+json"
# The identifier the contract declares, as it declares it: `format` is an annotation, and the
# pattern is what carries the rule.
TOOL_ID = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")


def problem(title: str, status: int, detail: str, headers: dict[str, str] | None = None):
    """RFC 9457 problem details, the shape the contract declares for everything that is not
    an answer. `type` stays `about:blank` while no documentation page is published."""
    body = {"type": "about:blank", "title": title, "status": status, "detail": detail}
    return JSONResponse(body, status_code=status, media_type=PROBLEM, headers=headers)


def create_app(database: Path) -> FastAPI:
    """`openapi_url=None`: the contract is the document in `contracts/`, and this app never
    publishes one of its own (charter, C2)."""
    app = FastAPI(openapi_url=None)
    connection = store.open_store(database)

    def page(request: Request, correct: tuple[str, str] | None = None, typed: dict | None = None):
        field, message = correct or (None, None)
        return PAGES.TemplateResponse(
            request=request,
            name="page.html",
            context={
                "listings": store.listed(connection),
                "fields": listing.FIELDS,
                "typed": typed or {},
                "correct": field,
                "message": message,
            },
            status_code=422 if correct else 200,
        )

    @app.exception_handler(HTTPException)
    async def as_a_problem(request: Request, error: HTTPException):
        """Everything the routes do not answer themselves — an unknown path, a method this
        module does not serve — answered in the shape the contract declares. `error.headers`
        carries the `Allow` the router builds for a 405, and RFC 9110 requires it."""
        return problem(str(error.detail), error.status_code, "", headers=error.headers)

    @app.get("/")
    def neighbourhood(request: Request):
        return page(request)

    @app.post("/")
    async def publish(request: Request):
        form = await request.form()
        typed = {field: str(form.get(field, "")) for field in listing.FIELDS}
        if correct := listing.incomplete(typed):
            return page(request, correct=correct, typed=typed)
        store.add(connection, listing.published(typed))
        # See it, rather than be asked to send the form again if the page is reloaded.
        return RedirectResponse("/", status_code=303)

    @app.get("/tools")
    def list_tools():
        """`listTools`. An empty list is a normal answer: a neighbourhood starts with nothing."""
        return JSONResponse({"tools": [item.as_declared() for item in store.listed(connection)]})

    @app.get("/tools/{tool_id}")
    def get_tool(tool_id: str):
        """`getTool`. The two error cases are the contract's own, word for word."""
        if not TOOL_ID.fullmatch(tool_id):
            return problem(
                "That is not a tool identifier", 400, "toolId is a UUID, as this contract declares."
            )
        found = store.one(connection, tool_id)
        if found is None:
            return problem(
                "No tool is listed under that identifier",
                404,
                "It may never have been listed, or the neighbour may have withdrawn it.",
            )
        return JSONResponse(found.as_declared())

    return app


def main(arguments: list[str]) -> int:
    """`PYTHONPATH=src python -m catalog.app [database] [port]`, from the module folder."""
    database = Path(arguments[0]) if arguments else MODULE / "catalog.sqlite3"
    port = int(arguments[1]) if len(arguments) > 1 else 8000
    uvicorn.run(create_app(database), host="127.0.0.1", port=port, log_level="warning")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
