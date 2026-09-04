# pass — 7 PRDs landed, the collect wall has a name, and one fork goes to the user

Written 2026-09-04 03:30 by pearde-pass, scope
`a-lane-goes-when-its-prd-fails-not-only-when-it-collects`.
`main` = `session/s85810` = **`776a105`**, tree clean.
`done 137/188 · 72%` (was 130 · 69%). `collect 19` (was 22). `blocked 17` (was 21).

## Landed — 7 PRDs, all on `main`

| prd | commit | what unstuck it |
|---|---|---|
| every-question-answered-and-the-prd-stays-in-question | `a6ff010` | rebase by hand, 2 marker commits skipped, stale spec path |
| one-prd-reading-primitive | `fe75b91` | rebase (guard.py import block) |
| enforce-pointer-not-verdict | `676ce01` | rebase (pearde-health.md frontmatter) |
| cmd-vault-calls-a-function-that-was-deleted | `b0022b9` | specced + implemented this pass; two verify-block defects fixed |
| one-verb-set | `7f760c2` | rebase (both sides added `cmd_reading`) |
| a-collect-closes-the-claim-dir-it-measured-against | `b63e442` | specced + implemented this pass |
| doctor-walks-machine-local-lanes | `776a105` | specced + implemented this pass |

The old standing `asking 1` is gone with the first of these. The `asking 1` on
the board now is the **new** fork below.

## THE WALL — `index.py check` is red on main and 12 of the 19 collects assert it

`python3 resources/index.py check` exits 1 on `main`. 17 problem rows. It sits
in the `## Verify and Proof` block of **136 spec files**, so its red exit fails
the whole block and a PRD whose own work is perfect collects as `spec01 exit 1`.

Measured over the 19 still in *collect* — how many of each one's specs run it:

```
3 …/the-vault-roots-…   2 …/tags-are-derived-…   2 …/the-skills-fold-into-one-index
1 …/the-template-twins-…   1 …/the-obsidian-vault-is-opt-in   1 …/scout-s-research-…
1 …/the-core-board-modules-delegate-to-common   1 the-capability-registry
1 pending-gets-an-expiry-not-a-decree   1 …/collect-runs-the-invariants-and-red-refuses
1 …/a-lane-rebases-before-collect   1 a-harness-never-dispatches-the-live-board
0 …/legacy-migrations-retire  0 …/a-lane-is-removed-…  0 one-section-registry
0 one-graph-writer  0 one-board-path-resolver-fewer  0 …/a-lane-goes-when-its-prd-fails-…
```

Two were **proven** blocked by it with clean rebases and green code today:
`pending-gets-an-expiry-not-a-decree` and `…/the-template-twins-…`.

