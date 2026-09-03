#!/usr/bin/env bash
# no-destructive-git-runs-in-a-tree-the-session-does-not-own — the verify
# command of the memo of the same name. Run from the repo root:
#
#     bash resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh
#
# Exit 0 while the invariant holds, 1 the moment it does not.
#
# The invariant: `git reset --hard`, `checkout --`, `clean` and a real `stash`
# are refused in any tree the running session does not own. The shell half is
# @resources/guard.py's `PreToolUse` hook and it needs no check here — it asks
# @resources/board/refuse.py about every Bash line there is. The half that
# regresses silently is the board's OWN code: `refuse.py` guards the call
# sites that ask it, and a call site that does not ask is caught by nothing.
# That is the exact shape of the loss the memo records — one `reset --hard`
# inside `collect`'s `unland`, in a checkout three sessions shared.
#
# So this reads the board's Python for a destructive git that is not gated,
# and fails naming the file and the line. Three shapes are accepted:
#
#   - a call inside a function that also asks the guard — `_may_discard(…)`,
#     `refuse.guard(…)`, `refuse.allowed(…)`, `refuse.check_line(…)`;
#   - `collect.py`'s `_park` / `guarded_run` stash-then-POP pair, whose whole
#     purpose is to move a PEER's dirt out of a verify block's reach and put
#     it back — putting it under the refusal was measured and it destroyed
#     exactly the work the refusal exists to protect. The exemption is spent
#     only while the recorded reason is still in the file: delete the comment
#     and this goes red;
#   - anything the reader's own table says cannot discard — `stash create`,
#     `clean -n`, `reset --keep`, `restore --staged`, a plain
#     `checkout <branch>`. `session.py`'s reaper is green by this rule and by
#     construction: it snapshots through `write-tree` / `commit-tree` and
#     spells no stash at all.
#
# The table is `refuse.py`'s own `SPELLINGS`, read from the tree being
# scanned, so the check and the mechanism can never drift into two answers —
# and deleting `refuse.py` fails this outright.
#
# The tree to scan is `$1`, defaulting to the working directory, and NOT
# `PEARDE_ROOT`: the injection proof below runs from a scratch copy while
# `PEARDE_ROOT` still names the real tree, and a root read from the
# environment would quietly scan the wrong one and pass.
#
# It can fail, and the way to prove that is not to trust this comment:
#
#     T=$(mktemp -d); cp -R resources "$T/resources"
#     printf '\nimport subprocess\nsubprocess.run(["git","reset","--hard"])\n' \
#       >> "$T/resources/board/orphans.py"
#     ( cd "$T" && bash resources/invariants/<this>.sh )   # exits 1
#
# A scanner that has stopped matching passes everything, so two self-tests run
# before the tree does: one synthetic module that MUST be flagged and one that
# must not. A broken reader fails here rather than reading green over a tree
# full of faults.
set -u

