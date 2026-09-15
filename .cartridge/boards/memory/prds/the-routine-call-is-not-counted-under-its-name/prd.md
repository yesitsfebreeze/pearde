---
repo: /Users/feb/dev/cartridge/memory.ctg
state: done
origin: requested
priority: 50
blast-radius: mid
workflow: develop-one-cartridge
capability-owner: memory
work-kind: leaf
---

# a `routine:<leaf>` MCP call is dispatched as an operation of its own and counted under its own name — the claim this part's title makes is false as of `6a0daf0d`

The title states what was true when this part was written and is false now; it
stands because a part is cited by its name and an edit adds rather than deletes
the sentence it corrects ([[SYSTEM]]). What it says — that `routine_answer`
composes the answer in the client out of two `part` operations, so the ledger
counts a routine as the reads it borrowed and holds no `routine:` key — was
measured on a scratch record that left `reflex.json` reading
`{"counts": {"part": 3}}`. The `Do` below then landed as `6a0daf0d` and the
ledger counts the routine, which is what [routines-are-tools](../routines-are-tools/prd.md) needs for
`reflex {action: draw}` to draw a routine by its own use instead of as cold
forever.

## Do

Add the `routine:` arm to the match in `Server::invoke`
(`src/rpc/src/server.rs:127-152`): a name carrying the prefix resolves its leaf
against the watched roots the way `crate::part` already resolves a path, reads
that part, strips the front matter and answers the body with the optional
`input` at its head. Then cut `routine_answer`
(`src/commands/src/commands_mcp.rs`) down to one `route_to(node, name, args)`
— the composition moves behind the operation, `tools/list` keeps `routines()`
and `ROUTINE_SCHEMA` as they are, and the count lands because the dispatched
name is the routine's. `src/rpc/src/reflex.rs` is not touched.

## Acceptance
`cargo test --test dynamic_surface` — the test already serves a `Reflex::open`
on a temp ledger, so the third clause of [routines-are-tools](../routines-are-tools/prd.md)'s Check is one
assertion after the existing `tools/call` on `routine:polish`: read
`<ledger>/reflex.json` and hold `counts["routine:polish"]` at 1, with the
`part` count unchanged by that call.

Run today, green: `test every_declared_routine_is_a_tool_that_answers_with_its_part
... ok`. The landed assertion (`tests/dynamic_surface.rs:157-162`) holds
`counts["routine:polish"]` at 2 rather than 1 because the test now calls the
routine twice — once bare, once with an `input` — so the ledger is measured as
one count per call, which is the same claim counted twice.

The second clause is not an assertion but a call graph, and it holds: the only
`self.reflex.record(name)` in the tree is `src/rpc/src/server.rs:125`, at the
head of `Server::invoke`, and `tool_routine` (`src/rpc/src/server.rs:157`)
reaches the record through `crate::part::invoke` directly (lines 168 and 180)
instead of re-entering `invoke`, so the two reads a routine is still made of are
invisible to the ledger. The one `part` dispatch left in the flow is
`routines()` (`src/commands/src/commands_mcp.rs:172`) serving `tools/list`,
which is a different call from a different client turn.
