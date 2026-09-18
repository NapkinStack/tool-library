# loans

Who holds a listed tool, from the day it is handed over to the day it comes back.

- **Owner**: NapkinStack/loans
- **Criticality**: standard
- **Manifest**: [MANIFEST.yaml](./MANIFEST.yaml)

## Getting started

```bash
nstack check loans          # ruff: format and lint, under 2 min
nstack test loans           # pytest; never starts another module
nstack e2e   loans          # the scenarios, in a browser at a 375-pixel-wide viewport
```

`uv` is the only prerequisite. Every command resolves its own tools, so a fresh clone
needs no bootstrap step; `e2e` also installs its browser as a package, never as an action
(charter, C2.3). `e2e` starts the page itself and leaves its evidence in `.evidence/`,
which CI uploads — that is what the test sheets link to.

## The page

One page, phone first, because the use happens in a garage or on a doorstep: what is
listed and who holds it, one form to record a loan with its two dates, and the history of
who held what and between which dates. A return date before the hand-over date is refused
— the page says what to correct, keeps what was typed, and records nothing.

The loans are this module's own data: SQLite, one file, at `LOANS_DB` (by default
`.data/loans.sqlite3`, never committed). Nobody else reads it.

## Contracts

This module consumes **`catalog-api v1`**, and knows the catalogue through nothing else.

| Where | What it is |
|---|---|
| `contracts/catalog-api/v1/openapi.yaml` | the contract, hand-written, never edited once merged |
| `src/loans/contract.py` | the one place that reads the document |
| `src/loans/catalogue_double.py` | the double, **built from that document**: the tools it serves and the problems it answers are the document's own examples |
| `src/loans/catalogue.py` | the consumer side: the four fields the contract declares, and no fifth |

It never imports `catalog`, never starts it and never reads its data — and the double
built here is this module's own: sharing one double between the two sides would prove that
the shared code works, not that the contract is sufficient.

`tests/test_the_catalogue_through_its_contract.py` is the consumer-side contract test
(`docs/os/03-contracts.md` §5): every answer is validated against the contract's schemas.
Deliverable D3's last acceptance criterion is the isolation itself — `loans` passes with
`catalog` neither running nor installed — and `e2e/test_record_a_loan.py` asserts it, with
`.evidence/isolation.json` as its record.

**A note on the fitness functions.** `nstack boundaries` looks for another module's name in
an import line, so it warns (`B4`) that the declared dependency on `catalog` is unused. It
is used, by the only route a contract may be used by: a document read at
`src/loans/contract.py`. A consumer that imports nothing of its producer is exactly what
ADR-0001 asks for, and it is invisible to a detector calibrated for imports.

## Decisions

See [`docs/adr/0001-two-modules-meeting-through-one-contract.md`](../../docs/adr/0001-two-modules-meeting-through-one-contract.md)
for why this module exists and where its boundary is.
