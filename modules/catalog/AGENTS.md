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
- **`user_facing` is `true` since D2**, the deliverable that put a page in front of a
  neighbour, raised in that same pull request. Every pull request touching this module
  beyond its description now carries a test sheet, and no later one can lower the flag back:
  T1 reads the stricter of base and head.

- **The page is not in the contract, and must not become one.** `catalog-api` v1 declares
  two read operations, which is how another module knows this one. Publishing is something a
  neighbour does on `catalog`'s own page — `GET /` and `POST /` — and a consumer that started
  depending on it would be depending on something nothing promised. A write another module
  needs is a contract change, additive, in its own pull request.

- **The page and the contract answer from the same store and the same rules.** The three
  fields, their bounds and the correction a neighbour reads all live in `listing.py`; the
  page and the API each render what it says. A rule copied into the template would drift from
  the one the contract is tested against.

## Business invariants

- **A tool's location is approximate, never an exact address.** It is shown to neighbours
  who have not met the lender yet. Nothing in a response carries a precise address: there is
  no field for one, the page says so under the field a neighbour types into, and D2's second
  scenario reads the page and every response looking for one. **The field is free text, so
  the module does not refuse an address a neighbour types in anyway** — that guard is not a
  criterion of cycle 1 and adding it would be behaviour no sheet verifies. Reported with D2.
- **Every actor in a test is an invented persona, in test data only.** Nothing in this
  project reaches a real person (charter, no-go).

## Known traps

- **`--locked` says nothing about `uv run --with`.** A package given with `--with` is
  resolved in a layer of its own, outside `uv.lock`, and what it pulls in floats from one run
  to the next with no refusal. A package a verb needs goes in a dependency group of
  `pyproject.toml`, then `uv lock`, and the verb runs `--group <name>`. A pin changed without
  `uv lock` is refused by every verb, and `uv` names the fix.
- **`.python-version` holds the charter's Python, 3.13 (C2).** Without it `uv` takes the
  newest interpreter it finds or downloads: CI ran 3.14 while workstations ran 3.13.

- **`src/` is not on `sys.path` under `uv run`.** This `pyproject.toml` declares no
  `[build-system]`, so uv treats the project as non-packaged and never installs it:
  `python -m contract_double` fails with *No module named contract_double*, while `pytest`
  works because `pythonpath = ["src"]` covers it alone. Found at D1's review, in a README
  command nothing ran. Caught now by the scenarios, which start the double with the command
  `README.md` documents and no other. The page is started the same way, with `PYTHONPATH=src`
  in front — which is why the `run` verb carries it.

- **`bootstrap` stopped being optional at D2.** The scenarios drive a browser, and Playwright
  downloads it once per clone. `nstack e2e catalog` on a fresh clone fails with Playwright's
  own *Executable doesn't exist* until `nstack bootstrap catalog` has run. The browser's
  system libraries are the runner image's, not this module's: `--with-deps` is deliberately
  not used, because it needs `sudo` and would make the verb unrunnable on a workstation.

- **`pytest` is 9 here, and that is Schemathesis's constraint.** `schemathesis` 4 requires
  `pytest>=9,<10`. Both the `test` and `e2e` environments moved together so the module runs
  one pytest; pinning an older Schemathesis to keep pytest 8 would have been the more
  expensive half of the same choice.

- **`contract_double` does not coerce a parameter's type.** A value is validated as the raw
  string it arrives as, so a document declaring a parameter of any type but `string` gets
  that operation's declared `400`, for its own example included — a wrong answer, not a
  `501`. `catalog-api v1` declares one string parameter, coercion was deliberately not
  built at D1's review, and the scenario that would catch it is not written because it
  would be red by design. Build the coercion before pointing the double at such a document.

## Non-standard commands

None. Everything runs through the MANIFEST's verbs.
