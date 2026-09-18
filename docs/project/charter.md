---
status: accepted               # proposed | accepted — the decider accepts
decider: "@napkinstack-admin" # the human who validates the charter and the cycles
success_criteria:             # when the goal is reached: measurable, dated or relative to a named event
  - "At the closure of cycle 1: a full NapkinStack cycle ran end to end — a charter accepted, one cycle accepted with an appetite and an end date, two modules created with owners and manifests, a versioned contract provided by one and consumed by the other, every accepted deliverable's test sheet run by a verifier who is not its author with its evidence attached, a closure decision recorded on or before the end date, and nstack fitness green on main throughout"
---

# Charter — tool-library

> Written once, at the first framing (`playbooks/framing.md`), copied to `charter.md`;
> changed only through a PDR. Every agent session reads it.

This project is an **acknowledged rehearsal**. The software is built for real, under the
framework's own rules; the market is not entered. The source is
`docs/project/discovery.md`, decided **go** by @napkinstack-admin on 2026-09-18, in their
words: *"go — an acknowledged rehearsal, criterion A only"*. That go authorises this
charter and one bounded cycle. It authorises no deployment.

---

## Users and their problem

**Held as an assumption, knowingly, and not tested by this project.**

- **Who** — people living in one neighbourhood in France, on two sides at once: the one who
  owns a tool and is willing to lend it, and the one who needs it for an afternoon. Nobody
  is only a borrower or only a lender by design.
- **How many** — unknown. No count exists for a first neighbourhood, and the discovery
  found no figure for how many households own a tool they would lend. The supply side is
  unmeasured.
- **The problem, as the decider reads it** — the tool is often already a few doors away and
  unused, but nobody knows which garage it is in; asking around reaches only the neighbours
  one already talks to, so the neighbour buys or rents instead.

**No user has been interviewed, and none will be.** The discovery records the decider's
answer in round 1: *"none. The problem is the decider's own reading, not a user's words"*,
and their refusal to interview three neighbours before the first cycle. The evidence
gathered neither confirms nor refutes the problem: willingness is high, refusal is high,
and nothing found measures the gap between *would ask a neighbour I know* and *would ask a
stranger two streets away* — which is exactly the gap the product claims to close.

This is the single largest thing the project does not know, and it stays that way. Since
nothing is deployed, no neighbour is reached, so the assumption is neither confirmed nor
tested here. **It is carried, not resolved.** A later project that seeks users starts by
resolving it, not by inheriting it.

---

## Success criteria

**One criterion, and it is about the framework, not the product.** The discovery separated
two criteria and then withdrew the second:

| Criterion | What it measures | Status |
|---|---|---|
| **A — the framework** | Did a full NapkinStack development cycle run properly, end to end | **The only criterion of this project** |
| **B — the product** | Twenty loans made and returned in one neighbourhood at three months, half of them second loans | **Withdrawn**, discovery §6 reason 2 — dropped, not deferred |

B is gone because the decider refused to arrange the ending the challenger predicted:
*"A declared, B never measured"*. The twenty loans, the second-loan share and the third
refutation condition are no longer success criteria of this project. The value hypothesis
stays in `docs/project/discovery.md` §4 as what was believed at round 1 and what the
evidence says of it. **It is not being tested here**, and nothing in this charter rests on
it being true.

**How criterion A is observed.** At the **closure of cycle 1** — a named event, the cycle
file reaching `status: closed` or `status: stopped` with its `outcome` and `ended_on`
recorded. What must be observable at that moment is in the front matter above.

**How it is missed.** Three ways, and only three:

1. the end date passes with **no decision recorded** on or before it;
2. a barrier is **bypassed** — a `skip`, a `--no-verify`, a disabled check, a test
   weakened to make a sheet go green, a ruleset bypass used;
3. a deliverable is **closed without its evidence**.

**The circuit breaker firing is not a miss.** A cycle that reaches its end date and is
stopped by a recorded decision is a barrier holding, observed — which is the thing this
project exists to watch. The miss is silence past the end date, never the content of the
decision. Counting an honest stop as a failure would recreate the pressure the cycle's end
date exists to remove.

---

## Constraints

### C1 — What counts as a verified deliverable

**This is the constraint the whole project turns on.** The discovery removed the criterion
that would have produced evidence from real use. Without the rule below, a cycle can close
green while proving only that the paperwork moved. Every deliverable's acceptance criteria
must be satisfiable under it, or the cycle is not framed.

