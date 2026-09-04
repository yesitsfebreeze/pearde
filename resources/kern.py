#!/usr/bin/env python3
"""kern memory, wired into the loop — recall before a turn, capture after it.

    kern.py recall    UserPromptSubmit — what this project already knows about
                      the prompt, printed so it enters the turn's context
    kern.py capture   Stop — the turn's transcript delta, spooled to
                      `<repo>/.kern/intake/` for the daemon to distill
    kern.py drain     SessionStart — make sure something serves this project,
                      so a spooled delta becomes memory instead of a file
    kern.py check     what this board's memory holds and owes, on demand

kern (`kern` on PATH) keeps one knowledge graph per directory and ships no
session hook of its own: the drop dir is the seam, and the caller writes it.
This is that caller. @references/knowledge.md holds the other memory — the
knowledge layer is what the board researched, kern is what the sessions said.

Every path is fail-open and silent. No `kern` on PATH, no `.kern/` in the
tree, a query that answers nothing, a daemon that will not start: exit 0,
print nothing. A memory that is not there must never cost a session.

The machine-wide `kern` plugin captures the same turns into the same spool.
Both writers share `<spool>/.offsets.json`, keyed by session id: whoever runs
first consumes the delta, the other reads `start >= lines` and no-ops. No turn
is captured twice, and neither writer needs to know about the other.

Python 3 stdlib only.
"""
import json
import os
import shutil
import subprocess
import sys

_D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _D if os.path.isfile(os.path.join(_D, "pearde_path.py"))
                else os.path.dirname(_D))

HITS = 99                 # thoughts recalled per prompt
RECALL_TIMEOUT = 4       # seconds — a prompt is not held up for memory
RECALL_CHARS = 2000      # cap on what one recall injects
DRAIN_TIMEOUT = 20       # seconds — spawning a daemon re-loads the store
MIN_PROMPT = 12          # shorter than this recalls nothing worth the call
MAX_SPOOL = 500          # capture files kept before the oldest are dropped


def binary():
    return shutil.which("kern")


def root_of(start):
    """The nearest ancestor of `start` holding a `.kern/` — the project whose
    memory this is. None where no directory on the way up has one: kern is
    opt-in per tree, and a hook must not create a memory nobody asked for."""
    d = os.path.abspath(start or os.getcwd())
    while True:
        if os.path.isdir(os.path.join(d, ".kern")):
            return d
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent


def ready(data):
    """(root, binary) for this hook payload, or (None, None) — the one gate
    every verb passes through."""
    b = binary()
    if not b:
        return None, None
    return root_of(data.get("cwd") or os.getcwd()), b


