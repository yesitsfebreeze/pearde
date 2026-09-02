# a-session-start-brings-the-board-up — implementer

Verdict: DONE

worker: impl-session · as engineer · workflow probe-then-spec · 2026-09-02

Second pass on this PRD, on the route the analyst also ran. Pass one built and
measured spec01 and spec03's two doc edits and left them uncommitted; this pass
wrote the two things it did not — spec02's `doctor` note and spec03's five
harness numbers — and re-proved the whole set on the tree as it stands now.

## Boxes

| spec | boxes | state |
|---|---|---|
| `specs/spec01.md` | 7 / 7 `[x]` | already stood; re-proved — probe A–D green, `guard status` prints the note on this repo |
| `specs/spec02.md` | 6 / 6 `[x]` | **written this pass** — two lines in `resources/doctor.sh` |
| `specs/spec03.md` | 7 / 7 `[x]` | **written this pass** — five numbers in the sibling harness |

Every spec's `## Verify and Proof` block was run the way `collect` runs it
(`bash -e -o pipefail`, cwd = repo root, all fences of the section joined):
**spec01 exit 0, spec02 exit 0, spec03 exit 0.**

```
this PRD's probe          46 checks · 46 pass · 0 fail · 0 skip   (was 45 pass · 1 fail)
guard-on-is-one-command   78 checks · 78 pass · 0 fail            (was 73 pass · 5 fail)
the-skill-tree-is-guarded 41 checks · 41 pass · 0 fail
doctor-completes-without-a-home  12 checks · 12 pass · 0 fail
the-view-row-names-a-variable    6 checks · 6 pass · 0 fail
python3 resources/index.py check  exit 0
```

## What this pass wrote

**`resources/doctor.sh`** — two lines under the guard row's `ok`, exactly the
insertion spec02 carried, on the anchor it named. The file was contended
through pass one and is committed now, so it was free. `guard ok` is unchanged,
`--fix` writes nothing, and doctor's exit code is identical wired and unwired
(both `0` on the fixture; both `1` on this repo, for `origin`).

The flip is this pass's: `git show HEAD:resources/doctor.sh | grep -c 'serve\.py
ensure'` → `0`, the working tree → `1`, and the probe's section E went
`FAIL → ok` on that change alone.

**`.pearde/prds/the-tool-keeps-its-word/guard-on-is-one-command/probe/verify.sh`**
— the five literal counts spec03 named, each check's text renamed to the number
it now asserts (lines 38, 65, 94, 104, 119; `4→5`, `3→4`, `4→5`, `3→4`, `3→4`).
Each replacement was asserted against the exact old line before it was written.
Nothing else in that file moved and its other 73 checks stayed green.

## One box was re-aimed, and why

spec03's stale-label box read
`grep -c 'three - lines\|four + lines\|three + lines' … returns 0`. Run
verbatim after the rename it returns **1** — because line 119's *correct new*
label is `C four + lines — the cap was set` (section C starts from a settings
file whose cap is already `4000`, so the cap adds no `+` line and the four
hooks are all of them), and the bare needle `four + lines` matches it. The box
is now aimed at the five stale labels by name —
`'three - lines\|three + lines\|A four + lines\|B four + lines'` → `0` — and
spec03 says so above the table. The rule it asserts, that no check still counts
three hooks, did not move.

## The live section is raced by a neighbour's reap

The probe's section I (a real `claude -p` session start) failed three times in a
row mid-run and passes in isolation — measured 5/5 standalone, hit on the first
poll every time. The cause is not the wiring: `serve.py ensure` starts the
daemon and registers the board a moment later, and `serve.py stranded()` calls
a daemon "watching no board" stranded, which is exactly what one looks like
inside that window. `resources/doctor.sh --harnesses` grew a `serve.py reap` at
the end of its sweep during this run (a sibling's uncommitted hunk, lines
809-826), and the sweep runs all 54 harnesses in parallel with
`PEARDE_HARNESSES=1` set. Section I now stands down under that variable
(`skip`, `43 checks · 43 pass · 0 fail · 1 skip`) and polls five seconds
instead of two when it does run. It is measured, not asserted, under a sweep —
the shape the route prescribes for a check a neighbour's scheduling decides.

## Harness accounting

