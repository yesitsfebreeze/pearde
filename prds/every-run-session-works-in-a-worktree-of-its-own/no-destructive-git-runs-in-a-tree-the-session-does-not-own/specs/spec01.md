---
complexity: 16
footprint:
  - resources/board/refuse.py
  - resources/guard.py
  - resources/board/lanes.py
  - resources/board/collect.py
---

# spec01 — the refusal, in the board's own code and in a session's own shell

`reset --hard`, `checkout --`, `clean` and a real `stash` are refused in any
tree the running session does not own. One reader answers both halves:
`resources/board/refuse.py` says what discards and who owns a tree, the
board's own destructive call sites ask it before they run, and
`resources/guard.py`'s `PreToolUse` hook asks it of every Bash command a
session types.

**This spec stands.** The probe is green — 29 checks, A1–A10, B1–B6, C1–C4,
D1–D5, E1–E2, F1, G1 — and the harness sweep is byte-identical to its
baseline: 48 failing before and after on the analyst's tree, and re-measured
on 2026-09-02 by the implementer, 51 failing before and the same 51 after,
none reddened and none silently fixed. The two numbers are two trees, four
commits apart, and neither difference is this unit's. What is left is the
review, and the two things the build deliberately did not do, both recorded
below so the next worker does not re-open them.

**Ownership is two rules, and the second is why this is not `session owns`.**
A tree is this session's when the ledger's row for it carries this session's
pid, OR when it is the very worktree the running process is working inside and
no other live session holds it. Rule 2 is load-bearing: a worker runs in a
lane, a lane is on no session ledger, and the ledger alone would refuse a
worker every legitimate `git clean` in its own lane — and refuse a person
their own shell in the main checkout. The harm the memo records is a session
reaching OUT of its tree into a tree another session is writing, and that is
what rule 2 refuses.

**Two things the build did NOT do, and must not be "finished" by adding
them.**

1. `collect._park`'s `git stash push -u` is **not** under the refusal, and the
   comment above it says why in the file. It is a stash-then-POP pair whose
   pop is in `guarded_run`'s `finally`, and whose whole purpose is to move a
   peer's dirt out of the verify block's reach and put it back. Putting it
   under the refusal was tried and measured: four checks of
   `prds/collect-must-not-reset-the-checkout-it-did-not-write` flipped from
   pass to fail, "the neighbour's uncommitted work is still there" stopped
   being true, and six harnesses reddened. A protective stash refused destroys
   exactly the work the refusal exists to protect. The distinction that makes
   this consistent: a `stash` a session TYPES has no matching pop.
2. Everything the guard does is inside one `try`, and a refusal module that
   will not import denies nothing. A `PreToolUse` hook is answered by what it
   prints; a traceback is not a decision and the tool call does not proceed,
   so a raised hook costs the session the tool while a missed refusal costs
   one command. `[[260902-4f91]]` on the record.

## Acceptance

- [x] `resources/board/refuse.py` reads `reset --hard`, `checkout --`,
      `checkout -f`, `clean`, a real `stash`, `restore` and
      `switch --discard-changes` as destructive, and reads `reset --keep`,
      `checkout <branch>`, `clean -n`, `stash create`, `stash list` and
      `restore --staged` as not
- [x] a `cd <dir> && git clean -fdx` is read against `<dir>`, not against the
      cwd — the `cd` holds for the rest of the line
- [x] two live sessions each holding uncommitted work in a tree of its own:
      each may discard in its own tree, neither may discard in the other's,
      and neither may discard in the main checkout that neither holds
- [x] a shell whose cwd is the main checkout, with no session on the ledger
      holding it, may discard there
- [x] `resources/guard.py pre` returns a `deny` for a destructive git aimed at
      a tree this session does not own, and the denial names both the command
      and the memo
- [x] the guard's check runs before the no-board return, so a cwd with no
      board above it is not a way around the ledger above the target
- [x] a tree with no board above it is allowed — no ledger, no ownership
- [x] `resources/board/refuse.py` imports nothing from the board's other
      modules, so the guard keeps its rule that a broken planner never blocks
      a tool call
