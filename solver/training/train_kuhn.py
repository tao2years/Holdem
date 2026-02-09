"""Train CFR on Kuhn Poker as a minimal solver example."""

from __future__ import annotations

from typing import Dict

from solver.core.cfr import CFRTrainer
from solver.eval.report import format_strategy


def train_kuhn(iterations: int = 10000) -> Dict[str, Dict[str, float]]:
    trainer = CFRTrainer()
    strategy = trainer.train(iterations)
    print(f"Iterations: {iterations}")
    print(format_strategy(strategy))
    return strategy


if __name__ == "__main__":
    train_kuhn()
