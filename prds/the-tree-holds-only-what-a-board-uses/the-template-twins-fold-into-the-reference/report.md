Verdict: DONE

Second pass of `probe-then-spec` on this PRD — the analyst pass built and
specced, this pass measured, verified and repaired the spec block. All five
of `spec01`'s acceptance boxes are ticked against output quoted below. The
build stands uncommitted in the lane
`.pearde/.lanes/the-tree-holds-only-what-a-board-uses-the-template-twins-fold-into-the-reference`
at HEAD `4a94475`, the same HEAD the orchestrator's checkout is on.

## Workflow probe-then-spec

| # | step | outcome |
|---|------|---------|
| 1 | `read-the-contract` | pass — PRD, `specs/spec01.md` and the previous pass's `report.md` read; `@@templates` resolved; `git status --short` recorded in **both** roots before the first edit |
| 2 | `capture-the-harness-baseline` | pass — pre-edit tree recovered by `git clone --shared <lane> <scratch>/pre` at `4a94475`. Two atomic defects found, see `### Edits` |
| 3 | `attempt-the-build` | **not entered** — its own first `Fails when` row: this is the route's second pass, `spec01` is the only spec and its build is already in the lane. Verified against the **files**, not a diff (every folded sentence grepped in its target). No spec was left unentered with a clean footprint |
| 4 | `re-run-the-harnesses` | pass — same set, same order, same `PEARDE_ROOT`, no count dropped, no flip claimed |
| 5 | `write-the-specs` | applied its `Fails when` to the standing block; no spec authored. The block **could not exit 0** and was repaired — see *The verify block could not pass* |

### Edits

Two replacement texts for `capture-the-harness-baseline`. Neither workflow
file was edited by this pass.

**1 — the clone-the-lane row produces a false red.** The row *"the earlier
build is uncommitted in a **lane**, and that pass published no counts"* says
`git clone --shared <lane> <scratch>/pre` and run the set there. Done exactly
so, `python3 resources/grammar.py check` printed
``references/grammar.md: no `---` frontmatter fence, or one unterminated``
(exit 1) in the clone and was **silent** in the lane, on byte-identical
files. Cause: a lane lives at `<board>/.lanes/<slug>`, *under* the live
board, so board resolution walking up from it finds the real board; a clone
in scratch has no board above it and `grammar_path()` falls through to a
reference page that is not a board grammar. Symlinking the board in made the
clone silent. Append to that row's `do`:

> …and `ln -s <board> <scratch>/pre/.pearde` before the first run. A lane
> under `<board>/.lanes/` resolves the live board by walking up and a clone
> in scratch does not, so every board-reading gate answers about a board that
> is not there — measured here: `grammar.py check` reddens on
> ``references/grammar.md: no `---` frontmatter fence`` in the clone and is
> silent in the lane on identical bytes, and goes silent in the clone the
> moment the board is linked in. Link it in both trees or neither, and say
> which in the report.

**2 — the sweep has no budget, and a `for` loop over harnesses aborts.** Step
1 says to run the harness set; `bash resources/doctor.sh --harnesses <board>`
did not finish in **10 minutes** on this board (92 `verify.sh`). Separately,
the loop that runs them aborts on the first harness that exits non-zero when
the outer shell is `nu` — six of the eight ran, two never did. Add a row to
`## Fails when`:

> | the full `--harnesses` sweep does not finish inside the window, or the loop stops after the first red harness | the board has grown past a sweep-per-run (92 here, over 10 minutes), and a `for` loop in `nu` — the shell this repo runs under — takes a non-zero harness exit as the loop's own | baseline the **subset** that names a footprint path: `grep -ln "<path>" $(find <board>/prds -name verify.sh)`, plus every enumerating harness. Say in the report that the sweep was narrowed and to what — a sweep that times out is no baseline at all, and `doctor.sh` without `--harnesses` finishes and still carries every non-harness row. Run the loop as `bash -c "for …; done; exit 0"`, never from `nu` directly |

## Baseline and re-run

Pre-edit tree: `git clone --shared <lane> <scratch>/pre` at `4a94475`, live
board symlinked in. Re-run: the lane itself, `PEARDE_ROOT=<lane>`. Both HEADs
were `4a94475` at the first command and still are.

| gate | before the first edit | after |
|---|---|---|
| `ls references/templates/*.doc.md` | 7 files | no matches |
| `python3 resources/index.py check` | exit 1, 3 lines, none naming `doc.md` | exit 1, **the same 3 lines**, none naming `doc.md` |
| `python3 resources/grammar.py check` | silent, exit 0 | silent, exit 0 |
| `python3 resources/workflows.py check` | silent, exit 0 | silent, exit 0 |

Harness subset — the 8 that name `templates/` or `doc.md`
(`grep -ln 'doc\.md\|templates/' $(find .pearde/prds -name verify.sh)`), run
with `PEARDE_ROOT` at each tree. Exit codes identical before and after:
`one-verb-set` 1, `vision-is-first-class` 0, `workflow-seed` 1,
`too-big-splits-itself` 1, `one-command` 1,
`the-documented-board-matches-the-code` 1, `workflow-attach` 1. Whole outputs
`diff`ed: seven byte-identical, one added line, in `workflow-seed`:
`note tracked root files modified by other work — reported, not gated: index.md`
— a note, not a gated row, and it names this PRD's own edit. **No harness
went green-to-red and no flip is claimed.** `init-asks-nothing` timed out in
the baseline and was therefore not re-run; it is recorded as unmeasured, not
as green.

