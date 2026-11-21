"""Lab 01 tests: schemas enforced, permissions recorded, jail holds."""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from harnesskit import ToolError  # noqa: E402
from solution import build_registry  # noqa: E402


class TestToolRegistry(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="lab01_")
        self.reg = build_registry(self.root)

    def test_valid_round_trip(self):
        self.reg.call("write_file", {"path": "a.txt", "content": "hello"})
        self.assertEqual(self.reg.call("read_file", {"path": "a.txt"}), "hello")

    def test_unknown_tool_rejected(self):
        with self.assertRaises(ToolError):
            self.reg.call("readfile", {"path": "a.txt"})

    def test_missing_argument_rejected(self):
        with self.assertRaises(ToolError):
            self.reg.call("read_file", {})

    def test_wrong_type_rejected(self):
        with self.assertRaises(ToolError):
            self.reg.call("write_file", {"path": "a.txt", "content": 42})

    def test_unexpected_argument_rejected(self):
        with self.assertRaises(ToolError):
            self.reg.call("read_file", {"path": "a.txt", "mode": "r"})

    def test_jail_blocks_escape(self):
        with self.assertRaises(ToolError):
            self.reg.call("read_file", {"path": "../outside.txt"})
        with self.assertRaises(ToolError):
            self.reg.call("write_file", {"path": "/tmp/evil.txt", "content": "x"})

    def test_missing_file_is_tool_error_not_crash(self):
        with self.assertRaises(ToolError):
            self.reg.call("read_file", {"path": "nope.txt"})

    def test_execute_class_tool(self):
        self.assertEqual(self.reg.call("eval_expr", {"expr": "6 * 7"}), "42")

    def test_registry_describes_permissions(self):
        text = self.reg.describe()
        self.assertIn("[read]", text)
        self.assertIn("[write]", text)
        self.assertIn("[execute]", text)


if __name__ == "__main__":
    unittest.main(verbosity=2)
