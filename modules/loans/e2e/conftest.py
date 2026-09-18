"""D3's scenarios, driven in a browser at the width a doorstep has.

Everything runs inside this module: `loans`' own page, served here, and the double built
from `contracts/catalog-api/v1/openapi.yaml`. `catalog` is neither imported, installed nor
started — D3's fourth criterion, asserted in `test_record_a_loan.py`.

The evidence lands in `modules/loans/.evidence/`, which CI uploads
(`.github/workflows/module-checks.yml`): that is what makes the test sheet's results
machine-produced rather than asserted (charter, C1.3).
"""

from __future__ import annotations

import json
import socket
import subprocess
import threading
import time
from pathlib import Path

import pytest
import uvicorn
from playwright.sync_api import sync_playwright

from loans.web import create_app

MODULE = Path(__file__).resolve().parents[1]
EVIDENCE = MODULE / ".evidence"
HOST = "127.0.0.1"
PHONE = {"width": 375, "height": 812}  # the doorstep, not the development machine
STARTUP_SECONDS = 15


def _free_port() -> int:
    with socket.socket() as probe:
        probe.bind((HOST, 0))
        return probe.getsockname()[1]


def _head() -> str:
    found = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=MODULE, capture_output=True, text=True, check=False
    )
    return found.stdout.strip() or "unknown"


@pytest.fixture(scope="session")
def evidence() -> Path:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    for stale in [
        *EVIDENCE.glob("s?-*.png"),
        EVIDENCE / "isolation.json",
        EVIDENCE / "e2e-run.json",
    ]:
        stale.unlink(missing_ok=True)
    return EVIDENCE


@pytest.fixture(scope="session")
def browser():
    with sync_playwright() as driver:
        started = driver.chromium.launch()
        yield started
        started.close()


@pytest.fixture
def page(browser):
    context = browser.new_context(viewport=PHONE)
    opened = context.new_page()
    yield opened
    context.close()


@pytest.fixture
def neighbourhood(tmp_path, monkeypatch) -> str:
    """The page, served on a store of its own, reading the catalogue through the double."""
    monkeypatch.setenv("LOANS_DB", str(tmp_path / "loans.sqlite3"))
    monkeypatch.delenv("CATALOG_BASE_URL", raising=False)
    port = _free_port()
    server = uvicorn.Server(uvicorn.Config(create_app(), host=HOST, port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    deadline = time.monotonic() + STARTUP_SECONDS
    while not server.started:  # an observable state, never a fixed wait
        if not thread.is_alive() or time.monotonic() > deadline:
            raise RuntimeError("the loans page did not start")
        time.sleep(0.02)
    yield f"http://{HOST}:{port}"
    server.should_exit = True
    thread.join(timeout=STARTUP_SECONDS)


@pytest.fixture
def shot(evidence: Path):
    """Takes the screenshot a scenario names as its evidence."""

    def take(page, name: str) -> None:
        page.screenshot(path=str(evidence / name), full_page=True)

    return take


def pytest_sessionfinish(session, exitstatus) -> None:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    record = {
        "verb": "e2e",
        "module": "loans",
        "viewport": PHONE,
        "commit": _head(),
        "collected": session.testscollected,
        "failed": session.testsfailed,
        "exit_status": int(exitstatus),
        "screenshots": sorted(path.name for path in EVIDENCE.glob("s?-*.png")),
    }
    (EVIDENCE / "e2e-run.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
