Verdict: DONE

# The daemon's liveness moves onto the board — implementer report

Second pass of `probe-then-spec`. The analyst pass built the change and wrote
`spec01`; none of it was committed, so this pass inherited the code in the lane
and owed it the three checks the analyst could not finish, the real pre-edit
baseline the analyst says it skipped, and the `Fails when` reading of the block
that already stood. One line of behaviour was added — the PRD's own
`## Fails when` clause, which the standing build did not implement. See
`## The one thing that was still missing`.

Lane `/Users/feb/dev/infra/pearde/.pearde/.lanes/the-daemon-s-liveness-moves-onto-the-board`,
branch `lane/the-daemon-s-liveness-moves-onto-the-board`, one modified file,
`resources/board/serve.py`, +109/-2.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | read-the-contract | pass, via the table's last row: the lane holds no board, so the live board was symlinked in at `<lane>/.pearde` (`/.pearde` is gitignored there). `git status --short` recorded in both roots before the first edit — lane: `M resources/board/serve.py` alone; checkout: ten modified files, `resources/board/serve.py` **not** among them at that moment |
| 2 | capture-the-harness-baseline | pass on the second attempt. The first pre-edit tree was a `git archive HEAD` extraction and carried no `.git`, which reddens every harness that runs git at `ROOT`; that baseline was unusable and was thrown away. A `git clone --no-hardlinks` of the lane, plus the gitignored bundles a clone omits, gave the real one. See `### Edits` |
| 3 | attempt-the-build | entered as the route's second pass (`attempt-the-build`'s first `Fails when` row): spec01's own footprint was already dirty, so this was re-measurement rather than a rebuild — except for the one clause in `## The one thing that was still missing`, which no code implemented |
| 4 | re-run-the-harnesses | pass. The seven harnesses that read the footprint are identical before and after; the whole-board sweep ran to a `harnesses` row once per tree, on the third attempt each, and every count that moved is attributed by name to a neighbour or to the clone. See `## Harness baseline` |
| 5 | write-the-specs | applied as the route says for a second pass — no spec authored, its `Fails when` table read against the block that already stood. Two of its rows fired on spec01's `## Verify and Proof`; both are fixed and the block now exits 0 the way `collect` runs it |

No back-edge was taken.

### Edits

Replacement text for what the atomics cost this run. Not applied — the brief
forbids editing the workflow files.

**`capture-the-harness-baseline`, `## Done when`, the "resuming a killed run"
paragraph.** It names `git clone --no-hardlinks` as the recovery for an
uncommitted earlier build, which is right, but says nothing about what a clone
does *not* carry, and the first baseline this run took was worthless for it.
Add after "`git clone --no-hardlinks` recovers the pre-edit tree only where the
harnesses are tracked **in the repo you cloned**.":

> Recover it with `clone`, never with `git archive`: an extracted tree has no
> `.git`, and on a board whose harnesses run `git` at `ROOT` that alone moves
> dozens of counts — a baseline that reads red for the absence of a repository
> is not a baseline. Then put back what a clone leaves out before measuring
> anything: the gitignored third-party bundles (`resources/board/node_modules`,
> the vendored plugin directories) the js and view harnesses need, and a symlink
> to the live board at the clone's root, because the clone has none and every
> board-rooted line in a harness would otherwise answer about nothing. Measured
> here: with `archive` and no bundles, four of seven harnesses moved and read as
> regressions; with `clone` plus both, all seven read identically before and
> after.

**`capture-the-harness-baseline`, `## Fails when`, new row.** Nothing warns that
the tree under measurement must not be walked recursively once a board has been
linked into it:

> | `diff -r <clone> <lane>` never returns | the board symlinked into the tree points at a directory holding `.lanes/<slug>`, which is the tree itself — `diff -r` follows it and walks the same path forever | compare with `git diff` between the two roots, or pass `-x .pearde -x pearde`; never recurse a tree a board has been linked into |

**`re-run-the-harnesses`, `## Fails when`, new row.** Every row in that table
reads a neighbour who *landed files*. The neighbour that cost this run was one
**running the same board-wide sweep at the same time**, and there is no row for
it:

> | a harness exits 137 or 143, or `doctor.sh --harnesses` dies before its `harnesses` row prints | another session is running the same sweep over the same board, and that sweep's own population includes harnesses that `kill` process lists they read out of `ps` — so the two runs stop each other's fixtures, and a signal exit is contention, not a fault | `ps -eo pid,command \| grep 'doctor.sh --harnesses'` before quoting any count; where a second sweep is up, re-run the harness rather than record it — a signal exit is not a count — and say in the report how many concurrent sweeps the run saw. Never compare a signalled run against an unsignalled one. Measured here: the same seven harnesses gave four signal exits under three concurrent sweeps and none under one |

