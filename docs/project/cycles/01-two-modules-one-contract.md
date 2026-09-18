---
goal: "Run one NapkinStack cycle end to end on two modules that meet only through a versioned contract, each delivering something a neighbour could see on a phone, each verified by a session that did not write it"
status: accepted           # proposed | accepted | closed | stopped — the decider accepts
appetite_weeks: 1         # the time the decider WANTS to spend, not an estimate
start: 2026-09-19         # YYYY-MM-DD
end: 2026-09-26           # start + appetite: the first day the cycle is over — the circuit breaker
deliverables:
  - id: D1
    title: "catalog-api v1: the versioned contract catalog provides, and a double built from it that a consumer can work against before any implementation exists"
    module: "catalog"
    state: ready
    acceptance:
      - "Given contracts/catalog-api/v1/openapi.yaml, when the e2e verb of catalog runs in CI, then the document is reported as a valid OpenAPI 3.1 document and the report is written to modules/catalog/.evidence/"
      - "Given no implementation of catalog, when the double built from the schema is started and every operation the contract declares is called with the examples the contract itself carries, then each answers with the status and the payload the contract declares, and the transcript is written to modules/catalog/.evidence/"
      - "Given the error cases the contract declares — a tool that does not exist, and a malformed request — when each is called against the double, then the status and the error shape are those the contract declares, and the transcript is written to modules/catalog/.evidence/"
  - id: D2
    title: "A neighbour publishes a tool on a phone and sees it in the neighbourhood list"
    module: "catalog"
    state: ready
    acceptance:
      - "Given a neighbourhood with no tool listed, when a neighbour opens the list at a 375-pixel-wide viewport, then the page says that no tool is listed yet and how to publish the first one, and the screenshot is written to modules/catalog/.evidence/"
      - "Given the test persona Amina at a 375-pixel-wide viewport, when she publishes a tool with its name and an approximate location, then the tool appears in the neighbourhood list, no exact address appears on the page or in any response, and the screenshots are written to modules/catalog/.evidence/"
      - "Given a publication form left incomplete, when the neighbour submits it, then the page names the field to correct, nothing is added to the list, and the screenshot is written to modules/catalog/.evidence/"
      - "Given catalog running, when the producer contract test calls every operation of contracts/catalog-api/v1/openapi.yaml against it, then each answers as the contract declares and the report is written to modules/catalog/.evidence/"
  - id: D3
    title: "A neighbour records a loan of a listed tool with its two dates, and records its return"
    module: "loans"
    state: proposed
    acceptance:
      - "Given the test persona Bruno at a 375-pixel-wide viewport and a tool listed in catalog, when he records a loan with a hand-over date and a return date, then the loan appears with both dates, the tool is shown as out on loan, and the screenshots are written to modules/loans/.evidence/"
      - "Given a loan recorded and the tool handed back, when the return is recorded, then the history shows who held the tool and between which dates, the tool is shown as available again, and the screenshots are written to modules/loans/.evidence/"
      - "Given a return date earlier than the hand-over date, when the neighbour submits the loan, then the page says what to correct, no loan is recorded, and the screenshot is written to modules/loans/.evidence/"
      - "Given catalog neither running nor installed, when the test and e2e verbs of loans run against the double built from contracts/catalog-api/v1/openapi.yaml alone, then both pass and the run is written to modules/loans/.evidence/"
# outcome: completed      # closed: completed | shipped — stopped: reframed | stopped
# ended_on: YYYY-MM-DD
---

# Cycle 01 — Two modules, one contract

> Copied to `NN-<slug>.md` at framing (`playbooks/framing.md`). One accepted cycle at a
> time; no automatic extension.

## Goal

The charter's only success criterion is observed at this cycle's closure. So this cycle is
not shaped by what the product most needs — the product is not being deployed — but by what
criterion A has to be able to watch: **two modules, owned separately, that know each other
only through a versioned contract, each delivering something a user could see, each
verified by someone who did not write it, and a decision recorded on or before 2026-09-26.**

The product is the material. Everything delivered here is real software, built under the
framework's rules, on an invented subject with test data only.

Three deliverables and one week is deliberately tight. The answer to a deliverable that
does not fit is the circuit breaker, not an extension — and the circuit breaker firing is
not a failure of criterion A (charter, *Success criteria*).

## Deliverables

**Before D1, and not deliverables themselves:** the two modules are created by the engine's
scaffolding, one pull request each, once this cycle is accepted —
`nstack new-module catalog NapkinStack/catalog standard --user-facing` and
`nstack new-module loans NapkinStack/loans standard --user-facing`. Creating a module is a
decision and carries its ADR (`modules/README.md`, `docs/os/02-modules.md` §3): the
capability covered, the boundary, the alternatives rejected. `catalog` is owned by
`NapkinStack/catalog`, `loans` by `NapkinStack/loans`; both `criticality: standard` and
`user_facing: true` (charter, C3).

