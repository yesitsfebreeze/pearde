---
state: done
origin: requested
priority: 75
complexity: 8
blast-radius:
workflow: probe-then-spec
actual: 11.72h
commit: a27c5c0
---

# two harnesses still name a tree they do not measure

<The request, for an analyst who knows the codebase but not this conversation:
what exists when this is done and why, what must not change, pointers to files
and prior PRDs. One contract per PRD — a second is a second PRD, or a split via
refine.>

## Report

spec01: exit 0
probe: two harnesses still name a tree they do not measure — board /Users/feb/dev/infra/pearde/.pearde
A. each of the four takes its root from the runner
  ok   A1 every-run-session-works-in-a-worktree-of-its-own/probe
  ok   A1 a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe
  ok   A1 resources-are-organised-by-responsibility/probe
  ok   A1 every-module-finds-its-siblings-by-one-rule/probe
B. the root each one resolves, measured by running it
  ok   B1 session harness is red against a tree with no sessions.py
  ok   B2 …and red for that reason, not another
  ok   B3 …and green when the runner names the tree that holds it
  ok   B4 every-run-session-works-in-a-worktree-of-its-own reads the tree the runner named
  ok   B4 a-session-ledger-names-who-holds-what-and-reaps-what-is-gone reads the tree the runner named
  ok   B4 resources-are-organised-by-responsibility reads the tree the runner named
  ok   B4 every-module-finds-its-siblings-by-one-rule reads the tree the runner named
C. section A can fail — proven on a copy, never on the file itself
  ok   C1 a planted defect is seen: does not read ${PEARDE_ROOT:-;counts .. to reach the repo
  ok   C2 a planted defect is seen: does not read ${PEARDE_ROOT:-;names an absolute root
  ok   C3 a planted defect is seen: does not walk up to its board
  ok   C4 a planted defect is seen: does not read ${PEARDE_ROOT:-
  ok   C5 …and the file it was copied from is unchanged
probe: 16 passed, 0 failed
PROBE GREEN  <- prds/every-run-session-works-in-a-worktree-of-its-own/a-session-ledger-names-who-holds-what-and-reaps-what-is-gone/probe/verify.sh
probe: 18 passed, 2 failed  <- prds/resources-are-organised-by-responsibility/probe/verify.sh
probe: 3 passed, 20 failed  <- prds/resources-are-organised-by-responsibility/every-module-finds-its-siblings-by-one-rule/probe/verify.sh
