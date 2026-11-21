"""Lab 05 starter: verification against ground truth.

TODO: implement verify_run() so it checks the run's OUTCOME on disk --
never the model's final message.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import check_file_equals  # noqa: E402,F401


def verify_run(root, result):
    """Return True only if count.txt in `root` holds the true word count
    of notes.txt, recomputed here from disk. The model's answer text and
    the run status are claims -- ignore them."""
    # TODO: read notes.txt, compute its word count, and compare against
    # count.txt with check_file_equals.
    return False
