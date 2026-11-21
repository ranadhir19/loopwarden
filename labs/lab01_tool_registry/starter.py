"""Lab 01 starter: build a Tool Registry.

Fill in the TODOs. The worked solution is in solution.py -- try first.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit.registry import Tool, ToolRegistry, ToolError, jailed_path  # noqa: E402,F401


def build_registry(root):
    """Return a ToolRegistry over workspace `root` with:
    read_file (read), write_file (write), eval_expr (execute).
    Every file path must be jailed inside root.
    """
    registry = ToolRegistry()
    # TODO: define the three tool handlers. Each file handler must resolve
    # its path with jailed_path(root, path) before touching the disk.
    # TODO: register each tool with the right permission class and schema.
    return registry
