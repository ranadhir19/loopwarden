"""harnesskit: the shared building blocks for the loopwarden labs.

Pure Python standard library. No API keys, no network, no installs.
"""
from .model import ScriptedModel, tool_call, say, final, repeat, always_say
from .registry import Tool, ToolRegistry, ToolError, jailed_path, make_workspace_tools
from .context import ContextManager, estimate_chars
from .guardrails import Budget, GuardrailStop
from .loop import run_agent, RunResult
from .verify import (Verification, check_file_equals, check_file_contains,
                     check_file_absent, check_all, TraceInspector)

__all__ = [
    "ScriptedModel", "tool_call", "say", "final", "repeat", "always_say",
    "Tool", "ToolRegistry", "ToolError", "jailed_path", "make_workspace_tools",
    "ContextManager", "estimate_chars", "Budget", "GuardrailStop",
    "run_agent", "RunResult", "Verification", "check_file_equals",
    "check_file_contains", "check_file_absent", "check_all", "TraceInspector",
]
