# GitHub repo brief — loopwarden

**Repo name:** `loopwarden`
(for Ranadhir Ghosh's GitHub, i.e. `ranadhir19/loopwarden`. The name was
collision-checked against existing GitHub repos, PyPI packages and
products — see NAME_CHECK.md. The original working name "harnessforge"
was rejected: it is already used by several projects, including a GitHub
repo + PyPI package of the same name and an EMNLP 2026 paper.)

**About / description (one paragraph):**
A free, offline, hands-on lab for the agentic harness — the engineering
layer around a language model (tool registry, swappable model layer,
context management, guardrails, the agent loop, and verification) that
turns an erratic model into a dependable agent. Six progressive labs plus
a capstone, all in pure Python standard library with a deterministic
scripted model: no API keys, no paid models, no installs. Each lab fixes
one classic failure of a bare agent loop, and the capstone grades an
assembled harness against a frozen 9-case eval set with refusal
(near-miss) cases and a stated pass standard.

**Suggested topics / tags:**
`ai-agents`, `llm`, `agent-harness`, `agentic-ai`, `tutorial`, `lab`,
`hands-on`, `python`, `offline`, `guardrails`, `evaluation`, `tool-use`,
`prompt-engineering` (contrast topic), `education`

**Publish checklist for the parent agent:**
- Create the repo via the browser (connector create returns 403).
- Push the contents of this folder as-is (folder name on disk stays
  `harnessforge/`; the repo is `loopwarden`).
- Run the standing pre-push compliance scan on the exact pushed
  content before the push (done locally at build time; re-run on the
  final tree).
- `python3 validate.py` must exit 0 on the pushed tree (verified locally).
- After the push: YouTube explanation, then LinkedIn post, per the
  standing HOL sequencing rule for any catalog listing.
