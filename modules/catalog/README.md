# catalog

The tools a neighbour is willing to lend in their neighbourhood.

- **Owner**: NapkinStack/catalog
- **Criticality**: standard, user-facing
- **Manifest**: [MANIFEST.yaml](./MANIFEST.yaml)

## Getting started

```bash
nstack check catalog        # ruff: format and lint, under 2 min
nstack test catalog         # pytest; never starts another module
nstack e2e catalog          # the contract validated, then called against its double
```

`uv` is the only prerequisite. All three commands resolve their own tools, so a fresh clone
needs no bootstrap step. `e2e` writes its report and its transcripts to `.evidence/`, which
CI uploads: that is the evidence a test sheet links to (charter, C1).

## Contracts

**Provided: `catalog-api` v1**, at
[`contracts/catalog-api/v1/openapi.yaml`](../../contracts/catalog-api/v1/openapi.yaml) —
hand-written, never generated from this package (charter, C2). `v1` is never edited once
merged; a breaking change creates `v2` beside it.

A consumer does not wait for an implementation: the document is servable on its own.

```bash
cd modules/catalog
uv run --group e2e python -m contract_double ../../contracts/catalog-api/v1/openapi.yaml 8000
```

`contract_double` holds no `catalog` behaviour and nothing about tools: it answers each
request from the document — the declared example for the operation asked, the declared
`404` for an identifier the document does not carry, the declared `400` for what its
schemas reject. Point it at another OpenAPI document and it serves that one.

## Decisions

See [`docs/adr/0001-two-modules-meeting-through-one-contract.md`](../../docs/adr/0001-two-modules-meeting-through-one-contract.md)
for why this module exists and where its boundary is.
