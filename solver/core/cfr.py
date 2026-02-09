"""Counterfactual Regret Minimization (CFR) - minimal implementation."""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import permutations
from typing import Dict, Iterable, List, Tuple

from solver.game import kuhn


@dataclass
class InfoSet:
    actions: Tuple[str, ...]
    regret_sum: Dict[str, float] = field(default_factory=dict)
    strategy_sum: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.regret_sum:
            self.regret_sum = {a: 0.0 for a in self.actions}
        if not self.strategy_sum:
            self.strategy_sum = {a: 0.0 for a in self.actions}

    def get_strategy(self, realization_weight: float) -> Dict[str, float]:
        positive_regrets = {a: max(self.regret_sum[a], 0.0) for a in self.actions}
        normalizing_sum = sum(positive_regrets.values())

        if normalizing_sum > 0:
            strategy = {a: positive_regrets[a] / normalizing_sum for a in self.actions}
        else:
            uniform = 1.0 / len(self.actions)
            strategy = {a: uniform for a in self.actions}

        for action, prob in strategy.items():
            self.strategy_sum[action] += realization_weight * prob

        return strategy

    def get_average_strategy(self) -> Dict[str, float]:
        normalizing_sum = sum(self.strategy_sum.values())
        if normalizing_sum == 0:
            uniform = 1.0 / len(self.actions)
            return {a: uniform for a in self.actions}
        return {a: self.strategy_sum[a] / normalizing_sum for a in self.actions}


class CFRTrainer:
    def __init__(self) -> None:
        self.nodes: Dict[str, InfoSet] = {}

    def train(self, iterations: int) -> Dict[str, Dict[str, float]]:
        for _ in range(iterations):
            for cards in permutations(kuhn.CARDS, 2):
                self.cfr(list(cards), "", 1.0, 1.0)
        return self.get_average_strategy()

    def cfr(self, cards: List[int], history: str, p0: float, p1: float) -> float:
        if kuhn.is_terminal(history):
            return float(kuhn.utility(history, cards))

        player = len(history) % 2
        actions = tuple(kuhn.get_actions(history))
        info_key = f"{cards[player]}{history}"

        node = self.nodes.get(info_key)
        if node is None:
            node = InfoSet(actions=actions)
            self.nodes[info_key] = node

        strategy = node.get_strategy(p0 if player == 0 else p1)

        util: Dict[str, float] = {}
        node_util = 0.0

        for action in actions:
            next_history = history + action
            if player == 0:
                util[action] = self.cfr(cards, next_history, p0 * strategy[action], p1)
            else:
                util[action] = self.cfr(cards, next_history, p0, p1 * strategy[action])
            node_util += strategy[action] * util[action]

        for action in actions:
            regret = util[action] - node_util
            if player == 0:
                node.regret_sum[action] += p1 * regret
            else:
                node.regret_sum[action] += p0 * (-regret)

        return node_util

    def get_average_strategy(self) -> Dict[str, Dict[str, float]]:
        return {key: node.get_average_strategy() for key, node in self.nodes.items()}
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Tuple

from solver.game.types import GameState


@dataclass
class InfoSetNode:
    actions: List[str]
    regret_sum: Dict[str, float]
    strategy_sum: Dict[str, float]

    @classmethod
    def from_actions(cls, actions: Iterable[str]) -> "InfoSetNode":
        action_list = list(actions)
        return cls(
            actions=action_list,
            regret_sum={action: 0.0 for action in action_list},
            strategy_sum={action: 0.0 for action in action_list},
        )

    def get_strategy(self, reach_prob: float) -> Dict[str, float]:
        positive_regrets = {
            action: max(0.0, self.regret_sum[action]) for action in self.actions
        }
        normalizer = sum(positive_regrets.values())
        if normalizer <= 0.0:
            strategy = {action: 1.0 / len(self.actions) for action in self.actions}
        else:
            strategy = {
                action: positive_regrets[action] / normalizer for action in self.actions
            }

        for action in self.actions:
            self.strategy_sum[action] += reach_prob * strategy[action]

        return strategy

    def get_average_strategy(self) -> Dict[str, float]:
        normalizer = sum(self.strategy_sum.values())
        if normalizer <= 0.0:
            return {action: 1.0 / len(self.actions) for action in self.actions}
        return {action: self.strategy_sum[action] / normalizer for action in self.actions}


def cfr(
    state: GameState,
    player: int,
    reach_probs: List[float],
    infosets: Dict[str, InfoSetNode],
) -> float:
    if state.is_terminal():
        return state.utility(player)

    if state.is_chance():
        util = 0.0
        for action, prob in state.chance_outcomes():
            util += prob * cfr(
                state.next_state(action),
                player,
                reach_probs,
                infosets,
            )
        return util

    current = state.current_player()
    info_key = state.information_set_key(current)
    node = infosets.get(info_key)
    if node is None:
        node = InfoSetNode.from_actions(state.legal_actions())
        infosets[info_key] = node

    strategy = node.get_strategy(reach_probs[current])
    action_utils: Dict[str, float] = {}
    node_util = 0.0

    for action in node.actions:
        next_reach = reach_probs.copy()
        next_reach[current] *= strategy[action]
        action_utils[action] = cfr(
            state.next_state(action),
            player,
            next_reach,
            infosets,
        )
        node_util += strategy[action] * action_utils[action]

    if current == player:
        opp_prob = 1.0
        for idx, prob in enumerate(reach_probs):
            if idx != current:
                opp_prob *= prob
        for action in node.actions:
            regret = action_utils[action] - node_util
            node.regret_sum[action] += opp_prob * regret

    return node_util


def train_cfr(
    game_factory,
    iterations: int,
    num_players: int,
) -> Dict[str, InfoSetNode]:
    infosets: Dict[str, InfoSetNode] = {}
    for _ in range(iterations):
        for player in range(num_players):
            cfr(game_factory(), player, [1.0] * num_players, infosets)
    return infosets
