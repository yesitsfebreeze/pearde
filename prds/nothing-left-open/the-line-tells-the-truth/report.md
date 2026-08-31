# the-line-tells-the-truth — implementer report

**BLOCKED** — all four contract items are delivered and verified; 7 of 31
acceptance boxes cannot be closed by anything in this footprint. The wall is
the board's move to `.pearde/`, which landed **after** these specs were
written and broke every harness on the board.

- boxes: 24 closed, 7 open (spec01 5/7 · spec02 8/8 · spec03 3/7 · spec04 8/9)
- this PRD's own probe: `85 checks · 80 pass · 5 fail` (was 28 pass on arrival)
- the 5 probe failures and 6 of the 7 open boxes have one cause, named below

## Where each footprint path resolved

The orchestrator asked which root holds each `footprint:` entry.

| footprint entry | root | note |
|---|---|---|
| `resources/board/collect.py` | outer `/Users/feb/dev/infra/pearde` | |
| `resources/board/transitions.py` | outer | |
| `resources/board/plan.py` | outer | |
| `references/parts/progress.md` | outer | |
| `references/parts/statusline.md` | outer | |
| `resources/statusline.sh` | outer | |
| `README.md` | outer | the board has no `README.md` at its root |
| `prds/the-board-runs-itself/transitions-are-commands/probe/verify.sh` | board `/Users/feb/dev/infra/pearde/.pearde` | |
| `prds/the-board-runs-itself/specced-is-a-command/probe/verify.sh` | board | |
| `prds/memos/two-holes-the-flag-probe-found.md` | board, **at a different path** | the file is `.pearde/memos/two-holes-the-flag-probe-found.md` — `memos/` became a sibling of `prds/` in the move, so the footprint spelling is stale by one segment |

## What the tree held when I arrived, and what I changed

The brief said "the tree already holds the probe's uncommitted code". It does
not — a sibling session swept it into **`7b88100` "the board moves to
`.pearde/`, and the knowledge layer lands"** (15:49:30), together with the
`.pearde` migration. So the outer repo read *clean* at my first
`git status --short`, while every one of the four contract items was already
present and committed. Nothing was lost; the diff the specs told me to inspect
is simply empty now.

Committed by that sibling, not by me — verified present and working:

1. `collect.py` `parse_args`/`cmd_collect` — the persona refusal.
2. `transitions.py` `CLAIM_STATES` + the `cmd_set` clause.
3. The `asked`→`done` rename across `plan.py`, `transitions.py`,
   `progress.md`, `statusline.md`, `statusline.sh`, `README.md`, **and** the
   two matchers in `transitions-are-commands` and `specced-is-a-command`.
4. `plan.Flags` / `VISION_FLAGS` / `EXAMPLE_FLAGS`, `transitions.Flags = planlib.Flags`.

Also already landed: spec01's "what is left" — both collect harness `run()`
helpers already carry `PEARDE_AS=engineer`.

**I wrote exactly two files, both on the board:**

- `.pearde/memos/two-holes-the-flag-probe-found.md` — spec02's one remaining
  write. `Open.` in `## Decision` replaced with "Closed, both in
  `nothing-left-open/the-line-tells-the-truth` — hole 1 as its `spec01`, hole 2
  as its `spec02`." The two numbered findings stay as the record.
  `python3 resources/memos.py check .` exits 0, silent.
- `prds/nothing-left-open/the-line-tells-the-truth/probe/verify.sh` — re-aimed
  at the new board layout (below). It is in all four specs' `footprint:`.

I wrote nothing in the outer repo.

## The wall — the `.pearde` move broke every harness on the board

Two independent breakages, both from the move, both landed after these specs:

**a. `ROOT` is one level short.** Every harness derives the repo root by
counting `..` from its own path, which assumed `prds/` sat at the repo root:

```sh
ROOT="$(cd "$HERE/../../../.." && pwd)"   # → /Users/feb/dev/infra/pearde/.pearde
```

That now lands on the board, not the repo, so `$ROOT/resources/board/plan.py`
does not exist. **26 of the 33 harnesses** carry this shape.

**b. `--board <x>/prds` is no longer a board.** `plan.py` now has
`BOARD_DIR = ".pearde"` and `find_board`; a board is passed as the `.pearde`
directory itself. Every harness passes `--board "$D/prds"` and gets
`pearde: no .pearde/ board at <D>/prds`. `plan.py example <d>` likewise now
writes the board *at* `<d>` (settings.md, memos, workflows, prds as siblings),
not at `<d>/prds`.

Measured on arrival, before my first edit:

