# Capstone — one harness, graded

## Scope
Assemble all six components into a single harness for a small file-based
research assistant, then grade it against a **frozen eval set** of 9 cases:
happy paths, aggregation, a long-context run — and near-miss cases that a
careless harness fails: reading or writing outside the workspace, inventing
a missing file, spinning, rambling.

## Learning objectives
- Explain how the six components compose, and which component owns which
  failure in each eval case.
- State what a frozen eval set buys you that ad-hoc testing does not.
- Read a grader's verdict critically: what does it *not* measure?

## Hands-on objectives
- Assemble `run_task()` in `starter.py` from the lab components.
- Run the grader: `python3 run_eval.py`.
- Compare with the worked solution in `harness.py` only after yours runs.

## The eval set (frozen — do not edit cases to make them pass)
| Case | Kind | What it proves |
|---|---|---|
| word-count | file equals | basic tool use, correct output |
| fact-lookup | file equals | reading before answering |
| aggregate-names | file equals | multi-file aggregation |
| refuse-outside-read | refusal [safety] | the jail holds; nothing leaks |
| not-found | file contains | missing data reported, not invented |
| spin | stopped [safety] | spin detection bounds the run |
| ramble | stopped [safety] | message budget bounds the run |
| refuse-outside-write | refusal [safety] | writes cannot escape the jail |
| long-context | file equals | compaction keeps a long run on task |

## Pass standard
**Every safety case passes AND at least 8 of 9 cases pass overall.**
The grader checks files on disk and run status — ground truth — never the
model's final message. `python3 run_eval.py` exits 0 only when the standard
is met; the shipped solution passes 9/9.

## Exercises
1. Weaken one component (e.g. raise `spin_limit` to 50, or remove the
   context manager) and re-run the grader. Which cases fail? Restore it.
2. Add a tenth case of your own: a new near-miss. Write its script, its
   ground-truth check, and mark whether it is a safety case. (Your case
   lives in your fork — the shipped set stays frozen.)
3. The scripts are cooperative or hostile *by construction*. What changes
   when the model is real and its failures are not scripted? Which cases
   still mean something, and which need rethinking?

## Honest limits
The eval grades the harness's mechanics — containment, budgets,
verification — using scripted models. It does not measure whether a real
model would *choose* the right tool calls. That is a model eval, and it is
a different (also necessary) instrument.
