"""Lab 00 tests: the bare agent must demonstrably fail in all three ways."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
import solution  # noqa: E402


class TestBareAgentFailures(unittest.TestCase):
    def test_invented_tool_crashes(self):
        self.assertTrue(solution.failure_1_invented_tool_crashes())

    def test_spin_never_stops(self):
        self.assertTrue(solution.failure_2_spin_never_stops())

    def test_false_claim_unchecked(self):
        self.assertTrue(solution.failure_3_false_claim_unchecked())


if __name__ == "__main__":
    unittest.main(verbosity=2)
