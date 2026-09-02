# leaked-background-services-outlive-their-fixtures — implementer report

Verdict: DONE

Worker `impl-leaked`, as `engineer`, workflow `probe-then-spec`. Second pass on
the route, plus a third pass answering two defects the collect-time consult
raised. **23 of 23** acceptance boxes ticked — spec01 7/7, spec02 10/10,
spec03 6/6. All three `## Verify and Proof` blocks exit 0 under
`bash -e -o pipefail`, the way `collect.py:1057` runs them. The probe is
`17 checks · 17 pass · 0 fail`, stable over three consecutive runs.

This report replaces the analyst's report at the same path; its findings are
carried forward by name below.

## The two defects the consult held this on — both fixed, both now pinned

**1. `reap --pid abc` silently swept the whole machine.** Confirmed exactly as
reported: a malformed value was dropped, `only` came back empty, and an empty
filter means *every daemon on this box*. So `--pid "$VAR"` with `VAR` unset was
the grace-less machine-wide sweep the flag exists to prevent. `main()` now
refuses — a value that is not a positive integer prints to stderr and exits
**2**, and no daemon is judged. Shown red before the fix, on the live service:

```
FAIL  reap --pid 'abc' refuses instead of sweeping the machine — exit 0,
      and it reported on: serve: keeping pid 28740 · port 8443 — watching 9 live board(s)…
16 checks · 11 pass · 4 fail
```

and green after, for `abc`, `""`, `--`, `12x` and `0`, in both the probe
(section 5) and spec02's own block (`--pid 'abc' -> exit 2`, five lines).

**2. Nothing green proved the grace ever expires.** Also confirmed: every stop
assertion ran at `PEARDE_REAP_GRACE_S=0`, so a default of 86400 would have kept
every box green while the reaper never reaped again. Probe section 6 now pins
it two ways:

- **the arithmetic** — a daemon it started is `keeping` inside
  `PEARDE_REAP_GRACE_S=30`, and two seconds later the same command at
  `PEARDE_REAP_GRACE_S=1` says `would stop`, on that same pid. Two seconds of
  runtime.
- **the shipped default** — read out of the module and asserted `0 < x <= 600`.
  A **bound, not a literal**: 30 or 120 pass, 86400 does not.

The second was added because the first alone did **not** close the hole the
consult named. Measured, not assumed: with the arithmetic check in place I set
the default to 86400 and the probe still printed `16 checks · 16 pass · 0 fail`.
With the bound added, the same mutation prints
`the shipped grace default is 86400.0s — long enough that nothing is ever reaped`
and `16 checks · 15 pass · 1 fail`. Restored from a scratch copy, `cmp` clean.

## A third defect, found while pinning the second, and it is the important one

Standing the probe up against the live machine crashed `reap` outright:

```
TypeError: stat: path should be string, bytes, os.PathLike or integer, not NoneType
  serve.py:1904 in stranded  →  os.path.isdir(b.get("path", ""))
```

`b.get("path", "")` returns `None` when the key is **present and null** — the
default only covers a missing key. One malformed neighbour took the entire reap
down before it judged anything, which is worse than the leak.

It is not hypothetical and it is not mine: **a parallel session is landing an
`all` view right now**, and `AllBoard` is by its own docstring "not a Board: it
has no path, nothing on disk". The live daemon on 8443 serves it today:

```
  all              synced never · None · master of 9: dotfiles, master, …
```

So as their work lands, `doctor.sh`'s end-of-sweep reap tracebacks and reaps
nothing at all — this PRD's entire contract, silently off. Fixed in
`stranded()`: non-dict entries skipped, `b.get("path") or ""`, name defaulted.
Probe section 7 stands up an HTTP server answering `/status` with
`{"boards":[{"name":null,"path":null}]}` and asserts `stranded()` returns a
verdict. Putting the old shape back reddens **three** checks; restored, `cmp`
clean. Two PRDs interact here and the orchestrator should know: the fix is
already in, on my side of the line, and their feature needs no change.

## The collision this PRD was sent at

`spec02`'s block was red on the built tree, asserting `would stop` on a daemon
it had started seconds earlier. `REAP_GRACE_S` correctly refuses that — a
daemon seconds old watching nothing is the shape a `SessionStart` hook's
`ensure` leaves between its bind and the board's first `/register`, and
`a-session-start-brings-the-board-up` (committed, `d646168`) makes that normal.

**Nothing was stood down.** `REAP_GRACE_S` (default 60s) stands exactly as
built, consumed as the first branch of `stranded()` before port, status or
`isdir` are consulted — one rule, no test-only fork. The block was re-aimed and
box 2 split, so the shipped grace now carries its own `keeping` assertion the
block never made before.

## What this implementer wrote

