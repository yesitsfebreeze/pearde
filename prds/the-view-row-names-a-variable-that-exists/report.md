# report — the-view-row-names-a-variable-that-exists · implementer as engineer

Verdict: **DONE**. 1 spec, 4/4 acceptance boxes ticked, verify block rc=0.

## What changed

Nothing beyond pass one. The probe round's edit was already on the tree and is
correct as written; this run was the confirmation breadth the spec asked for.
`resources/doctor.sh` is the only dirty file in the code repo, and it carries
exactly the one line plus its comment:

| where | line |
|-------|------|
| definition | `590:  PBOARD=$(cd "$BOARD" 2>/dev/null && pwd -P)` |
| read | `598: \|\| printf '%s' "$SRV" \| grep -qF "\"$PBOARD\"" \` |
| block | `if [ -n "$BOARD" ]` opened at 584 — definition precedes the read |

## The four boxes, each run

| # | box | evidence |
|---|-----|----------|
| 1 | `PBOARD` defined in the view block before the `elif` that greps it | `grep -n 'PBOARD' resources/doctor.sh` -> 582 (comment), 590 (definition), 598 (read) |
| 2 | symlinked-cwd daemon -> `view ok`, no `unbound variable` anywhere | probe checks 3 and 5: `ok    no unbound-variable line anywhere in doctor's report`, `ok    view ok across a symlinked START — pwd -P bridges the spelling` |
| 3 | every variable the `elif` names is assigned in `doctor.sh` | probe check 2: `ok    every variable the view row names is defined` |
| 4 | the two view harnesses still green | 24/24 and 30/30, both rc=0 — see below |

Box 4 named `.pearde/prds/the-page-shows-the-round/probe/verify.sh`, which does
not exist at that path: that PRD is a child of `the-board-runs-itself`. The
real path is
`.pearde/prds/the-board-runs-itself/the-page-shows-the-round/probe/verify.sh`
— rc=0, `24/24 checks pass`, with its served half reporting
`skip  no daemon on :8443 — the served half was not run` (the view daemon is
down, as the round said). `one-page-that-says-whats-up`: rc=0,
`30 checks · 30 pass · 0 fail`. The spec's stale path is recorded in the box
itself; no file was moved to satisfy it.

## Verify and Proof — run twice, identical, rc=0

Run under `bash -e -o pipefail` from the code repo, as `collect` runs it:

```
0
  view        off     not running — the board reads and plans without it
590:  PBOARD=$(cd "$BOARD" 2>/dev/null && pwd -P)
  ok    the view block defines PBOARD before its elif reads it
  ok    every variable the view row names is defined
  ok    no unbound-variable line anywhere in doctor's report
  ok    view ok when the service holds the spelling doctor walks
  ok    view ok across a symlinked START — pwd -P bridges the spelling
  ok    the ok line names the board, spelled /tmp/pearde-viewrow.4c9ONB · /status holds it
6 checks · 6 pass · 0 fail
probe harness complete
verify done rc=0
```

The `view off` line is correct, not a failure: the block pins `PEARDE_PORT=1`,
so nothing answers `/status` and the row takes its `off` arm. The row's `ok`
arm — the one `PBOARD` serves — is exercised by the probe's fixture servers on
scratch ports 8477-8479, which is where checks 4 and 5 come from.

The probe's three `Terminated: 15` job-control notices arrive after
`probe harness complete` and before `verify done rc=0`; they are the trap
reaping its own fixture servers, on stderr, and do not affect the exit code.
Nothing the probe spawns outlives it.

## The gate

`bash resources/doctor.sh --harnesses /Users/feb/dev/infra/pearde` **never
returns** — it printed 14 rows and then hung, and I killed it at 540s. The
`harnesses` and `jstests` rows never appeared. That is the sibling
implementer's report reproduced, and finding 1 below is its actual cause: it
is not the dirty `doctor.sh`.

So I ran the gate's harness set the way the `harnesses` row runs it
(`find "$BOARD" -name verify.sh`, `PEARDE_HARNESSES=1 bash "$h" </dev/null`,
all in parallel), with a 200s alarm per harness so one hang could not swallow
the result:

```
harnesses: 43 total · 40 rc=0 · 3 nonzero
```

