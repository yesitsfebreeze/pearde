#!/usr/bin/env python3
"""Fixture probe for `the-budget-ceiling-counts-the-session-it-stops`.

Builds a throwaway board with `context-budget: 50k` and a fake transcript
already over that cap, then feeds resources/guard.py real PreToolUse
payloads shaped like an orchestrator's own call (no agent_id/agent_type)
and like a dispatched worker's call (agent_id + agent_type present, exactly
as observed on this board's own live hook payloads — see the PRD report).
Never touches this repo's own `.pearde/settings.md`.
"""
import json
import os
import subprocess
import sys
import tempfile

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
GUARD = os.path.join(REPO, "resources", "guard.py")

fails = []
ran = []


def check(name, cond):
    ran.append(name)
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        fails.append(name)


def main():
    fixture = tempfile.mkdtemp(prefix="budget-ceiling-probe-")
    board = os.path.join(fixture, ".pearde")
    os.makedirs(board, exist_ok=True)
    with open(os.path.join(board, "settings.md"), "w") as f:
        f.write("---\nname: fixture\ncontext-budget: 50k\n---\n\n# fixture\n")

    over_cap = os.path.join(fixture, "over_cap.jsonl")
    with open(over_cap, "w") as f:
        f.write(json.dumps({"type": "assistant", "message": {"usage": {
            "input_tokens": 1000, "cache_read_input_tokens": 90000,
            "cache_creation_input_tokens": 0}}}) + "\n")

    warn_75 = os.path.join(fixture, "warn_75.jsonl")
    with open(warn_75, "w") as f:
        f.write(json.dumps({"type": "assistant", "message": {"usage": {
            "input_tokens": 1000, "cache_read_input_tokens": 36500,
            "cache_creation_input_tokens": 0}}}) + "\n")

    env = dict(os.environ)
    env["PEARDE_GUARD_STATE"] = os.path.join(fixture, "guardstate")

    def call(payload):
        base = {"session_id": "shared-session", "cwd": fixture,
                "hook_event_name": "PreToolUse"}
        base.update(payload)
        p = subprocess.run([sys.executable, GUARD, "pre"],
                            input=json.dumps(base), capture_output=True,
                            text=True, env=env)
        return p.stdout.strip()

    worker = {"agent_id": "abc123", "agent_type": "pearde-analyst"}

    # 1. Orchestrator-shaped call, over cap, on its own PRD-ish file — denied.
    out = call({"transcript_path": over_cap, "tool_name": "Bash",
                "tool_input": {"command": "echo hi"}})
    check("orchestrator over cap is denied",
          '"permissionDecision": "deny"' in out and "50k budget" in out)

    # 2. Dispatched-worker-shaped call, same over-cap transcript, same
    #    board, same session_id — NOT denied.
    out = call({"transcript_path": over_cap, "tool_name": "Read",
                "tool_input": {"file_path": os.path.join(fixture, "x.md")},
                **worker})
    check("dispatched worker over cap is not denied", out == "")

    out = call({"transcript_path": over_cap, "tool_name": "Bash",
                "tool_input": {"command": "cat x"}, **worker})
    check("dispatched worker's Bash over cap is not denied", out == "")

    # 3. A dispatched worker over cap is never funneled into writing the
    #    round file — because it is never denied in the first place, it
    #    never sees the deny text that names round.md as the escape.
    round_md = os.path.join(board, ".state", "round.md")
    out = call({"transcript_path": over_cap, "tool_name": "Write",
                "tool_input": {"file_path": round_md, "content": "x"},
                **worker})
    check("dispatched worker writing round.md over cap raises no ceiling deny",
          out == "")

    # 4. The orchestrator itself keeps the escape hatch at the ceiling.
    out = call({"transcript_path": over_cap, "tool_name": "Write",
                "tool_input": {"file_path": round_md, "content": "x"}})
    check("orchestrator's own round.md write at the ceiling stays open",
          out == "")

    # 5. The orchestrator still gets the one-shot 70%/85% notes; a worker at
    #    the same transcript gets nothing.
    out = call({"transcript_path": warn_75, "tool_name": "Bash",
                "tool_input": {"command": "echo hi"}})
    check("orchestrator at 75% gets the warn note",
          "additionalContext" in out and "37k of the 50k budget" in out)

    out = call({"transcript_path": warn_75, "tool_name": "Bash",
                "tool_input": {"command": "echo hi"}, **worker})
    check("dispatched worker at 75% gets no note", out == "")

    sys.path.insert(0, os.path.join(REPO, "resources"))
    import importlib
    guard = importlib.import_module("guard")

    # 6. The signal itself, against the exact payload key sets captured from
    #    this board's own live PreToolUse traffic (orchestrator calls and
    #    dispatched-worker calls, same round, same session_id). These are the
    #    real shapes, not invented ones — the fix is a no-op if they drift.
    live_orchestrator = {
        "cwd": ".", "effort": "high", "hook_event_name": "PreToolUse",
        "permission_mode": "bypassPermissions", "prompt_id": "p",
        "session_id": "2f52d04a-b11d-4874-b08b-122fd4f640cc",
        "tool_input": {}, "tool_name": "Bash", "tool_use_id": "t",
        "transcript_path": "/nope",
    }
    live_worker = dict(live_orchestrator,
                       agent_id="a3a409f905c4945c6",
                       agent_type="pearde-implementer")
    check("live orchestrator payload shape is not dispatched",
          guard.dispatched(live_orchestrator) is False)
    check("live worker payload shape is dispatched",
          guard.dispatched(live_worker) is True)
    check("the two live shapes share one session_id, so it cannot be the signal",
          live_orchestrator["session_id"] == live_worker["session_id"])

    # 7. budget_of() parsing is untouched: off / bare number / k-suffix.
    b_off = os.path.join(fixture, "off"); os.makedirs(b_off, exist_ok=True)
    open(os.path.join(b_off, "settings.md"), "w").write(
        "---\ncontext-budget: off\n---\n")
    b_bare = os.path.join(fixture, "bare"); os.makedirs(b_bare, exist_ok=True)
    open(os.path.join(b_bare, "settings.md"), "w").write(
        "---\ncontext-budget: 42000\n---\n")
    b_k = os.path.join(fixture, "k"); os.makedirs(b_k, exist_ok=True)
    open(os.path.join(b_k, "settings.md"), "w").write(
        "---\ncontext-budget: 160k\n---\n")
    check("budget_of parses off as 0", guard.budget_of(b_off) == 0)
    check("budget_of parses a bare number", guard.budget_of(b_bare) == 42000)
    check("budget_of parses a k suffix", guard.budget_of(b_k) == 160000)

    print()
    if fails:
        print(f"{len(fails)} of {len(ran)} checks failed: {', '.join(fails)}")
        return 1
    print(f"{len(ran)} of {len(ran)} checks pass")
    return 0


if __name__ == "__main__":
    sys.exit(main())
