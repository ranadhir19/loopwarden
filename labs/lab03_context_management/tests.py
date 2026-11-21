"""Lab 03 tests: budget enforced, task pinned, key facts survive compaction."""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.dirname(__file__))
from harnesskit import estimate_chars  # noqa: E402
from solution import trim_history, demo_history  # noqa: E402


class TestContextManagement(unittest.TestCase):
    def test_over_budget_history_is_trimmed_to_budget(self):
        history = demo_history()
        self.assertGreater(estimate_chars(history), 1500)
        view = trim_history(history, 1500)
        self.assertLessEqual(estimate_chars(view), 1500)

    def test_task_is_never_dropped(self):
        view = trim_history(demo_history(), 1500)
        contents = [m["content"] for m in view]
        self.assertTrue(any("TASK: report the total word count" in c for c in contents))

    def test_key_fact_survives_via_summary(self):
        view = trim_history(demo_history(), 1500)
        contents = [m["content"] for m in view]
        self.assertTrue(any("TOTAL_WORDS_SO_FAR: 5" in c for c in contents),
                        "the planted key fact must survive compaction")

    def test_newest_observation_kept_verbatim(self):
        view = trim_history(demo_history(), 1500)
        self.assertEqual(view[-1]["content"], "read_file -> latest observation")

    def test_small_history_passes_through(self):
        small = [{"role": "user", "content": "hi"}]
        self.assertEqual(trim_history(small, 1500), small)


if __name__ == "__main__":
    unittest.main(verbosity=2)