The three, and why none is mine — none of the three names `doctor.sh`,
`PBOARD`, or the view row (`grep -c 'doctor.sh'` returns 0 on all three):

| harness | rc | verdict |
|---------|----|---------|
| `the-graph-lands-inside-the-board/probe/verify.sh` | 142 (my alarm) | hangs forever — finding 1 |
| `nothing-left-open/the-line-tells-the-truth/probe/verify.sh` | 1 in parallel | **green serially**: `verify: 85 checks · 85 pass · 0 fail`, rc=0 — a parallel-run artifact, finding 2 |
| `the-board-runs-itself/transitions-are-commands/probe/verify.sh` | 1 | fails serially too: `74 checks · 66 pass · 8 fail` — finding 3 |

## Findings (not mine to fix)

1. **`the-graph-lands-inside-the-board/probe/verify.sh` hangs unbounded, and
   that is why `doctor.sh --harnesses` emits no `harnesses` or `jstests` row.**
   The row runs every harness in parallel and then `wait`s; one harness that
   never exits blocks the `wait`, so neither row is ever printed and doctor
   exits only when killed. Not caused by a dirty `doctor.sh` — I saw two other
   sessions' processes stuck on this same harness (one a bare run with no
   doctor in the picture, stuck 27 minutes). It hangs at its step 3:

   ```
   [3] extract (full, --force) leaves the vault + marker in place too
   [graphify] WARNING: ollama backend selected with no OLLAMA_API_KEY set;
   sending corpus to http://127.0.0.1:11434/v1.
   ```

   A full `graphify extract ... --backend ollama --force` against the real repo
   with no timeout. The fix belongs to that PRD — a bounded call, or the
   harness skipping the extract when the backend does not answer. Until then
   the `harnesses` row is unreachable on this machine, which costs the board
   its only automatic gate.

2. `nothing-left-open/the-line-tells-the-truth` fails under the parallel run
   (`FAIL E14 no scratch index is left behind`) and passes 85/85 alone. It
   asserts on a shared scratch index, so a concurrent harness's leftover
   reddens it. Real, and it will redden the `harnesses` row at random once
   finding 1 is fixed and the row can complete.

3. `the-board-runs-itself/transitions-are-commands` fails 8 of 74 serially,
   against committed code: `claim next now succeeds`, `state is claimed`,
   `claim: impl-1 <now> written`, `the diff is two lines written`, `the line
   opens with the transition`, `as <persona> is last`, `@<w> workers from
   settings`, `.transitions.jsonl has one row per state move (13)`. The
   sibling's `resources/board/transitions.py` work committed mid-run (the tree
   went from 10 dirty files to 1 while I was working); this harness was not
   brought along. It reads nothing of mine.

4. `winpath()` at `resources/doctor.sh:566` converts `/` to `\` in its
   fallthrough branch on every platform, so off Windows `WBOARD_JSON` is
   backslash junk that can never match — the third grep arm is dead weight.
   Carried forward from the analyst round, still true, still harmless (the
   first arm matches via `-F`). Untouched: fixing it is a contract widening.

## Housekeeping

- The code repo is `M resources/doctor.sh` and nothing else. No commit, no
  stash, no `git checkout` of a path.
- Every process I started, I killed: one orphaned `doctor.sh --harnesses` with
  its child, and two `graphify extract` children left by the alarmed runs. I
  left the other sessions' stuck processes alone, and left the view daemon
  down and the registry untouched — the probe never binds 8443.
- No knowledge written: every fact this run produced is about this repo. The
  `set -u` fall-through fact was already recorded by the probe round at
  `wiki/sources/260831-cdcb.md`.

## Carried forward from the probe round (not yet landed)

The analyst drafted one atomic the library lacks,
`setu-variable-existence-sweep`, whose three steps are: find the removal commit
(`git log -p -S 'NAME=' -- <file>`) and grep every remaining reader; test the
`set -u` fall-through shape in isolation, since bash 3.2 prints
`NAME: unbound variable` and continues with the condition false rather than
aborting; re-scope the definition into the block that reads it, beside the
other per-row derivations, not back into the row that lost it. Done when a full
run prints no `unbound variable` line and the branch behaves on both sides of
the spelling it bridges. Recorded here so the round's one library artifact is
not lost with the analyst's report.
