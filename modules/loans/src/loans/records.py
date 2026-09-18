"""The loans this module owns: which tool, held by whom, between which dates.

SQLite, one file, owned here and read by nobody else (charter C2;
`docs/os/08-quality.md` §8). The tool's name is copied into the record on purpose: the
history has to stay readable when a listing is withdrawn from the catalogue, and asking
`catalog` what a returned tool was called would be a dependency the history does not need.
"""

from __future__ import annotations

import os
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import date
from pathlib import Path

DEFAULT_STORE = Path(__file__).resolve().parents[2] / ".data" / "loans.sqlite3"
SCHEMA = """
CREATE TABLE IF NOT EXISTS loans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tool_id     TEXT    NOT NULL,
    tool_name   TEXT    NOT NULL,
    holder      TEXT    NOT NULL,
    handed_over TEXT    NOT NULL,
    back_on     TEXT    NOT NULL,
    returned    INTEGER NOT NULL DEFAULT 0
)
"""


class Refused(ValueError):
    """What the neighbour has to correct. Its text is what the page shows them."""


@dataclass(frozen=True)
class Loan:
    id: int
    tool_id: str
    tool_name: str
    holder: str
    handed_over: date
    back_on: date
    returned: bool


def _a_date(value: str, which: str) -> date:
    try:
        return date.fromisoformat(value.strip())
    except ValueError as malformed:
        raise Refused(f"Give the {which} date as a date, for example 2026-09-21.") from malformed


class Loans:
    """Every loan recorded in this neighbourhood, and nothing about what is listed."""

    def __init__(self, store: Path | str | None = None) -> None:
        self._store = str(store or os.environ.get("LOANS_DB") or DEFAULT_STORE)
        Path(self._store).parent.mkdir(parents=True, exist_ok=True)
        with self._open() as connection:
            connection.execute(SCHEMA)

    @contextmanager
    def _open(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self._store)
        connection.row_factory = sqlite3.Row
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def record(
        self, *, tool_id: str, tool_name: str, holder: str, handed_over: str, back_on: str
    ) -> Loan:
        """A loan, or the refusal that says what to correct. Nothing in between is stored."""
        holder = holder.strip()
        if not holder:
            raise Refused("Say who is taking the tool: the history is a name and two dates.")
        leaves = _a_date(handed_over, "hand-over")
        comes_back = _a_date(back_on, "return")
        if comes_back < leaves:
            raise Refused(
                "The return date is before the hand-over date. Correct the dates: "
                "a tool cannot come back before it leaves."
            )
        with self._open() as connection:
            cursor = connection.execute(
                "INSERT INTO loans (tool_id, tool_name, holder, handed_over, back_on) "
                "VALUES (?, ?, ?, ?, ?)",
                (tool_id, tool_name, holder, leaves.isoformat(), comes_back.isoformat()),
            )
        return Loan(int(cursor.lastrowid), tool_id, tool_name, holder, leaves, comes_back, False)

    def record_return(self, loan_id: int) -> None:
        """The tool is back. A loan is not finished until this is recorded (charter)."""
        with self._open() as connection:
            connection.execute("UPDATE loans SET returned = 1 WHERE id = ?", (loan_id,))

    def recorded(self) -> list[Loan]:
        """The history: who held what, between which dates, most recent first."""
        with self._open() as connection:
            rows = connection.execute("SELECT * FROM loans ORDER BY id DESC").fetchall()
        return [
            Loan(
                row["id"],
                row["tool_id"],
                row["tool_name"],
                row["holder"],
                date.fromisoformat(row["handed_over"]),
                date.fromisoformat(row["back_on"]),
                bool(row["returned"]),
            )
            for row in rows
        ]

    def out_on_loan(self) -> dict[str, Loan]:
        """The tools that have not come back, by tool identifier."""
        return {loan.tool_id: loan for loan in reversed(self.recorded()) if not loan.returned}
