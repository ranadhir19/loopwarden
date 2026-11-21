"""Lab 02 starter: the swappable model layer.

Any object with respond(history, tool_names) -> action is a model.
TODO: implement EchoScriptModel below so the SAME agent code that runs the
ScriptedModel also runs yours, unchanged.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import final  # noqa: E402


class EchoScriptModel:
    """A minimal custom model: reads notes.txt, then finishes.

    It must decide from the history it is given (like a real model would),
    not from a fixed playback: if it has not yet seen a tool result for
    read_file, ask for it; otherwise finish with what it read.
    """

    name = "echo-script"

    def respond(self, history, tool_names):
        # TODO: scan history for a tool message containing the file content;
        # if none, return a tool_call for read_file notes.txt;
        # if found, return final(...) quoting the content.
        return final("[not implemented]")
