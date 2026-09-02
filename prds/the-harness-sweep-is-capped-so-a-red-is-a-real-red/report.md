# the-harness-sweep-is-capped-so-a-red-is-a-real-red — implementer report

Verdict: DONE

All twenty acceptance boxes across the three specs are ticked and quoted. The
one that was open — spec01's acceptance sentence — was closed by this pass,
against the bar the user settled at the drill of 2026-09-02 (`## Answers` Q1):
a **rate cut**, not an elimination. The earlier `Verdict: QUESTION` is stale;
the question it asked has been answered on the PRD and the box was measured
against the answered bar without being reworded or lowered.

**The measurement.** Five capped `doctor --harnesses` runs produced **zero**
contention-class reds. One uncapped run produced **one**. Five sweeps against
one, zero against one — the per-run rate is cut by at least fivefold, which is
the bar. No survivor in the contending class remains to name.

## Box status — 20 of 20

| spec | boxes | note |
|---|---|---|
| spec01 — the cap | 7/7 | the last open box closed this pass; see the quoted block below |
| spec02 — the view-row ports and the leak | 7/7 | unchanged, carried from the previous pass |
| spec03 — the spare-port TOCTOU | 6/6 | unchanged, carried from the previous pass |

`grep -c '^- \[ \]'` over `specs/*.md` → `0`, `0`, `0`.

## spec01's `## Verify and Proof` block — run once, in full

Extracted with `awk` and run the way `collect` runs it
(`bash -c "set -o pipefail; …"`) from `/Users/feb/dev/infra/pearde`. It took
roughly twenty minutes: five capped sweeps, two serial re-runs over all 52
harnesses, one uncapped sweep.

```
16 checks · 16 pass · 0 fail · 0 skip
probe harness complete
two serial re-runs agree — that set is the genuine one
capped: 0 contention red(s) across five runs
uncapped: 1 contention red(s) in one run
.pearde/prds/nothing-left-open/the-line-tells-the-truth/probe/verify.sh
per-sweep contention reds — capped: 0/5 · uncapped: 1/1
89:  parallel but caps how many are in flight at once — `PEARDE_HCAP`, default
101:  rather than testing. Raising `PEARDE_HCAP` trades isolation for time,
MET: 0 over five capped runs vs 1 over one uncapped run — the per-run rate is cut at least fivefold
BLOCK_EXIT=0
```

The block ends on the bare test `[ "$CAPN" -le "$UNCN" ]`, last, so that line
decides the exit — `BLOCK_EXIT=0` is the assertion passing, not a swallowed
status. `index.py check` and `memos.py check` are inside the block and both ran
silent; a line from either would have appeared above `MET:`.

The uncapped run's one red is
`.pearde/prds/nothing-left-open/the-line-tells-the-truth/probe/verify.sh` —
the harness the PRD body already names as a proven sweep artifact, green at
85/85 when run alone. That is the class being removed, observed being removed.

## Survivors — named

**In the contending class: none.** Zero across five capped runs. There is
nothing left to name under the box's own words.

**Outside it, one red persists**, and it is the remainder the PRD already
routes to `two-self-tests-fail-on-timing-not-on-code`. A capped sweep taken
immediately after the block, to enumerate every red rather than only the
contending ones:

```
harnesses   broken  9 of 52 green · 43 unpinned · 91s · 1 failed
.pearde/prds/scan-parses-the-board-once-and-caches-it-by-mtime/probe/verify.sh — exit 1 · FAIL: warm not faster than cold
```

That is a wall-clock assertion — warm cache against cold — and no cap above one
settles it. Not this PRD's, not touched.

**`the-fixtures-meet-the-tool` — expected red, read green.** The brief expects
it red under every sweep, since it reads the whole working tree's git diff and
five files are uncommitted. It did **not** appear in this pass's sweep, and run
alone it reads `35 checks · 35 pass · 0 fail`, exit 0. Recorded as it measured,
not as it was predicted. It is outside the contending class either way and is
not evidence for or against the cap.

## The tree

`git status --short` at the repo root lists the same five files it listed
before this pass:

```
 M references/parts/doctor.md
 M references/parts/workers.md
 M resources/board/brief.py
 M resources/board/collect.py
 M resources/doctor.sh
```

`resources/doctor.sh` carries this PRD's cap **and** a neighbour's hunk at
577-595; that hunk was not read, not touched and not staged. This pass wrote
exactly two files, both inside this PRD's folder: `specs/spec01.md` (one
character, `[ ]` → `[x]`) and this report. Nothing was committed.

