"""Lab 03 starter: context management.

TODO: implement trim_history() using harnesskit.ContextManager so the
history handed to the model stays within a character budget while the
task (first two entries) and the newest observations survive.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import ContextManager  # noqa: E402,F401


def trim_history(history, budget_chars):
    """Return a within-budget view of history."""
    # TODO: build a ContextManager with this budget and return its view.
    return history
