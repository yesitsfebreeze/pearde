---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
estimate: "1h"
description: "`~/.cargo/bin/memory` predates the tree's newest dispatch rows and `health` fields, so it answers `unknown operation` for them and every negative a check reports against it is vacuous — and `just install` cannot fix it while the trunk holds nine sessions' uncommitted `src/`"
---

# the installed binary answers for a memory that is gone

Found 2026-09-09 by a lane checking its work against the installed
`~/.cargo/bin/memory`: that binary answers `unknown operation` for a dispatch row
the tree had just gained, and its `health` carries none of the fields that
landed with it.

The trap is that a check against the stale binary **passes silently**. A
negative — no row in the daemon log, no counter moved — is what lanes report as
their strongest evidence, and against this binary that sentence is true of a
defect that fired on every call. The lane caught it by rebuilding
`target/debug/memory` in the lane and then proving the channel live with a
deliberate probe that did raise the row and moved the counter to 1.

`just install` is the obvious fix and is not available: the trunk holds nine
sessions' uncommitted `src/` files, so installing from it would ship their
unlanded work, and it needs a daemon stop besides
([a-killed-daemon-pays-a-full-index-rebuild](../a-killed-daemon-pays-a-full-index-rebuild/prd.md)).

## Do

Make the trap loud instead of silent. The cheapest form: `memory health` reports
the build it is answering from — a commit or a build stamp — so a checker
comparing it against `git rev-parse HEAD` sees the mismatch, and a lane's
Check can name the binary it measured. A positive control is the other half:
a check that claims a negative first proves the channel by raising a positive,
the way that lane did by hand ([[what-makes-an-empty-lsp-answer-trustworthy]]
asks the same question of an empty LSP answer).

Not in scope: running `just install` on a dirty trunk.

Done 2026-09-09. `memory health` opens with a `build:` line naming the daemon's
executable and its mtime — `identity::build_stamp()` over `HealthRes.build_stamp`,
append-only beside the `build_id` hash that was already on the wire and never
printed. A daemon predating the field sends nothing, and the line says
`(unstamped: older than this field, or an unreadable executable)`, which is the
whole signal: measured live against a scratch-root daemon started from
`~/.cargo/bin/memory` (the stale one this memo is about) it prints exactly that,
and against a daemon from this branch it prints the path and the build time. The
positive-control half of the Do — a check that proves a channel by raising a
row before trusting an empty one — is a practice for lanes, not code, and is
not in this change.

The diagnosis was verified before it was built on: the installed binary carries
none of the newer `health` fields, and its live `memory health` prints the
degraded line ending at `failed memory writes`.

## Acceptance
A daemon started from a binary older than the tree is visibly older —
`memory health` names its build, and a lane that checks anything against it can
say so from the answer alone rather than by remembering to rebuild.
