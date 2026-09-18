"""What the scenarios need: the contract document, something serving it, and the folder the
evidence is written to.

The scenarios read the document themselves rather than through `contract_double`: an oracle
that shares its reader with the thing it judges goes green on a bug they hold in common.

D1's scenarios call the double built from the document. D2's drive `catalog` itself — the
page, in a browser at a phone's width, and the contract this module provides answered by the
module rather than by a double.
"""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
import yaml
from playwright.sync_api import APIRequestContext, Browser, Error, Page, Playwright, sync_playwright

from catalog.listing import Listing
from catalog.store import add, open_store

MODULE = Path(__file__).resolve().parents[1]
CONTRACT = MODULE.parents[1] / "contracts" / "catalog-api" / "v1" / "openapi.yaml"
EVIDENCE = MODULE / ".evidence"
READY = 20.0  # seconds allowed for a server to accept its first request
PHONE = 375  # the viewport the discovery's platform constraint is about (charter, C1)


@pytest.fixture(scope="session")
def contract() -> Path:
    return CONTRACT


@pytest.fixture(scope="session")
def document() -> dict[str, Any]:
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


@pytest.fixture(scope="session")
def evidence() -> Callable[[str, Any], Path]:
    """Writes one piece of machine-produced evidence, and returns where it landed."""

    def write(name: str, payload: Any) -> Path:
        EVIDENCE.mkdir(exist_ok=True)
        path = EVIDENCE / name
        path.write_text(
            json.dumps(
                {"written_at": datetime.now(UTC).isoformat(), "contract": CONTRACT.name, **payload},
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        return path

    return write


@pytest.fixture(scope="session")
def driver() -> Iterator[Playwright]:
    """One driver for the whole session: the API request context D1 calls the double with,
    and the browser D2's page is judged in."""
    with sync_playwright() as playwright:
        yield playwright


def free_port() -> int:
    with socket.socket() as free:
        free.bind(("127.0.0.1", 0))
        return int(free.getsockname()[1])


def answering(process: subprocess.Popen[bytes], base: str, what: str) -> None:
    """Waits for the observable event — the first answer — never for a duration
    (`playbooks/tests.md`)."""
    deadline = time.monotonic() + READY
    while True:
        if process.poll() is not None:
            raise RuntimeError(f"{what} exited with {process.returncode} before answering")
        try:
            with urllib.request.urlopen(f"{base}/", timeout=1):  # a port this test opened
                return
        except OSError:
            if time.monotonic() > deadline:
                raise RuntimeError(f"{what} did not answer within {READY:.0f}s") from None


@contextmanager
def serving(database: Path) -> Iterator[str]:
    """`catalog` itself, on its own SQLite file, started by the command `README.md` documents
    and by no other: a documented way to start it that nothing runs is a way that stops
    working unnoticed."""
    port = free_port()
    process = subprocess.Popen(
        [sys.executable, "-m", "catalog.app", str(database), str(port)],
        cwd=MODULE,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    base = f"http://127.0.0.1:{port}"
    try:
        answering(process, base, "catalog")
        yield base
    finally:
        process.terminate()
        process.wait(timeout=10)


@pytest.fixture(scope="session")
def double(driver: Playwright) -> Iterator[APIRequestContext]:
    """The double, started from the contract document alone, and the client that calls it.

    No implementation of catalog is started here: D1's scenarios are about what a consumer
    can work against before one exists. Started by the command `README.md` documents, and by
    no other — the reason is the one above `serving`.
    """
    port = free_port()
    process = subprocess.Popen(
        [sys.executable, "src/contract_double.py", str(CONTRACT), str(port)],
        cwd=MODULE,
    )
    try:
        api = driver.request.new_context(base_url=f"http://127.0.0.1:{port}", timeout=10_000)
        deadline = datetime.now(UTC).timestamp() + READY
        while True:
            if process.poll() is not None:
                raise RuntimeError(f"the double exited with {process.returncode} before answering")
            try:
                api.get("/", timeout=1_000)
                break
            except Error:
                if datetime.now(UTC).timestamp() > deadline:
                    raise RuntimeError(f"the double did not answer within {READY:.0f}s") from None
        yield api
        api.dispose()
    finally:
        process.terminate()
        process.wait(timeout=10)


@pytest.fixture
def neighbourhood(tmp_path: Path) -> Iterator[str]:
    """A neighbourhood with nothing listed: a fresh SQLite file per scenario, so no scenario
    inherits what another published."""
    with serving(tmp_path / "catalog.sqlite3") as base:
        yield base


def listed_example(document: dict[str, Any]) -> dict[str, Any]:
    """The tools the contract's own `listTools` example describes — never a list written by
    hand here."""
    content = document["paths"]["/tools"]["get"]["responses"]["200"]["content"]
    return content[next(iter(content))]["example"]


@pytest.fixture(scope="session")
def listed_neighbourhood(document: dict[str, Any], tmp_path_factory) -> Iterator[str]:
    """`catalog` running, holding exactly what the contract's own examples describe.

    The producer contract test then meets both the `200` the document declares — the example
    identifier it carries is listed — and the `404` it declares for every other identifier.
    """
    database = tmp_path_factory.mktemp("listed") / "catalog.sqlite3"
    connection = open_store(database)
    for tool in listed_example(document)["tools"]:
        add(
            connection,
            Listing(tool["id"], tool["name"], tool["lender"], tool["approximateLocation"]),
        )
    connection.close()
    with serving(database) as base:
        yield base


@pytest.fixture(scope="session")
def browser(driver: Playwright) -> Iterator[Browser]:
    """The browser the charter's C2 fixes for `e2e`. Headless: CI has no screen, and the
    screenshots are the evidence, not a window."""
    started = driver.chromium.launch()
    try:
        yield started
    finally:
        started.close()


@pytest.fixture
def phone(browser: Browser) -> Iterator[Page]:
    """A phone: 375 pixels wide. The use happens in the garage or on the doorstep, and that
    constraint is about the software, so it survives the decision not to deploy (charter, C1)."""
    context = browser.new_context(viewport={"width": PHONE, "height": 812})
    page = context.new_page()
    try:
        yield page
    finally:
        context.close()


@pytest.fixture(scope="session")
def shot() -> Callable[[Page, str], Path]:
    """Takes one screenshot into `.evidence/`, and returns where it landed. The width is in
    the name because the width is what the scenario is about."""

    def take(page: Page, name: str) -> Path:
        EVIDENCE.mkdir(exist_ok=True)
        path = EVIDENCE / f"{name}-{PHONE}.png"
        page.screenshot(path=path, full_page=True)
        return path

    return take
