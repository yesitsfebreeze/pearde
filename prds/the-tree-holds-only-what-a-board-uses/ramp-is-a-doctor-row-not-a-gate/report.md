# ramp is a doctor row not a gate — analyst report

Verdict: SPECCED

The build went through whole. Every acceptance box in both specs is green in
the lane right now; nothing is left but the commit.

## What the build did

`pearde ramp` used to be loop step 0, held open by `happiness:` — a key
`pearde init` seeded as `0` and only a person could close. Zero meant every
pass on a fresh board called scout's `route.sh` once per gap word, wrote
`.pearde/.state/ask.md` and handed back `ASK` before it had read a single PRD.
The cost fell on the run least able to pay it, and the answer was reliably
*get on with it*.

The key is deleted, not defaulted. `happiness()`, `write_ask()`, `cmd_happy()`
and `cmd_gate()` are gone from `resources/board/ramp.py`; `cmd_measure()` is
the bare verb, printing the gap and, per unanswered job, the candidates with
their exact `npx skills add` line, writing nothing. `have`, `need`, `gap` and
`find` are untouched. `init.py`'s `DEFAULTS` loses its sixth pair.

The reading it used to force moves to `doctor`, one row between `board` and
`vault`, modelled on `plugins`: it runs `ramp gap`, which is tracked paths
against this machine's skill directories and costs no network call. A gap is
`off`, never `broken` — an install is not broken because a field has no
published skill — and the fix line is `pearde ramp`, the reading that does pay
for the routes, run when a person asks for it.

Measured on this repo's own board: `ramp ok · 4 jobs · every one answered`. On
a run-time fixture with a Cargo.toml, five `.rs` files and an empty skill
directory: `ramp off · 0 of 1 job answered · gap: rust`, doctor's exit code
unchanged.

## The one decision the contract did not settle

`cmd_gap` returned **1** whenever a job stood unanswered. That is the last
place the gate could hide: a non-zero exit turns a reading into a check, and
`doctor` — which ignores the code today — would be one line away from going
red because somebody's machine has no Rust skill. It now returns 0, and
`references/parts/ramp.md` says so in as many words. Nothing in the tree read
that exit code; the probe asserts the new one.

## Findings, out of scope

- **Four `index.py check` problems predate this PRD** and are untouched:
  `resources/common.py` is on disk with no row in `references/files.md` (added
  by 7e4d610); `references/files.md` and the `@@view` scope both name
  `@resources/board/hotreload-test.js`, deleted by b1d3f5d;
  `references/parts/commits.md` cites `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`,
  not on disk. Each is a one-line map fix and none belongs to this contract.
- **A board that already carries `happiness: 0`** now carries a key nothing
  reads and nothing reports. Harmless, but a person reading their own
  `settings.md` is misled. A `settings` row that names keys nobody declared is
  a different contract — worth a PRD, not a widening of this one.
- **`references/parts/ramp.md` keeps one mention of `happiness:`** on purpose,
  to say the key was removed and why. The probe's key check is scoped to
  `resources/` and `references/settings.md` for that reason.
- The knowledge query returned 90 notes, 88 strong. No gap, nothing enqueued
  to `.pearde/wiki/pending/`. No fact was learned outside this tree.
- `probe-then-spec` fit the run exactly, step for step. No new workflow file.

## Footprint union

```
resources/board/ramp.py
resources/board/init.py
resources/doctor.sh
references/settings.md
references/files.md
references/parts/loop.md
references/parts/ramp.md
references/parts/doctor.md
references/parts/handles.md
```

## Specs

- `specs/spec01.md` — the gate comes out of the code · complexity 6 ·
  `resources/board/ramp.py`, `resources/board/init.py`
- `specs/spec02.md` — the reading moves to a doctor row, and the loop opens on
  the scan · complexity 9 · `resources/doctor.sh` and the five reference files

Sum 15, two specs — under `split-above: 40` and `specs-above: 6`.

## Reasoning for the scores

**complexity 15.** One module loses four functions and gains one, one default
tuple loses a pair, one doctor row is written against an existing template
(`plugins`), and five reference files are re-worded. No new mechanism, no new
data, no migration.

**blast-radius mid.** `doctor.sh` runs on every install check and `init.py` on
every new board, and `references/parts/loop.md` is the orchestrator's own
contract — its step numbering changes shape. Against that: nothing but
`ramp.py` ever read the key, every invariant and the whole index check are
unchanged, and a board carrying the old key is unaffected.

## Probe

`probe/verify.sh` — 19 checks, all green, every fixture built in a `mktemp -d`
at run time. Runs against this checkout, or `PEARDE_ROOT=<dir>` against
another:

```sh
PEARDE_ROOT=$(pwd) bash .pearde/prds/the-tree-holds-only-what-a-board-uses/ramp-is-a-doctor-row-not-a-gate/probe/verify.sh
```

## Scores

complexity: 15
blast-radius: mid
workflow: probe-then-spec