- [x] `lanes.py`'s `reset --hard` fallback runs only when the lane is this
      process's to discard
- [x] `collect.py`'s `_park` still parks, and the comment above it says why it
      is not under the refusal
- [x] `pearde refuse tree` and `pearde refuse cmd` both route, exit 0 when
      allowed and 3 when refused
- [x] the harness sweep names the same failing probes as it did before this
      change — none reddened, none silently fixed

## Verify and Proof

```sh
cd "$PEARDE_ROOT"
bash pearde/prds/every-run-session-works-in-a-worktree-of-its-own/no-destructive-git-runs-in-a-tree-the-session-does-not-own/probe/verify.sh
# `<cmd> && echo` cannot fail a block — `-e` skips every command of an AND-OR
# list but the last — so each assertion below puts the failure last instead.
fail() { echo "FAIL: $*"; exit 1; }
python3 resources/pearde.py refuse tree >/dev/null \
  || fail "refuse tree did not route, or refused this session its own tree"
echo "refuse routes, exit 0 in a tree this session owns"
# and exit 3 in one it does not: a fresh repo under mktemp is on no ledger
# row and is not the tree this process is working in, so rule 2 declines it.
d=$(mktemp -d); git -C "$d" init -q
python3 resources/pearde.py refuse cmd "git -C $d clean -fdx" \
  --board "$PEARDE_ROOT/pearde" >/dev/null 2>&1 && rc=0 || rc=$?
rm -rf "$d"
[ "$rc" = 3 ] || fail "refuse cmd exited $rc on a tree this session does not own, want 3"
echo "refuse cmd exits 3 when refused"
python3 - <<'PY'
import ast, sys
t = ast.parse(open("resources/board/refuse.py").read())
mods = {n.module or "" for n in ast.walk(t) if isinstance(n, ast.ImportFrom)} | \
       {a.name for n in ast.walk(t) if isinstance(n, ast.Import) for a in n.names}
bad = mods & {"plan", "lanes", "session", "collect", "edit", "transitions", "specs"}
sys.exit(f"refuse.py imports the board: {bad}" if bad else 0)
PY
grep -q "stash-then-POP" resources/board/collect.py \
  || fail "_park's measured reason is gone from collect.py"
echo "_park's reason is on record"
grep -q "_may_discard(wt)" resources/board/lanes.py \
  || fail "lanes.py's reset --hard is no longer conditional"
echo "the lane reset is conditional"
# The sweep is a board-wide gate: `doctor.sh` exits 1 while ANY row is
# broken, and three are red on this tree for reasons outside this footprint
# (index, origin, knowledge). Piped, `pipefail` made that exit the block's, so
# the block could not pass however green this unit was — measured, exit 1 on
# `doctor.sh | grep '^  index'`. Captured instead: the rows stay visible and
# stop deciding, and the one thing gated is this PRD's own probe.
out=$(bash resources/doctor.sh --harnesses "$PEARDE_ROOT" 2>&1) && rc=0 || rc=$?
[ -n "$out" ] || { echo "FAIL: the sweep printed nothing (exit $rc)"; exit 1; }
printf '%s\n' "$out" | grep '^  harnesses'
{ printf '%s\n' "$out" | grep 'verify.sh — exit' || true; } \
  | sed 's/ — exit.*//; s/^ *//' | sort
# the PATH of this PRD's own probe, never the bare slug: the lane directory
# is named for the slug too, so a neighbour's FAIL line quoting a path inside
# this worker's lane matched the slug and read as this PRD going red —
# measured, on `a-lane-s-wiki-is-a-stub-…`, which was red before and after.
mine='prds/every-run-session-works-in-a-worktree-of-its-own/no-destructive-git-runs-in-a-tree-the-session-does-not-own/probe/verify.sh'
if printf '%s\n' "$out" | grep 'verify.sh — exit' | grep -qF "$mine"; then
  echo "FAIL: this PRD's own probe is red in the sweep"; exit 1
fi
```
