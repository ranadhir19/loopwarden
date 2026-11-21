"""Guardrails: hard limits that stop a misbehaving agent loop.

A guardrail never tries to fix the model. It bounds the damage: how many
tool calls, how many messages, how many retries of the same failing call,
how long the run may take, and whether the model is spinning in place.
"""
import time


class GuardrailStop(Exception):
    def __init__(self, reason):
        super().__init__(reason)
        self.reason = reason


class Budget:
    def __init__(self, max_tool_calls=25, max_messages=40, max_retries=2,
                 wall_clock_seconds=60.0, spin_limit=3):
        self.max_tool_calls = max_tool_calls
        self.max_messages = max_messages
        self.max_retries = max_retries
        self.wall_clock_seconds = wall_clock_seconds
        self.spin_limit = spin_limit
        self.tool_calls = 0
        self.messages = 0
        self._started = None
        self._failures = {}
        self._recent_calls = []

    def start(self):
        self._started = time.monotonic()

    def check_clock(self):
        if self._started is not None and \
                time.monotonic() - self._started > self.wall_clock_seconds:
            raise GuardrailStop("wall_clock_exceeded")

    def note_message(self):
        self.messages += 1
        if self.messages > self.max_messages:
            raise GuardrailStop("message_budget_exceeded")

    def note_tool_call(self, name, args):
        """Record a tool call; raise GuardrailStop if a limit is crossed.

        Returns the number of consecutive identical calls (for the trace).
        """
        self.tool_calls += 1
        if self.tool_calls > self.max_tool_calls:
            raise GuardrailStop("tool_call_budget_exceeded")
        key = (name, repr(sorted((args or {}).items())))
        self._recent_calls.append(key)
        run = 0
        for k in reversed(self._recent_calls):
            if k == key:
                run += 1
            else:
                break
        if run >= self.spin_limit:
            raise GuardrailStop(f"spin_detected: {name} called {run} times "
                                "in a row with identical arguments")
        return run

    def note_tool_failure(self, name, args):
        key = (name, repr(sorted((args or {}).items())))
        self._failures[key] = self._failures.get(key, 0) + 1
        if self._failures[key] > self.max_retries:
            raise GuardrailStop(
                f"retry_budget_exceeded: {name} failed "
                f"{self._failures[key]} times with the same arguments")
