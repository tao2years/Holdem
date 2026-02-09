"""CLI entry for Kuhn Poker CFR training."""

from __future__ import annotations

import argparse

from solver.training.train_kuhn import train_kuhn


def main() -> None:
    parser = argparse.ArgumentParser(description="Run CFR on Kuhn Poker.")
    parser.add_argument("--iterations", type=int, default=10000)
    args = parser.parse_args()
    train_kuhn(iterations=args.iterations)


if __name__ == "__main__":
    main()
import argparse

from solver.core.cfr import train_cfr
from solver.game.kuhn_poker import initial_state


def main() -> None:
    parser = argparse.ArgumentParser(description="Train CFR on Kuhn Poker.")
    parser.add_argument("--iterations", type=int, default=10000)
    args = parser.parse_args()

    infosets = train_cfr(initial_state, args.iterations, num_players=2)
    for key in sorted(infosets.keys()):
        avg = infosets[key].get_average_strategy()
        print(f"{key} -> {avg}")


if __name__ == "__main__":
    main()
