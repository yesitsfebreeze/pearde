---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/own.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/ask.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/host/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp/base.rs
commit: "1404881a611d85262cdea227974f9c86c92800fa"
---

# the host's cartridge entities carry state and generation

## Outcome

The host's `cartridge:` entities carry what memo's `kernel` context source gave: every cartridge of the profile, not only the active ones, with its lifecycle state as `host.state`, its failure or wait reason as `host.error`, and its start count as the node's revision, so a fact another cartridge asserted about it before a restart comes back stale. With this, memo's `kernel` source has nothing left that ASP lacks.

## Acceptance

- [x] A named test expands `cartridge:<id>`, sees `host.state` `active` and revision `1`, restarts the cartridge, and sees the revision move.
- [x] `docs/asp.txt` describes the attributes and the revision.

## Note (2026-09-19, ASP coordinator)

The collected commit `1404881` was rebased onto the user's `f3bf806` (a
README rename to Ackin, pushed from GitHub) before it was pushed, because
`main` on the remote had moved. The pushed commit is `445a87f`. Its tree
differs from `1404881` only by that README change.
