---
state: "done"
origin: requested
priority: 100
repo: "/Users/feb/dev/cartridge/cartridge.ctg"
work-kind: leaf
capability-owner: runtime
footprint:
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/mod.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/src/asp/protocol.rs
  - /Users/feb/dev/cartridge/cartridge.ctg/docs/asp.txt
  - /Users/feb/dev/cartridge/cartridge.ctg/.cartridge/tests/unit/src/asp.rs
commit: "2ea1aae611499b3210b6c363b55d56c2d20853a7"
---

# an asp action's args are the tool's input

## Outcome

An action's `args` is the named tool's input, exactly what an agent passes to that tool, and never the `{op, input, context}` envelope a harness wraps around it. The first two real providers disagreed on 2026-09-19: fs declared the whole envelope and memo declared the input. An agent reads an action and calls the tool with `args`, so the input is the only shape it can use. The command line's `act` wraps the envelope itself, as `{op: "call", input: args}`, with no caller context.

## Acceptance

- [x] A named test runs an action through `act`, and the tool receives `{op: "call", input: <args>}`.
- [x] `docs/asp.txt` and `protocol.rs` state the rule.