Baseline taken before this pass's first edit, HEAD `9df1035`, `git status
--short` = 11 modified + 5 added. 24 harnesses: every one naming a footprint
path, plus the three that enumerate the board.

| harness | before | after | whose |
|---|---|---|---|
| `a-session-start-brings-the-board-up` | 45 pass · 1 fail | **46 pass · 0 fail** | mine — spec02's line closed section E |
| `guard-on-is-one-command` | 73 pass · 5 fail | **78 pass · 0 fail** | mine — spec03 |
| `the-fixtures-meet-the-tool` | 31 pass · 4 fail | 31 pass · 4 fail | red **before the first edit**, unchanged, not mine |
| `the-gate-runs-the-harnesses` | 56 pass · 1 fail | 56 pass · 1 fail | red **before the first edit**, unchanged, not mine |
| `init-seeds-a-board-doctor-calls-green` | 41 pass · 0 fail | 33 pass · 8 fail | **not mine** — see below |
| `upgrade-leaves-the-memo-index-stale` | 40 pass · 0 fail | 36 pass · 4 fail | **not mine** — same cause |
| `the-loop-is-commands` | 58 pass · 0 fail | 58 pass · 1 fail | **not mine** — HEAD moved |
| `the-round-runs-in-a-window-that-ends` | 26 pass · 0 fail | 25 pass · 1 fail | **not mine** — same commit |
| `workflow-skill` | 55 pass · 0 fail | 54 pass · 1 fail | **not mine** — a sibling grew another harness |
| the other 15 | green | green, same counts | — |

**The two doctor-on-a-copy harnesses.** `init-seeds` and `upgrade-leaves` build
their fixture with `git ls-files -z | rsync --files-from=-`, which copies
tracked paths only. A sibling session has `references/files.md` and `index.md`
modified (tracked, so copied) listing five **untracked** new files —
`references/grammar.md`, `references/parts/grammar.md`,
`references/skills/pearde-grammar.md`, `references/templates/grammar.md`,
`resources/grammar.py` — which rsync therefore does not copy. Reproduced by
hand: the same copy gives `index broken · 28 problems ·
references/files.md lists @references/grammar.md — not on disk`, so doctor
exits 1 in the copy and every "closes green" assertion goes red. Nothing in my
footprint reaches those rows.

**`the-loop-is-commands` and `the-round-runs-in-a-window-that-ends`.** HEAD
moved under this run, `9df1035 → 49f09b5` ("the-ramp-asks-before-the-board-runs"),
and that commit took `references/parts/loop.md` from 168 to 177 lines.
Both failing lines are `loop.md is 177 lines` and `loop.md is still one page`.

**`workflow-skill`.** Its one red is
`readme-in-three-rings holds its baseline … got [75 checks · 75 pass] want [74
checks · 74 pass]` — a sibling added a check to
`prds/the-board-runs-itself/readme-in-three-rings/probe/verify.sh` at 10:43,
after my baseline.

**Repo gate.** `python3 resources/index.py check` exit 0 before and after.
`bash resources/doctor.sh` exit 1 before and after, on `origin broken` both
times. Rows that moved, with `statusline` excluded as the route says:

- `guard` gained **this PRD's note** — spec02's box 6, the only row change that
  is mine.
- `index` 130 → 132 files, `grammar` 170 → 172 terms, `harnesses` 53 → 54: the
  sibling sessions' files.
- `knowledge` `ok → broken` — `graph.json is behind the files` naming six notes
  none of which this pass wrote. A sibling recorded knowledge without running
  `knowledge.py relink`. Not mine to fix; it is one command.

**Contended files.** `resources/doctor.sh` also carries a sibling's hunk added
during this run (the `serve.py reap` block at 809-826, and its
`HLEAK` line in the `harnesses` row). My two lines at 278-279 are disjoint from
it and both stand. `resources/board/serve.py` and `resources/board/collect.py`
went dirty under a sibling mid-run; neither is in my footprint and neither was
touched.

**Nothing landed outside the footprint.** `ls .pearde/prds` = 55, the same
directories as before; no fixture board reached the live daemon on 8443; the
probe's ports 8457 and 8459 are down; every fixture lived under `mktemp -d` or
the session scratchpad, and this repo's own `.claude/settings.json` was read
and never written.

## Findings

The three findings pass one recorded, carried forward by name — none is fixed,
and the first two are still true:

- **`resources/install.sh` writes no hooks.** The PRD names it as "whatever
  writes the guard hooks into a project's `.claude/settings.json`". It does
  not — it symlinks skill files. The only writer is `pearde guard on`, and that
  is where the fourth hook went. Nothing in `install.sh` changed.
- **`references/parts/doctor.md`'s row table omits `guard`** — and `plugins`,
  `vault`, `vision`, `briefs`, `knowledge`, `jstests`. Adding the note needed no
  edit there, but the table reads as if it were the whole set. Not this PRD's
  contract, and the file is held by a sibling.
- **The `guard on`/`guard off` output shape is asserted by line count in a
  closed PRD's harness.** This is the finding this pass paid for: five `eq`
  checks on `grep -c` of the `+` and `-` lines break on any fourth hook,
  forever. A shape assertion — which events, which commands — would not.
  `guard-on-is-one-command`'s other 73 checks are shape assertions and all
  held. The numbers are correct again; the design is unchanged.

Two new ones:

- **`serve.py reap` calls a starting daemon stranded.** `stranded()` returns
  `True` for a daemon "watching no board", which every daemon is between
  binding its port and its first `/register`. A sweep that reaps in that window
  kills a daemon a session start had just brought up. `reap` is right about
  leaks and wrong about the newborn; a grace period on daemon start time, or
  skipping a daemon younger than a second, closes it. The file is a sibling's
  in flight, so this is reported and not touched.
- **`doctor`'s `knowledge` row is broken on this repo** for notes this pass did
  not write. `python3 resources/knowledge.py relink` is the whole fix.

No word in the contract was missing from `resources/grammar.py show`.

## Workflow probe-then-spec

| # | step | outcome |
|---|---|---|
| 1 | `read-the-contract` | ok — PRD, three specs, pass one's report read; `git status --short` recorded before the first edit. No `## Questions`, no `## Answers`, no `## Failure` |
| 2 | `capture-the-harness-baseline` | ok — 24 harnesses + the repo gate, whole outputs kept under a subdirectory named for this run; four reds recorded "before the first edit" |
| 3 | `attempt-the-build` | **partially entered.** The route's own row for a second pass says to run 1, 2 and 4 only. Two of the three specs were unbuilt, so the build ran for those two and for nothing else — both are edits to existing footprint files (a guard branch, five literal counts), so both were built in place, not staged under `probe/` |
| 4 | `re-run-the-harnesses` | ok — same set, same order, same command lines; every drop traced to a named sibling file, both flips shown against `git show 9df1035:` |
| 5 | `write-the-specs` | **not entered** — the specs exist; this is the implementer's pass. Two edits inside them: spec03's re-aimed box, and spec02's verify block, below |

