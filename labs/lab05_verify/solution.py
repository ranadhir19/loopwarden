"""Lab 05 solution: recompute the truth, compare, and audit the trace."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import check_file_equals, TraceInspector  # noqa: E402


def true_word_count(root):
    with open(os.path.join(root, "notes.txt"), encoding="utf-8") as fh:
        return str(len(fh.read().split()))


def verify_run(root, result):
    """Ground truth is recomputed from disk. result.answer is never read."""
    check = check_file_equals(os.path.join(root, "count.txt"),
                              true_word_count(root))
    return check.passed


def audit_trace(result):
    """What an auditor can learn from the trace alone."""
    insp = TraceInspector(result.trace)
    return {
        "tool_results": insp.count("tool_result"),
        "tool_errors": insp.count("tool_error"),
        "stop_reason": insp.stop_reason(),
        "read_notes": len(insp.tool_calls("read_file")) > 0,
    }
