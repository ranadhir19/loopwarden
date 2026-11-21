"""Verify: check outcomes against ground truth, never the model's claim.

A model's final message is a *claim*. Verification re-derives the truth
from the world (files on disk, recomputed values) and compares.
"""
import os


class Verification:
    def __init__(self, name, passed, detail=""):
        self.name = name
        self.passed = bool(passed)
        self.detail = detail

    def __repr__(self):
        return f"Verification({self.name}: {'PASS' if self.passed else 'FAIL'} {self.detail})"


def check_file_equals(path, expected):
    if not os.path.isfile(path):
        return Verification("file_equals", False, f"{path} does not exist")
    with open(path, encoding="utf-8") as fh:
        actual = fh.read()
    ok = actual.strip() == expected.strip()
    return Verification("file_equals", ok,
                        "" if ok else f"expected {expected.strip()!r}, found {actual.strip()!r}")


def check_file_contains(path, needle):
    if not os.path.isfile(path):
        return Verification("file_contains", False, f"{path} does not exist")
    with open(path, encoding="utf-8") as fh:
        actual = fh.read()
    return Verification("file_contains", needle in actual,
                        "" if needle in actual else f"{needle!r} not in {path}")


def check_file_absent(path):
    return Verification("file_absent", not os.path.exists(path),
                        "" if not os.path.exists(path) else f"{path} should not exist")


def check_all(checks):
    return all(c.passed for c in checks)


class TraceInspector:
    """Read a run trace the way an auditor would."""

    def __init__(self, trace):
        self.trace = trace

    def count(self, event):
        return sum(1 for e in self.trace if e.get("event") == event)

    def tool_calls(self, name=None):
        return [e for e in self.trace
                if e.get("event") in ("tool_result", "tool_error")
                and (name is None or e.get("name") == name)]

    def errors(self):
        return [e for e in self.trace if e.get("event") == "tool_error"]

    def stop_reason(self):
        for e in self.trace:
            if e.get("event") == "guardrail_stop":
                return e.get("reason")
        return None

    def saw_error_containing(self, text):
        return any(text in e.get("error", "") for e in self.errors())
