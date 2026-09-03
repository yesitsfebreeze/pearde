"""`quiet check` — two Bash shapes that pay for nothing, denied before they run.

An idle poll (`echo tick`, `sleep 5; echo waiting`, `true`) re-sends the whole
window to pass time: 1,078 turns and 145M context tokens on 2026-09-03. A
`cat` of a whole file over 8 KB pins its bytes in the window for every later
turn. Both have a cheaper spelling, and the deny names it.

Stdlib only, imports nothing from the planner, and `check` never raises —
@resources/guard.py calls it on every Bash tool call, and a hook that raises
is a session that cannot use a tool."""
import glob
import os
import re
import shlex

BIG = 8192
IDLE = re.compile(r"\s*(sleep\s+\d+\s*;?\s*)?(echo\s*[^|&;>]*|true|:)\s*")
SLEEP = re.compile(r"\s*sleep\s+\d+\s*$")
# the whole line is `cat` and its arguments: no pipe, chain, heredoc or redirect
CAT = re.compile(r"\s*cat\s+([^|;&<>]+)$")

IDLE_WHY = ("Idle polls burn the whole window per turn (1,078 turns / 145M "
            "tokens on 2026-09-03). Hold with the `Monitor` tool on the report "
            "file or transcript you are waiting for, or return `MORE` and let "
            "a fresh window continue. Never `echo`/`sleep`/`true` to pass time.")


def big_files(args, cwd):
    """The existing files among `args` (globs expanded, relative to `cwd`)
    that are over BIG bytes, as (path, size) pairs."""
    out = []
    for a in args:
        if a.startswith("-"):
            continue
        p = a if os.path.isabs(a) else os.path.join(cwd or ".", a)
        for f in (glob.glob(p) if glob.has_magic(p) else [p]):
            if os.path.isfile(f) and os.path.getsize(f) > BIG:
                out.append((a if not glob.has_magic(p) else f, os.path.getsize(f)))
    return out


def check(cmd, cwd):
    """A deny reason for `cmd`, or None."""
    try:
        if IDLE.fullmatch(cmd) or SLEEP.match(cmd):
            return IDLE_WHY
        m = CAT.fullmatch(cmd.strip())
        if not m:
            return None
        big = big_files(shlex.split(m.group(1)), cwd)
        if not big:
            return None
        kb = sum(s for _, s in big) // 1024
        return (f"`cat` of a {kb} KB file pins ~{kb // 4}K tokens in this "
                "window for every later turn. Read the part you need: "
                "`sed -n 'a,bp'`, `grep -n`, `Read` with offset/limit, or a "
                "`pearde` verb for the one PRD. Files: "
                + ", ".join(f"{p} ({s // 1024} KB)" for p, s in big))
    except Exception:
        return None


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    assert check("echo tick", here) and check("sleep 5; echo waiting", here)
    assert check("true", here) and check("sleep 3", here)
    assert check("echo ok | head -1", here) is None
    assert check("cat init.py", here) and check("cat -n collect.py", here)
    assert check("cat init.py | head", here) is None
    assert check("cat > /tmp/x <<'EOF'", here) is None
    assert check("cat nope.py", here) is None and check("ls", here) is None
    print("quiet ok")
