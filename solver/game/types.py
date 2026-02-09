from __future__ import annotations

from typing import Iterable, Protocol, Tuple


class GameState(Protocol):
    def current_player(self) -> int:
        ...

    def is_terminal(self) -> bool:
        ...

    def utility(self, player: int) -> float:
        ...

    def legal_actions(self) -> Iterable[str]:
        ...

    def next_state(self, action: str) -> "GameState":
        ...

    def information_set_key(self, player: int) -> str:
        ...

    def is_chance(self) -> bool:
        ...

    def chance_outcomes(self) -> Iterable[Tuple[str, float]]:
        ...
