"""Lab 04 starter: guardrails.

TODO: configure a Budget that stops each misbehaving model below with the
right reason. The loop and Budget class are in harnesskit -- your job is
choosing limits and reading the stop reasons.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import Budget  # noqa: E402


def make_budget():
    """Return a Budget tight enough for a 5-file research task:
    at most 12 tool calls, at most 20 messages, at most 2 retries of a
    failing call, spin detection after 3 identical calls in a row."""
    # TODO: return Budget(...) with those limits.
    return Budget()
