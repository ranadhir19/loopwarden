"""Lab 00 starter: encode the failure analysis yourself.

Run demo_failure.py, read bare_agent.py, then implement the three checks
below so each returns True exactly when the bare agent fails in the
described way. Compare with solution.py when yours work.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import ScriptedModel, tool_call, final, repeat  # noqa: E402,F401
from bare_agent import run_bare_agent  # noqa: E402,F401


def fresh_workspace():
    root = tempfile.mkdtemp(prefix="lab00_start_")
    with open(os.path.join(root, "notes.txt"), "w", encoding="utf-8") as fh:
        fh.write("the quick brown fox jumps")  # 5 words
    return root


def failure_1_invented_tool_crashes():
    """TODO: drive the bare agent with a model that calls a tool named
    'readfile' (which does not exist). Return True if the run crashes."""
    return False


def failure_2_spin_never_stops():
    """TODO: drive it with a model that repeats one read forever. Return
    True if only the demo step cap stops the run."""
    return False


def failure_3_false_claim_unchecked():
    """TODO: drive it with a model that writes '999' and claims success.
    Return True if the loop accepts the claim and the wrong file stands."""
    return False
