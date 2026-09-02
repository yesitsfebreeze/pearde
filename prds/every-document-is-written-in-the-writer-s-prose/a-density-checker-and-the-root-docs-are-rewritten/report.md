Verdict: DONE

# a density checker and the root docs are rewritten — implementer report

Second pass of `probe-then-spec` on this PRD. The analyst's pass built and
specced; this pass measured, verified and ticked. Steps 3 and 5 were not
entered as build-and-spec work — the row in step 3's `Fails when` that names
the route's second pass. No code was written this run; every red-to-green on
this tree was earned by the analyst's pass.

## Boxes

16 of 16 ticked, none inherited. Every block was run the way `collect` runs
it, under `bash -e -o pipefail`, from the lane root.

| spec | boxes | block exit | mutated exit | restored |
|---|---|---|---|---|
| spec01 the checker and the rules | 4/4 | `0` — `spec01: 8 assertions` | `1` | `cmp` ok |
| spec02 `references/files.md` | 3/3 | `0` — `spec02: rows before 152 after 153` | `1` | `cmp` ok |
| spec03 `index.md` | 3/3 | `0` — `spec03: keywords before 37 after 37` | `1` | `cmp` ok |
| spec04 `README.md` | 3/3 | `0` — `spec04: glossary rows before 24 after 24` | `1` | `cmp` ok |
| spec05 `SKILL.md` | 3/3 | `0` — `spec05: 3 assertions` | `1` | `cmp` ok |

spec01's mutation is behavioural, not a string match: `MEAN_SENTENCE_MAX` was
moved from `24` to `3` in `resources/prose.py` — the constant the tool
computes against — and the block went to exit `1`. spec02 to spec05 were
mutated by appending one unbound-pronoun sentence to the footprint file, the
same class of regression the box claims. Every file was backed up to a scratch
directory outside the repo, restored by `cp`, and the restore proved with
`cmp`.

Quoted output behind the boxes: `check` on a clean fixture `rc=0`; on a
planted preamble `rc=1` printing `banned opener — "this document"`; `stat`
printing `total: 77550`; the `## Density` table carrying 9 rules plus its
header (`Lead with the answer`, `Cut twice`, `No unbound`, `Emphasis earns its
place` all present); `check` `rc=0` on all four rewritten root docs;
`| @resources/prose.py |` at `references/files.md:133`; `@resources/prose.py`
in `index.md`'s `@@language` row at line 76.

## Harnesses

A real pre-build baseline was taken, not inherited. The six footprint files
were copied to scratch, reverted with `git checkout --` (and `prose.py`
removed), the set run, then restored and proved byte-identical with `cmp`.
The lane holds no neighbour's hunks, so the revert cost nothing.

18 harnesses — every one whose text names a footprint path, plus the four that
enumerate the board — run twice with `PEARDE_ROOT=<lane>`, same order, same
command line. **Every count is identical before and after.** Nothing in this
build moved a harness.

| harness | before | after |
|---|---|---|
| a-harness-measures-the-tree-its-worker-built-in | 18 pass, 0 fail | same |
| list-the-collects-the-repo-bug-orphaned | 10 pass · 1 fail | same |
| files-score-their-health-and-the-brief-names-the-unhealthy | 37 pass · 0 fail | same |
| graph-probe-makes-harness-sweep-unaffordable | 3 pass · 1 fail | same |
| nothing-left-open/the-line-tells-the-truth | 85 pass · 0 fail | same |
| nothing-left-open/the-skill-tree-is-guarded | 40 pass · 1 fail | same |
| one-definition-of-the-board-not-two | fail=7 | same |
| init-seeds-a-board-doctor-calls-green | 31 pass · 10 fail | same |
| the-fixtures-meet-the-tool | 30 pass · 5 fail | same |
| the-board-runs-itself/an-example-board | 37 pass · 0 fail | same |
| the-board-runs-itself/init-asks-nothing | 89 pass · 0 fail | same |
| the-board-runs-itself/readme-in-three-rings | 72 pass · 1 fail | same |
| the-board-runs-itself/the-loop-is-commands | 60 pass · 0 fail | same |
| the-gate-runs-the-harnesses | 54 pass · 3 fail | same |
| the-round-runs-in-a-window-that-ends | 26 pass · 0 fail | same |
| upgrade-leaves-the-memo-index-stale | 35 pass · 5 fail | same |
| workflows-on-the-board/workflow-seed | 67 pass · 5 fail | same |
| workflows-on-the-board/workflow-skill | 49 pass · 6 fail | same |

Every failing line above was recorded failing **before the first edit** of the
analyst's pass was on the tree. None is this PRD's.

Only four harness outputs differ textually between the two runs, and none of
the differences is a count: two are timings and a temp-dir name, one is
another session's PRD landing mid-run (`prd.md` files on disk `119` to `120`),
and one is the `index.py check` line count discussed below.