## Workflow probe-then-spec

Rows 1-3 and 5 are carried from the previous pass, which built the whole unit;
they are that worker's record, not re-run here. **This pass re-ran step 4 —
`re-run-the-harnesses` — and nothing else**, which is the whole of the bounded
dispatch it was given.

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | ok (previous pass) — prd.md, three specs, the analyst's report; `git status --short` recorded before the first edit. Re-read this pass for `## Answers` Q1, which had landed since. |
| 2 | `capture-the-harness-baseline` | **partial, and the previous pass's error** — probe-file baselines were taken as inherited on the false premise that `.pearde` was untracked. It is a linked worktree with 49 harnesses in its own `HEAD`; a real pre-edit baseline was available and was not taken. Not re-takeable now — the build is on disk. |
| 3 | `attempt-the-build` | ok (previous pass) — edits in place in existing footprint files, plus two new checks in this PRD's own probe. No new files outside `probe/`. |
| 4 | `re-run-the-harnesses` | **ok, re-run this pass** — spec01's block once in full: five capped sweeps, two agreeing serial re-runs, one uncapped run, exit 0. Plus one enumerating capped sweep to name every red. No harness outside this PRD was edited. |
| 5 | `write-the-specs` | n/a for this role. Its box-6/box-7 checks caught two spec-block defects in the previous pass that would have passed `collect` while asserting nothing. |

### Edits

One row, carried unchanged from the previous pass, against `write-the-specs`.
This pass found no new failure the atomics caused. (The previous pass's edit
against `capture-the-harness-baseline` stays **withdrawn** — it encoded a false
premise about `.pearde` being untracked.)

**`write-the-specs` — `## Fails when`, generalise the `grep -c` row.** The
existing row names `grep -c`/`grep -vc` whose passing value is `0`. Two wider
shapes bit this PRD, and the second is the dangerous one:

> | seen | means | do |
> |------|-------|----|
> | a block exits non-zero on the result that means it passed | a command whose **passing** result is "nothing matched" — `grep -c`, `grep -vc`, `ls <glob>`, `find … \| wc -l` — exits non-zero on exactly that result | guard the *producer*, not the pipeline: `{ <cmd> \|\| true; } \| wc -l` |
> | a block exits **0** while a line in it printed a failure | the assertion is written `[ <test> ] && echo "<the good news>"`, or `<probe> && echo BAD \|\| echo OK`. Neither can fail a block: a false test prints nothing and the next command's status becomes the block's, and the `&&…\|\|` pair always exits 0 | put the assertion **last** and write it bare — `[ ! -s "$f" ]` — or accumulate a counter in the loop and end on `[ "$N" = 0 ]`. Then run the block the way collect does (`awk` it out, `set -o pipefail`) **against a tree where the check should fail**, and confirm it does |

## Findings carried forward

Carried by name from the previous passes. None is closed by this one.

- **Finding 1 — `wait -n` does not exist on this shell.** bash 4.3; `/bin/bash`
  on macOS is 3.2.57. Written as the old comment specified, the cap would have
  broken `doctor` on every macOS box. On record as `[[260902-e933]]`. Still
  asserted green by the probe.
- **Finding 2 — no harness that reports skips can pin its denominator.**
  `doctor` recognises only the literal `$((PASS+FAIL))`. This PRD's own harness
  pins honestly on `$((PASS+FAIL+SKIP))` and is reported unpinned for it. Open,
  and visible in this pass's sweep as `43 unpinned`.
- **Finding 3 — `the-fixtures-meet-the-tool` reads the whole working tree's
  diff**, so its result moves with any neighbour's uncommitted work. It read
  green in this pass. Untouched.
- **Finding 4 — the board was written while it was measured** during the
  analyst's pass (48 → 51 → 52). The sweep now counts 52 and was quiet through
  this pass's runs.
- **Finding 5 — two fixture defects as method.** A shared counter file
  under-reports concurrency; a port holder with `listen(1)` reads as *free*.
  Both still true.
- **Finding 6 — the timing residue is real and routed.**
  `scan-parses-the-board-once-and-caches-it-by-mtime` fails on `warm not faster
  than cold` under a capped sweep. Outside every footprint here; belongs to
  `two-self-tests-fail-on-timing-not-on-code`.

**Not re-filed:** the flaky neighbour harnesses are outside this contract and
the orchestrator is routing them. Nothing has been filed by this pass.

## Scores

complexity: 18
blast-radius: mid
workflow: probe-then-spec
