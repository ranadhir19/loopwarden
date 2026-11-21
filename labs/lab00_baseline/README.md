# Lab 00 — The Baseline: an agent with no harness

## Scope
The "before" picture. A bare Think → Act → Observe loop wired straight to
raw file functions: no tool registry, no validation, no limits, no
verification. You will run it against a scripted model that misbehaves in
the three classic ways — and watch the loop catch none of them.

## Learning objectives
- Explain why "write a better prompt" cannot fix any of the three failures.
- Name which harness component (Labs 01–05) repairs which failure.
- Distinguish a model *claim* ("Done!") from a verified outcome.

## Hands-on objectives
- Run `python3 demo_failure.py` and observe all three failure modes.
- Read `bare_agent.py` and find every place a harness component is missing.
- Run `python3 tests.py` — the tests assert the failures happen.

## Exercises
1. Run the demo. For each of the three runs, write one sentence: what did
   the model do, and what did the loop fail to do about it?
2. Remove the `demo_step_cap` argument's effect by raising it to 10,000 for
   run 2 only. What happens to run time? What would that cost with a real,
   billed model?
3. In run 3, the model's number (999) is wrong. List two places the truth
   ("5") was available but never consulted.

## What to observe
- A tool call is a *request*. The bare loop treats it as a command.
- The loop has no error channel: a bad tool name is a crash, not feedback.
- Nothing in the loop ever looks at the disk to check the model's claim.

Next: Lab 01 gives the loop a Tool Registry.
