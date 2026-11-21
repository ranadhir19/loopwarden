"""Capstone solution: one harness, all six components.

  1. Tool Registry      - make_workspace_tools: schemas, permissions, jail
  2. Model layer        - any respond() object; the eval uses scripted ones
  3. Context Management - ContextManager with a fixed character budget
  4. Guardrails         - Budget: call/message/retry caps, spin detection
  5. Agent Loop         - harnesskit.run_agent (Think -> Act -> Observe)
  6. Verify             - run_eval.py grades outcomes against ground truth
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from harnesskit import (Budget, ContextManager, make_workspace_tools,  # noqa: E402
                        run_agent)


def build_harness(root):
    registry = make_workspace_tools(root)
    context = ContextManager(budget_chars=2500, pinned=2, keep_recent=3)
    budget = Budget(max_tool_calls=20, max_messages=30, max_retries=2,
                    wall_clock_seconds=30.0, spin_limit=3)
    return registry, context, budget


def run_task(root, prompt, model):
    registry, context, budget = build_harness(root)
    return run_agent(model, registry, prompt,
                     budget=budget, context_manager=context)
