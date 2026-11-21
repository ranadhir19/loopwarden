"""Lab 00 solution: the failure analysis, encoded as runnable checks.

The 'solution' to Lab 00 is not a fixed bare agent -- it is a precise,
checkable statement of HOW the bare agent fails, which the labs that follow
then repair one component at a time.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import ScriptedModel, tool_call, say, final, repeat  # noqa: E402
from bare_agent import run_bare_agent  # noqa: E402

TRUE_COUNT = "5"


def fresh_workspace():
    root = tempfile.mkdtemp(prefix="lab00_sol_")
    with open(os.path.join(root, "notes.txt"), "w", encoding="utf-8") as fh:
        fh.write("the quick brown fox jumps")
    return root


def failure_1_invented_tool_crashes():
    """No registry -> an invented tool name crashes the loop outright."""
    root = fresh_workspace()
    model = ScriptedModel([tool_call("readfile", path="notes.txt")])
    try:
        run_bare_agent(model, root, "count the words")
        return False
    except KeyError:
        return True


def failure_2_spin_never_stops():
    """No guardrails -> a spinning model is stopped only by the demo cap."""
    root = fresh_workspace()
    model = ScriptedModel([repeat(tool_call("read_file", path="notes.txt"))])
    status, _answer, steps = run_bare_agent(model, root, "count the words")
    return status == "demo_cap_reached" and steps == 30


def failure_3_false_claim_unchecked():
    """No verification -> a made-up answer is accepted at face value."""
    root = fresh_workspace()
    model = ScriptedModel([
        tool_call("write_file", path="count.txt", content="999"),
        final("Done! The word count is 999."),
    ])
    status, _answer, _steps = run_bare_agent(model, root, "count the words")
    with open(os.path.join(root, "count.txt"), encoding="utf-8") as fh:
        return status == "model_claimed_done" and fh.read() == "999"