`doctor.sh --harnesses` was abandoned at 10 minutes (see `### Edits`);
`doctor.sh` without it completed and its red rows — `knowledge` (graph.json
behind the files), `questions` (3 PRDs with `## Answers` and no
`## Questions`), memo `tags:` — are all **before the first edit** and outside
this footprint.

## Acceptance — all five boxes, ticked as they closed

1. `ls references/templates/*.doc.md` → `No such file or directory`. The
   seven twins are staged deleted in the lane.
2. `python3 resources/index.py check` names no `doc.md` anchor and no
   `@@templates` `doc.md` entry. It prints 3 lines and exits 1 — see
   *Findings* for what those actually are.
3. `python3 resources/grammar.py check` — silent, exit 0.
4. `python3 resources/workflows.py check` — silent, exit 0.
5. `git grep -n 'doc\.md' -- references resources` → one hit,
   `resources/knowledge.py:897`, the `index_stem` docstring's naming
   example. Not a citation of a file on disk. (The spec's block spelled it
   `:895`; the line is 897.)

Every folded sentence was checked in its target file, not in a diff:
`One contract per PRD` and the `## Failure`-reads-as-a-failed-attempt line in
`references/drill.md`; `pearde specced` refuses a spec with no box in
`references/parts/contract.md`; the `"slower"` example and
`deliberately does NOT fix` in `references/memo.md`'s body table; both atomic
examples, `named the way a request arrives`, `this section is the lookup` and
`is a list, not a workflow` in `references/workflow.md`.
`resources/memos.py:311` now cites `@references/memo.md`.

## The verify block could not pass

`spec01`'s `## Verify and Proof` block, as written by the analyst pass, exits
**1** on a correct tree. `collect` runs it `bash -e -o pipefail`
(`resources/board/collect.py:2242`) and its first line was
`ls references/templates/*.doc.md`, which exits 1 on exactly the result that
means the spec passed — `write-the-specs`' own row *"a block exits non-zero
on the result that means it passed"*. Its second and fifth lines were bare
board-wide gates (`index.py check`, `git grep`), the shape the *"`collect`
refuses with `spec<NN> exit <n>`"* row names.

Rewritten per both rows — producer guarded, gate captured and grepped rather
than gating, and one section added asserting each folded sentence is on
record. Proven both ways:

- On the lane: `BLOCK EXIT=0`.
- On the pre-edit clone (twins present): `doc.md twins on disk: 7`,
  `BLOCK EXIT=1`.
- On a clone with the twins deleted and nothing else updated: exit 1, naming
  32 dangling `doc.md` rows in `files.md`, `index.md` and `memos.py`.
- On a clone with the twins deleted and the rows updated but the folds not
  made: exit 1. Every section of the block can fail.

## Findings

Carried forward from the analyst pass's report, unfixed and still true:

- **`pearde workflow add` does not exist.** Both `atomic.doc.md` and
  `workflow.doc.md` cited `pearde workflow add [atomic] <subject>`; `pearde
  --help` lists only `workflow list/show/brief/check/retag`. The files are
  deleted so the wrong claim went with them, but it was not checked for
  elsewhere. Outside this footprint.
- **`lanes.create` failed silently at claim time**, and `cut_lane` swallowed
  the `LaneError` and fell back to the checkout while `pearde brief` kept
  printing the lane as `repo:`. Not reproduced on retry.

New, this pass:

- **The spec's attribution of the two inherited `index.py check` rows is
  wrong, and so was the previous report's.** Both call
  `resources/common.py is on disk with no row in references/files.md` and the
  two `hotreload-test.js` rows *"pre-existing unrelated failures from a
  concurrent uncommitted pass"*. They reproduce on a **clean clone of
  `4a94475` with nothing uncommitted at all** — they are committed-state
  defects on `main`, not another session's working tree, and nobody's merge
  will clear them. They want a PRD. Left as found; the repaired verify block
  captures `index.py check` instead of gating on it, so this spec no longer
  depends on them.
- **`references/drill.md` will conflict on merge.** The checkout has
  uncommitted work inserting 61 lines at `@@ -5,0 +6,61 @@` — the same anchor
  this PRD inserts `**One contract per PRD.**` at. `index.md` and
  `references/files.md` are also written by both, but their hunks are
  disjoint (`index.md`: neighbour at 62/66/85, this PRD at 77;
  `references/files.md`: neighbour at 124/161/171/263, this PRD at 97 and
  110-116). Per `read-the-contract`, the neighbour's hunks were left in the
  checkout and not carried into the lane. **Flag `references/drill.md` before
  collecting either.**
- The checkout's dirty list moved during this run — `resources/board/init.py`,
  `transitions.py` and `graph/graph.sh` left it, `references/parts/doctor.md`,
  `parts/handles.md` and `resources/board/purge.py` joined it. Other sessions
  are live in it; neither HEAD moved.

Nothing in the footprint was under the health floor. No word was missing from
the grammar. No fact came from outside this repo, so nothing was written to
the knowledge layer.

## Scores

complexity: 8
blast-radius: low
workflow: probe-then-spec
