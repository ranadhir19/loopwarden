"""Run the bare agent against a misbehaving scripted model and watch it fail.

    python3 demo_failure.py

The task: read notes.txt and write the word count into count.txt.
The model rambles, invents a tool name, spins on one file, then writes a
made-up number and claims success. The bare loop catches none of it.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from harnesskit import ScriptedModel, tool_call, say, final, repeat  # noqa: E402
from bare_agent import run_bare_agent  # noqa: E402


def main():
    root = tempfile.mkdtemp(prefix="lab00_")
    with open(os.path.join(root, "notes.txt"), "w", encoding="utf-8") as fh:
        fh.write("the quick brown fox jumps")  # 5 words

    misbehaving = ScriptedModel([
        say("Let me think about word counts in general..."),       # rambles
        tool_call("readfile", path="notes.txt"),                   # invented tool name
    ])
    try:
        status, answer, steps = run_bare_agent(
            misbehaving, root, "Write the word count of notes.txt into count.txt")
        print(f"run 1: status={status} steps={steps} answer={answer!r}")
    except Exception as exc:  # the bare loop has no error channel at all
        print(f"run 1: CRASHED with {type(exc).__name__}: {exc} "
              "(no observation was returned to the model)")

    spinning = ScriptedModel([
        repeat(tool_call("read_file", path="notes.txt")),          # spins forever
    ])
    status, answer, steps = run_bare_agent(
        spinning, root, "Write the word count of notes.txt into count.txt")
    print(f"run 2: status={status} steps={steps} "
          "(stopped only by the demo cap -- a real bare loop never stops)")

    hallucinating = ScriptedModel([
        tool_call("write_file", path="count.txt", content="999"),  # made-up number
        final("Done! The word count is 999."),                     # false claim
    ])
    status, answer, steps = run_bare_agent(
        hallucinating, root, "Write the word count of notes.txt into count.txt")
    with open(os.path.join(root, "count.txt"), encoding="utf-8") as fh:
        on_disk = fh.read()
    print(f"run 3: status={status} answer={answer!r}")
    print(f"       count.txt on disk says {on_disk!r}; the true count is 5. "
          "Nothing checked.")


if __name__ == "__main__":
    main()
