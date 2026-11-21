"""Lab 03 solution: budget, pin the task, compact the middle, keep the new."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import ContextManager, estimate_chars  # noqa: E402,F401


def trim_history(history, budget_chars):
    manager = ContextManager(budget_chars=budget_chars, pinned=2, keep_recent=3)
    return manager.build(history)


def demo_history():
    """A long run: task, then 8 tool observations, the first of which
    carries a key fact on its first line."""
    history = [
        {"role": "system", "content": "You are an agent in a sandbox."},
        {"role": "user", "content": "TASK: report the total word count."},
        {"role": "tool", "content": "TOTAL_WORDS_SO_FAR: 5\n(from notes.txt, first pass)"},
    ]
    for i in range(7):
        history.append({"role": "tool",
                        "content": f"read chunk {i}: " + ("filler text " * 40)})
    history.append({"role": "tool", "content": "read_file -> latest observation"})
    return history
