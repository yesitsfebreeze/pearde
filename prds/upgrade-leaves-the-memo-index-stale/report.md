# upgrade-leaves-the-memo-index-stale — analyst report

Verdict: SPECCED — one spec, `specs/spec01.md`, complexity `9`, blast-radius
`low`, workflow `probe-then-spec`. The build went through end to end: the fix
stands in `resources/board/init.py` and a 40-check harness at
`.pearde/prds/upgrade-leaves-the-memo-index-stale/probe/verify.sh` reads
`40 checks · 40 pass · 0 fail · 0 skip` on a quiet machine and
`39 pass · 0 fail · 1 skip` while a sibling session was writing the
Obsidian vault list — both readings taken, the skip is section H's
stand-down and is never counted a pass. Nothing was left undefined and
no fork was hit.

## What was built

The change is an **edit to an existing footprint file**, so it was built in
place rather than staged under `probe/` — a call site has no meaning outside
the function it lives in. Three hunks, all in `resources/board/init.py`:

- `:349` — `index_memos(board)` became `index_memos(board, verb="init")`, and
  its failure line's hard-coded `init:` prefix became `{verb}:`. `cmd_init`'s
  call at `:582` is untouched; the parameter defaults.
- `:753-770` in `cmd_upgrade` — between the `wiki` row and `write_obsidian`,
  and so before the `plant_graph` loop, which is the ordering `plant_graph`'s
  own docstring fixes (`knowledge.py board` reads the memos this step
  indexes). It reads `memos/README.md`'s bytes, calls
  `index_memos(board, "upgrade")`, reads them again, and prints one aligned row
  in `upgrade`'s existing format — `regenerated …`, `already current …`, or
  `no memo on this board — nothing to index`. Reading the bytes rather than
  asking `index_memos` is what lets the row say which of the two happened, the
  way `wiki` and `register` already do, and it gives the harness a predicate
  that can fail in both directions.

`index_memos` has exactly two callers, both in this file. Nothing else in
`resources/`, `references/` or `index.md` names it.

## The red, reproduced before the first edit

The old shape is built rather than described: the example board copied through
`shutil.ignore_patterns("README.md")`, which is literally what `init --example`
did before the index step existed. On that fixture, before the fix:

```
--- memo check BEFORE upgrade ---   README.md: the kind index is stale — run `memo index`   rc=1
--- upgrade ---                     (wiki, vault, gitignore, register, board, relink — no memos row)
--- memo check AFTER upgrade ---    README.md: the kind index is stale — run `memo index`   rc=1
--- README present? ---             no
--- doctor memos row ---            memos  broken  1 memos · 1 problem
```

After the fix, same fixture, under a HOME holding no Obsidian config:
`memos     regenerated memos/README.md, the index by kind`, `memo check` rc 0
and silent, the page byte-identical to the example board's own, and doctor
closes on `pearde: every part this repo owns checks out.`

## The harness

`probe/verify.sh`, sections A–H, 40 checks. Its shape follows the precedent in
`seven-closed-probes-drifted-red/init-seeds-a-board-doctor-calls-green` — a
repo copy from `git ls-files` read out of the *working* tree, so the
uncommitted footprint edit is what is measured; one `mktemp -d` removed at
exit; every board command under `env -u XDG_CONFIG_HOME HOME=<empty>`.

- **A** sees the fixture red before anything repairs it — `memos/one-author-is-not-an-accepted-spec.md`,
  every box below ticked against a predicate seen failing.
- **C** is the contract driven rather than read: doctor's report compared row
  by row between the upgraded board and a freshly `init --example`ed one.
- **F** strips `index_memos(board, "upgrade")` back out of the *copy* of
  `init.py` and watches `memo check` go red and doctor's `memos` row go
  `broken` again, then restores and proves it with `cmp`. Without F every box
  in B and C is a check that could not fail.
- **G** mutates the copy's `memos.py index` to fail and asserts the line reads
  `upgrade: could not regenerate memos/README.md` — the verb parameter's whole
  reason to exist.
- **H** asserts no fixture of the run reached this machine's Obsidian vault
  list, and that the live daemon's registry is byte-identical.

## Baseline, and two inherited reds that closed under me

Taken before the first edit, at `HEAD f3aea95`:

| harness | before | after |
|---|---|---|
| `guard-on-is-one-command` | 78/78 pass | 78/78 pass |
| `init-seeds-a-board-doctor-calls-green` | 41/41 pass | 41/41 pass |
| `readme-in-three-rings` | 74/74 pass | 74/74 pass |
| `the-next-line-runs` | 96/96 pass | 96/96 pass |
| `init-asks-nothing` | **88 checks · 87 pass · 1 fail** (exit 1) | 88/88 pass |
| `index.py check` | silent, exit 0 | silent, exit 0 |
| `doctor.sh` | **exit 1** | exit 0, green |

Both reds were there **before the first edit** and both were closed by sibling
sessions during the run, not by me:

- `init-asks-nothing` failed on `FAIL J the copy's registry never learned a
  fixture`. That label no longer exists anywhere in that harness — its file's
  mtime is `00:01` today. A sibling rewrote section J; the flip is theirs.
