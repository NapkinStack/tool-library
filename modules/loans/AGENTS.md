# loans — local instructions

> Only what is **specific to this module**.
> Never duplicate a kernel rule (`/AGENTS.md`): that is wasted context and a source of
> divergence.

## Responsibility

Records who holds a listed tool, from the day it is handed over to the day it comes back.

## What this module does not do

- **It does not hold the catalogue.** What a tool is, who lends it and roughly where belong
  to `catalog`. This module refers to a tool by what the contract exposes, never by reading
  the other module's store.
- **It does not decide what the catalogue publishes.** That is the contract's job.

## Internal conventions nobody could guess

- **`catalog` is reached only through `contracts/catalog-api/v1/openapi.yaml`**, and in
  tests only through a double built from that schema. Importing `catalog`, or reading its
  data, is refused by B2 and B5 — and it would destroy the only property cycle 1 exists to
  demonstrate.
- **`consumes` declares `catalog-api v1`, and the contract is read as a document.**
  `src/loans/contract.py` is the only place that opens
  `contracts/catalog-api/v1/openapi.yaml`; `src/loans/catalogue_double.py` builds the
  double from it. Nothing here imports `catalog`, which is why `nstack boundaries` warns
  `B4` ("no use detected"): its detection looks for the other module's name in an import
  line, and a consumer that imports nothing of its producer is exactly what ADR-0001 asks
  for. Do not silence the warning by inventing an import.
- **`user_facing` is `true` since D3** — the deliverable that put the page in front of a
  neighbour raised it in its own pull request. Every pull request touching this module now
  carries a test sheet, and none can lower the flag back.
- **`commands` name `src tests e2e` rather than `.`** A tool pointed at a folder also
  walks whatever a workstation leaves in it.

## Business invariants

- **A loan has two dates, and the second is never before the first.** A return recorded
  before the hand-over is refused, not stored and corrected later.
- **The history says who held the tool and between which dates.** It is what replaces trust
  between neighbours who have not met; losing it is worse than losing the loan itself.
- **Every actor in a test is an invented persona, in test data only.** Nothing in this
  project reaches a real person (charter, no-go).

## Known traps

- **`--locked` says nothing about `uv run --with`.** A package given with `--with` is
  resolved in a layer of its own, outside `uv.lock`, and what it pulls in floats from one run
  to the next with no refusal. A package a verb needs goes in a dependency group of
  `pyproject.toml`, then `uv lock`, and the verb runs `--group <name>`. A pin changed without
  `uv lock` is refused by every verb that runs `uv run`, and `uv` names the fix — not by
  `check`, which runs ruff through `uvx` and never reads the lock.
- **`test` and `e2e` run `--exact`.** Without it `uv run` installs what is missing
  and never removes an extraneous package, so in CI, where the verbs share one environment, a
  verb would pass on a package only another group brings, and fail on a workstation that runs
  it first.
- **`.python-version` holds the charter's Python, 3.13 (C2).** `requires-python` only sets a
  floor: without the pin, a runner whose own Python is below it gets the newest one `uv` can
  download — CI ran 3.14.7 while workstations ran 3.13.
- **`httpx.ASGITransport` is asynchronous only.** It is what lets this module speak real
  HTTP to the double without opening a port, and it is why `Catalogue` and the page's
  routes are `async`. A synchronous `httpx.Client` fails on it at construction, not at the
  first call, so the symptom is an `AttributeError` about `__enter__`.
- **Playwright's synchronous API keeps an event loop running in the test's thread**, so
  `asyncio.run(...)` inside an `e2e` test raises *cannot be called from a running event
  loop*. Run the coroutine on a thread of its own — `what_the_double_answers()` in
  `e2e/test_record_a_loan.py`.
- **FastAPI cannot build a response model from a union of responses.** A handler that
  answers either a page or a redirect is annotated `-> Response`, not
  `-> HTMLResponse | RedirectResponse`, which fails at application creation.

## Non-standard commands

None. Everything runs through the MANIFEST's verbs.
