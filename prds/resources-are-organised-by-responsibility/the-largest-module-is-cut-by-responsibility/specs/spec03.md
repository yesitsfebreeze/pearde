---
complexity: 7
footprint:
  - .pearde/prds/the-board-runs-itself/one-command/probe/verify.sh
  - .pearde/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh
  - .pearde/prds/complexity-is-guarded-like-priority/probe/verify.sh
  - .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
---

# spec03 — the four harnesses that read the file by name, re-pointed

The contract says every harness is unchanged from the outside. Twenty-seven of
the board's harnesses name `plan.py`; twenty-three of them go on printing what
they printed before the cut, because they call the commands and read the
board. Four do not: they reach past the interface and read the file itself, so
they are pinned to which file holds what, and the cut moves it. Each one is
re-pointed at the module that now holds the code — the assertion it makes is
unchanged, only the file it looks in.

**What stands.** All four edits, and the measurement behind them.
`probe/verify.sh` section E runs all four and compares each one's FAIL count,
and each one's traceback count, against the counts taken on a tree with no cut
in it. Measured on the checkout at `31620bb`, no cut: `one-command` 7 FAIL,
`one-predicate-for-dispatchable` 33 FAIL and 1 traceback,
`complexity-is-guarded-like-priority` 6 FAIL and 1 traceback,
`scan-parses-the-board-once-and-caches-it-by-mtime` 0 FAIL and 1 traceback.
With the cut and these four edits: 1, 29 and 1, 0, 0. Several of these
harnesses were already red for reasons outside this contract, which is why the
box is "no worse", not "zero".

The one traceback that survives is `39c0cab`'s, not this unit's.
`state_dir` there stopped calling `die()` and started raising `NotABoard`, and
`one-predicate-for-dispatchable`'s fixture hands it a path that carries no
board — so a `python3 -c` calling in gets a traceback where it used to get a
one-line refusal. The count is 1 with the cut and 1 without it, at `1880990`
it was 0, and nothing in this footprint can close it. It is a baseline in the
block rather than a wall.

**What is left.** Nothing in this spec.

1. **`the-board-runs-itself/one-command`** — 1 FAIL becomes 7. Its fixture
   builds a fake repo and symlinks a hard-coded list of board modules:
   `for f in plan.py serve.py render.py edit.py; do ln -s …`. `plan.py` now
   needs nine siblings beside it, so in the fixture it imports nothing and
   `pearde help` exits non-zero. Add the nine names to that list. No assertion
   changes.
2. **`the-tool-keeps-its-word/one-predicate-for-dispatchable`** — 29 becomes
   33. Four `grep -F` assertions read `$PLAN` for text that is now in
   `schedule.py`: `plan.py defines dispatchable once`,
   `cmd_scan calls it on the free set`, `compute_plan holds what it refuses`
   and `plan_frontier reads the hold`. `dispatchable`, `compute_plan` and
   `plan_frontier` are all in `schedule.py`; `cmd_scan` stays in `plan.py` but
   the harness reads the whole set out of one variable. Point the four at the
   file that holds each.
3. **`complexity-is-guarded-like-priority`** — 0 becomes 5. It asserts against
   `plan.py`'s text that `num`, `dur` and `bad_value` are defined there, that
   no `int()` over `settings.get` is unguarded and that three `float()` calls
   remain. All of that is in `prdfile.py` now. Point the five at `prdfile.py`.
4. **`scan-parses-the-board-once-and-caches-it-by-mtime`** — 0 FAILs but an
   `AttributeError: module 'plan' has no attribute '_PCACHE'`. Line 136 pokes
   the cache directly: `planlib._PCACHE.clear(); planlib._PCACHE_LOADED = True`.
   These two are rebound module globals and cannot be re-exported — an
   assignment on `plan` would set an attribute nothing reads. Address them
   through the module that owns them: `planlib.prdfile._PCACHE.clear();
   planlib.prdfile._PCACHE_LOADED = True`. This is the one place where the
   contract's "unchanged from the outside" cannot hold literally, and the
   reason is a mechanism, not a choice.

## Acceptance