- `doctor` read `briefs broken` on
  `NameError: name 'VERDICT_MARK' is not defined` at
  `resources/board/brief.py:194`. `brief.py` is now modified in the working
  tree and the row reads ok. Also a sibling's.

Working tree at the end: `references/parts/workers.md`, `resources/board/brief.py`,
`resources/board/collect.py`, `resources/board/init.py`, `resources/doctor.sh`
modified. Only `init.py` is mine.

## Findings — none of these belong in a spec

### The `vision` row is a second divergence of exactly this shape

Section C's first draft failed: **one** doctor row still differs between an
upgraded board and a fresh one.

```
vision off      no vision.md — the board orders by dependency, weight and priority alone
vision ok       vision declared · no terminals — no axis
```

`write_board` copies `VISION_TEMPLATE` to `vision.md` when it is missing;
`cmd_init` calls `write_board`, `cmd_upgrade` never does. So `upgrade` seeds
the wiki content, the vault, the gitignore, the graph and now the memo index —
and no `vision.md`. Doctor calls the result `off`, not `broken`, so both boards
are green and the user's contract ("exactly as healthy") holds on health; they
are not *identical*. The harness excludes the row by name, with the reason
written beside it, so the check stays true both before and after that gap
closes and never locks it in. **This is its own contract — widening spec01 to
cover it would have been initiative, not the PRD.** Suggested shape: `upgrade
seeds vision.md the way init does`, footprint `resources/board/init.py`.

### The harness set writes this machine's real Obsidian vault list

The first reproduction — run before I isolated `HOME` — printed
`register  added` and put a temp path into
`~/Library/Application Support/obsidian/obsidian.json`. Looking at that file:

```
total vaults: 700 · temp-dir fixtures: 674 · paths gone: 660
```

New entries were landing **while I read it** — eight in the last 49 seconds,
from paths shaped `…/T/tmp.*/{a,c,e,f,g,h,i}/.pearde`, which is another
session's fixture set. `register_vault` (`init.py:211`) has no fixture guard;
it writes whatever board it is handed, and any harness that runs `init` or
`upgrade` against a `mktemp -d` board without an isolated `HOME` grows this
file by one entry per fixture per run. 660 of the 700 entries point at
directories that no longer exist. This is board-wide across the harness set,
not this PRD's footprint, and it is the reason section H reports `skip` rather
than asserting the file unchanged — a whole-file assertion here is a check
decided by scheduling (`memos/a-check-decided-by-scheduling.md`). The race-free
half — no path of *this* run in that file — is asserted and passes. My
committed harness adds nothing to it; the one entry my throwaway reproduction
added is in there among the 674.

### `knowledge.py board` counts the generated index page as a memo

`upgrade` prints `board: 8 PRD note(s), 2 memos scanned` on a board doctor
calls `1 memos`. The extra one is `memos/README.md`, the generated index. A
fresh `init --example` prints the same `2 memos scanned`, so this is
**pre-existing on both paths and not introduced here** — it moved from 1 to 2
on the upgrade path only because the index now exists there too. Cosmetic:
`knowledge doctor` reports `graph in sync` and doctor's `knowledge` row reads
ok either way. Outside this footprint — it is `resources/knowledge.py`'s memo
scan.

### `.pearde/` is gitignored whole, so no board file ever shows in `git status`

`.gitignore:16` ignores `.pearde/`. Neither this probe nor these specs nor any
other PRD's harness is tracked. Two consequences worth knowing: the brief's
"leave the probe code in the tree, uncommitted" is automatic on this board and
cannot be otherwise; and `attempt-the-build`'s done-when "`git status --short`
shows the probe under the PRD folder" cannot hold here — the untracked-list
check it prescribes answers nothing on this repo. The rest of that atomic held.

### `ignore_patterns("README.md")` — noted, not re-filed

`init.py:155` is still directory-blind and the harness *depends* on it to build
the old shape. Its consequence is closed by `index_memos` on both paths now.
The orchestrator's brief says this is already on record; nothing new here.

## Workflow

`probe-then-spec` fit without amendment and every step ran in order:
`read-the-contract` → `capture-the-harness-baseline` → `attempt-the-build` →
`re-run-the-harnesses` → `write-the-specs`. `capture-the-harness-baseline`'s
"a harness already failing is recorded as failing before your first edit" is
what made the two sibling flips above legible instead of alarming, and
`attempt-the-build`'s row on a mutation restore proved with `cmp` is exactly
what sections F and G do. No new workflow, no new atomic.

One recurrence worth noting rather than filing: **three** of this board's
harnesses now open by copying the repo from `git ls-files` into a `mktemp -d`
and running every board command under an empty `HOME`. That preamble is
becoming an atomic in its own right — `isolate-the-fixture-from-the-machine` —
but it is a job that already has a home inside `attempt-the-build` steps 2–3,
so this is a finding, not a second file.

## Knowledge

`knowledge.py query` on the contract returned `11 hit(s), 6 strong · 11 notes
on record` and enqueued no gap into `.pearde/wiki/pending/`. Every fact this
run used came from this tree, so nothing was written back with `remember`.

## Scores

complexity: 9
blast-radius: low
workflow: probe-then-spec
