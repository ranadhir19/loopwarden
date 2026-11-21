# Lab 04 — Guardrails: bounding a run that goes wrong

## Scope
The fourth harness component. Guardrails do not make the model smarter;
they bound the damage when it misbehaves. One `Budget` object enforces:
tool-call cap, message cap, per-call retry cap, a wall-clock limit, and
spin detection (the same tool called with identical arguments repeatedly).
Every stop carries a machine-readable reason in the trace.

## Learning objectives
- Explain why limits must live outside the model (a spinning model will
  happily agree to stop — and then not stop).
- Match each misbehaviour (spin, ramble, retry-loop, runaway) to the limit
  that catches it, and name the limit that catches it *first*.
- Argue how limits should be sized: from the task, not from vibes.

## Hands-on objectives
- Configure `make_budget()` in `starter.py` for a 5-file research task.
- Run `python3 tests.py`: four misbehaving models stopped with the right
  reasons; one good model untouched.
- Read a stopped run's trace and find the `guardrail_stop` event.

## Exercises
1. The retry-loop test can be stopped by spin detection *or* the retry
   budget. Which fires first with the solution's limits, and why? Change
   one number so the other fires first, and prove it with the trace.
2. Set `spin_limit` to 10 and `max_tool_calls` to 6. Which limit now
   protects you from the spinner, and what did you lose?
3. A legitimate task needs to read the same file twice (before and after a
   write). Does spin detection block it? Read the detector and explain.

## What to observe
- A stop is a *successful* harness outcome: bounded cost, clear reason.
- The trace records the reason — that is what your on-call self wants at
  3 a.m., not a 40,000-line transcript.

Next: Lab 05 checks the work itself, not the model's word for it.
