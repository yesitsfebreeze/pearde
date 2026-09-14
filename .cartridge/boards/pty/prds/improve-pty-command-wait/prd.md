---
repo: /Users/feb/dev/cartridge/pty.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-capability-owner: pty
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: improve-pty-command-wait
needs:
- '@pty/improve-pty-shell-identity'
footprint:
- /Users/feb/dev/cartridge/pty.ctg/src/main.rs
- /Users/feb/dev/cartridge/pty.ctg/src/tool.rs
- /Users/feb/dev/cartridge/pty.ctg/src/marks.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/tests/integration/process.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/tests/unit/marks/tests.rs
---

# Wait and retrieve output for one terminal command

Baseline (pty 0db055d, transport port): OSC 133 marks give each command an `id`
(`src/marks.rs`); `pty {op:"commands"}` lists bounded history with ids; `Shell::run` waits for
the done mark, never kills on timeout, and marks output past the limit as "truncated; tail
shown" (`src/main.rs`). Gaps: the `tool.shell` command result is text without the id, a caller
cannot wait on an id later, an id evicted from history is indistinguishable from unknown, and
the handoff record beside this PRD shows unresolved delayed-mark correlation. Excluded: input
lease semantics (`@pty/improve-pty-input-ownership`) and the tui.

## Acceptance

- [ ] A `tool.shell` command result carries its command id, exit (or running) and `truncated`, as additive fields.
- [ ] Waiting on command A's id while B later completes returns A's own exit and output; a wait timeout leaves A running.
- [ ] An id evicted from history, or a shell without mark integration, returns an explicit `unavailable` reason, never a false completion.
- [ ] A marker arriving after the wait deadline is attributed to the right id on the next wait (fixture from the handoff context).

## Proof and recovery

First step: run `just test pty` (cwd `/Users/feb/dev/cartridge`) and record the baseline,
including the two known failures in release-status; reproduce the delayed-mark case in
`.cartridge/tests/integration/process.rs` without a live user terminal. Gate: the same command.
Rollback: fields and the wait op are additive; old callers keep text results, and the shared
shell PID is never restarted by this change.

## Dependencies and review

Ready: shell identity is done. [Review history](review.md); rounds inherited from `improve-pty-command-wait`; limit five.
