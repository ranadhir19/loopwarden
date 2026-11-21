"""Lab 01 solution: a Tool Registry with schemas, permissions and a jail."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import make_workspace_tools  # noqa: E402


def build_registry(root):
    """The standard workspace registry: read/write/execute tool classes,
    JSON-style argument schemas, and every path jailed inside `root`."""
    return make_workspace_tools(root)
