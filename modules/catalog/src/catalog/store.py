"""Where the listings are kept: one SQLite file, owned by this module (charter, C2).

Nobody reads this file but `catalog`. Another module goes through `catalog-api` v1, which is
the whole point of the boundary (ADR-0001). Who holds a tool right now, and between which
dates, is not here either: `loans` owns that.
"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from catalog.listing import Listing

SCHEMA = """
create table if not exists listings (
    id                   text primary key,
    name                 text not null,
    lender               text not null,
    approximate_location text not null,
    listed_at            text not null default (datetime('now'))
)
"""


def open_store(database: Path) -> sqlite3.Connection:
    """The file, created if it is not there yet. A neighbourhood starts with nothing listed."""
    database.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(database, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    with connection:
        connection.execute(SCHEMA)
    return connection


def add(connection: sqlite3.Connection, listing: Listing) -> None:
    with connection:
        connection.execute(
            "insert into listings (id, name, lender, approximate_location) values (?, ?, ?, ?)",
            (listing.id, listing.name, listing.lender, listing.approximate_location),
        )


def _listing(row: sqlite3.Row) -> Listing:
    return Listing(row["id"], row["name"], row["lender"], row["approximate_location"])


def listed(connection: sqlite3.Connection) -> list[Listing]:
    """Everything listed, the most recently published first: what a neighbour opening the
    page is most likely to be looking for."""
    rows = connection.execute("select * from listings order by listed_at desc, rowid desc")
    return [_listing(row) for row in rows]


def one(connection: sqlite3.Connection, identifier: str) -> Listing | None:
    row = connection.execute("select * from listings where id = ?", (identifier,)).fetchone()
    return _listing(row) if row else None
