# the-prose-and-the-invariants-say-dot-pearde — implementer report

Verdict: DONE

Second pass on this route. The analyst's pass (2026-09-03, report below this
one in git) probed, built and specced; its build stands uncommitted in the
lane — 14 files, +128 −100 — and every spec's **Stands** held when checked
against the files. This pass ran no build of its own: it entered step 3 for no
spec, re-measured, ran every spec's `## Verify and Proof` block the way
`collect` runs it, proved each can fail, and ticked 16 of 16 boxes.

Baseline inherited and confirmed: the five board harnesses this footprint
moves were re-run in the lane and every count equals the number the analyst's
report published (colour-group 8 groups, board-file 20 PASS 0 FAIL,
every-artifact 7 PASS 0 FAIL, destructive 6 PASS 0 FAIL, one-copy 4 PASS 0
FAIL) — so the inherited baseline stands without a revert window, per the
route's cheaper confirmation. Lane HEAD was `f8968fe` at the first command and
at the last; the checkout's HEAD was `e55a0e7` at both. No head moved.

## Workflow probe-then-spec

| step | atomic | result |
|---|---|---|
| 1 | read-the-contract | prd.md read; three specs read; git status recorded in both roots before any edit — checkout held `references/drill.md` and `references/skills/pearde-drill.md` modified (a neighbour's, outside the footprint, untouched); lane held exactly the 14 footprint files |
| 2 | capture-the-harness-baseline | taken in the lane, then confirmed equal to the analyst's published counts; repo gate recorded in both roots |
| 3 | attempt-the-build | not entered — second pass; every spec's footprint is in the lane tree, checked by reading `git -C <lane> status --short` (14 files, all named in the specs' footprints) |
| 4 | re-run-the-harnesses | all five harnesses re-run in the lane, same order, no PEARDE_ROOT either time: 20/0, 7/0, 6/0, 4/0, 8 groups — equal to baseline and to the analyst's published numbers |
| 5 | write-the-specs | none authored — second pass; boxes ticked as closed |

### Edits

None — the route's workflow files are not this pass's to edit, and no atomic
failed in a way that named a wrong command, path, or check. The one mis-run
that could have become an edit did not: the first spec01 block run executed
from the checkout because the shell resets cwd between calls, and its
`cd "$(git rev-parse --show-toplevel)"` then resolved the checkout — the
expected pre-merge failure, which was re-run deliberately in the lane and in
the merged scratch tree after. No workflow edit needed.

## Per-spec verification

Run the way `collect` runs it, `bash -e -o pipefail` with the block awked out,
from the lane:

| spec | in lane | verbatim in checkout | merged tree |
|---|---|---|---|
| spec01 | rc 0 · `spec01 ok` | rc 1 · `FAIL references/parts/commits.md` | rc 0 · `spec01 ok` |
| spec02 | rc 0 · `spec02 ok` | rc 1 · `BROKEN: no board at pearde/` | rc 0 · `spec02 ok` |
| spec03 | rc 0 · `spec03 ok` | rc 1 · undotted `guard.MEMO` grep hit | rc 0 · `spec03 ok` |

The verbatim-in-checkout column is the red-to-green flip shown against the
tree that does not hold the build, quoted per the route.

Can-it-fail proof, one mutation per spec, each restored from a scratch copy
outside the repo and proved back with `cmp`:

| spec | mutation | result |
|---|---|---|
| spec01 | appended a line spelling `pearde/` as the board to `board.md` | rc 1, `FAIL board.md` |
| spec02 | appended an undotted comment to the board-file invariant | rc 1, grep names line 433 |
| spec03 | `guard.MEMO` spelled undotted | rc 1, grep names line 463 |

spec03's mutation is a computed constant, not a grep needle — it proves the
block detects a regression, not only that the counter is wired. spec01's and
spec02's are counter-wiring mutations against string greps; the report says so
rather than let the ticks imply more.

The merged tree: `git clone --no-hardlinks` of the checkout at `e55a0e7`, then
`git apply --3way` of the lane's diff — rc 0, no conflict — so the
rebase/merge `collect` runs will land clean. spec01 and spec03 pass in the
merged tree; spec02 passes there with the live board symlinked in (state
named: the merged tree has no board of its own, and the colour-group harness
needs one to read).

