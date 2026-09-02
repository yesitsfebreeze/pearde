---
state: done
origin: derived
priority: 90
complexity: 8
blast-radius: mid
from: collect-must-not-reset-the-checkout-it-did-not-write  # derived only — the PRD whose work surfaced this one
workflow: probe-then-spec
actual: 0.7h
commit: d240590 a2019f2
---

# a refused rebase must not destroy the lane it was left in

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
192:            aborted = git(wt, "rebase", "--abort", check=False)
193:            if aborted.returncode == 0:
== case 1: refused rebase (dirty tree, no real conflict) ==
merge() raised: merge conflict: lane/x onto main — see git status
-- lane_wt state after the refusal --
 M other.txt
PASS: the lane's uncommitted dirt survived the refused rebase

== case 2: a genuine mid-rebase conflict still resolves cleanly ==
merge() raised: merge conflict: lane/y onto main — f.txt
-- lane_wt2 state after the conflict --
PASS: branch/tree restored to the pre-rebase tip

2 cases · 2 pass · 0 fail