| file | change |
|---|---|
| `resources/board/serve.py` | `--pid <n>` on `reap` and its **refusal** of a value that is not a pid (`cmd_reap` filter, `main()` parse, usage block); the null-path hardening in `stranded()` |
| `references/parts/view.md` | what `--pid` is for, and that `doctor.sh`'s sweep names no pid and keeps the shipped grace |
| `specs/spec02.md` | box 2 split; `--pid` refusal box; null-path box; block re-aimed |
| `specs/spec03.md` | box 6 reads the **parsed tally**, never a literal total |
| `probe/verify.sh` | sections 5, 6 and 7; section 3's poll now waits for the registration, not just the bind |

Everything else in the footprint was built by the earlier passes and continued,
not reverted — including the `doctor.sh` `HLEAK` lines (848–854, 889).

## Which hunks in shared files are mine — corrected

My previous report claimed the whole `serve.py` diff. **That is no longer
true**: a parallel session began writing the `all` view into `serve.py` during
this run.

| file | mine | not mine |
|---|---|---|
| `resources/board/serve.py` | the lifetime docstring paragraph, `IDLE_EXIT_S`/`OWNER_PID`/`REAP_GRACE_S`, `vanished()`, `orphaned()`, the grace arithmetic in `watch()`, `PEARDE_SERVE_OWNER` in `cmd_ensure`, `daemon_pids()`, `listen_port()`, `age_s()`, `stranded()`, `cmd_reap()`, the `reap` branch in `main()` | the `all` docstring paragraph, the `AllBoard` class, the `/board/<name>` usage line about `all`, and the `all`-refusal branch in `Handler` — four regions naming `@references/parts/all.md`, none of which exist at `HEAD` |
| `resources/pearde.py` | one entry: `"reap"` in `FORWARD["view"]` | the `grammar` and `health` rows in the same hunk |
| `resources/doctor.sh` | the `HLEAK=$(… reap …)` block after `wait` and the `· <n> leaked service(s) reaped` suffix on `HDET` | the whole `── health:` row block |
| `resources/invariants/…-inside-the-board.sh` | both hunks (`export PEARDE_PORT=1`, and the port on the `forget` line) | — |
| `references/parts/view.md` | the whole diff | — |
| `resources/board/render.py`, `resources/board/all.py` | **nothing — never opened, never written** | entirely the `all` session's |

Nothing staged. Nothing written outside the footprint and the PRD folder.

## Harnesses

| harness | baseline | final | whose |
|---|---|---|---|
| `the-harness-sweep-is-capped-so-a-red-is-a-real-red` | `16 · 16 pass · 0 fail · 0 skip` | `16 · 14 pass · 0 fail · 2 skip` | its own port stand-down, see below |
| `a-session-start-brings-the-board-up` | `46 · 46 pass · 0 fail · 0 skip` | same | — |
| `the-view-row-names-a-variable-that-exists` | `6 · 6 pass · 0 fail` | `6 · 5 pass · 1 skip · 0 fail` | same stand-down |
| `nothing-left-open/the-line-tells-the-truth` | `85 · 84 pass · 1 fail` | `85 · 85 pass · 0 fail` | E14 was a neighbour's transient scratch dir |
| `one-page-that-says-whats-up` | `31 · 31 pass · 0 fail` | `31 · 30 pass · 1 fail` | **the `all` session's**, see below |
| `an-unknown-flag-refuses` | — | `196 · 196 pass · 0 fail` | run after `--pid` landed |
| `the-board-runs-itself/collect-is-a-command` | — | `133 · 133 pass · 0 fail` | reads the invariant script |
| `the-board-runs-itself/init-asks-nothing` | — | `89 · 89 pass · 0 fail` | reads the invariant script |
| `the-gate-runs-the-harnesses` | — | `57 · 56 pass · 1 fail` | pre-existing, see findings |
| `every-artifact-lands-inside-the-board.sh` | 7 PASS 0 FAIL | same | with `PEARDE_PORT=1` |
| this PRD's `probe/verify.sh` | `9 · 9 pass · 0 fail` | `17 · 17 pass · 0 fail` | +8 written this pass |

No count anywhere is gated on a literal total. spec03's box reads the probe's
own tally and asserts `checks == pass && fail == 0` — the probe gains checks as
the contract does, and it gained eight today.

**`one-page-that-says-whats-up` is the `all` session's, proven, not asserted.**
The red check is `the bar is seven anchors that jump`, over
`resources/board/render.py` — a file outside my footprint that I never opened.
`git show HEAD:resources/board/render.py` counts **7**; the working tree counts
**8**, the new one being `href="#view=boards"`. `git status` shows `render.py`
as `M` and it is not in any spec's `footprint:`.

**The two skips are the capped-sweep design working.** Both harnesses stand
down on fixed ports 8477–8479; `lsof` says 8479 is held by pid 98905, a
neighbour's fixture daemon watching two boards that still exist — which `reap`
correctly **keeps**, and which `IDLE_EXIT_S` will end when its boards go. Skips,
not fails; both harnesses exit 0. Nothing of mine binds a fixed port: every
daemon this PRD starts takes a `spare()` port picked at run time.

## Repo gate

