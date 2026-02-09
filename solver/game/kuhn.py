"""Kuhn Poker: a minimal imperfect-information game for CFR validation."""

from __future__ import annotations

from typing import Iterable, List

CARDS: List[int] = [1, 2, 3]


def get_actions(history: str) -> Iterable[str]:
    if history in ("", "p"):
        return ("p", "b")
    if history in ("b", "pb"):
        return ("f", "c")
    return ()


def is_terminal(history: str) -> bool:
    if history in ("pp",):
        return True
    return history.endswith("f") or history.endswith("c")


def utility(history: str, cards: List[int]) -> int:
    """Return payoff for player 0."""
    card_p0, card_p1 = cards[0], cards[1]

    if history == "pp":
        return 1 if card_p0 > card_p1 else -1

    if history.endswith("f"):
        # The bettor wins +1 net.
        return 1 if history in ("bf",) else -1

    if history.endswith("c"):
        return 2 if card_p0 > card_p1 else -2

    raise ValueError(f"Non-terminal history: {history}")
