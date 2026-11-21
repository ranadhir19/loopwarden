"""Model layer: a swappable interface plus a deterministic scripted model.

An *action* is a plain dict, one of:
  {"type": "tool_call", "name": <str>, "args": {<str>: value}}
  {"type": "say",       "text": <str>}    # model talks, takes no action
  {"type": "final",     "text": <str>}    # model declares the task done

A model is any object with:
  respond(history, tool_names) -> action dict
where history is a list of {"role": ..., "content": ...} dicts.
"""
import copy


def tool_call(name, **args):
    return {"type": "tool_call", "name": name, "args": args}


def say(text):
    return {"type": "say", "text": text}


def final(text):
    return {"type": "final", "text": text}


def repeat(action):
    """A script step that returns the same action forever (a spinning model)."""
    def step(history):
        return copy.deepcopy(action)
    return step


def always_say(text):
    """A script step that rambles forever without ever acting or finishing."""
    def step(history):
        return say(text)
    return step


class ScriptedModel:
    """Deterministic fake model: plays back a fixed script of actions.

    Each script item is either an action dict or a callable(history)->action.
    When the script runs out, the model declares the task finished, so a
    script can never hang the loop by itself. One exception: if the LAST
    remaining step is callable, it is treated as the model's standing
    policy and is not consumed -- that is how repeat() and always_say()
    simulate a model that spins or rambles forever.
    """

    def __init__(self, script, name="scripted"):
        self._script = list(script)
        self.name = name
        self.calls = 0

    def respond(self, history, tool_names):
        self.calls += 1
        if not self._script:
            return final("[script exhausted]")
        if len(self._script) == 1 and callable(self._script[0]):
            return self._script[0](history)  # standing policy: not consumed
        step = self._script.pop(0)
        if callable(step):
            return step(history)
        return copy.deepcopy(step)