Filed as **`the-file-index-is-green-so-a-spec-can-assert-it`** (derived, p85,
`open`, the board's only ready PRD). Four causes, one mechanical: three missing
`files.md` rows; **18 `@docs/…` rows for a tree on disk that git does not
track**; rows for `purge.py` and `hotreload-test.js`, planned and never built;
and a probe fixture row `zzdead` committed into `capabilities.md:58`.

**Its Q1 is the ASK.** `knowledge query` was run first per step 7 — 161 hits,
none answering it, gap enqueued. Only a person decides whether `docs/` is
committed or ignored. **Do not dispatch that PRD until the answer is in** — it
is the asker, so the drill gate holds it and nothing else.

## Two claimed PRDs whose worker is finished and whose collect refuses

**Named here on purpose: `sweep` leaves a claim the pass file names.** Neither
has a live worker; both have DONE reports and green probes. Do not re-dispatch,
do not let them be swept — finish the collect.

**`a-lane-goes-when-its-prd-fails-not-only-when-it-collects`** (the scope) —
`impl-lane-fails`, lane rebased onto `776a105`, probe
`13 checks · 13 pass · 0 fail` **run by hand from the lane**. Its five PRD-level
boxes were unticked (the worker ticks spec boxes, not PRD boxes); ticked on that
evidence and committed to the board as `e69565e`.
Its collect still dies **`spec01 exit 127`, `bash: line 3: PASS:: command not
found`** — the pasted probe output under the sh block was being executed as a
second block. I tagged that fence ```` ```text ````, verified with
`specs.fenced()` that the section now yields exactly **one** block, committed it
to the board — **and collect still runs the old text.** So collect is reading
the spec from somewhere other than the board working copy or the `pearde`
branch tip. **That is the thing to find next: which copy of a spec does a
collect actually execute?** It explains stale-spec failures across the queue.

**`a-lane-is-declared-at-spec-time-and-only-a-writer-gets-one`** —
`impl-lane-declared`, DONE, 7/7. Collect refuses on its own probe:
`AssertionError: lane: read cut a worktree` — a `read`-role claim cut a worktree
where only a writer should. A real finding, not a merge problem.

## Four defects in *newly written* specs — check every new one for these

1. **`prds/…` instead of `.pearde/prds/…`.** Analysts are still writing the
   pre-dotted path. Hit `every-question-answered-…`, `cmd-vault-…` and
   `a-collect-closes-…` — the last two written **this pass**.
2. **A `grep` asserting absence.** `cmd-vault-…`'s spec opened with
   `grep -n "…" resources/board/init.py   # expect no output`. No match is
   exit 1, which kills the block. Rewritten `! grep -n …`.
3. **A literal placeholder.** `pending-gets-an-expiry-…` spec01 line 102 read
   `PEARDE_ROOT=<repo-root> bash …`. Now `PEARDE_ROOT="$PWD"`.
4. **Pasted probe output in an untagged fence** — see the scope PRD above.
   Tag it ```` ```text ````.

## Two board-level fixes, both the orchestrator's

- `.pearde/workflows/probe-then-spec.md` `runs: 77 → 81`. A red `workflow
  check` **refuses any `specced` carrying a new `## Route`** — that is what
  blocked `cmd-vault-…`. This is the step-6 `runs +1` bookkeeping four passes
  skipped. **Do not skip it again.**
- `the-file-index-…`'s fork rewritten to pass `questions.py check`: under 60
  words, no backticks, no filenames, three numbered answers with
  `(recommended)` first. `questions check` is now **clean**, one of doctor's
  seven broken rows closed. `.pearde/.state/ask.md` carries the same words.

## Three traps that cost this pass real time

1. **A resolver can report success over a broken tree.** Always check the
   *commit*: `git show HEAD:<f> | grep -c '^<<<<<<<\|^|||||||'`. Every resolver
   dispatched after 03:30 is told to verify this itself.
2. **`session/s85810` moves under a running resolver.** One rebased onto a
   commit whose own collect then failed and unmerged, giving the lane a phantom
   parent. Fix: `git rebase --onto session/s85810 <phantom>`. **Do not run
   resolvers and collects of the same cluster at once.**
3. **After a collect, `main` holds the collect's own merge output** and
   `session land` refuses the fast-forward. Routine: `git status
   --untracked-files=no` → `git stash push -m "<what>" -- <paths>` →
   `session land`. Never `git checkout --`; the safety net refuses it.

## Resolved lanes that still will not collect

- **`one-section-registry`** — rebase clean, no markers, and its probe run by
  hand in the lane prints **`10/10 passed, 0 skipped`**. Collect still dies
  `cp: …/render_stub.py: No such file or directory`. Same shape as the scope
  PRD: green by hand, red under collect. **The same investigation covers both.**
- **`…/the-vault-roots-at-the-project-and-obsidian-is-taught-to-ind`** — rebase
  clean, but **spec01 is stale against upstream**: it is written entirely around
  the AGPL `unhide` plugin (20 references, pins, `data.json` shape, acceptance
  boxes) and upstream replaced it with MIT `hidden-folders-access`. Not a sed —
  the spec needs rewriting. `pearde release <prd> failed` with a `## Failure`
  naming the plugin swap, then re-spec.
- **`…/legacy-migrations-retire`** — rebase clean (`95b92da`), spec01 and
  spec02 exit 0, **spec03 exit 1** on the same plugin swap: the shared store
  still holds `unhide` bundles while the checkout holds `hidden-folders-access`.
  Its resolver also flags that
  `resources/invariants/the-guard-and-the-planner-name-the-same-board.sh` is
  guaranteed-red once this lands — it asserts a legacy/dotted *pair* this PRD
  retires. Retire or reduce that invariant with it.

## Open findings workers reported, none acted on

- **`git add -A` exits 1 inside a freshly created lane** — `link_board` plants
  the board symlink at a sparse-excluded path, so git refuses "paths outside
  your sparse-checkout definition: .pearde". It stages correctly; only the exit
  code is wrong, which is enough to abort any probe asserting rc 0. Proven
  against the pre-`link_board` commit, which exits 0. Owner: whoever owns
  `link_board`. Note: `git add -A` in an *existing* lane exits 0 here, so it is
  the fresh-create path.
- `doctor` live: **`lanes broken 6 of 45 lane(s) cannot find the board`** — the
  new row from `doctor-walks-machine-local-lanes`, working as intended.
- `lanes.create`'s early-return path still never calls `link_board`.
- `references/parts/doctor.md` does not name the new `lanes` row, so
  `the-documented-board-matches-the-code` now lists 8 missing rows, not 7. The
  exact row to append is in `doctor-walks-…`'s report.
- `unhide_board` refuses every `pearde vault` with no `--dir` — `BOARD_DIR` is
  now dotted. In `cmd-vault-…`'s report under `## Finding`.

## Still owed

1. **Answer Q1**, then land `the-file-index-…`. That unblocks 12 collects.
2. Find which copy of a spec a collect executes — it blocks 2 finished PRDs.
3. The two `unhide`-stale specs: `…/the-vault-roots-…`, `…/legacy-migrations-retire`.
4. The 11 `failed` PRDs in *waiting on you*, 8 with partial code on `lane/<prd>`.
5. `resources/board-name.sh` untracked — one of the three missing `files.md` rows.
6. Real probe failures, unfinished work not tooling: `one-graph-writer` (spec01),
   `one-board-path-resolver-fewer` (spec02).

## Knowledge (step 7)

`knowledge round` 02:53: every tool current — scout 0d, graph 0d, vault 0d.
The fork was queried against the record before it was written. Nothing owed.

## Budget

`transitions-per-pass` = 8, **11 returns collected** — 7 `done` and 4 `specced`,
each re-claimed and dispatched to an implementer in the same turn. The pass held
past its count rather than dropping workers, and every one of the 13 dispatched
came back alive. **Nothing is in flight. The board's one ready PRD is the asker.**
