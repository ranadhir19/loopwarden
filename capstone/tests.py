"""Capstone tests: the assembled harness meets the eval pass standard."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(__file__))
import run_eval  # noqa: E402


class TestCapstoneEval(unittest.TestCase):
    def test_eval_set_has_at_least_eight_cases_with_near_misses(self):
        import json
        with open(os.path.join(os.path.dirname(__file__), "eval_cases.json"),
                  encoding="utf-8") as fh:
            data = json.load(fh)
        self.assertGreaterEqual(len(data["cases"]), 8)
        kinds = {c["kind"] for c in data["cases"]}
        self.assertIn("refusal", kinds)   # near-miss cases exist
        self.assertIn("stopped", kinds)

    def test_harness_meets_pass_standard(self):
        ok, results = run_eval.run_all(verbose=False)
        failed = [r["id"] for r in results if not r["passed"]]
        self.assertTrue(ok, f"eval failed; failing cases: {failed}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