> A deliverable of this project is **verified** when, and only when, all four hold.
>
> **1. The sheet is the criteria.** Its acceptance criteria, written *given · when · then*,
> are transcribed as the test sheet in its pull request, and every scenario carries a
> result and evidence tied to the pull request's head commit.
>
> **2. The verifier is a separate session, and nothing is `human only`.** The sheet is run
> by an agent session in the verifier posture that did not write the change and does not
> fix it. Because this project reaches no real user, **no scenario may be of kind
> `human only`**: a criterion only a real user could confirm is not an acceptance criterion
> of this project and goes to *Out of scope* rather than into a sheet. This ban holds
> while nothing is deployed; **the day anything is deployed it lifts, by ADR.**
>
> **3. The evidence is machine-produced and re-runnable.** For an `automated` scenario: the
> CI run of the module's `e2e` verb and the artefact CI uploads from
> `modules/<module>/.evidence/`. For an `explored` scenario: a screenshot produced by that
> same `e2e` run and uploaded from `.evidence/` — **never a screenshot pasted by hand into
> the pull request**, which is the one point where *machine-produced* leaks back into
> *asserted*. The actor in every *given* is a named test persona, in test data only.
>
> **4. The criteria are fixed at acceptance.** A deliverable's acceptance criteria are
> those the decider accepted with the cycle. Changing them afterwards is a **re-framing**,
> recorded as such, never an edit to the cycle file. A sheet that passes because its
> criteria were softened is not a pass.

Clause 4 is what stops clause 1 being circular: *the sheet is the criteria* means something
only if the criteria cannot move. Otherwise the author or the verifier can lower the bar
until the sheet goes green, and every clause above it becomes decoration.

*Sources: `docs/os/05-workflow.md` §7 and §10; `playbooks/verification.md`;
`docs/os/09-platform.md` §2; `.github/workflows/module-checks.yml`, which already runs
`nstack e2e` and uploads `.evidence/`; enforced in part by `nstack pr-check`, rules T1 to
T5. Decided by @napkinstack-admin, 2026-09-18.*

One genuine user-facing bar survives the removal of the market: the discovery's platform
constraint — *"it must work on a phone: the use happens in the garage or on the doorstep"*
— is about the **software**, not about users, so it holds, and it is verified by driving
the page at a phone viewport.

### C2 — The stack

Recorded here because the project's `docs/tooling-profile.md` is updated in its own pull
request, outside this framing. The Prior Art Gate was applied
(`docs/os/06-decisions.md` §2): every row below is the field's convention, and none of them
is a deviation that needs paying for.

| Capability | Tool | Why |
|---|---|---|
| Language and runner | Python 3.13, managed by `uv` | `uv` is already the project's only prerequisite, and `astral-sh/setup-uv` is the single third-party action the repository allows: a Python stack needs no action that is not already permitted |
| Web surface | FastAPI + Jinja2, server-rendered HTML | One phone-first page. No build step, no bundler, no second app store |
| Data owned by a module | SQLite, one file per module | Each domain owns its data (`docs/os/08-quality.md` §8): nothing shared, nothing to host |
| `check` | ruff — format and lint | Under two minutes, the field's default |
| `test` | pytest | The field's default. A module's `test` never starts another module (`docs/os/09-platform.md` §2) |
| `e2e` | Playwright for Python, trace and screenshots written to `modules/<m>/.evidence/` | The established browser driver. It is what makes C1's evidence machine-produced rather than asserted, and what lets a scenario run at a phone viewport |
| Contract format | OpenAPI 3.1, hand-written | The convention for a versioned HTTP contract |
| Contract tests | Schemathesis on the producer side; a schema-built double on the consumer side | Both directions, as `docs/os/03-contracts.md` §5 requires |

Three precisions, decided with the stack and binding:

1. **The contract lives at `contracts/catalog-api/v1/openapi.yaml`, hand-written.** A
   breaking change creates `v2` beside `v1`; **`v1` is never edited.** It is not generated
   from FastAPI's models — a contract generated from the producer's internal classes is the
   first anti-pattern of `docs/os/03-contracts.md` §7.
2. **`loans` never imports `catalog`.** In tests it uses only the double built from the
   schema. This is the one property that makes the two-team observation worth anything.
3. **Playwright installs its browser as a package, not as an action**, so the
   organisation's allowed-actions policy is untouched. The download is budgeted in CI time
   and is **never a reason to skip `e2e`**.

### C3 — Criticality of the modules

`catalog` and `loans` are both declared **`criticality: standard`** and
**`user_facing: true`**.

