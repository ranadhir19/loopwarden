"""Lab 00 starter: a bare agent loop with NO harness.

This is deliberately naive -- it is the "before" picture. It dispatches
whatever the model asks for, validates nothing, limits nothing, and trusts
the model's final message. Your job in this lab is only to RUN it, watch it
fail, and write down which missing harness component allowed each failure.

Do not fix this file. The fixes are Labs 01-05.
"""
import os


def make_raw_tools(root):
    """Raw tool functions: no schemas, no permissions, no jail."""
    def read_file(path):
        with open(os.path.join(root, path), encoding="utf-8") as fh:
            return fh.read()

    def write_file(path, content):
        with open(os.path.join(root, path), "w", encoding="utf-8") as fh:
            fh.write(content)
        return "written"

    return {"read_file": read_file, "write_file": write_file}


def run_bare_agent(model, root, task, demo_step_cap=30):
    """A bare Think -> Act -> Observe loop.

    demo_step_cap exists ONLY so this teaching demo terminates. A real bare
    loop has no cap at all: it runs (and bills) until the model stops.
    Returns (status, answer, steps_taken).
    """
    tools = make_raw_tools(root)
    history = [{"role": "user", "content": task}]
    steps = 0
    while steps < demo_step_cap:
        steps += 1
        action = model.respond(history, sorted(tools))
        if action.get("type") == "final":
            return "model_claimed_done", action.get("text", ""), steps
        if action.get("type") == "say":
            history.append({"role": "assistant", "content": action.get("text", "")})
            continue
        if action.get("type") == "tool_call":
            fn = tools[action["name"]]            # KeyError if name is wrong
            result = fn(**action.get("args", {}))  # no validation of args
            history.append({"role": "tool", "content": str(result)})
            continue
    return "demo_cap_reached", None, steps
