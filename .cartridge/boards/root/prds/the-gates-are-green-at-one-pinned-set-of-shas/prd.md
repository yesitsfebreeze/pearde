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
