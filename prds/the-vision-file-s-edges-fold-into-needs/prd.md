---
state: done
origin: requested
priority: 26
complexity: 12
blast-radius: low
workflow: probe-then-spec
actual: 0.65h
commit: 4680284
---

# The vision file's edges fold into needs

*Source: `docs/content/docs/improvements/board-vision-needs.mdx` — the page this PRD files. It left the working tree mid-pass (a concurrent collect parked it); recover the prose at git 6839a9b if the file is gone. The body below is the page's own argument.*



**Tool:** board · **Axis:** sensibility (7 → 8) · **Pulls the score up by
~4 points**

## Why now

The vision file carries three keys: `vision:` (one sentence, where the board
is going), `terminals:` (the PRDs whose completion *is* the vision), and
`edges:` — "a dependency nobody wrote as `needs:`". That last key is the
tell: the plan reads edges because a PRD may have *forgotten* to say
`needs:`. Two orderings now hold the same truth — the PRD's frontmatter and
the vision file — and the plan must reconcile them on every read. A
dependency that exists only in `edges:` is a PRD whose own file lies.

## The change

`edges:` stops being an input to the plan and becomes a *check*: the plan
still reads `needs:` alone, and a vision edge whose PRDs do not declare the
matching `needs:` is reported — by the same derived-work tripwire that
reports work the board found — as "the vision says X needs Y; X does not".
The fix is one line in the PRD, made obvious. `edges:` shrinks to the
empty state it should mostly be.

## Done when

- A board whose PRDs declare every vision edge plans identically before and
  after (byte-identical `plan` output — the ordering did not change).
- A board with one un-declared edge reports the pair, PRD-named, on the
  next plan; adding the `needs:` silences it.
- The vision template's `edges:` row documents the new meaning, and the
  reference stops calling it an input.

## Fails when

- The tripwire fires on an edge that is *intentionally* plan-only — an edge
  between PRDs from different boards. Guard: the check crosses members the
  same way `needs:` resolution does, or the edge names its board.

## What stays out

No removal of `edges:` — the key stays for cross-board edges the PRDs
cannot see. What changes is who reads it as truth: the check, not the plan.

## Report

spec01: exit 0
## every edge already declared as needs: — no change in plan output
  ok   vision output byte-identical with a declared edge present or absent
  ok   vision --json byte-identical with a declared edge present or absent
  ok   --check exits 0 on a fully-declared edge
## an edge is no longer a hop — it does not deepen the axis
  ok   far is not placed on the axis by the edge alone
  ok   far is off-axis — the edge named no needs:
## an undeclared edge is reported, PRD-named — adding needs: silences it
  ok   --check exits 1 on an undeclared edge
  ok   the pair is named, PRD-named
  ok   doctor's vision row carries the same line
  ok   adding the matching needs: silences the report
## an edge naming no PRD is still reported the old way
  ok   --check exits 1 on a dangling edge end
  ok   the dangling end is still named the old way
verify: 11/11 checks pass
0
resources/common.py is on disk with no row in references/files.md
references/files.md lists @resources/board/hotreload-test.js — not on disk
@@view names @resources/board/hotreload-test.js — not on disk
references/parts/handles.md references @@purge — no such keyword
references/parts/handles.md references @resources/board/purge.py — not on disk
