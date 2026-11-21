# Lab 01 — Tool Registry: what the agent may touch

## Scope
The first harness component. A registry turns raw functions into governed
tools: each has a name, an argument schema, and a permission class
(read / write / execute). Every file path is jailed inside the workspace,
so `../` escapes and absolute paths are refused before they touch the disk.
Crucially, every problem becomes a `ToolError` — an observation the model
can react to — instead of a crash.

## Learning objectives
- Explain why a tool call must be validated before it is executed.
- Distinguish permission classes and say why they matter for safety review.
- Explain how a path jail works and what it does *not* protect against.

## Hands-on objectives
- Complete `starter.py`: register read/write/execute tools over a folder.
- Break it on purpose: wrong types, missing args, unknown names, escapes.
- Run `python3 tests.py`.

## Exercises
1. Add a `delete_file` tool. Which permission class is it? Should the
   registry allow it at all in a read-only research agent? Justify.
2. Call `write_file` with `path="sub/../a.txt"`. Does the jail allow it?
   Should it? (Check where the resolved path lands.)
3. A model keeps calling `read_file` with an integer path. In the bare loop
   of Lab 00 this crashed. Trace what happens now, end to end.

## What to observe
- Validation errors are *feedback*: they go back into the conversation as
  observations, so a model can recover instead of dying.
- The registry is also documentation: `registry.describe()` is exactly
  what you would show a model (or an auditor) about its powers.

Next: Lab 02 puts the model behind a swappable interface.
