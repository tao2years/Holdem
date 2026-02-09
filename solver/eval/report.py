"""Format training results for quick inspection."""

from __future__ import annotations

from typing import Dict


def format_strategy(strategy: Dict[str, Dict[str, float]]) -> str:
    ordered_keys = sorted(strategy.keys())
    output_lines = []
    for key in ordered_keys:
        actions = strategy[key]
        action_str = ", ".join(f"{action}:{prob:.3f}" for action, prob in actions.items())
        output_lines.append(f"{key} -> {action_str}")
    return "\n".join(output_lines)
