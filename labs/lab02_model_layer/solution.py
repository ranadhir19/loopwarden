"""Lab 02 solution: one agent, three models, zero agent-code changes."""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import ScriptedModel, tool_call, final  # noqa: E402
from harnesskit.http_model import HttpModel  # noqa: E402,F401  (adapter, optional)


class EchoScriptModel:
    """A decision-making fake model: reacts to history instead of replaying
    a fixed script -- the closest offline stand-in for a real LLM."""

    name = "echo-script"

    def respond(self, history, tool_names):
        for msg in reversed(history):
            if msg.get("role") == "tool" and "read_file ->" in msg.get("content", ""):
                content = msg["content"].split("read_file ->", 1)[1].strip()
                return final("The notes say: " + content)
        return tool_call("read_file", path="notes.txt")


def scripted_playback_model():
    """The same behaviour as a fixed playback script (Lab 00 style)."""
    return ScriptedModel([
        tool_call("read_file", path="notes.txt"),
        final("The notes say: the quick brown fox jumps"),
    ], name="playback")


def make_model(kind):
    """Factory: pick a model by name. 'http' needs HF_MODEL_* env vars and
    is never used by the tests; the agent code does not care which it gets."""
    if kind == "playback":
        return scripted_playback_model()
    if kind == "echo":
        return EchoScriptModel()
    if kind == "http":
        return HttpModel()
    raise ValueError("unknown model kind: " + kind)
