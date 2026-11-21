# Lab 02 — The Model Layer: swappable by design

## Scope
The second harness component. The model sits behind one tiny interface —
`respond(history, tool_names) -> action` — so the agent code never knows
which model it is running. You will run the *same* agent against a playback
script, a decision-making fake model, and (optionally) a real
OpenAI-compatible endpoint, and get the same behaviour from all of them.

## Learning objectives
- Explain why the model must be a replaceable part, not the architecture.
- Describe what a scripted model can and cannot teach you about a real one.
- State the offline-first rule: no lab or test may require an API key.

## Hands-on objectives
- Implement `EchoScriptModel` in `starter.py` (decides from history).
- Run `python3 tests.py`, including the HTTP-adapter test, which uses a
  local stub server — no internet, no key.
- Swap models in `solution.make_model` and re-run the agent unchanged.

## Exercises
1. Write a third fake model that always asks for one more file than exists,
   and run the agent with it. What stops the run? (Nothing yet — that is
   Lab 04's job. Note the behaviour.)
2. Point the HTTP adapter at a real endpoint you control (set
   `HF_MODEL_ENDPOINT`, `HF_MODEL_NAME`, `HF_MODEL_API_KEY`). What breaks
   first: the model's action format, or your assumptions about it?
3. The playback model and the echo model return the same answer by
   different routes. Which one would catch a registry change (e.g. the
   read tool renamed to `fetch_file`)? Why?

## What to observe
- Tests never call the real adapter's network path; the stub proves the
  parsing contract offline.
- Model choice becomes a configuration decision, reviewable like any other.

Next: Lab 03 manages what the model gets to see.
