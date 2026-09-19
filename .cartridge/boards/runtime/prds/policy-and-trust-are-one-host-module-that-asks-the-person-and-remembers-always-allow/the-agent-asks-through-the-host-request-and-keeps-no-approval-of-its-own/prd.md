---
state: open
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/agent.ctg"
capability-owner: runtime
needs:
  - '@runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/a-consumer-raises-an-approve-or-input-request-and-a-person-answers-it-from-the-command-line'
footprint:
  - /Users/feb/dev/cartridge/agent.ctg/src/lib.rs
  - /Users/feb/dev/cartridge/agent.ctg/src/module.rs
  - /Users/feb/dev/cartridge/agent.ctg/cartridge.json
  - /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/unit/run_state.rs
  - /Users/feb/dev/cartridge/agent.ctg/.cartridge/tests/integration/loop.rs
  - /Users/feb/dev/cartridge/agent.ctg/README.md
  - /Users/feb/dev/cartridge/agent.ctg/.cartridge/help.md
---

# the agent asks through the host request and keeps no approval of its own

## Outcome

on `ask`, `prepare_tool` calls `policy.request {kind:"approve", operation:{tool, op}, summary}` with no tool input in the summary, and maps `allowed` to run and anything else to `permission denied`. The following are deleted: `Approval`, `live.pending`, `fn approve`, `fn answer`, the `answer` op in `cartridge.json` and `module.rs`, the `awaiting_approval` phase and `approval_requested` kind, and `approval_timeout_secs`, which becomes the request's `timeout_ms`. `cartridge.json` needs `policy.request`.

## Acceptance

- [ ] Named test in `loop.rs`: an `ask` decision raises exactly one `policy.request` whose summary carries no input. `allowed` runs the tool, and `denied` and `timed_out` return `permission denied`.
- [ ] `grep -n 'awaiting_approval\|approval_requested\|"answer"' src cartridge.json` finds nothing, and `just test agent` and `just check agent` pass.

## Provenance

Child 6 of 7 of @runtime/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow, split 2026-09-19 by coordinator cartridge-4b from its analyst report (base cartridge.ctg 324f36e). Review rounds used: 0 of 5 (the parent had no review.md). Evidence: the parent `## Split` section and `.state/loop/policy-and-trust-are-one-host-module-that-asks-the-person-and-remembers-always-allow/analyst-1.md`.

## Notes from cartridge-eb, which owns the agent board (2026-09-19)

- The approval path to delete, measured on the live tree: `struct Approval` at `agent.ctg/src/lib.rs:109`, `pending: Option<Approval>` at `:124`, `load_pending` at `:229`, the `"answer"` dispatch arm at `:246`, the pending/snapshot check at `:400-404`, the cancel path that sends `false` at `:421-422`, `live.pending = None` at `:581`, and `approve` at `:854-869`.
- `@agent/an-event-declares-its-type` (in `question`) relies on `record()` at `src/lib.rs:203` being the single choke point for the journal kinds. Tell cartridge-eb the final kind set when this lands.
- `@agent/a-denied-tool-call-journals-its-error-flag` has a lane on `.cartridge/tests/integration/loop.rs`, cut from `620857d`. Whichever of the two lands second checks `git -C agent.ctg status --porcelain` before collecting.
- `agent.ctg/src/lib.rs:634` skips the whole policy branch when `config.yolo` is set, and `CARTRIDGE_YOLO=1` reaches the integration harness. Setting `yolo = false` in the test profile does not help, because `settings::apply` merges the environment's value over it (`cartridge.ctg/src/transport/settings.rs:126-145`). Measure with `env -u CARTRIDGE_YOLO`.
