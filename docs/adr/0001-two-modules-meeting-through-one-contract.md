# ADR-0001 — Split the domain into `catalog` and `loans`, meeting through one contract

- **Status**: Accepted
- **Date**: 2026-09-18
- **Decision makers**: @napkinstack-admin (decider, charter)
- **Scope**: project
- **Reversibility**: costly — merging two modules later is cheap; splitting a module that
  has grown into one is not

---

## Context

The charter was accepted on 2026-09-18 and cycle 1 runs from 2026-09-19 to 2026-09-26. The
project builds real software on an invented subject, with test data only and no
deployment: what it measures is whether a full NapkinStack cycle runs end to end and
whether its barriers hold (charter, *Success criteria*).

That purpose puts a requirement on the architecture that the product alone would not: the
cycle has to show **two modules, owned by different teams, that know each other only
through a versioned contract**. A single module would deliver the same software and
demonstrate nothing.

## Problem

Where does the boundary go, so that two teams can work in parallel without waiting on each
other, and so that the separation is real rather than declared?

## Constraints

- Two owners exist and are separate: `NapkinStack/catalog` and `NapkinStack/loans`.
- One week of appetite, three deliverables. A boundary that needs long negotiation does not
  fit.
- `loans` must be able to start before `catalog` has an implementation: deliverable D3 is
  gated on D1, the contract, and not on D2, the producer's interface (cycle 1,
  *Deliverables*).
- No deployment and no real user, so the boundary cannot be justified by scaling or by
  operational independence. It has to be justified by the domain.

---

## Prior art

**Dominant convention of the field:** a lending system separates *what exists* from *who
has it right now*. This is not a recent idea and not an opinion — it is how library systems
have been built for forty years, and how commerce systems separate inventory from orders.

**References examined:**

| Reference | What it does | Applicable here? |
|---|---|---|
| Koha, the integrated library system | Separates *Cataloguing* — the record of an item — from *Circulation* — checkouts, due dates, returns. They are distinct modules with distinct permissions | Directly. `catalog` is cataloguing, `loans` is circulation, and the same reason applies: an item's description changes for different reasons, and at a different rate, than the record of who holds it |
| Evergreen ILS | The same split, reached independently: bibliographic records on one side, circulation on the other | Confirms the convention is the field's answer rather than one product's choice |
| Domain-Driven Design (Evans), bounded contexts | A boundary follows the language: when two groups use the same word for different things, they belong to different contexts | Applicable: "a tool" means *a listed thing* in `catalog` and *the object of a loan, with two dates* in `loans` |

**Why the convention is not enough:** it is enough. This decision adopts it, and the only
thing added is a NapkinStack requirement — that the boundary be crossed by a versioned
contract document rather than by a shared library or a shared database
(`docs/os/03-contracts.md`).

---

## Options considered

### Option 1 — One module, `library`
- Description: tools and loans in one module, one owner.
- Advantages: no contract to write, no coordination, the fastest way to working software.
- Drawbacks: demonstrates nothing the project exists to measure. Two teams cannot work in
  parallel, and the cycle's goal is unreachable.
- Cost of getting out: high — splitting a module whose code has grown across the boundary
  is the expensive direction.

### Option 2 — `catalog` and `loans`, meeting through `catalog-api v1` *(chosen)*
- Description: `catalog` owns what is listed; `loans` owns who holds what, and between which
  dates. `loans` reads the catalogue through a hand-written contract and never imports the
  producer.
- Advantages: the boundary follows the domain and the field's convention; the two teams can
  start in parallel as soon as the contract exists; the separation is testable, not stated.
- Drawbacks: a contract to write and to version before any interface exists; one more
  document to keep true.
- Cost of getting out: low. Merging two modules is cheap.

### Option 3 — Do nothing, decide at the first conflict
- Description: start in one module and split when it hurts.
- Drawbacks: the cycle ends on 2026-09-26. "When it hurts" arrives after the measurement,
  so the project would close having observed nothing about parallel teams.

---

## Decision

**Option 2.** The argument that settles it is not that two modules are better than one — for
this software, one would do. It is that the boundary chosen is the one the field already
draws, so the split is not an artefact of the exercise: *what a tool is* and *who has it
between which dates* change for different reasons, at different rates, and are read by
different people. A boundary drawn anywhere else would have to be defended; this one is
inherited.

The second half of the decision is the one NapkinStack adds: the boundary is crossed by
`contracts/catalog-api/v1/openapi.yaml`, **hand-written**, never generated from the
producer's classes. A generated contract is a projection of the producer's internals, and
every consumer becomes coupled to them without anyone deciding it — the failure appears
only at the first refactor.

`provides` stays empty in `catalog`'s manifest until that document exists. The manifest is
the declared graph and must never promise what the real graph does not have.

---

## Success criterion

> We will consider this was the right call if, **before 2026-09-26**, `loans`' `test` and
> `e2e` verbs pass with **`catalog` neither running nor installed**, against the double
> built from the contract's schema alone.

That is already deliverable D3's last acceptance criterion, so the ADR is checked by the
cycle rather than by an intention. If it cannot be met, the boundary is not real and the
honest conclusion is one module, not two.

What we do if it is not: supersede this ADR and merge the modules. The direction that costs
little.

---

## Consequences

**Positive:** two owners can work at the same time from the day the contract lands; the
isolation is expressed as a test rather than as a rule; the vocabulary of each module is
free to diverge, which is the point of the boundary.

**Negative and accepted debt:** a contract document to maintain by hand, and a double to
keep in step with it. Cheap at one contract; it is the second and third that would need a
generator, and that is a decision for later.

**Impacts on other modules or contracts:** none. These are the project's first two modules
and its first contract.

**Rule to automate:** the fitness functions already carry it — `B1` refuses a reference to a
module absent from `consumes`, `B2` refuses importing another module's implementation, and
`B5` refuses reading another module's data. Nothing new has to be written: the decision is
enforced by checks that already exist, which is why it can be trusted after this session
ends.

---

## Rejected alternatives

- **A shared database with two schemas.** Refused by `docs/os/03-contracts.md`: a contract
  is the only channel between modules, and a shared store makes the boundary invisible to
  every check.
- **A shared Python package for the tool model.** The same coupling as a generated
  contract, arriving by another route: the two modules would agree by construction rather
  than by agreement, and the first divergence would be a merge conflict instead of a
  version.
- **Three modules, adding `neighbourhood`.** Refused on `docs/os/02-modules.md` §3: one
  module is often enough to start, and nothing in cycle 1 needs a third owner.