**`attempt-the-build`, `## Fails when`, new row.** The table has a row for
standing a machine-wide guard down. It has none for the cleanup afterwards,
which is the same failure with the sign flipped, and is the one this run
committed:

> | a probe leaves a daemon behind and the worker clears it with a pattern kill (`pkill -f serve.py`) | the pattern names the *program*, not this probe's instance of it, so it reaches every session's daemon and the machine's real service with them — the same machine-wide reach the guard row forbids, taken during cleanup instead of during the check | kill only pids the probe itself recorded, put that kill inside the probe, and assert it (`kill -0` must fail after); never a pattern. Where the real service has already gone, `serve.py ensure <board>` from the board's own root brings it back under the same name — and say in the report that it was stopped and restored, and that every *other* board the old daemon watched has lost its registration and only its own session can restore it |

**`attempt-the-build`, `## Done when`, second bullet.** The bullet allows a probe
with no `verify.sh` where the spec's block invokes it by name — this PRD's shape
— but says nothing about how such a probe finds the tree it is to measure. Add:

> A probe invoked by a spec block takes its tree the way the board's harnesses
> do — `ROOT="${PEARDE_ROOT:-$(dirname "$BOARD")}"` with `BOARD` found by walking
> up from `$0` — never a lane path written out in full. A probe holding an
> absolute lane path passes today and measures a directory that stops existing
> the moment the lane merges.

## The one thing that was still missing

The PRD's `## Fails when` is a contract clause, not a caveat:

> Two sessions on one board: both write the file, one pid wins. The writer takes
> the file only under the same lock the state writes take (@@pass), and a loser
> reads the winner's file rather than overwriting.

The standing build wrote unconditionally on every `ensure`. The analyst's report
argues the race is harmless because both writers ask the same live daemon and so
produce identical bytes — true, and not what the clause asks: it asks that the
loser *read* rather than overwrite.

`@@pass` resolves to `references/parts/pass.md`, which names no lock, and there
is no `flock`, `fcntl` or `LOCK_EX` anywhere under `resources/`
(`grep -rn "flock|LOCK_EX|import fcntl" resources` returns nothing). So "the same
lock the state writes take" is `common.atomic_write`'s tmp-then-`os.replace`, and
there is no second lock to take. What the clause still buys, and what this pass
added, is one guard in `write_view`:

    rec = {"pid": pid, "port": port, "started_at": started_at, "board": name}
    if read_view(board) == rec:
        return

A file already saying these exact bytes is left alone, so one `os.replace` per
fact ever lands and the loser of the race reads the winner's file. A file saying
anything else — a pid that has since died, a port that moved — is stale by
definition, and this write is the rewrite `## The change` requires of the next
`ensure`. Probe check `1d` is the witness: a second `ensure` on a board that
already carries the file leaves its mtime untouched.

## Boxes — spec01

All six ticked, each against output quoted in the box.

1. `ast.parse` — exit 0.
2. and 3. `probe.sh` — `probe: 9 passed, 0 failed`, both scenarios. Scenario 1
   writes `view.json`; `status` names the same pid and port;
   `PEARDE_REAP_GRACE_S=1` with a 2s sleep shuts the window provably, and the
   verdict is `serve: keeping pid … — named by project's .state/view.json —
   file-backed, no grace needed`. Scenario 2 deletes the board first and still
   gets `serve: would stop pid … — watching no board`. The probe now also
   asserts it left no daemon behind (`2c`).
4. `reap --dry-run` over the six live machine daemons, run from a clone of the
   pre-edit tree and from the build: `serve: 0 of 6 stranded` both times, exit 0
   both times, every pid kept in both. The four carrying no `view.json` keep
   their reason verbatim, the real machine daemon among them
   (`pid 3707 · port 8443 — watching 2 live board(s): pearde, forkprobe`), as
   does the one inside the window (`started 47s ago — inside the 60s grace a
   session start needs to register its board`). The two whose reason moved are
   the two that do carry a file — that is the change.
5. `doctor.sh --harnesses` — see `## Harness baseline`.
6. `index.py check` — three lines, all present in the pre-edit run too, none
   naming `resources/board/serve.py`.

The spec's `## Verify and Proof` block exits 0 the way `collect` runs it:
`bash -e -o pipefail -c "$(awk '/^```sh/{f=1;next} /^```/{f=0} f' spec01.md)"`.
Both of its static guards were negative-tested in a scratch clone — appending a
line to `doctor.sh` and lowering the shipped grace each make the block exit 1 —
so neither is a check that cannot fail.

