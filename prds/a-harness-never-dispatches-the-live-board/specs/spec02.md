---
complexity: 13
footprint:
  - resources/invariants/harness-dispatch-reader.py
  - resources/invariants/no-harness-under-the-board-dispatches-it.sh
  - references/files.md
  - index.md
  - .pearde/memos/no-harness-under-the-board-dispatches-it.md
---

# spec02 — the check that proves no harness on this board dispatches it

The contract asks for the absence to be proved over every `probe/` on the
board, not over the one file this PRD repaired. A grep cannot do it: `grep -rn
run.py` over this board returns 27 lines of which 8 are the defect, and it
misses the worst one entirely, because that one is written as an assignment on
line 17 and a use on line 29 with the dispatcher's name in neither command
position.

So a reader, in the shape the board already uses for
`no-destructive-git-runs-in-a-tree-the-session-does-not-own`: a script under
`resources/invariants/` named for its memo's slug, with the memo carrying it
as `verify:`. Shell is read positionally with the file's own variable
assignments resolved; Python is read as an AST, with module- and
function-level bindings resolved to a fixed point in order, so a
`subprocess.run(argv)` whose `argv` was built two assignments earlier is seen
and a docstring naming `run.py` is not.

One harness dispatches legitimately — `the-board-locks-by-realpath` proves two
dispatchers race by starting two, against a board it built in a mktemp dir
with the adapter stubbed. Telling that board from the user's is not decidable
from the source, so that harness carries `# dispatch-exempt: <reason>` within
six lines above the call, and an empty marker is not an exemption. This is the
same shape as `collect.py`'s `_park` exemption and is written down for the
same reason.

**Already stands**, uncommitted in the lane: both files, self-testing and
correctly red — 2 PASS on the synthetic boards, 1 FAIL naming eight lines in
three harnesses, 4 PASS on the mechanism. **Left:** the memo, the two manifest
rows, and the `@@` scope entry.

## Acceptance

- [x] `resources/invariants/harness-dispatch-reader.py <board>` prints one line per finding as `RED <rel>:<line>: <text>`, a `— N harness file(s) read · M dispatcher launch(es)` tally, and exits 1 when M is non-zero
- [x] the reader sees all six planted spellings on the synthetic red board: a shell `$VAR` two lines from its assignment, a `dispatch.py`, a `claude … /pearde run`, a bare `pearde run all`, a literal `subprocess.run([… "run.py", "all"])`, and one spelled through two Python variables
- [x] the reader clears all eight near-misses on the synthetic green board: `--dry`, `plan all`, a `grep` argument, a `[ -f … ]` test, an `open()`, a commented-out line, a docstring, and an exempted fixture dispatch
- [x] the invariant refuses — exit 1, not a pass — when no board is found at or above the working directory
- [x] the invariant also checks the mechanism: `run.py all` refuses, the refusal names `pearde plan`, `plan slots` prints its reading, and `plan.py` names `read_main`
- [x] injecting `python3 "$ROOT/resources/board/run.py" all` into any harness on the board turns the invariant red and names that file and line
- [x] a memo `.pearde/memos/no-harness-under-the-board-dispatches-it.md`, `kind: invariant`, carries the script as its `verify:` command, and `pearde memo check` passes on it
- [x] the memo's Consequences name what the reader cannot see: a command built from a variable the file does not assign, and a dispatcher reached through a wrapper not in its table
- [x] `references/files.md` carries a row for each of the two new files, and `pearde index check` reports no new line beyond the four already on the baseline

## Verify and Proof

```sh
bash resources/invariants/no-harness-under-the-board-dispatches-it.sh
python3 resources/memos.py check
python3 resources/memos.py verify no-harness-under-the-board-dispatches-it
python3 resources/index.py check
# it can fail: inject one, and the named file comes back
T=$(mktemp -d); mkdir -p "$T/prds/z/probe"
printf '#!/usr/bin/env bash\npython3 "/repo/resources/board/run.py" all\n' > "$T/prds/z/probe/verify.sh"
python3 resources/invariants/harness-dispatch-reader.py "$T" | grep -q 'RED prds/z/probe/verify.sh:2'
python3 resources/invariants/harness-dispatch-reader.py "$T" >/dev/null 2>&1 && { echo "FAIL the injection read green"; exit 1; }
rm -rf "$T"
```
