"""D2's first three acceptance criteria, end to end (cycle 1).

One test per criterion, in the order of the test sheet, driven in a browser at the
375-pixel-wide viewport the discovery's platform constraint is about. Each writes its
screenshot to `.evidence/` before it asserts, so a failure is documented rather than silent.

Amina is an invented persona and every place below is invented test data (charter, C4).
Nothing here reaches a real person.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path
from typing import Any

from playwright.sync_api import Page, expect

AMINA = {
    "Your name": "Amina",
    "The tool": "Hammer drill",
    "Roughly where it is": "Rue des Lilas, near the bakery",
}

# What an exact address looks like where this product would be used: a number in front of a
# street, or a postcode. The no-go is the charter's, and the invariant is this module's.
ADDRESS = re.compile(
    r"\b\d+\s*(?:bis|ter)?\s*,?\s*(?:rue|avenue|av\.|boulevard|bd|all[eé]e|impasse|chemin"
    r"|place|quai|route|square)\b|\b\d{5}\b",
    re.IGNORECASE,
)


def fill(page: Page, typed: dict[str, str]) -> None:
    for label, value in typed.items():
        page.get_by_label(label).fill(value)


def declared_properties(document: dict[str, Any]) -> set[str]:
    """The properties the contract's `Tool` declares — never a list written by hand here."""
    return set(document["components"]["schemas"]["Tool"]["properties"])


def test_an_empty_neighbourhood_says_how_to_publish_the_first_tool(
    neighbourhood: str, phone: Page, shot: Callable[[Page, str], Path]
) -> None:
    """S1 — the empty state: the one every neighbour sees first (`playbooks/ux.md`)."""
    phone.goto(neighbourhood)
    written = shot(phone, "empty-neighbourhood")
    expect(phone.get_by_role("status")).to_contain_text("No tool is listed yet")
    expect(phone.get_by_role("button", name="Publish it")).to_be_visible()
    for label in AMINA:
        expect(phone.get_by_label(label)).to_be_visible()
    assert written.is_file(), f"the screenshot was not written to {written}"


def test_amina_publishes_a_tool_and_sees_it_in_the_neighbourhood_list(
    neighbourhood: str,
    document: dict[str, Any],
    phone: Page,
    shot: Callable[[Page, str], Path],
) -> None:
    """S2 — the nominal state, and the no-go that holds on the page and in every response."""
    phone.goto(neighbourhood)
    fill(phone, AMINA)
    shot(phone, "publishing")
    phone.get_by_role("button", name="Publish it").click()
    expect(phone.get_by_role("listitem")).to_have_count(1)
    written = shot(phone, "published")

    listed = phone.get_by_role("listitem").first
    expect(listed).to_contain_text("Hammer drill")
    expect(listed).to_contain_text("Amina")
    expect(listed).to_contain_text("Rue des Lilas, near the bakery")

    tools = phone.request.get(f"{neighbourhood}/tools").json()["tools"]
    assert len(tools) == 1, f"the contract's list answers {tools}"
    assert set(tools[0]) == declared_properties(document), (
        f"the answer carries {sorted(tools[0])}, the contract declares "
        f"{sorted(declared_properties(document))}"
    )
    one = phone.request.get(f"{neighbourhood}/tools/{tools[0]['id']}")
    assert one.json() == tools[0], "the tool read on its own differs from the one in the list"

    for what, text in (("the page", phone.content()), ("a response", one.text())):
        found = ADDRESS.search(text)
        assert not found, f"an exact address appears in {what}: {found.group(0)!r}"
    assert written.is_file(), f"the screenshot was not written to {written}"


def test_an_incomplete_form_names_the_field_and_lists_nothing(
    neighbourhood: str, phone: Page, shot: Callable[[Page, str], Path]
) -> None:
    """S3 — the recoverable error state: what to correct, and what was typed kept."""
    phone.goto(neighbourhood)
    fill(phone, {"Your name": "Amina", "The tool": "Hammer drill"})  # where it is, left empty
    phone.get_by_role("button", name="Publish it").click()
    expect(phone.get_by_role("alert")).to_be_visible()
    written = shot(phone, "incomplete-form")

    expect(phone.get_by_role("alert")).to_contain_text("Roughly where it is")
    expect(phone.get_by_label("The tool")).to_have_value("Hammer drill")
    expect(phone.get_by_label("Your name")).to_have_value("Amina")
    expect(phone.get_by_role("listitem")).to_have_count(0)
    assert phone.request.get(f"{neighbourhood}/tools").json() == {"tools": []}, (
        "the contract's list is not empty after a form that was refused"
    )
    assert written.is_file(), f"the screenshot was not written to {written}"
