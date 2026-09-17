---
state: open
origin: requested
priority: 30
repo: "/Users/feb/dev/cartridge"
work-kind: leaf
canonical-scope: cli-spec-cartridge
footprint:
  - "cli.ctg"
---

# An external command is learned once and driven from its spec

An agent driving an unfamiliar command line re-derives its surface every session, from help output it re-reads or from memory of a version that may have moved. Port pi's `cli` as `cli.ctg`: explore a binary once, record its command surface, then drive it from that record.

Learning explores the binary however it wants to be explored — help output, the subcommand tree, man pages, completion scripts — and records commands, flags, positionals, gotchas and a read-only classification per command. The record is machine-level, not repository-level, because an installed binary is a fact about the machine, and it is keyed by the version it was learned against, so a binary upgrade reports a stale spec instead of confidently describing commands that were renamed.

Running goes through an explicit argument vector, never a shell string, so nothing is word-split or glob-expanded. The run reports which command it matched, any flag the spec does not declare, and whether the command mutates state. An argument vector the spec does not match still runs and says so: a spec is one exploration pass, not a grammar.

## Acceptance

- [ ] Learning a fixture binary records its commands, flags, positionals and a read-only classification per command, keyed by the binary's version.
- [ ] Running against a spec learned for a different version reports a stale spec and names both versions, rather than answering from the old surface.
- [ ] A run is invoked with an explicit argument vector and no shell: an argument containing spaces, a glob character and a semicolon reaches the binary as one unmodified argument.
- [ ] A run reports the matched command by longest subcommand path, names every flag the spec does not declare, and states whether the matched command mutates state.
- [ ] An argument vector matching no command in the spec still runs and is reported as unmatched.
- [ ] A command classified as mutating is decided by `policy.ctg` before it runs; a read-only one is not gated on that decision.
- [ ] Learning, matching and staleness are tested offline in `just test cli` against fixture binaries; no real network tool is invoked.

## Proof and recovery

Port from `/Users/feb/dev/pi/packages/coding-agent/src/core/cli/` (889 lines at survey, verified present). Upstream stores specs under a home directory path of its own and dispatches learning to its own sub-agent chassis; here the store is the composition's machine-level state and learning dispatches through `agent.ctg`.

Gates, cwd `/Users/feb/dev/cartridge`: `just test cli`, `just check cli`. Not run for this plan.