`standard` because nothing is deployed and only test data exists, so the personal-data
trigger does not fire in this cycle. `user_facing: true` because it is what makes the test
sheet mandatory on their pull requests (`nstack pr-check`, T1) — the barrier criterion A is
measuring.

**The trigger is recorded with the decision: the day anything is deployed, both modules go
to `high`, by ADR.**

### C4 — The operator, the money, the time, the platform

Carried from the discovery, unchanged:

| Constraint | What it is | What it implies |
|---|---|---|
| Who runs it | The decider, personally | One person. No support rota, no out-of-hours answer |
| Budget | *"Close to nothing"* | No paid hosting, no paid moderation, no paid insurance. **No cost figure appears anywhere in the discovery** — the one constraint said to be load-bearing was never priced |
| Time | *"A few hours a week"* | A cycle must be small enough to finish in that |
| Platform | *"It must work on a phone: the use happens in the garage or on the doorstep"* | Phone-first, one web page |
| Money | Free to start; a paid model stays possible later | Nothing may assume a payment rail, nothing should make one impossible |
| Data | **Test data only.** An invented subject, no real person's contact | Stated in this repository's `README.md`, and what keeps C3 at `standard` |

### C5 — Law, carried as fact and not as argument

These are the discovery's factual corrections, accepted by the decision. They are recorded
as facts a later session must not re-derive, not as positions to argue:

- **The DSA's gate is remuneration, not size.** Article 3(a) defines an information society
  service by reference to Directive (EU) 2015/1535 art. 1(1)(b), *"normally provided for
  remuneration"*. The discovery's stage 2 stated that art. 16 applies to every hosting
  provider whatever its size; that is wrong on the threshold. **A reporting route is built
  anyway** — the correction removes a claimed certainty, not the duty of care.
- **The lender's liability exists and was missing.** C. civ. art. 1891: a lender who knew
  of a defect and did not disclose it answers for the harm it causes. Art. 1888: the agreed
  term binds the lender, who cannot take the thing back early. The product's signature
  feature — a declared, photographed state at hand-over — is written evidence of what the
  lender knew.
- **The borrower's liability, already recorded.** C. civ. art. 1880, and a thing valued at
  the time of the loan puts the loss on the borrower even by force majeure unless otherwise
  agreed.
- **"Below *à titre professionnel*" is an unsourced inference**, not a finding. Nothing
  sourced supports it, and the discovery's own research says a neighbourhood association
  running such a service may well be in scope of art. L111-7.
- **The only behavioural figure in the discovery is American** — YouGov, 35 878 US adults.
  The French sources measure goodwill and rental prices, not borrowing behaviour.
- **Mutum resolves against the idea** — liquidated at the end of 2017 with 113 000 objects
  listed, in France, on the money-free model. The discovery left it open as an assumption;
  it is now a finding.
- **The discovery's research missed France.** `entrevoisins.eu`, the same product, free and
  in French, already shipped; Smiile's domain for sale after 500 000 neighbours. The
  stopping rule was met and the question was not answered. Recorded as the finding it is.

---

## Risks

The **product** risks are accepted as true and do not block, because nothing is deployed.
They are not re-argued here and they are not softened: the pre-mortem's ten endings and the
eleven counter-evidence rows of `docs/project/discovery.md` §5 stand as written. Every one
of them is an ending of a *deployed* product with users. **They would block a product that
sought users. This one seeks none.** A later project that decides to deploy inherits them
whole, starting with `entrevoisins.eu` and the French base rate for the money-free model.

The risks **this** project carries are different, and they are about the rehearsal:

| Risk | What it would look like | What answers it |
|---|---|---|
| **The rehearsal proves only that the paperwork moved** | Three deliverables accepted, three green sheets, and nothing that would have caught a real defect | C1, in full. Machine-produced evidence, a separate verifier, criteria fixed at acceptance |
| **The contract is decorative** | Two modules split for the rehearsal rather than by the domain, coupled in fact and separated only on paper | The isolation property of C2.2 is itself an acceptance criterion: `loans`' tests pass with `catalog` absent |
| **One week is not enough** | The end date arrives with a deliverable unfinished | The circuit breaker, not an extension. It firing is not a failure of criterion A |
| **An agent verifies an agent** | The verifier session shares the author's blind spot and the sheet goes green on a misunderstanding they hold in common | `docs/os/07-governance.md` §7: an agent's approval does not count toward merging. The human decider approves, and notes what the verifier missed — that measurement is part of what criterion A produces |
| **The problem is an assumption and stays one** | Software built well for a need nobody confirmed | Accepted, and named. It is a defect of the discovery that this framing inherits rather than repairs — and it costs nothing here, because nothing is deployed |

