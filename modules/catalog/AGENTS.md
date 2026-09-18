# catalog — local instructions

> Only what is **specific to this module**.
> Never duplicate a kernel rule (`/AGENTS.md`): that is wasted context and a source of
> divergence.

## Responsibility

Holds the tools a neighbour is willing to lend in their neighbourhood.

## What this module does not do

- **It does not know who has a tool right now.** A loan, its two dates and its history
  belong to `loans`. If you need to show that a tool is out, `loans` says so; `catalog`
  never stores it.
- **It does not decide what another module may read.** That is the contract's job, and the
  contract is a document, not a consequence of this package.

## Internal conventions nobody could guess

- **The contract is hand-written and is never generated from this package** (charter,
  constraint C2). A contract derived from the producer's classes couples every consumer to
  the producer's internals, and the coupling only shows up when the producer is refactored.
- **`commands` name `src tests` rather than `.`** A tool pointed at the folder also walks
  whatever a workstation leaves in it, and fails for reasons that have nothing to do with
  the code.
- **`provides` declares `catalog-api` v1 since D1**, in the pull request that created the
  document. The manifest is the declared graph; it must never promise what the real graph
  does not have — and `v1` is never edited once merged, a breaking change creating `v2`.

- **`contract_double` answers from the contract document and from nothing else.** No tool,
  no listing, no store: the example the document carries for the operation asked, its
  declared `404` for an identifier the document does not carry, its declared `400` for what
  its schemas reject. Adding domain behaviour to it would make it a second implementation
  of `catalog`, agreeing with the first by construction instead of by contract — which is
  exactly what a double exists to prevent. What it needs is in the document.

- **The `e2e` scenarios read the document themselves**, and never through
  `contract_double`: an oracle sharing its reader with what it judges goes green on a bug
  they hold in common. The duplication between the two is deliberate.
- **`user_facing` is raised by the deliverable that puts a page in front of a neighbour**,
  in that same pull request — D2 for this module. It is `false` while nothing is visible,
  because the manifest describes what is. Do not raise it in advance and do not forget it:
  from the moment it is `true`, every pull request touching this module carries a test
  sheet, and no later pull request can lower it back.

## Business invariants

- **A tool's location is approximate, never an exact address.** It is shown to neighbours
  who have not met the lender yet. Nothing in a response carries a precise address.
- **Every actor in a test is an invented persona, in test data only.** Nothing in this
  project reaches a real person (charter, no-go).

## Known traps

Nothing recorded yet. The first entry belongs to whoever hits it, with the test that would
have caught it.

## Non-standard commands

None. Everything runs through the MANIFEST's verbs.
