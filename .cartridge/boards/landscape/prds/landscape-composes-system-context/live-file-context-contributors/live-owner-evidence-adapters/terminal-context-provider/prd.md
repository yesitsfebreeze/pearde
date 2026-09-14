---
repo: /Users/feb/dev/cartridge/pty.ctg
state: open
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: pty
work-kind: leaf
review-round: 3
review-status: passed
canonical-scope: landscape-composes-system-context/live-file-context-contributors/live-owner-evidence-adapters/terminal-context-provider
needs:
- "@memo/landscape-live-owner-context-facade"
- "@pty/context-terminal-metadata"
footprint:
- /Users/feb/dev/cartridge/pty.ctg/cartridge.json
- /Users/feb/dev/cartridge/pty.ctg/init.lua
- /Users/feb/dev/cartridge/pty.ctg/src/context.rs
- /Users/feb/dev/cartridge/pty.ctg/.cartridge/tests/unit/context/tests.rs
---

# Pty answers context with terminal lifecycle metadata

pty has a bounded observation of an existing shared terminal (`src/context.rs`, schema `pty.context.v1`: shell identity, lifecycle and control state, no screen, command, output or title). `@pty/context-terminal-metadata` finishes that observation. This leaf makes pty define and listen to `context.terminal`, answering memo's `contribute` and `read` shapes (`memo.ctg/.cartridge/docs/context.md`) for the terminal that belongs to the trusted `scope`.

## Acceptance

- [ ] A memo `context` prepare naming `terminal` returns one row with `reference.kind: terminal` for the active terminal. It carries only the `pty.context.v1` allowlist and a stable revision.
- [ ] Contribute and read never start a terminal, take input ownership or advance a screen cursor. With no active terminal the state is `unavailable`.
- [ ] After the shell exits or is replaced, readback of an earlier reference is `changed`, not a substitute row. With pty removed from the composition, `terminal` is `absent`.

## Proof and recovery

Probe first: whether the shared terminal can be tied to the scoped session, or is global to the composition. If it is global, state that in `.cartridge/docs/context.md` and ignore `scope`. Extend `.cartridge/tests/unit/context/tests.rs` and `.cartridge/tests/integration/process.rs`. Gates, cwd `/Users/feb/dev/cartridge`: `just test pty`, `just check pty`, `just isolation`. Not run. Rollback: remove the event.

## Dependencies and review

Needs the specced pty metadata leaf and memo's scope facade. Rounds 1–2 are inherited; this leaf was created by the round-3 split ([review](review.md)).
