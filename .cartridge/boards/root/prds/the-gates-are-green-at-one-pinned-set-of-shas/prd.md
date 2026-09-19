---
state: open
origin: requested
priority: 80
repo: "/Users/feb/dev/cartridge"
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: root
work-kind: milestone
wave: 2
date: "2026-09-15"
footprint: []
needs:
- the-record-has-one-vocabulary-and-no-shadowed-copies
- sessions-and-gitfs-tests-are-green
- pty-router-harness-mcp-tests-are-green
- host-tests-hold-under-suite-contention
- smoke-passes-mcp-and-proxy
---

# The gates are green at one pinned set of SHAs

## Outcome

Milestone 1. The composition is provably green before anything is built on it.

## Acceptance

- [ ] From `/Users/feb/dev/cartridge` at one recorded set of submodule SHAs: `just check`, `just test`, `just smoke`, `just verify` exit 0 and `just isolation` reports nothing; the SHAs are in Result.

## Folds

Deferred with `superseded-by` pointing here:

- @root/the-composed-system-proves-the-plan
- @root/cartridge-improvement-programme

## Result

Not started.

## Why this row never becomes dispatchable while work is in flight (2026-09-17)

Its footprint is `/Users/feb/dev/cartridge` — the whole repository. That
reserves everything, so `plan` holds it against any claim on the board and it
has been held all day, first by the proxy PRD and then by each successor in
turn. The blame `plan` prints names whichever PRD happens to hold a claim; it is
not really about that PRD.

This is not a defect in the row. A gate run across one pinned set of shas is
only meaningful on a quiet board, because any lane that lands while it runs
changes the shas it is attesting. So this row is by nature the LAST thing done,
not a row to squeeze in beside others.

Practical consequence for whoever picks it up: release every claim first, let
every lane land or be set aside, and only then claim this. Running it early
produces a receipt that is already stale.

Measured today, and the reason it matters: twenty-plus submodule pointers moved
during this session and no composed gate run happened across them. `just audit`
and `just isolation` are green at 18 of 18 as of the web.ctg collection, but
`just check`, `just test` and `just smoke` have not been run over the whole
composition at one sha.
