---
state: done
origin: requested
priority: 90
complexity: 32
blast-radius:
workflow: probe-then-spec
actual: 0.31h
---

# a verify block that pipes a probe exits zero on a broken tree under pipefail

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
0 problem(s)
24 passed, 0 failed
spec01 green

spec02: exit 0
checked 10 shapes
0 problem(s)
spec02 green

spec03: exit 0
34 probe(s) swept · 1 with no verdict: ['a-verify-block-must-not-destroy-the-checkout-it-runs-in']
0 problem(s)
spec03 green
