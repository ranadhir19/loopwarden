"""The agent loop: Think -> Act -> Observe -> Repeat, inside the harness.

The loop is the only place the model meets the world, and it routes every
interaction through the harness components: context management shapes what
the model sees, the registry validates and executes tool calls, guardrails
bound the run, and every step is written to a trace for verification.
"""
from .guardrails import Budget, GuardrailStop
from .registry import ToolError


class RunResult:
    def __init__(self, status, answer, trace, tool_calls, messages):
        self.status = status          # completed | stopped | model_finished_no_answer
        self.answer = answer          # final text from the model, or None
        self.trace = trace            # list of event dicts
        self.tool_calls = tool_calls
        self.messages = messages
        self.stop_reason = None

    def __repr__(self):
        return (f"RunResult(status={self.status!r}, tool_calls={self.tool_calls}, "
                f"messages={self.messages}, stop_reason={self.stop_reason!r})")


def run_agent(model, registry, task, budget=None, context_manager=None):
    budget = budget or Budget()
    budget.start()
    history = [
        {"role": "system",
         "content": "You are an agent working in a sandboxed workspace. "
                    "Use tools to do the work; do not guess file contents."},
        {"role": "user", "content": task},
    ]
    trace = [{"event": "task", "content": task}]
    answer = None
    status = "model_finished_no_answer"
    try:
        while True:
            budget.check_clock()
            view = context_manager.build(history) if context_manager else history
            action = model.respond(view, registry.names())
            budget.note_message()
            trace.append({"event": "model_action", "action": action})
            if action.get("type") == "final":
                answer = action.get("text", "")
                status = "completed"
                history.append({"role": "assistant", "content": answer})
                break
            if action.get("type") == "say":
                history.append({"role": "assistant", "content": action.get("text", "")})
                continue
            if action.get("type") == "tool_call":
                name, args = action.get("name", ""), action.get("args", {})
                budget.note_tool_call(name, args)
                try:
                    result = registry.call(name, args)
                    trace.append({"event": "tool_result", "name": name,
                                  "args": args, "result": str(result)[:500]})
                    history.append({"role": "tool",
                                    "content": f"{name} -> {result}"})
                except ToolError as exc:
                    budget.note_tool_failure(name, args)
                    trace.append({"event": "tool_error", "name": name,
                                  "args": args, "error": str(exc)})
                    history.append({"role": "tool",
                                    "content": f"{name} ERROR: {exc}"})
                continue
            history.append({"role": "assistant",
                            "content": f"[unrecognised action: {action!r}]"})
    except GuardrailStop as stop:
        status = "stopped"
        trace.append({"event": "guardrail_stop", "reason": stop.reason})
        result = RunResult(status, answer, trace, budget.tool_calls, budget.messages)
        result.stop_reason = stop.reason
        return result
    return RunResult(status, answer, trace, budget.tool_calls, budget.messages)