### Edits

Two edits to files this pass owns, neither to a workflow file.

**`specs/spec02.md`, `## Verify and Proof`.** The block was
`bash resources/doctor.sh` bare, which exits 1 on this repo (`origin broken`)
and so failed the whole block under `bash -e -o pipefail` on a row belonging to
another PRD. Replaced with the capture-then-grep shape the route's own
`Fails when` row prescribes:

```sh
out=$(bash resources/doctor.sh 2>&1 || true)
printf '%s\n' "$out" | grep -E '^  guard +ok'
printf '%s\n' "$out" | grep -F 'no SessionStart hook — the view is not brought up on a session start; pearde guard on writes it'
```

**`specs/spec03.md`, acceptance box 4.** Re-aimed, with the reason written into
the spec — see "One box was re-aimed" above.

Nothing in the atomics was wrong. One row is worth adding to
`attempt-the-build`'s `Fails when`, and is offered here rather than written:

| seen | means | do |
|------|-------|----|
| a spec's stale-literal box greps for a needle that its own rename re-creates | the box was written from the old set of labels, and one new label legitimately contains a needle that used to mean "stale" | run the box's command verbatim after the rename, and if it counts the corrected line, name the stale labels individually instead of by the shared substring — say in the spec why the survivor is correct |

## Scores

complexity: 15
blast-radius: mid
workflow: probe-then-spec
