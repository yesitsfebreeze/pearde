---
complexity: 4
footprint:
  - pearde/prds/the-daemon-must-not-write-into-a-board-path-it-no-longer-own/probe/verify.sh
  - pearde/prds/the-daemon-must-not-write-into-a-board-path-it-no-longer-own/probe/repro.py
---

# spec03 — the harness that fails on the write

Every check here is a write that must not happen, so the harness is built
around what is on disk after a call, not what the call returned.

## What already stands

Both files, written and run. Red at HEAD (6 of 10 failing), green with spec01
and spec02 in the tree — so the harness can fail, and does.

## What is left

Nothing but keeping it honest. Three properties it must not lose:

- Fixtures are made at run time under `<ROOT>/.probe-daemon-path` and removed
  on the way out. **Never under `/tmp`**: `serve.EPHEMERAL` turns `save_entry`
  into a no-op there, so a `/tmp` fixture would report the write as absent when
  the guard is the fixture's own location. The first draft of this probe passed
  three checks for exactly that reason.
- The denominator is pinned at 10. A harness that loses its checks to an import
  error prints `0 checks · 0 pass · 0 fail` and exits 0, which is
  indistinguishable from success.
- The can-it-fail proof runs on a **copy**, never on the tree it is run in.
  `collect` merges the lane first and then runs this block in the
  orchestrator's checkout, so a proof written as `git stash push` / `git stash
  pop` around a revert has two ways to end badly there: after the merge both
  files are committed, the `push` saves nothing and the trailing `pop` takes
  whatever a peer session left on top of the stash stack; and the revert can
  never turn the harness red once HEAD carries the build, so the block fails
  for ever. The tree under test is chosen by `PEARDE_ROOT`, so the proof
  copies `resources/` into a scratch root, removes the two guards there, and
  points the harness at the copy — the checkout is read and never written.

## Acceptance

- [x] `verify.sh` takes its tree from `PEARDE_ROOT` and falls back to the board's own repo, so a worker building in a lane measures the lane.
- [x] The harness prints `N checks · N pass · 0 fail` and `probe harness complete`, and exits non-zero on any failure.
- [x] It reports a failure rather than a pass when the probe reports other than its 10 defined checks.
- [x] It builds no fixture under `/tmp` and none under `prds/`, and removes its fixture root on the way out.
- [x] A tree whose `resources/board/plan.py` and `resources/board/serve.py` carry neither of this unit's guards turns it red, proved on a copy the block makes and removes — never by reverting the tree the block runs in.

## Verify and Proof

```sh
bash pearde/prds/the-daemon-must-not-write-into-a-board-path-it-no-longer-own/probe/verify.sh
mkdir -p pearde/.state
M="$PWD/$(mktemp -d pearde/.state/probe-mutant-XXXXXX)"
mkdir -p "$M/resources/board"
cp resources/*.py "$M/resources/"
cp resources/board/*.py "$M/resources/board/"
python3 - "$M" <<'PY'
import os, sys
m = sys.argv[1]
for rel, anchor in (("resources/board/plan.py", "    if not is_board_dir(board):"),
                    ("resources/board/serve.py", "    if not planlib.is_board_dir(b.path):")):
    p = os.path.join(m, rel)
    s = open(p, encoding="utf-8").read()
    if anchor not in s:
        raise SystemExit("mutation anchor gone from " + rel + ": " + anchor)
    open(p, "w", encoding="utf-8").write(s.replace(anchor, "    if False:", 1))
print("the two guards removed in the copy")
PY
PEARDE_ROOT="$M" bash pearde/prds/the-daemon-must-not-write-into-a-board-path-it-no-longer-own/probe/verify.sh > "$M/mutant.txt" 2>&1 && rc=0 || rc=$?
tail -2 "$M/mutant.txt"
rm -rf "$M"
[ "$rc" -ne 0 ]
```
