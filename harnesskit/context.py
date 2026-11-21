"""Context management: keep the model's view of the world inside a budget.

Strategy (deliberately simple and deterministic):
  * The first `pinned` history entries (system + task) are never dropped.
  * The most recent entries are kept verbatim, newest last.
  * Everything in between is compacted into one summary entry. The summary
    keeps the first line of each dropped entry, so planted facts that a tool
    put at the top of its result (e.g. "TOTAL_WORDS: 5") survive compaction.
"""
import copy


def estimate_chars(history):
    return sum(len(m.get("content", "")) for m in history)


class ContextManager:
    def __init__(self, budget_chars=4000, pinned=2, keep_recent=4):
        self.budget_chars = budget_chars
        self.pinned = pinned
        self.keep_recent = keep_recent
        self.compactions = 0

    def build(self, history):
        """Return the history the model should see for this turn."""
        history = [dict(m) for m in history]
        if estimate_chars(history) <= self.budget_chars:
            return history
        head = history[: self.pinned]
        tail = history[-self.keep_recent:] if self.keep_recent else []
        middle = history[self.pinned: len(history) - len(tail)] if tail else history[self.pinned:]
        if not middle:
            return head + tail
        digest = []
        for m in middle:
            first_line = m.get("content", "").split("\n", 1)[0].strip()
            if first_line:
                digest.append(f"- [{m.get('role', '?')}] {first_line[:100]}")
        summary = {"role": "system",
                   "content": "[compacted %d earlier messages]\n%s"
                              % (len(middle), "\n".join(digest))}
        self.compactions += 1
        result = head + [summary] + tail
        # If even head+summary+tail is over budget, shrink the digest.
        while estimate_chars(result) > self.budget_chars and len(digest) > 1:
            digest.pop()  # drop the newest digested lines; earliest facts stay
            summary["content"] = ("[compacted %d earlier messages]\n%s"
                                   % (len(middle), "\n".join(digest)))
            result = head + [summary] + tail
        return result
