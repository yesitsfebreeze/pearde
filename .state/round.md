# round — at its budget. the next session resumes from here.

The guard is right: this window is 390k and the board is on disk. **`context-budget` is restored to `160k`** and the exemption fix is live (workers carry `agent_id`/`agent_type`, the orchestrator is refused past the ceiling — measured after restore, both shapes pass).

## End the round here. Eight analysts were dispatched and are STILL RUNNING

They write their reports and return one-line verdicts; a fresh session acts on
them via `python3 resources/board/plan.py scan` + this file:

| PRD | worker claim |
|---|---|
| the-board-asks-for-itself/two-questions-start-a-drill | an-20 |
| the-other-boards-move-once-and-the-script-goes | an-21 |
| the-collect-and-brief-harnesses-are-carried-across-the-layou | an-21 |
| an-acceptance-box-that-cannot-fail-is-refused | an-22 |
| an-analyst-workflow-does-not-survive-into-specced | an-22 |
| collect-commits-only-the-prd-s-own-edits-not-the-footprint-s | an-23 |
| the-view-row-names-a-variable-that-exists | an-24 |
| collect-commits-.../list-the-collects-the-repo-bug-orphaned | an-24 |

Their reports land at `.pearde/prds/<prd>/report.md`; each ends `## Scores`.
`pearde specced <prd>`, then claim + dispatch implementers. Every collect
needs the code repo clean first — `collect` now handles both repos itself
(the repo-default fix landed), so NO hand-committing.

## What is DONE and committed — 49/53 requested, 93%

Landed this round, both repos clean (code repo head `7809756`, board repo
`2a3c69a` + collects after): apply-the-prds-rename-table, the-vault-ignores,
the-sweep-leaves-nothing, collect-defaults-to-the-boards-enclosing-repo
(THE repo bug), state-dir, example-layout, route-at-spec-time, one-definition,
brief-gate (brief now takes --worker; stop forcing), doctor board/guard/skills
rows, doctor exit 0, budget-ceiling guard fix (`dispatched(data)` exempts
workers; `--worker`), knowledge-loop, graph-in-board, probe-harness wall
(878d164 — ~25 harnesses re-aimed, 4 product defects fixed at root: members()
double-join, add() relpath, init.py plugin-dir makedirs, stale daemon regs),
a-quoted-walk-is-data, the-line-tells-the-truth (30/31 boxes; the last is a
reconciled dead diff assertion), nothing-left-open,
every-document-names (container).

## End-of-round verification — the gate

`index.py check` 0 · `memos.py check` 0 · `workflows.py check` 0 · doctor exit 1
ONLY on `origin: 7 derived in flight vs 7 requested` (clears when the analysts land)
· code repo clean · board repo clean.

## The round's own hazards — read before touching anything

- Every board command needs `--as engineer` (this shell is nu). `settings`
  refuses `--as`.
- `brief` no longer needs `--force` IF you pass `--worker <the claim's holder>`.
  The documented loop now works as written.
- Verify blocks run `bash -e -o pipefail` from the code repo on stdin. Guard
  expected failures with `|| true`; never pipe a non-zero producer into grep;
  a bare grep finding nothing exits 1 when clean; end on an explicit echo.
- Probe code never goes in `footprint:` — `collect` refuses board paths.
- `collect` reads a Verify block's LAST exit; a block that ends on grep/head/
  echo unconditionally is a check that cannot fail — PRD
  `an-acceptance-box-that-cannot-fail-is-refused` owns making `specced` refuse.
- Workers died twice on the 100k ceiling applied per-worker and once clobbered
  this very file when the guard left it the only writable path. Both fixed and
  committed; the budget is back at 160k.
- `.pearde` (BOARD repo) holds prds/memos/workflows/.state; the CODE repo holds
  references/ resources/ README.md index.md. Briefs carry the correction.

## Asked

Nothing is out to the user.