| harness | baseline | contract wanted |
|---|---|---|
| `the-line-tells-the-truth` (this PRD's own) | `85 checks · 28 pass · 57 fail` | green |
| `collect-keeps-its-word` | `101 checks · 23 pass · 78 fail` | 101/101 |
| `collect-is-a-command` | `133 checks · 31 pass · 102 fail` | 133/133 |
| `transitions-are-commands` | `74 checks · 10 pass · 64 fail` | matcher passes |
| `specced-is-a-command` | `ModuleNotFoundError: No module named 'transitions'` / `no example board at .../.pearde/resources/board/example/prds` | 90/90 |
| `an-unknown-flag-refuses` | `verify: 196 checks · 80 pass · 116 fail` | 196/196 |

None of these are regressions from this PRD. Every failing line names the
missing `$ROOT/resources/...` or the refused `<x>/prds` board — nothing in this
footprint closes any of them.

### Who owns it

`every-document-names-the-path-the-board-is-on` (open, priority 75) scopes
itself to "prose and the strings inside it: `skills/*.md`, `references/**`,
`README.md`, `index.md`, `resources/*.sh`, …" and says the Python under
`resources/board/` "has already been moved and is not in scope". **It does not
name `prds/**/probe/verify.sh`.** So the 33 harnesses' `ROOT` and `--board`
lines are owned by nobody. That is the single highest-value derived PRD on the
board right now: until it lands, no harness on this board can be trusted, and
every future implementer will re-measure the same red.

`resources/statusline.sh`'s board lookup *is* in that PRD's `resources/*.sh`
scope — see the finding below.

## What I did about my own probe

This PRD's harness is mine, and a PRD whose own harness cannot run is not
provable. I re-aimed it and nothing else: `ROOT` one level further up; the
fixture builds the board at `<d>/.pearde`; `B="$D/.pearde"`; PRD files read
through `$B/prds/…`; the transitions log at `.pearde/.state/transitions.jsonl`;
section E's git paths under `.pearde/prds/…`; `serve.py ensure "$D/.pearde"`;
`example <dir>` asserted at `<dir>/settings.md`. No assertion was weakened,
added or removed — the count is still 85.

**28 pass → 80 pass, of 85.** Sections A (collect persona, 15), B (`--force`
clears the claim, 18), C1–C4 and C6–C7 (the `done` term), D (vision/example
flags, 16), E (private index, 17) and F (daemon isolation, 7) are all green.

The 5 remaining failures are C5, G1, G2, G3, G5 — every one of them the
`statusline.sh` finding below.

## Findings — defects outside this footprint, not fixed

**1. `resources/statusline.sh` still resolves the board as `<x>/prds`.**
Lines 79–85 walk up looking for `$d/prds` and set `BOARD="$d/prds"`, which the
scan now refuses. This is the `.pearde` move, not the `asked`→`done` rename
spec03 owns ("nothing else in those files moves"), and `resources/*.sh` is
explicitly in `every-document-names-the-path-the-board-is-on`'s scope. It is
the sole cause of probe C5/G1/G2/G3/G5 and of spec03's statusline box. The fix
is the same board-discovery change `plan.py` already made.

**2. `plan.py example` writes no `.state/`, and `collect` crashes on it.**
On a fresh `example` board, `collect <prd> --as engineer --trust` writes
`state: done` into the PRD and *then* dies:

```
FileNotFoundError: [Errno 2] No such file or directory:
  '<board>/.pearde/.state/transitions.jsonl'
```

A partial write — the PRD moved, the log did not. `state-dir-belongs-to-the-board`
(open, priority 85) is the owner. My fixture works around it with one
`mkdir -p "$d/.pearde/.state"`, marked in the harness with the PRD's name.

**3. Both repo gates were red before my first edit, on files I never touched.**
`python3 resources/index.py check` exits 1: `references/files.md` references
`@skills/*.md` "not on disk" (the `skills/` → `references/` move, `3b829fd`),
and `resources/pearde.py` references `@prds/the-board-runs-itself/one-command/prd.md`
(the `.pearde` move). `bash resources/doctor.sh`: `questions broken — 7 rounds
the user cannot act on`, `view off`, `harnesses off`, and doctor resolves the
board to `/Users/feb/dev/infra/prds` — one directory too high, the same
migration. Grepped: **no line in either gate names any file in this
footprint.**

**4. A sibling landed 47 outer files mid-run.** Between my baseline and my last
check, `every-document-names-the-path-the-board-is-on` wrote 47 files in the
outer repo, two of them mine: `resources/board/collect.py` and `README.md`.
Checked for collision — `collect.py`'s hunks are **docstring prose only**
(`prds/.claims/` → `.pearde/.claims/`), zero lines touching the persona
refusal; `README.md` is the prose rename. `plan.py`, `transitions.py`,
`statusline.sh`, `progress.md` and `statusline.md` are untouched by them.
Re-ran the probe after: 80/85, unchanged. Outer HEAD also moved to `2d35439`
during the run.

**5. Daemon registry is clean.** `serve.py status` after the run lists only
real boards — `pearde → /Users/feb/dev/infra/pearde/.pearde` — no fixture
leaked. No `pearde-index-*` scratch left behind. All probe work ran with
`PEARDE_PORT=1`.

## Open boxes, and what closes each

| spec | box | closed by |
|---|---|---|
| spec01 | `collect-keeps-its-word` 101/101 | the harness `ROOT`/`--board` sweep |
| spec01 | `collect-is-a-command` 133/133 | same |
| spec03 | statusline renders `▸pearde <rd>/<rn>` | finding 1 — `statusline.sh` board lookup |
| spec03 | `specced-is-a-command` 90/90 | the sweep |
| spec03 | `transitions-are-commands` matcher passes | the sweep — the matcher itself already reads `· done`, confirmed by inspection |
| spec03 | `git diff HEAD --` the four docs holds only rename hunks | unclosable as written: the rename is **committed** (`7b88100`), so that diff is empty; it now holds the sibling's `prds/`→`.pearde/` hunks instead |
| spec04 | `an-unknown-flag-refuses` 196/196 | the sweep — and this harness is **not** in this PRD's footprint |

## Proof of the four contract items

Run by hand on a fresh `example` board at `<d>/.pearde`, and mechanised as
sections A–D of this PRD's probe.

**1. `collect` refuses without a persona.**

```
$ env -u PEARDE_AS python3 resources/board/collect.py finished --board <d>/.pearde
exit=1
collect: refused — persona: `--as <id>` on the line, or PEARDE_AS in the environment
  — `export PEARDE_AS=engineer` is the line `install --apply` prints beside the alias
$ git status --porcelain          # in <d>: empty — nothing written
$ grep -c 'persona: ' resources/board/collect.py
0                                  # the text is imported, never copied
```

`--snapshot` refuses identically (exit 1). `--bogus` still exits 2.
`PEARDE_AS=skeptic … --dry --trust` prints
`dry · ▸ finished: claimed → done · … · as skeptic`.

**2. `set --force` clears a claim the target cannot carry.**

```
$ python3 resources/board/brief.py building --board <d>/.pearde --as engineer
pearde brief: skipped building — held — building is `claimed`, `claim: worker-building …`
$ python3 resources/board/transitions.py set building open --force --as engineer --board <d>/.pearde
▸ building: claimed → open · forced · done 2/8 · 15% · open 4/8 · 50% · ready 2 · blocked 4 · collect 1 @1 workers · round file owed · as engineer
$ grep -c '^claim: ' <d>/.pearde/prds/building/prd.md
0
$ python3 resources/board/brief.py building --board <d>/.pearde --as engineer
# brief building · analyst · as engineer · …     ← no longer held
```

`--dry` keeps the claim; `→ analyzing` keeps it; `→ deferred`/`→ shelved` clear
it; forcing the state it already holds is refused with the claim intact.

**3. The first term is `done`.**

```
$ python3 resources/board/plan.py scan <d>/.pearde
progress: done 2/8 · 15% · open 3/8 · 38%
$ grep -rl -E '"asked"|<ad>|asked [0-9]+/[0-9]+' resources references README.md
(nothing — exit 1)
```

Both committed matchers already read the new word:
`transitions-are-commands/probe/verify.sh:74` matches `"▸ next: specced → claimed · done "*`,
`specced-is-a-command/probe/verify.sh:126` matches `'^▸ big/second: analyzing → specced · done'`.

**4. `vision` and `example` declare their flags.**

```
$ python3 resources/pearde.py vision --bogus --board <d>/.pearde   → exit 2
pearde vision: unknown flag --bogus — vision takes: --board, --json, --next, --check
$ python3 resources/pearde.py example --bogus                      → exit 2
pearde example: unknown flag --bogus — example takes: no flags
$ python3 resources/pearde.py vision --board                       → exit 2
pearde vision: --board takes a value — vision takes: --board, --json, --next, --check
$ python3 resources/pearde.py set --bogus x open --board <d>/.pearde → exit 2
pearde set: unknown flag --bogus — set takes: --as, --board, --worker, --force, --dry
$ python3 -c "… import transitions, plan; print(transitions.Flags is plan.Flags, …)"
True --board, --json, --next, --check no flags
```

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | **passed with a finding.** PRD, four specs and every `@` reference resolved. Two footprint paths did not resolve as written: `prds/memos/…` is now `memos/…`, and the whole footprint spans two repos. `git status --short` recorded before the first edit — the outer repo was *clean*, which the brief did not predict. |
| 2 | `capture-the-harness-baseline` | **passed, baseline all red.** `find prds -name verify.sh` listed 33. Ran the 5 in footprint plus `an-unknown-flag-refuses`; every one already failing before my first edit, all on the `.pearde` migration. `index.py check` (exit 1) and `doctor.sh` recorded, both red before my first edit, neither naming this footprint. |
| 3 | `attempt-the-build` | **nothing to build.** All four items were already committed by a sibling in `7b88100`. Confirmed each by hand on a fixture board, then re-aimed this PRD's own probe so the confirmation is repeatable. Edits made in place in footprint files, never staged under `probe/` — every remaining change was an edit to an existing file. Fixtures built under `mktemp -d`, removed at exit, `PEARDE_PORT=1` throughout. |
| 4 | `re-run-the-harnesses` | **no back-edge taken.** Own probe 28 → 80 of 85, a rise from re-aiming my own harness, stated as mine. The five committed harnesses stand exactly at their baselines — not moved by me in either direction. Per this atomic's own row ("every failing line names a file outside your footprint… report it as a finding and do not back-edge"), reported, not repaired. |
| 5 | `write-the-specs` | **not run.** The brief's tail dispatches this as an implementer on an already-specced PRD; the specs exist and were not mine to rewrite. |

### Edits

The atomics sent me somewhere their text does not cover. Replacement text, per
`@references/workflow.md` — I edited no workflow file.

**1. `read-the-contract` → `## Fails when`, new row.** The atomic assumes one
repo. This board's `repo:` line names `.pearde`, which holds its own `.git`,
while most of the footprint lives in the outer checkout — and step 1's
`git status --short` is meaningless unless it is run in both.

| seen | means | do |
|------|-------|----|
| a `footprint:` path is absent under the `repo:` root | the board is a `.pearde/` inside a code repo, and the footprint spans both | resolve each entry against the board root and the checkout above it, take whichever holds it, and record `git status --short` **in both** — one root's clean tree says nothing about the other's |

**2. `read-the-contract` → `## Fails when`, new row.** The `prds/memos/…`
footprint entry pointed at nothing; the file had moved to `memos/…` when the
board was restructured. The atomic has no row for a footprint spelling that a
layout change made stale.

| seen | means | do |
|------|-------|----|
| a `footprint:` path does not exist and no sibling is writing it | a layout change moved the file after the specs were written | `find <board> -name '<basename>'`; if exactly one match, take it as the same file, do the contracted work there, and name both spellings in the report — a missing footprint path is a stale spelling far more often than a file to create |

**3. `capture-the-harness-baseline` → `## Fails when`, new row.** Every row in
this atomic assumes a mostly-green baseline with a failure or two to note. This
board's baseline was 6 of 6 red from one cause, and the atomic gives no
guidance for that.

| seen | means | do |
|------|-------|----|
| **every** harness you baseline is red, and the failing lines share one cause outside your footprint | a layout or path migration landed between spec-writing and dispatch; the harness set is measuring the migration, not your unit | record the shared cause once instead of per-harness, verify your own contract items by hand on a fixture, and report the sweep that repairs the set as its own PRD — do not repair a subset, a half-swept harness set is worse evidence than a uniformly red one |

**4. `attempt-the-build` → `## Fails when`, new row.** The brief promised "the
tree already holds the probe's uncommitted code"; a sibling had swept it into
its own commit, so `git diff HEAD` was empty and the work looked lost.

| seen | means | do |
|------|-------|----|
| the brief says the probe's code is uncommitted, and `git status --short` is clean | a sibling session committed the whole tree, your hunks with it | `git log -1 -- <footprint path>` and read the file itself before concluding anything is missing; if the behaviour is present, the work stands — record the commit that took it, and read every spec's "what already stands" against the **file**, never against a diff |

**5. `write-the-specs` → `## Use when`, clarification.** `probe-then-spec` is
an analyst route, but this brief handed it to an implementer on a PRD already
in `specced`, so step 5 was unreachable by construction. The `## Use when`
block should say that an implementer handed this route runs steps 1–4 and stops,
and that step 5 is the analyst's alone — otherwise every implementer on this
workflow reports a step it could never have run.

## What unblocks this PRD

One sweep, as its own PRD: re-aim all 33 `prds/**/verify.sh` at the `.pearde`
layout — `ROOT` one level up, `--board <x>/prds` → `<x>/.pearde`, fixture
boards built at `<d>/.pearde`, PRD files read through `<board>/prds/…`. This
PRD's own probe is a worked example of exactly that change; the diff on it
shows every shape the sweep needs. With that landed and finding 1 fixed, all
7 open boxes here close with no further code change.
