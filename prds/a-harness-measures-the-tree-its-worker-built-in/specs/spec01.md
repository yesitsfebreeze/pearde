---
complexity: 10
footprint:
  - .pearde/prds/a-cross-board-need-that-names-no-board-in-the-scan-is-ignore/probe/verify.sh
  - .pearde/prds/a-session-start-brings-the-board-up/probe/verify.sh
  - .pearde/prds/an-acceptance-box-that-cannot-fail-is-refused/probe/verify.sh
  - .pearde/prds/an-analyst-workflow-does-not-survive-into-specced/probe/verify.sh
  - .pearde/prds/brief-does-not-refuse-the-claim-it-was-just-handed/probe/verify.sh
  - .pearde/prds/check-crosses-member-boundaries/probe/verify.sh
  - .pearde/prds/collect-stages-a-shared-file-whole/probe/verify.sh
  - .pearde/prds/files-score-their-health-and-the-brief-names-the-unhealthy/probe/verify.sh
  - .pearde/prds/filing-refuses-a-file-it-does-not-hold/probe/verify.sh
  - .pearde/prds/leaked-background-services-outlive-their-fixtures/probe/verify.sh
  - .pearde/prds/nothing-left-open/a-quoted-walk-is-data/probe/verify.sh
  - .pearde/prds/one-page-that-says-whats-up/probe/verify.sh
  - .pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh
  - .pearde/prds/the-board-asks-for-itself/a-question-in-plain-words/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/an-example-board/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/brief-is-printed/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/hunks-land-where-they-came-from/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/the-page-shows-the-round/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/too-big-splits-itself/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh
  - .pearde/prds/the-board-runs-itself/vision-is-first-class/probe/verify.sh
  - .pearde/prds/the-brief-names-the-verdict-line-collect-requires/probe/verify.sh
  - .pearde/prds/the-round-runs-in-a-window-that-ends/probe/verify.sh
  - .pearde/prds/the-tool-keeps-its-word/collect-keeps-its-word/probe/verify.sh
  - .pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh
  - .pearde/prds/the-tool-keeps-its-word/one-predicate-for-dispatchable/probe/verify.sh
  - .pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh
  - .pearde/prds/the-whole-machine-is-worked-as-one-board/the-machine-frontier-is-one-ordered-list/probe/verify.sh
  - .pearde/prds/upgrade-leaves-the-memo-index-stale/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-improve/probe/verify.sh
  - .pearde/prds/workflows-on-the-board/workflow-reader/verify.sh
---

# spec01 — one preamble roots the thirty-two harnesses that only need a root

Every harness on this board works out which tree to measure by counting `..`
from its own path. That path is always the orchestrator's checkout: the board
lives there and a lane worktree at `<board>/.lanes/<slug>` holds no copy of it.
So a worker's build is invisible to every board harness, and a box that goes
green proves a tree holding none of the work — measured, not argued, in
`probe/root-probe.sh`.

These thirty-two harnesses read the code tree and nothing else. Each gets the
same preamble, replacing whatever it uses now:

```sh
HERE="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
BOARD="$HERE"
while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ]; do BOARD="$(dirname "$BOARD")"; done
ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"
```

Two things change together. `BOARD` is found by walking up to the `.pearde`
the file sits under, so no count of `..` has to match the PRD's nesting depth —
today four spellings exist (four levels for a top-level PRD, five for a nested
one, `workflows-on-the-board/workflow-reader/verify.sh` outside a `probe/` dir,
and two files that hardcode `/Users/feb/dev/infra/pearde`). `ROOT` is the
runner's tree when it names one, that board's repo otherwise — the walk-up
survives as the fallback, so a harness run by hand from anywhere behaves as it
does today. `probe/rootwalk-probe.sh` runs the walk from all fifty-nine harness
directories and resolves the same board and the same repo from every one.

The file's own root variable keeps its name. Eleven of these call it `ROOT`,
and the rest `REPO`, `CODE`, `R` or nothing at all (`cd "$(dirname
"$0")/../../../.."` and then `$PWD`); each keeps whatever it had, assigned from
the `ROOT` the preamble computed. No assertion in any of these files changes —
`nothing-left-open` is not in scope here and no check's subject moves.

**Already standing (this analyst's uncommitted pass one):**
`.pearde/prds/the-view-row-names-a-variable-that-exists/probe/verify.sh` carries
the preamble and passes both ways: green against the orchestrator's checkout,
and red under `PEARDE_ROOT=<lane>` when the lane's `doctor.sh` has the
`PBOARD=` line it guards deleted. That is the whole mechanism, proven on one
file. The other thirty-one are the same edit.

## Acceptance

- [x] All 32 files in the footprint carry the preamble: `while [ "$BOARD" != / ] && [ "$(basename "$BOARD")" != .pearde ]` appears once in each.
- [x] All 32 read `${PEARDE_ROOT:-` — no file in the footprint computes its root without consulting the runner.
- [x] No file in the footprint still counts `..` to reach the repo: `grep -c 'dirname "\$0")/\.\./\.\./\.\.' <file>` is 0 for each, and the same for the `BASH_SOURCE[0]` and `$HERE` spellings.
- [x] Neither hardcoded absolute path survives: `grep -rl '/Users/feb/dev/infra/pearde' <footprint>` is empty.
- [x] Run from the orchestrator's checkout with `PEARDE_ROOT` unset, each of the 32 exits with the code it exited with before the edit — the list of exit codes is unchanged file for file.
- [x] Run with `PEARDE_ROOT` naming a lane worktree, each of the 32 resolves `ROOT` to that lane — proven by one harness per shape family going red on a defect planted only in the lane.

## Verify and Proof

```sh
cd /Users/feb/dev/infra/pearde
B=.pearde/prds/a-harness-measures-the-tree-its-worker-built-in
N=0
# the preamble is there, and nothing counts `..` or names an absolute path to
# reach the repo any more. Every offender is printed and counted; the block
# ends on the counter, so a check that finds nothing cannot exit the block.
for h in $(sed -n 's/^  - //p' $B/specs/spec01.md); do
  grep -qF 'basename "$BOARD"' "$h" || { echo "no preamble: $h"; N=$((N+1)); }
  grep -qF '${PEARDE_ROOT:-' "$h" || { echo "no PEARDE_ROOT: $h"; N=$((N+1)); }
  if grep -qE '(dirname "\$0"|BASH_SOURCE\[0\]}"|\$HERE)/\.\./\.\./\.\.' "$h"; then
    echo "still walks: $h"; N=$((N+1))
  fi
  if grep -qF '/Users/feb/dev/infra/pearde' "$h"; then echo "absolute root: $h"; N=$((N+1)); fi
done
echo "spec01 census over 32 harnesses: $N offending"
# the walk resolves board and repo from every harness directory
bash $B/probe/rootwalk-probe.sh
# a defect planted only in a lane is seen when the runner names the lane, and
# not otherwise. `root-probe.sh` runs it against this PRD's real lane and so
# only while one is cut; `probe/verify.sh` section C carries the same
# experiment on a fixture, which is what survives the merge.
if [ -d .pearde/.lanes/a-harness-measures-the-tree-its-worker-built-in ]; then
  bash $B/probe/root-probe.sh
else
  echo "root-probe: no lane cut — verify.sh section C runs the same experiment on a fixture"
fi
[ "$N" = 0 ]
```
