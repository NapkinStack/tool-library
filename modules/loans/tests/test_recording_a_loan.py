"""The invariants of a loan, at the level that actually verifies them.

A loan has two dates and the second is never before the first; the history says who held
the tool and between which dates. Every neighbour below is an invented persona
(charter, C4).
"""

from __future__ import annotations

from datetime import date

import pytest

from loans.records import Loans, Refused

DRILL = ("9f1c6f6a-5f1e-4e2a-9a1e-6a1b0c2d3e4f", "Hammer drill")


@pytest.fixture
def loans(tmp_path) -> Loans:
    return Loans(tmp_path / "loans.sqlite3")


def a_loan(loans: Loans, handed_over: str = "2026-09-21", back_on: str = "2026-09-24"):
    return loans.record(
        tool_id=DRILL[0],
        tool_name=DRILL[1],
        holder="Bruno",
        handed_over=handed_over,
        back_on=back_on,
    )


def test_a_recorded_loan_keeps_both_dates_and_the_name_of_who_holds_the_tool(
    loans: Loans,
) -> None:
    recorded = a_loan(loans)

    assert recorded.holder == "Bruno"
    assert recorded.handed_over == date(2026, 9, 21)
    assert recorded.back_on == date(2026, 9, 24)
    assert loans.out_on_loan() == {DRILL[0]: recorded}


def test_a_loan_handed_over_and_back_on_the_same_day_is_recorded(loans: Loans) -> None:
    recorded = a_loan(loans, handed_over="2026-09-21", back_on="2026-09-21")

    assert recorded.handed_over == recorded.back_on


def test_a_return_date_before_the_hand_over_is_refused_and_nothing_is_recorded(
    loans: Loans,
) -> None:
    with pytest.raises(Refused) as refused:
        a_loan(loans, handed_over="2026-09-24", back_on="2026-09-21")

    assert "before the hand-over date" in str(refused.value)
    assert loans.recorded() == []


def test_a_loan_with_nobody_holding_the_tool_is_refused(loans: Loans) -> None:
    with pytest.raises(Refused):
        loans.record(
            tool_id=DRILL[0],
            tool_name=DRILL[1],
            holder="   ",
            handed_over="2026-09-21",
            back_on="2026-09-24",
        )

    assert loans.recorded() == []


def test_a_date_that_is_not_one_is_refused(loans: Loans) -> None:
    with pytest.raises(Refused):
        a_loan(loans, back_on="next tuesday")

    assert loans.recorded() == []


def test_once_the_return_is_recorded_the_tool_is_free_and_the_history_keeps_the_dates(
    loans: Loans,
) -> None:
    recorded = a_loan(loans)

    loans.record_return(recorded.id)

    assert loans.out_on_loan() == {}
    history = loans.recorded()
    assert [
        (loan.holder, loan.tool_name, loan.handed_over, loan.back_on, loan.returned)
        for loan in history
    ] == [("Bruno", "Hammer drill", date(2026, 9, 21), date(2026, 9, 24), True)]


def test_the_history_survives_a_new_reader_of_the_same_store(tmp_path) -> None:
    a_loan(Loans(tmp_path / "loans.sqlite3"))

    assert len(Loans(tmp_path / "loans.sqlite3").recorded()) == 1
