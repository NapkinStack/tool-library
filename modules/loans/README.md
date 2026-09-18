# loans

Who holds a listed tool, from the day it is handed over to the day it comes back.

- **Owner**: NapkinStack/loans
- **Criticality**: standard
- **Manifest**: [MANIFEST.yaml](./MANIFEST.yaml)

## Getting started

```bash
nstack check loans          # ruff: format and lint, under 2 min
nstack test loans           # pytest; never starts another module
```

`uv` is the only prerequisite. Both commands resolve their own tools, so a fresh clone
needs no bootstrap step.

## Contracts

Nothing is consumed yet. `catalog-api v1` arrives with deliverable D1 of cycle 1; this
module declares it in `consumes` in the pull request that first reads it, because a
dependency declared and never used is itself a violation (B4).

This module reads the catalogue **only** through that contract and through a double built
from its schema. It never imports `catalog` and never reads `catalog`'s data. Deliverable
D3's last acceptance criterion is exactly that property: `loans` passes with `catalog`
neither running nor installed.

## Decisions

See [`docs/adr/0001-two-modules-meeting-through-one-contract.md`](../../docs/adr/0001-two-modules-meeting-through-one-contract.md)
for why this module exists and where its boundary is.