## Box status

All 16 boxes ticked against commands run this session:

- spec01 — 5/5: `prose.py check references/parts/board.md` printed nothing;
  the dotted-order greps, the memo name, `leaves no link behind` and
  `@references/obsidian.md's` all hit; the bare-`pearde/` grep over
  `commits.md`, `guard.md` and `board.md` is clean and fires under mutation.
- spec02 — 5/5: colour-group green from the lane and from a fresh worktree
  holding an empty `.pearde/` (the case that was red at the analyst's
  baseline); board-file 20 PASS 0 FAIL with `board=$code/.pearde`;
  every-artifact 7 PASS 0 FAIL; the all-invariants grep clean, fires under
  mutation.
- spec03 — 6/6: refusal strings name `.pearde/memos/…` (asserted in Python
  against the imported `refuse` and `guard`); `graph.sh` asks `.pearde/`
  first; `shared.py` rows ordered `['.pearde/graphify/cache',
  'pearde/graphify/cache']` with the LEGACY comment present; all modules
  parse; one-copy 4 PASS 0 FAIL, destructive 6 PASS 0 FAIL.

## The repo gate

- `python3 resources/index.py check` — lane: rc 1, three lines (common.py
  row, hotreload-test.js row, @@view), unchanged before and after, inherited.
  Checkout: rc 1, four lines — the three above plus
  `references/parts/commits.md references @pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md — not on disk`. That fourth line exists only in
  the checkout, where `commits.md` is still undotted; the lane's rewrite dots
  the reference, so the merge closes it. Inherited, closing on merge.
- `bash resources/doctor.sh` — lane: broken rows index, vault, origin,
  health, knowledge; checkout: the same five, and the checkout's index row
  carries the fourth line. The vault row's fix line still spells
  `upgrade → pearde/` — the vault sibling's row, not this footprint's. No row
  went from ok to broken in either root, and none was closed by this run's
  edits (the checkout's two dirty files are a neighbour's `drill` files).

## Findings carried forward by name (all stand, none closed by this PRD)

From the analyst's report, unchanged and still owned by their siblings:

1. Three siblings overlap on eleven files — stands; the specs stop at the
   line.
2. Two resolvers ask the legacy name first (`doctor.sh:264`,
   `statusline.sh:96`) — stands, owner `the-board-name-is-one-dotted-constant`.
3. `doctor`'s `board broken` fix line moves a board to the undotted name
   (`doctor.sh:379/381`), and the vault row's fix line runs `pearde upgrade`
   — stands, same owner plus the vault PRD.
4. The graphify cache store keyed on a path no tree holds (`shared.py
   CACHE_KEY`) — stands; this PRD reorders the rows and comments the key only.
5. `board.md` defers the vault to `@references/obsidian.md` — stands by
   design; the vault sibling settles it.
6. Pre-existing reds: index.py check's lines, doctor's five broken rows,
   `prose.py check references/parts/commits.md`'s three waste words — stand,
   not this PRD's.

New findings this pass:

7. The checkout's `commits.md` at HEAD references a memo path that does not
   exist — `@pearde/memos/a-board-s-own-file-commits-in-the-board-repo.md`,
   the undotted spelling of a memo that lives at `.pearde/memos/`. The lane's
   rewrite dots it, so this closes on the merge; it is the only gate line
   this PRD's merge closes.
8. The live serve registry holds two fixture boards from earlier probe runs —
   `a` at `/private/tmp/pearde-probe-c78NOK/a/.pearde` and `tmp.0BOFUrSzMM`
   at a deleted temp path, both under the master board `all`. Not landed by
   this run (no `--fix`-shaped command ran here); the coordinator should
   `[ -d <path> ] || serve.py forget <name>` each — test the path first.
9. Two warns from `specced --check` a later author should fix in the spec
   text: spec02's verify block spells its harness paths through `$I` and a
   loop variable, so the checker reads no footprint path in it — the block
   ran green and its mutation proof fires, but it is the checker's blind spot
   by construction. The implementer-ticked warn on all three specs is the
   expected shape, not a defect.

## Health floor

The brief names none of the 14 footprint files under the floor. Nothing moved.

## Scores

complexity: 12
blast-radius: mid
workflow: probe-then-spec
