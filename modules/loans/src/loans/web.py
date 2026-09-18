"""The one page a neighbour uses, on a phone, on a doorstep.

Server-rendered HTML, one round trip, no build step (charter, C2). One list and one form
(cycle 1, *Out of scope*): what is listed and who holds it, the loan to record, and the
history that replaces trust between neighbours who have not met.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, Form, Request, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from loans.catalogue import Catalogue, client
from loans.records import Loans, Refused

TEMPLATES = Jinja2Templates(directory=str(Path(__file__).resolve().parent / "templates"))
SEE_THE_PAGE_AGAIN = 303


def create_app() -> FastAPI:
    app = FastAPI(title="loans", description="Who holds a listed tool, and until when.")
    catalogue = Catalogue(client())
    loans = Loans()

    async def page(
        request: Request, *, error: str = "", typed: dict | None = None, status: int = 200
    ) -> HTMLResponse:
        return TEMPLATES.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "tools": await catalogue.tools(),
                "loans": loans.recorded(),
                "out": loans.out_on_loan(),
                "error": error,
                "typed": typed or {},
            },
            status_code=status,
        )

    @app.get("/", response_class=HTMLResponse)
    async def neighbourhood(request: Request) -> HTMLResponse:
        return await page(request)

    @app.post("/loans", response_class=HTMLResponse)
    async def record_a_loan(
        request: Request,
        tool_id: str = Form(""),
        holder: str = Form(""),
        handed_over: str = Form(""),
        back_on: str = Form(""),
    ) -> Response:
        typed = {
            "tool_id": tool_id,
            "holder": holder,
            "handed_over": handed_over,
            "back_on": back_on,
        }
        tool = await catalogue.tool(tool_id)
        if tool is None:
            return await page(
                request, error="Choose one of the tools listed above.", typed=typed, status=400
            )
        try:
            loans.record(
                tool_id=tool.id,
                tool_name=tool.name,
                holder=holder,
                handed_over=handed_over,
                back_on=back_on,
            )
        except Refused as refused:
            return await page(request, error=str(refused), typed=typed, status=400)
        return RedirectResponse("/", status_code=SEE_THE_PAGE_AGAIN)

    @app.post("/loans/{loan_id}/return")
    def record_a_return(loan_id: int) -> Response:
        loans.record_return(loan_id)
        return RedirectResponse("/", status_code=SEE_THE_PAGE_AGAIN)

    return app
