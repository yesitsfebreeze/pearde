---
state: "analyzing"
origin: requested
priority: 40
repo: "/Users/feb/dev/cartridge/harness.ctg"
footprint:
  - /Users/feb/dev/cartridge/harness.ctg/.cartridge/tests/integration/support.rs
claim: "coordinator-codex-18 2026-09-19T19:18:24.547Z"
---

# the harness test support spawns a base with a clean environment

## Outcome

The harness integration tests measure the harness, not the shell they were
launched from. `support.rs` removes `CARTRIDGE_YOLO` from the environment of
every base binary it spawns, so a run from a `--yolo` launched session composes
and trusts exactly as a run from a plain one.

## Evidence

Filed 2026-09-19 from a finding by the reviewer of
`@agent/a-denied-tool-call-journals-its-error-flag`, which swept the composition
for harnesses with the same hole and named seven. This is the harness one, and
it is filed here rather than left in that PRD's report because a loop directory
is cleaned and a finding left there evaporates.

`harness.ctg/.cartridge/tests/integration/support.rs` spawns the base binary
twice, at `:112` (the daemon, `Command::new(base()).current_dir(dir).env(
"CARTRIDGE_HOME", dir)`) and at `:142` (`cli`, the same shape). Both set
`CARTRIDGE_HOME` to an isolated directory and neither removes any variable from
the inherited environment. `just launch claude --yolo` exports
`CARTRIDGE_YOLO=1` in every session on this machine, so both spawns inherit it.

**This one is latent, not live, and the PRD should not overstate it.** Probed
2026-09-19: only `agent.ctg`, `memo.ctg` and `proxy.ctg` declare a `yolo`
setting, and `harness.ctg/cartridge.json` does not. The composition these tests
build therefore contains no cartridge whose behaviour the variable changes
through settings. What it still reaches is the trust check
(`cartridge.ctg/src/trust/mod.rs:94`), where the variable makes an untrusted
file trusted — the same mechanism that flips
`lua::tests::each_file_is_evaluated_in_a_state_of_its_own` in `cartridge.ctg`.
So today the tests pass either way, and the defect is that they would not
notice a trust regression when run from a `--yolo` shell.

Priority 40 reflects exactly that: a real hermeticity gap with no current
failure behind it. It should not be ranked against rows that are fixing
something observably broken.

## Acceptance

- [ ] `support.rs` removes `CARTRIDGE_YOLO` from the environment of the base
      binary at both spawn sites, `:112` and `:142`. The precedent in the tree
      is `memory.ctg/src/hub/src/lib.rs:121` and
      `memory.ctg/src/commands/src/commands_hub.rs:454`, which strip
      `TAKEOVER_ENV` at their spawn sites for the same reason.
- [ ] The harness integration target passes with `CARTRIDGE_YOLO=1` exported and
      under `env -u CARTRIDGE_YOLO`, and the two runs agree.
- [ ] The spec states whether a blanket `CARTRIDGE_*` scrub was considered and
      rejected. It must be rejected: these spawns depend on `CARTRIDGE_HOME`
      for their isolation, and removing it would break the very property the
      comment at `support.rs:109-111` describes.
- [ ] A test proves trust is enforced in the spawned composition, so the gap
      this PRD closes has a witness rather than only a diff. Without it the
      change is unobservable and the next refactor can undo it silently.

## Related

Same defect, different harness, already `claimed` with an implementer in its
lane: `@agent/a-denied-tool-call-journals-its-error-flag` (slug stale; the
outcome is the hermetic agent harness). The live case is on the root board,
`.cartridge/tests/integration/smoke.test.ts:118`, whose composition does include
`proxy` and `memo`. The remaining latent cases belong to other boards and their
coordinators have been told the file and line:
`mcp.ctg/.cartridge/tests/integration/instances.test.ts:22,120,136`,
`tools.ctg/.cartridge/tests/integration/lane.test.ts:48`,
`pty.ctg/.cartridge/tests/integration/process.rs:108,136`,
`memory.ctg/.cartridge/tests/integration/cartridge.rs:103,116,154` and
`docs.ctg/.cartridge/tests/host.rs:76`.

The root cause of the whole family is
`@root/the-composition-s-gates-do-not-inherit-cartridge-yolo`, held by
coordinator-4b-1, which strips the variable in the gate itself. If that lands
first this row shrinks to the witness test, because the gate will no longer pass
the variable down. It does not make this row redundant: a test harness invoked
directly rather than through `just` would still inherit it.