## Harness baseline

Both trees are the lane's: a `git clone --no-hardlinks` of it at `HEAD` (the
pre-edit tree, with `node_modules`, the vendored plugin bundles and a board
symlink put back) and the lane itself. They differ in exactly one file,
`resources/board/serve.py`. No tree was swapped under a running check —
`PEARDE_ROOT` names which one each run measures, and all seven harnesses honour
it (`grep -L PEARDE_ROOT` over the set returns nothing).

The seven board harnesses that spell the footprint, run sequentially, before and
after:

| harness | before the first edit | after |
|---|---|---|
| `a-session-start-brings-the-board-up` | 43 checks · 37 pass · 6 fail · 1 skip | identical |
| `one-page-that-says-whats-up` | 31 checks · 28 pass · 3 fail | identical |
| `seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green` | 37 checks · 24 pass · 12 fail · 1 skip | identical |
| `the-board-runs-itself/the-next-line-runs` | 96 checks · 95 pass · 1 fail | identical |
| `the-board-runs-itself/the-page-shows-the-round` | 29/29 checks pass | identical |
| `upgrade-leaves-the-memo-index-stale` | 40 checks · 18 pass · 22 fail · 0 skip | identical |
| `leaked-background-services-outlive-their-fixtures` | exit 0 | exit 0 |

Every red above is red **before the first edit** and is a finding about its own
PRD, not about this one.

The two static halves of box 5, which are what this footprint actually owes the
sweep's `reap` line:

- `git diff --stat -- resources/doctor.sh` in the lane is empty — doctor's
  flag-less `reap` is the one it has always run.
- `REAP_GRACE_S = float(os.environ.get("PEARDE_REAP_GRACE_S", "60"))` reads
  identically at `HEAD` (line 229) and in the build (line 230). The shipped
  grace is kept; only the probe lowers it, in its own environment, and only
  behind a `--pid` narrowing.

### The whole-board sweep, both trees

Both ran to a `harnesses` row on the third attempt each — the first two
attempts on the pre-edit side died before printing one, under three to eight
other sessions running the same sweep over the same board at the same time.

| | pre-edit clone | build |
|---|---|---|
| `harnesses` | `broken  3 of 98 green · 86 unpinned · 653s · 62 failed` | `broken  4 of 99 green · 87 unpinned · 872s · 60 failed` |
| `jstests` | `ok  viewtest.js --example · 49/49 passed` | `off  node found, playwright-core missing` |
| leaked services reaped | none on the row | none on the row |

The totals moved, and none of the movement is this footprint's. Read by name
instead of by total — 64 failing harnesses before, 62 after:

- **One name is new**, `prds/the-lifecycle-contract-and-purge-reclaims-it`. It
  did not exist when the baseline was taken (the checkout carries an untracked
  `resources/board/purge.py` from the same neighbour). Per
  `re-run-the-harnesses`, a harness with no baseline is recorded as new and
  compared to nothing.
- **Three names left the list**, and a sequential re-run of each — one harness
  at a time, no sweep running — attributes all three away from this change:
  - `the-board-runs-itself/the-page-shows-the-round`: `29/29 checks pass` in
    both trees. Its red in the pre-edit sweep was contention.
  - `the-harness-sweep-is-capped-so-a-red-is-a-real-red`: exit 0 in both trees.
    Same.
  - `the-daemon-must-not-write-into-a-board-path-it-no-longer-own`: this one
    does read the daemon and did flip — `10 checks · 9 pass · 1 fail` in the
    clone, `10 · 10 · 0` in the lane. It is still not the change: copying
    **only** the built `serve.py` into the clone and re-running leaves it at
    `9 pass · 1 fail`, on the same check (`FAIL save_entry still records a real
    board`). The one variable that moves it is the clone, not the edit.
- **`jstests` reads `off` in the build's run** for `playwright-core missing`,
  and that is the clone's incompleteness showing from the other side: the lane
  *has* `resources/board/node_modules/playwright-core` and the clone does not.
  The row reads no file in this footprint either way.
- **No failing harness names this PRD** in either run — `grep -c
  'the-daemon-s-liveness'` over both failing-name lists is `0` and `0`.

The clone artefact above is worth one more line on the
`capture-the-harness-baseline` edit: a clone can redden a harness that writes
its fixtures under `ROOT`, for reasons that have nothing to do with the
footprint, so **isolate every flip by copying only the footprint file into the
clone and re-running** before calling it a landing. That single swap is what
turned an apparent green-flip here into a clone artefact.