**Criticality implied: `standard`** for both modules (C3). Nothing in this project moves
money, acts on someone's behalf, or holds a real person's data.

**Harm.** No user can be harmed by this project, since none is reached. The only exposed
surface is a public repository: test data only, no real person's contact, and no secret —
ever — in the repository.

---

## Vocabulary

| Term | Meaning |
|---|---|
| **Neighbour** | A person in the neighbourhood, on either side of a loan. Nobody is a lender or a borrower by design |
| **Tool** | The object lent. Listed by the neighbour who owns it |
| **Listing** | A tool published as available to lend. A listing is not a loan |
| **Loan** | A tool handed from one neighbour to another, with a hand-over date and a return date agreed between them. In French law, a *prêt à usage* — C. civ. arts. 1875 to 1891 |
| **Hand-over** | The moment the tool leaves the lender |
| **Return** | The moment it comes back. A loan is not finished until it is recorded |
| **History** | The record of who held what, and between which dates. The product's only output in a dispute |
| **Neighbourhood** | One place, opened by anyone, with no invitation. **None is opened by this project** |
| **`catalog`** | The module that owns tools and listings, and **provides** `catalog-api` |
| **`loans`** | The module that owns loans and their history, and **consumes** `catalog-api` |
| **Rehearsal** | This project. The software is built for real, under the framework's rules; the market is not entered |
| **Verified** | Constraint C1, in full. Not a synonym for "the tests pass" |
| **Test persona** | An invented neighbour in test data. The actor in every acceptance criterion. No real person |

---

## Out of scope

**The eleventh no-go overrides the ten others where they overlap.** Its wording is settled
here, as the decision asked the framing to settle it:

> **No deployment to a real user.** No neighbourhood opened, no household approached,
> nothing shipped. This replaces — it does not merely subsume — the framer no-go *"no
> second neighbourhood counted as success before the first reaches twenty returned loans"*,
> which lost its measure when criterion B was withdrawn.

The ten no-gos of the discovery stand:

*Given by the decider:*

- **No payment, no commission, no membership.** The service does not live off the exchange.
  Not permanent: a paid model stays open for later.
- **No arbitration.** The product records and never judges who is right.
- **No delivery and no logistics.** The two neighbours hand the tool over themselves.
- **No gatekeeping of who may open a neighbourhood.** No invitation, no vouching.

*Proposed by the framer at round 1, kept by the decider, theirs now:*

- **No insurance, no guarantee and no deposit handled by the product** — said in plain
  words at the moment of the loan, not buried in terms.
- **No exact address in public.** An approximate location until both neighbours have agreed
  on the loan.
- **No value shown without its consequence shown.** The field must not exist without the
  explanation of C. civ. art. 1880 beside it.
- **No reputation score on a person.** A record of loans, yes; a public rating attached to
  a named neighbour, no.
- **No native mobile application in the first cycle.** One phone-first web page.
- (The sixth is replaced by the eleventh, above.)

And what this project deliberately does not do:

- **It does not measure criterion B**, and does not keep it for later. It is withdrawn.
- **It does not test the value hypothesis.** No neighbour is asked anything.
- **It runs no spike.** All four of the challenger's tests need real neighbours or a real
  deployment; keeping one would create a deliverable this project could not close honestly.
  **The pricing exercise included** — so the budget constraint stays unpriced, knowingly.
- **It does not enter the market.** `entrevoisins.eu` already ships this product, free, in
  French. That removes the reason to deploy. It does not remove the reason to build, which
  is the framework's cycle, not the product's originality.

---

## Open questions

**Blocking:** none.

**Not blocking:**

1. **Open question 12, carried from the discovery** — *"As the controller under the GDPR
   you have to be reachable and to answer a deletion request. Are you willing to publish a
   contact and answer one?"* It stays open: it concerns the operator, not the market.
   Nothing in cycle 1 depends on the answer, because nothing is deployed and only test data
   exists. **It becomes blocking on the day anything is deployed**, together with the
   reporting route of C5 and the conflict between a clear history and the right to erasure
   that the discovery recorded and did not resolve.

*(Open questions 10 and 11 — which neighbourhood is first, and how many tools must be
listed before the count starts — fell with criterion B and are not carried.)*
