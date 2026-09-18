"""What a listing is, and what makes one incomplete.

The rules are the contract's own (`contracts/catalog-api/v1/openapi.yaml`): three fields,
each required, each bounded. They live here rather than in the page or in the store so that
one rule answers the form and the API at once, and so that they can be tested without either.

The bounds are not decoration: a value longer than the contract declares would be an answer
`catalog` promised never to give.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

# The form's field -> what the neighbour is asked, the contract's bound, and what the page
# says under it. The order is the order the page asks in, and the order a correction is
# named in.
FIELDS: dict[str, tuple[str, int, str]] = {
    "lender": ("Your name", 80, "The neighbours will see it beside the tool."),
    "name": ("The tool", 120, "What it is, in your words — a hammer drill, an extension ladder."),
    "approximate_location": (
        "Roughly where it is",
        120,
        "A street or a landmark. Never your exact address: the two of you agree on the rest "
        "between yourselves.",
    ),
}


@dataclass(frozen=True)
class Listing:
    """One tool a neighbour is willing to lend. It holds nothing else — no value, no rating,
    no way to reach anyone, and no exact address (charter, no-gos)."""

    id: str
    name: str
    lender: str
    approximate_location: str

    def as_declared(self) -> dict[str, str]:
        """The shape `catalog-api` v1 declares, and nothing beside it."""
        return {
            "id": self.id,
            "name": self.name,
            "lender": self.lender,
            "approximateLocation": self.approximate_location,
        }


def incomplete(typed: dict[str, str]) -> tuple[str, str] | None:
    """The first field to correct and what to say about it, or None when nothing is missing.

    One field at a time, in the order the page asks: a correction a neighbour can act on
    without reading a list (`playbooks/ux.md`).
    """
    for field, (label, limit, _) in FIELDS.items():
        value = typed.get(field, "").strip()
        if not value:
            return field, f"{label}: this one is needed before the tool can be listed."
        if len(value) > limit:
            return field, f"{label}: {limit} characters at most, and {len(value)} were typed."
    return None


def published(typed: dict[str, str]) -> Listing:
    """The listing a complete form describes. Called once `incomplete` has said nothing."""
    values = {field: typed[field].strip() for field in FIELDS}
    return Listing(id=str(uuid.uuid4()), **values)
