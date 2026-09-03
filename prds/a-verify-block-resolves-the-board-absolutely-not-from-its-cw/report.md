# report — a-verify-block-resolves-the-board-absolutely-not-from-its-cw

Verdict: DONE

This route was already run once — the analyst pass wrote `## Workflow
probe-then-spec` and `SPECCED` below (kept, per this route's own `Fails
when`: "the report path already holds a previous pass's report ... carry
its `## Findings` forward into yours by name"). This is the second pass:
implementing the specs that already stand, per the workflow's own `Use
when` — "the specs **do** exist and an implementer is dispatched on this
same route" — so steps 3 and 5 below re-measure and re-check rather than
build or author.

`prd.md`'s body is still the unedited template; the contract is
`specs/spec01.md` and this file's own prior pass, per step 1's `Fails
when` row for a placeholder body.

## Workflow probe-then-spec

| # | step | result |
|---|------|--------|
| 1 | read-the-contract | Read `prd.md` (template body), `specs/spec01.md`, this report's prior pass, and the sibling PRD it cites (`the-verify-guard-parses-git-s-own-output-before-it-trusts-it`). `git status --short` in the lane: ` M resources/board/specs.py` — the probe's code, already there. |
| 2 | capture-the-harness-baseline | Footprint `resources/board/specs.py`. Harnesses that read it: `an-acceptance-box-that-cannot-fail-is-refused/probe/verify.sh` and `an-analyst-workflow-does-not-survive-into-specced/probe/verify.sh`. Repo gate: no `verify:` key on the PRD; documented gate is `python3 resources/index.py check` + `bash resources/doctor.sh`. Baselined **both roots** (lane is 20+ commits behind the checkout's `HEAD` — cut before `d0a8da0`, the `pearde/`→`.pearde/` prose rename): checkout `index.py check` exits 0, clean; lane exits 1 with 4 lines, all naming `.md` prose (`references/files.md`, `references/parts/commits.md`), none naming `specs.py` or `resources/board/`. `doctor.sh` in the checkout is already exit 1 before any edit — pre-existing rows: `memos` (missing `tags:`), `knowledge` (graph stale), `questions` (dangling `## Answers`) — none name `specs.py` or `resources/board/`. |
| 3 | attempt-the-build (re-measure, per the second-pass rule) | Symlinked the live board into the lane (`ln -s /Users/feb/dev/infra/pearde/.pearde <lane>/.pearde`, gitignored both spellings) so the probe and the two harnesses resolve. `git diff -- resources/board/specs.py` in the lane already carries `_hardcoded_root`, `check_spec(..., repo=None)`, and `read_specs` threading `repo` through — matches spec01's contract exactly. |
| 4 | re-run-the-harnesses | `probe_hardcoded_cd.py`: `9 passed, 0 failed`, all 4 refusal cases carry file:line, all 4 "untouched" cases clean, `repo=None` skip clean. `PEARDE_ROOT=<lane> bash .../an-acceptance-box-that-cannot-fail-is-refused/probe/verify.sh` → `verify: 2 passed, 0 failed`. `PEARDE_ROOT=<lane> bash .../an-analyst-workflow-does-not-survive-into-specced/probe/verify.sh` → `verify: 21/21 checks pass` (both runs carry one identical, pre-existing `rm: ... is a directory` stderr line, reproduced unmodified in the checkout too — not a regression). Per this route's "repo-wide gate is red in the lane on lines the checkout does not print" row: the 4 `index.py check` lines are absent in the checkout and present in the lane, i.e. they close on the merge — none is a live finding against this footprint. |
| 5 | write-the-specs (apply Fails-when only, per the second-pass rule) | No new spec authored. Ran `grep -c '^- \[ \]'` (0 remaining unticked before this pass) and `PEARDE_ROOT=<lane> python3 resources/pearde.py specced <prd> --check --as engineer` → `ok · complexity 8 · footprint resources/board/specs.py`, one warning ("4 of 4 boxes already ticked before an implementer ran them") — expected, since this run is the implementer ticking them. Ran the PRD's own `## Verify and Proof` block verbatim: `python3 .pearde/prds/<prd>/probe/probe_hardcoded_cd.py` → exit 0, `9 passed, 0 failed`. |

### Edits

None — every atomic's command ran as written, no stale path, no check that
cannot fail, no shape outside its `## Fails when` table.

## What ran, per box

`specs/spec01.md`'s four boxes are all `[x]`, each ticked with the command
and output that closed it (`probe_hardcoded_cd.py` per-case lines, and the
two harnesses' final lines) — see the spec file itself, not repeated here.

## Findings carried forward from the prior pass — not fixed here, out of footprint

- **72 existing spec files, across mostly `done` PRDs, still hardcode
  `cd /Users/feb/dev/infra/pearde`.** This PRD's check only gates *new*
  specs at `specced` time; retrofitting the 72 is a different PRD's
  footprint.
- **A subset of those same 72 blocks additionally read `P=prds/<slug>/probe`**
  (no leading `.pearde/`) — a spelling from before the board's directory
  was renamed to `.pearde/` (`d0a8da0`) — e.g.
  `finished-counts-both-files/specs/spec01.md`.

## New finding this pass

- The lane worktree for this PRD was cut at commit `0c8fd02`, well behind
  the checkout's `HEAD` (`4a94475` at the time of this run) — it predates
  `d0a8da0` (the `pearde/`→`.pearde/` prose rename). `index.py check` run
  inside the lane therefore reports 4 stale-prose lines the checkout does
  not. Not this PRD's to fix: it closes on the lane's next rebase/merge,
  not on an edit to `resources/board/specs.py`.

## Scores

complexity: 8
blast-radius: low
workflow: probe-then-spec
