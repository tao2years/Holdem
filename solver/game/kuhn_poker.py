from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple

from solver.game.types import GameState


CARDS = ("J", "Q", "K")
CARD_RANK = {"J": 0, "Q": 1, "K": 2}


@dataclass(frozen=True)
class KuhnState(GameState):
    cards: Tuple[str, str] | None
    history: str

    def is_chance(self) -> bool:
        return self.cards is None

    def chance_outcomes(self) -> Iterable[Tuple[str, float]]:
        deals: List[Tuple[str, float]] = []
        total = 0
        for i in range(len(CARDS)):
            for j in range(len(CARDS)):
                if i == j:
                    continue
                total += 1
                deals.append((CARDS[i] + CARDS[j], 0.0))
        prob = 1.0 / total
        return [(deal, prob) for deal, _ in deals]

    def current_player(self) -> int:
        if self.is_chance():
            return -1
        return len(self.history) % 2

    def is_terminal(self) -> bool:
        return self.history in ("cc", "bc", "bf", "cbc", "cbf")

    def utility(self, player: int) -> float:
        if not self.is_terminal():
            raise ValueError("Utility requested for non-terminal state.")

        assert self.cards is not None
        card0, card1 = self.cards
        winner = 0 if CARD_RANK[card0] > CARD_RANK[card1] else 1

        if self.history in ("cc",):
            payoff = 1
        elif self.history in ("bc", "cbc"):
            payoff = 2
        elif self.history == "bf":
            return 1 if player == 0 else -1
        elif self.history == "cbf":
            return -1 if player == 0 else 1
        else:
            raise ValueError("Unknown terminal history.")

        return payoff if player == winner else -payoff

    def legal_actions(self) -> Iterable[str]:
        if self.is_terminal() or self.is_chance():
            return []

        if self.history in ("", "c"):
            return ["c", "b"]
        if self.history in ("b", "cb"):
            return ["c", "f"]
        raise ValueError(f"Illegal history: {self.history}")

    def next_state(self, action: str) -> "KuhnState":
        if self.is_chance():
            if len(action) != 2:
                raise ValueError("Chance action must be a two-card string.")
            return KuhnState(cards=(action[0], action[1]), history="")
        return KuhnState(cards=self.cards, history=self.history + action)

    def information_set_key(self, player: int) -> str:
        if self.cards is None:
            return "chance"
        return f"{self.cards[player]}:{self.history}"


def initial_state() -> KuhnState:
    return KuhnState(cards=None, history="")
