---
complexity: 22
footprint:
  - resources/board/transitions.py
---

# spec01 — the sweep commits a lane before it drops it, and a live claim can be checkpointed on demand

`sweep --apply` is the only edge that removes a worktree holding uncommitted
work, and on 2026-09-03 it dropped 44 paths across four lanes. This unit
closes that with the one mechanism that already existed unwired,
`lanes.commit_all`, wired into the two places a lane's standing work needs
to reach the branch before something drops or outlives it: `drop_lane`
commits everything standing before `lanes.remove` runs, and `pearde
checkpoint <prd>` gives a pass, a person or a watchdog a one-word way to do
the same thing on a live claim, on demand, moving no state and writing no
board file. Both calls share one mechanism and one file, so they are one
implementable unit, not two: the checkpoint command's fixture and refusal
paths are the same lane-resolution code the sweep's edge already needed,
and reviewing them apart would mean reading the same `commit_all` call
twice for no reason.

What already stands (built and probed in this pass, uncommitted in the
lane):

- `drop_lane` checkpoints before `lanes.remove` when the lane is dirty,
  prints `N path(s) committed as <sha>`, and only prints `uncommitted
  path(s) dropped` when the checkpoint itself raised `LaneError` — the
  `## Failure` section's "the branch is kept" line was true of an empty ref
  whenever the lane held dirt; now it is true of the commit that carries
  the work.
- `cmd_checkpoint` (`pearde checkpoint <prd>`) resolves the PRD, refuses one
  with no lane, prints `N path(s) committed as <sha>` / `lane clean,
  nothing standing` / `would commit N path(s)` under `--dry` (checked before
  the clean-lane branch, so a dry run on a clean lane still answers),
  requires a persona (not in `DEFAULTS_FOR`, so no `--as` and no
  `PEARDE_AS` refuses exit 1), is declared in `FLAGS` and `COMMANDS`, and
  is in `pearde help` from its own docstring.

## Acceptance

- [x] `drop_lane` calls `lanes.commit_all` with the PRD rel in the message before `lanes.remove`, and only when `lanes.dirty` is non-empty
- [x] a fixture lane holding uncommitted work, swept with `--apply`, leaves the worker's bytes recoverable with `git show lane/<branch>:<path>` after the worktree is gone
- [x] the sweep line says `path(s) committed as` and never says `uncommitted path(s) dropped` when the checkpoint succeeded; a `LaneError` from the checkpoint instead prints `checkpoint failed` and the sweep still removes the worktree, reporting the drop as before
- [x] a clean lane produces no checkpoint commit and the sweep line still says the branch is kept
- [x] `pearde checkpoint <prd>` commits every standing path of the claim's lane to `lane/<slug>`, prints `path(s) committed as` with a resolvable sha, and leaves the PRD's `state:`/`claim:` frontmatter byte-identical and the lane worktree on disk, clean in `git status --porcelain`
- [x] a second `checkpoint` run on a now-clean lane prints `nothing standing`; `--dry` prints `would commit N path(s)` on either a dirty or a clean lane and commits nothing
- [x] a PRD with no lane, and a call with no `--as` and no `PEARDE_AS`, each refuse `checkpoint` with exit 1 and write nothing; `checkpoint` is listed in `pearde help`

## Verify and Proof

```sh
LANE="$(git rev-parse --show-toplevel)"
D="$(mktemp -d)"; mkdir -p "$D/w/.pearde"
cp -R "$LANE/resources/board/example/." "$D/w/.pearde/"
mkdir -p "$D/w/.pearde/.state" "$D/w/src"
printf 'base\n' > "$D/w/src/app.py"
printf '.pearde/.lanes/\n.pearde/.state/\n.pearde/prds/**/probe/\n' > "$D/w/.gitignore"
find "$D/w" -type f -exec touch {} +
git -C "$D/w" init -q -b main && git -C "$D/w" add -A && git -C "$D/w" commit -q -m fixture
python3 - "$D/w" "$LANE" <<'EOF'
import os, sys
d, root = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(root, "resources", "board"))
import lanes
lane = lanes.create(os.path.join(d, ".pearde"), d, "building")
open(os.path.join(lane, "src", "app.py"), "w").write("the worker's line\n")
EOF
find "$D/w" -type f -not -path '*/.git/*' -exec python3 -c 'import os,sys,time; t=time.time()-7200; [os.utime(p,(t,t)) for p in sys.argv[1:]]' {} +
out="$(python3 "$LANE/resources/pearde.py" sweep --apply --board "$D/w/.pearde" --as engineer 2>&1)"
echo "$out" | grep -q "committed as" || { echo "FAIL: no checkpoint line"; exit 1; }
got="$(git -C "$D/w" show lane/building:src/app.py 2>/dev/null || echo lost)"
[ "$got" = "the worker's line" ] || { echo "FAIL: work not on branch, got: $got"; exit 1; }
echo "sweep-checkpoint: ok"

D2="$(mktemp -d)"; mkdir -p "$D2/w/.pearde"
cp -R "$LANE/resources/board/example/." "$D2/w/.pearde/"
mkdir -p "$D2/w/.pearde/.state" "$D2/w/src"
printf 'base\n' > "$D2/w/src/app.py"
printf '.pearde/.lanes/\n.pearde/.state/\n.pearde/prds/**/probe/\n' > "$D2/w/.gitignore"
find "$D2/w" -type f -exec touch {} +
git -C "$D2/w" init -q -b main && git -C "$D2/w" add -A && git -C "$D2/w" commit -q -m fixture
python3 - "$D2/w" "$LANE" <<'EOF'
import os, sys
d, root = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(root, "resources", "board"))
import lanes
lane = lanes.create(os.path.join(d, ".pearde"), d, "building")
open(os.path.join(lane, "src", "app.py"), "w").write("the worker's line\n")
EOF
before="$(grep -m1 '^state:' "$D2/w/.pearde/prds/building/prd.md")"
out="$(python3 "$LANE/resources/pearde.py" checkpoint building --board "$D2/w/.pearde" --as engineer 2>&1)"
echo "$out" | grep -q "committed as" || { echo "FAIL: no commit line"; exit 1; }
[ "$before" = "$(grep -m1 '^state:' "$D2/w/.pearde/prds/building/prd.md")" ] || { echo "FAIL: state moved"; exit 1; }
got="$(git -C "$D2/w" show lane/building:src/app.py 2>/dev/null || echo lost)"
[ "$got" = "the worker's line" ] || { echo "FAIL: work not on branch"; exit 1; }
[ -d "$D2/w/.pearde/.lanes/building" ] || { echo "FAIL: lane removed"; exit 1; }
again="$(python3 "$LANE/resources/pearde.py" checkpoint building --board "$D2/w/.pearde" --as engineer 2>&1)"
echo "$again" | grep -q "nothing standing" || { echo "FAIL: second run not clean"; exit 1; }
dry="$(python3 "$LANE/resources/pearde.py" checkpoint building --board "$D2/w/.pearde" --dry --as engineer 2>&1)"
echo "$dry" | grep -q "would commit" || { echo "FAIL: --dry did not say would commit"; exit 1; }
echo "checkpoint-command: ok"
```
