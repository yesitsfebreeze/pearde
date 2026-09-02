---
state: done
origin: requested
priority: 85
complexity: 18
blast-radius:
workflow: probe-then-spec
actual: 0.35h
---

# collect stages the board s gitignore in the outer repo which ignores it

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
PASS both layouts: the board's own file is committed in the board repo, the flat layout is unchanged
fixture: /var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/pearde-gitignore-check-kz2up0w9
PASS mutant: the check goes red when foot_root routes nothing

spec02: exit 0
PASS  the lane does not hold the board own file — it is cut without the board
PASS  nested: collect exits 0 (got 0)
PASS  nested: no run hits `fatal: pathspec … did not match any files`
PASS  nested: a NEW commit in the BOARD repo holds .gitignore
PASS  nested: the board working tree is clean after (got '')
PASS  nested: the code repo commits the code file
PASS  nested: the code repo never stages the board own path
PASS  nested: collect names the board-owned path it dropped from the lane add
PASS  flat: collect exits 0 (got 0)
PASS  flat: the code file lands in the one repo there is
PASS  flat: nothing is rerouted — the two roots are one
PASS  every fixture is under one mktemp -d, removed on exit (/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.5PzAlHIEeq)
PASS  the lane does not hold the board own file — it is cut without the board
FAIL  nested: collect exits 0 (got 1) — collect: p1: fatal: pathspec 'pearde/.gitignore' did not match any files — nothing written; the lane still holds the work on `lane/p1`
FAIL  nested: no run hits `fatal: pathspec … did not match any files`
FAIL  nested: a NEW commit in the BOARD repo holds .gitignore
FAIL  nested: the board working tree is clean after (got ' M .gitignore')
FAIL  nested: the code repo commits the code file
PASS  nested: the code repo never stages the board own path
FAIL  nested: collect names the board-owned path it dropped from the lane add
PASS  flat: collect exits 0 (got 0)
PASS  flat: the code file lands in the one repo there is
PASS  flat: nothing is rerouted — the two roots are one
PASS  every fixture is under one mktemp -d, removed on exit (/var/folders/_p/tzmzw3m10kg7sg9hc7_mkm7w0000gn/T/tmp.GCs6HWxHcB)

6 check(s) failed — the invariant is broken.

spec03: exit 0
