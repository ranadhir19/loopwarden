# Lab 05 — Verify: never grade the model's homework by its own answer

## Scope
The sixth harness component (the Agent Loop itself was Lab 04's stage).
Verification recomputes ground truth from the world — files on disk,
recomputed values — and compares it with what the run actually produced.
The model's final message is treated as an unverified claim, always.

## Learning objectives
- Explain the difference between run status, model claim, and verified
  outcome — and why only the third is evidence.
- Design a checker that cannot be fooled by the artefact it checks (the
  truth here is recomputed from the *source* file, not read from the
  model's output file and compared with itself).
- Use a trace as an audit artefact: counts, errors, stop reasons.

## Hands-on objectives
- Implement `verify_run` in `starter.py` (recompute, then compare).
- Run `python3 tests.py`: the lying model from Lab 00 finally fails.
- Extend `audit_trace` with one more signal you would want on call.

## Exercises
1. Write a model script that produces the *right* count.txt by luck
   (hard-codes "5" without reading notes.txt). Verification passes — is
   that acceptable? Use the trace audit to catch it, and add a check.
2. The checker compares stripped text. When is exact-byte comparison the
   right standard instead? Give one task of each kind.
3. Verification here is post-hoc. Sketch how you would verify *during*
   the run (after each write) and what that buys you.

## What to observe
- Lab 00's run 3 and this lab's lying run are the same script. The loop
  says "completed" both times. Only verification separates them.
- A frozen, independent checker is the seed of the capstone's grader.

Next: the capstone assembles all six components into one harness and
grades it against a frozen eval set.
