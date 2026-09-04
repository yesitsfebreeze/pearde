---
state: specced
origin: requested
priority: 26
complexity: 12
blast-radius: mid
workflow: probe-then-spec
---


# One board-path resolver fewer

*Source: `docs/content/docs/improvements/board-path-resolver.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** board · **Axis:** integration (8 → 9) · **Pulls the score up by
~3 points**

## Why now

The board's directory is found by four rules: `.pearde/` carrying a board,
`pearde/` carrying one (legacy), the one immediate child holding
`settings.md`, else the default. The dot cost the board nothing; the
undotted name cost two outages — one board answering to two names fanned
every dispatch out twice and refused every collect. The compat symlink is
read *through*, so the resolver carries the history everywhere it runs, and
it runs in scan, guard, doctor, the status line and the view. Every module
finds its siblings by one rule; the *board* is still found by several.

## The change

The legacy-name rule retires on a date: `pearde upgrade` moves the last
`pearde/` boards once and the resolver drops rule 2 — the compat symlink
reads *through* no longer, it resolves as a link like any other link. One
rule remains above the fallback: `.pearde/` or nothing, else the child with
`settings.md`. The outage class (one board, two names) becomes structurally
impossible rather than guarded against.

## Done when

- A checkout holding both `.pearde/` and a `pearde/` compat link, after
  `pearde upgrade`, holds one real directory — and the resolver's tests for
  the link-through case are deleted with the rule.
- Every resolver call site (scan, guard, doctor, statusline, serve) goes
  through the one function — provable by the same grep that proves the
  sibling rule.
- The reference's four-rule table becomes three, and the two outages'
  memos stay as the reason.

## Fails when

- A board that never upgrades keeps resolving — the rule is dropped from
  the *resolver*, not from the upgrade script, which must still move an
  old board. Guard: the upgrade path keeps its own resolution until the
  move is done.

## What stays out

No rename of any board on this machine — `upgrade` already moves boards
that have not run it; this page only stops the resolver from carrying the
compatibility forever.

## History

**failed, retried 2026-09-03 21:03**

swept 2026-09-03 21:01 — claim impl-path-resolver 2026-09-03 17:46, silent 3.2h: no file of this PRD's moved past `claim-ttl`. Read the worker's output before a retry; partial code stands on branch `lane/one-board-path-resolver-fewer`, whose worktree this sweep removed — the branch is kept.

## Blocked

**2026-09-03 21:56 — the lane will not rebase**

`lane/one-board-path-resolver-fewer` does not land on `main`; 1 file(s) disagree:

- `references/files.md`

Nothing is lost: the worker's commits are on `lane/one-board-path-resolver-fewer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-board-path-resolver-fewer`.

**2026-09-04 02:28 — the lane will not rebase**

`lane/one-board-path-resolver-fewer` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/one-board-path-resolver-fewer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-board-path-resolver-fewer`.

**2026-09-04 04:18 — the lane will not rebase**

`lane/one-board-path-resolver-fewer` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/one-board-path-resolver-fewer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-board-path-resolver-fewer`.

**2026-09-04 09:31 — the lane will not rebase**

`lane/one-board-path-resolver-fewer` does not land on `main`; git named no file — `git status` in the lane says which.


Nothing is lost: the worker's commits are on `lane/one-board-path-resolver-fewer` and the checkout never moved. Resolve the conflict in the lane, then `pearde unblock one-board-path-resolver-fewer`.
