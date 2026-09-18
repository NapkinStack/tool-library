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
- **`consumes` stays empty until the contract exists.** A dependency declared and never
  used is a violation in its own right (B4).
- **`user_facing` is raised by the deliverable that puts a page in front of a neighbour**,
  in that same pull request — D3 for this module. It is `false` while nothing is visible,
  because the manifest describes what is. From the moment it is `true`, every pull request
  touching this module carries a test sheet, and no later pull request can lower it back.
- **`commands` name `src tests` rather than `.`** A tool pointed at a folder also walks
  whatever a workstation leaves in it.

## Business invariants

- **A loan has two dates, and the second is never before the first.** A return recorded
  before the hand-over is refused, not stored and corrected later.
- **The history says who held the tool and between which dates.** It is what replaces trust
  between neighbours who have not met; losing it is worse than losing the loan itself.
- **Every actor in a test is an invented persona, in test data only.** Nothing in this
  project reaches a real person (charter, no-go).

## Known traps

Nothing recorded yet. The first entry belongs to whoever hits it, with the test that would
have caught it.

## Non-standard commands

None. Everything runs through the MANIFEST's verbs.
