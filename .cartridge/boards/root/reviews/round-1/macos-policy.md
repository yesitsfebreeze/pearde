---
state: open
origin: requested
priority: 60
complexity: 0
blast-radius:
needs:
  - command-adapter
---

# macos-policy — macOS commands enforce manifest capabilities through sandbox-exec with verified runtime exceptions and real allowed/denied operation tests.

macOS commands enforce manifest capabilities through sandbox-exec with verified runtime exceptions and real allowed/denied operation tests.

## Implementation handoff

complete the macOS manifest policy and adversarial OS proof

Complexity 15; blast-radius mid. Starts from the existing Seatbelt compiler and
five unit plus five live-wall checks. Owns `src/sandbox.rs` after the adapter
handoff; add backend tests in the same module. Exercise granted and denied
reads, writes, execution, networking, canonical paths, escaping profile text,
and scripts. Boot failure is not proof of resource denial. Review broad runtime
exceptions against what a child actually needs. Preserve Q1: nonempty network
opens networking, with hostname limitations stated explicitly.

The build hit this owner at policy compilation and direct live-wall tests.
Completion is meaningful OS enforcement independent of the launch caller.


Source snapshots and verified probes are listed in `../report.md` under Exact source handoff. Apply only this child's files from those patches; preserve unrelated changes.
