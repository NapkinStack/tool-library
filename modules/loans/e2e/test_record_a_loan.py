"""D3, scenario by scenario, in the order the cycle states them.

S1 to S3 drive the page at a 375-pixel-wide viewport and leave their screenshots in
`.evidence/`; S4 asserts that nothing of `catalog` was present while they ran.
"""

from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

from loans import catalogue_double, contract
from loans.catalogue import DOUBLE

DRILL = "9f1c6f6a-5f1e-4e2a-9a1e-6a1b0c2d3e4f"  # the contract's own example
NOT_LISTED = "00000000-0000-4000-8000-000000000000"
HANDED_OVER = "2026-09-21"
BACK_ON = "2026-09-24"


def what_the_double_answers() -> list[dict]:
    """Off the browser driver's loop: Playwright's synchronous API keeps one running in
    this thread, and a second loop cannot be started inside it."""
    with ThreadPoolExecutor(max_workers=1) as aside:
        return aside.submit(asyncio.run, _ask_the_double()).result()


async def _ask_the_double() -> list[dict]:
    """Every operation the contract declares, put to the double, answer by answer."""
    asked = [
        ("listTools", "/tools"),
        ("getTool", f"/tools/{DRILL}"),
        ("getTool", f"/tools/{NOT_LISTED}"),
        ("getTool", "/tools/a-hammer-drill"),
    ]
    async with httpx.AsyncClient(
        transport=httpx.ASGITransport(app=catalogue_double.build()), base_url=DOUBLE
    ) as double:
        answers = [(operation, request, await double.get(request)) for operation, request in asked]
    return [
        {
            "operation": operation,
            "request": request,
            "status": answer.status_code,
            "payload": answer.json(),
        }
        for operation, request, answer in answers
    ]


def state_of(page, tool_id: str) -> str:
    return page.locator(f"li[data-tool='{tool_id}'] [data-state]").get_attribute("data-state")


def fill_in_a_loan(page, base_url: str, handed_over: str, back_on: str) -> None:
    page.goto(base_url)
    page.select_option("#tool_id", DRILL)
    page.fill("#holder", "Bruno")
    page.fill("#handed_over", handed_over)
    page.fill("#back_on", back_on)


def test_bruno_records_a_loan_and_the_tool_goes_out_on_loan(page, neighbourhood, shot) -> None:
    fill_in_a_loan(page, neighbourhood, HANDED_OVER, BACK_ON)
    shot(page, "s1-the-loan-to-record.png")

    page.get_by_role("button", name="Record the loan").click()

    recorded = page.locator("#history li").first.inner_text()
    assert "Bruno" in recorded
    assert HANDED_OVER in recorded and BACK_ON in recorded
    assert state_of(page, DRILL) == "out-on-loan"
    assert "Out on loan" in page.locator(f"li[data-tool='{DRILL}']").inner_text()
    shot(page, "s1-the-loan-recorded.png")


def test_the_return_is_recorded_and_the_history_says_who_held_the_tool(
    page, neighbourhood, shot
) -> None:
    fill_in_a_loan(page, neighbourhood, HANDED_OVER, BACK_ON)
    page.get_by_role("button", name="Record the loan").click()
    assert state_of(page, DRILL) == "out-on-loan"
    shot(page, "s2-before-the-return.png")

    page.get_by_role("button", name="Record the return of Hammer drill").click()

    history = page.locator("#history li").first.inner_text()
    assert "Bruno held Hammer drill" in history
    assert f"from {HANDED_OVER} to {BACK_ON}" in history
    assert state_of(page, DRILL) == "available"
    assert "Available" in page.locator(f"li[data-tool='{DRILL}']").inner_text()
    shot(page, "s2-the-tool-is-back.png")


def test_a_return_date_before_the_hand_over_is_refused_and_nothing_is_recorded(
    page, neighbourhood, shot
) -> None:
    fill_in_a_loan(page, neighbourhood, handed_over=BACK_ON, back_on=HANDED_OVER)

    page.get_by_role("button", name="Record the loan").click()

    problem = page.locator("#error")
    assert problem.is_visible()
    assert "before the hand-over date" in problem.inner_text()
    assert "No loan recorded yet" in page.locator("#history").inner_text()
    assert state_of(page, DRILL) == "available"
    assert page.input_value("#holder") == "Bruno"  # what was typed is kept
    assert page.input_value("#handed_over") == BACK_ON
    shot(page, "s3-the-dates-are-refused.png")


def test_catalog_is_neither_running_nor_installed(evidence: Path) -> None:
    assert importlib.util.find_spec("catalog") is None, "catalog must not be installed"
    assert "catalog" not in sys.modules, "catalog must not be imported"
    assert os.environ.get("CATALOG_BASE_URL") is None, "nothing outside answers the catalogue"
    assert not [entry for entry in sys.path if "modules/catalog" in entry.replace("\\", "/")]

    record = {
        "criterion": "D3.4 - catalog neither running nor installed",
        "contract": contract.PATH.relative_to(contract.PATH.parents[3]).as_posix(),
        "contract_sha256": contract.digest(),
        "catalog_importable": False,
        "catalog_imported": False,
        "catalog_base_url_configured": False,
        "answers_came_from": "the double built from the contract, inside modules/loans",
        "transcript": what_the_double_answers(),
    }
    (evidence / "isolation.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
