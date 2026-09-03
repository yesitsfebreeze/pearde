---
complexity: 8
footprint:
  - pearde/memos/no-destructive-git-runs-in-a-tree-the-session-does-not-own.md
  - resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh
---

# spec03 — the rule is an invariant with a command that can fail, not a comment

The refusal is a rule about every future call site, not about the four this
PRD found. This board keeps a rule like that as a memo of kind `invariant`
carrying a `verify:` command, run by `pearde memo verify` — five already sit
in `resources/invariants/`. Without one, the next `reset --hard` written into
the board's own code is caught by nothing: `refuse.py` guards the call sites
that ask it, and a new call site that does not ask is exactly the shape of the
loss the memo records.

**What stands.** Nothing — this spec is entirely new work. The decision memo
it rests on is already written and settled:
`pearde/memos/a-session-that-writes-a-shared-checkout-can-revert-another-
session-s-work.md`. This one is the invariant beside it, not a second
telling of it.

**What the check must do.** Read the board's own Python for a destructive git
that is not gated, and fail naming the file and the line. The three gated
sites are the shapes it must accept: `lanes.py`'s `_may_discard(wt)`
condition, `collect.py`'s `_park` with the comment above it saying why it
stands, and `session.py`'s reaper, which uses `stash create` and never a real
stash. Everything else that spells one of the four in a `subprocess`
argument list or a `git(...)` call is a finding.

A check that cannot fail is worth nothing, so the box below asks for the
injection: put a bare `reset --hard` into a board module in a scratch copy and
watch the check go red on it.

## Acceptance

- [x] `resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh`
      exists, exits 0 on this tree, and prints one line per problem when there
      is one
- [x] it names the file and the line for every ungated destructive git it
      finds in the board's own Python
- [x] it accepts the three sites that stand — `lanes.py`'s conditional
      `reset --hard`, `collect.py`'s `_park`, and `session.py`'s
      `stash create` — and names none of them
- [x] injected into a scratch copy of the tree, a bare `git reset --hard` in
      a board module makes it exit non-zero and name that file
- [x] `pearde/memos/no-destructive-git-runs-in-a-tree-the-session-does-not-own.md`
      is a memo of kind `invariant` whose `verify:` runs that script
- [x] `pearde memo check` is silent, and `pearde memo verify` runs the new
      invariant green
- [x] the memo names the decision memo it rests on and does not restate it

## Verify and Proof

```sh
cd "$PEARDE_ROOT"
bash resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh
python3 resources/pearde.py memo check
python3 resources/pearde.py memo verify no-destructive-git-runs-in-a-tree-the-session-does-not-own
# the check can fail: inject one into a scratch copy and watch it go red
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cp -R resources "$T/resources"
printf '\nimport subprocess\nsubprocess.run(["git","reset","--hard"])\n' \
  >> "$T/resources/board/orphans.py"
( cd "$T" && bash "$PEARDE_ROOT/resources/invariants/no-destructive-git-runs-in-a-tree-the-session-does-not-own.sh" ) \
  && { echo "FAIL: the check passed an injected reset --hard"; exit 1; } \
  || echo "the check fails on an injected reset --hard"
```