**Order and dependencies:**

```
modules created  →  D1 (the contract + its double)  →  D2   (catalog)
                                                    →  D3   (loans)
```

**D1 comes first, and both other deliverables build on it, not on each other.**

**D3 is `proposed` until D1 is merged, and becomes `ready` then.** The reason matters more
than the rule: `loans` builds against **the contract and the double built from its schema**,
never against `catalog`'s implementation or its interface. **D3 must not wait for D2.**
Gating `loans` on `catalog`'s user-facing deliverable would contradict what this cycle
exists to demonstrate — that two modules know each other only through their contract — and
it would concentrate the risk: if D2 slips inside a one-week appetite, D3 would never start
and the two-team observation would be lost entirely. D2 and D3 proceed in parallel, neither
waiting on the other.

**Why D1's module is `catalog` and not `contracts`.** The contract document itself lives at
`contracts/catalog-api/v1/openapi.yaml`, hand-written, and `v1` is never edited — a breaking
change creates `v2` beside it (charter, C2). But the deliverable is `catalog`'s, for a
reason the repository decides rather than the framer: CI discovers modules under
`modules/` only (`.github/workflows/module-checks.yml`), so a pull request touching
`contracts/` alone runs no verb and produces no `.evidence/` artefact — and evidence from a
CI run is what the charter's C1 requires. The executable part of D1 — the validation of the
document, the double built from the schema, and the `e2e` verb that writes both transcripts
to `modules/catalog/.evidence/` — therefore lives in `catalog`, the module that **provides**
the contract. `catalog`'s manifest declares `catalog-api` v1 under `provides`; `loans`'
manifest declares it under `consumes`. The fitness functions compare those declarations with
the code.

`pr_scope.sh` counts modules under `modules/`, `services/`, `apps/` and `packages/` only, so
a pull request carrying both the contract document and `catalog`'s code counts as one
module and does not need the `cross-module` label.

**Every acceptance criterion above is satisfiable under the charter's C1**: each scenario is
`automated` or `explored`, none is `human only`, and each names the evidence the `e2e` run
writes to `.evidence/`. The criteria are fixed at acceptance: changing one afterwards is a
re-framing, recorded as such, never an edit to this file.

## Out of scope

Not done in this cycle, even if time remains.

- **The photographed state at hand-over and at return.** The discovery calls it what makes
  this a lending product rather than a list, and it is the heaviest part of the product. It
  does not fit a one-week appetite; the scope is cut rather than the appetite stretched
  (`playbooks/framing.md` §2.5). It is in *Later*, first in line.
- **The optional value on a listing.** The no-go is that the field must never exist without
  the consequence of C. civ. art. 1880 beside it. The cheapest way to honour it in one week
  is for the field not to exist at all. In *Later*, with its explanation.
- **Accounts, login and authentication.** A neighbour is a name typed on a form, against
  test data. This is what keeps `playbooks/security.md` out of the first cycle; it applies
  in full the moment identity or a real person's data enters.
- **Search, filtering, sorting, notifications and any message between neighbours.** One
  list, one form.
- **Anything that would deploy.** No hosting, no domain, no `release` verb, no neighbourhood
  opened, no household approached.
- **Everything the charter puts out of scope**, in particular the eleven no-gos.

## Later

Candidates for the next framing, in the order the discovery argues for them:

1. **The state at hand-over and at return**, photographed and timestamped — the product's
   signature feature, and the one the discovery's usability risk is about.
2. **The optional value, with the consequence of art. 1880 shown beside it.**
3. **What the lender is told**: C. civ. art. 1891 — a defect known and not disclosed puts
   the harm on them — and art. 1888, which makes the agreed term binding on them. The
   discovery's flaw 9: a candour that omits the half affecting the person supplying the tool
   is not candour.
4. **A usable route to report a listing**, built whatever the DSA's remuneration gate turns
   out to mean (charter, C5).
5. **Deletion, retention, and what the history is for.** The discovery's flaw 13: a deletion
   request from one party lands inside the record the other party depends on — most acutely
   when the tool has not come back. It is a design decision, not only a duty to implement.
6. **Accounts and identity**, and with them `playbooks/security.md` from that cycle's first
   day.
7. **A cost figure for one neighbourhood for a year.** The discovery's flaw 2: the one
   constraint said to be load-bearing was never priced. It was not kept as a spike here
   because the decider kept none; it stays worth an hour.

## Open questions

**Blocking:** none.

**Not blocking:**

1. The charter's open question 12 — whether the operator publishes a contact and answers a
   deletion request — stays open and does not bear on this cycle: nothing is deployed and
   only test data exists.

## Closure

<Written at the end: what was delivered, which success criteria moved, what was deferred,
where the next framing starts.>
