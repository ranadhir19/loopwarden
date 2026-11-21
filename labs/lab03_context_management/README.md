# Lab 03 — Context Management: what the model gets to see

## Scope
The third harness component. A long run produces more history than any
context window (or budget) can hold. The harness — not the model — decides
what survives: the task is pinned, the newest observations stay verbatim,
and the middle is compacted into a summary whose digest keeps the first
line of each dropped observation, so key facts tools reported survive.

## Learning objectives
- Explain the failure mode of naive "keep everything" and "keep last N".
- Describe a compaction policy and its information-loss trade-off.
- Explain why context policy belongs to the harness, not the prompt.

## Hands-on objectives
- Implement `trim_history` in `starter.py` on top of `ContextManager`.
- Run `python3 tests.py`: budget enforced, task pinned, fact survives.
- Print a before/after view of `demo_history()` and diff them by eye.

## Exercises
1. Lower the budget to 400 characters. What is lost first? Is the result
   still safe to hand to a model? What would you pin that we do not?
2. Change the digest rule from "first line" to "last line". Which test
   fails, and what does that tell you about tool-output design? (Tools
   should put their key result on the first line.)
3. A tool returns a 50,000-character file. Where in this design does that
   get stopped — context manager, tool, or registry? Argue for one place.

## What to observe
- Compaction is lossy by design; the skill is choosing *what* is lost.
- The summary is labelled as a summary — the model can tell digested
  history from verbatim observation.

Next: Lab 04 bounds how long and how hard the loop may run.