ROOT=${1:-$PWD}
# `refuse.py` found by the one rule — resources/ first, then every
# directory directly under it — so the module can move and this harness
# needs no second edit. @resources/pearde_path.py `script()` is the
# Python half of the same rule; this is the smallest shell that holds it,
# and it searches the tree being MEASURED, not the one this file sits in.
REFUSE=$(ls "$ROOT"/resources/refuse.py "$ROOT"/resources/*/refuse.py \
         2>/dev/null | head -1)
exec python3 - "$ROOT" "$REFUSE" <<'PY'
import ast
import importlib.util
import os
import sys

root = os.path.abspath(sys.argv[1])
FAIL = []


def no(msg):
    print("FAIL  " + msg)
    FAIL.append(msg)


def ok(msg):
    print("PASS  " + msg)


refuse_path = sys.argv[2] if len(sys.argv) > 2 else ""
if not refuse_path or not os.path.isfile(refuse_path):
    no("no refuse.py anywhere under %s/resources — the reader the whole "
       "mechanism is built on is gone" % root)
    sys.exit(1)
spec = importlib.util.spec_from_file_location("_refuse_invariant", refuse_path)
refuse = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(refuse)
except Exception as e:                                   # noqa: BLE001
    no("%s will not import: %s" % (refuse_path, e))
    sys.exit(1)

# the two call shapes the board writes a git in
RUNNERS = ("run", "Popen", "check_output", "check_call", "call")
HELPERS = ("git", "git_out", "gitq", "_git", "run_git")
# a function holding one of these has asked who owns the tree
GUARDS = ("_may_discard", "refuse.guard", "refuselib.guard",
          "refuse.allowed", "refuselib.allowed",
          "refuse.check_line", "refuselib.check_line")
# (file, function) -> the recorded reason that has to still be in the file.
# An exemption whose reason is gone is a finding, not an exemption.
EXEMPT = {
    ("resources/board/collect.py", "_park"): "stash-then-POP",
    ("resources/board/collect.py", "guarded_run"): "stash-then-POP",
}

HOLE = "\0"          # a non-literal argument: present, unreadable


def _elems(nodes):
    out = []
    for n in nodes:
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            out.append(n.value)
        else:
            out.append(HOLE)
    return out


def _flat(node):
    """One argv list, flattened through `+`. `["git", …] + paths` is how
    `collect._park` spells its stash and the shape this missed on its first
    run — the bait below keeps it caught."""
    if isinstance(node, (ast.List, ast.Tuple)):
        return _elems(node.elts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _flat(node.left), _flat(node.right)
        if left is None or right is None:
            return None
        return left + right
    return [HOLE]


def _argv(call):
    """The git arguments this call runs, or None when it runs no git."""
    f = call.func
    name = f.attr if isinstance(f, ast.Attribute) else \
        (f.id if isinstance(f, ast.Name) else "")
    if name in RUNNERS and call.args:
        e = _flat(call.args[0])
        if e and os.path.basename(e[0]) == "git":
            return e[1:]
        return None
    if name in HELPERS and len(call.args) >= 2:
        return _elems(call.args[1:])
    return None


def sites(src, where):
    """Every destructive git in one module: (line, verb, why, function)."""
    tree = ast.parse(src, filename=where)
    fn = {}
    for parent in ast.walk(tree):
        for child in ast.iter_child_nodes(parent):
            fn[child] = parent
    found = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        argv = _argv(node)
        if argv is None:
            continue
        verb, args, _at = refuse.verb_of(argv)
        row = refuse.SPELLINGS.get(verb)
        if not row or not row[0](args):
            continue
        up, name = fn.get(node), None
        while up is not None:
            if isinstance(up, (ast.FunctionDef, ast.AsyncFunctionDef)):
                name = up.name
                break
            up = fn.get(up)
        found.append((node.lineno, verb, row[1], name, up))
    return found


def gated(src, holder):
    if holder is None:
        return False
    body = "\n".join(src.splitlines()[holder.lineno - 1:holder.end_lineno])
    return any(g in body for g in GUARDS)


# ── the reader reads: a scanner that matches nothing passes everything ───────
BAIT = ('import subprocess\n'
        'def f():\n'
        '    subprocess.run(["git", "-C", d, "reset", "--hard"])\n'
        '    subprocess.run(["git", "-C", d, "clean", "-fdx", "--"] + paths)\n'
        '    git(wt, "stash", "push", "-u")\n')
SAFE = ('import subprocess\n'
        'def f():\n'
        '    subprocess.run(["git", "-C", d, "reset", "--keep"])\n'
        '    subprocess.run(["git", "stash", "create"])\n'
        '    git(d, "checkout", branch)\n')
hit = sites(BAIT, "<bait>")
if [h[1] for h in hit] == ["reset", "clean", "stash"]:
    ok("the reader sees an ungated `reset --hard`, a `clean` spelled with a "
       "concatenated pathspec, and a real `stash`, in a synthetic module")
else:
    no("the reader saw %r in a module holding a reset --hard, a clean and a "
       "stash — it has stopped matching, and every result below is worthless"
       % ([h[1] for h in hit],))
miss = sites(SAFE, "<safe>")
if not miss:
    ok("and reads `reset --keep`, `stash create` and a plain `checkout` as "
       "discarding nothing")
else:
    no("the reader called %d spelling(s) destructive that discard nothing: %s"
       % (len(miss), ", ".join(m[1] for m in miss)))

# ── the tree ─────────────────────────────────────────────────────────────────
base = os.path.join(root, "resources")
if not os.path.isdir(base):
    no("no resources/ under %s — nothing to read" % root)
    sys.exit(1)

files, problems, accepted = [], [], []
for d, dirs, names in os.walk(base):
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    for n in sorted(names):
        if n.endswith(".py"):
            files.append(os.path.join(d, n))
for path in sorted(files):
    rel = os.path.relpath(path, root)
    src = open(path, encoding="utf-8", errors="replace").read()
    try:
        found = sites(src, rel)
    except SyntaxError as e:
        problems.append("%s:%s — will not parse: %s" % (rel, e.lineno, e.msg))
        continue
    for line, verb, why, name, holder in found:
        key = (rel, name)
        if key in EXEMPT:
            reason = EXEMPT[key]
            if reason in src:
                accepted.append("%s:%d — git %s in `%s`, exempt while its "
                                "recorded reason (%r) stands"
                                % (rel, line, verb, name, reason))
            else:
                problems.append("%s:%d — git %s in `%s` is exempt only while "
                                "the reason %r is written above it, and it is "
                                "gone" % (rel, line, verb, name, reason))
            continue
        if gated(src, holder):
            accepted.append("%s:%d — git %s in `%s`, gated" % (rel, line,
                                                               verb, name))
            continue
        problems.append("%s:%d — git %s is not gated: %s. Ask "
                        "@resources/board/refuse.py before it runs"
                        % (rel, line, verb, why))

for a in accepted:
    ok(a)
if problems:
    for p in problems:
        no(p)
else:
    ok("%d Python file(s) under resources/ hold no ungated destructive git"
       % len(files))

if FAIL:
    print("\n%d problem(s) — the invariant is broken." % len(FAIL))
    sys.exit(1)
sys.exit(0)
PY
