# loopwarden — the Agentic Harness, as a hands-on lab

> Stop trying to fix an unreliable agent with a better prompt. Build the
> system around the model that controls everything you *can* control:
> its tools, its context, its limits, its loop — and the proof that the
> work actually happened.

**loopwarden** is a free, offline, hands-on lab that teaches the *agentic
harness*: the engineering layer around a language model that turns a
clever-but-erratic model into a dependable agent. You start with a bare
agent loop that fails in three classic ways, then build the harness one
component at a time — Tool Registry, swappable Model layer, Context
Management, Guardrails, the Agent Loop, and Verify — and finish with a
capstone that assembles all six and grades them against a frozen eval set.

Everything runs **offline, with zero API keys and zero paid models**. A
deterministic scripted model plays the part of the LLM — including its
failure modes (rambling, inventing tools, spinning in place) — so every
exercise is reproducible on any machine. An optional adapter for a real
OpenAI-compatible endpoint is included for afterwards, but nothing in the
lab requires it.

Framework background: this lab is the hands-on companion to the tutorial
*The Agentic Harness — From First Loop to Production System*, which builds
on the framework popularised in Tejas Kumar's talk on the agentic harness
(six components; a weaker model with an unchanged prompt completing a task
once a harness was built around it).

## Scope

In scope: the six harness components, each as a runnable lab with tests;
a complete assembled harness; a frozen eval set with near-miss (refusal)
cases and a stated pass standard. Out of scope: model training, prompt
engineering techniques, any specific vendor framework, and hosted
services. Pure Python 3 standard library — no `pip install`, ever.

## Learning objectives

By the end you will be able to:

1. Explain why prompts alone cannot fix an unreliable agent, and name the
   harness component responsible for each classic failure.
2. Design a tool registry with argument schemas, permission classes
   (read / write / execute) and path jailing.
3. Put any model behind a swappable interface and test agent code against
   a deterministic fake model.
4. Manage context deliberately: budgets, pinning, compaction that keeps
   key facts alive.
5. Bound a run with guardrails — tool-call, message and retry budgets,
   wall-clock limits, spin detection — and read stop reasons from a trace.
6. Verify outcomes against ground truth instead of trusting the model's
   own claim of success, and grade a harness against a frozen eval set.

## Hands-on objectives

You will build, break, and test:

- a bare agent loop, and a written analysis of its three failure modes;
- a tool registry that turns crashes into recoverable observations;
- two interchangeable fake models plus an HTTP adapter proven against a
  local stub server;
- a context manager that keeps a long run inside a fixed budget;
- a budget configuration that stops spinning, rambling and retry-looping
  models — each with the right reason;
- a verifier that catches a model lying about its own work;
- a complete harness that passes a 9-case frozen eval, including safety
  cases that must refuse or stop.

## Prerequisites

- Python 3.10+ (standard library only). Check: `python3 --version`.
- A terminal and a text editor. No accounts, keys, or network needed.

## Get the lab and run it

```sh
git clone https://github.com/ranadhir19/loopwarden.git
cd loopwarden
python3 validate.py        # runs every lab's tests + the capstone grader
```

Then work the labs in order. Each lab folder has a `README.md` (scope,
objectives, exercises), a `starter.py` to complete, a `solution.py` to
compare against, and `tests.py` to check your work:

```sh
python3 labs/lab00_baseline/tests.py
```

## Lab map

| Lab | Component | The failure it fixes |
|---|---|---|
| [lab00_baseline](labs/lab00_baseline/) | — (no harness) | the baseline: crash, spin, false claim |
| [lab01_tool_registry](labs/lab01_tool_registry/) | Tool Registry | invented tools, bad args, path escapes |
| [lab02_model_layer](labs/lab02_model_layer/) | Model layer | agent code welded to one model |
| [lab03_context_management](labs/lab03_context_management/) | Context Management | unbounded, unmanaged history |
| [lab04_guardrails](labs/lab04_guardrails/) | Guardrails (+ the Loop) | spins, rambles, retry loops, runaway cost |
| [lab05_verify](labs/lab05_verify/) | Verify | the model's word taken as proof |
| [capstone](capstone/) | all six, assembled | graded against a frozen eval set |

## Suggested timeline

**7-day plan** (about an hour a day):

| Day | Work |
|---|---|
| 1 | Lab 00 — run the failures, write the analysis |
| 2 | Lab 01 — tool registry |
| 3 | Lab 02 — model layer |
| 4 | Lab 03 — context management |
| 5 | Lab 04 — guardrails |
| 6 | Lab 05 — verify |
| 7 | Capstone — assemble, grade, do exercise 1 (weaken & restore) |

**2-weekend plan**:

| Session | Work |
|---|---|
| Weekend 1, day 1 | Labs 00–01 |
| Weekend 1, day 2 | Labs 02–03 |
| Weekend 2, day 1 | Labs 04–05 |
| Weekend 2, day 2 | Capstone + exercises; re-run `validate.py` |

## The capstone

A complete harness for a small file-based research assistant, graded by
`capstone/run_eval.py` against 9 frozen cases — happy paths, aggregation,
a long-context run, and near-misses that must be refused or safely stopped
(reads/writes outside the workspace, a missing file that must not be
invented, a spinning model, a rambling model). **Pass standard: every
safety case passes AND at least 8 of 9 cases pass.** The shipped solution
passes 9/9. See [capstone/README.md](capstone/README.md).

## Repository harness

`python3 validate.py` is this repo's own harness — fittingly. It checks
the structure (every lab has a README, starter, solution and tests), runs
every lab's test suite, and runs the capstone grader, exiting 0 only when
everything passes. Current state: **all labs pass; capstone 9/9.**

## License

MIT — see [LICENSE](LICENSE). Copyright (c) 2026 Ranadhir Ghosh.

## Name

The lab was built under the working name "harnessforge"; that name turned
out to be taken by several existing projects, so the lab is published as
**loopwarden** — the warden that guards the agent loop. The full collision
check is recorded in [NAME_CHECK.md](NAME_CHECK.md).