- [x] `the-board-runs-itself/one-command` prints no more than 1 FAIL, the
  count it printed before the cut, and its fixture links every module
  `plan.py` imports
- [x] `the-tool-keeps-its-word/one-predicate-for-dispatchable` prints no more
  than 29 FAILs, and all four of the assertions this spec re-points —
  `schedule.py defines dispatchable once`, `cmd_scan calls it on the free
  set`, `compute_plan holds what it refuses`, `plan_frontier reads the hold`
  — print `ok`
- [x] `complexity-is-guarded-like-priority` prints 0 FAILs
- [x] `scan-parses-the-board-once-and-caches-it-by-mtime` prints 0 FAILs and
  no `Traceback`, and ends on `parse-cache verify: pass`
- [x] each of the four still asserts what it asserted: the diff against its
  pre-cut text changes only file paths and module prefixes, no `eq`/`has`
  expectation is deleted or weakened

## Verify and Proof

```sh
cd "$(git rev-parse --show-toplevel)"
# The tree under measurement is the cwd — a lane, a session worktree or the
# checkout — and `PEARDE_ROOT="$PWD"` below is what points each harness at it.
# The harness SCRIPTS live on the board, which is not in the code repo at all:
# a worktree of it holds an empty `.pearde/` and a cwd-relative board path
# resolves to nothing there. The board sits beside the main `.git`, so the
# common dir finds it from a worktree and from the checkout alike.
B="$(cd "$(git rev-parse --git-common-dir)/.." && pwd)/.pearde/prds"
test -f "$B/the-board-runs-itself/one-command/probe/verify.sh"
test -f "$B/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh"
test -f "$B/complexity-is-guarded-like-priority/probe/verify.sh"
test -f "$B/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh"
grep -q 'prdfile\._PCACHE' "$B/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh"
# Each row is a FAIL baseline and then a traceback baseline, both measured on
# a tree with no cut in it. The one non-zero traceback is `39c0cab`'s and not
# this unit's — `state_dir` there stopped calling `die()` and started raising
# `NotABoard`, so a harness calling in through `python3 -c` gets a traceback
# where it used to get a one-line refusal. A blanket "no Traceback" would
# fail this block for a sibling's landing, which is a file outside this
# footprint deciding the exit; a per-row baseline still catches any traceback
# the cut adds, on this row or the other three.
for row in "the-board-runs-itself/one-command 1 0" \
           "the-tool-keeps-its-word/one-predicate-for-dispatchable 29 1" \
           "complexity-is-guarded-like-priority 0 0" \
           "scan-parses-the-board-once-and-caches-it-by-mtime 0 0"; do
  set -- $row; rel=$1; base=$2; tbase=$3
  # a harness with FAILs exits non-zero, and a bare assignment from a command
  # substitution would carry that status and kill the block on exactly the
  # output it was written to read. grep -c exits 1 on a count of 0, the same way.
  out=$(PEARDE_ROOT="$PWD" bash "$B/$rel/probe/verify.sh" 2>&1) && rc=0 || rc=$?
  [ -n "$out" ]
  n=$(printf '%s\n' "$out" | grep -cE '(^|  )FAIL' || true)
  tb=$(printf '%s\n' "$out" | grep -c 'Traceback (most recent call last)' || true)
  printf '%s: %s FAIL (was %s), %s traceback (was %s), harness exit %s\n' \
    "$rel" "$n" "$base" "$tb" "$tbase" "$rc"
  test "$n" -le "$base" || exit 1
  test "$tb" -le "$tbase" || exit 1
  # a FAIL count that merely does not rise would still pass if the cut broke
  # one of the four assertions this spec re-points and a fixture closed
  # another, so each of the four is read by name
  if [ "$rel" = "the-tool-keeps-its-word/one-predicate-for-dispatchable" ]; then
    for lbl in "schedule.py defines dispatchable once" \
               "cmd_scan calls it on the free set" \
               "compute_plan holds what it refuses" \
               "plan_frontier reads the hold"; do
      test "$(printf '%s\n' "$out" | grep -cF "  ok   $lbl" || true)" = 1 || exit 1
    done
  fi
done
exit 0
```
