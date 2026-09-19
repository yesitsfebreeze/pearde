---
state: "done"
origin: requested
priority: 75
repo: "/Users/feb/dev/cartridge/agent.ctg"
footprint:
  - /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/integration/loop.rs
commit: "17e27b74f7126165a93ff46b531b5e78481bcd31"
---

# the agent's integration harness does not inherit CARTRIDGE_YOLO

The slug of this PRD still reads `a-denied-tool-call-journals-its-error-flag`.
That is the name it was filed under on 2026-09-19, from a misdiagnosis, and it
is retained because the address is already cited from
`@agent/an-event-declares-its-type`. The outcome below is the real one.

## Outcome

The agent's integration tests measure the agent, not the shell they were
launched from. `just test agent` produces the same result whether or not
`CARTRIDGE_YOLO` is set in the environment, because the harness removes that
variable when it spawns the base binary. A run under a `--yolo` launched session
can no longer report a green suite as red.

## Evidence

Measured 2026-09-19 by probe, in a throwaway rsync copy at
`/tmp/analyst-denyflag/probe`; the shared checkout was untouched, `git status
--porcelain` empty before and after, HEAD `620857d`.

The PRD as originally filed claimed that a policy-denied tool call journals
`result.error == false` and that the flag was lost between
`agent.ctg/src/lib.rs:658` and `:758` or `:776`. **No line loses it.**
`error: true` is never minted, because the policy is never consulted: the read
is allowed, the tool really runs, and `error: false` is the correct journal
entry for what happened.

The cause is `CARTRIDGE_YOLO=1` in the environment of the session that ran the
gate, which `just launch claude --yolo` sets. The host merges `yolo: true` into
every cartridge declaring that setting
(`cartridge.ctg/src/settings/mod.rs:15-16`, `transport/settings.rs:188-192`),
and `agent.ctg/src/lib.rs:634` then skips the entire policy branch.
`.cartridge/tests/integration/loop.rs:165` (`Base::cli`) and `:201` (`start`)
spawn the base binary without `env_remove`, so the daemon inherits it.

Three probes establish that the branch never runs, rather than inferring it from
a reading:

- a recording policy fixture reported `PROBE policy seen = []` — never called —
  while `tool.read` was nonetheless dispatched with `{"path":"a"}`;
- a policy returning `bogus-decision` still produced `phase: "completed"`,
  where `lib.rs:637-652` would have returned `Err("invalid policy decision")`
  had it executed;
- an `emit` probe above `lib.rs:634` reported `"yolo": true` for both tools,
  though `cartridge.json` defaults it false and the test profile never sets it.

The variable is the sole discriminator, with the tree and the test unmodified:

| command | exit |
| --- | --- |
| `env -u CARTRIDGE_YOLO cargo test -p agent --test loop` | 0 — 13 passed, 0 failed |
| `CARTRIDGE_YOLO=1 cargo test -p agent --test loop` | 1 — 12 passed, 1 failed |
| `env -u CARTRIDGE_YOLO just test agent` | 0 — `test agent pass` |
| `just test agent` (variable inherited) | 1 — `test agent FAIL` |
| `env -u CARTRIDGE_YOLO just check agent` | 0 — pass, `isolation composition pass` |

Consequence for the board: `just test agent` is **not** red at HEAD. It is red
only when run from a `--yolo` launched shell, which is every coordinator and
worker session on this machine. Any agent-board PRD blocked on that gate was
blocked on a measurement artifact. Under `yolo`, bypassing policy is the
declared behaviour (`agent.ctg/cartridge.json:103`), so there is nothing to fix
in `src/lib.rs`; what is wrong is that the harness is not hermetic.

## Acceptance

- [x] `.cartridge/tests/integration/loop.rs` removes `CARTRIDGE_YOLO` from the
      environment of every base binary it spawns, at `:165` (`Base::cli`) and
      `:201` (`start`). The precedent in the tree is
      `memory.ctg/src/hub/src/lib.rs:121` and `commands_hub.rs:454`, which do
      this with `TAKEOVER_ENV`.
- [x] `multiple_tool_calls_execute_and_persist_in_response_order` passes with
      `CARTRIDGE_YOLO=1` exported, and the assertion at `loop.rs:798` is
      unchanged: the fix is in the harness, not in the test and not in
      `src/lib.rs`.
- [x] The whole `loop` target passes under both `CARTRIDGE_YOLO=1` and
      `env -u CARTRIDGE_YOLO`, and the two runs agree.
- [x] No behavioural change to `src/lib.rs`. If the eventual diff touches it at
      all, the spec says why in a sentence.
