# catalog

The tools a neighbour is willing to lend in their neighbourhood.

- **Owner**: NapkinStack/catalog
- **Criticality**: standard, user-facing
- **Manifest**: [MANIFEST.yaml](./MANIFEST.yaml)

## Getting started

```bash
nstack check catalog        # ruff: format and lint, under 2 min
nstack test catalog         # pytest; never starts another module
```

`uv` is the only prerequisite. Both commands resolve their own tools, so a fresh clone
needs no bootstrap step.

## Contracts

Nothing is provided yet. `catalog-api v1` arrives with deliverable D1 of cycle 1, at
`contracts/catalog-api/v1/openapi.yaml`, hand-written and never generated from this
package (charter, constraint C2). It is declared in `provides` in the same pull request
that creates it, so the declared graph never promises what the real one does not have.

## Decisions

See [`docs/adr/0001-two-modules-meeting-through-one-contract.md`](../../docs/adr/0001-two-modules-meeting-through-one-contract.md)
for why this module exists and where its boundary is.
