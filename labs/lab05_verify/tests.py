"""Lab 05 tests: a lying model fails verification; an honest one passes;
the run status alone proves nothing either way."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from harnesskit import ScriptedModel, make_workspace_tools, run_agent, tool_call, final  # noqa: E402
from solution import verify_run, audit_trace  # noqa: E402


def run_with(script):
    root = tempfile.mkdtemp(prefix="lab05_")
    reg = make_workspace_tools(root)
    reg.call("write_file", {"path": "notes.txt",
                            "content": "the quick brown fox jumps"})  # 5 words
    result = run_agent(ScriptedModel(script), reg,
                       "Write the word count of notes.txt into count.txt")
    return root, result


class TestVerify(unittest.TestCase):
    def test_honest_run_passes(self):
        _root, result = run_with([
            tool_call("read_file", path="notes.txt"),
            tool_call("write_file", path="count.txt", content="5"),
            final("Done: 5 words."),
        ])
        root = _root
        self.assertEqual(result.status, "completed")
        self.assertTrue(verify_run(root, result))

    def test_lying_run_fails_despite_claiming_success(self):
        root, result = run_with([
            tool_call("write_file", path="count.txt", content="999"),
            final("Done! The word count is 999."),
        ])
        self.assertEqual(result.status, "completed")   # the loop believed it
        self.assertFalse(verify_run(root, result))     # verification does not

    def test_no_output_fails(self):
        root, result = run_with([final("I could not do it.")])
        self.assertFalse(verify_run(root, result))

    def test_trace_audit(self):
        _root, result = run_with([
            tool_call("read_file", path="notes.txt"),
            tool_call("read_file", path="ghost.txt"),
            tool_call("write_file", path="count.txt", content="5"),
            final("done"),
        ])
        audit = audit_trace(result)
        self.assertTrue(audit["read_notes"])
        self.assertEqual(audit["tool_errors"], 1)
        self.assertIsNone(audit["stop_reason"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
