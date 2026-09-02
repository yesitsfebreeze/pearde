# a verify block that pipes a probe exits zero on a broken tree under pipefail

Verdict: DONE

Three specs, 19 acceptance boxes, all ticked against output quoted below.
spec01 and spec02 stood in the lane from pass one and were re-measured, not
re-claimed. spec03 was built this pass: `specs.probe_verdict`, the formatter
warning, and both wired into `specced`.

Every one of the 14 baselined harnesses prints the count it printed before the
first edit — the diff of the two runs is empty. `index.py check` in the lane is
byte-identical to its pre-edit baseline. One doctor row moved and it is a
sibling's, named under `## Findings`.

## Per-spec box status

| spec | boxes | how it was closed |
|---|---|---|
| spec01 | 5/5 | its `## Verify and Proof` block, exit 0, `0 problem(s)` · `24 passed, 0 failed` · `spec01 green` |
| spec02 | 6/6 | its block, exit 0, `checked 10 shapes` · `0 problem(s)` · `spec02 green` |
| spec03 | 8/8 | its block, exit 0, `34 probe(s) swept · 1 with no verdict` · `0 problem(s)` · `spec03 green`; boxes 6 and 7 also proved directly, quoted below |

Run the way `collect` runs them — `bash -e -o pipefail -c "$(awk …)"` — from a
merged tree, not by hand. See `### Where the blocks were run`.

## What was built this pass — spec03

Three additions to `resources/board/specs.py`, nothing else touched:

- `probe_verdict(prd_dir)` — reads `<prd_dir>/probe/verify.sh`, takes its last
  logical statement through `_seg_can_fail`, and returns one refusal line with
  that statement quoted when it can only exit 0. No `probe/` at all returns an
  empty list. Helper scripts beside the harness (`fixture.sh`,
  `build_fixture.sh` and the 26 others) are not probes and carry no verdict, so
  only `verify.sh` is read — stated in the docstring.
- `_drains_the_verdict(block)` plus `FORMATTERS` — a **warning**, per the spec:
  it fires only when the block's *last* logical statement is one bare pipeline
  (`|` only, no `;`, `&&`, `||`, `&`) whose final member's command word is a
  pure formatter and holds no `exit`. `| head -N` earns an extra clause about
  truncation and the SIGPIPE race.
- Wiring: `read_specs` appends `probe_verdict(prd["dir"])` to the refusals;
  `check_spec` appends the drain warning, but only for a block
  `_cannot_fail_why` did not already refuse — one message per defect.

### Boxes 6 and 7, proved directly

`_cannot_fail_why` accepts all three of these — the warning is the only thing
that separates them:

```
bare pipeline into a formatter:   refuse=None  warn="its last statement ends `| tail -1` — a formatter returns 0 on any text it is handed, so the pipeline's exit says nothing about what the text said"
pipes for display, then asserts:  refuse=None  warn=None
awk that judges:                  refuse=None  warn=None
```

### End to end, on a fixture board under `mktemp -d`

```
--- dead probe:
warn: spec01.md:13: verify block 1 drains its own verdict — its last statement ends `| tail -1` — …
pearde specced: refused — fx/probe/verify.sh: its last statement `echo "$PASS passed, $FAIL failed"` can only exit 0 — the probe prints its verdict and never returns it, so every verify block running this probe is green on a broken tree. End it on the verdict itself: `[ "$FAIL" = 0 ]` or `exit $((FAIL > 0))`
--- probe given a verdict:
warn: spec01.md:13: verify block 1 drains its own verdict — …
fx: ok · complexity 3 · footprint resources/board/specs.py
```

The refusal fires, the warning fires and does not refuse, and repairing the
probe clears the refusal while the warning stands. The fixture board was made
and removed under `mktemp -d`; `serve.py status` after the run lists the same
four real boards and no temp path.

### The migration behind it, measured

- `probe_verdict` over all **139 PRDs** on the board refuses **1**:
  `a-verify-block-must-not-destroy-the-checkout-it-runs-in`. That PRD is
  `done`, so no PRD on the board can be blocked by this rule today.
