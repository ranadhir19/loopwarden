"""Tool Registry: named tools with schemas, permission classes, path jailing.

Permission classes:
  read    - observes the world, changes nothing
  write   - creates or modifies files inside the workspace
  execute - runs a computation (no direct file access)
"""
import ast
import os


class ToolError(Exception):
    """Raised for every tool problem; the loop turns it into an observation."""


_TYPE_CHECKS = {
    "str": lambda v: isinstance(v, str),
    "int": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "float": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "bool": lambda v: isinstance(v, bool),
}


class Tool:
    def __init__(self, name, description, permission, schema, handler):
        if permission not in ("read", "write", "execute"):
            raise ValueError("permission must be read, write or execute")
        self.name = name
        self.description = description
        self.permission = permission
        self.schema = schema  # {arg_name: type_name}; all listed args required
        self.handler = handler


class ToolRegistry:
    def __init__(self):
        self._tools = {}

    def register(self, tool):
        if tool.name in self._tools:
            raise ToolError("duplicate tool: " + tool.name)
        self._tools[tool.name] = tool
        return tool

    def names(self):
        return sorted(self._tools)

    def describe(self):
        lines = []
        for name in self.names():
            t = self._tools[name]
            args = ", ".join(f"{k}: {v}" for k, v in t.schema.items())
            lines.append(f"{t.name}({args}) [{t.permission}] - {t.description}")
        return "\n".join(lines)

    def call(self, name, args):
        if name not in self._tools:
            raise ToolError(f"unknown tool: {name!r}. Available: {', '.join(self.names())}")
        tool = self._tools[name]
        args = dict(args or {})
        for arg, type_name in tool.schema.items():
            if arg not in args:
                raise ToolError(f"tool {name}: missing required argument {arg!r}")
            if not _TYPE_CHECKS[type_name](args[arg]):
                raise ToolError(
                    f"tool {name}: argument {arg!r} must be {type_name}, "
                    f"got {type(args[arg]).__name__}")
        extra = set(args) - set(tool.schema)
        if extra:
            raise ToolError(f"tool {name}: unexpected arguments {sorted(extra)}")
        return tool.handler(**args)


def jailed_path(root, rel):
    """Resolve rel inside root; refuse anything that escapes the jail."""
    root_abs = os.path.realpath(root)
    target = os.path.realpath(os.path.join(root_abs, rel))
    if target != root_abs and not target.startswith(root_abs + os.sep):
        raise ToolError(f"path escapes workspace: {rel!r}")
    return target


def _safe_eval(expr):
    """Evaluate an arithmetic expression without eval(): walk the AST."""
    ops = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b,
           ast.Mult: lambda a, b: a * b, ast.Div: lambda a, b: a / b,
           ast.Mod: lambda a, b: a % b, ast.USub: lambda a: -a}

    def walk(node):
        if isinstance(node, ast.Expression):
            return walk(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        if isinstance(node, ast.BinOp) and type(node.op) in ops:
            return ops[type(node.op)](walk(node.left), walk(node.right))
        if isinstance(node, ast.UnaryOp) and type(node.op) in ops:
            return ops[type(node.op)](walk(node.operand))
        raise ToolError("expression not allowed")

    return walk(ast.parse(expr, mode="eval"))


def make_workspace_tools(root):
    """The standard file tools over a workspace directory, fully jailed."""
    os.makedirs(root, exist_ok=True)
    reg = ToolRegistry()

    def list_dir(path="."):
        base = jailed_path(root, path)
        if not os.path.isdir(base):
            raise ToolError(f"not a directory: {path!r}")
        return "\n".join(sorted(os.listdir(base)))

    def read_file(path):
        target = jailed_path(root, path)
        if not os.path.isfile(target):
            raise ToolError(f"no such file: {path!r}")
        with open(target, encoding="utf-8") as fh:
            return fh.read()

    def write_file(path, content):
        target = jailed_path(root, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(content)
        return f"wrote {len(content)} chars to {path}"

    def append_file(path, content):
        target = jailed_path(root, path)
        with open(target, "a", encoding="utf-8") as fh:
            fh.write(content)
        return f"appended {len(content)} chars to {path}"

    def eval_expr(expr):
        return str(_safe_eval(expr))

    reg.register(Tool("list_dir", "List files in a workspace directory",
                      "read", {"path": "str"}, list_dir))
    reg.register(Tool("read_file", "Read a UTF-8 text file in the workspace",
                      "read", {"path": "str"}, read_file))
    reg.register(Tool("write_file", "Write (overwrite) a text file in the workspace",
                      "write", {"path": "str", "content": "str"}, write_file))
    reg.register(Tool("append_file", "Append text to a file in the workspace",
                      "write", {"path": "str", "content": "str"}, append_file))
    reg.register(Tool("eval_expr", "Evaluate a safe arithmetic expression",
                      "execute", {"expr": "str"}, eval_expr))
    return reg
