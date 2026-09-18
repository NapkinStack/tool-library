"""What D1's scenarios need: the contract document, the double that serves it, and the
folder the evidence is written to.

The scenarios read the document themselves rather than through `contract_double`: an
oracle that shares its reader with the thing it judges goes green on a bug they hold in
common.
"""

from __future__ import annotations

import json
import socket
import subprocess
import sys
from collections.abc import Callable, Iterator
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest
import yaml
from playwright.sync_api import APIRequestContext, Error, sync_playwright

MODULE = Path(__file__).resolve().parents[1]
CONTRACT = MODULE.parents[1] / "contracts" / "catalog-api" / "v1" / "openapi.yaml"
EVIDENCE = MODULE / ".evidence"
READY = 20.0  # seconds allowed for the double to accept its first request


@pytest.fixture(scope="session")
def contract() -> Path:
    return CONTRACT


@pytest.fixture(scope="session")
def document() -> dict[str, Any]:
    return yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))


@pytest.fixture
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
def double() -> Iterator[APIRequestContext]:
    """The double, started from the contract document alone, and the client that calls it.

    No implementation of catalog exists, and none is started here. Started by the command
    `README.md` documents, and by no other: a documented way to start it that nothing runs
    is a way that stops working unnoticed — which is exactly what happened at D1's review.
    Readiness is waited for on the observable event — the first answer — never on a
    duration (`playbooks/tests.md`).
    """
    with socket.socket() as free:
        free.bind(("127.0.0.1", 0))
        port = free.getsockname()[1]
    process = subprocess.Popen(
        [sys.executable, "src/contract_double.py", str(CONTRACT), str(port)],
        cwd=MODULE,
    )
    try:
        with sync_playwright() as driver:
            api = driver.request.new_context(base_url=f"http://127.0.0.1:{port}", timeout=10_000)
            deadline = datetime.now(UTC).timestamp() + READY
            while True:
                if process.poll() is not None:
                    raise RuntimeError(
                        f"the double exited with {process.returncode} before answering"
                    )
                try:
                    api.get("/", timeout=1_000)
                    break
                except Error:
                    if datetime.now(UTC).timestamp() > deadline:
                        raise RuntimeError(
                            f"the double did not answer within {READY:.0f}s"
                        ) from None
            yield api
            api.dispose()
    finally:
        process.terminate()
        process.wait(timeout=10)
