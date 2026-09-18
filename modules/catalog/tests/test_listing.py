"""The rules a listing has to satisfy, tested where they live.

A pure business rule is a unit test, not an end-to-end scenario (`playbooks/tests.md` §1):
the page covers the journey, this covers the edges the journey never walks.
"""

import pytest

from catalog.listing import FIELDS, incomplete, published

WHOLE = {"lender": "Amina", "name": "Hammer drill", "approximate_location": "Rue des Lilas"}


@pytest.mark.parametrize("missing", list(FIELDS))
def test_every_field_is_needed_and_the_missing_one_is_named(missing: str) -> None:
    correct = incomplete({**WHOLE, missing: ""})
    assert correct is not None, f"{missing} left empty was accepted"
    assert correct[0] == missing
    assert FIELDS[missing][0] in correct[1], "the message must name the field, not the column"


def test_a_value_of_nothing_but_spaces_is_not_a_value() -> None:
    assert incomplete({**WHOLE, "name": "   \t "}) is not None


def test_a_value_longer_than_the_contract_declares_is_refused() -> None:
    limit = FIELDS["approximate_location"][1]
    correct = incomplete({**WHOLE, "approximate_location": "x" * (limit + 1)})
    assert correct is not None, "the answer would be longer than catalog-api v1 declares"
    assert str(limit) in correct[1], "the message must say what the bound is"


def test_a_whole_form_is_published_with_its_own_identifier_and_nothing_trimmed_away() -> None:
    assert incomplete(WHOLE) is None
    listing = published({field: f"  {value}  " for field, value in WHOLE.items()})
    assert listing.as_declared() == {
        "id": listing.id,
        "name": "Hammer drill",
        "lender": "Amina",
        "approximateLocation": "Rue des Lilas",
    }
    assert published(WHOLE).id != listing.id, "two listings must not share an identifier"