def run(argv, root, timeout):
    """(stdout, ok). Anything that goes wrong reads as no output."""
    try:
        p = subprocess.run(argv, cwd=root, capture_output=True, text=True,
                           timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return "", False
    return p.stdout, p.returncode == 0


# ── recall ────────────────────────────────────────────────────────────────────
def recall(data):
    root, b = ready(data)
    prompt = (data.get("prompt") or "").strip()
    if not root or len(prompt) < MIN_PROMPT:
        return 0
    out, ok = run([b, "query", prompt, "--k", str(HITS)], root, RECALL_TIMEOUT)
    out = out.strip()
    if not ok or not out or out == "no results":
        return 0
    print("kern memory — what this project already recorded about that:\n"
          + out[:RECALL_CHARS])
    return 0


# ── capture ───────────────────────────────────────────────────────────────────
def delta(lines, offset):
    """(text, consumed) — the user prompts and assistant prose past `offset`.
    Tool calls and tool results are not memory: a `user` block whose content
    is a list is a tool result, and only `text` blocks of an assistant turn
    are the assistant talking."""
    out = []
    for raw in lines[offset:]:
        if not raw.strip():
            continue
        try:
            o = json.loads(raw)
        except ValueError:
            continue
        c = (o.get("message") or {}).get("content")
        if o.get("type") == "user" and isinstance(c, str) and c.strip():
            out.append("user: " + c.strip())
        elif o.get("type") == "assistant" and isinstance(c, list):
            for blk in c:
                if isinstance(blk, dict) and blk.get("type") == "text" \
                        and (blk.get("text") or "").strip():
                    out.append("assistant: " + blk["text"].strip())
    return "\n\n".join(out), len(lines)


def offsets(path, write=None):
    """Read the shared offsets file, or write it atomically. The other writer
    of this spool reads the same file, so a half-written one would make it
    re-capture a turn: tmp file, pid-tagged, then a rename."""
    if write is None:
        try:
            with open(path, encoding="utf-8") as fh:
                d = json.load(fh)
            return d if isinstance(d, dict) else {}
        except (OSError, ValueError):
            return {}
    tmp = f"{path}.{os.getpid()}.tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(write, fh)
        os.replace(tmp, path)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass


def evict(spool):
    """Drop the oldest capture files past MAX_SPOOL — an undrained spool must
    not grow without bound across sessions."""
    try:
        names = [n for n in os.listdir(spool) if n.endswith(".txt")]
        if len(names) <= MAX_SPOOL:
            return
        rows = sorted((os.path.getmtime(os.path.join(spool, n)), n)
                      for n in names)
        for _, n in rows[:len(rows) - MAX_SPOOL]:
            os.unlink(os.path.join(spool, n))
    except OSError:
        pass


def capture(data):
    root, _ = ready(data)
    path = data.get("transcript_path")
    session = data.get("session_id")
    if not root or not path or not session or not os.path.isfile(path):
        return 0
    try:
        with open(path, encoding="utf-8", errors="replace") as fh:
            lines = fh.read().split("\n")
    except OSError:
        return 0
    if lines and lines[-1] == "":
        lines.pop()
    spool = os.path.join(root, ".kern", "intake")
    try:
        os.makedirs(spool, exist_ok=True)
    except OSError:
        return 0
    marks = os.path.join(spool, ".offsets.json")
    seen = offsets(marks)
    start = seen.get(session) or 0
    if start >= len(lines):
        return 0
    text, consumed = delta(lines, start)
    if text.strip():
        try:
            with open(os.path.join(spool, f"{session}-{consumed}.txt"), "w",
                      encoding="utf-8") as fh:
                fh.write(text)
        except OSError:
            return 0
    seen[session] = consumed
    offsets(marks, seen)
    evict(spool)
    return 0


# ── drain ─────────────────────────────────────────────────────────────────────
def drain(data):
    """Ask the hub for the endpoint serving this project — it starts a daemon
    where none is, and the daemon is what watches the spool. Idempotent: a
    project already served answers `running` and nothing is spawned. The root
    is passed absolute; `.` resolves somewhere else."""
    root, b = ready(data)
    if not root:
        return 0
    run([b, "hub", "resolve", root], root, DRAIN_TIMEOUT)
    return 0


# ── check ─────────────────────────────────────────────────────────────────────
ROW = "  %-11s %-7s %s"          # doctor.sh's row(), byte for byte


def check(data):
    b = binary()
    if not b:
        print(ROW % ("kern", "off", "no `kern` on PATH — the board remembers "
                                    "nothing across sessions"))
        return 1
    root = root_of(data.get("cwd") or os.getcwd())
    if not root:
        print(ROW % ("kern", "off", "no .kern/ above " + os.getcwd()
                     + " — `mkdir .kern` opts this tree in"))
        return 1
    status, _ = run([b, "status"], root, RECALL_TIMEOUT)
    serving = "daemon       serving" in status
    intake, _ = run([b, "intake", "status"], root, RECALL_TIMEOUT)
    head = intake.strip().split("\n")[0] if intake.strip() else "intake unknown"
    print(ROW % ("kern", "ok" if serving else "broken",
                 f"{root}/.kern · " + ("served" if serving else "NOT served")))
    print(ROW % ("", "", head))
    if not serving:
        print(ROW % ("", "", "fix: kern hub resolve " + root
                     + "  (the SessionStart hook does this)"))
        return 2
    return 0


VERBS = {"recall": recall, "capture": capture, "drain": drain, "check": check}


def command(args):
    """kern memory — recall before a turn, capture after it, drain the spool"""
    verb = args[0] if args else "check"
    if verb not in VERBS:
        print("pearde kern {recall|capture|drain|check}", file=sys.stderr)
        return 1
    data = {}
    if verb != "check" and not sys.stdin.isatty():
        try:
            data = json.loads(sys.stdin.read() or "{}")
        except ValueError:
            data = {}
    if not isinstance(data, dict):
        data = {}
    try:
        return VERBS[verb](data)
    except Exception:                       # a memory never costs a session
        return 0


command.flags = "recall | capture | drain | check"
COMMANDS = {"kern": command}


def demo():
    """One runnable check of the only non-trivial logic here: the delta walk
    and the shared offset that stops a second writer re-capturing a turn."""
    lines = [
        json.dumps({"type": "user", "message": {"content": "why is it red?"}}),
        json.dumps({"type": "assistant", "message": {"content": [
            {"type": "thinking", "thinking": "hmm"},
            {"type": "text", "text": "the probe never ran"}]}}),
        json.dumps({"type": "user", "message": {"content": [
            {"type": "tool_result", "content": "ok"}]}}),
        "",
    ]
    text, consumed = delta(lines, 0)
    assert text == "user: why is it red?\n\nassistant: the probe never ran", text
    assert consumed == 4, consumed
    assert delta(lines, consumed) == ("", 4)      # nothing left for the second writer
    assert delta(lines, 1)[0] == "assistant: the probe never ran"
    assert delta(["{bad json"], 0) == ("", 1)     # a torn line is skipped, not fatal
    print("ok")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "demo":
        sys.exit(demo())
    sys.exit(command(sys.argv[1:]))
