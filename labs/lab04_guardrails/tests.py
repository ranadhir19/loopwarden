"""Lab 04 tests: spinner, rambler and retry-looper are all stopped, each
with the right reason; a well-behaved model is not stopped at all."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from harnesskit import (ScriptedModel, make_workspace_tools, run_agent,  # noqa: E402
                        tool_call, final, repeat, always_say)
from solution import make_budget  # noqa: E402


def workspace():
    root = tempfile.mkdtemp(prefix="lab04_")
    reg = make_workspace_tools(root)
    reg.call("write_file", {"path": "notes.txt", "content": "alpha beta gamma"})
    return reg


class TestGuardrails(unittest.TestCase):
    def test_spinner_stopped_by_spin_detection(self):
        model = ScriptedModel([repeat(tool_call("read_file", path="notes.txt"))])
        result = run_agent(model, workspace(), "read the notes", budget=make_budget())
        self.assertEqual(result.status, "stopped")
        self.assertIn("spin_detected", result.stop_reason)
        self.assertLessEqual(result.tool_calls, 3)

    def test_rambler_stopped_by_message_budget(self):
        model = ScriptedModel([always_say("thinking... let me think more...")])
        result = run_agent(model, workspace(), "read the notes", budget=make_budget())
        self.assertEqual(result.status, "stopped")
        self.assertEqual(result.stop_reason, "message_budget_exceeded")
        self.assertEqual(result.tool_calls, 0)

    def test_retry_looper_stopped(self):
        # The same failing call repeated is caught by spin detection or the
        # retry budget -- whichever trips first, the run must stop.
        model = ScriptedModel([repeat(tool_call("read_file", path="missing.txt"))])
        result = run_agent(model, workspace(), "read a missing file", budget=make_budget())
        self.assertEqual(result.status, "stopped")
        self.assertIn(result.stop_reason.split(":")[0],
                      ("spin_detected", "retry_budget_exceeded"))

    def test_tool_call_budget_bounds_distinct_calls(self):
        calls = [tool_call("eval_expr", expr=f"{i} + 1") for i in range(30)]
        model = ScriptedModel(calls)
        result = run_agent(model, workspace(), "do sums", budget=make_budget())
        self.assertEqual(result.status, "stopped")
        self.assertEqual(result.stop_reason, "tool_call_budget_exceeded")
        self.assertEqual(result.tool_calls, 13)  # 12 allowed + the one that trips

    def test_well_behaved_model_unaffected(self):
        model = ScriptedModel([
            tool_call("read_file", path="notes.txt"),
            tool_call("eval_expr", expr="3 + 0"),
            final("notes have 3 words"),
        ])
        result = run_agent(model, workspace(), "count words", budget=make_budget())
        self.assertEqual(result.status, "completed")
        self.assertEqual(result.answer, "notes have 3 words")


if __name__ == "__main__":
    unittest.main(verbosity=2)