- The rule read over all **71** `probe/verify.sh` on the board (not the 34
  top-level ones spec03's own block sweeps) fires on the same single file.
- The drain warning over all **279** standing verify blocks warns on **30** —
  the shape spec03 anticipated at 27 and the reason it is a warning. None of
  the 30 is refused.

### One cleanup, inside spec02's scope

`_segments` carried `or line[i:i + 1] == "&" and False` from pass one — a
clause dead by construction (`X or (Y and False)` is `X`) beside a second guard
whose `and not line[i + 1:i + 2].isspace()` could not be reached after
`== ">"`. Both collapsed into one condition. Every block re-run green
afterwards and the harness set re-run identical; this is the only change in
the file that is not spec03's.

## Harness baseline and re-run

Baseline taken **before the first edit** against a `git clone --shared` of the
lane at its own HEAD `7d65ef2` — a real pre-edit tree, not an inherited number.
`resources/board/collect.py` and `resources/board/specs.py` are byte-identical
at `7d65ef2` and at the checkout's HEAD `58c92e6`, so that clone is a valid
baseline for the merge target too. Every harness run
`PEARDE_ROOT=<root> bash <harness> </dev/null`, same command line both times.

| harness | baseline (pre-edit) | after the build |
|---|---|---|
| an-acceptance-box-that-cannot-fail-is-refused | `verify: 1 passed, 1 failed` (red) | `verify: 1 passed, 1 failed` |
| the-brief-names-the-verdict-line-collect-requires | `13 ok · 2 FAIL` (red) | `13 ok · 2 FAIL` |
| a-verify-block-must-not-destroy-the-checkout-it-runs-in | `24 passed, 0 failed` | `24 passed, 0 failed` |
| collect-must-not-reset-the-checkout-it-did-not-write | `31 checks · 31 pass · 0 fail` | `31 checks · 31 pass · 0 fail` |
| the-tool-keeps-its-word/collect-keeps-its-word | `101 checks · 101 pass · 0 fail` | `101 checks · 101 pass · 0 fail` |
| an-analyst-workflow-does-not-survive-into-specced | `verify: 21/21 checks pass` | `verify: 21/21 checks pass` |
| the-verify-guard-parses-git-s-own-output-before-it-trusts-it | `46 passed, 0 failed` | `46 passed, 0 failed` |
| filing-refuses-a-file-it-does-not-hold | `52 checks · 52 pass · 0 fail` | `52 checks · 52 pass · 0 fail` |
| collect-stages-a-shared-file-whole | `verify.sh exit 1` (red) | `verify.sh exit 1` |
| the-board-runs-itself/collect-is-a-command | `133 checks · 133 pass · 0 fail` | `133 checks · 133 pass · 0 fail` |
| the-board-runs-itself/specced-is-a-command | `verify: 90/90 checks pass` | `verify: 90/90 checks pass` |
| nothing-left-open/the-line-tells-the-truth | `verify: 85 checks · 44 pass · 41 fail` (red) | `verify: 85 checks · 44 pass · 41 fail` |
| the-board-runs-itself/hunks-land-where-they-came-from | `47 checks · 47 pass · 0 fail` | `47 checks · 47 pass · 0 fail` |
| resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule | `probe: 3 passed, 20 failed` (red) | `probe: 3 passed, 20 failed` |

`diff baseline after` is **empty**. Five harnesses were already red **before the
first edit**; all five are equally red in the orchestrator's own checkout at
`58c92e6`, run as a control, so none is an artefact of the scratch baseline
root and none is this unit's. **No flip is claimed by this pass.** The one
red-to-green this PRD's work produces — the eater block — is inside spec01's
own block and was earned by pass one, which built it.

The set is the 14 harnesses that name `resources/board/collect.py` or
`resources/board/specs.py`, grepped for the path spelled from the repo root.
The board-enumerating harnesses were not added: this footprint is under
`resources/`, not under the board, so the rule that adds them does not apply.

## The repo's own gate

`python3 resources/index.py check` in the lane: **5 lines, exit 1, identical to
the pre-edit baseline**, byte for byte. Every line names a file outside this
footprint (`references/skills/pearde-machine.md`, `@@share`, `index.md`,
`references/language.md`, `resources/board/edit.py`). The same command in the
checkout prints **1** line — the lane is behind the checkout on the other four,
and they close on the merge. Nothing here is to be repaired in the lane.

`bash resources/doctor.sh` in the lane, rows compared without `statusline`:
identical to the pre-edit baseline on every row except `knowledge`, which is a
sibling's — see below. `index broken`, `origin broken`, `memos broken`,
`workflows broken` were all red before the first edit; the last two are red in
the lane and green in the checkout, the "behind the checkout" shape again.

`python3 -m py_compile` clean on both footprint files. No formatter or linter
is configured in this repo — no `justfile`, `pyproject.toml`, `ruff`, `flake8`.

### Where the blocks were run

Not in the lane. `lanes.create` gives the lane a `.pearde/` holding only
`graphify/` — no `prds/` — and all three blocks read `.pearde/prds/…`:
spec01 runs a sibling's harness through it, spec02 and spec03 sweep the board
through it. Run in the lane they measure an empty board and pass vacuously.
They were run in a merged tree instead: `git clone --shared <checkout>`,
`git apply` of the lane's uncommitted diff, `.pearde` symlinked to the live
board — the root `collect` will run them from, with this build in it. Each
block was rebuilt into a fresh merged tree after every edit.

### Every block detects a regression, not just a renamed string

Mutations applied in the merged scratch tree, backed up by `cp` to a scratch
dir outside the repo and proved back with `cmp`:

| spec | behavioural mutation | block's exit |
|---|---|---|
| spec01 | `run()` put back on `input=script` | **1** — `FAIL broken tree went green: exit 0` |
| spec02 | the `$\((?!\()` guard put back to `$\(` | **1** — `FAIL the counter block is still accepted` |
| spec03 | `probe_verdict`'s `_seg_can_fail(lines[-1])` forced to `True` | **1** — `FAIL probe_verdict accepts a probe ending on an echo` |

`cmp` equal on both files after restore; all three blocks back to exit 0. These
are mutations of what the tool **computes**, not of a string a `grep` reads.

## Findings — not fixed, outside this footprint

**Carried forward from pass one, still open.**

- **One probe on the board has no verdict.**
  `a-verify-block-must-not-destroy-the-checkout-it-runs-in/probe/verify.sh`
  ends `echo "$PASS passed, $FAIL failed"`; its 24 checks can all go red and it
  still exits 0. That PRD is `done` and the file is outside this footprint. It
  is now the single file the new rule names, so the repair is one line: append
  the verdict with `printf` and a leading newline, since the file ends with no
  trailing newline.
- **`| head -N` is racy as well as truncating.** `head` cuts the failure line
  away and its early exit races the writer's SIGPIPE, so the same block can
  return 0 or 141 on identical input. The drain warning names this specifically
  for `head`.
- **`export VAR=$(pipeline)` masks the status; a bare `VAR=$(pipeline)` does
  not.** Caught today by `_cannot_fail_why` via `ALWAYS0`, incidentally rather
  than by a rule that knows why.
- **A naive drain detector over-fires** — 27 specs on a first cut. Confirmed at
  30 with the last-statement restriction, which is why it is a warning.

**New this pass.**

- **spec03's footprint is short by the `references/` prose it asks for.**
  The spec's "Left to finish" names "the two lines of `references/` prose that
  make the convention sayable", but `footprint:` holds only
  `resources/board/specs.py` and no acceptance box asks for the prose. Nothing
  was written outside the footprint. The convention is now enforced in code and
  quoted in `probe_verdict`'s docstring and its refusal message; a follow-up
  PRD owes it a line in `references/`.
- **`doctor`'s `knowledge` row went `ok` → `broken` mid-run, and it is not
  mine.** `knowledge: graph.json is behind the files: 260902-2085`.
  `pearde/wiki/sources/260902-2085.md` was written at **22:23**, six minutes
  after my baseline doctor at 22:17, by the sibling PRD
  `a-lane-s-wiki-is-a-stub-so-every-worker-s-knowledge-query-re` — its own
  `provenance:` names it. The graph was not relinked. Not in my footprint, not
  repaired.
- **The workflow's cited line numbers are stale** — both named in `### Edits`.

**Knowledge.** Nothing new was learned outside this repo this pass; every fact
used was measured here or already on record from pass one. Pass one's two
source notes still exist **only** in the lane's `pearde/wiki/sources/` and do
not travel with the lane's commits — the exact defect the sibling PRD above
owns. So that they survive the lane being discarded, both files are copied into
this PRD at `prds/…/probe/knowledge/260902-ee90.md` and `…/260902-9cf3.md`.
The orchestrator can re-run the two `remember` calls in the checkout from
those files; writing to `pearde/wiki/` is outside this footprint.

**Grammar.** No word in the contract was missing from
`python3 resources/grammar.py show`. `drain` and `formatter` in the new code
are that code's shorthand, not terms proposed for the vocabulary.

## Workflow probe-then-spec

| # | atomic | result | note |
|---|---|---|---|
| 1 | read-the-contract | pass | PRD body is the unfilled template — the title is the whole contract, as pass one recorded. Three specs read. `git status --short` recorded in **both** roots before the first edit: checkout clean at `58c92e6`, lane holding `resources/board/collect.py` and `resources/board/specs.py`. Both footprint paths exist. The step-1 lane row applied and its worry did not: the lane's base `7d65ef2` is an ancestor of the checkout's HEAD and both footprint files are identical at the two commits, so pass one's build is intact in the lane and the merge has nothing to refuse. |
| 2 | capture-the-harness-baseline | pass | 71 harnesses on the board, 14 read the footprint. Baselined against a `git clone --shared` at the lane's own HEAD — a real pre-edit tree, not inherited. 70 of 71 harnesses honour `PEARDE_ROOT`, so the merged-tree-and-symlink workaround was not needed for them. Five red before the first edit, confirmed red in the checkout as a control. |
| 3 | attempt-the-build | pass | Second pass on this route, but **not** the "nothing to do" case its table describes: spec01 and spec02 stood, spec03 said "Already standing: nothing" and was built. Built **in place** in the footprint file, not under `probe/` — the change is a new function and two call sites inside `specs.py`, which have no meaning outside it. Every fixture under `mktemp -d`, removed. |
| 4 | re-run-the-harnesses | pass | Same 14, same order, same command line, same `PEARDE_ROOT`. `diff` of the two runs empty. No count rose and none dropped, so no flip is attributed either way. |
| 5 | write-the-specs | n/a — second pass | Specs already existed; this pass applied the section's `Fails when` table to the blocks that stand rather than authoring one. All three blocks run the way `collect` runs them, all three proved to fail on a behavioural mutation. |

### Edits

Two stale line citations in the atomics, both measured against the checkout at
`58c92e6`. Never edited here.

**`write-the-specs`, step 4** — reads "the checker at
`resources/board/specs.py:523` matches the `footprint:` string". That matcher,
the `any(p in b for b in blocks for p in fp)` line in `check_spec`, is at line
**535**. Replacement text:

> Give each spec a `## Verify and Proof` block in which every path is
> spelled **literally**, not through a variable — the checker in
> `check_spec` (`resources/board/specs.py`, the `any(p in b for b in blocks
> for p in fp)` line) matches the `footprint:` string, and a
> `"references/personas/$f.md"` reads as no footprint path at all.

**`write-the-specs`, step 4** — reads "the pair at
`resources/board/collect.py:1242`". The `["bash", "-e", "-o", "pipefail"]` pair
is now at lines **1300** and **1849**. Replacement text:

> The flags are `bash -e -o pipefail` — the pair `collect.py` passes to
> `run` and to `guarded_run` — and both matter, in opposite directions:

A third edit, for a shape no row lists. `capture-the-harness-baseline` and
`write-the-specs` both tell a worker in a lane where to run a **harness**;
neither says a lane cannot run a **spec's own block**. `lanes.create` gives the
lane a `.pearde/` holding `graphify/` and no `prds/`, so any block naming
`.pearde/prds/…` — spec01, spec02 and spec03 all do — sweeps an empty board and
passes vacuously in the lane. That is a green block measuring nothing, which is
the failure this whole PRD is about. Proposed new row for `write-the-specs`'s
`## Fails when`:

> | a block reading `.pearde/prds/…` passes in the lane and its census counts read 0 or near it | `lanes.create` gives the lane its own `.pearde/`, holding `graphify/` and no `prds/` — the block is sweeping an empty board and passing vacuously | build the merged tree (`git clone --shared <checkout>`, `git apply` the lane's diff, `ln -s <board> <scratch>/.pearde`) and run every block there, rebuilding it after each edit. Quote a census count from the block: a sweep that finds no PRDs is the tell |

## The numbers

19 of 19 acceptance boxes ticked across three specs, each against quoted
output. 14 harnesses re-run, 14 counts unchanged, 0 regressions, 0 flips
claimed. 139 PRDs swept by the new refusal, 1 refused and it is `done`. 279
verify blocks swept by the new warning, 30 warned, 0 refused. Two files
changed, both in the footprint: `resources/board/collect.py`,
`resources/board/specs.py`.
