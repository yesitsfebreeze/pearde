#!/bin/bash
# probe harness — an-acceptance-box-that-cannot-fail-is-refused
# The analyzer in resources/board/specs.py refuses a Verify block that cannot
# exit non-zero, judged under the exact runner collect uses: `bash -e
# -o pipefail`. Fixtures are unit cases; the differential runs the classifier
# and real bash side by side — a refused script that bash exits non-zero on
# is a false refusal and fails the run; the gate fixture pins the specced
# refusal end to end.
# The tree under test is the runner's when it names one. A worker builds in a
# lane worktree at <board>/.lanes/<slug>, which holds no board of its own, so a
# walk up from $0 always lands in the orchestrator's checkout and a green box
# proves a tree holding none of the work. BOARD is the `.pearde` this harness
# sits under, found by walking, so no count of `..` has to match the PRD's
# nesting depth; ROOT is PEARDE_ROOT when the runner set one, that board's repo
# otherwise.
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ] && [ "$(basename "$BOARD")" != pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
D="$HERE"
pass=0; fail=0
ok() { if [ "$2" = "0" ]; then pass=$((pass+1)); else fail=$((fail+1)); echo "FAIL: $1"; fi; }

REPO="$ROOT"
python3 - "$D/analyzer.py" "$REPO/resources/board/specs.py" <<'PYEND'
import sys, importlib.util, subprocess, random, os
spec = importlib.util.spec_from_file_location("probe", sys.argv[1])
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
probe = importlib.util.spec_from_file_location("specs", sys.argv[2])
lib = importlib.util.module_from_spec(probe)
probe.loader.exec_module(lib)

fails = []
CASES = [
    ("echo done", True), ("true", True), (":", True),
    ("grep -q foo f\necho ok", False),
    ("grep -q foo f || true\necho ok", True),
    ("test -f x || true\necho ok", True),
    ("! test -f x\necho ok", True),
    ("run.sh && echo ok || true\necho done", True),
    ("run.sh || die\necho done", False),
    ("x=$(false)\necho ok", False),
    ("x=1\necho ok", True),
    ("x=$(false)\n", False),
    ("grep -q p f && echo found || true\necho done", True),
    ("python3 check.py || echo skip\necho ok", True),
    ("cat f | wc -l\necho ok", False),
    ("set -e\necho ok", True),
    ("cd $D\necho ok", False),
    ("ok() { echo hi; }\nok", False),
    ("exit 0\necho ok", True), ("exit 0", True), ("exit 1", False),
    ("test -f f || exit 1\necho ok", False),
    ("test -f f || exit 0\necho ok", True),
    ("[ -f f ] || echo missing\necho done", True),
    ("grep -q p f # nope\necho ok", False),
    ("[[ -f f ]]\necho ok", False),
    ("echo a; grep -q p f; echo c", False),
    ("x=$(grep p f)\necho done", False),
    ("grep -q p f || :\necho ok", True),
    ("grep -q p f && echo y\necho n", True),
    ("false && true\necho ok", True),
    ("false && true", False),
    ("test -f f && echo yes", False),
    ("x=$(false) || echo no\necho ok", True),
    ("python3 check.py || true\necho done", True),
    ("set +e\nfalse\necho ok\n", None),
    ("echo done\ngrep -q p f || true\n", True),
    ("test -f f && while read -r l; do :; done < /dev/null\n", False),
]
for sc, want in CASES:
    got = mod._cannot_fail_why(sc) is not None
    if want is None:
        continue
    if got and want is False:
        r = subprocess.run(["bash", "-e", "-o", "pipefail"], input=sc,
                           capture_output=True, text=True, cwd="/tmp")
        print("     case", repr(sc), "refused; bash exit", r.returncode)
        if r.returncode == 0:
            fails.append("false refusal: %r" % sc)
    if want is True and not got:
        r = subprocess.run(["bash", "-e", "-o", "pipefail"], input=sc,
                           capture_output=True, text=True, cwd="/tmp")
        if r.returncode == 0:
            fails.append("lost refusal: %r" % sc)

random.seed(160)
CMDS = ["grep -q p /dev/null || true", "test -d /tmp || true", "echo step",
        "x=1", "true", ":", "x=$(false) || echo no", "! true",
        "while read -r l; do :; done < /dev/null", "[ -f f ] || true",
        "printf ok", "test -f f && echo y || true",
        "python3 -c 'import sys; sys.exit(0)'",
        "ls /tmp >/dev/null 2>&1 || true", "exit 1 || true", "cd /tmp",
        "diff /etc/hostname /etc/hostname || true",
        "if test -f f; then :; fi", "( false ); true", "false"]
for _ in range(400):
    n = random.randint(1, 3)
    lines = []
    for _ in range(n):
        parts = [random.choice(CMDS) for _ in range(random.randint(1, 3))]
        s = parts[0]
        for k in range(1, len(parts)):
            s += " " + random.choice(["&&", "||", ";", "|"]) + " " + parts[k]
        lines.append(s)
    script = "\n".join(lines) + random.choice(
        ["", "\necho ok", "; echo done", " || true"])
    if lib._cannot_fail_why(script + "\n") is None:
        continue
    r = subprocess.run(["bash", "-e", "-o", "pipefail"], input=script,
                       capture_output=True, text=True, cwd="/tmp")
    if r.returncode != 0:
        fails.append("false refusal: %r exit %d" % (script, r.returncode))

print("case suite + differential done; violations:", len(fails))
for f in fails:
    print("  " + f)
raise SystemExit(1 if fails else 0)
PYEND
ok "case suite and differential" $?

T="$(mktemp -d)"
trap 'rm -rf "$T"' EXIT
cat > "$T/spec01.md" <<'SPEC'
---
complexity: 5
footprint:
  - resources/board/specs.py
---
# spec01 — probe

One unit.

## Acceptance

- [ ] a check that can fail

## Verify and Proof

```sh
test -f prd.md || true
echo done
```
SPEC
python3 - "$T" <<'PYEND'
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "resources", "board"))
import specs
t = sys.argv[1]
path = os.path.join(t, "spec01.md")
text = open(path, encoding="utf-8").read()
fm, _, _ = specs.plan.parse_prd(path)
b, w, fp = specs.check_spec(path, fm, text, {}, [])
assert any("cannot fail" in m for _, m in b), b
new = text.replace("test -f prd.md || true\necho done",
                   "python3 -c 'import sys; sys.exit(1)'; echo spec01-red")
b, w, fp = specs.check_spec(path, fm, new, {}, [])
assert not any("cannot fail" in m for _, m in b), b
print("gate: cannot-fail refused, live accepted")
raise SystemExit(0)
PYEND
ok "check_spec gate refuses cannot-fail, accepts live" $?

echo
echo "verify: $pass passed, $fail failed"
[ "$fail" = "0" ]