`python3 resources/index.py check` was **exit 0** at baseline and is **exit 1**
now, on two problems, both the `all` session's and neither in my footprint:

```
resources/board/all.py is on disk with no row in references/files.md
resources/board/serve.py references @references/parts/all.md — not on disk
```

`resources/board/all.py` is untracked (`??`), `references/parts/all.md` does
not exist, and `git show HEAD:resources/board/serve.py | grep -c parts/all.md`
returns **0** — every one of those four references arrived in the working tree
during this run. Their author closes this by writing `parts/all.md` and the
`files.md` row.

`bash resources/doctor.sh` exit 1 before and after. Every row that moved
between the two runs is somebody else's: `index ok → broken` (above),
`origin broken → ok` (a sibling closed it), `memos 27 → 28`, and the
`knowledge` note list. `knowledge` was **broken before my first edit** and
still is. No row names a file of mine.

## Findings — reported, not fixed

- **The `all` view makes the null-path crash reachable on the live daemon.**
  Fixed on my side; their feature needs no change. Worth the orchestrator
  knowing the two PRDs met.
- **`the-gate-runs-the-harnesses` check J**, `54 · want 56`. The matcher wants
  a literal `fail`/`FAIL` *inside* the brackets, so
  `a-session-start-brings-the-board-up/probe/verify.sh` ending `[ "$F" = 0 ]`
  reads as carrying no exit-carrying test while carrying one. Both offenders
  are committed at the board's own `HEAD` (`1da9628`), so this predates my
  first command. **Left alone deliberately, per instruction.**
- **`E14` in `the-line-tells-the-truth` is racy across sessions** — its
  predicate is a whole-machine `/tmp/pearde-index-*` glob, and a live session's
  scratch dir existed for the seconds it ran. 85/85 on re-run.
- **The live service still watches `rampdemo` and `manola`.** spec03 closes the
  route inside my footprint that registers them, so no new one can land; the
  two rows already there are registry hygiene, not stranded processes, and
  `reap` keeps them correctly because both directories exist. Not removed on
  purpose — spec03 box 5 requires the `status` set to be identical around the
  harness run, and `manola` may be a board the user keeps.
  `python3 resources/board/serve.py forget rampdemo` is the command, for
  whoever owns that call.
- **`--pid` is test scaffolding shipped as a product flag.** Accepted by the
  consult and kept, now made safe. Its only consumers are spec02's block, the
  probe, `parts/view.md` and `serve.py`; `doctor.sh` calls bare `reap`.

## Health floor

`resources/board/serve.py` scores **27** (floor 40), worst `lines branching` —
1853 lines and branching 117 in `do_GET`. Nothing moved and nothing could
inside this spec's scope: the score is dominated by `do_GET`, which no box here
touches. This pass's additions are shallow module-level functions, none nested
beyond 2 or branching above 6, so the branching figure is untouched; the line
count necessarily rose. Splitting `serve.py` is a defect outside this scope —
**reported, not done** — and it is getting more urgent, not less, now that a
second PRD is adding a class to the same file. It wants its own PRD, and
`do_GET` is where it starts.

## Workflow probe-then-spec

| # | step | result |
|---|---|---|
| 1 | `read-the-contract` | ok — PRD, specs, probe and the analyst's report read; `git status --short` recorded before the first edit |
| 2 | `capture-the-harness-baseline` | ok — baseline inherited and **confirmed** by re-running the analyst's published set on the built tree, per the atomic's cheaper-confirmation clause; `knowledge` recorded red before the first edit |
| 3 | `attempt-the-build` | entered twice — once for `--pid`, once for its refusal plus the null-path fix. Built **in place** in the footprint file: a flag and a guard have no meaning outside the function they live in |
| 4 | `re-run-the-harnesses` | ok — eleven harnesses plus the repo gate; every count attributed; no flip claimed |
| 5 | `write-the-specs` | not entered — the specs exist. Four corrections made under the atomic's own rules: a wrong quoted count, a check re-aimed at behaviour the contract changed, a pinned total replaced by a parsed tally, and two boxes added for defects found in my own code |

### Edits

No edit to the workflow files is needed; two rows fired and both were right.
One row is worth **adding**, and a worker never edits a workflow, so it is
proposed here for `attempt-the-build`, beside the existing `PEARDE_PORT=1` row:

| seen | means | do |
|------|-------|----|
| a check stands a machine-wide guard down (`PEARDE_REAP_GRACE_S=0`, a disabled cap, a bypassed lock) to reach the behaviour it is measuring | the guard is the only thing keeping the action off a neighbouring session's processes, and the check has just removed it machine-wide | scope the action to what the check itself started — a `--pid`, a port, a path filter — and make the narrowing flag **refuse** an unreadable value rather than falling back to "everything". Assert the guard both ways: kept inside it, and expiring outside it, or a widened default keeps every box green while the guard never fires |

## Scores

complexity: 31
blast-radius: high
workflow: probe-then-spec