## Incident — an unscoped `pkill` stopped every daemon on this machine

Mid-run I ran `pkill -f 'serve.py run' -P 1` to clear a daemon my own probe had
leaked. `-f` matches the *program*, not my instance of it: it stopped every
`serve.py run` on the box — the machine's real view service on 8443 among them,
other sessions' fixture daemons, and four of my own background tasks with them.
`serve.py status` then read `serve: not running`.

Restored at once with `python3 resources/board/serve.py ensure
/Users/feb/dev/infra/pearde/.pearde`, from the checkout's own code rather than
the build, so no `view.json` was written into the real board:
`serve: up on http://127.0.0.1:8443 · pid 59189`,
`pearde … /Users/feb/dev/infra/pearde/.pearde`, and
`ls .pearde/.state/view.json` still says no such file.

**Not restored:** the daemon that died was also watching a board named
`forkprobe` belonging to another session; that registration is gone and only
that session's own `ensure` can bring it back. Any session whose fixture daemon
died in that window lost it to this, not to its own code. The probe now kills
only the pid it recorded and asserts the kill (`2c`), and the
`attempt-the-build` edit above is the rule that should have stopped me.

## The merge, proved rather than assumed

`resources/board/serve.py` was clean in the orchestrator's checkout when this
run started and is **modified there now** — a neighbour added `ask_digest` and
touched `Board` and `watch()`, at lines 295, 442 and 797. `resources/doctor.sh`
is modified there too. Neither is mine; neither was touched here.

Checked the way `read-the-contract`'s table asks rather than by eye: cloned the
checkout to scratch, committed the neighbour's working copy there, then
`git apply --3way` of this lane's diff — `Applied patch to
'resources/board/serve.py' cleanly.` My hunks (156, 262, 533, 1195, 1855, 2005,
2048) and theirs do not touch. The merge needs nothing cleared.

## Findings

Carried forward from the analyst pass, both still standing, neither fixed:

- **`serve.json` already exists and is close kin.** `entry_path`/`save_entry`
  write `.state/serve.json` — `{path, name, port, at}` — from the daemon's own
  thread on `/register`. It carries no pid and neither `reap` nor `cmd_status`
  consults it. `view.json` is deliberately a second file: different writer
  (client, from `ensure`), different purpose (the pid liveness is judged by).
  Nobody should merge the two as a cleanup without weighing that.
- **`knowledge.py query` returned 103 "strong" hits and nothing on point** for a
  specific, on-repo question about this daemon's lifecycle, and enqueued no gap.
  That is a finding about the ranker, not a question of this PRD's.

New here:

- **The board-wide harness sweep barely survives another session running it.**
  `ps` showed between three and eight sessions running
  `bash resources/doctor.sh --harnesses` over this board at once. Under that,
  two `doctor.sh --harnesses` runs were SIGTERMed before their `harnesses` row
  printed and two of the seven focused harnesses came back 137 and 143; it took
  three attempts per tree to get a row at all, and even the rows that landed
  carry reds that a sequential re-run turns green. The board owes itself either
  a lock on that sweep or a written rule that it is single-writer — same class
  as the memo `a-harness-that-reads-the-whole-checkout-is-not-a-harness`, and
  the reason the `re-run-the-harnesses` edit above exists.
- **This PRD has a `probe/probe.sh` and no `probe/verify.sh`, so nothing on the
  board will ever run it again.** Allowed — `attempt-the-build`'s `Done when`
  permits a probe the spec's block invokes by name — but the behaviour this PRD
  adds then has no regression net in the sweep. Adding one would also move the
  sweep's own `HN`, which is why it was not done inside this pass's baseline. It
  belongs to whoever closes the PRD.
- **The whole PRD directory is untracked in the board's own repo**
  (`git -C .pearde status --short` → `?? prds/the-daemon-s-liveness-moves-onto-the-board/`),
  so any harness fixture that copies from `git ls-files` cannot see the probe.
- **`grammar.py show "fails when"` → `is not defined on this board`.** The
  phrase heads a section in every PRD and decides, as it did here, whether a
  clause is a caveat or a contract. It should have a term.

## Health floor

Nothing in the footprint was under the floor and the brief listed nothing.
`doctor`'s `health` row reads `189 files · 6 under 40` in both sweeps, and
`resources/board/serve.py` is not among the six. (It read `188` in the very
first run of this session and `189` afterwards — a neighbour added a file
mid-run, not this footprint.) Nothing was refactored.

## Scores

complexity: 18
blast-radius: mid
workflow: probe-then-spec
