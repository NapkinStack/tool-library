# catalog

The tools a neighbour is willing to lend in their neighbourhood.

- **Owner**: NapkinStack/catalog
- **Criticality**: standard, user-facing
- **Manifest**: [MANIFEST.yaml](./MANIFEST.yaml)

## Getting started

```bash
nstack bootstrap catalog    # downloads Playwright's browser; once per clone
nstack check catalog        # ruff: format and lint, under 2 min
nstack test catalog         # pytest; never starts another module
nstack e2e catalog          # the contract, the double, and the page driven on a phone
nstack run catalog          # the page, on http://127.0.0.1:8000
```

`uv` is the only prerequisite; every command resolves its own tools. **`bootstrap` is no
longer optional**: since D2 the scenarios drive a browser, and Playwright installs it as a
package rather than as a CI action (charter, C2). `e2e` writes its reports, its transcripts
and its screenshots to `.evidence/`, which CI uploads: that is the evidence a test sheet
links to (charter, C1).

## The page

One server-rendered page, read at 375 pixels wide because the use happens in the garage or
on the doorstep (charter, C1). It lists what the neighbourhood lends and carries the form
that publishes a tool: your name, the tool, and roughly where it is — **never an exact
address**, which is a no-go of the charter and an invariant of this module.

```bash
cd modules/catalog
PYTHONPATH=src uv run python -m catalog.app [database] [port]
```

This is the command the `run` verb and the scenarios both use, so it is checked on every run
rather than only written down. Without arguments it writes `modules/catalog/catalog.sqlite3`
and listens on 8000. The file is this module's own data and is never committed; delete it to
get an empty neighbourhood back.

`PYTHONPATH=src` is not decoration — see *Known traps* in [AGENTS.md](./AGENTS.md).

## Contracts

**Provided: `catalog-api` v1**, at
[`contracts/catalog-api/v1/openapi.yaml`](../../contracts/catalog-api/v1/openapi.yaml) —
hand-written, never generated from this package (charter, C2). `v1` is never edited once
merged; a breaking change creates `v2` beside it.

A consumer does not wait for an implementation: the document is servable on its own. Since
D2 the module answers that contract itself, and `e2e/test_producer_contract.py` is what says
so — Schemathesis calls every operation the document declares against the running module
(`docs/os/03-contracts.md` §5, the producer side). The page is **not** in the contract:
publishing is something a neighbour does, not something another module does.

```bash
cd modules/catalog
uv run --group e2e python src/contract_double.py ../../contracts/catalog-api/v1/openapi.yaml 8000
```

This is the command the `e2e` scenarios use to start it, so it is checked on every run
rather than only written down.

`contract_double` holds no `catalog` behaviour and nothing about tools: it answers each
request from the document — the declared example for the operation asked, the declared
`404` for an identifier the document does not carry, the declared `400` for what its
schemas reject, and a `501` for a response the document declares without an example.

**What it does not do.** A parameter value is validated as the raw string it arrives as,
with no coercion. A document declaring a parameter of any type other than `string` gets
that operation's declared `400` — even for the example the document itself carries. That is
a wrong answer rather than a `501`, and nothing detects it. `catalog-api v1` declares one
path parameter and it is a string; another document needs the coercion built first.

## Decisions

See [`docs/adr/0001-two-modules-meeting-through-one-contract.md`](../../docs/adr/0001-two-modules-meeting-through-one-contract.md)
for why this module exists and where its boundary is.

<!-- Probe P1: this pull request deliberately touches two modules. -->
