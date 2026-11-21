"""Lab 04 solution: budgets sized to the task, and each stop reason read."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import Budget  # noqa: E402


def make_budget():
    return Budget(max_tool_calls=12, max_messages=20, max_retries=2,
                  wall_clock_seconds=30.0, spin_limit=3)
