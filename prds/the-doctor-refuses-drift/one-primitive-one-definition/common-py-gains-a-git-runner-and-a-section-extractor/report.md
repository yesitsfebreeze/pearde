Verdict: DONE

# common-py-gains-a-git-runner-and-a-section-extractor — implementer report

Followed `probe-then-spec` as the second pass named in its "Use when": specs
already existed (`specs/spec01.md`, all three acceptance boxes already
ticked by the analyst pass whose `report.md` was here before this one).
Step 3 was a re-measure, step 5 applied the atomic's `## Fails when` table
to the block that already stands, without authoring anything new. Per
that table's "the report path already holds a previous pass's report" row,
the analyst's `## Findings` are carried forward below by name, not dropped.

## Workflow probe-then-spec

| # | step | result |
|---|------|--------|
| 1 | read-the-contract | `prd.md` body is the title only, no `## Answers`; `specs/spec01.md` read whole. `git status --short` in the lane: ` M resources/common.py` — the probe's uncommitted code, already there as the brief said. Checkout `git status --short`: unrelated dirty files (`references/drill.md`, `references/skills/pearde-drill.md`, `resources/board/dispatch.py`, `.pi/`), none touching this footprint |
| 2 | capture-the-harness-baseline | Baseline already recorded in `spec01.md`'s "What already stands" and the analyst's report; re-confirmed by step 3's re-measure below rather than re-captured on a clean tree, since the edit already stands and cannot be reverted without destroying pass one |
| 3 | attempt-the-build (re-measure) | `resources/common.py` tail read: `run_git` and `section` match the signatures spec01 states, byte for byte. Probe run: `PASS: every checked caller contract reproduced` (exit 0). `ast.parse` on `resources/common.py`: `common.py parses` |
| 4 | re-run-the-harnesses | `PEARDE_ROOT=<lane> python3 resources/index.py check` vs. checkout's own run: identical 6-line output both times, exit 1 both — `resources/common.py is on disk with no row in references/files.md` pre-existing, not new. `PEARDE_ROOT=<lane> bash resources/doctor.sh` vs. checkout: `diff` empty, both exit 1, both 87 lines — no drift from this edit |
| 5 | write-the-specs (apply Fails when, no authoring) | Checked spec01.md's block against the table: no board-wide gate inside the `## Verify and Proof` block, no inverted-status or vacuous-pass shape, no `## ` inside a heredoc, box 3's quoted output matches what running the commands prints now. Nothing to change |

### Edits

None — the atomics' `on failure` and `Fails when` shapes matched what actually happened; no wrong command, stale path, unfalsifiable check, or uncovered shape found.

## Findings (carried forward from the analyst's pass)

- `resources/common.py is on disk with no row in references/files.md` was
  already failing `index.py check` before this edit — pre-existing, not
  this PRD's footprint to fix. Reconfirmed still true and still identical
  between lane and checkout.
- `resources/board/refuse.py`'s `_run` also runs `ps`, not only `git`; it
  cannot fully delegate to `run_git` — only its git-only call sites can.
  Worth the delegate PRD's attention, not a spec of its own.
- `resources/questions.py`'s `sections(body, pattern)` anchors on the
  literal `## ` prefix (`Q_RE = r"^##\s+Questions\b"`); migrating this
  caller to `common.section` means redefining `Q_RE` to `r"Questions\b"`,
  or using `prefix=True, word=True` — proven equivalent in the probe, a
  migration-time simplification, not a behaviour change.

## Acceptance (spec01)

- [x] `common.py` defines `run_git` and `section` with the signatures
  above, stdlib only (`os`, `re`, `subprocess`, `sys`). Confirmed by
  reading the tail of `resources/common.py` in the lane.
- [x] A probe reproduces, for every cataloged caller, both its success
  shape and its failure shape from a one-line call into the new primitive.
  Ran: `PEARDE_ROOT=<lane> python3 <prd>/probe/probe_common.py` →
  `PASS: every checked caller contract reproduced`
- [x] `resources/index.py check` and `resources/doctor.sh` show no new
  failures against the pre-edit baseline. Ran both in the lane and in the
  checkout: identical output, identical exit codes, `diff` empty on
  `doctor.sh`'s full output.

## Verify and Proof

```
$ PEARDE_ROOT=<lane> python3 .pearde/prds/.../probe/probe_common.py
PASS: every checked caller contract reproduced
$ python3 -c "import ast; ast.parse(open('resources/common.py').read())" && echo "common.py parses"
common.py parses
```
