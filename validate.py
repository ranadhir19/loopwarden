#!/usr/bin/env python3
"""loopwarden repo harness: structural checks + every lab's tests +
the capstone grader. Exit 0 only when everything passes.

    python3 validate.py
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
LABS = [
    "labs/lab00_baseline",
    "labs/lab01_tool_registry",
    "labs/lab02_model_layer",
    "labs/lab03_context_management",
    "labs/lab04_guardrails",
    "labs/lab05_verify",
    "capstone",
]


def structural_checks():
    problems = []
    for rel in ["README.md", "LICENSE", "NAME_CHECK.md"]:
        if not os.path.isfile(os.path.join(ROOT, rel)):
            problems.append(f"missing {rel}")
    for lab in LABS:
        d = os.path.join(ROOT, lab)
        for needed in ["README.md", "tests.py"]:
            if not os.path.isfile(os.path.join(d, needed)):
                problems.append(f"{lab}: missing {needed}")
        if lab != "capstone":
            for needed in ["starter.py", "solution.py"]:
                if not os.path.isfile(os.path.join(d, needed)):
                    problems.append(f"{lab}: missing {needed}")
        else:
            for needed in ["harness.py", "run_eval.py", "eval_cases.json", "scripts.py"]:
                if not os.path.isfile(os.path.join(d, needed)):
                    problems.append(f"{lab}: missing {needed}")
    return problems


def run(cmd, cwd):
    proc = subprocess.run([sys.executable] + cmd, cwd=cwd,
                          capture_output=True, text=True, timeout=300)
    return proc.returncode, (proc.stdout + proc.stderr)


def main():
    failures = []
    print("== structural checks ==")
    problems = structural_checks()
    if problems:
        for p in problems:
            print("  MISSING:", p)
        failures.extend(problems)
    else:
        print("  all required files present")

    print("\n== lab test suites ==")
    for lab in LABS:
        rc, out = run([os.path.join(ROOT, lab, "tests.py")], ROOT)
        last = [ln for ln in out.strip().splitlines() if ln.strip()]
        verdict = "OK" if rc == 0 else "FAILED"
        print(f"  [{verdict}] {lab} ({last[-1] if last else 'no output'})")
        if rc != 0:
            failures.append(lab)
            print(out)

    print("\n== capstone grader ==")
    rc, out = run([os.path.join(ROOT, "capstone", "run_eval.py")], ROOT)
    for ln in out.strip().splitlines():
        print("  " + ln)
    if rc != 0:
        failures.append("capstone grader")

    print("\n== summary ==")
    if failures:
        print(f"FAIL: {len(failures)} problem(s): {failures}")
        return 1
    print(f"PASS: structure OK, {len(LABS)} test suites green, capstone standard met.")
    print("Coverage (honest): unit-level checks of the six harness components "
          "plus the 9-case capstone eval. No network, no real-model behaviour, "
          "no performance claims are tested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