## The one line this build adds to the repo gate

`python3 resources/index.py check` in the lane goes from **2 lines to 3**. The
added line is

```
references/language.md references @references/personas/writer.md — not on disk
```

It names a footprint file, so it is this build's. It closes on the merge, and
is not repairable in the lane:

- `references/personas/writer.md` is on disk in the orchestrator's checkout
  (staged `A`, 5766 bytes) and absent from the lane — the lane was cut off
  `HEAD`, which does not carry it (`harnesses-copy-tracked-files-only`).
- Proved directly: copying the checkout's `writer.md` into the lane, running
  `index.py check`, and removing it again drops that line.
- With `writer.md` present the checkout **already carries its manifest row** —
  `| @references/personas/writer.md | Vera Lindqvist — technical writer, the
  density rules |` at `references/files.md:94`. Adding that row in the lane
  would duplicate a hunk the checkout already holds, which the route forbids.

`references/files.md` is modified in **both** roots. The hunks are disjoint —
the checkout's single hunk is at line 94, the lane's are at 3, 7, 10, 133, 194
and 203 — so the merge is clean, but the orchestrator should expect to merge
rather than replace this file.

`readme-in-three-rings` and `the-gate-runs-the-harnesses` each carry one
`index.py check is silent — got '3', want '0'` line; both were already red on
`got '2'` before the build. The rule did not move and the count did not move.

## Repo gate, both roots

| gate | lane before | lane after | checkout |
|---|---|---|---|
| `index.py check` | rc 1, 2 lines | rc 1, 3 lines | rc 1, 2 lines |
| `doctor.sh` | rc 1 | rc 1, identical rows | not this PRD's |

`doctor.sh` in the lane reports `board broken`, `view broken`, `knowledge
broken` and most rows `off` — the lane worktree carries no `.pearde/` of its
own. Unchanged by this build, and the same lane-wide quirk the analyst
recorded.

## Findings

Carried forward from the analyst's pass, all still open:

- **`references/language.md` is in no PRD's rewrite footprint.** The sibling
  `the-loose-reference-files-are-rewritten-dense` excludes it and
  `references/files.md` by name, and this PRD's contract asks only that it
  *carries* the `## Density` section. Confirmed this pass: `prose.py check
  references/language.md` exits `1` on its own pre-existing body while all four
  contracted root docs exit `0`. A gap for the orchestrator to route.
- **Pre-existing, outside this footprint:** `references/skills/pearde-machine.md`
  has no row in `references/files.md`; `resources/board/edit.py` references
  `@questions.py`, not on disk. Both were in the lane's `index.py check` before
  the first edit. The checkout has since renamed `references/parts/machine.md`
  to `run.md` and deleted `references/skills/pearde-machine.md`, so the first
  line is a live sibling's to close, not this PRD's.
- **The lane's `doctor.sh` is structurally red** — no `.pearde/` in the
  worktree. Matches the parent's report; a lane-wide quirk.
- **The whole-tree 30% word cut is the parent PRD's item, not this child's.**
  This tree's total is `77,550` words, up 80 from `77,470`: the `## Density`
  section's own words outweigh the words cut from four files. Expected and
  correct at this PRD's scope; the cut lands when the siblings do.

New this pass:

- **`resources/prose.py` is untracked.** It will not reach a harness fixture
  built from `git ls-files` until the orchestrator stages it — the
  `harnesses-copy-tracked-files-only` shape on record.

## Workflow probe-then-spec

| step | atomic | outcome |
|---|---|---|
| 1 | read-the-contract | pass — `prd.md`, 5 specs and the analyst's `report.md` read; `git status --short` recorded in both roots before the first command; every footprint path located, `references/personas/writer.md` named as the one dangling `@` |
| 2 | capture-the-harness-baseline | pass — 18 harnesses plus both repo gates, `PEARDE_ROOT=<lane>`, taken on a genuinely reverted tree, whole outputs saved under a per-run scratch subdirectory |
| 3 | attempt-the-build | **not entered** — second pass; the specs and the build already stand. The `Fails when` row naming the route's second pass |
| 4 | re-run-the-harnesses | pass — same set, same order, same `PEARDE_ROOT`; every count equal; the one moved gate line traced to its cause and proved to close on the merge |
| 5 | write-the-specs | **not entered as spec-writing** — its `Fails when` table applied to the blocks that already stand: every block run under `-e -o pipefail`, every one proved to fail on a mutated footprint file, no box asserts a literal probe total, no block's exit is decided outside its own footprint |

### Edits

None. No atomic named a wrong command, a stale path, a check that cannot fail,
or a shape its `Fails when` table does not list. Two rows earned their place on
this run and are recorded as working as written: step 3's second-pass row, and
step 4's row on a repo-wide gate red in the lane and absent in the checkout.

## Scores

complexity: 35
blast-radius: low
workflow: probe-then-spec
